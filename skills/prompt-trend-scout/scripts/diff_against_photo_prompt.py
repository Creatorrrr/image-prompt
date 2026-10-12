#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from common import TARGET_SKILL_DIR, default_data_dir, load_json, read_records, run_id, utc_now, write_json


def existing_index() -> dict[str, Any]:
    import sys
    sys.path.insert(0,str(TARGET_SKILL_DIR/'scripts'))
    import photo_candidate_corpus as c
    source=c.load(TARGET_SKILL_DIR/'assets')
    candidate_ids=set(source['candidates'])
    texts={str(r['content'].get(lang,'')).casefold() for r in source['candidates'].values() for lang in ('en','ko')}
    return {'candidate_ids':candidate_ids,'candidate_texts':texts-{' '},'slot_tags':set(source['slot_catalog']),
            'facet_values':{k:set(v) for k,v in source['policies'].get('facet_vocab',{}).items()}}


def diff_candidates(input_path: str, *, output: str | None = None, data_dir: str | None = None) -> dict[str, Any]:
    candidates = read_records(Path(input_path))
    index = existing_index()
    diffed: list[dict[str, Any]] = []
    for candidate in candidates:
        candidate = dict(candidate)
        proposed = candidate.get("proposed", {})
        overlaps: list[str] = []
        novelty = "new"
        if candidate["kind"] == "tag":
            slot = proposed.get("slot", "")
            value = proposed.get("value") or proposed.get("id")
            en = str(proposed.get("en", "")).lower()
            if value in index["candidate_ids"]:
                novelty = "reinforce"
                overlaps.append(f"{slot}.{value}")
            elif en and en in index["candidate_texts"]:
                novelty = "reinforce"
                overlaps.append(f"{slot}.text:{en}")
            elif slot not in index["slot_tags"]:
                novelty = "conflict"
                overlaps.append(f"unknown_slot:{slot}")
        elif candidate["kind"] == "facet_value":
            facet = proposed.get("facet_name", "")
            value = proposed.get("value") or proposed.get("id")
            if value in index["facet_values"].get(facet, set()):
                novelty = "reinforce"
                overlaps.append(f"facet:{facet}.{value}")
            elif facet and facet not in index["facet_values"]:
                novelty = "conflict"
                overlaps.append(f"unknown_facet:{facet}")
        candidate["novelty"] = novelty
        candidate["overlap_with_existing"] = overlaps
        if novelty == "conflict" and candidate.get("recommendation") == "adopt":
            candidate["recommendation"] = "needs_human"
        diffed.append(candidate)

    data_root = default_data_dir(data_dir)
    rid = run_id("diffed")
    out = Path(output) if output else data_root / "candidates" / f"{rid}.json"
    write_json(out, {"run_id": rid, "generated_at": utc_now(), "records": diffed})
    return {"run_id": rid, "output": str(out), "records": diffed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare prompt trend candidates with photo-prompt assets.")
    parser.add_argument("input")
    parser.add_argument("--output")
    parser.add_argument("--data-dir")
    args = parser.parse_args()
    result = diff_candidates(args.input, output=args.output, data_dir=args.data_dir)
    print(result["output"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
