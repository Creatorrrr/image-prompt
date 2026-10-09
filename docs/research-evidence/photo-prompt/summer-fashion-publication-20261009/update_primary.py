"""Fast-forward main while preserving its independently authored dirty overlay."""
import argparse
import hashlib
import json
import shutil
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--target', required=True)
args = parser.parse_args()
root = Path('/Users/chasoik/Projects/image-prompt')
evidence = root / 'docs/research-evidence/photo-prompt/summer-fashion-publication-20261009'
holding = Path('/Users/chasoik/.cache/image-prompt/summer-fashion-publication-20261009/primary-holding')
skill = root / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(skill / 'scripts'))
from photo_runtime_sources import source_update, SnapshotPublisher, capture_sources, json_digest


def git(*arguments):
    return subprocess.check_output(['git', *arguments], cwd=root)


def signature(path):
    if not path.exists():
        return None
    if path.is_symlink():
        return dict(symlink=str(path.readlink()))
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return dict(sha256=h.hexdigest(), mode=stat.S_IMODE(path.stat().st_mode), bytes=path.stat().st_size)


assert git('branch', '--show-current').decode().strip() == 'main'
assert not git('diff', '--cached', '--name-only').strip(), 'Another operation has staged primary files.'
old_head = git('rev-parse', 'HEAD').decode().strip()
target = git('rev-parse', args.target).decode().strip()
subprocess.run(['git', 'merge-base', '--is-ancestor', old_head, target], cwd=root, check=True)
changes = [path for path in git('diff', '--name-only', '-z', old_head, target).decode().split('\0') if path]
tracked = {path for path in git('ls-files', '-z').decode().split('\0') if path}
derived = {'skills/photo-prompt-image-generator/assets/' + name for name in (
    'photo_prompt_source_manifest.json', 'photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json')}
for rel in changes:
    if rel in tracked and rel not in derived:
        assert git('show', old_head + ':' + rel) == (root / rel).read_bytes(), 'Dirty tracked overlap requires an intent merge: ' + rel
    elif rel not in tracked and (root / rel).exists():
        assert git('show', target + ':' + rel) == (root / rel).read_bytes(), 'Untracked overlap differs from reviewed target: ' + rel
protected = {path: signature(root / path) for path in tracked - set(changes)}
before_source, _ = capture_sources(skill)
before = dict(head=old_head, target=target, changed_paths=changes, protected=protected,
              derived={path: signature(root / path) for path in derived}, source_fingerprint=json_digest(before_source))
(evidence / 'primary-before-fast-forward.json').write_text(json.dumps(before, ensure_ascii=False, indent=2) + '\n')
saved = []
with source_update(skill):
    for rel in derived:
        source, dest = root / rel, holding / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        assert not dest.exists(), 'Holding already exists; inspect before retry: ' + rel
        shutil.copy2(source, dest)
        saved.append(rel)
    overlaps = [path for path in changes if path not in tracked and (root / path).exists()]
    for rel in overlaps:
        source, dest = root / rel, holding / 'untracked' / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        assert not dest.exists(), 'Overlap holding already exists: ' + rel
        shutil.move(source, dest)
    assert git('rev-parse', 'HEAD').decode().strip() == old_head, 'Primary HEAD advanced before update.'
    subprocess.run(['git', 'restore', '--source=' + old_head, '--worktree', '--', *sorted(derived)], cwd=root, check=True)
    try:
        with (evidence / 'primary-fast-forward.log').open('w') as stream:
            subprocess.run(['git', 'merge', '--ff-only', target], cwd=root, stdout=stream, stderr=subprocess.STDOUT, check=True)
    except BaseException:
        for rel in saved:
            shutil.copy2(holding / rel, root / rel)
        for rel in overlaps:
            shutil.move(holding / 'untracked' / rel, root / rel)
        raise
    for rel in saved:
        shutil.copy2(holding / rel, root / rel)
    # The existing local registry includes other unpublished domains. Preserve
    # its complete registration order after verifying this committed subset.
    local_manifest = json.loads((root / 'skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json').read_text())
    published = json.loads(git('show', target + ':skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json'))
    local_rows = {(row['file'], row['kind']): row for row in local_manifest['sources']}
    for row in published['sources']:
        actual = local_rows.get((row['file'], row['kind']))
        assert actual is not None and actual['required'] == row['required'], 'Published registry entry absent from local overlay.'
after_source, _ = capture_sources(skill)
assert json_digest(after_source) == before['source_fingerprint'], 'Authored working source changed; indexes need a merged local rebuild.'
drift = [path for path, value in protected.items() if signature(root / path) != value]
assert not drift, 'Unexpected protected primary drift: ' + ', '.join(drift[:12])
assert all(signature(root / path) == value for path, value in before['derived'].items()), 'Dirty derived overlay was not restored byte/mode-wise.'
assert git('rev-parse', 'HEAD').decode().strip() == target
pointer = SnapshotPublisher(skill).publish()
receipt = dict(status='pass', completed_at=datetime.now(timezone.utc).isoformat(), previous_head=old_head,
               main_head=target, protected_files_checked=len(protected), protected_drift=drift,
               preserved_derived_overlay=sorted(derived), moved_equal_untracked_files=len(overlaps),
               working_source_fingerprint_unchanged=True, current_runtime=pointer,
               meaning='Git main is fast-forwarded to the reviewed publication; independently authored local source/index overlay remains byte/mode-identical and runtime-valid.')
(evidence / 'primary-fast-forward-receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt, ensure_ascii=False))
