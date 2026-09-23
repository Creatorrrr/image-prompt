# 막차 정류장 이미지: 스킬 3장 / 미사용 3장 비교

## 방법

원문 요청: 비 오는 밤, 막차가 떠나는 정류장에 혼자 남은 성인이 젖은 서류를 쥔 순간. 지나가던 사람이 급히 찍은 실사 사진. 버스를 놓친 사건과 인물의 낙담이 한 프레임에서 읽히게.

- 미사용 3건은 독립 문맥의 서브에이전트가 원문 97자를 변형 없이 image_gen.imagegen에 전달했다. 프롬프트 SHA-256은 세 건 모두 `0a1df9e8f4f85c5f4deef4092c506809e494c2afdc451d1c49458c59ce725244`이다.
- 스킬 3건은 각각 독립 Git worktree에서 동일한 요청 envelope과 동일한 수정 스킬 스냅샷(SHA-256 `fa84622f90eba6d07bb272d296d648505fbe0b89f48b431d2d8fe4e512b9b3f2`)으로 실행했다. 각자 기본 프롬프트와 v6 후보팩 하나를 만든 뒤 최종 프롬프트로 1회 생성했다.
- 각 arm의 이미지 생성 호출은 1회이며 재시도는 없었다. 결과를 A~F로 무작위 이름 붙이고 조건과 프롬프트를 가린 독립 에이전트가 사전 고정한 8개 시각 기준(각 0~2점)으로 픽셀을 검토했다. 점수 공개 후 원본을 다시 확인했다.
- 원문은 나라를 지정하지 않았다. 미사용 이미지는 한국식 정류장과 버스, 스킬 이미지는 영국식 거리·버스로 나타났으나, 국가 선택은 점수에 넣지 않았다.

## 이미지 결과

| 조건 | 이미지 | 점수 /16 | 주된 강점 | 주된 한계 |
|---|---|---:|---|---|
| 미사용 1 | [원본](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/images/direct-1.png) | 13 | 젖은 종이와 낙담한 자세 | 버스 출발 순간과 반응의 연결이 약함 |
| 미사용 2 | [원본](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/images/direct-2.png) | 15 | N73 버스·막차 표지·젖은 종이·낙담이 한 프레임에 읽힘 | 정돈된 서사 구도, 일부 전광판 글자 불안정 |
| 미사용 3 | [원본](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/images/direct-3.png) | 12 | 낙담한 자세와 야간 비 | 젖은 종이·버스 이탈이 모호함 |
| 스킬 1 | [원본](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/images/skill-1.png) | 13 | 버스 물보라·막차 안내·공간적 분리 | 젖은 종이와 낙담이 약함 |
| 스킬 2 | [원본](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/images/skill-2.png) | 13 | 'LAST BUS DEPARTED' 표지와 떠나는 버스 | 종이가 비닐 슬리브 안에 있어 젖음 불명확, 낙담 약함 |
| 스킬 3 | [원본](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/images/skill-3.png) | 12 | 물방울이 떨어지는 서류 | 같은 노선이 'Due'로 표시돼 막차 사건과 충돌, 낙담 약함 |

| 시각 기준(3장 합계 /6) | 미사용 | 스킬 |
|---|---:|---:|
| 비 오는 밤 | 6 | 6 |
| 버스 이탈 | 4 | 5 |
| 혼자 남은 성인 | 6 | 6 |
| 손에 든 젖은 서류 | 5 | 4 |
| 버스를 놓친 사건 | 4 | 5 |
| 낙담 | 6 | 3 |
| 급히 찍은 행인 사진 | 3 | 3 |
| 실사·공간 자연스러움 | 6 | 6 |
| **합계(/48)** | **40** | **38** |

