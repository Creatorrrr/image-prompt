"""Authored research inputs. Not operating semantic or candidate authority."""
DATE = '2026-10-22'
REFERENCE_ID = '6ada011f-1294-83ee-969f-be549a1046c2'
# table,row counts checked against the rendered reference conversation, not the 20k preview.
REFERENCE_COUNTS = [21,18,25,22,23,24,26,12,15,31,26,7,5,7,6,12,5,12]
TAIL_TABLES = {
9: '''Dubcon / Dubious Consent — 불분명한 동의
Noncon / Non-consent — 비동의
Sexual Coercion — 성적 강요
Slavery / Enslavement — 노예제·노예화
Slave / Binding Contract — 노예계약·구속계약
Mind Control / Hypnosis — 정신지배·최면
Succubus / Incubus — 서큐버스·인큐버스
Monster Romance — 비인간 존재와의 로맨스
Dual / Sexual Cultivation — 쌍수·성적 수련
성적 에너지·행위를 성장 자원으로 삼는 설정
Pregnancy / Fertility Mechanics — 임신·생식력 규칙
Breeding / Reproductive Control — 번식·생식 통제
NTR / Netorare — 네토라레
Taboo Relationship — 금기 관계
Tentacle Motif — 촉수 소재
Armor Break — 방어구 파괴''',
10: '''UI — User Interface
GUI — Graphical User Interface
HUD — Head-Up Display
Status Window / Stat Screen
Character Sheet — 캐릭터 시트
Health / Resource Bar — 체력·자원 막대
Nameplate — 이름표
Floating Combat Text — 전투 수치 텍스트
Tooltip / Inspect Panel — 툴팁·조사창
Toast / Notification — 짧은 알림
Quest Tracker — 퀘스트 추적 영역
Modal / Dialog — 모달·대화창
Combat / System Log — 전투·시스템 로그
Inventory Grid — 인벤토리 격자
Paper Doll / Equipment Slots
Hotbar / Action Bar — 단축바
Radial Menu — 원형 메뉴
Cooldown Sweep — 쿨다운 음영
Lock-on Reticle / Target Bracket
Minimap / Radar — 미니맵·레이더
Fog of War — 전장의 안개
Rarity Color Coding — 등급별 색상 구분
Redaction / Hidden Information — 정보 가림
Glitch / Corrupted UI — 손상된 UI
Progressive Disclosure — 단계적 정보 공개
Alert Hierarchy — 경고의 중요도 구분''',
11: '''Screen-space UI — 화면 좌표 UI
World-space UI — 세계 좌표 UI
Head-locked / View-locked UI
Floating Panel — 공중 패널
Holographic Interface — 홀로그램형 인터페이스
AR Overlay — 증강현실 오버레이
FUI — Fictional / Fantasy User Interface''',
12: '''Diegetic UI — 작중에 존재하는 UI
Non-diegetic UI — 관객·플레이어에게 제시되는 UI
Spatial / Geometric 표시
Meta-perceptual 표현 — 감각을 번역한 효과
작중 기기의 화면을 확대해 제시''',
13: '''《The Wandering Inn》 — 웹소설
《나 혼자만 레벨업》 — TV 애니메이션
《소드 아트 온라인》 — 아인크라드 편 애니메이션
《전지적 독자 시점》 — 웹툰
《아픈 건 싫으니까 방어력에 올인하려고 합니다》 — 애니메이션
《던전에서 만남을 추구하면 안 되는 걸까》 — 소설·애니메이션
《코노스바》 계열 — 모험자 카드''',
14: '''《쥬만지: 새로운 세계》 — 영화
《프리 가이》 — 영화
《레디 플레이어 원》 — 영화
《스콧 필그림》 — 영화
《아이언맨》 — 영화
《데드 스페이스》 — 게임''',
15: '''청색 반투명 패널
밝은 소프트웨어 메뉴
레트로 RPG 창
아케이드형 보상 연출
군사·SF HUD
종이·카드·장부
피부·문신·신성문자
장비 내장 표시
의식·감각형 표시
손상된 시스템창
유기적·생체적 인터페이스
관전·후원 피드''',
16: '소설\n웹툰·만화\n애니메이션\n실사 영화\n게임',
17: '''누가 볼 수 있는가?
다른 사람의 상태도 읽을 수 있는가?
표시가 무엇을 측정하는가?
표시는 항상 정확한가?
어떻게 호출하고 조작하는가?
창을 닫거나 거부할 수 있는가?
창의 빛이 얼굴을 비추는가?
다른 물체에 가려지는가?
카메라에 찍히거나 공유되는가?
능력치가 내려가면 몸과 마음도 바뀌는가?
호감도·충성도는 감정인가, 강제 효과인가?
부활한 사람은 이전과 같은 사람인가?'''
}

