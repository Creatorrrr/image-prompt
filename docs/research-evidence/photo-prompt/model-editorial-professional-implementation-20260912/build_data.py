import json,hashlib
from pathlib import Path
ROOT=Path.cwd()
ASSETS=ROOT/"skills/photo-prompt-image-generator/assets"
RESEARCH=ROOT/"docs/research-evidence/photo-prompt/model-editorial-professional-20260912"
OUT=ROOT/"docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912"
OUT.mkdir(parents=True,exist_ok=True)
def read(p): return json.loads(p.read_text())
def digest(x): return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def write(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
def distinct_terms(items):
 seen=set(); result=[]
 for item in items:
  key=item.casefold()
  if key not in seen: result.append(item); seen.add(key)
 return result
proposals=read(RESEARCH/"visual-proposals.json")["proposals"]
plans={r["proposal_id"]:r for r in read(RESEARCH/"integration-plan.json")["rows"]}
bundles=read(RESEARCH/"candidate-bundles.json")["bundles"]
included=[p for p in proposals if p["scope"]=="single_image"]
slot_changes={"mep_garment_movement":"motion","mep_jewelry_contact":"contact_point","mep_graphic_pose":"body_pose","mep_poised_support":"body_orientation","mep_gaze_target":"gaze_target"}
extra_units={
"mep_casting_front":["model digitals","front-facing casting portrait"],
"mep_casting_profile":["casting profile view"],
"mep_casting_full_length":["full-length model digitals"],
"mep_garment_clearance":["garment-aware posing","visible garment details"],
"mep_garment_side_depth":["side seam detail"],
"mep_garment_movement":["fabric in motion","moving fashion"],
"mep_product_hero":["product-led shoot","product hero image"],
"mep_jewelry_contact":["jewelry campaign","jewellery campaign"],
"mep_beauty_detail":["beauty editorial","makeup detail"],
"mep_hair_outline":["hair model","hair silhouette"],
"mep_cover_copy_space":["cover copy space","magazine cover"],
"mep_environment_relation":["editorial portrait","environmental portrait"],
"mep_graphic_pose":["graphic pose","sculptural pose"],
"mep_gaze_target":["directed eye-line","gaze target"],
"mep_poised_support":["poised posture","balanced stillness"],
"mep_in_between":["in-between moment","pose transition"],
"mep_surface_texture":["texture preservation","skin retention"],
"mep_selective_imperfection":["deliberate imperfection"],
"mep_visual_juxtaposition":["visual juxtaposition","visual tension"],
"mep_tether_review":["tethered review","digital tech"],
"mep_fitting_adjustment":["wardrobe fitting","fit model"]
}
# English contrast phrases support non-Korean retrieval without making labels hard.
contrasts={
"mep_garment_clearance":["hands covering the jacket buttons","face-only crop hiding garment details"],
"mep_beauty_detail":["blue background with black eyeliner","color appears only on clothing"],
"mep_surface_texture":["plastic skin with sharp knit background","uniform noise pasted over smooth skin"],
"mep_jewelry_contact":["jewel fused into skin","bright sparkle with no readable jewel outline"],
"mep_product_hero":["sharp face and blurred product","hands hide the defining product shape"],
"mep_casting_front":["fashion test shoot with dramatic makeup","instant-film borders on an editorial portrait"],
"mep_cover_copy_space":["arbitrary masthead over the face","small accidental gap without usable copy space"],
"mep_tether_review":["laptop as decoration","finished fashion portrait without a production activity"],
"mep_fitting_adjustment":["fitness model exercising","hands hover without changing the garment"]
}
profiles=[];slots={};member_ids={};slot_by_id={}
for p in included:
 pid=p["id"];units=[c["prompt_fragment_en"] for c in p["components"]]
 definition="; ".join(units)
 profile={"id":pid,"category":"photographic_presentation_relation",
  "activation":{"exact_terms":[definition],"requires_adult_character":True,"semantic_discovery_requires_component_evidence":False},
  "semantics":{"definition":definition,"paraphrase_examples":distinct_terms([p["label_ko"],*extra_units[pid],*p["related_terms"]]),
   "contrast_examples":[*p["contrast_examples_ko"],*contrasts.get(pid,[])],
   "claim_limits":[p["limitations_ko"],"The requested owner and scope must be visible in one saved image; professional status, production history and delivery compliance are not pixel claims."]},
  "concept_candidate":{"concept_terms":[p["label_ko"],*extra_units[pid],*units]},
  "runtime_expression":{"default_mode":"definition_with_optional_label","prompt_label_terms":[],"forbidden_prompt_terms":[],"runtime_forbidden_labels":[]},
  "reject_substitutes":[*p["contrast_examples_ko"],*contrasts.get(pid,[])],
  "authored_components":{"contract_version":"photo-authored-visual-components/v1","components":[]}}
 for i,c in enumerate(p["components"],1):
  phrase=c["prompt_fragment_en"]
  profile["authored_components"]["components"].append({"id":f"component_{i}","match_terms":[phrase],
   "evidence_field":f"component_{i}_phrase","evidence_terms":[phrase],"min_content_words":3,
   "instruction":"Preserve the requested subject and make this selected relation visible: "+phrase,
   "render_gate":{"id":f"vo_{pid}_{i}","review_scale":c["review_scale"],
    "description":phrase+". Judge the explicitly declared owner and scope in this saved image; missing, obscured, reversed or unclear evidence fails."}})
 profiles.append(profile)
 slot=slot_changes.get(pid,plans[pid]["proposed_slot"])
 eid=pid+"_candidate"
 entry={"id":eid,"ko":p["label_ko"],"en":definition,"weight":0.55,
  "tags":["human","adult","fashion","portrait","photographic_presentation"],
  "for_any":["human"],"requires_primary_any_tags":["human","portrait","fashion","beauty","commercial"],
  "aliases":[p["label_ko"],*extra_units[pid]],"keywords":[*extra_units[pid],*p["related_terms"]],
  "embedding_text":p["label_ko"]+"; "+"; ".join(extra_units[pid]+units),
  "concept_units":[*extra_units[pid],*units],
  "relations":[{"id":pid+"_owner_relation","type":p["relation"],"subject":p["owner"],"object":"the declared photographic subject and frame"}],
  "affected_dimensions":p["affected_dimensions"]}
 if pid in {"mep_tether_review","mep_fitting_adjustment"}:
  entry["requires_primary_any_tags"]=["production_activity","photography_workflow","garment_fitting"]
 slots.setdefault(slot,[]).append(entry);member_ids[pid]=eid;slot_by_id[pid]=slot
runtime_bundles=[]
for b in bundles:
 if b["scope"]!="single_image":continue
 ps=[p for p in included if p["id"] in b["component_proposal_ids"]]
 runtime_bundles.append({"id":b["id"],"primary_visual_proposition":b["request_condition_ko"],
  "component_groups":[{"id":p["id"]+"_component","visible_evidence":["; ".join(c["prompt_fragment_en"] for c in p["components"])]} for p in ps],
  "candidate_ids":[member_ids[p["id"]] for p in ps],"candidate_slots":{member_ids[p["id"]]:slot_by_id[p["id"]] for p in ps},
  "hard_profile_ids":[p["id"] for p in ps],"confusion_boundaries":[b["conflict_ko"],b["selection_note_ko"]],
  "source_keywords":list(dict.fromkeys(u for p in ps for u in extra_units[p["id"]])),
  "relations":[{"id":b["id"]+"_joint","type":"co_realized_with_same_subject_and_event","subject":ps[0]["owner"],"object":"all selected component owners in one coherent photograph"}]})
extension={"schema_version":"photo-prompt-research-extension/v1","slots":slots,"visual_semantics":runtime_bundles}
record={"record_id":"photo_prompt_model_editorial_extension","authored_source_sha256":digest(extension),
 "maintenance_only":{"research_path":str(RESEARCH.relative_to(ROOT)),"source_ids":sorted({s for p in included for s in p["source_ids"]}),
  "included_proposal_ids":[p["id"] for p in included],"deferred_proposals":[p for p in proposals if p["scope"]!="single_image"],
  "deferred_bundles":[b for b in bundles if b["scope"]!="single_image"],
  "reason":"Series and layout require a separate output-level contract, not hard duties on a single image.",
  "broad_term_policy":"industry status, publication provenance and subjective quality are advisory context only",
  "claim_boundary":"Source and index integrity are not candidate adoption or rendered success."}}
write(ROOT/"docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_model_editorial_extension.json",record)
extension["maintenance_ref"]={"contract_version":"photo-extension-maintenance-ref/v1","record_id":record["record_id"],"sha256":digest(record)}
for profile in profiles:
 if profile["id"]=="mep_garment_side_depth":
  profile["semantics"]["paraphrase_examples"]=[t for t in profile["semantics"]["paraphrase_examples"] if t not in {"Catalog","Lookbook","Garment-aware"}]
write(ASSETS/"photo_prompt_model_editorial_extension.json",extension)
write(ASSETS/"photo_prompt_visual_obligations_model_editorial.json",{"schema_version":"photo-visual-obligation-registry-extension/v1",
 "relation_contract_version":"photo-visual-relation/v1","description":"Request-bound photographic presentation; broad model/editorial/professional labels remain advisory.","profiles":profiles})
# Only extend the three existing medium entries, preserving legacy wording and selection weights.
path=ASSETS/"photo_prompt_tags.json"; text=path.read_text(); original=read(path)
enhance={
"fashion_editorial":{"concept_units":["fashion editorial photograph","request-led narrative or concept with visible subject context"],"affected_dimensions":["style"],"keywords":["fashion editorial","editorial portrait","fashion story"]},
"lookbook":{"concept_units":["brand lookbook photograph","garment presentation within the requested framing"],"affected_dimensions":["style"],"keywords":["lookbook","garment-aware posing","collection presentation"]},
"campaign_photo":{"concept_units":["advertising campaign photograph","brand communication with request-defined visual priorities"],"affected_dimensions":["style"],"keywords":["advertising campaign","product-led shoot","hero image"]}
}
for entry in original["slots"]["medium"]:
 if entry["id"] not in enhance:continue
 old=json.dumps(entry,ensure_ascii=False,indent=2)
 # Locate the exact object by ID then balanced brace; replace only that small record.
 marker='"id": "'+entry["id"]+'"';pos=text.index(marker)
 start=text.rfind("{",0,pos);depth=0;end=None
 for i in range(start,len(text)):
  if text[i]=="{":depth+=1
  elif text[i]=="}":
   depth-=1
   if depth==0:end=i+1;break
 indent=len(text[text.rfind("\n",0,start)+1:start])
 updated={**entry,**enhance[entry["id"]]}
 replacement=json.dumps(updated,ensure_ascii=False,indent=2).replace("\n","\n"+" "*indent)
 text=text[:start]+replacement+text[end:]
needle='"photo_prompt_color_relations_extension.json"\n    ]'
if '"photo_prompt_model_editorial_extension.json"' not in text:
 assert needle in text
 text=text.replace(needle,'"photo_prompt_color_relations_extension.json",\n      "photo_prompt_model_editorial_extension.json"\n    ]',1)
path.write_text(text)
write(OUT/"source-coverage.json",{"profiles":len(profiles),"candidate_entries":sum(map(len,slots.values())),"bundles":len(runtime_bundles),
 "deferred_profiles":len(proposals)-len(profiles),"deferred_bundles":len(bundles)-len(runtime_bundles),
 "slot_ownership":slot_by_id,"render_status":"NOT_RUN"})
print(json.dumps(read(OUT/"source-coverage.json"),ensure_ascii=False,indent=2))
