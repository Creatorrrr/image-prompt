"""Qualify five unused helpers and two bindings, preserving overlapping dirty work."""
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
E = ROOT/'docs/research-evidence/photo-prompt/runtime-small-five-cleanup-20261019'
HELPER = 'tools/photo_runtime_maintenance/small_cleanup.py'
PREFIX = 'skills/photo-prompt-image-generator/scripts/'
FUNCTIONS = {
    'prompt_generator.py': ['character_axis_value_classes', 'cosine_similarity',
        'core_focal_hit_supported', 'filter_authorial_negative_entries'],
    'audit_composed_prompt.py': ['english_prompt_word_count'],
}
TARGETS = {PREFIX+f for f in [*FUNCTIONS, 'photo_runtime_sources.py']}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def transform(raw, filename):
    tree = ast.parse(raw)
    selected = [n for n in tree.body if isinstance(n, ast.FunctionDef)
                and n.name in FUNCTIONS.get(filename, [])]
    if len(selected) != len(FUNCTIONS.get(filename, [])):
        raise ValueError('function scope drift')
    removed = {i for n in selected for i in range(n.lineno, n.end_lineno+1)}
    lines = raw.splitlines(keepends=True)
    expected = tree
    expected.body = [n for n in tree.body if n not in selected]
    if filename == 'photo_runtime_sources.py':
        imports = [n for n in tree.body if isinstance(n, ast.Import)
                   and len(n.names) == 1 and n.names[0].name == 'photo_shared_views']
        readers = [n for n in tree.body if isinstance(n, ast.ImportFrom)
                   and n.module == 'photo_search_reader']
        if len(imports) != 1 or len(readers) != 1:
            raise ValueError('import scope drift')
        first, reader = imports[0], readers[0]
        if first.lineno != first.end_lineno or reader.lineno != reader.end_lineno:
            raise ValueError('unexpected multiline import')
        if [a.name for a in reader.names] != ['SearchReader', 'LazyRuntimeData', 'identity']:
            raise ValueError('reader bindings changed')
        removed.add(first.lineno)
        lines[reader.lineno-1] = b'from photo_search_reader import LazyRuntimeData, identity\n'
        expected.body.remove(first)
        reader.names = reader.names[1:]
    changed = b''.join(line for i, line in enumerate(lines, 1) if i not in removed)
    if ast.dump(expected, include_attributes=False) != ast.dump(ast.parse(changed), include_attributes=False):
        raise ValueError('unapproved AST change')
    return changed


def dirty_payload(before, after):
    old, current = before.splitlines(keepends=True), after.splitlines(keepends=True)
    changes = [(tag, [b.hex() for b in old[i:j]], [b.hex() for b in current[k:l]])
               for tag, i, j, k, l in difflib.SequenceMatcher(None, old, current, autojunk=False).get_opcodes()
               if tag != 'equal']
    return digest(json.dumps(changes, separators=(',', ':')).encode())


def owned(relative):
    return relative == HELPER or relative.startswith(str(E.relative_to(ROOT))+'/')


