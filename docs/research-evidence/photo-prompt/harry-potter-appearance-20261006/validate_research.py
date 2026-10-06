#!/usr/bin/env python3
"""Validate research references and source preservation, not runtime or pixels."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
from visual_profile_contracts import compile_visual_profile
import prompt_generator as pg


def load(name):
    return json.loads((OUT / name).read_text())


def identity(rows):
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids)), "duplicate IDs"
    return set(ids)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    # Parsing and cross-references are independent of the builder assertions.
    json_files = sorted(p for p in OUT.glob("*.json") if p.name != "VALIDATION.json")
    for path in json_files:
        json.loads(path.read_text())
    seeds = load("SEED-INVENTORY.json")["rows"]
    sources = load("SOURCES.json")
    source_rows = sources["sources"] if isinstance(sources, dict) else sources
    units = load("SEMANTIC-UNITS.json")["units"]
    candidates = load("CANDIDATE-DRAFTS.json")["candidates"]
    mappings = load("RUNTIME-MAPPING.json")["mappings"]
    coverage = load("SEED-COVERAGE.json")["rows"]
    bundles = load("BUNDLE-DRAFTS.json")["bundles"]
    regressions = load("REGRESSION-PLAN.json")
    pixels = load("PIXEL-QUALIFICATION-PLAN.json")
    prototypes = load("PROFILE-PROTOTYPES.json")["prototypes"]
    catalog = load("EXISTING-DATA-CATALOG.json")
    snapshot = load("CHECKOUT-SNAPSHOT.json")
    seed_ids, source_ids, unit_ids = identity(seeds), identity(source_rows), identity(units)
    candidate_ids = identity(candidates)
    assert seed_ids == {f"ref_{n:03d}" for n in range(1, 150)}
    assert unit_ids == {f"H{n:03d}" for n in range(1, 121)}
    assert len(source_rows) == 46 and len(candidates) == 111 and len(bundles) == 8
    assert identity(coverage) == seed_ids
    assert {r["semantic_id"] for r in mappings} == unit_ids and len(mappings) == 120
    assert identity(bundles) == {f"B{n:02d}" for n in range(1, 9)}
    profile_ids = {r["id"] for r in catalog["profiles"]}
    entry_ids = {r["id"] for r in catalog["candidates"]}
    for row in units:
        assert set(row["seed_refs"]) <= seed_ids
        assert set(row["source_refs"]) <= source_ids
        assert len(row["components"]) == 3 and row["relations"]
        assert all(len(r["observable_predicate_en"].split()) >= 5 for r in row["components"])
        assert {r["id"] for r in row["existing_links"]["profiles"]} <= profile_ids
        assert {r["id"] for r in row["existing_links"]["candidates"]} <= entry_ids
        for relation in row["relations"]:
            assert relation["subject"] and relation["object"] and relation["type"]
            assert relation["owner_binding"]
    for row in coverage:
        assert set(row["mapped_semantic_ids"]) <= unit_ids
        actual = {u["id"] for u in units if row["id"] in u["seed_refs"]}
        assert actual == set(row["mapped_semantic_ids"]) and actual
        assert set(row["source_refs_for_verified_scope"]) <= source_ids
        assert row["whole_seed_row_verified"] is False
    banned = re.compile(
        r"\b(?:Harry|Potter|Hogwarts|Malfoy|Draco|Dumbledore|Hermione|Narcissa|"
        r"Gryffindor|Ravenclaw|Slytherin|Hufflepuff|Voldemort|Lockhart)\b|"
        r"해리포터|말포이|헤르미온느|슬리데린|래번클로|호그와트|"
        r"https?://|\bS\d{2}\b|\bH\d{3}\b|RESEARCH_DRAFT|rather than|instead of", re.I
    )
    for row in candidates:
        assert row["semantic_id"] in unit_ids
        assert row["adoption_ready"] is False
        assert set(row["source_refs"]) <= source_ids
        assert not banned.search(row["positive_retrieval_text"]), row["id"]
        assert row["adoption_constraints"]["default_optional"] is True
    for row in bundles:
        assert set(row["semantic_members"]) <= unit_ids
        assert set(row["member_draft_ids"]) <= candidate_ids
        assert row["primary_relation"] in row["semantic_members"]
        assert row["candidate_only"] and row["no_hard_activation_by_association"]
    assert len(regressions["cases"]) == 1080 and regressions["independent_holdouts"] == 0
    identity(regressions["cases"])
    for row in regressions["cases"]:
        assert row["semantic_id"] in unit_ids and row["status"] == "PLANNED_NOT_EXECUTED"
    assert len(pixels["case_groups"]) == 20 and pixels["native_generations_run"] == 0
    identity(pixels["case_groups"])
    for row in pixels["case_groups"]:
        assert set(row["semantic_ids"]) <= unit_ids
        assert row["pixel_policy"]["hidden_required"] == "UNOBSERVABLE_NOT_PASS"
    projection = []
    for row in prototypes:
        assert row["semantic_id"] in unit_ids
        result = compile_visual_profile(row["profile"])
        assert len(result["required_evidence_fields"]) == len(result["render_gates"]) == 3
        assert result["semantics"]["component_semantics"]["minimum_component_groups"] == 3
        projection.append({"semantic_id": row["semantic_id"], "profile_id": result["id"],
                           "status": "PASS_COMPILER_PROJECTION_ONLY", "evidence_fields": result["required_evidence_fields"],
                           "gate_ids": [g["id"] for g in result["render_gates"]],
                           "runtime_registry_adoption": "NOT_PERFORMED"})
    assert len(projection) == 3
    hash_checks = {}
    for kind in ("source_hashes", "generated_index_hashes"):
        changed = [name for name, expected in snapshot[kind].items()
                   if not (ROOT / name).exists() or sha(ROOT / name) != expected]
        hash_checks[kind] = {"status": "UNCHANGED" if not changed else "DRIFT_REQUIRES_REFRESH",
                            "files_compared": len(snapshot[kind]), "changed_paths": changed}
    live_registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
    live_profiles = {p["id"] for p in live_registry["profiles"]}
    live_entries = set()
    for path in [SKILL / "assets/photo_prompt_tags.json", *sorted((SKILL / "assets").glob("photo_prompt*extension*.json"))]:
        for rows in json.loads(path.read_text()).get("slots", {}).values():
            live_entries.update(r["id"] for r in rows)
    assert all({r["id"] for r in u["existing_links"]["profiles"]} <= live_profiles for u in units)
    assert all({r["id"] for r in u["existing_links"]["candidates"]} <= live_entries for u in units)
    # Only local document links are checked here; this does not re-verify web facts.
    local_links = 0
    for path in OUT.glob("*.md"):
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", path.read_text()):
            target = target.strip("<>")
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            target = target.split("#")[0]
            if not target:
                continue
            # VALIDATION.json is written below after all checks succeed.
            assert (path.parent / target).exists() or target == "VALIDATION.json", (path.name, target)
            local_links += 1
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    current_status = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
    research_prefix = str(OUT.relative_to(ROOT)) + "/"
    def external_status(value):
        return sorted(line for line in value.splitlines() if research_prefix not in line)
    report = {
        "schema_version": "harry-potter-research-validation/v1",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "research_structure": "PASS",
        "counts": {"json_files_parsed": len(json_files), "seed_rows": len(seeds), "semantic_units": len(units),
                   "source_records": len(source_rows), "candidate_drafts": len(candidates), "bundle_drafts": len(bundles),
                   "planned_regressions_not_executed": len(regressions["cases"]), "planned_pixel_groups_not_executed": len(pixels["case_groups"]),
                   "local_links_checked": local_links},
        "reference_checks": {"seed_coverage": "149/149_RECEIVED_ROWS", "semantic_source_refs": "PASS", "existing_ids_in_live_authored_data": "PASS",
                             "positive_retrieval_reserved_name_url_status_id_check": "PASS", "drafts_still_optional_and_unadopted": "PASS"},
        "prototype_compiler_projections": projection,
        "preservation": {"baseline_head": snapshot["head"], "head_now": head, "head_unchanged": head == snapshot["head"],
                         "git_status_outside_research_unchanged": external_status(current_status) == external_status(snapshot["status_porcelain"]), **hash_checks},
        "limits": ["Structural checks do not prove source facts, runtime schema acceptance, complete activation, owner/effect validity or retrieval quality.",
                   "Hash preservation covers the frozen 98 source/code files and two index manifests, not every existing untracked file or shard.",
                   "All 149 source rows retain whole_seed_row_verified=false; only selected facts have been rechecked.",
                   "Generic fallback relations still require explicit endpoint mapping before adoption.",
                   "The 1080 case specifications are derived from these same research cards, not executed tests or independent holdouts."],
        "runtime_authored_adoption": "NOT_PERFORMED", "index_rebuild_or_qualification": "NOT_PERFORMED",
        "candidate_pack_exposure_or_selection": "NOT_PERFORMED", "full_runtime_regression_suite": "NOT_PERFORMED",
        "native_generation": "NOT_PERFORMED", "user_judgment": "pending",
        "research_package_hashes": {str(p.relative_to(OUT)): sha(p) for p in sorted(OUT.iterdir())
                                    if p.is_file() and p.name != "VALIDATION.json"},
    }
    (OUT / "VALIDATION.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"research_structure": report["research_structure"], "counts": report["counts"],
                      "source_preservation": hash_checks, "compiler_projections": len(projection)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
