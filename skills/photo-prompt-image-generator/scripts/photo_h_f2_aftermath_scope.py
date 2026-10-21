"""Bounded bilingual aftermath intent and source compatibility contracts.

These contracts govern advisory material presentation, never source admission.
They read explicit positive text and verified selected-primary fields only.
"""
import re
from photo_h_f2_query_scope import _quoted,analyze

_PAST = re.compile(r'\b(?:prior|earlier|past|completed|finished)\s+(?:\w+\s+){0,2}(?:event|action|operation|process|reception|gathering|meeting|failure)|\b(?:extinguished|snuffed)\s+candle\b|\bpost[- ]event\b|\bafter[- ]event\b|\baftermath\b|\baftereffects?\b|\bafter\b.{0,110}\b(?:ended|finished|over|opened|extinguish\w*|snuff\w*|blown out|gone out|failed|left|completed)|\bonce\b.{0,50}\b(?:over|finished)|\bsettling aftereffect\b|(?:사후|사건\s*(?:이후|뒤)|행사\s*(?:이후|뒤))|(?:끝[난나]|완료된|앞선|이전의?).{0,35}(?:사건|동작|행사|뒤|후|주방|흔적)|(?:사건|행사|동작|모임|회의|파티|리셉션|요리|시도|주문|마법|초|촛불).{0,35}(?:끝난|끝나|꺼진|끈\s*뒤|남은)',re.I)
_TRACE = re.compile(r'\b(?:physical\s+(?:residue|traces?|remnants?|aftermath|aftereffects?)|residual\s+(?:traces?|smoke)|material\s+traces?|kitchen\s+(?:mess|aftermath)|remnants?|residue|aftereffects?|smoke|wax|displaced glassware|traces?\s+(?:left|remaining)|crumbs|pawprints|torn wrapping)\b|(?:물리적|물질적|사후|잔여).{0,12}(?:흔적|잔여물|잔재|여파|연기)|(?:흔적|연기|잔재|부스러기|발자국|포장지)',re.I)
_ACTIVE = re.compile(r'\b(?:ongoing\s+(?:process|action|cause)|(?:action|operation)\s+(?:is\s+)?(?:still\s+)?underway|still\s+in\s+progress)|(?:진행\s*중|진행하는|진행되는)',re.I)
_GENERIC = frozenset(('a an the show photograph use only visible physical material residual residue residues trace traces remnants remnant aftereffect aftereffects aftermath owned own owner its their on of by from in with and or as is are has have been belonging to remaining remains remain left behind once after before earlier prior past post completed complete finished finish ended end over action actions event events operation process support surface initiating cause result stage settling diminishing motion separate distinct rather than arbitrary static stationary pose camera effect photographic role without not depict depicting explicitly declared').split())
_FAMILIES = {
 'candle': re.compile(r'\bcandles?\b|촛불|(?:^|\s)초(?:가|를|의|에|는|\s)',re.I),
 'recipe': re.compile(r'\b(?:recipe|cooking|baking|kitchen)\b|레시피|요리|제빵|주방',re.I),
 'event_setting': re.compile(r'\b(?:party|reception|meeting|gathering|guests?|chairs?|cups?|room)\b|파티|리셉션|모임|회의|손님|의자|컵|공간|방',re.I),
 'other_owner': re.compile(r'\b(?:dog|pawprints?|bread|crumbs?|cutting board|parcel|wrapping|package)\b|발자국|(?:^|\s)개가|(?:^|\s)빵(?:을|이|의|\s)|도마|소포|포장지',re.I),
}
# Each supported owner needs its residual material and support in the same
# affirmative selected source. A boot print cannot become a dog's pawprint and
# soil crumbs cannot become bread. Unknown owners remain unsupported.
_OWNED_TRACES = {
 'dog_pawprints': (
  re.compile(r'\bdog\b|(?:^|\s)개(?:가|의|는|\s)',re.I),
  re.compile(r'\bpawprints?\b|발자국',re.I),
  re.compile(r'\bfloor\b|바닥',re.I)),
 'bread_crumbs': (
  re.compile(r'\bbread\b|\bloaf\b|(?:^|\s)빵(?:을|이|의|\s)',re.I),
  re.compile(r'\bcrumbs\b|부스러기',re.I),
  re.compile(r'\bcutting board\b|도마',re.I)),
 'parcel_wrapping': (
  re.compile(r'\bparcel\b|소포',re.I),
  re.compile(r'\btorn wrapping\b|찢어진\s*포장지',re.I),
  re.compile(r'\btable\b|테이블',re.I)),
}


def owned_traces(text,raw=None):
    raw=text if raw is None else raw
    out=[]
    for family,patterns in _OWNED_TRACES.items():
        groups=[[m for m in pattern.finditer(text) if affirmative(raw,m)] for pattern in patterns]
        if all(groups):
            out.extend({'family':family,'component':i,'start':m.start(),'end':m.end(),'quote':m.group()}
                       for i,matches in enumerate(groups) for m in matches)
    return out
