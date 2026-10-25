"""Sports owner, phase and interpretation boundaries; saved pixels require separate review."""
import json, unittest
from pathlib import Path
A=Path(__file__).resolve().parents[1]/'assets'
def read(n):return json.loads((A/n).read_text())
class SportsFictionSemantics(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=read('photo_sports_fiction_semantics_20261025.json')
  cls.cards={c['id']:c for c in cls.s['cards']}
  cls.records=read('photo_candidate_sports_fiction_20261025.json')['candidates']
  cls.bindings=read('photo_candidate_sports_fiction_bindings_20261025.json')['slot_bindings']
 def test_relay_keeps_two_hand_owners_on_one_baton(self):
  c=self.cards['A04'];text=c['proposal_en']
  for part in ['rear runner\'s hand','single baton','front runner reaches back']:self.assertIn(part,text)
  contacts={r['subject'] for r in c['relations'] if r['object']=='baton' and r['predicate']=='contacts'}
  self.assertEqual(contacts,{'giving_hand','receiving_hand'})
  self.assertIn('합법성',c['confusion_boundary'])
 def test_swim_support_is_separate_from_airborne_phase(self):
  self.assertIn('front and back on the starting platform',self.cards['S01']['proposal_en'])
  self.assertIn('hands hold the front edge',self.cards['S01']['proposal_en'])
  self.assertIn('feet have left',self.cards['S02']['proposal_en'])
  self.assertNotEqual(self.s['card_candidate_map']['S01'],self.s['card_candidate_map']['S02'])
 def test_archery_distinguishes_bow_and_string_owners(self):
  edges={(r['subject'],r['predicate'],r['object']) for r in self.cards['R01']['relations']}
  self.assertIn(('bow_hand','holds','bow'),edges)
  self.assertIn(('string_hand','contacts','string'),edges)
  self.assertIn(('arrow','nocked_on','string'),edges)
 def test_narrative_and_diagnosis_cannot_get_positive_bindings(self):
  diag={cid for cid,r in self.records.items() if r['record_kind']=='diagnostic'}
  self.assertEqual(len(diag),330)
  self.assertTrue(all(b['candidate_id'] not in diag for b in self.bindings.values()))
  for cid in diag:self.assertEqual(self.records[cid]['effects'],{'dimensions':[],'properties':[]})
 def test_screen_does_not_assert_legality(self):
  c=self.cards['B02'];self.assertEqual(len(c['owners']),4)
  self.assertIn('합법성',c['confusion_boundary']);self.assertIn('ball handler',c['proposal_en'])
 def test_sample_containers_do_not_prove_doping(self):
  self.assertIn('검사=위반',self.cards['X07']['confusion_boundary'])
  self.assertIn('sealed sample containers',self.cards['X07']['proposal_en'])
 def test_single_tap_contact_does_not_prove_surrender_or_consent(self):
  self.assertIn('항복·동의',self.cards['X05']['confusion_boundary'])
  self.assertEqual(self.cards['X05']['verification_scope'],'authored_snapshot_result_unobservable')
 def test_jammer_and_kneeskin_have_distinct_torso_connections(self):
  self.assertIn('bare upper torso remains separate',self.cards['W09']['proposal_en'])
  self.assertIn('continuous swimsuit torso',self.cards['W14']['proposal_en'])
  self.assertNotEqual(self.s['card_candidate_map']['W09'],self.s['card_candidate_map']['W14'])
 def test_training_bib_reuses_source_and_graphic_aura_is_deferred(self):
  self.assertEqual(self.s['card_candidate_map']['W01'],'cand_257e281178dd57ddbeb1902f74e619a9')
  self.assertIn('X02',self.s['deferred_cards']);self.assertNotIn('X02',self.s['card_candidate_map'])
 def test_selected_source_requires_all_visible_groups_and_preserves_limits(self):
  for c in self.cards.values():
   self.assertEqual(len(c['components']),3)
   self.assertEqual(c['review_policy'],{'partial_is_fail':True,'unobservable':'UNOBSERVABLE_NOT_PASS','no_pixels':'BLOCKED_UNSCORED'})
   self.assertFalse(c['hard_activation']);self.assertFalse(c['automatic_bundle'])
  for r in self.records.values():
   if r['record_kind']!='visual_option':continue
   contract=r['content']['application_contract']
   for clause in ['partial_is_fail','UNOBSERVABLE_NOT_PASS','No native or pixel approval']:self.assertIn(clause,contract)
   self.assertEqual(r['content']['aliases'],[])
 def test_adult_relational_proposal_requires_explicit_adult_context(self):
  cid=self.s['card_candidate_map']['X08']
  self.assertIs(self.records[cid]['conditions']['requires_adult_context'],True)
  self.assertIn('성인성은 사용자 설정 근거',self.cards['X08']['confusion_boundary'])
 def test_provenance_has_no_dangling_source_or_owner_endpoint(self):
  source_ids={s['id'] for s in self.s['sources']}
  for c in self.cards.values():
   self.assertTrue(set(c['source_ids'])<=source_ids)
   owners={o['id'] for o in c['owners']}
   for r in c['relations']:
    self.assertIn(r['subject'],owners);self.assertIn(r['object'],owners)
if __name__=='__main__':unittest.main()
