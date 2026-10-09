"""Compile research documents. This does not register, rebuild or publish runtime data."""
from pathlib import Path
import csv, hashlib, importlib.util, json, re
from collections import Counter
from datetime import datetime, timezone, timedelta
from authored_research import SOURCES, CARDS, GROUP_MAP
from regression_design import PAIR_ROWS, COMBINATION_ROWS, MUTATIONS, PIXEL_ROWS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

REVIEWED = {
 2:["pfe_midriff_candidate"],4:["sw_candidate_bandeau","y2kr_bandeau"],
 5:["clt_ct038_v1"],8:["clt_ct018_v1"],11:["clt_ct064_v1","clt_ct064_v2"],
 28:["cold_shoulder_cutout_sleeve_bridge"],33:["fit_ff09_v1_candidate"],
 35:["fit_ff52_v1_candidate","fit_ff52_v2_candidate","crossback_strap_intersection"],
 38:["pfe_skimming_candidate"],42:["bias_cut_body_skimming_drape"],
 48:["clt_ct031_v1"],50:["pfe_lateral_chest_candidate","pfe_lower_chest_candidate"],
 51:["pfe_midriff_candidate"],55:["y2kr_whale_tail"],65:["sw_candidate_wrapcover"],
 78:["sw_candidate_triangle"],79:["sw_candidate_bandeau"],
 80:["sw_candidate_tankini","sw_candidate_onepiece"],81:["sff_extra_xa005"],
 83:["sw_candidate_highleg"],91:["sw_candidate_coverup"],
 98:["broderie_anglaise_eyelet"],100:["clt_ct065_v1","clt_ct065_v2"],
 112:["fisherman_sandals"],118:["clt_ct113_v2"]
}
P0 = {2,5,28,35,37,50,51,54,79,80,81,83,85,93,98,112,118}