_QUIET = re.compile(r'\bquiet(?:\s+(?:event|party))?\s+(?:room|space|setting)\b|\bquiet\b|조용(?:한|해진)\s*(?:행사\s*)?(?:공간|방)|조용',re.I)
_FAILED = re.compile(r'\b(?:failed\s+(?:\w+\s+){0,2}(?:recipe|baking)|(?:recipe|cooking)\s+failure)\b|레시피.{0,18}실패|실패한.{0,12}(?:요리|제빵|레시피)',re.I)
_KO_GENERIC = re.compile(r'사진\s*역할|장면\s*맥락|사진으로|보여줘|보여주세요|표현해줘|(?:완료된|끝난|앞선|이전의?)\s*(?:사건|동작|행사)(?:이|의|에|을|를)?|주동작(?:이|의)?|사건(?:이|의|에)?|동작(?:이|의)?|끝난\s*(?:후|뒤)|끝나고|(?:잔여물|흔적|잔재|여파|움직임|지지\s*표면|표면)(?:이|을|를|은|에|의|만)?|(?:물리적|물질적|눈에\s*보이는|사후|잔여(?=\s))|가라앉는|남아\s*있는|남겨진|남은|남긴|속한|뒤에|이후|후에|(?:^|\s)(?:그|뒤|후|에|를|을|이|가|만|의|으로|과|와)(?=\s|$)|\s|[.!?;,:·]',re.I)


def affirmative(text,match):
    """An absent/missing counterpart is not a scene or context assertion."""
    tail=text[match['end'] if isinstance(match,dict) else match.end():]
    return not re.match(r'\s*(?:(?:is|are|was|were|remains?)\s+(?:absent\b|missing\b|not\b)|(?:cannot|can[\x27’]t|must\s+not|should\s+not)\s+(?:supply\s+this\s+relation\b|(?:substitute|replace)\b|be\s+(?:used|substituted)\s+as\s+(?:a\s+)?(?:substitute|replacement)\b)|(?:이|가|은|는)?\s*(?:없|아니|없이))',tail,re.I)


def positive_text(text, scope):
    """Retain offsets while excluding quoted, contrasted or negative clauses."""
    chars=[' ']*len(text)
    for row in scope['positive_spans']:
        chars[row['start']:row['end']]=text[row['start']:row['end']]
    for start,end in _quoted(text):chars[start:end]=' '*(end-start)
    for m in re.finditer(r'\b(?:without|excluding|exclude|do\s+not|with\s+no|no(?!\s+longer)|not(?!\s+only))\b[^.!?;\n]*',text,re.I):
        if any(a<=m.start()<b for a,b in _quoted(text)):continue
        chars[m.start():m.end()]=' '*(m.end()-m.start())
    for sentence in re.finditer(r'[^.!?;\n]+',text):
        s=sentence.group();base=sentence.start()
        contrast=re.search(r'아니라|대신|말고|구분해(?:줘|주세요)?',s)
        if contrast:chars[base:base+contrast.end()]=' '*contrast.end()
        if re.search(r'보여주지|요청하지|원하지|넣지|제외해|의미는\s*없|상징적\s*의미는\s*없|아직\s*(?:생기지|없)',s):
            chars[base:sentence.end()]=' '*(sentence.end()-base)
    return ''.join(chars)


def excluded_completed_phase(text,scope):
    """An affirmed ongoing action can explicitly reject completed aftermath.

    Quoted labels do not constrain the physical phase. Return original Unicode
    offsets for both sides; do not turn a negative counterpart into a request.
    """
    positive=positive_text(text,scope)
    active=list(_ACTIVE.finditer(positive))
    if not active:return None
    spans={(r['start'],r['end']) for r in scope['contrast_spans']}
    spans.update((m.start(),m.end()) for m in re.finditer(r'\b(?:not(?!\s+only)|rather than|instead of|without)\b[^.!?;\n]*',text,re.I))
    for sentence in re.finditer(r'[^.!?;\n]+',text):
        contrast=re.search(r'아니라|대신|말고',sentence.group())
        if contrast:spans.add((sentence.start(),sentence.start()+contrast.end()))
    excluded=[]
    for start,end in sorted(spans):
        chars=list(text[start:end])
        for a,b in _quoted(text):
            for i in range(max(start,a),min(end,b)):chars[i-start]=' '
        clause=''.join(chars)
        if _PAST.search(clause) and _TRACE.search(clause):
            excluded.append({'start':start,'end':end,'quote':text[start:end]})
    if not excluded:return None
    return {'phase':'post_event_residue',
            'positive_ongoing_witnesses':[{'start':m.start(),'end':m.end(),'quote':text[m.start():m.end()]} for m in active],
            'excluded_post_event_witnesses':excluded}


