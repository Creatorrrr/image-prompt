"""Build a reviewable research package; never loads or edits runtime assets."""
from __future__ import annotations
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def rows(value):
    return [line.split('|') for line in value.strip().splitlines() if line.strip()]

# Summaries below are narrow paraphrases. Staging proposals are our authored
# hypotheses, not empirical results or image annotations supplied by a source.
DICTIONARY = rows('''
pensive|https://dictionary.cambridge.org/us/dictionary/english/pensive|조용하고 진지하게 생각하는 뜻. 불안·슬픔을 포함할 수 있으나 특정 표정은 정의되지 않는다.|search_excerpt
contemplative|https://www.merriam-webster.com/dictionary/contemplative|숙고·관조에 관계된 뜻. 종교적 용례는 별도 문맥이다.|opened
reflective|https://www.merriam-webster.com/dictionary/reflective|빛을 반사하는 뜻과 생각에 잠기는 뜻이 공존한다.|opened
introspective|https://www.merriam-webster.com/dictionary/introspective|자기 생각과 감정을 살피는 뜻. 내향적 성격과 동의어가 아니다.|opened
ruminative|https://www.merriam-webster.com/dictionary/ruminative|반복해서 곱씹는 생각. 해당 페이지의 ruminate 연결을 확인했다.|opened_redirect
engrossed|https://www.merriam-webster.com/dictionary/engrossed|주의를 온전히 사로잡는 뜻. engross의 다른 문서 용례와 분리한다.|opened_redirect
inquisitive|https://www.merriam-webster.com/dictionary/inquisitive|묻고 알아보려는 성향. 긍정적 탐구와 지나친 캐묻기의 문맥이 갈린다.|opened
analytical|https://www.merriam-webster.com/dictionary/analytical|요소를 나누어 분석하는 뜻. analytic의 전문 용례들과 구별한다.|opened_redirect
skeptical|https://www.merriam-webster.com/dictionary/skeptical|회의·의심의 태도. 얼굴 한 부위로 정의되는 뜻이 아니다.|opened
discerning|https://www.merriam-webster.com/dictionary/discerning|차이를 알아보고 판단하는 안목. 선호하는 의상 형태를 정의하지 않는다.|opened
astute|https://www.merriam-webster.com/dictionary/astute|예리하게 알아차리고 이해하는 뜻. 책략의 용례가 곧 범죄라는 뜻은 아니다.|opened
scholarly|https://www.merriam-webster.com/dictionary/scholarly|학문·학자와 관계되거나 학구적인 뜻. 실제 직업을 증명하는 외양 규칙은 아니다.|opened
erudite|https://www.merriam-webster.com/dictionary/erudite|공부로 얻은 풍부한 지식. 소품 개수로 측정할 수 없다.|opened
cerebral|https://www.merriam-webster.com/dictionary/cerebral|뇌에 관계된 뜻과 지적 사고를 강조하는 비유적 뜻이 공존한다.|opened
professorial|https://www.merriam-webster.com/dictionary/professorial|교수와 관계되거나 교수 같은 뜻. 의상·연령·성별은 필수 조건이 아니다.|opened
methodical|https://www.merriam-webster.com/dictionary/methodical|방법·질서·체계를 따르는 뜻. 정리된 방만을 의미하지 않는다.|opened
measured|https://www.merriam-webster.com/dictionary/measured|신중하고 절제된 뜻 외에 측정·리듬의 뜻이 있다.|opened
pedantic|https://www.merriam-webster.com/dictionary/pedantic|세부나 학식을 과도하게 내세우는 비판적 함의. 박학과 등치하지 않는다.|opened
''')

SOURCES = [dict(id='D_' + word, title=word + ' dictionary entry', url=url,
                authority='dictionary_publisher', access=access, support=summary,
                limits='어휘 뜻의 근거이며 특정 얼굴·의상·지능 또는 정신 상태의 시각적 판별 근거는 아니다.')
           for word, url, summary, access in DICTIONARY]
for sid, title, url, authority, access, support, limits in rows('''
S_RODIN|Musée Rodin — The Thinker|https://www.musee-rodin.fr/en/musee/collections/oeuvres/thinker|collection_owner|opened|작품의 기원과 사유하는 신체의 조형 맥락.|실제 인물의 지능 근거가 아니다. 이번 조사에서 원본 이미지의 관절 좌표를 계측하지 않았다.
S_PENSIVE|National Museum of Korea — Pensive Bodhisattva|https://www.museum.go.kr/ENG/contents/E0201070000.do?relicId=17730&schM=view&showHallId=631120|collection_owner|opened|오른발을 왼 무릎에 놓고 오른손 손가락을 뺨에 대는 자세와 불교적 유래를 설명한다.|중립적인 포즈와 보살 도상·시대·문화 정체성은 별도 조건이다.
S_ERASMUS|National Gallery — Erasmus|https://www.nationalgallery.org.uk/paintings/hans-holbein-the-younger-erasmus|collection_owner|opened|학자 초상에서 책·손·문구 등 상징이 조직되는 구체 사례.|소장기관의 작품 해석이다. 상징을 실제 인물의 능력이나 실제 작업실 기록으로 일반화하지 않는다.
S_ARISTOTLE|Met — Aristotle with a Bust of Homer|https://www.metmuseum.org/art/collection/search/437394|collection_owner|opened|손과 흉상의 접촉 및 의복·메달을 통한 상징적 초상 사례.|모든 학자에게 책·검소한 옷·안경이 필요하다는 규칙으로 사용하지 않는다.
S_GESTURE|McNeill Lab — Gesture: A Psycholinguistic Approach|https://mcneilllab.uchicago.edu/pdfs/gesture.a_psycholinguistic_approach.cambridge.encyclop.pdf|research_author|opened_pdf|도상성·은유성·지시성·시간적 강조는 한 몸짓에서 겹칠 수 있는 차원이다. 비트는 말과 시간 관계를 갖는다.|단일 스틸로 비트나 발화 동기화를 검증할 수 없다. 사물을 가리키는 손가락만이 지시 몸짓인 것도 아니다.
S_FACS|Paul Ekman Group — FACS|https://www.paulekman.com/facial-action-coding-system/|method_owner|opened|얼굴의 관찰 가능한 움직임을 기술하는 방법의 범위.|이번 조사에서 유료 매뉴얼이나 코더 인증 검증을 수행하지 않았다. AU 번호·감정·지능 자동 판정을 붙이지 않는다.
S_EYE|Wiseman et al. — The Eyes Don't Have It (2012)|https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0040259|research_authors|opened|세 연구에서 검토한 NLP식 눈 방향과 거짓말 판별 주장의 근거를 찾지 못했다.|모든 시선과 모든 인지 과정의 무관함을 입증한 연구가 아니다. 눈 방향을 기억·거짓말 코드로 사용하지 않는다.
S_YALE_CAMERA|Yale Film Analysis — Cinematography|https://filmanalysis.yale.edu/cinematography/|university_teaching|opened|숏 크기·시점·프레이밍·깊은 초점·얕은 초점·시간에 따른 초점 이동을 구별한다.|영화 분석 용례다. 정확한 초점거리·조리개를 픽셀만으로 역산하는 근거가 아니다.
S_YALE_STAGE|Yale Film Analysis — Mise-en-scène|https://filmanalysis.yale.edu/mise-en-scene/|university_teaching|opened|공간·소품·의상·조명을 함께 구성하며 하이키·로키를 키와 필의 관계로 설명한다.|하이키를 과노출, 로키를 무조건 어두운 이미지로 대체하지 않는다.
S_ENV|Nikon — Environmental Portraiture with Joey Terrill|https://www.nikonusa.com/p/environmental-portraiture-featuring-joey-terrill/18483/overview|practitioner_publisher|search_excerpt|장소와 인물이 관계를 맺는 환경 초상 강좌의 범위.|강좌 전체나 실습을 확인한 것은 아니다. 실제 직업 증명의 기준으로 사용하지 않는다.
S_NEGATIVE|Adobe — Negative space photography|https://www.adobe.com/creativecloud/photography/type/negative-space-photography.html|practitioner_publisher|search_excerpt|주된 대상과 주변 여백의 관계를 설명하는 촬영 개념.|여백이 반드시 단색·무질감일 필요는 없다. 지적 능력의 근거가 아니다.
S_COMPOSITION|Adobe — The basics of photography composition|https://www.adobe.com/creativecloud/photography/discover/photo-composition.html|practitioner_publisher|opened|삼분할·시점·크롭·유도선은 의도를 돕는 구성 선택이다.|공식 하나로 이미지 의미나 품질을 보장하지 않는다.
S_LINES|Adobe — Leading lines photography|https://www.adobe.com/creativecloud/photography/discover/leading-lines-photography.html|practitioner_publisher|opened|선형 요소가 화면의 대상이나 관심 지점으로 주의를 연결한다.|모든 선이 소실점으로 수렴해야 하는 것은 아니다.
S_REMBRANDT|Profoto / Hannah Couzens — How to create Rembrandt light|https://www.profoto.com/bg/en/still-photography/tips-tricks/how-to-create-rembrandt-light/|lighting_practitioner|search_excerpt|코와 뺨의 그림자가 이어져 어두운 쪽 뺨에 빛 삼각형을 남기는 배치.|장비 명칭이나 고정 45도만으로 성공을 판정하지 않는다. broad/short lighting과 독립 축이다.
S_PYTHON_ERRORS|Python — Errors and Exceptions|https://docs.python.org/3/tutorial/errors.html|software_maintainer|opened|오류·예외 메시지와 traceback의 실행 위치 연결.|임의의 코드 화면은 디버깅 증거가 아니다. 버전별 UI 외양을 규칙으로 만들지 않는다.
S_PDB|Python — pdb|https://docs.python.org/3/library/pdb.html|software_maintainer|opened|중단점·실행 스택·상태 조사라는 디버거 작업.|스크린샷의 사실성 또는 실제 프로그램 수정 성공을 입증하지 않는다.
S_SCATTER|NIST / SEMATECH — Scatter Plot|https://www.itl.nist.gov/div898/handbook/eda/section3/scatterp.htm|method_publisher|opened|짝지어진 변수의 산점도와 패턴·이상 관측 탐색.|상관을 인과로 바꾸지 않는다. 원자료 대응은 별도 확인한다.
S_DARWIN|Darwin Correspondence Project — Reading notebooks|https://www.darwinproject.ac.uk/people/about-darwin/what-darwin-read/darwin-s-reading-notebooks|archive_research_project|opened|읽은 책·읽을 책과 독서 기록이 남는 사례.|모든 메모의 내용·인지 능력·시대 의상을 일반화하지 않는다.
S_SCORE|Library of Congress — Beethoven sketch for Das Schweigen|https://www.loc.gov/collections/moldenhauer-archives/articles-and-essays/guide-to-archives/beethovens-das-schweigen/|collection_owner|search_excerpt_open_failed|악보 초안의 단편과 수정·작업 과정이 보존된 구체 사례.|원본 픽셀을 검수하지 않았다. 임의 음표의 음악적 정확성은 입증되지 않는다.
S_TWEED|Harris Tweed Authority — Greasy and woven tweed|https://www.harristweed.org/journal/word-of-the-week-greasy-and-woven-tweed/|material_authority|search_excerpt|경사·위사를 짜는 직물 구조의 사례.|Harris Tweed의 지역·생산 조건을 일반 트위드의 보이는 속성으로 추론하지 않는다.
S_DARK|Vogue — Fashion's new trend funnel (2020)|https://www.vogue.com/article/from-tiktok-to-depop-fashions-new-trend-funnel|fashion_original_reporting|opened|다크 아카데미아의 학구적 공간·고스/프레피 스타일을 다룬 문화 사례.|2020년 기사다. 2026년 인기 순위·실제 학적·연령의 근거가 아니다.
S_GEEK|Vogue — Geek-chic Bayonetta glasses|https://www.vogue.com/article/geek-chic-bayonetta-glasses-renaissance-gabbriette-bella-hadid-miu-miu|fashion_original_reporting|opened|좁은 안경 프레임을 포함하는 패션 사례.|안경을 쓴 사람의 능력·직업·성향을 판정하지 않는다.
S_OFFICE|Vogue — Office siren, girlhood and patriarchy (2024)|https://www.vogue.com/article/office-siren-girlhood-trend-patriarchy|fashion_original_reporting|opened|안경·셔츠·슬림한 실루엣 등이 사용된 2024년 패션 담론.|성인 패션 선택과 실제 사무직·권력 관계·동의를 분리한다. 현재 유행 강도는 조사하지 않았다.
S_SAPIO|Merriam-Webster — Gender and identity terms: sapiosexual section|https://www.merriam-webster.com/wordplay/merriam-websters-short-list-of-gender-and-identity-terms/gender-dysphoria-gender-identity-disorder|dictionary_publisher|opened|지성에 대한 성적 매력을 가리키는 용어의 설명.|실제 인물의 성적 지향은 시각 데이터로 판정하지 않는다. 장면 모티프만 별도로 저작할 수 있다.
S_WARROOM|GOV.UK — Secret war rooms|https://www.gov.uk/government/news/secret-war-rooms|historic_site_government_record|opened|Cabinet War Rooms의 Map Room과 지도를 통한 전황 기록의 역사 사례.|현재 군사 전술·지도 정확성·인물의 실제 명령 권한을 입증하지 않는다.
S_EVIDENCE|NISTIR 7928 — Biological Evidence Preservation (2013)|https://nvlpubs.nist.gov/nistpubs/ir/2013/NIST.IR.7928.pdf|method_publisher|opened_pdf|생물학적 증거의 분리 포장·봉인·표지·추적을 다루는 지침.|2013년 자료의 시각적 소품 설계 참고다. 전체 법과학이나 관할 법률의 최신 적합성을 인증하지 않는다.
S_CHESS|FIDE — Laws of Chess, Article 2.1|https://handbook.fide.com/chapter/E012023|rules_authority|opened|밝고 어두운 64칸으로 이루어진 8×8 보드의 구조.|보드 외양만으로 임의 국면의 합법성·복기 내용·전략 능력을 판정하지 않는다.
S_GO|AGA Rules Committee — Concise Rules|https://www.usgo-archive.org/files/pdf/conciserules.pdf|rules_authority_archive|search_excerpt|돌을 빈 교차점에 놓는 보드 배치.|아카이브 문서다. 특정 기보 전체의 합법성·승패는 별도 검증한다.
'''):
    SOURCES.append(dict(id=sid, title=title, url=url, authority=authority,
                        access=access, support=support, limits=limits))

