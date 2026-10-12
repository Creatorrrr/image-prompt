#!/usr/bin/env python3
"""Maintenance evidence: current source identities and same-slot exact recall.

No network, embeddings, image calls, source edits, or alternate ranker.
All queries use production rank_bm25f on every document in the owning slot.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import csv
import json
import multiprocessing
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--root", type=Path, required=True)
parser.add_argument("--lane", required=True)
parser.add_argument("--inventory-only", action="store_true")
parser.add_argument("--runtime-store", type=Path)
args = parser.parse_args()
ROOT = args.root
OUT = OUT / args.lane
OUT.mkdir(exist_ok=True)
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as g
from photo_runtime_sources import RuntimeSnapshotProvider
from photo_source_manifest import SourceInventory

INDEX = None


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def exact_slot(job):
    slot, entries = job
    allowed = [f"slot:{slot}:{entry['id']}" for entry in entries]
    results = []
    for entry in entries:
        queries = [(field, entry[field]) for field in ("en", "ko") if entry.get(field)]
        queries.extend(("alias", value) for value in dict.fromkeys(entry.get("aliases") or []) if value)
        for field, query in queries:
            ranked = g.rank_bm25f(INDEX, {"slot_focus": query}, allowed_ids=allowed, limit=len(allowed))
            ids = [row["document_id"] for row in ranked]
            expected = f"slot:{slot}:{entry['id']}"
            rank = ids.index(expected) + 1 if expected in ids else None
            results.append({"slot": slot, "entry_id": entry["id"], "query_field": field,
                            "query": query, "rank": rank, "slot_limit": g.candidate_pack_slot_limit(slot),
                            "returned_count": len(ids), "top_ids": ids[:8]})
    return slot, results


def main():
    global INDEX
    start = time.monotonic()
    provider = RuntimeSnapshotProvider(SKILL, args.runtime_store or OUT.parent / (args.lane + "-runtime-store"))
    snapshot = provider.acquire()
    save("runtime-acquisition.json", {"generation_id": snapshot.generation_id, "source_fingerprint": snapshot.manifest["source_fingerprint"], "sealed_root": str(snapshot.root)})
    data = snapshot.data
    inventory = SourceInventory.load(snapshot.root / "assets")
    raw = collections.defaultdict(list)
    for name in ("photo_prompt_tags.json", *inventory.files("candidate")):
        path = snapshot.root / "assets" / name
        if not path.exists():
            continue
        payload = json.loads(path.read_text())
        for slot, entries in payload.get("slots", {}).items():
            for position, entry in enumerate(entries):
                raw[(slot, entry["id"])].append({"source_file": name, "position": position,
                                                "en": entry.get("en"), "ko": entry.get("ko")})
    loaded = {(slot, entry["id"]): entry for slot, entries in data["slots"].items() for entry in entries}
    corpus_json = json.dumps(data["slots"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    INDEX = data.slot_index(corpus_json)
    expected = {f"slot:{slot}:{eid}" for slot, eid in loaded}
    lexical = set(INDEX["documents"])
    semantic = set(data[g.SEMANTIC_INDEX_DATA_KEY]["entries"])
    semantic_slots = {key for key in semantic if key.startswith("slot:")}
    rows = []
    for slot, entries in sorted(data["slots"].items()):
        ownership = g.photo_candidate_semantics.slot_dimensions(slot, data.get("candidate_semantic_policy"))
        fallback = sorted({value for entry in entries for value in entry.get("affected_dimensions") or []})
        rows.append({"slot": slot, "candidate_count": len(entries), "ownership": ownership,
                     "entry_dimension_fallback": fallback, "focus_capable": bool(ownership or fallback),
                     "slot_limit": g.candidate_pack_slot_limit(slot),
                     "sources": sorted({r["source_file"] for entry in entries for r in raw[(slot, entry["id"])]}),
                     "ids": [entry["id"] for entry in entries]})
    result = {"generation_id": snapshot.generation_id, "source_fingerprint": snapshot.manifest["source_fingerprint"],
              "raw_count": len(raw), "loaded_count": len(loaded), "slot_count": len(rows),
              "duplicate_source_ids": [list(key) for key, value in raw.items() if len(value) != 1],
              "raw_not_loaded": [list(key) for key in raw.keys() - loaded.keys()],
              "loaded_not_raw": [list(key) for key in loaded.keys() - raw.keys()],
              "source_labels_changed": [list(key) for key, entry in loaded.items()
                  if any(entry.get(field) != raw[key][0].get(field) for field in ("en", "ko"))],
              "lexical_missing": sorted(expected - lexical), "lexical_extra": sorted(lexical - expected),
              "semantic_missing": sorted(expected - semantic_slots), "semantic_extra": sorted(semantic_slots - expected),
              "semantic_non_slot_documents": len(semantic - semantic_slots), "slots": rows}
    save("inventory.json", result)
    save("candidate-provenance.json", {f"slot:{slot}:{eid}": value[0] for (slot, eid), value in raw.items()})
    if args.inventory_only:
        print(json.dumps({"slots": len(rows), "candidates": len(loaded),
                          "generation_id": snapshot.generation_id, "exact_sweep_rerun": False}), flush=True)
        return
    print(f"Inventory: {len(rows)} slots / {len(loaded)} candidates; exact query sweep started", flush=True)
    totals = collections.Counter()
    per_slot = []
    with (OUT / "exact-recall.ndjson").open("w") as stream, concurrent.futures.ProcessPoolExecutor(
            max_workers=4, mp_context=multiprocessing.get_context("fork")) as pool:
        jobs = [(slot, [{"id": entry["id"], "en": entry.get("en"), "ko": entry.get("ko"),
                        "aliases": list(entry.get("aliases") or [])} for entry in data["slots"][slot]])
                for slot in sorted(data["slots"])]
        futures = {pool.submit(exact_slot, job): job[0] for job in jobs}
        for future in concurrent.futures.as_completed(futures):
            slot, results = future.result()
            counters = collections.Counter()
            by_field = {}
            for row in results:
                stream.write(json.dumps(row, ensure_ascii=False) + "\n")
                counters["queries"] += 1
                rank = row["rank"]
                for name, condition in (("top1", rank == 1), ("within_slot_cap", rank is not None and rank <= row["slot_limit"]),
                                        ("top24", rank is not None and rank <= 24), ("retrievable", rank is not None)):
                    counters[name] += int(condition)
                field = by_field.setdefault(row["query_field"], collections.Counter())
                field["queries"] += 1
                field["top1"] += int(rank == 1)
                field["within_slot_cap"] += int(rank is not None and rank <= row["slot_limit"])
                field["top24"] += int(rank is not None and rank <= 24)
                field["retrievable"] += int(rank is not None)
            stream.flush()
            totals.update(counters)
            per_slot.append({"slot": slot, **dict(counters), "by_field": {key: dict(value) for key, value in by_field.items()}})
            print(f"Exact {slot}: {counters['retrievable']}/{counters['queries']} retrieved, cap {counters['within_slot_cap']}", flush=True)
    save("exact-recall-summary.json", {"totals": dict(totals), "slots": sorted(per_slot, key=lambda row: row["slot"]),
                                       "elapsed_seconds": round(time.monotonic() - start, 3),
                                       "query_policy": "all en, all ko, all unique explicit aliases; full same-slot allowed IDs; production ranker"})
    print(json.dumps(dict(totals)), flush=True)


if __name__ == "__main__":
    main()
