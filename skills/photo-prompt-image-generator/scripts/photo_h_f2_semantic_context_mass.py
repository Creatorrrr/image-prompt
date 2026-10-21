"""Bounded, source-witnessed contextual declaration comparison.

No retrieval, metadata identities, slot tags, model calls or adoption authority.
A caller retains native guards/permissions; supported means advisory whole-source
semantic compatibility only. Application contracts restrict, never create facts.
"""
from __future__ import annotations
import copy
import re

_FLAGS = re.I | re.S
_ROLES = {'publication_caption', 'declared_background', 'physical_mass'}
_QUOTES = re.compile(r'“[^”]*”|‘[^’]*’|"[^"\n]*"|(?<!\w)\x27[^\x27\n]*\x27')
_UNKNOWN = re.compile(r'\b(?:unknown|unspecified|unstated|undeclared|unprovided|unresolved|disputed)\b|\b(?:not|no|never)\s+(?:been\s+)?(?:supplied|provided|given|declared|stated)|\bno\s+(?:\w+\s+){0,4}(?:declaration|statement|mass|weight|biography)\b|미상|미지정|미해결|불확실|(?:선언|명시|지정|제공|주어지|공급)\s*(?:되지|되지도|되지\s*않|되지\s*않았|하지|하지\s*않|않|없)|(?:명시|주어지|제공)\S*\s*않|알\s*수\s*없', re.I)
_SUPPLIED = re.compile(r'\b(?:supplied|provided|declared|stated|explicit|report(?:ed|ing)|self-described|self-identification|requester)\b|제공|명시|선언|밝힌|밝혔|진술|요청자|스스로', re.I)
_ADULT = re.compile(r'\badult\b|성인', re.I)
_HUMAN = re.compile(r'\b(?:person|human|adult|porter|sitter|photographer|worker|man|woman)\b|사람|성인|짐꾼|피사체|사진가|인물', re.I)
_STOP = set('a an the its their this that same already independently identified declared existing selected specified complete whole of on in for to with and source original material physical object carrier tool property adult subject main subject retained retain keeps keep mass weight is has have as by from at belonging attached supplied value numeric number quantity claim earlier later stated condition conditions currently exact any own only part contextual photograph context person portrait'.split())
_NUM_WORDS = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split())}
_NUM_WORDS.update(dict(twenty=20, thirty=30, forty=40, fifty=50, sixty=60, seventy=70, eighty=80, ninety=90))
_NW = '|'.join(sorted([*_NUM_WORDS, 'hundred', 'thousand'], key=len, reverse=True))
_QUANTITY = re.compile(r'(?P<value>\d+(?:\.\d+)?|(?:'+_NW+r')(?:[ -]+(?:'+_NW+r'))*)[ -]*(?P<unit>kilograms?|grams?|kg\b|g\b|킬로그램|그램)', re.I)
_UNITS = {'kilogram': 'kg', 'kilograms': 'kg', 'kg': 'kg', '킬로그램': 'kg', 'gram': 'g', 'grams': 'g', 'g': 'g', '그램': 'g'}


def _sentences(text):
    # Decimal points are not sentence boundaries.
    return [x.strip() for x in re.split(r'(?<!\d)[.!?](?!\d)|[;\n]', text) if x.strip()]


def _focus(text):
    m = re.search(r'^Photographic role:\s*(.*?)(?=\nScene context:|\Z)', text, re.S)
    return m.group(1) if m else text


