"""Durable, request-bound embeddings. Offline local or explicit Gemini."""
from __future__ import annotations
import base64, hashlib, json, math, os, time, uuid
from pathlib import Path
from datetime import datetime, timezone
from photo_candidate_corpus import canonical_bytes, digest, decode
import fcntl

GEMINI_SPACE={'provider':'gemini','model':'gemini-embedding-2','dimensions':768}
SPACE=GEMINI_SPACE # Compatibility for historical fixtures; not runtime selection.

def validate_space(space):
    if space==GEMINI_SPACE:return space
    if not isinstance(space,dict) or space.get('provider')!='embeddinggemma2-local' or space.get('dimensions')!=768:
        raise ValueError('unsupported embedding space')
    from photo_local_embedding import space as local_space
    if space!=local_space():raise ValueError('foreign local embedding space')
    return space

def default_space():
    root=Path(__file__).resolve().parents[1]
    backend=os.environ.get('PHOTO_EMBEDDING_BACKEND')
    config=root/'embedding-default.json'
    if backend is None:backend=decode(config.read_bytes())['provider'] if config.is_file() else 'gemini'
    if backend=='gemini':return dict(GEMINI_SPACE)
    if backend!='embeddinggemma2-local':raise ValueError('unknown embedding backend')
    from photo_local_embedding import space as local_space
    return local_space()

def validate_execution(trace,space,text,vector,kind='query'):
    validate_space(space)
    if trace.get('provider_executed') is not True:raise ValueError('embedding was not executed')
    if space==GEMINI_SPACE:
        if trace.get('http_status')!=200 or not isinstance(trace.get('response_sha256'),str) or len(trace['response_sha256'])!=64 or any(c not in '0123456789abcdef' for c in trace['response_sha256']):
            raise ValueError('missing successful Gemini response evidence')
        return
    from photo_local_embedding import runtime_lock,digest as local_digest,model_inputs
    lock=runtime_lock()
    if (trace.get('schema')!='photo-local-inference/v1' or trace.get('space')!=space
            or trace.get('runtime')!=lock['runtime'] or trace.get('installation_sha256')!=local_digest(lock)
            or trace.get('kind')!=kind or trace.get('input_sha256')!=hashlib.sha256(model_inputs([text],kind)[0].encode()).hexdigest()
            or trace.get('vector_sha256')!=digest(vector) or trace.get('http_status') is not None):
        raise ValueError('invalid local inference evidence')

