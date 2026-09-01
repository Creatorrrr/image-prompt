from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_space_extension.json"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "space-visual-semantics-20260901"
    / "evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "active comet coma tail system": "active_comet_coma_tail_system",
    "barred spiral galaxy structure": "barred_spiral_galaxy_structure",
    "interacting galaxies with tidal bridge": "interacting_galaxies_tidal_structure",
    "Einstein ring lens alignment": "einstein_ring_lens_alignment",
    "black hole shadow reconstruction": "black_hole_shadow_reconstruction",
    "relativistic accretion-disk visualization": (
        "relativistic_accretion_disk_visualization"
    ),
    "protostar disk bipolar outflow system": "protostar_disk_bipolar_outflow",
    "supernova remnant shock shell": "supernova_remnant_shock_shell",
    "auroral arc curtain atmosphere": "auroral_arc_curtain_atmosphere",
    "solar prominence magnetic loop": "solar_prominence_magnetic_loop",
    "solar flare active-region burst": "solar_flare_active_region_burst",
    "CME coronagraph snapshot": "cme_coronagraph_snapshot",
    "EVA spacewalk work system": "eva_spacewalk_work_system",
    "microgravity orbital interior": "microgravity_orbital_interior",
    "spacecraft docking capture alignment": (
        "spacecraft_docking_capture_alignment"
    ),
    "planetary rover surface operation": "planetary_rover_surface_operation",
}

PROFILE_IDS = set(PROFILE_ROUTES.values())

CLUSTER_PROFILE_IDS = {
    "small_body_encounter": "active_comet_coma_tail_system",
    "stellar_lifecycle_observation": "protostar_disk_bipolar_outflow",
    "galaxy_structure_observation": "interacting_galaxies_tidal_structure",
    "compact_object_visualization": "black_hole_shadow_reconstruction",
    "solar_space_weather": "cme_coronagraph_snapshot",
    "orbital_human_operations": "eva_spacewalk_work_system",
    "planetary_surface_exploration": "planetary_rover_surface_operation",
}


class PhotoSpaceVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.routing_index = prompt_generator.build_visual_profile_index_payload(
            cls.registry
        )
        cls.real_index = prompt_generator.load_visual_profile_index(
            INDEX_PATH,
            cls.registry,
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

    def test_sixteen_profiles_have_component_evidence_and_pixel_gates(self):
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
                self.assertGreaterEqual(components["minimum_component_groups"], 4)
                self.assertEqual(
                    len(components["required_group_ids"]),
                    len(components["groups"]),
                )
                self.assertGreaterEqual(len(profile["required_evidence_fields"]), 4)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertGreaterEqual(len(profile["render_gates"]), 4)
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 4)
                gate_ids.extend(str(gate["id"]) for gate in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_direct_terms_route_to_only_the_intended_new_profile(self):
        for term, profile_id in PROFILE_ROUTES.items():
            with self.subTest(term=term):
                self.assertEqual(
                    self.hard_visual_matches(term) & PROFILE_IDS,
                    {profile_id},
                )

    def test_real_generated_index_contains_all_space_profiles_and_vectors(self):
        self.assertEqual(
            self.real_index["registry_sha256"],
            prompt_generator.visual_profile_registry_sha256(self.registry),
        )
        for profile_id in PROFILE_IDS:
            with self.subTest(profile=profile_id):
                entry = self.real_index["entries"][profile_id]
                self.assertEqual(len(entry["vector"]), 768)
                self.assertTrue(entry["text"])
                exact_ids = {
                    row["profile_id"]
                    for row in self.real_index["exact_lookup"]
                    if row["profile_id"] == profile_id
                }
                self.assertEqual(exact_ids, {profile_id})

    def test_embedding_only_space_paraphrases_remain_optional_in_fake_vector_seam(self):
        selected = {
            "active_comet_coma_tail_system",
            "interacting_galaxies_tidal_structure",
            "eva_spacewalk_work_system",
            "planetary_rover_surface_operation",
        }
        for expected_id in selected:
            with self.subTest(profile=expected_id):
                paraphrase = self.profiles[expected_id]["semantics"][
                    "paraphrase_examples"
                ][0]
                vectors = {
                    profile["id"]: (
                        [1.0, 0.0]
                        if profile["id"] == expected_id
                        else [0.0, 1.0]
                    )
                    for profile in self.registry["profiles"]
                }
                fake_index = prompt_generator.build_visual_profile_index_payload(
                    self.registry,
                    vectors=vectors,
                    dimensions=2,
                )
                resolution = prompt_generator.resolve_visual_profile_hits(
                    self.registry,
                    [
                        {
                            "source": "authorial_core_interpretation",
                            "text": paraphrase,
                            "polarity": "advisory",
                        }
                    ],
                    visual_profile_index=fake_index,
                    query_text=paraphrase,
                    query_vector=[1.0, 0.0],
                    adult_context=True,
                )
                hit = next(
                    row
                    for row in resolution["hits"]
                    if row["profile_id"] == expected_id
                )
                self.assertEqual(hit["match_basis"], "embedding")
                self.assertFalse(hit["hard_eligible"])
                self.assertTrue(hit["optional_eligible"])

    def test_broad_space_terms_remain_advisory(self):
        broad_terms = (
            "space",
            "outer space",
            "universe",
            "cosmos",
            "우주",
            "galaxy",
            "은하",
            "star",
            "별",
            "black hole",
            "블랙홀",
            "planet",
            "행성",
            "astronaut",
            "우주비행사",
            "science fiction",
            "dark matter",
            "dark energy",
            "exoplanet",
            "pulsar",
            "wormhole",
            "warp drive",
            "Dyson sphere",
            "alien civilization",
            "terraforming",
        )
        for term in broad_terms:
            with self.subTest(term=term):
                self.assertTrue(self.hard_visual_matches(term).isdisjoint(PROFILE_IDS))

    def test_nearest_visual_substitutes_do_not_activate_space_profiles(self):
        substitutes = (
            "bare asteroid",
            "meteor streak in the atmosphere",
            "rocket exhaust plume",
            "ordinary spiral galaxy",
            "two unrelated galaxies",
            "glowing portal ring",
            "solar eclipse",
            "Saturn rings",
            "generic colorful nebula",
            "green storm clouds",
            "astronaut costume portrait in a studio",
            "person jumping inside a capsule set",
            "two spacecraft flying in formation",
            "stationary planetary lander",
            "toy rover portrait",
        )
        for term in substitutes:
            with self.subTest(term=term):
                self.assertTrue(self.hard_visual_matches(term).isdisjoint(PROFILE_IDS))

    def test_extension_has_eight_complete_six_slot_clusters(self):
        self.assertIn(
            EXTENSION_PATH.name,
            prompt_generator.RESEARCH_EXTENSION_FILENAMES,
        )
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
                        len(str(row.get("embedding_text") or "").split()),
                        8,
                    )
                    self.assertIn("space_visual_semantics", row.get("tags", []))
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)
        self.assertEqual(len(extension_ids), 48)
        self.assertEqual(len(extension_ids), len(set(extension_ids)))

    def test_cluster_manifest_binds_seven_hard_and_one_candidate_only_route(self):
        rows = {
            str(row["id"]): row for row in self.extension["visual_semantics"]
        }
        self.assertEqual(len(rows), 8)
        all_candidate_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        bound_candidate_ids: list[str] = []
        for cluster_id, profile_id in CLUSTER_PROFILE_IDS.items():
            row = rows[cluster_id]
            self.assertEqual(row["hard_profile_id"], profile_id)
            self.assertIn(profile_id, self.profiles)
            self.assertEqual(len(row["candidate_ids"]), 6)
            self.assertTrue(set(row["candidate_ids"]) <= all_candidate_ids)
            self.assertGreaterEqual(len(row["component_groups"]), 4)
            self.assertGreaterEqual(len(row["confusion_boundaries"]), 4)
            bound_candidate_ids.extend(str(value) for value in row["candidate_ids"])

        speculative = rows["speculative_space_systems"]
        self.assertIs(speculative["candidate_only"], True)
        self.assertNotIn("hard_profile_id", speculative)
        self.assertEqual(len(speculative["candidate_ids"]), 6)
        bound_candidate_ids.extend(
            str(value) for value in speculative["candidate_ids"]
        )
        self.assertEqual(set(bound_candidate_ids), all_candidate_ids)

    def test_representation_modes_keep_observation_and_concept_claims_separate(self):
        modes = {
            str(row["id"]): str(row["meaning"])
            for row in self.extension["representation_modes"]
        }
        self.assertEqual(
            set(modes),
            {
                "visible_light_observation",
                "false_color_or_multiwavelength",
                "measurement_reconstruction",
                "scientific_simulation_or_map",
                "artist_concept_or_fiction",
            },
        )
        speculative = next(
            row
            for row in self.extension["slots"]["aesthetic_trend"]
            if row["id"] == "space_speculative_systems_aesthetic"
        )
        self.assertIn("artist_concept_or_fiction", speculative["tags"])
        self.assertIn("never presented", speculative["embedding_text"])

    def test_research_evidence_is_approved_and_contract_bound(self):
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 16)
        extension_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        covered_profiles: set[str] = set()
        for row in rows:
            with self.subTest(evidence=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["domain"], "space_visual_semantics")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertGreaterEqual(len(row["abstracted_dimensions"]), 3)
                self.assertGreaterEqual(len(row["research_limitations"]), 2)
                self.assertTrue(row["reuse_note"])
                self.assertTrue(set(row["candidate_ids"]) <= extension_ids)
                for contract_id in row["affected_contract_ids"]:
                    self.assertTrue(contract_id.startswith("visual_obligation:"))
                    profile_id = contract_id.split(":", 1)[1]
                    self.assertIn(profile_id, PROFILE_IDS)
                    covered_profiles.add(profile_id)
        self.assertEqual(covered_profiles, PROFILE_IDS)

    def test_registry_schema_accepts_space_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
