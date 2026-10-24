"""Bilingual development probes of the complete sealed pool; no topic prefilter."""
from pathlib import Path
import json,sys

O=Path(__file__).resolve().parent;R=O.parents[4]
def read(p):return json.loads(p.read_bytes())
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

CASES=[
 ('umbrella',['R07'],'두 사람 머리 위를 같은 우산 천 하나가 덮고 그 우산대는 둘 사이에 있다.','One shared umbrella canopy extends over both people, with its shaft between them.'),
 ('earbuds',['R08'],'서로 다른 두 귀에 들어간 이어버드의 선이 하나의 분기점을 지나 같은 기기로 이어진다.','The cables from earbuds at two different people’s ears meet at one junction leading to the same device.'),
 ('sleeve',['R05'],'상대의 맨 손목 대신 소맷단의 천만 손끝으로 집는다.','Fingertips pinch only another person’s sleeve fabric near the cuff, leaving the bare wrist untouched.'),
 ('comic_reaction',['F03'],'한 사람의 접시 위 케이크가 무너져 있고 다른 사람이 그 케이크를 보며 반응한다.','One person holds a collapsed cake on a plate while another person looks at the cake and reacts.'),
 ('shoulder_openings',['W09'],'어깨 위 지지 천과 소매가 남은 상의의 둘러싸인 어깨 구멍.','A top retains shoulder straps and sleeves around bounded shoulder cutouts.'),
 ('screen_mismatch',['S09'],'같은 채팅 화면의 수신자 머리글은 B인데 메시지의 호명은 C다.','Within one chat screen the recipient header names B but the message salutation addresses C.'),
 ('slow_burn',[],'관계가 긴 시간에 걸쳐 천천히 깊어지는 슬로번이라는 서사 맥락.','The narrative describes a slow-burn relationship developing over an extended period.'),
 ('ordinary_work',[],'동료들이 각자 다른 서류를 읽는 평범한 업무 장면.','Coworkers independently read different documents in an ordinary work scene.'),
]

def main():
    successor=read(O/'successor.json');native=Path(successor['store'])/'generations'/successor['native_generation_id'];sys.path.insert(0,str(native/'scripts'))
    from photo_h_f2_generation import Generation
    from photo_h_f2_encoder import LocalEncoder
    import photo_canonical_source as canonical
    g=Generation(successor['store'],successor['generation_id'],full=True);index=g.index()
    fresh=read(O/'new-native-records.json');mapping={r['card_id']:r['candidate_id'] for r in read(O/'adoption-review.json')}
    diagnostics={cid for cid,r in fresh.items() if r['record_kind']=='diagnostic'}
    assert diagnostics.isdisjoint({x['cid'] for x in g.metadata})
    queries=[(name,lang,ko if lang=='ko' else en,keys) for name,keys,ko,en in CASES for lang in ('ko','en')]
    with LocalEncoder(R/'skills/photo-prompt-image-generator') as encoder:
        assert encoder.binding==g.binding
        vectors=encoder.encode([q[2] for q in queries],'query')
    results=[]
    for (case,lang,query,keys),vector in zip(queries,vectors,strict=True):
        found=index.search(query,vector,g.binding)
        assert found['lane_calls']=={'BM25F':1,'local_cosine':1}
        targets={mapping[k] for k in keys}
        rank=next((i+1 for i,row in enumerate(found['order']) if row['cid'] in targets),None)
        results.append({'case':case,'language':lang,'query':query,'target_CIDs':sorted(targets),'target_rank':rank,'top10':found['order'][:10],'lane_calls':found['lane_calls'],'considered_CIDs':found['considered_CIDs'],'native_approval':False,'adoption':'NOT_ASSESSED'})
    for cid,record in fresh.items():assert canonical.native_snapshot(g.body.record(cid))==record
    result={'status':'whole_pool_development_probes_complete','queries':results,'diagnostics_excluded':len(diagnostics),'new_source_snapshots_exact':True,'pool_positive_CIDs':g.manifest['CID_count'],'generation_id':successor['generation_id'],'limits':'Six bilingual authored target cases and two bilingual controls; not holdout, semantic approval, causal improvement or image evidence.'}
    write(O/'retrieval-probes.json',result)
    print(json.dumps({'queries':len(results),'target_queries':sum(bool(x['target_CIDs']) for x in results),'target_at10':sum(x['target_rank'] is not None and x['target_rank']<=10 for x in results),'diagnostics_excluded':len(diagnostics)},ensure_ascii=False))

if __name__=='__main__':main()
