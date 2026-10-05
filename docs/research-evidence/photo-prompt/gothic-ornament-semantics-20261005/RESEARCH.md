# 고딕·장식 디테일의 시각 의미와 후보 데이터 강화 연구

2026-10-05 KST · **연구와 반영 계획 완료 / 활성 데이터 채택·이미지 검증 미실행**

장식 디테일을 강화하려면 **무엇이 얼마나 많이 있는지, 어떤 구조로 연결되는지, 어느 대상에 붙는지, 최종 이미지에서 어디까지 읽히는지**를 함께 기록해야 한다. `Gothic Maximalism`, `Ornate Gothic`, `Gothic Baroque`는 이를 결합한 제작 표현으로 다룬다. 역사적 고딕·바로크의 분류와 같은 단일 양식으로 등록하지 않는다.

이번 결과는 참조 대화에서 복원한 **124개 표 항목**, 연구자가 보충한 **20개 관계**, **71개 후보 초안·12개 조합 초안**, **92개 의미/잠금 회귀 계획·22개 원본 픽셀 사례**다. 60개 출처의 텍스트·소장품 기록·초록을 확인했으며, 접근 실패한 후속 문헌 1개는 의미 근거에서 제외했다. 기존 후보 16개 identity와 프로파일 3개 identity를 재사용 대상으로 연결했다. 이 숫자는 채택량이나 이미지 성공률이 아니다.

## 조사 범위와 증거

