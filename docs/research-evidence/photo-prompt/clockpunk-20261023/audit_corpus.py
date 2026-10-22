"""Read only the current authored manifest; save a research snapshot in this folder."""
import collections,hashlib,json,pathlib,re
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3];A=ROOT/'skills/photo-prompt-image-generator/assets'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def dump(n,v):(HERE/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def audit():
    manifest=json.loads((A/'photo_candidate_corpus_manifest.json').read_text())
    pats=json.loads((HERE/'corpus-lexical-audit.json').read_text())['patterns']
    candidates={};bindings=collections.defaultdict(list);modules={}
    for mod in manifest['modules']:
        p=A/mod['file'];modules[mod['file']]=sha(p.read_bytes());d=json.loads(p.read_text())
        if mod['kind']=='candidates':
            for cid,c in d['candidates'].items():
                assert cid not in candidates,cid
                candidates[cid]=(mod['file'],c)
        elif mod['kind']=='slot_bindings':
            for bid,b in d['slot_bindings'].items():bindings[b['candidate_id']].append(b)
    matches=[]
    for cid,(module,c) in candidates.items():
        co=c.get('content',{})
        txt=' '.join(str(co.get(k,'')) for k in ['en','ko','phrase_en','phrase_ko','aliases','definition'])
        hit=[k for k,p in pats.items() if re.search(p,txt,re.I)]
        if hit:matches.append(dict(candidate_id=cid,module=module,kind=c['record_kind'],matches=hit,en=co.get('en',''),ko=co.get('ko','')))
    notes={
      'cand_fad77205dfbf5f55bbbc88dbc6257442':('split_fictional_hybrid_from_historical_instruments',['D02','D03','D04'],'영문은 회전 구형 고리를 가진 판타지 포켓워치인데 한국어는 아스트롤라베 시계만 남는다. 평면 아스트롤라베 사실·기계 판타지·천체/시간 마법 embedding을 별도 저술하고 기존 허구를 삭제하지 않는다.'),
      'cand_473bd368aa555c93bc88221265b0b027':('review_bilingual_and_effect_scope',['D03','D04'],'orrery와 혼천의의 번역 불일치를 먼저 해결한다. head-height 행성 관계와 실제 scale owner를 보존하며 body_geometry 효과가 이 물건의 어떤 변화를 뜻하는지 검토한다.'),
      'cand_cb1f8a7534d15030b51f6652cf24295e':('revise_genre_context_after_scope_review',['A01','A02','A03','A04','B01','C07'],'embedding의 without steam을 장르 보편 정의로 유지하지 않는다. 주동력과 조절·전달·프로그램 역할을 분리하고 르네상스/근세는 대표 맥락으로 둔다. 기존 장르 guard를 무단 완화하지 않는다.'),
      'cand_cca5b1e30e485a199e31c82711a5acb9':('split_structure_from_temporal_claim',['A01','A03','A04','B02'],'spring barrel·escapement·cam stack·gear train 구조와 반복 출력/계산 성능을 분리한다. 모든 미세 부품을 한 프레임의 필수 조건으로 강제하지 않는다.'),
      'cand_682fdf57d4745bbe841ab5862eb798f4':('split_structure_from_measurement',['A02','A04','B02','B12'],'박동·하강·캠 타이밍·계산 출력 오차의 동시 검증은 시간·측정이 필요하다. 투명 프레임만으로 오차 판정을 통과시키지 않는다.'),
      'cand_a71c7b7cf4785d238f2e729feeeb4798':('split_repair_cues_from_verified_output',['E05','C01'],'마모/대체 캠 비교, 수리 인계, 반복 출력 검증을 분리한다. 사진 속 부품 교체와 검증 완료 이력은 별개다.'),
      'cand_c6b9cc7879b35ac096badbd0355b25c2':('reuse_after_full_contract_review',['C05'],'정비/노동 장면에 기존의 풍화된 관절 인형·솔·계산대 접촉을 재사용 검토한다. 기존 전체 문구·날씨 흔적을 보존하고 예속을 추가하지 않는다.'),
      'cand_82a2b14d01fb59778be107ad217439d8':('reuse_component',['G01'],'목을 둘러싼 주름 러프라는 기존 부품을 재사용 검토한다. 착용자·더블릿·시대·직업을 이 CID 하나에서 얻을 수 없다.'),
      'cand_00e1c881614a51ed8f149a9a4fc0b416':('reuse_only_if_whole_bundle_fits',['G01'],'러프뿐 아니라 별도 흉갑·천 제복까지 함께 보존하는 조건이다. 러프만 떼어 쓰면 정본 의미를 삭제한다.'),
      'cand_522fa4df296f59db9a1dc282d7ec8f4c':('reuse_component',['A01','C05'],'태엽식 황동 자동인형의 일반 피사체는 재사용 가능성을 검토한다. 보이는 감기 소켓·기어 연결·의식은 별도 근거가 필요하다.')}
    snapshots=[]
    for r in matches:
        cid=r['candidate_id'];module,c=candidates[cid]
        disposition,ids,reason=notes.get(cid,('adjacent_component_only',[], '지정 어휘의 부분 일치다. 소재·표현물·다른 장르의 전체 조건을 보존하고 clockpunk 또는 실제 자동기구로 자동 승격하지 않는다.'))
        snapshots.append(dict(candidate_id=cid,source_module=module,module_sha256=modules[module],record_sha256=sha(canonical(c)),record=c,bindings=bindings[cid],lexical_matches=r['matches'],proposed_disposition=disposition,related_card_ids=ids,reason_ko=reason,actual_retrieval_rank=None,native_adoption='NOT_RUN'))
    dump('existing-source-mapping.json',{'source_manifest_sha256':sha((A/'photo_candidate_corpus_manifest.json').read_bytes()),'module_sha256':modules,'record_count':len(candidates),'record_kinds':dict(collections.Counter(c['record_kind'] for _,c in candidates.values())),'scope':'Read-only lexical and manually reviewed source snapshot; not retrieval ranks, full equivalence search or native qualification.','records':snapshots})
    dump('corpus-lexical-audit.json',{'scope':'Authored modules in current working-tree manifest; lexical inspection only, no retrieval execution','counts':dict(collections.Counter(c['record_kind'] for _,c in candidates.values())),'patterns':pats,'match_counts':dict(collections.Counter(k for r in matches for k in r['matches'])),'matches':matches})
    lines=['# 기존 후보 진단','',f'작업 트리 manifest의 source {len(candidates):,}개 중 지정 어휘에 일치한 {len(matches)}개를 기록했다. 전수 의미 동등성 조사나 검색 성능 측정은 아니다. broad alias의 부분 일치도 포함한다.','', '| CID | 처리 제안 | 연결 카드 | 판단 |','|---|---|---|---|']
    for r in snapshots:lines.append(f"| `{r['candidate_id']}` | {r['proposed_disposition']} | {', '.join(r['related_card_ids']) or '인접 요소'} | {r['reason_ko']} |")
    lines += ['', '원본 전체·조건·효과·binding·record/module hash는 existing-source-mapping.json에 보존했다. 빈 effects와 태그만으로 자격을 추정하지 않는다. 이미 dirty인 module은 이 작업에서 수정하지 않았다.']
    (HERE/'CORPUS-FINDINGS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'records':len(candidates),'matches':len(matches),'manual_decisions':len(notes)},ensure_ascii=False))
if __name__=='__main__':audit()
