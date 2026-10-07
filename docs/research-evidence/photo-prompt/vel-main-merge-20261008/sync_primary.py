"""Fast-forward main while retaining both reviewed and unrelated local changes."""
from pathlib import Path
import argparse
import ast
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
WORK = Path(__file__).resolve().parents[4]
SKILL = Path('skills/photo-prompt-image-generator')
EVIDENCE = Path(__file__).resolve().parent
BACKUP = PRIMARY/'.codex-artifacts/vel-main-merge-20261008/primary-sync'
DERIVED = {(SKILL/'assets'/name).as_posix() for name in
           ('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json')}
MANIFEST = (SKILL/'assets/photo_prompt_source_manifest.json').as_posix()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=PRIMARY)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(name, value):
    (EVIDENCE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def merge_manifest(base, local, target):
    result = copy.deepcopy(local)
    original = {row['file']: row for row in base['sources']}
    current = {row['file']: row for row in result['sources']}
    assert len(current) == len(result['sources'])
    for row in target['sources']:
        name = row['file']
        incoming = {k: v for k, v in row.items() if k != 'load_order'}
        if name in current:
            existing = {k: v for k, v in current[name].items() if k != 'load_order'}
            if existing != incoming:
                old = {k: v for k, v in original.get(name, {}).items() if k != 'load_order'}
                assert existing == old or incoming == old, ('registration conflict', name)
                if existing == old:
                    current[name].update(incoming)
        else:
            added = dict(row, load_order=max(
                r['load_order'] for r in result['sources'] if r['kind'] == row['kind'])+1)
            result['sources'].append(added)
            current[name] = added
    return (json.dumps(result, ensure_ascii=False, indent=2)+'\n').encode()


def existing_vel_scope_merge(base, local, target):
    """Accept only the single reviewed exclusion already present locally."""
    filename = 'photo_prompt_vel_appearance_relations_extension.json'
    def without_exclusion(raw):
        tree = ast.parse(raw)
        removed = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Set):
                old = node.elts
                node.elts = [item for item in old if not (
                    isinstance(item, ast.Constant) and item.value == filename)]
                removed += len(old)-len(node.elts)
        return ast.dump(tree, include_attributes=False), removed
    original, old_count = without_exclusion(base)
    incoming, incoming_count = without_exclusion(target)
    _, local_count = without_exclusion(local)
    assert old_count == 0 and incoming_count == local_count == 1
    assert incoming == original, 'Incoming test changes more than the reviewed VEL source exclusion'
    return local


def prepare(target):
    base = git('rev-parse', 'HEAD').decode().strip()
    assert git('symbolic-ref', '--short', 'HEAD').decode().strip() == 'main'
    assert subprocess.call(['git', 'diff', '--cached', '--quiet'], cwd=PRIMARY) == 0
    assert subprocess.call(['git', 'merge-base', '--is-ancestor', base, target], cwd=PRIMARY) == 0
    before = json.loads((EVIDENCE/'PRIMARY-BEFORE.json').read_text())['files']
    for name, row in before.items():
        path = PRIMARY/name
        if 'symlink' in row:
            assert path.is_symlink() and path.readlink().as_posix() == row['symlink'], name
        else:
            assert path.is_file() and sha(path.read_bytes()) == row['sha256'], name
    incoming = set(git('diff', '--name-only', base, target).decode().splitlines())
    overlap = {name for name in incoming if name in before and before[name]['status'] != '??'}
    collisions = {name for name in incoming if name in before and before[name]['status'] == '??'}
    retained = {}
    exact = []
    BACKUP.mkdir(parents=True, exist_ok=True)
    for name in sorted(overlap | collisions):
        path = PRIMARY/name
        assert path.is_file() and not path.is_symlink(), name
        raw = path.read_bytes()
        saved = BACKUP/name
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
        new = git('show', target+':'+name)
        if raw == new:
            exact.append(name)
            continue
        if name in DERIVED:
            retained[name] = raw
            continue
        if name == MANIFEST:
            retained[name] = merge_manifest(json.loads(git('show', base+':'+name)),
                                            json.loads(raw), json.loads(new))
            continue
        if name in collisions:
            raise AssertionError('Different untracked collision: '+name)
        old_path = BACKUP/'.merge-base'
        new_path = BACKUP/'.merge-target'
        old_path.write_bytes(git('show', base+':'+name))
        new_path.write_bytes(new)
        merged = subprocess.run(['git', 'merge-file', '-p', str(path),
                                 str(old_path), str(new_path)], capture_output=True)
        if merged.returncode == 1 and name.startswith('tests/'):
            retained[name] = existing_vel_scope_merge(old_path.read_bytes(), raw, new)
        else:
            assert merged.returncode == 0, ('Unresolved text conflict', name)
            retained[name] = merged.stdout
    save('PRIMARY-SYNC-PLAN.json', {
        'base': base, 'target': target, 'incoming_paths': sorted(incoming),
        'tracked_overlaps': sorted(overlap), 'untracked_collisions': sorted(collisions),
        'exact_adoptions': exact, 'local_overlays_retained': sorted(retained),
        'backup': str(BACKUP)})
    return base, before, incoming, overlap, collisions, retained


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    target = git('rev-parse', args.target).decode().strip()
    base, before, incoming, overlap, collisions, retained = prepare(target)
    if not args.apply:
        print(json.dumps({'plan': 'PASS', 'tracked_overlaps': len(overlap),
                          'untracked_collisions': len(collisions),
                          'local_overlays_retained': len(retained)}))
        return
    sys.path.insert(0, str(PRIMARY/SKILL/'scripts'))
    from photo_runtime_sources import source_update
    advanced = False
    with source_update(PRIMARY/SKILL):
        try:
            for name in overlap:
                (PRIMARY/name).write_bytes(git('show', base+':'+name))
            for name in collisions:
                moved = BACKUP/'untracked-collisions'/name
                moved.parent.mkdir(parents=True, exist_ok=True)
                os.replace(PRIMARY/name, moved)
            subprocess.run(['git', 'merge', '--ff-only', target], cwd=PRIMARY,
                           check=True, stdout=subprocess.DEVNULL)
            advanced = True
            for name, raw in retained.items():
                (PRIMARY/name).write_bytes(raw)
            for name in overlap | collisions:
                (PRIMARY/name).chmod(before[name]['mode'])
        finally:
            if not advanced:
                for name in overlap:
                    shutil.copy2(BACKUP/name, PRIMARY/name)
                for name in collisions:
                    moved = BACKUP/'untracked-collisions'/name
                    if moved.exists():
                        os.replace(moved, PRIMARY/name)
    unexpected = []
    unchanged = 0
    for name, row in before.items():
        path = PRIMARY/name
        if name in incoming or 'symlink' in row:
            continue
        if not path.is_file() or sha(path.read_bytes()) != row['sha256']:
            unexpected.append(name)
        else:
            unchanged += 1
    assert not unexpected, unexpected
    save('PRIMARY-SYNC-VERIFICATION.json', {
        'status': 'PASS', 'head': git('rev-parse', 'HEAD').decode().strip(),
        'target': target, 'unchanged_unrelated_files': unchanged,
        'non_owned_drift': unexpected, 'combined_indexes_require_canonical_check': True,
        'backup': str(BACKUP)})
    print(json.dumps({'sync': 'PASS', 'unchanged_unrelated_files': unchanged,
                      'head': target}))


if __name__ == '__main__':
    main()
