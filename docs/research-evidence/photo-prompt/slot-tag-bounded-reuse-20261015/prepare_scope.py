"""Freeze existing-review cases using metadata only; no semantic approvals."""
import copy
from common import *


def main():
    data = source()
    baseline = read(BASELINE)
    pairs = {(v['candidate_id'], v['slot_id']): bid for bid, v in data['slot_bindings'].items()}
    deferred = data['policies']['_slot_binding_review']['deferred']
    inventory_path = RESEARCH / 'ROOT-CURRENT149-APPROVAL-INVENTORY-04.json'
    assert artifact(inventory_path)['sha256'] == baseline['inventory']['raw_sha256']
    inventory = read(inventory_path)
    primary_ids = {r['candidate_id'] for r in baseline['primary_scope']['records']}
    batch_cache = {}
    primary = []
    for record in baseline['primary_scope']['records']:
        file = record['batch']['file']
        batch_cache.setdefault(file, read(ROOT / file))
        rows = {r['candidate_id']: r for r in batch_cache[file]['records']}
        row = rows[record['candidate_id']]
        current = data['candidates'][record['candidate_id']]
        assert c.digest(current) == record['operating_record_sha256']
        assert c.digest(row['proof']) == record['accepted_proof_sha256']
        after = copy.deepcopy(row['source_after'])
        actual = copy.deepcopy(current)
        for value in (after, actual):
            for key in ('application_contract', 'role_evidence'):
                value['content'].pop(key, None)
        assert actual == after
        primary.append({**record, 'source': current, 'accepted_review': row})
    assert len(primary) == 9 and sum(len(r['role_pairs']) for r in primary) == 19
    old_catalog = read(PILOT / 'CATALOG.json')
    if 'slot_catalog' in old_catalog:
        old_catalog = old_catalog['slot_catalog']
    rows = [json.loads(line) for line in (PILOT / 'REVIEWS.jsonl').read_text().splitlines()]
    screening = {'pilot_rows': len(rows), 'exact_source_no_correction': 0,
                 'same_specs_and_existing_witness_eligible_pairs': 0}
    eligible = []
    for row in rows:
        cid = row['candidate_id']
        if cid in primary_ids or cid in {r['candidate_id'] for r in baseline['already_applied_comparator']}:
            continue
        current = data['candidates'][cid]
        if (row['source_record_sha256'] != c.digest(current)
                or row['reviewed_record_sha256'] != c.digest(current)
                or row['correction_proposal'] or row['reference_ids']
                or row['record_kind_reviewed'] != current['record_kind']
                or current['record_kind'] == 'diagnostic'):
            continue
        screening['exact_source_no_correction'] += 1
        witnesses = sorted(bid for bid, binding in data['slot_bindings'].items()
                           if binding['candidate_id'] == cid)
        if not witnesses:
            continue
        for decision in row['role_decisions']:
            slot = decision['slot_id']
            if decision['decision'] not in ('retain', 'add') or slot not in data['slot_catalog']:
                continue
            # A pilot row explicitly requiring source refinement is not reusable.
            if decision['native_owned_fit_diagnostic']['status'] != 'eligible':
                continue
            spec = data['slot_catalog'][slot]
            related = {slot, *spec['neighbors']}
            if any(old_catalog.get(tag) != data['slot_catalog'].get(tag) for tag in related):
                continue
            bid = pairs.get((cid, slot))
            if bid and bid not in deferred:
                continue  # no-op rows do not consume the supplement
            screening['same_specs_and_existing_witness_eligible_pairs'] += 1
            rank = 0 if bid in deferred else 1 if slot not in old_catalog else 2
            eligible.append((rank, cid, slot, row, decision, bid, witnesses[0]))
    selected = {}
    for rank, cid, slot, row, decision, bid, witness in sorted(eligible, key=lambda v: v[:3]):
        if cid not in selected and len(selected) == 12:
            continue
        count = sum(len(v['role_pairs']) for v in selected.values())
        if count == 24:
            break
        if cid not in selected:
            selected[cid] = {'candidate_id': cid, 'source': data['candidates'][cid],
                             'pilot_review': row, 'role_pairs': []}
        selected[cid]['role_pairs'].append({'slot_id': slot, 'binding_id': bid,
            'state': 'deferred' if bid in deferred else 'missing',
            'witness_binding_id': witness, 'pilot_decision': decision})
    scope = {'schema': 'photo-bounded-tag-reuse-scope/v1',
        'source_sha256': c.digest(data), 'catalog_sha256': c.digest(data['slot_catalog']),
        'baseline': artifact(BASELINE), 'inventory': artifact(inventory_path),
        'pilot_catalog': artifact(PILOT / 'CATALOG.json'),
        'pilot_reviews': artifact(PILOT / 'REVIEWS.jsonl'), 'screening': screening,
        'primary': primary, 'supplement': list(selected.values()),
        'source_semantic_approval_created': False, 'new_native_qualification': False,
        'Gemini_calls': 0, 'replacements_after_deferral': False}
    count = len(primary) + len(selected)
    cases = sum(len(v['role_pairs']) for v in primary + list(selected.values()))
    assert count <= 21 and cases <= 43
    save('SCOPE.json', scope)
    # Packets contain only the frozen candidates, original evidence, and their
    # relevant specifications; printing them later cannot expand the scope.
    for group, values in [('primary', primary), ('supplement', list(selected.values()))]:
        for row in values:
            slots = {case['slot_id'] for case in row['role_pairs']}
            slots |= {n for tag in list(slots) for n in data['slot_catalog'][tag]['neighbors']}
            save('packets/' + group + '-' + row['candidate_id'] + '.json',
                 {**row, 'current_specs': {tag: data['slot_catalog'][tag] for tag in sorted(slots)}})
    save('STAGE01.json', {'status': 'PASS', 'pull': 'already up to date',
        'primary_candidates': len(primary), 'primary_pairs': 19,
        'supplement_candidates': len(selected), 'supplement_pairs': cases - 19,
        'total_candidates': count, 'total_pairs': cases, 'screening': screening,
        'new_semantic_approvals': 0, 'native_qualifications_added': 0, 'Gemini_calls': 0})
    print(json.dumps(read(HERE / 'STAGE01.json')))


if __name__ == '__main__':
    main()
