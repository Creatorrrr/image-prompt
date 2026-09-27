from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
ASSET_DIR = SKILL_DIR / "assets"
REGISTRY_PATH = ASSET_DIR / "photo_prompt_visual_obligations.json"
VISUAL_INDEX_PATH = ASSET_DIR / "photo_prompt_visual_profile_index.json"
SEMANTIC_INDEX_PATH = ASSET_DIR / "photo_prompt_semantic_index.json"
TAGS_PATH = ASSET_DIR / "photo_prompt_tags.json"
EXTENSION_PATH = ASSET_DIR / "photo_prompt_reactorprompt_visual_relations_extension.json"
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "reactorprompt_visual_relations_three_arm_pixel_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "patterned_cast_shadow_receiver_continuity",
    "two_adult_shared_target_handoff",
    "satin_directional_luster_drape_surface",
}

TOPIC_CANDIDATES = {
    "composition": {
        "crop_boundary_anchor_integrity",
        "multi_panel_count_layout_sequence",
        "foreground_midground_background_depth_chain",
        "product_surface_support_hierarchy",
        "food_material_state_vessel_relation",
        "nature_habitat_subject_state_advisory",
    },
    "body_pose": {"single_support_backward_flexed_free_leg"},
    "body_framing": {"forward_torso_lean_close_crop"},
    "contact_point": {
        "fingertip_contact_visible_target_non_support",
        "load_bearing_contact_deformation",
    },
    "action": {"tool_contact_active_process_visible_result"},
    "lens": {"source_relative_perspective_distance_coherence"},
    "focus": {"subject_anchor_focus_plane_priority"},
    "light_shape": {"patterned_cast_shadow_receiver_continuity"},
    "lighting": {
        "daylight_fill_flash_balance_relation",
        "multi_material_same_source_response",
    },
    "color_grading": {
        "palette_role_hierarchy_relation",
        "selective_color_same_surface_exception_relation",
        "low_chroma_preserved_color_separation",
    },
    "weather": {"weather_material_subject_consequence_chain"},
    "relational_action": {
        "two_adult_shared_target_handoff",
        "cropped_companion_visible_contact_relation",
    },
    "partner_framing": {
        "foreground_background_two_actor_occlusion_relation",
        "cropped_companion_limb_ownership",
    },
    "proxemics": {"focused_group_shared_access_formation"},
    "gaze_target": {"head_eye_counterorientation_relation"},
    "expression": {"facial_display_native_readability"},
    "surface_material": {
        "satin_directional_luster_drape_surface",
        "velvet_pile_nap_direction_surface",
    },
    "hair_style": {"wind_displaced_hair_coherence"},
    "skin_finish": {"skin_microtexture_local_light_response"},
    "capture_context": {
        "front_camera_low_light_response_advisory",
        "capture_label_effect_separation",
    },
    "narrative_phase": {
        "precontact_readiness_visible_gap",
        "locomotion_counterturn_midphase",
        "source_to_receiver_liquid_transfer_midphase",
        "tool_contact_active_process_phase",
        "postcontact_release_continuing_trajectory",
        "visible_mishap_repair_phase",
        "untouched_target_preuse_threshold",
        "settling_aftereffect_trace_phase",
    },
}


class PhotoReactorPromptVisualRelationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"]}
        cls.tags = prompt_generator.load_json(TAGS_PATH)

    def hard_matches(self, text: str) -> set[str]:
        rows = [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            }
        ]
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            rows,
            adult_context=True,
        )
        return {
            row["profile_id"]
            for row in resolution["hits"]
            if row["match_basis"] == "exact" and row["hard_eligible"] is True
        }

    def test_three_request_scoped_profiles_have_typed_relation_contracts(self) -> None:
        self.assertEqual(
            self.registry["relation_contract_version"],
            "photo-visual-relation/v1",
        )
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                relation = profile["visual_relation"]
                self.assertEqual(relation["schema_version"], "photo-visual-relation/v1")
                self.assertEqual(relation["status"], "request_scoped")
                self.assertEqual(relation["observability"]["ineligible_state"], "UNSCORED")
                self.assertIs(relation["activation"]["hard_only_from_exact_source"], True)
                self.assertIs(relation["activation"]["embedding_only_is_advisory"], True)
                self.assertIs(relation["activation"]["all_required_components_coexist"], True)
                self.assertEqual(
                    set(relation["observability"]["required_visible_regions"]),
                    set(relation["visible_regions"]),
                )
                components = profile["semantics"]["component_semantics"]
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(len(profile["render_gates"]), 5)

    def test_exact_terms_activate_only_narrow_profiles(self) -> None:
        cases = {
            "patterned cast shadow receiver continuity": "patterned_cast_shadow_receiver_continuity",
            "two adult shared target handoff": "two_adult_shared_target_handoff",
            "satin directional luster": "satin_directional_luster_drape_surface",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected})

    def test_broad_or_confounded_terms_remain_non_hard(self) -> None:
        for text in (
            "leaf shadow portrait",
            "printed leaf pattern on a shirt",
            "two friends with objects",
            "a static object between two people",
            "satin dress",
            "global bloom on dark fabric",
            "velvet",
            "cinematic lighting",
        ):
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_profile_projection_carries_relation_metadata_into_candidate_pack(self) -> None:
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                obligation = prompt_generator.candidate_pack_visual_profile_obligation(
                    self.profiles[profile_id],
                    self.registry,
                    activation_source="explicit_visual_intent",
                    source_intent_ids=["test-intent"],
                )
                self.assertEqual(
                    obligation["visual_relation"],
                    self.profiles[profile_id]["visual_relation"],
                )
                self.assertEqual(
                    obligation["visual_relation"]["observability"]["ineligible_state"],
                    "UNSCORED",
                )

    def test_advisory_candidates_cover_research_topics_without_negative_footer(self) -> None:
        raw_extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        self.assertIn("T14 failure prevention", raw_extension["description"])
        self.assertIn("T15 clause lineage", raw_extension["description"])
        for slot, expected_ids in TOPIC_CANDIDATES.items():
            with self.subTest(slot=slot):
                actual = {row["id"] for row in self.tags["slots"][slot]}
                self.assertTrue(expected_ids <= actual)
        all_expected = {
            f"slot:{slot}:{entry_id}"
            for slot, entry_ids in TOPIC_CANDIDATES.items()
            for entry_id in entry_ids
        }
        self.assertGreaterEqual(len(all_expected), 35)
        forbidden_broad_ids = {
            "bad_anatomy",
            "ai_artifact",
            "no_plastic_skin",
            "no_waxy_skin",
            "beauty_filter_negative",
        }
        self.assertTrue(
            forbidden_broad_ids.isdisjoint(
                {
                    row["id"]
                    for slot in raw_extension["slots"].values()
                    for row in slot
                }
            )
        )

    def test_generated_indexes_include_profiles_and_candidates(self) -> None:
        visual_index = prompt_generator.load_visual_profile_index(
            VISUAL_INDEX_PATH,
            self.registry,
            provider=prompt_generator.SEMANTIC_PROVIDER,
            model=prompt_generator.SEMANTIC_MODEL_ID,
            dimensions=prompt_generator.DEFAULT_SEMANTIC_DIMENSIONS,
        )
        self.assertTrue(PROFILE_IDS <= set(visual_index["entries"]))
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        expected = {
            f"slot:{slot}:{entry_id}"
            for slot, entry_ids in TOPIC_CANDIDATES.items()
            for entry_id in entry_ids
        }
        self.assertTrue(expected <= set(semantic_index["entries"]))

    def test_three_arm_fixture_preserves_independence_and_all_of_gates(self) -> None:
        if not CASES_PATH.exists():
            self.skipTest("three-arm fixture is written after independent arm generation")
        rows = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual({row["profile_id"] for row in rows}, PROFILE_IDS)
        self.assertEqual(len({row["arm_id"] for row in rows}), 3)
        for row in rows:
            with self.subTest(arm_id=row["arm_id"]):
                self.assertIs(row["generation_policy"]["single_generation_call"], True)
                self.assertIs(row["generation_policy"]["cross_arm_inputs_allowed"], False)
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")
                self.assertEqual(row["verdict_rule"]["invisible_required_region"], "UNSCORED")
                self.assertEqual(
                    set(row["required_gate_ids"]),
                    {gate["id"] for gate in self.profiles[row["profile_id"]]["render_gates"]},
                )


if __name__ == "__main__":
    unittest.main()