def write_json(name, value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")

def action(card):
    num=int(card["id"][2:])
    if not card["variants"]: return "preserve_specification_no_automatic_pixel_candidate"
    if num==81: return "split_historical_and_modern_context_before_reuse"
    if num in REVIEWED: return "reuse_meaning_review_relation_and_effect_scope"
    return "review_equivalents_then_add_or_extend_visible_variant"

def main():
    audit=json.loads((HERE/"current-source-audit.json").read_text())
    inventory=json.loads((HERE/"term-inventory.json").read_text())
    records=json.loads((HERE/"current-positive-records.json").read_text())
    additional=json.loads((HERE/"additional-reviewed-records.json").read_text())
    for row in additional:
        assert row["source_sha256"]==audit["source_sha256"][row["source"]],row["source"]
    records += additional
    current={r["id"]:r for r in records if r["kind"]=="slot_candidate"}
    groups=list(dict.fromkeys(t["group"] for t in inventory))
    assert len(groups)==len(GROUP_MAP)==24
    assert len(inventory)==299 and len(CARDS)==118
    assert all(cid in current for ids in REVIEWED.values() for cid in ids), [
        cid for ids in REVIEWED.values() for cid in ids if cid not in current]
    term_map={}
    for group, assignments in zip(groups,GROUP_MAP):
        terms=[t for t in inventory if t["group"]==group]
        assert len(terms)==len(assignments),(group,len(terms),len(assignments))
        for term,cid in zip(terms,assignments): term_map[term["id"]]=f"SF{cid:03d}"
    cards={c["id"]:c.copy() for c in CARDS}
    sources={s["id"]:s for s in SOURCES}
    known_paths=set(audit["candidate_property_paths"])
    proposals=[]
    for cid,c in cards.items():
        num=int(cid[2:])
        c["seed_term_ids"]=[tid for tid,cardid in term_map.items() if cardid==cid]
        c["seed_terms"]=[t["term"] for t in inventory if t["id"] in c["seed_term_ids"]]
        c["priority"]="P0" if num in P0 else "P1" if num<104 else "P2"
        c["recommended_action"]=action(c)
        c["reviewed_existing_candidate_ids"]=REVIEWED.get(num,[])
        c["scope_status"]="existing_candidate_property_family" if c["property_family"] in known_paths else "proposed_family_requires_schema_and_effect_review"
        c["proposed_candidate_ids"]=[]
        c["evidence_limits"]=[
            "씨앗 표와 출처의 가족 매핑이며 행 내 모든 별칭의 독립 재검증은 아니다.",
            "관찰 문장·연결 그래프·프레이밍은 연구자가 제안한 선택형 실현이며 출처의 원문 인용이 아니다.",
            "소스/후보 ID 존재나 토큰 이웃은 의미 동등성·실제 검색·채택·픽셀·선호의 증거가 아니다."
        ]
        for i,v in enumerate(c["variants"],1):
            pid=f"draft_summer_{cid.lower()}_v{i}"
            units=[x.strip() for x in v["prompt_en"].split(";") if x.strip()]
            # IDs are research-local. The draft has no owner resolver, activation
            # policy, profile or registration and must not be copied wholesale.
            draft=dict(id=pid,ko=c["title"],en=v["prompt_en"],concept_units=units,
                       relations=[dict(id=f"{pid}_relation",**v["relation"])],
                       affected_dimensions=["appearance"],
                       affected_properties=[dict(dimension="appearance",target="main_subject",property=c["property_family"])])
            proposal=dict(id=pid,card_id=cid,slot=c["slot"],payload_draft=draft,
                          owner_binding_proposal=c["owner"],scope_status=c["scope_status"],
                          scope_review_status="requires_complete_per_variant_effect_review",
                          source_ids=c["source_ids"],recommended_action=c["recommended_action"],
                          reviewed_existing_candidate_ids=c["reviewed_existing_candidate_ids"],
                          adoption="optional_only_after_frozen_core_and_explicit_choice",
                          selection_conditions=[
                              "요청 문맥이 이 의복 owner와 선택 변형을 실제로 지지한다.",
                              "appearance와 모든 실제 변경 property가 해당 core/intent-lock에서 허용된다.",
                              "고정된 identity/body_geometry/가림 부위 의미를 새로 바꾸지 않는다.",
                              "관계 evidence와 채택된 구성 요소의 literal evidence를 모두 작성한다."
                          ],
                          observation_condition=c["observation_condition"],
                          rejection_boundary=c["confusion_boundary"],
                          render_gate_drafts=[
                              dict(id=f"{pid}_unit_{j}",description=u,scale="native",
                                   status="planned_not_executed") for j,u in enumerate(units,1)
                          ]+[dict(id=f"{pid}_owner_relation",description=v["relation"],
                                  scale="native",status="planned_not_executed")],
                          proof_status=dict(research="authored",runtime_registered=False,
                                            retrieval_executed=False,composition_executed=False,
                                            pixel_verified=False,user_accepted=False))
            proposals.append(proposal);c["proposed_candidate_ids"].append(pid)
    term_plan=[]
    for t in inventory:
        c=cards[term_map[t["id"]]]
        neighbors=t["lexical_neighbors"]
        term_plan.append(dict(term_id=t["id"],group=t["group"],term=t["term"],card_id=c["id"],
                              action=c["recommended_action"],priority=c["priority"],slot=c["slot"],
                              owner=c["owner"],property_family=c["property_family"],scope_status=c["scope_status"],
                              source_ids=c["source_ids"],related_family_draft_ids=c["proposed_candidate_ids"],
                              reviewed_existing_candidate_ids=c["reviewed_existing_candidate_ids"],
                              lexical_neighbor_count=len(neighbors),
                              lexical_neighbors=neighbors,
                              evidence_level="family_sources_plus_researcher_visual_decomposition",
                              semantic_equivalence_status="requires_variant_specific_review",
                              candidate_assignment_status="family_inventory_only_not_direct_alias_mapping"))
    write_json("source-ledger.json",list(sources.values()))
    write_json("semantic-cards.json",list(cards.values()))
    write_json("candidate-proposals.json",proposals)
    write_json("term-plan.json",term_plan)
    fields=["term_id","group","term","card_id","action","priority","slot","owner","property_family",
            "scope_status","source_ids","related_family_draft_ids","reviewed_existing_candidate_ids",
            "lexical_neighbor_count","evidence_level","semantic_equivalence_status","candidate_assignment_status"]
    with (HERE/"term-plan.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for row in term_plan:
            writer.writerow({k:";".join(row[k]) if isinstance(row[k],list) else row[k] for k in fields})
    md=["# 여름 패션 상세 시각 의미 카드","",
        "각 카드는 가족 단위 연구 기록이다. 같은 카드의 variant는 독립 선택형이며 모두 동시에 요구하지 않는다.",
        "출처는 정의/문맥의 근거, 연결 그래프와 영문 관찰 문장은 연구자의 반영 제안이다. runtime-ready 데이터가 아니다.",""]
    for c in cards.values():
        md += [f"## {c['id']} · {c['title']}", "",
               f"씨앗: {', '.join(c['seed_terms'])}","",
               f"의미: {c['meaning_ko']}","",
               f"소유자: {c['owner']}. 제안 슬롯: `{c['slot']}`. 속성 가족: `{c['property_family']}` ({c['scope_status']}).","",
               f"혼동 경계: {c['confusion_boundary']}","",
               f"관찰 조건: {c['observation_condition']}","",
               f"처리: {c['priority']} / {c['recommended_action']}. 기존 검토 ID: {', '.join(c['reviewed_existing_candidate_ids']) or '행별 lexical neighbor를 검토한 뒤 결정'}.","",
               "출처: "+", ".join(f"[{sources[s]['title']}]({sources[s]['url']})" for s in c["source_ids"])+".",""]
        if not c["variants"]:
            md += ["명세/물품 유형을 보존하되 이번에는 자동 픽셀 후보를 만들지 않는다. 별도 관찰 가능한 물품 시점이 필요한 경우 후속 승격에서 작성한다.",""]
        for i,v in enumerate(c["variants"],1):
            r=v["relation"]
            md += [f"- 독립 변형 {i}: {v['prompt_en']}",
                   f"  관계: {r['subject']} → {r['type']} → {r['object']}.",""]
    (HERE/"semantic-cards.md").write_text("\n".join(md)+"\n")
    reg=dict(status="planned_not_executed",comparison_pairs=[
        dict(id=f"SP{i:02d}_{slug}",a=a,b=b,expected=exp,card_ids=[f"SF{x:03d}" for x in ids])
        for i,(slug,a,b,exp,*ids) in enumerate(PAIR_ROWS,1)],
        allowed_combinations=[dict(id=slug,card_ids=[f"SF{x:03d}" for x in ids],expected=exp)
                              for slug,ids,exp in COMBINATION_ROWS],
        mutations=[dict(id=slug,change=change,expected=exp) for slug,change,exp in MUTATIONS],
        pixel_groups=[dict(id=slug,card_ids=[f"SF{x:03d}" for x in ids],
                           capture_condition=cap,required_boundary=boundary,
                           all_of_required=True,occlusion="UNOBSERVABLE_NOT_PASS",
                           status="planned_not_rendered") for slug,ids,cap,boundary in PIXEL_ROWS],
        proof_layers=["authored_source","index_integrity","retrieval","adoption_and_composed_audit",
                      "runtime_transport","native_pixels","user_acceptance"],
        retrieval_protocol=[
            "원문 labels/별칭, 새로 쓴 한국어·영어 관찰형 paraphrase, negation, homonym을 각각 사용.",
            "authorial core를 각 request에서 독립 작성·freeze한 뒤에만 live retrieval 실행.",
            "선택 품질·출현 여부와 similarity score 자체를 hard authority로 혼동하지 않음.",
            "paired positives가 원하는 owner/relation을 회수하고 adjacent/homonym negatives에 exact hard leak이 없는지 확인.",
            "모든 선택 relation과 unit literal evidence, effect lock, selected profile gate 전파를 감사.",
            "현재 계획에서 임베딩·검색·composition·render는 실행하지 않았다."
        ])
    write_json("regression-plan.json",reg)
    plan=dict(status="research_complete_implementation_not_started",baseline_head=audit["head"],
              preferred_strategy="reuse_domain_owners_before_creating_any_summer_extension",
              phases=[
                  dict(id="W0",purpose="원본 의미 동등성 및 source 소유권 확정",deliverable=f"299행에서 재사용/수정/신규/명세-only 최종 판정; {len(proposals)} drafts 중 실제 승격 수 결정",
                       checks=["source snapshot 최신성 재확인","monokini historical/modern split","현재 lexical 이웃을 단어 일치로 병합하지 않기"]),
                  dict(id="W1",purpose="핵심 경계와 잘못된 의미 전이 방지",cards=[f"SF{x:03d}" for x in sorted(P0)],
                       deliverable="형상·앞뒤·층·끈·커버리지 독립 축, broad label/negation/homonym 반례"),
                  dict(id="W2",purpose="기존 후보/프로필 관계 및 effect scope 보강",
                       source_targets=["photo_prompt_swimwear_extension.json","photo_prompt_visual_obligations_swimwear.json",
                                       "photo_prompt_clothing_structure_extension.json","photo_prompt_visual_obligations_clothing_structure.json",
                                       "photo_prompt_fashion_fit_extension.json","photo_prompt_visual_obligations_fashion_fit.json",
                                       "photo_prompt_portrait_fashion_exposure_extension.json","photo_prompt_visual_obligations_portrait_fashion_exposure.json"],
                       deliverable="concrete same-owner nodes, single directed relation, separately selected variants, complete affected-properties"),
                  dict(id="W3",purpose="표면·장신구·스타일의 선택 후보 보완",
                       source_targets=["photo_prompt_textile_surface_extension.json","photo_prompt_visual_obligations_textile_surface.json",
                                       "photo_prompt_ornament_structure_extension.json","photo_prompt_visual_obligations_ornament_structure.json",
                                       "photo_prompt_y2k_extension.json","photo_prompt_tags.json","photo_prompt_visual_obligations.json"],
                       deliverable="seersucker/eyelet/mesh/satin visible atoms, footwear/chain endpoint, optional style bundles",
                       note="y2k 파일 이름은 manifest에서 실제 등록명 재확인 후 선택; 새 계절별 중복 파일은 비용/이득이 확인될 때만."),
                  dict(id="W4",purpose="파생 인덱스와 current runtime publication",
                       deliverable="source_manifest/maintenance_ref → semantic/BM25F index → visual profile index → current runtime receipt",
                       constraints=["새/변경 semantic text만 embedding batch size 1","동일 provider/model/dimensions/전체 입력 text의 벡터만 재사용",
                                    "stale dictionary/registry hash와 source_revision_pending를 은폐하지 않기","runtime snapshot 및 historical pack 불변 유지"]),
                  dict(id="W5",purpose="검색·선택·composition 및 회귀 검증",deliverable="비교/동시성/mutation를 실제 새 revision에 실행하고 증거 분리"),
                  dict(id="W6",purpose="요청 범위에 따라 픽셀과 사용자 선호 확인",
                       deliverable="선택한 18개 pixel group의 비용/범위·gates 확정 후 native full image와 crops 평가; 별도 사용자 acceptance",
                       note="이번 연구는 이미지 생성을 요청하지 않았으므로 생성·비용 지출은 실행하지 않음")
              ],
              scoped_existing_tests=[
                  "tests/test_photo_fashion_fit_semantics.py","tests/test_photo_swimwear_semantics.py",
                  "tests/test_photo_clothing_terminology_semantics.py","tests/test_photo_ornament_structure.py",
                  "tests/test_photo_textile_opacity_effect_scope.py","tests/test_photo_womens_summer_trend_visual_semantics.py",
                  "tests/test_photo_candidate_semantics.py","tests/test_photo_visual_profile_retrieval.py",
                  "tests/test_photo_visual_profile_shards.py","tests/test_photo_runtime_freshness.py"],
              counts=dict(seed_rows=len(inventory),semantic_cards=len(cards),candidate_drafts=len(proposals),
                          source_rows=len(sources),comparison_pairs=len(PAIR_ROWS),allowed_combinations=len(COMBINATION_ROWS),
                          mutations=len(MUTATIONS),pixel_groups=len(PIXEL_ROWS)),
              promotion_conditions=[
                  "term-plan의 related_family_draft_ids는 같은 가족의 검토 인벤토리다. 각 용어와 각 변형의 동등성·compatible 부분 속성을 별도로 확정한 뒤 직접 매핑한다.",
                  "새 profile은 bare term로 hard 활성화하지 않는다; 명시 requester 의미/complete selected variant 근거가 필요.",
                  "등록 후보는 연구 URL·출처 제목·연구 라벨·원문 bulk 어휘를 semantic fields에 넣지 않는다.",
                  "선택형 bundle은 모든 member와 허용된 전체 effects를 확보; candidate/profile label 자체는 hard 근거가 아님.",
                  "가림/작은 해상도/부분 성공은 all-of PASS가 아님; performance/hidden process를 픽셀 claim으로 만들지 않음.",
                  "runtime/검색/픽셀/미학/사용자 acceptance가 없으면 그 층의 성공을 주장하지 않는다."
              ])
    # Keep source target names grounded in the current manifest.
    manifest=json.loads((ROOT/"skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json").read_text())
    y2k=[s["file"] for s in manifest["sources"] if s["kind"]=="candidate" and "y2k" in s["file"].lower()]
    targets=plan["phases"][3]["source_targets"]
    targets.remove("photo_prompt_y2k_extension.json");targets.extend(y2k)
    for test in plan["scoped_existing_tests"]: assert (ROOT/test).exists(),test
    write_json("implementation-plan.json",plan)
    counts=plan["counts"]
    validation=dict(status="PASS",scope="research_artifact_integrity_only",counts=counts,
                    checks=dict(all_seed_rows_mapped=True,all_cards_have_seed_rows=all(c["seed_term_ids"] for c in cards.values()),
                                unique_ids=len(proposals)==len({x["id"] for x in proposals}),
                                source_links_resolved=all(s in sources for c in cards.values() for s in c["source_ids"]),
                                reviewed_existing_ids_exist=True,
                                all_relations_have_endpoints=all(all(p["payload_draft"]["relations"][0].get(k) for k in ["subject","type","object"]) for p in proposals),
                                no_or_relations=all("_or_" not in p["payload_draft"]["relations"][0]["type"] for p in proposals),
                                no_source_urls_in_payload=all("http" not in json.dumps(p["payload_draft"]) for p in proposals),
                                no_identity_or_body_geometry_effects=all(p["payload_draft"]["affected_dimensions"]==["appearance"] for p in proposals),
                                all_gates_remain_planned=True,
                                csv_json_rows_agree=True),
                    runtime_data_validation="not_run",embedding_calls=0,image_calls=0,
                    interpretation_quality="human_review_required_before_runtime_promotion")
    assert all(validation["checks"].values()),validation["checks"]
    csv_rows=list(csv.DictReader((HERE/"term-plan.csv").open()))
    assert len(csv_rows)==len(term_plan)
    assert all(a["term_id"]==b["term_id"] and a["term"]==b["term"] and a["card_id"]==b["card_id"] for a,b in zip(csv_rows,term_plan))
    write_json("research-validation.json",validation)
    print(json.dumps(dict(status=validation["status"],counts=counts,actions=dict(Counter(t["action"] for t in term_plan)),
                          property_families_new=sorted({c["property_family"] for c in cards.values() if c["scope_status"].startswith("proposed")}),
                          y2k_sources=y2k),ensure_ascii=False))

if __name__ == "__main__": main()
