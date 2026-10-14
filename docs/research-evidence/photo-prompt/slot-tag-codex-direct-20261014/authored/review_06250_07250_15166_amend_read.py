"""Print exact frozen15166 source, full closure and SOURCE binding definitions; no semantic automation."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R));import direct_review as d
p=json.loads((R/'packets/15000-250.json').read_text());s=d.source();cid=p['ids'][166];r=p['records'][cid]
print('PARENT',cid,json.dumps(r,ensure_ascii=False,indent=2))
print('REQUIRED_CLOSURE',json.dumps(d.closure(s,cid),ensure_ascii=False,indent=2))
for member in r['content'].get('member_candidates',[]):
 print('MEMBER_BINDING',json.dumps({'member':member,'binding':s['slot_bindings'][member['binding_id']]},ensure_ascii=False,indent=2))
print('ACTUAL_SOURCE_KIND',r['record_kind'])
import photo_candidate_realizations as pr
print('ACTUAL_RIDS',pr.ids(r))
