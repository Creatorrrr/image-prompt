"""Validate the research envelope and pure draft projections, not model behavior."""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = "skills/photo-prompt-image-generator"
CHECKS = []


def read(name):
    return json.loads((HERE / name).read_text())


def check(label, condition, count=None):
    assert condition, label
    CHECKS.append(dict(check=label, status="PASS", count=count))


def main():
    audit = read("CURRENT-DATA-AUDIT.json")
    manifest = read("SOURCE-MANIFEST.json")
    pin = audit["source_commit"]

    def frozen(path):
        return subprocess.check_output(["git", "show", pin + ":" + path], cwd=ROOT)

    def asset(name):
        return json.loads(frozen(f"{SKILL}/assets/{name}"))

    for path, expected in manifest["files"].items():
        data = frozen(path)
        check("pinned source hash: " + path, hashlib.sha256(data).hexdigest() == expected["sha256"] and len(data) == expected["bytes"])
        if path.endswith(".py"):
            check("pure compiler revision: " + path, (ROOT / path).read_bytes() == data)

    sys.path.insert(0, str(ROOT / SKILL / "scripts"))
    import prompt_generator as generator
    import photo_candidate_semantics as semantics
    from visual_profile_contracts import compile_visual_profile, validate_hard_activation
    from photo_visual_retrieval import positive_visual_profile_text

    all_json = sorted(HERE.glob("*.json"))
    for path in all_json:
        json.loads(path.read_text())
    for path in HERE.glob("*.py"):
        ast.parse(path.read_text())
    check("JSON and Python syntax", True, len(all_json))

    inventory = read("SOURCE-TERM-GROUPS.json")
    decisions = read("TERM-DECISIONS.json")["rows"]
    check("13 sections, 25 tables, 368 source rows", len(inventory["tables"]) == 25 and len({t["section"] for t in inventory["tables"]}) == 13 and sum(len(t["term_rows"]) for t in inventory["tables"]) == 368, 368)
    expected_rows = {f"t{t['table_index']:02d}_r{n:02d}": term for t in inventory["tables"] for n,term in enumerate(t["term_rows"],1)}
    check("all source rows routed without dropped or altered term groups", {r["source_row_id"]:r["term_group"] for r in decisions} == expected_rows and len(decisions) == 368, 368)

    sources = read("SOURCES.json")["sources"]
    source_ids = {s["id"] for s in sources}
    check("40 unique sourced records with limits and verification scope", len(sources) == len(source_ids) == 40 and all(s["limits"] and s["supports"] and s["verification"] and s["url"].startswith("https://") for s in sources), 40)

    proposal = read("PROPOSED-DATA.json")
    concepts = proposal["concepts"]
    concept_ids = {r["id"] for r in concepts}
    check("unique concept IDs and valid source references", len(concept_ids) == len(concepts) == 64 and all(set(r["source_ids"]) <= source_ids for r in concepts), 64)
    check("nonvisual evidence modes cannot create static candidates", all(r["candidate_slot"] is None and not r["hard_profile_draft"] and not r["observable_components"] for r in concepts if r["evidence_mode"] not in {"static_form", "context_variant"}))
    check("no hidden-state or temporal claims allowed for static proposals", all(not r["hidden_state_claims_allowed"] and not r["temporal_claims_allowed"] for r in concepts))
    check("explicit sexual terms remain lexical only", next(r for r in concepts if r["id"] == "ae_explicit_terms")["evidence_mode"] == "lexical_only")

    baseline = asset("photo_prompt_tags.json")
    for name in audit["candidate_extension_files"]:
        baseline = generator.merge_research_extension(baseline, asset(name))
    baseline_ids = {(slot,r["id"]) for slot, rows in baseline["slots"].items() for r in rows}
    baseline_profile_ids = {r["id"] for name in audit["registry_files"] for r in asset(name)["profiles"]}
    reuse = read("REUSE-PLAN.json")["reuse"]
    check("11 reuse targets exist in declared slots", len(reuse) == 11 and all((r["slot"],r["existing_candidate_id"]) in baseline_ids for r in reuse), 11)
    check("verified concentration lower-lip-bite existing target", ("expression", "ctx_c126") in baseline_ids)

    ext = read("DRAFT-CANDIDATE-EXTENSION.json")
    new_rows = [(slot,r) for slot,rows in ext["slots"].items() for r in rows]
    check("38 new candidate IDs do not shadow pinned IDs", len(new_rows) == 38 and all((slot,r["id"]) not in baseline_ids for slot,r in new_rows), 38)
    check("maintenance reference hashes actual research envelope", ext["maintenance_ref"]["sha256"] == hashlib.sha256((HERE / "PROPOSED-DATA.json").read_bytes()).hexdigest())
    merged = generator.merge_research_extension(copy.deepcopy(baseline), ext)
    semantics.validate_candidate_entries(merged, generator.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
    check("candidate extension pure merge and semantic schema", sum(len(rows) for rows in merged["slots"].values()) == audit["candidate_entry_count"] + 38, 38)

    profiles = read("DRAFT-VISUAL-PROFILES.json")["profiles"]
    profile_ids = {p["id"] for p in profiles}
    check("11 new profile IDs are unique and unshadowed", len(profile_ids) == len(profiles) == 11 and not profile_ids & baseline_profile_ids, 11)
    for p in profiles:
        validate_hard_activation(p["activation"]["hard_activation"])
        compiled = compile_visual_profile(p)
        components = p["authored_components"]["components"]
        check("profile projection: " + p["id"], len(compiled["render_gates"]) == len(components) == len(compiled["required_evidence_fields"]), len(components))
        contaminated = copy.deepcopy(compiled)
        contaminated["semantics"]["contrast_examples"].append("contrast_source_leak_marker_qz")
        contaminated["semantics"]["claim_limits"].append("claim_source_leak_marker_qz")
        positive = positive_visual_profile_text(contaminated)
        check("negative surfaces excluded: " + p["id"], "source_leak_marker_qz" not in positive)
    bundles = ext["visual_semantics"]
    check("11 draft bundle profile and candidate references", len(bundles) == 11 and all(set(b["hard_profile_ids"]) <= profile_ids and all((b["candidate_slots"][cid],cid) in {(s,r['id']) for s,r in new_rows} for cid in b["candidate_ids"]) for b in bundles), 11)

    cases = [json.loads(line) for line in (HERE / "REGRESSION-CASES.jsonl").read_text().splitlines()]
    check("75 authored regression records clearly unexecuted", len(cases) == len({c["id"] for c in cases}) == 75 and all(c["observed_status"] == "not_run" and set(c["related_concept_ids"]) <= concept_ids for c in cases), 75)
    pixels = read("PIXEL-PLAN.json")["static_pairs"]
    check("11 unexecuted pixel pairs preserve evidence and result distinctions", len(pixels) == 11 and all(p["concept_id"] in concept_ids and p["execution_status"] == "NOT_RUN" and "UNOBSERVABLE" in p["result_states"] and "MODERATION_BLOCKED" in p["result_states"] for p in pixels), 11)
    for path in HERE.glob("*.md"):
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" not in target and not target.startswith("#"):
                check("local report link: " + path.name + " -> " + target, (path.parent / target.split("#")[0]).exists())

    result = dict(schema_version="acting-research-package-validation/v1", status="PASS", source_commit=pin, checks=CHECKS,
        counts=read("PACKAGE-COUNTS.json"),
        verification_boundary="JSON/Python, source hashes, draft profile projection, pure candidate schema/merge, existing IDs and report links only. No context resolver, ranking, guard runtime, semantic scenario, prompt composition, image generation or user acceptance test was executed.",
        deployment_status="not_registered; contextual guards require implementation and semantic validation")
    (HERE / "VALIDATION.json").write_text(json.dumps(result,ensure_ascii=False,indent=2) + "\n")
    print(json.dumps(dict(status=result["status"], checks=len(CHECKS), counts=result["counts"], verification_boundary=result["verification_boundary"]),ensure_ascii=False))


if __name__ == "__main__":
    main()
