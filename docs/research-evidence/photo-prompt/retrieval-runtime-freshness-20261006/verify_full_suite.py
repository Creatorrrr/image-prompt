"""Run all discovered tests by file in isolated workers and retain diagnostics."""
from __future__ import annotations
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite): yield from flatten(item)
        else: yield item


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--directory',type=Path,required=True)
    parser.add_argument('--worker');parser.add_argument('--jobs',type=int,default=4);args=parser.parse_args()
    sys.path.insert(0,str(Path.cwd()));sys.path.insert(0,str(Path.cwd() / 'tests'));args.directory.mkdir(parents=True,exist_ok=True)
    if args.worker:
        start=time.perf_counter()
        suite=unittest.defaultTestLoader.loadTestsFromName('tests.'+args.worker)
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        record={'module':args.worker,'tests':result.testsRun,'seconds':time.perf_counter()-start,
                'failures':[{'id':test.id(),'traceback':trace} for test,trace in result.failures],
                'errors':[{'id':test.id(),'traceback':trace} for test,trace in result.errors],
                'skips':[{'id':test.id(),'reason':reason} for test,reason in result.skipped]}
        (args.directory/(args.worker+'.json')).write_text(json.dumps(record,indent=2)+'\n')
        return
    suite=unittest.defaultTestLoader.discover('tests',pattern='test*.py')
    tests=list(flatten(suite));modules=sorted({test.id().split('.')[0] for test in tests})
    (args.directory/'DISCOVERY.json').write_text(json.dumps({'test_count':len(tests),'modules':modules},indent=2)+'\n')
    environment={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','GEMINI_API_KEY':'','GOOGLE_API_KEY':'','OPENAI_API_KEY':''}
    def execute(module):
        with (args.directory/(module+'.log')).open('w') as stream:
            process=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--directory',str(args.directory.resolve()),'--worker',module],
                cwd=Path.cwd(),env=environment,stdout=stream,stderr=subprocess.STDOUT)
        path=args.directory/(module+'.json')
        return json.loads(path.read_text()) if path.exists() else {'module':module,'tests':0,'errors':[{'id':module,'traceback':f'worker exit {process.returncode}; see log'}],'failures':[],'skips':[]}
    start=time.perf_counter();completed=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures={pool.submit(execute,module):module for module in modules}
        for future in concurrent.futures.as_completed(futures):
            record=future.result();completed.append(record)
            print(json.dumps({'done':len(completed),'of':len(modules),'module':record['module'],'tests':record['tests'],'failures':len(record['failures']),'errors':len(record['errors'])}),flush=True)
            progress={'schema':'photo-full-file-isolated-regression/v1','planned_tests':len(tests),'completed_modules':len(completed),
                'module_count':len(modules),'tests':sum(row['tests'] for row in completed),'seconds':time.perf_counter()-start,
                'complete':len(completed)==len(modules),'results':sorted(completed,key=lambda row:row['module']),
                'proof_boundary':'Every discovered file is run in a fresh interpreter. No claim that the single-process order is free of pre-existing global patch contamination.'}
            temporary=args.directory/'PROGRESS.tmp';temporary.write_text(json.dumps(progress,indent=2)+'\n');temporary.replace(args.directory/'RESULTS.json')


if __name__=='__main__':main()