# id|title|url|access|claim boundary. All paraphrases; no copied passages.
SOURCE_ROWS = '''S01|Level Up Publishing: What is LitRPG|https://www.levelup.pub/what-is-litrpg|body|출판사의 장르 설명. RPG 규칙 중심이라는 범위만 지원하며 공통 UI 외형을 규정하지 않는다.
S02|Andrew Rowe: Progression Fantasy|https://andrewkrowe.wordpress.com/2019/02/26/progression-fantasy-a-new-subgenre-concept/|body|작가가 성장 판타지와 LitRPG의 중첩 및 차이를 설명한다. 숫자나 상태창은 성장 판타지 전체의 필수 요소가 아니다.
S03|Andrew Rowe: Core Loops|https://andrewkrowe.wordpress.com/2022/11/03/progression-fantasy-core-loops/|body|전투 보상, 반복 숙련, 퀘스트, 실패 후 재도전 등 반복 구조의 구분. 한 장의 이미지로 반복 이력을 입증하지 않는다.
S04|FFXIV: Navigating the Game Screen|https://eu.finalfantasyxiv.com/game_manual/view/|body|파티 목록, 상태 효과, 타깃, 시전 진행, 자원, 전투 수치, 퀘스트 등 기능 구분. FFXIV의 규칙과 색을 장르 공통으로 강제하지 않는다.
S05|Path of Exile: Game|https://www.pathofexile.com/game|body|스킬 젬과 보조 젬, 패시브 연결, 아이템 옵션, 파티 인스턴스와 거래 구조. 다른 작품의 슬롯 개수나 물약 소모 규칙으로 일반화하지 않는다.
S06|Cantina Creative: Free Guy|https://www.cantinacreative.com/film/free-guy|body_and_one_still|제작사가 HUD, 아이템 선택, 레벨업, 미니맵 작업을 공개한다. grenade 스틸을 브라우저에서 실제 관찰했다. 다른 GIF의 시간 변화는 검증하지 않았다.
S07|Territory Studio: Ready Player One|https://territorystudio.com/project/ready-player-one/|body|GSS와 IOI의 그래픽 언어, 개인별 HUD, 모니터·바이저·공간 표지의 차이. 각 시스템의 규칙이나 현실 VR 기술 수준은 별도다.
S08|Beyond the HUD: Fagerholt and Lorentzon|https://publications.lib.chalmers.se/records/fulltext/111921.pdf|pdf_text_limited|표지·초록의 UI 설계 공간 연구를 확인했다. 후속 본문 위치 조회는 timeout이었다. 두 독립 축의 구체 설명은 이를 논의하는 S09 본문과 교차 확인했으며 원 논문 전체 정밀 검토로 표시하지 않는다.
S09|Peacocke et al: HUD and Diegetic Ammo Displays|https://www.yorku.ca/mack/ieee_gem2015.html|body|연구 본문이 공간·작중 통합을 구별하고 Dead Space의 등 체력계와 공중 인벤토리를 설명한다. 제한된 탄약 과제 실험을 전체 몰입 우열로 확대하지 않는다.
S10|Unity uGUI 2.0: Canvas|https://docs.unity3d.com/Packages/com.unity.ugui@2.0/manual/UICanvas.html|body|Overlay, Camera, World Space 렌더 모드와 원근·가림 차이. 문서의 diegetic 용어를 서사적 인지 여부와 완전 동치로 취급하지 않는다.
S11|The Wandering Inn 1.00|https://wanderinginn.com/2017/03/03/rw1-00/|body|작가 공식 본문의 대괄호 직업·레벨·스킬 알림. 문자 분리 자체는 공중 패널의 형태를 확정하지 않는다.
S12|Blizzard: Classic Hardcore Rules|https://news.blizzard.com/en-gb/article/23973734/rules-of-engagement-classic-hardcore-is-coming-to-world-of-warcraft|body|해당 Hardcore 서버에서의 영구 사망과 다른 서버 이동의 구분. 영구라는 말의 적용 범위를 명시해야 한다.
S13|Royal Road: Content Guidelines|https://www.royalroad.com/support/knowledgebase/114|body|성적 내용, 충격적 내용, 노골적 폭력 등의 분리된 경고 체계. 플랫폼 분류이며 개인의 동의나 장르 공식 사전은 아니다.
S14|Mountaindale Press: Divine Dungeon|https://www.mountaindalepress.store/pages/series/divine-dungeon|body|던전 자체가 성장 주체인 출판사 소개. 보석 코어의 보편적 색·방 개수·공간 제어 효과는 주장하지 않는다.
S15|BOFURI official story|https://bofuri.jp/story/|body|방어 집중 투자, 여러 스킬과 길드 활동이라는 공식 소개. 상태창의 상세 픽셀 구성은 이번에 확인하지 않았다.
S16|KonoSuba Explosion episode 10|https://konosuba.com/bakuen/story/?mode=story10|body|길드의 모험자 카드 조회를 공식 줄거리가 명시한다. 카드의 정확한 색·행·인장은 미확인이다.
S17|DanMachi official prototype chapter 4|https://danmachi.com/10_projects/prototype_04.php|body|공식 게시 텍스트의 등 문자와 스테이터스 갱신. 프로토타입 텍스트의 증거이며 모든 애니 장면의 재료·발광·움직임을 확정하지 않는다.
S18|Mega Crit: Slay the Spire press kit|https://www.megacrit.com/press-kits/slay-the-spire/|body|덱 구성과 로그라이크 결합의 개발사 설명. LitRPG 자체나 카드 UI의 단일 표준을 뜻하지 않는다.
S19|Dead Space producer Chuck Beaver guest article|https://arstechnica.com/gaming/2008/05/guest-writer-dead-space-producer-chuck-beaver-on-story-ui/|body|개발자의 실시간 월드 내부 인벤토리·지도 설계 설명. 전체 UI의 사용성 우월성은 입증하지 않는다.
S20|D&D 2024 Basic Rules: Playing the Game|https://www.dndbeyond.com/sources/dnd/br-2024/playing-the-game|body|능력치와 판정·플레이 구조의 특정 규칙 사례. DEX와 AGI를 공통 동의어로 만들거나 HP를 실제 혈액량으로 취급하지 않는다.
S21|Iron Man HUD: creator oral history|https://vfxblog.com/ironman/|body|제작자 인터뷰의 얼굴 연기, 그래픽 깊이와 시선 대응. 헬멧 HUD 사례이며 LitRPG 분류 근거는 아니다.
S22|Scott Pilgrim: creator interview|https://www.artofthetitle.com/title/scott-pilgrim-vs-the-world/|body|감독·디자이너의 오프닝 그래픽 제작 인터뷰. 점수·모든 장면의 diegesis는 이 자료로 확정하지 않는다.
S23|Solo Leveling episode 4 recap|https://www.crunchyroll.com/news/features/2024/1/31/solo-leveling-episode-4-recap|location_redirect|이번 요청은 지역 제한 화면으로 이동했다. 참조 대화의 청색 패널 기술은 재검증되지 않았고 작품 고유 픽셀 주장의 근거로 사용하지 않는다.
S24|Sword Art Online Aincrad official|https://www.swordart-online.net/aincrad/|http_403|공식 URL의 이번 접근은 403이었다. 메뉴 제스처·색·배치 주장은 독립 확인 대기다.
S25|DanMachi legacy glossary|https://danmachi.com/danmachi/special/index.html|body_partial_and_search_excerpt|일반 본문은 접근했으나 용어집 본문은 도구에 온전히 노출되지 않았다. 검색 발췌를 픽셀 증거로 쓰지 않고 S17의 공식 본문으로 범위를 좁혔다.
S26|WEBTOON Omniscient Reader episode 1|https://www.webtoons.com/en/action/omniscient-reader/episode-1/viewer?episode_no=2&title_no=2154|body_and_image_references_only|공식 회차 페이지와 이미지 참조를 확인했다. 이번 작업에서 실제 이미지들을 열어 보지 않았으므로 검은 상자·붉은 글자에 대한 기존 대화의 주장은 재검증 대기다.
S27|Jumanji production notes republication|https://www.visualhollywood.com/jumanji-welcome-to-the-jungle-2017-production-notes|reprinted_production_notes|제작 노트 재게시의 제작자 발언이 아바타·여러 목숨·능력 및 약점 설정을 설명한다. 원 배급사 문서의 보존본 여부와 UI 픽셀·팔 표시는 미확인이다.'''

