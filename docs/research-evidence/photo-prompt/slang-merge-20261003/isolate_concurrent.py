"""Freeze the tested publication index while preserving concurrent worktree edits."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SNAPSHOT = Path('/tmp/image-prompt-slang-merge-20261003-otvpg0ba')
INDEX = SNAPSHOT / 'publication.index'
ASSETS = Path('skills/photo-prompt-image-generator/assets')
REGISTRY = ASSETS / 'photo_prompt_visual_obligations.json'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    suite = json.loads((HERE / 'full-suite/FULL-SUITE-RESULT.json').read_text())
    proof = json.loads((HERE / 'PRESERVATION.json').read_text())
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == proof['pulled_remote']
    assert not INDEX.exists()
    current_index = Path(subprocess.check_output(['git', 'rev-parse', '--git-path', 'index'], cwd=ROOT, text=True).strip())
    shutil.copyfile(ROOT / current_index, INDEX)
    environment = {**os.environ, 'GIT_INDEX_FILE': str(INDEX)}
    changed = {
        name: {'tested_sha256': expected, 'worktree_sha256': digest((ROOT / name).read_bytes())}
        for name, expected in suite['source_binding'].items()
        if digest((ROOT / name).read_bytes()) != expected
    }
    helpers = runpy.run_path(ROOT / 'docs/research-evidence/photo-prompt/semantic-guidance-merge-20261003/reconcile_merge.py')
    parents = [json.loads((SNAPSHOT / side / REGISTRY).read_text()) for side in ('base', 'local', 'remote')]
    merged = helpers['merge_json'](*parents)
    recovered = {str(REGISTRY): (json.dumps(merged, ensure_ascii=False, indent=2) + '\n').encode()}
    for name in proof['exclusive_local_files']:
        if name in suite['source_binding'] and name in changed:
            recovered[name] = (SNAPSHOT / 'local' / name).read_bytes()
    for name, raw in recovered.items():
        assert digest(raw) == suite['source_binding'][name], name
        oid = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'], input=raw, cwd=ROOT, text=False).decode().strip()
        subprocess.check_call(['git', 'update-index', '--add', '--cacheinfo', '100644', oid, name], cwd=ROOT, env=environment)
    for name, expected in suite['source_binding'].items():
        raw = subprocess.check_output(['git', 'show', f':{name}'], cwd=ROOT, env=environment)
        assert digest(raw) == expected, name
    # Restore this chat's accidentally staged concurrent changes to the tested
    # version in the shared index, leaving every worktree byte untouched.
    for name, raw in recovered.items():
        before = (ROOT / name).read_bytes()
        oid = subprocess.check_output(['git', 'hash-object', '--stdin'], input=raw, cwd=ROOT).decode().strip()
        subprocess.check_call(['git', 'update-index', '--add', '--cacheinfo', '100644', oid, name], cwd=ROOT)
        assert (ROOT / name).read_bytes() == before, name
    result = {
        'schema_version': 'photo-slang-concurrent-work-preservation/v1',
        'tested_sources_frozen_in_separate_index': True,
        'reviewed_index': str(INDEX), 'expected_parent': proof['pulled_remote'],
        'concurrent_source_changes': changed,
        'recovered_owned_source_paths': sorted(recovered),
        'concurrent_worktree_bytes_not_written': True,
        'all_reviewed_index_source_hashes_match_complete_suite': True,
    }
    (HERE / 'CONCURRENT-WORKTREE.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'concurrent_source_files': len(changed), 'isolated_index_sources_match_tests': True, 'worktree_bytes_written': 0}))


if __name__ == '__main__':
    main()
