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



    def test_guarded_action_lookup_recovers_focus_without_inherited_choices(self):
        data = {"candidate_semantic_policy": {"slot_dimensions": {"action": ["action"]}},
                "slots": {"action": [
                    {"id": "generic", "en": "ordinary standing action"},
                    {"id": "counterfire", "en": "firing a luminous return shot toward a chasing fighter"},
                    {"id": "excluded", "en": "red scarf return shot toward a fighter"},
                    {"id": "blocked", "en": "firing a luminous return shot toward a chasing fighter", "requires_all": ["missing_context"]},
                ]}}
        core = self.core()
        core["source_request"] = "A human witch fires a return shot."
        controls = prompt_generator.creative_controls.resolve(core["source_request"],
            context={"subject_category": "human"}, overrides={"sensual": 0, "fetish": 0}, seed=1)
        core["creative_controls_sha256"] = controls["canonical_sha256"]
        slots, binding, _ = prompt_generator.retrieve_core_slots(data, core, controls)
        ids = {row["id"] for row in slots["action"]["candidates"]}
        self.assertIn("slot:action:counterfire", ids)
        self.assertNotIn("slot:action:excluded", ids)
        self.assertNotIn("slot:action:blocked", ids)
        self.assertEqual(binding["active_slots"]["action"]["source_fields"], ["event"])
        self.assertEqual(binding["candidate_adoption"], "optional")

    def test_subject_lookup_keeps_typed_human_and_adult_style_guards(self):
        data = {"candidate_semantic_policy": {"slot_dimensions": {"subject": ["subject"]}},
                "slots": {"subject": [
                    {"id": "generic", "en": "a human witness", "tags": ["human"]},
                    {"id": "witch", "en": "an adult human witch with feline ears", "tags": ["human", "witch", "adult", "role"]},
                    {"id": "cat", "en": "a stray cat", "tags": ["animal"]},
                    {"id": "adult_styling", "en": "an adult human witch in suggestive styling", "tags": ["human", "witch", "adult", "suggestive"]},
                ]}}
        core = self.core()
        core["source_request"] = "An adult human cat-eared witch."
        controls = prompt_generator.creative_controls.resolve(core["source_request"],
            context={"subject_category": "human"}, overrides={"sensual": 0, "fetish": 0}, seed=1)
        core["creative_controls_sha256"] = controls["canonical_sha256"]
        slots, _, _ = prompt_generator.retrieve_core_slots(data, core, controls)
        ids = {row["id"] for row in slots["subject"]["candidates"]}
        self.assertIn("slot:subject:witch", ids)
        self.assertNotIn("slot:subject:cat", ids)
        self.assertNotIn("slot:subject:adult_styling", ids)

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




if __name__ == "__main__":
    unittest.main()