# id|family|title|evidence mode|sources|owner definitions|directed relations|English authored realization|Korean authored realization|confusion / limits
# Relation syntax is symbolic for research review; it is NOT an existing runtime schema.
CARD_ROWS = '''U01|표시 매체|공간 패널과 손의 앞뒤|still|S08 S10|panel=tilted free-standing panel;hand=one hand;room=visible room|hand>occludes>panel;panel>in_front_of>room|A tilted status panel stands between a hand and the room, with the hand cleanly occluding one panel edge.|기울어진 상태 패널이 손과 방 사이에 있고 손이 패널 모서리 일부를 가린다.|평평한 화면 자막과 구분;누가 볼 수 있는지는 가림만으로 확정 불가
U02|표시 매체|화면 가장자리 HUD|displayed|S04 S06 S10|frame=image frame;hud=corner resource display;scene=street|hud>aligned_to>frame;hud>overlays>scene|A compact resource display aligns with the image corner while the street remains visible behind it.|작은 자원 표시가 이미지 모서리에 맞고 뒤로 거리가 보인다.|원근 패널과 구분;카메라 추종은 연속 장면 필요
U03|표시 매체|손에 든 모험자 카드|still|S16|card=one rigid record card;hand=holder hand;clerk=clerk hand|hand>supports>card;clerk>points_at>card|One hand supports a rigid adventurer record card while a clerk points to its separate class and skill rows.|한 손이 단단한 모험자 기록 카드를 받치고 접수원의 손이 직업·스킬 행을 가리킨다.|일반 신분증과 비교;카드 재질·행 구성은 창작 선택
U04|표시 매체|신체에 기록된 능력|still|S17|skin=back skin;marks=organized glyph rows|marks>conform_to>skin|Ordered dark glyph rows follow the curvature of a person's back rather than floating in front of the skin.|정돈된 어두운 문자 행이 피부 앞에 뜨지 않고 등 굴곡을 따른다.|장식 문신과 비교;기록 내용·성장 효력은 별도 문맥
U05|표시 매체|장비에 내장된 자원계|still|S09 S19|rig=back-mounted equipment;meter=segmented meter|meter>embedded_in>rig|A segmented resource meter is physically embedded in a back-mounted equipment housing with visible edges and fasteners.|분절된 자원계가 테두리와 고정부가 보이는 등 장비 하우징에 내장돼 있다.|피부 문양·공중 막대와 구분;정확한 HP 여부는 라벨 필요
U06|표시 매체|안면과 바이저 정보층|still|S07 S21|face=face inside visor;ui=curved near-face graphics;visor=visor rim|ui>beside>face;face>inside>visor|Curved information layers flank a face inside a visor, leaving the eyes and mouth readable.|바이저 안 얼굴 양쪽에 굽은 정보층을 놓고 눈과 입을 읽을 수 있게 한다.|유리에 인쇄된 글씨와 비교;시선 추적·심리 상태는 단일 프레임 불가
U07|표시 매체|본문과 분리된 시스템 행|displayed|S11|page=text page;notice=bracketed isolated line;prose=ordinary paragraph|notice>separated_from>prose;notice>printed_on>page|A bracketed system notice occupies its own line between ordinary prose paragraphs on a visible page.|보이는 페이지에서 대괄호 시스템 알림이 일반 서술 문단 사이 독립 행을 차지한다.|공중 홀로그램을 추가하지 않음;소설 표기와 작중 시각을 구분
U08|표시 매체|두 정보 영역의 대비|displayed|S07|left=personal display;right=institutional display;divider=clear separation|left>distinct_from>right;divider>between>left|A personal display with rounded icons sits beside a separate institutional display with rigid aligned data columns.|둥근 아이콘의 개인 화면 옆에 각진 데이터 열의 기관 화면을 별도로 놓는다.|브랜드 구도는 창작;UI만으로 선악·기업 정체 확정 불가
I01|정보 구조|상태 요약과 능력치 표|displayed|S04 S20|sheet=status sheet;header=identity header;stats=attribute rows;resources=resource block|header>inside>sheet;stats>inside>sheet;resources>inside>sheet;header>above>stats;resources>separate_from>stats|A status sheet separates an identity header, labeled attribute rows, and a resource block with current and maximum values.|상태 시트에서 식별 머리글·능력치 행·현재값과 최대값의 자원 구획을 나눈다.|일반 대시보드와 비교;숫자는 표시값이지 실제 능력 검증 아님
I02|정보 구조|서로 다른 자원 막대|displayed|S04|hp=HP bar;mp=MP bar;st=stamina bar;labels=distinct resource labels|labels>identify>hp;mp>parallel_to>hp;st>parallel_to>mp|Three separately labeled HP, MP, and stamina bars show different fill lengths and current/maximum numbers.|HP·MP·스태미나 막대를 별도 라벨로 식별하고 채움 길이와 현재·최대 수를 다르게 한다.|색만으로 자원을 추정하지 않음;HP와 상처·피의 양은 비동치
I03|정보 구조|레벨과 경험치 분리|displayed|S04 S11|level=level badge;xp=experience progress bar;threshold=next threshold|xp>below>level;threshold>labels>xp|A level badge sits above an experience bar whose threshold is separately labeled.|레벨 표식 아래에 다음 기준값이 별도로 적힌 경험치 막대를 둔다.|가득 찬 막대가 실제 레벨업 순간을 증명하지 않음
I04|정보 구조|남은 포인트와 배분 선택|displayed|S15 S20|pool=unspent point total;rows=attribute rows;controls=increment controls|controls>beside>rows;pool>above>rows|An unspent-point total sits above attribute rows with aligned increment controls on each row.|미사용 포인트 총량을 능력치 행 위에 두고 각 행 옆에 증가 선택을 정렬한다.|능력치 증가의 실제 신체 효과와 분리;SP 약어는 풀어 적기
I05|정보 구조|요구 조건이 있는 해금 그래프|displayed|S05|root=entry node;branch=connected branch;locked=locked endpoint;edge=prerequisite connector|edge>connects>root;edge>ends_at>branch;locked>beyond>branch|An entry node connects to a selected branch and a locked endpoint with a visible requirement label.|시작 노드가 선택된 분기와 연결되고 그 끝 잠금 노드에 요구 조건 라벨이 있다.|장식 별자리와 구분;선행 연결과 단순 근접을 혼동하지 않음
I06|정보 구조|직업 분기와 다중 직업|displayed|S04 S05|base=base class node;choices=two class alternatives;connector=branch connector|connector>starts_at>base;connector>reaches>choices|One base class node branches into two distinct class choices without merging their identity labels.|하나의 기본 직업 노드가 식별 라벨을 합치지 않은 두 직업 선택으로 갈라진다.|승급·전직·멀티클래스는 동일 문법 아님;활성 상태를 별도 명시
I07|정보 구조|종족 진화 선택과 현재 신체|displayed|S14 S15|body=current creature silhouette;choices=two morphology branches;marker=current-state marker|marker>labels>body;choices>branch_from>body|A current creature silhouette is marked separately from two possible morphology branches.|현재 생물 실루엣에 현재 표식을 두고 두 형태 분기를 따로 표시한다.|분기 표시가 실제 변신 완료를 뜻하지 않음;몸 개수 증가 방지
I08|정보 구조|비교 가능한 기록 값|displayed|S03 S11|old=earlier labeled record;new=later labeled record;id=shared identity marker|id>matches>old;id>matches>new;old>beside>new|Two dated status records share one identity marker but show separately labeled earlier and later values.|날짜가 다른 두 상태 기록이 같은 식별자를 공유하되 이전·이후 값을 각각 적는다.|숫자 차이는 기록의 주장;실제 성장·회귀·동일 인물 입증은 별도
Q01|퀘스트·경제|퀘스트 목표와 물증 대응|still|S03 S04|board=quest board;token=objective-marked token;parcel=matching parcel|token>attached_to>board;parcel>matches_symbol_of>token|A quest token on a board and a sealed parcel on the counter carry the same distinct objective symbol.|게시판 퀘스트 토큰과 계산대의 봉인 물품이 같은 목표 표식을 가진다.|심부름 표식과 비교;수락·완료·보상 지급의 인과는 별도
Q02|퀘스트·경제|추적기와 장면 속 목표|displayed|S04|tracker=objective tracker;target=visible target;symbol=shared marker|symbol>labels>target;tracker>references>symbol|An objective tracker repeats the marker attached to one visible target in the scene.|목표 추적기가 장면 속 한 대상에 붙은 표식을 반복한다.|장식 아이콘과 구분;화살표만으로 정확한 도착지 판단 금지
Q03|퀘스트·경제|실패 조건과 경고 위계|displayed|S04 S06|dialog=warning dialog;condition=separate failure condition;choices=choice controls|condition>inside>dialog;choices>below>condition|A warning dialog separates the objective, failure condition, and two choice controls with distinct emphasis.|경고창에서 목표·실패 조건·두 선택을 강조 차이를 두고 나눈다.|붉은색이 즉시 죽음이라는 공통 규칙은 아님;거부 가능성은 실제 규칙 필요
Q04|퀘스트·경제|물건의 크기를 보존한 격자|displayed|S04 S05|grid=inventory grid;item=long item icon;cells=occupied adjacent cells|item>spans>cells;cells>inside>grid|One long item spans several adjacent inventory cells, leaving the empty cells visibly separate.|긴 아이템 하나가 인벤토리의 이웃한 여러 칸을 차지하고 빈칸은 구분된다.|격자는 소지품 표현;물체의 실제 차원 수납은 미증명
Q05|퀘스트·경제|장비 슬롯과 신체 부위|displayed|S04|figure=body diagram;head=head slot;hand=hand slot;lines=slot connectors|lines>connect_to>head;lines>connect_to>hand;head>above>figure|A body diagram links distinct head and hand equipment slots to their corresponding regions.|인체 도식의 머리·손 장비 슬롯을 각각 대응 부위와 연결한다.|슬롯 아이콘과 실제 착용 구분;화면 표시는 물리 접촉이 아님
Q06|퀘스트·경제|감정창과 조사 대상 연결|still|S04 S05|item=single inspected object;panel=inspection panel;line=leader line|line>starts_at>panel;line>ends_at>item|An inspection panel connects by one leader line to a single isolated item on the table.|감정창의 안내선 하나가 탁자의 고립된 물건 하나에 닿는다.|다른 물건으로 연결하면 실패;창의 내용은 진실성 보증 아님
Q07|퀘스트·경제|등급·옵션·내구도 분리|displayed|S05|card=item card;rarity=rarity label;mods=modifier block;wear=durability field|rarity>separate_from>mods;wear>below>mods;mods>inside>card|An item card separates a rarity label, modifier list, and durability field rather than collapsing them into one score.|아이템 카드의 희귀도·옵션 목록·내구도 칸을 하나의 점수로 합치지 않고 구분한다.|보라색이 항상 고등급은 아님;희귀도·성능·상태는 다른 축
Q08|퀘스트·경제|보석 소켓과 장착 경계|still|S05|weapon=weapon body;socket=recessed socket;gem=inserted gem;rim=socket rim|socket>part_of>weapon;gem>inside>socket;rim>occludes_edge_of>gem|A gem sits within a recessed socket in a weapon, and the socket rim overlaps the gem edge.|무기 몸체의 오목한 소켓 안에 보석이 놓이고 테두리가 보석 가장자리를 덮는다.|장식 보석과 구분;마법 효력·귀속 규칙은 외형만으로 불가
Q09|퀘스트·경제|제작 재료·작업·결과의 자리|still|S03 S04|recipe=recipe diagram;materials=separated materials;tool=tool at workpiece;workpiece=unfinished object|recipe>corresponds_to>materials;tool>contacts>workpiece|Separated recipe materials match a recipe diagram while a tool touches an unfinished workpiece.|분리된 재료가 제작법 도식과 대응하고 도구는 미완성 작업물에 닿는다.|제작 성공·품질 상승은 미증명;보통 공방과 시스템 정보 구별
Q10|퀘스트·경제|경매의 서로 다른 거래 위치|displayed|S05|listing=item listing;price=asking price;bid=separate bid;item=item identifier|listing>references>item;price>inside>listing;bid>distinct_from>price|An item listing shows one item identifier, an asking price, and a distinct current bid field.|매물 하나에 아이템 식별자·희망 가격·현재 입찰가를 별도 칸으로 놓는다.|시스템 상점·플레이어 경매는 비동치;거래 완료를 추정하지 않음
Q11|퀘스트·경제|덱·손패·버림패 구분|displayed|S18|deck=face-down draw stack;hand=face-up hand fan;discard=separate discard stack|hand>between>deck;discard>separate_from>deck|A face-up hand fan sits between a face-down draw stack and a separately labeled discard stack.|앞면 손패가 뒤집힌 드로 더미와 별도 라벨의 버림 더미 사이에 놓인다.|카드 한 장으로 덱빌딩 입증 불가;뽑기·수집·덱 구성 구별
Q12|퀘스트·경제|추첨 보상과 확률 표시|displayed|S13 S18|pool=reward pool;weights=probability labels;result=separate revealed result|weights>label>pool;result>separate_from>pool|A reward pool with labeled probabilities is displayed apart from one revealed result.|확률 라벨을 붙인 보상 집합과 공개 결과 하나를 별도 영역에 표시한다.|RNG·가챠·일반 드롭은 동의어 아님;표시 확률의 실제 정확성 미증명
C01|전투·협업|보호자와 피보호자의 위치|still|S04|tank=shield-bearing protector;ally=protected ally;enemy=opponent;shield=shield|tank>between>enemy;ally>behind>tank;shield>faces>enemy|A shield-bearing protector stands between an opponent and a separate ally, with the shield facing the opponent.|방패 든 보호자가 적과 별도 아군 사이에 서서 방패를 적 쪽으로 향한다.|갑옷 외형만으로 탱커 확정 금지;어그로 수치는 별도
C02|전투·협업|지원 효과의 발신자와 수신자|still|S04|healer=support caster;ally=separate recipient;effect=continuous support arc|effect>starts_at>healer;effect>ends_at>ally|One support arc visibly starts at a caster's hand and ends at a separate ally's equipment.|지원 궤적 하나가 시전자의 손에서 시작해 별도 아군 장비에 닿는다.|빛만으로 치유·강화 수치 단정 불가;공격 궤적과 문맥 구별
C03|전투·협업|시전 진행과 대기 음영|displayed|S04|cast=cast progress bar;icon=skill icon;mask=radial cooldown mask|mask>covers_part_of>icon;cast>separate_from>icon|A cast progress bar is separate from a skill icon covered by a partial radial cooldown mask.|시전 진행 막대와 일부가 부채꼴 대기 음영으로 덮인 스킬 아이콘을 분리한다.|시전·쿨다운·지속시간은 세 타이머;정지 화면은 감소 속도 미증명
C04|전투·협업|효과 아이콘의 소유 대상|displayed|S04|target=selected creature;bar=target bar;effects=status icons;leader=target connector|effects>adjacent_to>bar;leader>connects>bar;leader>ends_at>target|Status icons sit beside the selected creature's target bar with a clear connector to that creature.|상태 아이콘이 선택 생물의 타깃 막대 옆에 있고 연결선은 해당 생물에 닿는다.|버프·디버프 소유자 혼동 방지;독·정신지배 원인은 아이콘만으로 미확정
C05|전투·협업|범위 경계와 안팎 위치|still|S04|zone=bounded ground marker;inside=one figure inside;outside=one figure outside;floor=continuous floor|zone>lies_on>floor;inside>inside>zone;outside>outside>zone|A bounded marker lies on continuous ground with one figure inside and another clearly outside its edge.|연속 바닥의 경계 표식 안에 한 인물, 경계 밖에 다른 인물을 분명히 둔다.|마법진 자체가 광역 피해 아님;친구·적·피해 규칙은 문맥
C06|전투·협업|공격 수치와 타격 대상|displayed|S04 S06|number=combat number;target=one struck target;impact=visible impact point|number>near>impact;impact>on>target|One combat number sits near a visible impact point on a single target, apart from other nameplates.|전투 숫자 하나를 단일 대상의 타격 지점 가까이에 두고 다른 이름표와 분리한다.|피해·치명·회복은 라벨과 규칙 필요;큰 글씨가 치명타 보증 아님
C07|전투·협업|분리된 소환·동료 개체|still|S04|caster=one caster;companion=separate creature;connection=control indicator;floor=floor|connection>starts_at>caster;connection>ends_at>companion;companion>supported_by>floor|A separate creature stands on the ground beside a caster with one distinct linking indicator between them.|별도 생물이 시전자 옆 바닥에 서고 두 존재 사이에 독립된 연결 표식을 둔다.|분신·야생동물·소환·조련은 비동치;자율성과 소유권 미확정
C08|전투·협업|파티 목록과 인물 대응|displayed|S04|party=list of members;figures=distinct party figures;marks=matching role markers|marks>identify>figures;party>repeats>marks|Distinct role markers above separate figures repeat in a compact party list with individual resource rows.|서로 다른 인물 위 역할 표식이 개별 자원 행을 가진 파티 목록에 반복된다.|사람 수와 목록 수 일치 확인;단순 군중이 레이드 아님
W01|세계·성장 주체|게이트 경계와 목적 공간|still|S14|gate=freestanding aperture;near=near ground;far=different space;rim=continuous rim|rim>bounds>gate;gate>between>near;far>visible_through>gate|A continuous aperture rim separates near ground from a different visible space beyond it.|연속된 입구 테두리가 가까운 바닥과 그 너머 다른 공간을 가른다.|문·마법진·던전은 동일하지 않음;인스턴스 복제 여부 미증명
W02|세계·성장 주체|층별 경로와 도달 지점|still|S18|tower=stacked levels;route=connecting route;landing=marked landing|route>connects_levels_of>tower;landing>on>route|A visible route connects stacked levels and reaches a distinctly marked landing.|보이는 경로가 층들을 연결하며 뚜렷한 표식의 층 도착점에 닿는다.|수직 건물만으로 탑등반 장르 아님;층별 시험은 문맥
W03|세계·성장 주체|코어와 관리 공간의 대응|still|S14|core=central core object;rooms=separate room models;links=room-control connectors|links>start_at>core;links>end_at>rooms|A central core object connects to separate room models through distinct visible lines.|중앙 코어 물체에서 독립된 연결선들이 별도 방 모형들에 닿는다.|보석 보물과 구분;코어의 의식·던전 전체 지배는 미확정
W04|세계·성장 주체|안전 경계와 접근 조건|displayed|S04 S12|boundary=marked boundary;outside=hazard area;sign=access condition;entry=entry point|sign>beside>entry;boundary>separates>outside|A marked boundary separates an entry point from a hazard area, with an explicit access-condition sign at the entry.|표시 경계가 진입점과 위험 구역을 나누고 입구 옆에 접근 조건 표지가 있다.|밝은 원=절대 안전 아님;레벨 제한·면역의 작동은 미검증
W05|세계·성장 주체|거점의 생산 흐름|still|S03 S14|store=resource store;workshop=workshop;settlement=settlement plan;routes=marked production routes|routes>connect>store;routes>end_at>workshop;workshop>part_of>settlement|Marked production routes connect a resource store to a workshop within a settlement plan.|거점 도면 안 자원 저장소와 작업장을 생산 경로로 연결한다.|일반 건축 모형과 비교;인구 성장·왕국 통치·자동 생산은 문맥
W06|세계·성장 주체|생활 기술과 시스템 기록|still|S03 S11|cook=working cook;tool=working utensil;food=prepared food;record=skill record|tool>contacts>food;record>beside>cook|A working utensil contacts prepared food while a separate skill record stands beside the cook's workspace.|작업 도구가 음식에 닿고 요리 작업대 옆에 별도 숙련 기록을 둔다.|생활물과 cozy 정서는 비동치;도구 배치가 실제 숙련 상승은 아님
D01|죽음·이력|재출현 지점과 남은 장비|still|S12 S03|marker=restart marker;gear=abandoned gear;route=route between locations|route>starts_at>marker;route>ends_at>gear|A restart marker and abandoned equipment occupy separate locations linked by a visible route.|재시작 표식과 남겨진 장비를 서로 다른 위치에 놓고 보이는 경로로 잇는다.|시체 회수·리스폰·부활·회귀는 비동치;과거 죽음은 정지 사진 미증명
D02|죽음·이력|손실 항목의 명시|displayed|S12|record=death-loss record;xp=experience loss field;gear=equipment loss field;scope=rule scope|xp>inside>record;gear>separate_from>xp;scope>labels>record|A death-loss record separates experience and equipment loss fields and names the scope of the rule.|사망 손실 기록에서 경험치·장비 손실 칸을 나누고 규칙 적용 범위를 적는다.|붉은 창만으로 영구 사망·전체 약탈 추정 금지
D03|죽음·이력|같은 식별자의 반복 기록|displayed|S03|rows=separate attempt rows;id=shared identifier;outcomes=distinct outcomes|id>repeats_in>rows;outcomes>label>rows|Separate attempt rows repeat one identifier while displaying distinct outcomes and timestamps.|서로 다른 시도 행마다 한 식별자를 반복하고 결과·시각을 다르게 적는다.|시도 기록과 실제 시간 반복 구분;동일 인격 연속성은 별도
H01|폭력·신체|손상된 장비와 신체 경계|still|S12 S13|armor=damaged armor plate;body=wearer's body;gap=broken plate gap|gap>inside>armor;armor>worn_by>body|A broken armor plate has a visible fracture gap while the wearer's body remains a separate surface behind it.|파손 갑옷 판의 틈과 그 뒤 착용자의 신체 표면을 구분한다.|방어구 손상·신체 손상·성적 노출은 독립;자동 탈의 금지
H02|폭력·신체|변형 부위와 정상 부위 경계|still|S13 S17|limb=one limb;changed=changed surface region;ordinary=ordinary region;seam=continuous transition|changed>part_of>limb;ordinary>part_of>limb;seam>between>changed|One continuous limb carries a sharply bounded changed surface next to an ordinary surface region.|연속된 사지 하나의 변형 표면과 정상 표면 사이에 경계를 둔다.|바디 호러·단순 유혈 구별;강제성·원인·통증은 미확정
H03|폭력·신체|부착체와 숙주의 경계|still|S13|host=host surface;organism=attached organism;attachment=contact seam|organism>distinct_from>host;attachment>connects>organism;attachment>touches>host|An attached organism has its own outline and a visible contact seam on the host surface.|부착 생물은 독립 윤곽을 가지며 숙주 표면의 접합 경계가 보인다.|장식·기생·공생의 인과 차이;촉수 존재가 성적 내용은 아님
H04|폭력·신체|오염 표시와 변화 대상|displayed|S13|meter=corruption meter;body=affected figure;connector=ownership connector|connector>starts_at>meter;connector>ends_at>body|A labeled corruption meter connects to one specific figure rather than the whole scene.|오염 라벨의 게이지가 장면 전체가 아닌 특정 인물 하나와 연결된다.|오염=도덕적 악·정신질환 아님;색·게이지만으로 진단 금지
R01|관계·권한|관계도와 복수 인물|displayed|S13|center=central person node;others=separate person nodes;edges=labeled relationship edges|edges>start_at>center;edges>end_at>others|Labeled relationship edges connect a central person node to several separate person nodes.|관계 라벨을 붙인 선이 중심 인물 노드와 여러 개별 인물 노드를 잇는다.|하렘·역하렘·합의된 다자관계·단순 파티 비동치;동의는 외형 미증명
R02|관계·권한|호감도 표시와 감정의 구별|displayed|S13|panel=relationship panel;person=referenced person;value=displayed affinity value;id=identifier|id>links>panel;id>identifies>person;value>inside>panel|A relationship panel names one referenced person and shows a clearly labeled affinity value.|관계 패널이 특정 인물을 식별하고 호감도라는 라벨의 값을 표시한다.|수치가 실제 감정·복종·동의임을 뜻하지 않음;미소는 검증 대체 불가
R03|관계·권한|명령 권한과 구속 계약|displayed|S13|contract=contract record;issuer=issuer field;recipient=recipient field;restriction=restriction clause|issuer>inside>contract;recipient>distinct_from>issuer;restriction>below>recipient|A contract record separates issuer and recipient fields from a specific restriction clause.|계약 기록에서 발행자·대상자 칸과 구체적인 제한 조항을 구분한다.|구속 계약·노예제·합의된 권력교환은 동의어 아님;목걸이로 판정 금지
R04|관계·권한|관전·후원 정보와 대상|displayed|S06 S07|feed=observer feed;recipient=recipient identifier;messages=stacked messages;reward=separate donation badge|messages>inside>feed;reward>beside>recipient|An observer feed contains stacked messages and a separate donation badge beside one recipient identifier.|관전 피드의 누적 메시지와 별도 후원 표식을 특정 수신자 식별자 옆에 둔다.|별·채팅창만으로 성좌 후원 확정 불가;실시간 갱신은 시간 증거
R05|관계·권한|혈통 도식과 생식 기록|displayed|S13|chart=family chart;nodes=separate family nodes;links=descent links;record=separate fictional fertility field|links>connect>nodes;record>separate_from>chart|A family chart connects separate generation nodes while a fictional fertility field is kept in a separate record.|세대별 노드의 혈통 도식과 허구의 생식력 수치 기록을 분리한다.|임신·성행위·강제 생식은 도식·복부 외형으로 입증 불가
E01|UI 구성|이름표와 정확한 대상|displayed|S04|plate=nameplate;target=single character;line=short ownership line|line>starts_at>plate;line>ends_at>target|A short line joins one nameplate to exactly one character without crossing another person's head.|짧은 연결선이 이름표 하나와 인물 하나를 잇고 다른 머리를 가로지르지 않는다.|이름표와 일반 자막 구분;정체성·플레이어/NPC 여부는 문맥
E02|UI 구성|원형 선택과 한 선택지|displayed|S04 S06|ring=radial choice ring;segments=separate wedges;selected=one highlighted wedge|segments>part_of>ring;selected>one_of>segments|A radial choice ring contains separated wedges with exactly one visibly selected wedge.|원형 선택기에 구분된 부채꼴들을 두고 그중 하나만 선택 상태로 표시한다.|조준기·마법진과 구분;입력 방식·선택 완료는 미증명
E03|UI 구성|하위 정보의 펼침|displayed|S04|row=selected item row;detail=expanded detail panel;anchor=shared row marker|anchor>labels>row;anchor>repeats_in>detail;detail>beside>row|A selected row and an expanded detail panel share one marker with clear separation from other rows.|선택 행과 펼친 상세창이 같은 표식을 공유하며 다른 행과 분리된다.|정보 확장의 현재 배치만;열리는 애니메이션은 시간 필요
E04|UI 구성|탐색 지도와 미탐색 경계|displayed|S04 S18|map=map field;known=known region;hidden=masked region;edge=mask boundary|known>inside>map;hidden>inside>map;edge>between>known|A map separates an outlined known region from a masked unknown region with a clean boundary.|지도에서 윤곽이 있는 탐색 영역과 가려진 미탐색 영역의 경계를 구분한다.|구름·검열·안개 날씨와 구분;일반 지도만으로 실제 탐색 이력 불가
E05|UI 구성|잠금·알 수 없음·손상 분리|displayed|S04 S10|locked=locked field;unknown=unknown field;broken=misaligned field;panel=containing panel|locked>inside>panel;unknown>distinct_from>locked;broken>distinct_from>unknown|One panel distinguishes a locked field, an unknown-value field, and a visibly misaligned damaged field.|한 패널에서 잠금 칸·값 미확인 칸·정렬 손상 칸을 서로 다르게 표시한다.|검열·미해금·오류·불신뢰 시스템을 하나로 합치지 않음
E06|UI 구성|정돈된 로그와 단발 알림|displayed|S04 S11|log=timestamped log rows;toast=one isolated notice;gap=visible separation|toast>separate_from>log;gap>between>toast|Timestamped log rows occupy one area while a single isolated acquisition notice sits apart from them.|시각이 붙은 로그 행 영역과 단일 획득 알림을 떨어뜨려 놓는다.|알림의 잠깐 출현·중복 재발은 단일 프레임으로 불가
X01|비시각 문맥|장르 분류는 규칙·서사 문맥|context|S01 S02|context=story rule description|context>requires>context|Genre classification needs the role of game rules in the story; a blue panel alone is insufficient.|장르 분류에는 게임 규칙의 서사적 역할이 필요하며 푸른 패널만으로 충분하지 않다.|LitRPG·GameLit·성장물·이세계·VR·헌터물·코지의 비동치
X02|비시각 문맥|사적 시각과 작중 존재|context|S08 S09|context=fictional perception rule|context>requires>context|Specify who can perceive the interface separately from where it appears in the frame.|인터페이스를 누가 인지하는지와 화면 어디에 놓이는지를 별도로 명시한다.|다른 사람이 반응하지 않는 한 장면은 안 보인다는 증거 아님
X03|비시각 문맥|머리·시야·세계 고정|sequence|S10|context=multi-view observation|context>requires>context|Compare multiple views before claiming an interface follows the head or stays fixed in the world.|머리를 따르거나 세계에 고정됐다는 판정은 여러 시점 비교가 필요하다.|한 프레임의 원근·모서리 위치만으로 추종 규칙 확정 금지
X04|비시각 문맥|스탯의 계산 의미|context|S20|context=local stat definitions|context>requires>context|Resolve local definitions for DEX, AGI, SP, HP, and derived values before choosing visual labels.|DEX·AGI·SP·HP·파생 수치의 작품별 뜻을 확인한 뒤 라벨을 선택한다.|CHA=미모·INT=IQ·HP=혈액량으로 치환 금지
X05|비시각 문맥|전투 효율·확률·빌드|context|S04 S05|context=combat rules and repeated outcomes|context>requires>context|Damage rate, critical chance, min-maxing, synergy, and a glass-cannon build need rules or comparative outcomes.|DPS·치명 확률·최적화·시너지·유리대포 빌드는 규칙이나 비교 결과가 필요하다.|큰 무기·빛·가녀린 체형은 전투 성능 증거가 아님
X06|비시각 문맥|반복 성장과 시간 변화|sequence|S03|context=ordered event evidence|context>requires>context|Grinding, farming, rotations, damage-over-time, and repeated quests require ordered events or explicitly displayed records.|그라인딩·파밍·로테이션·지속 피해·반복 퀘스트에는 순서 있는 사건 또는 표시 기록이 필요하다.|기록의 주장을 실제 시간 증거와 구분
X07|비시각 문맥|죽음 이후의 동일성과 복귀|sequence|S12 S03|context=death and return rule evidence|context>requires>context|Distinguish respawn, resurrection, regression, reincarnation, and time loops using the rule and ordered events.|리스폰·부활·회귀·환생·시간 루프는 규칙과 사건 순서로 구분한다.|같은 얼굴 두 명·문·묘비는 동치 증거가 아님
X08|비시각 문맥|권한·자각·신뢰|context|S07 S08|context=agency and information rules|context>requires>context|Administrator authority, NPC self-awareness, and deceptive system information require narrative context.|관리자 권한·NPC 자각·거짓 시스템 정보는 서사 문맥이 필요하다.|왕관·로봇 얼굴·글리치·관객 응시만으로 판정 금지
X09|비시각 문맥|동의와 강요|context|S13|context=explicit relationship and consent context|context>requires>context|Keep consent, coercion, ambiguous consent, and non-consent as contextual claims, independent of attractiveness or accessories.|동의·강요·불분명한 동의·비동의는 매력이나 장신구와 독립된 문맥 주장으로 둔다.|미소·침묵·수치·목걸이·노출로 동의 추론 금지
X10|비시각 문맥|관계 구성과 표현 수위|context|S13|context=relationship and depiction descriptors|context>requires>context|Separate relationship topology from sexual explicitness, fetish emphasis, and a fade-to-black narrative transition.|관계 구성·성적 상세함·페티시 강조·장면 생략 전환을 분리한다.|BL·GL·하렘·다자연애·비인간 로맨스 자체는 노골적 성행위 아님
X11|비시각 문맥|기억·정체성·원작 지식|context|S02 S03|context=identity and memory history|context>requires>context|Foreknowledge, metagaming, body swaps, and erased memory require a specified knowledge or identity history.|사전 지식·메타게이밍·몸 교환·기억 소실에는 지식·정체성 이력이 필요하다.|거울·동일 얼굴·화면 오류가 기억이나 성 정체성을 증명하지 않음
X12|비시각 문맥|통증·정신 안정·영혼|context|S13|context=fictional sensation and ontology|context>requires>context|Pain feedback, sanity points, soul damage, and soul destruction are fictional context claims rather than medical diagnoses.|통증 피드백·정신 안정 수치·영혼 손상·소멸은 허구 문맥이며 의학적 진단이 아니다.|표정·게이지·기하학 효과만으로 통증·정신건강·영혼 존재 판단 금지
X13|비시각 문맥|상해 강도·원인·반복 가해|context|S13|context=violence depiction and causation|context>requires>context|Separate visible injury, graphic detail, torture intent, and repeated harm through resurrection.|보이는 상해·묘사 상세함·고문 의도·부활 반복 가해를 구분한다.|피가 많음=고문·스플래터·바디 호러·잔혹한 정치 모두 아님
X14|비시각 문맥|출산·생식·혈통·금기|context|S13|context=family and reproductive rules|context>requires>context|Fertility, reproductive control, betrayal, and taboo relationships need explicit fictional context.|생식력·생식 통제·배신·금기 관계에는 명시적인 허구 문맥이 필요하다.|배의 형태·나이 추정·혈통 도식으로 임신·성적 행위·강요 판정 금지
X15|비시각 문맥|공개 정보와 감시·후원|context|S06 S07|context=information distribution rules|context>requires>context|Resolve the recipients and permissions of party information, spectatorship, sponsorship, reputation, and karma.|파티 정보·관전·후원·평판·업보의 수신자와 권한을 명시한다.|채팅창·군중·별무늬만으로 성좌·감시·도덕 판단 증명 금지
X16|비시각 문맥|오류·허점·쉬운 공략|context|S05 S08|context=expected rules and observed deviation|context>requires>context|Distinguish a glitch, exploit, cheat ability, and easy tactic by their relation to the intended rules.|오류·허점 이용·치트 능력·쉬운 전술을 의도된 규칙과의 관계로 구분한다.|깨진 글자나 승리 장면만으로 해킹·버그·부정행위 확정 금지
X17|비시각 문맥|표시의 진실성|context|S08 S13|context=display provenance and truth evidence|context>requires>context|A displayed stat, contract, probability, or relationship score proves what is shown, not that the system reports truth.|스탯·계약·확률·관계 수치는 무엇이 표시됐는지 입증하며 시스템의 진실성을 보증하지 않는다.|숫자 정확도와 사실 정확도는 독립
X18|비시각 문맥|등장·소멸·거부 가능성|sequence|S04 S21|context=ordered interface interaction|context>requires>context|Opening, closing, forced reappearance, gesture control, and countdown motion need sequential evidence.|개폐·강제 재등장·제스처 조작·카운트다운 움직임은 연속 증거가 필요하다.|손을 댄 한 장면은 실제 입력 반응·거부 가능성을 증명하지 않음'''

