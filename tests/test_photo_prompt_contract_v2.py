from __future__ import annotations

import copy
from contextlib import redirect_stdout
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
WRAPPER_PATH = SCRIPT_DIR / "generate_photo_prompt.py"
EVAL_PATH = SCRIPT_DIR / "eval_semantic.py"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
GENERALIZATION_PATH = SKILL_DIR / "assets" / "generalization_cases.jsonl"
HOLDOUT_PATH = SKILL_DIR / "assets" / "generalization_holdout_cases.jsonl"
DOMAIN_HOLDOUT_V2_PATH = SKILL_DIR / "assets" / "generalization_domain_holdout_v2.jsonl"
RETRIEVAL_HOLDOUT_V3_PATH = SKILL_DIR / "assets" / "semantic_retrieval_holdout_v3.jsonl"
RETRIEVAL_HOLDOUT_V4_PATH = SKILL_DIR / "assets" / "semantic_retrieval_holdout_v4.jsonl"
SUBCULTURE_RETRIEVAL_HOLDOUT_V1_PATH = SKILL_DIR / "assets" / "semantic_retrieval_holdout_subculture_v1.jsonl"
WORLDBUILDING_RETRIEVAL_HOLDOUT_V1_PATH = SKILL_DIR / "assets" / "semantic_retrieval_holdout_worldbuilding_v1.jsonl"
RESEARCH_EVIDENCE_PATH = SKILL_DIR / "assets" / "research_evidence.jsonl"
RESEARCH_EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_research_extension.json"
SUBCULTURE_EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_subculture_extension.json"
WORLDBUILDING_EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_worldbuilding_extension.json"
QUALITY_LAYERS_PATH = SKILL_DIR / "assets" / "photo_prompt_quality_layers.json"
DOMAIN_VISUAL_REVIEW_PLAN_PATH = SKILL_DIR / "assets" / "visual_review_domain_extension_plan.json"
DOMAIN_VISUAL_REVIEW_RESULTS_PATH = SKILL_DIR / "assets" / "visual_review_domain_extension_results.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_composed_prompt  # noqa: E402
import eval_semantic  # noqa: E402
import generate_photo_prompt  # noqa: E402
import prompt_generator  # noqa: E402


