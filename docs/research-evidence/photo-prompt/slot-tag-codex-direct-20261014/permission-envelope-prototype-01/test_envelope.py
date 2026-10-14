"""Tests of explicit synthetic expectations, not mirrored semantic classifiers."""
import copy
import json
import unittest
from dataclasses import replace
from envelope import compare, bind_source, source_binding, digest, IndependentPins, BoundSource, anchors_from_core
from fixtures import make, repin, refresh, PRIMITIVES, CID, EREFS, full_source_context, contract

CASES=[]

def run(f):
 return compare(f['bound'],core=f['core'],resolved_view=f['view'],inventory=f['inventory'],assessment=f['assessment'],expected=f['pins'],primitives=PRIMITIVES)


def expectation(name, f, allowed):
 before=digest({k:v for k,v in f.items() if k not in ['bound','pins']})
 try:r=run(f);actual=r['permission_only_pass'];reason=r['reasons']
 except ValueError as exc:r=None;actual=False;reason=[str(exc)]
 CASES.append({'name':name,'expected_permission_only':allowed,'actual_permission_only':actual,'reasons':reason,'passed':actual==allowed})
 assert actual==allowed,(name,reason)
 assert before==digest({k:v for k,v in f.items() if k not in ['bound','pins']}), 'pure input mutation'
 return r


def trusted_review_refresh(f):
 # A test-author independent review update; not a candidate-controlled production API.
 f['assessment']['inventory_sha256']=digest(f['inventory']);f['assessment']['resolved_view_sha256']=digest(f['view'])
 repin(f,inventory=True,assessment=True)


