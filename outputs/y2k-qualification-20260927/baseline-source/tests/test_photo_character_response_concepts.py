from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
ASSETS_DIR = SKILL_DIR / "assets"
FIXTURE_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "character_response_concepts_v1.jsonl"
)
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
from tests.test_photo_authorial_core_v6 import core, envelope  # noqa: E402


class PhotoCharacterResponseConceptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = prompt_generator.load_json(
            ASSETS_DIR / "photo_prompt_tags.json"
        )
        cls.bm25f = prompt_generator.build_semantic_bm25f_payload(cls.data)
        cls.profile = next(
            row
            for row in prompt_generator.character_response_concept_profiles(
                cls.data
            )
            if row.get("id") == "tsundere"
        )
        cls.yandere_profile = next(
            row
            for row in prompt_generator.character_response_concept_profiles(
                cls.data
            )
            if row.get("id") == "yandere"
        )
        cls.kuudere_profile = next(
            row
            for row in prompt_generator.character_response_concept_profiles(
                cls.data
            )
            if row.get("id") == "kuudere"
        )

    def normalize_core(self) -> dict:
        request_envelope = prompt_generator.normalize_request_envelope(envelope())
        return prompt_generator.normalize_authorial_core(
            core(),
            request_envelope=request_envelope,
        )

    def test_multilingual_fixture_uses_contrastive_bm25f(self):
        for raw_line in FIXTURE_PATH.read_text(encoding="utf-8").splitlines():
            case = json.loads(raw_line)
            with self.subTest(case=case["id"]):
                rows = prompt_generator.rank_character_response_concept_candidates(
                    self.data,
                    self.bm25f,
                    {"active_request": case["text"]},
                    limit=3,
                )
                actual = (
                    str(rows[0]["document_id"]).split(":", 1)[1]
                    if rows
                    else None
                )
                self.assertEqual(actual, case["expected_profile_id"])

    def test_profile_defines_abstract_meaning_without_scene_geometry(self):
        self.assertEqual(self.profile["domain"], "character_response")
        self.assertEqual(
            {row["operator"] for row in self.profile["required_relations"]},
            {"contrasts", "same_target", "temporal_order"},
        )
        self.assertEqual(
            set(self.profile["axis_requirements"]),
            {
                "surface_affect",
                "underlying_affiliation",
                "affect_leak_timing",
                "affect_leak_intentionality",
            },
        )
        serialized = json.dumps(self.profile, ensure_ascii=False)
        for scene_field in (
            "camera",
            "composition",
            "facial_geometry",
            "gaze_direction",
            "pose",
            "prop",
            "relationship_register",
        ):
            self.assertNotIn(f'"{scene_field}"', serialized)
        self.assertEqual(
            self.profile["applicability"],
            {
                "retrieval_only": True,
                "hard_eligible": False,
                "requester_definition_precedence": True,
            },
        )

    def test_confounders_share_the_existing_semantic_index(self):
        concept_ids = (
            prompt_generator.semantic_character_response_concept_document_ids(
                self.data
            )
        )
        confounder_ids = (
            prompt_generator.semantic_character_response_confounder_document_ids(
                self.data,
                profile_id="tsundere",
            )
        )
        self.assertEqual(
            concept_ids,
            {
                "character_response_concept:tsundere",
                "character_response_concept:yandere",
                "character_response_concept:kuudere",
            },
        )
        self.assertEqual(len(confounder_ids), 7)
        self.assertTrue(
            all(document_id in self.bm25f["documents"] for document_id in confounder_ids)
        )
        yandere_confounder_ids = (
            prompt_generator.semantic_character_response_confounder_document_ids(
                self.data,
                profile_id="yandere",
            )
        )
        self.assertEqual(len(yandere_confounder_ids), 7)
        self.assertTrue(
            all(
                document_id in self.bm25f["documents"]
                for document_id in yandere_confounder_ids
            )
        )
        kuudere_confounder_ids = (
            prompt_generator.semantic_character_response_confounder_document_ids(
                self.data,
                profile_id="kuudere",
            )
        )
        self.assertEqual(len(kuudere_confounder_ids), 7)
        self.assertTrue(
            all(
                document_id in self.bm25f["documents"]
                for document_id in kuudere_confounder_ids
            )
        )

    def test_actual_generated_index_contains_profile_and_confounders(self):
        index = prompt_generator.load_semantic_index_payload(
            ASSETS_DIR / "photo_prompt_semantic_index.json"
        )
        prompt_generator.validate_semantic_index_metadata(index, self.data)
        self.assertIn("character_response_concept:tsundere", index["entries"])
        self.assertIn("character_response_concept:yandere", index["entries"])
        self.assertIn("character_response_concept:kuudere", index["entries"])
        self.assertIn(
            "character_response_confounder:tsundere:pure_hostility",
            index["entries"],
        )
        self.assertIn(
            "character_response_confounder:yandere:role_only_care",
            index["entries"],
        )
        self.assertIn(
            "character_response_confounder:kuudere:generic_stoicism",
            index["entries"],
        )

    def test_yandere_profile_is_behavior_led_and_contrastive(self):
        profile = self.yandere_profile
        self.assertEqual(profile["domain"], "character_response")
        self.assertEqual(
            profile["axis_requirements"]["underlying_affiliation"][
                "semantic_classes"
            ],
            ["obsessive"],
        )
        self.assertEqual(
            {row["operator"] for row in profile["required_relations"]},
            {"contrasts", "same_target", "temporal_order"},
        )
        same_target = next(
            row
            for row in profile["required_relations"]
            if row["operator"] == "same_target"
        )
        self.assertEqual(
            same_target["members"],
            [
                "relationship_target",
                "surface_affect",
                "primary_action",
                "immediate_consequence",
            ],
        )
        self.assertIn("role_only_care", {row["id"] for row in profile["confounders"]})
        self.assertIn(
            "horror_threat_aesthetic",
            {row["id"] for row in profile["confounders"]},
        )
        serialized = json.dumps(profile, ensure_ascii=False)
        for scene_field in (
            "camera",
            "composition",
            "facial_geometry",
            "gaze_direction",
            "pose",
            "prop",
            "relationship_register",
        ):
            self.assertNotIn(f'"{scene_field}"', serialized)

        normalized = self.normalize_core()
        assertion = normalized["semantic_assertions"][0]
        assertion["axes"].update(
            {
                "surface_affect": "openly affectionate",
                "underlying_affiliation": "possessive",
                "affect_leak_intentionality": "deliberate",
            }
        )
        assertion["relations"] = copy.deepcopy(profile["required_relations"])
        result = prompt_generator.evaluate_character_response_profile(
            normalized,
            self.data,
            profile,
        )
        self.assertEqual(result["status"], "consistent")

        reordered = copy.deepcopy(normalized)
        same_target_assertion = next(
            row
            for row in reordered["semantic_assertions"][0]["relations"]
            if row["operator"] == "same_target"
        )
        same_target_assertion["members"].reverse()
        result = prompt_generator.evaluate_character_response_profile(
            reordered,
            self.data,
            profile,
        )
        self.assertEqual(result["status"], "consistent")

        missing_consequence = copy.deepcopy(normalized)
        missing_same_target = next(
            row
            for row in missing_consequence["semantic_assertions"][0]["relations"]
            if row["operator"] == "same_target"
        )
        missing_same_target["members"].remove("immediate_consequence")
        result = prompt_generator.evaluate_character_response_profile(
            missing_consequence,
            self.data,
            profile,
        )
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["missing_relation_operators"], ["same_target"])

        assertion["axes"]["underlying_affiliation"] = "negative"
        result = prompt_generator.evaluate_character_response_profile(
            normalized,
            self.data,
            profile,
        )
        self.assertEqual(result["status"], "conflicting")

    def test_yandere_atomic_support_excludes_horror_and_invisible_shortcuts(self):
        slot_entries = {
            str(row.get("id") or ""): row
            for slot in ("expression", "mood", "reflection_logic")
            for row in self.data.get("slots", {}).get(slot, [])
            if isinstance(row, dict)
        }
        for entry_id in (
            "half_lidded_menacing_distant_gaze",
            "reflection_extra_presence",
            "obsessive_devotion",
        ):
            self.assertNotIn("yandere", slot_entries[entry_id].get("tags", []))

        for slot, entry_id in (
            ("expression", "obsessive_tender_smile"),
            ("distance_narrative", "half_step_too_close"),
            ("relational_action", "pulling_handoff_back"),
        ):
            entry = next(
                row
                for row in self.data.get("slots", {}).get(slot, [])
                if row.get("id") == entry_id
            )
            self.assertIn("yandere", entry.get("tags", []))

    def test_kuudere_profile_keeps_composure_and_same_target_care_together(self):
        profile = self.kuudere_profile
        self.assertEqual(
            profile["axis_requirements"]["surface_affect"]["semantic_classes"],
            ["composed_reserve"],
        )
        self.assertEqual(
            profile["axis_requirements"]["affect_leak_timing"][
                "semantic_classes"
            ],
            ["within_stable_surface"],
        )
        self.assertEqual(
            {row["operator"] for row in profile["required_relations"]},
            {"contrasts", "same_target", "temporal_order"},
        )
        same_target = next(
            row
            for row in profile["required_relations"]
            if row["operator"] == "same_target"
        )
        self.assertEqual(
            same_target["members"],
            [
                "relationship_target",
                "primary_action",
                "affect_leak",
                "immediate_consequence",
            ],
        )
        confounder_ids = {row["id"] for row in profile["confounders"]}
        self.assertTrue(
            {
                "generic_stoicism",
                "dandere_shy_withdrawal",
                "tsundere_hostile_denial",
                "role_only_service",
                "yandere_possessive_control",
            }
            <= confounder_ids
        )
        serialized = json.dumps(profile, ensure_ascii=False)
        for scene_field in (
            "camera",
            "composition",
            "facial_geometry",
            "gaze_direction",
            "pose",
            "prop",
            "relationship_register",
        ):
            self.assertNotIn(f'"{scene_field}"', serialized)

        normalized = self.normalize_core()
        assertion = normalized["semantic_assertions"][0]
        assertion["axes"].update(
            {
                "surface_affect": "composed reserve",
                "underlying_affiliation": "positive",
                "affect_leak_timing": "within the stable composed surface",
                "affect_leak_intentionality": "understated",
            }
        )
        assertion["relations"] = copy.deepcopy(profile["required_relations"])
        result = prompt_generator.evaluate_character_response_profile(
            normalized,
            self.data,
            profile,
        )
        self.assertEqual(result["status"], "consistent")

        conflict = copy.deepcopy(normalized)
        conflict["semantic_assertions"][0]["axes"][
            "surface_affect"
        ] = "shy avoidance"
        result = prompt_generator.evaluate_character_response_profile(
            conflict,
            self.data,
            profile,
        )
        self.assertEqual(result["status"], "conflicting")

    def test_post_core_retrieval_is_advisory_and_score_free(self):
        normalized = self.normalize_core()
        semantic_index = prompt_generator.load_semantic_index_payload(
            ASSETS_DIR / "photo_prompt_semantic_index.json"
        )
        contract = prompt_generator.compile_character_response_contract(
            normalized,
            data=self.data,
            semantic_index=semantic_index,
        )
        self.assertIsNotNone(contract)
        assert contract is not None
        retrieval = contract["advisory_retrieval"]
        self.assertTrue(retrieval["evaluated"])
        candidates = retrieval["candidates"]
        self.assertIn(
            "character_response_concept:tsundere",
            {row["candidate_id"] for row in candidates},
        )
        linked_runtime_ids = {
            f"character_mechanism_node:{runtime_id}"
            for runtime_id in self.profile["optional_runtime_node_ids"]
        }
        behavior_ids = {
            row["candidate_id"]
            for row in candidates
            if row["candidate_type"] == "behavior_support"
        }
        self.assertTrue(behavior_ids <= linked_runtime_ids)
        self.assertTrue(all(row["hard_eligible"] is False for row in candidates))
        serialized = json.dumps(retrieval, ensure_ascii=False)
        for private_field in (
            '"score"',
            '"rank"',
            '"matched_terms"',
            '"document_frequency"',
            '"vector"',
        ):
            self.assertNotIn(private_field, serialized)
        concept = next(
            row
            for row in candidates
            if row["candidate_id"] == "character_response_concept:tsundere"
        )
        self.assertEqual(
            concept["semantic_consistency"]["status"],
            "consistent",
        )
        self.assertFalse(concept["semantic_consistency"]["hard_eligible"])

    def test_profile_consistency_is_data_driven_and_requester_first(self):
        normalized = self.normalize_core()
        conflict = copy.deepcopy(normalized)
        conflict["semantic_assertions"][0]["axes"]["surface_affect"] = "hostile"
        conflict["semantic_assertions"][0]["axes"][
            "underlying_affiliation"
        ] = "negative"
        result = prompt_generator.evaluate_character_response_profile(
            conflict,
            self.data,
            self.profile,
        )
        self.assertEqual(result["status"], "conflicting")
        self.assertEqual(
            set(result["conflicting_axes"]),
            {"surface_affect", "underlying_affiliation"},
        )

        overridden = copy.deepcopy(normalized)
        overridden["user_definitions"] = [
            {
                "term": "츤데레",
                "source_text": "내 정의에서 츤데레는 처음부터 솔직한 친절이다",
                "interpreted_meaning": "open kindness from the beginning",
                "prompt_evidence": "wraps the coworker's scraped wrist with practical care",
            }
        ]
        result = prompt_generator.evaluate_character_response_profile(
            overridden,
            self.data,
            self.profile,
        )
        self.assertEqual(
            result["status"],
            "superseded_by_requester_definition",
        )

    def test_conflicting_or_requester_superseded_profiles_cannot_link_behavior(self):
        semantic_index = prompt_generator.load_semantic_index_payload(
            ASSETS_DIR / "photo_prompt_semantic_index.json"
        )
        cases = []

        conflicting = self.normalize_core()
        conflicting["semantic_assertions"][0]["axes"][
            "surface_affect"
        ] = "hostile"
        conflicting["semantic_assertions"][0]["axes"][
            "underlying_affiliation"
        ] = "negative"
        cases.append(("conflicting", conflicting))

        overridden = self.normalize_core()
        overridden["user_definitions"] = [
            {
                "term": "츤데레",
                "source_text": "내 정의에서 츤데레는 처음부터 솔직한 친절이다",
                "interpreted_meaning": "open kindness from the beginning",
                "prompt_evidence": "wraps the coworker's scraped wrist with practical care",
            }
        ]
        cases.append(("superseded_by_requester_definition", overridden))

        for expected_status, normalized in cases:
            with self.subTest(status=expected_status):
                retrieval = (
                    prompt_generator.retrieve_character_response_behavior_candidates(
                        self.data,
                        normalized,
                        semantic_index=semantic_index,
                    )
                )
                profile = next(
                    row
                    for row in retrieval["candidates"]
                    if row["candidate_id"]
                    == "character_response_concept:tsundere"
                )
                self.assertEqual(
                    profile["semantic_consistency"]["status"],
                    expected_status,
                )
                self.assertEqual(profile["applicability"], "diagnostic_only")
                self.assertEqual(retrieval["concept_profile_support_matches"], 0)
                self.assertFalse(
                    any(
                        row["candidate_type"] == "behavior_support"
                        for row in retrieval["candidates"]
                    )
                )

    def test_new_profile_uses_the_same_schema_without_code_changes(self):
        extended = copy.deepcopy(self.data)
        clone = copy.deepcopy(self.profile)
        clone.update(
            {
                "id": "guarded_affiliation_example",
                "aliases": [
                    "guarded affiliation example",
                    "억제된 호감 예시",
                    "抑えた好意の例",
                ],
                "en": "a generic guarded-affiliation contrast example",
                "ko": "일반적인 억제된 호감 대비 예시",
                "ja": "一般的な抑えた好意の対比例",
            }
        )
        extended["character_mechanism_graph"]["concept_profiles"].append(clone)
        prompt_generator.validate_character_mechanism_graph(extended)
        ids = prompt_generator.semantic_character_response_concept_document_ids(
            extended
        )
        self.assertIn(
            "character_response_concept:guarded_affiliation_example",
            ids,
        )


if __name__ == "__main__":
    unittest.main()
