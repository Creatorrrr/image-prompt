"""Finalize exact B2 stage; preserve byte-exact archival whitespace findings."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'member-B2-integration-01'


def raw(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p): return json.loads(p.read_bytes())


def save(p, value):
    with p.open('x') as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write('\n')


paths = {Path(__file__).resolve(), HERE / 'commit_member_B2_integration_01.py'}
handoff_path = HERE / 'worker-notes/native-member-B2-FINAL-02-handoff-02-20261015.json'
assert raw(handoff_path) == 'c709df3db8e1791ef7b1fa04d6823377863ab5cec2f63e89313d606071639f74'
for row in read(handoff_path)['changed_files']:
    p = ROOT / row['file']; assert raw(p) == row['raw_sha256']; paths.add(p)
for p in (HERE / 'worker-notes').glob('native-member-B2*'):
    if p.is_file(): paths.add(p)
    elif p.is_dir(): paths.update(x for x in p.rglob('*') if x.is_file())
for suffix in ['json', 'md']:
    paths.add(HERE / ('worker-notes/native-existing-member-scope-B2-release-plan-20261015.' + suffix))
paths.update(HERE / name for name in [
    'run_member_B2_root_integration_01.py', 'run_member_B2_root_integration_01.json', 'run_member_B2_root_integration_01.log',
    'run_member_B2_runtime_01.py', 'run_member_B2_runtime_01.log',
    'check_member_B2_discovery_boundary_01.py', 'ROOT-MEMBER-B2-DISCOVERY-BOUNDARY-01.json', 'ROOT-MEMBER-B2-INTEGRATION-01.json'])
paths.update(OUT / name for name in ['FROZEN-PRODUCTION-PINS.json', 'native-v4-runtime-01/PREFLIGHT.json',
    'native-v4-runtime-01/VERIFICATION.json', 'native-v4-runtime-01/build-cache/BUILD-REPORT.json'])
paths.update(ROOT / name for name in ['skills/photo-prompt-image-generator/references/maintenance.md',
    'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'])
allowed = {str(p.relative_to(ROOT)) for p in paths}
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines())
assert staged <= allowed and len(staged) == 121
report = read(HERE / 'ROOT-MEMBER-B2-INTEGRATION-01.json')
assert report['B2_engine_consumer_integration_complete'] and report['native_operating_qualified_records'] == 0
for name, sha in read(HERE / 'run_member_B2_root_integration_01.json')['after_hashes'].items(): assert raw(ROOT / name) == sha
patches = {name for name in allowed if name.endswith('.patch')}
first = subprocess.run(['git', 'diff', '--cached', '--check', '--', *sorted(staged - patches)], cwd=ROOT, capture_output=True, text=True)
assert first.returncode != 0
archive_bad = set(re.findall(r'^([^+].+?):\d+:', first.stdout, re.MULTILINE))
expected = {str((HERE / 'worker-notes' / name).relative_to(ROOT)) for name in [
    'native-member-B2-FINAL-02-bytes-20261015/skills/photo-prompt-image-generator/scripts/prompt_generator.py',
    'native-member-B2-before-20261015/skills/photo-prompt-image-generator/scripts/prompt_generator.py',
    'native-member-B2-development-transport-01/prompt_generator.py',
    'native-member-B2-root-closure-before-20261015/skills/photo-prompt-image-generator/scripts/prompt_generator.py',
    'native-member-B2-focused-01.log', 'native-member-B2-transport-01.log', 'native-member-B2-transport-02.log']}
assert archive_bad == expected, (archive_bad, expected)
failed = HERE / 'ROOT-MEMBER-B2-COMMIT-CHECK-FAILED-01.json'
save(failed, {'schema': 'photo-root-archival-commit-check-failure/v1', 'actor': '/root',
    'first_runner': 'commit_member_B2_integration_01.py', 'actual_cached_check_returncode': first.returncode,
    'actual_check_output': first.stdout,
    'resolution': 'Preserve all exact archived log/copy bytes and hashes. Exempt only these seven archive files plus archived patches. Recheck all production/tests/current docs and remaining evidence. No production source change, test repeat or runtime rebuild is needed for archival formatting.',
    'no_failed_functional_or_runtime_result_reclassified': True})
paths.add(failed)
for p in paths:
    assert p.is_file() and not p.is_symlink()
    if p.suffix == '.py': ast.parse(p.read_bytes(), filename=str(p))
    if p.suffix == '.json': read(p)
names = sorted(str(p.relative_to(ROOT)) for p in paths)
subprocess.run(['git', 'add', '--', *names], cwd=ROOT, check=True)
exempt = sorted(patches | archive_bad)
check = subprocess.run(['git', 'diff', '--cached', '--check', '--', *[name for name in names if name not in exempt]], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout
allow = HERE / 'ROOT-MEMBER-B2-INTEGRATION-01-COMMIT-ALLOWLIST.json'
save(allow, {'schema': 'photo-root-exact-commit-allowlist/v1',
    'files': sorted(names + [str(allow.relative_to(ROOT))]),
    'file_byte_hashes': {str(p.relative_to(ROOT)): raw(p) for p in sorted(paths)},
    'self_hash_excluded': True, 'exact_archival_whitespace_exempt': exempt,
    'archive_reason': 'Byte-identical original source copies keep inherited EOF spacing; failed unittest output retains actual trailing spaces; patches retain original context. Current production/tests are checked.',
    'nonarchival_cached_check_returncode': 0, 'new_inference_and_Gemini_calls': 0})
paths.add(allow)
subprocess.run(['git', 'add', '--', str(allow.relative_to(ROOT))], cwd=ROOT, check=True)
assert set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, text=True).splitlines()) <= {str(p.relative_to(ROOT)) for p in paths}
for p in paths:
    assert subprocess.check_output(['git', 'show', ':' + str(p.relative_to(ROOT))], cwd=ROOT) == p.read_bytes()
print(json.dumps({'verified_files': len(paths), 'production_and_test_checks': 'pass', 'published_generation': report['runtime']['actual_acquire']['generation_id']}))
