# 막차 정류장: 이미지 생성 프롬프트 비교

## 공통 입력

원문은 아래 97자이며, 스킬 미사용 3건에서 그대로 이미지 생성 도구에 전달됐다. 세 프롬프트의 SHA-256은 `0a1df9e8f4f85c5f4deef4092c506809e494c2afdc451d1c49458c59ce725244`로 같다.

> 비 오는 밤, 막차가 떠나는 정류장에 혼자 남은 성인이 젖은 서류를 쥔 순간. 지나가던 사람이 급히 찍은 실사 사진. 버스를 놓친 사건과 인물의 낙담이 한 프레임에서 읽히게.

원문은 비·밤, 떠나는 막차, 혼자 남은 성인, 젖은 서류, 놓침과 낙담, 지나가는 행인의 실사 촬영을 지정한다. 구체적인 성별·국가·버스 번호·시간·손·표정 동작·조명·렌즈·화면 배치는 열려 있다.

## 스킬 조건의 기본 프롬프트

세 arm은 독립적으로 영어 기본 프롬프트를 작성했다. 각각 193, 185, 169단어이며, 후보팩을 읽기 전에 이미 다음을 구체화했다.

- 버스가 후미를 보이며 멀어지는 공간 관계, 후미등과 노면 반사. 닫힌 뒷문은 1·3번에서 명시했다.
- 인물의 축 처진 어깨·낮은 시선·서류를 쥔 손과 버스를 보는 반응.
- 구겨지거나 휘고 물이 번지는 서류의 형태.
- 행인의 눈높이와 약간 불완전한 프레임, 가장자리 움직임.

이 구체화는 스킬의 독립 기본 프롬프트 작성 단계에서 이루어졌다. 따라서 **이 부분은 후보팩의 효과로 돌릴 수 없다.**

| arm | 기본 프롬프트 | 최종 본문 | 실제 도구 입력 | 후보팩에서 채택한 요소 |
|---|---|---|---|---|
| 스킬 1 | [193단어](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-1/baseline_prompt_en.txt) | [253단어](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-1/final_prompt_en.txt) | [정확한 문자열](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-1/runtime_prompt_en.txt) | `craft:frame_hierarchy`, `craft:light_provenance` |
| 스킬 2 | [185단어](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-2/baseline_prompt_en.txt) | [247단어](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-2/final_prompt_en.txt) | [정확한 문자열](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-2/runtime_prompt_en.txt) | `slot:light_type:sodium_vapor_streetlight` |
| 스킬 3 | [169단어](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-3/baseline_prompt_en.txt) | [237단어](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-3/final_prompt_en.txt) | [정확한 문자열](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/runs/skill-3/runtime_prompt_en.txt) | `slot:lens:35mm`, `slot:light_type:sodium_vapor_streetlight` |

최종 본문에 이미지 도구용 품질 결함 회피 문장을 붙인 실제 입력은 각각 270, 263, 260단어다. 한글 97자와 영어 단어 수는 동등한 길이 척도가 아니며, 여기서는 지시의 구체화 정도만 보여 준다.

## 후보팩 후 추가된 내용과 결과

- 스킬 1은 인물과 버스 사이의 빈 탑승 공간을 시선 흐름으로 만들고, 정류장 조명과 버스 후미등이 젖은 바닥을 밝히게 했다. [결과](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/images/skill-1.png)에서 떠나는 버스는 분명하지만 젖은 서류와 낙담은 약하다.
- 스킬 2는 정류장 기둥이 전경을 가로지르게 하고 주황색 가로등이 종이·뺨·노면을 함께 비추게 했다. 기본 프롬프트부터 `LAST BUS DEPARTED` 표지 문구를 추가해 사건을 설명했다. [결과](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/images/skill-2.png)는 버스 이탈이 명확하지만 서류가 투명 슬리브에 들어가 젖은 종이가 모호하다.
- 스킬 3은 35mm 시야와 정류장 가로등을 더했다. [결과](/Users/chasoik/Projects/image-prompt/output/last-bus-six-image-comparison-20260923/images/skill-3.png)에는 물방울이 떨어지는 서류가 나오지만, 안내판이 같은 버스 노선을 아직 도착 예정으로 표시해 막차를 놓쳤다는 사건과 충돌한다.

스킬 조건의 프롬프트는 모두 요청의 핵심 요소를 문장으로 보존했다. 이미지 결과에서는 그 요소가 모두 구현되지는 않았다. 특히 세 스킬 결과는 낙담이 약했으며 세 조건 모두 '급히 찍힌' 사진의 우발성이 약했다. 채택된 후보는 조명·렌즈·구도에 집중됐고, 최종 채택 기준으로 동작·표정 후보는 없었다.

후보팩 provenance는 세 번 모두 `requested_selection_mode: semantic`, 실제 `selection_mode: rule`로 기록됐다. 이 3대3 실험은 스킬 전체와 원문 직접 생성의 비교이며, 후보팩만의 효과나 의미 임베딩 선택 경로의 효과를 분리하지 않는다.
