"""Canonical conditional effects; a selected branch never inherits other branches.

Source effects remain owned once. Branch member references reuse canonical
records and guards, rather than copying meanings or adding search documents.
"""
from __future__ import annotations
import copy

PROJECTION_FIELDS = frozenset({'en', 'ko', 'embedding_text', 'concept_units', 'relations'})
# The existing primitive shape is unchanged. Mechanisms have an explicit
# per-kind extension because their canonical positive meaning lives in definition.
MECHANISM_PROJECTION_CONTRACT = 'photo-relationship-realization-content/v1'
MECHANISM_PROJECTION_FIELDS = PROJECTION_FIELDS | {'definition'}
PROJECTION_FIELDS_BY_KIND = {'visual_option': PROJECTION_FIELDS,
                             'relationship_mechanism': MECHANISM_PROJECTION_FIELDS}
# These positive source surfaces are read by index/render consumers but have no
# selected counterpart in the exact mechanism contract. Fail visibly rather
# than leaving an alternative in the selected entry or silently hiding it.
MECHANISM_UNPROJECTED_POSITIVE_FIELDS = frozenset({'ja', 'label_en', 'label_ko',
    'definitions_by_topic', 'manifestations', 'components', 'member_candidates',
    'embedding_texts', 'concept_candidate'})
MECHANISM_UNPROJECTED_SEMANTIC_FIELDS = frozenset({'definition', 'semantic_caption',
    'visual_components', 'support_cues', 'component_semantics'})


def validate_content(record):
    """Explicit OR choices own selected text, never identity or guards.

    Canonical search text remains owned once by the source record. These
    manually authored render projections do not create search documents.
    """
    choices = record['content'].get('realization_content')
    if choices is None:
        return
    import photo_candidate_corpus as c
    fields = PROJECTION_FIELDS_BY_KIND.get(record['record_kind'])
    if (fields is None
            or not record['effects'].get('realizations')
            or not isinstance(choices, dict) or set(choices) != set(ids(record))):
        raise ValueError('primitive realization text must cover every actual branch exactly once')
    if record['record_kind'] == 'relationship_mechanism':
        c.validate_effects(record['effects'], record['id'])
        unsupported = sorted(key for key in MECHANISM_UNPROJECTED_POSITIVE_FIELDS
                             if record['content'].get(key))
        semantics = record['content'].get('semantics')
        if isinstance(semantics, dict):
            unsupported.extend('semantics.' + key for key in sorted(
                MECHANISM_UNPROJECTED_SEMANTIC_FIELDS) if semantics.get(key))
        if unsupported:
            raise ValueError('mechanism projection has unprojected positive source fields: '
                             + ', '.join(unsupported))
    string_fields = ('en', 'ko', 'embedding_text', 'definition') if (
        record['record_kind'] == 'relationship_mechanism') else ('en', 'ko', 'embedding_text')
    for rid, text in choices.items():
        if (not isinstance(text, dict) or set(text) != fields
                or any(not isinstance(text[k], str) or not text[k].strip()
                       for k in string_fields)
                or not c.strings(text['concept_units'], rid + '.concept_units')
                or not isinstance(text['relations'], list)
                or any(not isinstance(row, dict) for row in text['relations'])):
            raise ValueError('primitive realization text cannot replace identity, guards or other metadata')


def project_content(record, realization_id):
    """Project one declared choice, preserving full canonical discovery text."""
    choices = record['content'].get('realization_content')
    if choices is None:
        return {}
    branch(record, realization_id)  # Reject foreign choices even without a prior validate call.
    if record['record_kind'] == 'relationship_mechanism':
        # entry() may be used without an earlier corpus validate(). Never emit
        # an unqualified mechanism definition or extra positive source surface.
        validate_content(record)
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
                 *, check_effect_scope=True, dependency_selections=None):
    import photo_candidate_corpus as c
    import prompt_generator as g
    record = data['candidates'][candidate_id]
    result = []
    for rid in ids(record):
        selected = branch(record, rid)
        if not context_satisfied(selected, core):
            continue
        entry = c.entry(data, candidate_id, binding_id, realization_id=rid, dependency_selections=dependency_selections)
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
        import photo_semantic_evidence as native
        selected_choices = dependency_selections or {}
        if native.native_status(record) == 'qualified':
            proof = native.proof_of(entry)
            adopted = {row['candidate_id'] for row,_ in native.selected_dependencies(proof, rid, selected_choices)}
        else:
            # Stage 5C search preserves canonical required/unspecified members.
            # Explicitly optional source members never default to all-selected.
            adopted = {row['candidate_id'] for row in pointers if row.get('adoption') != 'optional'
                       or row['candidate_id'] in selected_choices}
        member_failed = False
        for pointer in pointers:
            child_id = pointer['candidate_id']
            if child_id not in wanted or child_id not in adopted:
                continue
            # Transitional presentation conditions remain ANDed only when the
            # source explicitly names that binding. No old-binding lookup fallback.
            bid = pointer.get('binding_id')
            role = data['slot_bindings'][bid]['slot_id'] if bid else ''
            child_selections = selected_choices
            if native.native_status(data['candidates'][child_id]) == 'qualified':
                child_guard = native.compact(data['candidates'][child_id], data)
                descendant_ids = {cid for child_rid in ids(data['candidates'][child_id])
                    for cid in native.dependency_choices(child_guard, child_rid)}
                child_selections = {cid:value for cid,value in selected_choices.items() if cid in descendant_ids}
            choices = eligible_ids(data, child_id, core, contract, picked, role, bid,
                check_effect_scope=check_effect_scope, dependency_selections=child_selections)
            actual_choice = selected_choices.get(child_id)
            if not choices or actual_choice is not None and actual_choice not in choices:
                member_failed = True; break
        if member_failed:
            continue
        result.append(rid)
    return result
