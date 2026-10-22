"""Bilingual after-release whole-pool probes; no source or pixel approval.

New exact CIDs were absent from the baseline by construction. Their before
rank is not a meaningful semantic baseline, so no before/after gain is claimed.
"""
import gc
gc.disable()
from pathlib import Path
import collections,csv,hashlib,json,sys
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt')
read=lambda p:json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def main():
 B=read(O/'before.json');S=read(O/'successor.json');I=read(O/'install.log');assert I['status']=='pass' and I['generation_id']==S['generation_id'];target_store=I['store'];sys.path.insert(0,str(Path(I['store'])/'generations'/S['native_generation_id']/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 from photo_runtime_sources import RuntimeSnapshotProvider
 import photo_canonical_source as canonical,photo_recall_first as rf
 qfile=O.parents[1]/'evaluation-cases.json'
 registry=read(O/'data-integration.json');lookup={x['id']:x.get('candidate_id') for x in registry['cards']};fresh=read(O/'new-native-records.json');new_visual={cid for cid,r in fresh.items() if r['record_kind']=='visual_option'}
 cases=[]
 for row in read(qfile)['cases']:
  for lang in ('ko','en'):
   cases.append({'id':row['id']+'-'+lang,'cohort':row['group'],'language':lang,'query':row['query_'+lang],'expected_cards':row['expected_card_ids'],'expected_judgment':row['review_ko']})
 assert len(cases)==160
 before_manifest=read(Path(B['store'])/'h-f2-generations'/B['config']['generation_id']/'manifest.json')
 after_manifest=read(Path(target_store)/'h-f2-generations'/S['generation_id']/'manifest.json')
 path=O/'qualification-query-evidence.json'
 if path.exists():encoded=read(path)
 else:
  encoded={'binding':after_manifest['binding'],'query_source_sha256':hashlib.sha256(qfile.read_bytes()).hexdigest(),'rows':[]}
  with LocalEncoder(R/'skills/photo-prompt-image-generator') as enc:
   assert enc.binding==before_manifest['binding']==after_manifest['binding']
   for start in range(0,len(cases),12):
    batch=cases[start:start+12];rows=enc.encode([x['query'] for x in batch],'query')
    for row,e in zip(batch,rows,strict=True):rf.check_embedding(e,enc.binding,row['query'],'query');encoded['rows'].append({'id':row['id'],'query':row['query'],'embedding':e})
    print('encoded',len(encoded['rows']),flush=True)
  write(path,encoded)
 assert [(x['id'],x['query']) for x in encoded['rows']]==[(x['id'],x['query']) for x in cases]
 after=Generation(target_store,S['generation_id'],full=True)
 source=RuntimeSnapshotProvider(store=target_store).load_generation(S['native_generation_id'])
 assert all(canonical.native_snapshot(source.data['candidates'][cid])==v for cid,v in fresh.items())
 indexes=[after.index()];results=[]
 for row,ev in zip(cases,encoded['rows'],strict=True):
  expected={lookup[x] for x in row['expected_cards'] if lookup.get(x)};out={**row,'registered_expected_CIDs':sorted(expected),'held_or_unregistered_cards':[x for x in row['expected_cards'] if not lookup.get(x)],'route':'whole_pool_probe_not_managed_sampling_or_slot_approval'}
  for name,g,index in zip(('after',),(after,),indexes,strict=True):
   result=index.search(row['query'],ev['embedding'],encoded['binding']);assert result['lane_calls']=={'BM25F':1,'local_cosine':1};order=result['order']
   out[name]={'generation_id':g.id,'population':result['considered_CIDs'],'top10':order[:10],'target_rank':next((i+1 for i,x in enumerate(order) if x['cid'] in expected),None),'new_at10':[x['cid'] for x in order[:10] if x['cid'] in new_visual]}
  results.append(out)
  if len(results)%12==0:print('searched',len(results),flush=True)
 positive=[r for r in results if r['cohort']=='positive'];controls=[r for r in results if r['cohort']!='positive']
 summary={'status':'bilingual_whole_pool_probes_complete','queries':len(results),'after_executions':len(results),'development_queries':len(positive),'control_queries':len(controls),'registered_positive_queries':sum(bool(r['registered_expected_CIDs']) for r in positive),'held_positive_queries':sum(not r['registered_expected_CIDs'] for r in positive),'after_target_at10':sum(r['after']['target_rank'] is not None and r['after']['target_rank']<=10 for r in positive),'after_target_at32':sum(r['after']['target_rank'] is not None and r['after']['target_rank']<=32 for r in positive),'controls_with_new_at10':sum(bool(r['after']['new_at10']) for r in controls),'baseline_manifest_positive_CIDs':before_manifest['CID_count'],'after_positive_CIDs':after.manifest['CID_count'],'new_native_snapshots_exact':True,'candidate_policy_and_embedding_space_preserved':True,'latest_query_scope_overlay':True,'baseline_search_executed':False,'limits':'Source-derived development probes; baseline CID absence cannot measure gain. No independent holdout, auto eligibility, native semantic qualification, managed sampling, causal image improvement or user acceptance. Controls require source-specific semantic review; exposure is not automatically an error.'}
 write(O/'retrieval-qualification.json',{'summary':summary,'cases':results});print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
