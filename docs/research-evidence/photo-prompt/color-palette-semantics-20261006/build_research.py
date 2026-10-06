#!/usr/bin/env python3
"""Build research artifacts only; never write runtime assets or call embedding/image APIs."""
from __future__ import annotations
import csv, hashlib, itertools, json, math, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg
from visual_profile_contracts import compile_visual_profile
from photo_candidate_semantics import validate_candidate_entries
from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS, property_effects_allowed

def read(name):
    return json.loads((BASE / name).read_text())
def write(name, value):
    (BASE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
def filehash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def numeric_color(hex_color):
    rgb = [int(hex_color[i:i+2], 16) / 255.0 for i in (1, 3, 5)]
    r, g, b = [x/12.92 if x <= 0.04045 else ((x+0.055)/1.055)**2.4 for x in rgb]
    y = 0.2126*r + 0.7152*g + 0.0722*b
    l = (0.4122214708*r + 0.5363325363*g + 0.0514459929*b)**(1/3)
    m = (0.2119034982*r + 0.6806995451*g + 0.1073969566*b)**(1/3)
    s = (0.0883024619*r + 0.2817188376*g + 0.6299787005*b)**(1/3)
    light = 0.2104542553*l + 0.7936177850*m - 0.0040720468*s
    a = 1.9779984951*l - 2.4285922050*m + 0.4505937099*s
    bb = 0.0259040371*l + 0.7827717662*m - 0.8086757660*s
    chroma = math.hypot(a, bb)
    # This is a display heuristic, never a hard semantic activation threshold.
    hue = math.degrees(math.atan2(bb, a)) % 360 if chroma >= 0.02 else None
    return {"hex":hex_color, "relative_luminance":round(y,6),
            "oklab":{"L":round(light,6), "a":round(a,6), "b":round(bb,6)},
            "oklch":{"L":round(light,6), "C":round(chroma,6), "h_degrees":round(hue,3) if hue is not None else None},
            "low_chroma_hue_undefined_for_this_review": hue is None}

def color_pairs(colors):
    result=[]
    for i,j in itertools.combinations(range(len(colors)),2):
        a,b=colors[i],colors[j]
        ya,yb=a["relative_luminance"],b["relative_luminance"]
        oa,ob=a["oklab"],b["oklab"]
        ha,hb=a["oklch"]["h_degrees"],b["oklch"]["h_degrees"]
        result.append({"color_indices":[i,j], "contrast_ratio":round((max(ya,yb)+0.05)/(min(ya,yb)+0.05),3),
                       "delta_oklab_x100":round(100*math.sqrt(sum((oa[k]-ob[k])**2 for k in ("L","a","b"))),3),
                       "delta_lightness":round(abs(oa["L"]-ob["L"]),6),
                       "hue_separation_degrees":round(min(abs(ha-hb),360-abs(ha-hb)),3) if ha is not None and hb is not None else None})
    return result

def build_atlas(cards, metric_rows, source_rows):
    by_metric={row["seed_id"]:row for row in metric_rows}
    rows=[]
    for card in cards:
        row={k:card[k] for k in ("semantic_id","seed_id","label_ko","group_id","group_label_ko","meaning_ko","priority","source_refs")}
        row.update({"owners":card["owner_binding_examples"],"relation_en":card["visual_relation_en"],
                    "failure_ko":card["false_substitutes_ko"][0],"colors":by_metric[card["seed_id"]]["colors"]})
        row["search_text"]=json.dumps(row,ensure_ascii=False).lower()
        rows.append(row)
    raw=json.dumps({"cards":rows,"sources":source_rows},ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")
    template=(BASE/"palette-atlas.template.html").read_text()
    assert template.count("__PALETTE_DATA__")==1
    html=template.replace("__PALETTE_DATA__",raw)
    (BASE/"PALETTE-ATLAS.html").write_text(html)
    scripts=re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',html,re.S)
    (BASE/"atlas-script.js").write_text("\n".join(s for s in scripts if not s.lstrip().startswith("{")))

def refs(raw): return [x for x in raw.split(",") if x and x!="-"]
def clean(text): return re.sub(r":chatgpt-content-reference\{[^}]*\}", "", text).replace("**","").strip()
def role_label(role):
    return {"large_field":"큰 바탕 예시","supporting_region":"지지 영역","small_accent":"작은 강조","dark_anchor":"어두운 지지점",
            "light_region":"밝은 구별 영역","middle_region":"중간 밝기","structural_dark":"윤곽·경계","reflective_accent":"반사 강조",
            "repeated_band":"반복 띠","color_block":"독립 색면","line_color":"문양 선","gradient_endpoint":"공간 경로 끝점",
            "transition_region":"전이 영역","cool_light_footprint":"차가운 색광의 수신 영역","warm_light_footprint":"따뜻한 색광의 수신 영역",
            "tint_region":"공통 보정 경향","achromatic_region":"무채색 영역","single_color_exception":"같은 owner의 유채색 예외",
            "emissive_region":"발광면","translucent_region":"투과 표면","retained_local_color":"보존할 국소색",
            "printed_region":"인쇄색 영역","subject_region":"피사체 영역","surface_color_region":"국소 표면색",
            "color_band":"분리 색띠","warning_region":"경고 패널","instruction_region":"안내 패널",
            "negative_data_side":"기준의 음쪽","data_center":"중앙 기준","positive_data_side":"기준의 양쪽",
            "categorical_region":"순위 없는 범주","low_data_anchor":"낮은 값 대표점","data_anchor":"중간 값 대표점",
            "high_data_anchor":"높은 값 대표점"}.get(role,role)

def slot_for(mode):
    if mode in {"global_grade","selective_grade"}: return "color_grading"
    if mode=="colored_lighting": return "lighting"
    return "color"

def make_entry(seed,spec,owners):
    sid=seed["seed_id"];slot=slot_for(spec["mechanism"])
    dims=["color","lighting"] if slot=="lighting" else ["color"]
    units=[]
    for owner in owners:
        if spec["mechanism"]=="data_mapping":
            units.append(owner["owner_phrase_en"]+" carries the declared color at its labeled value or category")
        else:
            units.append(owner["owner_phrase_en"]+" retains its assigned visible color region")
    units.append(spec["relation_en"])
    # Research placeholders are deliberately marked; they must be replaced with exact
    # frozen-core target/property paths before any candidate can be promoted.
    effects=[]
    for o in owners:
        effects.append({"dimension":"color","target":"research_owner_"+o["owner_key"],"property":"surface.local_color"})
        if slot=="lighting" and "light_footprint" in o["role"]:
            effects.append({"dimension":"lighting","target":"research_owner_"+o["owner_key"],"property":"illumination.color_footprint"})
    if slot=="color_grading":
        effects=[{"dimension":"color","target":"research_owner_declared_scope","property":"image.grade.color_mapping"}]
    entry={"id":"pal_"+spec["slug"].replace("-","_"),"ko":seed["label_ko"],"en":"; ".join(units),
           "aliases":[seed["label_ko"]],"keywords":[seed["label_ko"]]+[o["owner_phrase_en"] for o in owners],
           "concept_units":units,
           "relations":[{"id":"palette_relation","type":"assigned_color_regions_in_declared_scope","subject":owners[0]["owner_key"],"object":"declared_scope"}],
           "affected_dimensions":dims,"affected_properties":effects,
           "tags":["owner_bound_palette_application"],"weight":1.0,
           "embedding_text":"; ".join(units)}
    return slot,entry

def make_prototype(card,draft):
    sid=card["seed_id"];parts=card["observable_components_en"]
    profile={
        "id":"pal_research_"+str(sid).zfill(3), "category":"selected_color_region_relation",
        "activation":{"exact_terms":[card["visual_relation_en"]],"requires_adult_character":False,
                      "semantic_discovery_requires_component_evidence":True},
        "semantics":{"definition":card["visual_relation_en"], "paraphrase_examples":[card["label_ko"]],
                     "claim_limits":["Research prototype only: a palette name never requires these particular owners or materials.",
                                     "Owner and property binding must be resolved to the actual frozen core before adoption."]},
        "concept_candidate":{"concept_terms":parts,"affected_dimensions":draft["entry_proposal"]["affected_dimensions"],
                             "affected_properties":draft["entry_proposal"]["affected_properties"]},
        "runtime_expression":{"default_mode":"definition_with_optional_label","prompt_label_terms":[],
                              "forbidden_prompt_terms":[],"runtime_forbidden_labels":[]},
        "reject_substitutes":card["false_substitutes_ko"],
        "authored_components":{"contract_version":"photo-authored-visual-components/v1","components":[]}
    }
    for i,part in enumerate(parts,1):
        profile["authored_components"]["components"].append({
            "id":"component_"+str(i),"match_terms":[part],"evidence_field":"component_"+str(i)+"_phrase",
            "evidence_terms":[part],"min_content_words":3,
            "instruction":"Preserve this selected region relation: "+part,
            "render_gate":{"id":"vo_pal_research_"+str(sid).zfill(3)+"_"+str(i),"review_scale":"both",
                           "description":"Inspect only the selected declared owner and scope: "+part+". Missing, swapped or unclear evidence fails under partial_is_fail."}})
    compile_visual_profile(profile)
    return {"semantic_id":card["semantic_id"],"status":"RESEARCH_PROTOTYPE_NOT_ADOPTED",
            "qualification_scope":"Component compiler projection only; no registry, activation, owner binding, pack, runtime or pixel qualification.",
            "profile":profile}

def main():
    seeds=read("SEED-KEYWORDS.json")["rows"];source_rows=read("SOURCES.json")["sources"]
    mechanism_rows=read("MECHANISM-CARDS.json")["units"];audit=read("CURRENT-DATA-AUDIT.json")
    source_ids={x["source_id"] for x in source_rows};m_ids={x["semantic_id"] for x in mechanism_rows}
    data=pg.load_json(SKILL/"assets/photo_prompt_tags.json")
    registry=pg.load_visual_obligation_registry(SKILL/"assets/photo_prompt_visual_obligations.json")
    pids={p["id"] for p in registry["profiles"]};entries={(slot,e["id"]):e for slot,rows in data["slots"].items() for e in rows}
    cid_slots={}
    for slot,cid in entries:cid_slots.setdefault(cid,[]).append(slot)
    spec_rows=list(csv.DictReader((BASE/"PALETTE-AUTHORING.tsv").read_text().splitlines(),delimiter="|"))
    assert len(seeds)==len(spec_rows)==100
    assert {int(x["seed_id"]) for x in spec_rows}==set(range(1,101))
    for m in mechanism_rows:
        assert set(m["existing_profile_ids"])<=pids,(m["semantic_id"],set(m["existing_profile_ids"])-pids)
        assert set(m["source_refs"])<=source_ids
    by_m={m["semantic_id"]:m for m in mechanism_rows}
    source_owner={}
    base_data=json.loads((SKILL/"assets/photo_prompt_tags.json").read_text())
    for slot,rows in base_data["slots"].items():
        for entry in rows:source_owner[(slot,entry["id"])]="photo_prompt_tags.json"
    source_manifest=json.loads((SKILL/"assets/photo_prompt_source_manifest.json").read_text())
    for row in sorted([r for r in source_manifest["sources"] if r["kind"]=="candidate"],key=lambda r:r["load_order"]):
        ext=json.loads((SKILL/"assets"/row["file"]).read_text())
        for slot,rows in ext.get("slots",{}).items():
            for entry in rows:source_owner[(slot,entry["id"])]=row["file"]
    cards=[];drafts=[];mapping=[];metric_rows=[]
    for seed,spec in zip(seeds,spec_rows):
        sid=seed["seed_id"];assert int(spec["seed_id"])==sid
        hexes=seed["hex_srgb_approximations"];owners=[]
        for encoded in spec["owners"].split(";"):
            key,index,role,phrase=encoded.split("~");index=int(index)
            owners.append({"owner_key":key,"color_index":index,"hex_reference":hexes[index],"role":role,
                           "role_ko":role_label(role),"owner_phrase_en":phrase,"binding_status":"EXAMPLE_ONLY_REBIND_TO_FROZEN_CORE_REQUIRED"})
        assert {o["color_index"] for o in owners}==set(range(len(hexes))),sid
        srefs=refs(spec["source_refs"]);mrefs=refs(spec["mechanism_cards"]);existing=refs(spec["existing_candidates"])
        assert set(srefs)<=source_ids and set(mrefs)<=m_ids,sid
        assert all(x in cid_slots for x in existing),(sid,[x for x in existing if x not in cid_slots])
        stats=[numeric_color(h) for h in hexes];pairs=color_pairs(stats)
        metrics={"seed_id":sid,"colors":stats,"pairwise_metrics":pairs,
                 "model":"Encoded sRGB -> linear sRGB (D65) -> Oklab, 2021 direct linear-sRGB coefficients",
                 "metric_scope":"Proposed flat swatches only. Not measurements of source artwork, material, image generation or accessible interface."}
        metric_rows.append(metrics)
        slot,entry=make_entry(seed,spec,owners)
        comps=entry["concept_units"]
        analytic=spec["mechanism"]=="data_mapping";held=analytic or sid in (68,89,90,93,94,95,96,97)
        profiles=sorted({pid for mid in mrefs for pid in by_m[mid]["existing_profile_ids"]})
        direct_profiles={"cr_"+cid.removeprefix("cr_candidate_") for cid in existing if cid.startswith("cr_candidate_")}
        curated={4:["cr_high_value_contrast"],6:["cr_depth_palette"],9:["cr_high_value_contrast"],
                 10:["cr_light_on_light"],20:["cr_isolated_accent"],26:["cr_high_value_contrast"],
                 38:["cr_high_value_contrast"],49:["cr_high_value_contrast"],65:["cr_warm_subject"],
                 78:["cr_high_value_contrast"],81:["cr_dark_on_dark"],85:["cr_color_blocks"],
                 91:["cr_light_on_light"],92:["cr_hue_contrast"]}
        own_profiles=[] if analytic else sorted((direct_profiles|set(curated.get(sid,[]))) & pids)
        card={"semantic_id":"P"+str(sid).zfill(3),"seed_id":sid,"label_ko":seed["label_ko"],
              "group_id":seed["group_id"],"group_label_ko":seed["group_label_ko"],
              "seed_case_inspired":seed["case_inspired"],
              "claim_status":"DESIGN_APPLICATION_PROPOSAL_WITH_SEPARATE_CONTEXT_SOURCES",
              "meaning_ko":clean(seed["intent_original"]),"visual_relation_en":spec["relation_en"],
              "mechanism":spec["mechanism"],"mechanism_card_ids":mrefs,"owner_binding_examples":owners,
              "observable_components_en":comps,
              "false_substitutes_ko":[spec["failure_ko"],"색 목록이 같아도 서로 다른 owner·범위·광원 역할로 옮기면 선택한 관계의 충족이 아니다."],
              "source_refs":srefs,"source_support_scope":"Sources support the listed dimension or documented context. The owner allocation and HEX values remain authored proposals.",
              "existing_profile_options":own_profiles,
              "profile_mapping_scope":"Structural reuse options only; full exact/semantic context, scope and components must be reviewed. No match or equivalence is asserted.",
              "adjacent_mechanism_profiles_for_confusion_review":profiles,
              "hard_requirement_boundary":"Palette keywords alone do not prescribe these example objects, materials, counts, ratios, setting, light or psychological effects.",
              "ratio_policy":"No mandatory area ratio. Preserve requester allocation; compare alternate roles as a separate authorial choice.",
              "lighting_material_policy":"Owner materials must already be present or separately authorized. A new reflection, glaze, transparency or light mechanism requires declared additional effects.",
              "hex_policy":"Original proposed sRGB approximations; ordinary photographic shading need not equal every flat-chip RGB byte.",
              "priority":spec["priority"],"qualification_status":"PROPOSED_NOT_RUN"}
        cards.append(card)
        draft={"draft_id":entry["id"],"semantic_id":card["semantic_id"],"slot_proposal":slot,
               "status":"RESEARCH_ONLY_NOT_RUNTIME_SCHEMA","scope_binding_status":"UNRESOLVED_RESEARCH_PLACEHOLDERS",
               "entry_proposal":entry,"source_refs":srefs,
               "owner_preconditions":[o["owner_phrase_en"]+" must be independently present and identified in the frozen core" for o in owners],
               "effects_review_required":"Resolve every research_owner target and property to the actual core path. Do not use placeholder paths in property compatibility checks.",
               "existing_candidate_ids":existing,
               "adoption_recommendation":"ANALYTIC_RESEARCH_ONLY" if analytic else ("CONTEXT_FACTS_HELD_VISUAL_OPTION_REVIEW" if held else "DEDUPE_AND_BIND_OPTIONAL_APPLICATION"),
               "not_proven":["effective activation","candidate exposure","candidate adoption","literal prompt binding","native pixels","requesting-user acceptance"]}
        drafts.append(draft)
        mapping.append({"semantic_id":card["semantic_id"],"seed_id":sid,"priority":spec["priority"],
                        "decision":draft["adoption_recommendation"],"mechanism_cards":mrefs,
                        "existing_candidate_sources":[{"id":cid,"slot":sl,"source_file":source_owner.get((sl,cid))}
                                                      for cid in existing for sl in cid_slots[cid]],
                        "existing_profile_options":own_profiles,
                        "adjacent_profiles_are_not_equivalent":True,
                        "specific_reuse_risks":["The nearby existing oxblood palette adds antique gold absent from this seed; never adopt it as a complete match."] if sid==81 else [],
                        "candidate_file_preference":"Preserve the actual existing source owner. New palette-only variants may use the existing color relation source after dedupe.",
                        "new_extension_name_if_needed":"photo_prompt_palette_applications_extension.json",
                        "new_extension_registered":False,
                        "target_property_binding":entry["affected_properties"],
                        "binding_verified":False,"research_metadata_stays_external":True})
    validate_candidate_entries({"slots":{slot:[d["entry_proposal"] for d in drafts if d["slot_proposal"]==slot]
                                         for slot in sorted({d["slot_proposal"] for d in drafts})}},
                               AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
    assert len({d["draft_id"] for d in drafts})==100
    # Compiler examples are not recommendations to create four duplicate profiles.
    prototype_ids=[8,9,66,92];prototypes=[make_prototype(cards[i-1],drafts[i-1]) for i in prototype_ids]
    write("SEMANTIC-CARDS.json",{"schema_version":"color-palette-semantic-research/v1","status":"RESEARCH_ONLY","cards":cards})
    write("CANDIDATE-DRAFTS.json",{"schema_version":"color-palette-candidate-research/v1","status":"NOT_A_CANDIDATE_PACK","drafts":drafts})
    write("RUNTIME-MAPPING.json",{"schema_version":"color-palette-adoption-plan/v1","status":"PROPOSED_NOT_RUN","mappings":mapping})
    write("SWATCH-METRICS.json",{"schema_version":"color-palette-swatch-metrics/v1","source_refs":["S04","S37"],
                                 "numeric_rule":"Use modeled flat-chip metrics as review aids, never as universal hue harmony or photographic material pass thresholds.",
                                 "palette_rows":metric_rows})
    write("PROFILE-PROTOTYPES.json",{"schema_version":"color-palette-component-prototypes/v1","status":"RESEARCH_ONLY","prototypes":prototypes})
    # Human-readable cards remain concrete; URLs and negative examples never enter entry text.
    doc=["# 100개 배색의 시각 의미 카드","", "2026-10-06 KST · 선택 가능한 설계 예시 · 활성 데이터/인덱스/이미지 검증 미실행",
         "", "각 색의 owner는 하나의 가능한 적용 예시다. 조합 이름만으로 이 물체·재질·면적·장면을 요구하지 않는다. 출처는 맥락과 구조를 뒷받침하며, HEX·배치는 제안값이다.",
         "", "전체 정의·효과 초안은 SEMANTIC-CARDS.json과 CANDIDATE-DRAFTS.json, 계산값은 SWATCH-METRICS.json에 있다."]
    for card,metrics in zip(cards,metric_rows):
        doc += ["","## "+card["semantic_id"]+" "+card["label_ko"],"",
                "**계열:** "+card["group_label_ko"],"","**설계 의도:** "+card["meaning_ko"],"",
                "**관찰할 관계:** "+card["visual_relation_en"],"",
                "|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|","|---|---|---|---|"]
        for o in card["owner_binding_examples"]:
            c=metrics["colors"][o["color_index"]]
            doc.append("|"+o["hex_reference"]+"|"+o["owner_phrase_en"]+"|"+o["role_ko"]+"|"+str(c["oklch"]["L"])+" / "+str(c["oklch"]["C"])+"|")
        src_text=", ".join("["+s["source_id"]+" "+s["title"]+"]("+s["url"]+")" for s in source_rows if s["source_id"] in card["source_refs"])
        doc += ["","**오인 경계:** "+card["false_substitutes_ko"][0],"",
                "**연결:** "+", ".join(card["mechanism_card_ids"])+" · "+card["priority"],
                "", "**맥락 출처:** "+src_text,"",
                "**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다."]
    (BASE/"SEMANTIC-CARDS.md").write_text("\n".join(doc)+"\n")
    source_doc=["# 출처와 확인 범위","", "2026-10-06 KST · 원문 인용 없이 사실 범위와 제한을 요약했다.","",
                "검색 결과에서 확보한 공식 페이지의 텍스트와 직접 열린 본문/메타데이터를 구분한다. 일부 직접 열기는 오류 또는 내비게이션만 반환했다. 원본 작품·장면 이미지의 픽셀 관찰은 이 조사에서 수행하지 않았다."]
    for s in source_rows:
        source_doc += ["","## "+s["source_id"]+" ["+s["title"]+"]("+s["url"]+")","",
                       "- 자료 유형: "+s["source_type"],
                       "- 확인 방식: "+s["access_mode"],
                       "- 확인한 범위: "+s["supported_claim_ko"],
                       "- 제한: "+s["limit_ko"]]
    (BASE/"SOURCES.md").write_text("\n".join(source_doc)+"\n")
    build_atlas(cards,metric_rows,source_rows)
    low_light=[]
    for row in metric_rows:
        # Narrow spread is a review cue. It is not a failed photo or text contrast result.
        Ls=[c["oklch"]["L"] for c in row["colors"]]
        if max(Ls)-min(Ls)<0.18:low_light.append(row["seed_id"])
    result={"cards":len(cards),"mechanism_cards":len(mechanism_rows),"candidate_drafts":len(drafts),
            "sources":len(source_rows),"prototype_count":len(prototypes),
            "prototype_component_count":sum(len(p["profile"]["authored_components"]["components"]) for p in prototypes),
            "palette_color_refs":sum(len(x["hex_srgb_approximations"]) for x in seeds),
            "unique_hex_refs":len({h for s in seeds for h in s["hex_srgb_approximations"]}),
            "priorities":{p:sum(c["priority"]==p for c in cards) for p in ("P0","P1","P2")},
            "mechanisms":{m:sum(c["mechanism"]==m for c in cards) for m in sorted({c["mechanism"] for c in cards})},
            "small_modeled_lightness_spread_review_ids":low_light,
            "candidate_effect_structure":"PASS_ONLY_SYNTACTIC_SCOPE","prototype_component_compile":"PASS_ONLY_COMPONENT_PROJECTION",
            "owner_target_binding":"NOT_VERIFIED","runtime_adoption":"NOT_RUN","retrieval_qualification":"NOT_RUN",
            "native_pixels":"NOT_RUN","acceptance":"NOT_REQUESTED"}
    write("BUILD-RESULT.json",result)
    print(json.dumps(result,ensure_ascii=False))

if __name__=="__main__":main()
