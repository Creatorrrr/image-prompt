"""Add hand-curated relation, owner, regression, and pack-review proposals."""
import json
from pathlib import Path
from collections import Counter

OUT = Path(__file__).resolve().parent


def read(name):
    return json.loads((OUT / name).read_text())


def save(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n")


def rows(name):
    return [line.split("|") for line in (OUT/name).read_text().splitlines() if line and not line.startswith("#")]


def enrich():
    semantic = read("SEMANTIC-UNITS.json"); units = {u["id"]:u for u in semantic["units"]}
    for unit in units.values():
        unit["relations"]=[r for r in unit["relations"] if "contract_status" not in r]
    for suffix, relation, subject, target in rows("structural-relations.psv"):
        unit = units["sca_"+suffix.lower()]
        unit["relations"].append({"id":f"sca_{suffix.lower()}_struct_{len(unit['relations'])}",
                                  "type":relation,"subject":subject,"object":target,
                                  "contract_status":"research relation; normalize and validate against runtime contract before promotion"})
    save("SEMANTIC-UNITS.json", semantic)
    candidate = read("CANDIDATE-DRAFTS.json")
    for draft in candidate["candidates"]:
        draft["relations_proposal"] = units[draft["semantic_unit_id"]]["relations"]
    save("CANDIDATE-DRAFTS.json", candidate)
    catalog = read("REFERENCE-CATALOG-SNAPSHOT.json")
    profile = {p["id"]:p for p in catalog["profiles"]}
    entry = {e["slot"]+"."+e["id"]:e for e in catalog["candidates"]}
    owner_map = []
    for tids, pids, cids, boundary in rows("owner-map.psv"):
        plist=[] if pids=="-" else pids.split(",");clist=[] if cids=="-" else cids.split(",")
        assert all(pid in profile for pid in plist), (tids, [pid for pid in plist if pid not in profile])
        assert all(cid in entry for cid in clist), (tids, [cid for cid in clist if cid not in entry])
        owner_map.append({"term_or_split_ids":tids.split(","),"existing_profile_ids":plist,"existing_candidate_keys":clist,
                          "profile_property_scope":{pid:profile[pid]["concept_candidate"].get("affected_properties",[]) for pid in plist},
                          "candidate_property_scope":{cid:entry[cid].get("affected_properties",[]) for cid in clist},
                          "reuse_boundary":boundary,"status":"BASELINE_ID_VERIFIED_MEANING_REVIEW_REQUIRED"})
    save("OWNER-MAP.json",{"schema_version":"research-owner-map/v1","reference":"verified Git baseline, not latest working tree","mappings":owner_map})
    cases=read("CHARACTER-CASEBOOK.json")
    additions={"K01":["X03"],"K04":["X10","X15"],"K06":["X16"],"K07":["X01"],"K12":["X06"],"K18":["X05"],"K26":["X13"],"K28":["X14"],"K30":["X03"],"K34":["X11"]}
    for case in cases["cases"]:
        case["boundary_comparison_unit_ids"]=["sca_"+x.lower() for x in additions.get(case["id"],[])]
        case["boundary_comparison_scope"]="comparison questions, not proof that this case contains each structure"
    save("CHARACTER-CASEBOOK.json",cases)
    regressions=[]
    for rid, uids, ko, en, negative, boundary in rows("regression-pairs.psv"):
        assert all(uid in units for uid in uids.split(","))
        regressions.append({"id":rid,"unit_ids":uids.split(","),"positive_ko":ko,"positive_en":en,
                            "nearby_negative_ko":negative,"expected_boundary":boundary,
                            "test_layers":["scoped core interpretation","candidate eligibility","owner/property evidence","native pixel relation"],
                            "exact_alias_status":"positive fragments are test proposals; not automatically authored exact aliases",
                            "status":"PROPOSED_NOT_RUN"})
    policy_scenarios=[
        ("Q01","hard activation authority","BM25F/embedding-only similarity hits remain advisory; exact positives require validated core scope before obligations"),
        ("Q02","negation and quoted context","requests excluding animal ears or quoting a third-party caption do not create positive anatomical ear obligations"),
        ("Q03","body property lock across carriers","locked body volume cannot be changed by a surface-material or wardrobe candidate whose visual effect changes the same body boundary"),
        ("Q04","garment coverage lock","an open body dimension does not permit changing locked sleeve neckline or exposure boundaries"),
        ("Q05","unscoped slot fail closed","prop and aftermath_trace entries with empty slot dimensions remain ineligible for bundle adoption; do not launder them through scale_relation"),
        ("Q06","medium lock","a chibi or no-highlight illustrated motif cannot override a locked photographic medium or infer a different age"),
        ("Q07","species and identity locks","ear accessories may retain a human subject; a biological body conversion cannot bypass locked species/subject ownership"),
        ("Q08","candidate pack bounds","at most 15 discovery candidates total, 3 per assertion; at most 8 bundles with 8 members; identical owner/property proposals deduplicated"),
        ("Q09","broad costume context","Gothic Lolita or mecha label alone does not activate every representative garment, body, prop, color or action feature"),
        ("Q10","duplicate owner conflict","two candidates with conflicting values for the same owner/property do not survive whole-pack compatibility review"),
        ("Q11","partial and occluded pixels","one selected component missing is FAIL; occluded required relation is UNOBSERVABLE and cannot count as PASS"),
        ("Q12","moderation and acceptance layers","blocked generation is an attempt with no quality outcome; pixel PASS does not mean user preference or acceptance")]
    for rid, topic, predicate in policy_scenarios:
        regressions.append({"id":rid,"topic":topic,"expected_predicate":predicate,"status":"PROPOSED_NOT_RUN"})
    save("REGRESSION-PROPOSALS.json",{"schema_version":"research-regression-proposals/v1","runtime_fixture_schema":False,"cases":regressions})
    packs=[
        ("B01","명시된 성인의 두 나선 머리와 흰 리본, 분리 소매",["h05","x10","g01","g20"],"두 나선·흰 리본·분리 소매를 각각 명시; 몸 체적과 나이 고정","색 분할 염색·신체 귀·군복 전체 강제 제외"),
        ("B02","표시 패널 가면을 쓴 인간",["p09","x05","p11"],"인간 몸과 제거 가능한 가면 명시; species/body 고정","통합 인공 얼굴 X05는 비교 반례로 거부; sun visor 혼동 거부"),
        ("B03","등에 부착한 기계 날개 장비",["c15","p08","g15"],"인간 몸과 장착 장비 명시; 팔·등 해부학 고정","생물 날개·팔 대체·탑승체로 변환 거부"),
        ("B04","속치마로 종형을 만든 성인 복식",["g08","g06","g18"],"선택한 종형 치마와 속치마 관계 명시; 실제 골반 폭 고정","역사적 옆 후프·버슬·몸 골반 확대 거부"),
        ("B05","토끼 귀 머리띠를 쓴 성인 보디수트",["x01","a13","a16"],"성인 인간·의상 귀·한 벌 몸판 명시; biological ears/sexual tone 고정","생물 토끼 귀·실제 꼬리·추가 노출·결박 행동 거부"),
        ("B06","공·소켓 인형 관절이 보이는 인공 존재",["n22","x13","b14"],"인공 인형 몸 명시; head/body ratio와 medium 고정","치비 비례 자동 추가 거부; cross-dimension 후보는 정책 해결 전 보류"),
        ("B07","재료별 전투 손상과 큰 열쇠형 소품",["p04","p16"],"소품 조립 구조와 금속/천 손상 부위 명시","현재 prop/aftermath_trace scope가 비어 있어 채택 보류를 올바른 결과로 기록"),
        ("B08","노출 경계를 고정한 성인 체형 묘사",["a01","a04","a09","a10","a19"],"가슴 또는 허벅지의 한 부위만 명시하고 의복 coverage 잠금","body open을 이유로 underboob/sideboob/노출띠 후보 채택 금지")]
    bundles=[]
    for bid, prompt, members, core, reject in packs:
        assert all("sca_"+m in units for m in members)
        bundles.append({"id":bid,"name_free_context_ko":prompt,"candidate_research_ids":["sca_candidate_"+m for m in members],
                        "core_prerequisite_and_locks":core,"expected_filtering":reject,
                        "joint_adoption":"whole pack compatibility and property guards; all candidates may be rejected",
                        "status":"RESEARCH_FIXTURE_NOT_RUNTIME_PACK","sources_are_not_core_inputs":True})
    save("PACK-CONTEXT-PROPOSALS.json",{"schema_version":"research-pack-context-proposals/v1","runtime_pack_schema":False,"contexts":bundles})
    sources=read("RESEARCH-SOURCES.json")["sources"]
    markdown=["# 출처와 확인 범위", "", "2026-10-03 조회. 검색 요약·본문 읽기·픽셀 관찰·접근 제한을 구분했습니다. 아래 사실 범위를 넘어선 구성요소/소유자/속성 설계는 연구자의 제안입니다.", ""]
    for source in sources:
        markdown.extend([f"- **{source['id']}** [{source['title']}]({source['url']}) — `{source['access']}`. {source['source_supported_scope']}. 제한: {source['limits']}."])
    (OUT/"SOURCES.md").write_text("\n".join(markdown)+"\n")
    summary=read("SUMMARY.json")
    summary.update({"typed_structural_relations":len(rows("structural-relations.psv")),"owner_comparison_mappings":len(owner_map),
                    "regression_proposals":len(regressions),"pack_context_proposals":len(bundles),
                    "source_access_counts":dict(Counter(s["access"] for s in sources))})
    save("SUMMARY.json",summary)


if __name__=="__main__":
    enrich()
