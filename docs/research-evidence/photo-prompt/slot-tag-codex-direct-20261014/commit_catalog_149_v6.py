"""Commit the exact manually selected149 research catalog and bounded audits."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def raw(p): return hashlib.sha256(p.read_bytes()).hexdigest()


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
paths = {Path(__file__).resolve()}
for prefix in ['native_12250_taxonomy_mechanics_articulation_relational_20261015', 'native_12250_taxonomy_mass_20261015', 'native_12250_catalog149_v6_proposal_20261015']:
    paths.update(p for p in (HERE / 'authored').glob(prefix + '*') if p.is_file())
for name in ['worker-notes/native-12250-taxonomy-mechanics-articulation-relational-20261015.json',
    'worker-notes/native-12250-taxonomy-mass-20261015.json',
    'worker-notes/native_12250_catalog149_v6_proposal_20261015.json',
    'CATALOG-FINAL-149-V6.json', 'CATALOG-FINAL-149-V6-REVIEW.json',
    'CATALOG-FINAL-149-V6-ACCEPTANCE.json', 'NATIVE-CATALOG-APPROVAL-149-V6.json',
    'ROOT-FINAL-CATALOG-149-V6-VERIFICATION.json', 'finalize_catalog_149_v6.py']:
    paths.add(HERE / name)
paths.add(ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md')
report = json.loads((HERE / 'ROOT-FINAL-CATALOG-149-V6-VERIFICATION.json').read_bytes())
assert report['whole18250_container_integrity'] == 'pass' and report['all149_spec_schema_dimensions_neighbor_refs'] == 'pass'
assert report['unchanged145_existing_from146_exact'] and report['relational_action_unchanged']
assert report['catalog']['sha256'] == 'd9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
for p in paths:
    assert p.is_file() and not p.is_symlink()
    if p.suffix == '.py': ast.parse(p.read_bytes(), filename=str(p))
    if p.suffix == '.json': json.loads(p.read_bytes())
names = sorted(str(p.relative_to(ROOT)) for p in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
allow = HERE / 'ROOT-CATALOG-149-V6-COMMIT-ALLOWLIST.json'
with allow.open('x') as stream:
    json.dump({'schema': 'photo-root-exact-commit-allowlist/v1',
        'files': sorted(names + [str(allow.relative_to(ROOT))]),
        'file_byte_hashes': {str(p.relative_to(ROOT)): raw(p) for p in sorted(paths)},
        'self_hash_excluded': True, 'operating_changes': 0, 'new_candidate_approvals': 0}, stream, indent=2, sort_keys=True)
    stream.write('\n')
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()) <= {str(p.relative_to(ROOT)) for p in paths}
for p in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(p.relative_to(ROOT))], cwd=ROOT) == p.read_bytes()
print(json.dumps({'verified_files': len(paths), 'research_catalog': 149, 'operating_catalog': 139, 'new_candidate_approvals': 0}))
