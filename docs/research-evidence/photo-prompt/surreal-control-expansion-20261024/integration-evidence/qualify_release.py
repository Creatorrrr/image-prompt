from pathlib import Path
import hashlib,json,sys
O=Path(__file__).parent.resolve();R=Path('/Users/chasoik/Projects/image-prompt');rd=lambda p:json.loads(p.read_bytes())
def wr(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 B=rd(O/'before.json');S=rd(O/'successor.json');sys.path.insert(0,str(Path(B['native'])/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 from photo_runtime_sources import RuntimeSnapshotProvider
 import photo_canonical_source as canonical,photo_recall_first as rf
 plan=O.parent/'retrieval-evaluation-plan.json';case_source=rd(plan)['cases'];cases=[]
 registry=rd(O/'data-integration.json');lookup={r['research_id']:r['candidate_id'] for r in registry['cards'] if 'research_id' in r};new=rd(O/'new-native-records.json');expected={cid for cid,r in new.items() if r['record_kind']!='diagnostic'};diag=set(new)-expected
 for case in case_source:
  for lang in ['ko','en']:cases.append({'id':case['case_id']+'-'+lang,'kind':case['kind'],'language':lang,'query':case[lang],'expected_cid':lookup.get(case['research_target'])})
 before=Generation(B['store'],B['config']['generation_id'],full=True);after=Generation(S['store'],S['generation_id'],full=True);source=RuntimeSnapshotProvider(store=S['store']).load_generation(S['native_generation_id'])
 assert all(canonical.native_snapshot(source.data['candidates'][cid])==v for cid,v in new.items());assert after.manifest['CID_count']==before.manifest['CID_count']+19
 before_source=RuntimeSnapshotProvider(store=B['store']).load_generation(B['config']['native_generation_id']);assert all(source.data['candidates'][cid]==r for cid,r in before_source.data['candidates'].items())
 assert len(source.data['candidates'])==len(before_source.data['candidates'])+35
 indexes=[before.index(),after.index()];assert expected.issubset({r['cid'] for r in after.metadata});assert not diag.intersection({r['cid'] for r in after.metadata})
 path=O/'qualification-query-evidence.json'
 if path.exists():encoded=rd(path)
 else:
  encoded={'binding':after.binding,'query_source_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'rows':[]}
  with LocalEncoder(R/'skills/photo-prompt-image-generator') as enc:
   assert enc.binding==before.binding==after.binding
   for start in range(0,len(cases),10):
    batch=cases[start:start+10];es=enc.encode([r['query'] for r in batch],'query')
    for row,e in zip(batch,es,strict=True):rf.check_embedding(e,enc.binding,row['query'],'query');encoded['rows'].append({'id':row['id'],'query':row['query'],'embedding':e})
    print('encoded',len(encoded['rows']),flush=True)
  wr(path,encoded)
 assert [(r['id'],r['query']) for r in cases]==[(r['id'],r['query']) for r in encoded['rows']]
 results=[]
 for row,ev in zip(cases,encoded['rows'],strict=True):
  out={**row,'route':'whole_pool_development_probe_not_managed_sample'}
  for label,g,index in zip(['before','after'],[before,after],indexes,strict=True):
   result=index.search(row['query'],ev['embedding'],encoded['binding']);assert result['lane_calls']=={'BM25F':1,'local_cosine':1};order=result['order'];assert not diag.intersection(r['cid'] for r in order)
   out[label]={'generation_id':g.id,'population':result['considered_CIDs'],'top8':order[:8],'target_rank':next((i+1 for i,r in enumerate(order) if r['cid']==row['expected_cid']),None),'new_at8':[r['cid'] for r in order[:8] if r['cid'] in expected]}
  results.append(out)
  if len(results)%10==0:print('searched',len(results),flush=True)
 pos=[r for r in results if r['expected_cid']];ctrl=[r for r in results if not r['expected_cid']]
 summary={'status':'pass_integrity_and_measured_probes','queries':len(results),'before_after_executions':2*len(results),'positive_queries':len(pos),'control_queries':len(ctrl),'before_target_at8':sum(r['before']['target_rank'] is not None and r['before']['target_rank']<=8 for r in pos),'after_target_at8':sum(r['after']['target_rank'] is not None and r['after']['target_rank']<=8 for r in pos),'after_target_at32':sum(r['after']['target_rank'] is not None and r['after']['target_rank']<=32 for r in pos),'controls_new_at8':sum(bool(r['after']['new_at8']) for r in ctrl),'new_positive_indexed':19,'new_diagnostics_excluded':16,'old_installed_records_exactly_preserved':len(before_source.data['candidates']),'before_positive':before.manifest['CID_count'],'after_positive':after.manifest['CID_count'],'independent_holdout':False,'limits':'Source-derived development probes; rank is not sampled exposure, semantic precision, final adoption, native approval, causal image improvement or pixel success. Ordinary-query optional material exposure requires author review, not automatic suppression.'}
 wr(O/'retrieval-qualification.json',{'summary':summary,'cases':results});print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
