# 독립 평가 C

첫 native 생성 1회와 독립 평가를 완료했다. 키워드 엄격 판정은 **2/3 통과**, 고정한 전체 컨셉의 all-of 결과는 **실패**다. 생성 도구 성공 및 프롬프트 감사 PASS와 픽셀 자격 판정을 구분한다.

무재추첨 seed는 `15331982403002488971`다. 장소는 복원된 실내 여객선 터미널, 행동은 지도 접기 도중 정지, 소품은 말린 수국의 바구니, 시간은 가을 황혼, 빛은 벽등 2개와 흐린 입구 자연광으로 추첨했다. 원 대화 키워드만 읽고 중립 특징 10개를 선택한 다음 독립 271단어 baseline, embodiment review, required typed assertions 3개와 core를 동결했다. 최종 프롬프트는 347단어다. 다른 arm의 프롬프트·팩·이미지·평가를 입력으로 사용하지 않았다.

| 고정 키워드 | 엄격 판정 | 원본 픽셀 근거 |
| --- | --- | --- |
| seated triangular composition | fail | 머리와 팔꿈치 쪽의 삼각형 외곽은 암시된다. 그러나 한쪽 손이 턱을 지지하고 다른 팔은 지도/무릎 위에 있어, 고정한 두 forearm의 separated-knee support를 명확히 확인할 수 없다. 단순 삼각형 윤곽을 지지 관계의 증명으로 대체하지 않았다. |
| symmetrical architecture with asymmetrical pose | pass | 중앙 창문/출입구, 좌우 아치와 벽등이 대응한다. 수직 기둥과 바닥선은 반듯하고, 손·팔 높이와 고개/어깨 배열은 대칭축에서 벗어난다. 얼굴이 초점 중심이다. |
| still subject and moving surroundings | pass | 주인공 얼굴·지도·석재 벤치·건축은 선명하다. 뒤의 여행자 2명과 짐에 수평 이동 궤적이 붙어 있어 보케나 전체 프레임 흔들림과 구분된다. |

전체 장면에서는 지도 접기 동작과 actor-relative 발 지지가 실패했다. 지도는 펼친 채 한 손으로 들고 다른 손은 턱을 받친다. 정면 사진에서 화면 오른쪽의 subject-left 발은 단 위, 화면 왼쪽의 subject-right 발은 바닥에 있어 동결한 left-floor/right-step와 반대다. 옷과 지도에 가려진 두 forearm의 무릎 접촉을 추정으로 통과 처리하지 않았다. 얼굴/헤어의 보이는 참고, 성인으로 창작한 인물, 수국 바구니, 석재 벤치, 혼합광은 확인됐다. 정확한 가을과 역사적 복원 여부는 한 장의 실내 픽셀로 증명할 수 없는 컨텍스트다.

새 `pc_` 후보는 정상 semantic v6 팩에서 실제로 15개 노출됐다. `slot:composition:pc_pc27_component_4`를 채택해 `Between the lamp-lit arches, the face retains focal priority within the paired architecture`라는 장면 문장과 owner relation evidence를 기록했다. `visual-concept:pc_pc29_owner_relation`를 전체 opt-in 의무와 함께 채택했다. 이에 대한 4개 native/thumbnail 픽셀 게이트는 모두 통과했다. pc09 프로파일은 얼굴-팔꿈치-무릎을 꼭짓점으로 고정하지만 독립 core는 머리-양팔꿈치를 고정했으므로 그 선택지는 거절했다. 미노출 후보를 강제 선택하지 않았다.

`precore_feature_selection`, composed prompt와 exact native request 감사는 통과했다. composed quality의 warn은 core anchor가 후보 자체로 덮이지 않아 독립 문장/typed assertion으로 보존됐다는 8개 정보성 경고다. 픽셀 review 감사는 9개 정확한 게이트, schema failures 0개를 확인하고 `failed_technical_hard_gates`를 반환했다. 실패 게이트는 `embodiment_support_and_balance`, `embodiment_contact_and_space`다. 사용자 직접 선호 판정은 아직 받지 않았다.

입력 참고 사진은 얼굴/헤어의 보이는 외형에만 활용했다. 실제 신원·실제 나이·민족·성격·직업을 추론하지 않았다. `source_request`와 envelope bytes, baseline/core 파일 해시는 동결 후 유지됐다. native call은 감사한 prompt/negative/reference bytes를 사용했고, 최초 원본과 thumb만 보존했으며 추가 생성은 하지 않았다. run manifest v2의 `status: success`는 도구가 이미지 파일을 생성했다는 뜻이며, 픽셀 자격 결과는 `fail`이다.

- 원본 이미지: [attempt-01.png](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/generated_images/attempt-01.png) — 1237 × 1272, SHA `64baf49dfa33a00872f20ae3deac8b90b7f54b9ca9fa8ed7b2e9a4b52e0c0b3a`
- 최종 프롬프트: [final_prompt_en.txt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/final_prompt_en.txt)
- 고정 판정표: [test_case.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/test_case.json)
- 실제 픽셀 평가: [pixel_test_result.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/pixel_test_result.json)
- review 감사: [image_render_review.audit.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/image_render_review.audit.json)
- 노출/채택 증거: [candidate_exposure_adoption.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/candidate_exposure_adoption.json)
- run manifest: [run_manifest.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/run_manifest.json)
- ledger: [image_runs.ndjson](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/image_runs.ndjson)
- source snapshot: [source_snapshot.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/source_snapshot.json)

팩 `51054a89cc275ff7`, prompt `fdd840ec38cad46e`, run `eb8aad56a5f9a763`. Canonical core SHA `16996ea44ed0caa015036ad97ba8e7efdb34ddce54f4d4b2def42ad615c55e9d`, intent-lock SHA `973c347ad247921791bad514aec0143beaa1c5c87a3a5259ee93350a285fac93`, 참고 SHA `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`. 소스 `source-snapshot:872193e003ce286db77b5db9636e1c2c32ac2882c82378d7eab9bbbc94532384`.
