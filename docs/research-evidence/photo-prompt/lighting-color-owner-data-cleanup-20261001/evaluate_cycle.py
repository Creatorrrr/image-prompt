"""Frozen bounded DATA evaluation; paid work requires explicit --execute.

This is an evidence runner, never imported by production retrieval.
"""
from pathlib import Path
import argparse,copy,datetime,gzip,hashlib,json,math,os,sys,tempfile,time,urllib.request,urllib.error
R=Path(__file__).resolve().parents[4];A=R/'skills/photo-prompt-image-generator/assets'
E=Path(__file__).resolve().parent
sys.path.insert(0,str(A.parent/'scripts'));import prompt_generator as g
import build_semantic_index as builder
from bm25f_retrieval import rank_bm25f
P=argparse.ArgumentParser();P.add_argument('--execute',action='store_true');P.add_argument('--replay',action='store_true');P.add_argument('--stop-file',type=Path);args=P.parse_args()
F=json.loads((E/'frozen-inventory-queries.json').read_text());assert hashlib.sha256((E/'frozen-inventory-queries.json').read_bytes()).hexdigest()==(E/'frozen-sha256.txt').read_text().split()[0]
B=json.loads(gzip.decompress((E/'baseline-merged-data.json.gz').read_bytes()));assert g.dictionary_hash(B)==F['baseline_dictionary_hash']
with tempfile.NamedTemporaryFile(dir=A,suffix='.json',delete=False) as f:
 baseline_manifest=Path(f.name);f.write((E/'baseline-index-manifest.json').read_bytes())
try:old=g.load_semantic_index(baseline_manifest,B)
finally:baseline_manifest.unlink()
D=g.load_json(A/'photo_prompt_tags.json');expected=copy.deepcopy(B)
for r in F['inventory']:
 rows=expected['slots'][r['slot']];i=next(i for i,e in enumerate(rows)if e['id']==r['id']);assert rows[i]==r['before'];rows[i]=r['proposed_after']
assert D['slots']==expected['slots'],'Merged slots must equal frozen field edits'
assert all(D[k]==expected[k] for k in expected if k not in ['slots','candidate_bundles'])
allowed_owner_pairs={(r['before']['relations'][0]['object'],r['proposed_after']['relations'][0]['object'])for r in F['inventory']if r['decision']=='fix'and r['before'].get('relations')}
def differences(a,b,path=()):
 if isinstance(a,dict)and isinstance(b,dict):
  assert a.keys()==b.keys(),path
  for k in a:yield from differences(a[k],b[k],path+(str(k),))
 elif isinstance(a,list)and isinstance(b,list):
  assert len(a)==len(b),path
  for i,(x,y)in enumerate(zip(a,b)):yield from differences(x,y,path+(str(i),))
 elif a!=b:yield path,a,b
bundle_diffs=list(differences(B['candidate_bundles'],D['candidate_bundles']))
for path,a,b in bundle_diffs:assert path[-1]=='object'and(a,b)in allowed_owner_pairs,(path,a,b)

work=[]
for k,kind,e,s in g.iter_semantic_entries(D):
 text=g.semantic_text_for_entry(e,s,kind=kind)
 if old['entries'][k]['text']!=text:work.append({'kind':'document','key':k,'text':text})
assert len(work)==5
work += [{'kind':'query','key':q['id'],'text':q['query']}for q in F['queries']]
cache_path=E/'new-vector-cache.json';attempt_path=E/'api-attempts.json'
cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
for p in sorted({*E.parent.glob('*/new-vector-cache.json'),*E.parent.glob('*/query-vectors.json')}):
 if p==cache_path:continue
 for h,v in json.loads(p.read_text()).items():
  if v.get('model')==g.SEMANTIC_MODEL_ID and v.get('dimensions')==768 and len(v.get('vector',[]))==768:cache.setdefault(hashlib.sha256(v['text'].encode()).hexdigest(),v)
