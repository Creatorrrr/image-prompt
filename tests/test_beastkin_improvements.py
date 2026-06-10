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


class TestBeastkinImprovements(unittest.TestCase):
    def setUp(self):
        self.recipes = json.loads((SKILL_DIR / "assets" / "concept_recipes.json").read_text(encoding="utf-8"))
        self.tags = json.loads((SKILL_DIR / "assets" / "photo_prompt_tags.json").read_text(encoding="utf-8"))

    def slot_ids(self, slot):
        return {entry["id"] for entry in self.tags["slots"][slot]}

    def test_beastkin_slots_and_negative_pool_are_registered(self):
        self.assertIn("anatomical_connection", self.tags["slots"])
        self.assertIn("body_evidence_region", self.tags["slots"])
        self.assertIn("costume_absorption_guard", self.tags["slots"])

        self.assertIn("anatomical_connection", self.tags["slot_pick_order"])
        self.assertIn("body_evidence_region", self.tags["slot_pick_order"])
        self.assertIn("costume_absorption_guard", self.tags["slot_pick_order"])
        self.assertGreaterEqual(self.tags["slot_priorities"]["anatomical_connection"], 2.0)

        self.assertTrue(
            {
                "tail_base_under_waistband",
                "ear_root_in_hairline",
                "feather_skin_follicle_boundary",
                "scale_skin_gradient_boundary",
            }.issubset(self.slot_ids("anatomical_connection"))
        )
        self.assertIn("anti_ornament_absorption", self.tags["negative_prompt_pools"])

    def test_every_beastkin_species_variant_pins_marker_texture_and_body_connection(self):
        mixin = self.recipes["mixins"]["수인"]
        species_ids = self.slot_ids("species_marker")
        texture_ids = self.slot_ids("texture")
        anatomy_ids = self.slot_ids("anatomical_connection")

        for variant in mixin["species_variants"]["variants"]:
            with self.subTest(variant=variant["id"]):
                forced = variant.get("set", {})
                self.assertIn(forced.get("species_marker"), species_ids)
                self.assertIn(forced.get("texture"), texture_ids)
                self.assertIn(forced.get("anatomical_connection"), anatomy_ids)
                self.assertIn("species_marker", variant.get("soft_anchor_slots", []))
                self.assertIn("anatomical_connection", variant.get("soft_anchor_slots", []))

    def test_beastkin_required_priority_is_body_rooted_not_ears_tail_only(self):
        mixin = self.recipes["mixins"]["수인"]
        required = [
            group for group in mixin["render_priority_terms"]
            if group["tier"] == "required" and group["id"] == "beastkin_body_rooted_evidence"
        ]
        self.assertEqual(len(required), 1)
        terms = set(required[0]["terms"])
        self.assertGreaterEqual(required[0]["min_hits"], 2)
        self.assertNotIn("pointed ears", terms)
        self.assertNotIn("tail", terms)
        self.assertTrue({"ear root", "tail base", "horn root", "feather follicle"}.issubset(terms))
        self.assertIn("anatomical_connection", required[0]["target_slots"])

    def test_review_weak_roles_have_role_specific_beastkin_bundles(self):
        mixin = self.recipes["mixins"]["수인"]
        covered_roles = set()
        for bundle in mixin["bundles"]:
            covered_roles.update(bundle.get("roles") or [])
        self.assertTrue(
            {"산타복", "운동복", "공주", "고스로리", "광부", "사복 여친", "바니걸"}.issubset(covered_roles)
        )

        conditional_roles = set()
        for rule in mixin["conditional_additional"]:
            conditional_roles.update(rule.get("roles") or [])
        self.assertTrue(
            {"산타복", "운동복", "공주", "고스로리", "광부", "사복 여친", "바니걸"}.issubset(conditional_roles)
        )

    def test_beastkin_ornament_risk_appends_absorption_negatives(self):
        forced_choices = {
            "subject": ["beastkin_subject"],
            "costume_style": ["bunny_girl_costume"],
            "species_marker": ["lagomorph_ear_root_parting_hair"],
            "transition_stage": ["boundary_stage_visible_skin_shift"],
            "anatomical_connection": ["ear_root_in_hairline"],
            "costume_absorption_guard": ["costume_bunny_ears_separate_from_anatomy_guard"],
        }
        item = prompt_generator.generate_once(
            self.tags,
            random.Random(81),
            preset_id="japanese_otaku_costume_portrait",
            langs=["en"],
            forced_choices=forced_choices,
            include_negative=True,
            negative_count=3,
            include_choices=False,
        )

        self.assertIn("costume headband ears", item["negative_en"])
        self.assertIn("costume bunny ears read as living anatomy", item["negative_en"])
        self.assertIn("hood trim mistaken for animal ears", item["negative_en"])

    def test_role_beastkin_explain_carries_body_evidence_slots(self):
        args, explanations = generate_photo_prompt.resolve_concepts(
            ["--selection-mode", "rule", "--seed", "27"],
            ["유나 바니걸 수인"],
            concept_mode="legacy",
        )

        self.assertIn("--preset", args)
        concept = explanations[0]
        self.assertEqual(concept["applied_mixins"], ["수인"])
        self.assertEqual(concept["selected_bundles"][0]["bundle_id"], "bunny_stage_living_lagomorph_guard")
        forced = concept["combined_forced_slots"]
        self.assertIn("species_marker", forced)
        self.assertIn("anatomical_connection", forced)
        self.assertIn("body_evidence_region", forced)
        self.assertIn("costume_absorption_guard", forced)


if __name__ == "__main__":
    unittest.main()
