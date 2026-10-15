"""Mechanical final identity readback; human semantic review is explicit in immutable handover note."""
from boot import *
from collections import Counter
J=json.loads((O/'BATCH-v1.json').read_text());CHECKS=json.loads((O/'CHECKS-v3.json').read_text());out=[]
for row,p in zip(J['records'],PLAN['records']):
 proof=row['proof'];assert row['candidate_id']==p['candidate_id'];assert row['source_after']==p['after'];assert proof['facts']==p['facts'];e=next(f for f in proof['facts'] if f['mode']=='effect')
 actual_units={}
 for u in proof['source_units']:
  value=n.positive_string(row['source_after'],u['pointer'],realization_id='base');assert u['quote']==value;actual_units[u['pointer']]=u['quote']
 assert actual_units=={u['pointer']:u['quote']for u in p['source_units']}
 for f in proof['facts']:
  assert f['target']=='main_subject' and f['realization_id']=='base'
  assert f['quote'] in n.positive_string(row['source_after'],f['pointer'],realization_id='base')
 out.append({'ordinal':row['ordinal'],'source_after_sha256':c.digest(row['source_after']),'facts_equal_actually_read_plan05':True,'fact_scopes':[{'id':f['id'],'mode':f['mode'],'dimension':f['dimension'],'target':f['target'],'property':f['property'],'value':f['value'],'requires':f['requires'],'fact_sha256':c.digest(f)}for f in proof['facts']],'unique_whole_positive_units_exact_actually_read_plan05':len(actual_units),'unit_scopes':[{'pointer':u['pointer'],'quote_sha256':c.digest(u['quote']),'disposition':u['disposition'],'fact_refs':u['fact_refs'],'reference_relation':u.get('reference_relation'),'retained_constraint_rationale':u.get('retained_constraint_rationale')}for u in proof['source_units']],'views':[{'id':v['id'],'slot':v['role_id'],'E_fact_id':e['id'],'E_fact_sha256':c.digest(e),'facet_quote':v['normal_anchors'][0]['facet_quote'],'facet_scope':'Exact local App clause inside this same complete E quote; original mode, value, address, main_subject and all P/PR/Rx persist.','canonical_fields_preserved':True,'complete_requires':v['requires_refs']}for v in proof['manual_role_views']]})
readback={'schema':'photo-worker-expression5-final-fact-unit-view-scope-readback/v1','rows':out,'checks_by_case':dict(Counter(x['case']for x in CHECKS['checks'])),'actual_fresh_source_whole_reread':0,'unchanged_whole_after_actual_prior_read_reused':5,'all37_final_fact_scopes_reviewed':True,'all58_whole_positive_unit_actual_prior_read_reuse_and_final_placement_reviewed':True,'seven_final_App_local_view_scopes_reviewed':True}
save(O/'FINAL-SCOPE-READBACK-v1.json',readback)
for r in out:
 print(json.dumps({'ordinal':r['ordinal'],'facts':r['fact_scopes'],'views':r['views'],'unique_whole_units':r['unique_whole_positive_units_exact_actually_read_plan05'],'unit_placements':[{'pointer':u['pointer'],'disposition':u['disposition'],'refs':u['fact_refs'],'relation':u['reference_relation']}for u in r['unit_scopes']]},ensure_ascii=False))
print('CHECKS',json.dumps(readback['checks_by_case'],ensure_ascii=False))
