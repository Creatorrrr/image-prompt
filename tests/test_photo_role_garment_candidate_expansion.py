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
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "research_evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generate_photo_prompt  # noqa: E402


class PhotoRoleGarmentCandidateExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.recipes = json.loads(RECIPES_PATH.read_text(encoding="utf-8"))
        cls.by_slot = {
            slot: {row["id"]: row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.presets = {row["id"]: row for row in cls.tags["presets"]}
        cls.evidence = {
            row["id"]: row
            for row in (
                json.loads(line)
                for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
        }

    def explain(self, concept: str, seed: int = 73) -> dict:
        _args, explanations = generate_photo_prompt.resolve_concepts(
            ["--selection-mode", "rule", "--seed", str(seed)],
            [concept],
            concept_mode="legacy",
        )
        self.assertEqual(len(explanations), 1)
        return explanations[0]

    def test_candidate_ids_and_presets_form_closed_slot_references(self) -> None:
        expected_by_slot = {
            "subject": {
                "aircraft_pilot_role_model",
                "military_uniform_duty_model",
                "armor_reference_adult_model",
                "revealing_armor_adult_model",
            },
            "costume_style": {
                "professional_aircraft_pilot_uniform",
                "professional_cabin_crew_uniform",
                "coordinated_school_uniform_system",
                "military_service_uniform_system",
                "military_field_uniform_system",
                "wearable_plate_mail_armor_system",
                "commercial_revealing_fantasy_armor",
            },
            "wardrobe_style": {
                "one_piece_a_line_dress",
                "one_piece_wrap_dress",
                "one_piece_shirt_dress",
                "sheer_opaque_overlay_garment",
                "sheer_panel_tailored_garment",
            },
            "adult_context": {
                "adult_original_fantasy_character_context",
                "adult_fashion_material_study_context",
            },
            "action": {
                "pilot_preflight_control_check",
                "pilot_taxi_instrument_crosscheck",
                "pilot_approach_control_scan",
                "cabin_emergency_equipment_check",
                "cabin_exit_crosscheck",
                "cabin_safety_demonstration",
                "school_uniform_component_inspection",
                "one_piece_drape_turnaround",
                "sheer_backlight_transmission_test",
                "military_uniform_duty_inspection",
                "armor_articulation_stance",
                "revealing_armor_design_turntable",
            },
            "prop": {
                "flight_controls_checklist_prop",
                "cabin_emergency_equipment_prop",
                "generic_fictional_insignia_set",
                "armor_articulation_detail_board",
            },
            "location": {
                "aircraft_flight_deck",
                "general_aviation_cockpit",
                "aircraft_cabin_exit_galley",
                "garment_design_studio",
                "textile_backlight_studio",
                "military_uniform_inspection_room",
                "fantasy_armor_campaign_studio",
            },
            "surface_material": {
                "sheer_organza_chiffon_transmission",
                "armor_plate_mail_leather_material",
            },
            "garment_detail": {
                "one_piece_continuous_bodice_to_hem",
                "one_piece_seam_closure_drape",
                "school_uniform_consistent_trim_system",
                "sheer_transmission_opaque_underlayer",
                "sheer_visible_edge_weave",
                "armor_articulated_overlap_attachment",
                "revealing_armor_deliberate_exposure_pattern",
                "revealing_armor_opaque_intimate_coverage",
            },
        }
        for slot, expected_ids in expected_by_slot.items():
            with self.subTest(slot=slot):
                self.assertTrue(expected_ids <= set(self.by_slot[slot]))

        expected_presets = {
            "aircraft_pilot_operation_portrait",
            "military_uniform_duty_editorial",
            "wearable_armor_reference_editorial",
            "commercial_revealing_fantasy_armor_editorial",
        }
        self.assertTrue(expected_presets <= set(self.presets))
        for preset_id in expected_presets | {"flight_attendant_service_portrait"}:
            with self.subTest(preset_id=preset_id):
                preset = self.presets[preset_id]
                self.assertTrue(preset["required_slots"])
                for slot, slot_filter in preset["filters"].items():
                    self.assertIn(slot, self.by_slot)
                    self.assertTrue(set(slot_filter.get("ids", [])) <= set(self.by_slot[slot]))

        cabin = self.presets["flight_attendant_service_portrait"]
        self.assertIn("prop", cabin["required_slots"])
        self.assertTrue(
            {
                "cabin_emergency_equipment_check",
                "cabin_exit_crosscheck",
                "cabin_safety_demonstration",
            }
            <= set(cabin["filters"]["action"]["ids"])
        )

    def test_recipes_route_roles_mixins_and_requester_glossary(self) -> None:
        pilot = self.explain("성인 파일럿 항공기 조종석")
        self.assertEqual(pilot["applied_role"], "파일럿")
        self.assertEqual(pilot["recipe"]["preset"], "aircraft_pilot_operation_portrait")
        self.assertIn(
            "aircraft_pilot_role_model",
            pilot["combined_forced_slots"]["subject"],
        )
        self.assertIn(
            pilot["combined_forced_slots"]["action"][0],
            {
                "pilot_preflight_control_check",
                "pilot_taxi_instrument_crosscheck",
                "pilot_approach_control_scan",
            },
        )

        mixin_cases = {
            "성인 교복 의상 레퍼런스": (
                "교복",
                "costume_style",
                "coordinated_school_uniform_system",
            ),
            "A라인 원피스 드레스": (
                "원피스",
                "garment_detail",
                "one_piece_continuous_bodice_to_hem",
            ),
            "성인 시스루 직물 화보": (
                "시스루",
                "surface_material",
                "sheer_organza_chiffon_transmission",
            ),
            "성인 가상 군복 검사": (
                "군복",
                "costume_style",
                "military_service_uniform_system",
            ),
            "착용형 갑옷 구조 레퍼런스": (
                "갑옷",
                "garment_detail",
                "armor_articulated_overlap_attachment",
            ),
            "성인 오리지널 상업적인 방어력 높은 갑옷": (
                "노출 갑옷",
                "garment_detail",
                "revealing_armor_opaque_intimate_coverage",
            ),
        }
        for concept, (mixin, slot, expected_id) in mixin_cases.items():
            with self.subTest(concept=concept):
                explanation = self.explain(concept)
                self.assertIn(mixin, explanation["applied_mixins"])
                self.assertIn(expected_id, explanation["combined_forced_slots"][slot])

        revealing = self.explain("성인 오리지널 상업적인 방어력 높은 갑옷")
        self.assertNotIn("갑옷", revealing["applied_mixins"])
        self.assertIn(
            "adult_original_fantasy_character_context",
            revealing["combined_forced_slots"]["adult_context"],
        )
        self.assertEqual(self.recipes["aliases"]["상업적 방어력"], "노출 갑옷")
        self.assertNotEqual(self.recipes["aliases"].get("교복"), "학생")

    def test_research_rows_cover_sources_candidates_contracts_and_limitations(self) -> None:
        expected_rows = {
            "pilot_faa_checklist_controls_operation",
            "cabin_crew_icao_safety_duties",
            "school_uniform_govuk_policy_components",
            "one_piece_cambridge_construction",
            "one_piece_met_structural_seaming",
            "sheer_jstage_textile_transmission",
            "military_uniform_army_system_components",
            "armor_royal_armouries_articulation",
            "revealing_armor_met_exposure_boundary",
        }
        self.assertTrue(expected_rows <= set(self.evidence))
        all_candidate_ids = {
            candidate_id
            for entries in self.by_slot.values()
            for candidate_id in entries
        }
        for row_id in expected_rows:
            with self.subTest(row_id=row_id):
                row = self.evidence[row_id]
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertEqual(row["status"], "approved")
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["affected_contract_ids"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                self.assertTrue(set(row["candidate_ids"]) <= all_candidate_ids)

        revealing = self.evidence["revealing_armor_met_exposure_boundary"]
        self.assertTrue(
            any(
                "comes exclusively from the requester's project definition" in limitation
                for limitation in revealing["research_limitations"]
            )
        )


if __name__ == "__main__":
    unittest.main()
