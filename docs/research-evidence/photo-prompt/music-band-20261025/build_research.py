"""Build research-only music/band artifacts. Never imports or edits runtime data."""
from pathlib import Path
import json, hashlib, re, collections

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

# Publisher text establishes bounded facts. All complete scenes below are authored options.
# Fields: ID | title | URL | evidence file | scope | access
SOURCE_ROWS = '''
S01|Fender — Palm muting|https://www.fender.com/articles/techniques/3-keys-to-ace-your-palm-muting|web-verified-a.txt|피킹 손바닥과 브리지 근처 현의 접촉|publisher_text_read
S02|Fender — Guitar solo techniques|https://www.fender.com/articles/techniques/how-to-guitar-solo|web-verified-a.txt|벤딩·태핑·얼터네이트 피킹의 연주 문맥|publisher_text_read
S03|Fender — Beginner bass guide|https://www.fender.com/articles/techniques/how-to-play-bass-guitar|web-verified-a.txt|기타와 베이스 역할·현·핑거스타일·피크·슬랩/팝|publisher_text_read
S04|Yamaha — Basic drum position|https://www.yamaha.com/en/musical_instrument_guide/drums/play/|web-instruments.txt|양손과 킥·하이햇 페달의 기본 배치|publisher_text_read
S05|Yamaha — Stick grips|https://hub.yamaha.com/music-educators/instruments/perc/a-guide-to-proper-stick-grips/|web-verified-a.txt|매치드/트래디셔널 그립의 손과 스틱 지지|publisher_text_read
S06|Yamaha — Violin position|https://www.yamaha.com/en/musical_instrument_guide/violin/play/|web-instruments.txt|턱·어깨 지지, 오른손 활, 왼손 운지, 무프렛 지판|publisher_text_read
S07|Yamaha — Essential cello|https://hub.europe.yamaha.com/articles/the-essential-cello|web-instrument-extra.txt|앉은 연주자와 수직 악기·엔드핀·바닥 지지|publisher_excerpt_read
S08|Yamaha — Saxophone position|https://www.yamaha.com/en/musical_instrument_guide/saxophone/play/|web-instruments.txt|스트랩·엄지·입의 지지와 자세 변이|publisher_text_read
S09|Yamaha — Flute playing|https://www.yamaha.com/en/musical_instrument_guide/flute/play/|web-final-primary.txt|입술·취구·양손 지지와 횡방향 연주|publisher_text_read
S10|Yamaha — Electric guitar structure|https://www.yamaha.com/en/musical_instrument_guide/electric_guitar/mechanism/|web-final-primary.txt|브리지·픽업·현·케이블·앰프와 기타/베이스 부품|publisher_text_read
S11|Shure — In-ear monitors and wedges|https://www.shure.com/en-US/insights/10-reasons-why-in-ear-monitors-are-better-than-wedges|web-final-primary.txt|귀 모니터·바디팩·웨지의 다른 구조와 모니터 문맥|publisher_text_read
S12|Shure — Feedback and cupping|https://www.shure.com/en-IN/insights/how-to-control-feedback-in-a-sound-system|web-final-primary.txt|마이크 그릴 커핑과 피드백 경로; 소리 확인은 별도|publisher_text_read
S13|Shure — Recording microphone techniques|https://www.shure.com/en-US/docs/education/Microphone-Techniques-for-Recording|web-technique.txt|팝 필터·마이크·음원과 녹음 환경의 위치 관계|publisher_excerpt_read
S14|Yamaha — Smooth sound check|https://hub.yamaha.com/proaudio/livesound/seven-ways-to-ensure-a-smooth-sound-check/|web-verified-a.txt|인풋 리스트·스테이지 플롯·DI·모니터 배치와 점검|publisher_text_read
S15|Ableton — Comping|https://www.ableton.com/en/live-manual/12/comping/|web-definitions.txt|복수 테이크 레인에서 메인 레인으로 부분 선택|publisher_text_read
S16|Ableton — Live concepts|https://www.ableton.com/en/live-manual/12/live-concepts/|web-definitions.txt|오디오·MIDI·트랙·타임라인·세션과 편곡 화면의 구분|publisher_text_read
S17|Ableton — Stems|https://help.ableton.com/hc/en-us/articles/360000843404-Importing-and-exporting-stems|web-definitions.txt|그룹 렌더와 개별 파트 출력의 용례 차이|publisher_text_read
S18|Pioneer DJ — Instruction manual|https://assets.pioneerdjhub.com/DRI1936B_EN.pdf|web-search-2.txt|인쇄 p.108: CUE/MASTER 모니터 밸런스와 헤드폰 조작|publisher_excerpt_read
S19|Jazz in America — Elements glossary|https://jazzinamerica.org/StudentHandout/11/2|web-search-3.txt|재즈 컴핑·코러스·즉흥·편곡·앙부슈어 정의|publisher_excerpt_read
S20|Berklee — Conductor|https://www.berklee.edu/careers/roles/conductor|web-stage.txt|지휘·해석·리허설·음악감독 직무의 관계|publisher_excerpt_read
S21|Berklee — Concertmaster|https://www.berklee.edu/careers/roles/concertmasterconcertmistress|web-stage.txt|제1바이올린 수석·보잉·조율·지휘자 연결 직무|publisher_excerpt_read
S22|Berklee — Bandleader|https://www.berklee.edu/careers/roles/band-leader|web-verified-c.txt|밴드리더의 연주·리허설·조직 운영|publisher_text_read
S23|Berklee — Tour manager|https://www.berklee.edu/careers/roles/tour-manager|web-verified-c.txt|데이 시트·여행·숙박·재정·일정 조율|publisher_text_read
S24|NYU — Elena Humphreys Riot Grrrl Collection|https://findingaids.library.nyu.edu/fales/mss_394/|web-final-primary.txt|1990년대 뉴욕 운동의 진·포스터·전단·활동 기록|publisher_text_read
S25|NGV — Bondage trousers|https://www.ngv.vic.gov.au/explore/collection/work/67628/|web-final-primary.txt|펑크 복식과 페티시 씬·가죽·라텍스의 역사적 연결|publisher_text_read
S26|Museum at FIT — Gothic: Dark Glamour|https://www.fitnyc.edu/museum/exhibitions/gothic-dark-glamour.php|web-culture.txt|고스 하위문화·고급복식·공포·에로틱한 미학의 연결|publisher_text_read
S27|V&A — Theatre and Performance Archives|https://www.vam.ac.uk/info/theatre-performance-archives|web-verified-b.txt|공연복·악기·소품·스케치·가사·사진 아카이브|publisher_text_read
S28|The Met — Camp exhibition galleries|https://www.metmuseum.org/exhibitions/listings/2019/camp-notes-on-fashion/exhibition-galleries|web-verified-b.txt|캠프의 인공성·연극성·과장·패러디와 복식|publisher_text_read
S29|Musicians' Union — Appropriate behaviour|https://musiciansunion.org.uk/legal-money/rights-at-work/equality-rights/sexual-harassment-at-work/appropriate-behaviour-at-work|web-roles.txt|음악 노동의 업무 관계·권력차·압박·성희롱 문맥|publisher_excerpt_read
S30|HSE — Crowd safety hazards|https://www.hse.gov.uk/event-safety/crowd-management-assess.htm|web-verified-b.txt|군중 이동·압박·고정 구조물·출입 동선 위험의 구별|publisher_text_read
S31|US Copyright Office — Musicians|https://www.copyright.gov/engage/musicians/|web-verified-b.txt|미국 자료에서 곡/가사와 특정 녹음물의 구분|publisher_text_read
S32|Girls Band Cry — Official story|https://girls-band-cry.com/story/|web-works.txt|밴드 결성·생계·갈등·대반·티켓·프로 계약의 서사|publisher_text_read
S33|BLUE GIANT — Official story|https://bluegiant-movie.jp/story.html|web-works.txt|색소폰·피아노·드럼 트리오 JASS의 구체 편성|publisher_text_read
S34|Sony Pictures Classics — Whiplash|https://www.sonyclassics.com/film/whiplash/|web-works.txt|음대 드러머·교육자의 폭압·완벽주의 서사|publisher_text_read
S35|BFI — Concert films|https://www.bfi.org.uk/lists/10-great-concert-films|web-verified-b.txt|공연 기록 영화의 사례; 쇼와 실제 폭력의 다른 맥락|publisher_text_read
S36|TBS — K-ON!! story|https://www.tbs.co.jp/anime/k-on/k-on_tv/story/story.html|web-verified-c.txt|학교 경음부·초보자·신입·축제와 일상의 결합|publisher_text_read
S37|Aniplex — Bocchi story|https://www.aniplex.co.jp/lineup/bocchi/story/|web-verified-c.txt|서포트 기타·라이브하우스·작사·노르마의 서사|publisher_text_read
S38|Shueisha Cookie — NANA|https://cookie.shueisha.co.jp/story/25.html|web-verified-c.txt|프로 가수 지망·재결성·동거와 밴드 관계|publisher_text_read
S39|Kodansha archive — BECK|https://archive.kodansha.us/series/beck/index.html|web-last.txt|음악을 시작한 계기·만남·록 밴드 성장|publisher_excerpt_read
S40|GKIDS — Linda Linda Linda|https://gkids.com/films/linda-linda-linda/|web-gaps.txt|보컬 결원·새 보컬·3일간 세 곡 준비의 서사|publisher_excerpt_read_open_timeout
S41|V&A — Lolita street style|https://www.vam.ac.uk/articles/lolita-fashion-japanese-street-style|web-verified-b.txt|비주얼계와 복식·헤어·역사적 참조의 연결|publisher_text_read
S42|Rosco — Image Spot|https://us.rosco.com/en/product/image-spot|web-gaps.txt|고보 카세트·광학 투사 장비 문맥|publisher_excerpt_read
S43|Rosco — Fog FAQs|https://us.rosco.com/en/rosco-fog-faqs|web-last.txt|헤이즈가 빛 경로를 보이게 하는 문맥|publisher_excerpt_read
S44|BFI — This Is Spinal Tap|https://www.bfi.org.uk/film/19ffddd8-c421-5da6-b33d-7f923ec1467c/this-is-spinal-tap-a-rockumentary-by-martin-di-bergi|web-gaps.txt|가상 밴드의 투어를 다큐 형식으로 연출하는 모큐멘터리|publisher_excerpt_read
S45|Fender — Power chord|https://www.fender.com//articles/chords/what-is-a-power-chord|web-technical-detail.txt|근음·5도·옥타브 중복과 파워 코드|publisher_text_read
S46|Fender — Guitar beginner FAQs|https://www.fender.com//articles/setup/for-those-about-to-rock-10-beginner-faqs|web-technical-detail.txt|표준 튜닝·현 순서와 검지 바레의 설명|publisher_text_read
S47|Yamaha — Drumming techniques|https://www.yamaha.com/en/musical_instrument_guide/drums/play/play003.html|web-technical-detail.txt|오픈·클로즈드·림 전용 등 rimshot 용례와 접점 차이|publisher_text_read
S48|Yamaha — Piano posture|https://www.yamaha.com/en/musical_instrument_guide/piano/play/play002.html|web-technical-detail.txt|벤치·건반·양손·손목/팔꿈치 높이와 바닥 지지|publisher_text_read
S49|Yamaha — Grand and upright pedals|https://www.yamaha.com/en/musical_instrument_guide/piano/selection/|web-technical-detail.txt|오른쪽 댐퍼, 가운데·왼쪽 기능의 피아노 종류별 차이|publisher_text_read
S50|Indiana University — Violin pizzicato|https://isfee.music.indiana.edu/pizzicatoV|web-technical-closure-2.txt|오른손 검지 피치카토와 활을 내려놓는 선택|publisher_excerpt_read
S51|Yamaha — Trombone slide structure|https://www.yamaha.com/en/musical_instrument_guide/trombone/mechanism/mechanism002.html|web-technical-detail.txt|왼손 악기 지지·오른손 슬라이드 손잡이|publisher_text_read
S52|Roland — TD-07KV cross-stick|https://support.roland.com/hc/en-us/articles/360051167812-TD-07KV-Activating-and-adjusting-the-snare-cross-stick-sensitivity|web-technique-final.txt|특정 전자패드는 rim-to-rim과 헤드 접촉에 따른 트리거 차이가 있음|publisher_excerpt_read
'''
sources=[]
for line in SOURCE_ROWS.strip().splitlines():
    sid,title,url,evidence,scope,status=line.split('|')
    sources.append(dict(id=sid,title=title,url=url,evidence_file=evidence,verified_scope_ko=scope,access_status=status,access_date='2026-10-25',timezone='Asia/Seoul',visual_specimen_reviewed=False,limits_ko='이 출처의 제한된 정의·문맥만 근거로 사용한다. 아래 창작 장면 전체, 특정 표본의 픽셀·치수·소재·배선 작동·보편적 외형을 입증하지 않는다.'))
