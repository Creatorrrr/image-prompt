"""Validate nine authored relation decisions against accepted evidence only."""
import copy
from common import *
import native_reviews as reviews
import photo_scoped_slot_adoption as scoped


def at(value, pointer):
    for token in pointer.strip('/').split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def main():
    data = source()
    scope = read(HERE / 'SCOPE.json')
    authored = read(HERE / 'AUTHORED-DECISIONS.json')
    assert not scope['supplement']
    assert {r['ordinal'] for r in authored['records']} == {r['ordinal'] for r in scope['primary']}
    decisions, audit, verified = [], [], {}
    for row in scope['primary']:
        manual = next(v for v in authored['records'] if v['ordinal'] == row['ordinal'])
        assert set(manual['roles']) == {v['slot_id'] for v in row['role_pairs']}
        assert manual['quote'] in at(data['candidates'][row['candidate_id']], manual['pointer'])
        batch_path = ROOT / row['batch']['file']
        if str(batch_path) not in verified:
            folder = batch_path.parent
            checked = reviews.verify_batch(RESEARCH / 'native-inputs/prepared' / folder.name / 'ASSIGNMENT.json',
                batch_path, folder / 'NOTE.json', root=ROOT, here=RESEARCH)
            reviews.verify_acceptance(ROOT, row['acceptance'], checked)
            verified[str(batch_path)] = checked
        accepted = verified[str(batch_path)]['records'][row['candidate_id']]
        assert accepted['status'] == 'approved'
        assert c.digest(accepted['proof']) == row['accepted_proof_sha256']
        witnesses = sorted(
            (v for v in data['slot_bindings'].values() if v['candidate_id'] == row['candidate_id']), key=lambda v: v['id'])
        assert witnesses
        for case in row['role_pairs']:
            tag = case['slot_id']
            assert accepted['proof']['roles'][tag]['spec_sha256'] == c.digest(data['slot_catalog'][tag])
            before = data['slot_bindings'].get(case['binding_id'])
            witness = before or witnesses[0]
            action = 'retain' if before else 'add'
            after = copy.deepcopy(witness)
            if not before:
                after.update(id=scoped.binding_id(row['candidate_id'], tag), slot_id=tag)
            citation = '; '.join([row['acceptance']['file'], row['batch']['file'],
                'CID=' + row['candidate_id'], 'witness=' + witness['id'],
                manual['pointer'] + ': ' + manual['quote'], 'native qualification unchanged'])
            decisions.append({'action': action, 'before': before, 'after': after,
                              'reason': manual['reason'], 'source_citation': citation})
            audit.append({'candidate_id': row['candidate_id'], 'ordinal': row['ordinal'],
                'slot_id': tag, 'before_state': case['state'], 'decision': action,
                'binding_id': after['id'], 'source_pointer': manual['pointer'],
                'quote': manual['quote'], 'reason': manual['reason'],
                'negative_boundary': manual['negative_boundary'],
                'current_spec_sha256': c.digest(data['slot_catalog'][tag]),
                'accepted_proof_sha256': row['accepted_proof_sha256'],
                'native_permission_added': False})
    manifest = {'schema': scoped.SCHEMA, 'source_sha256': c.digest(data),
        'source_catalog_sha256': c.digest(data['slot_catalog']),
        'reviewed_catalog_sha256': c.digest(data['slot_catalog']),
        'catalog': data['slot_catalog'], 'catalog_reason': 'Keep the exact operating149 definitions.',
        'catalog_source_citation': str(BASELINE.relative_to(ROOT)), 'binding_decisions': decisions}
    preview = scoped.build_preview(data, manifest)
    after = preview['corpus']
    assert data['candidates'] == after['candidates'] and data['slot_catalog'] == after['slot_catalog']
    assert len(decisions) == 19 and sum(v['action'] == 'add' for v in decisions) == 10
    assert len(after['policies']['_slot_binding_review']['deferred']) == 3483
    save('MIGRATION.json', manifest)
    save('RELATION-REVIEW.json', {'schema': 'photo-bounded-existing-role-review/v1',
        'records': audit, 'candidates_read': 9, 'roles_reviewed': 19,
        'supplement': 0, 'new_native_qualifications': 0, 'whole_corpus_review': False})
    save('STAGE02.json', {'status': 'PASS', 'accepted_batches_reverified': len(verified),
        'source_sha256': c.digest(data), 'result_sha256': c.digest(after),
        'relations': 19, 'new_bindings': 10, 'deferred_released': 6,
        'existing_relations_retained': 3, 'remaining_deferred': 3483,
        'new_native_qualifications': 0, 'preview': preview['report'], 'Gemini_calls': 0})
    print(json.dumps(read(HERE / 'STAGE02.json')))


if __name__ == '__main__':
    main()
