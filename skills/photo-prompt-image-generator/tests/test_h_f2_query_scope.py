"""Scope behavior, literal ownership and original-input binding regression tests."""
from pathlib import Path
import hashlib
import re
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from photo_h_f2_query_scope import analyze

def tokens(text):
    return re.findall(r'[^\W_]+',text.casefold(),re.UNICODE)

class QueryScopeTests(unittest.TestCase):
    def scope(self,text):
        out=analyze(text,tokens)
        self.assertEqual(out['input_sha256'],hashlib.sha256(text.encode()).hexdigest())
        for key in ['format_spans','contrast_spans','positive_spans']:
            for row in out[key]:self.assertEqual(row['quote'],text[row['start']:row['end']])
        self.assertFalse(out['candidate_filter']);self.assertFalse(out['embedding_input_changed'])
        return out
    def test_headers_are_not_meaning(self):
        r=self.scope('Photographic role: A visible knot.\nScene context: Sailing rope.')
        self.assertEqual(r['positive_terms'],sorted(set(tokens('Photographic A visible knot. Scene context: Sailing rope.'))))
    def test_real_role_word_survives(self):
        r=self.scope('Photographic role: The declared role of one participant.')
        self.assertIn('role',r['positive_terms'])
    def test_comma_contrast_is_not_positive_evidence(self):
        r=self.scope('Etched surface texture, distinct from digital noise.')
        self.assertIn('etched',r['positive_terms']);self.assertNotIn('digital',r['positive_terms'])
    def test_separate_from_adjunct(self):
        r=self.scope('A physical temperature, separate from illumination tint.')
        self.assertNotIn('illumination',r['positive_terms'])
    def test_spatial_relation_is_preserved(self):
        r=self.scope('The stone remains separate from the bowl.')
        self.assertIn('bowl',r['positive_terms']);self.assertFalse(r['contrast_spans'])
    def test_scene_line_resumes_after_exclusion(self):
        r=self.scope('Photographic role: A mineral , distinct from painted foam.\nScene context: A tabletop.')
        self.assertNotIn('foam',r['positive_terms']);self.assertIn('tabletop',r['positive_terms'])
    def test_clause_resumes(self):
        r=self.scope('A woven fabric, distinct from velvet but with canvas; brass hardware.')
        self.assertNotIn('velvet',r['positive_terms']);self.assertIn('canvas',r['positive_terms']);self.assertIn('brass',r['positive_terms'])
    def test_not_only_is_additive(self):
        r=self.scope('Not only velvet but also silk.')
        self.assertIn('velvet',r['positive_terms']);self.assertIn('silk',r['positive_terms'])
    def test_quoted_not_is_literal(self):
        for quote in ['"NOT OPEN"',"'NOT OPEN'",'“NOT OPEN”','‘NOT OPEN’','`NOT OPEN`']:
            with self.subTest(quote=quote):
                r=self.scope('Show '+quote+' in the image.')
                self.assertIn('not',r['positive_terms']);self.assertIn('open',r['positive_terms']);self.assertFalse(r['contrast_spans'])
    def test_epistemic_without_is_retained(self):
        r=self.scope("The actor's declared pose, without adding a prop.")
        self.assertIn('prop',r['positive_terms'])
    def test_quoted_punctuation_does_not_close_scope(self):
        r=self.scope('A physical mark rather than "a; fake" print. A second scene.')
        self.assertNotIn('print',r['positive_terms']);self.assertIn('second',r['positive_terms'])
    def test_decimal_does_not_close_scope(self):
        r=self.scope('A mineral, distinct from 3.5 kg of clay. A blue support.')
        self.assertNotIn('clay',r['positive_terms']);self.assertIn('blue',r['positive_terms'])
    def test_unclosed_quote_is_retained(self):
        r=self.scope('Show "NOT OPEN')
        self.assertIn('not',r['positive_terms']);self.assertFalse(r['contrast_spans'])
    def test_unknown_language_keeps_terms(self):
        text='나무 표면의 실제 결을 보여 준다.';r=self.scope(text)
        self.assertEqual(r['positive_terms'],sorted(set(tokens(text))))
    def test_ordinary_text_is_unchanged(self):
        text='A small open box and one declared red object.';r=self.scope(text)
        self.assertEqual(r['positive_terms'],sorted(set(tokens(text))))
    def test_header_inside_literal_is_not_a_format(self):
        r=self.scope('"Photographic role: not a caption"')
        self.assertIn('photographic',r['positive_terms']);self.assertIn('not',r['positive_terms'])
    def test_hash_changes_with_original_constraint(self):
        a=self.scope('A knot, distinct from wire.');b=self.scope('A knot, distinct from glue.')
        self.assertEqual(a['positive_terms'],b['positive_terms']);self.assertNotEqual(a['canonical_sha256'],b['canonical_sha256'])
    def test_empty_input_rejected(self):
        with self.assertRaises(ValueError):analyze(' ',tokens)

if __name__=='__main__':unittest.main()
