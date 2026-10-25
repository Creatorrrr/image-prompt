"""Identical whole-pool development queries on selected baseline and successor."""
from pathlib import Path
import gc,json,sys,hashlib,time
gc.disable()
O=Path(__file__).resolve().parent;ROOT=O.parents[4];S=ROOT/'skills/photo-prompt-image-generator'
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 base=read(O/'release-base.json');stage=read(O/'successor.json');N=Path(stage['store'])/'generations'/stage['native_generation_id'];sys.path.insert(0,str(N/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 import photo_recall_first as rf
 queries=read(O/'qualification-queries.frozen.json');qsha=hashlib.sha256((O/'qualification-queries.frozen.json').read_bytes()).hexdigest();mapping=read(O/'card-candidate-map.json');new=read(O/'new-native-records.json');diag={cid for cid,r in new.items() if r['record_kind']=='diagnostic'};positive=set(new)-diag
 binding=read(Path(stage['store'])/'h-f2-generations'/stage['generation_id']/'manifest.json')['binding'];cache=O/'qualification-query-evidence.json'
 if cache.exists():
  encoded=read(cache);assert encoded['query_sha256']==qsha and encoded['binding']==binding
 else:
  encoded={'query_sha256':qsha,'binding':binding,'rows':[]}
  with LocalEncoder(S) as enc:
   assert enc.binding==binding
   for start in range(0,len(queries),12):
    batch=queries[start:start+12];es=enc.encode([q['text'] for q in batch],'query')
    for q,e in zip(batch,es,strict=True):rf.check_embedding(e,binding,q['text'],'query');encoded['rows'].append({'id':q['id'],'embedding':e})
  write(cache,encoded)
 rows=[];pop={}
 for label,store,gid in [('baseline',base['store'],base['config']['generation_id']),('stage',stage['store'],stage['generation_id'])]:
  generation=Generation(store,gid,full=True);assert generation.binding==binding;index=generation.index()
  for q,e in zip(queries,encoded['rows'],strict=True):
   assert q['id']==e['id'];out=index.search(q['text'],e['embedding'],binding);assert out['lane_calls']=={'BM25F':1,'local_cosine':1};order=out['order'];assert not any(r['cid'] in diag for r in order)
   targets={mapping[c] for c in q['target_research_cards']};rank=next((i+1 for i,r in enumerate(order) if r['cid'] in targets),None)
   rows.append({**q,'build':label,'target_ids':sorted(targets),'target_rank':rank,'top10':order[:10],'new_at10':[r['cid'] for r in order[:10] if r['cid'] in positive],'population':out['considered_CIDs'],'generation_id':gid,'route':'whole_pool_rank_probe_not_managed_sample','semantic_adoption':'not_tested'})
   pop[label]=out['considered_CIDs']
   print(label,q['id'],'target_rank',rank,flush=True)
  del index,generation;gc.collect()
 summary={'status':'complete','queries_per_build':len(queries),'whole_pool_searches':len(rows),'development_topic_requests':20,'ordinary_controls':6,'holdout_cases':0,'population':pop,'diagnostic_new_records_excluded':len(diag),'new_positive_records':len(positive),'native_approval':False,'counts':{}}
 for label in ['baseline','stage']:
  topical=[r for r in rows if r['build']==label and r['kind']!='ordinary_control'];ordinary=[r for r in rows if r['build']==label and r['kind']=='ordinary_control']
  summary['counts'][label]={'target_at8':sum(r['target_rank'] is not None and r['target_rank']<=8 for r in topical),'target_at32':sum(r['target_rank'] is not None and r['target_rank']<=32 for r in topical),'ordinary_with_new_at10':sum(bool(r['new_at10']) for r in ordinary)}
 summary['limits']='Authored exposed development requests; target rank is not complete semantic recall, actual managed material sampling, native source qualification, source adoption, saved pixels, causal quality gain or requester acceptance.'
 write(O/'retrieval-qualification.json',{'summary':summary,'cases':rows});print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
if __name__=='__main__':main()
