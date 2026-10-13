"""Actual source-based re-review of failed citations or ambiguous judgments."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import argparse,gzip,json,sys,time,hashlib,threading
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from review_corpus import MODEL,SKILL,ROOT,blinded,refs,dump,load_env,genai,types,ensure_prompt_cache
from normalize_reviews import normalize
from validate_reviews import validate

def main():
 p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=12);p.add_argument('--pilot-only',action='store_true');a=p.parse_args();load_env(ROOT/'.env')
 source=json.loads(gzip.decompress((HERE/'REVIEW-SOURCE.json.gz').read_bytes()));client=genai.Client(http_options=types.HttpOptions(retry_options=types.HttpRetryOptions(attempts=1)));stop=threading.Event()
 cache,_,_=ensure_prompt_cache(client,source)
 pilot=set(json.loads((HERE/'REVIEW-ORDER.json').read_text())['ids'][:610]);todo=[];out=HERE/'adjudicated-reviews';out.mkdir(exist_ok=True)
 for file in sorted((HERE/'normalized-reviews').glob('*.json')):
  for envelope in json.loads(file.read_text())['rows']:
   r=envelope['review'];cid=r['id']
   unclear=any(u.get('kind')=='visual_semantic_ambiguity' for u in r['uncertainties'])
   if not envelope['mechanical_errors'] and not unclear:continue
   if a.pilot_only and cid not in pilot:continue
   if (out/(cid+'.json')).exists():continue
   todo.append(envelope)
 def one(previous):
  raw=previous['review'];cid=raw['id'];record=source['candidates'][cid]
  if stop.is_set():return {'id':cid,'resolved':False,'provider_call':False,'reason':'spending cap; queued request cancelled'}
  referenced=set(refs(record['content']))-{cid}
  request=json.dumps({'task':'Re-read the COMPLETE original source. The prior review failed these checks; replace it with a complete accurate review, not just a patch. Use exact source quotes, catalog dimensions and role type; no routing tag as a visual fact. Preserve true conditions and alternatives. For relational_action, an explicitly declared actor-object interaction is sufficient, a second human is not required. Metadata recommendations go in recommended_kind or facts, not text corrections. Exact alias phrases under activation/exact_terms are positive aliases; other activation policies are not visual facts. If a quote cannot be sourced, do not approve it. Resolve semantic ambiguity by faithfully preserving the original supported meaning; external facts not verified must remain stated as unverified.','failed_checks':previous['mechanical_errors'],'previous_review':raw,'primary_records':[blinded(record)],'referenced_records':[blinded(source['candidates'][x]) for x in sorted(referenced)]},ensure_ascii=False,separators=(',',':'))
  errors=[]
  for attempt in range(5):
   try:
    if stop.is_set():return {'id':cid,'resolved':False,'provider_call':False,'reason':'spending cap; queued request cancelled'}
    dump(out/(cid+f'.attempt-{attempt+1}.json'),{'schema':'photo-text-provider-attempt/v1','candidate_id':cid,'model':MODEL,'request_sha256':hashlib.sha256(request.encode()).hexdigest(),'started_at_epoch':time.time(),'status':'started_response_unknown'})
    start=time.time();resp=client.models.generate_content(model=MODEL,contents=request,config=types.GenerateContentConfig(cached_content=cache,response_mime_type='application/json',temperature=.1,max_output_tokens=32768,thinking_config=types.ThinkingConfig(thinking_level='HIGH')))
    answer=json.loads(resp.text)
    if isinstance(answer,dict) and 'reviews' in answer:answer=answer['reviews']
    if isinstance(answer,list):assert len(answer)==1;answer=answer[0]
    fixed,repairs,meta=normalize(answer,record,source['slot_catalog']);issues=validate(fixed,record,source['slot_catalog'])
    if any(u.get('kind')=='visual_semantic_ambiguity' for u in fixed['uncertainties']):issues.append('unresolved visual_semantic_ambiguity')
    value={'schema':'photo-source-review-adjudication/v1','candidate_id':cid,'review':fixed,'representation_repairs':repairs,'metadata_suggestions':meta,'mechanical_errors':issues,'actual_provider_call':True,'model':MODEL,'request_sha256':hashlib.sha256(request.encode()).hexdigest(),'usage':resp.usage_metadata.model_dump(mode='json') if resp.usage_metadata else None,'elapsed_seconds':time.time()-start,'attempt_errors':errors,'original_response_file':previous['original_response_file'],'previous_review_sha256':hashlib.sha256(json.dumps(raw,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'independent_human_review':False}
    if issues:
     dump(out/(cid+f'.failed-{attempt+1}.json'),value);raise ValueError(str(issues))
    dump(out/(cid+'.json'),value);return {'id':cid,'seconds':round(time.time()-start,2),'resolved':True}
   except Exception as e:
    errors.append({'attempt':attempt+1,'type':type(e).__name__,'detail':str(e)[:1600]})
    dump(out/(cid+'.errors.json'),{'candidate_id':cid,'errors':errors})
    if 'monthly spending cap' in str(e).lower():
     stop.set();return {'id':cid,'resolved':False,'reason':'project monthly spending cap; new requests stopped','errors':errors}
    if attempt==4:return {'id':cid,'resolved':False,'errors':errors}
    time.sleep(min(12,2**attempt))
 print(json.dumps({'queued_records':len(todo),'pilot_only':a.pilot_only}),flush=True)
 with ThreadPoolExecutor(max_workers=a.workers) as pool:
  for f in as_completed([pool.submit(one,x) for x in todo]):print(json.dumps(f.result()),flush=True)
if __name__=='__main__':main()
