"""Read a pinned Git object snapshot; write research evidence only.

This audit never opens working-tree asset JSON, never modifies runtime data,
and does not measure resolver recall, image quality, or human emotion.
"""
from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
COMMIT = "0adb5f6e56416e2656dfb4150d0724867530c2bc"
SKILL = "skills/photo-prompt-image-generator"
ASSETS = f"{SKILL}/assets"
SCRIPTS = f"{SKILL}/scripts"


def git_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{COMMIT}:{path}"], cwd=ROOT)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write(name: str, data: object) -> None:
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def fields_text(row: dict) -> str:
    # Positive visible-language fields only. Do not use candidate IDs,
    # contextual interpretive readings, negatives, or provenance as evidence.
    values = []
    for key in ("ko", "en", "aliases", "keywords", "paraphrases", "concept_units"):
        value = row.get(key, [])
        values.extend([value] if isinstance(value, str) else value)
    for relation in row.get("relations", []):
        values.extend(str(relation.get(k, "")) for k in ("subject", "type", "object"))
    return " | ".join(x for x in values if isinstance(x, str))


def term_hit(term: str, text: str) -> bool:
    # A lexical inventory diagnostic, deliberately not the runtime matcher.
    # English boundaries avoid AU1 matching AU10 and lip matching lipstick.
    escaped = re.escape(term.casefold())
    if re.fullmatch(r"[a-z0-9][a-z0-9 '’\-/]*", term.casefold()):
        return bool(re.search(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])", text.casefold()))
    return term.casefold() in text.casefold()


