"""Authorized evidence-only revision after root preserved before snapshots."""
import json,sys
from pathlib import Path
r=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');sys.path.insert(0,str(r));import direct_review as d
p=json.loads((r/'packets/01250-250.json').read_text());a=r/'authored/review_01250_02250_01250_01500.json';v=json.loads(a.read_text())
for ordinal,prop in [(1341,'props.type.ready_weapon'),(1418,'body.pose.seated')]:
 row=v['decisions'][ordinal-1250];ko=p['records'][row['candidate_id']]['content']['ko']
 for fact in row['facts']:
  if fact['property']==prop:fact.update(pointer='/content/ko',quote=ko)
 for role in row['roles']:
  for fact in role['evidence']:
   if fact['property']==prop:fact.update(pointer='/content/ko',quote=ko)
d.write(a,v)
for script,old,new in [('review_01250_02250_1250b.py','prop:weapon:ready_weapon','prop@ko:weapon:ready_weapon'),('review_01250_02250_1250d.py','body_pose:participants:seated','body_pose@ko:participants:seated')]:
 path=r/'authored'/script;path.write_text(path.read_text().replace(old,new))
n=r/'worker-notes/review_01250_02250-01250-01500.json';note=json.loads(n.read_text());note['evidence_pointer_revision']={'ordinals':[1341,1418],'before_snapshot':'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/revisions/01250-01500-evidence-pointer-correction','authorization':'Root preserved authored/compiled/note before snapshots and exact hashes and explicitly authorized this evidence-only revision.','change':'Weapon in 1341 and seated pose in 1418 now cite their actual Korean positive text. Meanings and roles unchanged; original literal authoring scripts updated to reproduce Korean pointers.'};d.write(n,note)
data=d.source()
for i,row in enumerate(v['decisions'],1):d.validate_decision(dict(d.binding(data,row['candidate_id'])|row,schema=d.SCHEMA,reviewer='Codex',review_method='codex_direct_source_read',independent_human_review=False,packet_sha256=d.c.digest(p),authored_decision=dict(file=str(a),item=i,sha256=d.c.digest(row))),data)
print('authorized evidence-only revision validated')
