"""Reconciliation preserves the original uncertain event and verifies bytes."""
import copy, hashlib, json, subprocess, sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from photo_native_preview_reconcile import validate, PROVENANCE, SCHEMA
from photo_workflow_state import encode
from photo_native_bridge import BRIDGE_JAVASCRIPT


def fixture(tmp_path):
    img=tmp_path/'actual.png';img.write_bytes(b'\x89PNG\r\n\x1a\ntest')
    sh=lambda b:hashlib.sha256(b).hexdigest()
    h=sh(img.read_bytes()); note=tmp_path/'agent-observation.md';note.write_text(f'Agent-reported native result {img}; sha256 {h}')
    op={'operation_id':'op1','lane':'native','status':'preview_only','attempts':[{'attempt':1}],'input_bindings':{'pack':'hash'}}
    state={'mode':'image','run_id':'run1','operations':[op],'artifacts':{'native_plan':{'sha256':'planhash'}}}
    plan={'operation_id':'op1','input_bindings':{'pack':'hash'}};obs={'operation_id':'op1','outcome':'preview_only'}
    ev={'schema':SCHEMA,'provenance':PROVENANCE,'run_id':'run1','source_operation_id':'op1','native_plan_sha256':'planhash',
        'observation_canonical_sha256':sh(encode(obs)),'source_note_path':str(note),'source_note_sha256':sh(note.read_bytes()),
        'reported_original_path':str(img),'result_path':str(img),'result_sha256':h}
    return state,ev,obs,plan


def test_original_result_binds_without_rewriting_preview(tmp_path):
    state,ev,obs,plan=fixture(tmp_path); before=copy.deepcopy(state)
    assert validate(state,ev,obs,plan)['sha256']==ev['result_sha256']
    assert state==before


@pytest.mark.parametrize('field,value', [('run_id','wrong'),('native_plan_sha256','wrong'),('result_sha256','wrong'),('provenance','provider_authenticated'),('source_operation_id','other')])
def test_mismatch_is_rejected(tmp_path,field,value):
    state,ev,obs,plan=fixture(tmp_path);ev[field]=value
    with pytest.raises(ValueError):validate(state,ev,obs,plan)


def test_changed_report_or_conflicting_attempt_is_rejected(tmp_path):
    state,ev,obs,plan=fixture(tmp_path)
    Path(ev['source_note_path']).write_text('changed')
    with pytest.raises(ValueError,match='source_note_changed'):validate(state,ev,obs,plan)


@pytest.mark.parametrize('hint,expected', [
    ('Saved image at /tmp/example.png',{'outcome':'returned','image_path':'/tmp/example.png'}),
    ('No local file',{'outcome':'preview_only'}),
    ('/tmp/a.png and /tmp/b.png',{'outcome':'preview_only'}),
    ('https://example.com/a.png',{'outcome':'preview_only'}),
])
def test_bridge_uses_only_unambiguous_local_tool_output_hint(hint,expected):
    script=BRIDGE_JAVASCRIPT+'\nprocess.stdout.write(JSON.stringify(photoNativeObservation('+json.dumps({'output_hint':hint})+')));'
    result=subprocess.run(['node','-e',script],capture_output=True,text=True,check=True)
    assert json.loads(result.stdout)==expected
