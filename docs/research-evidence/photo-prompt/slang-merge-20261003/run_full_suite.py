"""Run every discovered unittest module in disjoint processes with live results."""
from __future__ import annotations
import argparse
import ast
import concurrent.futures
from collections import Counter
import hashlib
import json
import subprocess
import sys
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def source_binding():
    paths = []
    for skill in ('photo-prompt-image-generator', 'subculture-illustration-image-generator'):
        directory = ROOT / 'skills' / skill
        paths += sorted((directory / 'assets').glob('*.json'))
        paths += sorted((directory / 'scripts').glob('*.py'))
    paths += sorted((ROOT / 'skills/photo-prompt-image-generator/precore').glob('*.json'))
    paths += sorted((ROOT / 'skills/photo-prompt-image-generator/precore').glob('*.py'))
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def test_ids(suite):
    return [item.id() for item in suite] if not any(isinstance(item, unittest.TestSuite) for item in suite) else [
        value for item in suite for value in (test_ids(item) if isinstance(item, unittest.TestSuite) else [item.id()])]


def worker(number, modules, output_dir):
    sys.path.insert(0, str(ROOT))
    binding = source_binding()
    suite = unittest.TestLoader().loadTestsFromNames(modules)
    discovered_ids = test_ids(suite)
    executed_ids = []
    path = output_dir / f'full-suite-worker-{number}.json'
    started = time.time()

    class Result(unittest.TextTestResult):
        def startTest(self, test):
            executed_ids.append(test.id())
            super().startTest(test)

        def stopTest(self, test):
            super().stopTest(test)
            path.write_text(json.dumps({
                'modules': modules, 'tests_run': self.testsRun,
                'failures': [{'test': str(t), 'traceback': text} for t, text in self.failures],
                'errors': [{'test': str(t), 'traceback': text} for t, text in self.errors],
                'skipped': [{'test': str(t), 'reason': text} for t, text in self.skipped],
                'elapsed_seconds': round(time.time() - started, 3),
                'complete': False, 'source_binding': binding,
                'discovered_ids': discovered_ids, 'executed_ids': executed_ids,
                'test_module_hashes': {module: hashlib.sha256(
                    (ROOT / (module.replace('.', '/') + '.py')).read_bytes()).hexdigest()
                    for module in modules}}, ensure_ascii=False, indent=2) + '\n')

    result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(suite)
    data = json.loads(path.read_text()); data['complete'] = True
    data['all_discovered_tests_executed_once'] = Counter(discovered_ids) == Counter(executed_ids) and len(executed_ids) == len(set(executed_ids))
    data['sources_unchanged'] = source_binding() == binding
    data['successful'] = result.wasSuccessful() and data['all_discovered_tests_executed_once'] and data['sources_unchanged']
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return int(not data['successful'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', type=int)
    parser.add_argument('--run-name', default='')
    parser.add_argument('modules', nargs='*')
    args = parser.parse_args()
    if args.run_name and not args.run_name.replace('-', '').isalnum():
        raise ValueError('Invalid run directory name')
    output_dir = HERE / args.run_name if args.run_name else HERE
    output_dir.mkdir(exist_ok=True)
    if args.worker is not None:
        return worker(args.worker, args.modules, output_dir)
    binding = source_binding()
    (output_dir / 'SOURCE-BINDING.json').write_text(json.dumps(binding, ensure_ascii=False, indent=2) + '\n')
    discovered = []
    for file in sorted((ROOT / 'tests').glob('test*.py')):
        count = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith('test_') for n in ast.walk(ast.parse(file.read_text())))
        source = file.read_text()
        estimate = count + 30 * sum(source.count(pattern) for pattern in ('run_current(', 'generate_current(', 'current_bundle(', 'run_current_v6('))
        discovered.append((estimate, count, f'tests.{file.stem}'))
    # Module-sized jobs balance expensive complete pack replays without
    # repeating their class setup for every individual test case.
    groups = [[module] for estimate, count, module in sorted(discovered, reverse=True)]
    print(json.dumps({'modules': len(discovered), 'authored_test_methods': sum(x[1] for x in discovered), 'workers': 6}), flush=True)

    def invoke(pair):
        index, modules = pair
        with (output_dir / f'full-suite-worker-{index}.log').open('w') as log:
            return subprocess.run([sys.executable, str(Path(__file__).resolve()), '--run-name', args.run_name, '--worker', str(index), *modules], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT).returncode
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        return_codes = list(pool.map(invoke, enumerate(groups)))
    results = [json.loads((output_dir / f'full-suite-worker-{i}.json').read_text()) for i in range(len(groups))]
    ids = [test_id for row in results for test_id in row['executed_ids']]
    sources_match = source_binding() == binding and all(row['source_binding'] == binding for row in results)
    output = {'schema_version': 'photo-merge-full-suite-result/v2', 'modules': len(discovered),
        'tests_run': sum(x['tests_run'] for x in results),
        'failures': [item for x in results for item in x['failures']],
        'errors': [item for x in results for item in x['errors']],
        'skipped': [item for x in results for item in x['skipped']],
        'complete': all(x['complete'] for x in results), 'return_codes': return_codes,
        'successful': all(x['successful'] for x in results) and sources_match and len(ids) == len(set(ids)),
        'sources_unchanged': sources_match,
        'all_discovered_tests_executed_once': all(x['all_discovered_tests_executed_once'] for x in results) and len(ids) == len(set(ids)),
        'executed_test_ids': ids,
        'source_binding': binding}
    (output_dir / 'FULL-SUITE-RESULT.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: len(v) if isinstance(v, list) else v for k, v in output.items()}), flush=True)
    return int(not output['successful'])


if __name__ == '__main__': raise SystemExit(main())
