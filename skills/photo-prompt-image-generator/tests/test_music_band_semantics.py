"""Consequential music source/ownership boundaries; no claims about saved pixels."""
import json,unittest
from pathlib import Path
A=Path(__file__).resolve().parents[1]/'assets'
def read(name):return json.loads((A/name).read_text())
class MusicBandSemantics(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.registry=read('photo_music_band_semantics_20261025.json')
  cls.cards={x['id']:x for x in cls.registry['cards']}
  cls.records=read('photo_candidate_music_band_20261025.json')['candidates']
  cls.bindings=read('photo_candidate_music_band_bindings_20261025.json')['slot_bindings']
 def test_slap_and_pop_have_different_actual_contact_owners(self):
  self.assertIn('thumb',self.cards['A12']['phrase_en'])
  self.assertIn('index finger under',self.cards['A13']['phrase_en'])
  self.assertNotEqual(self.cards['A12']['candidate_id'],self.cards['A13']['candidate_id'])
 def test_crossed_and_open_hands_do_not_share_one_realization(self):
  self.assertIn('right-hand stick above the left arm',self.cards['A15']['phrase_en'])
  self.assertIn('arms uncrossed',self.cards['A16']['phrase_en'])
 def test_acoustic_cross_stick_is_not_electronic_pad_trigger_authority(self):
  self.assertIn('acoustic snare',self.cards['A20']['phrase_en'])
  self.assertIn('어쿠스틱',self.cards['A20']['phrase_ko'])
  self.assertIn('전자패드',self.cards['A20']['confusion_boundary_ko'])
  self.assertIn('오픈',self.cards['A19']['name_ko'])
 def test_rimshot_contrast_is_not_an_equivalent_component(self):
  row=next(k for k in self.registry['keyword_routes'] if k['term'].startswith('림샷'))
  self.assertIn(self.cards['A20']['candidate_id'],row['contrast_candidate_ids'])
  self.assertNotIn(self.cards['A20']['candidate_id'],row['component_candidate_ids'])
  self.assertFalse(row['equivalence'])
 def test_cello_keeps_floor_endpin_and_opposite_hand_bow(self):
  text=self.cards['A26']['phrase_en']
  for clause in ['between a seated cellist\'s knees','endpin supported on the floor','left hand fingers','right-hand bow hair crosses']:self.assertIn(clause,text)
 def test_flute_does_not_borrow_saxophone_mouthpiece(self):
  self.assertIn('lip plate below the lower lip',self.cards['A27']['phrase_en'])
  self.assertIn('mouthpiece meets the mouth',self.cards['A28']['phrase_en'])
 def test_cables_keep_source_and_destination(self):
  for cid,words in [('B07',['bass cable','DI box','stage-box input']),('B08',['guitar output','three pedals','amplifier input']),('A31',['MIDI controller','data cable','computer'])]:
   for word in words:self.assertIn(word,self.cards[cid]['phrase_en'])
 def test_midi_notes_and_audio_waveform_keep_separate_screen_regions(self):
  self.assertIn('rectangular notes',self.cards['B04']['phrase_en'])
  self.assertIn('continuous waveform',self.cards['B04']['phrase_en'])
  self.assertIn('MIDI 자체',self.cards['B04']['confusion_boundary_ko'])
 def test_shared_microphone_does_not_become_two_capsules_or_a_kiss(self):
  self.assertIn('Two vocalists face one stand-microphone capsule',self.cards['G01']['phrase_en'])
  self.assertIn('각자의',self.cards['G01']['phrase_ko'])
  self.assertIn('키스',self.cards['G01']['confusion_boundary_ko'])
 def test_crowd_support_has_multiple_hand_owners_and_body_regions(self):
  for word in ['hands from different people','back, pelvis, and legs']:self.assertIn(word,self.cards['G15']['phrase_en'])
 def test_reuse_keeps_existing_right_ear_receiver_and_barrier(self):
  self.assertEqual(self.cards['C07']['candidate_id'],'cand_a49173126daf573f9083c0ae11ebf5c6')
  self.assertIn('right ear',self.cards['C07']['registered_phrase_en'])
  self.assertIn('receiver',self.cards['C07']['registered_phrase_en'])
  self.assertIn('front barrier',self.cards['G02']['registered_phrase_en'])
 def test_harness_and_guitar_strap_have_different_targets(self):
  text=self.cards['E10']['phrase_en'];self.assertIn('torso-harness straps meet at a ring',text);self.assertIn('separate broad guitar strap',text)
 def test_specific_trio_does_not_silently_add_a_fourth_bassist(self):
  text=self.cards['H04']['phrase_en'];self.assertIn('saxophonist, pianist, and drummer',text);self.assertNotIn('bassist',text)
 def test_diagnostics_never_receive_positive_bindings(self):
  diagnostic={cid for cid,r in self.records.items() if r['record_kind']=='diagnostic'}
  self.assertEqual(len(diagnostic),32)
  self.assertFalse(any(b['candidate_id'] in diagnostic for b in self.bindings.values()))
 def test_research_has_no_native_or_keyword_activation_authority(self):
  self.assertFalse(self.registry['native_approval']);self.assertFalse(self.registry['automatic_hard_activation'])
  for c in self.cards.values():self.assertFalse(c['native_approval'])
  for k in self.registry['keyword_routes']:self.assertFalse(k['adoption_authority']);self.assertFalse(k['automatic_hard_activation'])
 def test_explicit_adult_sources_keep_their_condition(self):
  for c in self.cards.values():
   if c.get('registration_status')=='reused_complete_existing_source':continue
   r=self.records[c['candidate_id']]
   if 'adult' in c['phrase_en'].lower():self.assertIs(r['conditions'].get('requires_adult_context'),True)
 def test_whole_bilingual_source_is_preserved_and_not_relabelled_qualified(self):
  for c in self.cards.values():
   if c.get('registration_status')=='reused_complete_existing_source':continue
   r=self.records[c['candidate_id']]
   self.assertEqual(r['content']['en'],c['phrase_en']);self.assertEqual(r['content']['ko'],c['phrase_ko'])
   self.assertIn('both relation endpoints',r['content']['application_contract'])
   self.assertEqual(c['native_qualification'],'not_qualified')
if __name__=='__main__':unittest.main()
