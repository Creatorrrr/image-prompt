from pathlib import Path
import json,sys,unittest,hashlib
SKILL=Path(__file__).resolve().parents[1];sys.path.insert(0,str(SKILL/'scripts'))
# The maintained working tree dispatches managed dependencies from its sealed release.
if not (SKILL/'scripts/photo_recall_first.py').is_file():
 from photo_installed_h_f2 import release,default_store,read,CONFIG
 native,_,_=release(default_store(),read(SKILL/CONFIG)['generation_id'])
 sys.path.append(str(native/'scripts'))
import photo_h_f2_query_scope as q
from photo_h_f2_search import present_material
from photo_h_f2_event_phase import RECIPE as PHASE

class ProofAndNegativeScopeTests(unittest.TestCase):
 def test_mechanical_and_placement_proofs_match_across_process_hash_seeds(self):
  import os,subprocess
  code="""import sys,json;sys.path.insert(0,sys.argv[1])
import photo_h_f2_query_scope as q
from photo_h_f2_semantic_object_makeup_prop import Semantic
s=Semantic(q._focus_positive)
texts=[('object_structure','A camera lens barrel is attached by a bayonet connection to the same camera assembly.'),('prop_placement',"Photographic role: Put the notebook flat on the table on the reader's right, its spine parallel to the table edge.\\nScene context: An existing adult reader and notebook."),('prop_placement','Photographic role: Preserve the current position and orientation; do not hold or move the prop.\\nScene context: An existing adult and prop.')]
print(json.dumps([s.request(role,text) for role,text in texts],sort_keys=True,ensure_ascii=False))
"""
  outputs=[subprocess.check_output([sys.executable,'-c',code,str(Path(q.__file__).parent)],env=dict(os.environ,PYTHONHASHSEED=str(seed)),text=True) for seed in (1,17,73)]
  self.assertEqual(outputs[0],outputs[1]);self.assertEqual(outputs[1],outputs[2])
 def test_internal_age_relations_emit_round_trip_json_values(self):
  source='The existing adult has an older-looking face.'
  u={'pointer':'/content/en','text':source,'candidate_id':'independent','realization_id':'base','source_sha256':hashlib.sha256(source.encode()).hexdigest(),'literal_id':'u0'}
  effect={'dimensions':['appearance'],'properties':[{'dimension':'appearance','property':'age.presentation','target':'face'}]}
  contracts=q.compile_focus_contracts({'s':source},source_units=lambda _: [u],source_effects=lambda _: effect)
  _,trace=q.order_focus([{'id':'s'}],'Photographic role: Show the existing adult with an older-looking face.',contracts)
  self.assertIn('s',trace['supported_ids']);self.assertEqual(trace,json.loads(json.dumps(trace)))
 def test_legacy_adult_context_flag_cannot_be_supplied_by_rank(self):
  self.assertFalse(q._minimum_declared_guards('Photographic role: Preserve the person’s supplied birthplace.',{'source_conditions':{'requires_adult_context':True}}))
  self.assertTrue(q._minimum_declared_guards('Photographic role: Preserve the existing adult’s supplied birthplace.',{'source_conditions':{'requires_adult_context':True}}))
 def test_negative_domain_without_positive_change_never_pads_unknown_material(self):
  text='Photographic role: Keep the iris color unspecified; do not change it.'
  _,trace=q.order_focus([{'id':'unknown'}],text,{})
  self.assertIn('eye_detail',trace['request']['strict_nonpositive_roles'])
  rows,projection=present_material([{'id':'unknown'}],{'schema':PHASE},focus=trace)
  self.assertEqual(rows,[]);self.assertFalse(projection['unknown_source_padding'])
 def test_carried_physical_text_retains_priority_over_quoted_temperature(self):
  text='Photographic role: Show “HOT” only as printed sign lettering; no physical temperature is supplied.'
  _,trace=q.order_focus([{'id':'text'}],text,{})
  rows,_=present_material([{'id':'text'}],{'schema':PHASE},focus=trace,literal={'schema':'photo-h-f2-primary-carried-literal/v3','request':{'mode':'physical'},'compatible':{'text':{}},'conflicting':{}})
  self.assertEqual(rows,[{'id':'text'}])
 def test_ordinary_unsupported_blush_is_not_a_negative_change_request(self):
  req=q.focus_request('Photographic role: Surface cosmetic pigment or blush applied to cheek skin.')
  self.assertFalse((req or {}).get('strict_nonpositive_roles'))
 def test_scene_explicit_absence_is_a_scope_constraint(self):
  req=q.focus_request('Photographic role: Record the open umbrella.\nScene context: No construction detail is requested.')
  self.assertIn('object_structure',req['strict_nonpositive_roles'])
 def test_local_korean_conversion_denial_retains_declared_adult(self):
  text='성인 기술자의 제공된 거주 이력을 외모로 바꾸지 않고 그대로 유지한다.'
  self.assertTrue(q._minimum_declared_guards(text,{'source_conditions':{'requires_adult_context':True}}))
 def test_local_korean_invention_denial_retains_declared_adult(self):
  text='성인 피사체의 명시된 언어 이력을 조상을 만들어내지 않고 보존한다.'
  self.assertTrue(q._minimum_declared_guards(text,{'source_conditions':{'requires_adult_context':True}}))
 def test_unmodeled_physical_placement_cannot_shadow_frame_triangle(self):
  req=q.focus_request('Photographic role: Arrange three existing pebbles as a stable triangle inside the image frame.\nScene context: Three pebbles on the ground.')
  self.assertEqual(req['role'],'composition')
 def test_nonmutating_profile_primary_can_exclude_but_never_promote(self):
  source='The human iris has green color and radial streaks.'
  u={'pointer':'/content/en','text':source,'candidate_id':'independent','realization_id':'base','source_sha256':hashlib.sha256(source.encode()).hexdigest(),'literal_id':'u0'}
  contracts=q.compile_focus_contracts({'s':source},source_units=lambda _: [u],source_effects=lambda _: {'dimensions':[],'properties':[]})
  self.assertFalse(contracts['s']['eye_detail']['positive_support_eligible'])
  _,trace=q.order_focus([{'id':'s'}],'Photographic role: Show the human green iris with radial streaks.',contracts)
  self.assertNotIn('s',trace['supported_ids'])
 def test_unmodeled_concrete_restriction_does_not_pad_unknown_material(self):
  text='Photographic role: Show the existing ewer but do not infer its unprovided maker.'
  _,trace=q.order_focus([{'id':'unknown'}],text,{})
  self.assertIn('unmodeled_restricted_change',trace['request']['strict_nonpositive_roles'])
  rows,_=present_material([{'id':'unknown'}],{'schema':PHASE},focus=trace)
  self.assertEqual(rows,[])
 def test_taxonomy_without_instantiated_scene_keeps_ordinary_discovery(self):
  req=q.focus_request('Photographic role: A declared actor performs a concrete activity without changing its identity.')
  self.assertFalse((req or {}).get('strict_nonpositive_roles'))
 def test_korean_without_additions_never_pads_unknown_animal_material(self):
  text='Photographic role: 성인 연기자를 동물 신체 추가 없이 인간으로 유지한다.\nScene context: 기존 성인 연기자가 연습실에 있다.'
  _,trace=q.order_focus([{'id':'unknown'}],text,{})
  rows,_=present_material([{'id':'unknown'}],{'schema':PHASE},focus=trace)
  self.assertEqual(rows,[])
 def test_equal_visual_prominence_cannot_create_a_priority_tier(self):
  text='Photographic role: Give the two glass jars equal image prominence.\nScene context: Two existing jars stand together.'
  _,trace=q.order_focus([{'id':'unknown'}],text,{})
  self.assertIn('visual_hierarchy',trace['request']['strict_nonpositive_roles'])
  rows,_=present_material([{'id':'unknown'}],{'schema':PHASE},focus=trace)
  self.assertEqual(rows,[])
if __name__=='__main__':unittest.main()
