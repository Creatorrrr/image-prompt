"""Pure offset-preserving reflection-identity and tilt-owner witnesses.

Adapted from the reviewed private shadow; this module has no storage or corpus
access. It ranks only direct primary source text corroborated by a selected-RID
effect supplied by the caller.
"""

from __future__ import annotations



import re



# Pattern and span functions reviewed in single_property_witness_shadow_v3.py.

FLAGS = re.IGNORECASE

KO_TILT_VERB = r'기울(?:어(?:져|진|있(?:다)?)?|어진|어졌다|었다|고)|비스듬(?:하|히)|회전(?:하|된|해)'

def span(text: str, start: int, end: int, role: str) -> dict:
    return {'role': role, 'start': start, 'end': end, 'quote': text[start:end]}

def first_spans(text: str, patterns: list[tuple[str, str]]) -> list[dict]:
    found = []
    for role, pattern in patterns:
        match = re.search(pattern, text, FLAGS)
        if match:
            found.append(span(text, match.start(), match.end(), role))
    return found

def query_recognizer(text: str) -> dict | None:
    """Recognize a question class and retain its literal, code-point spans."""
    imperative = re.search(r'^\s*(?:find|show|retrieve|select|return|search|look for|choose|identify)\b|'
                           r'^\s*(?:찾아|보여|골라|선택|검색|찾아줘)', text, FLAGS)
    interrogative = bool(re.search(r'[?？]|(?:인가|일까|인가요|있나요|어떤가요|어느\s*쪽인가)\s*$', text))
    if imperative or not interrogative:
        return None
    reflection_context = first_spans(text, [
        ('reflection_context', r'\b(?:mirror|reflection|reflected|selfie|glass)\b'),
        ('reflection_context', r'거울|유리|반사|비친|셀카')])
    identity_alternatives = first_spans(text, [
        ('identity_alternative', r'\b(?:same person|another person|other person|second person|different person|herself|himself|own reflection)\b'),
        ('identity_alternative', r'다른\s*사람|다른\s*인물|본인|자신|같은\s*(?:사람|인물)')])
    if reflection_context and identity_alternatives:
        return {'kind': 'reflection_identity', 'evidence_spans': reflection_context + identity_alternatives}

    head = first_spans(text, [('head_owner', r'\bhead\b'), ('head_owner', r'머리')])
    frame = first_spans(text, [('frame_owner', r'\b(?:frame|horizon|camera roll)\b'),
                               ('frame_owner', r'프레임|수평선|카메라\s*롤')])
    tilt = first_spans(text, [('tilt_request', r'\b(?:tilt|tilted|roll|canted|dutch angle)\b'),
                              ('tilt_request', r'기울|더치\s*앵글')])
    contrast = first_spans(text, [('alternative', r'\b(?:or|rather than|instead of|versus|vs)\b'),
                                  ('alternative', r'아니면|혹은|또는|반면')])
    if head and frame and tilt and contrast:
        return {'kind': 'tilt_owner_disambiguation', 'evidence_spans': head[:1] + frame[:1] + tilt[:1] + contrast[:1]}
    return None

def source_sentences(text: str) -> list[tuple[int, int]]:
    bounds = []
    start = 0
    for match in re.finditer(r'[.!?。！？\n]+', text):
        end = match.end()
        if text[start:end].strip():
            left = start
            while left < end and text[left].isspace():
                left += 1
            right = end
            while right > left and text[right - 1].isspace():
                right -= 1
            if left < right:
                bounds.append((left, right))
        start = end
    if start < len(text):
        left, right = start, len(text)
        while left < right and text[left].isspace():
            left += 1
        while right > left and text[right - 1].isspace():
            right -= 1
        if left < right:
            bounds.append((left, right))
    return bounds

def quote_ranges(text: str) -> list[tuple[int, int]]:
    patterns = [r'"[^"\n]*"', r'“[^”\n]*”', r'‘[^’\n]*’', r'«[^»\n]*»',
                r'「[^」\n]*」', r'『[^』\n]*』', r'【[^】\n]*】',
                r"(?<!\w)'[^'\n]+'(?!\w)"]
    out = []
    for pattern in patterns:
        out.extend((m.start(), m.end()) for m in re.finditer(pattern, text))
    return sorted(set(out))