write('sources.json',sources)

# Each scene has three authored, positive, directly inspectable gates.
# ID | title | sources | Korean proposition | English proposition | gates | boundary
SCENES = '''
A01|기타의 두 손과 스트랩|S10,S02|기타리스트의 왼손은 넥의 현을 누르고 오른손의 피크는 몸체 위 현에 닿으며, 스트랩은 어깨에서 기타 몸체 양끝으로 이어진다.|A guitarist presses the neck strings with the left hand and touches a pick to the strings over the body with the right hand; a strap runs over the shoulder to the two body attachment points.|왼손-넥의 현;오른손 피크-몸체 위 현;어깨-스트랩-양끝|오른손잡이 한 실현이며 왼손잡이 연주를 오류로 간주하지 않는다.
A02|앉은 어쿠스틱 지지|S10|앉은 연주자의 허벅지 위에 어쿠스틱 기타의 잘록한 몸체가 놓이고 왼손은 넥을 감싸며 오른손은 사운드홀 앞 현에 닿는다.|A seated player supports an acoustic guitar's waist on one thigh, holds the neck with the left hand, and touches the strings in front of the soundhole with the right hand.|허벅지-몸체 지지;왼손-넥;오른손-사운드홀 앞 현|클래식 발받침·오른다리 지지·왼손잡이는 별도 실현으로 둔다.
A03|기타 보컬의 세 접점|S10,S13|기타 보컬이 양손을 각각 기타 넥과 몸체의 현에 둔 채 입을 별도 스탠드 마이크 쪽으로 향한다.|A guitar vocalist keeps one hand on the neck strings and the other on the strings over the body while facing a separate stand microphone with the mouth.|양손의 서로 다른 연주 위치;입-마이크 방향;기타와 별도 마이크|기타를 들고 서 있다는 것만으로 동시 연주·가창의 실제 소리는 입증되지 않는다.
A04|파워 코드 운지 초안|S02,S10|한 기타 넥의 인접한 두 현을 검지와 약지가 서로 다른 프렛에서 누르고 다른 손의 피크가 같은 악기의 현에 놓인다.|An index finger and ring finger press two adjacent strings at different frets on one guitar neck while the other hand's pick rests on the same instrument's strings.|두 현;서로 다른 프렛;반대손 피크와 같은 악기|근음·완전5도는 튜닝과 정확한 위치를 함께 확인해야 한다. 임의의 두 손가락 사진을 파워 코드로 확정하지 않는다.
A05|바레의 가로지르는 검지|S02,S10|기타리스트의 검지가 지판의 같은 프렛 여러 현을 가로질러 누르고 다른 운지 손가락은 그보다 몸체 쪽 프렛에 놓인다.|A guitarist's index finger presses across several strings at one fret while the other fretting fingers occupy frets nearer the body.|검지의 횡방향;같은 프렛 여러 현;다른 손가락의 구분|잡는 외형을 다루며 정확한 코드명·모든 현의 발음은 별도 확인한다.
A06|팜 뮤트 접점|S01|피킹 손의 손날이 기타 브리지 바로 옆 현 위에 닿고 같은 손의 피크 끝이 그 앞쪽 현을 향한다.|The edge of the picking hand rests on the strings beside the guitar bridge, with the pick tip aimed at the strings just in front of it.|브리지 위치;손날-현 접촉;같은 손 피크|운지 손의 뮤트·완전 소음·음색 정도와 구별한다.
A07|벤딩의 옆으로 밀린 현|S02|기타 넥의 한 현이 운지 손가락 아래에서 이웃 현 쪽으로 휘고, 같은 프렛 주변의 다른 현들은 곧게 남는다.|One guitar string bends sideways toward a neighboring string beneath a fretting finger while the surrounding strings near that fret remain straight.|눌린 한 현;옆으로 휜 국소 구간;곧은 이웃 현|정지 사진은 벤딩의 음정과 비브라토의 반복을 입증하지 않는다.
A08|양손 태핑의 넥 공유|S02|기타리스트의 양손 손가락이 같은 지판의 서로 다른 프렛에서 현에 닿고 몸체 위 피킹 영역은 비어 있다.|Both hands touch strings at different frets on the same guitar fingerboard, leaving the picking area over the body clear.|양손-같은 지판;서로 다른 프렛;몸체 위 빈 피킹 영역|손 두 개가 넥을 잡은 것과 실제 음 발생·연속 태핑은 별도다.
A09|어쿠스틱 핑거스타일|S10,S02|어쿠스틱 연주자의 오른손 엄지는 굵은 현에, 검지와 중지는 그 아래 서로 다른 현에 닿고 왼손은 넥의 현을 누른다.|An acoustic player's right thumb touches a thick string, the index and middle fingers touch separate thinner strings below it, and the left hand frets the neck.|엄지-굵은 현;검지·중지-별도 현;왼손 운지|스트로밍의 순간과 아르페지오의 시간 순서를 이 한 프레임으로 확정하지 않는다.
A10|낮게 멘 기타의 몸체 높이|S10|긴 어깨 스트랩에 매달린 기타 몸체가 연주자의 골반 아래에 놓이며 양손은 같은 기타의 넥과 몸체 위 현에 각각 닿는다.|A long shoulder strap suspends the guitar body below the player's pelvis, while the two hands touch the neck and body strings of that same guitar.|골반보다 낮은 몸체;어깨 스트랩;양손-같은 기타|낮은 악기 높이가 록 장르·연주 실력·인물 성격을 결정하지 않는다.
A11|베이스 두 손가락 연주|S03|베이시스트의 오른손 검지와 중지가 픽업 위 굵은 현에 번갈아 닿을 위치로 나뉘고 왼손은 같은 베이스 넥을 운지한다.|A bassist separates the right index and middle fingers over the thick strings above the pickup while the left hand frets the same bass neck.|굵은 현과 픽업;검지·중지 분리;왼손-같은 베이스|교대 순서·그루브·피크 연주의 열등함을 사진에서 추론하지 않는다.
A12|슬랩의 엄지 접점|S03|베이시스트의 오른손 엄지 옆면이 지판 끝 가까운 굵은 현에 닿고 다른 손가락들은 그 현에서 떨어져 있다.|The side of a bassist's right thumb touches a thick string near the end of the fingerboard while the other fingers remain clear of that string.|엄지 옆면;지판 끝 근처 현;다른 손가락과 분리|엄지 타격의 속도와 타격음은 시간·음향 확인이 필요하다.
A13|팝의 당겨진 현|S03|베이시스트의 구부린 검지가 가는 현 아래로 걸려 그 현을 몸체 바깥쪽으로 들어 올리고 엄지는 그 현과 떨어져 있다.|A bassist hooks a bent index finger under a thin string and lifts it away from the body while the thumb stays clear of that string.|현 아래 검지;몸체에서 들린 현;엄지 분리|슬랩 엄지와 팝 검지를 같은 접점으로 합치지 않는다.
A14|4현 베이스와 6현 기타 비교|S03,S10|나란한 스탠드 위 두 악기 중 한 악기는 굵은 현 네 개와 네 페그, 다른 악기는 가는 현 여섯 개와 여섯 페그를 갖는다.|On adjacent stands, one instrument has four thick strings and four tuning pegs, while the other has six thinner strings and six tuning pegs.|각각 별도 악기;4현·4페그;6현·6페그|이 선택안의 수만 고정한다. 5·6현 베이스와 다현 기타를 배제하는 정의가 아니다.
A15|드럼 크로스핸드|S04|앉은 드러머의 오른손 스틱이 왼팔 위를 가로질러 왼쪽 하이햇에 닿고 왼손 스틱은 중앙 스네어를 향한다.|A seated drummer crosses the right-hand stick above the left arm to touch the left-side hi-hat while the left-hand stick points toward the central snare.|오른손 스틱-왼쪽 하이햇;팔 교차;왼손 스틱-스네어|오른손잡이 한 배치이며 모든 드러머의 의무 자세가 아니다.
A16|드럼 오픈핸드|S04|앉은 드러머의 왼손 스틱은 왼쪽 하이햇에, 오른손 스틱은 중앙 스네어에 닿고 두 팔은 서로 교차하지 않는다.|A seated drummer touches the left hi-hat with the left-hand stick and the central snare with the right-hand stick, keeping the arms uncrossed.|왼손-하이햇;오른손-스네어;팔 분리|크로스핸드와 같은 순간의 두 대안으로 합치지 않는다.
A17|매치드 그립의 대칭|S05|두 손이 각자 스틱을 위에서 감싸 쥐고 각 엄지와 검지가 자기 스틱의 지지점을 이룬다.|Both hands wrap over their own drumsticks, each thumb and index finger forming the support point for its stick.|각 손의 별도 스틱;양손 위쪽 그립;엄지·검지 지지|양손의 정확한 각도는 변할 수 있다. 특정 장르만의 그립으로 고정하지 않는다.
A18|트래디셔널 그립의 비대칭|S05|오른손은 스틱을 위에서 감싸고 왼손 스틱은 엄지와 검지 사이에서 손바닥 위를 지나 약지 쪽에 지지된다.|The right hand wraps over its stick while the left stick passes through the thumb-index web above the palm and rests toward the ring finger.|오른손 위 그립;왼손 엄지·검지 사이;왼손 스틱의 아래 지지|왼손을 뒤집은 매치드 그립으로 단순화하지 않는다.
A19|림샷의 두 접점|S04,S05|스네어 위 한 스틱의 끝은 드럼 헤드에, 같은 스틱의 몸통은 테두리에 동시에 닿는다.|The tip of one stick touches the snare head while the shaft of that same stick simultaneously touches the rim.|같은 스틱;끝-헤드;몸통-림|림샷 상세 표본 검토 전 보류. 크로스스틱과 별도다.
A20|크로스스틱의 가로 놓인 스틱|S04,S05|스네어 헤드 위를 가로지른 스틱의 한쪽 끝이 손 아래 헤드에 고정되고 반대쪽 몸통은 림 위에 놓인다.|A stick lies across the snare head with one end held against the head beneath the hand and the opposite shaft resting on the rim.|헤드 위 가로 스틱;손 아래 고정 끝;반대쪽 림 접점|림샷의 공중 타격 구도와 다르며 전용 교습 표본을 추가 검토한다.
A21|킥과 하이햇의 두 발|S04|드러머의 오른발은 킥 페달에, 왼발은 하이햇 페달에 놓이고 각 페달의 링크는 서로 다른 악기로 이어진다.|A drummer's right foot rests on the kick pedal and the left foot on the hi-hat pedal, each linkage reaching its own instrument.|각각 별도 발;킥 페달-킥;하이햇 페달-하이햇|발이 앉는 위치와 실제 킥·하이햇 소리는 다른 증거다.
A22|피아노의 두 손과 건반|S16|피아니스트의 양손이 하나의 건반 위 서로 다른 음역에 놓이고 손가락 끝 아래 흰 건반과 검은 건반이 구분된다.|A pianist places both hands in different registers of one keyboard, with distinct white and black keys beneath the fingertips.|같은 건반;두 음역;손끝과 개별 키|연주 곡·난도·화음·프로 신분은 보이지 않는다.
A23|피아노 발과 페달|S16|앉은 피아니스트의 오른발 앞부분이 피아노 오른쪽 페달에 닿고 뒤꿈치는 바닥에 놓이며 양손은 건반 위에 남는다.|A seated pianist touches the rightmost piano pedal with the front of the right foot, keeps the heel on the floor, and leaves both hands on the keys.|오른발 앞-오른쪽 페달;뒤꿈치-바닥;양손-건반|피아노 전용 교육 출처 보강 전 구조 초안. 실제 서스테인 지속은 확인하지 않았다.
A24|바이올린 보잉의 지지|S06|바이올린이 연주자의 턱과 왼어깨 사이에 놓이고 왼손은 넥을 운지하며 오른손 활털은 브리지와 지판 끝 사이 현을 가로지른다.|A violin rests between the player's chin and left shoulder, the left hand fingers its neck, and the right-hand bow hair crosses the strings between bridge and fingerboard end.|턱·왼어깨 지지;왼손-넥;오른손 활털-현|표준 한 배치다. 활의 속도·연주 정확도는 사진만으로 보장하지 않는다.
A25|바이올린 피치카토|S06|턱과 어깨에 지지된 바이올린의 현 하나를 오른손 검지가 걸어 당기며 활은 별도 스탠드에 놓인다.|The right index finger plucks one string of a violin supported by chin and shoulder, while the bow rests on a separate stand.|턱·어깨-악기;검지-한 현;별도 스탠드의 활|활을 든 채 뜯는 방식·왼손 피치카토도 별도 대안으로 남긴다.
A26|첼로의 몸체·활·엔드핀|S07|앉은 첼리스트의 무릎 사이 첼로가 엔드핀으로 바닥에 지지되고 왼손은 넥을 운지하며 오른손 활털은 현을 가로지른다.|A cello sits between a seated cellist's knees with its endpin supported on the floor, the left hand fingers the neck, and right-hand bow hair crosses the strings.|무릎 사이 몸체;엔드핀-바닥;왼손 운지와 오른손 활털|기존 자세·동작·접촉 후보들의 의미를 합치면 새 전체 명제이므로 별도 심사가 필요하다.
A27|플루트의 취구와 횡방향|S09|플루티스트의 아랫입술 아래에 취구판이 놓이고 관은 오른쪽으로 뻗으며 두 손은 관의 서로 다른 키 묶음을 잡는다.|A flutist places the lip plate below the lower lip, extends the tube to the right, and places the hands on different key groups.|아랫입술-취구판;횡방향 관;별도 키 묶음의 양손|리드 마우스피스를 물고 있는 색소폰 자세로 대체하지 않는다.
A28|색소폰의 스트랩·입·키|S08|색소폰 스트랩이 연주자의 목에서 악기 걸이에 이어지고 마우스피스가 입에 닿으며 양손은 같은 악기의 위아래 키에 놓인다.|A saxophone strap runs from the player's neck to the instrument hook, the mouthpiece meets the mouth, and both hands rest on upper and lower keys of the same instrument.|목-스트랩-걸이;입-마우스피스;양손-같은 악기|모든 색소폰을 같은 크기·벨 방향으로 고정하지 않는다.
A29|트롬본 슬라이드의 별도 손|S19|트롬본 연주자의 입에 마우스피스가 닿고 왼손은 몸체 지지부를, 오른손은 앞으로 뻗은 슬라이드 손잡이를 잡는다.|A trombonist meets the mouthpiece with the mouth, holds the body brace with the left hand, and grips the extended slide handle with the right hand.|입-마우스피스;왼손-몸체;오른손-슬라이드|글리산도는 움직임과 소리다. 트롬본 전용 제작자 표본을 후속 확인한다.
A30|DJ 헤드폰 큐잉|S18|DJ가 한쪽 헤드폰 컵을 귀에 대고 다른 손 검지를 믹서의 CUE 버튼에 놓으며 두 데크는 믹서 양옆에 있다.|A DJ holds one headphone cup to an ear, places the other index finger on the mixer's CUE button, and has a deck on each side of the mixer.|귀-한 컵;다른 손-CUE;중앙 믹서와 두 데크|큐 신호 청취·비트매칭 성공은 화면만으로 증명되지 않는다.
A31|MIDI 컨트롤러의 연결|S16|연주자의 손가락이 MIDI 컨트롤러 건반에 닿고 데이터 케이블은 같은 컨트롤러에서 컴퓨터로 이어지며 화면에는 노트 직사각형들이 있다.|A player's fingers touch MIDI controller keys, a data cable runs from that controller to a computer, and the screen contains rectangular note blocks.|손끝-컨트롤러;컨트롤러-컴퓨터 케이블;화면의 노트 블록|케이블이 오디오 파형이나 외부 스피커로 바로 바뀌지 않는다. 소리 생성은 별도다.
A32|합창의 악보와 지휘 시선|S20|합창자 여섯 명이 두 줄에 세 명씩 서서 각자 악보철을 들고 앞쪽 지휘자의 손을 바라본다.|Six choristers stand in two rows of three, each holding a score folder and watching the conductor's hands in front.|6명·2줄·각3명;각자의 악보철;앞 지휘자-시선|이 선택안의 인원수이며 모든 합창 편성의 정의가 아니다. 화음·무반주는 비가시다.
B01|팝 필터의 사이 위치|S13|가수의 입과 스탠드 마이크 사이에 원형 팝 필터가 놓이고 필터의 집게 팔은 같은 스탠드에 이어진다.|A circular pop filter stands between a singer's mouth and a stand microphone, with its clamp arm attached to that same stand.|입-필터-마이크 순서;필터의 독립 원형;집게팔-스탠드|팝 필터는 마이크 캡슐이나 헤드폰이 아니다.
B02|컨트롤룸 유리 양쪽|S13,S16|유리창 한쪽에는 헤드폰을 쓴 가수와 마이크가, 반대쪽에는 믹서 앞 엔지니어가 있고 서로의 시선이 유리를 통과한다.|On one side of a studio window, a singer wears headphones beside a microphone; on the other, an engineer sits at a mixer, their sightline crossing the glass.|유리 양쪽 별도 사람;가수-마이크;엔지니어-믹서|유리 반사가 추가 가수를 만들지 않는다. 두 사람의 직함은 설정이다.
B03|녹음 컴핑 레인|S15|모니터의 세 테이크 레인에서 서로 다른 색의 짧은 구간들이 위쪽 단일 메인 레인에 조합되어 보이고 편집자의 손은 마우스에 놓인다.|On a monitor, short segments of different colors from three take lanes appear assembled in one main lane above, while an editor holds the mouse.|3개 테이크 레인;위쪽 단일 합성 레인;화면-편집자 분리|재즈 반주의 컴핑과 다른 뜻이다. 좋은 테이크라는 평가는 소리와 판단이 필요하다.
B04|MIDI 노트와 오디오 파형 비교|S16|한 모니터 안 두 편집 영역 중 왼쪽은 건반 눈금 옆 직사각형 노트들을, 오른쪽은 시간축 위 연속 파형을 보여 준다.|Two editor panes on one monitor show rectangular notes beside a piano-key scale on the left and a continuous waveform on a timeline on the right.|한 화면의 두 영역;노트·건반 눈금;별도 파형·시간축|MIDI 자체를 녹음된 오디오라고 정의하지 않는다.
B05|오버더빙 중인 보컬|S15,S16|헤드폰을 쓴 보컬 앞 마이크가 있고 모니터에는 기존 세 트랙 아래 별도 빨간 녹음 트랙이 놓인다.|A vocalist in headphones faces a microphone while a monitor shows a separate red recording track below three existing tracks.|헤드폰-보컬;보컬-마이크;기존3트랙과 별도 녹음행|기존 트랙이 실제로 재생되는지와 새 소리가 더해지는지는 음향·시간 증거가 필요하다.
B06|펀치 구간의 두 마커|S16|DAW 타임라인의 한 트랙에서 두 수직 마커 사이 구간만 붉게 표시되고 그 앞뒤 파형은 다른 색으로 남는다.|On one DAW track, only the section between two vertical timeline markers is red, while the waveforms before and after it remain another color.|한 트랙;두 마커;사이 구간과 앞뒤 분리|그림의 강조 구간이 실제 펀치 녹음 수행의 증거는 아니다.
B07|DI의 입력과 별도 출력|S14|베이스의 케이블이 바닥 DI 박스 한쪽에 연결되고 박스 반대쪽의 별도 케이블은 스테이지 박스 입력으로 이어진다.|A bass cable enters one side of a floor DI box, and a separate cable from the opposite side reaches a stage-box input.|베이스-입력 케이블;별도 DI 박스;출력 케이블-스테이지 박스|DI를 기타 이펙트 페달로 이름만 바꾸지 않는다. 커넥터 규격·작동은 모델별 후속 확인한다.
B08|페달보드의 연속 케이블|S10,S14|기타 출력 잭의 케이블이 페달 세 개를 짧은 패치 케이블로 차례로 거쳐 앰프 입력으로 이어진다.|A cable from the guitar output passes through three pedals joined in sequence by short patch cables and reaches the amplifier input.|기타 출력;3개 페달 사이 패치;끝-앰프 입력|선택안의 가시 연결이며 유일한 이펙트 순서·왜곡량·슈게이즈 정체성은 아니다.
B09|스템과 개별 트랙의 표시|S17|모니터 왼쪽에 별도 킥·스네어·하이햇 트랙 세 줄이 있고 오른쪽에는 이를 묶은 한 줄의 드럼 그룹 출력이 보인다.|A monitor shows separate kick, snare, and hi-hat tracks on the left and a single grouped drum output lane on the right.|3개 분리 행;하나의 그룹 출력;양쪽 화면 구분|스템·파트 용례는 유동적이다. 숫자만으로 권리나 실제 파일 내용을 추론하지 않는다.
B10|믹싱의 분리된 채널|S16|엔지니어 앞 믹서 화면에 보컬·베이스·드럼의 별도 페이더가 있고 손 하나가 베이스 채널 페이더에 닿는다.|A mixer screen before an engineer has separate vocal, bass, and drum faders, with one hand touching the bass-channel fader.|별도 채널;베이스 페이더의 손;한 엔지니어와 화면|믹스가 좋아졌다는 청감 평가는 보이지 않는다.
B11|마스터링을 위한 출력 비교|S17|모니터에는 두 완성 스테레오 파형과 각각의 출력 미터가 나란히 있고 개별 악기 트랙들은 접혀 있다.|A monitor displays two finished stereo waveforms beside their output meters while individual instrument tracks are folded away.|두 스테레오 파형;각 출력 미터;접힌 개별 트랙|이 화면은 마스터링 장면의 선택안이다. 전용 마스터링 문헌 없이 절차·음질 개선을 확정하지 않는다.
B12|토크백의 두 공간|S13,S14|컨트롤룸 엔지니어가 탁상 토크백 버튼에 손을 대고 유리 너머 헤드폰 착용 가수는 그쪽을 바라본다.|A control-room engineer touches a desk talkback button while a singer wearing headphones looks toward the engineer through the glass.|손-버튼;유리 양쪽 사람;가수 헤드폰|통신이 들렸는지와 지시 내용은 비가시다.
B13|클릭 설정과 인이어|S11,S16|컴퓨터 화면의 메트로놈 표시 옆에 작은 박 격자가 있고 드러머는 케이블이 연결된 인이어를 착용한다.|A small beat grid sits beside a metronome icon on a computer screen, and a drummer wears connected in-ear earpieces.|메트로놈 표시;박 격자;드러머-인이어|관객에게 클릭이 들리지 않는다는 것은 라우팅·음향 확인이 필요하다.
B14|루퍼의 발과 연주 손|S16|기타리스트의 양손이 같은 악기를 연주하는 위치에 남고 오른발 앞은 바닥 루퍼 페달의 스위치에 닿는다.|A guitarist keeps both hands in playing positions on the same instrument and touches a floor looper switch with the front of the right foot.|양손-기타;오른발-스위치;별도 바닥 루퍼|녹음·재생·오버더브 단계와 반복 횟수는 표시와 시간 증거가 더 필요하다.
C01|무대 배치도와 실제 자리|S14|탁자 위 평면 배치도에는 드럼·기타·보컬 위치가 표시되고 뒤쪽 실제 무대에 그 세 장비 묶음이 같은 좌우 순서로 놓인다.|A table-top stage plan marks drum, guitar, and vocal positions, and the actual stage behind it places those three equipment groups in the same left-to-right order.|탁자 위 도면;뒤 실제 무대;일치하는 순서|도면 속 아이콘은 실제 인물·악기 수에 더하지 않는다.
C02|인풋 리스트 대조|S14|스태프가 번호표가 달린 케이블 끝을 들고 다른 손으로 종이의 같은 채널 번호 행을 짚는다.|A technician holds a numbered cable end and points with the other hand to the matching channel-number row on a paper list.|케이블 끝 번호;종이 행 번호;같은 번호의 대조|텍스트가 읽혀야 번호 일치를 통과한다. 장비가 실제 작동한다는 증거는 아니다.
C03|라인체크의 한 입력|S14|스태프 한 명이 한 마이크에 입을 대는 방향을 취하고 다른 스태프는 믹서 한 채널의 켜진 미터를 가리킨다.|One technician faces a microphone with the mouth while another points to the illuminated meter of one mixer channel.|마이크 앞 사람;다른 사람-한 미터;분리된 두 역할|실제 신호 일치·점검 성공은 음향과 로그가 필요하다.
C04|빈 객석의 사운드체크|S14|빈 객석 앞 무대에서 기타리스트가 페달 노브에 몸을 굽히고 객석 쪽 믹서의 엔지니어가 무대를 바라본다.|Before empty audience rows, a guitarist bends over a pedal knob onstage while an engineer at the audience-side mixer watches the stage.|빈 객석;무대-기타리스트·페달;객석측 믹서-엔지니어|노브 조작이 특정 음색을 완성했다는 뜻은 아니다.
C05|FOH와 무대의 공간 구분|S14|객석 뒤 믹싱 콘솔 앞 엔지니어의 어깨 너머로 관객 줄과 멀리 떨어진 무대가 보인다.|Over an engineer's shoulder at a rear-of-house mixing console, audience rows lead toward a distant stage.|앞 콘솔·엔지니어;중간 객석;먼 무대|모든 FOH가 객석 맨 뒤에 있는 것은 아니다. 선택한 위치만 고정한다.
C06|웨지의 기울어진 전면|S11|무대 바닥의 쐐기형 모니터 두 대가 각자 뒤쪽 연주자를 향해 기울어진 그릴을 드러내고 관객용 스피커는 옆 기둥에 있다.|Two wedge monitors on the stage floor tilt their grilles toward performers behind them, while audience speakers stand on side supports.|바닥 웨지2대;연주자 쪽 그릴;별도 관객 스피커|웨지 신발·음식 조각과 구별한다. 모니터 믹스 내용은 보이지 않는다.
C07|인이어의 귀·케이블·팩|S11|퍼포머의 오른귀 안 이어피스에서 케이블이 귀 뒤로 돌아 허리 뒤에 집게로 고정된 작은 팩으로 이어진다.|An earpiece in a performer's right ear has a cable curving behind the ear to a small pack clipped at the back waist.|같은 사람의 귀;귀 뒤 케이블;허리 집게팩|송신기와 수신기를 외형만으로 확정하지 않는다. 기존 후보의 수신기 설정은 보존해야 한다.
C08|체인지오버의 교대 장비|S14,S23|한 스태프가 케이스를 무대 옆으로 굴리고 다른 스태프는 비워진 자리에 다음 팀의 건반 스탠드를 펼친다.|One technician rolls a case toward the stage wing while another opens the next band's keyboard stand in the vacated area.|퇴장 케이스;별도 사람-새 스탠드;같은 교대 공간|이 한 순간만으로 두 팀의 공연 순서·고용 관계를 확정하지 않는다.
C09|로드인의 손잡이와 램프|S23|스태프 두 명이 플라이트케이스 양쪽 손잡이를 잡고 밴 뒤 경사판 위 같은 케이스를 지지한다.|Two crew members hold opposite handles of one flight case and support it on a ramp behind a van.|두 사람;같은 케이스 양쪽 손잡이;밴 뒤 경사판|안전한 실제 운반 절차를 안내하는 자료가 아니다. 무게·협의는 별도다.
C10|티켓 정산의 남은 표|S37,S32|라이브하우스 탁자에 티켓 묶음과 별도 정산 종이가 있고 멤버 한 명이 남은 티켓을 세는 손동작을 취한다.|A live-house table holds a ticket bundle and a separate settlement sheet while a member makes a counting gesture over the remaining tickets.|티켓 묶음;별도 정산지;표 위 손|노르마 채무·정확한 매출·계약 조건은 종이와 설정이 필요하다.
C11|발밑 셋리스트|S14|마이크 스탠드 발 옆에 곡 제목이 줄로 적힌 종이가 네 모서리 테이프로 바닥에 고정되고 기타리스트의 신발이 그 바깥에 있다.|Beside a microphone-stand foot, a song list is taped to the floor at all four corners, with the guitarist's shoes outside the paper.|줄글 종이;네 모서리 테이프;스탠드 발·신발과 분리|정확한 곡명·공연 순서가 필요하면 실제 글자를 별도 판독한다.
C12|머치와 DIY 진 테이블|S24,S23|공연장 옆 탁자 위에 접힌 티셔츠·패치·스테이플 진이 서로 다른 더미로 놓이고 판매자가 그 뒤에 앉는다.|A venue-side table holds separate stacks of folded T-shirts, patches, and stapled zines, with a seller seated behind it.|서로 다른 상품 더미;스테이플 진;탁자 뒤 판매자|상품만으로 라이엇 그럴 운동 참여·수익·공식 판매권을 확정하지 않는다.
C13|투어 데이 시트|S23|밴 옆에 선 투어 매니저가 시간별 일정표를 들고 세 멤버는 악기 케이스를 든 채 그 종이를 바라본다.|Beside a van, a tour manager holds a timed day sheet while three members carrying instrument cases look at the paper.|밴·일정표;3명과 각 케이스;종이로 모인 시선|매니저 직함과 투어 일정은 설정·텍스트 문맥이며 외모 판정이 아니다.
C14|버스킹의 열린 케이스|S10,S23|거리 연주자가 기타와 마이크 앞에 서고 바닥의 열린 악기 케이스 안 동전은 연주자의 발과 떨어져 있다.|A street musician stands with guitar and microphone, with coins inside an open instrument case on the ground clear of the player's feet.|거리 연주자;기타·마이크;별도 열린 케이스 안 동전|버스킹 허가·생계 수입·첫 거리 공연 여부는 비가시다.
E01|밴드·투어 티셔츠의 앞뒤|S27|같은 티셔츠의 앞면에는 큰 밴드 도안이, 별도 뒤쪽 보기에는 도시 이름이 줄로 배열된다.|One view of a T-shirt shows a large band graphic on the front, while a separate rear view shows rows of city names.|앞 보기;별도 뒤 보기;도안·도시행 구분|두 보기는 명시적 비교용이다. 한 장면에서 보이지 않는 뒷면 문구를 판정하지 않는다.
E02|배틀 베스트의 패치|S25,S27|소매 없는 데님 베스트의 등에 큰 봉제 패치 하나가 있고 앞판에는 작은 직물 패치 여럿이 별도 솔기로 붙어 있다.|A sleeveless denim vest has one large sewn back patch and several smaller fabric patches attached to the front panels with separate seams.|민소매 데님;큰 등 패치;앞 작은 패치 솔기|정확한 음악·팬 정체성은 패치 문양만으로 확정하지 않는다. 전용 수집 표본 보강 대상이다.
E03|라이더 재킷의 비대칭 지퍼|S25|가죽처럼 광택 있는 짧은 재킷의 전면 지퍼가 비스듬히 올라가고 접힌 라펠과 금속 스냅이 따로 보인다.|A short leather-like jacket has a diagonal front zipper, folded lapels, and distinct metal snaps.|비스듬한 지퍼;접힌 라펠;금속 스냅|광택만으로 실제 가죽의 소재 화학을 단정하지 않는다.
E04|플란넬과 해진 데님의 층|S27|연주자가 체크 셔츠를 티셔츠 위에 열어 입고 무릎이 해진 데님 바지를 입은 채 기타 케이스에 앉아 있다.|A musician wears an open checked shirt over a T-shirt and worn-knee denim trousers while sitting on a guitar case.|셔츠-티셔츠 층;해진 무릎;케이스 지지|그런지의 선택적 복식 관습이며 장르나 계층의 필요조건이 아니다.
E05|타탄과 안전핀의 위치|S25|타탄 치마 옆 한 찢어진 천 가장자리를 큰 안전핀 하나가 통과하며 핀의 양 끝은 천에 고정된다.|One large safety pin passes through the two torn fabric edges at the side of a tartan skirt, with both pin ends fixed in the cloth.|타탄 천;두 찢어진 가장자리;핀의 양쪽 천 접점|핀의 수·위치를 보존하고 피부 피어싱으로 바꾸지 않는다.
E06|본디지 트라우저의 바지 간 끈|S25|성인 공연자의 바지 양쪽 다리 바깥 고리에 천 스트랩 하나가 연결되어 무릎 뒤쪽을 가로지르고 두 고리가 보인다.|A fabric strap joins outer loops on the two trouser legs of an adult performer, crossing behind the knees with both loops visible.|각 바짓단 고리;두 고리 사이 스트랩;무릎 뒤 경로|선택한 창작 구조다. NGV 소장품의 정확 복제품이나 실제 구속 행위로 주장하지 않는다.
E07|피시넷과 메시의 구조 비교|S26|나란한 두 소매 중 하나에는 큰 마름모 망이, 다른 하나에는 작고 촘촘한 격자 망이 있고 각 소매 끝선이 분리된다.|Of two sleeves shown side by side, one has large diamond netting and the other a fine dense mesh, with separate sleeve edges.|두 별도 소매;큰 마름모;촘촘한 격자와 끝선|패턴만으로 성적 의미·모든 망의 소재를 고정하지 않는다.
E08|코르셋의 보닝과 뒤 레이싱|S25,S26|성인 퍼포머의 허리 코르셋은 세로 보닝 선과 뒤쪽 양 고리열을 잇는 교차 끈을 드러낸다.|An adult performer's waist corset shows vertical boning lines and crossed lacing joining the two rear eyelet rows.|허리 의복;세로 보닝;뒤 두 고리열·교차끈|모든 코르셋이 같은 길이·레이싱·속옷 기능을 갖는다는 정의가 아니다.
E09|뷔스티에의 컵과 몸통|S26|성인 공연자의 끈 없는 뷔스티에는 두 가슴 컵과 허리 위 몸통 패널이 이어지고 별도 코르셋 레이싱은 보이지 않는다.|An adult performer's strapless bustier joins two bust cups to a torso panel above the waist, with no separate corset lacing visible.|두 컵;이어진 몸통 패널;끈 없는 윗선|이 선택안의 형태다. 코르셋·브라·뷔스티에의 역사적 경계는 전용 복식 자료로 추가 심사한다.
E10|하네스와 기타 스트랩 분리|S25|성인 기타리스트의 몸통 하네스 두 끈은 가슴 앞 고리에서 만나고 별도 넓은 기타 스트랩은 한쪽 어깨에서 악기로 내려간다.|Two torso-harness straps meet at a ring on an adult guitarist's chest, while a separate broad guitar strap descends from one shoulder to the instrument.|몸통 두 끈·고리;별도 넓은 악기 스트랩;각각 다른 연결 대상|몸통 하네스를 악기 지지대·동의·페티시 선호의 증거로 바꾸지 않는다.
E11|월릿 체인의 양 끝|S25|금속 체인 한쪽은 바지 벨트 고리에, 다른 끝은 뒷주머니 안 지갑 고리에 연결되어 허벅지 옆으로 처진다.|A metal chain connects a trouser belt loop to a wallet ring inside the back pocket and hangs beside the thigh.|벨트 고리;지갑 고리;두 끝 사이 처진 체인|허리 장식 벨트와 지갑 지지 체인의 끝점을 구분한다.
E12|불릿 벨트의 장식 반복|S27|성인 공연자의 허리띠에 탄약 모양 장식들이 같은 방향으로 연속 고정되고 위쪽 재킷과 아래 바지는 별도 의복으로 남는다.|An adult performer wears a belt with cartridge-shaped ornaments fixed in a repeated direction, with jacket above and trousers below remaining separate garments.|허리띠;반복 장식;별도 위아래 의복|금속 장식이 실제 탄약·사용 가능한 무기라는 뜻은 아니다. 전용 표본 확보 대상이다.
E13|라텍스·PVC의 반사 초안|S25|성인 공연자의 몸에 붙는 검은 의복 위로 연속된 밝은 반사띠가 흐르고 옆선의 지퍼와 봉제선은 따로 보인다.|Broad continuous highlights cross an adult performer's close-fitting black garment, while a side zipper and seams remain distinct.|밀착 검은 의복;연속 하이라이트;별도 지퍼·솔기|반사 외형만으로 라텍스와 PVC를 판별하지 않는다. 소재 설정·제작자 명세가 필요하다.
E14|보디수트와 캣수트의 길이|S27|비교 화면 왼쪽 성인의 보디수트는 골반에서 끝나 다리가 드러나고 오른쪽 성인의 캣수트는 같은 몸통에서 발목까지 이어진다.|In a comparison view, the left adult's bodysuit ends at the pelvis with the legs exposed, while the right adult's catsuit continues from torso to ankles.|비교용 두 사람;골반 끝선;몸통-발목 연속|의복 범주를 위한 두 대안이며 일반 장면에 인원2명을 자동 도입하지 않는다.
E15|플랫폼 부츠의 앞뒤 두께|S27|부츠 한 켤레는 발가락 아래에도 두꺼운 밑창이 있고 뒤꿈치 밑창은 그보다 높게 이어진다.|A pair of boots has thick soles beneath the toes as well as higher sole sections beneath the heels.|한 켤레;앞발 두꺼운 밑창;더 높은 뒤꿈치|플랫폼을 굽만 높은 신발과 구별한다. 공연 능력·성별을 추론하지 않는다.
E16|크리퍼스의 낮은 갑피와 솔|S25|발목 아래 낮은 구두 갑피에 끈 구멍이 있고 발 전체 아래 두꺼운 골진 솔이 같은 높이로 이어진다.|A low shoe upper ending below the ankle has lace eyelets and a thick ridged sole continuing beneath the whole foot.|발목 아래 갑피;끈 구멍;전체 발 아래 골진 솔|정확한 크리퍼스 표본 확인 전 보류. 단순 웨지·컴뱃 부츠로 대체하지 않는다.
E17|콘서트 블랙의 서로 다른 옷|S20,S27|현악 연주자 네 명이 각각 검은 셔츠·재킷·바지·긴 치마를 조합해 입고 각자의 악기와 보면대 앞에 앉는다.|Four string players combine black shirts, jackets, trousers, and a long skirt in different outfits while seated at their own instruments and stands.|4명;서로 다른 검은 복식;각자 악기·보면대|콘서트 블랙은 단일 턱시도나 동일한 성별 복장의 동의어가 아니다.
E18|테일코트의 뒤 갈라진 자락|S27|성인 연주자의 정장 상의 앞자락은 허리에서 끝나고 뒤에는 두 갈래 긴 꼬리가 내려가며 흰 셔츠 앞판이 보인다.|An adult musician's formal coat ends at the waist in front and divides into two long tails behind, with a white shirt front visible.|짧은 앞자락;두 갈래 뒤 꼬리;별도 흰 셔츠|턱시도와 테일코트를 한 이름으로 합치지 않는다.
E19|시퀸과 라인스톤 비교|S27,S28|한 소매에는 겹친 작은 납작 원판이, 다른 소매에는 돌출된 각진 투명 장식이 붙어 점광원을 서로 다르게 반사한다.|One sleeve carries overlapping small flat discs while another bears raised faceted clear ornaments, reflecting point lights differently.|서로 다른 소매;납작 원판;돌출 각진 장식|반사만으로 유리·플라스틱 재질이나 가격을 판정하지 않는다.
E20|비주얼계의 개별 페르소나|S41,S26|세 성인 밴드 멤버가 서로 다른 큰 헤어 실루엣·극적 눈화장·구조적인 무대복을 조합해 각자 악기 옆에 선다.|Three adult band members combine distinct large hair silhouettes, theatrical eye makeup, and structured stage clothes beside their own instruments.|3명;서로 다른 헤어·화장·복식;각자 악기|하나의 음향 장르·모든 멤버 동일 복식·성정체성으로 환원하지 않는다.
F01|모호크의 중앙 띠|S25|머리 중앙에 앞에서 뒤로 이어지는 세운 머리 띠가 있고 양옆 머리는 짧게 드러난다.|An upright strip of hair runs from front to back along the center of the head, with short hair visible on both sides.|중앙 앞뒤 띠;세운 모발;양옆 짧은 머리|헤어 하나로 펑크 소속·성향·성별을 확정하지 않는다.
F02|리버티 스파이크의 여러 꼭짓점|S25|머리 둘레에서 굳혀 세운 모발 다발 여러 개가 서로 떨어진 뾰족한 꼭짓점을 이룬다.|Several stiffened hair bundles project around the head as separate pointed spikes.|여러 모발 다발;각 꼭짓점;다발 사이 분리|모호크 중앙 연속 띠와 구별한다. 전용 헤어 표본을 후속 확보한다.
F03|언더컷의 위아래 길이|S41|정수리의 긴 머리 아래로 짧게 깎은 옆머리 구간이 귀 위에 드러나고 두 길이 경계가 뚜렷하다.|Below long crown hair, a closely cut side section appears above the ear with a distinct length boundary.|긴 위 머리;귀 위 짧은 구간;길이 경계|머리 길이가 음악 장르·나이·성정체성을 결정하지 않는다.
F04|티즈드 헤어의 부피|S27,S28|성인 공연자의 뿌리 부근 머리 다발이 부풀어 머리 둘레를 넓히고 끝머리는 어깨 쪽으로 따로 내려간다.|An adult performer's hair expands around the head near the roots, with separate ends falling toward the shoulders.|부푼 뿌리;넓어진 둘레;아래 끝머리|완성 외형만으로 백코밍 시술 과정을 입증하지 않는다.
F05|퐁파두르의 앞 볼륨|S27|앞머리가 이마 위에서 뒤로 높게 말려 넘어가고 옆머리는 머리 윤곽을 따라 눌려 있다.|Front hair rises above the forehead and rolls back, while the side hair lies close to the head contour.|이마 위 볼륨;뒤로 말린 방향;눌린 옆머리|전용 복식·헤어 자료 전 세부 용어 자격은 보류한다.
F06|사이드 프린지의 한쪽 눈 경계|S41|긴 앞머리가 이마를 비스듬히 가로질러 한쪽 눈썹에 내려오고 반대쪽 눈과 눈썹은 드러난다.|A long fringe crosses the forehead diagonally toward one eyebrow, leaving the opposite eye and eyebrow exposed.|비스듬한 앞머리;한쪽 눈썹 경계;반대 눈 노출|이모의 필요조건·내향성·정신 상태를 추론하지 않는다.
F07|번진 아이라인의 표면|S26|눈꺼풀 가까운 검은 화장이 눈 아래 피부에 부드러운 얼룩으로 번지고 눈가 피부의 표면은 연속된다.|Black makeup close to the eyelid smudges into a soft patch below the eye while the surrounding skin surface remains continuous.|눈꺼풀 화장;눈 아래 얼룩;연속 피부 표면|화장 번짐·눈물·폭행 흔적·공연 후 피로의 원인은 각각 별도다.
F08|콥스 페인트의 흑백 구획|S26|성인 무대 공연자의 얼굴에 흰 바탕 화장이 깔리고 검은 영역이 양 눈 주위와 입가에 경계 있는 무늬로 놓인다.|An adult stage performer's face has a white makeup base with bounded black patterns around both eyes and the mouth.|흰 화장 바탕;눈 주위 검정;입가 별도 무늬|해골 분장·실제 시신·사악한 성격·실제 종교와 동일시하지 않는다. 전용 씬 자료 필요.
G01|한 마이크 공유|S13,S35|두 보컬의 얼굴이 하나의 스탠드 마이크 양옆에서 같은 캡슐을 향하고 각자의 손은 자기 악기에 남는다.|Two vocalists face one stand-microphone capsule from opposite sides, each keeping their hands on their own instrument.|두 사람;한 캡슐과 양쪽 입;각자 악기 위 손|입술 접촉·키스·연애·두 번째 마이크를 자동 추가하지 않는다.
G02|관객 쪽 마이크|S35|퍼포머가 오른팔로 마이크를 앞 장벽 너머 관객 쪽에 내밀고 그릴은 자기 입 반대 방향을 향한다.|A performer extends a microphone in the right hand across the front barrier toward the audience, with the grille facing away from the performer's own mouth.|오른손-손잡이;장벽 너머 방향;그릴-입 반대|관객의 실제 노래 소리와 친밀감은 비가시다.
G03|등 맞댄 별도 악기|S35|두 기타리스트의 등 윗부분이 맞닿고 각자 다른 방향을 보며 자기 기타의 넥과 몸체 현에 양손을 둔다.|Two guitarists touch upper backs, face different directions, and keep both hands on the neck and body strings of their own guitars.|등-등 접촉;다른 방향;각자 기타·양손|팔·기타 넥을 상대 인물 소유로 섞지 않는다.
G04|합주 직전 눈맞춤 큐|S19,S22|기타리스트가 손을 현 위에 멈춘 채 드러머를 보고 드러머는 스틱 두 개를 든 채 시선을 되돌린다.|A guitarist pauses with hands above the strings and looks at a drummer, who returns the gaze while holding two sticks.|기타 손 위치;드러머 두 스틱;서로 향한 시선|다음 박·카운트인·실제 동시 진입은 시퀀스가 필요하다.
G05|웨지 위 한 발|S11,S35|기타리스트의 한쪽 신발 밑창이 무대 웨지 윗면에 닿고 다른 발은 바닥을 지지하며 기타는 스트랩에 매달린다.|One guitarist's shoe sole contacts the top of a stage wedge, the other foot supports the body on the floor, and the guitar hangs from a strap.|신발-웨지 접촉;다른 발-바닥;기타-스트랩|하중·실제 장비 안전성·공연자 실력을 입증하지 않는다.
G06|헤드뱅잉의 순간 외형|S35|연주자의 상체가 앞으로 기울고 긴 머리카락이 얼굴 앞 공중으로 뻗으며 양손은 자기 악기에 남는다.|A player's torso leans forward, long hair extends through the air before the face, and both hands remain on the player's instrument.|앞 기울기;공중 머리카락;양손-자기 악기|머리 움직임의 주기·목의 안전성·소리는 정지 화면에 없다.
G07|기타 윈드밀의 팔 궤적 초안|S35|기타리스트의 오른팔이 어깨 위로 크게 올라가고 왼손은 넥을 잡으며 기타 스트랩은 몸체를 지지한다.|A guitarist raises the right arm high above the shoulder while the left hand holds the neck and the strap supports the guitar body.|높은 오른팔;왼손-넥;스트랩-몸체|한 장면은 원형 회전·스트로크를 입증하지 않는다. 팔 윈드밀의 과정 후보는 별도다.
G08|윈드밀 헤드뱅잉의 머리 띠|S35|성인 연주자의 긴 머리가 머리 둘레 바깥으로 원호 모양 펼쳐지고 두 팔은 몸통 아래 자기 악기 쪽에 있다.|An adult player's long hair fans outward in an arc around the head while both arms stay below the torso toward the player's instrument.|머리 주위 원호;모발 소유자;아래쪽 별도 팔|팔 회전 윈드밀과 다른 외형이며 전체 회전은 시퀀스가 필요하다.
G09|점프의 두 발 공중|S35|기타를 멘 연주자의 두 신발이 무대 바닥에서 떨어지고 스트랩은 어깨에 남으며 양손은 같은 기타를 잡는다.|Both shoes of a player wearing a guitar clear the stage floor, the strap remains on the shoulder, and both hands hold that guitar.|두 신발-바닥 간격;어깨 스트랩;같은 기타의 두 손|착지·높이·안전성·계속 연주했는지는 비가시다.
G10|니 슬라이드의 무릎 접점|S35|연주자의 양 무릎이 무대 바닥에 닿고 상체는 뒤로 기울며 기타 몸체는 무릎 위쪽에서 스트랩에 지지된다.|A player's two knees contact the stage floor, the torso leans back, and the guitar body hangs from a strap above the knees.|두 무릎-바닥;뒤 기울기;무릎 위 기타 지지|미끄러진 경로와 동작 안전성을 한 사진으로 확정하지 않는다.
G11|덕워크의 낮은 자세|S35|기타리스트가 무릎을 깊이 굽혀 낮게 앉은 자세에서 한 발을 앞으로 뻗고 양손을 자기 기타에 둔다.|A guitarist bends the knees into a low crouch, extends one foot forward, and keeps both hands on the guitar.|깊은 무릎 굽힘;앞으로 나온 발;양손-기타|걸음의 연속·특정 음악가 모사·유래는 별도 출처가 필요하다.
G12|데빌 혼스의 손가락|S35|성인 관객의 한 손에서 검지와 새끼손가락은 펴지고 중지와 약지는 엄지 아래 접힌다.|On one adult audience member's hand, the index and little fingers extend while the middle and ring fingers fold beneath the thumb.|같은 손;검지·새끼 펴짐;중지·약지·엄지 관계|손짓만으로 실제 신앙·정치·모든 문화의 의미를 단정하지 않는다.
G13|포고의 별도 공중 인물|S30|작은 공연장 관객 둘이 서로 떨어진 채 각각 두 발을 바닥에서 띄우고 주변 사람들은 발을 바닥에 둔다.|Two audience members in a small venue each lift both feet off the floor while remaining apart, and surrounding people keep their feet grounded.|공중 인물2명;서로 사이 간격;주변 바닥 지지|반복 점프·모싱·폭행을 모두 같은 행위로 묶지 않는다.
G14|모시 피트의 공간과 방향|S30|관객들이 중앙의 작은 빈 원 둘레에서 서로 다른 방향으로 몸을 기울이고 바깥 관객은 그 공간을 둘러싼다.|Audience members lean in different directions around a small central opening, with an outer ring of spectators surrounding that space.|중앙 빈 공간;다른 방향 몸;바깥 둘레|자발성·합의·충돌 강도·군중 압박·폭행 여부는 사진만으로 판정하지 않는다.
G15|크라우드서핑의 다중 지지|S30|성인 한 명이 관객 머리 위에 수평으로 놓이고 서로 다른 사람의 손들이 등·골반·다리 아래를 나누어 지지한다.|One adult lies horizontally above audience heads while hands from different people separately support the back, pelvis, and legs.|수평 한 사람;다수 손 소유자;등·골반·다리 아래 지지|지지 손을 떠 있는 장식으로 만들지 않는다. 실제 동의·안전성을 보장하지 않는다.
G16|스테이지 다이빙의 출발 경계|S30|성인 퍼포머가 무대 가장자리 바깥 공중에 있고 아래 객석의 여러 팔이 그쪽으로 뻗으며 무대 끝선이 뒤에 남는다.|An adult performer is airborne beyond the stage edge, several audience arms reach toward the performer below, and the stage boundary remains behind.|공중 퍼포머;뒤 무대 끝;아래 뻗은 팔|도약 원인·받침 성공·착지·부상 여부는 시간 증거가 필요하다.
H01|지휘자와 각자의 악기|S20|지휘대의 한 지휘자가 봉을 들고 그 앞 네 연주자는 각자 악기를 잡은 채 지휘자의 손을 바라본다.|One conductor on a podium raises a baton while four players in front hold their own instruments and watch the conductor's hand.|지휘대1명;앞 연주자4명;손-악기 소유와 시선|기차 차장·도체·활을 든 임의 인물과 구별한다. 지휘의 음악적 효과는 비가시다.
H02|악장과 지휘자의 분리|S21,S20|제1바이올린 앞줄의 연주자가 활을 들고 다른 현악 주자들을 향해 몸을 돌리며 별도 지휘자는 지휘대에 서 있다.|A front-row first violinist turns toward the other string players with a bow raised while a separate conductor stands on the podium.|앞줄 바이올린;다른 현악 주자 방향;별도 지휘대 사람|악장 직함은 설정·프로그램·직무 증거가 필요하다. 단순 앞자리만으로 확정하지 않는다.
H03|현악 사중주의 네 악기|S06,S07|두 바이올린·비올라 한 대·첼로 한 대를 든 네 연주자가 서로 마주보는 반원에 앉고 각자 앞에 보면대가 있다.|Four players with two violins, one viola, and one cello sit in an inward-facing semicircle, each with a music stand.|4명;바이올린2·비올라1·첼로1;안쪽 반원·각 보면대|콰르텟은 일반적으로 4인이라는 뜻이다. 이 악기 편성만의 동의어가 아니다.
H04|색소폰·피아노·드럼 트리오|S33,S19|작은 클럽에 색소폰 연주자·피아니스트·드러머가 각자 악기를 두고 삼각 배치로 서로 바라본다.|A saxophonist, pianist, and drummer occupy a triangular arrangement with their own instruments in a small club, looking toward one another.|3명;서로 다른 세 악기;삼각·상호 시선|BLUE GIANT의 구체 편성을 참고한 선택안이다. 모든 재즈 트리오에 베이스가 없다는 뜻이 아니다.
H05|부원 모집과 빈 악기 자리|S36,S37|연습실 문에 모집 전단이 붙고 방 안 두 멤버는 비어 있는 건반 스탠드 쪽으로 세 번째 방문자를 안내한다.|A recruitment flyer hangs on a rehearsal-room door while two members guide a third visitor toward an empty keyboard stand.|문 전단;멤버2·방문자1;빈 건반 스탠드|전단의 실제 모집 조건·성별·연령·학적은 별도다.
H06|작은 첫 무대의 긴장|S37,S40|작은 무대 보컬의 손이 마이크 손잡이를 꽉 감싸고 뒤 두 멤버는 그를 보며 앞줄 일부 객석은 비어 있다.|On a small stage, a vocalist grips a microphone handle tightly while two members behind look toward the vocalist and some front-row seats remain empty.|앞 보컬;뒤 멤버2명 시선;일부 빈 객석|첫 공연·무대공포 진단·실패는 이 외형만으로 확정하지 않는다.
H07|편곡 의견 충돌의 악보|S22,S32|두 멤버가 같은 악보의 서로 다른 마디를 각자 손가락으로 짚고 세 번째 멤버는 접은 팔로 둘을 바라본다.|Two members point to different bars on the same score while a third watches them with folded arms.|같은 악보;다른 마디의 각 손;세 번째 사람 반응|견해차의 내용·사이 악화·공로 탈취는 시각 설정 밖의 정보다.
H08|탈퇴의 빈 자리와 케이스|S38,S32|연습실 안 세 멤버 앞에 빈 의자 하나가 있고 문가의 다른 인물은 닫힌 악기 케이스를 들고 밖을 향한다.|One empty chair stands before three members in a rehearsal room, while another person at the door carries a closed instrument case facing outward.|방 안3명;빈 의자1개;문가 별도 사람·케이스|실제 탈퇴·일시 외출·재결합 이력을 소품만으로 판정하지 않는다.
H09|재결합의 낡은 사진|S38,S27|현재 성인 네 명이 악기 앞에 서고 탁자 위 낡은 사진에는 네 연주자의 과거 무대 모습이 별도 사각 영역 안에 있다.|Four present-day adults stand before instruments, while an old photograph on a table contains a separate rectangular image of four earlier-stage players.|현재4명;탁자 위 별도 사진;사진 내부4명|사진 속·현재의 동일 신원과 시간 관계는 설정이다. 반사상·추가 실물로 세지 않는다.
H10|수리 흔적이 있는 악기|S10,S27|기타 몸체 가장자리의 벗겨진 도장 옆에 작은 보수 패치가 있고 같은 악기의 넥·브리지·현은 연속된다.|A small repair patch borders worn paint on one guitar's body edge while its neck, bridge, and strings remain continuous.|국소 마모;보수 패치;같은 악기 연속|유품·유명 연주자의 악기·정확한 연식·작동 가능성을 입증하지 않는다.
H11|생업 뒤 합주실|S23,S32|한 성인 멤버가 작업 앞치마를 벗어 의자에 걸고 다른 손으로 기타 케이스를 열며 뒤편 두 멤버는 악기를 준비한다.|One adult member hangs a removed work apron on a chair and opens a guitar case with the other hand while two members behind prepare instruments.|앞치마-의자;한 손-케이스;뒤 멤버2명|직업·소득·근로시간·꿈의 좌절은 설정과 서사가 필요하다.
H12|무대와 백스테이지의 거울|S27|성인 공연자가 거울 앞 의자에 앉고 화려한 무대 재킷은 옆 걸이에, 닦아낸 화장 자국은 탁자 위 솜에 남는다.|An adult performer sits before a mirror, a theatrical stage jacket hangs beside the chair, and removed makeup stains a cotton pad on the table.|인물과 거울;별도 재킷 걸이;솜 위 화장 자국|거울은 추가 인물이 아니다. 피로·퇴폐·행복·몰락의 감정은 외형만으로 확정되지 않는다.
H13|성인 무대의 성적 매력 연출|S25,S26|성인 퍼포머가 열린 재킷 안 뷔스티에를 드러내고 한 손은 마이크 스탠드에, 시선은 관객 쪽에 둔다.|An adult performer reveals a bustier beneath an open jacket, places one hand on a microphone stand, and looks toward the audience.|열린 재킷·안쪽 뷔스티에;손-스탠드;관객 방향 시선|성적 매력은 맥락·선택적 연출이다. 복식 하나를 욕망·동의·강요로 분류하지 않는다.
H14|성인 누드 퍼포먼스 연구 초안|S27|누드인 성인 공연자가 비어 있는 무대 중앙에 서고 손의 마이크와 뒤편 열린 커튼이 무대 맥락을 드러낸다.|A nude adult performer stands at the center of an empty stage, with a handheld microphone and an open curtain behind establishing the performance setting.|명시된 성인1명;누드 신체 상태;마이크·커튼·무대|누드 자체를 성행위로 바꾸지 않는다. 이번 출처는 공연 일반 문맥만 지원하므로 구체 표본·작품 의도는 보류다.
H15|버레스크의 장갑과 커튼|S27,S28|성인 공연자가 커튼 앞에서 한 손으로 반대쪽 긴 장갑 끝을 잡고 스팽글 의상의 장식과 발밑 스포트 원이 보인다.|An adult performer before a curtain holds the end of the opposite long glove, with sequined costume details and a circular spotlight at the feet.|한 손-반대 장갑끝;시퀸 의상;발밑 원형 빛|정확한 버레스크 전통·스트립 단계·동의는 별도 출처와 문맥이 필요하다.
H16|캠프의 과장된 실루엣|S28|성인 공연자가 지나치게 큰 깃털 어깨 장식과 반짝이는 플랫폼 부츠를 착용하고 작은 마이크 스탠드 옆에서 과장된 팔 자세를 취한다.|An adult performer wears oversized feathered shoulders and sparkling platform boots and strikes an exaggerated arm pose beside a small microphone stand.|큰 어깨 장식;플랫폼 부츠;작은 스탠드와 과장 팔|과장된 한 장면이 캠프 전체 정의·성적 지향·젠더 정체성을 증명하지 않는다.
H17|학대적 지도 장면의 거리|S34,S29|서 있는 지도자가 연주자의 악보를 손가락으로 찌르듯 가리키고 앉은 드러머는 몸을 뒤로 빼며 양 스틱을 무릎 위에 둔다.|A standing instructor points sharply at a player's score while a seated drummer leans away with both sticks resting on the knees.|서 있는 사람-악보;앉은 드러머 후퇴;양 스틱-무릎|위협적 구도는 창작 프록시다. 학대·폭행·훈련의 정당성을 사진만으로 판정하지 않는다.
H18|계약 압박 장면의 손과 출구|S29,S31|탁자 한쪽 사람이 계약서의 서명란을 짚고 반대쪽 성인 음악가는 펜을 내려놓은 채 열린 문을 바라본다.|A person on one side of a table points to a contract signature box while an adult musician opposite sets down a pen and looks toward an open door.|서명란을 짚는 손;반대 음악가·내려놓은 펜;열린 문과 시선|권력형 성적 강요·캐스팅 카우치·부당 계약·동의 여부는 이 프레임으로 증명되지 않는다.
H19|악기 파괴의 동작과 잔해 분리|S35|성인 공연자가 기타 넥을 두 손으로 들고 몸체 끝을 빈 무대 바닥에 부딪치는 순간, 별도 떨어진 조각들이 그 접점 옆에 있다.|An adult performer holds a guitar neck with both hands as the body end strikes an empty stage floor, with separate fragments beside the contact point.|두 손-같은 넥;몸체끝-바닥 접점;옆 별도 조각|계획된 쇼·분노·기물 범죄·사고는 문맥으로 구분한다. 파괴 후 정적 후보는 별도다.
H20|모조 피와 실제 상처의 구별|S35,S26|쇼크 록 무대 의상 위 붉은 액체 자국이 있고 옆 소품 탁자에 열린 무대 분장 용기가 있으며 피부 표면은 연속된다.|Red liquid stains a shock-rock stage costume, an open theatrical-makeup container sits on a prop table beside it, and the skin surface remains continuous.|의복 위 액체;별도 분장 용기;연속 피부|용기만으로 모조 피라는 물질·출처가 확정되지 않는다. 실제 부상·고어 이미지·의상 패턴은 별도 실현이다.
'''

