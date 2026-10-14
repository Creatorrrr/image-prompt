"""An explicitly selected primitive alternative cannot render another body."""
import copy
import unittest

from tests.test_photo_candidate_corpus import fixture, A
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_global_index as index
import photo_search_layout as layout
import prompt_generator as g


def source():
    data = fixture();record = data['candidates'][A]
    record['content'] = {'en': 'standing or walking', 'ko': '서 있거나 걷는',
        'embedding_text': 'standing or walking', 'aliases': ['standing or walking'],
        'keywords': ['walking'], 'concept_units': ['standing or walking'],
        'realization_content': {rid: {'en': en, 'ko': ko, 'embedding_text': en,
            'concept_units': [en], 'relations': []}
            for rid, en, ko in [('standing', 'a standing adult', '서 있는 성인'),
                               ('walking', 'a walking adult', '걷는 성인')]}}
    record['effects'] = {'dimensions': [], 'properties': [],
        'realizations': {'mode': 'one', 'branches': [
            {'id': rid, 'conditions': {}, 'context_terms': [],
             'effects': {'dimensions': ['pose'], 'properties': [
                 {'dimension': 'pose', 'target': 'main_subject', 'property': 'body.pose.' + rid}]}}
            for rid in ['standing', 'walking']]}}
    return data


class RealizationContentTests(unittest.TestCase):
    def test_selected_text_and_properties_exclude_the_other_primitive_choice(self):
        data = source();before = copy.deepcopy(data);c.validate(data)
        entry = c.entry(data, A, realization_id='standing')
        self.assertEqual(entry['en'], 'a standing adult')
        self.assertEqual(entry['ko'], '서 있는 성인')
        self.assertEqual(entry['concept_units'], ['a standing adult'])
        self.assertNotIn('walking', g.candidate_pack_entry_blob(entry, [entry['embedding_text']]))
        self.assertEqual(entry['affected_properties'][0]['property'], 'body.pose.standing')
        self.assertNotIn('realization_content', entry)
        self.assertEqual(data, before)

    def test_projection_does_not_add_or_duplicate_a_search_document_or_ranking_text(self):
        data = source();without = copy.deepcopy(data)
        without['candidates'][A]['content'].pop('realization_content')
        self.assertEqual(index.documents(data), index.documents(without))
        self.assertEqual(index.text(data['candidates'][A]), index.text(without['candidates'][A]))

    def test_lazy_guard_and_payload_select_identical_positive_text(self):
        data = source();record = data['candidates'][A]
        lazy = {**data, 'candidates': {A: layout.guard_record(record)}}
        for rid in r.ids(record):
            full, compact = c.entry(data, A, realization_id=rid), c.entry(lazy, A, realization_id=rid)
            self.assertEqual(g.candidate_pack_entry_blob(full, [full['embedding_text']]),
                             g.candidate_pack_entry_blob(compact, [compact['embedding_text']]))

    def test_foreign_missing_or_guard_overriding_primitive_text_is_rejected(self):
        for defect in ['missing', 'foreign', 'guard', 'identity', 'empty', 'unconditional']:
            data = source();record = data['candidates'][A];choices = record['content']['realization_content']
            if defect == 'missing':
                choices.pop('walking')
            elif defect == 'foreign':
                choices['invented'] = copy.deepcopy(choices['walking'])
            elif defect == 'guard':
                choices['standing']['conditions'] = {}
            elif defect == 'identity':
                choices['standing']['id'] = 'another-candidate'
            elif defect == 'empty':
                choices['standing']['concept_units'] = []
            else:
                record['effects'].pop('realizations')
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                c.validate(data)


if __name__ == '__main__':
    unittest.main()
