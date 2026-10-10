import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
view = json.loads((ROOT / 'composer_view.json').read_text())
q = view['requirements']
core = q['authorial_core']
baseline = (ROOT / 'baseline_prompt_en.txt').read_text()

seat = "Beside her left thigh, the rust skirt gathers into short compressed folds where that same skirt meets the bench seat; a thin contact shadow follows the cloth-to-wood junction."
pleat = "Across the front of that rust skirt, long raised pleat ridges alternate with darker recessed valleys from the upper skirt down toward its lower hem, opening slightly over the bent knees."
weave = "On the moss jacket's turned cuff, a small stitched hem borders a locally readable weave. Fine interlaced yarns remain visible across the same textile surface beside its stitched edge."
hair = "A few short loose strands curve out from her own bob, remaining visibly rooted at the same temple."
ribbon = "The mustard ribbon tail rises from its attached hat-band anchor, with the pinned section staying against the crown."
air = "In the sea breeze, those rooted strands bend in fine small arcs while the wider attached ribbon makes a softer curl toward the same open harbor side."
face = "Her face retains readable features at the selected portrait scale."
hands = "The needle-holding hand and pinned ribbon fold remain legible together in the same focal zone."
place = "The ferry boarding ramp establishes the harbor setting through its recognizable outline beyond the bench."

prompt = baseline
clothing = "She wears an open moss-green cotton twill chore jacket over an ivory rib-knit scoop-neck top, with a rust-colored pleated midi skirt falling over her knees."
cuffs = "Rolled jacket cuffs expose a slightly lighter inner twill at her wrists; the outer sleeves retain small diagonal folds near the bent elbows."
old_air = "A sea breeze lifts only the free ribbon tail and a few short strands at her cheek while the held section stays pressed to the crown."
for old, new in (
    (clothing, clothing + ' ' + seat + ' ' + pleat),
    (cuffs, cuffs + ' ' + weave),
    (old_air, hair + ' ' + ribbon + ' ' + air),
    ("Make an observed travel lifestyle photograph from a front three-quarter viewpoint at conversational distance.", "Make an observed travel lifestyle photograph in a portrait two-by-three frame, from a front three-quarter viewpoint at conversational distance."),
    ("Use natural skin texture and enough depth of field for the needle-to-stitch connection and fabric surfaces to remain readable.", "Use natural skin texture and enough depth of field for the needle-to-stitch connection and fabric surfaces to remain readable. " + face + ' ' + hands + ' ' + place),
):
    assert prompt.count(old) == 1, old
    prompt = prompt.replace(old, new)

chosen = [
    'slot:body_pose:wkr_wk095_selected_relation_candidate',
    'bundle:suf_sf064_v1_bundle',
    'slot:motion:vg_shared_airflow_hair_ribbon',
]
visuals = [
    'visual-concept:wkr_wk047_selected_relation',
    'visual-concept:vg_face_hands_place_readability_profile',
]
interpretations = [
    {'candidate_id': chosen[0],
     'artistic_interpretation': "The skirt's local pressure trace gives the supported travel pause a concrete cloth-to-seat relationship beneath the sewing action.",
     'transformation': "Place compressed short folds beside the left thigh at the existing bench seat, separate from the ordered long front pleats; keep the original agent-authored bench because this source requires a seat surface, not a chair.",
     'prompt_evidence': seat,
     'relation_evidence': {'wkr_wk095_selected_relation_relation_1': seat}},
    {'candidate_id': chosen[1],
     'artistic_interpretation': "Ordered pleat relief creates a warm rhythmic field beneath the small hat stitch and separates the skirt from the knit and twill.",
     'transformation': "Let the seated knees gently spread long skirt pleats while upper-to-hem ridges and valleys remain one continuous rust garment, with seat pressure localized at the side.",
     'prompt_evidence': pleat,
     'component_evidence': {
         'component_1': 'long raised pleat ridges alternate with darker recessed valleys',
         'component_2': 'from the upper skirt down toward its lower hem',
         'owner_relation': 'Across the front of that rust skirt, long raised pleat ridges alternate with darker recessed valleys'},
     'relation_evidence': {'suf_sf064_v1_owner_relation': 'Across the front of that rust skirt, long raised pleat ridges alternate with darker recessed valleys'}},
    {'candidate_id': chosen[2],
     'artistic_interpretation': "Two already present materials respond to the harbor breeze and connect the loose ribbon to the traveler's need to repair it.",
     'transformation': "Keep fine bob strands rooted and the wider ribbon attached to the hat band, giving their separate arcs a shared harbor-side direction rather than disconnected floating fragments.",
     'prompt_evidence': air,
     'relation_evidence': {
         'vg_shared_airflow_hair_ribbon_r1': hair,
         'vg_shared_airflow_hair_ribbon_r2': ribbon,
         'vg_shared_airflow_hair_ribbon_r3': air}},
]

