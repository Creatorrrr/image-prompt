"""Read-only cleanup inventory and protected-state checks; no runtime imports."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/runtime-cleanup-20261019'
OWNED_PLAN = 'docs/plans/photo-runtime-and-research-cleanup.md'
OWNED_PREFIXES = ('tools/photo_runtime_maintenance/',
                  'docs/research-evidence/photo-prompt/runtime-cleanup-20261019/')
SHARED = Path.home() / '.cache/image-prompt/photo-shared-runtime'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    p = Path(path)
    return json.loads(gzip.decompress(p.read_bytes()) if p.suffix == '.gz' else p.read_bytes())


def write(path, value):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))+'\n').encode()
    p.write_bytes(gzip.compress(data, mtime=0) if p.suffix == '.gz' else data)


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def status(root):
    raw = git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all').decode().split('\0')
    result = {}
    i = 0
    while i < len(raw):
        row = raw[i]
        i += 1
        if not row:
            continue
        result[row[3:]] = row[:2]
        if 'R' in row[:2] or 'C' in row[:2]:
            result[raw[i]] = 'rename_source'
            i += 1
    return result


def stamp(path):
    p = Path(path)
    if p.is_symlink():
        return {'kind': 'symlink', 'target': os.readlink(p)}
    if not p.exists():
        return {'kind': 'absent'}
    s = p.stat()
    return {'kind': 'file', 'bytes': s.st_size, 'sha256': sha(p),
            'mode': s.st_mode & 0o777, 'device': s.st_dev, 'inode': s.st_ino, 'links': s.st_nlink}


def same(before, after):
    # Existing sealed generations can bind inode identity. Never recreate them.
    return before == after


def files(root, *, skip=('.git', '.venv', '__pycache__', '.runtime')):
    root = Path(root)
    for directory, names, leaves in os.walk(root, followlinks=False):
        names[:] = [n for n in names if n not in skip and not (Path(directory)/n).is_symlink()]
        for name in leaves:
            yield Path(directory)/name


def worktrees():
    rows = git(ROOT, 'worktree', 'list', '--porcelain').decode().splitlines()
    return [Path(r[9:]) for r in rows if r.startswith('worktree ')]


def capture():
    if (EVIDENCE/'BASELINE.json.gz').exists():
        raise ValueError('baseline already exists; never replace it')
    roots = worktrees()
    repo = {}
    protected = set()
    for root in roots:
        changed = status(root)
        if root == ROOT:
            changed.pop(OWNED_PLAN, None)  # Our preceding plan is explicitly included in stage 1.
            changed = {p:v for p,v in changed.items() if not p.startswith(OWNED_PREFIXES)}
        tracked = set(git(root, 'ls-files', '-z').decode().split('\0')) - {''}
        rels = tracked | set(changed)
        protected.update(str(root/p) for p in rels)
        repo[str(root)] = {'head': git(root, 'rev-parse', 'HEAD').decode().strip(),
                           'index_sha256': sha(git(root, 'rev-parse', '--git-path', 'index').decode().strip()),
                           'status': changed, 'tracked_count': len(tracked)}
    pointers = []
    inventories = {}
    for root in [*roots, SHARED]:
        count = 0
        size = 0
        for p in files(root):
            if p.is_symlink():
                continue
            s = p.stat()
            count += 1
            size += s.st_size
            if p.name == 'CURRENT.json':
                pointers.append(str(p))
        inventories[str(root)] = {'files': count, 'logical_bytes': size}
    protected.update(pointers)
    skill = ROOT/'skills/photo-prompt-image-generator'
    config = read(skill/'retrieval-runtime.json')
    base = Path(os.environ.get('PHOTO_RUNTIME_STORE', SHARED)).expanduser()
    store = base/config['store_subdirectory']
    native = store/'generations'/config['native_generation_id']
    hroot = store/'h-f2-generations'/config['generation_id']
    protected.update(str(p) for r in (native, hroot, store/'receipts', store/'h-f2-receipts', store/'receipt-index')
                     for p in files(r, skip=('.git', '__pycache__')))
    lock = read(skill/'embedding-runtime.lock.json')
    protected.update(str(skill/lock['package']/p) for p in lock['files'])
    protected.add(str(skill/'retrieval-runtime.json'))
    print('hashing protected files', len(protected), flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = dict(zip(sorted(protected), pool.map(stamp, sorted(protected))))
    write(EVIDENCE/'BASELINE.json.gz', {'schema': 'photo-cleanup-baseline/v1', 'repositories': repo,
          'files': rows, 'pointers': sorted(pointers), 'inventory': inventories,
          'installed': {'store': str(store), 'native': str(native), 'hroot': str(hroot), 'config': config}})
    write(EVIDENCE/'PROTECTED.json', {'schema': 'photo-cleanup-protection/v1',
          'baseline': 'BASELINE.json.gz', 'baseline_sha256': sha(EVIDENCE/'BASELINE.json.gz'),
          'protected_file_count': len(rows), 'dirty_work': {r:v['status'] for r,v in repo.items()},
          'CURRENT': {p:rows[p] for p in pointers}, 'installed': config,
          'owned_preexisting_plan': OWNED_PLAN, 'defer_unknown': True})
    print('baseline captured', len(rows), 'files;', len(pointers), 'CURRENT pointers', flush=True)


def verify(allow=(), output=None):
    baseline = read(EVIDENCE/'BASELINE.json.gz')
    allow = {str(ROOT/p) for p in allow}
    dirty = {str(Path(root)/p) for root,r in baseline['repositories'].items() for p in r['status']}
    if allow & dirty:
        raise ValueError('allowlist overlaps original dirty work')
    failures = []
    checked = 0
    paths = [p for p in baseline['files'] if p not in allow]
    with ThreadPoolExecutor(max_workers=4) as pool:
        actual = pool.map(stamp, paths)
        for path, after in zip(paths, actual):
            if not same(baseline['files'][path], after):
                failures.append(path)
            checked += 1
    supplementary = EVIDENCE/'ADDITIONAL-PROTECTED.json.gz'
    if supplementary.exists():
        for path, before in read(supplementary).items():
            if not same(before,stamp(path)):
                failures.append(path)
            checked += 1
    for root, row in baseline['repositories'].items():
        current = status(root)
        for path, state in row['status'].items():
            if current.get(path) != state:
                failures.append(str(Path(root)/path)+': git status changed')
        if root != str(ROOT) and git(root, 'rev-parse', 'HEAD').decode().strip() != row['head']:
            failures.append(root+': other worktree HEAD changed')
    result = {'status': 'PASS' if not failures else 'FAIL', 'protected_files_checked': checked,
              'allowed_paths': sorted(allow), 'failures': failures, 'Gemini_calls': 0, 'CURRENT_writes': 0}
    if output:
        write(output, result)
    print(json.dumps({k:v for k,v in result.items() if k!='allowed_paths'} |
                     {'allowed_path_count':len(allow)}, ensure_ascii=False), flush=True)
    if failures:
        raise ValueError('protected state changed')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['capture', 'verify'])
    p.add_argument('--allow-json', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    if a.command == 'capture':
        capture()
    else:
        verify(read(a.allow_json) if a.allow_json else (), a.output)
