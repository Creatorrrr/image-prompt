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
    / "fantasy-visual-semantics-20260901"
    / "evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "차원문": "fantasy_portal_two_world_threshold",
    "소환사": "summoner_distinct_entity_arrival",
    "연금술사": "alchemist_material_transmutation_process",
    "골렘": "golem_constructed_material_agency",
    "living armor": "living_armor_hollow_articulated_agency",
    "wyvern": "wyvern_two_leg_wing_tail_topology",
    "griffin": "griffin_eagle_lion_topology",
    "hippogriff": "hippogriff_eagle_horse_topology",
    "hydra monster": "hydra_multi_neck_single_body",
    "phoenix rebirth": "phoenix_rebirth_causal_cycle",
    "사역마": "familiar_practitioner_reciprocal_bond",
    "마법진": "magic_circle_local_rule_boundary",
}

PROFILE_IDS = set(PROFILE_ROUTES.values())

EXPECTED_BY_SLOT = {
    "subject": {
        "summoner_practitioner_role_model",
        "alchemist_practitioner_role_model",
        "constructed_golem_subject",
        "hollow_living_armor_subject",
        "heraldic_wyvern_subject",
        "griffin_eagle_lion_subject",
        "hippogriff_eagle_horse_subject",
        "hydra_multi_neck_subject",
        "phoenix_rebirth_subject",
    },
    "action": {
        "opening_two_world_threshold_crossing",
        "summoning_distinct_entity_arrival",
        "stabilizing_arrived_entity",
        "releasing_summoned_entity_return",
        "distilling_visible_material_transition",
        "testing_transmutation_sample",
        "cooling_transmuted_material",
        "directing_constructed_golem_task",
        "living_armor_independent_motion",
        "wyvern_spreading_wings_two_leg_profile",
        "griffin_turning_eagle_lion_profile",
        "hippogriff_turning_eagle_horse_profile",
        "hydra_necks_fanning_from_one_torso",
        "phoenix_emerging_from_ash_nest",
        "coordinating_familiar_shared_task",
        "closing_magic_circle_boundary",
    },
    "prop": {
        "bounded_summoning_anchor_prop",
        "portal_threshold_control_markers_prop",
        "alchemical_retort_crucible_prop",
        "paired_material_sample_prop",
        "familiar_shared_token_prop",
    },
    "location": {
        "summoning_observation_chamber",
        "two_world_portal_threshold_location",
        "alchemist_heatwork_lab",
        "fantasy_construct_test_court",
    },
    "surreal_physics_detail": {
        "portal_cross_boundary_parallax",
        "summoned_entity_contact_shadow_forming",
        "transmutation_boundary_material_gradient",
        "magic_circle_effect_boundary_stop",
    },
    "aftermath_trace": {
        "portal_crossing_residue_trace",
        "summoning_displaced_dust_trace",
        "transmutation_before_after_trace",
        "golem_task_material_trace",
        "phoenix_ash_to_feather_trace",
    },
}

EVIDENCE_IDS = {
    "fantasy_portal_sfe_transport_boundary",
    "fantasy_summoner_folger_operator_apparition",
    "fantasy_alchemy_shi_workshop_process",
    "fantasy_golem_jewish_museum_construct_agency",
    "fantasy_living_armor_met_articulation",
    "fantasy_wyvern_british_museum_heraldic_topology",
    "fantasy_griffin_met_eagle_lion_topology",
    "fantasy_hippogriff_ariosto_princeton_eagle_horse_topology",
    "fantasy_hydra_met_multi_head_boundary",
    "fantasy_phoenix_met_rebirth_cycle",
    "fantasy_familiar_folger_helper_relation_boundary",
    "fantasy_magic_circle_wellcome_bounded_structure",
}


