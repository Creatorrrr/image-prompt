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
ROUTING_PATH = ROOT / "tests" / "fixtures" / "photo_prompt" / "visual_obligation_routing_v1.jsonl"
PIXEL_CASES_PATH = ROOT / "tests" / "fixtures" / "photo_prompt" / "humanlike_semantics_five_arm_cases_v1.jsonl"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "biological_human_clone_provenance",
    "human_cellular_chimera_lineage",
    "anthrobot_microscopic_ciliated_biobot",
    "human_digital_twin_bidirectional_sync",
    "biohybrid_robot_living_synthetic_integration",
}


class PhotoHumanlikeSemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.pixel_cases = [
            json.loads(line)
            for line in PIXEL_CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        cls.routing_cases = [
            payload
            for line in ROUTING_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
            for payload in [json.loads(line)]
            if any(
                marker in payload.get("id", "")
                for marker in (
                    "human_clone",
                    "human_chimera",
                    "anthrobot",
                    "human_digital_twin",
                    "biohybrid_robot",
                )
            )
        ]

    def test_five_profiles_have_independent_obligation_and_gate_ownership(self) -> None:
        profiles = {
            profile["id"]: profile
            for profile in self.registry["profiles"]
            if profile.get("id") in PROFILE_IDS
        }
        self.assertEqual(set(profiles), PROFILE_IDS)
        gate_sets = []
        for profile_id, profile in profiles.items():
            with self.subTest(profile_id=profile_id):
                self.assertGreaterEqual(len(profile["required_evidence_fields"]), 5)
                gates = {row["id"] for row in profile["render_gates"]}
                self.assertGreaterEqual(len(gates), 5)
                self.assertTrue(all(gate.startswith("vo_") for gate in gates))
                self.assertTrue(profile["activation"]["semantic_discovery_requires_component_evidence"])
                gate_sets.append(gates)
        for index, left in enumerate(gate_sets):
            for right in gate_sets[index + 1 :]:
                self.assertTrue(left.isdisjoint(right))

    def test_routing_pairs_keep_exact_profiles_hard_and_components_advisory(self) -> None:
        self.assertGreaterEqual(len(self.routing_cases), 25)
        for case in self.routing_cases:
            with self.subTest(case=case["id"]):
                rows = [{"source": "concept_lock", "text": case["text"], "polarity": "required"}]
                hard = prompt_generator.candidate_pack_auto_visual_obligation_matches(self.registry, rows)
                advisory = prompt_generator.candidate_pack_auto_visual_concept_matches(self.registry, rows)
                self.assertEqual(sorted(hard), sorted(case["expected_profile_ids"]))
                self.assertEqual(sorted(advisory), sorted(case["expected_candidate_profile_ids"]))

    def test_android_factory_candidate_no_longer_owns_plain_clone_tag(self) -> None:
        entry = next(
            row
            for row in self.tags["slots"]["subject"]
            if row.get("id") == "mass_production_line_clone_unit"
        )
        exact_values = {
            str(value).casefold()
            for field in ("tags", "aliases", "keywords")
            for value in entry.get(field, [])
        }
        self.assertNotIn("clone", exact_values)
        self.assertIn("android_clone", exact_values)
        self.assertIn("manufactured_duplicate", exact_values)

    def test_five_arm_pixel_cases_bind_exact_registry_gates(self) -> None:
        self.assertEqual(len(self.pixel_cases), 5)
        self.assertEqual({case["profile_id"] for case in self.pixel_cases}, PROFILE_IDS)
        for case in self.pixel_cases:
            with self.subTest(case=case["case_id"]):
                profile = prompt_generator.visual_obligation_profile_by_id(
                    self.registry,
                    case["profile_id"],
                )
                self.assertIsNotNone(profile)
                self.assertEqual(
                    case["required_gate_ids"],
                    [gate["id"] for gate in profile["render_gates"]],
                )
                self.assertTrue(case["randomized_complex_concept"])
                self.assertTrue(case["reference_image_role"])
                self.assertEqual(case["verdict_rule"]["pass"], "all_required_gates_pass")
                self.assertEqual(case["verdict_rule"]["partial_or_missing"], "fail")


if __name__ == "__main__":
    unittest.main()
