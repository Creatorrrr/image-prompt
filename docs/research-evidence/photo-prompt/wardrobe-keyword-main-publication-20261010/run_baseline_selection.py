"""Replay actual failing test selections on a clean fetched-main checkout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import unittest

parser=argparse.ArgumentParser()
parser.add_argument('--source-root',type=Path,required=True)
parser.add_argument('--selection',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
root=args.source_root.resolve(); names=json.loads(args.selection.read_text())
sys.path.insert(0,str(root)); os.chdir(root)
loader=unittest.TestLoader(); suite=loader.loadTestsFromNames(names)
began=time.perf_counter(); result=unittest.TextTestRunner(stream=sys.stdout,verbosity=2).run(suite)
report={'schema_version':'wardrobe-publication-clean-main-failure-replay/v1','source_root':str(root),
        'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'selections':names,'tests_run':result.testsRun,'seconds':time.perf_counter()-began,
        'status':'PASS' if result.wasSuccessful() else 'FAIL',
        'failures':[{'id':test.id(),'traceback':trace} for test,trace in result.failures],
        'errors':[{'id':test.id(),'traceback':trace} for test,trace in result.errors],
        'skipped':[{'id':test.id(),'reason':reason} for test,reason in result.skipped],
        'discovery_errors':loader.errors}
args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'seconds':report['seconds']}),flush=True)
raise SystemExit(0 if result.wasSuccessful() else 1)
