"""Source projection and authority-boundary regressions for Atompunk data."""
import copy
import json
from pathlib import Path
import sys
import unittest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))
import photo_global_index as projection
import photo_semantic_evidence as native


class AtompunkSourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assets = SKILL / 'assets'
        cls.records = json.loads((assets / 'photo_candidate_atompunk_20261023.json').read_bytes())['candidates']
        cls.by_card = {r['content']['research_semantics']['id']: r for r in cls.records.values()}
        cls.registry = json.loads((assets / 'photo_atompunk_semantics_20261023.json').read_bytes())

    def test_context_is_excluded_by_actual_positive_document_projection(self):
        docs = projection.documents({'candidates': self.records})
        self.assertEqual(len(docs), 88)
        for key in ['V05', 'X01', 'X02', 'X03', 'X04', 'X05', 'X06', 'X07', 'X08', 'X09', 'X10', 'X11', 'X12']:
            self.assertNotIn(self.by_card[key]['id'], docs)

    def test_graphs_and_claim_limits_do_not_enter_positive_text(self):
        source = copy.deepcopy(self.by_card['E08'])
        marker = 'UNTRUSTED_RESEARCH_ONLY_SENTINEL_99173'
        source['content']['research_semantics']['claim_limit_ko'] = marker
        source['content']['research_semantics']['relations'].append({'subject':marker, 'predicate':marker, 'object':marker})
        self.assertNotIn(marker, projection.text(source)[1])

    def test_research_metadata_does_not_supply_native_qualification(self):
        for key in ['E05', 'S01', 'M07', 'B02', 'V03', 'H03']:
            with self.subTest(key=key):
                self.assertNotEqual(native.native_status(self.by_card[key]), 'qualified')

    def test_no_automatic_profile_or_bundle_is_created(self):
        self.assertEqual({r['record_kind'] for r in self.records.values()}, {'visual_option','diagnostic'})
        for record in self.records.values():
            self.assertNotIn('associated_profile_ids', record['content'])
            self.assertNotIn('member_candidates', record['content'])

    def test_keyword_rows_are_routes_and_do_not_replace_source_meaning(self):
        routes = self.registry['keyword_routes']
        self.assertEqual(len(routes), 191)
        for row in routes:
            self.assertTrue(row['seed_is_not_full_card_equivalence'])
            self.assertTrue(all(cid in self.records for cid in row['candidate_ids']))

    def test_every_research_relation_has_its_own_declared_endpoints(self):
        for record in self.records.values():
            meta = record['content']['research_semantics']
            owners = {r['id'] for r in meta['owners']}
            for rel in meta['relations']:
                self.assertLessEqual({rel['subject'],rel['object']}, owners)

    def test_distinct_satellite_and_lighting_sources_keep_their_structures(self):
        satellite = self.by_card['S01']['content']
        lamp = self.by_card['F03']['content']
        self.assertIn('four long whip antennae', satellite['en'])
        self.assertIn('네 개', satellite['ko'])
        self.assertNotIn('bulb', satellite['en'])
        self.assertIn('each rod tip', lamp['en'])
        self.assertIn('각 막대 끝', lamp['ko'])

    def test_en_ko_shape_boundaries_remain_explicit(self):
        for key, en, ko in [('B02','lower central','낮은 중앙'), ('M07','overlap in depth','깊이 방향으로 겹친'),
                            ('H03','six-legged','여섯 다리'), ('E08','below the water surface','수면 아래'),
                            ('V03','one-piece swimsuit','원피스 수영복')]:
            with self.subTest(key=key):
                self.assertIn(en,self.by_card[key]['content']['en'])
                self.assertIn(ko,self.by_card[key]['content']['ko'])


if __name__ == '__main__':
    unittest.main()
