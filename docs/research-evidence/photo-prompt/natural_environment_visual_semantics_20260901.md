# 자연환경 시각 의미·후보팩 강화 리서치

- 조사일: 2026-09-01
- 입력: ChatGPT 대화 `자연환경 용어 조사`에서 정리한 지권·수권·대기권·생물권·빙권, 생태계, 전이지대, 자연현상, 시간·계절·광선·질감 어휘
- 적용 대상: `photo-prompt-image-generator`의 후보팩과 시각 의무 프로필
- 적용 원칙: 넓은 자연어 사전을 그대로 추가하지 않고, 정지 이미지에서 서로 구별할 수 있는 **구성요소 + 공간 순서 + 물질 접촉 + 원인·결과 흔적**으로 축약한다.

## 1. 결론

이번 조사에서는 자연환경을 단순한 장소명이나 분위기 태그가 아니라, 한 장면 안에서 관찰 가능한 관계 문법으로 재구성했다.

- 12개 환경 문법을 후보팩에 추가했다.
- 12개 문법을 7개 슬롯의 75개 후보로 분해했다.
  - `aesthetic_trend` 12
  - `subject` 12
  - `action` 12
  - `location` 12
  - `surface_material` 11
  - `composition` 12
  - `weather` 4
- 그중 정지 이미지 한 장에서 핵심 구성요소와 순서를 비교적 안정적으로 검증할 수 있는 8개만 하드 시각 프로필로 승격했다.
- 나머지 4개는 후보팩과 소프트 라우팅에는 포함하지만, 보이지 않는 연결·과정·생태 기능을 이미지가 증명한 것처럼 판정하지 않도록 하드 프로필에서는 제외했다.
- `forest`, `wetland`, `glacier`, `storm`, `reef`, `nature` 같은 넓은 단어는 새 하드 프로필이나 새 믹스인을 자동으로 켜지 않는다. 하드 활성화는 연구된 좁은 구문으로 제한한다.

## 2. 추상화 방법

원 대화의 용어는 다음 네 층으로 분리했다.

1. **개체**: 나무, 물, 암석, 얼음, 구름처럼 화면에 나타날 수 있는 대상
2. **구조**: 층, 띠, 경사, 경계, 네트워크처럼 대상들이 차지하는 공간 관계
3. **과정 흔적**: 침식·퇴적·포화·유동·노출처럼 물질 상태나 배열에 남은 결과
4. **맥락 주장**: 나이, 유량, 화학 조성, 법적 분류, 장기 변화, 생태 기능처럼 한 프레임만으로는 확정할 수 없는 사실

후보팩은 1~3층을 표현할 수 있지만, 하드 픽셀 판정은 반드시 복수의 구성요소와 그 관계가 함께 보여야 한다. 4층은 프롬프트의 배경 설명으로 사용할 수 있어도 픽셀 통과 조건으로 삼지 않는다.

## 3. 환경 문법 선정표

