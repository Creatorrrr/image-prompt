"""Read authored source only; write snapshots solely within this research folder."""
from pathlib import Path
import collections, hashlib, json, re, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
def digest(b): return hashlib.sha256(b).hexdigest()
def canonical(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def dump(name, x): (HERE/name).write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n')
PATTERNS = {
    'specific': r'flintlock|musket|gunpowder|black powder|miquelet|snaphaunce|brown bess|charleville|baker rifle|ramrod|paper cartridge|socket bayonet|blunderbuss|cuirass|hussar|grenadier|line infantry|broadside|carronade|ravelin|glacis|star fort|powder mage|전열보병|수석식|플린트록|화약|머스킷',
    'adjacent': r'\b(pistol|rifle|cannon|bayonet|tricorn|shako|epaulette|bastion|redoubt|semaphore|cartridge|pelisse|sabre|saber)\b|삼각모|총검|견장|흉갑|화승|프록코트',
}
NOTES = {
 'cand_42d2b29291fe52db93a6bf09617d266e': ('refine', ['D05','D06'], 'EN은 본체 부착 보루/해자 건너 분리된 외보/입구 차폐를 갖지만 KO는 제목형 축약이다. 번역·embedding·effect 범위를 검토하고 이 전체 관계를 보존한다.'),
 'cand_9c0d3821b9ae5cc49781a59f278b4f29': ('refine', ['D01'], '기존 포좌-흉벽-포문 정렬을 재사용 검토한다. KO 축약을 보완하고 cannon의 신규 owner와 effects를 현행 계약에 맞게 직접 검토한다.'),
 'cand_c79a072f53df533cb9a46d96e9ced116': ('reuse', ['A03'], '외부 wheel이 있는 휠록 전시다. alias의 플린트록은 비교 경계일 뿐 positive flintlock 격발부가 아니다. 전시/총열 아래 위치의 전체 의미를 유지하고 원전 도판으로 재검토한다.'),
 'cand_db7d982e859c5f52aa75982e7e263f8a': ('context', ['A01','B01'], 'EN은 일반 총기 정물이나 embedding에는 현대 슬라이드/회전탄창/receiver가 있다. 수석식 정답으로 취급하지 않는다. 기능성도 원문 외형만으로 추정하지 않는다.'),
 'cand_2a4606c052a65cb194a4dbf7ae04447d': ('context', ['A07','B01'], '현대 소총 구조라는 명시를 보존한다. rifle과 flintlock의 축을 구분하는 현대 control이며 역사 총기 부족을 채우는 재사용 대상이 아니다.'),
 'cand_6bd1ad0fcf775ccaa867d438086d2182': ('reuse', ['C07'], '낡은 삼각모 소품만 재사용 검토 가능하다. pirate tag는 착용자의 직업·시대·국가 증거가 아니다. human guard를 유지한다.'),
 'cand_00e1c881614a51ed8f149a9a4fc0b416': ('context', ['C06'], '흉갑과 러프가 함께 있는 완전 bundle이다. 러프를 삭제해 나폴레옹 흉갑기병으로 재명명하지 않는다. 흉갑기병은 별도 실현을 제안한다.'),
 'cand_9debbd3052f958bdb327be49da46722c': ('context', ['C08'], '왕실/공주 문맥과 실제 subject_applicability를 포함한다. 일반 장교 제복 또는 현지 회사군으로 무단 변환하지 않는다.'),
 'cand_f365853663525b9e852396e14eae05c8': ('reuse', ['C08'], '왕실 문장 견장의 원래 전체 뜻이 요청과 맞을 때만 재사용한다. 장교 계급·충성·고증의 자동 증거로 삼지 않는다.'),
 'cand_e55f66332e315f20bf90ddbb61f8d36b': ('reuse', ['C08'], '재킷 어깨의 장식 견장과 부착부를 부품 수준으로 검토한다. 수석식 시대와 계급은 별도 명시가 필요하다.'),
 'cand_748ceab940f952b9830b04d8b619219e': ('reuse', ['B08'], '세이버라는 물건 유형은 재사용 검토 가능하다. 별도 곡률·칼집·소유자·접촉·역사 모델은 이 CID에서 얻지 못한다.'),
 'cand_ce196d11c0855603851e504849247bec': ('reuse', ['B08'], '칼집 속 의장용 소품이라는 전체 한정이 맞을 때만 재사용한다. 실제 전투 무기 또는 뽑힌 검으로 바꾸지 않는다.'),
 'cand_033e7d080d73a070221b915a72412fea': ('context', ['B04'], 'bayonet은 카메라 렌즈 마운트다. 총검 정답이 아닌 다의어 control이다.'),
}

def main():
    manifest_path=ASSETS/'photo_candidate_corpus_manifest.json'
    manifest_bytes=manifest_path.read_bytes(); manifest=json.loads(manifest_bytes)
    candidates={}; bindings=collections.defaultdict(list); hashes={}; catalog={}
    for entry in manifest['modules']:
        path=ASSETS/entry['file']; raw=path.read_bytes(); hashes[entry['file']]=digest(raw)
        payload=json.loads(raw); field=entry['kind']
        if field=='candidates':
            for cid,c in payload[field].items():
                assert cid not in candidates, cid
                candidates[cid]=(entry['file'],c)
        elif field=='slot_bindings':
            for b in payload[field].values(): bindings[b['candidate_id']].append(b)
        elif field=='slot_catalog': catalog.update(payload[field])
    assert manifest_path.read_bytes()==manifest_bytes, 'manifest drift; repeat snapshot'
    assert all(digest((ASSETS/f).read_bytes())==h for f,h in hashes.items()), 'source drift; repeat snapshot'
    matches=[]; snapshots=[]; fields=('en','ko','aliases','keywords','tags','definition','embedding_text','concept_units')
    for cid,(module,c) in candidates.items():
        content=c['content']; found={}
        for name,pattern in PATTERNS.items():
            rx=re.compile(pattern,re.I)
            hit={key: sorted(set(rx.findall(json.dumps(content.get(key,''),ensure_ascii=False)))) for key in fields}
            hit={k:v for k,v in hit.items() if v}
            if hit: found[name]=hit
        if not found: continue
        decision,related,reason=NOTES.get(cid,('defer',[], '인접/다의어 어휘 일치다. 원문·conditions·effects·bindings를 snapshot으로 보존했으며 아직 의미 동등성 검토를 완료하지 않았다.'))
        row={'candidate_id':cid,'source_module':module,'matched_fields':found}
        matches.append(row)
        snapshots.append(dict(row,disposition=decision,related_card_ids=related,reason_ko=reason,record_sha256=digest(canonical(c)),record=c,bindings=bindings[cid],manual_review=cid in NOTES,retrieval_rank=None,native_approval=False))
    baseline={'date':'2026-10-23','timezone':'Asia/Seoul','head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'git_status_porcelain_z':subprocess.check_output(['git','status','--porcelain=v1','-z'],cwd=ROOT).decode().split('\0'),'manifest_sha256':digest(manifest_bytes),'module_sha256':hashes,'candidate_count':len(candidates),'binding_count':sum(map(len,bindings.values())),'record_kind_counts':dict(collections.Counter(c['record_kind'] for _,c in candidates.values())),'slot_count':len(catalog),'scope':'Working-tree authored source snapshot; no runtime imports, index build, retrieval, generation, installation or Git writes.'}
    for relative in ['skills/photo-prompt-image-generator/retrieval-runtime.json','skills/photo-prompt-image-generator/assets/photo_candidate_search.json','skills/photo-prompt-image-generator/SKILL.md']:
        path=ROOT/relative
        baseline.setdefault('protected_files',{})[relative]=digest(path.read_bytes()) if path.exists() else None
    dump('BASELINE.json',baseline)
    dump('corpus-lexical-audit.json',{'scope':'Fixed authored text fields only; lexical coverage is not semantic absence or search evaluation.','patterns':PATTERNS,'matches':matches,'specific_count':sum('specific' in x['matched_fields'] for x in matches),'adjacent_count':sum('adjacent' in x['matched_fields'] for x in matches)})
    dump('existing-source-mapping.json',{'manifest_sha256':baseline['manifest_sha256'],'records':snapshots,'manual_review_count':sum(x['manual_review'] for x in snapshots),'unreviewed_matches_policy':'defer; do not imply full-corpus semantic review'})
    lines=['# 기존 후보 원문 감사','',f"작업 트리 {len(candidates):,}개 source와 {baseline['binding_count']:,}개 binding을 읽었다. 지정 어휘 {len(matches)}개 일치 중 {len(NOTES)}개를 수동 검토했다. 특정 용어가 없다고 전체 의미가 없다고 단정하지 않으며 실제 검색은 실행하지 않았다.",'','| CID | 결정 | 카드 | 이유 |','|---|---|---|---|']
    for x in snapshots:
        if x['manual_review']: lines.append(f"| `{x['candidate_id']}` | {x['disposition']} | {', '.join(x['related_card_ids'])} | {x['reason_ko']} |")
    lines+=['','`existing-source-mapping.json`에 원본 전체/conditions/effects/bindings/record hash를 저장했다. 어휘만 일치한 나머지는 모두 defer이다. 파일명 재사용은 현재 source 재사용과 구별하며, actual CID/RID·native 자격은 이번 연구 초안에 부여하지 않았다.']
    (HERE/'CORPUS-FINDINGS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({k:baseline[k] for k in ['head','candidate_count','binding_count','slot_count','record_kind_counts']},ensure_ascii=False))
    print(json.dumps({'lexical_matches':len(matches),'manual_reviews':sum(x['manual_review'] for x in snapshots)},ensure_ascii=False))
if __name__=='__main__': main()
