#!/usr/bin/env python3
"""Read-only source inventory and lexical diagnostics for the vel study."""
from __future__ import annotations
import collections, csv, hashlib, json, sys, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
ASSETS=ROOT/"skills/photo-prompt-image-generator/assets"
SCRIPTS=ROOT/"skills/photo-prompt-image-generator/scripts"
sys.path.insert(0,str(SCRIPTS))
import prompt_generator as pg
from bm25f_retrieval import rank_bm25f

SLOTS={
"01":["mood","expression","aesthetic_trend","atmosphere"],
"02":["wardrobe_style","costume_style","garment_detail","silhouette_proportion"],
"03":["surface_material","texture","garment_detail"],
"04":["wardrobe_style","costume_style","garment_detail","neckline"],
"05":["surface_material","texture","hair_style","skin_condition","weather","garment_detail"],
"06":["wearable_accessory","garment_detail","fetish_styling"],
"07":["body_pose","body_orientation","hand_pose","contact_point","gaze_target","location","situation_context"],
"08":["expression","eye_detail","gaze_engagement","gaze_target","lip_finish"],
"09":["viewer_position","proxemics","distance_narrative","camera_height","camera_direction","composition","subject_framing","focus"],
"10":["prop","action","costume_style","wardrobe_style","footwear"],
"11":["action","hand_pose","relational_action","body_pose","contact_point"],
"12":["action","relational_action","prop","motion","ambient_particle","surreal_physics_detail"],
"13":["relational_action","body_pose","contact_point","viewer_position","hand_pose"],
"14":["expression","relational_action","action","intent_state","proxemics","situation_context","gaze_target","hand_pose"],
"15":["aftermath_trace","space_condition","location","ambient_particle","action","prop"],
"16":["skin_condition","aftermath_trace","garment_detail","surface_material","prop"],
"17":["expression","body_pose","action","hand_pose","contact_point","intent_state","narrative_phase"],
"18":["location","space_condition","atmosphere","body_pose","contact_point","surface_material","expression","surreal_concept"],
"19":["medium","lighting","light_direction","light_type","skin_finish","body_pose","contact_point","surface_material","grain_profile","color_grading","ambient_particle"],
"20":[],"21":[],
"22":["garment_detail","body_framing","subject_framing","expression","makeup_style","prop","ambient_particle","light_type"],
}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return " ".join("".join(c if c.isalnum() else " " for c in unicodedata.normalize("NFKC",s).casefold()).split())
def save(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
def positive(d):
 return {k:[(f,v) for f,vs in row.items() if f not in {"semantic_caption","slot_context"} for v in vs if isinstance(v,str) and v.strip()] for k,row in d.items()}
def presence(phrase,docs,allowed=None):
 n=" "+norm(phrase)+" "
 return [{"id":k,"field":f,"matched_text":v} for k,vals in docs.items() if allowed is None or k in allowed for f,v in vals if n in " "+norm(v)+" "][:8]

def main():
 seed=json.loads((OUT/"SOURCE-KEYWORDS.json").read_text())
 manifest=json.loads((ASSETS/"photo_prompt_source_manifest.json").read_text())
 paths=[ASSETS/x["file"] for x in manifest["sources"]]+[ASSETS/"photo_prompt_tags.json",ASSETS/"photo_prompt_visual_obligations.json",ASSETS/"photo_prompt_source_manifest.json"]+list(SCRIPTS.glob("*.py"))
 before={str(p.relative_to(ROOT)):digest(p) for p in paths}
 data=pg.load_json(ASSETS/"photo_prompt_tags.json")
 registry=pg.load_visual_obligation_registry(ASSETS/"photo_prompt_visual_obligations.json")
 assert all(digest(ROOT/p)==h for p,h in before.items()),"Concurrent source change during load"
 entries={k:(kind,e,slot) for k,kind,e,slot in pg.iter_semantic_entries(data)}
 cp=positive(pg.semantic_bm25f_documents(data)); pp=positive(pg.visual_profile_bm25f_documents(registry))
 ci=pg.build_semantic_bm25f_payload(data); pi=pg.build_visual_profile_bm25f_payload(registry)
 profiles={p["id"]:p for p in registry["profiles"]}
 inventory={"slots":{},"profiles":{},"semantic_non_slot_kinds":dict(collections.Counter(v[0] for v in entries.values()))}
 for k,(kind,e,slot) in entries.items():
  if kind=="slot":
   inventory["slots"][k]={"slot":slot,"en":e.get("en"),"ko":e.get("ko"),"concept_units":e.get("concept_units",[]),"relations":e.get("relations",[]),"affected_dimensions":e.get("affected_dimensions",[]),"affected_properties":e.get("affected_properties",[]),"requires":e.get("requires"),"contextual_usage":e.get("contextual_usage")}
 for k,p in profiles.items():
  inventory["profiles"][k]={"category":p.get("category"),"exact_terms":(p.get("activation") or {}).get("exact_terms",[]),"definition":(p.get("semantics") or {}).get("definition"),"visual_components":(p.get("semantics") or {}).get("visual_components",[]),"contrast_examples":(p.get("semantics") or {}).get("contrast_examples",[]),"required_evidence_fields":p.get("required_evidence_fields"),"support_concept_units":p.get("support_concept_units",[]),"authored_components":p.get("authored_components"),"runtime_expression":p.get("runtime_expression"),"render_gates":p.get("render_gates")}
 save("CURRENT-INVENTORY.json",inventory)
 rows=[]
 for i,s in enumerate(seed["entries"]):
  cat=s["category"][:2]; mapped=[x for x in SLOTS[cat] if x in data["slots"]]
  allowed={k for k,(kind,e,slot) in entries.items() if kind=="slot" and slot in mapped}
  r={**s,"mapped_slots":mapped,"candidate_phrase_presence":presence(s["phrase"],cp,allowed),"profile_phrase_presence":presence(s["phrase"],pp),"candidate_neighbors":[],"profile_neighbors":[],"diagnostic_scope":"phrase-only lexical diagnostics; not runtime applicability, equivalence, eligibility or exposure"}
  if s["polarity"]!="부정":
   q={"active_request":[s["phrase"]]}
   for n in rank_bm25f(ci,q,allowed_ids=allowed,limit=5):
    kind,e,slot=entries[n["document_id"]]
    r["candidate_neighbors"].append({"id":n["document_id"],"slot":slot,"en":e.get("en",e.get("definition"))})
   for n in rank_bm25f(pi,q,limit=5):
    p=profiles[n["document_id"]]
    r["profile_neighbors"].append({"id":n["document_id"],"definition":(p.get("semantics") or {}).get("definition")})
  else:r["negative_query_policy"]="excluded from positive lexical probes; original negation retained for firewall development cases"
  rows.append(r)
  if (i+1)%50==0:print("Probed",i+1,"/217",flush=True)
 drift=[p for p,h in before.items() if digest(ROOT/p)!=h]
 assert not drift,"Concurrent source change during probes: "+str(drift)
 summary={"source_rows":len(rows),"category_count":len(set(r["category"] for r in rows)),"source_count":len(seed["sources"]),"polarity_counts":dict(collections.Counter(r["polarity"] for r in rows)),"slot_count":len(data["slots"]),"slot_entry_count":len(inventory["slots"]),"semantic_document_count":len(entries),"profile_count":len(profiles),"candidate_bundle_count":len(data.get("candidate_bundles",[])),"manifest_source_counts":dict(collections.Counter(r["kind"] for r in manifest["sources"])),"positive_candidate_phrase_presence_rows":sum(bool(r["candidate_phrase_presence"]) for r in rows if r["polarity"]!="부정"),"positive_profile_phrase_presence_rows":sum(bool(r["profile_phrase_presence"]) for r in rows if r["polarity"]!="부정"),"positive_either_phrase_presence_rows":sum(bool(r["candidate_phrase_presence"] or r["profile_phrase_presence"]) for r in rows if r["polarity"]!="부정"),"dictionary_hash":pg.dictionary_hash(data),"visual_registry_hash":pg.visual_profile_registry_sha256(registry),"query_embedding_calls":0,"live_pack_calls":0,"generation_calls":0,"claim_limit":"Counts describe the current authored corpus and phrase presence; absent strings do not establish absent meaning."}
 save("CURRENT-COVERAGE.json",{"schema_version":"vel-research-keyword-crosswalk/v1","summary":summary,"rows":rows})
 save("AUDIT-SOURCE-HASHES.json",{"source_hashes":before,"changed_during_audit":drift})
 with (OUT/"LEXICAL-DIAGNOSTICS.csv").open("w",newline="",encoding="utf-8-sig") as f:
  w=csv.writer(f);w.writerow(["id","category","phrase","polarity","source_kind","age_context","candidate_phrase_presence","profile_phrase_presence","candidate_neighbors","profile_neighbors"])
  for r in rows:w.writerow([r["id"],r["category"],r["phrase"],r["polarity"],r["source_kind"],r["age_context"],";".join(x["id"] for x in r["candidate_phrase_presence"]),";".join(x["id"] for x in r["profile_phrase_presence"]),";".join(x["id"] for x in r["candidate_neighbors"]),";".join(x["id"] for x in r["profile_neighbors"])])
 print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
if __name__=="__main__":main()
