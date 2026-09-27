"""Run every discovered unittest module in four disjoint, recorded groups."""
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / 'integration'
sys.path.insert(0, str(ROOT))

def main():
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / 'tests'))
    if loader.errors:
        result = {'schema_version': 'portrait-composition-full-suite/v1',
                  'status': 'collection_failed', 'full_suite_completed': False,
                  'collection_errors': loader.errors}
        (OUT / 'full-suite-results.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({'status': result['status'], 'collection_error_count': len(loader.errors)}), flush=True)
        return 1
    modules = {}
    def visit(item):
        if isinstance(item, unittest.TestSuite):
            for child in item:
                visit(child)
        else:
            name = item.id().rsplit('.', 2)[0]
            modules[name] = modules.get(name, 0) + item.countTestCases()
    visit(suite)
    groups = [{'modules': [], 'expected_tests': 0} for _ in range(4)]
    for name, count in sorted(modules.items(), key=lambda row: (-row[1], row[0])):
        group = min(groups, key=lambda row: row['expected_tests'])
        group['modules'].append(name)
        group['expected_tests'] += count
    processes = []
    for number, group in enumerate(groups, 1):
        log = OUT / f'full-suite-group-{number}.log'
        stream = log.open('w')
        argv = [sys.executable, '-m', 'unittest', *['tests.' + name for name in group['modules']], '-v']
        process = subprocess.Popen(argv, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
        processes.append((process, stream, log, group))
    results = []
    for number, (process, stream, log, group) in enumerate(processes, 1):
        code = process.wait()
        stream.close()
        text = log.read_text()
        found = re.search(r'Ran (\d+) tests? in ([\d.]+)s', text)
        actual = int(found.group(1)) if found else None
        row = {'group': number, **group, 'actual_tests': actual, 'exit_code': code,
               'status': 'pass' if code == 0 and actual == group['expected_tests'] else 'fail',
               'log': str(log.relative_to(ROOT))}
        results.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != 'modules'}), flush=True)
    result = {'schema_version': 'portrait-composition-full-suite/v1',
              'discovered_modules': len(modules), 'expected_tests': suite.countTestCases(),
              'actual_tests': sum(row['actual_tests'] or 0 for row in results),
              'status': 'pass' if all(row['status'] == 'pass' for row in results) else 'fail', 'groups': results}
    (OUT / 'full-suite-results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'groups'}), flush=True)
    return 0 if result['status'] == 'pass' else 1

if __name__ == '__main__':
    raise SystemExit(main())
