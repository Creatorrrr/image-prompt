"""Freeze the additive palette boundary without rewriting V1--V32 history."""
from pathlib import Path
import copy
import hashlib
import json
import os
import subprocess
import sys

E=Path(__file__).resolve().parent
W=E.parents[3]
S=Path('skills/photo-prompt-image-generator')
I=Path('skills/subculture-illustration-image-generator')
A=W/I/'assets'
STORE=Path('/tmp/color-palette-main-merge-20261007/runtime-store')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def differences(before,after,pointer=''):
    if pointer in {'/0/creative_augmentation/candidates','/0/semantic_clarification/candidates','/0/visual_concept_candidates/candidates'}:
        return [] if before==after else [{'pointer':pointer,'before':before,'after':after}]
    if type(before)!=type(after):return [{'pointer':pointer,'before':before,'after':after}]
    if isinstance(before,dict):
        if set(before)!=set(after):
            assert pointer in {'/0/slots/color_grading/candidates/1','/0/slots/texture/candidates/0'},pointer
            return [{'pointer':pointer,'before':before,'after':after}]
        return [d for k in sorted(before) for d in differences(before[k],after[k],pointer+'/'+k.replace('~','~0').replace('/','~1'))]
    if isinstance(before,list):
        assert len(before)==len(after),(pointer,'list length changed')
        return [d for k,(a,b) in enumerate(zip(before,after)) for d in differences(a,b,pointer+'/'+str(k))]
    return [] if before==after else [{'pointer':pointer,'before':before,'after':after}]

environment=os.environ.copy()
environment['PHOTO_RUNTIME_STORE']=str(STORE)
environment['GEMINI_API_KEY']='';environment['GOOGLE_API_KEY']=''
commands=[('dictionary-validation',[sys.executable,str(S/'scripts/validate_photo_prompt_dictionary.py'),'--no-runtime-publication']),
          ('runtime-publication',[sys.executable,str(S/'scripts/publish_photo_runtime_snapshot.py'),'--runtime-store',str(STORE)])]
for label,cmd in commands:
    with (E/(label+'.stdout')).open('w') as out,(E/(label+'.log')).open('w') as err:
        subprocess.run(cmd,cwd=W,env=environment,stdout=out,stderr=err,check=True)

old=read(A/'photo_regression_baseline_v32.json')
cmd=list(old['command']);cmd[0]=sys.executable;cmd[-1]=str(E/'current-pack.json')
with (E/'current-pack-generation.log').open('w') as log:
    subprocess.run(cmd,cwd=W,env=environment,stdout=log,stderr=log,check=True)
newraw=(E/'current-pack.json').read_bytes();newpack=json.loads(newraw)[0]
previous=read(A/'photo_regression_baseline_v32_pack.json')
delta=differences(previous,[newpack])
save(E/'PACK-DELTA.json',delta)
allowed={'/0/core_retrieval/canonical_sha256','/0/core_retrieval/slot_corpus_sha256','/0/core_retrieval/slot_ownership_sha256','/0/pack_id','/0/provenance/tags_hash',
         '/0/creative_augmentation/candidates','/0/creative_augmentation/hard_eligible_pool_sha256','/0/semantic_clarification/candidates','/0/visual_concept_candidates/candidates',
         '/0/slots/color/candidate_count','/0/slots/color_grading/candidate_count','/0/slots/lighting/candidate_count','/0/slots/texture/candidate_count',
         '/0/slots/color_grading/candidates/1','/0/slots/texture/candidates/0'}
assert {r['pointer'] for r in delta}==allowed,[(r['pointer']) for r in delta]
for key in previous[0]:
    if key not in {'pack_id','core_retrieval','provenance','creative_augmentation','semantic_clarification','visual_concept_candidates','slots'}:
        assert previous[0][key]==newpack[key],key
for slot,oldslot in previous[0]['slots'].items():
    oldrows={r['id']:r for r in oldslot['candidates']};newrows={r['id']:r for r in newpack['slots'][slot]['candidates']}
    assert all(oldrows[k]==newrows[k] for k in oldrows.keys()&newrows.keys()),slot
assert all(r['opt_in_contract']['obligation']['activation']['source']=='composer_opt_in' for r in newpack['visual_concept_candidates']['candidates'])

