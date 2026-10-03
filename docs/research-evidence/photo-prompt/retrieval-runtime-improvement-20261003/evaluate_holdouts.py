"""Replay the pre-patch new-scene controls with either runtime on fixed DATA."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-repo", type=Path, required=True)
    parser.add_argument("--test-repo", type=Path, required=True)
    parser.add_argument("--data-repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.test_repo))
    sys.path.insert(0, str(args.runtime_repo / "skills/photo-prompt-image-generator/scripts"))
    import prompt_generator as pg
    file = args.test_repo / "tests/test_photo_retrieval_runtime_improvement.py"
    spec = importlib.util.spec_from_file_location("frozen_retrieval_controls", file)
    controls = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(controls)
    source = args.test_repo / "tests/fixtures/photo_prompt/retrieval_runtime_holdout_v1.json"
    fixture = json.loads(source.read_text())
    data = pg.load_runtime_data(args.data_repo / "skills/photo-prompt-image-generator/assets/photo_prompt_tags.json")
    out = {"holdout_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "provider_calls": 0,
        "category_cases": [], "owner_cases": []}
    author = controls.PhotoRetrievalSubjectHandoffTests()
    for case in fixture["category_cases"]:
        raw, snapshot = author.inputs(case)
        core = author.normalized(raw, snapshot)
        contract, picked = pg.frozen_core_context(data, core, snapshot)
        out["category_cases"].append({"id": case["id"], "authored_category": case["category"],
            "runtime_category": contract["subject_category"], "core_sha256": core["canonical_sha256"],
            "surface_expected": case["surface_allowed"],
            "surface_block_reason": pg.slot_block_reason(data, "surface_material", contract),
            "surface_eligible_before_ranking": sum(pg.core_slot_entry_eligible(data, core, contract, picked,
                "surface_material", entry) for entry in data["slots"]["surface_material"])})
    author = controls.PhotoRetrievalOwnerQueryTests()
    for case in fixture["owner_cases"]:
        corpus, core, snapshot = author.inputs(case)
        corpus["slots"][case["slot"]] = [{"id": "literal_relation", "en": case["evidence"]}]
        query, fields = pg.core_slot_focus_text(corpus, core, case["slot"])
        slots, _, _ = pg.retrieve_core_slots(corpus, core, snapshot)
        out["owner_cases"].append({"id": case["id"], "query": query, "source_fields": fields,
            "contains_owner_phrase": case["evidence"] in query,
            "contains_unrelated_phrase": case["irrelevant"] in query,
            "exposed_candidates": sum(len(s["candidates"]) for s in slots.values())})
    args.output.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
