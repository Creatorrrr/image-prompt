"""Transfer this conversation's reviewed scope to a clean publication checkout."""
import copy
import hashlib
import json
import pathlib
import shutil
import sys

PRIMARY = pathlib.Path('/Users/chasoik/Projects/image-prompt')
TARGET = pathlib.Path(sys.argv[1]).resolve()
PUBLICATION = pathlib.Path(__file__).resolve().parent
REL_PUBLICATION = PUBLICATION.relative_to(PRIMARY)
OUT = TARGET / REL_PUBLICATION
OUT.mkdir(parents=True, exist_ok=True)
ASSETS = pathlib.Path('skills/photo-prompt-image-generator/assets')
REFINEMENT = PRIMARY / 'docs/research-evidence/photo-prompt/wardrobe-keyword-refinement-20261010'
RECORDS = pathlib.Path('docs/research-evidence/photo-prompt/extension-maintenance')


def load(path):
    return json.loads(path.read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


copied, excluded = [], []


def transfer(rel):
    source, target = PRIMARY / rel, TARGET / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    copied.append(str(rel))


exact_paths = [
    'skills/photo-prompt-image-generator/SKILL.md',
    'skills/photo-prompt-image-generator/references/embodiment-preflight.md',
    'skills/photo-prompt-image-generator/references/image-runtime.md',
    'skills/photo-prompt-image-generator/scripts/photo_workflow.py',
    str(ASSETS / 'photo_prompt_wardrobe_owner_relations_extension.json'),
    str(ASSETS / 'photo_prompt_visual_obligations_wardrobe_owner_relations.json'),
    'tests/test_photo_wardrobe_owner_relations.py',
    'tests/test_photo_native_independent_manifest.py',
]
hashes = {row['path']: row['current_sha256'] for row in load(REFINEMENT / 'SOURCE-DELIVERY.json')['files']}
for rel in exact_paths:
    assert hashlib.sha256((PRIMARY / rel).read_bytes()).hexdigest() == hashes[rel]
    transfer(pathlib.Path(rel))

# Keep the published clothing rows and apply only the two owned effect deltas.
clothing_name = 'photo_prompt_clothing_structure_extension.json'
profiles_name = 'photo_prompt_visual_obligations_clothing_structure.json'
before_clothing = load(TARGET / ASSETS / clothing_name)
before_profiles = load(TARGET / ASSETS / profiles_name)
clothing, profiles = copy.deepcopy(before_clothing), copy.deepcopy(before_profiles)
local_clothing = load(PRIMARY / ASSETS / clothing_name)
local_profiles = load(PRIMARY / ASSETS / profiles_name)
local_candidates = {row['id']: row for rows in local_clothing['slots'].values() for row in rows}
local_profile_map = {row['id']: row for row in local_profiles['profiles']}
candidate_ids = {'clt_ct037_v1', 'clt_ct047_v1'}
profile_ids = {'clothing_ct037_v1', 'clothing_ct047_v1'}
for rows in clothing['slots'].values():
    for row in rows:
        if row['id'] in candidate_ids:
            for field in ['affected_dimensions', 'affected_properties']:
                row[field] = copy.deepcopy(local_candidates[row['id']][field])
for row in profiles['profiles']:
    if row['id'] in profile_ids:
        for field in ['affected_dimensions', 'affected_properties']:
            row['concept_candidate'][field] = copy.deepcopy(local_profile_map[row['id']]['concept_candidate'][field])

prior_ref = clothing.pop('maintenance_ref')
record_id = 'clothing-retained-wardrobe-effects-publication-20261010-v1'
record = {
    'schema_version': 'photo-extension-maintenance/v1', 'record_id': record_id,
    'maintenance_only': True, 'source_filename': clothing_name,
    'profile_filename': profiles_name, 'prior_maintenance_ref': prior_ref,
    'historical_refinement_record_id': 'clothing-retained-wardrobe-effects-20261010',
    'candidate_ids': sorted(candidate_ids), 'profile_ids': sorted(profile_ids),
    'authored_source_sha256': digest(clothing), 'profile_source_sha256': digest(profiles),
    'preserved_published_candidate_source_sha256': digest({k: v for k, v in before_clothing.items() if k != 'maintenance_ref'}),
    'preserved_published_profile_source_sha256': digest(before_profiles),
    'research_sources': ['WK024', 'WK029'],
    'reason': 'Preserve published clothing meaning and add only retained same-owner cowl drape and bishop sleeve/cuff effects. Unrelated primary changes are not publication inputs.'
}
clothing['maintenance_ref'] = {'contract_version': 'photo-extension-maintenance-ref/v1', 'record_id': record_id, 'sha256': digest(record)}
write(TARGET / RECORDS / (record_id + '.json'), record)
write(TARGET / ASSETS / clothing_name, clothing)
write(TARGET / ASSETS / profiles_name, profiles)
before_candidates = {row['id']: row for rows in before_clothing['slots'].values() for row in rows}
after_candidates = {row['id']: row for rows in clothing['slots'].values() for row in rows}
before_profile_map = {row['id']: row for row in before_profiles['profiles']}
after_profile_map = {row['id']: row for row in profiles['profiles']}
assert set(before_candidates) == set(after_candidates)
assert set(before_profile_map) == set(after_profile_map)
assert all(after_candidates[key] == row for key, row in before_candidates.items() if key not in candidate_ids)
assert all(after_profile_map[key] == row for key, row in before_profile_map.items() if key not in profile_ids)
assert all(after_profile_map[key]['activation'] == row['activation'] and after_profile_map[key]['authored_components'] == row['authored_components'] for key, row in before_profile_map.items())

manifest_path = TARGET / ASSETS / 'photo_prompt_source_manifest.json'
manifest = load(manifest_path)
original_registrations = copy.deepcopy(manifest['sources'])
local_manifest = load(PRIMARY / ASSETS / manifest_path.name)
new_names = {'photo_prompt_wardrobe_owner_relations_extension.json', 'photo_prompt_visual_obligations_wardrobe_owner_relations.json'}
registrations = [row for row in local_manifest['sources'] if row['file'] in new_names]
assert len(registrations) == 2
assert not new_names & {row['file'] for row in manifest['sources']}
for row in registrations:
    row['load_order'] = sum(old['kind'] == row['kind'] for old in manifest['sources'])
    assert {old['load_order'] for old in manifest['sources'] if old['kind'] == row['kind']} == set(range(row['load_order']))
    manifest['sources'].append(copy.deepcopy(row))
assert manifest['sources'][:len(original_registrations)] == original_registrations
write(manifest_path, manifest)

for record_path in sorted((PRIMARY / RECORDS).glob('*wardrobe*20261010*.json')):
    transfer(record_path.relative_to(PRIMARY))

evidence_names = ['wardrobe-keyword-semantics-20261010', 'wardrobe-keyword-integration-20261010', 'wardrobe-keyword-refinement-20261010']
for name in evidence_names:
    directory = PRIMARY / 'docs/research-evidence/photo-prompt' / name
    for source in sorted(directory.rglob('*')):
        if not source.is_file():
            continue
        rel = source.relative_to(PRIMARY)
        inner = source.relative_to(directory)
        reason = None
        if any(part in {'__pycache__', '.git', '.venv', 'runtime_store', 'runtime-store', 'publication-runtime-store'} for part in inner.parts):
            reason = 'private runtime/cache/environment'
        elif source.name.endswith('.LOCK') or source.name == '.LOCK':
            reason = 'process lock'
        elif inner.parts[0] in {'management-report', 'management-report-v2'}:
            reason = 'large regenerable global management dump; retained in primary'
        if reason:
            excluded.append({'path': str(rel), 'reason': reason, 'bytes': source.stat().st_size})
        else:
            transfer(rel)

for rel in [REL_PUBLICATION / 'prepare_scope.py', REL_PUBLICATION / 'PRIMARY-BEFORE.json']:
    transfer(rel)
preservation = {
    'status': 'PASS', 'published_registration_count_preserved': len(original_registrations),
    'added_registrations': registrations, 'candidate_ids_preserved': len(before_candidates),
    'profile_ids_preserved': len(before_profile_map), 'all_existing_clothing_activation_and_components_exact': True,
    'only_changed_candidate_effect_rows': sorted(candidate_ids), 'only_changed_profile_effect_rows': sorted(profile_ids),
    'unrelated_ct073_published_row_preserved': after_profile_map['clothing_ct073_v2'] == before_profile_map['clothing_ct073_v2'],
    'wardrobe_extension_and_profiles_byte_exact_to_completed_task': True,
    'new_published_clothing_maintenance_record': record_id,
    'historical_refinement_records_not_rewritten': True
}
write(OUT / 'AUTHORED-PRESERVATION.json', preservation)
plan = {'schema_version': 'wardrobe-publication-reviewed-scope/v1', 'copied_paths': copied,
        'authored_modified_paths': [str(ASSETS / name) for name in [clothing_name, profiles_name, manifest_path.name]],
        'new_maintenance_path': str(RECORDS / (record_id + '.json')), 'excluded_local_only': excluded,
        'generated_indexes': 'rebuild from this scoped source; never copy wholesale primary indexes',
        'unrelated_primary_dirty_files': 'preserved in place', 'image_qualification': 'historical 1/3; not promoted by publication'}
write(OUT / 'SCOPE.json', plan)
for name in ['AUTHORED-PRESERVATION.json', 'SCOPE.json']:
    shutil.copy2(OUT / name, PUBLICATION / name)
print(json.dumps({'status': 'PASS', 'copied_files': len(copied), 'excluded_files': len(excluded),
                  'excluded_bytes': sum(row['bytes'] for row in excluded), 'registered_sources': len(manifest['sources']),
                  'target': str(TARGET)}, ensure_ascii=False))
