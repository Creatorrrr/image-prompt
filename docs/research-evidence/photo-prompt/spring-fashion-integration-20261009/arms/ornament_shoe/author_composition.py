import hashlib
import json
from pathlib import Path

ARM = Path(__file__).resolve().parent
PACK = json.loads((ARM / 'run/revisions/0706f0abc2614555aff88abff03eb942/pack.json').read_text())[0]

PROMPT = """A spring fashion photograph of a person guided by the supplied reference, with visible facial features and short black hair guided by the supplied portrait. Spring clothing structures are visibly worn within a particular moment of ordinary work. Use the attached portrait for the visible face and short black bob with fine forehead fringe. At a small ferry landing just after morning rain, she sits on a low timber bench and clips the loosened upper corner of a rain-warped route sheet back onto the wire of a narrow notice frame beside her. The other upper corner is already fastened; a damp crease runs diagonally across the paper, and a small ferry is entering the gap between the landing posts. Her fingertips finish the fastening as her chin turns slightly toward the returning boat, a small easing of her lips giving the otherwise concentrated face an approachable warmth.

She wears a pale apricot blouse beneath a sage apron-style dress. The sage bib front is physically joined at its two upper corners to the dress's own narrow shoulder straps, with both joins exposed beside the apricot chest fabric. The bib and straps sit outside a separately worn apricot blouse, whose sleeves, neckline and visible side sections retain their own edges. These two garments belong to the seated woman. The blouse has soft diagonal folds descending from her left shoulder toward the opposite waist. A fabric flower is fixed at the left shoulder: separate curled petal edges gather around a compact center, and the flower's base sits flush against the blouse at that single attachment point. Its fold starts remain visible below the flower and above the low bib edge.

The sage dress is one garment from neckline to hem, with an A-line dress silhouette opening below the fitted waist. Its visible waist seam and closure connect the bib to the skirt: a small side fastening gathers the overlapping front panel at the waist, and the panel's diagonal free edge lies above an under-panel. Below this edge, repeated narrow vertical pleats open slightly over the nearer bent knee and continue into long folds below it. The sage drape continues into the hem. Keep the upper strap joins, bib edge, waist seam and lower panel continuous so the whole dress reads as one garment. The apron is clothing worn over a blouse, with raised fabric panel edges and contact shadows that resolve the layer order.

Her hips are supported by the bench, her torso faces the camera in a relaxed three-quarter orientation, and her left palm rests beside her hip on the seat. Her right arm reaches sideways to the notice frame at shoulder level, with the elbow softly bent and the right thumb and forefinger pressing a wooden clip over the paper and wire. The frame stands close enough that her shoulder remains over her seated pelvis. Both feet rest flat on the planks, the nearer foot half a shoe-length ahead and angled outward. The hem ends above her ankles. Each ivory flat has a rounded shallow toe and one solid narrow instep strap arching over the top of her foot. The strap's inner end joins the inner side of that same flat, and its outer end closes onto the outer side of that same flat. Show both contacts on each shoe. Separate thin ribbons start at rear side fittings of each flat, form an X over that foot's instep, continue around the same ankle and finish in a small tied bow. Keep these ribbon paths clear of the solid strap and hem.

Use a vertical head-to-toe view from just below her seated eye level, looking obliquely across the bench so the face, shoulder flower, apron joins, wrap edge, lower pleats and both shoes have room to resolve. The board occupies a slim zone beside her reaching hand, leaving the center of the clothing visible. Darkened wet planks and a pale reflection under the bench carry the recent rain; the small boat and bright channel sit farther behind her. Soft directional daylight gives the flower and sage panel edges shallow contact shadows, catches the pleat ridges and separates the shoe straps from skin. Let quiet concentration lead, the repaired corner connect the scene to a returning journey, and the folding rhythms of paper and clothing support that moment. Keep the subject tactile and the background gently quieter."""

