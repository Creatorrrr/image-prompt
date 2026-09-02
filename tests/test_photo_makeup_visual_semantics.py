from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EVIDENCE_PATH = ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "makeup_semantics_routing_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "no_makeup_makeup_layering",
    "smoky_eye_diffused_gradient",
    "cut_crease_lid_separation",
    "graphic_negative_space_eyeliner",
    "glass_skin_specular_diffuse_balance",
    "gradient_lip_center_distribution",
    "sunburn_blush_cross_face_distribution",
    "contour_highlight_cosmetic_sculpting",
}

MODULAR_SLOT_IDS = {
    "complexion_coverage": {
        "sheer_translucent_complexion_coverage",
        "sheer_complexion_texture_preservation",
        "light_selective_complexion_evening",
        "medium_buildable_complexion_coverage",
        "full_opaque_complexion_coverage",
        "selective_spot_concealment",
    },
    "eyeshadow_style": {
        "smoky_lashline_diffused_gradient",
        "cut_crease_lid_separation",
        "halo_eye_center_lid_focus",
        "monochrome_diffused_lid_wash",
        "lower_lid_smoke_color_focus",
        "inner_corner_lid_highlight",
    },
    "eye_makeup_line": {
        "graphic_floating_eyeliner",
        "smudged_soft_grunge_liner",
        "classic_tapered_wing_liner",
        "clean_interlash_tightline",
        "lower_waterline_kohl_liner",
    },
    "lash_style": {
        "clean_separated_defined_lashes",
        "soft_volumized_fanned_lashes",
        "elongated_outer_corner_lashes",
        "wet_clustered_editorial_lashes",
        "colored_mascara_accent",
        "lower_lash_statement_detail",
    },
    "cheek_makeup": {
        "soft_apple_cheek_blush",
        "cheekbone_to_temple_blush_drape",
        "across_nose_sunburn_blush",
        "under_eye_high_cheek_blush",
        "diffused_low_cheek_blush",
        "muted_monochrome_cheek_wash",
    },
    "face_sculpting": {
        "matte_plane_contour_blend",
        "balanced_contour_highlight_dimension",
        "luminous_strobing_high_points",
        "soft_bronzed_perimeter_warmth",
        "minimal_nose_bridge_contour_highlight",
    },
    "makeup_decoration": {
        "micro_crystal_face_gem_constellation",
        "graphic_decal_face_applique",
        "metallic_foil_eye_accent",
        "hand_painted_geometric_face_motif",
        "cosmetic_freckle_dot_scatter",
    },
    "lip_color_placement": {
        "center_saturated_gradient_lip",
        "uniform_full_lip_color_coverage",
        "softly_diffused_vermilion_edge",
        "crisp_vermilion_lip_line",
        "two_tone_ombre_lip_transition",
    },
    "lip_finish": {
        "soft_blur_matte_lip_finish",
        "natural_balm_lip_sheen",
        "stained_soft_matte_lip_finish",
        "high_shine_glossy_lip",
        "satin_creme_lip_finish",
    },
    "makeup_wear_state": {
        "fresh_precise_makeup_application",
        "softly_lived_in_makeup_edges",
        "rain_softened_eye_makeup",
        "tear_track_through_cosmetics",
        "patchy_transferred_foundation_wear",
        "faded_lip_center_wear",
    },
}


class PhotoMakeupVisualSemanticsTests(unittest.TestCase):
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
        cls.routing_cases = [
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

    def test_makeup_profiles_are_component_and_pixel_contracts(self) -> None:
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], False)
                self.assertTrue(
                    profile["activation"]["semantic_discovery_requires_component_evidence"]
                )
                self.assertGreaterEqual(components["minimum_component_groups"], 4)
                self.assertGreaterEqual(len(components["required_group_ids"]), 4)
                self.assertGreaterEqual(len(profile["required_evidence_fields"]), 4)
                self.assertGreaterEqual(len(profile["render_gates"]), 4)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertTrue(profile["reject_substitutes"])

    def test_exact_terms_route_and_confusers_or_negations_fail_closed(self) -> None:
        for case in self.routing_cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(
                    self.hard_matches(case["text"]),
                    set(case["expected_profile_ids"]),
                )

    def test_definition_only_profiles_hide_ambiguous_or_value_loaded_labels(self) -> None:
        definition_only = {
            "no_makeup_makeup_layering",
            "glass_skin_specular_diffuse_balance",
            "sunburn_blush_cross_face_distribution",
        }
        for profile_id in definition_only:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                runtime = profile["runtime_expression"]
                exact_terms = set(profile["activation"]["exact_terms"])
                self.assertEqual(runtime["default_mode"], "definition_only")
                self.assertEqual(runtime["prompt_label_terms"], [])
                self.assertTrue(exact_terms <= set(runtime["forbidden_prompt_terms"]))
                self.assertTrue(exact_terms <= set(runtime["runtime_forbidden_labels"]))

    def test_embedding_only_component_paraphrase_remains_optional(self) -> None:
        target_id = "glass_skin_specular_diffuse_balance"
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
                        "broad low-contrast diffuse radiance covers the complexion; "
                        "localized specular highlights follow coherent high facial planes; "
                        "pores and natural skin microtexture remain visible; oily hotspots "
                        "plastic smoothing and overexposure do not substitute"
                    ),
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text="controlled luminous complexion optics",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        hit = next(row for row in resolution["hits"] if row["profile_id"] == target_id)
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_generated_index_is_registry_bound_for_every_makeup_profile(self) -> None:
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

    def test_candidate_pack_covers_each_independent_makeup_axis(self) -> None:
        for slot, expected_ids in MODULAR_SLOT_IDS.items():
            with self.subTest(slot=slot):
                self.assertEqual(set(self.candidates[slot]), expected_ids)
                self.assertIn(slot, self.tags["slot_pick_order"])
                self.assertIn(slot, self.tags["slot_priorities"])
                self.assertEqual(
                    self.tags["slot_applicability"]["slots"][slot]["subject_categories"],
                    ["human"],
                )
                self.assertTrue(
                    all(row.get("for_any") == ["human"] for row in self.candidates[slot].values())
                )

    def test_runtime_semantics_do_not_encode_demographic_or_beauty_values(self) -> None:
        forbidden = (
            "healthy",
            "youthful",
            "attractive",
            "flattering",
            "for women",
            "for men",
            "feminine face",
            "masculine face",
        )
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                payload = json.dumps(self.profiles[profile_id], ensure_ascii=False).casefold()
                self.assertFalse(any(term in payload for term in forbidden))
        for slot in MODULAR_SLOT_IDS:
            for entry in self.candidates[slot].values():
                with self.subTest(slot=slot, candidate_id=entry["id"]):
                    payload = json.dumps(entry, ensure_ascii=False).casefold()
                    self.assertFalse(any(term in payload for term in forbidden))

    def test_research_evidence_is_approved_source_bound_and_candidate_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        makeup_rows = [row for row in rows if row["domain"] == "makeup_visual_semantics"]
        self.assertEqual(len(makeup_rows), 13)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in makeup_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])


if __name__ == "__main__":
    unittest.main()
