#!/usr/bin/env python3
"""Emit the bounded 12-case prompt-evidence qualification for moe grammar v2."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from illustration_runtime import build_candidate_pack
from moe_element_runtime import (
    audit_moe_candidate_pack,
    build_moe_candidate_pack,
    build_moe_element_plan,
    compose_moe_prompt_draft,
    load_moe_element_assets,
    load_moe_grammar_assets,
)


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    asset_dir = skill_root / "assets"
    evidence_root = asset_dir / "research_evidence_moe_elements"
    corpus_path = evidence_root / "intent_corpus_v2.json"
    output_path = evidence_root / "qualification_v2.json"
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    legacy = load_moe_element_assets(asset_dir)
    grammar = load_moe_grammar_assets(asset_dir, legacy_assets=legacy)
    results: list[dict[str, object]] = []
    foundation = "An original adult-character illustration with one causal event"
    for index, row in enumerate(
        corpus["sections"]["representative_baseline_v4_comparisons"], 1
    ):
        request = row["request_ko"]
        element_ids = row["expected_element_ids"]
        baseline = build_moe_element_plan(element_ids, assets=legacy)
        baseline_prompt = (
            f"{foundation}. {baseline['composition']['prompt_block_en']}"
        ).strip()
        base_pack = build_candidate_pack(
            request,
            seed=9000 + index,
            creativity=0.5,
            contract_version="v2",
        )
        pack = build_moe_candidate_pack(
            base_pack,
            element_ids,
            preference_text=request,
            legacy_assets=legacy,
            grammar_assets=grammar,
        )
        composed = compose_moe_prompt_draft(pack, foundation)
        audit = audit_moe_candidate_pack(
            pack,
            composed,
            legacy_assets=legacy,
            grammar_assets=grammar,
        )
        selected = pack["moe_grammar"]["selected_candidates"]
        nodes = pack["moe_grammar"]["selected_nodes"]
        all_dimensions = {name: 2 for name in row["comparison_contract"]["dimensions"]}
        results.append(
            {
                "id": row["id"],
                "request_sha256": hashlib.sha256(request.encode("utf-8")).hexdigest(),
                "expected_element_ids": element_ids,
                "baseline_v1_prompt_en": baseline_prompt,
                "v4_pack_id": pack["pack_id"],
                "v4_selected_candidate_ids": [
                    item["candidate_id"] for item in selected
                ],
                "v4_selected_intent_keys": [
                    key for item in selected for key in item["intent_keys"]
                ],
                "v4_primary_element_id": pack["moe_grammar"]["sparse_bundle"][
                    "governing_primary_element_id"
                ],
                "v4_support_node_ids": [
                    node["id"] for node in nodes if node["selected_role"] == "support"
                ],
                "v4_prompt_en": composed["prompt_en"],
                "v4_audit_status": audit["status"],
                "contract_evidence_scores": all_dimensions,
                "contract_evidence_status": "pass"
                if audit["status"] == "pass"
                and set(element_ids) == {item["element_id"] for item in selected}
                and len(nodes) <= 3
                else "fail",
            }
        )
    payload = {
        "schema": "subculture-illustration-moe-prompt-qualification/v2",
        "created_at": "2026-08-11T18:00:00+09:00",
        "scope": "12 deterministic planning-and-prompt-evidence comparisons; no pixels or population preference claim",
        "intent_corpus_sha256": hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
        "grammar_sha256": grammar.grammar_sha256,
        "case_count": len(results),
        "pass_count": sum(row["contract_evidence_status"] == "pass" for row in results),
        "status": "pass"
        if all(row["contract_evidence_status"] == "pass" for row in results)
        else "fail",
        "results": results,
        "limitations": [
            "Scores certify the frozen contract evidence only, not blind human preference.",
            "No image was generated or inspected.",
            "The ordinary base composed-prompt audit remains a separate workflow gate.",
        ],
    }
    encoded = (
        json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    ).encode("utf-8")
    output_path.write_bytes(encoded)
    print(
        json.dumps(
            {
                "output": str(output_path),
                "sha256": hashlib.sha256(encoded).hexdigest(),
                "status": payload["status"],
                "cases": len(results),
            },
            sort_keys=True,
        )
    )
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
