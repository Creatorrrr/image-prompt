#!/usr/bin/env python3
"""Replay the diagnosed data probes without network calls or source mutations."""
import argparse
import collections
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as pg
import photo_candidate_semantics as candidates
from bm25f_retrieval import rank_bm25f


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    previous = json.loads((ROOT / "docs/analysis/2026-09-06-photo-data-audit/data-audit.json").read_text())
    data = pg.load_json(ASSETS / "photo_prompt_tags.json")
    registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
    index = pg.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", registry)
    profiles = registry["profiles"]
    probes = []
    for old in previous["exact_activation_probes"]:
        resolution = pg.resolve_visual_profile_hits(
            registry, old["source_rows"], visual_profile_index=index,
            adult_context=old["adult_context"],
        )
        probes.append({
            "case_id": old["case_id"], "source_rows": old["source_rows"],
            "before": old["hits"], "after": resolution["hits"],
        })
    lexical = []
    for old in previous["raw_bm25f_probes"]:
        hits = rank_bm25f(index["bm25f"], old["query_fields"], limit=5)
        lexical.append({"query_fields": old["query_fields"],
                        "before": old["raw_top_three_before_applicability"], "after": hits})
    mutation_results = []
    mutation = copy.deepcopy(data)
    mutation["candidate_bundles"][0]["associated_profile_ids"] = ["audit_nonexistent_profile"]
    try:
        candidates.validate_bundle_references(mutation, profiles)
        mutation_results.append({"probe": "dangling_profile", "status": "accepted"})
    except ValueError as error:
        mutation_results.append({"probe": "dangling_profile", "status": "rejected", "error": str(error)})
    mutation_results.append({"probe": "bundle_hash_binding", "status": "pass" if pg.dictionary_hash(data) != pg.dictionary_hash(mutation) else "fail"})
    try:
        pg.merge_research_extension(copy.deepcopy(data), {"schema_version": pg.RESEARCH_EXTENSION_SCHEMA, "unrecognized_runtime_policy": True})
        mutation_results.append({"probe": "unknown_runtime_key", "status": "accepted"})
    except ValueError as error:
        mutation_results.append({"probe": "unknown_runtime_key", "status": "rejected", "error": str(error)})
    process_tags = []
    labels = collections.defaultdict(list)
    examples = []
    sample_ids = {"lit_clean_large_soft_key_return", "lit_clean_low_ratio_open_shadow", "lit_clean_vertical_catchlight_pair"}
    for slot, rows in data["slots"].items():
        for entry in rows:
            public_tags = pg.candidate_pack_public_tags(data, entry)
            if any(candidates.maintenance_tag(tag) for tag in public_tags):
                process_tags.append(f"{slot}:{entry['id']}")
            labels[(slot, entry.get("en", "").strip().casefold())].append(entry["id"])
            if entry["id"] in sample_ids:
                examples.append({"slot": slot, "entry_id": entry["id"],
                                 "surface": candidates.semantic_source(entry, slot, data.get("candidate_semantic_policy"))})
    report = {
        "scope": "Authored data and deterministic retrieval probes; raw search ranks precede applicability; no render acceptance claim.",
        "dictionary_sha256": pg.dictionary_hash(data),
        "registry_sha256": index["registry_sha256"],
        "counts": {
            "profiles": len(profiles), "candidate_bundles": len(data.get("candidate_bundles", [])),
            "slot_candidates": sum(map(len, data["slots"].values())),
            "authored_component_profiles": sum(bool(p.get("authored_components")) for p in profiles),
            "profiles_with_claim_limits": sum(bool(p["semantics"].get("claim_limits")) for p in profiles),
            "single_literal_rules": sum(len(r.get("must_mention_any", [])) == 1 for p in profiles for r in p["evidence_requirements"].values()),
            "candidates_with_public_process_tags": len(process_tags),
        },
        "activation_probes": probes, "raw_bm25f_probes": lexical,
        "mutation_results": mutation_results, "public_semantic_examples": examples,
        "same_slot_exact_label_duplicates": [{"slot": slot, "label": label, "ids": ids} for (slot, label), ids in labels.items() if label and len(ids) > 1],
        "source_files": [{"path": str(p.relative_to(ROOT)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(ASSETS.glob("*.json"))],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