rejections = {
    'appearance_rel_h050': 'Eyeglass lenses and local eye magnification would add an optical object that does not develop the hat repair.',
    'chrh_rel_hair_color_state_lowlights': 'The supplied dark bob already guides the hair; separate darker color sections are not useful to the present repair.',
    'chrh_rel_hair_main_laid_edges': 'Sculpted forehead swoops would compete with the few wind-loosened strands and have no reference-established role.',
    'composite_overwhelmed_expression': 'The complete upward/asymmetric pupil, open mouth and external tongue combination expresses a different event from absorbed sewing.',
    'diegetic_reality_invariant_failure': 'A shared broken-world rule would become a separate premise; the saved surreal zero and this practical harbor repair favor physically coherent space.',
    'ed_cafe_pickup_wait': 'Counter, prepared drink and customer handoff relations belong to a different place and activity.',
    'ed_clean_room_reset': 'Returning an item beside a cleared indoor surface would replace the quay repair with another event.',
    'embodied_corruption_transition': 'An unfinished on-body corruption boundary would displace the practical travel task and introduce an unsupported state transition.',
    'kuudere_composed_warmth_relation': 'There is no same trusted counterpart receiving an already visible benefit; adding that relationship would create a second story.',
    'pc_pc23_owner_relation': 'A hand-supported mirror would consume an acting hand and compete with the needle and pinned ribbon.',
    'pr_camcorder_still_temporal_container': 'A video frame cue and motion trace do not improve this observed travel photograph or its small sewing contact.',
    'suf_sf062_v1': 'The authored midi garment can remain generic clothing; an additional rigid hem/lower-leg-gap opt-in is less useful than the seated cloth topology already chosen.',
    'wkr_wk104_selected_relation': 'The continuous chore-jacket sleeves have no separate upper-arm sleeve band or bodice-side gap; rolled cuffs cannot substitute for that relation.',
}
clarifications = []
for c in q['semantic_clarification']['candidates']:
    cid = c['id']
    if cid == 'clarification:authorial-core:interpreted-intent':
        x = {'clarification_id': cid, 'decision': 'applied', 'rationale': 'Preserve every requester-owned anchor and the typed reference-guided human category, keeping particulars agent-owned.', 'prompt_evidence': 'a coherent complex photographic scene'}
    elif c.get('profile_id') == 'vg_face_hands_place_readability_profile':
        x = {'clarification_id': cid, 'decision': 'applied', 'rationale': 'Shared readability of the face, sewing contact and harbor setting allows the repair to read as one situated action.', 'prompt_evidence': hands}
    elif c.get('profile_id') == 'wkr_wk047_selected_relation':
        x = {'clarification_id': cid, 'decision': 'applied', 'rationale': 'Apply the complete local yarn-interlace relation beside the stitched edge of the same turned moss cuff, without claiming fiber identity from pixels.', 'prompt_evidence': weave}
    else:
        x = {'clarification_id': cid, 'decision': 'rejected', 'rationale': rejections[c['profile_id']]}
    clarifications.append(x)

