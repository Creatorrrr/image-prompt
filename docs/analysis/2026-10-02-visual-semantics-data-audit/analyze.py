"""Reproduce the local visual-semantics inventory; never changes runtime assets.

Run with the bundled workspace Python (NumPy is used only for vector pairs).
Counts describe authored/compiled records, not image quality or usage frequency.
"""
from __future__ import annotations

import ast
import collections
import csv
import hashlib
import json
import math
import re
import statistics
import subprocess
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", str(text)).casefold().split())


def has_ko(text):
    return bool(re.search(r"[가-힣]", str(text)))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(values):
    values = sorted(values)
    if not values:
        return {"n": 0}
    def quantile(p):
        i = (len(values) - 1) * p
        lo = int(i)
        hi = math.ceil(i)
        return values[lo] + (values[hi] - values[lo]) * (i - lo)
    return {"n": len(values), "sum": sum(values), "min": values[0],
            "median": statistics.median(values), "p90": quantile(.9),
            "p95": quantile(.95), "max": values[-1],
            "mean": statistics.mean(values)}


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def csv_out(name, rows):
    with (OUT / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def duplicate_groups(rows):
    return [{"value": key, "profile_ids": sorted(set(ids)), "n": len(set(ids))}
            for key, ids in rows.items() if len(set(ids)) > 1]


def historical_inventory(revision):
    prefix = "skills/photo-prompt-image-generator/"
    code = git("show", f"{revision}:{prefix}scripts/prompt_generator.py")
    filenames = []
    for node in ast.parse(code).body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "VISUAL_OBLIGATION_EXTENSION_FILENAMES"
            for t in node.targets
        ):
            filenames = list(ast.literal_eval(node.value))
    tree = set(git("ls-tree", "-r", "--name-only", revision, prefix + "assets").splitlines())
    counts = {}
    for filename in ["photo_prompt_visual_obligations.json", *filenames]:
        path = prefix + "assets/" + filename
        if path in tree:
            counts[filename] = len(json.loads(git("show", f"{revision}:{path}"))["profiles"])
    return {"commit": git("rev-parse", revision),
            "committed_at": git("show", "-s", "--format=%cI", revision),
            "profiles": sum(counts.values()), "files": len(counts), "file_counts": counts}


