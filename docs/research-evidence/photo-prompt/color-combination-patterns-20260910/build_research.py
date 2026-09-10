"""Build research-only records. Does not load or modify production registries."""
import hashlib
import json
import pathlib
import re
import subprocess
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[3]
ASSETS = REPO / 'skills/photo-prompt-image-generator/assets'

def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

# Claim summaries are bounded paraphrases. Record access limits explicitly.
SOURCE_ROWS = '''S01|CIE|Saturation, e-ILV 17-22-073|2020-12|https://cie.co.at/eilvterm/17-22-073|색채감의 자기 밝기 대비 속성|definition
S02|CIE|Chroma, e-ILV 17-22-074|2020-12|https://cie.co.at/eilvterm/17-22-074|동일 조명 기준 영역에 상대적인 색채감|definition
S03|CIE|Lightness, e-ILV 17-22-063|2020-12|https://cie.co.at/eilvterm/17-22-063|같은 조명 아래 흰 기준에 대한 상대 밝기|definition
S04|CIE|Correlated colour temperature, e-ILV 17-23-068|2020-12|https://cie.co.at/eilvterm/17-23-068|플랑크 궤적 근방의 광원에 사용하는 CCT와 적용 한계|definition
S05|CIE|Perceived colour, e-ILV 17-22-040|2020-12|https://www.cie.co.at/eilvterm/17-22-040|지각색은 주변·영역 구조·적응 등 관찰 조건에 의존|definition
S06|Adobe / Vanessa Eckstein|Color combinations in design|date_not_confirmed|https://helpx.adobe.com/in_hi/illustrator/how-to/experiment-with-color-combinations-hybrid.html|보색·유사색·삼색·단색을 별도 조합으로 다룸|practice
S07|Adobe / Hep Svadja|Color Your Spring with Adobe Color Gradients|2020-04-27|https://blog.adobe.com/en/publish/2020/04/27/color-your-spring-with-adobe-color-gradients|분할 보색·double split complementary·정방형 및 그라디언트 조절|practice
S08|ColorAide project|Color Harmonies|date_not_stated|https://facelessuser.github.io/coloraide/harmonies/|색공간 선택에 따른 조화 계산 차이와 삼색·사색의 구현상 구분|implementation_convention
S09|Adobe Express|The color wheel explained and how colors work together|2026-05-28|https://www.adobe.com/express/learn/blog/color-wheel-explained|RYB/RGB 구분만 제한적으로 사용. split-complementary와 triadic을 혼동한 본문은 채택하지 않음|source_conflict
S10|Josef and Anni Albers Foundation|Interaction of Color|date_not_stated|https://www.albersfoundation.org/alberses/teaching/interaction-of-color|같은 색도 주변 맥락에 따라 다르게 보이는 실험적 접근|artist_primary
S11|Karen B. Schloss and Stephen E. Palmer|Aesthetic response to color combinations: preference, harmony, and similarity|2011; online 2010-11-10|https://pubmed.ncbi.nlm.nih.gov/21264737/|색쌍 선호·조화·배경 위 도형색 선호는 다른 판단|research_abstract
S12|Karen B. Schloss and Stephen E. Palmer|The role of spatial organization in preference for color pairs|2011|https://pubmed.ncbi.nlm.nih.gov/22208128/|색쌍의 공간 배치를 독립적으로 다룬 연구. 상세 효과 크기는 인용하지 않음|research_abstract
S13|Kassandra R. Lee, Alex J. Richardson, Eric Walowit, Michael A. Crognale, Michael A. Webster|Predicting color matches from luminance matches|2020-02-14 online; 2020-04 issue|https://opg.optica.org/abstract.cfm?uri=josaa-37-4-A35|등휘도 설정은 관찰자별 감도 차이의 영향을 받음|research_abstract
S14|Sherwin-Williams|How to Build a Color Palette in 5 Simple Steps|date_not_confirmed|https://blog.sherwin-williams.com/color/color-guidance/how-to-build-a-color-palette-in-5-simple-steps/|실내 공간의 주조·보조·강조색에 60–30–10을 제안|domain_heuristic
S15|Adobe|View histograms and pixel values in Photoshop|2023-05-24|https://helpx.adobe.com/photoshop/using/viewing-histograms-pixel-values.html|하이키·로키·중간키는 톤 분포로 설명 가능|tool_documentation
S16|amaran|Controlling Devices, Desktop App|date_not_stated|https://help.amarancreators.com/en/amaran-desktop-app/controlling-devices|바이컬러의 CCT 제어와 RGB의 HSI 제어를 구별|manufacturer_documentation
S17|Adobe|Make color and tonal adjustments in Adobe Camera Raw|2026-08, day_not_confirmed|https://helpx.adobe.com/camera-raw/desktop/using/make-color-tonal-adjustments-camera.html|톤 구간별 그레이딩과 split-tone 결과|tool_documentation
S18|Adobe|Duotones|2022-09-14|https://helpx.adobe.com/uk/photoshop/using/duotones.html|회색조를 두 잉크로 재현하는 듀오톤과 잉크별 곡선|tool_documentation
S19|Adobe|Make selective color adjustments|2023-05-24|https://helpx.adobe.com/photoshop/using/mix-colors.html|선택한 색 성분 안의 프로세스색 비율을 조절하는 Selective Color|tool_documentation
S20|Adobe|Apply special color effects in Photoshop|2023-05-24|https://helpx.adobe.com/photoshop/using/applying-special-color-effects-images.html|Gradient Map은 회색조 범위를 지정 그라디언트의 색으로 매핑|tool_documentation
S21|Getty Museum Education|Landscapes, Classical to Modern Curriculum: Background Information|date_not_stated|https://www.getty.edu/education/for_teachers/curricula/landscapes/background2.html|대기원근의 거리별 색 강도·명암 대비 감소, 중첩·크기 단서|museum_education
S22|Vittorio Storaro / American Society of Cinematographers|Wonder Wheel: Who’s Afraid of Red, Green and Blue?|date_not_confirmed|https://theasc.com/article/whos-afraid-of-red-green-and-blue/|촬영감독이 특정 작품에서 서사와 색을 설계한 1차 사례|practitioner_account
S23|Lomography|What is cross processing?|date_not_confirmed|https://www.lomography.com/school/what-is-cross-processing-fa-bne2kolj|필름에 지정된 것과 다른 현상 공정을 사용하는 의미|manufacturer_education
S24|W3C CSS Working Group|CSS Color Module Level 4|2026-09-08 Candidate Recommendation Draft|https://www.w3.org/TR/2026/CRD-css-color-4-20260908/|sRGB/P3·선형광 변환·색공간·색상각 보간을 명시적으로 구분|technical_specification
S25|Adobe / Jonpaul Douglass interview|One Tool, Three Ways: HSL Panel in Lightroom Classic CC|2018-07-18|https://blog.adobe.com/en/publish/2018/07/18/one-tool-three-ways-hsl-panel-in-lightroom-classic-cc|사진가가 색면의 색을 맞추거나 대비시키는 실제 보정 사용 사례|practitioner_account
S26|Adobe|Color correction workflow in Premiere|2026-01-07|https://helpx.adobe.com/premiere/desktop/correct-color/color-correction-fundamentals/color-correction-workflow.html|샷간 색 일치·기본 보정·톤 구간 조정의 구별|tool_documentation
S27|Johannes Itten; editor Faber Birren; John Wiley and Sons|The Elements of Color|1970|https://books.google.com/books/about/The_Elements_of_Color.html?id=ofvRhNBgoCoC|목차에서 The Seven Color Contrasts 절 확인. 세부 본문 전체는 검토하지 않음|book_preview'''