creative_rejections = {
    'slot:composition:wkr_wk111_selected_relation_candidate': "Its complete door-edge/shoulder overlap and visible garment-ribbon seam junction would require an extra foreground door and a different ribbon owner. The hat ribbon is not a garment seam, and that occlusion would weaken the repair.",
    'slot:footwear:spf_sf108_01': "Foot-crossing and ankle-circling sandal straps could be authored, but the retained ankle boots make the damp quay pause and travel ensemble more coherent. No foot-strap substitute is claimed.",
    'slot:expression:vel_small_lip_gap_concealed_teeth': "The baseline softly parted lips already support absorbed presence. Exact concealed-teeth and jaw geometry would over-specify a small expression without advancing the craft action.",
    'augmentation:adult_appeal:sensual:garment_detail:electric_static_cling_cloth': "A bounded patch against the thigh with converging folds is viable at the same strength, but the motivated skirt-seat compression better explains this supported pause; no additional cling patch is adopted.",
    'augmentation:adult_appeal:sensual:medium:pr_camcorder_still_temporal_container_candidate': "A visible video container, local motion trace and coherent video resolution are a possible portrayal, but their format would shift attention from the natural photographic sewing contact.",
}
creative = {'decisions': [
    {'candidate_id': cid, 'decision': 'rejected', 'rationale': creative_rejections[cid]}
    for cid in q['creative_augmentation']['candidates']['deferred_candidate_ids']
]}

contextual = [
    {'candidate_id': 'augmentation:adult_appeal:sensual:wardrobe_style:winter_wf24_v1_candidate', 'reading': 'potential',
     'reason': 'A double-breasted front is compatible with the invented traveler but would foreground formal closure over the practical open jacket.',
     'proposed_application': 'A moss coat could overlap its front panels broadly beneath two visible button rows while the same woman repairs the hat on the bench.'},
    {'candidate_id': 'augmentation:adult_appeal:sensual:garment_detail:electric_static_cling_cloth', 'reading': 'potential',
     'reason': 'A bounded local thigh contact is possible, but the chosen seat compression is better motivated by the supported pose.',
     'proposed_application': 'A small skirt patch could cling against the near thigh, with free fabric hanging beyond and small folds converging toward it; no electrical cause would be asserted.'},
    {'candidate_id': 'augmentation:adult_appeal:sensual:prop:electric_paper_attraction', 'reading': 'irrelevant',
     'reason': 'Paper pieces contacting a rod tip would add an unexplained second experiment. The hat, needle and pouch already explain the practical purpose.'},
    {'candidate_id': 'augmentation:adult_appeal:sensual:wardrobe_style:fit_ff03_v2_candidate', 'reading': 'potential',
     'reason': 'Roomy shoulder, sleeve and torso proportions could support an easy travel presence, but increased volume would compete with the cuff and fine sewing contact.',
     'proposed_application': 'The moss jacket could extend beyond her shoulders, with its sleeves and torso sharing enlarged proportions and rolled cuffs freeing the wrists for repair.'},
]

