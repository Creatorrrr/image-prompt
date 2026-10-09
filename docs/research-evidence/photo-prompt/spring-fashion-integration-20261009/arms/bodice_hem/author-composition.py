"""B-arm composition after independent freeze; no shared assets are written."""
import hashlib
import json
from pathlib import Path

ARM = Path(__file__).resolve().parent
overview = json.loads((ARM / "composer-overview.json").read_text())
requirements = overview["requirements"]
details = json.loads((ARM / "composer-details.json").read_text())
available = {row["id"]: row["candidate"] for row in details["candidates"]}

prompt = """In this complex spring-fashion photograph, a woman guided by the supplied photograph has spring garments worn visibly together while securing a loose blue sheet on a rooftop worktable. Her visible face and short black bob follow the supplied photograph. The scene takes place beside a modest rooftop drying line on a clear spring afternoon: botanical cyanotype sheets hang at staggered heights above a mesh-topped table, and the sheet nearest her has slipped from its clip. Its lifted corner is already flattened beneath her right palm, while a crease still holds a little tent of blue paper beyond her fingertips. The next empty clip hangs immediately above that sheet, making the small unfinished task readable. She stands beside the table with both feet planted on the dry stone deck, her hips facing the camera and her right shoulder turned only slightly toward the tabletop. Her right forearm extends sideways to the mesh surface rather than across the garment front; her left hand holds the fallen wooden clip beside her left hip. She turns her face toward the camera with a quiet, almost amused awareness after arresting the paper, lips relaxed and a warm direct gaze. That brief personal connection adds a subtle attraction to an otherwise practical moment. The sleeveless blouse on this woman forms a square opening with a straight horizontal lower cloth edge; two upright side edges join its ends. This square border stays crisp above the repeated waist gathering as she arrests the blue paper. Two narrow shoulder straps start at the neckline corners, while close parallel horizontal gathers shape the fitted bodice. A distinct horizontal waist seam connects the gathered bodice to a short flared peplum; the peplum's cream lace edge forms a row of rounded scallops, each ending in its own outward curve. The waist seam and the outward flare remain clear across the front, while the narrow straps rise individually over the shoulders. Below it she wears an A-line midi skirt with an asymmetric lower edge: the front finishes near her upper calf and the back drops lower toward her ankle. She wears the pale warm beige blouse together with a warm ivory skirt; their muted tones sit close within one warm palette. The pale beige blouse and warm ivory skirt become two calm luminous planes against the cool blue drying prints. The flared peplum belongs to the blouse and lies outside the skirt, with a visible break between its scalloped edge and the smooth ivory skirt surface. Their cloth edges remain distinct where the beige upper layer meets the ivory lower layer. Low rust-colored shoes rest on the stone, and a breeze gives the skirt's rear panel a small lifted fold while the waist stays settled. The table occupies the side of the frame, leaving her neckline, bodice, waist connection, peplum and skirt edge readable as a continuous outfit. A few pale botanical silhouettes on the drying sheets echo the spring setting. A tray with two clips and the crisp moving sheet supply the nearby evidence of work, with rooftop railings and a distant brick wall behind. Photograph her from a comfortable three-quarter frontal position, with the full skirt edge and grounded shoes inside a vertical frame. Soft afternoon light makes the gathered cloth cast small repeated shadows; her face stays readable at the full-outfit distance, her hand and the paper contact remain crisply recognizable, and the rooftop railing remains a legible setting cue behind her. The hanging prints form quieter blue planes behind her. The image feels like an observed interruption in a real task, with convincing paper thickness, separate garment edges, natural facial texture and ordinary rooftop depth."""

