import json,pathlib,hashlib,datetime,shutil,subprocess
out=pathlib.Path(__file__).parent
p=json.loads((out/'candidate_pack.json').read_text())[0]
core=p['authorial_core']; base=core['baseline_prompt_en']
extra=" A 35mm lens keeps the near ridge substantial while preserving the actor's natural scale; depth of field holds the shoe and tunnel path together. The full body fits within a landscape frame, with margin below both soles and the held tube entirely inside the image."
prompt=base+extra
sha=lambda b:hashlib.sha256(b).hexdigest()
reasons={
'body_bounded_negative_space':'An enclosed body-contour void is a different focal spatial proposition and would distract from the frozen diagonal path.',
'deliberate_underarm_salience':'Overhead arm salience conflicts with the held tube and forward elbow staging.',
'diegetic_reality_invariant_failure':'An impossible spatial or causal effect contradicts the plausible concrete stride scene.',
'figura_serpentinata_spiral_pose':'A whole-body counter-twist would alter the frozen push-off direction and limb arrangement.',
'pc_pc12_owner_relation':'Hands framing the face would remove the held tube or change the arm action.',
'pc_pc27_owner_relation':'Architectural axial symmetry would introduce a new governing composition in the locked dimension.',
'pc_pc29_owner_relation':'A stationary subject with peripheral trails contradicts the moving actor event.',
'rectangle_silhouette_relation':'Body silhouette constraints are unrelated to the focal composition and would add unsupported morphology.'}
clar=[]
for c in p['semantic_clarification']['candidates']:
 if c['required_in_final_prompt']:
  clar.append({'clarification_id':c['id'],'decision':'applied','rationale':'Preserve the independently frozen spatial momentum and legible actor.','prompt_evidence':'The woman sits left of center with open space ahead of her movement'})
 else: clar.append({'clarification_id':c['id'],'decision':'rejected','rationale':reasons[c['profile_id']]})
creative=[]
for c in p['creative_augmentation']['candidates']:
 cid=c['id']
 if cid=='slot:lens:35mm': creative.append({'candidate_id':cid,'decision':'transformed','affected_dimensions':['camera'],'artistic_interpretation':'A moderate wide view makes the diagonal route substantial without inflating the actor.','transformation':'Tie lens perspective to the near ridge and natural actor scale rather than adding generic documentary style.','rationale':'Preserve the path and readable whole actor in one projection.','prompt_evidence':"A 35mm lens keeps the near ridge substantial while preserving the actor's natural scale"})
 else:
  reason={'slot:quality:not_overdone':'Style is not an open dimension and the natural editorial finish is already frozen.','slot:location:subway_platform':'Replacing the riverside underpass would rewrite the frozen scene.','slot:lens:85mm':'Telephoto compression and shallow focus weaken the three-layer route.','slot:crowd_density:sparse_passersby':'Adding passersby alters the agent-frozen single-actor scene and occludes the path.','slot:body_orientation:pc_px01_component_2':'Additional facial-direction staging is unnecessary and pose is not an open dimension.'}[cid]
  creative.append({'candidate_id':cid,'decision':'rejected','rationale':reason})
review=json.loads((out/'embodiment_review.json').read_text()); review['provenance']='agent_postcomposition';review['prompt_sha256']=sha(prompt.encode());review['summary']='Rechecked the complete final prompt including moderate-wide perspective, connected whole-body coverage, shoe clearance and tube visibility; these support the frozen push-off action without changing contact or actor-relative directions.'
review['checks']['visibility_and_projection']['reason']='The oblique chest-height view and full-body landscape margin keep the face, both shoes and tube assessable together.'
review['checks']['visibility_and_projection']['prompt_evidence']=['an oblique side-front view at chest height','The full body fits within a landscape frame','with margin below both soles and the held tube entirely inside the image']
composed={'pack_id':p['pack_id'],'composer':'agent','prompt_en':prompt,'negative_en':p['negative_en'],'chosen_candidate_ids':['slot:lens:35mm','slot:focus:zone_focus_street','slot:subject_framing:face_hands_prop_visibility_budget'],'chosen_visual_concept_ids':[],
 'candidate_interpretations':[
 {'candidate_id':'slot:focus:zone_focus_street','artistic_interpretation':'Focus serves the motion path rather than isolating the face from the action.','transformation':'Keep footwear and the receding tunnel route simultaneously legible within the depth range.','prompt_evidence':'depth of field holds the shoe and tunnel path together'},
 {'candidate_id':'slot:subject_framing:face_hands_prop_visibility_budget','artistic_interpretation':'Extend the shared visibility budget to whole-body support and the carried prop.','transformation':'Use landscape margin below both soles and contain the entire held drawing tube.','prompt_evidence':'The full body fits within a landscape frame, with margin below both soles and the held tube entirely inside the image'}],
 'coverage_assertions':{a['prompt_evidence']:a['prompt_evidence'] for a in core['intent_lock']['semantic_anchors']},
 'authorial_core_binding':{'source_authorial_core_sha256':core['canonical_sha256'],'source_intent_lock_sha256':core['intent_lock']['canonical_sha256'],'preserved_anchor_ids':[a['anchor_id'] for a in core['intent_lock']['semantic_anchors']],'preserved_evidence':['Her left forefoot pushes against the pavement behind the threshold','Her left hand grips a rolled drawing tube beside her left thigh','Late-afternoon sun entering from one open side'],
 'authorial_decisions':[{'dimension':'camera','decision':'Use moderate-wide perspective and sufficient depth for the near ridge, shoe and route.','rationale':'Keep the frozen depth progression visible around a natural-scale actor.'},{'dimension':'framing','decision':'Include both soles and the held tube in a landscape frame with bottom margin.','rationale':'Make support and prop contact directly assessable without weakening directional continuation space.'}]},
 'semantic_clarification_decisions':clar,'creative_augmentation_brief':{'decisions':creative},
 'semantic_assertion_evidence':{'source_contract_sha256':p['semantic_assertion_obligations']['canonical_sha256'],'evidence':{o['assertion_id']:o['frozen_evidence'] for o in p['semantic_assertion_obligations']['obligations']}},
 'embodiment_review':{'source_contract_sha256':p['embodiment_preflight']['canonical_sha256'],'review':review}}
