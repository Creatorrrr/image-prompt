from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import photo_candidate_semantics as semantics
import prompt_generator as generator
from tests.test_photo_contextual_appeal import fixture

EVIDENCE = ROOT / "docs/research-evidence/photo-prompt/contextual-appeal-20260929"
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"


class ResearchIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = json.loads((ASSETS / "photo_prompt_contextual_appeal_extension.json").read_text())
        cls.entries = {entry["id"]: (slot, entry) for slot, rows in cls.extension["slots"].items() for entry in rows}
        cls.ledger = json.loads((EVIDENCE / "integration-ledger.json").read_text())

    def test_every_returned_record_has_one_explicit_integration_decision(self):
        academic = json.loads((EVIDENCE / "research/academic/candidate-research.json").read_text())["candidates"]
        community = json.loads((EVIDENCE / "research/community/community-candidate-research.json").read_text())["records"]
        expected = {("academic", row["stable_id"]) for row in academic} | {("community", row["candidate_research_id"]) for row in community}
        actual = [(row["origin"], row["research_id"]) for row in self.ledger["records"]]
        self.assertEqual(len(actual), len(set(actual)))
        self.assertEqual(set(actual), expected)
        for row in self.ledger["records"]:
            self.assertTrue(row["reason"])
            self.assertEqual(bool(row["runtime_ids"]), row["operation"] != "research_only")

    def test_original_artifact_bytes_remain_hash_bound(self):
        manifest = json.loads((EVIDENCE / "download-manifest.json").read_text())
        for report in manifest["research"]:
            for row in report["files"]:
                contents = (EVIDENCE / row["path"]).read_bytes()
                self.assertEqual(len(contents), row["bytes"])
                self.assertEqual(hashlib.sha256(contents).hexdigest(), row["sha256"])

    def test_source_ids_are_resolved_within_each_reports_namespace(self):
        for origin, source_file in (("academic", "sources.json"), ("community", "community-sources.json")):
            sources = json.loads((EVIDENCE / "research" / origin / source_file).read_text())["sources"]
            available = {row["source_id"] for row in sources}
            for record in self.ledger["records"]:
                if record["origin"] == origin:
                    self.assertTrue(set(record["source_ids"]) <= available)

    def test_context_extension_cannot_replace_meaning_scope_or_guards(self):
        base = {"action": [{"id": "original", "en": "one owner's hand at their cuff",
                            "affected_dimensions": ["action"], "for_any": ["human"]}]}
        for field in ("en", "affected_dimensions", "affected_properties", "for_any", "tags", "unknown"):
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "only paraphrases and contexts"):
                semantics.extend_slot_contexts(copy.deepcopy(base), {"action": {"original": {field: []}}})
        for update in ({"missing": {}}, {"action": {"missing": {"paraphrases": ["cue"]}}}):
            with self.assertRaisesRegex(ValueError, "unknown"):
                semantics.extend_slot_contexts(copy.deepcopy(base), update)
        addition = {"action": {"original": {"contexts": [{"id": "ordinary", "limits": "not evidence of memory"}]}}}
        semantics.extend_slot_contexts(base, addition)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            semantics.extend_slot_contexts(base, addition)

    def test_positive_equivalents_are_searchable_but_context_and_limits_are_not(self):
        base = {"action": [{"id": "repair", "en": "skillful work"}]}
        semantics.extend_slot_contexts(base, {"action": {"repair": {
            "paraphrases": ["hands beside an inspectable work result"],
            "contexts": [{"id": "boundary", "ordinary": "unsearchableordinarytoken",
                          "limits": "unsearchablecounterexampletoken"}]}}})
        row = base["action"][0]
        for text in (generator.semantic_text_for_entry(row, "action"),
                     json.dumps(generator.semantic_bm25f_fields_for_entry(row, "action"))):
            self.assertIn("inspectable work result", text)
            self.assertNotIn("unsearchableordinarytoken", text)
            self.assertNotIn("unsearchablecounterexampletoken", text)

    def test_reviewed_paraphrases_preserve_candidate_scope_and_are_searchable(self):
        additions = json.loads((EVIDENCE / "control-implementation-20260929/positive-paraphrases.json").read_text())
        for entry_id, phrases in additions.items():
            slot, row = self.entries[entry_id]
            self.assertTrue(row["affected_dimensions"])
            self.assertTrue(row["contextual_usage"])
            for phrase in phrases:
                self.assertIn(phrase, generator.semantic_text_for_entry(row, slot))
                self.assertIn(phrase, json.dumps(generator.semantic_bm25f_fields_for_entry(row, slot), ensure_ascii=False))

    def test_partial_neighbors_do_not_become_false_synonyms(self):
        updates = self.extension["existing_slot_context_extensions"]
        self.assertNotIn("pouring_coffee", updates.get("action", {}))
        self.assertIn("ctx_tea_sequence", self.entries)
        self.assertIn("ctx_c012", self.entries)  # tooth repair is not lipstick color
        self.assertNotIn("red_lip_classic", updates.get("makeup_style", {}))
        self.assertIn("ctx_c019", self.entries)  # thin choker is not necessarily tattoo loops
        self.assertIn("ctx_c135", self.entries)  # generic pencil skirt is not fixed ivory/blue
        joined = {row["research_id"]: row for row in self.ledger["records"]}
        self.assertEqual(joined["C058"]["runtime_ids"], joined["sfr26.loose-tie-after-duty"]["runtime_ids"])

    def test_wearing_change_obeys_property_and_action_locks_without_axis_tags(self):
        slot, row = self.entries["ctx_c158"]
        self.assertNotIn("sensual", row["tags"])
        self.assertNotIn("fetish", row["tags"])
        data, core, result = fixture()
        data["slots"] = {slot: [copy.deepcopy(row)]}
        core["baseline_prompt_en"] = "An adult removes a protective arm sleeve after work while meeting another adult's gaze."
        def ids():
            adult = generator.candidate_pack_contextual_adult_appeal(data, result, {}, authorial_core=core)
            return {candidate["entry_id"] for axis in adult["axes"].values() for candidate in axis["candidate_inventory"]}
        self.assertIn(row["id"], ids())
        core["intent_lock"]["semantic_anchors"].append({"dimension": "appearance", "target": "main_subject", "property": "wardrobe.wearing_state", "prompt_evidence": "sleeves remain on"})
        self.assertNotIn(row["id"], ids())
        core["intent_lock"]["semantic_anchors"].pop()
        core["intent_lock"]["locked_dimensions"].append("action")
        self.assertNotIn(row["id"], ids())

    def test_nonvisual_records_and_locked_face_scope_are_not_smuggled_into_adult_route(self):
        decisions = {row["research_id"]: row for row in self.ledger["records"]}
        for rid in ("C061", "C068", "C103", "sfr26.sequence-required"):
            self.assertEqual(decisions[rid]["operation"], "research_only")
        self.assertIn("body_geometry", self.entries["ctx_c035"][1]["affected_dimensions"])
        self.assertIn("setting", self.entries["ctx_wet_coat_dry_layer"][1]["affected_dimensions"])
        data, core, result = fixture()
        data["slots"] = {"anatomical_connection": [self.entries["ctx_c035"][1]]}
        core["intent_lock"]["semantic_anchors"].append({"dimension": "appearance", "target": "main_subject", "property": "face", "prompt_evidence": "the supplied reference face"})
        adult = generator.candidate_pack_contextual_adult_appeal(data, result, {}, authorial_core=core)
        self.assertTrue(all(not axis["candidate_inventory"] for axis in adult["axes"].values()))


if __name__ == "__main__":
    unittest.main()
