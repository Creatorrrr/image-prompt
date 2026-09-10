from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_legend_extension.json"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "legend-visual-semantics-20260901"
    / "evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "visible local legend transmission at its site": "local_legend_site_transmission",
    "legendary rock trace as site evidence": "legendary_rock_trace_evidence",
    "visible legendary landform-origin event": "legendary_landform_origin_causality",
    "guarded hidden treasure attempt visibly failing": "guarded_hidden_treasure_attempt_failure",
    "submerged settlement with in-situ architecture": "submerged_settlement_in_situ_structure",
    "former vessel breaking into spectral continuity": "ghost_ship_former_vessel_breach",
}

PROFILE_IDS = set(PROFILE_ROUTES.values())
EXISTING_REUSED_PROFILE_ID = "continuous_metamorphosis_source_target_bridge"

CLUSTER_PROFILES = {
    "local_legend_site_transmission": {"local_legend_site_transmission"},
    "legendary_rock_trace_evidence": {"legendary_rock_trace_evidence"},
    "legendary_landform_origin_causality": {
        "legendary_landform_origin_causality"
    },
    "guarded_hidden_treasure_attempt_failure": {
        "guarded_hidden_treasure_attempt_failure"
    },
    "submerged_settlement_in_situ_structure": {
        "submerged_settlement_in_situ_structure"
    },
    "ghost_ship_former_vessel_breach": {"ghost_ship_former_vessel_breach"},
    "stone_transformation_trace": {EXISTING_REUSED_PROFILE_ID},
    "prophecy_lineage_return_cycle": set(),
}


class PhotoLegendVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
        }
        cls.routing_registry = {
            **cls.registry,
            "profiles": [
                profile
                for profile in cls.registry["profiles"]
                if str(profile.get("id") or "") in PROFILE_IDS
            ],
        }
        cls.routing_index = prompt_generator.build_visual_profile_index_payload(
            cls.routing_registry
        )
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }

    def hard_visual_matches(self, text: str) -> set[str]:
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.routing_registry,
            [
                {
                    "source": "concept_lock",
                    "text": text,
                    "polarity": "required",
                    "priority": "critical",
                    "mandatory": True,
                },
                {
                    "source": "authorial_core_interpreted_intent",
                    "text": text,
                    "polarity": "required",
                    "priority": "critical",
                    "mandatory": True,
                },
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

    def test_six_new_profiles_have_five_components_fields_and_pixel_gates(self):
        self.assertLessEqual(PROFILE_IDS, set(self.profiles))
        gate_ids: list[str] = []
        for profile_id in PROFILE_IDS:
            with self.subTest(profile=profile_id):
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
                self.assertEqual(
                    set(components["required_group_ids"]),
                    {row["id"] for row in components["groups"]},
                )
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)
                gate_ids.extend(str(gate["id"]) for gate in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_narrow_exact_terms_route_to_exactly_one_new_profile(self):
        for text, profile_id in PROFILE_ROUTES.items():
            with self.subTest(profile=profile_id):
                self.assertEqual(self.hard_visual_matches(text), {profile_id})

    def test_broad_legend_terms_remain_advisory(self):
        broad_terms = (
            "legend",
            "legendary",
            "folklore",
            "heroic legend",
            "ancient legend",
            "cursed",
            "lost kingdom",
            "prophecy",
            "fate",
            "lineage",
            "returning king",
            "memorate",
            "contemporary legend",
            "urban legend",
            "legend cycle",
            "variant",
            "localization",
            "전설",
            "전설적인",
            "민간전승",
            "예언",
            "운명",
            "혈통",
            "왕의 귀환",
            "현대전설",
            "도시전설",
            "전설군",
            "변이",
            "지역화",
        )
        for term in broad_terms:
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), set())

    def test_nearest_substitutes_do_not_activate_new_profiles(self):
        substitutes = (
            "A generic storyteller portrait in a studio",
            "Tourists standing near an atmospheric ruin",
            "An ordinary weathered boulder with painted footprints",
            "A hero posing on a finished mountain",
            "An open treasure chest portrait with a guard nearby",
            "A successful treasure handoff after the fight",
            "A single shipwreck surrounded by scattered amphorae",
            "A fantasy palace glowing under blue water",
            "A foggy abandoned ship with an empty deck",
            "A fully translucent boat floating above the sea",
        )
        for text in substitutes:
            with self.subTest(text=text):
                self.assertEqual(self.hard_visual_matches(text), set())

    def test_extension_has_eight_complete_six_slot_clusters(self):
        self.assertIn(EXTENSION_PATH.name, prompt_generator.RESEARCH_EXTENSION_FILENAMES)
        self.assertEqual(
            {slot: len(rows) for slot, rows in self.extension["slots"].items()},
            {
                "aesthetic_trend": 8,
                "subject": 8,
                "action": 8,
                "location": 8,
                "prop": 8,
                "composition": 8,
            },
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
                        len(str(row.get("embedding_text") or "").split()), 8
                    )
                    self.assertIn("legend_visual_semantics", row.get("tags", []))
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)
        self.assertEqual(len(extension_ids), 48)
        self.assertEqual(len(extension_ids), len(set(extension_ids)))

    def test_cluster_manifest_binds_profiles_candidates_and_advisory_row(self):
        rows = {
            str(row["id"]): row for row in self.extension["visual_semantics"]
        }
        self.assertEqual(set(rows), set(CLUSTER_PROFILES))
        all_candidate_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        bound_candidates: list[str] = []
        for cluster_id, expected_profiles in CLUSTER_PROFILES.items():
            with self.subTest(cluster=cluster_id):
                row = rows[cluster_id]
                self.assertEqual(set(row["hard_profile_ids"]), expected_profiles)
                self.assertEqual(len(row["component_groups"]), 5)
                self.assertEqual(len(row["confusion_boundaries"]), 5)
                self.assertEqual(len(row["candidate_ids"]), 6)
                self.assertTrue(set(row["candidate_ids"]) <= all_candidate_ids)
                bound_candidates.extend(row["candidate_ids"])
        self.assertIs(rows["prophecy_lineage_return_cycle"]["candidate_only"], True)
        self.assertEqual(
            set(rows["stone_transformation_trace"]["hard_profile_ids"]),
            {EXISTING_REUSED_PROFILE_ID},
        )
        self.assertEqual(set(bound_candidates), all_candidate_ids)
        self.assertEqual(len(bound_candidates), len(set(bound_candidates)))

    def test_research_evidence_is_approved_and_contract_bound(self):
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 11)
        extension_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        covered_profiles: set[str] = set()
        for row in rows:
            with self.subTest(evidence=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["domain"], "legend_visual_semantics")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertGreaterEqual(len(row["abstracted_dimensions"]), 3)
                self.assertGreaterEqual(len(row["research_limitations"]), 2)
                self.assertTrue(row["reuse_note"])
                self.assertTrue(set(row["candidate_ids"]) <= extension_ids)
                for contract_id in row["affected_contract_ids"]:
                    self.assertTrue(contract_id.startswith("visual_obligation:"))
                    profile_id = contract_id.split(":", 1)[1]
                    self.assertIn(
                        profile_id, PROFILE_IDS | {EXISTING_REUSED_PROFILE_ID}
                    )
                    covered_profiles.add(profile_id)
        self.assertLessEqual(PROFILE_IDS, covered_profiles)
        self.assertIn(EXISTING_REUSED_PROFILE_ID, covered_profiles)

    def test_real_generated_index_contains_new_profiles_and_vectors(self):
        real_index = prompt_generator.load_visual_profile_index(
            INDEX_PATH,
            self.registry,
        )
        self.assertEqual(
            real_index["registry_sha256"],
            prompt_generator.visual_profile_registry_sha256(self.registry),
        )
        for profile_id in PROFILE_IDS:
            with self.subTest(profile=profile_id):
                entry = real_index["entries"][profile_id]
                self.assertEqual(len(entry["vector"]), 768)
                self.assertTrue(entry["text"])

    def test_registry_schema_accepts_legend_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