# One decision for every source term. The observable form is a proposed carrier,
# not a universal classifier. Reuse references are verified against the captured
# authored inventory; proposed units are defined further below.
DECISIONS = rows('''
1|context_only|사색은 내적 상태이며 고개 숙임·턱 괴기를 필수로 만들지 않는다.|요청한 책·메모가 있을 때 시선 이탈과 멈춘 손을 선택적 장면으로 제안한다.|졸림·슬픔·피로와 같은 자세가 겹친다. 실제 생각은 판정 불가.|pv_chin_support,pv_gaze_offcamera|ia_pause_work|D_pensive
2|context_only|관조의 사전 의미와 불교 도상을 나눈다.|거리 둔 관찰 또는 정적인 배치를 제안하되 대상은 요청에서 받는다.|모든 관조를 무판단·종교·명상으로 정의하지 않는다.|pv_seated_upright|ia_pause_work|D_contemplative
3|context_only|thoughtful 의미를 반사 재료 의미와 분리한다.|기존 메모와 수정본을 비교하는 장면을 선택할 수 있다.|Reflective만으로 금속·거울이나 과거 회상을 강제하지 않는다.|pv_book_read|ia_revision_sequence|D_reflective
4|context_only|자기 생각·감정을 살피는 뜻과 내향적 성격을 나눈다.|요청한 일지와 짧은 메모를 연결하는 장면은 가능하다.|장면에서 성격·정신 건강·실제 감정을 판정하지 않는다.|eyes_down_introspective|ia_pause_work|D_introspective
5|temporal_context|곱씹기의 반복은 한 장의 형태가 아니다.|동일 항목의 여러 검토 표시와 현재의 읽기 자세를 선택한다.|반복 사고의 지속 시간이나 병적 반추로 단정하지 않는다.|pv_book_read|ia_revision_sequence|D_ruminative
6|context_only|몰두는 주의의 정도이며 눈 찡그림과 동의어가 아니다.|현재 손의 작업 대상과 시선 대상이 연결된 모습을 선택한다.|배경의 고립·책의 양·안경은 몰두 증거가 아니다.|pv_book_read|ia_reference_link|D_engrossed
7|context_only|질문하고 알아보려는 뜻을 고개 기울임과 등치하지 않는다.|지적하는 미완 항목·메모·대화 상대를 연결한다.|캐묻기·불신·어린 외양을 자동 추가하지 않는다.|pv_head_tilt|ia_followup_question|D_inquisitive
8|context_only|분석의 대상·분해 기준이 필요하다.|같은 열 기준을 갖는 비교표와 특정 차이에 놓인 펜을 제안한다.|칠판의 복잡함을 분석의 정확성으로 바꾸지 않는다. 수학 전문 용례도 분리한다.||ia_comparison_matrix|D_analytical,S_SCATTER
9|context_only|검증하려는 회의와 단순한 옆눈을 나눈다.|원 주장과 반례 자료를 같은 기준으로 비교하는 장면을 선택한다.|skeptical_side_eye만 채택하면 요청하지 않은 시선 방향이 붙을 수 있다.|skeptical_side_eye|ia_reference_link|D_skeptical
10|context_only|분별력은 관찰 가능한 물리 속성이 아니다.|두 물건의 같은 부위를 확대해 비교하는 선택적 구성.|고급 의상·예술품 소유를 안목이나 계층의 증거로 쓰지 않는다.||ia_art_compare|D_discerning
11|context_only|예리한 이해와 책략·범죄를 분리한다.|도식의 특정 불일치에 펜을 정지시킨 장면을 선택한다.|날카로운 눈매·비대칭 미소가 지능·악의를 입증하지 않는다.||ia_reference_link|D_astute
12|context_only|학구적이라는 뜻과 학교 신분·교복을 나눈다.|출처 표시·주석·작업 문서처럼 학습 활동을 드러내는 구성을 제안한다.|연령·성별·실제 학력이나 직업을 보태지 않는다.|pv_book_read|ia_close_read|D_scholarly,S_ERASMUS
13|context_only|풍부한 학식을 도서 수량으로 대신하지 않는다.|서로 연결되는 두 출처의 인용 표시를 선택적 연출로 쓴다.|책장만으로 박학·다학제 지식을 판정하지 않는다.||ia_reference_link|D_erudite,S_ARISTOTLE
14|context_only|지적 사고를 강조하는 비유적 뜻과 뇌의 해부학적 뜻을 구별한다.|요청한 추론 도식의 전제·중간 단계·결론을 연결한다.|cerebral이 자동 무표정·미니멀·비관능이라는 뜻은 아니다.||ia_structured_board|D_cerebral
15|context_only|교수풍이라는 유사성 표현과 실제 교수를 나눈다.|공유 자료를 가리키는 설명 자세를 선택할 수 있다.|중년 남성·트위드·안경·엘보 패치를 필수로 만들지 않는다.|teaching_at_blackboard|ia_teaching_reference|D_professorial
16|context_only|방법을 따르는 행동과 단순한 정돈을 나눈다.|번호 있는 단계·같은 양식의 기록·진행 체크를 연결한다.|지저분한 방이 체계적이지 않다는 판정도 금지한다.||ia_revision_sequence|D_methodical
17|context_only|신중한 대응의 뜻과 물리적 측정의 뜻을 나눈다.|펜을 낮춘 손과 명시된 상대·자료를 보는 절제된 대응을 선택한다.|속도·리듬·숙고 시간을 스틸에서 판정하지 않는다.||ia_listening_reference|D_measured
18|context_only|현학의 비판적 과도함을 박학과 구별한다.|아주 작은 주석을 짚는 설명 장면은 가능하나 평가적 함의는 서사에 둔다.|빽빽한 주석·손가락 하나를 현학적 성격의 확정 증거로 쓰지 않는다.||ia_annotation_anchor|D_pedantic
19|named_pose|작품명·지지 기하·누드 여부를 별도 축으로 둔다.|낮은 좌석, 앞으로 접힌 몸통, 반대 허벅지의 팔꿈치, 턱에 닿은 손, 받쳐진 발.|Thinker만으로 옷을 벗기거나 실제 철학자를 추가하지 않는다.|pv_chin_support,pv_forward_torso_lean|ia_thinker_support|S_RODIN
20|named_pose|중립 반가 자세와 불교 보살 도상을 분리한다.|오른발이 왼 무릎 위, 오른손 손가락이 오른 뺨, 앉은 몸의 지지가 연결된다.|figure-four 전체를 반가사유와 동의어로 두지 않는다. 종교 표지는 별도 요청.|pv_figure_four|ia_pensive_support|S_PENSIVE
21|contact_form|chin cradle은 넓은 턱 지지 중 특정 접촉 변형이다.|엄지는 턱 아래, 검지는 뺨, 팔꿈치는 책상에 받쳐지는 연속 경로.|손이 목을 잡거나 턱 앞에 떠 있으면 충족하지 않는다.|pv_chin_support|ia_chin_cradle|S_FACS
22|contact_form|관자놀이 접촉과 두통·스트레스를 분리한다.|요청한 쪽 손가락 끝이 관자놀이에 닿고 다른 손은 지정 도구를 맡는다.|얼굴 전체를 가리는 손바닥이나 실제 통증을 추가하지 않는다.|pv_temple_touch|ia_temple_local|S_FACS
23|reuse_atomic|양손 대응 손끝과 떨어진 손바닥이 핵심이다.|동일 인물 두 손의 손끝이 맞닿고 손바닥 사이에 공간이 남는다.|합장·깍지·타인의 손과 구별한다. 권력·책략을 자동 추론하지 않는다.|pv_steepled_fingers||S_GESTURE
24|reuse_atomic|맞물린 손가락과 손 소유자를 분명히 한다.|동일 인물 두 손의 손가락이 번갈아 걸린 형태, 각각의 손목 연결.|손끝 맞대기와 타인의 손잡기를 별도 관계로 둔다.|pv_interlaced_fingers||S_GESTURE
25|contact_form|팔짱 전체가 아니라 한 팔이 다른 팔꿈치를 받치는 지지 구조다.|받치는 전완 위에 반대 팔꿈치, 그 팔의 손이 턱에 닿는다.|두 팔 모두 몸통에 감긴 방어적 팔짱으로 바꾸지 않는다.|pv_chin_support|ia_crossarm_support|S_RODIN
26|contact_form|뒷짐의 특정 손목 잡기 변형과 관찰 활동을 분리한다.|등 뒤 한 손이 반대 손목을 잡고 몸 앞 관찰 대상은 따로 지정.|손을 단순히 뒤로 숨기는 것만으로 손목 접촉을 충족하지 않는다.|pv_hands_behind_back|ia_wrist_behind_back|S_GESTURE
27|reuse_with_relation|몸통 전방 기울기와 카메라 접근을 나눈다.|앉은 골반의 지지, 몸통의 앞 기울기, 전완의 책상 지지, 상대 지향.|렌즈 근접·허리 굽힘만으로 경청을 증명하지 않는다.|pv_forward_torso_lean|ia_listening_reference|S_YALE_STAGE
28|reuse_with_relation|직립 자세와 실제 경청·복종을 구별한다.|등의 축, 내려간 어깨, 무릎이나 노트 위 손, 요청한 화자 지향.|군기·긴장·권위·순종을 자동 추가하지 않는다.|pv_seated_upright|ia_listening_reference|S_YALE_STAGE
29|support_variant|기댄 숙고는 등받이의 실제 지지가 중요하다.|등과 등받이의 접촉, 낮춘 펜 손, 화면 또는 지정한 윗지점의 시선.|떠 있는 상체나 졸림·안일함·실제 생각을 판정하지 않는다.||ia_reclined_support|S_YALE_STAGE
30|temporal_context|걷다가 멈췄다는 사건은 시간 정보가 필요하다.|한 발 앞의 정지 자세, 돌아간 머리, 들고 있는 메모를 종점 스틸로 제안.|스틸에서 이전 걷기나 제동을 검증하지 않는다.||ia_walk_notes|S_YALE_CAMERA
31|hand_prop_form|페이지 고정은 읽기 일반과 다른 접촉이다.|손바닥·엄지가 지정 여백을 누르고 종이 면과 책의 지지가 이어진다.|글을 가리는 손이나 책 위 떠 있는 손을 성공으로 세지 않는다.|pv_book_read|ia_page_hold|S_DARWIN
32|hand_prop_form|페이지가 들린 형상과 넘김의 시간적 움직임을 분리한다.|엄지·검지가 페이지 모서리를 잡고 휜 종이의 기부가 책에 이어진다.|낱장 전체가 분리되거나 양면이 동시에 관통하는 오류를 제외한다.|pv_book_read|ia_page_turn_endpoint|S_YALE_CAMERA
33|hand_prop_form|pen hover는 필기 접촉과 반대 상태다.|잡은 펜 끝과 종이 사이에 작은 가시적 간격, 받쳐진 손목.|펜 끝이 닿은 필기나 공중에 떠 있는 펜으로 대체하지 않는다.||ia_pen_hover|S_YALE_STAGE
34|hand_prop_form|벗어 든 안경은 착용 안경과 물체 상태가 다르다.|한 손이 안경의 다리를 잡고 얼굴에는 그 안경이 착용되지 않는다.|손에 든 안경과 얼굴의 같은 안경을 중복 생성하지 않는다.||ia_glasses_removed|S_GEEK
35|hand_prop_form|브리지 조정의 접촉 위치를 프레임 전체와 구별한다.|손끝이 코 위 프레임 브리지에 닿고 렌즈·다리 연결은 얼굴에 남는다.|렌즈를 관통하는 손가락·안경 제거·안경 디자인 교체는 별도다.||ia_glasses_bridge|S_GEEK
36|gaze_prop_form|안경 너머 보기는 프레임 높이와 시선 대상의 관계다.|낮춘 프레임 윗선 위에 눈이 보이고 지정 대상에 시선이 향한다.|고개 들기·눈 치켜뜨기·나이 듦을 필수로 만들지 않는다.||ia_over_glasses|S_GEEK
37|gesture_relation|지시성은 구체·추상 대상 모두 가능하며 검지만 필수는 아니다.|이번 구체 변형은 손 또는 펜의 방향 끝을 지정 자료의 항목에 연결.|중립 손모양만으로 대상 지시를 충족하지 않는다. 비트와 겹칠 수 있다.||ia_deictic_reference|S_GESTURE
38|gesture_relation|도상성은 의미와 형태의 유사 관계이며 양손 벌림 하나로 고정되지 않는다.|자료 속 특정 폭·윤곽·경로에 대응하는 손 사이 거리나 손 경로의 종점.|추상 선택지 설명과 실제 사물 크기를 구별한다. 말·의미 맥락 필요.||ia_iconic_span|S_GESTURE
39|gesture_context|은유성은 추상 의미의 공간 표현이며 시각 형상만으로 확정하기 어렵다.|자료에 A/B 대안이 있을 때 서로 다른 두 공간에 손을 둔 연출.|두 손 위치만으로 시간·논점의 뜻을 입증하지 않는다.||ia_metaphoric_options|S_GESTURE
40|temporal_defer|비트는 발화 운율과 시간 관계다.|정지 이미지는 열린 손의 한 종점만 제공하고 비트 명칭은 문맥 메타데이터에 둔다.|open palm 후보를 beat의 하드 만족 후보로 쓰지 않는다.|pv_palms_up||S_GESTURE
41|gesture_relation|위로 열린 손바닥은 설명의 선택적 전달 형태다.|손바닥 면·몸 가까운 팔꿈치·지정 상대 또는 자료의 관계.|구걸·도움 요청·복종이라는 의미를 자동 붙이지 않는다.|pv_palms_up|ia_open_palm_reference|S_GESTURE
42|gesture_relation|논점 세기는 손가락의 수와 자료 번호가 연결되어야 한다.|한 손의 펼친 손가락과 다른 손의 접촉 또는 1·2·3 자료 참조.|손가락을 무작정 많이 펴는 것·관객 수를 세는 장면과 구별한다.||ia_enumeration|S_GESTURE
43|gaze_relation|대상 지향을 기술하되 주의의 지속·강도는 판정하지 않는다.|눈의 방향과 지정한 페이지·표 지점이 시각적으로 연결된다.|머리와 눈이 항상 같은 각도여야 하는 것은 아니다.||ia_gaze_reference|S_EYE
44|expression_form|미세한 눈꺼풀 좁힘은 본래 눈 형태와 분리한다.|양쪽 또는 지정 쪽 눈꺼풀 틈이 좁아지는 국소 상태.|half-lidded·좁은 눈 형태·분석 능력·의심을 자동 등치하지 않는다.|ae_squinch||S_FACS
45|expression_form|내측 눈썹의 접근과 표정의 사회적 의미를 나눈다.|미간 쪽 눈썹의 간격·주름 변화를 좁은 범위로 기술.|분노·괴로움·집중 중 하나를 픽셀에서 확정하지 않는다.|ae_knitted_brow||S_FACS
46|expression_form|한쪽 눈썹만 올라가는 비대칭과 양쪽 올림은 다르다.|요청된 쪽 눈썹이 높고 반대쪽은 더 낮은 윤곽을 유지.|양쪽 놀람 눈썹·얼굴 비틀기·우월감으로 바꾸지 않는다.|ae_single_brow||S_FACS
47|reuse_with_relation|고개 기울임과 카메라 롤을 분리한다.|머리 축이 몸통 축에 대해 기울고 지정 질문 상대를 향한다.|화면 전체의 더치 틸트만으로 고개 기울임을 충족하지 않는다.|pv_head_tilt|ia_followup_question|S_YALE_CAMERA
48|expression_form|원 조사에는 오므리기와 앞으로 내미는 입술이 섞였다.|입구·입꼬리가 중심으로 좁아지는 purse와 앞으로 돌출하는 pucker를 별도 변형으로 둔다.|Lip press·키스 행동·관능적 의도를 자동 붙이지 않는다.|ae_purse,ae_pucker||S_FACS
49|expression_form|입술 압착은 둥근 입구와 구별한다.|닫힌 입술의 접촉선과 눌린 윤곽을 국소적으로 유지.|오므리기·앞으로 내밀기·적대적 성격을 필수로 만들지 않는다.|ae_lip_press||S_FACS
50|gaze_context|먼 곳의 응시와 눈의 초점 조절·실제 회상을 나눈다.|손 가까운 자료와 떨어진 화면 밖 시선 대상을 대비시키는 연출.|지각적 초점거리·공상·기억을 눈 방향만으로 확정하지 않는다.|pv_gaze_offcamera|ia_pause_work|S_EYE
51|reuse_with_relation|아래 응시의 목적지를 책에 연결한다.|눈이 펼친 책의 지정 영역을 향하고 페이지·손 지지가 보인다.|downcast를 슬픔·순종으로 바꾸지 않는다.|pv_gaze_down,pv_book_read|ia_gaze_reference|S_EYE
52|gaze_context|위 응시와 생각의 내용·진실성을 분리한다.|머리 각도와 눈 방향을 각각 지정하고 위쪽의 대상을 선택한다.|위/좌/우를 기억·거짓말의 코드로 쓰지 않는다.|pv_gaze_up,pv_chin_up||S_EYE
53|expression_context|중립 얼굴은 경청의 확정 증거가 아니다.|낮춘 펜과 화자를 향한 몸·얼굴·공유 자료를 연결한다.|무감정·무능·침묵 동의를 추론하지 않는다.|ae_deadpan_form|ia_listening_reference|S_FACS
54|expression_context|작은 양쪽 미소와 실제 이해를 나눈다.|닫힌 입술의 작은 양측 상승과 관련 자료를 같은 장면에 둔다.|미소만으로 정답 이해·동의·호감을 증명하지 않는다.|pv_smile_closed|ia_reference_link|S_FACS
55|expression_context|비대칭 미소는 knowing의 물리 형상으로만 다룬다.|요청된 한쪽 입꼬리의 국소 상승을 선택한다.|mature_knowing_smile의 연령 함의를 일반 knowing에 이식하지 않는다.|pv_asymmetric_mouth||S_FACS
56|temporal_context|deadpan delivery는 말과 웃음의 대비를 포함한다.|스틸에서는 작은 변화의 중립 얼굴만 제공한다.|무표정 형상만으로 재치·발화 방식·감정 부재를 주장하지 않는다.|ae_deadpan_form||S_FACS,S_GESTURE
57|temporal_defer|Eureka는 이전 상태에서 발견으로 넘어가는 변화다.|원인 자료와 특정 종점 표정을 고르면 정지 장면은 가능하다.|눈 확대·눈썹 상승 한 장을 발견 전후 변화의 성공으로 세지 않는다.||ia_reference_link|S_YALE_CAMERA
58|expression_context|곤혹스러움은 문제 자료와 반응의 맥락에 둔다.|읽히는 불일치 항목, 정지된 펜, 선택한 미간 상태를 연결한다.|반복 읽기·이해 실패·능력 부족을 한 장에서 확정하지 않는다.|ae_knitted_brow|ia_reference_link|S_FACS
59|temporal_defer|자료와 화자를 오간다는 뜻은 시선의 시간적 교대다.|스틸은 둘 중 하나를 현재 시선 대상으로 명시한다.|단일 눈을 두 방향으로 보내거나 복수 얼굴로 시간 전환을 흉내내지 않는다.||ia_listening_reference|S_YALE_CAMERA
60|expression_context|엄정한 검토는 자료 관계와 국소 얼굴 상태의 결합이다.|닫힌 입술·안정된 머리·자료 지향을 선택한다.|냉혹함·유죄 판단·범죄 성격을 추가하지 않는다.|ae_lip_press|ia_reference_link|S_FACS
61|reuse_with_relation|인물과 그 공간의 작업 관계가 환경 초상의 중심이다.|읽히는 작업 대상과 손의 활동을 배경의 장소 요소에 연결한다.|배경 책장만으로 학자 직업을 증명하지 않는다.|pc_pc15_component_1,pc_pc15_component_2|ia_close_read|S_ENV,S_YALE_STAGE
62|reuse_atomic|사분의 삼 방향과 사분의 삼 길이 크롭·광대 돌출을 구분한다.|얼굴의 정면과 측면이 함께 읽히는 사선 시점.|malar_forward_projection의 해부 형태를 카메라 각도로 활성화하지 않는다.|eye_level_three_quarter||S_YALE_CAMERA
63|reuse_atomic|옆모습 방향과 인물 프로필 문서를 나눈다.|한쪽 얼굴의 이마·코·입술·턱 윤곽이 측면에서 읽힌다.|이력 프로필·뒷모습·반측면과 구별한다.|side_profile_view||S_YALE_CAMERA
64|reuse_atomic|카메라 높이와 정면 방향을 독립시킨다.|카메라가 대상 눈 높이에 가까운 배치.|눈높이라는 말만으로 정면·대등함·권위 부재를 강제하지 않는다.|eye_level_observer||S_YALE_CAMERA
65|reuse_with_relation|약한 로우앵글의 높이와 상향 방향을 각각 기술한다.|대상 눈보다 조금 낮은 카메라, 제한된 상향 시선각.|극단적 웜즈아이·권력·공격성으로 바꾸지 않는다.|pc_pc07_component_2||S_YALE_CAMERA
66|reuse_atomic|수직 부감과 비스듬한 높은 시점을 구분한다.|책상 평면을 거의 수직으로 내려보며 자료의 상대 배치를 읽는다.|높은 코너 감시 카메라·드론 사선과 등치하지 않는다.|top_down_90,strict_top_down_flat_view||S_YALE_CAMERA
67|framing_constraint|미디엄 숏의 범위는 대상·관행에 따라 조정한다.|요청된 얼굴·양손·작업 자료가 들어오는 상반신 중심 크롭.|허리라는 명칭만 고수해 필수 손·자료를 자르지 않는다.||ia_evidence_frame|S_YALE_CAMERA
68|framing_constraint|클로즈업은 얼굴 또는 특정 세부를 크게 담는 선택이다.|요청된 얼굴 부위와 필요한 가까운 손·자료 접점을 함께 유지할 수 있는지 확인.|얼굴 타이트 크롭과 책상 전체를 동시에 하드 요구하면 충돌을 보고한다.||ia_evidence_frame|S_YALE_CAMERA
69|framing_constraint|인서트는 편집상 기능, 세부 숏은 스틸의 크기다.|손·펜·주석의 관계를 크게 보여주는 스틸 상세 변형.|다른 숏과의 편집 관계를 한 장에서 검증하지 않는다.||ia_evidence_frame|S_YALE_CAMERA
70|reuse_with_relation|전경 어깨의 소유자와 주된 작업 인물을 나눈다.|전경 인물 어깨, 그 너머 대상, 공유 자료의 삼자 배치.|OTS만으로 인원 수를 늘리지 않는다. 기존 count와 충돌하면 거절.|pc_pc17_component_1,pc_pc17_component_3|ia_ots_reference|S_YALE_CAMERA
71|reuse_with_relation|시점 소유자의 눈 위치와 대상의 시야를 연결한다.|요청한 인물의 눈 높이 부근에서 자료를 내려보고 필요하면 그 인물 손이 보인다.|주관 시점에 관찰자 얼굴 전체를 자동 추가하지 않는다.|first_person_pov_hand_foreground|ia_pov_work|S_YALE_CAMERA
72|count_constraint|투숏은 두 주체의 화면 구성이다.|이미 요청된 두 인물과 공통 자료를 같은 프레임에 둔다.|1인 count 잠금을 우회해 동료를 추가하지 않는다.||ia_shared_reference|S_YALE_CAMERA
73|composition_form|중앙 배치와 대칭축은 별도 요건이다.|주체의 화면 중심 위치, 요청된 좌우 대응 요소와 기준축.|중앙의 얼굴 하나만으로 배경·소품 대칭을 충족하지 않는다.|pc_pc27_component_1||S_COMPOSITION
74|reuse_atomic|삼분할은 구성 선택이며 모든 요소의 교점 배치 규칙이 아니다.|주된 의미 앵커를 선택한 삼분할 선·영역에 둔다.|원고·손·얼굴 전부를 교점으로 밀어 관계를 깨지 않는다.|rule_of_thirds||S_COMPOSITION
75|composition_relation|look room은 시선이 향한 쪽의 여백이다.|눈·얼굴 지향과 그 방향의 화면 가장자리 사이 공간.|머리 위 일반 여백이나 화면 반대편 빈 공간과 구별한다.||ia_look_room|S_COMPOSITION
76|composition_relation|여백은 주체와 주변 면의 시각적 비중 관계다.|주요 얼굴·손·자료와 덜 복잡한 주변 영역을 구분한다.|단색 배경만 허용하지 않는다. 여백 확대가 필수 자료를 제거하면 거절.|large_negative_space_top_area||S_NEGATIVE
77|reuse_atomic|화면 안의 물리 프레임과 그래픽 테두리를 나눈다.|문·창 등 구조 경계가 요청한 인물 또는 활동을 둘러싼다.|액자 효과·캡션 테두리를 물리 프레임으로 세지 않는다.|pc_pc20_component_1,pc_pc20_component_2||S_YALE_STAGE
78|composition_relation|유도선은 대상과의 연결이 중요하다.|책상 모서리·선반·팔 등의 선이 얼굴이나 지정 자료에 이어진다.|소실점·모든 선의 수렴을 강제하지 않는다.||ia_leading_reference|S_LINES
79|composition_relation|깊이 배치는 초점 선명도와 독립 축이다.|전경 손·중경 얼굴·후경 보드의 가림과 상대 크기 관계.|모든 층이 선명해야 한다는 deep-focus 요건을 자동 부착하지 않는다.||ia_deep_layers|S_YALE_STAGE
80|reuse_with_relation|딥 포커스는 여러 깊이의 필요한 세부가 읽히는 상태다.|필수 전경 손·중경 얼굴·후경 자료 각각의 가독성.|f/숫자나 deep-focus 문구만으로 픽셀 성공을 판정하지 않는다.|deep_focus,pe_deep_readability|ia_deep_layers|S_YALE_CAMERA
81|reuse_with_relation|얕은 초점은 특정 대상의 선명도와 다른 깊이의 흐림 관계다.|필수 손·얼굴·자료를 선택한 초점면에 모으거나 우선순위를 요청과 조정.|불가능한 깊이의 세 필수 대상을 동시에 razor sharp라고 강제하지 않는다.|shallow_depth,pe_shallow_falloff|ia_evidence_frame|S_YALE_CAMERA
82|temporal_defer|랙 포커스는 시간에 따라 초점 대상이 변하는 현상이다.|스틸은 시작 또는 끝의 한 초점 상태만 표현한다.|한 장의 깊은 초점이나 이중 초점을 rack-focus 성공으로 세지 않는다.||ia_deep_layers|S_YALE_CAMERA
83|authored_composition|얼굴–손–자료 삼각 배치는 이번 연출 제안이며 표준 학술 용어가 아니다.|세 의미 앵커가 구별되고 손·자료의 참조 관계가 삼각형 안에 유지된다.|단지 삼각형 모양만 만들고 펜과 문서를 끊으면 실패.|ctx_hand_object_face_triad|ia_face_hand_document|S_COMPOSITION
84|optical_relation|반사된 상과 유리 너머 투과된 대상을 분리한다.|유리 경계, 반사 얼굴의 원 소유자, 투과 문서와 공간 위치를 연결한다.|추가 실제 인물·무작위 이중 얼굴·읽히지 않는 자료로 대체하지 않는다.|window_reflection_layering,rb_glass_reflection_transmission_candidate|ia_reflection_reference|S_YALE_STAGE
85|reuse_with_relation|창광의 방향과 광원 크기는 다른 축이다.|창 쪽 얼굴·손·페이지에 일관된 밝기 변화가 나타난다.|창이 있다는 이유만으로 측면광·soft light를 모두 충족하지 않는다.|window_side_soft,lit_window_large_soft_source||S_YALE_STAGE
86|reuse_profile|어두운 쪽 뺨의 빛 삼각형과 코·뺨 그림자 연결이 핵심이다.|요청된 얼굴에 코 그림자와 뺨 그림자가 이어지며 작은 빛 영역이 남는다.|broad/short·45도 장비 위치·책략가 서사와 독립이다.||ia_rembrandt_reference|S_REMBRANDT
87|reuse_with_relation|로키는 낮은 필·높은 명암 대비를 중심으로 둔다.|그림자 영역을 유지하면서 필수 눈·손·자료의 일부 정보는 읽힌다.|저노출·완전 검정·야간 시간으로 자동 대체하지 않는다.|low_key||S_YALE_STAGE
88|reuse_with_relation|하이키는 밝은 저대비 조명 관계다.|밝은 배경·완만한 얼굴 명암·남아 있는 흰 종이 경계.|종이를 날리거나 성격·낙관성을 자동 추가하지 않는다.|high_key||S_YALE_STAGE
89|reuse_profile|화면 속 실제 광원과 주변 밝기 영역의 연결이 중요하다.|보이는 스탠드의 위치·방향이 얼굴·책상에 떨어지는 빛과 맞는다.|스탠드 소품만 있고 다른 쪽에서 빛이 오면 만족하지 않는다.|lit_practical_motivated_mixed_interior||S_YALE_STAGE
90|lighting_relation|화면의 발광과 얼굴·손의 방향·거리 관계를 둔다.|발광 화면 가까운 면에 빛이 닿고 화면 내용과 눈이 과도한 glare 없이 남는다.|코딩 소품·푸른 색보정만으로 화면광을 세지 않는다.||ia_screen_light|S_YALE_STAGE
91|reuse_with_relation|윤곽광은 가장자리 분리이며 전체 실루엣과 다르다.|머리·어깨 가장자리가 배경과 분리되고 필수 얼굴 정보는 별도 확보.|눈·손·문서가 완전히 어두우면 관련 장면 의무는 실패.|rim_light||S_YALE_STAGE
92|palette_choice|절제는 색 수·면적·강도의 선택이지 지능 지표가 아니다.|정한 소수 색과 한 강조색의 영역 배치를 제안한다.|architectural luxury 팔레트·차가운 피부·무채색 옷을 자동 추가하지 않는다.|||S_COMPOSITION
93|appearance_choice|안경의 프레임 형태·재질·착용 상태를 분리한다.|테·렌즈·브리지·다리가 연결되고 요청한 얼굴에 착용된다.|학력·지능·성적 지향·연령의 증거로 쓰지 않는다.|wireframe_round_glasses,y2kr_oval_glasses|ia_glasses_bridge|S_GEEK
94|garment_relation|셔츠와 니트는 두 의복 층의 경계 관계다.|니트 목둘레 밖의 셔츠 칼라, 소매 끝의 커프스, 각 층의 연속성.|니트 프린트나 교복 의무·단정한 성격으로 대체하지 않는다.||ia_shirt_knit_layers|S_YALE_STAGE
95|material_garment|트위드 직물과 팔꿈치 패치는 독립 요소다.|직물의 짜임을 읽을 수 있는 면과 팔꿈치 위치에 붙은 별도 패치.|모든 트위드가 헤링본·Harris산이라고 단정하지 않는다.||ia_elbow_patch|S_TWEED
96|appearance_choice|단색 하이넥은 선택적 스타일이다.|목을 둘러 올라가는 실제 의복 경계와 단색 몸판.|이지적 인상·성별·직업·신체 비율을 자동 부여하지 않는다.|||S_YALE_STAGE
97|document_trace|주석은 원문의 특정 위치와 연결되어야 한다.|원문 행의 밑줄·여백 주석·연결 표시가 같은 페이지에 대응.|무작위 낙서·글자 더미를 주석의 의미적 대응으로 세지 않는다.||ia_annotation_anchor|S_DARWIN
98|document_trace|교정 흔적은 지운 부분과 대체·삽입의 대응이다.|취소선·삽입 기호·바꿀 문구의 자리 관계를 단순하고 읽히게 둔다.|빨간 낙서의 양이 교정 정확성·완료를 증명하지 않는다.||ia_correction_anchor|S_SCORE
99|document_trace|비교표는 공유 기준과 대응 행이 필요하다.|두 대상 열·같은 행 기준·표시된 차이와 펜 참조.|열 제목과 값의 연결이 없는 그래프 벽을 분석으로 세지 않는다.||ia_comparison_matrix|S_SCATTER
100|document_trace|논리 보드는 글자 양보다 단계 간 연결이다.|전제·중간 단계·결론을 식별하고 화살표가 해당 노드에 닿는다.|임의 화살표·수식·정답성을 논리적 구조로 대체하지 않는다.||ia_structured_board|S_YALE_STAGE
101|tool_relation|자·캘리퍼·확대경은 각각 다른 사용 기하를 갖는다.|자의 눈금과 측정 선, 캘리퍼 양 턱과 물체, 확대경과 같은 대상의 확대상을 분리한다.|모든 도구를 동시에 넣지 않는다. 정밀도·실제 수치는 별도 근거 필요.||ia_ruler_measure,ia_caliper_measure,ia_magnifier_target|S_YALE_STAGE
102|document_trace|누적 작업은 버전·순서·변경점의 대응으로 만든다.|v1/v2/v3처럼 지정된 소수 초안과 같은 항목의 변경 표시.|잔·구겨진 종이의 수량을 천재·노력 시간의 증거로 쓰지 않는다.||ia_revision_sequence|S_DARWIN,S_SCORE
103|activity_bundle|정독은 읽기 대상·행위·주석의 연결로 구체화한다.|펼친 책 지지, 해당 행으로 향한 눈, 여백 주석과 펜.|책만 들기·엉뚱한 곳 응시·기존의 읽기 포즈 중복을 구별.|pv_book_read|ia_close_read|S_DARWIN
104|activity_bundle|판본 대조는 같은 구절의 두 버전 관계다.|두 페이지의 대응 문단, 차이를 표시한 메모, 가리키는 손.|무관한 두 책·서로 다른 기준의 문단은 실패.||ia_edition_compare|S_DARWIN
105|activity_bundle|교정 행위와 교정 흔적을 연결한다.|한 손의 페이지 지지, 다른 손 펜 끝의 실제 접촉, 수정 대상 행.|pen hover를 필기 접촉으로 세거나 필기 손을 두 개로 늘리지 않는다.||ia_proofread|S_YALE_STAGE
106|activity_bundle|유도는 전후 식의 의미적 연결이 필요하다.|x+3=7 → x=4 같은 간단한 검증 가능한 단계와 손의 참조.|무작위 수식의 양으로 유도·정답성을 세지 않는다.||ia_derivation|S_YALE_STAGE
107|activity_bundle|디버깅은 코드와 오류 위치·조사 상태의 연결이다.|같은 파일·행의 코드, traceback 표시, 조사 중인 변수 또는 줄.|코드 창만 있는 작업·트레이딩 차트·성공한 수정은 별도다.||ia_debugging|S_PYTHON_ERRORS,S_PDB
108|activity_bundle|분석 장면은 기록·축·선택 관측의 대응이 필요하다.|단위 있는 축, 같은 값의 원자료 행, 지정 이상점과 펜.|상관을 인과·미래 예측·금융 수익으로 일반화하지 않는다.||ia_data_analysis|S_SCATTER
109|activity_bundle|실험 관찰은 장치·관찰 지점·기록의 관계다.|하나의 명시 장치, 해당 눈금·상태, 시간/값 기록을 연결.|장치 군집·흰 가운만으로 실제 실험·과학자 직업을 판정하지 않는다.||ia_experiment_log|S_YALE_STAGE
110|activity_bundle|현장 측정은 장소의 같은 지점과 도면·기록을 연결한다.|명시 측정 선, 한 도구의 위치, 같은 지점 식별자가 있는 평면 기록.|추가 측량사를 자동 생성하지 않는다. 수치 정확성은 holdout으로 확인.||ia_field_measure|S_YALE_STAGE
111|activity_bundle|도면과 모형의 같은 구조를 비교한다.|2D 접합부 A와 3D 접합부 A, 그 부위를 가리키는 손.|멋진 모형과 무관한 청사진만 병치하면 실패.||ia_drawing_model|S_YALE_STAGE
112|activity_bundle|체스와 바둑의 보드·표기 규칙을 별도 변형으로 둔다.|체스 말은 8×8 칸, 바둑 돌은 교차점; 같은 국면의 기록을 참조.|체스 말을 교차점에 놓거나 실제 합법 국면·승패를 무근거 주장하지 않는다.||ia_chess_review,ia_go_review|S_CHESS,S_GO
113|activity_bundle|비교 감상은 같은 형식 요소를 비교하는 작업이다.|두 작품의 구도·색·선 중 지정 공통 요소와 메모의 참조.|유명 작품·고급 복장만으로 실제 안목을 판정하지 않는다.||ia_art_compare|S_ERASMUS,S_ARISTOTLE
114|activity_bundle|악보의 특정 마디와 분석 표지가 연결되어야 한다.|마디 식별자, 해당 음형, 그 범위의 주석과 가리키는 도구.|소리·연주 실력·임의 음표의 음악적 정확성은 스틸에서 보장하지 않는다.||ia_score_study|S_SCORE
115|activity_bundle|원문·번역문은 같은 구절의 대응 관계다.|짧은 source/target 행과 정해진 대응 표시.|두 언어 글자만 있으면 번역으로 세지 않는다. 번역 의미는 별도 검증.||ia_translation|S_YALE_STAGE
116|activity_bundle|학술 토론은 공유 근거와 두 해석의 관계로 구성한다.|기존에 요청된 두 인물, 공통 문단, 서로 다른 메모·지시 대상.|서로 마주보기만으로 논쟁·학자 직업·우열을 판정하지 않는다.||ia_shared_reference|S_GESTURE
117|activity_bundle|설명은 손·보드·듣는 대상의 참조 연결이다.|손 또는 펜이 가리키는 보드 노드와 요청된 청자의 방향.|teaching_at_blackboard만으로 논점 대응·실제 교직을 보장하지 않는다.|teaching_at_blackboard|ia_teaching_reference|S_GESTURE
118|activity_bundle|질문을 듣는 순간의 물리 종점을 선택한다.|낮춘 펜, 질문자를 향한 몸·시선, 공유 항목.|청각·질문 이해·동의의 실제 성공은 판정하지 않는다.||ia_listening_reference|S_GESTURE
119|activity_bundle|후속 질문은 앞 질문의 빈 단계와 연결된 연출이다.|공유 도식의 빈 단계와 그곳을 가리키는 손, 상대의 대응 위치.|완전한 소크라테스 방법·대화 전후를 한 스틸에서 주장하지 않는다.||ia_followup_question|S_GESTURE
120|activity_bundle|동료 검토는 초안의 같은 위치와 검토 의견의 대응이다.|초안 행 식별자와 리뷰 코멘트의 앵커, 지정된 작성자·검토자 역할.|의견의 옳음·실제 학술 동료평가 완료·직업을 판정하지 않는다.||ia_peer_review|S_DARWIN
121|setting_activity|야간 분위기와 실제 시각·노력의 지속을 분리한다.|어두운 창밖, 책상 광원, 읽히는 원고와 현재 작업.|정확한 시각·밤샘·근면함은 별도 요청 없이 추론하지 않는다.||ia_night_work|S_YALE_STAGE
122|temporal_context|산책 중 사유는 이동 서사와 현재 메모 작업을 분리한다.|정지한 보행 자세, 휴대 메모와 같은 항목의 참조.|걷기의 과거·생각의 내용·도시 지명을 자동 붙이지 않는다.||ia_walk_notes|S_YALE_CAMERA
123|historical_pending|문인·선비의 역사 맥락과 일반 붓 필기 기하를 나눈다.|종이에 닿은 붓끝, 펼친 책과 필사 행, 소매·먹 도구의 지정 관계.|이번 조사로 특정 시대·계층·복식 고증을 완료했다고 주장하지 않는다.||ia_brush_copy|S_YALE_STAGE
124|activity_bundle|자연 관찰은 표본의 형태와 스케치의 같은 특징을 잇는다.|잎맥·윤곽 등 지정한 관찰 특징과 종이 그림의 대응.|실제 자연학자 신분·종 분류 정답·채집 이력을 추론하지 않는다.||ia_naturalist_sketch|S_DARWIN
125|cultural_style|다크 아카데미아는 문서화된 문화·패션 맥락이다.|원한 어두운 학구 공간·선택한 고스/프레피 요소·실제 읽기 관계.|젊은 학생·유럽 학교·교복·2026 인기 순위를 강제하지 않는다.|dark_academia_study_tabletop|ia_dark_academia_scene|S_DARK
126|authored_style|밝은 학구풍은 원 대화의 연출 변형이다.|밝은 저대비 공간과 남아 있는 종이·노트의 작업 관계.|표준 분류나 Dark academia의 공식 반대 개념으로 주장하지 않는다.|light_academia_knit_layers|ia_light_study_scene|S_DARK
127|cultural_style|긱 시크의 패션 형태와 실제 지능·개발자 신분을 분리한다.|요청한 좁은 안경·셔츠·미니멀 의상에서 선택한다.|모든 프레임을 좁게 바꾸거나 원한 활동을 사무직으로 바꾸지 않는다.||ia_geek_frame_scene|S_GEEK
128|nonvisual_identity|sapiosexual은 매력·지향의 용어다. 시각 판별 클래스로 만들지 않는다.|명시된 성인 간 공동 독서·대화 모티프는 별도로 저작 가능.|안경·책·응시로 실제 성적 지향·동의를 판정하지 않는다.||ia_adult_shared_interest|S_SAPIO
129|adult_trope|성인 미디어 모티프와 실제 사서의 직업·외양을 분리한다.|요청한 성인·독서 활동·안경/의상 중 선택한 스타일의 결합.|노출·신체 비율·성적 동의·학생 외양을 자동 추가하지 않는다.||ia_adult_reading_style|S_OFFICE,S_GEEK
130|adult_style|office siren은 2024년 문서화된 패션 맥락이다.|요청한 성인과 좁은 안경·셔츠·슬림 의복 중 선택한 요소.|회사원·상하 관계·복종·노출·2026 유행 강도를 자동 추론하지 않는다.||ia_office_style|S_OFFICE
131|authored_adult_scene|지적 플러팅은 이번 장면 연출명이다.|명시 성인 간 공동 자료와 서로 향한 반응을 요청 범위 안에서 구성.|호감·욕망·동의·관계 이력을 픽셀에서 판정하지 않는다.||ia_adult_shared_interest|S_SAPIO
132|adult_style|독서 활동과 의상·관능 축을 각각 소유시킨다.|책·손·시선의 읽기 관계와 요청한 로브의 실제 층·경계를 함께 보존.|관능 후보가 책·손 역할을 지우거나 자동 탈의·노출을 추가하면 실패.||ia_adult_reading_style|S_YALE_STAGE
133|fiction_contrast|단정한 외양과 위험 흔적은 두 개의 독립 관찰 축이다.|정한 의상과 깨진 유리·얼룩 등 요청한 허구 흔적을 별개 소유자에 둔다.|흔적만으로 가해자·피해자·사건·유죄·폭력 욕망을 추론하지 않는다.||ia_neat_danger_contrast|S_YALE_STAGE
134|fiction_trope|mastermind는 허구의 역할이며 손끝 맞대기의 뜻이 아니다.|계획 노드와 연결 선 중 특정 경로를 참조하는 손.|손 포즈만으로 범죄·권력·실제 능력을 하드 활성화하지 않는다.|pv_steepled_fingers|ia_plan_reference|S_GESTURE
135|fiction_scene|심문 장면의 지적 대치와 강압 사건을 구별한다.|명시된 두 성인, 테이블 자료, 각자의 자료·응시·손 역할.|서늘한 조명·의자 배치만으로 고문·유죄·기억·범행을 판정하지 않는다.||ia_interrogation_reference|S_YALE_STAGE
136|fiction_trope|mad scientist는 허구 장르 명칭이며 진단 분류가 아니다.|명시 장치와 여러 가설 기록, 현재 지점에 연결된 손.|헝클어진 머리·가운·실험실을 정신질환·폭력성·실제 과학자 증거로 쓰지 않는다.||ia_fiction_experiment|S_YALE_STAGE
137|historical_scene|전쟁 상황실은 지도·기록을 비교하는 역사·허구 맥락이다.|같은 영역의 지도와 시점 표시 보고서, 일치 또는 불일치 항목의 참조.|실제 작전 능력·현재 전쟁 지휘·지도 최신성을 보장하지 않는다.||ia_warroom_reference|S_WARROOM
138|evidence_scene|증거 검토는 사진·식별자·포장의 동일 항목 연결이다.|서로 맞는 식별자와 봉인 포장·사진·검토 기록, 지정 손 역할.|모든 생물학적 증거를 투명 비닐에 넣지 않는다. 유죄·법적 적합성은 별도.||ia_evidence_compare|S_EVIDENCE
139|fiction_scene|감금 서사는 명시 요청에서 받고 철창 무늬와 독립시킨다.|요청한 제한 공간·장벽과 실제 책·손·읽기 시선의 관계.|줄무늬 그림자만으로 수감·피해 이력·범죄를 추론하지 않는다.|pv_book_read|ia_confined_read|S_YALE_STAGE
140|adult_art_scene|고전 누드는 성인 신체·조각/실제 인물·포즈를 별도 조건으로 둔다.|요청이 성인 누드를 명시할 때 지지된 접힌 자세와 몸의 연속성을 보존.|Thinker·classical만으로 옷 잠금을 풀지 않는다. 조각 참조와 살아 있는 성인을 분리한다.|pv_chin_support|ia_classical_contemplation|S_RODIN
''')

