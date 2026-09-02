# 하렘 시각 의미 3-arm 독립 렌더 검증

## 결론

- 독립 서브에이전트 3개가 서로 다른 랜덤 복합 컨셉을 맡았다.
- built-in `image_gen` 호출은 arm당 1회, 합계 3회였다. 재시도 0회, fallback 0회, cross-arm 입력 0회다.
- v6 후보팩, composed prompt, 실제 참조 파일을 포함한 runtime request 감사가 3/3 PASS했다.
- strict pixel qualification은 1/3 arm PASS, 13/15 hard gate PASS다. `partial_is_fail` 때문에 전체 render-fidelity 판정은 FAIL이다.
- 서브에이전트 판정과 root의 사후 독립 판정은 15/15 gate에서 일치했다.
- 사용자 미학·외형 유사도·의미 체감 판단은 아직 `unscored`다.

## 랜덤 배정

- 선택 seed: `16147456212566632864`
- 방식: `random.Random(seed).sample` without replacement
- eligible pool: Ottoman household complex, Mughal screened-courtyard household, constructed Orientalist tableau, adult multi-interest ensemble, adult central-target rivalry event
- 선택 순서:
  1. `adult_multi_interest_harem_ensemble_relation`
  2. `orientalist_harem_constructed_tableau`
  3. `mughal_zenana_courtyard_household`

## 결과 요약

| Arm | 복합 컨셉 | Pack / prompt-runtime | 픽셀 게이트 | Strict 판정 |
|---|---|---|---:|---|
| 01 | 비로 열차가 지연된 야간 예술축제 역에서 중심 성인에게 우산·음료/스카프·대체 승차권/노선도 제안이 동시에 들어오는 장면 | `bba9810fcee58e55`; PASS / PASS | 4/5 | FAIL |
| 02 | 현대 미술관 사운드스테이지가 제작 장비를 노출한 채 구성한 19세기 오리엔탈리즘 타블로 | `423c5e691c0e67b1`; PASS / PASS | 5/5 | PASS |
| 03 | 우기 저녁의 무굴 차폐 안뜰 가구에서 직물·음악·놀이 모임을 준비하는 연결된 작업 장면 | `ef7d019728d5feda`; PASS / PASS | 4/5 | FAIL |

Composed prompt는 각각 231, 223, 227 words다. 모두 320-word absolute maximum 안이며, 필수 literal evidence 때문에 기본 180-word 권장치를 넘은 quality warning만 있다.

## Arm 01 — 성인 다중 관심 관계

![arm 01](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-01-multi-interest/final.png)

- PASS: 중심 성인 1명, 구분되는 성인 상대 3명, 서로 다른 세 제안, 단순 단체사진·팬 군중·retinue·2인 삼각형으로의 붕괴 방지.
- FAIL: 중심 인물의 기다리라는 손바닥은 보이지만, 세 상대가 모두 중심만 본다. 상대끼리의 교차 시선, 다른 제안을 보고 멈춘 손, 능동적 자리 조정이 명확하지 않다.
- 최소 차기 수리축: 인원·제안·중심 반응은 그대로 보존하고, 한 상대의 시선을 다른 상대의 물건/손으로 돌리며 다른 상대가 실제로 손을 멈추거나 비켜서는 관계만 강화한다.
- 이미지: `1536×1024`, SHA-256 `6e7bb34f3557601ad4d1e4cc78011ad2de35ba8a903d9c0594928a5744608c70`
- [composed prompt](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-01-multi-interest/composed_prompt.json), [pixel review](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-01-multi-interest/pixel_review.json), [manifest](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-01-multi-interest/run_manifest.json)

## Arm 02 — 구성된 오리엔탈리즘 스튜디오 타블로

![arm 02](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-02-orientalist-tableau/final.png)

- PASS: 성인 출연진 4명, 과잉된 상상 실내 장식, 정적인 reclining/seated/turned 군상, 비대칭 문턱 시점, 노출된 제작 흔적이 한 프레임에서 함께 읽힌다.
- 제작 흔적은 좌측 회색 외벽, 플랫 절단면, 대각 목재 brace, 금속 stand/clamp, cable, warm spill로 픽셀에 직접 남았다.
- 이 노출 구역 때문에 역사 기록이나 평범한 호텔 장식보다 현대 스튜디오에서 구성한 비판적 타블로라는 경계가 보인다.
- 이미지: `1122×1402`, SHA-256 `f28a688f33488b09327fe19f02fa557d5c1dfd9cd0f45efb4916c10844b9d514`
- [composed prompt](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-02-orientalist-tableau/composed_prompt.json), [pixel review](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-02-orientalist-tableau/pixel_review.json), [manifest](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-02-orientalist-tableau/run_manifest.json)

