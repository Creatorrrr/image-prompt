# 전기·번개·전자 시각 의미 데이터 확장 리서치

연구일: 2026-10-08, Asia/Seoul. 요청 범위는 상세 리서치와 반영 계획이다. 이 폴더는 연구 산출물이며, 현재 스킬의 원본 데이터·인덱스·실행 코드를 바꾸지 않았다.

## 핵심 결론

전기라는 단어를 하나의 번개 모양으로 바꾸는 방식으로는 데이터가 충분해지지 않는다. **무엇이 발생시키고, 어떤 매질에서, 어디와 연결되며, 무엇을 밝히거나 변형하는지**를 각각 저장해야 한다. 전하·전류·전압·자기장처럼 직접 보이지 않는 개념은 계측·물리적 결과·명시적인 설명 모형으로 표현하고, 창작 설정과 비유는 그 의미를 유지한다.

반영의 최소 단위는 다음과 같다.

> 의미·문맥 → 관측 모드 → 발생원/대상/매질 → 보이는 구성요소 → 방향이 있는 관계 → 혼동 경계 → 변경하는 속성 → 필요한 증거와 판정 한계

이번 패키지에는 원문 키워드 **435개**, 상세 연구 카드 **116개**, 후보 설계 초안 **95개**, 출처 레코드 **42개**를 담았다. 116개는 71개 직접 관측 표현, 12개 설명 모형, 8개 시간 기록, 6개 광학·장면 응용, 11개 창작 설정, 7개 문맥 카드, 1개 보고된 희귀 현상으로 나뉜다. 이 숫자는 조사 자료의 규모이며 런타임 등록·검색·선택·픽셀 검증이 완료됐다는 뜻이 아니다.

24개 P0 카드부터 검토하고, 54개 P1은 인접 영역을 확장하며, 38개 P2는 추가 출처·판본 확인 또는 분해가 필요하다. 15개 family 카드는 단일 후보로 활성화하지 않는다. 435개 seed 중 280개는 상세 카드와 연결됐고, 155개는 비가시적 의미·기기 판본·관측 조건에 대한 후속 경로를 기록했다. **435개 모두를 독립적으로 실증 검증했거나, 각각을 시각 원자로 만들었다고 주장하지 않는다.**

## 1. 참조 대화 복구와 조사 근거

