import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d;import photo_semantic_evidence as n;import photo_candidate_realizations as r
s=d.source();o=json.loads((R/'ORDER.json').read_text())
for i in map(int,sys.argv[1:]):
 cid=o[i];rec=s['candidates'][cid];refs=n.referenced_records(rec,s);row=dict(ordinal=i,candidate_id=cid,source=rec,actual_rids=r.ids(rec),local_effect_sets={rid:n.effect_set(rec,rid) for rid in r.ids(rec)},references={k:s['candidates'][k] for k in refs if d.c.ID.fullmatch(k)},bindings={k:s['slot_bindings'][k] for k in refs if d.c.BINDING_ID.fullmatch(k)})
 path=R/f'authored/botanical_catalog_v2_12250_witness_{i}.json'
 if not path.exists():d.write(path,row)
 assert json.loads(path.read_text())==row
 print(json.dumps(row,ensure_ascii=False,separators=(',',':')))
