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
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
EVIDENCE_PATH = ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
CASES_PATH = ROOT / "tests" / "fixtures" / "photo_prompt" / "face_shape_five_arm_cases_v1.jsonl"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "oval_face_contour_relation",
    "round_compact_face_relation",
    "oblong_elongated_face_relation",
    "square_face_contour_relation",
    "rectangular_face_contour_relation",
    "triangle_lower_face_dominant_relation",
    "diamond_zygomatic_dominant_relation",
    "upper_face_to_chin_taper_relation",
    "v_tapered_lower_face_relation",
    "u_rounded_lower_face_relation",
    "cjk_seed_face_relation",
}

DEFINITION_ONLY_IDS = {
    "v_tapered_lower_face_relation",
    "u_rounded_lower_face_relation",
    "cjk_seed_face_relation",
}

EXPECTED_CANDIDATES = {
    "face_shape_relation": PROFILE_IDS,
    "anatomical_connection": {
        "jawline_soft_tissue_contour",
        "zygomatic_cheek_plane",
        "forehead_width_relation",
        "forehead_height_hairline_span",
        "hairline_contour_shape",
        "temple_fullness_transition",
        "temporal_hollow_transition",
        "zygomatic_lateral_width",
        "malar_forward_projection",
        "cheek_soft_tissue_fullness",
        "subtle_cheek_hollow",
        "bigonial_width_relation",
        "gonial_angle_definition",
        "chin_width_tip_contour",
        "chin_vertical_length",
        "chin_sagittal_projection",
        "facial_thirds_landmark_span",
        "facial_profile_convexity",
    },
    "subject_framing": {
        "neutral_front_face_contour_read",
        "restrained_three_quarter_face_depth_read",
        "strict_profile_face_projection_read",
        "hair_clear_face_perimeter",
        "distortion_controlled_portrait_perspective",
        "neutral_expression_soft_form_light",
    },
}


class PhotoFaceShapeSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.index = prompt_generator.load_visual_profile_index(INDEX_PATH, cls.registry)
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

    def test_profiles_are_complete_relational_pixel_contracts(self) -> None:
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], False)
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertTrue(profile["reject_substitutes"])

    def test_exact_contextual_terms_route_to_one_profile(self) -> None:
        cases = {
            "oval face shape portrait": "oval_face_contour_relation",
            "둥근 얼굴형 인물사진": "round_compact_face_relation",
            "elongated face shape study": "oblong_elongated_face_relation",
            "사각형 얼굴형 정면 사진": "square_face_contour_relation",
            "rectangular face shape portrait": "rectangular_face_contour_relation",
            "pear-shaped face portrait": "triangle_lower_face_dominant_relation",
            "다이아몬드형 얼굴 정면": "diamond_zygomatic_dominant_relation",
            "heart-shaped face portrait": "upper_face_to_chin_taper_relation",
            "V-line face portrait": "v_tapered_lower_face_relation",
            "U라인 얼굴 정면 사진": "u_rounded_lower_face_relation",
            "瓜子脸 人像摄影": "cjk_seed_face_relation",
            "鹅蛋脸 portrait": "oval_face_contour_relation",
        }
        for text, expected_id in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected_id})

    def test_non_face_homonyms_bare_letters_and_single_cues_fail_closed(self) -> None:
        cases = (
            "oval body silhouette",
            "oval mirror product photograph",
            "round mirror in a square room",
            "square picture frame",
            "rectangular doorway",
            "pear fruit still life",
            "triangle logo",
            "diamond necklace portrait",
            "heart icon on a poster",
            "long face after bad news",
            "V-line",
            "V-neckline fashion portrait",
            "inguinal V-line anatomy",
            "U-line",
            "U-shaped pipe",
            "광대 clown makeup",
            "full cheeks",
            "pointed chin",
            "high cheekbones",
            "wide jaw",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_width_projection_and_global_local_boundaries_are_explicit(self) -> None:
        diamond = json.dumps(
            self.profiles["diamond_zygomatic_dominant_relation"], ensure_ascii=False
        )
        round_face = json.dumps(
            self.profiles["round_compact_face_relation"], ensure_ascii=False
        )
        v_face = json.dumps(
            self.profiles["v_tapered_lower_face_relation"], ensure_ascii=False
        )
        seed_face = json.dumps(
            self.profiles["cjk_seed_face_relation"], ensure_ascii=False
        )
        self.assertIn("lateral zygomatic region is clearly widest", diamond)
        self.assertIn("high_cheekbone_projection_only", diamond)
        self.assertIn("full_cheeks_only", round_face)
        self.assertIn("pointed_chin_only", v_face)
        self.assertIn("egg_oval_without_stronger_lower_taper", seed_face)

    def test_sensitive_cultural_and_letter_labels_are_definition_only(self) -> None:
        for profile_id in DEFINITION_ONLY_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                runtime = profile["runtime_expression"]
                self.assertEqual(runtime["default_mode"], "definition_only")
                self.assertEqual(runtime["prompt_label_terms"], [])
                exact_terms = set(profile["activation"]["exact_terms"])
                self.assertTrue(exact_terms <= set(runtime["forbidden_prompt_terms"]))
                self.assertTrue(exact_terms <= set(runtime["runtime_forbidden_labels"]))

    def test_embedding_only_component_paraphrase_remains_optional(self) -> None:
        target_id = "cjk_seed_face_relation"
        vectors = {
            profile["id"]: ([1.0, 0.0] if profile["id"] == target_id else [0.0, 1.0])
            for profile in self.registry["profiles"]
        }
        fake_index = prompt_generator.build_visual_profile_index_payload(
            self.registry,
            vectors=vectors,
            dimensions=2,
        )
        paraphrase = (
            "the complete hairline temple cheek jaw and chin perimeter remains visible; "
            "the upper and middle face are moderately longer than wide; the cheek region "
            "is wider than the jaw; the jaw narrows more strongly and smoothly into a "
            "small chin; egg oval V-line surgery ethnicity and beauty value do not "
            "substitute for those visible relations"
        )
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "authorial_core_interpretation",
                    "text": paraphrase,
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text="component-only face contour calibration",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        hit = next(
            row for row in resolution["hits"] if row["profile_id"] == target_id
        )
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_generated_index_is_registry_bound_for_all_face_profiles(self) -> None:
        exact_by_profile = {
            profile_id: {
                row["term"]
                for row in self.index["exact_lookup"]
                if row["profile_id"] == profile_id
            }
            for profile_id in PROFILE_IDS
        }
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                self.assertIn(profile_id, self.index["entries"])
                self.assertEqual(
                    exact_by_profile[profile_id],
                    set(self.profiles[profile_id]["activation"]["exact_terms"]),
                )

    def test_profiles_do_not_encode_fixed_numeric_face_ideals(self) -> None:
        numeric_threshold = re.compile(
            r"\b\d+(?:\.\d+)?\s*(?:%|cm|mm|degrees?|ratio)\b",
            re.IGNORECASE,
        )
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                payload = json.dumps(self.profiles[profile_id], ensure_ascii=False)
                self.assertIsNone(numeric_threshold.search(payload))
                self.assertNotIn("universally ideal", payload.casefold())

    def test_candidate_pack_covers_global_regional_and_observability_axes(self) -> None:
        for slot, expected_ids in EXPECTED_CANDIDATES.items():
            with self.subTest(slot=slot):
                self.assertTrue(expected_ids <= set(self.candidates[slot]))
        self.assertIn("face_shape_relation", self.tags["slot_pick_order"])
        self.assertIn("face_shape_relation", self.tags["slot_priorities"])
        self.assertNotIn("face_shape_relation", json.dumps(self.tags["presets"]))

    def test_research_evidence_is_approved_and_candidate_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        face_rows = [row for row in rows if row["id"].startswith("face_shape_semantics_")]
        self.assertEqual(len(face_rows), 13)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in face_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertEqual(row["domain"], "face_shape_visual_semantics")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])

    def test_five_arm_cases_are_distinct_and_hash_bound(self) -> None:
        self.assertEqual(len(self.pixel_cases), 5)
        self.assertEqual(len({row["arm_id"] for row in self.pixel_cases}), 5)
        self.assertEqual(len({row["concept_seed"] for row in self.pixel_cases}), 5)
        self.assertEqual(len({row["concept_domain"] for row in self.pixel_cases}), 5)
        self.assertEqual(len({row["target_profile_id"] for row in self.pixel_cases}), 5)
        for row in self.pixel_cases:
            with self.subTest(arm_id=row["arm_id"]):
                self.assertIn(row["target_profile_id"], PROFILE_IDS)
                self.assertEqual(row["reference"]["role"], "appearance_reference")
                self.assertEqual(
                    row["reference"]["sha256"],
                    "e3e010b75a48da02f914d7e8202690b3353450a78832daaefea0bbbc234aa5b3",
                )
                self.assertIn("not biometric identity verification", row["reference"]["boundary"])
                profile_gate_ids = {
                    gate["id"]
                    for gate in self.profiles[row["target_profile_id"]]["render_gates"]
                }
                self.assertEqual(set(row["expected_gate_ids"]), profile_gate_ids)


if __name__ == "__main__":
    unittest.main()
