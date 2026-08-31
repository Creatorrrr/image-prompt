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
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "womens_casualwear_pixel_test_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "button_down_collar_fastening",
    "cold_shoulder_cutout_topology",
    "wrap_front_overlap_closure",
    "bifurcated_one_piece_jumpsuit",
    "culotte_cropped_wide_leg_topology",
}

EXPECTED_CANDIDATES = {
    "wardrobe_style": {
        "button_down_poplin_shirt_tailored_trousers",
        "cold_shoulder_knit_top_midi_skirt",
        "wrap_front_blouse_straight_trousers",
        "tailored_full_length_jumpsuit",
        "culotte_button_front_blouse",
    },
    "garment_detail": {
        "button_down_collar_point_fastening",
        "cold_shoulder_cutout_sleeve_bridge",
        "wrap_front_diagonal_overlap_tie",
        "jumpsuit_bodice_crotch_leg_continuity",
        "culotte_inseam_leg_separation",
        "skort_outer_panel_inner_shorts",
        "pleat_fold_ridge_valley_geometry",
    },
    "silhouette_proportion": {
        "cropped_wide_leg_culotte_geometry",
        "tailored_jumpsuit_continuous_line",
        "oversized_design_ease_relation",
        "cropped_hem_landmark_relation",
        "palazzo_full_length_wide_leg_geometry",
    },
    "surface_material": {
        "woven_poplin_crisp_fold_surface",
        "rib_knit_stretch_recovery_surface",
        "fluid_satin_luster_drape_surface",
        "lightweight_crepe_matte_drape_surface",
    },
}


class PhotoWomensCasualwearVisualSemanticsTests(unittest.TestCase):
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
                self.assertEqual(len(components["groups"]), 5)
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertEqual(len(profile["reject_substitutes"]), 5)

    def test_exact_terms_route_to_one_profile(self) -> None:
        cases = {
            "adult editorial in a button-down shirt": "button_down_collar_fastening",
            "콜드숄더 탑을 입은 성인 여성": "cold_shoulder_cutout_topology",
            "documentary portrait in a wrap-front blouse": "wrap_front_overlap_closure",
            "테일러드 점프수트 패션 화보": "bifurcated_one_piece_jumpsuit",
            "큐롯 팬츠를 입은 성인 여성": "culotte_cropped_wide_leg_topology",
        }
        for text, expected_id in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected_id})

    def test_confounds_and_non_garment_homonyms_fail_closed(self) -> None:
        cases = (
            "a generic button-up shirt with loose collar points",
            "give the colleague the cold shoulder during the meeting",
            "an off-shoulder top with no shoulder fabric bridges",
            "a plain blouse printed with one diagonal stripe",
            "matching top and trousers with a visible waistband gap",
            "a single-panel midi skirt with deep pleat shadows",
            "full-length palazzo trousers reaching the floor",
            "two buttons displayed beside a detached collar sample",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_candidates_are_axis_owned_and_semantically_decomposed(self) -> None:
        for slot, candidate_ids in EXPECTED_CANDIDATES.items():
            self.assertTrue(candidate_ids <= set(self.candidates[slot]))
            for candidate_id in candidate_ids:
                with self.subTest(slot=slot, candidate_id=candidate_id):
                    candidate = self.candidates[slot][candidate_id]
                    self.assertTrue(candidate.get("aliases"))
                    self.assertTrue(candidate.get("keywords"))
                    self.assertGreaterEqual(len(candidate.get("embedding_text", "").split()), 8)
                    self.assertIn("human", candidate.get("for_any", []))
        all_expected = set().union(*EXPECTED_CANDIDATES.values())
        actual_owner_count = {
            candidate_id: sum(
                candidate_id in self.candidates[slot]
                for slot in EXPECTED_CANDIDATES
            )
            for candidate_id in all_expected
        }
        self.assertEqual(set(actual_owner_count.values()), {1})

    def test_embedding_only_component_paraphrase_remains_optional(self) -> None:
        target_id = "wrap_front_overlap_closure"
        component_context = "; ".join(
            group["any_terms"][0]
            for group in self.profiles[target_id]["semantics"]["component_semantics"]["groups"]
        )
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
                    "text": component_context,
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text="component-only crossed front-panel garment topology",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        hit = next(row for row in resolution["hits"] if row["profile_id"] == target_id)
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_registry_bound_payload_contains_exact_lookup_for_all_profiles(self) -> None:
        vectors = {
            profile["id"]: [float(index + 1), 1.0]
            for index, profile in enumerate(self.registry["profiles"])
        }
        index = prompt_generator.build_visual_profile_index_payload(
            self.registry,
            vectors=vectors,
            dimensions=2,
        )
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
        casualwear_rows = [
            row for row in rows if row["id"].startswith("casualwear_semantics_")
        ]
        self.assertEqual(len(casualwear_rows), 4)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in casualwear_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertEqual(row["domain"], "womens_casualwear_visual_semantics")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])

    def test_five_arm_pixel_cases_bind_all_profile_gates_and_reference(self) -> None:
        self.assertEqual(len(self.pixel_cases), 5)
        self.assertEqual(len({row["arm_id"] for row in self.pixel_cases}), 5)
        self.assertEqual(
            {row["profile_id"] for row in self.pixel_cases},
            PROFILE_IDS,
        )
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
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")


if __name__ == "__main__":
    unittest.main()