family_names={'A':'instrument','B':'studio','C':'live_labor','E':'wardrobe','F':'hair_makeup','G':'performance_crowd','H':'ensemble_story_adult_dark'}
cards=[]
for line in SCENES.strip().splitlines():
    cid,title,sids,ko,en,gates,boundary=line.split('|')
    family=family_names[cid[0]]
    slots={'A':['action','hand_pose','contact_point','object_structure'],'B':['procedure_step','prop_placement','object_structure'],'C':['location','procedure_step','prop_placement'],'E':['garment_detail','wardrobe_layering'],'F':['hair_style','makeup_style'],'G':['body_pose','relational_action','contact_point'],'H':['relational_action','narrative_clue','composition']}[cid[0]]
    gate_list=gates.split(';')
    cards.append(dict(id=cid,name_ko=title,family=family,phrase_ko=ko,phrase_en=en,source_ids=sids.split(','),source_support='bounded_definition_or_domain_context_only_not_whole_scene_proof',authorship='original_optional_visual_proposition',observable_components=[{'id':f'{cid}.{i+1}','requirement_ko':s,'required_if_selected':True} for i,s in enumerate(gate_list)],owner_contract={'keep_all_stated_owners':True,'keep_all_stated_counts':True,'keep_directed_contact_support_and_cable_endpoints':True,'one_selected_alternative_only':True,'reflections_displays_and_photographs_are_separate_media_owners':True,'source_proposition_en':en,'source_proposition_ko':ko},confusion_boundary_ko=boundary,proposed_slots=slots,slot_status='unreviewed_proposal',seed_ids=[],runtime_importable=False,native_approval=False,automatic_hard_activation=False,qualification='research_draft_only',visual_specimen_verified=False,pixel_gate='Every selected component and both relation endpoints must be jointly visible. Partial or occluded required evidence cannot pass. Sound, temporal history, identity, consent, diagnosis and material chemistry require separate evidence.'))
