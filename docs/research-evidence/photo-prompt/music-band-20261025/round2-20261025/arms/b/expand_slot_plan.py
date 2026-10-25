import json,pathlib,hashlib,copy
p=pathlib.Path('docs/research-evidence/photo-prompt/music-band-20261025/round2-20261025/arms/b');a=json.loads((p/'authored-intents.json').read_text());m=json.loads(pathlib.Path('generated/photo-runs/music-band-20261025-r2-b/revisions/178f590d1e2146baba15598abfc5730e/slot_intent_material.json').read_text())
extras={
'anatomical_connection':('Connected shoulder-elbow-wrist chains establish both hands as one performer.', 'one pianist with two continuous shoulder elbow wrist and hand chains reaches different piano key registers while both legs connect to supported shoes'),
'body_pose':('Seated support and right pedal reach need a coherent local pose.', 'a securely bench-seated pianist balances over the seat with left shoe on floor and right heel grounded while the forefoot presses the rightmost sustain pedal'),
'hand_pose':('Separate fingertip-key surfaces need specific hand articulation.', 'a pianist left fingertips depress lower-register keys and right fingertips depress higher-register keys with unused keys visible between both contact groups'),
'relational_action':('The musical action must keep player, keys and sustain target linked.', 'one pianist simultaneously operates two separated piano keyboard registers and the rightmost sustain pedal with visible actor to target connections')}
for k,(reason,focus) in extras.items():
 r=copy.deepcopy(a['slots']['action']);r['reason']=reason;r['role_focus']=focus;r['expressive_goal']=reason;a['slots'][k]=r
reasons={
'apparatus_pov':'The capture is an ordinary exterior view; a depicted apparatus viewpoint is absent.',
'body_form':'The repair preserves the ordinary performer structure rather than developing a body-form change.',
'body_orientation':'The relevant orientation is already integrated into the searched seated body-pose relation; it supplies no independent expressive role.',
'body_region':'No isolated body region carries the photograph; the complete contact chain is handled as action.',
'camera_distance':'Distance is subordinate to keeping the exact full support frame; no independent distance expression is sought.',
'camera_height':'Bench-seat height belongs to the searched camera-direction relation and is not a second independent camera idea.',
'camera_movement':'A still camera exposure carries the scene; no capture movement is part of this moment.',
'camera_type':'No particular camera apparatus has visible meaning in the rehearsal.',
'capture_configuration':'A conventional single photograph has no special capture arrangement to express.',
'capture_context':'The recital rehearsal is preserved; no additional capture-context narrative is part of the repair.',
'depth_of_field':'Deep focus is the technical support of the integrated composition; no selective-focus story is developed.',
'exposure':'Ordinary legibility is retained and the consequential illumination is handled by the lighting role.',
'facial_geometry':'The supplied reference already governs facial proportions; reshaping this geometry is outside repair.',
'focus':'Continuous focus supports the searched composition rather than an independent focus transition.',
'grain_profile':'Grain is not an expressive carrier for these small contact endpoints.',
'image_artifact':'No recording artifact is involved in the intended photograph.',
'image_detail':'Fine legibility supports the contact action; no separate detail treatment is needed.',
'lens':'A moderate lens serves the complete frame and has no independent expressive distortion.',
'lens_artifact':'No flare or optical artifact participates in the current scene.',
'light_color':'Natural light color remains incidental to the required illumination relation.',
'light_direction':'The useful direction is integrated into the searched window and reflected-fill lighting role.',
'light_intensity':'The useful intensity is integrated into the searched face-to-pedal illumination role.',
'light_quality':'The soft quality is integrated into the searched window and reflected-fill lighting role.',
'light_shape':'No projected light shape or gobo carries the musical action.',
'light_type':'The existing window/reflected fill is handled as a single searched lighting relationship.',
'motion_rendering':'The shutter freezes the contacts; blur would obscure the target relations and is not a separate idea.',
'physical_motion':'The important movement is the searched instrument-operation action, not an independent moving-body motif.',
'platform_framing':'No platform-specific framing or embedded display is present.',
'procedure_step':'This is one ongoing musical phrase rather than a staged instructional procedure.',
'prop_placement':'The piano remains the played instrument; contact placement is integrated into action and composition.',
'reflection_logic':'The pale reflected fill is illumination, with no visible reflected subject or mirror path.',
'scale_relation':'The ordinary performer-piano scale is preserved, with no comparative size motif.',
'shadow_relation':'Shadow remains subordinate to the searched readable illumination rather than a separate relation.',
'shot_scale':'The complete required endpoints govern the frame; shot-size terminology adds no independent scene role.',
'silhouette_proportion':'Body and wardrobe proportions remain preserved appearance rather than a repair target.',
'spatial_depth':'The continuous depth serves the searched camera/composition relationship rather than another setting idea.',
'subject_framing':'The consequential framing is integrated into the searched complete composition.',
'transformation_stage':'No transformation or state-change sequence is depicted.',
'visual_density':'A quiet recital scene has no separate density change within the repair scope.',
'visual_hierarchy':'The same performer-and-contact hierarchy is developed in composition rather than a competing independent motif.'}
for k in m['requested_slot_ids']:
 if k in a['slots']:continue
 a['slots'][k]={'status':'not_applicable','reason':reasons[k],'expressive_goal':'','observable_targets':[],'owner_relations':[],'required_constraints':[],'preserved_choices':[],'open_scope':[],'unknowns':[],'role_focus':'','scene_context':'','language':'en','grounds':[],'review':{'author':'Codex','rationale':reasons[k]}}
(p/'authored-intents.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
