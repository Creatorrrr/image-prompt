from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EVIDENCE_PATH = ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "slender_linear_build",
    "soft_full_figure_volume",
    "curvilinear_figure_relation",
    "toned_muscular_build",
    "bust_prominence_relation",
    "top_hourglass_silhouette_relation",
    "bottom_hourglass_silhouette_relation",
    "triangle_lower_body_dominant_relation",
    "spoon_high_hip_silhouette_relation",
    "rectangle_silhouette_relation",
    "inverted_triangle_upper_body_dominant_relation",
    "oval_central_torso_silhouette_relation",
    "diamond_central_torso_silhouette_relation",
}


class PhotoBodyShapeSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"]}
        cls.candidates = {
            slot: {row["id"]: row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }

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
        return set(
            prompt_generator.candidate_pack_auto_visual_obligation_matches(
                self.registry,
                rows,
            )
        )

    def test_profiles_are_componentized_and_adult_scoped(self):
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], True)
                self.assertGreaterEqual(len(components["required_group_ids"]), 4)
                self.assertGreaterEqual(components["minimum_component_groups"], 4)
                self.assertGreaterEqual(len(profile["required_evidence_fields"]), 4)
                self.assertGreaterEqual(len(profile["render_gates"]), 4)
                self.assertTrue(profile["reject_substitutes"])

    def test_exact_body_terms_route_to_one_profile(self):
        cases = {
            "adult slender build": "slender_linear_build",
            "adult soft full figure": "soft_full_figure_volume",
            "adult curvy figure": "curvilinear_figure_relation",
            "adult toned physique": "toned_muscular_build",
            "adult busty figure": "bust_prominence_relation",
            "adult top hourglass silhouette": "top_hourglass_silhouette_relation",
            "adult bottom hourglass silhouette": "bottom_hourglass_silhouette_relation",
            "adult pear-shaped figure": "triangle_lower_body_dominant_relation",
            "adult spoon-shaped figure": "spoon_high_hip_silhouette_relation",
            "adult straight body silhouette": "rectangle_silhouette_relation",
            "adult inverted triangle figure": "inverted_triangle_upper_body_dominant_relation",
            "adult apple-shaped figure": "oval_central_torso_silhouette_relation",
            "adult diamond-shaped figure": "diamond_central_torso_silhouette_relation",
            "성인 여성 슬렌더 체형": "slender_linear_build",
            "성인 여성 글래머 체형": "curvilinear_figure_relation",
            "성인 여성 거유 체형": "bust_prominence_relation",
            "성인 여성 하이힙 스푼 체형": "spoon_high_hip_silhouette_relation",
        }
        for text, expected_id in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected_id})

    def test_hourglass_variants_do_not_double_activate_base_profile(self):
        self.assertEqual(
            self.hard_matches("adult hourglass silhouette"),
            {"hourglass_silhouette_relation"},
        )
        self.assertEqual(
            self.hard_matches("adult top hourglass silhouette"),
            {"top_hourglass_silhouette_relation"},
        )
        self.assertEqual(
            self.hard_matches("adult bottom hourglass silhouette"),
            {"bottom_hourglass_silhouette_relation"},
        )

    def test_regional_and_global_terms_are_not_equivalent(self):
        self.assertEqual(
            self.hard_matches("adult busty figure"),
            {"bust_prominence_relation"},
        )
        self.assertNotIn(
            "curvilinear_figure_relation",
            self.hard_matches("adult busty figure"),
        )
        self.assertEqual(
            self.hard_matches("adult curvy figure"),
            {"curvilinear_figure_relation"},
        )
        self.assertNotIn(
            "bust_prominence_relation",
            self.hard_matches("adult curvy figure"),
        )
        self.assertEqual(
            self.hard_matches("adult slender build"),
            {"slender_linear_build"},
        )
        self.assertNotIn(
            "toned_muscular_build",
            self.hard_matches("adult slender build"),
        )

    def test_ambiguous_bare_labels_and_non_body_homonyms_fail_closed(self):
        cases = (
            "slender",
            "curvy",
            "busty",
            "petite",
            "willowy",
            "statuesque",
            "글래머",
            "육덕",
            "거유",
            "S라인",
            "콜라병 몸매",
            "개미허리",
            "골반 미인",
            "베이글녀",
            "BBW",
            "plus-size",
            "adult athletic competition",
            "adult toned photograph",
            "pear fruit still life",
            "diamond necklace portrait",
            "oval mirror product photo",
            "rectangle table design",
            "classical portrait bust sculpture",
            "petite clothing size chart",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_triangle_spoon_and_central_torso_boundaries_are_explicit(self):
        triangle = json.dumps(
            self.profiles["triangle_lower_body_dominant_relation"],
            ensure_ascii=False,
        )
        spoon = json.dumps(
            self.profiles["spoon_high_hip_silhouette_relation"],
            ensure_ascii=False,
        )
        oval = json.dumps(
            self.profiles["oval_central_torso_silhouette_relation"],
            ensure_ascii=False,
        )
        diamond = json.dumps(
            self.profiles["diamond_central_torso_silhouette_relation"],
            ensure_ascii=False,
        )
        self.assertIn("no mandatory high-hip shelf", triangle)
        self.assertIn("rapid outward transition at the high-hip", spoon)
        self.assertIn("weak waist indentation", oval)
        self.assertIn("tapers toward both", diamond)
        self.assertIn(
            "oval_without_two_direction_taper",
            self.profiles["diamond_central_torso_silhouette_relation"][
                "reject_substitutes"
            ],
        )

    def test_profiles_do_not_encode_numeric_body_thresholds(self):
        numeric_body_threshold = re.compile(
            r"\b\d+(?:\.\d+)?\s*(?:%|cm|mm|inch|inches)\b",
            re.IGNORECASE,
        )
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                semantic_payload = json.dumps(
                    {
                        "semantics": profile["semantics"],
                        "concept_candidate": profile["concept_candidate"],
                        "composition_instruction": profile["composition_instruction"],
                    },
                    ensure_ascii=False,
                )
                self.assertIsNone(numeric_body_threshold.search(semantic_payload))
                self.assertNotIn("universally ideal", semantic_payload.casefold())

    def test_candidate_pack_covers_build_region_shape_and_observability_axes(self):
        expected_by_slot = {
            "silhouette_proportion": {
                "slender_linear_build",
                "soft_full_figure_volume",
                "curvilinear_figure_relation",
                "toned_muscular_definition",
                "compact_adult_frame",
                "willowy_long_limb_proportion",
                "statuesque_tall_large_proportion",
                "long_torso_shorter_leg_relation",
                "short_torso_longer_leg_relation",
                "top_hourglass_relation",
                "bottom_hourglass_relation",
                "triangle_lower_body_dominant_relation",
                "spoon_high_hip_relation",
                "rectangle_low_waist_definition_relation",
                "inverted_triangle_upper_body_dominant_relation",
                "oval_central_torso_relation",
                "diamond_central_torso_relation",
            },
            "anatomical_connection": {
                "bust_to_ribcage_projection_relation",
                "bust_to_waist_width_relation",
                "narrow_shoulder_ribcage_frame",
                "broad_shoulder_ribcage_frame",
                "narrow_pelvic_frame_relation",
                "wide_pelvic_frame_relation",
                "rounded_gluteal_projection",
                "full_outer_thigh_volume",
                "lean_defined_thigh_contour",
                "central_abdominal_projection_relation",
            },
            "body_framing": {
                "bilateral_torso_shape_read",
                "full_body_vertical_proportion_read",
                "bust_ribcage_waist_relation_crop",
                "hip_glute_thigh_relation_crop",
                "front_side_central_torso_read",
            },
        }
        for slot, expected_ids in expected_by_slot.items():
            with self.subTest(slot=slot):
                self.assertTrue(expected_ids <= set(self.candidates[slot]))

    def test_research_evidence_is_approved_and_candidate_bound(self):
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        body_shape_rows = [
            row for row in rows if row["id"].startswith("body_shape_semantics_")
        ]
        self.assertEqual(len(body_shape_rows), 13)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in body_shape_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertEqual(row["domain"], "body_shape_visual_semantics")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])


if __name__ == "__main__":
    unittest.main()
