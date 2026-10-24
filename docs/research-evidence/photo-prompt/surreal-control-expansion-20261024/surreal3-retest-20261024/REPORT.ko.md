# surreal=3 독립 이미지 시험 결과

**독립 서브에이전트 3개가 서로 다른 컨셉으로 각각 1장, 총 3장을 생성했다. 실제 control snapshot은 모두 surreal=3이다. 초현실 관계가 사진의 주된 인상을 이끄는 정성 기준은 3/3 통과했고, 사전 등록한 세부 관계까지 포함하는 엄격한 장면 기준은 1/3 통과했다.**

| 실행 | 컨셉 | 실제 설정 | 초현실 주도성 | 장면별 엄격 판정 | 핵심 관측 |
|---|---|---|---|---|---|
| A | 수직 조수 경계 | surreal=3 | PASS | FAIL | 물벽·손끝·파문은 선명하다. 수평 바다와 수직 물벽이 하나의 수면으로 꺾여 이어지는 90도 경계는 확인되지 않는다. |
| B | 천장에 거꾸로 선 인물 | surreal=3 | PASS | PASS | 양쪽 구두가 벽돌 천장에 닿는다. 정상 방향의 가로등·도로·연석과 거꾸로 선 전신이 함께 보인다. |
| C | 성냥갑에서 이어지는 거대한 기관차 | surreal=3 | PASS | FAIL | 작은 객차와 큰 기관차가 이어지지만, 동일 기관차 몸체의 연속 확대와 양쪽 레일의 상자 입구부터 바닥까지의 연속은 모두 추적되지 않는다. |

‘부분 구현’과 ‘관측 불가’를 완전한 관계의 통과로 계산하지 않았다. 세 원본 모두 coordinator가 직접 확인했으며, 에이전트의 픽셀 판정과 일치했다. 얼굴·짧은 단발·가는 앞머리의 참고 외관은 세 장 모두 읽힌다. 이 판단은 실제 신원·나이·성격을 확정하지 않는다. 사용자 선호와 수용 판단은 아직 받지 않았다.

## 생성 이미지와 프롬프트

### A — 수직 조수 경계

![수직 조수 경계](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-a/results/vertical-tide.png)

[실제 입력 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-a/final_prompt.txt) · [생성 전 테스트케이스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-a/pre_registered_testcases.json) · [픽셀 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-a/pixel_test_results.json) · [결과 요약](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-a/arm_result.json)

거대한 물벽이 화면 대부분을 차지하고 손끝 파문이 인물과 그 환경을 연결한다. 다만 수평 바다에서 꺾여 올라오는 경계가 보이지 않아 ‘하나의 연속 수면’이라는 강한 조건은 partial→FAIL이다. 의도했던 마른 승강장도 실제로는 젖고 반사되어 보인다. 파생 신체·접점 게이트 5개는 통과했지만, 그것이 별도로 등록한 수면 연속성 실패를 덮지는 않는다.

### B — 천장에 거꾸로 선 인물

![천장에 거꾸로 선 인물](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-b/surreal3-b-inverted-arcade.png)

[실제 입력 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-b/final_prompt.txt) · [생성 전 테스트케이스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-b/pre_render_testcases.json) · [픽셀 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-b/surreal3-pixel-test-result.json) · [결과 요약](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-b/result.json)

전신과 양쪽 밑창의 천장 접점이 함께 보이고, 가로등과 도로·건물의 정상 방향이 보조 기준을 제공한다. 전체 사진을 회전한 외관과 구별되며, 사전 장면 기준 4개와 파생 신체·접점 게이트 5개가 모두 통과했다. 실제 중력이나 보이지 않는 지지 장치를 실증하는 판정이 아니라 요청한 시각적 배치의 판정이다.

### C — 성냥갑에서 이어지는 거대한 기관차

![성냥갑에서 이어지는 거대한 기관차](/Users/chasoik/Projects/image-prompt/generated/images/surreal3-fresh-c-matchbox-locomotive-20261024/original.png)

[실제 입력 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-c/final_prompt.txt) · [생성 전 테스트케이스](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-c/testcase_pre_generation.json) · [픽셀 판정·결과](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-c/result.json)

상자를 잡고 받치는 양손과 열차의 상자 입구 통과는 보인다. 그러나 작은 객차들이 큰 기관차 뒤로 연결되는 형태가 되었고, 사전에 요구한 동일 기관차의 보일러·바퀴와 두 선로 전체의 연속 변화는 확보하지 못했다. 장면 기준 4개 중 3개가 통과했고, 정식 신체·접점 게이트에서는 visibility_and_projection이 partial→FAIL이다. 정지 이미지에서 실제 성장·이동·원인·시간 순서를 증명했다고 해석하지 않는다.

