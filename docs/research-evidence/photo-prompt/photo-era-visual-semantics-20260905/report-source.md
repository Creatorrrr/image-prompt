# 사진 촬영 시대별 특징: 시각 의미·후보팩 강화 리서치

- 조사일: 2026-09-05
- 대상: `skills/photo-prompt-image-generator`
- 참조 대화: `사진 촬영 시대별 특징 조사` (`6a9a7c73-fb08-83e8-8a72-c3d7c3f0e75b`)
- 상태: 연구·데이터 설계 완료, 런타임 미반영
- 동반 산출물: `candidate-data-proposal.json`, `evidence.jsonl`, `routing-regression-proposal.jsonl`, `iteration-record.json`

## 1. 결론

사진의 시대성은 `연도 -> 세피아/그레인`처럼 한 단계로 번역하면 안 된다. 한 프레임에서 보이는 시대감은 다음 요소가 겹친 결과다.

1. 촬영 공정과 원본 지지체: 은도금 동판, 종이 네거티브, 유리판, 롤필름, 디지털 센서.
2. 이미지 형성 재료와 반응: 은 입자, 알부민, 콜로디온, 염료, 전분색소 스크린, 디지털 화소와 압축.
3. 카메라·광학·노출 관계: 장노출에 따른 정지성, 직광 플래시, 얕거나 깊은 피사계심도, 작은 센서의 제한된 톤 반응, 다중 프레임 합성.
4. 장르와 촬영 관습: 스튜디오 초상, 스냅, 화보, 보도, 가정 사진, 소셜 피드.
5. 출력·유통 컨테이너: 케이스 속 판, 카드 마운트, 슬라이드, 인화지, 신문 망점, 화면 재촬영, 정사각·세로 피드.
6. 보존·열화: 황변, 은경화, 염료 퇴색, 채널링, 균열, 곰팡이와 취급 손상.
7. 후대 재현: 필름 에뮬레이션, 레트로 필터, 합성 테두리, 디지털 그레인, 재압축.
8. 당시 생활문화의 장면 단서: 복식, 가전, 거리 구조, 가구, 인쇄물. 이 층은 지역·계층·장르·보급 지연에 따라 달라진다.

따라서 후보팩은 `era`라는 단일 슬롯보다 `capture process`, `material object`, `capture response`, `genre practice`, `output container`, `deterioration`, `retro simulation`, `scene prior`를 분리해 조합해야 한다. 특정 연도, 실제 필름 재고, 카메라 모델, 촬영자, 출판 이력, 원본성은 픽셀만으로 입증할 수 없으므로 메타데이터 차선에 둔다.

이번 제안은 18개 좁은 hard-profile 계약, 60개 후보 원자, 23개 시대/공정 후보군, 27개 근거 원장 행, 71개 라우팅·컴포넌트 절삭·충돌 회귀 항목을 설계한다. 다만 이는 **연구 제안**이다. 공유 레지스트리, 검색 인덱스, 런타임 후보팩은 변경하지 않았고 프롬프트·이미지·사용자 평가는 수행하지 않았다.

## 2. 참조 대화에서 회수한 범위

참조 대화는 1820년대 헬리오그래프부터 2020년대 계산사진과 디카 리바이벌까지 다음 계열을 제시했다.

- 초기 공정: 헬리오그래프, 다게레오타입, 칼로타입, 습판 콜로디온, 알부민 인화, 앰브로타입·틴타입, 젤라틴 건판.
- 대중화 장치: Kodak 롤필름, Brownie, Autochrome, Kodachrome, Tri-X, Instamatic 126, Super 8, 110, 즉석사진.
- 사진사적 관습: Pictorialism, New Vision, FSA 다큐멘터리, 할리우드 글래머, 전시 보도 플래시, 거리사진, New Color, New Topographics.
- 소비자 디지털: 1980년대 자동초점 콤팩트·미니랩, 1990년대 일회용 카메라·4×6 인화·날짜 각인, 2000년대 CCD 디카·JPEG·직광 플래시.
- 플랫폼·계산사진: 초기 정사각 소셜 피드, 인물 모드, HDR, Night mode, 0.5× 초광각, 9:16 세로 유통, 의도적 불완전성과 디카 리바이벌.
- 국내 장면 가설: 전후·산업화기 흑백 기록, 1980년대 컬러 TV와 가정 플래시, 1990년대 학교·여행·스티커 사진, 2000년대 디카·초기 SNS, 2010년대 카페·정사각 피드, 2020년대 네 컷·초광각·Y2K 재현.

이 목록은 키워드 범위를 제공하지만 보급률·대표성·국가별 동시성을 증명하는 코퍼스는 아니다. 특히 제품 발표 연도와 대중적 사용 기간, 촬영 당시의 원본 특성과 후대 열화, 실제 옛 사진과 현대 레트로 재현을 구분해야 한다.

## 3. 증거 모델

### 3.1 시간 주장의 다섯 종류

| 시간 주장 | 예 | 픽셀만으로 판정 가능한가 | 데이터 처리 |
|---|---|---:|---|
| 공정 가용 시기 | 다게레오타입은 1839년에 공표됨 | 아니요 | 출처가 있는 메타데이터 |
| 대중 보급 시기 | Instamatic이 1960년대 가정 스냅에 널리 쓰임 | 아니요 | 지역·시장 출처가 있는 후보 prior |
| 장면의 사건 시기 | 사진 속 사건이 1974년에 일어남 | 아니요 | 캡션·기록 메타데이터 |
| 물체의 경과 시간 | 인화지가 오래되어 열화됨 | 일부 증상만 가능 | 열화 profile, 연대 추론 금지 |
| 후대 재현 시기 | 2026년에 1990년대 룩을 흉내 냄 | 아니요 | retro-simulation 차선 |