UNCERTAINTY_RE = re.compile(
    r'\b(?:may|might|could|perhaps|maybe|possibly|unclear|uncertain|unknown|unconfirmed|'
    r'seemingly|seems? to be|appears? to be|cannot tell|can\s*not tell|hard to tell)\b|'
    r'가능성|일지도|일\s*수\s*있|모호|불분명|확실하지|알\s*수\s*없|추정|불확실|듯(?:하다|한|해)|같을\s*수|미상|판별하기\s*어렵', FLAGS)

ATTRIBUTION_RE = re.compile(
    r'\b(?:caption|text|label|sign|subtitle|description|note)\b.{0,50}\b(?:says?|reads?|states?|claims?|reports?|describes?)\b|'
    r'\b(?:says?|reads?|states?|claims?|reports?|describes?)\b.{0,50}\b(?:caption|text|label|sign|subtitle|description|note)\b|'
    r'(?:캡션|문구|표지|자막|설명|텍스트).{0,40}(?:말하|적혀|쓰여|표시|기재|언급|주장)|'
    r'(?:말하|적혀|쓰여|표시|기재|언급|주장).{0,40}(?:캡션|문구|표지|자막|설명|텍스트)', FLAGS)

NEG_EN = re.compile(r'\b(?:not|never|no|without|doesn\x27t|don\x27t|didn\x27t|isn\x27t|aren\x27t|wasn\x27t|weren\x27t|cannot|can\x27t|is\s+not|are\s+not|was\s+not|were\s+not)\b', FLAGS)

NEG_KO = re.compile(
    r'(?:아니라|아니고|아님|않(?:은|는|다|고|아서|아도|습니다|아요|지|았|을)?|'
    r'못\s*(?:찍|촬영|기울|비치|보이|나오|되|하|반사)|'
    r'없(?:다|고|는|어|으며|어서|습니다|아요|을)|'
    r'(?<!\w)안\s*(?:찍|촬영|기울|비치|보이|나오|되|하|반사))')

def local_negation(text: str, start: int, end: int, margin: int = 20) -> bool:
    local = text[max(0, start - margin):min(len(text), end + margin)]
    return bool(NEG_EN.search(local) or NEG_KO.search(local))

def range_overlaps(start: int, end: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start < right and left < end for left, right in ranges)

def guarded_window(text: str, window_start: int, window_end: int, evidence: list[dict]) -> dict | None:
    window = text[window_start:window_end]
    translated = [{**x, 'start': x['start'] - window_start, 'end': x['end'] - window_start} for x in evidence]
    qrs = quote_ranges(window)
    if any(range_overlaps(x['start'], x['end'], qrs) for x in translated):
        return {'blocked': 'quoted_evidence'}
    if ATTRIBUTION_RE.search(window):
        return {'blocked': 'attributed_claim'}
    if UNCERTAINTY_RE.search(window):
        return {'blocked': 'uncertain_claim'}
    return None

