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
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "research_evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "간호사": "clinical_nursing_duty_system",
    "경찰관": "police_public_safety_duty_system",
    "소방관": "firefighter_protective_response_system",
    "응급구조사": "emergency_medical_transport_system",
    "해양경찰": "maritime_safety_coast_guard_role",
    "철도 기관사": "rail_driver_operation",
    "플랫폼 역무원": "rail_platform_dispatch_operation",
    "보안요원": "private_security_access_control",
}

PROFILE_IDS = set(PROFILE_ROUTES.values())

EXPECTED_BY_SLOT = {
    "costume_style": {
        "clinical_nursing_scrub_duty_system",
        "police_public_safety_duty_uniform",
        "firefighter_turnout_ppe_system",
        "emt_high_visibility_transport_uniform",
        "coast_guard_maritime_rescue_uniform",
        "rail_driver_cab_duty_uniform",
        "rail_platform_dispatch_uniform",
        "private_security_access_control_uniform",
        "professional_kitchen_protective_workwear",
        "postal_route_delivery_uniform_system",
        "hotel_front_desk_service_attire_option",
    },
    "action": {
        "nurse_patient_identifier_vitals_handover",
        "police_perimeter_radio_flow_control",
        "firefighter_scba_pressure_equipment_check",
        "emt_assess_secure_transport_patient",
        "coast_guard_rescue_line_recovery",
        "train_driver_control_signal_crosscheck",
        "rail_dispatch_doors_clear_ready_signal",
        "security_verify_credential_control_gate",
        "chef_temperature_ticket_hygiene_check",
        "postal_scan_sort_deliver_route_item",
        "hotel_register_guest_issue_keycard",
    },
    "prop": {
        "clinical_identifier_chart_monitor_set",
        "police_radio_log_barrier_set",
        "firefighter_scba_gauge_tool_set",
        "emt_stretcher_monitor_medical_pack_set",
        "coast_guard_rescue_line_lifebuoy_radio_set",
        "train_cab_controller_route_display_set",
        "rail_dispatch_radio_indicator_baton_set",
        "security_credential_reader_entry_log_set",
        "chef_thermometer_ticket_sanitation_set",
        "postal_scanner_route_mailbag_set",
        "hotel_keycard_reservation_terminal_set",
    },
    "location": {
        "active_clinical_bedside_handover_zone",
        "controlled_public_safety_perimeter",
        "fire_station_apparatus_check_bay",
        "ambulance_loading_handover_bay",
        "coast_guard_rescue_boat_deck",
        "active_rail_driver_cab",
        "staffed_platform_dispatch_zone",
        "controlled_facility_access_lobby",
        "professional_kitchen_pass_hygiene_station",
        "postal_route_doorstep_delivery_point",
        "hotel_front_desk_registration_zone",
    },
}

EXPECTED_PRESETS = {
    "clinical_nursing_duty_documentary",
    "police_public_safety_duty_documentary",
    "firefighter_protective_readiness_documentary",
    "emergency_medical_transport_documentary",
    "maritime_rescue_coast_guard_documentary",
    "rail_driver_operation_documentary",
    "rail_platform_dispatch_documentary",
    "private_security_access_control_documentary",
    "professional_kitchen_workflow_documentary",
    "postal_route_delivery_documentary",
    "hotel_front_desk_service_documentary",
}

ROLE_EXPECTATIONS = {
    "간호사": (
        "clinical_nursing_duty_documentary",
        "nurse_patient_identifier_vitals_handover",
    ),
    "경찰": (
        "police_public_safety_duty_documentary",
        "police_perimeter_radio_flow_control",
    ),
    "소방관": (
        "firefighter_protective_readiness_documentary",
        "firefighter_scba_pressure_equipment_check",
    ),
    "응급구조사": (
        "emergency_medical_transport_documentary",
        "emt_assess_secure_transport_patient",
    ),
    "보안요원": (
        "private_security_access_control_documentary",
        "security_verify_credential_control_gate",
    ),
    "요리사": (
        "professional_kitchen_workflow_documentary",
        "chef_temperature_ticket_hygiene_check",
    ),
    "호텔리어": (
        "hotel_front_desk_service_documentary",
        "hotel_register_guest_issue_keycard",
    ),
    "우체부": (
        "postal_route_delivery_documentary",
        "postal_scan_sort_deliver_route_item",
    ),
    "기차 차장": (
        "rail_platform_dispatch_documentary",
        "rail_dispatch_doors_clear_ready_signal",
    ),
    "역무원": (
        "rail_platform_dispatch_documentary",
        "rail_dispatch_doors_clear_ready_signal",
    ),
    "해양경찰": (
        "maritime_rescue_coast_guard_documentary",
        "coast_guard_rescue_line_recovery",
    ),
    "철도 기관사": (
        "rail_driver_operation_documentary",
        "train_driver_control_signal_crosscheck",
    ),
}