[NARA의 디지털 사진 기록 지침](https://www.archives.gov/records-mgmt/initiatives/digital-photo-records.html)은 캡션, 촬영자, 원래 매체, 압축, 색 프로필, EXIF 같은 정보를 별도 메타데이터로 보존하도록 요구한다. 이는 사진의 연도·촬영자·원본 매체를 외관만으로 확정하면 안 된다는 설계 근거다.

### 3.2 시각 의미의 여덟 차선

| 차선 | 소유하는 시각 정보 | 소유하지 않는 주장 |
|---|---|---|
| `capture_process` | 판/종이/필름에 남은 공정 고유 구조 | 정확한 촬영 연도, 진품 여부 |
| `material_object` | 지지체, 마운트, 케이스, 가장자리, 두께 | 보관 기간, 소유자 |
| `capture_response` | 노출, 톤, 색, 노이즈, 광학 관계 | 정확한 카메라·필름 모델 |
| `genre_practice` | 프레이밍, 포즈, 카메라 위치, 촬영 상황 | 작가, 기관, 실제 역사적 프로젝트 |
| `output_container` | 신문 망점, 슬라이드 마운트, 인화지, 화면/피드 | 최초 배포 경로, 플랫폼 계정 |
| `deterioration` | 은경화, 채널링, 염료 퇴색 같은 물질 증상 | 촬영 당시 룩, 고전성 |
| `retro_simulation` | 의도적으로 추가한 필터·그레인·테두리 | 진짜 아날로그 공정 |
| `scene_prior` | 시대와 함께 등장한 사물·공간·행동 후보 | 그 사물 하나로 연대 확정 |

[미 의회도서관](https://www.loc.gov/preservation/care/photolea.html)은 사진을 support–binder–final image material의 복합 물체로 설명하고, 열·습도·빛·오염·불완전 처리로 인한 변색과 손상을 별도로 다룬다. [캐나다 보존연구소](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/photographic-materials.html)도 알부민의 미세 균열, 은경화, 필름 지지체 열화를 촬영 당시 미학이 아니라 재료의 구조와 손상으로 설명한다.

### 3.3 증거 등급

- `A — object/process diagnostic`: 지지체와 이미지 형성 구조가 같은 프레임에 보이며 가까운 대체물을 배제할 수 있다. 좁은 exact hard profile 후보.
- `B — multi-cue appearance`: 광학·톤·구도 단서 여러 개가 함께 있지만 실제 장비나 시기는 증명하지 못한다. “look”으로만 hard profile 후보.
- `C — genre/scene prior`: 특정 시기에 자주 연결되지만 다른 시기에도 가능한 장면. 후보군과 검색 alias만 허용.
- `D — metadata-only`: 날짜, 모델, 필름 재고, 작가, 프로젝트, 출판·삭제·소유 이력. hard 활성화 금지.

## 4. 현재 저장소 기준선과 빈틈

2026-09-05의 공유 자산 스냅샷은 다음과 같다.

| 항목 | 상태 |
|---|---:|
| 슬롯 | 111 |
| 프리셋 | 575 |
| visual obligation profiles | 333 |
| `medium` | 57 |
| `genre` | 56 |
| `capture_context` | 76 |
| `camera_type` | 25 |
| `composition` | 256 |
| `lens` | 33 |
| `color` | 54 |
| `film_emulation` | 18 |
| `surface_material` | 141 |
| `lens_artifact` | 10 |
| `grain_profile` | 7 |
| `color_grading` | 8 |

이미 재사용할 수 있는 후보에는 `archive_scan`, `smartphone_snapshot`, `nostalgic_archive`, `full_print_edge_scan_capture`, `early_2000s_digicam_social_repost_capture`, `contact_sheet_selection_capture`, `compact_digital_camera`, `disposable_film_camera`, `instant_camera`, `digicam_2000s_camera`, `phone_0_5x_ultrawide`, `sepia`, `film_faded`, `phone_hdr_color`, `compact_ccd_digicam`, `polaroid_sx70`, `super8_film_frame`, `light_leak_streak`, `smartphone_night_noise`가 있다.

재사용 가능한 hard profile은 `physical_print_scan_material_context`, `early_2000s_compact_digicam_social_repost`, `contact_sheet_selection_context`, `photobooth_four_cut_sequence`다.

빈틈은 후보 수가 아니라 의미 소유권이다.

- `sepia`는 현재 `aged sepia tone`으로 되어 있어 색조와 나이를 결합한다.
- 필름·디카 후보가 대체로 한 줄 룩이라 지지체, 광학 반응, 출력물, 재압축을 구분하지 못한다.
- 다게레오타입·칼로타입·습판·알부민·Autochrome 같은 공정은 전용 시각 계약이 없다.
- 은경화·염료 퇴색·채널링 같은 보존 열화가 촬영 시대나 필름 에뮬레이션과 분리되어 있지 않다.
- 정사각·9:16 같은 유통 프레임이 촬영 센서 시대를 대신할 위험이 있다.
- `Kodak`, `Polaroid`, `CCD`, `Instamatic`, `110` 같은 상표·기술명이 단독으로 과도한 시각 의무를 만들 수 있다.

## 5. 시대·공정 지도

아래 연대는 출처가 지지하는 가용 시점 또는 역사적 범위이지, 전 세계 동시 보급이나 사진 한 장의 연대 판정 규칙이 아니다.

| 범위 | 근거가 강한 공정·관습 | 후보팩에서 보일 수 있는 것 | hard/profile 정책 | 주요 오탐 |
|---|---|---|---|---|
| 1820s–1830s | 헬리오그래프, 매우 긴 노출 | 정적 건축, 낮은 미세 대비, 물질 표면 | 후보 전용 | 장노출 느낌만으로 헬리오그래프 주장 |
| 1839–1850s | 다게레오타입 | 은도금 판의 거울성, 각도에 따른 양/음 전환, 케이스 | A급 좁은 profile | 세피아 종이사진, 은경화, 거울 |
| 1841–1860s | 칼로타입·염지 인화 | 종이 섬유가 이미지 경계를 가로지르는 매트한 내재상 | A급 좁은 profile | 종이 텍스처 오버레이, 단순 블러 |
| 1851–1880s | 습판 콜로디온 | 유리판, 선명한 디테일, 국소 도포 가장자리·먼지 핀홀 | A급 좁은 profile | 전면 그런지, 라이트릭, 금 간 유리 |
| 1850–1890s | 알부민 인화 | 얇고 매끈한 인화층, 카드 마운트, 미세 균열 | A급 object profile | 갈색 색보정만 있는 디지털 이미지 |
| 1842 이후 | cyanotype | 프러시안 블루와 접촉물의 흰/청색 실루엣 | A급 좁은 profile | 청색 모노크롬, 설계도 선화 |
| 1870s–1900s | 젤라틴 건판·은염 인화 | 유리/필름 지지체와 젤라틴층, 안정적 세부 | 후보 전용 | 깨끗한 흑백을 특정 공정으로 단정 |
| 1888–1910s | 롤필름·Brownie 스냅 | 비격식 프레이밍, 생활 동작, 단순 카메라 위치 | C급 후보군 | 모든 흔들림·중앙구도를 Brownie로 단정 |
| 1890s–WWI | Pictorialism | 선택적 연초점, 큰 톤 덩어리, 손작업 표면·마운트 | B급 exact style profile | 전체 Gaussian blur, 안개 필터 |
| 1907–1930s | Autochrome | 투명 유리 지지체, 미세 색소 모자이크, 절제된 투과색 | A급 좁은 profile | 디지털 RGB 픽셀, 점묘화, 파스텔 필터 |
| 1920s | New Vision | 극단적 상하 시점, 대각 구조, 스케일 전도, 포토그램 | B급 geometry profile | 셀피 Dutch angle, 광각 왜곡 하나 |
| 1935–1944 | FSA/OWI 기록 | 농촌·소도시·산업·가정 환경, 기록적 거리와 행동 | C/D급 후보·메타 | 흑백·빈곤 장면만으로 FSA 주장 |
| 1930s–1940s | 보도 플래시·신문 복제, 글래머·누아르 | 광축 근처 직광, 빠른 감쇠, 하드 그림자, 망점·신문지 | B급 결합 profile | 1990s 파티 플래시, 어두운 배경만의 누아르 |
| 1935–1960s+ | 컬러 슬라이드와 가정 여행 | 투명 필름과 마운트, 투과광, 채도·밀도 | A급 object profile | 화면 속 사진, 가짜 슬라이드 테두리 |
| 1950s | 고감도 흑백 거리·가정 컬러 | 상황 포착, 가용광, 색 슬라이드 | C급 후보군 | Tri-X/Kodachrome 명칭만으로 stock 판정 |
| 1963–1970s | Instamatic 126·flashcube·Super 8 | 정면 플래시, 중앙 가정 스냅, 연속 홈무비 프레임 | C급 후보군 | 정사각 크롭을 126 증거로 사용 |
| 1972–1980s | 110 pocket·integral instant | 작은 포맷 스냅 룩, 완전한 즉석 인화물 객체 | 110은 C급, 즉석 인화물은 A급 | 저해상도=110, 흰 테두리=Polaroid |
| 1980s | 자동초점 콤팩트·미니랩 | 광택 인화물, 근축 플래시, 가까운 배경 그림자, casual crop | B급 print/capture profile | 네온·빨간눈 하나로 1980s 단정 |
| 1990s | 일회용 카메라·4×6·날짜 각인 | 직광 파티 스냅, 소비자 인화물, 선택적 날짜 자막 | C급 후보군 | 날짜 워터마크가 실제 날짜를 증명 |
| 2000–2004 | 소형 CCD 디카·초기 카메라폰 | 제한된 하이라이트, 혼합 WB, 색 노이즈, JPEG 재압축 | 기존 profile 재사용 | 모든 purple fringe를 CCD로 단정 |
| 2005–2009 | 콤팩트/초기 DSLR·웹 사진 | 과포화·비네트·초기 HDR처럼 보이는 편집 조합 | C급 후보군 | 편집 preset을 카메라 세대로 오인 |
| 2010–2014 | 초기 Instagram 정사각·필터 | 정사각 유통 컨테이너, lifted black, warm fade | C급 output 후보 | 정사각 사진=2010s 원본 촬영 |
| 2015–2019 | 인물 모드·Smart HDR·ring light | 마스크 기반 피사체 분리, 국소 톤 보정, 다중프레임 look | B급 look 또는 후보 | 얕은 심도=인물 모드, HDR=스마트폰 |
| 2020–2022 | Night mode·0.5×·9:16 | 저조도 밝기·디테일, 초광각 근원근, 세로 유통 | B/C급 분리 | 9:16=스마트폰 센서 시대 |
| 2023–2026 | 계산사진 정교화와 의도적 결함 | 깨끗한 합성과 현재 장면 속 옛 디카 룩의 이중 시간 | C급 dual-time 후보 | 레트로 룩을 실제 옛 사진으로 주장 |

[V&A의 공정 안내](https://www.vam.ac.uk/articles/photographic-processes)는 다게레오타입, 칼로타입, 콜로디온, 알부민, cyanotype, Autochrome의 재료와 외관 차이를 설명한다. [Kodak의 연혁](https://www.kodak.com/en/company/page/milestones/)은 Brownie, Instamatic, Super 8, Pocket Instamatic 110, 초기 디지털 카메라의 제품 시점을 뒷받침하지만, 출시 연도는 곧바로 지역별 보급률을 뜻하지 않는다.

## 6. 제안 hard profile 18개

모든 profile은 exact/context-complete 문구에만 hard 활성화한다. 다섯 구성요소가 한 프레임에 모두 읽혀야 하며 하나라도 빠지면 실패다.

### 6.1 공정·물질 객체

#### `daguerreotype_reflective_cased_plate_object`

필수: 은색 금속판 표면, 시점에 따른 반사/명암 전환, 종이섬유가 아닌 미세 이미지, 판의 전체 경계와 깊이, 매트·유리·케이스의 보호 구조.

거부: 세피아 종이 인화, tintype, 일반 거울 속 초상, 은경화, 무작위 스크래치. [CCI의 케이스 사진 관리 자료](https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-encased-photographic-images.html)는 다게레오타입을 은도금 동판 위의 거울 같은 이미지로 설명한다.

#### `calotype_salted_paper_fiber_image_relation`

필수: 매트한 종이 지지체, 이미지의 밝고 어두운 영역을 실제 섬유가 가로지름, 섬유층에 내재된 은상, 연속적이지만 약간 부드러운 세부, 전체 종이 경계.

거부: 종이 텍스처 오버레이, 전체 초점 흐림, 알부민 광택, 캔버스, 디지털 노이즈.

#### `wet_collodion_glass_plate_coating_trace`

필수: 유리판 경계·두께, 선명하고 입자감이 적은 세부, 한쪽 도포 가장자리, 국소 흐름 자국, 흰 먼지 핀홀/화학 불균일이 판 표면에 귀속됨.

거부: 전면 그레인, 라이트릭, 깨진 유리 소품, 먼지 오버레이, 필름 스트립.

#### `albumen_card_mount_print_material_relation`

필수: 얇은 인화지가 두꺼운 카드에 붙은 층 관계, 매끈한 알부민 표면, 풍부한 미세 디테일, 전체 카드/인화 경계, 표면 전반의 미세 crackle 또는 종이섬유가 비치는 영역.

거부: 갈색 필터, 거친 무광 염지 인화, 코팅 없는 카드, 가짜 빈티지 테두리, 큰 건조 균열.

#### `cyanotype_contact_print_prussian_blue_relation`

필수: 프러시안 블루 이미지장, 접촉 물체의 흰/옅은 청색 형태, 불투명도 차에 따른 톤, 겹침과 접촉 경계, 종이 전체 경계.

거부: 청색조 사진, blueprint 선화, X-ray, 흰 실루엣 합성, cyan color grade.

#### `autochrome_glass_transparency_color_screen`

필수: 투명 유리판, 후면 또는 투과광, 균일 영역의 미세 적·녹·청 계열 전분 모자이크, 흑백 명도상 위에 얹힌 절제된 색, 전체 판 경계.

거부: 디지털 RGB 픽셀 격자, 컬러 필름 그레인, 점묘화, 파스텔 필터, 종이 인화. V&A는 Autochrome을 염색한 감자 전분 모자이크와 흑백 이미지층을 결합한 최초의 실용적 컬러 공정으로 설명한다.

#### `integral_instant_print_object_relation`

필수: 완전한 물리 인화물 경계, 거의 정사각 이미지 영역과 비대칭 외곽 여백, 인화물 두께/그림자, 이미지가 테두리 안에 포함된 관계, 국소 현상 불균일이나 취급 흔적.

거부: 흰 프레임 그래픽, 정사각 크롭, 스마트폰 화면, 네 컷 스트립, peel-apart 인화. [Smithsonian의 SX-70 자료](https://americanhistory.si.edu/collections/object/nmah_689070)는 1972년 SX-70 객체를 기록하며, [Cooper Hewitt](https://www.cooperhewitt.org/2018/02/23/instant-photography-before-the-internet/)는 자동 현상되는 즉석사진 맥락을 설명한다.

#### `mounted_slide_transparency_object_relation`

필수: 투명 필름 프레임, 카드/플라스틱 마운트, 투과광, 이미지가 마운트 개구부 안에 놓인 관계, 프레임 가장자리의 밀도/필름 두께.

거부: 화면 속 사진, 가짜 슬라이드 UI, 종이 인화, 필름 네거티브, 채도 높은 이미지 단독.

### 6.2 촬영·출력 관습

#### `pictorialist_handworked_print_relation`

필수: 선택적 연초점과 보존된 초점 기준, 큰 명암 덩어리, 손작업 인화 표면, 국소 pigment/gravure 변화, 작품·마운트 전체 관계.

거부: 전체 Gaussian blur, 안개만 있는 풍경, modern glow filter, 일반 회화, 선명한 기록사진. [Art Institute of Chicago](https://archive.artic.edu/stieglitz/pictorialism/)는 Pictorialism의 회화적·이상화된 이미지와 gum bichromate·photogravure 같은 손작업 공정을 설명한다.

#### `new_vision_modernist_camera_geometry`

필수: 극단적 상/하 시점, 강한 대각 구조, 스케일 또는 방향의 낯설게 하기, 선명한 광영 그래픽, 실제 산업·도시 구조 또는 물체 실루엣.

거부: Dutch-angle 셀피, 광각 얼굴 왜곡, Bauhaus 장식 소품, 일반 고대비 흑백, 기울인 후처리만. [Metropolitan Museum 자료](https://resources.metmuseum.org/resources/metpublications/pdf/Recent_Acquisitions_A_Selection_2004_2005_The_Metropolitan_Museum_of_Art_Bulletin_v_63_no_2_Fall_2005.pdf)는 Moholy-Nagy와 New Vision의 photogram, negative print, 비관습적 시점과 추상화를 연결한다.

#### `press_flash_newsprint_reproduction_relation`

필수: 광축 가까운 직광, 가까운 면의 반사 하이라이트, 배경으로의 빠른 감쇠와 하드 그림자, 급박한 비대칭 크롭/행동, 종이와 망점이 보이는 신문 복제.

거부: 1990s 파티 플래시, 스튜디오 스트로브, 어두운 배경만, halftone 필터만, 깨끗한 디지털 보도사진.

#### `late_century_minilab_flash_print_relation`

필수: 완전한 소비자용 광택/RC 인화지, near-axis 플래시, 가까운 배경 그림자, casual crop과 순간 동작, 인화물 경계/주변 앨범 또는 탁자.

거부: 화면 캡처, 스튜디오 포트레이트, 가짜 Polaroid 테두리, 날짜 자막만, 극단적 빈티지 손상.

### 6.3 계산사진과 동시대 촬영 관계

#### `smartphone_ultrawide_near_far_perspective_relation`

필수: 매우 넓은 시야, 가까운 전경의 상대적 확대, 가장자리 방향의 늘어남, 중앙 원근 기준, 스마트폰을 몸 가까이 둔 촬영 위치 또는 전경-원경 행동 연결.

거부: fisheye 원형 왜곡, panorama stitching, 일반 넓은 방, 얼굴만 왜곡, 세로 크롭만.

[Sony의 원근 안내](https://www.sony.com/lr/electronics/focal-length-angle-of-view-perspective)는 넓은 화각에서 전경을 같은 크기로 담기 위해 카메라가 가까워지면 원경이 상대적으로 작게 보인다고 설명한다. [Apple의 카메라 안내](https://support.apple.com/fr-fr/102443)는 지원 기기의 0.5× Ultra Wide 선택을 문서화한다. 따라서 hard profile은 가까운 촬영 거리와 근원근 관계를 소유하고, `0.5×` 기기 라벨은 명시 메타데이터로만 취급한다.

#### `computational_hdr_local_tone_balance_look`

필수: 강한 밝기 차가 있는 장면, 밝은 영역 세부 보존, 어두운 영역의 낮은 노이즈와 세부, 전역 평탄화가 아닌 국소 톤 연결, 움직이는 경계에서 합성 충돌이 없거나 매우 국소적인 흔적.

거부: halo가 심한 단일 HDR 필터, 평평한 노출, shadow lift만, 과도한 sharpening, 실제 스마트폰/알고리즘 주장. [Google의 HDR+ 연구](https://research.google/pubs/burst-photography-for-high-dynamic-range-and-low-light-imaging-on-mobile-cameras/)는 여러 짧은 노출의 정렬·병합과 tone mapping을 설명하고, [Apple의 HDR 안내](https://support.apple.com/en-mide/guide/iphone/iph2cafe2ebc/ios)는 서로 다른 노출을 결합해 밝고 어두운 영역의 세부를 보존한다고 설명한다. profile은 이 원인을 증명하지 않고 보이는 결과만 소유한다.

#### `computational_low_light_multiframe_look`

필수: 실제 저조도 광원, 과도하게 날리지 않은 광원, 어두운 면의 읽을 수 있는 색·구조, 억제된 랜덤 노이즈, 사람/손/차량 경계의 일관성.

거부: 낮 장면을 어둡게 한 것, 장노출 광궤적만, flash-lit foreground, noiseless CGI, 야간이라는 라벨. [Google Night Sight](https://research.google/blog/night-sight-seeing-in-the-dark-on-pixel-phones/)와 [Apple Night mode](https://support.apple.com/guide/iphone/take-night-mode-photos-iph1a3c5b4c3/26/ios)는 저조도에서 여러 프레임·긴 노출을 이용해 밝기와 세부를 확보하며 정지와 정렬이 중요함을 설명한다.

### 6.4 보존 열화

#### `silver_mirroring_surface_region_relation`

필수: 은염 이미지가 있는 물리 인화/네거티브, 어두운 고밀도 영역에 모이는 청회색 금속성 광택, 표면 반사, 영향받지 않은 비교 영역, 손상이 이미지층에 귀속되는 경계.

거부: 다게레오타입 판 전체의 거울성, 유리 glare, 청색 grade, 은색 액자, 렌즈 플레어.

#### `acetate_channeling_shrinkage_relation`

필수: 플라스틱 필름 지지체, 유제와 지지체의 수축 차, 굽고 이어지는 channel/wrinkle 망, 이미지 왜곡·박리, 덜 손상된 가장자리 비교.

거부: 종이 crackle, 건조한 흙, 물결 필터, 깨진 유리, 무작위 스크래치. [Library of Congress의 네거티브 보존 자료](https://www.loc.gov/collections/genthe/articles-and-essays/deterioration-and-preservation-of-negatives-autochromes-and-lantern-slides/negatives/)는 acetate film의 심한 channeling과 가소제 결정화를 별도 열화로 보여준다.

#### `chromogenic_dye_fade_covered_edge_relation`

필수: 컬러 인화/투명 이미지, 염료 채널의 불균등 손실, 밀도·대비 저하, 빛 노출/보관 경계와 정렬된 변화, 가려졌거나 덜 손상된 비교 영역.

거부: warm grade, tungsten 조명, expired-film capture cast, sepia, 전역 저채도. 이 profile은 촬영 연대를 말하지 않으며 열화 상태만 표현한다.

## 7. 후보군 설계

`candidate-data-proposal.json`은 23개 source-bound family를 정의한다. 각 family는 최소한 다음 역할을 분리한다.

```text
primary_tag
availability_window_metadata
capture_process_or_device_candidate
material_object_candidate
capture_response_candidate
genre_or_scene_candidate
output_container_candidate
deterioration_candidate
retro_simulation_candidate
hard_profile_ids
confounds
claim_boundary
```

### 7.1 공정 중심 후보군

- `daguerreotype_cased_plate_1839_1860s`
- `calotype_salted_paper_1841_1860s`
- `wet_collodion_albumen_1851_1890s`
- `cyanotype_contact_process_1842_present`
- `gelatin_dry_plate_1870s_1920s`
- `autochrome_transparency_1907_1930s`
- `integral_instant_1972_onward`

이 후보군은 물질 객체 profile과 강하게 연결되지만, 연대는 메타데이터다. 동일 공정의 현대 재현이나 잘 보존된 원본도 가능하다.

### 7.2 촬영 관습 중심 후보군

- `rollfilm_brownie_snapshot_1888_1910s`
- `pictorialist_handworked_1890s_1910s`
- `new_vision_geometry_1920s_1930s`
- `fsa_owi_documentary_context_1935_1944`
- `wartime_press_flash_newsprint_1930s_1940s`
- `midcentury_bw_street_and_color_slide_1950s`
- `instamatic_flashcube_super8_1960s`
- `pocket_110_and_new_color_1970s`
- `autofocus_minilab_family_flash_1980s`
- `disposable_party_print_1990s`

[Library of Congress FSA/OWI 컬렉션](https://www.loc.gov/pictures/collection/fsa/)은 1935–1944년의 대규모 기록 프로젝트를 제공하며 흑백뿐 아니라 별도의 컬러 투명 원고도 남아 있다. 따라서 `FSA look = 흑백 + 빈곤` 같은 규칙은 금지하고, 프로젝트명은 메타데이터 또는 장면 후보로만 둔다.

### 7.3 디지털·플랫폼 후보군

- `early_compact_digicam_social_repost_2000_2004`
- `consumer_digital_web_2005_2009`
- `square_social_filter_output_2010_2014`
- `portrait_hdr_ringlight_2015_2019`
- `night_ultrawide_vertical_2020_2022`
- `computational_clean_vs_digicam_revived_2023_2026`

플랫폼의 화면 비율은 촬영 공정과 분리한다. [Meta의 2015년 공지](https://about.fb.com/ja/news/2015/08/non-square/)는 Instagram이 기존 정사각 형식에 가로·세로 형식을 추가했다고 설명한다. 따라서 정사각은 초기 유통 관습의 후보일 뿐 센서나 촬영 연도의 증거가 아니고, 9:16도 마찬가지다.

### 7.4 국내 장면 prior

국내 키워드는 별도의 `korea_scene_prior_overlay`로만 제안한다.

| 시기 후보 | 장면 원자 예시 | 사용 제한 |
|---|---|---|
| 1950s | 전후 복구, 임시 구조물, 공공 기록 사진 | 고통·빈곤을 자동 기본값으로 만들지 않음 |
| 1960s–1970s | 학교·졸업·가족 스튜디오, 산업화 거리·작업장, 흑백 인화물 | 흑백만으로 한국/연대 판정 금지 |
| 1980s | 컬러 TV, CRT, 가정 행사, 직광 플래시, 광택 인화 | 컬러 TV 하나로 1980s 판정 금지 |
| 1990s | 수학여행·학교 행사, 일회용/콤팩트, 사진 스티커, 날짜 자막 | 날짜 자막을 사실 메타데이터로 사용하지 않음 |
| 2000s | 은색 디카, 초기 SNS 재업로드, 저해상도 JPEG, 교실/노래방/PC방 장면 | 실제 계정·서비스·기기 모델 추론 금지 |
| 2010s | 스마트폰, 카페·flat lay·정사각 유통, golden-hour lifestyle | Instagram 라벨만으로 hard 활성화 금지 |
| 2020s | 네 컷 포토부스, 0.5× 초광각, 9:16, Y2K·디카 재현 | 현재 장면과 재현 대상 시대를 이중 기록 |

[국가기록원](https://theme.archives.go.kr/next/photo/homeAppliances02List.do)은 국내 컬러 TV 시판 허용과 컬러 방송 시작을 1980년으로 기록한다. 이는 장면 소품의 가용성 경계만 지지하며, 사진 자체의 색 재현 방식이나 개별 가정의 보급 시점을 증명하지 않는다. 국내 prior는 향후 국가기록원·대한민국역사박물관의 연대가 확인된 사진 표본을 장르별로 수집해 검증해야 한다.

## 8. 후보팩 활성화 정책

### 8.1 hard 활성화

- 정확하고 좁은 문구가 다섯 구성요소를 직접 요구할 때만 hard profile을 연결한다.
- `1840년대 사진`, `1970년대 사진`, `옛날 사진`, `레트로`, `필름 느낌`, `Kodak`, `Polaroid`, `CCD`, `Instagram 감성`은 hard profile 0개다.
- broad 시대어는 2–4개 후보 family를 반환하고 사용자가 공정·장르·출력물·지역을 선택할 수 있게 한다.
- BM25F/embedding hit는 후보 발견 신호일 뿐 hard 의무가 아니다.
- 사용자의 명시적 공정 정의가 레지스트리 기본과 충돌하면 먼저 명확화한다.

### 8.2 후보 우선순위

1. 사용자가 명시한 촬영 공정과 출력물.
2. 사용자가 명시한 장르·상황·지역.
3. 공정과 모순하지 않는 촬영 반응.
4. 별도 선택 가능한 열화와 후대 재현.
5. 마지막에만 생활문화 scene prior.

예를 들어 `1970년대 즉석사진`은 `integral instant print object`를 우선하며, 110·노란색 cast·light leak을 자동으로 덧붙이지 않는다. `2000년대 싸이월드 디카`는 기존 `early_2000s_compact_digicam_social_repost`를 재사용하되 실제 싸이월드 계정이나 CCD 센서를 주장하지 않는다.

### 8.3 충돌 규칙

- `daguerreotype mirror surface`와 `silver mirroring deterioration`은 서로 다른 주 소유자다.
- `calotype paper fiber`와 `paper texture overlay`는 이미지층 귀속 여부로 나눈다.
- `wet collodion coating trace`와 `global grunge`는 국소성·판 경계로 나눈다.
- `albumen`과 `sepia`는 지지체·binder·mount 관계로 나눈다.
- `Autochrome mosaic`와 `digital pixel grid`는 물리 투명판과 모자이크 규모·귀속으로 나눈다.
- `Pictorialism`과 단순 blur는 선택적 초점·인화 표면으로 나눈다.
- `New Vision`과 Dutch angle은 구조적 대각·스케일 전도로 나눈다.
- `press flash newsprint`와 1990s party flash는 출력 컨테이너와 사건 프레이밍으로 나눈다.
- `instant print`와 fake border는 물체 두께·전체 경계·그림자로 나눈다.
- `computational HDR look`과 aggressive HDR filter는 halo·전역 평탄화·경계 일관성으로 나눈다.
- `chromogenic fade`와 warm grade는 가려진 비교 영역과 염료별 불균등 손실로 나눈다.

## 9. 회귀·평가 계약

`routing-regression-proposal.jsonl`은 다음 유형을 포함한다.

- broad-negative: 시대명·상표·무드만 있는 입력은 hard profile 0개.
- narrow-positive: 다섯 구성요소를 모두 포함한 한·영 문구가 하나의 primary owner로 연결됨.
- component-ablation: 구성요소 하나를 제거하면 해당 profile이 통과하지 않음.
- confound/collision-negative: 가장 가까운 대체물이 잘못된 profile을 활성화하지 않음.
- metadata-boundary: 실제 연도·작가·기기·플랫폼 계정·원본성은 별도 필드에 남음.
- dual-time: 현재 장면과 재현하려는 과거 룩을 별도 시간 필드로 보존함.

구현 후 필요한 검증은 다음 순서다.

1. 후보·profile ID 고유성, source ID 연결, 각 profile의 구성요소 5개와 reject 5개 구조 검사.
2. shared source extension을 통한 병합 후 visual-profile/semantic index 재생성.
3. 한·영 exact, broad-negative, component-ablation, collision 회귀.
4. candidate-pack v6 배열에서 source/core/prompt/request lineage와 후보 ID 노출 확인.
5. 서로 다른 공정·디지털·열화 profile의 독립 렌더 arm. arm마다 고정 prompt·pack·request·hash, 1회 생성, 교차 입력 없음.
6. thumbnail/native에서 5/5 strict gate 판정. 부분 충족은 실패.
7. 프롬프트/런타임 PASS, 이미지 전달, 픽셀 PASS, 사용자 선호를 별도 결과로 기록.

## 10. 우선 구현 순서

### P0 — 오탐 감소와 물질 공정

1. `sepia`의 영어 설명을 `sepia-toned color treatment`처럼 나이 주장 없는 표현으로 교정.
2. 다게레오타입, 칼로타입, 습판 콜로디온, 알부민, cyanotype, Autochrome, 즉석 인화물, 슬라이드 마운트 8개 object/process profile.
3. 은경화·acetate channeling·chromogenic fade 3개 열화 profile을 별도 레지스트리 차선으로 추가.
4. broad 시대/상표 0-hard 규칙과 충돌 회귀를 먼저 잠금.

### P1 — 촬영 관습과 소비자 출력

1. Pictorialism, New Vision, press-flash/newsprint, late-century minilab 4개 profile.
2. Brownie, FSA, 126, 110, Super 8, 일회용 카메라, 1990s date print는 후보군으로 추가하고 hard 연대 판정을 금지.
3. 기존 `physical_print_scan_material_context`, `contact_sheet_selection_context`, `early_2000s_compact_digicam_social_repost`와 중복되지 않게 primary owner를 지정.

### P2 — 계산사진·지역 prior

1. 초광각 원근, computational HDR look, computational low-light look 3개 profile.
2. 정사각·9:16은 output-container candidate로만 추가.
3. 국내 decade prior는 연대가 확인된 박물관·아카이브 표본을 장르별로 추가 수집한 뒤 활성화.

## 11. 한계와 후속 조사

- 사진 공정의 외관은 보존 상태, 스캔, 색 관리, 재인화에 따라 달라진다. 공정 profile도 진품 감정 계약이 아니다.
- Autochrome 모자이크·알부민 crackle·은경화처럼 native scale이 필요한 단서는 썸네일만으로 판정할 수 없다.
- 126·110·일회용 카메라·compact CCD의 “룩”은 렌즈, 노출, 인화, 스캔과 함께 형성되어 단일 장치명으로 고정할 수 없다.
- Pictorialism, New Vision, FSA, New Color, New Topographics는 사진사적 범주이며 한 장의 구도·색만으로 저자나 운동 소속을 증명하지 않는다.
- 계산사진은 잘 작동할수록 합성 흔적이 보이지 않을 수 있다. proposed profile은 실제 알고리즘이 아니라 요청된 결과 look만 평가한다.
- 국내 decade prior는 현재 가용성 경계와 일부 공공 컬렉션 사례만 확보했다. 인구집단 대표성이나 “한국의 전형적 사진”을 주장하지 않는다.
- 브랜드·필름 주식의 색 재현은 제조 시기, 노출, 현상, 스캔에 따라 달라진다. `Kodachrome`, `Tri-X`, `Kodak Gold`, `Polaroid SX-70`는 명시적 요청 메타데이터와 bounded look 후보로만 유지한다.

## 12. 핵심 출처

- [Victoria and Albert Museum — A to Z of photographic processes](https://www.vam.ac.uk/articles/photographic-processes)
- [Canadian Conservation Institute — Caring for photographic materials](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/photographic-materials.html)
- [Canadian Conservation Institute — Care of encased photographic images](https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-encased-photographic-images.html)
- [Library of Congress — Care, handling, and storage of photographs](https://www.loc.gov/preservation/care/photolea.html)
- [Library of Congress — Deterioration of negatives](https://www.loc.gov/collections/genthe/articles-and-essays/deterioration-and-preservation-of-negatives-autochromes-and-lantern-slides/negatives/)
- [Art Institute of Chicago — Pictorialism](https://archive.artic.edu/stieglitz/pictorialism/)
- [Metropolitan Museum of Art — Moholy-Nagy and New Vision source](https://resources.metmuseum.org/resources/metpublications/pdf/Recent_Acquisitions_A_Selection_2004_2005_The_Metropolitan_Museum_of_Art_Bulletin_v_63_no_2_Fall_2005.pdf)
- [Library of Congress — FSA/OWI collection](https://www.loc.gov/pictures/collection/fsa/)
- [Kodak — Milestones](https://www.kodak.com/en/company/page/milestones/)
- [Smithsonian National Museum of American History — Polaroid SX-70](https://americanhistory.si.edu/collections/object/nmah_689070)
- [NIST — JPEG compression artifact study](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=908515)
- [National Archives — Digital photographic records](https://www.archives.gov/records-mgmt/initiatives/digital-photo-records.html)
- [Google Research — Burst photography for HDR and low light](https://research.google/pubs/burst-photography-for-high-dynamic-range-and-low-light-imaging-on-mobile-cameras/)
- [Google Research — Night Sight](https://research.google/blog/night-sight-seeing-in-the-dark-on-pixel-phones/)
- [Apple — HDR camera guidance](https://support.apple.com/en-mide/guide/iphone/iph2cafe2ebc/ios)
- [Sony — Focal length, angle of view, and perspective](https://www.sony.com/lr/electronics/focal-length-angle-of-view-perspective)
- [Apple — 0.5× Ultra Wide camera guidance](https://support.apple.com/fr-fr/102443)
- [Meta — Instagram landscape and portrait formats](https://about.fb.com/ja/news/2015/08/non-square/)
- [국가기록원 — 컬러텔레비전 등장](https://theme.archives.go.kr/next/photo/homeAppliances02List.do)

## 13. 주장 경계

이 보고서가 입증한 것은 다음뿐이다.

- 참조 대화의 키워드를 공정·물질·촬영 반응·장르·출력·열화·재현·장면 prior로 분해할 수 있다.
- 공공기관·박물관·제조사·공식 기술 자료를 통해 18개 좁은 시각 계약과 23개 후보군을 제안할 근거가 있다.
- 현재 저장소의 중복 지점과 오탐 위험을 확인했고, 이를 검증할 라우팅·절삭·충돌 회귀안을 만들었다.

이 보고서는 런타임 구현, 검색 노출, composed prompt 전달, 이미지 생성 성공, 픽셀 충족, 사용자 미감 만족을 입증하지 않는다.
