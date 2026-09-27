"""Research-to-runtime photographic relations and candidate exposure."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))

import photo_candidate_semantics as candidate_semantics
import prompt_generator as pg
from visual_profile_contracts import compile_visual_profile


class PhotorealismElementsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assets = SKILL / "assets"
        cls.extension = json.loads(
            (assets / "photo_prompt_photorealism_elements_extension.json").read_text()
        )
        cls.registry = pg.load_visual_obligation_registry(
            assets / "photo_prompt_visual_obligations.json"
        )
        cls.profiles = {
            p["id"]: p for p in cls.registry["profiles"] if p["id"].startswith("pr_")
        }
        cls.only_new = {
            **cls.registry,
            "profiles": list(cls.profiles.values()),
        }
        cls.index = pg.build_visual_profile_index_payload(cls.only_new)
        cls.data = pg.load_json(assets / "photo_prompt_tags.json")

    def hard(self, text):
        rows = [{
            "source": "concept_lock",
            "text": text,
            "polarity": "required",
            "priority": "critical",
            "mandatory": True,
        }]
        found = pg.resolve_visual_profile_hits(
            self.only_new, rows, visual_profile_index=self.index, adult_context=True
        )
        return {
            hit["profile_id"] for hit in found["hits"]
            if hit.get("match_basis") == "exact" and hit.get("hard_eligible")
        }

    def test_exact_complete_relation_hardens_but_label_or_fragment_does_not(self):
        self.assertEqual(len(self.profiles), 12)
        for profile in self.profiles.values():
            with self.subTest(profile=profile["id"]):
                exact = profile["activation"]["exact_terms"][0]
                self.assertEqual(self.hard(exact), {profile["id"]})
                self.assertNotIn(profile["id"], self.hard("not " + exact))
                first = profile["authored_components"]["components"][0]["match_terms"][0]
                self.assertNotIn(profile["id"], self.hard(first))
                self.assertEqual(len(compile_visual_profile(profile)["render_gates"]), 4)
        for broad in (
            "photorealistic", "documentary photography", "RAW image",
            "film grain", "sensor noise", "clean portrait", "카메라 사진",
            "reposted photo", "one contact shadow",
        ):
            self.assertEqual(self.hard(broad), set(), broad)

    def test_all_researched_visual_rows_are_optional_candidates(self):
        entries = [
            entry for rows in self.extension["slots"].values() for entry in rows
        ]
        self.assertEqual(len(entries), 19)
        self.assertTrue(all(e["affected_dimensions"] is not None for e in entries))
        source_ids = {e["id"] for e in entries}
        loaded_ids = {e["id"] for rows in self.data["slots"].values() for e in rows}
        self.assertTrue(source_ids <= loaded_ids)
        self.assertNotIn("pr_documentary_authenticity_boundary_candidate", loaded_ids)
        self.assertNotIn("pr_conditional_imperfection_budget_candidate", loaded_ids)
        self.assertEqual(len(self.extension["visual_semantics"]), 3)

    def test_bundles_require_all_members_and_open_dimensions(self):
        for bundle in self.data["candidate_bundles"]:
            if not bundle["id"].startswith("pe_"):
                continue
            with self.subTest(bundle=bundle["id"]):
                self.assertEqual(
                    bundle["profile_activation"], "independent_request_evidence_only"
                )
                dims = set()
                slots = {}
                for member in bundle["member_candidates"]:
                    dims.update(member["affected_dimensions"])
                    slots.setdefault(member["slot"], {"candidates": []})[
                        "candidates"
                    ].append({
                        "id": member["id"], "applicability": {"status": "eligible"}
                    })
                pack = {
                    "slots": slots,
                    "authorial_core": {"intent_lock": {"open_dimensions": list(dims)}},
                }
                source = {**self.data, "candidate_bundles": [bundle]}
                self.assertEqual(
                    len(candidate_semantics.public_bundles(source, pack)["candidates"]), 1
                )
                missing = copy.deepcopy(pack)
                next(iter(missing["slots"].values()))["candidates"].clear()
                self.assertEqual(
                    candidate_semantics.public_bundles(source, missing)["candidates"], []
                )
                locked = copy.deepcopy(pack)
                locked["authorial_core"]["intent_lock"]["open_dimensions"].pop()
                self.assertEqual(
                    candidate_semantics.public_bundles(source, locked)["candidates"], []
                )

    def test_generated_indexes_bind_sources(self):
        assets = SKILL / "assets"
        semantic = pg.load_semantic_index_payload(
            assets / "photo_prompt_semantic_index.json"
        )
        pg.validate_semantic_index_metadata(semantic, self.data)
        for slot, rows in self.extension["slots"].items():
            for entry in rows:
                self.assertIn(f"slot:{slot}:{entry['id']}", semantic["entries"])
        visual = json.loads(
            (assets / "photo_prompt_visual_profile_index.json").read_text()
        )
        pg.validate_visual_profile_index_metadata(visual, self.registry)
        self.assertTrue(set(self.profiles) <= set(visual["entries"]))


if __name__ == "__main__":
    unittest.main()
