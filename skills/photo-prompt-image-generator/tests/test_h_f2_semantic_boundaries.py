"""Semantic boundaries exercised through the parent focus integration API.

Synthetic independent meanings only; no corpus IDs, saved queries or model calls.
"""
from pathlib import Path
import hashlib,importlib.util,json,sys,unittest
SKILL=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SKILL/'scripts'))
import photo_h_f2_query_scope as q

def request(focus,scene=''):
 return q.focus_request('Photographic role: '+focus+'\nScene context: '+scene)
def semantics(row):return (row or {}).get('all_semantics',{})
def source_unit(text):
 return {'pointer':'/content/en','text':text,'candidate_id':'independent-source','realization_id':'base','source_sha256':hashlib.sha256(text.encode()).hexdigest(),'literal_id':'u0'}
def camera_contracts(conditions):
 text='The taking camera has a horizontal optical axis and a level view.'
 effects={'dimensions':['camera'],'properties':[{'dimension':'camera','target':'taking_camera','property':'camera.direction.pitch'}]}
 return q.compile_focus_contracts({'s':text},source_units=lambda _: [source_unit(text)],source_effects=lambda _: effects,source_constraints=lambda _: {'source_conditions':conditions,'realization_conditions':{}})
def supported_camera(focus,conditions,scene=''):
 text='Photographic role: '+focus+'\nScene context: '+scene
 return q.order_focus([{'id':'s'}],text,camera_contracts(conditions))[1]

class ParentFocusIntegrationBoundaries(unittest.TestCase):
 def test_parent_and_helpers_use_same_skill_code(self):
  self.assertEqual(Path(q.__file__).resolve().parent,(SKILL/'scripts').resolve())
  for name,loaded in list(sys.modules.items()):
   if name.startswith('photo_h_f2_semantic_'):
    self.assertEqual(Path(loaded.__file__).resolve().parent,(SKILL/'scripts').resolve())
 def test_naked_quoted_hot_does_not_assert_temperature(self):
  self.assertNotIn('thermal_state',semantics(request('“HOT”')))
 def test_quoted_hot_working_title_does_not_assert_temperature(self):
  self.assertNotIn('thermal_state',semantics(request('Use “HOT” only as the quoted working title.')))
 def test_actual_temperature_is_retained(self):
  self.assertIn('thermal_state',semantics(request('The water physical temperature is 19 °C.')))
 def test_quote_before_actual_temperature_does_not_erase_actual(self):
  row=request('The quoted working title is “HOT”; the water physical temperature is 19 °C.')
  self.assertIn('thermal_state',semantics(row))
 def test_free_of_cosmetics_does_not_erase_later_camera_orientation(self):
  row=request('Keep the skin free of cosmetics; keep the taking camera level with a horizontal optical axis.')
  self.assertIn('camera_direction',semantics(row));self.assertNotIn('makeup_decoration',semantics(row))
 def test_without_cosmetics_does_not_erase_positive_camera_conjunct(self):
  row=request('Without cosmetic decoration, keep the taking camera horizontal.')
  self.assertIn('camera_direction',semantics(row));self.assertNotIn('makeup_decoration',semantics(row))
 def test_numeric_mass_remains_a_physical_declaration(self):
  row=request('The existing brass block has a declared physical mass of 3 kilograms.')
  self.assertIn('physical_mass',semantics(row))
  self.assertEqual(semantics(row)['physical_mass']['kind'],'numeric')
 def test_visual_mass_does_not_become_numeric_or_physical_mass(self):
  row=request('Balance the visually heavy bowl with open space across the photographic frame.')
  self.assertNotIn('physical_mass',semantics(row))
 def test_explicit_adult_guard_is_not_supplied_by_a_role_or_rank(self):
  trace=supported_camera('Keep the taking camera level with a horizontal optical axis.',{'requires_all_tags':['adult']})
  self.assertNotIn('s',trace['supported_ids'])
 def test_declared_adult_satisfies_only_that_minimum_guard(self):
  trace=supported_camera('Keep the taking camera level with a horizontal optical axis.',{'requires_all_tags':['adult']},'One existing adult is photographed.')
  self.assertIn('s',trace['supported_ids']);self.assertFalse(trace['native_approval'])
 def test_korean_adult_before_later_negation_survives(self):
  trace=supported_camera('성인이며 화장 장식은 추가하지 않는다. 촬영 카메라의 광축을 수평으로 유지한다.',{'requires_all_tags':['adult']})
  self.assertIn('s',trace['supported_ids'])
 def test_korean_adult_in_scene_before_later_negation_survives(self):
  trace=supported_camera('촬영 카메라의 광축을 수평으로 유지한다.',{'requires_all_tags':['adult']},'인물은 성인이며 연령을 추정하지 않는다.')
  self.assertIn('s',trace['supported_ids'])
 def test_quoted_adult_does_not_satisfy_a_source_guard(self):
  trace=supported_camera('Keep the taking camera level with a horizontal optical axis.',{'requires_all_tags':['adult']},'“adult” is a quoted series title.')
  self.assertNotIn('s',trace['supported_ids'])
 def test_bird_wing_joint_request_stays_anatomical(self):
  row=request("Show the bird's wing anatomical connection to its own shoulder and body.")
  self.assertIsNotNone(row);self.assertEqual(row['role'],'anatomical_connection')
 def test_explicit_species_features_are_species_markers(self):
  row=request('Show species-defining red crown feathers and a curved beak on the parrot itself.')
  self.assertIn('species_marker',semantics(row))
 def test_ordinary_cheek_blush_is_not_a_decorative_motif(self):
  self.assertNotIn('makeup_decoration',semantics(request('Use soft ordinary rosy cheek blush on the adult face.')))
 def test_explicit_cheek_cosmetic_motif_is_decoration(self):
  row=request('Paint a tiny blue temporary cosmetic star motif on the adult cheek skin.')
  self.assertIn('makeup_decoration',semantics(row))
 def test_blank_scene_does_not_break_positive_focus(self):
  self.assertIn('camera_direction',semantics(request('Keep the taking camera level with a horizontal optical axis.','')))
 def test_whitespace_scene_does_not_break_positive_focus(self):
  self.assertIn('camera_direction',semantics(request('Keep the taking camera level with a horizontal optical axis.','   ')))
 def test_blank_focus_and_scene_do_not_create_positive_roles(self):
  self.assertEqual(semantics(request('','')), {})
if __name__=='__main__':unittest.main()
