"""Serialize individually authored profile judgments; no semantic classification."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(R));import direct_review as d
from photo_candidate_realizations import ids
P=R/'packets/18000-250.json';packet=json.loads(P.read_text());data=d.source()
def save(rows,complete=False,issues=None,corrections=None):
 assert [row[0] for row in rows]==list(range(18000,18000+len(rows)))
 out=[]
 for n,meaning,choices,boundary in rows:
  cid=packet['ids'][n-18000];rec=packet['records'][cid];assert ids(rec)==['base']
  roles=[];facts=[]
  for choice in choices:
   slot,owner,prop,quote,*rest=choice;ptr=rest[0] if rest else '/content/semantics/definition';scope=rest[1] if len(rest)>1 else 'whole_record';spec=data['slot_catalog'][slot]
   f={'pointer':ptr,'quote':quote,'dimension':spec['dimensions'][0],'target':owner,'property':prop}
   try:d.validate_fact(f,rec,data['slot_catalog'],slot)
   except Exception as e:raise ValueError((n,slot,prop,str(e),spec['property_prefixes'])) from e
   found=next((x for x in roles if x['slot_id']==slot),None)
   if found:found['evidence'].append(f)
   else:roles.append({'slot_id':slot,'semantic_role':spec['semantic_role'],'scope':scope,'realization_ids':['base'],'rationale':meaning+' The quoted proposition owns '+prop+' on '+owner+'.'+(' This role is supported only in the explicitly selected source alternative, whose native realization ID remains base.' if scope=='positive_alternative' else ''),'evidence':[f]})
   facts.append({**f,'realization_id':'base'})
  out.append({'candidate_id':cid,'meaning_summary':meaning,'recommended_kind':'visual_profile','corrections':(corrections or {}).get(n,[]),'roles':roles,'facts':facts,'rejected_boundaries':[boundary],'uncertainties':[],'status':'approved','all_roles_considered':True})
 path=R/'authored/review_18000_18250_18000_18250.json';d.write(path,{'decisions':out})
 for i,row in enumerate(out,1):
  d.validate_decision({**d.binding(data,row['candidate_id']),**row,'schema':d.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':d.c.digest(packet),'authored_decision':{'file':str(path.relative_to(d.ROOT)),'item':i,'sha256':d.c.digest(row)}},data)
 note={'task_name':'review_18000_18250','agent_id':'/root/review_18000_18250','model':'gpt-6.1-sol','reasoning_effort':'high','start':18000,'stop':18250,'packet_paths':[str(P.relative_to(d.ROOT))],'authored_paths':[str(path.relative_to(d.ROOT))],'complete_source_read':complete,'directly_reviewed_count':len(rows),'unresolved_ordinals':list(range(18000+len(rows),18250)),'complete_primary_records_read':len(rows),'reference_records_read':0,'frozen_slot_bindings_read':0,'next_unread_ordinal':18000+len(rows),'qualification_issues':issues or [
'All 250 assigned records are visual_profile with actual canonical realization ID base, no member_candidates, no candidate-reference closure, and no binding IDs. No parent/member role migration applies.',
'Canonical conditions, effects.dimensions and effects.properties are empty in this packet while primary authored components carry owned duties and activation guards. Semantic review does not certify canonical effect-lock completeness or bypass intrinsic/catalog eligibility.',
'Textual OR alternatives remain source alternatives on canonical RID base; no synthetic realization IDs or automatic role unions were introduced. Source native realization refinement may be needed where distinct options affect eligibility.',
'Clamshell ordinal 18067 eye catchlight applicability was directly read with visual_profile_contracts.py:245-280: the native projection filters active components and regenerates groups/evidence/gates/composition. Closed-eye omit/explicit-request retain guards remain authoritative.',
'Capture-direction roles were withheld from ambiguous stride/stance wording at ordinals 18105, 18106 and 18123. Explicit capture/view-axis sources elsewhere were judged separately.',
'Explicit authored source corrections currently address tracheal-versus-bronchial Korean translation at 18056 (two strings), handoff-object count scope at 18065 (two strings), and contradictory small-muscle-volume paraphrase at 18088 (one string).',
'Catalog domain/subject applicability is retained. Semantic role support is not a declaration that every source role is runtime-eligible in every domain.',
'No generation, embedding, network/API/model call, register, verify, canonical edit or git operation was performed. Native pixels, acquisition history, scientific/clinical efficacy and user acceptance remain untested.'
]};d.write(R/'worker-notes/review_18000_18250-18000-18250.json',note);print(len(out),'validated',path)