## Arm 03 — 무굴 차폐 안뜰 가구 활동

![arm 03](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-03-mughal-zenana/final.png)

- PASS: lattice screen, 중앙 안뜰, 회랑과 여러 작은 방의 깊이; 성인 5명의 구분된 직물·배치·악기 활동; 이동식 물건과 준비 결과; public ceremony나 costume-only 장면으로의 붕괴 방지.
- FAIL: 전경 arch/lattice는 있지만 카메라에서 안뜰까지 시선이 곧게 열린다. 공공 공간에서 시작해 꺾이거나 비껴난 입구가 직선 시선을 실제로 막는 관계는 보이지 않는다.
- 최소 차기 수리축: 사람·작업·물건·안뜰은 보존하고, 전경에 공공 복도와 불투명 벽을 둔 뒤 화면 밖 측면으로 한 번 꺾여 screen을 통해 안뜰이 드러나는 2-stage entry geometry만 강화한다.
- 이미지: `1402×1122`, SHA-256 `a300a5402ae9ef3071e83bcb2f38c0ce041588d25fb5df38557386dd1e5507ec`
- [composed prompt](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-03-mughal-zenana/composed_prompt.json), [pixel review](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-03-mughal-zenana/pixel_review.json), [manifest](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/arm-03-mughal-zenana/run_manifest.json)

## 참조 이미지 경계

첨부 이미지는 각 arm의 지정 lead/coordinator에만 보이는 성인 외형 단서로 사용했다: 긴 짙은 웨이브 머리, 중앙에 가까운 가르마, 짙은 눈, 자연스러운 메이크업, 전면 얼굴 비율. 생성 이미지에 대한 신원, 동일인, 생체식별, 인종·민족·국적, 보호 특성, 실제 관계, 역사적 신분, 직업, 성격, 매력 판단은 하지 않았다. 모든 생성 인물은 픽셀에서 성인으로 읽혔다. 외형 유사도와 미학적 선호는 사용자가 판단할 별도 층이다.

## Preflight에서 잡힌 사항

- 현재 요청 원문은 이전 조사 키워드 중 랜덤 선택을 위임했을 뿐 세 좁은 profile 이름을 직접 담지 않는다. 따라서 agent-authored core 문구만으로 hard profile을 활성화하지 않는 후보팩 동작이 정상적으로 확인됐다.
- 이미지 호출 0회 상태에서 각 선택 profile을 governing frozen interpreted intent에 묶는 request-scoped `photo-visual-intent/v1`을 추가했다. 첫 no-obligation pack은 진단 시도 이력만 남기고 조합·렌더에 사용하지 않았다.
- Arm 03은 definition-only runtime 정책에 맞춰 금지 runtime label을 같은 의미의 관찰 가능한 정의로 바꿨다. 의미, 인물, 공간, 사건, 외형 우선순위는 바뀌지 않았다.

## 검증과 동시 작업 경계

- Root 재실행: composed audit 3/3 PASS, runtime audit 3/3 PASS.
- Pixel review audit: Arm 01과 03은 각각 정확한 hard gate 1개 실패로 `failed_technical_hard_gates`; Arm 02는 `technical_qualified=true`이지만 사용자 판단이 없어 representative eligibility는 pending이다.
- Harem focused regression: 13/13 PASS.
- 같은 검증 체크포인트에서 dictionary metadata PASS, visual-profile index `278 profiles / 1480 exact terms` PASS, semantic index `7890 entries` PASS였다.
- 이후 같은 shared workspace의 별도 capture/lighting 작업이 전역 registry/index/script를 다시 수정했다. 그 변경 도중 실행한 adjacent regression 40건은 unrelated 신규 lighting evidence field validation 2 FAIL과 transient registry/index mismatch 1 ERROR가 발생했다. 이 보고서는 그 외부 변경을 수정하거나 성공으로 주장하지 않는다.

## 핵심 증거

- [사전 테스트 케이스](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/coordination/test_cases.json)
- [랜덤 배정 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/coordination/random_assignment.json)
- [Pre-pack correction log](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/coordination/prepack_correction_log.json)
- [Root 독립 픽셀 리뷰](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/coordination/root_independent_pixel_review.json)
- [실행 환경 경계](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-harem-three-arm-reference-v1/coordination/run_environment_boundary.json)

