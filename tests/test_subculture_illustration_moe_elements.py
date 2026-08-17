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
    COMPOSED_SCHEMA_V2,
    COMPOSED_SCHEMA_V4,
    GRAMMAR_SCHEMA,
    GRAMMAR_SCHEMA_V2,
    GRAMMAR_SCHEMA_V4,
    PACK_AUDIT_SCHEMA,
    PACK_AUDIT_SCHEMA_V2,
    PACK_AUDIT_SCHEMA_V4,
    PACK_SCHEMA,
    PACK_SCHEMA_V4,
    PACK_SCHEMA_V6,
    PLAN_SCHEMA,
    MoeElementError,
    audit_moe_candidate_pack,
    audit_moe_element_prompt,
    build_moe_candidate_pack,
    build_moe_element_plan,
    canonical_json_bytes,
    compose_moe_prompt_draft,
    list_moe_elements,
    load_moe_element_assets,
    load_moe_grammar_assets,
    resolve_element_tokens,
)
from compile_moe_grammar_v2 import compile_grammar as compile_grammar_v2  # noqa: E402
from compile_moe_grammar_v3 import compile_grammar as compile_grammar_v3  # noqa: E402
from compile_moe_grammar_v4 import compile_grammar as compile_grammar_v4  # noqa: E402
from build_moe_meaning_contracts_v2 import build_assets as build_visual_assets  # noqa: E402
from illustration_runtime import build_candidate_pack  # noqa: E402
from moe_meaning_contract import runtime_label_present  # noqa: E402
from qualify_moe_grammar_v4 import build_qualification  # noqa: E402


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
            grammar_version="v2",
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
        compiled = compile_grammar_v2(ASSET_ROOT)
        stored = json.loads(
            (ASSET_ROOT / "illustration_moe_grammar_v2.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(compiled, stored)
        self.assertEqual(GRAMMAR_SCHEMA_V2, stored["schema"])
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
                self.assertEqual(PACK_SCHEMA_V4, pack["contract_version"])
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
                self.assertEqual(COMPOSED_SCHEMA_V2, composed["schema"])
                self.assertEqual(PACK_AUDIT_SCHEMA_V2, audit["schema"])
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


class SubcultureIllustrationMoeGrammarV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.legacy = load_moe_element_assets(ASSET_ROOT)
        cls.grammar = load_moe_grammar_assets(
            ASSET_ROOT,
            legacy_assets=cls.legacy,
            grammar_version="v3",
        )
        cls.corpus = json.loads(
            (
                ASSET_ROOT / "research_evidence_moe_elements" / "intent_corpus_v2.json"
            ).read_text(encoding="utf-8")
        )
        cls.foundation = (
            "An original adult-character illustration with one causal event"
        )

    def _build(
        self,
        request: str,
        element_ids: list[str],
        *,
        seed: int = 29,
        output_mode: str = "auto",
    ) -> tuple[dict, dict, dict]:
        base = build_candidate_pack(
            request,
            seed=seed,
            creativity=0.5,
            contract_version="v2",
        )
        pack = build_moe_candidate_pack(
            base,
            element_ids,
            preference_text=request,
            output_mode=output_mode,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        composed = compose_moe_prompt_draft(pack, self.foundation)
        return base, pack, composed

    @staticmethod
    def _rehash_pack(pack: dict) -> None:
        pack["pack_id"] = None
        pack["pack_id"] = hashlib.sha256(canonical_json_bytes(pack)).hexdigest()[:16]

    def test_v3_compile_is_reproducible_and_all_meanings_are_normalized(self) -> None:
        compiled = compile_grammar_v3(ASSET_ROOT)
        stored = json.loads(
            (ASSET_ROOT / "illustration_moe_grammar_v3.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(compiled, stored)
        self.assertEqual(GRAMMAR_SCHEMA, stored["schema"])
        self.assertEqual(29, stored["element_count"])
        self.assertEqual(29, len(self.grammar.elements_by_id))
        for element in stored["elements"]:
            contract = element["meaning_contract"]
            self.assertEqual(
                contract["canonical_definition_ko"],
                element["definition_and_history"],
            )
            self.assertNotIn("SRC_", element["definition_and_history"])
            self.assertFalse(
                any(
                    subtype["id"].startswith("researched_variant_")
                    for subtype in element["semantic_subtypes"]
                )
            )
            self.assertGreaterEqual(len(contract["essential_semantics_ko"]), 2)
            self.assertGreaterEqual(len(contract["non_equivalents_ko"]), 2)
            self.assertGreaterEqual(len(contract["component_groups"]), 2)

        ahegao = self.grammar.elements_by_id["moe_ahegao_expression"][
            "meaning_contract"
        ]
        self.assertIn("성적 쾌감", ahegao["canonical_definition_ko"])
        self.assertIn("표정 통제를 잃은", ahegao["canonical_definition_ko"])
        self.assertEqual("exact_componentized", ahegao["semantic_fidelity"])
        self.assertIn("ahegao", ahegao["runtime_forbidden_labels"])
        self.assertEqual(
            [
                "eye_control_loss",
                "mouth_control_loss",
                "tongue_exposure",
                "secondary_overload_marker",
            ],
            [group["id"] for group in ahegao["component_groups"]],
        )
        self.assertEqual(
            "safe_analogue",
            self.grammar.elements_by_id["moe_mesugaki_provocation"]["meaning_contract"][
                "semantic_fidelity"
            ],
        )

    def test_all_neutral_and_preference_requests_bind_and_audit_meaning(self) -> None:
        rows = [
            *self.corpus["sections"]["neutral_requests"],
            *self.corpus["sections"]["preference_requests"],
        ]
        self.assertEqual(58, len(rows))
        for row in rows:
            with self.subTest(case=row["id"]):
                base, pack, composed = self._build(
                    row["request_ko"], row["expected_element_ids"]
                )
                self.assertEqual(PACK_SCHEMA, pack["contract_version"])
                self.assertEqual(COMPOSED_SCHEMA, composed["schema"])
                self.assertEqual(base["safety"], pack["safety"])
                self.assertEqual(base["negative_en"], pack["negative_en"])
                self.assertEqual(
                    "original_request_plus_canonical_meaning",
                    pack["semantic_contract"]["safety_evaluation_source"],
                )
                self.assertEqual(
                    "forbidden",
                    pack["semantic_contract"]["silent_semantic_substitution"],
                )
                bindings = pack["moe_grammar"]["meaning_bindings"]
                selected = pack["moe_grammar"]["selected_candidates"]
                self.assertEqual(
                    row["expected_element_ids"],
                    [binding["element_id"] for binding in bindings],
                )
                for candidate, binding in zip(selected, bindings, strict=True):
                    self.assertEqual(
                        binding["contract_sha256"],
                        candidate["meaning_contract_sha256"],
                    )
                    for label in binding["contract"]["runtime_forbidden_labels"]:
                        self.assertFalse(
                            runtime_label_present(label, composed["prompt_en"])
                        )
                        self.assertFalse(
                            runtime_label_present(label, composed["negative_en"])
                        )
                audit = audit_moe_candidate_pack(
                    pack,
                    composed,
                    legacy_assets=self.legacy,
                    grammar_assets=self.grammar,
                )
                self.assertEqual(PACK_AUDIT_SCHEMA, audit["schema"])
                self.assertEqual("pass", audit["status"], audit["failures"])

    def test_v3_qualification_is_bound_to_current_assets(self) -> None:
        qualification = json.loads(
            (
                ASSET_ROOT / "research_evidence_moe_elements" / "qualification_v3.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            "subculture-illustration-moe-prompt-qualification/v3",
            qualification["schema"],
        )
        self.assertEqual(self.grammar.grammar_sha256, qualification["grammar_sha256"])
        self.assertEqual(
            self.grammar.payload["meaning_contracts_sha256"],
            qualification["meaning_contracts_sha256"],
        )
        self.assertEqual(29, qualification["meaning_contract_count"])
        self.assertEqual(12, qualification["case_count"])
        self.assertEqual(12, qualification["pass_count"])
        self.assertEqual("pass", qualification["status"])

    def test_sensitive_label_component_and_contract_mutations_fail_closed(self) -> None:
        request = "아헤가오의 눈과 입 구성을 정확히 살린 성인 캐릭터 얼굴을 그려줘."
        _, pack, composed = self._build(request, ["moe_ahegao_expression"])
        self.assertIn("tongue", composed["prompt_en"].casefold())
        self.assertTrue(
            any(
                marker in composed["prompt_en"].casefold()
                for marker in ("drool", "tears", "sweat", "flush", "asymmetry")
            )
        )

        leaked = copy.deepcopy(composed)
        leaked["prompt_en"] += " Use an ahegao expression."
        audit = audit_moe_candidate_pack(
            pack,
            leaked,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertIn(
            "runtime_label_policy", {failure["check"] for failure in audit["failures"]}
        )

        missing = copy.deepcopy(composed)
        for node in pack["moe_grammar"]["selected_nodes"]:
            missing["prompt_en"] = missing["prompt_en"].replace(
                node["prompt_fragment_en"], "Show a generic facial expression."
            )
        audit = audit_moe_candidate_pack(
            pack,
            missing,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertTrue(
            {"literal_evidence", "meaning_component_group"}.issubset(
                {failure["check"] for failure in audit["failures"]}
            )
        )

        forged_pack = copy.deepcopy(pack)
        binding = forged_pack["moe_grammar"]["meaning_bindings"][0]
        binding["contract"]["canonical_definition_ko"] += " 임의 축약."
        forged_hash = hashlib.sha256(
            canonical_json_bytes(binding["contract"])
        ).hexdigest()
        binding["contract_sha256"] = forged_hash
        forged_pack["moe_grammar"]["selected_candidates"][0][
            "meaning_contract_sha256"
        ] = forged_hash
        self._rehash_pack(forged_pack)
        forged_composed = compose_moe_prompt_draft(forged_pack, self.foundation)
        audit = audit_moe_candidate_pack(
            forged_pack,
            forged_composed,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertIn(
            "meaning_bindings", {failure["check"] for failure in audit["failures"]}
        )

        malformed_pack = copy.deepcopy(pack)
        malformed_pack["moe_grammar"]["meaning_bindings"][0]["contract"].pop(
            "component_groups"
        )
        self._rehash_pack(malformed_pack)
        audit = audit_moe_candidate_pack(
            malformed_pack,
            composed,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertIn(
            "meaning_bindings", {failure["check"] for failure in audit["failures"]}
        )

    def test_safe_analogue_and_medium_capability_cannot_be_overclaimed(self) -> None:
        _, safe_pack, _ = self._build(
            "메스가키의 관계적 도발을 성인 캐릭터로 안전하게 표현해줘.",
            ["moe_mesugaki_provocation"],
        )
        forged_safe = copy.deepcopy(safe_pack)
        forged_safe["moe_grammar"]["selected_candidates"][0]["semantic_fidelity"] = (
            "exact_componentized"
        )
        self._rehash_pack(forged_safe)
        forged_composed = compose_moe_prompt_draft(forged_safe, self.foundation)
        audit = audit_moe_candidate_pack(
            forged_safe,
            forged_composed,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertIn(
            "semantic_fidelity", {failure["check"] for failure in audit["failures"]}
        )

        with self.assertRaisesRegex(MoeElementError, "cannot carry"):
            self._build(
                "흑화 전후의 동일 인물을 보여줘.",
                ["moe_darkening_corruption"],
                output_mode="single_frame",
            )

        _, interaction_pack, _ = self._build(
            "화면을 흔들 때 움직여 보이는 착시를 만들어줘.",
            ["moe_screen_shake_illusion"],
        )
        forged_interaction = copy.deepcopy(interaction_pack)
        forged_interaction["moe_grammar"]["frame_contract"]["resolved_output_mode"] = (
            "single_frame"
        )
        self._rehash_pack(forged_interaction)
        forged_composed = compose_moe_prompt_draft(forged_interaction, self.foundation)
        audit = audit_moe_candidate_pack(
            forged_interaction,
            forged_composed,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertIn(
            "meaning_capability", {failure["check"] for failure in audit["failures"]}
        )


class SubcultureIllustrationMoeGrammarV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.legacy = load_moe_element_assets(ASSET_ROOT)
        cls.grammar = load_moe_grammar_assets(
            ASSET_ROOT,
            legacy_assets=cls.legacy,
            grammar_version="v4",
        )
        cls.foundation = (
            "An original adult-character illustration with one causal event"
        )
        cls.corpus = json.loads(
            (
                ASSET_ROOT
                / "research_evidence_moe_elements"
                / "intent_corpus_v2.json"
            ).read_text(encoding="utf-8")
        )

    def _build(
        self,
        requested_tokens: list[str],
        *,
        request: str = "성인 캐릭터로 요청한 시각 의미를 정확히 보여줘.",
        output_mode: str = "auto",
    ) -> tuple[dict, dict]:
        base = build_candidate_pack(
            request,
            seed=43,
            creativity=0.5,
            contract_version="v2",
        )
        pack = build_moe_candidate_pack(
            base,
            requested_tokens,
            preference_text=request,
            output_mode=output_mode,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        composed = compose_moe_prompt_draft(pack, self.foundation)
        return pack, composed

    @staticmethod
    def _rehash_pack(pack: dict) -> None:
        pack["pack_id"] = None
        pack["pack_id"] = hashlib.sha256(canonical_json_bytes(pack)).hexdigest()[:16]

    def test_visual_assets_and_v4_grammar_are_reproducible_and_complete(self) -> None:
        evidence, visual = build_visual_assets(ASSET_ROOT)
        stored_evidence = json.loads(
            (
                ASSET_ROOT
                / "research_evidence_moe_elements"
                / "image_search_evidence_v1.json"
            ).read_text(encoding="utf-8")
        )
        stored_visual = json.loads(
            (
                ASSET_ROOT
                / "research_evidence_moe_elements"
                / "moe_meaning_contracts_v2.json"
            ).read_text(encoding="utf-8")
        )
        stored_grammar = json.loads(
            (ASSET_ROOT / "illustration_moe_grammar_v4.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(evidence, stored_evidence)
        self.assertEqual(visual, stored_visual)
        self.assertEqual(compile_grammar_v4(ASSET_ROOT), stored_grammar)
        self.assertEqual(GRAMMAR_SCHEMA_V4, stored_grammar["schema"])
        self.assertEqual(
            hashlib.sha256(
                (ASSET_ROOT / "illustration_moe_grammar_v3.json").read_bytes()
            ).hexdigest(),
            stored_grammar["base_grammar_v3_sha256"],
        )
        self.assertEqual(29, visual["contract_count"])
        self.assertEqual(29, evidence["record_count"])
        self.assertEqual(52, sum(len(row["visual_variants"]) for row in visual["contracts"]))
        self.assertEqual(124, len(self.grammar.visual_contracts.alias_bindings))
        relation_counts: dict[str, int] = {}
        for binding in self.grammar.visual_contracts.alias_bindings.values():
            relation = binding["relation"]
            relation_counts[relation] = relation_counts.get(relation, 0) + 1
        self.assertEqual(
            {"exact": 98, "variant": 6, "carrier": 14, "related": 6},
            relation_counts,
        )
        for record in evidence["records"]:
            self.assertTrue(record["queries"])
            self.assertGreaterEqual(len(record["recurring_features_en"]), 2)
            self.assertTrue(
                all(
                    url.startswith("https://")
                    for url in record["representative_source_urls"]
                )
            )

    def test_all_29_canonical_elements_emit_and_audit_visual_evidence(self) -> None:
        for element_id in self.legacy.records_by_id:
            with self.subTest(element_id=element_id):
                pack, composed = self._build([element_id])
                self.assertEqual(PACK_SCHEMA_V6, pack["contract_version"])
                self.assertEqual(COMPOSED_SCHEMA_V4, composed["schema"])
                self.assertEqual(
                    "canonical", pack["moe_intent"][0]["alias_relation"]
                )
                self.assertEqual(1, len(composed["visual_evidence"]))
                audit = audit_moe_candidate_pack(
                    pack,
                    composed,
                    legacy_assets=self.legacy,
                    grammar_assets=self.grammar,
                )
                self.assertEqual(PACK_AUDIT_SCHEMA_V4, audit["schema"])
                self.assertEqual("pass", audit["status"], audit["failures"])

    def test_v4_qualification_covers_all_canonical_and_alias_contracts(self) -> None:
        stored = json.loads(
            (
                ASSET_ROOT
                / "research_evidence_moe_elements"
                / "qualification_v4.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(build_qualification(ASSET_ROOT), stored)
        self.assertEqual("pass", stored["status"])
        self.assertEqual(29, stored["canonical_case_count"])
        self.assertEqual(124, stored["alias_case_count"])
        self.assertEqual(118, stored["activating_alias_count"])
        self.assertEqual(6, stored["related_alias_rejection_count"])
        self.assertEqual(153, stored["pass_count"])

    def test_alias_relations_activate_or_reject_without_silent_substitution(
        self,
    ) -> None:
        for binding in self.grammar.visual_contracts.alias_bindings.values():
            alias = binding["alias"]
            with self.subTest(alias=alias, relation=binding["relation"]):
                if binding["relation"] == "related":
                    with self.assertRaisesRegex(MoeElementError, "related-only"):
                        self._build([alias])
                    continue
                pack, composed = self._build([alias])
                self.assertEqual(
                    binding["relation"], pack["moe_intent"][0]["alias_relation"]
                )
                self.assertEqual(
                    binding["element_id"],
                    pack["request_contract"]["selected_element_ids"][0],
                )
                if binding["relation"] == "variant":
                    self.assertEqual(
                        binding["variant_id"],
                        pack["moe_intent"][0]["selected_visual_variant_id"],
                    )
                audit = audit_moe_candidate_pack(
                    pack,
                    composed,
                    legacy_assets=self.legacy,
                    grammar_assets=self.grammar,
                )
                self.assertEqual("pass", audit["status"], audit["failures"])

    def test_variant_alias_forces_one_lineage_without_cross_variant_mixing(self) -> None:
        pack, composed = self._build(["body-swap transformation"])
        candidate = pack["moe_grammar"]["selected_candidates"][0]
        binding = pack["moe_grammar"]["visual_bindings"][0]
        variant = binding["selected_variant"]
        self.assertEqual("reciprocal_body_swap", candidate["visual_variant_id"])
        self.assertIn(candidate["subtype_id"], variant["candidate_subtype_ids"])
        for phrase in variant["all_of_en"]:
            self.assertIn(phrase, composed["prompt_en"])
        other_variants = [
            row
            for row in binding["contract"]["visual_variants"]
            if row["id"] != variant["id"]
        ]
        for other in other_variants:
            self.assertFalse(
                all(phrase in composed["prompt_en"] for phrase in other["all_of_en"])
            )

    def test_sensitive_label_is_omitted_while_visual_geometry_stays_exact(self) -> None:
        pack, composed = self._build(["moe_ahegao_expression"])
        meaning = pack["moe_grammar"]["meaning_bindings"][0]["contract"]
        variant = pack["moe_grammar"]["visual_bindings"][0]["selected_variant"]
        for label in meaning["runtime_forbidden_labels"]:
            self.assertFalse(runtime_label_present(label, composed["prompt_en"]))
        for field in (
            "all_of_en",
            "topology_edges_en",
            "camera_requirements_en",
        ):
            for phrase in variant[field]:
                self.assertIn(phrase, composed["prompt_en"])
        self.assertIn("tongue", composed["prompt_en"].casefold())
        audit = audit_moe_candidate_pack(
            pack,
            composed,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("pass", audit["status"], audit["failures"])

    def test_six_multi_element_cases_share_visual_mode_and_sparse_budget(self) -> None:
        for row in self.corpus["sections"]["cross_element_combinations"]:
            with self.subTest(case=row["id"]):
                pack, composed = self._build(
                    row["expected_element_ids"],
                    request=row["request_ko"],
                )
                nodes = pack["moe_grammar"]["selected_nodes"]
                self.assertEqual(
                    len(row["expected_element_ids"]),
                    len(pack["moe_grammar"]["visual_bindings"]),
                )
                self.assertEqual(
                    1, sum(node["selected_role"] == "primary" for node in nodes)
                )
                self.assertLessEqual(len(nodes), 3)
                audit = audit_moe_candidate_pack(
                    pack,
                    composed,
                    legacy_assets=self.legacy,
                    grammar_assets=self.grammar,
                )
                self.assertEqual("pass", audit["status"], audit["failures"])

    def test_negative_confound_is_pixel_review_not_a_lexical_ban(self) -> None:
        pack, composed = self._build(["moe_mesugaki_provocation"])
        self.assertIn("rather than a generic smug face", composed["prompt_en"])
        self.assertIn(
            "generic smug face",
            composed["visual_evidence"][0]["negative_visual_confounds_en"],
        )
        audit = audit_moe_candidate_pack(
            pack,
            composed,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("pass", audit["status"], audit["failures"])

    def test_visual_phrase_contract_and_medium_mutations_fail_closed(self) -> None:
        pack, composed = self._build(["moe_tsf_transformation"])
        variant = pack["moe_grammar"]["visual_bindings"][0]["selected_variant"]
        missing = copy.deepcopy(composed)
        required_phrase = variant["topology_edges_en"][0]
        missing["prompt_en"] = missing["prompt_en"].replace(
            required_phrase, "generic transformation framing"
        )
        audit = audit_moe_candidate_pack(
            pack,
            missing,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertIn(
            "visual_requirement", {failure["check"] for failure in audit["failures"]}
        )

        with self.assertRaisesRegex(MoeElementError, "cannot carry"):
            self._build(
                ["moe_darkening_corruption"],
                output_mode="single_frame",
            )

        forged = copy.deepcopy(pack)
        forged["semantic_contract"]["image_search_evidence_sha256"] = "0" * 64
        self._rehash_pack(forged)
        forged_composed = compose_moe_prompt_draft(forged, self.foundation)
        audit = audit_moe_candidate_pack(
            forged,
            forged_composed,
            legacy_assets=self.legacy,
            grammar_assets=self.grammar,
        )
        self.assertEqual("fail", audit["status"])
        self.assertIn(
            "visual_meaning_bindings",
            {failure["check"] for failure in audit["failures"]},
        )


if __name__ == "__main__":
    unittest.main()