def _positive(text):
    """Local polarity, retaining affirmative conjuncts before a later denial."""
    text = _QUOTES.sub(lambda m: ' ' * len(m.group()), text)
    out = []
    for clause in _sentences(text):
        # Korean suffix negation belongs to the last predicate conjunct. This
        # avoids erasing a migration because a later birthplace is rejected.
        clause = re.sub(r'(?:유지하며|보존하며|유지하되|보존하되|하고|하지만|반면|다만)', ';', clause)
        for part in clause.split(';'):
            # An object-local negative adjunct ending in -지 않고 does not
            # negate an earlier supplied biography in the same sentence.
            part = re.sub(r'\S{1,24}(?:을|를|으로|로)\s+(?:바꾸지|만들어내지|추론하지|부여하지)\s*않고', ' ', part)
            m = re.search(r'\b(?:distinct\s+from|rather\s+than|as\s+opposed\s+to|not\s+to\s+be\s+confused\s+with|without|excluding|exclude|do\s+not|does\s+not|cannot|can\s+not|with\s+no|no(?!\s+longer)|not(?!\s+only)|never|neither)\b', part, re.I)
            if m:
                part = part[:m.start()]
            # A suffix denial masks only this predicate conjunct, not the
            # preceding separately retained field. Unknown state stays separate.
            if re.search(r'(?:하지|되지|주어지지|명시되지|선언되지|제공되지|지정되지)\s*않|하지\s*말|제공하지|부여하지|취급하지|바꾸지|만들어내지|지정하지|요청하지|입증하지|확정하지|공급하지|추론하지', part):
                continue
            out.append(part)
    return '. '.join(out)


def _quantities(text):
    rows = []
    for m in _QUANTITY.finditer(text):
        raw = m.group('value').lower()
        if re.fullmatch(r'\d+(?:\.\d+)?', raw):
            val = float(raw)
        else:
            total = group = 0
            for word in re.split(r'[ -]+', raw):
                if word == 'hundred': group = max(group, 1) * 100
                elif word == 'thousand': total += max(group, 1) * 1000; group = 0
                else: group += _NUM_WORDS[word]
            val = float(total + group)
        rows.append({'value': val, 'unit': _UNITS[m.group('unit').lower()], 'quote': m.group(), 'start': m.start(), 'end': m.end()})
    return rows


def _unit_values(rows):
    return [(q['value'], q['unit']) for q in rows]


def _words(text):
    return {w.casefold() for w in re.findall(r'[A-Za-z]+', text) if len(w) > 1 and w.casefold() not in _STOP}


def _primary(units):
    facts, constraints = [], []
    for u in units:
        p, t = u.get('pointer', ''), u.get('text', '')
        if not t: continue
        if p == '/content/application_contract': constraints.append(copy.deepcopy(u))
        elif re.match(r'^/content/(?:en$|ko$|definition$|concept_units(?:/|$)|semantic_relations(?:/|$)|embedding_text$|components/|semantics/)', p): facts.append(copy.deepcopy(u))
    return facts, constraints


def _english(facts):
    return next((u['text'] for u in facts if u['pointer'] == '/content/en'), '')


def _effect_role(role, effects):
    prefixes = {'publication_caption': ('publication.caption', 'caption.context'), 'declared_background': ('identity.background', 'identity.origin'), 'physical_mass': ('physical.mass',)}[role]
    return any(p.get('property', '').startswith(prefixes) for p in effects.get('properties', []))


def _background_fields(text, *, source=False):
    """Typed predicates; prohibitions/unknown fields cannot add a subtype."""
    t = _positive(text)
    fields = set()
    if re.search(r'language.{0,35}(?:household|use|history|background)|(?:household|speaking).{0,35}(?:language|history)|언어\s*(?:사용|배경|이력)|(?:가정|가구).{0,28}(?:한국어|스페인어|언어)', t, re.I): fields.add('language')
    if re.search(r'self[- ](?:described|identif)|identif\w*.{0,30}cultural|(?:heritage|cultural affiliation|cultural self-identification)|스스로.{0,20}(?:밝|문화)|문화적?\s*(?:배경|소속|유산|자기)|문화\s*공동체', t, re.I): fields.add('culture')
    if re.search(r'different places.{0,35}successive|(?:moving|moved|migration|migrated).{0,70}(?:from|history)|(?:from).{1,30}(?:to).{1,30}(?:childhood|life stage)|이주|서로\s*다른.{0,16}(?:시기|장소)', t, re.I): fields.add('migration')
    if re.search(r'\bbirthplace\b|\bborn\b|place of birth|출생지|출생이라고|태어', t, re.I): fields.add('birthplace')
    if re.search(r'\b(?:lived|resided|residence)\b|거주|살았|\d+년간\s*살|년간\s*살았|기간.{0,12}살았', t, re.I): fields.add('residence')
    if re.search(r'upbringing|grew up|raised in|childhood (?:city|place|home)|place.{0,12}childhood|성장\s*(?:지역|도시|지)|자랐|자란|어린\s*시절을\s*보낸', t, re.I): fields.add('upbringing')
    if not fields and re.search(r'personal (?:place of )?origin|place of origin|hometown|개인적?\s*출신|고향', t, re.I): fields.add('origin')
    # Time of language exposure is not geographical childhood/home geography.
    if 'language' in fields: fields.discard('upbringing')
    if source:
        # Source family comes from its affirmative main assertion. Later
        # explanations may discuss separately unspecified neighboring fields.
        if 'migration' in fields: return {'migration'}
        if 'language' in fields: return {'language'}
        if 'culture' in fields: return {'culture'}
    return fields



