"""Opt-in, pure, source-bound *partial* semantic constraint checks.

This is a small English grammar, not an LLM or a general entailment engine.
``compatible`` means that the recognized footprint is consistent with the
recognized requester locks; it is not a certificate that all prose is safe.
Unrecognized/ambiguous relevant statements produce ``unknown``.  Only explicit
incompatible propositions produce ``contradiction``.  Catalog identifiers,
retrieval scores, tags, and pre-core audit material are never read.
"""
from __future__ import annotations

import re
import hashlib
from typing import Any, Mapping

from slot_retrieval import clauses, _is_depicted, _camera_geometry_regions

VERSION = 'photo-semantic-constraints/v1'
LIGHT_SLOTS = frozenset({'lighting', 'light_type', 'light_shape', 'light_direction', 'light_intensity'})
CAMERA_SLOTS = frozenset({'camera_direction', 'camera_height', 'camera_type', 'lens', 'composition'})
LIMITATIONS = [
    'Bounded English patterns only; no external semantic model is configured.',
    'No general coreference, quantifier, metaphor, or depicted-scene reasoning.',
    'Only lighting source/state/direction, taking-camera viewpoint/roll, and explicit scene presence are compared.',
    'Compatibility covers recognized propositions only; unknown is not an acceptance decision.',
    'A required fact omitted from a final prompt is reported as missing/unknown, not invented as a contradiction.',
]
_PERSON = r'(?:people|persons?|humans?|adults?|women|woman|men|man|children|child|girl|boy|visitors?|players?|spectators?|staff|human reflections?|human silhouettes?)'
_SOURCE = r'(?:lamp|lantern|softbox|flash|strobe|spotlight|headlight|candle|screen|monitor|light)'
_OBJECT = r'(?:' + _SOURCE + r'|mug|teacup|cup|book|chair|table|violin|guitar|camera|vase|bottle|statue|poster|atlas|pear|fern)'
_DET = r'(?:(?:the|a|an|one|this|that|both|two|three|its)\s+)?'
_MOD = r'(?:(?:open|burning|vintage|hanging|brass|desk|table|wall|ceiling|nearby|small|large|red|blue|ceramic|paper|oil|floor|reading|bedside|unlit|inactive|lit|glowing|adult|seated|standing|young|old)\s+){0,4}'
_NP = _DET + _MOD + '(?:' + _OBJECT + '|' + _PERSON + ')'
_NEG = re.compile(r"\b(?:not|never|neither|without|no|avoid|excluding|except|rather than|instead of)\b|n['’]t\b", re.I)
_UNCERTAIN = re.compile(r'\b(?:if|unless|perhaps|maybe|possibly|might|could|either)\b|\bor\b', re.I)
_CUES = re.compile(r'\b(?:light(?:s|ing)?|lit|lamp|lantern|flash|strobe|sunlight|daylight|moonlight|backlight|backlit|window|viewpoint|camera|angle|overhead|frontal|eye[ -]level|roll|horizon|people|person|woman|man|adult|human|mug|cup|teacup|book|chair|violin)\b', re.I)


def _entity(phrase: str) -> str:
    value = phrase.casefold().strip(' ,.:;')
    value = re.sub(r'^(?:the|a|an|one|this|that|both|two|three|its)\s+', '', value)
    value = re.sub(r'^(?:(?:unlit|inactive|lit|glowing|burning|nearby)\s+)+', '', value)
    if re.fullmatch(_MOD + _PERSON, value):
        return 'people'
    return value


def _fact(entity: str, prop: str, value: str, evidence: str, *, polarity: str = 'positive',
          relation: str = '', **extra: Any) -> dict[str, Any]:
    return {'entity': entity, 'property': prop, 'value': value, 'polarity': polarity,
            'relation': relation, 'evidence': evidence, **extra}