EVIDENCE_IDS = {
    "womens_uniform_nhs_clinical_workwear",
    "womens_uniform_korean_police_variant_system",
    "womens_uniform_osha_firefighter_ppe_system",
    "womens_uniform_ems_transport_scope",
    "womens_uniform_imo_maritime_rescue_appliances",
    "womens_uniform_rssb_platform_dispatch",
    "womens_uniform_orr_train_driver_operation",
    "womens_uniform_cisa_private_access_control",
    "womens_uniform_fda_kitchen_workwear",
    "womens_uniform_usps_role_specific_uniforms",
    "womens_uniform_bls_hotel_service_uniform_limit",
}


class WomensProfessionalUniformVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.recipes = json.loads(RECIPES_PATH.read_text(encoding="utf-8"))
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
        }
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.presets = {str(row["id"]): row for row in cls.tags["presets"]}

    def hard_visual_matches(self, text: str) -> set[str]:
        return set(
            prompt_generator.candidate_pack_auto_visual_obligation_matches(
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
        )

    @staticmethod
    def normalized_set(role: dict) -> dict[str, str]:
        raw = role.get("set", {})
        if isinstance(raw, dict):
            return {str(key): str(value) for key, value in raw.items()}
        result: dict[str, str] = {}
        for entry in raw:
            slot, candidate_id = str(entry).split("=", 1)
            result[slot] = candidate_id
        return result

    def test_eight_hard_profiles_have_component_contracts_and_five_pixel_gates(self):
        self.assertLessEqual(PROFILE_IDS, set(self.profiles))
        gate_ids: list[str] = []
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertTrue(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ]
                )
                self.assertGreaterEqual(components["minimum_component_groups"], 3)
                self.assertGreaterEqual(len(components["required_group_ids"]), 3)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)
                gate_ids.extend(str(gate["id"]) for gate in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_direct_professional_terms_route_to_only_the_intended_new_profile(self):
        for term, profile_id in PROFILE_ROUTES.items():
            with self.subTest(term=term):
                self.assertEqual(
                    self.hard_visual_matches(term) & PROFILE_IDS,
                    {profile_id},
                )

    def test_generic_gendered_uniform_and_costume_terms_do_not_force_profiles(self):
        negatives = (
            "여성 제복",
            "여자 제복",
            "여성 유니폼",
            "women's uniform",
            "female uniform",
            "woman in uniform",
            "nurse costume",
            "police cosplay",
            "firefighter costume portrait",
            "romantic platform farewell",
            "security fashion suit",
        )
        for text in negatives:
            with self.subTest(text=text):
                self.assertEqual(self.hard_visual_matches(text) & PROFILE_IDS, set())

    def test_candidate_pack_has_complete_role_task_tool_location_clusters(self):
        self.assertGreaterEqual(
            tuple(int(part) for part in str(self.tags["version"]).split(".")),
            (1, 39),
        )
        for slot, expected_ids in EXPECTED_BY_SLOT.items():
            with self.subTest(slot=slot):
                self.assertLessEqual(expected_ids, set(self.by_slot[slot]))
                for candidate_id in expected_ids:
                    row = self.by_slot[slot][candidate_id]
                    self.assertTrue(row.get("ko"))
                    self.assertTrue(row.get("en"))
                    self.assertTrue(row.get("aliases"))
                    self.assertTrue(row.get("keywords"))
                    self.assertTrue(row.get("embedding_text"))
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)
        self.assertLessEqual(EXPECTED_PRESETS, set(self.presets))

    def test_role_recipes_use_procedural_presets_and_actions(self):
        for role_name, (preset_id, action_id) in ROLE_EXPECTATIONS.items():
            with self.subTest(role_name=role_name):
                role = self.recipes["roles"][role_name]
                selected = self.normalized_set(role)
                self.assertEqual(role["preset"], preset_id)
                self.assertEqual(selected["action"], action_id)
                self.assertIn(selected["action"], self.by_slot["action"])
                self.assertIn(selected["location"], self.by_slot["location"])
                self.assertIn(selected["prop"], self.by_slot["prop"])

        hotel = self.normalized_set(self.recipes["roles"]["호텔리어"])
        self.assertNotIn("costume_style", hotel)
        hotel_preset = self.presets["hotel_front_desk_service_documentary"]
        self.assertNotIn("costume_style", hotel_preset["required_slots"])
        self.assertTrue(
            any(
                row.get("slot") == "costume_style"
                for row in hotel_preset["optional_slots"]
            )
        )

    def test_research_rows_are_approved_source_bound_and_candidate_complete(self):
        rows = {
            row["id"]: row
            for row in (
                json.loads(line)
                for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
            if row.get("domain") == "womens_professional_uniform_visual_semantics"
        }
        self.assertEqual(set(rows), EVIDENCE_IDS)
        all_candidates = set().union(*EXPECTED_BY_SLOT.values())
        for evidence_id, row in rows.items():
            with self.subTest(evidence_id=evidence_id):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                self.assertTrue(set(row["candidate_ids"]) <= all_candidates)
                for contract_id in row["affected_contract_ids"]:
                    contract_type, contract_name = contract_id.split(":", 1)
                    if contract_type == "visual_obligation":
                        self.assertIn(contract_name, PROFILE_IDS)
                    else:
                        self.assertEqual(contract_type, "preset")
                        self.assertIn(contract_name, EXPECTED_PRESETS)

    def test_registry_schema_accepts_professional_uniform_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
