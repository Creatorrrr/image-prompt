"""Freeze a uniform without-replacement sample; no semantic verdicts here."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import hashlib,json,random,secrets,subprocess,sys
ROOT=Path(__file__).resolve().parents[4];R=Path(__file__).parent;S=ROOT/'skills/photo-prompt-image-generator';sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
from photo_runtime_sources import RuntimeSnapshotProvider
sha=lambda raw:hashlib.sha256(raw).hexdigest()
if (R/'SAMPLE-MANIFEST.json').exists():raise SystemExit('frozen sample already exists; do not resample')
provider=RuntimeSnapshotProvider();snapshot=provider.acquire();corpus=c.load(S/'assets');assert c.digest(corpus)==snapshot.manifest['search_layout']['corpus_sha256']
source=c.decode((S/'assets'/c.MANIFEST_NAME).read_bytes());files={c.MANIFEST_NAME:sha((S/'assets'/c.MANIFEST_NAME).read_bytes())};owners={}
for module in source['modules']:
 raw=(S/'assets'/module['file']).read_bytes();files[module['file']]=sha(raw)
 if module['kind']=='candidates':
  for cid in c.decode(raw)['candidates']:owners[cid]=module['file']
bindings=defaultdict(list)
for row in corpus['slot_bindings'].values():bindings[row['candidate_id']].append(row)
seed=secrets.randbits(128);population=sorted(corpus['candidates']);ids=random.Random(seed).sample(population,1000)
rows=[]
for i,cid in enumerate(ids,1):
 rows.append({'sample_number':i,'source_file':owners[cid],'record_sha256':c.digest(corpus['candidates'][cid]),'candidate':corpus['candidates'][cid],'bindings':sorted(bindings[cid],key=lambda x:x['slot_id'])})
(R/'samples.jsonl').write_text(''.join(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n' for row in rows))
(R/'SLOT-CATALOG.json').write_bytes(c.canonical_bytes(corpus['slot_catalog']))
# Full positive/profile/bundle dependencies for interpreting sampled references.
refs=set()
def find(v):
 if isinstance(v,str) and v in corpus['candidates']:refs.add(v)
 elif isinstance(v,dict):
  for x in v.values():find(x)
 elif isinstance(v,list):
  for x in v:find(x)
for row in rows:find(row['candidate']['content'])
refs-=set(ids);(R/'REFERENCE-RECORDS.json').write_bytes(c.canonical_bytes({cid:corpus['candidates'][cid] for cid in sorted(refs)}))
meta={'created_at':datetime.now(timezone.utc).isoformat(),'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),'generation_id':snapshot.generation_id,'source_fingerprint':snapshot.manifest['source_fingerprint'],'corpus_sha256':c.digest(corpus),'seed_decimal':str(seed),'sampler':'python random.Random(int(seed)).sample(sorted(canonical_ids),1000)','population':len(population),'sample_count':len(ids),'sampling_unit':'canonical candidate, all six kinds, no replacement or post-selection','population_kinds':dict(Counter(r['record_kind'] for r in corpus['candidates'].values())),'sample_kinds':dict(Counter(r['candidate']['record_kind'] for r in rows)),'sample_with_persistent_binding':sum(bool(r['bindings']) for r in rows),'sample_binding_count':sum(len(r['bindings']) for r in rows),'sample_slot_counts':dict(Counter(b['slot_id'] for r in rows for b in r['bindings'])),'source_files_sha256':files,'samples_sha256':sha((R/'samples.jsonl').read_bytes()),'ordered_sample_ids_sha256':c.digest(ids),'catalog_sha256':c.digest(corpus['slot_catalog']),'reference_record_count':len(refs),'source_validation':'native corpus validate passed; semantic verdict not inferred','provider_calls':0,'image_calls':0}
(R/'SAMPLE-MANIFEST.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');(R/'reviews').mkdir();(R/'views').mkdir()
print(json.dumps({k:v for k,v in meta.items() if k not in ('source_files_sha256','sample_slot_counts')},ensure_ascii=False))