assert len(cards)==124, len(cards)
technical_sources={'A04':['S45','S46'],'A05':['S46'],'A19':['S47'],'A20':['S47','S52'],'A22':['S48'],'A23':['S48','S49'],'A25':['S06','S50'],'A29':['S51']}
for c in cards:
    if c['id'] in technical_sources:c['source_ids']=technical_sources[c['id']]
    if c['id']=='A19':
        c['name_ko']='오픈 림샷의 두 접점'
        c['confusion_boundary_ko']='오픈 림샷의 선택안이다. Yamaha 자료의 rimshot은 림 전용·클로즈드 등도 포괄하므로 림샷이라는 말만으로 헤드/림 동시 접촉을 의무화하지 않는다.'
    if c['id']=='A20':
        c['phrase_ko']=c['phrase_ko'].replace('스네어 헤드','어쿠스틱 스네어 헤드',1)
        c['phrase_en']=c['phrase_en'].replace('snare head','acoustic snare head',1)
        c['owner_contract']['source_proposition_ko']=c['phrase_ko'];c['owner_contract']['source_proposition_en']=c['phrase_en']
        c['confusion_boundary_ko']='어쿠스틱 스네어 한 실현이다. TD-07KV 등 일부 전자패드는 rim-to-rim 및 헤드 접촉 조건이 다르므로 이 자세를 전자패드로 자동 이전하지 않는다.'
    if c['id']=='A23':c['confusion_boundary_ko']='오른쪽 댐퍼 페달의 기능은 확인했다. 발의 접점은 이 선택안이며 실제 서스테인·페달 순서·연주 성공은 비가시다. 가운데/왼쪽 기능은 그랜드와 업라이트가 다르다.'
    if c['id']=='A29':c['confusion_boundary_ko']='왼손 지지와 오른손 슬라이드 구조는 확인했다. 글리산도의 연속 음정·슬라이드 움직임은 소리·시간 증거가 필요하다.'

