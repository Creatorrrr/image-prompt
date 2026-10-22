"""Read-only artifact verification; writes only the final evidence summary/index."""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path('/Users/chasoik/Projects/image-prompt')
EVIDENCE = Path(__file__).resolve().parent
RESEARCH = EVIDENCE.parent
MAINTENANCE = ROOT / 'generated/maintenance/medical-horror-20261022'


def read_json(path):
    return json.loads(Path(path).read_text())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


checks = []


def check(name, condition):
    checks.append({'name': name, 'status': 'pass' if condition else 'fail'})


reference = Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
reference_sha = digest(reference)
expected_skill = '7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35'
generation = '3ed7d4cd1bacbf4bea873116a5ff51b113e6f9ed5b983889d85f84933fd533b5'
check('current_skill_equals_all_tested_skill_bytes', digest(ROOT / 'skills/photo-prompt-image-generator/SKILL.md') == expected_skill)

reports = {'a': 'arm-a-report.md', 'b': 'REPORT.md', 'c': 'report.md'}
arms = []
external_artifacts = []
for arm in 'abc':
    run = ROOT / ('generated/photo-runs/medical-horror-20261022-arm-' + arm + '-image-v2')
    manifest = read_json(run / 'run_manifest.json')
    workflow = read_json(run / 'workflow.json')
    operations = workflow['operations']
    check(arm + '_official_review_phase', workflow['phase'] == 'review_record_validated')
    check(arm + '_one_complete_operation', len(operations) == 1 and operations[0]['status'] == 'complete' and len(operations[0]['attempts']) == 1)
    operation = operations[0]
    args = operation['record_args']
    ledger = ROOT / args[args.index('--ledger') + 1]
    rows = [json.loads(line) for line in ledger.read_text().splitlines() if line.strip()]
    check(arm + '_one_recorded_image_call', len(rows) == 1 and manifest['image_call_count'] == 1)
    check(arm + '_no_cross_arm_inputs_declared', manifest['cross_arm_inputs_used'] is False)
    check(arm + '_reference_and_skill_match', manifest['reference_sha256'] == [reference_sha] and manifest['skill_sha256'] == expected_skill)
    check(arm + '_actual_test_generation', workflow['h_f2_binding']['generation_id'] == generation)
    prompt = args[args.index('--prompt-en') + 1]
    prompt_path = run / 'final-prompt.txt'
    prompt_sha = hashlib.sha256(prompt.encode()).hexdigest()
    check(arm + '_final_prompt_equals_recorded_tool_prompt', prompt_path.read_text().rstrip('\n') == prompt and prompt_sha == manifest['runtime_prompt_sha256'])
    image_path = Path(manifest['image_paths'][0])
    image_bytes = image_path.read_bytes()
    image_sha = digest(image_path)
    check(arm + '_returned_image_hash', len(manifest['image_paths']) == 1 and image_sha == manifest['image_hashes'][0]['sha256'] == operation['result_binding']['sha256'])
    check(arm + '_nonempty_png', image_bytes[:8] == b'\x89PNG\r\n\x1a\n' and len(image_bytes) > 1000)
    width, height = struct.unpack('>II', image_bytes[16:24])
    report = run / reports[arm]
    check(arm + '_review_report_present', report.is_file() and report.stat().st_size > 500)
    arms.append({
        'arm': arm.upper(), 'run_path': str(run), 'phase': workflow['phase'],
        'image_call_count': manifest['image_call_count'], 'ledger_rows': len(rows),
        'image_path': str(image_path), 'image_sha256': image_sha, 'size': [width, height],
        'prompt_path': str(prompt_path), 'runtime_prompt_sha256': prompt_sha,
        'report_path': str(report), 'h_f2_generation': workflow['h_f2_binding']['generation_id'],
        'overall': 'PARTIAL', 'strict_whole_case': 'FAIL', 'user_acceptance': 'pending'
    })
    external_artifacts.extend([image_path, prompt_path, report, run / 'run_manifest.json', ledger, run / 'workflow.json'])

check('three_distinct_images', len({arm['image_sha256'] for arm in arms}) == 3)
check('three_distinct_prompts', len({arm['runtime_prompt_sha256'] for arm in arms}) == 3)

baseline = read_json(MAINTENANCE / 'before.json')
expected_changes = {
    'skills/photo-prompt-image-generator/retrieval-runtime.json',
    'skills/photo-prompt-image-generator/assets/photo_candidate_search.json'
}
protected_changes = []
missing = []
for name, before_sha in baseline['protected_hashes'].items():
    path = ROOT / name
    if not path.is_file():
        missing.append(name)
    elif digest(path) != before_sha:
        protected_changes.append(name)
