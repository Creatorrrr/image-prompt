"""Source-derived bilingual development and boundary probes, never pixel approval."""
import gc
gc.disable()
from pathlib import Path
import collections,csv,hashlib,json,sys,time
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt')
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 B=read(O/'before.json');S=read(O/'successor.json');I=read(O/'install.json')
 assert I['status']=='pass' and I['generation_id']==S['generation_id']
 store=Path(I['store']);sys.path.insert(0,str(store/'generations'/S['native_generation_id']/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 from photo_runtime_sources import RuntimeSnapshotProvider
 import photo_canonical_source as canonical,photo_recall_first as rf
 qfile=O.parents[1]/'evaluation-cases.json';bfile=O.parents[1]/'CONFUSION-CASES.tsv';registry=read(O.parent/'data-integration.json');fresh=read(O/'new-native-records.json')
 lookup=collections.defaultdict(set)
 for v in registry['cards']:
  if v['positive']:lookup[v['card_id']].add(v['candidate_id'])
 source=read(qfile)['cases']
 cases=[{'id':x['id']+'-'+lang,'cohort':('authored_development' if x['type']=='development' else 'context_boundary'),'language':lang,'query':x['query_'+lang],'expected_cards':x['expected_card_ids'],'expected_judgment':x['must_not_conflate']} for x in source for lang in ('ko','en')]
 with bfile.open() as f:boundaries=list(csv.DictReader(f,delimiter='\t'))
 cases.extend({'id':x['pair_id']+'-'+side+'-'+lang,'cohort':'boundary_or_ordinary_control','language':lang,'query':x['query_'+side+'_'+lang],'expected_cards':[],'expected_judgment':x['expected_boundary']} for x in boundaries for side in ('a','b') for lang in ('ko','en'))
 assert len(cases)==272
 oldmanifest=read(Path(B['store'])/'h-f2-generations'/B['config']['generation_id']/'manifest.json')
 newmanifest=read(store/'h-f2-generations'/S['generation_id']/'manifest.json')
 ep=O/'qualification-query-evidence.json'
 if ep.exists():encoded=read(ep)
 else:
  encoded={'binding':newmanifest['binding'],'query_source_sha256':hashlib.sha256(qfile.read_bytes()+bfile.read_bytes()).hexdigest(),'rows':[]}
  with LocalEncoder(R/'skills/photo-prompt-image-generator') as enc:
   assert enc.binding==newmanifest['binding']==oldmanifest['binding']
   for start in range(0,len(cases),12):
    batch=cases[start:start+12];embeddings=enc.encode([x['query'] for x in batch],'query')
    for row,e in zip(batch,embeddings,strict=True):
     rf.check_embedding(e,enc.binding,row['query'],'query');encoded['rows'].append({'id':row['id'],'query':row['query'],'embedding':e})
    print('encoded',len(encoded['rows']),flush=True)
  write(ep,encoded)
 assert encoded['binding']==oldmanifest['binding']==newmanifest['binding']
 assert [(x['id'],x['query']) for x in encoded['rows']]==[(x['id'],x['query']) for x in cases]
 after=Generation(store,S['generation_id'],full=True);ai=after.index()
 indexed={x['cid'] for x in after.metadata};held={cid for cid,v in fresh.items() if v['record_kind']=='diagnostic'}
 assert not indexed.intersection(held) and {cid for cid,v in fresh.items() if v['record_kind']=='visual_option'}<=indexed
 before=Generation(B['store'],B['config']['generation_id'],full=True);bi=before.index()
 snapshot=RuntimeSnapshotProvider(store=store).load_generation(S['native_generation_id'])
 assert all(canonical.native_snapshot(snapshot.data['candidates'][cid])==v for cid,v in fresh.items())
 newvisual={cid for cid,v in fresh.items() if v['record_kind']=='visual_option'};results=[]
 for row,ev in zip(cases,encoded['rows'],strict=True):
  targets=set().union(*(lookup[x] for x in row['expected_cards'])) if row['expected_cards'] else set()
  result=ai.search(row['query'],ev['embedding'],encoded['binding']);assert result['lane_calls']=={'BM25F':1,'local_cosine':1};order=result['order']
  out={**row,'registered_expected_CIDs':sorted(targets),'held_or_context_cards':[x for x in row['expected_cards'] if not lookup[x]],'route':'whole_pool_probe_not_managed_sampling_or_slot_approval','after':{'generation_id':after.id,'population':result['considered_CIDs'],'top10':order[:10],'target_rank':next((i+1 for i,x in enumerate(order) if x['cid'] in targets),None),'new_at10':[x['cid'] for x in order[:10] if x['cid'] in newvisual]}}
  if row['cohort']=='boundary_or_ordinary_control':
   old=bi.search(row['query'],ev['embedding'],encoded['binding']);assert old['lane_calls']=={'BM25F':1,'local_cosine':1}
   out['before']={'generation_id':before.id,'population':old['considered_CIDs'],'top10':old['order'][:10]}
   out['old_top10_overlap']=len({x['cid'] for x in old['order'][:10]}&{x['cid'] for x in order[:10]})
  results.append(out)
  if len(results)%12==0:print('searched',len(results),flush=True)
 development=[x for x in results if x['cohort']=='authored_development'];registered=[x for x in development if x['registered_expected_CIDs']];controls=[x for x in results if x['cohort']=='boundary_or_ordinary_control']
 summary={'status':'bilingual_whole_pool_probes_complete','queries':len(results),'after_executions':len(results),'before_control_executions':len(controls),'development_queries':len(development),'registered_development_queries':len(registered),'held_or_context_development_queries':len(development)-len(registered),'after_target_at10':sum(x['after']['target_rank'] is not None and x['after']['target_rank']<=10 for x in registered),'after_target_at32':sum(x['after']['target_rank'] is not None and x['after']['target_rank']<=32 for x in registered),'controls_with_new_at10':sum(bool(x['after']['new_at10']) for x in controls),'control_old_top10_mean_overlap':sum(x['old_top10_overlap'] for x in controls)/len(controls),'baseline_positive_CIDs':before.manifest['CID_count'],'after_positive_CIDs':after.manifest['CID_count'],'new_native_snapshots_exact':True,'source_query_sha256':hashlib.sha256(qfile.read_bytes()).hexdigest(),'boundary_query_sha256':hashlib.sha256(bfile.read_bytes()).hexdigest(),'registered_visual_cards':len(lookup)-sum(not v for v in lookup.values()),'candidate_policy_code_and_embedding_space_preserved':True,'limits':'Source-derived development probes, not an independent holdout. No before/after semantic gain is measured for absent new CIDs. Boundary queries can validly retrieve authored near neighbors; exposure alone is not adoption or an error. No native semantic qualification, causal image improvement or user acceptance.'}
 write(O/'retrieval-qualification.json',{'summary':summary,'cases':results});print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
