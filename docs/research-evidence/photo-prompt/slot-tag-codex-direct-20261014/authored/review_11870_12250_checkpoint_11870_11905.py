"""Serialize and validate the 35 explicit first-source decisions only.

No provider calls, source inference, registration, git or global report writes.
"""
import json, runpy, sys
from pathlib import Path
H = Path(__file__).resolve().parent
R = H.parent
sys.path.insert(0,str(R))
import direct_review as dr
L=runpy.run_path(str(H/'review_11870_12250_literals.py'))
D=L['D']; assert len(D)==35
p=json.loads((R/'packets/11870-130.json').read_text())
data=dr.source(); assert dr.c.digest(data)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
rows=[]; cache={}
for ordinal,meaning,boundary,selected in D:
 assert ordinal==11870+len(rows)
 roles={};facts=[]
 for tag,dimension,owner,prop,pointer,quote,rationale in selected:
  # Corrections below concern the individually inspected literal source pointer.
  if ordinal==11872 and tag=='attire_context': pointer='/content/paraphrases/2'
  if ordinal==11881 and tag=='ambient_particle':
   # Precipitation is declared, but distinct resolved particles are not.
   continue
  f=dict(pointer=pointer,quote=quote,dimension=dimension,target=owner,property=prop)
  facts.append(dict(f,realization_id='base'))
  if tag not in roles:
   roles[tag]=dict(slot_id=tag,semantic_role=data['slot_catalog'][tag]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale=rationale,evidence=[])
  else: roles[tag]['rationale']+=' '+rationale
  roles[tag]['evidence'].append(f)
 decision=dict(candidate_id=p['ids'][ordinal-11870],meaning_summary=meaning,recommended_kind='visual_option',corrections=L['CORRECTIONS'].get(ordinal,[]),roles=list(roles.values()),facts=facts,rejected_boundaries=[boundary],uncertainties=[],status='approved',all_roles_considered=True)
 assert not p['references'][decision['candidate_id']]
 assert dr.c.decode(dr.c.canonical_bytes(decision))==decision
 row={**dr.binding(data,decision['candidate_id'],cache=cache),**decision,'schema':dr.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':dr.c.digest(p),'authored_decision':{'file':str(Path(__file__).with_suffix('.json').relative_to(dr.ROOT)),'item':len(rows)+1,'sha256':dr.c.digest(decision)}}
 dr.validate_decision(row,data,binding_cache=cache)
 rows.append(decision)
result={'decisions':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'validated_count':len(rows),'start':11870,'stop':11905,'correction_ordinals':[11883],'unresolved_ordinals':[]},ensure_ascii=False))
