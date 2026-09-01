# 우주 요소 시각 의미·후보팩 강화 리서치

- 조사·반영일: 2026-09-01
- 대상: `photo-prompt-image-generator`
- 입력: 참조 대화 「우주 요소 조사」의 우주·천체·탐사·SF 키워드 분류
- 구현: 좁은 시각 의무 16개, 자문형 후보 클러스터 8개·후보 48개, 표현 방식 5개
- 판정 원칙: `partial = fail`; 데이터·프롬프트 합격과 실제 렌더 픽셀 합격을 분리한다.

## 결론

`우주`, `은하`, `블랙홀`, `행성`, `우주비행사`, `SF`처럼 넓은 말은 하나의 고정 외형이 없다. 이들을 정확어 하드 라우팅에 넣으면 단순한 별 배경, 빛나는 고리, 우주복 코스튬, 바퀴 달린 장난감이 본래의 물리 구조나 작업 관계를 대체한다. 따라서 다음 두 층으로 나눴다.

1. **하드 시각 계약**: 좁은 복합 구문이 직접 요청되거나 사용자가 정의한 경우에만 활성화한다. 각 계약은 단일 프레임에서 함께 확인할 독립 구성요소와 실패 대체물을 가진다.
2. **자문형 후보팩**: 작은 천체, 별의 생애, 은하 구조, 조밀천체, 태양 우주기상, 궤도 작업, 행성 표면 탐사, 사변 시스템을 여섯 슬롯의 완결된 클러스터로 제공한다. BM25F·임베딩 검색 결과는 선택 재료이며 의무가 아니다.

## 표현 방식 5개

| 방식 | 주장할 수 있는 것 | 금지되는 혼동 |
|---|---|---|
| `visible_light_observation` | 가시광이나 육안형 장면의 관찰 구조 | 보이지 않는 파장을 자연색 사진처럼 주장 |
| `false_color_or_multiwavelength` | 서로 다른 파장·에너지를 색으로 매핑 | 표시색을 천체의 일상적 실제색이라고 단정 |
| `measurement_reconstruction` | 희소·간접 측정으로 재구성한 영상 | 블랙홀 그림자 등을 선명한 직접 사진처럼 표현 |
| `scientific_simulation_or_map` | 모델·지도·설명용 시각화 | 시뮬레이션을 관측된 사건으로 제시 |
| `artist_concept_or_fiction` | 관측 불가능하거나 미래적인 독창 설계 | 다이슨 구조·워프·웜홀을 검증된 사실처럼 제시 |

NASA의 전자기 스펙트럼 자료는 검출 에너지가 이미지로 변환되고 거짓색이 정보를 전달하는 방식을 설명한다. EHT는 블랙홀 영상이 관측 데이터로부터 만든 재구성임을 명확히 한다. 이 구분은 미적 스타일이 아니라 증거 주장 경계다.

## 하드 시각 계약 16개

### 1. 활동 혜성: `active_comet_coma_tail_system`

- 필수: 응축된 머리 / 확산 코마 / 코마에서 이어지는 먼지·이온 꼬리 / 태양 반대 방향
- 실패: 코마 없는 소행성, 대기권 유성, 로켓 플룸, 머리와 분리된 장식 꼬리
- 근거: ESA의 혜성 구조 자료는 핵 주변 코마와 태양풍·복사압에 반응하는 먼지·이온 꼬리를 구분한다.

### 2. 막대나선은하: `barred_spiral_galaxy_structure`

- 필수: 중심팽대부 / 이를 가로지르는 항성 막대 / 막대 끝에서 시작하는 나선팔 / 하나의 은하 원반
- 실패: 일반 나선은하, 막대가 숨은 측면 은하, 렌즈 플레어
- 근거: NASA의 은하 형태 분류는 막대나선은하의 중심 막대와 팔 구조를 구분한다.

### 3. 상호작용 은하: `interacting_galaxies_tidal_structure`

- 필수: 구별되는 두 은하·핵 / 조석 다리 또는 꼬리 / 외곽 원반 비대칭 / 같은 조우에 귀속되는 변형
- 실패: 우연히 가까운 두 은하, 단일 불규칙 은하, 성운 리본
- 근거: NASA의 Tidal Tales 자료는 은하 상호작용의 꼬리·다리·껍질 구조를 관측 분류 단서로 다룬다.

### 4. 아인슈타인 고리: `einstein_ring_lens_alignment`

- 필수: 중심의 전경 렌즈 / 배경 광원의 얇은 고리·대응 호 / 렌즈 둘레 접선 곡률 / 공통 정렬
- 실패: 헤일로, 포털, 블랙홀 방출고리, 행성 고리
- 근거: ESA의 설명은 전경 질량과 배경 광원의 정렬이 고리 또는 호를 만드는 중력렌즈 구조를 보여준다.

### 5. 블랙홀 그림자 재구성: `black_hole_shadow_reconstruction`