def main() -> None:
    manifest: dict[str, dict] = {}

    def read_asset(name: str) -> dict:
        path = f"{ASSETS}/{name}"
        data = git_bytes(path)
        manifest[path] = {"sha256": sha(data), "bytes": len(data)}
        return json.loads(data)

    source = git_bytes(f"{SCRIPTS}/prompt_generator.py")
    constants: dict[str, object] = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            try:
                constants[name] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                if isinstance(node.value, ast.Tuple):
                    items = []
                    for item in node.value.elts:
                        if isinstance(item, ast.Name) and item.id in constants:
                            items.append(constants[item.id])
                        else:
                            try:
                                items.append(ast.literal_eval(item))
                            except (ValueError, TypeError):
                                break
                    else:
                        constants[name] = tuple(items)

    # The imported pure compilers must match the pinned source exactly.
    # Refuse a mixed-revision audit if another task changes these scripts.
    for name in ("prompt_generator.py", "visual_profile_contracts.py", "photo_visual_retrieval.py", "photo_candidate_semantics.py", "photo_contracts.py"):
        path = f"{SCRIPTS}/{name}"
        frozen = git_bytes(path)
        live = (ROOT / path).read_bytes()
        if frozen != live:
            raise RuntimeError(f"Compiler differs from pinned revision: {path}")
        manifest[path] = {"sha256": sha(frozen), "bytes": len(frozen), "working_tree_matches_pinned": True}
    sys.path.insert(0, str(ROOT / SCRIPTS))
    import prompt_generator as generator
    from photo_visual_retrieval import positive_visual_profile_text
    from visual_profile_contracts import compile_visual_profile

    registry_files = [constants["VISUAL_OBLIGATION_REGISTRY_FILENAME"], *constants["VISUAL_OBLIGATION_EXTENSION_FILENAMES"]]
    profile_sources = {}
    profiles = []
    for name in registry_files:
        rows = read_asset(name)["profiles"]
        for row in rows:
            profile_sources[row["id"]] = name
            profiles.append(compile_visual_profile(row))
    ids = [row["id"] for row in profiles]
    assert len(ids) == len(set(ids))

    data = read_asset("photo_prompt_tags.json")
    for name in constants["RESEARCH_EXTENSION_FILENAMES"]:
        data = generator.merge_research_extension(data, read_asset(name))
    entries = [(slot, row) for slot, rows in data["slots"].items() for row in rows]
    expression = data["slots"].get("expression", [])
    relevant_ids = {
        "achievement_reward_smile", "affiliative_reassurance_smile", "decision_uncertainty_display",
        "embarrassment_repair_display", "verified_safety_relief", "contained_affect_self_presentation", "mep_gaze_target",
        "pv_profile_eyes_closed", "pv_profile_half_lidded", "pv_profile_smile_closed", "pv_profile_smile_teeth",
        "pv_profile_asymmetric_mouth", "pv_profile_parted_lips", "pv_profile_puffed_cheeks", "pv_profile_raised_brows", "pv_profile_wink",
    }
    relevant = [{"id": row["id"], "source": profile_sources[row["id"]], "activation": row["activation"],
                 "definition": row["semantics"]["definition"],
                 "required_component_groups": row["semantics"].get("component_semantics", {}).get("required_group_ids", []),
                 "render_gates": row.get("render_gates", [])} for row in profiles if row["id"] in relevant_ids]
    queries = ["smize", "squinch", "side-eye", "smirk", "sneer", "coy", "coquettish", "sultry", "smoldering", "smouldering",
               "lip pressing", "lip tightening", "lip bite", "half-lidded", "Duchenne", "deadpan", "double take", "microexpression", "AU24",
               "눈물 참기", "입틀막", "동공지진", "억눌린 분노", "입을 다문 미소", "한쪽 눈만 닫힌 윙크"]
    diagnostics = []
    for term in queries:
        diagnostics.append({
            "query": term,
            "exact_profile_ids": [row["id"] for row in profiles if any(term.casefold() == x.casefold() for x in row["activation"].get("exact_terms", []) + row["activation"].get("project_glossary_aliases", []))],
            "positive_profile_text_ids": [row["id"] for row in profiles if term_hit(term, positive_visual_profile_text(row))],
            "positive_candidate_ids": [f"{slot}.{row['id']}" for slot, row in entries if term_hit(term, fields_text(row))],
        })
    inventory = json.loads((HERE / "SOURCE-TERM-GROUPS.json").read_text())
    coverage = []
    for table in inventory["tables"]:
        for index, cell in enumerate(table["term_rows"]):
            terms = [x.strip() for x in cell.split(",") if x.strip()]
            profile_hits = {x["id"] for x in profiles if any(term_hit(t, positive_visual_profile_text(x)) for t in terms)}
            candidate_hits = {f"{slot}.{x['id']}" for slot, x in entries if any(term_hit(t, fields_text(x)) for t in terms)}
            coverage.append({"source_row_id": f"t{table['table_index']:02d}_r{index:02d}", "section": table["section"], "terms": terms,
                             "term_kind": table["term_kind"], "positive_profile_text_ids": sorted(profile_hits),
                             "positive_candidate_ids": sorted(candidate_hits),
                             "interpretation": "lexical_surface_hit_only; no semantic coverage, ranking, activation, prompt, or pixel verdict"})
    write("CURRENT-DATA-AUDIT.json", {
        "schema_version": "acting-research-current-data-audit/v1", "source_commit": COMMIT,
        "registry_files": registry_files, "registry_profile_count": len(profiles), "unique_profile_ids": len(set(ids)),
        "candidate_extension_files": list(constants["RESEARCH_EXTENSION_FILENAMES"]), "candidate_entry_count": len(entries),
        "slot_counts": {k: len(v) for k, v in data["slots"].items()},
        "candidate_semantic_policy": data.get("candidate_semantic_policy"),
        "expression_count": len(expression),
        "expression_semantic_fields": {k: sum(k in x for x in expression) for k in ("concept_units", "relations", "affected_dimensions", "affected_properties", "contextual_usage")},
        "expression_rows": [{k: x[k] for k in ("id", "ko", "en", "concept_units", "relations", "affected_dimensions", "affected_properties") if k in x} for x in expression],
        "reuse_profiles": relevant, "term_diagnostics": diagnostics,
        "character_mechanism_graph": {"schema_version": data.get("character_mechanism_graph", {}).get("schema_version"),
                                      "concept_profile_count": len(data.get("character_mechanism_graph", {}).get("concept_profiles", [])),
                                      "axis_vocabularies": data.get("character_mechanism_graph", {}).get("axis_vocabularies", {})},
        "limits": ["All counts describe the pinned commit, not the moving working tree.", "A missing label does not imply no visual or generic-assertion support.",
                   "No approximate resolver queries, candidate-pack generation, render requests, or image scoring were executed.",
                   "Existing expression candidates include fantasy, animal, historical, and contextual entries; 111 is not a count of actor facial primitives."]
    })
    write("KEYWORD-COVERAGE.json", {"source_commit": COMMIT, "rows": coverage,
                                   "limits": "A comma split is an inventory aid, not a sense merger. Lexical substring matches are discovery diagnostics only."})
    write("SOURCE-MANIFEST.json", {"source_commit": COMMIT, "files": manifest,
                                  "source_authority": "git object bytes read from pinned commit; runtime working-tree assets not used",
                                  "working_tree_status_at_audit": subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True),
                                  "head_at_audit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()})
    print(json.dumps({"commit": COMMIT, "profiles": len(profiles), "registry_files": len(registry_files),
                      "candidate_entries": len(entries), "expression": len(expression), "coverage_rows": len(coverage),
                      "source_files": len(manifest), "expression_semantic_fields": {k: sum(k in x for x in expression) for k in ("concept_units", "relations", "affected_dimensions", "affected_properties")}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