checks = {
    'body_ownership': {'status': 'supported', 'reason': 'One focal seated body owns the connected shoulders, forearms and separated repair hands; no second actor supplies a limb.', 'prompt_evidence': ['Both forearms belong visibly to her relaxed shoulders', 'Her left thumb and index finger press the folded ribbon', 'Her right hand holds a single slender needle']},
    'joint_chain_and_reach': {'status': 'supported', 'reason': 'Bent forward elbows bring separated hands to one hat on the lap; the needle is only a few centimeters above its band, with ordinary reachable wrist positions.', 'prompt_evidence': ['with elbows bent forward over her lap', 'her hands occupy separate spaces on either side of the stitch', 'a few centimeters above the band']},
    'support_and_balance': {'status': 'supported', 'reason': 'The retained bench bears seated weight, feet meet quay stones, and thighs support the hat; local skirt folds lie at that same bench contact.', 'prompt_evidence': ['The hat rests across her thighs', 'Her feet rest on the quay stones, knees support the hat, and the bench supports her seated weight.', seat]},
    'contact_and_space': {'status': 'supported', 'reason': 'Left fingers pin the band to the crown while the right hand raises the connected needle and thread in separate space. Bag and pouch leave both acting hands available; cloth compression stays at the bench junction.', 'prompt_evidence': ['Her left thumb and index finger press the folded ribbon against the straw crown.', 'The thread visibly connects that needle to the new stitch.', 'Rolled jacket cuffs expose a slightly lighter inner twill at her wrists', seat]},
    'visibility_and_projection': {'status': 'supported', 'reason': 'Front three-quarter full seated portrait keeps face, connected arms, sewing contact, supported lap and boots; the crown tilts toward the camera and the turned cuff, skirt-seat side and harbor ramp remain inspectable without replacing the scene with a texture crop.', 'prompt_evidence': ['Frame her head, connected shoulders and arms, the sewing contact and boots together', hands, place, weave]},
}
ph = hashlib.sha256(prompt.encode()).hexdigest()
result = {
    'pack_id': q['pack_id'], 'composer': 'agent', 'prompt_en': prompt,
    'negative_en': q['negative_en'], 'chosen_candidate_ids': chosen,
    'chosen_visual_concept_ids': visuals, 'candidate_interpretations': interpretations,
    'authorial_core_binding': {
        'source_authorial_core_sha256': core['canonical_sha256'],
        'source_intent_lock_sha256': core['intent_lock']['canonical_sha256'],
        'preserved_anchor_ids': [x['anchor_id'] for x in core['intent_lock']['semantic_anchors']],
        'preserved_evidence': [],
        'authorial_decisions': [
            {'dimension': 'material', 'decision': 'Localize short pressure folds at the same skirt-to-bench contact and show cuff weave beside its own stitched edge.', 'rationale': 'Material relationships explain support and repair-ready clothing while preserving the original bench.'},
            {'dimension': 'appearance', 'decision': 'Continue long pleat ridges and recessed valleys down the rust skirt.', 'rationale': 'Ordered garment relief stays distinct from local seat pressure and the jacket weave.'},
            {'dimension': 'action', 'decision': 'Give rooted short hair and the anchored hat ribbon different arcs toward the same harbor side.', 'rationale': 'The shared breeze links the visible loose band to the practical repair.'},
            {'dimension': 'camera', 'decision': 'Keep facial features, needle-hand contact and recognizable ferry setting jointly legible.', 'rationale': 'The image needs a readable person, purposeful contact and waiting place together.'},
            {'dimension': 'format', 'decision': 'Use a portrait two-by-three frame retaining boots, supported lap and a narrow harbor strip.', 'rationale': 'The person and repair carry the photograph while material and place cues remain subordinate.'},
        ],
    },
    'semantic_clarification_decisions': clarifications,
    'creative_augmentation_brief': creative,
    'semantic_assertion_evidence': {
        'source_contract_sha256': q['semantic_assertion_obligations']['canonical_sha256'],
        'evidence': {'reference_human_subject': {'subject_phrase': 'a woman whose visible face and hair follow the supplied reference image'}},
    },
    'visual_obligation_evidence': {
        'wkr_wk047_selected_relation': {'component_1_phrase': weave},
        'vg_face_hands_place_readability_profile': {'component_1_phrase': face, 'component_2_phrase': hands, 'component_3_phrase': place},
    },
    'adult_appeal_brief': {
        'agency_phrase': 'Her left thumb and index finger press the folded ribbon against the straw crown.',
        'axes': {
            'sensual': {'intensity': 1, 'realization': 'baseline', 'affected_dimensions': [], 'artistic_interpretation': 'The original absorbed gaze, natural lips and open practical ensemble keep everyday attraction a subtle supporting quality of the repair.', 'prompt_evidence': 'She looks down at the stitch with patient concentration, lips softly parted, shoulders at ease'},
            'fetish': {'intensity': 0, 'realization': 'baseline', 'affected_dimensions': [], 'artistic_interpretation': 'The saved zero retains the ordinary repair and clothing without added fetish significance or treatment.', 'prompt_evidence': 'a person absorbed in a practical task'},
        },
        'blend': {'emphasis': 'sensual_led'},
        'contextual_review': contextual,
        'contextual_comparison': 'At the same saved sensual 1/fetish 0 strengths, broad coat closure would foreground formal styling, enlarged jacket proportions would foreground volume, and a local cloth-cling patch would foreground the thigh. Those coherent alternatives remain optional and less useful to this small practical travel pause. Retain baseline absorbed presence and open twill/knit ensemble, developing the motivated seat pressure, cuff weave, pleat relief and harbor breeze as ordinary scene relationships.',
    },
    'embodiment_review': {
        'source_contract_sha256': q['embodiment_preflight']['canonical_sha256'],
        'review': {'contract_version': 'photo-embodiment-review/v1', 'provenance': 'agent_postcomposition', 'prompt_sha256': ph, 'scope': 'body_action', 'summary': 'One traveler repairs a hat supported by her lap on the retained wooden bench. Both acting arms reach one band; local skirt pressure, cuff yarns and shared breeze retain their own owners while face, hands and place remain jointly assessable.', 'checks': checks},
    },
}
for a in core['intent_lock']['semantic_anchors']:
    assert a['prompt_evidence'] in prompt
