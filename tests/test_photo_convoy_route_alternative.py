"""Proposed post-integration data tests; not executed during BEFORE qualification."""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(S));import prompt_generator as g
PID='biaoju_guarded_cargo_departure';FIELD='departure_route_phrase'
NEW='transport contact points and body orientations continue from yard through gate onto one readable road'
OLD='wheels hooves handles and body orientations continue from yard through gate onto one readable road'
class ConvoyRouteAlternativeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.registry=g.load_visual_obligation_registry(S.parent/'assets/photo_prompt_visual_obligations.json')
  cls.profile=next(p for p in cls.registry['profiles']if p['id']==PID)
 def bindings(self,route):
  extras={'bureau_origin_phrase':' with the open threshold and adjacent road visible together','loaded_cargo_phrase':' with tied panniers or boxes visibly attached to this chosen single unit','escort_distribution_phrase':' keeping each adult outside the sealed load with clear protective spacing','biaoju_confound_phrase':' as shown by the shared load ownership and armed protective positions'}
  out={k:v['must_mention_any'][0]+extras.get(k,'')for k,v in self.profile['evidence_requirements'].items()};out[FIELD]=route+' with the chosen transport grounded on that same departure path';return out
 def normalize(self,b):
  return g.normalize_visual_intent(dict(contract_version=g.VISUAL_INTENT_CONTRACT_VERSION,provenance='agent_prepack',obligations=[dict(profile_id=PID,source='explicit_user_requirement',scope='request_only',source_text=self.profile['activation']['exact_terms'][0],bindings=b)]),self.registry)
 def test_generic_and_legacy_routes(self):
  for branch in (NEW,OLD):
   b=self.bindings(branch);self.normalize(b);self.assertTrue(g.candidate_pack_visual_component_match(self.profile,' '.join(b.values())))
 def test_five_duties_remain_required(self):
  self.assertEqual(len(self.profile['required_evidence_fields']),5)
  for key in self.profile['required_evidence_fields']:
   b=self.bindings(NEW);del b[key]
   self.assertIsNone(g.candidate_pack_visual_component_match(self.profile,' '.join(b.values())))
 def test_disconnected_route_rejected(self):
  b=self.bindings(NEW);b[FIELD]='The distant road remains disconnected from the closed loading yard and its stationary sealed cargo transport'
  with self.assertRaises(ValueError):self.normalize(b)
 def test_preserve_legacy_and_gate(self):
  group=next(x for x in self.profile['semantics']['component_semantics']['groups']if x['id']=='continuous_departure_route')
  self.assertIn(OLD,group['any_terms']);self.assertIn(NEW,group['any_terms']);self.assertIn(OLD,self.profile['evidence_requirements'][FIELD]['must_mention_any']);self.assertEqual(self.profile['evidence_requirements'][FIELD]['min_content_words'],15)
if __name__=='__main__':unittest.main()
