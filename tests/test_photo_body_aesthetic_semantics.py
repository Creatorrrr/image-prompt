from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EVIDENCE_PATH = ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
PIXEL_CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "body_semantics_pixel_test_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


class PhotoBodyAestheticSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"]}
        cls.candidates = {
            slot: {row["id"]: row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.pixel_cases = [
            json.loads(line)
            for line in PIXEL_CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

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

    def test_research_profiles_are_componentized_and_registered(self):
        expected = {
            "upper_lip_philtral_contour",
            "clavicle_supraclavicular_hollow",
            "decolletage_neckline_exposure",
            "lateral_waist_hip_contour_transition",
            "posterior_lumbosacral_landmarks",
            "contrapposto_weight_shift",
            "body_bounded_negative_space",
            "hogarth_waving_line_of_beauty",
            "hogarth_serpentine_line_of_grace",
            "hourglass_silhouette_relation",
        }
        self.assertTrue(expected <= set(self.profiles))
        for profile_id in expected:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                required_groups = set(
                    profile["semantics"]["component_semantics"]["required_group_ids"]
                )
                self.assertGreaterEqual(len(required_groups), 3)
                self.assertGreaterEqual(len(profile["required_evidence_fields"]), 4)
                self.assertGreaterEqual(len(profile["render_gates"]), 4)

    def test_exact_terms_route_and_ambiguous_shorthand_fails_closed(self):
        positives = {
            "Cupid's bow portrait": "upper_lip_philtral_contour",
            "adult décolletage fashion": "decolletage_neckline_exposure",
            "adult hip dip side view": "lateral_waist_hip_contour_transition",
            "adult Dimples of Venus back view": "posterior_lumbosacral_landmarks",
            "contrapposto": "contrapposto_weight_shift",
            "body-bounded negative space between arm and waist": "body_bounded_negative_space",
            "Hogarth line of beauty": "hogarth_waving_line_of_beauty",
            "Hogarth serpentine line": "hogarth_serpentine_line_of_grace",
            "adult hourglass silhouette": "hourglass_silhouette_relation",
        }
        for text, profile_id in positives.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {profile_id})

        for text in (
            "V-line",
            "S-line",
            "swan neck",
            "비너스의 언덕",
            "beautiful female body",
            "attractive thighs",
            "shapely thighs",
            "negative space between arm and waist",
        ):
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_waving_and_serpentine_lines_keep_distinct_visual_owners(self):
        waving = self.profiles["hogarth_waving_line_of_beauty"]
        serpentine = self.profiles["hogarth_serpentine_line_of_grace"]
        self.assertIn("planar", waving["semantics"]["definition"])
        self.assertIn("three-dimensional", serpentine["semantics"]["definition"])
        self.assertIn(
            "occlusion_reappearance",
            serpentine["semantics"]["component_semantics"]["required_group_ids"],
        )
        self.assertNotIn(
            "occlusion_reappearance",
            waving["semantics"]["component_semantics"]["required_group_ids"],
        )

    def test_thigh_gap_uses_closed_straight_stance_and_neutral_inference(self):
        profile = self.profiles["inner_thigh_negative_space"]
        joined = json.dumps(profile, ensure_ascii=False)
        self.assertIn("feet touching", joined)
        self.assertIn("crossed_leg_accidental_opening", profile["reject_substitutes"])
        self.assertNotIn(
            "appeal_emphasis_phrase",
            profile["required_evidence_fields"],
        )
        for broad_term in ("attractive thighs", "shapely thighs", "각선미 강조"):
            self.assertNotIn(broad_term, profile["semantics"]["paraphrase_examples"])
        claim_limits = " ".join(profile["semantics"]["claim_limits"])
        for inference in ("health", "weight", "body fat", "fertility", "gender", "value"):
            self.assertIn(inference, claim_limits)

    def test_candidate_pack_separates_landmarks_contours_pose_and_composition(self):
        expected_by_slot = {
            "anatomical_connection": {
                "philtral_columns_cupid_bow",
                "clavicle_supraclavicular_hollow",
                "decolletage_neckline_exposure_boundary",
                "intermammary_cleavage_boundary",
                "inframammary_crease_boundary",
                "linea_alba_navel_axis",
                "iliac_crest_side_landmark",
                "trochanteric_depression_hip_dip",
                "posterior_spinal_groove_lumbar_curve",
                "posterior_psis_dimples_pair",
                "inguinal_skin_crease",
                "infragluteal_crease_boundary",
                "calf_to_ankle_taper",
            },
            "silhouette_proportion": {
                "natural_hourglass_relation",
                "shoulder_to_waist_taper",
                "waist_to_hip_flare",
                "hip_to_outer_thigh_transition",
                "back_to_waist_curve",
                "waist_to_glute_transition",
            },
            "composition": {
                "arm_waist_triangle_negative_space",
                "bent_elbow_torso_negative_space",
                "hand_face_negative_space",
                "hogarth_waving_line_path",
                "hogarth_serpentine_depth_path",
                "contour_transition_sequence",
            },
            "body_framing": {
                "philtrum_lip_landmark_closeup",
                "clavicle_upper_chest_landmark_crop",
                "lumbosacral_back_landmark_crop",
                "waist_hip_transition_three_quarter_crop",
                "full_body_countertilt_pose_read",
            },
        }
        for slot, expected_ids in expected_by_slot.items():
            with self.subTest(slot=slot):
                self.assertTrue(expected_ids <= set(self.candidates[slot]))

        self.assertIn("straight support leg", self.candidates["body_pose"]["contrapposto_full_body"]["embedding_text"])
        self.assertIn("planar S rhythm", self.candidates["body_pose"]["editorial_s_curve_pose"]["embedding_text"])
        self.assertNotEqual(
            self.candidates["silhouette_proportion"]["natural_hourglass_relation"]["embedding_text"],
            self.candidates["silhouette_proportion"]["cinched_hourglass_waist"]["embedding_text"],
        )

    def test_research_evidence_is_approved_and_candidate_bound(self):
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        body_rows = [row for row in rows if row["id"].startswith("body_semantics_")]
        self.assertEqual(len(body_rows), 12)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in body_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["status"], "approved")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])

    def test_selected_pixel_cases_are_registry_bound_and_fail_closed(self):
        expected_profile_ids = {
            "contrapposto_weight_shift",
            "body_bounded_negative_space",
            "upper_lip_philtral_contour",
        }
        self.assertEqual(
            {case["profile_id"] for case in self.pixel_cases},
            expected_profile_ids,
        )
        self.assertEqual(len(self.pixel_cases), len(expected_profile_ids))

        for case in self.pixel_cases:
            with self.subTest(case_id=case["case_id"]):
                profile = self.profiles[case["profile_id"]]
                registry_gate_ids = [gate["id"] for gate in profile["render_gates"]]

                self.assertEqual(
                    case["schema_version"],
                    "photo-body-semantic-pixel-case/v1",
                )
                self.assertEqual(
                    self.hard_matches(case["activation_text"]),
                    {case["profile_id"]},
                )
                self.assertEqual(case["required_gate_ids"], registry_gate_ids)
                self.assertEqual(
                    set(case["reject_substitutes"]),
                    set(profile["reject_substitutes"]),
                )
                self.assertEqual(
                    set(case["required_review_scales"]),
                    {"thumbnail", "native"},
                )
                self.assertEqual(
                    case["verdict_rule"],
                    {
                        "unit": "one_saved_image",
                        "pass": "all_required_gates_pass",
                        "partial_or_missing": "fail",
                        "prompt_presence_only": "insufficient",
                    },
                )
                self.assertEqual(
                    case["reference_image_role"],
                    "facial_appearance_only",
                )
                self.assertTrue(case["randomized_complex_concept_required"])
                self.assertTrue(case["non_activating_confusers"])
                self.assertTrue(case["neutrality_boundaries"])
                for confuser in case["non_activating_confusers"]:
                    self.assertEqual(self.hard_matches(confuser), set())

    def test_pixel_cases_cover_global_regional_and_local_visual_scales(self):
        self.assertEqual(
            {case["visual_scale"] for case in self.pixel_cases},
            {"global_full_body", "regional_composition", "local_surface_anatomy"},
        )
        cases = {case["profile_id"]: case for case in self.pixel_cases}
        self.assertEqual(
            cases["body_bounded_negative_space"]["target_region"],
            "arm_waist",
        )
        self.assertIn(
            "both feet visible",
            cases["contrapposto_weight_shift"]["observable_success_signals"],
        )
        self.assertIn(
            "paired upper-lip arc survives thumbnail review",
            cases["upper_lip_philtral_contour"]["observable_success_signals"],
        )


if __name__ == "__main__":
    unittest.main()
