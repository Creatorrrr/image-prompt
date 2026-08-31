# arm-04-sari-nivi 결과

- 목표 프로필: `nivi_sari_continuous_pleat_pallu_system`
- 후보팩: v6, 최종 `pack_id=e6c37131cd6d6755`
- 프롬프트 감사: PASS (`quality_status=warn`; 205단어가 기본 180단어 권장치는 넘지만 hard-evidence 조정 상한 213단어와 절대 상한 320단어 이내)
- 런타임 요청 감사: PASS (`runtime_prompt_id=7a65c0ff2b8901dc`)
- 이미지 생성: SUCCESS, built-in image generator 1회, 재시도 없음
- 렌더 SHA-256: `6dc3e1880b8251ff7633022ba284ddf9305c5d02e32a048a127d8f1ded6dd730`
- 픽셀 판정: **FAIL** (strict target gates 4/5 PASS, 1/5 FAIL; partial-is-fail)
- 사용자 수용 판단: pending

최초 pre-intent v6 팩은 Nivi 프로필을 hard-route하지 못해 그대로 보존했다. frozen `authorial_core.interpreted_intent`와 byte-equal한 `source_text`를 가진 arm-local `photo-visual-intent/v1`을 추가한 뒤 같은 seed로 재생성했고, 목표 프로필 하나와 5개 게이트만 hard obligation으로 활성화했다. `figura_serpentinata`, `medium_native_glitch` 및 모든 creative 후보는 선택하지 않았다.

## 픽셀 게이트

| 게이트 | 판정 | 근거 요약 |
|---|---|---|
| `vo_nivi_continuous_sari_cloth` | PASS | thumbnail/native에서 허리-앞주름-몸통 대각선-왼쪽 어깨-free pallu가 같은 직물/보더 체계로 이어짐 |
| `vo_nivi_waist_wrap_front_pleats` | PASS | 중앙 앞쪽의 여러 평행 주름이 waist insertion 쪽으로 수렴하며 random gown folds로 보이지 않음 |
| `vo_nivi_torso_crossing_left_pallu` | PASS | 같은 프레임에서 대각선 몸통 횡단과 subject-left shoulder pallu/free end가 명확함 |
| `vo_nivi_support_layers` | FAIL | 별도 검은 blouse는 보이지만 petticoat/underskirt waist 또는 두 번째 support-layer 경계가 native에서도 가려짐 |
| `vo_nivi_not_gown_and_scarf` | PASS | 180×320 thumbnail에서도 stitched gown + detached scarf가 아닌 하나의 Nivi형 드레이프 체계로 읽힘 |

보조 관찰로, 황동 rain gauge는 돌 위에 완전히 지지된 채 손끝이 닿아 있어 locked event의 “mid-lift”는 touch/preparation으로 읽혀 FAIL이다. 참조 사진과의 비교는 장발·얼굴 길이·눈 간격·코·입술·턱의 비생체적 visible-appearance 연속성만 기록했으며 신원 확인으로 취급하지 않았다.

## 핵심 산출물

- `pack/candidate_pack_v6_preintent.json`: hard-route 실패를 보존한 최초 팩
- `postcore/visual_intent.json`: frozen interpreted intent에 묶인 arm-local visual intent
- `pack/candidate_pack_v6.json`: 렌더에 사용한 최종 팩
- `composition/composed_prompt.json`, `composition/exact_prompt.txt`, `composition/audit.json`
- `runtime/render_request.json`, `runtime/render_request_audit.json`
- `generation/attempt-01/render.png`, `generation/attempt-01/thumbnail-320.png`
- `evaluation/pixel_review.json`, `evaluation/pixel_review_audit.json`
- `run_manifest.json`, `runs/image_runs.ndjson`, `provenance.json`
