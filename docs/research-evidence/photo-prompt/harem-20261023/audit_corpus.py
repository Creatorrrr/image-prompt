"""Read-only, lexical source audit. Never calls retrieval or changes runtime files."""
from pathlib import Path
import json, hashlib, re, collections

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT/'skills/photo-prompt-image-generator/assets'
PATTERNS = {
 'harem':r'harem|하렘', 'personality':r'tsundere|yandere|kuudere|dandere|츤데레|얀데레',
 'contact':r'kabedon|sleeve tug|lap pillow|bridal carry|interlaced fingers|카베돈|무릎베개|공주님 안기',
 'costume':r'garter belt|suspender belt|bustier|peignoir|가터벨트|뷔스티에|페뇨아르',
 'route':r'otome|오토메|branching route',
}

def canonical(x):
 return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode()

def run():
 target=HERE/'corpus-snapshot.json'
 if target.exists():
  raise SystemExit('Snapshot already exists; collect a later stage in a separate directory.')
 manifest=json.loads((ASSETS/'photo_candidate_corpus_manifest.json').read_text())
 records={}; bindings=collections.defaultdict(list); modules=[]
 for mod in manifest['modules']:
  p=ASSETS/mod['file']; raw=p.read_bytes(); d=json.loads(raw)
  modules.append(dict(**mod, sha256=hashlib.sha256(raw).hexdigest()))
  if mod['kind']=='candidates':
   for cid,record in d.get('candidates',{}).items():
    assert cid not in records, cid
    records[cid]=(mod['file'],record)
  if mod['kind']=='slot_bindings':
   for bid,b in d.get('slot_bindings',{}).items(): bindings[b['candidate_id']].append(b)
 matches=[]; counts=collections.Counter()
 for cid,(module,r) in records.items():
  c=r.get('content',{})
  # Flat source fields only: no nested research metadata, definitions or generated index.
  text=' '.join(str(c.get(k,'')) for k in ['en','ko','aliases','keywords','tags'])
  hit=[k for k,p in PATTERNS.items() if re.search(p,text,re.I)]
  if not hit: continue
  counts.update(hit)
  matches.append(dict(candidate_id=cid,module=module,match_groups=hit,record=r,
      record_sha256=hashlib.sha256(canonical(r)).hexdigest(),bindings=bindings[cid]))
 illustration=[]
 p=ROOT/'skills/subculture-illustration-image-generator/assets/research_evidence_moe_elements'
 for filename,key in [('moe_meaning_contracts_v1.json','contracts'),('moe_visual_additions_v1.json','profiles')]:
  d=json.loads((p/filename).read_text())
  for row in d[key]:
   text=canonical(row).decode()
   if re.search(r'NTR|netor|harem|tsundere|yandere|하렘|츤데레|얀데레|네토',text,re.I):
    illustration.append(dict(file=str((p/filename).relative_to(ROOT)),record=row))
 snapshot=dict(schema='harem-research-corpus-snapshot/v1',head=json.loads((HERE/'BASELINE.json').read_text())['head'],
  scope='Manifest candidate modules; lexical scan only, not semantic retrieval or completeness proof',
  modules=modules,candidate_count=len(records),binding_count=sum(map(len,bindings.values())),
  slot_count=len(json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']),
  patterns=PATTERNS,group_counts=dict(counts),match_count=len(matches),matches=matches,illustration_neighbors=illustration)
 target.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:snapshot[k] for k in ['candidate_count','binding_count','slot_count','match_count','group_counts']},ensure_ascii=False))

if __name__=='__main__': run()
