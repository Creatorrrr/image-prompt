"""Lexical and primary-source scope for one unchanged, proof-bound H-F2 query.

The structural role label and explicit comparison adjuncts provide conservative
witnesses for a bounded lexical correction. They are not discarded globally.
Photographic/scene context priors and epistemic constraints remain unchanged. This
never rewrites embedding input or authorizes adoption. Full-pool scores stay
intact; a bounded, source-witnessed material projection follows ranking.
Offsets address the original Unicode string. Unrecognized prose keeps ordinary
lexical behavior; quoted literal text is never a contrast operator.
"""
import hashlib
import json
import re
import math
import statistics
from functools import lru_cache

RECIPE = 'photo-h-f2-positive-query-scope/v1'
_FORMAT = re.compile(r'^Photographic(?P<label>[ \t]+role):[ \t]*', re.I | re.M)
_NEGATION = re.compile(r'\b(?:rather\s+than|instead\s+of)\b', re.I)
_CONTRAST = re.compile(r'(?:^|(?<=[,;\n]))[ \t]*(?:distinct|separate)\s+from\b', re.I)
_RESUME = re.compile(r'\b(?:but|however|whereas|while)\b', re.I)
_QUOTES = {'"': '"', "'": "'", '“': '”', '‘': '’', '`': '`'}


def _quoted(text):
    spans = []
    i = 0
    while i < len(text):
        char = text[i]
        if char not in _QUOTES or (char in "'‘" and i and text[i-1].isalnum()):
            i += 1
            continue
        end = i + 1
        while end < len(text):
            if text[end] == '\\':
                end += 2
            elif text[end] == _QUOTES[char]:
                break
            else:
                end += 1
        spans.append((i, min(end + 1, len(text))))
        i = min(end + 1, len(text))
    return spans


