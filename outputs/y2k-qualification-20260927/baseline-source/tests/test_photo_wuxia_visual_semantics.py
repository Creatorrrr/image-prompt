from __future__ import annotations

import json
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
SEMANTIC_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_semantic_index.json"
EVIDENCE_PATH = (
    ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "wuxia rooftop qinggong traversal": "wuxia_rooftop_qinggong_traversal",
    "무협 죽림 공중 결투": "wuxia_bamboo_forest_aerial_duel",
    "jianghu frontier inn identity standoff": "jianghu_inn_identity_standoff",
    "비무 포권 대치": "formal_biwu_reciprocal_salute_standoff",
    "xia protective intervention": "xia_protective_intervention_event",
    "표국 화물 호송": "biaoju_guarded_cargo_departure",
}

PROFILE_IDS = set(PROFILE_ROUTES.values())

EXPECTED_BY_SLOT = {
    "subject": {
        "adult_jianghu_martial_wanderer",
        "wuxia_rival_martial_pair",
        "martial_sect_disciple_group",
        "biaoju_armed_escort_team",
        "xia_protective_intervention_group",
    },
    "action": {
        "qinggong_tiled_roof_traversal",
        "bamboo_forest_aerial_duel_exchange",
        "jianghu_inn_identity_standoff",
        "formal_biwu_reciprocal_salute",
        "xia_protective_interposition",
        "biaoju_guarded_convoy_departure",
        "martial_sect_ranked_courtyard_drill",
    },
    "prop": {
        "jianghu_sheathed_jian_travel_bundle",
        "blank_hero_invitation_token_set",
        "biaoju_loaded_cart_sealed_cargo_set",
        "martial_sect_training_rack_and_drum",
        "jianghu_inn_meal_and_travel_prop_set",
        "wrapped_martial_manual_lineage_token_pair",
    },
    "location": {
        "wuxia_old_tiled_rooftop_route",
        "wuxia_bamboo_depth_action_corridor",
        "jianghu_frontier_inn_hall",
        "formal_biwu_courtyard_platform",
        "martial_sect_gate_training_courtyard",
        "biaoju_gate_loading_yard_road",
        "jianghu_mountain_pass_waystation",
    },
    "world": {"jianghu_unofficial_social_world"},
    "lighting": {
        "moonlit_tiled_roof_edge_light",
        "bamboo_canopy_dappled_action_light",
        "jianghu_inn_threshold_faction_light",
    },
    "composition": {
        "wuxia_action_path_start_transit_destination",
        "jianghu_inn_faction_zone_triangle",
        "formal_biwu_bilateral_witness_frame",
        "xia_intervention_three_role_blocking",
    },
    "motion": {
        "qinggong_takeoff_landing_fabric_lag",
        "bamboo_duel_opposed_vertical_reversal",
    },
    "mood": {
        "jianghu_watchful_restraint",
        "xia_intervention_immediate_release",
    },
    "wearable_accessory": {
        "jianghu_bamboo_travel_hat_chin_tie",
        "jianghu_sash_scabbard_token_suspension",
    },
}

EVIDENCE_IDS = {
    "wuxia_teo_martial_chivalry_xia_action",
    "wuxia_cambridge_jianghu_social_world",
    "wuxia_bfi_king_hu_visual_grammar",
    "wuxia_bfi_rooftop_traversal",
    "wuxia_criterion_touch_of_zen_bamboo_action",
    "wuxia_criterion_dragon_inn_standoff",
    "wuxia_iwuf_reciprocal_salute_protocol",
    "wuxia_biaoju_museum_material_institution",
    "wuxia_hebei_biaoju_cargo_escort_history",
    "wuxia_mdpi_xianxia_cultivation_boundary",
}


