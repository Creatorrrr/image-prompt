"""Reconcile a reported saved native result without rewriting the original attempt.

The tool response was not durably recorded for these historical attempts. This
verifies local consistency and retains an explicit self-reported provenance; it
cannot authenticate the provider's output or prove the file was returned for
this invocation. It never makes an image call or converts the original event.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

from photo_workflow_state import bound_path, commit_stage, digest, encode, locked_state, read_json, value

PROVENANCE = 'self_reported_native_result_not_provider_authenticated'
SCHEMA = 'photo-native-preview-reconciliation/v1'


def validate(state, evidence, observation, plan):
    def require(ok, code):
        if not ok: raise ValueError(code)
    require(isinstance(evidence, dict) and evidence.get('schema') == SCHEMA, 'unsupported_evidence')
    require(evidence.get('provenance') == PROVENANCE, 'unsupported_provenance')
    require(state.get('mode') == 'image', 'not_image_run')
    ops = [op for op in state.get('operations', []) if op.get('operation_id') == evidence.get('source_operation_id')]
    require(len(ops) == 1, 'source_operation_not_unique')
    op = ops[0]
    require(op.get('lane') == 'native' and op.get('status') == 'preview_only' and len(op.get('attempts', [])) == 1, 'source_not_single_preview')
    require(observation == {'operation_id': op['operation_id'], 'outcome': 'preview_only'}, 'source_observation_mismatch')
    require(plan.get('operation_id') == op['operation_id'] and plan.get('input_bindings') == op.get('input_bindings'), 'plan_operation_mismatch')
    require(evidence.get('run_id') == state.get('run_id'), 'run_mismatch')
    require(evidence.get('native_plan_sha256') == state['artifacts']['native_plan']['sha256'], 'native_plan_mismatch')
    require(evidence.get('observation_canonical_sha256') == digest(encode(observation)), 'observation_mismatch')
    require(evidence.get('source_note_path') and evidence.get('source_note_sha256'), 'source_note_required')
    note = Path(evidence['source_note_path'])
    require(note.is_absolute() and note.is_file() and digest(note.read_bytes()) == evidence['source_note_sha256'], 'source_note_changed')
    source = Path(evidence.get('reported_original_path', ''))
    target = Path(evidence.get('result_path', ''))
    require(source.is_absolute() and source.is_file() and target.is_absolute() and target.is_file(), 'result_not_available')
    data = target.read_bytes()
    require(data.startswith(b'\x89PNG\r\n\x1a\n') and digest(data) == evidence.get('result_sha256'), 'result_hash_mismatch')
    require(digest(source.read_bytes()) == evidence['result_sha256'], 'original_copy_mismatch')
    require(str(source) in note.read_text() and evidence['result_sha256'] in note.read_text(), 'reported_path_not_attested')
    return {'path': str(target.resolve()), 'sha256': digest(data)}


def reconcile(run, evidence_path, *, audit_bound):
    from photo_workflow import ensure
    with locked_state(run) as state:
        ensure(state)
        for role in ('pack', 'runtime_receipt', 'composed', 'composed_audit', 'render_request', 'runtime_audit', 'native_plan'):
            bound_path(state, role)
        raw = Path(evidence_path).read_bytes(); ev = json.loads(raw)
        oid = ev.get('source_operation_id', '')
        observation_path = Path(run) / 'operations' / (oid + '.observation.json')
        observation = read_json(observation_path); plan = value(state, 'native_plan')
        result = validate(state, ev, observation, plan)
        evidence_id = digest(raw)
        existing = [x for x in state['operations'] if x.get('lane') == 'native_reconciled']
        if existing:
            if len(existing) == 1 and existing[0].get('evidence_id') == evidence_id and existing[0].get('result_binding') == result:
                return {'status':'already_reconciled', 'result_binding':result, 'image_call_count':0}
            raise ValueError('conflicting_reconciliation')
        if len(state['operations']) != 1: raise ValueError('unexpected_other_operation')
        audits = audit_bound(state, runtime=True)
        if any(audits[k].get('status') != 'pass' or audits[k].get('failures') for k in ('composed_audit', 'runtime_audit')) or audits.get('contract_failures'):
            raise ValueError('fresh_audit_failed')
        before = encode(state)
        operation = {'operation_id':'reconciled-'+evidence_id[:32], 'lane':'native_reconciled', 'status':'complete',
                     'source_operation_id':oid, 'attempts':[], 'image_call_count':0, 'result_binding':result,
                     'evidence_id':evidence_id, 'provenance':PROVENANCE}
        state['operations'].append(operation)
        commit_stage(run, state, state['phase'], {'native_reconcile_evidence':raw,
                     'native_reconcile_pre_state':before, 'native_reconcile_original_observation':observation_path.read_bytes()})
        return {'status':'reconciled', 'result_binding':result, 'image_call_count':0, 'provenance':PROVENANCE}


def validate_reconciled_operation(state, operation):
    evidence_path = bound_path(state, 'native_reconcile_evidence')
    raw = evidence_path.read_bytes(); evidence = json.loads(raw)
    observation = read_json(bound_path(state, 'native_reconcile_original_observation'))
    plan = value(state, 'native_plan')
    if (operation.get('status') != 'complete' or operation.get('provenance') != PROVENANCE
        or operation.get('evidence_id') != digest(raw) or operation.get('source_operation_id') != evidence.get('source_operation_id')):
        raise ValueError('native_reconciliation_mismatch')
    result = validate(state, evidence, observation, plan)
    if result != operation.get('result_binding'): raise ValueError('native_reconciliation_mismatch')


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--run',type=Path,required=True);parser.add_argument('--evidence',type=Path,required=True)
    args=parser.parse_args()
    metadata = json.loads((args.run / 'workflow.json').read_bytes())
    binding = metadata.get('h_f2_binding') or {}
    if not binding.get('store') or not binding.get('generation_id'):
        raise ValueError('bound_hf2_generation_required')
    from photo_installed_h_f2 import release
    native, manifest, _ = release(Path(binding['store']), binding['generation_id'])
    if manifest['native_generation_id'] != (metadata.get('source_binding') or {}).get('generation_id'):
        raise ValueError('native_generation_mismatch')
    sys.path.insert(0, str(native / 'scripts'))
    from photo_workflow_worker import audit_bound
    print(json.dumps(reconcile(args.run,args.evidence,audit_bound=audit_bound),ensure_ascii=False))

if __name__ == '__main__':
    try: main()
    except (ValueError,OSError,KeyError,TypeError) as error:
        print(json.dumps({'status':'error','code':str(error),'image_call_count':0}),file=__import__('sys').stderr)
        raise SystemExit(2)
