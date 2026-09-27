# Y2K 시각 의미 반영과 독립 이미지 시험

2026-09-27. 이 문서는 앞선 [조사 보고서](report.ko.md)의 제안을 실제 런타임에 반영한 후의 기록이다. 원래 제안 파일의 `planned` / `proposed` 상태는 조사 당시 기록으로 유지한다.

## 실제 반영

- 308개 조사 키워드를 바탕으로 형태와 위치를 정의한 시각 의미 프로필 306개를 추가했다. 완전한 형태 설명이 있어야 해당 프로필의 필수 의무가 활성화된다. Y2K, McBling, Gyaru 같은 계열 이름이나 검색 유사도만으로는 활성화되지 않는다.
- 후보 343개와 선택형 묶음 20개를 기존 확장 로더에 등록했다. 새 후보는 기존 슬롯을 사용하며, 새 전용 라우팅 분기는 추가하지 않았다.
- 후보 중 37개는 의복 소재 또는 소품 위치가 명확한 변형이다. 일반 소재 슬롯의 비인물 제한을 유지하면서 의복 표면 후보 19개를 `garment_detail`에 추가했다. 소품 변형 18개는 작업대, 배경 설치, 목 착용 위치를 구분한다.
- 의복 사이의 길이·부피 대비 4개는 신체 해부학을 바꾸는 `body_geometry` 대신 `appearance`로 관리한다.
- 기기 묶음은 같은 작업면 위의 배열을 명시하고 `setting`이 열려 있어야 선택할 수 있다. 원래 위치 미지정 소품은 범위 미확정 제한을 유지한다.
- 출처, 시대 설명, 역사적 보급률의 한계는 별도 유지보수 기록에 보관한다. 픽셀로 검증할 수 없는 섬유 성능이나 착용자 정체성을 긍정 프롬프트에 넣지 않는다.

실제 파일:

- [후보 확장](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_y2k_extension.json)
- [시각 의미 확장](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_y2k.json)
- [유지보수·출처 결합 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/extension-maintenance/y2k-style-research-20260927.json)
- [반영 수량과 파일 해시](runtime-adoption.json)
- [회귀 검사](/Users/chasoik/Projects/image-prompt/tests/test_photo_y2k_visual_semantics.py)

## 시험 설계

세 서브에이전트는 다른 실험군의 기본 프롬프트·후보팩·이미지를 읽지 않았다. 각자 무작위 seed를 기록하고 중립 관찰 범주만 읽은 뒤 기본 프롬프트와 판정 게이트를 동결했다. 구체적인 장면은 에이전트의 창작 선택이며 사용자의 새로운 정의로 기록하지 않았다.

| 실험군 | 독립 컨셉 | 주요 시각 요소 | seed |
|---|---|---|---|
| A | 플라네타륨의 별 투사기 수동 조정 | 은색 의복, iridescent PVC, 로우라이즈 카고, 곡률 안경, 플랫폼 부츠 | 7278773002676095595 |
| B | 재봉 코너에서 비즈 팔찌 선물 포장 | 분홍 벨루어, 라인스톤, 낮은 플레어 데님, 후프 귀걸이, 은색 가방 | 9854938545815500778 |
| C | 축제 분수 광장의 농구 리바운드와 돌풍 | baby tee, 낮은 나일론 트랙 팬츠, 플랫폼 운동화, 안경, 힙 체인, CD 플레이어 | 7812644412754200727 |

위 seed는 컨셉 선택과 후보팩 생성의 기록용이다. 내장 이미지 생성 도구의 재현 시드를 뜻하지 않는다.

첨부 사진은 보이는 외형 참조로만 사용한다. 생성 대상은 명시적인 성인이다. 사진으로 정체성·실제 나이·국적·직업 등을 추정하지 않는다.