def prepare(private):
    if E.exists():
        raise FileExistsError('never replace existing qualification')
    before = state.read(private/'BEFORE.json.gz')
    base = before['repositories'][str(ROOT)]['head']
    if state.git(ROOT, 'rev-parse', 'HEAD').decode().strip() != base or state.git(ROOT, 'diff', '--cached', '--name-only'):
        raise ValueError('HEAD or staging changed')
    originals = {rel: (ROOT/rel).read_bytes() for rel in TARGETS}
    heads = {rel: state.git(ROOT, 'show', base+':'+rel) for rel in TARGETS}
    work = {rel: transform(raw, Path(rel).name) for rel, raw in originals.items()}
    index = {rel: transform(raw, Path(rel).name) for rel, raw in heads.items()}
    if any(state.stamp(ROOT/rel) != before['files'][str(ROOT/rel)] for rel in TARGETS):
        raise ValueError('source drift after capture')
    payloads = {rel: dirty_payload(heads[rel], originals[rel]) for rel in TARGETS}
    if any(dirty_payload(index[rel], work[rel]) != payloads[rel] for rel in TARGETS):
        raise ValueError('original dirty changes were altered')
    E.mkdir(parents=True)
    shutil.copy2(private/'BEFORE.json.gz', E/'BASELINE.json.gz')
    patches = {}
    for label, old, changed in [('WORKING', originals, work), ('INDEX', heads, index)]:
        raw = ''.join(line for rel in sorted(TARGETS) for line in difflib.unified_diff(
            old[rel].decode().splitlines(True), changed[rel].decode().splitlines(True),
            fromfile='a/'+rel, tofile='b/'+rel)).encode()
        (E/(label+'.patch.gz')).write_bytes(gzip.compress(raw, mtime=0))
        (private/(label+'.patch')).write_bytes(raw)
        patches[label] = {'raw_sha256': digest(raw), 'sha256': state.sha(E/(label+'.patch.gz'))}
    worker = ROOT/'docs/research-evidence/photo-prompt/runtime-remaining-after-camera-20261019/probe_worker.py'
    shutil.copy2(worker, E/'worker.py')
    projects = {}
    for label in ('control', 'combined', 'operating'):
        project = private/label
        skill = four_patch.copy_code(project)
        projects[label] = str(project)
        if label != 'control':
            for rel, raw in work.items():
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
    for args in [('--reverse', '--check'), ('--reverse',)]:
        subprocess.run(['git', '-C', str(project), 'apply', *args, str(private/'WORKING.patch')], check=True)
    if any((project/rel).read_bytes() != originals[rel] for rel in TARGETS):
        raise ValueError('inverse did not restore source bytes')
    subprocess.run(['git', '-C', str(project), 'apply', str(private/'WORKING.patch')], check=True)
    new(E/'TARGETS.json', {'base_head': base, 'functions': FUNCTIONS, 'functions_removed': 5,
        'function_lines_removed': 41, 'import_bindings_removed': 2,
        'original': {rel: before['files'][str(ROOT/rel)] for rel in sorted(TARGETS)},
        'working': {rel: digest(raw) for rel, raw in work.items()},
        'index': {rel: digest(raw) for rel, raw in index.items()},
        'original_dirty_payload_sha256': payloads, 'patches': patches,
        'remaining_AST_equal': True, 'working_patch_inverse_exact': True,
        'original_dirty_payload_equal': True})
    new(E/'PRIVATE-PROJECTS.json', {'projects': projects, 'private_parent': str(private),
        'model_and_assets_independent_APFS_clones': True, 'model_files': len(lock['files']),
        'source_files': 76, 'scratch_is_not_unique_recovery_material': True})