square = "bundle:spf_sf004_01_bundle"
tonal = "bundle:spf_sf104_2_bundle"
visual = "visual-concept:vg_face_hands_place_readability_profile"
square_lower = "a straight horizontal lower cloth edge"
square_sides = "two upright side edges join its ends"
square_owner = "The sleeveless blouse on this woman forms a square opening"
tonal_colors = "She wears the pale warm beige blouse together with a warm ivory skirt; their muted tones sit close within one warm palette"
tonal_edges = "Their cloth edges remain distinct where the beige upper layer meets the ivory lower layer"
visual_fields = {
    "component_1_phrase": "her face stays readable at the full-outfit distance",
    "component_2_phrase": "her hand and the paper contact remain crisply recognizable",
    "component_3_phrase": "the rooftop railing remains a legible setting cue behind her",
}
clarification_rationales = {
    "embodied_corruption_transition": "An on-body dark transition would introduce a different event and visual hierarchy into this ordinary drying interruption; the optional meaning is not adopted.",
    "inverted_triangle_upper_body_dominant_relation": "The supplied visible face and hair do not ground a body-breadth category; no authored torso-width comparison is needed for the chosen garment construction.",
    "kuudere_composed_warmth_relation": "The scene has no independently grounded trusted counterpart or already-visible benefit for that counterpart. A quiet face alone would not establish the required character relation.",
    "one_piece_dress_construction": "The authorial outfit uses separate blouse and skirt with the blouse peplum outside the skirt; a continuous one-piece join would replace that construction.",
    "pc_pc23_owner_relation": "A handheld mirror would compete with the stabilizing right hand and clip-bearing left hand and add a different prop interaction, so that optional relation is declined.",
    "pfe_one_shoulder": "The authored square opening uses two shoulder supports; the optional single-support diagonal geometry would change the intended neckline study.",
    "rectangle_silhouette_relation": "A new bodily breadth comparison is unnecessary to observe the neckline, waist seam and separate hem boundaries and is not inferred from the reference portrait.",
    "sheer_garment_optical_layering": "The selected cloth geometry needs neither transmission nor an underlying layer. Introducing that optical relation would add a separate study beyond the selected spring candidates.",
}
clarifications = []
for row in requirements["semantic_clarification"]["candidates"]:
    cid = row["id"]
    if cid == "clarification:authorial-core:interpreted-intent":
        clarifications.append({"clarification_id": cid, "decision": "applied", "rationale": "All four minimum requester-owned anchors remain literal. The rooftop event, garments, palette and optical detail stay authorial choices within the frozen open dimensions.", "prompt_evidence": "In this complex spring-fashion photograph, a woman guided by the supplied photograph has spring garments worn visibly together"})
    elif cid.endswith("vg_face_hands_place_readability_profile"):
        clarifications.append({"clarification_id": cid, "decision": "applied", "rationale": "The selected optical-focus relation preserves the face, lateral hand-paper contact and already-authored rooftop railing together in the same full-outfit frame.", "prompt_evidence": ", ".join(list(visual_fields.values())[:2])})
    else:
        clarifications.append({"clarification_id": cid, "decision": "rejected", "rationale": clarification_rationales[cid.rsplit(":", 1)[1]]})

creative_rationales = {
    "augmentation:adult_appeal:sensual:garment_detail:vel_held_towel_continuous_front": "The two-hand towel tension and swimsuit coverage alternative would occupy both action hands and cover the garment front in this authorial cyanotype task.",
    "slot:capture_mode:sf_076_base": "A floor-supported capture plane with the actor rising would foreshorten the hand contact and gathered front. The open camera choice is retained at a comfortable three-quarter position for shared readability.",
    "slot:action:mep_in_between_candidate": "The independent scene already supplies the interrupted paper correction, settled foot support and displaced paper. An additional generic midway movement would not add a useful relation to this particular task.",
    "slot:garment_detail:spf_sf014_02": "The complete bilateral front-to-rear strap attachment paths cannot be assessed from this frontal outfit view. The independent front strap cues remain authorial without adopting this candidate's rear topology.",
    "slot:light_shape:fire_f012": "A continuous tapered flame envelope would introduce an unrelated light source. Afternoon light already gives the repeated gathers the small shadows needed here.",
}
creative = [{"candidate_id": cid, "decision": "rejected", "rationale": creative_rationales[cid]} for cid in requirements["creative_augmentation"]["candidates"]["deferred_candidate_ids"]]

