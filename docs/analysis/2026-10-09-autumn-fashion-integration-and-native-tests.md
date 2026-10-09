# 가을 패션 데이터 반영 및 독립 생성 3건 검증

가을 패션 조사 결과를 후보 데이터와 시각 의미 데이터에 반영하고, 현재 스킬로 독립된 에이전트 3개가 첨부 이미지를 참조해 서로 다른 복잡한 장면을 작성·생성·검토했다. 실제 생성은 각 1회, 총 3회다. 데이터·인덱스 검증은 통과했지만 이미지에서는 일부 관계가 누락되었다. 새 시각 의미 프로필이 실제 검색 결과에 노출되지 않았으므로 신규 112개 프로필의 이미지 인증을 주장하지 않는다.

## 반영한 데이터

조사한 347개 용어를 113개 의미 카드와 연결했다. 129개 구체 후보안 중 기존 계약 17개를 재사용하고 신규 후보 112개, 신규 시각 의미 프로필 112개를 등록했다. 신규 후보는 wardrobe_style 22개, garment_detail 66개, surface_material 20개, footwear 4개다. 프로필에는 선택된 관계를 판정하는 native 기준 115개가 있으며, 필수 구성 요소가 가려지거나 일부만 나타나면 실패한다.

- [신규 후보 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_autumn_fashion_extension.json)
- [신규 시각 의미 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_autumn_fashion.json)
- [등록 명세](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json)
- [347개 용어의 반영 위치와 처리 구분](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/term-runtime-map.json)
- [상세 조사와 출처 42개](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-09-autumn-fashion-visual-semantics-research.md)

각 후보는 착용자, 의복 경계, 속성, 관계 양 끝점을 구체적으로 기술한다. 레이어는 같은 착용자의 겉옷 앞판과 안쪽 칼라의 관계로, 길이는 의복 하단과 신체·허리밴드의 기준점으로 표현했다. 효과 범위에는 의복 종류와 해당 구조·재료 속성을 함께 선언했다. 시스루, 구멍, 절개, 보이는 별도 하의를 분리하고 형제 변형을 한꺼번에 강제하지 않는다. 가족명이나 embedding 유사도만으로 hard 의무가 생기지 않는다.

AFR068의 섬유 기원·함량, AFR092의 맥락 없는 절대 색 인증, AFR113의 정확 DEN은 픽셀 계약으로 승격하지 않았다. 명세와 출처 맵에 남겼으며 기존 색상 후보는 보존했다. 347개 용어의 연결은 모든 용어가 직접 검색 별칭이 되었다는 의미가 아니다.

## 독립성과 실행 조건

원래 사용자 요청의 바이트와 두 active span을 위임 전에 고정했다. 세 에이전트는 다른 에이전트의 프롬프트·이미지·선택을 받지 않고 일반 지식과 첨부 사진, 현재 스킬의 중립 계약만으로 첫 core를 작성했다. 의미 카드와 후보 목록은 core를 고정한 뒤에 조회했다. 2번의 최초 천문대 컨셉은 중복을 발견해 검색·생성 전에 폐기했고, 구체적인 타 사례 내용을 제공하지 않은 중립 다양성 필터로 다시 추첨했다. 폐기한 core와 재추첨 기록도 보존했다.

최종 시드와 컨셉은 다음과 같다.

| 사례 | 시드 | 연결된 복잡한 장면 |
|---|---:|---|
| 1 | 2026100901 | 비 온 뒤 천문대에서 별지도를 젖은 난간과 바람으로부터 보호한다 |
| 2 | 202610090202 | 직물 공방에서 셔틀을 날실 사이로 통과시키며 실 고리를 조절한다 |
| 3 | 2026100903 | 옥상 소극장 리허설에서 풀린 무대 천을 금속 고리에 모은다 |

사용한 [현재 SKILL.md](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md)의 SHA-256은 `9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b`다. 세 실행은 같은 source generation `19523d77b4b4b00ec7eb9ef36833ac8e80c50a0631bfc03babd711b24078d838`과 source fingerprint `b7d450b6529925a0e03786f168c919abd9833a5747e2dd6c97af80747e0bacc6`를 사용했다.

첨부 JPEG SHA-256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다. 원본 파일을 세 native 호출에 실제 첨부했으며 얼굴과 헤어의 보이는 특징을 안내하는 용도로 사용했다. 생성 인물은 성인 가상 인물로 작성했다. 실제 인물의 신원이나 나이를 인증하지 않는다. 관측된 생성 도구는 image_gen이고 이미지 모델명은 반환 정보에 없어 unknown으로 기록했다.

## 원본 이미지 판정

각 에이전트와 부모가 저장된 원본 이미지를 확인했다. 정확한 hard gate와 이번에 채택한 신규 후보 관계의 보조 검사를 구분했다. 다른 이미지의 통과 요소를 합치지 않았다.

