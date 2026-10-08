"""Owner, sense and optional-activation regressions; not image proof."""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
from photo_contracts import property_effects_allowed
from visual_profile_contracts import compile_visual_profile,hard_activation_is_supported

class SoilEarthRelationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.extension=json.loads((SKILL/'assets/photo_prompt_soil_earth_extension.json').read_text())
  cls.candidates={c['id']:c for rows in cls.extension['slots'].values() for c in rows}
  cls.authored=json.loads((SKILL/'assets/photo_prompt_visual_obligations_soil_earth.json').read_text())['profiles']
  cls.profiles={p['id']:compile_visual_profile(p) for p in cls.authored}
 def supported(self,p,text):
  return hard_activation_is_supported(p,text,matches=pg.intent_alias_matches,is_negated=pg.intent_term_is_negated)
 def test_complete_realization_and_negation(self):
  for p in self.authored:
   with self.subTest(profile=p['id']):
    whole=p['activation']['exact_terms'][0]
    self.assertTrue(self.supported(p,whole))
    self.assertFalse(self.supported(p,'not '+whole))
    self.assertFalse(self.supported(p,p['semantics']['paraphrase_examples'][0]))
    self.assertFalse(self.supported(p,p['semantics']['visual_components'][0]))
 def test_ambiguous_nonvisual_and_broad_labels_create_no_hard_duties(self):
  for text in ['흙','진흙','토성','식토','소성','군도','자기','매장','대지','지각','사직','석기',
   'pH','CEC','비옥도','페트리코','체르노젬','WAM','Gaia','soil','mud','fertile ground','a muddy portrait']:
   with self.subTest(text=text):self.assertFalse(any(self.supported(p,text) for p in self.authored))
 def test_natural_owner_phrases_enable_optional_discovery(self):
  cases={
   'e010':('A boot pressing into mud leaves a tread depression and a raised mud ridge.','A boot floats over a patterned plastic floor.'),
   'e036':('The slope has shallow erosion channels and downhill branching grooves.','Painted branches surround a smooth flat wall.'),
   'e086':('Unfired earthen blocks are joined by earthen mortar joints.','Glazed red ceramic tiles with white grout.'),
   'e088':('Horizontal rammed earth lifts carry formwork impressions.','Striped wallpaper on a concrete panel.'),
   'e093':('Hands shaping clay hold a clay vessel on wheel beside clay slurry on fingers.','Hands hold a finished porcelain cup beside a steering wheel.'),
   'e109':('Skin beside mud shows thick adhering mud and a fingertip track at edge.','Brown skin with a flat painted line.'),
  }
  for key,(positive,negative) in cases.items():
   p=self.profiles['soil_rel_'+key]
   with self.subTest(profile=key):
    self.assertIsNotNone(pg.candidate_pack_visual_component_match(p,positive))
    self.assertIsNone(pg.candidate_pack_visual_component_match(p,negative))
    self.assertFalse(self.supported(p,positive))
 def test_material_carriers_preserve_body_and_wardrobe_locks(self):
  for eid,dim,target,prop in [('soil_e010','pose','main_subject','foot'),('soil_e109','appearance','main_subject','skin'),
   ('soil_e110','appearance','main_subject','wardrobe'),('soil_e108','concept','selected_terrain','fictional_physics')]:
   c=self.candidates[eid]; lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':dim,'target':target,'property':prop}]}
   with self.subTest(candidate=eid):
    self.assertFalse(property_effects_allowed(lock,c['affected_dimensions'],c['affected_properties']))
    moved=copy.deepcopy(c['affected_properties'])
    for row in moved:row['dimension']='material'
    self.assertFalse(property_effects_allowed(lock,['material'],moved))
  garment=self.candidates['soil_e110']
  optical={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'appearance','target':'main_subject','property':'wardrobe.optical_transmission'}]}
  self.assertTrue(property_effects_allowed(optical,garment['affected_dimensions'],garment['affected_properties']))
 def test_survey_props_and_enclosed_interiors_are_not_default_duties(self):
  for eid in ['soil_e002','soil_e016','soil_e021','soil_e037','soil_e060']:
   self.assertNotIn('scale reference',self.candidates[eid]['en'])
   self.assertNotIn('colour reference',self.candidates[eid]['en'])
  self.assertNotIn('chamber',self.candidates['soil_e100']['en'])
  self.assertNotIn('mound',self.candidates['soil_e100_chamber']['en'])
  self.assertNotIn('touching hand',self.candidates['soil_e109']['en'])
  self.assertNotIn('optical_transmission',{e['property'] for e in self.candidates['soil_e110']['affected_properties']})
 def test_existing_identity_and_effects_are_preserved(self):
  files=tuple(n for n in pg.RESEARCH_EXTENSION_FILENAMES if n!='photo_prompt_soil_earth_extension.json')
  before=pg.load_json(SKILL/'assets/photo_prompt_tags.json',inventory=pg.photo_source_manifest.SourceInventory.for_test(SKILL/'assets',candidate_files=files))
  current=pg.load_json(SKILL/'assets/photo_prompt_tags.json')
  for slot,updates in self.extension['existing_slot_context_extensions'].items():
   old_by={c['id']:c for c in before['slots'][slot]}; new_by={c['id']:c for c in current['slots'][slot]}
   for cid,update in updates.items():
    with self.subTest(candidate=cid):
     old,new=old_by[cid],new_by[cid]
     self.assertEqual({k:v for k,v in old.items() if k not in {'paraphrases','contextual_usage'}},
                      {k:v for k,v in new.items() if k not in {'paraphrases','contextual_usage'}})
     self.assertTrue(set(old.get('paraphrases',[]))<=set(new['paraphrases']))
     self.assertTrue(set(update['paraphrases'])<=set(new['paraphrases']))
 def test_microscopic_and_nonvisual_units_stay_context_only(self):
  for eid in ['e001','e003','e015','e032','e034','e046','e071','e075','e076','e079','e095','e103','e104','e111','e112','e113','e114','e117','e118','e119','e120']:
   with self.subTest(unit=eid):
    self.assertNotIn('soil_'+eid,self.candidates)
    self.assertNotIn('soil_rel_'+eid,self.profiles)
  self.assertNotIn('soil_e023',self.candidates)
if __name__=='__main__':unittest.main()
