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
FIXTURE_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "traditional_clothing_visual_routing_v1.jsonl"
)
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "traditional-clothing-20260831"
    / "evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


GARMENT_SYSTEM_IDS = {
    "hanbok_jeogori_lower_layer_system",
    "kimono_kosode_obi_system",
    "hanfu_historical_layer_system",
    "qipao_standing_collar_diagonal_closure",
    "sari_continuous_drape_system",
    "nivi_sari_pleat_pallu_system",
    "ao_dai_long_tunic_trouser_system",
    "kebaya_front_open_blouse_sarong_system",
    "barong_tagalog_untucked_formal_shirt",
    "moroccan_caftan_center_front_belt_system",
    "huipil_rectilinear_tunic_system",
    "scottish_kilt_pleated_wrap_system",
    "dirndl_bodice_blouse_skirt_apron_system",
    "norwegian_bunad_regional_ensemble",
    "mongol_deel_overlap_sash_system",
    "central_asian_chapan_open_robe_system",
    "dhoti_waist_leg_drape_system",
    "salwar_kameez_tunic_trouser_scarf_system",
    "baju_kurung_long_tunic_skirt_system",
    "longyi_waist_wrap_tube_system",
    "west_african_grand_boubou_system",
    "west_african_agbada_layered_robe_system",
    "andean_poncho_panel_system",
    "mexican_rebozo_shawl_wrap_system",
    "thai_chut_thai_regional_ensemble",
    "sami_gakti_regional_ensemble",
    "arabian_thobe_ankle_length_robe",
    "abaya_outer_robe_system",
}

GARMENT_DETAIL_IDS = {
    "hanbok_short_upper_lower_layer_boundary",
    "kimono_wrap_front_obi_layer_boundary",
    "hanfu_period_collar_layer_sequence",
    "qipao_standing_collar_diagonal_frog_line",
    "sari_waist_wrap_and_pallu_route",
    "nivi_front_pleats_left_shoulder_pallu",
    "ao_dai_side_openings_over_trousers",
    "kebaya_center_fastening_front_opening",
    "barong_untucked_translucent_embroidery",
    "caftan_center_front_trim_and_belt",
    "huipil_rectilinear_panel_neck_opening",
    "kilt_flat_apron_side_back_pleats",
    "dirndl_bodice_blouse_skirt_apron_layers",
    "deel_asymmetric_overlap_and_sash",
    "chapan_open_front_quilted_edge",
    "baju_kurung_tunic_skirt_boundary",
    "longyi_waist_fold_tube_body",
    "boubou_broad_sleeve_rectangular_volume",
    "poncho_central_neck_front_back_panels",
    "rebozo_long_shawl_route_and_fringe",
}

TEXTURE_IDS = {
    "hand_drawn_batik_wax_resist_texture",
    "ikat_pre_dyed_yarn_soft_edge_texture",
    "kente_interwoven_band_texture",
    "tartan_sett_twill_texture",
    "brocade_supplementary_pattern_texture",
    "hand_embroidered_thread_relief_texture",
}

SURFACE_IDS = {
    "batik_wax_resist_dyed_cloth_surface",
    "ikat_pre_dyed_yarn_weave_surface",
    "kente_joined_strip_woven_surface",
    "tartan_wool_twill_sett_surface",
    "brocade_raised_supplementary_weft_surface",
    "hand_embroidery_thread_relief_surface",
}

ACCESSORY_IDS = {
    "kebaya_kerongsang_brooch_set",
    "kimono_obi_obijime_layer",
    "moroccan_mdamma_belt",
    "deel_broad_functional_sash",
    "rebozo_woven_shawl_with_fringe",
    "bunad_region_specific_accessory_set",
}

PROFILE_IDS = {
    "qipao_standing_collar_diagonal_closure_system",
    "kebaya_front_open_blouse_sarong_system",
    "nivi_sari_continuous_pleat_pallu_system",
    "andean_poncho_central_opening_panel_system",
    "west_african_grand_boubou_volume_system",
}


class PhotoTraditionalClothingSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
        }

    def test_candidate_pack_contains_bounded_garment_and_textile_clusters(self):
        self.assertEqual(self.tags["version"], "1.31")
        expected_by_slot = {
            "costume_style": GARMENT_SYSTEM_IDS,
            "garment_detail": GARMENT_DETAIL_IDS,
            "texture": TEXTURE_IDS,
            "surface_material": SURFACE_IDS,
            "wearable_accessory": ACCESSORY_IDS,
        }
        for slot, expected_ids in expected_by_slot.items():
            with self.subTest(slot=slot):
                rows = {
                    str(row["id"]): row for row in self.tags["slots"][slot]
                }
                self.assertTrue(expected_ids <= set(rows))
                for candidate_id in expected_ids:
                    row = rows[candidate_id]
                    self.assertTrue(row.get("en"))
                    self.assertTrue(row.get("ko"))
                    self.assertTrue(row.get("aliases"))
                    self.assertTrue(row.get("keywords"))
                    self.assertTrue(row.get("embedding_text"))
                    self.assertGreater(float(row.get("weight", 0)), 0)

    def test_new_candidates_do_not_infer_wearer_identity_from_clothing(self):
        all_ids = (
            GARMENT_SYSTEM_IDS
            | GARMENT_DETAIL_IDS
            | TEXTURE_IDS
            | SURFACE_IDS
            | ACCESSORY_IDS
        )
        rows = {
            str(row["id"]): row
            for slot_rows in self.tags["slots"].values()
            for row in slot_rows
            if isinstance(row, dict) and str(row.get("id") or "") in all_ids
        }
        forbidden_claims = {
            "korean face",
            "japanese face",
            "chinese face",
            "indian face",
            "african face",
            "ethnicity",
            "skin tone proves",
            "nationality proves",
            "racial features",
        }
        for candidate_id, row in rows.items():
            with self.subTest(candidate_id=candidate_id):
                text = " ".join(
                    [
                        str(row.get("en") or ""),
                        str(row.get("ko") or ""),
                        str(row.get("embedding_text") or ""),
                        *[str(value) for value in row.get("aliases") or []],
                        *[str(value) for value in row.get("keywords") or []],
                    ]
                ).lower()
                self.assertFalse(forbidden_claims & {term for term in forbidden_claims if term in text})

    def test_five_render_profiles_have_connected_component_and_gate_contracts(self):
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        gate_ids: list[str] = []
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                self.assertEqual(profile["category"], "culture_bounded_garment_system")
                self.assertGreaterEqual(
                    len(profile["semantics"]["component_semantics"]["required_group_ids"]),
                    4,
                )
                self.assertGreaterEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)
                gate_ids.extend(str(row["id"]) for row in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_generic_labels_never_hard_activate_a_named_profile(self):
        forbidden_generic_terms = {
            "traditional dress",
            "traditional clothing",
            "folk costume",
            "ethnic costume",
            "tribal dress",
            "indigenous dress",
            "Asian robe",
            "전통 의복",
            "전통 의상",
            "민속 의상",
            "민족 의상",
            "부족 의상",
        }
        exact_terms = {
            str(term)
            for profile in self.registry["profiles"]
            for term in profile["activation"]["exact_terms"]
        }
        self.assertTrue(forbidden_generic_terms.isdisjoint(exact_terms))

    def test_exact_candidate_and_hard_negative_routing_fixture(self):
        cases = [
            json.loads(line)
            for line in FIXTURE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for case in cases:
            with self.subTest(case=case["id"]):
                source_rows = [
                    {
                        "source": "concept_lock",
                        "text": case["text"],
                        "polarity": "required",
                        "priority": "critical",
                        "mandatory": True,
                    }
                ]
                hard_matches = (
                    prompt_generator.candidate_pack_auto_visual_obligation_matches(
                        self.registry,
                        source_rows,
                    )
                )
                optional_matches = (
                    prompt_generator.candidate_pack_auto_visual_concept_matches(
                        self.registry,
                        source_rows,
                    )
                )
                self.assertEqual(
                    sorted(hard_matches), sorted(case["expected_profile_ids"])
                )
                self.assertEqual(
                    sorted(optional_matches),
                    sorted(case["expected_candidate_profile_ids"]),
                )

    def test_component_complete_paraphrases_are_bm25f_optional_never_hard(self):
        cases = [
            json.loads(line)
            for line in FIXTURE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip() and '"candidate_' in line
        ]
        visual_profile_index = prompt_generator.build_visual_profile_index_payload(
            self.registry
        )
        for case in cases:
            with self.subTest(case=case["id"]):
                target_id = case["expected_candidate_profile_ids"][0]
                source_rows = [
                    {
                        "source": "authorial_core_interpretation",
                        "text": case["text"],
                        "polarity": "advisory",
                    }
                ]
                resolution = prompt_generator.resolve_visual_profile_hits(
                    self.registry,
                    source_rows,
                    visual_profile_index=visual_profile_index,
                    query_text=case["text"],
                    query_fields={
                        "active_request": case["text"],
                        "interpreted_intent": case["text"],
                    },
                    adult_context=True,
                )
                hit = next(
                    row
                    for row in resolution["hits"]
                    if row["profile_id"] == target_id
                )
                self.assertEqual(hit["match_basis"], "bm25f")
                self.assertFalse(hit["hard_eligible"])
                self.assertTrue(hit["optional_eligible"])
                self.assertTrue(resolution["bm25f_evaluated"])
                self.assertFalse(resolution["embedding_evaluated"])

    def test_research_evidence_maps_only_to_existing_candidates_and_profiles(self):
        known_candidate_ids = {
            str(row["id"])
            for slot_rows in self.tags["slots"].values()
            for row in slot_rows
            if isinstance(row, dict) and row.get("id")
        }
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 20)
        for row in rows:
            with self.subTest(evidence=row["id"]):
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertTrue(set(row.get("candidate_ids") or []) <= known_candidate_ids)
                self.assertTrue(
                    set(row.get("affected_contract_ids") or []) <= set(self.profiles)
                )
                self.assertTrue(row.get("research_limitations"))
                self.assertTrue(row.get("reuse_note"))

    def test_registry_schema_is_valid_apart_from_generated_index_refresh(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
