"""Source-witnessed bilingual aftermath ordering and material presentation.

Verified selected-RID primary fields supply declared phase, scene and context.
Residual motion is distinct from its initiating action. Material witnesses are
advisory and establish neither causal history from pixels nor native approval.
"""
import re
from photo_h_f2_query_scope import _quoted, analyze
import photo_h_f2_aftermath_scope as aftermath_scope

RECIPE = 'photo-h-f2-event-phase-order/v7'
_RESIDUE = re.compile(r'\b(?:residue|residual traces?|physical traces?|remnants?|aftereffects?)\b', re.I)
_PRIOR = re.compile(r'\b(?:prior|past|earlier|completed|finished)\s+(?:event|action|operation|process)\b', re.I)
_ACTIVE = re.compile(r'\b(?:(?:ongoing|unfinished)\s+(?:\w+\s+){0,2}(?:process|action|operation|event)|emerging\s+target\s+(?:form|surface)|undergoing\s+(?:a\s+)?transformation|mid[- ]action|(?:action|operation)\s+(?:(?:is|remains?)\s+)?(?:visibly\s+)?underway)\b|진행\s*중|진행하는|진행되는|형성\s*중', re.I)
_AFTER = re.compile(r'\b(?:after[- ]event|after an event|post[- ]event|aftermath|settling aftereffect|(?:completed|finished)\s+(?:event|action|operation|process))\b|\b(?:after|once)\b.{0,110}\b(?:finished|completed|fully opened)\b|(?:행사|동작)\s*(?:직후|뒤|이후)|동작이?\s*끝난\s*뒤', re.I)
# These verbs name termination, not a material state such as burned or wet.
_TERMINATION = re.compile(r'\bjust[- ](?:snuffed|extinguished)\b|\b(?:extinguished|snuffed)\s+candle\b|꺼진\s*(?:촛불|초)', re.I)
_MATERIAL = re.compile(r'\b(?:residue|(?:residual\s+)?traces?|remnants?|smoke|kitchen mess|pawprints?|crumbs|torn wrapping)\b|흔적|잔여물|잔재|연기|발자국|부스러기|찢어진\s*포장지', re.I)
_RELATION = re.compile(r'\b(?:on|across|from|of|with|visible)\b|(?:촛불|초|심지)의|(?:바닥|도마|테이블)\s*위에', re.I)
_GENERIC = frozenset(('a an the of from on in with for and or is are as its their one '
                     'owned owner physical visible observed observable residual residue trace traces '
                     'remnant remnants aftereffect aftereffects explicitly declared earlier prior past '
                     'completed finished event events action actions process operation '
                     'photographic photograph role show depict retain remains').split())
_NEGATIVE = re.compile(r'\b(?:not(?!\s+only\b)|never|no|absent|missing|without|unless|if|suppose|imagine|example)\b|아니|없|않|가정|예시', re.I)


def _span(text, match):
    return {'start': match.start(), 'end': match.end(), 'quote': match.group()}


def request(text, scope, tokenize):
    return aftermath_scope.query(text,scope,tokenize,context_requirements)


def compile_contract(document, tokenize):
    # D starts with the actual primary meaning, before lookup labels and examples.
    end = re.search(r'[.?!;\n]', document)
    assertion = document[:end.start() if end else len(document)]
    if not assertion.strip() or _quoted(assertion) or _NEGATIVE.search(assertion):
        return None
    scope = analyze(assertion, tokenize)
    protected = [(r['start'], r['end']) for r in scope['contrast_spans']]
    def direct(pattern):
        return [m for m in pattern.finditer(assertion) if not any(a <= m.start() < b for a, b in protected)]
    active = direct(_ACTIVE)
    after = direct(_AFTER) + direct(_TERMINATION)
    material = direct(_MATERIAL)
    relation = direct(_RELATION)
    if after and material and relation and not active:
        return {'phase': 'post_event_residue', 'assertion': {'start': 0, 'end': len(assertion), 'quote': assertion},
                'phase_witnesses': [_span(document, m) for m in after],
                'material_witnesses': [_span(document, m) for m in material],
                'relation_witnesses': [_span(document, m) for m in relation]}
    if active and not after:
        return {'phase': 'ongoing_action', 'assertion': {'start': 0, 'end': len(assertion), 'quote': assertion},
                'phase_witnesses': [_span(document, m) for m in active]}
    return None


