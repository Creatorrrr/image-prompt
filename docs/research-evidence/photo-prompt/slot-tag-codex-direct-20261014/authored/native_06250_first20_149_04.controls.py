"""Evidence/coverage/signature and exact reuse controls; no source mutation."""
import sys,json,copy,hashlib
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839');sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import native_reviews as nr
sys.path[:]=[str(G/'scripts'),str(G/'precore')]+[p for p in sys.path if p not in {str(ROOT/'skills/photo-prompt-image-generator/scripts'),str(G/'scripts'),str(G/'precore')}]
raw=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert raw(Path(e.__file__))=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
P=R/'native-inputs/prepared/review06250-00000-00020-149-04';O=R/'native_batches/review06250-00000-00020-149-04';I=json.load(open(P/'INPUT.json'));S=nr.artifact(ROOT,I['current_snapshot']);B=json.load(open(O/'BATCH.json'));OLD=json.load(open(R/'native_batches/review06250-00000-00020-149-03/BATCH.json'));checks=[]
for n in [3,4,5,8,9,10,13,14,15,16,17,18,19]:
 row=B['records'][n];old=OLD['records'][n];assert row['source_after']==old['source_after'] and row['dependency_records']==old['dependency_records'] and row['reference_bindings']==old['reference_bindings'] and c.canonical_bytes(row['proof'])==c.canonical_bytes(old['proof']);assert row['proof']['catalog_sha256']==c.digest(S['slot_catalog']) and all(v['spec_sha256']==c.digest(S['slot_catalog'][tag]) for tag,v in row['proof']['roles'].items());checks.append({'ordinal':n,'exact_source_proof_closure_catalog_spec_reuse':True,'new_read_credit':0,'proof_sha256':c.digest(row['proof'])})
for n in [0,1,2,6,7,11,12]:
 row=B['records'][n];cid=row['candidate_id'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=copy.deepcopy(row['proof']);data={**S,'candidates':{**S['candidates'],cid:rec}};results=[]
 assert row['source_after']==S['candidates'][cid]
 for field in ['en','ko','tags']:assert row['source_after']['content'][field]==row['source_before']['content'][field]
 assert row['proof']['owner_maps']['base']['schema']==e.MEMBER_OWNER_SCHEMA
 assert all('core_role' not in x and x['origin']=='existing' for x in row['proof']['owner_maps']['base']['bindings'])
 for f in row['proof']['facts']:
  if f['mode']=='effect':assert f['receivers']==(['illuminated_receivers'] if f['dimension']=='lighting' else [])
 for defect in ['missing_App','missing_KO','reference_only_App','metadata_fact','unsigned_value_change','E_downgraded_to_P','original_canonical_property_rename']:
  bad=copy.deepcopy(rec);p=bad['content']['role_evidence'];ef=next(f for f in p['facts'] if f['mode']=='effect')
  if defect=='missing_App':p['source_units']=[u for u in p['source_units'] if u['pointer']!='/content/application_contract']
  elif defect=='missing_KO':p['source_units']=[u for u in p['source_units'] if u['pointer']!='/content/ko']
  elif defect=='reference_only_App':p['source_units'][0].update(disposition='semantic_reference',reference_relation='partial_restatement',retained_constraint_rationale='Intentional invalid missing ordinary anchor test, not a semantic judgement.')
  elif defect=='metadata_fact':ef['pointer']='/content/tags/0';ef['quote']=bad['content']['tags'][0]
  elif defect=='unsigned_value_change':ef['value']['value']='unsigned_other_value'
  elif defect=='E_downgraded_to_P':ef['mode']='prerequisite';ef.pop('operation');ef.pop('receivers')
  else:ef['property']='lighting.renamed_for_role_prefix'
  if defect!='unsigned_value_change':p['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(p)
  try:e.validate(bad,S['slot_catalog'],corpus={**data,'candidates':{**data['candidates'],cid:bad}})
  except ValueError:results.append(defect)
  else:raise AssertionError((n,defect))
 checks.append({'ordinal':n,'rejected_controls':results,'unchanged_original_EN_KO_tags_provenance':True,'canonical_all_E_dimensions_properties_preserved':True,'existing_independent_point_and_complete_scope_selectors':True,'all_lighting_E_have_all_receiver_scope':True,'native_contract_sha256':row['proof']['review']['native_review']['native_contract_sha256']})
mods={}
for name,m in sorted(sys.modules.items()):
 if name.startswith(('photo_','photo_precore_')) and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'raw_sha256':raw(p)}
q=O/'CONTROLS.json';assert not q.exists();q.write_text(json.dumps({'schema':'photo-first20-source04-controls/v1','checks':checks,'actual_modules':mods,'boundary':'13 exact proof byte reuses,7 manually authored actual selected source04 proofs. Structure and source-value/qualification pin checks are not automatic language entailment, actual requester/complete universe verification, root acceptance or production adoption.'},ensure_ascii=False,indent=2)+'\n');print('PASS20',raw(q))
