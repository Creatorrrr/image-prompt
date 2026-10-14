"""Explicit application clauses require whole-source disposition, not retrieval votes."""
import copy
import unittest

from tests.test_photo_semantic_evidence import A, c, e, index, face_source, seal, reattest
from tests.test_photo_semantic_reference_units import reference


def source():
    data = face_source()
    record = data['candidates'][A]
    record['content']['application_contract'] = 'Apply this lighting to the same explicitly established face.'
    seal(data, {'light_direction': ['underlight']})
    proof = record['content']['role_evidence']
    proof['source_units'] = [unit for unit in proof['source_units']
                             if unit['pointer'] != '/content/application_contract']
    proof['source_units'].append(reference('/content/application_contract',
        record['content']['application_contract'], ['face'], relation='same_selected_owner'))
    reattest(data)
    return data


class ApplicationContractFieldTests(unittest.TestCase):
    def test_only_the_exact_named_field_is_added_without_retrieval_expansion(self):
        data = face_source()
        record = data['candidates'][A]
        before = copy.deepcopy(index.fields(record)), index.text(record)
        old_paths = e.primary_paths(record, 'base')
        record['content'].update(application_contract='An explicit same-owner application.',
                                 arbitrary_contract='Unreviewed arbitrary text.',
                                 metadata={'application_contract': 'Nested arbitrary text.'})
        self.assertEqual(e.primary_paths(record, 'base'), old_paths | {'/content/application_contract'})
        self.assertEqual((index.fields(record), index.text(record)), before)

    def test_missing_whole_application_disposition_rejects_even_with_other_fields_covered(self):
        data = source()
        c.validate(data)
        proof = data['candidates'][A]['content']['role_evidence']
        proof['source_units'] = [unit for unit in proof['source_units']
                                 if unit['pointer'] != '/content/application_contract']
        reattest(data)
        with self.assertRaisesRegex(ValueError, 'complete source-unit'):
            c.validate(data)

    def test_app_reference_needs_its_exact_quote_and_an_independent_normal_anchor(self):
        for defect in ('short_local_quote', 'missing_direct_anchor', 'self_anchor'):
            data = source()
            proof = data['candidates'][A]['content']['role_evidence']
            app = next(unit for unit in proof['source_units'] if unit['pointer'] == '/content/application_contract')
            if defect == 'short_local_quote':
                app['quote'] = 'the same explicitly established face'
            elif defect == 'missing_direct_anchor':
                for unit in proof['source_units']:
                    if unit['disposition'] == 'semantic' and 'face' in unit['fact_refs']:
                        unit['fact_refs'] = [fid for fid in unit['fact_refs'] if fid != 'face']
            else:
                fact = next(fact for fact in proof['facts'] if fact['id'] == 'face')
                fact.update(pointer='/content/application_contract', quote='established face')
            reattest(data)
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                c.validate(data)

    def test_an_ordinary_direct_fact_can_use_its_own_exact_application_field(self):
        data = source()
        record = data['candidates'][A]
        proof = record['content']['role_evidence']
        fact = next(fact for fact in proof['facts'] if fact['id'] == 'face')
        fact.update(pointer='/content/application_contract', quote='established face')
        for unit in proof['source_units']:
            if unit['pointer'] == '/content/en':
                unit['fact_refs'] = [fid for fid in unit['fact_refs'] if fid != 'face']
        proof['source_units'] = [unit for unit in proof['source_units']
                                 if unit['pointer'] != '/content/application_contract']
        proof['source_units'].append({'realization_id': 'base', 'pointer': '/content/application_contract',
            'quote': record['content']['application_contract'], 'fact_refs': ['face'], 'disposition': 'semantic'})
        reattest(data)
        c.validate(data)

    def test_selected_application_never_borrows_a_sibling_or_routing_field(self):
        record = {'content': {'application_contract': 'The same common selected owner.',
            'realization_content': {'left': {'en': 'Left selected body.'},
                                    'right': {'en': 'Right selected body.'}}}}
        self.assertEqual(e.primary_paths(record, 'left'),
            {'/content/application_contract', '/content/realization_content/left/en'})
        with self.assertRaises(ValueError):
            e.positive_string(record, '/content/realization_content/right/en', realization_id='left')
        record['conditions'] = {'application_contract': 'Routing conditions are not positive evidence.'}
        with self.assertRaises(ValueError):
            e.positive_string(record, '/conditions/application_contract', realization_id='left')


if __name__ == '__main__':
    unittest.main()
