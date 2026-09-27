from pathlib import Path
import json,hashlib,copy,subprocess,datetime
p=Path(__file__).resolve().parent; read=lambda n:json.loads(p.joinpath(n).read_text()); write=lambda n,d:p.joinpath(n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n'); sha=lambda b:hashlib.sha256(b).hexdigest()
pack=read('candidate_pack.json');pack=pack[0] if isinstance(pack,list) else pack
core=pack['authorial_core']; lock=core['intent_lock']; baseline=core['baseline_prompt_en']
framing='The frame leaves a narrow band of floor beyond both shoes, so the brush contact and seated support can be traced in one reading.'
light="Daylight fades gently across the tabletop toward the drying boards; the woman's sleeve and the pigment dish cast soft shadows in the same direction."
contact='A fine contact shadow joins the bristle tips to the sheet along the pressing stroke.'
material='Uneven deckled edges and tiny fiber flecks remain legible around the smooth newly flattened patch.'
prompt=' '.join((baseline+' '+framing+' '+light+' '+contact+' '+material).split())
chosen=['slot:lighting:soft_window','slot:shot_scale:full_length_body_shot','integration:physical_contact','integration:material_trace']
interpretations=[
 {'candidate_id':chosen[0],'artistic_interpretation':'A single diffuse window source unifies the actor with the work surfaces.','transformation':'Relate the window gradient to the sleeve, paper workspace and pigment dish shadows.','prompt_evidence':light},
 {'candidate_id':chosen[1],'artistic_interpretation':'Body coverage is necessary to read upper-near and lower-receding perspective.','transformation':'Keep a floor margin past both shoes while the work contact and stool remain assessable.','prompt_evidence':framing},
 {'candidate_id':chosen[2],'artistic_interpretation':'Fine bristle contact establishes the action at the paper surface.','transformation':'Use the joined bristle-tip shadow to expose the exact pressing stroke.','prompt_evidence':contact},
 {'candidate_id':chosen[3],'artistic_interpretation':'Local paper fibers and edge irregularity reveal the material being flattened.','transformation':'Contrast an uneven deckled boundary with a smooth newly flattened paper patch.','prompt_evidence':material}
]
rejection_reasons={
 'bust_prominence_relation':'Regional breast geometry would change the reference-guided subject instead of clarifying elevated camera projection.',
 'diamond_central_torso_silhouette_relation':'A central torso silhouette is unrelated to camera elevation and introduces body-shape staging.',
 'hands_free_supported_drink_load':'It would replace the brush-paper interaction and the two working hand positions.',
 'inverted_triangle_upper_body_dominant_relation':'Body breadth is not a substitute for upper-near lower-receding camera perspective.',
 'kuudere_composed_warmth_relation':'Relationship behavior and a counterpart are absent from the independently frozen scene.',
 'pc_pc02_owner_relation':'Camera-addressed eye contact and a head turn would change the task-directed action.',
 'pc_pc03_owner_relation':'An across-table companion perspective is unnecessary and risks substituting another camera meaning.',
 'pr_instant_print_material_object':'An instant print card is a different action-bearing object from the paper sheet.'}
clar=[]
for c in pack['semantic_clarification']['candidates']:
 cid=c['id']
 if c.get('required_in_final_prompt'):clar.append({'clarification_id':cid,'decision':'applied','rationale':'Preserve the independently frozen elevated oblique camera meaning and coherent working scene.','prompt_evidence':'The elevated oblique viewpoint looks downward across the subject and the work surface'})
 else:clar.append({'clarification_id':cid,'decision':'rejected','rationale':rejection_reasons.get(c.get('profile_id'),'Unnecessary optional meaning for the frozen scene.')})
creasons={
 'slot:apparatus_pov:two_way_mirror_pov':'A mirror apparatus changes the locked camera viewpoint and supplies an unrelated observation device.',
 'slot:camera_direction:over_shoulder_observer_clean':'An over-shoulder observer view changes the locked elevated downward viewpoint.',
 'slot:location:brutalist_plaza':'A concrete plaza would discard the independently fixed paper studio.',
 'slot:body_orientation:pc_px01_component_2':'Separate crop and facial direction wording adds no needed realization and risks changing fixed body visibility.',
 'slot:gaze_engagement:direct_camera_aware':'Camera gaze introduces an unrequested expression dimension and distracts from brush contact.',
 'slot:light_type:golden_hour':'Golden light changes the randomized diffuse north-window source rather than improving its legibility.'}
creative=[{'candidate_id':c['id'],'decision':'rejected','rationale':creasons[c['id']]} for c in pack['creative_augmentation']['candidates']]
rev=copy.deepcopy(read('embodiment_review.json')); rev['provenance']='agent_postcomposition';rev['prompt_sha256']=sha(prompt.encode());rev['summary']='The complete final prompt preserves connected working arms, seated stool and floor support, brush-paper contact and the elevated oblique projection. Added floor margin and a shared daylight gradient improve assessability; material texture and contact shadows do not change the frozen mechanism.';rev['checks']['visibility_and_projection']['prompt_evidence'].append(framing);rev['checks']['contact_and_space']['prompt_evidence'].append(contact)
comp={'pack_id':pack['pack_id'],'prompt_en':prompt,'negative_en':pack['negative_en'],'composer':'agent','chosen_candidate_ids':chosen,'chosen_visual_concept_ids':[],'candidate_interpretations':interpretations,'authorial_core_binding':{'source_authorial_core_sha256':core['canonical_sha256'],'source_intent_lock_sha256':lock['canonical_sha256'],'preserved_anchor_ids':[a['anchor_id'] for a in lock['semantic_anchors']],'preserved_evidence':['her right hand holds the brush against the paper while her left palm steadies its far corner','Her hips rest on a square wooden stool, both feet rest on the floor','Diffuse north-window daylight reveals the paper fibers, linen folds, and soft hand shadows'],'authorial_decisions':[{'dimension':'framing','decision':framing,'rationale':'Keep the action and both support paths readable together to judge elevated projection.'},{'dimension':'lighting','decision':light,'rationale':'Make one source of daylight connect subject, workspace and material surfaces.'}]},'semantic_clarification_decisions':clar,'creative_augmentation_brief':{'decisions':creative},'semantic_assertion_evidence':{'source_contract_sha256':pack['semantic_assertion_obligations']['canonical_sha256'],'evidence':{r['assertion_id']:r['frozen_evidence'] for r in pack['semantic_assertion_obligations']['obligations']}},'embodiment_review':{'source_contract_sha256':pack['embodiment_preflight']['canonical_sha256'],'review':rev}}
write('composed_prompt.json',comp);p.joinpath('final_prompt_en.txt').write_text(prompt+'\n');p.joinpath('request_original.txt').write_text(read('request_envelope.json')['request_text']);write('chosen_candidate_ids.json',chosen)
view=read('composer_view.json');details=read('selected_candidate_details.json')
write('candidate_exposure_and_selection.json',{'pack_id':pack['pack_id'],'pack_count':1,'composer_overview_read_before_details':True,'overview_path':str(p/'composer_view.json'),'overview_sha256':sha((p/'composer_view.json').read_bytes()),'catalog_ids_exposed_in_compact_view':[c['id'] for c in view['candidate_catalog']],'full_detail_ids_read':[c['id'] for c in details['candidates']],'selected_candidate_ids':chosen,'selected_visual_concept_ids':[],'selection_records':interpretations,'clarification_decisions':clar,'creative_decisions':creative,'ordinary_unselected_rule':'All other ordinary candidates are unselected optional suggestions; none creates a prompt or pixel obligation. Candidates replacing subject, paper action, studio, or locked camera meaning are rejected.','retrieval_observation':'coverage.intent_constraints.domains includes food through the ambiguous agent staging token dish in pigment dish. This is post-core retrieval routing drift, not a requester definition or allowed scene replacement.'})
ref='89384cd990223b4e4e44404253f554f23d8cbd3c'
subprocess.run(['git','archive','--format=tar','--output='+str(p/'skill_source_snapshot.tar'),ref,'skills/photo-prompt-image-generator'],check=True)
write('source_snapshot.json',{'source_ref':ref,'skill_path':'skills/photo-prompt-image-generator','skill_sha256':sha(Path('skills/photo-prompt-image-generator/SKILL.md').read_bytes()),'skill_tree_working_changes':[],'snapshot_tar':str(p/'skill_source_snapshot.tar'),'snapshot_tar_sha256':sha((p/'skill_source_snapshot.tar').read_bytes()),'source_basis':'git HEAD skill tree verified clean at run time; archive is provenance, not initial meaning input','imagegen_skill_sha256':sha(Path('/Users/chasoik/.codex/skills/.system/imagegen/SKILL.md').read_bytes()),'recorded_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
print(json.dumps({'pack_id':pack['pack_id'],'canonical_core_sha256':core['canonical_sha256'],'intent_lock_sha256':lock['canonical_sha256'],'final_prompt_sha256':sha(prompt.encode()),'prompt_words':len(prompt.split()),'chosen':chosen},indent=2))
