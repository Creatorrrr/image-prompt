"""Source-projection and nonvisual-boundary regressions for espionage data."""
import copy,json,sys,unittest
from pathlib import Path
SKILL=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SKILL/'scripts'))
import photo_global_index as projection
import photo_semantic_evidence as native

class EspionageBoundaries(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  a=SKILL/'assets'
  cls.records=json.loads((a/'photo_candidate_espionage_20261023.json').read_bytes())['candidates']
  cls.bindings=json.loads((a/'photo_candidate_espionage_bindings_20261023.json').read_bytes())['slot_bindings']
  cls.registry=json.loads((a/'photo_espionage_semantics_20261023.json').read_bytes())
  cls.by_slug={r['content']['research_semantics']['slug']:r for r in cls.records.values() if 'slug' in r['content']['research_semantics']}
 def test_real_positive_projection_excludes_context_and_held_specimens(self):
  docs=projection.documents({'candidates':self.records})
  positives={cid for cid,r in self.records.items() if r['record_kind']=='visual_option'}
  self.assertEqual(set(docs),positives)
  for slug in ['button_lens','watch_camera','number_pad','peak_lapel','plate_carrier','microdot_comparison']:
   self.assertNotIn(self.by_slug[slug]['id'],docs)
 def test_mutated_research_graph_is_neither_search_text_nor_native_proof(self):
  record=copy.deepcopy(self.by_slug['earpiece_contact'])
  before=projection.text(record)
  record['content']['research_semantics']['directed_relations'].append({'subject':'FAKE_AUTHORITY_SENTINEL','relation':'claims','object':'qualified'})
  record['content']['research_semantics']['native_approval']=True
  self.assertEqual(projection.text(record),before)
  self.assertNotEqual(native.native_status(record),'qualified')
 def test_context_cannot_get_optional_binding(self):
  for binding in self.bindings.values():
   self.assertEqual(self.records[binding['candidate_id']]['record_kind'],'visual_option')
   self.assertEqual(binding['role'],'optional')
 def test_human_contact_does_not_become_unconditional_object_fact(self):
  for slug in ['direct_handoff','earpiece_contact','cuff_adjustment','other_tie','restrained_seated']:
   self.assertEqual(self.by_slug[slug]['conditions'],{'for_any':['human']})
 def test_transfer_contact_and_not_yet_touching_are_separate_sources(self):
  direct=self.by_slug['direct_handoff']['content'];gap=self.by_slug['suspended_handoff']['content']
  self.assertIn('opposite edges of one envelope',direct['en'])
  self.assertIn('visible gap',gap['en'])
  self.assertIn('빈틈',gap['ko'])
  self.assertNotIn('associated_profile_ids',direct)
 def test_ear_worn_contact_does_not_borrow_telephone_endpoints(self):
  ear=self.by_slug['earpiece_contact']['content'];phone=self.by_slug['receiver_pose']['content']
  self.assertIn('seated at the same person',ear['en'])
  self.assertIn('upper end',phone['en']);self.assertIn('lower end',phone['en'])
  self.assertNotIn('receiver',ear['en'])
 def test_actor_lookback_is_not_a_camera_effect(self):
  self.assertNotIn('camera',self.by_slug['over_shoulder_glance']['effects']['dimensions'])
  self.assertIn('torso faces forward',self.by_slug['over_shoulder_glance']['content']['en'])
 def test_same_wearer_and_other_wearer_are_not_unioned(self):
  self.assertIn('same wearer',self.by_slug['cuff_adjustment']['content']['en'])
  self.assertIn('another person',self.by_slug['other_tie']['content']['en'])
 def test_restraint_chain_has_two_separately_declared_endpoints(self):
  graph=self.by_slug['restrained_seated']['content']['research_semantics']['directed_relations']
  self.assertIn({'subject':'chain.end1','relation':'attached_to','object':'cuff1'},graph)
  self.assertIn({'subject':'chain.end2','relation':'attached_to','object':'cuff2'},graph)
 def test_nonvisual_terms_do_not_create_visual_profiles_or_bundles(self):
  self.assertEqual({r['record_kind'] for r in self.records.values()},{'visual_option','diagnostic'})
  for r in self.records.values():
   self.assertNotIn('member_candidates',r['content'])
   self.assertNotIn('associated_profile_ids',r['content'])
  contexts=self.registry['context_distinctions']
  for term in ['Consent','Torture','Sexual blackmail','Honey trap vs cyber honeypot']:
   self.assertTrue(any(c['term_en']==term and c['positive_retrieval_eligible'] is False for c in contexts))
 def test_reuse_does_not_claim_new_native_authority(self):
  reused=[d for d in self.registry['adoption_decisions'] if d['decision']=='reuse']
  self.assertEqual(len(reused),17)
  self.assertTrue(all(d['original_unchanged'] for d in reused))
  for record in self.records.values():self.assertNotEqual(native.native_status(record),'qualified')
if __name__=='__main__':unittest.main()
