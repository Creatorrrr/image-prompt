import json
import random
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = PROJECT_ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
sys.path.append(str(SCRIPT_DIR))

import generate_photo_prompt  # noqa: E402
import prompt_generator  # noqa: E402


class TestPromptExpansionRoutes(unittest.TestCase):
    def setUp(self):
        self.tags = json.loads((SKILL_DIR / "assets" / "photo_prompt_tags.json").read_text(encoding="utf-8"))
        self.recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))

    def slot_ids(self, slot):
        return {entry["id"] for entry in self.tags["slots"][slot]}

    def preset(self, preset_id):
        return next(preset for preset in self.tags["presets"] if preset["id"] == preset_id)

    def slot_entry(self, slot, entry_id):
        return next(entry for entry in self.tags["slots"][slot] if entry["id"] == entry_id)

    def test_new_presets_and_slot_entries_are_registered(self):
        self.assertTrue(
            {
                "moonlit_fairy_garden_portrait",
                "digital_disintegration_portrait",
                "modern_hanbok_valley_fullbody",
            }.issubset({preset["id"] for preset in self.tags["presets"]})
        )
        self.assertTrue(
            {
                "crystal_rain_bokeh",
                "fireflies_drift",
                "luminous_pollen_glow",
                "glowing_butterflies_soft",
            }.issubset(self.slot_ids("ambient_particle"))
        )
        self.assertTrue(
            {"white_dove_perched", "white_dove_in_flight", "pastel_parakeet_pair"}.issubset(
                self.slot_ids("companion_animal")
            )
        )
        self.assertTrue(
            {"surface_pixel_mosaic_dissolve", "particle_disperse_to_black"}.issubset(
                self.slot_ids("transition_stage")
            )
        )
        self.assertIn("landscape_embroidery_hem", self.slot_ids("garment_detail"))
        self.assertIn("anti_food_sensual", self.tags["negative_prompt_pools"])

    def test_bride_alias_routes_to_bridal_not_priest(self):
        _args, explanations = generate_photo_prompt.resolve_concepts(
            ["--selection-mode", "rule", "--seed", "1"],
            ["천사 신부 꽃방"],
            concept_mode="legacy",
        )
        explanation = explanations[0]
        self.assertIsNone(explanation["role"])
        self.assertIn("브라이덜", explanation["applied_mixins"])
        self.assertIn("천사", explanation["applied_mixins"])
        self.assertNotEqual(explanation.get("applied_role"), "사제")
        self.assertIn(
            "bridal_veil_white_gown_costume",
            explanation["combined_forced_slots"]["costume_style"],
        )

    def test_student_train_platform_route_requires_approval_by_default(self):
        _args, explanations = generate_photo_prompt.resolve_concepts(
            ["--selection-mode", "rule", "--seed", "1"],
            ["성인 학생 기차 플랫폼 헤드폰"],
            concept_mode="legacy",
        )
        recipe = explanations[0]["recipe"]
        forced = explanations[0]["combined_forced_slots"]
        self.assertEqual(explanations[0]["applied_role"], "학생")
        self.assertNotIn("korean_train_platform", forced["location"])
        self.assertNotIn("train_platform_last_car", forced["location"])
        self.assertNotIn("prop", forced)

        route = recipe["approval_required_routes"]["adult_transit_reference"]
        self.assertTrue(route["requires_user_approval"])
        self.assertEqual(route["default"], "off")
        self.assertIn("location=korean_train_platform,train_platform_last_car", route["on_accept"]["set"])
        self.assertIn("prop=over_ear_headphones,black_backpack_one_shoulder,train_ticket_stub_prop", route["on_accept"]["set"])
        self.assertTrue(route["on_decline"]["preserve_original_intent"])

    def test_digital_disintegration_preserves_integrity_policy(self):
        preset = self.preset("digital_disintegration_portrait")
        self.assertEqual(
            set(preset["filters"]["transition_stage"]["ids"]),
            {"surface_pixel_mosaic_dissolve", "particle_disperse_to_black"},
        )
        guard = next(
            rule
            for rule in self.tags["coherence_rules"]["slot_context_rules"]
            if rule["id"] == "digital_dissolution_integrity_guard"
        )
        self.assertEqual(set(guard["requires_item_any"]), {"face_integrity", "eye_integrity", "hand_integrity", "no_text"})
        policy = self.tags["semantic_policy"]["families"]["digital_entity"]
        self.assertIn("digital_disintegration_portrait", policy["preset_policy"]["allow_ids"])

    def test_tomato_near_lips_appends_food_sensual_negatives(self):
        picked = {"prop": self.slot_entry("prop", "single_ripe_tomato_near_lips")}
        entries_without_approval = prompt_generator.choose_negative_entries(
            self.tags,
            random.Random(7),
            count=1,
            picked=picked,
            safety_transform_approved=False,
        )
        negative_en = {entry["en"] for entry in entries_without_approval}
        self.assertNotIn("lip licking", negative_en)
        self.assertNotIn("food fetish framing", negative_en)

        entries = prompt_generator.choose_negative_entries(
            self.tags,
            random.Random(7),
            count=1,
            picked=picked,
            safety_transform_approved=True,
        )
        approved_negative_en = {entry["en"] for entry in entries}
        self.assertIn("lip licking", approved_negative_en)
        self.assertIn("food fetish framing", approved_negative_en)

    def test_candidate_pack_safety_transforms_are_pending_without_approval(self):
        args, explanations = generate_photo_prompt.resolve_concepts(
            ["--selection-mode", "rule", "--seed", "1"],
            ["유나 바니걸"],
            concept_mode="soft",
            safety_transform_approved=False,
        )
        explanation = explanations[0]
        policy = explanation["soft_anchor_spec"]
        pending = explanation["approval_required_safety_transforms"]

        self.assertEqual(pending["status"], "pending")
        self.assertTrue(pending["requires_user_approval"])
        self.assertEqual(policy["visual_guards"], [])
        self.assertEqual(policy["free_slot_constraints"], {})
        self.assertEqual(policy["safety_negative_floor"], [])
        self.assertTrue(any(item["field"] == "safety_negative_floor" for item in pending["items"]))
        additional_args = [
            args[index + 1]
            for index, value in enumerate(args[:-1])
            if value == "--additional-requirement"
        ]
        self.assertNotIn(
            "adult subject only; bunny-girl costume must be covered stage cosplay, not lingerie focus, nudity, or explicit sexual posing",
            additional_args,
        )
        self.assertFalse(any("covered adult bunny-girl stage costume" in arg for arg in additional_args))

    def test_candidate_pack_safety_transforms_apply_after_approval(self):
        args, explanations = generate_photo_prompt.resolve_concepts(
            ["--selection-mode", "rule", "--seed", "1"],
            ["유나 바니걸"],
            concept_mode="soft",
            safety_transform_approved=True,
        )
        policy = explanations[0]["soft_anchor_spec"]

        self.assertNotIn("approval_required_safety_transforms", explanations[0])
        self.assertTrue(policy["visual_guards"])
        self.assertIn("lingerie focus", policy["safety_negative_floor"])
        self.assertIn(
            "adult subject only; bunny-girl costume must be covered stage cosplay, not lingerie focus, nudity, or explicit sexual posing",
            args,
        )
        self.assertTrue(any("covered adult bunny-girl stage costume" in arg for arg in args))

    def test_candidate_pack_forward_args_default_to_safety_approval_required(self):
        args = generate_photo_prompt.build_forward_args(
            ["--concept", "유나 바니걸", "--emit-candidate-pack", "--selection-mode", "rule"]
        )
        self.assertIn("--safety-transform-policy", args)
        self.assertEqual(args[args.index("--safety-transform-policy") + 1], "approval-required")

        approved_args = generate_photo_prompt.build_forward_args(
            [
                "--concept",
                "유나 바니걸",
                "--emit-candidate-pack",
                "--selection-mode",
                "rule",
                "--approve-safety-transforms",
            ]
        )
        self.assertIn("--safety-transform-policy", approved_args)
        self.assertEqual(approved_args[approved_args.index("--safety-transform-policy") + 1], "approved")

    def test_modern_hanbok_fullbody_preset_pins_boundary_and_valley(self):
        preset = self.preset("modern_hanbok_valley_fullbody")
        self.assertEqual(preset["filters"]["shot_scale"]["ids"], ["full_length_body_shot"])
        self.assertEqual(preset["filters"]["frame_anchor_medium"]["ids"], ["full_body_boundary_preserved"])
        self.assertIn("mountain_valley_stream_spring", preset["filters"]["location"]["ids"])
        self.assertIn("landscape_embroidery_hem", preset["filters"]["garment_detail"]["ids"])


if __name__ == "__main__":
    unittest.main()
