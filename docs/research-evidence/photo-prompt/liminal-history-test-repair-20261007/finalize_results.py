from pathlib import Path
import hashlib,json,re,shutil,datetime
ROOT=Path.cwd()
OUT=ROOT/'docs/research-evidence/photo-prompt/liminal-history-test-repair-20261007'
WORK=Path('/Users/chasoik/.codex/worktrees/vel-appearance-integration/image-prompt')
def cases(name):
 text=(OUT/name).read_text()
 assert re.search(r'Ran \d+ tests? in ',text),name
 records={}
 for match in re.finditer(r'^(test_\w+) \(([^)]+)\) \.\.\. (ok|ERROR|FAIL)$',text,re.M):
  key=match.group(2)
  if not key.endswith('.'+match.group(1)):key+='.'+match.group(1)
  records[key]=match.group(3)
 return records
batch_path = OUT/'RELATED-BATCH-RESULTS.json'
batch=json.loads((batch_path if batch_path.exists() else OUT/'TEST-RESULTS.json').read_text())
metadata='tests.test_photo_candidate_semantics.PhotoCandidateSemanticsTests.test_maintenance_prose_is_external_and_hash_bound'
assert batch['tests_run']==159
assert batch['failing_ids']==[metadata],batch
if not batch_path.exists():
 shutil.copy2(OUT/'TEST-RESULTS.json',batch_path)
combined=cases('related-tests.log')
assert len(combined)==159
targeted=cases('final-targeted-tests.log')
owners=cases('owning-integration-tests.log')
assert len(targeted)==12 and all(v=='ok' for v in targeted.values())
assert len(owners)==25 and all(v=='ok' for v in owners.values())
combined.update(targeted)
combined.update(owners)
assert all(v=='ok' for v in combined.values()),combined
shutil.copy2('/tmp/vel-liminal-worktree-fixed.log',OUT/'worktree-liminal-tests.log')
worktree=cases('worktree-liminal-tests.log')
assert len(worktree)==11 and all(v=='ok' for v in worktree.values())
before=json.loads((OUT/'PRIMARY-BEFORE.json').read_text())['protected_paths_sha256']
owned={'tests/test_photo_liminal_active_use_korean_data_cleanup.py','tests/test_photo_candidate_semantics.py'}
assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in before.items() if name not in owned)
report={'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'unique_primary_final_results':len(combined),'passed':len(combined),'failed':0,'errors':0,'full_suite_run':False,'batch_before_maintenance_chain_fix':batch,'after_fix_targeted_rerun':{'tests':12,'passed':12},'owning_integration_suites':{'tests':25,'passed':25},'isolated_worktree_liminal_suite':{'tests':11,'passed':11},'aggregation':'Final observed status per test ID; the one old maintenance test error was corrected and rerun, the full 159 batch was not repeated.','runtime_data_or_index_changes':False,'owned_test_paths':sorted(owned),'final_test_status_by_id':dict(sorted(combined.items()))}
(OUT/'TEST-RESULTS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['unique_primary_final_results','passed','failed','errors','full_suite_run']},ensure_ascii=False))
