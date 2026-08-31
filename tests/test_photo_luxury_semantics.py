from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
RECIPES_PATH = SKILL_DIR / "assets" / "concept_recipes.json"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
EVIDENCE_PATH = (
    ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generate_photo_prompt  # noqa: E402
import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


EXPECTED_BY_SLOT = {
    "action": {
        "hand_saddle_stitching_full_grain_leather",
        "weaving_leather_strips_by_hand",
        "hand_cutting_individual_paper_pattern",
        "fitting_basted_toile_on_client",
        "draping_and_hand_finishing_couture_layers",
        "building_reinforced_travel_case_frame",
        "setting_matched_gemstones_under_magnification",
        "hand_finishing_mechanical_watch_bridges",
        "private_advisor_curating_small_selection",
        "comparing_archive_sample_with_new_iteration",
        "inspecting_material_junction_and_finish",
    },
    "capture_context": {
        "luxury_atelier_process_documentary",
        "material_finish_macro_editorial",
        "brand_neutral_house_code_editorial",
        "private_appointment_service_capture",
        "archive_reinterpretation_material_study",
    },
    "prop": {
        "leather_clamp_two_needle_setup",
        "individual_paper_pattern_chalk_set",
        "basted_toile_dress_form_prop",
        "woven_leather_sample_panel",
        "reinforced_travel_case_corner_sample",
        "matched_gemstone_setting_layout_tray",
        "open_mechanical_movement_loupe_prop",
        "curated_private_viewing_tray",
        "blank_aftercare_restoration_folder",
        "archive_sample_new_iteration_pair",
    },
    "location": {
        "couture_atelier_fitting_room",
        "bespoke_tailoring_cutting_room",
        "leather_artisan_workbench",
        "heritage_travel_case_workshop",
        "high_jewelry_setting_bench",
        "fine_watchmaking_finishing_bench",
        "private_client_material_salon",
        "architectural_material_gallery_salon",
        "grand_gilded_mirror_salon",
    },
    "narrative_phase": {
        "luxury_raw_material_selection_phase",
        "pattern_toile_development_phase",
        "hand_assembly_craft_phase",
        "surface_finishing_inspection_phase",
        "final_fitting_function_check_phase",
        "private_presentation_aftercare_phase",
    },
    "surface_material": {
        "full_grain_leather_natural_variation_surface",
        "hand_burnished_painted_leather_edge_surface",
        "fine_wool_cashmere_matte_pile_surface",
        "silk_tulle_embroidery_layer_surface",
        "handwoven_leather_grid_surface",
        "wood_canvas_leather_brass_travel_structure_surface",
        "precision_brushed_polished_metal_junction_surface",
        "gemstone_metal_setting_structure_surface",
        "gilded_marble_velvet_opulence_surface",
        "stone_wood_brass_precision_junction_surface",
    },
    "garment_detail": {
        "basted_toile_balance_and_fit_lines",
        "hand_canvassed_tailoring_interior",
        "couture_internal_support_and_drape_layers",
        "metiers_art_embroidery_attachment_detail",
    },
    "color": {
        "greige_camel_cream_quiet_palette",
        "obsidian_antique_gold_oxblood_palette",
        "pearl_ivory_champagne_gold_palette",
        "midnight_sapphire_platinum_palette",
    },
    "lighting": {
        "grazing_material_reveal_lighting",
        "controlled_gemstone_specular_lighting",
        "quiet_diffuse_material_gallery_lighting",
        "baroque_gilded_chiaroscuro_lighting",
    },
    "aesthetic_trend": {
        "quiet_luxury_aesthetic",
        "conspicuous_original_code_luxury_aesthetic",
        "craftsmanship_process_luxury_aesthetic",
        "heritage_reinterpretation_luxury_aesthetic",
        "heritage_travel_object_luxury_aesthetic",
        "couture_atelier_craft_aesthetic",
        "bespoke_tailoring_craft_aesthetic",
        "architectural_material_luxury_aesthetic",
        "baroque_opulent_luxury_aesthetic",
        "high_jewelry_craft_aesthetic",
        "fine_watchmaking_craft_aesthetic",
        "private_client_service_luxury_aesthetic",
    },
}

MIXIN_ROUTES = {
    "quiet luxury": "콰이어트 럭셔리",
    "conspicuous luxury": "컨스피큐어스 럭셔리",
    "luxury craftsmanship": "장인 공정 럭셔리",
    "reinterpreted heritage": "헤리티지 재해석 럭셔리",
    "trunk-maker aesthetic": "헤리티지 트래블 럭셔리",
    "haute couture": "쿠튀르 아틀리에",
    "bespoke tailoring": "비스포크 테일러링",
    "architectural luxury": "건축적 소재 럭셔리",
    "baroque luxury": "바로크 오퓰런트 럭셔리",
    "high jewelry": "하이 주얼리 크래프트",
    "fine watchmaking": "파인 워치메이킹",
    "private client luxury": "프라이빗 클라이언트 럭셔리",
}

PROFILE_ROUTES = {
    "quiet luxury": "low_brand_prominence_material_luxury",
    "conspicuous luxury": "conspicuous_original_house_code_display",
    "haute couture": "couture_atelier_individual_construction",
    "bespoke tailoring": "bespoke_tailoring_individual_pattern",
    "trunk-maker aesthetic": "heritage_travel_object_construction",
    "high jewelry": "high_jewelry_setting_integration",
    "fine watchmaking": "fine_watchmaking_mechanical_finishing",
    "private client luxury": "private_client_service_interaction",
}

NEW_EVIDENCE_IDS = {
    "luxury_brand_prominence_quiet_conspicuous",
    "luxury_couture_fhcm_individual_atelier",
    "luxury_bespoke_savile_row_individual_pattern",
    "luxury_leather_saddle_stitch_hermes_process",
    "luxury_woven_leather_bottega_intrecciato_boundary",
    "luxury_fine_wool_loro_piana_material_boundary",
    "luxury_travel_case_louis_vuitton_construction",
    "luxury_gemstone_setting_gia_structure",
    "luxury_watchmaking_fhh_finish_function",
    "luxury_private_clienteling_mckinsey_service",
    "luxury_baroque_vam_integrated_movement",
    "luxury_modern_material_moma_mies_planes",
    "luxury_craftsmanship_unesco_skill_transmission",
}


class PhotoLuxurySemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.recipes = json.loads(RECIPES_PATH.read_text(encoding="utf-8"))
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
        }

    def explain(self, concept: str, seed: int = 17):
        _args, explanations = generate_photo_prompt.resolve_concepts(
            ["--seed", str(seed), "--selection-mode", "rule", "--emit-candidate-pack"],
            [concept],
        )
        self.assertEqual(len(explanations), 1)
        return explanations[0]

    def hard_visual_matches(self, text: str) -> list[str]:
        matches = prompt_generator.candidate_pack_auto_visual_obligation_matches(
            self.registry,
            [
                {
                    "source": "concept_lock",
                    "text": text,
                    "polarity": "required",
                    "priority": "critical",
                    "mandatory": True,
                }
            ],
        )
        return sorted(matches)

    def test_research_candidates_exist_in_expected_slots_without_rank_fields(self):
        for slot, expected_ids in EXPECTED_BY_SLOT.items():
            with self.subTest(slot=slot):
                self.assertLessEqual(expected_ids, set(self.by_slot[slot]))
                for candidate_id in expected_ids:
                    row = self.by_slot[slot][candidate_id]
                    self.assertTrue(row.get("en"))
                    self.assertTrue(row.get("ko"))
                    self.assertTrue(row.get("aliases"))
                    self.assertTrue(row.get("keywords"))
                    self.assertTrue(row.get("embedding_text"))
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)

    def test_precise_terms_route_mixins_while_broad_luxury_remains_unforced(self):
        for term, mixin_name in MIXIN_ROUTES.items():
            with self.subTest(term=term):
                explanation = self.explain(term)
                self.assertEqual(explanation["applied_mixins"], [mixin_name])
                self.assertTrue(explanation["forced_slots_applied"])
                self.assertGreaterEqual(
                    len(explanation["combined_forced_slots"]),
                    3,
                )

        for broad in ("luxury", "럭셔리", "명품", "luxury brand"):
            with self.subTest(broad=broad):
                explanation = self.explain(broad)
                self.assertEqual(explanation["applied_mixins"], [])
                self.assertEqual(explanation["combined_forced_slots"], {})
                self.assertEqual(self.hard_visual_matches(broad), [])

    def test_luxury_mixins_never_own_identity_body_or_real_brand_slots(self):
        forbidden_slots = {
            "subject",
            "appearance_type",
            "hair_color",
            "hair_style",
            "eye_color",
            "eye_shape",
            "body_type",
            "body_framing",
            "person_origin",
            "species_marker",
            "facial_structure",
        }
        for mixin_name in MIXIN_ROUTES.values():
            with self.subTest(mixin=mixin_name):
                mixin = self.recipes["mixins"][mixin_name]
                self.assertGreaterEqual(mixin["soft_min_anchors"], 3)
                self.assertFalse(set(mixin["set"]) & forbidden_slots)
                self.assertFalse(set(mixin.get("anchor_pool") or {}) & forbidden_slots)
                serialized = json.dumps(mixin, ensure_ascii=False).lower()
                for real_brand in (
                    "louis vuitton",
                    "hermès",
                    "hermes",
                    "chanel",
                    "gucci",
                    "cartier",
                    "rolex",
                ):
                    self.assertNotIn(real_brand, serialized)

    def test_eight_profiles_have_component_evidence_and_unique_pixel_gates(self):
        self.assertLessEqual(set(PROFILE_ROUTES.values()), set(self.profiles))
        gate_ids: list[str] = []
        for profile_id in PROFILE_ROUTES.values():
            with self.subTest(profile=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertTrue(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ]
                )
                self.assertGreaterEqual(len(components["required_group_ids"]), 4)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 4)
                gate_ids.extend(str(row["id"]) for row in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_exact_visual_routes_and_paired_negatives(self):
        for term, profile_id in PROFILE_ROUTES.items():
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), [profile_id])

        negatives = (
            "generic beige minimalism in an empty white room",
            "generic black and gold luxury hotel lobby",
            "finished runway gown glamour portrait",
            "well-fitted stock-pattern suit portrait",
            "decorative old suitcase with a random monogram",
            "loose gems and glitter on velvet",
            "smartwatch with a printed skeleton wallpaper",
            "empty marble lobby with champagne and a velvet rope",
        )
        for negative in negatives:
            with self.subTest(negative=negative):
                matches = set(self.hard_visual_matches(negative))
                self.assertTrue(matches.isdisjoint(PROFILE_ROUTES.values()))

    def test_research_evidence_is_approved_and_bound_to_existing_data(self):
        known_candidates = {
            str(row["id"])
            for rows in self.tags["slots"].values()
            for row in rows
            if isinstance(row, dict) and row.get("id")
        }
        rows = {
            row["id"]: row
            for row in (
                json.loads(line)
                for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
            if row["id"] in NEW_EVIDENCE_IDS
        }
        self.assertEqual(set(rows), NEW_EVIDENCE_IDS)
        for evidence_id, row in rows.items():
            with self.subTest(evidence=evidence_id):
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                for contract_id in row["affected_contract_ids"]:
                    kind, value = contract_id.split(":", 1)
                    if kind == "visual_obligation":
                        self.assertIn(value, self.profiles)
                    elif kind == "concept_recipe":
                        self.assertIn(value, self.recipes["mixins"])
                    else:
                        self.fail(f"unexpected contract kind: {contract_id}")

    def test_registry_schema_is_valid_after_generated_index_refresh(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
