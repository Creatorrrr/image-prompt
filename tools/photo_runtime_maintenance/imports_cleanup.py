"""Qualify nine unused imports and one dead local without publishing a runtime."""
from __future__ import annotations

import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
import difflib
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess

import checks
import four_checks
import four_patch
import four_state
from history_state import new, pointers
import state

os.environ['GIT_OPTIONAL_LOCKS'] = '0'
os.environ['GIT_NO_LAZY_FETCH'] = '1'
ROOT = state.ROOT
SKILL = ROOT/'skills/photo-prompt-image-generator'
E = ROOT/'docs/research-evidence/photo-prompt/runtime-import-nine-cleanup-20261019'
HELPER = 'tools/photo_runtime_maintenance/imports_cleanup.py'
PARENT = ROOT/'docs/research-evidence/photo-prompt/runtime-small-five-cleanup-20261019'
PREFIX = 'skills/photo-prompt-image-generator/scripts/'
IMPORTS = {'photo_contracts': {'hashlib', 'json', 'Any'},
           'photo_embodiment': {'copy', 'hashlib', 'json', 'Any'},
           'photo_shared_views': {'Path', 'index'}}
TARGETS = {PREFIX+name+'.py' for name in [*IMPORTS, 'photo_runtime_sources']}


def transform(raw, module):
    tree = ast.parse(raw)
    removed = []
    if module in IMPORTS:
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = {a.asname or a.name for a in node.names}
                if names & IMPORTS[module]:
                    if not names <= IMPORTS[module] or node.lineno != node.end_lineno:
                        raise ValueError('import scope changed')
                    removed.append(node)
        if len(removed) != len(IMPORTS[module]):
            raise ValueError('binding scope changed')
        tree.body = [n for n in tree.body if n not in removed]
    elif module == 'photo_runtime_sources':
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'algorithm_binding')
        removed = [n for n in function.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'get' for t in n.targets)]
        if len(removed) != 1 or removed[0].lineno != removed[0].end_lineno:
            raise ValueError('local assignment scope changed')
        if any(isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load) and n.id == 'get'
               for n in ast.walk(function)):
            raise ValueError('local is now used; defer')
        function.body.remove(removed[0])
    else:
        raise ValueError('unapproved module')
    lines = {n.lineno for n in removed}
    changed = b''.join(line for i, line in enumerate(raw.splitlines(keepends=True), 1) if i not in lines)
    if ast.dump(tree, include_attributes=False) != ast.dump(ast.parse(changed), include_attributes=False):
        raise ValueError('AST exceeds approved scope')
    return changed


def parent_files(delta):
    for name in ('BASELINE.json.gz', 'AFTER-DELTA.json.gz'):
        if state.sha(PARENT/name) != delta['parent_sha256'][name]:
            raise ValueError('parent protection changed')
    files = dict(state.read(PARENT/'BASELINE.json.gz')['files'])
    for path, row in state.read(PARENT/'AFTER-DELTA.json.gz')['source_replacements'].items():
        if files[path] != row['before']:
            raise ValueError('parent source protection changed')
        files[path] = row['after']
    return files


def baseline():
    delta = state.read(E/'BASELINE-DELTA.json.gz')
    files = parent_files(delta)
    files.update(delta['additional_files'])
    return {**delta, 'files': files}


