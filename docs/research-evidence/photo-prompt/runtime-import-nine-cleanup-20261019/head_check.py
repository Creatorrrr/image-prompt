"""Compare the exact committed Python variant without including existing dirty fixes."""
from pathlib import Path
import shutil
import sys

ROOT = Path('/Users/chasoik/Projects/image-prompt')
sys.path.insert(0, str(ROOT/'tools/photo_runtime_maintenance'))
import imports_cleanup as scope
from history_state import new

output = scope.E/'HEAD-COMPARISON.json'
if output.exists():
    raise FileExistsError('never overwrite completed evidence')
info = scope.state.read(scope.E/'PRIVATE-PROJECTS.json')
targets = scope.state.read(scope.E/'TARGETS.json')
tests = ['tests.test_photo_bm25f_retrieval', 'tests.test_photo_contextual_source_effects',
         'tests.test_photo_workflow_precore', 'tests.test_photo_precore_feature_selection']
results = {}
for label in ('control', 'combined'):
    project = Path(info['private_parent'])/('head-'+label)
    skill = scope.four_patch.copy_code(project)
    for part in ('scripts', 'precore'):
        for path in (skill/part).glob('*.py'):
            rel = str(path.relative_to(project))
            raw = scope.state.git(ROOT, 'show', targets['base_head']+':'+rel)
            if label == 'combined' and rel in scope.TARGETS:
                raw = scope.transform(raw, path.stem)
                if __import__('hashlib').sha256(raw).hexdigest() != targets['candidate'][rel]:
                    raise ValueError('committed source differs from qualified candidate')
            path.write_bytes(raw)
    shutil.copytree(ROOT/'tests', project/'tests', ignore=shutil.ignore_patterns('__pycache__'))
    for rel in scope.state.git(ROOT, 'ls-tree', '-r', '--name-only', targets['base_head'], '--', 'tests').decode().splitlines():
        path = project/rel; path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(scope.state.git(ROOT, 'show', targets['base_head']+':'+rel))
    policy = scope.four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))'
    result = scope.worker(project, label == 'combined', tests, policy, 180)
    if result.get('tests') != 35 or result.get('skipped') != 0 or result.get('errors'):
        raise ValueError(result.get('stderr', '')+result.get('stdout', ''))
    results[label] = result
    print('HEAD', label, 'tests', result['tests'], 'existing failures', len(result['failures']), flush=True)
control, candidate = results['control'], results['combined']
if control['failures'] != candidate['failures'] or control['errors'] != candidate['errors'] or control['exit_code'] != candidate['exit_code']:
    raise ValueError('new committed-source regression')
if len(control['failures']) != 2:
    raise ValueError('preexisting HEAD baseline changed; inspect')
new(output, {'status': 'PASS', 'qualification': 'Differential only: 33 pass and identical 2 preexisting failures per arm',
    'baseline_test_status': 'FAIL', 'cases': results, 'tests_each': 35, 'preexisting_failures_each': 2,
    'new_candidate_failures': 0, 'normalized_failure_details_exactly_equal': True,
    'source_and_tracked_tests_from': targets['base_head'], 'nonpython_inputs': 'preserved working copies',
    'original_writes_denied': True, 'network_denied': True, 'Gemini_calls': 0, 'CURRENT_writes': 0})
