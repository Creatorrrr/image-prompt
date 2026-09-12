from __future__ import annotations

import json
import re
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
    "rapier": "rapier_acute_point_elaborate_guard",
    "할버드": "halberd_axe_point_rear_spike",
    "compound bow": "compound_bow_cam_cable_system",
    "석궁": "crossbow_stock_prod_release_system",
    "revolver": "revolver_chambered_cylinder_system",
    "박격포": "ground_mortar_tube_bipod_baseplate_system",
}

PROFILE_IDS = set(PROFILE_ROUTES.values())

EXPECTED_BY_SLOT = {
    "action": {
        "presenting_rapier_guard_and_point",
        "presenting_halberd_full_head_profile",
        "holding_compound_bow_cams_visible",
        "supporting_crossbow_mechanism_profile",
        "presenting_revolver_cylinder_profile",
        "examining_ground_mortar_mount_system",
    },
    "prop": {
        "rapier_museum_reference_prop",
        "halberd_museum_replica_prop",
        "compound_bow_cam_cable_reference_prop",
        "deactivated_crossbow_display_prop",
        "nonfunctional_revolver_prop",
        "ground_mortar_system_reference_prop",
    },
}

EVIDENCE_IDS = {
    "weapon_rapier_met_acute_point_guard",
    "weapon_halberd_met_composite_head",
    "weapon_compound_bow_world_archery_pulleys_cables",
    "weapon_crossbow_met_transverse_longitudinal_topology",
    "weapon_revolver_atf_chambered_cylinder_boundary",
    "weapon_ground_mortar_army_tube_bipod_baseplate",
}


class PhotoWeaponVisualSemanticsTests(unittest.TestCase):
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
        ).lower()

    def test_six_profiles_have_complete_component_evidence_and_pixel_gates(self):
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
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
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
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

    def test_exact_terms_route_to_only_the_intended_weapon_profile(self):
        for term, profile_id in PROFILE_ROUTES.items():
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), [profile_id])

        paired_terms = {
            "레이피어": "rapier_acute_point_elaborate_guard",
            "halberd": "halberd_axe_point_rear_spike",
            "컴파운드 보우": "compound_bow_cam_cable_system",
            "crossbow": "crossbow_stock_prod_release_system",
            "리볼버": "revolver_chambered_cylinder_system",
            "ground mortar system": "ground_mortar_tube_bipod_baseplate_system",
        }
        for term, profile_id in paired_terms.items():
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), [profile_id])

    def test_adjacent_and_generic_terms_do_not_force_the_six_profiles(self):
        negatives = (
            "greatsword",
            "plain medieval sword",
            "spear",
            "glaive",
            "poleaxe",
            "recurve bow",
            "longbow",
            "bow",
            "활",
            "semi-automatic pistol",
            "handgun",
            "권총",
            "kitchen mortar and pestle",
            "mortar and pestle",
            "wheeled cannon",
            "shoulder launcher",
            "weapon portrait",
            "real weapon",
        )
        for negative in negatives:
            with self.subTest(negative=negative):
                self.assertTrue(
                    set(self.hard_visual_matches(negative)).isdisjoint(PROFILE_IDS)
                )

    def test_candidate_pack_contains_bounded_action_and_prop_pairs(self):
        version = tuple(int(part) for part in str(self.tags["version"]).split("."))
        self.assertGreaterEqual(version, (1, 34))
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

    def test_exact_prop_aliases_do_not_collapse_adjacent_weapon_classes(self):
        forbidden_aliases = {
            "medieval_longsword_replica_prop": {
                "greatsword",
                "broadsword",
                "대검",
                "검",
            },
            "replica_spear_prop": {"lance", "polearm", "랜스", "장병기"},
            "halberd_museum_replica_prop": {
                "glaive",
                "poleaxe",
                "폴암",
                "장병기",
            },
            "wooden_training_bow_prop": {"longbow", "recurve bow"},
            "deactivated_crossbow_display_prop": {"bow", "archery bow", "활"},
            "nonfunctional_revolver_prop": {"pistol", "handgun", "권총", "총"},
            "nonfunctional_modern_rifle_prop": {
                "assault rifle",
                "automatic rifle",
                "돌격소총",
                "카빈",
            },
        }
        for candidate_id, forbidden in forbidden_aliases.items():
            with self.subTest(candidate_id=candidate_id):
                aliases = {
                    str(value).casefold()
                    for value in self.by_slot["prop"][candidate_id].get("aliases", [])
                }
                self.assertTrue({value.casefold() for value in forbidden}.isdisjoint(aliases))

    def test_profiles_describe_external_morphology_without_state_claims(self):
        forbidden_tokens = {"functional", "operational", "deactivated", "inert", "safe"}
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile_text = json.dumps(
                    self.profiles[profile_id], ensure_ascii=False
                ).casefold()
                tokens = set(re.findall(r"[a-z]+", profile_text))
                self.assertTrue(forbidden_tokens.isdisjoint(tokens))

    def test_research_evidence_is_approved_source_bound_and_limited(self):
        rows = {
            row["id"]: row
            for row in (
                json.loads(line)
                for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
            if row["id"] in EVIDENCE_IDS
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
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                self.assertEqual(len(row["affected_contract_ids"]), 1)
                contract_id = row["affected_contract_ids"][0]
                kind, profile_id = contract_id.split(":", 1)
                self.assertEqual(kind, "visual_obligation")
                self.assertIn(profile_id, PROFILE_IDS)

    def test_registry_schema_is_valid_after_weapon_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