각 실험군은 v6 후보팩 1개와 생성 이미지 1장만 사용한다. 재추첨, 이미지 재생성, CLI 우회는 0회이다. 핵심 요소의 일부만 보이면 통과로 올리지 않는다(`partial_is_fail`). 가림이나 차단으로 판정할 수 없는 항목은 `unscored`로 기록한다. 프롬프트 검사, 런타임 요청 검사, 픽셀 판정은 분리한다.

실험군마다 처음 고정한 열린 차원이 다르다. 특히 B는 복장·행동·배경을 고정했으므로 새 의복 후보를 채택할 수 없다. 실제 후보 노출과 선택 수를 따로 보고하여 단순 등록을 이미지 개선으로 간주하지 않는다.

[공통 시험 프로토콜](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/protocol.json)

## 검증 결과

### 데이터·인덱스

사전 검사, 의미 인덱스 일치 검사, 시각 프로필 인덱스 일치 검사, 장면 표현 감사가 모두 통과했다. 의미 후보 인덱스는 8,972개, 시각 프로필 인덱스는 944개이다. 이전 638개 시각 프로필의 벡터는 그대로 유지했다. 확장 후보·부정문·잘못된 소유자·의복 소재 범위·묶음의 모든 구성원·실제 인덱스 검색을 확인하는 집중 검사 25개도 통과했다.

추가 진단에서는 바꿔 쓴 형태 설명 8개를 944개 프로필의 실제 벡터 인덱스에 질의했다. 솟은 번, 지그재그 가르마, 낮은 허리선, 부츠컷, 나비 헤어 클립, 벨루어, 테리, 폴더폰 모두 해당 신규 프로필을 선택형 후보로 발견했다(8/8). 같은 8개에 대한 가짜 벡터 경계 검사도 통과했으며, 두 경로 모두 새 강제 의미 활성화는 0개였다. 질의 임베딩은 한 번에 문장 1개, 총 8회이며 이미지 생성 횟수에 포함되지 않는다. 이는 좁은 검색 진단으로, 독립 홀드아웃이나 전체 306개 의미의 렌더 자격 검증으로 부르지 않는다. 기록: [검색 진단](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/retrieval-probe.json).

전체 회귀는 86개 모듈의 테스트 메서드 **1,210개를 모두 실행**했다. 1,181개 메서드가 통과했고, 29개 메서드에서 실패 또는 오류가 발생했다. 하위 케이스를 포함한 실패 기록은 53건, 오류 기록은 3건이다. 전체 결과는 **미통과**다. 완료된 동일 원본의 통과 로그 628개를 해시와 케이스 ID로 보존하고, 미완료·실패 케이스 582개를 같은 동결 원본에서 이어 실행했다. 기대값이나 테스트 메서드는 변경하지 않았다. 기록: [집중 검사](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/focused-tests-final.log), [전체 회귀 결과](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/completed-full-suite/full-suite-summary.json), [통과 로그 보존 증거](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/completed-full-suite/prefix-pass-evidence.json).

변경 전 실패 대조는 원래 로더·사전·인덱스를 복사한 별도 원본에서 수행했다. 실패·오류 기록 56건 중 **55건은 같은 케이스 ID, 실패·오류 종류, 예외 종류, 테스트의 실패 행에서 재현**됐다. 나머지 1건은 아래의 선택형 후보 목록 변경이다. 미대조 항목은 0건이다. 마지막 시각 의미 라우팅 대조는 관측된 실패 8개 행을 원래 픽스처에서 그대로 선택하여 동일 테스트의 기존 assertion으로 실행했다. 행 내용과 기대값은 변경하지 않았다. 최종 결합 기록: [실패 대조](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/full-failure-baseline-comparison.json), [시각 의미 대조와 선택 범위](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/baseline-visual-final-comparison.json). 이 비교는 모든 diff 값의 일치나 모든 동작 회귀의 부재를 증명하지 않는다.