OWNERS = {
    'pose': 'photo_prompt_pose_vocabulary_extension.json',
    'portrait': 'photo_prompt_portrait_composition_extension.json',
    'light': 'photo_prompt_lighting_extension.json',
    'background': 'photo_prompt_realistic_background_extension.json',
    'clothing': 'photo_prompt_clothing_structure_extension.json',
    'accessory': 'photo_prompt_accessory_structure_extension.json',
    'activity': 'photo_prompt_intellectual_activity_extension.json',
    'adult': 'photo_prompt_contextual_appeal_extension.json',
    'fiction': 'photo_prompt_violence_crime_extension.json',
}
# Activity is a proposed new owner. Existing owners take local refinements;
# activity owns document-reference work, not faces, lighting or adult tone.
# Directed edges are research graph proposals, not new runtime relation enums.
UNIT_DEFS = rows('''
ia_pause_work|자료 옆의 정지된 손과 별도 시선 대상|action|pose|work_document rests on a stated surface~actor's hand remains connected to its lowered tool~the current gaze target is declared separately|actor>holds>tool~surface>supports>work_document~actor>looks_toward>declared_target|멈춘 순간의 배치. 생각 내용·지속 시간은 비시각.|pause beside an open document; 자료 곁에서 펜을 낮춘|S_YALE_STAGE
ia_reference_link|원 항목과 검토 표지의 참조 연결|action|activity|source item has a distinct local anchor~review mark corresponds to that same anchor~pointing or writing hand has one declared role|review_mark>refers_to>source_anchor~actor_hand>points_to>source_anchor|지식·판단의 옳음을 보장하지 않는다.|같은 항목의 근거를 검토; review a referenced item|S_DARWIN
ia_thinker_support|반대 허벅지로 이어지는 턱 지지|body_pose|pose|pelvis is supported by a low seat~torso folds forward relative to pelvis~one elbow rests on the opposite thigh~that arm's hand contacts the chin~feet have stated receiving surfaces|seat>supports>pelvis~opposite_thigh>supports>elbow~hand>contacts>chin|양측 방향은 요청 또는 참조에서 받는다. 누드·지능은 효과가 아니다.|반대 허벅지에 팔꿈치를 놓고 턱 괴기; cross-thigh chin support|S_RODIN
ia_pensive_support|반가 자세와 뺨 접촉|body_pose|pose|right foot rests on left knee in this specified variant~right fingertips contact right cheek~pelvis and other foot retain stated supports|left_knee>supports>right_foot~right_fingertips>contacts>right_cheek~seat>supports>pelvis|불교 도상 표지는 별도 프로파일/요청으로 묶는다.|오른발을 왼 무릎에 놓고 오른 뺨 짚기; pensive half-seated configuration|S_PENSIVE
ia_chin_cradle|엄지·검지의 분리된 턱·뺨 접촉|contact_point|pose|thumb contacts underside of chin~index finger contacts cheek~same arm's elbow rests on desk~hand wrist arm and head remain continuous|thumb>contacts>chin_underside~index>contacts>cheek~desk>supports>elbow|pv_chin_support의 좁은 변형으로 우선 통합 검토.|thumb under chin and index along cheek; 엄지로 턱 아래 받치기|S_FACS
ia_temple_local|관자놀이 국소 접촉과 다른 손 역할|contact_point|pose|specified fingertips touch the requested temple~other hand retains its explicitly assigned tool~face remains visible around the local contact|fingertips>contacts>temple~other_hand>holds>assigned_tool|두통·감정·필기 역할 추가는 없다.|관자놀이에 손끝 대기; fingertips at the temple|S_FACS
ia_crossarm_support|전완–팔꿈치–턱의 지지 사슬|contact_point|pose|lower forearm supports opposite elbow~supported arm's hand touches chin~two arms retain separate coherent wrist connections|lower_forearm>supports>opposite_elbow~supported_hand>contacts>chin|일반 팔짱 또는 두 손 턱 지지와 구별.|다른 팔에 팔꿈치를 받친 턱 괴기; cross-arm elbow support|S_RODIN
ia_wrist_behind_back|등 뒤의 한 손–반대 손목 접촉|hand_pose|pose|one hand grips the opposite wrist behind the torso~both arms connect to the declared actor~specified inspection object stays in front|one_hand>contacts>opposite_wrist~actor>looks_toward>inspection_object|손목을 잡지 않은 뒷짐은 이 변형을 만족하지 않는다.|등 뒤에서 반대 손목 잡기; wrist held behind the back|S_GESTURE
ia_reclined_support|등받이 지지와 낮춘 도구 손|body_pose|pose|back visibly rests against the chair back~pelvis is supported by seat~one tool hand is lowered without writing contact|chair_back>supports>back~seat>supports>pelvis~hand>holds>tool|졸림·무관심·생각은 시각 확정 항목이 아니다.|등받이에 등을 댄 채 펜을 낮춘; supported reclined posture|S_YALE_STAGE
ia_page_hold|지정 여백의 페이지 고정|hand_pose|activity|palm or thumb contacts a declared page margin~page remains attached to the open book~book rests on a stated support~requested passage remains unobscured|hand>presses>page_margin~page>part_of>book~surface>supports>book|손 위치·역할을 request/core에 결속한다.|엄지로 페이지 여백 누르기; hold the page margin|S_DARWIN
ia_page_turn_endpoint|책에 붙어 있는 들린 페이지 모서리|hand_pose|activity|thumb and index pinch one page corner~page bends away from adjacent page~page root remains attached to the book~hand wrist and page thickness stay coherent|fingers>pinch>page_corner~page_root>attached_to>book_spine|움직임의 전체 시간은 별도 매체 검증.|페이지 모서리를 집어 들기; raised page-turn endpoint|S_YALE_CAMERA
ia_pen_hover|펜 끝과 종이의 비접촉 간격|hand_pose|activity|hand grips one pen~pen tip has a visible small gap above paper~wrist or forearm has declared support|hand>holds>pen~pen_tip>separated_from>paper~surface>supports>wrist|필기 접촉 후보와 동시에 동일 손에 배정하지 않는다.|종이 위에 펜 끝을 띄운; pen poised above the page|S_YALE_STAGE
ia_glasses_removed|한 손에 들린 벗은 안경|hand_pose|activity|hand holds spectacles by a temple arm~bridge lenses and temple arms form one connected object~same spectacles are absent from face|hand>holds>spectacle_temple~spectacles>removed_from>face|기존 착용 안경 잠금과 충돌하면 선택 거절. 안경 디자인은 보존.|안경 다리를 잡아 벗어 든; removed spectacles in hand|S_GEEK
ia_glasses_bridge|착용 프레임 브리지에 닿은 손끝|contact_point|activity|spectacles remain worn on face~fingertip touches the bridge over the nose~lenses and temple arms retain connections|fingertip>contacts>spectacle_bridge~spectacles>worn_by>actor|안경 재질·색·형태와 손 위치의 효과를 분리.|코 위 안경 브리지 짚기; touch the spectacles bridge|S_GEEK
ia_over_glasses|프레임 위로 보이는 눈과 지정 시선|gaze_engagement|activity|worn frame sits lower than eye line~eyes are visible above upper rim~gaze points to one declared target|spectacle_rim>below>eyes~actor>looks_toward>declared_target|얼굴 연령·우월감·고개 상향을 필수로 만들지 않는다.|안경 윗선 너머로 자료 보기; gaze over the spectacles rim|S_GEEK
ia_deictic_reference|지시 끝과 문서 항목의 연결|relational_action|activity|one hand or held pointer supplies a clear direction endpoint~endpoint aligns to a specific document anchor~anchor is visible and not obscured|actor_hand>holds>optional_pointer~direction_endpoint>points_to>document_anchor|구체 지시 변형이다. 추상 지시와 시간적 비트는 추가 맥락.|도표의 A 항목을 가리키는; point to the specified diagram node|S_GESTURE
ia_iconic_span|손의 범위와 자료 속 실제 형상의 대응|relational_action|activity|two hands or one traced endpoint define a specific span~the span corresponds to a named object's width or route in the reference~hand owners remain explicit|hand_span>depicts>reference_shape~reference_shape>part_of>document|도상성을 양손 대칭으로 고정하지 않는다. 크기 정답은 별도.|자료의 폭을 두 손으로 나타내는; depict a concrete span|S_GESTURE
ia_metaphoric_options|추상 대안과 두 공간 위치의 대응|relational_action|activity|document explicitly labels two abstract alternatives~each hand position is assigned to one alternative~labels and positions remain distinguishable|left_position>represents>option_A~right_position>represents>option_B|은유적 의미는 문맥에 의존. 스틸 형상만으로 분류 불가.|A와 B를 두 손 위치에 나눈; spatialized alternatives|S_GESTURE
ia_open_palm_reference|열린 손바닥과 자료·상대의 참조|relational_action|activity|palm faces upward or toward the declared listener~elbow remains near the body~one requested shared referent remains visible|palm>oriented_toward>listener_or_referent~actor>refers_to>shared_item|손바닥 형태는 pv_palms_up를 재사용. 말 내용·동의는 별도.|자료를 향해 손바닥을 여는; open-palm reference gesture|S_GESTURE
ia_enumeration|손가락·논점 번호의 대응|relational_action|activity|declared hand shows a chosen number of fingers~other hand touches one enumerated finger if requested~numbered document items correspond to the chosen sequence|enumerated_finger>corresponds_to>numbered_item~other_hand>touches>enumerated_finger|손가락 수·손 소유자·논점 수를 각각 검증.|논점 1·2를 손가락으로 세는; enumerate document points|S_GESTURE
ia_gaze_reference|현재 시선과 특정 자료의 대응|gaze_target|activity|document has one requested target area~eyes orient toward that area~head direction can differ within a plausible eye rotation|actor_eyes>looks_toward>document_anchor|실제 읽기 이해·주의 지속·눈의 조절 초점거리는 주장하지 않는다.|지정 문단을 내려보는; gaze at the specified passage|S_EYE
ia_annotation_anchor|원문 행·여백 주석의 앵커|prop|activity|one short passage is identifiable~underline is on the requested source line~margin note has a visible link to that line~writing tool has a declared current role|underline>marks>source_line~margin_note>refers_to>source_line|가독 문구는 명시 text 요청 시 정확 검증. 일반 주석은 내용 진실까지 요구하지 않는다.|행과 연결된 여백 주석; anchored margin annotation|S_DARWIN
ia_correction_anchor|취소·삽입·대체의 위치 대응|prop|activity|crossed-out segment remains identifiable~replacement or insertion connects to its intended location~correction marks do not swallow the entire passage|replacement>replaces>crossed_segment~insertion_mark>points_to>insertion_location|수정 흔적과 실제 문장 정답을 구별.|같은 문구의 취소선과 대체어; anchored draft correction|S_SCORE
ia_comparison_matrix|같은 기준의 두 대상 비교표|prop|activity|two object columns have distinct headers~rows use common criterion labels~one difference is explicitly marked~pointer aligns to the marked cell|column_A>evaluated_by>common_criterion~column_B>evaluated_by>common_criterion~pointer>points_to>difference_cell|기준·셀·포인터 대응이 필수. 자료 없는 차트 장식과 구분.|동일 기준의 A/B 비교표; common-criteria comparison table|S_SCATTER
ia_structured_board|전제–중간 단계–결론의 보드|prop|activity|a few declared nodes are distinguishable~premise intermediate step and conclusion have clear order~arrow ends contact corresponding nodes~pointing target is declared|premise>connects_to>intermediate~intermediate>connects_to>conclusion~pointer>points_to>declared_node|논리 정답은 짧은 내용 fixture로 별도 검증. 복잡한 수식 벽은 대체 불가.|전제에서 결론으로 연결된 보드; linked reasoning diagram|S_YALE_STAGE
ia_revision_sequence|동일 항목의 소수 버전과 변경점|prop|activity|two or three versions have short ordered identifiers~each contains the same anchored section~one change can be traced across versions|version_1>precedes>version_2~change_note>refers_to>shared_section|버전 흔적은 시간의 길이·노력·능력을 증명하지 않는다.|v1과 v2의 같은 문단 수정; ordered document revisions|S_DARWIN,S_SCORE
ia_ruler_measure|자의 눈금과 측정 선|procedure_step|activity|ruler edge aligns with one declared dimension~scale origin is matched to one endpoint~other endpoint and its unit are identifiable|ruler_origin>aligned_with>endpoint_A~ruler_scale>measures>dimension_AB|실제 수치 정확성은 알려진 치수 fixture로 별도 검증.|자 끝을 측정 시작점에 맞춘; ruler aligned to a dimension|S_YALE_STAGE
ia_caliper_measure|캘리퍼 두 턱과 같은 물체 면|procedure_step|activity|caliper jaws remain connected to the sliding body~each jaw contacts an opposite face of one object~scale or readout corresponds to the selected dimension|jaw_A>contacts>object_face_A~jaw_B>contacts>object_face_B~readout>refers_to>dimension_AB|자의 변형이 아니다. 물체 관통·장식 접촉은 실패.|양쪽 면에 캘리퍼 턱을 댄; caliper jaw contact|S_YALE_STAGE
ia_magnifier_target|확대경과 같은 대상의 확대 영역|procedure_step|activity|hand holds magnifier by its handle~lens overlaps one target area from the camera's view~magnified features correspond to that same target~background is not a second unrelated object|hand>holds>magnifier_handle~lens>magnifies>target_area|실제 배율·진단은 별도. 확대경 뒤 이미지 일관성 필요.|잎맥 위 확대경; magnifier over the declared detail|S_YALE_STAGE
ia_close_read|페이지·주석·눈·손이 연결된 정독|action|activity|open book has coherent receiving support~eyes orient to one source line~annotation is anchored to that line~one hand holds page and other tool role is stated|support>supports>book~eyes>looks_toward>source_line~annotation>refers_to>source_line~holding_hand>presses>page_margin|읽기 포즈는 pv_book_read 재사용, 추가 가치는 참조 관계.|행을 보며 연결 주석을 읽는; read an anchored passage|S_DARWIN
ia_edition_compare|같은 문단의 두 판본 대조|action|activity|two editions show matching passage anchors~difference note names that anchor~hand or pointer targets the corresponding segment in one edition|edition_A_passage>corresponds_to>edition_B_passage~difference_note>refers_to>passage_pair~pointer>points_to>declared_segment|두 책 자체는 충분하지 않다. 양쪽 텍스트 정답은 fixture 필요.|같은 문단의 판본 차이 대조; compare corresponding editions|S_DARWIN
ia_proofread|받친 페이지와 수정 지점의 펜 접촉|action|activity|one hand fixes page margin~other hand grips a pen~pen tip contacts the specified correction site~cross-out or insertion targets the same passage|holding_hand>presses>page_margin~writing_hand>holds>pen~pen_tip>contacts>correction_site|hover와 contact를 같은 순간에 요구하지 않는다.|페이지를 누르고 지정 행을 교정; proofread at an anchored line|S_YALE_STAGE
ia_derivation|간단한 전후 식과 참조 손|action|activity|short equations form a correct declared transformation~arrow connects successive lines~one hand or pointer targets the current step~other hand support is stated|equation_1>transforms_to>equation_2~pointer>points_to>current_step|고급 수학 일반 정확성을 주장하지 않는다. 간단 fixture로 시작.|x+3=7에서 x=4로 이어지는; linked equation derivation|S_YALE_STAGE
ia_debugging|코드·오류 행·조사 상태의 연결|action|activity|one short source file and its traceback share filename and line anchor~selected code line matches error locus~current variable or stack inspection is visible~hand roles match screen interaction|traceback>refers_to>code_line~inspection>examines>declared_state~actor_hand>operates>input_device|실제 수정 성공은 별도. 스크린샷·개인 코드 입력은 요청된 fixture만.|오류가 가리킨 줄을 조사; inspect the traceback-linked line|S_PYTHON_ERRORS,S_PDB
ia_data_analysis|원자료 행·축·선택 점의 대응|action|activity|plot has declared x and y units~one source row supplies a known coordinate pair~marked plot point matches that row~pointer targets the same observation|plot_point>corresponds_to>source_row~axis_x>represents>variable_x~axis_y>represents>variable_y~pointer>points_to>plot_point|정확한 값·텍스트는 fixture. 분석 능력·인과·금융 성과는 효과 아님.|원자료의 같은 점을 그래프에서 확인; linked data observation|S_SCATTER
ia_experiment_log|장치 상태와 기록의 같은 관측|action|activity|one named apparatus has a designated observation site~log has one short time or sample identifier~recorded state matches that site~one hand role is observation or note-taking|log_entry>records>apparatus_state~apparatus_state>observed_at>named_site|작동 법칙·실험 안전·결과 정답은 장치별 추가 검증 필요.|장치 눈금과 같은 항목의 기록; apparatus-to-log observation|S_YALE_STAGE
ia_field_measure|현장 지점·측정 선·평면 기록|action|activity|one location anchor is named~one selected measuring tool aligns with declared endpoints~plan note repeats the same location identifier~actor count comes from request|tool>measures>site_dimension~plan_note>refers_to>site_anchor|구체 도구·단위 선택은 context에서 받는다. 측량 정확도 인증 아님.|현장 A 지점과 도면 A를 연결; linked field measurement|S_YALE_STAGE
ia_drawing_model|도면·모형의 동일 접합부|action|activity|2D drawing and 3D model identify the same local joint~pointer targets that joint~scale relation is stated without invented dimensions|drawing_joint>corresponds_to>model_joint~pointer>points_to>joint_pair|설계 강도·시공 가능성·실제 전문가 신분은 주장하지 않는다.|도면 A 접합부와 모형 A 비교; drawing-model correspondence|S_YALE_STAGE
ia_chess_review|체스 보드 칸과 기록의 같은 국면|action|activity|board has eight by eight alternating squares~pieces stand within declared squares~short recorded position anchor matches selected square~hand points without changing the declared position|piece>located_in>declared_square~record_anchor>corresponds_to>board_square~hand>points_to>selected_position|체스 합법 국면·승패까지 요구되면 외부 fixture 검증을 추가.|체스의 e4 칸과 기록 대조; review a referenced chess square|S_CHESS
ia_go_review|바둑 교차점과 기록의 같은 국면|action|activity|chosen board has a consistent line grid~stones center on intersections~record marks the same selected intersection~hand does not replace grid or extra stone identity|stone>located_on>intersection~record_anchor>corresponds_to>board_intersection~hand>points_to>selected_position|체스 칸과 구분. 지정 기보의 합법성·승패는 별도.|교차점의 돌과 기록 대조; review a referenced go intersection|S_GO
ia_art_compare|두 작품의 같은 형식 요소 대조|action|activity|two declared artworks remain distinct~one common formal feature is marked on each~comparison note links those two feature anchors|feature_A>compared_with>feature_B~note>refers_to>feature_pair|감상자의 능력·작품 진위·저작자 동일성을 추론하지 않는다.|두 그림의 같은 색 배치 비교; compare a declared visual feature|S_ERASMUS,S_ARISTOTLE
ia_score_study|악보 마디와 분석 표지|action|activity|short score excerpt has one clear bar identifier~analysis mark covers that bar's note figure~pointer targets the same bar~score page remains supported|analysis_mark>refers_to>bar_anchor~pointer>points_to>bar_anchor|음악적 정답은 사전 검증한 짧은 악보 fixture로 별도.|악보 2마디와 주석 연결; annotated score-bar study|S_SCORE
ia_translation|원문·번역문의 짧은 대응 행|action|activity|source and target passage anchors are distinct~one correct short fixture pair is supplied~alignment marks connect matching passages~tool targets current phrase|source_phrase>aligned_with>target_phrase~pointer>points_to>current_phrase|언어 의미·철자는 fixture 검증. 이국적 글자 장식은 불충분.|원문 한 행과 번역문 한 행 대조; aligned translation passages|S_YALE_STAGE
ia_shared_reference|기존 두 인물과 공통 근거의 다른 참조|relational_action|activity|requested two actors retain distinct hands and gaze targets~one shared document anchor stays visible~each interpretation or note attaches to the same source|actor_A>refers_to>shared_anchor~actor_B>refers_to>shared_anchor~note_A>interprets>shared_anchor~note_B>interprets>shared_anchor|1인 잠금에서는 거절. 토론의 실제 발화·우열·이해는 비시각.|같은 문단을 두 사람이 검토; discuss one shared passage|S_GESTURE
ia_teaching_reference|보드 노드·설명 손·청자의 참조 연결|relational_action|activity|board has one declared concept anchor~speaker's pointer targets it~already-requested listener turns toward the intended referent~actor count remains frozen|speaker_pointer>points_to>board_anchor~listener>looks_toward>declared_referent|청자를 추가할 권한은 이 후보에 없다. 강의 정답·직업은 별도.|보드 A 개념을 가리켜 설명; explain a board node|S_GESTURE
ia_listening_reference|낮춘 도구와 화자 지향의 현재 배치|relational_action|activity|listener's pen is lowered without writing~listener's torso or face turns toward the declared speaker~shared material retains one anchor~each hand has one role|listener>oriented_toward>speaker~listener_hand>holds>lowered_pen~speaker>refers_to>shared_anchor|경청·청력·이해의 실제 성공은 확정하지 않는다.|펜을 낮추고 질문자를 바라보는; current listening arrangement|S_GESTURE
ia_followup_question|빈 단계와 질문 손·상대의 연결|relational_action|activity|shared diagram has one explicitly incomplete step~questioner's pointer targets that step~requested partner and response area remain distinct|questioner_pointer>points_to>missing_step~partner>refers_to>same_step|발화 전후·대화 철학·관계 이력은 비시각.|빈 단계에 대해 되묻는 배치; question a missing step|S_GESTURE
ia_peer_review|초안과 리뷰 의견의 같은 위치|relational_action|activity|draft has a short line or section anchor~review comment refers to that anchor~writer and reviewer roles come from request~hands do not swap document ownership|review_comment>refers_to>draft_anchor~reviewer>points_to>comment~writer>looks_toward>draft_anchor|실제 피어리뷰 완료나 판정의 옳음은 효과가 아니다.|초안 2행과 검토 의견 연결; anchored peer review|S_DARWIN
ia_night_work|어두운 창밖·국소 광원·현재 작업|situation_context|activity|outside window appears darker than desk region~visible or declared lamp motivates local illumination~document and hand interaction remain readable|lamp>illuminates>work_surface~actor_hand>interacts_with>document|정확한 시각·밤샘·근면함은 추론하지 않는다.|어두운 창밖과 국소 책상 작업; night-work staging|S_YALE_STAGE
ia_walk_notes|휴대 메모와 멈춘 보행 자세|action|activity|actor stands with declared foot supports~one hand supports a small notebook~other hand's pen state is explicit~gaze target is current note or environment|hand>supports>notebook~feet>supported_by>ground~eyes>looks_toward>current_target|이전 걷기·생각의 전환은 연속매체로만 검증.|길에서 멈춰 메모를 보는; paused field-note arrangement|S_YALE_CAMERA
ia_brush_copy|붓끝·필사 행·원문 대응|action|activity|one hand holds brush with coherent grip~brush tip contacts requested paper location~source book passage corresponds to copied line~sleeve avoids impossible ink/tool intersections|hand>holds>brush~brush_tip>contacts>copy_location~copied_line>corresponds_to>source_passage|시대·계층·전통 복식 고증은 미완. 중립 필기 기하만 우선.|같은 구절을 붓으로 필사; brush-copying reference|S_YALE_STAGE
ia_naturalist_sketch|자연물 특징과 스케치의 대응|action|activity|declared specimen feature is visible~sketch repeats that same contour or vein pattern~one pointer or pencil targets the corresponding feature|sketch_feature>depicts>specimen_feature~pencil>points_to>feature_anchor|실제 종 판별·과학자 신분·채집 이력은 별도.|잎맥과 같은 형태의 스케치; specimen-sketch correspondence|S_DARWIN
ia_evidence_frame|필수 얼굴·손·자료의 크롭·초점 보존|composition|portrait|required face area is visible~hand-object contact remains in frame~document anchor remains large enough to inspect~focus priority respects actual depth arrangement|crop>includes>required_face~crop>includes>hand_contact~focus_priority>preserves>document_anchor|장면 전체와 얼굴 타이트 크롭이 불가능하면 충돌 보고. 카메라 잠금 우회 금지.|얼굴·손 접점·자료를 함께 남긴; preserve required visual anchors|S_YALE_CAMERA
ia_ots_reference|전경 어깨와 작업 주체·자료의 소유 분리|composition|portrait|foreground shoulder belongs to an already-requested actor~main actor remains beyond that shoulder~shared material has its own anchor~occlusion does not erase required hand contact|foreground_actor>owns>foreground_shoulder~shoulder>foreground_of>main_actor~main_actor>refers_to>document|OTS의 기존 원자는 재사용. count·gaze·crop 효과를 축소 신고하지 않는다.|기존 동료 어깨 너머 같은 문서; over-shoulder shared reference|S_YALE_CAMERA
ia_pov_work|눈 위치 부근의 시점과 같은 인물 손|viewer_position|portrait|camera position approximates declared viewpoint owner~visible foreground hands belong to that owner~work surface lies within plausible downward view|camera>approximates_view_of>viewpoint_owner~foreground_hands>owned_by>viewpoint_owner~hands>interact_with>document|관찰자 얼굴 추가나 역할 교체는 효과가 아니다.|자기 눈 위치에서 보는 손과 자료; viewpoint-owned work view|S_YALE_CAMERA
ia_look_room|시선 방향과 같은 쪽 화면 여백|composition|portrait|current gaze direction is declared~space remains between face and frame edge in that direction~required document is not cropped by the spacing choice|gaze_direction>toward>look_space~look_space>between>face_and_frame_edge|시선 잠금과 반대 방향 여백은 거절 또는 별도 구성.|시선이 향한 쪽 여백; gaze-side look room|S_COMPOSITION
ia_leading_reference|선형 요소와 의미 앵커의 연결|composition|portrait|one or more scene-owned lines lead toward a declared anchor~anchor remains visible~line source retains plausible scene geometry|scene_line>leads_toward>meaning_anchor|무작위 선·소실점 자체를 성공으로 세지 않는다.|책상 선이 자료로 이어지는; lines toward the reference|S_LINES
ia_deep_layers|여러 깊이의 소유자·가림·가독성|composition|portrait|foreground middle and background roles are explicit~occlusion boundaries follow their depth order~required details have a separately declared focus rule|foreground>in_front_of>middle~middle>in_front_of>background~focus_rule>applies_to>required_anchors|deep space와 deep focus를 하나로 합치지 않는다.|손·얼굴·보드의 깊이 배치; owned depth layers|S_YALE_STAGE,S_YALE_CAMERA
ia_face_hand_document|얼굴·손·자료의 삼각 관계 구성|composition|portrait|face hand contact and source anchor remain distinct~their spatial locations form a deliberate triangle~hand still refers to the correct source anchor|face>spatially_linked_to>hand_contact~hand_contact>refers_to>source_anchor~source_anchor>spatially_linked_to>face|저작된 구성명이다. 기존 ctx_hand_object_face_triad와 의미 중복을 비교.|얼굴–손–문서 삼각 배치; face-hand-document arrangement|S_COMPOSITION
ia_reflection_reference|반사 얼굴·투과 자료·유리 경계|reflection_logic|background|glass boundary or plane is identifiable~reflected face has one declared real owner~transmitted document remains located beyond glass~reflection and transmission respect plane geometry|reflection>image_of>actor~glass>reflects>actor~glass>transmits_view_of>document|추가 실제 인물·무작위 복제 얼굴·계획 없는 이중 노출은 실패.|유리 반사 얼굴과 너머 자료; owned reflection-transmission layers|S_YALE_STAGE
ia_rembrandt_reference|기존 뺨 삼각형 프로파일의 작업 장면 적용|lighting|light|existing Rembrandt profile owns cheek-light triangle~nose and cheek shadows join~requested eyes hands and document remain separately readable|nose_shadow>joins>cheek_shadow~cheek_triangle>on>shadow_side_cheek|새 Rembrandt ID를 만들지 않고 기존 프로파일과 작업 가독성 조합.|자료를 읽히게 남긴 렘브란트 얼굴광; Rembrandt work-scene readability|S_REMBRANDT
ia_screen_light|화면 위치와 얼굴·손 밝기의 대응|lighting|light|one declared screen is emissive~near facing face and hand surfaces receive plausible illumination~required eyes and screen content retain readability|screen>illuminates>facing_face_plane~screen>illuminates>near_hand~glare_control>preserves>required_detail|푸른 색보정은 화면 발광의 대체 증거가 아니다.|화면이 가까운 얼굴과 손을 비추는; screen-owned illumination|S_YALE_STAGE
ia_shirt_knit_layers|셔츠 칼라·커프스와 니트 층의 경계|garment_detail|clothing|shirt collar emerges outside knit neckline~shirt cuffs emerge from knit sleeve ends if requested~each garment has continuous boundaries|shirt_collar>outside>knit_neckline~shirt_cuff>beyond>knit_sleeve|색·재질·성별·직업 잠금을 보존. 커프스는 요청한 변형에만 필수.|니트 밖 셔츠 칼라와 커프스; shirt-knit layer boundaries|S_YALE_STAGE
ia_elbow_patch|팔꿈치에 붙은 별도 패치|garment_detail|clothing|patch lies on the requested elbow region~patch perimeter attaches to the sleeve surface~sleeve bends coherently with the arm|patch>attached_to>sleeve_elbow~sleeve>follows>arm_bend|트위드 직물·패치·학구 서사를 별도 축으로 둔다.|소매 팔꿈치의 패치; elbow-owned sleeve patch|S_TWEED
ia_dark_academia_scene|요청한 다크 아카데미아와 읽기 관계|situation_context|activity|requested dark scholarly setting remains specific~chosen wardrobe or furniture elements stay optional~book hand and gaze reference remain linked|actor>interacts_with>book~book>located_in>requested_setting|주제명만으로 모든 소품·교복·국적을 강제하지 않는다.|다크 아카데미아에서 주석을 읽는; dark-academia reference scene|S_DARK
ia_light_study_scene|밝은 학구풍의 작업 관계|situation_context|activity|bright low-contrast setting preserves paper edges~requested reading or writing contact remains visible~light wardrobe choices stay independent|illumination>preserves>paper_detail~actor_hand>interacts_with>document|원 대화의 연출 변형. 정식 문화 분류로 노출하지 않는다.|밝은 서재의 주석 작업; bright scholarly staging|S_DARK,S_YALE_STAGE
ia_geek_frame_scene|요청한 긱 시크 프레임과 활동의 분리|wearable_accessory|accessory|selected eyewear keeps specified narrow or geometric frame~spectacles have coherent bridge and temple support~requested activity remains separately grounded|spectacles>worn_by>actor~actor_hand>interacts_with>requested_work|기본 안경 원자 재사용 우선. 성인·관능 효과를 요청 없는 긱 시크에 추가하지 않는다.|선택한 긱 시크 안경 형태; chosen geek-chic frame|S_GEEK
ia_adult_shared_interest|명시 성인 간 공동 자료와 반응|relational_action|adult|two explicitly adult requested actors have distinct ownership~one shared passage anchors their activity~current reciprocal orientation comes from request~wardrobe and tone follow open axes only|actor_A>refers_to>shared_passage~actor_B>refers_to>shared_passage~actor_A>oriented_toward>actor_B|지향·동의·욕망·관계 이력의 픽셀 판정 금지. 실제 성인 관계는 요청에서 받는다.|성인 두 사람의 공동 독서 장면; adult shared-interest staging|S_SAPIO
ia_adult_reading_style|성인 독서 활동과 선택한 의상 축|situation_context|adult|explicit adult reads a supported book~hands and gaze retain their reading roles~chosen robe or other garment has coherent layers~tone additions require an open allowed scope|eyes>looks_toward>book~hand>supports>book~garment>worn_by>adult_actor|같은 활동의 일반·관능 변형 비교. 노출·체형·학생 외양을 자동 추가하지 않는다.|성인의 독서와 요청 의상; adult reading and wardrobe staging|S_YALE_STAGE,S_OFFICE
ia_office_style|성인 오피스 사이렌의 선택 요소|wardrobe_style|adult|requested adult styling uses selected frame shirt or fitted garment elements~each garment retains real boundaries~work activity is independently grounded if requested|spectacles>worn_by>adult_actor~garment>worn_by>adult_actor~hand>interacts_with>requested_document|2024년 문화 근거. 실제 회사원·권력 관계·노출 자동 부여 금지.|명시 성인의 오피스 사이렌 스타일; selected office-siren elements|S_OFFICE
ia_neat_danger_contrast|의상과 요청 위험 흔적의 소유 분리|concept_tension|fiction|requested neat garment remains distinct~one explicitly requested fictional trace has a declared surface or object owner~work reference stays readable|garment>worn_by>actor~trace>located_on>declared_surface~hand>refers_to>document|범행·가해자·피해자·동의의 해석은 요청 없이는 추가하지 않는다.|단정한 옷과 지정 허구 흔적; owned neat-danger contrast|S_YALE_STAGE
ia_plan_reference|계획 노드와 지정 경로 참조|action|activity|a small plan graph has identifiable nodes~one selected connection is visible~hand or pointer targets that connection~actor role comes from explicit narrative only|node_A>connects_to>node_B~pointer>points_to>selected_connection|mastermind·범죄·능력은 별도 허구 요청. steepled fingers 단독으로 활성화하지 않는다.|계획 A→B 경로를 가리키는; referenced plan connection|S_GESTURE
ia_interrogation_reference|명시 성인 두 역할과 같은 자료|situation_context|fiction|two explicitly adult requested roles remain distinct~table has one shared evidence anchor~each gaze and hand points to its declared target~lighting does not erase the anchor|actor_A>refers_to>evidence_anchor~actor_B>looks_toward>declared_target~table>supports>evidence_document|강압·고문·유죄는 별도 사건 요청. 공유 자료 토론과 혼동 경계를 둔다.|허구의 심문 자료 대치; fictional interrogation reference|S_YALE_STAGE
ia_fiction_experiment|허구 실험 가설과 관측 기록|situation_context|activity|one requested fictional apparatus anchors the scene~two or three hypothesis cards are distinguishable~current observation entry connects to apparatus state|hypothesis_card>refers_to>experiment_site~observation_log>records>apparatus_state|정신 건강 진단·실제 연구자 직업·위험한 실험 절차는 효과가 아니다.|허구 장치와 가설 기록 검토; fictional experiment review|S_YALE_STAGE
ia_warroom_reference|지도 영역·시점 보고서의 대응|situation_context|activity|one fictional or historical map region is identified~report uses the same region identifier and declared time~pointer targets a stated discrepancy or entry|report>refers_to>map_region~pointer>points_to>selected_entry~report_time>qualifies>report|역사 참고와 현재 사실·작전 정확성은 분리. 구체 전술은 생성 효과가 아니다.|지도 A구역과 같은 보고서 대조; map-report reference review|S_WARROOM
ia_evidence_compare|봉인 항목·사진·검토 기록의 식별자|procedure_step|activity|package photo and record share one short identifier~package seal remains coherent~material-specific packaging comes from a declared fixture~hands follow requested viewing or handling roles|photo>depicts>evidence_item~record>refers_to>evidence_id~package>contains>evidence_item~seal>closes>package|생물학적 증거 지침을 전체 법과학 규칙으로 확대하지 않는다. 실제 증거·법적 효력·유죄 판정은 없음.|E1 봉인 포장과 같은 사진·기록; matched evidence identifiers|S_EVIDENCE
ia_confined_read|명시 제한 공간과 읽기 접촉의 보존|situation_context|fiction|explicit fictional restricted setting has declared barrier geometry~book is supported within reachable space~hands and gaze still connect to the page|barrier>bounds>requested_space~surface>supports>book~eyes>looks_toward>page|줄무늬 그림자 단독에서 감금 서사를 활성화하지 않는다.|명시 감금 공간에서 읽는; confined reading staging|S_YALE_STAGE
ia_classical_contemplation|명시 성인·매체와 사유 포즈의 분리|body_pose|pose|adult status and nude or clothed choice come from request~live human or statue medium is declared~supported torso arm chin and feet retain continuity|seat>supports>pelvis~hand>contacts>chin~medium>qualifies>subject_representation|누드 요청·의상 잠금·조각/인물 참조를 동시에 확인. 자동 체형·노출 강도 추가 없음.|명시 성인 고전 사유 포즈; explicit adult classical contemplation|S_RODIN
''')