## 실행과 검증

- 실제 현재 요청 원문 `surreal 3 으로 테스트해줘.`와 실제 이전 사용자 문맥, 같은 첨부 사진을 각 독립 실행에 고정했다. 초기 저술에는 이전 프롬프트·생성 이미지·후보 pack을 제공하지 않았다. coordinator는 초안 확정 전에 겹친 메커니즘을 다시 정하도록 했고, 최종 장면과 프롬프트는 각 author가 저술했다.
- 이번 실행의 override는 `surreal: 3` 하나다. 나머지는 저장된 sensual=1, fetish=0, creativity=1, adult_appeal_emphasis=auto, viewer_experience=false, reference_edit_mode=off, trend_layer=off를 유지했다. 저장 기본값 파일의 해시는 시작과 종료에 동일하다.
- 현재 로컬 canonical SKILL.md와 설치된 H-F2 데이터 세대를 세 실행 모두 사용했다. [버전 고정 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/surreal-control-expansion-20261024/surreal3-retest-20261024/version-pin.json)에 skill hash와 설치 runtime/data generation이 있다.
- 각 실행에서 compose 감사와 실제 참조 bytes·runtime prompt 감사가 통과했다. built-in image_gen을 정확히 1회씩 호출했으며 추가 생성은 없다. 모든 실행은 `review_record_validated`, native operation complete, attempt 1개로 마감했다.
- 세 실행의 workflow artifact 해시, 첨부 참조 해시, 실제 runtime prompt와 native payload·ledger·manifest의 일치, 이미지 파일 해시를 검증했다. B/C의 도구 반환 원본과 workspace 사본도 byte-identical이다. 세 최종 프롬프트 파일은 실제 runtime prompt와 동일하다.
- 정식 리뷰 기록은 모두 유효하다. 일반 embodiment 기술 판정은 A/B PASS, C FAIL이며, 장면별 엄격 판정은 A/C FAIL·B PASS다. `FINAL-VALIDATION.json`의 pass는 기록과 입력·출력 무결성의 통과를 뜻한다.

## 이번 결과가 말해 주는 범위

surreal=3은 초현실성이 사진의 주된 인상과 방향을 이끈다는 저술 지침이며, 기이한 소품 수나 디테일 수를 뜻하지 않는다. 이번 세 이미지에는 그 주도성이 관측되었다. 동시에 설정 강도가 높아도 정확한 경계·연속성까지 보장되지는 않았고, A와 C에서 해당 한계가 드러났다.

후보 원문은 A 31개/32회 노출, B 31개/32회 노출, C 29개/32회 노출을 검토했다. A/B의 최종 material inspiration은 0개이고 C는 기존 소스의 ‘비교 기준을 같은 깊이에 두는’ 일반 전략 1개를 반영했다. 신규 완성 후보의 원본 전체 native 채택은 세 실행 모두 0개다. 따라서 이번 결과를 신규 완성 후보의 전체 픽셀 자격 통과나 데이터 증설의 인과 효과로 승격하지 않는다.

이전 surreal=0 실행도 명시된 초현실 주제를 보존했다. 이번에는 장면과 프롬프트를 새로 저술했으므로 0→3 변경 효과를 수치로 추정하는 통제 A/B 시험이 아니다. 이전 결과는 보존했고, 같은 장면의 인과 비교를 했다고 보고하지 않는다. 준비 단계의 미사용 retry 경로는 [시험 프로토콜](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/surreal-control-expansion-20261024/surreal3-retest-20261024/TEST-PROTOCOL.ko.md)에 분리해 기록했다.

## 증거 파일

- [coordinator의 직접 픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/surreal-control-expansion-20261024/surreal3-retest-20261024/coordinator-pixel-review.json)
- [최종 무결성 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/surreal-control-expansion-20261024/surreal3-retest-20261024/FINAL-VALIDATION.json)
- [검증 스크립트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/surreal-control-expansion-20261024/surreal3-retest-20261024/validate_fresh_results.py)
- [A manifest](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-a/run_manifest.json) · [B manifest](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-b/run_manifest.json) · [C manifest](/Users/chasoik/Projects/image-prompt/generated/photo-runs/surreal3-fresh-20261024-c/run_manifest.json)
