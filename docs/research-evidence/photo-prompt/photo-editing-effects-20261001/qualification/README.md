# 독립 3개 장면의 최종 원본 픽셀 검증

2026-10-01. 서로의 장면·초안·선택·이미지를 공유하지 않은 3개 에이전트가 seed로 복잡한 컨셉을 선택하고, 첨부한 초상 사진의 보이는 성인 얼굴·헤어 외관을 가이드로 사용했다. 에이전트가 생성 전 동결한 장면·물리 관계·효과 기준을 원본 이미지에서 판정했고, 코디네이터도 원본을 별도로 검토했다. 신원·몸 형태·인격은 참조 범위에 포함하지 않는다.

최종 효과 **5/9 PASS**, 장면 전체 **1/3 PASS**다. 선택한 시각 프로필 성분 **10/14**, 물리 관계 **15/15**, 참조 외관 **3/3** 통과했다. 신규 테스트 대상 source 후보 **10/10**이 실제 팩에 노출되고 선택됐다. 부분 충족은 실패다. 모든 사용자 수용은 대기 상태다.

| 장면 | 효과 | v2 원본 판정 | 판정 근거 |
|---|---|---|---|
| A 항구 수선 부스 | 영상면 미세 필름 입자 | FAIL | 벽 얼룩·문틀 도장 박락이 재질을 따라 나타남. 여러 중간톤 owner에 독립적인 미세 영상면 입자가 확인되지 않음 |
| A | 적주황 밝음-어둠 경계 halation | FAIL | 전구의 따뜻한 rim은 있으나 전구 윤곽 대부분이 밝은 벽 앞에 위치. 지정한 어두운 들보 배경 관계가 부분 충족 |
| A | 완만한 하이라이트 롤오프 | PASS | 뺨·컵 유약·구겨진 종이의 밝은 영역이 점진적으로 변화하며 형태와 질감 유지 |
| B 심야 롤러장 | 직접 플래시 | PASS | 가까운 인물의 정면 반사, 짧은 스케이트 그림자, 어두운 주변광이 함께 관찰됨 |
| B | 선명한 인물과 짧은 움직임 궤적 | PASS | 선명한 주인물에 소매·바퀴의 왼쪽 연속 잔상이 연결되고 고정된 난간·반납대가 선명함 |
| B | 암부의 luma·chroma 노이즈 | PASS | 벽과 재킷 암부의 미세 밝기 변화와 작은 녹색·자홍 점, 밝은 얼굴의 낮은 노이즈가 함께 확인됨. 큰 얼룩은 노이즈 근거에서 제외 |
| C 공연 후 소품 수선실 | 빨간 물체만 남기는 selective color | FAIL | 빨간 문진은 충족하지만 피부·종이·배경에 따뜻한 색 기운이 남아 나머지 무채색 조건 불충족 |
| C | lifted black floor와 암부 세부 | FAIL | 머리·선반의 세부는 보이나 최암부가 깊게 남아 눈에 보이는 회색 하한의 전체 적용 불충족 |
| C | 피부 톤 정리와 미세 질감 유지 | PASS | 뺨의 연속적인 톤 변화와 미세한 모공·불규칙한 피부 표면 유지 |

## A: 비 오는 항구의 수리된 컵 공개

장면 전체 **FAIL**, 효과 **1/3**, 선택 프로필 **0/2**. 오른손은 컵 바닥을 지지하고 왼손은 포장지를 벗긴다. 기다리는 고객의 손과 작업대, 컵의 수선 이음이 함께 보인다.

[프롬프트](arm-a-film-optics/v2/prompt.en.txt) · [negative](arm-a-film-optics/v2/negative.en.txt) · [생성 전 테스트](arm-a-film-optics/v2/test_cases.pre-render.json) · [독립 판정](arm-a-film-optics/v2/report.md) · [팩](arm-a-film-optics/v2/candidate_pack.json)

![A 최종 생성 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/photo-editing-effects-20261001/qualification/arm-a-film-optics/v2/image.native.png)