adult = {
    "agency_phrase": "while securing a loose blue sheet on a rooftop worktable",
    "axes": {
        "sensual": {"intensity": 1, "realization": "baseline", "affected_dimensions": [], "artistic_interpretation": "A warm moment of camera awareness remains a subtle supporting attraction while she controls the paper; no new sensual-axis candidate or changed axis dimension is introduced.", "prompt_evidence": "lips relaxed and a warm direct gaze"},
        "fetish": {"intensity": 0, "realization": "baseline", "affected_dimensions": [], "artistic_interpretation": "The independent ordinary cloth-and-paper task receives no added fetish treatment."},
    },
    "blend": {"emphasis": "sensual_led"},
    "contextual_review": [
        {"candidate_id": "augmentation:adult_appeal:sensual:wardrobe_style:fit_ff03_v2_candidate", "reading": "potential", "reason": "The shared enlarged jacket body and sleeves could give a relaxed spring outline on this human subject, but would cover the gathered blouse and reduce the waist join's readability.", "proposed_application": "An open-dimension alternative would replace the visible upper layer with a roomy light jacket whose broad shoulder span, sleeves and torso share enlargement, while retaining the sheet task and full-outfit distance."},
        {"candidate_id": "augmentation:adult_appeal:sensual:expression:ae_smolder_attraction", "reading": "uncertain", "reason": "Its adult-scene and primary-attraction prerequisites are not grounded by the requester or the face reference. Iris target and eye opening alone do not supply those context prerequisites; the baseline warm direct awareness is retained."},
        {"candidate_id": "augmentation:adult_appeal:sensual:garment_detail:vel_held_towel_continuous_front", "reading": "irrelevant", "reason": "A held towel in front of a swimsuit is a different practical setup. Two towel grips and continuous front coverage would block the independently authored paper palm, clip hand and visible blouse construction."},
        {"candidate_id": "augmentation:adult_appeal:sensual:wardrobe_style:winter_wf24_v1_candidate", "reading": "potential", "reason": "An overlapping coat front and paired button rows could remain a composed clothing alternative for this human subject, but would bury the study's square opening, gathers and separate peplum boundary.", "proposed_application": "An alternate open appearance could use a light coat with visibly overlapping front panels and two button rows on the same coat while preserving the rooftop task; its closed front would replace the chosen exposed blouse details."},
    ],
    "contextual_comparison": "At the same sensual intensity 1, the independent warm direct awareness adds a small personal connection while her paper-stabilizing agency stays first. A roomy jacket could supply relaxed attraction and a paired-row coat could supply composed dress, but both reduce the particular upper-body cloth geometry being tested. The towel setup would change the action and block those edges, and the smoldering expression lacks independently grounded adult/primary-attraction context. Retaining the baseline eye connection and practical stance best keeps the whole person, spring outfit and unfinished task coherent at this strength.",
}

review = json.loads((ARM / "embodiment-review-input.json").read_text())
review["provenance"] = "agent_postcomposition"
review["prompt_sha256"] = hashlib.sha256(prompt.encode()).hexdigest()
review["summary"] += " Re-review of the full final prompt confirms that the adopted square opening and beige/ivory palette refine the neckline and color without changing the described body ownership, reachable table contact or planted support."

