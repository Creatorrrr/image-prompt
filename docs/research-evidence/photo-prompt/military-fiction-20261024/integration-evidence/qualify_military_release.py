"""Whole-pool development probes; no request authoring and no image calls."""
from pathlib import Path
import collections,gc,json,hashlib,sys,time
gc.disable()
O=Path(__file__).resolve().parent;R=O.parent;ROOT=R.parents[3];S=ROOT/'skills/photo-prompt-image-generator'
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 base=read(O/'release-base.json')
 release=read(O/'successor.json') if (O/'successor.json').exists() else {'status':'encoding_only','store':base['store'],'generation_id':base['config']['generation_id'],'native_generation_id':base['config']['native_generation_id']}
 assert release['status']=='staged_verified' or '--encode-only' in sys.argv
 n=Path(release['store'])/'generations'/release['native_generation_id'];sys.path.insert(0,str(n/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 import photo_recall_first as rf
 queries=read(R/'evaluation-queries.json');mapping=read(O/'card-candidate-map.json')
 ordinary=[('ordinary-potted-plant','A small potted plant on a quiet apartment windowsill.'),('ordinary-portrait','A close portrait beside a plain wall with soft window light.'),('ordinary-tea','A ceramic cup of tea on a wooden kitchen table.'),('ordinary-library','Two friends reading a book at a public library table.'),('ordinary-bicycle','A bicycle leaning against a brick wall after rain.'),('ordinary-cat','A sleeping cat curled on a woven blanket.')]
 queries+= [{'id':i,'language':'en','text':t,'kind':'ordinary_control','target_research_cards':[],'holdout':False} for i,t in ordinary]
 write(O/'qualification-queries.frozen.json',queries);qsha=hashlib.sha256((O/'qualification-queries.frozen.json').read_bytes()).hexdigest()
 binding=read(Path(release['store'])/'h-f2-generations'/release['generation_id']/'manifest.json')['binding'];cache=O/'qualification-query-evidence.json'
 if cache.exists():encoded=read(cache);assert encoded['query_sha256']==qsha and encoded['binding']==binding
 else:
  encoded={'query_sha256':qsha,'binding':binding,'rows':[]}
  with LocalEncoder(S) as encoder:
   assert encoder.binding==binding
   for start in range(0,len(queries),12):
    batch=queries[start:start+12];out=encoder.encode([q['text'] for q in batch],'query')
    for q,e in zip(batch,out,strict=True):rf.check_embedding(e,binding,q['text'],'query');encoded['rows'].append({'id':q['id'],'embedding':e})
    print('query embeddings',len(encoded['rows']),flush=True)
  write(cache,encoded)
 if '--encode-only' in sys.argv:
  print(json.dumps({'status':'query_embeddings_saved','count':len(encoded['rows']),'model_space':binding['model'] if 'model' in binding else binding}),flush=True);return
 generation=Generation(release['store'],release['generation_id'],full=True);index=generation.index();new=read(O/'new-native-records.json');positive={cid for cid,r in new.items() if r['record_kind']=='visual_option'};diagnostic=set(new)-positive;rows=[]
 for q,e in zip(queries,encoded['rows'],strict=True):
  assert q['id']==e['id'];out=index.search(q['text'],e['embedding'],binding)
  assert out['lane_calls']=={'BM25F':1,'local_cosine':1}
  order=out['order'];assert not any(r['cid'] in diagnostic for r in order)
  expected={mapping[c] for c in q['target_research_cards']};rank=next((i+1 for i,r in enumerate(order) if r['cid'] in expected),None)
  rows.append({**q,'target_candidate_ids':sorted(expected),'target_rank':rank,'top10':order[:10],'new_at10':[r['cid'] for r in order[:10] if r['cid'] in positive],'population':out['considered_CIDs'],'generation_id':generation.id,'route':'whole_pool_probe_not_managed_sampling','semantic_adoption':'not_tested'})
  if len(rows)%24==0:print('whole-pool probes',len(rows),flush=True)
 positive_rows=[r for r in rows if r['kind']!='ordinary_control'];natural=[r for r in rows if r['kind']=='authored_development_query']
 summary={'status':'complete','generation_id':generation.id,'query_count':len(rows),'literal_card_queries':208,'natural_development_queries':48,'ordinary_controls':len(ordinary),'target_at8':sum(r['target_rank'] is not None and r['target_rank']<=8 for r in positive_rows),'target_at32':sum(r['target_rank'] is not None and r['target_rank']<=32 for r in positive_rows),'natural_target_at8':sum(r['target_rank'] is not None and r['target_rank']<=8 for r in natural),'natural_target_at32':sum(r['target_rank'] is not None and r['target_rank']<=32 for r in natural),'ordinary_controls_with_new_at10':sum(bool(r['new_at10']) for r in rows if r['kind']=='ordinary_control'),'diagnostic_records_excluded_from_positive_pool':len(diagnostic),'baseline_search_executed':False,'native_approval':False,'holdout_cases':0,'limits':'Authored development probes and structural coverage only. Exposure is not source fit, actual selection, image realization, causal gain or user acceptance.'}
 write(O/'retrieval-qualification.json',{'summary':summary,'cases':rows});print(json.dumps(summary,indent=2),flush=True)
if __name__=='__main__':main()