def reflection_matches(text: str) -> list[dict]:
    """Find direct same/other reflection relations; return original-source spans."""
    sentences = source_sentences(text)
    found = []
    patterns = [
        ('same_self_photo', r'(?P<owner>\b(?:woman|person|subject|girl|man|she|he)\b).{0,60}(?P<action>\b(?:photograph\w*|take\w*|shoot\w*|capture\w*)\b).{0,40}(?P<self>\b(?:herself|himself|themselves|themself|oneself)\b)',
         [('owner', 'owner'), ('action', 'self_photo_action'), ('self', 'self_reference')]),
        ('same_self_photo', r'(?P<owner>여성|인물|사람|주인공|여자).{0,32}(?P<self>자신|본인).{0,25}(?P<reflection>거울|반사|셀카).{0,24}(?P<action>사진.{0,4}(?:찍|촬영)|셀카.{0,10}(?:찍|촬영))',
         [('owner', 'owner'), ('self', 'self_reference'), ('reflection', 'reflection_context'), ('action', 'self_photo_action')]),
        ('same_person_reflection', r'(?P<owner>\b(?:her|his|their|the subject[\x27’]s|the woman[\x27’]s)\b).{0,8}(?P<own>own).{0,8}(?P<reflection>reflection)\b',
         [('owner', 'owner'), ('own', 'same_person_relation'), ('reflection', 'reflection_context')]),
        ('same_person_reflection', r'(?P<owner>자신|본인)의\s*(?P<reflection>반사상|거울상|모습)',
         [('owner', 'owner'), ('reflection', 'reflection_context')]),
        ('same_person_reflection', r'(?P<relation>\b(?:same person|same subject|same actor)\b).{0,55}(?P<reflection>\b(?:mirror|reflection|reflected|reflect\w*)\b)',
         [('relation', 'same_person_relation'), ('reflection', 'reflection_context')]),
        ('same_person_reflection', r'(?P<reflection>\b(?:mirror|reflection|reflected|reflect\w*)\b).{0,55}(?P<relation>\bsame (?:person|subject|actor)\b)',
         [('relation', 'same_person_relation'), ('reflection', 'reflection_context')]),
        ('same_person_reflection', r'(?P<relation>같은\s*(?:사람|인물|주체)).{0,45}(?P<reflection>거울|반사|두\s*면)',
         [('relation', 'same_person_relation'), ('reflection', 'reflection_context')]),
        ('same_person_reflection', r'(?P<reflection>거울|반사|두\s*면).{0,45}(?P<relation>같은\s*(?:사람|인물|주체))',
         [('relation', 'same_person_relation'), ('reflection', 'reflection_context')]),
        ('different_person_reflection', r'(?P<relation>\b(?:different|another|other|second|distinct) person\b).{0,45}(?P<reflection>\b(?:mirror|reflection|reflected)\b)',
         [('relation', 'other_person_relation'), ('reflection', 'reflection_context')]),
        ('different_person_reflection', r'(?P<reflection>\b(?:mirror|reflection|reflected)\b).{0,45}(?P<relation>\b(?:different|another|other|second|distinct) person\b)',
         [('relation', 'other_person_relation'), ('reflection', 'reflection_context')]),
        ('different_person_reflection', r'(?P<relation>다른\s*사람|별개의\s*사람|또\s*다른\s*인물).{0,45}(?P<reflection>거울|반사|비치)',
         [('relation', 'other_person_relation'), ('reflection', 'reflection_context')]),
        ('different_person_reflection', r'(?P<reflection>거울|반사|비치).{0,45}(?P<relation>다른\s*사람|별개의\s*사람|또\s*다른\s*인물)',
         [('relation', 'other_person_relation'), ('reflection', 'reflection_context')]),
    ]
    for ss, se in sentences:
        sentence = text[ss:se]
        mirror_matches = list(re.finditer(r'\b(?:mirror|reflection|reflected|selfie|glass)\b|거울|유리|반사|비친|셀카', sentence, FLAGS))
        for state, pattern, group_roles in patterns:
            for m in re.finditer(pattern, sentence, FLAGS):
                spans = [span(text, ss + m.start(g), ss + m.end(g), role) for g, role in group_roles]
                # For self-photo patterns, a separate reflective-context span is required.
                if state == 'same_self_photo' and not any(x['role'] == 'reflection_context' for x in spans):
                    related = next((x for x in mirror_matches if abs(x.start() - m.start()) <= 150), None)
                    if not related:
                        continue
                    spans.append(span(text, ss + related.start(), ss + related.end(), 'reflection_context'))
                relation = next((x for x in spans if x['role'] in {'self_photo_action', 'same_person_relation', 'other_person_relation'}), None)
                if relation and local_negation(text, relation['start'], relation['end']):
                    continue
                if state == 'same_self_photo':
                    action = next(x for x in spans if x['role'] == 'self_photo_action')
                    if local_negation(text, action['start'], action['end'], margin=16):
                        continue
                guard = guarded_window(text, ss, se, spans)
                if guard:
                    continue
                found.append({'state': state, 'spans': spans, 'window_start': ss, 'window_end': se})
    # Deduplicate overlapping matches of the same direct relation.
    unique = {}
    for item in found:
        key = (item['state'], tuple((x['role'], x['start'], x['end']) for x in item['spans']))
        unique[key] = item
    return list(unique.values())

def sentence_windows(text: str, max_chars: int = 360) -> list[tuple[int, int]]:
    sentences = source_sentences(text)
    windows = []
    for i, (start, end) in enumerate(sentences):
        windows.append((start, end))
        if i + 1 < len(sentences):
            end2 = sentences[i + 1][1]
            if end2 - start <= max_chars:
                windows.append((start, end2))
    return sorted(set(windows), key=lambda x: (x[0], x[1] - x[0]))

