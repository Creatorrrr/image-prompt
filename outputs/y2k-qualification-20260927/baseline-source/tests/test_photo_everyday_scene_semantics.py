"""Everyday event data: narrow duties, optional admission, and index binding."""

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
sys.path.insert(0, str(SKILL / "scripts"))

import photo_candidate_semantics as candidate_semantics
import prompt_generator as pg
from visual_profile_contracts import compile_visual_profile


class EverydaySceneSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = json.loads(
            (ASSETS / "photo_prompt_everyday_scene_extension.json").read_text()
        )
        cls.registry = pg.load_visual_obligation_registry(
            ASSETS / "photo_prompt_visual_obligations.json"
        )
        cls.profiles = {
            row["id"]: row for row in cls.registry["profiles"]
            if row["id"].startswith("ed_")
        }
        cls.only_new = {**cls.registry, "profiles": list(cls.profiles.values())}
        cls.profile_index = pg.build_visual_profile_index_payload(cls.only_new)
        cls.data = pg.load_json(ASSETS / "photo_prompt_tags.json")

    def hard_hits(self, text):
        rows = [{
            "source": "concept_lock", "text": text, "polarity": "required",
            "priority": "critical", "mandatory": True,
        }]
        found = pg.resolve_visual_profile_hits(
            self.only_new, rows, visual_profile_index=self.profile_index,
            adult_context=True,
        )
        return {
            hit["profile_id"] for hit in found["hits"]
            if hit.get("match_basis") == "exact" and hit.get("hard_eligible")
        }

    def test_complete_relation_only_activates_hard_profile(self):
        self.assertEqual(len(self.profiles), 7)
        for profile in self.profiles.values():
            with self.subTest(profile=profile["id"]):
                complete = profile["activation"]["exact_terms"][0]
                self.assertEqual(self.hard_hits(complete), {profile["id"]})
                self.assertNotIn(profile["id"], self.hard_hits("not " + complete))
                part = profile["authored_components"]["components"][0]["match_terms"][0]
                self.assertNotIn(profile["id"], self.hard_hits(part))
                self.assertEqual(len(compile_visual_profile(profile)["render_gates"]), 4)
        for broad in (
            "everyday scene", "일상적인 장면", "neighborhood cafe",
            "small market", "clean home", "a person uses a phone",
            "candid portrait", "ordinary city sidewalk",
        ):
            self.assertEqual(self.hard_hits(broad), set(), broad)

    def test_twenty_research_rows_are_optional_and_bound_to_source(self):
        source = json.loads((ROOT / "docs/research-evidence/photo-prompt/everyday-scene-20260923/candidate-bundles.json").read_text())
        source_ids = {row["id"] for row in source["candidate_bundles"]}
        entries = [row for values in self.extension["slots"].values() for row in values]
        self.assertEqual(len(entries), 20)
        self.assertEqual(source_ids, {row["id"] for row in self.extension["visual_semantics"]})
        self.assertEqual({row["id"] for row in entries}, {name + "_candidate" for name in source_ids})
        self.assertTrue(all("human" in row["tags"] and row["affected_dimensions"] for row in entries))
        for bundle in self.data["candidate_bundles"]:
            if bundle["id"] in source_ids:
                self.assertEqual(bundle["adoption"], "optional")
                self.assertEqual(bundle["profile_activation"], "independent_request_evidence_only")
        ref = self.extension["maintenance_ref"]
        record = json.loads((ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (ref["record_id"] + ".json")).read_text())
        self.assertEqual(ref["sha256"], candidate_semantics.digest(record))
        raw = copy.deepcopy(self.extension)
        raw.pop("maintenance_ref")
        self.assertEqual(record["authored_source_sha256"], candidate_semantics.digest(raw))

    def test_bundles_require_open_dimensions_and_admit_natural_scene_phrases(self):
        own = [row for row in self.data["candidate_bundles"] if row["id"].startswith("ed_")]
        self.assertEqual(len(own), 20)
        for bundle in own:
            member = bundle["member_candidates"][0]
            dimensions = member["affected_dimensions"]
            pack = {
                "authorial_core": {"intent_lock": {"open_dimensions": dimensions}},
                "slots": {member["slot"]: {"candidates": [
                    {"id": member["id"], "applicability": {"status": "eligible"}}
                ]}},
            }
            selected = {**self.data, "candidate_bundles": [bundle]}
            self.assertEqual(len(candidate_semantics.public_bundles(selected, pack)["candidates"]), 1)
            pack["authorial_core"]["intent_lock"]["open_dimensions"] = []
            self.assertEqual(candidate_semantics.public_bundles(selected, pack)["candidates"], [])

        scenes = [
            ("An adult waits at a cafe pickup counter while a prepared drink rests on the service side.", "action", "ed_cafe_pickup_wait"),
            ("An adult compares two items at a market shelf while holding one beside the other.", "action", "ed_market_compare"),
            ("An adult is tidying a clean actively used room and returns a cloth to its shelf.", "setting", "ed_clean_room_reset"),
            ("One adult shows a phone screen to another adult who reacts to the shared view.", "relationship", "ed_shared_phone"),
        ]
        for scene, dimension, bundle_id in scenes:
            with self.subTest(bundle=bundle_id):
                core = {
                    "contract_version": "photo-authorial-core/v3", "source_request": scene,
                    "subject": "an adult person", "setting": scene, "baseline_prompt_en": scene,
                    "intent_lock": {"open_dimensions": [dimension]},
                }
                pack = {"authorial_core": core, "slots": {}, "provenance": {"seed": 41}}
                exposed = pg.candidate_pack_candidate_bundles(self.data, pack)
                self.assertIn("bundle:" + bundle_id, {row["id"] for row in exposed["candidates"]})
                core["intent_lock"]["open_dimensions"] = []
                exposed = pg.candidate_pack_candidate_bundles(self.data, pack)
                self.assertNotIn("bundle:" + bundle_id, {row["id"] for row in exposed["candidates"]})

    def test_generated_indexes_bind_new_data(self):
        semantic = pg.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
        pg.validate_semantic_index_metadata(semantic, self.data)
        for slot, rows in self.extension["slots"].items():
            for row in rows:
                self.assertIn(f"slot:{slot}:{row['id']}", semantic["entries"])
        visual = json.loads((ASSETS / "photo_prompt_visual_profile_index.json").read_text())
        pg.validate_visual_profile_index_metadata(visual, self.registry)
        self.assertTrue(set(self.profiles) <= set(visual["entries"]))


if __name__ == "__main__":
    unittest.main()
