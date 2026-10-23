"""Whole-pool source-derived development probes and unchanged ordinary controls."""
import gc;gc.disable()
from pathlib import Path
import json,sys,hashlib
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt')
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
B=read(O/'before.json');S=read(O/'successor.json');I=read(O/'install.json');assert I['status']=='pass'
store=Path(I['store']);sys.path.insert(0,str(store/'generations'/S['native_generation_id']/'scripts'))
from photo_h_f2_generation import Generation
from photo_h_f2_encoder import LocalEncoder
from photo_runtime_sources import RuntimeSnapshotProvider
import photo_canonical_source as canon,photo_recall_first as rf
fresh=read(O/'new-native-records.json');cards=read(O/'semantic-cards.json');cases=[]
for c in cards:
 if c['id'].startswith('R2V'):
  for lang in ('ko','en'):cases.append(dict(id=c['id']+'-'+lang,cohort='source_derived_development',query=c['visible_'+lang],target=c['candidate_id']))
controls=[('거들지의 흰색 부분을 보지만 접힘 가장자리는 소매 뒤에 가려졌다.','A white cuff is visible but its fold edge is hidden behind the sleeve.'),('폴로네즈 치마의 세 덩이는 보이지만 안쪽 끈은 보이지 않는다.','Three puffs of a polonaise skirt are visible while the internal cords remain hidden.'),('학 두 마리가 있는 그림으로 실제 관직과 신분이 증명되는가.','Can an image of two cranes prove an actual office and rank?'),('닫힌 펜던트에서 향기와 병 예방 효과를 확인한다.','Determine fragrance and disease prevention from a closed pendant.'),('머리 장식 한 개만 있고 목걸이와 팔찌는 프레임 밖이다.','Only a headdress is visible; the necklace and bracelets are outside the frame.'),('서 있는 한 장으로 뒷걸음 퇴장 순서를 확정한다.','Establish a backing-away exit sequence from one standing still image.'),('평범한 현대 카페에서 커피 잔을 내려놓는다.','A person sets down a coffee cup in an ordinary modern cafe.'),('모래사장에서 파란 바람막이를 입고 걷는다.','Walking on a sandy beach wearing a blue windbreaker.'),('유리 온실에서 화분에 물을 주는 사람.','A person waters plants in a glass greenhouse.'),('달 밝은 사막에 놓인 빈 캠핑 의자.','An empty camping chair in a moonlit desert.'),('흰 벽 스튜디오에서 상반신 얼굴 인물 사진.','An upper-body face portrait in a white-wall studio.'),('전족용 작은 신과 중앙 받침 신발을 구별한다.','Distinguish a tiny bound-foot shoe from a shoe with a central platform support.')]
for i,(ko,en) in enumerate(controls):
 for lang,q in [('ko',ko),('en',en)]:cases.append(dict(id=f'CTRL{i:02}-{lang}',cohort='boundary_or_ordinary_control',query=q,target=None))
write(O/'qualification-cases.json',{'cases':cases,'independent_holdout':False})
newm=read(store/'h-f2-generations'/S['generation_id']/'manifest.json');oldm=read(Path(B['store'])/'h-f2-generations'/B['config']['generation_id']/'manifest.json')
proof=O/'query-embeddings.json'
if proof.exists():encoded=read(proof)
else:
 encoded=[]
 with LocalEncoder(R/'skills/photo-prompt-image-generator') as enc:
  assert enc.binding==newm['binding']==oldm['binding']
  for st in range(0,len(cases),12):
   part=cases[st:st+12];es=enc.encode([c['query'] for c in part],'query')
   for row,e in zip(part,es,strict=True):rf.check_embedding(e,enc.binding,row['query'],'query');encoded.append(dict(id=row['id'],query=row['query'],embedding=e))
   print('encoded',len(encoded),flush=True)
 write(proof,encoded)
assert [(x['id'],x['query']) for x in encoded]==[(x['id'],x['query']) for x in cases]
a=Generation(store,S['generation_id'],full=True);ai=a.index();b=Generation(B['store'],B['config']['generation_id'],full=True);bi=b.index();snap=RuntimeSnapshotProvider(store=store).load_generation(S['native_generation_id']);assert all(canon.native_snapshot(snap.data['candidates'][cid])==v for cid,v in fresh.items())
indexed={x['cid'] for x in a.metadata};assert not indexed&{cid for cid,v in fresh.items() if v['record_kind']=='diagnostic'};assert {cid for cid,v in fresh.items() if v['record_kind']=='visual_option'}<=indexed
rows=[]
for row,e in zip(cases,encoded,strict=True):
 result=ai.search(row['query'],e['embedding'],newm['binding']);assert result['lane_calls']=={'BM25F':1,'local_cosine':1};order=result['order'];out={**row,'top10':order[:10],'target_rank':next((i+1 for i,x in enumerate(order) if x['cid']==row['target']),None),'population':result['considered_CIDs']}
 if row['cohort']=='boundary_or_ordinary_control':
  old=bi.search(row['query'],e['embedding'],oldm['binding']);assert old['lane_calls']=={'BM25F':1,'local_cosine':1};out['old_top10']=old['order'][:10];out['overlap']=len({x['cid'] for x in old['order'][:10]}&{x['cid'] for x in order[:10]})
 rows.append(out)
 if len(rows)%12==0:print('searched',len(rows),flush=True)
dev=[x for x in rows if x['target']];con=[x for x in rows if not x['target']];summary=dict(status='pass',queries=len(rows),development_queries=len(dev),target_at10=sum(x['target_rank'] is not None and x['target_rank']<=10 for x in dev),target_at32=sum(x['target_rank'] is not None and x['target_rank']<=32 for x in dev),before_control_queries=len(con),control_mean_top10_overlap=sum(x['overlap'] for x in con)/len(con),all_new_native_exact=True,diagnostics_excluded_from_positive_index=True,baseline_positive_CIDs=b.manifest['CID_count'],after_positive_CIDs=a.manifest['CID_count'],limits='Source-derived development queries, not independent holdout or causal image improvement. Whole-pool retrieval exposure does not authorize sampling/adoption, historical authenticity or pixel success.')
write(O/'retrieval-qualification.json',dict(summary=summary,cases=rows));print(json.dumps(summary),flush=True)