두 조건 모두 비 오는 밤, 혼자 남은 성인, 실사 자연스러움은 세 이미지에서 분명했다. 스킬은 버스 이탈과 놓침의 연결이 각각 1점 높았고, 미사용은 젖은 서류가 1점, 낙담이 3점 높았다. 여섯 이미지 모두 급히 찍힌 행인 사진의 우발성은 부분적(각 1/2점)이었다. 별도 실사 자연스러움 평가는 전부 4/5점이었다.

## 프롬프트 비교

미사용 조건의 [정확한 원문 프롬프트](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/direct_prompt.txt)는 세 번 동일했다. 스킬 조건의 최종 본문은 237~253 영어 단어, 도구에 전달된 문자열은 260~270단어였다. 언어가 다르므로 문자·단어 수를 품질 점수로 비교하지 않았다.

| 조건 | 기본 → 최종 본문 단어 | 실제 채택 후보 | 정확한 도구 입력 |
|---|---:|---|---|
| 스킬 1 | 193 → 253 | `craft:frame_hierarchy, craft:light_provenance` | [프롬프트](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-1/runtime_prompt_en.txt) |
| 스킬 2 | 185 → 247 | `slot:light_type:sodium_vapor_streetlight` | [프롬프트](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-2/runtime_prompt_en.txt) |
| 스킬 3 | 169 → 237 | `slot:lens:35mm, slot:light_type:sodium_vapor_streetlight` | [프롬프트](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-3/runtime_prompt_en.txt) |

스킬의 세 기본 프롬프트에는 이미 버스 후미와 멀어지는 후미등, 젖은 종이의 형태, 시선과 어깨, 버스와 인물 사이 거리, 지나가며 찍는 카메라가 들어 있었다. 닫힌 뒷문은 1·3번 기본 프롬프트에 명시됐다. 최종 단계에서 조명·렌즈·화면의 시선 흐름을 주로 더했다. **동작과 감정의 핵심 구체화는 후보팩 이전에 이루어졌다.** 세 arm에서 동작·표정 후보는 채택되지 않았다.

스킬 2는 'LAST BUS DEPARTED'라는 표지 문구까지 지정해 놓친 사건의 가독성을 높였다. 반면 이미지 속 종이는 투명 슬리브에 보관되어 원문의 '젖은 서류'가 약해졌다. 스킬 3은 최종 프롬프트에 마지막 버스라고 썼지만 결과 안내판이 같은 12번 버스를 'Due'로 표시해 장면의 핵심 주장을 흔든다. 세 프롬프트 모두 구성·런타임 감사는 통과했지만 이 감사는 픽셀의 의미 충실도를 보증하지 않는다.

## 결론과 한계

**이번 3장 대 3장의 블라인드 픽셀 비교에서는 스킬의 시각적 우위가 확인되지 않았다.** 점수는 미사용 40/48, 스킬 38/48이며 범위가 크게 겹친다. 미사용 2가 15/16으로 가장 높은 단일 결과였다. 스킬은 사건의 공간 관계를 프롬프트에 더 분명히 표현했지만, 생성된 사진의 낙담과 서류의 젖음에서는 그 이점이 나타나지 않았다.

여섯 장은 통계적 결론을 내기에는 적고 이미지 생성에는 제어된 seed가 없다. 미사용은 동일 프롬프트 3회, 스킬은 독립 작성된 프롬프트 3개를 1회씩 사용했으므로 프롬프트 작성 변동성도 처리 조건에 포함된다. 후보팩 자체의 효과는 스킬 기본 프롬프트만 사용하는 제3 조건이 없어 분리할 수 없다. 세 팩은 `requested_selection_mode: semantic`이지만 실제 `selection_mode: rule`로 기록되어, 의미 임베딩 선택 경로 전체를 검증한 결과도 아니다. 블라인드 점수는 에이전트의 픽셀 판독이며 요청자의 직접 수락 판단은 아직 없다.

[블라인드 원본 평가](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/blind/blind_review.json) · [점수와 해시](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/comparison_results.json) · [실험 환경](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/environments.json)
