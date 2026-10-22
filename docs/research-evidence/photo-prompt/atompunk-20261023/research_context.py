"""Research inputs only; no operating corpus or image generation imports."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
CONVERSATION = '6ada2ca9-1618-83ee-a5f8-f03f49b24312'
DATE = '2026-10-23'

# Transcribed term labels from all 13 rendered vocabulary tables in the referenced chat.
# Each original multi-term row stays one seed; these are not 191 independent genre names.
SECTIONS = [
('장르·인접 개념', '''Atompunk / Atomicpunk — 아톰펑크
Retrofuturism — 레트로퓨처리즘
Atomic Age — 원자력 시대
Space Age — 우주 시대
Jet Age — 제트 시대
Raygun Gothic — 레이건 고딕
Raypunk — 레이펑크
Rocketpunk — 로켓펑크
Steampunk — 스팀펑크
Dieselpunk — 디젤펑크
Decopunk — 데코펑크
Cassette Futurism — 카세트 퓨처리즘
Soviet Retrofuturism — 소비에트 레트로퓨처리즘
Alternate History — 대체 역사'''),
('에너지·과학 낙관', '''Atomic Optimism — 원자력 낙관주의
Atoms for Peace — 평화를 위한 원자력
Too Cheap to Meter — 계량할 필요조차 없을 만큼 싼 전력
Nuclear Fission — 핵분열
Nuclear Fusion — 핵융합
Nuclear Reactor / Reactor Core — 원자로·노심
Miniature Reactor — 초소형 원자로
Atomic Battery / RTG — 원자력 전지·방사성동위원소 열전발전기
Ford Nucleon — 포드 뉴클리온
Nuclear Thermal Rocket — 핵열 로켓
Project Orion / Nuclear Pulse Propulsion — 오리온 계획·핵펄스 추진
Project Plowshare — 플라우셰어 계획
Uranium Prospecting — 우라늄 탐사
Geiger Counter — 가이거 계수기
Cloud Chamber — 안개상자
Cherenkov Glow — 체렌코프광
Atomic Energy Lab — 원자력 실험 완구'''),
('우주·교통·장비', '''Space Race — 우주경쟁
Sputnik — 스푸트니크
Cosmonaut — 코스모노트
Finned Rocket — 꼬리날개가 강조된 로켓
Flying Saucer — 비행접시
Flying Car — 하늘을 나는 자동차
Jetpack / Rocket Belt — 제트팩·로켓 벨트
Lunar Colony / Moon Dome — 달 거주지·월면 돔
Wheel Space Station — 바퀴형 우주정거장
Artificial Gravity — 인공중력
Bubble Helmet — 버블 헬멧
Silver Spacesuit — 은색 우주복
Ray Gun / Disintegrator — 광선총·분해광선총
Force Field — 역장·보호장'''),
('컴퓨터·로봇·조작계', '''Vacuum Tube — 진공관
Transistor — 트랜지스터
Mainframe / Room-sized Computer — 대형 컴퓨터
Analog Computer — 아날로그 컴퓨터
Electronic Brain — 전자두뇌
CRT — 브라운관
Oscilloscope — 오실로스코프
Nixie Tube — 닉시관
Punched Card — 천공카드
Magnetic Tape Reel — 자기테이프 릴
Control Console — 제어 콘솔
Radar Display / SAGE — 레이더 화면·SAGE
Cybernetics — 사이버네틱스
Servomechanism — 서보 기구
Domestic Robot — 가정용 로봇
Android / Gynoid — 안드로이드·여성형 인조인간
Cyborg — 사이보그'''),
('건축·도시', '''Mid-century Modern — 미드센추리 모던
Googie — 구기 건축
Streamline Moderne — 스트림라인 모던
Populuxe — 포퓰럭스
Upswept Roof — 치켜올린 지붕
Cantilever — 캔틸레버
Butterfly Roof — 나비 지붕
Folded-plate Roof — 절판 지붕
Geodesic Dome — 지오데식 돔
Flying-saucer Architecture — 비행접시형 건축
World’s Fair — 세계박람회
Monorail — 모노레일
Suburbia / Ranch House — 교외 주거지·랜치 하우스
Soviet Modernism — 소비에트 모더니즘'''),
('형태·색·재료', '''Atomic Motif — 원자 모티프
Starburst / Sunburst — 스타버스트·선버스트
Sputnik Chandelier — 스푸트니크 샹들리에
Boomerang Shape — 부메랑형
Kidney Shape — 강낭콩형
Biomorphic Design — 생물형 디자인
Chrome Trim — 크롬 장식
Formica / Decorative Laminate — 포마이카·장식용 적층판
Molded Plastic — 성형 플라스틱
Fiberglass — 유리섬유 강화 재료
Pastel Enamel — 파스텔 에나멜
Two-tone Color — 투톤 배색
Tailfins — 테일핀
Bubble Canopy — 버블 캐노피'''),
('소비·생활·광고', '''Diner — 다이너
Drive-in — 드라이브인
Motor Lodge / Motel — 모터 로지·모텔
Neon Sign / Pylon Sign — 네온·파일런 간판
Jukebox — 주크박스
TV Dinner — TV 디너
Dream Kitchen — 드림 키친
Push-button Living — 버튼식 생활
Bachelor Pad — 독신자의 세련된 주거 공간
Tiki Culture — 티키 문화
Advertising Mascot — 광고 마스코트
Consumer Utopia — 소비 유토피아
Atomic Tourism — 원자력 관광'''),
('패션·헤어', '''New Look — 뉴 룩
Pencil Skirt — 펜슬 스커트
Bullet Bra — 불릿 브라
Sweater Girl — 스웨터 걸
Space-age Fashion — 우주 시대 패션
Mini Dress / Shift Dress — 미니드레스·시프트 드레스
Go-go Boots — 고고 부츠
Metallic Fabric / PVC Fashion — 금속성 직물·PVC 패션
Mod — 모드
Jumpsuit / Unisex Uniform — 점프슈트·유니섹스 제복
Beehive Hairdo — 비하이브 헤어'''),
('성인 시각문화·비평', '''Pin-up — 핀업
Cheesecake — 치즈케이크 이미지
Beefcake — 비프케이크 이미지
Bombshell — 밤셸
Bikini — 비키니
Miss Atomic Bomb — 미스 아토믹 봄
Showgirl / Burlesque — 쇼걸·벌레스크
Space Babe / Space Siren — 우주 미녀·우주의 유혹자
Erotic Science Fiction — 에로틱 SF
Sexploitation — 섹스플로이테이션
Fetish Fashion — 페티시 패션
BDSM Iconography — BDSM 도상
Artificial Lover — 인공 연인
Sexual Liberation — 성적 해방'''),
('음악·그래픽·매체', '''Space-age Pop — 스페이스 에이지 팝
Lounge Music — 라운지 음악
Exotica — 엑조티카
Hi-fi / Stereophonic Sound — 하이파이·스테레오 사운드
Theremin — 테레민
Electronic Tonalities — 전자적 음향
Public Service Film — 공공 교육·홍보영화
Newsreel — 뉴스영화
B-Movie Aesthetics — B급 영화 미학
Pulp Cover Art — 펄프 표지화
Kitsch — 키치
Camp — 캠프'''),
('냉전·사회 통제', '''Cold War — 냉전
Iron Curtain — 철의 장막
Red Scare — 적색 공포
McCarthyism — 매카시즘
Blacklisting — 블랙리스트
Lavender Scare — 라벤더 공포
Military–Industrial Complex — 군산복합체
Technocracy — 기술관료주의
Corporate Paternalism — 기업 온정주의·가부장주의
Surveillance State — 감시 국가
Loyalty Test — 충성심 검사
Suburban Conformity — 교외의 동조 압력
Nuclear Family — 핵가족
Gender Roles / Domesticity — 성 역할·가정성
Objectification / Male Gaze — 대상화·남성적 시선'''),
('핵전쟁·민간 피해', '''Nuclear Arms Race — 핵 군비경쟁
Nuclear Deterrence — 핵 억지
MAD, Mutual Assured Destruction — 상호확증파괴
Brinkmanship — 벼랑 끝 전술
Doomsday Device — 최후의 날 장치
Civil Defense — 민방위
Duck and Cover — 엎드려 몸을 가리기
Fallout Shelter — 낙진 대피소
Radioactive Fallout — 방사성 낙진
Mushroom Cloud — 버섯구름
Nuclear Test Site — 핵실험장
Doom Town / Test Houses — 핵실험용 모형 마을
Radiation Sickness — 방사선 질환·피폭 피해
Downwinders — 풍하 지역의 피폭 피해 주민들
Nuclear Colonialism — 핵 식민주의
Nuclear Winter — 핵겨울
Post-nuclear Wasteland — 핵전쟁 이후의 황무지'''),
('괴수·실험·폭력', '''Mad Scientist — 광기 어린 과학자
Secret Laboratory — 비밀 연구소
Human Experimentation — 인간 대상 실험
Atomic Monster — 원자력 괴수
Kaiju — 괴수
Giant Insects — 거대 곤충
Radiation-induced Mutation — 방사선 유발 돌연변이
Mutant Outcast — 배척당한 돌연변이
BEM, Bug-eyed Monster — 눈이 툭 튀어나온 괴물
Alien Invasion — 외계 침공
Body Snatcher / Replacement Paranoia — 신체 강탈·대체 불안
Brain in a Jar — 병 속의 뇌
Mind Control — 정신 지배
Super-soldier — 초인 병사
Eugenics / Reproductive Control — 우생학·생식 통제
Sexual Captivity / Coercion — 성적 감금·강압
Body Horror — 바디 호러
Gore / Splatter — 고어·스플래터
Robot Uprising — 로봇 반란'''),
]


def seeds():
    rows = []
    for section, (category, text) in enumerate(SECTIONS, 1):
        for row_in_table, line in enumerate(text.splitlines(), 1):
            en, ko = line.split(' — ', 1)
            rows.append({'id': f'A{len(rows)+1:03}', 'section': section,
                         'row_in_original_table': row_in_table, 'category_ko': category,
                         'en': en, 'ko': ko})
    assert len(rows) == 191
    return rows