def prepare(private):
    if E.exists():
        raise FileExistsError('never replace completed evidence')
    before = state.read(private/'BEFORE.json.gz')
    original = {rel: (ROOT/rel).read_bytes() for rel in TARGETS}
    for rel, raw in original.items():
        if rel in before['repositories'][str(ROOT)]['status'] or raw != state.git(ROOT, 'show', 'HEAD:'+rel):
            raise ValueError('target now has existing work; defer')
        if state.stamp(ROOT/rel) != before['files'][str(ROOT/rel)]:
            raise ValueError('target drift')
    delta = {'parent_sha256': {n: state.sha(PARENT/n) for n in ('BASELINE.json.gz', 'AFTER-DELTA.json.gz')}}
    previous = parent_files(delta)
    if any(before['files'][p] != stamp for p, stamp in previous.items()):
        raise ValueError('parent snapshot drift')
    new(E/'BASELINE-DELTA.json.gz', {**delta, 'parent_path': str(PARENT.relative_to(ROOT)),
        'additional_files': {p: s for p, s in before['files'].items() if p not in previous},
        'repositories': before['repositories'], 'pointers': before['pointers'],
        'previous_absent': before['previous_absent'], 'protected_count': len(before['files'])})
    candidate = {rel: transform(raw, Path(rel).stem) for rel, raw in original.items()}
    if sum(len(original[p].splitlines())-len(candidate[p].splitlines()) for p in TARGETS) != 10:
        raise ValueError('ten-line scope changed')
    patch = ''.join(line for rel in sorted(TARGETS) for line in difflib.unified_diff(
        original[rel].decode().splitlines(True), candidate[rel].decode().splitlines(True),
        fromfile='a/'+rel, tofile='b/'+rel)).encode()
    (E/'PATCH.patch.gz').write_bytes(gzip.compress(patch, mtime=0))
    executable = private/'qualified.patch'; executable.write_bytes(patch)
    projects = {}
    for label in ('control', 'combined', 'operating'):
        project = private/label; skill = four_patch.copy_code(project); projects[label] = str(project)
        if label != 'control':
            for rel, raw in candidate.items():
                (project/rel).write_bytes(raw)
        if label == 'control':
            (skill/'.runtime').symlink_to(SKILL/'.runtime', target_is_directory=True)
        else:
            subprocess.run(['/bin/cp', '-c', '-R', '-p', str(SKILL/'assets'), str(skill/'assets')], check=True)
            shutil.copytree(ROOT/'tests', project/'tests', ignore=shutil.ignore_patterns('__pycache__'))
            (project/'docs').symlink_to(ROOT/'docs', target_is_directory=True)
            lock = state.read(SKILL/'embedding-runtime.lock.json')
            package = skill/lock['package']; package.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(['/bin/cp', '-c', '-R', '-p', str(SKILL/lock['package']), str(package)], check=True)
            (skill/'.runtime/embedding-python').symlink_to(SKILL/'.runtime/embedding-python', target_is_directory=True)
        print('private project prepared:', label, flush=True)
    project = Path(projects['combined'])
    for flags in [('--reverse', '--check'), ('--reverse',)]:
        subprocess.run(['git', '-C', str(project), 'apply', *flags, str(executable)], check=True)
    if any((project/rel).read_bytes() != raw for rel, raw in original.items()):
        raise ValueError('inverse did not restore exact source')
    subprocess.run(['git', '-C', str(project), 'apply', str(executable)], check=True)
    new(E/'TARGETS.json', {'original': {rel: before['files'][str(ROOT/rel)] for rel in sorted(TARGETS)},
        'candidate': {rel: hashlib.sha256(raw).hexdigest() for rel, raw in candidate.items()},
        'source_lines_removed': 10, 'import_bindings_removed': 9, 'local_assignments_removed': 1,
        'base_head': before['repositories'][str(ROOT)]['head'], 'remaining_AST_equal': True,
        'inverse_exact': True, 'patch_sha256': state.sha(E/'PATCH.patch.gz'),
        'raw_patch_sha256': hashlib.sha256(patch).hexdigest()})
    new(E/'PRIVATE-PROJECTS.json', {'projects': projects, 'private_parent': str(private),
        'model_and_assets_independent_APFS_clones': True, 'model_files': len(lock['files']),
        'source_files': 76, 'scratch_is_not_unique_recovery_material': True})


def worker(project, removed, modules, policy, timeout, log=None):
    env = checks.environment(); env['PHOTO_RUNTIME_STORE'] = str(project/'.test-runtime')
    command = ['/usr/bin/sandbox-exec', '-p', policy, str(SKILL/'.runtime/embedding-python/bin/python'),
        '-I', '-B', str(E/'worker.py'), str(project), '1' if removed else '0', *modules]
    if log:
        with log.open('x') as stream:
            child = subprocess.Popen(command, cwd=project, env=env, stdout=subprocess.PIPE,
                stderr=stream, text=True, start_new_session=True)
            try:
                stdout, _ = child.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGTERM); stdout, _ = child.communicate()
                return {'status': 'TIMEOUT', 'stdout': stdout, 'stderr': log.read_text()}
        stderr, code = log.read_text(), child.returncode
    else:
        child = subprocess.run(command, cwd=project, env=env, capture_output=True, text=True, timeout=timeout)
        stdout, stderr, code = child.stdout, child.stderr, child.returncode
    try:
        result = json.loads(stdout.splitlines()[-1])
    except (ValueError, IndexError):
        result = {'status': 'HARNESS_UNAVAILABLE'}
    result.update(exit_code=code, stdout=stdout, stderr=stderr)
    return result


