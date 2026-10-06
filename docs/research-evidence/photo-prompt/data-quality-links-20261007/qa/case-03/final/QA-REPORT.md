Case 03 round-2: 숲속 폭포의 아침 역광 물보라

같은 synthetic 요청, 같은 동결 입력, 같은 seed=303을 새 세대에서 재실행했다. 새 meaning이나 영어 baseline을 작성하지 않았으며 기존 기술 사본도 bytes 그대로 사용했다. 초기 봉인 run과 ISOLATION.json/precore-frozen을 보존했다. API·이미지·네트워크 호출은 없었다.

| 평가 | 상태 | 근거 |
| --- | --- | --- |
| 기술 감사 | PASS | 공식 feature/composed 감사, 실패 0·경고 6 |
| 연결 정확성 | PASS | 원본 edge 2,971개, 실제 조회 93회·왕복 38경로 일치 |
| 최신성 | PASS | 정상 current 성공·손상/wrong root 거부 |
| 의미 보존 | PASS | 초기와 동일한 normalized core 및 영어 baseline |
| 작품 판단 | PARTIAL | 프롬프트 판단만 수행, 픽셀·사용자 수용 미검증 |

pack `498635d44f1e8731`의 receipt generation은 전달된 `db193081d04dba97d754e8809cebfb67a97133c7162a5429da965d53e9c88462`와 정확히 일치한다. source fingerprint는 `6f42582a01533dedf985a68e65391e058bdd1c387954907c421c09143f10e351`이며 관리 report ID는 `5f9c83e3803e85f9f718e1fd237bae2b917a245a716d636f7c48ae416a7ead1f`다. 검색은 `core_bm25f`와 `same_slot_core_focus_and_frozen_observation_bm25f_rrf`의 로컬 lexical 방식이다.

수정 대상 rb_shared_wind_response_candidate와 pr_casual_crop_subject_legibility_candidate는 초기 pack에 있었고 round-2 pack 전체에서 모두 사라졌다. 원본 두 row는 각각 kind=[human], for_any=[human]이다. 같은 환경/no_people 계약으로 실행한 순수 runtime entry_block_reason 진단은 초기 row에 null, 새 row에 explicit_no_people을 반환했다. 이 코드 진단과 실제 pack 노출 사실을 따로 기록했다.

ordinary 후보 수는 64로 같고, 제거된 두 후보 자리는 pe_rotation_arc와 commute_rush_morning이 채웠다. 범위 수정으로 이번 요청의 노출을 제한했으며 전체 관리 corpus에서 원본 후보나 번들 관계를 삭제하지 않았다. 특정 두 후보에 대한 재현 결과를 모든 선택 후보의 의미 호환성 증명으로 일반화하지 않는다.

공식 feature selection 검증은 경고 없이 통과했고 composed 감사는 실패 0, 경고 6이다. 경고는 후보가 대신 충족하지 않은 requester 의미를 독립 문장/assertion으로 보존했다는 기록이다. 최종 후보 및 visual concept 선택은 0개다. 익숙한 풍경 방향이지만 요청과 creativity=1에 맞으며, 다른 직물·실내·초현실·조간대 의미를 채택할 이유가 없다.

숲속 폭포·물보라·아침 햇빛의 후면 조명과 사람 제외를 유지했다. 후면은 조명 속성이다. camera assertion은 unprescribed/open/open, evidence={}이고 nonhuman/no_people=true/explicit_nonsexual=false다. 저장 sensual=1은 유효값 0으로 해소되고 creativity=1/surreal=0을 유지한다. 새 필수 visual obligation은 없으며 핵심 역광 의미는 동결 backlit_spray_effect assertion으로 보존된다.

관리 helper를 재사용하지 않는 별도 oracle은 불변 generation의 raw candidate_ids/candidate_slots/hard_profile_id(s)에서 전체 2,971개 edge를 계산했다. 보고서와 누락·추가 없이 일치했다. 노출 후보 64개와 관련/노출 profile 29개를 실제 CLI로 93회 조회했고 후보→번들→profile 38경로는 역방향에서도 모두 확인됐다. 현재 12개 노출 후보가 연결되고 52개는 정상 미연결이다.

관계 반환은 meaning_support=not_inferred, profile_activation=independent_request_evidence_only를 유지한다. 관리 관계는 전체 corpus의 선언된 참조이며, 요청에서 후보가 제외된 사실과 구분된다. 물보라 후보 water_w024 및 profile water_rel_w024의 미연결을 이름 유사성으로 강제 연결하지 않았다. raw hard_profile_ids 필드를 필수 활성화로 해석하지 않았다.

대표 current query는 cr_candidate_accent_cluster→cr_variant_accent_cluster→cr_accent_cluster 경로를 반환하고 current_verified로 성공했다. links.json을 손상한 scratch 보고서는 report_invalid checksum mismatch로, wrong source root는 report_not_current authority/root mismatch로 거부됐다. 93회 묶음 조회의 freshness는 pinned_report이며 current 검증과 구분했다.

