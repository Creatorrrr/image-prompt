"""Full-pool bilingual development/boundary probes; no pixel or native approval."""
from pathlib import Path
import gc
gc.disable()
import csv,hashlib,json,sys,time,collections
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt')
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 B=read(O/'before.json');S=read(O/'successor.json');I=read(O/'install.json');assert I['status']=='pass'
 store=Path(I['store']);sys.path.insert(0,str(store/'generations'/S['native_generation_id']/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 import photo_recall_first as rf,photo_canonical_source as canonical
 from photo_runtime_sources import RuntimeSnapshotProvider
 registry=read(O.parent/'data-integration.json');lookup={r['card_id']:r['candidate_id'] for r in registry['adoptions'] if r['decision'] in ('new','reuse')}
 qfile=O.parent.parent/'EVALUATION-CASES.tsv'
 with qfile.open() as f:source=list(csv.DictReader(f,delimiter='\t'))
 cases=[{'id':r['case_id']+'-'+lang,'cohort':r['split'],'language':lang,'query':r['query_'+lang],'expected_cards':r['relevant_research_card_ids'].replace('|',',').split(',') if r['relevant_research_card_ids'] else [],'limits':r['limit_or_expected_result']} for r in source for lang in ('ko','en')]
 for row in read(O/'new-phrasing-cases.json'):
  cases.extend({'id':row['id']+'-'+lang,'cohort':'new_scene_phrasing','language':lang,'query':row[lang],'expected_cards':[row['card']],'limits':'Coordinator-authored fresh phrasing frozen before search; author saw research. Not a blind independent holdout.'} for lang in ('ko','en'))
 write(O/'frozen-query-cases.json',cases)
 after=Generation(store,S['generation_id'],full=True);before=Generation(B['store'],B['config']['generation_id'],full=True)
 assert before.binding==after.binding
 ep=O/'query-embeddings.json'
 if ep.exists():encoded=read(ep)
 else:
  encoded={'binding':after.binding,'case_sha256':hashlib.sha256((O/'frozen-query-cases.json').read_bytes()).hexdigest(),'rows':[]}
  with LocalEncoder(R/'skills/photo-prompt-image-generator') as enc:
   assert enc.binding==after.binding
   for start in range(0,len(cases),12):
    batch=cases[start:start+12];es=enc.encode([r['query'] for r in batch],'query')
    for row,e in zip(batch,es,strict=True):rf.check_embedding(e,after.binding,row['query'],'query');encoded['rows'].append({'id':row['id'],'query':row['query'],'embedding':e})
    print('encoded',len(encoded['rows']),flush=True)
  write(ep,encoded)
 assert [(r['id'],r['query']) for r in cases]==[(r['id'],r['query']) for r in encoded['rows']]
 ai=after.index();bi=before.index();results=[]
 snapshot=RuntimeSnapshotProvider(store=store).load_generation(S['native_generation_id']);fresh=read(O/'new-native-records.json')
 assert all(canonical.native_snapshot(snapshot.data['candidates'][cid])==v for cid,v in fresh.items())
 newvisual={cid for cid,r in fresh.items() if r['record_kind']=='visual_option'};diagnostics=set(fresh)-newvisual
 assert diagnostics.isdisjoint({r['cid'] for r in after.metadata})
 for row,ev in zip(cases,encoded['rows'],strict=True):
  targets={lookup[k] for k in row['expected_cards'] if k in lookup};a=ai.search(row['query'],ev['embedding'],after.binding);assert a['lane_calls']=={'BM25F':1,'local_cosine':1}
  rank=next((i+1 for i,x in enumerate(a['order']) if x['cid'] in targets),None)
  out={**row,'registered_expected_CIDs':sorted(targets),'after':{'rank':rank,'top8':a['order'][:8],'population':a['considered_CIDs'],'query_scope':a['query_scope']},'new_at8':[r['cid'] for r in a['order'][:8] if r['cid'] in newvisual],'route':'full_pool_probe_before_managed_random_sampling; no slot or adoption approval'}
  if row['cohort'] not in ('development','new_scene_phrasing'):
   b=bi.search(row['query'],ev['embedding'],before.binding);out['before_top8']=b['order'][:8];out['old_top8_overlap']=len({r['cid'] for r in b['order'][:8]}&{r['cid'] for r in a['order'][:8]})
  results.append(out)
  if len(results)%16==0:print('searched',len(results),flush=True)
 groups={}
 for cohort in sorted({r['cohort'] for r in results}):
  rows=[r for r in results if r['cohort']==cohort];graded=[r for r in rows if r['registered_expected_CIDs']]
  groups[cohort]={'queries':len(rows),'registered_targets':len(graded),'target_at8':sum(r['after']['rank'] is not None and r['after']['rank']<=8 for r in graded),'target_at32':sum(r['after']['rank'] is not None and r['after']['rank']<=32 for r in graded),'new_sources_at8':sum(bool(r['new_at8']) for r in rows)}
 summary={'status':'source_and_retrieval_probes_complete','queries':len(results),'before_control_queries':sum('before_top8' in r for r in results),'groups':groups,'new_CIDs_exact':len(fresh),'diagnostics_excluded_from_positive_search':len(diagnostics),'before_positive_CIDs':before.manifest['CID_count'],'after_positive_CIDs':after.manifest['CID_count'],'native_approval':False,'pixel_status':'SEPARATE','limits':'Source-derived development and reviewed new phrasing, not blind holdout. Rank/exposure does not prove source compatibility, native adoption or causal image improvement.'}
 write(O/'retrieval-qualification.json',{'summary':summary,'cases':results});print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
