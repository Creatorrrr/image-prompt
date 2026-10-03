"""Offline, identical-DATA replay of both archived twelve-scene input arms.

Run this file with --runtime-repo for the implementation and --data-repo for
the fixed production assets. It never rewrites the archives or input cores.
Private ranks are diagnostics here, never the shuffled public array order.
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
from pathlib import Path
import subprocess
import sys
from unittest import mock


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-repo", type=Path, required=True)
    parser.add_argument("--data-repo", type=Path, required=True)
    parser.add_argument("--frozen-inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    scripts = args.runtime_repo / "skills/photo-prompt-image-generator/scripts"
    sys.path.insert(0, str(scripts))
    import prompt_generator as pg

    assets = args.data_repo / "skills/photo-prompt-image-generator/assets"
    data = pg.load_runtime_data(assets / "photo_prompt_tags.json")
    args.output.mkdir(parents=True, exist_ok=True)
    summary = {
        "runtime_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=args.runtime_repo, text=True).strip(),
        "runtime_sources": {p.name: digest(p) for p in scripts.glob("*.py")},
        "data_sha256": pg.canonical_json_sha256({
            "dictionary": pg.dictionary_hash(data),
            "quality_layers": data[pg.QUALITY_LAYERS_DATA_KEY],
            "registry": data[pg.VISUAL_OBLIGATIONS_DATA_KEY],
            "semantic_index_source": digest(assets / "photo_prompt_semantic_index.json"),
            "visual_index_source": digest(assets / pg.VISUAL_PROFILE_INDEX_FILENAME),
        }),
        "semantic_entries": len(data[pg.SEMANTIC_INDEX_DATA_KEY]["entries"]),
        "visual_profiles": len(data[pg.VISUAL_OBLIGATIONS_DATA_KEY]["profiles"]),
        "quality_layers_loaded": True, "provider_calls": 0, "scenes": [],
    }
    original_rank = pg.rank_bm25f
    traces = {}

    def rank(index, queries, **kwargs):
        rows = original_rank(index, queries, **kwargs)
        if inspect.currentframe().f_back.f_code is pg.retrieve_core_slots.__code__:
            ids = kwargs.get("allowed_ids") or []
            if ids:
                slot = next(iter(ids)).split(":", 2)[1]
                traces.setdefault(slot, {}).setdefault(next(iter(queries)), []).append({
                    "query": next(iter(queries.values())), "ranks": rows,
                })
        return rows

    for arm in ("public-cli", "public-cli-property"):
        for n in range(1, 13):
            case = f"blind_scene_{n:03d}"
            path = args.frozen_inputs / arm / "inputs" / case
            inputs = {name: json.loads((path / (name + ".json")).read_text())
                      for name in ("authorial-core", "creative-controls", "request-envelope", "embodiment-review")}
            controls = inputs["creative-controls"]
            core = pg.normalize_authorial_core(inputs["authorial-core"],
                request_envelope=pg.normalize_request_envelope(inputs["request-envelope"]),
                creative_control_snapshot=controls)
            traces.clear()
            with mock.patch.object(pg, "rank_bm25f", rank), mock.patch.object(
                    pg, "cached_gemini_client", side_effect=AssertionError("offline replay forbids provider calls")):
                pack = pg.generate_candidate_pack(data, core, controls, inputs["embodiment-review"], seed=829)
            contract, picked = pg.frozen_core_context(data, core, controls)
            slot_rows = {}
            for slot in ("light_direction", "camera_direction", "focus", "surface_material", "texture"):
                entries = data["slots"].get(slot, [])
                returned = pack["slots"].get(slot, {}).get("candidates", [])
                slot_rows[slot] = {
                    "corpus_count": len(entries),
                    "eligible_before_ranking": sum(pg.core_slot_entry_eligible(data, core, contract, picked, slot, e) for e in entries),
                    "block_reason": pg.slot_block_reason(data, slot, contract),
                    "public_ids": [c["id"] for c in returned],
                    "public_eligibility": {c["id"]: c.get("applicability") for c in returned},
                    "retrieval": traces.get(slot, {}),
                }
            total = sum(len(s["candidates"]) for s in pack["slots"].values())
            row = {"arm": arm, "case": case, "input_sha256": {p.name: digest(p) for p in path.glob("*.json")},
                   "core_sha256": core["canonical_sha256"], "subject_category": contract["subject_category"],
                   "total_candidates": total, "all_ids": {s: [c["id"] for c in v["candidates"]] for s, v in pack["slots"].items()},
                   "all_applicability": {c["id"]: c.get("applicability") for v in pack["slots"].values() for c in v["candidates"]},
                   "target_slots": slot_rows, "candidate_order": pack["authorial_composition"]["candidate_order"]}
            summary["scenes"].append(row)
            (args.output / f"{arm}-{case}-pack.json").write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n")
            print(arm, case, "total", total, "targets", {s: len(v["public_ids"]) for s, v in slot_rows.items()}, flush=True)
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