def csv(value):
    return [x for x in value.split(',') if x]

def make_units():
    mapped = {}
    for n, kind, meaning, observable, contrast, reuse, units, refs in DECISIONS:
        for uid in csv(units):
            mapped.setdefault(uid, []).append(int(n))
    result = []
    for uid, label, slot, owner, components, edge_spec, limit, positive, refs in UNIT_DEFS:
        edges = []
        for index, edge in enumerate(edge_spec.split('~'), 1):
            subject, predicate, obj = edge.split('>')
            edges.append(dict(id=f'{uid}_r{index}', subject=subject,
                              predicate=predicate, object=obj,
                              status='proposed_graph_not_runtime_enum'))
        dimensions = {
            'body_pose': ['pose'], 'contact_point': ['pose','relationship'],
            'hand_pose': ['pose','action'], 'gaze_engagement': ['expression','relationship'],
            'gaze_target': ['expression','relationship'], 'action': ['action','pose','relationship'],
            'relational_action': ['action','relationship'], 'prop': ['setting','text','relationship'],
            'procedure_step': ['action','relationship','setting'],
            'situation_context': ['setting','action','relationship'],
            'composition': ['composition','framing','camera'],
            'viewer_position': ['camera','framing','relationship'],
            'reflection_logic': ['setting','composition'], 'lighting': ['lighting'],
            'garment_detail': ['appearance','material'], 'wearable_accessory': ['appearance'],
            'wardrobe_style': ['appearance','style'], 'concept_tension': ['concept','setting'],
        }[slot]
        if uid == 'ia_classical_contemplation':
            dimensions = ['pose','body_geometry','appearance','sexual_tone','reference_use']
        elif uid in {'ia_adult_shared_interest','ia_adult_reading_style'}:
            dimensions += ['appearance','sexual_tone']
        elif uid == 'ia_office_style':
            dimensions += ['sexual_tone']
        result.append(dict(
            id=uid, label_ko=label, proposed_slot=slot,
            proposed_owner_file=OWNERS[owner], source_term_numbers=mapped.get(uid, []),
            status='PROPOSED_NOT_INTEGRATED', positive_query_forms=positive.split('; '),
            proposed_concept_units=components.split('~'), proposed_relations=edges,
            proposed_entity_roles=sorted({e['subject'] for e in edges} | {e['object'] for e in edges}),
            proposed_affected_dimensions=list(dict.fromkeys(dimensions)),
            effect_axes_status='UNVALIDATED_NONEXHAUSTIVE_REVIEW_HYPOTHESES',
            property_scope_status='must bind each role to grounded frozen-core targets, enumerate every actual effect and review dimension/target/property scopes; draft axes are not executable lock compatibility declarations',
            activation_policy='advisory after core freeze; concrete context-valid user/core assertion may become scoped required only after profile review; abstract mood alone does not force this recipe',
            claim_limits=[limit], source_ids=csv(refs),
            source_support='source supports term, general visual principle, historical example, or method as stated in SOURCES.json; this exact staging graph is an authored proposal',
            adoption_requirements=['reuse-or-extension review by slot/id', 'grounded actor/document/tool bindings',
                                   'polarity and contextual sense checks', 'actual dimension/target/property effects review',
                                   'candidate exposure then optional selection evidence', 'native-pixel all-of validation'],
        ))
    return result

