"""Whole-pool bilingual probes, independent of the three image arms."""
from pathlib import Path
import gc,json,sys,argparse,hashlib,collections
gc.disable()
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt')
E=R/'docs/research-evidence/photo-prompt/espionage-20261023/integration-evidence'
read=lambda p:json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['encode','after','before','summary']);phase=p.parse_args().phase
 B=read(O/'before.json')
 S=read(O/'successor.json') if (O/'successor.json').exists() else B['config']
 I=read(O/'install.json') if (O/'install.json').exists() else {'store':B['store']}
 sys.path.insert(0,str(Path(I['store'])/'generations'/S['native_generation_id']/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 import photo_recall_first as rf
 registry=read(E/'data-integration.json')
 lookup={v['card_id']:v['candidate_id'] for v in registry['adoptions'] if v['decision'] in ('new','reuse')}
 source=read(E.parent/'evaluation-cases.json')
 cases=[{'id':c['id']+'-'+lang,'cohort':c['split'],'language':lang,'query':c['query_'+lang],'expected_cards':c.get('expected_card_refs',[])} for c in source for lang in ('ko','en')]
 fingerprint=hashlib.sha256(json.dumps(cases,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 if phase=='encode':
  write(O/'frozen-query-cases.json',cases)
  old=read(Path(B['store'])/'h-f2-generations'/B['config']['generation_id']/'manifest.json')
  new=read(Path(I['store'])/'h-f2-generations'/S['generation_id']/'manifest.json')
  assert old['binding']==new['binding']
  data={'binding':new['binding'],'case_sha256':fingerprint,'rows':[]}
  with LocalEncoder(R/'skills/photo-prompt-image-generator') as enc:
   assert enc.binding==data['binding']
   for start in range(0,len(cases),24):
    rows=cases[start:start+24]
    for c,v in zip(rows,enc.encode([x['query'] for x in rows],'query'),strict=True):
     rf.check_embedding(v,enc.binding,c['query'],'query');data['rows'].append({'id':c['id'],'query':c['query'],'embedding':v})
    print('encoded',len(data['rows']),flush=True)
  write(O/'query-embeddings.json',data);return
 encoded=read(O/'query-embeddings.json')
 assert encoded['case_sha256']==fingerprint
 assert [(c['id'],c['query']) for c in cases]==[(x['id'],x['query']) for x in encoded['rows']]
 if phase in ('after','before'):
  store=Path(I['store']) if phase=='after' else Path(B['store'])
  gid=S['generation_id'] if phase=='after' else B['config']['generation_id']
  generation=Generation(store,gid,full=True);index=generation.index()
  assert generation.binding==encoded['binding']
  checkpoint=O/('probe-'+phase+'.json')
  result=read(checkpoint) if checkpoint.exists() else {'generation_id':gid,'case_sha256':fingerprint,'rows':[]}
  assert result['generation_id']==gid and result['case_sha256']==fingerprint
  done={c['id'] for c in result['rows']}
  for case,ev in zip(cases,encoded['rows'],strict=True):
   if case['id'] in done:continue
   if phase=='before' and case['cohort'] in ('source_literal_smoke','natural_regression'):continue
   found=index.search(case['query'],ev['embedding'],encoded['binding'])
   assert found['lane_calls']=={'BM25F':1,'local_cosine':1}
   targets={lookup[c] for c in case['expected_cards'] if c in lookup}
   result['rows'].append({**case,'registered_expected_CIDs':sorted(targets),
    'target_rank':next((i+1 for i,x in enumerate(found['order']) if x['cid'] in targets),None),
    'top8':found['order'][:8],'population':found['considered_CIDs'],'lane_calls':found['lane_calls']})
   if len(result['rows'])%24==0:
    write(checkpoint,result);print('searched',phase,len(result['rows']),flush=True)
  result['complete']=True;write(checkpoint,result);return
 after=read(O/'probe-after.json');before=read(O/'probe-before.json')
 assert after['complete'] and before['complete']
 assert len(after['rows'])==len(cases)
 groups={}
 for cohort in sorted({c['cohort'] for c in cases}):
  rows=[c for c in after['rows'] if c['cohort']==cohort];eligible=[c for c in rows if c['registered_expected_CIDs']]
  groups[cohort]={'queries':len(rows),'graded_queries':len(eligible),'target_at8':sum(c['target_rank'] is not None and c['target_rank']<=8 for c in eligible),'target_at32':sum(c['target_rank'] is not None and c['target_rank']<=32 for c in eligible),'by_language':{lang:{'graded':sum(c['language']==lang for c in eligible),'at8':sum(c['language']==lang and c['target_rank'] is not None and c['target_rank']<=8 for c in eligible)} for lang in ('ko','en')}}
 diagnostics={cid for cid,c in read(O/'new-native-records.json').items() if c['record_kind']=='diagnostic'}
 assert not any(x['cid'] in diagnostics for row in after['rows'] for x in row['top8'])
 summary={'status':'source_and_bilingual_whole_pool_probes_complete','queries':len(cases),'before_control_queries':len(before['rows']),'groups':groups,'positive_CIDs':read(Path(I['store'])/'h-f2-generations'/S['generation_id']/'manifest.json')['CID_count'],'diagnostics_excluded':True,
 'limits':'Literal smoke and card-author paraphrases are not an independent holdout. Source exposure is not adoption, native semantic approval, pixel quality or causal improvement. Before comparisons cover boundary/ordinary/nonvisual controls.'}
 write(O/'retrieval-qualification.json',{'summary':summary,'after':after,'before':before});print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