def atomic(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.write-'+uuid.uuid4().hex)
    with temporary.open('wb') as stream:
        stream.write(canonical_bytes(value));stream.flush();os.fsync(stream.fileno())
    os.replace(temporary,path)

def validate_vector(vector, dimensions=768):
    if (not isinstance(vector,(list,tuple)) or len(vector)!=dimensions
            or any(type(x) not in (int,float) or not math.isfinite(x) for x in vector)
            or sum(x*x for x in vector)<=0):
        raise ValueError('embedding must be a finite nonzero vector in the bound space')
    return vector

def load_env(path):
    path=Path(path)
    if path.is_file():
        for raw in path.read_text().splitlines():
            line=raw.strip()
            if line.startswith('export '):line=line[7:]
            if not line or line.startswith('#') or '=' not in line:continue
            name,value=line.split('=',1);name=name.strip();value=value.strip().strip("\"'")
            if name in {'GEMINI_API_KEY','GOOGLE_API_KEY'} and value:os.environ.setdefault(name,value)

def embed(text, binding, cache, *, space=None, repair_unknown=False,kind='query'):
    space=dict(space or default_space());validate_space(space)
    if space!=GEMINI_SPACE:
        return embed_many([text],[binding],cache,space=space,kind=kind)[0]
    if kind not in {'query','document'}:raise ValueError('embedding kind must be query or document')
    request={'schema':'photo-embedding-request/v1','text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),
             'space':space,'binding':binding}
    key=digest(request);directory=Path(cache)/key;directory.mkdir(parents=True,exist_ok=True)
    with (directory/'LOCK').open('a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        result=directory/'RESULT.json'
        if result.is_file():
            row=decode(result.read_bytes())
            if row.get('request')!=request or row.get('vector_sha256')!=digest(row.get('vector')):
                raise ValueError('embedding cache binding/content mismatch')
            validate_vector(row['vector'],space['dimensions'])
            return {**row,'cache_hit':True}
        attempts=list(directory.glob('ATTEMPT-*.json'))
        for path in attempts:
            previous=decode(path.read_bytes())
            if previous['state'] in {'started','unknown'}:
                if not repair_unknown:
                    raise RuntimeError('embedding transport outcome unknown; inspect durable attempt before resending')
                atomic(directory/('REPAIR-'+path.name),{'schema':'photo-embedding-unknown-repair/v1',
                    'original_attempt_sha256':digest(previous),'reason':'explicit maintenance rebuild after durable unknown transport; original evidence retained',
                    'possible_duplicate_provider_cost':True})
            if previous['state']=='failed' and previous.get('http_status') not in {429,500,502,503,504}:
                raise RuntimeError('recorded embedding provider failure; explicit repair is required')
        key_value=os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
        if not key_value:raise RuntimeError('GEMINI_API_KEY or GOOGLE_API_KEY is required for hybrid retrieval')
        from google import genai
        from google.genai import types
        for attempt_number in range(len(attempts),len(attempts)+3):
            attempt_path=directory/f'ATTEMPT-{attempt_number:03d}.json';raw_path=directory/f'RESPONSE-{attempt_number:03d}.json'
            attempt={'request':request,'state':'started','started_at':datetime.now(timezone.utc).isoformat()}
            atomic(attempt_path,attempt);response_record={};sent=False
            def before_send(request):
                nonlocal sent
                if sent:raise RuntimeError('embedding transport repeated unexpectedly')
                sent=True
                atomic(attempt_path,{**attempt,'transport_send_started':True})
            def response_hook(response):
                response.read();body=response.content
                response_record.update({'http_status':response.status_code,'body_sha256':hashlib.sha256(body).hexdigest(),
                    'body_base64':base64.b64encode(body).decode()})
                atomic(raw_path,{'request_sha256':key,**response_record})
            client=genai.Client(api_key=key_value,vertexai=False,http_options=types.HttpOptions(
                timeout=60000,retry_options=types.HttpRetryOptions(attempts=1),
                client_args={'follow_redirects':False,'event_hooks':{'request':[before_send],'response':[response_hook]}}))
            start=time.monotonic()
            try:
                response=client.models.embed_content(model=space['model'],contents=text,
                    config=types.EmbedContentConfig(output_dimensionality=space['dimensions']))
                vector=[round(float(x),6) for x in response.embeddings[0].values]
                validate_vector(vector,space['dimensions'])
                row={'schema':'photo-embedding-result/v1','request':request,'vector':vector,'vector_sha256':digest(vector),
                     'execution':{'provider_executed':True,'http_status':response_record.get('http_status'),
                        'response_sha256':response_record.get('body_sha256'),'elapsed_seconds':round(time.monotonic()-start,4),
                        'attempt':attempt_number,'usage':json.loads(response.model_dump_json()).get('usageMetadata')}}
                atomic(result,row);atomic(attempt_path,{**attempt,'state':'succeeded',**response_record})
                return {**row,'cache_hit':False}
            except Exception as error:
                status=response_record.get('http_status')
                connection_failed=type(error).__module__.startswith('httpx') and type(error).__name__ in {'ConnectError','ConnectTimeout'}
                state='connection_failed' if connection_failed else ('failed' if status else 'unknown')
                atomic(attempt_path,{**attempt,'state':state,'http_status':status,'transport_send_started':sent,'error_type':type(error).__name__})
                if not connection_failed and status not in {429,500,502,503,504}:
                    raise RuntimeError('embedding provider failed; see durable response/attempt (no lexical fallback)') from None
                if attempt_number==len(attempts)+2:raise RuntimeError('embedding provider retry budget exhausted') from None
                time.sleep(min(30,5*(2**(attempt_number-len(attempts)))))
            finally:client.close()
    raise RuntimeError('embedding unavailable')

def embed_many(texts,bindings,cache,*,space=None,kind='query'):
    """Local batches retain per-input locks, attempts, cache and provenance."""
    from contextlib import ExitStack
    space=dict(space or default_space());validate_space(space)
    if len(texts)!=len(bindings):raise ValueError('embedding input/binding cardinality mismatch')
    if space==GEMINI_SPACE:return [embed(t,b,cache,space=space,kind=kind) for t,b in zip(texts,bindings,strict=True)]
    from photo_local_embedding import infer
    requests=[{'schema':'photo-local-embedding-request/v1','text':t,'text_sha256':hashlib.sha256(t.encode()).hexdigest(),
               'space':space,'binding':b,'kind':kind} for t,b in zip(texts,bindings,strict=True)]
    unique={digest(r):r for r in requests};results={};pending=[]
    with ExitStack() as stack:
        for key,request in sorted(unique.items()):
            directory=Path(cache)/key;directory.mkdir(parents=True,exist_ok=True)
            lock=stack.enter_context((directory/'LOCK').open('a+b'));fcntl.flock(lock,fcntl.LOCK_EX)
            path=directory/'RESULT.json'
            if path.exists():
                row=decode(path.read_bytes())
                if row.get('request')!=request or row.get('vector_sha256')!=digest(row.get('vector')):raise ValueError('local cache binding/content mismatch')
                validate_vector(row['vector']);validate_execution(row['execution'],space,request['text'],row['vector'],kind)
                results[key]={**row,'cache_hit':True}
            else:
                attempts=list(directory.glob('ATTEMPT-*.json'));attempt=directory/f'ATTEMPT-{len(attempts):03d}.json'
                atomic(attempt,{'request':request,'state':'started','started_at':datetime.now(timezone.utc).isoformat()})
                pending.append((key,request,directory,attempt))
        if pending:
            try:
                rows=infer([r['text'] for _,r,_,_ in pending],kind,space)
                for (key,request,directory,attempt),value in zip(pending,rows,strict=True):
                    vector=value['vector'];validate_vector(vector);validate_execution(value['execution'],space,request['text'],vector,kind)
                    row={'schema':'photo-embedding-result/v1','request':request,'vector':vector,'vector_sha256':digest(vector),'execution':value['execution']}
                    atomic(directory/'RESULT.json',row);atomic(attempt,{'request':request,'state':'succeeded','vector_sha256':row['vector_sha256']})
                    results[key]={**row,'cache_hit':False}
            except Exception as error:
                for _,request,_,attempt in pending:atomic(attempt,{'request':request,'state':'failed','error_type':type(error).__name__})
                raise
    return [results[digest(r)] for r in requests]
