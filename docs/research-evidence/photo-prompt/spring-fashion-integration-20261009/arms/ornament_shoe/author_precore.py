from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
S=Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt/skills/photo-prompt-image-generator')
def save(n,v): (B/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
env=json.loads((B/'request_envelope.json').read_text())
controls=json.loads((B/'run/revisions/42f7a47a09d24d8f96d777986dc56dbb/creative_controls.json').read_text())
prompt='''A spring fashion photograph of a person guided by the supplied reference, with visible facial features and short black hair guided by the supplied portrait. Spring clothing structures are visibly worn within a particular moment of ordinary work. At a small ferry landing just after morning rain, she sits on a low timber bench and clips the loosened upper corner of a rain-warped route sheet back onto the wire of a narrow notice frame beside her. The other upper corner is already fastened; a damp crease runs diagonally across the paper, and a small ferry is entering the gap between the landing posts. Her fingertips finish the fastening as her chin turns slightly toward the returning boat, a small easing of her lips giving the otherwise concentrated face an approachable warmth.

Her pale apricot blouse has a soft diagonal drape descending from the left shoulder toward the opposite waist. A fabric flower is fixed at the left shoulder: separate curled petal edges gather around a compact center, and the flower's base sits flush against the blouse at that single attachment point. The folds radiate from beneath that base instead of floating beside it. Her sage skirt has an upper wrap panel crossing the waist, its diagonal free edge visibly lying over the under-panel; below that edge, a broad lower section falls in repeated narrow vertical pleats. The pleats open slightly over the nearer bent knee and continue into long folds below it. These are distinct constructions with readable edges, attachment and overlap rather than a mass of rippling fabric.

Her hips are supported by the bench, her torso faces the camera in a relaxed three-quarter orientation, and her left palm rests beside her hip on the seat. Her right arm reaches sideways to the notice frame at shoulder level, with the elbow softly bent and the right thumb and forefinger pressing a wooden clip over the paper and wire. The frame stands close enough that her shoulder remains over her seated pelvis. Both feet rest flat on the planks, the nearer foot half a shoe-length ahead and angled outward. The skirt ends above her ankles. Each ivory ballet flat has a rounded shallow toe and thin ribbons threaded from the shoe's side attachments across the instep in clear X crossings, then continuing around the ankle into a small tied bow; the ribbon paths remain visible against the skin and separate from the skirt hem.

Use a vertical head-to-toe view from just below her seated eye level, looking obliquely across the bench so the face, shoulder flower, wrap edge, lower pleats and both shoes all have room to resolve. The board occupies a slim zone beside her reaching hand, leaving the center of the clothing visible. Darkened wet planks and a pale reflection under the bench carry the recent rain; the small boat and bright channel sit farther behind her. Soft directional daylight gives the flower a shallow contact shadow, catches the outer edges of the skirt pleats and keeps the ribbon crossings distinct. Let her quiet concentration lead, the repaired corner connect the scene to a returning journey, and the repeated folding rhythms of paper and clothing support that moment. The photograph feels naturally inhabited, with crisp tactile detail on the subject and a gently quieter background.'''
prompt=' '.join(prompt.split())
(B/'baseline_draft.txt').write_text(prompt+'\n')
core={
'contract_version':'photo-authorial-core/v3','provenance':'agent_prepack','source_request':env['request_text'],
'creative_controls_sha256':controls['canonical_sha256'],
'interpreted_intent':'The requester asks for a distinct randomly chosen complex test concept that can show newly integrated spring fashion meaning in an image using the attached portrait. The title of the conversation supplies spring fashion as the topic. The ferry-landing scene, notice sheet, fastening gesture, clothing colors and precise constructions are independent authorial choices, not user locks. An ordinary repair at the moment a boat returns gives the structure-rich photograph a present purpose. The resolved saved controls are sensual 1, fetish 0, creativity 1, surreal 0, emphasis sensual-led; subtle human warmth supports the scene, while practical geometry and restrained visual echoes provide complexity without an added surreal treatment.',
'subject':'A reference-guided person wearing visible spring clothing structures; only visible facial appearance and short black hair use the photograph.',
'setting':'Agent-chosen small ferry landing after morning rain, with low timber bench, narrow notice frame and distant returning ferry.',
'event':'Spring clothing structures are visibly worn; the sheet-corner fastening is agent-authored current action.',
'visual_priorities':[
'The concentrated reference-guided face and fingertips at the nearly repaired paper corner establish the current moment.',
'The flower base contacts the shoulder, with visible petal curl and blouse folds descending from that attachment.',
'The upper wrap edge lies over its under-panel, while the lower pleated section continues past the bent knee.',
'The two supported feet display continuous ribbons from shoe attachments through instep crossings to ankle bows.',
'The already-fastened corner, damp crease and small returning boat connect the repair to the landing reopening.'
],
'baseline_prompt_en':prompt,'user_definitions':[],
'interpretation_provenance':[
{'term':'random complex concept for testing the integrated topic','source_text':env['active_spans'][0]['text'],'basis':'request_context','resolution':'One distinct randomly chosen spring-fashion test photograph; the requester authorizes agent-authored concept choice and actual image testing. Specific scene, garments, hand mechanics and props remain open authorial staging.','sources':[]},
{'term':'use the supplied photograph','source_text':env['active_spans'][1]['text'],'basis':'request_context','resolution':'Use the portrait as visual facial-appearance and short-black-hair guidance; it provides no biography, personality, body measurements or garment obligation.','sources':[]}
],
'unresolved_ambiguities':[],'user_exclusions':[],'runtime_forbidden_labels':[],
'intent_lock':{'contract_version':'photo-intent-lock/v2','priority':'requesting_user',
'semantic_anchors':[
{'anchor_id':'core_concept','source_text':'이번에 반영한 주제가 이미지에 실제로 반영되는지까지 테스트할 수 있는 랜덤한 복잡한 컨셉','dimension':'concept','prompt_evidence':'A spring fashion photograph'},
{'anchor_id':'core_subject','source_text':'첨부한 이미지를 활용하여','dimension':'subject','prompt_evidence':'a person guided by the supplied reference'},
{'anchor_id':'core_event','source_text':'이번에 반영한 주제가 이미지에 실제로 반영되는지까지 테스트할 수 있는','dimension':'event','prompt_evidence':'Spring clothing structures are visibly worn'},
{'anchor_id':'reference_appearance','source_text':'첨부한 이미지를 활용하여','dimension':'reference_use','prompt_evidence':'visible facial features and short black hair guided by the supplied portrait'}
],
'locked_dimensions':['concept','subject','event','reference_use'],
'open_dimensions':['appearance','count','age','pose','body_geometry','expression','action','setting','relationship','style','viewer_outcome','framing','composition','lighting','camera','color','material','timing','atmosphere']},
'semantic_assertions':[
{'assertion_id':'subject_category','dimension':'subject','polarity':'required','source_span_ids':['reference_use'],'affected_dimensions':['subject'],'axes':{'subject_category':'human'},'evidence':{'subject_phrase':'a person guided by the supplied reference'}},
{'assertion_id':'camera_axis_review','dimension':'camera','polarity':'advisory','source_span_ids':['concept_scope'],'affected_dimensions':['camera'],'axes':{'camera_axis_review':'camera_axis_review_v1','capture_owner':'unprescribed','direction_requirement':'open','height_requirement':'open'},'evidence':{}}
],
'request_lineage':None,
'style':{'domain':'editorial portrait','family':'situated spring fashion documentary','evidence':['naturally inhabited current action','crisp tactile detail on the subject and a gently quieter background']},
'variation_key':'ornament_shoe_seed_7825148642666662853'}
save('authorial_core.input.json',core)
ph=hashlib.sha256(prompt.encode()).hexdigest()
selection={
'contract_version':'photo-precore-feature-selection/v1','request_id':env['request_id'],'active_span_ids':[s['span_id'] for s in env['active_spans']],
'catalog_path':'skills/photo-prompt-image-generator/precore/visual_feature_catalog.json','catalog_schema_version':'photo-precore-feature-catalog/v1',
'catalog_sha256':hashlib.sha256((S/'precore/visual_feature_catalog.json').read_bytes()).hexdigest(),'request_sha256':env['request_sha256'],'baseline_prompt_sha256':ph,
'selected':[
{'category_id':'feature.situation','basis':'request_derived','source_span_ids':['concept_scope'],'source_text':None,'derivation':'The requested image test needs an observable present state of the integrated spring-fashion topic; the specific dock repair is optional staging.','reason':'Place the garment structures on a visible wearer within the test photograph.','baseline_evidence':'Spring clothing structures are visibly worn'},
{'category_id':'feature.subject','basis':'request_derived','source_span_ids':['reference_use'],'source_text':None,'derivation':'The supplied close portrait is used for the visible face and short black hair, with no personal-history inference.','reason':'Make the provided visual reference relevant at the visible subject face.','baseline_evidence':'visible facial features and short black hair guided by the supplied portrait'},
{'category_id':'feature.narrative_context','basis':'agent_visual_choice','source_span_ids':[],'source_text':None,'derivation':None,'reason':'An already-fastened corner and a returning ferry make the repair part of the landing being ready again.','baseline_evidence':'The other upper corner is already fastened; a damp crease runs diagonally across the paper, and a small ferry is entering the gap between the landing posts'},
{'category_id':'feature.location','basis':'agent_visual_choice','source_span_ids':[],'source_text':None,'derivation':None,'reason':'The narrow dock notice frame gives the reaching hand a reachable target and a useful repair.','baseline_evidence':'At a small ferry landing just after morning rain'},
{'category_id':'feature.clothing','basis':'agent_visual_choice','source_span_ids':[],'source_text':None,'derivation':None,'reason':'Choose mutually visible shoulder attachment, skirt overlap and pleats, and connected shoe ribbons as varied spring-fashion geometry.','baseline_evidence':'Her sage skirt has an upper wrap panel crossing the waist, its diagonal free edge visibly lying over the under-panel'},
{'category_id':'feature.hand_gesture','basis':'agent_visual_choice','source_span_ids':[],'source_text':None,'derivation':None,'reason':'The clip, paper and wire give thumb and forefinger a single concrete contact.','baseline_evidence':'the right thumb and forefinger pressing a wooden clip over the paper and wire'},
{'category_id':'feature.pose','basis':'agent_visual_choice','source_span_ids':[],'source_text':None,'derivation':None,'reason':'Seated support and two feet on the planks let the skirt and shoes remain legible during the repair.','baseline_evidence':'Both feet rest flat on the planks, the nearer foot half a shoe-length ahead and angled outward'},
{'category_id':'feature.shot_size','basis':'agent_visual_choice','source_span_ids':[],'source_text':None,'derivation':None,'reason':'A head-to-toe image preserves the reference face while allowing the shoe ribbon paths to be assessed.','baseline_evidence':'Use a vertical head-to-toe view from just below her seated eye level'},
{'category_id':'feature.light_quality','basis':'agent_visual_choice','source_span_ids':[],'source_text':None,'derivation':None,'reason':'Gentle directional light differentiates attached flower base, pleat edges and ribbon crossings.','baseline_evidence':'Soft directional daylight gives the flower a shallow contact shadow, catches the outer edges of the skirt pleats and keeps the ribbon crossings distinct'}
]}
save('precore_feature_selection.input.json',selection)
review={
'contract_version':'photo-embodiment-review/v1','provenance':'agent_prepack','prompt_sha256':ph,'scope':'body_action',
'summary':'Ordinary human seated model. Pelvis and left palm receive bench support; both feet carry a small stabilizing load on the planks. The right shoulder and elbow reach laterally to a close notice frame, and thumb plus forefinger press a wooden clip around the co-located upper paper corner and horizontal wire. The view exposes shoulder, garment panel edges, shoes and hand contact together; the sheet is beside the torso rather than across the lap.',
'checks':{
'body_ownership':{'status':'supported','reason':'The reaching right arm and gripping digits are explicitly owned by the seated wearer; her left palm is a separate support, and both feet belong to the same wearer.','prompt_evidence':['Her right arm reaches sideways to the notice frame at shoulder level','her left palm rests beside her hip on the seat']},
'joint_chain_and_reach':{'status':'supported','reason':'Lateral shoulder reach with softly flexed elbow keeps the hand near shoulder level; the close frame does not demand impossible extension or a torso twist while the seated pelvis remains below the shoulder.','prompt_evidence':['with the elbow softly bent','The frame stands close enough that her shoulder remains over her seated pelvis']},
'support_and_balance':{'status':'supported','reason':'The bench supports hips; left palm is adjacent support; both flat feet and mild forward offset widen the contact footprint. The fingers do not support body weight.','prompt_evidence':['Her hips are supported by the bench','Both feet rest flat on the planks']},
'contact_and_space':{'status':'supported','reason':'The wooden clip encloses the paper corner and wire, with thumb and forefinger pressing its outer surfaces. Side-mounted board leaves clearance at torso and skirt; ribbon loops remain separate from skirt hem.','prompt_evidence':['the right thumb and forefinger pressing a wooden clip over the paper and wire','The board occupies a slim zone beside her reaching hand, leaving the center of the clothing visible']},
'visibility_and_projection':{'status':'supported','reason':'Oblique head-to-toe camera view sees the reaching-side hand, reference-guided face, left shoulder flower contact, front panel overlap, lower skirt folds and both foot uppers. The nearer foot is turned enough to reveal instep ribbons while remaining flat; the small ferry stays in background.','prompt_evidence':['looking obliquely across the bench so the face, shoulder flower, wrap edge, lower pleats and both shoes all have room to resolve','The skirt ends above her ankles']}
}}
save('embodiment_review.input.json',review)
save('concept_note.json',{
'concept_name_ko':'비 뒤 첫 배를 기다리는 접힌 항로','concept_name_en':'Folded Routes Before the First Returning Ferry',
'random_draw':json.loads((B/'random_draw.json').read_text()),
'precore_direction_comparison':'All four authored possibilities were considered at the resolved saved strengths before local data access. A ferry reopening makes a small fastening act consequential and gives folds in the paper and clothing a restrained visual echo. A rehearsal would shift attention toward a performing role, orchard packing would require more cargo, and a roof pennant would give wind a stronger clothing effect. The seeded choice selected the ferry landing; its scene can display the allocated structural themes without changing requester meaning.',
'why_now':'A rain-loosened chart corner is being reattached as a boat returns. The first corner and damp crease are visible preceding traces, fingertip contact is the current act, and the returning boat is the emerging next use.',
'controls_used':{k:v['value'] for k,v in controls['controls'].items()},'resolved_emphasis':controls['resolved_emphasis'],
'ownership':'All detailed garment variants, setting, moment, props, color, pose, framing and lighting are agent choices; core mandatory evidence retains only the actual topic-image test and reference use.',
'feature_selection_count':len(selection['selected']),'baseline_words':len(prompt.split()),'baseline_sha256':ph
})
print(json.dumps({'prompt_sha256':ph,'words':len(prompt.split()),'selection_count':len(selection['selected'])}))