추가된 후보 목록과 기존 기대값이 충돌한 한 케이스도 그대로 남겼다. `negative_qipao_collar_only`의 입력은 “A modern bodycon dress with a Mandarin collar”다. 기존 호환 API의 선택형 투영은 변경 전 `[]`, 변경 후 `["y2kr_bodycon"]`을 반환한다. 해당 API는 구성요소 검색 대체 경로를 포함하며, 이 입력에 대한 실제 타입 지정 resolver의 필수·선택형 결과는 전후 모두 `[]`다. 두 경로 모두 치파오 필수 의미가 활성화되지 않았다. 따라서 이 실패를 치파오 오활성화나 실제 후보팩 채택으로 해석하지 않는다. 동결 픽스처의 “선택형 후보도 0개” 기대값은 바꾸지 않았다. 기록: [변경 전](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/bodycon-boundary-before.json), [변경 후](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/bodycon-boundary-after.json).

이미지 생성과 동결 판정이 끝난 뒤 공유 폴더에 별도의 `portrait_composition` 확장이 등록되며 사전·시각 인덱스가 바뀌었다. 실행 중이던 혼합 상태 검사는 중단하고 로그를 보존했다. 다른 작업의 변경을 되돌리지 않고, 원래 준비된 5개 파일의 해시 및 의미 벡터 샤드 16개와 일치하는 복사본에서 전체 회귀를 완료했다. 이 문서의 8,972 / 944 수량과 데이터 검증은 **Y2K 변경만 들어간 동결 원본**에 대한 결과이며, 동시 작업을 포함한 공유 폴더 전체의 최신 상태를 뜻하지 않는다. 기록: [분리 원본](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/qualification-source-manifest.json), [중단 기록](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/interrupted-mixed-source-suite.json).

### 실제 후보 노출·채택

| 실험군 | 공개 후보 목록 행 수 | 신규 Y2K 후보 노출 | 신규 Y2K 후보 채택 | 신규 Y2K 프로필 발견 |
|---|---:|---:|---:|---:|
| A | 101 | 0 | 0 | 0 |
| B | 101 | 1 | 1 | 0 |
| C | 103 | 0 | 0 | 0 |

B가 실제로 채택한 신규 후보는 `slot:lighting:y2kr_retro_flash` 한 개다. 정면 반짝임과 가까운 그림자는 보이지만, 프롬프트가 구체화한 **의자와 후디의 그림자 전체**는 가려져 미확정이다. A·C는 기존 조명·초점·구도 후보만 채택했다. 세 실험군 모두 새 의복 후보가 실제 공개 목록에 노출되지 않았다. A·C의 `appearance`가 열려 있어도 실제 슬롯 목록에 의복·의복 디테일·신발 슬롯이 생기지 않았다는 것이 확인된 한계다. 이를 숨기기 위한 재추첨이나 열린 차원 확대는 하지 않았다.

따라서 새 데이터의 등록·인덱스 검색 가능성은 확인했으나, **새 의복 후보가 이번 실행 경로에서 채택되고 이미지에 남았다는 증거는 없다.** 이미지의 의상 성공은 후보팩 접근 전에 동결한 독립 기본 프롬프트의 실현으로 해석한다.

### 픽셀 판정

에이전트가 직접 원본 해상도 이미지를 확인한 원 판정은 유지했다. 주 에이전트도 같은 이미지를 재검수했다. B는 에이전트 판정서를 읽기 전에 관찰을 기록했으며, A·C 재검수는 원 판정서를 받은 후 진행했으므로 맹검으로 부르지 않는다. 게이트·프롬프트·후보팩·이미지는 변경하지 않았다.

