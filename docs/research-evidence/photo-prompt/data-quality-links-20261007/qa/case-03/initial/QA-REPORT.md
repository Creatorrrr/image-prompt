Case 03: 숲속 폭포의 아침 역광 물보라 검증

요청은 coordinator가 사용자 위임에 따라 만든 synthetic 사례다. 실제 인간이 이 문장을 직접 요청했다고 보고하지 않는다. 격리된 case-03만 사용했으며 이미지/API 호출, 다른 사례·기본 checkout·프로젝트 메모리 조회, 원본 skill 수정은 없었다.

| 평가 | 상태 | 근거 |
| --- | --- | --- |
| 기술 감사 | PASS | 공식 feature 검증 및 composed 감사, 실패 0 / 경고 6 |
| 연결 정확성 | PASS | 원본 전체 2,971 edge 일치, 실제 조회 99회, 왕복 44경로 일치 |
| 최신성 | PASS | 정상 current 성공, 손상·잘못된 root·재해시한 사본 거부 |
| 의미 보존 | PASS | 최종 영어 prompt와 동결 baseline의 바이트 동일 |
| 작품 판단 | PARTIAL | 프롬프트 방향은 타당하며 실제 픽셀과 사용자 선호는 미검증 |

pack `5d40a8ad73632c81`는 receipt generation `2135faf8f2451eac73b90c447edbd496545d20d974c158f44ec67d98e9107f2a`와 연결된다. source fingerprint는 `98f7d0ffafa290a2f63583ce8ff41d1c38208bdacc12e1e279458bea81e9d24a`이고 관리 report ID는 `b60c07f041e096fd245115f9ed067e9f7220be6cb7620cab4a5d399cdc898392`다. 검색은 `core_bm25f`와 `same_slot_core_focus_and_frozen_observation_bm25f_rrf`의 로컬 lexical 방식이었다.

원본 동결 파일은 모두 보존했다. feature selection의 catalog_path를 고정 논리 경로로 바꾸고 core의 영어 제외어 people을 원문 noun 사람으로 옮긴 기술 사본을 만들었다. 영어 baseline, source request, anchors, assertions, 선택 관찰 축은 바꾸지 않았다. 수정 전후 해시와 후보 DATA 접근 전 순서는 technical_schema_corrections.json 및 POSTCORE-ACCESS.ndjson에 있다.

동결은 `2026-10-06T16:42:22.040214+00:00`, source-bound 생성 명령 시작은 `2026-10-06T16:50:11.196533+00:00`, 세대 source 관측은 `2026-10-06T16:50:28.216525+00:00`다. 첫 실패 명령은 원본 제외어의 source binding 단계에서 거부되어 DATA acquire에 도달하지 않았다. 공개 generator는 envelope/core/camera/embodiment 검증 뒤에만 DATA를 acquire한다. 이는 기록과 구현 순서의 증거이며 별도의 시스템 I/O 추적이라고 주장하지 않는다.

최종 구성은 후보 0개를 선택하고 baseline을 유지했다. 필수 requester clarification은 적용하고 선택적 시각 의미 및 creative 제안은 이유와 함께 거부했다. 실내 조명·직물·초현실 실패·조간대 노출은 이 숲 장면을 강화하지 않는다. 물보라 원인 관계나 landscape라는 호환 제안도 이미 독립적으로 작성된 의미에 불필요한 기하/계약을 추가하지 않도록 미채택했다.

아침 햇빛의 후면 방향은 waterfall_spray의 illumination.direction 속성이다. 카메라 assertion은 capture_owner=unprescribed, direction_requirement=open, height_requirement=open 및 evidence={}이다. creative_context는 nonhuman/no_people=true/explicit_nonsexual=false다. 저장된 sensual=1은 사람 제외로 유효값 0이고 creativity=1, surreal=0을 유지한다. 사람 제외는 core와 bound creative context 및 pack guard에 남으며, 픽셀에서의 생존은 이번 검증 범위가 아니다.

