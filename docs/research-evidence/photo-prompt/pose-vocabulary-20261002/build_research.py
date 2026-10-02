#!/usr/bin/env python3
"""Build this research dossier only; never modify runtime sources or indexes.

Run from any directory with the repository's Python environment. The output
schemas deliberately differ from runtime schemas. Proposal fields require
review/adaptation before promotion. No renderer or network is called here.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
ASSETS = SCRIPTS.parent / "assets"
sys.path.insert(0, str(SCRIPTS))
import prompt_generator as pg  # noqa: E402


def write_json(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def norm(value):
    value = unicodedata.normalize("NFKD", value).casefold()
    return " ".join(re.sub(r"[^\w\s]", " ", value).split())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


FAMILY_SOURCES = {
    "F01": ["S01", "S02", "S03", "S36", "S37"],
    "F02": ["S04", "S05", "S07"], "F03": ["S05", "S07"],
    "F04": ["S04", "S05", "S29"], "F05": ["S06", "S29"],
    "F06": ["S04"], "F07": ["S07", "S08"], "F08": ["S07", "S08"],
    "F09": ["S04", "S23"], "F10": ["S07", "S09"],
    "F11": ["S07", "S09", "S10", "S16"], "F12": ["S07", "S11"],
    "F13": ["S11", "S12", "S13", "S14", "S15", "S16", "S38"],
    "F14": ["S07"], "F15": ["S36"], "F16": ["S18", "S36"],
    "F17": ["S19"], "F18": ["S03", "S20", "S21", "S22"],
    "F19": ["S23", "S24", "S25", "S26", "S39", "S40", "S41", "S42"],
    "F20": ["S27"], "F21": ["S28", "S29", "S30", "S31"],
    "F22": ["S32"], "F23": ["S06"], "F24": ["S06", "S07"],
    "F25": ["S06", "S21", "S33", "S34"], "F26": ["S35", "S27"],
}
FAMILY_NEXT = {
    "F01": "Separate projected curve, axial rotation, support configuration and drawing-process metadata; reuse the three existing named sculpture profiles.",
    "F02": "Specify foot spacing, load role, knee/ankle configuration and body-camera orientation independently; reuse existing neutral/orientation candidates where exact.",
    "F03": "Specify seat orientation, pelvis support, leg crossing level and arm contact; a chair prop alone does not establish these relations.",
    "F04": "Separate pelvis-to-heel height, knee versus foot support, and hands-and-knees versus palms-and-toes support; proposal narrative is optional metadata.",
    "F05": "Specify which torso surface contacts the support, then add knee/arm variants; separate body-relative from frame-relative diagonal.",
    "F06": "Name the joint/segment and anatomical plane; split opposing movements into distinct values; do not infer pelvic motion from body shape.",
    "F07": "Specify arm chain, hand count, actual target, contact versus no contact and occlusion; extend existing candidates instead of duplicating them.",
    "F08": "Separate hand location, wrist angle, digit geometry and target/contact role; loaded chin support requires an elbow/forearm receiving base.",
    "F09": "Specify left/right owner, knee crossing level, ankle angle, foot contact and split plane independently.",
    "F10": "Separate head roll/yaw/pitch/translation from pupil direction and eye aperture; target changes need explicit property ownership.",
    "F11": "Reuse generic expression candidates; calibrate close eye/lip references before promoting nickname-specific gates; no mood/trait inference.",
    "F12": "Choose finger/arm geometry and palm orientation; collect adult neutral gesture references for heart variants before hard promotion.",
    "F13": "Retain date/community and variant provenance; select a concrete geometry or leave nickname unresolved; OOTD/candid are capture metadata.",
    "F14": "Choose touch/grip/support/occlusion role and actor-target ownership; broad everyday/working/window labels require a specified interaction.",
    "F15": "Select support versus flight phase and prop trajectory role; a single image cannot establish the whole action sequence.",
    "F16": "Separate casting/presentation context, geometric styling and camera framing; no automatic wardrobe, gender, film type or body-shape changes.",
    "F17": "Bind actor_1/actor_2/actor_n, left/right limbs, contact targets and support; specify actor count and avoid inferring personal relationships.",
    "F18": "Use museum-object-specific forms for iconography; duration, drawing practice, genre and nudity are not skeletal pose atoms.",
    "F19": "Choose school, working leg, viewer direction and movement phase; a still form and a transition must keep distinct canonical meanings.",
    "F20": "Choose performance style and one identifiable element/phase; retain ballroom cultural context without identity inference; collect practitioner-reviewed references.",
    "F21": "Expand the eleven source groups into twenty-eight named poses; check school-specific meanings and individual pages, including Cow/Boat/Dancer naming collisions.",
    "F22": "Scope official names to NPC bodybuilding and named variants; rules establish names, while photographs are needed to calibrate exact limb forms.",
    "F23": "Retain as genre/capture/styling metadata; user-requested genre does not itself pick a unique pose or introduce exposure.",
    "F24": "Reuse neutral geometry atoms for identical arrangements; select support and view variants without automatically changing sexual tone or clothing.",
    "F25": "Separate lexical adult-editorial names from specified knees/feet/support and covering targets; obtain exact variant references for M and quadruped nicknames.",
    "F26": "Record choreography/action phase, fan/glove contacts, visible restraint and support state separately; do not infer consent, intent or a universal floor/suspension form.",
}
META_TERMS = {
    "Line of action", "Gesture", "Silhouette readability", "Tension / Relaxation",
    "Model digitals / Polaroids", "Catalogue / E-commerce posing", "Lookbook posing",
    "Editorial posing", "Beauty posing", "Sculptural pose", "Exaggerated pose",
    "Mannequin-like pose", "Hero pose", "Anti-pose / Unposed aesthetic", "OOTD pose",
    "Staged candid / Candid-style pose", "Standing nude", "Seated nude", "Reclining nude",
    "Odalisque", "Gesture drawing", "Long pose", "Mudra", "Voguing", "Hand performance",
    "Catwalk", "Floor performance", "Floorwork", "Glamour", "Pin-up", "Cheesecake",
    "Boudoir", "Lingerie posing", "Swimwear posing", "Fine-art nude", "Gravure / グラビア",
    "Erotic posing", "Burlesque posing", "Fetish posing", "Dominant / Submissive staging",
    "Bondage posing", "Shibari / Kinbaku", "Floor / Suspension", "Strategic covering",
    "Implied-undressing pose", "Everyday action", "Working pose", "Window pose",
}
DEFER = {
    "Smize": "Eye-smile label needs a chosen observable eye/mouth variant; historical usage does not establish a universally distinct eyelid geometry.",
    "Fish gape": "Media descriptions overlap with parted lips and Sparrow Face; keep lexical usage and collect two independent visual variants before assigning exact anatomy.",
    "Cat heart": "Cat-heart variants need a directly inspectable practitioner reference; do not alias to cat-paw, cheek-heart or ordinary hand-heart by similarity.",
    "Cheek heart": "Original caption lead could not be read. Require adult reference images identifying which cheek, hand count, fingers and contact/gap.",
    "Duckwalk": "Require a ballroom practitioner definition and phase reference; a generic low squat alone cannot establish this performance element.",
    "Spins and dips": "Split spin from dip and solo-voguing dip from supported partner dip; choreographic phase and practitioner reference remain missing.",
    "Bump and grind": "Separate pelvis direction, body support and sampled movement phase; genre label alone cannot establish one still form.",
    "Tease and reveal": "Require a named covering object, coverage states and selected moment; never infer new exposure from a broad performance label.",
    "Quarter turn": "Distinguish NPC comparison sequence from photographic three-quarter view and specify the current orientation; not a single universal endpoint.",
    "Runway walk / End-of-runway pose": "Split travel phase from a stopped turn/stance, then select an agency/runway-specific arrangement.",
}
YOGA_CHILDREN = [
    (1, "Tadasana"), (1, "Vrksasana"), (1, "Utkatasana"),
    (2, "Warrior I"), (2, "Warrior II"), (2, "Warrior III"),
    (3, "Trikonasana"), (3, "Utthita Parsvakonasana"),
    (4, "Garudasana"), (4, "Natarajasana"),
    (5, "Sukhasana"), (5, "Padmasana"), (5, "Baddha Konasana"),
    (6, "Balasana"), (6, "Paschimottanasana"),
    (7, "Bhujangasana"), (7, "Ustrasana"), (7, "Dhanurasana"),
    (8, "Setu Bandha Sarvangasana"), (8, "Urdhva Dhanurasana"),
    (9, "Marjaryasana"), (9, "Bitilasana"), (9, "Downward Facing Dog"),
    (10, "Navasana"), (10, "Plank"), (10, "Crow pose"), (10, "Crane pose"),
    (11, "Savasana"),
]
REUSE = {
    "contrapposto": ("body_pose", "contrapposto_full_body", "contrapposto_weight_shift"),
    "serpentinata": ("body_pose", "figura_serpentinata_full_body", "figura_serpentinata_spiral_pose"),
    "tribhanga": ("body_pose", "tribhanga_three_bend_full_body", "tribhanga_three_bend_pose"),
    "s_curve": ("body_pose", "editorial_s_curve_pose", None),
    "c_curve": ("body_pose", "single_arc_c_curve_pose", None),
    "standing_neutral": ("body_pose", "neutral_standing_pose", None),
    "staggered_feet": ("body_pose", "staggered_leg_depth_separation", None),
    "crossed_ankles_standing": ("body_pose", "crossed_ankles_narrow_base", None),
    "edge_sit": ("body_pose", "perched_edge_sit_grounded_support", None),
    "pointed_foot": ("body_pose", "lower_limb_plantarflexed_line", None),
    "elbow_propped": ("body_pose", "propped_elbow_recline_support", None),
    "axial_twist": ("body_orientation", "thorax_pelvis_opposed_azimuth", None),
    "head_torso_opposed": ("body_orientation", "head_shoulder_opposition", None),
    "soft_wrist": ("hand_pose", "relaxed_wrist_offset_line", None),
    "arms_overhead": ("hand_pose", "arms_raised_overhead", None),
    "walking_stride": ("body_pose", "walking_mid_stride_pose", None),
    "phone_hold": ("hand_pose", "holding_phone_visible", None),
    "glasses_adjust": ("hand_pose", "hand_adjusting_sunglasses", None),
    "kickback_bent_leg": ("body_pose", "single_support_backward_flexed_free_leg", None),
    "fingertip_touch": ("contact_point", "fingertip_contact_visible_target_non_support", None),
}
PROFILE_ATOMS = [
    "contrapposto", "serpentinata", "tribhanga", "figure_four", "knee_over_knee",
    "ankle_cross_seated", "reverse_chair", "chair_straddle", "tall_kneel", "heel_sit",
    "half_kneel", "squat_grounded", "toe_squat", "quadruped", "supine", "prone",
    "side_lying", "chin_support", "fingertip_touch", "pointed_foot", "heel_lift",
    "v_sign", "double_v", "finger_heart", "two_hand_heart", "gyaru_v", "squinch",
    "handholding_pair", "head_shoulder_pair", "cradle_carry", "thinker", "abhaya",
    "arabesque", "attitude", "retire", "tendu", "croise", "efface", "demi_pointe",
    "en_pointe", "grand_jete", "warrior_i", "warrior_ii", "warrior_iii",
    "trikonasana", "parsvakonasana", "kakasana", "bakasana", "self_cover_hands",
    "m_leg_variant", "quadruped_arch_variant",
]
ALIAS_CONTEXT_RULES = {
    "single_support": [{"terms":["Weight shift"], "rule":"Broad weight shift can involve seated pelvis or arms; one-leg support is only an optional variant, not an exact definition."}],
    "one_leg_balance": [{"terms":["Flamingo pose"], "rule":"Select a reference specifying free-knee angle and foot location; generic one-leg balance does not prove this nickname."}],
    "heel_lift": [{"terms":["Barbie feet"], "rule":"Bare foot, forefoot support and raised heel are required in the documented variant; a shoe-only heel lift is insufficient. If clothing/footwear is locked, report conflict instead of changing appearance."}],
    "heel_sit": [{"terms":["Bambi pose"], "rule":"Require low pelvis-to-heels and thighs above shins in the documented variant; no implied wardrobe or sexual-tone change."}],
    "v_near_eye": [{"terms":["Peace sign near eye"], "rule":"Bind near-target to the selected eye."}, {"terms":["Chin V pose"], "rule":"Bind near-target to chin; it is not an eye-near placement."}],
    "cheek_touch": [{"terms":["Toothache pose","虫歯ポーズ"], "rule":"Nickname needs a selected cheek/hand variant reference; general cheek touch is not evidence of toothache or a globally standardized pose."}],
    "forehead_touch": [{"terms":["Migraine pose","Headache pose"], "rule":"Choose forehead/hairline/temple target and one/two-hand variant from explicit definition or reference; no medical inference."}],
    "soft_wrist": [{"terms":["T-rex hands"], "rule":"A bent wrist alone does not establish the nickname; choose hand position, elbow configuration and finger variant."}],
    "splayed_fingers": [{"terms":["Jazz hands"], "rule":"Static finger spread can be represented; shaking/performance phase requires separate temporal evidence."}],
    "pout": [{"terms":["Duck face"], "rule":"Choose a lip-pursing/protrusion variant; generic pout does not establish every duck-face convention."}],
    "hair_flip": [{"terms":["Hair twirl"], "rule":"The cited head/hair display movement differs from winding a strand around a finger; specify which meaning is requested."}],
    "passe_phase": [{"terms":["Passé"], "rule":"Keep passing-movement meaning separate; a requester's explicitly defined static retiré usage can override the glossary but cannot prove a complete transition."}],
    "bakasana": [{"terms":["Bakasana","Crane pose"], "rule":"Use the selected straighter-arm teaching convention; other schools' Crow/Crane naming must not be overwritten."}],
    "self_cover_hands": [{"terms":["Hand bra"], "rule":"Bind covering target to explicitly requested chest/body-or-garment region; palms must actually occlude it. Do not infer or introduce nudity."}, {"terms":["Self-covering pose"], "rule":"Broad covering can use hands, forearms or fabric; a hand-only form is an optional variant until object and target are specified."}],
    "m_leg_variant": [{"terms":["M字開脚","M-shaped leg pose"], "rule":"Do not activate exact geometry until seat, knees, feet, support and viewer projection are reference-defined."}],
    "quadruped_arch_variant": [{"terms":["女豹のポーズ"], "rule":"Caption usage is lexical evidence only; choose a directly inspected support/curve/head variant before exact promotion."}],
}


def property_scope(slot, atom):
    if slot == "contact_point":
        return ["relationship"], "contact_geometry"
    if slot == "relational_action":
        return ["action", "pose", "relationship"], "relative_actor_arrangement"
    if slot == "action":
        return ["action", "pose"], "selected_action_phase"
    if slot in {"expression", "gaze_engagement"}:
        return ["expression"], "eye_direction" if slot == "gaze_engagement" else "facial_configuration"
    if slot == "hand_pose":
        return ["pose"], "hand_digit_configuration"
    if slot == "body_orientation":
        return ["pose"], "head_orientation" if atom.startswith(("head_", "chin_")) else "segment_orientation"
    if atom in {"pointed_foot", "flexed_foot", "heel_lift", "demi_pointe", "en_pointe"}:
        return ["pose"], "ankle_and_foot_support"
    return ["pose"], "body_support_and_configuration"


def main():
    source_payload = json.loads((HERE / "sources.json").read_text())
    sources = {s["id"]: s for s in source_payload["sources"]}
    base = json.loads((ASSETS / "photo_prompt_tags.json").read_text())
    data = pg.load_json(ASSETS / "photo_prompt_tags.json")
    registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
    profile_ids = {p["id"] for p in registry["profiles"]}
    existing = {(slot, e["id"]): e for slot, entries in data["slots"].items() for e in entries}
    candidates = []
    for line in (HERE / "candidate-atoms.tsv").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        atom, families, slot, ko, aliases, components, rejects, refs, qualification = line.split("|")
        dims, prop = property_scope(slot, atom)
        owner = "declared_actors" if "F17" in families else "actor_1"
        components = components.split("^")
        alias_values = list(dict.fromkeys(aliases.split(";") + [ko]))
        source_ids = refs.split(",")
        assert all(s in sources for s in source_ids), atom
        target = owner + (".face" if slot in {"expression", "gaze_engagement"} else ".body")
        reuse = REUSE.get(atom)
        if reuse:
            assert reuse[:2] in existing, reuse
            assert not reuse[2] or reuse[2] in profile_ids, reuse
        phase = slot == "action" or "phase" in qualification
        cand = {
            "id": "pv_" + atom, "families": families.split(","), "target_slot": slot,
            "status": "research_proposal", "ko": ko,
            "en": "; ".join(components), "aliases": alias_values,
            "embedding_text_proposed": "; ".join([ko, *alias_values, *components]),
            "concept_units": components,
            "typed_assertions": [
                {"id": f"pv_{atom}_c{i}", "kind": "observable_relation",
                 "owner": owner, "predicate": c, "coordinate_frame": "explicitly_declared_per_assertion",
                 "evidence_basis": "project_operationalization_of_sources"}
                for i, c in enumerate(components, 1)
            ],
            "required_entity_bindings": {
                "owner": owner, "laterality": "actor_left_right_when_material",
                "target": "explicit_body_landmark_prop_partner_or_support_surface",
                "mirror_rule": "reflection_does_not_create_a_new_actor",
            },
            "contact_and_support_policy": {
                "roles": ["no_contact", "near", "touch", "grip", "apparent_support", "occlusion"],
                "selected_role": "derive_from_declared_components_not_from_broad_label",
                "force_measurement": "not_inferable_from_single_photo",
            },
            "affected_dimensions": dims,
            "affected_properties": [{"dimension": d, "target": target, "property": prop} for d in dims],
            "locked_by_default": ["identity", "appearance", "setting", "lighting", "camera", "framing", "sexual_tone"],
            "scope_note": "Property names/targets are research design. Adapt to current property contract and actual core owners before promotion; broad action/pose changes are not automatically authorized.",
            "confusion_boundaries": rejects.split(";"), "source_ids": source_ids,
            "qualification": qualification,
            "existing_reuse_or_extension_target": {"slot": reuse[0], "id": reuse[1], "profile_id": reuse[2]} if reuse else None,
            "observability": {
                "required_regions": components,
                "hidden_region": "UNOBSERVABLE_not_assumed_pass",
                "framing_conflict": "report_conflict_do_not_expand_locked_crop",
                "thumbnail": "check_global_arrangement_if_visible",
                "native_pixels": "check_all_contact_digit_joint_owner_details",
            },
            "temporal_semantics": "one_selected_phase_only_sequence_requires_sequential_evidence" if phase else "single_arrangement",
            "activation": {
                "aliases_are_retrieval_leads_not_global_synonyms": True,
                "optional_only_until_promoted": True, "pack_exposure_does_not_activate_profile": True,
                "exact_label_requires_context_variant_negation_and_property_scope_checks": True,
                "broad_similarity_cannot_set_hard_requirement": True,
            },
            "conditional_alias_constraints": ALIAS_CONTEXT_RULES.get(atom, []),
        }
        candidates.append(cand)
    by_atom = {c["id"][3:]: c for c in candidates}
    assert len(by_atom) == len(candidates)
    assert all(p in by_atom for p in PROFILE_ATOMS)

    decompositions = {}
    for line in (HERE / "row-decompositions.tsv").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        rid, analogies, targets, definition = [part.strip() for part in line.split("|")]
        analogies = ["pv_"+a for a in analogies.split(";") if a]
        target_refs = []
        for target_ref in targets.split(";"):
            if not target_ref:
                continue
            slot, eid = target_ref.split(":")
            assert (slot, eid) in existing, (rid, target_ref)
            target_refs.append({"slot":slot, "id":eid})
        assert all(a[3:] in by_atom for a in analogies), rid
        assert rid not in decompositions, rid
        decompositions[rid] = {"candidate_analogies_not_aliases":analogies,
                               "existing_targets_require_scope_review":target_refs,
                               "operational_definition_proposed":definition,
                               "automatic_joint_adoption":False}

    searchable = []
    for (slot, eid), entry in existing.items():
        if slot not in {"body_pose", "body_orientation", "hand_pose", "contact_point",
                        "gaze_target", "gaze_engagement", "expression", "relational_action",
                        "action", "capture_context", "composition", "body_framing", "subject_framing"}:
            continue
        values = [entry.get("ko", ""), entry.get("en", ""), *entry.get("aliases", []), *entry.get("keywords", [])]
        searchable.append((slot, eid, {norm(v) for v in values if isinstance(v, str)}, norm(" ".join(values))))

    def annotate(fid, row_id, term, section, parent=None):
        alternatives = [norm(t) for t in term.split(" / ")]
        alternatives = [t for t in alternatives if t]
        proposed = []
        for c in candidates:
            if fid in c["families"] and set(alternatives) & {norm(a) for a in c["aliases"]}:
                proposed.append(c["id"])
        exact, lexical = [], []
        for slot, eid, terms, joined in searchable:
            if set(alternatives) & terms:
                exact.append({"slot": slot, "id": eid})
            elif any(" " + t + " " in " " + joined + " " for t in alternatives):
                lexical.append({"slot": slot, "id": eid})
        broad = term in META_TERMS
        deferred = DEFER.get(term)
        if parent is None and fid == "F21":
            disposition = "expand_group_to_named_children"
        elif deferred:
            disposition = "retain_source_defer_exact_geometry"
        elif broad:
            disposition = "context_metadata_or_underspecified_not_unique_pose"
        elif proposed:
            disposition = "review_concrete_candidate_draft"
        elif row_id in decompositions:
            disposition = "review_curated_decomposition"
        elif exact:
            disposition = "existing_label_hint_requires_scope_review"
        else:
            disposition = "needs_variant_or_atomic_decomposition"
        return {
            "id": row_id, "family_id": fid, "source_section": section, "source_term": term,
            "parent_row_id": parent,
            "source_role": "untrusted_seed_not_definition_authority",
            "slash_policy": "alternative_names_or_opposing_values_require_semantic_review_not_synonym_assumption",
            "current_exact_label_hits": exact, "current_phrase_hints": lexical[:12],
            "current_phrase_hint_count": len(lexical),
            "current_evidence_limit": "lexical_presence_only_not_selection_or_pixel_coverage",
            "proposed_candidate_ids": proposed,
            "curated_decomposition": decompositions.get(row_id),
            "disposition": disposition,
            "family_research_source_ids": FAMILY_SOURCES[fid],
            "source_scope": "family_background_only_does_not_verify_each_term",
            "next_action": deferred or decompositions.get(row_id, {}).get("operational_definition_proposed") or FAMILY_NEXT[fid],
        }

    rows, sections = [], {}
    for line in (HERE / "seed-terms.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        fid, section, terms = line.split("|")
        sections[fid] = section
        for i, term in enumerate(terms.split(";"), 1):
            rows.append(annotate(fid, f"{fid}_{i:02}", term, section))
    assert len(rows) == 398, len(rows)
    children = [annotate("F21", f"Y{i:02}", term, sections["F21"], f"F21_{parent:02}")
                for i, (parent, term) in enumerate(YOGA_CHILDREN, 1)]
    assert len(children) == 28
    assert set(decompositions).issubset({r["id"] for r in rows})
    write_json("keyword-catalog.json", {
        "schema_version": "pose-keyword-research-catalog/v1", "date": "2026-10-02",
        "conversation_id": "6abf0e48-7010-83ee-8bbf-7764bcfe2150", "title": "포즈 용어 조사",
        "extraction": "read_thread returned a bounded 20000-character preview; browser visible DOM provided the remaining tables. English search labels were transcribed and normalized, not a byte-exact conversation backup.",
        "counts": {"seed_table_rows": len(rows), "families": len(sections), "yoga_named_children": len(children), "annotation_records": len(rows)+len(children)},
        "count_limit": "Rows include duplicates, compound alternatives and metadata. This is not a unique-formal-term count or evidence of runtime semantic coverage.",
        "excluded_from_keyword_count": {"classification_axes_in_section_18": 14, "combined_examples": 6, "intro_classification_rows": 3},
        "rows": rows, "yoga_children": children,
    })
    write_json("candidate-data.proposed.json", {
        "schema_version": "pose-candidate-research-proposal/v1", "not_runtime_drop_in": True,
        "source_basis": "candidate-atoms.tsv + sources.json", "count": len(candidates),
        "weight_policy": "Tune against sibling candidates after promotion; no research weight implies live rank or an authorized core change.",
        "candidates": candidates,
    })

    profiles = []
    cases = []
    for atom in PROFILE_ATOMS:
        c = by_atom[atom]
        cid = c["id"]
        reuse = c["existing_reuse_or_extension_target"]
        existing_profile = reuse["profile_id"] if reuse else None
        pid = existing_profile or "pv_profile_" + atom
        fields = [f"component_{i}" for i in range(1, len(c["concept_units"])+1)]
        gates = [{"id": f"{pid}_{f}", "required_field": f, "rule": unit,
                  "review_resolution": "native_pixels", "hidden_or_occluded": "UNOBSERVABLE",
                  "partial": "FAIL", "basis": "proposed_project_gate_not_source_standard"}
                 for f, unit in zip(fields, c["concept_units"])]
        profiles.append({
            "id": pid, "candidate_id": cid,
            "operation": "review_existing_profile_do_not_duplicate" if existing_profile else "propose_new_profile",
            "qualification": c["qualification"], "source_ids": c["source_ids"],
            "activation": {"request_only": True, "exact_contextual_terms_proposed": c["aliases"],
                           "negation_blocks": True, "user_definition_precedes": True,
                           "semantic_similarity_optional_only": True, "requires_resolved_variant": True,
                           "pack_selection_alone_never_activates": True},
            "conditional_alias_constraints": c["conditional_alias_constraints"],
            "runtime_expression_proposed": c["en"],
            "required_evidence_fields": fields, "render_gates_proposed": gates,
            "gate_aggregation": "all_required_PASS_and_observable; partial_is_fail; UNOBSERVABLE_is_not_success",
            "reject_substitutes": c["confusion_boundaries"],
            "locked_crop_conflict": "declare_unverifiable_or_request_explicit_reframing_choice_before_future_render",
        })
        cases.extend([
            {"id": pid+"_definition_positive", "profile_id": pid, "layer": "definition_fixture", "input_components": c["concept_units"], "expected": "all_components_required", "is_generated_image": False},
            {"id": pid+"_near_miss", "profile_id": pid, "layer": "confusion_fixture", "input_substitute": c["confusion_boundaries"][0], "expected": "reject_as_exact_named_pose", "is_generated_image": False},
            {"id": pid+"_partial", "profile_id": pid, "layer": "gate_aggregation_fixture", "missing_required_field": fields[-1], "expected": "FAIL_not_success", "is_generated_image": False},
            {"id": pid+"_hidden", "profile_id": pid, "layer": "observability_fixture", "hidden_required_field": fields[0], "expected": "UNOBSERVABLE_not_success", "is_generated_image": False},
        ])
    write_json("visual-profiles.proposed.json", {"schema_version": "pose-visual-profile-research-proposal/v1", "not_runtime_drop_in": True, "profiles": profiles})
    extra = [
        ("arabesque_motif", "arabesque wall ornament behind a neutral seated actor", "do_not_activate_ballet_arabesque"),
        ("v_neck", "a V-neck top, hands relaxed at the sides", "do_not_activate_V_sign"),
        ("s_hair", "S-curve hair waves, neutral body posture", "do_not_activate_body_S_curve"),
        ("three_quarter_crop", "three-quarter-length portrait with front-facing torso", "do_not_force_three_quarter_body_turn"),
        ("no_bambi", "무릎을 꿇되 밤비 포즈는 제외하고 골반을 높인다", "tall_kneel_only_no_Bambi_profile"),
        ("no_finger_heart", "손가락 하트 없이 양손 브이", "double_V_only"),
        ("name_override", "Here Bambi means the animal printed on a bag; actor stands neutrally", "user_definition_precedes_no_kneeling"),
        ("locked_close_crop", "contrapposto support-leg study, locked head-and-shoulders crop", "report_support_unverifiable_do_not_silently_expand_crop"),
        ("touch_vs_support", "fingertip near cheek with a gap", "near_not_touch_or_chin_support"),
        ("reflection_owner", "one adult taking a mirror selfie", "one_actor_plus_reflection_not_two_actors"),
        ("partner_owner", "actor_1 left hand holds actor_2 right hand", "resolve_actor_and_laterality_do_not_self_interlace"),
        ("styling_lock", "fully clothed heel-sitting portrait called Bambi", "pose_change_only_preserve_clothing_and_sexual_tone"),
        ("pointed_vs_pointe", "seated actor with one pointed airborne foot", "plantarflexion_without_en_pointe_support"),
        ("front_vs_side", "front split", "do_not_replace_with_side_split"),
        ("cow_name_collision", "Bitilasana tabletop cow pose", "do_not_retrieve_Gomukhasana_seated_cow_face_as_synonym"),
        ("dancer_name_collision", "standing Natarajasana with hand holding rear foot", "do_not_retrieve_lying_twist"),
        ("pose_vs_phase", "static retiré photograph", "do_not_assert_entire_passe_transition"),
        ("genre_no_geometry", "boudoir, no pose specified", "offer_optional_pose_variants_do_not_hard_activate_heel_sit_or_exposure"),
        ("ordinary_heart", "heart pattern printed on a shirt", "do_not_activate_hand_heart"),
        ("metadata_polaroid", "model digitals on a phone camera", "do_not_force_instant_film_capture_or_rewrite_camera"),
    ]
    cases.extend({"id": "scope_"+cid, "layer": "activation_and_scope_fixture", "input": text, "expected": expectation, "is_generated_image": False} for cid,text,expectation in extra)
    (HERE / "evaluation-cases.proposed.jsonl").write_text("".join(json.dumps(c,ensure_ascii=False)+"\n" for c in cases))

    slots = ["body_pose", "body_orientation", "hand_pose", "contact_point", "gaze_target", "gaze_engagement", "expression", "relational_action", "action"]
    source_paths = {ASSETS/"photo_prompt_tags.json", ASSETS/"photo_prompt_visual_obligations.json",
                    SCRIPTS/"prompt_generator.py", SCRIPTS/"photo_candidate_semantics.py", SCRIPTS/"photo_contracts.py",
                    SCRIPTS/"photo_embodiment.py", ROOT/"tests/test_photo_pose_visual_semantics.py"}
    for name in (*pg.RESEARCH_EXTENSION_FILENAMES, *pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES):
        if (ASSETS/name).exists(): source_paths.add(ASSETS/name)
    loaded_hashes = {str(p.relative_to(ROOT)):digest(p) for p in sorted(source_paths)}
    inventory = [{"slot":s, "id":e["id"], "ko":e.get("ko"), "en":e.get("en"), "affected_dimensions":e.get("affected_dimensions"), "affected_properties":e.get("affected_properties")} for s in slots[:-1] for e in data["slots"].get(s, [])]
    watch_terms = ["arabesque", "bambi", "barbie feet", "finger heart", "figure-four", "tall kneeling", "supine", "prone", "gyaru", "squinch", "abhaya", "warrior", "passé"]
    watch = {}
    for term in watch_terms:
        watch[term] = [{"slot":s,"id":e["id"]} for s in slots for e in data["slots"].get(s,[]) if term in json.dumps({k:e.get(k) for k in ("ko","en","aliases","keywords","embedding_text")}, ensure_ascii=False).casefold()]
    write_json("current-data-audit.json", {
        "schema_version": "pose-source-audit/v1", "date": "2026-10-02",
        "git_head": subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "preexisting_untracked_preserved": ["docs/analysis/2026-10-02-visual-semantics-data-audit/"],
        "base_slot_counts": {s:len(base["slots"].get(s,[])) for s in slots},
        "merged_slot_counts": {s:len(data["slots"].get(s,[])) for s in slots},
        "base_profile_count": len(json.loads((ASSETS/"photo_prompt_visual_obligations.json").read_text())["profiles"]),
        "merged_profile_count": len(registry["profiles"]),
        "confirmed_named_sculpture_profile_ids": ["contrapposto_weight_shift","figura_serpentinata_spiral_pose","tribhanga_three_bend_pose"],
        "slot_dimensions": {s:data["candidate_semantic_policy"]["slot_dimensions"].get(s) for s in slots},
        "source_sha256": loaded_hashes, "watch_term_lexical_hits_in_audited_slots": watch,
        "lexical_limit": "No English-name hit does not prove absent geometry. This audit is authored-source inspection, not retrieval, rank, pack exposure, render or user qualification.",
        "merged_pose_related_inventory": inventory,
    })
    validation = {
        "schema_version": "pose-research-static-verification/v1", "date": "2026-10-02",
        "seed_row_count": len(rows), "yoga_child_count": len(children), "family_count": len(sections),
        "candidate_count": len(candidates), "profile_proposal_count": len(profiles),
        "curated_row_decomposition_count": len(decompositions),
        "existing_profiles_to_reuse": sum(p["operation"].startswith("review") for p in profiles),
        "new_profile_proposals": sum(p["operation"].startswith("propose") for p in profiles),
        "case_count": len(cases), "source_record_count": len(sources),
        "candidate_qualifications": dict(Counter(c["qualification"] for c in candidates)),
        "catalog_dispositions": dict(Counter(r["disposition"] for r in rows+children)),
        "checks": {"398_seed_rows_annotated":True,"28_yoga_children_annotated":True,"unique_candidate_ids":True,"candidate_source_refs_exist":True,"reuse_targets_exist":True,"profile_candidate_refs_exist":True,"proposal_fields_required":True},
        "production_assets_after_build_equal_inspected_hashes": all(digest(ROOT/p)==h for p,h in loaded_hashes.items()),
        "evidence_boundary": {"runtime_candidate_pack_generated":False,"runtime_indexes_changed":False,"runtime_assets_changed":False,"images_generated":False,"source_reference_pixels_qualified":False,"native_generated_pixels_reviewed":False,"user_acceptance_claimed":False},
    }
    write_json("verification.json", validation)
    print(json.dumps({k:validation[k] for k in ("seed_row_count","yoga_child_count","family_count","candidate_count","profile_proposal_count","existing_profiles_to_reuse","new_profile_proposals","case_count","source_record_count","catalog_dispositions")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
