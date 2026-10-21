from pathlib import Path
import copy
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from photo_h_f2_query_scope import analyze
from photo_h_f2_literal_text import request, compile_contract, compile_contracts, order_literal

T = lambda s: re.findall(r'[^\W_]+', s.casefold(), re.UNICODE)
PRESERVE = ('The already declared inscription retains its complete character sequence, '
            'capitalization, punctuation and line arrangement on the already declared entrance-door glass.')
FIXED = 'A glazed entrance door carries BONJOUR in separate uppercase painted letters across its glass pane.'
QUERY = 'Photographic role: Show the exact word HELLO painted on the shop door glass.'

class LiteralTextTests(unittest.TestCase):
    def req(self, text):
        return request(text, analyze(text, T), T)
    def run_order(self, texts, query=QUERY):
        rows = [{'id': str(i), 'bm25': 9-i, 'cosine': .9-i/100, 'rrf': .1-i/1000} for i in range(len(texts))]
        original = copy.deepcopy(rows)
        result, trace = order_literal(rows, query, analyze(query, T), compile_contracts(dict(zip(map(str, range(len(texts))), texts)), T), T)
        self.assertEqual(rows, original)
        self.assertEqual({r['id'] for r in result}, {r['id'] for r in rows})
        self.assertEqual({r['id']: r for r in result}, {r['id']: r for r in rows})
        return result, trace
    def test_unquoted_value_has_real_offsets_and_carrier(self):
        r = self.req(QUERY)
        self.assertEqual(r['literal']['quote'], 'HELLO')
        self.assertEqual(QUERY[r['literal']['start']:r['literal']['end']], 'HELLO')
        self.assertEqual(r['carrier']['head'], 'glass')
    def test_quoted_case_spacing_and_punctuation_are_exact(self):
        q = 'Show the exact text "Hello,  World!" on the shop door glass.'
        self.assertEqual(self.req(q)['literal']['quote'], 'Hello,  World!')
    def test_unquoted_numerals(self):
        self.assertEqual(self.req('Show the exact numerals 42 on the painted wooden crate.')['literal']['quote'], '42')
    def test_object_open_is_not_an_inscription(self):
        self.assertIsNone(self.req('Show the open glass door with the shop inside.'))
    def test_multiple_literals_require_manual_assignment(self):
        self.assertIsNone(self.req(QUERY + ' Show the exact letters BYE on the side door glass.'))
    def test_negated_and_quoted_mentions_do_not_trigger(self):
        for q in ['Do not ' + QUERY, 'A scene, rather than show the exact word HELLO painted on the shop door glass.', 'Discuss "the exact word HELLO painted on the shop door glass".']:
            with self.subTest(q=q): self.assertIsNone(self.req(q))
    def test_carrier_cannot_be_borrowed_from_next_sentence(self):
        self.assertIsNone(self.req('Show the exact word HELLO painted. A hand rests on the shop door glass.'))
    def test_incomplete_unquoted_phrase_is_unsupported(self):
        self.assertIsNone(self.req('Show the exact phrase HELLO WORLD painted on the shop door glass.'))
    def test_unterminated_quotes_fail_closed(self):
        self.assertIsNone(self.req('Show the exact text "HELLO on the shop door glass.'))
    def test_source_preservation_contract_is_field_local(self):
        c = compile_contract(PRESERVE, T)
        self.assertEqual(c['preservation']['sequence']['quote'], 'complete character sequence')
        self.assertEqual(c['preservation']['carrier']['head'], 'glass')
        self.assertIsNone(compile_contract('A portrait of a person. ' + PRESERVE, T))
    def test_negative_or_quoted_source_cannot_supply_a_contract(self):
        for d in ['Do not use this: ' + PRESERVE, '"' + PRESERVE + '"']:
            with self.subTest(d=d): self.assertIsNone(compile_contract(d, T))
    def test_incomplete_preservation_does_not_imply_exact_case(self):
        self.assertIsNone(compile_contract(PRESERVE.replace('capitalization', 'color'), T))
    def test_preservation_and_wrong_literal_cannot_be_mixed(self):
        doc = PRESERVE[:-1] + ' while the door carries BONJOUR in painted letters.'
        self.assertIsNone(compile_contract(doc, T))
    def test_preservation_beats_context_match_and_conflict_goes_last(self):
        rows, trace = self.run_order([FIXED, 'A glass door with reflected branches.', PRESERVE, 'A shop entrance photograph.'])
        self.assertEqual([r['id'] for r in rows], ['2', '1', '3', '0'])
        self.assertTrue(trace['applied'])
        self.assertEqual(trace['conflicting']['0']['source']['fixed'][0]['quote'], 'BONJOUR')
        self.assertFalse(trace['native_approval'])
    def test_unrelated_carrier_does_not_promote_or_suppress(self):
        for q in ['Show the exact letters HELLO printed on the fabric banner.', 'Show the exact numerals 42 on the painted wooden crate.']:
            rows, trace = self.run_order([FIXED, PRESERVE], q)
            self.assertEqual([r['id'] for r in rows], ['0', '1'])
            self.assertFalse(trace['applied'])
    def test_no_positive_contract_preserves_original_order(self):
        rows, trace = self.run_order([FIXED, 'A shop window.'])
        self.assertEqual([r['id'] for r in rows], ['0', '1'])
        self.assertFalse(trace['applied'])
    def test_case_sensitive_fixed_literal_matching(self):
        rows, trace = self.run_order([FIXED.replace('BONJOUR', 'HELLO'), FIXED, PRESERVE])
        self.assertEqual([r['id'] for r in rows], ['0', '2', '1'])
        self.assertEqual(trace['compatible']['0']['kind'], 'fixed_exact_match')
        q = QUERY.replace('HELLO', 'Hello')
        rows, trace = self.run_order([FIXED.replace('BONJOUR', 'HELLO'), PRESERVE], q)
        self.assertEqual([r['id'] for r in rows], ['1', '0'])
    def test_head_and_two_carrier_terms_are_required(self):
        for q in [QUERY.replace('shop door glass', 'shop window glass'), QUERY.replace('shop door glass', 'shop glass door')]:
            rows, trace = self.run_order([FIXED, PRESERVE], q)
            self.assertEqual([r['id'] for r in rows], ['0', '1'])
            self.assertFalse(trace['applied'])
    def test_neutral_and_compatible_groups_keep_original_rrf_order(self):
        rows, trace = self.run_order(['A shop.', PRESERVE, 'A reflection.', PRESERVE])
        self.assertEqual([r['id'] for r in rows], ['1', '3', '0', '2'])
        self.assertEqual(trace['score_changes'], 0)
    def test_scene_location_is_not_part_of_the_bearing_carrier(self):
        for suffix in ['inside the photographed scene', 'within the photographed scene', 'in a photographed room']:
            q='Show the exact letters CAUTION printed on a fabric banner '+suffix+'.'
            r=self.req(q)
            self.assertEqual(r['carrier']['head'],'banner')
            self.assertEqual(r['carrier']['quote'],'a fabric banner')
    def test_surface_wrapper_retains_original_quote_and_carrier_identity(self):
        q='Show the exact numerals 007 on a painted wooden crate surface.'
        r=self.req(q)
        self.assertEqual(r['literal']['quote'],'007')
        self.assertEqual(r['carrier']['head'],'crate')
        self.assertEqual(r['carrier']['quote'],'a painted wooden crate surface')
        source=PRESERVE.replace('entrance-door glass','wooden crate')
        rows,trace=self.run_order(['A numbered prop.',source],q)
        self.assertTrue(trace['applied']);self.assertEqual(rows[0]['id'],'1')
    def test_generic_surface_alone_cannot_create_an_owned_carrier(self):
        self.assertIsNone(self.req('Show the exact numerals 007 on a wooden surface.'))
    def test_named_part_or_different_carrier_remains_separate(self):
        source=PRESERVE.replace('entrance-door glass','wooden crate')
        for carrier in ['wooden crate panel','wooden box surface','fabric banner surface']:
            rows,trace=self.run_order(['A numbered prop.',source],f'Show the exact numerals 007 on a {carrier}.')
            self.assertFalse(trace['applied']);self.assertEqual(rows[0]['id'],'0')
    def test_cloth_carrier_preserves_other_literal_without_object_transfer(self):
        source=PRESERVE.replace('entrance-door glass','fabric banner')
        rows,trace=self.run_order(['A generic cloth graphic.',source],
                                  'Show the exact text "Gate B-9" printed on a fabric banner inside the scene.')
        self.assertTrue(trace['applied']);self.assertEqual(rows[0]['id'],'1')
        self.assertEqual(trace['request']['literal']['quote'],'Gate B-9')

if __name__ == '__main__': unittest.main()
