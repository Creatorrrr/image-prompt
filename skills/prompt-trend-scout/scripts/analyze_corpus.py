#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Any

from common import SKILL_DIR, default_data_dir, load_json, normalize_space, read_records, run_id, utc_now, write_json


RISK_PREFIXES = ("ip_", "brand", "minor_", "sexual_", "graphic_")


def token_set(text: str) -> set[str]:
    return {token for token in normalize_space(text.lower()).replace("_", " ").split(" ") if len(token) > 2}


def jaccard(a: str, b: str) -> float:
    left = token_set(a)
    right = token_set(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def candidate_id(kind: str, key: str) -> str:
    digest = hashlib.sha256(f"{kind}:{key}".encode("utf-8")).hexdigest()[:12]
    return f"cand-{digest}"


def load_taxonomy() -> dict[str, Any]:
    taxonomy = load_json(SKILL_DIR / "assets" / "visual_grammar_taxonomy.json")
    return {rule["id"]: rule for rule in taxonomy.get("rules", [])}


def make_unknown_rule(element: str) -> dict[str, Any]:
    phrase = element.replace("_", " ")
    return {
        "id": element,
        "kind": "tag",
        "target_asset": "photo_prompt_tags.json",
        "slot": "mood",
        "en": phrase,
        "ko": phrase,
        "facet": {},
    }


def analyze_records(
    input_path: str,
    *,
    output: str | None = None,
    data_dir: str | None = None,
    min_frequency: int = 1,
    verbatim_threshold: float = 0.25,
) -> dict[str, Any]:
    records = read_records(Path(input_path))
    taxonomy = load_taxonomy()
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grammar = record.get("abstract_visual_grammar", {})
        for element in grammar.get("visual_elements", []) or []:
            grouped[str(element)].append(record)

    candidates: list[dict[str, Any]] = []
    for element, examples in sorted(grouped.items()):
        if len(examples) < min_frequency:
            continue
        rule = taxonomy.get(element) or make_unknown_rule(element)
        proposed = {
            "id": rule["id"],
            "en": rule.get("en", rule["id"].replace("_", " ")),
            "ko": rule.get("ko", rule.get("en", rule["id"])),
            "facet": rule.get("facet", {}),
        }
        if rule.get("slot"):
            proposed["slot"] = rule["slot"]
            proposed["value"] = rule["id"]
        risk_flags = sorted({flag for ex in examples for flag in ex.get("flags", []) if flag.startswith(RISK_PREFIXES)})
        max_similarity = max(jaccard(proposed["en"], ex.get("sanitized_prompt", "")) for ex in examples)
        recommendation = "adopt" if len(examples) >= 3 else "trial"
        if risk_flags:
            recommendation = "needs_human"
        if max_similarity > verbatim_threshold:
            recommendation = "reject"
        confidence = min(0.95, 0.45 + len(examples) * 0.12)
        candidates.append(
            {
                "candidate_id": candidate_id(rule["kind"], rule["id"]),
                "kind": rule["kind"],
                "target_asset": rule["target_asset"],
                "proposed": proposed,
                "abstracted_from": [ex["id"] for ex in examples],
                "frequency": len(examples),
                "novelty": "new",
                "overlap_with_existing": [],
                "confidence": round(confidence, 2),
                "rationale": f"Observed reusable visual grammar: {proposed['en']}.",
                "risk_flags": risk_flags,
                "verbatim_similarity": round(max_similarity, 3),
                "recommendation": recommendation,
            }
        )
    data_root = default_data_dir(data_dir)
    rid = run_id("candidates")
    out = Path(output) if output else data_root / "candidates" / f"{rid}.json"
    write_json(out, {"run_id": rid, "generated_at": utc_now(), "records": candidates})
    return {"run_id": rid, "output": str(out), "records": candidates}


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze sanitized examples into reflection candidates.")
    parser.add_argument("input")
    parser.add_argument("--output")
    parser.add_argument("--data-dir")
    parser.add_argument("--min-frequency", type=int, default=1)
    parser.add_argument("--verbatim-threshold", type=float, default=0.25)
    args = parser.parse_args()
    result = analyze_records(
        args.input,
        output=args.output,
        data_dir=args.data_dir,
        min_frequency=args.min_frequency,
        verbatim_threshold=args.verbatim_threshold,
    )
    print(result["output"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