def compile_contracts(documents, tokenize, *, source_units):
    contracts = {}
    for key, text in documents.items():
        contract = compile_contract(text, tokenize)
        if contract is None and not ((_AFTER.search(text) or _TERMINATION.search(text)) and _MATERIAL.search(text)):
            continue
        units=source_units(key)
        primary=[(unit,compile_contract(unit['text'],tokenize)) for unit in units]
        witnessed=[(unit,c) for unit,c in primary if c is not None]
        if not witnessed:continue
        phases={c['phase'] for _,c in witnessed}
        if len(phases)>1:
            contract={'phase':'mixed_phase','primary_phase_evidence':[dict(unit)|{'contract':c} for unit,c in witnessed]}
        else:
            contract=dict(witnessed[0][1]);contract['primary_phase_evidence']=[dict(unit)|{'contract':c} for unit,c in witnessed]
        if contract['phase'] == 'post_event_residue':
            contract['context_requirements'] = context_requirements(units, tokenize)+aftermath_scope.extra_requirements(units,tokenize)
            contract['source_profile']=aftermath_scope.source_profile(units,contract['context_requirements'],tokenize)
        contracts[key] = contract
    return contracts


def order_phase(rows, text, scope, contracts, tokenize):
    trace = {'schema': RECIPE, 'applied': False, 'candidate_filter': False,
             'score_changes': 0, 'native_approval': False}
    req = request(text, scope, tokenize)
    if req is None:
        exclusion=aftermath_scope.excluded_completed_phase(text,scope)
        if exclusion is None:return rows,trace
        rejected={row['id']:contracts[row['id']] for row in rows
                  if row['id'] in contracts and contracts[row['id']]['phase']=='post_event_residue'}
        result=sorted(rows,key=lambda row:row['id'] in rejected)
        trace.update({'excluded_phase':exclusion,'rejected_completed_sources':rejected,
                      'stable_within_groups':True,'reason':'explicitly_excluded_completed_phase',
                      'applied':[row['id'] for row in rows]!=[row['id'] for row in result]})
        return result,trace
    trace['request'] = req
    trace['context_qualified'] = {row['id']: contracts[row['id']] for row in rows
        if row['id'] in contracts and contracts[row['id']].get('context_requirements')}
    decisions={key:aftermath_scope.compatibility(c,req) for key,c in contracts.items() if c['phase']=='post_event_residue'}
    trace['source_compatibility']={key:{'compatible':ok,'reason':reason} for key,(ok,reason) in decisions.items()}
    positive = {row['id']: contracts[row['id']] for row in rows if decisions.get(row['id'],(False,''))[0]}
    if not positive:
        trace['reason'] = 'no_positive_source_contract'
        return rows, trace
    negative = {row['id']: contracts[row['id']] for row in rows
                if row['id'] in contracts and contracts[row['id']]['phase'] == 'ongoing_action'}
    result = sorted(rows, key=lambda row: 0 if row['id'] in positive else 2 if row['id'] in negative else 1)
    trace.update({'positive': positive, 'conflicting': negative, 'stable_within_groups': True})
    if [r['id'] for r in result] == [r['id'] for r in rows]:
        trace['reason'] = 'order_already_satisfies_phase_contract'
    else:
        trace['applied'] = True
    return result, trace