| 문법 | 한 프레임의 핵심 관찰 관계 | 주요 혼동 대체물 | 하드 프로필 |
|---|---|---|---|
| 노령림 구조 | 서로 다른 크기의 살아 있는 나무 + 다층 수관 + 선 고사목 + 굵은 쓰러진 목재 | 균일 조림지, 큰 나무 한 그루, 단순한 울창함 | 예 |
| 습지 수문 모자이크 | 얕은 물/포화지 + 물에 의해 드러난 토양 + 습생 식생 + 젖고 덜 젖은 미세지형 | 연못 가장자리 갈대, 물웅덩이, 침수 잔디밭 | 예 |
| 하천변 범람원 구배 | 활동 하도 + 신선한 퇴적지 + 범람원 단 + 더 건조한 상부와 식생 변화 | 단순 강변 풍경, 제방 공원, 범람 흔적 없는 숲 | 아니오 |
| 조간대 수직 대상 | 마른 상부 비말대 → 교대 노출 중부대 → 젖은 하부대 → 현재 수면의 연속 순서 | 바위 해변, 조수 웅덩이 클로즈업, 색 띠 | 예 |
| 카르스트 배수 지형 | 용식 암반 + 폐쇄 함몰지 + 물이 들어가는 소실점 + 떨어진 용출점 | 동굴 내부, 채석장, 분화구, 가려진 하천 | 예 |
| 활동 빙하 지형 | U자 계곡의 연속 빙체 + 유동 방향 표면 + 빙퇴석 접촉 + 말단 융빙수 | 설산, 결빙호, 얼음 동굴 | 예 |
| 풍성사구 구조 | 완만한 바람받이 사면 + 마루 + 급한 미끄럼면 + 정렬된 잔물결 | 대칭 모래더미, 평면 모래무늬, 먼지 구름 | 예 |
| 화산 열수지대 | 균열 분기공 + 국지 수증기 + 변질 지면 + 광물 침전 또는 끓는 물 | 안개 낀 화산, 연막, 일반 온천 | 아니오 |
| 적란운 구조 | 어두운 밑면 + 깊은 대류탑 + 섬유상 모루 + 강수/미류 기둥 | 먹구름, 번개 합성, 연기 기둥 | 예 |
| 고산 수목한계 전이지대 | 하부 닫힌 숲 → 키 작고 듬성한 나무 → 왜성·편향 수목 → 무수목 고산대 | 나무 한 그루, 벌목선, 적설선 | 예 |
| 맹그로브 조석 뿌리 체계 | 조석 수면 + 뿌리 네트워크 + 뿌리 사이 세립 퇴적물 + 수관 연결 | 물가 나무, 늪의 일반 뿌리, 침수된 숲 | 아니오 |
| 산호초 횡단 대상 | 얕은 리프 플랫 → 파랑이 깨지는 크레스트 → 깊어지는 포어리프 | 임의의 산호 정원, 얕은 라군, 수족관 | 아니오 |

## 4. 하드 시각 프로필 8종

### 4.1 노령림 구조

미국 산림청 자료는 노령림의 반복 가능한 구조 축으로 큰 살아 있는 나무, 큰 선 고사목, 큰 쓰러진 목재, 다양한 나무 크기와 여러 수관층을 제시한다. 따라서 `오래된`, `원시`, `보호된` 같은 상태 단어가 아니라 네 가지 구조의 동시 가시성을 요구한다.

- 필수: 크기가 다른 생목 군집, 상·중·하층 수관, 선 고사목, 바닥과 접촉한 큰 쓰러진 목재
- 거부: 균일한 줄기 간격과 크기의 조림지, 거목 한 그루, 고사목만 있는 숲
- 비추론: 실제 임령, 생태적 연속성, 보호구역 여부, 서식처 품질

### 4.2 습지 수문·토양·식생 모자이크

미국 환경보호청은 물의 존재가 습지 토양과 식생을 규정한다고 설명한다. 이 정의를 픽셀 문법으로 바꿀 때는 물만 있는 연못이 아니라, 연결된 저지대의 얕은 물/포화, 노출된 진흙 또는 포화 토양, 그 기질에서 자라는 습생 식생, 미세한 고저에 따른 젖음 모자이크가 함께 필요하다.

- 필수: 얕은 침수 또는 포화, 포화 토양, 습생 식생의 기질 접촉, 습·건 미세지형
- 거부: 장식 연못, 갈대 한 무리, 반사로 푸르게 보이는 마른 초지
- 비추론: 법적 습지 경계, 수문기간, 토양 화학, 지역별 식물 동정

### 4.3 조간대 수직 대상

미국 해양대기청은 조간대를 만조선과 간조선 사이로 설명하고 비말대·고조대·중조대·저조대의 노출 차이를 구분한다. 따라서 색이 다른 수평 띠가 아니라 현재 수면에서 위쪽 해안까지 이어지는 고도 순서, 젖음 차이, 웅덩이와 부착 생물 피복 변화가 필요하다.

- 필수: 상대적으로 마른 상부, 교대 노출 중부, 젖고 피복이 조밀한 하부, 하나의 연속 고도 순서
- 거부: 바위 해변 전경, 웅덩이 하나, 페인트 같은 색 띠
- 비추론: 정확한 조석고, 종 동정, 노출 시간

### 4.4 카르스트 지표·지하 배수

미국 지질조사국은 석회암·백운암 등의 용식으로 폐쇄 함몰지, 소실 하천, 지하 배수, 샘이 형성될 수 있음을 설명한다. 화면은 지하 연결 자체를 볼 수 없으므로, 용식된 암반 지형과 소실점·용출점이라는 두 표면 단서를 동시에 제시하되 그 사이의 실제 수리 연결은 증명하지 않는다.