def _presence(clause: str) -> list[dict[str, Any]]:
    facts = []
    # Explicit negative noun phrases, never arbitrary token absence.
    for match in re.finditer(r'\b(?:no|without|excluding)\s+(' + _NP + r')\b', clause, re.I):
        facts.append(_fact(_entity(match[1]), 'presence', 'present', match[0], polarity='negative', relation='in_scene'))
    for match in re.finditer(r'\b(' + _NP + r')\s+(?:is|are|remains?)\s+(?:absent|not present)\b', clause, re.I):
        facts.append(_fact(_entity(match[1]), 'presence', 'present', match[0], polarity='negative', relation='in_scene'))
    if re.search(r'\b(?:nobody|no one)\b', clause, re.I):
        facts.append(_fact('people', 'presence', 'present', clause, polarity='negative', relation='in_scene'))
    negative_ranges = [(m.start(), m.end()) for m in re.finditer(r'\b(?:no|without|excluding)\s+(' + _NP + r')\b', clause, re.I)]
    # A determiner, an explicit relational argument, or the clause subject is
    # required. "human-scale lighting" and "person-shaped vase" are not people.
    pattern = r'(?<![\w-])(' + _NP + r')(?![\w-])'
    for match in re.finditer(pattern, clause, re.I):
        if any(start <= match.start() < end for start, end in negative_ranges):
            continue
        before, after = clause[:match.start()], clause[match.end():]
        if _entity(match[1]) == 'camera' and not re.search(r'\b(?:holding|holds|carrying|carries|displayed|vintage|product)\b', clause, re.I) and not re.match(r'\s+(?:rests?|sits?|lies|stands?)\b', after, re.I):
            continue
        if re.match(r'\s+(?:statue|painting|poster|portrait|drawing|photo|image|shaped|charm|ornament)\b', after, re.I):
            continue
        if re.match(r'\s+(?:is|are|remains?)\s+(?:absent|not present)\b', after, re.I):
            continue
        if _NEG.search(before):
            continue
        explicit = (match.start() == 0 or bool(re.match(r'^(?:the|a|an|one|this|two|three|both)\s+', match[1], re.I))
                    or bool(re.search(r'\b(?:on|beside|holding|holds|carrying|carries|with|onto|illuminates|lights)\s*$', before, re.I)))
        if explicit:
            facts.append(_fact(_entity(match[1]), 'presence', 'present', match[0], relation='in_scene'))
    return facts


