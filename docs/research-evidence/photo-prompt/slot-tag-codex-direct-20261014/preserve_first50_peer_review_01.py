"""Preserve first50 peer findings and explicit root holds without approval."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def raw(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path): return json.loads(path.read_bytes())


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
note_path = HERE / 'worker-notes/native-08250-first50-04-independent-20261015.json'
assert raw(note_path) == '4af1111478d44d0d6e180eb43c662d42e2fba38a259e1ebdd9b2531f8d785b55'
note = read(note_path)
assert note['mechanical_validation']['whole_full_validate_and_compact_pass'] == 45
assert note['mechanical_validation']['all26_expected']
folder = HERE / 'native_batches/review11870-01250-01300-04'
assert raw(folder / 'BATCH.json') == 'e129dd8657930fb90d017aeaa3ad26935aa6441de8065b614aea0f3496cc1d6a'
report = folder / 'ROOT-SEMANTIC-REOPEN-01.json'
save(report, {'schema': 'photo-root-first50-peer-review-reopen/v1', 'actor': '/root',
    'batch_sha256': '4d55aef65775e0dc7f85e3446196195be8875b6700c590f3e5894620b0259c94',
    'peer_note': {'file': str(note_path.relative_to(ROOT)), 'raw_sha256': raw(note_path)},
    'peer_whole50_original_current_5B_binding_closure_read': True,
    'root_whole50_read_claim': False,
    'root_read_boundary': 'Root reviewed whole peer report conclusions and selected detailed precision cases; actual single1257/1264/1267/1285 sources/proofs were handled separately. Peer full437 facts/174units review is not root whole50 source reading.',
    'root_batch_acceptance': False, 'operating_qualification': 0,
    'quote_holds': {
        '1262': 'Announcing with raised gavel does not independently state holding; use exact full Korean/application holding anchor and explicit partial English reference. Announcement alone is not gavel-directed relational interaction.',
        '1271': 'Korean polaroid group does not independently establish stacked arrangement. Exact English/application remain direct and whole effects must remain.',
        '1298': 'Korean disguised prop does not independently state complete cover-identity purpose. Exact English/application retain direct support.'},
    'clarifications_to_preserve': {'1253': 'Counter distance physical application versus short standalone quote.', '1255': 'Own side means proximity to self; do not invent lateral geometry.'},
    'technical_holds': {
        'generic_same_fact_relational_role_views': [1255, 1258, 1262, 1266, 1271, 1275, 1296],
        '1271_handheld_contact': 'Actual contact facet, no implicit new contact E.',
        '1278_anatomical_connection': 'Actual same-actor face/hand part_of guard needs fresh guarded role proof, no category-to-anatomy inference.',
        '1286_apparatus_pov': 'Actual identified mirror view may use a same-fact view; no fake camera property/effect.',
        '1299': 'Actual variable existing-hand/member structure awaits source interpretation and scoped consumer proof.'},
    'canonical_note_wrapper_boundary': 'Exact schema wrapper repairs the note envelope only. It adds no source read, semantic correction, proof/status or root approval.',
    'worker45_approved5_pending_statuses_preserved': True,
    'earlier_worker_and_peer_failed_runs_preserved': True,
    'source_catalog_bindings_runtime_changed': False, 'Gemini_calls': 0})
paths = {Path(__file__).resolve(), report}
paths.update(p for p in folder.iterdir() if p.is_file())
paths.update(p for p in (HERE / 'worker-notes').glob('native-08250-first50-04-independent-20261015.*') if p.is_file())
for p in paths:
    assert p.is_file() and not p.is_symlink()
    if p.suffix == '.py': ast.parse(p.read_bytes(), filename=str(p))
    if p.suffix == '.json': read(p)
names = sorted(str(p.relative_to(ROOT)) for p in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
allow = HERE / 'ROOT-FIRST50-PEER-REVIEW-01-COMMIT-ALLOWLIST.json'
save(allow, {'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(names + [str(allow.relative_to(ROOT))]),
    'file_byte_hashes': {str(p.relative_to(ROOT)): raw(p) for p in sorted(paths)},
    'self_hash_excluded': True, 'root_batch_acceptances': 0, 'native_operating_qualified': 0})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()) <= {str(p.relative_to(ROOT)) for p in paths}
for p in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(p.relative_to(ROOT))], cwd=ROOT) == p.read_bytes()
print(json.dumps({'verified_files': len(paths), 'root_batch_acceptances': 0}))