- 필수: 용식·절리 암반, 표면 출구가 없는 함몰지, 하천의 명확한 진입점, 떨어진 샘 또는 동굴 출구
- 거부: 동굴 장식물만 있는 내부, 채석장, 단순 분화구, 바위 뒤로 가려진 물
- 비추론: 암석 화학, 지하 유로, 대수층 경계, 두 물점의 실제 연결

### 4.5 활동 빙하 유동 지형

미국 지질조사국의 빙하지형 설명에서 U자 계곡, 빙퇴석, 빙하가 깎은 계곡 형상을 가져왔다. 여기에 현재 빙체의 표면 구조와 말단을 결합해, 설산이나 얼음 색만으로 빙하라고 부르는 혼동을 차단한다.

- 필수: U자 계곡을 채우는 연속 빙체, 하류 방향의 균열·유동띠, 얼음에 접한 빙퇴석, 말단과 융빙수
- 거부: 결빙호, 설원, 푸른 얼음 동굴, 빙퇴석 없는 얼음 조각
- 비추론: 실제 유속, 빙령, 질량수지, 후퇴율

### 4.6 풍성사구 바람 구조

미국 국립공원관리청 자료는 사구를 바람이 만든 지형으로 설명하며, 바람받이 사면·마루·바람그늘의 미끄럼면과 사립의 도약 이동을 구분한다. 한 사구 몸체 위에서 비대칭 단면과 작은 잔물결이 일관된 방향성을 보여야 한다.

- 필수: 긴 완경사 바람받이 면, 연속 마루, 마루 뒤 급경사 미끄럼면, 바람받이 면의 정렬된 잔물결
- 거부: 대칭 모래더미, 평평한 모래무늬, 형상 없이 떠도는 먼지
- 비추론: 정확한 풍속·풍향, 이동률, 안정화 연대

### 4.7 적란운 대류 폭풍 구조

세계기상기구 국제구름도감은 적란운을 큰 수직 발달, 섬유상·줄무늬상의 펼쳐진 상부, 어두운 밑면, 강수 또는 미류와 연결해 설명한다. 번개는 강한 시각 신호지만 구조를 대신하지 못하므로 필수로 두지 않는다.

- 필수: 넓고 어두운 밑면, 같은 밑면에서 솟은 대류탑, 섬유상·편평한 모루, 아래로 내리는 강수 또는 미류
- 거부: 먹구름만 있는 하늘, 번개 그래픽, 연기·화산재 기둥, 분리된 모루 모양
- 비추론: 폭풍 등급, 풍속, 우박 크기, 토네이도 가능성

### 4.8 고산 수목한계 전이지대

미국 국립공원관리청 자료는 닫힌 숲에서 더 짧고 성긴 수목, 바람에 눕거나 편향된 크룸홀츠, 무수목 고산 식생으로 이어지는 전이를 설명한다. 날카로운 이분 경계가 아니라 위로 갈수록 나무의 높이·간격·형태가 변하는 연속 구배가 핵심이다.

- 필수: 하부 닫힌 숲, 짧고 성긴 전이목, 낮고 편향된 크룸홀츠 띠, 그 위 무수목 고산대
- 거부: 뒤틀린 나무 한 그루, 벌목·산불 경계, 적설선
- 비추론: 고도, 종, 기후 원인, 수목한계 이동 추세

## 5. 후보팩 전용 4종과 하드 승격 보류 이유

### 5.1 하천변 범람원 구배

USGS 자료가 제시하는 활동 하도·범람원·비활동 범람원·상부 지형과 식생·침식·퇴적의 상호작용을 후보 슬롯으로 만들었다. 그러나 새 퇴적지와 식생 구배만으로 최근 범람 빈도나 하도-범람원 교환을 한 프레임에서 확정하기 어렵다. 따라서 프롬프트 구성에는 쓰되 자동 픽셀 PASS는 만들지 않았다.

### 5.2 화산 열수지대

USGS가 설명하는 분기공, 진흙탕, 끓는 못, 수증기 지면, 황갈색 변질암과 점토를 후보로 만들었다. 하지만 안개·온천·연막과의 시각 혼동이 크고, 지하 열원·투수성·지하수 연결은 보이지 않는다. 국지 분출구와 변질 지면을 강화하되 하드 판정은 보류했다.

### 5.3 맹그로브 조석 뿌리 체계

