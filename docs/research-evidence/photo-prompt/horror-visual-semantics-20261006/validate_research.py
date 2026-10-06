#!/usr/bin/env python3
"""Validate research integrity and current source preservation, never render."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import hashlib, json, re, sys, ast

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
sys.path.insert(0,str(ROOT/"skills/photo-prompt-image-generator/scripts"))
import prompt_generator as pg
from visual_profile_contracts import compile_visual_profile
from photo_candidate_semantics import validate_relations

def load(name):
    return json.loads((OUT/name).read_text())

def ids(rows):
    values=[r["id"] for r in rows]
    assert len(values)==len(set(values)), "Duplicate identity"
    return set(values)

def main():
    for p in OUT.glob("*.json"):
        json.loads(p.read_text())
    for p in OUT.glob("*.py"):
        ast.parse(p.read_text(),filename=str(p))
    seeds=load("SEED-INVENTORY.json")["rows"]
    sources=load("SOURCES.json")["records"]
    units=load("SEMANTIC-UNITS.json")["units"]
    candidates=load("CANDIDATE-DRAFTS.json")["candidates"]
    mapping=load("RUNTIME-MAPPING.json")["mappings"]
    coverage=load("SEED-COVERAGE.json")["rows"]
    bundles=load("BUNDLE-DRAFTS.json")["bundles"]
    prototypes=load("PROFILE-PROTOTYPES.json")["prototypes"]
    source_ids,unit_ids,candidate_ids=ids(sources),ids(units),ids(candidates)
    seed_ids=ids(seeds)
    assert len(seeds)==len(units)==len(mapping)==len(coverage)==250
    assert len(candidates)==161 and len(bundles)==12 and len(prototypes)==3
    assert {s for u in units for s in u["seed_refs"]}==seed_ids
    assert ids(coverage)==seed_ids
    assert {m["semantic_id"] for m in mapping}==unit_ids
    assert {x["semantic_id"] for x in coverage}==unit_ids
    mode=Counter(u["mode"] for u in units)
    assert dict(mode)=={"visual":155,"context":19,"reuse":21,"variant_hold":6,"critical":9,"temporal":16,"audio":18,"bundle":6}
    units_by={u["id"]:u for u in units}
    gate_ids=[]
    for u in units:
        assert not u["whole_seed_row_verified"]
        assert u["components"] and u["relations"] and u["confusion_boundaries"]
        assert set(u["source_refs"])<=source_ids
        ids(u["components"])
        validate_relations(u["relations"],u["id"])
        assert all(c["owner_binding"] and len(c["observable_predicate_en"].split())>=4 for c in u["components"])
        if u["mode"] in {"audio","temporal","critical","context"}:
            assert not u["pixel_gates"] and u["static_image_status"]=="NO_DIRECT_STILL_IMAGE_PROOF"
        gate_ids.extend(g["id"] for g in u["pixel_gates"])
    assert len(gate_ids)==len(set(gate_ids))
    assets=ROOT/"skills/photo-prompt-image-generator/assets"
    data=pg.load_json(assets/"photo_prompt_tags.json")
    registry=pg.load_visual_obligation_registry(assets/"photo_prompt_visual_obligations.json")
    current_entry_ids={e["id"] for rows in data["slots"].values() for e in rows}
    current_profile_ids={p["id"] for p in registry["profiles"]}
    current_gate_ids={g["id"] for p in registry["profiles"] for g in p.get("render_gates",[])}
    assert not set(gate_ids)&current_gate_ids
    assert not candidate_ids&current_entry_ids
    for m in mapping:
        for link in m["existing_links"]:
            assert link["id"] in (current_entry_ids if link["kind"]=="candidate" else current_profile_ids),link["id"]
        assert m["candidate_draft_id"] is None or m["candidate_draft_id"] in candidate_ids
    forbidden=re.compile(r"https?://|SOURCES(?:\.md|\.json)|RESEARCH_DRAFT|\bS\d{2}\b|\bKCI\b|British Library|\bBFI\b|\bYale\b|Merriam|\bIEEE\b|조회 실패",re.I)
    for c in candidates:
        assert c["semantic_id"] in unit_ids and c["slot"] in data["slots"]
        assert set(c["source_refs"])<=source_ids and not c["adoption_ready"]
        assert c["entry_projection"]["id"]==c["id"]
        assert not forbidden.search(json.dumps(c["entry_projection"],ensure_ascii=False)),c["id"]
        assert c["effect_review"]["current_declared_slot_dimensions"]==data["candidate_semantic_policy"]["slot_dimensions"].get(c["slot"],[])
        assert c["activation"]=="optional_postcore" and not c["broad_seed_alias_activation"]
        validate_relations(c["entry_projection"]["relations"],c["id"])
    for b in bundles:
        assert set(b["semantic_members"])<=unit_ids
        assert set(b["member_draft_ids"])<=candidate_ids
        assert b["adoption"]=="optional" and b["no_hard_activation_by_association"]
        assert b["all_members_required_if_selected"] and b["joint_components"]
        validate_relations(b["relations"],b["id"])
    projection=[]
    for row in prototypes:
        p=row["profile"]
        for generated in ("required_evidence_fields","evidence_requirements","render_gates","composition_instruction"):
            assert generated not in p
        assert "component_semantics" not in p["semantics"]
        compiled=compile_visual_profile(p)
        assert len(compiled["required_evidence_fields"])==len(compiled["render_gates"])==3
        bad=deepcopy(p)
        bad["authored_components"]["obligations"][0]["component_ids"].pop()
        try:
            compile_visual_profile(bad)
        except ValueError:
            mutation="PASS_REJECTED_UNBOUND_COMPONENT"
        else:
            raise AssertionError("Compiler accepted an unbound required component")
        projection.append({"id":compiled["id"],"status":"PASS_COMPILER_PROJECTION_ONLY","mutation":mutation,
                           "gate_ids":[g["id"] for g in compiled["render_gates"]]})
    regression=load("REGRESSION-PLAN.json")
    assert regression["status"]=="PLANNED_NOT_EXECUTED" and regression["independent_holdouts"]==0
    assert len(regression["development_cases"])==728 and len(regression["global_controls"])==14
    ids(regression["development_cases"]);ids(regression["global_controls"])
    pixels=load("PIXEL-QUALIFICATION-PLAN.json")
    assert len(pixels["case_groups"])==22 and pixels["native_generations_run"]==0
    for c in pixels["case_groups"]:
        assert set(c["semantic_ids"])<=unit_ids
        assert c["evaluation"]["partial_is_fail"] and c["evaluation"]["hidden_required"]=="UNOBSERVABLE_NOT_PASS"
    palettes=load("PALETTE-DRAFTS.json")["palettes"]
    assert len(palettes)==12 and all(len(p["hex"])==len(p["proposed_owners"])==3 for p in palettes)
    assert all(re.fullmatch("#[0-9A-F]{6}",h) for p in palettes for h in p["hex"])
    # Reference links in generated local reports must resolve to files. Anchor-only links are excluded.
    local_links=[]
    for p in OUT.glob("*.md"):
        for url in re.findall(r"\]\(([^)]+)\)",p.read_text()):
            if "://" not in url and not url.startswith("#"):
                target=OUT/url.split("#",1)[0]
                assert target.is_file(), (p.name,url)
                local_links.append(url)
    snapshot=load("CHECKOUT-SNAPSHOT.json")
    drift=[]
    for f in snapshot["files"]:
        path=ROOT/f["path"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=f["sha256"]:
            drift.append(f["path"])
    receipt={
        "status":"PASS_RESEARCH_INTEGRITY","as_of":"2026-10-06 KST",
        "seed_coverage":{"rows":250,"unmapped":0,"duplicate_ids":0},
        "candidate_proposals":{"count":161,"held":6,"live_adoption_ready":0,"current_id_collisions":0},
        "existing_neighbor_links_verified":sum(bool(m["existing_links"]) for m in mapping),
        "bundle_proposals":12,"palette_proposals":12,
        "compiler_prototypes":projection,
        "source_claims":"Declared read depths and explicit limits retained; not whole-row factual verification.",
        "local_document_links_resolved":len(local_links),
        "source_preservation":{"files_checked":len(snapshot["files"]),"status":"UNCHANGED" if not drift else "DRIFT_REQUIRES_REVIEW","drift":drift},
        "planned_not_executed":{"development_cases":728,"global_controls":14,"pixel_groups":22},
        "not_performed":["live source registration","index rebuilding","real retrieval qualification","candidate-pack execution","image generation","native pixel review","user visual acceptance"]
    }
    (OUT/"VALIDATION.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(receipt,ensure_ascii=False))

if __name__=="__main__":
    main()
