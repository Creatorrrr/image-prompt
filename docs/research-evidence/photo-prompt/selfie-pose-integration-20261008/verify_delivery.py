"""Verify published source, preserved originals and delivery file integrity."""
import datetime, hashlib, json, re
from pathlib import Path

W = Path(__file__).resolve().parents[4]
P = Path('/Users/chasoik/Projects/image-prompt')
REL = Path('docs/research-evidence/photo-prompt/selfie-pose-integration-20261008')
E, D = W / REL, P / REL

def read(path):
    return json.loads(path.read_text())

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

skill = P / 'skills/photo-prompt-image-generator/SKILL.md'
skill_sha = sha(skill)
assert skill_sha == sha(W / skill.relative_to(P))
application = read(D / 'primary-application-revision-3.json')
assert len(application['copied']) == 40
for row in application['copied']:
    assert sha(P / row['path']) == row['after_sha256']
preservation = read(D / 'preservation-verification.json')
assert preservation['head_before'] == preservation['head_after']
assert not preservation['unrelated_differences']
assert all(row['matches_application'] for row in preservation['owned_artifacts'])

sources = P / 'skills/photo-prompt-image-generator/assets'
candidate_data = read(sources / 'photo_prompt_selfie_pose_extension.json')
profiles = read(sources / 'photo_prompt_visual_obligations_selfie_pose.json')['profiles']
candidate_count = sum(len(slot)
                      for collection in ['slots', 'existing_slot_context_extensions']
                      for slot in candidate_data[collection].values())
assert candidate_count == 104 and len(profiles) == 101
component_count = sum(len(profile['authored_components']['components']) for profile in profiles)
assert component_count == 303

cases = read(D / 'test-cases.json')['cases']
native_checks = []
arm_files_checked = 0
for case in cases:
    arm = case['arm']
    root = D / 'arms' / arm
    q = read(root / 'qualification.json')
    manifest = read(root / 'run_manifest.json')
    assert manifest['skill_sha256'] == skill_sha
    if arm == 'mirror':
        origin = Path(q['image']['returned_local_path'])
        observations = list(q['official_hard_gates'].values())
        calls = q['image']['actual_image_tool_calls']
    elif arm == 'ultrawide':
        origin = Path(q['generation']['returned_local_path'])
        observations = q['official_pixel_review']['hard_gate_observations']
        calls = q['generation']['actual_image_call_count']
    else:
        origin = Path(q['generation']['native_image_path'])
        observations = q['authoritative_gate_results']
        calls = q['generation']['actual_image_call_count']
    assert calls == 1
    assert len(observations) == case['official_hard_gates']['expected']
    assert all(row['status'].lower() == 'pass' for row in observations)
    assert sha(origin) == sha(Path(case['image_path'])) == case['image_sha256']
    native_checks.append({'arm': arm, 'returned_original': str(origin),
                          'delivered_original': case['image_path'],
                          'sha256': case['image_sha256'], 'unedited': True,
                          'actual_native_calls': calls,
                          'official_gate_count': len(observations),
                          'exact_scope': 'Existing embodiment gates; ultrawide also uses existing pc16. No new visual profile was adopted.'})
    for file in (W / REL / 'arms' / arm).rglob('*'):
        if file.is_file():
            assert sha(file) == sha(P / file.relative_to(W)), file
            arm_files_checked += 1

links = re.findall(r'\]\((/[^)]+)\)', (D / 'README.md').read_text())
for target in links:
    assert Path(target).is_file(), target
records = [{'path': str(file.relative_to(D)), 'bytes': file.stat().st_size,
            'sha256': sha(file)} for file in sorted(D.rglob('*'))
           if file.is_file() and file.name != 'delivery-integrity.json']
receipt = {
    'schema_version': 'selfie-pose-delivery-integrity/v1',
    'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'current_skill_path': str(skill), 'current_skill_sha256': skill_sha,
    'three_arms_used_current_skill_bytes': True,
    'new_source_counts': {'candidates': candidate_count, 'profiles': len(profiles),
                          'authored_components': component_count},
    'final_publication': read(D / 'primary-runtime-publication-revision-3.json'),
    'applied_artifacts_hash_matched': 40,
    'tracked_paths_preservation_verified': preservation['tracked_paths_checked'],
    'head_unchanged': True, 'unrelated_tracked_changes': [],
    'arm_files_byte_matched_with_worktree': arm_files_checked,
    'native_original_checks': native_checks,
    'local_report_file_links_checked': len(links),
    'delivery_files': records,
    'limits': ['File and source binding verification does not establish visual correctness.',
               'Native pixel reviews are manual observations preserved in each arm report.',
               'No generated baseline comparison, user acceptance or all-profile pixel validation.']
}
(D / 'delivery-integrity.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
assert read(D / 'delivery-integrity.json') == receipt
print(json.dumps({'delivery_files': len(records), 'arm_files_matched': arm_files_checked,
                  'native_originals_matched': len(native_checks),
                  'current_skill_bytes_matched': True,
                  'source_counts': receipt['new_source_counts']}, ensure_ascii=False))
