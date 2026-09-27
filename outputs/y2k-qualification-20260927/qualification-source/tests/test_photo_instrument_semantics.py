from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
EVIDENCE_PATH = (
    ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "가야금": "gayageum_movable_bridge_pluck_press",
    "geomungo": "geomungo_fretted_suldae_zither",
    "alto saxophone": "alto_tenor_saxophone_reed_conical_body",
    "trumpet": "modern_piston_trumpet_three_valve",
    "cello": "cello_endpin_seated_bowed",
    "double bass": "double_bass_human_scale_floor_supported",
    "vibraphone": "vibraphone_metal_bars_motor_pedal",
    "xylophone": "xylophone_wooden_bar_resonator",
    "theremin": "theremin_dual_antenna_noncontact",
    "MIDI controller": "midi_controller_external_sound_source",
}

EXPECTED_BY_SLOT = {
    "subject": {
        "adult_instrument_performer",
        "adult_gugak_instrument_performer",
        "adult_electronic_instrument_performer",
    },
    "action": {
        "gayageum_pluck_press_action",
        "geomungo_suldae_strike_action",
        "saxophone_reed_key_action",
        "trumpet_lip_valve_action",
        "cello_seated_bowing_action",
        "double_bass_floor_play_action",
        "vibraphone_mallet_pedal_action",
        "xylophone_mallet_strike_action",
        "theremin_noncontact_pitch_volume_action",
        "midi_controller_external_sound_action",
    },
    "prop": {
        "gayageum_movable_bridge_zither_prop",
        "geomungo_fretted_suldae_zither_prop",
        "alto_tenor_saxophone_reed_keywork_prop",
        "modern_piston_trumpet_prop",
        "cello_endpin_bowed_prop",
        "double_bass_human_scale_prop",
        "vibraphone_motor_pedal_prop",
        "xylophone_wooden_bar_prop",
        "theremin_dual_antenna_prop",
        "midi_controller_external_sound_chain_prop",
    },
    "contact_point": {
        "gayageum_right_pluck_left_press_contact",
        "geomungo_suldae_string_contact",
        "saxophone_reed_lip_key_contact",
        "trumpet_mouthpiece_valve_contact",
        "cello_bow_hair_string_contact",
        "double_bass_string_and_floor_contact",
        "vibraphone_mallet_bar_pedal_contact",
        "xylophone_mallet_wood_bar_contact",
        "theremin_no_contact_dual_field_relation",
        "midi_controller_touch_and_output_relation",
    },
    "body_pose": {
        "seated_horizontal_zither_two_hand_pose",
        "wind_embouchure_two_hand_key_pose",
        "cello_between_knees_floor_endpin_pose",
        "double_bass_floor_supported_standing_pose",
        "keyboard_percussion_standing_reach_pose",
        "theremin_split_hand_field_pose",
        "midi_controller_touch_signal_pose",
    },
    "capture_context": {
        "instrument_mechanism_performance_documentary",
        "instrument_confusion_pair_diagnostic_capture",
    },
    "location": {
        "gugak_instrument_rehearsal_room",
        "orchestral_instrument_rehearsal_stage",
        "keyboard_percussion_rehearsal_bay",
        "electronic_instrument_signal_studio",
    },
    "lighting": {
        "instrument_structure_grazing_light",
        "controlled_brass_keywork_reflection_light",
        "electronic_control_separation_light",
    },
    "composition": {
        "instrument_silhouette_contact_same_frame",
        "instrument_diagnostic_detail_native_scale",
        "instrument_scale_support_full_relation",
    },
    "scale_relation": {
        "human_scale_upright_instrument_relation",
        "seated_horizontal_zither_scale_relation",
    },
    "surface_material": {
        "traditional_zither_wood_string_bridge_surface",
        "reed_keywork_brass_tubing_surface",
        "bowed_string_wood_endpin_surface",
        "keyboard_percussion_bar_resonator_surface",
        "electronic_instrument_control_signal_surface",
    },
    "prop_direction": {
        "horizontal_zither_cross_frame_direction",
        "wind_bell_forward_mouthpiece_back_direction",
        "upright_string_endpin_to_neck_direction",
        "keyboard_percussion_bar_field_direction",
        "theremin_split_antenna_field_direction",
    },
    "narrative_phase": {
        "instrument_attack_transition_phase",
        "sustained_instrument_control_phase",
        "instrument_setup_signal_check_phase",
    },
}