composed = {
    "composer": "agent",
    "prompt_en": prompt,
    "negative_en": requirements["negative_en"],
    "chosen_candidate_ids": [square, tonal],
    "chosen_visual_concept_ids": [visual],
    "coverage_assertions": {row["text"]: row["text"] for row in requirements["mandatory_intents"]},
    "candidate_interpretations": [
        {"candidate_id": square, "artistic_interpretation": "The rectangular neck border gives a quiet geometric anchor above the gathered peplum while her sideways arm keeps the same blouse front unobstructed.", "transformation": "Attach the lower and paired upright edges to the woman's existing sleeveless blouse and hold that border crisp above the rhythmic gathers in this paper-stopping moment.", "prompt_evidence": "This square border stays crisp above the repeated waist gathering as she arrests the blue paper", "affected_properties": available[square]["member_candidates"][0]["affected_properties"], "component_evidence": {"component_01": square_lower, "component_02": square_sides}, "relation_evidence": {"declared_owner": square_owner, "edge_01": "a straight horizontal lower cloth edge; two upright side edges join its ends"}},
        {"candidate_id": tonal, "artistic_interpretation": "Two related warm garment planes make the cool cyanotypes stand away from the wearer while the separate blouse and skirt edges preserve layered cloth construction.", "transformation": "Shift the independent pistachio-and-cream choice to a pale warm beige blouse and warm ivory skirt, keeping the peplum outside the skirt and its boundaries legible.", "prompt_evidence": "The pale beige blouse and warm ivory skirt become two calm luminous planes against the cool blue drying prints", "affected_properties": available[tonal]["member_candidates"][0]["affected_properties"], "component_evidence": {"component_1": tonal_colors, "component_2": tonal_edges}, "relation_evidence": {"existing_wearer_scope": "She wears the pale warm beige blouse together with a warm ivory skirt", "sf104_2_relation_1": tonal_colors, "sf104_2_relation_2": tonal_edges}},
    ],
    "authorial_core_binding": {
        "preserved_anchor_ids": ["core_concept", "core_subject", "core_event", "reference_use"],
        "preserved_evidence": [],
        "authorial_decisions": [
            {"dimension": "appearance", "decision": "Clarify the independent square neckline as the same horizontal lower edge joined by two upright sides on the woman's blouse.", "rationale": "The optional new geometry preserves the spring garment event and fits the existing two-strap gathered blouse; the user did not prescribe the garment outline.", "affected_properties": available[square]["member_candidates"][0]["affected_properties"]},
            {"dimension": "color", "decision": "Use pale warm beige on the blouse and warm ivory on the separate skirt, with their cloth edges still distinct.", "rationale": "Related muted warm planes test the new palette relation while the blue prints give the outfit a calm visible contrast; color was left open.", "affected_properties": available[tonal]["member_candidates"][0]["affected_properties"]},
            {"dimension": "camera", "decision": "Keep the face, lateral paper contact and rooftop railing readable together at the full-outfit distance.", "rationale": "The optical choice adopts one existing complete visual relation and supports the hand task without replacing the independent framing or requester reference use.", "affected_properties": available[visual]["affected_properties"]},
        ],
    },
    "semantic_clarification_decisions": clarifications,
    "creative_augmentation_brief": {"decisions": creative},
    "adult_appeal_brief": adult,
    "visual_obligation_evidence": {"vg_face_hands_place_readability_profile": visual_fields},
    "embodiment_review": {"review": review},
}

