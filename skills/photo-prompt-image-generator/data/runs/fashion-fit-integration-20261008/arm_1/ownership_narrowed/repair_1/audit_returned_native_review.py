"""Read-only formal audit of the actual same-call return after capture recovery.

The managed preview_only operation and its observation remain untouched. This
uses the official receipt-bound worker and official native-scale validator,
while checking the separately admitted, native-plan-audited ledger row.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile

run = Path(__file__).resolve().parent
parent = run.parent
scripts = Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts')
sys.path.insert(0, str(scripts))
from photo_workflow_worker import audit_bound
from photo_workflow_reviews import validate_visual_scales

temp_root = run / '.audit_tmp'
temp_root.mkdir(exist_ok=True)
tempfile.tempdir = str(temp_root)
state = json.loads((run / 'workflow.json').read_text())
pending = copy.deepcopy(state)
review_path = run / 'render_review_repair_1.json'
raw_review = review_path.read_bytes()
review = json.loads(raw_review)
pending['artifacts']['visual_review'] = {
    'path': str(review_path),
    'sha256': hashlib.sha256(raw_review).hexdigest(),
}
plan = json.loads(Path(state['artifacts']['native_plan']['path']).read_bytes())
rows = [json.loads(line) for line in (parent / 'image_runs.ndjson').read_text().splitlines() if line]
row = next(x for x in rows if x.get('workflow_operation_id') == plan['operation_id'] + ':1')
image_path = Path(review['result_image'])
image_hash = hashlib.sha256(image_path.read_bytes()).hexdigest()
actual_request = json.loads((run / 'native_tool_request_actual.json').read_text())
copy_proof = json.loads((run / 'native_result_copy.json').read_text())
checks = {
    'same_native_operation': row['workflow_operation_id'] == plan['operation_id'] + ':1',
    'successful_return_record': row['status'] == 'success' and row['tool'] == 'image_gen',
    'same_pack': row['pack_id'] == review['pack_id'],
    'same_image_path': str(image_path) in row['image_paths'],
    'same_image_hash': {'path': str(image_path), 'sha256': image_hash} in row['image_hashes'],
    'review_image_hash': image_hash == review['result_sha256'],
    'actual_request_equals_audited_plan': actual_request == plan['payload'],
    'same_runtime_prompt': row['runtime_prompt_sha256'] == hashlib.sha256(plan['payload']['prompt'].encode()).hexdigest(),
    'exact_returned_bytes': copy_proof['source_sha256'] == copy_proof['local_image_sha256'] == image_hash,
    'actual_returned_source_retained': hashlib.sha256(Path(copy_proof['source_path_explicitly_returned']).read_bytes()).hexdigest() == image_hash,
    'correct_parent_retry': row['retry_of'] == '06aaf7ee5558cd92',
    'actual_arm_call_count': row['image_call_count'] == 2,
}
if not all(checks.values()):
    raise ValueError('independent_native_return_binding_failed')

contracts = audit_bound(pending, runtime=True, reviews=True)
if any(contracts[k]['status'] != 'pass' or contracts[k]['failures'] for k in ('composed_audit', 'runtime_audit')):
    raise ValueError('independent_review_requires_audited_inputs')
visual = contracts['visual_review_audit']
if visual['schema_failures']:
    raise ValueError('invalid_independent_visual_review_record')
validate_visual_scales(review, contracts)
summary = {
    'schema_version': 'fashion-fit-independent-render-review-audit/v1',
    'audit_method': 'Official receipt-bound photo_workflow_worker.audit_bound(runtime=True,reviews=True) plus official validate_visual_scales and exact actual ledger/image/request checks.',
    'scope': 'independent_receipt_bound_formal_audit; managed admission is not claimed',
    'status': 'pass',
    'record_valid': True,
    'technical_qualification': 'pass' if visual['technical_qualified'] else 'fail',
    'source_binding': state['source_binding'],
    'native_plan': state['artifacts']['native_plan'],
    'ledger_run_id': row['run_id'],
    'ledger_path': str(parent / 'image_runs.ndjson'),
    'binding_checks': checks,
    'visual': visual,
    'managed_admission': {'status': 'error', 'code': 'review_result_not_bound_to_observed_attempt', 'operation_historical_status': 'preview_only', 'arbitrary_state_mutation': False},
    'additional_generation_calls_for_capture_recovery': 0,
}
(run / 'independent_bound_audit_full.json').write_text(json.dumps(contracts, ensure_ascii=False, indent=2) + '\n')
(run / 'render_review_repair_1_audit.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: summary[k] for k in ('status', 'record_valid', 'technical_qualification', 'scope')}, ensure_ascii=False))
