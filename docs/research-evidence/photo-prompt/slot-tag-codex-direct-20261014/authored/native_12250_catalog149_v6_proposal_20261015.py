"""Immutable research composition only; no approval, source/proof or runtime mutation."""
import copy, datetime, hashlib, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
STEM='native_12250_catalog149_v6_proposal_20261015'
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def artifact(name):
 p=R/name
 return dict(path=str(p),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
base_path=R/'CATALOG-FINAL-146-V5.json';base_raw=base_path.read_bytes();base=json.loads(base_raw)
assert digest(base)=='3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645'
mechanics_name='authored/native_12250_taxonomy_mechanics_articulation_relational_20261015.json'
mass_name='authored/native_12250_taxonomy_mass_20261015.json'
m=json.loads((R/mechanics_name).read_bytes());q=json.loads((R/mass_name).read_bytes())
assert digest(m)=='7cb6652ea80520d1be8b77e57ce952a612cb0b12cdd21de5aff563dac1cbc4dc'
assert digest(q)=='2e60ca6d630fd245398e677dbaed752143c34b8101baeecba38a8c6455a42320'
assert m['catalog_sha256']==q['catalog_sha256']==digest(base)
new=copy.deepcopy(base)
for k in ['material_mechanics','material_thickness']:
 assert k not in base;new[k]=copy.deepcopy(m['research_new_slots'][k])
assert 'physical_mass' not in base;new['physical_mass']=copy.deepcopy(q['after'])
revision=m['existing_spec_revision_proposals']['body_pose'];assert revision['before']==base['body_pose']
new['body_pose']=copy.deepcopy(revision['after'])
new_keys=sorted(set(new)-set(base)); changed=sorted(k for k in base if new[k]!=base[k]);unchanged=sorted(k for k in base if new[k]==base[k])
assert new_keys==['material_mechanics','material_thickness','physical_mass'] and changed==['body_pose'] and len(unchanged)==145 and len(new)==149
changed_fields=sorted(k for k in set(base['body_pose'])|set(new['body_pose']) if base['body_pose'].get(k)!=new['body_pose'].get(k))
assert changed_fields==['description','description_ko','excludes','includes']
assert new['relational_action']==base['relational_action']
# Structural checks are deliberately local/stdlib: they are not native qualification.
fields=set(next(iter(base.values())))
allowed={k:set(v for s in base.values() for v in s[k]) for k in ['dimensions','owners','core_fields']}
for name,spec in new.items():
 assert set(spec)==fields and spec['id']==name
 assert isinstance(spec['applicability'],dict)
 for key in ['description','description_ko','semantic_role','priority']:assert isinstance(spec[key],str) and spec[key]
 for key in ['core_fields','dimensions','owners','property_prefixes','evidence_terms','includes','excludes','neighbors']:
  assert isinstance(spec[key],list) and all(isinstance(v,str) and v for v in spec[key])
  assert len(spec[key])==len(set(spec[key]))
 for key in allowed:assert set(spec[key])<=allowed[key]
 assert spec['semantic_role'] in {s['semantic_role'] for s in base.values()} and spec['priority'] in {s['priority'] for s in base.values()}
 assert set(spec['neighbors'])<=set(new) and name not in spec['neighbors']
 assert spec['property_prefixes']
# Actual literal-prefix overlaps are reported, never treated as positive semantic evidence.
overlap=[]
for name in new_keys:
 for prefix in new[name]['property_prefixes']:
  for other,spec in new.items():
   if other==name:continue
   for old in spec['property_prefixes']:
    if prefix.startswith(old) or old.startswith(prefix):overlap.append(dict(new_slot=name,new_prefix=prefix,other_slot=other,other_prefix=old,relation='literal_prefix_overlap_requires_independent_manual_semantic_fit'))
unchanged_hashes={k:dict(before=digest(base[k]),after=digest(new[k]),canonical_spec_bytes_equal=True) for k in unchanged}
assert all(x['before']==x['after'] for x in unchanged_hashes.values())
cat_path=R/'authored'/f'{STEM}.catalog-compact.json'
with cat_path.open('x') as f:json.dump(new,f,ensure_ascii=False,sort_keys=True,separators=(',',':'));f.write('\n')
# Raw formatted spec blocks also remain exact in this same-format standalone file.
def raw_spec_blocks(raw):
 text=raw.decode();decoder=json.JSONDecoder();result={};i=1
 while True:
  while text[i].isspace() or text[i]==',':i+=1
  if text[i]=='}':break
  key,j=decoder.raw_decode(text,i);i=j
  while text[i].isspace() or text[i]==':':i+=1
  _,j=decoder.raw_decode(text,i);result[key]=text[i:j].encode();i=j
 return result
raw_before=raw_spec_blocks(base_raw);raw_after=raw_spec_blocks(cat_path.read_bytes())
assert all(raw_before[k]==raw_after[k] for k in unchanged)
report=dict(schema='photo-worker-catalog149-v6-research-proposal/v1',task_name='/root/review_12250_13000',model='gpt-6.1-sol',reasoning_effort='high',status='research_proposal_only_root_selection_pending_not_FINAL_not_APPROVAL',base_catalog=artifact('CATALOG-FINAL-146-V5.json'),base_catalog_sha256=digest(base),proposed_count=149,proposed_catalog=artifact(f'authored/{STEM}.catalog-compact.json'),proposed_catalog_sha256=digest(new),new_slots=new_keys,changed_existing_specs=changed,body_pose_exact_changed_fields=changed_fields,exact_delta={k:dict(before=base.get(k),after=new[k]) for k in new_keys+changed},unchanged_existing_count=145,unchanged_existing_spec_hashes=unchanged_hashes,unchanged145_raw_formatted_fullspec_blocks_exact=True,relational_action_exact_unchanged=True,research_provenance=[artifact(mechanics_name),artifact('worker-notes/native-12250-taxonomy-mechanics-articulation-relational-20261015.json'),artifact(mass_name),artifact('worker-notes/native-12250-taxonomy-mass-20261015.json')],read_provenance=dict(new_full149_catalog_personal_read_claim=False,unchanged145='Exact original146V5 raw formatted fullspec blocks and canonical values/hashes mechanically reused; prior related-fullspec review provenance retained. No new145/149 personal wholecatalog read count.',new_or_changed_four_fullspecs='Entire mechanics/thickness/body_pose after and physical_mass fullspecs directly read in current bounded composition turn; immutable serialized four afters will be directly reread before the separate completion note.',prior_actual_source_witnesses='Original audit source/current5B/ownbinding/closure whole reads remain in immutable referenced audit artifacts; no new witness/source read count inferred from composition.',prepared_bulk=[9350,9400],frozen_bulk_prefix=[9250,9355],cumulative_actual_bulk_read=105,unread_prepared_bulk=[9355,9400]),structural_checks=dict(count149=True,exact3additions=True,only4body_pose_fields_changed=True,all149_exact_field_shape_and_typed_lists=True,known_dimensions_owners_corefields_roles_priorities=True,no_duplicate_list_entries=True,all_neighbors_exist_no_self_neighbors=True,all145_existing_rawblocks_and_canonical_bytes_equal=True),technical_prefix_overlap_check=dict(method='Literal pairwise startswith comparison for3new role prefixes versus all149 role prefixes; no property aliases, role inference or change to broad existingprefixes.',overlaps=overlap,semantic_boundary='A technical prefix overlap alone never authorizes both roles. Surface_material covers declared material identity/optical response; mechanics covers explicit constitutive response; thickness covers explicit material-layer/cross-section thickness; physical_mass covers explicit carrier mass/physical heaviness. Same carrier alone is not a second fact. No material-name/shape/optical/style/mood-to-mechanics/thickness/mass inference.',limits='This is a structural and bounded manual semantic review, not exhaustive automatic semantic conflict detection, runtime validator integration, all-candidate tagging or numeric/comparison witness qualification.'),guard_and_mode_boundary='Actual carrier/part ownership, P/PR/E modes, selected operations, receiver/endpoint independence and original AND/OR/optional/adult/human/domain/lock guards remain source-specific mandatory checks. Role additions create no entity, new anatomy, mass change, measurement verification or automatic role union. Preserve actual qualitative source properties without requiring a number.',new_native_signature_count=0,candidate_tag_approval_count=0,catalog_approval=None,production_source_binding_proof_status_git_changes=0,network_calls=0,model_provider_calls=0,fixed_generation_boundary='No runtime modules imported for this stdlib-only catalog composition. Bulk prototype remains frozenGEN188c semantic6833; no working/native modules used for signing.',start=datetime.datetime.now(datetime.timezone.utc).isoformat(),full_serialized_after_reread_pending=True)
path=R/'authored'/f'{STEM}.json'
with path.open('x') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
assert base_path.read_bytes()==base_raw
print(json.dumps(dict(path=str(path),proposal_sha256=digest(report),catalog_sha256=digest(new),count=len(new),prefix_overlaps=overlap),ensure_ascii=False))
print('FULL_AFTER_FOUR')
print(json.dumps({k:new[k] for k in new_keys+changed},ensure_ascii=False,indent=2))