def _lighting(clause: str, slot: str | None) -> list[dict[str, Any]]:
    facts = []
    # Source state is tied to the grammatical actor, not a noun elsewhere.
    state = r'(?:(?:switched|turned|powered)[ -]off|unlit|unplugged|inactive|disabled|off(?![-\w]))'
    for match in re.finditer(r'\b(' + _NP + r')\s+(?:(?:must|should)\s+)?(?:is|are|remain|remains|stay|stays|be)\s+(?:visible\s+but\s+)?(' + state + r')(?=$|[\s,.!;])', clause, re.I):
        if _NEG.search(clause[:match.start()]):
            continue
        tail = clause[match.end():]
        if match[2].casefold() == 'off' and re.match(r'\s+(?:camera|stage|screen|white)\b', tail, re.I):
            continue
        facts.append(_fact(_entity(match[1]), 'lighting.state', 'inactive', match[0], relation='emits_light'))
    for match in re.finditer(r'\b((?:the|a|an)\s+(' + state + r')\s+' + _MOD + _SOURCE + r')\b', clause, re.I):
        if _NEG.search(clause[:match.start()]):
            continue
        actor = re.sub(r'\b' + state + r'\s+', '', match[1], flags=re.I)
        facts.append(_fact(_entity(actor), 'lighting.state', 'inactive', match[0], relation='emits_light'))
    active = r'(?:emit(?:s)?|produce(?:s)?|cast(?:s)?|give(?:s)?)'
    for match in re.finditer(r'\b(' + _NP + r')\s+(?:(does|do)\s+)?(?:(not|never)\s+)?(' + active + r'|illuminates?|lights|glows?|shines?)\b([^;.!]*)', clause, re.I):
        actor, _, neg, verb, rest = match.groups()
        if _NEG.search(clause[:match.start()]):
            continue
        if not re.search(r'\b' + _SOURCE + r'\b', actor, re.I):
            continue
        # Casting a shadow proves that the object receives light, not emits it.
        if re.match(active + r'$', verb, re.I) and not re.search(r'\b(?:light|illumination|glow|light pool)\b', rest, re.I):
            if not (verb.casefold().startswith('produc') and re.match(r'\s+(?:a\s+)?localized pool\b', rest, re.I)):
                continue
        if _NEG.search(rest) and not re.match(r'\s+no\s+(?:light|illumination|glow)\b', rest, re.I):
            continue
        inactive = bool(neg or re.match(r'\s+no\s+(?:light|illumination|glow)\b', rest, re.I))
        facts.append(_fact(_entity(actor), 'lighting.state', 'inactive' if inactive else 'active', match[0], relation='emits_light'))
    if _NEG.search(clause):
        # Explicit source exclusions use the same grammar as positive sources,
        # but unsupported mixed positive/negative clauses are not inverted.
        prefix = re.match(r'^(?:no|without|avoid)\s+(.+)$', clause, re.I)
        if not prefix:
            return facts
        source_text, source_polarity = prefix[1], 'negative'
    else:
        source_text, source_polarity = clause, 'positive'
    source_patterns = (
        ('window', r'(?:window\s+(?:is|provides)\s+(?:the\s+)?(?:main|only)\s+light|window(?:[ -]side)?\s+(?:day)?light|daylight\s+(?:enters|entering|comes|coming)\s+from\s+(?:the\s+)?(?:left\s+|right\s+)?window)'),
        ('sun', r'(?:sunlight|direct sun|low[ -]sun|sun backlight)'),
        ('daylight', r'(?:daylight|overcast (?:sky)?light|skylight)'),
        ('moon', r'moonlight'), ('candle', r'(?:candlelight|(?:illuminated|lit)\s+only\s+by\s+(?:one|a|the)\s+(?:burning\s+)?candle)'), ('fire', r'firelight'),
        ('flash', r'(?:(?:studio|direct|hard|on[ -]camera|near[ -]camera[ -]axis)[ -])*(?:flash|strobe)(?:\s+lighting)?'),
        ('softbox', r'softbox\s+(?:light|lighting)'),
        ('tungsten', r'tungsten\s+(?:light|lighting|practical light)'),
        ('fluorescent', r'fluorescent\s+(?:light|lighting|top light|ceiling light)'),
        ('neon', r'neon\s+(?:light|lighting|sign spill light)'),
        ('lamp', r'(?:lamp|lantern|practical)\s+(?:light|lighting)'),
        ('electric', r'electric lights?'),
        ('ceiling_panel', r'(?:lit by (?:cool |warm )?ceiling panels|ceiling panels light)'),
        ('screen', r'(?:screen|monitor)\s+glow'),
    )
    source_values = []
    for value, pattern in source_patterns:
        for match in re.finditer(r'\b(?:' + pattern + r')\b', source_text, re.I):
            if value == 'daylight' and any(f['value'] == 'window' for f in facts if f['property'] == 'lighting.source'):
                continue
            if value == 'flash' and source_polarity == 'positive' and slot not in LIGHT_SLOTS and not re.search(r'\b(?:direct|studio|on[ -]camera|hard|near[ -]camera[ -]axis|fires?|firing|illuminat|lit by|with)\b', source_text, re.I) and source_text.strip().casefold() != match[0].casefold():
                continue
            source_values.append(value)
            # Retain a local source noun's identity where the phrase supplies
            # it. A generic family name cannot silently resolve to one of
            # several physical sources elsewhere in the scene.
            source_entity = ''
            for noun in re.finditer(r'(?<![\w-])(' + _NP + r')(?=\s+light(?:ing)?\b)', source_text, re.I):
                if noun.start() <= match.start() < noun.end():
                    source_entity = _entity(noun[1])
            facts.append(_fact('illumination', 'lighting.source', value, match[0], polarity=source_polarity,
                               relation='illuminates_scene', source_entity=source_entity,
                               exclusive=bool(re.search(r'\bonly\b|\bsole\b', clause, re.I))))
    # An inactive source noun cannot turn into an active source footprint.
    if any(f['property'] == 'lighting.state' and f['value'] == 'inactive' for f in facts):
        facts = [f for f in facts if f['property'] != 'lighting.source']
    if _NEG.search(clause):
        return facts
    light_context = bool(re.search(r'\b(?:light|lighting|daylight|sunlight|backlight|backlit|underlighting|key|fill|illumination)\b', clause, re.I))
    if not light_context:
        return facts
    # Do not borrow direction from a camera, person's gaze, or a lamp position.
    direction_region = re.split(r'\b(?:while|but|who|whose|camera|viewpoint)\b', clause, maxsplit=1, flags=re.I)[0]
    if re.search(r'\bfrom camera (?:left|right)\b', clause, re.I):
        direction_region = clause
    subject = ('light:' + source_values[0]) if len(set(source_values)) == 1 else 'illumination'
    if re.search(r'\bfill\b', direction_region, re.I):
        subject += ':fill'
    elif re.search(r'\bkey\b', direction_region, re.I):
        subject += ':key'
    patterns = (
        ('lighting.direction.horizontal', 'left', r'(?:light(?:ing)?\s+(?:enters?|entering|comes?|coming|falls?|falling)?\s*from\s+(?:the\s+)?(?:camera\s+)?left|from camera left|window on the left|left[ -]side (?:key |window )?light)'),
        ('lighting.direction.horizontal', 'right', r'(?:light(?:ing)?\s+(?:enters?|entering|comes?|coming|falls?|falling)?\s*from\s+(?:the\s+)?(?:camera\s+)?right|from camera right|window on the right|right[ -]side (?:key |window )?light)'),
        ('lighting.direction.depth', 'rear', r'(?:backlight|backlit|light from behind(?: the subject)?)'),
        ('lighting.direction.depth', 'front', r'(?:frontal light|front light|near[ -]camera[ -]axis frontal flash|on[ -]camera flash)'),
        ('lighting.direction.vertical', 'above', r'(?:overhead (?:fluorescent )?top light|overhead light|top light|light from above)'),
        ('lighting.direction.vertical', 'below', r'(?:underlighting|light from below)'),
    )
    for prop, value, pattern in patterns:
        for match in re.finditer(r'\b(?:' + pattern + r')\b', direction_region, re.I):
            facts.append(_fact(subject, prop, value, match[0], relation='incident_from'))
    return facts


