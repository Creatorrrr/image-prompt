실제 내장 image_gen 호출 1회, 재시도 0회로 이미지를 만들고 원본·축소본·7개 무손실 원본 크롭을 직접 검토했다. 선택된 canonical hard gate는 13개 중 7개 통과, 6개 실패다. 같은 이미지에서 모든 gate를 통과해야 하므로 전체 판정은 실패/부분 달성(0/1)이다. 공식 검토 감사는 기록 유효성 PASS, technical qualification FAIL을 반환했다. 도구 ledger의 success는 이미지가 반환·저장됐다는 뜻이다.

콘셉트는 독립적으로 작성한 네 상황·복장 조합에서 secrets.randbelow(4)를 한 번 호출해 선택한 도심 카페 장면이다. 여름 소나기 뒤 고인 차양 빗물을 어깨 높이 루프로 빼면서 반대 손으로 의자를 기울이는 인과관계를 한 사진에 담았다. 시어서커 셔츠·크로셰 탱크·버뮤다 길이 스코트·샌들을 agent-owned 구성으로 작성했다. 최신 후보·프로필·연구 자료에 접근하기 전에 core, 정확한 현재 요청, 참조 범위, creative controls를 고정했고 다른 arm의 콘텐츠는 보지 않았다. 원래 인물의 얼굴·헤어 가시 참고만 사용했다.

최신 데이터 snapshot은 generation `4d983fa8c19d53c5be8f1269ef5897d9c04ae02a90ed3e3d76eff0e7e47cb756`, fingerprint `3627d26fe90e911e3c3ce6001eed297d98767530a3bbe2b042078ae5af1c8060`로 DATA_READY와 일치한다. pack `86b5e9d5f1312d8e`를 arm 전용 runtime-store에서 한 번 조회했다. 신규 노출 ID는 5개이며, 실제 채택은 `bundle:suf_sf073_v1_bundle`과 `visual-concept:suf_sf069_v1`이다. 기존 `visual-concept:sheer_garment_optical_layering`도 명시적으로 선택했다. 스코트 앞판·쇼츠 구성요소와 같은 허리밴드에서의 앞뒤 겹침을 literal evidence로 최종 프롬프트에 넣었다. `suf_sf073_v1` 연관 프로필은 advisory로 유지하며 canonical gate로 자동 승격하지 않았다. 새 시어서커·크로셰 source ID는 이 bounded pack에 노출되지 않아 채택 증거가 없다. 원래 작성한 시각 묘사가 생성된 것만으로 해당 신규 데이터 적용을 주장하지 않는다. 수영 쇼츠 의미는 노출됐지만 완전한 의미 단위로 검토 후 선택하지 않았다.

| Canonical hard gate | 판정 | 실제 픽셀 근거 |
|---|---|---|
| vo_suf_sf069_v1_1 | FAIL | 양쪽 밑단이 허벅지 중간에 끝나 무릎 가까운 기준 미달 |
| vo_suf_sf069_v1_2 | PASS | 같은 허리밴드·버튼이 두 다리 패널을 연결 |
| vo_suf_sf069_v1_owner | FAIL | 착용자 소유는 읽히나 밑단과 해당 무릎 사이 관계 미달 |
| vo_sheer_textile_first_read | FAIL | 축소본에서 셔츠가 대부분 불투명하게 읽힘 |
| vo_sheer_weave_edge_legibility | PASS | 연속 직물 표면·여밈·소매 가장자리·주름 확인 |
| vo_sheer_transmission_relationship | FAIL | UNOBSERVABLE_NOT_PASS: 흰 직물 띠를 통과한 안쪽 경계 확인 불가 |
| vo_sheer_layer_coherence | FAIL | UNOBSERVABLE_NOT_PASS: 주름 밀도만으로 같은 층의 투과 관계 입증 불가 |
| vo_sheer_not_optical_or_generation_substitute | PASS | 일반 직물 유지; 유리·과노출·누락으로 대체하지 않음 |
| embodiment_body_ownership | PASS | 두 팔·두 다리의 동일 인물 연결 확인 |
| embodiment_joint_chain_and_reach | PASS | 어깨-팔꿈치-손목과 무릎-발목 연결 및 도달 가능 |
| embodiment_support_and_balance | PASS | 두 샌들 접지, 의자 앞발 들림·뒷발 지지 확인 |
| embodiment_contact_and_space | FAIL | 루프/의자 접촉은 정상이나 작성한 인물 기준 좌우 손 배치 반전 |
| embodiment_visibility_and_projection | PASS | 핵심 접촉·샌들·차양 물줄기·의자 발끝 판정 가능 |

