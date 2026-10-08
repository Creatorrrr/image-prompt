# 120개 흙·땅 연구 카드

모든 항목은 연구·저작 제안이다. 정의의 출처 상태와 시각 구현의 검증 상태는 별개다.
각 card의 구성은 전체 term의 공통 외형이 아니라 선택 가능한 구체적 realization이다.

## E001 · 흙·땅·지반의 관찰 단위

물질·지표 공간·지지 기반은 서로 다른 관찰 단위다.

원 대화 범주: 1 · 표현 방식: context · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| ground | a bounded exposed ground patch beside the path |
| soil | loose particles resting on that ground patch |

관계: soil → rests_on → ground

혼동 경계: 땅이라는 말만으로 갈색 토양·수직 절개·지하 공동을 강제하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.

## E002 · 구분되는 모래 입자

USDA에서 모래는 0.05–2 mm 입경 범위다.

원 대화 범주: 2, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| sand | individual coarse grains resolved on one sand patch |
| sand | small shadows between adjacent grains on that patch |
| scale_reference | a scale reference in the same focal plane |

관계: scale_reference → scales → sand

혼동 경계: 멀리서 보이는 점무늬는 개별 입자 증거가 아니다. 모래를 석영과 동일시하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S02 NRCS Soil Texture and Structure Guide](https://www.nrcs.usda.gov/sites/default/files/2022-11/Texture%20and%20Structure%20-%20Soil%20Health%20Guide_0.pdf), [S35 NRCS Rangeland Ecohydrology Soil Particle Size](https://directives.nrcs.usda.gov/sites/default/files2/1712930384/33921.pdf)

출처 확인 범위: S02 [pdf_structure_verified] 입경표·토성 삼각형·구조 도식. 텍스트 추출이 빈약하여 도식 판독은 별도 검증한다.; S35 [primary_search_excerpt] USDA 입경 수치와 육안으로 구분 가능한 입경의 한계.

## E003 · 실트·점토 입경과 토성

실트 0.002–0.05 mm와 점토 0.002 mm 미만은 입경 분류다.

원 대화 범주: 2, 5 · 표현 방식: micro · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| sample | a labelled fine sediment sample under magnification |
| scale_bar | a calibrated scale bar beside the resolved sample |
| sample | a separate bulk sample outside the magnified view |

관계: scale_bar → scales → sample

혼동 경계: 일반 풍경 사진에서 점토 입자의 판상 결정이나 정확한 토성 비율을 주장하지 않는다. 양토는 1:1:1 혼합이 아니다.

프레이밍·배율·채택 조건: Require a requested microscope/magnified view and verified sample identity. No ordinary-photo hard profile.

출처: [S02 NRCS Soil Texture and Structure Guide](https://www.nrcs.usda.gov/sites/default/files/2022-11/Texture%20and%20Structure%20-%20Soil%20Health%20Guide_0.pdf), [S35 NRCS Rangeland Ecohydrology Soil Particle Size](https://directives.nrcs.usda.gov/sites/default/files2/1712930384/33921.pdf)

출처 확인 범위: S02 [pdf_structure_verified] 입경표·토성 삼각형·구조 도식. 텍스트 추출이 빈약하여 도식 판독은 별도 검증한다.; S35 [primary_search_excerpt] USDA 입경 수치와 육안으로 구분 가능한 입경의 한계.

## E004 · 둥근 자갈·각진 쇄석·잔돌

입경·원마도·광물 종류는 별개의 속성이다.

원 대화 범주: 2, 17, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| gravel | rounded pebbles embedded in a finer sediment bed |
| gravel | irregular grain sizes with visible pebble edges |
| matrix | fine sediment occupying gaps around the pebbles |

관계: matrix → surrounds → gravel

혼동 경계: 갈색 흙만으로 자갈 혼합을 증명하지 않는다. 각진 쇄석 변형은 별도 후보로 분리한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S18 British Geological Survey Rocks and Minerals](https://www.bgs.ac.uk/discovering-geology/rocks-and-minerals/)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S18 [direct_page_scope] 암석/광물/풍화 연구의 출처 입구. 개별 암종·자원 수치의 전수 검증은 아니다.

## E005 · 입단과 경운 흙덩이

입단은 구조 단위이며 경운으로 생긴 흙덩이와 동일하지 않다.

원 대화 범주: 2, 5, 29 · 표현 방식: macro · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| aggregate | small crumb aggregates on a broken soil face |
| aggregate | irregular natural boundaries around each crumb |
| soil_face | interaggregate gaps continuing into the exposed soil face |

관계: aggregate → part_of → soil_face

혼동 경계: 돌·팝콘·구슬로 대체하지 않는다. 흙덩이 모양만으로 안정성·생물 접착 원인을 확정하지 않는다.

프레이밍·배율·채택 조건: Frame the material and a same-plane scale; do not infer microscopic particles.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S02 NRCS Soil Texture and Structure Guide](https://www.nrcs.usda.gov/sites/default/files/2022-11/Texture%20and%20Structure%20-%20Soil%20Health%20Guide_0.pdf)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S02 [pdf_structure_verified] 입경표·토성 삼각형·구조 도식. 텍스트 추출이 빈약하여 도식 판독은 별도 검증한다.

## E006 · 판상·괴상·주상 구조

토양 구조는 입자가 모여 배열된 형식이다.

원 대화 범주: 5 · 표현 방식: macro · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_face | thin horizontal peds stacked within a soil face |
| ped_boundary | separation planes bounding those same peds |
| scale_reference | a centimetre scale adjacent to the exposed structure |

관계: ped_boundary → bounds → soil_face

혼동 경계: 입자의 납작함과 판상 입단을 구별한다. 주상·괴상 변형은 수직/덩어리 방향을 별도로 작성한다.

프레이밍·배율·채택 조건: Frame the material and a same-plane scale; do not infer microscopic particles.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S02 NRCS Soil Texture and Structure Guide](https://www.nrcs.usda.gov/sites/default/files/2022-11/Texture%20and%20Structure%20-%20Soil%20Health%20Guide_0.pdf)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S02 [pdf_structure_verified] 입경표·토성 삼각형·구조 도식. 텍스트 추출이 빈약하여 도식 판독은 별도 검증한다.

## E007 · 마른 흙의 분진과 발생점

바람·접촉으로 지표 입자가 공중에 이동할 수 있다.

원 대화 범주: 2, 12, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_surface | a dry loose surface at the wheel contact |
| dust | a suspended dust plume starting at that contact |
| wheel | a wheel touching the same dusty ground patch |

관계: dust → originates_at → soil_surface

혼동 경계: 먼지와 안개·연기·필름 입자를 구별한다. 달에서는 대기 중 먼지 구름으로 적용하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S06 NPS Aeolian Landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm)

출처 확인 범위: S06 [direct_text] 바람의 침식·운반·퇴적; 사구·뢰스·풍식석·야르당과 다양한 발생 환경.

## E008 · 진흙과 흙탕물의 상태 차이

진흙의 변형 가능한 바탕과 물속 부유 입자는 다른 상태다.

원 대화 범주: 2, 6, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| mud | a cohesive muddy bed holding a shallow groove |
| water | turbid standing water adjoining that muddy bed |
| contact_boundary | a visible margin between bed and standing water |

관계: water → adjoins → mud

혼동 경계: 갈색 액체만으로 진흙 바닥을 증명하지 않는다. 물의 탁함과 점도는 같은 뜻이 아니다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S13 USGS Aquifers and Groundwater](https://www.usgs.gov/water-science-school/science/aquifers-and-groundwater)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S13 [primary_search_excerpt_after_timeout] 대수층·피압·함양·수위의 관계. 직접 본문 요청은 timeout.

## E009 · 촉촉한 무광 흙과 수막 광택

토색 관찰에는 수분 상태를 함께 기록한다.

원 대화 범주: 4, 6, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_surface | a damp matte patch beside a wetter glossy patch |
| water_film | small specular reflections confined to the wetter patch |
| boundary | a local moisture boundary across the same soil surface |

관계: water_film → coats → soil_surface

혼동 경계: 젖은 흙 전체를 검정 플라스틱으로 바꾸지 않는다. 어두운 색만으로 수분량을 측정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.

## E010 · 발의 압력과 진흙 발자국

접촉 자국은 눌린 바탕과 그 접촉체의 관계로 작성한다.

원 대화 범주: 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| boot | one boot partly pressing into a muddy surface |
| footprint | a matching tread depression beside that same boot |
| mud_ridge | displaced mud raised along the impression edge |

관계: boot → imprints → footprint

혼동 경계: 공중에 뜬 부츠와 떨어진 자국은 접촉 증거가 아니다. 얕은 자국으로 지반 지지력을 확정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E011 · 차륜 홈과 융기한 흙

하중 흔적은 차륜·홈·밀려난 재료의 연결로 묘사한다.

원 대화 범주: 29, 21 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| rut | two parallel wheel ruts along one dirt track |
| soil_ridge | displaced soil ridges along the rut sides |
| tread | repeated tread marks aligned with each rut |

관계: tread → marks → rut

혼동 경계: 하천 도랑·경작 이랑과 혼동하지 않는다. 자국만으로 차량 무게·통행 횟수를 추정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E012 · 다각형 건열과 마른 판

기존 건열 후보의 연결된 균열·마른 판·공통 표면을 재사용한다.

원 대화 범주: 8, 12, 29 · 표현 방식: reuse · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| crack_network | connected polygonal cracks across one dry sediment surface |
| sediment_plate | dried sediment plates bounded by those cracks |
| surface | a coherent drying bed carrying the complete crack network |

관계: crack_network → bounds → sediment_plate

혼동 경계: 시멘트 줄눈·파충류 비늘·얼음 쐐기 다각형은 다른 의미다. 건열만으로 버티솔을 진단하지 않는다.

프레이밍·배율·채택 조건: Review the cited existing ID before adding any duplicate realization.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E013 · 공극과 뿌리 통로

공극은 입자·입단 사이의 공간이며 통로와 연결될 수 있다.

원 대화 범주: 5, 19 · 표현 방식: macro · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_face | an exposed soil face with resolved channel openings |
| root_channel | a root-sized channel continuing into the soil face |
| aggregate | crumb boundaries surrounding the channel mouth |

관계: root_channel → passes_through → soil_face

혼동 경계: 모든 공극을 거대한 동굴로 바꾸지 않는다. 사진으로 공극률·투수계수를 수치화하지 않는다.

프레이밍·배율·채택 조건: Frame the material and a same-plane scale; do not infer microscopic particles.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.

## E014 · 가소성 점토의 눌림

가소성의 시각 단서는 성형 후 남는 변형을 보여주는 것이다.

원 대화 범주: 5, 22 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| hand | fingertips pressing one soft clay lump |
| clay | finger grooves retained on that same clay lump |
| clay | a folded edge adjoining the fresh grooves |

관계: hand → deforms → clay

혼동 경계: 가마 소성과 구별한다. 표면 홈만으로 광물 조성이나 손의 감각을 확정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S02 NRCS Soil Texture and Structure Guide](https://www.nrcs.usda.gov/sites/default/files/2022-11/Texture%20and%20Structure%20-%20Soil%20Health%20Guide_0.pdf), [S21 V&A An A-Z of Ceramics](https://www.vam.ac.uk/articles/a-z-of-ceramics)

출처 확인 범위: S02 [pdf_structure_verified] 입경표·토성 삼각형·구조 도식. 텍스트 추출이 빈약하여 도식 판독은 별도 검증한다.; S21 [primary_search_text_and_page] 슬립·몸체·유약·자기 관련 재료 구별. 모든 성형 방식의 작업 과정 자료는 아니다.

## E015 · 팽윤·수축·압밀의 시간성

부피 변화와 배수 과정은 시점·하중·수분 조건을 필요로 한다.

원 대화 범주: 5 · 표현 방식: context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| sample_pair | two time-labelled views of the same soil specimen |
| scale_reference | the same scale visible beside both specimen views |
| measurement | a separate measurement annotation outside the soil material |

관계: measurement → describes → sample_pair

혼동 경계: 단일 정지 사진으로 변화량·속도·원인을 증명하지 않는다. 다짐과 압밀을 동의어로 묶지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.

## E016 · 토양 단면의 층위 경계

토양 단면은 층위의 수직 배열이다.

원 대화 범주: 3 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_cut | a continuous vertical soil exposure from surface downward |
| horizon_boundary | irregular boundaries separating contrasting soil bands |
| scale_reference | a vertical depth scale against the same soil cut |

관계: horizon_boundary → divides → soil_cut

혼동 경계: O-A-E-B-C-R을 모든 토양에 강제하지 않는다. 장식 줄무늬와 퇴적 층리를 토양층위로 확정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile)

