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
RESEARCH_EVIDENCE_PATH = SKILL_DIR / "assets" / "research_evidence.jsonl"
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
        self.assertEqual(payload["generalization_check"]["case_count"], 60)
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

        evidence_rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertGreaterEqual(len(evidence_rows), 4)
        for row in evidence_rows:
            self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
            self.assertEqual(row["status"], "approved")
            self.assertTrue(str(row["source_url"]).startswith("https://"))
            self.assertTrue(row["abstracted_dimensions"])
            self.assertTrue(row["candidate_ids"])
            self.assertIn("no ", row["reuse_note"].lower())
            self.assertIn("copied", row["reuse_note"].lower())

    def test_compact_quality_gate_summary_keeps_gate_and_check_counts(self):
        summary = {
            "quality_gate": {"passed": True, "legacy_passed": True},
            "golden_modes": [
                {"mode": "rule", "average_coverage": 1.0, "quality_fail_count": 0, "results": [1, 2]},
            ],
            "generalization_check": {"case_count": 60, "failed_case_count": 0, "results": [1]},
            "retrieval_holdout_v3_check": {"case_count": 6, "failed_case_count": 0, "results": [1]},
        }
        compact = eval_semantic.compact_quality_gate_summary(summary)
        self.assertEqual(compact["quality_gate"]["passed"], True)
        self.assertEqual(compact["checks"]["generalization_check"]["case_count"], 60)
        self.assertEqual(compact["checks"]["retrieval_holdout_v3_check"]["failed_case_count"], 0)
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