sources = []
for line in SOURCE_ROWS.splitlines():
    sid, publisher, title, date, url, claim, kind = line.split('|')
    sources.append(dict(id=sid, publisher_or_author=publisher, title=title, publication_date=date,
                        url=url, accessed_at='2026-09-10', supported_claim=claim, source_type=kind,
                        access_scope=('indexed abstract; full-text access blocked or incomplete' if kind=='research_abstract' else 'bibliographic metadata and table of contents only' if kind=='book_preview' else 'relevant public page text'),
                        does_not_establish='image-generation reliability, universal beauty, or measured effects in natural photographs'))
write('sources.json', sources)

# Each row is a research family, not an activated runtime profile.
# id|axis|Korean name|source terms|observable components (semicolon separated)|false substitutes|literal proposal|sources|disposition
ROWS = '''monochromatic|hue|한 유채색군의 변주|Monochromatic|이름 붙인 유채색 영역들이 한 색상군에 머묾;영역 사이 명도나 채도 단계는 구별됨|흑백만 있음;전역 색광 워시로 표면 구별이 사라짐|Keep the named chromatic regions within one hue family, with readable lightness or chroma variation.|S06,S08|new_narrow
achromatic|hue|무채색 톤 구성|Achromatic|대상 범위의 유채색이 제거됨;흑색·회색·백색 사이 톤과 재질이 구별됨|세피아 단색;저채도지만 색이 남는 장면|Render the specified scope without chromatic hues while retaining its tonal and material distinctions.|S03,S15|new_narrow
analogous|hue|인접 색상군|Analogous|주요 유채색 영역들이 같은 색상환의 연속된 이웃 구간에 놓임;각 영역은 다른 색상군으로 구별됨|한 색의 밝기 변화만 있음;멀리 떨어진 포인트를 필수로 추가|Keep the principal chromatic regions in neighboring hue families on the declared wheel.|S06,S08|new_narrow
complementary|hue|대향 색상군|Complementary;Complementary Contrast|두 주요 색상군의 영역 소유자가 구별됨;선택한 색상환에서 서로 대향함|두 색이 다르기만 함;한쪽 색은 조명 번짐뿐임|Assign the two named regions opposing hue families on the declared wheel, retaining each region's boundary.|S06,S08|new_narrow
near_complementary|hue|보색 부근의 어긋남|Near-Complementary|두 영역은 넓은 색상 차를 유지함;한쪽이 선언된 보색 기준에서 약간 이동함|보색과 같은 프로필로 중복 집계;임의의 두 색|Offset one member of the declared opposing pair slightly while preserving a clear two-region hue contrast.|S08|parameter_variant
split_complementary|hue|기준색과 분할된 대향군|Split Complementary|기준 영역 하나와 대향 쪽 두 색상군이 구별됨;대향 쪽 두 색의 벌어짐이 각각 보임|삼색 균등 간격으로 치환;보색 한쪽만 존재|Use one base hue family and two distinct families flanking its opposite on the declared wheel.|S07,S08|new_narrow
triadic|hue|세 방향 색상군|Triadic|세 주요 유채색군이 각각 영역에 귀속됨;선택한 색상환에서 세 방향 간격이 대체로 균등함|세 개 물체지만 색상군은 둘;분할 보색으로 대체|Place three distinguishable hue families approximately evenly around the declared wheel and assign each to a named region.|S06,S08|new_narrow
tetradic|hue|두 보색쌍의 사색 관계|Tetradic;Double Complementary;Rectangle Scheme|네 색상군을 두 대향쌍으로 연결할 수 있음;각 색상군의 영역과 쌍 관계가 보존됨|Adobe double split complementary와 무조건 동일시;네 색이기만 함|Assign four hue families as two opposing pairs, recording whether the requested geometry is rectangular or square.|S07,S08|parameter_variant
square|hue|정방형 사색 관계|Square Scheme|네 주요 색상군이 구별됨;선택한 색상환의 네 방향 간격이 대체로 균등함|직사각형 사색을 같은 것으로 판정;세 색과 중성색 하나|Distribute four principal hue families approximately evenly around the declared wheel.|S07,S08|new_narrow
accented_analogous|hue|유사색 기반의 이탈 포인트|Accented Analogous|큰 기반 영역은 인접 색상군을 이룸;별도 작은 영역은 그 범위에서 떨어진 색상군임|기반부터 다색으로 분산;강조색이 기반만큼 큼|Use an analogous base field and a bounded accent outside that hue neighborhood.|S06,S14|new_narrow
limited_palette|hue|제한된 색상 자원|Limited Palette;Restricted Subject Palette;Restricted Background Palette|제한할 피사체 또는 배경 범위가 지정됨;그 범위의 주된 색상군 수나 범위가 제한됨|무조건 단색으로 바꿈;화면 전체 제한을 피사체만으로 대체|Restrict the principal hue families within the named scope, leaving other scopes as requested.|S06,S25|parameter_variant
polychromatic|hue|다색 구성|Polychromatic|다수의 구별 가능한 색상군이 지정 범위에서 함께 읽힘;그 색들이 여러 실제 영역에 귀속됨|고채도 한 색;작은 노이즈를 색상군으로 집계|Allow multiple clearly distinct hue families across the specified regions without imposing a fixed harmony scheme.|S05,S25|advisory
hue_contrast|hue|색상 차이 축|Hue Contrast|비교할 두 영역이 구별됨;명도나 채도만이 아닌 색상군 차이가 있음|명암만 강함;무조건 보색으로 확대|Keep a readable hue difference between the named regions independently of their lightness contrast.|S05,S06|parameter_variant
chroma_field|chroma|전체 채도 수준|High-Chroma Palette;Low-Chroma Palette;Muted Palette|조절할 범위가 명시됨;그 범위에 선명함 또는 억제된 색채감이 지속됨|밝기만 올림;암부로 묻어 색이 안 보임|Set the overall chroma level of the named field while retaining its requested hue and tonal structure.|S01,S02|parameter_variant
chroma_separation|chroma|영역간 채도 대비|Saturation / Chroma Contrast;Saturated Accent;Vivid-on-Muted;Muted-on-Vivid;Subject–Background Saturation Separation|비교 대상의 소유자가 분리됨;한쪽의 색채감이 다른 쪽보다 뚜렷이 강함|밝은 쪽을 고채도로 오인;배경도 함께 선명해짐|Give the named subject and environment a clear chroma hierarchy, in the requested direction.|S01,S02,S11|new_narrow
chroma_gradient|chroma|채도의 순차 변화|Chroma Gradient|변화의 공간 경로나 대상 순서가 있음;그 순서를 따라 채도 단계가 일관되게 변함|명도만 변함;랜덤한 색 점들의 나열|Vary chroma progressively along the specified path while holding the other requested color axes stable.|S02,S24|parameter_variant
chroma_distribution|chroma|색상군별 채도 배분|Uniform Saturation;Mixed Saturation;Soft-on-Soft|대상 색상군과 비교 기준이 지정됨;유사 채도 또는 차등 채도 배분이 여러 영역에서 확인됨|HSV 수치가 같으면 지각도 동일하다고 단정;soft를 흐림으로 대체|Distribute chroma consistently or unequally across the specified hue groups, preserving the requested tonal softness separately.|S01,S02,S03|parameter_variant
tonal_key|tone|명도 분포의 키|High-Key Palette;Low-Key Palette;Mid-Key Palette|밝은·어두운·중간 영역 중 요청한 범위가 화면 분포를 지배함;핵심 피사체의 필요한 계조는 남음|하이키를 클리핑으로 대체;로키를 전역 노출 부족으로 대체|Bias the image's tonal distribution toward the requested key while retaining the specified subject detail.|S15|reuse_existing
value_contrast|tone|영역간 명도 대비|Light–Dark / Value Contrast;High-Value Contrast;Low-Value Contrast|비교할 영역이 명확함;요청한 큰 또는 작은 밝고 어두움의 차이가 존재함|채도 차이만 있음;강한 그림자를 무조건 추가|Control the lightness difference between the named regions without changing their hue relationship unnecessarily.|S03,S15|parameter_variant
tonal_layering|tone|비슷한 톤의 층 구별|Tonal Harmony;Tone-on-Tone;Dark-on-Dark;Light-on-Light|비슷한 톤 또는 같은 색군의 영역이 겹치거나 이웃함;미세한 명도·색·질감 차이로 경계가 남음|검은 실루엣으로 합쳐짐;밝은 영역 전부 클리핑|Layer related tones while preserving small readable differences at the named boundaries.|S03,S15|new_narrow
equiluminance|tone|등휘도와 근사 밝기 일치|Isoluminant / Equiluminant Color|서로 다른 색상군을 비교할 영역이 정해짐;선언한 측정 색공간과 표시 조건에서 휘도 일치 여부를 확인함|같은 HSV V;그레이스케일처럼 보인다는 주관적 판정만 있음|For a photographic approximation, use different hues with closely matched displayed luminance; reserve exact equiluminance for calibrated testing.|S13,S24|measurement_only
simultaneous_contrast|perception|동일 자극과 주변색의 상호작용|Simultaneous Contrast|서로 다른 주변색 안의 비교 자극이 같은 표시색인지 확인됨;자극 차이와 구별된 주변 맥락 효과를 관찰 조건과 함께 평가함|두 자극 자체의 RGB가 다름;조명 차이로 실제 표면 표시색이 달라진 것을 지각 착시로 단정|Place matching displayed-color samples in different surrounds; evaluate the contextual perceptual effect separately from pixel equality.|S05,S10|measurement_only
role_hierarchy|area|주조·보조·강조의 역할 위계|Dominant–Secondary–Accent;Dominant Color;Supporting Color;Secondary Color;Accent Color;60–30–10 Rule;Extension / Proportion Contrast|주조 영역이 가장 넓고 보조 영역이 구별됨;강조 영역의 면적과 위치가 두 기반 영역에 종속됨|모든 색면을 같은 비중으로 배치;색목록만 있고 영역 소유자가 없음|Keep a large dominant field, a smaller supporting region, and a bounded accent, with proportions specified only when requested.|S14,S12|reuse_existing
single_accent|area|단일 강조 색상군|Single Color Accent;Achromatic + Accent;Chromatic Accent;Color Pop;Neutral Field / Chromatic Subject;Chromatic Field / Neutral Subject|기반의 중성 또는 저채도 성격이 분명함;강조할 색상군과 소유자가 제한됨|중성 기반과 저채도 기반을 무조건 같게 봄;단일 색상군을 단일 물체로 강제|Confine the principal chromatic accent to the named owner against the requested neutral or restrained base.|S02,S14|new_narrow
isolated_accent|spatial|공간적으로 고립된 포인트|Isolated Accent|포인트 영역이 따로 식별됨;주변에 경쟁 색 덩어리 없이 분리 공간이 남음|포인트 주변에 같은 색이 붙어 큰 덩어리가 됨;무조건 중앙 배치|Separate the bounded accent from competing chromatic regions with a readable surrounding interval.|S12,S14|new_narrow
micro_accent|area|작지만 읽히는 포인트|Micro Accent|강조 영역은 기반에 비해 작음;최종 출력과 썸네일 목표에서 요구한 표적은 식별 가능함|작아서 사라짐;큰 소품을 마이크로라 부름|Use a small localized chromatic accent that remains identifiable at the intended viewing size.|S05,S14|parameter_variant
accent_distribution|spatial|강조색의 군집과 분산|Accent Cluster;Scattered Accent;Clustered Color;Distributed Color|같은 역할의 색 요소들이 여러 개 있음;한정 영역 집중 또는 화면 분산이라는 요청한 배치가 보임|군집과 분산을 동시 의무화;색상 히스토그램만으로 판단|Place the accent elements in the requested cluster or dispersed arrangement, retaining each element's boundary.|S05,S12|parameter_variant
color_repetition|spatial|분리된 소유자 사이 색 반복|Repeated Accent;Color Echo;Color Repetition;Color Link|서로 떨어진 둘 이상의 영역이 구별됨;그 영역의 색상군이 시각적으로 연결됨|한 물체의 반사상만으로 별도 소유자 조건 충족;전역 워시|Repeat a recognizable hue family across distinct, separated scene elements.|S05,S12|new_narrow
color_rhythm|spatial|순서와 간격을 가진 반복|Color Rhythm;Alternating Color|색 요소의 순서가 읽힘;반복 또는 교대 간격이 구도의 방향을 이룸|두 개 색 점만으로 리듬 보장;무작위 산포|Repeat or alternate the named color regions along a readable sequence with visible intervals.|S05,S12|parameter_variant
color_anchor|attention|색의 초점과 균형점|Color Anchor;Chromatic Focal Point;Focal Color;Key Color;Highlight Color|의도한 시각 표적이 지정됨;그 표적의 색 대비가 주변과 구별됨|highlight를 무조건 밝은 톤으로 해석;면적 최대인 색을 무조건 시선 초점으로 간주|Use the named region as the chromatic focal cue while preserving its intended relation to surrounding areas.|S11,S12|advisory
color_bridge|spatial|두 색군 사이 연결 영역|Color Bridge;Transitional Color|서로 다른 두 색군의 영역이 있음;중간 색조를 가진 제삼의 연결 영역 또는 연속 경로가 있음|배경 어디든 중간색 한 점;단순 두 색 혼합|Place a visible intermediate-color region between the two named palette regions.|S07,S05|new_narrow
temperature_field|temperature|따뜻한·차가운 색 지배|Warm-Dominant;Cool-Dominant|대상 범위의 상대적 한난 경향이 읽힘;요청한 중성 예외나 반대 영역이 있으면 보존됨|특정 켈빈을 픽셀에서 역산;웜을 무조건 주황색 워시로 만듦|Make the specified field relatively warm or cool while retaining any named neutral exceptions.|S04,S05|advisory
temperature_separation|temperature|소유자별 한난 분리|Warm–Cool Contrast;Warm Subject / Cool Environment;Cool Subject / Warm Environment;Subject–Background Temperature Separation;Character–Environment Palette Contrast|피사체와 환경 등 비교 소유자가 구별됨;두 영역이 상대적으로 반대 한난 경향을 가짐|피부를 고정 주황색으로 만듦;전체 색조만 따뜻해짐|Separate the named owners by relative warm and cool color tendencies in the requested direction.|S04,S22|new_narrow
depth_temperature|temperature|깊이별 한난 배열|Warm Foreground / Cool Background;Cool Foreground / Warm Background;Temperature Gradient|전후경 또는 공간 방향이 독립 단서로 읽힘;그 경로를 따라 요청한 한난 순서가 존재함|평면 위 두 색 띠를 깊이 증거로 대체;먼 곳은 항상 파랑으로 고정|Arrange the requested warm–cool order across independently readable spatial planes or a named spatial path.|S21,S22|parameter_variant
mixed_illuminants|illumination|혼합 광원의 색 관계|Mixed Color Temperature|서로 다른 광원의 방향과 수광 영역이 구별됨;같은 재질 또는 중성 기준에서 두 조명 응답이 일관됨|명암 기반 split tone만 있음;전역 캐스트만 존재|Let distinct illuminants affect traceable receiving regions, with a declared white-balance anchor.|S04,S16|reuse_existing
tone_temperature|grading|명암 구간별 한난 배분|Warm Highlight / Cool Shadow;Cool Highlight / Warm Shadow;Shadow Tint;Midtone Tint;Highlight Tint|하이라이트·중간톤·암부의 대상 구간이 선언됨;그 구간에 요청한 색 경향이 존재함|좌우 두 색 조명을 무조건 같은 의미로 처리;전역 단색 틴트|Give the specified tonal bands distinct color tendencies with controlled transitions and named protected regions.|S17|parameter_variant
multicolor_lighting|illumination|여러 색광의 수광 관계|Bi-Color Lighting;Dual-Tone Lighting;Two-Color Lighting;Tri-Color Lighting;RGB Lighting;Gel Contrast|요청한 수의 색광 기여가 수광면에서 구별됨;빛의 방향·가림·겹침이 장면 표면과 연결됨|장비가 RGB라는 이유만으로 세 광원 판정;바이컬러 백색광 장비를 두 색 연출로 강제|Use separately traceable colored-light contributions on the specified receiving surfaces.|S16,S04|new_narrow
key_fill_color|illumination|주광·보조광의 색 역할|Colored Key + Neutral Fill;Neutral Key + Colored Fill|주광과 보조광의 역할이 형상과 그림자에서 구별됨;각 역할에 색 또는 중성 특성이 요청대로 귀속됨|중성 피부라는 말만 있음;두 광원의 역할이 반대|Assign the requested color to the key or fill contribution while keeping the other contribution relatively neutral.|S16|new_narrow
colored_rim|illumination|윤곽에 귀속된 색광|Colored Rim Light;Contrasting Rim Light|피사체 윤곽 일부에 색광이 존재함;그 색광이 후방 또는 측후방 수광 형상과 일치함|후광 그래픽;배경색 경계를 림광으로 오인|Keep the colored light on source-facing contours, with its hue distinct from the key when requested.|S16,S22|new_narrow
color_wash|illumination|범위를 가진 색광 워시|Color Wash;Background Color Wash|워시를 받을 공간이나 배경이 지정됨;그 범위에 색광이 넓게 이어지면서 가림을 따름|배경 페인트색만 있음;배경 한정을 무시하고 얼굴까지 워시|Wash the named receiving area with colored illumination, preserving requested spill boundaries.|S16|parameter_variant
cross_color_light|illumination|반대 방향의 서로 다른 색광|Cross-Color Lighting;Color Separation Lighting|분리된 방향 또는 수광 영역이 있음;그 영역별 다른 색광과 경계 전이가 읽힘|화면 위 색 필터 두 장;광원 방향 없는 착색|Let differently colored contributions arrive from distinct directions and follow the receiving forms and occlusions.|S16,S22|new_narrow
figure_ground|spatial|형태와 배경의 색 분리|Subject–Background Color Separation;Figure–Ground Color Contrast|피사체 외곽과 배경이 독립 영역으로 구별됨;요청한 색 차이가 주요 외곽을 따라 유지됨|흐림만으로 분리;배경 일부 작은 색 점|Maintain the requested color contrast along the subject–background boundary.|S11,S12|new_narrow
depth_palette|spatial|공간 층별 팔레트|Foreground–Midground–Background Palette;Layered Color Palette;Color Depth Separation|전경·중경·배경이 중첩·크기 등으로 구별됨;각 층의 색군 역할이 혼동되지 않음|색면 세 개만 있음;블러 단계만 존재|Assign distinct palette roles to independently readable foreground, middle, and background planes.|S21|new_narrow
atmospheric_color|spatial|거리 증가에 따른 색·대비 변화|Atmospheric Color Separation|원근 거리 순서가 다른 단서로 확인됨;먼 영역의 색 강도와 명암 대비가 대기 조건에 맞게 약화됨|전역 뿌연 필터;모든 원경을 무조건 파랑으로 변경|Let distant planes lose chroma and local tonal contrast relative to nearer planes, consistent with the depicted atmosphere.|S21|reuse_or_parameter
color_framing|spatial|색 영역의 둘러쌈|Color Framing|중심 표적과 주변 색 영역이 구별됨;색 영역이 두 면 이상 또는 요청한 윤곽을 따라 표적을 감쌈|색 소품 하나가 근처에 있음;후반 테두리를 자동 추가|Use the specified colored scene regions to surround or bracket the focal subject.|S05,S12|new_narrow
color_blocks|spatial|넓고 분리된 색면|Color Blocking;Large Color Fields|넓은 색면들이 각각 식별됨;색면 사이 경계가 구도에서 읽힘|잘게 쪼개진 다색 무늬;무조건 평면 포스터|Compose with large, clearly bounded color fields while retaining the requested photographic surface and depth cues.|S25|new_narrow
color_split|spatial|지정 방향의 색면 분할|Split Color Composition;Diagonal Color Split|주요 색 영역들이 큰 구획으로 나뉨;경계의 위치나 대각 방향이 요청과 일치함|split toning으로 치환;작은 대각 소품만 있음|Divide the main composition into the requested large color regions with a readable directional boundary.|S25|parameter_variant
color_bands|spatial|수평·수직 색 띠|Horizontal Color Bands;Vertical Color Bands|둘 이상의 길게 이어진 색 띠가 보임;띠의 방향과 순서가 명확함|줄무늬 의상만으로 전역 구도 충족;임의 색 점|Arrange the specified scope as ordered horizontal or vertical color bands.|S25|parameter_variant
radial_color|spatial|방사·동심 배열|Radial Color Arrangement;Concentric Color Structure|중심 또는 공통 축이 식별됨;방사 방향 또는 둘러싼 고리들의 색 순서가 보임|단순 중앙 포인트;원형 물체 하나|Arrange color regions as rays or nested surrounding zones around a visible shared center.|S05|parameter_variant
spatial_gradient|spatial|공간을 따른 연속 색 변화|Gradient;Ombré|변화하는 물체나 공간 경로가 지정됨;그 경로에서 색상·명도·채도의 선언된 축이 연속적으로 변함|Gradient Map과 동의어 처리;색 띠의 단절을 연속으로 판정|Change the specified color axis smoothly along the named surface or spatial path.|S07,S24|parameter_variant
color_zones|spatial|영역별 색 구획|Color Zoning|둘 이상의 의미 있는 공간 구역이 있음;각 구역의 색 역할과 경계가 유지됨|아무 다색 장면;영역 소유자 없는 팔레트|Assign stable palette roles to the named spatial zones, preserving their boundaries.|S05,S25|advisory
palette_complexity|complexity|피사체·배경 색상군 복잡도 차|Simple Background / Complex Subject Palette;Complex Background / Simple Subject Palette;Palette Density Contrast|피사체와 배경의 평가 범위가 분리됨;한쪽의 유효 색상군 다양성이 다른 쪽보다 큼|채도 높은 한 색을 복잡하다고 간주;질감 노이즈만 증가|Use more distinct hue families in one named scope and fewer in the other, independently of texture detail.|S05,S12|new_narrow
split_toning|grading|두 톤 구간의 색조 분리|Split Toning|주로 암부와 밝은 톤에 다른 색 경향이 있음;색 변화가 화면 좌표보다 톤 구간에 결부됨|좌우 색광만 있음;전역 한 색 틴트|Apply different color tendencies to shadows and highlights with an explicit transition policy.|S17|new_narrow
three_way_grade|grading|세 톤 구간의 독립 보정|Three-Way Color Grading|암부·중간톤·하이라이트 처리 방향이 각각 지정됨;구간 전이가 연속적이고 보호 대상이 유지됨|색광 세 개;반드시 세 개 서로 다른 Hue로 강제|Control shadows, midtones, and highlights separately; the three controls need not introduce three different hues.|S17|parameter_variant
duotone|grading|제한 색조의 톤 재해석|Duotone;Tritone|제한된 색조가 여러 원래 표면의 명암 구조를 재해석함;잔존 원색과 계조의 허용 범위가 선언됨|두 색 의상;두 색 조명|Use a declared two- or three-color tonal remapping treatment, with the intended treatment of original surface hues made explicit.|S18,S20|new_narrow
selective_retention|grading|국소 색 보존·억제|Selective Color;Partial Desaturation|남길 영역과 억제할 영역이 지정됨;경계·질감·동일 물체의 연결성이 유지됨|채도 높은 소품을 중성 배경에 둔 것만으로 편집 이력 단정;Photoshop Selective Color 조정과 무조건 동의어|Retain chroma in the selected region while suppressing it elsewhere, with continuous shading and texture across the mask boundary.|S19,S25|reuse_existing
global_tint|grading|범위 전체의 공통 색 편향|Global Tint;Color Cast Unification|전역 또는 지정 범위에 공통 색 편향이 있음;예외로 둔 중성 또는 제품 표면이 있으면 구별됨|한 색 물체만 많음;광원 원인을 단정|Apply a shared color bias within the declared scope, with explicit exceptions where requested.|S17,S26|parameter_variant
gradient_mapping|grading|톤값을 색으로 대응|Gradient Mapping|회색조 기준과 색 정지점 대응이 지정됨;떨어진 영역도 같은 톤 조건에서 같은 매핑 체계를 따름|왼쪽에서 오른쪽으로만 바뀌는 배경;후반 도구 사용 이력을 픽셀만으로 확정|Map the declared tonal range to a specified sequence of color stops rather than to screen position.|S20|new_narrow
cross_processed|grading|교차 현상풍 색·톤 관계|Cross-Processed Palette|어떤 색·톤 구간이 어떻게 이동하는지 지정됨;표면별 계조와 선택한 편향이 읽힘|녹색 캐스트 하나를 모든 교차 현상 표준으로 취급;생성 이미지로 실제 현상 이력 주장|Describe the requested channel or tonal color shifts explicitly, treating cross-processing as a look reference unless process metadata exists.|S23|advisory
discord|attention|의도한 색 불균형|Color Discord;Clashing Colors;Chromatic Tension;Unequal Color Balance;Off-Balance Palette;Abrupt Color Contrast;Controlled Discord|기반 색 관계와 이탈 또는 급변 영역을 구별할 수 있음;이탈의 면적·위치·색 차이가 선언됨|불쾌함·긴장감의 보편적 발생을 보장;임의 다색 혼란|Introduce the specified hue, chroma, area, or spatial imbalance relative to an otherwise readable palette structure.|S10,S11|advisory
palette_continuity|sequence|연속 장면의 색 관계 유지|Palette Continuity|둘 이상의 순서 있는 프레임이 있음;소유자별 색 관계가 장면 변화에도 유지됨|단일 이미지로 연속성 통과;전체 평균 RGB만 일치|Maintain the declared owner-to-color relationships across the ordered frames.|S26|sequence_only
palette_progression|sequence|시간에 따른 색 변화|Palette Progression;Color Arc|세 개 이상의 순서 있는 프레임 또는 시간 표본이 있음;지정 색 축의 변화 방향이 연속적으로 읽힘|한 장의 공간 그라디언트;사진 하나로 서사 변화 입증|Change the declared palette axis progressively across the ordered sequence.|S22,S26|sequence_only
palette_shift|sequence|사건 전후 색 체계 전환|Palette Shift|전환 전후 프레임과 사건 경계가 지정됨;그 경계에서 요청한 팔레트 관계가 바뀜|화이트밸런스 오류를 의도된 사건으로 추론;정지 사진 한 장|Change the declared palette relationship at the specified sequence boundary.|S22,S26|sequence_only
palette_inversion|sequence|전후 색 역할 반전|Palette Inversion|비교할 전후 프레임이 있음;같은 소유자들에 배정된 색 역할이 서로 뒤바뀜|RGB 음화 반전;장면 사이 무관한 색 변화|Swap the declared owner-to-color roles between the before and after frames.|S22,S26|sequence_only
color_motif|sequence|반복되는 색과 서사 대상|Color Motif;Signature Color|동일한 서사 대상 또는 주제가 외부 맥락으로 지정됨;여러 프레임에서 그 대상과 색군의 결합이 반복됨|한 이미지의 포인트색으로 고유 시그니처나 감정 단정;국적·성격 추론|Repeat the declared color association with the specified narrative referent across the sequence.|S22|sequence_only
color_coding|sequence|대상별 색 부호|Color Coding|둘 이상의 인물·장소·상황에 대응 규칙이 선언됨;각 대상이 해당 규칙에 맞는 색 관계를 반복 유지함|임의 색 옷으로 신분이나 역할 단정;명시한 대응표 없이 상징 주장|Maintain the explicitly declared color code for each named entity or setting.|S22,S26|sequence_only'''