def present_material(rows, phase):
    """At most eight sources; never pad a supported phase request with unknowns.

    `rows` remains the complete scored, CID-deduplicated order. Only the material
    presentation is bounded here. A recognized request with zero positive source
    contracts deliberately returns zero, without another query or fallback.
    Audits independently recompile phase evidence before calling this function.
    """
    if phase.get('schema') != RECIPE:
        raise ValueError('foreign event-phase projection policy')
    supported = phase.get('request') is not None
    excluded = phase.get('rejected_completed_sources', {})
    positive = phase.get('positive', {}) if supported else {}
    available = sum(row['id'] in positive for row in rows) if supported else sum(row['id'] not in excluded for row in rows)
    limit = min(8, available)
    selected = rows[:limit]
    if supported and any(row['id'] not in positive for row in selected):
        raise ValueError('phase-witnessed material is not the positive order prefix')
    if any(row['id'] in excluded for row in selected):
        raise ValueError('explicitly rejected completed phase entered material')
    projection = {'schema': 'photo-h-f2-material-projection/v1',
                  'mode': 'post_event_source_witnesses' if supported else 'explicit_phase_exclusion' if excluded else 'ordinary_top8',
                  'maximum': 8, 'available': available, 'returned': len(selected),
                  'unfilled': 8 - len(selected),
                  'reason': ('source_witnesses_only' if available else 'no_positive_source_contract') if supported else 'completed_sources_explicitly_excluded' if excluded else 'ordinary_query',
                  'returned_ids': [row['id'] for row in selected],
                  'unknown_phase_padding': not supported, 'pre_search_filter': False,
                  'additional_search_calls': 0, 'native_approval': False,
                  'context_qualified_count': len(phase.get('context_qualified', {})) if supported else 0,
                  'withheld_context_requirements': {key: value['context_requirements']
                      for key, value in phase.get('context_qualified', {}).items() if key not in positive} if supported else {},
                  'accepted_context_requirements': {key:value['context_requirements'] for key,value in positive.items() if value.get('context_requirements')},
                  'query_scene_family':phase.get('request',{}).get('scene_family') if supported else None,
                  'query_context_permissions':phase.get('request',{}).get('context_permissions',{}) if supported else {},
                  'explicit_phase_exclusion':phase.get('excluded_phase'),
                  'excluded_completed_ids':list(excluded)}
    return selected, projection


def primary_units(record, realization_id, source_sha256):
    """Exact selected-RID primary fields; lookup-only names/tags are not facts."""
    meaning = record['meaning']
    return [{'candidate_id': record['id'], 'realization_id': realization_id,
             'source_sha256': source_sha256, 'pointer': pointer, 'literal_id': literal,
             'text': meaning['literals'][literal]}
            for pointer, literal in sorted(meaning['primary'][realization_id].items())]


_CONTEXT_EFFECT = re.compile(r'\b(?:spell|magic(?:al)?|supernatural|enchanted)\s+(?:physical\s+|visible\s+)?(?:residue|traces?|remnants?|smoke|aftereffects?)\b', re.I)
_EFFECT_ORIGIN = re.compile(r'\b(?:residue|traces?|remnants?|smoke|aftereffects?)\s+(?:(?:left|created|produced|remaining)\s+)?(?:by|from|of|after)\s+(?:an?\s+|the\s+)?(?:spell|magic(?:al)?(?:\s+process)?|supernatural(?:\s+process)?)\b', re.I)
_KO_CONTEXT = re.compile(r'(?:마법(?:적)?|주술(?:적)?|초자연(?:적)?)(?:의)?\s*(?:(?:물리적|가시적)\s*)?(?:잔여물|잔여\s*흔적|잔흔|흔적|연기)')
# An authored interpretive relation is an extra context, even when the depicted
# physical object is ordinary. Death vocabulary alone asserts neither symbolism
# nor a death event. Keep that distinction separate from supernatural causation.
_SYMBOL_OBJECT = r'(?:mortality|vanitas|memento\s+mori|death)'
_SYMBOL_OBJECTS = _SYMBOL_OBJECT + r'(?:\s+(?:or|and)\s+' + _SYMBOL_OBJECT + r')*'
_SYMBOL_MEANING = re.compile(r'\b(?:supports?|supporting|conveys?|conveying|evokes?|evoking|represents?|representing)\s+(?:(?:a|the)\s+)?' + _SYMBOL_OBJECTS + r'\s+(?:symbolic\s+meaning|meaning|symbolism|theme|interpretation)\b', re.I)
_SYMBOL_RELATION = re.compile(r'\b(?:(?:symbols?|allegory|emblem)\s+of\s+(?:(?:a|the)\s+)?' + _SYMBOL_OBJECTS + r'|(?:symbolizes?|symbolizing)\s+' + _SYMBOL_OBJECTS + r')\b', re.I)
_SYMBOL_COMPOUND = re.compile(r'\b' + _SYMBOL_OBJECT + r'\s+(?:symbols?|symbolism|allegory)\b', re.I)
_KO_SYMBOL = re.compile(r'(?:죽음|유한성|바니타스|메멘토\s*모리)(?:의)?\s*(?:상징|알레고리)')
# A source can tie fresh residue to a separately authored history of opulence.
# Ordinary wear, dust, velvet, metal or luxury objects alone assert no such past.
_LUXURY_OBJECT = r'(?:luxury|opulence|splendou?r)'
_LUXURY_HISTORY = re.compile(r'\b(?:former|past|faded|lost|decaying|declining)\s+' + _LUXURY_OBJECT + r'(?:\s+(?:decline|decay))?\b', re.I)
_LUXURY_DECLINE = re.compile(r'\b(?:decline|decay|fading|loss)\s+of\s+(?:(?:a|the)\s+)?(?:(?:former|past)\s+)?' + _LUXURY_OBJECT + r'\b', re.I)
_ONCE_LUXURIOUS = re.compile(r'\bonce[- ](?:luxurious|opulent|splendid)\s+(?:\w+\s+){0,2}in\s+(?:decline|decay)\b', re.I)
_KO_LUXURY_HISTORY = re.compile(r'(?:과거(?:의)?\s*(?:호화|사치|영화)(?:로움)?(?:의)?\s*(?:쇠락|퇴락|몰락)|(?:쇠락한|퇴락한|몰락한)\s*(?:호화|사치|영화))')
_CLAUSE = re.compile(r'[.!?;,\n]|\b(?:and|but|however|yet|while)\b', re.I)
_NEGATED = re.compile(r'\b(?:not(?!\s+only\b)|no|never|without|absent|missing)\b', re.I)
_TAIL_NEGATED = re.compile(r'^\s*(?:(?:is|are|was|were|remains?)\s+(?:not\b|absent\b|missing\b)|(?:must|should|does|do)\s+not\b|(?:이|가|은|는)?\s*(?:아니|없|없이))', re.I)
_STAGE_DEVICE = re.compile(r'^\s+(?:show|trick|act|performance|lantern|marker|hour)\b', re.I)


