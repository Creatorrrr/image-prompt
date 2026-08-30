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
    / "pose_semantics_five_arm_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_CONTRACTS = {
    "figura_serpentinata_spiral_pose": {
        "required_groups": {
            "support_initiator",
            "segment_opposition",
            "arm_head_counterturn",
            "three_dimensional_read",
        },
        "gate_ids": {
            "vo_serpentinata_support_initiator",
            "vo_serpentinata_segment_opposition",
            "vo_serpentinata_head_arm_counterturn",
            "vo_serpentinata_three_dimensional_read",
        },
    },
    "tribhanga_three_bend_pose": {
        "required_groups": {
            "inclined_head",
            "opposing_middle_bend",
            "bent_knee_return",
            "alternating_three_bend_rhythm",
        },
        "gate_ids": {
            "vo_tribhanga_inclined_head",
            "vo_tribhanga_opposing_middle_bend",
            "vo_tribhanga_bent_knee_return",
            "vo_tribhanga_full_body_three_bend_read",
        },
    },
}


class PhotoPoseVisualSemanticsTests(unittest.TestCase):
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

    def test_hard_profiles_are_componentized_and_pixel_testable(self) -> None:
        for profile_id, contract in PROFILE_CONTRACTS.items():
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertEqual(
                    set(components["required_group_ids"]),
                    contract["required_groups"],
                )
                self.assertEqual(
                    components["minimum_component_groups"],
                    len(contract["required_groups"]),
                )
                self.assertGreaterEqual(len(profile["required_evidence_fields"]), 4)
                self.assertEqual(
                    {gate["id"] for gate in profile["render_gates"]},
                    contract["gate_ids"],
                )
                self.assertTrue(
                    {"thumbnail", "both"}
                    <= {gate["review_scale"] for gate in profile["render_gates"]}
                )

    def test_exact_terms_activate_without_broad_pose_aliases(self) -> None:
        positives = {
            "figura serpentinata full-body photo": "figura_serpentinata_spiral_pose",
            "피구라 세르펜티나타 전신 포즈": "figura_serpentinata_spiral_pose",
            "tribhaṅga editorial pose": "tribhanga_three_bend_pose",
            "트리방가 자세": "tribhanga_three_bend_pose",
        }
        for text, profile_id in positives.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {profile_id})

        for text in (
            "hip pop",
            "pelvic tilt",
            "generic torso twist",
            "editorial S-line pose",
            "C-line pose",
            "beautiful feminine pose",
            "sensual elegant stance",
            "Hogarth serpentine line",
            "a serpentine road",
            "Indian-inspired costume portrait",
            "contrapposto",
        ):
            with self.subTest(text=text):
                self.assertTrue(
                    self.hard_matches(text).isdisjoint(PROFILE_CONTRACTS),
                    text,
                )

    def test_candidate_pack_has_distinct_pose_orientation_and_wrist_atoms(self) -> None:
        expected_by_slot = {
            "body_pose": {
                "figura_serpentinata_full_body",
                "tribhanga_three_bend_full_body",
                "single_arc_c_curve_pose",
                "pelvic_obliquity_single_support",
                "staggered_leg_depth_separation",
                "crossed_ankles_narrow_base",
                "lower_limb_plantarflexed_line",
                "perched_edge_sit_grounded_support",
                "propped_elbow_recline_support",
                "casual_lean_against_wall",
                "walking_mid_stride_pose",
            },
            "body_orientation": {
                "thorax_pelvis_opposed_azimuth",
                "axial_elongation_relaxed_shoulders",
                "head_shoulder_opposition",
            },
            "hand_pose": {"relaxed_wrist_offset_line"},
        }
        for slot, expected_ids in expected_by_slot.items():
            with self.subTest(slot=slot):
                self.assertTrue(expected_ids <= set(self.candidates[slot]))

        self.assertIn(
            "frontal plane",
            self.candidates["body_pose"]["pelvic_obliquity_single_support"]["embedding_text"],
        )
        self.assertIn(
            "different depth azimuths",
            self.candidates["body_orientation"]["thorax_pelvis_opposed_azimuth"]["embedding_text"],
        )
        self.assertIn(
            "stance leg",
            self.candidates["body_pose"]["walking_mid_stride_pose"]["embedding_text"],
        )
        self.assertIn(
            "joint stays anatomically continuous",
            self.candidates["hand_pose"]["relaxed_wrist_offset_line"]["embedding_text"],
        )

    def test_pose_research_evidence_is_approved_and_candidate_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        pose_rows = [row for row in rows if row["id"].startswith("pose_semantics_")]
        self.assertEqual(len(pose_rows), 6)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in pose_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["status"], "approved")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])

    def test_five_arm_pixel_fixture_binds_registry_and_atomic_gates(self) -> None:
        self.assertEqual(len(self.pixel_cases), 5)
        self.assertEqual(
            {case["arm_id"] for case in self.pixel_cases},
            {"arm-01", "arm-02", "arm-03", "arm-04", "arm-05"},
        )
        all_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for case in self.pixel_cases:
            with self.subTest(case_id=case["case_id"]):
                self.assertEqual(
                    case["schema_version"],
                    "photo-pose-semantic-pixel-case/v1",
                )
                self.assertTrue(case["randomized_complex_concept_required"])
                self.assertEqual(case["reference_image_role"], "facial_appearance_only")
                self.assertTrue(set(case["candidate_ids"]) <= all_candidates)
                self.assertGreaterEqual(len(case["atomic_pixel_gates"]), 2)
                self.assertEqual(
                    case["verdict_rule"],
                    {
                        "unit": "one_saved_image",
                        "pass": "all_registry_and_atomic_gates_pass",
                        "partial_or_missing": "fail",
                        "prompt_presence_only": "insufficient",
                    },
                )
                profile_id = case["registry_profile_id"]
                if profile_id is None:
                    self.assertEqual(case["registry_gate_ids"], [])
                else:
                    profile = self.profiles[profile_id]
                    self.assertEqual(
                        case["registry_gate_ids"],
                        [gate["id"] for gate in profile["render_gates"]],
                    )
                    self.assertEqual(
                        self.hard_matches(case["activation_text"]),
                        {profile_id},
                    )


if __name__ == "__main__":
    unittest.main()
