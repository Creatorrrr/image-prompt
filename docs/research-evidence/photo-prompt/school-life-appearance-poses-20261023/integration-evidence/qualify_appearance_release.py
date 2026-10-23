"""Full deployed validation and predeclared development probes, no safety/quality waivers."""
import gc;gc.disable()
import json,hashlib,sys,collections,gzip
from pathlib import Path
O=Path(__file__).resolve().parent;S=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator')
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if str(p).endswith('.gz') else p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def main():
 r=read(O/'successor.json');b=read(O/'release-base.json');sys.path.insert(0,str(Path(r['store'])/'generations'/r['native_generation_id']/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 import photo_recall_first as rf
 import photo_candidate_corpus as c
 import photo_canonical_source as canonical
 g=Generation(r['store'],r['generation_id'],full=True)
 fresh=read(O/'new-native-records.json');union=read(O/'release-new-native-records.json');corpus=c.load(Path(r['store'])/'generations'/r['native_generation_id']/'assets')
 meta=read(g.root/'indexed-documents.json.gz');indexed={v['cid'] for v in meta};pos={cid for cid,x in fresh.items() if x['record_kind']=='visual_option'};diag=set(fresh)-pos
 assert len(pos)==140 and len(diag)==28 and pos<=indexed and not diag&indexed
 assert all(canonical.native_snapshot(corpus['candidates'][cid])==x for cid,x in union.items())
 write(O/'registration-qualification.json',{'status':'pass','new_visual_CIDs':len(pos),'new_diagnostic_CIDs':len(diag),'new_visual_CIDs_indexed':len(pos&indexed),'diagnostic_positive_leaks':len(diag&indexed),'released_source_native_roundtrip_exact':len(union),'full_deployed_generation_validation':True,'native_approval':False})
 del corpus;gc.collect()
 cases=read(O/'retrieval-development-cases.json')['cases'];assert len(cases)==28;sourcehash=hashlib.sha256((O/'retrieval-development-cases.json').read_bytes()).hexdigest();assert read(O/'retrieval-cases-freeze.json')['sha256']==sourcehash
 binding=read(g.root/'manifest.json')['binding'];cache=O/'qualification-query-evidence.json'
 if cache.exists():ev=read(cache)
 else:
  ev={'query_source_sha256':sourcehash,'binding':binding,'rows':[]}
  with LocalEncoder(S) as encoder:
   assert encoder.binding==binding
   for off in range(0,len(cases),12):
    batch=cases[off:off+12]
    for case,e in zip(batch,encoder.encode([x['query'] for x in batch],'query'),strict=True):
     rf.check_embedding(e,binding,case['query'],'query');ev['rows'].append({'id':case['id'],'query':case['query'],'embedding':e})
    print('encoded',len(ev['rows']),flush=True)
  write(cache,ev)
 assert ev['query_source_sha256']==sourcehash and ev['binding']==binding
 assert [(x['id'],x['query']) for x in cases]==[(x['id'],x['query']) for x in ev['rows']]
 lookup={x['card_id']:x['candidate_id'] for x in read(O/'data-integration.json')['cards']};index=g.index();results=[]
 for case,e in zip(cases,ev['rows'],strict=True):
  out=index.search(case['query'],e['embedding'],binding);assert out['lane_calls']=={'BM25F':1,'local_cosine':1};order=out['order'];assert not any(x['cid'] in diag for x in order)
  expected={lookup[k] for k in case['expected_cards']};rank=next((i+1 for i,x in enumerate(order) if x['cid'] in expected),None)
  results.append({**case,'target_rank':rank,'top10':order[:10],'new_visual_at10':[x['cid'] for x in order[:10] if x['cid'] in pos],'generation_id':g.id,'route':'whole-pool development probe; not managed adoption','considered_CIDs':out['considered_CIDs']})
  write(O/'retrieval-progress.json',{'completed':len(results),'cases':results});print('searched',case['id'],'target rank',rank,flush=True)
 del index,g;gc.collect()
 baseline=Generation(b['store'],b['config']['generation_id'],full=True);baselineindex=baseline.index();controls=[]
 for case,e in zip(cases,ev['rows'],strict=True):
  if case['set']!='general_control':continue
  out=baselineindex.search(case['query'],e['embedding'],binding);after=next(x for x in results if x['id']==case['id']);before=[x['cid'] for x in out['order'][:10]];afterids=[x['cid'] for x in after['top10']]
  controls.append({'id':case['id'],'before':before,'after':afterids,'top10_exact_order_preserved':before==afterids,'top10_overlap':len(set(before)&set(afterids))})
 positive=[x for x in results if x['set']=='development'];at32=sum(x['target_rank'] is not None and x['target_rank']<=32 for x in positive)
 summary={'status':'complete','queries':len(results),'sets':dict(collections.Counter(x['set'] for x in results)),'positive_target_at10':sum(x['target_rank'] is not None and x['target_rank']<=10 for x in positive),'positive_target_at32':at32,'positive_gate':'PASS' if at32==16 else 'FAIL','diagnostic_positive_leaks':0,'control_top10_unchanged':sum(x['top10_exact_order_preserved'] for x in controls),'native_approval':False,'limit':'Authored development probes, no independent holdout, no prompt or pixel causality claim. Boundary retrieval is exposure, not boundary reasoning proof.'}
 write(O/'retrieval-qualification.json',{'summary':summary,'cases':results,'baseline_controls':controls});print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
