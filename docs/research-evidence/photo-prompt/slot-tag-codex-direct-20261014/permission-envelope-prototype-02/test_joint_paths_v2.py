"""Independent regression cases for the actual joint property-path hole.

No source truth/native qualification is manufactured. Synthetic comparison-only
wildcard cases are explicitly separate from B1's actual fact property grammar.
"""
import copy,unittest
from envelope import compare,joint_properties_allowed,digest
from fixtures import make,PRIMITIVES,EREFS

CASES=[]
def run(f):
 before=digest({k:v for k,v in f.items()if k not in ['bound','pins']})
 r=compare(f['bound'],core=f['core'],resolved_view=f['view'],inventory=f['inventory'],assessment=f['assessment'],expected=f['pins'],primitives=PRIMITIVES)
 assert digest({k:v for k,v in f.items()if k not in ['bound','pins']})==before
 assert r['original_permission_scope']==f['view']['permission_scope']
 assert r['original_expanded_effects']==[e for n in f['view']['nodes']for e in n['expanded_facts']if e['mode']=='effect']
 assert {e['fact_id']for e in r['original_expanded_effects']if e['candidate_id']==f['contexts'][0]['candidate_id']}==set(EREFS)
 assert not r['native_qualified'] and not r['consumer_integrated']
 return r
def check(name,f,expected):
 r=run(f);CASES.append({'name':name,'expected':expected,'actual':r['permission_only_pass'],'reasons':r['reasons'],'unchanged_original_E_Rx':True,'stage':'actual_frozen_B1_plus_permission_only'})
 assert r['permission_only_pass']==expected,(name,r['reasons'])
 return r
def local(prop,target,rx=(),dim='framing'):
 return {'dimension':dim,'property':prop,'target':{'canonical_owner_id':target},'canonical_receivers':list(rx)}

class JointPathTests(unittest.TestCase):
 def test_01_eight_actual_regressions_each_topology(self):
  for same in [False,True]:
   for name,target,prop,receiver in [
    ('parent_shot','I','shot',None),('child_shot','I','shot.scale.detail',None),
    ('parent_framing','I','framing',None),('child_coverage','I','framing.coverage.detail',None),
    ('item_action_parent','X','action.interaction',None),('face_alias','F1_alt','framing',None),
    ('hand_carrier_ancestor','U','action.interaction',None),('other_receiver','Z','framing','F1')]:
    f=make(same=same,joint={'target':target,'property':prop,'value':'independent_selected_state',**({'receiver':receiver}if receiver else{})},joint_impact='disjoint')
    r=check(name+'_'+str(same),f,False);self.assertIn('actual joint property-path overlap',r['reasons'])

 def test_02_related_owner_unrelated_property_controls(self):
  for same in [False,True]:
   for name,target,prop in [('same_image_unrelated','I','custom.unrelated_palette'),('related_carrier_unrelated','U','custom.surface_finish'),('disjoint_Z_parent','Z','shot'),('substring_not_alias','I','not_shot.scale_copy'),('sibling_not_parent','I','shot.scale_copy')]:
    check(name+'_'+str(same),make(same=same,joint={'target':target,'property':prop,'value':'independent_selected_state'},joint_impact='disjoint'),True)

 def test_03_cross_dimension_path_overlap(self):
  for target,prop in [('I','shot'),('F1_alt','framing'),('U','action.interaction')]:
   check('actual_cross_dimension_'+target,make(joint={'target':target,'property':prop,'dimension':'action','value':'independent_selected_state'},joint_impact='disjoint'),False)

 def test_04_unknown_manual_semantics_still_failclosed(self):
  for target,prop in [('Z','custom.unrelated_palette'),('I','not_shot.scale_copy')]:
   check('unreviewed_joint_'+target,make(joint={'target':target,'property':prop,'value':'independent_selected_state'},joint_impact='unknown'),False)

 def test_05_exact_parent_child_wildcards_use_frozen_primitive(self):
  graph=make()['view']['permission_scope']['owner_graph']
  pairs=[('shot.scale','shot'),('shot','shot.scale'),('shot.scale','shot.scale.detail'),('shot.scale.detail','shot.scale'),('shot.*','shot.scale'),('shot.scale','shot.*'),('*','shot.scale'),('shot.scale','*'),('shot.s*','shot.scale'),('framing.coverage','framing.*')]
  for a,b in pairs:
   for left,right in [(local(a,'I'),local(b,'I')),(local(a,'H1'),local(b,'U')),(local(a,'F1'),local(b,'F1_alt')),(local(a,'Z',['H1']),local(b,'U'))]:
    ok=joint_properties_allowed(left,right,owner_graph=graph,property_primitive=PRIMITIVES['property_effects_allowed']);CASES.append({'name':'comparison_only_'+a+'_'+b+'_'+left['target']['canonical_owner_id']+'_'+right['target']['canonical_owner_id'],'expected':False,'actual':ok,'stage':'direct_permission_comparison_not_B1_wildcard_E'});self.assertFalse(ok)

 def test_06_comparison_properties_are_not_substring_aliases(self):
  graph=make()['view']['permission_scope']['owner_graph']
  for a,b in [('shot.scale','not_shot.scale_copy'),('shot.scale','shot.scale_copy'),('framing.coverage','framing.coverage_copy')]:
   ok=joint_properties_allowed(local(a,'I'),local(b,'I'),owner_graph=graph,property_primitive=PRIMITIVES['property_effects_allowed']);CASES.append({'name':'no_substring_'+b,'expected':True,'actual':ok,'stage':'direct_permission_comparison'});self.assertTrue(ok)

 def test_07_unknown_owner_separation_failsclosed(self):
  graph=copy.deepcopy(make()['view']['permission_scope']['owner_graph']);graph['owners']['W']='entity'
  ok=joint_properties_allowed(local('shot.scale','I'),local('shot','W'),owner_graph=graph,property_primitive=PRIMITIVES['property_effects_allowed']);CASES.append({'name':'independently_named_W_no_disjoint_proof','expected':False,'actual':ok,'stage':'direct_permission_comparison'});self.assertFalse(ok)

 def test_08_explicit_owner_disjointness_allows_same_path(self):
  graph=make()['view']['permission_scope']['owner_graph']
  for a,b in [('shot.scale','shot'),('shot.*','shot.scale'),('*','shot.scale')]:
   ok=joint_properties_allowed(local(a,'I'),local(b,'Z'),owner_graph=graph,property_primitive=PRIMITIVES['property_effects_allowed']);CASES.append({'name':'explicit_disjoint_'+a+'_'+b,'expected':True,'actual':ok,'stage':'direct_permission_comparison'});self.assertTrue(ok)

 def test_09_B1_wildcard_fact_grammar_not_relaxed(self):
  for prop in ['shot.*','framing.*','*']:
   with self.assertRaisesRegex(ValueError,'untyped selected fact'):
    make(joint={'target':'I','property':prop,'value':'independent_selected_state'},joint_impact='disjoint')
   CASES.append({'name':'B1_rejects_wildcard_fact_'+prop,'expected':'B1_reject','actual':'B1_reject','stage':'actual_frozen_B1_fact_grammar'})

if __name__=='__main__':unittest.main(verbosity=2)
