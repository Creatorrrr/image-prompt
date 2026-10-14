"""Lossless expansion of explicit hand-authored native draft tables only.

Every mode/target/value/operation/receiver/requires/owner/disposition/condition is
an explicit table cell. Only field names, full addressed quotes and hashes are
computed. No semantic decision, default empty array, proof or approval is made.
"""
import copy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
import direct_review as d
import photo_semantic_evidence as n
packet=d.c.decode((R/'authored/native_06250_00250_01250.prepared.json').read_bytes());oldbindings=d.c.decode((R/'authored/native_06250_00250_01250.bindings-prepared.json').read_bytes());catalog=d.c.decode((R/'CATALOG-FINAL-142-V2.json').read_bytes());by={r['ordinal']:r for r in packet['records']}
path=Path(sys.argv[1]);tables=d.c.decode(path.read_bytes());rows=[]
for table in tables:
 origin=by[table['ordinal']];after=d.corrected_record(origin['five_b_source_after'],table['source_edits']);facts=[]
 for cells in table['facts_table']:
  assert len(cells) in (10,12)
  fact=dict(zip(('id','realization_id','pointer','quote','dimension','target','property','mode','value','requires'),cells[:10]));assert len(cells[8])==2
  fact['value']=dict(zip(('type','value'),cells[8]))
  if len(cells)==12:fact.update(operation=cells[10],receivers=cells[11])
  n._fact_valid(fact);assert fact['quote'] in n.positive_string(after,fact['pointer'],realization_id=fact['realization_id']);facts.append(fact)
 owners={rid:{'schema':n.OWNER_SCHEMA,'bindings':[dict(zip(('target','core_role','origin','introduced_by'),cells)) for cells in values]} for rid,values in table['owners_table'].items()}
 units=[]
 for cells in table['units_table']:
  assert len(cells)==4;rid,pointer,refs,disposition=cells
  units.append(dict(realization_id=rid,pointer=pointer,quote=n.positive_string(after,pointer,realization_id=rid),fact_refs=refs,disposition=disposition))
 roles={tag:dict(zip(('scope','realization_ids','fact_refs','support_modes'),cells)) for tag,cells in table['roles_table'].items()}
 by_fact={f['id']:f for f in facts};assert len(by_fact)==len(facts)
 for rid,manual in table['effect_sets'].items():
  assert manual==n.effect_set(after,rid),(table['ordinal'],manual,n.effect_set(after,rid))
  active=[f for f in facts if f['realization_id']==rid];n._validate_owner_map(owners[rid],active)
  assert {n.property_key(f) for f in active if f['mode']=='effect'}=={n.property_key(x) for x in manual['properties']}
  assert n.primary_paths(after,rid)=={u['pointer'] for u in units if u['realization_id']==rid}
 for unit in units:
  for ref in unit['fact_refs']:assert by_fact[ref]['pointer']==unit['pointer'] and by_fact[ref]['realization_id']==unit['realization_id']
 for tag,role in roles.items():
  assert len(table['roles_table'][tag])==4
  for ref in role['fact_refs']:
   f=by_fact[ref];assert f['dimension'] in catalog[tag]['dimensions'];assert any(f['property'].startswith(p) for p in catalog[tag]['property_prefixes']);assert f['mode'] in role['support_modes']
 row={k:copy.deepcopy(v) for k,v in table.items() if k not in {'facts_table','owners_table','units_table','roles_table'}}
 row.update(candidate_id=origin['candidate_id'],facts=facts,roles=roles,owner_maps=owners,source_units=units,
  source_before=copy.deepcopy(origin['source_before']),five_b_source_after=copy.deepcopy(origin['five_b_source_after']),source_after=after,
  source_before_sha256=origin['source_before_sha256'],five_b_source_after_sha256=origin['five_b_source_after_sha256'],source_after_sha256=d.c.digest(after),
  original_compiled_locator=copy.deepcopy(origin['original_compiled_locator']),original_catalog_sha256=origin['five_b_compiled']['catalog_sha256'],
  catalog_sha256=d.c.digest(catalog),role_spec_sha256={tag:d.c.digest(catalog[tag]) for tag in roles},
  own_persistent_bindings_read=copy.deepcopy(oldbindings['bindings'][origin['candidate_id']]),reference_records=copy.deepcopy(origin['reference_records']),reference_bindings=copy.deepcopy(origin['reference_bindings']))
 rows.append(row)
output=path.with_name(path.name.replace('.tables.json','.draft.json'));assert output!=path
with output.open('x') as f:json.dump({'schema':'photo-codex-native-source-inventory-draft/v1','task_name':'/root/review_06250_07250','model':'gpt-6.1-sol','reasoning_effort':'high','catalog_sha256':d.c.digest(catalog),'prepared_packet_count':1000,'formal_input_assignment_received':False,'formal_native_reviews_authored':0,'operational_native_qualified_count':0,'records':rows},f,ensure_ascii=False,separators=(',',':'));f.write('\n')
for row in rows:print(json.dumps({'ordinal':row['ordinal'],'full_source_after_for_actual_reread':row['source_after']},ensure_ascii=False,separators=(',',':')))
print('DRAFT_PATH',output)
