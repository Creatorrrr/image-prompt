from pathlib import Path
import json, hashlib
BASE=Path('/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/bodice_hem')
WORK=Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')

def save(name,x):
    (BASE/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
e=json.loads((BASE/'request_envelope.json').read_text())
s=json.loads((BASE/'run/workflow.json').read_text())
controls=json.loads(Path(s['artifacts']['creative_controls']['path']).read_text())
catalog_path=WORK/'skills/photo-prompt-image-generator/precore/visual_feature_catalog.json'
catalog_raw=catalog_path.read_bytes()
# Author-selected observation categories were chosen for the drawn scene before writing its draft.
category_plan=['feature.situation','feature.narrative_clues','feature.subject','feature.clothing','feature.action','feature.location','feature.gaze','feature.light_quality','feature.framing']
save('feature-plan.json',{'categories':category_plan,'provenance':'agent_prepack','concept_note':'concept-note.json','purpose':'Observe one coherent rooftop moment, reference appearance and visible spring garment connections.'})
draft='''In this complex spring-fashion photograph, a woman guided by the supplied photograph has spring garments worn visibly together while securing a loose blue sheet on a rooftop worktable. Her visible face and short black bob follow the supplied photograph. The scene takes place beside a modest rooftop drying line on a clear spring afternoon: botanical cyanotype sheets hang at staggered heights above a mesh-topped table, and the sheet nearest her has slipped from its clip. Its lifted corner is already flattened beneath her right palm, while a crease still holds a little tent of blue paper beyond her fingertips. The next empty clip hangs immediately above that sheet, making the small unfinished task readable.

She stands beside the table with both feet planted on the dry stone deck, her hips facing the camera and her right shoulder turned only slightly toward the tabletop. Her right forearm extends sideways to the mesh surface rather than across the garment front; her left hand holds the fallen wooden clip beside her left hip. She turns her face toward the camera with a quiet, almost amused awareness after arresting the paper, lips relaxed and a warm direct gaze. That brief personal connection adds a subtle attraction to an otherwise practical moment.

Her pale pistachio top has a straight square neckline, two narrow shoulder straps attached at the neckline corners, and a fitted bodice covered in close parallel horizontal gathers. A distinct horizontal waist seam connects the gathered bodice to a short flared peplum; the peplum's cream lace edge forms a row of rounded scallops, each ending in its own outward curve. The waist seam and the outward flare remain clear across the front, while the narrow straps rise individually over the shoulders. Below it she wears a soft cream A-line midi skirt with an asymmetric lower edge: the front finishes near her upper calf and the back drops lower toward her ankle. The flared peplum belongs to the top and lies outside the skirt, with a visible break between its scalloped edge and the smooth skirt surface. Low rust-colored shoes rest on the stone, and a breeze gives the skirt's rear panel a small lifted fold while the waist stays settled.

The table occupies the side of the frame, leaving her neckline, bodice, waist connection, peplum and skirt edge readable as a continuous outfit. A few pale botanical silhouettes on the drying sheets echo the spring setting. A tray with two clips and the crisp moving sheet supply the nearby evidence of work, with rooftop railings and a distant brick wall behind. Photograph her from a comfortable three-quarter frontal position, with the full skirt edge and grounded shoes inside a vertical frame. Soft afternoon light makes the gathered cloth cast small repeated shadows; the face, hand-paper contact and garment front hold the clearest focus, while the hanging prints form quieter blue planes behind her. The image feels like an observed interruption in a real task, with convincing paper thickness, separate garment edges, natural facial texture and ordinary rooftop depth.'''
prompt=' '.join(draft.split())
(BASE/'baseline-draft.txt').write_text(draft+'\n')
(BASE/'baseline-canonical.txt').write_text(prompt+'\n')
ph=hashlib.sha256(prompt.encode()).hexdigest()
core={
 'contract_version':'photo-authorial-core/v3','provenance':'agent_prepack',
 'source_request':e['request_text'],'creative_controls_sha256':controls['canonical_sha256'],
 'interpreted_intent':'Requester asks for a random complex concept testing newly integrated spring-fashion visual semantics and candidates, using the supplied photograph. The independently drawn scene is a rooftop cyanotype drying interruption: the visible slipped sheet, stabilizing palm and empty clip connect preceding loss, present correction and an unfinished next step. All paper props, rooftop setting, gesture and garment geometry are agent-owned staging. Visible face and short dark bob use the reference; no real biography, personality or body measurement is inferred. The viewer first meets a quietly appealing person, then reads the spring outfit and the small practical task. Resolved sensual=1 supports warm direct awareness; fetish=0 and surreal=0 add no treatment; creativity=1 keeps the ordinary setting coherent despite the requester\u2019s complex test scope.',
 'subject':'A woman whose visible face and short black bob use the supplied photograph as reference.',
 'setting':'A real rooftop drying line and mesh worktable on a clear spring afternoon.',
 'event':'Spring garments are visibly worn together during a current rooftop moment; the specific sheet-rescue action is independent authorial staging.',
 'visual_priorities':['The face and short dark bob carry the supplied reference in a warm moment of camera awareness.','The loose cyanotype corner, flattening palm and empty clip connect the cause, immediate result and unfinished task.','The top\u2019s narrow straps, straight neckline, gathered bodice and waist-to-peplum join read as one garment.','The peplum scallops and the separate asymmetric skirt edge remain distinct across the visible outfit.'],
 'baseline_prompt_en':prompt,
 'user_definitions':[],
 'interpretation_provenance':[
  {'term':'random complex test concept for the newly integrated topic','source_text':e['active_spans'][0]['text'],'basis':'request_context','resolution':'The current conversation topic is 봄 패션 용어 조사. The user requests an independently chosen complex concept that tests that topic in the image; no particular garment geometry, prop or setting is prescribed.','sources':[]},
  {'term':'supplied-image use','source_text':e['active_spans'][1]['text'],'basis':'request_context','resolution':'Use the supplied photograph for visible face and short dark hair cues. It supplies no actual biography or inner-life evidence and does not prescribe the clothing or scene.','sources':[]}
 ],
 'unresolved_ambiguities':[], 'user_exclusions':[], 'runtime_forbidden_labels':[],
 'intent_lock':{
  'contract_version':'photo-intent-lock/v2','priority':'requesting_user',
  'semantic_anchors':[
   {'anchor_id':'core_concept','source_text':e['active_spans'][0]['text'],'dimension':'concept','prompt_evidence':'complex spring-fashion photograph'},
   {'anchor_id':'core_subject','source_text':e['active_spans'][1]['text'],'dimension':'subject','prompt_evidence':'a woman guided by the supplied photograph'},
   {'anchor_id':'core_event','source_text':e['active_spans'][0]['text'],'dimension':'event','prompt_evidence':'spring garments worn visibly together'},
   {'anchor_id':'reference_use','source_text':e['active_spans'][1]['text'],'dimension':'reference_use','prompt_evidence':'Her visible face and short black bob follow the supplied photograph'}
  ],
  'locked_dimensions':['concept','subject','event','reference_use'],
  'open_dimensions':['appearance','pose','body_geometry','expression','action','setting','relationship','style','framing','composition','lighting','camera','color','material','timing','atmosphere','viewer_outcome']
 },
 'semantic_assertions':[
  {'assertion_id':'camera_axes','dimension':'camera','polarity':'advisory','source_span_ids':['concept_scope'],'affected_dimensions':['camera'],'axes':{'camera_axis_review':'camera_axis_review_v1','capture_owner':'unprescribed','direction_requirement':'open','height_requirement':'open'},'evidence':{}}
 ],
 'request_lineage':None,
 'style':{'domain':'fashion photography','family':'inhabited spring rooftop editorial','evidence':['The task leaves its cause and present correction visible beside a legible outfit.','Soft ordinary daylight preserves individual garment boundaries and warm reference-guided presence.']},
 'variation_key':'bodice_hem_seed_9878669292090812608'
}
save('authorial-core-input.json',core)
def row(cat,reason,evidence,basis='agent_visual_choice',spans=None,derivation=None):
 return {'category_id':cat,'basis':basis,'source_span_ids':spans or [],'source_text':None,'derivation':derivation,'reason':reason,'baseline_evidence':evidence}
selection={'contract_version':'photo-precore-feature-selection/v1','request_id':e['request_id'],'active_span_ids':[s['span_id'] for s in e['active_spans']],'catalog_path':'skills/photo-prompt-image-generator/precore/visual_feature_catalog.json','catalog_schema_version':'photo-precore-feature-catalog/v1','catalog_sha256':hashlib.sha256(catalog_raw).hexdigest(),'request_sha256':e['request_sha256'],'baseline_prompt_sha256':ph,'selected':[
 row('feature.situation','A interrupted drying task gives the photograph a visible present purpose.','while securing a loose blue sheet on a rooftop worktable'),
 row('feature.narrative_clues','The slipped clip and remaining fold preserve evidence of what has just changed.','the sheet nearest her has slipped from its clip'),
 row('feature.subject','The supplied image governs visible face and hair cues rather than an inferred life story.','Her visible face and short black bob follow the supplied photograph','request_derived',['reference_use'],'Use the supplied image\u2019s directly visible face and short dark hair for the primary person.'),
 row('feature.clothing','Visible top construction and separate lower edges let the garment topic be assessed within a coherent outfit.','A distinct horizontal waist seam connects the gathered bodice to a short flared peplum'),
 row('feature.action','The stabilizing hand and paper state make the current correction understandable.','Its lifted corner is already flattened beneath her right palm'),
 row('feature.location','The outdoor work surface and drying line provide physically useful surroundings.','beside a modest rooftop drying line on a clear spring afternoon'),
 row('feature.gaze','Warm camera awareness supports the resolved subtle attraction through personal presence.','lips relaxed and a warm direct gaze'),
 row('feature.light_quality','Repeated shadows make gathers assessable without turning the scene into a measurement plate.','Soft afternoon light makes the gathered cloth cast small repeated shadows'),
 row('feature.framing','The crop includes the full lower edge and supporting feet needed to read the joined outfit.','with the full skirt edge and grounded shoes inside a vertical frame')
]}
save('precore-feature-selection-input.json',selection)
review={'contract_version':'photo-embodiment-review/v1','provenance':'agent_prepack','prompt_sha256':ph,'scope':'body_action','summary':'Ordinary human body model. The upright person stabilizes a nearby loose sheet laterally on a waist-height worktable. Her hips remain front-facing while a small shoulder turn and sideways forearm reach preserve contact, balance and garment visibility. The separate left hand holds one light clip beside the left hip.','checks':{
 'body_ownership':{'status':'supported','reason':'Right palm and right forearm belong to the primary woman; the left hand owns the clip. The paper corner is acted on by that right palm.','prompt_evidence':['Its lifted corner is already flattened beneath her right palm','her left hand holds the fallen wooden clip beside her left hip']},
 'joint_chain_and_reach':{'status':'supported','reason':'A small right shoulder turn and sideways arm reach give a short shoulder-elbow-wrist path to the table beside her; the prompt does not force a reach across the torso. The elbow can remain gently bent.','prompt_evidence':['her right shoulder turned only slightly toward the tabletop','Her right forearm extends sideways to the mesh surface rather than across the garment front']},
 'support_and_balance':{'status':'supported','reason':'Both feet stay planted on a dry horizontal deck with torso over the pelvis; the reachable side table lets the woman press a light sheet without committing body weight to an unsupported corner.','prompt_evidence':['She stands beside the table with both feet planted on the dry stone deck','her hips facing the camera']},
 'contact_and_space':{'status':'supported','reason':'Palm contact is on the sheet corner resting on the mesh tabletop. The lifted crease lies beyond fingertips, not between palm and support. The table to the side leaves room for her forearm and the clip hand.','prompt_evidence':['Its lifted corner is already flattened beneath her right palm','a crease still holds a little tent of blue paper beyond her fingertips','The table occupies the side of the frame']},
 'visibility_and_projection':{'status':'supported','reason':'A three-quarter frontal view can see the hand-paper contact on the side table while preserving the front neckline, top waist join and the full skirt edge. Arm direction and separate clip hand do not occlude the decisive front cloth geometry.','prompt_evidence':['Photograph her from a comfortable three-quarter frontal position','leaving her neckline, bodice, waist connection, peplum and skirt edge readable as a continuous outfit','with the full skirt edge and grounded shoes inside a vertical frame']}
}}
save('embodiment-review-input.json',review)
(BASE/'visual_feature_catalog.snapshot.json').write_bytes(catalog_raw)
print(json.dumps({'baseline_sha256':ph,'word_count':len(prompt.split()),'feature_count':len(selection['selected']),'controls_sha256':controls['canonical_sha256']}))