def _camera(clause: str, slot: str | None) -> list[dict[str, Any]]:
    if re.search(r'\b(?:holding|holds|carrying|carries|camera[ -]shaped)\b', clause, re.I) and not re.search(r'\b(?:shot|photographed|framed|viewpoint)\b', clause, re.I):
        return []
    if _NEG.search(clause):
        # Narrow direct negation is a forbidden value, never its opposite.
        neg = re.match(r'^(?:no|not|without|avoid)\s+(.+)$', clause, re.I)
        if not neg:
            return []
        body, polarity = neg[1], 'negative'
    else:
        body, polarity = clause, 'positive'
    regions = _camera_geometry_regions(body, 'camera_direction')
    if re.search(r'\b(?:shoot|photograph|capture)\s+(?:from|at)\b', body, re.I):
        regions.append(body)
    if re.fullmatch(r'(?:at |from )?(?:eye[ -](?:level|height)|straight[ -]on|above|below)', body, re.I):
        regions.append(body)
    if re.search(r'\b(?:camera roll|Dutch angle|level (?:camera|horizon)|untilted|top[ -]down (?:composition|view)|(?:low|high)[ -]angle perspective)\b', body, re.I):
        regions.append(body)
    # Typed catalog slots permit an isolated, grammatical viewpoint fragment;
    # slot labels alone never convert a lighting/gaze clause to camera geometry.
    if slot in {'camera_direction', 'camera_height', 'composition'} and re.search(r'\b(?:view|viewpoint|angle|perspective|camera height|POV)\b', body, re.I):
        regions.append(body)
    patterns = (
        ('camera.viewpoint.azimuth', 'front', r'(?:straight[ -]on|frontal (?:view|shot)|directly in front)'),
        ('camera.viewpoint.azimuth', 'side', r'(?:side[ -]profile view|side view|from (?:the |her |his |their )?side)'),
        ('camera.viewpoint.azimuth', 'rear', r'(?:rear[ -]?view|from behind (?:the )?subject)'),
        ('camera.viewpoint.azimuth', 'three_quarter', r'three[ -]quarter (?:view|viewpoint|shot)'),
        ('camera.viewpoint.elevation', 'eye_level', r'(?:eye[ -](?:level|height)|at the height of (?:her|his|their|the subject.s) eyes|near the visible eye line)'),
        ('camera.viewpoint.elevation', 'high', r'(?:(?:slightly )?high(?:[ -]angle| observer angle| viewpoint)|from (?:a little |slightly )?above|looks? downward|looking down|oblique downward)'),
        ('camera.viewpoint.elevation', 'low', r'(?:low[ -](?:angle|ground[ -]level)|low angle|from below|worm[’\x27]s[ -]eye|looks? upward|looking up|below the face)'),
        ('camera.viewpoint.elevation', 'overhead', r'(?:top[ -]down|overhead view|bird[’\x27]s[ -]eye view|vertically downward)'),
        ('camera.roll', 'tilted', r'(?:Dutch angle|camera roll rotates|tilted (?:camera|horizon)|camera (?:is )?tilted)'),
        ('camera.roll', 'level', r'(?:level camera roll|camera roll (?:is|remains) level|level horizon|untilted camera|camera (?:is|remains) level)'),
    )
    facts = []
    for prop, value, pattern in patterns:
        for region in regions:
            for match in re.finditer(r'\b(?:' + pattern + r')\b', region, re.I):
                facts.append(_fact('camera', prop, value, match[0], polarity=polarity, relation='taking_view'))
    return facts


def _relevant_unknown(text: str) -> bool:
    if re.search(r'\b(?:properties of|displayed object|displayed camera)\b', text, re.I):
        return False
    if re.search(r'\b(?:camera|viewpoint|angle)\b.*\b(?:remains? open|freely chosen|your choice)\b', text, re.I):
        return False
    return bool(re.search(
        r'\b(?:lighting|illuminat\w*|light(?:s)?|lit|sunlight|daylight|moonlight|backlight|'
        r'backlit|viewpoint|camera roll|camera angle|eye[ -]level|frontal|overhead|'
        r'no people|without people|no one|nobody)\b', text, re.I))


