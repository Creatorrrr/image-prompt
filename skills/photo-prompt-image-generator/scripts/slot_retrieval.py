"""Post-freeze advisory slot retrieval evidence, never a meaning author.

This projection reads an explicit allowlist of frozen core fields only. Its
small grammatical recognizers retain source spans and uncertainty; they do not
create anchors, obligations, rewrite the baseline, or claim full language
understanding. Catalogue IDs and pre-core audit records are deliberately absent.
"""
from __future__ import annotations

import re
from typing import Any, Mapping

# Ownership uses the v3 vocabulary; retrieval cues are narrower, slot-local
# photographic properties. In particular a camera lock does not make a lens
# sentence positive evidence for camera direction (or vice versa).
from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS

DIMENSION_CUES = {
    "lighting": r"lights?|lighting|lit|(?:sun|lamp|candle|moon|fire|spot|back)lights?|beams?|illuminat(?:e|es|ed|ing|ion)|shadows?|flash(?:es)?|caustics?|backlit|sunlit|daylight|moonlit|glow(?:s|ing)?|diffus(?:e|ed|ing|ion)|softbox(?:es)?",
    "composition": r"fram(?:e|es|ed|ing)|compos(?:e|ed|ition)|perspective|diagonal|foreground|background|depth|negative space|leading lines|symmetr(?:y|ic|ical|ically)",
    "framing": r"fram(?:e|es|ed|ing)|waist[ -]up|full[ -]body|close[ -]up|head[ -]and[ -]shoulders|wide shot|medium shot|tight crop|cropp(?:ed|ing)",
    "pose": r"seat(?:ed|ing)?|sit(?:s|ting)?|stand(?:s|ing)?|kneel(?:s|ing)?|crouch(?:es|ed|ing)?|lean(?:s|ed|ing)?|reclin(?:e|es|ed|ing)|bend(?:s|ing)?|bent|pose|posture|walk(?:s|ed|ing)?|run(?:s|ning)?",
}
PROP_CUES = r"hold(?:s|ing)?|held|carry(?:ing)?|carries|carried|wield(?:s|ed|ing)?|rest(?:s|ed|ing)?|placed|mount(?:s|ed|ing)?|grasp(?:s|ed|ing)?|using|wear(?:s|ing)?|worn|props?|objects?|beside|beneath|on the table"
SLOT_DIMENSIONS = {
    "body_pose": ("pose",),
    "prop": ("appearance", "action", "setting"),
    "composition": ("composition",),
    **{s: ("camera",) for s in ("camera_direction", "camera_height", "camera_type", "lens")},
    **{s: ("framing",) for s in ("shot_scale", "subject_framing", "platform_framing")},
    **{s: ("lighting",) for s in ("lighting", "light_type", "light_shape", "light_direction", "light_intensity")},
}
SLOT_CUES = {
    "prop": PROP_CUES,
    "lens": r"lens(?:es)?|wide[ -]angle|telephoto|focal(?: length)?|macro|zoom|millimet(?:er|re)s?|\d+(?:[.–-]\d+)?\s*mm",
    "camera_direction": r"angle(?![ -]lens)|eye[ -](?:level|height)|straight[ -]on|directly in front|from (?:(?:the|her|his|their) |a little |slightly )?(?:side|behind|above|below)|overhead|vertically (?:upward|downward)|(?:low|high|raised) (?:angle|viewpoint|position)|viewpoint|near shoulder|over[ -]the[ -]shoulder|profile|rear[ -]view",
    "camera_height": r"eye[ -](?:level|height)|height of (?:her|his|their|the) eyes|ground[ -]level|(?:low|high|raised|elevated) (?:angle|viewpoint|position)|(?:above|below) (?:the )?(?:subject|player|reader)|waist[ -]height",
    "camera_type": r"(?:film|digital|mirrorless|SLR|DSLR|pinhole|instant|large[ -]format|medium[ -]format) camera|smartphone photograph|shot on (?:film|a phone)",
}
RELATIONS = re.compile(r"\b(holding|held|carrying|carried|wielding|wearing|worn|resting|mounted|standing|seated|under|underneath|above|beside|behind|through|from|toward|without|depicted|painted|reflected)\b", re.I)
REPRESENTATION = r'(?:picture|painting|poster|photo(?:graph)?|image|drawing|print|portrait|mural|illustration)'
DEPICTED = re.compile(
    r"\bdepicted\b|\b" + REPRESENTATION + r"\s+of\b|\b" + REPRESENTATION
    + r"\b(?:\s+[\w'-]+){0,4}?\s+(?:shows?|depicts?|portrays?|features?)\b"
    + r"|\b(?:painted|printed|pictured)\s+(?:on|in|onto)\b", re.I)