def main():
    source = json.loads((HERE / 'SOURCE-KEYWORDS.json').read_text())
    inventory = json.loads((HERE / 'AUTHORING-INVENTORY.json').read_text())
    candidates = inventory.get('candidates', inventory.get('retained_candidates', []))
    profiles = inventory.get('profiles', inventory.get('retained_profiles', []))
    by_id = {}
    for entry in candidates:
        by_id.setdefault(entry['id'], []).append(entry)
    units = make_units()
    source_ids = {s['id'] for s in SOURCES}
    unit_ids = {u['id'] for u in units}
    entries = []
    for number, kind, meaning, observable, contrast, reuse, proposed, refs in DECISIONS:
        term = source['entries'][int(number)-1]
        assert term['number'] == int(number)
        assert set(csv(refs)) <= source_ids
        assert set(csv(proposed)) <= unit_ids
        assert set(csv(reuse)) <= by_id.keys(), (number, set(csv(reuse)) - by_id.keys())
        entries.append(dict(number=int(number), source_label=term['label'], decision=kind,
            meaning_correction=meaning, observable_proposal=observable,
            contrasts_and_claim_limits=[contrast], source_ids=csv(refs),
            source_support='lexical/method/historical/general principle; observable staging is a research proposal unless source explicitly describes that geometry',
            reuse=[dict(id=rid, records=[{k:e.get(k) for k in ['file','slot','ko','en','concept_units','relations','affected_dimensions','affected_properties']} for e in by_id[rid]]) for rid in csv(reuse)],
            proposed_unit_ids=csv(proposed), core_activation='no invented required recipe from a vague intellectual adjective',
            implementation_status='PLANNED_NOT_RUN', pixel_status='NOT_GENERATED_NOT_EVALUATED'))
    assert [e['number'] for e in entries] == list(range(1,141))
    assert len(unit_ids) == len(units)
    assert all(u['source_term_numbers'] for u in units)
    write('SOURCES.json', dict(schema_version='intellectual-research-sources/v1',
        accessed_date_kst='2026-10-05', boundary='Links and narrow source summaries. No source image dataset downloaded, no original source pixels scored. Search excerpts and failed opens are labelled explicitly.', sources=SOURCES))
    write('TERM-DECISIONS.json', dict(schema_version='intellectual-term-decisions/v1',
        status='RESEARCH_ONLY', source_count=len(entries), decisions=entries))
    write('CANDIDATE-DRAFTS.json', dict(schema_version='intellectual-candidate-proposals/v1',
        status='PROPOSED_NOT_INTEGRATED', candidate_count=len(units),
        boundary='Research proposal schema. Not photo-candidate-pack/v6, not an executable profile registry. Proposed owner, relation predicates and effects must be translated and reviewed against current contracts before integration.',
        proposed_new_owner='photo_prompt_intellectual_activity_extension.json: only if deduplication proves existing activity owners cannot absorb document-reference relations',
        candidates=units))
    p1={'ia_thinker_support','ia_pensive_support','ia_chin_cradle','ia_temple_local','ia_crossarm_support',
        'ia_wrist_behind_back','ia_reclined_support','ia_page_hold','ia_page_turn_endpoint','ia_pen_hover',
        'ia_glasses_removed','ia_glasses_bridge','ia_over_glasses','ia_evidence_frame','ia_ots_reference',
        'ia_pov_work','ia_look_room','ia_leading_reference','ia_deep_layers','ia_face_hand_document',
        'ia_reflection_reference','ia_rembrandt_reference','ia_screen_light','ia_shirt_knit_layers','ia_elbow_patch',
        'ia_gaze_reference','ia_deictic_reference','ia_geek_frame_scene'}
    p2={'ia_reference_link','ia_annotation_anchor','ia_correction_anchor','ia_comparison_matrix',
        'ia_structured_board','ia_revision_sequence','ia_ruler_measure','ia_caliper_measure','ia_magnifier_target'}
    p3={'ia_close_read','ia_edition_compare','ia_proofread','ia_derivation','ia_debugging','ia_data_analysis',
        'ia_shared_reference','ia_peer_review','ia_listening_reference','ia_followup_question'}
    adoption=[]
    for u in units:
        uid=u['id']
        reuse={r['id'] for e in entries if e['number'] in u['source_term_numbers'] for r in e['reuse']}
        phase='P1' if uid in p1 else 'P2' if uid in p2 else 'P3' if uid in p3 else 'P4'
        notes=[]
        if uid=='ia_rembrandt_reference':
            notes.append('Reuse rembrandt_face_light_pattern; do not add a second Rembrandt profile.')
        if uid=='ia_pensive_support':
            notes.append('Neutral pose goes to pose owner; Buddhist iconography requires separately explicit religious context.')
        if uid=='ia_brush_copy':
            notes.append('Historical dress/period/material claim remains pending primary-source fixture verification.')
        if uid in {'ia_pause_work','ia_walk_notes'}:
            notes.append('Static endpoint only; temporal narrative is not a hard still-image gate.')
        if u['proposed_owner_file']==OWNERS['activity']:
            notes.append('New owner is conditional on deduplication against current activity/tool/document meanings.')
        adoption.append(dict(research_unit_id=uid,priority=phase,
            source_term_numbers=u['source_term_numbers'],proposed_slot=u['proposed_slot'],
            proposed_owner_file=u['proposed_owner_file'],reuse_candidate_ids=sorted(reuse),
            decision='reuse_or_extend_review' if reuse else 'new_relation_or_bundle_review',
            runtime_profile_plan='extend the actual owning registry or create the proposed activity registry only for a reviewed non-substitutable meaning; no one-to-one profile expansion',
            blocking_implementation_reviews=['semantic deduplication','complete actual property effects','grounded role binding','source/context eligibility','adopted stable runtime IDs'],
            notes=notes,status='PLANNED_NOT_IMPLEMENTED'))
    write('ADOPTION-MAP.json',dict(schema_version='intellectual-adoption-map/v1',
        scope='78 research units, not 78 approved runtime insertions',entries=adoption))
    # Retain verified references, not a 19 MB copy of the entire runtime corpus.
    needed = {r['id'] for e in entries for r in e['reuse']}
    retained = [e for e in candidates if e['id'] in needed]
    profile_keep = {'rembrandt_face_light_pattern','motivated_practical_mixed_interior_relation',
                    'blue_hour_ambient_practical_balance','rb_practical_pool','pv_profile_chin_support',
                    'pv_profile_figure_four','ae_profile_lip_press'}
    retained_profiles = [p for p in profiles if p['id'] in profile_keep]
    catalog = inventory.get('candidate_catalog') or [{k:e[k] for k in ['file','slot','id']} for e in candidates]
    profile_catalog = inventory.get('profile_catalog') or [{k:p[k] for k in ['file','id']} for p in profiles]
    write('AUTHORING-INVENTORY.json',dict(schema_version='intellectual-authored-inventory/v2',
        capture_boundary='Full identity catalogue plus the original captured bytes decoded for selected reuse references. Counts describe the audit snapshot, not live resolver exposure.',
        candidate_catalog=catalog, profile_catalog=profile_catalog,
        retained_candidates=retained, retained_profiles=retained_profiles))
    header = ['# 140개 용어의 연구 결정', '',
              '원 대화의 정의·연출 제안은 [SOURCE-KEYWORDS.json](SOURCE-KEYWORDS.json), 근거·한계는 [SOURCES.json](SOURCES.json), 기존 ID의 상세 효과는 [TERM-DECISIONS.json](TERM-DECISIONS.json)에 보존했다. 아래 관찰 형태는 고정된 분류 기준이 아니라 저작 제안이다.', '',
              '| 번호 | 용어 / 결정 | 의미 범위와 관찰 제안 | 혼동·주장 한계 | 재사용 / 초안 |',
              '|---|---|---|---|---|']
    for e in entries:
        refs = ', '.join(f'[{sid}]({next(s["url"] for s in SOURCES if s["id"]==sid)})' for sid in e['source_ids'])
        mapping = ', '.join([r['id'] for r in e['reuse']]+e['proposed_unit_ids']) or '선택적 기존 스타일 재사용; 새 하드 프로파일 없음'
        header.append(f'| {e["number"]} | **{e["source_label"]}**<br>{e["decision"]} | {e["meaning_correction"]}<br>제안: {e["observable_proposal"]}<br>{refs} | {e["contrasts_and_claim_limits"][0]} | {mapping} |')
    (HERE/'TERM-DECISIONS.md').write_text('\n'.join(header)+'\n')
    stats = dict(source_terms=len(entries), sources=len(SOURCES), proposed_units=len(units),
                 unique_reuse_candidate_ids=len(needed), retained_reuse_records=len(retained),
                 retained_profiles=len(retained_profiles), decisions=dict(Counter(e['decision'] for e in entries)),
                 runtime_status='NOT_INTEGRATED', image_status='NOT_GENERATED')
    write('PACKAGE-COUNTS.json',stats)
    print(json.dumps(stats,ensure_ascii=False))

if __name__=='__main__':
    main()