apron_evidence = {
    'component_1': "The sage bib front is physically joined at its two upper corners to the dress's own narrow shoulder straps, with both joins exposed beside the apricot chest fabric",
    'component_2': 'The bib and straps sit outside a separately worn apricot blouse, whose sleeves, neckline and visible side sections retain their own edges',
}
shoe_evidence = {
    'component_1': 'one solid narrow instep strap arching over the top of her foot',
    'component_2': "The strap's inner end joins the inner side of that same flat, and its outer end closes onto the outer side of that same flat",
}
chosen = ['bundle:spf_sf071_1_bundle', 'bundle:spf_sf107_02_bundle']
interpretations = [
    {'candidate_id': chosen[0], 'artistic_interpretation': 'The sage outer dress creates visible joins and layer edges within the practical ferry repair scene; the separate blouse preserves the shoulder flower and warm spring palette.', 'transformation': 'Replace the authorial standalone skirt with one sage bib-to-hem apron dress over the independently worn blouse, while keeping the panel overlap and lower pleats.', 'prompt_evidence': apron_evidence['component_1'], 'component_evidence': apron_evidence, 'relation_evidence': {'existing_wearer_scope': 'These two garments belong to the seated woman', 'sf071_1_relation_1': apron_evidence['component_1'], 'sf071_1_relation_2': apron_evidence['component_2']}},
    {'candidate_id': chosen[1], 'artistic_interpretation': 'A solid ivory strap makes the shoe-to-foot connection inspectable while thinner ankle ribbons retain the baseline folding rhythm.', 'transformation': 'Add a separate narrow instep bridge attached to the two opposite upper sides of each flat; retain the ankle ribbons on distinct rear fittings.', 'prompt_evidence': "The strap's inner end joins the inner side of that same flat, and its outer end closes onto the outer side of that same flat", 'component_evidence': shoe_evidence, 'relation_evidence': {'sf107_02_edge_1': shoe_evidence['component_1'], 'sf107_02_edge_2': "The strap's inner end joins the inner side of that same flat", 'sf107_02_edge_3': 'its outer end closes onto the outer side of that same flat'}},
]

clarification_reasons = {
    'authorial-core:interpreted-intent': ('applied', 'Preserve the frozen spring photograph, human subject, visibly worn clothing and reference appearance anchors.', 'A spring fashion photograph of a person guided by the supplied reference'),
    'visual-profile:one_piece_dress_construction': ('applied', 'The outer bib, waist seam and lower panel now form a deliberately selected continuous sage dress.', 'The sage dress is one garment from neckline to hem'),
    'visual-profile:mg_paper_cut_relation': ('rejected', 'The route sheet is a single rain-warped document; layered cut-paper artwork would change its practical role.', None),
    'visual-profile:sheer_garment_optical_layering': ('rejected', 'The blouse and sage outer garment are opaque layers; light transmission is outside this selected construction.', None),
    'visual-profile:embodied_corruption_transition': ('rejected', 'No bodily dark-state transition belongs to the ordinary dock repair event.', None),
    'visual-profile:hands_free_supported_drink_load': ('rejected', 'The hands support a clip and bench contact; there is no drink load to balance.', None),
    'visual-profile:kuudere_composed_warmth_relation': ('rejected', 'The expression is independently authored everyday concentration; a target-directed archetype relation is not selected.', None),
    'visual-profile:pfe_one_shoulder': ('rejected', 'A blouse flower on one shoulder does not create the asymmetric covered and exposed shoulder geometry of that optional profile.', None),
    'visual-profile:rectangle_silhouette_relation': ('rejected', 'The scene specifies garment joins and an A-line dress; anatomical width ratios are not an adopted portrayal requirement.', None),
}
clarifications = []
for row in PACK['semantic_clarification']['candidates']:
    decision, rationale, evidence = clarification_reasons[row['id'].removeprefix('clarification:')]
    r = {'clarification_id': row['id'], 'decision': decision, 'rationale': rationale}
    if evidence:
        r['prompt_evidence'] = evidence
    clarifications.append(r)