PRIMARY_IMAGE_SUBJECT = r'(?:the|this)\s+(?:(?:final|resulting|output)\s+)?(?:photograph|photo|image|picture|shot)'
CARRIED = re.compile(r"\b(?:hold(?:s|ing)?|held|carrying|carries|carried|wielding)\b", re.I)
NEGATIVE = re.compile(r"\b(?:not|no|never|neither|without|avoid|unlit|unplugged|inactive)\b|\b(?:rather than|instead of)\b|\b(?:switched|turned|powered)[ -]off\b|n['’]t\b", re.I)
FUNCTION_WORDS = frozenset('a an the is are was were be been being it its this that these those and or of to as with by for in at into from on but while which who she he they her his their there has have had photograph photo image make create visibly'.split())


def tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.casefold()) if t not in FUNCTION_WORDS}


def direct_subject_categories(subject: str) -> list[str]:
    """Recognize a narrow direct human noun phrase, not a depicted person.

    The existing category policy omits woman/man. Do not match an embedded
    mention (statue/photo of a person), a compound object head (woman statue),
    or a nonhuman adult. Unknown syntax remains unclassified.
    """
    match = re.match(r'^\s*(?:(?:a|an|the)\s+)?adult\s+(?:woman|man|women|men)\b(.*)$', subject, re.I)
    if not match:
        return []
    suffix = match.group(1).strip()
    if suffix and suffix != '.' and not re.match(r'^(?:in|with|who|whose|wearing)\b', suffix, re.I):
        return []
    # An image/container is not the main physical human. Restrict this check
    # to the immediate "in a ... image" complement; a person carrying a photo
    # or standing in a room with pictures is still a person.
    representation = r'(?:photo(?:graph)?|picture|painting|poster|portrait|drawing|print|sculpture|statue)'
    if re.match(r'^in\s+(?:(?:a|an|the)\s+)?(?:(?!(?:with|of|beside|containing|near|behind)\b)[a-z-]+\s+){0,3}' + representation + r'\b', suffix, re.I):
        return []
    if re.match(r'^in\s+(?:bronze|marble|stone|clay|wax)\s*(?:$|[,.])', suffix, re.I):
        return []
    return ['human']


def clauses(text: str) -> list[str]:
    # A determiner alone is not a new clause: "a poster of a seated pianist
    # and a standing dancer" keeps both people inside the depicted scope.
    finite = (r'(?:is|are|was|were|has|have|stands?|sits?|leans?|lies|rests?|glows?|'
              r'shines?|emits?|lights?|illuminates?|produces?|casts?|looks?|faces?|'
              r'points?|observes?|reads?|holds?|carries|wears?|refracts?|balances?|'
              r'remains?|stays?|supplies|draws?|enters?|falls?|shows?)')
    new_subject = r'(?:(?:she|he|they|we|it)\s+|(?:the|an?)\s+(?:[\w\'-]+\s+){1,5})' + finite + r'\b'
    # Comma coordination is split later without a finite-verb vocabulary;
    # retain the enclosing clause here so a depicted scene keeps its scope.
    return [s.strip() for s in re.split(
        r"[.;\n]+|(?<![,\s])\s+(?:and|but|while)\s+(?=" + new_subject + r')',
        text, flags=re.I) if s.strip()]


def dimension_for_slot(slot: str) -> tuple[str, ...]:
    return SLOT_DIMENSIONS.get(slot, (slot,) if slot in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS else ())


def _is_depicted(text: str) -> bool:
    # Definite output-image narration is not an object in the image. Allow an
    # output modifier and manner adverb without admitting physical modifiers
    # such as "framed" or "on the wall". Later depictions keep their scope.
    primary = re.match(r'^\s*' + PRIMARY_IMAGE_SUBJECT + r'\s+(?:[a-z]+ly\s+)?(?:shows?|captures?|frames?)\b', text, re.I)
    if primary:
        text = text[primary.end():]
    return bool(DEPICTED.search(text))


