#!/usr/bin/env python3
"""Rebuild research artifacts; never register or alter runtime assets."""
from __future__ import annotations
import copy, hashlib, json, re, subprocess, sys
from collections import Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
ASSETS=ROOT/".agents/skills/photo-prompt-image-generator/assets"
SCRIPTS=ROOT/".agents/skills/photo-prompt-image-generator/scripts"
def read(p): return json.loads(p.read_text())
def write(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(obj): return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def manifest(bases):
    return {str(p.relative_to(ROOT)):sha(p) for b in bases for p in sorted(b.rglob("*")) if p.is_file() and "__pycache__" not in str(p)}
parent_files={p.name:sha(p) for p in HERE.parent.iterdir() if p.is_file()}
runtime_files=manifest((ASSETS,SCRIPTS))
old=read(HERE.parent/"candidate-drafts.json")
seed=read(HERE/"research-additions.json")
snapshot=read(HERE/"source-conversation.json")
text="\n".join(i.get("text","") for t in snapshot["turns"] for i in t.get("items",[]) if i["type"]=="agentMessage")
(HERE/"source-conversation-text.md").write_text(text+"\n")
tables=[]; in_table=False; section=""
for lineno,line in enumerate(text.splitlines(),1):
    if line.startswith("#"): section=line
    if line.startswith("|"):
        if not in_table:
            tables.append({"section":section,"header_raw":line,"rows":[]}); in_table=True; continue
        if re.match(r"^\|[ :|-]+\|$",line): continue
        cells=[re.sub(r"\ue200[^\ue201]*\ue201","",c).strip() for c in line.strip("|").split("|")]
        tables[-1]["rows"].append({"source_line":lineno,"raw":line,"cells":cells})
    else: in_table=False
M=[
["fitted_medieval_dress,houppelande_bombard,veil_head_drape","gamurra_laced_sleeves,giornea_open_sides","tudor_forepart_cuffs,gable_hood,french_hood,ruff_repeated_loops","pointed_bodice_front,falling_band_shoulders,virago_sleeves","francaise_free_back,lateral_pannier,stomacher_insert","empire_raised_waist,spencer_over_gown,pelisse_long_coat","romantic_gigot","cage_crinoline","first_bustle,shelf_bustle","edwardian_bloused_front,lingerie_daydress","drop_waist_1920,cloche_bell","bias_draped_1930"],
["fitted_medieval_dress","fitted_medieval_dress","chemise_visible_layer","houppelande_bombard","mantle_shoulder_drape","houppelande_bombard","tippet_back_sleeve"],
["veil_head_drape","wimple_chin_neck","barbette_underchin_band","fillet_head_band","conical_turret_veil","headcloth_hair_wrap"],
["fitted_medieval_dress,mantle_shoulder_drape","fitted_medieval_dress,headcloth_hair_wrap","headcloth_hair_wrap,matte_woven_cloth","mantle_shoulder_drape","overskirt_layering","tippet_back_sleeve,veil_head_drape"],
["gamurra_laced_sleeves","giornea_open_sides","french_hood","gable_hood","ruff_repeated_loops","spanish_conical_support,wheel_farthingale","pointed_bodice_front","falling_band_shoulders","court_mantua"],
["francaise_free_back","anglaise_fitted_back","polonaise_three_lifts","lateral_pannier","stays_structure_display","stomacher_insert","engageantes_sleeve_ends","fichu_shoulders","chemise_gown_sash"],
["empire_raised_waist","spencer_over_gown","pelisse_long_coat","cage_crinoline","first_bustle,shelf_bustle","overskirt_layering","romantic_gigot,1890s_gigot_knit","shirtwaist_separate_skirt"],
["","pelisse_long_coat","","","tea_gown_fitted_drape","mourning_crepe","edwardian_bloused_front","lingerie_daydress","drop_waist_1920","cloche_bell","bias_draped_1930"],
["matte_woven_cloth","velvet_pile_surface","satin_reflection","taffeta_structured_folds","brocade_raised_motifs,damask_tonal_pattern","muslin_light_layers","lace_insertion,embroidered_cuffs,fine_pintucks","ribbon_rosettes,layered_flounces","metal_thread_embroidery"],
["","","","","","reticule_handheld_bag,mantle_shoulder_drape","chatelaine_waist_tools"],
["chima_jeogori_layers,jangot_headcover,sseugaechima_headcover","dangui_open_sides,chima_jeogori_layers","gaeryang_hanbok_1920","kosode_small_opening,kimono_obi_wrap","qing_embroidered_robe,qing_jacket_skirt","qipao_1920_loose,qipao_1930_shaped"],
["fitted_medieval_dress,mantle_shoulder_drape,veil_head_drape","headcloth_hair_wrap,matte_woven_cloth","gamurra_laced_sleeves,giornea_open_sides","tudor_forepart_cuffs,gable_hood","satin_reflection,falling_band_shoulders","francaise_free_back,stomacher_insert,engageantes_sleeve_ends","empire_raised_waist,spencer_over_gown","mourning_crepe,veil_head_drape","shirtwaist_separate_skirt","lingerie_daydress","drop_waist_1920,cloche_bell","bias_draped_1930"],
["","","","","","","",""]]
assert len(tables)==len(M)==13
candidates=copy.deepcopy(old["candidate_drafts"])+copy.deepcopy(seed["candidate_drafts"])
byid={c["id"]:c for c in candidates}
assert len(byid)==len(candidates)
alignment=[]
for ti,(table,maps) in enumerate(zip(tables,M),1):
    assert len(table["rows"])==len(maps),(ti,len(table["rows"]),len(maps))
    for ri,(row,ids) in enumerate(zip(table["rows"],maps),1):
        ids=["hw_"+x for x in ids.split(",") if x]
        cat="garment_or_detail"
        if ti==1: cat="era_navigation_not_single_uniform"
        if ti in (4,12): cat="creative_scene_not_historical_evidence"
        if ti==8 and ri<=5: cat="occasion_requires_dated_variant"
        if ti==9: cat="material_or_surface_design"
        if ti==10: cat="prop_action_recipe_requires_period_check"
        if ti==13: cat="capture_direction_not_garment_era"
        alignment.append({**row,"id":f"T{ti:02d}R{ri:02d}","table":ti,"section":table["section"],"category":cat,"candidate_ids":ids,"alignment_status":"mapped","historical_verification":"not_implied_by_source_alignment"})
        for cid in ids: assert cid in byid,cid
assert len(alignment)==110
notes=[
{"id":"P01","source_lines":[60,64],"keyword":"hennin / conical headdress","policy":"검색 별칭 hennin 유지; 원뿔과 베일의 형태·시대는 별도 판정.","candidate_ids":["hw_conical_turret_veil"]},
{"id":"P02","source_lines":[260,262],"keyword":"lens / full-length / three-quarter rear","policy":"렌즈·조리개는 시작값. 요구 특징을 보이는 시점과 해상도를 확보.","candidate_ids":[]},
{"id":"P03","source_lines":[268,280],"keyword":"four example prompts","policy":"4개 예시는 창작 레시피. 프랑세즈 등 주름 판정에는 후면이 필요.","candidate_ids":[]},
{"id":"P04","source_lines":[286,288],"keyword":"Pre-Raphaelite-inspired medieval romance","policy":"19세기 중세 재해석과 실제 중세 표본을 구분.","candidate_ids":["hw_aesthetic_shoulder_fall"]},
{"id":"P05","source_lines":[290,292],"keyword":"fitted gown / stays / corset","policy":"서로 다른 시대와 구성. 불투명 옷 내부를 픽셀 의무로 요구하지 않음.","candidate_ids":["hw_fitted_medieval_dress","hw_stays_structure_display"]},
{"id":"P06","source_lines":[294,296],"keyword":"court / everyday / social roles","policy":"서사의 역할과 보이는 옷을 구별. 사진에서 신분·직업을 추정하지 않음.","candidate_ids":[]},
{"id":"P07","source_lines":[298,300],"keyword":"daguerreotype / modern recreation","policy":"의복 시대와 촬영 공정 독립. 중세 당시 실제 사진이라는 주장을 생성하지 않음.","candidate_ids":[]}]
oldids={c["id"] for c in old["candidate_drafts"]}
for c in candidates:
    c["source_row_ids"]=[r["id"] for r in alignment if c["id"] in r["candidate_ids"]]
    c["source_prose_ids"]=[r["id"] for r in notes if c["id"] in r["candidate_ids"]]
    if c["id"] in oldids:
        c["previous_keyword_origin"]=c.pop("keyword_origin",None)
        c["keyword_origin"]="reference_aligned_existing_draft" if c["source_row_ids"] else "adjacent_extension_beyond_source_tables"
        c["reference_conversation_alignment"]="mapped_to_source" if c["source_row_ids"] or c["source_prose_ids"] else "adjacent_comparative_candidate"
        c["readiness"]="draft_needs_case_qualification" if c["status"]=="proposed" else c["status"]
    c["runtime_importable"]=False
    c["basis_boundary"]="기관의 역사·구조 주장과 연구자가 설계한 관찰 문구를 분리. 원문 매핑은 고증 통과를 뜻하지 않음."
    c["affected_dimension_proposal"]={"garment_structure":"appearance","surface_material":"material","body_geometry":"do_not_change_from_costume_label"}
    c["visibility_policy"]="특징이 가려지거나 잘리면 충족으로 간주하지 않는다. 불투명 옷 내부는 판독 불가로 기록한다."
def amend(cid,reason,sources=None,components=None,limits=None):
    c=byid[cid]; c.setdefault("source_aligned_revisions",[]).append(reason)
    if sources: c["source_ids"]=sources
    if components: c["components"]=[{"id":f"component_{i+1}","proposed_slot":s,"phrase_en":p} for i,(s,p) in enumerate(components)]
    if limits: c.setdefault("claim_limits_ko",[]).extend(limits)
amend("hw_fitted_medieval_dress","1540년대 자료 S09를 중세 직접 근거에서 제거.",["S02","S03"],limits=["Kirtle/Cotte/Cotehardie의 용례 차이를 보존. 이 후보는 밀착 변형이며 모든 커틀이 밀착하거나 앞 끈으로 닫히는 것은 아님."])
amend("hw_gamurra_laced_sleeves","사각 목선은 선택 표본. 분리 소매 접합은 S07로 보강.",["S06","S07"],limits=["둥근 목선·다른 소매 여밈 변형까지 배제하지 않음."])
amend("hw_giornea_open_sides","자료에 열린 옆선·닫힌 옆선 모두 존재.",limits=["열린 옆선은 선택 변형. Giornea 명칭만으로 전부 강제하지 않음."])
amend("hw_anglaise_fitted_back","후면 판별 번들에서 동시에 보기 어려운 앞 페티코트 조건을 분리.",components=[("garment_detail","the gown back is shaped closely to the waist"),("garment_detail","the gown skirt spreads below the shaped back waist")],limits=["앞 열림은 hw_overskirt_layering에서 별도 판정. 후면 판별에 정면 사진을 요구하지 않음."])
amend("hw_conical_turret_veil","원문 명칭 논점과 원뿔 구조를 분리.",limits=["hennin은 현대 검색 별칭으로 유지; 특정 학설을 이미지 판정 규칙으로 만들지 않음."])
byid["hw_conical_turret_veil"]["search_terms"]+=["hennin","haut bonnet","헤닌"]
amend("hw_court_mantua","원문 late17c mantua와 NMS 18c court mantua 범위 분리.",limits=["후보는 18세기 궁정형. 초기 만투아 전체를 넓은 치마로 고정하지 않음.","NMS 원래 스토머커는 소실. 전시 보완 부품을 해당 원형의 실물로 취급하지 않음."])
amend("hw_lateral_pannier","측면 폭의 근거를 기존18c 자료·실물로 보강.",["S18","S21","S22"],limits=["정면만으로 앞뒤 깊이까지 판독하지 않음. 몸의 골반 폭 확대 요청이 아님."])
amend("hw_chemise_gown_sash","1780년대 자연 허리 새시와 뒤의 높은 허리선 분리.",["S21","S23"],[("costume_style","a lightweight gown forms soft gathers through the bodice and skirt"),("garment_detail","a sash gathers the chemise gown near the natural waist")],["자연 허리 변형. 엠파이어 허리로 자동 상승시키지 않음."])
amend("hw_cage_crinoline","내부 구조 전시와 완성 드레스 외곽선은 별도 시험.",limits=["후보는 노출한 케이지 구조용. 불투명 완성복을 뚫고 후프·테이프가 보이면 실패.","crinoline은 초기 직물·페티코트 의미도 있으므로 cage 범위 유지."])
amend("hw_crinolette_rear","내부 지지 구조가 보이는 전시·분석 사례.",limits=["불투명 완성복에서 반후프의 실재를 픽셀로 단정하지 않음."])
amend("hw_edwardian_bloused_front","앞 부피를 신체가 아닌 블라우스 원단에 귀속.",limits=["가슴 크기·척추 굴곡 강제 금지. 원단 블라우징과 속 코르셋은 다른 검증 대상."])
amend("hw_sseugaechima_headcover","긍정 문구의 부정형을 연속 천 관계로 변경.",components=[("wearable_accessory","a skirt-shaped sseugaechima falls from a gathered band over the crown"),("wearable_accessory","two ties from the sseugaechima band meet below the chin"),("garment_detail","the gathered skirt cloth continues down both sides of the head covering")])
amend("hw_spanish_conical_support","긍정 문구를 연속 경사 형태로 한정.",components=[("garment_detail","the gown skirt widens steadily from the waist toward a broad hem"),("garment_detail","the gown upper skirt follows a continuous sloping outline")])
for cid in ("hw_french_hood","hw_gable_hood"):
    byid[cid]["readiness"]="needs_original_portrait_crosscheck"
    byid[cid].setdefault("claim_limits_ko",[]).append("S11 영화 분석은 원 초상 대체 근거가 아님. 원 초상 대조 전 번들 미포함.")
byid["hw_virago_sleeves"]["readiness"]="source_reopen_failed_hold"
byid["hw_bliaut_layered_sleeves"]["readiness"]="outside_core_scope_and_full_source_pending"
byid["hw_sideless_surcoat"]["readiness"]="needs_primary_shape_evidence"
amend("hw_francaise_free_back","독립 슬롯에서도 주름의 소유 의복을 명시.",components=[("garment_detail","deep box pleats originate at the gown upper back neckline"),("garment_detail","the gown back pleats descend freely past the waist into the skirt")])
amend("hw_lateral_pannier","대명사 대신 치마를 반복해 독립 후보의 소유 대상을 고정.",components=[("garment_detail","the gown skirt extends strongly to the left and right of the waist"),("garment_detail","the gown skirt has less front-to-back depth than lateral width")])
amend("hw_empire_raised_waist","몸판과 치마를 가운의 구성요소로 명시.",components=[("garment_detail","the gown bodice ends immediately below the bust"),("garment_detail","the gown skirt descends from the raised bodice seam in a relatively narrow column")])
amend("hw_stomacher_insert","앞판과 몸판의 의복 소유권 명시.",components=[("garment_detail","a distinct stomacher panel tapers downward inside the gown bodice opening"),("garment_detail","the outer gown bodice edges frame the inserted stomacher panel")])
amend("hw_shelf_bustle","후방 돌출을 가운 치마에 귀속.",components=[("garment_detail","the gown skirt projects sharply backward just below the waist"),("garment_detail","the gown rear skirt falls from the elevated projecting mass")])
amend("hw_polonaise_three_lifts","들어 올리는 대상을 가운의 겉치마로 명시.",components=[("garment_detail","the gown overskirt is drawn up into three distinct draped sections"),("garment_detail","a separate petticoat remains visible below the lifted gown overskirt")])
for c in candidates:
    for component in c["components"]:
        if component["proposed_slot"]=="silhouette_proportion":
            component["previous_proposed_slot"]="silhouette_proportion"
            component["proposed_slot"]="garment_detail"
    c["proposed_slot_members"]=[{"id":f"{c['id']}_{i}","slot":component["proposed_slot"]} for i,component in enumerate(c["components"],1)]
sources=copy.deepcopy(old["source_records"])+copy.deepcopy(seed["source_records"])
rechecks={"S02":"page_text","S03":"page_text","S05":"page_text","S06":"page_text","S07":"page_text","S14":"page_text","S16":"page_text","S17":"page_text","S18":"page_text_and_image","S19":"page_text","S20":"page_text_and_image","S21":"page_text","S24":"page_text","S25":"catalog_metadata","S26":"page_text","S29":"page_text","S37":"page_text"}
for s in sources:
    if s["id"].startswith("S"):
        s["previous_access_status"]=s["access_status"]
        s["current_pass_access_status"]=rechecks.get(s["id"],"inherited_not_rechecked")
        if s["id"]=="S15": s["current_pass_access_status"]="open_failed_internal_error"
    else: s["current_pass_access_status"]=s["access_status"]
sourceids={s["id"] for s in sources}
for c in candidates:
    assert set(c["source_ids"])<=sourceids
    c["source_check_summary"]={sid:next(s["current_pass_access_status"] for s in sources if s["id"]==sid) for sid in c["source_ids"]}
write("source-ledger.json",{"schema_version":"historical-womenswear-source-ledger/v2","created_on":"2026-09-08","sources":sources,"rule":"supported_claim 범위만 인용. inherited_not_rechecked는 이번에 다시 읽었다는 뜻이 아님."})
write("keyword-alignment.json",{"schema_version":"historical-womenswear-keyword-alignment/v2","conversation_id":snapshot["conversation_id"],"conversation_sha256":sha(HERE/"source-conversation.json"),"table_count":13,"row_count":110,"rows":alignment,"prose_notes":notes})
write("candidate-drafts.v2.json",{"schema_version":"historical-womenswear-candidate-drafts/v2","status":"research_proposal_not_adopted","runtime_importable":False,"source_conversation_sha256":sha(HERE/"source-conversation.json"),"historical_scope":"원문 중심: 유럽14–1930년대, 한국·일본·중국 선택 사례. 인접 후보는 별도 표시.","candidate_drafts":candidates})
source_asset_files=[p for p in sorted(ASSETS.glob("*.json")) if "index" not in p.name]
entries=[]
for p in source_asset_files:
    for slot,values in read(p).get("slots",{}).items():
        for e in values: entries.append((p.name,slot,e))
coverage=[]
for c in candidates:
    hits=[]; terms=[t.casefold() for t in c["search_terms"] if len(t)>2]
    for fn,slot,e in entries:
        hay=json.dumps(e,ensure_ascii=False).casefold(); matched=[t for t in terms if t in hay]
        if matched: hits.append({"file":fn,"slot":slot,"id":e["id"],"en":e.get("en"),"matched_terms":matched})
    coverage.append({"candidate_id":c["id"],"lexical_hits":hits,"semantic_coverage":"manual_decision_required","no_hit_is_not_semantic_absence":True})
write("local-coverage.v2.json",{"schema_version":"historical-womenswear-local-coverage/v2","git_head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),"method":"Case-folded literal substring search of authored top-level asset slot entries; excludes generated indexes/shards. Not an embedding or routing test.","files":[{"path":str(p.relative_to(ROOT)),"sha256":sha(p)} for p in source_asset_files],"coverage":coverage})
chosen=["francaise_free_back","anglaise_fitted_back","polonaise_three_lifts","lateral_pannier","stomacher_insert","chemise_gown_sash","empire_raised_waist","shelf_bustle","tippet_back_sleeve","wimple_chin_neck","barbette_underchin_band","lingerie_daydress","drop_waist_1920","cloche_bell","jangot_headcover","sseugaechima_headcover","dangui_open_sides","kosode_small_opening","qing_embroidered_robe","qipao_1920_loose","lace_insertion","brocade_raised_motifs","damask_tonal_pattern","chatelaine_waist_tools"]
rels={
"francaise_free_back":("originates_at","gown back pleats","upper back neckline"),
"anglaise_fitted_back":("shaped_to","gown back","gown waist"),
"polonaise_three_lifts":("reveals_below","lifted gown overskirt","separate petticoat"),
"lateral_pannier":("greater_than","skirt lateral width","skirt front-to-back depth"),
"stomacher_insert":("framed_by","stomacher front panel","outer bodice edges"),
"chemise_gown_sash":("gathers_at","gown sash","natural waist level"),
"empire_raised_waist":("descends_from","gown skirt","raised bodice seam"),
"shelf_bustle":("projects_behind","gown rear skirt","gown waist"),
"tippet_back_sleeve":("attached_to","tippet strip","back of gown upper sleeve"),
"wimple_chin_neck":("covers","same wimple cloth","underside of chin and neck"),
"barbette_underchin_band":("passes_under","barbette band","chin"),
"lingerie_daydress":("joins","dress lace insertion","outer garment fabric panels"),
"drop_waist_1920":("below","dress waist seam","wearer's natural waist"),
"cloche_bell":("fits_around","cloche crown","head"),
"jangot_headcover":("belongs_to","hanging sleeves","coat-shaped head covering"),
"sseugaechima_headcover":("continues_from","gathered head-covering cloth","skirt waistband"),
"dangui_open_sides":("separates","dangui side slit","long front and back jacket panels"),
"kosode_small_opening":("part_of","small wrist opening","larger kosode sleeve panel"),
"qing_embroidered_robe":("embroidered_on","butterfly motifs","robe fabric"),
"qipao_1920_loose":("belongs_to","wide long sleeves","loose cheongsam body"),
"lace_insertion":("joins","lace strip","two blouse fabric panels"),
"brocade_raised_motifs":("woven_into","brocaded motifs","textile ground"),
"damask_tonal_pattern":("alternates_with","matte motif area","lustrous motif area within same cloth"),
"chatelaine_waist_tools":("suspended_from","tool case","waist clasp")}
policy=read(ASSETS/"photo_prompt_tags.json")["candidate_semantic_policy"]
ext={"schema_version":"photo-prompt-historical-womenswear-proposal/v1","slots":{},"visual_semantics":[]}
for short in chosen:
    c=byid["hw_"+short]; members=[]; scopes={}; groups=[]
    for i,comp in enumerate(c["components"],1):
        slot=comp["proposed_slot"]
        if slot=="silhouette_proportion": slot="garment_detail"
        dims=policy["slot_dimensions"].get(slot,[])
        assert dims and "body_geometry" not in dims,(c["id"],slot,dims)
        eid=f"{c['id']}_{i}"
        entry={"id":eid,"ko":c["label_ko"],"en":comp["phrase_en"],"weight":1.0,"tags":["historical_garment_component"],"keywords":[c["label_en"],comp["phrase_en"]],"embedding_text":comp["phrase_en"],"concept_units":[comp["phrase_en"]],"affected_dimensions":dims}
        ext["slots"].setdefault(slot,[]).append(entry); members.append(eid); scopes[eid]=slot
        groups.append({"id":comp["id"],"visible_evidence":[comp["phrase_en"]]})
    t,sub,obj=rels[short]
    ext["visual_semantics"].append({"id":c["id"],"primary_visual_proposition":c["label_en"],"component_groups":groups,"candidate_ids":members,"candidate_slots":scopes,"hard_profile_ids":[],"relations":[{"id":"relation_1","type":t,"subject":sub,"object":obj}],"confusion_boundaries":c["confusion_boundaries_ko"],"candidate_only":True})
maintenance={"record_id":"historical_womenswear_source_aligned_20260908","status":"research_proposal_unregistered","source_ledger_sha256":sha(HERE/"source-ledger.json"),"candidate_drafts_sha256":sha(HERE/"candidate-drafts.v2.json"),"conversation_sha256":sha(HERE/"source-conversation.json"),"source_ids":sorted({s for short in chosen for s in byid["hw_"+short]["source_ids"]}),"excluded_from_positive_runtime_text":["historical_source_prose","social_status_inference","review_status","citation_urls","claim_limits"],"adoption_boundary":"Compiler validation is not exposure, activation or rendering evidence."}
write("maintenance-record.json",maintenance)
ext["maintenance_ref"]={"contract_version":"photo-extension-maintenance-ref/v1","record_id":maintenance["record_id"],"sha256":digest(maintenance)}
write("optional-extension.proposed.json",ext)
sys.dont_write_bytecode=True
sys.path.insert(0,str(SCRIPTS))
import photo_candidate_semantics as semantics
allowed=set(d for ds in policy["slot_dimensions"].values() for d in ds)
semantics.validate_extension_keys(ext)
data={"slots":copy.deepcopy(ext["slots"]),"candidate_semantic_policy":copy.deepcopy(policy)}
semantics.validate_candidate_entries(data,allowed)
semantics.compile_extension_bundles(data,ext)
semantics.validate_bundle_references(data,[])
assert len(data["candidate_bundles"])==len(chosen)
for raw,compiled in zip(ext["visual_semantics"],data["candidate_bundles"]):
    assert compiled["source_sha256"]==digest(raw)
    assert compiled["adoption"]=="optional" and compiled["profile_activation"]=="independent_request_evidence_only"
    assert compiled["associated_profile_ids"]==[]
    assert len(compiled["member_candidates"])<=policy["joint_adoption"]["maximum_members_per_bundle"]
assert not {e["id"] for _,_,e in entries}.intersection(e["id"] for es in ext["slots"].values() for e in es)
write("compiled-bundles.preview.json",{"status":"compiler_output_only_not_registered","candidate_bundles":data["candidate_bundles"]})
assert parent_files=={p.name:sha(p) for p in HERE.parent.iterdir() if p.is_file()}
assert runtime_files==manifest((ASSETS,SCRIPTS))
checks={"schema_version":"historical-womenswear-artifact-check/v2","status":"pass_for_listed_structural_checks_only","source_table_count":13,"mapped_source_rows":110,"unmapped_source_rows":0,"source_prose_notes":len(notes),"research_candidates":len(candidates),"new_candidates":len(seed["candidate_drafts"]),"candidate_components":sum(len(c["components"]) for c in candidates),"sources_total":len(sources),"new_sources":len(seed["source_records"]),"source_access_counts":dict(Counter(s["current_pass_access_status"] for s in sources)),"proposed_bundles":len(chosen),"proposed_slot_members":sum(map(len,ext["slots"].values())),"proposed_slots":list(ext["slots"]),"checks":{k:"pass" for k in ["source_row_mapping","unique_candidate_ids","source_references","extension_top_level_schema","candidate_entry_validation","real_bundle_compiler","bundle_reference_validation","source_hash_bindings","no_existing_slot_id_collision","nonempty_owned_dimensions","no_body_geometry_from_garments","max_members_per_bundle","parent_files_preserved","runtime_assets_and_scripts_preserved"]},"not_run":["full_extension_loader","maintenance_registry_resolution","BM25F_or_embedding_index_rebuild","candidate_exposure","hard_profile_activation","prompt_generation","image_generation","rendered_pixel_evaluation","user_judgment"],"no_runtime_registration":True,"parent_file_sha256":parent_files,"runtime_manifest_sha256":digest(runtime_files),"commands":["python3 docs/research-evidence/photo-prompt/historical-womenswear-20260908/source-aligned/build_research.py"]}
write("artifact-check.v2.json",checks)
lines=["# 원문 키워드 대조표","","원문13개 표의110개 데이터 행을 모두 대조했다. 매핑은 역사 검증 통과를 뜻하지 않는다.","","| 원문 ID / 행 | 키워드 | 처리 유형 | 연결 후보 |","|---|---|---|---|"]
for r in alignment:
    label=re.sub(r"\*\*","",r["cells"][0]).replace(chr(96),"").replace("|","/")
    lines.append(f"| {r['id']} / {r['source_line']} | {label} | {r['category']} | {', '.join(r['candidate_ids']) or '맥락/레시피로 유지; 의복 후보 강제 생성 없음'} |")
lines+=["","## 표 밖의 범위·주의점",""]+[f"- {r['id']} ({r['source_lines'][0]}–{r['source_lines'][1]}행): **{r['keyword']}** — {r['policy']}" for r in notes]
(HERE/"keyword-alignment.md").write_text("\n".join(lines)+"\n")
print(json.dumps(checks,ensure_ascii=False,indent=2))
