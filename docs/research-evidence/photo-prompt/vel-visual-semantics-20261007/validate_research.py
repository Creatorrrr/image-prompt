#!/usr/bin/env python3
"""Research-package integrity, never runtime or image qualification."""
from __future__ import annotations
import ast,collections,csv,hashlib,json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def read(n):return json.loads((OUT/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 s=read("SOURCE-KEYWORDS.json");c=read("RESEARCH-PROPOSALS.json")["cards"];u=read("SEMANTIC-UNITS.json")["units"]
 d=read("CANDIDATE-DRAFTS.json")["drafts"];b=read("BUNDLE-DRAFTS.json")["bundles"];r=read("REGRESSION-PLAN.json")
 sources=read("SOURCES.json")["primary_sources"];p=read("PIXEL-QUALIFICATION-PLAN.json");m=read("RUNTIME-MAPPING.json")["mappings"]
 inv=read("CURRENT-INVENTORY.json");cov=read("CURRENT-COVERAGE.json");summary=read("RESEARCH-SUMMARY.json")
 source_ids={x["id"] for x in s["entries"]};card_ids={x["id"] for x in c};external_ids={x["id"] for x in sources};inventory_ids=set(inv["slots"])|set(inv["profiles"])
 assert len(s["entries"])==len(source_ids)==217
 assert len({x["category"] for x in s["entries"]})==s["summary"]["category_count"]==22
 assert len(s["sources"])==19
 assert dict(collections.Counter(x["polarity"] for x in s["entries"]))=={"긍정":100,"설명":97,"부정":20}
 assert source_ids=={"K"+str(i).zfill(3) for i in range(1,218)}
 assert len(c)==len(card_ids)==60
 assert {k for x in c for k in x["keyword_ids"]}==source_ids
 assert len(u)==217 and {x["id"] for x in u}==source_ids
 for x in u:
  original=next(row for row in s["entries"] if row["id"]==x["id"])
  assert all(x[k]==v for k,v in original.items()),"Changed source meaning/polarity/provenance "+x["id"]
  assert set(x["proposal_ids"])<=card_ids and x["proposal_ids"]
  assert x["source_id"] in s["sources"]
  if x["polarity"]=="부정":assert x["polarity_lane"]=="exclusion_only"
 slots={v["slot"] for v in inv["slots"].values()}
 for x in c:
  assert x["runtime_ready"] is False
  assert set(x["keyword_ids"])<=source_ids
  assert set(x["research_source_ids"])<=external_ids
  assert set(x["existing_ids_to_review"])<=inventory_ids,(x["id"],"Unknown existing ID")
  assert set(x["target_slots"])<=slots,(x["id"],"Unknown current slot")
  assert x["confusion_boundaries"] and x["proposition_en"] and x["owner_scope"]
  for rel in x["directed_relations"]:assert set(rel)=={"subject","predicate","object"} and all(rel.values())
 assert len(d)==46 and sum(x["change_kind"]=="new_optional_relation_trial" for x in d)==24
 for x in d:
  assert x["runtime_ready"] is False and x["runtime_exact_terms"]==[]
  assert x["proposal_id"] in card_ids and x["primary_slot"] in slots
  assert x["property_effect_review"]["requires_concrete_runtime_targets"] is True
 for x in m:
  assert x["runtime_ready"] is False and set(x["existing_ids"])<=inventory_ids
  for filename in x["current_source_files"]:assert (ROOT/filename).exists()
  if "proposed new" not in x["target_state"]:
   for filename in x["proposed_target_files"]:assert (ROOT/filename).exists(),filename
 assert len(m)==60 and len(b)==12
 for x in b:assert set(x["member_ids"])<=card_ids and x["runtime_ready"] is False
 assert len(sources)==len(external_ids)==20
 assert all(x["url"].startswith("https://") and x["locator"] and x["limits"] for x in sources)
 assert len(r["cases"])==r["case_count"]==462 and len({x["id"] for x in r["cases"]})==462
 assert all(x["status"]=="planned_not_executed" for x in r["cases"])
 assert len(p["groups"])==18 and all(x["status"]=="planned_not_executed" for x in p["groups"])
 assert sum(x["priority"]=="proposed_P0_pilot" for x in p["groups"])==6
 assert p["sampling_plan"]["currently_generated"]==0 and p["sampling_plan"]["initial_pilot_planned_images"]==36
 for x in p["groups"]:assert set(x["proposal_ids"])<=card_ids and x["all_of_native_gates"]
 assert summary["executed_regression_cases"]==summary["runtime_changes"]==summary["image_generations"]==0
 assert cov["summary"]["source_rows"]==217
 assert {x["id"] for x in cov["rows"]}==source_ids
 assert cov["summary"]["query_embedding_calls"]==cov["summary"]["live_pack_calls"]==cov["summary"]["generation_calls"]==0
 for x in cov["rows"]:
  if x["polarity"]=="부정":assert not x["candidate_neighbors"] and not x["profile_neighbors"]
 receipt=read("SOURCE-DOWNLOAD-RECEIPT.json")
 assert sha(OUT/"SOURCE-KEYWORDS.json")==receipt["sha256"]
 downloaded=Path(receipt["original_path"])
 if downloaded.exists():assert sha(downloaded)==receipt["sha256"]
 for script in OUT.glob("*.py"):ast.parse(script.read_text(),filename=str(script))
 for filename in ["RESEARCH.md","IMPLEMENTATION-PLAN.md","SEMANTIC-CARDS.md","KEYWORD-CROSSWALK.md","SOURCES.md"]:
  text=(OUT/filename).read_text()
  for target in re.findall(r"\]\(([^)]+)\)",text):
   if not re.match(r"^[a-z]+:",target) and not target.startswith("#") and target != "VALIDATION.json":assert (OUT/target.split("#")[0]).exists(),(filename,target)
 for filename in ["KEYWORD-CROSSWALK.csv","LEXICAL-DIAGNOSTICS.csv"]:
  with (OUT/filename).open(encoding="utf-8-sig",newline="") as f:assert len(list(csv.DictReader(f)))==217
 snapshot=read("CURRENT-SOURCE-SNAPSHOT.json")
 drift=[{"path":f["path"],"snapshot_sha256":f["sha256"],"current_sha256":sha(ROOT/f["path"]) if (ROOT/f["path"]).exists() else None} for f in snapshot["files"] if not (ROOT/f["path"]).exists() or sha(ROOT/f["path"])!=f["sha256"]]
 audited=read("AUDIT-SOURCE-HASHES.json")["source_hashes"]
 drift_after_audit=[filename for filename,h in audited.items() if not (ROOT/filename).exists() or sha(ROOT/filename)!=h]
 out={"status":"PASS_RESEARCH_INTEGRITY","source_rows":217,"source_categories":22,"preserved_source_fields":True,"source_sha256_verified":receipt["sha256"],"cards":60,"candidate_drafts":46,"new_relation_trials":24,"bundle_menus":12,"external_sources":20,"planned_regression_cases":462,"executed_regression_cases":0,"pixel_contrast_groups":18,"planned_pilot_images":36,"actual_image_generations":0,"unknown_existing_ids":0,"active_runtime_adoption":False,"index_publication":False,"source_snapshot_drift_count":len(drift),"source_snapshot_drift":drift,"source_drift_after_lexical_audit":drift_after_audit,"evidence_limit":"Package integrity and read-only current lexical diagnostics only; no live frozen-core pack, native image success, user acceptance or causal effect verified.","preservation_limit":"Source hash comparison records drift; it is not attribution of writes by other concurrent sessions."}
 (OUT/"VALIDATION.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps({k:v for k,v in out.items() if k!="source_snapshot_drift"},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
