import json, hashlib, sys
from pathlib import Path
P=Path(__file__).parent
S=Path('skills/photo-prompt-image-generator/precore')
sys.path.insert(0,str(S.resolve()))
import photo_authoring_wire as wire
import photo_semantic_witnesses as witnesses

def save(name,obj):
    (P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

env0=json.loads((P/'revisions/ea54f712a86043f1b79d58748909aaf6/request_envelope_input.json').read_text())
assert hashlib.sha256((P/'revisions/ea54f712a86043f1b79d58748909aaf6/request_envelope_input.json').read_bytes()).hexdigest()=='6a640590860a9b922fcda1e8f20b950a833b05a5043f20ab126adff8a4ce3bc7'
env=wire.normalize_request_envelope(env0)
controls=json.loads((P/'revisions/300e752752d6427db239994d6fd1bf42/creative_controls.json').read_text())
baseline="""A photographic space-horror scene records a dangerous moment aboard a spacecraft. At the right side of a wide rectangular hatch, a woman whose facial appearance and hairstyle follow the supplied portrait crouches beside the final clamp of a temporary clear pressure partition. Her dark chin-length bob and wispy fringe frame large brown eyes, softly rounded cheeks and natural pink lips. Her concentrated face carries an intimate, vulnerable presence within the emergency; a small sheen of perspiration catches the work light. She wears a fitted off-white thermal coverall with worn utility seams. The corridor around her still holds breathable air. Beyond the transparent partition, two frost-coated cryogenic storage capsules flank a torn opening in the ship's outer wall, exposing small sharp stars in black space. The partition is the thin physical boundary preserving the corridor. Its upper and side edges are already captured by evenly spaced metal clamps; its clear sheet bows away from her into the depressurized bay. At the lower-right corner, a short unfinished seam remains visibly open just to the left of a red over-center lever. Fine white condensation threads stream through that gap away from the corridor toward the open bay. She has one knee on the corridor floor and the opposite boot planted firmly beside her. Her right hand closes around the red lever, folding it toward the lower-right jamb; her left palm braces the same solid jamb above the clamp. Her arms remain on the corridor side of the sheet. She watches the remaining gap as she works, lips slightly parted, with the incompletely closed lever and the escaping threads visible together. Photograph from the corridor at a shallow oblique angle, wide enough to include all four partition edges, her face, both connected arms, the grounded knee and boot, and the torn hull beyond. Keep the clamp large and unobstructed beside her hand. A warm portable work lamp describes her face and fingers against cold blue reflections on the transparent sheet; a dim red service beacon recedes into the bay. The vulnerable clear surface, purposeful hand, and indifferent patch of outer space form the photograph's visual hierarchy, with tactile condensation and restrained documentary grain."""
baseline=wire.clean_spaces(baseline)
(P/'baseline.draft.txt').write_text(baseline+'\n')
appearance_phrase="a woman whose facial appearance and hairstyle follow the supplied portrait"

# Only source-grounded reference scope is frozen as a fact. All emergency mechanics stay authorial.
assertions=[
 {'assertion_id':'woman_owner','dimension':'subject','polarity':'required','source_span_ids':['visual_request'],'affected_dimensions':['subject'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':'owner','owner':'woman','owner_kind':'human'},'evidence':{'owner_phrase':appearance_phrase}},
 {'assertion_id':'woman_main_role','dimension':'subject','polarity':'required','source_span_ids':['visual_request'],'affected_dimensions':['subject'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':'role','role':'main_subject','owner':'woman'},'evidence':{'role_phrase':appearance_phrase}},
 {'assertion_id':'reference_face_hair','dimension':'appearance','polarity':'required','source_span_ids':['visual_request'],'affected_dimensions':['appearance'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':'fact','owner':'woman','property':'reference.face_hair','value_type':'reference.face_hair/v1','value':'supplied_portrait_face_and_hair','scope_kinds':['reference_appearance'],'source_input_ids':['portrait']},'evidence':{'appearance_phrase':appearance_phrase}},
 {'assertion_id':'camera_axes_open','dimension':'camera','polarity':'advisory','source_span_ids':['visual_request'],'affected_dimensions':['camera'],'axes':{'camera_axis_review':'camera_axis_review_v1','capture_owner':'unprescribed','direction_requirement':'open','height_requirement':'open'},'evidence':{}}
]
for scope,state,items in [
 ('reference_appearance','known_present',[{'assertion_id':'reference_face_hair','dimension':'appearance','target':'woman','property':'reference.face_hair','value':{'type':'reference.face_hair/v1','value':'supplied_portrait_face_and_hair'}}]),
 ('requester_identity','known_absent',[])
]:
    inventory={'schema':'photo-frozen-scope-inventory/v1','complete':True,'input_binding':witnesses.input_binding(env),'reviewed_input_ids':[i['id'] for i in env0['input_inventory']['items']],'state':state,'items':items}
    assertions.append({'assertion_id':'scope_'+scope,'dimension':'subject','polarity':'required','source_span_ids':['visual_request'],'affected_dimensions':['subject'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':'scope_inventory','owner':'woman','scope_kind':scope,'inventory':witnesses.canonical(inventory)},'evidence':{'scope_phrase':appearance_phrase}})

core={
 'contract_version':'photo-authorial-core/v3','provenance':'agent_prepack','source_request':env0['request_text'],'creative_controls_sha256':controls['canonical_sha256'],
 'interpreted_intent':"Requester asks independent random topic-appropriate concepts, testcases and reference-guided images; the positive topic antecedent is space horror. The coordinator's spacecraft-survival/physical-boundaries domain is agent-owned exploration scope, not a requester scene prescription. An independent random draw selected a damaged cryogenic-bay pressure partition. The fictional operator is saving the still-pressurized corridor by closing the last corner of a clear sheet; the hull tear, bowed membrane, escaping condensation, concentrated hand and waiting face give the viewer a readable present cause, action and already-visible consequence. The selected scene wins over a small window patch because a single large boundary makes both sides and her relation to them legible; the docking-collar alternative would dilute her face with suit hardware. Saved creativity=1 supports local refinement; sensual=1 is a subtle quality of face, perspiration and intimate attention, fetish=0 adds no treatment, surreal=0 preserves physically grounded science fiction. Required concept/subject/event evidence retains only a photographic space-horror test, reference-guided human presence and a broad dangerous spacecraft moment. The cryogenic bay, role, membrane, tear, clamps, pose, action, geometry and lighting are all agent-owned staging and create no requester assertion or lock. Reference use covers facial appearance and hairstyle only; identity, biography, real age, clothing and actual personality are not inferred.",
 'subject':'A fictional woman using the supplied portrait for facial appearance and hairstyle; an operator role is agent-authored.',
 'setting':'Agent-authored pressurized spacecraft corridor beside a decompressed cryogenic storage bay with a torn outer hull.',
 'event':'Broad space-horror danger, realized by agent-owned staging: closing the final corner clamp of a temporary clear pressure partition.',
 'visual_priorities':['The clear membrane and its hatch perimeter divide a breathable corridor from a bay that opens directly onto black space.','Her connected right hand acts on the final lower-right clamp while the adjacent unfinished seam and outgoing condensation show why the action matters now.','Her reference-guided face, purposeful concentration, grounded crouch and bracing hand maintain a vulnerable human presence at the boundary.','The sheet bows into the bay and the visible tear behind it give the pressure direction and endangered living space an observable relationship.'],
 'baseline_prompt_en':baseline,'user_definitions':[],
 'interpretation_provenance':[{'term':'이번에 반영한 주제','source_text':'이번에 반영한 주제가 이미지에 실제로 반영되는지까지 테스트할 수 있는 주제에 어울리는 랜덤한 컨셉을 정하여','basis':'request_context','resolution':'The exact positive antecedent names space horror; the user leaves the concrete concept to independent random authoring. This entry resolves that reference without treating the selected spacecraft mechanics as requester specifications.','sources':[]},{'term':'첨부한 이미지를 활용하여','source_text':'첨부한 이미지를 활용하여','basis':'request_context','resolution':'Use the supplied portrait as a visual guide to facial appearance and hairstyle of the fictional subject; no real identity, age, personality, biography, outfit or body-shape claim is established.','sources':[]}],
 'unresolved_ambiguities':[],'user_exclusions':[],'runtime_forbidden_labels':[],
 'intent_lock':{'contract_version':'photo-intent-lock/v2','priority':'requesting_user','semantic_anchors':[
 {'anchor_id':'core_concept','source_text':'이번에 반영한 주제','dimension':'concept','prompt_evidence':'A photographic space-horror scene'},
 {'anchor_id':'core_subject','source_text':'첨부한 이미지를 활용하여','dimension':'subject','prompt_evidence':appearance_phrase},
 {'anchor_id':'core_event','source_text':'주제에 어울리는 랜덤한 컨셉을 정하여','dimension':'event','prompt_evidence':'a dangerous moment aboard a spacecraft'},
 {'anchor_id':'portrait_face_hair','source_text':'첨부한 이미지를 활용하여','dimension':'appearance','target':'woman','property':'reference.face_hair','prompt_evidence':appearance_phrase}
 ],'locked_dimensions':['concept','subject','event'],'open_dimensions':['identity','count','age','role','species','appearance','pose','body_geometry','expression','action','setting','relationship','sexual_tone','style','reference_use','viewer_outcome','text','format','framing','composition','lighting','camera','color','material','timing','atmosphere']},
 'semantic_assertions':assertions,'request_lineage':None,
 'style':{'domain':'photography','family':'restrained spacecraft emergency documentary','evidence':['warm portable work light against cold blue reflections','tactile condensation and restrained documentary grain']},'variation_key':'arm_b_cryo_partition_independent_draw'
}
save('authorial_core.input.json',core)
selection_rows=[
 ('feature.situation','The human aim, unfinished seal and dangerous opposite side form one incident.','The partition is the thin physical boundary preserving the corridor.'),
 ('feature.location','A traversable hatch connects safe corridor, cryogenic bay and exterior breach.','two frost-coated cryogenic storage capsules flank a torn opening'),
 ('feature.action','Her active closing grip has a specific reachable target and unfinished state.','Her right hand closes around the red lever'),
 ('feature.environmental_details','The membrane deformation and condensation carry the otherwise invisible pressure difference.','its clear sheet bows away from her into the depressurized bay'),
 ('feature.subject','Reference-guided facial presence carries the personal stake.','a woman whose facial appearance and hairstyle follow the supplied portrait'),
 ('feature.pose','The crouch gives her a stable stance beside the low clamp.','one knee on the corridor floor and the opposite boot planted firmly beside her'),
 ('feature.gaze','Attention connects face with the hazardous unsealed edge.','She watches the remaining gap as she works'),
 ('feature.spatial_depth','The single view must connect her near-side work with the far-side cosmic opening.','all four partition edges, her face, both connected arms, the grounded knee and boot, and the torn hull beyond')
]
selected=[]
for cat,reason,phrase in selection_rows:
    row={'category_id':cat,'basis':'agent_visual_choice','source_span_ids':[],'source_text':None,'derivation':None,'reason':reason,'baseline_evidence':phrase}
    if cat=='feature.subject':
       row.update(basis='request_derived',source_span_ids=['visual_request'],derivation='The user asks to use the supplied image; the reference is used for facial appearance and hairstyle only.')
    selected.append(row)
save('precore_feature_selection.input.json',{'selected':selected})
review={'contract_version':'photo-embodiment-review/v1','provenance':'agent_prepack','scope':'body_action','summary':'An ordinary human crouches beside a low right-side hatch clamp. Both arms remain on the pressurized corridor side and reach the same solid jamb. She braces above the working hand, with a floor knee and opposite planted boot supporting the load. The camera sees the full boundary, connected arms, exposed clamp and adjacent leaking seam simultaneously. The film bows away into the bay, not into her working space. The reference establishes visible face/hair only.','checks':{
 'body_ownership':{'status':'supported','reason':'The acting right hand and bracing left palm are explicitly hers; both connected arms remain visible in the frame.','prompt_evidence':['Her right hand closes around the red lever','her left palm braces the same solid jamb above the clamp','both connected arms']},
 'joint_chain_and_reach':{'status':'supported','reason':'She crouches directly beside the lower-right jamb rather than reaching across the hatch. Her right hand operates the nearby lever and the left reaches the same jamb above it.','prompt_evidence':['crouches beside the final clamp','folding it toward the lower-right jamb','her left palm braces the same solid jamb above the clamp']},
 'support_and_balance':{'status':'supported','reason':'One floor knee and opposite planted boot provide a stable base while the left palm braces a rigid frame. The support is visible at the selected frame scale.','prompt_evidence':['one knee on the corridor floor and the opposite boot planted firmly beside her','her left palm braces the same solid jamb above the clamp']},
 'contact_and_space':{'status':'supported','reason':'Her hand surrounds the physical lever and folds it into its jamb. The membrane bulges away into the bay while her arms stay on the corridor side, leaving room for the operation. The gap is immediately left of the lever, distinct from her grip.','prompt_evidence':['Her right hand closes around the red lever','Her arms remain on the corridor side of the sheet','a short unfinished seam remains visibly open just to the left of a red over-center lever']},
 'visibility_and_projection':{'status':'supported','reason':'The oblique wide-medium frame includes the complete seal perimeter, the hand/lever contact and the nearby leak without requiring a hidden reverse side. The clamp is explicitly unobstructed beside the hand. Her face remains larger than a background detail, with the bay tear behind the membrane.','prompt_evidence':['wide enough to include all four partition edges','Keep the clamp large and unobstructed beside her hand','the incompletely closed lever and the escaping threads visible together']}
}}
save('embodiment_review.input.json',review)
print(json.dumps({'baseline_words':len(baseline.split()),'baseline_sha256':hashlib.sha256(baseline.encode()).hexdigest(),'selected_features':len(selected),'concept':'cryo_bay_pressure_partition'},ensure_ascii=False))