class PhotoFantasyVisualSemanticsTests(unittest.TestCase):
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

    def test_twelve_profiles_have_component_evidence_and_pixel_gates(self):
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
                gate_ids.extend(str(gate["id"]) for gate in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_direct_terms_route_to_only_the_intended_new_profile(self):
        for term, profile_id in PROFILE_ROUTES.items():
            with self.subTest(term=term):
                matched_new = set(self.hard_visual_matches(term)) & PROFILE_IDS
                self.assertEqual(matched_new, {profile_id})

    def test_adjacent_and_broad_terms_do_not_force_new_profiles(self):
        negatives = (
            "portal site",
            "login portal",
            "ordinary mirror",
            "glowing ring",
            "companion portrait",
            "necromancer",
            "corpse",
            "potion bottle",
            "chemist portrait",
            "colored smoke",
            "statue",
            "humanoid robot",
            "armored knight",
            "armor mannequin",
            "dragon",
            "pegasus",
            "cerberus",
            "fire bird",
            "cat portrait",
            "circular rug",
            "fantasy",
            "high fantasy",
            "grimdark",
            "cozy fantasy",
            "wizard",
            "sorcerer",
            "warlock",
            "hard magic",
            "elf",
            "orc",
            "fairy",
        )
        for negative in negatives:
            with self.subTest(negative=negative):
                self.assertTrue(
                    (set(self.hard_visual_matches(negative)) & PROFILE_IDS) == set()
                )

    def test_griffin_hippogriff_and_wyvern_boundaries_remain_separate(self):
        distinctions = {
            "eagle lion griffin": "griffin_eagle_lion_topology",
            "eagle horse hippogriff": "hippogriff_eagle_horse_topology",
            "two-legged wyvern": "wyvern_two_leg_wing_tail_topology",
        }
        for phrase, expected in distinctions.items():
            with self.subTest(phrase=phrase):
                self.assertEqual(
                    set(self.hard_visual_matches(phrase)) & PROFILE_IDS,
                    {expected},
                )
        wyvern_definition = self.profiles[
            "wyvern_two_leg_wing_tail_topology"
        ]["semantics"]["definition"].casefold()
        self.assertIn("user definition overrides", wyvern_definition)

    def test_candidate_pack_contains_complete_relation_clusters(self):
        self.assertGreaterEqual(
            tuple(int(part) for part in str(self.tags["version"]).split(".")),
            (1, 37),
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

    def test_summoner_and_alchemist_roles_have_identity_and_four_scenes(self):
        expected = {
            "소환사": "summoner_practitioner_role_model",
            "연금술사": "alchemist_practitioner_role_model",
        }
        for role_name, subject_id in expected.items():
            with self.subTest(role_name=role_name):
                role = self.recipes["roles"][role_name]
                self.assertEqual(role["identity_core"], {"subject": subject_id})
                self.assertEqual(len(role["scene_variants"]), 4)
                self.assertEqual(
                    len({scene["id"] for scene in role["scene_variants"]}), 4
                )
                for scene in role["scene_variants"]:
                    for slot, candidate_id in scene["set"].items():
                        self.assertIn(candidate_id, self.by_slot[slot])
                self.assertGreaterEqual(len(role["additional"]), 3)
                self.assertGreaterEqual(len(role["review_gates"]), 2)

    def test_role_aliases_are_narrow_and_do_not_claim_adjacent_classes(self):
        aliases = self.recipes["aliases"]
        self.assertEqual(aliases["summoner"], "소환사")
        self.assertEqual(aliases["alchemist"], "연금술사")
        for forbidden in ("conjurer", "stage magician", "wizard", "sorcerer"):
            self.assertNotEqual(aliases.get(forbidden), "소환사")
        for forbidden in ("chemist", "apothecary", "herbalist", "witch"):
            self.assertNotEqual(aliases.get(forbidden), "연금술사")

    def test_research_evidence_is_approved_bound_and_limited(self):
        rows = {
            row["id"]: row
            for row in (
                json.loads(line)
                for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
        }
        self.assertEqual(set(rows), EVIDENCE_IDS)
        all_candidates = set().union(*EXPECTED_BY_SLOT.values())
        for evidence_id in EVIDENCE_IDS:
            with self.subTest(evidence_id=evidence_id):
                row = rows[evidence_id]
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                self.assertTrue(set(row["candidate_ids"]) <= all_candidates)
                for contract_id in row["affected_contract_ids"]:
                    self.assertTrue(contract_id.startswith("visual_obligation:"))
                    self.assertIn(contract_id.split(":", 1)[1], PROFILE_IDS)

    def test_registry_schema_accepts_fantasy_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
