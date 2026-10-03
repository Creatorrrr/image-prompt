"""Build a research-only corpus from curated specs and a verified Git baseline.

Does not edit skill assets, rebuild indexes, call image generation, or execute
the proposed semantic regressions. Run from the repository root.
"""
from __future__ import annotations

import hashlib
import copy
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SKILL = Path("skills/photo-prompt-image-generator")


def read_psv(name, count):
    result = []
    for line in (OUT / name).read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        row = line.split("|")
        assert len(row) == count, (name, row[0], len(row))
        result.append(row)
    return result


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def clean(value):
    return re.sub(r":chatgpt-content-reference\{[^}]+\}", "", value).replace("**", "").strip()


def source_inventory():
    sections = {}
    section = 0
    for line in (OUT / "source-conversation.partial.md").read_text().splitlines():
        match = re.match(r"#+ (\d+)\.", line)
        if match:
            section = int(match[1])
        if line.startswith("| **") and line.endswith("|"):
            cells = [clean(x) for x in line.strip("|").split("|")]
            assert len(cells) == 2
            sections.setdefault(section, []).append(cells)
    tail = json.loads((OUT / "source-tail.json").read_text())
    assert len(sections[11]) == 15
    sections[11].extend(tail["section_11_rows_from_16"])
    sections[12] = tail["section_12_rows"]
    groups = {5: "H", 6: "F", 7: "B", 8: "N", 9: "C", 10: "G", 11: "A", 12: "P"}
    terms = {}
    for section, prefix in groups.items():
        for i, (label, description) in enumerate(sections[section], 1):
            tid = f"{prefix}{i:02d}"
            terms[tid] = {"id": tid, "source_section": section, "source_label": label,
                          "source_description": description, "group": prefix}
    cases = []
    for section in range(1, 5):
        for label, description in sections[section]:
            cases.append({"id": f"K{len(cases)+1:02d}", "source_section": section,
                          "source_label": label, "source_description": description})
    assert len(terms) == 171 and len(cases) == 37
    save("SOURCE-CONVERSATION.json", {
        "schema_version": "research-source-dialogue/v1",
        "conversation_id": "6ac0831d-0450-83ee-a900-01dbfc850d62",
        "title": "서브컬처 외형 용어 조사", "untrusted_source_data": True,
        "retrieval": {"connector": "read_thread turnLimit=10, no older cursor",
                      "connector_response_limit_chars": 20000,
                      "browser": "read-only rendered DOM, 13 tables, 14 sections",
                      "full_table_counts": [14, 7, 8, 8, 21, 20, 14, 26, 19, 25, 23, 23, 8],
                      "local_copy": "bounded Markdown plus normalized missing table rows",
                      "full_raw_transcript_archived": False},
        "terms": list(terms.values()), "cases": cases,
        "ambiguities": tail["section_13_ambiguities"],
        "example_titles": tail["section_14_example_titles"]})
    return terms, cases


def positive_profile_text(profile):
    # Do not treat usage contexts, rejects, source prose, or claim limits as coverage.
    activation = profile.get("activation") or {}
    semantics = profile.get("semantics") or {}
    return {"labels": activation.get("exact_terms", []),
            "paraphrases": semantics.get("paraphrase_examples", []),
            "components": semantics.get("visual_components", []),
            "definition": semantics.get("definition", ""),
            "concepts": (profile.get("concept_candidate") or {}).get("concept_terms", [])}