def _biographical_literals(text):
    # Only direct name-bearing predicates yield fixed values. Generic phrases
    # such as "a supplied place" are parameters, not invented place names.
    positive = _positive(text)
    result = []
    name = r"([A-Z][\w’'-]*(?: [A-Z][\w’'-]*)*)"
    for field, head in [('birthplace', r'\bborn in\s+'), ('upbringing', r'\b(?:raised in|grew up in)\s+'), ('residence', r'\b(?:lived in|resided in)\s+')]:
        for match in re.finditer(head + name, positive):
            result.append((field, match.group(1)))
    return result


def _date_literals(text):
    # No dates are manufactured from archive styling or source metadata.
    return re.findall(r'(?<![\w\d])(?:1[6-9]\d{2}|20\d{2})(?:-\d{2}-\d{2})?(?![\w\d])', _positive(text))


def _background_owner(focus):
    # Possessive declaration ownership, not every mentioned human noun.
    if re.search(r"photographer[’']s|사진가의|사진작가의|촬영자의", focus, re.I): return 'photographer'
    if re.search(r"author[’']s|작가의\s*(?:약력|출생|성장)", focus, re.I): return 'author'
    return 'depicted_subject'


def _physical_predicate_text(text):
    # Visual/compositional weight is a layout relation, not an independently
    # declared physical quantity. Remove only that local noun phrase: a later
    # literal physical declaration in the same request must remain available.
    t = _positive(text)
    # Unknown mass is not an affirmative property. Mask the local predicate,
    # retaining a separately declared luggage quantity beside an unknown body.
    t = re.sub(r'\b(?:unknown|unstated|undeclared|unspecified)\s+(?:(?:physical|body)\s+)?(?:mass|weight)\b|\b(?:(?:physical|body)\s+)?(?:mass|weight)(?:\s+of\s+[^,.!?;\n]{1,24})?\s*(?:,\s*which\s+is|\s+is|\s+remains|\s+was|\s+has\s+been)?\s+(?:unknown|unstated|undeclared|unspecified)\b|(?:(?:신체|물리)\s*)?(?:질량|무게)(?:은|는|이|가)?\s*(?:미상|미지정)', ' ', t, flags=re.I)
    return re.sub(r'\b(?:visual(?:ly)?|compositional|optical|apparent|emotional|metaphorical)\s+(?:mass(?:es)?|weight(?:s|y)?)\b|(?:시각적(?:인)?|구도상(?:의)?|감정적(?:인)?|정서적(?:인)?)\s*(?:질량|무게|중량)', ' ', t, flags=re.I)


def _mass_kind(text):
    t = _physical_predicate_text(text)
    if re.search(r'change.{0,25}(?:physical )?mass|mass change|became.{0,50}(?:lighter|heavier)|mass.{0,25}from.{0,30}to|질량의?\s*변화|질량이\s*변|가벼워졌|무거워졌', t, re.I): return 'change'
    if re.search(r'mass comparison|(?:heavier|lighter)\s+(?:in physical mass\s+)?than|비교|보다.{0,18}(?:무겁|가볍)', t, re.I): return 'comparison'
    if re.search(r'physical heaviness(?: or |/)lightness|physically\s+(?:lightweight|light|heavy|heavier|lighter)|physical\s+(?:heaviness|lightness)|물리적으로\s*(?:가볍|무겁)|물리적\s*(?:무거움|가벼움)', t, re.I): return 'qualitative'
    if _quantities(t) or re.search(r'complete declared physical mass|declared physical mass as a property|선언된\s*물리\s*질량\s*전체', t, re.I): return 'numeric'
    return None