for c in checks.values():
    assert all(s in prompt for s in c['prompt_evidence'])
assert 48 <= len(prompt.split()) <= 1280
(ROOT / 'composed_prompt.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'prompt_en.txt').write_text(prompt)
(ROOT / 'negative_en.txt').write_text(q['negative_en'])
(ROOT / 'composition_self_review.json').write_text(json.dumps({
    'provenance': 'agent_postcomposition', 'review_count': 1, 'prompt_sha256': ph,
    'word_count': len(prompt.split()), 'status': 'supported',
    'whole_scene': 'The supported ferry-quay hat repair remains one coherent present event; colors, local cloth behavior and accessory junctions support the traveler rather than an inventory.',
    'owner_and_contact_review': 'One needle belongs to the right hand, one ochre thread connects it to the stitch, left fingers pin the same ribbon, hat rests on thighs, seat folds belong to the same rust skirt, weave and stitched hem share one cuff, rooted hair and anchored ribbon respond with separate forms.',
    'candidate_boundaries': 'Rolled cuffs are not detached upper-arm sleeves; the hat ribbon is not a garment-seam knot; bench is a valid seat surface; no yarn pattern proves cotton composition or causal wind from a still image.',
    'controls': {'sensual': 1, 'fetish': 0, 'surreal': 0, 'creativity': 1, 'unchanged': True},
    'method_limit': 'Core/baseline/controls match the diagnostic run byte-for-byte, but retrieval seeds differ (1872214162960451119 versus 7180700068034827031). This is runtime-use qualification, not a matched before/after causal experiment.',
    'pixel_proof': 'pending_first_native_image',
}, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'new_wkr_selection.json').write_text(json.dumps({
    'pack_id': q['pack_id'], 'source_generation': 'c68a7d2e44db608a6372800dae6f51dc99ca907bfb561e6e5c8fd05aae262f14',
    'selected': [
        {'id': chosen[0], 'reason': interpretations[0]['transformation'], 'full_detail_source': 'considered_details.json'},
        {'id': visuals[0], 'reason': 'The existing twill cuff has a stitched hem and can carry complete local weave beside it; actual native yarn interlace will be judged strictly.', 'full_detail_source': 'considered_details.json'},
    ],
    'rejected': [
        {'id': 'slot:composition:wkr_wk111_selected_relation_candidate', 'reason': creative_rejections['slot:composition:wkr_wk111_selected_relation_candidate']},
        {'id': 'visual-concept:wkr_wk104_selected_relation', 'reason': rejections['wkr_wk104_selected_relation']},
        {'id': 'bundle:wkr_wk095_selected_relation_bundle', 'reason': 'Its complete seat-contact meaning is tested through the ordinary candidate; duplicate bundle adoption would add no different relation.'},
        {'id': 'bundle:wkr_wk111_selected_relation_bundle', 'reason': 'The same complete door/shoulder/garment-ribbon relation is declined for the ordinary candidate; no owner substitution is made.'},
    ],
    'no_cross_arm_inputs': True,
}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'pack_id': q['pack_id'], 'prompt_sha256': ph, 'word_count': len(prompt.split()), 'chosen': chosen, 'visuals': visuals}, ensure_ascii=False))
