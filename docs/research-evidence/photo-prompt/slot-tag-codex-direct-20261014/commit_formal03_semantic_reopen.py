"""Preserve an exact completed research batch and explicit semantic objections.

No subset of its worker positives is accepted. Historical proofs stay intact;
future inputs must address the separately authored source/quote corrections.
"""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BATCH = HERE / 'native_batches/review11870-01250-01300-03'


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': raw(path)}


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


batch = read(BATCH / 'BATCH.json')
assert raw(BATCH / 'BATCH.json') == '9124a53c724f485ad29bf3509d64cc3ad19dc117397bb66dc08fc77042418e65'
assert raw(BATCH / 'NOTE.json') == '9b828f53a01d450ea266a50fc513d7e113cec30238e7704b67b1d4daede89483'
peer_path = HERE / 'worker-notes/native-07250-first50-formal03-independent-20261015.json'
assert raw(peer_path) == 'add883b54b566877ff4883ddf7c5bea6f1d0c74d1be90ae30057424dfe7cb22f'
peer = read(peer_path)
assert peer['scope']['actual_unique_root_sources_read'] == 50
assert peer['scope']['full_proofs_read'] == 33
assert peer['scope']['individual_fact_rows_read'] == 265
shape = read(BATCH / 'ROOT-VERIFICATION-01.json')
assert shape['shape_valid'] and shape['statuses'] == {'approved': 33, 'pending': 17, 'diagnostic_reviewed': 0}
assert shape['facts_checked'] == 265 and shape['source_units_checked'] == 115
assert peer['conclusion']['approved_rows_with_independent_quote_or_inventory_objections'] == [1250, 1251, 1289, 1290]
assert len(batch['records']) == 50
reopen_path = BATCH / 'ROOT-SEMANTIC-REOPEN-01.json'
save(reopen_path, {
    'schema': 'photo-root-native-semantic-reopen/v1', 'actor': '/root',
    'batch': ref(BATCH / 'BATCH.json'), 'note': ref(BATCH / 'NOTE.json'),
    'pure_shape_verification': ref(BATCH / 'ROOT-VERIFICATION-01.json'),
    'independent_direct_semantic_review': ref(peer_path),
    'root_direct_read_scope': {
        'all_fifty_independent_semantic_judgements_and_objections_read': True,
        'complete_three_sources_facts_and_units_reread_for_quote_objections': [1250, 1251, 1289],
        'complete_1290_original_current_ambient_thermal_proposal_and_own_binding_read': True,
        'all33_full_proofs_personally_read_or_approved_by_root': False},
    'worker_statuses_preserved': shape['statuses'],
    'root_acceptance_written': False, 'root_accepted_records': 0,
    'root_supported_reopen_ordinals': [1250, 1251, 1289, 1290],
    'reasons': {
        '1250': 'A fleeting/caught typed expression needs its own full positive Korean/application quote. Root selects explicit whole-source-preserving clarifications for a new input; the old fact remains historical.',
        '1251': 'Quote extentKo must include the existing complete face-filling Korean field. No source change is needed; the old short quote is not full support.',
        '1289': 'Inside is explicit in original phrase fields but absent in three individually cited fields. Root selects corresponding label/application clarification from that existing interior meaning; no cross-pointer borrowing.',
        '1290': 'Sticky tropical heat expressly includes qualitative ambient physical heat on the existing scene. Weather-only E cannot substitute for a material thermal.state effect or complete applicable-role inventory. Root has read the separate minimal ambient-thermal source proposal.'},
    'source_quote_clarifications': ref(HERE / 'authored/root_quote_local_source_clarifications_v1.json'),
    'remaining_seventeen_pending_preserved': True,
    'next': 'Prepare a new exact source input only after all chosen whole source/guard corrections are manually settled. Require actual whole rereads, exact local quote support and consumer controls; never auto-resign or accept a subset of this batch.',
    'canonical_source_binding_or_catalog_changed': False,
    'operational_native_qualified_records': 0, 'provider_or_embedding_network_calls': 0,
    'gemini_calls': 0, 'stage05_complete': False, 'stages06_08_complete': False})
paths = {path for path in BATCH.iterdir() if path.is_file()}
paths.update((HERE / 'authored').glob('native_11870_formal03_*.py'))
paths.update((HERE / 'authored').glob('native_11870_formal03_*.json'))
paths.update((HERE / 'worker-notes').glob('native-11870-formal03-*.json'))
paths.update((HERE / 'worker-notes').glob('native-07250-first50-formal03-independent-20261015.*'))
paths.update(HERE / name for name in [Path(__file__).name,
    'authored/root_quote_local_source_clarifications_v1.py',
    'authored/root_quote_local_source_clarifications_v1.json'])
paths.add(ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md')
completion = read(HERE / 'worker-notes/native-11870-formal03-first50-complete-v1.json')
for checkpoint in completion['immutable_checkpoints']:
    for key in ['checkpoint', 'worker_note']:
        item = checkpoint[key]
        assert raw(ROOT / item['file']) == item['file_sha256']
        assert ROOT / item['file'] in paths
for path in paths:
    if path.suffix == '.json': read(path)
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
allowlist_path = HERE / 'ROOT-FORMAL03-SEMANTIC-REOPEN-COMMIT-ALLOWLIST.json'
save(allowlist_path, {
    'schema': 'photo-root-research-exact-commit-allowlist/v1',
    'files': sorted(str(path.relative_to(ROOT)) for path in paths | {allowlist_path}),
    'file_byte_hashes': {str(path.relative_to(ROOT)): raw(path) for path in sorted(paths)},
    'self_hash_excluded_to_avoid_cycle': True,
    'purpose': 'Preserve worker research, exact failed/iterated controls, independent objections and explicit root reopen. No operating approval.',
    'worker_positive_count': 33, 'worker_pending_count': 17,
    'root_accepted_records': 0, 'source_quote_input_proposals_only': True,
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
print(json.dumps({'staged_files': len(paths), 'shape': '33 positive/17 pending,265facts/115units',
    'independent_reopens': [1250, 1251, 1289, 1290], 'root_accepted_records': 0,
    'cached_check': 'pass', 'operational_qualified_records': 0}))