def source(group):
    output = E/('SOURCE-'+group+'.json')
    if output.exists():
        raise FileExistsError('never overwrite evidence')
    project = Path(state.read(E/'PRIVATE-PROJECTS.json')['projects']['operating' if group == 'operating' else 'combined'])
    log = project/('source-'+group+'.log')
    new(E/('SOURCE-'+group+'-progress.json'), {'private_log': str(log), 'final_log': output.name})
    policy = four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))'
    result = worker(project, True, checks.GROUPS[group], policy, 1800, log)
    expected = state.read(E/'TARGETS.json')['candidate']
    if result.get('exit_code') or result.get('tests') != (48 if group == 'operating' else 70) or result.get('skipped') != 0:
        result['status'] = 'FAIL'
    for rel, sha in expected.items():
        if result.get('loaded_modules', {}).get(Path(rel).stem, {}).get('sha256') != sha:
            result['status'] = 'FAIL'
    result.update(network_denied=True, original_source_reads_denied=True, original_writes_denied=True,
        torch_module_read_denied=True, Gemini_calls=0, CURRENT_writes=0)
    new(output, result); print(group, result['status'], result.get('tests'), 'tests', flush=True)
    if result['status'] != 'PASS':
        raise ValueError(result.get('stderr', '')[-5000:])


def smoke(kind):
    output = E/('SMOKE-'+kind+'.json')
    if output.exists():
        raise FileExistsError('never overwrite evidence')
    project = ROOT if kind == 'applied' else Path(state.read(E/'PRIVATE-PROJECTS.json')['projects'][kind])
    policy = checks.profile() if kind == 'applied' else four_patch.policy()
    policy += '(deny file-read* (regex "/site-packages/torch(/|$)"))'
    if kind == 'applied':
        policy += '(deny file-read* (regex '+json.dumps('^'+re.escape(str(SKILL))+r'/(scripts|precore)/.*\.(pyc|pyo|so|dylib)$')+'))'
    result = worker(project, kind != 'control', [], policy, 90)
    targets = state.read(E/'TARGETS.json')
    expected = {p: s['sha256'] for p, s in targets['original'].items()} if kind == 'control' else targets['candidate']
    if result.get('exit_code') or result.get('status') != 'PASS':
        raise ValueError(result.get('stderr', '')+result.get('stdout', ''))
    for rel, sha in expected.items():
        if result['loaded_modules'][Path(rel).stem]['sha256'] != sha:
            raise ValueError('unexpected source loaded')
    result.update(bytecode_reads_denied=kind == 'applied', network_denied=True,
        original_writes_denied=True, Gemini_calls=0, CURRENT_writes=0)
    new(output, result); print(kind, 'actual source/algorithm/guard smoke PASS', flush=True)


def delegate(kind):
    previous = four_state.E; four_state.E = E
    try:
        if kind.startswith('managed-'):
            four_checks.managed(kind.removeprefix('managed-'))
        elif kind.startswith('history-'):
            four_checks.history(kind.removeprefix('history-'))
        elif kind == 'installed':
            four_checks.installed()
        else:
            raise ValueError(kind)
    finally:
        four_state.E = previous


def verify(output, full=False):
    before = baseline(); applied = state.read(E/'APPLICATION.json')['applied'] if (E/'APPLICATION.json').exists() else {}
    selected = before['files'] if full else {p: s for p, s in before['files'].items()
        if p in before['pointers'] or Path(p).is_relative_to(SKILL/'scripts') or Path(p).is_relative_to(SKILL/'precore')
        or Path(p).name in {'retrieval-runtime.json', 'embedding-default.json', 'embedding-runtime.lock.json'}}
    failures = []; paths = sorted(selected)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path, actual in zip(paths, pool.map(state.stamp, paths)):
            rel = str(Path(path).relative_to(ROOT)) if Path(path).is_relative_to(ROOT) else None
            good = actual == selected[path] if rel not in applied else actual.get('sha256') == applied[rel] and all(
                actual.get(k) == selected[path].get(k) for k in ('mode', 'links'))
            if not good:
                failures.append(path)
    for work, row in before['repositories'].items():
        dirty = state.status(work)
        if work == str(ROOT):
            dirty = {p: s for p, s in dirty.items() if p != HELPER and not p.startswith(str(E.relative_to(ROOT))+'/') and p not in applied}
        if dirty != row['status']:
            failures.append(work+':original work')
        if state.git(work, 'diff', '--cached', '--raw', '-z').decode() != row['staged']:
            failures.append(work+':staging')
        if work != str(ROOT) and (state.git(work, 'rev-parse', 'HEAD').decode().strip() != row['head'] or state.sha(row['index_path']) != row['index_sha256']):
            failures.append(work+':other worktree')
    if pointers() != before['pointers']:
        failures.append('CURRENT inventory')
    for path in before['previous_absent']:
        if Path(path).exists() or Path(path).is_symlink():
            failures.append(path+':removed cache reappeared')
    result = {'status': 'FAIL' if failures else 'PASS', 'checked_paths': len(paths), 'full': full,
        'CURRENT_count': len(before['pointers']), 'failures': failures, 'Gemini_calls': 0, 'CURRENT_writes': 0}
    new(output, result); print(json.dumps(result), flush=True)
    if failures:
        raise ValueError('preservation failed')