- 필수: 중심 밝기 함몰 / 둘러싼 두꺼운 방출고리 / 밝기 비대칭 / 제한된 해상도의 측정 재구성
- 실패: 검은 원, 일식, 포털, 선명한 검은 구체
- 근거: NASA의 블랙홀 해부 자료와 EHT FAQ는 그림자·방출고리 및 직접 사진과 재구성 영상의 경계를 제공한다.

### 6. 상대론적 강착원반: `relativistic_accretion_disk_visualization`

- 필수: 납작한 발광 원반 / 중심 그림자 / 그림자 위아래로 휘어 보이는 원반 먼 쪽 / 한쪽 밝기 비대칭
- 실패: 행성 고리, 불꽃 소용돌이, 평면 헤일로
- 표현: 과학 시각화 또는 시뮬레이션임을 보존한다.

### 7. 원시별 원반·양극 분출: `protostar_disk_bipolar_outflow`

- 필수: 먼지 속 어린 중심원 / 납작한 원반 / 같은 중심에서 나오는 양쪽 분출 / 원반과 분출축의 직교
- 실패: 고리 달린 성숙별, 나선은하, 원반 없는 모래시계 성운
- 근거: NASA/Hubble의 원시행성 원반 자료는 어린 별 주변 원반과 분출 구조를 보여준다.

### 8. 초신성 잔해 충격 껍질: `supernova_remnant_shock_shell`

- 필수: 진화한 껍질 / 충격 가열 필라멘트 / 바깥 충격 전면 / 밀려난 주변 물질
- 실패: 폭발 순간, 행성상성운, 일반 색 성운
- 근거: NASA의 초신성 잔해 자료는 팽창하는 충격파와 잔해 구조를 구분한다.

### 9. 오로라 호·커튼: `auroral_arc_curtain_atmosphere`

- 필수: 행성 지평선·대기 / 긴 호 / 접힌 커튼 / 내부 수직 광선
- 실패: 녹색 구름, 성운, 광공해
- 근거: NOAA의 오로라 교육 자료는 arc, band, curtain, ray 형태와 상층대기 발생을 설명한다.

### 10. 태양 홍염 고리: `solar_prominence_magnetic_loop`

- 필수: 태양 가장자리 / 솟은 플라스마 호 / 채층의 두 발점 / 발점 간 연속 고리
- 실패: 분리된 불꽃, 일반 코로나 헤일로

### 11. 태양 플레어 활동영역: `solar_flare_active_region_burst`

- 필수: 태양 원반·가장자리 / 국소 활동영역 / 강한 섬광·리본 / 연결된 코로나 반응
- 실패: 홍염, 전 태양 균일 발광, 분리된 CME 전면

### 12. CME 코로나그래프 관측: `cme_coronagraph_snapshot`

- 필수: 광구를 가리는 차폐 원반 / 등록된 태양 중심 / 넓게 팽창하는 전면 / 희미한 바깥 코로나
- 실패: 태양 플레어, 혜성 꼬리, 헤일로, 방출 전면 없는 일식
- 근거: NASA는 플레어와 CME를 서로 다른 현상으로 구분한다. 코로나그래프 표현은 관측 장비의 차폐 구조를 보존해야 한다.

### 13. EVA 작업 체계: `eva_spacewalk_work_system`

- 필수: 우주선 외부 / 압력복·헬멧·PLSS / 안전줄·손잡이·발 구속 / 외부 장비와 도구 접촉
- 실패: 스튜디오 코스튬, 선내 우주복 인물, 구속 없는 포즈, 장비 옆 포즈
- 근거: NASA 우주복 기본 자료는 EVA 우주복의 생명유지와 우주선 외부 작업 맥락을 설명한다.

### 14. 미세중력 정거장 내부: `microgravity_orbital_interior`

- 필수: 정거장 모듈 하드웨어 / 지지 없이 떠 있는 복수 요소 / 공유된 아래 방향 없음 / 손잡이·구속으로 이동 제어
- 실패: 점프, 와이어 공중부양, 회전 세트에 누운 인물
- 근거: NASA의 microgravity 자료는 궤도 자유낙하가 지속되는 환경과 일상 작업 효과를 설명한다.

### 15. 도킹 포획 정렬: `spacecraft_docking_capture_alignment`

- 필수: 두 우주선·모듈 / 서로 마주보는 호환 인터페이스 / 공통 중심축 / 소프트·하드 포획 접촉
- 실패: 플라이바이, 편대비행, 충돌, 장식 고리
- 근거: International Docking System Standard는 인터페이스·정렬·포획·결합의 기술 경계를 제공한다.

### 16. 행성 로버 표면 작업: `planetary_rover_surface_operation`

- 필수: 임무에 맞는 이동형 본체 / 지면 접촉 / 특정 표적을 다루는 과학 장비 / 천공·변위·시료·측정 결과
- 실패: 착륙선, 궤도선, 장난감, 작업 없는 로버 초상
- 근거: NASA Perseverance 구성 자료는 이동계와 과학 장비를 설명한다. 바퀴 수는 임무별 속성이므로 보편 의무가 아니다.