def _mass_positive(text):
    t = _physical_predicate_text(text)
    return bool(re.search(r'physical (?:mass|weight|heaviness|lightness)|net mass|(?:declared|declares).{0,45}(?:mass|weight)|physically\s+(?:light|heavy|heavier|lighter)|\b(?:kilograms?|grams?|kg)\b|질량|물리적\s*(?:무게|무거움|가벼움)|물리적으로\s*(?:가볍|무겁)|킬로그램|그램', t, re.I))


def _unknown_mass(text):
    # Relation-local status: do not let a numeric declaration's epistemic
    # disclaimer ("not visually certified") erase its positive mass.
    return bool(re.search(r'(?:no|unknown|unstated|undeclared|unspecified).{0,40}(?:physical\s+)?(?:mass|weight)|(?:mass|weight).{0,35}(?:unknown|unstated|undeclared|unspecified)|(?:mass|weight).{0,30}(?:not|no).{0,15}(?:supplied|declared|stated)|(?:질량|무게).{0,25}(?:선언|명시|주어지|지정).{0,12}(?:않|없)|(?:질량|무게).{0,16}(?:미상|미지정)', text, re.I))


def _caption_affirmative_text(text):
    # A family noun before a denied/absent request is not positive evidence.
    # Mask only the denied relationship, preserving a separate affirmative
    # caption clause and denials of unrelated predicates such as pixel text.
    t = re.sub(r'(?:external|publication|editorial|accompanying|exhibition)\b[^.!?;\n]{0,45}?\b(?:caption|cutline|wording|copy|description)\b\s+(?:(?:(?:is|was|remains|has\s+been)\s+)?(?:not\s+(?:(?:being|to\s+be)\s+)?(?:requested|required|wanted|provided|supplied|included|added|used)|absent|unrequested|unsupplied)|(?:should|must|will|would)\s+not\s+be\s+(?:requested|required|provided|included|added|used))\b', ' ', text, flags=re.I)
    return _positive(t)


def _external(text):
    t = _caption_affirmative_text(text)
    return bool(re.search(r'caption in the surrounding article|(?:external|publication|editorial|accompanying)\b[^.!?;\n]{0,45}\b(?:caption|cutline|wording|copy|description)\b|\bcaption\b[^.!?;\n]{0,40}(?:outside|publication)|(?:외부|게재|편집|게시)[^.!?;\n]{0,25}(?:캡션|게시\s*설명|설명|문구)|사진에\s*붙는\s*게시\s*설명', t, re.I))


def _caption_components(text):
    t = _caption_affirmative_text(text)
    kinds = set()
    for name, pattern in {
        'archive': r'\barchive\b|\barchival\b|자료사진|자료[·\s]|기록\s*날짜|기록\s*사진',
        'staged': r'\bstaged\b|staging|\bposed\s+(?:illustration|photograph|image|portrait)|연출|미니어처\s*시연',
        'illustrative': r'illustrati\w*|예시\s*(?:이미지|사진)|예시·',
        'event_history': r'event history|reopening|resumption|return of.{0,20}service|사건\s*이력|재개장|재개일|서비스.{0,16}다시\s*시작',
        'quotation': r'\b(?:quoted|quotation|quote|statement|testimony)\b|인용|발언',
        'credit': r'\bcredits?\b|photographer attribution|authorship|촬영자\s*귀속|사진가\s*크레디트|크레디트',
        'place': r'\b(?:location|clinic|place)\b|진료소\s*이름|촬영\s*장소|제공된\s*장소',
        'observed_content': r'visible content|depicted (?:activity|actions?)|observed.action|보이는\s*내용|묘사된\s*(?:활동|행동)',
    }.items():
        if re.search(pattern, t, re.I): kinds.add(name)
    if re.search(r'(?:capture|archive|established|supplied).{0,20}date|촬영일|기록\s*날짜', t, re.I): kinds.add('capture_date')
    if re.search(r'uncertain.{0,35}(?:photographer|attribution)|disputed authorship|불확실.{0,25}(?:촬영자|귀속)|논쟁.{0,20}(?:저자|귀속)', text, re.I): kinds.add('uncertain_attribution')
    return kinds


