"""Retain the initial complete run and append targeted rechecks after fixes."""
from __future__ import annotations
import concurrent.futures
import json
from pathlib import Path
import run_full_suite as runner

HERE=Path(__file__).resolve().parent

def main():
    initial=json.loads((HERE/'full-suite-parallel/RESULTS.json').read_text())
    runner.OUT=HERE/'full-suite-rechecks';runner.OUT.mkdir(exist_ok=True)
    failed=[row for row in initial['batches'] if row['status']!='PASS']
    results=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures=[pool.submit(runner.run_batch,(row['batch'],row['test_ids'])) for row in failed]
        for future in concurrent.futures.as_completed(futures):
            result=future.result();results.append(result)
            print(f"Rechecked batch {result['batch']}: {result['status']}",flush=True)
    results.sort(key=lambda row:row['batch'])
    indexed={row['batch']:row for row in results}
    final=[indexed.get(row['batch'],row) for row in initial['batches']]
    failure_count=sum(row['status']!='PASS' for row in final)
    report={'method':'complete unittest discovery plus targeted failed-batch rechecks','initial_result':'full-suite-parallel/RESULTS.json','initial_status':initial['status'],'initial_failed_batch_count':initial['failed_batch_count'],'discovered_test_count':initial['discovered_test_count'],'all_discovered_ids_executed':initial['all_discovered_ids_executed'],'final_tests_accounted_for':sum(row['tests_run'] for row in final),'recheck_test_count':sum(row['tests_run'] for row in results),'remaining_failed_batch_count':failure_count,'rechecks':results,'status':'PASS' if failure_count==0 and sum(row['tests_run'] for row in final)==initial['discovered_test_count'] else 'FAIL','corrections':['Historical projections exclude the later neutral extension; original historical inputs remain intact.','Preservation checks admit only recorded equivalent paraphrase additions; definitions effects guards and gates remain exact.','Current sibling baseline refreshed only at SHA and pack ID after whole-pack provenance-only comparison; V1-V4 remain unchanged.']}
    (HERE/'FULL-SUITE-FINAL.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='rechecks'},ensure_ascii=False),flush=True)
    return 0 if report['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