def tilt_matches(text: str) -> list[dict]:
    found = []
    frame_patterns = [
        (r'(?P<tilt>\b(?:tilted|canted|rolled|rotated)\b)\s+(?P<owner>\b(?:horizon|frame)\b)', [('owner', 'frame_owner'), ('tilt', 'frame_tilt')]),
        (r'(?P<owner>\b(?:frame|horizon|camera roll)\b).{0,22}(?P<tilt>\b(?:tilted|canted|rolled|rotated)\b)', [('owner', 'frame_owner'), ('tilt', 'frame_tilt')]),
        (rf'(?P<owner>수평선|프레임|카메라\s*롤).{{0,22}}(?P<tilt>{KO_TILT_VERB})', [('owner', 'frame_owner'), ('tilt', 'frame_tilt')]),
        (rf'(?P<tilt>{KO_TILT_VERB}).{{0,22}}(?P<owner>수평선|프레임|카메라\s*롤)', [('owner', 'frame_owner'), ('tilt', 'frame_tilt')]),
    ]
    head_patterns = [
        (r'(?P<owner>\bhead\b).{0,24}(?P<tilt>\b(?:tilted|inclined|leans?|tilts?)\b)', [('owner', 'head_owner'), ('tilt', 'head_tilt')]),
        (r'(?P<tilt>\b(?:tilted|inclined|leans?|tilts?)\b).{0,24}(?P<owner>\bhead\b)', [('owner', 'head_owner'), ('tilt', 'head_tilt')]),
        (rf'(?P<owner>머리).{{0,24}}(?P<tilt>{KO_TILT_VERB})', [('owner', 'head_owner'), ('tilt', 'head_tilt')]),
        (rf'(?P<tilt>{KO_TILT_VERB}).{{0,24}}(?P<owner>머리)', [('owner', 'head_owner'), ('tilt', 'head_tilt')]),
    ]
    for ws, we in sentence_windows(text):
        window = text[ws:we]
        frame_spans = []
        head_spans = []
        # Direct owner/tilt links must occur in one sentence. Only the
        # explicit anaphoric assignment rules below may bridge two sentences.
        for sent_start, sent_end in source_sentences(window):
            sentence = window[sent_start:sent_end]
            base = ws + sent_start
            for pattern, roles in frame_patterns:
                for m in re.finditer(pattern, sentence, FLAGS):
                    owner = span(text, base + m.start('owner'), base + m.end('owner'), 'frame_owner')
                    tilt = span(text, base + m.start('tilt'), base + m.end('tilt'), 'frame_tilt')
                    if not local_negation(text, tilt['start'], tilt['end'], margin=14):
                        frame_spans.append([owner, tilt])
            for pattern, roles in head_patterns:
                for m in re.finditer(pattern, sentence, FLAGS):
                    owner = span(text, base + m.start('owner'), base + m.end('owner'), 'head_owner')
                    tilt = span(text, base + m.start('tilt'), base + m.end('tilt'), 'head_tilt')
                    if not local_negation(text, tilt['start'], tilt['end'], margin=14):
                        head_spans.append([owner, tilt])

        # Explicit transfer of an already-described tilt to frame/camera roll,
        # with head as the rejected alternative. The tilt antecedent and binding
        # are separately quoted at their original offsets.
        assignments = []
        for m in re.finditer(r'\b(?:the\s+)?(?:described\s+)?tilt\b.{0,26}\bbelongs\s+to\s+(?P<frame>(?:the\s+)?(?:image\s+)?frame|camera\s+roll)\b.{0,35}\b(?:rather\s+than|instead\s+of|not)\b.{0,20}\b(?P<head>(?:the\s+)?(?:woman[\x27’]s\s+)?head)\b', window, FLAGS):
            antecedent = re.search(r'\b(?:tilted|canted|rolled|rotated)\b.{0,18}\b(?:horizon|frame)\b|\b(?:frame|horizon|camera roll)\b.{0,18}\b(?:tilted|canted|rolled|rotated)\b', window, FLAGS)
            if antecedent and local_negation(window, antecedent.start(), antecedent.end(), margin=12):
                antecedent = None
            if antecedent:
                assignments.append([
                    span(text, ws + antecedent.start(), ws + antecedent.end(), 'explicit_tilt_antecedent'),
                    span(text, ws + m.start('frame'), ws + m.end('frame'), 'frame_owner_assignment'),
                    span(text, ws + m.start('head'), ws + m.end('head'), 'head_rejected_alternative'),
                    span(text, ws + m.start(), ws + m.end(), 'owner_contrast'),
                ])
        for m in re.finditer(r'(?P<tiltref>이\s*기울기(?:는|가)).{0,32}(?P<head>머리).{0,12}(?P<neg>아니라|아니고|아닌).{0,30}(?P<frame>프레임|카메라\s*롤)', window):
            antecedent = re.search(rf'(?P<tilt>{KO_TILT_VERB}).{{0,22}}(?P<owner>수평선|프레임|카메라\s*롤)|(?P<owner2>수평선|프레임|카메라\s*롤).{{0,22}}(?P<tilt2>{KO_TILT_VERB})', window)
            if antecedent and local_negation(window, antecedent.start(), antecedent.end(), margin=12):
                antecedent = None
            if antecedent:
                assignments.append([
                    span(text, ws + antecedent.start(), ws + antecedent.end(), 'explicit_tilt_antecedent'),
                    span(text, ws + m.start('frame'), ws + m.end('frame'), 'frame_owner_assignment'),
                    span(text, ws + m.start('head'), ws + m.end('head'), 'head_rejected_alternative'),
                    span(text, ws + m.start(), ws + m.end(), 'owner_contrast'),
                ])

        contrast = bool(re.search(r'\b(?:rather than|instead of|while|whereas|but|as opposed to|or)\b|아니라|아니고|반면|대신|보다', window, FLAGS))
        head_level = bool(re.search(r'\bhead\b.{0,28}(?:\bnot\s+tilted\b|\b(?:remains?|stays?)\s+(?:level|upright|straight)\b)|(?:\bnot\s+to\s+(?:the\s+)?(?:woman[\x27’]s\s+)?head\b)|머리.{0,28}(?:수평|곧게|바로|않고)', window, FLAGS))
        frame_level = bool(re.search(r'\b(?:frame|horizon|camera roll)\b.{0,28}(?:\bnot\s+tilted\b|\b(?:remains?|stays?)\s+(?:level|straight)\b)|(?:\bnot\s+(?:the\s+)?(?:image\s+)?frame\b)|(?:프레임|수평선|카메라\s*롤).{0,28}(?:수평|곧게|바로|않고)', window, FLAGS))

        if assignments:
            for evidence in assignments:
                if guarded_window(text, ws, we, evidence):
                    continue
                found.append({'state': 'frame_roll', 'spans': evidence, 'window_start': ws, 'window_end': we})
        if frame_spans and head_spans and contrast:
            for f in frame_spans:
                for h in head_spans:
                    evidence = f + h + [span(text, ws, we, 'owner_contrast')]
                    if not guarded_window(text, ws, we, evidence):
                        found.append({'state': 'both_explicitly_tilted', 'spans': evidence, 'window_start': ws, 'window_end': we})
        if frame_spans and head_level and contrast:
            for f in frame_spans:
                evidence = f + first_spans(window, [('head_rejected_alternative', r'\bhead\b|머리')]
                                             )[:1]
                # Rebase local span and keep the contrast marker separate.
                evidence = [f[0], f[1]] + [span(text, ws + x['start'], ws + x['end'], x['role']) for x in evidence[2:]]
                evidence.append(span(text, ws, we, 'owner_contrast'))
                if not guarded_window(text, ws, we, evidence):
                    found.append({'state': 'frame_roll', 'spans': evidence, 'window_start': ws, 'window_end': we})
        if head_spans and frame_level and contrast:
            for h in head_spans:
                evidence = h + first_spans(window, [('frame_rejected_alternative', r'\b(?:frame|horizon|camera roll)\b|프레임|수평선|카메라\s*롤')])[:1]
                evidence = [h[0], h[1]] + [span(text, ws + x['start'], ws + x['end'], x['role']) for x in evidence[2:]]
                evidence.append(span(text, ws, we, 'owner_contrast'))
                if not guarded_window(text, ws, we, evidence):
                    found.append({'state': 'head_tilt', 'spans': evidence, 'window_start': ws, 'window_end': we})
    # Prefer the shortest explicit witness window for concise quotations.
    unique = {}
    for item in found:
        key = (item['state'], tuple((x['role'], x['start'], x['end']) for x in item['spans']))
        unique[key] = item
    return sorted(unique.values(), key=lambda x: (x['window_end'] - x['window_start'], x['window_start']))

