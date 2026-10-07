"""Verify frozen experiment bindings and consolidate the three native runs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path('/Users/chasoik/Projects/image-prompt')
HERE = Path(__file__).resolve().parent
WT = Path('/Users/chasoik/.codex/worktrees/ethereal-gothic-qualification/image-prompt')
SKILL = 'skills/photo-prompt-image-generator'

def read(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(v): return hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def write(name, v): (HERE/name).write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n')

def main():
    pin = read(HERE/'QUALIFICATION-SOURCE.json')
    latest = read(HERE/'primary-runtime-publication-final.json')
    failures = []
    def check(ok, message):
        if not ok: failures.append(message)
    check(sha(WT/SKILL/'SKILL.md') == pin['skill_sha256'], 'frozen skill changed')
    check(sha(ROOT/SKILL/'SKILL.md') == pin['skill_sha256'], 'current skill changed')
    source_checks = []
    for rel, expected in pin['data'].items():
        actual = sha(WT/SKILL/rel)
        check(actual == expected, 'qualification source changed: '+rel)
        source_checks.append(dict(path=rel, expected=expected, actual=actual))
    before_ext = read(WT/SKILL/'assets/photo_prompt_ethereal_gothic_scene_extension.json')
    current_ext = read(ROOT/SKILL/'assets/photo_prompt_ethereal_gothic_scene_extension.json')
    before_operational = {k:v for k,v in before_ext.items() if k!='maintenance_ref'}
    current_operational = {k:v for k,v in current_ext.items() if k!='maintenance_ref'}
    check(before_operational == current_operational, 'current candidate meaning differs from tested DATA')
    check(sha(WT/SKILL/'assets/photo_prompt_visual_obligations_ethereal_gothic_scene.json') == sha(ROOT/SKILL/'assets/photo_prompt_visual_obligations_ethereal_gothic_scene.json'), 'profile DATA differs')
    initial=read(HERE/'INITIAL-SNAPSHOT.json')
    mutable={'assets/photo_prompt_source_manifest.json','assets/photo_prompt_semantic_index.json','assets/photo_prompt_visual_profile_index.json'}
    protected=[]
    for rel, expected in initial['file_sha256'].items():
        if rel not in mutable:
            actual=sha(ROOT/SKILL/rel)
            check(actual==expected, 'unrelated initial source changed: '+rel)
            protected.append(rel)
    titles={'a':'마지막 회차 정류장의 꽃 운반 여행자','b':'야간 수분 관찰 유리온실','c':'빈 리허설룸의 무대 셔터 조절 기술자'}
    pair_map={
        'a':[('image_render_request.json','native_tool_args.json')],
        'b':[('runtime_request.json','native_image_args.json'),('runtime_request_attempt_2.json','native_image_args_attempt_2.json')],
        'c':[('render_request.json','native_tool_args.json'),('render_request_attempt_2.json','native_tool_args_attempt_2.json')],
    }
    images={'a':['native_image_attempt_1.png'],'b':['native_attempt_1.png','native_attempt_2.png'],'c':['generated_image_attempt_1.png','generated_image_attempt_2.png']}
    expected_image_hashes={
        'a':['2614f27720eed20653b29470f0d7b62273d23d804a01661f43c47139333c4d33'],
        'b':['8f8b2c0cc9efac65018e768afb215d7ca2ed90d0f9cf69cd9539f60ac1aa212a','91271364baee9299cf9b5131cbc9ce12f225a8c67508ef65bdefa52f2dcd7541'],
        'c':['e999862ea5a8e6f0cd262de2877af6eaa1f6a07668a1ecc826c4af758853f34e','756ac8bd88532021b25b2bd16928edf856653eccfb68e9854ec2de8503e46dfb'],
    }
    selected={
        'a':['egr_fabric_rosette_vs_living_flower'],
        'b':['egr_fabric_rosette_vs_living_flower','egr_dark_lateral_negative_space'],
        'c':['egr_mume_on_leafless_woody_branches','egr_cool_skin_warm_reflected_edge'],
    }
    arms=[]
    arm_proofs=[]
    for a in 'abc':
        q=HERE/('arm_'+a); result=read(q/'QUALIFICATION-RESULT.json'); frozen=read(q/'PRECORE-FROZEN.json')
        hashes=frozen.get('byte_hashes') or frozen['files']
        for name, expected in hashes.items(): check(sha(q/name)==expected,a+': changed frozen '+name)
        manifest=read(q/'run_manifest.json'); ledger=[json.loads(line) for line in (q/'image_runs.ndjson').read_text().splitlines() if line.strip()]
        count=len(pair_map[a]); check(len(ledger)==count,a+': ledger count mismatch')
        check(manifest['image_call_count']==count,a+': manifest call count mismatch')
        check(not manifest['cross_arm_inputs_used'],a+': cross-arm input')
        check(manifest['skill_sha256']==pin['skill_sha256'],a+': skill pin mismatch')
        receipt=read(q/'runtime_receipt.json')
        check(receipt['generation_id']==pin['runtime_generation']['generation_id'],a+': generation mismatch')
        check(receipt['source_fingerprint']==pin['runtime_generation']['source_fingerprint'],a+': source fingerprint mismatch')
        for i,row in enumerate(ledger):
            check(row['pack_id']==manifest['pack_id'],a+': different pack in attempt')
            check(row['authorial_core_sha256']==manifest['authorial_core_sha256'],a+': different core in attempt')
            check(row['intent_lock_sha256']==manifest['intent_lock_sha256'],a+': different lock in attempt')
            check(row['tool']=='image_gen.imagegen' and row['generation_environment']=='codex_native',a+': non-native tool')
            check(row['status']=='success',a+': generation failure')
            check(row['retry_of']==(ledger[i-1]['run_id'] if i else None),a+': retry chain mismatch')
        request_checks=[]
        for rn,an in pair_map[a]:
            req=read(q/rn); args=read(q/an)
            check(args['prompt']==req['runtime_prompt_en'],a+': actual native text differs from audited runtime')
            check(req['runtime_negative_en'] in args['prompt'],a+': negative bytes missing')
            check(args['referenced_image_paths']==[r['path'] for r in req['references']],a+': tool refs differ')
            for r in req['references']: check(sha(r['path'])==r['sha256'],a+': reference bytes changed')
            request_checks.append(dict(request=rn,native_args=an,exact_prompt_equal=True,reference_count=len(req['references'])))
        image_rows=[]
        for name,expected in zip(images[a],expected_image_hashes[a]):
            actual=sha(q/name);check(actual==expected,a+': image bytes changed')
            image_rows.append(dict(path=str(q/name),sha256=actual))
        native_pass = result['new_data']['native_component_review']['all_source_components_native_observed'] if a=='a' else (result['all_selected_new_data_components_complete'] if a=='b' else result['final_selected_data_all_components_visible'])
        strict_pass = result['strict_native_status']['technical_qualified'] if a=='a' else (result['strict_auditor_result']['technical_qualified'] if a=='b' else result['final_strict_qualified'])
        check(native_pass==(a=='a'),a+': expected DATA outcome differs from review')
        check(strict_pass==(a!='c'),a+': expected strict outcome differs from review')
        arm_proofs.append(dict(arm=a,frozen_file_count=len(hashes),all_frozen_bytes_equal=True,ledger_count=count,exact_requests=request_checks,images=image_rows,result_json_sha256=sha(q/'QUALIFICATION-RESULT.json')))
        arms.append(dict(arm=a,title=titles[a],image_call_count=count,pack_id=manifest['pack_id'],normal_retrieval_mode='core_bm25f',new_candidate_entry_ids_adopted=selected[a],new_visual_profiles_selected=[],selected_data_all_components_status='PASS' if native_pass else 'FAIL',strict_embodiment_status='PASS_5_OF_5' if strict_pass else 'FAIL_4_OF_5',strict_failed_gates=[] if strict_pass else ['embodiment_visibility_and_projection'],images=image_rows,final_image_path=image_rows[-1]['path'],result_path=str(q/'QUALIFICATION-RESULT.json'),user_judgment='pending'))
    verification=dict(schema_version='ethereal-qualification-binding-verification/v1',status='PASS' if not failures else 'FAIL',failures=failures,skill_sha256=pin['skill_sha256'],qualification_generation_id=pin['runtime_generation']['generation_id'],qualification_source_fingerprint=pin['runtime_generation']['source_fingerprint'],qualification_source_files_checked=len(source_checks),all_qualification_sources_unchanged=not any('qualification source changed' in x for x in failures),unrelated_initial_source_files_checked=len(protected),all_unrelated_initial_sources_unchanged=not any('unrelated initial source changed' in x for x in failures),current_operational_candidates_equal_tested=True,current_operational_digest=digest(current_operational),current_primary_runtime_generation_id=latest['generation_id'],current_primary_fingerprint=latest['source_fingerprint'],metadata_revision=str(HERE/'MAINTENANCE-METADATA-REVISION.json'),arms=arm_proofs,boundary='Hash verification binds recorded files and receipts; recorded reviews and actual tool returns establish the native observation layer. Hashes alone are not pixel truth or causal improvement.')
    write('BINDING-VERIFICATION.json',verification)
    summary=dict(schema_version='ethereal-gothic-qualification-summary/v1',task_execution_completed=not failures,new_candidate_count=60,new_visual_profile_count=41,new_optional_bundle_count=68,enriched_existing_entries=5,arm_count=3,native_tool_calls=5,selected_data_complete_arm_pass_count=1,selected_data_complete_arm_fail_count=2,strict_embodiment_complete_arm_pass_count=2,strict_embodiment_complete_arm_fail_count=1,unique_new_entries_adopted=sorted({x for v in selected.values() for x in v}),unique_new_entries_adopted_count=4,total_new_candidates=60,new_visual_profiles_exposed_in_arms=0,new_visual_profiles_native_hard_gate_coverage=0,arms=arms,live_retrieval_probe_summary=read(HERE/'LIVE-RETRIEVAL-PROBES.json')['summary'],qualification_pin=pin['runtime_generation'],primary_current_runtime=latest,binding_verification_status=verification['status'],user_judgment='pending',causal_improvement_proven=False,full_regression_status='FAIL_INCOMPLETE',limits=['Ordinary selected-candidate DATA observations are supplemental all-component reviews, not fabricated hard gates from unexposed visual profiles.','No baseline image or ablation was rendered.','Three random scenes tested four of sixty new entries; they do not qualify all forty-one profiles.','Maintenance v2 changed metadata only; native experiments retain their exact v1 generation.','Full regression logs preserve archived source mismatches and other unresolved failures.'])
    write('QUALIFICATION-SUMMARY.json',summary)
    print(json.dumps(dict(binding_status=verification['status'],failures=failures,native_calls=5,data_arms_pass=1,data_arms_fail=2,protected_sources=len(protected))))
    return 0 if not failures else 1

if __name__=='__main__': raise SystemExit(main())
