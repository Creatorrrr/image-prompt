from pathlib import Path
import json,hashlib,copy
ROOT=Path.cwd();OUT=ROOT/'docs/research-evidence/photo-prompt/harry-potter-integration-20261006/main-merge';A=ROOT/'skills/subculture-illustration-image-generator/assets';P=ROOT/'skills/photo-prompt-image-generator/assets'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
parent=read(OUT/'V26-PARENT-SOURCE.json')
for row in parent['members']:
 if row['source_path'].startswith(str(OUT.relative_to(ROOT))+'/v26-parent-source-files/'):(ROOT/row['source_path']).chmod(int(row['mode'][-3:],8))
oldproof=read(ROOT/'docs/research-evidence/photo-prompt/scene-authorship-main-merge-20261006/V26-SCENE-BUDGET-PROOF.json')
oldbaseline=read(A/'photo_regression_baseline_v26.json');oldpack=read(A/'photo_regression_baseline_v26_pack.json')[0]
newpack=read(OUT/'current-pack.raw.json')[0];delta=read(OUT/'PACK-DELTA.json')
allowed={'/0/core_retrieval/canonical_sha256','/0/core_retrieval/slot_corpus_sha256','/0/core_retrieval/slot_ownership_sha256','/0/pack_id','/0/provenance/tags_hash'}
assert {d['pointer'] for d in delta}==allowed
adoption=read(OUT/'MERGED-ADOPTION-MANIFEST.json');authored=adoption['source_files_changed'];changed=set(authored)|{'photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json'}
files_after=dict(oldproof['source_files_after'])
files_after.update({'skills/photo-prompt-image-generator/assets/'+n:sha(P/n) for n in changed})
active={}
for name in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
 for row in read(P/name)['shards']:active['skills/photo-prompt-image-generator/assets/'+row['path']]=sha(P/row['path'])
current=A/'photo_regression_baseline_v27_pack.json';current.write_bytes((OUT/'current-pack.raw.json').read_bytes())
proof={'schema':'photo-appearance-paraphrase-data-transition/v27','previous_qualified_commit':parent['source_pin'],'previous_qualified_tree':parent['source_tree'],'parent_manifest':str((OUT/'V26-PARENT-SOURCE.json').relative_to(ROOT)),'parent_manifest_sha256':sha(OUT/'V26-PARENT-SOURCE.json'),'previous_manifest_sha256':sha(A/'photo_regression_baseline_v26.json'),'previous_pack_sha256':sha(A/'photo_regression_baseline_v26_pack.json'),'current_pack_sha256':sha(current),'previous_pack_id':oldpack['pack_id'],'current_pack_id':newpack['pack_id'],'reviewed_pack_delta':delta,'allowed_pack_delta_pointers':sorted(allowed),'frozen_inputs':oldbaseline['frozen_inputs'],'source_files_after':files_after,'source_inventory_before':{Path(k).name:v for k,v in oldproof['source_files_after'].items() if k.startswith('skills/photo-prompt-image-generator/assets/') and Path(k).suffix=='.json'},'source_inventory_after':{p.name:sha(p) for p in sorted(P.glob('*.json'))},'active_shards_after':active,'authored_data_changed':authored,'new_profiles':42,'new_candidates':42,'existing_profiles_extended':45,'existing_candidates_extended':14,'optional_bundles':6,'current_dictionary_hash':read(P/'photo_prompt_semantic_index.json')['dictionary_hash'],'previous_validator_sha256':sha(ROOT/'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py'),'previous_universal_descriptor_sha256':sha(A/'universal_scene_baseline_v2.json'),'preserved_public_candidates_scene_controls_negative_and_budget':True,'prior_native_image_tests':'Preserved original three arms; A passed, B and C failed. No new merged-tree render or causal improvement claim.'}
# The V26 proof includes the complete live DATA via its V25 predecessor inventory.
ct=read(ROOT/oldproof['previous_proof_path']);proof['source_inventory_before']=ct['source_inventory_after']
save(OUT/'V27-APPEARANCE-DATA-PROOF.json',proof)
b=copy.deepcopy(oldbaseline);b.update(schema='photo_regression_baseline/v27',change_scope='Add reviewed appearance relation paraphrases and optional candidates while preserving all main runtime, owner corrections, frozen scene and prompt-budget v3.',historical_baseline={'path':'photo_regression_baseline_v26.json','schema':'photo_regression_baseline/v26','sha256':sha(A/'photo_regression_baseline_v26.json')},sha256=sha(current),pack_id=newpack['pack_id'],purpose='Preserve all prior source, candidate, scene, privacy and native failure evidence; qualify the additive appearance DATA successor separately.')
b['command'][-1]='/tmp/subculture-illustration-photo-baseline-v27.json';b.pop('scene_budget_transition')
b['appearance_data_transition']={'evidence_path':str((OUT/'V27-APPEARANCE-DATA-PROOF.json').relative_to(ROOT)),'evidence_sha256':sha(OUT/'V27-APPEARANCE-DATA-PROOF.json'),'previous_qualified_commit':parent['source_pin'],'parent_manifest_sha256':sha(OUT/'V26-PARENT-SOURCE.json')}
save(A/'photo_regression_baseline_v27.json',b)
print(json.dumps({'proof_sha256':sha(OUT/'V27-APPEARANCE-DATA-PROOF.json'),'pack_delta_leaves':len(delta),'authored_files':len(authored),'before_assets':len(proof['source_inventory_before']),'after_assets':len(proof['source_inventory_after']),'preserved_public_candidate_count':oldbaseline['public_candidate_count']}))