def source(group):
    output = E/('SOURCE-'+group+'.json')
    if output.exists():
        raise FileExistsError('never overwrite evidence')
    info = state.read(E/'PRIVATE-PROJECTS.json')
    project = Path(info['projects']['operating' if group == 'operating' else 'combined'])
    for rel, sha in state.read(E/'TARGETS.json')['working'].items():
        if state.sha(project/rel) != sha:
            raise ValueError('candidate drift')
    log = project/('source-'+group+'.log')
    new(E/('SOURCE-'+group+'-progress.json'), {'private_log': str(log), 'final_log': output.name})
    policy = four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))'
    env = checks.environment(); env['PHOTO_RUNTIME_STORE'] = str(project/'.test-runtime')
    names = [n for values in FUNCTIONS.values() for n in values]
    with log.open('x') as stream:
        process = subprocess.Popen(['/usr/bin/sandbox-exec', '-p', policy,
            str(SKILL/'.runtime/embedding-python/bin/python'), '-I', '-B', str(E/'worker.py'),
            str(project), json.dumps(names), '1', *checks.GROUPS[group]], cwd=project, env=env,
            stdout=subprocess.PIPE, stderr=stream, text=True, start_new_session=True)
        try:
            stdout, _ = process.communicate(timeout=1800)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM); stdout, _ = process.communicate()
            new(output, {'status': 'TIMEOUT', 'stdout': stdout, 'stderr': log.read_text()})
            raise ValueError('source timeout')
    try:
        result = json.loads(stdout.splitlines()[-1])
    except (ValueError, IndexError):
        result = {'status': 'HARNESS_UNAVAILABLE'}
    result.update(exit_code=process.returncode, stdout=stdout, stderr=log.read_text(),
        network_denied=True, live_source_reads_denied=True, original_writes_denied=True,
        torch_module_read_denied=True, Gemini_calls=0, CURRENT_writes=0)
    if process.returncode or result.get('tests') != (48 if group == 'operating' else 70) or result.get('skipped') != 0:
        result['status'] = 'FAIL'
    for module in ('prompt_generator', 'audit_composed_prompt', 'photo_runtime_sources'):
        row = result.get('loaded_modules', {}).get(module, {})
        rel = PREFIX+module+'.py'
        if row.get('sha256') != state.read(E/'TARGETS.json')['working'][rel]:
            result['status'] = 'FAIL'
    new(output, result)
    print(group, result['status'], result.get('tests'), 'tests', flush=True)
    if result['status'] != 'PASS':
        raise ValueError(result['stderr'][-5000:])


def delegate(kind):
    previous = four_state.E
    four_state.E = E
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


def smoke(kind):
    """Check actual loaded Python paths, removed attributes and source-hash guards."""
    import re
    output = E/('SMOKE-'+kind+'.json')
    if output.exists():
        raise FileExistsError('never overwrite smoke evidence')
    targets = state.read(E/'TARGETS.json')
    project = ROOT if kind == 'applied' else Path(state.read(E/'PRIVATE-PROJECTS.json')['projects'][kind])
    policy = checks.profile() if kind == 'applied' else four_patch.policy()
    policy += '(deny file-read* (regex "/site-packages/torch(/|$)"))'
    if kind == 'applied':
        policy += '(deny file-read* (regex '+json.dumps(
            '^'+re.escape(str(SKILL))+r'/(scripts|precore)/.*\.(pyc|pyo|so|dylib)$')+'))'
    names = [] if kind == 'control' else [n for values in FUNCTIONS.values() for n in values]
    command = ['/usr/bin/sandbox-exec', '-p', policy, str(SKILL/'.runtime/embedding-python/bin/python'),
        '-I', '-B', str(E/'worker.py'), str(project), json.dumps(names), '0' if kind == 'control' else '1']
    process = subprocess.run(command, env=checks.environment(), capture_output=True, text=True, timeout=90)
    if process.returncode:
        raise ValueError(process.stderr+process.stdout)
    result = json.loads(process.stdout.splitlines()[-1])
    expected = {rel: row['sha256'] for rel, row in targets['original'].items()} if kind == 'control' else targets['working']
    if any(row['sha256'] != expected[PREFIX+module+'.py'] for module, row in result['loaded_modules'].items()):
        raise ValueError('unexpected loaded source')
    if result['status'] != 'PASS':
        raise ValueError('smoke failed')
    guard = subprocess.run(['/usr/bin/sandbox-exec', '-p', policy,
        str(SKILL/'.runtime/embedding-python/bin/python'), '-I', '-B', '-c', four_patch.SMOKE,
        str(project/'skills/photo-prompt-image-generator'), '{}'],
        env=checks.environment(), capture_output=True, text=True, timeout=90)
    if guard.returncode:
        raise ValueError(guard.stderr+guard.stdout)
    result.update(functional_guard=json.loads(guard.stdout), bytecode_reads_denied=kind == 'applied',
        network_denied=True, original_writes_denied=True, Gemini_calls=0, CURRENT_writes=0)
    new(output, result); print(kind, 'source and functional guard smoke PASS', flush=True)


