"""Close stage07 only when all public, composition and negative checks finish."""
import hashlib
import json
from pathlib import Path
import subprocess

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
ROOT = Path('/Users/chasoik/.codex/worktrees/slot-retrieval-stage07-integration/image-prompt')
OUT = Path(__file__).resolve().parent


def read(name):
    return json.loads((OUT/name).read_text())


def save(name, value):
    (OUT/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def main():
    rows=read('QUALIFIED-COMPOSITION-VALIDATION.json')
    assert len(rows)==48, len(rows)
    assert all(r['composed_audit']['status']=='pass' and r['runtime_audit']['status']=='pass'
               and r['actual_receipt_verified'] and not r['embodiment_failures'] for r in rows)
    meta=read('QUALIFIED-RUNTIME.json')
    assert {r['generation_id'] for r in rows}=={meta['generation_id']}
    assert {r['source_fingerprint'] for r in rows}=={meta['source_fingerprint']}
    inputs=read('QUALIFIED-COMPOSITION-INPUTS.json')['cases']
    prose_review=read('FINAL-PROSE-REVIEW.json')
    assert prose_review['reviewed_count']==48
    prose_by_case={(r['case'],r['variant']):r for r in prose_review['cases']}
    reviews=[]
    for row in inputs:
        for binding in row['inputs'].values():
            assert hashlib.sha256(Path(binding['path']).read_bytes()).hexdigest()==binding['sha256']
        composed=json.loads(Path(row['inputs']['composed']['path']).read_text())
        actual_review=prose_by_case[(row['case'],row['variant'])]
        assert actual_review['composed_file_sha256']==row['inputs']['composed']['sha256']
        assert actual_review['prompt_sha256']==hashlib.sha256(composed['prompt_en'].encode()).hexdigest()
        pack=json.loads(Path(row['inputs']['pack']['path']).read_text())[0]
        reviews.append(dict(case=row['case'],variant=row['variant'],
            chosen_candidate_ids=composed['chosen_candidate_ids'],
            baseline_prefix_retained=composed['prompt_en'].startswith(pack['authorial_core']['baseline_prompt_en']),
            final_prompt_en=composed['prompt_en'],negative_en=composed['negative_en'],
            full_prompt_sha256=hashlib.sha256(composed['prompt_en'].encode()).hexdigest(),
            embodiment_review=composed['embodiment_review'],
            visual_obligation_evidence=composed.get('visual_obligation_evidence',{}),
            core_binding=composed['authorial_core_binding'],inputs=row['inputs']))
    assert all(r['baseline_prefix_retained'] for r in reviews)
    save('COMPOSITION-REVIEW.json',dict(review_kind='Agent-authored complete final prose rereview; no native pixels or user acceptance.',cases=reviews))
    save('COMPOSITION-SUMMARY.json',dict(cases=48,reject_all=40,adopt_compatible=8,
        composed_pass=48,runtime_pass=48,embodiment_errors=0,verified_receipts=48,
        baseline_prefix_retained=48,golem_zero_optional_choices=True,
        adopted_candidate_references=sum(len(r['chosen_candidate_ids']) for r in rows),
        generation_id=meta['generation_id'],source_fingerprint=meta['source_fingerprint'],
        before_source_amendment=dict(cases=48,composed_pass=47,composed_fail=1,
            failed_case='holdout-10-fantasy-ko',raw_evidence='COMPOSITION-VALIDATION.json'),
        boundary='A runtime-only pass never substitutes for composed audit. All 48 require both audits and current full final prose embodiment review. No generated image or pixel claim.'))
    before=read('PRIMARY-BEFORE.json')
    dirty=[]
    for name, old in before['dirty'].items():
        path=PRIMARY/name
        assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==old['sha256'] and path.stat().st_mode==old['mode'],name
        dirty.append(name)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=PRIMARY,text=True).strip()
    assert head==before['head']
    pointer=Path(before['runtime_pointer_path'])
    assert hashlib.sha256(pointer.read_bytes()).hexdigest()==before['runtime_pointer_sha256']
    staged=subprocess.check_output(['git','diff','--cached','--name-only'],cwd=PRIMARY,text=True).splitlines()
    assert staged==before['staged']==[]
    save('PRESERVATION-FINAL.json',dict(primary_head=head,head_unchanged=True,
        tracked_dirty_paths=len(dirty),tracked_dirty_hashes_and_modes_unchanged=True,
        staged_paths=staged,default_current_byte_identical=True,
        default_current_path=str(pointer),default_current_sha256=before['runtime_pointer_sha256'],
        default_generation=before['runtime_pointer']['generation_id'],
        worktree_root=str(ROOT),worktree_branch='codex/slot-retrieval-stage07-integration',
        committed=False,pulled=False,merged=False,pushed=False,
        existing_untracked_work='No broad cleanup, reset or stash; this run writes its own evidence directory and isolated worktree only. Untracked historical work is not claimed as exhaustively rehashed.'))
    inventory=read('qualified-inventory/inventory.json')
    issues={k:len(inventory[k]) for k in ('duplicate_source_ids','raw_not_loaded','loaded_not_raw','source_labels_changed','lexical_missing','lexical_extra','semantic_missing','semantic_extra')}
    assert not any(issues.values()),issues
    exact=read('exact/exact-recall-summary.json')['totals']
    public=read('PUBLIC-VALIDATION.json')
    tests=read('TEST-VALIDATION.json')
    tamper=read('TAMPER-VALIDATION.json')
    assert tamper['negative_cases']==tamper['rejection_count']==12
    summary=dict(stage=7,status='qualified_scoped_integration_complete',remaining_planned_stages=[],
        base_commit=before['head'],branch='codex/slot-retrieval-stage07-integration',implementation_root=str(ROOT),
        committed=False,pushed=False,runtime=meta,inventory=dict(slots=112,ordinary_candidates=11977,issues=issues),
        exact=exact,exact_reuse=read('RETRIEVAL-INVARIANCE.json')['exact_and_role_probe_reuse'],
        public={k:public[k] for k in ('cases','cli_errors','view_errors','recomputation_errors','candidate_omission_detected','native_positive_hits','native_positive_total','native_adjacent_false_hits','native_adjacent_excluded_total','target_exposure_hits','target_exposure_total','targets_adoption_eligible','private_rank_leaks')},
        composition=read('COMPOSITION-SUMMARY.json'),tests=dict(before_source_fix=136,after_source_fix=78,unique_across_both=180,all_latest_selector_results_pass=True,whole_suite_current=tests['whole_suite_current']),
        negative_tests=dict(rejected=12,total=12,real_filesystem_freshness_before_fix='integrated-focused tests include full runtime freshness module'),
        vectors=dict(semantic_entries=12013,visual_entries=3791,new_embeddings=0,all_vector_bodies_unchanged=True),
        source_amendment=read('SOURCE-REPAIR.json'),primary_preserved=22,embedding_api_calls=0,image_calls=0,
        limitations=['Full exact addressability is not cap success: 232 queries miss 2/4 cap; 41 rank below top24.',
          'Two unsupported subject advisories remain, rejected in final compositions; four empty subject inventories are not meaning passes.',
          '13 required exposures include one ineligible backlight; adoption compatibility is 12/13, not 13/13.',
          'Source-derived probes are maintenance inputs, not independent quality; 92/112 target hit and public/probe union 109/112 slot exposure.',
          'Original 49 diagnostics remain 4 slot cap, 44 global cap, 1 source missing; no cap enlargement or claimed resolution.',
          'Current whole suite not rerun after source-only amendment. Prior stage6 whole suite had 99 matched baseline failure/error records; whole suite is not green.',
          'Prompt/runtime audits and final prose review do not establish generated pixels or user preference.'])
    save('SUMMARY.json',summary)
    report=f'''# 7단계 슬롯 후보 조회 통합 검증

7단계를 완료했다. 기준은 6단계 공개 커밋 `{before['head']}`이다. **현재 등록 source의 적재·index ID 오류 0, 실제 공개 CLI/view/receipt/recomputation 40/40, 최종 composition와 runtime audit 48/48, 변조 차단 12/12**를 확인했다. 이번에 발견한 골렘 evidence 표현 문제는 source의 다섯 anchor 목록에 대체 표현을 하나씩 추가해 수정했고, source 수정 후 관련 검사 78개가 통과했다.

결과는 `codex/slot-retrieval-stage07-integration` worktree와 격리 store에 있다. 현재 요청으로 커밋·pull·main 병합·푸시를 실행하지 않았다. 원본 main HEAD·기존 dirty 22개 파일의 해시와 mode·staged 상태·default CURRENT 바이트는 유지했다. 원래 계획의 남은 단계는 0개이며, 아래 의미·cap·전체 suite 한계는 별도로 남는다.

## 고정 입력과 runtime

- 원래 [FIX-PLAN]({PRIMARY}/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/FIX-PLAN.md)의 7단계와 [실행 계획]({OUT}/PLAN.md)을 적용했다. 개발 8개·holdout 12개 자연어 입력 및 20개 원문 문자 입력, core/controls·64/4/2 cap·판정 기준을 수정 전에 고정했다. holdout은 이미 전 단계에서 결과를 본 사례이며 blind 평가로 주장하지 않는다.
- baseline generation: `{read('runtime-acquisition.json')['generation_id']}`. qualified generation: `{meta['generation_id']}`. source fingerprint: `{meta['source_fingerprint']}`. runtime code binding: `{meta['code_sha256']}`.
- source → 정상 빌더 → dictionary/visual 검사 → publisher 순으로 반영했다. 격리 store와 worktree 기본 store가 같은 qualified generation을 가리킨다. 원본 default generation `{before['runtime_pointer']['generation_id']}`은 바뀌지 않았다. 이전 generation과 실제 receipt도 보존했다.

## 전수 source·검색 결과

| 검사 | 결과 | 판정 범위 |
|---|---:|---|
| 등록 source / loader / lexical / semantic slot ID | 11,977개·112개 슬롯, 누락·중복·extra·label 오류 0 | source 적재 정합성 |
| en/ko/unique 명시 alias exact addressability | 40,380/40,380 | owning-slot 전체, production ranker |
| top1 / cap 2·4 / top24 | 39,346 / 40,148 / 40,339 | cap 밖 232개, top24 밖 41개 |
| source 유래 역할 probe | 222개 중 target 149개, target hit 슬롯 92/112 | source를 읽어 만든 유지보수 입력 |
| 공개 입력에서 반환된 슬롯 / probe 합집합 | 101/112 / 109/112 | 모든 슬롯의 독립 의미 성공을 뜻하지 않음 |
| semantic / visual vector | 12,013 / 3,791개 모두 동일 | 신규 embedding 0 |

exact sweep와 역할 probe는 골렘 보완 전 sealed generation에서 실행했다. 보완 후 전체 slot corpus, code 바이트, BM25F 문서·정책·exact lookup·entry order, semantic/visual text와 vector가 같음을 [invariance 기록]({OUT}/RETRIEVAL-INVARIANCE.json)으로 전수 대조했다. 따라서 그 결과를 재사용했다. 새 generation의 inventory·공개 CLI 40개·receipt·최종 composition는 따로 실행했다. `source hash만 바뀌었으므로 동일하다`고 가정하지 않았다.

114→112 슬롯 차이는 두 제어 슬롯의 역할 정리다. 원래 후보 12,043개와 현재 11,977개의 차이는 retire 28개, 원본 private 미커밋 extension 43개, 신규 typed carrier 5개로 정확히 설명된다. ID 31쌍은 같은 local ID 이동 또는 EN/KO label 동일성을 확인했다(이동 5, ID 변경 26). loader가 설명 없이 잃은 ID는 0이다. private 43개는 원본에 보존했으며 이번 canonical main 범위에 넣지 않았다. [source 대응표]({OUT}/SOURCE-ID-LEDGER.json), [슬롯 역할표]({OUT}/SLOT-ROLE-LEDGER.json)에 개별 근거를 남겼다.

이번 source/public 입력 조합에서 `fetish_styling`, `person_origin`, `procedure_step`의 실제 pack 노출은 관측되지 않았다. 세 슬롯의 source exact 조회는 확인했지만 공개 노출까지 PASS로 승격하지 않았다.

세 surreal 슬롯은 source probe의 concept anchor 없는 입력에서 focus가 비었다. 실제 공개 core에는 concept intent-lock anchor가 있고 세 슬롯 모두 반환·source 재계산됐다. 이 차이를 일반 경로 차단으로 판정하지 않았고, 임의의 concept fallback을 추가하지 않았다.

## 공개 CLI와 최종 composition

| 검사 | 결과 |
|---|---:|
| 공개 CLI / composer view / receipt·source recomputation | 40/40, 오류 0 |
| candidate 삭제 감지 | 40/40 |
| 5개 원문 문자 양성 (EN/KO) | 10/10 |
| 인쇄 문자·명시 제외 오노출 | 0/10 |
| 자연어 기준 필요 후보 노출 | 13/13 |
| 그 후보 중 실제 adoption eligible | 12/13 |
| core·controls·negative 변경 / cap 위반 / private rank 유출 | 0 |
| 후보 전부 거절 composition | 40/40 |
| 의미·owner를 읽고 작성한 채택 composition | 8/8, 선택 참조 9개 |
| composed audit / runtime audit / 최종 prose embodiment | 48/48, 오류 0 |

노출 13개 중 잎의 backlight는 보호된 lighting property와 coarse scope가 겹쳐 `ineligible`이다. 원래 backlight 문장을 보존하고 후보 채택은 거절했다. 이 후보를 억지로 채택하는 변조는 audit가 거절한다. 컵·새·회로·잎·발목 부츠·사리의 채택 8개는 원래 주체·색·접촉·시점·시야를 유지한 완전한 문장으로 작성했다. 나머지 제안은 모두 선택 사항으로 남고, 두 잔여 subject advisory 및 광범위한 의상 family도 거절했다.

모든 composition은 기존 baseline 전체를 prefix로 보존하며, final prompt를 다시 읽은 agent postcomposition embodiment record와 prompt SHA를 남겼다. 실제 matching sealed worker가 receipt를 검증한 source로 전체 composed audit를 실행했고, 별도로 runtime request를 감사했다. runtime PASS를 composed PASS로 상속하지 않았다. [채택·거절 작성 근거]({OUT}/ADOPTION-AUTHORING.json), [최종 문장·검토 기록]({OUT}/COMPOSITION-REVIEW.json), [48개 전체 audit]({OUT}/QUALIFIED-COMPOSITION-VALIDATION.json)을 함께 보관했다.

실제 48개 final prose를 두 묶음으로 읽고 [문장 재검토 판단]({OUT}/FINAL-PROSE-REVIEW.json)을 별도로 기록했다. 원문 문자 입력의 거절 composition은 착용자/인쇄 카드의 소유와 지지를 보존하는 retrieval fixture다. 의상 family의 구체적인 문화 형식이나 렌더된 글자가 검증됐다는 뜻은 아니다.

## 통합 검증 중 수정한 골렘 evidence

보완 전 48개 composition 중 골렘 1개가 실패했다. `후보 전부 거절`만으로 requester가 명시한 constructed-material golem의 기존 hard components를 면제할 수 없었다. 돌로 된 몸·동일 재질 연속·조립 경계·독립 움직임 흔적·완료 작업 근거를 final prose에 명시해야 했다. 기존 evidence anchor는 `clay stone earth or wood` 같은 여러 대안을 합친 긴 문구를 literal로 요구해 자연스러운 돌 전용 표현이 바인딩되지 않았다.

`photo_prompt_visual_obligations.json`의 `golem_constructed_material_agency`에 다섯 대체 표현을 추가했다. 기존 anchor·minimum word count·component·activation·alias·hard gate는 그대로다. ordinary candidate, tokenizer, eligibility, ranking, cap, runtime code를 바꾸지 않았다. 골렘은 현재 shutter에서 계속 정지한다. 열린 action/timing 범위 안에서 이전 움직임의 먼지·발자국 및 기존 성문에서 완료된 통행로 작업의 흔적을 문장으로 보완했고, 새 actor나 운반 물체를 추가하지 않았다. source의 positive 검색 텍스트와 모든 벡터가 같다는 검사도 추가했다.

골렘은 optional 선택 0개 상태로 전체 audit를 통과한다. task 근거를 빼면 실패하며, 현재 정지 상태를 unreviewed runtime 동작으로 바꾸어도 실패한다. 이는 prompt와 선언된 관계의 검증이다. 이전 움직임·재질·인과가 실제 픽셀에서 증명됐다는 뜻은 아니다. [source 수정 기록]({OUT}/SOURCE-REPAIR.json), [골렘 작성 판단]({OUT}/GOLEM-COMPOSITION-AUTHORING.json)을 참조할 수 있다.

## 실패 이력·변조·회귀 검사

source 수정 전 관련 검사 136개가 통과했다. 수정 후 visual obligations/profile retrieval·embodiment·composer view·core retrieval의 기존 74개 및 신규 회귀 4개를 검증했다. 최초 74개 실행에서 CLI 13개가 `source_revision_pending`으로 차단됐다. 격리 qualification store는 완성됐지만 worktree 기본 store의 revision은 미완료였다. 정상 publisher로 완료한 뒤 그 13개 selector가 모두 통과했다. 따라서 수정 후 고유 78개가 최종 통과했고, 수정 전후 전체 고유 selector는 180개다. 실패 로그는 유지했다. 테스트를 완화하거나 원본 CURRENT를 직접 편집하지 않았다.

처음 빌드할 때 visual cache CLI 인자가 dirty 원본 cache를 가리키는 helper 기본값 문제도 드러났다. canonical cache로 다시 실행했고 3,791개 벡터를 모두 재사용했다. 첫 시도는 API key 조회 함수에서 중단돼 embedding HTTP 요청이 0이었다. 이 과정의 pending revision은 builder·validator 성공까지 활성화되지 않았다. semantic/visual metadata는 정상 빌더 산출물이며 JSON/shard를 손으로 맞추지 않았다.

[변조 검증]({OUT}/TAMPER-VALIDATION.json)은 후보 삭제·ID 치환·후보 의미 위조·corpus hash 위조·receipt source/code hash 위조·ineligible lighting 강제 채택·필수 task 제거·stale final review·runtime-only 새 동작·negative byte drift·runtime retrieval hash drift 12개를 모두 차단했다. pack/receipt hash를 같이 위조한 사례도 pinned source의 전체 recomputation에서 거절했다. 수정 전 136개 검사의 runtime freshness module은 실제 임시 파일·process를 사용하는 stale source/alias/cache/receipt/code, 중단 publication 및 지연 publisher도 검사했다. source-only 보완 뒤 이 모듈 전체를 중복 실행하지 않았으며, 새 publication과 receipt 검증은 실제 새 generation에서 수행했다.

## 남은 한계와 전달 상태

- 전 단계의 subject 의미 평가 결과를 같은 현재 후보 ID 집합과 대조했다. 20개 자연어 사례에서 부적합 subject advisory 2개(지도 검토의 world-survey, 골렘의 rover)가 남아 있다. 두 제안은 최종 composition에서 거절했다. subject가 빈 4개 사례를 의미 PASS로 계산하지 않았다. 이 단계가 모든 슬롯의 semantic precision을 독립 평가한 것은 아니다.
- 원래 49개 rank/cap/source 진단은 owning-slot cap 4개·global cap 44개·source missing 1개로 남는다. 이번 단계는 cap을 확대하지 않았고 이 49개를 해결했다고 보고하지 않는다. 전수 exact addressability와 64/4/2 cap 안의 실제 노출은 서로 다른 분모다.
- 현재 source-only 수정 이후 전체 suite는 재실행하지 않았다. 6단계의 넓은 suite는 2,102개 발견·2,018개 실행, failure 30·error 69(수집 오류 12 포함), 99개 실패 기록이 그때의 수정 전 기준선에서 같은 예외로 재현됐다. 이 결과는 과거 증거이며 **현재 전체 suite PASS 또는 신규 전체 실패 0**을 주장하지 않는다.
- 이미지·embedding API 호출은 0이다. runtime request 감사와 최종 prose 검토까지 완료했으며, native pixel·실제 이미지 품질·사용자 선호는 원래 계획에서 별도 범위다.

검토 가능한 수정은 source 1개·derived index manifest 2개·그 manifest가 참조하는 신규 semantic shard 16개·회귀 테스트와 fixture·이 리포트 및 선택한 evidence이다. 활성 shard의 실제 SHA를 확인하고 검토 scope에 명시했다. 중간 store·미활성 shard·대용량 원시 runtime은 local evidence로 보존하며 검토 범위에 섞지 않는다. 모든 단계 결과와 한계는 [SUMMARY]({OUT}/SUMMARY.json), 원본 보존은 [PRESERVATION]({OUT}/PRESERVATION-FINAL.json)에 기록했다. **7단계 변경은 아직 미커밋·미푸시다.**
'''
    (OUT/'REPORT.md').write_text(report)
    analysis=PRIMARY/'docs/analysis/2026-10-12-slot-retrieval-stage07-integration.md'
    analysis.write_text(f'''# 슬롯 후보 조회 7단계 통합 검증

7단계를 완료했다. source/loader/index ID 오류 0, 공개 CLI/view/receipt/recomputation 40/40, 후보 거절·채택 composition와 runtime audit 48/48, 변조 차단 12/12다. 골렘의 기존 hard evidence에 자연스러운 돌·정지 후 흔적 표현 5개를 추가했고, 기존 기준과 검색 텍스트·벡터를 보존했다. source 수정 후 관련 검사 78개가 통과했다.

전체 exact addressability는 40,380/40,380이며 cap 2/4 안에서는 40,148개다. 필요 후보 노출 13/13 중 실제 adoption eligible은 12/13이다. 부적합 subject advisory 2개와 원래 49개 cap/source 진단은 남아 있고, final composition에서 후보를 거절할 수 있다. 전체 suite와 픽셀·사용자 선호 PASS는 주장하지 않는다.

qualified generation: `{meta['generation_id']}`. 원본 main/dirty 22개/default CURRENT는 보존했다. 구현은 `{ROOT}`의 `codex/slot-retrieval-stage07-integration`에 있으며 미커밋·미푸시다. 남은 원래 계획 단계는 0개다.

[전체 리포트]({OUT}/REPORT.md) · [측정 요약]({OUT}/SUMMARY.json) · [source 변경]({OUT}/SOURCE-REPAIR.json) · [최종 문장 검토]({OUT}/COMPOSITION-REVIEW.json) · [실행 테스트]({OUT}/TEST-VALIDATION.json)
''')
    print(json.dumps(dict(stage=7,status='complete',composition_pass=48,primary_preserved=22,committed=False)))


if __name__=='__main__':
    main()