observations = {
    square: {
        "component_01": "Observe one straight horizontal lower cloth edge belonging to this woman's blouse neckline; the entire decisive edge must be visible at native and thumbnail scale.",
        "component_02": "Observe both upright side edges joining the respective ends of that same lower edge, making one three-sided opening on the same blouse; a U or V outline fails.",
        "declared_owner": "Trace the observed neckline to the sleeveless blouse actually worn on the primary woman, rather than a hanging print, railing or another garment.",
        "edge_01": "Trace continuous contact at both lower-edge-to-side-edge junctions on the same neckline, with both endpoints visible; disconnected, partly hidden or inferred junctions fail.",
    },
    tonal: {
        "component_1": "Observe a pale warm beige blouse and warm ivory skirt on the same wearer, both muted warm tones and close in palette; an unseen item or strongly opposed saturated pair fails.",
        "component_2": "Observe distinct upper and lower cloth boundaries between those garment colors, including the blouse peplum edge and separate smooth skirt surface.",
        "existing_wearer_scope": "Observe both the selected blouse and selected skirt actually worn by the primary woman; no background color may substitute for either item.",
        "sf104_2_relation_1": "Compare the blouse's visible muted warm tone with the skirt's visible muted warm tone in the same pixels, retaining a close tonal relation on those two owners.",
        "sf104_2_relation_2": "Trace the blouse cloth boundary as distinct from the skirt cloth boundary at their meeting region; a merged one-piece surface or an occluded relation fails.",
    },
}
plan = {
    "schema_version": "spring-fashion-supplemental-topic-plan/v1",
    "arm_id": "bodice_hem",
    "frozen_before_image_invocation": True,
    "pack_id": requirements["pack_id"],
    "source_generation": "a7fd58162695c7c23a9257ac89b13434e94e6899fc3891858b837636ad1ced6c",
    "selected_new_candidate_ids": [square, tonal],
    "chosen_visual_concept_ids": [visual],
    "spring_profile_hard_activation": "not_exposed_not_verified",
    "separate_from_runtime_hard_gates": True,
    "qualification": "Each selected topic is all-of across every component and relation below in the same actual saved image. Every required native and thumbnail observation must pass; partial, hidden, uncertain or unobservable is fail. No cross-image averaging.",
    "observations": [],
}
for cid in [square, tonal]:
    candidate = available[cid]
    interpretation = next(x for x in composed["candidate_interpretations"] if x["candidate_id"] == cid)
    for key, criterion in observations[cid].items():
        c = next((x for x in candidate["components"] if x["id"] == key), None)
        r = next((x for x in candidate["relations"] if x["id"] == key), None)
        plan["observations"].append({"observation_id": cid + ":" + key, "candidate_id": cid, "component_id": key if c else None, "relation_id": key if r else None, "source_contract_sha256": candidate["source_contract_sha256"], "concept_units": c["concept_units"] if c else [], "relation": r, "owner": "main_subject.worn_blouse" if cid == square else "main_subject.worn_blouse_and_skirt", "review_scales": ["thumbnail", "native"], "criterion": criterion, "prompt_evidence": interpretation["component_evidence" if c else "relation_evidence"][key]})
plan["additional_authorial_checks"] = [
    {"id": "gathered_bodice", "criterion": "Close parallel horizontal gathers visibly belong to the same fitted blouse body."},
    {"id": "waist_to_peplum", "criterion": "A distinct horizontal waist seam joins the blouse body to its short outward peplum."},
    {"id": "scallop_edge", "criterion": "The blouse peplum lace edge contains repeated separate rounded outward curves."},
    {"id": "high_low_skirt", "criterion": "The same separate A-line skirt visibly has a shorter front edge and lower rear edge; hidden or inferred rear edge fails."},
    {"id": "reference_visible_features", "criterion": "Compare visible face cues and the short black bob to the supplied reference; no identity or body measurement claim."},
    {"id": "complex_current_event", "criterion": "One current paper-stabilizing task shows the loose sheet, acting palm, held clip and drying line together with the worn outfit."},
]

def write(name, data):
    (ARM / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

assert all(phrase in prompt for row in composed["candidate_interpretations"] for mapping in [row["component_evidence"], row["relation_evidence"]] for phrase in mapping.values())
assert all(row["text"] in prompt for row in requirements["mandatory_intents"])
write("composed-input.json", composed)
write("selected-topic-plan.json", plan)
(ARM / "final-prompt.txt").write_text(prompt + "\n")
photo = Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
write("transport-input.json", {"references": [{"path": str(photo), "sha256": hashlib.sha256(photo.read_bytes()).hexdigest(), "role": "visible_face_and_short_black_bob_reference_only"}], "referenced_image_paths": [str(photo)], "transparent_background": False})
source = json.loads((ARM / "request_envelope.json").read_text())["request_text"]
write("authorization-input.json", {"lanes": ["native"], "invocation_limit": 1, "authorization_source": source})
print(json.dumps({"prompt_words": len(prompt.split()), "selected_new_candidates": [square, tonal], "topic_observations": len(plan["observations"]), "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(), "topic_plan_sha256": hashlib.sha256((ARM / 'selected-topic-plan.json').read_bytes()).hexdigest()}, indent=2))