# Explicit row dispositions. A route is one possible component, never a definition/equivalence.
# Table index -> semicolon-separated list, one entry per original row. '-' retains context only.
ROUTES={
0:'-;-;H05;H11;C13;H01;H01;H04;A32;A02;A30;-;-;-;-;-;-;-;-',
1:'A03;G02;G04;A03;A07;A01;A11;A15;A22;G01;G04;A28;H03;A14;H05;A31',
2:'B05;H06;H07;H07;B10;C01;H01;H02;-;C13;C10;C12;C13;C09',
3:'-;-;-;-;-;B13;-;G04;-;A15;-;-;-;-;-;-',
4:'-;-;-;-;-;-;-;-;-;-;-;A07;H07;-',
5:'G04;G04;H04;H04;A22;-;G02;G04',
6:'A01;A01;A04;A05;A06;A07;A07;A08;A08;A09;A12,A13;A15;A15;A19;A17;A18;A25,A26;A24;A29;A28',
7:'A03;A03;A03;A03;-;-;-;H04;A03;B01',
8:'B05;B04;A31;B05;B05;B06;B03;B09;B09;B10;B11;-;B10;B10;B08;B08;-;B14;B04;B05;B13;-;B07;-',
9:'C04;C10;C14;H06;H06;H04;H04;E20;C08;C05;C04;C08;C10;C11;C04;G02;G02;C13',
10:'C04;C03;C05;C05;C06;C07;B08;C01;C02;B12;C08;C09;C01',
11:'-;C12;C12;-;-;-;-;-;-;-;C12;C12;-;-;C11;C13;-;-',
12:'C04;A10;E02;E05;G14;H05;F06;E17;E08;E19;F04;E04;B08;E20;H20;C12',
13:'A07;H04;H04;A12,A13;A03;A02;F05;A31;A03;H03',
14:'A01;A10;A11;G05;A02;A07;A08;A11;A12,A13;A15;A16;A22,A23;A24;A26;A28;A27;A30',
15:'H13;G01;G02;G03;G04;G05;G06;G07;G08;G11;G09;G10;G10;G12;G13;G14;G15;G16;H19;A03',
16:'E01;E01;E03;E02;E04;E04;E05;E01;H13;E06;E07;E08;E09;E10;E10;E05;E11;E12;E13;E14;E15;E15;E16;E17;E19;E20;E17;E18;E20',
17:'F01;F02;F03;F04;F06;F05;F06;F07;F07;E19;F08;E20;E20;H12',
18:'A14;A02;A01;A01;A14;A05;A14;A06;A09;B08;B08;A21;A15;A31;C09;B01;H07;H10',
19:'C04;B02;B01;H12;C12;H16;G06;E19;A07;G05;H01;C04;H12;-;-',
20:'H05;H07;H07;G04;H06;H06;H06;H07;G04;H07;C08;G01;H08,H09;H11;C12;B05;H09;H10;H06;H08',
21:'H12;H12;H13;E06,E10;E08,E09;H14;H15;H16;E20;-;G02;H13',
22:'H17;H18;H18;H18;-;-;H12;-;H07;H19;G14;G14;H20;F08;-',
23:'H05;H06;H11;H05;H09;H04;H06;H17;H16',
24:'B08;H11;H12;H04;E20;H09;H20'
}
CONTEXT_BY_TABLE={0:'N01',1:'N02',2:'N02',3:'N03',4:'N04',5:'N05',6:'N06',7:'N07',8:'N08',9:'N09',10:'N10',11:'N11',12:'N12',13:'N12',14:'N06',15:'N13',16:'N14',17:'N14',18:'N15',19:'N16',20:'N17',21:'N18',22:'N19',23:'N20',24:'N20'}
CONTEXT_ROWS='''
N01|작품·매체 분류|음악 드라마·뮤지컬·전기·콘서트 필름·로큐멘터리·모큐멘터리는 서사 방식과 기록/허구 계약을 따로 요구한다. 악기를 든 인물만으로 구별되지 않는다.|S35,S44
N02|인물 직무와 편성|프런트퍼슨은 공식 리더와 다를 수 있고 지휘자·악장·MD·프로듀서·A&R·매니저·프로모터·에이전트는 서로 다른 역할이다. 듀오/트리오/콰르텟은 인원만 뜻하며 걸즈 밴드는 장르·성년 여부를 정하지 않는다.|S20,S21,S22,S23
N03|소리의 구조와 시간|선율·화성·키·전조·박자·템포·그루브·싱코페이션·백비트·다이내믹스·음색·텍스처·프레이징·유니즌은 듣기·악보·시간 문맥이 필요하다. 소품을 보인 사실이 청감 특성을 증명하지 않는다.|S16,S19
N04|곡 구간의 중의어|리프·리크·훅·후렴·브리지·브레이크·브레이크다운·빌드업/드롭·리프라이즈는 곡 구조·시간 문맥이다. chorus는 재즈의 전체 코러스·합창·후렴·효과를 문맥별로 분리한다. bridge는 악기 부품과 별개다.|S19,S10
N05|합주 상호작용|큐의 눈맞춤은 가시적이지만 카운트인·콜앤리스폰스·즉흥·컴핑·그루브의 성립은 소리와 시간 증거를 요구한다. 재즈 컴핑과 녹음 편집 컴핑은 별도 sense다.|S19,S15
N06|연주 기술과 정지 프록시|동작명 전체와 한 순간 손·현·활·키·페달 접촉을 분리한다. 음정·발음·교대·반복·숙련도·정확한 코드·튜닝은 구조만으로 입증하지 않는다. 좌우는 선택 실현에만 잠근다.|S01,S02,S03,S04,S06,S08,S09
N07|가창 소리와 얼굴|클린/허시·스크리밍·그로울링·팔세토·벨팅·스캣·멜리스마·랩 플로·브레스는 음향·연속 행위가 필요하다. 벌린 입이나 힘준 목은 기술·건강·음역의 판정 근거가 아니다.|S13,S19
N08|제작·신호·음향|MIDI 정보와 오디오·스템과 개별 트랙·믹싱과 마스터링·샘플링과 새 연주를 구별한다. 컴프레서·EQ·잔향·딜레이·왜곡·피치 보정·립싱크/핸드싱크·백킹·클릭은 화면이나 장비만으로 수행·효과를 증명하지 않는다.|S15,S16,S17,S12
N09|공연 형식과 일본 현장어|원맨 라이브는 한 팀 중심이며 반드시 한 명이 아니다. 대반은 복수 팀 공연 문맥, 노르마는 계약별 조건이다. 인디·커버·카피·트리뷰트·헤드라이너·앙코르는 외형만으로 확정되지 않는다.|S37,S32,S35
N10|무대 운영의 단계|라인체크의 입력 확인과 사운드체크의 전체 균형 점검, PA와 모니터, FOH와 백라인, 배치도와 인풋 리스트, 토크백과 가창 마이크, 반입·교대·반출을 분리한다.|S14,S11,S23
N11|산업·권리·팬 관계|노래 자체와 특정 녹음물의 권리는 별개라는 미국 자료의 설명을 개념 구분에만 쓴다. 레이블·크레디트·선급금/회수·로열티·부틀렉·퍼블리싱·셀아웃·원 히트 원더의 사실·법적 판단은 문서·시점·관할이 필요하다.|S31,S24,S23
N12|장르·운동·복식 비동치|Punk와 Funk의 한국어 펑크를 분리한다. 이모 패션·고스 문화·고딕 록·글램·비주얼계·라이엇 그럴·슈게이즈는 서로 다른 음악·문화·운동·미학 문맥이다. 검은 옷이나 여성 밴드 하나로 소속을 추론하지 않는다.|S24,S25,S26,S41
N13|쇼맨십·군중 행위|기타 팔 윈드밀과 머리 윈드밀, 점프·포고·모싱·서핑·다이빙·압박·실제 폭행은 구별한다. 운동 궤적·합의·받침 성공·안전·부상 유무는 단일 사진에서 확정되지 않는다.|S30,S35
N14|복식·소재·몸·정체성|코르셋/뷔스티에, 하네스/기타 스트랩, 라텍스/PVC, 피시넷/메시, 플랫폼/웨지/굽, 턱시도/테일코트의 가시 구조를 분리한다. 복장·화장·헤어는 나이·젠더 정체성·성적 지향·욕망·동의를 판정하지 않는다.|S25,S26,S27,S28,S41
N15|악기와 소품의 부품 소유|기타/베이스 변형, 할로/세미할로, 싱글/더블컷, 픽업/브리지, 드럼·심벌 종류, 케이스·악보 종류는 부품 위치·단면·모델 정보가 필요하다. 모든 악기의 현·페그 수를 보편화하지 않는다.|S10,S04,S06
N16|공간·조명·화면의 증거|컨트롤룸 유리·팝 필터·객석·무대·배치도·사진/거울의 경계를 보존한다. 다이제틱/논다이제틱 음악과 공연 후 정적은 소리·시간 문맥이며 역광·헤이즈·고보 외형만으로 장르나 실제 대기 성분을 확정하지 않는다.|S13,S14,S42,S43
N17|서사의 원인과 이력|첫 무대·재결합·유품·재능/노력·화해·공로 다툼·생계·연애·마지막 공연·성장과 악화는 외형의 암시와 실제 이력을 분리한다. 미완성곡·작사 노트의 법적 저자와 시간은 문서 문맥이 필요하다.|S32,S36,S37,S38,S40
N18|성인 표현·친밀감·상품화|섹스 어필·페티시 패션·속옷 겉옷화·성인 누드·버레스크·캠프·젠더 퍼포먼스·그루피·팬서비스·몸의 상품화를 구별한다. 성인 설정을 보존하고 자발적 표현·외부 압박·욕망·실제 관계는 분리한다.|S25,S26,S27,S28,S29
N19|폭력·착취·건강·파멸|학대·성적 강요·캐스팅 카우치·스토킹·의존·번아웃·청력/목소리/손 문제·표절·폭행·압박·모조 피·오컬트 페르소나는 삭제하지 않는다. 피해·진단·권리·강요·실제 신앙은 장면 외형만으로 확정하지 않고 추가 문맥을 보존한다.|S29,S30,S31,S34,S35
N20|작품과 조합의 참조 범위|공식 작품 소개는 서사의 소재 근거다. 등장인물·장면 전체의 재현이나 새 후보의 실제 외형 검증이 아니다. 원문의 조합 예시 7행은 저자 제안이며 표준 장르 정의가 아니다.|S32,S33,S34,S36,S37,S38,S39,S40,S44
'''
contexts=[]
for line in CONTEXT_ROWS.strip().splitlines():
    nid,title,bound,sids=line.split('|'); contexts.append(dict(id=nid,name_ko=title,meaning_boundary_ko=bound,source_ids=sids.split(','),runtime_importable=False,positive_visual_candidate=False,seed_ids=[]))
