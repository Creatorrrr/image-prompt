"""Campus data regression boundaries, independent of image/render success."""
import json
from pathlib import Path
import unittest

A=Path(__file__).resolve().parents[1]/'assets'
REG=json.loads((A/'photo_campus_life_semantics_20261024.json').read_text())
CARDS={c['card_id']:c for c in REG['cards']}
ROWS=json.loads((A/'photo_candidate_campus_life_20261024.json').read_text())['candidates']
BIND=json.loads((A/'photo_candidate_campus_life_bindings_20261024.json').read_text())['slot_bindings']

class CampusBoundaryTests(unittest.TestCase):
    def row(self,key):return ROWS[CARDS[key]['candidate_id']]
    def test_context_never_has_positive_binding(self):
        bound={b['candidate_id'] for b in BIND.values()}
        for c in REG['cards']:
            if c['mode'] in {'context_only','temporal'}:
                self.assertEqual(self.row(c['card_id'])['record_kind'],'diagnostic')
                self.assertNotIn(c['candidate_id'],bound)
                self.assertEqual(self.row(c['card_id'])['effects']['dimensions'],[])
    def test_all_reference_routes_have_registered_targets(self):
        manifest=json.loads((A/'photo_candidate_corpus_manifest.json').read_text())
        all_ids=set()
        for m in manifest['modules']:
            if m['kind']=='candidates':all_ids.update(json.loads((A/m['file']).read_text())['candidates'])
        self.assertEqual(len(REG['keyword_routes']),356)
        self.assertTrue(all(set(r['candidate_ids'])<=all_ids for r in REG['keyword_routes']))
    def test_jacket_is_distinct_from_knitted_letter_sweater(self):
        j=self.row('W01')['content']['en'];s=self.row('W02')['content']['en']
        self.assertIn('front snaps',j);self.assertIn('contrasting sleeves',j)
        self.assertIn('knitted pullover',s);self.assertIn('letter patch',s)
        self.assertNotEqual(CARDS['W01']['candidate_id'],CARDS['W02']['candidate_id'])
    def test_lab_work_closure_and_wrist_boundary_are_preserved(self):
        en=self.row('W23')['content']['en'];ko=self.row('W23')['content']['ko']
        for term in ['closed lab coat','over the eyes','no exposed wrist gap']:self.assertIn(term,en)
        self.assertIn('손목 피부가 드러나지 않는다',ko)
    def test_subfusc_is_under_gown_and_not_gown_synonym(self):
        self.assertIn('beneath a black academic gown',self.row('W28')['content']['en'])
        self.assertNotEqual(CARDS['W27']['candidate_id'],CARDS['W28']['candidate_id'])
    def test_head_support_differs_from_pelvic_support(self):
        head=CARDS['A27']['relations'];pelvis=CARDS['A30']['relations']
        self.assertIn({'from':'A_head','relation':'supported_by','to':'B_thighs'},head)
        self.assertIn({'from':'A_pelvis','relation':'supported_by','to':'B_thighs'},pelvis)
    def test_draped_garment_owner_and_helper_hands_are_separate(self):
        g=CARDS['A23']['relations']
        self.assertIn({'from':'B_hands','relation':'belongs_to','to':'B'},g)
        self.assertIn({'from':'jacket','relation':'rests_on','to':'A_shoulders'},g)
        self.assertIn('outside its sleeves',self.row('A23')['content']['en'])
    def test_wall_contact_has_visible_passage_distinct_from_doorway_occupation(self):
        self.assertIn('visible passage beside B',self.row('A32')['content']['en'])
        self.assertIn('occupying most of its width',self.row('A37')['content']['en'])
    def test_screen_aliases_do_not_add_physical_people(self):
        en=self.row('P07')['content']['en']
        self.assertIn('inside a laptop screen',en);self.assertIn('only one physical person',en)
    def test_diagnostic_claim_limits_remain_explicit(self):
        for key in ['C02','C10','C14','C15','C16','C18','C20']:
            self.assertEqual(self.row(key)['record_kind'],'diagnostic')
            self.assertFalse(self.row(key)['content']['research_semantics']['native_approval'])
    def test_new_records_and_binding_roles_have_expected_closure(self):
        self.assertEqual(sum(r['record_kind']=='visual_option' for r in ROWS.values()),100)
        self.assertEqual(sum(r['record_kind']=='diagnostic' for r in ROWS.values()),23)
        self.assertEqual(len(BIND),220)
        self.assertNotIn(CARDS['A25']['candidate_id'],ROWS)
    def test_research_graph_is_not_native_authority(self):
        for row in ROWS.values():
            self.assertNotIn('semantic_review',row)
            self.assertFalse(row['content']['research_semantics']['native_approval'])
            self.assertIn('not native facts',row['content']['application_contract'] if row['record_kind']=='visual_option' else 'not native facts')

if __name__=='__main__':unittest.main()
