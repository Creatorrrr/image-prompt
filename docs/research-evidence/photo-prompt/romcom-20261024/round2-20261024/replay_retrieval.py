"""Offline development comparison: exact old queries/vectors, unchanged kernel and sampling seeds."""
from pathlib import Path
import json,sys,hashlib
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt')
read=lambda p:json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 b=read(O/'BASELINE.json');s=read(O/'successor.json');sys.path.insert(0,str(Path(b['native'])/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_search import present_material
 import photo_h_f2_sampling as sampler
 import photo_recall_first as rf
 oldids=set(read(O.parent/'integration-evidence/new-source-cids.json')['visual_CIDs']);reviewed=read(O/'reviewed-native-records.json');newids=set(reviewed)-set(read(O/'release-changed-native-records.json'));tracked=oldids|newids
 cases=[]
 for arm,run in [('a','final-run-v2'),('b','narrowed'),('c','corrected-authoring-run')]:
  p=R/'generated/photo-runs'/f'romcom-20261024-{arm}'/run;f=next(p.glob('revisions/*/h_f2_material.json'));pack=read(f)
  for q,item in pack['query_set']['slots'].items():cases.append((arm,q,item,pack['queries'][q]['row'],pack['sampling_seed'],str(f)))
 report={'schema':'romcom-offline-development-replay/v1','base':b['config']['generation_id'],'successor':s['generation_id'],'kernel_unchanged':True,'query_embedding_calls':0,'topic_prefilter':False,'cases':[],'limits':'Author-exposed old natural queries, not a holdout. Equal fixed seeds compare presentation, not artistic adoption or pixels.'}
 for name,store,gid in [('base',b['store'],b['config']['generation_id']),('successor',s['store'],s['generation_id'])]:
  gen=Generation(store,gid,full=True);index=gen.index();cache={}
  for arm,q,item,vec,seed,source in cases:
   text=item['text'];key=hashlib.sha256(text.encode()).hexdigest()
   if key not in cache:cache[key]=index.search(text,vec,gen.binding)
   result=cache[key];order=result['order'];ranks={row['cid']:i+1 for i,row in reversed(list(enumerate(order)))}
   win,projection=present_material(order,result['query_scope']['event_phase'],literal=result['query_scope']['literal_text'],focus=result['query_scope']['primary_focus'],maximum=32)
   exposed,evidence=sampler.sample(win,1,seed,q,item['text_sha256'])
   row={'arm':arm,'query_id':q,'dataset':name,'query':text,'source_material':source,'query_vector_sha256':vec['execution']['vector_sha256'],'pool_CIDs':gen.manifest['CID_count'],'lane_calls':result['lane_calls'],'old_romcom_best_rank':min((ranks[c] for c in oldids if c in ranks),default=None),'new_guidance_ranks':{c:ranks.get(c) for c in sorted(newids)},'romcom_in_top32':[r['cid'] for r in win if r['cid'] in tracked],'romcom_sampled':[r['cid'] for r in exposed if r['cid'] in tracked],'top8_ranked_CIDs':[r['cid'] for r in order[:8]],'sampling_seed':seed,'native_approval':False}
   report['cases'].append(row)
  print(name,'complete',len(cases),'queries',len(cache),'unique',flush=True)
  del gen,index,cache
 write(O/'offline-retrieval-comparison.json',report)
 print(json.dumps({n:{'query_occurrences':sum(r['dataset']==n for r in report['cases']),'romcom_window_occurrences':sum(len(r['romcom_in_top32']) for r in report['cases'] if r['dataset']==n),'romcom_sampled_occurrences':sum(len(r['romcom_sampled']) for r in report['cases'] if r['dataset']==n)} for n in ['base','successor']}))
if __name__=='__main__':main()
