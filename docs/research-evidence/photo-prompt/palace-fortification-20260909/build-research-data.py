"""Build research-only drafts and source audit; does not register runtime data."""
import hashlib
import json
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'

def save(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

SOURCES = [
('S01','English Heritage','Goodrich Castle Glossary','https://www.english-heritage.org.uk/siteassets/home/visit/places-to-visit/goodrich-castle/school-visits/goodrich-castle-glossary.pdf','pp.1–2; gate, wall, openings','primary',None),
('S02','Historic England','Stone Castles','https://historicengland.org.uk/images-books/publications/iha-stone-castles/heag235-stone-castles/','PDF pp.5–6; arrangement and residential functions','primary',None),
('S03','English Heritage','Castles Through Time','https://www.english-heritage.org.uk/castles/castles-through-time/','Norman castles; stone keeps; later castles','primary',None),
('S04','Cadw','Beaumaris Castle','https://cadw.gov.wales/visit/places-to-visit/beaumaris-castle','Concentric defences and incomplete building','primary',None),
('S05','Cadw','Raglan Castle','https://cadw.gov.wales/visit/places-to-visit/raglan-castle','Gatehouse and flared machicolations','primary',None),
('S06','UNESCO World Heritage Centre','Fortifications of Vauban','https://whc.unesco.org/en/list/1283/','Bastioned towns, citadels, coastal and mountain sites','primary',None),
('S07','US National Park Service','Defense in Depth Wayside','https://www.nps.gov/places/000/defense-in-depth-wayside.htm','Ravelin, dry moat, covered way, glacis','primary',None),
('S08','UNESCO World Heritage Centre','Historic Fortified City of Carcassonne','https://whc.unesco.org/en/list/345/','Urban enclosure and nineteenth-century restoration','primary',None),
('S09','UNESCO World Heritage Centre','Castle of the Teutonic Order in Malbork','https://whc.unesco.org/en/list/847/','Brick Gothic castle-monastery and restoration','primary',None),
('S10','Getty Research Institute','Art & Architecture Thesaurus: keeps, 300003694','https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300003694','Scope note; keep/donjon sense','primary',None),
('S11','English Heritage','Life in a castle','https://www.english-heritage.org.uk/castles/life-in-a-castle/','Residential spaces, reconstructed Dover interiors, kitchens','primary',None),
('S12','English Heritage','Description of Dunstanburgh Castle','https://www.english-heritage.org.uk/visit/places/dunstanburgh-castle/history/description/','Gate passage, window seats, uncertain barbican reconstruction','primary',None),
('S13','Historic Royal Palaces','Great Hall, Hampton Court Palace','https://www.hrp.org.uk/hampton-court-palace/whats-on/great-hall/','Hammerbeam roof and Tudor hall','primary',None),
('S14','The Metropolitan Museum of Art','Gothic Art','https://www.metmuseum.org/essays/gothic-art','Pointed arches, rib vaults, support system and ornament','institutional_synthesis','2002-10'),
('S15','Château de Versailles','The King’s State Apartment','https://en.chateauversailles.fr/discover/estate/palace/king-state-apartment','Ceremonial rooms; marble, painted ceilings, changing use','primary',None),
('S16','Château de Versailles','The Hall of Mirrors','https://en.chateauversailles.fr/discover/estate/palace/hall-mirrors','Mirrors opposite windows; connected ceremonial gallery','primary',None),
('S17','Château de Versailles','Completion of the restauration of the Salon de Diane','https://en.chateauversailles.fr/press/restorations/completion-restauration-salon-diane','Enfilade; marble revetments; restoration','primary',None),
('S18','Wikipedia contributors','Enfilade (architecture)','https://en.wikipedia.org/wiki/Enfilade_(architecture)','Aligned doorways through a series of rooms; terminology cross-check','secondary',None),
('S19','Bavarian Palace Administration','Amalienburg','https://www.schloss-nymphenburg.de/englisch/p-palaces/amalien.htm','1734–1739 pleasure/hunting palace; Rococo interior ensemble','primary',None),
('S20','The Metropolitan Museum of Art','Boiserie from the Palais Paar','https://www.metmuseum.org/art/collection/search/202997','ca.1765–72 with later additions; mixed-room museum installation; gray paint','primary',None),
('S21','Domaine national de Chambord','Not to be missed','https://www.chambord.org/en/history/the-chateau/not-to-be-missed/','Twin helical ramps around a hollow core; keep and wings','primary',None),
('S22','Patronato de la Alhambra y Generalife','Patio de los Leones','https://www.alhambra-patronato.es/edificios-lugares/patio-de-los-leones','Open court, perimeter arcade, fountain and disputed original paving','primary',None),
('S23','Patronato de la Alhambra y Generalife','The Hall of the two sisters','https://www.alhambra-patronato.es/en/edificios-lugares/the-hall-of-the-two-sisters','Muqarnas dome, tile socle, fountain-to-court channel','primary',None),
('S24','Fondazione Musei Civici di Venezia','Building and history — Palazzo Ducale','https://palazzoducale.visitmuve.it/en/building-and-history/','Gothic/Renaissance/Mannerist phases and waterside wing','primary',None),
('S25','Victoria and Albert Museum','Robert Adam: Neoclassical architect and designer','https://www.vam.ac.uk/articles/robert-adam-neoclassical-architect-and-designer','Coordinated classical ornament across interior elements','institutional_synthesis','2024-04-17'),
('S26','Château de Versailles','The Orangery','https://en.chateauversailles.fr/discover/estate/gardens/orangery','Winter shelter/summer display; masonry galleries; parterre','primary',None),
('S27','Château de Versailles','The Groves','https://en.chateauversailles.fr/discover/estate/gardens/groves','Enclosed outdoor rooms, fountains and changes over time','primary',None),
('S28','Historic England','The Grotto and the River God’s Cave, list entry 1318473','https://historicengland.org.uk/listing/the-list/list-entry/1318473','Artificial rockwork, constructed chambers and water feature','primary','1987-09-09'),
('S29','Opéra national de Paris','Palais Garnier','https://www.operadeparis.fr/en/about/theaters-and-workshops/palais-garnier','Opera auditorium, staircase and public spaces','primary',None),
('S30','Scottish Geology Trust / McAdam and Clarkson (eds.)','Building stones of Edinburgh — Lothian geology: an excursion guide','https://geoguide.scottishgeologytrust.org/p/egs_lo/egs_lo_04_buildingstonesofedin','Building terms: ashlar, rubble, courses, mullions; not a current site-condition source','specialist_field_guide','1987'),
('S31','Bavarian Palace Administration','Neuschwanstein Castle — Historicism','https://www.neuschwanstein.de/englisch/idea/histor.htm','Medieval references combined with modern building technology','primary',None),
('S32','English Heritage','Description of Castle Acre Castle and Bailey Gate','https://www.english-heritage.org.uk/visit/places/castle-acre-castle-and-bailey-gate/history/description/','Mound and baileys, successive changes, town and castle gates','primary',None),
('S33','US National Park Service','Teacher-led School Groups — Castillo de San Marcos','https://www.nps.gov/casa/learn/education/classrooms/teacher-led.htm','Bastions, gun deck and ravelin geometry','primary',None),
]
save('sources.json', {'accessed_on':'2026-09-09','date_policy':'null means publication date not established; crawl dates are not publication dates', 'sources':[dict(zip(['id','publisher','title','url','scope','kind','publication_or_update_date'],s), access='page_body_read' if s[0]!='S33' else 'search_returned_substantial_page_text') for s in SOURCES]})

PROFILES=[]
def p(id, ko, aliases, priority, historical_scope, fact_sources, en, composition, gates, reject, limits='형태의 적합성은 실제 장소·연대·소유자·용도의 확정 근거가 아니다.'):
    PROFILES.append(dict(id=id,ko=ko,aliases=aliases.split(';'),priority=priority,historical_scope=historical_scope,source_ids=fact_sources.split(','),source_role='architectural premise only; wording, gates and camera choices are proposed operationalizations',scene_en=en,composition_en=composition,component_gates=[dict(id=f'{id}_g{i+1}',description_ko=g,review_scale='native' if i==1 else 'both') for i,g in enumerate(gates.split(';'))],reject_substitutes=reject.split(';'),claim_limits=limits,status='proposed',activation_policy='explicit named structure in correct sense or request-supplied component relation; broad style/place/mood labels and retrieval alone do not hard-activate',requires_human=False))

p('pf_motte_bailey','둔덕과 인접 방어구역','motte-and-bailey;모트 앤드 베일리;목책','P1','초기 노르만 계열의 한 유형','S03,S32','a tower on a raised earth mound beside a separately enclosed lower yard, linked by an ascending access route','an oblique elevated view retaining both ground levels and their connecting route','둔덕 정상과 탑이 붙어 있다;아래 구획의 방어 경계가 따로 읽힌다;두 구획 사이 접근로가 연속된다','탑만 있는 언덕;자연 언덕 옆 평범한 농장')
p('pf_keep_ward','주탑과 생활 구획','keep;great tower;donjon;주탑;bailey;ward','P0','중세 성의 선택적 구성; 모든 성의 필수 아님','S10,S02','a dominant fortified residential tower inside a bounded ward with smaller service buildings','a wide courtyard view showing the tower base, enclosure and adjacent working buildings together','주탑의 큰 체적이 별도 건물로 구별된다;마당 둘레 경계와 부속 건물이 보인다;탑 출입부와 마당이 같은 지면에 연결된다','지하 감옥;교회 종탑;주탑 없는 성을 오류 처리')
p('pf_concentric','중첩 성벽','concentric castle;동심형 성;중첩 성벽','P0','중세 후기의 특정 방어 구성','S04,S02','nested defensive wall circuits enclosing one castle, with an inner wall rising behind an outer wall and a visible intervening strip','an elevated oblique view across both circuits without hiding the space between them','한 성을 감싼 안팎 경계가 보인다;성벽 사이 공간이 추적된다;서로 다른 성 두 개가 아닌 포함 관계가 읽힌다','평행 담장 두 개;완벽한 원형을 강제;보마리스의 미완성을 폐허로 단정')
p('pf_walled_town','도시를 감싼 성곽','walled city;fortified town;성곽도시','P0','중세 및 중층 시대의 도시 방어','S08,S32','a defensive circuit enclosing connected streets, clustered houses and a civic or religious landmark','an elevated city-edge view including an entering street, gate and inhabited urban fabric','성벽 안에 복수 주택과 가로망이 보인다;도시 출입로가 문을 통과한다;성 하나의 안마당과 다른 도시 규모가 드러난다','성 한 채;빈 요새 마당;19세기 복원 모습을 중세 원형으로 확정')
p('pf_wall_tower_walk','성벽·측방탑·보행로','curtain wall;flanking tower;mural tower;wall walk;성벽 보행로','P1','여러 시대 성곽의 형태 관계','S01,S02','a wall segment joining projecting defensive towers with a continuous walk behind its parapet','an oblique view along the wall revealing the walk surface and the wall-to-tower junction','탑이 성벽 외측으로 돌출한다;탑 사이 벽이 끊기지 않는다;벽 위 보행면이 방벽 뒤에 붙어 있다','분리된 탑;공중에 뜬 보행로;현대 커튼월')
p('pf_crenellation','성가퀴의 실체와 틈','battlement;crenellation;merlon;crenel;성가퀴','P1','형태 단위; 기능과 연대는 별도','S01,S02','a parapet alternating solid upright blocks with open gaps, backed by a walkable surface','a near-oblique parapet view with background visible through its gaps','높은 실체와 열린 틈이 교대한다;틈 너머 외부 배경이 이어진다;요철이 지붕 장식이 아닌 방벽 상부에 속한다','벽면에 칠한 체크무늬;전면이 막힌 장식;요철만으로 전투용 성 확정')
p('pf_gate_sequence','외곽 방어구역에서 문루까지','barbican;gatehouse;바비칸;문루','P0','개별 성문의 접근 체계','S12,S32','an outer defended entry enclosure leading across a bounded approach into the main gatehouse passage','a three-quarter entry view retaining the outer enclosure, approach and inner doorway','외곽 구획과 본 문루가 구분된다;그 사이 길이 이어진다;문이 하나의 장식 아치로 축소되지 않는다','문루 자체를 무조건 바비칸이라 부름;근거 없는 미복원 구조 복원')
p('pf_portcullis','수직 격자 낙하문','portcullis;낙하문;격자 성문','P0','목재 또는 철재 격자; 특정 재료 고정 금지','S01,S12','a heavy gridded gate partly lowered within vertical side grooves inside a fortified entrance','a close oblique gate-passage view showing the grid edge seated inside its guide channel','격자가 출입 개구부 안에 있다;격자 옆단이 수직 홈에 맞물린다;문짝 회전이 아닌 상하 이동 구조가 읽힌다','옆으로 여는 철문;창살 창문;문장에 그려진 낙하문')
p('pf_drawbridge','도랑을 건너는 가동 교량','drawbridge;도개교','P0','연구 초안은 한쪽 경첩형; 모든 도개교 방식 대표 아님','S01,S33','a timber bridge deck raised partway about a hinge at the gate threshold, leaving a gap over the ditch','a side-three-quarter view retaining the hinge line, tilted deck and ditch beneath','교량판이 문턱에 붙어 회전한다;기울어진 판 아래 도랑이 보인다;반대편 접근로와 교량 끝의 틈이 구별된다','낙하문;고정 석교;매달린 공중 발판')
p('pf_machicolation','돌출 방벽 아래 개구부','machicolation;마시쿨레이션','P0','중세 방어시설 형태; 실전 사용 여부 별도','S05','a corbel-supported stone parapet projecting beyond the wall face, with openings through its underside','a low oblique exterior view exposing the gap beneath the projection and its stone supports','방벽이 본 벽면 밖으로 나온다;받침돌 사이 바닥 개구부가 보인다;개구부가 외벽 바깥 수직선 위에 있다','장식 처마 받침만 있음;문 통로 천장의 murder hole;실제 투하 장면 강제')
p('pf_arrow_loop','좁은 외부 틈과 안쪽 창턱','arrow loop;arrow slit;화살창','P1','형태·사용 맥락을 함께 확인','S01,S02','a narrow exterior slit through a thick defensive wall, opening into a wider interior recess','an interior oblique view retaining the recess sides and narrow daylight opening','좁은 외부 개구부가 보인다;안쪽 공간과 벽 두께가 연결된다;일반 큰 창이나 유리창으로 치환되지 않는다','장식 세로 선;커튼 틈;총안과 시대를 무차별 혼합')
p('pf_dry_moat','물 없는 방어 도랑','dry moat;defensive ditch;마른 해자','P0','담수 유무와 방어기능 분리','S07,S33','an excavated dry ditch beside the fort wall, with readable banks and a bridge crossing its exposed floor','an oblique edge view showing the ditch cross-section and continuous wall base','벽 아래 도랑 바닥이 노출된다;양안과 고저차가 읽힌다;횡단로가 도랑을 건너며 물로 채워지지 않는다','강이나 호수;평면 잔디 띠;모든 해자는 물이라는 기본값')
p('pf_bastion_ravelin','능보와 분리된 외보','bastion;ravelin;star fort;능보;라블랭','P0','근세 포병 요새; 특정 평면의 선택','S06,S07,S33','angular projecting bastions joined to the main enceinte, with a separate wedge-shaped ravelin across the ditch shielding the entrance','an elevated oblique plan-readable view preserving the gap between the main wall and the detached outwork','능보가 주 방어선과 연결된다;삼각 외보는 도랑 건너 분리된다;문·외보·접근로 위치가 구별된다','별 모양 지붕;모든 꼭짓점을 분리 탑으로 그림;라블랭과 능보 동의어')
p('pf_gun_battery','포대의 배치 관계','gun battery;cannon embrasure;포대;포좌','P1','포병 시대; 지형별 변형 허용','S33,S06','a broad gun platform behind a defensive parapet with mounted cannon facing outward through corresponding openings','a rear-side battery view retaining carriage contact, platform depth and outward orientation','포가 포가대와 지면에 지지된다;포신 방향이 외부 사계로 향한다;방벽 개구부와 포 위치가 대응한다','좁은 중세 화살창에 거대 포;공중에 뜬 포;방 안 장식 대포만 있음')
p('pf_window_seat','두꺼운 벽 속 창가 좌석','window recess;window seat;깊은 창가 좌석','P0','거주·문루 실내 등의 특정 공간','S12','a built-in seat occupying a deep window recess within thick masonry, with the window beyond the seat plane','a side-oblique interior view preserving seat depth, both reveals and the outer opening','좌석이 벽 깊이 안에 들어간다;창 측벽과 바깥 개구부가 연결된다;가구 하나를 창 앞에 둔 장면과 구별된다','얇은 현대 벽과 이동식 의자;인물 크롭으로 벽 두께 소실')
p('pf_hammerbeam_hall','목조 지붕 대홀','great hall;hammerbeam roof;대홀;해머빔','P1','튜더 예시; 일반 대홀의 필수 지붕은 아님','S13','a long communal hall beneath an exposed hammerbeam timber roof, with roof supports rising above a readable occupied floor zone','a longitudinal interior view including the upper roof structure and the hall floor','목재 지붕 구조가 노출된다;짧게 내민 보와 상부 지지 구조가 연결된다;공간 아래 생활용 홀의 바닥이 보인다','석조 리브 볼트;일반 통보 지붕을 해머빔이라 명명;모든 중세 홀에 강제')
p('pf_rib_vault_chapel','리브 볼트와 예배 공간','ribbed vault;castle chapel;리브 볼트;예배당','P1','고딕 계열 특정 구조; 예배당은 규모 별도','S14,S01','a compact chapel where stone ribs cross overhead and descend toward supports beside pointed openings, with a distinct worship end','a diagonal interior view showing ceiling intersections, wall supports and the chapel end','천장 리브가 교차한다;리브가 벽측 지지부와 연속된다;공간 끝의 예배 영역이 구분된다','천장에 그린 선;로마네스크 통형 볼트;성 전체를 대성당으로 바꿈')
p('pf_enfilade','방들을 관통하는 문 축선','enfilade;앙필라드','P0','궁전·대저택의 공간 구성; 고유 연대 아님','S18,S17','a sequence of separate furnished rooms whose open doorways align along one continuous sightline','a doorway-axis view through at least three readable room thresholds, with lateral wall returns revealing separate rooms','열린 문들이 한 시선축에 정렬된다;문마다 별도의 방과 벽 돌아감이 보인다;거울 복제가 아닌 실제 문 너머 깊이가 이어진다','긴 복도 옆에 난 문들;거울 무한반사;아치만 반복되는 단일 홀','세 문턱은 테스트용 가시성 기준이며 enfilade의 역사적 정의상 최소 개수가 아니다.')
p('pf_mirror_gallery','창과 마주보는 거울 회랑','hall of mirrors;mirror gallery;거울 회랑','P0','베르사유를 참고한 한 구성; 모든 거울방의 정의 아님','S16','a long gallery with repeated mirrors along one wall facing repeated windows on the opposite wall, both surfaces sharing one floor','an oblique central view showing actual windows, mirror surfaces and their corresponding reflections','실제 창벽과 맞은편 거울벽이 구별된다;반사된 창·기둥이 일관된 대응을 만든다;반사가 독립 방이나 추가 인물로 변하지 않는다','창문 양쪽 복제;거울을 문으로 그림;정확한 357장 수량을 일반 후보에 강제')
p('pf_rocaille_boiserie','로카유 장식 목재 패널','rocaille;boiserie;rococo salon;로코코 살롱','P0','18세기 로코코 실내의 선택적 모티프','S19,S20','carved wall panels whose curved frames integrate shell-like and foliate relief around a mirror and wall openings','a medium interior view retaining panel boundaries, relief depth and their relationship to the mirror','장식이 목재 패널 구획에 붙어 있다;곡선 장식에 깊이와 음영이 있다;거울·문틀·패널의 실내 관계가 읽힌다','금색 벽지 하나;펑크 의상;모든 패널·방을 비대칭으로 강제','로코코 전체를 금색·파스텔·전면 비대칭으로 정의하지 않는다. 박물관 조합실은 원위치 복원과 구분한다.')
p('pf_renaissance_court','질서 있는 궁정 중정','Renaissance palace;courtyard;loggia;르네상스 중정','P1','르네상스에서 영감받은 창작 구성','S21,S24','a palace courtyard enclosed by residential wings, with repeated bays and an upper gallery aligned over the lower level','a corner courtyard view retaining two adjoining elevations and their vertical bay alignment','중정 주위에 실제 건물동이 연결된다;층간 개구부 리듬이 대응한다;내부 중정과 외부 광장이 구별된다','균일한 현대 호텔;기둥만으로 연대 확정','이 장면 문법은 창작 설계이며 샹보르나 두칼레궁의 정확한 평면 복원이 아니다.')
p('pf_double_helix','서로 만나는 듯 분리된 두 계단','double-helix staircase;이중 나선계단','P0','샹보르 사례의 구조 관계','S21','two distinct helical stair flights winding around a shared hollow core, each retaining its own landings and circulation path','an oblique central-core view showing both flights over more than one level','두 개의 계단 경로가 추적된다;공유 중심부가 비어 보인다;두 경로가 중간에서 임의로 합쳐지거나 충돌하지 않는다','단일 나선계단;좌우 대칭 갈래 계단;외관 사진으로 내부 구조 증명')
p('pf_nasrid_water_court','나스르 중정과 수로 연결','Nasrid courtyard;Court of Lions;나스르 궁전;수로 중정','P0','알람브라를 참고한 관계; 정확한 장소 재현 별도','S22,S23','an open palace court enclosed by arcades, with a central basin linked to shallow axial water channels leading toward surrounding rooms','a court-edge view preserving a basin, a connected channel and the perimeter arcade in one frame','중정이 하늘로 열려 있다;수반과 수로가 물리적으로 연결된다;회랑·수로·주변 방 사이 공간이 이어진다','독립 분수 하나;일반 오리엔탈 장식;원래 바닥 식재 상태를 확정','사자의 중정 원래 바닥의 포장·식재 구성은 출처가 논쟁을 명시한다. 모든 나스르 궁전에 사자상·십자 수로를 강제하지 않는다.')
p('pf_muqarnas','입체 셀로 구성된 천장','muqarnas;무카르나스','P1','여러 이슬람 건축 전통; 나스르 사례 참조','S23','tiered small cellular niches forming a three-dimensional ceiling transition around a central geometric focus','an upward oblique view with enough side light to separate the depth of adjacent cells','셀 단위가 여러 층으로 겹친다;셀 내부 깊이가 실제 음영으로 읽힌다;벽 상단과 천장 사이 입체 전이가 보인다','평면 별 타일;일반 종유석 동굴;샹들리에')
p('pf_brick_castle','벽돌 성곽과 고딕 개구부','Brick Gothic;Malbork;벽돌 고딕','P1','발트해권 참고; 색만으로 지역 확정 금지','S09','a fortified courtyard whose brick courses continue through wall masses and shaped arched openings','a medium-wide court view retaining masonry joints and the relation of openings to thick walls','벽돌 단위와 줄눈이 보인다;벽돌이 아치·벽체를 구성한다;붉은 페인트 석재나 얇은 외장지와 구별된다','붉은 색조 필터;기사단 문장 자동 추가;복원 사진을 13세기 원형으로 단정')
p('pf_venetian_arcade','수변 궁전의 층별 아케이드','Venetian Gothic;Doge palace;베네치아 고딕','P1','두칼레궁에서 영감받은 형태 연구','S24,S14','a waterside palace elevation with an open lower arcade, a finer upper openwork gallery and a broad wall mass above','a water-edge oblique view retaining the lower arcade, upper gallery and palace mass','열린 아래 아케이드가 보인다;위층 개구 리듬이 아래층과 구별된다;상부 벽체가 갤러리 위에 실제로 지지된다','물가 대성당;공중 부양 벽;모든 고딕 궁전을 베네치아로 판정','세부 입면은 공식 사진과 대조할 후속 항목이며 복합 시대 건물의 단일 양식 확정은 피한다.')
p('pf_neoclassical_room','신고전주의 실내의 연결된 장식','neoclassical interior;Adam interior;신고전주의','P1','18세기 후반 영국 Adam 사례 참조','S25','a classical interior where restrained repeated ornamental bands coordinate wall divisions, ceiling panels and furnishings','a room-corner view retaining both wall-to-ceiling junctions and one corresponding furnishing','벽·천장 장식의 공통 모티프가 읽힌다;실내 구획과 장식 크기가 조화를 이룬다;흰색 기둥 하나로 유형을 대체하지 않는다','무장식 흰 방;그리스 유적을 실내로 치환;파스텔 금지')
p('pf_parterre_axis','낮은 정원 구획과 궁전 축선','formal garden;parterre;정형식 정원;파르테르','P1','특정 정형식 정원 구성; 시대·형태 고정 아님','S26,S27','low bounded planting or lawn compartments arranged around readable paths and a palace-facing axis','an elevated terrace view preserving the compartment plan and its axis toward the building','낮은 구획 경계가 평면 무늬를 만든다;길과 식재 구획이 구분된다;건물 방향 축선이 이어진다','높은 생울타리 미로;자연 초지;모든 파르테르에 꽃 요구')
p('pf_bosquet','수목 벽 안의 야외 방','bosquet;garden grove;보스케','P1','베르사유 정원 사례; 시기별 구성 다름','S27','a small garden room enclosed by dense greenery, entered through a narrow opening and organized around a basin or sculpture','a view from the entry showing the enclosure, interior gathering space and focal feature','녹지 벽이 내부 공간을 감싼다;입구와 내부 빈 공간이 연결된다;중심 시설이 자연 숲과 다른 정원 구성을 만든다','열린 숲길;전체 정원 조감;미로 길찾기 자동 추가')
p('pf_orangery','오랑주리의 월동 공간','orangery;오랑주리','P1','베르사유 masonry orangery 사례; 전체 유형 대표 아님','S26','a masonry garden gallery with tall windows sheltering container-grown citrus trees along a passable aisle','a diagonal gallery view linking the tree containers, thick window reveals and garden-facing entrance','나무가 이동 가능한 용기에 심겨 있다;창 있는 실내 공간에 놓인다;열대 정글이 아닌 통행 가능한 월동 배치다','전면 유리 식물원 강제;노지 과수원;겨울·여름 배치를 한 장면에 동시 강제')
p('pf_roofless_ruin','지붕 소실과 남은 실내 구조','roofless hall;castle ruins;폐성;성터','P0','상태 축; 원래 용도와 쇠락 원인은 별도','S12,S08','a roofless former hall with wall returns, surviving window openings and localized fallen masonry beneath the missing upper structure','a wide interior view including open sky above the room and the surviving wall-to-floor connections','지붕이 없어 방 안에서 하늘이 보인다;남은 벽·창·바닥이 이전 실내를 이룬다;파손이 구조 경계와 연결되며 단순 이끼가 아니다','잘 보존된 성에 담쟁이만 추가;전쟁 원인 단정;관리된 유적을 버려진 장소로 확정')
p('pf_garden_grotto','정원에 만든 인공 동굴','garden grotto;folly;인공 동굴','P1','18세기 풍경정원 사례; 장소 이력 별도','S28','a constructed rockwork grotto where a shaped chamber opens toward a landscaped water feature and a maintained garden path','a threshold view linking the grotto interior, crafted opening and garden beyond','동굴 같은 표면 뒤에 조성된 공간 구조가 읽힌다;정원 동선과 개구부가 이어진다;동굴·수경 시설이 같은 설계 공간으로 보인다','자연 석회동굴;실제 폐성;인공 유적을 자연 쇠락으로 단정')
p('pf_theatre_stair','극장의 계단·계단참·관람 관계','Palais Garnier;grand staircase;오페라 대계단','P1','19세기 사교·공연 건축; 왕궁과 별도','S29','a monumental opera-house stair rising toward landings and surrounding spectator balconies within a tall decorated interior','a lower-landing view preserving stair runs, upper landings and balcony sightlines','계단이 계단참에 실제로 연결된다;주변 발코니가 계단 공간을 향한다;공연장 맥락을 유지하고 왕좌를 추가하지 않는다','이중 나선계단으로 치환;왕궁으로 명명;난간과 계단 충돌')
p('pf_masonry_finish','다듬은 돌과 불규칙 돌쌓기','ashlar;rubble masonry;다듬은 돌;막돌 쌓기','P1','재료 마감 축; 폐허·시대·지역과 독립','S30','a masonry junction contrasting squared coursed blocks with irregular stonework, with mortar joints following the actual stone boundaries','a close oblique wall view under raking light retaining both masonry regions and their physical junction','반듯한 돌 구획과 불규칙 구획이 구별된다;줄눈이 돌의 경계를 따른다;거친 표면을 곧바로 붕괴 상태로 처리하지 않는다','rubble masonry를 잔해 더미로 번역;벽지 질감;색상만으로 암석 종 확정')

drafts=[]
bundles=[]
cases=[]
for x in PROFILES:
    ids=[]
    for slot,text in [('location',x['scene_en']),('composition',x['composition_en'])]:
        cid=x['id']+'_'+slot
        ids.append(cid)
        drafts.append(dict(id=cid,slot=slot,ko=x['ko']+(' 공간 관계' if slot=='location' else ' 관찰 구도'),en=text,aliases=x['aliases'] if slot=='location' else [],keywords=x['aliases'] if slot=='location' else [],tags=['palace_fortification_research',x['id'],slot],concept_units=[text],affected_dimensions=['setting' if slot=='location' else 'composition'],profile_proposal_id=x['id'],source_ids=x['source_ids'],candidate_status='research_only',render_validated=False,eligibility='request-compatible architecture meaning only; no automatic era, character, weather, costume or genre'))
    bundles.append(dict(id=x['id']+'_bundle_proposal',candidate_ids=ids,candidate_slots=dict(zip(ids,['location','composition'])),component_groups=[g['description_ko'] for g in x['component_gates']],confusion_boundaries=x['reject_substitutes'],associated_proposal_id=x['id'],adoption='optional',profile_activation='independent_request_evidence_only',status='design_not_runtime_schema'))
    cases += [dict(id=x['id']+'_positive',kind='positive_proposal',request=x['scene_en'],expected=x['id'],pixel_gates=[g['id'] for g in x['component_gates']],status='not_run'),dict(id=x['id']+'_contrast',kind='confusion_negative',request=x['reject_substitutes'][0],expected_no_automatic_profile=x['id'],status='not_run')]
save('candidate-drafts.json',dict(schema_version='palace-fortification-research-draft/v1',decision='proposed',runtime_compatible=False,profiles=PROFILES,candidates=drafts,bundles=bundles))

extra=[
('h01','궁전풍 호텔 로비','keep/portcullis/왕좌 자동 삽입 금지'),
('h02','성 없이 촬영한 로코코풍 드레스','건축·rococopunk로 전환 금지'),
('h03','낙하문 문장이 새겨진 깃발','실제 낙하문 프로필 비활성'),
('h04','I keep my notebook near a glass curtain wall','keep 주탑 및 성곽 curtain wall 비활성'),
('h05','해자가 없는 궁전','해자/도개교 강제 금지'),
('h06','밝은 낮의 고딕 예배당','공포·밤·폐허 자동 주입 금지'),
('h07','주탑 없는 중세 성곽','keep 필수 조건 금지'),
('h08','현대 복장을 입은 관광객이 노이슈반슈타인을 방문','중세 인물·의상·사진의 시대를 강제하지 않음'),
('h09','거울 회랑 대신 방 문들이 일직선으로 이어진 앙필라드','거울 후보 비활성; 방 구획 보존'),
('h10','마른 해자 너머 낮은 능보 요새의 사람 없는 전경','인물·물·높은 첨탑 자동 추가 금지'),
('h11','금박 없는 회색 로코코 보아즈리','금색 강제 금지; 패널과 조각 형상 유지'),
('h12','고딕과 바로크가 혼합된 판타지 궁전','명시 혼합 허용; 역사 사실로 주장하지 않음'),
('h13','정원 미로 옆의 열린 파르테르','미로와 낮은 구획 동시 존재 허용; 서로 치환하지 않음'),
('h14','성문에서 인물 얼굴만 보이는 타이트한 초상','성문 관계의 픽셀 검증 불가능을 기록; 전신 강제 변경 금지'),
('h15','사용 중인 중세 성의 채색 벽과 직물','회색 폐허 기본값 금지'),
('h16','다듬은 돌에 표면 녹화가 있는 보존된 성','masonry/condition/vegetation 별도'),
]
cases += [dict(id=i,kind='holdout',request=q,expectation=e,status='not_run') for i,q,e in extra]
save('verification-plan.json',dict(schema_version='palace-fortification-verification-plan/v1',status='not_executed',cases=cases,render_plan=dict(arms=['baseline_without_new_data','optional_candidate_exposure','requested_structural_profile'],controls=['same raw request and generation configuration','freeze each arm prompt and pack hashes','do not inspect sibling outputs during composition','one registered attempt per trial; blocked is unscored','repeat multiple matched trials before causal improvement claims'],priority_profiles=[x['id'] for x in PROFILES if x['priority']=='P0'],pass_rule='all material in-frame gates pass; occluded required relation fails a visibility contract; absence of render is unscored',separate_evidence=['package_validity','request_routing','candidate_exposure','candidate_adoption','prompt_actuation','generation_delivery','pixel_fidelity','user_judgment'])))

terms=['castle','palace','fortress','enfilade','portcullis','machicolation','bastion','drawbridge','concentric','rococo','궁전','성채','성곽']
audit=[]
for f in sorted(ASSETS.glob('*.json')):
    if 'index' in f.name: continue
    data=json.loads(f.read_text())
    hits=[]
    def walk(v,path=''):
        if isinstance(v,dict):
            if 'id' in v:
                fields={k:v[k] for k in ['id','ko','en','aliases','activation'] if k in v}
                txt=json.dumps(fields,ensure_ascii=False).lower()
                matched=[t for t in terms if (re.search(r'\b'+re.escape(t)+r'\b',txt) if t.isascii() else t in txt)]
                if matched:hits.append(dict(path=path,id=v['id'],terms=matched,fields=fields))
            for k,z in v.items():walk(z,path+'/'+k)
        elif isinstance(v,list):
            for i,z in enumerate(v):walk(z,path+'/'+str(i))
    walk(data)
    audit.append(dict(path=str(f.relative_to(ROOT)),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),hits=hits))
