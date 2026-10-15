"""Data-scoped positive/negative role checks; no new semantic source reviews."""
import copy
from common import *
from stage_and_verify import verify
import photo_role_proposals as roles
import photo_candidate_realizations as realizations


def main():
    after = c.load(SKILL / 'assets')
    report = read(HERE / 'STAGE04.json')
    before = copy.deepcopy(after)
    old_policy = read(Path(report['backup']) / 'photo_candidate_policies.json')['policies']
    before['policies'].update(old_policy)
    migration = read(HERE / 'MIGRATION.json')
    for row in migration['binding_decisions']:
        if row['action'] == 'add':
            del before['slot_bindings'][row['after']['id']]
    assert c.digest(before) == migration['source_sha256']
    integrity = verify(before, after, migration)
    checked = []
    for decision in migration['binding_decisions']:
        binding = decision['after']
        bid, cid, tag = (binding[k] for k in ('id', 'candidate_id', 'slot_id'))
        entry = c.entry(after, cid, bid)
        assert entry['_native_qualification'] == 'unqualified'
        assert c.binding_review_status(after, bid) == 'reviewed'
        proposal = roles.propose(after, tag, cid, [bid])
        assert proposal['native_qualification'] != 'qualified'
        assert proposal['applicability_status'] != 'eligible'
        assert proposal['conditions'] == after['candidates'][cid]['conditions']
        assert proposal['role_conditions'] == binding['conditions']
        roles.validate(after, proposal, [bid])
        negative = roles.propose(after, tag, cid, [])
        assert negative['applicability_status'] == 'incompatible'
        assert negative['semantic_fit']['reason'] == 'declared_role_conditions_not_satisfied'
        if bid in before['policies']['_slot_binding_review']['deferred']:
            prior = roles.propose(before, tag, cid, [bid])
            assert prior['semantic_fit']['reason'] == 'declared_role_semantic_review_deferred'
            assert proposal['semantic_fit']['reason'] != 'declared_role_semantic_review_deferred'
        checked.append({'candidate_id': cid, 'slot': tag, 'binding_id': bid,
            'applicability': proposal['applicability_status'], 'reason': proposal['semantic_fit']['reason'],
            'native_qualification': proposal['native_qualification'], 'guard_negative': 'PASS'})
    remaining = after['policies']['_slot_binding_review']['deferred']
    bid = sorted(remaining)[0]
    original = after['slot_bindings'][bid]
    blocked = roles.propose(after, original['slot_id'], original['candidate_id'], [bid])
    assert blocked['semantic_fit']['reason'] == 'declared_role_semantic_review_deferred'
    recovered = integrity['dependency_recovered']
    for cid in recovered:
        assert not c.deferred_dependency_bindings(after, after['candidates'][cid])
        c.entry(after, cid)
    suspended = next(cid for cid, row in after['candidates'].items() if c.deferred_dependency_bindings(after, row))
    # Raw source lookup remains available; the presentation gate rejects it.
    assert realizations.eligible_ids(after, suspended, {}, {}, {}) == []
    save('RELATION-REGRESSION.json', {'status': 'PASS', 'integrity': integrity,
        'positive_relationship_cases': checked, 'negative_binding_cases': len(checked),
        'recovered_dependency_cases': len(recovered), 'remaining_deferred_and_dependency_cases': 'PASS',
        'native_qualification_added': False, 'candidate_adoptions': 0, 'Gemini_calls': 0})
    print(json.dumps({'status': 'PASS', 'relations': len(checked), 'guard_negatives': len(checked),
        'dependency_recovered': len(recovered), 'candidate_adoptions': 0}))


if __name__ == '__main__':
    main()