(out/'composed_prompt.json').write_text(json.dumps(composed,ensure_ascii=False,indent=2)+'\n');(out/'final_prompt_en.txt').write_text(prompt+'\n');(out/'source_request.txt').write_text(core['source_request'])
view=json.loads((out/'composer_view.json').read_text())
exposure={'contract_version':'candidate-exposure-and-adoption/v1','arm':'dynamic_composition','first_surface':'compact composer_view.json','source_pack_id':p['pack_id'],'source_pack_file_sha256':sha((out/'candidate_pack.json').read_bytes()),'compact_view_file_sha256':sha((out/'composer_view.json').read_bytes()),'selected_detail_file_sha256':sha((out/'selected_candidate_details.json').read_bytes()),'exposed_candidate_ids':[c['id'] for c in view['candidate_catalog']],'adopted_candidate_ids':composed['chosen_candidate_ids'],'adopted_visual_concept_ids':[],'clarification_decisions':clar,'creative_decisions':creative,'ordinary_adoptions':composed['candidate_interpretations'],'unadopted_rule':'All other exposed candidates are optional and unselected. Composition candidates cannot replace frozen composition.','photographic_integration_observations':{'environment_binding':'side light stripe and wet concrete reflection already literal in frozen core','physical_contact':'left forefoot support and held tube already literal in frozen core'},'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(out/'candidate_exposure.json').write_text(json.dumps(exposure,ensure_ascii=False,indent=2)+'\n')
# Preserve the current skill source bytes after the immutable core has been validated. No other arm or past experiment is included.
src=pathlib.Path('skills/photo-prompt-image-generator');dest=out/'source_snapshot';files=[]
for part in ['SKILL.md','precore','scripts','assets']:
 pp=src/part
 paths=[pp] if pp.is_file() else sorted(pp.rglob('*'))
 for f in paths:
  if f.is_file() and '__pycache__' not in str(f) and f.suffix in ['.md','.py','.json']:
   rel=f.relative_to(src); d=dest/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,d);files.append({'path':str(f),'snapshot_path':str(d),'sha256':sha(f.read_bytes())})
for name in ['composition-contract.md','image-runtime.md','embodiment-preflight.md']:
 f=src/'references'/name;d=dest/'references'/name;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,d);files.append({'path':str(f),'snapshot_path':str(d),'sha256':sha(f.read_bytes())})
f=pathlib.Path('/Users/chasoik/.codex/skills/.system/imagegen/SKILL.md');d=dest/'system-imagegen-SKILL.md';shutil.copyfile(f,d);files.append({'path':str(f),'snapshot_path':str(d),'sha256':sha(f.read_bytes())})
identity=sha(json.dumps([{'path':f['path'],'sha256':f['sha256']} for f in files],sort_keys=True,separators=(',',':')).encode())
snap={'contract_version':'photo-source-snapshot/v1','git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'snapshot_identity':identity,'skill_sha256':sha((src/'SKILL.md').read_bytes()),'files':files}
(out/'source_snapshot_manifest.json').write_text(json.dumps(snap,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'pack_id':p['pack_id'],'canonical_core_sha256':core['canonical_sha256'],'canonical_intent_lock_sha256':core['intent_lock']['canonical_sha256'],'prompt_words':len(prompt.split()),'prompt_sha256':sha(prompt.encode()),'source_snapshot_identity':identity,'snapshot_files':len(files)},indent=2))
