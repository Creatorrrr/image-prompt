from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
ASSETS_DIR = SKILL_DIR / "assets"
TAGS_PATH = ASSETS_DIR / "photo_prompt_tags.json"
EXTENSION_PATH = ASSETS_DIR / "photo_prompt_poverty_extension.json"
REGISTRY_PATH = ASSETS_DIR / "photo_prompt_visual_obligations.json"
VISUAL_INDEX_PATH = ASSETS_DIR / "photo_prompt_visual_profile_index.json"
SEMANTIC_INDEX_PATH = ASSETS_DIR / "photo_prompt_semantic_index.json"
ROUTING_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "poverty_visual_obligation_routing_v1.jsonl"
)
PIXEL_CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "poverty_visual_semantics_three_arm_pixel_cases_v1.jsonl"
)
MAINTENANCE_DIR = (
    ROOT / "docs" / "research-evidence" / "photo-prompt" / "extension-maintenance"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import photo_candidate_semantics  # noqa: E402
import prompt_generator  # noqa: E402
from bm25f_retrieval import rank_bm25f  # noqa: E402


PROFILE_IDS = {
    "food_access_budget_choice_event",
    "household_food_depletion_portioning_event",
    "basic_needs_budget_tradeoff_deferral",
    "household_energy_affordability_coping_relation",
    "occupied_housing_habitability_mitigation_relation",
    "working_income_essential_cost_gap_relation",
    "transport_affordability_access_barrier_event",
    "material_replacement_deferral_repair_cycle",
    "relative_participation_affordability_barrier",
}

BROAD_TERMS = (
    "가난",
    "빈곤",
    "궁핍",
    "기아",
    "생활고",
    "working poor",
    "food insecurity",
    "energy poverty",
    "transport poverty",
    "relative deprivation",
)


class PhotoPovertyVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
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
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.merged_candidates = {
            str(row["id"]): (slot, row)
            for slot, rows in cls.tags["slots"].items()
            for row in rows
        }
        cls.routing_cases = [
            json.loads(line)
            for line in ROUTING_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        cls.pixel_cases = [
            json.loads(line)
            for line in PIXEL_CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    @staticmethod
    def source_rows(text: str) -> list[dict[str, object]]:
        return [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            }
        ]

    def exact_hard_matches(self, text: str) -> set[str]:
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.routing_registry,
            self.source_rows(text),
            visual_profile_index=self.routing_index,
            adult_context=True,
        )
        return {
            str(hit["profile_id"])
            for hit in resolution["hits"]
            if hit.get("match_basis") == "exact"
            and hit.get("hard_eligible") is True
        }

    def test_nine_profiles_compile_to_complete_five_gate_contracts(self) -> None:
        self.assertLessEqual(PROFILE_IDS, set(self.profiles))
        all_gate_ids = [
            str(gate["id"])
            for profile in self.registry["profiles"]
            for gate in profile["render_gates"]
        ]
        self.assertEqual(len(all_gate_ids), len(set(all_gate_ids)))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], True)
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertEqual(len(profile["activation"]["exact_terms"]), 4)
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
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
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 6)
                self.assertEqual(
                    profile["runtime_expression"]["default_mode"],
                    "definition_only",
                )
                self.assertEqual(
                    profile["runtime_expression"]["forbidden_prompt_terms"],
                    profile["runtime_expression"]["runtime_forbidden_labels"],
                )

    def test_research_routing_cases_preserve_exact_broad_and_negative_boundaries(self) -> None:
        self.assertEqual(len(self.routing_cases), 34)
        self.assertEqual(len({row["id"] for row in self.routing_cases}), 34)
        for row in self.routing_cases:
            with self.subTest(case_id=row["id"]):
                self.assertEqual(
                    self.exact_hard_matches(str(row["text"])),
                    set(row["expected_profile_ids"]),
                )

    def test_broad_terms_never_hard_activate_a_profile(self) -> None:
        for term in BROAD_TERMS:
            with self.subTest(term=term):
                self.assertEqual(self.exact_hard_matches(term), set())

    def test_exact_profile_plus_declared_substitute_fails_closed(self) -> None:
        cases = (
            "an adult returns one basic food item because a visibly finite grocery budget cannot cover the selected essentials, then completes the reduced purchase as ordinary price comparison",
            "in an occupied home, unaffordable or unavailable heating leaves the intact heat source inactive while adults consolidate activity and seal drafts as a cozy winter interior",
            "an adult's concrete essential trip is blocked at a transit boundary by a visible fare-resource gap while the usable vehicle departs after a forgotten wallet",
            "an adult repairs localized functional wear on an essential daily item because replacement is unavailable, then returns it to continued use as a slow fashion hobby",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.exact_hard_matches(text), set())

    def test_extension_merges_fifty_four_scoped_candidates_and_nine_bundles(self) -> None:
        self.assertIn(EXTENSION_PATH.name, prompt_generator.RESEARCH_EXTENSION_FILENAMES)
        self.assertEqual(len(self.extension["visual_semantics"]), 9)
        self.assertEqual(
            {row["id"] for row in self.extension["visual_semantics"]},
            PROFILE_IDS,
        )
        extension_rows = {
            str(row["id"]): (slot, row)
            for slot, rows in self.extension["slots"].items()
            for row in rows
        }
        self.assertEqual(len(extension_rows), 54)
        self.assertEqual(
            {slot: len(rows) for slot, rows in self.extension["slots"].items()},
            {
                "subject": 9,
                "action": 9,
                "location": 9,
                "prop": 9,
                "composition": 9,
                "aftermath_trace": 9,
            },
        )
        self.assertLessEqual(set(extension_rows), set(self.merged_candidates))
        for cluster in self.extension["visual_semantics"]:
            with self.subTest(cluster_id=cluster["id"]):
                self.assertEqual(cluster["hard_profile_ids"], [cluster["id"]])
                self.assertEqual(len(cluster["component_groups"]), 5)
                self.assertEqual(len(cluster["candidate_ids"]), 6)
                self.assertGreaterEqual(len(cluster["confusion_boundaries"]), 6)
                self.assertLessEqual(
                    set(cluster["candidate_ids"]), set(extension_rows)
                )
        for candidate_id, (slot, row) in extension_rows.items():
            with self.subTest(candidate_id=candidate_id):
                profile_tags = [tag for tag in row["tags"] if tag in PROFILE_IDS]
                self.assertEqual(len(profile_tags), 1)
                self.assertIn("poverty_access_visual_semantics", row["tags"])
                self.assertIn(slot, row["tags"])
                self.assertEqual(row["requires_primary_any_tags"], profile_tags)
                self.assertGreaterEqual(len(row["embedding_text"].split()), 12)
                self.assertEqual(len(row["concept_units"]), 1)
                if slot == "subject":
                    self.assertIn("adult", row["tags"])
                    self.assertEqual(row["kind"], ["human"])

    def test_external_sources_and_claim_limits_do_not_leak_into_candidates(self) -> None:
        for rows in self.extension["slots"].values():
            for row in rows:
                serialized = json.dumps(row, ensure_ascii=False).casefold()
                self.assertNotIn("http://", serialized)
                self.assertNotIn("https://", serialized)
                self.assertNotIn("world bank", serialized)
                self.assertNotIn("source_ids", serialized)
                self.assertNotIn("research_limitations", serialized)
                self.assertNotRegex(
                    " ".join(
                        [
                            str(row.get("en") or ""),
                            *[str(value) for value in row.get("aliases") or []],
                            str(row.get("embedding_text") or ""),
                        ]
                    ).casefold(),
                    r"\b(poor person|poverty face|poverty-stricken person|starving body|slum dweller)\b",
                )

    def test_maintenance_record_is_external_hash_bound_and_source_bound(self) -> None:
        reference = self.extension["maintenance_ref"]
        record_path = MAINTENANCE_DIR / (reference["record_id"] + ".json")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        self.assertEqual(reference["sha256"], photo_candidate_semantics.digest(record))
        source_without_reference = copy.deepcopy(self.extension)
        source_without_reference.pop("maintenance_ref")
        self.assertEqual(
            record["authored_source_sha256"],
            photo_candidate_semantics.digest(source_without_reference),
        )
        self.assertEqual(record["runtime_keys"], ["slots", "visual_semantics"])
        self.assertTrue(record["maintenance_only"])

    def test_compiled_bundles_keep_profile_activation_advisory(self) -> None:
        bundle_ids = {row["id"] for row in self.extension["visual_semantics"]}
        compiled = [
            row for row in self.tags["candidate_bundles"] if row["id"] in bundle_ids
        ]
        self.assertEqual(len(compiled), 9)
        for row in compiled:
            with self.subTest(bundle_id=row["id"]):
                self.assertEqual(row["adoption"], "optional")
                self.assertEqual(
                    row["profile_activation"],
                    "independent_request_evidence_only",
                )
                self.assertEqual(row["associated_profile_ids"], [row["id"]])
                self.assertEqual(len(row["member_candidates"]), 6)

    def test_generated_visual_index_contains_profiles_and_exact_terms(self) -> None:
        generated = prompt_generator.load_visual_profile_index(
            VISUAL_INDEX_PATH,
            self.registry,
        )
        self.assertLessEqual(PROFILE_IDS, set(generated["entries"]))
        exact_pairs = {
            (str(row["term"]), str(row["profile_id"]))
            for row in generated["exact_lookup"]
        }
        for profile_id in PROFILE_IDS:
            for term in self.profiles[profile_id]["activation"]["exact_terms"]:
                with self.subTest(profile_id=profile_id, term=term):
                    self.assertIn((term, profile_id), exact_pairs)

    def test_generated_semantic_index_contains_every_candidate(self) -> None:
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        prompt_generator.validate_semantic_index_metadata(semantic_index, self.tags)
        expected_entries = {
            f"slot:{slot}:{row['id']}"
            for slot, rows in self.extension["slots"].items()
            for row in rows
        }
        self.assertEqual(len(expected_entries), 54)
        self.assertLessEqual(expected_entries, set(semantic_index["entries"]))

    def test_bm25f_surfaces_each_new_candidate_from_its_authored_text(self) -> None:
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        prompt_generator.validate_semantic_index_metadata(semantic_index, self.tags)
        bm25f = prompt_generator.semantic_bm25f_payload_from_index(semantic_index)
        for slot, rows in self.extension["slots"].items():
            for row in rows:
                with self.subTest(candidate_id=row["id"]):
                    query = " ".join(
                        [row["en"], *row["aliases"], *row["keywords"]]
                    )
                    ranked = rank_bm25f(
                        bm25f,
                        {"active_request": query},
                        limit=16,
                    )
                    self.assertIn(
                        f"slot:{slot}:{row['id']}",
                        {str(hit["document_id"]) for hit in ranked},
                    )

    def test_p1_digital_and_specialist_bundles_remain_outside_runtime(self) -> None:
        self.assertNotIn(
            "digital_connectivity_affordability_workaround_event",
            self.profiles,
        )
        serialized = json.dumps(self.extension, ensure_ascii=False)
        self.assertNotIn("pov_digital_", serialized)
        for deferred in (
            "time_poverty_sequence_only",
            "period_material_facility_access_gap",
            "water_sanitation_access_gap",
            "healthcare_cost_deferral_explicit_only",
            "temporary_housing_insecurity_sequence",
            "community_food_access_distribution",
            "historical_relief_institution_context",
        ):
            self.assertNotIn(deferred, serialized)

    def test_three_arm_pixel_cases_are_hash_bound_independent_and_fail_closed(self) -> None:
        self.assertEqual(len(self.pixel_cases), 3)
        self.assertEqual(len({row["arm_id"] for row in self.pixel_cases}), 3)
        self.assertEqual(len({row["concept_seed"] for row in self.pixel_cases}), 3)
        self.assertEqual(
            {row["profile_id"] for row in self.pixel_cases},
            {
                "household_energy_affordability_coping_relation",
                "working_income_essential_cost_gap_relation",
                "transport_affordability_access_barrier_event",
            },
        )
        reference_hash = (
            "3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea"
        )
        for row in self.pixel_cases:
            with self.subTest(arm_id=row["arm_id"]):
                result_path = ROOT / row["result_path"]
                self.assertTrue(result_path.is_file())
                self.assertEqual(
                    hashlib.sha256(result_path.read_bytes()).hexdigest(),
                    row["result_sha256"],
                )
                self.assertEqual(row["reference_sha256"], reference_hash)
                self.assertEqual(
                    row["selected_candidate_id"],
                    f"visual-concept:{row['profile_id']}",
                )
                self.assertEqual(
                    set(row["required_gate_ids"]),
                    {
                        gate["id"]
                        for gate in self.profiles[row["profile_id"]]["render_gates"]
                    },
                )
                policy = row["generation_policy"]
                self.assertIs(policy["single_generation_call"], True)
                self.assertEqual(policy["retry_count"], 0)
                self.assertEqual(policy["fallback_count"], 0)
                self.assertIs(policy["cross_arm_inputs_allowed"], False)
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")
                self.assertEqual(row["verdict_rule"]["blocked_output"], "UNSCORED")
                self.assertEqual(row["verdict_rule"]["user_judgment"], "PENDING")
                for verdict_name in ("agent_verdict", "coordinator_verdict"):
                    verdict = row[verdict_name]
                    self.assertEqual(verdict["required"], 5)
                    self.assertEqual(
                        verdict["status"],
                        "PASS" if verdict["passed"] == 5 else "FAIL",
                    )
                    self.assertEqual(
                        len(verdict["failed_gate_ids"]),
                        verdict["required"] - verdict["passed"],
                    )


if __name__ == "__main__":
    unittest.main()
