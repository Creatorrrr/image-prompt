"""Realistic environments: conditional evidence, non-duplication, and guarded adoption."""
import copy
import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as cs
import validate_photo_prompt_dictionary as validator
from visual_profile_contracts import compile_visual_profile

class RealisticBackgroundTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ext=json.loads((SKILL/'assets/photo_prompt_realistic_background_extension.json').read_text())
  allreg=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
  cls.allreg=allreg
  cls.reg={**allreg,'profiles':[p for p in allreg['profiles'] if p['id'].startswith('rb_')]}
  cls.profiles={p['id']:p for p in cls.reg['profiles']}
  cls.index=pg.build_visual_profile_index_payload(cls.reg)
  cls.data=pg.load_json(SKILL/'assets/photo_prompt_tags.json')
 def hard(self,text):
  rows=[{'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}]
  r=pg.resolve_visual_profile_hits(self.reg,rows,visual_profile_index=self.index,adult_context=True)
  return {x['profile_id'] for x in r['hits'] if x.get('match_basis')=='exact' and x.get('hard_eligible')}
 def test_only_complete_relation_hardens_and_negation_blocks(self):
  for p in self.profiles.values():
   with self.subTest(profile=p['id']):
    phrase=p['activation']['exact_terms'][0]
    self.assertEqual(self.hard(phrase),{p['id']})
    self.assertNotIn(p['id'],self.hard('not '+phrase))
    component=p['authored_components']['components'][0]['evidence_terms'][0]
    self.assertNotIn(p['id'],self.hard(component))
 def test_realism_labels_and_clean_dry_low_noise_requests_do_not_create_hard_duties(self):
  for q in ['realistic background','현실적인 배경','on-location photography','available light','mixed lighting',
   'lived-in environment','documentary photography','sensor noise','film grain','HDR','cinematic',
   'clean new hotel lobby','건조한 맑은 낮 거리','바람 없는 실내','깨끗한 스마트폰 야간 사진',
   '85mm f/1.4 creamy bokeh','focus breathing','서울 주택가','green wallpaper with a white coat']:
   with self.subTest(query=q):self.assertEqual(self.hard(q),set())
 def test_existing_optics_and_wet_surface_profiles_are_reused(self):
  expected={'rb_wet_dry_boundary','rb_highlight_shoulder','rb_depth_focus_continuity','rb_soft_source_environment','rb_hard_source_environment'}
  self.assertFalse(expected & set(self.profiles))
  b=next(x for x in self.data['candidate_bundles'] if x['id']=='rbb_rain_aftermath')
  self.assertIn('wet_surface_light_reflection_owner_relation',b['associated_profile_ids'])
 def test_each_selected_profile_has_all_owner_components_and_invalid_evidence_is_rejected(self):
  for p in self.profiles.values():
   c=compile_visual_profile(p)
   self.assertEqual(len(c['required_evidence_fields']),3)
   self.assertEqual(len(c['render_gates']),3)
   bad=copy.deepcopy(p)
   bad['authored_components']['components'][1]['evidence_field']=bad['authored_components']['components'][0]['evidence_field']
   with self.assertRaises(ValueError):compile_visual_profile(bad)
 def test_bundle_requires_every_member_and_open_dimension(self):
  for b in [x for x in self.data['candidate_bundles'] if x['id'].startswith('rbb_')]:
   self.assertEqual(b['profile_activation'],'independent_request_evidence_only')
   slots={};dims=set()
   for m in b['member_candidates']:
    dims.update(m['affected_dimensions']);slots.setdefault(m['slot'],{'candidates':[]})['candidates'].append({'id':m['id'],'applicability':{'status':'eligible'}})
   pack={'slots':slots,'authorial_core':{'intent_lock':{'open_dimensions':list(dims)}}}
   data={**self.data,'candidate_bundles':[b]}
   self.assertEqual(len(cs.public_bundles(data,pack)['candidates']),1)
   missing=copy.deepcopy(pack);next(iter(missing['slots'].values()))['candidates'].clear()
   self.assertEqual(cs.public_bundles(data,missing)['candidates'],[])
   for dim in dims:
    locked=copy.deepcopy(pack);locked['authorial_core']['intent_lock']['open_dimensions'].remove(dim)
    self.assertEqual(cs.public_bundles(data,locked)['candidates'],[])
 def test_provenance_and_unverified_designs_are_maintenance_only(self):
  ref=self.ext['maintenance_ref'];rec=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(ref['record_id']+'.json')).read_text())
  self.assertEqual(ref['sha256'],cs.digest(rec))
  raw=copy.deepcopy(self.ext);raw.pop('maintenance_ref')
  self.assertEqual(rec['authored_source_sha256'],cs.digest(raw))
  self.assertEqual(sum(not x['source_ids'] for x in rec['maintenance_only']['coverage']),6)
  for entries in self.ext['slots'].values():
   for e in entries:
    self.assertNotIn('http',e['embedding_text'])
    self.assertFalse({'identity','age','species','role'} & set(e['affected_dimensions']))
 def test_real_indexes_bind_every_new_candidate_and_profile(self):
  si=pg.load_semantic_index_payload(SKILL/'assets/photo_prompt_semantic_index.json')
  pg.validate_semantic_index_metadata(si,self.data)
  expected={f"slot:{slot}:{e['id']}" for slot,entries in self.ext['slots'].items() for e in entries}
  self.assertTrue(expected <= set(si['entries']))
  vi=json.loads((SKILL/'assets/photo_prompt_visual_profile_index.json').read_text())
  pg.validate_visual_profile_index_metadata(vi,self.allreg)
  self.assertTrue(set(self.profiles)<=set(vi['entries']))
 def test_runtime_bundles_have_distinct_slots_and_natural_phrases_can_admit_them(self):
  for b in self.data['candidate_bundles']:
   if b['id'].startswith('rbb_'):
    slots=[m['slot'] for m in b['member_candidates']]
    self.assertEqual(len(slots),len(set(slots)),b['id'])
  scenes=[
   ('A portrait beside glass panels with readable material surfaces and middle distance forms.',
    'bundle:rbb_surface_focus'),
   ('A traveler studies a distant landscape with lighter contrast and environmental detail.',
    'bundle:rbb_landscape_depth'),
  ]
  for scene,expected in scenes:
   core={'contract_version':'photo-authorial-core/v3','source_request':scene,
    'subject':'an adult person','setting':scene,'baseline_prompt_en':scene,
    'intent_lock':{'open_dimensions':['composition','material','camera','lighting','atmosphere']}}
   pack={'authorial_core':core,'slots':{},'provenance':{'seed':41}}
   exposed=pg.candidate_pack_candidate_bundles(self.data,pack)
   self.assertIn(expected,{b['id'] for b in exposed['candidates']})
   core['intent_lock']['open_dimensions'].remove('camera')
   self.assertNotIn(expected,{b['id'] for b in pg.candidate_pack_candidate_bundles(self.data,pack)['candidates']})
 def test_short_discovery_units_remain_optional_and_scene_owner_is_not_lobby_only(self):
  for p in self.profiles.values():
   for cue in p['semantics']['visual_components']:
    self.assertNotIn(p['id'],self.hard(cue))
  clean=self.profiles['rb_clean_space_plausibility']['semantics']['definition']
  self.assertIn('clean interior',clean)
  self.assertNotIn('lobby',clean)
  material=next(e for e in self.ext['slots']['texture'] if e['id']=='rb_material_response_contrast_candidate')
  self.assertIsNone(pg.slot_block_reason(self.data,'texture',{'subject_category':'human','preset_domains':[]}))
  self.assertEqual(material['affected_dimensions'],['material'])
 def test_visual_component_schema_accepts_positive_units_and_rejects_malformed_data(self):
  for value in [[], 'glass', ['glass', 'GLASS'], [3], [' ']]:
   bad=copy.deepcopy(self.allreg)
   next(p for p in bad['profiles'] if p['id']=='rb_clean_space_plausibility')['semantics']['visual_components']=value
   errors=[]
   with patch.object(validator,'load_visual_obligation_registry',return_value=bad):
    validator.validate_visual_obligation_registry(SKILL/'assets/photo_prompt_tags.json',errors)
   self.assertTrue(any('visual_components' in e for e in errors),value)

if __name__=='__main__':unittest.main()