연결 검증은 관리 graph/query/corpus helper를 재사용하지 않고 불변 generation source의 candidate_ids/candidate_slots/hard_profile_id(s)로 별도 edge와 경로를 만들었다. 노출된 64개 후보와 관계/검색에 노출된 35개 profile을 실제 CLI로 조회했다. 14개 후보가 번들에 연결되고 50개는 미연결이며, source 참조가 없는 미연결은 오류로 바꾸지 않았다.

예를 들어 물보라 후보의 원본 참조는 `[{'file': 'photo_prompt_water_relations_extension.json', 'pointer': '/slots/ambient_particle/1'}]`이고 water_rel_w024 profile의 원본 참조는 `[{'file': 'photo_prompt_visual_obligations_water_relations.json', 'pointer': '/profiles/15'}]`다. 두 실제 query 모두 path_count=0이었다. 같은 뜻/이름은 명시적 bundle reference를 대신하지 않는다.

바람 후보는 원본 photo_prompt_realistic_background_extension.json#/slots/motion/1에서 rbb_breeze_garden 번들 #/visual_semantics/9의 member로 선언된다. 번들의 세 profile 선언은 후보→번들→바람/식생/발 접점 profile의 경로로 정확히 반환된다. 후보 하나가 다른 두 profile까지 전부 표현하는 것은 아니며, query의 meaning_support=not_inferred와 profile_activation=independent_request_evidence_only가 그 한계를 밝힌다. 원본 hard_profile_ids라는 필드 이름을 최종 필수 활성화로 해석하지 않았다.

no_people=true인데도 바람 후보는 eligible로 노출되고 scalp에 붙은 머리카락·jacket hem을 전체 의미에 포함한다. 이 장면에서는 부적합하여 미채택했다. eligible라는 기술 상태와 완전한 의미 호환성을 구분해야 하는 검색 품질 관찰이며, 관리 연결 오류나 필수 활성화 위반으로 확정하지 않는다.

정상 --require-current query는 current_verified로 성공했다. links.json checksum을 깨뜨린 사본은 report_invalid, 잘못된 source root는 report_not_current로 거부됐다. 후보 설명을 바꾸고 entity SHA-256, inventory member SHA-256, report_id를 재계산한 자기 일관 사본은 pinned 조회에서는 읽혔지만 --require-current에서는 verified generation inventory와 다르다는 이유로 거부됐다. 원본 source/code 133개 파일과 원본 보고서 및 동결 산출물의 해시는 모두 그대로다.

프롬프트의 작품 방향은 낙수 충돌→공중 물방울→물결이라는 물리적 흐름과 그늘진 숲 앞의 밝은 물보라라는 중심이 명료하다. 젖은 바위·이끼는 요청에 가까운 절제된 맥락이다. 익숙한 자연 풍경 방향이지만 creativity=1과 요청에 잘 맞는다. 실제 이미지가 없으므로 역광 표현·물방울 가독성·작품 선호·사용자 수용은 판정하지 않았다.

최종 영어 프롬프트:

A photograph of the spray at a forest waterfall, illuminated by morning sunlight shining from behind the spray. Falling water breaks against the pool, sending a drifting veil of fine droplets into the air. Light catches the airborne droplets, giving their edges a pale gold brightness against deep green woodland shadow. The cascade remains clearly visible beside this luminous cloud, with ripples spreading from its impact across the darker pool. Enclosing trees establish the forest around the water, their trunks and leaves receding into shade. Dark, water-polished rock and small patches of moss sit close to the falling water. A balanced landscape frame gives the illuminated spray the strongest visual presence while retaining its connection to the cascade and pool. The water has crisp, irregular detail, and brightness rolls gently into the surrounding natural shadows.

Prompt SHA-256: `850770cc233e21ec1c8b08d0242825b52c1ce58c4ebcb5d9bbd154eedb9c1999`. negative_en은 pack 원문과 동일하며 composed_prompt.json에 기록돼 있다.