def head_source():
    """Test the separately staged HEAD-derived Python variant with existing test inputs."""
    output = E/'HEAD-SOURCE.json'
    if output.exists():
        raise FileExistsError('never overwrite evidence')
    info, targets = state.read(E/'PRIVATE-PROJECTS.json'), state.read(E/'TARGETS.json')
    tests = ['tests.test_photo_bm25f_retrieval', 'tests.test_photo_contextual_source_effects']
    worker = E/'head_worker.py'
    raw_worker = (E/'worker.py').read_text()
    old = "'shared_views_loaded_before_generator':before_generator"
    extension = old+",'failures':[(test.id(), detail.replace(str(project), '<project>')) for test,detail in r.failures],'errors':[(test.id(), detail.replace(str(project), '<project>')) for test,detail in r.errors]"
    if raw_worker.count(old) != 1:
        raise ValueError('worker summary changed')
    worker.write_text(raw_worker.replace(old, extension))
    results = {}
    for label in ('control', 'combined'):
        project = Path(info['private_parent'])/('head-differential-'+label)
        skill = four_patch.copy_code(project)
        count = 0
        for part in ('scripts', 'precore'):
            for path in (skill/part).glob('*.py'):
                rel = str(path.relative_to(project))
                raw = state.git(ROOT, 'show', targets['base_head']+':'+rel)
                if label == 'combined' and rel in TARGETS:
                    raw = transform(raw, path.name)
                    if digest(raw) != targets['index'][rel]:
                        raise ValueError('HEAD-derived index variant differs')
                path.write_bytes(raw); count += 1
        if count != 76:
            raise ValueError('HEAD source closure changed')
        shutil.copytree(ROOT/'tests', project/'tests', ignore=shutil.ignore_patterns('__pycache__'))
        committed_tests = state.git(ROOT, 'ls-tree', '-r', '--name-only', targets['base_head'], '--', 'tests').decode().splitlines()
        for rel in committed_tests:
            path = project/rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(state.git(ROOT, 'show', targets['base_head']+':'+rel))
        names = [] if label == 'control' else [n for values in FUNCTIONS.values() for n in values]
        policy = four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))'
        process = subprocess.run(['/usr/bin/sandbox-exec', '-p', policy,
            str(SKILL/'.runtime/embedding-python/bin/python'), '-I', '-B', str(worker),
            str(project), json.dumps(names), '0' if label == 'control' else '1', *tests],
            env=checks.environment(), capture_output=True, text=True, timeout=120)
        try:
            result = json.loads(process.stdout.splitlines()[-1])
        except (ValueError, IndexError):
            result = {'status': 'HARNESS_UNAVAILABLE'}
        result.update(exit_code=process.returncode, stderr=process.stderr, stdout=process.stdout)
        if result.get('tests') != 15 or result.get('skipped') != 0 or result.get('errors'):
            raise ValueError(process.stderr+process.stdout)
        results[label] = result
    control, candidate = results['control'], results['combined']
    if (control['failures'] != candidate['failures'] or control['errors'] != candidate['errors']
            or control['exit_code'] != candidate['exit_code']):
        raise ValueError('HEAD-derived candidate changed baseline failures')
    if len(control['failures']) != 2:
        raise ValueError('initial HEAD baseline changed; inspect')
    new(output, {'status': 'PASS', 'cases': results, 'executions': 30, 'unique_tests': 15,
        'qualification': 'differential only; 13 pass and the same two preexisting failures in each arm',
        'baseline_test_status': 'FAIL', 'preexisting_failures_each': 2,
        'normalized_failure_details_exactly_equal': True, 'new_candidate_failures': 0,
        'python_source': 'all 76 modules from initial HEAD, with only approved changes in candidate',
        'test_inputs': 'matching initial HEAD tracked tests',
        'nonpython_inputs': 'preserved working copies', 'network_denied': True,
        'original_writes_denied': True, 'Gemini_calls': 0, 'CURRENT_writes': 0})
    print('HEAD-derived differential PASS: 13 pass and identical 2 preexisting failures per arm', flush=True)


