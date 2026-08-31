# 얼굴형 시각 의미 무참조 5-arm 소거 테스트

## 결과

참고 이미지 입력 없이 5개 arm 모두 이미지를 반환했고, 루트 원본 픽셀 판정에서 A·B·C·E가 각각 5/5 hard gate를 통과했다. D는 3/5로 strict FAIL이다. 전체는 23/25 gate PASS, 4/5 arm 완전 PASS이며 요청자 미적 판단은 아직 pending이다.

| Arm | 프로필 | 복합 콘셉트 | 새 pack | 루트 gate | 기술 판정 |
|---|---|---|---|---:|---|
| A | `oval_face_contour_relation` | 달빛 난초 온실의 꽃가루 궤적 복원 | `7e277f814274b5ec` | 5/5 | PASS |
| B | `round_compact_face_relation` | 극지 전파관측소 저잡음 수신기 교정 | `214c6ae5705ca369` | 5/5 | PASS |
| C | `diamond_zygomatic_dominant_relation` | 침수된 바로크 기록보관소 양피지 보존 | `c05efedad7872ee4` | 5/5 | PASS |
| D | `upper_face_to_chin_taper_relation` | 화산유리 키네틱 쿠튀르 아틀리에 | `57183a2bd4e7af33` | 3/5 | FAIL |
| E | `cjk_seed_face_relation` | 새벽 옥상 아날로그 천문 지도 제작 | `6a3d9938d48fe39d` | 5/5 | PASS |

D의 실패 gate는 두 개다. 긴 옆머리가 양쪽 상부 관자 경계를 가려 전체 perimeter가 보이지 않았고, 하안면은 좁은 턱까지 계속 수렴하지 않고 넓고 둥근 턱으로 끝났다. 세로 관계, 상부-하부 폭 위계, 조명·원근 confound control은 통과했다.

## 무참조 입력 증거

- 각 arm은 새 lineage-bound v3 core와 새 candidate-pack v6를 사용했다. 이전 참조 문구가 포함된 pack은 재사용하지 않았다.
- exact runtime request 5개 모두 `references=[]`, `reference_sha256=[]`이며 재감사 결과 `reference_count=0`, failures 0이다.
- built-in imagegen은 arm당 새 이미지 생성 1회만 호출했고 재시도하지 않았다. `referenced_image_paths`와 `num_last_images_to_include`는 호출에서 생략했다.
- composed/runtime prose에서 `attached`, `supplied`, `reference image`, `appearance reference`, `likeness`, `source portrait`, `input image` 의존 문구는 0건이다.
- manifest 5개 모두 candidate pack v6, `image_call_count=1`, `cross_arm_inputs_used=false`, `reference_sha256=[]`이며 저장된 이미지 해시와 일치한다.

## 직전 참고 이미지 실험과 비교

직전 실험은 4개 arm만 픽셀 평가가 가능했고 17/20 gate, 2/4 완전 PASS였다. 이번 실험은 5개 모두 평가되어 23/25 gate, 4/5 완전 PASS다. 동일하게 평가 가능한 A·B·D·E만 비교하면 17/20에서 18/20으로 한 gate 증가했고 완전 PASS는 2/4에서 3/4로 늘었다.

- A: 3/5 → 5/5. 새 샘플에서 머리카락이 얼굴 외곽에서 완전히 물러나 두 실패가 해소됐다.
- B: 5/5 → 5/5. round-compact 관계가 무참조에서도 유지됐다.
- C: 직전 transport error로 unscored → 이번 5/5. 새로 평가 가능해진 결과이며 직접적인 픽셀 delta는 아니다.
- D: 4/5 → 3/5. 관자 머리카락 실패가 유지되고 좁은 턱 수렴 gate도 새로 실패했다.
- E: 5/5 → 5/5. 문화권 label을 runtime에 쓰지 않고도 literal contour가 유지됐다.

이 차이를 참고 이미지 제거의 인과 효과로 단정할 수는 없다. native renderer에는 고정 가능한 대응 render seed가 없고, 각 조건은 arm당 한 장이며, 새 프롬프트는 참조 문구를 제거해 의미적으로 대응하지만 byte-identical하지 않다. 또한 A·B·D는 직전 세로 이미지와 달리 이번에 가로 이미지로 반환되어 출력 종횡비와 얼굴 점유율도 완전히 고정되지 않았다. 확인 가능한 결론은 이 다섯 조건에서 얼굴형 후보팩이 이미지 입력 없이도 4/5 arm에서 전체 픽셀 계약을 작동시켰다는 범위까지다.

## 증거 경계와 파일

- [루트 픽셀 판정](shared/coordinator_pixel_review.json)
- [참조 입력 0건 증거](shared/reference_input_proof.json)
- [참조/무참조 비교](shared/reference_ablation_comparison.json)
- [감사·해시·50개 회귀 테스트 검증](shared/verification.json)
- 각 arm의 `candidate_pack.json`, `composed_prompt.json`, `render_request.json`, `result.png`, `pixel_review.json`, `image_runs.ndjson`, `run_manifest.json`

프롬프트·runtime 감사 PASS는 픽셀 PASS와 별개다. MOE 전용 review auditor가 profile-only pack에서 낸 구조적 schema 결과도 얼굴형 5-gate 판정과 분리했다. 이미지 외관은 의도적으로 참조에 고정되지 않았으며, 동일 인물·닮음·생체 신원 판단은 수행하지 않았다.