PROFILE_BINDINGS = {
    "gayageum_movable_bridge_pluck_press": {
        "gayageum_movable_bridge_zither_prop",
        "gayageum_pluck_press_action",
        "gayageum_right_pluck_left_press_contact",
        "seated_horizontal_zither_two_hand_pose",
    },
    "geomungo_fretted_suldae_zither": {
        "geomungo_fretted_suldae_zither_prop",
        "geomungo_suldae_strike_action",
        "geomungo_suldae_string_contact",
        "seated_horizontal_zither_two_hand_pose",
    },
    "alto_tenor_saxophone_reed_conical_body": {
        "alto_tenor_saxophone_reed_keywork_prop",
        "saxophone_reed_key_action",
        "saxophone_reed_lip_key_contact",
        "wind_embouchure_two_hand_key_pose",
    },
    "modern_piston_trumpet_three_valve": {
        "modern_piston_trumpet_prop",
        "trumpet_lip_valve_action",
        "trumpet_mouthpiece_valve_contact",
        "wind_embouchure_two_hand_key_pose",
    },
    "cello_endpin_seated_bowed": {
        "cello_endpin_bowed_prop",
        "cello_seated_bowing_action",
        "cello_bow_hair_string_contact",
        "cello_between_knees_floor_endpin_pose",
    },
    "double_bass_human_scale_floor_supported": {
        "double_bass_human_scale_prop",
        "double_bass_floor_play_action",
        "double_bass_string_and_floor_contact",
        "double_bass_floor_supported_standing_pose",
    },
    "vibraphone_metal_bars_motor_pedal": {
        "vibraphone_motor_pedal_prop",
        "vibraphone_mallet_pedal_action",
        "vibraphone_mallet_bar_pedal_contact",
        "keyboard_percussion_standing_reach_pose",
    },
    "xylophone_wooden_bar_resonator": {
        "xylophone_wooden_bar_prop",
        "xylophone_mallet_strike_action",
        "xylophone_mallet_wood_bar_contact",
        "keyboard_percussion_standing_reach_pose",
    },
    "theremin_dual_antenna_noncontact": {
        "theremin_dual_antenna_prop",
        "theremin_noncontact_pitch_volume_action",
        "theremin_no_contact_dual_field_relation",
        "theremin_split_hand_field_pose",
    },
    "midi_controller_external_sound_source": {
        "midi_controller_external_sound_chain_prop",
        "midi_controller_external_sound_action",
        "midi_controller_touch_and_output_relation",
        "midi_controller_touch_signal_pose",
    },
}

NEW_EVIDENCE_IDS = {
    "instrument_taxonomy_mimo_hornbostel_sachs",
    "instrument_gayageum_ngc_structure",
    "instrument_geomungo_ngc_structure",
    "instrument_saxophone_yamaha_mechanism",
    "instrument_trumpet_yamaha_mechanism",
    "instrument_cello_philharmonia_scale_support",
    "instrument_double_bass_philharmonia_scale_support",
    "instrument_keyboard_percussion_philharmonia_material_system",
    "instrument_theremin_moog_dual_antenna",
    "instrument_midi_association_controller_source_boundary",
}


class PhotoInstrumentSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
        }
        cls.known_candidates = {
            str(row["id"])
            for rows in cls.tags["slots"].values()
            for row in rows
            if isinstance(row, dict) and row.get("id")
        }

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

    def test_instrument_candidates_exist_with_searchable_fields_and_no_rank(self):
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

    def test_each_profile_has_prop_action_contact_and_pose_candidates(self):
        self.assertEqual(set(PROFILE_BINDINGS), set(PROFILE_ROUTES.values()))
        for profile_id, candidate_ids in PROFILE_BINDINGS.items():
            with self.subTest(profile=profile_id):
                self.assertIn(profile_id, self.profiles)
                self.assertLessEqual(candidate_ids, self.known_candidates)
                self.assertEqual(len(candidate_ids), 4)

    def test_ten_profiles_have_five_component_groups_and_unique_pixel_gates(self):
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
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)
                gate_ids.extend(str(row["id"]) for row in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_exact_terms_route_only_the_intended_profile(self):
        for term, profile_id in PROFILE_ROUTES.items():
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), [profile_id])

        paired_terms = {
            "거문고": "geomungo_fretted_suldae_zither",
            "테너 색소폰": "alto_tenor_saxophone_reed_conical_body",
            "트럼펫": "modern_piston_trumpet_three_valve",
            "첼로": "cello_endpin_seated_bowed",
            "콘트라베이스": "double_bass_human_scale_floor_supported",
            "비브라폰": "vibraphone_metal_bars_motor_pedal",
            "실로폰": "xylophone_wooden_bar_resonator",
            "테레민": "theremin_dual_antenna_noncontact",
            "미디 컨트롤러": "midi_controller_external_sound_source",
        }
        for term, profile_id in paired_terms.items():
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), [profile_id])

    def test_broad_or_ambiguous_terms_do_not_force_an_instrument_profile(self):
        negatives = (
            "musical instrument portrait",
            "악기 연주",
            "string instrument",
            "woodwind instrument",
            "keyboard instrument",
            "bass frequency response",
            "horned animal portrait",
            "bow tie fashion",
            "reed plants beside a lake",
            "instrument calibration step",
            "soprano saxophone",
            "marimba performance",
            "standalone synthesizer",
        )
        profile_ids = set(PROFILE_ROUTES.values())
        for negative in negatives:
            with self.subTest(negative=negative):
                self.assertTrue(
                    set(self.hard_visual_matches(negative)).isdisjoint(profile_ids)
                )

    def test_research_evidence_is_approved_and_bound_to_existing_data(self):
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
                self.assertTrue(set(row["candidate_ids"]) <= self.known_candidates)
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                for contract_id in row["affected_contract_ids"]:
                    kind, value = contract_id.split(":", 1)
                    self.assertEqual(kind, "visual_obligation")
                    self.assertIn(value, self.profiles)

    def test_registry_schema_is_valid_after_instrument_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
