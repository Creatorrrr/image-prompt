"""Apply only new reviewed sources plus manifest append; keep current primary sources."""
from pathlib import Path
import hashlib
import json
import shutil
import stat
import sys
from datetime import datetime,timezone,timedelta

WORKTREE=Path(__file__).resolve().parents[4]
PRIMARY=Path("/Users/chasoik/Projects/image-prompt")
REL=Path("skills/photo-prompt-image-generator")
EVIDENCE=Path("docs/research-evidence/photo-prompt/fashion-fit-integration-20261008")
sys.path.insert(0,str(WORKTREE/REL/"scripts"))
import prompt_generator as pg
from photo_runtime_sources import source_update

def fingerprint(p):
 return {"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"mode":stat.S_IMODE(p.stat().st_mode),"bytes":p.stat().st_size}

def dump(p,d):
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")

def main():
 dst=PRIMARY/EVIDENCE;dst.mkdir(parents=True,exist_ok=True)
 before={}
 for p in (PRIMARY/REL/"assets").glob("*.json"):
  before[str(p.relative_to(PRIMARY))]=fingerprint(p)
 for area in ("scripts","precore","references"):
  for p in (PRIMARY/REL/area).rglob("*"):
   if p.is_file() and "__pycache__" not in p.parts: before[str(p.relative_to(PRIMARY))]=fingerprint(p)
 before[str(REL/"SKILL.md")]=fingerprint(PRIMARY/REL/"SKILL.md")
 dump(dst/"PRIMARY-PREAPPLY.json",{"checked_at_kst":datetime.now(timezone(timedelta(hours=9))).isoformat(),"files":before})
 manifest_path=PRIMARY/REL/"assets/photo_prompt_source_manifest.json"
 manifest=json.loads(manifest_path.read_text());old_rows=list(manifest["sources"])
 candidate=WORKTREE/REL/"assets/photo_prompt_fashion_fit_extension.json"
 visual=WORKTREE/REL/"assets/photo_prompt_visual_obligations_fashion_fit.json"
 ext=json.loads(candidate.read_text())
 for name,kind in [(candidate.name,"candidate"),(visual.name,"visual_profile")]:
  if (PRIMARY/REL/"assets"/name).exists(): raise ValueError("Primary destination already exists: "+name)
  if any(row["file"]==name for row in manifest["sources"]): raise ValueError("Manifest already owns "+name)
  manifest["sources"].append({"file":name,"kind":kind,"required":True,
    "load_order":max(s["load_order"] for s in manifest["sources"] if s["kind"]==kind)+1})
 with source_update(PRIMARY/REL):
  if json.loads(manifest_path.read_text())["sources"]!=old_rows:
   raise ValueError("Concurrent manifest change; recapture and merge again without overwriting it.")
  for p in (candidate,visual):
   shutil.copy2(p,PRIMARY/REL/"assets"/p.name)
  for p in (WORKTREE/"docs/research-evidence/photo-prompt/extension-maintenance").glob("fashion-fit-observable-variants-20261008*.json"):
   target=PRIMARY/"docs/research-evidence/photo-prompt/extension-maintenance"/p.name
   if target.exists() and target.read_bytes()!=p.read_bytes(): raise ValueError("Maintenance record collision: "+p.name)
   if not target.exists():shutil.copy2(p,target)
  dump(manifest_path,manifest)
 test=WORKTREE/"tests/test_photo_fashion_fit_semantics.py"
 target=PRIMARY/"tests"/test.name
 if target.exists():raise ValueError("Existing test path collision")
 shutil.copy2(test,target)
 for p in (WORKTREE/EVIDENCE).iterdir():
  if p.is_file() and p.name not in {"PRIMARY-BEFORE.json","PRIMARY-PREAPPLY.json","PRIMARY-APPLICATION.json"}:
   shutil.copy2(p,dst/p.name)
 payload=pg.load_semantic_index_payload(WORKTREE/REL/"assets/photo_prompt_semantic_index.json")
 keys={f"slot:{slot}:{r['id']}" for slot,rows in ext["slots"].items() for r in rows}
 keys.update(f"slot:{slot}:{cid}" for slot,updates in ext["existing_slot_context_extensions"].items() for cid in updates)
 cache={k:payload[k] for k in ("provider","embedding_model","embedding_dimensions")}
 cache["entries"]={k:payload["entries"][k] for k in keys}
 cache["cache_scope"]="Exact existing vectors/text only for this task's new/reused entries; auxiliary builder checkpoint, never a runtime index."
 checkpoint=dst/"isolated-compatible-vector-cache.json"
 dump(checkpoint,cache)
 after={rel:fingerprint(PRIMARY/rel) for rel in before}
 changes=[rel for rel in before if before[rel]!=after[rel]]
 if changes!=[str(REL/"assets/photo_prompt_source_manifest.json")]:
  # Other writers may operate independently; retain observations, never restore them.
  unexpected=[rel for rel in changes if rel!=str(REL/"assets/photo_prompt_source_manifest.json")]
 else:unexpected=[]
 dump(dst/"PRIMARY-APPLICATION.json",{
  "checked_at_kst":datetime.now(timezone(timedelta(hours=9))).isoformat(),
  "written_authored_files":[str(REL/"assets"/candidate.name),str(REL/"assets"/visual.name),str(REL/"assets/photo_prompt_source_manifest.json")],
  "existing_manifest_rows_preserved":manifest["sources"][:len(old_rows)]==old_rows,
  "existing_manifest_row_count":len(old_rows),"new_manifest_rows":manifest["sources"][len(old_rows):],
  "unchanged_original_files":sum(before[k]==after[k] for k in before),
  "compared_original_files":len(before),"changed_paths":changes,"concurrent_unexpected_differences":unexpected,
  "compatible_cache_entries":len(cache["entries"]),"cache_provider":cache["provider"],
  "cache_model":cache["embedding_model"],"cache_dimensions":cache["embedding_dimensions"],
  "primary_index_rebuild":"pending","source_only_application":True})
 print(json.dumps({"manifest_rows_preserved":len(old_rows),"new_sources":2,"compatible_vectors":len(cache["entries"]),"unexpected_differences":unexpected}))

if __name__=="__main__":main()
