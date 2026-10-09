"""Direct pixel judgments for precisely the managed effective gate set."""
from pathlib import Path
import copy
import hashlib
import json

ARM=Path(__file__).resolve().parent
state=json.loads((ARM/'run/workflow.json').read_text())
shape_path=Path(state['artifacts']['visual_review_shape']['path'])
shape=json.loads(shape_path.read_text())
review=copy.deepcopy(shape['review'])
assert hashlib.sha256(Path(review['result_image']).read_bytes()).hexdigest()==review['result_sha256']
evidence={
 'vo_spring_sf057_02_visible_variant':
   'At native resolution the ivory vest has connected relief-bearing yarn loops surrounding many true diamond-shaped gaps. Each gap shows a lower peach textile surface, with sage inner cloth or skin visible through that blouse in the corresponding region. Opaque yarn, true gap and lower owner remain distinct on this one vest. Neither printed diamonds nor dark filled cells provide the evidence.',
 'vo_sheer_textile_first_read':
   'In the 320x480 thumbnail the peach long sleeves and extending blouse hem immediately read as an airy translucent garment under the openwork vest. They retain clear sleeve/cuff/hem silhouettes rather than appearing as a vague bright patch.',
 'vo_sheer_weave_edge_legibility':
   'Native wrist and hem regions show fine textile surface lines, stitched cuff boundaries, a stitched blouse hem and coherent fabric folds. These positive cloth features identify the same transmitting peach surface as textile; exact fiber or manufacturing process is not claimed.',
 'vo_sheer_transmission_relationship':
   'Both thumbnail and native chest/sleeve views show light passing through the peach blouse while softened arm skin, upper chest skin and sage inner-top cloth remain visible underneath. The peach cloth continues across the inner top\'s upper boundary. The visible window is behind the sleeves, and all lower surfaces belong to this same wearer. The intended lower owner is retained rather than replaced with an opaque covering.',
 'vo_sheer_layer_coherence':
   'At native resolution the single-layer sleeve areas transmit softened skin, while doubled gathering at the cuffs becomes visibly denser and less transparent. The blouse hem and overlapping folds are also denser than the flatter sleeve/chest regions. The material changes remain coherent within the same peach blouse.',
 'vo_sheer_not_optical_or_generation_substitute':
   'At thumbnail and native scale the transmitting surface has garment seams, cuffs and a cloth hem, with a continuously owned body underneath. The outside window glass and reflective damp floor are spatially separate. No glass layer, wet garment shine, blown-out white patch, missing garment or transparent-body artifact supplies the requested textile transmission.',
 'embodiment_body_ownership':
   'Native upper-body and contact regions connect both hands through their own wrists, peach sleeves and arms to the one woman. Her right hand is the raised clip-operating hand and her left hand reaches across to the lower paper margin. The hands remain distinct, with no additional unowned limb donating a contact.',
 'embodiment_joint_chain_and_reach':
   'The right shoulder, upper sleeve, bent elbow, forearm and wrist form a plausible reach to the upper clip. The left shoulder and bent arm lead to the lower paper corner across the torso. The two targets are within these connected reaches, with separate wrist directions and no fused limb segments.',
 'embodiment_support_and_balance':
   'The two separated shod feet visibly meet the floor beneath the turned torso, with no unsupported body lean. The drying line stays taut across the clip region and both hands currently support or steady the light sheet at different dry margins. The paper does not impose an implausible load or contradict the standing support state.',
 'embodiment_contact_and_space':
   'The native upper contact shows right thumb/index meeting the metal spring clip across the dry top paper margin, with the taut line meeting the upper clip region. The lower left thumb/fingers steady a separate dry border; that hand retains a continuous wrist and available space. Finger, paper, clip and line boundaries are coherent. The rear clip jaw lies naturally behind the paper; independent visibility of that hidden rear face is not claimed.',
 'embodiment_visibility_and_projection':
   'The full frame and native body/contact crops expose both operative hand regions, their connected arm chains, the lateral print and a substantial front vest/blouse area. Foreshortening does not erase the clip interaction or lower hand ownership, and the paper leaves the selected yarn gaps and transmitted lower surfaces assessable. The extra lower-body span also exposes the standing supports.',
}
assert set(evidence)==set(review['hard_gates'])
definitions={g['id']:g for g in shape['gate_definitions']}
for key,row in review['hard_gates'].items():
 required=definitions[key].get('review_scale','native')
 row.update(status='pass',evidence=evidence[key],reviewed_scales=['native','thumbnail'] if required=='both' else [required])
review['reviewer']='spring_knit_layer agent / direct inspection of one saved result'
review['user_judgment']={'baseline_available':False,'genuinely_moe':'pending','better_than_baseline':'not_applicable',
                         'source':'not_yet_received','evidence':'The requesting user has not yet judged this generated image.'}
review['observation_provenance']={'native_image_path':review['result_image'],'native_dimensions':[1024,1536],
                                'native_views':'One-to-one source-pixel crops and the full generated frame.',
                                'thumbnail_dimensions':[320,480],
                                'view_manifest':str(ARM/'review-view-manifest.json'),
                                'derived_shape_path':str(shape_path),'derived_shape_sha256':hashlib.sha256(shape_path.read_bytes()).hexdigest()}
review['supplemental_review_files']=[str(ARM/'supplemental-new-candidate-review.json'),str(ARM/'supplemental-topic-review.json')]
review['supplemental_limits']='The separately preplanned skirt waistband endpoint is covered by the blouse and is recorded as a supplemental failure. It is excluded from the exact hard_gates, and the associated color profile is not hard-activated.'
(ARM/'native-pixel-gate-review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'exact_hard_gate_count':len(review['hard_gates']),'passed':len(review['hard_gates']),
                  'user_judgment_source':review['user_judgment']['source']}))
