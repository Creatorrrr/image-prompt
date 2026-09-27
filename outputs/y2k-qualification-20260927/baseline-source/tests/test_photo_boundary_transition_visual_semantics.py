from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EXTENSION_PATH = (
    SKILL_DIR / "assets" / "photo_prompt_boundary_transition_extension.json"
)
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "boundary-transition-visual-semantics-20260901"
    / "evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "visible pretransition critical threshold": (
        "critical_threshold_pretransition_accumulation"
    ),
    "visible physical barrier breakthrough": "barrier_breakthrough_causal_event",
    "sealed power limiter release": "dormant_capacity_limiter_release",
    "progressive rated-system overload failure": (
        "technical_overload_progressive_failure"
    ),
    "visible phase transition by nucleation and growth": (
        "phase_transition_nucleation_growth"
    ),
    "visible point-of-no-return crossing": (
        "irreversible_threshold_crossing_consequence"
    ),
}

PROFILE_IDS = set(PROFILE_ROUTES.values())

CLUSTER_PROFILES = {
    "critical_threshold_pretransition": {
        "critical_threshold_pretransition_accumulation"
    },
    "barrier_breakthrough": {"barrier_breakthrough_causal_event"},
    "dormant_limiter_release": {"dormant_capacity_limiter_release"},
    "technical_overload": {"technical_overload_progressive_failure"},
    "phase_transition": {"phase_transition_nucleation_growth"},
    "irreversible_crossing": {
        "irreversible_threshold_crossing_consequence"
    },
}


class PhotoBoundaryTransitionVisualSemanticsTests(unittest.TestCase):
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

    def test_six_profiles_have_five_component_groups_and_pixel_gates(self):
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

    def test_broad_limit_transcendence_terms_remain_advisory(self):
        broad_terms = (
            "limit",
            "threshold",
            "extreme",
            "peak",
            "breakthrough",
            "awakening",
            "release",
            "overload",
            "phase transition",
            "point of no return",
            "transcendence",
            "ascension",
            "singularity",
            "absolute",
            "infinity",
            "evolution",
            "한계",
            "문턱",
            "임계점",
            "극한",
            "돌파",
            "각성",
            "해제",
            "과부하",
            "상전이",
            "초월",
            "승천",
            "특이점",
            "절대",
            "무한",
            "진화",
        )
        for term in broad_terms:
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), set())

    def test_nearest_substitutes_do_not_activate_new_profiles(self):
        substitutes = (
            "A nervous portrait beside an unrelated gauge",
            "A victorious climber standing on a mountain summit",
            "An explosion in open air with no barrier",
            "A person walking through a normal doorway",
            "A sleeping person opening their eyes",
            "A costume change with glowing eyes",
            "A single electrical spark after an external impact",
            "A short circuit with no rated load reference",
            "Two unrelated materials under colored lighting",
            "Smoke and aura around a finished crystal",
            "A one-way road sign beside a standing person",
            "A glowing black orb used as a singularity icon",
        )
        for text in substitutes:
            with self.subTest(text=text):
                self.assertEqual(self.hard_visual_matches(text), set())

    def test_extension_has_six_complete_six_slot_clusters(self):
        self.assertIn(
            EXTENSION_PATH.name,
            prompt_generator.RESEARCH_EXTENSION_FILENAMES,
        )
        self.assertEqual(
            {slot: len(rows) for slot, rows in self.extension["slots"].items()},
            {
                "aesthetic_trend": 6,
                "subject": 6,
                "action": 6,
                "location": 6,
                "prop": 6,
                "composition": 6,
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
                    self.assertIn(
                        "boundary_transition_visual_semantics",
                        row.get("tags", []),
                    )
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)
        self.assertEqual(len(extension_ids), 36)
        self.assertEqual(len(extension_ids), len(set(extension_ids)))

    def test_cluster_manifest_binds_every_profile_and_candidate_once(self):
        rows = {
            str(row["id"]): row for row in self.extension["visual_semantics"]
        }
        self.assertEqual(set(rows), set(CLUSTER_PROFILES))
        all_candidate_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        bound_profiles: set[str] = set()
        bound_candidates: list[str] = []
        for cluster_id, expected_profiles in CLUSTER_PROFILES.items():
            with self.subTest(cluster=cluster_id):
                row = rows[cluster_id]
                self.assertEqual(set(row["hard_profile_ids"]), expected_profiles)
                self.assertEqual(len(row["component_groups"]), 5)
                self.assertEqual(len(row["confusion_boundaries"]), 5)
                self.assertEqual(len(row["candidate_ids"]), 6)
                self.assertTrue(set(row["candidate_ids"]) <= all_candidate_ids)
                bound_profiles.update(row["hard_profile_ids"])
                bound_candidates.extend(row["candidate_ids"])
        self.assertEqual(bound_profiles, PROFILE_IDS)
        self.assertEqual(set(bound_candidates), all_candidate_ids)
        self.assertEqual(len(bound_candidates), len(set(bound_candidates)))

    def test_research_evidence_is_approved_and_contract_bound(self):
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 9)
        extension_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        covered_profiles: set[str] = set()
        for row in rows:
            with self.subTest(evidence=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["domain"], "boundary_transition_visual_semantics")
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

    def test_registry_schema_accepts_boundary_transition_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
