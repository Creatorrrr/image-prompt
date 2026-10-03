#!/usr/bin/env python3
"""Execute every discovered unittest case in reproducible process partitions."""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path


def flat(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flat(item)
        else:
            yield item


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--workers', type=int, default=4)
    p.add_argument('--partition-by', choices=('module', 'test'), default='module')
    p.add_argument('--worker-index', type=int)
    p.add_argument('--modules-json')
    args = p.parse_args()
    root = Path(args.root).resolve(); out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.worker_index is None:
        start = time.monotonic()
        children = []
        for i in range(args.workers):
            cmd = [sys.executable, str(Path(__file__).resolve()), '--root', str(root), '--output', str(out),
                   '--workers', str(args.workers), '--worker-index', str(i), '--partition-by', args.partition_by]
            if args.modules_json:
                cmd += ['--modules-json', str(Path(args.modules_json).resolve())]
            log = (out / f'worker-{i}.log').open('w')
            children.append((subprocess.Popen(cmd, cwd=root, stdout=log, stderr=subprocess.STDOUT), log))
        for proc, log in children:
            proc.wait(); log.close()
        rows = [json.loads((out / f'worker-{i}.json').read_text()) for i in range(args.workers)]
        ids = [x for row in rows for x in row['test_ids']]
        summary = {'runner': f'unittest.TestLoader.discover; complete {args.partition_by} partitions',
                   'root': str(root), 'workers': args.workers, 'elapsed_seconds': round(time.monotonic() - start, 3),
                   'discovered_count': len(ids), 'tests_run': sum(row['tests_run'] for row in rows),
                   'failure_ids': [x for row in rows for x in row['failure_ids']],
                   'error_ids': [x for row in rows for x in row['error_ids']],
                   'skipped_ids': [x for row in rows for x in row['skipped_ids']],
                   'unexpected_success_ids': [x for row in rows for x in row['unexpected_success_ids']],
                   'discovery_sha256': hashlib.sha256(json.dumps(sorted(ids)).encode()).hexdigest(),
                   'successful': all(row['successful'] for row in rows)}
        write(out / 'SUMMARY.json', summary)
        print(json.dumps({k: v for k, v in summary.items() if not k.endswith('_ids')}, ensure_ascii=False), flush=True)
        if not summary['successful']:
            raise SystemExit(1)
        return
    os.chdir(root)
    sys.path.insert(0, str(root))
    all_cases = list(flat(unittest.TestLoader().discover(str(root / 'tests'), top_level_dir=str(root))))
    modules = set(json.loads(Path(args.modules_json).read_text())) if args.modules_json else None
    cases = [case for case in all_cases if (modules is None or case.__class__.__module__ in modules)
             and int(hashlib.sha256((case.id() if args.partition_by == 'test' else case.__class__.__module__).encode()).hexdigest(), 16) % args.workers == args.worker_index]
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(cases))
    record = {'test_ids': [case.id() for case in cases], 'tests_run': result.testsRun,
              'failure_ids': [case.id() for case, _ in result.failures], 'error_ids': [case.id() for case, _ in result.errors],
              'skipped_ids': [case.id() for case, _ in result.skipped],
              'unexpected_success_ids': [case.id() for case in result.unexpectedSuccesses],
              'successful': result.wasSuccessful()}
    write(out / f'worker-{args.worker_index}.json', record)


if __name__ == '__main__':
    main()
