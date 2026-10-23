"""Execute frozen development/control queries; exposure is not adoption."""
import gc
gc.disable()
import hashlib,json,sys,collections
from pathlib import Path
ROOT=Path('/Users/chasoik/Projects/image-prompt');Q=ROOT/'docs/research-evidence/photo-prompt/school-life-20261023';O=Path(__file__).resolve().parent;S=ROOT/'skills/photo-prompt-image-generator'
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 release=read(O/'successor.json');install={'generation_id':release['generation_id'],'store':release['store']};assert release['status']=='staged_verified'
 sys.path.insert(0,str(Path(install['store'])/'generations'/release['native_generation_id']/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 import photo_recall_first as rf
 full_cases=read(O/'retrieval-development-cases.json')['cases'];assert len(full_cases)==202
 selected=set(read(O/'retrieval-execution-scope.json')['selected_ids']);cases=[x for x in full_cases if x['id'] in selected];assert len(cases)==24
 registry=read(O/'data-integration.json');lookup={c['card_id']:c['candidate_id'] for c in registry['cards']};fresh=read(O/'new-native-records.json');visual={cid for cid,r in fresh.items() if r['record_kind']=='visual_option'};diagnostic=set(fresh)-visual
 manifest=read(Path(install['store'])/'h-f2-generations'/release['generation_id']/'manifest.json');binding=manifest['binding']
 cache=O/'qualification-query-evidence.json'
 if cache.exists():encoded=read(cache)
 else:
  encoded={'query_source_sha256':hashlib.sha256((O/'retrieval-development-cases.json').read_bytes()).hexdigest(),'binding':binding,'rows':[]}
  with LocalEncoder(S) as encoder:
   assert encoder.binding==binding
   for offset in range(0,len(cases),12):
    batch=cases[offset:offset+12];ev=encoder.encode([c['query'] for c in batch],'query')
    for c,e in zip(batch,ev,strict=True):rf.check_embedding(e,binding,c['query'],'query');encoded['rows'].append({'id':c['id'],'query':c['query'],'embedding':e})
    print('encoded',len(encoded['rows']),flush=True)
  write(cache,encoded)
 assert encoded['binding']==binding
 assert encoded['query_source_sha256']==hashlib.sha256((O/'retrieval-development-cases.json').read_bytes()).hexdigest()
 assert [(x['id'],x['query']) for x in full_cases]==[(x['id'],x['query']) for x in encoded['rows']]
 encoded['rows']=[x for x in encoded['rows'] if x['id'] in selected]
 generation=Generation(install['store'],release['generation_id'],full=True);index=generation.index();results=[]
 for case,ev in zip(cases,encoded['rows'],strict=True):
  out=index.search(case['query'],ev['embedding'],binding);assert out['lane_calls']=={'BM25F':1,'local_cosine':1}
  expected={lookup[cid] for cid in case.get('expected_cards',[])};order=out['order'];assert not any(r['cid'] in diagnostic for r in order), 'Diagnostic leaked into positive population'
  results.append({**case,'generation_id':generation.id,'population':out['considered_CIDs'],'target_rank':next((i+1 for i,r in enumerate(order) if r['cid'] in expected),None),'top10':order[:10],'new_at10':[r['cid'] for r in order[:10] if r['cid'] in visual],'route':'whole_pool_probe_not_managed_sampling','semantic_adoption':'not_tested'})
  write(O/'retrieval-smoke-progress.json',{'completed':len(results),'cases':results});print('searched',len(results),flush=True)
 positives=[r for r in results if r['set']=='development']
 summary={'status':'complete','qualification_store':install['store'],'generation_id':release['generation_id'],'query_count':len(results),'original_plan_queries':202,'unexecuted_plan_queries':178,'sets':dict(collections.Counter(r['set'] for r in results)),'positive_queries':len(positives),'languages':dict(collections.Counter(r['language'] for r in results)),'positive_target_at10':sum(r['target_rank'] is not None and r['target_rank']<=10 for r in positives),'positive_target_at32':sum(r['target_rank'] is not None and r['target_rank']<=32 for r in positives),'positive_target_at96':sum(r['target_rank'] is not None and r['target_rank']<=96 for r in positives),'ordinary_controls_with_new_at10':sum(bool(r['new_at10']) for r in results if r['set']=='general_control'),'kernel_change':'no executable kernel changes; current verified sealed implementation retained','baseline_search_executed':False,'diagnostic_positive_leaks':0,'native_approval':False,'limit':'Authored development probes, not independent holdout. Exposure is not source compatibility, selection, pixel pass or causal improvement. Diagnostic records are absent from the positive corpus by design.'}
 write(O/'retrieval-qualification.json',{'summary':summary,'cases':results});print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
