"""Author-owned development cases; no retrieval or image calls."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CASE_TEXT='''
E01|병영·전투|생활관 침상 끝에 체육복 차림으로 앉아 벗은 군화를 바라보는 사람|A person in athletic clothes sits at a bunk edge looking at removed combat boots.|V01,V19|침상 지지·군화 별도 위치|전투·무기·신병·남은 복무기간을 자동 부여하지 않음
E02|서열·외형|어깨 계급 표지와 소매 부대 표장을 따로 보여주는 제복|A uniform showing a shoulder rank marker separately from a unit sleeve patch.|V27|표장 종류와 부착면 분리|국가·정확한 계급·보직을 임의 확정하지 않음
E03|경례·몸|두 인물이 나란히 서 있고 한 사람만 오른손으로 경례하는 모습|Two people stand side by side with only one saluting with the right hand.|V49|해당 인물 손·손목·팔꿈치·어깨|다른 사람 팔로 연결하지 않음;정확한 국가 변형은 별도
E04|군복·패턴|각진 무늬가 있는 전투복의 주머니와 여밈선|Pockets and closure seams on a combat uniform with angular pattern elements.|V13,V46|옷 구조와 무늬 분리|무늬만으로 ACU·OCP·군종을 단정하지 않음
E05|재사용·트렌치|견장과 가슴 플랩이 있고 허리 고리로 벨트가 지나는 트렌치코트|A trench coat with epaulettes, a chest flap and a belt through waist loops.|V20|같은 옷의 벨트·고리·플랩|첩보원·군인 신분을 자동 부여하지 않음
E06|리그·방호|셔츠 위에 어깨끈으로 지지된 얇은 전면 파우치 패널|A thin front pouch panel supported by shoulder straps over a shirt.|V31|패널·옷·끈|안 보이는 방호판·방탄 등급을 추가하지 않음
E07|캐리어·판|탁자 위에 벗어 놓은 캐리어의 열린 수납구 밖으로 나온 판의 윗부분|The top of a plate projects from an open pocket of a carrier removed onto a table.|V30|판이 같은 수납구로 이어짐|착용 중 투시·실제 방호 성능을 주장하지 않음
E08|부착·격자|천 패널의 가로 웨빙 줄을 지나 고정된 파우치 뒤 끈|Rear straps of a pouch pass through horizontal webbing rows on a fabric panel.|V32,V33|같은 패널·뒤 끈·통과 구간|격자 무늬만으로 실제 결합을 대체하지 않음
E09|슬링·군장|같은 소총의 두 부착점에서 어깨로 이어지는 슬링|A sling runs from two attachment points of the same rifle over the shoulder.|V35|두 부착점·같은 총·어깨|끈을 다른 총·몸으로 전이하지 않음
E10|배낭·음용관|배낭 위에서 나와 어깨끈을 따라 내려오는 물주머니 음용관|A hydration tube emerges from a rucksack and follows its shoulder strap down.|V37|배낭 시작·관 연속·마우스피스|산소·수액관으로 바꾸지 않음
E11|NVG·올림|헬멧 마운트의 광학 장치가 이마 위로 올라가 두 눈이 보이는 모습|A helmet-mounted optical device is raised above the forehead leaving both eyes visible.|V39|마운트·팔·눈의 상대 위치|내림 상태·눈앞 렌즈를 동시에 만들지 않음
E12|NVG·내림|헬멧에 연결된 야시 장치가 두 눈 앞에 내려온 모습|A night-vision device connected to a helmet is lowered before the eyes.|V40|같은 연결 팔·눈앞 장치|올림 상태와 합치지 않음;녹색 현실 공간을 추가하지 않음
E13|화면·실물|휴대 장치 화면 속의 밝은 인체 형상과 화면 밖의 풍경|A bright human-shaped image inside a handheld display and the landscape outside it.|V41|화면 테두리·화면 속 대상·주변 실물|표시를 실제 인물 수·적의 정체·정확한 체온으로 승격하지 않음
E14|무전·소리|손에 든 수화기에서 허리 무전기로 이어지는 꼬인 케이블|A coiled cable connects a hand-held handset to a waist radio.|V58|손·수화기·케이블 양끝|대화 내용·교신 성공·Roger/Wilco를 증명하지 않음
E15|지도·공동 주목|한 사람이 지도의 한 지점을 짚고 다른 두 사람이 같은 지점을 보는 장면|One person points to one map location while two others look at that same location.|V59|손의 대상·시선 공통 끝점·지도 지지|지도 앞 인원을 지휘권·전황의 진실로 해석하지 않음
E16|해치·지지|차량 해치에 허리가 이어지고 두 팔이 가장자리에 놓인 사람|A person whose waist continues into a vehicle hatch rests both arms on the rim.|V60|해치 개구·몸 연속·양팔 지지|상체가 차체에 붙거나 하체가 차 밖으로 분리되지 않음
E17|들것·후송|두 사람이 천 들것 양끝 손잡이를 잡고 같은 천이 누운 몸을 받치는 모습|Two people grip the end handles of a fabric stretcher supporting one reclining body.|V67|같은 프레임·양쪽 손·몸 지지|바퀴 들것·구급대원·MEDEVAC 자격을 자동 추가하지 않음
E18|flight deck·공간|전방 창 아래 콘솔이 있고 창밖 수평선이 보이는 함교|A ship bridge has consoles below forward windows looking toward the horizon.|V74|함교·콘솔·전방 창|항공기 cockpit 별칭의 비행갑판으로 바꾸지 않음
E19|노즈아트·인물|기체 코 곡면에 그려진 성인 인물 그림과 옆에 선 실제 정비사|An adult figure painted on an aircraft nose beside a real maintainer.|V83|곡면·패널선·그림/실물 경계|그림 속 사람을 추가 실물 인원으로 세지 않음
E20|하네스·패션|성인 모델의 제복 재킷 위에서 가는 장식끈이 가슴 링에 모이는 패션|Thin decorative straps meet at a chest ring over an adult model's uniform-style jacket.|V88|옷 층·장식끈·링|군장 하중·파우치·구속·실제 군인 신분을 자동 부여하지 않음
E21|전우·로맨스|군복과 사복 차림 두 사람이 현관에서 마주 포옹하는 모습|A uniformed person and a civilian-dressed person embrace face to face at an entry.|V69|각자 팔·상대 등·발 지지|가족·연인·동의·실제 귀환 이력을 외형에서 추론하지 않음
E22|표정·진단|가까운 손 안의 작은 물건 너머를 보는 앉은 인물|A seated person looks beyond a small object in nearby hands.|V82|눈과 물건의 상대 방향|PTSD·도덕적 손상·전쟁 경험을 확정하지 않음
E23|구금·법적 지위|같은 인물의 두 손목 고리를 짧은 사슬이 연결한 모습|A short chain links two cuffs around the same person's wrists.|V102|같은 주인·두 고리·연결|POW·범죄·학대·동의·성적 의미를 자동 부여하지 않음
E24|손상·원인|찢긴 소매 가장자리 아래 피부가 보이는 옷의 상태|A torn sleeve exposes skin beneath its separated fabric edges.|V103|천의 연속·소매/피부 경계|신체 훼손·전상·공격 원인을 옷 손상과 합치지 않음
'''
cases=[]
for line in CASE_TEXT.strip().splitlines():
    cid,topic,ko,en,targets,required,limit=line.split('|')
    cases.append(dict(id=cid,topic=topic,query_ko=ko,query_en=en,target_research_cards=targets.split(','),
                      required_relation_ko=required,unsupported_inference_ko=limit,
                      provenance='research_author_development_case',holdout=False,
                      expected_runtime_candidate_ids=[],execution_status='not_run'))
(ROOT/'evaluation-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
cards=json.loads((ROOT/'semantic-cards.json').read_text())
queries=[]
for card in cards:
    for lang in ['ko','en']:
        queries.append(dict(id=f"{card['id']}-{lang}",language=lang,text=card['positive_'+lang],
                            kind='literal_card_probe',target_research_cards=[card['id']],holdout=False))
for c in cases:
    for lang in ['ko','en']:
        queries.append(dict(id=f"{c['id']}-{lang}",language=lang,text=c['query_'+lang],
                            kind='authored_development_query',target_research_cards=c['target_research_cards'],holdout=False))
(ROOT/'evaluation-queries.json').write_text(json.dumps(queries,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'bilingual_queries':len(queries),'literal_card_queries':len(cards)*2,
                  'independent_holdout_cases':0,'executed_queries':0,'image_calls':0},indent=2))
