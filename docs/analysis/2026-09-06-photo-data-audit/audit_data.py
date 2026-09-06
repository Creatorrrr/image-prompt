#!/usr/bin/env python3
"""Read-only data audit. Writes only the report requested with --output.

This is maintenance evidence, not a prompt-generation fixture or a holdout.
It uses the checked-in index, makes no network calls, and does not render images.
"""

from __future__ import annotations

import argparse
import ast
import collections
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata


ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as pg
from bm25f_retrieval import rank_bm25f


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    base = read(ASSETS / "photo_prompt_tags.json")
    data = pg.load_json(ASSETS / "photo_prompt_tags.json")
    registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
    index = pg.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", registry)
    recipes = read(ASSETS / "concept_recipes.json")
    profiles = registry["profiles"]
    profile_ids = {row["id"] for row in profiles}
    candidates = [(slot, row) for slot, rows in data["slots"].items() for row in rows]
    candidate_ids = {row["id"] for _, row in candidates}

    merge_ast = next(node for node in ast.parse(Path(pg.__file__).read_text()).body
                     if isinstance(node, ast.FunctionDef) and node.name == "merge_research_extension")
    consumed = sorted({node.args[0].value for node in ast.walk(merge_ast)
                       if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                       and isinstance(node.func.value, ast.Name) and node.func.value.id == "extension"
                       and node.func.attr == "get" and node.args and isinstance(node.args[0], ast.Constant)})
    extension_rows = []
    semantic_rows = []
    dangling = []
    for name in pg.RESEARCH_EXTENSION_FILENAMES:
        path = ASSETS / name
        if not path.exists():
            extension_rows.append({"file": name, "exists": False})
            continue
        payload = read(path)
        extension_rows.append({"file": name, "exists": True,
                               "keys_not_read_by_merge": sorted(set(payload) - set(consumed)),
                               "candidate_count": sum(len(rows) for rows in payload.get("slots", {}).values()),
                               "visual_semantics_count": len(payload.get("visual_semantics", []))})
        for row in payload.get("visual_semantics", []):
            semantic_rows.append({"file": name, "id": row["id"],
                                  "candidate_ids": row.get("candidate_ids", []),
                                  "hard_profile_ids": row.get("hard_profile_ids", [])})
            for field, targets in [("candidate_ids", candidate_ids), ("hard_profile_ids", profile_ids)]:
                for target in row.get(field, []):
                    if target not in targets:
                        dangling.append({"file": name, "id": row["id"], "field": field, "target": target})

    # Mutate only an in-memory copy: a supposedly linked field has no merge effect.
    extension = read(ASSETS / "photo_prompt_lighting_extension.json")
    mutated = copy.deepcopy(extension)
    mutated["visual_semantics"][0]["hard_profile_ids"] = ["audit_nonexistent_profile"]
    mutated["semantic_policy"]["hard_activation"] = "audit deliberately invalid descriptive policy"
    original_merge = pg.merge_research_extension(copy.deepcopy(base), extension)
    changed_merge = pg.merge_research_extension(copy.deepcopy(base), mutated)

    aliases = collections.defaultdict(set)
    for row in profiles:
        activation = row["activation"]
        for term in activation["exact_terms"] + activation.get("project_glossary_aliases", []):
            aliases[unicodedata.normalize("NFKC", term).casefold()].add(row["id"])
    duplicate_labels = collections.defaultdict(list)
    for slot, row in candidates:
        duplicate_labels[(slot, row.get("en", "").strip().casefold())].append(row["id"])

    # A triage heuristic, NOT a count of semantically incorrect records.
    boundary = re.compile(r"\b(?:no |not |without |rather than|never |not evidence|do not|does not|cannot |must not|nonsexual|nonexplicit)")
    flagged = [{"profile_id": row["id"], "definition_flag": bool(boundary.search(row["semantics"]["definition"])),
                "flagged_concept_terms": [term for term in row["concept_candidate"]["concept_terms"] if boundary.search(term)],
                "embedding_text_flag": bool(boundary.search(pg.visual_profile_semantic_text(row)))}
               for row in profiles]
    bm25_queries = ["health weight fertility", "fully clothed nonsexual"]
    lexical = [{"query_fields": {"active_request": query},
                "raw_top_three_before_applicability": rank_bm25f(index["bm25f"], {"active_request": query}, limit=3)}
               for query in bm25_queries]

    # Synthetic maintenance probes directly exercise the normal resolver.
    # They are not requester envelopes and do not claim full v6/render coverage.
    cases = [
        ("cabin_rest", "An adult flight attendant is resting in an aircraft cabin.",
         "An adult flight attendant sits in an aircraft cabin and reads a paperback during a quiet break."),
        ("pilot_rest", "An adult aircraft pilot rests in the aircraft cockpit.",
         "An adult aircraft pilot rests in the aircraft cockpit with hands folded and eyes closed."),
        ("underarm_secondary", "An adult runner with a small underarm tattoo ties her shoes.",
         "The adult runner bends forward to tie her shoes; her underarm tattoo is a minor detail."),
        ("underarm_product", "An adult hand holds an underarm deodorant bottle.",
         "An adult hand holds a capped underarm deodorant bottle against a plain tabletop."),
        ("rembrandt_short", "An adult portrait with Rembrandt triangle portrait light and short face-light orientation relation.",
         "An adult face turns toward an elevated side key; the narrow far cheek is lit while a small light triangle remains on the broad near shadow cheek."),
    ]
    activation_probes = []
    for name, request, context in cases:
        sources = [{"source": "user_requirement", "text": request, "polarity": "required"},
                   {"source": "authorial_core_baseline", "text": context, "polarity": "advisory"}]
        result = pg.resolve_visual_profile_hits(registry, sources, visual_profile_index=index, adult_context=True)
        activation_probes.append({"case_id": name, "source_rows": sources, "adult_context": True, "hits": result["hits"]})

    projection_examples = []
    projected_process_tag_ids = []
    selected = {"lit_clean_large_soft_key_return", "lit_clean_low_ratio_open_shadow", "lit_clean_vertical_catchlight_pair"}
    for slot, row in candidates:
        if any(tag.endswith("_visual_semantics") for tag in pg.candidate_pack_public_tags(data, row)):
            projected_process_tag_ids.append(f"{slot}:{row['id']}")
        if row["id"] in selected:
            candidate, _ = pg.candidate_pack_summarize_slot_candidate(data, slot, {"id": row["id"]}, 0.0, "")
            pg.candidate_pack_v4_project_candidate(candidate, salt=candidate["id"])
            projection_examples.append({"authored": row, "public_projection": candidate})

    categories = collections.Counter(row["category"] for row in profiles)
    report = {
        "report_kind": "maintenance_data_diagnosis_not_render_acceptance",
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "scope": "All merged profile/slot records counted and checked structurally; meaning reviewed selectively. No API calls or image generation.",
        "counts": {"base_presets": len(base["presets"]), "merged_presets": len(data["presets"]),
                   "slots": len(data["slots"]), "slot_candidates": len(candidates),
                   "profiles": len(profiles), "categories": len(categories),
                   "singleton_categories": sum(count == 1 for count in categories.values()),
                   "exact_lookup_rows": len(index["exact_lookup"]),
                   "visual_semantics_rows": len(semantic_rows),
                   "extensions_with_visual_semantics": sum(row.get("visual_semantics_count", 0) > 0 for row in extension_rows),
                   "required_evidence_fields": sum(len(row["evidence_requirements"]) for row in profiles),
                   "single_literal_evidence_rules": sum(len(rule.get("must_mention_any", [])) == 1 for row in profiles for rule in row["evidence_requirements"].values()),
                   "render_gates": sum(len(row["render_gates"]) for row in profiles),
                   "profiles_with_visual_relation": sum(isinstance(row.get("visual_relation"), dict) for row in profiles),
                   "profiles_with_boundary_prose_in_definition": sum(row["definition_flag"] for row in flagged),
                   "profiles_with_boundary_prose_in_concept_terms": sum(bool(row["flagged_concept_terms"]) for row in flagged),
                   "profiles_with_boundary_prose_in_embedding": sum(row["embedding_text_flag"] for row in flagged),
                   "candidates_with_public_process_tag": len(projected_process_tag_ids),
                   "recipe_roles": len(recipes["roles"]), "recipe_mixins": len(recipes["mixins"]), "recipe_aliases": len(recipes["aliases"]),
                   "character_concept_profiles": len(data["character_mechanism_graph"]["concept_profiles"])},
        "profile_category_counts": dict(sorted(categories.items())),
        "source_files": [{"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                         for path in sorted(ASSETS.glob("*.json"))],
        "consumed_extension_keys": consumed, "extensions": extension_rows,
        "visual_semantics_links": semantic_rows, "dangling_visual_semantics_links": dangling,
        "ignored_metadata_mutation_probe": {"files_modified": False,
                                            "changed_fields": ["visual_semantics[0].hard_profile_ids", "semantic_policy.hard_activation"],
                                            "merged_dictionary_unchanged": original_merge == changed_merge,
                                            "before_sha256": digest(original_merge), "after_sha256": digest(changed_merge)},
        "normalized_cross_profile_alias_collisions": {term: sorted(ids) for term, ids in aliases.items() if len(ids) > 1},
        "same_slot_exact_english_label_duplicates": [{"slot": key[0], "label_en": key[1], "ids": ids}
                                                      for key, ids in duplicate_labels.items() if key[1] and len(ids) > 1],
        "triage_regex": boundary.pattern, "boundary_prose_triage": flagged,
        "raw_bm25f_probes": lexical, "exact_activation_probes": activation_probes,
        "public_projection_examples": projection_examples,
        "candidates_with_public_process_tags": projected_process_tag_ids,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "counts": report["counts"],
                      "dangling_links": len(dangling), "alias_collisions": len(report["normalized_cross_profile_alias_collisions"]),
                      "ignored_metadata_mutation_unchanged": original_merge == changed_merge}, ensure_ascii=False))


if __name__ == "__main__":
    main()