def _camera_relation_prefix(text: str) -> str:
    # Relative clauses and lighting participles describe the photographed
    # subject/source, not another predicate of the taking camera. Apply this
    # boundary to active, passive and fragment-based camera recognition alike.
    return re.split(
        r'\b(?:who|whose|which|that|while|where|when|as|under|beneath|with|'
        r'lit|illuminated|backlit)\b', text, maxsplit=1, flags=re.I,
    )[0]


def _camera_geometry_regions(text: str, slot: str) -> list[str]:
    """Limit directional relations to the taking view, not a pictured gaze.

    This is a small grammatical recognizer. Mentioning a camera elsewhere in a
    clause is not sufficient to attribute a person's gaze or a lamp's position
    to it. Unsupported camera phrasing remains in the whole-scene lane.
    """
    regions = []
    actor = r'(?:camera|we|' + PRIMARY_IMAGE_SUBJECT + r'|(?:the|our) view(?:point)?)'
    verb = r'(?:looks?|faces?|points?|observes?|sees?|views?|is|was|are|were|remains?|stays?|shows?|frames?|sits?)'
    for match in re.finditer(r'\b(' + actor + r')\s+(?:[a-z]+ly\s+)?(' + verb + r')\b([^;.!]*)', text, re.I):
        subject, predicate, rest = match.groups()
        rest = _camera_relation_prefix(rest)
        if predicate.casefold().startswith('look') and slot == 'camera_direction':
            if re.match(r'\s+(?:[a-z]+ly\s+)?(?:up|down|upward|downward)\b', rest, re.I):
                regions.append('camera ' + predicate + rest)
        if predicate.casefold().startswith('show'):
            # A photograph can show light falling from above; require an
            # explicit framing/viewpoint term rather than a depicted relation.
            if not re.search(r'\b(?:viewpoint|angle|eye[ -]level|straight[ -]on|rear[ -]view)\b', rest, re.I):
                continue
        regions.append(rest)
    # Passive taking-view statements carry their own photographic relation.
    for match in re.finditer(r'\b(?:shot|photographed|framed|viewed|seen|captured)\s+(?:(?:[a-z]+ly)\s+)?(?:from|at|over|through)\b([^;.!]*)', text, re.I):
        region = _camera_relation_prefix(match.group(0))
        regions.append(region)
    # A viewpoint phrase is an explicit photographic property, not a subject
    # gaze. It is useful for fragments such as property-anchor evidence.
    fragment = _camera_relation_prefix(text)
    if re.search(
        r'\b(?:viewpoint|camera angle|rear[ -]view(?![ -]mirror)|'
        r'(?:eye[ -]level|overhead|low[ -]angle|high[ -]angle|side|frontal)'
        r'(?:\s+[a-z-]+){0,2}\s+(?:view|shot|framing))\b', fragment, re.I
    ):
        regions.append(fragment)
    return regions


def _has_slot_cue(text: str, slot: str) -> bool:
    pattern = SLOT_CUES.get(slot)
    if pattern is None:
        pattern = '|'.join(DIMENSION_CUES[d] for d in dimension_for_slot(slot) if d in DIMENSION_CUES)
    if not pattern:
        return False
    if slot in {'camera_direction', 'camera_height'}:
        regions = _camera_geometry_regions(text, slot)
        if slot == 'camera_direction' and any(re.search(
            r'\bcamera looks?\s+(?:[a-z]+ly\s+)?(?:up|down|upward|downward)\b', region, re.I
        ) for region in regions):
            return True
        # "wide-angle" denotes optics even when a camera is also mentioned.
        return any(re.search(r'\b(?:' + pattern + r')\b',
                             re.sub(r'\bwide[ -]angle\b', '', region, flags=re.I), re.I)
                   for region in regions)
    return re.search(r'\b(?:' + pattern + r')\b', text, re.I) is not None