신규 스코트 번들의 별도 구성요소 관찰은 3/3 통과했다. 앞판이 실제 쇼츠 앞에 놓이고, 별개의 두 쇼츠 밑단이 앞판 아래/옆에서 보이며, 같은 남색 허리 구성과 착용자에게 연결된다. 이 관찰 3개는 위 canonical hard gate 13개와 분리한다. 스코트 관계의 성공이 버뮤다 무릎 길이 실패를 상쇄하지 않는다.

크로셰 실 연결과 실제 구멍, 열린 셔츠 앞여밈, 느슨한 쇼츠 다리 공간은 읽힌다. 크로셰의 일정한 정사각 격자는 실제로 혼합된 둥근/마름모 패턴이라 미달이다. 시어서커처럼 보이는 오돌토돌한 relief는 보이나 규칙적인 솟은/매끈한 띠를 확정할 수 없어 부분 달성으로 기록했다. 셔츠 사이로 직접 보이는 안쪽 탱크는 흰 연속 직물을 통과한 투과 증거가 아니다. 가림·확인 불가는 UNOBSERVABLE_NOT_PASS다. 원료가 면/리넨인지, 냉감·땀 관리·수영 성능이나 숨은 여밈은 픽셀로 인증하지 않았다.

사진은 차양·루프·물줄기·기울어진 의자·접지된 두 발이 연결되는 설득력 있는 한 순간이며, 인물의 작은 미소와 작업을 향한 시선, 참조를 따른 짧은 어두운 단발과 가는 앞머리가 읽힌다. 전체 사진·인물·복합 콘셉트 품질은 좋지만 세부 충실도 제한이 있다. 물줄기가 의도한 얼굴/레이어보다 먼저 시선을 끌고, 손의 인물 기준 좌우 배치가 반전됐으며, 샌들 아래 바닥은 작성한 마른 문턱과 달리 젖어 있다. 이 미적 관찰은 참조 실물의 신원·나이·체형·성격에 대한 진술이 아니다. sensual=1, fetish=0, surreal=0, creativity=1의 기술적 binding은 유지되며, 사용자 선호 강도의 수용 판정은 받지 않았다.

composed audit는 PASS, quality WARN(좁은 core anchor 네 개가 free description/assertion으로 보존된 uncovered-intent 경고)다. runtime audit는 PASS이며 감사된 runtime prompt와 local reference path를 native payload에 그대로 사용했다. 요청 workflow에는 gpt-image-2와 1024×1536이 기록됐지만 내장 도구의 실제 반환에는 모델명이나 지정 크기 확인이 없다. 실제 원본은 1237×1272 PNG, 2,654,414 bytes, SHA-256 `448bdf21e308cc855604c7aca559eee2c8e2b0dab5b33a0f9cb54066e5a73bb1`다. 반환 tool output_hint의 로컬 원본을 byte-preserving copy하고 원래 파일은 남겼다. 내장 도구만 호출했고 CLI fallback은 없다.

관리 경로는 native-plan → native-started → 실제 내장 호출 1회 → native-result → review-shape → review-audit다. native-result가 independent provenance 인자를 자동 전달하지 않아, 공식 record_image_run.build_independent_manifest helper로 실제 단일 arm ledger row와 기존 검증 binding에서 v2 manifest를 만들었다. 추가 ledger row나 가짜 호출은 만들지 않았다. 직접 호출의 오류에는 공식 capture_image_tool_error.js helper를 쓸 준비를 했으며 실제 호출이 반환됐으므로 오류 캡처는 필요하지 않았다. source/skill/bridge/test 파일은 수정하지 않았다.

최초 review 기록의 사용자 판단 null 자리표시자가 공식 스키마에서 거절됐다. 원본 기록을 보존하고 사용자 판단 metadata만 `pending` / `not_applicable` / `not_yet_received`로 바꿨다. 모든 gate 판정·근거·image hash는 그대로 보존했다. 수정된 공식 감사는 record_valid=true, schema_failures=[], technical_qualification=fail을 확인했다. 사용자 수용은 아직 pending이며, 비교 생성 baseline이 없어 better_than_baseline은 not_applicable이다.

주요 파일: [최종 이미지](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/results/final.png), [최종 영문 프롬프트](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/final-prompt-en.txt), [exact runtime prompt](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/runtime-prompt.exact.txt), [native 검토](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/visual-review.json), [공식 review audit](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/revisions/1c81c0300e004a5da1d81d7c4a1f4856/review_audit.json), [전체 픽셀 관찰](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/pixel-observations.json), [크롭 manifest](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/native-crops/manifest.json), [실제 단일 ledger](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/image_runs.ndjson), [independent manifest](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/run_manifest.json), [case summary](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_a/case-summary.json).
