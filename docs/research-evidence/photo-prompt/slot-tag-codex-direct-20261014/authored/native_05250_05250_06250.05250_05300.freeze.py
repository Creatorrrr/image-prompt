"""Integrity and literal checks only; semantic decisions are manually authored."""
import copy, hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R))
import direct_review as dr
import photo_semantic_evidence as ne
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'authored/native_05250_05250_06250.05250_05300.packet.json'
d=R/'authored/native_05250_05250_06250.05250_05300.draft_before_reread.json'
pkt=json.loads(p.read_text());doc=json.loads(d.read_text());src=dr.source()
assert dr.c.digest(src)==pkt['source_sha256']==doc['source_sha256']
cat=json.loads((R/'CATALOG-FINAL-142-V2.json').read_text())
assert dr.c.digest(cat)==doc['catalog_sha256']=='0d7cab7b4add7279b0faa629bb5df72829da0c756adc6db21dcd7c09d56b971f'
order=json.loads((R/'ORDER.json').read_text())
checked_files={};fact_count=role_count=correction_count=0
for r,p in zip(doc['records'],pkt['records'],strict=True):
 o=r['ordinal'];cid=r['candidate_id'];assert order[o]==cid
 assert dr.c.canonical_bytes(src['candidates'][cid])==dr.c.canonical_bytes(r['source_before'])
 loc=r['original_compiled_locator'];path=dr.ROOT/loc['file']
 if path not in checked_files:checked_files[path]=(H(path),json.loads(path.read_text())['decisions'])
 fh,decisions=checked_files[path];original=decisions[loc['item']-1]
 assert fh==loc['file_sha256'] and dr.c.digest(original)==loc['row_sha256']
 assert original==r['original5B']
 after=dr.corrected_record(src['candidates'][cid],original['corrections']);after['record_kind']=original['recommended_kind']
 assert after==r['historical5B_after']
 assert r['source_intrinsic_conditions']==after['conditions']==r['source_after_proposal']['conditions']
 assert {k:v for k,v in src['slot_bindings'].items() if v['candidate_id']==cid}==r['original_own_bindings']
 assert r['actual_rids']==['base']==ne.realizations.ids(r['source_after_proposal'])
 assert not r['reference_records'] and not r['reference_bindings']
 assert not ne.referenced_records(r['source_after_proposal'],src)
 facts={f['id']:f for f in r['facts']};assert len(facts)==len(r['facts'])
 for f in facts.values():
  assert f['quote'] in ne.positive_string(r['source_after_proposal'],f['pointer'],realization_id='base')
  assert all(facts[x]['mode'] in {'preservation','prerequisite'} for x in f['requires'])
  if f['mode']=='effect':assert 'operation' in f and 'receivers' in f
  else:assert 'operation' not in f and 'receivers' not in f
 units=r['source_units'];assert {u['pointer'] for u in units}==ne.primary_paths(r['source_after_proposal'],'base')
 assert {f for u in units for f in u['fact_refs']}==set(facts)
 for u in units:
  assert u['quote']==ne.positive_string(r['source_after_proposal'],u['pointer'],realization_id='base')
  assert all(facts[x]['pointer']==u['pointer'] for x in u['fact_refs'])
 for tag,role in r['role_proposals'].items():
  assert role['spec_sha256']==dr.c.digest(cat[tag])
  for ref in role['fact_refs']:
   f=facts[ref];assert f['dimension'] in cat[tag]['dimensions']
   assert any(f['property'].startswith(x) for x in cat[tag]['property_prefixes'])
   assert f['mode'] in role['support_modes']
 effects=r['local_effect_sets']['base']
 assert effects==r['source_after_proposal']['effects']
 assert {(f['dimension'],f['target'],f['property']) for f in facts.values() if f['mode']=='effect'}=={(f['dimension'],f['target'],f['property']) for f in effects['properties']}
 assert r['formal_native_proof'] is None and r['native_signature'] is None
 assert not r['source_proposal_approved'] and not r['creation_permission_approved']
 fact_count+=len(facts);role_count+=len(r['role_proposals']);correction_count+=sum(x['pointer']!='/effects' for x in r['source_delta_from_historical5B_after'])
assert [r['ordinal'] for r in doc['records']]==list(range(5250,5300))
final=copy.deepcopy(doc)
final.update(checkpoint_state='frozen_manual_source_fact_draft_for_root_review',source_after_reread_count=50,
 integrity_and_literal_checks='passed; not formal native or independent semantic proof',formal_native_proof_count=0,
 qualified_count=0,whole_final_catalog_reviewed=False)
out=R/'authored/native_05250_05250_06250.05250_05300.draft.json'
with out.open('x') as f:f.write(json.dumps(final,ensure_ascii=False,separators=(',',':'))+'\n')
report=dict(ordinal_interval=[5250,5300],prepared=50,actual_source_and_binding_read=50,
 manually_authored=50,source_after_direct_or_exact_reuse_reread=50,formal_native_proof=0,qualified=0,
 facts=fact_count,roles=role_count,proposed_text_delta_fields=correction_count,
 output=str(out.relative_to(R)),output_byte_sha256=H(out),input_byte_sha256=H(d),
 checks='source/catalog/order/compiled-file-and-row/exact5B/own-bindings/closure/RIDs/quotes/source-unit-coverage/typed-shape/explicit-effects/spec-prefix-and-mode; integrity only')
print(json.dumps(report,ensure_ascii=False))
reportpath=R/'authored/native_05250_05250_06250.05250_05300.partial-checks.json'
with reportpath.open('x') as f:f.write(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