tables=json.loads((ROOT/'conversation-tables.json').read_text())
keywords=[]; by_card={x['id']:x for x in cards}; by_context={x['id']:x for x in contexts}
for table in tables:
    ti=table['table_index']; routes=ROUTES[ti].split(';'); assert len(routes)==len(table['rows']),(ti,len(routes),len(table['rows']))
    for ri,((term,definition),route) in enumerate(zip(table['rows'],routes),1):
        kid=f'K{len(keywords)+1:03d}'; cids=[] if route=='-' else route.split(','); nid=CONTEXT_BY_TABLE[ti]
        for cid in cids: by_card[cid]['seed_ids'].append(kid)
        by_context[nid]['seed_ids'].append(kid)
        keywords.append(dict(id=kid,table_index=ti,row_index=ri,section=table['section'],term=term,seed_definition=definition,seed_definition_status='conversation_seed_not_independently_verified_in_full',optional_visual_components=cids,context_ids=[nid],route_type='context_only' if not cids else 'optional_component_plus_context',equivalence=False,whole_compound_term_covered=False,automatic_hard_activation=False,adoption_authority=False,disposition='preserved_and_routed_not_all_meanings_verified'))
assert len(keywords)==392
for k in keywords:
    k['contrast_visual_cards']=[]
    if k['term'].startswith('림샷'):
        k['contrast_visual_cards']=['A20']
        by_card['A20']['seed_ids'].append(k['id'])
        by_card['A20']['seed_relation']='contrast_example_not_equivalent_to_open_rimshot'
