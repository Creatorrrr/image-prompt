"""Author direct-pixel observations on the one saved native image."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
state = json.loads((ROOT / 'run/workflow.json').read_text())
shape = json.loads(Path(state['artifacts']['visual_review_shape']['path']).read_text())
review = shape['review']
image = Path(review['result_image'])
assert hashlib.sha256(image.read_bytes()).hexdigest() == review['result_sha256']

judgments = {
    'vo_wkr_wk047_selected_relation_1': ('fail', ['native'], "In the original 1024x1536 image and unresampled cuff crop, the turned cuff has mottled cloth texture and a folded boundary, but individual fine yarn interlacing beside an identifiable stitched edge of that same cuff is not resolved. Hat braiding and jacket grain cannot substitute. Partial/unknown microstructure is fail."),
    'vo_vg_face_hands_place_readability_1': ('pass', ['native', 'thumbnail'], "The downward face has distinct facial contour, brows, eyelids, nose and pink lips at native size and in the 256x384 whole-image thumbnail. It remains readable inside the full seated portrait despite the hair fringe."),
    'vo_vg_face_hands_place_readability_2': ('pass', ['native', 'thumbnail'], "Both acting hands and the pinning hand's contact with the mustard ribbon on the straw crown are legible at native size and recognizable in the thumbnail. This gate proves optical hand/contact readability; it does not prove the separate right-hand needle assignment, which fails the actuation checks."),
    'vo_vg_face_hands_place_readability_3': ('pass', ['native', 'thumbnail'], "A diagonal railed gangway visibly joins the wet quay to the ferry doorway, with boat hull and cool water behind it; this place geometry remains identifiable at native and thumbnail scales. The boarding text is supplementary, not the only setting proof."),
    'embodiment_body_ownership': ('pass', ['native'], "One seated foreground woman owns both connected shoulders, sleeved arms, wrists and repair hands. The two booted lower legs belong to the same seated body; background people do not supply any foreground limb."),
    'embodiment_joint_chain_and_reach': ('pass', ['native'], "Both elbows bend forward over the supported lap, bringing separated hands to ordinary reachable positions around the same hat crown. The wrists have distinct contours without an extra hand or an implausibly long reach."),
    'embodiment_support_and_balance': ('pass', ['native'], "The seated skirt lies on the bench seat, the broad hat rests across the lap, and both boot soles meet wet paving. The support surfaces and local cloth contact are visible rather than inferred from floating objects."),
    'embodiment_contact_and_space': ('fail', ['native'], "The raised right thumb/index grip visibly draws golden thread legs. A needle-like thin line is at the ribbon beside the pinning left hand, while no single needle is demonstrably held between the raised right fingers. The required right-hand-to-needle-to-stitch chain is therefore partial/misassigned even though the broad repair gesture is coherent."),
    'embodiment_visibility_and_projection': ('fail', ['native'], "The frame retains head, shoulder-arm chains, hat, seat and boots, but the consequential needle-to-right-finger grip and its needle-eye-to-stitch connection cannot be inspected as declared. Visibility of hands and a nearby thin line is insufficient to establish that complete acting chain."),
}
assert set(judgments) == set(review['hard_gates'])
review['reviewer'] = 'arm_c_agent_direct_native_and_thumbnail_pixel_inspection'
for gid, (status, scales, evidence) in judgments.items():
    review['hard_gates'][gid] = {'status': status, 'evidence': evidence, 'reviewed_scales': scales}
review['user_judgment'] = {
    'baseline_available': False,
    'genuinely_moe': 'pending',
    'better_than_baseline': 'pending',
    'source': 'not_yet_received',
    'evidence': 'The requesting user has not evaluated this image. The preserved baseline is text; no baseline image was generated.',
}
(ROOT / 'visual_review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

observations = [
    {'id': 'wkr_wk095_selected_relation', 'status': 'pass', 'owner': 'same rust skirt and wooden bench seat', 'region_xyxy': [137, 820, 500, 1110], 'evidence': 'A continuous region of the worn rust skirt bunches into short folds where it lies against the wooden seat/front edge, with a cloth-to-wood contact shadow. This differs from the long hanging folds below. The visible locus is on the image-left side, so the authored left-thigh localization is not exact; the complete source relation is nevertheless present.', 'claim_limit': 'The visible contact and compression shape do not measure pressure or prove a mechanical history.'},
    {'id': 'wkr_wk047_selected_relation', 'status': 'fail', 'owner': 'moss jacket turned cuff', 'region_xyxy': [30, 620, 697, 832], 'evidence': judgments['vo_wkr_wk047_selected_relation_1'][2]},
    {'id': 'bundle_suf_sf064_v1', 'status': 'fail', 'owner': 'rust skirt', 'region_xyxy': [137, 820, 805, 1350], 'component_status': {'component_1': 'partial_is_fail', 'component_2': 'unobservable_is_fail', 'owner_relation': 'partial_is_fail'}, 'evidence': 'Long narrow ridges and valleys are visible, but they mix with irregular crumpling. The upper skirt edge is concealed beneath jacket/hat and cannot be traced continuously to the hem. Ordinary wrinkles or merely a pleated-skirt impression do not prove every adopted bundle component.'},
    {'id': 'vg_shared_airflow_hair_ribbon', 'status': 'fail', 'owner': 'same bob and mustard hat ribbon', 'region_xyxy': [200, 0, 700, 1060], 'relation_status': {'vg_shared_airflow_hair_ribbon_r1': 'pass', 'vg_shared_airflow_hair_ribbon_r2': 'fail', 'vg_shared_airflow_hair_ribbon_r3': 'fail'}, 'evidence': 'Short strands visibly connect to the bob. The long mustard strip is held on the crown, but its continuity to the encircling hat-band anchor is obscured by the fold/hand, and a shared directional response is not clear: hair fans around the face while the broad ribbon hangs mainly downward with a curl. Similar color, a held fold and loose shapes cannot complete the same-anchor/shared-airflow relation.', 'claim_limit': 'A still image cannot prove actual airflow or causal motion.'},
    {'id': 'two_hand_repair_and_single_needle_thread', 'status': 'fail', 'owner': 'right needle hand, left pinning hand, one hat', 'region_xyxy': [230, 535, 688, 866], 'observed_count': {'foreground_repair_hands': 2, 'hat': 1, 'needle_in_right_grip': 'not_resolved', 'complete_needle_eye_to_stitch_thread': 'not_resolved'}, 'evidence': 'The left pinning contact is visible, but the raised right fingers pull a golden thread loop/legs rather than clearly gripping one needle. A needle-like line lies near the left pinning fingers. Thread endpoints at the needle eye and one new stitch are not both traceable; older stitch count is also not resolved. The broad repair reads, while exact ownership/endpoints/quantity remain incomplete.'},
    {'id': 'left_fingers_pin_ribbon_to_crown', 'status': 'pass', 'owner': 'left hand and mustard folded ribbon on same straw crown', 'region_xyxy': [430, 676, 657, 790], 'evidence': 'Connected left fingers press the yellow fold directly against the crown; that contact is spatially coherent and separate from the raised opposite hand.'},
    {'id': 'crossbody_route_and_bag_junctions', 'status': 'fail', 'owner': 'walnut bag and brown strap', 'region_xyxy': [0, 315, 280, 1003], 'component_status': {'local_near_ring_tab_strap_bag_junction': 'pass', 'opposite_shoulder_crossbody_route': 'fail', 'multiple_ring_endpoint_count': 'unobservable_is_fail'}, 'evidence': 'One brass-colored oval ring clearly connects the strap and sewn leather tab on the same bag. The visible strap runs down from the same image-left shoulder to that hip rather than diagonally from the opposite shoulder. The far attachment/ring is not completely exposed; one local good junction cannot prove the complete crossbody route or plural endpoints.'},
    {'id': 'wardrobe_color_and_local_surface_carriers', 'status': 'fail', 'owner': 'jacket, top, skirt, ribbon, bag and boots', 'evidence': 'Moss/olive jacket, ivory vertically ribbed top, rust skirt, mustard ribbon and dark brown bag occupy distinct continuous owners. Lighter rolled inner cuffs differ from the outer sleeve, and plaited straw-like hat texture differs from garment texture. Two leather-looking ankle boots are visible; their shade is medium brown rather than the lighter tan wording, an authorial color drift.', 'claim_limit': 'These are rendered appearances. Cotton/fiber composition, authentic leather/straw/brass identity and hidden garment construction are not pixel-proven.'},
    {'id': 'reference_face_and_hair_guidance', 'status': 'pass', 'owner': 'generated foreground face and bob only', 'region_xyxy': [200, 0, 672, 444], 'evidence': 'Compared directly with the supplied photograph, the generated figure retains a dark chin-length bob with fine fringe, soft facial contour and natural pink lips. Downward eyelids make exact iris color unobservable. This supports visible face/hair guidance, without identity, actual age, body similarity or biography claims.', 'component_limit': 'Dark-eye iris-color fidelity is not separately passed because the downward gaze conceals it.'},
    {'id': 'place_and_tool_context', 'status': 'pass', 'owner': 'ferry quay, bench, lap hat and open pouch', 'evidence': 'Wet stone, reflective puddles, weathered wood, a mooring bollard, water and the gangway to the ferry form a coherent harbor setting. An open cloth pouch with one visible spool beside the seated person explains the available sewing tool context. Added signage and background people are not requester-owned details.'},
]
(ROOT / 'supplemental_pixel_review.json').write_text(json.dumps({
    'reviewer': review['reviewer'], 'result_image': str(image), 'result_sha256': review['result_sha256'],
    'method': 'Direct whole-image original, unresampled 1:1 native crops and 256x384 whole-image thumbnail',
    'inspection_manifest': str(ROOT / 'pixel_inspection/inspection_manifest.json'),
    'partial_or_unknown_policy': 'fail; no inferred hidden endpoints, counts, material identities or causation',
    'observations': observations,
    'boundary': 'Supplemental complete-relation judgments are separate from the exact effective hard-gate set; they are not extra hard gates.',
}, ensure_ascii=False, indent=2) + '\n')
(ROOT / 'whole_image_review.json').write_text(json.dumps({
    'reviewer': review['reviewer'], 'result_sha256': review['result_sha256'],
    'first_impression_record': str(ROOT / 'label_free_first_impression.json'),
    'scene_and_aesthetic': 'The face, supported hat and separate hands carry one absorbing harbor repair. Warm moss/ivory/rust/mustard surfaces and cool water/wet paving form a coherent travel photograph. The bench, pouch, ferry and bollard supply understandable context without taking the focal role from the person.',
    'controls_realization': {
        'sensual': {'configured': 1, 'agent_impression': 'Everyday attraction is a subtle support through absorbed presence, lips and practical clothing; the task remains dominant.'},
        'fetish': {'configured': 0, 'agent_impression': 'No material, body part or role is given special erotic significance.'},
        'surreal': {'configured': 0, 'agent_impression': 'The broad scene has coherent physical space and recognizable ordinary owners.'},
        'creativity': {'configured': 1, 'agent_impression': 'Refinements remain close to the independently authored ferry-quay repair.'},
    },
    'tradeoff': 'The full seated scene retains person, repair and place at the cost of unresolved fine cuff yarns and some small sewing endpoints. Its attractive whole-image read cannot turn these partials into passes.',
    'unexpected_additions': 'Journey/boarding signs in Japanese and English and several background people appeared; the script does not establish a real country or actual location.',
    'qualification': 'fail_complete_native_hard_gates_and_some_selected_optional_relations',
    'user_acceptance': 'pending_not_yet_received',
    'baseline_comparison': 'No baseline image exists. The diagnostic and requalification retrieval seeds differ, so no matched before/after causal claim is made.',
    'repair_render_count': 0,
}, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'hard_gates': len(judgments), 'pass': sum(v[0] == 'pass' for v in judgments.values()), 'fail': sum(v[0] == 'fail' for v in judgments.values()), 'user_judgment': review['user_judgment']}, ensure_ascii=False))
