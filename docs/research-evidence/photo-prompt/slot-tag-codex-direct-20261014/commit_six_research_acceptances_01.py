"""Preserve exact six root-reviewed research acceptances, no operational writes."""
from __future__ import annotations
import ast
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def raw(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def save(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT)
paths = {Path(__file__).resolve()}
for directory in [
    'native_batches/review11870-01257-05',
    'native_batches/review11870-01285-05',
    'native_batches/review11870-01285-06',
    'native_batches/review06250-01236-06',
    'native_batches/review06250-00259-06',
    'native_batches/review06250-00807-06',
    'native_batches/review06250-00924-06',
    'native-inputs/partner-chair-quote-recheck-plan-08',
    'native-inputs/prepared/review11870-01285-06',
]:
    paths.update(p for p in (HERE / directory).iterdir() if p.is_file())
for name in [
    'root_accept_bare_props_06.py', 'ROOT-BARE-PROP-RESEARCH-ACCEPTANCE-06.json',
    'root_accept_partner_chair_06.py', 'root_accept_partner_chair_06_02.py',
    'prepare_partner_chair_quote_recheck_08.py',
    'authored/native_06250_C4_formal06.write.py',
    'authored/native_06250_C4_formal06.check.py',
    'worker-notes/native-06250-C4-formal06-final-20261015.json',
    'worker-notes/native-06250-C4-formal06-diagnostic-20261015.json',
]:
    paths.add(HERE / name)
weather = read(HERE / 'native_batches/review11870-01257-05/ROOT-VERIFICATION-02.json')
chair = read(HERE / 'native_batches/review11870-01285-06/ROOT-VERIFICATION-02.json')
assert chair['supersedes_unpinned_verification_01']
assert chair['all_five_effects_owners_guards_and_receivers_unchanged']
assert chair['used_frozen_modules']['photo_semantic_evidence']['raw_sha256'] == '6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
prop_report = read(HERE / 'ROOT-BARE-PROP-RESEARCH-ACCEPTANCE-06.json')
assert len(prop_report['accepted_research_records']) == 4
acceptances = [HERE / 'native_batches/review11870-01257-05/ROOT-ACCEPTANCE.json',
    HERE / 'native_batches/review11870-01285-06/ROOT-ACCEPTANCE-02.json']
acceptances += [ROOT / row['acceptance']['file'] for row in prop_report['accepted_research_records']]
assert len(acceptances) == 6 and all(read(p)['actor'] == '/root' for p in acceptances)
report = HERE / 'ROOT-SIX-RESEARCH-ACCEPTANCES-01.json'
save(report, {'schema': 'photo-root-six-research-acceptances/v1', 'actor': '/root',
    'accepted_research_records': 6, 'actual_facts': 30, 'actual_source_units': 24,
    'acceptances': [{'file': str(p.relative_to(ROOT)), 'file_sha256': raw(p)} for p in acceptances],
    'root_direct_read_boundary': 'Exact six complete original/current/selected application/old5B/own binding/closure, actual facts/units/owners/guards/effects/roles and relevant whole specs reviewed. Retained15 chair facts reused by exact equality from root direct05 read. No all-corpus or all-first50 claim.',
    'root_actual_consumer_execution': {'weather_full_compact_admission_cases': 8, 'weather_old_binding_consumers': 8, 'weather_whole_locks': 4, 'props_and_chair_consumers': 'Worker evidence reviewed; not rerun or claimed as root tests.'},
    'root_batch_and_acceptance_integrity_checks': 6,
    'chair_first_root_engine_boundary_correction': 'native_batches/review11870-01285-06/ROOT-ENGINE-BOUNDARY-CORRECTION-01.json',
    'latest_chair_frozen_engine_verification': 'native_batches/review11870-01285-06/ROOT-VERIFICATION-02.json',
    'prior_failed_runs_and_original05_chair_proof_preserved': True,
    'operating_source_catalog_bindings_qualification_runtime_changed': False,
    'native_operating_qualified_records': 0, 'Gemini_calls': 0, 'stages05_08_complete': False})
paths.update({report, ROOT / 'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'})
for path in paths:
    assert path.is_file() and not path.is_symlink(), path
    if path.suffix == '.py': ast.parse(path.read_bytes(), filename=str(path))
    if path.suffix == '.json': read(path)
names = sorted(str(p.relative_to(ROOT)) for p in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
allow = HERE / 'ROOT-SIX-RESEARCH-ACCEPTANCES-01-COMMIT-ALLOWLIST.json'
save(allow, {'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(names + [str(allow.relative_to(ROOT))]),
    'file_byte_hashes': {str(p.relative_to(ROOT)): raw(p) for p in sorted(paths)},
    'self_hash_excluded': True, 'research_acceptances': 6, 'operating_qualified': 0})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()) <= {str(p.relative_to(ROOT)) for p in paths}
for path in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(path.relative_to(ROOT))], cwd=ROOT) == path.read_bytes()
print(json.dumps({'verified_files': len(paths), 'research_acceptances': 6, 'operating_qualified': 0}))