def _parse(text: str, source: str, ownership: str, slot: str | None = None) -> dict[str, Any]:
    facts, unknown, ignored = [], [], []
    for clause in clauses(text):
        clause = re.sub(r'^(?:(?:make|create|generate|take)\s+)?(?:a|an)\s+(?:product\s+)?(?:photo(?:graph)?|image|shot)\s+of\s+', '', clause, flags=re.I)
        if re.search(r'\b(?:your choice|choose .+ freely|choose .+ angle|is welcome|lens freely)\b', clause, re.I) and not re.search(r'\b(?:must|only|no|not|remain)\b', clause, re.I):
            continue
        if _is_depicted(clause):
            ignored.append({'source': source, 'evidence': clause, 'reason': 'depicted_scope_not_scene_fact'})
            continue
        if _UNCERTAIN.search(clause) and not re.match(r'^(?:no|without|avoid)\b', clause, re.I):
            unknown.append({'source': source, 'evidence': clause, 'reason': 'conditional_or_alternative_grammar'})
            continue
        # Split explicit negative/contrast adjuncts, keeping their polarity.
        parts = re.split(r',\s*(?=(?:no|not|without|avoid)\b)|\s+(?=(?:without|rather than|instead of)\b)', clause, flags=re.I)
        for part in parts:
            rows = _lighting(part, slot) + _camera(part, slot) + _presence(part)
            for row in rows:
                row.update({'source': source, 'ownership': ownership, 'source_context': part})
            facts.extend(rows)
            for adjunct in re.split(r'\s+(?:and|while|with|but)\s+|,\s*', part, flags=re.I)[1:]:
                if _relevant_unknown(adjunct) and not any(row['property'] != 'presence' and row['evidence'].casefold() in adjunct.casefold() for row in rows):
                    unknown.append({'source': source, 'evidence': adjunct, 'reason': 'unresolved_relevant_adjunct'})
            if not rows and (_relevant_unknown(part) or slot is not None):
                unknown.append({'source': source, 'evidence': part, 'reason': 'unsupported_relevant_grammar'})
            elif slot in LIGHT_SLOTS and not any(row['property'].startswith('lighting.') for row in rows):
                unknown.append({'source': source, 'evidence': part, 'reason': 'no_lighting_relation_in_candidate_clause'})
            elif slot in {'camera_direction', 'camera_height'} and not any(row['property'].startswith('camera.') for row in rows):
                unknown.append({'source': source, 'evidence': part, 'reason': 'no_taking_camera_relation_in_candidate_clause'})
            elif _NEG.search(part) and not any(row['polarity'] == 'negative' or row['value'] == 'inactive' for row in rows):
                unknown.append({'source': source, 'evidence': part, 'reason': 'unresolved_negation'})
    unique = []
    seen = set()
    for row in facts:
        key = tuple(row.get(k) for k in ('entity', 'property', 'value', 'polarity', 'evidence', 'source'))
        if key not in seen:
            unique.append(row)
            seen.add(key)
    return {'facts': unique, 'unknowns': unknown, 'ignored_spans': ignored}


def _property_matches(anchor: Mapping[str, Any], fact: Mapping[str, Any]) -> bool:
    dimension = anchor.get('dimension')
    prop = str(fact['property'])
    if prop == 'presence':
        return dimension in {'subject', 'appearance', 'action', 'setting', 'event'} and 'property' not in anchor
    if dimension not in {'camera', 'lighting'} or not prop.startswith(str(dimension) + '.'):
        return False
    if 'property' not in anchor:
        return True
    requested = str(anchor['property'])
    aliases = {'direction': ('camera.viewpoint.azimuth', 'lighting.direction'),
               'viewpoint': ('camera.viewpoint',), 'height': ('camera.viewpoint.elevation',),
               'roll': ('camera.roll',), 'source': ('lighting.source',), 'state': ('lighting.state',)}
    paths = aliases.get(requested, (requested, str(dimension) + '.' + requested))
    if not any(prop == path or prop.startswith(path + '.') for path in paths):
        return False
    target = str(anchor.get('target', ''))
    if target in {'camera', 'lighting', 'light', 'scene', 'illumination'}:
        return (dimension == 'camera' and fact['entity'] == 'camera') or dimension == 'lighting'
    return target.replace('_', ' ') == fact['entity']


