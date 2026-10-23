"""Authored development probes: retrieval exposure only, never pixel qualification."""
from pathlib import Path
import argparse, collections, gc, hashlib, json, sys
gc.disable()
O=Path(__file__).resolve().parent
R=Path('/Users/chasoik/Projects/image-prompt')
E=R/'docs/research-evidence/photo-prompt/idol-fiction-20261023/integration-evidence'
read=lambda p:json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['freeze','encode','after','before','summary']);phase=p.parse_args().phase
 source=read(E.parent/'evaluation-cases.json')
 cases=[{'id':c['id'],'cohort':c['kind'],'language':c['language'],'query':c['request'],'expected_cards':c.get('relevant_card_ids',[]),'insufficient_static_proxy_card_ids':c.get('insufficient_static_proxy_card_ids',[])} for c in source['cases']]
 fingerprint=hashlib.sha256(json.dumps(cases,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 if phase=='freeze':
  assert not (O/'frozen-query-cases.json').exists()
  write(O/'frozen-query-cases.json',{'sha256':fingerprint,'independent_holdout':False,'cases':cases});print(fingerprint);return
 assert read(O/'frozen-query-cases.json')=={'sha256':fingerprint,'independent_holdout':False,'cases':cases}
 B=read(O/'before.json');S=read(O/'successor.json');I=read(O/'install.json')
 sys.path.insert(0,str(Path(I['store'])/'generations'/S['native_generation_id']/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 import photo_recall_first as rf
 lookup=read(E/'card-candidate-map.json')
 if phase=='encode':
  old=read(Path(B['store'])/'h-f2-generations'/B['config']['generation_id']/'manifest.json')
  new=read(Path(I['store'])/'h-f2-generations'/S['generation_id']/'manifest.json')
  assert old['binding']==new['binding']
  data={'binding':new['binding'],'case_sha256':fingerprint,'rows':[]}
  with LocalEncoder(R/'skills/photo-prompt-image-generator') as enc:
   assert enc.binding==data['binding']
   for start in range(0,len(cases),24):
    rows=cases[start:start+24]
    for c,v in zip(rows,enc.encode([x['query'] for x in rows],'query'),strict=True):
     rf.check_embedding(v,enc.binding,c['query'],'query')
     data['rows'].append({'id':c['id'],'query':c['query'],'embedding':v})
    print('encoded',len(data['rows']),flush=True)
  write(O/'query-embeddings.json',data);return
 encoded=read(O/'query-embeddings.json');assert encoded['case_sha256']==fingerprint
 assert [(c['id'],c['query']) for c in cases]==[(x['id'],x['query']) for x in encoded['rows']]
 if phase in ('after','before'):
  store=Path(I['store']) if phase=='after' else Path(B['store'])
  gid=S['generation_id'] if phase=='after' else B['config']['generation_id']
  generation=Generation(store,gid,full=True);index=generation.index()
  assert generation.binding==encoded['binding']
  new_records=read(O/'new-native-records.json')
  diagnostic_ids={cid for cid,c in new_records.items() if c['record_kind']=='diagnostic'}
  checkpoint=O/('probe-'+phase+'.json')
  result=read(checkpoint) if checkpoint.exists() else {'generation_id':gid,'case_sha256':fingerprint,'rows':[]}
  assert result['generation_id']==gid and result['case_sha256']==fingerprint
  done={c['id'] for c in result['rows']}
  for case,ev in zip(cases,encoded['rows'],strict=True):
   if case['id'] in done:continue
   if phase=='before' and case['cohort'] not in ('contrast_development','temporal_or_context_development'):continue
   found=index.search(case['query'],ev['embedding'],encoded['binding'])
   assert found['lane_calls']=={'BM25F':1,'local_cosine':1}
   assert not diagnostic_ids.intersection(x['cid'] for x in found['order'])
   targets={lookup[c] for c in case['expected_cards']}
   ranks={cid:next((i+1 for i,x in enumerate(found['order']) if x['cid']==cid),None) for cid in targets}
   result['rows'].append({**case,'registered_expected_CIDs':sorted(targets),'target_ranks':ranks,
    'target_rank':min((v for v in ranks.values() if v is not None),default=None),
    'top8':found['order'][:8],'population':found['considered_CIDs'],'lane_calls':found['lane_calls']})
   if len(result['rows'])%16==0:
    write(checkpoint,result);print('searched',phase,len(result['rows']),flush=True)
  result['complete']=True;write(checkpoint,result);return
 after=read(O/'probe-after.json');before=read(O/'probe-before.json')
 assert after['complete'] and before['complete'] and len(after['rows'])==len(cases)
 groups={}
 for cohort in sorted({c['cohort'] for c in cases}):
  rows=[c for c in after['rows'] if c['cohort']==cohort];eligible=[c for c in rows if c['registered_expected_CIDs']]
  groups[cohort]={'queries':len(rows),'graded_queries':len(eligible),
   'any_target_at8':sum(c['target_rank'] is not None and c['target_rank']<=8 for c in eligible),
   'any_target_at32':sum(c['target_rank'] is not None and c['target_rank']<=32 for c in eligible),
   'all_targets_at32':sum(all(v is not None and v<=32 for v in c['target_ranks'].values()) for c in eligible),
   'by_language':{lang:{'graded':sum(c['language']==lang for c in eligible),'any_at8':sum(c['language']==lang and c['target_rank'] is not None and c['target_rank']<=8 for c in eligible)} for lang in ('ko','en')}}
 summary={'status':'development_whole_pool_probes_complete','queries':len(cases),'before_control_queries':len(before['rows']),
  'groups':groups,'positive_CIDs':read(Path(I['store'])/'h-f2-generations'/S['generation_id']/'manifest.json')['CID_count'],
  'diagnostics_excluded':True,'all_cases_authored_development':True,'independent_holdout':False,
  'limits':'Exposure to an expected optional source is not whole-scene semantic precision, mandatory adoption, native fact approval, pixel quality, or causal improvement. Combinations can be incompatible; all-target exposure is not simultaneous-use permission. Boundary/control before and after results require manual interpretation.'}
 write(O/'retrieval-qualification.json',{'summary':summary,'after':after,'before':before});print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
