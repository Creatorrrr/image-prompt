from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "photo-prompt-image-generator" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import bm25f_retrieval  # noqa: E402
import prompt_generator  # noqa: E402


class PhotoSlotQueryFusionTests(unittest.TestCase):
    def core(self):
        return {
            "contract_version": "photo-authorial-core/v3",
            "canonical_sha256": "f" * 64,
            "request_binding": {"active_spans": []},
            "subject": "an adult human cat-eared witch in a red scarf",
            "setting": "dark moonlit clouds above the city",
            "event": "the witch fires a luminous return shot toward a chasing KF-21 fighter",
            "visual_priorities": ["urgent candid night photograph"],
            "style": {"domain": "photojournalism", "family": "hurried night capture"},
            "user_exclusions": ["red scarf"],
        }

    def test_focus_queries_use_relevant_frozen_fields_and_redact_exclusions(self):
        core = self.core()
        subject, subject_fields = prompt_generator.candidate_pack_slot_focus_text(core, "subject")
        action, action_fields = prompt_generator.candidate_pack_slot_focus_text(core, "action")
        location, location_fields = prompt_generator.candidate_pack_slot_focus_text(core, "location")
        self.assertEqual(subject_fields, ["subject"])
        self.assertIn("cat-eared witch", subject)
        self.assertNotIn("red scarf", subject)
        self.assertEqual(action_fields, ["event"])
        self.assertIn("return shot", action)
        self.assertNotIn("moonlit clouds", action)
        self.assertEqual(location_fields, ["setting"])
        self.assertIn("moonlit clouds", location)
        self.assertNotIn("return shot", location)
        self.assertEqual(
            prompt_generator.candidate_pack_slot_focus_text(core, "unmapped_slot"),
            ("", []),
        )

    def test_without_guard_context_lookup_stays_in_supplied_pool(self):
        core = self.core()
        entries = [
            {"id": "generic", "en": "generic witch action"},
            {"id": "moon", "en": "moonlit flight"},
            {"id": "broom", "en": "broom travel"},
            {"id": "cloud", "en": "cloud transit"},
            {"id": "counterfire", "en": "luminous return shot toward a fighter"},
            {"id": "uneligible", "en": "luminous return shot toward a fighter"},
        ]
        documents = {
            f"slot:action:{entry['id']}": {
                "aliases": [entry["en"]],
                "definition": [entry["en"]],
            }
            for entry in entries
        }
        index = bm25f_retrieval.build_bm25f_index(
            documents,
            policy={
                "fields": {
                    "aliases": {"weight": 4.0, "b": 0.2},
                    "definition": {"weight": 2.0, "b": 0.7},
                },
                "query_fields": {},
            },
        )
        rows = [{"id": entry["id"], "weight": 1.0} for entry in entries[:-1]]
        global_query, _ = prompt_generator.authorial_core_retrieval_text(core)
        ranked, metadata = prompt_generator.candidate_pack_rank_slot_rows(
            {"slots": {"action": entries}},
            "action",
            rows,
            "generic",
            {"action": {"id": "generic"}},
            core,
            index,
            global_query,
        )
        self.assertEqual([row["id"] for row in ranked[:2]], ["generic", "counterfire"])
        self.assertNotIn("uneligible", [row["id"] for row in ranked])
        self.assertEqual(metadata["source_authorial_core_sha256"], core["canonical_sha256"])
        self.assertEqual(metadata["slot_query_source_fields"], ["event"])
        self.assertTrue(metadata["advisory_only"])

    def test_guarded_expansion_recovers_focused_action_without_user_exclusion(self):
        core = self.core()
        entries = [
            {"id": "generic", "en": "ordinary standing action", "weight": 1.0},
            {"id": "counterfire", "en": "firing a luminous return shot toward a chasing fighter", "weight": 1.0},
            {"id": "excluded", "en": "red scarf return shot toward a fighter", "weight": 1.0},
        ]
        documents = {
            f"slot:action:{entry['id']}": {
                "aliases": [entry["en"]],
                "definition": [entry["en"]],
            }
            for entry in entries
        }
        index = bm25f_retrieval.build_bm25f_index(
            documents,
            policy={"fields": {"aliases": {"weight": 4.0, "b": 0.2}}},
        )
        global_query, _ = prompt_generator.authorial_core_retrieval_text(core)
        contract = {
            "adult_allowed": True,
            "subject_category": "human",
            "intent_constraints": {"subject_categories": ["human"]},
            "soft_anchor_policy": {},
        }
        ranked, metadata = prompt_generator.candidate_pack_rank_slot_rows(
            {"slots": {"action": entries}},
            "action",
            [{"id": "generic", "weight": 1.0}],
            "generic",
            {"action": {"id": "generic"}},
            core,
            index,
            global_query,
            contract,
            {"id": "generic"},
        )
        self.assertEqual([row["id"] for row in ranked], ["generic", "counterfire"])
        self.assertEqual(metadata["hard_guarded_expansion_count"], 1)

    def test_cat_eared_human_core_does_not_route_to_animal_subject(self):
        data = {
            "slots": {"subject": [{"id": "stray_cat"}]},
            prompt_generator.QUALITY_LAYERS_DATA_KEY: {
                "intent_routing": {
                    "subject_routes": [
                        {"entry_id": "stray_cat", "category": "animal", "aliases": ["cat"]}
                    ],
                    "subject_categories": [
                        {"category": "human", "aliases": ["human", "witch"]},
                        {"category": "animal", "aliases": ["cat"]},
                    ],
                }
            },
        }
        constraints = prompt_generator.resolve_request_intent_constraints(
            data,
            None,
            {},
            authorial_core=self.core(),
        )
        self.assertEqual(constraints["subject_categories"], ["human"])
        self.assertEqual(constraints.get("subject_entry_ids", []), [])

        implicit_human = {**self.core(), "subject": "an adult cat-eared witch"}
        implicit_constraints = prompt_generator.resolve_request_intent_constraints(
            data, None, {}, authorial_core=implicit_human,
        )
        self.assertEqual(implicit_constraints["subject_categories"], ["human"])

        actual_cat = {
            **self.core(),
            "subject": "a stray cat",
            "event": "the stray cat crosses a quiet street",
            "visual_priorities": [],
            "style": {},
        }
        cat_constraints = prompt_generator.resolve_request_intent_constraints(
            data,
            None,
            {},
            authorial_core=actual_cat,
        )
        self.assertEqual(cat_constraints["subject_categories"], ["animal"])
        self.assertEqual(cat_constraints["subject_entry_ids"], ["stray_cat"])

        cat_near_witch = {
            **actual_cat,
            "event": "the stray cat crosses the path of a witch",
        }
        adjacent_constraints = prompt_generator.resolve_request_intent_constraints(
            data, None, {}, authorial_core=cat_near_witch,
        )
        self.assertEqual(adjacent_constraints["subject_categories"], ["animal"])

    def test_subject_expansion_keeps_typed_human_category(self):
        core = self.core()
        entries = [
            {"id": "generic", "en": "a human witness", "tags": ["human"]},
            {"id": "witch", "en": "an adult human witch with feline ears", "tags": ["human", "witch", "adult", "role"]},
            {"id": "cat", "en": "a stray cat", "tags": ["animal"]},
            {"id": "adult_styling", "en": "an adult human witch in suggestive styling", "tags": ["human", "witch", "adult", "suggestive"]},
        ]
        index = bm25f_retrieval.build_bm25f_index(
            {
                f"slot:subject:{entry['id']}": {"aliases": [entry["en"]]}
                for entry in entries
            },
            policy={"fields": {"aliases": {"weight": 4.0, "b": 0.2}}},
        )
        global_query, _ = prompt_generator.authorial_core_retrieval_text(core)
        ranked, metadata = prompt_generator.candidate_pack_rank_slot_rows(
            {"slots": {"subject": entries}},
            "subject",
            [{"id": "generic", "weight": 1.0}],
            "generic",
            {"subject": {"id": "generic"}},
            core,
            index,
            global_query,
            {
                "adult_allowed": False,
                "subject_category": "human",
                "intent_constraints": {"subject_categories": ["human"]},
                "soft_anchor_policy": {},
            },
            {"id": "generic"},
        )
        self.assertIn("witch", [row["id"] for row in ranked])
        self.assertNotIn("cat", [row["id"] for row in ranked])
        self.assertNotIn("adult_styling", [row["id"] for row in ranked])
        self.assertEqual(metadata["hard_guarded_expansion_count"], 1)

    def test_missing_index_preserves_existing_order(self):
        rows = [{"id": "first"}, {"id": "second"}]
        ranked, metadata = prompt_generator.candidate_pack_rank_slot_rows(
            {}, "action", rows, "first", {}, self.core(), None, "scene"
        )
        self.assertEqual(ranked, rows)
        self.assertIsNone(metadata)


if __name__ == "__main__":
    unittest.main()
