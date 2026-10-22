"""Read-only corpus inspection; writes snapshot evidence only in this directory."""
import collections,hashlib,json,pathlib,re
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(obj):return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
PATTERNS={
 'dying_earth_label':r'\bdying\s+(?:earth|sun)\b|죽어\s*가는\s*태양|노쇠한\s*세계',
 'cozy_label':r'\bco[sz]y\b|코지',
 'hospitality':r'\bhospitality\b|환대',
 'communal_food':r'\bcommunal\s+(?:meal|oven|table|bread)\b|\bsharing\s+(?:bread|food)\b|공동\s*(?:화덕|식사|식탁)',
 'serving_transfer':r'\b(?:serving|feeding|sharing|offering)\b.*\b(?:soup|bread|bowl|cup|food)\b',
 'repair':r'\b(?:repair|repairing|mending|darning)\b|수선|수리',
 'ration':r'\bration(?:s|ed|ing)?\b|배급',
 'molting':r'\b(?:molt|molting|molted|ecdysis|exuvia|exuviae)\b|탈피',
 'fungal_form':r'\b(?:mycelium|mycelial|fungal|fungus|fungi)\b|균사|균류',
 'spolia':r'\bspolia\b|스폴리아',
 'palimpsest':r'\bpalimpsest\b|팔림프세스트',
 'mourning':r'\bmourn(?:ing)?\b|\bfuneral\b|장례|애도',
 'bureaucratic':r'\bbureaucratic\b|관료|시민권',
 'infrastructure':r'\binfrastructure\b|배관\s*(?:수리|보수)|기반\s*시설',
}
# Candidate IDs are exact observed neighbors, not target retrieval outputs.
SELECTED={
 'cand_69aad1c674b64b97968b2f8673853038':('reuse_component',['D01','D02','D03'],'티포트 몸·주둥이·손잡이·뚜껑. 수프 전달 동작이나 손님을 추가할 권한은 없음.'),
 'cand_e42be4c368ba8e143d743e35db88b881':('reuse_component',['D02'],'기존 도구·용기·받침의 실제 접촉. 별도 기존 소유자 조건과 모든 효과를 보존해야 함.'),
 'cand_0bb2983bbfaa5b19bbcd8b811ae3a8a1':('context_only',['H06','H11'],'섭취자·음식 출처의 구분용 diagnostic. 긍정 후보로 재분류하지 않음.'),
 'cand_32f534773ab55b75bbcf885e4b56e012':('adjacent_not_generic_reuse',['D06','D12'],'무대 기술자·갭모에 대비·반환의 맥락이 붙음. 일반 돌봄·성역으로 라벨만 교체하면 의미가 달라짐.'),
 'cand_bf0bd293edea52e5985e0a6256033af6':('adjacent_not_generic_reuse',['D06'],'변신 히로인·이중생활·새벽·호출기 맥락 보존 필요. 단순 의복 수선과 같지 않음.'),
 'cand_83206043de15574488e68c0dca2cd729':('refine_neighbor',['A08','D06'],'필수 생활품과 기능 마모의 수선이라는 좋은 이웃. 실제 도구·소유자·접점은 초안에서 더 구체화해야 함.'),
 'cand_a04cdd9877de5455b64aa92197bcf3cf':('reuse_scoped',['D06'],'성인 섬유 작업자와 봉제 인형. 비인간 신체 간호로 변환하면 대상과 효과가 바뀜.'),
 'cand_74c968440a0e56b1907e181579c565b4':('refine_neighbor',['B01','D06'],'재사용 부품·수선 흔적의 개념은 이웃이지만 로코코 패니어 구조를 건축 스폴리아로 치환할 수 없음.'),
 'cand_83336192837d504da64501bb413d35ae':('reuse_context',['E03','E06'],'국경 지도와 배급 창구라는 장소. 구체적 계량·음식 전달·공정성을 증명하지 않음.'),
 'cand_c49cab39f4375620ad188e535af021de':('refine_neighbor',['E01','A02'],'에테르 카트리지 교체·하류 흐름 검증·인계가 붙은 완전 절차. 정지 장면에서 모두 보인다고 단정하면 안 됨.'),
 'cand_52b17aedc71a5b608e903aec505bccc1':('reuse_component',['E03','E07'],'배급 토큰·필터·검사표·접근 가능한 줄의 소품 묶음. 행위자와 계량 접점은 별도 필요.'),
 'cand_cfb0f5034e965ac8bf9404e74062ab39':('context_only',['E02','E03'],'공정 배급과 정당성의 상황. 외형으로 입증하는 규칙으로 전환 금지.'),
 'cand_b1dff106e3f85371bc1ad2beb7760e22':('reuse_declared_role',['E10'],'장례지도사라는 선언된 직업. 얼굴·옷만으로 직업을 진단하지 않음.'),
 'cand_6c405a8b0ca75bc2a211e7ce949809c7':('reuse_component',['B07','H03'],'기존 유골 저장·접근 통로. 애도 행동·사회 제도를 추가하는 근거 아님.'),
 'cand_8b65ed0e09195a94b2bd3b269967e5dd':('reuse_component',['B07'],'묘 정면·장례 부조·입구. 식품 좌판과는 별도 선택 관계.'),
 'cand_39c6cd09418d53a88f6a77fb330ced46':('reuse_component',['C01','C09'],'숲 바닥의 균사·작은 균류. 물·빛·집과 교환하는 관계는 없음.'),
 'cand_5c55276f88ca543f99e39f23eb3a95bc':('reuse_component',['C01'],'기질 위 가지줄·결절의 형태. 기억망·지능·급수 호스와 합치지 않음.'),
 'cand_4a860cd5b3415010a963025a16272a66':('reuse_component',['C08'],'숙주 경계의 균류 부착. 질환·기생 비용·동의는 별도.'),
 'cand_253d14b94e0b5b13b3fb9a41eab3d9c6':('reuse_component',['B10'],'종이의 밑글과 덧글. 도시 벽의 새 간판에 그대로 재태깅하면 소유자·재료가 바뀜.'),
 'cand_b99c238a660a5456a449f51519650678':('reuse_component',['B10'],'같은 필기면의 두 층. 건축 층위·연대·실제 해독을 추가하지 않음.'),
 'cand_718d416cbd8d57c5822d649710691324':('context_neighbor',['D07'],'작고 아늑한 아파트 라벨은 환대 동작·공동 식사·장르 조합의 증거 아님.'),
 'cand_b7c88f6ae6c151a18fcdade0fbfeae28':('false_friend',['C03'],'molten rock는 molting이 아니다. 초기 단순 부분문자열 탐색의 오탐 대조.'),
 'cand_98b7b7c37b725c98907ca621370c1d79':('false_friend',['D06'],'조석 수선은 옷을 고치는 수선이 아니다. 한국어 다의어 오탐 대조.'),
 'cand_d5cea5d299db561ea9415b8fa0f38f64':('false_friend',['E03'],'calibration은 ration이 아니다. 영어 부분문자열 오탐 대조.'),
}