records=[]
for line in ROWS.splitlines():
    rid,axis,ko,terms,components,rejects,positive,sids,disposition=line.split('|')
    parts=components.split(';')
    dims=['color']
    slot='color'
    if axis=='illumination': dims=['lighting','color'];slot='lighting'
    if axis in {'spatial','area','complexity','attention'}:dims=['color','composition']
    if axis=='grading':slot='color_grading'
    if axis=='sequence':slot=None
    records.append(dict(id='ccp_'+rid,axis=axis,name_ko=ko,source_terms=terms.split(';'),
        disposition=disposition,semantic_status='research_proposal',runtime_enabled=False,
        observable_components=parts,reject_substitutes=rejects.split(';'),
        candidate_proposal=dict(id='candidate_ccp_'+rid,proposed_slot=slot,
            affected_dimensions=dims,positive_literal=positive,open_slots=['actual hue choices','named region owners','requested strength'],
            retrieval_role='post_core_advisory',weight=None),
        activation_proposal=dict(exact_term_alone_sufficient=False,
            requester_evidence_required=['non-negated explicit visual request', 'intended scope and owners', 'compatible intent locks'],
            additional_required=['declared color wheel or qualitative interpretation'] if rid in {'complementary','near_complementary','split_complementary','triadic','tetradic','square','analogous'} else [],
            broad_label_policy='retrieve interpretations; do not introduce hidden hard obligations'),
        pixel_gate_proposals=[dict(id=f'ccp_{rid}_g{i+1}',condition=c,scale='sequence' if axis=='sequence' else 'thumbnail_and_native') for i,c in enumerate(parts)],
        qualification_status='unrendered_unqualified',source_ids=sids.split(','),
        evidence_boundary='Sources support the concept or adjacent design principle; region contracts and gates are authored proposals, not validated generator behavior.'))

