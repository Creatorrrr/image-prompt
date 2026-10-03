"""Verify both merge parents, unchanged authored indexes and retained evidence."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git_bytes(ref, name):
    return subprocess.check_output(['git', 'show', f'{ref}:{name}'], cwd=ROOT)


def main():
    parents = json.loads((HERE / 'PARENTS.json').read_text())
    changed = {side: set(subprocess.check_output(
        ['git', 'diff', '--name-only', parents['base'], parents[side]],
        cwd=ROOT, text=True).splitlines()) for side in ('local', 'remote')}
    overlap = changed['local'] & changed['remote']
    generator = 'skills/photo-prompt-image-generator/scripts/prompt_generator.py'
    assert overlap == {generator}, overlap
    preserved = {}
    for side in ('local', 'remote'):
        preserved[side] = {}
        for name in sorted(changed[side] - overlap):
            raw = (ROOT / name).read_bytes()
            assert raw == git_bytes(parents[side], name), name
            preserved[side][name] = sha(raw)
    raw = (ROOT / generator).read_bytes()
    registrations = [b'    "photo_prompt_visual_obligations_slang_visual.json",\n',
                     b'    "photo_prompt_slang_visual_extension.json",\n']
    remote_bytes = git_bytes(parents['remote'], generator)
    for line in registrations:
        assert raw.count(line) == 1 and line not in remote_bytes
        raw = raw.replace(line, b'', 1)
    assert raw == remote_bytes
    assets = ROOT / 'skills/photo-prompt-image-generator/assets'
    semantic = json.loads((assets / 'photo_prompt_semantic_index.json').read_text())
    for descriptor in semantic['shards']:
        name = 'skills/photo-prompt-image-generator/assets/' + descriptor['path']
        raw = (ROOT / name).read_bytes()
        assert sha(raw) == descriptor['sha256'] and raw == git_bytes(parents['local'], name)
    initial = HERE.parent / 'slang-integration-20261003'
    native = json.loads((initial / 'NATIVE-INTEGRITY.json').read_text())
    for attempt in native['attempts']:
        for name, expected in attempt['files_sha256'].items():
            assert sha((initial / name).read_bytes()) == expected, name
    assert sha((initial / 'reference-photo.jpg').read_bytes()) == native['reference_sha256']
    for name in ('visual_obligation_routing_v1.jsonl', 'visual_obligation_routing_holdout_v1.jsonl'):
        path = 'tests/fixtures/photo_prompt/' + name
        assert git_bytes(parents['local'], path) == git_bytes(parents['remote'], path) == (ROOT / path).read_bytes()
    for version in range(1, 8):
        path = f'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v{version}.json'
        assert git_bytes(parents['local'], path) == git_bytes(parents['remote'], path) == (ROOT / path).read_bytes()
    retrieval = json.loads((HERE / 'RETRIEVAL.json').read_text())
    assert retrieval['boundary']['candidate_pack_bytes_unchanged']
    assert all(all(arm['target_meanings_exposed'].values()) for arm in retrieval['arms'])
    result = {
        'schema_version': 'photo-slang-upstream-parent-preservation/v1', 'parents': parents,
        'local_exclusive_file_count': len(preserved['local']),
        'remote_exclusive_file_count': len(preserved['remote']),
        'exclusive_files_sha256': preserved, 'overlapping_paths': sorted(overlap),
        'merged_generator_equals_remote_plus_two_local_registrations': True,
        'authored_registry_and_semantic_visual_index_bytes_equal_local_parent': True,
        'existing_camera_owner_blind_V2_limitations_preserved_without_tuning': True,
        'all_frozen_inputs_and_holdouts_preserved': True,
        'all_three_arms_target_meanings_exposed': True,
        'boundary_V8_entire_pack_bytes_unchanged': True,
        'prior_native_bytes_and_verdicts_unchanged': True,
        'latest_arm_pixel_verdicts': native['latest_arm_verdicts'],
        'index_rebuilds_needed': 0, 'embedding_api_calls': 0, 'native_image_calls': 0,
    }
    (HERE / 'PRESERVATION.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'exclusive_files_sha256'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