def effect_supports(state: str, record: dict) -> list[dict]:
    props = ((record.get('effects') or {}).get('properties') or [])
    found = []
    for item in props:
        if not isinstance(item, dict):
            continue
        prop = str(item.get('property', ''))
        target = str(item.get('target', ''))
        pair = (prop + ' ' + target).casefold()
        ok = False
        if state == 'same_self_photo':
            ok = 'same_woman_photographs_self_in_mirror' in prop or ('photograph' in prop and 'self' in prop and 'mirror' in pair)
        elif state == 'same_person_reflection':
            ok = prop == 'reflection.logic.same_subject' or ('same_subject' in prop and 'reflect' in pair)
        elif state == 'different_person_reflection':
            ok = bool(re.search(r'(?:different|other|second)_?(?:person|subject)', prop)) and bool(re.search(r'mirror|reflect', pair))
        elif state == 'frame_roll':
            ok = ('camera.roll.tilted_horizon' in prop or 'frame.roll' in prop or 'camera.roll' in prop) and bool(re.search(r'frame|horizon|roll', pair))
        elif state == 'head_tilt':
            ok = bool(re.search(r'(?:head\.(?:orientation|pitch)|pose\.head|head.*tilt)', prop)) and 'head' in pair
        elif state == 'both_explicitly_tilted':
            continue  # Requires two independent effect properties, handled below.
        if ok:
            found.append({'property': prop, 'target': target, 'dimension': item.get('dimension')})
    if state == 'both_explicitly_tilted':
        frame = [x for x in props if isinstance(x, dict) and ('camera.roll' in str(x.get('property', '')) or 'frame.roll' in str(x.get('property', '')))]
        head = [x for x in props if isinstance(x, dict) and re.search(r'(?:head\.(?:orientation|pitch)|pose\.head|head.*tilt)', str(x.get('property', '')))]
        if frame and head:
            found = [{'property': x.get('property'), 'target': x.get('target'), 'dimension': x.get('dimension')} for x in frame + head]
        else:
            found = []
    return found


