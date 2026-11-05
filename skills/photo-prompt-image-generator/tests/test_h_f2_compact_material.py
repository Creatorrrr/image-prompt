"""Compact material presentation keeps issued identities and source literals."""
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
NATIVE = os.environ.get('PHOTO_H_F2_TEST_NATIVE')
if NATIVE:
    sys.path.insert(0, str(Path(NATIVE) / 'scripts'))
    sys.path.insert(0, str(SKILL / 'runtime-overlays/compact-material/scripts'))
    import photo_h_f2_workflow as workflow
    import photo_h_f2_receipts as receipts
    import compose_pack_view


@unittest.skipUnless(NATIVE, 'requires installed H-F2 dependencies')
class CompactMaterialTest(unittest.TestCase):
    def project(self, native, units, conditions=None):
        with patch.object(workflow.canonical, 'native', return_value=native), \
             patch.object(workflow.canonical, 'units', return_value=units):
            return workflow.compact_material({'conditions': conditions or {}}, {'cid': 'cand_x', 'rid': 'base'})

    def test_exact_english_contract_and_conditions(self):
        actual = self.project({'application_contract': 'Keep the relation.'},
                              {'/content/en': 'An adult faces the group.',
                               '/content/ko': '원문',
                               '/content/application_contract': 'Keep the relation.'},
                              {'requires_adult_context': True})
        self.assertEqual(actual, {'candidate_id': 'cand_x', 'meaning': 'An adult faces the group.',
                                  'conditions': {'requires_adult_context': True},
                                  'application_contract': 'Keep the relation.'})

    def test_components_are_not_rewritten_or_omitted_when_english_absent(self):
        actual = self.project({}, {'/content/components/0/concept_units/0': 'First owner.',
                                   '/content/components/1/concept_units/0': 'Second owner.',
                                   '/content/embedding_text': 'Search keywords.'})
        self.assertEqual(actual, {'candidate_id': 'cand_x', 'meaning': 'First owner.\nSecond owner.',
                                  'conditions': {}})

    def test_nested_conditions_are_copied_without_rewriting(self):
        conditions = {'for_any': ['human'], 'native_guards': {'rules': [
            {'kind': 'frozen_value', 'value': {'type': 'text', 'value': 'phone'}}]}}
        actual = self.project({}, {'/content/en': 'A person uses a phone.'}, conditions)
        self.assertEqual(actual['conditions'], conditions)
        actual['conditions']['native_guards']['rules'][0]['value']['value'] = 'changed'
        self.assertEqual(conditions['native_guards']['rules'][0]['value']['value'], 'phone')

    def test_missing_meaning_fails_closed(self):
        with self.assertRaises(ValueError):
            self.project({}, {'/content/embedding_text': 'keywords'})

    def test_material_view_includes_exact_source_conditions(self):
        conditions = {'requires_adult_context': True, 'for_any': ['human']}
        source = {'conditions': conditions}
        packet = {'goals': {'topic': {'candidates': [{'cid': 'cand_x', 'rid': 'base'}]}},
                  'sources': {'cand_x': source},
                  'query_set': {'query_scopes': {'topic': 'slot'}}}
        with patch.object(receipts, 'verify_bound', return_value=packet), \
             patch.object(workflow.canonical, 'native', return_value={}), \
             patch.object(workflow.canonical, 'units', return_value={'/content/en': 'An adult.'}), \
             patch.object(workflow, 'value', return_value={'contract_version': 'photo-validation-context/v1'}), \
             patch.object(compose_pack_view, 'build_view', return_value={}):
            view = workflow.view({})
        self.assertEqual(view['schema'], 'photo-h-f2-compact-material-view/v2')
        self.assertEqual(view['materials']['topic'][0], {
            'candidate_id': 'cand_x', 'meaning': 'An adult.', 'conditions': conditions})
        self.assertEqual(view['additional_search_calls'], 0)

    def test_decision_binding_is_automatic_and_checks_foreign_values(self):
        packet = {'goals': {'topic': {'candidates': [
            {'cid': 'cand_x', 'rid': 'base', 'source_sha256': 'source'}]}}}
        decision = {'slot': 'topic', 'candidate_id': 'cand_x', 'use': 'skip', 'rationale': 'not relevant'}
        with patch.object(receipts, 'verify_bound', return_value=packet):
            workflow.bind_material_decisions({}, {'h_f2_material_decisions': [decision]})
            self.assertEqual((decision['realization_id'], decision['source_sha256']), ('base', 'source'))
            decision['source_sha256'] = 'other'
            with self.assertRaises(ValueError):
                workflow.bind_material_decisions({}, {'h_f2_material_decisions': [decision]})


if __name__ == '__main__':
    unittest.main()
