"""Freeze complete authored inputs and reference ownership before native migration."""
from __future__ import annotations
import collections
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as c
import photo_global_index as index
import photo_runtime_sources as runtime

def main():
    source = c.load(SKILL / "assets")
    baseline = OUT / "CORPUS-BEFORE.json.gz"
    if baseline.exists():
        raise ValueError("Frozen baseline already exists; never overwrite it with a later stage")
    baseline.write_bytes(gzip.compress(c.canonical_bytes(source), mtime=0))
    manifest = c.decode((SKILL / "assets" / c.MANIFEST_NAME).read_bytes())
    owners = {}
    modules = {}
    for module in manifest["modules"]:
        path = SKILL / "assets" / module["file"]
        modules[module["file"]] = hashlib.sha256(path.read_bytes()).hexdigest()
        for cid in c.decode(path.read_bytes()).get("candidates", {}):
            owners[cid] = module["file"]
    bindings = collections.defaultdict(list)
    for bid, binding in source["slot_bindings"].items():
        bindings[binding["candidate_id"]].append(bid)
    inventory = []
    for cid, record in source["candidates"].items():
        recipe, text = index.text(record)
        def references(value):
            if isinstance(value, str):
                return [value] if c.ID.fullmatch(value) or c.BINDING_ID.fullmatch(value) else []
            if isinstance(value, dict):
                return [ref for key, nested in value.items() for ref in references(key) + references(nested)]
            if isinstance(value, list):
                return [ref for nested in value for ref in references(nested)]
            return []
        inventory.append({"candidate_id": cid, "record_kind": record["record_kind"],
            "payload_owner": owners[cid], "record_sha256": c.digest(record),
            "text_recipe": recipe, "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "binding_ids": bindings[cid], "slot_ids": [source["slot_bindings"][bid]["slot_id"] for bid in bindings[cid]],
            "references": sorted(set(references(record["content"]))),
            "provenance": record["provenance"], "effects": record["effects"],
            "taxonomy_review_scope": "existing bindings in stage03; whole-candidate enrichment remains stage04-08"})
    (OUT / "INVENTORY-BEFORE.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in inventory))
    search = c.decode((SKILL / "assets/photo_candidate_search.json").read_bytes())
    pointer_path = runtime._pointer_directory(runtime.default_store(), SKILL, "local_current") / "CURRENT.json"
    pointer = c.decode(pointer_path.read_bytes())
    protected = ["docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md",
                 "docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md"]
    report = {"git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "corpus_sha256": c.digest(source), "candidates": len(source["candidates"]),
        "bindings": len(source["slot_bindings"]), "slots": len(source["slot_catalog"]),
        "record_kinds": dict(collections.Counter(row["record_kind"] for row in inventory)),
        "payload_owner_coverage": len(owners), "inventory_count": len(inventory),
        "baseline_sha256": hashlib.sha256(baseline.read_bytes()).hexdigest(), "module_sha256": modules,
        "search_manifest": {"layout_id": search["layout_id"], "sha256": hashlib.sha256((SKILL / "assets/photo_candidate_search.json").read_bytes()).hexdigest()},
        "runtime_current": pointer, "operating_code": runtime.code_inventory(SKILL),
        "protected_dirty_files": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in protected},
        "effects_equal_in_all_bindings": all(binding["effects"] == source["candidates"][binding["candidate_id"]]["effects"] for binding in source["slot_bindings"].values()),
        "verified": len(inventory) == len(owners) == len(source["candidates"]) == 18250 and len(source["slot_bindings"]) == 12020}
    (OUT / "STAGE01-VERIFICATION.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    baseline_tests = Path("/tmp/image-prompt-slot-taxonomy-baseline-tests.log")
    if baseline_tests.exists():
        shutil.copyfile(baseline_tests, OUT / "baseline-tests.log")
    print(json.dumps({key: value for key, value in report.items() if key not in {"module_sha256", "operating_code", "protected_dirty_files", "runtime_current"}}, ensure_ascii=False))

if __name__ == "__main__":
    main()