## 후보팩 8개 클러스터

각 클러스터는 `aesthetic_trend`, `subject`, `action`, `location`, `prop`, `composition`의 여섯 후보를 가진다.

| 클러스터 | 대표 하드 프로필 | 표현 방식 |
|---|---|---|
| `small_body_encounter` | `active_comet_coma_tail_system` | visible-light observation |
| `stellar_lifecycle_observation` | `protostar_disk_bipolar_outflow` | multiwavelength/false-color 가능 |
| `galaxy_structure_observation` | `interacting_galaxies_tidal_structure` | visible-light 또는 multiwavelength |
| `compact_object_visualization` | `black_hole_shadow_reconstruction` | measurement reconstruction |
| `solar_space_weather` | `cme_coronagraph_snapshot` | instrument observation |
| `orbital_human_operations` | `eva_spacewalk_work_system` | operational documentary |
| `planetary_surface_exploration` | `planetary_rover_surface_operation` | operational documentary |
| `speculative_space_systems` | 없음, 후보 전용 | artist concept or fiction |

후보 48개는 비순위·선택형이다. 후보에 있는 소품이나 미학 하나만 선택해도 하드 프로필이 성립하는 것은 아니다.

## 후보 전용으로 남긴 개념

- `우주`, `cosmos`, `universe` 같은 장르·분위기 말
- 암흑물질·암흑에너지, CMB, 우주 거대구조처럼 단일 사진의 자연색 외형으로 고정할 수 없는 개념
- 외계행성 표면색·거주가능성, 외계 생명·문명·테크노시그니처처럼 관측 근거와 작가 콘셉트의 경계가 중요한 개념
- 펄서의 주기, 중력파, 스펙트럼, 적색편이처럼 시간·측정·그래프 증거가 핵심인 개념
- 웜홀, 워프, 다이슨 구조, 테라포밍처럼 사변 설정인 개념

이들은 의미 검색과 작가 콘셉트 재료가 될 수 있지만, 좁은 사용자 정의와 표현 방식 표기가 없으면 보편적인 픽셀 의무가 되지 않는다.

## 검증 경계

- **패키지**: JSON·레지스트리·인덱스 해시가 유효해야 한다.
- **프롬프트**: 좁은 정확 구문은 의도한 하나의 프로필을 활성화하고, 넓은 말과 근접 대체물은 활성화하지 않아야 한다.
- **렌더 픽셀**: 선택한 모든 게이트를 같은 저장 이미지에서 썸네일·네이티브 크기로 확인해야 한다. 부분 충족은 실패다.
- **사용자 판단**: 미감·선호·참조 외형 만족도는 기술 판정과 별도이며 요청 사용자의 직접 판단 전에는 미결이다.

## 공식·권위 출처

- ESA, comet structure: https://www.esa.int/ESA_Multimedia/Images/2023/11/Structure_of_a_comet
- NASA, galaxy types: https://science.nasa.gov/universe/galaxies/types/
- NASA, Galaxy Zoo Tidal Tales: https://science.nasa.gov/get-involved/citizen-science/help-galaxy-zoo-tidal-tales-open-cosmic-storybook/
- ESA, Einstein ring explained: https://www.esa.int/ESA_Multimedia/Images/2025/02/Einstein_ring_explained
- NASA, anatomy of a black hole: https://science.nasa.gov/universe/black-holes/anatomy/
- Event Horizon Telescope, image/reconstruction FAQ: https://eventhorizontelescope.org/faq/can-we-really-photograph-black-hole-are-they-not-entirely-dark-no-light-can-escape-them
- NASA/Hubble, planet-forming disks: https://science.nasa.gov/missions/hubble/hubbles-album-of-planet-forming-disks/
- NASA, supernova-remnant observatory study: https://science.nasa.gov/missions/hubble/nasas-great-observatories-may-unravel-400-year-old-supernova-mystery/
- NOAA Space Weather Prediction Center, Aurora PDF: https://www.swpc.noaa.gov/sites/default/files/images/u2/Aurora.pdf
- NASA, Sun facts: https://science.nasa.gov/sun/facts/
- NASA, Solar Flares FAQs: https://science.nasa.gov/blogs/solar-cycle-25/2022/06/10/solar-flares-faqs/
- NASA, Spacewalk Spacesuit Basics: https://www.nasa.gov/centers-and-facilities/johnson/spacewalk-spacesuit-basics/
- NASA, What Is Microgravity?: https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/
- International Docking System Standard: https://www.internationaldockingstandard.com/download/IDSS_IDD_Revision_E_TAGGED.pdf
- NASA, spacecraft classification: https://science.nasa.gov/learn/basics-of-space-flight/chapter9-1/
- NASA, Perseverance rover components: https://science.nasa.gov/mission/mars-2020-perseverance/rover-components/
- NASA, Energy to Image: https://science.nasa.gov/ems/04_energytoimage/

