"""Stage the exact nineteen relation decisions and verify all source invariants."""
import copy
import time
from common import *
import photo_scoped_slot_adoption as scoped
import photo_global_index as index
import photo_semantic_evidence as native


def verify(before, after, manifest):
    c.validate(after)
    assert before['candidates'] == after['candidates']
    assert before['slot_catalog'] == after['slot_catalog']
    assert set(after['candidates']) == set(before['candidates'])
    assert all(after['slot_bindings'][bid] == row for bid, row in before['slot_bindings'].items())
    for key in set(before['policies']) - {'_slot_binding_review'}:
        assert before['policies'][key] == after['policies'][key]
    expected_pairs = {(v['after']['candidate_id'], v['after']['slot_id'])
                      for v in manifest['binding_decisions']}
    scope = read(HERE / 'SCOPE.json')
    assert expected_pairs == {(v['candidate_id'], p['slot_id']) for v in scope['primary'] for p in v['role_pairs']}
    assert len(expected_pairs) == 19
    new = set(after['slot_bindings']) - set(before['slot_bindings'])
    assert new == {v['after']['id'] for v in manifest['binding_decisions'] if v['action'] == 'add'}
    old_policy = before['policies']['_slot_binding_review']
    policy = after['policies']['_slot_binding_review']
    released = set(old_policy['deferred']) - set(policy['deferred'])
    assert len(new) == 10 and len(released) == 6 and len(policy['deferred']) == 3483
    assert all(policy['deferred'][bid] == row for bid, row in old_policy['deferred'].items() if bid not in released)
    assert all(policy['reviewed'][bid] == row for bid, row in old_policy['reviewed'].items())
    assert len(policy['reviewed']) == 40
    suspended_before = {cid for cid, row in before['candidates'].items() if c.deferred_dependency_bindings(before, row)}
    suspended_after = {cid for cid, row in after['candidates'].items() if c.deferred_dependency_bindings(after, row)}
    assert suspended_after <= suspended_before
    assert sum(native.native_status(v) == 'qualified' for v in after['candidates'].values()) == 1
    assert all(index.text(row) == index.text(after['candidates'][cid]) for cid, row in before['candidates'].items())
    return {'status': 'PASS', 'source_sha256': c.digest(before), 'result_sha256': c.digest(after),
        'candidate_count': len(after['candidates']), 'all_candidates_byte_value_equal': True,
        'catalog_sha256': c.digest(after['slot_catalog']), 'slots': 149,
        'binding_count': len(after['slot_bindings']), 'new_bindings': sorted(new),
        'released_bindings': sorted(released), 'remaining_deferred': len(policy['deferred']),
        'reviewed_relations': len(policy['reviewed']), 'native_qualified': 1,
        'dependency_suspended_before': len(suspended_before), 'dependency_suspended_after': len(suspended_after),
        'dependency_recovered': sorted(suspended_before - suspended_after),
        'all_original_binding_values_preserved': True, 'embedding_inputs_equal': True,
        'Gemini_calls': 0, 'whole_corpus_meaning_review': False}


def main():
    before = source()
    manifest = read(HERE / 'MIGRATION.json')
    staging = Path('/tmp/photo-bounded-tags-staged-' + str(time.time_ns()))
    preview = scoped.stage_assets(SKILL / 'assets', manifest, staging)
    after = c.load(staging)
    report = verify(before, after, manifest)
    try:
        scoped.build_preview(after, manifest)
    except ValueError as error:
        assert 'exact original source/catalog digest required' in str(error)
    else:
        raise AssertionError('a stale/already applied manifest must fail')
    tampered = copy.deepcopy(manifest)
    added = next(v for v in tampered['binding_decisions'] if v['action'] == 'add')
    added['after']['conditions'] = {'for_any': ['unreviewed_guard_rewrite']}
    try:
        scoped.build_preview(before, tampered)
    except ValueError as error:
        assert 'witness' in str(error)
    else:
        raise AssertionError('a new tag cannot invent different guard conditions')
    report.update(staged_assets=str(staging), raw_stage=preview['report'],
                  already_applied_rejected=True, condition_tampering_rejected=True)
    save('STAGE03.json', report)
    print(json.dumps({k: v for k, v in report.items() if k != 'raw_stage'}))


if __name__ == '__main__':
    main()
