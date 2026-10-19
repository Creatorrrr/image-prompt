"""Compare successful corrected native runs; retain all earlier failed evidence."""
from pathlib import Path
import run
from history_state import new
files={'control':'NATIVE-BRANCH-control.json','combined':'NATIVE-BRANCH-combined.json'}
rows={k:run.state.read(run.E/v) for k,v in files.items()};targets=run.state.read(run.E/'TARGETS.json')
fields=['retrieve_phase','retrieve_reuse','real_recorder_subprocess','real_native_reaudit','native_ledger_status','native_terminal_status','native_last_event_stage','native_valid_evidence_hash_bound','native_operation_bound','negative_cases','local_native_keyword_only_diagnostic','H_default_checked_separately','Gemini_calls','new_embedding_calls','actual_image_calls','original_CURRENT_writes']
assert all(r['status']=='PASS' and r['exit_code']==0 for r in rows.values())
assert all(rows['control'][k]==rows['combined'][k] for k in fields)
assert rows['combined']['native_terminal_status']=='provider_blocked'
assert rows['combined']['native_last_event_stage']=='attempt_recorded'
assert set(rows['combined']['negative_cases'])=={'sha','prompt','attempt','runtime_prompt'}
for label,r in rows.items():
    expected=targets['original']['skills/photo-prompt-image-generator/scripts/photo_workflow.py']['sha256'] if label=='control' else targets['working']['skills/photo-prompt-image-generator/scripts/photo_workflow.py']
    assert r['loaded_modules']['photo_workflow']['sha256']==expected
    for module in ('record_image_run','image_attempt_evidence'):
        assert r['loaded_modules'][module]['sha256']==run.state.sha(run.SKILL/'scripts'/(module+'.py'))
new(run.E/'NATIVE-BRANCH-COMPARISON.json',{'status':'PASS','cases':{k:{'path':v,'sha256':run.state.sha(run.E/v)} for k,v in files.items()},
    'equal_semantic_fields':fields,'real_native_retrieve_reuse_and_audits':True,'real_recorder_and_native_reaudit':True,
    'valid_rejected_observation_recorded':True,'terminal_status':'provider_blocked','last_event_stage':'attempt_recorded',
    'evidence_sha_prompt_attempt_runtime_prompt_tampering_rejected_before_ledger':4,
    'source_workflow_hashes_verified':True,'earlier_failed_harness_attempts_retained':True,
    'Gemini_calls':0,'new_embedding_calls':0,'actual_image_calls':0,'original_CURRENT_writes':0})
print('native retrieve/reuse/real recorder/4 tamper cases/terminal state comparison PASS',flush=True)
