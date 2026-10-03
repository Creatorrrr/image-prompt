"""Source-state alignment for the selected partly-lowered portcullis variant."""
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg

KO_PARTIAL = '격자가 출입 개구부 안에 있다; 격자 옆단이 수직 홈에 맞물린다; 격자가 그 수직 홈을 따라 부분적으로 내려와 있다'
KO_MECHANISM = '격자가 출입 개구부 안에 있다; 격자 옆단이 수직 홈에 맞물린다; 문짝 회전이 아닌 상하 이동 구조가 읽힌다'
EN_PARTIAL = 'a heavy gridded gate occupies the entrance opening; the grid edges sit inside vertical guide grooves; the gate is partly lowered along those upright grooves'

class PhotoPortcullisKoreanStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}
        cls.index = pg.load_visual_profile_index(ASSETS / 'photo_prompt_visual_profile_index.json', cls.registry)

    def hard_hits(self, text):
        result = pg.resolve_visual_profile_hits(self.registry, [{'source': 'user_requirement', 'text': text, 'polarity': 'positive'}], visual_profile_index=self.index, query_text=text, adult_context=False)
        return {h['profile_id'] for h in result['hits'] if h.get('hard_eligible')}

    def test_exact_terms_align_both_languages_with_selected_state(self):
        self.assertEqual(self.profiles['pf_portcullis']['activation']['exact_terms'], [EN_PARTIAL, KO_PARTIAL])

    def test_complete_partial_variants_retain_hard_activation(self):
        for text in (KO_PARTIAL, EN_PARTIAL):
            with self.subTest(text=text):
                self.assertIn('pf_portcullis', self.hard_hits(text))

    def test_mechanism_only_and_fully_closed_do_not_require_partial_state(self):
        for text in (KO_MECHANISM, KO_MECHANISM + '. 격자는 문턱까지 완전히 내려와 통로를 닫고 있다.', KO_PARTIAL.replace('부분적으로 내려와 있다', '문턱까지 완전히 내려와 있다')):
            with self.subTest(text=text):
                self.assertNotIn('pf_portcullis', self.hard_hits(text))

    def test_omitted_guide_contact_does_not_complete_selected_relation(self):
        incomplete = '; '.join([KO_PARTIAL.split('; ')[0], KO_PARTIAL.split('; ')[2]])
        self.assertNotIn('pf_portcullis', self.hard_hits(incomplete))

    def test_drawbridge_sibling_remains_distinct(self):
        text = self.profiles['pf_drawbridge']['activation']['exact_terms'][0]
        hits = self.hard_hits(text)
        self.assertIn('pf_drawbridge', hits)
        self.assertNotIn('pf_portcullis', hits)

    def test_index_exact_terms_and_cached_semantic_text_are_current(self):
        terms = [r['term'] for r in self.index['exact_lookup'] if r['profile_id'] == 'pf_portcullis']
        self.assertIn(KO_PARTIAL, terms)
        self.assertNotIn(KO_MECHANISM, terms)
        self.assertEqual(self.index['entries']['pf_portcullis']['text'], pg.visual_profile_semantic_text(self.profiles['pf_portcullis']))

if __name__ == '__main__':
    unittest.main()