def main():
    started = time.monotonic()
    print("Load authored records", flush=True)
    files = [ASSETS / pg.VISUAL_OBLIGATION_REGISTRY_FILENAME] + [
        ASSETS / f for f in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES if (ASSETS / f).exists()]
    raw = []
    source_by_id = {}
    for path in files:
        for profile in json.loads(path.read_text())["profiles"]:
            raw.append(profile)
            source_by_id[profile["id"]] = path.name
    registry = pg.load_visual_obligation_registry(files[0])
    profiles = registry["profiles"]
    by_id = {p["id"]: p for p in profiles}
    index_path = ASSETS / pg.VISUAL_PROFILE_INDEX_FILENAME
    index = json.loads(index_path.read_text())
    print("Validate existing index without API calls", flush=True)
    pg.validate_visual_profile_index_metadata(index, registry)
    inventory = []
    categories = collections.Counter()
    exact_owners = collections.defaultdict(list)
    definition_owners = collections.defaultdict(list)
    positive_owners = collections.defaultdict(list)
    gate_owners = collections.defaultdict(list)
    by_file = collections.defaultdict(list)
    for p in profiles:
        pid = p["id"]
        semantics = p["semantics"]
        groups = semantics["component_semantics"]["groups"]
        exact = p["activation"]["exact_terms"]
        aliases = p["activation"].get("project_glossary_aliases", [])
        for term in exact + aliases:
            exact_owners[norm(term)].append(pid)
        definition_owners[norm(semantics["definition"])].append(pid)
        positive_owners[norm(pg.visual_profile_semantic_text(p))].append(pid)
        for gate in p["render_gates"]:
            gate_owners[gate["id"]].append(pid)
        categories[p["category"]] += 1
        words = [len(t.split()) for t in exact]
        discovery = p["activation"].get("semantic_discovery_requires_component_evidence") is True
        required = set(semantics["component_semantics"].get("required_group_ids", []))
        group_ko = [any(has_ko(t) for t in g["any_terms"]) for g in groups]
        row = {
            "profile_id": pid, "source_file": source_by_id[pid], "category": p["category"],
            "authored_components": "authored_components" in p,
            "component_groups": len(groups), "minimum_component_groups": semantics["component_semantics"]["minimum_component_groups"],
            "all_groups_required": len(required) == len(groups),
            "evidence_fields": len(p["required_evidence_fields"]), "render_gates": len(p["render_gates"]),
            "exact_terms": len(exact), "project_aliases": len(aliases),
            "exact_has_korean": any(has_ko(t) for t in exact + aliases),
            "semantic_text_has_korean": has_ko(pg.visual_profile_semantic_text(p)),
            "component_groups_with_korean": sum(group_ko),
            "all_component_groups_have_korean": all(group_ko),
            "exact_min_words": min(words), "exact_max_words": max(words),
            "all_exact_terms_10plus_words": all(w >= 10 for w in words),
            "exact_includes_complete_definition": norm(semantics["definition"]) in {norm(t) for t in exact},
            "paraphrases": len(semantics["paraphrase_examples"]),
            "contrasts": len(semantics["contrast_examples"]), "reject_substitutes": len(p["reject_substitutes"]),
            "has_claim_limits": bool(semantics.get("claim_limits")),
            "has_context_disambiguation": bool(p["activation"].get("context_disambiguation")),
            "has_hard_activation": bool(p["activation"].get("hard_activation")),
            "requires_component_evidence_for_discovery": discovery,
            "has_core_assertion_discovery": p["concept_candidate"].get("core_assertion_discovery") is True,
            "has_affected_dimensions": bool(p["concept_candidate"].get("affected_dimensions")),
            "has_affected_properties": bool(p["concept_candidate"].get("affected_properties")),
            "requires_adult_context": p["activation"].get("requires_adult_character") is True,
            "runtime_mode": p["runtime_expression"]["default_mode"],
            "has_runtime_forbidden_labels": bool(p["runtime_expression"].get("runtime_forbidden_labels")),
            "has_typed_visual_relation": isinstance(p.get("visual_relation"), dict),
        }
        inventory.append(row)
        by_file[row["source_file"]].append(row)
    file_rows = []
    for filename, rows in by_file.items():
        file_rows.append({"source_file": filename, "profiles": len(rows),
            "share_pct": round(100 * len(rows) / len(profiles), 3),
            "component_groups": sum(r["component_groups"] for r in rows),
            "median_components": statistics.median(r["component_groups"] for r in rows),
            "render_gates": sum(r["render_gates"] for r in rows),
            "median_gates": statistics.median(r["render_gates"] for r in rows),
            "exact_lookup_rows": sum(r["exact_terms"] + r["project_aliases"] for r in rows),
            "profiles_with_korean_exact": sum(r["exact_has_korean"] for r in rows),
            "profiles_with_korean_semantic_text": sum(r["semantic_text_has_korean"] for r in rows),
            "profiles_with_all_korean_component_groups": sum(r["all_component_groups_have_korean"] for r in rows),
            "component_discovery_guard": sum(r["requires_component_evidence_for_discovery"] for r in rows),
            "median_exact_min_words": statistics.median(r["exact_min_words"] for r in rows)})
    file_rows.sort(key=lambda r: -r["profiles"])
    category_rows = [{"category": k, "profiles": v, "share_pct": round(100*v/len(profiles), 3)}
                     for k, v in categories.most_common()]
    csv_out("profile-inventory.csv", inventory)
    csv_out("source-distribution.csv", file_rows)
    csv_out("category-distribution.csv", category_rows)
    flags = {key: sum(row[key] is True for row in inventory)
             for key in inventory[0] if isinstance(inventory[0][key], bool)}
    gate_scale = collections.Counter(g["review_scale"] for p in profiles for g in p["render_gates"])
    metrics = {
        "captured_at_kst": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
        "commit": git("rev-parse", "HEAD"), "grain": "one compiled visual profile, not one keyword or rendered image",
        "totals": {"files": len(files), "raw_profiles": len(raw), "compiled_profiles": len(profiles),
            "unique_profile_ids": len(by_id), "categories": len(categories),
            "single_profile_categories": sum(v == 1 for v in categories.values()),
            "exact_lookup_rows": len(index["exact_lookup"]), "unique_normalized_exact_terms": len(exact_owners),
            "index_entries": len(index["entries"]),
            "component_groups": sum(r["component_groups"] for r in inventory),
            "evidence_fields": sum(r["evidence_fields"] for r in inventory),
            "render_gates": sum(r["render_gates"] for r in inventory)},
        "profile_flags": flags,
        "summaries": {key: summary([r[key] for r in inventory]) for key in [
            "component_groups", "evidence_fields", "render_gates", "exact_terms", "exact_min_words", "paraphrases"]},
        "gate_review_scales": dict(gate_scale),
        "runtime_modes": dict(collections.Counter(r["runtime_mode"] for r in inventory)),
        "source_distribution": file_rows, "category_distribution": category_rows,
        "structure_checks": {"registry_index_metadata_check": "pass",
            "registry_hash_matches": pg.visual_profile_registry_sha256(registry) == index["registry_sha256"],
            "duplicate_profile_ids": len(raw) - len({p['id'] for p in raw}),
            "cross_profile_gate_id_collisions": len(duplicate_groups(gate_owners)),
            "exact_term_collision_groups": len(duplicate_groups(exact_owners))},
        "discovery_guard_details": {
            "guarded_profiles": sum(r["requires_component_evidence_for_discovery"] for r in inventory),
            "guarded_with_no_korean_component_terms": sum(r["requires_component_evidence_for_discovery"] and r["component_groups_with_korean"] == 0 for r in inventory),
            "guarded_with_all_groups_required": sum(r["requires_component_evidence_for_discovery"] and r["all_groups_required"] for r in inventory)},
        "duplicates": {"definitions": duplicate_groups(definition_owners),
            "positive_texts": duplicate_groups(positive_owners), "exact_terms": duplicate_groups(exact_owners),
            "gate_ids": duplicate_groups(gate_owners)},
        "limitations": ["Population is the local photo skill registry, not usage logs.",
            "Counts have mixed semantic granularity; shares do not establish coverage or user demand.",
            "Hangul detection measures authored Korean text, not multilingual embedding comprehension.",
            "Similar vectors are review leads, not automatic duplicate judgments.",
            "No embedding API, image generation, pixel review, or runtime data changes."]}
    self_conflicts = []
    for p in profiles:
        context = "; ".join(g["any_terms"][0] for g in p["semantics"]["component_semantics"]["groups"])
        eligible, reason = pg.visual_profile_context_applicability(
            p, context, has_authorial_core_context=True, require_positive_context_terms=False)
        if not eligible:
            excluded = list(p["activation"].get("exclude_if_any_terms", []))
            excluded += list((p["activation"].get("context_disambiguation") or {}).get("exclude_if_any_terms", []))
            terms = [t for t in excluded if pg.intent_alias_matches(context, t)]
            self_conflicts.append({"profile_id": p["id"], "reason": reason,
                                   "matched_exclusion_terms": terms, "source_component_context": context})
    metrics["source_component_context_conflicts"] = self_conflicts
    dump("source-component-context-conflicts.json", self_conflicts)
    print("Compare stored embedding vectors", flush=True)
    try:
        import numpy as np
        ids = list(index["entries"])
        matrix = np.array([index["entries"][pid]["vector"] for pid in ids], dtype=np.float64)
        finite_rows = np.isfinite(matrix).all(axis=1)
        lengths = np.linalg.norm(matrix, axis=1)
        valid = finite_rows & (lengths > 0)
        unit = matrix / np.where(valid, lengths, 1)[:, None]
        similarities = unit @ unit.T
        a, b = np.triu_indices(len(ids), 1)
        values = similarities[a, b]
        selected = np.flatnonzero(values >= .95)
        selected = selected[np.argsort(-values[selected])]
        pairs = [{"left": ids[a[i]], "right": ids[b[i]], "cosine": round(float(values[i]), 8),
                  "same_source": source_by_id[ids[a[i]]] == source_by_id[ids[b[i]]],
                  "left_definition": by_id[ids[a[i]]]["semantics"]["definition"],
                  "right_definition": by_id[ids[b[i]]]["semantics"]["definition"]} for i in selected]
        metrics["vector_checks"] = {"dimensions": matrix.shape[1], "finite_nonzero_rows": int(valid.sum()),
            "pair_counts_by_threshold": {str(t): int((values >= t).sum()) for t in [.9, .95, .97, .99, .999]},
            "highest_pairs": pairs[:30]}
        dump("near-duplicate-vector-pairs.json", pairs)
    except ImportError:
        metrics["vector_checks"] = {"status": "not_run_numpy_unavailable"}
    print("Compare committed source snapshots", flush=True)
    metrics["git_snapshots"] = [historical_inventory(r) for r in ["c3f35a85", "b8378429", "89384cd9", "a1e08cc0", "HEAD"]]
    manifest_paths = [*files, index_path, SKILL / "scripts/prompt_generator.py",
                      SKILL / "scripts/visual_profile_contracts.py", SKILL / "scripts/photo_visual_retrieval.py",
                      SKILL / "scripts/bm25f_retrieval.py", SKILL / "references/retrieval-contract.md",
                      SKILL / "references/maintenance.md"]
    dump("source-manifest.json", {"commit": metrics["commit"], "captured_at_kst": metrics["captured_at_kst"],
         "files": [{"path": str(p.relative_to(ROOT)), "sha256": sha(p), "bytes": p.stat().st_size} for p in manifest_paths]})
    dump("metrics.json", metrics)
    print(json.dumps({"totals": metrics["totals"], "flags": flags,
        "discovery": metrics["discovery_guard_details"], "checks": metrics["structure_checks"],
        "vectors": {k:v for k,v in metrics.get("vector_checks", {}).items() if k != "highest_pairs"},
        "seconds": round(time.monotonic()-started, 2)}, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
