"""Run every discovered unittest module in disjoint processes with live results."""
from __future__ import annotations
import argparse
import ast
import concurrent.futures
import json
import subprocess
import sys
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def worker(number, modules, output_dir):
    sys.path.insert(0, str(ROOT))
    suite = unittest.TestLoader().loadTestsFromNames(modules)
    path = output_dir / f'full-suite-worker-{number}.json'
    started = time.time()

    class Result(unittest.TextTestResult):
        def stopTest(self, test):
            super().stopTest(test)
            path.write_text(json.dumps({
                'modules': modules, 'tests_run': self.testsRun,
                'failures': [{'test': str(t), 'traceback': text} for t, text in self.failures],
                'errors': [{'test': str(t), 'traceback': text} for t, text in self.errors],
                'skipped': [{'test': str(t), 'reason': text} for t, text in self.skipped],
                'elapsed_seconds': round(time.time() - started, 3),
                'complete': False}, ensure_ascii=False, indent=2) + '\n')

    result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(suite)
    data = json.loads(path.read_text()); data['complete'] = True
    data['successful'] = result.wasSuccessful()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    return int(not result.wasSuccessful())


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
    output = {'schema_version': 'photo-full-suite-result/v1', 'modules': len(discovered),
        'tests_run': sum(x['tests_run'] for x in results),
        'failures': [item for x in results for item in x['failures']],
        'errors': [item for x in results for item in x['errors']],
        'skipped': [item for x in results for item in x['skipped']],
        'complete': all(x['complete'] for x in results), 'return_codes': return_codes,
        'successful': all(x['successful'] for x in results)}
    (output_dir / 'FULL-SUITE-RESULT.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: len(v) if isinstance(v, list) else v for k, v in output.items()}), flush=True)
    return int(not output['successful'])


if __name__ == '__main__': raise SystemExit(main())