주요 실제 명령:

feature-selection-final-core-audit (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/skill/scripts/validate_precore_feature_selection.py --catalog /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/skill/precore/visual_feature_catalog.json --request-envelope /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/request_envelope.json --authorial-core /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/authorial_core.runtime.json --embodiment-review /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/embodiment_review.json --selection /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/precore_feature_selection.runtime.json
```

generate-pack-source-bound (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/skill/scripts/generate_photo_prompt.py --request-envelope-json /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/request_envelope.json --authorial-core-json /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/authorial_core.runtime.json --creative-controls-json /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/creative_controls.json --embodiment-review-json /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/embodiment_review.json --new-author-camera-evidence --seed 303 --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/skill --source-mode local_current --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/runtime --runtime-receipt /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/runtime_receipt.json --output-file /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/candidate_pack.json
```

composed-audit (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/skill/scripts/audit_composed_prompt.py --pack /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/candidate_pack.json --composed /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/composed_prompt.json --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/runtime --runtime-receipt /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/runtime_receipt.json
```

management-build (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/tools/photo_data_maintenance/cli.py build --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/skill --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/runtime --generation 2135faf8f2451eac73b90c447edbd496545d20d974c158f44ec67d98e9107f2a --output /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/management-report
```

query-current-linked-candidate (exit 0):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/tools/photo_data_maintenance/cli.py query --report /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/management-report --candidate slot:motion:rb_shared_wind_response_candidate --require-current --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/skill --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/runtime
```

reject-corrupt-report (exit 1):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/tools/photo_data_maintenance/cli.py query --report /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/scratch/report-checksum-corrupt --candidate slot:motion:rb_shared_wind_response_candidate --require-current --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/skill --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/runtime
```

reject-wrong-source-root (exit 1):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/tools/photo_data_maintenance/cli.py query --report /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/management-report --candidate slot:motion:rb_shared_wind_response_candidate --require-current --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/scratch/wrong-source-root --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/runtime
```

reject-self-consistent-rewrite (exit 1):

```sh
/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/venv/bin/python /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/tools/photo_data_maintenance/cli.py query --report /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/scratch/report-self-consistent-rewrite --candidate slot:motion:rb_shared_wind_response_candidate --require-current --source-root /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/skill --runtime-store /Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/runtime
```

99개 query의 모든 argv·시각·exit code·stdout/stderr 경로와 해시는 management-query-commands.ndjson 및 evidence/management-queries에 있다. 일반 명령은 commands.ndjson과 evidence/*.result.json에 있다. 생성·감사·정상 조회·거부 출력은 각각 원문 그대로 보존했다.

주요 증거:

- [QA-RESULT.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/QA-RESULT.json)
- [PRECORE-FROZEN.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/PRECORE-FROZEN.json)
- [technical_schema_corrections.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/technical_schema_corrections.json)
- [composition-review.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/composition-review.json)
- [management-query-verification.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/management-query-verification.json)
- [links_source_oracle.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/links_source_oracle.json)
- [source-integrity-verification.json](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/source-integrity-verification.json)
- [POSTCORE-ACCESS.ndjson](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/POSTCORE-ACCESS.ndjson)
- [commands.ndjson](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/commands.ndjson)
- [management-query-commands.ndjson](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/management-query-commands.ndjson)

- [공식 composed 감사](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/evidence/composed-audit.stdout.txt)
- [관리 보고서 요약](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/run/management-report/SUMMARY.md)
- [바람 후보·번들 원본](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/runtime/generations/2135faf8f2451eac73b90c447edbd496545d20d974c158f44ec67d98e9107f2a/assets/photo_prompt_realistic_background_extension.json)
- [바람 profile 원본](/Users/chasoik/.cache/image-prompt/photo-data-quality-links-20261007/qa/case-03/runtime/generations/2135faf8f2451eac73b90c447edbd496545d20d974c158f44ec67d98e9107f2a/assets/photo_prompt_visual_obligations_realistic_background.json)
