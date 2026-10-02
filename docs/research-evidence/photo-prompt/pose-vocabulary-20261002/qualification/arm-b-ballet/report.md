B의 첫 네이티브 렌더는 원본 보존까지 완료했지만, 엄격한 동결 테스트는 전체 FAIL입니다. 프롬프트·런타임 감사와 물리 점검의 통과는 이 독립 all-of 결과를 바꾸지 않습니다.

난수 시드 `608642126586136787`에서 선택한 컨셉은 식물원 새벽 연습 공간의 성인 발레 인물, 아이보리 긴소매 레오타드와 짧은 차콜 스커트, 뒤쪽 음악 노트와 닫힌 악기 케이스, 푸른 창빛과 따뜻한 실내 램프입니다. 원본 참조는 얼굴과 헤어의 보이는 외관 안내에만 사용했습니다.

| 동결 키워드 | 네이티브 판정 | 원본 근거 | 새 데이터 노출/채택 |
| --- | --- | --- | --- |
| ballet second position | FAIL, 엄격한 간격 변형 | 양쪽 outward toes와 flat heel/sole은 보이지만 지지 폭이 동결한 modest hip-width보다 넓음 | `slot:body_pose:pv_ballet_second_flat` 노출·채택. 이 후보의 일반 flat-second 성분 자체는 모두 PASS |
| shallow demi-plié | FAIL | 양무릎 outward tracking, 골반 중앙, heel contact는 보이지만 무릎 굽힘이 shallow보다 깊음 | `slot:body_pose:pv_ballet_demi_plie_flat` 노출·채택. shallow 성분 FAIL |
| fifth-position arms / bras en couronne | PASS | 양팔 연결, 부드러운 elbow oval, 머리 위 두 손과 fingertip air gap, 낮은 shoulders 관찰 | 새 후보 및 프로필 미노출. 독립 baseline 구현으로만 기록 |

동결 키워드: PASS 1, FAIL 2, UNOBSERVABLE 0. 다섯 embodiment 게이트(body ownership, joint chain/reach, support/balance, contact/space, visibility/projection)는 각 PASS입니다. 실제 힘이나 운동학적 안정성을 측정한 결과는 아닙니다. 배경의 열린 음악 책과 검은 케이스는 관찰되지만 닫힌 케이스를 violin case로 식별할 특징이 부족해 해당 장면 성분은 UNOBSERVABLE입니다. 복잡한 장면 all-of는 FAIL입니다.

V6 pack `53f7462a9cfec002`은 한 번만 생성했습니다. ballet bundle 2개와 associated profile ID는 보였으나 advisory 참조이며 bundle을 선택하지 않았습니다. 발레 opt-in visual concept/profile 3개는 모두 미노출, 선택 0입니다. 팩을 수동 변경하거나 재생성하지 않았습니다.

Composed audit `pass`(필수 의미의 자유 서술 보존 경고 4개), runtime request audit `pass`. Render-review audit에는 schema failure와 failed hard gate가 없고 `technical_qualified=true`입니다. 종료 코드는 1이며 그 이유는 사용자 판단이 미수신이어서 `representative_eligible=false`인 것입니다. 이 감사의 실제 파생 체크리스트는 노출·선택된 발레 profile이 없으므로 5개 embodiment 게이트만 포함합니다; 독립 키워드 FAIL을 대신하지 않습니다.

원본: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/native_result.png`. PNG `1024×1536`, SHA256 `196f5beb543c1ff39ddf1cc3dd0717f062e1b31dcbae6805f3564c9849faf3d8`. 실제 imagegen 호출 1회, 추가 렌더/CLI 전환 0회. 네이티브 원본과 arm 복사본의 SHA는 일치합니다.

동결 core: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/authorial_core.json`
동결 testcase: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/test_case.json`
노출/채택: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/exposure_adoption_trace.json`
원본 픽셀 all-of: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/independent_pixel_review.json`
표준 review 및 감사: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/render_review.json`, `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/render_review_audit.json`
런타임 bytes/hashes: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/native_tool_args.json`, `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/prompt_runtime_hashes.json`
Ledger/manifest: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/image_runs.ndjson`, `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/run_manifest.json`
소스 확인: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/pre_retrieval_source_check.json`, `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/pre_imagegen_source_check.json`

각 시점에서 소스 manifest의 runtime scripts/assets 110개가 일치했고, Phase 1 동결 파일 10개도 최종까지 그대로입니다. 얼굴/헤어의 어두운 bob, 나뉜 fringe, defined brows, dark eyes, pink lips는 보입니다. 신원·생체 동일성·참조 인물의 실제 나이·신체·성격이나 사용자 수용은 주장하지 않습니다.

Metadata 정정: 초기 recorder 인자에서 pack seed를 누락하여 ledger seed가 null이었습니다. 기존 기록을 `metadata-correction-pack-seed-20261002/original/`에 보존한 뒤 같은 generation run_id `3280a1b1eab6217f` 기록을 실제 candidate-pack seed `1312320717690390855`로 재검증해 갱신했습니다. 이것은 pack seed이며 native imagegen 옵션이 아닙니다. Canonical ledger는 1행, 누적 image 호출은 1회로 유지됩니다. Phase 1, pack, prompt/negative, native PNG와 shared source는 변경하지 않았습니다.
