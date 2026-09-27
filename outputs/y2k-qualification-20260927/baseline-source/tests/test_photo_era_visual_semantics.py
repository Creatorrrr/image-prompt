from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
VISUAL_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
SEMANTIC_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_semantic_index.json"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
RESEARCH_DIR = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "photo-era-visual-semantics-20260905"
)
PROPOSAL_PATH = RESEARCH_DIR / "candidate-data-proposal.json"
ROUTING_PATH = RESEARCH_DIR / "routing-regression-proposal.jsonl"
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "photo_era_three_arm_pixel_test_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


class PhotoEraVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.proposal = json.loads(PROPOSAL_PATH.read_text(encoding="utf-8"))
        cls.routing_rows = [
            json.loads(line)
            for line in ROUTING_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"]}
        cls.profile_ids = {row["id"] for row in cls.proposal["proposed_profiles"]}
        cls.visual_index = prompt_generator.load_visual_profile_index(
            VISUAL_INDEX_PATH,
            cls.registry,
            provider=prompt_generator.SEMANTIC_PROVIDER,
            model=prompt_generator.SEMANTIC_MODEL_ID,
            dimensions=prompt_generator.DEFAULT_SEMANTIC_DIMENSIONS,
        )
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.entries_by_slot = {
            slot: {row["id"]: row for row in entries}
            for slot, entries in cls.tags["slots"].items()
        }
        cls.photo_era_exact_lookup = [
            row
            for row in cls.visual_index["exact_lookup"]
            if row["profile_id"] in cls.profile_ids
        ]

    def hard_matches(self, text: str) -> set[str]:
        rows = [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            }
        ]
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            rows,
            visual_profile_index=self.visual_index,
            adult_context=True,
        )
        return {
            hit["profile_id"]
            for hit in resolution["hits"]
            if hit["match_basis"] == "exact" and hit["hard_eligible"] is True
        }

    def indexed_exact_matches(self, text: str) -> set[str]:
        return {
            row["profile_id"]
            for row in self.photo_era_exact_lookup
            if prompt_generator.intent_alias_matches(text, row["term"])
            and not prompt_generator.candidate_pack_intent_term_is_negated(
                text, row["term"]
            )
        }

    def test_all_eighteen_profiles_are_complete_strict_contracts(self) -> None:
        self.assertEqual(len(self.profile_ids), 18)
        self.assertTrue(self.profile_ids <= set(self.profiles))
        all_gate_ids = [
            gate["id"]
            for profile in self.registry["profiles"]
            for gate in profile["render_gates"]
        ]
        self.assertEqual(len(all_gate_ids), len(set(all_gate_ids)))
        for profile_id in self.profile_ids:
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
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertEqual(len(profile["reject_substitutes"]), 5)

    def test_bilingual_narrow_exact_terms_have_single_profile_owners(self) -> None:
        for source_profile in self.proposal["proposed_profiles"]:
            profile_id = source_profile["id"]
            for exact_term in source_profile["exact_terms"]:
                with self.subTest(profile_id=profile_id, exact_term=exact_term):
                    self.assertEqual(
                        self.indexed_exact_matches(exact_term), {profile_id}
                    )

    def test_runtime_resolver_preserves_representative_exact_ownership(self) -> None:
        cases = {
            "reflective cased daguerreotype plate object":
                "daguerreotype_reflective_cased_plate_object",
            "오토크롬 유리 투명판 색소 스크린 객체":
                "autochrome_glass_transparency_color_screen",
            "computational multi-frame HDR local-tone balance look":
                "computational_hdr_local_tone_balance_look",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected})

    def test_sixty_candidate_atoms_and_twenty_three_families_resolve(self) -> None:
        proposed_candidates = self.proposal["proposed_candidates"]
        self.assertEqual(len(proposed_candidates), 60)
        self.assertEqual(len(self.proposal["candidate_families"]), 23)
        candidate_ids = set()
        for source in proposed_candidates:
            with self.subTest(candidate_id=source["id"]):
                candidate = self.entries_by_slot[source["slot"]][source["id"]]
                candidate_ids.add(source["id"])
                self.assertEqual(candidate["en"], source["en"])
                self.assertTrue(candidate["ko"])
        self.assertEqual(len(candidate_ids), 60)
        for family in self.proposal["candidate_families"]:
            with self.subTest(family=family["id"]):
                self.assertTrue(set(family["profile_ids"]) <= set(self.profiles))
                self.assertTrue(set(family["candidate_ids"]) <= candidate_ids)

    def test_sepia_is_a_treatment_candidate_without_an_age_claim(self) -> None:
        colors = self.entries_by_slot["color"]
        self.assertNotIn("sepia", colors)
        sepia = colors["sepia_treatment_without_age_claim"]
        self.assertEqual(
            sepia["en"], "sepia-toned color treatment without an age claim"
        )
        self.assertEqual(self.indexed_exact_matches("apply sepia tone"), set())

    def test_seventy_one_research_regressions_keep_hard_optional_boundary(self) -> None:
        self.assertEqual(len(self.routing_rows), 71)
        positive_count = 0
        for row in self.routing_rows:
            expected = row.get("expected_hard_profiles") or []
            if row["case_type"] == "narrow_positive":
                positive_count += 1
                self.assertEqual(len(expected), 1)
                profile_id = expected[0]
                profile = self.profiles[profile_id]
                with self.subTest(case=row["id"], profile_id=profile_id):
                    self.assertIsNotNone(
                        prompt_generator.candidate_pack_visual_component_match(
                            profile, row["prompt"]
                        )
                    )
                    bindings = {
                        field: profile["semantics"]["component_semantics"][
                            "groups"
                        ][index]["any_terms"][0]
                        for index, field in enumerate(
                            profile["required_evidence_fields"]
                        )
                    }
                    intent = prompt_generator.normalize_visual_intent(
                        {
                            "contract_version": "photo-visual-intent/v1",
                            "provenance": "agent_prepack",
                            "obligations": [
                                {
                                    "profile_id": profile_id,
                                    "source": "agent_postcore_interpretation",
                                    "scope": "request_only",
                                    "source_text": row["prompt"],
                                    "bindings": bindings,
                                }
                            ],
                        },
                        self.registry,
                        self.visual_index,
                    )
                    self.assertEqual(
                        intent["obligations"][0]["profile_id"], profile_id
                    )
                continue
            with self.subTest(case=row["id"]):
                self.assertEqual(self.indexed_exact_matches(row["prompt"]), set())
                profile_id = row.get("must_not_pass_profile")
                if profile_id:
                    self.assertIsNone(
                        prompt_generator.candidate_pack_visual_component_match(
                            self.profiles[profile_id], row["prompt"]
                        )
                    )
        self.assertEqual(positive_count, 18)

    def test_generated_indexes_include_profiles_and_all_candidate_atoms(self) -> None:
        self.assertTrue(self.profile_ids <= set(self.visual_index["entries"]))
        semantic_index = json.loads(SEMANTIC_INDEX_PATH.read_text(encoding="utf-8"))
        semantic_entry_ids = set(semantic_index["entry_order"])
        expected_entries = {
            f"slot:{row['slot']}:{row['id']}"
            for row in self.proposal["proposed_candidates"]
        }
        self.assertTrue(expected_entries <= semantic_entry_ids)
        self.assertNotIn("slot:color:sepia", semantic_entry_ids)

    def test_three_arm_fixture_is_reference_bound_and_partial_is_fail(self) -> None:
        if not CASES_PATH.exists():
            self.skipTest("three-arm fixture is written after independent render arms")
        rows = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({row["arm_id"] for row in rows}), 3)
        self.assertEqual(len({row["profile_id"] for row in rows}), 3)
        self.assertEqual(sum(row["image_call_count"] for row in rows), 3)
        self.assertEqual(sum(row["retry_count"] for row in rows), 0)
        self.assertEqual(sum(row["fallback_count"] for row in rows), 0)
        passed_gate_count = 0
        technically_qualified_count = 0
        for row in rows:
            with self.subTest(arm_id=row["arm_id"]):
                profile = self.profiles[row["profile_id"]]
                self.assertEqual(row["reference"]["role"], "appearance_reference")
                self.assertEqual(
                    row["reference"]["sha256"],
                    "3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea",
                )
                self.assertEqual(
                    set(row["required_gate_ids"]),
                    {gate["id"] for gate in profile["render_gates"]},
                )
                self.assertEqual(
                    set(row["gate_statuses"]), set(row["required_gate_ids"])
                )
                self.assertTrue(
                    set(row["gate_statuses"].values()) <= {"pass", "fail"}
                )
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")
                self.assertEqual(row["image_call_count"], 1)
                self.assertEqual(row["retry_count"], 0)
                self.assertEqual(row["fallback_count"], 0)
                self.assertIs(row["cross_arm_inputs_used"], False)
                self.assertEqual(row["user_judgment"], "not_yet_received")
                self.assertEqual(
                    row["candidate_exposure_status"], "candidate_exposure_failure"
                )
                for path_key, hash_key in (
                    ("request_envelope_path", "request_envelope_file_sha256"),
                    ("authorial_core_path", "authorial_core_file_sha256"),
                    ("candidate_pack_path", "candidate_pack_file_sha256"),
                    ("pixel_review_path", "pixel_review_file_sha256"),
                ):
                    artifact = ROOT / row[path_key]
                    self.assertTrue(artifact.is_file())
                    self.assertEqual(
                        hashlib.sha256(artifact.read_bytes()).hexdigest(),
                        row[hash_key],
                    )
                image = ROOT / row["image"]["path"]
                self.assertTrue(image.is_file())
                self.assertEqual(
                    hashlib.sha256(image.read_bytes()).hexdigest(),
                    row["image"]["sha256"],
                )
                pack = json.loads(
                    (ROOT / row["candidate_pack_path"]).read_text(encoding="utf-8")
                )[0]
                self.assertEqual(
                    [item["id"] for item in pack["visual_obligations"]["obligations"]],
                    [row["profile_id"]],
                )
                self.assertEqual(
                    set(pack["visual_obligations"]["required_hard_gates"]),
                    set(row["required_gate_ids"]),
                )
                passed_gate_count += sum(
                    status == "pass" for status in row["gate_statuses"].values()
                )
                technically_qualified_count += (
                    row["technical_status"]
                    == "visual_technical_qualified_user_judgment_pending"
                )
        self.assertEqual(passed_gate_count, 13)
        self.assertEqual(technically_qualified_count, 2)


if __name__ == "__main__":
    unittest.main()
