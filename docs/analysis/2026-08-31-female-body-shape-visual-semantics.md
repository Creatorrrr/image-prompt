# 여성 체형 표현의 시각 의미·후보팩 강화 리서치

검토일: 2026-08-31  
적용 범위: `photo-prompt-image-generator`의 성인 인물 사진 프롬프트  
핵심 원칙: 체형 명칭은 사람의 가치·건강·매력·체중을 판정하는 라벨이 아니라, 촬영 조건 아래 관찰 가능한 여러 신체 구간의 상대 관계로 번역한다.

## 1. 결론

여성 체형 표현은 하나의 단어를 하나의 고정 실루엣으로 바꾸는 방식으로는 안정적으로 표현할 수 없다. 같은 `curvy`라도 가슴 돌출, 자연 허리 함몰, 골반 폭, 둔부 돌출, 허벅지 볼륨이 서로 독립적으로 달라질 수 있고, `petite`는 작은 신장·프레임을 뜻할 수 있지만 `slender`와 동일하지 않다. 따라서 데이터 모델은 다음 세 층으로 나눈다.

1. **전역 체형 관계**: slender, soft full, curvilinear, toned muscular.
2. **지역 해부·볼륨 관계**: 어깨·흉곽, 가슴-흉곽, 자연 허리, 골반, 하이힙, 둔부, 허벅지, 중앙 복부의 폭과 깊이.
3. **관찰 계약**: 정면 또는 완만한 사선, 양측 외곽선, 머리부터 발까지의 전신, 정면 폭과 시상면 깊이, 의복·자세·렌즈의 별도 소유권.

FFIT의 9형 명칭은 검색과 사용자 언어를 보존하는 입구로만 사용한다. 런타임 하드 의무는 `상·하체 우세`, `자연 허리 함몰`, `하이힙의 빠른 전환`, `중앙 몸통 최대 폭·깊이와 양방향 테이퍼`처럼 화면에서 확인할 수 있는 관계로 구성한다.

## 2. 근거와 적용 경계

