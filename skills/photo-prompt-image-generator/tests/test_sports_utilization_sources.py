"""Actual discovery projection and local part boundaries, independent from generation outcomes."""
import json,sys,unittest
from pathlib import Path
S=Path(__file__).resolve().parents[1];A=S/'assets';sys.path.insert(0,str(S/'scripts'))
import photo_global_index as index
read=lambda n:json.loads((A/n).read_text())
class SportsUtilizationSources(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.side=read('photo_sports_fiction_semantics_20261025.json');cls.cards={c['id']:c for c in cls.side['cards']};cls.supp={c['id']:c for c in cls.side['supplemental_cards']};cls.records=read('photo_candidate_sports_fiction_20261025.json')['candidates'];cls.bindings=read('photo_candidate_sports_fiction_bindings_20261025.json')['slot_bindings']
 def test_components_are_actual_search_fields(self):
  for c in self.cards.values():
   cid=self.side['card_candidate_map'].get(c['id'])
   if cid not in self.records:continue
   r=self.records[cid];f=index.fields(r)
   self.assertEqual(f['concept_units'],[g[l] for g in c['components'] for l in ['en','ko']])
   self.assertTrue(f['semantic_relations']);self.assertTrue(f['keywords'])
   self.assertNotEqual(r['content']['definition'],r['content']['en'])
 def test_relations_keep_both_owned_endpoints_and_explicit_type(self):
  for c in self.cards.values():
   cid=self.side['card_candidate_map'].get(c['id'])
   if cid not in self.records:continue
   owners={x['id']:x['description'] for x in c['owners']}
   expected=[{'subject':owners[r['subject']],'type':r['predicate'].replace('_',' '),'object':owners[r['object']]} for r in c['relations']]
   self.assertEqual(self.records[cid]['content']['relations'],expected)
 def test_lookup_names_do_not_activate_or_claim_native_approval(self):
  self.assertFalse(self.side['utilization_enrichment']['native_approval'])
  self.assertEqual(self.side['utilization_enrichment']['rank_policy_changes'],0)
  for r in self.records.values():
   if r['record_kind']=='visual_option':self.assertEqual(r['content']['aliases'],[])
  for c in self.supp.values():self.assertFalse(c['hard_activation']);self.assertFalse(c['native_approval'])
 def test_shuttle_material_is_a_bounded_feathered_variant(self):
  c=self.supp['U05'];self.assertIn('feathered badminton shuttle',c['proposal_en'])
  self.assertIn('rounded cork base',c['proposal_en']);self.assertIn('open conical crown',c['proposal_en'])
  self.assertIn('not all shuttle materials',c['confusion_boundary'])
 def test_blade_and_boot_keep_different_ice_contacts(self):
  c=self.supp['U03'];self.assertIn('runner edge meets the ice',c['proposal_en']);self.assertIn('boot sole stays above',c['proposal_en'])
  self.assertIn('blade guard',c['confusion_boundary'])
 def test_bicycle_controls_do_not_prove_actuation(self):
  c=self.supp['U01'];self.assertIn('separate curved brake lever',c['proposal_en']);self.assertIn('does not prove braking',c['confusion_boundary'])
 def test_bottle_cage_and_frame_do_not_merge(self):
  c=self.supp['U02'];self.assertIn('inside that same cage',c['proposal_en']);self.assertIn('rather than merging with the frame tube',c['proposal_en'])
 def test_racket_has_one_continuous_structure(self):
  c=self.supp['U06'];self.assertIn('one closed head rim',c['proposal_en']);self.assertIn('one slender shaft',c['proposal_en']);self.assertIn('same racket',c['proposal_en'])
 def test_diagnostics_stay_out_of_bindings(self):
  diag={cid for cid,r in self.records.items() if r['record_kind']=='diagnostic'};self.assertEqual(len(diag),330)
  self.assertFalse(any(b['candidate_id'] in diag for b in self.bindings.values()))
 def test_historical_sources_do_not_claim_current_rules(self):
  for s in self.side['supplemental_sources']:
   if 'historical' in s['access']:self.assertTrue(any(term in s['scope'] for term in ['current','certification']))
if __name__=='__main__':unittest.main()
