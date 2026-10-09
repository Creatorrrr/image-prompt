"""Agent-authored judgments from direct whole/thumbnail/native pixel inspection.

This does not infer visual truth from a schema or source ID. All statuses below
were authored after viewing the same saved native result and its inspection views.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ARM = Path(__file__).resolve().parent
WORKTREE = Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
GENERATION = 'a7fd58162695c7c23a9257ac89b13434e94e6899fc3891858b837636ad1ced6c'
SOURCE_FINGERPRINT = '6d92970bf0f1f1acb3cf20b2ac5262a357f61f89b4dd03b1ede39945b77d1b8a'

def load(path):
    return json.loads(Path(path).read_text())

def write(name, value):
    (ARM/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

STATE = load(ARM/'run/workflow.json')
META = load(ARM/'native-result-metadata.json')
IMAGE = META['saved_image']
assert sha(IMAGE) == META['sha256']
PLAN = load(ARM/'new-topic-observation-plan.json')
assert sha(ARM/'new-topic-observation-plan.json') == load(ARM/'native-preinvoke-bindings.json')['supplemental_plan_sha256']

apron = {
    'component_1': 'At native scale, the two sage shoulder straps descend into separate upper bib corners, with a round button at each junction. Both joins resolve as garment edges on the same outer dress.',
    'component_2': 'The apricot blouse has a separate rounded neckline and two gathered sleeves; sage straps cross in front of its chest/shoulder fabric, and the sage bib occludes the central blouse. The blouse side sections remain visible outside the bib edges.',
    'existing_wearer_scope': 'The apricot neckline and sleeves enclose the seated wearer, and the sage bib, straps, waist and skirt surround that same torso and legs. No second wearer or separate displayed garment supplies a component.',
    'sf071_1_relation_1': 'Each sage strap terminates at its own upper corner of the sage bib with a visible button junction. The left and right corners both remain visible, including the corner below the flower.',
    'sf071_1_relation_2': 'Local boundaries put the sage straps and bib in front of apricot blouse fabric. The inner blouse neckline is visible above the bib and apricot sleeves extend independently beside the sage outer edges.',
}
shoe = {
    'component_1': 'Both ivory flats have a distinct broad narrow strap arching over the dorsal foot between the open toe/vamp and ankle. These solid straps are separate from the higher ankle ribbon crossings.',
    'component_2': 'On each flat, one solid strap edge meets the upper wall on the image-left side and the other meets the upper wall on the image-right side. The four contact locations are visible as joined upper boundaries, without requiring a hidden fastening method.',
    'sf107_02_edge_1': 'The solid strap crosses the visible top of each foot belonging to its own flat; the image-left and image-right shoes each satisfy the dorsal route. Higher ankle ribbons are not substituted for this strap.',
    'sf107_02_edge_2': 'For each shoe, the strap endpoint on the inward side meets the matching inward upper wall rather than skin or the other shoe. Both the farther image-left flat and nearer image-right flat show that boundary contact.',
    'sf107_02_edge_3': 'For each shoe, the opposite strap endpoint meets that shoe outer upper wall. The farther flat shows the curved end meeting its upper rim; the nearer flat shows its other end descending to the outer upper rim. Neither endpoint floats off the shoe.',
}
instances = [
    {'owner': 'main_subject.right_foot / image-left farther ivory flat', 'route': 'solid strap arches over that exposed dorsal foot', 'end_inward': 'strap edge meets the rim on the side facing the other shoe', 'end_outward': 'opposite strap edge meets the rim on the outward side', 'status':'pass'},
    {'owner': 'main_subject.left_foot / image-right nearer ivory flat', 'route': 'solid strap crosses that exposed dorsal foot between the toe opening and ankle', 'end_inward': 'strap edge meets that flat own inward upper wall', 'end_outward': 'opposite edge descends to that flat own outward upper wall', 'status':'pass'},
]
new_rows=[]
for source in PLAN['observations']:
    row=dict(source)
    key=row.get('source_component_id') or row['source_relation_id']
    row.update({'status':'pass','evidence':(apron if 'sf071' in row['candidate_id'] else shoe)[key], 'reviewed_scales':['native'], 'visibility':'both endpoints and declared owner observable in the same saved result', 'inspection_view':'torso_native.png' if 'sf071' in row['candidate_id'] else 'shoe_native.png'})
    if 'sf107' in row['candidate_id']:
        row['separate_shoe_instances']=instances
    new_rows.append(row)
write('new-topic-pixel-review.json', {'schema_version':'spring-topic-supplemental-review/v1','source_plan':str(ARM/'new-topic-observation-plan.json'),'source_plan_sha256':sha(ARM/'new-topic-observation-plan.json'),'image':{'path':IMAGE,'sha256':META['sha256'],'dimensions':META['dimensions']},'reviewer':'spring_ornament_shoe agent / direct native inspection','runtime_generation':GENERATION,'classification':'supplemental_topic_review_separate_from_runtime_hard_gates','pass_policy':PLAN['pass_policy'],'observations':new_rows,'candidate_results':[{'candidate_id':candidate,'status':'pass','passed_observations':5,'total_observations':5} for candidate in PLAN['selected_candidate_ids']],'overall_status':'pass','passed_observations':10,'total_observations':10,'spring_profile_hard_activation':'not_verified_not_promoted','unexposed_profile_ids':PLAN['unexposed_profile_ids'],'claim_limits':PLAN['claim_limits']})

baseline_evidence = {
    'obs_reference': ('pass', 'The face preserves reference-guided dark eyes, delicate facial contour and soft lip shape; the hair is a dark chin-length bob with fine separated forehead fringe. Different pose and expression prevent exact equality claims. This is visible appearance guidance only.'),
    'obs_flower': ('fail', 'Raised curled fabric petals and a compact flower center are visible, but the flower base sits on the sage outer shoulder strap, rather than flush against the declared apricot blouse. Correct garment ownership fails.'),
    'obs_drape': ('fail', 'Apricot cloth shows neckline and sleeve gathers. The sage bib covers the central torso, and neither a complete left-shoulder-to-opposite-waist diagonal nor folds starting beneath the flower on the blouse can be traced. Partial/occluded geometry fails.'),
    'obs_wrap': ('pass', 'A diagonal sage free edge crosses the lap below the waist fastening and lies above another sage surface with a clear local shadow. Both surfaces belong to the same outer dress lower section.'),
    'obs_pleats': ('pass', 'Repeated folded ridges begin below the sage overlapping panel, spread across the bent-knee region and continue down to a visible flared hem. They are raised cloth folds rather than printed stripes. Covered anatomy does not prove exact knee measurements or manufacture.'),
    'obs_ribbons': ('fail', 'The visible X crossings and bows surround the ankles. Their continuous route to rear shoe fittings and an X across the instep is not observable. The separate solid instep straps satisfy the new shoe candidate, but cannot substitute for the baseline ribbon route.'),
    'obs_clip': ('fail', 'Right-hand digits hold a wooden peg at a paper corner, but no wire is visibly caught in the same jaw. The second upper corner support and intended paper-wire coupling are not demonstrable; the board-backed substitute is only partial.'),
    'obs_support': ('pass', 'The wearer sits on a timber bench, left palm contacts the seat beside the hip, connected legs reach two feet whose soles contact the same dock planks. Nothing indicates hovering or detached limb support.'),
    'obs_story': ('fail', 'The wet planks, dock notices, fastening gesture and nearby boat provide a readable ferry setting. However, the specified diagonal damp crease and already-fastened opposite corner are not clearly visible; she faces the viewer rather than turning toward the boat. The full planned moment is partial.'),
}
baseline_rows=[]
for row in load(ARM/'prepixel-plan.json')['observations']:
    status,evidence=baseline_evidence[row['observation_id']]
    baseline_rows.append({'observation_id':row['observation_id'],'authority':row['authority'],'status':status,'evidence':evidence,'reviewed_scales':['native','thumbnail'] if row['review_scale']=='both' else [row['review_scale']]})
write('baseline-supplemental-pixel-review.json', {'schema_version':'spring-baseline-supplemental-review/v1','source_plan':str(ARM/'prepixel-plan.json'),'image':{'path':IMAGE,'sha256':META['sha256']},'classification':'supplemental_observations_not_runtime_hard_gates','policy':'all requested components within each planned observation; partial or unobservable is fail','observations':baseline_rows,'passed':sum(x['status']=='pass' for x in baseline_rows),'total':len(baseline_rows),'overall_status':'fail','note':'The standalone baseline skirt was authorially refined into the selected sage outer dress. Its actual lower panel relationships are assessed here without converting authorial staging into user locks.'})

write('user-duty-pixel-review.json', {'schema_version':'spring-requester-duty-review/v1','image':{'path':IMAGE,'sha256':META['sha256']},'reviewer':'spring_ornament_shoe agent / direct pixel inspection','duties':[{'anchor_id':'core_concept','status':'pass','evidence':'The image reads as a photographic spring clothing scene, with a light blouse, sage dress and light flats worn in an outdoor landing setting.'},{'anchor_id':'core_subject','status':'pass','evidence':'One central human wearer has a face and short dark hairstyle consistent with reference appearance guidance. The exact original portrait was attached in the native call.'},{'anchor_id':'core_event','status':'pass','evidence':'Spring clothing structures are worn on the same seated subject: joined dress straps/bib, blouse/dress layers, lower panel and shoe straps are visible.'},{'anchor_id':'reference_appearance','status':'pass','evidence':'Dark bob contour, fine forehead fringe, dark eyes and soft facial/lip contour track visible source guidance. This establishes appearance guidance only, not personal identity or biography.'}],'overall_status':'pass','source_reference_sha256':'06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7','claim_limit':'No identity, personality, life history, body dimension or private feeling inference.'})

write('artistic-impression-review.json', {'schema_version':'spring-artistic-impression-review/v1','image':{'path':IMAGE,'sha256':META['sha256']},'first_impression':META['first_whole_image_impression'],'subject_presence':'The reference-guided face and composed current work gesture provide a warm central presence. The sage garment edges and pleats form a coherent secondary rhythm; the boat and wet landing make the place readable.','situational_limit':'The subject looks toward the viewer and the paper/clip is board-backed; the authored return-and-repair relation is less precise than planned. Added umbrella/tote decorations are incidental and do not prove a clothing or user duty.','whole_image_preference':'A convincing and attractive quiet spring photograph, but the complete contact mechanism and several authorial garment details remain unqualified.','control_assessment_after_first_impression':{'sensual':{'observed_ordinal_impression':1,'evidence':'Subtle warmth comes from the relaxed portrait and practical action, with clothing and place carrying the composition.'},'fetish':{'observed_ordinal_impression':0,'evidence':'The whole frame presents normal spring clothing and work. Footwear details are inspectable parts of the outfit; there is no added focused erotic treatment.'},'creativity':{'observed_ordinal_impression':1,'evidence':'A grounded dock repair situation combines the clothing structures and wet timber rhythms without changing the scene into spectacle.'},'surreal':{'observed_ordinal_impression':0,'evidence':'The garment, bench, water, boat and body inhabit one ordinary photographic space. Failed clip-wire detail is a fidelity limit, not an authored surreal mechanism.'}},'assessment_boundary':'Agent qualitative impression after direct inspection; not a statistical intensity score or user acceptance.','user_judgment':{'source':'not_yet_received','status':'pending'}})

# The managed recorder binds native plan + original tuple before this helper is
# used. This creates the standard independently validated manifest without
# replaying or enriching an existing immutable ledger row.
entries=[json.loads(x) for x in (ARM/'image_runs.ndjson').read_text().splitlines() if x.strip()]
assert len(entries)==1
entry=entries[0]
assert entry['image_call_count']==1 and entry['image_paths']==[IMAGE]
assert entry['image_hashes']==[{'path':IMAGE,'sha256':META['sha256']}]
sys.path.insert(0,str(WORKTREE/'skills/photo-prompt-image-generator/scripts'))
from record_image_run import build_independent_manifest
args=SimpleNamespace(candidate_pack_version='v6',arm_id='ornament_shoe',worktree_id='spring-fashion-integration-20261009',skill_sha256=sha(WORKTREE/'skills/photo-prompt-image-generator/SKILL.md'),source_ref='runtime-generation:'+GENERATION,image_call_count=1,authorial_core_sha256=entry['authorial_core_sha256'],intent_lock_sha256=entry['intent_lock_sha256'],independent_no_cross_arm_inputs=True,reference_sha256=entry['reference_sha256'])
manifest=build_independent_manifest(entry,args)
assert args.skill_sha256=='9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b'
write('independent-run-manifest.json',manifest)
write('independent-manifest-validation.json',{'status':'pass','builder':'current record_image_run.build_independent_manifest','manifest_path':str(ARM/'independent-run-manifest.json'),'manifest_sha256':sha(ARM/'independent-run-manifest.json'),'managed_ledger_path':str(ARM/'image_runs.ndjson'),'ledger_sha256':sha(ARM/'image_runs.ndjson'),'ledger_row_count':1,'ledger_run_id':entry['run_id'],'image_call_count':1,'runtime_generation':GENERATION,'source_fingerprint':SOURCE_FINGERPRINT,'cross_arm_inputs_used':False,'no_ledger_replay':True,'note':'Managed native-result has no recorder-extra CLI flags. The standard manifest builder validates the arm metadata against the one concrete native ledger entry; the ledger row remains unchanged.'})

if 'visual_review_shape' in STATE['artifacts']:
    shape=load(STATE['artifacts']['visual_review_shape']['path'])
    review=shape['review']
    evidence={
        'vo_one_piece_continuous_unit':('pass','At thumbnail scale, the sage shoulder straps, bib, waist and skirt form one outer dress over a clearly distinct apricot blouse. The sage dress unit continues from upper bib/straps to lower hem.'),
        'vo_one_piece_silhouette_legible':('pass','Thumbnail and native views show a fitted sage waist and a lower skirt widening toward the hem; the seated drape retains the selected A-line outline rather than separate trouser legs.'),
        'vo_one_piece_construction_detail':('pass','Native detail shows two strap-to-bib button junctions, a waist band/seam with side button, a diagonal overlapping panel and raised pleats continuing into the same lower dress. These features form a plausible continuous construction.'),
        'vo_one_piece_neckline_to_hem':('pass','The full frame includes the sage upper bib edge and straps, waist connection, overlapping lower panel and complete hem. The separate apricot neckline does not replace the visible sage dress upper boundary.'),
        'vo_one_piece_not_adjacent_sense':('pass','The thumbnail reads as a sage apron dress over a blouse, without matching detached sage separates, jumpsuit/romper legs, swimwear or franchise cues.'),
        'embodiment_body_ownership':('pass','The raised right arm and holding digits connect to the same wearer; her left palm contacts the seat on the other side. Both visible legs and shoe-bearing feet belong to that one seated body.'),
        'embodiment_joint_chain_and_reach':('pass','The visible right shoulder, upper arm, bent elbow, forearm and hand form a coherent reachable chain to the close board. The hand is higher than the authored shoulder-level staging, but the current reach is physically coherent and the clip remains the right-hand target.'),
        'embodiment_support_and_balance':('pass','The wearer sits on a timber seat with left palm beside the hip; both connected feet rest on dock planks. The bench/sole contacts support the seated state and the reaching hand does not bear the body load.'),
        'embodiment_contact_and_space':('fail','Native hand detail shows a wooden peg at a paper corner with fingers contacting it, but no wire visibly passes through the same clip jaw. Paper backed by the wooden board is not the declared paper-and-wire coupling; the intended contact is partial.'),
        'embodiment_visibility_and_projection':('fail','The face, dress and shoes are exposed, but the consequential clip-to-paper-to-wire relation is not assessable. The wire endpoint is absent or hidden in the board area, so clear general framing cannot qualify that missing critical relationship.'),
    }
    assert set(review['hard_gates'])==set(evidence)
    defs={x['id']:x for x in shape['gate_definitions']}
    for key,row in review['hard_gates'].items():
        status,text=evidence[key];scale=defs[key].get('review_scale','native')
        row.update({'status':status,'evidence':text,'reviewed_scales':['native','thumbnail'] if scale=='both' else [scale]})
    review['reviewer']='spring_ornament_shoe agent / direct whole-image, thumbnail and 1:1 native inspection'
    review['user_judgment']={'baseline_available':False,'genuinely_moe':'pending','better_than_baseline':'not_applicable','source':'not_yet_received','evidence':'No requesting-user judgment has been received for this generated result.'}
    write('visual-pixel-review.json',review)
    write('exact-hard-gate-checklist.json', {'schema_version':'spring-effective-gate-checklist/v1','runtime_generation':GENERATION,'pack_id':review['pack_id'],'effective_visual_contract_sha256':entry['effective_visual_contract_sha256'],'source_shape':STATE['artifacts']['visual_review_shape'],'image':{'path':IMAGE,'sha256':META['sha256']},'required_gate_ids':list(review['hard_gates']),'gate_definitions':shape['gate_definitions'],'passed':sum(x['status']=='pass' for x in review['hard_gates'].values()),'total':len(review['hard_gates']),'failed_gate_ids':[k for k,v in review['hard_gates'].items() if v['status']=='fail'],'supplemental_rows_merged_into_hard_gates':False})
    print(json.dumps({'status':'authored','effective_hard_gates':len(evidence),'hard_passed':8,'hard_failed':2,'new_topic_passed':10,'new_topic_total':10,'ledger_rows':1,'manifest_valid':True}))
else:
    print(json.dumps({'status':'supplemental_and_manifest_authored','new_topic_passed':10,'new_topic_total':10,'waiting_for_managed_visual_review_shape':True}))
