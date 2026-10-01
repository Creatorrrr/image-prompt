from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "photo-prompt-image-generator" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import bm25f_retrieval  # noqa: E402


class PhotoBm25fQueryWeightingTests(unittest.TestCase):
    def setUp(self):
        self.documents = {
            "daylight": {"text": ["soft daylight window"]},
            "grammar": {"text": ["the is a"]},
            "lamp": {"text": ["lamp switched off"]},
        }
        self.policy = {"fields": {"text": {"weight": 1.0, "b": 0.0}}}
        self.index = bm25f_retrieval.build_bm25f_index(
            self.documents, policy=self.policy,
        )

    def test_default_retains_repetition_and_field_weights(self):
        terms = bm25f_retrieval._query_term_weights(
            {"primary": "the window window", "secondary": ["the", "window"]},
            policy={"query_fields": {"primary": 2.0, "secondary": 0.5}},
            lexicon=[],
        )
        self.assertEqual(terms, {"the": 2.5, "window": 4.5})
        query = {"scene": "the the the window lamp"}
        self.assertEqual(
            bm25f_retrieval.rank_bm25f(self.index, query),
            bm25f_retrieval.rank_bm25f(
                self.index, query, query_term_cap=None, function_word_weight=1.0,
            ),
        )

    def test_cap_combines_fields_and_values_before_damping(self):
        terms = bm25f_retrieval._query_term_weights(
            {"primary": ["the window window", "the"], "secondary": "the window"},
            policy={"query_fields": {"primary": 2.0, "secondary": 0.5}},
            lexicon=[], query_term_cap=1.0, function_word_weight=0.15,
        )
        self.assertEqual(terms, {"the": 0.15, "window": 1.0})

    def test_cap_does_not_inflate_small_field_weights(self):
        terms = bm25f_retrieval._query_term_weights(
            {"weak": "window", "disabled": "lamp"},
            policy={"query_fields": {"weak": 0.2, "disabled": 0.0}},
            lexicon=[], query_term_cap=1.0,
        )
        self.assertEqual(terms, {"window": 0.2})

    def test_cap_makes_repeated_queries_rank_identically(self):
        text = "the is soft daylight window lamp switched off"
        options = {"query_term_cap": 1.0, "function_word_weight": 0.15}
        self.assertEqual(
            bm25f_retrieval.rank_bm25f(self.index, {"scene": text}, **options),
            bm25f_retrieval.rank_bm25f(
                self.index, {"scene": [text] * 20, "baseline": text}, **options,
            ),
        )

    def test_function_word_damping_changes_score_without_deleting_match(self):
        normal = bm25f_retrieval.rank_bm25f(self.index, {"scene": "the"})
        damped = bm25f_retrieval.rank_bm25f(
            self.index, {"scene": "the"}, function_word_weight=0.15,
        )
        self.assertEqual(damped[0]["document_id"], "grammar")
        self.assertEqual(damped[0]["matched_terms"], ["the"])
        self.assertAlmostEqual(damped[0]["score"], normal[0]["score"] * 0.15, places=11)

    def test_negation_state_relations_and_other_languages_are_not_damped(self):
        text = (
            "not no never on off with without from under above behind in out "
            "of to has and or window 창문 빛 ランプ 水"
        )
        normal = bm25f_retrieval._query_term_weights(
            {"scene": text}, policy={}, lexicon=[],
        )
        damped = bm25f_retrieval._query_term_weights(
            {"scene": text}, policy={}, lexicon=[], function_word_weight=0.15,
        )
        self.assertEqual(damped, normal)

    def test_zero_damping_does_not_report_zero_weight_matches(self):
        rows = bm25f_retrieval.rank_bm25f(
            self.index, {"scene": "the is a daylight"}, function_word_weight=0.0,
        )
        self.assertEqual([row["document_id"] for row in rows], ["daylight"])
        self.assertEqual(rows[0]["matched_terms"], ["daylight"])
        self.assertEqual(
            bm25f_retrieval.rank_bm25f(
                self.index, {"scene": "the is a"}, function_word_weight=0.0,
            ),
            [],
        )

    def test_query_options_preserve_index_policy_and_validation(self):
        original = copy.deepcopy(self.index)
        bm25f_retrieval.rank_bm25f(
            self.index, {"scene": "the window window"},
            query_term_cap=1.0, function_word_weight=0.15,
        )
        self.assertEqual(self.index, original)
        bm25f_retrieval.validate_bm25f_index(
            self.index, self.documents, policy=self.policy,
        )
        self.assertEqual(self.index["tokenizer_recipe"], "photo-bm25f-tokenizer/v3")
        self.assertEqual(self.index["recipe_version"], "photo-bm25f-index/v1")

    def test_allowed_and_blocked_ids_are_still_enforced(self):
        rows = bm25f_retrieval.rank_bm25f(
            self.index, {"scene": "the window lamp"},
            allowed_ids=["daylight", "lamp"], blocked_ids=["lamp"],
            query_term_cap=1.0, function_word_weight=0.15,
        )
        self.assertEqual([row["document_id"] for row in rows], ["daylight"])

    def test_query_controls_reject_invalid_values_even_for_empty_query(self):
        for cap in (0, -1, float("nan"), float("inf"), True):
            with self.subTest(query_term_cap=cap), self.assertRaises(ValueError):
                bm25f_retrieval.rank_bm25f(self.index, {}, query_term_cap=cap)
        for weight in (-0.1, 1.1, float("nan"), float("inf"), True):
            with self.subTest(function_word_weight=weight), self.assertRaises(ValueError):
                bm25f_retrieval.rank_bm25f(self.index, {}, function_word_weight=weight)


if __name__ == "__main__":
    unittest.main()