출처 확인 범위: S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.

## E017 · 낙엽층과 어두운 상부 광물층

유기성 피복과 아래의 광물성 상부층은 구별한다.

원 대화 범주: 3, 19, 20 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| litter | recognisable leaf fragments lying at the ground surface |
| topsoil | a darker mineral layer directly beneath those fragments |
| root | fine roots crossing the litter to topsoil boundary |

관계: litter → overlies → topsoil

혼동 경계: 어두운 색만으로 유기물 함량·비옥도를 확정하지 않는다. 낙엽층을 모든 A층의 필수 조건으로 삼지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile), [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer)

출처 확인 범위: S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.; S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.

## E018 · 밝은 용탈층과 아래 집적층의 대비

밝은 용탈층과 어두운 아래층은 특정 단면 표현의 대비 단서다.

원 대화 범주: 3, 4 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| upper_band | a pale subsurface band in one soil cut |
| lower_band | a darker band immediately below that pale band |
| boundary | the continuous boundary linking the two bands |

관계: upper_band → overlies → lower_band

혼동 경계: 밝음만으로 E층·포드졸을 진단하지 않는다. 토양학 이름을 쓸 때 조사된 단면 문맥을 별도 유지한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/)

출처 확인 범위: S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.

## E019 · 풍화 모재와 연속 기반암

모재에 가까운 층과 단단한 기반암은 같은 흙층이 아니다.

원 대화 범주: 3, 17 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| weathered_material | loose weathered fragments above a rock contact |
| bedrock | continuous coherent bedrock below that contact |
| contact | a visible transition from loose material to solid rock |

관계: weathered_material → overlies → bedrock

