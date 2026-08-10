"""Focused executable contract tests for the sibling illustration skill.

These tests intentionally exercise only the public runtime/audit surface and the
frozen holdout.  They do not treat prompt-audit PASS as rendered-image proof.
"""

from __future__ import annotations

import copy
from dataclasses import replace
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "subculture-illustration-image-generator"
SCRIPT_ROOT = SKILL_ROOT / "scripts"
ASSET_ROOT = SKILL_ROOT / "assets"
sys.path.insert(0, str(SCRIPT_ROOT))

import illustration_audit as illustration_audit_module  # noqa: E402
from illustration_audit import (  # noqa: E402
    audit_composed_prompt,
    computed_pack_id,
)
from illustration_runtime import (  # noqa: E402
    CONTRACT_VERSION,
    LEGACY_CONTRACT_VERSION,
    SECOND_LOOK_CARRIER_KINDS,
    SECOND_LOOK_RISK_FLAGS,
    ResolutionError,
    build_candidate_pack,
    canonical_json_bytes,
    load_runtime_assets,
    resolve_request,
    validate_assets,
)
from validate_illustration_assets import (  # noqa: E402
    ValidationFailure,
    validate_all,
    validate_generation_retry_policy,
    validate_legacy_prompt_qualification,
    validate_prompt_qualification,
    validate_render_qualification,
    validate_render_v2_preflight,
    validate_render_v2_qualification,
    validate_render_v3_preflight,
    validate_render_v3_qualification,
)


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _evidence_phrase(field: str, prefix: str) -> str:
    readable = field.replace("_", " ")
    return f"{prefix} makes {readable} visible at the broken rescue gantry"


def _valid_composed(pack: dict[str, object]) -> dict[str, object]:
    """Build one literal, non-creative audit fixture from a compact pack."""

    grammar = pack["visual_grammar"]
    profile = pack["format_profile"]
    composition = pack["composition_contract"]
    assert isinstance(grammar, dict)
    assert isinstance(profile, dict)
    assert isinstance(composition, dict)

    visual_evidence = {
        field: _evidence_phrase(field, "A concrete scene cue")
        for field in grammar["required_evidence_types"]
    }
    authorial_grammar = {
        "focal_hierarchy_phrase": "A hard diagonal focal hierarchy isolates the exchanged rescue tool",
        "controlled_omission_phrase": "Quiet unmarked wall planes omit every unrelated secondary incident",
        "edge_or_mark_rule_phrase": "Taut ink edges sharpen only around the active hands and tool",
        "repeated_material_or_motif_rule_phrase": "Three matching repair stitches repeat from glove to harness to cable",
    }
    viewer_evidence = {
        "first_glance_hook_phrase": "First, the bright exchanged wrench anchors the eye between both partners",
        "second_look_reveal_phrase": "Second, their crossed safety lines reveal a restrained command dispute",
        "affect_actor_phrase": "The kneeling rescuer extends one gloved hand",
        "affect_action_phrase": "The open palm transfers the cracked wrench",
        "affect_target_phrase": "The standing partner braces the receiving wrist",
        "affect_consequence_phrase": "The shared cable pulls taut toward the unstable beam",
    }
    # General required_evidence_types includes post-render lifecycle gates.
    # Only the typed composition fields may be claimed before pixels exist.
    required_format_fields = [
        str(value) for value in profile.get("required_format_evidence_fields", [])
    ]
    format_evidence = {
        field: _evidence_phrase(field, "The typed format design")
        for field in dict.fromkeys(required_format_fields)
    }

    phrases = [
        *visual_evidence.values(),
        *authorial_grammar.values(),
        *viewer_evidence.values(),
        *format_evidence.values(),
    ]
    composed: dict[str, object] = {
        "pack_id": pack["pack_id"],
        "prompt_en": "",
        "negative_en": pack["negative_en"],
        "chosen_candidate_ids": list(composition["required_chosen_candidate_ids"]),
        "composer": "agent",
        "visual_evidence": visual_evidence,
        "authorial_grammar": authorial_grammar,
        "viewer_evidence": viewer_evidence,
        "format_evidence": format_evidence,
        "reference_boundary": {
            "original_design": True,
            "named_style_references": [],
            "protected_ip_references": [],
        },
    }
    if pack.get("contract_version") == CONTRACT_VERSION:
        primary = {
            "carrier_kind": "object_relation",
            "carrier_phrase": "one broad cracked-wrench silhouette",
            "protected_locus_phrase": "the clear center gap between both adults",
            "consequence_phrase": "The repaired wrench aligns with the taut rescue cable",
            "risk_flags": [],
        }
        fallback = {
            "carrier_kind": "environmental_trace",
            "carrier_phrase": "one wide dust-free cable arc",
            "protected_locus_phrase": "the bare floor strip beneath the unstable beam",
            "consequence_phrase": "The clean cable path terminates at the repaired anchor",
            "risk_flags": [],
        }
        plan_contract = pack["viewer_contract"]["second_look_plan_contract"]
        composed["schema"] = composition["composed_schema"]
        composed["second_look_plan"] = {
            "schema": plan_contract["schema"],
            "selected_proposal_id": None,
            "reveal_phrase": viewer_evidence["second_look_reveal_phrase"],
            "review_scale_ids": [plan_contract["allowed_review_scale_ids"][0]],
            "primary_carrier": primary,
            "fallback_carrier": fallback,
        }
        phrases.extend(
            value
            for carrier in (primary, fallback)
            for key, value in carrier.items()
            if key in {"carrier_phrase", "protected_locus_phrase", "consequence_phrase"}
        )
    composed["prompt_en"] = ". ".join(phrases) + "."
    return composed