[‘전기 용어 조사’](https://chatgpt.com/c/6ac64461-ac10-83ee-877a-636d18d1595f)의 조회 응답은 20,000자에서 잘렸다. 별도 브라우저의 보이는 대화에서 16–26번 범주를 복구했고, 앞부분과 합친 435개 키워드의 순서·문자열을 브라우저 목록과 대조했다. 비교값은 `60b23815`이며 재구성 목록과 일치한다. 이는 목록 복구 검사이고, 원래 ChatGPT의 설명이나 출처가 모두 정확하다는 검증은 아니다.

- 26개 번호 범주, 28개 키워드 표, 키워드 435행.
- 원문 마지막의 장면 조합 예시 5개는 키워드 수에서 제외했다.
- 원문 23번 범주의 문화 도상과 새 창작 명칭, 25번의 형태와 음향 표는 별도로 유지했다.
- 원문 전체 prose를 완전한 원문 파일로 확보한 것은 아니다. 잘린 조회 결과, 복구한 목록, 일부 읽은 후반부 설명의 경계를 보존했다.

[키워드 원문 목록](SEED-KEYWORDS.json), [항목별 처리 ledger](SEED-COVERAGE.tsv), [잘린 조회 원문](REFERENCE-EXCERPT.json)에 근거를 남겼다. 출처의 실제 읽기 수준은 [SOURCES.json](SOURCES.json)에 있다. PPPL 자료는 검색에 노출된 도표 설명까지만 확인했고 PDF 재조회와 스크린샷이 실패했다. Johns Hopkins 페이지는 술어·의료 문맥 수준의 근거다. 이 두 자료의 상세 도표·장치 geometry를 검증했다고 표시하지 않았다.

## 2. 원문 범주를 데이터로 바꾸는 처리

| 범주 | 원문 행 | 데이터에서 보강할 핵심 | 적용 경계 |
|---|---:|---|---|
| 1 전기 기본 개념 | 18 | 전하·전위·전압·전류·전력·에너지 구분 | 수치/숨은 상태를 빛의 형태로 치환하지 않음 |
| 2 입자·원자 | 20 | 전자·정공·양전자·오비탈·전자빔의 관측 모드 | 모형, 검출 결과, 육안 사진의 구분 |
| 3 재료·물성 | 16 | 도체/절연체/반도체/유전체/초전도체 | 외형만으로 전도성·초전도성 확정 금지 |
| 4 단위 | 15 | 단위 표기, 계기·축·값의 문맥 | Tesla 단위와 Tesla coil 장치를 분리 |
| 5 회로·신호 | 22 | 폐회로·개방·직렬·병렬·노드와 파형 | 접속 topology와 시간 변화는 별개 |
| 6 전자기 | 18 | 코일·기계적 결과·장선 설명 모형 | 보이지 않는 장과 실선의 구별 |
| 7 방전·플라즈마 | 16 | spark/arc/corona/glow/streamer/globe | 과정·물질 상태·장치·형태 분리 |
| 8 번개 종류 | 17 | cloud/ground/air 종점·분기·관측 위치 | 색으로 극성 판정하지 않음 |
| 9 뇌우 과정·동반 현상 | 16 | 연결된 구름, 용융 흔적, 돛대 발광 | 전하분리·기류는 모형, 천둥은 음향 |
| 10 상층대기·우주 | 13 | TLE의 높이 관계·기점·분리, 오로라·태양 | 제트/스프라이트/감마선/코로나 혼동 방지 |
| 11 부품 | 17 | 케이스·단자·권선·기판·광원 구조 | 외형과 증폭·접합·밴드갭의 구분 |
| 12 발전·저장·변환 | 18 | 케이블·포트·셀·모듈과 연결 | charging/discharging 방향은 로그/문맥 |
| 13 전력 시설 | 16 | conductor–insulator–support와 장치 접속 | 기기 등급·정전 원인을 외형으로 추정하지 않음 |
| 14 조명·열·동력 | 16 | 필라멘트/기체/LED, rotor/stator/plunger | 점등·회전·소리가 선택됐는지 확인 |
| 15 통신·계측 | 14 | probe–node–instrument–display 관계 | 무선 파형이나 실제 값은 별도 기록 |
| 16 전기화학 | 14 | 전극–용액–기포–도금층의 owner | 반응 역할과 단자 부호는 문맥 의존 |
| 17 생체전기 | 17 | 어류 형태, 막·이온·신호 모형 | 생물 사진에 번개를 자동 추가하지 않음 |
| 18 의료 | 15 | 기록/자극 장치, lead–pad–같은 환자 관계 | 진단·동의·치료 성과는 시각 gate 아님 |
| 19 사고·손상 | 18 | 사고 기점, 표면 흔적, 광·비산물 분리 | 고장 원인·상해·사망을 pose로 판정하지 않음 |
| 20 보호·차폐 | 14 | terminal/strap/enclosure와 연결 | 보호 성능·규정 준수는 외형이 증명하지 않음 |
| 21 역사 장치 | 12 | 유물 판본의 disc/layer/terminal/tube | 오래된 광고 효능과 장치 형태 구분 |
| 22 무기·강압·성인·의료 | 10 | 용도 의미와 기기 외형을 분리해 보존 | 장치 하나로 용도·동의·무해함 추론 금지 |
| 23 도상·창작 명칭 | 13 | 문화별 유물·도상, 창작 carrier | 도상 판본과 새 설정의 근거 분리 |
| 24 비유 | 18 | literal/figurative 문맥과 실제 반응 | 교감·휴식·피로를 공중 방전으로 치환하지 않음 |
| 25 형태·표면·음향·촬영 | 30 | 발광원·수광면·광학 효과·흔적·시간 | 빛/입자/반사/소리의 carrier를 구분 |
| 26 판타지·SF | 22 | 발생원–대상–경로–기점–반응 | 검증된 자연 현상으로 승격하지 않음 |

## 3. 방전은 발생 위치와 연결 관계로 구분한다

전기 방전과 플라즈마를 동의어로 저장하면 기체 상태, 전하 이동 과정, 장치의 외형이 섞인다. 전하 입자로 이루어진 상태는 [ITER의 플라즈마 설명](https://www.iter.org/index.php/fusion-energy/making-it-work)에서 확인했고, 기체 방전의 서로 다른 관측 표현은 [대학의 전기 시연 자료](https://sprott.physics.wisc.edu/demobook/CHAPTER4.HTM)를 대조했다. 핵융합 플라즈마의 온도·밀도를 모든 작은 방전에 옮기지 않는다.

| 선택 표현 | 발생원·종점·매질 | 보이는 구별점 | 대표 오인 |
|---|---|---|---|
| 짧은 스파크 | 두 가까운 금속 끝·공기 간극 | 끝점에 닿는 짧은 불규칙 통로 | 연마 입자·독립 반짝이 |
| 아크 | 두 전극·연속 전도성 기체 경로 | 집중된 발광 기둥과 양쪽 부착부 | 국소 코로나·네온관 |
| 코로나 | 뾰족한 도체 부근 기체 | 도체 가까이 붙은 작은 광역 | 도체 전체를 잇는 긴 아크 |
| 관 속 glow | 같은 관·끝 전극·기체 | 외피 안의 비교적 넓고 부드러운 광역 | LED 점열·관 밖 번개 |
| streamer 형태 | 기점 전극·분기 기체 통로 | 가는 필라멘트와 연결된 작은 가지 | 실제 전선·굵은 기둥 |
| plasma globe | 중앙 전극·유리구 내부 | 중앙에서 유리 안쪽으로 가는 줄기 | 자연 구상번개·마법구 |

스파크의 짧음, 아크의 지속성, streamer의 성장 방향 같은 시간적 정의는 한 프레임으로 검증할 수 없다. 이미지는 형태·기점·종점만 평가하고 시간 기록이 필요하면 별도 검증 대상으로 둔다. [MIT의 코로나 연구](https://news.mit.edu/2020/airplanes-counteract-st-elmos-fire-thunderstorms-0811)는 뾰족한 도체의 국소 발광과 성 엘모의 불을 설명한다. ‘corona’라는 문자열만으로 태양 코로나를 같은 의미에 넣지 않는다.

**공통 팔레트를 필수값으로 지정하지 않는다.** 기체·여기 상태·장치에 따라 광색이 달라지고, 촬영 노출·화이트밸런스도 외형에 영향을 준다. [Smithsonian의 발광 설명](https://hte.si.edu/Activities/HTE_ActivityGuide.pdf)을 근거로 색은 선택 가능한 표현값에 남긴다. 청백색 중심과 보라색 가장자리는 별도 광학·색 카드이며, 전압·위험도·양극성의 표식이 아니다.

## 4. 번개·TLE는 공간 topology가 핵심이다

[NWS의 번개 종류 설명](https://www.weather.gov/safety/lightning-science-types-flashes)은 구름 내부와 지면 연결, leader와 return stroke를 구분한다. 사진용 데이터에는 기점·종점이 실제로 보이는지 먼저 기록한다. 공중에서 끝난 듯 보여도 화면 밖 종점이 잘렸다면 cloud-to-air의 확인으로 사용하지 않는다. 상향 번개는 탑 꼭대기의 부착·상부 분지를 보여줄 수 있지만 실제 시작 방향은 시간 기록이 필요하다.

[열번개 설명](https://www.weather.gov/safety/lightning-heat)에 따르면 heat lightning은 먼 뇌우에서 온 섬광이다. 열기·증기·별도 색의 번개를 필수 형태로 만들지 않는다. 천둥이 안 들렸다는 정보 역시 사진 자체의 증거가 아니다.

TLE 카드는 색보다 **운정에 연결됐는지, 운정과 분리됐는지, 고리인지, 지평선 위 대기 구조인지**를 먼저 구분한다.

| 현상 | 우선할 시각 관계 | 강제하면 안 되는 정보 |
|---|---|---|
| 스프라이트 | 뇌우 훨씬 위의 기둥/촉수, 운정과 분리 | 모든 경우의 같은 모양·실측 고도 |
| 블루 제트 | 운정에 붙은 좁은 상향 구조 | 한 프레임에서 성장 속도 |
| 자이언틱 제트 | 운정의 좁은 하부와 넓게 갈라진 상부 연결 | 스프라이트와 색만으로 동치 |
| ELVES | 뇌우 위 고리와 중심 관계 | 단일 프레임에서 확장 속도·EMP량 |
| 오로라 커튼 subtype | 지평선, 아크, 같은 커튼 속 수직 광선 | 모든 확산 오로라에 커튼 강제 |
| TGF | 검출기·광자 기록·설명 도해 | 공중의 보라색 광선 |

근거: [NASA의 상층대기 구분](https://www.nasa.gov/image-article/upper-atmosphere-phenomena-caused-by-thunderstorms/), [운정에서 시작하는 제트와 분리된 스프라이트의 비교](https://science.nasa.gov/science-research/heliophysics/a-gigantic-jet-caught-on-camera-a-spritacular-moment-for-nasa-astronaut-nicole-ayers/), [오로라의 아크와 커튼](https://science.nasa.gov/earth/earth-observatory/auroras-dancing-in-the-night/).

구상번개는 보고된 현상의 관측·재현 카드로 둔다. [Cen·Yuan·Xue의 관측 논문](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.112.035001)은 분광 관측 사례를 제공하지만 모든 사례의 생성 원리·색·크기를 규격화하지 않는다. 작은 빛구슬이 검색됐다는 이유만으로 자연 구상번개라고 판정하지 않는다.

## 5. 회로·계측·설비는 물건 목록보다 연결을 보강한다

[직렬·병렬 회로](https://openstax.org/books/university-physics-volume-2/pages/10-2-resistors-in-series-and-parallel)는 부품의 화면상 위치가 아니라 접속 관계로 구분한다. 직렬은 한 경로의 연속 부하, 병렬은 같은 두 노드를 공유하는 별도 가지다. 선이 교차하는 그림에는 실제 접속점이 있는지 확인한다. ‘two wires’나 ‘two lamps’만으로 관계가 충족되지 않는다.

장치별로 다음 연결을 카드에 넣는다.

- `source terminal → outgoing wire → load → return wire → other terminal`
- `probe tips → selected circuit nodes → same meter → same display`
- `winding → same core → winding terminals`
- `conductor → insulator assembly → tower arm`
- `electrode → same bath → local bubbles/coating → same workpiece`
- `central electrode → filaments → inner glass boundary`

계기 화면은 [Tektronix의 전압·시간 축 설명](https://www.tek.com/en/documents/primer/setting-and-using-oscilloscope), 전압계/전류계의 서로 다른 접속은 [OpenStax 계측 설명](https://openstax.org/books/university-physics-volume-2/pages/10-4-electrical-measuring-instruments)으로 대조했다. 계기의 형상·값·축·측정 mode를 따로 기록하고, 화려한 sine wave를 공중의 실제 전류로 표현하지 않는다. 실제 계측 정확도는 화면 모양 검증과 별개다.

[EIA의 전력 전달 설명](https://www.eia.gov/energyexplained/electricity/delivery-to-consumers.php)은 전력망의 연결을 뒷받침한다. 한국 시설의 애자 개수·전선 색·장치 배치를 미국 자료로 고정하지 않는다. 보호접지·차폐·RCD·SPD·퓨즈는 표면에 보이는 연결/상태와 실제 기능을 구분하고, 판본 자료가 부족한 카드는 P2로 남겼다.

## 6. 재료·조명·전기화학·흔적의 carrier를 구분한다

필라멘트 가열, 기체 방전관, LED package는 서로 다른 발생체다. [DOE의 전구 역사](https://www.energy.gov/articles/history-light-bulb), [LED 설명](https://www.energy.gov/cmei/ssl/led-basics)을 대조해 발광원 구조를 작성했다. 같은 관형 외피의 LED 대체품이나 filament LED도 있으므로 외피 하나로 내부 기전을 판정하지 않는다. [점멸 설명](https://www.energy.gov/cmei/ssl/flicker-basics)은 시간 기록의 필요성을 뒷받침한다. 카메라 banding만으로 교류·주파수·고장을 확정하지 않는다.

금속의 반사색, 방전 광원색, 젖은 바닥 반사, 전역 color grading은 서로 다른 데이터다. 번개 반사는 **실제 광원과 같은 프레임의 수면/노면, 대응 위치, 끊김·차폐, 젖고 마른 경계**를 별도로 기록한다. 단순 푸른 세로 선을 ‘전광 반사’로 채택하지 않는다.

[전기분해·도금 설명](https://openstax.org/books/chemistry-2e/pages/17-7-electrolysis)에 따라 전극·같은 액체·기포·도금 표면을 묶는다. 애노드는 산화, 캐소드는 환원의 역할이며 단자 부호는 셀의 동작 문맥에 따라 구분한다. 사진에서 보이는 기포에 수소·산소를 색으로 구분하는 규칙은 만들지 않는다.

손상 데이터는 `발생 현상`, `표면 흔적`, `인체 반응`, `원인 문맥`을 분리한다. [OSHA의 아크 플래시 자료](https://www.osha.gov/electrical/flash-hazards)는 광·열·가스·비산 효과를 구분하는 근거다. 그을린 단자나 녹은 피복만으로 단락·과부하·누전의 원인을 확정하지 않는다. ESD 고장에 반드시 큰 불꽃이나 탄 기판이 보인다는 규칙도 만들지 않는다.

풀구라이트는 [NPS가 설명한 유리질 낙뢰관](https://www.nps.gov/articles/grsa-fulgurites.htm)의 표면·속벽·기질 관계로 연구했다. 피부의 분지 홍반은 [Lichtenberg 사례 연구](https://pmc.ncbi.nlm.nih.gov/articles/PMC8226253/)의 관측 형태와 판정 한계를 따로 둔다. 이마의 짧은 지그재그 흉터, 고체 안의 분지 패턴, 피부의 홍반은 서로 다른 carrier와 시간 의미다. 형태가 닮았다는 이유로 같은 profile을 재사용하지 않는다.

## 7. 생체·의료·성인·강압 용어도 의미 데이터에 유지한다

전기뱀장어는 [Smithsonian의 형태·발전기관 설명](https://www.nationalzoo.si.edu/animals/electric-eel)을 확인했다. 어류 외형과 물속 전기 기능을 분리하고, 현실 생물 주변에 가시 번개를 기본값으로 더하지 않는다. 막전위·활동전위는 [막과 이온 통로의 설명](https://openstax.org/books/anatomy-and-physiology-2e/pages/12-4-the-action-potential)에 근거한 과학 모형/계측 문맥으로 둔다.

심전도는 기록, 제세동기와 다른 자극 장치는 별도의 기능이다. [NHLBI의 AED 설명](https://www.nhlbi.nih.gov/health/defibrillators/how-do-defibrillators-work)을 근거로 pad–lead–same patient–same device 관계를 작성했다. 단일 장면의 파형·움찔하는 pose로 임상 진단이나 성공적인 소생을 판정하지 않는다. [NIMH의 ECT·TMS 구분](https://www.nimh.nih.gov/health/topics/brain-stimulation-therapies/brain-stimulation-therapies)을 유지하며 TMS의 외부 코일을 피부 전극 장치와 동치로 넣지 않는다.

원문 22번의 전기 고문, 전기적 성적 자극, electroplay, violet wand, violet ray, electroejaculation, CED/TASER, contact stun device, railgun을 전부 seed ledger에 보존했다. 이 용어들의 차이는 장치 형태 하나로 확정되지 않는다.

| 의미 | 데이터에 보존할 내용 | 자동 추가하지 않을 내용 |
|---|---|---|
| electroplay / E-stim | [문화상 용어의 사용](https://dame.com/blogs/sexual-wellness/exploring-electrosex-and-sensation-play), 기기와 액세서리 문맥 | 임의의 성행위·몸 부착·동의·감각 |
| violet ray / wand | [역사적 교체 유리 전극과 케이스](https://collection.sciencemuseumgroup.org.uk/objects/co142222/high-frequency-violet-ray-apparatus-england-before-1966), 서로 다른 용도 문맥 | 검증된 치료 효능·의료 장치와의 동치 |
| electroejaculation | [생식의료의 술어와 문맥](https://www.hopkinsmedicine.org/health/treatment-tests-and-therapies/penile-vibratory-stimulation-and-electroejaculation) | 임의 시술 geometry·성인 감각 놀이와의 동치 |
| CED / TASER / contact stun | [NIJ의 장치 범주](https://nij.ojp.gov/topics/articles/conducted-energy-devices-policies-use-evolve-reflect-research-and-field-deployment)와 방식 구분 | 실제 제압 성공·무해함·운용 절차 |
| railgun | [미 해군의 시험 자료](https://www.dvidshub.net/video/539084/navy-railgun-successfully-fires-multi-shot-salvos)와 전자기 가속 문맥 | 번개 자체를 탄환으로 발사한다는 현실 정의 |
| 전기 고문 | 강압 사건의 의미와 actor/affected-person 구분, 전용 인권·법의학 자료의 후속 조사 | 전극만으로 강압·동의·상해·사망 판정 |

용어를 의미 ledger에 보관하는 것과, 그 용어에서 특정한 시각 후보·행위 template를 자동 생산하는 것은 다른 단계다. 이 문맥 카드는 독립 시각 atom이 없으며 현재 후보 설계에서 제외했다. 조사 후 특정 요청이 주어지면 그 요청의 실제 의미와 장치 판본을 기준으로 형태를 작성해야 한다.

## 8. 도상·판타지·비유에는 다른 반영 규칙이 필요하다

금강저는 [British Museum의 특정 유물](https://www.britishmuseum.org/collection/object/A_1885-1227-58)을 기준으로 손잡이·양끝·선택 갈래 형태를 조사했다. 뇌신의 북은 [Sōtatsu 도상의 설명](https://archive.asia.si.edu/sotatsu/object.asp?id=ELS2015.6.44.1-2), 토르의 망치형 펜던트는 [박물관 안내](https://www.britishmuseum.org/sites/default/files/2021-05/large_print_guide_room_41.pdf)를 근거로 한다. 모든 뇌신에 북·망치·같은 복장을 넣거나 모든 금강저에 같은 갈래 수를 요구하지 않는다. 제우스 도상과 double vajra의 개별 판본은 후속 출처 확인 대상으로 명시했다.

창작 설정은 실제 과학 주장과 분리하면서 구체적인 관계를 쓴다. 예를 들어 chain lightning은 한 손에서 여러 대상으로 나가는 starburst와 다르다. source→target A→target B의 서로 다른 구간과 target의 identity를 보존해야 한다. armor는 몸을 따라가는 층, barrier는 몸 밖의 경계이며 같은 aura로 대체하지 않는다. weapon family는 spear/blade/whip을 각각 원자로 나눈 뒤 사용한다.

‘흑뢰’는 창작 설정이다. 빛을 내지 않는 어두운 채널, 밝은 rim과의 대비 등 요청에 맞는 실현을 선택할 수 있지만 검은 빛이 현실의 번개 등급이라는 규칙은 만들지 않는다. EMP는 기기 반응과 원인 문맥을 표현하고 보편적인 가시 구체 충격파를 강제하지 않는다. 전기적 소생은 실제 AED의 효능으로 바꾸지 않는다.

한국어 ‘전기가 통하다’, ‘방전됐다’, ‘충전하다’, ‘전광석화’, ‘스파크가 튀다’는 전체 문맥에서 의미를 판별한다. 관계·휴식·피로·갑작스러운 행동을 각각 보존하며, 사진에 전선·번개·불꽃을 자동 추가하지 않는다. 비유 카드는 고정 표정이나 하트 그래픽의 근거가 아니다.

## 9. 현재 데이터와 대조한 반영 후보

정적 대조 범위는 기본 candidate/profile 파일 2개와 manifest 등록 extension 102개, 총 104개다. 후보 10,531행과 profile 2,321행을 읽었으며 이는 **중복·확장·덮어쓰기 전 원본 행수**이지 실제 compiled corpus나 최신 런타임 검색 결과 수가 아니다. 정규식 관련 hit는 82개이며, 오인 예시의 언급과 `coronation` 같은 비관련 substring도 포함한다. 검색 결과의 존재/부재로 완전성을 판정하지 않았다. [정적 대조 자료](REPO-COVERAGE.json)를 남겼다.

| 연구 의미 | 확인한 기존 ID | 반영 결정 |
|---|---|---|
| 머리카락의 대전 형태 | `static_hair_charge` | 같은 carrier의 보강 또는 좁은 sibling |
| 천의 국소 달라붙음 | `static_cling_fabric` | wetness·transmission 자동 추가 없이 보강 |
| 유리관 간판 구조 | `neon_sign`, `neon_sign_light` | 기존 빗물·광원 spill 의미를 보존하고 구조 sibling |
| 오로라 커튼 | `auroral_arc_curtain_atmosphere` | 같은 complete subtype일 때 재사용 |
| 적란운 구조 | `cumulonimbus_tower_anvil_precipitation_outflow` | 기존 강수·outflow 의무를 축약하지 않고 비교 |
| 젖은 지면 반사 | `wet_surface_light_reflection_owner_relation` | 기존 5개 관계를 모두 만족할 때 재사용 |
| 피부 분지 홍반 | `appearance_h058`, `appearance_rel_h058` | 이마 흉터와 구별하는 새 sibling |
| 태양 코로나 관측 | `cme_coronagraph_snapshot` | CME 전면을 요구하지 않는 별도 의미 |
| 코일 장치 | `punk_teslapunk_mechanism_prop` 등 | 세계관 설비는 재사용하고 구체 장치 원자 분리 |
| 단자 손상 | `technical_overload_progressive_failure` | 흔적 하나를 연쇄 고장 전체와 동치로 넣지 않음 |

## 10. 반영 가능한 데이터 형태와 완료 경계

[research.json](research.json)은 의미·관측 모드·구성요소·local role·관계·혼동·출처·한계·우선순위를 저장한다. [CANDIDATE-BLUEPRINTS.json](CANDIDATE-BLUEPRINTS.json)은 긍정적인 component 문장, 관계, 제안 slot과 property 범위를 담는다. source URL·거절 예시·연구 상태를 positive embedding text에 넣지 않았다.

이 초안의 target/property는 실제 consumer에 대한 매핑 검증 전이다. graph 문자열이 있다는 사실만으로 runtime owner resolution이 작동하는 것은 아니다. prop·aftermath_trace처럼 현재 기본 slot dimension이 비어 있는 영역은 명시적인 실제 effects를 검토해야 한다. 근거 없이 빈 배열을 ‘변경 없음’으로 해석하지 않는다. 가족 카드와 문맥 카드에는 단일 후보를 만들지 않았고, P2 초안을 포함한 모든 blueprint는 `runtime_ready: false`다.

연구 자료는 외부 evidence 폴더에 남긴다. 상세 의미를 SKILL.md·pre-core catalog에 옮기거나, 전체 키워드 dump를 runtime 사전으로 넣지 않는다. 새 파일 등록, semantic/visual index 재생성, 실제 후보 노출·선택, prompt/runtime audit, 원본 픽셀과 사용자 판단은 [반영 계획](IMPLEMENTATION-PLAN.md)의 후속 단계다.

이번에 완료한 것은 원문 목록 복구, 주요 의미와 관계의 출처 대조, 정적 기존 데이터 비교, 연구 카드·후보 설계·후속 검증 계획의 구조 검사다. 런타임 통합, 임베딩 호출, 이미지 생성, 픽셀 판정, 커밋·푸시는 실행하지 않았다.
