"""Historical external evidence is linked without inventing an invocation."""
import copy
import hashlib
import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from photo_external_result import validate_evidence, reconcile


def setup(tmp_path):
    ref = tmp_path / 'reference.jpg'; ref.write_bytes(b'actual reference')
    img = tmp_path / 'result.png'; img.write_bytes(b'\x89PNG\r\n\x1a\nexample')
    sha = lambda b: hashlib.sha256(b).hexdigest()
    roles = ('pack', 'runtime_receipt', 'composed', 'composed_audit', 'render_request', 'runtime_audit')
    state = {'mode': 'image', 'phase': 'runtime_audited', 'run_id': 'abc', 'operations': [],
             'transport': {'lane': 'native'}, 'source_binding': {'generation_id': 'gen'},
             'artifacts': {r: {'sha256': sha(r.encode()), 'path': str(tmp_path / r)} for r in roles}}
    request = {'pack_id': 'pack1', 'runtime_prompt_en': 'Audited prompt', 'runtime_negative_en': None,
               'references': [{'path': str(ref), 'sha256': sha(ref.read_bytes()), 'role': 'reference'}],
               'referenced_image_paths': [str(ref)]}
    composed = {'prompt_en': 'Audited prompt', 'negative_en': None}
    started = {'schema': 'nun-reference-api-attempt/v1', 'status': 'started', 'run_id': 'abc', 'pack_id': 'pack1',
               'generation_id': 'gen', 'image_call_count': 1, 'sdk_retries': 0, 'composed_audit': 'pass',
               'runtime_audit': 'pass', 'bound_artifacts': {r: state['artifacts'][r]['sha256'] for r in roles},
               'runtime_prompt_sha256': sha(b'Audited prompt'), 'runtime_negative_sha256': None,
               'reference_path': str(ref), 'reference_sha256': sha(ref.read_bytes()), 'reference_role': 'reference',
               'model': 'requested-image-model'}
    outcome = {'status': 'succeeded', 'image_call_count': 1, 'provider_request_id': 'req_test',
               'image_path': str(img), 'image_sha256': sha(img.read_bytes())}
    return state, request, composed, started, outcome


def test_matching_evidence_binds_exact_image(tmp_path):
    state, request, composed, started, outcome = setup(tmp_path)
    assert validate_evidence(state, request, composed, started, outcome) == {'path': outcome['image_path'], 'sha256': outcome['image_sha256']}


@pytest.mark.parametrize('which,key,value', [
    ('started', 'run_id', 'other'), ('started', 'runtime_prompt_sha256', 'wrong'),
    ('started', 'reference_sha256', 'wrong'), ('started', 'sdk_retries', 1),
    ('outcome', 'status', 'unknown'), ('outcome', 'image_sha256', 'wrong'),
    ('outcome', 'provider_request_id', ''),
])
def test_cross_run_tampered_or_uncertain_evidence_rejected(tmp_path, which, key, value):
    state, request, composed, started, outcome = setup(tmp_path)
    (started if which == 'started' else outcome)[key] = value
    with pytest.raises(ValueError):
        validate_evidence(state, request, composed, started, outcome)


def test_reconcile_is_idempotent_and_preserves_uncertainty(tmp_path):
    from contextlib import contextmanager
    state, request, composed, started, outcome = setup(tmp_path)
    start_path, end_path = tmp_path/'started.json', tmp_path/'outcome.json'
    start_path.write_text(json.dumps(started)); end_path.write_text(json.dumps(outcome))
    for key, val in [('render_request', request), ('composed', composed)]:
        Path(state['artifacts'][key]['path']).write_text(json.dumps(val))
    @contextmanager
    def lock(_): yield state
    def bound(s, role): return Path(s['artifacts'][role]['path'])
    def commit(run, s, phase, outputs):
        assert 'external_pre_reconciliation_state' in outputs
    kwargs = dict(locked_state=lock, bound_path=bound, read_json=lambda p: json.loads(Path(p).read_bytes()),
                  ensure=lambda s: None, audit_bound=lambda *a, **k: {'composed_audit': {'status':'pass'}, 'runtime_audit': {'status':'pass'}},
                  commit_stage=commit, encode=lambda x: json.dumps(x).encode())
    result = reconcile(tmp_path, start_path, end_path, **kwargs)
    assert result['status'] == 'reconciled' and result['image_call_count'] == 0
    assert state['operations'][0]['lane'] == 'external_api'
    assert 'not_provider_authenticated' in state['operations'][0]['provenance']
    assert reconcile(tmp_path, start_path, end_path, **kwargs)['status'] == 'already_reconciled'
    changed = copy.deepcopy(outcome); changed['provider_request_id'] = 'req_other'; end_path.write_text(json.dumps(changed))
    with pytest.raises(ValueError, match='existing_operation'):
        reconcile(tmp_path, start_path, end_path, **kwargs)


def test_managed_review_rejects_modified_reconciled_evidence(tmp_path, monkeypatch):
    import importlib.util
    path = Path(__file__).resolve().parents[1] / 'scripts/photo_workflow_reviews.py'
    spec = importlib.util.spec_from_file_location('external_result_review_under_test', path)
    reviews = importlib.util.module_from_spec(spec); spec.loader.exec_module(reviews)
    state, request, composed, started, outcome = setup(tmp_path)
    enc = lambda x: json.dumps(x, ensure_ascii=False).encode()
    start_raw, end_raw = enc(started), enc(outcome)
    evidence_id = hashlib.sha256(start_raw + b'\0' + end_raw).hexdigest()
    result = {'path': outcome['image_path'], 'sha256': outcome['image_sha256']}
    record = {'schema':'photo-external-result-reconciliation/v1', 'evidence_id': evidence_id,
              'started_sha256': hashlib.sha256(start_raw).hexdigest(), 'outcome_sha256': hashlib.sha256(end_raw).hexdigest(),
              'result_binding': result, 'provenance':'self_reported_external_api_evidence_not_provider_authenticated'}
    for key, raw in [('external_started',start_raw), ('external_outcome',end_raw), ('external_reconciliation',enc(record))]:
        p = tmp_path/key; p.write_bytes(raw); state['artifacts'][key] = {'path':str(p), 'sha256':hashlib.sha256(raw).hexdigest()}
    operation={'lane':'external_api','status':'complete','external_evidence_id':evidence_id,'result_binding':result}
    def checked(s, role):
        row=s['artifacts'][role]; p=Path(row['path'])
        if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']: raise reviews.WorkflowError('stale_artifact')
        return p
    monkeypatch.setattr(reviews,'bound_path',checked)
    monkeypatch.setattr(reviews,'value',lambda s, role: request if role=='render_request' else composed)
    reviews.validate_external_operation(state,operation)
    Path(state['artifacts']['external_outcome']['path']).write_bytes(b'{}')
    with pytest.raises(reviews.WorkflowError, match='stale_artifact'):
        reviews.validate_external_operation(state,operation)