def _source_spans(text: str, slot: str) -> list[tuple[str, str]]:
    """Classify enclosing source roles independently of the cue vocabulary."""
    out = []
    for clause in clauses(text):
        depicted = _is_depicted(clause)
        cursor = 0
        governing_start = 0
        negative_enumeration = False
        # Bound explicit negative adjuncts without discarding the positive
        # prefix. Every returned span remains a contiguous source substring.
        for span in re.split(
            r',\s*(?=(?:not|no|never|without|rather than|instead of)\b)'
            r'|,\s+(?:and|but|while)\s+(?=(?:the|an?|she|he|they|we|it)\b)'
            r'|\s+(?=(?:rather than|instead of|with\s+no|without)\b)'
            r'|\s+(?=with\s+(?:(?:an?|the)\s+)?(?:(?:[a-z-]+|\d+)\s+){0,4}lens\b)',
            clause, flags=re.I,
        ):
            span = span.strip(' ,')
            if not span:
                continue
            start = clause.find(span, cursor)
            coordinated = bool(re.search(r',\s+(?:and|but|while)\s+$', clause[cursor:start], re.I))
            inherited_negative = coordinated and negative_enumeration
            if coordinated:
                governing_start = start
            cursor = start + len(span)
            # An optical adjunct inherits its governing source relation:
            # "holding a camera with a lens" is still a carried object, and
            # "do not shoot ... with a lens" is still a negative instruction.
            # Do not inherit a later contrast such as ", not a telephoto".
            optical_adjunct = re.match(r'^with\s+(?:(?:an?|the)\s+)?(?:(?:[a-z-]+|\d+)\s+){0,4}lens\b', span, re.I)
            role_context = clause[governing_start:cursor] if optical_adjunct else span
            inherited_negative = inherited_negative or bool(optical_adjunct and negative_enumeration)
            # A comma can delimit a negative noun list, not a fresh assertion:
            # "without a flash, a softbox, and the ring light" stays negative.
            # An inactive-entity clause beginning "The lamp ..." does not
            # establish this enumeration scope for a later daylight clause.
            negative_enumeration = inherited_negative or bool(re.match(
                r'^(?:without|no|not|never|avoid|rather than|instead of)\b', span, re.I))
            role = 'scene_evidence'
            if depicted:
                role = 'depicted_entity'
            elif inherited_negative or NEGATIVE.search(role_context) or inactive_entities(role_context):
                role = 'negative_or_contrast'
            elif 'camera' in dimension_for_slot(slot) and re.search(
                r'\b(?:camera|lens)(?:[ -]shaped|\s+(?:charm|ornament|pendant|replica|toy))\b', role_context, re.I
            ):
                role = 'scene_object'
            elif 'camera' in dimension_for_slot(slot) and CARRIED.search(role_context) and not re.search(
                r'\b(?:shot|framed|photographed|captured|viewpoint|shooting)\b', role_context, re.I
            ):
                role = 'carried_object'
            out.append((span, role))
    return out


def _projection_spans(text: str, slot: str) -> list[tuple[str, str]]:
    return [(span, role) for span, role in _source_spans(text, slot) if _has_slot_cue(span, slot)]


def _matches_exclusion(span: str, exclusion: str) -> bool:
    # Match the producer's ASCII word boundaries. "text" must not suppress
    # "texture" or "context" in the overlap lane after query redaction.
    pattern = re.escape(exclusion)
    if exclusion.isascii() and re.search(r'[A-Za-z0-9]', exclusion):
        pattern = r'(?<![A-Za-z0-9])' + pattern + r'(?![A-Za-z0-9])'
    return bool(re.search(pattern, span, re.I))