class Semantic:
    """Compile bounded source/query relationships and compare whole contracts."""
    def __init__(self, masker=None):
        self.masker = masker

    def _request(self, role, text):
        if role not in _ROLES or not isinstance(text, str): return None
        focus = _focus(text)
        # Incoming legacy masking can erase earlier Korean affirmative clauses.
        # Local predicate polarity above remains authoritative for these domains.
        base = {'role': role, 'raw_text': text, 'focus': focus, 'native_approval': False}
        if role == 'declared_background':
            fields = _background_fields(focus)
            quoted = bool(_QUOTES.search(focus) and re.search(r'lettering|book cover|표지|글자', focus, re.I))
            unknown = bool(re.search(r'(?:hometown|background|biography|life history|personal origin).{0,40}(?:unknown|unspecified|not supplied|unassigned)|(?:고향|배경|약력|이력|출신지).{0,25}(?:미상|지정되지|주어지지|제공하지|지정하지)', focus, re.I))
            evidence = _positive(focus)
            if not fields and not (quoted or unknown): return None
            # Source declaration in scene context may back an affirmed predicate;
            # merely discussing a supplied garment/appearance does not supply it.
            supplied = bool(fields and (_SUPPLIED.search(evidence) or _SUPPLIED.search(_positive(text))) and not unknown)
            return {**base, 'fields': sorted(fields), 'owner': _background_owner(focus), 'status': 'quoted' if quoted else 'unknown' if unknown else 'supplied' if supplied else 'unproven', 'adult': bool(_ADULT.search(text)), 'age_status': 'minor' if re.search(r'\b(?:minor|child|underage)\b|미성년|아동|어린이', evidence, re.I) else 'adult' if _ADULT.search(evidence) else 'unspecified', 'time_scope': bool(re.search(r'\b(?:years?|childhood|period|duration)\b|년간|기간|어린\s*시절|가정', text, re.I)), 'ordered_places': bool(re.search(r'from.{1,50}to|에서.{1,35}(?:로|으로)\s*이주', evidence, re.I)), 'attribution_preserved': True, 'fixed_values': _biographical_literals(text)}
        if role == 'physical_mass':
            positive = _physical_predicate_text(focus)
            relevant = _mass_positive(focus)
            unknown = _unknown_mass(focus)
            # Printed literals/metaphors do not become physical mass predicates.
            lettering = bool(_QUOTES.search(focus) and re.search(r'lettering|printed word|표지|단어|글자', focus, re.I))
            if lettering: return {**base, 'status': 'quoted', 'kind': None, 'target_human': False, 'context_declarations': []}
            if not relevant and not unknown: return None
            explicit_human_target = bool(re.search(r'requested target.{0,20}(?:porter|person|human)|요청\s*대상.{0,20}(?:짐꾼|사람|성인)', text, re.I))
            human_only_denied = bool(re.search(r'(?:body mass|신체\s*질량).{0,30}|(?:porter|짐꾼).{0,30}(?:unstated|unknown|미상|명시되지)', text, re.I))
            context_positive = bool(re.search(r'declared mass on|질량은.{0,20}유지|선언된\s*질량.{0,20}유지', positive, re.I))
            target_unknown = explicit_human_target and (_unknown_mass(text) or human_only_denied)
            # The whole source's nonhuman carrier limitation is enforced later.
            return {**base, 'status': 'unknown' if target_unknown or (unknown and not relevant) else 'supplied' if relevant else 'unproven', 'kind': _mass_kind(focus), 'quantities': _quantities(positive), 'positive_text': positive, 'target_human': explicit_human_target or bool(re.search(r'body mass|mass (?:of|on|to).{0,25}(?:adult|person|human|porter)|(?:성인|사람|짐꾼).{0,12}(?:신체\s*)?질량', positive, re.I)), 'context_declarations': [{'kind': 'mass', 'owner': 'other_declared_object', 'quantity_unresolved': not bool(_quantities(positive))}] if target_unknown and context_positive else [], 'scope': 'contents' if re.search(r'contents|net mass|내용물|쌀\s*내용물|자루\s*안\s*쌀', positive, re.I) else 'part' if re.search(r'\blid\b|removable|뚜껑|분리\s*가능', positive, re.I) else 'whole'}
        # Publication interpretation is never a physical inscription request.
        external = _external(focus) or bool(re.search(r'exhibition caption|전시\s*설명문', _caption_affirmative_text(focus), re.I) and re.search(r'outside|separate from|separate.{0,30}(?:anatomy|visible)|설명문.{0,40}별개|사진.{0,40}별개', text, re.I))
        exclusion = bool(re.search(r'(?:do not|without|no).{0,30}(?:external|publication|editorial).{0,25}(?:caption|copy)|(?:외부\s*캡션|게시\s*문구).{0,30}(?:추가하지|요청하지|없이)|캡션이나.{0,20}추가하지', text, re.I))
        quoted_mention = bool(_QUOTES.search(focus) and re.search(r'quoted.{0,30}title|title quoted|phrase.{0,90}(?:title|direction)|인용한\s*제목|제목으로만', focus, re.I))
        if quoted_mention or exclusion and not external:
            return {**base, 'status': 'excluded', 'components': [], 'date_status': 'unknown'}
        if not external: return None
        required = _caption_components(text)
        if re.search(r'repair|pass(?:es|ing)?|teaching|handwashing|수리|건네|가르치|손\s*씻기', _positive(text), re.I): required.add('observed_content')
        return {**base, 'status': 'supplied', 'components': sorted(required), 'date_status': 'unknown' if re.search(r'(?:year|date).{0,20}unknown|no archive date|연도.{0,12}미상|기록\s*날짜.{0,15}제공되지', text, re.I) else 'supplied' if 'capture_date' in _caption_components(text) else 'unspecified', 'depicted_people': bool(re.search(r'volunteers?|gardener|neighbor|nurse|자원봉사자|정원사|이웃|간호사', _positive(text), re.I)), 'visible_action': bool(re.search(r'repair|pass(?:es|ing)?|teaching|handwashing|수리|건네|가르치|손\s*씻기', _positive(text), re.I)), 'date_literals': _date_literals(text), 'supplied_reporting_explanation': bool(re.search(r'(?:supplied|provided|editor).{0,60}(?:statement|quotation|explanation|testimony)|(?:quoted|quotation).{0,45}(?:resident|source|statement)|(?:resident|source).{0,25}statement|제공된.{0,30}(?:발언|인용|설명)|(?:주민|취재\s*출처).{0,15}(?:발언|진술)|인용문은.{0,20}제공', _positive(text), re.I)), 'history_dates': bool(re.search(r'(?:interruption|resumption|reopening).{0,12}dates?|중단일|재개일', _positive(text), re.I))}

    def _source(self, role, units, effects):
        if role not in _ROLES or not _effect_role(role, effects): return None
        facts, constraints = _primary(units)
        if not facts: return None
        en = _english(facts)
        text = en or '\n'.join(u['text'] for u in facts)
        first = _sentences(text)[0] if _sentences(text) else ''
        restriction = '\n'.join(u['text'] for u in constraints)
        base = {'role': role, 'primary_units': facts, 'constraint_units': constraints, 'effects': copy.deepcopy(effects), 'native_approval': False, 'source_text': text}
        if role == 'declared_background':
            fields = _background_fields(first, source=True)
            if not fields or not re.search(r'supplied|stated|explicit|제공|명시', text, re.I): return None
            return {**base, 'fields': sorted(fields), 'owner': 'depicted_subject' if re.search(r'(?:adult.{0,25}(?:portrait )?subject|portrait subject|성인.{0,20}대상|인물사진.{0,12}대상)', text, re.I) else 'unresolved', 'adult_required': bool(_ADULT.search(text)), 'time_required': 'residence' in fields, 'ordered_places_required': 'migration' in fields, 'parameter_preservation': bool(re.search(r'retain|preserv|keep|유지|보존', text, re.I)), 'fixed_values': _biographical_literals(text)}
        if role == 'physical_mass':
            kind = _mass_kind(first)
            if not kind or not _mass_positive(first): return None
            quantities = _quantities(first)
            generic = bool(re.search(r'independently identified existing (?:object|carrier)|Two independently identified existing carriers|독립적으로\s*식별된\s*기존', first, re.I)) and not quantities
            # Qualitative source fixes no value; generic wording may bind only
            # the independently supplied polarity. A fixed heavy ledger may not.
            head = re.split(r'\b(?:has|is declared|is explicitly|the source|retains)\b|,', first, maxsplit=1, flags=re.I)[0]
            head = re.sub(r'^For\s+', '', head, flags=re.I)
            fixed_anchor = sorted(_words(head)) if not generic else []
            return {**base, 'kind': kind, 'generic': generic, 'quantities': quantities, 'fixed_owner_anchor': fixed_anchor, 'nonhuman_required': generic or bool(re.search(r'nonhuman|no.*human target', restriction, re.I)), 'scope': 'contents' if re.search(r'net mass|contained beans|순질량|내용물', first, re.I) else 'part' if re.search(r'removable battery|탈착식\s*배터리', first, re.I) else 'whole', 'qualitative_polarity': 'heavy' if re.search(r'physically heavy|물리적으로\s*무겁', first, re.I) else None, 'constraint_nonempty_numeric': bool(re.search(r'exact original numeric value|numeric value|수치', restriction, re.I)) if kind == 'numeric' else False}
        if not _external(first): return None
        generic = bool(re.search(r'distinguishes visible content from independently supplied context|publication-owned relationship separates observed image content|외부.{0,12}캡션.{0,35}보이는\s*내용.{0,45}독립적으로\s*제공된\s*맥락', text, re.I))
        components = _caption_components(text)
        # Capability is witnessed by the affirmative descriptive fields, not by
        # mentions in application restrictions. Generic optionality is itself a
        # positive primary statement and does not require all classes at once.
        return {**base, 'components': sorted(components), 'date_literals': _date_literals(text), 'generic_optional': generic and bool(re.search(r'It may|Only information actually supplied|optional|수\s*있다|실제로\s*제공된\s*정보만', text, re.I)), 'requires_people_action': bool(re.search(r'identifies the depicted activity|first describes the depicted action|묘사된\s*활동을\s*설명|먼저\s*묘사된\s*행동', first, re.I)), 'requires_reporting_explanation': bool(re.search(r'first describes.{0,70}then attributes a supplied explanation|먼저.{0,35}행동.{0,60}제공된\s*설명.{0,35}취재\s*출처에\s*귀속', text, re.I)), 'requires_history_dates': bool(re.search(r'establishes the interruption and resumption dates|중단일과\s*재개일을\s*확립', text, re.I)), 'requires_known_capture_date': bool(re.search(r'supplies its established capture date|확인된\s*촬영일', text, re.I)), 'requires_status': 'archive' if re.search(r'identifies an archive photograph|자료사진임을\s*명시', first, re.I) else 'illustrative' if re.search(r'labels the photograph as an illustrative image|사진을\s*예시\s*이미지라고\s*표시', first, re.I) else 'portrait' if re.search(r'posed portrait', first, re.I) else None}

    def request(self, role, text):
        req = self._request(role, text)
        if req is None or req.get('status') != 'supplied':
            return None
        patterns = {
            'publication_caption': r'exhibition caption|전시\s*설명문|(?:external|publication|editorial|accompanying)\b[^.!?;\n]{0,45}\b(?:caption|cutline|wording|copy|description)\b|(?:외부|게재|편집|게시)[^.!?;\n]{0,25}(?:캡션|설명|문구)',
            'declared_background': {'birthplace': r'birthplace|place of birth|born|출생지|출생|태어', 'upbringing': r'raised in|upbringing|grew up|childhood city|자랐|자란|성장', 'residence': r'lived|residen\w*|살았|거주', 'migration': r'moving|moved|migrat\w*|이주', 'language': r'language|speaking household|언어|사용하는 가정', 'culture': r'heritage|self-described|self-identif\w*|문화적|스스로 밝힌', 'origin': r'origin|hometown|고향|출신'},
            'physical_mass': r'declared.{0,35}(?:mass|weight)|physical(?:ly)?\s+(?:mass|weight|heavy|light\w*|heavier)|kilograms?|grams?|질량|물리적\s*(?:무게|무거움|가벼움)|물리적으로\s*(?:가볍|무겁)|킬로그램|그램',
        }
        pattern = patterns[role]
        if isinstance(pattern, dict):
            pattern = '|'.join(pattern[f] for f in req.get('fields', []) if f in pattern)
        witnesses = [{'field': 'role_focus', 'start': m.start(), 'end': m.end(), 'quote': m.group()} for m in re.finditer(pattern, req['focus'], re.I)] if pattern else []
        req.update(asserts=True, witnesses=witnesses, focus_offset=(re.search(r'^Photographic role:\s*', text).end() if re.search(r'^Photographic role:\s*', text) else 0))
        return req if witnesses else None

    def source(self, role, units, effects):
        src = self._source(role, units, effects)
        if src is not None:
            allowed_dimensions = {'publication_caption': {'text', 'viewer_outcome'}, 'declared_background': {'identity'}, 'physical_mass': {'material'}}[role]
            prefixes = {'publication_caption': ('publication.caption', 'caption.context'), 'declared_background': ('identity.background', 'identity.origin'), 'physical_mass': ('physical.mass',)}[role]
            src['unresolved_other_effects'] = bool(set(effects.get('dimensions', [])) - allowed_dimensions or any(not p.get('property', '').startswith(prefixes) for p in effects.get('properties', [])))
            src['external_owner_conflict'] = role in {'publication_caption', 'declared_background'} and any(p.get('target') not in {'context', 'publication_context', 'caption_context'} for p in effects.get('properties', []))
            src['evidence'] = copy.deepcopy(src['primary_units'])
            src['retained_constraints'] = copy.deepcopy(src['constraint_units'])
        return src

    def fit(self, req, src):
        if req is None or src is None or req.get('role') != src.get('role'): return 'unproven'
        if src.get('external_owner_conflict'): return 'conflicting'
        if src.get('unresolved_other_effects'): return 'unproven'
        if req.get('status') in {'quoted', 'excluded'}: return 'conflicting'
        if req.get('status') == 'unknown':
            return 'unproven' if req.get('context_declarations') and src.get('generic') else 'conflicting'
        if req.get('status') != 'supplied': return 'unproven'
        role = req['role']
        if role == 'declared_background':
            if req['owner'] != src['owner']: return 'conflicting'
            # Discovery compatibility does not certify an unstated age. The
            # original adult condition remains in primary/evidence and native
            # guards; only an explicitly contradictory child declaration fails.
            if src['adult_required'] and req.get('age_status') == 'minor': return 'conflicting'
            if set(req['fields']) != set(src['fields']): return 'conflicting'
            if src.get('fixed_values') and not set(src['fixed_values']).issubset(set(req.get('fixed_values', []))): return 'conflicting' if req.get('fixed_values') else 'unproven'
            if src['time_required'] and not req['time_scope']: return 'unproven'
            if src['ordered_places_required'] and not req['ordered_places']: return 'unproven'
            return 'supported'
        if role == 'physical_mass':
            if src['nonhuman_required'] and req['target_human']: return 'conflicting'
            if req['kind'] != src['kind']: return 'conflicting'
            if src['generic']:
                if req['kind'] == 'numeric' and not req['quantities']: return 'unproven'
                if req['kind'] == 'change' and not req['quantities']: return 'unproven'
                return 'supported'
            if not set(src['fixed_owner_anchor']).issubset(_words(req['positive_text'])): return 'conflicting'
            if _unit_values(src['quantities']) != _unit_values(req['quantities']): return 'conflicting'
            if src['scope'] != req['scope']: return 'conflicting'
            if src['qualitative_polarity'] == 'heavy' and re.search(r'light|가볍', req['positive_text'], re.I): return 'conflicting'
            return 'supported'
        wanted, found = set(req['components']), set(src['components'])
        if src['requires_known_capture_date'] and req['date_status'] != 'supplied': return 'conflicting' if req['date_status'] == 'unknown' else 'unproven'
        if src.get('requires_reporting_explanation') and not req.get('supplied_reporting_explanation'): return 'unproven'
        if src['requires_history_dates'] and not req['history_dates']: return 'unproven'
        if src.get('date_literals') and src['date_literals'] != req.get('date_literals', []): return 'conflicting' if req.get('date_literals') else 'unproven'
        status = src['requires_status']
        if status and status not in wanted: return 'conflicting'
        if src['requires_people_action'] and not (req['depicted_people'] and req['visible_action']): return 'unproven'
        if wanted - found: return 'unproven'
        return 'supported'
