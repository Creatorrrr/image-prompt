"""Check consequential mecha ownership and claim boundaries, not pixel quality."""
import json
from pathlib import Path
import unittest

A=Path(__file__).resolve().parents[1]/'assets'
def read(name):return json.loads((A/name).read_text())

class MechaSemantics(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.registry=read('photo_mecha_robot_semantics_20261024.json')
  cls.cards={c['id']:c for c in cls.registry['cards']}
  cls.records=read('photo_candidate_mecha_robot_20261024.json')['candidates']
  cls.bindings=read('photo_candidate_mecha_robot_bindings_20261024.json')['slot_bindings']
 def edges(self,card):return {(e['from'],e['predicate'],e['to']) for e in self.cards[card]['directed_relations']}
 def test_service_route_keeps_wall_and_machine_endpoints(self):
  self.assertTrue({('cable','joins','wall_socket'),('cable','joins','receptacle'),('receptacle','part_of','machine')}<=self.edges('D01'))
 def test_actuator_keeps_two_different_link_mounts(self):
  self.assertTrue({('barrel','pinned_to','upper_link'),('rod','emerges_from','barrel'),('rod','pinned_to','lower_link')}<=self.edges('B03'))
 def test_cockpit_contacts_do_not_merge_hands_or_pedals(self):
  self.assertEqual(self.edges('C03'),{('left_hand','grips','left_stick'),('right_hand','grips','right_stick'),('left_boot','rests_on','left_pedal'),('right_boot','rests_on','right_pedal')})
 def test_harness_has_seat_anchors_not_only_decorative_straps(self):
  self.assertIn(('straps','anchored_to','seat_frame'),self.edges('C02'))
 def test_robot_hand_and_human_limbs_have_distinct_owners(self):
  edges=self.edges('H07')
  self.assertTrue({('human_hand','part_of','adult'),('thighs','part_of','adult'),('palm','part_of','robot_hand'),('robot_fingers','part_of','robot_hand')}<=edges)
 def test_upper_limb_support_is_not_substituted_by_lower_limb_frame(self):
  edges=self.edges('A12')
  self.assertTrue({('harness','joins','bracket'),('bracket','fixed_to','upper_arm_cuff'),('upper_arm_cuff','joins','elbow_hinge'),('elbow_hinge','joins','forearm_cuff'),('human_wrist','part_of','human_arm')}<=edges)
  self.assertIn('knee_hinges',self.cards['A05']['owners'])
  self.assertNotIn('knee_hinges',self.cards['A12']['owners'])
  self.assertNotIn('adult',self.cards['A12']['proposal_en'].lower())
  self.assertNotIn('성인',self.cards['A12']['proposal_ko'])
 def test_unconfirmed_cases_never_enter_positive_retrieval(self):
  for key in ['G03','K06']:
   cid=self.cards[key]['candidate_id'];self.assertEqual(self.records[cid]['record_kind'],'diagnostic')
   self.assertFalse(any(b['candidate_id']==cid for b in self.bindings.values()))
  self.assertTrue(all(c['positive_retrieval'] is False for c in self.registry['context_boundaries']))
 def test_badge_graphic_is_not_advertised_as_readable_text(self):
  self.assertNotIn('visible_text',self.cards['G07']['proposed_slots'])
 def test_no_research_metadata_promotes_native_approval(self):
  self.assertIs(self.registry['native_approval'],False)
  for record in self.records.values():self.assertIs(record['content']['research_semantics']['native_approval'],False)
 def test_source_literals_preserve_whole_bilingual_realization(self):
  for c in self.cards.values():
   r=self.records[c['candidate_id']]
   if r['record_kind']!='visual_option':continue
   self.assertEqual(r['content']['en'],c['proposal_en']);self.assertEqual(r['content']['ko'],c['proposal_ko'])
   self.assertIn('partial_is_fail',r['content']['application_contract'])
 def test_binding_and_route_references_resolve(self):
  slots=read('photo_candidate_slot_catalog.json')['slot_catalog']
  for b in self.bindings.values():
   self.assertIn(b['candidate_id'],self.records);self.assertIn(b['slot_id'],slots);self.assertEqual(b['role'],'optional')
  for t in self.registry['term_routes']:
   self.assertFalse(t['equivalence']);self.assertFalse(t['automatic_hard_activation'])
   self.assertTrue(set(t['candidate_ids'])<=set(self.records))

if __name__=='__main__':unittest.main()
