"""Read-only forensic analysis of the already issued retrieval orders; no search."""
from pathlib import Path
import gzip,json,hashlib,numpy as np
O=Path(__file__).resolve().parent; R=O.parents[4]
read=lambda p:json.loads(p.read_bytes())
s=read(O/'successor.json');g=Path(s['store'])/'h-f2-generations'/s['generation_id']
meta=json.loads(gzip.decompress((g/'indexed-documents.json.gz').read_bytes()));new={r['cid'] for r in read(O/'new-cid-membership.json')['records'] if r['record_kind']=='visual_option'}
results=[]
for arm,folder in [(1,'harem-20261023-independent-1'),(2,'harem-20261023-independent-2b'),(3,'harem-20261023-independent-3')]:
 p=R/'generated/photo-runs'/folder/'.staging/h-f2';m=read(p/'material.json');assert m['generation_id']==s['generation_id']
 for query,goal in m['goals'].items():
  fn=hashlib.sha256(query.encode()).hexdigest()+'.npz';assert hashlib.sha256((p/fn).read_bytes()).hexdigest()==m['raw_files'][fn]
  with np.load(p/fn,allow_pickle=False) as z:order=z['order'].tolist()
  ranked=[(i+1,meta[index]['cid']) for i,index in enumerate(order) if meta[index]['cid'] in new]
  window=goal['material_projection']['returned_ids'];window_new=[x for x in window if x.split('|')[0] in new];exposed=[x['cid'] for x in goal['candidates'] if x['cid'] in new]
  results.append({'arm':arm,'query_id':query,'raw_ranked_positive_CIDs':len(order),'new_visual_sources_in_raw_order':len(ranked),'best_new_source_raw_rank':ranked[0] if ranked else None,'rank_window':m['sampling_policy']['rank_window'],'new_sources_in_projected_window':window_new,'new_sources_in_issued_sample':exposed,'additional_search_calls':0})
(O/'issued-rank-analysis.json').write_text(json.dumps({'status':'read_only_issued_evidence','generation_id':s['generation_id'],'queries':results,'limit':'Explains exact returned evidence only; no reranking, resampling, new source inspection or causal quality claim.'},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(results,ensure_ascii=False,indent=2))
