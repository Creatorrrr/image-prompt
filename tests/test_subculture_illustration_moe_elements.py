"""Focused contract tests for the additive 29-element moe research layer."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "subculture-illustration-image-generator"
SCRIPT_ROOT = SKILL_ROOT / "scripts"
ASSET_ROOT = SKILL_ROOT / "assets"
sys.path.insert(0, str(SCRIPT_ROOT))

from moe_element_runtime import (  # noqa: E402
    AUDIT_SCHEMA,
    COMPOSED_SCHEMA,
    GRAMMAR_SCHEMA,
    PACK_AUDIT_SCHEMA,
    PACK_SCHEMA,
    PLAN_SCHEMA,
    MoeElementError,
    audit_moe_candidate_pack,
    audit_moe_element_prompt,
    build_moe_candidate_pack,
    build_moe_element_plan,
    compose_moe_prompt_draft,
    list_moe_elements,
    load_moe_element_assets,
    load_moe_grammar_assets,
    resolve_element_tokens,
)
from compile_moe_grammar_v2 import compile_grammar  # noqa: E402
from illustration_runtime import build_candidate_pack  # noqa: E402


class SubcultureIllustrationMoeElementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.assets = load_moe_element_assets(ASSET_ROOT)

    def test_inventory_is_exact_34_origin_articles_to_29_elements(self) -> None:
        self.assertEqual(29, len(self.assets.records_by_id))
        origin_sources = [
            source
            for source in self.assets.research["sources"]
            if source["kind"] == "origin_record"
        ]
        self.assertEqual(34, len(origin_sources))
        self.assertEqual(
            {
                "character_relationship_narrative": 8,
                "wardrobe": 6,
                "body_hair_pose": 7,
                "expression_staging_perception": 3,
                "participatory_social_meme": 3,
                "fantasy_hazard": 2,
            },
            self.assets.payload["category_counts"],
        )
        self.assertEqual(
            list(range(1, 30)),
            [row["ordinal"] for row in list_moe_elements(self.assets)],
        )
        for record in self.assets.records_by_id.values():
            self.assertTrue(record["origin_source_ids"])
            self.assertTrue(record["independent_source_ids"])

    def test_all_29_direct_selections_compile_and_audit(self) -> None:
        for element_id in self.assets.records_by_id:
            with self.subTest(element_id=element_id):
                plan = build_moe_element_plan([element_id], assets=self.assets)
                self.assertEqual(PLAN_SCHEMA, plan["schema"])
                self.assertEqual([element_id], plan["selected_element_ids"])
                prompt = (
                    f"Original illustration. {plan['composition']['prompt_block_en']}"
                )
                audit = audit_moe_element_prompt(plan, prompt, assets=self.assets)
                self.assertEqual(AUDIT_SCHEMA, audit["schema"])
                self.assertEqual("pass", audit["status"], audit["failures"])


class SubcultureIllustrationMoeGrammarV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.legacy = load_moe_element_assets(ASSET_ROOT)
        cls.assets = cls.legacy
        cls.grammar = load_moe_grammar_assets(
            ASSET_ROOT,
            legacy_assets=cls.legacy,
        )
        cls.corpus = json.loads(
            (
                ASSET_ROOT / "research_evidence_moe_elements" / "intent_corpus_v2.json"
            ).read_text(encoding="utf-8")
        )

    def _build(self, row: dict[str, object], *, seed: int = 19) -> tuple[dict, dict]:
        request = str(row["request_ko"])
        base = build_candidate_pack(
            request,
            seed=seed,
            creativity=0.5,
            contract_version="v2",
        )
        pack = build_moe_candidate_pack(
            base,
            row["expected_element_ids"],
            preference_text=request,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        return base, pack

    def test_compiled_grammar_is_reproducible_and_research_rich(self) -> None:
        compiled = compile_grammar(ASSET_ROOT)
        stored = json.loads(
            (ASSET_ROOT / "illustration_moe_grammar_v2.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(compiled, stored)
        self.assertEqual(GRAMMAR_SCHEMA, stored["schema"])
        self.assertEqual(29, stored["element_count"])
        self.assertGreaterEqual(stored["candidate_count"], 200)
        self.assertEqual(29, len(self.grammar.elements_by_id))
        for element in self.grammar.elements_by_id.values():
            self.assertGreaterEqual(len(element["research_questions"]), 3)
            self.assertGreaterEqual(len(element["semantic_subtypes"]), 2)
            self.assertGreaterEqual(len(element["preference_axes"]), 2)
            self.assertGreaterEqual(len(element["candidates"]), 5)
            self.assertEqual(
                {0, 1, 2},
                {candidate["novelty_level"] for candidate in element["candidates"]},
            )

    def test_twelve_prompt_evidence_comparisons_are_bound_to_current_grammar(
        self,
    ) -> None:
        qualification = json.loads(
            (
                ASSET_ROOT / "research_evidence_moe_elements" / "qualification_v2.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            "subculture-illustration-moe-prompt-qualification/v2",
            qualification["schema"],
        )
        self.assertEqual(self.grammar.grammar_sha256, qualification["grammar_sha256"])
        self.assertEqual(12, qualification["case_count"])
        self.assertEqual(12, qualification["pass_count"])
        self.assertEqual("pass", qualification["status"])
        for row in qualification["results"]:
            self.assertEqual("pass", row["v4_audit_status"])
            self.assertEqual("pass", row["contract_evidence_status"])
            self.assertLessEqual(len(row["v4_support_node_ids"]), 2)
            self.assertNotIn("moe_", row["v4_prompt_en"])
            self.assertEqual({2}, set(row["contract_evidence_scores"].values()))

    def test_all_29_neutral_requests_choose_canonical_research_candidates(self) -> None:
        rows = self.corpus["sections"]["neutral_requests"]
        self.assertEqual(29, len(rows))
        for row in rows:
            with self.subTest(case=row["id"]):
                base, pack = self._build(row)
                selected = pack["moe_grammar"]["selected_candidates"]
                self.assertEqual(PACK_SCHEMA, pack["contract_version"])
                self.assertEqual(1, len(selected))
                self.assertTrue(selected[0]["canonical_default"])
                self.assertIn(
                    row["expected_candidate_selection"]["primary_candidate_key"],
                    selected[0]["intent_keys"],
                )
                self.assertEqual(0.5, base["request_contract"]["creativity"])
                self.assertEqual(base["safety"], pack["safety"])
                self.assertEqual(base["negative_en"], pack["negative_en"])
                composed = compose_moe_prompt_draft(
                    pack,
                    "An original adult-character illustration with one causal event",
                )
                audit = audit_moe_candidate_pack(
                    pack,
                    composed,
                    legacy_assets=self.legacy,
                    grammar_assets=self.grammar,
                )
                self.assertEqual(COMPOSED_SCHEMA, composed["schema"])
                self.assertEqual(PACK_AUDIT_SCHEMA, audit["schema"])
                self.assertEqual("pass", audit["status"], audit["failures"])

    def test_all_29_preferences_select_the_expected_material_variant(self) -> None:
        neutral_by_pair = {
            row["pair_id"]: row for row in self.corpus["sections"]["neutral_requests"]
        }
        rows = self.corpus["sections"]["preference_requests"]
        self.assertEqual(29, len(rows))
        for row in rows:
            with self.subTest(case=row["id"]):
                _, preferred_pack = self._build(row)
                _, neutral_pack = self._build(neutral_by_pair[row["pair_id"]])
                preferred = preferred_pack["moe_grammar"]["selected_candidates"][0]
                neutral = neutral_pack["moe_grammar"]["selected_candidates"][0]
                self.assertIn(
                    row["expected_candidate_selection"]["primary_candidate_key"],
                    preferred["intent_keys"],
                )
                self.assertEqual(
                    row["expected_candidate_selection"]["subtype_id"],
                    preferred["subtype_id"],
                )
                self.assertNotEqual(neutral["candidate_id"], preferred["candidate_id"])
                self.assertEqual(
                    "explicit_preference_cue",
                    preferred_pack["moe_intent"][0]["selection_reason"],
                )

    def test_six_cross_element_cases_use_one_global_primary_and_two_supports(
        self,
    ) -> None:
        rows = self.corpus["sections"]["cross_element_combinations"]
        self.assertEqual(6, len(rows))
        for row in rows:
            with self.subTest(case=row["id"]):
                _, pack = self._build(row)
                grammar = pack["moe_grammar"]
                nodes = grammar["selected_nodes"]
                self.assertEqual(
                    row["expected_element_ids"],
                    pack["request_contract"]["selected_element_ids"],
                )
                self.assertEqual(
                    row["expected_primary_element_id"],
                    grammar["sparse_bundle"]["governing_primary_element_id"],
                )
                self.assertEqual(
                    1, sum(node["selected_role"] == "primary" for node in nodes)
                )
                self.assertLessEqual(len(nodes), 3)
                self.assertEqual(
                    len(nodes) - 1, grammar["sparse_bundle"]["support_count"]
                )
                composed = compose_moe_prompt_draft(
                    pack,
                    "An original adult-character illustration with one causal event",
                )
                self.assertIn(
                    "one continuous shared event", composed["prompt_en"].casefold()
                )
                self.assertNotIn("moe_", composed["prompt_en"])
                audit = audit_moe_candidate_pack(
                    pack,
                    composed,
                    legacy_assets=self.legacy,
                    grammar_assets=self.grammar,
                )
                self.assertEqual("pass", audit["status"], audit["failures"])

    def test_creative_cue_changes_development_not_stored_creativity(self) -> None:
        request = "안경을 쓴 성인 수선사의 작가적이고 창의적인 한 장면을 만들어줘."
        base = build_candidate_pack(
            request,
            seed=77,
            creativity=0.5,
            contract_version="v2",
        )
        pack = build_moe_candidate_pack(
            base,
            ["moe_glasses"],
            preference_text=request,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual(0.5, base["request_contract"]["creativity"])
        self.assertTrue(base["authorial_contract"]["creative_development_required"])
        self.assertEqual(2, pack["moe_intent"][0]["target_novelty_level"])
        self.assertEqual(
            2, pack["moe_grammar"]["selected_candidates"][0]["novelty_level"]
        )

    def test_unrequested_elements_and_sparse_evidence_mutations_fail_closed(
        self,
    ) -> None:
        row = self.corpus["sections"]["cross_element_combinations"][0]
        _, pack = self._build(row)
        self.assertEqual(
            set(row["expected_element_ids"]),
            {
                candidate["element_id"]
                for candidate in pack["moe_grammar"]["selected_candidates"]
            },
        )
        composed = compose_moe_prompt_draft(
            pack,
            "An original adult-character illustration with one causal event",
        )
        missing = copy.deepcopy(composed)
        phrase = pack["moe_grammar"]["selected_nodes"][0]["prompt_fragment_en"]
        missing["prompt_en"] = missing["prompt_en"].replace(phrase, "generic pose")
        audit = audit_moe_candidate_pack(
            pack,
            missing,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertIn(
            "literal_evidence", {failure["check"] for failure in audit["failures"]}
        )

        forged = copy.deepcopy(composed)
        forged["chosen_candidate_ids"] = forged["chosen_candidate_ids"][:-1]
        audit = audit_moe_candidate_pack(
            pack,
            forged,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertIn(
            "chosen_candidate_ids", {failure["check"] for failure in audit["failures"]}
        )

    def test_complete_reviewed_aliases_are_explicit_inputs_not_concept_scans(
        self,
    ) -> None:
        for record in self.assets.records_by_id.values():
            alias = record["aliases"][0]
            with self.subTest(alias=alias):
                selected = resolve_element_tokens([alias], assets=self.assets)
                self.assertEqual(record["id"], selected[0]["id"])
        baseline = build_moe_element_plan([], assets=self.assets)
        self.assertEqual([], baseline["selected_element_ids"])
        self.assertEqual("", baseline["composition"]["prompt_block_en"])
        ordinary_prompt = "An original adult character repairs one weathered lantern."
        self.assertEqual(
            "pass",
            audit_moe_element_prompt(baseline, ordinary_prompt, assets=self.assets)[
                "status"
            ],
        )
        with self.assertRaisesRegex(MoeElementError, "unknown moe element"):
            resolve_element_tokens(
                ["a long concept that happens to mention glasses accessory nearby"],
                assets=self.assets,
            )

    def test_six_representative_combinations(self) -> None:
        combinations = [
            (["moe_glasses", "moe_ponytail", "moe_axilla"], "single_frame"),
            (["moe_classic_bunny_costume", "moe_stockings"], "single_frame"),
            (["moe_maternal_care", "moe_glasses"], "single_frame"),
            (["moe_darkening_corruption", "moe_tsf_transformation"], "sequence"),
            (["moe_pajama_challenge", "moe_abdomen"], "paired_frame"),
            (
                ["moe_sensory_deprivation_magic", "moe_quicksand_sinking"],
                "single_frame",
            ),
        ]
        for tokens, output_mode in combinations:
            with self.subTest(tokens=tokens):
                plan = build_moe_element_plan(
                    tokens, output_mode=output_mode, assets=self.assets
                )
                prompt = (
                    f"Original illustration. {plan['composition']['prompt_block_en']}"
                )
                self.assertEqual(
                    "pass",
                    audit_moe_element_prompt(plan, prompt, assets=self.assets)[
                        "status"
                    ],
                )

    def test_conflicts_and_representation_limits_fail_closed(self) -> None:
        for pair in (
            ["moe_i_balance_pose", "moe_thigh_gap"],
            ["moe_i_balance_pose", "moe_adult_finger_sucking"],
            ["moe_classic_bunny_costume", "moe_reverse_bunny_costume"],
        ):
            with (
                self.subTest(pair=pair),
                self.assertRaisesRegex(MoeElementError, "incompatible"),
            ):
                build_moe_element_plan(pair, assets=self.assets)
        with self.assertRaisesRegex(MoeElementError, "cannot prove"):
            build_moe_element_plan(
                ["moe_darkening_corruption"],
                output_mode="single_frame",
                assets=self.assets,
            )
        with self.assertRaisesRegex(MoeElementError, "optical interaction"):
            build_moe_element_plan(
                ["moe_screen_shake_illusion", "moe_tsf_transformation"],
                assets=self.assets,
            )

    def test_prompt_and_plan_mutations_are_rejected(self) -> None:
        plan = build_moe_element_plan(["moe_bubble_tea_challenge"], assets=self.assets)
        valid_prompt = (
            f"Original illustration. {plan['composition']['prompt_block_en']}"
        )
        self.assertEqual(
            "pass",
            audit_moe_element_prompt(plan, valid_prompt, assets=self.assets)["status"],
        )

        missing_contact = valid_prompt.replace(
            "visible contact shadow", "ordinary shading"
        )
        failure = audit_moe_element_prompt(plan, missing_contact, assets=self.assets)
        self.assertEqual("fail", failure["status"])
        self.assertIn(
            "literal_evidence", {item["check"] for item in failure["failures"]}
        )

        forged = copy.deepcopy(plan)
        forged["selected_element_ids"] = ["moe_glasses"]
        failure = audit_moe_element_prompt(forged, valid_prompt, assets=self.assets)
        self.assertEqual("fail", failure["status"])
        self.assertTrue(
            {"plan_id", "replay"}.intersection(
                item["check"] for item in failure["failures"]
            )
        )

    def test_existing_safety_retry_and_photo_baseline_assets_are_byte_stable(
        self,
    ) -> None:
        expected = {
            "image_generation_retry_policy_v1.json": "650f4123c5983a58d88fe888031add6e18966899e22713a17d4c187656e584b3",
            "photo_regression_baseline_v1.json": "3db499287144390ea4724a916069ef1a01b7b6d86064cebee56dd4a496d252c8",
        }
        for name, digest in expected.items():
            with self.subTest(name=name):
                self.assertEqual(
                    digest, hashlib.sha256((ASSET_ROOT / name).read_bytes()).hexdigest()
                )


if __name__ == "__main__":
    unittest.main()
