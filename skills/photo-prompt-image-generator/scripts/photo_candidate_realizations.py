"""Canonical conditional effects; a selected branch never inherits other branches.

Source effects remain owned once. Branch member references reuse canonical
records and guards, rather than copying meanings or adding search documents.
"""
from __future__ import annotations
import copy

PROJECTION_FIELDS = frozenset({'en', 'ko', 'embedding_text', 'concept_units', 'relations'})


def validate_content(record):
    """Primitive OR choices may own explicit text, never identity or guards.

    Canonical search text remains owned once by the source record. These
    manually authored render projections do not create search documents.
    """
    choices = record['content'].get('realization_content')
    if choices is None:
        return
    import photo_candidate_corpus as c
    if (record['record_kind'] != 'visual_option'
            or not record['effects'].get('realizations')
            or not isinstance(choices, dict) or set(choices) != set(ids(record))):
        raise ValueError('primitive realization text must cover every actual branch exactly once')
    for rid, text in choices.items():
        if (not isinstance(text, dict) or set(text) != PROJECTION_FIELDS
                or any(not isinstance(text[k], str) or not text[k].strip()
                       for k in ('en', 'ko', 'embedding_text'))
                or not c.strings(text['concept_units'], rid + '.concept_units')
                or not isinstance(text['relations'], list)
                or any(not isinstance(row, dict) for row in text['relations'])):
            raise ValueError('primitive realization text cannot replace identity, guards or other metadata')


def project_content(record, realization_id):
    """Project one declared primitive choice without mutating its source."""
    choices = record['content'].get('realization_content')
    if choices is None:
        return {}
    branch(record, realization_id)  # Reject foreign choices even without a prior validate call.
    selected = copy.deepcopy(choices[realization_id])
    # Canonical aliases/keywords can describe both alternatives. They remain
    # in the single search document, but cannot leak into a selected render
    # view or reject it for words belonging only to another choice.
    selected.update(aliases=[], keywords=[], terms=[], paraphrases=[], concept_terms=[],
                    phrase_en=selected['en'], phrase_ko=selected['ko'])
    return selected


def ids(record):
    conditional = record['effects'].get('realizations')
    if not conditional:
        return ['base']
    result = [row['id'] for row in conditional['branches']]
    return (['base'] + result) if conditional['mode'] == 'optional' else result


def branch(record, realization_id):
    if realization_id not in ids(record):
        raise ValueError('unknown canonical realization')
    if realization_id == 'base':
        return None
    return next(row for row in record['effects']['realizations']['branches']
                if row['id'] == realization_id)


def effects(record, realization_id):
    selected = branch(record, realization_id)
    base = record['effects']
    dimensions = list(base['dimensions'])
    properties = copy.deepcopy(base['properties'])
    if selected:
        dimensions = sorted(set(dimensions) | set(selected['effects']['dimensions']))
        for row in selected['effects']['properties']:
            if row not in properties:
                properties.append(copy.deepcopy(row))
    return {'dimensions': dimensions, 'properties': properties}


def member_ids(record, realization_id):
    selected = branch(record, realization_id)
    if selected and 'member_candidate_ids' in selected:
        return set(selected['member_candidate_ids'])
    return {p['candidate_id'] for p in record['content'].get('member_candidates', [])}


def context_satisfied(selected, core):
    """Require an already declared witness; candidate prose is never a witness."""
    if not selected or not selected.get('context_terms'):
        return True
    import prompt_generator as g
    text, _ = g.authorial_core_retrieval_text(core)
    return any(g.intent_alias_matches(text, term)
               and not g.intent_term_is_negated(text, term)
               for term in selected['context_terms'])


def entries(data, candidate_id, binding_id=None):
    import photo_candidate_corpus as c
    record = data['candidates'][candidate_id]
    return [c.entry(data, candidate_id, binding_id, realization_id=rid) for rid in ids(record)]


def selected_view(candidate, interpretation):
    """Resolve only an explicit presented choice, preserving the canonical body."""
    record=candidate.get('authored_record') or {}
    if not (record.get('effects') or {}).get('realizations'):
        return candidate
    rid=interpretation.get('realization_id')
    if rid not in ids(record):
        raise ValueError('conditional candidate requires one explicit canonical realization_id')
    choices={row['realization_id']:row for row in candidate.get('realization_choices',[])}
    if not choices:
        choices=candidate.get('realization_views') or {}
    if rid not in choices:
        raise ValueError('selected realization was not presented as eligible')
    return {**copy.deepcopy(candidate),**copy.deepcopy(choices[rid]),'realization_id':rid}


def eligible_ids(data, candidate_id, core, contract, picked, slot='', binding_id=None,
                 *, check_effect_scope=True):
    import photo_candidate_corpus as c
    import prompt_generator as g
    record = data['candidates'][candidate_id]
    result = []
    for rid in ids(record):
        selected = branch(record, rid)
        if not context_satisfied(selected, core):
            continue
        entry = c.entry(data, candidate_id, binding_id, realization_id=rid)
        if not g.core_entry_eligible(data, core, contract, picked, slot, entry,
                                     check_effect_scope=check_effect_scope):
            continue
        if selected and selected.get('conditions'):
            guard = {**copy.deepcopy(entry), **copy.deepcopy(selected['conditions'])}
            # AND with the canonical guard, already checked above.
            if not g.core_entry_eligible(data, core, contract, picked, slot, guard,
                                         check_effect_scope=False):
                continue
        pointers = record['content'].get('member_candidates', [])
        wanted = member_ids(record, rid)
        if any(not eligible_ids(data, pointer['candidate_id'], core, contract, picked,
                                data['slot_bindings'][pointer['binding_id']]['slot_id'],
                                pointer['binding_id'])
               for pointer in pointers if pointer['candidate_id'] in wanted):
            continue
        result.append(rid)
    return result