| 실험군 | 독립 에이전트 원 판정 | 주 에이전트 재검수 | 최종 상태와 근거 |
|---|---|---|---|
| A | 통과 7 / 실패 0 / 미확정 1 | 통과 5 / 실패 0 / 미확정 3 | **전체 미확정.** 은색/PVC 소재, 카고·플랫폼, 손과 투사기 접촉, 별 무늬는 보인다. 안경의 랩어라운드 곡률과 벨트 투명도는 확실히 읽기 어렵고, 이에 종속된 전체 액세서리 조합도 미확정이다. 오른쪽 투사기 구가 프레임 밖으로 잘렸다. |
| B | 통과 6 / 실패 0 / 미확정 0 | 통과 6 / 실패 0 / 미확정 0 | **동결한 6개 조건 통과.** 분홍 벨루어·라인스톤·로우라이즈 플레어·후프·은색 가방, 팔찌와 상자에 대한 양손 접촉, 준비물과 발 지지가 보인다. 신규 조명 후보의 세부 그림자 조항은 별도 미확정이다. |
| C | 통과 9 / 실패 1 / 미확정 0 | 통과 7 / 실패 2 / 미확정 1 | **실패.** baby tee·낮은 트랙 팬츠·두 플랫폼 신발·농구공 양손 지지·날리는 종이·분수와 축제 천막은 보인다. CD 플레이어 옆에 인식 가능한 스피커가 보이지 않으며, 이 소품 조건과 스피커 카트가 포함된 바람 사건 조건을 모두 충족하지 못했다. 안경 곡률은 미확정이다. |

최종 보수적 판정은 24개 조건 중 **18개 통과, 2개 실패, 4개 미확정**이다. 전체 컨셉 통과는 B 한 곳이다. C의 두 실패는 동일한 스피커 누락이 서로 다른 동결 조합 조건에 영향을 준 것으로, 독립적인 두 생성 결함을 뜻하지 않는다. 안경의 작은 곡률이나 일부 가려진 표면은 분위기만으로 통과시키지 않았다.

세 실험군의 구성 프롬프트 감사와 실제 도구 요청 감사는 모두 통과했다. 신체·접촉 관련 별도 5개 기술 게이트도 각 실험군에서 통과했지만, 이것이 잘린 장비나 누락된 스피커를 통과로 바꾸지는 않는다. 사용자 외형·미적 판단이 아직 없으므로 대표 성공 사례 등록 자격은 없다.

시험 소모량은 **후보팩 3개, 내장 이미지 생성 3회, 이미지 재시도 0회, CLI 우회 0회**다. 세 코어·기본 프롬프트·동결 게이트와 공통 데이터 준비 해시는 원본과 일치한다.

증거: [전체 결합 기록](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/qualification-summary.json), [A 재검수](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/parent-review-a.json), [B 재검수](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/parent-review-b.json), [C 재검수](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/parent-review-c.json).

### 생성 이미지·프롬프트

각 이미지 옆의 프롬프트 파일과 동결 테스트케이스를 열어 요청과 결과를 직접 비교할 수 있다.

A: [프롬프트](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/arm-a/runtime_prompt.txt) · [테스트케이스](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/arm-a/test_gates.json)

![A 플라네타륨](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/arm-a/generated_image.png)

B: [프롬프트](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/arm-b/runtime_request.json) · [테스트케이스](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/arm-b/test_gates.json)

![B 비즈 팔찌 포장](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/arm-b/generated_image.png)

C: [프롬프트](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/arm-c/runtime_prompt_en.txt) · [테스트케이스](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/arm-c/frozen_test_gates.json)

![C 축제 광장 농구](/Users/chasoik/Projects/image-prompt/outputs/y2k-qualification-20260927/arm-c/generated.png)

## 해석 범위

이 시험은 세 복잡한 컨셉의 키워드 실현을 확인한다. 306개 의미 전체의 픽셀 검증이나 역사적 시대 고증을 증명하지 않는다. 이전 데이터로 생성한 대조군이 없으므로 데이터 반영의 인과적 개선 효과는 측정하지 않는다. 최종 외형·미적 만족 판단은 사용자에게 남아 있다.