| 사례 | 현재 hard 기준 | 이번 신규 후보의 관계 | 의복 보조 목표 | 전체 장면 |
|---|---|---|---|---|
| 천문대 | 8/8 PASS | AFR006 셸 앞판 → 같은 착용자의 플리스 칼라 PASS | 4/5 | 느슨한 종이를 보호하는 전체 행동과 부츠 매듭 끝점 부족 |
| 직물 공방 | 6/8, FAIL | 노출된 두 신규 후보를 호환성 때문에 거절, 신규 채택 0 | 4/5 | 실 고리 접촉과 셔틀 통과가 확인되지 않아 FAIL |
| 옥상 극장 | 6/9, FAIL | AFR027 카디건 하단 → 같은 스커트 허리밴드 FAIL | 3/4 | 봉제선에서 시작하는 주름과 천의 고리 통과 경로가 불명확 |

**이번 변경의 실제 픽셀 검증 범위는 채택한 신규 후보 관계 2개 중 1개 통과다.** 세 사례에서 신규 autumn visual opt-in은 노출·선택되지 않았다. 천문대와 공방은 기존 `vg_face_hands_place_readability_profile`, 극장은 기존 `pr_fabric_tension_fold_attachment`를 선택했다. 이 기존 계약의 판정을 신규 112개 프로필이나 기존 재사용 계약 17개 전체의 인증으로 해석할 수 없다.

천문대에서는 열린 올리브 셸의 두 앞판 사이에 같은 인물의 크림색 플리스 칼라가 분명히 보인다. 코듀로이의 세로 골과 스커트 길이, 부츠와 양말의 순서도 읽힌다. 그러나 지도가 느슨한 종이보다 열린 책·폴리오처럼 보이며 부츠 매듭의 전체 끝점은 충분히 해상되지 않았다. 현재 8개 필수 기준 통과와 전체 authored scene의 완전 구현은 별개다.

![천문대 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/images/arm_1-attempt_1.png)

[실제 native 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/prompts/arm_1-native.en.txt) · [전체 arm 보고서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/autumn-fashion-integration-20261009/arm_1/final_report.json)

공방에서는 코듀로이 겉옷, 니트와 셔츠의 서로 다른 목선·커프스, 가죽 같은 로퍼가 보인다. 먼 손은 요구한 실 고리 대신 베틀 프레임에 놓여 있고 셔틀이 날실 간격을 통과하는 관계도 충분하지 않다. 두 개의 바지 앞주름은 확인되지 않는다. 새로 노출된 셸–플리스와 긴 스웨터–쇼츠 후보는 원래 실내 작업 복장을 바꾸므로 거절했다.

![직물 공방 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/images/arm_2-attempt_1.png)

[실제 native 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/prompts/arm_2-native.en.txt) · [전체 arm 보고서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/autumn-fashion-integration-20261009/arm_2_redraw/final_report.json)

극장에서는 트위드 같은 요철, 리브 칼라·커프스, 와인색 중간 층과 체크 스커트, 무릎 부츠가 나타난다. 카디건의 단추 앞판은 보이지만 카디건 하단과 스커트 허리밴드가 만나는 지점이 가려져 새 관계는 실패다. 천은 고리 근처에 모여 있으나 중앙을 통과하는 연속 경로가 보이지 않는다. 팔꿈치 주름을 식별 가능한 봉제선에 연결하는 증거도 부족하다.

![옥상 극장 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/images/arm_3-attempt_1.png)

[실제 native 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/prompts/arm_3-native.en.txt) · [전체 arm 보고서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/autumn-fashion-integration-20261009/arm_3/final_report.json)

실패한 정확한 gate는 공방의 `embodiment_contact_and_space`, `embodiment_visibility_and_projection`, 극장의 이 두 gate와 `vo_pr_fabric_tension_fold_attachment_2`다. 모든 리뷰 기록의 형식 감사는 유효하지만 픽셀 판정 자체는 위와 같이 FAIL이다. 사용자 판단은 모두 `not_yet_received`, 대표 이미지 승격은 false다.

## 추가 수정의 미실행 이유

두 실패 사례는 닫힌 retry projection을 준비했다. 부모는 enum과 필드 형식 등 중립 wire 도움만 제공했다. 원래 의복·장소와 신규 옷단의 선택적 문구가 공개 보존 맥락에 없어 같은 사례를 유지하는 수정본을 작성할 수 없었다. 기계적 freeze/projection의 통과와 실제 창작 맥락의 충분성을 구분했고, 준비된 child를 이미지 생성에 사용하지 않았다. 기존 payload를 수정 없이 다시 뽑는 reroll도 실행하지 않았다.

[SKILL.md:38](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md:38)은 다음을 명시한다.

> candidate inventories, unselected concepts, previous optional prose, other arms, maintenance examples, and the parent's feature-selection record remain unavailable.

원본 3개 생성은 완료됐으며, 추가 생성 0회다. 실패한 준비와 원래 생성 장부를 모두 보존했다. 생성 장부의 success는 이미지가 반환·저장됐다는 사실이며, 픽셀 FAIL은 별도 리뷰 장부·감사·최종 결과에 남겼다.

## 검증과 반영 상태

