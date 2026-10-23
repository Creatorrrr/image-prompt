"""Meaningful package-integrity checks; not semantic, runtime or image approval."""
import collections, hashlib, json, pathlib, re, sys
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read(name):return json.loads((HERE/name).read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 failures=[];checks=[]
 def check(label,value):
  checks.append({"check":label,"passed":bool(value)})
  if not value:failures.append(label)
 cards=read("semantic-cards.json");drafts=read("candidate-drafts.json")
 routes=read("keyword-routes.json");contexts=read("context-distinctions.json")
 sources=read("sources.json");cases=read("evaluation-cases.json")
 cids={x["id"] for x in cards};sids={x["id"] for x in sources}
 slots=json.loads((ROOT/"skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json").read_text())["slot_catalog"]
 check("unique card IDs",len(cids)==len(cards))
 check("unique source IDs",len(sids)==len(sources))
 check("one bilingual draft per card",len(drafts)==len(cards) and {x["card_ref"] for x in drafts}==cids)
 check("unique draft IDs",len({x["draft_id"] for x in drafts})==len(drafts))
 check("cards have English and Korean",all(x["visible_en"].strip() and re.search("[가-힣]",x["visible_ko"]) for x in cards))
 check("source references resolve",all(set(x["source_refs"])<=sids for x in cards+contexts+routes))
 check("roles are actual catalog keys",all(set(x["proposed_roles"])<=set(slots) for x in cards))
 check("relations and all endpoints present",all(x["directed_relations"] and all(e["subject"] in x["owners_and_parts"] and e["object"] in x["owners_and_parts"] and e["relation"] for e in x["directed_relations"]) for x in cards))
 check("compound endpoints expanded",all("_and_" not in e[k] for x in cards for e in x["directed_relations"] for k in ("subject","object")))
 check("two or more gates and confusions",all(len(x["observable_gates"])>=2 and len(x["confusion_boundaries"])>=2 for x in cards))
 check("all cards preserve strict pixel rules",all(x["pixel_rule"]=={"partial_is_fail":True,"unobservable":"UNOBSERVABLE_NOT_PASS","blocked":"BLOCKED_UNSCORED"} for x in cards))
 check("no native approval or runtime registration",all(x["native_approval"] is False and x["runtime_registered"] is False for x in cards))
 check("context excluded from positive retrieval",all(x["positive_retrieval_eligible"] is False for x in contexts))
 check("routes are advisory",all(x["hard_activation"] is False for x in routes))
 check("route and case targets resolve",all(set(x.get("card_refs",x.get("expected_card_refs",[])))<=cids for x in routes+cases))
 check("all evaluation bilingual and not run",all(x["query_en"] and x["query_ko"] and x["status"]=="NOT_RUN" for x in cases))
 check("case IDs unique",len({x["id"] for x in cases})==len(cases))
 check("literal smoke not presented as holdout",all(x["split"]!="heldout" for x in cases))
 ref=read("reference-conversation.json");expected=[]
 for ti,t in enumerate(ref["turns"]):
  for line_no,line in enumerate(t["items"][1]["text"].splitlines(),1):
   cells=line.split("|")
   if line.startswith("| **") and len(cells)>=4 and cells[1].strip().endswith("**"):
    expected.append((ti,line_no,cells[1].strip().strip("*"),cells[2].strip()))
 actual=[(r["source"]["turn_index"],r["source"]["line"],r["term_ko"]+(" — "+r["term_en"] if r["term_en"] else ""),r["original_definition"]) for r in routes]
 check("all complete original rows preserved exactly once",expected==actual)
 check("reference truncation recorded",all(t["items"][1]["truncated"] for t in ref["turns"]))
 old=read("existing-source-mapping.json")
 check("existing snapshots and bindings hashed",all(hashlib.sha256(json.dumps(x["record"],ensure_ascii=False,sort_keys=True).encode()).hexdigest()==x["record_sha256"] and x["bindings"] for x in old.values()))
 runtime=read("RUNTIME-CHECK.json")
 check("read-only runtime check",runtime.get("status")=="pass" and runtime.get("image_calls")==0 and runtime.get("source_writes")==0)
 for name in ("RESEARCH.md","IMPLEMENTATION-PLAN.md","README.md","CORPUS-FINDINGS.md","ACCESS-LIMITS.md","EVALUATION-PLAN.md","PIXEL-PLAN.md"):
  text=(HERE/name).read_text()
  for target in re.findall(r"\]\(([^)]+)\)",text):
   if "://" not in target:check("local link "+name+" -> "+target,(HERE/target.split("#")[0]).exists() or target in ("VALIDATION.json","SHA256SUMS"))
 baseline=read("BASELINE.json");changed=[];missing=[]
 for relative,h in baseline["protected_sha256"].items():
  f=ROOT/relative
  if not f.exists():missing.append(relative)
  elif digest(f)!=h:changed.append(relative)
 audit=read("CORPUS-LEXICAL-AUDIT.json")
 report={"status":"PASS" if not failures else "FAIL","scope":"research integrity only; no semantic truth or runtime/pixel qualification",
  "checks":checks,"failures":failures,"summary":read("SUMMARY.json"),
  "existing_source_read_stable":audit["manifest_unchanged_during_read"] and audit["modules_unchanged_during_read"],
  "protected_state":{"baseline_files":len(baseline["protected_sha256"]),"changed_since_baseline":changed,"missing_since_baseline":missing,
    "interpretation":"drift is reported separately; this validator never rewrites operating files"},
  "runtime_generation_id":runtime.get("generation_id"),"image_calls":0,"source_mutations_by_research_tools":0}
 (HERE/"VALIDATION.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
 members=sorted(p for p in HERE.iterdir() if p.is_file() and p.name!="SHA256SUMS")
 (HERE/"SHA256SUMS").write_text("".join(f"{digest(p)}  {p.name}\n" for p in members))
 print(json.dumps({"status":report["status"],"checks":len(checks),"failures":failures,"files_hashed":len(members),
   "protected_changed":len(changed),"protected_missing":len(missing)},ensure_ascii=False))
 if failures:sys.exit(1)
if __name__=="__main__":main()
