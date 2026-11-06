"""Reconcile a separately recorded, already returned image into a managed run.

This verifies consistency of local evidence; it does not authenticate the
provider or claim that a native tool invocation occurred. It makes no API call.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def validate_evidence(state, request, composed, started, outcome):
    """Validate historical self-reported attempt against exact bound inputs."""
    def require(condition, reason):
        if not condition:
            raise ValueError(reason)
    require(state.get('mode') == 'image' and state.get('phase') in ('runtime_audited', 'review_record_validated'), 'run_not_runtime_audited')
    require((state.get('transport') or {}).get('lane') == 'native', 'transport_mismatch')
    require(isinstance(started, dict) and started.get('schema') == 'nun-reference-api-attempt/v1' and started.get('status') == 'started', 'unsupported_attempt_evidence')
    require(isinstance(outcome, dict) and outcome.get('status') == 'succeeded', 'successful_outcome_required')
    require(started.get('run_id') == state.get('run_id') and started.get('pack_id') == request.get('pack_id'), 'run_or_pack_mismatch')
    require(started.get('generation_id') == (state.get('source_binding') or {}).get('generation_id'), 'generation_mismatch')
    require(started.get('image_call_count') == outcome.get('image_call_count') == 1 and started.get('sdk_retries') == 0, 'attempt_count_mismatch')
    require(started.get('composed_audit') == started.get('runtime_audit') == 'pass', 'attempt_audit_missing')
    roles = ('pack', 'runtime_receipt', 'composed', 'composed_audit', 'render_request', 'runtime_audit')
    require(started.get('bound_artifacts') == {r: state['artifacts'][r]['sha256'] for r in roles}, 'input_binding_mismatch')
    prompt = request.get('runtime_prompt_en')
    negative = request.get('runtime_negative_en')
    require(isinstance(prompt, str) and bool(prompt) and isinstance(composed, dict), 'prompt_missing')
    require(prompt == composed.get('prompt_en') + ('\n\nAvoid: ' + negative if negative is not None else ''), 'prompt_mismatch')
    require(negative == composed.get('negative_en'), 'negative_mismatch')
    require(started.get('runtime_prompt_sha256') == sha(prompt.encode()), 'prompt_hash_mismatch')
    require(started.get('runtime_negative_sha256') == (sha(negative.encode()) if negative is not None else None), 'negative_hash_mismatch')
    refs = request.get('references')
    require(isinstance(refs, list) and len(refs) == 1, 'one_reference_required')
    ref = refs[0]
    require(isinstance(ref, dict) and ref.get('path') and ref.get('sha256') and ref.get('role'), 'reference_missing')
    refpath = Path(ref['path']).resolve()
    require(str(refpath) == started.get('reference_path') and ref.get('sha256') == started.get('reference_sha256')
            and ref.get('role') == started.get('reference_role'), 'reference_binding_mismatch')
    require(refpath.is_file() and sha(refpath.read_bytes()) == ref['sha256'], 'reference_bytes_changed')
    paths = request.get('referenced_image_paths')
    require(isinstance(paths, list) and len(paths) == 1 and Path(paths[0]).resolve() == refpath, 'reference_transport_mismatch')
    model = started.get('model')
    request_id = outcome.get('provider_request_id')
    require(isinstance(model, str) and bool(model.strip()), 'model_missing')
    require(isinstance(request_id, str) and bool(re.fullmatch(r'req_[A-Za-z0-9_-]+', request_id)), 'request_id_missing')
    path = Path(outcome.get('image_path', ''))
    require(path.is_absolute() and path.is_file(), 'result_missing')
    data = path.read_bytes()
    require(data.startswith(b'\x89PNG\r\n\x1a\n') and sha(data) == outcome.get('image_sha256'), 'result_hash_mismatch')
    return {'path': str(path.resolve()), 'sha256': sha(data)}


def reconcile(run, started_path, outcome_path, *, locked_state, bound_path, read_json, ensure, audit_bound, commit_stage, encode):
    with locked_state(run) as state:
        ensure(state)
        for role in ('pack', 'runtime_receipt', 'composed', 'composed_audit', 'render_request', 'runtime_audit'):
            bound_path(state, role)
        started_raw, outcome_raw = Path(started_path).read_bytes(), Path(outcome_path).read_bytes()
        started, outcome = json.loads(started_raw), json.loads(outcome_raw)
        request, composed = read_json(bound_path(state, 'render_request')), read_json(bound_path(state, 'composed'))
        if isinstance(composed, list) and len(composed) == 1:
            composed = composed[0]
        result = validate_evidence(state, request, composed, started, outcome)
        existing = state.get('operations', [])
        evidence_id = sha(started_raw + b'\0' + outcome_raw)
        if existing:
            if len(existing) == 1 and existing[0].get('external_evidence_id') == evidence_id and existing[0].get('result_binding') == result:
                return {'status': 'already_reconciled', 'image_call_count': 0, 'result_binding': result}
            raise ValueError('existing_operation_requires_manual_reconciliation')
        audits = audit_bound(state, runtime=True)
        if any(audits[k].get('status') != 'pass' or audits[k].get('failures') for k in ('composed_audit', 'runtime_audit')) or audits.get('contract_failures'):
            raise ValueError('fresh_audit_failed')
        before = encode(state)
        operation = {'operation_id': 'external-' + evidence_id[:32], 'lane': 'external_api', 'status': 'complete',
                     'budget': 1, 'attempts': [{'attempt': 1, 'run_id': 'external-' + evidence_id[:32]}],
                     'result_binding': result, 'external_evidence_id': evidence_id,
                     'provenance': 'self_reported_external_api_evidence_not_provider_authenticated',
                     'image_call_count': 1}
        evidence = {'schema': 'photo-external-result-reconciliation/v1', 'evidence_id': evidence_id,
                    'started_sha256': sha(started_raw), 'outcome_sha256': sha(outcome_raw),
                    'result_binding': result, 'provider_request_id': outcome['provider_request_id'],
                    'requested_model': started['model'], 'observed_model': None,
                    'provenance': operation['provenance'], 'new_image_invocations': 0}
        state['operations'].append(operation)
        commit_stage(run, state, state['phase'], {'external_started': started_raw, 'external_outcome': outcome_raw,
            'external_reconciliation': encode(evidence), 'external_pre_reconciliation_state': before})
        return {'status': 'reconciled', 'image_call_count': 0, 'result_binding': result, 'provenance': operation['provenance']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--started', type=Path, required=True)
    parser.add_argument('--outcome', type=Path, required=True)
    args = parser.parse_args()
    metadata = json.loads((args.run / 'workflow.json').read_bytes())
    binding = metadata.get('h_f2_binding') or {}
    if not binding.get('store') or not binding.get('generation_id'):
        raise ValueError('bound_hf2_generation_required')
    from photo_installed_h_f2 import release
    native, manifest, _ = release(Path(binding['store']), binding['generation_id'])
    if manifest['native_generation_id'] != (metadata.get('source_binding') or {}).get('generation_id'):
        raise ValueError('native_generation_mismatch')
    sys.path.insert(0, str(native / 'scripts'))
    from photo_workflow_state import locked_state, bound_path, read_json, commit_stage, encode
    from photo_workflow import ensure
    from photo_workflow_worker import audit_bound
    result = reconcile(args.run, args.started, args.outcome, locked_state=locked_state, bound_path=bound_path,
                       read_json=read_json, ensure=ensure, audit_bound=audit_bound, commit_stage=commit_stage, encode=encode)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'error', 'code': str(error), 'image_call_count': 0}), file=sys.stderr)
        raise SystemExit(2)