def project(core: Mapping[str, Any], slot: str) -> dict[str, Any]:
    """Return source-bound, slot-local evidence without changing lock ownership.

    Explicit negative/depicted text is retained for diagnostics, but cannot
    become a positive cue through either raw baseline text or a shorter anchor.
    The recognizers are conservative English heuristics, not a semantic guard.
    """
    dimensions = dimension_for_slot(slot)
    lock = core.get('intent_lock') or {}
    baseline = str(core.get('baseline_prompt_en') or '')
    exclusions = [str(value).casefold() for value in core.get('user_exclusions') or [] if str(value)]
    source_spans = _source_spans(baseline, slot)
    spans = [(span, role) for span, role in source_spans if _has_slot_cue(span, slot)]
    positive_source = [span for span, role in source_spans if role == 'scene_evidence'
                       and not any(_matches_exclusion(span, excluded) for excluded in exclusions)]
    positive = [span for span, _ in spans if span in positive_source]
    # A single-family typed dimension is authoritative even when its language
    # is absent from our small cue lexicon. Shared-property camera/prop slots
    # still require local relevance, so direction cannot supply lens evidence.
    typed_context = spans if slot in SLOT_CUES else source_spans
    typed_positive = [span for span, _ in typed_context if span in positive_source]
    rows = []
    for span, role in spans:
        rows.append({'source': 'baseline_prompt_en', 'evidence': span, 'role': role,
                     'relations': RELATIONS.findall(span), 'ownership': 'authorial_baseline',
                     'positive_spans': [span] if span in positive else []})

    def positive_parts(evidence: str) -> list[str]:
        # Require positive *source context*, not merely a positive-sounding
        # substring of a negation or a depicted scene. Casefold matches v3.
        result = []
        for span in typed_positive:
            if evidence.casefold() in span.casefold():
                result.append(evidence)
            elif span.casefold() in evidence.casefold():
                result.append(span)
        return list(dict.fromkeys(result))

    for anchor in lock.get('semantic_anchors') or []:
        if not isinstance(anchor, dict) or anchor.get('dimension') not in dimensions:
            continue
        evidence = str(anchor.get('prompt_evidence') or '')
        if evidence and evidence.casefold() in baseline.casefold():
            parts = positive_parts(evidence)
            # Same v3 dimension can contain unrelated properties; retain a row
            # only when its evidence actually intersects this slot's spans.
            if not parts and not any(evidence.casefold() in span.casefold() or span.casefold() in evidence.casefold()
                                     for span, _ in typed_context):
                continue
            rows.append({'source': 'intent_lock.semantic_anchors', 'evidence': evidence,
                         'role': 'requester_evidence', 'relations': RELATIONS.findall(evidence),
                         'ownership': 'requester_locked', 'anchor_id': anchor.get('anchor_id'),
                         'positive_spans': parts})
    for assertion in core.get('semantic_assertions') or []:
        if not isinstance(assertion, dict) or assertion.get('polarity') != 'required':
            continue
        affected = set(assertion.get('affected_dimensions') or []) | {assertion.get('dimension')}
        if not affected.intersection(dimensions):
            continue
        for role, evidence in (assertion.get('evidence') or {}).items():
            if isinstance(evidence, str) and evidence and evidence.casefold() in baseline.casefold():
                parts = positive_parts(evidence)
                if not parts and not any(evidence.casefold() in span.casefold() or span.casefold() in evidence.casefold()
                                         for span, _ in typed_context):
                    continue
                rows.append({'source': 'semantic_assertions.evidence', 'evidence': evidence,
                             'role': role, 'relations': assertion.get('relations') or [],
                             'ownership': 'requester_locked', 'assertion_id': assertion.get('assertion_id'),
                             'positive_spans': parts})
    return {'version': 'photo-slot-meaning/v1', 'slot': slot, 'dimensions': list(dimensions),
            'locked_dimensions': [d for d in lock.get('locked_dimensions') or [] if d in dimensions],
            'open_dimensions': [d for d in lock.get('open_dimensions') or [] if d in dimensions],
            'evidence': rows, 'entities': inactive_entities(baseline),
            'interpretation': 'advisory_partial_projection', 'source_core_sha256': core.get('canonical_sha256', '')}


def positive_evidence(projection: Mapping[str, Any]) -> list[str]:
    return list(dict.fromkeys(str(span) for row in projection.get('evidence', [])
                             for span in row.get('positive_spans', [])))


# Bounded English noun phrases stop before finite verbs, conjunctions and
# spatial adjuncts. This intentionally misses ambiguous/complex grammar.
_NOUN_END = re.compile(
    r'\b(?:and|or|but|while|which|who|that|is|are|was|were|be|remains?|stays?|must|should|'
    r'can|will|stands?|rests?|sits?|lies|lie|glows?|shines?|emits?|lights|illuminates?|'
    r'produces?|casts?|supplies|on|in|at|under|beneath|beside|behind|above|below|near|'
    r'outside|inside|with|without|from|to|visible|present)\b', re.I)
_COPULA = r'(?:is|are|was|were|remains?|stays?)'
_OFF = r'off(?![-\w])(?=$|[,;.!]|\s+(?:and|but|while|under|beneath|beside|behind|with|without)\b)'
_STATE = r'(?:(?:switched|turned|powered)[ -])?' + _OFF + r'|unplugged|unlit|inactive|dark(?![-\w])'