def analyze(text, tokenize):
    if not isinstance(text, str) or not text.strip():
        raise ValueError('nonempty query required')
    quotes = _quoted(text)
    literal = lambda pos: any(a <= pos < b for a, b in quotes)
    formats = [(m.start('label'), m.end()) for m in _FORMAT.finditer(text) if not literal(m.start())]
    excluded = []
    markers = sorted([*_NEGATION.finditer(text), *_CONTRAST.finditer(text)], key=lambda m: m.start())
    for match in markers:
        start = match.start()
        if literal(start) or any(a <= start < b for a, b in excluded):
            continue
        end = match.end()
        while end < len(text):
            if not literal(end):
                char = text[end]
                decimal = char == '.' and end > 0 and end + 1 < len(text) and text[end-1].isdigit() and text[end+1].isdigit()
                if char in ';\n!?' or (char == '.' and not decimal) or _RESUME.match(text, end):
                    break
            end += 1
        excluded.append((start, end))
    merged = []
    for start, end in sorted(formats + excluded):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    positive = []
    cursor = 0
    for start, end in merged:
        if cursor < start:
            positive.append((cursor, start))
        cursor = end
    if cursor < len(text):
        positive.append((cursor, len(text)))
    terms = sorted({term for start, end in positive for term in tokenize(text[start:end])})
    locators = lambda ranges: [{'start': a, 'end': b, 'quote': text[a:b]} for a, b in ranges]
    result = {'schema': RECIPE, 'input_sha256': hashlib.sha256(text.encode()).hexdigest(),
              'format_spans': locators(formats), 'contrast_spans': locators(excluded),
              'positive_spans': locators(positive), 'positive_terms': terms,
              'candidate_filter': False, 'embedding_input_changed': False}
    result['canonical_sha256'] = hashlib.sha256(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return result

# Only lexical evidence for explicit multiword counterparts is used here. This
# is not a general natural-language contradiction or native-eligibility test.
_CONNECTIVES = frozenset('a an the of from and or to its their it is as in on for with rather than instead distinct separate s'.split())
CORRECTION_RECIPE = 'photo-h-f2-single-winner-scope-correction/v1'

def counterpart_matches(analysis, document, tokenize):
    wanted = set()
    for row in analysis['contrast_spans']:
        words = [t for t in tokenize(row['quote']) if t not in _CONNECTIVES]
        wanted.update(zip(words, words[1:]))
    words = [(m.group().casefold(), m.start(), m.end()) for m in re.finditer(r'[^\W_]+', document, re.UNICODE)
             if m.group().casefold() not in _CONNECTIVES]
    matches = []
    protected = _quoted(document) + [(r['start'],r['end']) for r in analyze(document,tokenize)['contrast_spans']]
    for first, second in zip(words, words[1:]):
        if (first[0], second[0]) in wanted:
            start, end = first[1], second[2]
            if any(a<=start<b for a,b in protected):
                continue
            prior=document[:start]
            boundary=max(prior.rfind(c) for c in '.;!?\n')
            clause=prior[boundary+1:]
            clause=re.split(r'\b(?:but|however|whereas)\b',clause,flags=re.I)[-1]
            if re.search(r'\b(?:never|without|not(?!\s+only\b))\b',clause,re.I):
                continue
            # A quoted witness must normalize back to its claimed endpoints.
            actual = [t for t in tokenize(document[start:end]) if t not in _CONNECTIVES]
            if actual == [first[0], second[0]]:
                matches.append({'terms': actual, 'start': start, 'end': end, 'quote': document[start:end]})
    return matches


def correct(metadata, sparse, dense, analysis, tokenize, fuse, contributions, document, document_frequency):
    """One bounded query-term correction; all RIDs remain in ordinary RRF10.

    Contributions and document accept a known RID ordinal, never a new query.
    Search obtains them from its single posting traversal; audits verify only
    those identified RID witnesses against the sealed index, without searching.
    """
    positions = {row['id']: i for i, row in enumerate(metadata)}
    original = fuse(metadata, sparse, dense, 10)
    old = original[0]
    i = positions[old['id']]
    positive = set(analysis['positive_terms'])
    formatting = {t for row in analysis['format_spans'] for t in tokenize(row['quote'])} - positive
    contrast = {t for row in analysis['contrast_spans'] for t in tokenize(row['quote'])} - positive
    ignored = formatting | contrast
    known = {}
    def parts(k):
        if k not in known:
            known[k] = contributions(k)
            if not all(math.isfinite(v) and v>=0 for v in known[k].values()):
                raise ValueError('invalid lexical contribution evidence')
        return known[k]
    def removed(k, terms):
        return math.fsum(parts(k).get(t, 0.) for t in sorted(terms))
    def signal(k):
        return max(0., float(sparse[k]) - removed(k, ignored))
    before_matches = counterpart_matches(analysis, document(i), tokenize) if contrast else []
    content = positive - _CONNECTIVES - {'photographic', 'scene', 'context'}
    frequencies = {term: document_frequency(term) for term in content if document_frequency(term)>0}
    median_frequency = statistics.median(frequencies.values()) if frequencies else 0
    format_frequency = min((document_frequency(t) for t in formatting if parts(i).get(t,0)>0),default=0)
    attempts = []
    for kind, terms in [('contrast', ignored), ('format', formatting)]:
        if kind == 'contrast' and not before_matches:
            continue
        if kind == 'format' and old['dense_rank'] <= len(metadata)/2:
            continue
        decrease = removed(i, terms)
        if decrease <= 0:
            continue
        proposal = list(map(float, sparse))
        proposal[i] = max(0., proposal[i] - decrease)
        order = fuse(metadata, proposal, dense, 10)
        new = order[0]
        j = positions[new['id']]
        if i == j:
            attempts.append({'kind': kind, 'reason': 'winner_unchanged'})
            continue
        if signal(j) <= signal(i):
            attempts.append({'kind': kind, 'reason': 'no_strict_positive_support_gain'})
            continue
        if kind == 'contrast' and counterpart_matches(analysis, document(j), tokenize):
            attempts.append({'kind': kind, 'reason': 'replacement_also_matches_counterpart'})
            continue
        positive_matches = counterpart_matches({'contrast_spans': analysis['positive_spans']}, document(j), tokenize)
        if kind == 'contrast' and not positive_matches:
            attempts.append({'kind': kind, 'reason': 'no_positive_compound_witness'})
            continue
        if kind == 'format' and not (new['dense_rank'] <= len(metadata)/2 and float(dense[j]) > float(dense[i])):
            attempts.append({'kind': kind, 'reason': 'no_independent_semantic_agreement'})
            continue
        discriminative = sorted(t for t,df in frequencies.items() if df < format_frequency
                                and parts(j).get(t,0)>0 and parts(i).get(t,0)==0)
        if kind == 'format' and len(discriminative)<2:
            attempts.append({'kind': kind, 'reason': 'insufficient_new_discriminative_terms'})
            continue
        trace = {'schema': CORRECTION_RECIPE, 'applied': True, 'kind': kind,
                 'affected_id': old['id'], 'replacement_id': new['id'],
                 'original_bm25': float(sparse[i]), 'corrected_bm25': proposal[i],
                 'positive_support_before': signal(i), 'positive_support_after': signal(j),
                 'old_dense_rank': old['dense_rank'], 'new_dense_rank': new['dense_rank'],
                 'removed_contributions': {t: parts(i).get(t, 0.) for t in sorted(terms) if parts(i).get(t, 0.) > 0},
                 'counterpart_witnesses': before_matches if kind == 'contrast' else [],
                 'positive_compound_witnesses': positive_matches if kind == 'contrast' else [],
                 'new_discriminative_terms': discriminative if kind == 'format' else [],
                 'median_positive_document_frequency': median_frequency,
                 'format_reference_document_frequency': format_frequency,
                 'max_affected_RIDs': 1, 'candidate_filter': False}
        return proposal, order, trace
    return list(map(float, sparse)), original, {'schema': CORRECTION_RECIPE, 'applied': False,
                                              'attempts': attempts, 'max_affected_RIDs': 1,
                                              'candidate_filter': False}

# A role is inferred from affirmative query meaning, never a slot tag, candidate
# ID or benchmark identity. Exact selected-primary spans supply advisory source
# support. Unknown support stays material for authorial review; it grants no
# permission, factual inference, causal proof or native qualification.
FOCUS_RECIPE = 'photo-h-f2-primary-focus-order/v1'
_FOCUS = {
 'age_presentation':r'middle[- ]aged appearance|youthful appearance|older[- ]looking|younger[- ]looking|youthful[- ]looking|middle[- ]aged[- ]looking|age (?:presentation|appearance)|elderly|나이.{0,12}(?:들어|보이)|연령.{0,8}(?:표현|외양)|중년|젊어\s*보',
 'anatomical_connection':r'(?:wing|limb).{0,55}(?:attach|articulat|shoulder)|anatomical (?:route|connection|continuity)|forelimb|foreleg|hindlimb|hind paw|hock|carpus|upper arm.{0,55}(?:elbow|wrist)|anatomy|해부|앞다리|뒷다리|뒷발|위팔.{0,40}(?:팔꿈치|손목)|관절.{0,15}연결|날개.{0,30}(?:어깨|관절)',
 'camera_direction':r'(?:taking|photographing) camera|viewing axis|look across.{0,25}(?:building|corner)|capture camera|camera optical axis|camera.{0,30}(?:viewing|optical|horizontal|level axis|pitched)|(?:촬영|관찰)\s*카메라|관찰축|카메라.{0,20}(?:광축|관찰|수평|방향)',
 'companion_animal':r'companionship|as a companion|keeping.{0,25}company|staying with.{0,25}(?:adult|person)|동반자|동반하는|동반\s*관계|곁을\s*지키|동행\s*관계|(?:animal|bird|dog|cat) companion|companion (?:animal|bird|dog|cat)|accompan(?:y|ies|ying|iment)|동반\s*(?:동물|새|개|고양이)|동물.{0,16}(?:동반|주\s*대상)|동행',
 'declared_background':r'biograph|upbringing|hometown|place of origin|language history|cultural (?:affiliation|self[- ]identification)|stated birthplace|grew up|life geography|약력|출신|성장지|고향|출생지|문화.{0,12}(?:소속|정체성)|언어.{0,12}(?:이력|배경)|거주.{0,12}(?:기간|선언)',
 'eye_detail':r'\biris(?:es)?\b|limbal|collarette|홍채|윤부',
 'makeup_decoration':r'cosmetic (?:stars?|glitter|decoration|paint)|makeup (?:appliqu|decoration|design)|face appliqu|body[- ]paint|메이크업|화장.{0,12}장식|피부.{0,12}(?:별|장식|페인팅)',
 'physical_mass':r'physical mass|\bweighs?\b|kilograms?|\bkg\b|질량|킬로그램|물리적\s*무게',
 'thermal_state':r'physical temperature|thermal (?:state|condition)|temperature (?:of|is|increasing|decreasing)|\b[0-9]+\s*°\s*[CF]\b|물리적\s*온도|열적\s*상태|온도가|온도는|냉각|가열|고온|저온',
 'publication_caption':r'(?:external|publication|editorial|accompanying) caption|caption (?:outside|accompanying|identifies|attributes)|외부\s*캡션|출판.{0,12}캡션|기사.{0,12}캡션|동반\s*설명문',
 'visual_hierarchy':r'visual (?:hierarchy|priority|attention)|primary (?:visual|attention|focal)|secondary (?:visual|attention|focal)|first.{0,24}(?:attention|read)|시각적?\s*(?:위계|우선|우선순위)|시선.{0,15}(?:먼저|우선)|주된\s*초점|보조\s*초점',
 'aesthetic_practice':r'minimalist photograph|미니멀리즘|aesthetic|photographic (?:practice|movement|treatment)|typological|straight[- ]photograph|pictorialis|modernist photograph|사진\s*(?:미학|미감|관습|경향)|미니멀\s*사진|유형학|스트레이트\s*사진|픽토리얼',
 'material_form':r'(?:viscous|flowing|pouring|continuous|curved).{0,25}(?:liquid|honey|ribbon|strand|thread)|(?:liquid|honey).{0,35}(?:form|strand|ribbon|loop|fold)|점성.{0,15}(?:액체|가닥)|(?:액체|꿀).{0,25}(?:형태|형상|가닥|줄기|리본|고리)',
 'object_structure':r'(?:frame tubes?|head tube|wheel axle|fork ends?|object assembly|component joints?|hinge leaves?|mechanical assembly)|(?:bicycle|umbrella|chair).{0,50}(?:join|attach|connect|frame|component)|(?:부품|구성요소).{0,25}(?:연결|결합|구조)|자전거.{0,35}(?:구조|프레임|포크)|힌지|경첩',
 'presentation_style':r'personal presentation|neat grooming|coordinated attire|groomed|grooming|polished (?:appearance|presentation)|몸단장|단정.{0,12}(?:외양|인상|정돈)|개인.{0,12}(?:꾸밈|차림|표현)',
 'prop_placement':r'prop.{0,25}(?:position|placement)|(?:place|position|rest).{0,28}(?:spoon|map|umbrella|phone|prop)|(?:spoon|map|umbrella|phone).{0,35}(?:rests|placed|positioned|leans)|소품.{0,18}(?:위치|배치)|(?:숟가락|지도|우산|휴대폰).{0,25}(?:놓|배치|기대|위치)',
 'species_marker':r'species (?:marker|feature|characteristic)|(?:fox|raven|butterfly|fennec).{0,35}(?:ear|tail|bill|antenna|muzzle)|종.{0,15}(?:표지|특징)|(?:여우|큰까마귀|나비|페넥).{0,25}(?:귀|꼬리|부리|더듬이|주둥이)',
 'subject_identity':r'(?:declared|principal|main|primary) (?:object )?subject|(?:teapot|watering can|violin|sewing machine).{0,30}(?:subject|main|principal)|주\s*(?:대상|피사체)|주된\s*피사체',
 'composition':r'(?:left|right).{0,35}(?:uninterrupted|open|empty|field)|stable triangle|frame.{0,30}triangle|frame.{0,30}(?:symmetr|balance)|(?:centered|foreground).{0,40}(?:chair|frame|branch)|(?:lower|upper) (?:left|right).{0,50}(?:diagonal|sweep)|프레임.{0,20}(?:삼각|균형)|빈\s*공간|좌우\s*대칭|전경.{0,20}(?:가지|틀)|화면.{0,18}(?:왼쪽|오른쪽)|(?:negative space|rule of thirds|left third|right third|triangular grouping|asymmetrical balance|centered symmetry|diagonal composition|foreground framing)|(?:objects?|frame|image).{0,30}(?:arrang|balance|triangle|non-collinear)|네거티브\s*스페이스|삼분할|삼각\s*배치|비대칭\s*균형|중앙\s*대칭|대각선\s*구도|전경\s*프레임|여백|화면.{0,12}(?:배치|균형)',
 'emotional_mood':r'\b(?:wistful|poignant|melanchol|eerie|serene|mood|emotional atmosphere)|정서적?\s*분위기|애잔|아련|서글|불길|평온|정적.{0,12}분위기',
}
def _semantic_pattern(value):
    # Stem alternatives are explicitly expanded; arbitrary substring matches
    # such as hock/shock or hind/behind never supply a semantic witness.
    for stem in ('biograph','typolog','pictorialis','pictorial','modernis','minimalis','photograph','melanchol','refrigerat','residen','migrat','appliqu'):
        value=re.sub(r'(?<![a-z])'+stem+r'(?![a-z])',lambda m:m.group()+r'\w*',value)
    value=value.replace('개가',r'(?<![가-힣])개가').replace('개의',r'(?<![가-힣])개의')
    return re.compile(r'(?<![a-z])(?:'+value+r')(?![a-z])',re.I)
_FOCUS_PATTERNS={k:_semantic_pattern(v) for k,v in _FOCUS.items()}
# Mutually distinct explicit subtypes. Shared context/owner words do not alone
# establish one of these positive properties; every witness stays field-local.
_FACETS={
 'camera_direction':{
  'down':r'downward|looks? down|slopes? down|descends?|하향|내려다|아래로',
  'up':r'upward|looks? up|앙각|올려다|위로\s*향',
  'level':r'level (?:optical|camera|axis|sightline|pitch)|horizontal (?:optical|camera|axis|view)|axis stays horizontal|수평.{0,12}(?:광축|관찰축|관찰|카메라)|(?:광축|관찰축).{0,10}수평',
  'topdown':r'vertical (?:plan|top|overhead)|top[- ]down|overhead plan|수직\s*(?:탑다운|하향|평면)|정수직|완전한\s*탑다운',
  'tilt':r'dutch|canted|tilted horizon|더치|기울어진\s*수평선',
  'oblique':r'oblique|three[- ]quarter|across.{0,20}corner|비스듬|사선|사분의\s*삼|삼사분'},
 'age_presentation':{'old':r'older[- ]looking|elderly|looks older|나이\s*들어|노년|늙어\s*보','youth':r'you(?:thful|nger)[- ]looking|looks (?:younger|youthful)|젊어\s*보|젊게','middle':r'middle[- ]aged[- ]looking|중년','synthetic':r'synthetic|android|silicone|mannequin|합성\s*(?:인간|인물|형상)|안드로이드|마네킹|실리콘'},
 'aesthetic_practice':{'minimal':r'minimalis|미니멀','typology':r'typolog|유형학','straight':r'straight[- ]photograph|스트레이트\s*사진','pictorial':r'pictorial|픽토리얼','modernist':r'modernis|new vision|모더니즘|뉴\s*비전'},
 'declared_background':{'upbringing':r'upbringing|grew up|childhood|성장지|자랐|성장했|어린\s*시절','birthplace':r'birthplace|place of birth|출생지|태어난\s*곳','residence':r'residen|lived (?:in|at|for)|거주','language':r'language|언어','culture':r'cultural|문화','migration':r'migrat|successive life stages|이주|이민|생애\s*단계'},
 'eye_detail':{'radial':r'radial|streak|방사|줄무늬','border':r'limbal|outer (?:iris )?(?:edge|border)|outer edge|outer.*iris|홍채.{0,15}(?:바깥|외곽|가장자리)|윤부','crypt':r'crypt|hollows|음와|움푹','collarette':r'collarette|칼라렛|주름띠','flecks':r'pigment flecks|색소\s*점'},
 'thermal_state':{'cooling':r'cooling|temperature is decreasing|냉각|온도.{0,8}내려|식어','warming':r'warming|temperature increasing|가열|온도.{0,8}올라|데워','cold':r'cold|refrigerat|차가|냉장|저온','hot':r'\bhot\b|heated|뜨거|고온'},
 'material_form':{'strand':r'strand|thread|ribbon|가닥|줄기|리본','loop':r'loops?|coils?|고리|감긴','sheet':r'sheet|film|막|박막','liquid':r'liquid|honey|액체|꿀'},
 'anatomical_connection':{'cat':r'\bcat\b|feline|고양이','dog':r'\bdog\b|canine|강아지|개의|개가','bird':r'\bbird\b|avian|새의|새가|조류','human':r'human|person|adult|사람|성인','plant':r'plant|leaf|petiole|식물|잎|잎자루','hind':r'hind|hock|뒷다리|뒷발','fore':r'forelimb|foreleg|front limb|앞다리|앞발','radiograph':r'radiograph|x[- ]ray|방사선|엑스레이'},
 'companion_animal':{'dog':r'\bdog\b|강아지|개의|개가','bird':r'\bbird\b|avian|새의|새가|조류','walk':r'walk|걷|산책|보행','lap':r'\blap\b|무릎','shoulder':r'shoulder|어깨','preen':r'preen|깃털.{0,10}고르'},
 'species_marker':{'fox':r'fox|여우','raven':r'raven|큰까마귀','butterfly':r'butterfly|나비','fennec':r'fennec|페넥'},
 'makeup_decoration':{'cheek':r'cheek|볼\s*피부|뺨','temple':r'temple|관자','clavicle':r'clavicle|collarbone|쇄골','hand':r'hand|손등','star':r'star[- ]shaped|cosmetic stars|별\s*모양|별\s*장식','pearl':r'pearl|진주'},
 'composition':{'triangle':r'triang|non-collinear|삼각|비공선','negative_space':r'negative space|여백|네거티브','symmetry':r'centered symmetry|symmetrical|중앙\s*대칭|좌우\s*대칭','diagonal':r'diagonal|대각선','frame':r'foreground fram|전경\s*프레임','balance':r'counterweight|counterbalance|asymmetr|비대칭|맞은편\s*균형'},
 'prop_placement':{'spoon':r'spoon|숟가락','phone':r'phone|휴대폰','umbrella':r'umbrella|우산','map':r'\bmap\b|지도','table':r'table|탁자|테이블','chair':r'chair|의자','floor':r'floor|바닥'},
 'subject_identity':{'teapot':r'teapot|찻주전자','wateringcan':r'watering can|물뿌리개','violin':r'violin|바이올린','sewingmachine':r'sewing machine|재봉틀'},
 'object_structure':{'bicycle':r'bicycle|자전거','umbrella':r'umbrella|우산','hinge':r'hinge|경첩|힌지','chair':r'chair|의자'},
}
_FACETS['anatomical_connection'].update({'arm':r'upper arm|forearm|elbow|wrist|위팔|아래팔|팔꿈치|손목','hand':r'hand|palm|finger|손등|손바닥|손가락','leg':r'leg|knee|다리|무릎','wing':r'wing|날개','leaf':r'leaf|petiole|잎자루|잎','genital':r'vulva|genital|외음부'})
_FACETS['composition']['negative_space']+=r'|uninterrupted field|open space|empty field|빈\s*공간'
_FACETS['composition']['triangle']+=r'|triangle|삼각형'
_FACETS['companion_animal']['dog']+=r'|terrier|테리어'
_FACET_PATTERNS={role:{k:_semantic_pattern(v) for k,v in groups.items()} for role,groups in _FACETS.items()}
# Explicit categories with different owners or material directions cannot be
# borrowed as one another. An unspecified source subtype remains unproven.
_EXCLUSIVE={
 'anatomical_connection':[{'cat','dog','bird','human','plant'},{'hind','fore'},{'arm','hand','leg','wing','leaf','genital'}],
 'camera_direction':[{'down','up','level','topdown'}],
 'aesthetic_practice':[{'minimal','typology','straight','pictorial','modernist'}],
 'species_marker':[{'raven','butterfly','fox'}],
 'subject_identity':[{'teapot','wateringcan','violin','sewingmachine'}],
 'object_structure':[{'bicycle','umbrella','hinge','chair'}],
 'thermal_state':[{'cooling','warming'},{'cold','hot'}],
 'prop_placement':[{'spoon','phone','umbrella','map'}],
}

@lru_cache(maxsize=4096)
def _focus_positive(text):
    # Positive surface with original Unicode offsets, limited to explicit
    # quotation/polarity operators. Complements after "but" remain affirmative.
    if not isinstance(text,str):raise ValueError('scope field must be text')
    if not text.strip():return text
    scope=analyze(text,lambda v:re.findall(r'[^\W_]+',v.casefold()))
    chars=list(text)
    for row in scope['contrast_spans']:
        chars[row['start']:row['end']]=' '*(row['end']-row['start'])
    quoted=_quoted(text)
    for a,b in quoted:chars[a:b]=' '*(b-a)
    for m in re.finditer(r'\b(?:without|free\s+of|excluding|exclude|do\s+not|with\s+no|no(?!\s+longer)|not(?!\s+only)|never|neither)\b',text,re.I):
        if any(a<=m.start()<b for a,b in quoted):continue
        stop=re.search(r'[.!?;\n]|\b(?:but|however|yet)\b|(?:,\s*|\band\s+)(?=(?:keep|retain|preserve|show|make|give|leave|aim|point|use|apply|arrange|position|compose|display)\b)',text[m.end():],re.I)
        end=m.end()+stop.start() if stop else len(text)
        chars[m.start():end]=' '*(end-m.start())
    for clause in re.finditer(r'[^.!?;,\n]+',text):
        raw=clause.group();base=clause.start()
        local=list(raw)
        # A case-marked object of a conversion/invention prohibition is a
        # local negative adjunct, not a denial of its earlier declared owner.
        for adjunct in re.finditer(r'\S{1,24}(?:을|를|으로|로)\s+(?:바꾸지|만들어내지|추론하지|부여하지)\s*않고',raw):
            a,b=adjunct.start(),adjunct.end();local[a:b]=' '*(b-a);chars[base+a:base+b]=' '*(b-a)
        raw=''.join(local)
        contrast=re.search(r'아니라|대신|말고',raw)
        if contrast:
            end=base+contrast.end();chars[base:end]=' '*(end-base)
        for m in re.finditer(r'[^,;.!?]{0,180}?(?:[가-힣]+지\s*않|하지\s*말|요청하지|원하지|아니며|아니고|제외한다|없다)',raw):
            a,b=base+m.start(),base+m.end()
            prefix=raw[m.start():m.end()]
            conjunctions=list(re.finditer(r'\S*(?:하고|하며|하되|있고|이고|이며|두고|놓고|유지한\s*채)\s+',prefix))
            if conjunctions:a+=conjunctions[-1].end()
            chars[a:b]=' '*(b-a)
    return ''.join(chars)

def _focus_spans(text,pattern):
    positive=_focus_positive(text)
    return [{'start':m.start(),'end':m.end(),'quote':text[m.start():m.end()]} for m in pattern.finditer(positive)]





_OWNER_PATTERNS={
 'human':r'\b(?:human|adult|person|people|man|woman|handler|walker|sitter)\b|성인|사람|인물|보호자',
 'cat':r'\b(?:cat|feline)\b|고양이', 'dog':r'\b(?:dog|canine|terrier)\b|강아지|테리어|개의|개가',
 'horse':r'\bhorse\b|말의|말이|말과', 'rabbit':r'\brabbit\b|토끼',
 'bird':r'\b(?:bird|avian|parrot|dove)\b|조류|앵무새|비둘기|새의|새가',
 'fox':r'\b(?:fox|fennec)\b|여우|페넥', 'butterfly':r'\bbutterfly\b|나비',
 'fantasy':r'\b(?:wyvern|dragon|phoenix|gryphon|griffin|magical|sorcery|supernatural)\b|와이번|드래곤|불사조|그리핀|마법|초자연',
 'chair':r'\bchair\b|의자','table':r'\b(?:table|tabletop|desk)\b|탁자|테이블|책상',
 'cup':r'\b(?:cup|mug)\b|찻잔|머그|컵','spoon':r'\bspoon\b|숟가락',
 'module':r'\b(?:storage modules?|module array)\b|수납\s*모듈',
 # Dependent regions are not independent owners; local facets retain them.
 'synthetic':r'\b(?:android|synthetic figure|mannequin|silicone face)\b|안드로이드|마네킹|합성\s*형상|실리콘\s*얼굴',
 'print':r'\b(?:radiograph|x-ray|printed (?:chart|diagram)|drawing of|anatomical chart)\b|방사선|엑스레이|인쇄된\s*(?:도표|그림)|해부\s*도표',
}
_OWNER_RX={k:_semantic_pattern(v) for k,v in _OWNER_PATTERNS.items()}
def _owner_atoms(text):
    return sorted(k for k,p in _OWNER_RX.items() if any(not (k=='dog' and _KOREAN_COUNTER.search(text[:m.start()])) for m in p.finditer(text)))

_FOOTPRINT_PREFIXES={'aesthetic_practice': ['style.aesthetic', 'style.trend', 'aesthetic.'], 'age_presentation': ['age.', 'subject.age', 'appearance.age'], 'anatomical_connection': ['body.connection', 'body.topology', 'anatomy.connection', 'topology.'], 'camera_direction': ['camera.direction', 'camera.angle', 'camera.roll', 'view.direction'], 'companion_animal': ['participant.animal', 'companion.animal'], 'composition': ['layout.', 'composition.', 'placement.'], 'declared_background': ['identity.background', 'identity.origin'], 'eye_detail': ['eyes.structure', 'eyes.iris', 'eyes.color', 'eye.'], 'makeup_decoration': ['makeup.decoration', 'skin.cosmetic_decoration'], 'material_form': ['matter.form', 'matter.contour', 'matter.volume_shape'], 'emotional_mood': ['mood.', 'affect.', 'scene.mood'], 'object_structure': ['object.structure', 'object.geometry', 'object.connection'], 'physical_mass': ['physical.mass', 'physical.weight'], 'presentation_style': ['presentation.', 'appearance.presentation'], 'prop_placement': ['props.placement', 'prop.position', 'prop.orientation', 'objects.position'], 'publication_caption': ['publication.caption', 'caption.context'], 'species_marker': ['species.', 'body.species', 'body.ear_structure', 'body.tail'], 'subject_identity': ['subject.', 'entity.', 'object_inventory'], 'thermal_state': ['thermal.state', 'thermal.temperature', 'thermal.process', 'material.thermal', 'object.temperature', 'surface.temperature'], 'visible_text': ['text.', 'lettering.', 'sign.content'], 'visual_hierarchy': ['layout.hierarchy', 'composition.hierarchy']}
_FOOTPRINT_DIMENSIONS={
 'aesthetic_practice':('style','color'), 'composition':('composition',),
 'eye_detail':('appearance',), 'makeup_decoration':('appearance',),
 'subject_identity':('subject',), 'camera_direction':('camera',),
}
_FOOTPRINT_PREFIXES['eye_detail'].append('face.eyes.')
_FOOTPRINT_PREFIXES['anatomical_connection'].append('botanical.structure')

# Bounded language coverage for explicit property relations. Stems are guarded
# at ASCII word boundaries; Korean standalone animal nouns require boundaries.
_FOCUS.update({
 'age_presentation':_FOCUS['age_presentation']+r'|(?:declared|stated|chronological) age|실제\s*(?:나이|연령)|연령\s*선언',
 'anatomical_connection':_FOCUS['anatomical_connection']+r'|petiole|leaf.{0,40}(?:join|connect|attach)|plant.{0,40}(?:join|connect|attach)|잎자루|잎.{0,24}(?:붙|이어|연결)|손목.{0,24}(?:그림|연결)',
 'camera_direction':_FOCUS['camera_direction']+r'|(?:건물|외벽).{0,30}(?:사선|모서리|바라)|(?:optical|viewing) axis|taking camera',
 'eye_detail':_FOCUS['eye_detail']+r'|pupils?|동공',
 'material_form':_FOCUS['material_form']+r'|material (?:body|contour|shape)|gel.{0,25}(?:dome|oval|form|contour)|(?:water|dough|wax).{0,30}(?:arch|spiral|pool|form|contour)|물질체|물질\s*윤곽|젤.{0,20}(?:타원|형태|돔)|(?:물|반죽|왁스).{0,20}(?:아치|나선|윤곽|웅덩이)',
 'emotional_mood':_FOCUS['emotional_mood']+r'|uneas\w*|tens\w*|hope\w*|festiv\w*|intima\w*|scene[- ]affect|emotional reading|정서|긴장감|불안|희망|친밀|축제|고요',
 'object_structure':_FOCUS['object_structure']+r'|articulated lamp|carabiner|headband|headphone|drawer.{0,22}(?:runner|cabinet)|folding stool|equipment case|관절형\s*등|카라비너|헤드폰|서랍.{0,15}(?:레일|캐비닛)|접이식\s*스툴|장비\s*케이스',
 'physical_mass':_FOCUS['physical_mass']+r'|(?:declared|stated|supplied) (?:[\w-]+ ){0,3}mass|physically (?:lightweight|heavier|lighter)|(?:grams?|그램).{0,20}(?:lighter|가벼워)|물리적으로\s*(?:가볍|무겁)|질량\s*변화',
 'presentation_style':_FOCUS['presentation_style']+r'|(?:hair|grooming).{0,55}(?:attire|clothes|clothing|garment)|(?:머리|머리카락|헤어).{0,35}(?:차림|옷|의복)',
 'prop_placement':_FOCUS['prop_placement']+r'|(?:tool|cloth|prop).{0,45}(?:pocket|edge|support|rests|held)|(?:도구|천|소품).{0,30}(?:주머니|가장자리|지지|받침|쥐)',
 'species_marker':_FOCUS['species_marker']+r'|axolotl|external gills|cat.{0,30}(?:ear|whisker|tail)|아홀로틀|외부\s*아가미|고양이.{0,25}(?:귀|수염|꼬리)',
 'visual_hierarchy':_FOCUS['visual_hierarchy']+r'|attention order|visual salience|눈에\s*먼저|먼저\s*(?:보|읽|시선)|그다음.{0,20}(?:보|읽|시선)',
})
_FACETS['physical_mass']={
 'numeric':r'quantity value|numeric|numerical|unit|kilograms?|grams?|킬로그램|그램|양\s*값|수치|단위',
 'qualitative':r'qualitative|lightweight|physically light|정성|물리적으로\s*가볍',
 'comparison':r'heavier than|lighter than|comparative|compared|보다.{0,12}(?:무겁|가볍)|질량\s*비교',
 'change':r'mass change|became.{0,30}lighter|change in.{0,15}mass|질량\s*변화|가벼워졌|무거워졌',
}
_FACETS['camera_direction'].update({
 'front':r'(?:camera|axis).{0,35}(?:straight toward the front|squarely|front[- ]facing)|정면.{0,15}(?:곧바로|향)|곧바로.{0,15}정면',
 'clockwise':r'clockwise|시계\s*방향',
 'roll':r'\broll\b|프레임.{0,8}회전|카메라.{0,16}(?:회전|좌우\s*기울기)',
 'shoulder_view':r'axis.{0,25}shoulder|over[- ]the[- ]shoulder|관찰축.{0,22}어깨',
})
_FACETS['species_marker'].update({'cat':r'cat|feline|고양이','axolotl':r'axolotl|아홀로틀'})
_FACETS['subject_identity'].update({'cat':r'cat|feline|고양이','olive':r'olive tree|올리브나무','potter':r'potter|도예가'})
_FACETS['eye_detail'].update({'pupil':r'round.{0,12}pupil|dark.{0,12}pupil|둥근.{0,12}동공|검은.{0,10}동공','unequal':r'heterochromia|different iris colors|unequal iris|양안.{0,10}(?:다른|상이)|서로\s*다른\s*홍채','central_color':r'central.{0,12}(?:color|ring)|ring.{0,15}pupil|중심.{0,12}색|동공.{0,12}색\s*고리'})
_FACETS['composition'].update({'center_pair':r'centered.{0,30}symmetr|symmetr.{0,30}either side|가운데.{0,20}좌우\s*대칭','route_diagonal':r'road.{0,25}diagonal|route.{0,25}diagonal|도로.{0,18}대각선','enclosure':r'foreground branches|전경\s*가지'})
_PRIORITY=['publication_caption','declared_background','physical_mass','thermal_state','eye_detail','makeup_decoration','age_presentation','aesthetic_practice','visual_hierarchy','material_form','companion_animal','subject_identity','anatomical_connection','camera_direction','prop_placement','composition','presentation_style','object_structure','species_marker','emotional_mood']
_FOCUS_PATTERNS={k:_semantic_pattern(_FOCUS[k]) for k in _PRIORITY}
_FACET_PATTERNS={role:{k:_semantic_pattern(v) for k,v in groups.items()} for role,groups in _FACETS.items()}
_EXCLUSIVE['species_marker']=[{'raven','butterfly','fox','cat','axolotl'}]
_EXCLUSIVE['subject_identity']=[{'teapot','wateringcan','violin','sewingmachine','cat','olive','potter'}]
# Field-local positive assertions that preserve supplied values can bind an open
# value without inventing it; a fixed example cannot supply that contract.
_PRESERVE=re.compile(r'\b(?:preserv\w*|retain\w*|keep\w*)\b|보존|유지',re.I)
_DECLARATION=re.compile(r'\b(?:declared|supplied|independently|existing)\b|선언|명시|독립적으로|기존',re.I)

def _source_family_guard(role,units):
    texts=[_focus_positive(u['text']) for u in units]
    joined='\n'.join(texts)
    if role=='physical_mass':
        return bool(_PRESERVE.search(joined) and _DECLARATION.search(joined) and re.search(r'physical mass|mass declaration|질량|물리적\s*무게',joined,re.I))
    if role=='companion_animal':
        animal=re.compile(r'\b(?:animal|dog|cat|bird|terrier|rabbit)\b|동물|고양이|강아지|테리어|토끼|(?<![가-힣])새(?:의|가|는|\s)',re.I)
        counterpart=re.compile(r'primary|counterpart|human|adult|handler|주\s*대상|성인|보호자',re.I)
        relation=re.compile(r'accompan\w*|companion|stays near|preen\w*|동반|동행|곁|털을\s*고르',re.I)
        return any(animal.search(t) and counterpart.search(t) and relation.search(t) and not re.match(r'\s*(?:A |The )?(?:caption|biography|article)\b',t,re.I) for t in texts)
    return True

def _parameter_preservation(role,units):
    text='\n'.join(_focus_positive(u['text']) for u in units)
    if not (_PRESERVE.search(text) and _DECLARATION.search(text)):return False
    patterns={
      'material_form':r'(?:declared|supplied).{0,60}(?:contour|shape)|(?:contour|shape).{0,60}(?:declared|supplied)|선언.{0,30}(?:윤곽|형상)|(?:윤곽|형상).{0,30}(?:보존|유지)',
      'publication_caption':r'(?:supplied|declared).{0,60}(?:account|caption|information)|제공.{0,35}(?:캡션|정보|서술)',
      'makeup_decoration':r'(?:declared|specified).{0,80}(?:design|region|motif)|(?:design|region|motif).{0,80}(?:declared|specified)|선언.{0,40}(?:피부|디자인|모티브)',
      'companion_animal':r'(?:primary|counterpart).{0,100}(?:declared|existing|retained)|(?:declared|existing).{0,100}(?:primary|counterpart)|주\s*대상.{0,45}(?:선언|유지)',
      'visual_hierarchy':r'(?:supplied|declared|existing).{0,60}(?:attention|order)|(?:attention|order).{0,60}(?:supplied|declared)|선언.{0,35}(?:순서|위계)',
    }
    return role in patterns and re.search(patterns[role],text,re.I) is not None

def _iris_base_colors(text):
    colors={
      'blue':r'\bblue\s+(?:iris|irises)|푸른\s*홍채|파란\s*홍채',
      'green':r'\b(?:moss[- ])?green\s+(?:base|iris|irises)|녹색\s*(?:바탕|홍채)|초록\s*홍채',
      'brown':r'\bbrown\s+(?:iris|irises)|갈색\s*홍채|브라운\s*홍채',
      'gray':r'\bgr[ae]y\s+(?:iris|irises)|회색\s*홍채',
    }
    return sorted(k for k,p in colors.items() if re.search(p,text,re.I))


_FACETS['age_presentation'].update({
 'face':r'face|facial|얼굴',
 'hands':r'hands?|hand skin|손등|손\s*피부|양손|두\s*손',
 'both_hands':r'both hands|two hands|양손|두\s*손',
 'two_people':r'two.{0,25}(?:adults|people|persons)|separate adults|두.{0,12}성인|서로.{0,15}성인',
})
_FACETS['camera_direction']['roll']=r'roll(?:s|ed|ing)?|프레임.{0,8}회전|카메라.{0,16}(?:회전|좌우\s*기울기)'
_FACET_PATTERNS={role:{k:_semantic_pattern(v) for k,v in groups.items()} for role,groups in _FACETS.items()}

def _raw_facet_spans(text,pattern):
    return [{'start':m.start(),'end':m.end(),'quote':m.group()} for m in pattern.finditer(text)]

def _facet_spans(text,pattern):
    matches=_focus_spans(text,pattern)
    out=[]
    for m in matches:
        tail=text[m['end']:]
        # Negation attaches to the exact property, not an earlier owner noun.
        if re.match(r'\s*(?:(?:으?로|을|를|이|가|은|는|도)\s*)?(?:아닌|아니라|아니고|없|두지\s*않|하지\s*않|바꾸지\s*않|기울이지\s*않|향하지\s*않)',tail):continue
        out.append(m)
    return out



_KOREAN_COUNTER=re.compile(r'(?:[0-9]+|한|두|세|네|다섯|여섯|몇|여러)\s*$')
def _source_owner_surface(text):
    chars=list(_focus_positive(text))
    # A type domain or unresolved private feeling does not assert another
    # pictured owner. Preserve the mandatory concrete-owner clauses elsewhere.
    for m in re.finditer(r'[^.!?;\n]*(?:may be human or nonhuman|human or nonhuman|leaving every person.{0,35}unknown|unknown private feeling)[^.!?;\n]*|(?:인간|사람).{0,35}(?:필요|요구).{0,8}없[^.!?;\n]*',text,re.I):
        chars[m.start():m.end()]=' '*(m.end()-m.start())
    return ''.join(chars)
_SUBJECT_SELECT=re.compile(r'\b(?:principal|primary|main)\s+(?:(?:declared|visible|observed|physical)\s+){0,2}(?:subject|entity|object|person|animal|plant)\b|central\s+(?:object|entity|subject)\s+of\s+interest|(?:photograph|photo|image).{0,30}(?:main|primary|principal)\s+attention\s+(?:to|toward)|what\s+(?:this|the)\s+(?:photograph|photo|image)\s+is\s+about|(?:주된|주요|주)\s*(?:가시적(?:인)?\s*)?(?:피사체|관찰\s*대상|대상|인물|개체|물체)|관심(?:의)?\s*중심.{0,12}(?:물체|대상|개체)|주로\s*관찰(?:하는|할)\s*대상|(?:사진|영상|이미지)(?:의)?\s*(?:주된|주요)\s*관심',re.I)
_FOCUS['subject_identity']+='|'+_SUBJECT_SELECT.pattern
_FOCUS['aesthetic_practice']+=r'|painterly photographic finish|color fields organize|chromatic relationships|컬러\s*블로킹|색의\s*관계.{0,30}미학|회화주의|회화적\s*세부'
_FACETS['aesthetic_practice']['color_fields']=r'color fields|chromatic relationships|broad areas of color|컬러\s*블로킹|색면|색의\s*관계'
_FACETS['aesthetic_practice']['pictorial']+=r'|painterly photographic finish|회화주의|회화적\s*세부'
_FACETS['age_presentation']['middle']+=r'|middle[- ]aged(?: appearance)?'
_FOCUS['age_presentation']+=r'|declared.{0,35}(?:year[- ]old|adult|age)|선언된\s*[0-9]+세|명시된.{0,20}성인.{0,10}세'
_FOCUS['declared_background']+=r'|이력|이주했|migration|life stages'
_FACETS['declared_background']['migration']+=r'|successive stages of life|이주|생애'
_FOCUS['material_form']+=r'|(?:flame|paste|wax|dough|gel|liquid|material).{0,80}(?:body|silhouette|contour|mound|pool|dome|shape)|(?:불꽃|페이스트|왁스|반죽|젤|액체).{0,70}(?:몸체|윤곽|더미|형태|형상|웅덩이)'
_FOCUS['makeup_decoration']+=r'|cosmetic (?:decals?|crystals?|foil|appliqu|ornament)|body makeup|face gems|skin.{0,70}(?:stickers?|decals?)|(?:별|화장용).{0,35}(?:스티커|크리스털|포일|물감)|(?:스티커|크리스털|장식).{0,40}피부'
_FACETS['makeup_decoration'].update({'applique':r'decals?|appliqu|stickers?|스티커|아플리케','pigment':r'cosmetic (?:paint|pigment)|body makeup|보디\s*메이크업|물감','foil':r'(?:metallic|cosmetic|gold).{0,12}foil|메탈릭\s*포일|금색.{0,10}포일','crystal':r'crystal|face gems|크리스털|젬'})
_FACETS['camera_direction']['front']+=r'|faces.{0,50}front surface squarely|축.{0,30}정면|정면.{0,25}관찰축'
_FACETS['camera_direction']['oblique']+=r'|across.{0,35}(?:outside|shared).{0,15}corner|외부\s*모서리'
_FACETS['camera_direction']['shoulder_view']+=r'|camera observes.{0,50}shoulder|axis.{0,50}shoulder|어깨\s*너머'
_FACETS['companion_animal']['walk']+=r'|direction of travel|travelling|이동\s*방향|함께\s*이동'
_FOCUS['composition']+=r'|(?:visual|asymmetric) balance|bilateral correspondence|foreground boundary|frame.{0,20}frame|(?:balance|align).{0,100}(?:frame|symmetr)|(?:프레임|화면).{0,45}균형|기존.{0,35}좌우\s*대칭'
_FACETS['composition']['balance']+=r'|counterweighted|asymmetric|visual balance|상쇄'
_FACETS['composition']['symmetry']+=r'|symmetrically|bilateral correspondence|중심축|좌우\s*대칭'
_FACETS['composition']['frame']+=r'|foreground boundary|enclosing.{0,25}subject|전경\s*경계|프레임\s*속\s*프레임'
_FACETS['composition']['enclosure']+=r'|foreground boundary|전경\s*경계'
# Explicit emotional interpretation takes priority over its means (spacing,
# light or layout). Literal physical attributes remain separate role requests.
_PRIORITY.remove('emotional_mood');_PRIORITY.insert(3,'emotional_mood')
_FOCUS_PATTERNS={k:_semantic_pattern(_FOCUS[k]) for k in _PRIORITY}
_FACET_PATTERNS={role:{k:_semantic_pattern(v) for k,v in groups.items()} for role,groups in _FACETS.items()}
_OWNER_RX={k:_semantic_pattern(v) for k,v in _OWNER_PATTERNS.items()}


# Independently tested, source-bound semantic comparators. They expose advisory
# compatibility only; native guards, owner binding and complete effects remain.
from photo_h_f2_semantic_age_eye import Semantic as _Semantic_age_eye
from photo_h_f2_semantic_context_mass import Semantic as _Semantic_context_mass
from photo_h_f2_semantic_layout_mood import Semantic as _Semantic_layout_mood
from photo_h_f2_semantic_species_anatomy_companion import Semantic as _Semantic_species_anatomy_companion
from photo_h_f2_semantic_subject_aesthetic_material import Semantic as _Semantic_subject_aesthetic_material
from photo_h_f2_semantic_object_makeup_prop import Semantic as _Semantic_object_makeup_prop
from photo_h_f2_semantic_camera_presentation import Semantic as _Semantic_camera_presentation
_CONTROLLERS={}
_controller_age_eye=_Semantic_age_eye(None)
_CONTROLLERS['age_presentation']=_controller_age_eye
_CONTROLLERS['eye_detail']=_controller_age_eye
_CONTROLLERS['thermal_state']=_controller_age_eye
_controller_context_mass=_Semantic_context_mass((lambda text:text))
_CONTROLLERS['publication_caption']=_controller_context_mass
_CONTROLLERS['declared_background']=_controller_context_mass
_CONTROLLERS['physical_mass']=_controller_context_mass
_controller_layout_mood=_Semantic_layout_mood(_focus_positive)
_CONTROLLERS['composition']=_controller_layout_mood
_CONTROLLERS['emotional_mood']=_controller_layout_mood
_CONTROLLERS['visual_hierarchy']=_controller_layout_mood
_controller_species_anatomy_companion=_Semantic_species_anatomy_companion(_focus_positive)
_CONTROLLERS['species_marker']=_controller_species_anatomy_companion
_CONTROLLERS['anatomical_connection']=_controller_species_anatomy_companion
_CONTROLLERS['companion_animal']=_controller_species_anatomy_companion
_controller_subject_aesthetic_material=_Semantic_subject_aesthetic_material(_focus_positive)
_CONTROLLERS['subject_identity']=_controller_subject_aesthetic_material
_CONTROLLERS['aesthetic_practice']=_controller_subject_aesthetic_material
_CONTROLLERS['material_form']=_controller_subject_aesthetic_material
_controller_object_makeup_prop=_Semantic_object_makeup_prop(_focus_positive)
_CONTROLLERS['object_structure']=_controller_object_makeup_prop
_CONTROLLERS['makeup_decoration']=_controller_object_makeup_prop
_CONTROLLERS['prop_placement']=_controller_object_makeup_prop
_controller_camera_presentation=_Semantic_camera_presentation(None)
_CONTROLLERS['camera_direction']=_controller_camera_presentation
_CONTROLLERS['presentation_style']=_controller_camera_presentation

_PRIORITY=['publication_caption','declared_background','physical_mass','thermal_state',
 'eye_detail','makeup_decoration','age_presentation','aesthetic_practice',
 'visual_hierarchy','emotional_mood','material_form','subject_identity',
 'companion_animal','anatomical_connection','species_marker','camera_direction',
 'prop_placement','composition','presentation_style','object_structure']

def _request_witnesses(descriptor,text,focus,offset):
    out=[]
    for w in descriptor.get('witnesses',[]):
        a,b=w.get('start'),w.get('end');quote=w.get('quote')
        if type(a) is not int or type(b) is not int or not isinstance(quote,str):continue
        # Comparators explicitly retain either role-local or full-request
        # offsets. Normalize only when the original addressed slice is exact.
        if w.get('pointer')=='/request' and text[a:b]==quote:
            out.append({**w,'pointer':'/request','start':a,'end':b})
        elif focus[a:b]==quote:
            out.append({**w,'pointer':'/request/role_focus','start':offset+a,'end':offset+b})
        elif text[a:b]==quote:
            out.append({**w,'pointer':'/request','start':a,'end':b})
    if not out:
        out=[{'pointer':'/request/role_focus','start':offset,'end':offset+len(focus),'quote':focus}]
    return out

_DOMAIN_HEADS={
 'age_presentation':r'\bage\b|elderly|older[- ]looking|youthful|연령|나이|노인|늙어',
 'eye_detail':r'\biris(?:es)?\b|\bpupils?\b|eye colo[u]?r|\beyes\b|홍채|동공|눈\s*색',
 'thermal_state':r'temperatur|thermal|\b(?:hot|cold|warm|heat)\b|온도|열적|냉각|가열|뜨거|차갑',
 'makeup_decoration':r'cosmetic|makeup|face gems|화장|메이크업|아플리케',
}
_STRICT_SCOPE_HEADS={
 'species_marker':r'actual animal|animal itself|animal|biological species|동물|실제\s*개체',
 'companion_animal':r'animal participant|companion|동반|동물',
 'anatomical_connection':r'anatomical|anatomy|body part|해부|신체\s*부위|연결',
 'object_structure':r'construction detail|construction|component joints?|part connections?|구조|부품|결합',
 'prop_placement':r'placement|orientation|position|carry|hold|배치|위치|방향|들고|쥐',
 'visual_hierarchy':r'prominen\w*|attention|primary|secondary|위계|주목|우선|보조|동등',
}
@lru_cache(maxsize=32)
def _scope_head_pattern(role):
    return _semantic_pattern('|'.join(v for v in (_DOMAIN_HEADS.get(role,''),_STRICT_SCOPE_HEADS.get(role,''),_FOCUS.get(role,'')) if v))

def _nonpositive_role_witnesses(role,text):
    pattern=_scope_head_pattern(role)
    positive=_focus_positive(text);out=[]
    contrasts=analyze(text,lambda v:re.findall(r'[^\W_]+',v.casefold()))['contrast_spans']
    quotes=_quoted(text)
    for m in pattern.finditer(text):
        masked=not positive[m.start():m.end()].strip()
        tail=text[m.end():m.end()+55]
        unknown=re.match(r"\s*(?:(?:colo[u]?r|details?|appearance|placement|position|state|temperature)\s+)?(?:(?:is|are|remains?|stays?|has been|should be)\s+)?(?:unknown|unspecified|unprovided|undeclared|unstated|not\s+(?:requested|specified|declared|provided)|must not be inferred)\b|\s*(?:(?:색|색상|세부|외양|위치|배치|상태|온도)(?:은|는|이|가)?\s*)?(?:은|는|이|가)?\s*(?:미상|미지정|알\s*수\s*없|지정하지|요청하지)",tail,re.I)
        if masked or unknown:
            end=m.end()+unknown.end() if unknown and not masked else m.end()
            soft=masked and any(r['start']<=m.start()<r['end'] for r in contrasts) and not any(a<=m.start()<b for a,b in quotes)
            out.append({'pointer':'/request','start':m.start(),'end':end,'quote':text[m.start():end],'basis':'contrast_counterpart' if soft else 'quoted_or_explicitly_nonpositive' if masked else 'unprovided_property','strict':not soft})
    return out

def _unmodeled_restriction(text,focus):
    # Unknown concrete intent with an explicit restriction cannot justify a
    # replacement property from unrelated advice. Nominal taxonomy controls
    # retain ordinary discovery; fully modeled affirmative neighbors win first.
    concrete=bool(re.search(r'\nScene context:\s*\S',text) or re.match(r'\s*(?:show|keep|make|give|place|arrange|record|render|treat|use|leave|depict|preserve|retain|photograph)\b',focus,re.I))
    if not concrete:return None
    patterns=[r'\b(?:without|do not|must not|should not|no(?!\s+longer)|not(?!\s+only)|never|neither|unknown|unspecified|unprovided|undeclared|unstated)\b',r'(?:하지|되지|부여하지|추론하지|바꾸지|요청하지|지정하지)\s*(?:않|말)|없이|미상|미지정|알\s*수\s*없']
    witnesses=[]
    capability_clauses=[(m.start(),m.end()) for m in re.finditer(
        r'\bsenses?\s+(?:(?:that|which)\s+)?(?:a\s+human\s+(?:observer|operator)|humans?)\s+(?:do|does|did)\s+not\s+(?:possess|have)\b',text,re.I)]
    for pattern in patterns:
        for m in re.finditer(pattern,text,re.I):
            # A relative clause about nonvisual human sensory capability is
            # descriptive context, not an instruction forbidding a prop change.
            # Keep commands, absent body parts and unspecified properties strict.
            if any(a <= m.start() and m.end() <= b for a,b in capability_clauses):
                continue
            end=re.search(r'[.!?;\n]',text[m.end():]);stop=m.end()+end.start() if end else len(text)
            witnesses.append({'pointer':'/request','start':m.start(),'end':stop,'quote':text[m.start():stop]})
    for a,b in _quoted(focus):
        offset=text.index(focus);witnesses.append({'pointer':'/request','start':offset+a,'end':offset+b,'quote':focus[a:b]})
    if not witnesses:return None
    return {'asserts':False,'exclusion_only':True,'intent_mode':'unmodeled_restricted_change','witnesses':witnesses,'native_approval':False}

def focus_request(text):
    m=re.search(r'^Photographic role:[ \t]*(.*?)(?=\nScene context:|\Z)',text,re.S)
    if not m:return None
    focus=m.group(1);excluded=[];strict=[];descriptors={};exclusion_requests={}
    for role in _PRIORITY:
        controller=_CONTROLLERS.get(role)
        if controller is None:continue
        desc=controller.request(role,text)
        if desc is not None and desc.get('asserts',True):
            descriptors[role]=desc
        else:
            pattern=_FOCUS_PATTERNS.get(role)
            explicit_head=re.search(_DOMAIN_HEADS.get(role,r'(?!)'),focus,re.I)
            witnesses=_nonpositive_role_witnesses(role,text)
            if desc is not None and desc.get('exclusion_only'):
                exclusion_requests[role]={**desc,'witnesses':_request_witnesses(desc,text,focus,m.start(1))};strict.append(role);excluded.append(role)
            elif witnesses:
                exclusion_requests[role]={'role':role,'asserts':False,'exclusion_only':True,'witnesses':witnesses,'native_approval':False}
                if any(w.get('strict') for w in witnesses):strict.append(role)
                excluded.append(role)
            elif explicit_head or pattern and pattern.search(focus) and not _focus_spans(focus,pattern):excluded.append(role)
    # A recognized relation with an unmodeled shape is a conservative fallback;
    # it cannot shadow a fully modeled affirmative property in the same query.
    ordered=sorted(_PRIORITY,key=lambda role:descriptors.get(role,{}).get('intent_mode')=='owned_relation_unmodeled')
    for role in ordered:
        if role not in descriptors:continue
        desc=descriptors[role]
        return {'role':role,'semantic':desc,'all_semantics':descriptors,'facets':{},'owner_atoms':[],
                'witnesses':_request_witnesses(desc,text,focus,m.start(1)),
                'focus_offset':m.start(1),'focus_sha256':hashlib.sha256(focus.encode()).hexdigest(),
                'scene_declared':bool(re.search(r'\nScene context:\s*\S',text)),
                'excluded_roles':sorted(set(excluded)),'strict_nonpositive_roles':sorted(set(strict)),
                'exclusion_requests':exclusion_requests,'native_approval':False}
    restricted=_unmodeled_restriction(text,focus)
    if restricted is not None and not strict:
        strict.append('unmodeled_restricted_change');exclusion_requests['unmodeled_restricted_change']=restricted
    if not excluded and not strict:return None
    return {'role':None,'facets':{},'semantic':None,'all_semantics':{},'excluded_roles':sorted(set(excluded)),
            'strict_nonpositive_roles':sorted(set(strict)),'exclusion_requests':exclusion_requests,
            'owner_atoms':[],'witnesses':[],'native_approval':False}


def _positive_unit(u):
    return re.match(r'^/content/(?:en$|ko$|definition$|phrase_en$|phrase_ko$|semantics/definition$|concept_units(?:/|$)|semantic_relations(?:/|$)|embedding_text$|components/)',u.get('pointer','')) is not None

def _checked_evidence(evidence,units):
    actual={(u['pointer'],u['literal_id'],u['text']):u for u in units if _positive_unit(u)}
    out=[]
    for u in evidence:
        key=(u.get('pointer'),u.get('literal_id'),u.get('text'))
        if key not in actual:continue
        original=actual[key]
        if any(u.get(k)!=original.get(k) for k in ('candidate_id','realization_id','source_sha256')):continue
        matches=[]
        for w in u.get('matches',[]):
            a,b=w.get('start'),w.get('end');quote=w.get('quote')
            if type(a) is int and type(b) is int and 0<=a<b<=len(u['text']) and u['text'][a:b]==quote:matches.append(w)
        if not matches:matches=[{'start':0,'end':len(u['text']),'quote':u['text']}]
        out.append({**original,'matches':matches,'facet_matches':[]})
    return out

def compile_focus_contracts(documents,*,source_units,source_effects=None,source_constraints=None):
    if source_effects is None:return {}
    contracts={}
    for did in documents:
        effects=source_effects(did)
        hints={role for role,prefixes in _FOOTPRINT_PREFIXES.items()
               if role in _CONTROLLERS and any(p.get('property','').startswith(tuple(prefixes)) for p in effects.get('properties',[]))}
        hints.update(role for role,dimensions in _FOOTPRINT_DIMENSIONS.items() if set(effects.get('dimensions',[]))&set(dimensions))
        if not effects.get('dimensions') and re.search(r'(?:declared|chronological) age|실제\s*(?:나이|연령)',documents[did],re.I):hints.add('age_presentation')
        eligible_hints=set(hints)
        if not effects.get('properties') and not effects.get('dimensions'):
            hints.update(role for role,pattern in _FOCUS_PATTERNS.items() if role in _CONTROLLERS and pattern.search(documents[did]))
        if not hints:continue
        units=source_units(did);constraints=source_constraints(did) if source_constraints else {}
        roles={}
        for role in sorted(hints):
            controller=_CONTROLLERS.get(role)
            if controller is None:continue
            semantic=controller.source(role,units,effects|constraints)
            if semantic is None or semantic.get('asserts') is False:continue
            evidence=_checked_evidence(semantic.get('evidence',[]),units)
            if not evidence:continue
            roles[role]={'semantic':semantic,'evidence':evidence,'facets':{},
                'selected_effect_footprint':effects.get('properties',[]),
                'effect_sha256':hashlib.sha256(json.dumps(effects,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                'constraints_sha256':hashlib.sha256(json.dumps(constraints,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                'source_constraints':constraints,
                'pure_role_scope':_pure_role_scope(role,effects,semantic),
                'positive_support_eligible':role in eligible_hints,
                'footprint_is_not_semantic_or_native_approval':True}
        if roles:contracts[did]=roles
    return contracts

def _pure_role_scope(role,effects,semantic):
    props=effects.get('properties',[])
    if props:return all(p.get('property','').startswith(tuple(_FOOTPRINT_PREFIXES.get(role,[]))) for p in props)
    if role=='age_presentation' and semantic.get('declaration_only'):return True
    dims=set(effects.get('dimensions',[]))
    exclusive={'composition':{'composition'},'aesthetic_practice':{'style','color'},
               'subject_identity':{'subject'},'camera_direction':{'camera'}}
    return bool(dims) and dims <= exclusive.get(role,set())

def order_focus(rows,text,contracts):
    req=focus_request(text)
    trace={'schema':FOCUS_RECIPE,'request':req,'applied':False,'score_changes':0,
           'pre_search_filter':False,'additional_search_calls':0,'native_approval':False}
    if req is None:return rows,trace
    role=req['role'];supported={};conflicting={};controller=_CONTROLLERS.get(role)
    for row in rows:
        profiles=contracts.get(row['id'],{})
        denied=[k for k in req.get('excluded_roles',[]) if k in profiles]
        if denied:
            conflicting[row['id']]={'explicitly_excluded_or_nonpositive_roles':denied};continue
        source=profiles.get(role)
        if source is not None and controller is not None:
            if not _minimum_declared_guards(text,source.get('source_constraints',{})):continue
            decision=controller.fit(req['semantic'],source['semantic'])
            if decision=='supported' and source.get('positive_support_eligible',True):supported[row['id']]=source;continue
            if decision=='conflicting':conflicting[row['id']]=source;continue
        # A pure declaration/mutation option cannot invent its own missing
        # requested property just to fill an ordinary material budget. Mixed,
        # unrecognized advice remains reviewable and receives no approval.
        missing=[k for k,v in profiles.items() if v.get('pure_role_scope')
                 and k not in req.get('all_semantics',{})]
        if missing:conflicting[row['id']]={'missing_independent_property_request':missing}
    result=sorted(rows,key=lambda row:0 if row['id'] in supported else 2 if row['id'] in conflicting else 1)
    trace.update({'supported_ids':sorted(supported),'conflicting_ids':sorted(conflicting),
        'supported_count':len(supported),'conflicting_count':len(conflicting),
        'returned_source_witnesses':{row['id']:supported[row['id']] for row in result[:8] if row['id'] in supported},
        'support_evidence_sha256':hashlib.sha256(json.dumps(supported,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'conflict_evidence_sha256':hashlib.sha256(json.dumps(conflicting,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'applied':[r['id'] for r in rows]!=[r['id'] for r in result],
        'stable_within_groups':True,'unknown_sources_retained':True})
    # Proof packets are JSON values. Internal comparators may use tuples, but
    # a saved packet must replay with the same public value types.
    trace=json.loads(json.dumps(trace,ensure_ascii=False,sort_keys=True,allow_nan=False))
    return result,trace

def _minimum_declared_guards(text,constraints):
    """Explicit guard prerequisites are never supplied by a topic or rank.

    This bounded exclusion is not a complete native predicate execution. The
    native graph/owner/condition checker remains required for actual adoption.
    """
    def required_adult(guard):
        if not isinstance(guard,dict):return False
        if 'adult' in guard.get('requires_all_tags',[]) or guard.get('requires_adult_context') is True:return True
        return any(required_adult(g) for g in guard.get('all_of',[]))
    if any(required_adult(constraints.get(k,{})) for k in ('source_conditions','realization_conditions')):
        return re.search(r'\badults?\b|성인',_focus_positive(text),re.I) is not None
    return True
