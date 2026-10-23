"""Read authored modules, snapshot bounded matches. No runtime loader or network."""
import collections, hashlib, json, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parents[4]
HERE=pathlib.Path(__file__).resolve().parent
ASSETS=ROOT/"skills/photo-prompt-image-generator/assets"
QUERIES={
 "trench":["trench coat"], "lapels":["notched lapel","shawl lapel","peaked lapel","peak lapel"],
 "pose":["contrapposto","over-the-shoulder look"], "view":["over-the-shoulder viewpoint"],
 "earpiece":["earpiece"], "reflection":["watching an implied target through a mirror"],
 "waistcoat":["three-piece suit with a separate waistcoat"],
 "satin":["Broad satin highlights follow"], "hair":["slicked-back wet-look","light stubble"],
 "dress":["slip dress"], "glove":["gloves worn to leave no trace"],
 "espionage":["cold-war espionage realism"], "cuff":["garment adjustment point"],
 "carry":["cheongsam with an angled front"],
 "gaps":["dead drop","cuff adjustment","chest rig","plate carrier","interrogation","handcuff"]
}
def main():
 manifest_path=ASSETS/"photo_candidate_corpus_manifest.json"
 before=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
 manifest=json.loads(manifest_path.read_text()); candidates={}; bindings={}; hashes={}
 for module in manifest["modules"]:
  if module["kind"] not in ("candidates","slot_bindings"): continue
  path=ASSETS/module["file"]; raw=path.read_bytes(); hashes[module["file"]]=hashlib.sha256(raw).hexdigest()
  data=json.loads(raw)[module["kind"]]
  target=candidates if module["kind"]=="candidates" else bindings
  for key,value in data.items():
   if key in target: raise ValueError("duplicate owner: "+key)
   target[key]={"module":module["file"],"record":value}
 hits={}; selected={}
 for category,queries in QUERIES.items():
  hits[category]={}
  for query in queries:
   matches=[]
   for cid,entry in candidates.items():
    c=entry["record"].get("content",{})
    text=" ".join(str(c.get(k,"")) for k in ("en","ko","phrase_en","phrase_ko"))
    if query.casefold() in text.casefold():
     matches.append(cid)
     if category!="gaps" and len(matches)<=4: selected[cid]=entry
   hits[category][query]=matches
 # Full source, conditions, effects, provenance and linked bindings are retained.
 for cid,entry in selected.items():
  linked={bid:b for bid,b in bindings.items() if cid in json.dumps(b["record"],ensure_ascii=False)}
  entry["bindings"]=linked
  entry["record_sha256"]=hashlib.sha256(json.dumps(entry["record"],ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 after=hashlib.sha256(manifest_path.read_bytes()).hexdigest()
 closure_stable=all(hashlib.sha256((ASSETS/f).read_bytes()).hexdigest()==h for f,h in hashes.items())
 report={"candidate_count":len(candidates),"binding_count":len(bindings),
         "manifest_sha256":before,"manifest_unchanged_during_read":before==after,
         "modules_unchanged_during_read":closure_stable,"source_module_sha256":hashes,"hits":hits,
         "method":"literal substring in four named positive fields; not retrieval or absence proof",
         "runtime_search":"NOT_RUN"}
 (HERE/"CORPUS-LEXICAL-AUDIT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
 (HERE/"existing-source-mapping.json").write_text(json.dumps(selected,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps({"candidates":len(candidates),"bindings":len(bindings),"snapshots":len(selected),"stable":closure_stable and before==after}))
if __name__=="__main__":main()