| 근거 | 이 프로젝트에 가져온 것 | 가져오지 않은 것 |
|---|---|---|
| [FFIT Part I](https://www.researchgate.net/publication/286985579_Female_Figure_Identification_Technique_FFIT_for_apparel_part_I_Describing_female_shapes) | hourglass, top/bottom hourglass, spoon, triangle, inverted triangle, rectangle, oval, diamond의 지역 비교 축 | 논문의 수치 임계값, 보편적 체형 판정, 선호도 |
| [FFIT 신뢰성 재평가](https://repository.mmu.ac.uk/articles/journal_contribution/Assessing_the_female_figure_identification_technique_s_reliability_as_a_body_shape_classification_system/32460303) | 측정 위치에 따른 불안정성, 어깨 측정 누락, 숫자 대신 랜드마크와 불확실성 명시 | 하나의 “정답” 측정법. 연구에서는 측정 위치에 따라 분류가 최대 40% 달라졌다 |
| [한국 성인 여성 3D 체형 연구](https://pmc.ncbi.nlm.nih.gov/articles/PMC13392141/) | 가슴-골반, 골반-허리, 정면 폭-깊이를 분리하는 다차원 축 | 815명 표본의 군집을 모든 한국인 또는 생성 이미지에 일반화 |
| [미국·한국 여성 체형 비교](https://www.emerald.com/ijcst/article-abstract/19/5/374/124961/Comparison-of-body-shape-between-USA-and-Korean) | 표본·집단에 따라 분포와 비례가 달라진다는 경계 | 민족이나 국적에서 개인 체형을 추정하는 기본값 |
| [Cambridge: slender](https://dictionary.cambridge.org/us/dictionary/english/slender), [curvy](https://dictionary.cambridge.org/us/dictionary/english/curvy), [full-figured](https://dictionary.cambridge.org/us/dictionary/english/full-figured), [toned](https://dictionary.cambridge.org/us/dictionary/english/toned), [busty](https://dictionary.cambridge.org/us/dictionary/english/busty) | 일반어의 최소 의미와 동음이의어 경계 | 매력·건강·체지방·운동 능력 같은 비가시적 함의 |
| [Cambridge: petite](https://dictionary.cambridge.org/us/dictionary/english/petite), [willowy](https://dictionary.cambridge.org/us/dictionary/english/willowy), [statuesque](https://dictionary.cambridge.org/us/dictionary/english/statuesque) | 신장, 프레임, 세로 비례, 체적을 분리한 후보 원자 | bare term에서 자동으로 하드 체형 의무를 만드는 것 |
| [표준국어대사전: 글래머](https://stdict.korean.go.kr/search/searchResult.do?pageSize=10&searchKeyword=%EA%B8%80%EB%9E%98%EB%A8%B8) | 한국어에서 몸의 풍만함과 성적 매력 평가가 결합된다는 혼동 경계 | `글래머`를 영어 glamour 사진 스타일이나 단일 해부학으로 등치 |

이 자료들은 “어떤 체형이 더 낫다”를 지지하지 않는다. 프로젝트가 채택한 것은 명칭의 구성 요소와 분류 불확실성뿐이다. 생성된 한 장의 사진은 신장, 몸무게, 의복 사이즈, 체지방률, 건강, 임신, 병리, 생식력, 민족을 검증할 수 없다.

## 3. 시각 의미 축

| 축 | 관찰 가능한 최소 증거 | 분리해야 하는 소유자 |
|---|---|---|
| 신장·세로 비례 | 머리부터 양발, 어깨-골반 몸통 구간, 골반-바닥 다리 구간 | 신발 굽, 카메라 높이, 원근, 크롭 |
| 프레임 | 어깨·흉곽의 폭, 장골 부근 골반 폭 | 근육·가슴·바깥 엉덩이 연부조직, 패드, 자세 |
| 연부조직 체적 | 몸통·위팔·골반·허벅지 여러 구간의 연속적 볼륨 | 의복 패딩, 한 부위만의 확대, 체중·건강 |
| 근육 정의 | 어깨·팔·몸통·대퇴·종아리의 면과 힘줄 전환 | 색 보정, 강한 그림자, 운동 장비, 경기력 |
| 가슴 | 양측 볼륨의 흉곽 기준 앞·옆 돌출, 자연 허리와의 관계 | 푸시업·패딩, cleavage만의 노출, 전신 실루엣 |
| 자연 허리 | 상체에서 허리로 들어오는 양측 전환과 다시 골반으로 나가는 전환 | 벨트·코르셋, 몸통 비틀기, 한쪽만 보이는 사선 |
| 골반·하이힙 | 골격 폭, 자연 허리 직하부의 빠른 돌출, 바깥 엉덩이 | 힙딥, 허리밴드 압박, 스커트 플레어 |
| 둔부·허벅지 | 골반 기준 후방 돌출, 골반-무릎의 바깥 윤곽 연속성 | 요추 자세, 의복 압박, 발 벌림 |
| 중앙 몸통 | 흉곽과 골반 사이 복부·허리의 정면 폭과 시상면 깊이 | 임신·병리·체중·건강 추정, 전면 의복 돌출 |

## 4. 키워드 분해와 혼동 경계

| 사용자 키워드 | 하드 프로필/후보 번역 | 반드시 구분할 것 |
|---|---|---|
| slender, 슬렌더 | 몸통·팔다리의 좁은 가로 체적 | tall, willowy, toned, underweight와 동일하지 않음 |
| slim, lean | 범용 하드 라벨 대신 좁은 체적·절제된 근육 면을 필요한 축으로 선택 | slim은 의복 핏, lean은 체지방·근육 함의를 섞을 수 있음 |
| toned, athletic | 여러 구간의 절제된 근육·힘줄 면 | 경기 종목, 실력, 힘, 건강, 체지방률 |
| muscular | toned과 같은 축이지만 근육 체적·선명도를 별도로 요청 가능 | 남성성·힘·운동 능력 추정 |
| curvy, 글래머 체형 | 상체-허리-골반-허벅지의 여러 안팎 곡선 전환 | busty, hourglass, full-figured와 자동 등치하지 않음 |
| voluptuous, full-figured, 풍만, 육덕진 체형 | 여러 구간의 연속적인 연부조직 체적 | 특정 허리형, 의복 사이즈, 체중, 매력·성적 가용성 |
| busty, large-busted, 거유 체형 | 흉곽 기준 양측 가슴 돌출과 자연 허리 관계 | curvy/hourglass 전신형, 조각 bust, 브라 사이즈 표 |
| petite | 작은 신장·작은 프레임 후보의 조합 | slender, 어려 보임, 미성년, petite 의류 사이즈 |
| willowy | 긴 팔다리·큰 세로 비례 + 좁은 체형 후보 | graceful/attractive 성격 평가, 단순 tall |
| statuesque | 큰 신장 + 비교적 큰 프레임·체적 후보 | 카메라 저각의 웅장함, attractive/impressive 평가 |
| hourglass | 상·하부 확장 + 상대적으로 좁은 자연 허리 | 벨트/코르셋, 고정 비율, top/bottom 변형 |
| top hourglass | hourglass의 모든 증거 + 상부 우세 | busty alone, waist가 약한 inverted triangle |
| bottom hourglass | hourglass의 모든 증거 + 하부 우세 | triangle처럼 상부 확장이 거의 없는 경우 |
| pear/triangle | 어깨·흉곽보다 골반·바깥 엉덩이·상부 허벅지 우세 | spoon의 빠른 하이힙 전환은 필수 아님 |
| spoon | 자연 허리 바로 아래 하이힙의 빠른 바깥 전환 + 하체 연속성 | gradual pear, hip dip만 보이는 경우 |
| rectangle | 상체-허리-골반 폭 변화가 작고 허리 함몰이 약함 | 직선 의복, 문자 그대로의 사각형, 정확히 같은 폭 |
| inverted triangle | 어깨·흉곽 등 명시한 상부 소유자가 골반보다 넓음 | busty alone, top hourglass, 어깨 패드·저각 |
| oval/apple | 중앙 복부·허리의 둥근 폭/깊이 + 약한 허리 함몰 | 임신·병리·체중 추정, oval face/mirror, 사과 정물 |
| diamond | 중앙 몸통 최대 폭/깊이 + 상·하 양방향 테이퍼 | oval의 완만한 둥근 전환, 보석·패턴 |

## 5. 한국어 인터넷·커뮤니티 표현의 처리

다음 표현은 사용자가 직접 정의하지 않는 한 하드 프로필로 만들지 않는다.

- `S라인`, `콜라병 몸매`, `개미허리`: 허리·상하체 관계, 자세, 의복 조임, 매력 평가가 섞인다. 필요한 경우 `hourglass` 구성 요소로 재확인한다.
- `골반 미인`: 골격 폭, 바깥 엉덩이 연부조직, 둔부 돌출, 미적 판단이 섞인다. `wide pelvic frame`, `outer-hip volume`, `gluteal projection`을 별도 후보로 제공한다.
- `베이글녀`: 얼굴의 나이 인상과 성인 몸의 성적 평가를 결합한다. 미성년 오인과 가치 판단 위험 때문에 자동 체형 라우팅에 사용하지 않는다.
- `BBW`, `plus-size`: 커뮤니티 정체성 또는 의류 사이즈 체계와 연결되며 시각적 임계값이 없다. `soft full figure volume`과 동일한 하드 동의어로 만들지 않는다.
- bare `글래머`: 한국어 체형 평가와 영어 glamour 사진 스타일이 충돌한다. `글래머 체형`처럼 성인 체형 문맥이 명시된 경우에만 curvilinear 관계를 활성화하고, 런타임 문장은 중립 정의를 사용한다.

## 6. 데이터 반영

### 하드 시각 프로필

- 전역 체형 4개: `slender_linear_build`, `soft_full_figure_volume`, `curvilinear_figure_relation`, `toned_muscular_build`.
- 지역 관계 1개: `bust_prominence_relation`.
- 실루엣 변형 8개: top/bottom hourglass, triangle, spoon, rectangle, inverted triangle, oval, diamond.
- 기존 `hourglass_silhouette_relation`에는 top/bottom 표현을 제외어로 추가해 두 프로필이 동시에 하드 활성화되지 않게 한다.

모든 새 하드 프로필은 다음을 공통으로 요구한다.

1. 명시적인 성인 문맥.
2. 최소 4개의 구성 요소 그룹.
3. 최소 4개의 프롬프트 증거 필드와 렌더 게이트.
4. 의복, 자세, 시점, 렌즈, 값 판단을 대체 증거에서 제외.

### 후보팩

- `silhouette_proportion`: 전역 체형, 세로 비례, 몸통-다리 비례, FFIT 관계.
- `anatomical_connection`: 가슴-흉곽, 가슴-허리, 어깨·흉곽 프레임, 골반 프레임, 둔부·허벅지, 중앙 복부 관계.
- `body_framing`: 양측 몸통, 전신 세로 비례, 가슴-흉곽-허리, 골반-둔부-허벅지, 중앙 몸통 폭·깊이를 실제로 볼 수 있는 촬영 계약.

`petite`, `willowy`, `statuesque`, 긴/짧은 몸통·다리 관계는 후보 원자로 제공하지만 bare term을 하드 프로필로 만들지 않는다. 검색 추천은 가능하되 사용자의 명시적 선택이나 구성 요소 증거 없이 필수 렌더 의무로 승격하지 않는다.

## 7. 검증 기준

구조 검증과 픽셀 검증을 구분한다.

- **구조·라우팅**: 성인 문맥이 있는 exact term만 하드 프로필을 활성화하는지, `busty != curvy`, `petite != slender`, `pear != spoon`, `athletic competition != toned`, top/bottom hourglass가 기본 hourglass와 중복되지 않는지 테스트한다.
- **후보 결합**: 모든 근거 행의 candidate id가 실제 슬롯에 존재하는지, 인덱스가 현재 레지스트리 해시와 일치하는지 검사한다.
- **렌더 픽셀**: 이번 변경은 이미지 생성을 수행하지 않는다. render gate는 향후 한 장의 저장 이미지마다 thumbnail/native에서 모두 판정해야 하며, 프롬프트에 문구가 있다는 사실만으로 통과시킬 수 없다.
- **사용자 판단**: 표현의 적합성과 선호는 구조·검색·픽셀 판정과 별도다. 사용자의 승인 전에는 “원하는 체형 표현을 달성했다”고 주장하지 않는다.

