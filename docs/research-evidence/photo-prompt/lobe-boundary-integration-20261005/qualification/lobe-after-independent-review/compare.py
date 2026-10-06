import copy
import hashlib
import json
from pathlib import Path

ROOT = Path('/workspace/scratch/ce8f20680f5a')
BASE = ROOT / 'recovery-after-reset-20261005'
OUT = BASE / 'lobe-after-independent-review'
BEFORE_REPO = ROOT / 'image-prompt-900-ct073'
AFTER_REPO = ROOT / 'image-prompt-lobe-after900'
ASSETS = Path('skills/photo-prompt-image-generator/assets')
TARGETS = {'visual-concept:orn_profile_gd46_three', 'visual-concept:orn_profile_gd46_four'}

def read(p):
    return json.loads(p.read_text())

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def write(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def differences(a, b, path=''):
    if type(a) is not type(b):
        yield {'path': path, 'before': a, 'after': b}
    elif isinstance(a, dict):
        for k in sorted(a.keys() | b.keys()):
            if k not in a or k not in b:
                yield {'path': path + '/' + k, 'before': a.get(k), 'after': b.get(k), 'key_missing': True}
            else:
                yield from differences(a[k], b[k], path + '/' + k)
    elif isinstance(a, list):
        if len(a) != len(b):
            yield {'path': path, 'before': a, 'after': b, 'length_changed': True}
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                yield from differences(x, y, path + '/' + str(i))
    elif a != b:
        yield {'path': path, 'before': a, 'after': b}

def id_list(value):
    return (isinstance(value, list) and bool(value)
            and all(isinstance(v, dict) and isinstance(v.get('id'), str) for v in value)
            and len({v['id'] for v in value}) == len(value))

def align(value):
    if isinstance(value, dict):
        return {k: align(v) for k, v in value.items()}
    if id_list(value):
        return {'ID=' + v['id']: align(v) for v in value}
    if isinstance(value, list):
        return [align(v) for v in value]
    return value

def lists(value, path=''):
    result = {}
    if isinstance(value, dict):
        for k, v in value.items():
            result.update(lists(v, path + '/' + k))
    elif isinstance(value, list):
        if id_list(value):
            result[path] = [v['id'] for v in value]
            for v in value:
                result.update(lists(v, path + '/ID=' + v['id']))
        else:
            for i, v in enumerate(value):
                result.update(lists(v, path + '/' + str(i)))
    return result

def surface_inventory(value, path=''):
    result = {}
    if isinstance(value, dict):
        for k, v in value.items():
            child = path + '/' + k
            if isinstance(v, list) and ('candidates' in k or k == 'candidate_inventory'):
                result[child] = {'count': len(v), 'ids': [x.get('id') if isinstance(x, dict) else x for x in v]}
            result.update(surface_inventory(v, child))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            result.update(surface_inventory(v, path + '/' + str(i)))
    return result

seal_path = BASE / 'lobe-boundary-candidate/candidate-20-file-seal.json'
assert digest(seal_path) == '8bf0dfe263cd9dace49de1f54b4744ab915e56dd49658511f2ef879dc6033f75'
seal_checks = []
for row in read(seal_path)['files']:
    p = AFTER_REPO / row['path']
    check = {'path': row['path'], 'expected_sha256': row['sha256'], 'actual_sha256': digest(p), 'size_matches': p.stat().st_size == row['bytes']}
    assert check['expected_sha256'] == check['actual_sha256'] and check['size_matches']
    seal_checks.append(check)

before_manifest = BASE / 'lobe-before-independent-review/inventory_manifest.json'
assert digest(before_manifest) == 'a888e40bfd25dfd03c47ef7b7c73ea581df1c4b2c60ed8d4f7a3ef5abd657859'
for row in read(before_manifest)['files']:
    assert digest(before_manifest.parent / row['path']) == row['sha256']

source_delta = []
for filename in ['photo_prompt_ornament_structure_extension.json', 'photo_prompt_visual_obligations_ornament_structure.json']:
    rel = ASSETS / filename
    for diff in differences(read(BEFORE_REPO / rel), read(AFTER_REPO / rel)):
        source_delta.append({'file': str(rel), 'pointer': diff['path'], 'before': diff['before'], 'after': diff['after']})
assert sorted(source_delta, key=lambda v: (v['file'], v['pointer'])) == sorted(read(BASE / 'lobe-boundary-candidate/pointer-delta.json'), key=lambda v: (v['file'], v['pointer']))
assert len(source_delta) == 9

index_checks = []
for filename in ['photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json']:
    a, b = read(BEFORE_REPO / ASSETS / filename), read(AFTER_REPO / ASSETS / filename)
    ds = list(differences(a, b))
    shard_checks = []
    for old, new in zip(a['shards'], b['shards']):
        p, q = BEFORE_REPO / ASSETS / old['path'], AFTER_REPO / ASSETS / new['path']
        assert p.read_bytes() == q.read_bytes()
        assert digest(p) == old['sha256'] == new['sha256'] == digest(q)
        shard_checks.append({'before_path': old['path'], 'after_path': new['path'], 'sha256': digest(p), 'byte_identical': True})
    index_checks.append({'file': filename, 'delta': ds, 'all_shards_identical': True, 'shards': shard_checks})

runtime_rel = Path('skills/photo-prompt-image-generator/scripts/prompt_generator.py')
assert (BEFORE_REPO / runtime_rel).read_bytes() == (AFTER_REPO / runtime_rel).read_bytes()

cases = []
all_deltas = {}
command_records = {c['case']: c for c in read(BASE / 'lobed-opening-after-900/COMMANDS.json')}
for case in ['three_lobed_stone', 'four_lobed_timber', 'painted_solid_panel', 'single_round_brick']:
    old_dir = 'lobed-opening-before-900-setting-adapter-01' if case == 'four_lobed_timber' else 'lobed-opening-before-900'
    bp, ap = BASE / old_dir / (case + '.pack.json'), BASE / 'lobed-opening-after-900' / (case + '.pack.json')
    before, after = read(bp), read(ap)
    assert len(before) == len(after) == 1
    assert digest(ap) == command_records[case]['pack_sha256']
    assert command_records[case]['returncode'] == 0
    raw = list(differences(before, after))
    by_id = list(differences(align(before), align(after)))
    old_lists, new_lists = lists(before), lists(after)
    assert old_lists.keys() == new_lists.keys()
    order_changes = []
    for path in old_lists:
        a, b = old_lists[path], new_lists[path]
        assert sorted(a) == sorted(b), ('candidate membership changed', case, path)
        if a != b:
            order_changes.append({'path': path, 'before': a, 'after': b, 'added_ids': [], 'removed_ids': []})
    for delta in by_id:
        path = delta['path']
        allowed = (path in ['/0/pack_id', '/0/provenance/tags_hash']
                   or (path.startswith('/0/visual_concept_candidates/candidates/ID=visual-concept:orn_profile_gd46_') and '/opt_in_contract/obligation/reject_substitutes/' in path)
                   or (path.startswith('/0/candidate_bundles/candidates/ID=bundle:orn_gd46_') and any(p in path for p in ['/confusion_boundaries/', '/source_sha256', '/source_contract_sha256']))
                   or (case == 'single_round_brick' and path.startswith('/0/candidate_bundles/candidates/ID=bundle:rbb_') and path.endswith('/joint_admission/source_dictionary_sha256')))
        assert allowed, ('unplanned content delta', case, delta)
    a, b = before[0], after[0]
    av, bv = a['visual_concept_candidates']['candidates'], b['visual_concept_candidates']['candidates']
    variation_material = '|'.join([str(a['provenance'].get('seed') or ''), str(a['provenance'].get('batch_index') or 0)])
    def sort_key(candidate):
        return hashlib.sha256(f'authorial-order|{variation_material}|visual-concepts|{canonical(candidate)}'.encode()).hexdigest()
    assert sorted(av, key=sort_key) == av
    prediction = copy.deepcopy(av)
    after_by_id = {c['id']: c for c in bv}
    for c in prediction:
        if c['id'] in TARGETS:
            c['opt_in_contract']['obligation']['reject_substitutes'] = after_by_id[c['id']]['opt_in_contract']['obligation']['reject_substitutes']
    prediction.sort(key=sort_key)
    assert prediction == bv
    non_target_order_same = [c['id'] for c in av if c['id'] not in TARGETS] == [c['id'] for c in bv if c['id'] not in TARGETS]
    assert non_target_order_same
    assert a['creative_augmentation'] == b['creative_augmentation']
    assert a['slots'] == b['slots']
    assert a['semantic_clarification'] == b['semantic_clarification']
    assert a['semantic_assertion_obligations'] == b['semantic_assertion_obligations']
    assert a['authorial_core'] == b['authorial_core']
    assert 'visual_obligations' not in a and 'visual_obligations' not in b
    cases.append({'case': case, 'before_path': str(bp), 'after_path': str(ap), 'before_sha256': digest(bp), 'after_sha256': digest(ap),
                  'before_pack_id': a['pack_id'], 'after_pack_id': b['pack_id'], 'raw_delta_count': len(raw), 'id_aligned_delta_count': len(by_id),
                  'all_id_memberships_preserved': True, 'all_id_list_order_preserved': not order_changes, 'order_changes': order_changes,
                  'non_lobe_visual_relative_order_preserved': non_target_order_same, 'shuffle_reproduction': {'variation_material': variation_material, 'before_order_reproduced': True, 'only_reject_strings_changed_then_sorted_equals_actual_after': True},
                  'all_slots_exact': True, 'creative_augmentation_exact': True, 'semantic_clarification_exact': True, 'requester_assertions_exact': True, 'frozen_core_exact': True,
                  'visual_profile_components_requirements_gates_unchanged_by_id': True, 'active_visual_obligations_section_present': False,
                  'before_surfaces': surface_inventory(before), 'after_surfaces': surface_inventory(after)})
    all_deltas[case] = {'exact_positional_delta': raw, 'id_aligned_delta': by_id}

actual_before, actual_after = BASE / 'actual-v22-before/pack.json', BASE / 'actual-lobe-after-boundary/pack.json'
official = BEFORE_REPO / 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v22_pack.json'
assert actual_before.read_bytes() == official.read_bytes()
actual_delta = list(differences(read(actual_before), read(actual_after)))
assert {v['path'] for v in actual_delta} == {'/0/pack_id', '/0/provenance/tags_hash'}
assert sorted(actual_delta, key=lambda v: v['path']) == sorted(read(BASE / 'actual-lobe-after-boundary/PACK-DELTA.json'), key=lambda v: v['path'])

summary = {'assessment': 'Narrow semantic boundary correction supported; exact order-invariance hypothesis fails for three natural cases. No adoption, final audit or image claim.',
           'strict_requested_order_invariance_pass': False, 'all_candidate_id_memberships_preserved': True, 'unplanned_id_aligned_content_changes': [],
           'candidate_seal_sha256': digest(seal_path), 'all_20_sealed_files_match': True, 'before_review_preserved': True,
           'before_review_manifest_sha256': digest(before_manifest), 'source_changed_leaves': len(source_delta), 'source_delta_matches_documented_proposal': True,
           'runtime_file_byte_identical': True, 'runtime_file_sha256': digest(AFTER_REPO / runtime_rel), 'cases': cases,
           'actual_frozen_case': {'before_equals_official_v22_bytes': True, 'before_sha256': digest(actual_before), 'after_sha256': digest(actual_after), 'delta': actual_delta},
           'retained_limitations': ['Wrong-count optional exposure in actual lobed openings', 'Both aperture meanings offered for explicitly painted solid door', 'No claim of a blind after review or domain-blind cohort', 'No composed adoption/final audit/image evidence', 'Presentation changes might affect downstream author choices; this was not measured']}
write('summary.json', summary)
write('all-public-pack-deltas.json', all_deltas)
write('source-nine-leaf-delta.json', source_delta)
write('candidate-seal-verification.json', seal_checks)
write('index-binding-verification.json', index_checks)
print(json.dumps({'cases': [{'case': c['case'], 'raw_delta_count': c['raw_delta_count'], 'id_aligned_delta_count': c['id_aligned_delta_count'], 'all_id_list_order_preserved': c['all_id_list_order_preserved']} for c in cases], 'outcome': summary['assessment']}, indent=2))