def _noun_phrase(text: str) -> str:
    phrase = _NOUN_END.split(text, maxsplit=1)[0].strip(' ,:').casefold()
    phrase = re.sub(r'^(?:the|an?|this|these|those)\s+', '', phrase)
    words = phrase.split()
    if not 1 <= len(words) <= 6 or not all(re.fullmatch(r'[a-z]+(?:-[a-z]+)*', word) for word in words):
        return ''
    if words[-1] in FUNCTION_WORDS or words[-1] in {'off', 'not', 'never'}:
        return ''
    return phrase


def inactive_entities(text: str) -> list[dict[str, str]]:
    """Retain local inactive-state evidence, never merge entities across sources."""
    out = []
    seen = set()
    for span in clauses(text):
        if _is_depicted(span):
            continue
        phrases = []
        for match in re.finditer(r'\b' + _COPULA + r'\s+(?:(?:visible|present)\s+but\s+)?(?:' + _STATE + r')\b', span, re.I):
            prefix = span[:match.start()]
            # Do not turn "not off" / "not switched off" into an inactive
            # state, or use a new noun after an earlier finite predicate.
            if re.search(r'\b(?:not|never|no)\b', prefix, re.I):
                continue
            prefix = re.split(r'\b' + _COPULA + r'\b', prefix, maxsplit=1, flags=re.I)[0]
            phrases.append(_noun_phrase(prefix))
        for match in re.finditer(
            r'\b(?:(?:switched|turned|powered)[ -]off|unplugged|unlit|inactive)\s+(?!to\b)([^,;.!]+)',
            span, re.I,
        ):
            # Postverbal "turned off ..." needs an explicit determiner;
            # hyphenated/prenominal states ("a switched-off brass lamp") do not.
            before = span[:match.start()]
            if re.search(r'\b(?:not|never|no)\b', before, re.I):
                continue
            state = match.group(0).split()[0].casefold()
            if state in {'turned', 'switched', 'powered'} and not re.match(r'^(?:the|an?|this|these|those)\b', match.group(1), re.I):
                if not re.search(r'\b(?:the|an?|this|these|those)\s*$', before, re.I):
                    continue
            phrases.append(_noun_phrase(match.group(1)))
        for phrase in phrases:
            if not phrase or (phrase, span) in seen:
                continue
            seen.add((phrase, span))
            out.append({'entity': phrase.split()[-1], 'entity_phrase': phrase,
                        'state': 'inactive', 'role': 'scene_entity', 'evidence': span})
    return out


def _conflict_sources(core: Mapping[str, Any], slot: str) -> list[str]:
    dimensions = set(dimension_for_slot(slot))
    lock = core.get('intent_lock') or {}
    baseline = str(core.get('baseline_prompt_en') or '')
    anchors = [row for row in lock.get('semantic_anchors') or []
               if isinstance(row, dict) and row.get('dimension') in dimensions
               and str(row.get('prompt_evidence') or '')
               and str(row.get('prompt_evidence') or '').casefold() in baseline.casefold()]
    property_scoped = any('property' in row for row in anchors)
    fully_locked = bool(dimensions.intersection(lock.get('locked_dimensions') or []))
    camera_slot = 'camera' in dimensions
    slot_spans = _projection_spans(baseline, slot) if camera_slot else []
    slot_anchors = [row for row in anchors if not camera_slot or any(
        str(row['prompt_evidence']).casefold() in span.casefold()
        or span.casefold() in str(row['prompt_evidence']).casefold()
        for span, _ in slot_spans
    )]
    # Even a broad legacy camera lock cannot turn a direction-only anchor into
    # evidence against an authored lens choice. Preserve the declared lock in
    # project(); merely abstain from this unsupported conflict inference.
    baseline_supported = fully_locked and not property_scoped and not (
        camera_slot and anchors and not slot_anchors
    )
    # Authorial choices on open dimensions are replaceable. Requester spans
    # still constrain both open and locked dimensions, even when their negative
    # clauses are not repeated in the baseline. Never concatenate the sources.
    sources = [baseline] if baseline_supported else []
    sources.extend(str(row.get('text') or '') for row in (core.get('request_binding') or {}).get('active_spans') or [] if isinstance(row, dict))
    sources.extend(str(row.get('prompt_evidence') or '') for row in slot_anchors)
    return list(dict.fromkeys(source for source in sources if source))