def query(text,scope,tokenize,context_extractor):
    positive=positive_text(text,scope)
    past=list(_PAST.finditer(positive));trace=list(_TRACE.finditer(positive))
    if not past or not trace or _ACTIVE.search(positive):return None
    # A future-only claim cannot supply the positive prior event.
    if re.search(r'\bfuture\b|앞으로|아직',positive,re.I):return None
    contexts=context_extractor([{'text':positive}],tokenize)
    modes={};context_witnesses=[]
    for w in contexts:
        if not affirmative(text,w):continue
        mode='optional' if re.search(r'\b(?:optional\w*|may|might|could)\b|선택적|허용',positive[max(0,positive.rfind('.',0,w['start'])+1):],re.I) else 'required'
        modes[w['context']]=mode
        context_witnesses.append({'context':w['context'],'permission':mode,'start':w['start'],'end':w['end'],'quote':text[w['start']:w['end']]})
    for context,pattern in [('supernatural_physical_effect',re.compile(r'\b(?:after|of|from)\s+(?:(?:a|an|the)\s+)?(?:(?:declared|finished|ended|completed)\s+)?spell\b',re.I)),('quiet_event_setting',_QUIET),('failed_recipe',_FAILED)]:
        for m in pattern.finditer(positive):
            if not affirmative(text,m):continue
            modes[context]='required';context_witnesses.append({'context':context,'permission':'required','start':m.start(),'end':m.end(),'quote':text[m.start():m.end()]})
    found={name for name,p in _FAMILIES.items() if any(affirmative(text,m) for m in p.finditer(positive))}
    owned=owned_traces(positive,text)
    owned_families={w['family'] for w in owned}
    if len(owned_families)==1:family=next(iter(owned_families))
    elif owned_families or 'other_owner' in found:family='unproven_owner'
    elif 'candle' in found:family='candle'
    elif 'recipe' in found:family='recipe'
    elif 'former_luxury_decline' in modes:family='luxury_setting'
    elif 'event_setting' in found:family='event_setting'
    else:
        # Unknown scene prose does not silently acquire generic compatibility.
        remainder=_KO_GENERIC.sub('',positive) if re.search('[가-힣]',positive) else ' '.join(set(tokenize(positive))-_GENERIC)
        family='unproven_owner' if remainder.strip(' .,:;!?') else 'generic'
    witnesses=[{'start':m.start(),'end':m.end(),'quote':text[m.start():m.end()]} for m in past+trace]
    return {'phase':'post_event_residue','positive_witnesses':witnesses,
            'excluded_witnesses':scope['contrast_spans'],'owner_scope':'generic_only' if family=='generic' else 'source_scene_required',
            'scene_family':family,'context_permissions':modes,
            'context_witnesses':context_witnesses,
            'scene_witnesses':[{'family':name,'start':m.start(),'end':m.end(),'quote':text[m.start():m.end()]} for name,pattern in _FAMILIES.items() for m in pattern.finditer(positive) if affirmative(text,m)]+owned,
            'language':'ko' if re.search('[가-힣]',positive) else 'en'}


def source_profile(units,requirements,tokenize):
    """Scene/context facts stay attached to the complete selected primary text."""
    texts=[(u['text'],positive_text(u['text'],analyze(u['text'],tokenize))) for u in units]
    def has(pattern):return any(affirmative(raw,m) for raw,positive in texts for m in pattern.finditer(positive))
    categories={w['context'] for w in requirements}
    found={name for name,p in _FAMILIES.items() if has(p)}
    owned={w['family'] for raw,positive in texts for w in owned_traces(positive,raw)}
    if len(owned)==1:family=next(iter(owned))
    elif owned:family='unproven_owner'
    elif 'candle' in found:family='candle'
    elif has(_FAILED):family='recipe'
    elif 'former_luxury_decline' in categories:family='luxury_setting'
    elif 'event_setting' in found:family='event_setting'
    elif 'other_owner' in found:family='unproven_owner'
    else:family='generic'
    return {'scene_family':family,'requires_declared_event_scene':family in _OWNED_TRACES}


def extra_requirements(units,tokenize):
    """Bounded source relations beyond symbols: a quiet setting or failed recipe."""
    import hashlib
    out=[]
    patterns=(('quiet_event_setting',re.compile(r'\bquiet\s+after[- ]event\s+state\b|행사\s*직후\s*조용해진\s*공간',re.I)),('failed_recipe',_FAILED))
    for unit in units:
        text=unit['text'];positive=positive_text(text,analyze(text,tokenize))
        for context,pattern in patterns:
            for m in pattern.finditer(positive):
                if not affirmative(text,m):continue
                out.append({k:v for k,v in unit.items() if k!='text'}|{'context':context,'start':m.start(),'end':m.end(),'quote':m.group(),'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'modality':'affirmative'})
    return out


def compatibility(contract,req):
    if contract['phase']!='post_event_residue':return False,'not_completed_physical_residue'
    family=contract.get('source_profile',{}).get('scene_family','generic')
    wanted=req.get('scene_family','generic')
    if wanted!='generic' and family!=wanted:return False,'unproven_scene_or_owner'
    if wanted=='generic' and contract.get('source_profile',{}).get('requires_declared_event_scene'):
        return False,'owned_event_scene_not_declared'
    requirements={w['context'] for w in contract.get('context_requirements',[])}
    permitted=req.get('context_permissions',{})
    if not requirements.issubset(permitted):return False,'additional_context_not_declared'
    required={c for c,mode in permitted.items() if mode=='required'}
    if not required.issubset(requirements):return False,'required_context_not_witnessed'
    return True,'compatible_source_witnesses'
