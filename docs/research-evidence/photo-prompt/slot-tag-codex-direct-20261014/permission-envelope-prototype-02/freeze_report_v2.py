"""Mechanical report/pin serialization after actual read, implementation and tests."""
from pathlib import Path
import difflib,json,hashlib,datetime
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');A=R/'permission-envelope-prototype-01';B=R/'permission-envelope-prototype-02'
def d(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def pin(p):
 b=p.read_bytes();return {'file':str(p),'raw_sha256':hashlib.sha256(b).hexdigest(),**({'canonical_sha256':d(json.loads(b))}if p.suffix=='.json'else{})}
def write(p,x):
 assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
p=B/'IMPLEMENTATION-DIFF-V2.patch';assert not p.exists();p.write_text(''.join(difflib.unified_diff((A/'envelope.py').read_text().splitlines(True),(B/'envelope.py').read_text().splitlines(True),fromfile='prototype01/envelope.py',tofile='prototype02/envelope.py')))
t=json.loads((B/'TEST-RESULTS-V2-attempt-01.json').read_text());cp=json.loads((B/'ORIGINAL-COPY-v1.json').read_text());assert all(hashlib.sha256((A/row['path']).read_bytes()).hexdigest()==row['raw_sha256']for row in cp['all_regular_files_copied_byte_identically']);assert t['success']and t['methods']==64 and t['original_scenarios']==141 and t['added_scenarios']==81
write(B/'REPORT-BUILD-FAILURE-v1.json',{'stage':'report-only heredoc before any statement executed','error':'SyntaxError: cannot assign to expression; accidental leading + before x= in report build code.','tests_previously_completed_unchanged':{'methods':64,'scenarios':222,'failures':0,'errors':0},'source_or_implementation_edits_from_failure':0,'correction':'New mechanical freeze_report_v2.py; no test-source changes or repeat runs required.'})
x={
 'schema':'permission-envelope-prototype02-report/v1','task':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'frozen_new_research_copy_for_root_independent_review',
 'original_immutable_copy':pin(B/'ORIGINAL-COPY-v1.json'),'prototype01_findings':pin(R/'permission-envelope-review11870-01/REPORT-v1.json'),
 'implementation_changes':[{'file':'envelope.py','lines':[140,156],'reason':'Pure joint property comparison delegates both actual E target/Rx unions to the frozen property primitive; no source facts or scope changes.'},{'file':'envelope.py','lines':[299,306],'reason':'Known exact/parent/child/wildcard overlap is nonwaivable by manual disjoint; aliases/ancestors/unknown separation handled by same primitive.'}],
 'actual_results':{'methods':64,'old_methods':55,'new_methods':9,'old_scenarios':141,'new_scenarios':81,'total_scenarios':222,'failures':0,'errors':0,'network_denied':True,'actual_new_frozen_B1_permission_scenarios':31,'direct_comparison_primitive_scenarios':47,'actual_B1_wildcard_fact_rejections':3},
 'regression_history':{'prototype01_original_55_141_all_passed':True,'independent_joint_false_accepts':8,'corrected_both_topologies_actual_cases':16,'prototype02_attempt01_all_passed':True,'independent_full_PR_example_snapshot_erratum':pin(R/'permission-envelope-review11870-01/SNAPSHOT-ERRATUM-v2.json'),'report_only_build_failure':pin(B/'REPORT-BUILD-FAILURE-v1.json'),'prior_failure_files_unchanged':True},
 'known_pending':t['PR_known_pending_boundary'],'actual_loaded_frozen_modules':t['actual_loaded_modules'],
 'artifacts':[pin(B/n)for n in ['SPEC-V2.md','envelope.py','fixtures.py','test_envelope.py','test_joint_paths_v2.py','run_tests_v2.py','TEST-RESULTS-V2-attempt-01.json','IMPLEMENTATION-DIFF-V2.patch','REPORT-V2.md','freeze_report_v2.py']],
 'read_boundary':'Original whole SPEC/envelope305/fixtures137/tests299 and current1299/design directly read; new complete helper/test/spec authored and reviewed. Frozen exact property primitive source and witness fact grammar actually read. All unchanged copied bytes losslessly reused, not counted as extra semantic review.',
 'source_E_P_PR_modes_operation_values_Rx_guards_ownbinding_closure_unchanged':True,'same_actual_B1_view_no_second_resolution':True,'new_shadow_effects_or_global_substring_aliases':False,
 'source1299_native_qualified':False,'B2_fullcompact_consumer_cache_publication_final_state_PR_or_operating_integrated':False,'native_proof_signature_or_rootapproval_count':0,'production_source_Git_model_network_changes':0,'bulk_frozen_count':130,'bulk_next':1630}
q=B/'REPORT-V2.json';write(q,x);print('REPORT canonical',d(x),'raw',hashlib.sha256(q.read_bytes()).hexdigest());print('envelope raw',hashlib.sha256((B/'envelope.py').read_bytes()).hexdigest())
