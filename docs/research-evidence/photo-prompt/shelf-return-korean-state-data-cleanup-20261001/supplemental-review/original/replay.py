"""Read-only cycle15 supplemental diagnostic. No paid calls, no repo writes.
Run: PYTHONDONTWRITEBYTECODE=1 python3 /tmp/cycle15-hybrid-review/replay.py
"""
from pathlib import Path
import sys,json,copy,hashlib,socket,urllib.request,random
from decimal import Decimal
R=Path('/workspace/scratch/ce8f20680f5a/image-prompt');E=R/'docs/research-evidence/photo-prompt/shelf-return-korean-state-data-cleanup-20261001';O=Path(__file__).parent
sys.path[:0]=[str(E),str(R)]
def deny(*a,**k):raise AssertionError('NETWORK/API/CREDENTIAL/REPO WRITE FORBIDDEN')
socket.create_connection=deny;socket.socket.connect=deny;urllib.request.urlopen=deny;urllib.request.build_opener=deny
import cycle_common as c
from bm25f_retrieval import rank_bm25f
g=c.g;c.write_json=deny;g.get_gemini_api_key=deny;g.cached_gemini_client=deny;g.embed_texts_with_gemini=deny
f=c.load_freeze();D=c.states_from_freeze(f);q=next(x for x in f['queries']if x['id']=='coexistence_en');cache=c.read_json(E/'new-vector-cache.json');v=cache[q['query_sha256']];c.validate_vector(v,q['query']);assert c.sha(q['query'].encode())==q['query_sha256'];T=c.TARGET;F='slot:aftermath_trace:localized_extinguished_flame_trace'
result={'query':q['query'],'query_sha256':q['query_sha256'],'freeze_sha256':c.sha((E/'frozen-inventory-queries.json').read_bytes()),'raw_query_vector_sha256':c.objsha(v['vector']),'cache_metadata':{k:x for k,x in v.items()if k!='vector'},'states':{},'network_calls':0,'source_hashes':{str(p.relative_to(R)):c.sha(p.read_bytes())for p in [E/'new-vector-cache.json',E/'evaluate_cycle.py',R/'skills/photo-prompt-image-generator/scripts/prompt_generator.py',R/'skills/photo-prompt-image-generator/scripts/bm25f_retrieval.py']}}
B={}
for state,data in D.items():
 b=g.build_semantic_bm25f_payload(data);B[state]=b;ids=['slot:aftermath_trace:'+x['id']for x in data['slots']['aftermath_trace']];ranked=rank_bm25f(b,{'query':q['query']},allowed_ids=ids,limit=len(ids));saved=next(x for x in c.read_json(E/'ranking-results.json')if(x['state'],x['method'],x['query_id'])==(state,'lexical','coexistence_en'));assert ranked==saved['full_ranking']
 found={key:{'rank':i,'score':row['score'],'matched_terms':row['matched_terms']}for i,row in enumerate(ranked,1)for key in[T,F]if row['document_id']==key}
 result['states'][state]={'dictionary_hash':g.dictionary_hash(data),'lexical_full_ranking':ranked,'lexical_focus':found,'target_minus_flame_margin':str(Decimal(str(found[T]['score']))-Decimal(str(found[F]['score']))),'bm25f_average_lengths':b['average_field_lengths'],'focus_document_fields':{key:b['documents'][key]for key in[T,F]}}