write('keyword-atlas.json',keywords); write('semantic-cards.json',cards); write('context-distinctions.json',contexts)

# New research includes concrete scene alternatives and a separate incompleteness register.
HOLD_ROWS='''
Q01|연주 기술의 세부 표본|A04,A05,A19,A20,A23,A25,A29|Fender·Yamaha·Indiana University·Roland 본문/발췌로 해당 정의와 일부 교습 관계를 보강했다. 실제 이미지/영상의 양끝 접점 확인, 튜닝/음정, 어쿠스틱 스네어와 모델별 전자패드 조건의 표본 심사는 남아 있다.
Q02|복식과 헤어의 세부 표본|E02,E08,E09,E12,E16,E18,F01,F02,F05,F08|배틀 재킷·코르셋/뷔스티에·불릿 벨트·크리퍼스·테일코트·모호크/리버티·퐁파두르·콥스페인트의 개별 소장품/씬 자료가 필요하다. 박물관 일반 소개를 전체 구조의 증명으로 쓰지 않는다.
Q03|발성·음악이론의 세부 용례||벨팅/팔세토/허시·그로울·멜리스마, 음색/텍스처/싱코페이션/유니즌/음계 구분은 원문 정의를 보존하되 교육·평가 1차 문헌으로 후속 검토한다. 얼굴 포즈 후보로 대체하지 않는다.
Q04|진정한 신호 작동과 라우팅|B07,B08,B12,B13,A30,A31|가시 케이블·미터만으로 전기적 작동·오디오 청취·MIDI 라우팅·클릭 비송출·통신 성공을 확인할 수 없다. 특정 장비 명세와 실제 동작 검증은 별도다.
Q05|군중·쇼맨십의 동적 차이|G06,G07,G08,G09,G10,G11,G13,G14,G15,G16|한 순간 외형을 반복 운동·전체 궤적·착지·합의·안전으로 승격하지 않는다. 장면 프록시는 가능하나 세부 동작·관습은 영상/공연 아카이브로 더 검토한다.
Q06|성인 누드·버레스크의 전용 근거|H14,H15|성인 표현을 연구에서 유지한다. 이번 자료는 공연 일반 맥락이며 구체 작품·표본·역사적 용례를 검증하지 못했다. 공연자/기관의 공개 아카이브로 후속 심사한다.
Q07|스토킹·성적 강요·캐스팅 카우치||위협 메시지·출입구·초인종·인물의 회피는 창작 프록시로 가능하다. 실제 강요·동의·범죄·권력관계·반복 감시는 설정/기록이 필요하다. 성적 의미를 일반 계약 갈등으로 소거하지 않는다.
Q08|약물·알코올·번아웃·신체 문제||병·컵·손의 붕대·귀 보호구·휴식은 그 자체만으로 중독·정신건강·청력·발성 장애·손상 원인을 입증하지 않는다. 음악 노동·의학 자료의 개념 검토 후 문맥으로 보존한다.
Q09|장르·지역·시대별 독립 표본||재즈/블루스/Funk/소울/포크/로커빌리/퓨전/신스팝/라이브 힙합, 개러지/메탈/하드코어/팝펑크/이모/포스트펑크/글램/그런지/슈게이즈의 독립 공연 아카이브가 더 필요하다. 한 가지 복식 묶음으로 일반화하지 않는다.
Q10|악기 바디·부품 변이|A14|할로/세미할로 단면·싱글/더블컷·오프셋·카포/슬라이드·키타·앰프헤드/캐비닛·심벌 종류·기가방/하드/플라이트케이스는 전용 모델 자료로 세분화한다. 외관이 비슷한 일반 소품을 완전 동의어로 쓰지 않는다.
Q11|라이브하우스 계약과 산업 용례|C10,C13|노르마·라이더·대반·원맨·EP 분량·회수·로열티·퍼블리싱의 지역/시장/계약별 차이를 확인한다. 미국 저작권 자료를 한국 법률 판단이나 특정 계약 사실로 옮기지 않는다.
Q12|운영 검색·native·픽셀||이번에는 source 수정·인덱스 빌드·검색 품질 평가·native 자격·이미지 생성·사용자 수용·commit/push를 실행하지 않았다. 각각 후속 단계의 독립 증거가 필요하다.
'''
holds=[]
for l in HOLD_ROWS.strip().splitlines():
    qid,title,cids,reason=l.split('|'); holds.append(dict(id=qid,topic=title,card_ids=cids.split(',') if cids else [],reason_and_next_ko=reason,status='open_followup_not_topic_exclusion'))