혼동 경계: 기반암을 검은 흙층으로 그리지 않는다. C층 모재가 언제나 바로 아래 암석에서 유래한다고 단정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile), [S18 British Geological Survey Rocks and Minerals](https://www.bgs.ac.uk/discovering-geology/rocks-and-minerals/)

출처 확인 범위: S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.; S18 [direct_page_scope] 암석/광물/풍화 연구의 출처 입구. 개별 암종·자원 수치의 전수 검증은 아니다.

## E020 · 묻힌 옛 토양과 시간 문맥

고토양은 과거 형성 후 보존된 토양이라는 해석을 포함한다.

원 대화 범주: 3, 24 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| buried_band | a soil-like band buried below younger sediment |
| overburden | a younger sediment package above the buried band |
| soil_cut | a single exposure showing their stratigraphic relation |

관계: overburden → overlies → buried_band

혼동 경계: 색 띠만으로 연대·고기후를 확정하지 않는다. 인물 초상 배경에 수직 절개를 자동 추가하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.

## E021 · 황갈색·적갈색·검은 토색

색 이름은 토양군·광물·기원 분류와 분리해 기록한다.

원 대화 범주: 4, 23, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_surface | a reddish brown soil patch under neutral illumination |
| reference | a neutral colour reference beside the soil patch |
| soil_surface | visible granular texture inside the coloured patch |

관계: reference → calibrates → soil_surface

혼동 경계: 적토를 피·화산재·오커 안료와 동일시하지 않는다. 조명색·후보정색을 흙의 물체색으로 대신하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.

## E022 · 체르노젬 문맥과 두꺼운 어두운 표층

체르노젬은 진단 요건을 가진 토양군이다.

원 대화 범주: 4 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_cut | a thick dark surface band in a documented soil cut |
| lower_band | a contrasting lower band beneath that surface band |
| grass_roots | grass roots entering the dark upper band |

관계: grass_roots → penetrate → soil_cut

혼동 경계: 검은 흙만으로 체르노젬·비옥도·초원 기원을 확정하지 않는다. 분류 검증은 사진 gate 밖에 둔다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.

## E023 · 포드졸의 조사 단면 문맥

포드졸 분류는 표층의 검은색 하나로 결정되지 않는다.

원 대화 범주: 4 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_cut | a documented cut with a pale intermediate band |
| subsoil | a darker subsurface band below the pale band |
| boundary | continuous uneven contacts across the same cut |

관계: subsoil → underlies → soil_cut

혼동 경계: 일반 숲바닥을 밝은 E층과 B층의 필수 조합으로 강제하지 않는다. E018과 중복 반영을 피한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.

## E024 · 화산성 흙·신선한 재·마사 재료

토양의 화산성 기원과 신선한 화산재·화강암 풍화재는 별개다.

원 대화 범주: 4, 17 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| volcanic_sample | a documented loose volcanic soil specimen |
| fragment | porous rock fragments adjoining that specimen |
| sample_boundary | a clear boundary between soil and separate ash sample |

관계: fragment → adjoins → volcanic_sample

혼동 경계: 안도솔=검은 흙으로 등록하지 않는다. 마사토와 신선한 화산재는 독립 후보가 필요하다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/), [S18 British Geological Survey Rocks and Minerals](https://www.bgs.ac.uk/discovering-geology/rocks-and-minerals/)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.; S18 [direct_page_scope] 암석/광물/풍화 연구의 출처 입구. 개별 암종·자원 수치의 전수 검증은 아니다.

## E025 · 이탄의 식물 섬유와 유기층

이탄과 유기성 토양군 이름은 재료와 분류의 차이를 유지한다.

원 대화 범주: 4, 18, 20 · 표현 방식: macro · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| peat | recognisable plant fibres within a dark organic slab |
| peat | compressed layered fibres exposed along the slab edge |
| cut_edge | a wet cut edge belonging to that same slab |

관계: cut_edge → exposes → peat

혼동 경계: 검은 진흙·석탄·부엽토와 자동 병합하지 않는다. 히스토솔 진단·탄소량은 별도 자료가 필요하다.

프레이밍·배율·채택 조건: Frame the material and a same-plane scale; do not infer microscopic particles.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/), [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.; S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.

## E026 · 버티솔의 수축 흔적과 쐐기 입단

버티솔은 수축성 점토와 진단 구조를 포함하는 분류다.

원 대화 범주: 4, 5 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_face | wedge-shaped peds within a documented clay soil face |
| ped_face | smooth grooved faces on those same peds |
| crack | a deep crack extending from the upper surface |

관계: ped_face → part_of → soil_face

혼동 경계: 건열 하나만으로 버티솔을 확정하지 않는다. 매끈한 면을 젖은 피부 광택으로 치환하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.

## E027 · 회색 바탕과 산화환원 반점

글레이성 표현의 회색 바탕과 반점은 수분 문맥과 함께 해석한다.

원 대화 범주: 4, 6 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_face | a grey matrix on one exposed soil face |
| mottle | rust-coloured mottles embedded within that grey matrix |
| root_channel | a root channel crossing the mottled soil face |

관계: mottle → embedded_in → soil_face

혼동 경계: 회색 흙=글레이솔·오염·특정 수위로 등록하지 않는다. 반점을 단순 색보정으로 대신하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.

## E028 · 소금 피막과 토양 바탕

표면 염류 석출과 솔론차크 분류는 다른 증거 수준이다.

원 대화 범주: 4, 8, 12, 29 · 표현 방식: macro · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| salt_crust | a white crystalline crust attached to a soil patch |
| soil_surface | brown substrate exposed through broken crust edges |
| salt_crust | raised crystal grains resolved at the crust margin |

관계: salt_crust → adheres_to → soil_surface

혼동 경계: 눈·흰 페인트·석고·균사를 배제한다. 하얀 피막만으로 염류 종류·농도·식물 피해를 진단하지 않는다.

프레이밍·배율·채택 조건: Frame the material and a same-plane scale; do not infer microscopic particles.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/), [S10 NRCS Resource Concern Guide Sheets](https://www.nrcs.usda.gov/sites/default/files/2023-03/Resource%20Concern%20Guide%20Sheets_1.pdf)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.; S10 [primary_search_excerpt] 침식·다짐·유기물·염류 등 자원 문제 범주. 개별 현상 진단은 조사 자료가 필요하다.

## E029 · 최근 충적 재료의 층과 입경 변화

플루비솔은 충적성 물질과 진단 조건으로 분류한다.

원 대화 범주: 4, 7, 10 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_cut | thin sediment bands in a documented riverbank cut |
| gravel_band | a coarse band interleaved with finer bands |
| river | the adjacent river in the same wider view |

관계: gravel_band → interleaves → soil_cut

혼동 경계: 층리만으로 플루비솔·홍수 연대·층위 기호를 확정하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/), [S07 NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.; S07 [direct_text] 유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계.

## E030 · 아레노솔과 사질 바탕

아레노솔은 모래성 단면의 분류이며 모래 색 이름이 아니다.

원 대화 범주: 4, 2 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_cut | a deep documented cut dominated by loose sandy material |
| grain_patch | resolved sand grains at the cut margin |
| root | sparse roots entering the same sandy cut |

관계: grain_patch → part_of → soil_cut

혼동 경계: 모래사장만으로 아레노솔 분류를 확정하지 않는다. E002와 신규 중복을 검토한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.

## E031 · 탄산염 집적의 결절·백색 띠

칼시솔은 탄산염 집적 진단을 가진 토양군이다.

원 대화 범주: 4, 5 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_face | pale nodules embedded in a documented soil face |
| nodule | white material exposed at a broken nodule edge |
| matrix | contrasting finer soil matrix around the nodules |

관계: nodule → embedded_in → matrix

혼동 경계: 돌·염류·석고를 색만으로 구별하지 않는다. 산 반응·화학 조성은 사진 gate로 삼지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html), [S05 WRB Reference Soil Groups](https://wrb.isric.org/soilgroups/)

출처 확인 범위: S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.; S05 [direct_text_overview] 32개 토양군 개요와 예시 자료. 최종 분류 판정은 S04의 공식 키로 재확인해야 한다.

## E032 · pH·CEC·밀도·비옥도의 비가시성

측정 성질과 외형은 동일한 데이터가 아니다.

원 대화 범주: 5, 8, 20 · 표현 방식: context · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| soil_sample | a soil specimen beside a separate test report |
| report | reported values printed outside the specimen image |
| sample_label | a specimen identifier matching the separate report |

관계: report → describes → soil_sample

혼동 경계: 어두움=비옥함, 푸석함=높은 CEC, 황색=산성을 금지한다. 수치와 화학 안전성은 외형으로 생성하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile), [S04 IUSS WRB Documents](https://wrb.isric.org/documents.html)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.; S04 [direct_text_version] WRB 2022 제4판 및 2024 정정본 확인. 정정 PDF 본문 접근 실패; 세부 진단 임계값은 이 연구에서 새로 전사하지 않는다.

## E033 · 표면 침투의 관찰 문맥

침투는 물이 지표에서 토양으로 들어가는 과정이다.

원 대화 범주: 6, 5 · 표현 방식: context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| wetting_front | a visibly darkened wetting patch beneath added water |
| soil_surface | a surrounding drier patch on the same soil surface |
| time_pair | two ordered views retaining the same framing |

관계: wetting_front → within → soil_surface

혼동 경계: 단일 젖은 표면으로 침투율·함양량을 증명하지 않는다. 검은 화살표를 자연 사진 표면에 삽입하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S13 USGS Aquifers and Groundwater](https://www.usgs.gov/water-science-school/science/aquifers-and-groundwater)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S13 [primary_search_excerpt_after_timeout] 대수층·피압·함양·수위의 관계. 직접 본문 요청은 timeout.

## E034 · 대수층·지하수면의 단면 표현

지하수는 포화된 공극·틈에 존재하며 대수층은 공급 능력도 포함한다.

원 대화 범주: 6 · 표현 방식: diagram · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| porous_layer | a diagram showing water in connected pore spaces |
| confining_layer | a lower permeability layer drawn above a confined unit |
| water_table | a labelled saturation boundary inside the diagram |

관계: confining_layer → overlies → porous_layer

혼동 경계: 지하수를 자동으로 거대 지하 호수로 바꾸지 않는다. 투시 단면·화살표는 도식 요청에서만 채택한다.

프레이밍·배율·채택 조건: Require an explicit map/cutaway/diagram request; no natural-photo projection.

출처: [S13 USGS Aquifers and Groundwater](https://www.usgs.gov/water-science-school/science/aquifers-and-groundwater), [S14 USGS What Is Groundwater](https://www.usgs.gov/faqs/what-groundwater?items_per_page=6&page=1)

출처 확인 범위: S13 [primary_search_excerpt_after_timeout] 대수층·피압·함양·수위의 관계. 직접 본문 요청은 timeout.; S14 [primary_search_excerpt] 지하 호수/강이라는 단일 비유로 지하수를 설명하지 않는 경계.

## E035 · 샘과 연결된 출수 물길

기존 샘 출수점 후보를 재사용하고 토양·암반 출구를 구별한다.

원 대화 범주: 6, 13 · 표현 방식: reuse · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| spring_outlet | water emerging from a bounded natural ground opening |
| channel | a shallow channel connected to that same outlet |
| substrate | damp substrate immediately adjoining the outlet |

관계: spring_outlet → feeds → channel

혼동 경계: 배관·배수구를 자연 샘으로 바꾸지 않는다. 피압 여부·음용 가능성을 사진으로 확정하지 않는다.

프레이밍·배율·채택 조건: Review the cited existing ID before adding any duplicate realization.

출처: [S13 USGS Aquifers and Groundwater](https://www.usgs.gov/water-science-school/science/aquifers-and-groundwater), [S08 NPS Karst Landscapes](https://www.nps.gov/subjects/caves/karst-landscapes.htm), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S13 [primary_search_excerpt_after_timeout] 대수층·피압·함양·수위의 관계. 직접 본문 요청은 timeout.; S08 [direct_text] 용해성 기반암·함몰·지하 물길·샘의 관계.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E036 · 세류침식의 작은 분기 홈

집중 유출은 작은 침식 물길을 만들 수 있다.

원 대화 범주: 7, 8 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| slope | several narrow shallow channels on one exposed slope |
| rill | branching channels following the downhill direction |
| deposit | small sediment deposits below the channel mouths |

관계: rill → cuts → slope

혼동 경계: 경운 이랑·타이어 홈과 구별한다. 공통 척도 없이 크기를 임의 규정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S11 NRCS Rangeland Water Erosion](https://www.nrcs.usda.gov/sites/default/files/2024-05/NRCS_Rangeland%20Soil_Water%20Erosion_Factsheet_04092024.pdf)

출처 확인 범위: S11 [primary_search_excerpt] 면상 유실과 집중 유출에 의한 세류·구곡, 속도 감소 구간의 퇴적.

## E037 · 구곡침식의 깊은 도랑과 두부

구곡은 깊고 뚜렷한 침식 통로로 기술한다.

원 대화 범주: 7, 8 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| gully | a deeply incised channel with steep soil sides |
| head_scarp | an abrupt headcut at the upper channel end |
| scale_reference | a scale object beside the same channel wall |

관계: head_scarp → terminates → gully

혼동 경계: 작은 균열을 구곡으로 키우지 않는다. 자연 계곡·굴착 배수로와 구별한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S11 NRCS Rangeland Water Erosion](https://www.nrcs.usda.gov/sites/default/files/2024-05/NRCS_Rangeland%20Soil_Water%20Erosion_Factsheet_04092024.pdf), [S12 NRCS Rangeland Hydrology and Soil Erosion](https://directives.nrcs.usda.gov/sites/default/files2/1712930328/33930.pdf)

출처 확인 범위: S11 [primary_search_excerpt] 면상 유실과 집중 유출에 의한 세류·구곡, 속도 감소 구간의 퇴적.; S12 [primary_search_excerpt] 실제 세류/구곡 사진 및 도랑 두부와 사면의 관계. 수치 기준은 보편 threshold로 전사하지 않는다.

## E038 · 하안 침식과 노출 뿌리

침식면은 잘린 바탕·노출된 뿌리·물길의 관계로 표현한다.

원 대화 범주: 7, 8, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| bank | an undercut soil bank beside the active channel |
| root | roots extending from that same exposed bank |
| fallen_clod | loose clods resting beneath the undercut edge |

관계: root → protrudes_from → bank

혼동 경계: 나무뿌리를 공중의 장식 끈으로 그리지 않는다. 정지 사진으로 침식 속도를 확정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S07 NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm), [S11 NRCS Rangeland Water Erosion](https://www.nrcs.usda.gov/sites/default/files/2024-05/NRCS_Rangeland%20Soil_Water%20Erosion_Factsheet_04092024.pdf)

출처 확인 범위: S07 [direct_text] 유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계.; S11 [primary_search_excerpt] 면상 유실과 집중 유출에 의한 세류·구곡, 속도 감소 구간의 퇴적.

## E039 · 면상 유실과 빗방울 비산의 한계

면상 유실은 얇은 표층 제거이며 빗방울 충격과 구별한다.

원 대화 범주: 7, 8 · 표현 방식: context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| pedestal | small soil pedestals protected beneath stones |
| stone | stones resting atop those soil pedestals |
| soil_surface | lower exposed material surrounding the protected patches |

관계: stone → covers → pedestal

혼동 경계: 전체 표토 손실 두께는 비교 조사 없이 주장하지 않는다. 빗방울 splash와 공중 먼지는 다른 후보다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S11 NRCS Rangeland Water Erosion](https://www.nrcs.usda.gov/sites/default/files/2024-05/NRCS_Rangeland%20Soil_Water%20Erosion_Factsheet_04092024.pdf), [S26 MIT Rainfall Can Release Aerosols](https://news.mit.edu/2015/rainfall-can-release-aerosols-0114)

출처 확인 범위: S11 [primary_search_excerpt] 면상 유실과 집중 유출에 의한 세류·구곡, 속도 감소 구간의 퇴적.; S26 [direct_text] 빗방울 접촉과 에어로졸 이동 연구; 냄새의 가시적 실체를 주장하지 않는다.

## E040 · 토석류의 큰 돌과 세립 기질

토석류는 물·퇴적물·암석이 섞이는 흐름 문맥이다.

원 대화 범주: 8 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| debris_lobe | a lobate mixed debris deposit at a channel mouth |
| boulder | large clasts protruding from its finer muddy matrix |
| levee | lateral ridges bounding the same deposit |

관계: boulder → embedded_in → debris_lobe

혼동 경계: 균일한 갈색 물과 구별한다. 퇴적 외형만으로 발생 시점·유속·피해 인원을 추론하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S15 USGS Landslide Types and Processes](https://pubs.usgs.gov/circ/c1244/c1244.pdf), [S16 USGS Effects of Earthquakes](https://www.usgs.gov/programs/earthquake-hazards/what-are-effects-earthquakes)

출처 확인 범위: S15 [primary_search_excerpt] 회전형·병진형 등 재해 유형과 물질·이동 방식의 구별.; S16 [primary_search_excerpt] 낙석·사면 이동·액상화의 모래 분사·침하 등. 픽셀 진단 기준으로 쓰지 않는다.

## E041 · 산사태의 상부 절벽과 하부 퇴적

중력 사면 이동은 발생부·이동부·퇴적부로 나눠 기술한다.

원 대화 범주: 8 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| head_scarp | an exposed arcuate scarp high on one slope |
| displaced_mass | displaced earth extending below that same scarp |
| toe | a bulging debris toe at the lower end |

관계: displaced_mass → below → head_scarp

혼동 경계: 수직 절벽 하나를 산사태 증거로 삼지 않는다. 회전형·병진형 변형은 별도 작성한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S15 USGS Landslide Types and Processes](https://pubs.usgs.gov/circ/c1244/c1244.pdf), [S16 USGS Effects of Earthquakes](https://www.usgs.gov/programs/earthquake-hazards/what-are-effects-earthquakes)

출처 확인 범위: S15 [primary_search_excerpt] 회전형·병진형 등 재해 유형과 물질·이동 방식의 구별.; S16 [primary_search_excerpt] 낙석·사면 이동·액상화의 모래 분사·침하 등. 픽셀 진단 기준으로 쓰지 않는다.

## E042 · 낙석과 사면 아래 각진 암편

낙석 흔적은 공급 절벽과 사면 아래 암편을 연결해 보여준다.

원 대화 범주: 8, 9 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| cliff | a fractured rock face above a steep slope |
| talus | angular fragments accumulated below that same face |
| fragment | one large block resting among the smaller fragments |

관계: talus → below → cliff

혼동 경계: 하천의 둥근 자갈층과 구별한다. 정지 블록으로 떨어지는 순간을 증명하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S16 USGS Effects of Earthquakes](https://www.usgs.gov/programs/earthquake-hazards/what-are-effects-earthquakes), [S18 British Geological Survey Rocks and Minerals](https://www.bgs.ac.uk/discovering-geology/rocks-and-minerals/)

출처 확인 범위: S16 [primary_search_excerpt] 낙석·사면 이동·액상화의 모래 분사·침하 등. 픽셀 진단 기준으로 쓰지 않는다.; S18 [direct_page_scope] 암석/광물/풍화 연구의 출처 입구. 개별 암종·자원 수치의 전수 검증은 아니다.

## E043 · 돌리네·함몰의 표면 형태

카르스트 함몰은 용해·붕괴 문맥과 함께 해석한다.

원 대화 범주: 8, 13 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| depression | a closed ground depression with continuous surrounding rim |
| rim | exposed soil and rock along part of that rim |
| floor | a lower floor inside the same depression |

관계: rim → bounds → depression

혼동 경계: 모든 도로 함몰을 카르스트 싱크홀로 단정하지 않는다. 숨은 공동을 실제 사진에 자동 투시하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S08 NPS Karst Landscapes](https://www.nps.gov/subjects/caves/karst-landscapes.htm)

출처 확인 범위: S08 [direct_text] 용해성 기반암·함몰·지하 물길·샘의 관계.

## E044 · 액상화 문맥의 분사공과 침하

포화 지반 강도 손실에는 지진·지반 조사 문맥이 필요하다.

원 대화 범주: 8 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| sand_vent | a sand vent surrounded by fresh sandy ejecta |
| ground_crack | a nearby crack within the same affected ground patch |
| settled_object | a tilted object adjoining the disturbed patch |

관계: sand_vent → emits → sandy_ejecta

혼동 경계: 모래 분사공 하나로 액상화를 확진하지 않는다. 지열 샘·배관 누출과 대조한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S16 USGS Effects of Earthquakes](https://www.usgs.gov/programs/earthquake-hazards/what-are-effects-earthquakes)

출처 확인 범위: S16 [primary_search_excerpt] 낙석·사면 이동·액상화의 모래 분사·침하 등. 픽셀 진단 기준으로 쓰지 않는다.

## E045 · 다짐과 토양 밀봉의 차이

밀봉은 표면 피복이며 다짐은 토양의 치밀화 과정이다.

원 대화 범주: 8, 21 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| pavement | an impervious pavement edge covering ground |
| soil_cut | exposed soil continuing beneath the pavement edge |
| boundary | a visible cover boundary at the pavement margin |

관계: pavement → covers → soil_cut

혼동 경계: 포장색을 토양 상태로 오인하지 않는다. 겉으로 단단함만으로 용적밀도를 정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S10 NRCS Resource Concern Guide Sheets](https://www.nrcs.usda.gov/sites/default/files/2023-03/Resource%20Concern%20Guide%20Sheets_1.pdf)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S10 [primary_search_excerpt] 침식·다짐·유기물·염류 등 자원 문제 범주. 개별 현상 진단은 조사 자료가 필요하다.

## E046 · 황폐지·사막화의 시간·지역 문맥

사막화는 시간과 환경 문맥을 포함하는 토지 변화 개념이다.

원 대화 범주: 8, 12, 30 · 표현 방식: context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| land_pair | two dated views of the same documented land patch |
| vegetation | reduced ground cover in the later view |
| soil_surface | more exposed soil within the matched later framing |

관계: vegetation → covers → soil_surface

혼동 경계: 모래언덕·황색·건열 하나를 사막화 진단으로 등록하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S10 NRCS Resource Concern Guide Sheets](https://www.nrcs.usda.gov/sites/default/files/2023-03/Resource%20Concern%20Guide%20Sheets_1.pdf), [S06 NPS Aeolian Landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm)

출처 확인 범위: S10 [primary_search_excerpt] 침식·다짐·유기물·염류 등 자원 문제 범주. 개별 현상 진단은 조사 자료가 필요하다.; S06 [direct_text] 바람의 침식·운반·퇴적; 사구·뢰스·풍식석·야르당과 다양한 발생 환경.

## E047 · 고원·메사·뷰트의 윤곽

평탄한 상부와 사면 형태는 상대 크기·주변 지형과 함께 기술한다.

원 대화 범주: 9, 12 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| mesa | a broad flat summit bounded by steep sides |
| butte | a smaller isolated flat-topped remnant nearby |
| plain | a lower surrounding plain connecting both landforms |

관계: mesa → above → plain

혼동 경계: 지평선만으로 높은 고원을 증명하지 않는다. 메사와 뷰트의 절대 크기 임계값을 만들지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S36 NPS Arid and Semi-arid Landforms](https://www.nps.gov/subjects/geology/arid-landforms.htm)

출처 확인 범위: S36 [direct_text] 메사·뷰트의 평탄한 상부/급한 사면, 자갈 포장, 산지 출구의 선상 퇴적을 본문에서 확인. 수치 크기 기준을 만들지 않는다.

## E048 · 능선·안부·분지·계곡의 상대 위치

지형 이름은 주변의 높낮이와 연결 관계를 필요로 한다.

원 대화 범주: 9, 10 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| ridge | two high ridge segments flanking a lower saddle |
| saddle | a pass joining the two ridge segments |
| valley | a valley floor lying below that same saddle |

관계: saddle → connects → ridge

혼동 경계: 높은 점 하나는 능선이 아니다. 능선과 분수계는 문맥 없이 동일시하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S07 NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S07 [direct_text] 유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계.

## E049 · 암석 풍화의 제자리 흔적

풍화는 제자리에서 물질이 변하는 작용이다.

원 대화 범주: 7, 17 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| rock_face | a weathered outer rind on a fractured rock face |
| fresh_face | a fresher contrasting interior at the same break |
| loose_grains | loose grains immediately beneath that broken surface |

관계: rock_face → surrounds → fresh_face

혼동 경계: 운반·퇴적과 원인 표기를 분리한다. 붉음만으로 철 산화 조성을 확정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S18 British Geological Survey Rocks and Minerals](https://www.bgs.ac.uk/discovering-geology/rocks-and-minerals/)

출처 확인 범위: S18 [direct_page_scope] 암석/광물/풍화 연구의 출처 입구. 개별 암종·자원 수치의 전수 검증은 아니다.

## E050 · 선상지와 삼각주의 출구 차이

산지 출구의 선상 퇴적과 수역 진입의 삼각주는 위치 관계가 다르다.

원 대화 범주: 10, 7 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| fan | a fan-shaped deposit spreading from a narrow mountain outlet |
| outlet | a confined channel opening onto the fan apex |
| plain | an open plain receiving the widening deposit |

관계: outlet → feeds → fan

혼동 경계: 삼각주는 바다·호수 진입을 별도 후보로 작성한다. 모든 삼각주를 삼각형으로 강제하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S07 NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm), [S36 NPS Arid and Semi-arid Landforms](https://www.nps.gov/subjects/geology/arid-landforms.htm)

출처 확인 범위: S07 [direct_text] 유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계.; S36 [direct_text] 메사·뷰트의 평탄한 상부/급한 사면, 자갈 포장, 산지 출구의 선상 퇴적을 본문에서 확인. 수치 크기 기준을 만들지 않는다.

## E051 · 자연제방과 낮은 배후습지

하천 가까운 미고지와 뒤쪽 낮은 습지는 상대 위치가 핵심이다.

원 대화 범주: 10, 6 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| river | a channel flanked by low sediment ridges |
| levee | a continuous low ridge adjoining that channel |
| backswamp | lower wet ground behind the same ridge |

관계: levee → separates → backswamp

혼동 경계: 인공 제방과 혼동하지 않는다. 단일 사진으로 범람 주기를 확정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S07 NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm)

출처 확인 범위: S07 [direct_text] 유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계.

## E052 · 곡류·우각호·침식안·퇴적안

기존 하천 의미에서 연결과 단절을 재사용한다.

원 대화 범주: 10 · 표현 방식: reuse · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| oxbow | a curved water body disconnected from the main channel |
| land_neck | land separating the curved water body from the river |
| river | the nearby main river visible in the same aerial view |

관계: land_neck → separates → oxbow

혼동 경계: 넓은 굽이를 곧바로 우각호로 부르지 않는다. 하중도·안쪽 퇴적안은 독립 세부 후보로 검토한다.

프레이밍·배율·채택 조건: Review the cited existing ID before adding any duplicate realization.

출처: [S07 NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S07 [direct_text] 유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E053 · 망상하천의 분기와 재결합

여러 물길이 퇴적체 사이에서 갈라졌다 다시 만난다.

원 대화 범주: 10 · 표현 방식: reuse · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| channels | multiple shallow channels splitting around sediment bars |
| bars | exposed gravel bars bounded by those channels |
| reconnection | downstream reconnections between previously separated channels |

관계: channels → surround → bars

혼동 경계: 지류 합류 한 번과 구별한다. 기존 water_w070 계열을 우선 재사용한다.

프레이밍·배율·채택 조건: Review the cited existing ID before adding any duplicate realization.

출처: [S07 NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S07 [direct_text] 유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E054 · 하안단구의 상·하 평탄면

단구는 현재 물길보다 높게 남은 과거 하천면의 문맥이다.

원 대화 범주: 10, 9 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| terrace | a flat bench above the current river |
| scarp | a step-like slope separating bench from lower floodplain |
| river | the current river lying below that same bench |

관계: terrace → above → river

혼동 경계: 계단식 농경지와 구별한다. 높이만으로 형성 연대나 융기량을 확정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S07 NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm)

출처 확인 범위: S07 [direct_text] 유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계.

## E055 · 반도·지협·섬의 연결 그래프

물과 육지의 연결·둘러싸임은 이름의 주요 공간 단서다.

원 대화 범주: 11, 16 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| isthmus | a narrow land neck connecting two larger land areas |
| water | water bordering both sides of that neck |
| landmasses | two continuous land areas joined through the neck |

관계: isthmus → connects → landmasses

혼동 경계: 사람 높이 사진의 좁은 길만으로 지협을 주장하지 않는다. 군도와 군용 칼의 동음 의미를 분리한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S09 NPS Beaches and Coastal Landforms](https://www.nps.gov/subjects/geology/coastal-landforms.htm), [S37 USGS This Dynamic Earth Plate Boundaries](https://pubs.usgs.gov/gip/dynamic/understanding.html)

출처 확인 범위: S09 [direct_text] 육수 경계·침식/퇴적 해안과 재료/조석/파랑 조건의 분리.; S37 [direct_fetch_failed] 원 대화의 판 구조 출처 단서. 지도/단층의 상세 지질 해석은 승격 전 재확인.

## E056 · 사취·육계사주·석호의 결합

퇴적 띠의 양끝 연결과 뒤쪽 수역을 구별한다.

원 대화 범주: 11 · 표현 방식: reuse · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| tombolo | a sediment ridge joining mainland to an offshore island |
| island | an island attached at the ridge outer end |
| water | water flanking both sides of the connecting ridge |

관계: tombolo → connects → island

혼동 경계: 한쪽만 붙은 사취와 구별한다. 기존 water_w077 계열의 관계를 우선 재사용한다.

프레이밍·배율·채택 조건: Review the cited existing ID before adding any duplicate realization.

출처: [S09 NPS Beaches and Coastal Landforms](https://www.nps.gov/subjects/geology/coastal-landforms.htm), [S38 NPS Sandy Coast Landforms](https://www.nps.gov/articles/sandy-coast-landforms.htm), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S09 [direct_text] 육수 경계·침식/퇴적 해안과 재료/조석/파랑 조건의 분리.; S38 [direct_text] 사주·사취·육계사주의 연결/퇴적 관계.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E057 · 모래 해변·자갈 해변·펄의 바탕

해변 재료와 조간대 위치는 별도 속성이다.

원 대화 범주: 11, 2 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| tidal_flat | a fine wet sediment flat beside a shallow tidal channel |
| channel | branching drainage grooves across that flat |
| waterline | a receding waterline adjoining the same flat |

관계: channel → cuts → tidal_flat

혼동 경계: 모든 갯벌이 순수 점토라는 정의를 피한다. 펄의 질척함만으로 염도·조석 시각을 정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S09 NPS Beaches and Coastal Landforms](https://www.nps.gov/subjects/geology/coastal-landforms.htm), [S06 NPS Aeolian Landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm)

출처 확인 범위: S09 [direct_text] 육수 경계·침식/퇴적 해안과 재료/조석/파랑 조건의 분리.; S06 [direct_text] 바람의 침식·운반·퇴적; 사구·뢰스·풍식석·야르당과 다양한 발생 환경.

## E058 · 해식애와 바다의 고립 바위기둥

해안 침식 지형의 바위와 해수 경계를 연결해 보여준다.

원 대화 범주: 11, 13 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| sea_stack | an isolated rock pillar surrounded by seawater |
| cliff | a nearby coastal cliff above the same waterline |
| water | seawater continuously separating pillar from the cliff |

관계: water → separates → sea_stack

혼동 경계: 단순 육상 뷰트와 구별한다. 고립 외형만으로 침식 연대를 확정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S09 NPS Beaches and Coastal Landforms](https://www.nps.gov/subjects/geology/coastal-landforms.htm)

출처 확인 범위: S09 [direct_text] 육수 경계·침식/퇴적 해안과 재료/조석/파랑 조건의 분리.

## E059 · 사구의 사면과 바르한 방향

사구는 바람에 쌓인 모래 언덕이며 해안에도 존재한다.

원 대화 범주: 12, 11 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| dune | a crescent-shaped sandy ridge with two extending horns |
| slip_face | a steeper face on one side of that ridge |
| stoss_slope | a gentler opposing slope on the same dune |

관계: slip_face → part_of → dune

혼동 경계: 바람 방향은 물체 움직임·문맥으로 검증한다. 모든 사막·해변에 바르한을 추가하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S06 NPS Aeolian Landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm)

출처 확인 범위: S06 [direct_text] 바람의 침식·운반·퇴적; 사구·뢰스·풍식석·야르당과 다양한 발생 환경.

## E060 · 모래 표면 사련의 배율

작은 퇴적물 물결무늬와 물의 표면 파도는 다르다.

원 대화 범주: 12, 2 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| sand_patch | repeated low ripple ridges on one sand patch |
| trough | dry sandy troughs between those ridges |
| scale_reference | a small scale reference beside the ripple pattern |

관계: trough → separates → sand_patch

혼동 경계: 수면 물결·거대한 사구와 구별한다. 사련만으로 바람/물 원인을 확정하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S06 NPS Aeolian Landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm), [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual)

출처 확인 범위: S06 [direct_text] 바람의 침식·운반·퇴적; 사구·뢰스·풍식석·야르당과 다양한 발생 환경.; S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.

## E061 · 뢰스의 퇴적 기원과 절개 표현

뢰스는 바람에 운반된 실트 중심 퇴적물이다.

원 대화 범주: 4, 12, 7 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| loess_cut | a documented fine sediment cliff with vertical joints |
| fine_matrix | fine material exposed across that same cut |
| land_context | the surrounding landscape visible beyond the cut |

관계: fine_matrix → part_of → loess_cut

혼동 경계: 황토색·황토 재료를 뢰스의 동의어로 강제하지 않는다. 기원은 조사 문맥으로 유지한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S06 NPS Aeolian Landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm)

출처 확인 범위: S06 [direct_text] 바람의 침식·운반·퇴적; 사구·뢰스·풍식석·야르당과 다양한 발생 환경.

## E062 · 야르당 능선과 풍식석의 표면

풍식의 능선형 지형과 암석 표면 마모는 규모가 다르다.

원 대화 범주: 12 · 표현 방식: direct · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| yardang | elongated parallel ridges in a sparsely vegetated terrain |
| corridor | eroded troughs running between those ridges |
| terrain | a common ground plane carrying the ridge field |

관계: corridor → separates → yardang

혼동 경계: 풍식석은 개별 암석의 면·홈으로 별도 작성한다. 사구의 퇴적 사면과 구별한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S06 NPS Aeolian Landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm)