_PRIMARY_POINTERS = {'/content/en', '/content/ko', '/content/definition'}
_SOURCE_HINTS = {
    'reflection_identity': re.compile(r'\b(?:mirror|reflection|reflected|selfie|glass)\b|거울|유리|반사|비친|셀카', FLAGS),
    'tilt_owner_disambiguation': re.compile(r'\b(?:tilted|canted|rolled|rotated|horizon|frame|head)\b|기울|수평선|프레임|머리|카메라\s*롤', FLAGS),
}


def source_witness(kind: str, units: list[dict], effects: dict) -> dict | None:
    """Return one same-selected-RID witness, or None when source is unresolved."""
    if kind not in _SOURCE_HINTS:
        return None
    primary = [unit for unit in units if unit.get('pointer') in _PRIMARY_POINTERS
               and isinstance(unit.get('text'), str) and unit['text'].strip()]
    if not primary:
        return None
    # Match the reviewed source selection contract: EN/KO literals are primary
    # when available; the authored definition is used only as fallback.
    if any(unit['pointer'] in {'/content/en', '/content/ko'} for unit in primary):
        primary = [unit for unit in primary if unit['pointer'] != '/content/definition']
    source_hashes = {unit.get('source_sha256') for unit in primary}
    if len(source_hashes) != 1 or not isinstance(next(iter(source_hashes)), str):
        return {'status': 'source_hash_disagreement', 'promoted': False}
    source_sha = next(iter(source_hashes))
    found = []
    for unit in primary:
        text = unit['text']
        if not _SOURCE_HINTS[kind].search(text):
            continue
        matches = reflection_matches(text) if kind == 'reflection_identity' else tilt_matches(text)
        for witness in matches:
            start, end = witness['window_start'], witness['window_end']
            found.append({
                'state': witness['state'],
                'pointer': unit['pointer'],
                'literal_id': unit.get('literal_id'),
                'source_sha256': source_sha,
                'source_span': {'start': start, 'end': end,
                                'offset_unit': 'unicode_code_points'},
                'source_quote': text[start:end],
                'evidence_spans': witness['spans'],
            })
    if not found:
        return None
    states = {item['state'] for item in found}
    if len(states) != 1:
        return {'status': 'ambiguous_source_state', 'candidate_states': sorted(states),
                'source_witnesses': found, 'promoted': False}
    state = next(iter(states))
    effect_witnesses = effect_supports(state, {'effects': effects or {}})
    found.sort(key=lambda item: (item['source_span']['end'] - item['source_span']['start'],
                                 item['pointer'], item['source_span']['start']))
    selected = dict(found[0])
    selected.update({
        'status': 'promoted' if effect_witnesses else 'unconfirmed_primary_text',
        'kind': kind,
        'effect_witnesses': effect_witnesses,
        'effect_corroboration_same_selected_rid': bool(effect_witnesses),
        'promoted': bool(effect_witnesses),
    })
    if len(found) > 1:
        selected['same_state_primary_witness_count'] = len(found)
    return selected