NOAA 자료의 조간대 수목, 조밀한 지주근, 조석수, 뿌리에 의한 유속 저감과 퇴적물 포획 관계를 후보로 만들었다. 다만 지주근 형태는 종과 지역에 따라 크게 달라지고, 한 프레임의 진흙이 실제 퇴적 포획 과정이나 조석 주기를 증명하지 못한다.

### 5.4 산호초 횡단 대상

NOAA가 구분하는 리프 플랫·리프 크레스트·포어리프와 파랑·수심 구배를 후보로 만들었다. 수중 시점에서는 원근·탁도·카메라 깊이 때문에 세 구역의 순서가 쉽게 왜곡되고, 단일 산호 정원이나 라군이 전체 횡단 구조로 오인될 수 있어 하드 판정을 보류했다.

## 6. 후보팩 구조

각 환경 문법은 다음 슬롯 역할로 분해했다.

| 슬롯 | 역할 | 예시 |
|---|---|---|
| `aesthetic_trend` | 장면 전체가 따라야 할 지배 구조 | `old_growth_forest_structure_aesthetic` |
| `subject` | 환경 자체를 주 피사체로 소유 | `active_glacier_landform_subject` |
| `action` | 물질 변화나 공간 상호작용 | `dune_saltation_stoss_lee_migration` |
| `location` | 관계가 동시에 보일 수 있는 장소 범위 | `karst_losing_stream_spring_location` |
| `surface_material` | 원인과 접촉을 보여 주는 국소 표면 | `wetland_hydric_soil_waterline_surface` |
| `composition` | 순서·단면·깊이를 보존하는 카메라 구성 | `shore_to_sea_tidal_bands_frame` |
| `weather` | 특정 문법에서만 필요한 대기·수면 상태 | `cumulonimbus_rain_shaft_outflow` |

12개 좁은 개념 구문은 각각 6~7개 슬롯을 강제하는 믹스인으로 연결했다. `surface_material`은 기존의 `layered_sediment_bank_surface`가 하천변 문법에 재사용 가능해 11개만 신설했다. 새 프리셋은 만들지 않았으므로 장면 표현 프리셋 수와 기존 선택 분포는 바꾸지 않는다.

## 7. 라우팅·혼동 방지 정책

- 하드 활성화: 프로필의 정확한 연구 구문에서만 허용
- 후보 믹스인: 한국어·영어의 좁은 동의 구문에서만 허용
- 광범위 단어: 새 믹스인과 하드 의무 모두 활성화하지 않음
- 의미 검색: 후보 발견에는 사용할 수 있지만 하드 의무로 승격하지 않음
- 부정·제외 구문: 기존 요청 극성 정책을 그대로 적용
- 사람·외모 슬롯: 자연환경 믹스인이 소유하지 않음
- 검증 단위: 개별 물체가 아니라 물체 사이의 순서, 접촉, 연결, 대비

## 8. 출처에서 추상화한 차원

| 기관·자료 | 사용한 일반 차원 | 사용하지 않은 것 |
|---|---|---|
| USFS Old-Growth Forests / DecAID | 크기 다양성, 수관층, 큰 생목·고사목·쓰러진 목재 | 특정 숲 사진의 구도, 임령 확정 |
| EPA Wetlands | 수문이 토양·식생을 지배, 침수·포화, 습생 식생 | 법적 경계 판정, 특정 지역 종 목록 |
| USGS Riparian Processes | 하도·범람원·상부 지형, 침식·퇴적·식생 상호작용 | 범람 빈도와 수문 연결의 픽셀 확정 |
| NOAA Intertidal Zone | 비말·고·중·저조대와 노출 차이 | 특정 생물 종의 보편적 높이 |
| USGS Karst | 용식 암반, 폐쇄 함몰지, 지하 배수, 소실 하천·샘 | 지하 유로와 암석 조성의 시각 확정 |
| USGS Glacier Landforms | U자 계곡, 빙퇴석, 빙하 침식 지형 | 현재 유속·후퇴율 |
| NPS Aeolian Landforms | 바람받이 사면, 마루, 미끄럼면, 도약 이동 | 정확한 풍속·이동량 |
| USGS Hydrothermal Features | 분기공, 진흙탕, 끓는 못, 변질 지면 | 열원·지하수·투수성의 직접 증명 |
| WMO International Cloud Atlas | 수직 발달, 섬유상 모루, 어두운 밑면, 강수·미류 | 폭풍 위험 등급 |
| NPS Alpine Vegetation | 숲에서 성긴 수목·크룸홀츠·툰드라로의 전이 | 기후 변화 인과 또는 이동률 |
| NOAA Mangroves | 조간대 수목, 지주근, 유속 저감, 퇴적 포획 | 종별 뿌리 형태의 보편화 |
| NOAA Coral Reef Zones | 리프 플랫·크레스트·포어리프 순서 | 모든 산호초의 동일 단면 |

