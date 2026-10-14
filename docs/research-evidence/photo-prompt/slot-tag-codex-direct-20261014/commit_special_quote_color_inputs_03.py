"""Verify and preserve prior special judgments and their fresh corrected inputs."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_semantic_evidence as native
import photo_candidate_corpus as c
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


paths = {Path(__file__).resolve(), HERE / 'prepare_special_quote_and_color_inputs_03.py'}
out = HERE / 'native-inputs/08250-special-quote-color-plan-03'
paths.update(path for path in out.iterdir() if path.is_file())
reports = []
for name, expected in [
    ('review08250-11128-03', 'f0ae59a64657158cf749deca2f833e2f53fe1322f61fea461c0012c2745ccc7a'),
    ('review08250-17437-02', '733107735d247ad5700c0a7dfe13660fec2f1dd1bfc1d29e153b531d7ea5ed46')]:
    directory = HERE / 'native_batches' / name
    batch = reviews.read_json(directory / 'BATCH.json')
    assert c.digest(batch) == expected
    result = reviews.verify_batch(str((HERE / 'native-inputs/prepared' / name / 'ASSIGNMENT.json').relative_to(ROOT)),
        str((directory / 'BATCH.json').relative_to(ROOT)), str((directory / 'NOTE.json').relative_to(ROOT)))
    reports.append({key: value for key, value in result.items() if key != 'records'})
    paths.update(directory / name for name in ['BATCH.json', 'NOTE.json'])
for name in ['review08250-11128-04', 'review08250-17437-03']:
    paths.update(path for path in (HERE / 'native-inputs/prepared' / name).iterdir() if path.is_file())
for name in [
    'authored/native_fresh_08250_11128_03.py',
    'authored/native_fresh_08250_11128_03_checks.py',
    'authored/native_fresh_08250_11128_03_checks.json',
    'authored/native_fresh_08250_17437_02.py',
    'authored/native_fresh_08250_17437_02_checks.json',
    'authored/native_fresh_08250_17437_02_read.py',
    'authored/native_fresh_08250_17437_02_read_cache.json',
    'authored/native_resolution_08250_17437_144v4_source_proposal_01.json',
    'authored/native_resolution_08250_17437_144v4_source_proposal_02.json',
    'worker-notes/native-fresh-08250-11128-03.json',
    'worker-notes/native-fresh-08250-17437-02.json',
    'worker-notes/native-fresh-08250-17437-02-color-reassessment.json']:
    paths.add(HERE / name)
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve(); assert path.is_relative_to(GEN)
        modules[name] = {'file': str(path), 'sha256': raw(path)}
report_path = HERE / 'ROOT-SPECIAL-QUOTE-COLOR-INPUTS-03-VERIFICATION.json'
save(report_path, {
    'schema': 'photo-root-special-corrected-source-inputs/v1', 'actor': '/root',
    'prior_exact_batches_shape_valid': reports, 'frozen_code_generation': GEN.name,
    'used_frozen_modules': modules,
    '11128_root_whole_source_and_71facts_26units_read': True,
    '11128_root_semantic_reopen': 'Common Korean pose quote omitted natural although natural_standing/natural_walking was the typed E. A same-pointer quote cannot borrow the English or selected branch qualifier. Source English/concept/relation/branch Korean already support natural; explicit corrected common Korean is selected for fresh04 input.',
    '11128_03_accepted_by_root': False,
    '17437_02_worker_status': 'pending', '17437_02_proof': None,
    '17437_root_source_selection': 'Proposal02 exact six effect address replacements were fully enumerated against whole before/current and no other source field differs. One visible cheek-color proposition remains one E. Proposal01 duplicate state/color suggestion was withdrawn and is preserved as history.',
    '17437_previous3555facts_personally_all_read_or_approved_by_root': False,
    '17437_new_atomic_owned_parts_and_complete18choices_still_require_fresh_review': True,
    'fresh_preparation_verification': {'file': str((out / 'ROOT-PREPARATION-VERIFICATION.json').relative_to(ROOT)), 'file_sha256': raw(out / 'ROOT-PREPARATION-VERIFICATION.json')},
    'prepared_count': 2, 'fresh_actual_read_count': 0, 'new_native_approvals': 0,
    'canonical_or_binding_changes': False, 'operational_native_qualified_records': 0,
    'os_network_denied': True, 'provider_keys_removed': True, 'gemini_calls': 0,
    'local_inference_inputs': 0, 'stage05_complete': False, 'stages06_08_complete': False})
paths.add(report_path)
for path in paths:
    if path.suffix == '.json': json.loads(path.read_bytes())
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
allowlist_path = HERE / 'ROOT-SPECIAL-QUOTE-COLOR-INPUTS-03-COMMIT-ALLOWLIST.json'
save(allowlist_path, {
    'schema': 'photo-root-research-exact-commit-allowlist/v1',
    'files': sorted(str(path.relative_to(ROOT)) for path in paths | {allowlist_path}),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded_to_avoid_cycle': True, 'new_native_approvals': 0,
    'canonical_or_binding_changes': False, 'operational_native_qualified_records': 0,
    'gemini_calls': 0, 'stage05_complete': False})
paths.add(allowlist_path)
names = sorted(str(path.relative_to(ROOT)) for path in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
check = subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged == set(names)
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes()
print(json.dumps({'staged_files': len(paths), 'old_batch_shape_checks': 2,
    'new_prepared': ['review08250-11128-04', 'review08250-17437-03'],
    'source_correction_approvals_are_input_only': True, 'native_approvals': 0,
    'cached_check': 'pass'}))
