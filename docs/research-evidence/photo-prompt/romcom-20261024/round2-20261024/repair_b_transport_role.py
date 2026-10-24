"""Coordinator-only, zero-call transport-role recovery using the unchanged sealed auditors.

The old admitted request and its failed preflight stay on disk. No frozen,
retrieval, source, composition, prompt, negative or image bytes can change here.
This helper is separately reviewed evidence, not a sealed runtime member.
"""
from pathlib import Path
import copy, hashlib, json, os, subprocess, sys, uuid

R = Path('/Users/chasoik/Projects/image-prompt')
O = Path(__file__).resolve().parent
S = R/'skills/photo-prompt-image-generator'
STORE = Path.home()/'.cache/image-prompt/photo-shared-runtime/h-f2-installed'
GEN = '22aa903c2257bc2b3da9dfe9361e54d186c2d5569733e63ecd30a9e62ffe46fb'
NATIVE = STORE/'generations/278453ebc86a659d8ab0b19e4aa5960ac840ce079c96bf47c3e553f71a7b7c19'
RUN = R/'generated/photo-runs/romcom-20261024-r2-b/compatible-run'
PARAMETERS = RUN/'authored/transport.json'

def corrected_request(old, parameters, expected):
    if set(parameters) != {'references', 'referenced_image_paths', 'transparent_background'}:
        raise ValueError('only existing transport reference role can be corrected')
    if len(old['references']) != 1 or len(parameters['references']) != 1:
        raise ValueError('one unchanged reference required')
    before, after = old['references'][0], parameters['references'][0]
    if set(before) != set(after) or set(after) != {'path', 'sha256', 'role'}:
        raise ValueError('reference row shape changed')
    if {k:v for k,v in before.items() if k != 'role'} != {k:v for k,v in after.items() if k != 'role'}:
        raise ValueError('reference bytes or path changed')
    if [{'role':after['role'], 'sha256':after['sha256']}] != expected:
        raise ValueError('exact projected role and digest required')
    for name in ['referenced_image_paths', 'transparent_background']:
        if old.get(name) != parameters[name]:
            raise ValueError('non-role transport change')
    result = copy.deepcopy(old)
    result['references'] = copy.deepcopy(parameters['references'])
    return result

def main():
    if '--execute-verified' not in sys.argv:
        sys.path.insert(0, str(S/'scripts'))
        from photo_installed_h_f2 import release, runtime_python
        native, manifest, _ = release(STORE, GEN)
        assert native == NATIVE
        env = dict(os.environ, PYTHONNOUSERSITE='1', HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1')
        for key in ['PYTHONPATH', 'OPENAI_API_KEY', 'GEMINI_API_KEY', 'GOOGLE_API_KEY', 'ANTHROPIC_API_KEY']:
            env.pop(key, None)
        raise SystemExit(subprocess.run([str(runtime_python(S,manifest)), '-I', str(Path(__file__).resolve()), '--execute-verified'], env=env).returncode)
    import gc
    gc.disable()
    sys.path.insert(0, str(NATIVE/'scripts'))
    import photo_workflow as workflow
    from photo_workflow_state import locked_state, bound_path, value, digest, encode, atomic_write, commit_stage
    from photo_workflow_worker import audit_bound
    with locked_state(RUN) as state:
        assert not state['operations'], 'zero reservations and attempts required'
        assert 'native_plan' not in state['artifacts'], 'no admitted native plan permitted'
        assert state['h_f2_binding']['generation_id'] == GEN
        for role, row in state['artifacts'].items():
            assert digest(bound_path(state,role).read_bytes()) == row['sha256'], role
        before_bindings = {role:row['sha256'] for role,row in state['artifacts'].items() if role not in {'render_request','runtime_audit'}}
        try:
            workflow.ensure(state)
        except workflow.WorkflowError as error:
            assert str(error) == 'child_preserved_reference_changed', str(error)
        else:
            raise ValueError('specific stale reference-role failure required')
        old = value(state,'render_request')
        params = json.loads(PARAMETERS.read_bytes())
        expected = value(state,'retry_context')['execution_scope']['references']
        new = corrected_request(old,params,expected)
        for reference in new['references']:
            assert hashlib.sha256(Path(reference['path']).read_bytes()).hexdigest() == reference['sha256']
        path = RUN/'.staging'/(uuid.uuid4().hex+'.role-corrected.request.json')
        atomic_write(path,encode(new))
        prospective = dict(state, artifacts=dict(state['artifacts']))
        prospective['artifacts']['render_request'] = {'path':str(path),'sha256':digest(path.read_bytes())}
        # All lineage/preservation checks run against the prospective exact request.
        workflow.ensure(prospective)
        audited = audit_bound(prospective,runtime=True)
        for role in ['composed_audit','runtime_audit']:
            assert audited[role]['status'] == 'pass' and not audited[role]['failures'], audited[role]
        evidence = {'status':'pass','recovery_kind':'prospective_reference_role_only','helper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sealed_generation':GEN,'old_render_request':dict(state['artifacts']['render_request']),'new_render_request_sha256':digest(path.read_bytes()),'exact_expected_references':expected,'unchanged_input_hashes':before_bindings,'native_calls_before':0,'audit':audited,'limits':'Coordinator transport recovery; no sealed kernel change, resampling, prompt revision or image invocation.'}
        atomic_write(O/'b-prospective-role-recovery.json',encode(evidence))
        commit_stage(RUN,state,'runtime_audited',{'render_request':path.read_bytes(),'runtime_audit':encode(audited['runtime_audit'])})
        assert before_bindings == {role:row['sha256'] for role,row in state['artifacts'].items() if role not in {'render_request','runtime_audit'}}
    print(json.dumps({'status':'pass','native_calls':0,'evidence':str(O/'b-prospective-role-recovery.json')},ensure_ascii=False))

if __name__ == '__main__':
    main()
