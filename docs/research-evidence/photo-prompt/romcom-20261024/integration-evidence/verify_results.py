"""Verify actual artifacts and bindings; pixel judgments remain separately authored."""
from pathlib import Path
import datetime,hashlib,json,struct

O=Path(__file__).resolve().parent
R=Path('/Users/chasoik/Projects/image-prompt')
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
digest_text=lambda text:hashlib.sha256(text.encode()).hexdigest()

def main():
    reference=Path(read(O/'BASELINE.json')['reference_path'])
    reference_sha=read(O/'independent-inputs/assignments.json')['reference_sha256']
    assert sha(reference)==reference_sha
    skill_sha=read(O/'BASELINE.json')['skill_sha256']
    frozen={r['arm']:r for r in read(O/'final-core-bindings.json')['arms']}
    reviews=read(O/'coordinator-pixel-review.json')
    tested=read(O/'successor.json')['generation_id']
    rows=[]
    for arm in ('a','b','c'):
        d=R/'generated/photo-runs'/f'romcom-20261024-{arm}'
        summary=read(d/'result-summary.json')
        manifest=read(d/'run_manifest.json')
        ledger=[json.loads(line) for line in (d/'image_runs.ndjson').read_text().splitlines() if line.strip()]
        matched=[r for r in ledger if r['run_id']==manifest['ledger_run_id']]
        assert len(matched)==1
        entry=matched[0]
        assert manifest['image_call_count']==entry['image_call_count']==1
        assert manifest['cross_arm_inputs_used'] is entry['cross_arm_inputs_used'] is False
        assert manifest['generation_environment']==entry['generation_environment']=='native_imagegen'
        assert manifest['candidate_pack_version']==entry['candidate_pack_version']=='h-f2-v2'
        assert manifest['status']==entry['status']=='success'
        # source_ref is a human label; canonical authority is the run and receipts.
        assert manifest['source_ref']==entry['source_ref']
        run=Path(frozen[arm]['run'])
        state=read(run/'workflow.json')
        assert state['h_f2_binding']['generation_id']==tested
        assert state['source_binding']['generation_id']==read(O/'successor.json')['native_generation_id']
        h_receipt=read(next(run.glob('revisions/*/h_f2_receipt.json')))
        native_receipt=read(next(run.glob('revisions/*/runtime_receipt.json')))
        assert h_receipt['generation_id']==tested
        assert native_receipt['generation_id']==state['source_binding']['generation_id']
        assert manifest['skill_sha256']==entry['skill_sha256']==skill_sha
        assert manifest['authorial_core_sha256']==entry['authorial_core_sha256']==frozen[arm]['core_canonical_sha256']
        assert manifest['reference_sha256']==entry['reference_sha256']==[reference_sha]
        plan=read(Path(entry['native_render_plan_json']))
        assert plan['attempt']==1
        assert plan['payload']['referenced_image_paths']==[str(reference)]
        assert plan['payload']['prompt']==entry['prompt_en']
        prompt=d/'final-prompt.txt'
        assert prompt.read_text()==plan['payload']['prompt']
        assert sha(prompt)==digest_text(plan['payload']['prompt'])==entry['runtime_prompt_sha256']==manifest['runtime_prompt_sha256']
        assert len(manifest['image_paths'])==len(manifest['image_hashes'])==1
        picture=Path(manifest['image_paths'][0])
        assert sha(picture)==manifest['image_hashes'][0]['sha256']==reviews['arms'][arm]['sha256']
        header=picture.read_bytes()[:24]
        assert header[:8]==b'\x89PNG\r\n\x1a\n'
        dimensions=list(struct.unpack('>II',header[16:24]))
        assert manifest['chosen_visual_concept_ids']==entry['chosen_visual_concept_ids']==[]
        assert entry['chosen_candidate_ids']==[]
        core=Path(frozen[arm]['core'])
        assert sha(core)==frozen[arm]['core_file_sha256']
        receipt=read(core.parent/'freeze_receipt.json')
        assert sha(core)==receipt['files']['authorial_core_normalized']
        rows.append({'arm':arm,'status':'pass','image_path':str(picture),'image_sha256':sha(picture),
                     'prompt_path':str(prompt),'prompt_sha256':sha(prompt),'image_call_count':1,
                     'reference_attached_in_audited_payload':True,'reference_sha256':reference_sha,
                     'manifest_path':str(d/'run_manifest.json'),'ledger_run_id':entry['run_id'],
                     'source_ref_label':entry['source_ref'],'h_f2_generation_id':tested,
                     'actual_image_dimensions':dimensions,'core_preserved':True,
                     'strict_testcase_result':reviews['arms'][arm]['strict_testcase_result'],
                     'new_CID_selected_count':0,'user_acceptance':'pending'})
    result={'status':'artifact_bindings_verified','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'arms':rows,'actual_native_image_calls':sum(r['image_call_count'] for r in rows),
            'strict_testcase_pass':sum(r['strict_testcase_result']=='PASS' for r in rows),
            'source_qualification':'No native approval is inferred from registration, retrieval, valid audits or these images.',
            'independence_scope':'Hashes and declared manifests bind the procedure; this is not proof of unseen agent cognition.',
            'data_improvement_effect':'NOT_DEMONSTRATED','user_acceptance':'pending'}
    (O/'arm-artifact-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'native_image_calls':result['actual_native_image_calls'],
                      'strict_testcase_pass':result['strict_testcase_pass']}))

if __name__=='__main__':main()
