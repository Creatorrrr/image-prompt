"""Install a verified fast-forward while retaining every unrelated working file.

Only the task's reviewed files may replace a dirty file. Other dirty/untracked
bytes, including unfinished local historical descriptors, remain in place.
The primary index and main ref advance to the already-published commit.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import zipfile

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
REL = Path('docs/research-evidence/photo-prompt/seduction-expression-main-merge-20261005')
HERE = Path(__file__).resolve().parent
destination = sys.argv[1]
assert re.fullmatch('[0-9a-f]{40}', destination)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=PRIMARY)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


before = json.loads((HERE / 'PRIMARY-BEFORE.json').read_text())
assert git('symbolic-ref', '--short', 'HEAD').decode().strip() == 'main'
assert git('rev-parse', 'HEAD').decode().strip() == before['head'], 'Primary HEAD advanced; recalculate the synchronization.'
assert git('rev-parse', 'origin/main').decode().strip() == destination, 'Destination must be the verified published main.'
subprocess.run(['git', 'merge-base', '--is-ancestor', before['head'], destination], cwd=PRIMARY, check=True)
subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=PRIMARY, check=True)
protected = {row['path']: row for row in before['dirty_files']}
for name, row in protected.items():
    assert sha(PRIMARY / name) == row['sha256'], ('Concurrent working-file change', name)

applied = json.loads((PRIMARY / 'docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/implementation/APPLIED-CHANGES-FINAL.json').read_text())
owned = {'skills/photo-prompt-image-generator/assets/' + name for name in applied['authored_files']}
owned.update({
    'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json',
    'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json',
    'skills/photo-prompt-image-generator/scripts/prompt_generator.py',
    'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v13.json',
    'skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json',
    'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py',
    'tests/photo_prompt_fixtures.py', 'tests/test_photo_krummholz_korean_alias_data_cleanup.py',
    'tests/test_photo_liminal_active_use_korean_data_cleanup.py', 'tests/test_photo_pose_vocabulary_semantics.py',
    'tests/test_photo_protostar_korean_alias_data_cleanup.py', 'tests/test_photo_scene_data_cleanup.py',
    'tests/test_photo_shelf_return_korean_state_data_cleanup.py',
})
# The former task-owned V13 has a distinct preserved name; the upstream V13
# uniform history keeps the canonical name, and this integration adds V16.
legacy = 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v13.json'
parallel = HERE / 'parallel-local-seduction-v13.json'
assert (PRIMARY / legacy).read_bytes() == parallel.read_bytes()

changes = [item.decode() for item in git('diff', '--name-only', '-z', before['head'], destination).split(b'\0') if item]
tree = {}
for item in git('ls-tree', '-r', '-z', destination).split(b'\0'):
    if not item:
        continue
    header, name = item.split(b'\t', 1)
    mode, kind, oid = header.decode().split()
    tree[name.decode()] = (mode, kind, oid)
local_indexes = {
    'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json',
    'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json',
}
planned = [name for name in changes if (name not in protected or name in owned) and name not in local_indexes]
for name in planned:
    if name in tree:
        mode, kind, oid = tree[name]
        assert kind == 'blob' and mode in {'100644', '100755'}, ('Unexpected file mode', name, mode)
        assert not (PRIMARY / name).is_symlink(), ('Unexpected existing symlink', name)
backup = PRIMARY / REL / 'PRIMARY-OWNED-BEFORE-SYNC.zip'
backup.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(backup, 'w', zipfile.ZIP_DEFLATED) as saved:
    for name in owned:
        path = PRIMARY / name
        if name in protected and path.is_file():
            saved.write(path, name)

# Update only the index; -u is deliberately absent so no working file can be
# overwritten implicitly. The conditional ref update detects concurrent Git work.
git('read-tree', '--reset', destination)
try:
    git('update-ref', '-m', 'merge latest main; preserve unrelated working files',
        'refs/heads/main', destination, before['head'])
except Exception:
    git('read-tree', '--reset', before['head'])
    raise
written, removed = [], []
for name in planned:
    path = PRIMARY / name
    if name not in tree:
        if path.is_file():
            path.unlink()
            removed.append(name)
        continue
    mode, kind, oid = tree[name]
    assert kind == 'blob' and mode in {'100644', '100755'}, ('Unexpected file mode', name, mode)
    raw = git('cat-file', 'blob', oid)
    if path.is_file() and path.read_bytes() == raw:
        continue
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    path.chmod(0o755 if mode == '100755' else 0o644)
    written.append(name)

from rebuild_primary_working_indexes import rebuild
working_indexes = rebuild()
retained = [name for name in protected if name not in owned]
assert all(sha(PRIMARY / name) == protected[name]['sha256'] for name in retained), 'Unrelated working-file bytes changed'
assert git('rev-parse', 'HEAD').decode().strip() == destination
subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=PRIMARY, check=True)
receipt = {
    'status': 'pass', 'previous_main': before['head'], 'installed_main': destination,
    'protected_working_files_retained': len(retained), 'retained_sha256': {name: protected[name]['sha256'] for name in retained},
    'written_paths': written, 'removed_paths': removed,
    'task_owned_before_archive_sha256': sha(backup), 'index_matches_published_commit': True,
    'local_draft_indexes_rebuilt_without_embedding_calls': working_indexes['status'] == 'pass',
    'verification_scope': 'Full tests passed on the isolated published tree. Unrelated local drafts remain uncommitted in the primary checkout.',
}
(PRIMARY / REL / 'PRIMARY-SYNC-VERIFICATION.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({key: value for key, value in receipt.items() if key not in {'retained_sha256', 'written_paths', 'removed_paths'}}))
