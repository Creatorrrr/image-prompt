"""Reproducible immutable research-only execution report. No legacy overwrite."""
import sys,json,hashlib,unittest,io,datetime,dataclasses
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent
sys.path.insert(0,str(P))
import test_envelope as original
import test_joint_paths_v2 as added
from envelope import compare,bind_source,digest,IndependentPins
from fixtures import contract,PRIMITIVES
attempt=sys.argv[1]if len(sys.argv)>1 else'01'
out=P/('TEST-RESULTS-V2-attempt-'+attempt+'.json');assert not out.exists()
stream=io.StringIO();suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(original),unittest.defaultTestLoader.loadTestsFromModule(added)])
res=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
# Full serialized independent two-image case, with the immutable-snapshot fix
# from review11870 v2. These are limitation probes, not safety PASS cases.
cp=R/'permission-envelope-review11870-01/COUNTEREXAMPLES-v2.json';ce=json.loads(cp.read_text());pr=next(x for x in ce['complete_examples']if x['name']=='native_visibility_only_I2_but_supplement_labels_I')
assert digest(pr['inventory'])==pr['independent_pins']['inventory_sha256'];assert pr['inventory']['witnesses'][0]['image']=='I'
pr_result=compare([bind_source(c,contract(c))for c in pr['source_contexts']],core=pr['core'],resolved_view=pr['view'],inventory=pr['inventory'],assessment=pr['assessment'],expected=IndependentPins(**pr['independent_pins']),primitives=PRIMITIVES)
assert pr_result['permission_only_pass']is True and pr_result['native_qualified']is False
def pin(p):
 b=p.read_bytes();return {'file':str(p),'raw_sha256':hashlib.sha256(b).hexdigest()}
modules={n:pin(Path(m.__file__).resolve())for n,m in sys.modules.items()if getattr(m,'__file__',None)and(n.startswith('photo_')or n=='prompt_generator')}
copy=json.loads((P/'ORIGINAL-COPY-v1.json').read_text());original_pins=[]
for row in copy['all_regular_files_copied_byte_identically']:
 p=Path(copy['source'])/row['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['raw_sha256'];original_pins.append(pin(p))
x={'schema':'permission-envelope-prototype02-execution/v1','task':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'methods':res.testsRun,'old_methods':55,'new_methods':9,'original_scenarios':len(original.CASES),'added_scenarios':len(added.CASES),'success':res.wasSuccessful(),'failures':len(res.failures),'errors':len(res.errors),'log':stream.getvalue(),'old_cases':original.CASES,'new_cases':added.CASES,'PR_known_pending_boundary':{'fixture':pin(cp),'actual_permission_only':pr_result['permission_only_pass'],'same_image_PR_mechanically_proved':False,'source1299_native_qualified':False,'reason':'Only I2-specific native source span; deliberately wrong independent supplement image I still passes. This is the already disclosed research-only trust boundary, not fixed or counted as admission success.'},'actual_loaded_modules':modules,'actual_research_modules':[pin(P/n)for n in ['envelope.py','fixtures.py','test_envelope.py','test_joint_paths_v2.py','run_tests_v2.py']],'prototype01_all_original_files_still_exact':original_pins,'frozen_generation':'50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839','network_denied':True,'API_keys_absent':True,'native_fullcompact_B2_consumer_statepreservation_runtime_or_operating':False,'source_proof_Git_production_changes':0}
out.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(json.dumps({k:x[k]for k in ['methods','original_scenarios','added_scenarios','success','failures','errors']},indent=2));print('canon',digest(x),'raw',hashlib.sha256(out.read_bytes()).hexdigest())
if not res.wasSuccessful():sys.exit(1)