def _rehash_pack(pack: dict[str, object]) -> None:
    pack["pack_id"] = computed_pack_id(pack)


class SubcultureIllustrationContractV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.assets = load_runtime_assets(ASSET_ROOT)
        cls.holdout = _jsonl(ASSET_ROOT / "illustration_prompt_holdout_v1.jsonl")
        cls.audit_pack = build_candidate_pack(
            "Adult rescue partners exchange a tool.",
            topic="ensemble_relationship_staging",
            format_id="ensemble_key_art",
            seed=42,
            creativity=0.0,
            assets=cls.assets,
        )
        cls.valid_composed = _valid_composed(cls.audit_pack)

    def assert_composed_failure(
        self,
        composed: dict[str, object],
        expected_check: str,
        *,
        pack: dict[str, object] | None = None,
    ) -> dict[str, object]:
        result = audit_composed_prompt(pack or self.audit_pack, composed)
        self.assertEqual("fail", result["status"], result)
        self.assertEqual([], result["integrity_errors"], result)
        self.assertIn(expected_check, {item["check"] for item in result["failures"]}, result)
        return result

    def test_asset_validator_passes_with_frozen_counts(self) -> None:
        result = validate_assets(ASSET_ROOT)
        self.assertEqual("pass", result["status"])
        self.assertEqual(24, result["route_count"])
        self.assertEqual(6, result["format_family_count"])
        self.assertEqual(10, result["format_variant_count"])
        self.assertEqual(264, result["runtime_node_count"])
        self.assertEqual(48, result["bundle_count"])
        self.assertEqual(
            {"guard": 27, "router": 28, "visual_atom": 209},
            result["role_counts"],
        )

    def test_generation_retry_policy_includes_three_unchanged_refusal_retries(self) -> None:
        result = validate_generation_retry_policy(ASSET_ROOT)
        self.assertEqual("pass", result["status"])
        self.assertEqual(3, result["max_unchanged_retries_after_initial"])
        self.assertEqual(4, result["max_calls_per_phase"])
        self.assertTrue(result["includes_safety_refusal"])
        self.assertTrue(result["includes_policy_refusal"])

    def test_generation_retry_policy_mutations_fail_closed(self) -> None:
        source = ASSET_ROOT / "image_generation_retry_policy_v1.json"
        policy = json.loads(source.read_text(encoding="utf-8"))
        mutations = (
            ("retry count", "exactly three", "max_unchanged_retries_after_initial", 2),
            ("policy refusal", "outcomes mismatch", "retryable_no_image_outcomes", [
                value for value in policy["retryable_no_image_outcomes"] if value != "policy_refusal"
            ]),
            ("prompt rewrite", "no_prompt_rewrite", "no_prompt_rewrite_between_retries", False),
        )
        for label, expected, field, value in mutations:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as temp_dir:
                copied = copy.deepcopy(policy)
                copied[field] = value
                target = Path(temp_dir) / source.name
                target.write_text(json.dumps(copied), encoding="utf-8")
                with self.assertRaisesRegex(ValidationFailure, expected):
                    validate_generation_retry_policy(target.parent)

    def test_audit_binding_uses_the_skill_specific_core(self) -> None:
        self.assertEqual(
            (SCRIPT_ROOT / "illustration_audit.py").resolve(),
            Path(illustration_audit_module.__file__).resolve(),
        )

    def test_all_24_frozen_requests_resolve_exact_route_variant_and_sparse_edge(self) -> None:
        self.assertEqual(24, len(self.holdout))
        seen_topics: set[str] = set()
        for case in self.holdout:
            with self.subTest(case_id=case["case_id"]):
                pack = build_candidate_pack(
                    str(case["request_ko"]),
                    seed=int(case["seed"]),
                    assets=self.assets,
                )
                request = pack["request_contract"]
                profile = pack["format_profile"]
                grammar = pack["visual_grammar"]
                self.assertEqual(case["topic_id"], request["route_id"])
                self.assertEqual(case["expected_format"], profile["variant_id"])
                seen_topics.add(str(request["route_id"]))

                nodes = grammar["runtime_nodes"]
                primary = [node for node in nodes if node["selected_role"] == "primary"]
                supports = [node for node in nodes if node["selected_role"] == "support"]
                self.assertEqual(1, len(primary))
                self.assertLessEqual(len(supports), 2)
                self.assertTrue(all(node["node_type"] == "visual_atom" for node in nodes))
                self.assertTrue(
                    all(profile["family_id"] in node["format_family_ids"] for node in nodes)
                )

                edge = grammar["selected_edge"]
                self.assertIn(edge["id"], grammar["compatible_edge_ids"])
                self.assertEqual(grammar["primary_runtime_id"], edge["primary_node_id"])
                self.assertCountEqual(grammar["support_runtime_ids"], edge["support_node_ids"])
                self.assertIn(profile["family_id"], edge["format_family_ids"])
        self.assertEqual(set(self.assets.routes_by_id), seen_topics)

    def test_same_input_is_canonically_deterministic(self) -> None:
        case = self.holdout[4]
        kwargs = {
            "seed": int(case["seed"]),
            "assets": self.assets,
        }
        first = build_candidate_pack(str(case["request_ko"]), **kwargs)
        second = build_candidate_pack(str(case["request_ko"]), **kwargs)
        self.assertEqual(first["pack_id"], second["pack_id"])
        self.assertEqual(canonical_json_bytes(first), canonical_json_bytes(second))

    def test_default_pack_uses_balanced_creativity_without_high_creative_development(self) -> None:
        pack = build_candidate_pack(
            "성인 수선사가 망가진 기상 장치를 복구하는 일러스트를 만들어줘.",
            topic="single_frame_narrative_compression",
            format_id="single_illustration",
            seed=77,
            assets=self.assets,
        )
        contract = pack["authorial_contract"]
        self.assertEqual(0.5, pack["request_contract"]["creativity"])
        self.assertFalse(contract["creative_development_required"])
        self.assertFalse(contract["familiar_anchor_required"])
        self.assertFalse(contract["one_changed_rule_required"])
        self.assertTrue(contract["first_second_look_required"])
        self.assertEqual(0, contract["proposal_count_required"])

    def test_explicit_creative_intent_keeps_high_creative_development(self) -> None:
        pack = build_candidate_pack(
            "성인 수선사가 망가진 기상 장치를 복구하는 작가적 일러스트를 만들어줘.",
            topic="single_frame_narrative_compression",
            format_id="single_illustration",
            seed=77,
            creativity=0.5,
            assets=self.assets,
        )
        contract = pack["authorial_contract"]
        self.assertEqual(0.5, pack["request_contract"]["creativity"])
        self.assertTrue(contract["creative_development_required"])
        self.assertTrue(contract["familiar_anchor_required"])
        self.assertTrue(contract["one_changed_rule_required"])
        self.assertTrue(contract["first_second_look_required"])
        self.assertEqual(4, contract["proposal_count_required"])

    def test_generic_request_uses_only_family_default(self) -> None:
        for concept in (
            "오리지널 애니메이션 일러스트를 만들어줘",
            "anime illustration of an adult mechanic",
            "studio portrait photograph of a mechanic",
        ):
            with self.subTest(concept=concept):
                resolved = resolve_request(concept, assets=self.assets)
                self.assertEqual("format_default", resolved.route_source)
                self.assertEqual("fallback", resolved.format_source)
                self.assertEqual("single_frame_narrative_compression", resolved.route["route_id"])
                self.assertEqual("single_illustration", resolved.variant["id"])
                self.assertEqual((), resolved.matched_rule_ids)

    def test_constructed_equal_priority_route_collision_fails_closed(self) -> None:
        copied_routes = copy.deepcopy(dict(self.assets.routes_by_id))
        collision_rule = {
            "id": "test::deliberate_collision",
            "locale": "en",
            "match": "exact_phrase",
            "priority": 9999,
            "phrases": ["deliberate collision trigger"],
        }
        route_ids = list(copied_routes)[:2]
        for route_id in route_ids:
            copied_routes[route_id]["routing_rules"] = [copy.deepcopy(collision_rule)]
        collided_assets = replace(self.assets, routes_by_id=copied_routes)
        with self.assertRaisesRegex(ResolutionError, "ambiguous topic rules"):
            resolve_request(
                "deliberate collision trigger",
                format_id="single_illustration",
                assets=collided_assets,
            )

    def test_one_valid_literal_composed_fixture_passes(self) -> None:
        result = audit_composed_prompt(self.audit_pack, self.valid_composed)
        self.assertEqual("pass", result["status"], result)
        self.assertEqual([], result["integrity_errors"])
        self.assertEqual([], result["failures"])

    def test_v2_pack_exposes_closed_second_look_contract(self) -> None:
        self.assertEqual(CONTRACT_VERSION, self.audit_pack["contract_version"])
        composition = self.audit_pack["composition_contract"]
        self.assertEqual(
            "subculture-illustration-composed-prompt/v2",
            composition["composed_schema"],
        )
        contract = self.audit_pack["viewer_contract"]["second_look_plan_contract"]
        self.assertEqual("illustration-second-look-plan/v1", contract["schema"])
        self.assertEqual(
            list(SECOND_LOOK_CARRIER_KINDS),
            contract["carrier_kinds"],
        )
        self.assertEqual(list(SECOND_LOOK_RISK_FLAGS), contract["risk_flags"])
        self.assertEqual(contract["risk_flags"], contract["forbidden_as_sole"])
        self.assertTrue(contract["fallback_must_reference_selected_consequence"])
        self.assertEqual(
            self.audit_pack["format_profile"]["scale_contract"]["inspection_scales"],
            contract["allowed_review_scale_ids"],
        )

    def test_legacy_pack_and_composed_contract_remain_supported(self) -> None:
        legacy_pack = build_candidate_pack(
            "Adult rescue partners exchange a tool.",
            topic="ensemble_relationship_staging",
            format_id="ensemble_key_art",
            seed=42,
            creativity=0.0,
            contract_version=LEGACY_CONTRACT_VERSION,
            assets=self.assets,
        )
        self.assertEqual(LEGACY_CONTRACT_VERSION, legacy_pack["contract_version"])
        self.assertNotIn("composed_schema", legacy_pack["composition_contract"])
        self.assertNotIn(
            "second_look_plan_contract",
            legacy_pack["viewer_contract"],
        )
        composed = _valid_composed(legacy_pack)
        self.assertNotIn("schema", composed)
        self.assertNotIn("second_look_plan", composed)
        result = audit_composed_prompt(legacy_pack, composed)
        self.assertEqual("pass", result["status"], result)

    def test_v1_and_v2_prompt_qualification_are_separate_and_valid(self) -> None:
        legacy = validate_legacy_prompt_qualification(ASSET_ROOT, self.assets)
        current = validate_prompt_qualification(ASSET_ROOT, self.assets)
        self.assertEqual("subculture-illustration-prompt-qualification/v1", legacy["schema"])
        self.assertEqual("subculture-illustration-prompt-qualification/v2", current["schema"])
        self.assertEqual(24, legacy["case_count"])
        self.assertEqual(24, current["case_count"])

    def test_case01_v2_preflight_is_clean_frozen_and_generation_free(self) -> None:
        summary = validate_render_v2_preflight(ASSET_ROOT, self.assets)
        self.assertEqual("historical_preflight_valid", summary["status"])
        self.assertEqual("ready_awaiting_user_approval", summary["recorded_status"])
        self.assertEqual("illustration_render_01_single_narrative", summary["case_id"])
        self.assertEqual("db15b9138a402405", summary["pack_id"])
        self.assertEqual("primary_carrier", summary["initial_attempted_role"])
        self.assertEqual("fallback_carrier", summary["repair_attempted_role"])
        self.assertFalse(summary["image_generated"])
        self.assertFalse(summary["historical_local_artifacts_verified"])

    def test_case01_v2_preflight_mutations_fail_closed(self) -> None:
        mutations = (
            (
                "premature approval",
                lambda value, directory: value.__setitem__(
                    "authorization_recorded_for_generation", True
                ),
                "await separate user authority",
            ),
            (
                "repeated primary repair",
                lambda value, directory: value["second_look_execution"][
                    "future_bounded_repair_if_needed"
                ].__setitem__("attempted_role", "primary_carrier"),
                "fallback repair contract mismatch",
            ),
            (
                "unexpected generated image",
                lambda value, directory: (directory / "unauthorized.png").write_bytes(
                    b"generation must not exist in a preflight"
                ),
                "must not contain generated images",
            ),
        )
        for label, mutate, expected in mutations:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as temp_dir:
                copied_assets = Path(temp_dir) / "assets"
                shutil.copytree(ASSET_ROOT, copied_assets)
                preflight_dir = copied_assets / "render_case01_v2_preflight"
                preflight_path = preflight_dir / "preflight.json"
                preflight = json.loads(preflight_path.read_text(encoding="utf-8"))
                mutate(preflight, preflight_dir)
                preflight_path.write_text(
                    json.dumps(preflight, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValidationFailure, expected):
                    validate_render_v2_preflight(copied_assets, self.assets)

    def test_aggregate_validator_does_not_hide_partial_pixel_qualification(self) -> None:
        summary = validate_all(ASSET_ROOT)
        self.assertEqual("pass", summary["status"])
        self.assertEqual("pass", summary["product_qualification_status"])
        self.assertEqual("partial", summary["render_qualification"]["qualification_status"])
        self.assertEqual("partial", summary["render_v2_qualification"]["qualification_status"])
        self.assertEqual("pass", summary["render_v3_qualification"]["qualification_status"])

    def test_case01_v2_successor_preserves_both_failed_roles(self) -> None:
        summary = validate_render_v2_qualification(ASSET_ROOT, self.assets)
        self.assertEqual("partial", summary["qualification_status"])
        self.assertEqual(2, summary["attempt_count"])
        self.assertEqual(1, summary["repair_count"])
        self.assertIsNone(summary["qualified_role"])
        self.assertEqual(5, summary["passed_case_count"])
        self.assertEqual(1, summary["failed_case_count"])
        self.assertFalse(summary["full_suite_executed"])
        self.assertFalse(summary["local_artifacts_verified"])

    def test_case01_v2_successor_cannot_promote_a_failed_carrier(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            copied_assets = Path(temp_dir) / "assets"
            shutil.copytree(ASSET_ROOT, copied_assets)
            review_path = copied_assets / "render_case01_v2_visual_review.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review["second_look_pixel_review"]["qualified_role"] = "fallback_carrier"
            review["second_look_pixel_review"]["qualification_status"] = "pass"
            review_path.write_text(
                json.dumps(review, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValidationFailure, "second-look summary mismatch"
            ):
                validate_render_v2_qualification(copied_assets, self.assets)

    def test_case01_v3_preflight_records_distinct_authorized_carriers(self) -> None:
        summary = validate_render_v3_preflight(ASSET_ROOT, self.assets)
        self.assertEqual("authorized_preflight_valid", summary["status"])
        self.assertEqual("authorized_ready_for_generation", summary["recorded_status"])
        self.assertEqual("db15b9138a402405", summary["pack_id"])
        self.assertEqual("primary_carrier", summary["initial_attempted_role"])
        self.assertEqual("fallback_carrier", summary["repair_attempted_role"])
        self.assertFalse(summary["image_generated_in_preflight"])

    def test_case01_v3_primary_pass_preserves_prior_failures(self) -> None:
        summary = validate_render_v3_qualification(ASSET_ROOT, self.assets)
        self.assertEqual("pass", summary["qualification_status"])
        self.assertEqual(1, summary["attempt_count"])
        self.assertEqual(0, summary["repair_count"])
        self.assertEqual("primary_carrier", summary["qualified_role"])
        self.assertEqual(6, summary["passed_case_count"])
        self.assertEqual(0, summary["failed_case_count"])
        self.assertTrue(summary["full_suite_executed"])

        preserved = validate_render_v2_qualification(ASSET_ROOT, self.assets)
        self.assertEqual("partial", preserved["qualification_status"])
        self.assertIsNone(preserved["qualified_role"])

    def test_case01_v3_primary_hash_or_role_mutations_fail_closed(self) -> None:
        mutations = (
            (
                "fallback promoted without attempt",
                lambda review: review["second_look_pixel_review"].__setitem__(
                    "qualified_role", "fallback_carrier"
                ),
                "second-look summary mismatch",
            ),
            (
                "final image hash changed",
                lambda review: review["final_image"].__setitem__("sha256", "0" * 64),
                "byte-identical passing primary image",
            ),
        )
        for label, mutate, expected in mutations:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as temp_dir:
                copied_assets = Path(temp_dir) / "assets"
                shutil.copytree(ASSET_ROOT, copied_assets)
                review_path = copied_assets / "render_case01_v3_visual_review.json"
                review = json.loads(review_path.read_text(encoding="utf-8"))
                mutate(review)
                review_path.write_text(
                    json.dumps(review, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(ValidationFailure, expected):
                    validate_render_v3_qualification(copied_assets, self.assets)

    def test_second_look_plan_mutations_fail_closed(self) -> None:
        cases: list[tuple[str, str, dict[str, object]]] = []

        missing = copy.deepcopy(self.valid_composed)
        del missing["second_look_plan"]
        cases.append(("missing plan", "second_look_plan", missing))

        duplicate_scale = copy.deepcopy(self.valid_composed)
        scale = duplicate_scale["second_look_plan"]["review_scale_ids"][0]
        duplicate_scale["second_look_plan"]["review_scale_ids"].append(scale)
        cases.append(("duplicate scale", "second_look_review_scales", duplicate_scale))

        unknown_scale = copy.deepcopy(self.valid_composed)
        unknown_scale["second_look_plan"]["review_scale_ids"] = ["invented_scale"]
        cases.append(("unknown scale", "second_look_review_scales", unknown_scale))

        duplicate_locus = copy.deepcopy(self.valid_composed)
        duplicate_locus["second_look_plan"]["fallback_carrier"][
            "protected_locus_phrase"
        ] = duplicate_locus["second_look_plan"]["primary_carrier"][
            "protected_locus_phrase"
        ]
        cases.append(("duplicate locus", "second_look_distinctness", duplicate_locus))

        fallback_risk = copy.deepcopy(self.valid_composed)
        fallback_risk["second_look_plan"]["fallback_carrier"]["risk_flags"] = [
            "subscale_symbol_decode"
        ]
        cases.append(("risky fallback", "second_look_fallback", fallback_risk))

        for label, expected_check, composed in cases:
            with self.subTest(case=label):
                self.assert_composed_failure(composed, expected_check)

    def test_risky_primary_requires_a_different_safe_fallback_kind(self) -> None:
        composed = copy.deepcopy(self.valid_composed)
        primary = composed["second_look_plan"]["primary_carrier"]
        fallback = composed["second_look_plan"]["fallback_carrier"]
        primary["carrier_kind"] = "projected_form"
        primary["carrier_phrase"] = "two overlapping hand shadows"
        primary["consequence_phrase"] = "Two overlapping hand shadows merge above the tool"
        primary["risk_flags"] = [
            "compound_anatomy",
            "overlapping_multi_limb_projection",
        ]
        composed["prompt_en"] += (
            " two overlapping hand shadows."
            " Two overlapping hand shadows merge above the tool."
        )
        result = audit_composed_prompt(self.audit_pack, composed)
        self.assertEqual("pass", result["status"], result)

        fallback["carrier_kind"] = "projected_form"
        self.assert_composed_failure(composed, "second_look_fallback")

    def test_linked_risk_backstop_is_narrow_and_fail_closed(self) -> None:
        underdeclared = copy.deepcopy(self.valid_composed)
        primary = underdeclared["second_look_plan"]["primary_carrier"]
        primary["carrier_phrase"] = "two overlapping hand shadows"
        primary["consequence_phrase"] = "Two overlapping hand shadows merge above the tool"
        underdeclared["prompt_en"] += (
            " two overlapping hand shadows."
            " Two overlapping hand shadows merge above the tool."
        )
        self.assert_composed_failure(underdeclared, "second_look_risk_backstop")

        unrelated = copy.deepcopy(self.valid_composed)
        unrelated["prompt_en"] += (
            " In the ordinary first-read action, two hands overlap briefly during the exchange."
        )
        result = audit_composed_prompt(self.audit_pack, unrelated)
        self.assertEqual("pass", result["status"], result)

    def test_high_creativity_plan_binds_selected_proposal_exactly(self) -> None:
        record = _jsonl(
            ASSET_ROOT / "prompt_qualification_v2" / "cases_01_04.jsonl"
        )[0]
        pack = record["candidate_pack"]
        valid = record["composed"]
        self.assertEqual("pass", audit_composed_prompt(pack, valid)["status"])

        wrong_proposal = copy.deepcopy(valid)
        wrong_proposal["second_look_plan"]["selected_proposal_id"] = "proposal_01_rejected"
        self.assert_composed_failure(
            wrong_proposal,
            "second_look_proposal_binding",
            pack=pack,
        )

        invented_consequence = copy.deepcopy(valid)
        replacement = "An invented consequence appears only to test exact proposal binding"
        invented_consequence["second_look_plan"]["fallback_carrier"][
            "consequence_phrase"
        ] = replacement
        invented_consequence["prompt_en"] += f". {replacement}."
        self.assert_composed_failure(
            invented_consequence,
            "second_look_proposal_binding",
            pack=pack,
        )

        self.assertTrue(
            any("cannot prove rendered pixel salience" in item for item in record["audit"]["limits"])
        )

    def test_post_render_pixel_review_is_not_a_pre_render_format_phrase(self) -> None:
        profile = self.audit_pack["format_profile"]
        self.assertIn("rendered_pixel_review", profile["required_evidence_types"])
        self.assertNotIn(
            "rendered_pixel_review",
            profile["required_format_evidence_fields"],
        )
        self.assertNotIn("rendered_pixel_review", self.valid_composed["format_evidence"])
        result = audit_composed_prompt(self.audit_pack, self.valid_composed)
        self.assertEqual("pass", result["status"], result)

    def test_pack_cannot_require_pixel_review_as_a_composed_format_field(self) -> None:
        mutated_pack = copy.deepcopy(self.audit_pack)
        mutated_pack["format_profile"]["required_format_evidence_fields"].append(
            "rendered_pixel_review"
        )
        _rehash_pack(mutated_pack)
        composed = copy.deepcopy(self.valid_composed)
        composed["pack_id"] = mutated_pack["pack_id"]
        result = audit_composed_prompt(mutated_pack, composed)
        self.assertEqual("error", result["status"], result)
        format_errors = [
            item for item in result["integrity_errors"] if item["check"] == "format_contract"
        ]
        self.assertTrue(
            any("rendered_pixel_review" in item.get("fields", []) for item in format_errors),
            result,
        )

    def test_named_style_guard_distinguishes_subject_from_creator_reference(self) -> None:
        generic_subject = copy.deepcopy(self.valid_composed)
        generic_subject["prompt_en"] += " Original illustration of an adult artifact restorer."
        generic_result = audit_composed_prompt(self.audit_pack, generic_subject)
        self.assertFalse(
            any(item["check"] == "named_style_reference" for item in generic_result["failures"]),
            generic_result,
        )

        named_creator = copy.deepcopy(self.valid_composed)
        named_creator["prompt_en"] += " Borrow the art of Hayao Miyazaki."
        self.assert_composed_failure(named_creator, "named_style_reference")

    def test_render_review_closes_frozen_views_without_hiding_the_failed_case(self) -> None:
        summary = validate_render_qualification(ASSET_ROOT, self.assets)
        self.assertEqual("partial", summary["qualification_status"])
        self.assertEqual(6, summary["case_count"])
        self.assertEqual(5, summary["passed_case_count"])
        self.assertEqual(1, summary["failed_case_count"])
        self.assertFalse(summary["local_artifacts_verified"])

        review = json.loads(
            (ASSET_ROOT / "render_illustration_quality_visual_review_v1.json").read_text(
                encoding="utf-8"
            )
        )
        failed = [case for case in review["cases"] if case["qualification_status"] == "fail_repair_exhausted"]
        self.assertEqual(1, len(failed))
        self.assertIsNone(failed[0]["final_image"])
        self.assertEqual(2, failed[0]["attempt_count"])
        self.assertEqual(1, failed[0]["repair_count"])
        self.assertEqual(
            ["second_look_ev_early_anomaly"],
            [
                item["focus"]
                for item in failed[0]["review_focus_results"]
                if item["outcome"] == "fail"
            ],
        )

    def test_composed_contract_mutations_fail_without_pack_integrity_errors(self) -> None:
        mutations: list[tuple[str, str, object]] = []

        composer = copy.deepcopy(self.valid_composed)
        composer["composer"] = "template"
        mutations.append(("composer", "output_contract", composer))

        negative = copy.deepcopy(self.valid_composed)
        negative["negative_en"] = str(negative["negative_en"]) + ", extra mutation"
        mutations.append(("negative", "negative_en", negative))

        selected_visuals = {
            node["id"] for node in self.audit_pack["visual_grammar"]["runtime_nodes"]
        }
        route = self.assets.routes_by_id["ensemble_relationship_staging"]
        unexposed_id = next(
            node_id for node_id in route["visual_candidate_ids"] if node_id not in selected_visuals
        )
        unexposed = copy.deepcopy(self.valid_composed)
        unexposed["chosen_candidate_ids"].append(f"visual:{unexposed_id}")
        mutations.append(("unexposed visual", "typed_candidate_boundary", unexposed))

        router_id = route["router_candidate_ids"][0]
        router = copy.deepcopy(self.valid_composed)
        router["chosen_candidate_ids"].append(f"visual:{router_id}")
        mutations.append(("router as visual", "typed_candidate_boundary", router))

        nonliteral = copy.deepcopy(self.valid_composed)
        evidence_key = next(iter(nonliteral["visual_evidence"]))
        nonliteral["visual_evidence"][evidence_key] = "This evidence exists only in metadata"
        mutations.append(("nonliteral evidence", "literal_evidence", nonliteral))

        named_style = copy.deepcopy(self.valid_composed)
        named_style["prompt_en"] += " Render it in the style of Studio Ghibli."
        mutations.append(("named style", "named_style_reference", named_style))

        universal = copy.deepcopy(self.valid_composed)
        universal["prompt_en"] += " Red universally means danger."
        mutations.append(("universal inference", "universal_inference", universal))

        aspect_only = copy.deepcopy(self.valid_composed)
        aspect_phrase = "A 16:9 aspect ratio frames the scene"
        aspect_only["format_evidence"] = {"aspect_ratio_phrase": aspect_phrase}
        aspect_only["prompt_en"] += f" {aspect_phrase}."
        mutations.append(("aspect-only format", "aspect_only_format", aspect_only))

        lifecycle_field = copy.deepcopy(self.valid_composed)
        lifecycle_phrase = "A future pixel review remains pending"
        lifecycle_field["format_evidence"]["rendered_pixel_review"] = lifecycle_phrase
        lifecycle_field["prompt_en"] += f" {lifecycle_phrase}."
        mutations.append(("post-render evidence field", "phase_boundary", lifecycle_field))

        completed_review_claim = copy.deepcopy(self.valid_composed)
        completed_review_claim["prompt_en"] += " The final image passed pixel review."
        mutations.append(("completed pixel-review claim", "phase_boundary", completed_review_claim))

        motif_soup = copy.deepcopy(self.valid_composed)
        motif_soup["prompt_en"] += (
            " Random symbols of moons, keys, clocks, and roses form a decorative motif collage."
        )
        mutations.append(("motif soup", "decorative_motif_soup", motif_soup))

        for label, expected_check, composed in mutations:
            with self.subTest(mutation=label):
                self.assert_composed_failure(composed, expected_check)

    def test_format_mismatch_is_a_pack_contract_error(self) -> None:
        mutated_pack = copy.deepcopy(self.audit_pack)
        mutated_pack["format_profile"]["variant_id"] = "single_illustration"
        _rehash_pack(mutated_pack)
        composed = copy.deepcopy(self.valid_composed)
        composed["pack_id"] = mutated_pack["pack_id"]
        result = audit_composed_prompt(mutated_pack, composed)
        self.assertEqual("error", result["status"], result)
        self.assertIn("format_contract", {item["check"] for item in result["integrity_errors"]})

    def test_support_budget_overflow_is_a_pack_contract_error(self) -> None:
        mutated_pack = copy.deepcopy(self.audit_pack)
        grammar = mutated_pack["visual_grammar"]
        selected = {node["id"] for node in grammar["runtime_nodes"]}
        family_id = mutated_pack["format_profile"]["family_id"]
        route = self.assets.routes_by_id["ensemble_relationship_staging"]
        extra_id = next(
            node_id
            for node_id in route["visual_candidate_ids"]
            if node_id not in selected
            and family_id in self.assets.nodes_by_id[node_id]["format_family_ids"]
        )
        asset_node = self.assets.nodes_by_id[extra_id]
        grammar["runtime_nodes"].append(
            {
                "id": extra_id,
                "node_type": "visual_atom",
                "selected_role": "support",
                "definition": asset_node["definition"],
                "observable_evidence_types": [extra_id],
                "format_family_ids": list(asset_node["format_family_ids"]),
            }
        )
        grammar["support_runtime_ids"].append(extra_id)
        grammar["required_evidence_types"].append(extra_id)
        grammar["selected_edge"]["support_node_ids"].append(extra_id)
        grammar["selected_edge"]["required_evidence_types"].append(extra_id)
        mutated_pack["composition_contract"]["required_chosen_candidate_ids"].append(
            f"visual:{extra_id}"
        )
        _rehash_pack(mutated_pack)

        composed = copy.deepcopy(self.valid_composed)
        composed["pack_id"] = mutated_pack["pack_id"]
        composed["chosen_candidate_ids"] = list(
            mutated_pack["composition_contract"]["required_chosen_candidate_ids"]
        )
        phrase = _evidence_phrase(extra_id, "A concrete scene cue")
        composed["visual_evidence"][extra_id] = phrase
        composed["prompt_en"] += f" {phrase}."
        result = audit_composed_prompt(mutated_pack, composed)
        self.assertEqual("error", result["status"], result)
        checks = {item["check"] for item in result["integrity_errors"]}
        self.assertIn("sparse_visual_bundle", checks, result)

    def test_canonical_pack_id_tamper_is_distinguished_from_composed_failure(self) -> None:
        mutated_pack = copy.deepcopy(self.audit_pack)
        mutated_pack["request_contract"]["request_text"] += " tampered"
        result = audit_composed_prompt(mutated_pack, self.valid_composed)
        self.assertEqual("error", result["status"], result)
        self.assertIn("pack_integrity", {item["check"] for item in result["integrity_errors"]})
        self.assertEqual([], result["failures"], result)


if __name__ == "__main__":
    unittest.main()
