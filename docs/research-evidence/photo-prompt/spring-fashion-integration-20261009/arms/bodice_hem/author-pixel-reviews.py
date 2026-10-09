"""Image-grounded B-arm observations of one saved native result."""
import hashlib
import json
from pathlib import Path

ARM = Path(__file__).resolve().parent
metadata = json.loads((ARM / "native-image-metadata.json").read_text())
shape_pointer = json.loads((ARM / "review-shape.json").read_text())
shape = json.loads(Path(shape_pointer["shapes"]["visual_review_shape"]).read_text())
review = shape["review"]
assert review["result_image"] == metadata["project_image_path"]
assert review["result_sha256"] == metadata["sha256"]
assert hashlib.sha256(Path(review["result_image"]).read_bytes()).hexdigest() == review["result_sha256"]

evidence = {
    "vo_vg_face_hands_place_readability_1": "Native 1024x1536: the primary woman's unobscured face has readable eyes, nose and mouth inside the full-outfit frame, with the short dark bob around it. Thumbnail 256x384: the face remains recognizable as the focal face and its directed camera awareness remains legible; no crop or prop covers it.",
    "vo_vg_face_hands_place_readability_2": "Native: the woman's right arm leads continuously to the palm and separated fingers flattening the blue botanical paper on the mesh table; the paper surface directly beneath the fingertips is sharp enough to identify the contact. Thumbnail: the lateral arm, light hand silhouette and flattened blue sheet form a clear single action/contact region, distinct from the hanging sheets.",
    "vo_vg_face_hands_place_readability_3": "Native: horizontal rooftop railing rails and vertical posts remain identifiable behind the wearer, with distant city buildings visibly softer. Thumbnail: that railing and skyline retain the form of an elevated rooftop setting. The background is subordinate rather than an equally sharp inventory of every object.",
    "embodiment_body_ownership": "Native: the hand on the blue sheet traces through one wrist, forearm, elbow and upper arm to the woman's right shoulder. Her other arm descends to the left hand holding the wooden clip beside her own left hip. The paper and clip belong to those distinct acted-on and held relations; there is no extra or transferred limb.",
    "embodiment_joint_chain_and_reach": "Native: the right shoulder-to-elbow-to-wrist chain reaches diagonally down and outward to the nearby side table, with a small natural elbow bend and no extension across the blouse front. The wrist meets the sheet in reach of that same arm. The left arm and clip hand remain separate and anatomically connected.",
    "embodiment_support_and_balance": "Native: both rust-colored low shoes meet the stone deck with corresponding contact/shadow regions. The stance is lightly crossed rather than the baseline's straighter stance, but the visible legs connect to the pelvis over the support area and the torso remains upright. The light paper press does not imply unsupported body weight or a floating foot.",
    "embodiment_contact_and_space": "Native: the right palm/finger pads rest on the paper laid over the mesh surface; a raised blue paper crease lies beyond that flattened contact region. Table, wrist and sheet do not intersect implausibly. The wooden clip is held at the separate hip-side hand rather than sharing the paper-pressing hand.",
    "embodiment_visibility_and_projection": "Native: the complete person, blouse front, waist band/join, peplum edge, asymmetric skirt edge and grounded shoes remain within the vertical frame. The table stays to the side and the reaching arm leaves the decisive neckline and garment front exposed. The hand-paper contact and the clip hand can be seen in this same view.",
}
assert set(evidence) == set(review["hard_gates"])
for gate in shape["gate_definitions"]:
    scales = ["thumbnail", "native"] if gate["review_scale"] == "both" else [gate["review_scale"]]
    review["hard_gates"][gate["id"]] = {"status": "pass", "evidence": evidence[gate["id"]], "reviewed_scales": scales}
review["reviewer"] = "agent"
review["user_judgment"] = {"baseline_available": False, "genuinely_moe": "pending", "better_than_baseline": "not_applicable", "source": "not_yet_received", "evidence": "No requesting-user judgment of this generated image or generated baseline comparison has been received. The supplied photo is a visible-feature reference, not a user-rated render baseline."}

