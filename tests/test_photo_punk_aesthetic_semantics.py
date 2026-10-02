
from tests import photo_prompt_fixtures as current_fixtures
import json
import random
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "photo-prompt-image-generator" / "scripts"
ASSETS = ROOT / "skills" / "photo-prompt-image-generator" / "assets"
TAGS_PATH = ASSETS / "photo_prompt_tags.json"
QUALITY_PATH = ASSETS / "photo_prompt_quality_layers.json"
EXTENSION_PATH = ASSETS / "photo_prompt_punk_aesthetics_extension.json"
EVIDENCE_PATH = ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"

sys.path.insert(0, str(SCRIPTS))
import prompt_generator  # noqa: E402


EXPECTED_STATUS_COUNTS = {
    "established_genre": 5,
    "established_derivative": 4,
    "emerging_community_genre": 1,
    "design_shorthand": 10,
}


class PunkAestheticSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.data = prompt_generator.load_json(TAGS_PATH)
        cls.data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = (
            prompt_generator.load_quality_layers(QUALITY_PATH)
        )
        cls.contracts = {
            item["id"]: item for item in cls.extension["visual_semantics"]
        }
        cls.catalog = set()
        for entries in cls.data["slots"].values():
            cls.catalog.update(item["id"] for item in entries)

    def test_contract_freezes_twenty_terms_and_evidence_tiers(self):
        self.assertEqual(len(self.contracts), 20)
        self.assertEqual(
            set(self.contracts),
            {
                "cyberpunk",
                "steampunk",
                "dieselpunk",
                "decopunk",
                "atompunk",
                "raypunk",
                "clockpunk",
                "teslapunk",
                "biopunk",
                "nanopunk",
                "solarpunk",
                "lunarpunk",
                "oceanpunk",
                "skypunk",
                "desertpunk",
                "stonepunk",
                "rococopunk",
                "magipunk",
                "aetherpunk",
                "crystalpunk",
            },
        )
        counts = {}
        for contract in self.contracts.values():
            counts[contract["establishment"]] = counts.get(contract["establishment"], 0) + 1
            self.assertTrue(contract["primary_visual_proposition"])
            self.assertGreaterEqual(len(contract["component_groups"]), 3)
            self.assertGreaterEqual(len(contract["confusion_boundaries"]), 3)
            self.assertGreaterEqual(len(contract["candidate_ids"]), 3)
            if contract["id"] != "solarpunk":
                self.assertEqual(len(contract["candidate_ids"]), 4)
            for group in contract["component_groups"]:
                self.assertTrue(group["id"])
                self.assertGreaterEqual(len(group["visible_evidence"]), 2)
            if contract["establishment"] in {
                "design_shorthand",
                "emerging_community_genre",
            }:
                self.assertEqual(contract["activation_mode"], "exact_only")
        self.assertEqual(counts, EXPECTED_STATUS_COUNTS)

    def test_every_contract_resolves_to_live_slot_candidates(self):
        for contract in self.contracts.values():
            with self.subTest(contract=contract["id"]):
                self.assertTrue(set(contract["candidate_ids"]) <= self.catalog)
                world = self.data["slots"]["narrative_core" if contract["id"] == "solarpunk" else "world"]
                props = self.data["slots"]["prop"]
                self.assertIn(contract["candidate_ids"][0], {row["id"] for row in world})
                self.assertLessEqual(set(contract["candidate_ids"][1:]), {row["id"] for row in props})




    def test_candidates_are_original_and_do_not_encode_fixed_identity(self):
        extension_text = json.dumps(self.extension, ensure_ascii=False).lower()
        for protected_reference in (
            "blade runner",
            "mad max",
            "bioshock",
            "frostpunk",
            "the flintstones",
            "kaladesh",
            "final fantasy",
            "star wars",
        ):
            self.assertNotIn(protected_reference, extension_text)
        subject = next(
            item
            for item in self.extension["slots"]["subject"]
            if item["id"] == "punk_world_resident_subject"
        )
        self.assertIn("without prescribing face body ethnicity or fixed wardrobe", subject["embedding_text"])

    def test_research_ledger_rows_reference_real_candidates(self):
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        punk_rows = [row for row in rows if row["id"].startswith("punk_aesthetic_")]
        self.assertGreaterEqual(len(punk_rows), 16)
        self.assertEqual(len({row["id"] for row in punk_rows}), len(punk_rows))
        for row in punk_rows:
            self.assertEqual(row["status"], "approved")
            self.assertTrue(set(row["candidate_ids"]) <= self.catalog, row["id"])
            self.assertIn("no ", row["reuse_note"].lower())
            self.assertIn("copied", row["reuse_note"].lower())
        evidence_by_topic = {}
        for row in punk_rows:
            evidence_by_topic.setdefault(row.get("topic_id"), set()).update(row["candidate_ids"])
        for concept_id, contract in self.contracts.items():
            if concept_id in {"solarpunk", "magipunk", "aetherpunk"}:
                continue
            self.assertTrue(
                set(contract["candidate_ids"]) <= evidence_by_topic.get(concept_id, set()),
                concept_id,
            )


if __name__ == "__main__":
    unittest.main()