lookup={r['id']:r for r in records}
# Broad figure/field contrast does not imply temperature or one accent hue.
for term in ['Neutral Field / Chromatic Subject','Chromatic Field / Neutral Subject']:
    lookup['ccp_single_accent']['source_terms'].remove(term)
    lookup['ccp_figure_ground']['source_terms'].append(term)
lookup['ccp_single_accent']['source_terms'].remove('Color Pop')
lookup['ccp_chroma_separation']['source_terms'].append('Color Pop')
lookup['ccp_temperature_separation']['source_terms'].remove('Character–Environment Palette Contrast')
lookup['ccp_figure_ground']['source_terms'].append('Character–Environment Palette Contrast')
lookup['ccp_figure_ground']['scope_warning']='Broad palette contrast permits multiple axes and hue families; do not force warm–cool separation or a single accent. Bind neutral/chromatic direction to the request.'
special={
 'ccp_tonal_key':['high_key_tonal_distribution','low_key_selective_illumination'],
 'ccp_mixed_illuminants':['mixed_illuminant_white_balance_relation'],
 'ccp_role_hierarchy':['palette_role_hierarchy_relation'],
 'ccp_selective_retention':['selective_color_same_surface_exception_relation'],
 'ccp_chroma_field':['muted','low_chroma_preserved_color_separation'],
 'ccp_achromatic':['monochrome'],
}
for rid,ids in special.items():lookup[rid]['existing_overlap_ids']=ids
direct_concepts={'monochromatic','analogous','complementary','split_complementary','triadic','tetradic','square','chroma_field','chroma_separation','tonal_key','value_contrast','equiluminance','simultaneous_contrast','mixed_illuminants','split_toning','three_way_grade','duotone','gradient_mapping','cross_processed','atmospheric_color','role_hierarchy'}
for r in records:
    r['source_support_level']='documented_definition_or_mechanism' if r['id'][4:] in direct_concepts else 'adjacent_principle_supports_authored_operationalization'
    r['term_standardization']='Do not treat descriptive workshop phrases as internationally standardized taxonomy; consult the disambiguation in report.md.'
    r['candidate_proposal']['open_slots_policy']='Potential authorial parameters only; bind to the actual request and do not reopen locked choices.'