save('local-coverage.json',dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),scope='top-level source asset JSON, excluding generated indexes; matching id/ko/en/aliases/activation only; lexical audit is not full semantic or runtime evidence',terms=terms,files=audit,script_source='build-research-data.py',status='read_only_snapshot'))

rows=['# 구조 프로필과 후보 데이터 매핑','', '모든 행은 연구 제안이다. 관찰 조건은 역사적 정의가 아니라 렌더 검증을 위한 조작적 기준이다.','', '|우선순위|프로필|검색어|화면에서 확인할 관계|혼동 경계|출처|','|---|---|---|---|---|---|']
lookup={s[0]:s for s in SOURCES}
for x in PROFILES:
    refs=' '.join(f'[{s}]({lookup[s][3]})' for s in x['source_ids'])
    rows.append(f"|{x['priority']}|{x['ko']} / `{x['id']}`|{', '.join(x['aliases'])}|{' / '.join(g['description_ko'] for g in x['component_gates'])}|{' / '.join(x['reject_substitutes'])}|{refs}|")
(HERE/'profile-matrix.md').write_text('\n'.join(rows)+'\n')
print(json.dumps(dict(profiles=len(PROFILES),candidates=len(drafts),bundle_proposals=len(bundles),gates=sum(len(x['component_gates']) for x in PROFILES),test_cases=len(cases),sources=len(SOURCES)),ensure_ascii=False))