write('remaining-research.json',holds)

direct_holds={}
for h in holds:
    for cid in h['card_ids']:direct_holds.setdefault(cid,[]).append(h['id'])
for c in cards:c['hold_ids']=direct_holds.get(c['id'],[])
write('semantic-cards.json',cards)
context_followups={'N03':['Q03'],'N04':['Q03'],'N07':['Q03'],'N09':['Q11'],'N11':['Q11'],'N12':['Q09'],'N15':['Q10'],'N18':['Q06'],'N19':['Q07','Q08']}
for k in keywords:
    k['hold_ids']=sorted(set([h for cid in k['optional_visual_components'] for h in by_card[cid]['hold_ids']]+[h for nid in k['context_ids'] for h in context_followups.get(nid,[])]))
    k['source_ids']=sorted(set([sid for cid in k['optional_visual_components']+k['contrast_visual_cards'] for sid in by_card[cid]['source_ids']]+[sid for nid in k['context_ids'] for sid in by_context[nid]['source_ids']]))
    k['source_support']='bounded_component_or_context_evidence_not_full_seed_definition_verification'
    k['sense_key']=f"table_{k['table_index']:02d}_row_{k['row_index']:02d}"
write('keyword-atlas.json',keywords)

def md_sources(ids):
    ss={s['id']:s for s in sources};return ', '.join(f"[{sid} {ss[sid]['title']}]({ss[sid]['url']})" for sid in ids)
lines=['# 음악물·밴드물 시각 의미 카드', '', '124개는 독립 저작한 선택적 장면 초안이다. 출처는 제한된 용어·직무·문화 문맥만 뒷받침하며 전체 장면의 실재 표본을 입증하지 않는다. 모든 후보의 운영 import·native 승인·자동 강제 활성화는 false다.', '']
for c in cards:
    lines += [f"## {c['id']} — {c['name_ko']}",'',c['phrase_ko'],'',c['phrase_en'],'', '**보존할 가시 관계:** '+ ' / '.join(g['requirement_ko'] for g in c['observable_components']), '', '**혼동 경계:** '+c['confusion_boundary_ko'], '', '**출처의 제한된 근거:** '+md_sources(c['source_ids']), '', '**원문 연결:** '+', '.join(c['seed_ids'])+'; **제안 슬롯:** '+', '.join(c['proposed_slots'])+'; **후속 검토:** '+(', '.join(c['hold_ids']) or '전체 문장 한영·소유자·슬롯 심사'), '']
(ROOT/'VISUAL-CARDS.md').write_text('\n'.join(lines))
lines=['# 원문 392행 추적표','','전체 뜻·복합 용어의 완전 검증을 주장하지 않는다. 카드 연결은 해당 뜻을 위한 선택적 부분 실현이며 모든 원문 설명을 그대로 보존한다. 상세 정의는 keyword-atlas.json에 있다.','', '| ID | 절/표 행 | 원문 키워드 | 선택 카드 | 문맥 |','|---|---|---|---|---|']
for k in keywords:
    choices=', '.join(k['optional_visual_components']) or '문맥 유지'
    if k['contrast_visual_cards']:choices+='; 대조: '+', '.join(k['contrast_visual_cards'])
    lines.append(f"| {k['id']} | T{k['table_index']:02d}/{k['row_index']} | {k['term']} | {choices} | {', '.join(k['context_ids'])} |")
(ROOT/'KEYWORD-ATLAS.md').write_text('\n'.join(lines)+'\n')
lines=['# 출처와 근거 범위','',f'확인일: 2026-10-25 KST. 공개 1차 출처 {len(sources)}개. publisher_excerpt_read는 검색 서비스가 제공한 발행자 발췌를 읽은 상태이며 전체 원문 확인과 구별한다. 원격 이미지/영상 표본의 시각 확인은 모두 미실행이다. 실패한 접근 경로는 아래 별도 기록했다.','']
for s in sources:
    lines += [f"## {s['id']} — {s['title']}",'',f"[{s['title']}]({s['url']})",'',f"- 확인 범위: {s['verified_scope_ko']}",f"- 접근: {s['access_status']}; 기록: `{s['evidence_file']}`",f"- 한계: {s['limits_ko']}",'']
lines += ['## 접근 실패와 대체 경로','','- Yamaha의 추정 경로 `/guitar/play/`는 열리지 않았다. electric_guitar/mechanism 및 악기별 실제 경로를 사용했다.','- V&A `/articles/the-story-of-punk`는 열리지 않았다. NGV의 소장품 설명으로 펑크와 페티시 복식의 연결을 확인했다.','- `bocchi.rocks/tv/story/`는 403이었다. Aniplex 공식 에피소드 소개에서 서포트·노르마·작사 문맥을 확인했다.','- GKIDS 페이지 직접 열기는 타임아웃이었다. 발행자 검색 발췌에서 세 곡·3일·보컬 결원 문맥을 확인했다.','- Shure SM4 및 MU 일부 직접 응답은 본문이 제한적이었다. source register는 실제 읽은 다른 Shure 교육 본문과 MU 발췌를 근거로 구분한다.','- 현행 장비 판매가·출시 상태·법률 자문·운영 안전 절차는 조사 결론 범위에 넣지 않았다.']
(ROOT/'SOURCES.md').write_text('\n'.join(lines)+'\n')
lines=['# 시각 판정과 문맥 판정','','문맥 진단은 긍정 장면 후보가 아니며 자동 profile activation의 근거가 아니다.','']
for n in contexts:lines += [f"## {n['id']} — {n['name_ko']}",'',n['meaning_boundary_ko'],'',md_sources(n['source_ids']),'']
(ROOT/'CONTEXT-DISTINCTIONS.md').write_text('\n'.join(lines))
summary={'scope':'research_and_integration_plan_only','date':'2026-10-25','timezone':'Asia/Seoul','conversation_id':'6adc0815-34c4-83ec-86c5-1f374795dad0','conversation_tool_truncated':True,'browser_read_all_14_sections':True,'seed_tables':len(tables),'seed_rows':len(keywords),'visual_cards':len(cards),'positive_component_gates':sum(len(c['observable_components']) for c in cards),'context_records':len(contexts),'source_records':len(sources),'source_access_counts':dict(collections.Counter(s['access_status'] for s in sources)),'followup_topics':len(holds),'card_families':dict(collections.Counter(c['family'] for c in cards)),'route_counts':dict(collections.Counter(k['route_type'] for k in keywords)),'all_seed_rows_preserved':True,'full_term_verification_complete':False,'runtime_source_modified':False,'native_qualified':False,'index_rebuilt':False,'retrieval_measured':False,'images_generated':0,'user_acceptance_established':False,'committed_or_pushed':False}
write('PACKAGE-SUMMARY.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
