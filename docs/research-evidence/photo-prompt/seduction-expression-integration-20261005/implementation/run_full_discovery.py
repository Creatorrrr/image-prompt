"""Run the full discovered unittest corpus, with isolated modules in four processes."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

def cases(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from cases(item)
        else:
            yield item

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--module')
    args = parser.parse_args()
    os.chdir(args.root)
    sys.path.insert(0, str(args.root))
    args.output.mkdir(parents=True, exist_ok=True)
    if args.module:
        suite = unittest.defaultTestLoader.loadTestsFromName(args.module)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        payload = {'module': args.module, 'tests_run': result.testsRun,
                   'failures': [{'id': test.id(), 'traceback': trace} for test, trace in result.failures],
                   'errors': [{'id': test.id(), 'traceback': trace} for test, trace in result.errors],
                   'skipped': [{'id': test.id(), 'reason': reason} for test, reason in result.skipped],
                   'successful': result.wasSuccessful()}
        (args.output / (args.module + '.json')).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
        return 0 if result.wasSuccessful() else 1
    discovered = unittest.defaultTestLoader.discover('tests', top_level_dir=str(args.root))
    all_cases = list(cases(discovered))
    modules = sorted({test._testMethodName if test.__class__.__module__ == 'unittest.loader'
                      and hasattr(test, '_exception') else test.__class__.__module__
                      for test in all_cases})
    (args.output / 'discovery.json').write_text(json.dumps({'test_count': len(all_cases), 'modules': modules, 'test_ids': [test.id() for test in all_cases]}, indent=2) + '\n')
    started = time.monotonic()
    def run(module):
        with (args.output / (module + '.log')).open('w') as log:
            result = subprocess.run([sys.executable, __file__, '--root', str(args.root), '--output', str(args.output), '--module', module], stdout=log, stderr=subprocess.STDOUT)
        return module, result.returncode
    completed = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run, module): module for module in modules}
        for future in as_completed(futures):
            module, code = future.result()
            completed.append({'module': module, 'exit_code': code})
            print(f'Completed {len(completed)}/{len(modules)} modules: {module} ({code})', flush=True)
    reports = [json.loads((args.output / (module + '.json')).read_text()) for module in modules]
    summary = {'full_unittest_discovery': True, 'execution': 'four isolated module processes',
               'discovered_test_count': len(all_cases), 'executed_test_count': sum(r['tests_run'] for r in reports),
               'module_count': len(modules), 'elapsed_seconds': round(time.monotonic() - started, 3),
               'failures': [r for report in reports for r in report['failures']],
               'errors': [r for report in reports for r in report['errors']],
               'skipped': [r for report in reports for r in report['skipped']]}
    summary['all_discovered_executed'] = summary['discovered_test_count'] == summary['executed_test_count']
    summary['successful'] = summary['all_discovered_executed'] and not summary['failures'] and not summary['errors']
    (args.output / 'SUMMARY.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in {'failures', 'errors', 'skipped'}}, ensure_ascii=False), flush=True)
    return 0 if summary['successful'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
