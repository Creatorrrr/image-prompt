"""Build this research folder only. No corpus, index, model or image writes."""
import collections, csv, hashlib, json, pathlib, re, unicodedata
import research_cards, research_cards_appearance, research_cards_surface
from research_sources import source_records
from research_routes import ALIASES, CONTEXT_RULES, SUPPLEMENTAL
from research_role_plan import roles_for
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def dump(name,value):
 (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
def norm(s):
 return re.sub(r"[^a-z0-9가-힣]+"," ",unicodedata.normalize("NFKC",s).casefold()).strip()
def build_cards():
 cards=[]
 hold={"drop_spike","button_lens","watch_camera","microdot_comparison","identity_comparison","number_pad","peak_lapel","plate_carrier","bias_drape","ripstop_grid"}
 for domain,sources,slots,limit,rows in research_cards.GROUPS:
  for line in rows.strip().splitlines():
   slug,name,en,ko,graph,gates,confusions=line.split("|")
   edges=[dict(zip(("subject","relation","object"),[v.strip() for v in edge.split(">")])) for edge in graph.split(";")]
   nodes=sorted({e[k] for e in edges for k in ("subject","object")})
   cards.append({"id":"esp_"+slug,"slug":slug,"name_ko":name,"domain":domain,
    "aliases":ALIASES.get(slug,[]),"visible_en":en,"visible_ko":ko,
    "owners_and_parts":nodes,"directed_relations":edges,"observable_gates":gates.split(";"),
    "confusion_boundaries":confusions.split(";"),"claim_limit":limit,
    "source_refs":sources.split(","),"source_support_scope":"Group-level meaning/convention support only. Exact visible composition, relations and gates are researcher-authored proposals, not source quotations or verified plates.",
    "proposed_roles":roles_for(domain,slug),"activation":"optional, requester-compatible, post-core only",
    "prerequisites":["Bind each existing owner/part to frozen request evidence; do not infer a new actor or device.","Check whole effects and original guards against locked dimensions before any adoption."],
    "visibility_plan":"Frame all consequential owner boundaries and listed contact/connection endpoints together; revise viewpoint or projection if hidden. Do not require every incidental support to be visible.",
    "source_specific_review":"HOLD exact specimen/material/function equivalence; plate/detail review required" if slug in hold else "Draft semantic review required",
    "pixel_rule":{"partial_is_fail":True,"unobservable":"UNOBSERVABLE_NOT_PASS","blocked":"BLOCKED_UNSCORED"},
    "native_approval":False,"runtime_registered":False})
 return cards
def build_routes(cards):
 lookup=collections.defaultdict(list)
 for card in cards:
  for alias in card["aliases"]:lookup[norm(alias)].append(card["id"])
 ref=json.loads((HERE/"reference-conversation.json").read_text())
 routes=[]; partial=[]
 for turn_index,turn in enumerate(ref["turns"]):
  section=""
  for line_no,line in enumerate(turn["items"][1]["text"].splitlines(),1):
   if line.startswith("## "):section=re.sub(r"^## \d+\.\s*","",line)
   if not line.startswith("| **"):continue
   cells=line.split("|")
   if len(cells)<4 or not cells[1].strip().endswith("**"):
    partial.append({"turn_index":turn_index,"line":line_no,"section":section,"text":line}); continue
   term=cells[1].strip().strip("*"); definition=cells[2].strip()
   parts=term.split(" — ",1);ko=parts[0];en=parts[1] if len(parts)>1 else ""
   linked=lookup.get(norm(en),[])
   context=CONTEXT_RULES.get(section)
   status="context_with_optional_projection" if context and linked else "context_only" if context else "visual_component_draft" if linked else "defer_specific_component_review"
   routes.append({"id":f"K{len(routes)+1:03d}","term_ko":ko,"term_en":en,
    "original_definition":definition,"source":{"conversation_id":ref["conversation_id"],"turn_index":turn_index,"line":line_no,"section":section},
    "status":status,"card_refs":linked,"link_relation":"component/proxy only; never full narrative equivalence" if context else "bounded visible realization; no extra emotional, material, identity or functional claim",
    "context_type":context[0] if context else None,
    "source_refs":context[1].split(",") if context else [],
    "claim_limit":context[2] if context else "The original term is preserved. A draft is not exhaustive, native approval or proof of source construction.",
    "hard_activation":False})
 dump("keyword-routes.json",routes);dump("unrecovered-fragments.json",partial)
 return routes,partial
def context_records(routes):
 rows=[{"id":"ctx_"+r["id"],"term_ko":r["term_ko"],"term_en":r["term_en"],"type":r["context_type"],
        "original_route":r["id"],"claim_limit":r["claim_limit"],"source_refs":r["source_refs"],
        "positive_retrieval_eligible":False,"optional_projection_card_refs":r["card_refs"],"native_approval":False}
       for r in routes if r["context_type"]]
 for i,(en,ko,sources,limit) in enumerate(SUPPLEMENTAL,1):
  rows.append({"id":f"ctx_supp_{i:02d}","term_ko":ko,"term_en":en,"type":"supplemental_sensitive_context",
   "origin":"researcher supplement; some Korean concepts are mentioned in the recovered introduction; not a claim of recovered missing table rows",
   "claim_limit":limit,"source_refs":sources.split(","),"positive_retrieval_eligible":False,
   "optional_projection_card_refs":[],"native_approval":False})
 return rows
def evaluate(cards,contexts):
 cases=[]
 for i,c in enumerate(cards):
  cases.append({"id":"P_"+c["slug"],"split":"source_literal_smoke",
   "type":"literal_discovery_smoke_not_semantic_benchmark","query_en":c["visible_en"],"query_ko":c["visible_ko"],
   "expected_card_refs":[c["id"]],"must_retain":c["observable_gates"],
   "forbidden_inferences":[c["claim_limit"]],"expected_roles":c["proposed_roles"],
   "expected_exact_cid_rid":"TBD after source adoption; card IDs are research locators","status":"NOT_RUN"})
 natural=[
 ("direct_handoff","두 사람이 종이 봉투 하나의 서로 다른 끝을 잡고 있음","Two people each grip a different end of a single paper envelope."),
 ("suspended_handoff","받는 손까지 아직 닿지 않은 서류","Paper held out just short of the recipient's waiting palm."),
 ("earpiece_contact","귓속 장치 위에 손가락을 댄 인물","A person presses a fingertip against the little device fitted in their ear."),
 ("receiver_pose","구형 전화 수화기를 귀와 입에 맞춰 든 손","A hand holds an old telephone handset between the ear and mouth."),
 ("over_shoulder_glance","걷는 방향은 그대로 두고 고개만 뒤로 돌림","The walker turns only their head back while the torso keeps facing ahead."),
 ("cuff_adjustment","자기 반대 손목의 셔츠 끝을 집어 정돈","Pinching the shirt edge at one's own opposite wrist."),
 ("other_tie","내 손은 상대방 목 아래의 매듭에 닿음","My hand touches the knot below the other person's neck."),
 ("mirror_attention","앞을 향한 몸과 뒤의 사람을 담은 거울","A forward-facing body beside a mirror that reflects someone behind."),
 ("back_to_back","등 윗부분은 닿고 얼굴은 서로 반대로 향함","Upper backs touching, faces turned in opposite directions."),
 ("divergent_gazes","가까이 선 두 사람이 서로 다른 쪽을 봄","Standing close together while attending to separate points."),
 ("supported_walk","동행인 어깨에 팔을 걸치고 옆몸을 받침","An arm draped over a companion's shoulder, the torso supported at the side."),
 ("restrained_seated","의자에 앉은 사람 두 손목 사이 짧은 금속 사슬","A short metal chain between the wrists of a person sitting in a chair."),
 ("notch_lapel","칼라와 앞깃이 만나는 곳의 작은 홈","A small cut-in gap where the collar meets the folded jacket front."),
 ("shawl_lapel","꺾인 모서리 없이 이어지는 둥근 재킷 앞깃","A rounded jacket facing flowing past the neck without a sharp corner."),
 ("trench_assembly","허리 고리를 통과하는 코트 끈과 어깨 견장","A coat belt threaded through waist loops beneath shoulder tabs."),
 ("stocking_support","허리에서 내려온 끈이 다리 양말 위끝과 연결","Straps from a waist belt clipped to the upper edge of leg stockings."),
 ("chest_rig","어깨 끈에 매달린 납작한 가슴 파우치 판","A flat pouch board suspended against the chest by shoulder straps."),
 ("illusion_panel","옷의 빈 부분처럼 보이지만 솔기로 연결된 미세 그물","A fine net joined by seams across an apparently open part of a dress."),
 ("slit_edge","치마의 매끈하게 마감된 두 가장자리 사이 다리","One leg between two neatly finished skirt edges."),
 ("oxford_closure","구두 앞면 아래로 붙어 닫히는 끈 판","Lacing panels joined underneath the front part of the shoe."),
 ("derby_closure","구두 앞판 위에 따로 얹힌 두 끈 날개","Two separate lacing wings sewn on top of the shoe front."),
 ("cufflink_bridge","셔츠 손목 끝 두 겹을 잇는 작은 잠금 장식","A small fastener joining the two folded ends at the shirt wrist."),
 ("smudged_makeup","눈 아래 피부에 내려온 불규칙한 화장 줄","Uneven cosmetic streaks extending below the eye."),
 ("monitor_boundary","실내 인물과 모니터 테두리 안 작은 사람 영상","A person in the room apart from a small human image inside the monitor frame."),
 ]
 for slug,ko,en in natural:
  c=next(c for c in cards if c["slug"]==slug)
  cases.append({"id":"Q_"+slug,"split":"natural_regression","type":"authored_paraphrase",
   "query_en":en,"query_ko":ko,"expected_card_refs":[c["id"]],"must_retain":c["observable_gates"],
   "forbidden_inferences":[c["claim_limit"]],"author_knows_cards":True,"status":"NOT_RUN"})
 # These are authored language probes, not automatically ranked negatives.
 boundary=[
 ("actor_vs_camera","어깨 너머로 뒤돌아보는 사람, 정면 카메라","A person looks back over their shoulder, photographed from the front.","head/torso relation","camera viewpoint must not substitute"),
 ("length_vs_view","허벅지까지 나온 정면 초상","A frontal three-quarter-length portrait.","crop length","three-quarter rotation must not be imposed"),
 ("ear_vs_receiver","이어피스를 착용한 귀에 손끝이 닿음","A fingertip touches an earpiece seated in the ear.","same-owner earpiece contact","telephone receiver beside ear is not equivalent"),
 ("self_vs_other","자신의 커프를 정리하는 손","One hand adjusts the opposite cuff on the same wearer.","same owner","no garment-fitting prerequisite bypass"),
 ("other_vs_self","다른 사람의 넥타이를 정리함","One person adjusts another person's tie.","two owners","self-adjustment is not equivalent"),
 ("drop_vs_handoff","사람 없이 보관 홈 안에 있는 봉투","An envelope inside a recess with nobody present.","static containment","no inferred prior handoff or later retrieval"),
 ("silk_vs_satin","섬유를 지정하지 않은 광택 직물","A glossy fabric with no specified fiber.","surface response","no silk fiber claim"),
 ("drape_vs_bias","대각 주름 드레스","A dress with diagonal draped folds.","visible folds","no grain direction certification"),
 ("plate_vs_rig","수납 패널만 있는 체스트 리그","A chest rig with a pouch panel.","carrying structure","no ballistic plate or armor rating"),
 ("slit_vs_tear","마감된 치마 트임","A skirt slit with finished edges.","finished boundaries","not torn fabric"),
 ("mesh_vs_void","네크라인을 잇는 망사","Fine mesh spans the neckline.","continuous mesh and seams","not empty skin opening"),
 ("ring_vs_marriage","손가락의 민무늬 반지","A plain band on a finger.","ring wearing","no marital status"),
 ("cuff_vs_torture","몸 앞에서 사슬로 연결된 수갑","Cuffs linked by a chain in front of the body.","restraint endpoints","no torture history or sexual context"),
 ("photo_vs_truth","테두리 속 합성처럼 보이는 사진","A photograph inside a clear border.","bounded represented medium","no authenticity or event claim"),
 ("redact_vs_classify","검은 막대가 덮인 인쇄물","Printed text covered by black bars.","occlusion","no legal classification or effective deletion claim"),
 ("one_vs_time","한 장의 숫자 패드","A single sheet of number groups.","printed groups","no one-time use or cryptographic claim"),
 ("mirror_vs_copy","거울 속의 뒷사람 반사","A mirror reflection of a person behind the observer.","mirror boundary","no extra physical person"),
 ("gloves_vs_trace","검은 장갑을 낀 손","A hand wearing black gloves.","wearing state","no trace-free performance"),
 ("body_vs_support","의자에 앉아 다리를 교차함","A person crosses their legs while seated on a chair.","support and limb ownership","no extra limb"),
 ("tux_vs_business","검정 비즈니스 수트","A black business suit.","requested garment","no automatic satin tuxedo facing"),
 ]
 for slug,ko,en,want,deny in boundary:
  cases.append({"id":"B_"+slug,"split":"boundary","type":"confusion_pair","query_en":en,"query_ko":ko,"must_retain":[want],"forbidden_inferences":[deny],"status":"NOT_RUN"})
 controls=[
 ("asset","분기별 금융 자산 보고서","A quarterly financial asset report."),
 ("mole","정원의 두더지","A mole in a garden."),
 ("cover","책의 표지","A book cover."),
 ("legend","판타지의 전설","A fantasy legend."),
 ("cutout","종이 오려낸 장식","A paper cutout decoration."),
 ("spy","가느다란 위스피 앞머리","Soft wispy bangs."),
 ("honey","사이버 허니팟 대시보드","A cyber honeypot dashboard."),
 ("party","평범한 블랙타이 행사","An ordinary black-tie reception."),
 ("office","일반 사무실 회의","An ordinary office meeting."),
 ("coat","비 오는 날의 통근자","A commuter on a rainy day."),
 ("latex","라텍스 재질 제품 사진","A latex product photograph."),
 ("passport","여행 서류를 정리하는 관광객","A tourist arranging travel documents."),
 ]
 for slug,ko,en in controls:cases.append({"id":"N_"+slug,"split":"ordinary_control","type":"unrelated_control","query_en":en,"query_ko":ko,"must_retain":["ordinary requested meaning"],"forbidden_inferences":["espionage, coercion, sexual activity or weapon hard activation"],"status":"NOT_RUN"})
 for c in contexts:
  if c["type"]=="supplemental_sensitive_context" or c.get("original_route") in {"K001","K020","K053","K069","K102","K126"}:
   cases.append({"id":"C_"+c["id"],"split":"nonvisual_control","type":"nonvisual","query_en":c["term_en"] or c["term_ko"],"query_ko":c["term_ko"],"must_retain":["context only unless separately specified visible meaning"],"forbidden_inferences":[c["claim_limit"]],"status":"NOT_RUN"})
 return cases
def main():
 cards=build_cards();routes,partial=build_routes(cards);contexts=context_records(routes);sources=source_records()
 dump("semantic-cards.json",cards);dump("context-distinctions.json",contexts);dump("sources.json",sources)
 drafts=[{"draft_id":"draft/espionage/"+c["slug"],"card_ref":c["id"],"en":c["visible_en"],"ko":c["visible_ko"],
  "proposed_roles":c["proposed_roles"],"intrinsic_owner_graph":c["directed_relations"],
  "prerequisite_review":c["prerequisites"],"confusions":c["confusion_boundaries"],
  "must_not_infer":c["claim_limit"],"source_refs":c["source_refs"],
  "status":"research_only_not_loader_input","conditions_effects_and_native_proof":"NOT_AUTHORED; assign to actual CID/RID only after per-source review",
  "source_specific_review":c["source_specific_review"],"native_approval":False} for c in cards]
 dump("candidate-drafts.json",drafts);cases=evaluate(cards,contexts);dump("evaluation-cases.json",cases)
 with (HERE/"EVALUATION-CASES.tsv").open("w") as f:
  w=csv.writer(f,delimiter="\t");w.writerow(["id","split","type","query_ko","query_en","status"])
  for c in cases:w.writerow([c[k] for k in ("id","split","type","query_ko","query_en","status")])
 with (HERE/"SOURCES.tsv").open("w") as f:
  w=csv.writer(f,delimiter="\t");w.writerow(["id","title","url","access","read_scope","limits"])
  for s in sources:w.writerow([s[k] for k in ("id","title","url","access","read_scope","limits")])
 atlas=["# 복원 키워드 경로\n\n모든 행은 선택적 연구 경로다. 원어/정의는 참조 대화의 복원 범위이며 독립 검증된 전문용어 사전이 아니다.\n\n|ID|원어|분야|경로|카드|\n|---|---|---|---|---|"]
 for r in routes:atlas.append(f"|{r['id']}|{r['term_ko']} / {r['term_en']}|{r['source']['section']}|{r['status']}|{', '.join(r['card_refs']) or '—'}|")
 (HERE/"KEYWORD-ATLAS.md").write_text("\n".join(atlas)+"\n")
 visual=["# 시각 의미 카드\n\n모든 문장과 관계는 연구 초안이다. 출처는 개념군 지원이며 출처의 문장을 복제한 것이 아니다. 선택된 카드의 모든 핵심 gate를 함께 판독해야 한다.\n"]
 for c in cards:
  visual.append(f"## {c['id']} — {c['name_ko']}\n\n{c['visible_ko']}\n\n{c['visible_en']}\n\n- 소유자/관계: "+"; ".join(f"{e['subject']} → {e['relation']} → {e['object']}" for e in c["directed_relations"])+f"\n- 관찰 gate: {'; '.join(c['observable_gates'])}\n- 혼동 경계: {'; '.join(c['confusion_boundaries'])}\n- 주장 한계: {c['claim_limit']}\n- 제안 role: {', '.join(c['proposed_roles'])}\n- 근거군: {', '.join(c['source_refs'])}; {c['source_specific_review']}\n")
 (HERE/"VISUAL-CARDS.md").write_text("\n".join(visual))
 summary={"phase":"RESEARCH_ONLY","date":"2026-10-23","complete_recovered_rows":len(routes),"partial_rows":len(partial),
  "route_status_counts":dict(collections.Counter(x["status"] for x in routes)),
  "visual_cards":len(cards),"bilingual_candidate_drafts":len(drafts),"context_records":len(contexts),
  "sources":len(sources),"evaluation_cases":len(cases),"bilingual_queries":2*len(cases),
  "evaluation_splits":dict(collections.Counter(x["split"] for x in cases)),
  "detail_or_specimen_holds":sum("HOLD" in c["source_specific_review"] for c in cards),
  "runtime_registration":"NOT_RUN","index_build":"NOT_RUN","retrieval_evaluation":"NOT_RUN","image_generation":"NOT_RUN","user_acceptance":"PENDING"}
 dump("SUMMARY.json",summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
