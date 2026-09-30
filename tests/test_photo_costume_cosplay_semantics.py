"""Costume relation activation, scope isolation and joint-candidate integration."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as pg
import photo_candidate_semantics as semantics
import validate_photo_prompt_dictionary as dictionary_validation


class CostumeCosplaySemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = json.loads((ASSETS / "photo_prompt_costume_cosplay_extension.json").read_text())
        cls.data = pg.load_json(ASSETS / "photo_prompt_tags.json")
        merged = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.registry = {**merged, "profiles": [p for p in merged["profiles"]
                         if p["id"].startswith("costume_ccx_")]}
        cls.index = pg.build_visual_profile_index_payload(cls.registry)
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}

    def hard(self, text):
        result = pg.resolve_visual_profile_hits(
            self.registry, [{"source": "concept_lock", "text": text,
                             "polarity": "required", "priority": "critical", "mandatory": True}],
            visual_profile_index=self.index, adult_context=True)
        return {hit["profile_id"] for hit in result["hits"]
                if hit.get("match_basis") == "exact" and hit.get("hard_eligible")}

    def test_exact_relation_does_not_impose_the_rest_of_a_costume_family(self):
        pid = "costume_ccx_cc01_01"
        phrase = self.profiles[pid]["activation"]["exact_terms"][0]
        self.assertEqual(self.hard(phrase), {pid})
        self.assertNotIn("costume_ccx_cc01_02", self.hard(phrase))
        self.assertNotIn("costume_ccx_cc01_03", self.hard(phrase))
        self.assertEqual(len(self.registry["profiles"]), 87)
        for profile in self.registry["profiles"]:
            with self.subTest(profile=profile["id"]):
                self.assertIn(profile["id"], self.hard(profile["activation"]["exact_terms"][0]))
                self.assertEqual(len(profile["authored_components"]["components"]), 1)

    def test_broad_roles_characters_and_styles_do_not_select_a_relation(self):
        for text in ["maid", "メイド", "메이드", "witch", "마녀", "armor", "갑옷", "Yelan",
                     "Ahri", "Rumi", "Jinx", "한복", "기모노", "고딕 로리타", "nurse cosplay",
                     "police costume", "pilot", "corset", "fursuit", "magical girl"]:
            with self.subTest(text=text):
                self.assertEqual(self.hard(text), set())

    def test_negated_relation_and_changed_owner_do_not_reuse_exact_meaning(self):
        phrase = self.profiles["costume_ccx_cc18_01"]["activation"]["exact_terms"][0]
        self.assertNotIn("costume_ccx_cc18_01", self.hard("not " + phrase))
        self.assertNotIn("costume_ccx_cc18_01", self.hard(
            "the costume tail root connects visibly to a tree behind the wearer"))

    def test_approximate_vector_discovery_stays_optional(self):
        pid = "costume_ccx_cc13_01"
        vectors = {p["id"]: ([1.0, 0.0] if p["id"] == pid else [0.0, 1.0])
                   for p in self.registry["profiles"]}
        index = pg.build_visual_profile_index_payload(self.registry, vectors=vectors, dimensions=2)
        unsupported = pg.resolve_visual_profile_hits(
            self.registry, [{"source": "authorial_core_interpretation",
                             "text": "a fabricated costume with flexible joints", "polarity": "advisory"}],
            visual_profile_index=index, query_text="flexible costume joints",
            query_vector=[1.0, 0.0], adult_context=True)
        self.assertNotIn(pid, {h["profile_id"] for h in unsupported["hits"]})
        phrase = self.profiles[pid]["semantics"]["paraphrase_examples"][0]
        result = pg.resolve_visual_profile_hits(
            self.registry, [{"source": "authorial_core_interpretation",
                             "text": phrase, "polarity": "advisory"}],
            visual_profile_index=index, query_text=phrase,
            query_vector=[1.0, 0.0], adult_context=True)
        hit = next(h for h in result["hits"] if h["profile_id"] == pid)
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_real_candidates_and_joint_bundles_preserve_scope(self):
        bundles = [b for b in self.data["candidate_bundles"] if b["id"].startswith("costume_b")]
        self.assertEqual(len(bundles), 27)
        merged = {f"slot:{slot}:{e['id']}" for slot, es in self.data["slots"].items() for e in es}
        for bundle in bundles:
            with self.subTest(bundle=bundle["id"]):
                self.assertEqual(bundle["profile_activation"], "independent_request_evidence_only")
                self.assertEqual(bundle["adoption"], "optional")
                slots = {}
                for member in bundle["member_candidates"]:
                    self.assertIn(member["id"], merged)
                    self.assertTrue(member["affected_dimensions"])
                    self.assertNotIn("body_geometry", member["affected_dimensions"])
                    slots.setdefault(member["slot"], {"candidates": []})["candidates"].append(
                        {"id": member["id"], "applicability": {"status": "eligible"}})
                dimensions = {d for m in bundle["member_candidates"] for d in m["affected_dimensions"]}
                pack = {"slots": slots, "authorial_core": {"intent_lock": {"open_dimensions": list(dimensions)}}}
                data = {**self.data, "candidate_bundles": [bundle]}
                self.assertEqual(len(semantics.public_bundles(data, pack)["candidates"]), 1)
                closed = copy.deepcopy(pack)
                closed["authorial_core"]["intent_lock"]["open_dimensions"] = []
                self.assertEqual(semantics.public_bundles(data, closed)["candidates"], [])
                missing = copy.deepcopy(pack)
                next(iter(missing["slots"].values()))["candidates"].pop()
                self.assertEqual(semantics.public_bundles(data, missing)["candidates"], [])

    def test_source_record_and_generated_indexes_bind_the_actual_runtime_data(self):
        ref = self.extension["maintenance_ref"]
        record_path = ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (ref["record_id"] + ".json")
        record = json.loads(record_path.read_text())
        self.assertEqual(ref["sha256"], semantics.digest(record))
        authored = copy.deepcopy(self.extension)
        authored.pop("maintenance_ref")
        self.assertEqual(record["authored_source_sha256"], semantics.digest(authored))
        semantic_index = pg.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
        pg.validate_semantic_index_metadata(semantic_index, self.data)
        ids = {f"slot:{slot}:{e['id']}" for slot, es in self.extension["slots"].items() for e in es}
        self.assertEqual(len(ids), 94)
        self.assertTrue(ids <= set(semantic_index["entries"]))
        full_registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        visual_index = pg.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", full_registry)
        self.assertTrue(set(self.profiles) <= set(visual_index["entries"]))

    def test_merged_registry_is_valid_and_discovery_examples_are_not_exact_triggers(self):
        errors = []
        dictionary_validation.validate_visual_obligation_registry(
            ASSETS / "photo_prompt_visual_obligations.json", errors)
        self.assertEqual(errors, [])
        for profile in self.registry["profiles"]:
            with self.subTest(profile=profile["id"]):
                exact = {term.casefold() for term in profile["activation"]["exact_terms"]}
                examples = {term.casefold() for term in profile["semantics"]["paraphrase_examples"]}
                self.assertFalse(exact & examples)


if __name__ == "__main__":
    unittest.main()