참조: [고딕 디테일 스타일 번역](chatgpt-conversation://6ac347c5-88e0-83ec-be45-3f8b28a2f7b4). 도구의 메시지별 20,000자 제한으로 긴 답변이 교차 해칭 설명 도중 잘렸다. **124개는 복원된 표 항목의 수이며 원문 전체의 총 용어 수라고 주장하지 않는다.** 초기 답변과 복원된 본문의 조합 표현도 아래에서 반영한다. 미복원된 꼬리 부분은 추정해 원문으로 채우지 않았다. [REFERENCE-CONVERSATION.json](REFERENCE-CONVERSATION.json)과 [SOURCE-KEYWORDS.json](SOURCE-KEYWORDS.json)에 원문 범위와 오프셋을 저장했다.

박물관/기관이 설명한 역사·기법의 좁은 사실, 연구자가 만든 가시 형태·관계의 제안, 현재 authored 데이터의 내용, runtime 노출/선택, 이미지 픽셀, 사용자 수용을 구분한다. 도판 원본 픽셀·영상·논문 전문까지 확인했다고 주장하지 않는다. [SOURCES.md](SOURCES.md)는 각 출처의 접근 깊이를 명시한다. [SEMANTIC-UNITS.md](SEMANTIC-UNITS.md)는 항목별 의미·형태·혼동 경계·한계를 제공한다.

## 1. 디테일을 여덟 축으로 분해한다

| 축 | 데이터에 기록할 것 | 같은 뜻으로 처리하면 생기는 오류 |
|---|---|---|
| 요소의 풍부함 | 사물/문양/재료의 종류와 반복 관계 | 반지 하나를 정밀하게 그리라는 요청에 소품이 증가 |
| 점유 범위 | 화면·벽·패널·의상·브로치 중 무엇을 채우는가 | 패널의 horror vacui가 얼굴이나 배경 전체로 번짐 |
| 연결 복잡함 | 분기·교차·고리·연속·간격 | 구조 대신 작은 잡음/점이 늘어남 |
| 크기 계층 | 큰 프레임→중간 모티프→작은 결합부 | 모든 요소가 같은 크기로 뭉개짐 |
| 깊이와 층 | 양각/음각/평면, 바탕→레이스→자수→구슬 | 레이어가 색 패턴 하나로 합쳐짐 |
| 재료 반응 | 금속선·입자·직물·망·에나멜의 경계와 표면 | 모든 재료가 같은 검은 광택으로 처리됨 |
| 형태와 문맥 | 아치/식물/로카유 등 형태, 시대/문화/서사 | goth 패션·고딕 건축·죽음·고어가 함께 활성화됨 |
| 가시성 | 대상 크기·가림·명암·필수 윤곽의 판정 가능 범위 | 큰 이미지나 선명한 피부만으로 세공 구조를 통과시킴 |

이 축은 이번 저작 설계다. 보편적인 미학 점수나 고정 임계값은 아니다. 밀도를 평가할 때는 먼저 요청된 대상 경계를 지정하고, 그 안의 상대적 점유·반복 간격·연결 형태를 본다. 모든 요청에 보석 수, 장식 층수, 활성 후보 수를 강제하지 않는다.

Maximalism은 풍부한 구성, horror vacui는 빈 공간이 적은 구성, intricate는 연결의 복잡함, micro-detailing은 작은 구조의 가독성을 맡긴다. 하나의 이미지는 여러 축을 함께 가질 수 있다. 반복 패턴 중심 작업과 복잡하게 채운 공간은 어두운 고딕 팔레트 없이도 성립한다. [Getty AAT: horror vacui](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300266827), [MOCA: Pattern and Decoration](https://www.moca.org/exhibitions/with-pleasure).

## 2. 역사적 양식과 현대 패션·혼성 표현

고딕 건축에서는 첨두 개구부, 리브와 지지체, 트레이서리 등 구조의 관계가 중요하다. 이 어휘는 장신구·용기·직물에도 옮겨졌다. 플랑부아양의 불꽃형 곡선, 고딕 리바이벌의 후대 재해석을 별도 sense로 유지한다. **검정·해골·십자가·성당 배경은 고딕이라는 단어 하나의 공통 의무가 아니다.** [Met: Gothic Art](https://www.metmuseum.org/essays/gothic-art), [Cleveland: Architectural Canopy](https://www.clevelandart.org/art/1974.4.2), [RIBA: Gothic Revival](https://www.riba.org/explore/riba-collections/architectural-styles/gothic-revival-movement/).

바로크는 볼륨과 운동, 로코코는 선택형 비대칭 C/S 곡선·로카유, 오리큘러는 둥글고 접힌 추상 로브, 아르누보는 흐르는 자연형 선과 구조/장식의 통합으로 조사했다. 지역·시대의 변형을 보존하며 `rococo=파스텔`, `Arts and Crafts=장식 최대량`, `Symbolism=세밀한 고딕` 같은 등식을 만들지 않는다. 추리게레스코·플라테레스코는 기관의 역사/건물 기록을 확보했지만, 좁은 하드 형태 프로파일은 특정 건물·부위 도판 대조 후 채택한다. [V&A: Baroque](https://www.vam.ac.uk/articles/the-baroque-style), [V&A: Rococo](https://www.vam.ac.uk/articles/the-rococo-style-an-introduction), [V&A: Art Nouveau](https://www.vam.ac.uk/articles/art-nouveau-an-international-style).

현대 고스 패션은 공포·문학·상복·무대·현대 소재가 만나는 여러 방향이다. 빅토리안/흡혈귀풍/인더스트리얼/사이버고스/스팀펑크는 고정한 의상 부품 목록으로 합치지 않는다. Gothic Lolita는 일본 패션의 범주로 다루고, 명칭에서 나이·노출·성적 장르를 추론하지 않는다. 드래그·캠프·퀴어 맥시멀리즘 역시 문화 문맥과 선택형 외형을 구분한다. [FIT: Gothic, Dark Glamour](https://www.fitnyc.edu/museum/exhibitions/gothic-dark-glamour.php), [V&A: Lolita fashion](https://www.vam.ac.uk/articles/lolita-fashion-japanese-street-style), [Met: Camp](https://www.metmuseum.org/exhibitions/listings/2019/camp-notes-on-fashion).

초기 답변의 `Neo-Baroque`, `Ornamentalism`, `Filigree-heavy`, `Decorative excess`, `Excessive ornamentation`, `Visual richness`, `Dense detailing`도 각각 **바로크 어휘의 후대 사용 / 장식 방향 / 선재 구조와 점유량 / 장식 강도 / 재료·형태의 풍부함 / 국소 밀도**로 연결한다. 새 동의어 묶음이나 단일 하드 프로파일을 추가할 이유는 없다. `Cyber-baroque`, `Mechanical filigree`, `Technorganic forms`는 이름을 유지하되 혼성 관계와 모든 변경 효과를 함께 제안한다.

## 3. 금속 세공에서 수정해야 할 구별

| 구별 | 필요한 가시 관계 | 외형만으로 확정할 수 없는 것 |
|---|---|---|
| 필리그리 / 인그레이빙 | 선재의 두께·연결 / 표면의 파인 홈 | 실제 도구·제작 이력 |
| 열린 필리그리 / 바탕판형 | 고리 사이 배경 / 연속 바탕 위 솟은 선재 | 모든 filigree에 관통 구멍이 있다는 일반화 |
| 그래뉼레이션 / 비드워크 | 금속 바탕의 입자 / 천에 속한 구슬 | 금속 조성·접합 공정 |
| 르푸세 / 체이싱 | 큰 판재 부조 / 부조에 더한 작은 윤곽 | 뒷면/앞면 가공 방향 |
| 에칭 / 선각 | 얕은 칸·표면 변화 / 좁은 파인 선 | 산 부식 또는 실제 절삭의 증명 |
| 클루아조네 / 샹르베 | 가는 경계선과 색칸 / 넓은 바탕 사이 오목한 칸 | 정면만으로 완벽한 공정 식별 |
| 니엘로 / 다마스키닝 | 밝은 금속의 어두운 채움 / 어두운 바탕의 밝은 금속 무늬 | 채움의 화학 조성·공정의 시대별 변형 |
| 컷 스틸 / 보석 / 금속 입자 | 면 있는 스터드 / 세팅 / 둥근 알갱이 | 강철·보석의 진품·가치 |
| 기요셰 / 그리블 | 정밀한 반복 선각 / 부착된 작은 부품 | 기계 사용이나 실제 작동 |

V&A는 **금속 바탕판에 부착된 필리그리**도 설명한다. 따라서 일반 `filigree`를 모두 열린 구멍 프로파일로 등록하면 오답이 된다. 에칭은 무늬 자체를 파거나 주변을 낮춰 양각처럼 보이게 할 수 있다. 샹르베와 다마스키닝도 한 외형/공정으로 축소하지 않는다. 이번 후보는 **선재·판재·입자·구획·홈·부착 경계**를 시각 대리조건으로 쓰며, 제작 진위는 별도의 출처 필드에 둔다. [V&A: Metalworking techniques](https://www.vam.ac.uk/articles/metalworking-techniques), [Met: Etruscan jewelry](https://www.metmuseum.org/art/collection/search/256976), [Met: Cloisonné sample](https://www.metmuseum.org/art/collection/search/40608), [Breguet: Guilloché](https://www.breguet.com/en/breguet-house/1775-1801/appearance-guilloche-watchmaking).

## 4. 직물·의상 장식의 바탕과 부착

브로케이드의 추가 직조 무늬, 다마스크의 직조/광택 차이, 보빈/니들 레이스의 제작 범주를 분리한다. 다마스크와 브로케이드가 한 직물에 공존하는 소장품도 있어 서로를 절대적인 배타 라벨로 만들지 않는다. tonal damask는 유용한 선택형이며 다마스크 전체의 단색 의무는 아니다. [Met: Chasuble](https://www.metmuseum.org/art/collection/search/156536), [Met: Woven textile](https://www.metmuseum.org/art/collection/search/44579).

샹티이는 가벼운 망과 꽃/스크롤의 관계, 기퓌르는 이번 연구에서 **브리지로 연결된 모티프 변형**을 우선한다. guipure 관련 명칭에는 다른 용례도 있으므로 한 구조로 전체를 정의하지 않는다. 레이스가 안감 위에 놓이면 레이스의 구멍으로 안감이 보인다. 이 관계는 피부 노출과 독립이다. `lace=투명 의상`, `Chantilly=반드시 검정·수제`로 등록하지 않는다. [Getty: Chantilly lace](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=work&subjectid=300264619), [Met: Guipure evening dress](https://www.metmuseum.org/art/collection/search/83327), [Getty: Tape lace](https://www.getty.edu/vow/AATFullDisplay?find=goat&logic=AND&note=&subjectid=300312139).

코우칭은 놓은 실→가로 고정 스티치→바탕의 관계, 스텀프워크는 바탕에서 솟은 모티프, 아플리케는 별도 천 조각의 경계, 파스망트리는 가장자리 트리밍의 범주다. 태슬/프린지, 구슬/시퀸의 묶음·연속·입자·평면을 구별한다. 코르셋에서는 몸 자체의 변화가 아니라 패널·보강선·센터 여밈·아일릿·한 끈의 경로를 기록한다. [V&A: Embroidery](https://www.vam.ac.uk/articles/embroidery-styles-an-illustrated-guide), [RSN: Techniques](https://royal-needlework.org.uk/courses/professional-embroidery-tutor-programme/techniques/), [Met: Corset underpinnings](https://www.metmuseum.org/art/collection/search/82076).

## 5. 건축과 모티프의 연결·규모

트레이서리는 개구부를 나누는 구획이고 스테인드글라스는 그 안에 들어가는 유리다. 판형은 넓은 석재 면과 구멍, 부재형은 가는 바와 연결을 본다. 트레포일/쿼트러포일은 세/네 로브가 **같은 개구부의 완전한 윤곽**에 있어야 한다. 오지 아치는 양쪽 곡률의 반전, 팬 볼트는 기점에서 퍼지는 리브, 무카르나스는 셀의 층·후퇴·전이를 본다. [Getty: Plate tracery](https://www.getty.edu/vow/AATFullDisplay?find=&logic=AND&note=clay&subjectid=300003202), [Getty: Ogee arches](https://www.getty.edu/vow/AATFullDisplay?find=church&logic=null&note=&subjectid=300001032), [King's College: Chapel](https://www.kings.cam.ac.uk/kings-college-chapel-1515), [Archnet: Masjid-i Imam](https://www.archnet.org/sites/1622?media_content_id=63198).

피니얼은 부재 끝에 붙고, 가고일은 배수 기능과 관련된다. 물길/출구가 확인되지 않은 괴물 조각은 외형 모티프로 남긴다. 아라베스크·랭소·아칸서스·스트랩워크·카르투슈·로제트·서예는 각각 줄기·띠·프레임·중앙 필드·획의 연결을 맡긴다. 장식적 그로테스크의 동물/인물/식물 혼성을 살아 있는 몸의 손상으로 판정하지 않는다. [Historic England: Gargoyle fountain](https://historicengland.org.uk/listing/the-list/list-entry/1113571), [Met: Grotesque ornament](https://www.metmuseum.org/art/collection/search/751281).

트레이서리 목 장식, 피니얼 왕관 같은 옮김은 **연구자가 제안한 형태 유추**다. 건축 owner를 장신구 owner로 바꿔 바인딩하고 실제 부착 구조를 검증한다. 이를 역사 유물의 제작법이나 배경 성당을 추가하는 권한으로 쓰지 않는다.

## 6. 죽음·관능·폭력·허구 몸과 기계

죽음의 상징, 실제 사망 사건, 성인 관능 연출, 구속 장치 모양, 실제 구속 사건, 허구 몸의 변형, 혈액/부상 흔적은 각각의 문맥·owner·관계를 가진다. 연구 데이터에는 모두 남기되 양식 단어 하나가 다른 event·노출·강도를 자동 추가하지 않게 한다.

Memento mori는 죽음을 환기하는 모티프, vanitas는 성취/향락의 물건과 덧없음의 단서가 함께 있는 정물 관계로 조사했다. 검은 옷은 현재 애도 상태의 증거가 아니며 성유물함 외형은 실제 내용물·성스러움의 증거가 아니다. Femme fatale은 서사 원형, camp/drag/queer는 문화적 문맥이며 실제 인물의 성격·지향·정체성을 픽셀 라벨로 만들지 않는다. [National Gallery: Vanitas](https://www.nationalgallery.org.uk/paintings/glossary/vanitas), [Met: Mourning attire](https://www.metmuseum.org/exhibitions/listings/2014/death-becomes-her).

Body horror는 몸의 구조/경계 변형, gore/splatter는 요청된 손상·혈액의 표현 축으로 구분한다. 에로구로와 에로·그로·넌센스는 현대 장르와 근대 일본 문화의 범위를 분리한다. 후자는 확인한 논문 초록 이상의 세부 시대 의무를 주장하지 않는다. [BFI: Cronenberg](https://www.bfi.org.uk/features/where-begin-with-david-cronenberg), [Suzuki: Cultural Critic](https://www.jstor.org/stable/25790963).

그리블은 표면의 작은 부품, 킷배싱은 부품 조합의 제작 개념, 노출 기구부는 덮개/공동/축/부품의 관계, 바이오메커니컬은 명시 허구 문맥의 유기형/기계형 연결을 조사했다. 부품의 수나 톱니 모양은 작동의 증거가 아니다. [Lucasfilm: Model-making interview](https://www.starwars.com/news/skeleton-crew-tippett-studio-interview), [BFI: Tetsuo](https://www.bfi.org.uk/features/5-reasons-tetsuo-iron-man).

## 7. 디테일을 드러내는 조명과 매체

키아로스쿠로는 명암으로 부피를 모델링하고, 테네브리즘은 어두운 환경 속 일부 중요한 영역을 선택적으로 드러낸다. 후자의 미학과 모든 미세 관계를 판정 가능한 상태로 보여주는 목표는 긴장 관계가 있을 수 있다. 이미지를 어둡게 만든 것으로 세공 의무를 충족했다고 평가하지 않는다. 교차 해칭은 선묘/판화의 명암 구성과 실제 사진의 표면 홈을 분리한다. [National Gallery: Chiaroscuro](https://www.nationalgallery.org.uk/paintings/glossary/chiaroscuro), [National Gallery: Tenebrism](https://www.nationalgallery.org.uk/paintings/glossary/tenebrism).

## 8. 현재 데이터에서 재사용할 것과 보강할 것

검사 기준은 [CHECKOUT-SNAPSHOT.json](CHECKOUT-SNAPSHOT.json)의 HEAD·등록 manifest·authored 해시다. shared checkout에 다른 작업의 변경이 있다. 원래 해시로 덮어쓰지 않는다. [EXISTING-COVERAGE.json](EXISTING-COVERAGE.json)은 긍정 라벨의 정확 일치와 제한된 문자열 단서를 기록한 **저작 인벤토리**다. registry의 `profiles`와 dictionary의 `visual_semantics`를 따로 기록했고 실제 resolver를 실행하지 않았다. 라벨 일치나 일치 없음은 의미 커버리지의 판정이 아니다.

| 현재 기록 | 재사용 판단 | 필요한 보강 |
|---|---|---|
| `sff_pro_j06` | 선재·음공간을 가진 wearable filigree 원자 | 열린/바탕판 변형 분리, 중립 object owner, 전체 material/property effects 검토 |
| `sff_relation_pro_r31` | 열린 필리그리와 프린트의 dictionary relation | 바탕판형까지 같은 구멍 의무를 물려주지 않기 |
| `sff_pro_j07` | 클루아조네 경계/색면 원자 | 구획 관계·object adapter·샹르베 구별 |
| `hw_brocade_raised_motifs_1` | 보조 직조 무늬 | 자수와 구별, 다른 owner로 확장 시 effects 바인딩 |
| `hw_damask_tonal_pattern_1` | 같은 색의 직물 광택 선택형 | 전체 다마스크 정의로 일반화하지 않기 |
| `pf_muqarnas_location`, `pf_muqarnas` | 셀·층·벽/천장 전이 | camera/조명 후보의 effects를 건축 의미와 분리 |
| `gothic_lolita_dress`, `victorian_gothic_world` | 기존 패션/세계 후보의 identity | 일반 gothic 문맥에서 하위 패션/배경을 강제로 활성화하지 않기 |
| 기존 chiaroscuro 후보들 | 명암/재료 구분 선택지 | focal required 구조가 실제로 판정 가능한지 원본 픽셀 확인 |

현재 `sff_pro_j06`는 appearance/material 차원을 선언하고 캡처된 property 목록에는 appearance의 `main_subject/accessories.jewelry`가 있다. 이것을 단독 상자의 장식에 그대로 복사하거나, material 잠금까지 호환된 것으로 간주하지 않는다. 이 사실은 **전체 효과 매핑을 다시 검토할 이유**이며 이 연구만으로 runtime 결함을 재현했다는 뜻은 아니다.

## 9. 후보팩에 반영하는 설계

[CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json)은 **RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA**다. 각 초안에는 긍정 형태, owner binding, 관계 설명, 제안 slot, 모든 effect area, 기존 stable identity, 문맥 조건, 대체 실패가 있다. `proposed_property_area`는 실제 runtime property 경로라고 주장하지 않는다. [ADOPTION-MAP.json](ADOPTION-MAP.json)과 [CANDIDATE-DETAILS.md](CANDIDATE-DETAILS.md)를 통해 현재 dimension/target/property로 변환·검증한 뒤 채택한다.

중립 물체·wearable·건축·직물의 의미는 재사용하되 target과 guard를 재사용하지 못하는 경우가 있다. 먼저 기존 owner에 적합한 원자가 있는지 확인한다. 필요성이 증명된 경우에만 중립적인 `ornament_structure` owner를 추가한다. style 전용 키워드 라우터나 두 번째 의미 저장소는 계획하지 않는다.

현재 v6의 확인된 순서는 **독립 core 동결 → core slot retrieval → visual profile resolution → obligations/concepts/clarification → 요청별 immutable pack**이다. 이후 composer가 전체 효과와 잠금을 검토한다. broad style은 advisory 선택지를 제공하고, 구체적인 요청 정의와 문맥에 맞는 selected form만 required가 될 수 있다. BM25F/embedding 유사도는 의미의 권한이 아니다. [현재 retrieval contract](../../../../skills/photo-prompt-image-generator/references/retrieval-contract.md).

71개 초안은 데이터 설계의 후보 목록이다. 한 요청에서 모두 노출하거나 채택할 수량이 아니다. 현재 ordinary slot 후보의 cap과 슬롯별 제약 안에서 관련 eligible 원자를 선택하며, 선택한 묶음은 멤버의 **모든 효과**가 합쳐진 상태로 잠금 검증을 통과해야 한다. 작은 재료 효과만 열렸다고 옷의 모양·색·camera까지 바꾸지 않는다.

## 10. 반영 순서와 검증

구체 실행은 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 있다. **P0 현재 데이터/owner 고정 → P1 재료와 연결 원자 → P2 모티프·건축·밀도 관계 → P3 문맥과 조합 → P4 인덱스/회귀 → P5 native 파일럿** 순서를 권한다.

92개 의미 probe는 자연어 최소 대조 72개, owner/property/medium 잠금 12개, 정의·부정·문맥 control 8개다. R14/R20/R24/R28/R29/R34의 문장은 긍정 별칭/embedding 텍스트로 넣지 않아 holdout으로 남긴다. 미일치 프로파일·잘못된 owner·명시 배제·복합 효과·한/영 우회 표현을 검사한다. [REGRESSION-PLAN.json](REGRESSION-PLAN.json).

원본 픽셀 계획은 22개다. 첫 파일럿은 열린/바탕판 필리그리, 레이스, 코우칭, 코르셋, 트레이서리, 무카르나스, 국소 밀도의 8개 요청 × 데이터 전/후 2개 arm × 독립 반복 3회 = **48개 이미지**다. 같은 frozen core와 생성 조건을 유지하고 데이터/인덱스 증분만 비교한다. source/runtime ID를 요청 문장에 넣어 검색을 유도하지 않는다. [PIXEL-QUALIFICATION-PLAN.md](PIXEL-QUALIFICATION-PLAN.md).

보고는 authored 무결성, eligible 노출, 선택/정당한 optional 거절, prompt/runtime 바인딩, native all-of, 사용자 수용을 분리한다. required 관계가 작거나 가려지면 `UNOBSERVABLE_NOT_PASS`; 일부만 맞으면 실패다. 생성 차단은 `BLOCKED_UNSCORED`다. **target 데이터가 실제 노출·선택·바인딩되지 않았다면 결과가 좋아 보여도 데이터 개선의 인과 증거로 보고하지 않는다.**

이번 실행의 실제 상태와 패키지 구조 검증은 [VALIDATION.json](VALIDATION.json), 수량은 [PACKAGE-COUNTS.json](PACKAGE-COUNTS.json), 저장 파일 무결성은 [MANIFEST.json](MANIFEST.json)에 남긴다. 활성 assets·index·generator 채택, semantic/runtime regression, 이미지 생성·픽셀 평가·사용자 수용은 아직 실행하지 않았다.