parent=read(E/'V32-PARENT-SOURCE.json');before=read(E/'REMOTE-V32-SOURCE-BOUNDARY.json')
after=dict(before['photo_source_files'])
names=['photo_prompt_source_manifest.json','photo_prompt_palette_applications_extension.json','photo_prompt_visual_obligations_palette_applications.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']
after.update({str(S/'assets'/name):sha(W/S/'assets'/name) for name in names})
inventory={p.name:sha(p) for p in sorted((W/S/'assets').glob('*.json'))}
active={str(S/'assets'/row['path']):sha(W/S/'assets'/row['path']) for n in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json'] for row in read(W/S/'assets'/n)['shards']}
receipt=read(Path(str(E/'current-pack.json')+'.runtime-receipt.json'))
generation=read(STORE/'generations'/receipt['generation_id']/'manifest.json')
save(E/'CURRENT-GENERATION.json',generation)
save(E/'CURRENT-BOUNDARY-RECEIPT.json',receipt)
packpath=A/'photo_regression_baseline_v33_pack.json';packpath.write_bytes(newraw)
record=Path('docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_palette_applications_extension-20261006.json')
proof={'schema':'photo-palette-application-data-transition/v33','previous_qualified_commit':parent['source_pin'],'previous_qualified_tree':parent['source_tree'],
       'parent_manifest':str((E/'V32-PARENT-SOURCE.json').relative_to(W)),'parent_manifest_sha256':sha(E/'V32-PARENT-SOURCE.json'),'parent_member_count':parent['member_count'],
       'previous_manifest_sha256':sha(A/'photo_regression_baseline_v32.json'),'previous_pack_sha256':sha(A/'photo_regression_baseline_v32_pack.json'),
       'current_pack_sha256':sha(packpath),'previous_pack_id':previous[0]['pack_id'],'current_pack_id':newpack['pack_id'],'reviewed_pack_delta':delta,'allowed_pack_delta_pointers':sorted(allowed),
       'frozen_inputs':old['frozen_inputs'],'source_files_after':after,'source_inventory_before':before['source_inventory'],'source_inventory_after':inventory,
       'active_shards_after':active,'retained_shards_before':before['active_shards'],'preserved_source_paths':[str(S/'assets'/n) for n in ['photo_prompt_source_manifest.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']],
       'authored_data_changed':names[:3],'new_candidates':37,'new_profiles':13,'context_records':52,'held_claims':11,
       'maintenance_successor':{'path':str(record),'sha256':sha(W/record)},'evidence_files':{str(p.relative_to(W)):sha(p) for p in [E/'CURRENT-GENERATION.json',E/'CURRENT-BOUNDARY-RECEIPT.json',E/'INDEX-REBUILD.json',E/'MERGE-ADOPTION.json']},
       'generation_id':receipt['generation_id'],'source_fingerprint':receipt['source_fingerprint'],'algorithm_sha256':receipt['algorithm_sha256'],'receipt_sha256':sha(E/'CURRENT-BOUNDARY-RECEIPT.json'),
       'previous_validator_sha256':sha(E/'v32-parent-source-files'/I/'scripts/validate_illustration_assets.py'),'previous_universal_descriptor_sha256':sha(E/'v32-parent-source-files'/I/'assets/universal_scene_baseline_v2.json'),
       'preserved_request_scene_controls_hard_obligations_negative_and_budget':True,'preserved_public_candidate_count':64,'reviewed_optional_catalog_changes':True,'prior_native_image_tests':'Archived five native calls: new selected visual profiles qualified in two arms; synthetic scenarios one PASS, two FAIL; ordinary new candidates selected zero; user judgment pending. No merged-tree image call or causal improvement claim.'}
save(E/'V33-PALETTE-DATA-PROOF.json',proof)
baseline=copy.deepcopy(old)
baseline.update(schema='photo_regression_baseline/v33',created_at='2026-10-07',historical_baseline={'path':'photo_regression_baseline_v32.json','schema':'photo_regression_baseline/v32','sha256':sha(A/'photo_regression_baseline_v32.json')},
                sha256=sha(packpath),pack_id=newpack['pack_id'],change_scope='Add optional narrow palette applications and complete carrier-bound visual profiles to pulled V32 main; preserve exact V1--V32 replay and frozen request, hard duties, scene and public candidate count. Review bounded optional catalog changes explicitly.',
                purpose='Qualify palette authored sources and merged indexes separately from retained native partial failures and pending user acceptance.')
baseline['command'][-1]='/tmp/subculture-illustration-photo-baseline-v33.json'
baseline.pop('robe_source_transition')
baseline['palette_data_transition']={'evidence_path':str((E/'V33-PALETTE-DATA-PROOF.json').relative_to(W)),'evidence_sha256':sha(E/'V33-PALETTE-DATA-PROOF.json'),'previous_qualified_commit':parent['source_pin'],'parent_manifest_sha256':sha(E/'V32-PARENT-SOURCE.json')}
save(A/'photo_regression_baseline_v33.json',baseline)
print(json.dumps({'proof_sha256':sha(E/'V33-PALETTE-DATA-PROOF.json'),'parent_sha256':sha(E/'V32-PARENT-SOURCE.json'),'pack_delta_leaves':len(delta),'source_files_after':len(after),'asset_inventory_after':len(inventory),'parent_members':len(parent['members']),'generation_id':receipt['generation_id']},ensure_ascii=False,indent=2),flush=True)