def index_check():
    """Exercise partial staging in a private index before touching the real index."""
    output = E/'INDEX-DRY-RUN.json'
    if output.exists():
        raise FileExistsError('never overwrite index evidence')
    targets, before = state.read(E/'TARGETS.json'), state.read(E/'BASELINE.json.gz')
    row = before['repositories'][str(ROOT)]
    if state.sha(row['index_path']) != row['index_sha256']:
        raise ValueError('original index changed')
    private = Path(state.read(E/'PRIVATE-PROJECTS.json')['private_parent'])
    index = private/'qualified.index'
    shutil.copy2(row['index_path'], index)
    env = {**os.environ, 'GIT_INDEX_FILE': str(index)}
    raw = gzip.decompress((E/'INDEX.patch.gz').read_bytes())
    if digest(raw) != targets['patches']['INDEX']['raw_sha256']:
        raise ValueError('index patch drift')
    for args in [('apply', '--cached', '--check', '-'), ('apply', '--cached', '-')]:
        subprocess.run(['git', '-C', str(ROOT), *args], input=raw, check=True, env=env)
    blobs = {}
    for rel in TARGETS:
        blob = subprocess.check_output(['git', '-C', str(ROOT), 'show', ':'+rel], env=env)
        blobs[rel] = digest(blob)
    stats = subprocess.check_output(['git', '-C', str(ROOT), 'diff', '--cached', '--numstat'], env=env).decode().splitlines()
    if blobs != targets['index'] or {r.split('\t')[2] for r in stats} != TARGETS:
        raise ValueError('private index includes unrelated changes')
    if sum(int(r.split('\t')[0]) for r in stats) != 1 or sum(int(r.split('\t')[1]) for r in stats) != 43:
        raise ValueError('index patch exceeds approved source scope')
    subprocess.run(['git', '-C', str(ROOT), 'diff', '--cached', '--check'], env=env, check=True)
    if state.sha(row['index_path']) != row['index_sha256']:
        raise ValueError('real index changed during dry run')
    new(output, {'status': 'PASS', 'private_index_blobs': blobs, 'source_added_lines': 1,
        'source_deleted_lines': 43, 'numstat': stats, 'real_index_unchanged': True,
        'original_dirty_changes_staged': False})
    print('Private partial index PASS: 1 added / 43 deleted source lines', flush=True)


def verify(output, full=False):
    before = state.read(E/'BASELINE.json.gz')
    targets = state.read(E/'TARGETS.json')
    applied = (E/'APPLICATION.json').exists()
    selected = before['files'] if full else {p: s for p, s in before['files'].items()
        if p in before['pointers'] or Path(p).is_relative_to(SKILL/'scripts')
        or Path(p).is_relative_to(SKILL/'precore') or Path(p).name in {
            'retrieval-runtime.json', 'embedding-default.json', 'embedding-runtime.lock.json'}}
    failures = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for path, actual in zip(selected, pool.map(state.stamp, selected)):
            rel = str(Path(path).relative_to(ROOT)) if Path(path).is_relative_to(ROOT) else None
            if applied and rel in TARGETS:
                good = actual.get('sha256') == targets['working'][rel] and all(
                    actual.get(k) == selected[path].get(k) for k in ('mode', 'links'))
            else:
                good = actual == selected[path]
            if not good:
                failures.append(path)
    for root, row in before['repositories'].items():
        dirty = state.status(root)
        if root == str(ROOT):
            dirty = {p: s for p, s in dirty.items() if not owned(p)
                     and not (p in TARGETS and p not in row['status'])}
        if dirty != row['status']:
            failures.append(root+':original status')
        if state.git(root, 'diff', '--cached', '--raw', '-z').decode() != row['staged']:
            failures.append(root+':staging')
        if root != str(ROOT) and (state.git(root, 'rev-parse', 'HEAD').decode().strip() != row['head']
                                  or state.sha(row['index_path']) != row['index_sha256']):
            failures.append(root+':other worktree')
    if pointers() != before['pointers']:
        failures.append('CURRENT inventory')
    for path in before['previous_absent']:
        if Path(path).exists() or Path(path).is_symlink():
            failures.append(path+':old bytecode reappeared')
    if applied:
        for rel in TARGETS:
            base = state.git(ROOT, 'show', targets['base_head']+':'+rel)
            if dirty_payload(transform(base, Path(rel).name), (ROOT/rel).read_bytes()) != targets['original_dirty_payload_sha256'][rel]:
                failures.append(rel+':dirty payload')
    result = {'status': 'FAIL' if failures else 'PASS', 'checked_paths': len(selected),
        'full': full, 'CURRENT_count': len(before['pointers']), 'failures': failures,
        'original_dirty_payload_preserved': applied, 'Gemini_calls': 0, 'CURRENT_writes': 0}
    new(output, result); print(json.dumps(result), flush=True)
    if failures:
        raise ValueError('preservation failed')