## 9. 검증 기준

데이터 승격은 다음을 모두 만족할 때만 프롬프트 동작 PASS로 본다.

1. 새 75개 후보 ID가 병합 사전에 존재하고 의미 메타데이터가 완전하다.
2. 12개 좁은 구문이 각각 지정 믹스인 하나로 라우팅된다.
3. 넓은 자연환경 단어는 새 믹스인과 8개 하드 프로필을 켜지 않는다.
4. 8개 프로필은 4개 필수 구성요소, 일치하는 증거 필드, 5개 픽셀 게이트, 거부 대체물을 가진다.
5. 4개 후보팩 전용 문법은 믹스인으로는 작동하지만 하드 프로필을 만들지 않는다.
6. 12개 연구 원장 행의 후보 ID가 실제 병합 사전에 모두 존재한다.
7. 시맨틱 인덱스와 시각 프로필 인덱스가 현재 사전 해시와 일치한다.

렌더를 수행하지 않은 이번 작업에서 패키지·라우팅·회귀 테스트 통과는 **프롬프트 동작 PASS**까지만 뜻한다. 실제 픽셀에서 구조가 유지되는지와 사용자의 시각 판단은 별도의 미평가 단계다.

## 10. 출처

- US Forest Service, [Old-Growth Forests in the Pacific Northwest](https://research.fs.usda.gov/treesearch/741)
- US Forest Service, [DecAID old-growth structural components](https://research.fs.usda.gov/treesearch/5546)
- US EPA, [What is a Wetland?](https://www.epa.gov/wetlands/what-wetland)
- US EPA, [Classification and Types of Wetlands](https://www.epa.gov/wetlands/classification-and-types-wetlands)
- USGS, [Riparian vegetation and fluvial geomorphic processes](https://www.usgs.gov/publications/riparian-vegetation-and-fluvial-geomorphic-processes)
- USGS, [Riparian geomorphic surfaces](https://pubs.usgs.gov/sir/2010/5016/section5.html)
- NOAA Ocean Service, [What is the intertidal zone?](https://oceanservice.noaa.gov/facts/intertidal-zone.html)
- USGS, [Natural processes of ground-water and surface-water interaction in karst terrain](https://pubs.usgs.gov/circ/circ1139/htdocs/natural_processes_of_ground.htm)
- USGS, [Karst aquifers](https://www.usgs.gov/mission-areas/water-resources/science/karst-aquifers?page=0)
- USGS, [Geology of Glacier National Park](https://www.usgs.gov/geology-and-ecology-of-national-parks/geology-glacier-national-park)
- National Park Service, [Aeolian landforms](https://www.nps.gov/subjects/geology/aeolian-landforms.htm)
- National Park Service, [Sand dune geology](https://www.nps.gov/slbe/learn/nature/sand-dune-geology.htm)
- USGS, [Volcanic hydrothermal systems](https://pubs.usgs.gov/fs/2002/fs101-02/)
- WMO International Cloud Atlas, [Cumulonimbus](https://cloudatlas.wmo.int/en/cumulonimbus-cb.html)
- WMO International Cloud Atlas, [Explanatory remarks: Cumulonimbus](https://cloudatlas.wmo.int/en/explanatory-remarks-and-special-clouds-cumulonimbus.html)
- National Park Service, [Alpine vegetation resource brief](https://home.nps.gov/articles/000/alpine-vegetation-resource-brief.htm)
- National Park Service, [Treeline shifts in Denali](https://www.nps.gov/articles/denali-treeline-shifts.htm)
- NOAA Ocean Service, [What is a mangrove forest?](https://oceanservice.noaa.gov/facts/mangroves.html)
- NOAA Ocean Service, [Coral reef zones](https://oceanservice.noaa.gov/education/tutorial_corals/media/supp_coral04b.html)