class EnvelopeTests(unittest.TestCase):
 def test_01_controlled_baselines_original3_unchanged(self):
  for same in [False,True]:
   f=make(same=same);r=expectation('baseline_same_'+str(same),f,True)
   self.assertEqual(len(r['original_expanded_effects']),3)
   self.assertEqual({e['fact_id'] for e in r['original_expanded_effects']},set(EREFS))
   self.assertEqual(r['original_permission_scope'],f['view']['permission_scope'])
   self.assertFalse(r['native_qualified']);self.assertFalse(r['consumer_integrated'])
   for e in r['original_expanded_effects']:
    if e['fact_id']!='exchangeApp':self.assertEqual(e['canonical_receivers'],sorted(['F1_alt' if x=='F1' else x for x in f['inventory']['scope_members']['framing_affected']]))
   self.assertEqual(len(r['preservation_obligations']),1)

 def test_02_all_original_target_receivers_cannot_be_waived(self):
  for same in [False,True]:
   base=make(same=same)
   for a in base['view']['permission_scope']['properties']:
    f=make(same=same,anchor=a,impacts={k:'disjoint' for k in EREFS})
    r=expectation('original_lock_'+str(same)+'_'+a['target']+'_'+a['property'],f,False)
    self.assertIn('original target/Rx property lock',r['reasons'])

 def test_03_cross_dimension_original_property(self):
  f=make(anchor={'dimension':'appearance','target':'H3','property':'framing.coverage'},impacts={k:'disjoint' for k in EREFS})
  r=expectation('original_property_other_dimension',f,False);self.assertIn('original target/Rx property lock',r['reasons'])

 def test_04_alias_original_lock(self):
  f=make(anchor={'dimension':'framing','target':'F1_alt','property':'framing.coverage'},impacts={k:'disjoint' for k in EREFS})
  r=expectation('actual_alias_lock',f,False);self.assertIn('original target/Rx property lock',r['reasons'])

 def test_05_ancestor_lock(self):
  # Exchange addresses hands/item, not carrier U, yet the explicitly owned hand reaches ancestor protection.
  f=make(anchor={'dimension':'action','target':'U','property':'action.interaction.exchange'},impacts={k:'disjoint' for k in EREFS})
  r=expectation('actual_part_ancestor_lock',f,False);self.assertIn('original target/Rx property lock',r['reasons'])

 def test_06_visible_body_and_inclusion_counterexamples(self):
  for same in [False,True]:
   for target,prop,dim in [('F1','subject.visibility','framing'),('F2','body.framing','framing'),('R1','framing.inclusion','framing'),('U','subject.visibility','framing'),('R2','subject.visibility','appearance'),('F1_alt','subject.visibility','appearance')]:
    f=make(same=same,anchor={'dimension':dim,'target':target,'property':prop,'reason':'The explicit selected crop excludes this currently included participant anatomy or carrier coverage.'},impacts={'macroApp':'affects','coverageApp':'affects','exchangeApp':'disjoint'})
    self.assertTrue(PRIMITIVES['property_effects_allowed'](f['core']['intent_lock'],f['view']['permission_scope']['dimensions'],f['view']['permission_scope']['literal_properties'],owner_graph=f['view']['permission_scope']['owner_graph']))
    r=expectation('envelope_gap_'+str(same)+'_'+target+'_'+prop+'_'+dim,f,False)
    self.assertTrue(r['additional_anchor_comparisons'])

 def test_07_whole_dimensions(self):
  for dim in ['framing','action']:
   f=make(anchor={'kind':'whole_dimension','dimension':dim},impacts={k:'disjoint' for k in EREFS})
   r=expectation('whole_'+dim,f,False);self.assertIn('original whole-dimension lock',r['reasons'])

 def test_08_other_dimension_whole_semantic_influence(self):
  f=make(anchor={'kind':'whole_dimension','dimension':'appearance'})
  key=digest({'kind':'whole_dimension','dimension':'appearance','target':'*','property':None})
  for d in f['assessment']['anchors']:
   if d['anchor_key']==key:d.update(impact='affects',reason='Independent manual review says selected crop changes a protected appearance scope despite its framing carrier dimension.')
  repin(f,assessment=True);expectation('other_whole_dim_manual_impact',f,False)

 def test_09_unrelated_explicit_disjoint_control(self):
  for same in [False,True]:
   f=make(same=same,anchor={'dimension':'appearance','target':'Z','property':'subject.visibility','reason':'Z is the separately declared preserved background object; same input explicitly keeps it visible and disjoint from every affected owner.'},impacts={k:'disjoint' for k in EREFS})
   expectation('unrelated_explicit_disjoint_'+str(same),f,True)

 def test_10_unknown_custom_property(self):
  f=make(anchor={'dimension':'appearance','target':'F1','property':'custom.face.safe_crop','reason':'No independently reviewed semantics for this custom protected address.'},impacts={k:'unknown' for k in EREFS})
  expectation('custom_unknown_failclosed',f,False)

 def test_11_no_substring_alias(self):
  f=make(anchor={'dimension':'appearance','target':'Z','property':'not_subject.visibility_copy','reason':'This explicitly unrelated Z metadata-like visual address is independently reviewed disjoint; spelling is not an alias.'},impacts={k:'disjoint' for k in EREFS})
  expectation('substring_not_global_alias',f,True)

 def test_12_missing_anchor_pair(self):
  f=make();f['assessment']['anchors'].pop();repin(f,assessment=True);expectation('missing_pair_even_rehashed',f,False)

 def test_13_duplicate_anchor_pair(self):
  f=make();f['assessment']['anchors'].append(copy.deepcopy(f['assessment']['anchors'][0]));repin(f,assessment=True);expectation('duplicate_pair',f,False)

 def test_14_no_semantic_reason(self):
  f=make();f['assessment']['anchors'][0]['reason']='';repin(f,assessment=True);expectation('empty_manual_reason',f,False)

 def test_15_missing_input_evidence(self):
  f=make();f['assessment']['anchors'][0]['input_ids']=[];repin(f,assessment=True);expectation('missing_actual_input_evidence',f,False)

 def test_16_inventory_missing_anchor(self):
  f=make();f['inventory']['anchors'].pop();trusted_review_refresh(f);expectation('missing_whole_or_anchor',f,False)

 def test_17_incomplete_unknown_unreviewed(self):
  for key,value in [('complete',False),('state','unknown'),('phase','after_discovery'),('reviewer',''),('reviewed_input_ids',[]),('reviewed_span_ids',[])]:
   f=make();f['inventory'][key]=value;trusted_review_refresh(f);expectation('inventory_'+key,f,False)

 def test_18_missing_actual_owner_even_new_hash(self):
  f=make();f['inventory']['owners'].remove('F2');trusted_review_refresh(f);expectation('fresh_hash_missing_F2_owner',f,False)

 def test_19_missing_actual_last_hand(self):
  f=make();f['inventory']['scope_members']['other_hands'].remove('H3');trusted_review_refresh(f);expectation('fresh_hash_missing_last_hand',f,False)

 def test_20_missing_actual_region(self):
  f=make();f['inventory']['scope_members']['framing_affected'].remove('F2');trusted_review_refresh(f);expectation('fresh_hash_missing_region_same_B1',f,False)

 def test_21_self_rehashed_complete_omission_vs_independent_root(self):
  f=make();oldpins=f['pins']
  for a in f['core']['semantic_assertions']:
   if a['axes'].get('scope_id')=='framing_affected':
    inv=json.loads(a['axes']['inventory']);inv['members']=[v for v in inv['members'] if v['owner_id']!='F2'];a['axes']['inventory']=json.dumps(inv,ensure_ascii=False,sort_keys=True,separators=(',',':'))
  # B1 can structurally resolve a freshly hashed but semantically false complete list.
  f['view']=refresh(f['core'],f['projection']);f['inventory'].update(core_sha256=f['core']['canonical_sha256'],core_payload_sha256=digest(f['core']))
  f['inventory']['scope_members']['framing_affected'].remove('F2');f['assessment']['inventory_sha256']=digest(f['inventory']);f['assessment']['resolved_view_sha256']=digest(f['view'])
  f['pins']=IndependentPins(oldpins.source_bindings,digest(f['view']),oldpins.inventory_sha256,digest(f['assessment']))
  expectation('fresh_B1_hash_false_complete_vs_independent_inventory',f,False)

 def test_22_stale_inventory_hash(self):
  f=make();f['inventory']['reason']+=' candidate rewrite';expectation('candidate_self_hash_not_authority',f,False)

 def test_23_stale_view_pin(self):
  f=make();f['pins']=replace(f['pins'],resolved_view_sha256='0'*64);expectation('stale_B1_view_pin',f,False)

 def test_24_stale_core_input_topology(self):
  for key in ['core_sha256','core_payload_sha256','topology_sha256']:
   f=make();f['inventory'][key]='0'*64;trusted_review_refresh(f);expectation('stale_'+key,f,False)
  f=make();f['inventory']['input_binding']['request_sha256']='0'*64;trusted_review_refresh(f);expectation('stale_request_hash',f,False)

 def test_25_PR_missing_or_wrong(self):
  for change in ['missing','target','image','property','value','frozen','assertion_id']:
   f=make();ws=f['inventory']['witnesses']
   if change=='missing':ws.clear()
   elif change=='value':ws[0]['value']={'type':'subject.visibility/v1','value':'hidden'}
   elif change=='frozen':ws[0]['frozen']=False
   else:ws[0][change]={'target':'H1','image':'OtherImage','property':'entity.presence','assertion_id':'presence4'}[change]
   trusted_review_refresh(f);expectation('item_visibility_PR_'+change,f,False)

 def test_26_presence_cannot_proxy_visibility(self):
  f=make();v=f['inventory']['witnesses'][0];v.update(property='entity.presence',dimension='subject',value={'type':'entity.presence/v1','value':'present'},assertion_id='presence4');trusted_review_refresh(f);expectation('presence_not_same_image_visibility',f,False)

 def test_27_item_same_other_image(self):
  f=make();f['inventory']['witnesses'][0]['image']='I2';trusted_review_refresh(f);expectation('same_item_other_image_not_PR',f,False)

 def test_28_native_visibility_fact_missing(self):
  f=make();f['core']['semantic_assertions']=[a for a in f['core']['semantic_assertions'] if a['assertion_id']!='item_visible'];f['view']=refresh(f['core'],f['projection']);f['inventory'].update(core_sha256=f['core']['canonical_sha256'],core_payload_sha256=digest(f['core']));f['assessment']['resolved_view_sha256']=digest(f['view']);repin(f,view=True);trusted_review_refresh(f);expectation('core_missing_actual_visibility_witness',f,False)

 def test_29_desired_framing_P_forbidden(self):
  ctx=full_source_context();e=next(f for f in ctx['facts'] if f['id']=='coverageApp');p={k:v for k,v in e.items() if k not in ['operation','receivers']};p.update(id='desiredFramingP',mode='prerequisite');ctx['facts'].append(p)
  with self.assertRaisesRegex(ValueError,'pre-frozen'):bind_source(ctx,contract(ctx))
  CASES.append({'name':'desired_framing_P','expected_rejection':'bind_source','passed':True})

 def test_30_source_authority_forgery_and_guard_drop(self):
  for change in ['property','target','value','operation','receivers','conditions','ordinaryunit','closure']:
   f=make();ctx=copy.deepcopy(f['contexts'][0])
   if change=='conditions':ctx['source_record']['conditions']={}
   elif change=='closure':ctx['closure_snapshot']['guards']={}
   elif change=='ordinaryunit':ctx['source_units'][0]['quote']='Macro'
   else:
    e=next(q for q in ctx['facts'] if q['id']=='macroApp')
    if change=='value':e['value']={'type':'shot.scale/v1','value':'wide'}
    elif change=='receivers':e['receivers']=[]
    elif change=='operation':e['operation']='relocate'
    elif change=='target':e['target']='exchange_item'
    elif change=='property':e['property']='image.shot.scale'
   try:f['bound'][0]=bind_source(ctx,contract(ctx))
   except ValueError as exc:CASES.append({'name':'forged_source_'+change,'expected_rejection':'bind_source','reason':str(exc),'passed':True});continue
   expectation('self_rehashed_source_not_independent_'+change,f,False)

 def test_31_context_object_alteration(self):
  f=make();p=json.loads(f['bound'][0].payload);p['context']['source_record']['content']['en']='forged';f['bound'][0]=BoundSource(json.dumps(p).encode());expectation('freely_constructed_BoundSource_not_authority',f,False)

 def test_32_missing_full_source_authority(self):
  f=make();f['pins']=replace(f['pins'],source_bindings={});expectation('no_independent_source_authority',f,False)

 def test_33_receiver_union_cannot_shrink(self):
  f=make();e=next(q for q in f['view']['nodes'][0]['expanded_facts'] if q['fact_id']=='coverageApp');e['canonical_receivers'].remove('F2');f['view']['canonical_sha256']=digest({k:v for k,v in f['view'].items() if k!='canonical_sha256'});repin(f,view=True);f['assessment']['resolved_view_sha256']=digest(f['view']);repin(f,assessment=True);expectation('fake_B1_Rx_shrink',f,False)

 def test_34_original_permission_scope_cannot_shrink(self):
  f=make();f['view']['permission_scope']['properties'].pop();f['view']['canonical_sha256']=digest({k:v for k,v in f['view'].items() if k!='canonical_sha256'});repin(f,view=True);f['assessment']['resolved_view_sha256']=digest(f['view']);repin(f,assessment=True);expectation('original_scope_union_removed',f,False)

 def test_35_unknown_joint_conflict(self):
  f=make(joint={'target':'F1','property':'subject.visibility'},joint_impact='unknown');expectation('joint_visibility_unknown',f,False)

 def test_36_actual_joint_influence(self):
  f=make(joint={'target':'F1','property':'subject.visibility'},joint_impact='affects');expectation('joint_visibility_affects',f,False)

 def test_37_joint_disjoint_control(self):
  f=make(joint={'target':'Z','property':'subject.visibility'},joint_impact='disjoint');expectation('joint_explicitly_unrelated_Z',f,True)

 def test_38_missing_joint_review(self):
  f=make(joint={'target':'F1','property':'subject.visibility'},joint_impact='disjoint');f['assessment']['joint'].pop();repin(f,assessment=True);expectation('missing_actual_joint_pair',f,False)

 def test_39_joint_E_receiver_influence(self):
  f=make(joint={'target':'Z','property':'subject.visibility','receiver':'F1'},joint_impact='affects');expectation('joint_other_E_all_Rx_review',f,False)

 def test_40_B1_original_conflict_not_waived(self):
  with self.assertRaisesRegex(ValueError,'conflicting joint'):
   make(joint={'target':'I','property':'shot.scale','value':'wide'},joint_impact='disjoint')
  CASES.append({'name':'B1_original_joint_conflict','expected_rejection':'actual frozen B1','passed':True})

 def test_41_missing_joint_source_authority(self):
  f=make(joint={'target':'Z','property':'subject.visibility'},joint_impact='disjoint');f['pins']=replace(f['pins'],source_bindings={CID:f['pins'].source_bindings[CID]});expectation('joint_other_source_missing_full_authority',f,False)

 def test_42_empty_scope_branch(self):
  f=make();f['inventory']['scope_members']['other_hands']=[];trusted_review_refresh(f);expectation('empty_actual_other_hand_scope',f,False)

 def test_43_bounded_sources(self):
  f=make();f['bound']*=9;expectation('source_node_cap',f,False)

 def test_44_bounded_owners(self):
  f=make();f['inventory']['owners']=['owner'+str(i) for i in range(65)];trusted_review_refresh(f);expectation('owner_cap',f,False)

 def test_45_bounded_anchors(self):
  core=make()['core'];core['intent_lock']['semantic_anchors']=[{'dimension':'framing','target':'F1','property':'explicit.protected.'+str(i)} for i in range(129)]
  with self.assertRaisesRegex(ValueError,'bounded'):anchors_from_core(core)
  CASES.append({'name':'anchor_cap','expected_rejection':'bounded exact lock inventory','passed':True})

 def test_46_bounded_effects(self):
  ctx=full_source_context();c=contract(ctx);ctx['canonical_effect_refs']=['effect'+str(i) for i in range(33)]
  with self.assertRaisesRegex(ValueError,'bounded'):bind_source(ctx,c)
  CASES.append({'name':'effect_cap','expected_rejection':'source binder cap','passed':True})

 def test_47_unknown_fields_no_guard_waiver(self):
  f=make();f['inventory']['waive_guards']=True;trusted_review_refresh(f);expectation('guard_waive_key_forbidden',f,False)

 def test_48_stale_manual_review_source_binding(self):
  f=make();f['assessment']['source_bindings_sha256']='0'*64;repin(f,assessment=True);expectation('manual_source_binding_stale',f,False)

 def test_49_finite_JSON(self):
  f=make();f['assessment']['anchors'][0]['reason']=float('nan');
  with self.assertRaises(ValueError):run(f)
  CASES.append({'name':'nonfinite_JSON','expected_rejection':'finite JSON','passed':True})

 def test_50_extra_shadow_effect(self):
  f=make();ctx=copy.deepcopy(f['contexts'][0]);e=copy.deepcopy(next(q for q in ctx['facts'] if q['id']=='coverageApp'));e.update(id='fakeVisibilityE',property='subject.visibility',target='initiating_hand');e['value']={'type':'subject.visibility/v1','value':'visible'};ctx['facts'].append(e)
  with self.assertRaisesRegex(ValueError,'extra'):bind_source(ctx,contract(ctx))
  CASES.append({'name':'fake_extra_visibility_E','expected_rejection':'not original E set','passed':True})

 def test_51_literal_union_cannot_shrink_even_rehashed(self):
  f=make();v=f['view'];v['permission_scope']['literal_properties'].pop();v['permission_scope_sha256']=digest(v['permission_scope']);v['canonical_sha256']=digest({k:x for k,x in v.items() if k!='canonical_sha256'});repin(f,view=True);f['assessment']['resolved_view_sha256']=digest(v);repin(f,assessment=True)
  expectation('literal_union_removed_rehashed',f,False)

 def test_52_different_region_cannot_borrow_item_PR(self):
  f=make(anchor={'dimension':'framing','target':'F1','property':'subject.visibility','reason':'The face is cropped, and item PR cannot preserve this other owner.'},impacts={k:'disjoint' for k in EREFS})
  lock=digest({'kind':'property','dimension':'framing','target':'F1','property':'subject.visibility'})
  for d in f['assessment']['anchors']:
   if d['anchor_key']==lock:d['preservation_ref']='itemVisiblePreservation'
  repin(f,assessment=True);expectation('borrow_item_PR_for_face_forbidden',f,False)

 def test_53_parent_child_property_paths(self):
  for prop in ['shot','shot.scale.detail','shot.*']:
   f=make(anchor={'dimension':'framing','target':'I','property':prop},impacts={k:'disjoint' for k in EREFS})
   expectation('original_parent_child_'+prop,f,False)

 def test_54_no_missing_ordinary_positive_unit(self):
  ctx=full_source_context();ctx['source_units']=[u for u in ctx['source_units'] if u['pointer']!='/content/ko']
  with self.assertRaisesRegex(ValueError,'full positive'):bind_source(ctx,contract(ctx))
  CASES.append({'name':'missing_full_KO_ordinary_unit','expected_rejection':'full positive unit inventory','passed':True})

 def test_55_bounded_total_source_anchor_joint_pairs(self):
  from fixtures import native,core_pin
  f=make();contexts=f['contexts'];projection=f['projection']
  # Seven independent controlled sources each explicitly select four local states
  # on existing Z; root1299 original3 E are untouched. No real semantic approval.
  for i in range(7):
   cid='cand_'+format(100+i,'032x');phrase='On independently existing Z select '+', '.join('controlled.state_'+str(i)+'_'+str(j)+'=selected' for j in range(4))+'.'
   pf={'id':'present','realization_id':'base','pointer':'/content/en','quote':'independently existing Z','mode':'prerequisite','dimension':'subject','target':'z','property':'entity.presence','value':{'type':'entity.presence/v1','value':'present'},'requires':[]}
   es=[{'id':'e'+str(j),'realization_id':'base','pointer':'/content/en','quote':'controlled.state_'+str(i)+'_'+str(j)+'=selected','mode':'effect','operation':'set_value','dimension':'action','target':'z','property':'controlled.state_'+str(i)+'_'+str(j),'value':{'type':'controlled.state/v1','value':'selected'},'receivers':[],'requires':['present']} for j in range(4)]
   src={'id':cid,'conditions':{},'content':{'en':phrase},'effects':{'dimensions':['action'],'properties':[{'dimension':e['dimension'],'target':e['target'],'property':e['property']} for e in es]},'record_kind':'visual_option'}
   c={'candidate_id':cid,'realization_id':'base','source_snapshot_sha256':digest(src),'catalog_sha256':contexts[0]['catalog_sha256'],'source_record':src,'facts':[pf,*es],'source_units':[{'disposition':'semantic','realization_id':'base','pointer':'/content/en','quote':phrase,'fact_refs':['present',*[e['id'] for e in es]]}],'positive_fields':[{'realization_id':'base','pointer':'/content/en','text':phrase}],'ownbindings':{},'closure_snapshot':{'guards':{},'selected_rids':['base'],'profiles':{},'CID_closure':{},'binding_closure':{},'reference_sha256':{}},'canonical_effect_refs':[e['id'] for e in es],'required_preservation_refs':[]};contexts.append(c)
   projection['nodes'].append({'candidate_id':cid,'realization_id':'base','meaning_sha256':digest(src),'qualification_sha256':digest({'synthetic_not_qualified':src}),'projection_sha256':'0'*64,'facts':[{k:v for k,v in e.items() if k not in ['pointer','quote']} for e in [pf,*es]],'bindings':[{'target':'z','origin':'existing','selection':{'kind':'selected_existing_owner','owner_id':'Z'}}],'guard_only_targets':[],'selected_children':[]});projection['roots'].append({'candidate_id':cid,'realization_id':'base'})
  # 6 whole locks + item anchor +121 explicitly enumerated protected paths =128.
  f['core']['intent_lock']['semantic_anchors'] += [{'dimension':'appearance','target':'Z','property':'controlled.protected_'+str(i)} for i in range(121)]
  f['view']=refresh(f['core'],projection);f['bound']=[bind_source(c,contract(c)) for c in contexts];v=f['view'];f['inventory'].update(core_sha256=f['core']['canonical_sha256'],core_payload_sha256=digest(f['core']),anchors=anchors_from_core(f['core']));pins={source_binding(b)['candidate_id']:source_binding(b) for b in f['bound']};f['assessment'].update(inventory_sha256=digest(f['inventory']),resolved_view_sha256=digest(v),source_bindings_sha256=digest(pins));f['pins']=IndependentPins(pins,digest(v),digest(f['inventory']),digest(f['assessment']))
  try:run(f)
  except ValueError as exc:self.assertIn('pair cap',str(exc))
  else:self.fail('31 E x128 anchors plus cross-source pairs must exceed cap')
  CASES.append({'name':'bounded_31E_128anchors_plus_joint_pairs','expected_rejection':'pair cap before enumeration','passed':True})


if __name__=='__main__':unittest.main(verbosity=2)