lookup['ccp_tonal_key']['scope_warning']='Existing low-key profile requires selective illumination, which is narrower than a dark tonal distribution. Reuse only for matching meaning; keep mid-key and distribution-only low-key separate.'
lookup['ccp_selective_retention']['scope_warning']='Existing same-surface exception is narrower than keeping one entire object colored. Retain separate variants. Selective Color adjustment tool requires its own disambiguated interpretation.'
lookup['ccp_multicolor_lighting']['activation_proposal']['additional_required']=['explicit request for separate colored-light contributions, not merely a bi-color fixture']
lookup['ccp_equiluminance']['activation_proposal']['additional_required']=['declared display/profile/observer conditions; otherwise only near-luminance photographic approximation']
lookup['ccp_equiluminance']['pixel_gate_proposals'][1]['scale']='calibrated_measurement'
lookup['ccp_simultaneous_contrast']['pixel_gate_proposals'][0]['scale']='color_managed_pixel_measurement'
lookup['ccp_simultaneous_contrast']['pixel_gate_proposals'][1]['scale']='controlled_perceptual_review'
lookup['ccp_role_hierarchy']['candidate_proposal']['open_slots'] += ['area denominator','area ordering or explicitly requested ratios']
lookup['ccp_color_motif']['candidate_proposal']['open_slots'] += ['externally declared association; no universal color-emotion mapping']