def extract_constraints(core: Mapping[str, Any]) -> dict[str, Any]:
    """Read frozen v3 sources without modifying or expanding the input contract.

    Active requester spans are authoritative. Anchors must be grounded in an
    active span and literal baseline evidence. Property locks must use v2 and
    canonical target/property paths in an open dimension. A bare locked
    dimension never turns all authorial baseline prose into requester facts.
    """
    baseline = str(core.get('baseline_prompt_en') or '')
    parsed = _parse(baseline, 'baseline_prompt_en', 'authorial_open')
    facts = list(parsed['facts'])
    unknowns = []
    active = []
    request = str(core.get('source_request') or '')
    binding = core.get('request_binding') or {}
    for index, span in enumerate(binding.get('active_spans') or []):
        if not isinstance(span, Mapping) or not isinstance(span.get('text'), str) or not span['text'].strip():
            unknowns.append({'source': 'request_binding.active_spans', 'reason': 'invalid_active_span'})
            continue
        text = span['text']
        if request and text not in request:
            unknowns.append({'source': 'request_binding.active_spans', 'evidence': text, 'reason': 'unbound_active_span'})
            continue
        if request and isinstance(span.get('start'), int) and isinstance(span.get('end'), int) and request[span['start']:span['end']] != text:
            unknowns.append({'source': 'request_binding.active_spans', 'evidence': text, 'reason': 'active_span_offset_mismatch'})
            continue
        active.append(span)
        result = _parse(text, f'request_binding.active_spans[{index}]', 'requester_locked')
        for row in result['facts']:
            row['source_span_id'] = span.get('span_id', '')
        facts.extend(result['facts'])
        unknowns.extend(result['unknowns'])
    lock = core.get('intent_lock') or {}
    for index, anchor in enumerate(lock.get('semantic_anchors') or []):
        if not isinstance(anchor, Mapping):
            continue
        source = f'intent_lock.semantic_anchors[{index}]'
        evidence = str(anchor.get('prompt_evidence') or '')
        source_text = str(anchor.get('source_text') or '')
        supported = [s for s in active if source_text and source_text.casefold() in s['text'].casefold()]
        dimension = anchor.get('dimension')
        valid = bool(supported and evidence and evidence.casefold() in baseline.casefold())
        if 'property' in anchor:
            valid = valid and lock.get('contract_version') == 'photo-intent-lock/v2' and dimension in (lock.get('open_dimensions') or [])
            valid = valid and all(re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*', str(anchor.get(k) or '')) for k in ('target', 'property'))
        else:
            valid = valid and dimension in (lock.get('locked_dimensions') or [])
        if not valid:
            unknowns.append({'source': source, 'evidence': evidence, 'reason': 'invalid_or_unbound_anchor'})
            continue
        matched = []
        for fact in parsed['facts']:
            if re.sub(r'^(?:the|a|an)\s+', '', fact['evidence'].casefold()) in evidence.casefold() and _property_matches(anchor, fact):
                row = {**fact, 'source': source, 'ownership': 'requester_locked', 'anchor_id': anchor.get('anchor_id', ''),
                       'source_span_ids': [s.get('span_id', '') for s in supported], 'requester_evidence': source_text,
                       'anchor_evidence': evidence}
                matched.append(row)
        facts.extend(matched)
        if not matched:
            if dimension in {'camera', 'lighting'}:
                unknowns.append({'source': source, 'evidence': evidence, 'dimension': dimension, 'reason': 'anchor_outside_recognized_footprint'})
    locked = [row for row in facts if row['ownership'] == 'requester_locked']
    return {'version': VERSION, 'source_core_sha256': core.get('canonical_sha256', ''), 'source_request_sha256': hashlib.sha256(request.encode()).hexdigest(), 'source_baseline_sha256': hashlib.sha256(baseline.encode()).hexdigest(), 'facts': facts,
            'locked_facts': locked, 'open_facts': [row for row in facts if row['ownership'] == 'authorial_open'],
            'unknowns': unknowns, 'coverage': _coverage(unknowns), 'baseline_ignored_spans': parsed['ignored_spans'], 'baseline_unknowns': parsed['unknowns']}


def _coverage(unknowns: list[dict[str, Any]]) -> dict[str, Any]:
    return {'scope': 'partial_explicit_english', 'complete': False, 'unknown_count': len(unknowns),
            'limitations': list(LIMITATIONS)}


def _same_entity(left: Mapping[str, Any], right: Mapping[str, Any], facts: list[dict[str, Any]]) -> bool:
    a, b = str(left['entity']), str(right['entity'])
    if a == b:
        return True
    # Generic reference to the one named object can resolve to that object.
    # Distinct modifiers never collapse (desk lamp != ceiling lamp).
    if ' ' in a and b == a.split()[-1] or ' ' in b and a == b.split()[-1]:
        head = a.split()[-1]
        specific = {str(row['entity']) for row in facts if str(row['entity']).endswith(' ' + head)}
        return len(specific) == 1
    return False


def _compare(locked: list[dict[str, Any]], observed: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], set[int]]:
    conflicts, matches, satisfied = [], [], set()
    all_facts = locked + observed
    for index, requirement in enumerate(locked):
        for found in observed:
            if requirement['property'] != found['property'] or not _same_entity(requirement, found, all_facts):
                continue
            same = requirement['value'] == found['value']
            opposite_polarity = requirement['polarity'] != found['polarity']
            conflict = same and opposite_polarity
            if not same and requirement['polarity'] == found['polarity'] == 'positive':
                # Several actual light sources may coexist unless "only" was
                # explicit. Directions/states of the same source are exclusive.
                conflict = requirement['property'] != 'lighting.source' or bool(requirement.get('exclusive'))
                # Window daylight and daylight are not disjoint source types.
                if requirement['property'] == 'lighting.source' and {requirement['value'], found['value']} <= {'window', 'daylight'}:
                    conflict = False
            if conflict:
                conflicts.append({'reason': 'explicit_incompatible_fact', 'locked_fact': requirement, 'observed_fact': found})
            elif same and not opposite_polarity:
                satisfied.add(index)
                matches.append({'locked_fact': requirement, 'observed_fact': found})
    return conflicts, matches, satisfied