topic_plan = json.loads((ARM / "selected-topic-plan.json").read_text())
topic_evidence = {
    "bundle:spf_sf004_01_bundle:component_01": {"native": "The blouse's front opening has one macroscopically straight lower edge running across the upper chest. Local fabric ruffling introduces small edge waves, but the contour does not descend as a rounded U or converge to a V.", "thumbnail": "The opening's lower border reads as one near-horizontal chest line rather than a U or V; its full span remains inside the unobstructed blouse front."},
    "bundle:spf_sf004_01_bundle:component_02": {"native": "A pair of upright cloth sides/front shoulder supports rise from the respective ends of that lower front border on the same blouse. The small perspective tilt of the right support does not replace either side with a rounded neckline slope.", "thumbnail": "Both pale side supports rise separately from the two ends of the flat opening. Together with the lower border they retain the three-sided square opening."},
    "bundle:spf_sf004_01_bundle:declared_owner": {"native": "The neck opening is attached to the pale blouse wrapped around the primary woman's torso and supported on her two shoulders; it is not a print or background structure.", "thumbnail": "The opening and two supports remain visibly on the sole wearer's blouse."},
    "bundle:spf_sf004_01_bundle:edge_01": {"native": "The left and right ends of the lower chest border meet the respective cloth side/support edges continuously. Both lower junctions are exposed between the shoulders and gathered body.", "thumbnail": "Both junctions can be traced where the pale side supports meet the chest border; neither end is covered by the acting arm, paper or bob."},
    "bundle:spf_sf104_2_bundle:component_1": {"native": "The worn upper blouse is light beige/peach cream and the worn skirt is warm off-white. Both are muted warm tones in a close light palette, while the blue prints are a separate cool background contrast.", "thumbnail": "The upper beige cream and lower warm off-white remain a close, low-saturation warm pair on the woman, distinguishable from the cool blue sheets."},
    "bundle:spf_sf104_2_bundle:component_2": {"native": "The blouse peplum's shaped lace edge lies outside a separate smoother ivory skirt surface. That overlap gives each color-bearing cloth layer its own visible boundary.", "thumbnail": "The flared blouse edge remains a separate outline over the smoother skirt plane; the two layers do not merge into one uninterrupted front surface."},
    "bundle:spf_sf104_2_bundle:existing_wearer_scope": {"native": "The pale blouse covers the primary woman's torso and the ivory skirt surrounds her hips and legs; both belong to this same wearer's visible outfit.", "thumbnail": "Both selected light garments are worn on the sole primary woman, rather than supplied by a plant, tabletop or hanging print."},
    "bundle:spf_sf104_2_bundle:sf104_2_relation_1": {"native": "Comparing the visible blouse body with the smooth skirt front shows neighboring light beige and warm ivory tones, not strongly opposed saturated colors. Sunlight changes local values without breaking the relation.", "thumbnail": "The two worn garment planes keep their adjacent pale warm color relation in the same frame."},
    "bundle:spf_sf104_2_bundle:sf104_2_relation_2": {"native": "The upper blouse's peplum perimeter is a foreground cloth edge, with the skirt continuing as its own cloth surface and separate asymmetric hem below it. Both endpoints of the compared boundary relation are visible.", "thumbnail": "The blouse's short flared lower outline and the skirt's longer smooth body/hem remain distinct at their meeting region."},
}
assert set(topic_evidence) == {row["observation_id"] for row in topic_plan["observations"]}
topic_review = {
    "schema_version": "spring-fashion-supplemental-topic-review/v1",
    "reviewer": "agent",
    "result_image": metadata["project_image_path"],
    "result_sha256": metadata["sha256"],
    "source_plan_path": str(ARM / "selected-topic-plan.json"),
    "source_plan_sha256": hashlib.sha256((ARM / "selected-topic-plan.json").read_bytes()).hexdigest(),
    "source_generation": topic_plan["source_generation"],
    "separate_from_runtime_hard_gates": True,
    "spring_profile_hard_activation": "not_exposed_not_verified",
    "qualification_rule": topic_plan["qualification"],
    "observations": [],
    "candidate_results": {},
}
for planned in topic_plan["observations"]:
    observed = topic_evidence[planned["observation_id"]]
    topic_review["observations"].append({"observation_id": planned["observation_id"], "candidate_id": planned["candidate_id"], "source_contract_sha256": planned["source_contract_sha256"], "owner": planned["owner"], "relation": planned["relation"], "status": "pass", "scales": {scale: {"status": "pass", "evidence": observed[scale]} for scale in planned["review_scales"]}})
