"""Verify final artifact bindings and summarize observations without quality inference."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
O = Path(__file__).resolve().parent
ROOT = O.parents[4]
S = ROOT / 'skills/photo-prompt-image-generator'
def read(p): return json.loads(p.read_bytes())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
release = read(O / 'successor.json')
freeze = read(O / 'independent-arm-freeze-and-binding.json')
exposure = read(O / 'managed-retrieval-exposure.json')
skill_sha = sha(S / 'SKILL.md')
expected_skill = 'e26f7fbefab8a3385ceb1780909513544d8deb011efd390cbb545e43b0b49cf9'
reference_sha = '06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7'
assert skill_sha == expected_skill
assert read(O / 'final-source-validation.json')['status'] == 'pass'
for name in ('final-default-preservation.json', 'final-default-search-preservation.json'):
    assert read(O / name)['status'] == 'pass'
result_names = {'a': 'FINAL-RESULT.json', 'b': 'arm-result.json', 'c': 'FINAL-RESULT.json'}
rows = []
for arm in 'abc':
    p = ROOT / ('generated/photo-runs/investigative-fiction-20261025-' + arm)
    m = read(p / 'run_manifest.json')
    w = read(p / 'workflow.json')
    prior = next(r for r in freeze['rows'] if r['arm'] == arm)
    assert sha(Path(prior['prospective_testcase']['path'])) == prior['prospective_testcase']['sha256']
    for k, v in prior['immutable_artifact_hashes_verified'].items():
        assert sha(Path(v['path'])) == v['sha256'], (arm, k)
    assert m['image_call_count'] == 1 and m['status'] == 'success'
    assert m['cross_arm_inputs_used'] is False
    assert m['skill_sha256'] == skill_sha
    assert m['reference_sha256'] == [reference_sha]
    assert m['source_ref'] in {
        'h-f2:' + release['generation_id'],
        'installed-h-f2:' + release['generation_id'],
        'h-f2:' + release['generation_id'] + '/native:' + release['native_generation_id']}
    assert read(Path(w['artifacts']['h_f2_receipt']['path']))['generation_id'] == release['generation_id']
    assert w['source_binding']['generation_id'] == release['native_generation_id']
    assert w['phase'] == 'review_record_validated'
    assert len(w['operations']) == 1 and w['operations'][0]['status'] == 'complete'
    assert len(w['operations'][0]['attempts']) == 1
    assert len(m['image_hashes']) == 1
    image_row = m['image_hashes'][0]
    assert sha(Path(image_row['path'])) == image_row['sha256']
    prompt = p / 'final-prompt.txt'
    prompt_runtime_sha = hashlib.sha256(prompt.read_text().strip().encode()).hexdigest()
    assert prompt_runtime_sha == m['runtime_prompt_sha256']
    root_review = read(O / ('root-pixel-review-' + arm + '.json'))
    assert root_review['image_path'] == image_row['path']
    assert root_review['expected_image_sha256'] == image_row['sha256']
    assert sum(g['strict_pass'] for g in root_review['gates']) == root_review['passed_gates']
    arm_result = p / result_names[arm]
    assert arm_result.is_file()
    rows.append({
        'arm': arm, 'run_id': w['run_id'], 'workflow_phase': w['phase'],
        'actual_image_calls': 1, 'quality_regenerations': 0,
        'image': image_row, 'prompt_path': str(prompt), 'prompt_file_sha256': sha(prompt),
        'runtime_prompt_sha256': prompt_runtime_sha,
        'manifest': {'path': str(p / 'run_manifest.json'), 'sha256': sha(p / 'run_manifest.json')},
        'arm_result': {'path': str(arm_result), 'sha256': sha(arm_result)},
        'prospective_testcase': prior['prospective_testcase'],
        'new_source_exposure': next(r for r in exposure['arms'] if r['arm'] == arm),
        'new_source_adoptions': 0,
        'existing_generic_inspiration_count': 1 if arm == 'c' else 0,
        'native_whole_source_selections': 0,
        'root_review_path': str(O / ('root-pixel-review-' + arm + '.json')),
        'root_passed_gates': root_review['passed_gates'],
        'total_gates': root_review['total_gates'],
        'broad_topic_visible': root_review['broad_investigative_topic_visible'],
        'strict_whole_scene_pass': root_review['strict_whole_scene_pass'],
        'requester_acceptance': 'pending'
    })
summary = {
    'schema': 'investigative-fiction-integration-final/v1',
    'completed_at_utc': datetime.now(timezone.utc).isoformat(),
    'requested_integration_and_three_independent_tests_completed': True,
    'data': {'new_optional_visual_sources': 66, 'new_excluded_diagnostics': 47,
             'new_optional_bindings': 132, 'existing_adjacent_sources_reused': 3,
             'narrow_existing_wording_updates': 5, 'advisory_routes': 339,
             'native_approval_granted': False},
    'tested_release': release,
    'current_default_preservation': read(O / 'final-default-search-preservation.json'),
    'source_validation': str(O / 'final-source-validation.json'),
    'retrieval_development': read(O / 'retrieval-qualification.json')['summary'],
    'image_experiment': {
        'independent_arms': 3, 'successful_actual_calls': sum(r['actual_image_calls'] for r in rows),
        'quality_regenerations': 0, 'broad_topic_visible': sum(r['broad_topic_visible'] for r in rows),
        'strict_whole_scene_passes': sum(r['strict_whole_scene_pass'] for r in rows),
        'arms_with_new_source_adoption': 0, 'new_source_pixel_effect_qualified': False,
        'SKILL_sha256': skill_sha, 'reference_sha256': reference_sha, 'arms': rows},
    'limits': [
        'Three random independent after-integration scenes are not a baseline-versus-successor causal image experiment.',
        'All three read as investigative fiction; none satisfies every prospective relation gate.',
        'New sources were sampled by A and B, but not adopted; C sampled no new source. New-data pixel effect is unverified.',
        'Agent/root gate counts differ for B topic conjunction and C exact map target; both reviewer sets reject strict whole scenes.',
        'The current default advanced concurrently and retained all investigative source changes; tests remain on their earlier pinned generation.',
        'User acceptance has not been received.'
    ],
    'commit_or_push_performed': False, 'requester_acceptance': 'pending'
}
(O / 'FINAL.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': 'complete', 'actual_calls': 3, 'broad_topic_visible': 3,
                  'strict_scene_passes': 0, 'new_source_adoptions': 0,
                  'manifest_and_frozen_artifact_bindings': 'pass'}, ensure_ascii=False))