augmentation_reasons = {
    'slot:eye_detail:sca_f04': 'A newly prescribed scleral band would redirect facial appearance from the supplied portrait without helping clothing legibility.',
    'slot:space_condition:hr_claustrophobic_body_clearance': 'Closely bounding walls and a low ceiling would replace the open landing and reduce space for the garment and hand relationships.',
    'slot:capture_mode:sf_076_base': 'A floor-supported camera would foreshorten the bib joins and clip contact; the independently authored seated-eye-level view better serves this scene.',
    'slot:gaze_target:ia_gaze_reference': 'Looking at a document target would replace the authored slight turn toward the returning boat, weakening the visible present circumstance.',
    'slot:action:mep_in_between_candidate': 'The existing fastening contact already supplies an incomplete current action; no additional displaced limb or material is needed.',
}
contextual = [
    {'candidate_id': 'augmentation:adult_appeal:sensual:location:karst_losing_stream_spring_location', 'reading': 'irrelevant', 'reason': 'The geological resurgence sense of spring introduces a karst valley system unrelated to the ferry landing and spring clothing.'},
    {'candidate_id': 'augmentation:adult_appeal:sensual:wardrobe_style:fit_ff03_v2_candidate', 'reading': 'potential', 'proposed_application': 'A roomy jacket could sit around the same blouse as another authorial outer layer within open appearance scope.', 'reason': 'A relaxed jacket could support the same subtle everyday warmth, but would cover the flower contact and apron shoulder joins. The blouse and apron alone serve the current moment more clearly.'},
    {'candidate_id': 'augmentation:adult_appeal:sensual:garment_detail:vel_held_towel_continuous_front', 'reading': 'irrelevant', 'reason': 'Two hands gripping a towel over swimwear would replace the clip action, bench support and the visible clothing construction being tested.'},
    {'candidate_id': 'augmentation:adult_appeal:sensual:location:water_w061', 'reading': 'irrelevant', 'reason': 'A spring pool and mist could create calm, but would replace the boat landing and obscure the concrete return-and-repair circumstance. Calm is already carried by the subject and light.'},
]
checks = {
    'body_ownership': {'status': 'supported', 'reason': 'One seated wearer owns the right reaching arm and clip digits, the left supporting palm and both shoe-bearing feet. The two garments and each shoe strap stay with that same wearer.', 'prompt_evidence': ['Her right arm reaches sideways to the notice frame at shoulder level', 'her left palm rests beside her hip on the seat', 'These two garments belong to the seated woman']},
    'joint_chain_and_reach': {'status': 'supported', 'reason': 'The close side frame and softly bent elbow allow a lateral shoulder-to-hand chain without pulling the shoulder away from the pelvis or requiring an extreme wrist route. The fingers press a small clip at shoulder height.', 'prompt_evidence': ['with the elbow softly bent', 'The frame stands close enough that her shoulder remains over her seated pelvis']},
    'support_and_balance': {'status': 'supported', 'reason': 'The pelvis sits on the bench and the left palm provides adjacent support while both feet contact the same planks. The right hand does not carry the wearer load; the modest foot offset permits a stable seated posture.', 'prompt_evidence': ['Her hips are supported by the bench', 'Both feet rest flat on the planks']},
    'contact_and_space': {'status': 'supported', 'reason': 'Thumb and forefinger press a clip around the co-located sheet and wire. The board stays beside the torso; dress straps join the bib outside the blouse; shoe instep straps connect to their own two sides, with ribbons on separate rear fittings.', 'prompt_evidence': ['the right thumb and forefinger pressing a wooden clip over the paper and wire', 'The board occupies a slim zone beside her reaching hand, leaving the center of the clothing visible', "The strap's inner end joins the inner side of that same flat, and its outer end closes onto the outer side of that same flat"]},
    'visibility_and_projection': {'status': 'supported', 'reason': 'The full seated oblique view exposes face, shoulder attachment, both bib joins, waist-to-hem continuity, right-hand contact and both foot uppers. The hem clears the ankles and the nearer foot turns outward; the frame and distant boat occupy separate depth zones.', 'prompt_evidence': ['looking obliquely across the bench so the face, shoulder flower, apron joins, wrap edge, lower pleats and both shoes have room to resolve', 'The hem ends above her ankles', 'Show both contacts on each shoe']},
}
visual_evidence = {
    'continuous_garment_phrase': 'The sage dress is one garment from neckline to hem',
    'dress_silhouette_phrase': 'an A-line dress silhouette opening below the fitted waist',
    'seam_or_closure_phrase': 'Its visible waist seam and closure connect the bib to the skirt',
    'drape_and_hem_phrase': 'The sage drape continues into the hem',
    'one_unit_legibility_phrase': 'the whole dress reads as one garment',
}
core = PACK['authorial_core']
composed = {
    'composer': 'agent', 'prompt_en': PROMPT, 'negative_en': PACK['negative_en'],
    'chosen_candidate_ids': chosen, 'chosen_visual_concept_ids': ['visual-concept:one_piece_dress_construction'],
    'candidate_interpretations': interpretations,
    'authorial_core_binding': {'source_authorial_core_sha256': core['canonical_sha256'], 'source_intent_lock_sha256': core['intent_lock']['canonical_sha256'], 'preserved_anchor_ids': ['core_concept','core_subject','core_event','reference_appearance'], 'preserved_evidence': [], 'authorial_decisions': [{'dimension': 'appearance', 'decision': 'Use a sage apron dress over the apricot blouse and add opposite-side instep straps to the ivory flats.', 'rationale': 'Two newly exposed optional bundles provide concrete joins and layer order compatible with the independently frozen spring scene. The sage dress also enables an explicit older construction obligation, while shoe ribbons remain a separate authorial detail.', 'affected_properties': [{'dimension':'appearance','target':'main_subject','property':p} for p in ['wardrobe.garment_type','wardrobe.layer.order','wardrobe.dress.overpanel_connection','wardrobe.shoe.strap_route','wardrobe.shoe.strap_attachment']]}]},
    'semantic_clarification_decisions': clarifications,
    'creative_augmentation_brief': {'decisions': [{'candidate_id': c['id'], 'decision': 'rejected', 'rationale': augmentation_reasons[c['id']]} for c in PACK['creative_augmentation']['candidates']]},
    'semantic_assertion_evidence': {'source_contract_sha256':PACK['semantic_assertion_obligations']['canonical_sha256'], 'evidence': {'subject_category': {'subject_phrase':'a person guided by the supplied reference'}}},
    'adult_appeal_brief': {'agency_phrase': 'she sits on a low timber bench and clips the loosened upper corner of a rain-warped route sheet back onto the wire of a narrow notice frame beside her', 'axes': {'sensual': {'intensity':1,'realization':'baseline','affected_dimensions':[],'affected_properties':[],'artistic_interpretation':'Subtle warmth in a concentrated everyday portrayal supports the present repair moment without competing with the visible clothing construction.','prompt_evidence':'a small easing of her lips giving the otherwise concentrated face an approachable warmth'},'fetish':{'intensity':0,'realization':'baseline','affected_dimensions':[],'affected_properties':[]}}, 'blend': {'emphasis':'sensual_led'}, 'contextual_review': contextual, 'contextual_comparison': 'At sensual 1 and fetish 0, the baseline quiet warmth, soft daylight and self-directed fastening already support an approachable ordinary portrayal. A roomy jacket could add ease but would hide the selected garment joins; a towel would replace both hand roles; karst and spring-pool settings would replace the ferry circumstance. Retain the baseline appeal realization and adopt the two clothing bundles solely for construction visibility.'},
    'visual_obligation_evidence': {'one_piece_dress_construction':visual_evidence},
    'embodiment_review': {'source_contract_sha256': PACK['embodiment_preflight']['canonical_sha256'], 'review':{'contract_version':'photo-embodiment-review/v1','provenance':'agent_postcomposition','prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest(),'scope':'body_action','summary':'The current apron-and-strap composition retains one seated body, ordinary lateral clip reach, bench and floor support, and visible contact surfaces while adding own-garment joins and same-shoe strap endpoints. This is a fresh preflight of the final prompt, not a kinematic proof or pixel score.','checks':checks}},
}

def write(name, value):
    (ARM/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

write('composed.input.json',composed)
(ARM/'prompt.en.txt').write_text(PROMPT+'\n')
write('native-transport.input.json', {'references': [{'path':'/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg','sha256':'06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7','role':'face_hair_reference'}], 'referenced_image_paths':['/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg'], 'transparent_background':False})
write('native-authorization.json', {'lanes':['native'],'invocation_limit':1,'authorization_source': 'Request envelope c66753a536517e5d8dcfb4d32141e8380cdfa671075f7345f923cdd23d19fa8e: the requesting user explicitly asks the three independent agents to use the attached image, write prompts, generate images, and test their reflected spring-fashion topics.'})

# Frozen BEFORE the native invocation. These rows remain supplemental and never
# become runtime hard_gates or unexposed spring-profile activation.
selected = json.loads((ARM/'selected-detail-view.json').read_text())['candidates']
observations=[]
for item in selected:
    if item['id'] not in chosen: continue
    c=item['candidate']
    own = 'seated main subject; sage outer dress; separate apricot inner blouse' if 'sf071' in c['id'] else 'seated main subject; each ivory flat and that flat own foot; same-shoe strap'
    view = 'Oblique torso view simultaneously exposing both sage bib-to-strap joins and sage edges in front of the separately bounded apricot blouse.' if 'sf071' in c['id'] else 'Both shoe uppers exposed; native view permits tracing each solid instep strap to both opposite sides of its own shoe. Score the far shoe separately; no near-shoe substitution.'
    for component in c['components']:
        observations.append({'observation_id':c['id']+':'+component['id'],'candidate_id':c['id'],'kind':'component','source_component_id':component['id'],'source_concept_units':component['concept_units'],'owner':own,'required_view':view,'review_scale':'native','all_of_criterion':'Every source concept unit must be visibly embodied by the declared same owner. Both shoes must satisfy the shoe component; one visible end is insufficient.','false_substitutes':c['confusion_boundaries'],'status':'not_run'})
    for relation in c['relations']:
        observations.append({'observation_id':c['id']+':'+relation['id'],'candidate_id':c['id'],'kind':'directed_relation','source_relation_id':relation['id'],'type':relation['type'],'subject':relation['subject'],'object':relation['object'],'owner':own,'required_view':view,'review_scale':'native','all_of_criterion':'Both endpoints and their directed relation must be observable in the same image, with correct ownership. For shoe relations, each foot/shoe is scored separately and both must pass.','false_substitutes':c['confusion_boundaries'],'status':'not_run'})
write('new-topic-observation-plan.json', {'schema_version':'spring-topic-supplemental-plan/v1','frozen_before_image_invocation':True,'runtime_generation':'a7fd58162695c7c23a9257ac89b13434e94e6899fc3891858b837636ad1ced6c','pack_id':PACK['pack_id'],'pack_sha256':hashlib.sha256((ARM/'run/revisions/0706f0abc2614555aff88abff03eb942/pack.json').read_bytes()).hexdigest(),'selected_candidate_ids':chosen,'unexposed_profile_ids':['spring_sf071_1','spring_sf107_02'],'profile_hard_activation':'not_verified_not_promoted','classification':'supplemental_topic_review_separate_from_runtime_hard_gates','pass_policy':'all_of; partial or unobservable is fail; both shoes independently must pass','claim_limits':['Visible structure only. No fiber content, manufacturing process, biomechanical force, identity or historical event proof.','The optional candidate selection does not hard-activate its associated profile.'], 'observations':observations})
print(json.dumps({'composed_path':str(ARM/'composed.input.json'),'prompt_sha256':hashlib.sha256(PROMPT.encode()).hexdigest(),'selected_new_bundle_count':len(chosen),'supplemental_observation_count':len(observations)},ensure_ascii=False))
