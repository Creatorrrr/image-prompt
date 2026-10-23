"""Semantic boundary regression checks without retrieval or image calls."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'

def read(name):return json.loads((A/name).read_text())

class HaremSemanticsTests(unittest.TestCase):
 def test_context_never_becomes_positive_visual_text(self):
  records=read('photo_candidate_harem_20261023.json')['candidates']
  diagnostics=[r for r in records.values() if r['record_kind']=='diagnostic']
  self.assertEqual(len(diagnostics),14)
  for r in diagnostics:
   self.assertNotIn('en',r['content']);self.assertNotIn('ko',r['content'])
   self.assertFalse(r['content']['research_semantics']['native_approval'])
   self.assertEqual(r['effects'],{'dimensions':[],'properties':[]})

 def test_advisory_routes_do_not_create_mandatory_bundles(self):
  reg=read('photo_harem_semantics_20261023.json')
  self.assertEqual(len(reg['keyword_routes']),320)
  self.assertFalse(reg['automatic_hard_activation'])
  for r in reg['keyword_routes']:
   self.assertFalse(r['automatic_hard_activation']);self.assertTrue(r['discovery_only'])

 def test_same_owner_and_cross_owner_interlacing_stay_separate(self):
  records=read('photo_candidate_harem_20261023.json')['candidates']
  selected=next(r for r in records.values() if r['content']['research_semantics']['id']=='H07')
  self.assertIn('A and B hold hands',selected['content']['en'])
  cid='cand_d2834908636b578489498652230bafd9'
  manifest=read('photo_candidate_corpus_manifest.json')
  old=next(d[cid] for m in manifest['modules'] if m['kind']=='candidates'
           for d in [read(m['file'])['candidates']] if cid in d)
  self.assertIn('같은 인물',old['content']['ko'])
  self.assertTrue(any("actor's own" in x for x in old['content']['paraphrases']))

 def test_existing_offer_keeps_alternative_not_two_objects(self):
  cid='cand_522c907a6a97547886a2d207a4138b03'
  manifest=read('photo_candidate_corpus_manifest.json')
  record=next(d[cid] for m in manifest['modules'] if m['kind']=='candidates'
              for d in [read(m['file'])['candidates']] if cid in d)
  self.assertIn(' or ',record['content']['en']);self.assertIn(' 또는 ',record['content']['ko'])
  self.assertIn('내민',record['content']['ko'])

if __name__=='__main__':unittest.main()
