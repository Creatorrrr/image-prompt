"""Additional read-only source review after Chrome recovered sections 12-17."""
from pathlib import Path
import collections, hashlib, json, re, subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];A=ROOT/'skills/photo-prompt-image-generator/assets'
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,x):(HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
PATTERN=r'\b(tricorn|bicorne|shako|coatee|gorget|waistcoat|breeches|cravat|panniers|empire waist|masquerade|boudoir|prosthetic|laudanum|ambulance)\b|스테이즈|파니에|샤코|코티|고젯|의족|의수'
NOTES={
 'cand_6bd1ad0fcf775ccaa867d438086d2182':('refine',['J01'],'낡은 삼각모 소품과 human guard를 보존한다. 세 챙의 정밀 기하는 현재 문구에 없으므로 원전 도판과 자격 검토가 추가로 필요하다.'),
 'cand_fc38c2780414540280a85f200fec999e':('reuse',['J11'],'몸판 아래 가슴 밑 이음선에서 치마가 내려오는 전체 원문이 해당 실현과 직접 대응한다. 정치적 제국/귀족/고증의 증거는 아니다.'),
 'cand_3d681021062f56b6a0254a3c1f110423':('context',['J11'],'좁은 column형 치마가 포함된 별도 실현이다. 이 추가 한정을 삭제해 일반 엠파이어 이음선 후보로 재명명하지 않는다.'),
 'cand_dfd89db900735d9b8116fccb6c52a6d2':('context',['J10'],'겉치마가 좌우로 넓어진 가시 silhouette다. 숨은 pannier/hoop 받침을 직접 보여 주는 원문이 아니다.'),
 'cand_22079d8d7f705caea3f446184813280f':('context',['J10'],'겉치마의 앞뒤 깊이와 좌우 폭 관계를 보존한다. 구조가 안 보이면 내부 후프를 승인하지 않는다.'),
 'cand_f25347e368185c8780231631bf099418':('reuse',['J06'],'겉코트 안에 별도 열린 조끼 앞판이 보이는 전체 관계를 재사용 검토한다. 시대/성별/신분은 자동 추가하지 않는다.'),
 'cand_e054ebbfbd5f5655a72a8794fcf71a1b':('context',['J06'],'조끼처럼 보이는 패널이 재킷에 붙어 있고 별도 조끼가 아니라는 원문이다. 독립 waistcoat의 반례 control로 보존한다.'),
 'cand_613c117d227555dca27eef2bc0b5b0be':('reuse',['J13'],'화장대/거울/문/별도 옆방 침대라는 완전 관계가 직접 대응한다. 방의 용도나 사람의 성적 관계를 새로 부여하지 않는다.'),
 'cand_316522c32c815f7b804490596151ced5':('context',['J13','I17'],'부두아르/침실/살롱 등의 기능 구별을 다루는 diagnostic이다. positive 가구 실현이나 실제 행위 증거로 승격하지 않는다.'),
 'cand_547ff2a6433b5ef6ae319ac4e7c80812':('context',['J14'],'구급차-들것-임상 인계라는 현대 이송 관계다. 역사적 두 바퀴 구호마차로 자동 전환하지 않는다.'),
 'cand_9815ce0405f353cabb702d81bc02f9fd':('context',['J14'],'이송 monitor와 restraint를 포함한 완전 세트다. monitor를 삭제해 역사 장면으로 개조하지 않는다.'),
 'cand_ce7b80fdc8f55da78b01b8a61ab3946d':('reuse',['I18'],'잔여 사지/소켓/의지의 연결을 부품 수준으로 재사용 검토한다. 수술·통증·전쟁 원인·회복 성공·동의는 추가하지 않는다.'),
 'cand_0d8982616d8254c39611ecdd8e1760bc':('reuse',['I18'],'치유된 잔여 전완과 옆 탁자의 별도 의수라는 전체 원문을 보존한다. 치유된 상태의 선언은 임상 진단이나 절단 원인 증거가 아니다.'),
}
def main():
    raw=(A/'photo_candidate_corpus_manifest.json').read_bytes();m=json.loads(raw);cs={};bs=collections.defaultdict(list);hashes={}
    for e in m['modules']:
        b=(A/e['file']).read_bytes();hashes[e['file']]=sha(b);p=json.loads(b)
        if e['kind']=='candidates':
            for cid,c in p['candidates'].items():cs[cid]=(e['file'],c)
        elif e['kind']=='slot_bindings':
            for v in p['slot_bindings'].values():bs[v['candidate_id']].append(v)
    assert (A/'photo_candidate_corpus_manifest.json').read_bytes()==raw
    assert all(sha((A/k).read_bytes())==v for k,v in hashes.items()), 'source drift; repeat supplemental snapshot'
    rx=re.compile(PATTERN,re.I);records=[]
    for cid,(module,c) in cs.items():
        matched={k:sorted(set(rx.findall(json.dumps(c['content'].get(k,''),ensure_ascii=False)))) for k in ['en','ko','aliases','keywords','embedding_text','definition']}
        matched={k:v for k,v in matched.items() if v}
        if not matched and cid not in NOTES:continue
        decision,ids,reason=NOTES.get(cid,('defer',[],'어휘 일치만 확인했다. 수동 의미 검토 미완료이므로 채택하지 않는다.'))
        records.append(dict(candidate_id=cid,source_module=module,matched_fields=matched,disposition=decision,related_card_ids=ids,reason_ko=reason,manual_review=cid in NOTES,record=c,bindings=bs[cid],record_sha256=sha(json.dumps(c,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),native_approval=False,retrieval_rank=None))
    result=dict(scope='Additional working-tree read-only audit after Chrome recovery; not retrieval or native review',head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),manifest_sha256=sha(raw),module_sha256=hashes,candidate_count=len(cs),pattern=PATTERN,excluded_false_match='The English verb stays is not a garment match. Initial broad exploration was narrowed before this saved audit.',records=records,manual_review_count=sum(r['manual_review'] for r in records))
    dump('existing-source-supplement.json',result)
    lines=['# 크롬 전문 확인 후 추가 후보 감사','',f"현재 authored source {len(cs):,}개에서 {len(records)}건을 보존했고 {result['manual_review_count']}건의 전체 문구/조건/효과/binding을 수동 검토했다. 최초 44건/13건 감사와 겹침이 있으므로 단순 합산하지 않는다.",'','| CID | 결정 | 카드 | 판단 |','|---|---|---|---|']
    for r in records:
        if r['manual_review']:lines.append(f"| `{r['candidate_id']}` | {r['disposition']} | {', '.join(r['related_card_ids'])} | {r['reason_ko']} |")
    (HERE/'CORPUS-SUPPLEMENT.md').write_text('\n'.join(lines)+'\n');print(json.dumps({'matches':len(records),'manual_review_count':result['manual_review_count'],'candidate_count':len(cs)},ensure_ascii=False))
if __name__=='__main__':main()