for cid in topic_plan["selected_new_candidate_ids"]:
    rows = [x for x in topic_review["observations"] if x["candidate_id"] == cid]
    topic_review["candidate_results"][cid] = {"status": "pass" if all(x["status"] == "pass" and all(s["status"] == "pass" for s in x["scales"].values()) for x in rows) else "fail", "all_of_observation_count": len(rows), "same_image": True}

additional = {
    "schema_version": "spring-authorial-and-artistic-review/v1",
    "result_image": metadata["project_image_path"],
    "result_sha256": metadata["sha256"],
    "not_runtime_hard_gates": True,
    "user_judgment_source": "not_yet_received",
    "requester_obligations": [
        {"anchor_id": "core_concept", "status": "pass", "evidence": "A photographic rooftop work scene integrates a person, worn spring cloth construction, blue botanical drying sheets, side table and visible paper correction as one current complex concept."},
        {"anchor_id": "core_subject", "status": "pass", "evidence": "The sole primary woman uses visible facial cues and short dark bob guidance from the actually attached local reference; this observation does not establish real-world identity."},
        {"anchor_id": "core_event", "status": "pass", "evidence": "The gathered blouse with flared peplum and separate asymmetric skirt are worn together in the same saved frame."},
        {"anchor_id": "reference_use", "status": "pass", "evidence": "Both source and output show a short dark bob, wispy forehead strands and comparable visible eye/nose/mouth arrangement. The output uses a new current scene and body portrayal; no source biography or body measurement is inferred."},
    ],
    "authorial_observations": [
        {"id": "gathered_bodice", "native_status": "pass", "thumbnail_status": "pass", "evidence": "Repeated horizontal compressed rows organize the blouse front, with gathered cloth relief between the rows; these visible shapes belong to the same fitted upper garment."},
        {"id": "waist_to_peplum", "native_status": "pass", "thumbnail_status": "pass", "evidence": "A horizontal waist band/join separates the fitted gathered body from the outward-flaring short peplum below it."},
        {"id": "scallop_edge", "native_status": "pass", "thumbnail_status": "fail", "evidence": "Native pixels show repeated rounded lace-edge lobes along the peplum perimeter. At 256x384 the lacy waviness is visible but individual rounded endpoints cannot all be confirmed, so that fine additional authorial detail is unobservable and fails at thumbnail scale."},
        {"id": "high_low_skirt", "native_status": "pass", "thumbnail_status": "pass", "evidence": "The exposed front skirt edge stops above the visibly lower rear/side continuation. The same skirt flares over the legs and keeps its longer rear edge inside the image."},
        {"id": "reference_visible_features", "native_status": "pass", "thumbnail_status": "pass", "evidence": "Visible face guidance and the short dark bob remain recognizable in the output. Fine source skin marks are not treated as an identity requirement."},
        {"id": "complex_current_event", "native_status": "pass", "thumbnail_status": "pass", "evidence": "One hand presses the loose blue sheet on the mesh table while the other holds a wooden clip; botanical sheets hang on the drying line behind the same worn outfit."},
    ],
    "artistic_observation": "The woman is the first focal presence, with warm camera awareness that remains subordinate to her practical paper correction. Blue botanical sheets establish a convincing color counterpoint to the two pale warm garment planes, and the raised paper crease/held clip connect the gesture to an unfinished task. The side table permits both contact and garment fronts to read. The slightly crossed stance feels more posed than the independent straighter baseline but remains mechanically plausible. Fine lace ends weaken at small thumbnail scale; that detail limit does not establish requesting-user acceptance or negate the separately inspected native geometry.",
    "agent_overall_artistic_judgment": "coherent_and_appealing_with_thumbnail_detail_limit",
}

def write(name, data):
    (ARM / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

write("visual-review-input.json", review)
write("supplemental-topic-review.json", topic_review)
write("supplemental-artistic-review.json", additional)
print(json.dumps({"exact_hard_gate_count": len(review["hard_gates"]), "hard_statuses": {k: v["status"] for k, v in review["hard_gates"].items()}, "supplemental_topic_pass": len(topic_review["observations"]), "new_candidate_results": topic_review["candidate_results"], "additional_thumbnail_failures": [x["id"] for x in additional["authorial_observations"] if x["thumbnail_status"] == "fail"], "requesting_user_judgment": "not_yet_received"}, indent=2))
