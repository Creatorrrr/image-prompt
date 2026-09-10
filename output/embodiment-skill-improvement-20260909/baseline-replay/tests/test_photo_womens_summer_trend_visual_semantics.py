from __future__ import annotations

import hashlib
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
RESEARCH_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "womens-summer-trends-20260901"
    / "source-research.md"
)
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "womens_summer_trend_pixel_test_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "capri_trouser_below_knee_clear_ankle_gap",
    "gathered_ankle_voluminous_trouser",
    "balloon_curved_leg_tapered_hem",
    "wrap_skirt_overlap_closure",
    "lace_trim_attached_edge",
    "jelly_footwear_molded_translucent_surface",
}

EXPECTED_CANDIDATES = {
    "wardrobe_style": {
        "fitted_tank_capri_low_profile_flat_ensemble",
        "fitted_top_harem_low_profile_ensemble",
        "fitted_top_balloon_trouser_ensemble",
        "simple_top_wrap_skirt_ensemble",
        "lace_trim_camisole_wide_denim_ensemble",
        "tank_lightweight_summer_layer_wide_trouser_ensemble",
        "fitted_top_bermuda_slim_belt_ensemble",
    },
    "garment_detail": {
        "lace_trim_edge",
        "harem_gathered_waist_ankle_cuff",
        "balloon_leg_curve_tapered_hem",
        "wrap_skirt_diagonal_overlap_closure",
    },
    "silhouette_proportion": {
        "casual_capri_below_knee_clear_ankle_gap",
        "harem_roomy_folds_gathered_ankles",
        "balloon_convex_leg_tapered_hem_silhouette",
        "fitted_top_voluminous_bottom_contrast",
        "bermuda_two_knee_length_short_hems",
    },
    "footwear": {
        "colorful_jelly_shoes",
        "low_profile_ballet_flat_topology",
        "thong_sandal_toe_post_topology",
    },
    "surface_material": {
        "lace_fabric_surface",
        "molded_translucent_jelly_footwear_surface",
        "lightweight_open_knit_layer_surface",
    },
    "wearable_accessory": {
        "narrow_lace_scarf_openwork_strip",
        "small_studded_dailywear_accessory",
        "clear_jelly_bag_charm_system",
    },
    "color": {"neutral_base_single_lemon_accent"},
}


class PhotoWomensSummerTrendVisualSemanticsTests(unittest.TestCase):
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
        all_gate_ids = {
            gate["id"]
            for profile in self.registry["profiles"]
            for gate in profile["render_gates"]
        }
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
                self.assertEqual(
                    len({gate["id"] for gate in profile["render_gates"]}),
                    5,
                )
                self.assertTrue(
                    {gate["id"] for gate in profile["render_gates"]} <= all_gate_ids
                )

    def test_exact_terms_route_to_one_profile(self) -> None:
        cases = {
            "adult fashion editorial in capri pants": "capri_trouser_below_knee_clear_ankle_gap",
            "하렘팬츠를 입은 성인 여성 전신 화보": "gathered_ankle_voluminous_trouser",
            "curved balloon trousers in a studio fashion frame": "balloon_curved_leg_tapered_hem",
            "여름 랩스커트 데일리룩": "wrap_skirt_overlap_closure",
            "satin camisole with attached lace trim": "lace_trim_attached_edge",
            "투명한 젤리샌들을 신은 패션 사진": "jelly_footwear_molded_translucent_surface",
        }
        for text, expected_id in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected_id})

    def test_confounds_negation_and_adjacent_garments_fail_closed(self) -> None:
        cases = (
            "a caprine animal with horizontal pupils",
            "no capri pants; use full-length trousers",
            "Bermuda shorts ending at the knees",
            "straight wide trousers with open hems and no ankle gathering",
            "a round balloon prop beside ordinary straight trousers",
            "an asymmetrical skirt with one printed diagonal stripe",
            "a whole lace dress with no different base fabric",
            "a jellyfish motif printed on opaque leather boots",
            "clear knee-high rain boots",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_harem_balloon_capri_terms_remain_distinct(self) -> None:
        self.assertEqual(
            self.hard_matches("harem trousers"),
            {"gathered_ankle_voluminous_trouser"},
        )
        self.assertEqual(
            self.hard_matches("balloon pants"),
            {"balloon_curved_leg_tapered_hem"},
        )
        self.assertEqual(
            self.hard_matches("capri trousers"),
            {"capri_trouser_below_knee_clear_ankle_gap"},
        )

    def test_candidates_are_axis_owned_and_semantically_decomposed(self) -> None:
        for slot, candidate_ids in EXPECTED_CANDIDATES.items():
            self.assertTrue(candidate_ids <= set(self.candidates[slot]))
            for candidate_id in candidate_ids:
                with self.subTest(slot=slot, candidate_id=candidate_id):
                    candidate = self.candidates[slot][candidate_id]
                    self.assertTrue(candidate.get("aliases"))
                    self.assertTrue(candidate.get("keywords"))
                    self.assertGreaterEqual(
                        len(candidate.get("embedding_text", "").split()),
                        8,
                    )
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
        target_id = "gathered_ankle_voluminous_trouser"
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
            query_text="roomy trouser folds tapering into two gathered ankle cuffs",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        hit = next(row for row in resolution["hits"] if row["profile_id"] == target_id)
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_registry_bound_payload_contains_exact_lookup_for_profiles(self) -> None:
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
        summer_rows = [row for row in rows if row["id"].startswith("summer_kr_")]
        self.assertEqual(len(summer_rows), 8)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in summer_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertEqual(
                    row["domain"],
                    "womens_summer_dailywear_visual_semantics",
                )
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])

    def test_three_arm_pixel_cases_bind_profiles_cores_and_reference(self) -> None:
        self.assertEqual(len(self.pixel_cases), 3)
        self.assertEqual(len({row["arm_id"] for row in self.pixel_cases}), 3)
        self.assertEqual(
            {row["profile_id"] for row in self.pixel_cases},
            {
                "capri_trouser_below_knee_clear_ankle_gap",
                "gathered_ankle_voluminous_trouser",
                "lace_trim_attached_edge",
            },
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
                self.assertIn("not identity", row["reference"]["boundary"])
                self.assertEqual(
                    set(row["required_gate_ids"]),
                    {gate["id"] for gate in profile["render_gates"]},
                )
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")
                for path_key, hash_key in (
                    ("request_envelope_path", "request_envelope_file_sha256"),
                    ("authorial_core_path", "authorial_core_file_sha256"),
                ):
                    artifact = ROOT / row[path_key]
                    self.assertTrue(artifact.is_file())
                    self.assertEqual(
                        hashlib.sha256(artifact.read_bytes()).hexdigest(),
                        row[hash_key],
                    )

    def test_research_note_keeps_nonvisual_and_identity_boundaries(self) -> None:
        note = RESEARCH_PATH.read_text(encoding="utf-8")
        for phrase in (
            "Popularity evidence decides what to prioritize",
            "not infer identity, same-person status, biometrics",
            "hidden bra cups",
            "cooling, UV blocking, waterproofing",
            "partial or missing hard gate is a failed arm",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, note)


if __name__ == "__main__":
    unittest.main()