class PhotoPromptContractV2Tests(unittest.TestCase):
    def run_wrapper(self, *args: str):
        completed = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_safety_contract_defaults_to_pass_and_evaluates_only_on_request(self):
        base_args = (
            "--concept",
            "유나 바니걸",
            "--selection-mode",
            "rule",
            "--seed",
            "11",
            "--emit-candidate-pack",
        )
        default_pack = self.run_wrapper(*base_args)[0]
        self.assertEqual(
            default_pack["safety"],
            {
                "mode": "automatic",
                "evaluation_requested": False,
                "status": "pass",
                "requires_user_approval": False,
                "items": [],
            },
        )

        evaluated_pack = self.run_wrapper(*base_args, "--safety-evaluation")[0]
        self.assertEqual(evaluated_pack["safety"]["mode"], "explicit_evaluation")
        self.assertTrue(evaluated_pack["safety"]["evaluation_requested"])
        self.assertEqual(evaluated_pack["safety"]["status"], "pass")
        self.assertFalse(evaluated_pack["safety"]["requires_user_approval"])
        self.assertTrue(evaluated_pack["safety"]["items"])
        self.assertTrue(all(item["status"] == "pass" for item in evaluated_pack["safety"]["items"]))

    def test_candidate_pack_integrity_and_assertions_fail_closed(self):
        pack = self.run_wrapper(
            "--preset",
            "product_hero_on_riser",
            "--selection-mode",
            "rule",
            "--seed",
            "17",
            "--emit-candidate-pack",
        )[0]
        chosen_id = next(
            candidate["id"]
            for candidate in pack["presets"]
            if candidate.get("selected_by_sampler")
        )
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": "A restrained product still life with believable contact shadow, no text or watermark.",
            "negative_en": pack.get("negative_en"),
            "chosen_candidate_ids": [chosen_id],
            "composer": "agent",
        }
        passed = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(passed["status"], "pass", passed)

        applicability_pack = copy.deepcopy(pack)
        chosen_slot = next(
            candidate
            for slot_payload in applicability_pack["slots"].values()
            for candidate in slot_payload["candidates"]
            if candidate.get("selected_by_sampler")
        )
        chosen_slot["applicability"] = {
            "status": "blocked",
            "source": "test",
            "reason": "synthetic contract violation",
        }
        applicability_pack["pack_id"] = audit_composed_prompt.computed_pack_id(applicability_pack)
        applicability_composed = {
            **composed,
            "pack_id": applicability_pack["pack_id"],
            "chosen_candidate_ids": [chosen_slot["id"]],
        }
        applicability_result = audit_composed_prompt.audit_composed_prompt(
            applicability_pack, applicability_composed
        )
        self.assertIn(
            "candidate_applicability",
            {failure["check"] for failure in applicability_result["failures"]},
        )

        tampered = copy.deepcopy(pack)
        tampered["provenance"]["seed"] = 999
        tampered_result = audit_composed_prompt.audit_composed_prompt(tampered, composed)
        self.assertIn("pack_integrity", {failure["check"] for failure in tampered_result["failures"]})

        spoofed = {**composed, "coverage_assertions": {"not-a-mandatory-intent": "product"}}
        spoofed_result = audit_composed_prompt.audit_composed_prompt(pack, spoofed)
        self.assertIn("coverage_assertions", {failure["check"] for failure in spoofed_result["failures"]})

        with self.assertRaisesRegex(ValueError, "exactly one pack"):
            audit_composed_prompt.first_pack([])
        with self.assertRaisesRegex(ValueError, "exactly one pack"):
            audit_composed_prompt.first_pack([pack, pack])

    def test_korean_no_people_intent_never_inverts_to_a_human_subject(self):
        pack = self.run_wrapper(
            "--preset",
            "environmental_portrait_composition",
            "--selection-mode",
            "rule",
            "--seed",
            "23",
            "--additional-requirement",
            "사람 없는 quiet brutalist reading room, no people",
            "--emit-candidate-pack",
        )[0]
        mandatory = {item["text"] for item in pack["mandatory_intents"]}
        self.assertTrue({"사람 없는", "no people"} <= mandatory)
        selected_subject = next(
            candidate
            for candidate in pack["slots"]["subject"]["candidates"]
            if candidate.get("selected_by_sampler")
        )
        self.assertNotIn("human", selected_subject.get("kind", []))
        active_axes = {axis["id"] for axis in pack["photographic_integration"]["active_axes"]}
        self.assertNotIn("person_presence", active_axes)

        person_only_slots = {
            "appearance_type",
            "body_pose",
            "costume_style",
            "hair_style",
            "hand_pose",
            "makeup_style",
            "wardrobe_style",
        }
        for slot, slot_payload in pack["slots"].items():
            self.assertNotIn(slot, person_only_slots)
            for candidate in slot_payload["candidates"]:
                self.assertEqual(
                    candidate["applicability"],
                    {
                        "status": "eligible",
                        "source": "sampler_eligible_pool",
                        "reason": None,
                    },
                )
                self.assertNotIn(
                    "human",
                    {str(item).lower() for item in [*candidate.get("kind", []), *candidate.get("tags", [])]},
                )

    def test_role_scene_variants_rotate_while_identity_core_stays_fixed(self):
        variant_ids = set()
        for seed in range(1, 13):
            _args, explanations = generate_photo_prompt.resolve_concepts(
                ["--selection-mode", "rule", "--seed", str(seed)],
                ["회사원"],
                concept_mode="soft",
            )
            explanation = explanations[0]
            variant_ids.add(explanation["selected_scene_variants"][0]["id"])
            forced = explanation["combined_forced_slots"]
            self.assertEqual(forced["subject"], ["office_worker"])
            self.assertEqual(forced["appearance_type"], ["corporate_professional"])
            self.assertEqual(forced["wardrobe_style"], ["clean_blazer_trousers"])
            self.assertNotIn("person_origin", forced)
        self.assertGreaterEqual(len(variant_ids), 2)

    def test_creative_discovery_pilot_roles_keep_identity_and_reach_atomic_scenes(self):
        expected_identity = {
            "사진작가": {
                "subject": ["photographer_role_model"],
                "costume_style": ["photographer_utility_vest_costume"],
            },
            "바리스타": {"subject": ["young_barista"]},
            "도예가": {"subject": ["ceramic_artist"]},
            "농부": {"subject": ["farmer_at_dawn"]},
            "기자": {"subject": ["field_reporter"]},
            "우주비행사": {
                "subject": ["astronaut_role_model"],
                "costume_style": ["astronaut_flight_suit_costume"],
            },
            "큐레이터": {
                "subject": ["museum_curator_role_model"],
                "costume_style": ["curator_suit_gloves_costume"],
            },
            "정비사": {"subject": ["garage_mechanic"]},
            "도서관 사서": {"subject": ["librarian_at_desk"]},
            "플로리스트": {
                "subject": ["florist_arranging_bouquet"],
                "wardrobe_style": ["knit_cardigan_jeans"],
            },
        }
        recipes = generate_photo_prompt.load_concept_recipes()

        for role, identity in expected_identity.items():
            with self.subTest(role=role):
                recipe = recipes["roles"][role]
                variants = recipe["scene_variants"]
                expected_variant_ids = {variant["id"] for variant in variants}
                self.assertGreaterEqual(len(expected_variant_ids), 2)
                self.assertTrue(set(identity).isdisjoint({slot for variant in variants for slot in variant["set"]}))

                observed_variant_ids = set()
                for seed in range(1, 65):
                    _args, explanations = generate_photo_prompt.resolve_concepts(
                        ["--selection-mode", "rule", "--seed", str(seed)],
                        [role],
                        concept_mode="soft",
                    )
                    explanation = explanations[0]
                    selected_scene = explanation["selected_scene_variants"][0]
                    observed_variant_ids.add(selected_scene["id"])
                    forced = explanation["combined_forced_slots"]
                    for slot, ids in identity.items():
                        self.assertEqual(forced[slot], ids)

                    atomic_group = f"role_scene:{selected_scene['id']}"
                    anchors = {
                        anchor["slot"]: anchor
                        for anchor in explanation["soft_anchor_spec"]["anchors"]
                    }
                    for slot, raw_ids in selected_scene["set"].items():
                        ids = [raw_ids] if isinstance(raw_ids, str) else raw_ids
                        self.assertEqual(anchors[slot]["pool"], ids)
                        self.assertEqual(anchors[slot]["variant_group"], atomic_group)
                        self.assertEqual(anchors[slot]["variant_strategy"], "atomic_scene")

                self.assertEqual(observed_variant_ids, expected_variant_ids)

    def test_high_creativity_marks_existing_contrasts_without_reordering_candidates(self):
        base_args = (
            "--concept",
            "도예가",
            "--selection-mode",
            "rule",
            "--seed",
            "42",
            "--emit-candidate-pack",
        )
        base_pack = self.run_wrapper(*base_args)[0]
        low_pack = self.run_wrapper(*base_args, "--creativity", "0.74")[0]
        creative_pack = self.run_wrapper(*base_args, "--creativity", "0.85")[0]
        repeated_pack = self.run_wrapper(*base_args, "--creativity", "0.85")[0]

        self.assertNotIn("creative_exploration", base_pack)
        self.assertNotIn("creative_exploration", low_pack)
        exploration = creative_pack["creative_exploration"]
        self.assertEqual(exploration, repeated_pack["creative_exploration"])
        self.assertEqual(exploration["source"], "exposed_sampler_eligible_pool")
        self.assertGreater(exploration["contrast_candidate_count"], 0)

        self.assertEqual(base_pack["presets"], creative_pack["presets"])
        self.assertEqual(set(base_pack["slots"]), set(creative_pack["slots"]))
        for slot in base_pack["slots"]:
            base_slot = base_pack["slots"][slot]
            creative_slot = creative_pack["slots"][slot]
            self.assertEqual(base_slot["selected"], creative_slot["selected"])
            self.assertEqual(
                [candidate["id"] for candidate in base_slot["candidates"]],
                [candidate["id"] for candidate in creative_slot["candidates"]],
            )

        selected_ids = {
            slot_payload["selected"]
            for slot_payload in creative_pack["slots"].values()
            if slot_payload.get("selected")
        }
        for contrast in exploration["contrast_candidates"]:
            slot_payload = creative_pack["slots"][contrast["slot"]]
            candidates = {candidate["id"]: candidate for candidate in slot_payload["candidates"]}
            candidate = candidates[contrast["candidate_id"]]
            self.assertEqual(contrast["replaces_candidate_id"], slot_payload["selected"])
            self.assertFalse(candidate["selected_by_sampler"])
            self.assertEqual(candidate["applicability"]["status"], "eligible")
            self.assertEqual(candidate["applicability"]["source"], "sampler_eligible_pool")
            self.assertGreaterEqual(
                contrast["feature_distance"],
                exploration["minimum_feature_distance"],
            )
            self.assertFalse(
                set(candidate["conflicts_with"]) & (selected_ids - {slot_payload["selected"]})
            )

    def test_atomic_scene_candidate_pools_and_audit_are_fail_closed(self):
        pack = self.run_wrapper(
            "--concept",
            "회사원",
            "--selection-mode",
            "rule",
            "--seed",
            "9",
            "--emit-candidate-pack",
        )[0]
        groups = pack["scene_contract"]["groups"]
        self.assertTrue(groups)
        for group in groups:
            self.assertEqual(group["strategy"], "atomic_scene")
            for slot, slot_contract in group["slots"].items():
                allowed = set(slot_contract["allowed_entry_ids"])
                candidates = {
                    candidate["entry_id"]
                    for candidate in pack["slots"].get(slot, {}).get("candidates", [])
                }
                self.assertTrue(candidates <= allowed)

        tampered = copy.deepcopy(pack)
        target_group = tampered["scene_contract"]["groups"][0]
        target_slot, target_contract = next(
            (slot, contract)
            for slot, contract in target_group["slots"].items()
            if contract.get("selected_entry_id")
        )
        target_id = target_contract["selected_entry_id"]
        target_contract["allowed_entry_ids"] = [
            entry_id for entry_id in target_contract["allowed_entry_ids"] if entry_id != target_id
        ]
        tampered["pack_id"] = audit_composed_prompt.computed_pack_id(tampered)
        prompt_terms = " ".join(str(item.get("text") or "") for item in tampered["mandatory_intents"])
        composed = {
            "pack_id": tampered["pack_id"],
            "prompt_en": prompt_terms,
            "negative_en": tampered.get("negative_en"),
            "chosen_candidate_ids": [f"slot:{target_slot}:{target_id}"],
            "composer": "agent",
        }
        result = audit_composed_prompt.audit_composed_prompt(tampered, composed)
        self.assertIn("atomic_scene_contract", {failure["check"] for failure in result["failures"]})

    def test_standalone_role_specific_mixin_does_not_borrow_an_unrelated_bundle(self):
        recipes = generate_photo_prompt.load_concept_recipes()
        mixin = recipes["mixins"]["암살자"]
        selected = generate_photo_prompt.select_bundle_for_mixin(
            "암살자", "암살자", mixin, ["--seed", "1"], None
        )
        self.assertIsNone(selected)

    def test_typed_routing_and_theme_guards_generalize_beyond_portraits(self):
        architecture = self.run_wrapper(
            "--preset",
            "infrastructure_inspection_record",
            "--selection-mode",
            "rule",
            "--seed",
            "29",
            "--additional-requirement",
            "bridge architecture and flood-control infrastructure as the primary subject",
            "--emit-candidate-pack",
        )[0]
        self.assertIn("environment", architecture["coverage"]["intent_constraints"]["subject_categories"])
        selected_subject = next(
            candidate
            for candidate in architecture["slots"]["subject"]["candidates"]
            if candidate.get("selected_by_sampler")
        )
        self.assertIn("environment", selected_subject["kind"])

        food = self.run_wrapper(
            "--preset",
            "community_kitchen_documentary",
            "--selection-mode",
            "rule",
            "--seed",
            "31",
            "--additional-requirement",
            "restrained observational food process",
            "--emit-candidate-pack",
        )[0]
        exposed_ids = {
            candidate["entry_id"]
            for slot_payload in food["slots"].values()
            for candidate in slot_payload["candidates"]
        }
        self.assertTrue(
            {
                "kinetic_spell_trail_motion",
                "visible_ball_joint_seam",
                "charging_indicator_glow",
                "thermal_lowfi_pov",
                "exposed_joint_focus",
                "boot_flicker_motion",
                "feather_skin_follicle_blend",
                "surface_caustic_light",
            }.isdisjoint(exposed_ids)
        )

    def test_visual_review_contract_rejects_empty_or_unprovenanced_payloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps({"cases": []}), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)["visual_review"]
        self.assertFalse(summary["passed"])
        self.assertGreaterEqual(summary["contract_failure_count"], 3)
        self.assertEqual(summary["failed_case_count"], 0)

    def test_visual_review_contract_rejects_invalid_enums_and_declared_conflicts(self):
        case = {
            "case": "synthetic",
            "prompt_id": "prompt-1",
            "image_id": "image-1",
            "dual_read": "maybe",
            "archetype_first_read": "pass",
            "body_drift": "none",
            "preset_conflict": "present",
            "role_anchor": "pass",
            "mixin_anchor": "pass",
            "body_coverage_guard": "pass",
            "render_modality": "pass",
            "framing_constraint": "pass",
            "body_emphasis_survived": "yes",
        }
        payload = {
            "schema_version": "photo-visual-review/v1",
            "provenance": {
                "generator_version": "test",
                "tags_hash": "hash",
                "reviewer": "reviewer",
                "reviewed_at": "2026-08-05T00:00:00Z",
            },
            "cases": [case],
        }
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps(payload), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)["visual_review"]
        self.assertFalse(summary["passed"])
        self.assertIn("case_field_enum", {failure["check"] for failure in summary["contract_failures"]})
        self.assertEqual(
            set(summary["failed_cases"][0]["failures"]),
            {"preset_conflict", "body_emphasis_survived"},
        )

    def test_domain_visual_review_plan_links_completed_review_but_is_not_acceptance_evidence(self):
        plan = json.loads(DOMAIN_VISUAL_REVIEW_PLAN_PATH.read_text(encoding="utf-8"))
        self.assertEqual(plan["schema_version"], "photo-domain-visual-review-plan/v1")
        self.assertEqual(plan["status"], "completed")
        self.assertFalse(plan["acceptance_artifact"])
        self.assertEqual(plan["review_artifact"], DOMAIN_VISUAL_REVIEW_RESULTS_PATH.name)
        self.assertEqual(len(plan["cases"]), 12)
        self.assertEqual(len({case["preset"] for case in plan["cases"]}), 12)

        summary = eval_semantic.summarize_visual_review(DOMAIN_VISUAL_REVIEW_RESULTS_PATH)["visual_review"]
        self.assertTrue(summary["passed"])
        self.assertEqual(summary["case_count"], 12)
        self.assertEqual(summary["failed_case_count"], 0)
        self.assertEqual(summary["contract_failure_count"], 0)
        self.assertEqual(summary["review_focus_result_count"], 36)
        self.assertEqual(summary["failed_review_focus_result_count"], 0)
        for field in (
            "body_drift",
            "role_anchor",
            "mixin_anchor",
            "body_coverage_guard",
            "body_emphasis_survived",
        ):
            self.assertEqual(summary["field_summaries"][field]["counts"]["not_applicable"], 12)

    def test_visual_review_contract_fails_closed_on_declared_review_focus_failure(self):
        payload = json.loads(DOMAIN_VISUAL_REVIEW_RESULTS_PATH.read_text(encoding="utf-8"))
        payload["cases"] = [dict(payload["cases"][0])]
        payload["cases"][0]["review_focus_results"] = [
            {
                "focus": "required visual evidence",
                "outcome": "fail",
                "evidence": "The required evidence is absent.",
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps(payload), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)["visual_review"]

        self.assertFalse(summary["passed"])
        self.assertEqual(summary["failed_case_count"], 1)
        self.assertEqual(summary["failed_review_focus_result_count"], 1)
        self.assertIn("review_focus", summary["failed_cases"][0]["failures"])

    def test_visual_review_contract_requires_reason_for_not_applicable_fields(self):
        payload = json.loads(DOMAIN_VISUAL_REVIEW_RESULTS_PATH.read_text(encoding="utf-8"))
        payload["cases"] = [dict(payload["cases"][0])]
        payload["cases"][0].pop("not_applicable_reason")
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps(payload), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)["visual_review"]

        self.assertFalse(summary["passed"])
        self.assertIn(
            "not_applicable_reason",
            {failure["check"] for failure in summary["contract_failures"]},
        )

    def test_expanded_dictionary_has_operational_domain_packs_facets_and_primary_guards(self):
        tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_LAYERS_PATH.read_text(encoding="utf-8"))
        preset_ids = {preset["id"] for preset in tags["presets"]}
        self.assertGreaterEqual(len(preset_ids), 555)
        self.assertTrue(
            {
                "wetland_behavior_documentary",
                "forest_floor_macro_ecology",
                "industrial_process_documentary",
                "infrastructure_inspection_record",
                "farm_to_table_process",
                "community_kitchen_documentary",
                "laboratory_measurement_record",
                "field_sensor_survey",
                "warehouse_flow_documentary",
                "transit_maintenance_record",
                "coastal_resilience_monitoring",
                "urban_heat_air_quality_record",
                "camera_trap_species_monitoring",
                "coastal_benthic_quadrat_survey",
                "orchard_harvest_grading_record",
                "fermentation_batch_monitoring",
                "electronics_repair_diagnostic_record",
                "materials_recovery_sorting_record",
            }
            <= preset_ids
        )
        subject_ids = {entry["id"] for entry in tags["slots"]["subject"]}
        self.assertTrue(
            {
                "pollinator_moth_night",
                "cleanroom_wafer_robot",
                "community_soup_pot",
                "microscope_sample_stage",
                "field_air_quality_station",
                "parcel_sorting_conveyor",
                "rail_switch_actuator",
                "coastal_erosion_marker_array",
                "urban_heat_sensor_station",
                "camera_trap_wildlife_passage",
                "intertidal_quadrat_biota",
                "orchard_fruit_grading_line",
                "fermentation_vessel_batch",
                "open_electronics_repair_board",
                "mixed_material_sorting_stream",
            }
            <= subject_ids
        )
        coastal_subject = next(
            entry for entry in tags["slots"]["subject"] if entry["id"] == "coastal_erosion_marker_array"
        )
        self.assertEqual(
            prompt_generator.subject_category({"subject": coastal_subject}, tags),
            "environment",
        )
        guarded_ids = {
            entry["id"]
            for entries in tags["slots"].values()
            for entry in entries
            if entry.get("requires_primary_any_tags")
        }
        self.assertTrue(
            {
                "kinetic_spell_trail_motion",
                "snowflake_pinpoint_glow",
                "thermal_lowfi_pov",
                "aligning_microscope_sample",
                "collecting_air_sample",
                "routing_parcels_conveyor",
                "inspecting_rail_switch",
                "measuring_shoreline_retreat",
                "logging_surface_temperature",
                "microscopy_measurement_capture",
                "thermal_field_survey_capture",
                "fixed_interval_monitoring_capture",
            }
            <= guarded_ids
        )
        self.assertTrue(
            {
                "relation_type",
                "event_phase",
                "process_stage",
                "capture_modality",
                "weather_effect",
                "movement_type",
            }
            <= set(tags["facet_vocab"])
        )
        operational_domains = {
            "science_inspection",
            "mobility_logistics",
            "climate_adaptation",
            "biodiversity_monitoring",
            "agriculture_food_systems",
            "circular_materials",
        }
        self.assertTrue(operational_domains <= set(quality["quality_profiles"]))
        self.assertTrue(
            operational_domains
            <= {row["domain"] for row in quality["intent_routing"]["domains"]}
        )
        self.assertTrue(
            {
                "relational_coordination",
                "process_stage_evidence",
                "instrument_capture_modality",
                "mobility_flow",
                "climate_material_consequence",
                "biodiversity_observation_protocol",
                "agriculture_batch_traceability",
                "circular_repair_material_flow",
            }
            <= {axis["id"] for axis in quality["photographic_integration"]["axes"]}
        )
        capture_policy = tags["slot_applicability"]["slots"]["capture_context"]
        self.assertTrue({"object", "environment"} <= set(capture_policy["subject_categories"]))
        self.assertTrue(operational_domains <= set(capture_policy["allow_domains"]))
        routing_categories = {
            row["category"] for row in quality["intent_routing"]["subject_categories"]
        }
        self.assertTrue({"animal", "object", "food", "plant", "environment"} <= routing_categories)
        expected_typed_presets = {
            "science_inspection": {"laboratory_measurement_record", "field_sensor_survey"},
            "mobility_logistics": {"warehouse_flow_documentary", "transit_maintenance_record"},
            "climate_adaptation": {"coastal_resilience_monitoring", "urban_heat_air_quality_record"},
            "biodiversity_monitoring": {"camera_trap_species_monitoring", "coastal_benthic_quadrat_survey"},
            "agriculture_food_systems": {"orchard_harvest_grading_record", "fermentation_batch_monitoring"},
            "circular_materials": {"electronics_repair_diagnostic_record", "materials_recovery_sorting_record"},
        }
        for domain, expected_ids in expected_typed_presets.items():
            actual_ids = {
                preset["id"]
                for preset in tags["presets"]
                if domain in prompt_generator.preset_domains(preset, tags)
            }
            self.assertEqual(actual_ids, expected_ids)

    def test_quality_facets_do_not_treat_focus_metadata_as_scene_location(self):
        pack = self.run_wrapper(
            "--preset",
            "laboratory_measurement_record",
            "--selection-mode",
            "rule",
            "--seed",
            "41",
            "--set",
            "focus=zone_focus_street",
            "--emit-candidate-pack",
        )[0]
        self.assertEqual(pack["quality_profile"]["profile_id"], "science_inspection")
        self.assertNotIn("street", pack["quality_profile"]["facets"].get("place_type", []))

    def test_new_typed_domain_packs_are_scoped_without_legacy_pool_pollution(self):
        tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_LAYERS_PATH.read_text(encoding="utf-8"))
        tags[prompt_generator.QUALITY_LAYERS_DATA_KEY] = quality
        presets = {preset["id"]: preset for preset in tags["presets"]}

        typed_presets = {
            "camera_trap_species_monitoring": "biodiversity_monitoring",
            "orchard_harvest_grading_record": "agriculture_food_systems",
            "electronics_repair_diagnostic_record": "circular_materials",
        }
        for preset_id, domain in typed_presets.items():
            preset = presets[preset_id]
            self.assertFalse(
                prompt_generator.preset_matches_automatic_intent_scope(preset, tags, None)
            )
            self.assertTrue(
                prompt_generator.preset_matches_automatic_intent_scope(
                    preset,
                    tags,
                    {
                        "intent_source": "user",
                        "intent_constraints": {"domains": [domain]},
                    },
                )
            )

        legacy_portrait = presets["maid_cafe_cosplay_portrait"]
        scoped_entries = [
            entry
            for entries in tags["slots"].values()
            for entry in entries
            if set(entry.get("tags", []))
            & set(prompt_generator.INTENT_SCOPED_ENTRY_DOMAIN_TAGS)
        ]
        self.assertEqual(len(scoped_entries), 40)
        self.assertTrue(
            all(
                not prompt_generator.entry_matches_preset_domain_scope(entry, legacy_portrait, tags)
                for entry in scoped_entries
            )
        )
        for preset_id in typed_presets:
            preset = presets[preset_id]
            filtered_ids = {
                entry_id
                for slot_filter in (preset.get("filters") or {}).values()
                for entry_id in slot_filter.get("ids", [])
            }
            scoped_for_preset = [entry for entry in scoped_entries if entry["id"] in filtered_ids]
            self.assertTrue(scoped_for_preset)
            self.assertTrue(
                all(
                    prompt_generator.entry_matches_preset_domain_scope(entry, preset, tags)
                    for entry in scoped_for_preset
                )
            )

        axis_profiles = {
            axis["id"]: axis.get("profile_match")
            for axis in quality["photographic_integration"]["axes"]
        }
        self.assertEqual(axis_profiles["biodiversity_observation_protocol"], ["biodiversity_monitoring"])
        self.assertEqual(axis_profiles["agriculture_batch_traceability"], ["agriculture_food_systems"])
        self.assertEqual(axis_profiles["circular_repair_material_flow"], ["circular_materials"])

        shared_facets = {
            "place_type": ["nature"],
            "process_stage": ["monitoring"],
            "capture_modality": ["surveillance"],
        }
        typed_craft = prompt_generator.candidate_pack_photographic_craft(
            tags,
            {"profile_id": "biodiversity_monitoring", "facets": shared_facets},
        )
        legacy_craft = prompt_generator.candidate_pack_photographic_craft(
            tags,
            {"profile_id": "nature", "facets": shared_facets},
        )
        typed_refinements = {
            refinement["id"]
            for dimension in typed_craft["active_dimensions"]
            for refinement in dimension["active_refinements"]
        }
        legacy_refinements = {
            refinement["id"]
            for dimension in legacy_craft["active_dimensions"]
            for refinement in dimension["active_refinements"]
        }
        self.assertIn("field_observation_record", typed_refinements)
        self.assertNotIn("field_observation_record", legacy_refinements)
        self.assertIn(
            "evidence_led",
            {strategy["id"] for strategy in typed_craft["strategy_variants"]},
        )
        self.assertNotIn(
            "evidence_led",
            {strategy["id"] for strategy in legacy_craft["strategy_variants"]},
        )

    def test_generalization_suite_is_executable_and_green(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(EVAL_PATH),
                "--tags",
                str(TAGS_PATH),
                "--generalization-cases",
                str(GENERALIZATION_PATH),
                "--generalization-check",
                "--holdout-cases",
                str(HOLDOUT_PATH),
                "--holdout-check",
                "--domain-holdout-v2-cases",
                str(DOMAIN_HOLDOUT_V2_PATH),
                "--domain-holdout-v2-check",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["generalization_check"]["case_count"], 79)
        self.assertEqual(payload["generalization_check"]["failed_case_count"], 0)
        self.assertEqual(payload["holdout_check"]["case_count"], 24)
        self.assertEqual(payload["holdout_check"]["failed_case_count"], 0)
        self.assertEqual(payload["domain_holdout_v2_check"]["case_count"], 6)
        self.assertEqual(payload["domain_holdout_v2_check"]["failed_case_count"], 0)

    def test_retrieval_holdout_and_research_evidence_contracts_are_versioned(self):
        retrieval_cases = eval_semantic.load_retrieval_holdout_cases(RETRIEVAL_HOLDOUT_V3_PATH)
        self.assertEqual(len(retrieval_cases), 6)
        self.assertTrue(all(case["allowed_selected_presets"] for case in retrieval_cases))
        self.assertTrue(all("preset" not in case for case in retrieval_cases))

        retrieval_v4_cases = eval_semantic.load_retrieval_holdout_cases(RETRIEVAL_HOLDOUT_V4_PATH)
        self.assertEqual(len(retrieval_v4_cases), 22)
        self.assertEqual(retrieval_v4_cases[:6], retrieval_cases)
        self.assertTrue(all(case["allowed_selected_presets"] for case in retrieval_v4_cases))
        self.assertTrue(all("preset" not in case for case in retrieval_v4_cases))

        evidence_rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertGreaterEqual(len(evidence_rows), 20)
        self.assertEqual(len({row["id"] for row in evidence_rows}), len(evidence_rows))
        self.assertGreaterEqual(len({row["domain"] for row in evidence_rows}), 15)
        merged_tags = prompt_generator.load_json(TAGS_PATH)
        catalog_ids = {str(preset["id"]) for preset in merged_tags["presets"]}
        for entries in merged_tags["slots"].values():
            catalog_ids.update(str(entry["id"]) for entry in entries)
        for row in evidence_rows:
            self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
            self.assertEqual(row["status"], "approved")
            self.assertTrue(str(row["source_url"]).startswith("https://"))
            self.assertTrue(row["abstracted_dimensions"])
            self.assertTrue(row["candidate_ids"])
            self.assertTrue(set(row["candidate_ids"]) <= catalog_ids, row["id"])
            self.assertIn("no ", row["reuse_note"].lower())
            self.assertIn("copied", row["reuse_note"].lower())

    def test_research_extension_is_additive_and_scopes_automatic_slots(self):
        raw_tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        extension = json.loads(RESEARCH_EXTENSION_PATH.read_text(encoding="utf-8"))
        merged = prompt_generator.merge_research_extension(copy.deepcopy(raw_tags), copy.deepcopy(extension))

        extension_ids = {preset["id"] for preset in extension["presets"]}
        merged_presets = {preset["id"]: preset for preset in merged["presets"]}
        self.assertEqual(len(extension_ids), 17)
        self.assertTrue(extension_ids <= set(merged_presets))

        for preset_id in extension_ids:
            preset = merged_presets[preset_id]
            self.assertEqual(preset["auto_optional_policy"], "authored_filters_only")
            filter_slots = set(preset.get("filters", {}))
            for spec in prompt_generator.optional_slot_specs(preset, merged):
                if spec.get("source") == "auto":
                    self.assertIn(spec["slot"], filter_slots, (preset_id, spec))

        duplicate = {
            "schema_version": prompt_generator.RESEARCH_EXTENSION_SCHEMA,
            "presets": [{"id": raw_tags["presets"][0]["id"], "filters": {}}],
        }
        with self.assertRaisesRegex(ValueError, "duplicate extension id"):
            prompt_generator.merge_research_extension(copy.deepcopy(raw_tags), duplicate)

        generic_window = prompt_generator.semantic_preset_score_window(
            {"semantic_profile": "conservative", "novelty": "low", "intent_constraints": {"domains": []}}
        )
        typed_window = prompt_generator.semantic_preset_score_window(
            {
                "semantic_profile": "conservative",
                "novelty": "low",
                "intent_constraints": {"domains": ["science_inspection"]},
            }
        )
        self.assertLess(typed_window, generic_window)

    def test_subculture_extension_routes_are_scoped_complete_and_runtime_selectable(self):
        data = prompt_generator.load_json(TAGS_PATH)
        extension = json.loads(SUBCULTURE_EXTENSION_PATH.read_text(encoding="utf-8"))
        extension_ids = {preset["id"] for preset in extension["presets"]}
        route_ids = extension_ids | {"punk_basement_show", "warehouse_rave_uv"}
        presets = {preset["id"]: preset for preset in data["presets"]}

        self.assertEqual(len(extension_ids), 33)
        self.assertEqual(
            set(extension["slot_applicability"]["preset_domain_overrides"]),
            route_ids,
        )
        self.assertTrue(route_ids <= set(presets))

        surface_policy = data["slot_applicability"]["slots"]["surface_material"]
        self.assertNotIn("human", surface_policy["subject_categories"])
        self.assertTrue(surface_policy["allow_domains_override_subject_categories"])
        self.assertEqual(
            prompt_generator.slot_block_reason(
                data,
                "surface_material",
                {"subject_category": "human", "preset_domains": ["sports_motion"]},
            ),
            "subject_category_not_allowed",
        )
        self.assertIsNone(
            prompt_generator.slot_block_reason(
                data,
                "surface_material",
                {
                    "subject_category": "human",
                    "preset_domains": ["subculture_practice"],
                },
            )
        )

        requested_context = {
            "intent_source": "user",
            "intent_constraints": {"domains": ["subculture_practice"]},
        }
        for seed, preset_id in enumerate(sorted(route_ids), start=1):
            preset = presets[preset_id]
            self.assertEqual(
                prompt_generator.preset_domains(preset, data),
                {"subculture_practice"},
            )
            self.assertTrue(
                {"subject", "action", "location", "prop"}
                <= set(preset["required_slots"]),
                preset_id,
            )
            self.assertFalse(
                prompt_generator.preset_matches_automatic_intent_scope(preset, data, None),
                preset_id,
            )
            self.assertTrue(
                prompt_generator.preset_matches_automatic_intent_scope(
                    preset, data, requested_context
                ),
                preset_id,
            )

            result = prompt_generator.generate_once(
                data,
                __import__("random").Random(seed),
                preset_id,
                ["en"],
                False,
                0,
                True,
                detail_level="detailed",
                selection_mode="rule",
                seed=seed,
            )
            choices = result["choices"]
            self.assertTrue(
                set(preset["required_slots"]) <= set(choices),
                (preset_id, sorted(set(preset["required_slots"]) - set(choices))),
            )
            for slot, choice in choices.items():
                authored_ids = set((preset.get("filters", {}).get(slot) or {}).get("ids", []))
                if authored_ids:
                    self.assertIn(choice["id"], authored_ids, (preset_id, slot, choice["id"]))

        first_route, second_route = sorted(route_ids)[:2]
        scoped_context = {
            "intent_source": "user",
            "intent_constraints": {
                "domains": ["subculture_practice"],
                "scoped_routes": [first_route],
            },
        }
        self.assertTrue(
            prompt_generator.preset_matches_automatic_intent_scope(
                presets[first_route], data, scoped_context
            )
        )
        self.assertFalse(
            prompt_generator.preset_matches_automatic_intent_scope(
                presets[second_route], data, scoped_context
            )
        )

        age_only_entries = [
            entry
            for entries in data["slots"].values()
            for entry in entries
            if "age_context_only" in set(entry.get("tags", []))
        ]
        self.assertGreaterEqual(len(age_only_entries), 40)
        for entry in age_only_entries:
            self.assertNotIn("adult", prompt_generator.adult_semantic_tokens(entry), entry["id"])

        legacy = presets["lowrider_night_meet"]
        self.assertFalse(legacy["automatic_discovery"])
        indexed_keys = {
            key for key, _, _, _ in prompt_generator.iter_semantic_entries(data)
        }
        self.assertNotIn("preset:lowrider_night_meet", indexed_keys)
        self.assertEqual(
            prompt_generator.choose_preset(
                data, __import__("random").Random(1), "lowrider_night_meet"
            )["id"],
            "lowrider_night_meet",
        )

        extension_text = json.dumps(extension, ensure_ascii=False).lower()
        for specific_ip_or_brand in (
            "pokemon",
            "mario",
            "gundam",
            "vocaloid",
            "hatsune miku",
            "disney",
            "sanrio",
            "hello kitty",
            "warhammer",
            "dungeons & dragons",
            "marvel",
            "dc comics",
            "nintendo",
            "playstation",
            "xbox",
            "hololive",
            "nijisanji",
            "live2d",
            "comiket",
        ):
            self.assertNotIn(specific_ip_or_brand, extension_text)

    def test_subculture_holdout_and_evidence_cover_all_frozen_themes(self):
        data = prompt_generator.load_json(TAGS_PATH)
        preset_ids = {preset["id"] for preset in data["presets"]}
        cases = eval_semantic.load_retrieval_holdout_cases(
            SUBCULTURE_RETRIEVAL_HOLDOUT_V1_PATH
        )
        self.assertEqual(len(cases), 70)
        self.assertEqual(len({case["id"] for case in cases}), 70)
        target_ids = {
            preset_id
            for case in cases
            for preset_id in case["allowed_selected_presets"]
        }
        self.assertEqual(len(target_ids), 35)
        self.assertTrue(target_ids <= preset_ids)
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        routing_policy = prompt_generator.candidate_pack_intent_routing_policy(data)
        scoped_rules = [
            rule
            for rule in routing_policy["scoped_routes"]
            if rule["domain"] == "subculture_practice"
        ]
        self.assertEqual(len(scoped_rules), 35)
        self.assertEqual({rule["preset_id"] for rule in scoped_rules}, target_ids)
        for rule in scoped_rules:
            self.assertEqual(rule["domain"], "subculture_practice")
            self.assertTrue(rule["aliases"])
        for case in cases:
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": case["intent"]}, {}
            )
            self.assertIn("subculture_practice", routed["domains"], case["id"])
            self.assertEqual(
                set(routed["scoped_routes"]),
                set(case["allowed_selected_presets"]),
                case["id"],
            )
        self.assertTrue(
            prompt_generator.intent_alias_matches("adult costume makers", "costume maker")
        )
        self.assertTrue(
            prompt_generator.intent_alias_matches("resin garage-kit parts", "garage kit")
        )
        for generic_intent in (
            "a generic studio portrait with neutral clothing and soft light",
            "판타지 코스프레 인물 사진",
            "K-style beauty editorial in a clean studio",
            "자동차 정비사가 주차된 차량을 점검하는 일반 다큐멘터리",
            "직업 교육 작업실에서 공구를 정리하는 모습",
        ):
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": generic_intent}, {}
            )
            self.assertNotIn("subculture_practice", routed["domains"], generic_intent)
            self.assertFalse(routed["scoped_routes"], generic_intent)

        evidence_rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line).get("domain") == "subculture_practice"
        ]
        self.assertGreaterEqual(len(evidence_rows), 46)
        theme_targets = {
            "cosplay": {"cosplay_fabrication_event_practice"},
            "fan_publishing": {"artist_alley_fan_publishing_exchange"},
            "zine_print": {"diy_zine_print_workshop"},
            "virtual_creator": {"virtual_creator_production_session"},
            "scale_models": {"scale_model_kitbash_workbench"},
            "diorama": {"miniature_diorama_build_workbench"},
            "toy_customization": {
                "doll_toy_customization_workshop",
                "plush_toy_repair_customization",
            },
            "character_suits": {
                "fursuit_fabrication_care",
                "mascot_suit_performance_care",
            },
            "lolita": {"lolita_coordinate_culture"},
            "japanese_street_style": {
                "decora_diy_maximalism",
                "gyaru_shibuya_glam",
                "heisei_y2k_revival",
            },
            "visual_kei": {"visual_kei_live_house"},
            "goth_club_rave": {
                "goth_scene_style_documentary",
                "cybergoth_club_style_documentary",
                "new_romantic_club_style_documentary",
                "warehouse_rave_uv",
            },
            "independent_music": {
                "punk_basement_show",
                "noise_performance_space_documentary",
                "shoegaze_small_venue_documentary",
            },
            "retro_gaming": {
                "retro_arcade_community_practice",
                "retro_lan_byoc_session",
                "retro_speedrun_event_practice",
            },
            "tabletop": {
                "ttrpg_collaborative_session",
                "miniature_wargaming_social_practice",
            },
            "custom_hardware": {
                "custom_pc_build_workbench",
                "mechanical_keyboard_build_workbench",
                "cyberdeck_enclosure_prototyping",
            },
            "vehicle_culture": {
                "lowrider_community_craft",
                "tuner_car_workshop_documentary",
                "itasha_display_culture_documentary",
            },
            "fandom_material": {
                "idol_fandom_material_culture",
                "anime_fandom_collection_exchange",
            },
        }
        self.assertEqual(len(theme_targets), 18)
        for theme, targets in theme_targets.items():
            independent_sources = {
                row["source_url"]
                for row in evidence_rows
                if targets & set(row["candidate_ids"])
            }
            self.assertGreaterEqual(len(independent_sources), 2, (theme, independent_sources))

    def test_worldbuilding_extension_routes_holdout_and_evidence_are_deep_and_scoped(self):
        data = prompt_generator.load_json(TAGS_PATH)
        extension = json.loads(WORLDBUILDING_EXTENSION_PATH.read_text(encoding="utf-8"))
        extension_ids = {preset["id"] for preset in extension["presets"]}
        presets = {preset["id"]: preset for preset in data["presets"]}

        self.assertEqual(len(extension_ids), 18)
        self.assertEqual(len(extension["preset_families"]), 6)
        self.assertEqual(
            sum(len(entries) for entries in extension["slots"].values()),
            288,
        )
        self.assertEqual(
            set(extension["slot_applicability"]["preset_domain_overrides"]),
            extension_ids,
        )
        self.assertTrue(extension_ids <= set(presets))

        world_evidence_slots = {
            "situation_context",
            "occasion_context",
            "narrative_core",
            "capture_context",
            "procedure_step",
            "surface_material",
        }
        requested_context = {
            "intent_source": "user",
            "intent_constraints": {"domains": ["worldbuilding_system"]},
        }
        for preset_id in sorted(extension_ids):
            preset = presets[preset_id]
            self.assertEqual(
                prompt_generator.preset_domains(preset, data),
                {"worldbuilding_system"},
            )
            self.assertTrue(
                {"subject", "action", "location", "prop"} | world_evidence_slots
                <= set(preset["required_slots"]),
                preset_id,
            )
            self.assertGreaterEqual(len(preset["facets"]["world_mechanism"]), 6)
            self.assertFalse(
                prompt_generator.preset_matches_automatic_intent_scope(preset, data, None)
            )
            self.assertTrue(
                prompt_generator.preset_matches_automatic_intent_scope(
                    preset, data, requested_context
                )
            )

            seen_subjects = set()
            for seed in (1, 2):
                result = prompt_generator.generate_once(
                    data,
                    __import__("random").Random(seed),
                    preset_id,
                    ["en"],
                    False,
                    0,
                    True,
                    detail_level="detailed",
                    selection_mode="rule",
                    seed=seed,
                )
                choices = result["choices"]
                self.assertTrue(set(preset["required_slots"]) <= set(choices), preset_id)
                subject_id = choices["subject"]["id"]
                seen_subjects.add(subject_id)
                scene_prefix = subject_id.removesuffix("_subject")
                for slot in (
                    "action",
                    "location",
                    "prop",
                    "situation_context",
                    "occasion_context",
                ):
                    self.assertTrue(
                        choices[slot]["id"].startswith(f"{scene_prefix}_"),
                        (preset_id, seed, slot, subject_id, choices[slot]["id"]),
                    )

                pack = prompt_generator.build_candidate_pack(result, data)
                self.assertEqual(pack["contract_version"], "photo-candidate-pack/v2")
                self.assertTrue(world_evidence_slots <= set(pack["slots"]), preset_id)
                self.assertEqual(
                    pack["quality_profile"]["facets"]["provenance_scope"],
                    preset["facets"]["provenance_scope"],
                    preset_id,
                )
                self.assertLessEqual(
                    sum(len(slot["candidates"]) for slot in pack["slots"].values()),
                    prompt_generator.CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT,
                    preset_id,
                )
            self.assertEqual(len(seen_subjects), 2, preset_id)

        self.assertEqual(
            presets["afrofuturist_worldmaking_curated"]["facets"]["provenance_scope"],
            ["public_culturally_curated"],
        )
        self.assertEqual(
            presets["indigenous_futurisms_curated"]["facets"]["provenance_scope"],
            ["public_culturally_curated"],
        )
        self.assertEqual(
            presets["fictional_esoteric_archive_world"]["facets"]["provenance_scope"],
            ["fictional_non_operational"],
        )
        self.assertEqual(
            presets["original_species_art_rpg_world"]["facets"]["provenance_scope"],
            ["rights_cleared_original"],
        )

        cases = eval_semantic.load_retrieval_holdout_cases(
            WORLDBUILDING_RETRIEVAL_HOLDOUT_V1_PATH
        )
        self.assertEqual(len(cases), 72)
        self.assertEqual(len({case["id"] for case in cases}), 72)
        targets = {
            preset_id
            for case in cases
            for preset_id in case["allowed_selected_presets"]
        }
        self.assertEqual(targets, extension_ids)
        self.assertTrue(all(len(case["allowed_selected_presets"]) == 1 for case in cases))

        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = prompt_generator.load_quality_layers(
            QUALITY_LAYERS_PATH
        )
        routing_policy = prompt_generator.candidate_pack_intent_routing_policy(data)
        world_rules = [
            rule
            for rule in routing_policy["scoped_routes"]
            if rule["domain"] == "worldbuilding_system"
        ]
        self.assertEqual(len(world_rules), 18)
        self.assertEqual({rule["preset_id"] for rule in world_rules}, extension_ids)
        for case in cases:
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": case["intent"]}, {}
            )
            self.assertIn("worldbuilding_system", routed["domains"], case["id"])
            self.assertEqual(
                set(routed["scoped_routes"]),
                set(case["allowed_selected_presets"]),
                case["id"],
            )

        solarpunk_case = next(case for case in cases if case["id"] == "world_solarpunk_ko_02")
        solarpunk_constraints = prompt_generator.resolve_request_intent_constraints(
            data, {"intent": solarpunk_case["intent"]}, {}
        )
        solarpunk_context = {
            "intent_source": "user",
            "intent_constraints": solarpunk_constraints,
        }
        self.assertTrue(
            prompt_generator.preset_matches_automatic_intent_scope(
                presets["civic_solarpunk_institutional_world"], data, solarpunk_context
            )
        )
        self.assertFalse(
            prompt_generator.preset_matches_automatic_intent_scope(
                presets["urban_heat_air_quality_record"], data, solarpunk_context
            )
        )

        for generic_intent in (
            "a generic studio portrait with neutral clothing and soft light",
            "a fantasy castle portrait with an unreadable map and cassette player",
            "documentary photo of city infrastructure maintenance",
            "solar panels and plants on a modern green roof",
            "a Black engineer repairing equipment in a future city",
            "an Indigenous adult using modern technology in a public library",
            "일반 기록관에서 오래된 종이 자료를 정리하는 성인 기록가",
            "판타지 성의 지도를 든 코스프레 인물",
        ):
            routed = prompt_generator.resolve_request_intent_constraints(
                data, {"intent": generic_intent}, {}
            )
            self.assertNotIn("worldbuilding_system", routed["domains"], generic_intent)
            self.assertFalse(routed["scoped_routes"], generic_intent)

        evidence_rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and json.loads(line).get("domain") == "worldbuilding_system"
        ]
        self.assertEqual(len(evidence_rows), 54)
        self.assertEqual(len({row["source_url"] for row in evidence_rows}), 54)
        self.assertEqual({row["topic_id"] for row in evidence_rows}, extension_ids)
        catalog_ids = set(presets)
        for entries in data["slots"].values():
            catalog_ids.update(entry["id"] for entry in entries)
        for preset_id in extension_ids:
            topic_rows = [row for row in evidence_rows if row["topic_id"] == preset_id]
            self.assertEqual(len(topic_rows), 3, preset_id)
            matrix_rows = [row for row in topic_rows if "world_mechanisms" in row]
            self.assertEqual(len(matrix_rows), 1, preset_id)
            matrix = matrix_rows[0]
            self.assertGreaterEqual(len(matrix["world_mechanisms"]), 6)
            self.assertGreaterEqual(len(matrix["photographic_evidence"]), 6)
            self.assertGreaterEqual(len(matrix["boundaries"]), 3)
            self.assertTrue(set(matrix["photographic_evidence"]) <= catalog_ids)
            self.assertTrue(
                all(set(row["candidate_ids"]) <= catalog_ids for row in topic_rows),
                preset_id,
            )

        extension_text = json.dumps(extension, ensure_ascii=False).lower()
        for protected_reference in (
            "pokemon",
            "middle earth",
            "star wars",
            "scp foundation",
            "dungeons & dragons",
            "mothman",
            "bigfoot",
            "hodag",
            "wakanda",
        ):
            self.assertNotIn(protected_reference, extension_text)

    def test_subculture_extension_override_contract_rejects_unknown_metadata(self):
        raw_tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        invalid = {
            "schema_version": prompt_generator.RESEARCH_EXTENSION_SCHEMA,
            "existing_preset_metadata_overrides": {
                raw_tags["presets"][0]["id"]: {"filters": {}}
            },
        }
        with self.assertRaisesRegex(ValueError, "unsupported keys"):
            prompt_generator.merge_research_extension(raw_tags, invalid)

    def test_research_presets_resist_legacy_bleed_and_misleading_intent(self):
        data = prompt_generator.load_json(TAGS_PATH)
        presets = {preset["id"]: preset for preset in data["presets"]}

        sports_wire = presets["sports_action_wire"]
        self.assertEqual(
            sports_wire["filters"]["subject"]["ids"],
            ["athlete_runner"],
        )
        self.assertEqual(
            sports_wire["filters"]["action"]["ids"],
            ["sprinting_track", "frozen_action"],
        )
        for preset_id in (
            "swimmer_lane_splash",
            "combat_sport_sweat",
            "track_sprint_blur",
            "equestrian_dust",
        ):
            preset_text = json.dumps(presets[preset_id], ensure_ascii=False).lower()
            self.assertNotIn("chalk", preset_text)

        pollinator = presets["pollinator_flower_visit_transect"]
        picked = {}
        contract = prompt_generator.make_generation_contract(data, pollinator, picked)
        subject = prompt_generator.choose_slot(
            "subject",
            data,
            pollinator,
            __import__("random").Random(7),
            picked,
            semantic_context=None,
            generation_contract=contract,
        )
        self.assertEqual(subject["id"], "pollinator_flower_visit_event")

        natural_markers = {
            "biological_soil_crust_patch": "biocrust",
            "streambank_erosion_deposition_profile": "geomorphology",
            "cold_surface_condensation_boundary": "condensation_process",
            "seed_radicle_emergence_macro": "germination",
            "freeze_thaw_soil_polygon_patch": "freeze_thaw",
        }
        for seed in range(1, 11):
            pack = self.run_wrapper(
                "--preset",
                "natural_process_trace_documentary",
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--emit-candidate-pack",
            )[0]
            selected = {
                slot: next(
                    candidate
                    for candidate in payload.get("candidates", [])
                    if candidate.get("selected_by_sampler")
                )
                for slot, payload in pack["slots"].items()
            }
            marker = natural_markers[selected["subject"]["entry_id"]]
            for slot in ("action", "location", "surface_material"):
                self.assertIn(marker, selected[slot].get("tags", []), (seed, slot, selected[slot]))

    def test_compact_quality_gate_summary_keeps_gate_and_check_counts(self):
        summary = {
            "quality_gate": {"passed": True, "legacy_passed": True},
            "golden_modes": [
                {"mode": "rule", "average_coverage": 1.0, "quality_fail_count": 0, "results": [1, 2]},
            ],
            "generalization_check": {"case_count": 60, "failed_case_count": 0, "results": [1]},
            "retrieval_holdout_v4_check": {"case_count": 22, "failed_case_count": 0, "results": [1]},
        }
        compact = eval_semantic.compact_quality_gate_summary(summary)
        self.assertEqual(compact["quality_gate"]["passed"], True)
        self.assertEqual(compact["checks"]["generalization_check"]["case_count"], 60)
        self.assertEqual(compact["checks"]["retrieval_holdout_v4_check"]["failed_case_count"], 0)
        self.assertNotIn("results", compact["checks"]["generalization_check"])
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "quality-report.json"
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                eval_semantic.emit_evaluation_summary(
                    summary,
                    summary_only=True,
                    report_json=report_path,
                )
            printed = json.loads(stdout.getvalue())
            report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertNotIn("results", printed["checks"]["generalization_check"])
        self.assertEqual(report["generalization_check"]["results"], [1])


if __name__ == "__main__":
    unittest.main()