GATES = ['SMOKE-control.json', 'SMOKE-combined.json', 'HEAD-SOURCE.json',
    'INDEX-DRY-RUN.json',
    'SOURCE-operating.json', 'SOURCE-native.json', 'MANAGED-control.json',
    'MANAGED-combined.json', 'INSTALLED.json', 'HISTORY-frozen.json',
    'HISTORY-archive.json', 'HISTORY-negative.json', 'HISTORY-native-view.json']


def apply():
    if (E/'APPLICATION.json').exists() or (E/'APPLY-INTENT.json').exists():
        raise FileExistsError('application already started; inspect instead')
    if any(state.read(E/n)['status'] != 'PASS' for n in GATES):
        raise ValueError('required gate failed')
    targets = state.read(E/'TARGETS.json')
    if state.git(ROOT, 'rev-parse', 'HEAD').decode().strip() != targets['base_head'] or state.git(ROOT, 'diff', '--cached', '--name-only'):
        raise ValueError('HEAD or staging drift')
    if any(state.stamp(ROOT/rel) != original for rel, original in targets['original'].items()):
        raise ValueError('source changed during qualification')
    compressed = E/'WORKING.patch.gz'
    raw = gzip.decompress(compressed.read_bytes())
    if state.sha(compressed) != targets['patches']['WORKING']['sha256'] or digest(raw) != targets['patches']['WORKING']['raw_sha256']:
        raise ValueError('qualified patch drift')
    subprocess.run(['git', '-C', str(ROOT), 'apply', '--check', '-'], input=raw, check=True)
    new(E/'APPLY-INTENT.json', {'gate_sha256': {n: state.sha(E/n) for n in GATES},
        'raw_patch_sha256': digest(raw), 'candidate': targets['working']})
    subprocess.run(['git', '-C', str(ROOT), 'apply', '-'], input=raw, check=True)
    if any(state.sha(ROOT/rel) != sha for rel, sha in targets['working'].items()):
        raise ValueError('applied source differs from tested bytes')
    new(E/'APPLICATION.json', {'status': 'APPLIED_PENDING_POSTCHECKS', 'applied': targets['working'],
        'functions_removed': 5, 'function_lines_removed': 41, 'import_bindings_removed': 2,
        'source_publish_calls': 0, 'Gemini_calls': 0, 'CURRENT_writes': 0})
    print('Applied qualified five-function/two-binding working patch', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command'); parser.add_argument('--private', type=Path)
    parser.add_argument('--output', type=Path); parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    if args.command == 'prepare':
        prepare(args.private)
    elif args.command in checks.GROUPS:
        source(args.command)
    elif args.command == 'verify':
        verify(args.output, args.full)
    elif args.command == 'apply':
        apply()
    elif args.command.startswith('smoke-'):
        smoke(args.command.removeprefix('smoke-'))
    elif args.command == 'head-source':
        head_source()
    elif args.command == 'index-check':
        index_check()
    else:
        delegate(args.command)
