from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_imaginal_extension.json"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "imaginal-visual-semantics-20260901"
    / "evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "dream logic scene": "oneiric_dream_logic_discontinuity",
    "ambiguous figure": "ambiguous_figure_ground_dual_read",
    "impossible object": "impossible_object_global_connection",
    "liminal space": "liminal_transition_use_gap",
    "magical realism": "magical_realism_matter_of_fact_anomaly",
    "independent reflection": "mirror_reflection_action_mismatch",
    "face pareidolia": "face_pareidolia_embedded_nonface_pattern",
    "visible metamorphosis": "continuous_metamorphosis_source_target_bridge",
    "phantasmagoria projection": "phantasmagoria_projected_spectral_sequence",
}

PROFILE_IDS = set(PROFILE_ROUTES.values())

EXPECTED_SLOT_COUNTS = {
    "subject": 2,
    "action": 9,
    "prop": 4,
    "location": 5,
    "composition": 5,
    "surreal_concept": 14,
    "surreal_anchor": 5,
    "surreal_physics_detail": 8,
    "reflection_logic": 2,
    "transition_stage": 1,
    "aftermath_trace": 2,
}

EVIDENCE_IDS = {
    "imaginal_dream_bizarreness_hobson",
    "imaginal_lucid_dream_meta_awareness_baird",
    "imaginal_hallucination_illusion_stimulus_boundary",
    "imaginal_ambiguous_figures_percept_reversal",
    "imaginal_impossible_objects_penrose_connection",
    "imaginal_liminal_place_diel_lewis",
    "imaginal_magical_realism_cambridge_naturalized_anomaly",
    "imaginal_mirror_reflection_alignment_openstax",
    "imaginal_pareidolia_nonface_pattern",
    "imaginal_chronophoto_metamorphosis_bridge",
    "imaginal_phantasmagoria_projection_medium",
    "imaginal_surrealism_strategy_not_style",
    "imaginal_time_memory_same_anchor_advisory",
    "imaginal_mirage_natural_optics_boundary",
    "imaginal_afterimage_temporal_inducer_boundary",
}


class PhotoImaginalVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
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
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
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

    def test_extension_has_fifty_seven_complete_candidates_and_is_loaded(self):
        self.assertIn(EXTENSION_PATH.name, prompt_generator.RESEARCH_EXTENSION_FILENAMES)
        self.assertEqual(
            {slot: len(rows) for slot, rows in self.extension["slots"].items()},
            EXPECTED_SLOT_COUNTS,
        )
        extension_ids: list[str] = []
        for slot, rows in self.extension["slots"].items():
            for row in rows:
                with self.subTest(slot=slot, candidate=row["id"]):
                    extension_ids.append(str(row["id"]))
                    self.assertIn(row["id"], self.by_slot[slot])
                    self.assertTrue(row.get("ko"))
                    self.assertTrue(row.get("en"))
                    self.assertTrue(row.get("aliases"))
                    self.assertTrue(row.get("keywords"))
                    self.assertGreaterEqual(
                        len(str(row.get("embedding_text") or "").split()), 8
                    )
                    self.assertIn("imaginal", row.get("tags", []))
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)
        self.assertEqual(len(extension_ids), 57)
        self.assertEqual(len(extension_ids), len(set(extension_ids)))

    def test_nine_profiles_have_five_component_groups_and_pixel_gates(self):
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
                    {"thumbnail", "both", "native"},
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

    def test_broad_advisory_and_neighbor_terms_do_not_force_new_profiles(self):
        broad_terms = (
            "fantasy",
            "dream",
            "dreamscape",
            "dreamy portrait",
            "oneiric portrait",
            "lucid dream",
            "hallucination",
            "visual hallucination",
            "surreal",
            "surrealism",
            "otherworldly",
            "ethereal",
            "mirage",
            "Fata Morgana",
            "afterimage",
            "time loop",
            "memory echo",
            "magical",
            "mirror",
            "empty mall",
            "transformation",
            "ghost",
            "phantom",
            "apparition",
            "phantasm",
            "floating island",
            "bioluminescence",
            "iridescence",
        )
        for term in broad_terms:
            with self.subTest(term=term):
                self.assertTrue(
                    self.hard_visual_matches(term).isdisjoint(PROFILE_IDS)
                )

    def test_close_visual_substitutes_do_not_activate_new_profiles(self):
        substitutes = (
            "empty room",
            "abandoned mall",
            "ordinary corridor",
            "ordinary mirror selfie",
            "twin portrait",
            "double exposure portrait",
            "painted face on a wall",
            "carved stone face",
            "costume change",
            "before and after transformation panels",
            "projector on a stage",
            "single hologram",
            "actual ghost in a room",
            "soft focus pastel portrait",
            "random floating stairs",
            "two pictures side by side",
        )
        for term in substitutes:
            with self.subTest(term=term):
                self.assertTrue(
                    self.hard_visual_matches(term).isdisjoint(PROFILE_IDS)
                )

    def test_research_evidence_is_approved_bound_and_limited(self):
        extension_ids = {
            str(row["id"])
            for rows in self.extension["slots"].values()
            for row in rows
        }
        rows = {
            row["id"]: row
            for row in (
                json.loads(line)
                for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
        }
        self.assertEqual(set(rows), EVIDENCE_IDS)
        bound_candidates: set[str] = set()
        for evidence_id, row in rows.items():
            with self.subTest(evidence=evidence_id):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["domain"], "imaginal_visual_semantics")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                self.assertTrue(set(row["candidate_ids"]) <= extension_ids)
                bound_candidates.update(str(value) for value in row["candidate_ids"])
                for contract_id in row["affected_contract_ids"]:
                    kind, value = contract_id.split(":", 1)
                    self.assertEqual(kind, "visual_obligation")
                    self.assertIn(value, PROFILE_IDS)
        self.assertEqual(bound_candidates, extension_ids)

    def test_registry_schema_accepts_imaginal_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])

    def test_embedding_only_paraphrase_remains_optional(self):
        target_id = "oneiric_dream_logic_discontinuity"
        vectors = {
            profile["id"]: (
                [1.0, 0.0] if profile["id"] == target_id else [0.0, 1.0]
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
                    "text": (
                        "ordinary recognizable room route furniture or routine; one "
                        "bounded change of orientation scale adjacency or continuity; "
                        "the same distinctive object pattern or threshold appears on both "
                        "sides; one person or object remains identifiable across the "
                        "impossible join; light perspective contact or shadow localizes "
                        "the break to one seam"
                    ),
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text="localized discontinuity in a familiar scene",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        hit = next(row for row in resolution["hits"] if row["profile_id"] == target_id)
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_generated_index_is_bound_to_every_imaginal_profile(self):
        exact_by_profile = {
            profile_id: {
                row["term"]
                for row in self.index["exact_lookup"]
                if row["profile_id"] == profile_id
            }
            for profile_id in PROFILE_IDS
        }
        for profile_id in PROFILE_IDS:
            with self.subTest(profile=profile_id):
                self.assertIn(profile_id, self.index["entries"])
                self.assertEqual(
                    exact_by_profile[profile_id],
                    set(self.profiles[profile_id]["activation"]["exact_terms"]),
                )


if __name__ == "__main__":
    unittest.main()
