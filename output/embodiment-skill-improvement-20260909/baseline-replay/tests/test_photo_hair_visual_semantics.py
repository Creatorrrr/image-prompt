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
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
EVIDENCE_PATH = ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
CASES_PATH = ROOT / "tests" / "fixtures" / "photo_prompt" / "hair_semantics_pixel_test_cases_v1.jsonl"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "two_block_disconnected_cut",
    "hime_cut_structural",
    "cornrow_scalp_row_topology",
    "locs_cord_structure",
    "bilateral_twin_tail_gather",
    "balayage_ribbon_color_placement",
    "wet_damp_clumped_hair_state",
}

EXPECTED_CANDIDATES = {
    "hair_style": {
        "two_block_korean_cut",
        "hime_cut",
        "cornrows",
        "dreadlocks",
        "bilateral_twin_tail_gather",
        "wet_damp_clumped_hair_state",
    },
    "hair_color": {"balayage_ribbon_color_placement"},
}


class PhotoHairVisualSemanticsTests(unittest.TestCase):
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
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
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

    def test_profiles_are_complete_five_group_pixel_contracts(self) -> None:
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], False)
                self.assertIs(
                    profile["activation"]["semantic_discovery_requires_component_evidence"],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertTrue(profile["reject_substitutes"])

    def test_exact_hair_terms_route_to_one_profile(self) -> None:
        cases = {
            "adult portrait with a two-block haircut": "two_block_disconnected_cut",
            "히메컷 헤어스타일 인물사진": "hime_cut_structural",
            "studio portrait with cornrow braids": "cornrow_scalp_row_topology",
            "adult portrait with locs hairstyle": "locs_cord_structure",
            "트윈테일 헤어를 한 성인 인물": "bilateral_twin_tail_gather",
            "editorial portrait with balayage hair": "balayage_ribbon_color_placement",
            "rain portrait with damp clumped hair": "wet_damp_clumped_hair_state",
        }
        for text, expected_id in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected_id})

    def test_homonyms_and_single_component_cues_fail_closed(self) -> None:
        cases = (
            "two blocks of concrete beside a wall",
            "a princess named Hime at court",
            "corn rows across an agricultural field",
            "database locks and file locks",
            "twin tails of two comets",
            "balayage paint technique on a canvas",
            "a wet-look leather jacket",
            "long hair with ordinary face-framing layers",
            "two ribbons clipped onto loose hair",
            "bright highlights on dry glossy hair",
            "one broad root-to-end color gradient",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_cultural_lineage_does_not_force_person_origin(self) -> None:
        for profile_id in (
            "two_block_disconnected_cut",
            "hime_cut_structural",
            "cornrow_scalp_row_topology",
            "locs_cord_structure",
        ):
            with self.subTest(profile_id=profile_id):
                serialized = json.dumps(self.profiles[profile_id], ensure_ascii=False)
                self.assertNotIn("person_origin", serialized)
                self.assertNotIn("ethnicity", self.profiles[profile_id]["category"])
        locs_runtime = self.profiles["locs_cord_structure"]["runtime_expression"]
        self.assertIn("locs hairstyle", locs_runtime["prompt_label_terms"])
        self.assertIn("dreadlocks", locs_runtime["runtime_forbidden_labels"])

    def test_candidates_are_axis_owned_and_semantically_decomposed(self) -> None:
        for slot, candidate_ids in EXPECTED_CANDIDATES.items():
            self.assertTrue(candidate_ids <= set(self.candidates[slot]))
            for candidate_id in candidate_ids:
                with self.subTest(slot=slot, candidate_id=candidate_id):
                    candidate = self.candidates[slot][candidate_id]
                    self.assertTrue(candidate.get("aliases"))
                    self.assertTrue(candidate.get("keywords"))
                    self.assertGreaterEqual(len(candidate.get("embedding_text", "").split()), 8)
        self.assertNotIn(
            "balayage_ribbon_color_placement",
            self.candidates["hair_style"],
        )
        self.assertIn(
            "balayage_ribbon_color_placement",
            self.candidates["hair_color"],
        )

    def test_embedding_only_component_paraphrase_remains_optional(self) -> None:
        target_id = "cornrow_scalp_row_topology"
        vectors = {
            profile["id"]: ([1.0, 0.0] if profile["id"] == target_id else [0.0, 1.0])
            for profile in self.registry["profiles"]
        }
        fake_index = prompt_generator.build_visual_profile_index_payload(
            self.registry,
            vectors=vectors,
            dimensions=2,
        )
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "authorial_core_interpretation",
                    "text": (
                        "multiple narrow braided ridges cover the scalp; "
                        "each row remains attached closely along the scalp; "
                        "clean scalp parting lanes separate adjacent rows; "
                        "the braided ridges follow continuous deliberate row paths; "
                        "two large Dutch braids and free box braids do not substitute"
                    ),
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text="component-only scalp braid topology",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        hit = next(
            row for row in resolution["hits"] if row["profile_id"] == target_id
        )
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_generated_index_is_registry_bound_for_all_hair_profiles(self) -> None:
        index = prompt_generator.load_visual_profile_index(INDEX_PATH, self.registry)
        exact_by_profile = {
            profile_id: {
                row["term"]
                for row in index["exact_lookup"]
                if row["profile_id"] == profile_id
            }
            for profile_id in PROFILE_IDS
        }
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                self.assertIn(profile_id, index["entries"])
                self.assertEqual(
                    exact_by_profile[profile_id],
                    set(self.profiles[profile_id]["activation"]["exact_terms"]),
                )

    def test_research_evidence_is_approved_and_candidate_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        hair_rows = [row for row in rows if row["id"].startswith("hair_semantics_")]
        self.assertEqual(len(hair_rows), 9)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in hair_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertEqual(row["domain"], "hair_visual_semantics")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])

    def test_five_arm_pixel_cases_bind_all_profile_gates_and_reference(self) -> None:
        self.assertEqual(len(self.pixel_cases), 5)
        self.assertEqual(len({row["arm_id"] for row in self.pixel_cases}), 5)
        self.assertEqual(len({row["profile_id"] for row in self.pixel_cases}), 5)
        for row in self.pixel_cases:
            with self.subTest(arm_id=row["arm_id"]):
                profile = self.profiles[row["profile_id"]]
                self.assertIs(row["randomized_complex_concept_required"], True)
                self.assertEqual(row["reference"]["role"], "appearance_reference")
                self.assertEqual(
                    row["reference"]["sha256"],
                    "3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea",
                )
                self.assertIn(
                    "not biometric identity verification",
                    row["reference"]["boundary"],
                )
                self.assertEqual(
                    set(row["required_gate_ids"]),
                    {gate["id"] for gate in profile["render_gates"]},
                )
                self.assertEqual(
                    row["verdict_rule"]["partial_or_missing"],
                    "fail",
                )


if __name__ == "__main__":
    unittest.main()
