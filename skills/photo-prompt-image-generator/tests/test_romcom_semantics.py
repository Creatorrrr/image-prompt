"""Boundary regressions for romcom data; no image or network calls."""
import json
from pathlib import Path
import unittest

A=Path(__file__).resolve().parents[1]/'assets'
def read(name):return json.loads((A/name).read_text())

class RomcomSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=read('photo_romcom_semantics_20261024.json')
        cls.records=read('photo_candidate_romcom_20261024.json')['candidates']
        cls.by_key={r['content']['research_semantics']['id']:r for r in cls.records.values()}

    def test_context_stays_out_of_positive_visual_source(self):
        diagnostics=[r for r in self.records.values() if r['record_kind']=='diagnostic']
        self.assertEqual(len(diagnostics),19)
        for r in diagnostics:
            self.assertNotIn('en',r['content']);self.assertNotIn('ko',r['content'])
            self.assertEqual(r['effects'],{'dimensions':[],'properties':[]})
            self.assertFalse(r['content']['research_semantics']['native_approval'])

    def test_complete_original_inventory_keeps_sensitive_tail(self):
        routes=self.registry['keyword_routes']
        self.assertEqual(len(routes),317)
        self.assertEqual([sum(k['table']==n for k in routes) for n in (19,20,21)],[15,19,14])
        self.assertFalse(self.registry['automatic_hard_activation'])
        for row in routes:
            self.assertTrue(row['discovery_only']);self.assertFalse(row['automatic_hard_activation'])
            self.assertTrue(row['original_definition'])

    def test_sleeve_skin_and_hand_owners_are_distinct(self):
        sleeve=self.by_key['R05']['content'];wrist=self.by_key['R28']['content']
        self.assertIn("A's sleeve",sleeve['en']);self.assertIn('off A\'s exposed wrist',sleeve['en'])
        self.assertIn("B's exposed wrist",wrist['en'])
        hand=self.by_key['R03']['content']
        self.assertIn('A and B',hand['en']);self.assertIn('two thumbs',hand['en'])

    def test_shared_object_requires_connection_endpoints(self):
        umbrella=self.by_key['R07']['content']['en'];earbuds=self.by_key['R08']['content']['en']
        for phrase in ('one umbrella shaft','same canopy','both heads'):self.assertIn(phrase,umbrella)
        for phrase in ("A's near ear","B's near ear",'Y junction','same device'):self.assertIn(phrase,earbuds)

    def test_no_contact_kiss_and_different_supports_are_not_merged(self):
        self.assertIn('visible gap between their lips',self.by_key['R20']['content']['en'])
        self.assertIn("beneath B's upper back",self.by_key['R15']['content']['en'])
        self.assertIn("beneath B's bent knees",self.by_key['R15']['content']['en'])
        self.assertIn("A's back",self.by_key['R16']['content']['en'])
        self.assertIn("B's thighs",self.by_key['R16']['content']['en'])

    def test_drawn_symbols_are_medium_guarded(self):
        for key in ('M01','M02','M03','M04'):
            r=self.by_key[key]
            self.assertIn('illustration',r['conditions']['requires_any_tags'])
            self.assertFalse(r['content']['research_semantics']['native_approval'])
        self.assertNotIn('requires_any_tags',self.by_key['E05']['conditions'])

    def test_optical_and_temporal_concepts_keep_their_boundaries(self):
        routes={k['id']:k for k in self.registry['keyword_routes']}
        self.assertNotIn(self.by_key['F06']['id'],routes['T17-R04']['candidate_ids'])
        self.assertEqual(routes['T04-R12']['context_card_id'],'X04')
        self.assertEqual(routes['T17-R04']['context_card_id'],'X13')
        self.assertEqual(self.by_key['X04']['record_kind'],'diagnostic')
        self.assertEqual(self.by_key['X13']['record_kind'],'diagnostic')
        self.assertNotIn('en',self.by_key['X13']['content'])

if __name__=='__main__':unittest.main()
