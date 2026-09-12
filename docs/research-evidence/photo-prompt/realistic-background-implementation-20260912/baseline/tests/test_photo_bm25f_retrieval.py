from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "photo-prompt-image-generator" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import bm25f_retrieval  # noqa: E402


POLICY = {
    "k1": 1.2,
    "fields": {
        "aliases": {"weight": 4.0, "b": 0.2},
        "definition": {"weight": 2.0, "b": 0.75},
        "visible_actions": {"weight": 2.5, "b": 0.65},
        "support_cues": {"weight": 0.5, "b": 0.75},
    },
    "query_fields": {
        "request": 3.0,
        "interpreted_intent": 2.0,
        "event": 2.0,
    },
    "candidate_limit": 8,
    "rrf_k": 60,
}


class PhotoBm25fRetrievalTests(unittest.TestCase):
    def test_korean_boundaries_do_not_turn_appearance_into_moe(self):
        lexicon = ["모에", "츤데레"]
        self.assertNotIn(
            "모에",
            bm25f_retrieval.tokenize_bm25f_text("외모에 어울리는", lexicon=lexicon),
        )
        self.assertNotIn(
            "모에",
            bm25f_retrieval.tokenize_bm25f_text("규모에 맞는", lexicon=lexicon),
        )
        self.assertIn(
            "모에",
            bm25f_retrieval.tokenize_bm25f_text("모에하게", lexicon=lexicon),
        )
        self.assertIn(
            "츤데레",
            bm25f_retrieval.tokenize_bm25f_text("츤데레를", lexicon=lexicon),
        )
        self.assertIn(
            "튜너",
            bm25f_retrieval.tokenize_bm25f_text("튜너들이", lexicon=["튜너"]),
        )

    def test_japanese_compounds_use_longest_first_authored_lexicon(self):
        tokens = bm25f_retrieval.tokenize_bm25f_text(
            "ツンデレメイド",
            lexicon=["ツンデレ", "メイド", "デレ"],
        )
        self.assertIn("ツンデレ", tokens)
        self.assertIn("メイド", tokens)
        self.assertNotIn("デレ", tokens)

        mixed_tokens = bm25f_retrieval.tokenize_bm25f_text(
            "物理パペットのちびSDマスコットとして",
            lexicon=["ちびSDマスコット"],
        )
        self.assertTrue({"ちび", "sd", "マスコット"} <= set(mixed_tokens))

    def test_alias_field_outranks_incidental_support_cue(self):
        documents = {
            "direct": {
                "aliases": ["츤데레"],
                "definition": ["guarded warmth toward an adult peer"],
                "visible_actions": [],
                "support_cues": [],
            },
            "incidental": {
                "aliases": [],
                "definition": ["ordinary portrait"],
                "visible_actions": [],
                "support_cues": ["츤데레 츤데레 츤데레"],
            },
        }
        index = bm25f_retrieval.build_bm25f_index(
            documents,
            policy=POLICY,
            lexicon=["츤데레"],
        )
        ranking = bm25f_retrieval.rank_bm25f(
            index,
            {"request": "츤데레를 행동으로 표현"},
        )
        self.assertEqual(ranking[0]["document_id"], "direct")

    def test_index_validation_detects_stale_authored_fields(self):
        documents = {
            "one": {
                "aliases": ["care"],
                "definition": ["practical care"],
                "visible_actions": ["repairs a broken prop"],
                "support_cues": [],
            }
        }
        index = bm25f_retrieval.build_bm25f_index(documents, policy=POLICY)
        changed = {
            "one": {
                **documents["one"],
                "definition": ["unrelated meaning"],
            }
        }
        with self.assertRaisesRegex(ValueError, "stale"):
            bm25f_retrieval.validate_bm25f_index(
                index,
                changed,
                policy=POLICY,
            )

    def test_rank_and_rrf_ties_are_deterministic(self):
        documents = {
            "b": {
                "aliases": ["care"],
                "definition": [],
                "visible_actions": [],
                "support_cues": [],
            },
            "a": {
                "aliases": ["care"],
                "definition": [],
                "visible_actions": [],
                "support_cues": [],
            },
        }
        index = bm25f_retrieval.build_bm25f_index(documents, policy=POLICY)
        ranking = bm25f_retrieval.rank_bm25f(index, {"request": "care"})
        self.assertEqual([row["document_id"] for row in ranking], ["a", "b"])

        fused = bm25f_retrieval.reciprocal_rank_fusion(
            [["a", "b"], ["b", "a"]],
            k=60,
        )
        self.assertEqual([row["document_id"] for row in fused], ["a", "b"])
        self.assertEqual(fused[0]["lane_count"], 2)


if __name__ == "__main__":
    unittest.main()