- 가을 및 관련 계약 회귀 검사 83건 PASS. 실제 embedding 질의 성공을 주장하지 않으며, 별도 제어 벡터 검사는 유사도가 높아도 hard 의무로 승격되지 않는 경계를 검증했다. 실제 세 조회는 core_bm25f와 keyword 경로다.
- 주 작업 폴더의 가을 검사 13건 PASS, 사전 검증 PASS. 원본으로 인덱스를 재생성했고 동일 텍스트·provider·model·dimensions·recipe가 유지되는 벡터만 재사용했다.
- 독립 작업 폴더의 고정 소스에서 전체 231개 모듈·1,904건을 실행했다. 원래 결과는 실패 이벤트 25개·오류 이벤트 27개로 전체 PASS가 아니다. 30개 이벤트는 가을 변경 전에도 재현됐고, 경로 준비로 인한 import 오류 12개는 수정 후 125건 모두 PASS, 기존 자료 누락 8개 이벤트는 자료 보충 후 4개 테스트 PASS다. 격리 의존성 경로 누락 2개 이벤트는 보충 후 기존 photo baseline 불일치로 재현됐다. 최초 중단·준비 실패·수정 후 재검사 로그도 보존했다. 이후 동시 변경이 들어온 주 작업 폴더 전체 검사로 확대해 주장하지 않는다.
- 변경 전 snapshot의 원래 dirty authored 파일 10개는 적용 시점과 첫 최종 검사에서 동일한 바이트로 보존했다. 이후 전달 직전에는 clothing_structure와 ornament_structure의 동시 변경을 관측해 되돌리지 않고 보존했다. 이번 가을 원본 2개와 스킬·검사 파일은 시험한 원본과 계속 동일하다. 기존 manifest 행과 동시에 들어온 계절 데이터도 유지했다. 스킬·제어·검색 알고리즘 소스는 수정하지 않았다.
- 주 작업 폴더의 전달 직전 검증 런타임 generation은 `b980b1d3f880f799b6a262bed44fc7562efeec0a5ad9841fa47ebb025c3557a8`, revision 71이다. 앞선 합본 검증 revision 69도 증거로 보존했다. 독립 이미지 테스트는 앞서 고정한 동일 generation으로 실행했으므로 이후 동시 작업이 시험 입력을 바꾸지 않았다.
- 커밋·푸시·PR은 요청되지 않아 수행하지 않았다. 원래 hash-bound 파일의 절대 경로를 다시 쓰지 않았으며, 원본 worktree도 보존했다. 중복 runtime snapshot은 원래 worktree에 남기고 주 폴더에는 결과·프롬프트·리뷰·장부를 정확한 바이트로 복사했다.

[전체 검사 분류](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/FULL-SUITE-CLASSIFICATION.json) · [처음 보존한 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/PRIMARY-FINAL-PRESERVATION.json) · [전달 직전 동시 변경 관측](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/PRIMARY-DELIVERY-CONCURRENCY.json) · [기계가 읽는 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/FINAL-RESULTS.json) · [고정된 테스트케이스 3개](/Users/chasoik/Projects/image-prompt/tests/fixtures/photo_prompt/autumn_fashion_three_arm_pixel_cases_v1.jsonl)

## 이번 결과가 요구하는 후속 반영 순서

1. 검색 노출부터 확인한다. 원래 독립 core를 바꾸지 않은 replay에서 신규 profile의 optional discovery가 왜 없었는지 추적하고, 같은 소유자와 관계 양 끝점을 가진 자연어 표현의 발견 범위를 보강한다. 슬롯 채택이나 embedding hit를 자동 hard 의무로 바꾸지 않는다. 성공 기준은 호환되는 신규 opt-in의 노출과 실제 선택 기록이다.
2. 선택된 관계의 관찰 조건을 검증한다. 카디건 하단–허리밴드처럼 가려지기 쉬운 끝점, 봉제선과 주름 시작점, 손–실·천–고리의 연속 접촉을 각각 노출·거리·가림 기준으로 시험한다. 인물·장소를 유지하면서 해당 조건을 만족할 수 있는지 확인한다.
3. retry 보존 맥락을 보완할 별도 작업을 설계한다. 실제 선택된 의복 관계와 핵심 장소·행동 의미를 좁은 property 범위로 보존하면서, 후보 목록·미선택 아이디어·이전 선택적 문구를 새 영감으로 전달하지 않는 계약이 필요하다. 이번 작업에서는 그 제어 코드를 바꾸지 않았다.
4. 기존 리서치의 12개 native 이미지 그룹을 관계별로 확장한다. 검색 노출 → 선택 → 정확한 프롬프트 반영 → 같은 이미지의 모든 native 기준 통과를 순서대로 증명한다. 한 사례의 통과를 전체 347개 용어의 인증으로 넓히지 않으며, 사용자 판단이 오기 전 대표 이미지로 승격하지 않는다.

위 항목은 이번 테스트에서 드러난 후속 계획이며, 이미 수행한 검증으로 표현하지 않는다.