def baseline_catalog():
    snapshot = json.loads((OUT / "RUNTIME-SNAPSHOT.json").read_text())
    revision = snapshot["git_head"]
    names = subprocess.run(["git", "ls-tree", "-r", "--name-only", revision, str(SKILL)],
                           cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
    with tempfile.TemporaryDirectory(prefix="subculture-reference-") as directory:
        root = Path(directory)
        for name in names:
            if name in snapshot["runtime_json_sha256"] or name.endswith(".py") or "/precore/" in name:
                data = subprocess.run(["git", "show", revision + ":" + name], cwd=ROOT,
                                      check=True, capture_output=True).stdout
                if name in snapshot["runtime_json_sha256"]:
                    assert hashlib.sha256(data).hexdigest() == snapshot["runtime_json_sha256"][name]
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        sys.path.insert(0, str(root / SKILL / "scripts"))
        import prompt_generator as generator
        asset = root / SKILL / "assets"
        registry = generator.load_visual_obligation_registry(asset / "photo_prompt_visual_obligations.json")
        tags = generator.load_json(asset / "photo_prompt_tags.json")
        assert len(registry["profiles"]) == snapshot["profiles"] == 1510
        profiles = [{"id": p["id"], "category": p.get("category"),
                     "positive_fields": positive_profile_text(p),
                     "concept_candidate": p.get("concept_candidate", {}),
                     "required_evidence_fields": p.get("required_evidence_fields", [])}
                    for p in registry["profiles"]]
        candidates = [{"slot": slot, "id": entry["id"], "ko": entry.get("ko"), "en": entry.get("en"),
                       "aliases": entry.get("aliases", []), "keywords": entry.get("keywords", []),
                       "concept_units": entry.get("concept_units", []), "relations": entry.get("relations", []),
                       "affected_dimensions": entry.get("affected_dimensions", []),
                       "affected_properties": entry.get("affected_properties", []),
                       "core_assertion_discovery": entry.get("core_assertion_discovery", False),
                       "slot_dimensions": tags["candidate_semantic_policy"]["slot_dimensions"].get(slot, [])}
                      for slot, entries in tags["slots"].items() for entry in entries]
        policy = tags["candidate_semantic_policy"]
    save("REFERENCE-CATALOG-SNAPSHOT.json", {
        "schema_version": "research-reference-catalog/v1", "reference_mode": "verified_git_baseline",
        "git_head": revision, "matches_initial_live_snapshot_hashes": True,
        "profile_count": len(profiles), "candidate_count": len(candidates),
        "profiles": profiles, "candidates": candidates, "candidate_semantic_policy": policy})
    return profiles, candidates, policy


def dimensions(slot, mode, tid, policy):
    result = list(policy["slot_dimensions"].get(slot, []))
    if mode == "cross_dimension":
        extras = (["style"] if tid == "B14" else ["concept"] if tid in {"P07", "P23"}
                  else ["body_geometry"] if tid in {"N20", "N21", "P14"}
                  else ["species", "subject"])
        result = list(dict.fromkeys(result + extras))
    return result


def render_region(tid, prop):
    if tid.startswith("H"): return "head and full selected hair boundary"
    if tid.startswith("F"): return "face crop with selected eyes or mouth large enough to resolve"
    if tid.startswith("B") or tid in {"N08", "N17", "N18", "N19", "N24"}: return "full body and named attachment or contact landmarks"
    if "face" in prop or "head" in prop: return "head and specified covering edges or organ roots"
    if tid.startswith("P"): return "selected object or surface plus its root/interface and comparison owner"
    return "named garment or body region with both relevant boundaries visible"


def build():
    terms, source_cases = source_inventory()
    sources = []
    for sid, title, url, authority, access, claim, limit in read_psv("sources.psv", 7):
        sources.append({"id": sid, "title": title, "url": url, "authority": authority,
                        "access": access, "reviewed_on": "2026-10-03 Asia/Seoul",
                        "source_supported_scope": claim, "limits": limit,
                        "operationalization": "components and proposed owner/property design are researcher-authored unless explicitly stated otherwise"})
    save("RESEARCH-SOURCES.json", {"schema_version": "research-source-ledger/v1", "sources": sources})
    source_ids = {x["id"] for x in sources}
    profiles, entries, policy = baseline_catalog()
    corrections = json.loads((OUT / "semantic-corrections.json").read_text())
    profile_texts = [(p, json.dumps(p["positive_fields"], ensure_ascii=False).casefold()) for p in profiles]
    entry_texts = [(entry, json.dumps({k:entry.get(k) for k in ["ko", "en", "aliases", "keywords", "concept_units", "relations"]}, ensure_ascii=False).casefold()) for entry in entries]
    units, drafts, audit = [], [], []
    for tid, en, slot, prop, components, contrast, source, priority, mode in read_psv("term-specs.psv", 9):
        term = terms[tid]
        assert slot in policy["slot_dimensions"] and all(x in source_ids for x in source.split(","))
        parts = components.split(";")
        affected = dimensions(slot, mode, tid, policy)
        allowed = policy["slot_dimensions"][slot]
        state = ("HOLD_UNSCOPED_SLOT" if not allowed else
                 "HOLD_CROSS_DIMENSION" if set(affected) - set(allowed) else
                 "CONTEXT_RECIPE_REVIEW" if mode == "recipe" else
                 "HOLD_LABEL_ONLY" if mode == "label_only" else
                 "MEDIUM_CONDITIONAL_REVIEW" if mode == "medium_guard" else
                 "EXISTING_OWNER_REVIEW" if mode == "reuse" else "ATOM_REVIEW")
        queries = [x.strip() for x in re.split(r"／|·", term["source_label"])] + [en]
        query_norm = [q.casefold() for q in queries if len(q) >= 3]
        profile_hits = []
        candidate_hits = []
        for profile, text in profile_texts:
            hits = [q for q in query_norm if q in text]
            if hits: profile_hits.append({"id": profile["id"], "matched_query_fragments": hits})
        for entry, text in entry_texts:
            hits = [q for q in query_norm if q in text]
            if hits: candidate_hits.append({"slot": entry["slot"], "id": entry["id"], "matched_query_fragments": hits})
        audit.append({"term_id": tid, "queries": queries,
                      "method": "literal positive-field substring probe; not runtime routing and not semantic equivalence",
                      "profile_hits": profile_hits, "candidate_hits": candidate_hits,
                      "decision": "manual owner/component comparison required; zero hits does not prove missing coverage"})
        term.update({"canonical_interpretation_en": en, "decision": mode, "priority": priority,
                     "unit_id": "sca_" + tid.lower(), "source_ids": source.split(","),
                     "binding_status": state, "lexical_status": "community_or_descriptive_label_requires_scope",
                     "lookup_authority": "advisory_until_explicit_positive_core_and_equivalence_review"})
        owner = prop.rsplit(".", 1)[0]
        unit = {"id": term["unit_id"], "term_ids": [tid], "label_ko": term["source_label"],
                "label_en": en, "source_ids": source.split(","),
                "basis": "researched interpretation proposal; source scope is recorded separately in RESEARCH-SOURCES",
                "selected_interpretation_only": True, "mode": mode,
                "owner_template": {"owner": owner, "target": "the same explicitly declared subject/object instance", "binding_required": True},
                "slot_proposal": slot, "affected_dimensions_proposal": affected,
                "property_anchor_proposal": prop,
                "property_namespace_status": "research namespace; translate to existing runtime property owner before promotion",
                "components": [{"id": f"{tid.lower()}_part_{i+1}", "positive_relation": part} for i, part in enumerate(parts)],
                "positive_paraphrase_ko": term["source_description"],
                "authored_paraphrase_ko": corrections.get(tid, term["source_description"]),
                "positive_paraphrase_en": "; ".join(parts),
                "ko_source_paraphrase_status": "source description retained for traceability; apply corrections in FINDINGS before runtime promotion",
                "confusions": [contrast],
                "relations": [{"id": f"{tid.lower()}_owner_{i+1}", "type": "declared_owner_scope", "subject": f"{tid.lower()}_part_{i+1}", "object": owner} for i in range(len(parts))],
                "observability": {"region": render_region(tid, prop), "occluded": "UNOBSERVABLE", "partial_is_fail": True,
                                  "perspective_control": "compare declared landmarks on the same owner; do not infer hidden structures"},
                "render_gates_proposed": [{"id": f"sca_{tid.lower()}_component_{i+1}", "criterion": part, "scale": "native"} for i, part in enumerate(parts)] +
                                         [{"id": f"sca_{tid.lower()}_owner", "criterion": "all selected parts bind to the declared owner; the listed confounder is not substituted", "scale": "native"}],
                "gate_logic": "ALL selected components AND owner; one selected recipe is not a universal definition of the source label",
                "not_inferred_from_label": ["specific colors unless selected", "material chemistry", "age", "gender identity", "narrative cause", "sexual tone"],
                "prerequisites": ["explicit adult context"] if tid.startswith("A") else ["explicit body/species/medium context where the selected interpretation needs it"],
                "priority": priority}
        units.append(unit)
        drafts.append({"id": "sca_candidate_" + tid.lower(), "source_term_id": tid, "semantic_unit_id": unit["id"],
                       "slot_proposal": slot, "affected_dimensions_proposal": affected,
                       "affected_properties_proposal": [prop], "owner_template": unit["owner_template"],
                       "en_proposal": unit["positive_paraphrase_en"],
                       "ko_source_draft": term["source_description"], "concept_units_proposal": parts,
                       "ko_proposal": unit["authored_paraphrase_ko"],
                       "relations_proposal": unit["relations"], "status": state,
                       "same_slot_context_extension_allowed": mode == "reuse",
                       "extension_condition": "only equivalent contexts after actual baseline ID/guards/components review; never change effects silently",
                       "required_before_adoption": ["map to actual core target", "resolve property namespace", "positive/exclusion check", "all dimension and property locks", "compatibility with whole pack", "medium/species/context prerequisites"],
                       "priority": priority, "source_ids": source.split(","), "runtime_eligible_now": False})
    assert len(units) == len(drafts) == 171 and {x["id"] for x in terms.values()} == {x["source_term_id"] for x in drafts}
    save("TERM-INVENTORY.json", {"schema_version": "research-term-inventory/v1", "terms": list(terms.values())})
    primary_unit_count = len(units)
    parent_units = {x["term_ids"][0]: x for x in units}
    parent_drafts = {x["source_term_id"]: x for x in drafts}
    for xid, parent, label, slot, prop, components, ko, contrast, source, mode in read_psv("structural-splits.psv", 10):
        parents = parent.split(",")
        assert all(tid in terms for tid in parents) and all(sid in source_ids for sid in source.split(","))
        parts = components.split(";")
        affected = dimensions(slot, mode, xid, policy)
        state = ("HOLD_UNSCOPED_SLOT" if not policy["slot_dimensions"][slot] else
                 "HOLD_CROSS_DIMENSION" if set(affected)-set(policy["slot_dimensions"][slot]) else
                 "EXISTING_OWNER_REVIEW" if mode == "reuse" else "ATOM_REVIEW")
        unit = copy.deepcopy(parent_units[parents[0]])
        unit.update({"id": "sca_"+xid.lower(), "split_id": xid, "term_ids": parents, "label_en": label,
                     "label_ko": ko, "source_ids": source.split(","), "mode": mode,
                     "slot_proposal": slot, "affected_dimensions_proposal": affected,
                     "property_anchor_proposal": prop,
                     "owner_template": {"owner": prop.rsplit(".",1)[0], "target": "the explicitly declared same owner", "binding_required": True},
                     "components": [{"id": f"{xid.lower()}_part_{i+1}", "positive_relation": part} for i,part in enumerate(parts)],
                     "positive_paraphrase_ko": ko, "authored_paraphrase_ko": ko,
                     "ko_source_paraphrase_status": "researcher-authored refinement", "positive_paraphrase_en": components,
                     "confusions": [contrast], "priority": "P0"})
        unit["relations"] = [{"id": f"{xid.lower()}_owner_{i+1}", "type": "declared_owner_scope", "subject": f"{xid.lower()}_part_{i+1}", "object": unit["owner_template"]["owner"]} for i in range(len(parts))]
        unit["observability"]["region"] = render_region(xid, prop)
        unit["render_gates_proposed"] = [{"id": f"sca_{xid.lower()}_component_{i+1}", "criterion": part, "scale": "native"} for i,part in enumerate(parts)] + [{"id":f"sca_{xid.lower()}_owner", "criterion":"all parts belong to the declared owner", "scale":"native"}]
        draft = copy.deepcopy(parent_drafts[parents[0]])
        draft.update({"id": "sca_candidate_"+xid.lower(), "source_term_id": None, "source_term_ids": parents,
                      "semantic_unit_id": unit["id"], "slot_proposal": slot, "affected_dimensions_proposal": affected,
                      "affected_properties_proposal": [prop], "owner_template": unit["owner_template"],
                      "en_proposal": components, "ko_source_draft": None, "ko_proposal": ko,
                      "concept_units_proposal": parts, "relations_proposal": unit["relations"], "status": state,
                      "same_slot_context_extension_allowed": mode=="reuse", "source_ids": source.split(","), "priority":"P0"})
        units.append(unit); drafts.append(draft)
    save("SEMANTIC-UNITS.json", {"schema_version": "subculture-visual-research-units/v1", "runtime_schema": False, "units": units})
    save("CANDIDATE-DRAFTS.json", {"schema_version": "subculture-candidate-research-drafts/v1", "runtime_schema": False, "candidates": drafts})
    save("COVERAGE-AUDIT.json", {"schema_version": "research-positive-field-audit/v1", "reference_mode": "verified_git_baseline", "terms": audit})
    cases = []
    for cid, version, source, state, termids, observation in read_psv("case-specs.psv", 6):
        linked = [] if termids == "-" else termids.split(",")
        assert all(tid in terms for tid in linked)
        cases.append({**source_cases[int(cid[1:])-1], "version_scope": version, "source_ids": source.split(","),
                      "evidence_state": state, "related_term_ids": linked,
                      "research_decomposition": observation,
                      "source_description_status": "source-dialogue hypothesis; only explicitly observed facts upgraded",
                      "candidate_use": "extract separate name-free atoms; whole character resemblance is not an activation trigger",
                      "runtime_index_proper_names": False})
    assert len(cases) == 37
    save("CHARACTER-CASEBOOK.json", {"schema_version": "research-character-casebook/v1", "cases": cases})
    lines = ["# 171개 용어의 반영 판단표", "", "기준본: `900848816f88a494e5bf16ea475a25074d584911`. 현재 운영 데이터에 적용된 목록이 아닙니다.", "",
             "| ID | 원 용어 | 선택한 해석 | 슬롯 제안 | 우선순위 | 판단 / 상태 |", "|---|---|---|---|---|---|"]
    for term, draft in zip(terms.values(), drafts):
        lines.append(f"| {term['id']} | {term['source_label']} | {term['canonical_interpretation_en']} | `{draft['slot_proposal']}` | {draft['priority']} | {term['decision']} / {draft['status']} |")
    (OUT / "TERM-DECISIONS.md").write_text("\n".join(lines) + "\n")
    summary = {"source_terms": len(terms), "character_cases": len(cases), "semantic_units": len(units),
               "primary_interpretations": primary_unit_count, "additional_structural_splits": len(units)-primary_unit_count,
               "candidate_drafts": len(drafts), "sources_total_including_dialogue": len(sources),
               "external_sources": len(sources)-1, "baseline_profiles": len(profiles),
               "candidate_status_counts": dict(Counter(d["status"] for d in drafts)),
               "priority_counts": dict(Counter(d["priority"] for d in drafts)),
               "source_group_counts": dict(Counter(t["group"] for t in terms.values())),
               "pixels_observed_official_reference_images": 2,
               "native_generated_image_qualification": "NOT_RUN", "runtime_integration": "NOT_PERFORMED"}
    save("SUMMARY.json", summary)
    import enrich_research_package
    enrich_research_package.enrich()
    print((OUT / "SUMMARY.json").read_text())


if __name__ == "__main__":
    build()