# Exact table row routes. More than one card can be consulted; none is automatically mandatory.
ROUTE_ROWS = {
0: 'X01 X01 X01 X01 X01 X01 X01 X01 I01 I01 W01 W03 I07 W01 W02 X01 Q11 Q09 W05 W06 X07',
1: 'X08 W01 I03 Q03 X08 X08 X08 X08 X11 X08 W01 X01 W01 W04 D01 C08 W04 X16',
2: 'I03 I03 I01 X04 X04 X04 X04 X04 X04 X04 X04 X04 I02 I02 I02 X04 I04 I01 X05 X05 Q07 I04 X04 X04 E05',
3: 'I06 I06 I06 I06 I06 C03 C03 X05 I08 I05 I05 X04 Q08 I07 X05 X05 X05 X05 I04 X05 D02 I03',
4: 'C01 C01 C06 C02 C07 C03 C03 C04 C04 X06 C05 C06 C04 X05 X06 X06 C08 X05 C05 X05 C08 D02 X13',
5: 'Q01 Q01 Q01 X06 Q02 Q03 Q04 Q04 X06 Q07 Q07 Q07 Q08 Q05 H01 Q04 Q07 Q09 Q09 Q06 Q10 Q10 Q12 Q12',
6: 'X06 X06 I08 X05 X16 X16 X16 E05 X07 X07 X11 X07 D03 X11 X11 X05 X05 C08 X15 R04 R04 X08 X08 X08 X11 X10',
7: 'D02 D01 D01 D02 D01 D02 X13 X13 X13 X13 D03 X12',
8: 'X13 X13 H02 H02 H02 H02 H03 X13 C07 X13 X13 X12 X12 H04 X01',
9: 'X10 X10 R01 R01 R01 R02 R02 X10 X10 X10 X10 X10 X10 X09 X10 X09 X09 X09 R03 R03 X09 H03 X10 X10 X10 X14 X14 X14 X14 H03 H01',
10: 'I01 I01 U02 I01 I01 I02 E01 C06 Q06 E06 Q02 Q03 E06 Q04 Q05 C03 E02 C03 E01 E04 E04 Q07 E05 E05 E03 Q03',
11: 'U02 U01 X03 U01 U01 U02 U08',
12: 'X02 X02 U01 X12 U06'
}
