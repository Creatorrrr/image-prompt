#!/usr/bin/env python3
"""Build research-only crosswalks and plans from reviewed cards, without runtime writes."""
from __future__ import annotations
import collections,csv,hashlib,json
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
ASSETS=ROOT/"skills/photo-prompt-image-generator/assets"
def read(n):return json.loads((OUT/n).read_text())
def save(n,x):(OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+"\n")
def age_class(text):
 if "15세" in text:return "source_explicit_minor"
 if "학생" in text:return "source_youth_context_age_unspecified"
 if "teen/young adult" in text:return "source_mixed_teen_adult"
 if "미확인" in text or "명시 없음" in text:return "source_age_unspecified"
 if "설명문" in text:return "descriptive_age_claim_not_verified"
 return "prompt_explicit_adult_claim_not_independently_replayed"
def main():
 source=read("SOURCE-KEYWORDS.json");cards=read("RESEARCH-PROPOSALS.json")["cards"];cov=read("CURRENT-COVERAGE.json");inventory=read("CURRENT-INVENTORY.json")
 sources=read("SOURCES.json")["primary_sources"];bundles=read("BUNDLE-DRAFTS.json")["bundles"]
 by={c["id"]:c for c in cards};source_by={r["id"]:r for r in source["entries"]};coverage={r["id"]:r for r in cov["rows"]}
 manifest=json.loads((ASSETS/"photo_prompt_source_manifest.json").read_text())
 id_files=collections.defaultdict(list)
 for item in manifest["sources"]:
  p=ASSETS/item["file"];d=json.loads(p.read_text())
  for slot,values in d.get("slots",{}).items():
   for e in values:id_files["slot:"+slot+":"+e["id"]].append(str(p.relative_to(ROOT)))
  for prof in d.get("profiles",[]):id_files[prof["id"]].append(str(p.relative_to(ROOT)))
 for k in inventory["slots"]:
  if k not in id_files:id_files[k]=["skills/photo-prompt-image-generator/assets/photo_prompt_tags.json"]
 for k in inventory["profiles"]:
  if k not in id_files:id_files[k]=["skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json"]
 units=[]
 for s in source["entries"]:
  assigned=[c for c in cards if s["id"] in c["keyword_ids"]]
  r=coverage[s["id"]]
  units.append({**s,"semantic_unit_id":"VEL-U-"+s["id"][1:],"proposal_ids":[c["id"] for c in assigned],"age_evidence_class":age_class(s["age_context"]),"source_status":"imported audit dictionary; historical original prompt/native image not independently authenticated","polarity_lane":"exclusion_only" if s["polarity"]=="부정" else "source_observation","research_propositions":[{"proposal_id":c["id"],"owner":c["owner_scope"],"proposition_en":c["proposition_en"],"directed_relations":c["directed_relations"]} for c in assigned],"existing_ids_to_review":list(dict.fromkeys(x for c in assigned for x in c["existing_ids_to_review"])),"phrase_presence_candidates":r["candidate_phrase_presence"],"phrase_presence_profiles":r["profile_phrase_presence"],"source_case_sexual_replay_policy":"not authorized; youth/mixed/unspecified ages cannot supply a sexual source replay","claim_limit":"meaning analysis and proposed visible configuration, not causal keyword effect, actual age, diagnosis, consent, perpetrator responsibility or rendered quality"})
 save("SEMANTIC-UNITS.json",{"schema_version":"vel-research-semantic-units/v1","units":units})
 with (OUT/"KEYWORD-CROSSWALK.csv").open("w",newline="",encoding="utf-8-sig") as f:
  w=csv.writer(f);w.writerow(["id","category","phrase","polarity","source_id","source_kind","age_context","age_evidence_class","proposal_ids","existing_ids_to_review"])
  for u in units:w.writerow([u["id"],u["category"],u["phrase"],u["polarity"],u["source_id"],u["source_kind"],u["age_context"],u["age_evidence_class"],";".join(u["proposal_ids"]),";".join(u["existing_ids_to_review"])])
 dims={"garment_detail":"appearance","wardrobe_style":"appearance","wearable_accessory":"appearance","surface_material":"material","texture":"material","body_pose":"pose","hand_pose":"pose","action":"action","relational_action":"relationship","contact_point":"pose","gaze_target":"expression","expression":"expression","viewer_position":"camera","camera_height":"camera","camera_direction":"camera","composition":"composition","focus":"camera","prop":"setting","skin_condition":"appearance","hair_style":"appearance","ambient_particle":"atmosphere","space_condition":"setting","aftermath_trace":"event","location":"setting","lighting":"lighting","light_type":"lighting","motion":"action","surreal_physics_detail":"concept","costume_style":"appearance"}
 drafts=[];mapping=[]
 interaction_ids={24,26,34,35,37,41,43,46,51}
 for c in cards:
  num=int(c["id"][-3:]);reuse=c["proposal_kind"]=="reuse_extend";new=c["proposal_kind"]=="new_relation_trial"
  current=sorted(set(f for k in c["existing_ids_to_review"] for f in id_files[k]))
  if num in interaction_ids:target=["skills/photo-prompt-image-generator/assets/photo_prompt_interaction_state_extension.json","skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_interaction_state.json"];target_state="proposed new authored sources, not created"
  elif num in {12,14,15}:target=["skills/photo-prompt-image-generator/assets/photo_prompt_portrait_fashion_exposure_extension.json","skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_portrait_fashion_exposure.json"];target_state="existing source; source-scoped adoption review required"
  elif num in {20,21}:target=["skills/photo-prompt-image-generator/assets/photo_prompt_accessory_structure_extension.json","skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_accessory_structure.json"];target_state="existing source; owner-specific variant review required"
  elif num in {38,39,45,47,48,50,54}:target=["skills/photo-prompt-image-generator/assets/photo_prompt_scene_state_relations_extension.json","skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_scene_state_relations.json"];target_state="proposed new authored sources, not created"
  elif num==4:target=["skills/photo-prompt-image-generator/assets/photo_prompt_clothing_structure_extension.json","skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_clothing_structure.json"];target_state="existing source"
  elif num==18:target=["skills/photo-prompt-image-generator/assets/photo_prompt_water_relations_extension.json","skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_water_relations.json"];target_state="existing source; glass-plane specificity required"
  else:target=current;target_state="existing IDs or research/generic contract lane"
  row={"proposal_id":c["id"],"kind":c["proposal_kind"],"existing_ids":c["existing_ids_to_review"],"current_source_files":current,"proposed_target_files":target,"target_state":target_state,"candidate_pack_contract":"photo-candidate-pack/v6 unchanged","runtime_ready":False,"adoption_requirements":["compare full current meaning, owner and effect; a lexical neighbor is not equivalence","resolve actual scene targets and property effects before adoption","new optional atom or bundle only within open dimensions","new exact hard activation requires paired narrow positives and context negatives; broad labels stay advisory","compile any adopted authored-components through current v2 compiler and preserve all selected prior gates"]}
  mapping.append(row)
  if reuse or new:
   primary=c["target_slots"][0]
   draft={"proposal_id":c["id"],"change_kind":"extend_equivalent_meaning_or_keep" if reuse else "new_optional_relation_trial","proposed_new_id":None if reuse else "vel_relation_"+c["id"][-3:],"primary_slot":primary,"en":c["proposition_en"],"concept_units":c["visual_components"],"relations":[{"id":"vel_"+c["id"][-3:]+"_r"+str(i+1),"type":r["predicate"],"subject":r["subject"],"object":r["object"]} for i,r in enumerate(c["directed_relations"])],"proposed_affected_dimensions":list(dict.fromkeys(dims[s] for s in c["target_slots"] if s in dims)),"property_effect_review":{"owner_scope":c["owner_scope"],"requires_concrete_runtime_targets":True,"target_or_property_changes_must_match_frozen_core":True,"cross_owner_transfer_forbidden":True},"current_equivalent_candidates_or_profiles_to_review":c["existing_ids_to_review"],"confusion_boundaries":c["confusion_boundaries"],"runtime_exact_terms":[],"promotion_blockers":["research-only; not validated as runtime schema","actual affected_properties target binding pending","equivalence/context/eligibility tests pending","indexes and current candidate-pack exposure pending","native pixel review and user judgment pending"],"runtime_ready":False}
   drafts.append(draft)
 save("CANDIDATE-DRAFTS.json",{"schema_version":"vel-research-candidate-drafts/v1","distributable_runtime_data":False,"drafts":drafts})
 save("RUNTIME-MAPPING.json",{"schema_version":"vel-research-runtime-mapping/v1","mappings":mapping,"actual_runtime_changes":[]})
 cases=[]
 for c in cards:
  if c["proposal_kind"] in {"reuse_extend","new_relation_trial"}:
   tests=[
    ("owned_positive",c["proposition_en"],"candidate meaning is eligible for consideration; optional hit never becomes mandatory"),
    ("owner_reversal","Swap the declared owner or target in "+c["id"],"not equivalent; reject adoption with a mismatched owner"),
    ("request_negation","Negate the complete requested relation for "+c["id"],"exclude the negated meaning without inventing a positive obligation"),
    ("locked_property","Lock a property affected by "+c["id"]+" to an incompatible existing value","reject candidate without rewriting request/core/identity"),
    ("required_occlusion","Occlude an adopted required component from "+c["id"],"native required gate cannot pass: UNOBSERVABLE_NOT_PASS"),
    ("zero_adoption","Retrieve "+c["id"]+" but author chooses zero adoption","preserve authored baseline and produce no new obligation"),
   ]
   tests += [("specific_confound_"+str(i+1),x,"do not substitute this configuration for "+c["id"]) for i,x in enumerate(c["confusion_boundaries"])]
   for kind,inp,expected in tests:cases.append({"id":c["id"]+"-"+kind,"proposal_id":c["id"],"kind":kind,"input_or_mutation":inp,"expected":expected,"status":"planned_not_executed","claim_limit":"development specification, not frozen lexical holdout or a test result"})
 for s in source["entries"]:
  if s["polarity"]=="부정":cases.append({"id":s["id"]+"-original-negative","keyword_id":s["id"],"kind":"source_negative_scope","input":s["phrase"],"source_context":s["role"],"expected":"retain original negative scope; no positive candidate/evidence inversion; defect intent remains separate","status":"planned_not_executed"})
 globals=[
 ("age-source-polarity","Keep S14 explicit age 15 and S15 youth context while analyzing nonsexual conflict","no sensual/fetish combination or invented adult source replay"),
 ("description-not-input","Treat all 97 descriptive entries as descriptions","no claim that they were final generation inputs"),
 ("red-not-blood","Red code particles or a crimson machine glow","not injury; no tissue-disruption candidate adoption"),
 ("historical-no-gore","A positive fictional action with explicit no-blood/no-gore","preserve allowed action and enforce scoped exclusions"),
 ("appearance-not-consent","Close lens eye contact or kneeling","no certification of consent, desire, personality or diagnosis"),
 ("research-not-runtime","A valid research candidate JSON","cannot enter runtime without manifest registration, target binding and index rebuild"),
 ("public-pack-no-scores","Emit a selected candidate in v6","private scores/ranks/raw research URLs remain outside public candidate meaning"),
 ("source-generation-integrity","Source text/hash/model vector changes","rebuild/review; never edit generated index shards by hand"),
 ]
 for id,inp,expected in globals:cases.append({"id":"GLOBAL-"+id,"kind":"global_boundary","input_or_mutation":inp,"expected":expected,"status":"planned_not_executed"})
 save("REGRESSION-PLAN.json",{"schema_version":"vel-research-regression-plan/v1","cases":cases,"status":"planned_not_executed","case_count":len(cases),"language_holdout_plan":"Before adoption, independently author natural Korean/English paraphrases and adjacent homonyms; freeze bytes separately from card-development examples. No real holdout success is claimed."})
 lines=["# Semantic cards — 60 reviewed research proposals","","All cards are researcher-authored design proposals. They are not live assets, mandatory meanings, or tested image effects.",""]
 for c in cards:
  lines += ["## "+c["id"]+" — "+c["title_ko"],"","- Keywords: "+", ".join(c["keyword_ids"]),"- Kind / priority: "+c["proposal_kind"]+" / "+c["priority"],"- Owner: "+c["owner_scope"],"- Slots: "+", ".join(c["target_slots"]),"- Observable proposition: "+c["proposition_en"],"- Components: "+"; ".join(c["visual_components"]),"- Relations: "+"; ".join(r["subject"]+" → "+r["predicate"]+" → "+r["object"] for r in c["directed_relations"]),"- Confusions: "+"; ".join(c["confusion_boundaries"]),"- Existing IDs to review: "+(", ".join(c["existing_ids_to_review"]) or "no equivalent existing ID established"),"- Research sources: "+", ".join("["+r+"]("+next(s["url"] for s in sources if s["id"]==r)+")" for r in c["research_source_ids"]),"- Adoption note: "+c["implementation_note_ko"],""]
 (OUT/"SEMANTIC-CARDS.md").write_text("\n".join(lines)+"\n")
 lines=["# Original 217-keyword crosswalk","","Source polarity, source kind and source age are retained verbatim. All proposal IDs are research-only.","","| Original ID | Category | Phrase | Polarity | Source | Proposals |","|---|---|---|---|---|---|"]
 for u in units:lines.append("| "+ " | ".join([u["id"],u["category"],u["phrase"].replace("|","/"),u["polarity"],u["source_id"],", ".join(u["proposal_ids"])])+" |")
 (OUT/"KEYWORD-CROSSWALK.md").write_text("\n".join(lines)+"\n")
 lines=["# External research sources","","20 primary publications, institutional object records, creator references and technical sources; their evidential scope differs.",""]
 for s in sources:lines += ["## "+s["id"]+" — "+s["title"],"","["+s["title"]+"]("+s["url"]+")","",s["finding"],"","- Type / date: "+s["kind"]+" / "+str(s["date"]),"- Checked: "+s["checked_on"],"- Inspected scope: "+s["locator"],"- Access: "+s["access"],"- Limits: "+s["limits"],""]
 (OUT/"SOURCES.md").write_text("\n".join(lines)+"\n")
 summary={"source_rows":len(units),"original_categories":22,"mapped_keywords":len(set(k for c in cards for k in c["keyword_ids"])),"proposal_cards":len(cards),"proposal_kinds":dict(collections.Counter(c["proposal_kind"] for c in cards)),"candidate_drafts":len(drafts),"new_relation_trials":sum(c["proposal_kind"]=="new_relation_trial" for c in cards),"bundle_menus":len(bundles),"external_sources":len(sources),"planned_regression_cases":len(cases),"executed_regression_cases":0,"runtime_changes":0,"image_generations":0,"age_evidence_counts":dict(collections.Counter(u["age_evidence_class"] for u in units))}
 save("RESEARCH-SUMMARY.json",summary);print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
