"""Run every unittest-discovered case in isolated, bounded process batches."""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import subprocess
import sys
import time
import unittest
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).parent/'full-suite-parallel'


def flatten(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):yield from flatten(item)
        else:yield item


def run_batch(batch):
    number,ids=batch;started=time.monotonic()
    try:
        result=subprocess.run([sys.executable,'-m','unittest',*ids],cwd=ROOT,text=True,capture_output=True,timeout=900)
        output=result.stdout+result.stderr;returncode=result.returncode
    except subprocess.TimeoutExpired as exc:
        output='Batch exceeded 900 seconds.\n'+str(exc.stdout or '')+str(exc.stderr or '');returncode=124
    p=OUT/f'batch-{number:03d}.log';p.write_text(output)
    match=re.search(r'Ran (\d+) tests? in ([\d.]+)s',output)
    return {'batch':number,'test_ids':ids,'returncode':returncode,'tests_run':int(match.group(1)) if match else 0,'wall_seconds':round(time.monotonic()-started,3),'log':str(p.relative_to(ROOT)),'log_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'PASS' if returncode==0 else 'FAIL'}


def main():
    OUT.mkdir(exist_ok=True)
    sys.path.insert(0,str(ROOT))
    loader=unittest.TestLoader();suite=loader.discover(str(ROOT/'tests'),top_level_dir=str(ROOT))
    if loader.errors:raise RuntimeError('\n'.join(loader.errors))
    ids=[case.id() for case in flatten(suite)]
    if len(ids)!=len(set(ids)):raise RuntimeError('duplicate discovered test IDs')
    groups=defaultdict(list)
    for case_id in ids:groups[case_id.rsplit('.',1)[0]].append(case_id)
    batches=[]
    for class_ids in groups.values():
        for start in range(0,len(class_ids),4):batches.append((len(batches),class_ids[start:start+4]))
    discovery={'method':'unittest.TestLoader.discover','top_level_dir':str(ROOT),'start_dir':str(ROOT/'tests'),'discovered_test_count':len(ids),'test_ids':ids,'batch_size_maximum':4,'workers':6,'runtime_manifest':'../OPERATIONAL-INPUTS.json'}
    (OUT/'DISCOVERY.json').write_text(json.dumps(discovery,indent=2)+'\n')
    print(f'Discovered {len(ids)} tests in {len(batches)} isolated batches.',flush=True)
    results=[];started=time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures=[pool.submit(run_batch,batch) for batch in batches]
        for future in concurrent.futures.as_completed(futures):
            result=future.result();results.append(result)
            if len(results)%10==0 or result['status']=='FAIL':print(f"Completed {len(results)}/{len(batches)} batches; failures {sum(r['status']=='FAIL' for r in results)}.",flush=True)
    results.sort(key=lambda r:r['batch'])
    report={'method':'complete unittest discovery with isolated subprocess batches','discovered_test_count':len(ids),'tests_run':sum(r['tests_run'] for r in results),'batch_count':len(batches),'failed_batch_count':sum(r['status']=='FAIL' for r in results),'wall_seconds':round(time.monotonic()-started,3),'all_discovered_ids_executed':sorted(x for r in results for x in r['test_ids'])==sorted(ids),'batches':results}
    report['status']='PASS' if report['failed_batch_count']==0 and report['tests_run']==len(ids) and report['all_discovered_ids_executed'] else 'FAIL'
    (OUT/'RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='batches'}),flush=True)
    return 0 if report['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