def _unresolved_entity_comparisons(locked: list[dict[str, Any]], observed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unknowns = []
    all_facts = locked + observed
    for requirement in locked:
        for found in observed:
            if requirement['property'] != found['property'] or _same_entity(requirement, found, all_facts):
                continue
            if not requirement['property'].startswith('lighting.direction.'):
                continue
            a, b = str(requirement['entity']), str(found['entity'])
            if (a == 'illumination' or b == 'illumination') and requirement['value'] != found['value']:
                unknowns.append({'source': found['source'], 'evidence': found['evidence'],
                                 'reason': 'unresolved_direction_source_identity', 'locked_fact': requirement})
    return unknowns


def _unresolved_inactive_sources(locked: list[dict[str, Any]], observed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """A source-family fragment does not identify a physical source instance.

    Do not infer that all lamps are one lamp or that a noun fragment states an
    exact actor-emission relation. Explicitly distinct qualified sources are
    allowed; unresolved identity requires review rather than hard rejection.
    """
    families = {'lamp': {'lamp', 'lantern'}, 'flash': {'flash', 'strobe'},
                'softbox': {'softbox'}, 'candle': {'candle'}, 'screen': {'screen', 'monitor'}}
    unknowns = []
    for inactive in locked:
        if inactive['property'] != 'lighting.state' or inactive['value'] != 'inactive' or inactive['polarity'] != 'positive':
            continue
        actor = str(inactive['entity'])
        head = actor.split()[-1]
        for source in observed:
            if source['property'] != 'lighting.source' or source['polarity'] != 'positive' or head not in families.get(source['value'], set()):
                continue
            other = str(source.get('source_entity') or '')
            # Qualification on both sides proves different named source NPs.
            # An unqualified noun on either side leaves identity unresolved.
            if other and ' ' in actor and ' ' in other and actor != other:
                continue
            unknowns.append({'source': source['source'], 'evidence': source['evidence'],
                             'reason': 'source_family_inactive_actor_identity_unresolved',
                             'locked_fact': inactive, 'observed_fact': source})
    return unknowns


def _change_mode(constraints: Mapping[str, Any], parsed: Mapping[str, Any], label: str) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    """A source label alone does not say whether it replaces or supplements.

    Camera properties with no requester lock can be replaced; source mixing
    requires a local secondary/addition role or an explicit replacement verb.
    This does not turn replaceable baseline choices into hard constraints.
    """
    unknowns, conflicts = [], []
    sources = [f for f in parsed['facts'] if f['property'] == 'lighting.source' and f['polarity'] == 'positive']
    previous = [f for f in constraints['facts'] if f['property'] == 'lighting.source' and f['polarity'] == 'positive']
    if not sources:
        return 'property_refinement', unknowns, conflicts
    source_values = {f['value'] for f in sources}
    previous_values = {f['value'] for f in previous}
    if source_values <= previous_values or source_values | previous_values <= {'window', 'daylight'}:
        return 'same_source_refinement', unknowns, conflicts
    if not previous_values:
        return 'open_source_addition', unknowns, conflicts
    replacement = bool(re.search(r'\b(?:replace|replaces|replacing|substitute|substitutes|substituting)\b', label, re.I))
    secondary = bool(re.search(r'\b(?:fill|secondary|supplemental|supplementary)\b', label, re.I))
    if replacement:
        for locked in constraints['locked_facts']:
            if locked['property'] == 'lighting.source' and locked['polarity'] == 'positive' and locked['value'] not in source_values:
                conflicts.append({'reason': 'replacement_removes_required_source', 'locked_fact': locked, 'observed_fact': sources[0]})
        return 'explicit_replacement', unknowns, conflicts
    if secondary:
        return 'explicit_secondary_addition', unknowns, conflicts
    unknowns.append({'source': 'entry.en', 'evidence': label, 'reason': 'source_addition_or_replacement_unspecified',
                     'existing_sources': sorted(previous_values), 'candidate_sources': sorted(source_values)})
    return 'unknown', unknowns, conflicts


def _combination_conflicts(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    for index, first in enumerate(facts):
        conflicts, _, _ = _compare([first], facts[index + 1:])
        for conflict in conflicts:
            conflict['reason'] = 'inconsistent_final_combination'
            result.append(conflict)
    return result


def assess_candidate(core: Mapping[str, Any], entry: Mapping[str, Any], slot: str) -> dict[str, Any]:
    """Assess the authored label only. Unknown entries are never certified safe."""
    constraints = extract_constraints(core)
    parsed = _parse(str(entry.get('en') or ''), 'entry.en', 'candidate', slot)
    conflicts, matches, _ = _compare(constraints['locked_facts'], parsed['facts'])
    change_mode, change_unknowns, change_conflicts = _change_mode(constraints, parsed, str(entry.get('en') or ''))
    conflicts.extend(change_conflicts)
    unknowns = list(parsed['unknowns']) + change_unknowns + _unresolved_entity_comparisons(constraints['locked_facts'], parsed['facts']) + _unresolved_inactive_sources(constraints['locked_facts'], parsed['facts'])
    relevant = [row for row in parsed['facts'] if
                (slot in LIGHT_SLOTS and row['property'].startswith('lighting.')) or
                (slot in CAMERA_SLOTS and row['property'].startswith('camera.')) or
                (slot not in LIGHT_SLOTS | CAMERA_SLOTS and row['property'] == 'presence')]
    if not relevant:
        unknowns.append({'source': 'entry.en', 'reason': 'no_recognized_slot_footprint'})
    # An unparsed requester sentence may contain a relevant lock. Do not claim
    # that the lack of a recognized conflict has established compatibility.
    dimensions = ({'lighting'} if slot in LIGHT_SLOTS else {'camera'} if slot in CAMERA_SLOTS else set())
    for row in constraints['unknowns']:
        if row.get('dimension') in dimensions or _relevant_unknown(str(row.get('evidence', ''))):
            unknowns.append(row)
    status = 'contradiction' if conflicts else 'unknown' if unknowns else 'compatible'
    return {'version': VERSION, 'status': status, 'slot': slot, 'change_mode': change_mode, 'facts': parsed['facts'],
            'candidate_text_sha256': hashlib.sha256(str(entry.get('en') or '').encode()).hexdigest(),
            'ignored_spans': parsed['ignored_spans'],
            'contradictions': conflicts, 'matches': matches, 'unknowns': unknowns,
            'coverage': _coverage(unknowns), 'source_core_sha256': constraints['source_core_sha256'],
            'source_request_sha256': constraints['source_request_sha256'], 'source_baseline_sha256': constraints['source_baseline_sha256']}


def validate_final(core: Mapping[str, Any], prompt_en: str) -> dict[str, Any]:
    """Detect explicit opposing additions and report every unpreserved lock."""
    constraints = extract_constraints(core)
    parsed = _parse(str(prompt_en or ''), 'prompt_en', 'final')
    conflicts, matches, satisfied = _compare(constraints['locked_facts'], parsed['facts'])
    combination_conflicts = _combination_conflicts(parsed['facts'])
    combination_unknowns = _unresolved_inactive_sources(parsed['facts'], parsed['facts'])
    missing = [fact for index, fact in enumerate(constraints['locked_facts']) if index not in satisfied]
    unknowns = list(parsed['unknowns']) + list(constraints['unknowns']) + _unresolved_entity_comparisons(constraints['locked_facts'], parsed['facts']) + _unresolved_inactive_sources(constraints['locked_facts'], parsed['facts'])
    unknowns.extend(row for row in combination_unknowns if row not in unknowns)
    if not constraints['locked_facts']:
        unknowns.append({'source': 'core', 'reason': 'no_recognized_requester_locks'})
    status = 'contradiction' if conflicts or combination_conflicts else 'unknown' if missing or unknowns else 'compatible'
    return {'version': VERSION, 'status': status, 'facts': parsed['facts'], 'contradictions': conflicts,
            'combination_conflicts': combination_conflicts, 'ignored_spans': parsed['ignored_spans'],
            'prompt_sha256': hashlib.sha256(str(prompt_en or '').encode()).hexdigest(),
            'matches': matches, 'missing_locked_facts': missing, 'unknowns': unknowns,
            'coverage': _coverage(unknowns), 'source_core_sha256': constraints['source_core_sha256'],
            'source_request_sha256': constraints['source_request_sha256'], 'source_baseline_sha256': constraints['source_baseline_sha256']}
