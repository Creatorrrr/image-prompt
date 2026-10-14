"""Exact named phrase surfaces: structural coverage and pure retrieval projection.

Synthetic proofs here exercise contracts; they do not approve corpus meanings.
"""
import copy
import hashlib
import unittest

from tests.test_photo_semantic_evidence import (
    A, c, e, r, index, layout, face_source, seal, reattest,
)
from tests.test_photo_semantic_reference_units import reference
from tests.test_photo_candidate_corpus import fixture
from photo_native_pack import WorkingPack, finalize
from bm25f_retrieval import rank_bm25f


def phrase_source():
    data = face_source()
    record = data['candidates'][A]
    record['content'].update(phrase_en='Keep the underlit face readable.',
                             phrase_ko='같은 얼굴의 아래쪽 조명을 읽을 수 있게 유지한다.')
    seal(data, {'light_direction': ['underlight']})
    proof = record['content']['role_evidence']
    proof['source_units'] = [u for u in proof['source_units']
                             if u['pointer'] not in {'/content/phrase_en', '/content/phrase_ko'}]
    for key in ('phrase_en', 'phrase_ko'):
        proof['source_units'].append(reference('/content/'+key, record['content'][key], ['underlight']))
    reattest(data)
    return data


class NamedPhraseFieldTests(unittest.TestCase):
    def test_exact_two_named_fields_and_no_generic_expansion(self):
        record = fixture()['candidates'][A]
        record['content'].update(phrase_en='inside the orchard', phrase_ko='과수원 안에서',
                                 aliases=['alias phrase'], tags=['tag phrase'],
                                 unknown_extra='unreviewed extra', metadata={'en': 'metadata phrase'})
        self.assertEqual(e.primary_paths(record, 'base'),
                         {'/content/en', '/content/phrase_en', '/content/phrase_ko'})
        for pointer in ['/content/aliases/0', '/content/tags/0']:
            with self.assertRaises(ValueError):
                e.positive_string(record, pointer, realization_id='base')
        self.assertNotIn('unreviewed extra', index.text(record)[1])
        self.assertNotIn('metadata phrase', index.text(record)[1])

    def test_actual_missing_orchard_phrase_units_rejected(self):
        # Exact actual CID6673 strings. Only the coverage verifier is exercised;
        # nonsemantic test dispositions are not a semantic corpus judgement.
        record = {'content': {
            'en': 'a lush summer fruit orchard with vines, wet grass, natural paths, and green fruit trees',
            'ko': '덩굴과 열매가 우거진 여름 과수원',
            'phrase_en': 'deep inside a lush summer fruit orchard with vines, wet grass, natural paths, and green fruit trees',
            'phrase_ko': '덩굴과 젖은 풀, 자연스러운 길, 푸른 과실나무가 우거진 여름 과수원 깊숙한 곳에서'}}
        units = [{'realization_id': 'base', 'pointer': '/content/'+key, 'quote': value,
                  'disposition': 'nonsemantic', 'fact_refs': []}
                 for key, value in record['content'].items()]
        e._validate_source_units(record, {'source_units': units}, {}, 'base')
        for key in ('phrase_en', 'phrase_ko'):
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'complete source-unit'):
                e._validate_source_units(record, {'source_units': [u for u in units
                    if u['pointer'] != '/content/'+key]}, {}, 'base')

    def test_phrase_references_require_complete_same_rid_direct_anchor(self):
        data = phrase_source()
        c.validate(data)
        proof = data['candidates'][A]['content']['role_evidence']
        self.assertEqual(len(proof['facts']), 2)
        # A normal fact may be directly authored in this exact named field.
        proof['facts'][1].update(pointer='/content/phrase_en', quote='underlit face')
        proof['source_units'] = [u for u in proof['source_units'] if u['pointer'] != '/content/phrase_en']
        for u in proof['source_units']:
            if u['pointer'] == '/content/en':
                u['fact_refs'] = ['face']
        proof['source_units'].append({'realization_id': 'base', 'pointer': '/content/phrase_en',
            'quote': data['candidates'][A]['content']['phrase_en'], 'fact_refs': ['underlight'],
            'disposition': 'semantic'})
        reattest(data)
        c.validate(data)  # phrase_ko now references the distinct phrase_en direct anchor.
        proof['facts'][1]['realization_id'] = 'sibling'
        reattest(data)
        with self.assertRaises(ValueError):
            c.validate(data)

    def test_alias_metadata_unknown_cannot_anchor_phrase_reference(self):
        for key in ('aliases', 'tags', 'unknown_extra', 'metadata'):
            with self.subTest(key=key):
                data = phrase_source()
                record = data['candidates'][A]
                record['content'][key] = ['underlit face']
                proof = record['content']['role_evidence']
                proof['meaning_sha256'] = e.meaning_sha256(record)
                proof['facts'][1].update(pointer='/content/'+key+'/0', quote='underlit face')
                for unit in proof['source_units']:
                    if unit['pointer'] == '/content/en':
                        unit['fact_refs'] = ['face']
                proof['source_units'].append({'realization_id': 'base', 'pointer': '/content/'+key+'/0',
                    'quote': 'underlit face', 'fact_refs': ['underlight'], 'disposition': 'semantic'})
                reattest(data)
                with self.assertRaises(ValueError):
                    c.validate(data)

    def test_selected_primary_paths_never_borrow_sibling(self):
        record = {'content': {'phrase_en': 'common explicit phrase', 'realization_content': {
            'left': {'en': 'left local phrase'}, 'right': {'en': 'right local phrase'}}}}
        self.assertEqual(e.primary_paths(record, 'left'),
                         {'/content/phrase_en', '/content/realization_content/left/en'})
        with self.assertRaises(ValueError):
            e.positive_string(record, '/content/realization_content/right/en', realization_id='left')
        units = [reference('/content/phrase_en', 'common explicit phrase', ['sibling'], rid='left'),
            {'realization_id': 'left', 'pointer': '/content/realization_content/left/en',
             'quote': 'left local phrase', 'fact_refs': [], 'disposition': 'nonsemantic'}]
        sibling = {'id': 'sibling', 'realization_id': 'right',
                   'pointer': '/content/realization_content/right/en', 'quote': 'right local phrase'}
        with self.assertRaises(ValueError):
            e._validate_source_units(record, {'source_units': units}, {'sibling': sibling}, 'left')

    def test_phrase_source_and_source_unit_signature_binding(self):
        data = phrase_source()
        record = data['candidates'][A]
        compact = e.compact(record, data)
        old_meaning = e.meaning_sha256(record)
        record['content']['phrase_en'] += ' distinctly'
        self.assertNotEqual(e.meaning_sha256(record), old_meaning)
        with self.assertRaises(ValueError):
            c.validate(data)
        data = phrase_source()
        record = data['candidates'][A]
        proof = record['content']['role_evidence']
        old_signature = e.native_contract_sha256(proof)
        proof['source_units'][-1]['retained_constraint_rationale'] += ' Explicit fixture revision.'
        self.assertNotEqual(e.native_contract_sha256(proof), old_signature)
        reattest(data)
        c.validate(data)
        self.assertNotEqual(e.compact(record, data)['compact_sha256'], compact['compact_sha256'])

    def test_base_entry_full_authored_record_and_selected_projection_preserved(self):
        data = fixture()
        record = data['candidates'][A]
        record['content'].update(phrase_en='inside a blue-lit data center', phrase_ko='푸른 조명의 데이터 센터에서')
        before = copy.deepcopy(data)
        entry = c.entry(data, A)
        for key in ('en', 'phrase_en', 'phrase_ko'):
            self.assertEqual(entry[key], record['content'][key])
        pack = finalize(WorkingPack({'global_retrieval': {'role_proposals': {}}}, {}), data, [A], {})
        self.assertEqual(pack['candidate_pool'][A]['authored_record'], record)
        self.assertEqual(r.project_content(record, 'base'), {})
        self.assertEqual(data, before)
        record['effects'] = {'dimensions': [], 'properties': [], 'realizations': {'mode': 'one', 'branches': [
            {'id': rid, 'conditions': {}, 'context_terms': [], 'effects': {'dimensions': [], 'properties': []}}
            for rid in ('left', 'right')]}}
        record['content']['realization_content'] = {rid: {'en': rid+' exact text', 'ko': rid+' 한국어',
            'embedding_text': rid+' exact text', 'concept_units': [rid+' unit'], 'relations': []}
            for rid in ('left', 'right')}
        expected = {**copy.deepcopy(record['content']['realization_content']['left']),
                    'aliases': [], 'keywords': [], 'terms': [], 'paraphrases': [], 'concept_terms': [],
                    'phrase_en': 'left exact text', 'phrase_ko': 'left 한국어'}
        self.assertEqual(r.project_content(record, 'left'), expected)
        record.clear(); record.update(before['candidates'][A])
        self.assertEqual(data, before)

    def test_unique_phrase_retrievable_in_label_bm25_lane(self):
        data = fixture()
        data['candidates'][A]['content']['phrase_en'] = 'orchardphraseunique'
        other = 'cand_'+'b'*32
        data['candidates'][other] = copy.deepcopy(data['candidates'][A])
        data['candidates'][other]['id'] = other
        del data['candidates'][other]['content']['phrase_en']
        rows = rank_bm25f(index.lexical(data), {'frozen_core': 'orchardphraseunique'})
        self.assertEqual(rows[0]['document_id'], A)
        self.assertGreater(rows[0]['score'], 0)
        self.assertIn('orchardphraseunique', index.fields(data['candidates'][A])['labels'])

    def test_recipe_and_text_identity_only_exact_named_nonblank_strings(self):
        record = fixture()['candidates'][A]
        old_recipe, old_text = index.text(record)
        self.assertEqual(old_recipe, index.RECIPE)
        for extras in ({'unknown_extra': 'extra'}, {'phrase_en': ''}, {'phrase_ko': '  '},
                       {'phrase_en': ['not a named string']}, {'metadata': {'phrase_en': 'extra'}}):
            changed = copy.deepcopy(record); changed['content'].update(extras)
            self.assertEqual(index.text(changed), (old_recipe, old_text))
        for key in ('phrase_en', 'phrase_ko'):
            changed = copy.deepcopy(record); changed['content'][key] = 'new exact phrase'
            recipe, body = index.text(changed)
            self.assertEqual(recipe, 'photo-global-visual-phrase-text/v1')
            self.assertIn('new exact phrase', body)
            self.assertNotEqual(hashlib.sha256(body.encode()).digest(), hashlib.sha256(old_text.encode()).digest())
            # Even equal deduplicated text has a different explicit projection recipe.
            changed['content'][key] = changed['content']['en']
            self.assertEqual(index.text(changed), (index.PHRASE_RECIPE, old_text))
        self.assertEqual(index.QUERY_RECIPE, 'photo-independent-slot-query/v2')

    def test_vector_row_rejects_old_recipe_even_for_deduplicated_same_text(self):
        data = fixture()
        record = data['candidates'][A]
        recipe, body = index.text(record)
        row = {'id': A, 'recipe': recipe, 'text': body,
               'text_sha256': hashlib.sha256(body.encode()).hexdigest(),
               'vector': [1.0]+[0.0]*767}
        vectors = {'schema': index.SCHEMA, 'space': index.SPACE,
                   'corpus_sha256': c.digest(data), 'entries': {A: row}}
        index.validate(vectors, data)
        record['content']['phrase_en'] = record['content']['en']
        vectors['corpus_sha256'] = c.digest(data)
        self.assertEqual(index.text(record)[1], body)
        with self.assertRaisesRegex(ValueError, 'identity/text/recipe'):
            index.validate(vectors, data)
        row['recipe'] = index.PHRASE_RECIPE
        index.validate(vectors, data)
        record['content']['phrase_en'] = 'new explicit distinct phrase'
        vectors['corpus_sha256'] = c.digest(data)
        with self.assertRaisesRegex(ValueError, 'identity/text/recipe'):
            index.validate(vectors, data)

    def test_profile_projection_retains_its_existing_fields_and_recipe(self):
        record = {'record_kind': 'visual_profile', 'content': {
            'semantics': {'definition': 'An explicitly authored profile meaning.',
                          'visual_components': ['one authored component']}}}
        before_fields, before_text = index.fields(record), index.text(record)
        record['content'].update(phrase_en='unprojected profile extra', phrase_ko='별도 필드')
        self.assertEqual(index.fields(record), before_fields)
        self.assertEqual(index.text(record), before_text)
        self.assertEqual(before_text[0], index.PROFILE_RECIPE)


if __name__ == '__main__':
    unittest.main()