write('candidate-research.json',dict(schema_version='photo-color-combination-research/v1',
    status='proposed_not_runtime_compatible', records=records,
    policy=dict(no_production_activation=True,no_fixed_hue_defaults=True,
                hard_profile_adoption='Only a separately reviewed observable meaning with requester support may later be promoted.',
                variants='Grouped terms are parameter variants or related senses, not interchangeable exact aliases.',
                source_grounding='Source-backed definitions and authored operational proposals are distinct.',
                color_owner_model=['surface_appearance','illumination','capture_white_balance','global_grade','regional_grade','tone_response'],
                color_relation_axes=['hue','lightness','chroma','relative_warm_cool','area','spatial_topology','tone_band','temporal_order'])))

coverage=[dict(term=t,research_family=r['id'],relationship='source_keyword_to_family_not_exact_alias',disposition=r['disposition']) for r in records for t in r['source_terms']]
write('keyword-coverage.json',dict(source_conversation_id='6aa0c013-97c8-83ee-a09f-39992239b0d9',
    extraction_method='Manual mapping of named English pattern terms in source sections 1–15; prose examples in section 16 are compositions, not additional primitives.',
    mappings=coverage))

BUNDLE_ROWS='''restrained_isolated_accent|chroma_separation,single_accent,isolated_accent|같은 기반과 강조 소유자를 세 후보에서 공유;기반 저채도·강조 고채도·고립 위치가 각각 유지|color,composition
analogous_with_remote_accent|analogous,accented_analogous,isolated_accent|유사색 조건은 기반에만 적용;이탈 포인트는 기반의 Hue 범위 조건에서 제외|color,composition
split_complementary_hierarchy|split_complementary,role_hierarchy|세 색군과 세 영역 역할을 대응;기하와 면적 비중은 별도 매개변수|color,composition
chromatic_monochrome_layers|monochromatic,tonal_layering|같은 유채색군의 영역 연결;미세한 톤 층을 흑백·흐림으로 대체하지 않음|color
repeated_accent_depth|color_repetition,depth_palette|반복 색이 나타나는 복수 소유자와 깊이 층을 연결;모든 층을 같은 색으로 칠할 의무 없음|color,composition
neutral_key_background_wash|key_fill_color,color_wash|중성 주광의 보호 수광 영역과 배경 워시를 분리;얼굴 색을 중성화하기 위해 물리적 색광을 지우지 않음|color,lighting
split_tone_surface_protection|split_toning,tonal_layering|암부·밝은 톤의 색 처리와 표면 층 구분이 함께 유지;색광 원인이나 실제 편집 도구는 주장하지 않음|color
large_fields_small_accent|color_blocks,single_accent,role_hierarchy|큰 기반 색면과 작은 강조 영역의 경계 연결;색면 수와 강조 색상군 수는 별도 관리|color,composition'''
bundles=[]
for row in BUNDLE_ROWS.splitlines():
    bid,families,relations,dimensions=row.split('|')
    members=['ccp_'+f for f in families.split(',')]
    assert all(m in lookup for m in members)
    bundles.append(dict(id='bundle_ccp_'+bid,member_family_ids=members,
        candidate_ids=[lookup[m]['candidate_proposal']['id'] for m in members],
        required_shared_bindings=relations.split(';'),affected_dimensions=dimensions.split(','),
        selection='optional_post_core',hard_profile_activation='never_from_bundle_selection_alone',
        hue_defaults=None,weight=None,status='research_template_not_runtime_compatible',
        pixel_status='not_rendered',conflict_policy='Check same owner, same scope, same axis and same time; respect all requester locks.'))
