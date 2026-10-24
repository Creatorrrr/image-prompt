"""Real bilingual full-pool probes and complete sealed-source validation."""
from pathlib import Path
import gc; gc.disable()
import json,sys,hashlib,collections

O=Path(__file__).resolve().parent
R=O.parents[5]
S=R/'skills/photo-prompt-image-generator'
def read(p):
 import gzip
 raw=Path(p).read_bytes();return json.loads(gzip.decompress(raw) if str(p).endswith('.gz') else raw)
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def main():
 r=read(O/'successor.json');b=read(O/'release-base.json');N=Path(r['store'])/'generations'/r['native_generation_id'];sys.path.insert(0,str(N/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 import photo_recall_first as rf
 import photo_candidate_corpus as c
 import photo_canonical_source as canonical
 g=Generation(r['store'],r['generation_id'],full=True)
 records=read(O/'release-new-native-records.json');registration=read(O/'source-registration.json')
 corpus=c.load(N/'assets');positive=set(registration['new_visual_ids']);diagnostic=set(registration['diagnostic_ids']);meta=read(g.root/'indexed-documents.json.gz');indexed={v['cid'] for v in meta}
 assert len(positive)==87 and len(diagnostic)==247
 assert positive<=indexed and not diagnostic&indexed
 assert all(canonical.native_snapshot(corpus['candidates'][cid])==raw for cid,raw in records.items())
 assert all(cid in indexed for cid in registration['reused_existing_ids'].values())
 write(O/'registration-qualification.json',{'status':'pass','new_visual_CIDs':len(positive),'new_diagnostic_CIDs':len(diagnostic),'new_visual_CIDs_indexed':len(positive&indexed),'diagnostic_positive_leaks':len(diagnostic&indexed),'released_source_native_roundtrip_exact':len(records),'full_deployed_generation_validation':True,'reused_existing_ids_present':True,'native_approval':False})
 del corpus;gc.collect()
 seeds=read(O.parents[1]/'evaluation-cases.json');cases=[]
 for row in seeds:
  for lang in ('ko','en'):cases.append({'id':row['id']+'-'+lang,'query':row['query_'+lang],'set':'authored_development' if row['expected_card']!='NONE' else 'context_boundary','expected_card':row['expected_card'],'boundary':row['required_boundary']})
 for i,text in enumerate(['a white ceramic mug resting on a wooden table','an adult pianist pressing a grand piano key','a plain cotton shirt with visible seams']):cases.append({'id':'control-'+str(i+1),'query':text,'set':'general_control','expected_card':'NONE'})
 write(O/'retrieval-probes.json',cases)
 binding=g.binding;cache=O/'qualification-query-evidence.json';casehash=hashlib.sha256((O/'retrieval-probes.json').read_bytes()).hexdigest()
 if cache.exists():evidence=read(cache);assert evidence['case_sha256']==casehash and evidence['binding']==binding
 else:
  evidence={'case_sha256':casehash,'binding':binding,'rows':[]}
  with LocalEncoder(S) as encoder:
   assert encoder.binding==binding
   for off in range(0,len(cases),12):
    batch=cases[off:off+12]
    for case,e in zip(batch,encoder.encode([x['query'] for x in batch],'query'),strict=True):
     rf.check_embedding(e,binding,case['query'],'query');evidence['rows'].append({'id':case['id'],'query':case['query'],'embedding':e})
    print('query embeddings',len(evidence['rows']),flush=True)
  write(cache,evidence)
 assert [(x['id'],x['query']) for x in cases]==[(x['id'],x['query']) for x in evidence['rows']]
 index=g.index();results=[]
 for case,e in zip(cases,evidence['rows'],strict=True):
  out=index.search(case['query'],e['embedding'],binding);assert out['lane_calls']=={'BM25F':1,'local_cosine':1}
  assert not any(x['cid'] in diagnostic for x in out['order'])
  target=registration['card_candidate_map'].get(case['expected_card']);rank=next((i+1 for i,x in enumerate(out['order']) if x['cid']==target),None)
  results.append({**case,'target_candidate':target,'target_rank':rank,'top10':out['order'][:10], 'considered_CIDs':out['considered_CIDs'],'lane_calls':out['lane_calls']})
  write(O/'retrieval-progress.json',{'completed':len(results),'total':len(cases),'last':case['id']})
  print('searched',case['id'],'target rank',rank,flush=True)
 del index,g;gc.collect()
 baseline=Generation(b['store'],b['config']['generation_id'],full=True);baseline_index=baseline.index();controls=[]
 for case,e in zip(cases,evidence['rows'],strict=True):
  if case['set']!='general_control':continue
  before=baseline_index.search(case['query'],e['embedding'],binding);after=next(x for x in results if x['id']==case['id']);old=[x['cid'] for x in before['order'][:10]];new=[x['cid'] for x in after['top10']]
  controls.append({'id':case['id'],'before':old,'after':new,'top10_exact_order_preserved':old==new,'top10_overlap':len(set(old)&set(new)),'new_marine_in_top10':[x for x in new if x in positive]})
 pos=[x for x in results if x['expected_card']!='NONE' and x['target_candidate']]
 diagnostic_only=[x for x in results if x['expected_card'] in ('V074','T002')]
 summary={'status':'complete','queries':len(results),'bilingual_seed_queries':80,'general_controls':3,'positive_target_queries':len(pos),'target_at8':sum(x['target_rank'] is not None and x['target_rank']<=8 for x in pos),'target_at32':sum(x['target_rank'] is not None and x['target_rank']<=32 for x in pos),'diagnostic_positive_leaks':0,'context_or_sequence_only_queries_without_positive_target':len(diagnostic_only),'control_top10_unchanged':sum(x['top10_exact_order_preserved'] for x in controls),'native_approval':False,'limit':'Authored development probes, not independent holdout; retrieval exposure does not prove boundary reasoning, native adoption, image causality or pixel success.'}
 write(O/'retrieval-qualification.json',{'summary':summary,'cases':results,'baseline_controls':controls});print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
