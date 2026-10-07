#!/usr/bin/env python3
"""Read authored sources only; no index publication, API call or pack access."""
import collections, hashlib, json, sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as pg
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ASSETS/'photo_prompt_source_manifest.json').read_text())
paths=[ASSETS/r['file'] for r in manifest['sources']]+[ASSETS/'photo_prompt_tags.json',ASSETS/'photo_prompt_visual_obligations.json',ASSETS/'photo_prompt_source_manifest.json']
before={str(p.relative_to(ROOT)):sha(p) for p in paths}
data=pg.load_json(ASSETS/'photo_prompt_tags.json')
registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
entries={key:{'kind':kind,'slot':slot,'entry':e} for key,kind,e,slot in pg.iter_semantic_entries(data)}
profiles={p['id']:p for p in registry['profiles']}
assert all(sha(ROOT/p)==h for p,h in before.items()),'Concurrent authored-source change during native load'
inventory={'status':'read_only_native_loader_snapshot','summary':{'manifest_source_count':len(manifest['sources']),'manifest_kinds':dict(collections.Counter(r['kind'] for r in manifest['sources'])),'slot_count':len(data['slots']),'slot_entry_count':sum(e['kind']=='slot' for e in entries.values()),'semantic_document_count':len(entries),'profile_count':len(profiles),'bundle_count':len(data.get('candidate_bundles',[])),'dictionary_hash':pg.dictionary_hash(data),'registry_hash':pg.visual_profile_registry_sha256(registry),'embedding_calls':0,'live_pack_calls':0,'generation_calls':0},'manifest':manifest,'source_hashes':before,'slot_names':list(data['slots']),'entries':entries,'profiles':profiles}
(OUT/'CURRENT-INVENTORY.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
patterns=['ribbed','ring','towel','condensation','slit','choker','corset','mirror','supine','contrapposto','no_contact','gaze','bandage','transparent','status_led','gauze']
matches={}
for pattern in patterns:
 hits=[]
 for key,row in entries.items():
  if row['kind']!='slot':continue
  e=row['entry']; text=' '.join(str(e.get(k,'')) for k in ('id','en','ko','aliases','exact_terms')).casefold()
  if pattern in text:
   hits.append({'id':key,'slot':row['slot'],'en':e.get('en'),'ko':e.get('ko')})
 ph=[]
 for key,p in profiles.items():
  text=' '.join(str(p.get(k,'')) for k in ('id','activation','semantics')).casefold()
  if pattern in text:
   ph.append({'id':key,'definition':(p.get('semantics') or {}).get('definition')})
 matches[pattern]={'candidates':hits,'profiles':ph}
(OUT/'LEXICAL-REVIEW-NEIGHBORS.json').write_text(json.dumps({'claim_limit':'substring neighbors for manual inspection; no equivalence or runtime eligibility proof','matches':matches},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(inventory['summary'],ensure_ascii=False,indent=2))
for pattern in ('ribbed','towel','mirror','corset','no_contact','status_led'):
 print(pattern,json.dumps({k:v[:8] for k,v in matches[pattern].items()},ensure_ascii=False))