write('candidate-bundles.research.json',dict(schema_version='photo-color-combination-bundle-research/v1',bundles=bundles))

# Snapshot authored sources separately from generated indexes. Only read local data.
files=[ASSETS/'photo_prompt_tags.json',ASSETS/'photo_prompt_visual_obligations.json',
 ASSETS/'photo_prompt_reactorprompt_visual_relations_extension.json',ASSETS/'photo_prompt_lighting_extension.json',
 ASSETS/'photo_prompt_swimwear_extension.json',ASSETS/'photo_prompt_visual_obligations_swimwear.json',
 REPO/'skills/photo-prompt-image-generator/references/maintenance.md',
 REPO/'skills/photo-prompt-image-generator/scripts/prompt_generator.py']
tags=json.loads(files[0].read_text());registry=json.loads(files[1].read_text())
entry_lookup={}
for p in ASSETS.glob('photo_prompt*extension.json'):
    d=json.loads(p.read_text())
    for slot,rows in d.get('slots',{}).items():
        if isinstance(rows,list):
            for row in rows:
                if isinstance(row,dict) and row.get('id'):entry_lookup.setdefault(row['id'],[]).append(dict(file=str(p.relative_to(REPO)),slot=slot))
for slot,rows in tags['slots'].items():
    if isinstance(rows,list):
        for row in rows:
            if isinstance(row,dict) and row.get('id'):entry_lookup.setdefault(row['id'],[]).append(dict(file=str(files[0].relative_to(REPO)),slot=slot))
