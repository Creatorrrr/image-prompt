from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_mythology_extension.json"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
EVIDENCE_PATH = (
    ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "earth-diver creation myth": "earth_diver_first_land_creation",
    "cosmic egg creation myth": "cosmic_egg_world_emergence",
    "world-parent separation myth": "world_parent_separation_creation",
    "mythic axis mundi": "axis_mundi_three_realm_connection",
    "Moirai life thread": "moirai_fate_thread_life_allocation",
    "mythic apotheosis of a mortal": (
        "mythic_apotheosis_mortal_divine_transition"
    ),
    "mythic katabasis into the underworld": (
        "katabasis_living_underworld_descent"
    ),
    "Egyptian weighing of the heart": "egyptian_heart_weighing_judgment",
    "great flood myth preservation vessel": "mythic_flood_preservation_vessel",
    "Chaoskampf cosmogonic combat": "chaoskampf_cosmogonic_ordering",
}

PROFILE_IDS = set(PROFILE_ROUTES.values())

EVIDENCE_IDS = {
    "mythology_oxford_earth_diver_creation",
    "mythology_oxford_cosmic_egg_creation",
    "mythology_teara_world_parent_separation",
    "mythology_met_axis_mundi_world_tree",
    "mythology_met_moirai_life_thread_roles",
    "mythology_british_museum_apotheosis_homer",
    "mythology_getty_katabasis_orpheus",
    "mythology_british_museum_egyptian_heart_weighing",
    "mythology_british_museum_flood_tablet_preservation",
    "mythology_oracc_combat_myth_ordering",
}

EXPECTED_SLOT_COUNTS = {
    "aesthetic_trend": 10,
    "subject": 10,
    "action": 10,
    "location": 10,
    "prop": 10,
    "composition": 10,
}


class PhotoMythologyVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.routing_index = prompt_generator.build_visual_profile_index_payload(
            cls.registry
        )
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
        }

    def hard_visual_matches(self, text: str) -> set[str]:
        resolution = prompt_generator.resolve_visual_profile_hits(
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
            visual_profile_index=self.routing_index,
            adult_context=True,
        )
        return {
            str(hit["profile_id"])
            for hit in resolution["hits"]
            if hit.get("match_basis") == "exact"
            and hit.get("hard_eligible") is True
        }

    def test_extension_has_sixty_complete_candidates_and_is_runtime_loaded(self):
        self.assertIn(
            EXTENSION_PATH.name,
            prompt_generator.RESEARCH_EXTENSION_FILENAMES,
        )
        self.assertEqual(
            {slot: len(rows) for slot, rows in self.extension["slots"].items()},
            EXPECTED_SLOT_COUNTS,
        )
        extension_ids: list[str] = []
        for slot, rows in self.extension["slots"].items():
            for row in rows:
                with self.subTest(slot=slot, candidate=row["id"]):
                    candidate_id = str(row["id"])
                    extension_ids.append(candidate_id)
                    self.assertIn(candidate_id, self.by_slot[slot])
                    self.assertTrue(row.get("ko"))
                    self.assertTrue(row.get("en"))
                    self.assertTrue(row.get("aliases"))
                    self.assertTrue(row.get("keywords"))
                    self.assertGreaterEqual(
                        len(str(row.get("embedding_text") or "").split()),
                        8,
                    )
                    self.assertIn("mythology", row.get("tags", []))
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)
        self.assertEqual(len(extension_ids), 60)
        self.assertEqual(len(extension_ids), len(set(extension_ids)))

    def test_visual_semantic_manifest_binds_each_cluster_to_one_profile(self):
        rows = self.extension["visual_semantics"]
        self.assertEqual(len(rows), 10)
        self.assertEqual({str(row["id"]) for row in rows}, PROFILE_IDS)

        all_candidate_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        bound_candidate_ids: list[str] = []
        for row in rows:
            with self.subTest(profile=row["hard_profile_id"]):
                self.assertEqual(row["id"], row["hard_profile_id"])
                self.assertIn(row["hard_profile_id"], self.profiles)
                self.assertEqual(len(row["component_groups"]), 5)
                self.assertGreaterEqual(len(row["confusion_boundaries"]), 4)
                self.assertEqual(len(row["candidate_ids"]), 6)
                self.assertTrue(set(row["candidate_ids"]) <= all_candidate_ids)
                bound_candidate_ids.extend(str(value) for value in row["candidate_ids"])
        self.assertEqual(len(bound_candidate_ids), 60)
        self.assertEqual(set(bound_candidate_ids), all_candidate_ids)

    def test_ten_profiles_have_five_component_evidence_and_render_gates(self):
        self.assertLessEqual(PROFILE_IDS, set(self.profiles))
        gate_ids: list[str] = []
        for profile_id in PROFILE_IDS:
            with self.subTest(profile=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], False)
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
                self.assertEqual(len(components["groups"]), 5)
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "native", "both"},
                )
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)
                gate_ids.extend(str(gate["id"]) for gate in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_direct_terms_route_to_only_the_intended_new_profile(self):
        for term, profile_id in PROFILE_ROUTES.items():
            with self.subTest(term=term):
                self.assertEqual(
                    self.hard_visual_matches(term) & PROFILE_IDS,
                    {profile_id},
                )

    def test_broad_terms_remain_advisory_and_do_not_force_new_profiles(self):
        broad_terms = (
            "myth",
            "mythology",
            "신화",
            "folklore",
            "legend",
            "pantheon",
            "creation",
            "cosmogony",
            "world tree",
            "axis mundi",
            "fate",
            "Moirai",
            "thread of destiny",
            "apotheosis",
            "katabasis",
            "underworld",
            "Anubis",
            "Thoth",
            "afterlife judgment",
            "flood",
            "ark",
            "dragon",
            "chaos",
            "order",
        )
        for term in broad_terms:
            with self.subTest(term=term):
                self.assertTrue(
                    self.hard_visual_matches(term).isdisjoint(PROFILE_IDS)
                )

    def test_close_substitutes_do_not_activate_mythology_profiles(self):
        substitutes = (
            "animal swimming in a lake",
            "ornate closed egg",
            "two distant giants",
            "giant decorative tree",
            "three women holding yarn",
            "glowing floating person",
            "ordinary cave exploration",
            "dead soul psychopomp escort",
            "generic scales of justice",
            "fishing boat in heavy rain",
            "hero fighting a random dragon",
        )
        for term in substitutes:
            with self.subTest(term=term):
                self.assertTrue(
                    self.hard_visual_matches(term).isdisjoint(PROFILE_IDS)
                )

    def test_research_evidence_is_approved_bound_and_culturally_limited(self):
        rows = {
            row["id"]: row
            for row in (
                json.loads(line)
                for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
            if row.get("id") in EVIDENCE_IDS
        }
        self.assertEqual(set(rows), EVIDENCE_IDS)

        extension_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        bound_candidate_ids: set[str] = set()
        for evidence_id, row in rows.items():
            with self.subTest(evidence=evidence_id):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["domain"], "mythology_visual_semantics")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertGreaterEqual(len(row["abstracted_dimensions"]), 3)
                self.assertGreaterEqual(len(row["research_limitations"]), 2)
                self.assertTrue(row["reuse_note"])
                self.assertTrue(set(row["candidate_ids"]) <= extension_ids)
                bound_candidate_ids.update(str(value) for value in row["candidate_ids"])
                self.assertEqual(len(row["affected_contract_ids"]), 1)
                contract_id = row["affected_contract_ids"][0]
                self.assertTrue(contract_id.startswith("visual_obligation:"))
                self.assertIn(contract_id.split(":", 1)[1], PROFILE_IDS)
        self.assertEqual(bound_candidate_ids, extension_ids)

    def test_registry_schema_accepts_mythology_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
