#!/usr/bin/env python3
"""Validate research references and current source preservation; no runtime mutation."""
from __future__ import annotations
import hashlib,json,math,re,sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3]
sys.path.insert(0,str(BASE))
import build_research as build
from photo_candidate_semantics import validate_candidate_entries
from visual_profile_contracts import compile_visual_profile
from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS

def read(name):return json.loads((BASE/name).read_text())
def require(value,message):
    if not value:raise AssertionError(message)

def main():
    seeds=read("SEED-KEYWORDS.json")["rows"];cards=read("SEMANTIC-CARDS.json")["cards"]
    drafts=read("CANDIDATE-DRAFTS.json")["drafts"];sources=read("SOURCES.json")["sources"]
    mechanisms=read("MECHANISM-CARDS.json")["units"];mapping=read("RUNTIME-MAPPING.json")["mappings"]
    metrics=read("SWATCH-METRICS.json")["palette_rows"];prototypes=read("PROFILE-PROTOTYPES.json")["prototypes"]
    regressions=read("REGRESSION-PLAN.json")["cases"];pixels=read("PIXEL-QUALIFICATION-PLAN.json")["cases"]
    sid={r["source_id"] for r in sources};mids={r["semantic_id"] for r in mechanisms}
    ids=set(range(1,101));require(len(sid)==len(sources)==37,"unique sources")
    require(len(mids)==len(mechanisms)==16,"unique mechanism cards")
    for group in (seeds,cards,mapping,metrics):
        require(len(group)==100 and {x["seed_id"] for x in group}==ids,"complete ordered palette coverage")
    require(len(drafts)==len({d["draft_id"] for d in drafts})==100,"unique candidate draft IDs")
    require(len({c["group_id"] for c in cards})==13,"13 source families")
    require(sum(c["seed_case_inspired"] for c in cards)==32,"source case/design distinction preserved")
    require({r["mechanism_id"] for r in regressions}==mids and len(regressions)==64,"regression plan coverage")
    require({p["mechanism_id"] for p in pixels}==mids and len(pixels)==16,"pixel plan coverage")
    require(all(r["status"]=="PROPOSED_NOT_RUN" for r in regressions),"planned cases not results")
    require(sum(p["status"].startswith("HELD") for p in pixels)==3,"sensitive context plans held")
    for seed,card,draft,maprow,metric in zip(seeds,cards,drafts,mapping,metrics):
        i=seed["seed_id"]
        require(card["semantic_id"]==draft["semantic_id"]==maprow["semantic_id"]=="P"+str(i).zfill(3),"cross-file semantic ID "+str(i))
        require(set(card["source_refs"])<=sid and set(card["mechanism_card_ids"])<=mids,"source/mechanism refs "+str(i))
        require({o["color_index"] for o in card["owner_binding_examples"]}==set(range(len(seed["hex_srgb_approximations"]))),"complete owner/color coverage "+str(i))
        require([c["hex"] for c in metric["colors"]]==seed["hex_srgb_approximations"],"original HEX bytes "+str(i))
        require(len(metric["pairwise_metrics"])==math.comb(len(metric["colors"]),2),"all color pairs "+str(i))
        require(draft["scope_binding_status"]=="UNRESOLVED_RESEARCH_PLACEHOLDERS" and not maprow["binding_verified"],"no unproved owner binding "+str(i))
        entry=draft["entry_proposal"];serialized=json.dumps(entry,ensure_ascii=False)
        require("http" not in serialized and "source_refs" not in entry and "qualification" not in entry,"research metadata separated "+str(i))
        require(all(effect["target"].startswith("research_owner_") for effect in entry["affected_properties"]),"placeholder explicitly marked "+str(i))
        require(not entry.get("core_assertion_discovery",False),"unqualified discovery not enabled "+str(i))
        for st in metric["colors"]:
            require(all(math.isfinite(v) for v in st["oklab"].values()),"finite color values")
            require(0<=st["relative_luminance"]<=1,"luminance bounds")
    require(build.numeric_color("#000000")["relative_luminance"]==0,"linear black")
    require(build.numeric_color("#FFFFFF")["relative_luminance"]==1,"linear white")
    require(abs(build.numeric_color("#FF0000")["oklab"]["L"]-0.627955)<0.000002,"reference red coordinate")
    require(all(metrics[99]["colors"][j]["oklch"]["L"]<metrics[99]["colors"][j+1]["oklch"]["L"] for j in range(4)),"ordered representative Viridis anchor lightness")
    for m in mechanisms:require(set(m["source_refs"])<=sid,"mechanism source refs")
    data=build.pg.load_json(build.SKILL/"assets/photo_prompt_tags.json")
    registry=build.pg.load_visual_obligation_registry(build.SKILL/"assets/photo_prompt_visual_obligations.json")
    current_profiles={p["id"] for p in registry["profiles"]}
    current_candidates={(slot,e["id"]) for slot,rows in data["slots"].items() for e in rows}
    for card,row in zip(cards,mapping):
        require(set(card["existing_profile_options"])<=current_profiles,"current profile references")
        for r in row["existing_candidate_sources"]:
            require((r["slot"],r["id"]) in current_candidates,"current candidate ref")
            require((build.SKILL/"assets"/r["source_file"]).is_file(),"actual source owner file")
    slots={}
    for d in drafts:slots.setdefault(d["slot_proposal"],[]).append(d["entry_proposal"])
    validate_candidate_entries({"slots":slots},AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
    gate_ids=[]
    for proto in prototypes:
        compiled=compile_visual_profile(proto["profile"]);serialized=json.dumps(compiled,ensure_ascii=False)
        for component in proto["profile"]["authored_components"]["components"]:
            require(component["evidence_terms"][0] in serialized and component["render_gate"]["id"] in serialized,"compiled component/evidence/gate projection")
            gate_ids.append(component["render_gate"]["id"])
    require(len(gate_ids)==len(set(gate_ids))==16,"unique prototype gate IDs")
    for path in BASE.glob("*.md"):
        text=path.read_text()
        for target in re.findall(r"\]\(([^)]+)\)",text):
            if "://" in target or target.startswith("#"):continue
            require((path.parent/target.split("#")[0]).exists(),"local link "+str(path.name)+" -> "+target)
    modules=["test_photo_color_relations","test_photo_lighting_color_owner_data_cleanup","test_photo_lighting_visual_semantics",
             "test_photo_candidate_semantics","test_photo_visual_profile_retrieval","test_photo_positive_retrieval",
             "test_photo_bm25f_retrieval","test_photo_authorial_core_v6","test_photo_core_retrieval",
             "test_photo_semantic_index","test_photo_visual_profile_shards","test_photo_structure_maintenance"]
    require(all((ROOT/"tests"/(m+".py")).exists() for m in modules),"planned suites exist")
    audit=read("CURRENT-DATA-AUDIT.json");changes=[];missing=[]
    for rel,h in audit["protected_sha256"].items():
        p=ROOT/rel
        if not p.exists():missing.append(rel)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=h:changes.append(rel)
    html=(BASE/"PALETTE-ATLAS.html").read_text()
    require("__PALETTE_DATA__" not in html and "research-data" in html,"atlas data populated")
    raw=re.search(r'<script id="research-data" type="application/json">(.*?)</script>',html,re.S).group(1)
    payload=json.loads(raw);require(len(payload["cards"])==100,"atlas card count")
    for row,card,metric in zip(payload["cards"],cards,metrics):
        require(row["seed_id"]==card["seed_id"] and row["owners"]==card["owner_binding_examples"],"atlas owner data current")
        require(row["colors"]==metric["colors"] and row["relation_en"]==card["visual_relation_en"],"atlas metrics/relation current")
        require(row["failure_ko"]==card["false_substitutes_ko"][0],"atlas contrast current")
    require(payload["sources"]==sources,"atlas source limits current")
    require(not re.search(r'<script[^>]+src=',html,re.I),"no external scripts")
    result={"status":"PASS" if not changes and not missing else "RESEARCH_INTEGRITY_PASS_SOURCE_DRIFT",
            "counts":{"palette_cards":100,"mechanism_cards":16,"candidate_drafts":100,"sources":37,
                      "prototype_components":16,"proposed_regression_cases":64,"proposed_pixel_scenarios":16,
                      "input_color_refs":sum(len(x["hex_srgb_approximations"]) for x in seeds)},
            "checks":["complete seed/color coverage","unique stable draft IDs","source/mechanism/owner references",
                      "research metadata isolation","current candidate/profile/source existence",
                      "candidate effect syntax","component compiler evidence/gate projection",
                      "Oklab reference coordinates","ordered representative Viridis lightness",
                      "local report links","planned test module existence","atlas data, current source projection and no external scripts"],
            "protected_file_count":len(audit["protected_sha256"]),"protected_files_unchanged":len(audit["protected_sha256"])-len(changes)-len(missing),
            "changed_protected_paths":changes,"missing_protected_paths":missing,
            "owner_binding":"UNVERIFIED_DRAFTS","retrieval":"NOT_RUN","native_pixels":"NOT_RUN",
            "runtime_suite":"NOT_RUN_RESEARCH_SCOPE","embedding_api_calls":0,"image_api_calls":0,
            "browser_render":"UNVERIFIED_FILE_URL_BLOCKED_BY_BROWSER_POLICY",
            "browser_policy_note":"The browser rejected file: navigation. No alternate browser surface or HTTP workaround was attempted."}
    (BASE/"VALIDATION-REPORT.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