def _ordered_phrase(text: str) -> list[str]:
    return [t for t in re.findall(r'[a-z0-9]+', text.casefold())
            if t not in {'a', 'an', 'the', 'is', 'are', 'was', 'were'}]


def _exclusion_phrases(text: str) -> list[str]:
    out = []
    for span in clauses(text):
        if _is_depicted(span):
            continue
        for match in re.finditer(r'\b(?:avoid|without|no)\s+([^,;.!]+)', span, re.I):
            # A trailing spatial adjunct belongs to the scene unless a narrow
            # directional relation is explicit. Preserve "hands above head";
            # do not swallow "traffic under warm street lamps".
            phrase = re.split(r'\b(?:under|beneath|on|in|at|beside|behind|near|with|from|through|while|but|and)\b', match.group(1), maxsplit=1, flags=re.I)[0].strip()
            out.append(phrase)
    return out


def conflict_reasons(core: Mapping[str, Any], entry: Mapping[str, Any], slot: str) -> list[str]:
    """Source-supported advisory warnings, never proof of incompatibility.

    These partial English recognizers are ranking penalties only. They cannot
    reject candidates, transfer authorial choices to requester ownership, or
    establish semantic precision beyond the covered grammar.
    """
    label = str(entry.get('en') or '')
    if re.search(r"\b(?:not|never|without|no|neither|avoid)\b|n['’]t\b", label, re.I):
        return []
    label_words = _ordered_phrase(label)
    label_phrase = ' ' + ' '.join(label_words) + ' '
    reasons = []
    for source in _conflict_sources(core, slot):
        for row in inactive_entities(source):
            head = row['entity']
            # A source relation is required: inactive objects can still cast
            # shadows under somebody else's light.
            active = re.match(r'^(?:the |an? )?(.+?)\s+(produces?|emits?|illuminates?|lights|glows?|shines?|casts?)\b(.*)', label, re.I)
            if not active:
                continue
            actor, verb, remainder = active.groups()
            if NEGATIVE.search(actor + ' ' + remainder):
                continue
            actor_tokens = tokens(actor)
            entity_tokens = tokens(row.get('entity_phrase', head))
            if head not in actor_tokens or not actor_tokens.issubset(entity_tokens):
                continue
            if actor_tokens != entity_tokens and len(re.findall(r'\b' + re.escape(head) + r'\b', source, re.I)) != 1:
                continue
            if verb.lower().startswith('cast') and not re.search(r'\b(?:light|illumination|glow)\b', remainder, re.I):
                continue
            reasons.append('inactive_entity_as_active_source')
        for phrase in _exclusion_phrases(source):
            excluded_words = _ordered_phrase(phrase)
            excluded_phrase = ' ' + ' '.join(excluded_words) + ' '
            if len(excluded_words) >= 2 and len(label_words) >= 2 and (
                excluded_phrase in label_phrase or label_phrase in excluded_phrase
            ):
                reasons.append('explicit_baseline_exclusion')
    return list(dict.fromkeys(reasons))


def candidate_positive_text(entry: Mapping[str, Any]) -> str:
    # Counterexamples/usage notes are intentionally not positive query material.
    pieces = [str(entry.get('en') or ''), *map(str, entry.get('concept_units') or [])]
    for relation in entry.get('relations') or []:
        if isinstance(relation, dict):
            pieces.extend(str(relation.get(k) or '') for k in ('subject', 'predicate', 'object'))
    return ' '.join(pieces)


def evidence_overlap(entry: Mapping[str, Any], evidence: list[str]) -> float:
    """Length-normalized precision over positive authored candidate cues.

    This is a bounded relevance feature, not a semantic correctness classifier.
    """
    label_tokens = tokens(str(entry.get('en') or ''))
    if not label_tokens:
        return 0.0
    relation_tokens = tokens(candidate_positive_text(entry))
    return max((0.8 * len(label_tokens & tokens(span)) / len(label_tokens)
                + 0.2 * len(relation_tokens & tokens(span)) / max(1, len(relation_tokens))
                for span in evidence), default=0.0)