unexpected = sorted(set(protected_changes) - expected_changes)
check('protected_files_preserved_except_expected_index_config', not missing and not unexpected)
drift_path = EVIDENCE / 'concurrent-source-drift.json'
documented_drift = read_json(drift_path) if drift_path.is_file() else {}
documented_rows = documented_drift.get('changed_protected_paths', [])
documented_hashes = {row['path']: row['closeout_observed_sha256'] for row in documented_rows}
drift_matches_record = set(unexpected) == set(documented_hashes) and all(digest(ROOT / name) == sha for name, sha in documented_hashes.items())
check('concurrent_drift_matches_explicit_observation', drift_matches_record)
current_baseline = read_json(EVIDENCE / 'CURRENT-preservation-baseline.json')
current_observed = {name: digest(name) for name in current_baseline}
check('global_CURRENT_unchanged', current_baseline == current_observed)
config = read_json(ROOT / 'skills/photo-prompt-image-generator/retrieval-runtime.json')
inclusion = read_json(EVIDENCE / 'default-data-inclusion.json')
check('default_config_still_matches_data_inclusion_proof', config == inclusion['default_config'])

historical = []
for line in (RESEARCH / 'SHA256SUMS').read_text().splitlines():
    sha, name = line.split(maxsplit=1)
    name = name.lstrip('*')
    historical.append({'path': name, 'pass': digest(RESEARCH / name) == sha})
check('historical_research_checksums_unchanged', all(x['pass'] for x in historical))

failed_checks = [x['name'] for x in checks if x['status'] == 'fail']
source_observation_checks = {
    'current_skill_equals_all_tested_skill_bytes',
    'protected_files_preserved_except_expected_index_config',
    'concurrent_drift_matches_explicit_observation',
    'default_config_still_matches_data_inclusion_proof'
}
artifact_failed_checks = [name for name in failed_checks if name not in source_observation_checks]
result = {
    'schema': 'medical-horror-completion-validation/v1',
    'status': 'pass' if not failed_checks else ('partial_source_integrity_unverified' if not artifact_failed_checks else 'fail'),
    'scope': 'Physical artifact closure and preservation. The protected-file equality failure is retained; it does not invalidate already sealed image artifacts or certify later changed working code. No status overrides PARTIAL image outcomes.',
    'failed_checks': failed_checks,
    'artifact_checks_pass': not artifact_failed_checks,
    'artifact_failed_checks': artifact_failed_checks,
    'later_working_skill_retested': False,
    'current_working_skill_sha256': digest(ROOT / 'skills/photo-prompt-image-generator/SKILL.md'),
    'documented_concurrent_source_drift': str(drift_path),
    'checks': checks, 'arms': arms, 'reference_sha256': reference_sha,
    'total_image_calls': sum(x['image_call_count'] for x in arms),
    'strict_cases_pass': 0, 'strict_cases_fail': 3,
    'protected_files': len(baseline['protected_hashes']), 'protected_changes': protected_changes,
    'missing_protected': missing, 'unexpected_protected_changes': unexpected,
    'historical_checksum_members': len(historical),
    'CURRENT_hashes': current_observed, 'default_config': config,
    'own_commit_push_operations': 0, 'own_CURRENT_writes': 0,
    'user_acceptance': 'pending'
}
write_json(EVIDENCE / 'completion-validation.json', result)

files = sorted(p for p in EVIDENCE.rglob('*') if p.is_file() and p.name != 'EVIDENCE-INDEX.json')
index = {
    'schema': 'medical-horror-evidence-index/v1',
    'scope': 'Hashes of final integration evidence plus primary image artifacts; not web-source body hashes.',
    'integration_files': [{'path': str(p), 'sha256': digest(p), 'bytes': p.stat().st_size} for p in files],
    'primary_image_artifacts': [{'path': str(p), 'sha256': digest(p), 'bytes': p.stat().st_size} for p in external_artifacts]
}
write_json(EVIDENCE / 'EVIDENCE-INDEX.json', index)
print(json.dumps({'status': result['status'], 'checks': len(checks), 'arms': len(arms), 'image_calls': result['total_image_calls'], 'historical_checksums': len(historical), 'evidence_files': len(files), 'unexpected_protected_changes': unexpected}))
if result['status'] == 'fail':
    raise SystemExit(1)
