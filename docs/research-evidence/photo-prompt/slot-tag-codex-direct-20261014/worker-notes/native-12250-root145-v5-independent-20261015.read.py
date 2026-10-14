"""Read-only bounded independent catalog/witness reader; preparation is not direct reading."""
import json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d
p=json.loads((R/'authored/root_catalog145_v5_boundary_proposal_03.json').read_text());q=json.loads((R/'authored/native_catalog_v5_gap_proposal_02.json').read_text());before=json.loads((R/'CATALOG-FINAL-144-V4.json').read_text());after=p['proposed_catalog'];S=d.source();O=json.loads((R/'ORDER.json').read_text())
assert d.c.digest(before)==p['prior_catalog_sha256'];assert d.c.digest(after)==p['proposed_catalog_sha256'];assert len(after)==145
changed=sorted(k for k in after if before.get(k)!=after[k]);assert changed==p['changed_or_new_specs'];assert sum(before[k]==after[k] for k in before)==138
w={r['ordinal']:r for r in q['source_witnesses']}
for o,r in w.items():
 cid=r['candidate_id'];assert O[o]==cid;assert r['whole_original_source']==S['candidates'][cid];assert r['source_record_sha256']==d.c.digest(S['candidates'][cid]);assert sorted(r['complete_own_bindings'],key=lambda b:b['id'])==sorted([b for b in S['slot_bindings'].values() if b['candidate_id']==cid],key=lambda b:b['id'])
 loc=r['5B_locator'];f=d.ROOT/loc['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==loc['raw_sha256'];doc=json.loads(f.read_text());assert doc['decisions'][loc['index']]==r['whole_5B'];assert d.c.digest(r['whole_5B'])==loc['row_sha256']
 if 'source_only_revision_pin' in r:
  pin=r['source_only_revision_pin'];fp=Path(pin['file']);assert hashlib.sha256(fp.read_bytes()).hexdigest()==pin['raw_sha256'];rows=json.loads(fp.read_text())['records'];assert next(x for x in rows if x['ordinal']==o)==r['whole_source_only_revision_read']
mode=sys.argv[1]
if mode=='witness':
 for o in map(int,sys.argv[2:]):print('WITNESS',o,json.dumps(w[o],ensure_ascii=False,separators=(',',':')))
elif mode=='neighbors':
 keys=sorted({v for k in changed for v in after[k]['neighbors']}-set(changed));start,stop=map(int,sys.argv[2:]);
 for k in keys[start:stop]:print('NEIGHBOR',k,json.dumps(after[k],ensure_ascii=False,separators=(',',':')))
elif mode=='check':print(json.dumps(dict(changed=changed,unchanged_existing=138,old_count=len(before),new_count=len(after),catalog_sha=d.c.digest(after),witnesses=sorted(w),not_direct_read_count=True)))