profile_ids={x['id'] for x in registry['profiles']}
aud=dict(audit_date='2026-09-10',head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
    counts={'base_color_slot':len(tags['slots']['color']),'base_color_grading_slot':len(tags['slots']['color_grading']),
            'base_film_emulation_slot':len(tags['slots']['film_emulation']),'base_registry_profiles':len(registry['profiles'])},
    count_scope='Base authored files only, not merged runtime totals or generated search indexes.',
    files=[dict(path=str(p.relative_to(REPO)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files],
    existing_overlap={k:[dict(id=i,base_profile=i in profile_ids,entry_locations=entry_lookup.get(i,[])) for i in ids] for k,ids in special.items()},
    observed_slot_dimensions={k:tags['candidate_semantic_policy']['slot_dimensions'].get(k) for k in ['color','color_grading','composition','lighting','light_intensity']},
    working_tree_scope='Pre-existing production changes were present. This research writes only its own evidence directory.')
write('local-audit.json',aud)

# Review fixtures are design data; no test runner or image model is executed.
CASE_ROWS='''monochromatic|동일 유채색군의 옷·벽·소품을 명도 차이로 나눈 사진|고대비 흑백 사진|색상군 변주와 무채색 분리
complementary|선언한 색상환의 보색을 피사체와 배경에 각각 배정|보색을 쓰지 않고 밝기 차이만 크게|부정어 우선 및 명도 대비와 구분
split_complementary|기준 의상색과 그 보색 양옆의 서로 다른 배경·소품색|세 색이 색상환에 균등 간격인 삼색 구성|분할 보색과 삼색 구분
triadic|서로 균등 간격인 세 색상군을 세 표면에 배정|세 물체를 두 색으로 칠함|물체 수와 색상군 수 분리
tetradic|선언한 색상환에서 두 보색쌍을 네 영역으로 배정|Adobe double split complementary 다섯 스와치|제품 명칭과 사색쌍 혼동 방지
single_accent|흑백 배경과 의상 속 소품 하나만 유채색|저채도이지만 모든 표면에 다른 색이 남음|무채색 기반과 저채도 기반 분리
isolated_accent|넓은 중성 공간 안에 혼자 떨어진 작은 색 소품|같은 색 소품 여러 개가 빽빽하게 둘러쌈|고립과 군집을 교환하지 않음
micro_accent|최종 크기에서 보이는 작은 색 핀 한 개|색 핀이 축소 시 사라짐|존재와 목표 크기 가독성 분리
role_hierarchy|주조·보조·강조의 큰·중간·작은 면적|세 색을 같은 넓이로 배치|면적 위계와 색 수 구분
chroma_separation|저채도 피사체와 고채도 배경|고채도 피사체와 저채도 배경|대상·배경의 방향 역전 검출
tonal_key|하이키이며 피사체 하이라이트의 질감이 남음|흰 배경인데 피사체는 암부 실루엣|전역 분포와 배경색 구분
tonal_layering|어두운 두 직물이 미세한 톤 차이로 구별|검은 한 덩어리로 합쳐진 실루엣|톤 층의 경계 보존
equiluminance|프로파일이 명시된 화면에서 두 영역의 상대 Y를 측정|HSV V가 같으므로 등휘도라고 주장|등휘도 측정 조건
color_repetition|의상·멀리 놓인 소품에 동일 색군이 반복|의상 전체에 한 색 워시가 번짐|복수 소유자와 전역 워시 구분
color_rhythm|일정 방향으로 두 색 영역이 교대|두 색 점이 무작위로 흩어짐|반복 순서와 분포 구분
color_bridge|서로 다른 색 벽 사이 연결 면이 중간 색조|중간색 소품이 화면 반대쪽에 무관하게 있음|연결 위치가 의미를 소유
temperature_separation|차가운 피사체와 따뜻한 환경|따뜻한 피사체와 차가운 환경|온도 분리 방향 역전 검출
mixed_illuminants|서로 다른 광원이 같은 재질에 방향별로 작용|암부·명부의 색만 바꾼 split toning|혼합광 원인과 출력 룩 구분
multicolor_lighting|양쪽 색광이 각각 수광면과 가림 경계를 따름|바이컬러 LED 한 대를 중성 백색으로 사용|장비명으로 두 색광 강제 금지
key_fill_color|중성 주광이 얼굴을 비추고 색 보조광은 암부에 제한|색 주광과 중성 보조광|광원 역할의 역전 검출
colored_rim|측후방 광원 방향에 맞는 좁은 색 윤곽광|주변에 그린 후광 그래픽|윤곽 수광과 그래픽 구분
color_wash|배경에만 색광을 넓게 비추고 얼굴은 별도 주광|피사체 얼굴까지 같은 색으로 워시|효과 범위 보존
depth_palette|중첩으로 구별되는 전경·중경·배경마다 색군 배정|평면에 그린 세 색 띠|색과 독립 깊이 단서
atmospheric_color|멀수록 대비와 색 강도가 약해지는 산 능선|전 화면에 동일 안개 필터|거리 순서가 있어야 함
color_blocks|큰 두 색면이 사진의 배경을 나눔|작은 다색 직물 무늬|색면 스케일 구별
spatial_gradient|벽의 왼쪽에서 오른쪽으로 색상이 연속 변화|같은 밝기 영역을 모두 같은 색으로 매핑|공간 함수와 톤 함수 구분
palette_complexity|여러 색 의상과 색상군이 제한된 배경|단색 고채도 의상과 다색 배경|색상군 복잡도 방향 검출
split_toning|암부와 밝은 톤에 다른 색조를 주는 보정|화면 왼쪽만 색 조명 하나|톤 구간과 공간 구간 구별
duotone|여러 표면을 두 색조의 톤 맵으로 재해석|두 색 의상을 입은 자연색 사진|두 색 물체와 재매핑 구별
selective_retention|동일 직물의 한 영역만 컬러이고 나머지는 흑백|Photoshop Selective Color로 녹색의 시안 성분 조절|선택 보존과 도구명 분리
gradient_mapping|명암값 순서에 세 색 정지점을 배정|좌우 그라디언트 배경|톤 대응과 공간 배경 분리
cross_processed|교차 현상풍으로 암부와 밝은 톤의 이동을 지정|녹색이면 실제 교차 현상 필름으로 판정|룩과 실제 공정 이력 분리
discord|유사색 기반의 한 구역에 의도한 강한 채도 이탈|부조화라는 이유로 불쾌감이 객관적으로 입증됨|시각 조건과 감정 판단 분리
palette_continuity|두 장면에서 같은 소유자별 색 관계가 유지|단일 사진 하나만 제공|시퀀스 최소 입력
palette_inversion|전후 두 프레임에서 두 대상의 색 역할이 바뀜|한 장을 RGB 음화 반전|역할 반전과 음화 구분
color_motif|명시된 대상과 색의 연결이 여러 프레임에서 반복|한 프레임의 색만으로 인물 성격 추론|서사 근거와 단일 픽셀 판단 분리'''
cases=[]
for i,line in enumerate(CASE_ROWS.splitlines(),1):
    rid,positive,negative,purpose=line.split('|')
    cases.append(dict(id=f'ccp_review_{i:03d}',family_id='ccp_'+rid,positive_query=positive,
                      adjacent_negative_or_mutation=negative,review_target=purpose,
                      expected='Recognize the positive visual sense; do not promote the mutation into that same sense.',
                      status='proposed_not_executed'))
write('regression-cases.json',cases)

src_ids={s['id'] for s in sources}
assert len(lookup)==len(records)
assert len({x['term'].casefold() for x in coverage})==len(coverage)
assert all(set(r['source_ids'])<=src_ids for r in records)
assert all(len(r['observable_components'])>=2 and len(r['reject_substitutes'])>=2 for r in records)
assert all(c['family_id'] in lookup for c in cases)
assert all(not r['runtime_enabled'] for r in records)
assert all(len(r['pixel_gate_proposals'])>=2 for r in records)
for rid,ids in special.items():
    for i in ids:assert i in entry_lookup or i in profile_ids, i
source=json.loads((ROOT/'source-conversation.json').read_text())
source_text='\n'.join(i.get('text','') for t in source['turns'] for i in t['items'])
assert all(x['term'].lower() in source_text.lower() for x in coverage), [x['term'] for x in coverage if x['term'].lower() not in source_text.lower()]
named_source_terms=[]
for line in source_text.split('# 16.')[0].splitlines():
    if line.startswith('### '):
        named_source_terms.append(line[4:].replace('**','').strip())
    elif line.startswith('- **'):
        named_source_terms.extend(re.findall(r'\*\*([^*]+)\*\*',line))
    elif line.startswith('|'):
        cells=[c.replace('**','').strip() for c in line.split('|')[1:-1]]
        if cells and re.match('[A-Za-z]',cells[0]):
            named_source_terms.append(re.split(r' / (?=[가-힣])',cells[0])[0])
        elif len(cells)>1 and re.match('[A-Za-z]',cells[1]) and not re.search('[가-힣]',cells[1]):
            named_source_terms.append(cells[1])
known_terms={x['term'].lower() for x in coverage}
assert all(t.lower() in known_terms for t in named_source_terms), [t for t in named_source_terms if t.lower() not in known_terms]
validation=dict(status='research_structure_pass',record_count=len(records),source_count=len(sources),
    mapped_keyword_count=len(coverage),proposed_regression_case_count=len(cases),bundle_template_count=len(bundles),
    counts_by_axis=dict(Counter(r['axis'] for r in records)),counts_by_disposition=dict(Counter(r['disposition'] for r in records)),
    checks=['JSON structure','unique IDs and keywords','source references resolve','mapped keywords present in full source conversation','all named source headings/bullets/table terms in sections 1–15 covered',
            'component and reject completeness','review fixtures reference records','bundle members reference records','existing overlap IDs found in current authored assets'],
    runtime_tests='not_run',embedding_rebuild='not_run',image_generation='not_run',pixel_review='not_run',user_judgment='pending')
write('validation.json',validation)

# Human-readable appendix from the same data prevents separate-table drift.
lines=['# 색 조합 패턴별 데이터 설계 부록','',
       '아래는 연구용 의미군과 시각 조건이다. 같은 행에 묶인 용어는 관련 변형이며 무조건 교환 가능한 exact alias가 아니다. 모든 게이트는 제안 상태이고 렌더 검증은 하지 않았다.','']
for r in records:
    lines += [f"## {r['id']} · {r['name_ko']}",'',
              f"용어: {', '.join(r['source_terms'])}", '',
              f"분류: `{r['axis']}` / `{r['disposition']}`. 후보 슬롯: `{r['candidate_proposal']['proposed_slot']}`.", '',
              '관찰 조건: '+' / '.join(r['observable_components'])+'.','',
              '혼동·대체 배제: '+' / '.join(r['reject_substitutes'])+'.','',
              '영문 제어 초안: '+r['candidate_proposal']['positive_literal'],'',
              '근거: '+', '.join(f"[{sid}]({next(s['url'] for s in sources if s['id']==sid)})" for sid in r['source_ids'])+
              '. 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.','']
    if 'scope_warning' in r:lines += ['기존 데이터와의 경계: '+r['scope_warning'],'']
(ROOT/'pattern-catalog.md').write_text('\n'.join(lines))
print(json.dumps(validation,ensure_ascii=False,indent=2))
