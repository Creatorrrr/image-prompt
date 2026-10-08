"""Read-only lexical inventory for the 2026-10-08 fashion-fit research.

This writes evidence beside itself, never runtime assets or generated indexes.
It does not call retrieval, an embedding provider or an image provider.
Positive-field mentions are lexical evidence, not semantic support or pixel proof.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import stat
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
sys.dont_write_bytecode = True
sys.path.insert(0, str(SKILL / "scripts"))


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def normalize(text):
    text = unicodedata.normalize("NFKC", str(text)).casefold()
    return re.sub(r"[\W_]+", " ", text).strip()


def snap(paths):
    result = {}
    for path in paths:
        p = Path(path)
        b = p.read_bytes()
        result[str(p.relative_to(ROOT))] = {
            "sha256": hashlib.sha256(b).hexdigest(),
            "bytes": len(b),
            "mode": stat.S_IMODE(p.stat().st_mode),
        }
    return result


def seed_terms():
    terms, groups = [], []
    group = None
    for line in (HERE / "seed-terms.txt").read_text().splitlines():
        if line.startswith("@"):
            key, label = line[1:].split("|", 1)
            group = {"id": key, "label": label, "term_ids": []}
            groups.append(group)
        elif line.strip():
            for raw in line.split(";"):
                term_id = f"FIT{len(terms) + 1:03d}"
                pair = raw.split(" — ", 1)
                ko, en = pair[0], pair[1] if len(pair) > 1 else ""
                query_variants = [ko, en]
                query_variants += re.split(r" / |·", ko)
                if " / " in en:
                    query_variants += en.split(" / ")
                terms.append({"id": term_id, "group": group["id"],
                              "source_term": raw, "ko": ko, "en": en,
                              "query_variants": list(dict.fromkeys(x for x in query_variants if x))})
                group["term_ids"].append(term_id)
    assert len(terms) == 513, len(terms)
    return terms, groups


def main():
    import prompt_generator as pg

    started = datetime.now(ZoneInfo("Asia/Seoul")).isoformat()
    manifest = json.loads((ASSETS / "photo_prompt_source_manifest.json").read_text())
    source_paths = [ASSETS / s["file"] for s in manifest["sources"] if (ASSETS / s["file"]).is_file()]
    source_paths += [ASSETS / name for name in ["photo_prompt_source_manifest.json", "photo_prompt_tags.json", "photo_prompt_visual_obligations.json"]]
    source_paths += [SKILL / "scripts" / name for name in ["prompt_generator.py", "photo_candidate_semantics.py", "photo_source_manifest.py", "photo_visual_retrieval.py"]]
    source_paths = sorted(set(source_paths))
    before = snap(source_paths)
    status = subprocess.check_output(["git", "status", "--porcelain=v1", "-z"], cwd=ROOT).decode().split("\0")
    dirty = [x for x in status if x and "fashion-fit-20261008" not in x]
    tracked_dirty_paths = [ROOT / x[3:] for x in dirty if x[:2] != "??" and (ROOT / x[3:]).is_file()]
    dirty_before = snap(tracked_dirty_paths)
    data = pg.load_json(ASSETS / "photo_prompt_tags.json")
    registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
    candidates = []
    for slot, entries in data["slots"].items():
        for entry in entries:
            fields = pg.semantic_bm25f_fields_for_entry(entry, slot)
            # slot context is a routing field, not term meaning.
            text = normalize(" ".join(v for k, values in fields.items() if k != "slot_context" for v in values))
            candidates.append({"id": entry["id"], "slot": slot, "ko": entry.get("ko"),
                               "en": entry.get("en"), "text": text,
                               "concept_units": entry.get("concept_units", []),
                               "relations": entry.get("relations", []),
                               "affected_properties": entry.get("affected_properties", [])})
    profiles = [{"id": p["id"], "category": p.get("category"),
                 "text": normalize(pg.positive_visual_profile_text(p)),
                 "definition": (p.get("semantics") or {}).get("definition"),
                 "activation": p.get("activation"),
                 "affected_dimensions": p.get("affected_dimensions", [])}
                for p in registry["profiles"]]
    terms, groups = seed_terms()
    for t in terms:
        hits = {"candidates": [], "profiles": []}
        variants = [(v, normalize(v)) for v in t["query_variants"] if normalize(v)]
        for label, rows in [("candidates", candidates), ("profiles", profiles)]:
            for row in rows:
                matched = [raw for raw, q in variants if f" {q} " in f" {row['text']} "]
                if matched:
                    hits[label].append({"id": row["id"], "slot": row.get("slot"), "matched": matched})
        t["positive_field_mentions"] = hits
        t["coverage_claim"] = "lexical_only_not_semantic_support"
    after = snap(source_paths)
    changed = [p for p in before if before[p] != after[p]]
    dump("source-snapshot.json", {
        "started_at_kst": started, "completed_at_kst": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip(),
        "manifest_source_counts": dict(collections.Counter(s["kind"] for s in manifest["sources"])),
        "source_files": before, "changed_during_load": changed,
        "preexisting_git_status": dirty, "tracked_dirty_files": dirty_before,
        "compiled_counts": {"slots": len(data["slots"]), "candidates": len(candidates),
                            "semantic_documents": len(list(pg.iter_semantic_entries(data))),
                            "profiles": len(profiles), "bundles": len(data.get("candidate_bundles", []))},
        "candidate_field_counts": {k: sum(bool(c[k]) for c in candidates)
                                   for k in ["concept_units", "relations", "affected_properties"]},
        "scope": "working_tree_authored_data_including_preexisting_changes",
        "runtime_dispatch_executed": False, "embedding_calls": 0, "image_calls": 0,
    })
    dump("term-inventory.json", {"origin": {"conversation_id": "6ac663bd-9f50-83e8-9f1d-d9cc4afbe32f",
        "conversation_title": "패션 핏 용어 조사", "read_thread_message_truncated_at": 20000,
        "complete_browser_dom_read": True, "source_vocabulary_sections": 21,
        "source_vocabulary_rows": 513, "source_comparison_rows": 14, "source_combination_rows": 6,
        "extraction": "first-column labels from rendered source tables; original definitions are not copied"},
        "groups": groups, "terms": terms,
        "limitations": ["Aliases within one source row do not count as separate terms.",
                        "Positive-field mention does not prove semantic equivalence, live retrieval, activation or rendered pixels.",
                        "Generic single-word variants can have many unrelated mentions.",
                        "Absence of a phrase is not absence of the underlying visual meaning."]})
    scoped_records = {}
    for label, rows in [("candidates", candidates), ("profiles", profiles)]:
        selected_ids = set()
        for term in terms:
            hits = term["positive_field_mentions"][label]
            if len(hits) <= 24:
                selected_ids.update(h["id"] for h in hits)
        scoped_records[label] = [{k: v for k, v in row.items() if k != "text"}
                                 for row in rows if row["id"] in selected_ids]
    scoped_records["scope"] = "Records mentioned by a seed with at most 24 hits; scores, vectors and full search text are omitted."
    dump("current-positive-records.json", scoped_records)
    print(json.dumps({"counts": {"terms": len(terms), "candidates": len(candidates), "profiles": len(profiles)},
        "source_changed_during_load": changed,
        "terms_with_candidate_mentions": sum(bool(t["positive_field_mentions"]["candidates"]) for t in terms),
        "terms_with_profile_mentions": sum(bool(t["positive_field_mentions"]["profiles"]) for t in terms)}, ensure_ascii=False))
    if changed:
        raise SystemExit("Source changed during inventory; do not use this snapshot as a stable measurement.")


if __name__ == "__main__":
    main()