class PhotoWuxiaVisualSemanticsTests(unittest.TestCase):
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

    def hard_visual_matches(self, text: str) -> list[str]:
        return sorted(
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
    def candidate_text(row: dict) -> str:
        return " ".join(
            [
                str(row.get("ko") or ""),
                str(row.get("en") or ""),
                str(row.get("embedding_text") or ""),
                *[str(value) for value in row.get("aliases") or []],
                *[str(value) for value in row.get("keywords") or []],
            ]
        ).casefold()

    def test_six_profiles_have_complete_component_evidence_and_pixel_gates(self):
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        gate_ids: list[str] = []
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
                self.assertEqual(len(components["groups"]), 5)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)
                self.assertTrue(
                    {gate["review_scale"] for gate in profile["render_gates"]}
                    <= {"thumbnail", "native", "both"}
                )
                gate_ids.extend(str(gate["id"]) for gate in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_narrow_scene_terms_route_to_only_the_intended_profile(self):
        for term, profile_id in PROFILE_ROUTES.items():
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), [profile_id])

    def test_genre_social_and_adjacent_terms_do_not_force_scene_profiles(self):
        negatives = (
            "wuxia",
            "무협",
            "jianghu",
            "강호",
            "xia",
            "협객",
            "biwu",
            "비무",
            "biaoju",
            "표국",
            "martial arts",
            "hanfu portrait",
            "xianxia cultivation immortal",
            "선협 수선",
            "generic bamboo portrait",
            "modern city rooftop parkour",
            "ordinary tavern dinner",
            "solo taolu performance",
            "merchant caravan",
            "hero pose",
            "qinggong rooftop traversal",
            "무협 죽림 결투",
            "jianghu inn standoff",
            "formal biwu challenge",
            "무협 비무 대결",
            "협객의 의로운 개입",
            "biaoju convoy departure",
            "표국 호송 출발",
        )
        for negative in negatives:
            with self.subTest(negative=negative):
                self.assertTrue(
                    set(self.hard_visual_matches(negative)).isdisjoint(PROFILE_IDS)
                )

    def test_candidate_pack_contains_neutral_event_components(self):
        version = tuple(int(part) for part in str(self.tags["version"]).split("."))
        self.assertGreaterEqual(version, (1, 36))
        for slot, expected_ids in EXPECTED_BY_SLOT.items():
            with self.subTest(slot=slot):
                self.assertTrue(expected_ids <= set(self.by_slot[slot]))
                for candidate_id in expected_ids:
                    row = self.by_slot[slot][candidate_id]
                    self.assertTrue(row.get("ko"))
                    self.assertTrue(row.get("en"))
                    self.assertTrue(row.get("aliases"))
                    self.assertTrue(row.get("keywords"))
                    self.assertTrue(row.get("embedding_text"))
                    self.assertGreater(float(row.get("weight", 0)), 0)
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)

    def test_generated_semantic_index_contains_every_new_candidate(self):
        manifest = json.loads(SEMANTIC_INDEX_PATH.read_text(encoding="utf-8"))
        indexed = {str(value) for value in manifest["entry_order"]}
        expected = {
            f"slot:{slot}:{candidate_id}"
            for slot, candidate_ids in EXPECTED_BY_SLOT.items()
            for candidate_id in candidate_ids
        }
        self.assertTrue(expected <= indexed)

    def test_wuxia_and_xianxia_legacy_candidates_are_not_synonyms(self):
        for slot, candidate_id in (
            ("genre", "wuxia_portrait"),
            ("subject", "wuxia_cosplay_model"),
            ("costume_style", "flowing_wuxia_robe"),
        ):
            with self.subTest(candidate_id=candidate_id):
                row = self.by_slot[slot][candidate_id]
                text = " ".join(
                    [
                        str(row.get("ko") or ""),
                        str(row.get("en") or ""),
                        *[str(value) for value in row.get("aliases") or []],
                        *[str(value) for value in row.get("keywords") or []],
                    ]
                ).casefold()
                self.assertNotIn("xianxia", text)
                self.assertNotIn("선협", text)
                self.assertNotIn("cosplay", text)
                self.assertNotIn("코스프레", text)

        xianxia_row = self.by_slot["world"]["xianxia_misty_realm"]
        xianxia_text = " ".join(
            [
                str(xianxia_row.get("ko") or ""),
                str(xianxia_row.get("en") or ""),
                *[str(value) for value in xianxia_row.get("aliases") or []],
                *[str(value) for value in xianxia_row.get("keywords") or []],
            ]
        ).casefold()
        self.assertNotIn("wuxia", xianxia_text)
        self.assertNotIn("무협", xianxia_text)

    def test_xia_relation_is_not_inferred_from_appearance_or_identity(self):
        profile_text = json.dumps(
            self.profiles["xia_protective_intervention_event"],
            ensure_ascii=False,
        ).casefold()
        self.assertIn("event geometry", profile_text)
        self.assertIn("rather than costume", profile_text)
        forbidden_positive_claims = {
            "ethnicity-specific face",
            "nationality-specific face",
            "same person as the reference",
            "morally good face",
            "virtuous face",
            "appearance proves virtue",
            "face proves faction",
        }
        all_expected_ids = set().union(*EXPECTED_BY_SLOT.values())
        for slot, rows in self.by_slot.items():
            for candidate_id, row in rows.items():
                if candidate_id not in all_expected_ids:
                    continue
                with self.subTest(slot=slot, candidate_id=candidate_id):
                    text = self.candidate_text(row)
                    for forbidden in forbidden_positive_claims:
                        self.assertNotIn(forbidden, text)

    def test_research_evidence_is_approved_source_bound_and_limited(self):
        rows = {
            row["id"]: row
            for row in (
                json.loads(line)
                for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
            if row.get("domain") == "wuxia_visual_semantics"
        }
        self.assertEqual(set(rows), EVIDENCE_IDS)
        all_candidate_ids = {
            str(row["id"])
            for slot_rows in self.tags["slots"].values()
            for row in slot_rows
            if isinstance(row, dict) and row.get("id")
        }
        for evidence_id, row in rows.items():
            with self.subTest(evidence_id=evidence_id):
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= all_candidate_ids)
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                self.assertTrue(row["affected_contract_ids"])
                for contract_id in row["affected_contract_ids"]:
                    kind, profile_id = contract_id.split(":", 1)
                    self.assertEqual(kind, "visual_obligation")
                    self.assertIn(profile_id, PROFILE_IDS)

    def test_registry_schema_is_valid_after_wuxia_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