for e in old['entries'].values():cache.setdefault(hashlib.sha256(e['text'].encode()).hexdigest(),{'text':e['text'],'vector':e['vector'],'model':g.SEMANTIC_MODEL_ID,'dimensions':768})
needed={hashlib.sha256(w['text'].encode()).hexdigest()for w in work};cache={h:v for h,v in cache.items()if h in needed}
pending=[w for w in work if hashlib.sha256(w['text'].encode()).hexdigest()not in cache]
attempts=json.loads(attempt_path.read_text())if attempt_path.exists()else[]
deadline=datetime.datetime.fromisoformat('2026-10-02T11:46:56+00:00')
plan={'model':g.SEMANTIC_MODEL_ID,'dimensions':768,'new_documents':5,'frozen_queries':14,'total_texts':len(work),'maximum_calls':20,'pending_texts':len(pending),'automatic_retries':0,'input_utf8_bytes':sum(len(x['text'].encode())for x in pending),'token_limit_per_input':8192,'price_usd_per_million_tokens':0.20,'price_source':'https://ai.google.dev/gemini-api/docs/pricing','token_limit_source':'https://ai.google.dev/gemini-api/docs/embeddings','price_verified_utc':'2026-10-01T11:52:47Z','additional_conservative_upper_bound_usd':20*8192*0.2/1000000,'previous_tracked_cost_upper_usd':1.0190848,'project_budget_usd':10.0,'budget_limit_note':'tracked cleanup calls; unrelated upstream work has not been reconciled with the billing account','status':'plan_only','deadline_utc':deadline.isoformat()}
if not args.replay:(E/'api-workload.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps({'pending':len(pending),'bound':20,'upper_usd':plan['additional_conservative_upper_bound_usd']}),flush=True)
if not args.execute and not args.replay:raise SystemExit(0)
if args.replay and pending:raise SystemExit('Replay needs existing vectors; no API calls made')
if args.execute:
 builder.load_project_env();key=os.environ.get('GEMINI_API_KEY')or os.environ.get('GOOGLE_API_KEY')
 if not key:raise SystemExit('API configuration absent; no call sent')
 attempted={a['sha256']for a in attempts}
 for w in pending:
  if args.stop_file and args.stop_file.exists():raise SystemExit('Stop requested; saved work preserved')
  if datetime.datetime.now(datetime.timezone.utc)>=deadline:raise SystemExit('Deadline reached; saved work preserved')
  h=hashlib.sha256(w['text'].encode()).hexdigest()
  if h in attempted:raise SystemExit('Prior attempt requires explicit review; automatic retry disabled')
  if len(attempts)>=20 or 1.0190848+(len(attempts)+1)*8192*0.2/1000000>10:raise SystemExit('Bound reached; no call sent')
  rec={'number':len(attempts)+1,'kind':w['kind'],'key':w['key'],'sha256':h,'status':'attempt_started','utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};attempts.append(rec);attempt_path.write_text(json.dumps(attempts,indent=2)+'\n')
  req=urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent',data=json.dumps({'model':'models/gemini-embedding-2','content':{'parts':[{'text':w['text']}]},'outputDimensionality':768}).encode(),headers={'Content-Type':'application/json','x-goog-api-key':key},method='POST')
  try:
   with urllib.request.urlopen(req,timeout=45)as response:out=json.load(response)
   vector=g.round_embedding_vector(out['embedding']['values'],768);assert all(math.isfinite(v)for v in vector)
  except urllib.error.HTTPError as err:
   rec.update(status='failed',http_status=err.code);attempt_path.write_text(json.dumps(attempts,indent=2)+'\n');raise SystemExit('Embedding request failed HTTP '+str(err.code)+'; response suppressed; no retry')
  except Exception as err:
   rec['error_class']=type(err).__name__
   rec['status']='failed';attempt_path.write_text(json.dumps(attempts,indent=2)+'\n');raise SystemExit('Embedding request failed; details suppressed; no retry')
  cache[h]={'text':w['text'],'vector':vector,'model':'gemini-embedding-2','dimensions':768};cache_path.write_text(json.dumps(cache,ensure_ascii=False,separators=(',',':'))+'\n');rec['status']='completed';attempt_path.write_text(json.dumps(attempts,indent=2)+'\n');print('completed',len(attempts),flush=True);time.sleep(0.8)

bm=g.build_semantic_bm25f_payload(D);entries={}
for k,kind,e,s in g.iter_semantic_entries(D):
 text=g.semantic_text_for_entry(e,s,kind=kind);v=old['entries'][k]['vector']if old['entries'][k]['text']==text else cache[hashlib.sha256(text.encode()).hexdigest()]['vector'];entries[k]={'kind':kind,'slot':s,'id':e['id'],'text':text,'vector':v,'bm25f_document':bm['documents'][k]}
index={'provider':g.SEMANTIC_PROVIDER,'dictionary_hash':g.dictionary_hash(D),'semantic_text_recipe':g.SEMANTIC_TEXT_RECIPE_VERSION,'embedding_model':g.SEMANTIC_MODEL_ID,'embedding_dimensions':768,'bm25f':{k:v for k,v in bm.items()if k!='documents'},'entries':entries}
g.validate_semantic_index_metadata(index,D)
if not args.replay:builder.write_sharded_payload(A/'photo_prompt_semantic_index.json',index,keep_stale_generations=True)
actual=g.load_semantic_index(A/'photo_prompt_semantic_index.json',D);assert actual['entries']==entries
assert len(entries)==10174 and sum(old['entries'][k]['vector']==e['vector']for k,e in entries.items())==10169
def cosine(a,b):return sum(x*y for x,y in zip(a,b))/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(x*x for x in b)))
for label,ix,data in [('baseline',old,B),('final',index,D)]:
 dense=[];lexical=[];bm=g.semantic_bm25f_payload_from_index(ix)
 for q in F['queries']:
  vector=cache[hashlib.sha256(q['query'].encode()).hexdigest()]['vector'];scores=[{'id':k,'score':round(cosine(vector,e['vector']),12)}for k,e in ix['entries'].items()if e['kind']=='slot'and e['slot']==q['slot']];scores.sort(key=lambda x:(-x['score'],x['id']));rk=next(i for i,x in enumerate(scores,1)if x['id']==q['target']);dense.append({**q,'rank':rk,'corpus_size':len(scores),'target_score':scores[rk-1]['score'],'top5':scores[:5]})
  ids=['slot:'+q['slot']+':'+e['id']for e in data['slots'][q['slot']]];rs=rank_bm25f(bm,{'query':q['query']},allowed_ids=ids,limit=len(ids));lexical.append({**q,'rank':next((i for i,x in enumerate(rs,1)if x['document_id']==q['target']),None),'corpus_size':len(ids),'top5':rs[:5]})
 for method,rs in [('dense',dense),('lexical',lexical)]:
  path=E/(method+'-'+label+'.json')
  if args.replay:assert json.loads(path.read_text())==rs,(method,label)
  else:path.write_text(json.dumps(rs,ensure_ascii=False,indent=2)+'\n')
plan.update(status='completed',initial_pending_texts=plan['pending_texts'],pending_texts=0,calls_attempted=len(attempts),calls_completed=sum(a['status']=='completed'for a in attempts),actual_attempt_conservative_upper_usd=len(attempts)*8192*0.2/1000000,cumulative_tracked_upper_usd=1.0190848+len(attempts)*8192*0.2/1000000,final_dictionary_hash=g.dictionary_hash(D),index_documents=10174,reused_document_vectors=10169,new_document_vectors=5,attempted_input_utf8_bytes=sum(len(cache[a['sha256']]['text'].encode())for a in attempts if a['sha256']in cache))
if not args.replay:(E/'api-workload.json').write_text(json.dumps(plan,indent=2)+'\n')
print('Validated current index and all 28 paired-query results'+(' reproduced'if args.replay else' saved'),flush=True)