def context_requirements(units, tokenize):
    """Recognize authored effect, symbolic or historical context, not a tag.

    Witness offsets address the complete field, including later sentences. A
    positive conditional effect still needs authored context; negated, quoted
    or comparison-counterpart mentions supply no affirmative requirement.
    """
    import hashlib
    out = []
    for unit in units:
        text = unit['text']
        protected = _quoted(text) + [(r['start'], r['end']) for r in analyze(text, tokenize)['contrast_spans']]
        patterns = [('supernatural_physical_effect', p) for p in (_CONTEXT_EFFECT, _EFFECT_ORIGIN, _KO_CONTEXT)] + [('mortality_symbolism', p) for p in (_SYMBOL_MEANING, _SYMBOL_RELATION, _SYMBOL_COMPOUND, _KO_SYMBOL)] + [('former_luxury_decline', p) for p in (_LUXURY_HISTORY, _LUXURY_DECLINE, _ONCE_LUXURIOUS, _KO_LUXURY_HISTORY)]
        matches = sorted([(m, context) for context, pattern in patterns for m in pattern.finditer(text)], key=lambda row: row[0].start())
        seen = set()
        for match, context in matches:
            start, end = match.span()
            if (start, end, context) in seen or any(a < end and start < b for a, b in protected):
                continue
            seen.add((start, end, context))
            prior = list(_CLAUSE.finditer(text[:start]))
            beginning = prior[-1].end() if prior else 0
            next_boundary = _CLAUSE.search(text, end)
            ending = next_boundary.start() if next_boundary else len(text)
            before, after = text[beginning:start], text[end:ending]
            if _NEGATED.search(before) or _TAIL_NEGATED.search(after) or _STAGE_DEVICE.match(text[end:]) or not aftermath_scope.affirmative(text,match):
                continue
            out.append({k: v for k, v in unit.items() if k != 'text'} | {
                'context': context, 'start': start, 'end': end,
                'quote': match.group(), 'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
                'modality': 'conditional_or_modal' if re.search(r'\b(?:if|unless|may|might|could)\b', text[max((text.rfind(c,0,start) for c in '.!?\n'),default=-1)+1:start], re.I) else 'affirmative'})
    return out
