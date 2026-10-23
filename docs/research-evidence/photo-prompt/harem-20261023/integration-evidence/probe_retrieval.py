"""Small bilingual whole-pool development probes. No candidate prefilter."""
from pathlib import Path
import json,sys,gc
O=Path(__file__).resolve().parent;R=O.parents[4]
read=lambda p:json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
CASES=[
 ('offers',['H01','H25'],'두 사람이 각자 다른 선물을 같은 사람에게 내밀고 수신자는 아직 받지 않았다.','Two people each extend a separate gift toward the same recipient, who has not accepted either gift.'),
 ('interlaced',['H07'],'서로 다른 두 사람이 손을 잡고 양손 손가락이 번갈아 엇갈리며 각 손목이 자기 팔로 이어진다.','Two distinct people hold hands with alternating interlaced fingers and each wrist remains connected to its own arm.'),
 ('sleeve',['H05'],'한 사람이 다른 사람 손목 근처 소매 천을 집고 맨 손목은 붙잡지 않는다.','One person pinches the fabric of another person’s sleeve near the cuff while leaving the bare wrist untouched.'),
 ('garter',['W17'],'성인 인물의 허리벨트에서 내려온 가터 끈과 클립이 별도 스타킹 윗단에 연결된다.','On an adult wearer, garter straps descend from a waist belt and their clips attach to the tops of separate stockings.'),
 ('ordinary_group',['H03','H26'],'세 동료가 공동 주방에서 읽기와 물 따르기와 정리를 각자 한다.','Three coworkers independently read, pour water and tidy up in a shared kitchen.'),
 ('context_consent',[],'복수 관계에 대한 모든 참여자의 인지와 동의라는 문맥.','Context states that every participant knows and consents to multiple relationships.'),
]

def main():
 s=read(O/'successor.json');native=Path(s['store'])/'generations'/s['native_generation_id'];sys.path.insert(0,str(native/'scripts'))
 from photo_h_f2_generation import Generation
 from photo_h_f2_encoder import LocalEncoder
 import photo_canonical_source as canonical
 g=Generation(s['store'],s['generation_id'],full=True);index=g.index()
 fresh=read(O/'new-native-records.json');mapping={x['card_id']:x['candidate_id'] for x in read(O/'adoption-review.json')}
 diags={cid for cid,r in fresh.items() if r['record_kind']=='diagnostic'}
 assert diags.isdisjoint({x['cid'] for x in g.metadata})
 queries=[(case,lang,ko if lang=='ko' else en,keys) for case,keys,ko,en in CASES for lang in ['ko','en']]
 with LocalEncoder(R/'skills/photo-prompt-image-generator') as encoder:
  assert encoder.binding==g.binding
  vectors=encoder.encode([x[2] for x in queries],'query')
 results=[]
 for (case,lang,query,keys),vector in zip(queries,vectors,strict=True):
  found=index.search(query,vector,g.binding);assert found['lane_calls']=={'BM25F':1,'local_cosine':1}
  targets={mapping[x] for x in keys};rank=next((n+1 for n,row in enumerate(found['order']) if row['cid'] in targets),None)
  results.append({'case':case,'language':lang,'query':query,'target_CIDs':sorted(targets),'target_rank':rank,'top10':found['order'][:10],
    'lane_calls':found['lane_calls'],'considered_CIDs':found['considered_CIDs'],'native_approval':False,'adoption':'NOT_ASSESSED_BY_THIS_PROBE'})
 for cid,record in fresh.items():assert canonical.native_snapshot(g.body.record(cid))==record
 write(O/'retrieval-probes.json',{'status':'whole_pool_bilingual_development_probes_complete','queries':results,'context_diagnostics_excluded':len(diags),
  'new_source_snapshots_exact':True,'pool_positive_CIDs':g.manifest['CID_count'],'generation_id':s['generation_id'],
  'limits':'Twelve authored development queries, not an independent recall estimate, semantic/native approval, adoption or image-quality proof.'})
 print(json.dumps({'queries':len(results),'target_queries':sum(bool(x['target_CIDs']) for x in results),'target_at10':sum(x['target_rank'] is not None and x['target_rank']<=10 for x in results),'diagnostics_excluded':len(diags)},ensure_ascii=False))

if __name__=='__main__':main()
