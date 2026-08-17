#!/usr/bin/env python3
"""Qualify all v4 visual contracts and typed aliases without rendering images."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from illustration_runtime import build_candidate_pack
from moe_element_runtime import (
    PACK_SCHEMA_V6,
    MoeElementError,
    audit_moe_candidate_pack,
    build_moe_candidate_pack,
    compose_moe_prompt_draft,
    load_moe_element_assets,
    load_moe_grammar_assets,
)
from moe_meaning_contract import runtime_label_present


SCHEMA = "subculture-illustration-moe-visual-qualification/v4"
CREATED_AT = "2026-08-18T00:00:00+09:00"
REQUEST = "성인 캐릭터로 요청한 모에 요소의 시각적 핵심을 정확히 보여줘."
FOUNDATION = "An original adult-character illustration with one causal event"


def _build_case(
    token: str,
    *,
    seed: int,
    legacy: Any,
    grammar: Any,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    base = build_candidate_pack(
        REQUEST,
        seed=seed,
        creativity=0.5,
        contract_version="v2",
    )
    pack = build_moe_candidate_pack(
        base,
        [token],
        preference_text=REQUEST,
        legacy_assets=legacy,
        grammar_assets=grammar,
    )
    composed = compose_moe_prompt_draft(pack, FOUNDATION)
    audit = audit_moe_candidate_pack(
        pack,
        composed,
        legacy_assets=legacy,
        grammar_assets=grammar,
    )
    return pack, composed, audit


def build_qualification(asset_dir: str | Path) -> dict[str, Any]:
    root = Path(asset_dir).expanduser().resolve()
    legacy = load_moe_element_assets(root)
    grammar = load_moe_grammar_assets(
        root,
        legacy_assets=legacy,
        grammar_version="v4",
    )
    if grammar.visual_contracts is None:
        raise MoeElementError("v4 visual contracts are unavailable")

    canonical_results: list[dict[str, Any]] = []
    for ordinal, element_id in enumerate(legacy.records_by_id, 1):
        pack, composed, audit = _build_case(
            element_id,
            seed=9400 + ordinal,
            legacy=legacy,
            grammar=grammar,
        )
        candidate = pack["moe_grammar"]["selected_candidates"][0]
        meaning = pack["moe_grammar"]["meaning_bindings"][0]["contract"]
        visual = pack["moe_grammar"]["visual_bindings"][0]["selected_variant"]
        runtime_labels_absent = not any(
            runtime_label_present(label, composed["prompt_en"])
            for label in meaning["runtime_forbidden_labels"]
        )
        required_phrases = [
            *visual["all_of_en"],
            *visual["any_of"]["alternatives_en"][: visual["any_of"]["minimum"]],
            *visual["topology_edges_en"],
            *visual["camera_requirements_en"],
            *visual["temporal_states_en"],
            *visual["interaction_requirements_en"],
        ]
        phrases_present = all(
            phrase in composed["prompt_en"] for phrase in required_phrases
        )
        status = (
            "pass"
            if pack["contract_version"] == PACK_SCHEMA_V6
            and audit["status"] == "pass"
            and runtime_labels_absent
            and phrases_present
            else "fail"
        )
        canonical_results.append(
            {
                "element_id": element_id,
                "candidate_id": candidate["candidate_id"],
                "candidate_subtype_id": candidate["subtype_id"],
                "visual_variant_id": candidate["visual_variant_id"],
                "resolved_output_mode": pack["moe_grammar"]["frame_contract"][
                    "resolved_output_mode"
                ],
                "required_visual_phrase_count": len(required_phrases),
                "runtime_labels_absent": runtime_labels_absent,
                "prompt_sha256": hashlib.sha256(
                    composed["prompt_en"].encode("utf-8")
                ).hexdigest(),
                "audit_status": audit["status"],
                "status": status,
            }
        )

    alias_results: list[dict[str, Any]] = []
    for index, binding in enumerate(grammar.visual_contracts.alias_bindings.values(), 1):
        alias = binding["alias"]
        relation = binding["relation"]
        if relation == "related":
            rejected = False
            error = ""
            try:
                _build_case(
                    alias,
                    seed=9800 + index,
                    legacy=legacy,
                    grammar=grammar,
                )
            except MoeElementError as exc:
                error = str(exc)
                rejected = "related-only" in error
            alias_results.append(
                {
                    "alias": alias,
                    "element_id": binding["element_id"],
                    "relation": relation,
                    "expected_variant_id": None,
                    "selected_variant_id": None,
                    "audit_status": "not_run",
                    "rejected": rejected,
                    "error_sha256": hashlib.sha256(error.encode("utf-8")).hexdigest(),
                    "status": "pass" if rejected else "fail",
                }
            )
            continue
        pack, _, audit = _build_case(
            alias,
            seed=9800 + index,
            legacy=legacy,
            grammar=grammar,
        )
        selected_variant_id = pack["moe_intent"][0]["selected_visual_variant_id"]
        variant_match = (
            relation != "variant" or selected_variant_id == binding["variant_id"]
        )
        status = (
            "pass"
            if pack["moe_intent"][0]["alias_relation"] == relation
            and pack["request_contract"]["selected_element_ids"]
            == [binding["element_id"]]
            and variant_match
            and audit["status"] == "pass"
            else "fail"
        )
        alias_results.append(
            {
                "alias": alias,
                "element_id": binding["element_id"],
                "relation": relation,
                "expected_variant_id": binding["variant_id"],
                "selected_variant_id": selected_variant_id,
                "audit_status": audit["status"],
                "rejected": False,
                "error_sha256": None,
                "status": status,
            }
        )

    status = (
        "pass"
        if all(row["status"] == "pass" for row in canonical_results)
        and all(row["status"] == "pass" for row in alias_results)
        else "fail"
    )
    return {
        "schema": SCHEMA,
        "created_at": CREATED_AT,
        "scope": (
            "All 29 canonical visual-meaning contracts plus all 124 typed alias "
            "bindings; deterministic prompt preflight only, with no rendered-pixel "
            "or population-preference claim."
        ),
        "grammar_sha256": grammar.grammar_sha256,
        "base_grammar_v3_sha256": grammar.payload["base_grammar_v3_sha256"],
        "meaning_contracts_sha256": grammar.payload["meaning_contracts_sha256"],
        "visual_meaning_contracts_sha256": grammar.payload[
            "visual_meaning_contracts_sha256"
        ],
        "image_search_evidence_sha256": grammar.payload[
            "image_search_evidence_sha256"
        ],
        "canonical_case_count": len(canonical_results),
        "alias_case_count": len(alias_results),
        "activating_alias_count": sum(
            row["relation"] != "related" for row in alias_results
        ),
        "related_alias_rejection_count": sum(
            row["relation"] == "related" and row["rejected"]
            for row in alias_results
        ),
        "pass_count": sum(row["status"] == "pass" for row in canonical_results)
        + sum(row["status"] == "pass" for row in alias_results),
        "status": status,
        "canonical_results": canonical_results,
        "alias_results": alias_results,
        "limitations": [
            "Prompt and audit PASS proves literal contract binding, not successful pixels.",
            "Image-search evidence is qualitative and does not establish prevalence, popularity, or ownership.",
            "Negative visual confounds are pixel-review checks, not forbidden words in a positive prompt.",
            "Low-confidence or source-empty searches remain explicit instead of being upgraded by inference.",
        ],
    }


def _encoded(payload: dict[str, Any]) -> bytes:
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--asset-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets",
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    asset_dir = args.asset_dir.expanduser().resolve()
    output = (
        asset_dir
        / "research_evidence_moe_elements"
        / "qualification_v4.json"
    )
    payload = build_qualification(asset_dir)
    encoded = _encoded(payload)
    if args.check:
        if not output.is_file() or output.read_bytes() != encoded:
            raise SystemExit("moe visual qualification v4 is stale")
    else:
        output.write_bytes(encoded)
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": hashlib.sha256(encoded).hexdigest(),
                "status": payload["status"],
                "cases": payload["canonical_case_count"]
                + payload["alias_case_count"],
                "check": args.check,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