a=result['states']['baseline']['lexical_focus'];z=result['states']['proposal']['lexical_focus'];result['lexical_deltas']={key:str(Decimal(str(z[key]['score']))-Decimal(str(a[key]['score'])))for key in[T,F]};result['lexical_deltas']['target_minus_flame_margin']=str(Decimal(result['states']['proposal']['target_minus_flame_margin'])-Decimal(result['states']['baseline']['target_minus_flame_margin']))
print('Lexical focus and exact decimal deltas:',json.dumps({'before':a,'after':z,'deltas':result['lexical_deltas']},ensure_ascii=False),flush=True)
# Inventory exact-text vector cache coverage without attempting a fallback.
axes=g.extract_intent_axes(q['query'],None,'auto','user',D['proposal']);texts=[{'role':'raw_query','text':g.clean_spaces(q['query'])}]+[{'role':'default_axis','text':g.semantic_axis_embedding_text(x['text'],D['proposal']),'axis_text':x['text']}for x in axes['items']]
fixture=c.read_json(E/'scout/generated-contract.json');core=fixture['provenance']['authorial_core'];expanded,prov=g.authorial_core_retrieval_text(core,q['query']);texts.append({'role':'existing_scout_core_query','text':expanded,'core_source_request':core['source_request'],'caveat':'The saved core belongs to a different shorter request. It cannot stand in for the full frozen coexistence query.'})
need={c.sha(t['text'].encode()):t['text']for t in texts};hits={h:[]for h in need};paths=set((R/'docs/research-evidence/photo-prompt').rglob('*cache*.json'))|set((R.parent/'daylong-progress').rglob('*cache*.json'));scanned=[]
for p in sorted(paths):
 if p.stat().st_size>30_000_000:continue
 try:obj=c.read_json(p)
 except(Exception):continue
 scanned.append(str(p))
 def scan(x):
  if isinstance(x,dict):
   if isinstance(x.get('text'),str)and isinstance(x.get('vector'),list):
    h=c.sha(x['text'].encode())
    if h in need and x['text']==need[h]:
     try:c.validate_vector(x,need[h])
     except Exception:return
     hits[h].append({'path':str(p),'vector_sha256':c.objsha(x['vector']),'model':x.get('model'),'dimensions':x.get('dimensions')})
   else:
    for value in x.values():scan(value)
  elif isinstance(x,list):
   for value in x:scan(value)
 scan(obj)
for t in texts:t['sha256']=c.sha(t['text'].encode());t['compatible_exact_text_model_dimension_cache_hits']=hits[t['sha256']]
result['cache_coverage']={'axes':axes,'texts':texts,'cache_files_scanned':scanned,'production_task_type':'SEMANTIC_SIMILARITY','evaluator_task_type_field':'omitted','task_type_documentation':'https://ai.google.dev/gemini-api/docs/embeddings#task-types','task_type_caveat':'Official documentation says gemini-embedding-2 does not support task_type. No live request equivalence was tested. This is not evidence of differing vector semantics; raw cached vectors are used only at a named ranker-stage seam.'}
print('Cache coverage:',json.dumps([{'role':t['role'],'sha256':t['sha256'],'text':t['text'],'hits':len(t['compatible_exact_text_model_dimension_cache_hits'])}for t in texts],ensure_ascii=False),flush=True)
base,_=c.load_baseline_index(f,D['baseline']);proposal=g.load_semantic_index(c.A/'photo_prompt_semantic_index.json',D['proposal']);IX={'baseline':base,'proposal':proposal}
# A strict supported default-context attempt; returns cache-only and stops before API on first missing axis.
calls=[]
def cached_only(text,model,dimensions,api_key):
 calls.append({'text':text,'sha256':c.sha(text.encode()),'model':model,'dimensions':dimensions})
 record=cache.get(c.sha(text.encode()))
 if not record:raise RuntimeError('NO_EXACT_CACHED_VECTOR: '+c.sha(text.encode()))
 c.validate_vector(record,text);assert model==record['model']and dimensions==record['dimensions'];return record['vector']
g.embed_single_semantic_text=cached_only
try:
 g.make_semantic_context(D['proposal'],q['query'],'hybrid','medium',semantic_index=proposal)
 raise AssertionError('Expected missing default axis')
except RuntimeError as exc:result['default_hybrid_context_attempt']={'status':'blocked_before_shortlist','error':str(exc),'embedding_requests':calls.copy(),'api_fallback':'forbidden'}
# The supported axis-off option still canonicalizes the full query's product family.
# Do not bypass this production behavior or invent missing vectors.
calls.clear()
try:
 g.make_semantic_context(D['proposal'],q['query'],'hybrid','medium',semantic_index=proposal,semantic_axis_mode='off')
 raise AssertionError('Expected uncached family embedding even with axis off')
except RuntimeError as exc:result['supported_axis_off_attempt']={'status':'blocked_before_shortlist','error':str(exc),'embedding_requests':calls.copy(),'api_fallback':'forbidden','note':'Axis-off is a nondefault option checked only to establish that it still needs an uncached canonical product-family vector. No shortlist was computed.'}
result['conclusion']={'natural_default_hybrid':'Not replayable from available exact vectors: all three default derived axes are absent. No full-query V6 authorial core and its expanded embedding are available.','ranker_stage':'Not claimed. Even the supported axis-off option requests the uncached canonical product-family text. Suppressing this or inventing vectors would be a different context, so no fake successful shortlist is presented.','lexical_harm':'Target falls from 5 to 6, unrelated extinguished flame enters top five from 6. Top12 membership stability does not remove that loss.'}
(O/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('WROTE',str(O/'result.json'),flush=True)