출처 확인 범위: S06 [direct_text] 바람의 침식·운반·퇴적; 사구·뢰스·풍식석·야르당과 다양한 발생 환경.

## E063 · 자갈 포장 사막과 모래바다

사막의 표면은 모래·암석·자갈·염류 등 다양하다.

원 대화 범주: 12 · 표현 방식: direct · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| pavement | a closely packed gravel surface extending across dry terrain |
| fine_matrix | fine material visible between the gravel clasts |
| boundary | a nearby loose sand patch separated from the gravel cover |

관계: pavement → covers → fine_matrix

혼동 경계: 사막포도를 포도 열매로 오해하지 않는다. 어스 톤만으로 건조 기후를 진단하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S06 NPS Aeolian Landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm), [S36 NPS Arid and Semi-arid Landforms](https://www.nps.gov/subjects/geology/arid-landforms.htm)

출처 확인 범위: S06 [direct_text] 바람의 침식·운반·퇴적; 사구·뢰스·풍식석·야르당과 다양한 발생 환경.; S36 [direct_text] 메사·뷰트의 평탄한 상부/급한 사면, 자갈 포장, 산지 출구의 선상 퇴적을 본문에서 확인. 수치 크기 기준을 만들지 않는다.

## E064 · 용식·용암·해식동굴의 문맥

동굴의 빈 공간과 형성 원인은 별개 자료다.

원 대화 범주: 13, 7 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| cave | a bounded cave entrance continuing into a dark passage |
| rock_wall | coherent bedrock framing the passage entrance |
| ground | an entrance floor continuous with the exterior ground |

관계: rock_wall → bounds → cave

혼동 경계: 어둠만으로 지하·카르스트를 주장하지 않는다. 원인별 동굴은 조사 문맥과 재료를 별도 작성한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S08 NPS Karst Landscapes](https://www.nps.gov/subjects/caves/karst-landscapes.htm), [S39 NPS Speleothems](https://www.nps.gov/subjects/caves/speleothems.htm)

출처 확인 범위: S08 [direct_text] 용해성 기반암·함몰·지하 물길·샘의 관계.; S39 [direct_text] 천장 종유석·바닥 석순·연결 기둥의 부착 방향을 본문에서 확인. 형태만으로 정확한 광물 조성을 판정하지 않는다.

## E065 · 종유석·석순·석주의 부착 방향

천장·바닥 부착과 두 구조의 연결을 구별한다.

원 대화 범주: 13 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| stalactite | a tapered formation attached to the cave ceiling |
| stalagmite | an upward formation attached to the floor below |
| column | a separate continuous column joining floor and ceiling |

관계: stalactite → attached_to → cave_ceiling

혼동 경계: 바닥 위의 뾰족한 돌을 종유석으로 부르지 않는다. 물고드름은 다른 재료다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S39 NPS Speleothems](https://www.nps.gov/subjects/caves/speleothems.htm)

출처 확인 범위: S39 [direct_text] 천장 종유석·바닥 석순·연결 기둥의 부착 방향을 본문에서 확인. 형태만으로 정확한 광물 조성을 판정하지 않는다.

## E066 · 빙하 계곡·권곡·아레트의 지형

빙하 침식 지형은 주변 사면과 계곡 단면으로 표현한다.

원 대화 범주: 14, 9 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| valley | a broad U-shaped valley with steep sidewalls |
| floor | a relatively broad valley floor between the sidewalls |
| cirque | a bowl-like headwall basin at the upper valley end |

관계: floor → between → valley_walls

혼동 경계: 모든 계곡을 U자곡으로 만들지 않는다. 빙하가 현재 화면 안에 있어야만 옛 빙하 지형인 것은 아니다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S19 NPS Glaciers and Glacial Landforms](https://home.nps.gov/subjects/geology/glacial-landforms.htm)

출처 확인 범위: S19 [primary_search_excerpt] 빙하 침식과 퇴적 지형 및 틸과 지형의 구별.

## E067 · 틸·모레인·표석·에스커의 규모

퇴적 재료와 퇴적 지형의 이름을 분리한다.

원 대화 범주: 14, 2 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| moraine | a debris ridge along a documented glacier margin |
| clasts | mixed-size rock fragments visible on that ridge |
| glacier | the adjoining glacier edge in the same landscape view |

관계: moraine → adjoins → glacier

혼동 경계: 틸을 모두 둥근 하천 자갈로 그리지 않는다. 드럼린·에스커는 형태별 별도 세부 후보로 작성한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S19 NPS Glaciers and Glacial Landforms](https://home.nps.gov/subjects/geology/glacial-landforms.htm)

출처 확인 범위: S19 [primary_search_excerpt] 빙하 침식과 퇴적 지형 및 틸과 지형의 구별.

## E068 · 영구동토·활동층과 얼음 쐐기

영구동토는 최소 2년의 동결 지속이라는 시간 정의다.

원 대화 범주: 14, 5 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| ground_cut | a documented frozen-ground cut with an exposed ice wedge |
| ice_wedge | a wedge of ice extending downward into that cut |
| surface_polygon | polygon boundaries at the surface above the wedge |

관계: ice_wedge → within → ground_cut

혼동 경계: 눈 덮인 땅을 영구동토로 확정하지 않는다. 마른 진흙 건열과 얼음 쐐기를 별도 의미로 둔다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S20 NSIDC Science of Frozen Ground](https://nsidc.org/learn/parts-cryosphere/frozen-ground-permafrost/science-frozen-ground), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S20 [direct_text] 2년 이상 동결의 정의, 얼음 쐐기·열카르스트와 관측 문맥.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E069 · 열카르스트의 꺼진 지표와 수면

열카르스트는 지중 얼음 해빙과 연결된 지표 변화 문맥이다.

원 대화 범주: 14, 8 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| depression | a subsided ground patch adjoining a thaw pond |
| pond | standing water within the lower depression |
| bank | an uneven retreating bank beside the same pond |

관계: pond → occupies → depression

혼동 경계: 모든 웅덩이를 열카르스트로 부르지 않는다. 사진으로 동토 온도·해빙 기간을 확정하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S20 NSIDC Science of Frozen Ground](https://nsidc.org/learn/parts-cryosphere/frozen-ground-permafrost/science-frozen-ground)

출처 확인 범위: S20 [direct_text] 2년 이상 동결의 정의, 얼음 쐐기·열카르스트와 관측 문맥.

## E070 · 단층 어긋남과 습곡의 연속 층

끊겨 어긋난 층과 이어져 굽은 층은 다른 형상이다.

원 대화 범주: 15, 7 · 표현 방식: direct · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| strata | continuous layered bands bent through one rock exposure |
| fold_hinge | a curved hinge shared by several adjacent bands |
| rock_face | a coherent rock face containing the whole fold |

관계: fold_hinge → bends → strata

혼동 경계: 토양 줄무늬·회화 무늬와 구별한다. 단층 변형은 잘린 같은 층의 양쪽 어긋남을 별도 작성한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S46 USGS What Is a Tectonic Plate](https://pubs.usgs.gov/gip/dynamic/tectonic.html), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S46 [primary_search_excerpt_after_403] 기관 검색 본문에서 판이 대륙·해양 암석권을 함께 포함할 수 있음을 확인; 직접 요청은 403. 대륙 윤곽과 판을 동일시하지 않는다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E071 · 대륙·지각·판·대륙붕의 표현

지리 단위와 지질 구조·수심 단위는 서로 다른 관찰 범위다.

원 대화 범주: 15, 16, 1 · 표현 방식: diagram · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| map | a labelled map with a declared projection and date |
| continental_shelf | a bathymetric shelf band beyond a coastline |
| tectonic_boundary | a separately styled plate boundary on the same map |

관계: continental_shelf → extends_beyond → coastline

혼동 경계: 대륙 이름만으로 특정 지형·인종·의상을 강제하지 않는다. 판 경계와 해안선을 동일 선으로 그리지 않는다.

프레이밍·배율·채택 조건: Require an explicit map/cutaway/diagram request; no natural-photo projection.

출처: [S46 USGS What Is a Tectonic Plate](https://pubs.usgs.gov/gip/dynamic/tectonic.html), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S46 [primary_search_excerpt_after_403] 기관 검색 본문에서 판이 대륙·해양 암석권을 함께 포함할 수 있음을 확인; 직접 요청은 403. 대륙 윤곽과 판을 동일시하지 않는다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E072 · 암석·광물·입경의 독립 축

암석 종류·광물 종류·입자 크기는 함께 적용될 수 있는 다른 분류다.

원 대화 범주: 17, 2 · 표현 방식: macro · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| rock | interlocking light and dark crystals on a rock specimen |
| fracture | a fresh broken face exposing those same crystals |
| scale_reference | a scale reference beside the specimen edge |

관계: fracture → exposes → rock

혼동 경계: 모래=석영, 흰색=대리암, 검은색=현무암으로 확정하지 않는다. 화성·퇴적·변성의 각각은 따로 조사한다.

프레이밍·배율·채택 조건: Frame the material and a same-plane scale; do not infer microscopic particles.

출처: [S18 British Geological Survey Rocks and Minerals](https://www.bgs.ac.uk/discovering-geology/rocks-and-minerals/)

출처 확인 범위: S18 [direct_page_scope] 암석/광물/풍화 연구의 출처 입구. 개별 암종·자원 수치의 전수 검증은 아니다.

## E073 · 광맥·광상·사금의 주장 한계

광물의 집중과 경제적 광석 평가는 동일하지 않다.

원 대화 범주: 18, 17 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| vein | a contrasting mineral band crossing a rock specimen |
| host_rock | host rock visible on both sides of that band |
| contact | two clear contacts bounding the mineral band |

관계: vein → cuts → host_rock

혼동 경계: 반짝임만으로 금·광석 품위를 확정하지 않는다. 사금은 퇴적물 속 입자 관계를 별도 작성한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S18 British Geological Survey Rocks and Minerals](https://www.bgs.ac.uk/discovering-geology/rocks-and-minerals/)

출처 확인 범위: S18 [direct_page_scope] 암석/광물/풍화 연구의 출처 입구. 개별 암종·자원 수치의 전수 검증은 아니다.

## E074 · 석탄·원유·가스·지열의 별도 기원

지하 자원을 오래된 흙의 단순 변형으로 설명하지 않는다.

원 대화 범주: 18, 17 · 표현 방식: context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| specimen | a separately labelled resource specimen |
| host_context | a documented geological context outside the specimen |
| record | a resource identification record beside that context |

관계: record → describes → specimen

혼동 경계: 검은 흙을 석탄·원유로 바꾸지 않는다. 지열은 흙의 외형 재료 후보가 아니다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S18 British Geological Survey Rocks and Minerals](https://www.bgs.ac.uk/discovering-geology/rocks-and-minerals/), [S13 USGS Aquifers and Groundwater](https://www.usgs.gov/water-science-school/science/aquifers-and-groundwater)

출처 확인 범위: S18 [direct_page_scope] 암석/광물/풍화 연구의 출처 입구. 개별 암종·자원 수치의 전수 검증은 아니다.; S13 [primary_search_excerpt_after_timeout] 대수층·피압·함양·수위의 관계. 직접 본문 요청은 timeout.

## E075 · 토양 미생물과 생물 피각

미생물의 실체와 지표 생물 피각의 거시 외형은 구별한다.

원 대화 범주: 19 · 표현 방식: micro · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| micrograph | a calibrated micrograph of one soil sample |
| scale_bar | a micrometre scale inside that micrograph |
| soil_sample | the bulk sample separately identified beside the micrograph |

관계: micrograph → depicts → soil_sample

혼동 경계: 풍경에 거대 세균·선충을 자동 추가하지 않는다. 생물 피각은 기존 후보를 보강하는 별도 거시 변형이다.

프레이밍·배율·채택 조건: Require a requested microscope/magnified view and verified sample identity. No ordinary-photo hard profile.

출처: [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a), [S47 NPS Cryptobiotic Soil Crusts](https://www.nps.gov/glca/learn/nature/soils.htm)

출처 확인 범위: S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.; S47 [primary_search_excerpt] 생물 피각과 일반 마른 물리 피막을 구별하는 출처 단서.

## E076 · 균사·균근·근권·뿌리털

실 모양 구조와 공생 관계·활동 영역은 다른 의미다.

원 대화 범주: 19, 20 · 표현 방식: micro · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| root | an identified root segment in a magnified sample |
| hyphae | fine fungal filaments adjoining the same root |
| scale_bar | a calibrated scale beside the root and filaments |

관계: hyphae → adjoin → root

혼동 경계: 흰 실만으로 균근·질소고정·건강한 공생을 확정하지 않는다. 뿌리털과 균사는 별도로 식별한다.

프레이밍·배율·채택 조건: Require a requested microscope/magnified view and verified sample identity. No ordinary-photo hard profile.

출처: [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer), [S22 NRCS Soil Health Management](https://www.nrcs.usda.gov/conservation-basics/soil/soil-health/soil-health-management)

출처 확인 범위: S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.; S22 [direct_text] 교란·피복·뿌리·식물 다양성과 관리 이력의 관계.

## E077 · 지렁이·굴 입구·분변토

생물과 그 흔적은 서로의 위치 관계를 함께 작성한다.

원 대화 범주: 19, 20 · 표현 방식: macro · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| earthworm | a segmented earthworm on a moist soil patch |
| burrow | a small burrow opening beside that same animal |
| cast | small coiled soil casts adjoining the opening |

관계: cast → adjoins → burrow

혼동 경계: 일반 흙덩이를 자동 분변토로 분류하지 않는다. 몸 마디가 없는 끈으로 지렁이를 대체하지 않는다.

프레이밍·배율·채택 조건: Frame the material and a same-plane scale; do not infer microscopic particles.

출처: [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer)

출처 확인 범위: S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.

## E078 · 개미·흰개미와 흙 구조물

굴과 구조물의 종·행동 해석에는 생물 식별 문맥이 필요하다.

원 대화 범주: 19 · 표현 방식: macro · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| ant | a resolved ant beside a soil nest opening |
| nest_opening | a bounded opening with loose grains around its rim |
| soil_grains | grains carried or displaced near that same opening |

관계: ant → adjoins → nest_opening

혼동 경계: 모든 흙무더기를 흰개미집으로 부르지 않는다. 흰개미 변형은 몸 구조와 출처를 별도로 조사한다.

프레이밍·배율·채택 조건: Frame the material and a same-plane scale; do not infer microscopic particles.

출처: [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer)

출처 확인 범위: S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.

## E079 · 톡토기·응애·노래기·지네의 배율

분류군별 외형과 먹이망 역할을 하나의 벌레로 통합하지 않는다.

원 대화 범주: 19 · 표현 방식: micro · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| arthropod | a resolved small arthropod on leaf litter |
| legs | visible appendages attached to that same body |
| scale_bar | a calibrated scale beside the organism |

관계: legs → attached_to → arthropod

혼동 경계: 서로 다른 다리 수·몸 구획을 공통 레시피로 만들지 않는다. 대형화는 요청된 초현실 변형에만 둔다.

프레이밍·배율·채택 조건: Require a requested microscope/magnified view and verified sample identity. No ordinary-photo hard profile.

출처: [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer)

출처 확인 범위: S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.

## E080 · 낙엽 분해와 숲바닥 피복

낙엽 형태의 잔존과 무너진 유기물 바탕을 함께 관찰한다.

원 대화 범주: 19, 20, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| litter | partly decomposed leaves still retaining some veins |
| organic_layer | dark broken organic fragments beneath those leaves |
| ground | a common forest-floor patch supporting both layers |

관계: litter → overlies → organic_layer

혼동 경계: 검은색만으로 분해 단계·부식 화학을 확정하지 않는다. 이끼 피복은 별도 재료/생물 변형이다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer), [S22 NRCS Soil Health Management](https://www.nrcs.usda.gov/conservation-basics/soil/soil-health/soil-health-management)

출처 확인 범위: S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.; S22 [direct_text] 교란·피복·뿌리·식물 다양성과 관리 이력의 관계.

## E081 · 잘린 흙벽의 뿌리 연결

노출 뿌리는 식물·흙벽·절단면의 연결로 표현한다.

원 대화 범주: 20, 29, 3 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| root | branching roots protruding from one cut soil wall |
| soil_wall | fine material continuing around the exposed roots |
| plant | a plant above connected to the larger root branches |

관계: root → connects → plant

혼동 경계: 갈라진 흙에 장식 끈을 얹는 것으로 대체하지 않는다. 뿌리털은 이 배율의 필수 요소가 아니다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S03 NRCS A Soil Profile](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/a-soil-profile), [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer)

출처 확인 범위: S03 [direct_text] 수직 층위·O A B C E R·보이는 성질과 덜 보이는 성질 구별.; S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.

## E082 · 경운의 이랑·도구·뒤집힌 흙

경운 흔적은 도구 방향과 뒤집힌 표토의 관계로 기술한다.

원 대화 범주: 20, 21 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| tool | a soil-turning tool engaging one field strip |
| furrow | a fresh furrow continuing behind the tool |
| turned_soil | turned clods deposited beside that same furrow |

관계: tool → forms → furrow

혼동 경계: 도로 차륜 홈·침식 수로와 구별한다. 경운을 건강한 토양의 자동 증거로 쓰지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S22 NRCS Soil Health Management](https://www.nrcs.usda.gov/conservation-basics/soil/soil-health/soil-health-management)

출처 확인 범위: S22 [direct_text] 교란·피복·뿌리·식물 다양성과 관리 이력의 관계.

## E083 · 무경운·피복작물·멀칭·윤작

현재 피복의 외형과 여러 해의 관리 이력은 다르다.

원 대화 범주: 20 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| residue | crop residues covering soil between living rows |
| seedling | seedlings emerging through that same residue layer |
| soil_patch | small uncovered soil patches between the residues |

관계: residue → covers → soil_patch

혼동 경계: 단일 사진으로 무경운·윤작 이력을 확정하지 않는다. 플라스틱 멀칭은 유기 피복과 별도 재료다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S22 NRCS Soil Health Management](https://www.nrcs.usda.gov/conservation-basics/soil/soil-health/soil-health-management)

출처 확인 범위: S22 [direct_text] 교란·피복·뿌리·식물 다양성과 관리 이력의 관계.

## E084 · 등고선 경작과 계단식 경작지

경사면에서 선의 방향과 단의 연속성을 관찰한다.

원 대화 범주: 20, 9 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| terraces | cultivated benches stepping down one hillside |
| riser | steep risers separating adjacent cultivated benches |
| crop_rows | crop rows following each bench rather than descending slope |

관계: riser → separates → terraces

혼동 경계: 하안단구·임의 곡선 무늬와 구별한다. 등고선 경작은 계단 구조 없이도 별도로 표현한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S22 NRCS Soil Health Management](https://www.nrcs.usda.gov/conservation-basics/soil/soil-health/soil-health-management), [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual)

출처 확인 범위: S22 [direct_text] 교란·피복·뿌리·식물 다양성과 관리 이력의 관계.; S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.

## E085 · 퇴비·부엽토·배양토·바이오차

배지와 토양 개량재의 재료·제조·용도는 별개다.

원 대화 범주: 20, 18 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| potting_mix | a documented growing mix with fibrous pieces and coarse inclusions |
| container | a plant container holding that same mix |
| plant | roots entering the mix inside the container |

관계: container → contains → potting_mix

혼동 경계: 모든 배양토에 광물성 흙을 강제하지 않는다. 검은 입자만으로 바이오차·비료 효능을 단정하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S17 NRCS Soil Biology Primer](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-biology-primer), [S22 NRCS Soil Health Management](https://www.nrcs.usda.gov/conservation-basics/soil/soil-health/soil-health-management)

출처 확인 범위: S17 [direct_text_scope] 먹이망과 세균·균류·선충·절지동물·지렁이의 분리. 종별 현미경 형태는 후속 전문 자료가 필요하다.; S22 [direct_text] 교란·피복·뿌리·식물 다양성과 관리 이력의 관계.

## E086 · 어도비 흙벽돌과 줄눈

전통 어도비는 가마에 굽지 않고 말린 흙벽돌이다.

원 대화 범주: 21 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| adobe_blocks | unfired earthen blocks laid in staggered courses |
| mortar | earthen joints visibly separating those blocks |
| broken_edge | a broken block edge showing granular fibrous material |

관계: mortar → between → adobe_blocks

혼동 경계: 갈색 소성벽돌·판축과 구별한다. 완성 미장면에서 숨은 벽돌 줄눈을 반드시 노출시키지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S23 NPS Preservation of Historic Adobe Buildings](https://www.nps.gov/orgs/1739/upload/preservation-brief-05-adobe.pdf)

출처 확인 범위: S23 [direct_pdf_text] 전통 어도비의 비소성·재료·흙 줄눈·목재 등과의 접합.

## E087 · 콥의 덩어리 흙벽과 섬유

콥은 덩어리 흙 배합물을 쌓는 건축 문맥이다.

원 대화 범주: 21 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| cob_wall | a continuous earthen wall with rounded irregular edges |
| fibre | fibres visible at a local damaged wall edge |
| wall_body | continuous material without modular brick joints |

관계: fibre → embedded_in → cob_wall

혼동 경계: 갈색 벽 전체로 콥을 확정하지 않는다. 지방·시대별 마감 차이를 보존한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S24 Getty Earthen Architecture](https://www.getty.edu/news/why-earthen-architecture-may-be-a-big-part-of-our-future/), [S25 Historic England Repairing Walls](https://historicengland.org.uk/advice/your-home/maintain-repair/walls/)

출처 확인 범위: S24 [direct_text] 어도비·판축·와틀 도브와 지역/문화별 건축 변형.; S25 [primary_search_excerpt] 목구조의 엮은 골격과 흙 채움, 콥 등 흙벽 및 보호 마감.

## E088 · 판축의 다짐층과 거푸집 흔적

판축은 거푸집 안의 층별 다짐 방식이다.

원 대화 범주: 21 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| rammed_wall | horizontal compacted lifts on one continuous earthen wall |
| formwork_mark | regular formwork impressions crossing those lifts |
| wall_edge | a wall edge showing continuous compacted material |

관계: formwork_mark → marks → rammed_wall

혼동 경계: 수평 띠만으로 판축을 확정하지 않는다. 퇴적 지층·콘크리트 판넬과 대조한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S24 Getty Earthen Architecture](https://www.getty.edu/news/why-earthen-architecture-may-be-a-big-part-of-our-future/), [S25 Historic England Repairing Walls](https://historicengland.org.uk/advice/your-home/maintain-repair/walls/)

출처 확인 범위: S24 [direct_text] 어도비·판축·와틀 도브와 지역/문화별 건축 변형.; S25 [primary_search_excerpt] 목구조의 엮은 골격과 흙 채움, 콥 등 흙벽 및 보호 마감.

## E089 · 와틀 앤드 도브의 골격과 흙

엮은 골격과 흙 배합물의 피복 관계가 핵심이다.

원 대화 범주: 21 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| wattle | woven rods exposed at a broken wall panel |
| daub | earthen daub adhering around the same woven rods |
| frame | a timber frame bounding the infilled panel |

관계: daub → coats → wattle

혼동 경계: 나무 위 갈색 페인트로 치환하지 않는다. 멀쩡한 완성 벽에 손상부를 강제로 추가하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S24 Getty Earthen Architecture](https://www.getty.edu/news/why-earthen-architecture-may-be-a-big-part-of-our-future/), [S25 Historic England Repairing Walls](https://historicengland.org.uk/advice/your-home/maintain-repair/walls/)

출처 확인 범위: S24 [direct_text] 어도비·판축·와틀 도브와 지역/문화별 건축 변형.; S25 [primary_search_excerpt] 목구조의 엮은 골격과 흙 채움, 콥 등 흙벽 및 보호 마감.

## E090 · 잔디집·흙지붕의 층과 지지부

식물 뿌리와 흙층·지지 구조의 결합을 표현한다.

원 대화 범주: 21, 20 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| sod | root-bound turf blocks at a documented wall edge |
| root_mat | dense roots holding the turf block together |
| support | a supporting structure beneath an earthen roof layer |

관계: root_mat → binds → sod

혼동 경계: 초록 지붕만으로 잔디집 구조를 확정하지 않는다. 실제 하중·방수 성능은 사진으로 평가하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S24 Getty Earthen Architecture](https://www.getty.edu/news/why-earthen-architecture-may-be-a-big-part-of-our-future/), [S25 Historic England Repairing Walls](https://historicengland.org.uk/advice/your-home/maintain-repair/walls/)

출처 확인 범위: S24 [direct_text] 어도비·판축·와틀 도브와 지역/문화별 건축 변형.; S25 [primary_search_excerpt] 목구조의 엮은 골격과 흙 채움, 콥 등 흙벽 및 보호 마감.

## E091 · 절토·성토·굴착·되메우기의 상태

파낸 면·쌓은 바탕·채운 공간을 서로 다른 상태로 둔다.

원 대화 범주: 21, 8 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| excavation | an open trench with exposed soil sides |
| spoil | a separate spoil pile beside that same trench |
| cut_face | a continuous cut face ending at the trench floor |

관계: spoil → beside → excavation

혼동 경계: 굴착=산사태·참호로 자동 치환하지 않는다. 되메우기는 채워진 공간의 별도 변형이다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S01 USDA NRCS Soil Survey Manual](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-survey-manual), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S01 [direct_page] 관찰·측정 절차의 범위; 2017판 안내. 전체 장을 전수 판독한 것은 아니다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E092 · 토루·제방·흙댐·토성·해자

흙 구조물의 재료 형태와 방어·차수 기능은 분리한다.

원 대화 범주: 21, 25, 10 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| earth_rampart | a long earthen embankment with a continuous crest |
| ditch | a parallel ditch on one side of the embankment |
| ground | the same ground plane joining embankment and ditch |

관계: ditch → adjoins → earth_rampart

혼동 경계: 토성의 토양 입경 의미와 구별한다. 마른 해자에 물을 자동 추가하지 않는다. 군사 구조의 시공법을 제공하는 데이터가 아니다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S07 NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm), [S23 NPS Preservation of Historic Adobe Buildings](https://www.nps.gov/orgs/1739/upload/preservation-brief-05-adobe.pdf), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S07 [direct_text] 유역·분수계·범람원·자연제방·곡류 및 망상 하천의 관계.; S23 [direct_pdf_text] 전통 어도비의 비소성·재료·흙 줄눈·목재 등과의 접합.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E093 · 물레의 젖은 태토와 슬립

슬립은 물속에 분산된 점토 배합물이다.

원 대화 범주: 22, 5 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| hands | two hands shaping one vessel on a pottery wheel |
| vessel | a wet clay vessel centred on that same wheel |
| slip | thin clay slurry deposited on fingers and wheel rim |

관계: hands → shape → vessel

혼동 경계: 물레 회전 자국과 몸 위 진흙을 혼동하지 않는다. 슬립은 액체 상태이고 소성 후 유약과 다르다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S21 V&A An A-Z of Ceramics](https://www.vam.ac.uk/articles/a-z-of-ceramics)

출처 확인 범위: S21 [primary_search_text_and_page] 슬립·몸체·유약·자기 관련 재료 구별. 모든 성형 방식의 작업 과정 자료는 아니다.

## E094 · 코일링·판 성형의 접합

띠를 쌓는 방식과 판을 붙이는 방식은 접합 방향이 다르다.

원 대화 범주: 22 · 표현 방식: direct · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| coil | a clay coil being joined to an existing vessel rim |
| vessel | previous coils forming the lower vessel wall |
| finger | a fingertip smoothing the junction on that same vessel |

관계: coil → joins → vessel

혼동 경계: 물레의 회전 줄무늬만으로 코일링을 확정하지 않는다. 판 성형은 판 모서리 접합을 별도 작성한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S21 V&A An A-Z of Ceramics](https://www.vam.ac.uk/articles/a-z-of-ceramics), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S21 [primary_search_text_and_page] 슬립·몸체·유약·자기 관련 재료 구별. 모든 성형 방식의 작업 과정 자료는 아니다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E095 · 가마 소성과 가소성의 동음 경계

소성 firing은 열처리이며 plasticity는 변형 성질이다.

원 대화 범주: 22, 5, 21 · 표현 방식: context · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| kiln | a documented kiln chamber containing ceramic pieces |
| shelf | shelves supporting those pieces inside the chamber |
| ceramic_piece | a separate ceramic object after the documented firing |

관계: shelf → supports → ceramic_piece

혼동 경계: 붉은 조명만으로 소성 온도·완료 상태를 주장하지 않는다. 단어 소성 하나로 가마 장면을 강제하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S21 V&A An A-Z of Ceramics](https://www.vam.ac.uk/articles/a-z-of-ceramics), [S23 NPS Preservation of Historic Adobe Buildings](https://www.nps.gov/orgs/1739/upload/preservation-brief-05-adobe.pdf)

출처 확인 범위: S21 [primary_search_text_and_page] 슬립·몸체·유약·자기 관련 재료 구별. 모든 성형 방식의 작업 과정 자료는 아니다.; S23 [direct_pdf_text] 전통 어도비의 비소성·재료·흙 줄눈·목재 등과의 접합.

## E096 · 테라코타·유약·석기·자기

몸체와 소성 상태·유리질 표면은 독립 재료 속성이다.

원 대화 범주: 22, 21 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| ceramic_body | an exposed matte terracotta body at an unglazed foot |
| glaze | a glossy glaze terminating above that foot |
| boundary | a visible edge separating glaze from the clay body |

관계: glaze → coats → ceramic_body

혼동 경계: 유광만으로 자기를 확정하지 않는다. 자기의 인칭·자기장 의미와 구별하고 석기는 석제 도구 의미와 분리한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S21 V&A An A-Z of Ceramics](https://www.vam.ac.uk/articles/a-z-of-ceramics)

출처 확인 범위: S21 [primary_search_text_and_page] 슬립·몸체·유약·자기 관련 재료 구별. 모든 성형 방식의 작업 과정 자료는 아니다.

## E097 · 오커·시에나·엄버의 재료와 색

흙 안료의 원료 이름과 색상군 이름은 분리한다.

원 대화 범주: 23, 4 · 표현 방식: named_context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| pigment | a mound of documented brown earth pigment powder |
| swatch | a bound paint swatch beside the loose powder |
| binder | a separate binder container adjoining the powder |

관계: pigment → beside → swatch

혼동 경계: 흙색 옷·주황 조명은 안료 실물의 증거가 아니다. 광물 조성·가열 이력은 색만으로 확정하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S27 MFA CAMEO Umber](https://cameo.mfa.org/wiki/Umber), [S28 MFA CAMEO Sienna](https://cameo.mfa.org/wiki/Sienna)

출처 확인 범위: S27 [direct_text] 엄버의 안료 재료·raw/burnt 차이. 색만으로 화학 조성을 판단하지 않는다.; S28 [blocked_403] 원 대화와 안료 계열의 추가 출처 단서. 시에나 세부 화학은 확인 미완료.

## E098 · 대지미술의 장소와 개입

대지미술은 장소·재료·예술가의 개입 문맥을 포함한다.

원 대화 범주: 22, 30 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| earthwork | a deliberate arrangement of earth and stones across a site |
| site | the surrounding landscape continuous with that arrangement |
| viewer_scale | a scale reference establishing the arrangement's site extent |

관계: earthwork → part_of → site

혼동 경계: 대지미술을 고정 나선 모양으로 정의하지 않는다. 우연한 흙무더기를 작품으로 확정하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S29 Dia Robert Smithson Spiral Jetty Publication](https://www.diaart.org/about/press/dia-art-foundation-and-the-university-of-california-press-publish-new-book-on-robert-smithsons-monumental-earthwork-spiral-jetty/type/text)

출처 확인 범위: S29 [primary_search_excerpt] 작품·영화·텍스트와 장소 관계. 모든 대지미술을 나선으로 일반화하지 않는다.

## E099 · 발굴 단면·유물의 제자리 관계

발굴은 층위와 물체 위치를 기록하는 조사 문맥이다.

원 대화 범주: 24, 3 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| baulk | a stratified excavation face beside a bounded grid |
| artifact | a pottery fragment partly embedded at one layer contact |
| scale_reference | a scale beside that same fragment and contact |

관계: artifact → embedded_in → baulk

혼동 경계: 주워 놓은 소품으로 제자리 유물 증거를 대신하지 않는다. 아래=항상 더 오래됨은 교란 문맥을 검토한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S30 한국학중앙연구원 한국민족문화대백과사전 무덤](https://encykorea.aks.ac.kr/Article/E0018983), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S30 [direct_text] 봉분·매장 공간·재료별 무덤의 구별. 범죄 사건 판단의 자료가 아니다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E100 · 봉분·토광·석실·부장품의 구별

무덤의 덮개·매장 공간·재료·부장 배치는 별도 단위다.

원 대화 범주: 24, 25 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| burial_mound | a rounded earthen mound in a documented cemetery |
| chamber | a separately documented stone chamber exposure |
| grave_goods | objects recorded within that chamber context |

관계: grave_goods → within → chamber

혼동 경계: 단일 사진에 닫힌 봉분과 내부 석실을 동시에 투시하지 않는다. 매장 埋藏·埋葬·상점 의미를 분리한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S30 한국학중앙연구원 한국민족문화대백과사전 무덤](https://encykorea.aks.ac.kr/Article/E0018983)

출처 확인 범위: S30 [direct_text] 봉분·매장 공간·재료별 무덤의 구별. 범죄 사건 판단의 자료가 아니다.

## E101 · 참호의 흙벽·바닥·통로

군사 참호는 방호·이동 문맥을 가진 지면 통로다.

원 대화 범주: 25, 21 · 표현 방식: direct · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| trench | a narrow recessed passage with continuous earthen walls |
| duckboard | wooden boards resting on the muddy passage floor |
| sandbag | sandbags placed along part of the upper trench edge |

관계: duckboard → rests_on → trench_floor

혼동 경계: 트렌치코트와 구별한다. 역사·지역·시기별 요소는 선택적이며 모든 참호에 덧붙이지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S31 IWM Voices of the First World War Trench Life](https://www.iwm.org.uk/podcasts/voices-of-the-first-world-war/ep-20-trench-life), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S31 [direct_fetch_failed] 원 대화의 역사 출처 단서. 장비·구조·시대별 세부는 후속 확인 대상으로 남긴다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E102 · 파괴 구덩이와 매몰 생활 흔적

구덩이 외형과 폭발·충돌·굴착 원인은 별도 의미다.

원 대화 범주: 25, 8, 28 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| crater | a ground depression with a disturbed raised rim |
| ejecta | displaced soil fragments adjoining that rim |
| object | a household object partly buried in nearby sediment |

관계: ejecta → adjoins → crater

혼동 경계: 정지 구덩이만으로 포탄 종류·폭발 원인·전쟁을 확정하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S16 USGS Effects of Earthquakes](https://www.usgs.gov/programs/earthquake-hazards/what-are-effects-earthquakes), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S16 [primary_search_excerpt] 낙석·사면 이동·액상화의 모래 분사·침하 등. 픽셀 진단 기준으로 쓰지 않는다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E103 · 지뢰·암매장·집단매장·생매장의 관찰 경계

은폐·범죄·살아 있음·피해 규모는 외형과 별개인 사건 문맥이다.

원 대화 범주: 25, 24 · 표현 방식: context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| buried_object | an object partially obscured by deposited soil |
| soil_cover | soil covering a clearly bounded part of that object |
| record | a separate scene narrative identifying the requested event |

관계: soil_cover → occludes → buried_object

혼동 경계: 평범한 흙을 지뢰·범죄 흔적으로 추정하지 않는다. 설치·은폐·실행 절차는 시각 의미 데이터에 포함하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S30 한국학중앙연구원 한국민족문화대백과사전 무덤](https://encykorea.aks.ac.kr/Article/E0018983), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S30 [direct_text] 봉분·매장 공간·재료별 무덤의 구별. 범죄 사건 판단의 자료가 아니다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E104 · 가이아·텔루스·게브·대지모신의 문화 문맥

대지 신격의 성별·재료·표상은 문화와 개별 자료에 따라 다르다.

원 대화 범주: 26, 30 · 표현 방식: context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| object_reference | a specific cited cultural object reference |
| iconographic_detail | a documented motif on that same object |
| catalogue | the object catalogue identifying place and period |

관계: catalogue → describes → object_reference

혼동 경계: 모든 대지 신을 흙 피부의 풍만한 여성으로 강제하지 않는다. 게브 자료의 거위 연관도 보편 외형으로 확대하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S43 Met Cosmetic Spoon 27.3.614](https://www.metmuseum.org/art/collection/search/552553), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S43 [direct_text] 거위와 게브의 연관을 신중하게 설명한 개별 소장품. 게브 신상의 보편적인 외형 자료는 아니다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E105 · 지신·터주·사직·지신밟기

땅·집터·곡식 의례와 농악 공연은 구별되는 문화 문맥이다.

원 대화 범주: 26, 20 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| performers | a named regional nongak group within a village yard |
| instruments | percussion instruments held by the same performers |
| yard | the ground of that yard continuous beneath the group |

관계: performers → stand_on → yard

혼동 경계: 땅을 밟는 동작 하나를 지신밟기로 확정하지 않는다. 사직은 사직 resignation 의미와 구별한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S33 국립국악원 지신밟기](https://www.gugak.go.kr/ency/topic/view/747), [S44 한국학중앙연구원 지신](https://encykorea.aks.ac.kr/Article/E0054279), [S45 한국학중앙연구원 사직](https://encykorea.aks.ac.kr/Article/E0025967)

출처 확인 범위: S33 [direct_text] 농악대·집/마을 의례·공동우물 등 지역별 진행 차이.; S44 [direct_text] 대지·토지의 신격이라는 정의와 터의 신앙 문맥.; S45 [direct_page_scope] 토지·곡식 의례의 출처 입구. 사직 resignation과 구별하기 위한 문맥 검토.

## E106 · 파차마마·아푸와 땅에 바치는 행위

안데스 자료의 봉헌·돌무더기·산신 문맥을 구체 사례로 유지한다.

원 대화 범주: 26, 16 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| offering | liquid poured from a vessel onto a bounded ground spot |
| vessel | a ceremonial vessel held above that same spot |
| cairn | a documented stone offering pile beside the ground spot |

관계: offering → contacts → ground_spot

혼동 경계: 모든 안데스 땅 장면에 같은 의례를 강제하지 않는다. 인카 ushnu 태양 제단과 파차마마 봉헌은 자료 맥락을 구별한다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S34 NMAI Inka Road Religion](https://americanindian.si.edu/inkaroad/inkauniverse/inkaroadexpansion/road-religion.html)

출처 확인 범위: S34 [direct_text] 파차마마 봉헌·아푸·apacheta와 us hnu의 자료별 맥락.

## E107 · 흙 골렘의 재료와 작용

골렘 전승과 선택한 흙 재질의 허구적 구현을 분리한다.

원 대화 범주: 26 · 표현 방식: reuse · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| golem | a constructed humanoid with a visibly earthen body |
| body_joint | lump-like articulated joints belonging to that body |
| material_trace | earthen crumbs beside a hand acting on one object |

관계: material_trace → originates_at → golem

혼동 경계: 기존 구성 재료·행위 프로필을 재사용한다. 돌 거인·살아 있는 갑옷과 재질만으로 동일시하지 않는다.

프레이밍·배율·채택 조건: Review the cited existing ID before adding any duplicate realization.

출처: [S32 Jewish Museum Berlin GOLEM](https://www.jmberlin.de/en/exhibition-golem), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S32 [direct_text] 전승과 다양한 현대 표상; 특정 흙 거인 외형을 보편 골렘 정의로 삼지 않는다.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E108 · 떠 있는 지층과 대지 마법

허구 물리와 실제 지질 작용은 명시적으로 구별한다.

원 대화 범주: 26, 30 · 표현 방식: fantasy · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| floating_block | a layered earth block separated from the ground |
| root | roots hanging from its exposed underside |
| ground_gap | a continuous air gap beneath the same block |

관계: root → hangs_from → floating_block

혼동 경계: 사진적 자연 설명으로 융기·섭입을 이 장면에 연결하지 않는다. 석화 저주는 선택한 변환 경계가 필요하다.

프레이밍·배율·채택 조건: Require explicit fictional physics and open concept scope.

출처: [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E109 · 피부 위 진흙의 부착과 접촉 흔적

피부와 진흙은 경계·두께·접촉 흔적으로 구별한다.

원 대화 범주: 27, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| skin | visible bare skin adjoining a local mud coating |
| mud_coat | a thick mud patch adhering to that same skin |
| finger_track | a dragged fingertip track crossing the coating edge |

관계: mud_coat → adheres_to → skin

혼동 경계: 노동·놀이·의례·패션·페티시 문맥을 외형만으로 결정하지 않는다. 피부 색을 흙 색으로 바꾸지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E110 · 옷에 묻은 진흙과 젖은 천

고형 부착물과 천의 수분 변화는 서로 다른 표면 효과다.

원 대화 범주: 27, 29 · 표현 방식: direct · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| garment | an opaque garment retaining its original seams |
| mud_deposit | raised muddy clumps attached near the garment hem |
| stain_edge | a bounded deposit edge contrasting with nearby clean fabric |

관계: mud_deposit → adheres_to → garment

혼동 경계: 진흙·젖음으로 의복 투명화·노출·소재 변경을 자동 허용하지 않는다. 물 후보의 광학 관계와 경계를 유지한다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E111 · 머드팩·목욕·놀이·레슬링의 목적 문맥

비슷한 진흙 접촉 외형이라도 장면의 목적은 다르다.

원 대화 범주: 27 · 표현 방식: context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| mud | mud contacting a clearly identified skin patch |
| tool | an applicator or play object belonging to the chosen scene |
| setting | a setting consistent with the separately stated activity |

관계: tool → contacts → mud

혼동 경계: 머드팩의 미용 효능·머드놀이의 성적 의미·레슬링의 의도를 외형으로 확정하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E112 · WAM·스플로싱·머드 페티시

원 대화의 하위문화 용어는 명시된 취향 문맥으로 보존한다.

원 대화 범주: 27 · 표현 방식: context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| mud_coat | a local mud coating with a visible material boundary |
| gesture | a hand contacting that same coating |
| garment | the requested garment structure retained beside the contact |

관계: gesture → contacts → mud_coat

혼동 경계: 용어의 1차 자료 검증은 미완료다. 일반 splosh 동사·비성적 진흙 접촉을 취향 표기로 승격하지 않는다. 동의·흥분은 픽셀로 판단하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E113 · 흙냄새·페트리코·지오스민

비와 지표의 접촉은 냄새 성분을 공기로 옮기는 과정과 관련된다.

원 대화 범주: 27 · 표현 방식: context · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| raindrop | a raindrop contacting a previously dry soil patch |
| wet_patch | a local wet patch around that same contact |
| plant | nearby vegetation retained in the scene context |

관계: raindrop → contacts → wet_patch

혼동 경계: 냄새를 갈색 연기·녹색 발광으로 고정하지 않는다. 지오스민 분자·페트리코의 향은 실제 사진 gate로 삼지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S26 MIT Rainfall Can Release Aerosols](https://news.mit.edu/2015/rainfall-can-release-aerosols-0114)

출처 확인 범위: S26 [direct_text] 빗방울 접촉과 에어로졸 이동 연구; 냄새의 가시적 실체를 주장하지 않는다.

## E114 · 식토 토성·지오파지 식토의 동음 경계

점토 함량의 토성 말과 흙을 먹는 행위는 다른 뜻이다.

원 대화 범주: 27, 2 · 표현 방식: context · 우선순위: P0

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| clay_sample | a separately identified clay-rich soil specimen |
| context_record | a record stating material classification or consumption context |
| scene_subject | the explicitly requested actor kept separate from specimen identity |

관계: context_record → describes → clay_sample

혼동 경계: 흙을 만지는 손을 섭취 장면으로 바꾸지 않는다. 영양·치료 효능이나 건강 상태를 외형으로 주장하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S35 NRCS Rangeland Ecohydrology Soil Particle Size](https://directives.nrcs.usda.gov/sites/default/files2/1712930384/33921.pdf), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S35 [primary_search_excerpt] USDA 입경 수치와 육안으로 구분 가능한 입경의 한계.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E115 · 달 레골리스의 표면과 발자국

달 표면 재료와 지구의 생물성 토양은 환경이 다르다.

원 대화 범주: 28, 2 · 표현 방식: direct · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| regolith | a grey granular regolith bed around one bootprint |
| bootprint | sharp tread impressions pressed into that same bed |
| rock_fragment | small angular rock fragments beside the impression |

관계: bootprint → within → regolith

혼동 경계: 회색 흙만으로 달 위치를 증명하지 않는다. 바람에 떠다니는 먼지·낙엽·유기 뿌리를 자동 추가하지 않는다.

프레이밍·배율·채택 조건: Use only after contextual owner binding and explicit optional adoption or a complete requester proposition.

출처: [S41 NASA What Is Lunar Regolith](https://science.nasa.gov/biological-physical/what-is-lunar-regolith/)

출처 확인 범위: S41 [direct_text] 각진 표면 재료·발자국·자원 이용 연구. 본문의 지구 토양 단순화는 S01/S03으로 교차 해석한다.

## E116 · 충돌구와 분출물의 원인 경계

원인 이름과 오목한 지형·주변 분출물의 외형은 분리한다.

원 대화 범주: 28, 25 · 표현 방식: named_context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| impact_crater | a bounded crater with a continuous raised rim |
| ejecta | a radial rough deposit extending beyond that rim |
| terrain | surrounding terrain continuous with the crater exterior |

관계: ejecta → surrounds → impact_crater

혼동 경계: 화산 분화구·포탄 구덩이·싱크홀과 구별한다. 정지 외형으로 충돌체·연대를 확정하지 않는다.

프레이밍·배율·채택 조건: Visible form is optional; cause/classification/culture/time requires separately grounded context.

출처: [S41 NASA What Is Lunar Regolith](https://science.nasa.gov/biological-physical/what-is-lunar-regolith/), [S42 NASA Moon Composition](https://science.nasa.gov/moon/composition/)

출처 확인 범위: S41 [direct_text] 각진 표면 재료·발자국·자원 이용 연구. 본문의 지구 토양 단순화는 S01/S03으로 교차 해석한다.; S42 [direct_text_and_primary_search] 암편·광물편·유리·어글루티네이트 및 입경/발생 환경의 차이.

## E117 · 충돌 유리와 어글루티네이트의 배율

어글루티네이트는 유리질 결합을 가진 입자라는 재료 문맥이다.

원 대화 범주: 28, 17 · 표현 방식: micro · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| grain | an identified agglutinate grain under microscopy |
| glass_binding | glass-like material connecting fragments within that grain |
| scale_bar | a calibrated microscopic scale adjoining the grain |

관계: glass_binding → binds → grain

혼동 경계: 달 풍경의 거대한 유리 구슬·반짝이로 대신하지 않는다. 미세 재료 정체는 검증 시료 문맥이 필요하다.

프레이밍·배율·채택 조건: Require a requested microscope/magnified view and verified sample identity. No ordinary-photo hard profile.

출처: [S42 NASA Moon Composition](https://science.nasa.gov/moon/composition/)

출처 확인 범위: S42 [direct_text_and_primary_search] 암편·광물편·유리·어글루티네이트 및 입경/발생 환경의 차이.

## E118 · 레골리스 모사토와 현지자원활용

모사 재료·실제 천체 시료·장비 용도는 별도 식별한다.

원 대화 범주: 28, 18 · 표현 방식: context · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| sample | a labelled regolith simulant container |
| apparatus | a documented processing apparatus adjoining that container |
| output | a separately identified processed specimen |

관계: apparatus → uses → sample

혼동 경계: 지구 실험실 시료를 실제 달 시료로 주장하지 않는다. ISRU 기술 가능성과 실제 운용 성공은 사진으로 확정하지 않는다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S41 NASA What Is Lunar Regolith](https://science.nasa.gov/biological-physical/what-is-lunar-regolith/), [S42 NASA Moon Composition](https://science.nasa.gov/moon/composition/)

출처 확인 범위: S41 [direct_text] 각진 표면 재료·발자국·자원 이용 연구. 본문의 지구 토양 단순화는 S01/S03으로 교차 해석한다.; S42 [direct_text_and_primary_search] 암편·광물편·유리·어글루티네이트 및 입경/발생 환경의 차이.

## E119 · 고향·죽음·기억·금기·뿌리내림

비유는 장면 의미를 열어두며 보편적인 물체 레시피가 아니다.

원 대화 범주: 30, 1, 24 · 표현 방식: symbolic · 우선순위: P2

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| hand | a hand holding a bounded amount of soil |
| place | a separately stated meaningful place in the frame |
| gesture | a visible gesture directed toward that held soil |

관계: gesture → directed_at → hand

혼동 경계: 흙으로 돌아가다를 즉시 시신·무덤으로, 뿌리내리다를 몸의 실제 뿌리로 강제하지 않는다. 소속감은 픽셀에서 확정하지 않는다.

프레이밍·배율·채택 조건: Retain authored emotional context; never turn metaphor into an automatic object recipe.

출처: [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

## E120 · 풍요·척박함·생장 관계의 선택적 표현

생장 외형과 비옥도·정서·토양 건강 진단은 구별한다.

원 대화 범주: 20, 29, 30 · 표현 방식: context · 우선순위: P1

| 소유 대상 | 선택한 관찰 표현 |
|---|---|
| seedling | a seedling emerging from one crumbly soil patch |
| root | roots entering that same patch at a visible edge |
| soil | granular soil supporting the stem at its base |

관계: root → penetrates → soil

혼동 경계: 새싹·검은 흙만으로 비옥도·재생·희망을 증명하지 않는다. 인간의 반응은 배우·대상·행위·감정·결과를 별도 작성한다.

프레이밍·배율·채택 조건: Retain named context; components are optional bridges, not required evidence of the abstract term.

출처: [S22 NRCS Soil Health Management](https://www.nrcs.usda.gov/conservation-basics/soil/soil-health/soil-health-management), [S40 흙 관련 용어 조사 및 이번 저작 제안](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)

출처 확인 범위: S22 [direct_text] 교란·피복·뿌리·식물 다양성과 관리 이력의 관계.; S40 [user_referenced_conversation_not_primary_fact] 용어 범위와 창작 관계의 출발점. 전문 사실·성적 하위문화 정의·특정 문화 외형을 검증하는 출처로 취급하지 않는다.