def main():
    manifest_raw=(ASSETS/'photo_candidate_corpus_manifest.json').read_bytes()
    manifest=json.loads(manifest_raw);rows=[];bindings=collections.defaultdict(list);hashes={}
    for mod in manifest['modules']:
        raw=(ASSETS/mod['file']).read_bytes();hashes[mod['file']]=sha(raw);payload=json.loads(raw)
        if mod['kind']=='candidates':
            for cid,rec in payload['candidates'].items():rows.append((cid,rec,mod['file']))
        elif mod['kind']=='slot_bindings':
            for bind in payload['slot_bindings'].values():bindings[bind['candidate_id']].append(bind)
    patterns={}
    for name,pattern in PATTERNS.items():
        matches=[]
        for cid,rec,mod in rows:
            co=rec['content'];hits=[]
            for field in ('en','ko','additional_details'):
                value=co.get(field,'');value=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False)
                if re.search(pattern,value,re.I):hits.append(field)
            if hits:matches.append({'candidate_id':cid,'record_kind':rec['record_kind'],'module':mod,'matched_fields':hits,'en':co.get('en',''),'ko':co.get('ko','')})
        patterns[name]={'pattern':pattern,'count':len(matches),'matches':matches}
    by_id={cid:(rec,mod) for cid,rec,mod in rows};snapshots=[]
    for cid,(decision,cards,reason) in SELECTED.items():
        rec,mod=by_id[cid]
        snapshots.append({'candidate_id':cid,'source_module':mod,'source_sha256':sha(canonical(rec)),
          'module_sha256':hashes[mod],'record':rec,'bindings':bindings[cid],
          'proposed_disposition':decision,'related_cards':cards,'reason_ko':reason,
          'actual_retrieval_rank':None,'native_adoption':'NOT_RUN','requires_full_contract_review_before_use':True})
    drift=[f for f,h in hashes.items() if sha((ASSETS/f).read_bytes())!=h]
    kinds=dict(collections.Counter(rec['record_kind'] for _,rec,_ in rows))
    result={'schema':'genre-fusion-corpus-lexical-audit/v1','captured_date_kst':'2026-10-22',
      'candidate_count':len(rows),'record_kinds':kinds,'positive_count':len(rows)-kinds.get('diagnostic',0),
      'binding_count':sum(map(len,bindings.values())),'module_count':len(manifest['modules']),
      'manifest_sha256':sha(manifest_raw),'source_module_sha256':hashes,
      'snapshot_changed_during_read':drift,'fields':['content.en','content.ko','content.additional_details'],
      'excluded_fields':['aliases','definition','tags','conditions','obligations','research_metadata','native_proof'],
      'limit':'Lexical evidence only: zero is not semantic absence; counts are not search ranks, eligibility, exposure, adoption, or pixel quality.',
      'patterns':patterns}
    (HERE/'CORPUS-LEXICAL-AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    (HERE/'existing-source-mapping.json').write_text(json.dumps(snapshots,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'candidates':len(rows),'positive':result['positive_count'],'diagnostic':kinds['diagnostic'],'mappings':len(snapshots),'snapshot_drift':drift,'counts':{k:v['count'] for k,v in patterns.items()}},ensure_ascii=False))

if __name__=='__main__':main()
