#!/usr/bin/env python3
"""Emit bounded semantic/prompt qualification evidence for moe grammar v3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from illustration_runtime import build_candidate_pack
from moe_element_runtime import (
    PACK_SCHEMA,
    audit_moe_candidate_pack,
    build_moe_candidate_pack,
    compose_moe_prompt_draft,
    load_moe_element_assets,
    load_moe_grammar_assets,
)


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    asset_dir = skill_root / "assets"
    evidence_root = asset_dir / "research_evidence_moe_elements"
    corpus_path = evidence_root / "intent_corpus_v2.json"
    output_path = evidence_root / "qualification_v3.json"
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    legacy = load_moe_element_assets(asset_dir)
    grammar = load_moe_grammar_assets(
        asset_dir,
        legacy_assets=legacy,
        grammar_version="v3",
    )
    foundation = "An original adult-character illustration with one causal event"
    results: list[dict[str, object]] = []
    for index, row in enumerate(
        corpus["sections"]["representative_baseline_v4_comparisons"], 1
    ):
        request = row["request_ko"]
        element_ids = row["expected_element_ids"]
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
        bindings = pack["moe_grammar"]["meaning_bindings"]
        selected = pack["moe_grammar"]["selected_candidates"]
        nodes = pack["moe_grammar"]["selected_nodes"]
        result_status = (
            "pass"
            if pack["contract_version"] == PACK_SCHEMA
            and audit["status"] == "pass"
            and element_ids == [binding["element_id"] for binding in bindings]
            and all(
                candidate["meaning_contract_sha256"] == binding["contract_sha256"]
                for candidate, binding in zip(selected, bindings, strict=True)
            )
            else "fail"
        )
        results.append(
            {
                "id": row["id"],
                "request_sha256": hashlib.sha256(request.encode("utf-8")).hexdigest(),
                "expected_element_ids": element_ids,
                "v5_pack_id": pack["pack_id"],
                "v5_selected_candidate_ids": [
                    candidate["candidate_id"] for candidate in selected
                ],
                "v5_selected_semantic_fidelities": [
                    candidate["semantic_fidelity"] for candidate in selected
                ],
                "v5_meaning_contract_sha256": [
                    binding["contract_sha256"] for binding in bindings
                ],
                "v5_support_node_ids": [
                    node["id"] for node in nodes if node["selected_role"] == "support"
                ],
                "v5_prompt_en": composed["prompt_en"],
                "v5_audit_status": audit["status"],
                "meaning_binding_status": result_status,
            }
        )

    payload = {
        "schema": "subculture-illustration-moe-prompt-qualification/v3",
        "created_at": "2026-08-17T00:00:00+09:00",
        "scope": (
            "12 deterministic semantic-binding and prompt-component comparisons; "
            "no rendered-pixel or population-preference claim"
        ),
        "intent_corpus_sha256": hashlib.sha256(corpus_path.read_bytes()).hexdigest(),
        "grammar_sha256": grammar.grammar_sha256,
        "meaning_contracts_sha256": grammar.payload["meaning_contracts_sha256"],
        "meaning_contract_count": len(grammar.elements_by_id),
        "case_count": len(results),
        "pass_count": sum(row["meaning_binding_status"] == "pass" for row in results),
        "status": (
            "pass"
            if all(row["meaning_binding_status"] == "pass" for row in results)
            else "fail"
        ),
        "results": results,
        "limitations": [
            "The audit proves canonical contract binding and literal component evidence, not rendered pixels.",
            "Safe-analogue fidelity preserves relational structure without claiming a literal sensitive archetype.",
            "Sequence- and interaction-required meanings still need their declared output medium and final perceptual review.",
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
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
