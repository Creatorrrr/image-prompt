"""Serialize and validate only the78 individually authored source decisions.

No model call, semantic classifier, registration, global report or git action.
"""
import json,runpy,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R));import direct_review as dr
L=runpy.run_path(str(H/'review_11870_12250_literals_12000.py'))
p=json.loads((R/'packets/12000-250.json').read_text());data=dr.source()
assert dr.c.digest(data)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
authored={o:(m,b,selected,L['KINDS'].get(o,'visual_option')) for o,m,b,selected in L['D']}
for o,m,b in L['DIAGNOSTICS']:
 assert o not in authored
 authored[o]=(m,b,[],'diagnostic')
assert sorted(authored)==list(range(12000,12078))
target=Path(__file__).with_suffix('.json');assert not target.exists(),'never overwrite a frozen checkpoint'
rows=[];cache={}
for ordinal,(meaning,boundary,selected,kind) in sorted(authored.items()):
 roles={};facts=[]
 for tag,dim,owner,prop,pointer,quote,why in selected:
  f=dict(pointer=pointer,quote=quote,dimension=dim,target=owner,property=prop)
  facts.append(dict(f,realization_id='base'))
  if tag not in roles:roles[tag]=dict(slot_id=tag,semantic_role=data['slot_catalog'][tag]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale=why,evidence=[])
  else:roles[tag]['rationale']+=' '+why
  roles[tag]['evidence'].append(f)
 issues=L.get('UNCERTAINTIES',{}).get(ordinal,[])
 status='needs_boundary_review' if issues else 'diagnostic_reviewed' if kind=='diagnostic' else 'approved'
 decision=dict(candidate_id=p['ids'][ordinal-12000],meaning_summary=meaning,recommended_kind=kind,corrections=L.get('CORRECTIONS',{}).get(ordinal,[]),roles=list(roles.values()),facts=facts,rejected_boundaries=[boundary],uncertainties=issues,status=status,all_roles_considered=True)
 assert not p['references'][decision['candidate_id']]
 row={**dr.binding(data,decision['candidate_id'],cache=cache),**decision,'schema':dr.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':dr.c.digest(p),'authored_decision':dict(file=str(target.relative_to(dr.ROOT)),item=len(rows)+1,sha256=dr.c.digest(decision))}
 try:dr.validate_decision(row,data,binding_cache=cache)
 except Exception as exc:raise ValueError((ordinal,str(exc))) from exc
 rows.append(decision)
target.write_text(json.dumps(dict(decisions=rows),ensure_ascii=False,indent=2)+'\n')
from collections import Counter
print(json.dumps(dict(start=12000,stop=12078,validated=len(rows),statuses=dict(Counter(x['status'] for x in rows)),unresolved_ordinals=sorted(L['UNCERTAINTIES']))))
