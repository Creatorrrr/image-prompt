"""Read-only taxonomy evidence; never edits candidate or runtime sources."""
from __future__ import annotations

import ast
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import photo_candidate_corpus as corpus
import prompt_generator as generator
import photo_slot_queries as queries
import photo_runtime_sources as runtime


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    data = corpus.load(SKILL / "assets")
    catalog = data["slot_catalog"]
    groups = {
        key.removeprefix("SLOT_FOCUS_").removesuffix("_SLOTS"): getattr(generator, key)
        for key in vars(generator)
        if key.startswith("SLOT_FOCUS_") and key.endswith("_SLOTS")
    }
    bindings = collections.defaultdict(list)
    for binding in data["slot_bindings"].values():
        bindings[binding["slot_id"]].append(binding)
    consumers = collections.defaultdict(list)
    for directory in (SKILL / "scripts", SKILL / "precore"):
        for path in sorted(directory.glob("*.py")):
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in catalog:
                    pointer = {"path": str(path.relative_to(ROOT)), "line": node.lineno}
                    if pointer not in consumers[node.value]:
                        consumers[node.value].append(pointer)
    inventory, cards = [], []
    for slot, definition in catalog.items():
        rows = bindings[slot]
        # Rare roles: every linked payload. Other roles: stable order spread plus
        # three ID-hash picks. This is qualitative coverage, not a random accuracy estimate.
        if len(rows) <= 12:
            selected = rows
        else:
            selected = [rows[0], rows[len(rows) // 2], rows[-1]]
            selected += sorted(rows, key=lambda b: hashlib.sha256(b["candidate_id"].encode()).hexdigest())[:3]
        unique = {row["id"]: row for row in selected}
        example_ids = []
        for binding in unique.values():
            candidate = data["candidates"][binding["candidate_id"]]
            cards.append({"slot_id": slot, "candidate": candidate, "binding": binding})
            example_ids.append(candidate["id"])
        dimensions = set(definition["dimensions"])
        inventory.append({
            "slot_id": slot,
            "definition": definition,
            "query_focus_ko": queries.KO[slot],
            "linked_binding_count": len(rows),
            "linked_candidate_count": len({b["candidate_id"] for b in rows}),
            "label_only_description": definition["description"] == slot.replace("_", " "),
            "empty_dimensions": not dimensions,
            "dimension_disjoint_bindings": sum(not dimensions.intersection(b["effects"]["dimensions"]) for b in rows),
            "effect_dimensions": sorted({d for b in rows for d in b["effects"]["dimensions"]}),
            "focus_groups": [key for key, values in groups.items() if slot in values],
            "presentation_priority": "core" if slot in generator.CANDIDATE_PACK_CORE_SLOTS else "support",
            "representative_candidate_ids": example_ids,
            "exact_string_code_consumers": consumers[slot],
        })
    save("INVENTORY.json", inventory)
    (OUT / "CANDIDATE-CARDS.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in cards))
    save("CATALOG-SNAPSHOT.json", catalog)
    authored = [path for path in (SKILL / "assets").glob("photo_candidate_*.json")
                if "search" not in path.name]
    plan = "docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md"
    tracked_dirty = [name for name in subprocess.check_output(
        ["git", "diff", "--name-only"], cwd=ROOT, text=True).splitlines() if name != plan]
    critical = [SKILL / "scripts" / name for name in (
        "photo_candidate_corpus.py", "photo_slot_queries.py", "photo_role_proposals.py",
        "photo_slot_retrieval.py", "photo_global_retrieval.py", "prompt_generator.py",
    )]
    search_path = SKILL / "assets/photo_candidate_search.json"
    search_manifest = json.loads(search_path.read_text())
    pointer_path = runtime._pointer_directory(runtime.default_store(), SKILL, "local_current") / "CURRENT.json"
    pointer = json.loads(pointer_path.read_text())
    summary = {
        "schema": "photo-slot-taxonomy-evidence/v1",
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "corpus_sha256": corpus.digest(data),
        "candidate_count": len(data["candidates"]),
        "record_kinds": dict(collections.Counter(r["record_kind"] for r in data["candidates"].values())),
        "binding_count": len(data["slot_bindings"]),
        "slot_count": len(catalog),
        "label_only_description_count": sum(row["label_only_description"] for row in inventory),
        "empty_dimension_slots": [r["slot_id"] for r in inventory if r["empty_dimensions"]],
        "empty_dimension_binding_count": sum(r["linked_binding_count"] for r in inventory if r["empty_dimensions"]),
        "slots_without_core_focus_projection": [r["slot_id"] for r in inventory if not r["focus_groups"]],
        "dimension_slot_counts": dict(collections.Counter(d for spec in catalog.values() for d in spec["dimensions"])),
        "candidate_card_count": len(cards),
        "unique_review_card_candidates": len({r["candidate"]["id"] for r in cards}),
        "selection_method": "all linked candidates when <=12; otherwise first/middle/last plus three SHA256-ID picks; not statistical",
        "input_files": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(authored + critical)},
        "operating_code_sha256": runtime.code_inventory(SKILL),
        "active_search_manifest_sha256": hashlib.sha256(search_path.read_bytes()).hexdigest(),
        "active_search_layout_id": search_manifest["layout_id"],
        "runtime_pointer_path": str(pointer_path),
        "runtime_pointer_sha256": hashlib.sha256(pointer_path.read_bytes()).hexdigest(),
        "runtime_pointer": pointer,
        "unrelated_tracked_dirty_hashes": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in tracked_dirty},
        "runtime_mutation": False,
        "provider_calls": 0,
    }
    save("SOURCE-VERIFICATION.json", summary)
    print(json.dumps({key: value for key, value in summary.items() if key not in {
        "input_files", "operating_code_sha256", "unrelated_tracked_dirty_hashes", "runtime_pointer_path", "runtime_pointer",
    }}, ensure_ascii=False))


if __name__ == "__main__":
    main()