초기 봉인 파일 578개는 모두 원래 해시를 유지한다. round-2 source member 165개, tool code, 복사된 frozen inputs, precore-frozen 12개 파일 및 원본 관리 보고서도 변하지 않았다. scratch 사본만 손상했다.

작품 판단은 프롬프트 범위에서 긍정적이다. 낙수의 충돌과 공중 물방울, 물결의 진행이 원인과 결과를 만들고 밝은 물보라가 그늘진 숲 앞에서 시각적 중심을 가진다. 젖은 바위와 이끼는 보조 맥락으로 절제돼 있다. 실제 이미지가 없어 픽셀에서의 역광·물방울 가독성, 작품 선호, 사용자 수용은 판정하지 않았다.

최종 영어 프롬프트:

A photograph of the spray at a forest waterfall, illuminated by morning sunlight shining from behind the spray. Falling water breaks against the pool, sending a drifting veil of fine droplets into the air. Light catches the airborne droplets, giving their edges a pale gold brightness against deep green woodland shadow. The cascade remains clearly visible beside this luminous cloud, with ripples spreading from its impact across the darker pool. Enclosing trees establish the forest around the water, their trunks and leaves receding into shade. Dark, water-polished rock and small patches of moss sit close to the falling water. A balanced landscape frame gives the illuminated spray the strongest visual presence while retaining its connection to the cascade and pool. The water has crisp, irregular detail, and brightness rolls gently into the surrounding natural shadows.

Prompt SHA-256: `850770cc233e21ec1c8b08d0242825b52c1ce58c4ebcb5d9bbd154eedb9c1999`. Negative는 pack 원문과 동일하며 composed_prompt.json에 기록했다.

주요 실제 명령:

feature-selection-audit (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/skill/scripts/validate_precore_feature_selection.py --catalog /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/skill/precore/visual_feature_catalog.json --request-envelope /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/request_envelope.json --authorial-core /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/authorial_core.runtime.json --embodiment-review /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/embodiment_review.json --selection /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/precore_feature_selection.runtime.json
```

generate-pack (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/skill/scripts/generate_photo_prompt.py --request-envelope-json /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/request_envelope.json --authorial-core-json /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/authorial_core.runtime.json --creative-controls-json /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/creative_controls.json --embodiment-review-json /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/embodiment_review.json --new-author-camera-evidence --seed 303 --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/skill --source-mode local_current --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/runtime --runtime-receipt /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/runtime_receipt.json --output-file /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/candidate_pack.json
```

composed-audit (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/skill/scripts/audit_composed_prompt.py --pack /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/candidate_pack.json --composed /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/composed_prompt.json --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/runtime --runtime-receipt /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/runtime_receipt.json
```

management-build (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/tools/photo_data_maintenance/cli.py build --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/skill --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/runtime --generation db193081d04dba97d754e8809cebfb67a97133c7162a5429da965d53e9c88462 --output /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/management-report
```

query-current-linked-candidate (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/tools/photo_data_maintenance/cli.py query --report /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/management-report --candidate slot:color:cr_candidate_accent_cluster --require-current --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/skill --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/runtime
```

reject-corrupt-report (exit 1):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/tools/photo_data_maintenance/cli.py query --report /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/scratch/report-checksum-corrupt --candidate slot:color:cr_candidate_accent_cluster --require-current --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/skill --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/runtime
```

reject-wrong-source-root (exit 1):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/tools/photo_data_maintenance/cli.py query --report /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/management-report --candidate slot:color:cr_candidate_accent_cluster --require-current --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/scratch/wrong-source-root --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/runtime
```

전체 query의 argv·시각·exit code·출력 경로·해시는 management-query-commands.ndjson 및 evidence/management-queries에 있다. 일반 명령은 commands.ndjson과 evidence/*.result.json에 보존했다.

주요 증거:

- [QA-RESULT.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/QA-RESULT.json)
- [human-scope-regression.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/human-scope-regression.json)
- [human-scope-guard-evidence.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/human-scope-guard-evidence.json)
- [round2-input-verification.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/round2-input-verification.json)
- [management-query-verification.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/management-query-verification.json)
- [links_source_oracle.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/links_source_oracle.json)
- [source-integrity-verification.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/source-integrity-verification.json)
- [composition-review.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/composition-review.json)
- [commands.ndjson](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/commands.ndjson)
- [management-query-commands.ndjson](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/management-query-commands.ndjson)

- [공식 composed 감사](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/evidence/composed-audit.stdout.txt)
- [대표 current query](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/evidence/query-current-linked-candidate.stdout.txt)
- [관리 보고서 요약](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/round-2/run/management-report/SUMMARY.md)
- [초기 봉인 기록](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/INITIAL-ROUND-SEALED.json)
