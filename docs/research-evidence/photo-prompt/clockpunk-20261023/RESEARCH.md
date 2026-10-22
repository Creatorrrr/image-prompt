# Clockpunk 시각 의미·후보 데이터 상세 조사

2026-10-23, Asia/Seoul. 범위: [참조 대화](https://chatgpt.com/c/6ada2cba-cb44-83ee-9f24-61beb17fe339)의 16개 분야·17개 표·213개 항목과 현재 작업 트리의 후보 원본. **이번 결과는 연구·초안·반영 계획이다. 운영 데이터 변경이나 검색·이미지 성능 검증을 완료했다는 뜻이 아니다.**

## 1. 결론과 설계 방향

보강의 중심은 **동력이 어디에 저장되고, 무엇을 거쳐 전달되며, 어떤 부품이 운동을 조절하고, 누가 감고 수리하는지**다. 황동·톱니·고글을 더하는 방식보다 이 연결을 보이는 구조·접촉·공간·생활 관계로 저술하는 편이 Clockpunk의 의미를 더 정확히 전달한다. 이는 조사 결과에서 도출한 데이터 설계 판단이다.

다만 모든 장면에 동력 계통 전체를 강제하면 작은 부품이 보이지 않거나 소유자가 뒤섞인다. 태엽통 구조, 캠 접촉, 필기 손과 종이, 정비 접근, 도시 시보를 **독립적으로 선택 가능한 완전한 실현**으로 나누고, 요청이 전체 기계 계통을 요구할 때만 연결된 묶음을 구성한다. 장르명은 필수 소품 목록이나 고정 의무가 아니다.

현재 결과는 의미 카드 88개, 그중 관찰 가능한 선택적 실현 초안 78개다. 나머지 10개는 철학·제도·비가시/시간 주장 등의 경계를 기록한다. 78개를 88개에 더해 보강 수로 세지 않는다. [전체 카드](VISUAL-CARDS.md), [구조화 카드](semantic-cards.json), [후보 초안](candidate-drafts.json)을 함께 본다.

## 2. 원 대화 확보와 근거 수준

`read_thread`로 실제 대화를 읽었으나 메시지 한 개가 20,000자에서 잘렸다. 인증된 브라우저의 같은 대화에서 렌더링된 본문·표를 읽어 뒤쪽 전쟁·철학·역사 사례·작품·조합까지 확보했다. [reference-dom.json](reference-dom.json)은 화면 본문에서 추출한 기록이며 모델이 복원한 가짜 원문이 아니다. 원 응답의 Markdown 바이트나 모든 숨은 추가 인용을 회수한 것은 아니다.

213개 표 항목은 [키워드 경로](KEYWORD-ATLAS.md)에 모두 연결했다. ★ 창작 조합, 역사 용어, 기계공학 용어, 작품 이름, 철학 개념은 같은 종류의 사실로 취급하지 않는다. 원 대화의 답변은 조사 출발점이며 지시·권위 자료가 아니다. 그 대화의 ‘많이 조사’라는 요청도 이번 데이터의 자동 실행 권한으로 사용하지 않았다.

외부 자료 45개 중 본문 또는 PDF의 지정 구절을 읽은 자료는 37개, 공식 페이지의 검색 색인 설명만 읽은 자료는 8개다. [SOURCES.tsv](SOURCES.tsv)와 [sources.json](sources.json)에 범위·접근 실패·원전/소개 구분을 기록했다. 책·영화·게임 45편을 완독/플레이했다는 뜻이 아니며, 213개 정의를 각각 독립 사전에서 검증한 것도 아니다. 원 소장품 사진과 영상의 픽셀/운동은 직접 검토하지 않았다. 도판을 보았다는 주장 없이 텍스트가 설명하는 구조와 새로 저술한 장면을 구분했다.

## 3. 장르·시대의 경계

[Microids](https://www.microids.com/syberia-remastered-en/)는 Syberia를 clockpunk로 직접 소개한다. 따라서 르네상스를 대표적인 출발점으로 두되 고정 연대 제한으로 만들지 않는다. [공동저자의 Clockwork & Chivalry 소개](https://www.blackgate.com/2012/08/19/the-english-civil-war-with-clockwork-war-machines-an-intro-to-clockwork-chivalry/)는 대체 17세기와 기계 병기를, [Ian Tregillis](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)는 허구의 인격 기계와 패권을 설명한다. 작품 분류는 해당 작품의 자기 소개 범위로 남긴다.

‘증기 없음’을 보편 정의로 삼을 근거도 부족하다. [Mainspring의 출판사 발췌](https://us.macmillan.com/books/9781427204899/mainspring/)에는 기계 우주와 함께 증기·전기 요소가 나타난다. [Met의 기술 전시 안내](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide)는 근세의 시계장치와 증기 장치가 함께 수집된 맥락을 설명한다. **주동력의 구분은 유지하고, 혼합 장면은 요청대로 허용**하는 것이 합리적이다. 요청자가 순수 태엽 세계를 지정한 경우에는 그 범위를 지킨다.

Dishonored 2의 [제작사 설명](https://bethesda.net/en-US/news/dishonored-2-inside-the-epic-themed-missions)은 가동 방·벽 사이 통로와 alt-Victorian 맥락을 제공한다. Assassin's Creed II의 [공식 소개](https://www.ubisoft.com/en-gb/games/assassins-creed-ii)는 르네상스 활극의 인접 사례다. 두 작품 전체를 같은 장르로 단정하거나 고유 모델을 범용 후보의 정본 디자인으로 옮기지 않는다.

## 4. 동력·전달·조절을 분리하는 핵심 사전

| 계층 | 포함할 개념 | 한 프레임에서 평가할 것 | 별도 검증할 것 |
|---|---|---|---|
| 동력 저장/입력 | 동력 태엽·태엽통·추·인력·수력 | 태엽의 통 내부 관계, 줄의 추/드럼 종단, 감는 손과 축 | 저장 에너지·지속 시간·실제 출력 |
| 전달 | 기어열·피니언·축·링크 | 맞물림·축 지지·관절 연결·출력 소유자 | 기어비·간섭·토크·손실 |
| 방출/조절 | 탈진기·버지·폴리엇·진자·밸런스 | 바퀴/팔레트 접촉, 조절자의 연결과 형식 | 주기·시각 정확도·계속 진동 |
| 힘 보정/잠금 | 퓨지·래칫·걸쇠 | 원뿔 홈/체인/태엽통 연결, 걸쇠 접촉 | 힘 보정 곡선·잠금 성능·역구동 |
| 출력 | 필기·타종·연주·계산 표시 | 펜촉/종이, 망치/종, 건반/음원, 별도 표시창 | 글 전체의 작성 인과·음향·정답 |

[Museo Galileo](https://catalogue.museogalileo.it/object/ModelPendulumClock.html)는 추/태엽·전달계·탈진기·조절자를 나누어 설명한다. [Met의 시계 연구](https://www.metmuseum.org/essays/seventeenth-century-european-watches)는 퓨지와 실태엽의 역할, 1675년 이후의 변화를 구체적으로 설명한다. 이 구분을 A01–A12의 구조·혼동 경계로 옮겼다. 동력 태엽과 실태엽을 번역상 유사어로 병합하지 않는다.

플라이휠·조속 날개·원심구 조속기도 하나의 ‘돌아가는 바퀴’ 후보로 묶지 않는다. 이번 조사에서 A09/A10은 구조 초안까지 만들었고, 형식별 공학 원전·도판 검토가 추가로 필요하다. 그럴듯한 부품 이름을 붙인 것만으로 기능 사실을 승인하지 않는다.

## 5. 운동·기계 기억의 관찰 범위

[Science Museum의 마이야르데 설명](https://blog.sciencemuseum.org.uk/introducing-the-draughtsman-writer-automaton/)은 캠에 정해진 시·그림의 운동 정보가 들어 있음을 보여 준다. 여기서 유효한 확장은 **캠 윤곽→팔로어→링크→필기 손**이다. 인형이 뜻을 이해하거나 새 문장을 자유롭게 만들어 낸다는 능력까지 역사 사실로 확장하지 않는다.

| 구조 | 핵심 구별 | 후보/검증 방향 |
|---|---|---|
| 캠/캠 스택/핀 실린더 | 윤곽 접촉·여러 출력·핀 배치가 다름 | B01–B03; 팔로어 접촉과 출력 종단을 분리 |
| 링크/크랭크 슬라이더/랙 피니언 | 관절 사슬·회전/왕복·회전/직선 | B04–B06; 막대가 허공에서 끊기지 않게 연결 |
| 웜/베벨 | 엇갈림축과 교차축·나사형과 원뿔형 | B07–B08; 자기잠김이나 회전비를 사진으로 단정하지 않음 |
| 유성/차동 | 기어의 배치와 다축 회전 관계는 별도 | B09/B11; 어느 부재가 입력·고정·출력인지 별도 선언 |
| 제네바 | 핀의 슬롯 진입과 정지 구간 | B10; 슬롯 정지 사진과 한 주기 검증을 나눔 |
| 기계식 계산·기억 | 숫자 표시와 실제 연산·이해는 별도 | B12/C07; 정답과 지능을 display에서 추정하지 않음 |

[Vinci의 랙 피니언 모형](https://museoleonardiano.it/en/opera/rack-and-pinion/)과 [RWTH 제공 제네바 설명](https://www.dmg-lib.org/dmglib/handler?mcdsc=208025)을 직접 대조했다. [제조사 기술 PDF](https://www.qtcgears.com/tools/catalogs/PDF_Q420/Tech.pdf)의 지정 단락으로 웜 자기잠김의 조건성·유성 부재·백래시를 추가 확인했다. 현대 기술 문헌은 구조 구분의 근거이며 특정 근세 기계의 제작·성능 증거는 아니다.

## 6. 천문·항해: 현재 가장 명확한 번역 보정 대상

| 기구 | 구별할 형상/기능 | 잘못 합쳐지는 이웃 |
|---|---|---|
| 아스트롤라베 | 평면 몸체·위도판·rete·alidade | 회전 구형 고리·태엽 포켓워치 |
| 환구의/혼천의형 기구 | 천구 좌표 고리·중심 구체·극축 | 태양 둘레 행성 팔 |
| 오러리 | 중심 태양과 서로 다른 행성 팔·기계적 운동 모형 | 환구의·우주를 실제 구동하는 장치 |
| 천문시계/아스트라리움 | 시각 외에 천체·달력 정보 | 장식 원판·보통 시계의 색다른 다이얼 |
| 항해 시계 | 항해 중 기준 시간 유지 | 지도 옆 일반 시계·위도 관측기 |

[평면 아스트롤라베](https://catalogue.museogalileo.it/object/PlaneAstrolabe.html), [1564년 환구의](https://catalogue.museogalileo.it/object/ArmillarySphere_n02.html), [RMG의 오러리 기록](https://www.rmg.co.uk/collections/objects/rmgc-object-11220)을 별도 항목으로 다뤘다. 첫 둘은 직접 본문, 오러리는 공식 컬렉션의 색인 본문을 읽었다. 박물관의 용어·유물 연대·결손 기록을 유지한다.

현재 `cand_473bd368aa555c93bc88221265b0b027`은 영문 orrery를 ‘방 크기의 혼천의’로 축약한다. `cand_fad77205dfbf5f55bbbc88dbc6257442`는 ‘회전 황동 고리’가 있는 허구 포켓워치인데 한국어와 embedding의 천체/시간 마법 범위가 다르다. 역사 기구·작가가 요청한 혼성 기구를 구분해 보정해야 하며 기존 허구 조합 자체를 오류로 삭제해서는 안 된다. [전체 원문/조건/효과 snapshot](existing-source-mapping.json)에 기록했다.

## 7. 공방·재료·복식·공간

공방의 차별점은 완성된 기어 더미가 아니라 **제작 중인 부품, 서로 다른 교체품, 손이 닿는 작업점, 공구 받침, 정비 통로**다. [Making Marvels](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)의 인출대·음악 시계·다직종 협업을 바탕으로 E01–E06을 설계했다. 금속 피로·공차·윤활 성공은 마모 무늬만으로 증명하지 않는다.

‘황동’·‘금도금’·‘청동 녹청’·‘청색 강철’은 재료/마감/색상 층이 다르다. 기요셰는 표면의 규칙적 절삭 문양, 필리그리는 가는 금속선 구조라는 차이를 보존한다. 반복 문양을 보고 실제 가공법까지 확정하지 않는다.

[V&A의 바로크 공연 설명](https://www.vam.ac.uk/articles/performance-and-the-baroque)은 무대 전환 기계·조명·복식·권력의 연결을 제공한다. F02/F06은 열린 패널·레일·뒤 통로·줄 종단을 드러내는 선택적 실현이다. ‘가동 건축’이라는 말만으로 방 변환 전후를 정지 사진에서 통과시키지 않는다.

러프·더블릿·슬래싱·스테이즈·쇼핀은 별도 소유 부품과 특정 시대·지역의 맥락을 갖는다. [FIT 개설](https://fashionhistory.fitnyc.edu/1580-1589/)과 [쇼핀이 드러나는 1588년경 판화](https://www.metmuseum.org/art/collection/search/356244)를 대조했다. 스테이즈를 보강하기 위해 [1846년 Southwark 소장품](https://heritage.southwark.gov.uk/objects/11787/stays)도 확인했지만, 이를 르네상스 패턴 증거로 전용하지 않는다. 복식·성적 취향·계급·직업은 별도 주장이다.

## 8. 지역별 기계 전통: 범용 ‘동양풍’ 묶음을 피한다

| 전통 | 이번 조사에서 확인한 것 | 후보 설계 시 보존할 구분 |
|---|---|---|
| 안티키테라 | 수동 천문 계산·남은 파편·현대 재구성 가설 | 유물/복원, 수동/태엽, 계산/지능 |
| 알자자리 | 1315년 필사본에 담긴 수력 공작 시계 도해 | 발명/필사본/모형 연대, 그림/실물 |
| 수운의상대 | 북송 수력 탑의 상부 관측·중부 천구·하부 시보 | 중국 탑 전체와 다른 지역 장치 |
| 자격루 | 1434년 원형 소실, 1536년 항아리 잔존, 국가 시보 | 남은 항아리/전체 복원, 수력/태엽 |
| 가라쿠리 | 에도 목제 차 운반 인형·태엽·캠의 복원 모형 설명 | 서비스 동작/현대 로봇/다른 문화 자동인형 |
| 기도 수도사·터크 | 종교 행위 모사와 감춰진 인간 체스 조작의 서로 다른 역사 | 기계의 종교 도상/신앙, 외형상 자동/실제 조작자 |

근거는 [UCL](https://www.ucl.ac.uk/news/2021/mar/experts-recreate-mechanical-cosmos-worlds-first-computer), [Met의 알자자리 folio](https://www.metmuseum.org/art/collection/search/451302), [Hong Kong Space Museum](https://hk.space.museum/en/web/spm/resources/curators-blog/2020/12/su-song-and-the-water-driven-astronomical-clock-tower.html), [국립고궁박물관](https://www.gogung.go.kr/gogung/pgm/psgudMng/view.do?menuNo=800065&psgudSn=370348), [국립과학박물관](https://www.kahaku.go.jp/exhibitions/vm/past_parmanent/rikou/computer/karakuripuppet.html), [Computer History Museum](https://www.computerhistory.org/chess/stl-431e1a07e7e40/)이다.

이 자료들도 서로 다른 층을 읽어야 한다. Met 알자자리 페이지는 소개 문장의 활동 세기와 생몰 정보가 충돌하므로 이 패키지는 그 문장의 세기를 채택하지 않는다. 국립고궁박물관 항아리 항목만으로 구슬 장치·시보 인형 전체를 검증했다고 말하지 않는다. M03/M04는 완성된 문화별 정본이 아니라 후속 분할 저술의 출발점이다.

## 9. 신체·성인 소재·폭력의 의미 범위를 유지한다

### 신체와 표현물

철제 의수, 외골격, 밀랍 해부 모형, 유기/기계 혼성체, 분리 가능한 자동인형은 **생물 몸·인공 보철·외부 장치·표현된 해부**가 서로 다르다. [Science Museum 의수 기록](https://collection.sciencemuseumgroup.org.uk/objects/co126769/artificial-hand-and-forearm-1601-1700)은 일부 유사품이 후대 복제품일 가능성을 경고한다(이번 열람은 색인 본문). [La Specola](https://www.sma.unifi.it/index.php?func=viewpage&module=CMpro&newlang=eng&pageid=631)는 1771년 공방과 분리되는 밀랍 층을 설명한다. 장애와 실제 보철을 자동으로 공포·악역·비인간성으로 처리하지 않는다.

### 성인 미학과 사회

에로틱 오토마타/시계, 플랩 판화, 자동인형 연인, 피그말리온, 인형화, 기계 페티시, 본디지, 관음, 동의/프로그램 충돌, 유곽, 정조대 모두 경로와 카드를 유지했다. [British Museum OA.10757](https://www.britishmuseum.org/collection/object/H_OA-10757)의 숨겨진 에로틱 장치는 공식 검색 색인으로 존재를 확인했지만 직접 본문은 403이었다. [Met의 플랩 판화](https://www.metmuseum.org/art/collection/search/356244)는 직접 본문을 읽었고 도상과 현실 관람자의 개입을 구분했다. [M.574](https://www.britishmuseum.org/collection/object/H_M-574)의 위조 분류 역시 색인 근거이며 모든 물건의 역사에 일반화하지 않는다.

유물에 표현된 성인, 그림 속 인물, 현실 관람자, 허구 자동인형, 실제 성인은 서로 다른 소유자다. 성적 의미·합의/강압·직업·소유 관계를 금속·가죽·미소·노출 정도에서 추정하지 않는다. 성인/페티시 맥락 역할은 실제 요청과 현행 적용 조건을 충족할 때만 검토하며, 이번 연구는 기본 강도나 eligibility 로직을 바꾸지 않는다.

### 전쟁·고문·처형·저항

레이피어/망고슈, 휠록/플린트록, 다총열 화기, 공성 기계, 기계 병사/암살자, 함정, 고문, 처형, 사보타주를 누락하지 않았다. [Peter Peck의 휠록](https://www.metmuseum.org/art/collection/search/22387)에서는 시계공/총포 제작자의 연결과 점화 구조를, [방어 단검 항목](https://www.metmuseum.org/art/collection/search/32166)에서는 지역·시기별 병용 차이를 확인했다. 기계 고문·자동 처형의 구체 역사 유물은 이번 범위에서 별도 확인하지 않았으므로 허구 제도/맥락으로 보존한다. 폭력적 소재를 삭제하는 것과 역사적 장치로 거짓 승인하지 않는 것은 구분해야 한다.

## 10. 비가시 주장과 다중 프레임

동의·인격·영혼·자유의지·법적 소유·식민 수탈·동작 반복·시간 고장·기억 삭제·감염 인과·신의 부재는 한 프레임의 장식이나 자세로 확정할 수 없다. 연구 카드의 `context_only`는 이 의미를 삭제하는 태그가 아니라 **무엇으로 입증해야 하는지 지정하는 경계**다.

관찰 가능한 대리 장면에는 작동계와 연결된 열쇠, 부품 접근 차이, 교체품, 같은 척도의 다른 표시창, 분리된 부품의 틈 등이 있다. 이 장면도 제도나 과거 사건의 단서일 뿐 사실 확정은 아니다. 반복·교체 전후·계산 오류 개선을 요청했다면 시퀀스·원전·실험 로그가 필요하다. 단일 이미지의 PASS 항목에서 보이지 않는 주장을 제거하고, 요청 맥락에는 그대로 남긴다.

## 11. 기존 데이터의 구체적 처리 제안

[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)에 현재 manifest 20,054개 source 중 지정 어휘 일치 20개를 기록했다. 이 숫자는 전체 데이터의 Clockpunk 의미 커버리지나 검색 recall이 아니다. 주요 수정/재사용 검토는 다음과 같다.

| 대상 | 제안 |
|---|---|
| `cand_473bd368aa555c93bc88221265b0b027` | orrery/혼천의 번역과 head-height 행성의 소유/규모 효과 검토 |
| `cand_fad77205dfbf5f55bbbc88dbc6257442` | 역사 아스트롤라베와 허구 포켓워치 분리; EN/KO/embedding 전체 범위 일치 |
| `cand_cb1f8a7534d15030b51f6652cf24295e` | `without steam` 보편 정의 보정; 장르 guard와 동력/전달/조절 구분 |
| `cand_cca5b1e30e485a199e31c82711a5acb9` | 열린 무브먼트의 정적 구조와 반복 출력 주장 분리 |
| `cand_682fdf57d4745bbe841ab5862eb798f4` | 검사 프레임과 박동·하강·계산 오차 측정을 분리 |
| `cand_a71c7b7cf4785d238f2e729feeeb4798` | 수리 비교/인계의 가시 관계와 검증 완료 이력을 분리 |
| `cand_c6b9cc7879b35ac096badbd0355b25c2` | 솔·계산대 접촉의 기존 완전 실현 재사용부터 검토 |
| 기존 러프·흉갑·재료·인형 외장 | 조건·묶음 전체를 보존하는 범위에서 재사용; 표면만으로 자동기계/신분을 부여하지 않음 |

6개 핵심 보정은 현재 dirty source를 이 작업에서 덮어써도 된다는 승인 목록이 아니다. 구현 시 최신 원본 diff와 다른 작업 소유 범위를 다시 대조한다. 빈 effects나 태그가 있다고 native 자격이 이미 성립한 것으로 간주하지 않는다.

## 12. 충분성 기준과 남은 조사

이번 패키지의 ‘충분’은 어휘 수만 의미하지 않는다. 213개 입력 경로, 88개 소유자/관계 카드, 78개 한영 실현, 혼동 경계, 구절별 출처 범위, 기존 CID 처리 판단, 회귀/픽셀 계획이 함께 있다. 각 단계의 미검증도 명시한다.

다음 7개 카드는 세부 공학/복식 원전 검토를 남겼다: A09 플라이휠, A10 조속 날개, B03 핀 실린더, B05 크랭크 슬라이더, B11 차동기어, E02 절삭 방식, G02 시대별 스테이즈 패턴. 기타 일반 장면은 가족 수준의 출처를 바탕으로 저술한 제안이며 정본 고증 검증을 받았다는 뜻이 아니다. `additional_engineering_review_required=false`도 역사 진품/기능/도판 검증 PASS를 뜻하지 않는다.

특히 M03은 수운의상대 탑과 자격루 항아리, M04는 차 운반 인형과 숨은 인간 조작 경계를 함께 다룬 연구 카드다. 운영 등록 때는 서로 다른 실물 전통을 하나의 동의어 묶음으로 만들지 않도록 분할한다. H04·L02·J05·K04도 제도·철학·폭력별로 문맥 레코드를 분할해야 한다.

## 13. 다음 실행을 위한 산출물

[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)은 구체 경로·단계·종료 조건을, [SCENE-BLUEPRINTS.md](SCENE-BLUEPRINTS.md)는 원 대화의 7개 조합을, [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv)는 120개 한영 사례/240개 질의를, [PIXEL-PLAN.md](PIXEL-PLAN.md)은 첫 12군×3 arm 비교를 정의한다. 평가 사례는 이번 저자가 만든 개발/경계 사례이며 독립 holdout이 아니다.

구조 검증·원본 보존은 [VALIDATION.json](VALIDATION.json)과 [SHA256SUMS](SHA256SUMS)에 기록한다. source 등록·native 자격·검색/embedding·runtime 게시·이미지 생성/픽셀·사용자 수용·커밋/푸시는 이 연구 단계에서 실행하지 않았다.
