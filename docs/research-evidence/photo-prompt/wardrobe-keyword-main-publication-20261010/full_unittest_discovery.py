"""Run the entire ordinary unittest discovery in isolated module-group workers.

No production auditor, fixture or test method is replaced. The complete discovered
ID inventory and worker assignments are retained for coverage reconciliation.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def flatten(suite):
    for value in suite:
        if isinstance(value, unittest.TestSuite):
            yield from flatten(value)
        else:
            yield value


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def discover():
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / 'tests'), pattern='test*.py', top_level_dir=str(ROOT))
    return list(flatten(suite)), loader.errors


def run_worker(assignment, output):
    selected = set(json.loads(assignment.read_text()))
    tests, discovery_errors = discover()
    chosen = [test for test in tests if test.id() in selected]
    assert {test.id() for test in chosen} == selected, 'worker discovery inventory drift'
    events = (output / (assignment.stem + '-events.jsonl')).open('w')
    started = []

    class RecordedResult(unittest.TextTestResult):
        def startTest(self, test):
            self.started_at = time.perf_counter()
            started.append(test.id())
            events.write(json.dumps({'event': 'start', 'id': test.id(), 'time': time.time()}) + '\n')
            events.flush()
            super().startTest(test)

        def stopTest(self, test):
            super().stopTest(test)
            events.write(json.dumps({'event': 'stop', 'id': test.id(), 'seconds': time.perf_counter() - self.started_at}) + '\n')
            events.flush()

    began = time.perf_counter()
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2, resultclass=RecordedResult).run(unittest.TestSuite(chosen))
    events.close()
    report = {'status': 'PASS' if result.wasSuccessful() else 'FAIL', 'selected_ids': sorted(selected),
              'started_ids': started, 'tests_run': result.testsRun, 'seconds': time.perf_counter() - began,
              'failures': [{'id': test.id(), 'traceback': trace} for test, trace in result.failures],
              'errors': [{'id': test.id(), 'traceback': trace} for test, trace in result.errors],
              'skipped': [{'id': test.id(), 'reason': reason} for test, reason in result.skipped],
              'expected_failures': [test.id() for test, _ in result.expectedFailures],
              'unexpected_successes': [test.id() for test in result.unexpectedSuccesses],
              'discovery_errors': discovery_errors}
    write_json(output / (assignment.stem + '-result.json'), report)
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=6)
    parser.add_argument('--worker-assignment', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.worker_assignment:
        return run_worker(args.worker_assignment, args.output)
    tests, discovery_errors = discover()
    ids = [test.id() for test in tests]
    assert len(ids) == len(set(ids)), 'duplicate discovered test IDs'
    groups = {}
    for test in tests:
        groups.setdefault(test.__class__.__module__, []).append(test.id())
    buckets, loads = [[] for _ in range(args.workers)], [0] * args.workers
    for module, values in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        bucket = min(range(args.workers), key=lambda number: loads[number])
        buckets[bucket].extend(values)
        loads[bucket] += len(values)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    write_json(args.output / 'DISCOVERED-INVENTORY.json', {'source_commit': revision, 'tests': ids,
        'count': len(ids), 'workers': args.workers, 'assignment_counts': loads, 'discovery_errors': discovery_errors})
    assignments = []
    for number, values in enumerate(buckets):
        path = args.output / f'worker-{number + 1:02d}.json'
        write_json(path, values)
        assignments.append(path)
    began = time.perf_counter()

    def launch(path):
        environment = dict(os.environ)
        environment['PYTHONDONTWRITEBYTECODE'] = '1'
        # Runtime stores are private worker artifacts outside the Git checkout.
        cache = Path.home() / '.cache/image-prompt/wardrobe-main-publication-20261010/full-tests' / path.stem
        environment['PHOTO_RUNTIME_STORE'] = str(cache)
        with (args.output / (path.stem + '.log')).open('w') as log:
            completed = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--output', str(args.output),
                '--worker-assignment', str(path)], cwd=ROOT, env=environment, stdout=log, stderr=subprocess.STDOUT)
        return {'assignment': path.name, 'exit_code': completed.returncode}

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        outcomes = list(executor.map(launch, assignments))
    reports = [json.loads((args.output / (path.stem + '-result.json')).read_text()) for path in assignments]
    assigned = [value for report in reports for value in report['selected_ids']]
    assert len(assigned) == len(set(assigned)) and set(assigned) == set(ids), 'full inventory not covered exactly once'
    failures = [failure for report in reports for failure in report['failures']]
    errors = [error for report in reports for error in report['errors']]
    result = {'schema_version': 'wardrobe-publication-full-unittest-discovery/v1',
        'status': 'PASS' if all(report['status'] == 'PASS' for report in reports) else 'FAIL',
        'source_commit': revision, 'discovered_tests': len(ids), 'tests_run': sum(report['tests_run'] for report in reports),
        'discovery_complete': True, 'every_discovered_id_assigned_exactly_once': True,
        'workers': args.workers, 'outcomes': outcomes, 'seconds': time.perf_counter() - began,
        'failures': failures, 'errors': errors, 'skipped': [row for report in reports for row in report['skipped']],
        'expected_failures': [row for report in reports for row in report['expected_failures']],
        'unexpected_successes': [row for report in reports for row in report['unexpected_successes']],
        'boundary': 'Ordinary discovered tests and their original assertions, run in independent module groups; no live embedding or image-generation run is part of this validation.'}
    write_json(args.output / 'FULL-RESULT.json', result)
    print(json.dumps({key: result[key] for key in ['status', 'discovered_tests', 'tests_run', 'seconds']}), flush=True)
    print(json.dumps({'failures': len(failures), 'errors': len(errors), 'skipped': len(result['skipped'])}), flush=True)
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