GATES = ['SMOKE-control.json', 'SMOKE-combined.json', 'SOURCE-operating.json', 'SOURCE-native.json',
    'HEAD-COMPARISON.json', 'PRE-APPLY-PRESERVATION.json', 'BEFORE-APPLICATION-FULL.json',
    'MANAGED-control.json', 'MANAGED-combined.json', 'INSTALLED.json', 'HISTORY-frozen.json',
    'HISTORY-archive.json', 'HISTORY-negative.json', 'HISTORY-native-view.json']


def apply():
    if (E/'APPLICATION.json').exists() or (E/'APPLY-INTENT.json').exists():
        raise FileExistsError('application already started; inspect instead')
    if any(state.read(E/name)['status'] != 'PASS' for name in GATES):
        raise ValueError('required gate did not pass')
    for key in ('algorithm_without_code', 'algorithm_binding_signature'):
        if state.read(E/'SMOKE-control.json')[key] != state.read(E/'SMOKE-combined.json')[key]:
            raise ValueError('algorithm policy or signature changed')
    targets = state.read(E/'TARGETS.json')
    if state.git(ROOT, 'rev-parse', 'HEAD').decode().strip() != targets['base_head'] or state.git(ROOT, 'diff', '--cached', '--name-only'):
        raise ValueError('HEAD or staging changed')
    dirty = state.status(ROOT)
    if any(rel in dirty or state.stamp(ROOT/rel) != stamp for rel, stamp in targets['original'].items()):
        raise ValueError('target changed; defer')
    raw = gzip.decompress((E/'PATCH.patch.gz').read_bytes())
    if state.sha(E/'PATCH.patch.gz') != targets['patch_sha256'] or hashlib.sha256(raw).hexdigest() != targets['raw_patch_sha256']:
        raise ValueError('qualified patch changed')
    subprocess.run(['git', '-C', str(ROOT), 'apply', '--check', '-'], input=raw, check=True)
    new(E/'APPLY-INTENT.json', {'gate_sha256': {n: state.sha(E/n) for n in GATES}, 'candidate': targets['candidate']})
    subprocess.run(['git', '-C', str(ROOT), 'apply', '-'], input=raw, check=True)
    if any(state.sha(ROOT/rel) != sha for rel, sha in targets['candidate'].items()):
        raise ValueError('applied source differs from tested bytes')
    stats = state.git(ROOT, 'diff', '--numstat', '--', *sorted(TARGETS)).decode().splitlines()
    if sum(int(r.split('\t')[0]) for r in stats) != 0 or sum(int(r.split('\t')[1]) for r in stats) != 10:
        raise ValueError('scope exceeds ten deleted lines')
    new(E/'APPLICATION.json', {'status': 'APPLIED_PENDING_POSTCHECKS', 'applied': targets['candidate'],
        'source_lines_removed': 10, 'import_bindings_removed': 9, 'local_assignments_removed': 1,
        'remaining_AST_equal': True, 'runtime_publish_calls': 0, 'Gemini_calls': 0, 'CURRENT_writes': 0})
    print('Applied qualified nine-import/one-local patch: 10 deleted lines', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command'); parser.add_argument('--private', type=Path)
    parser.add_argument('--output', type=Path); parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args.private)
    elif args.command in checks.GROUPS:
        source(args.command)
    elif args.command.startswith('smoke-'):
        smoke(args.command.removeprefix('smoke-'))
    elif args.command == 'verify':
        verify(args.output, args.full)
    elif args.command == 'apply':
        apply()
    else:
        delegate(args.command)