## B: 심야 롤러장의 마지막 활주

장면 전체 **PASS**, 효과 **3/3**, 선택 프로필 **6/6**. 반납대 옆에서 친구의 카메라를 바라보는 순간에 플래시, 움직임 잔상, 디지털 노이즈를 결합했다. 기술 자격 통과·사용자 판단 대기 상태이며 실제 카메라·ISO·셔터값을 증명하지 않는다.

[프롬프트](arm-b-digital-motion/v2/prompt.txt) · [negative](arm-b-digital-motion/v2/negative.txt) · [생성 전 테스트](arm-b-digital-motion/v2/pre_render_test_case.json) · [독립 판정](arm-b-digital-motion/v2/qualification_report.md) · [팩](arm-b-digital-motion/v2/candidate_pack.json)

![B 최종 생성 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/photo-editing-effects-20261001/qualification/arm-b-digital-motion/v2/generated_original.png)

## C: 공연 후 말린 도면을 펴는 작업

장면 전체 **FAIL**, 효과 **1/3**, 선택 프로필 **4/6**. 오른손은 빨간 문진 위를 누르고 왼손은 도면의 반대쪽을 고정하며 두 팔은 작업대에서 지지된다. 참조 외관과 피부 질감은 유지되지만 전체 무채색과 암부 하한은 부분 충족에 머물렀다.

[프롬프트](arm-c-tonal-skin/v2/prompt_en.txt) · [negative](arm-c-tonal-skin/v2/negative_en.txt) · [생성 전 테스트](arm-c-tonal-skin/v2/pre_render_test_cases.json) · [독립 판정](arm-c-tonal-skin/v2/qualification_report.md) · [팩](arm-c-tonal-skin/v2/candidate_pack.json)

![C 최종 생성 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/photo-editing-effects-20261001/qualification/arm-c-tonal-skin/v2/generated-original.png)

## 보존·집계·검증 범위

최초 v1 원본 3장의 효과 판정은 4/9, 장면 전체 0/3이었다. A/C의 효과 슬롯과 B의 세부 노이즈 후보가 충분히 노출되지 않는 검색 공백을 수정하고, 같은 코어·controls·scene seed로 v2를 재시험했다. native 이미지 모델의 sampling seed는 통제되지 않으므로 4/9→5/9는 관측 결과이며 인과 효과나 성공 빈도가 아니다.

실제 imagegen 호출은 **7회**이며, 성공 원본 **6장**과 출력 안전 차단 **1건**을 모두 보존했다. 차단은 이미지가 없어 픽셀 평가에서 제외했다. 각 버전·에이전트마다 성공 팩을 하나씩 발행했다. B의 별도 snapshot generator 경로 오류는 pack·image를 발행하지 않은 호출이며 원장을 보존했다.

[통합 JSON 원장](coordinator-review.json)에 7개 run ID, 최종 9개 효과 근거, 10개 실제 노출·선택 ID, 모든 프롬프트·원본·핵심 artifact 해시가 있다. [검증 스크립트](../verify_qualification_artifacts.py)의 **169 PASS**는 파일·요청·core·선택·runtime·원본 바이트 무결성이다. 이 스크립트와 deterministic review auditor는 저장한 리뷰를 검사하며 이미지를 자동 판정하지 않는다.

모든 최종 원본은 1237×1272이며 생성 도구가 반환한 파일과 보존 사본의 SHA-256이 같다. 필터·픽셀 수정·사후 이미지 편집을 적용하지 않았다. 효과 검사와 선택 프로필 성분은 겹치므로 독립 시행으로 합산하지 않는다. 3개 조합의 관찰을 전체 후보 133개의 픽셀 자격이나 사용자 수용으로 확대하지 않는다. 남은 네 혼동과 제안된 후속 사례는 [반영 보고서의 계획](../implementation-report.md#결과를-후속-데이터-검증에-반영하는-계획)에 기록했다.
