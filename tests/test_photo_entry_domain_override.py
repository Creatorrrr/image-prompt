"""Catalog domain exceptions must survive entry filtering without erasing guards."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as generator
from photo_global_retrieval import guard_policy


class EntryDomainOverrideTests(unittest.TestCase):
    def setUp(self):
        self.entry = {'tags': ['human'], 'en': 'Existing disturbed chair and seat'}
        self.policy = {
            'subject_categories': ['human'],
            'allow_domains': ['visual_structure'],
            'allow_domains_override_subject_categories': True,
            'deny_domains': ['product'],
        }
        self.catalog = {'aftermath_trace': {
            'owners': ['entity'], 'applicability': self.policy}}
        self.contract = {
            'subject_category': 'object', 'domains': ['visual_structure'],
            'adult_allowed': False,
            'intent_constraints': {'subject_categories': ['object']},
        }

    def reason(self):
        return generator.entry_block_reason(
            self.entry, 'aftermath_trace', self.contract, catalog=self.catalog)

    def test_exact_catalog_exception_matches_policy_and_survives_entry_filter(self):
        self.assertTrue(guard_policy(self.policy, self.contract))
        self.assertIsNone(self.reason())

    def test_missing_wrong_or_disabled_exception_preserves_typed_filter(self):
        for change in [
            {'domains': []}, {'domains': ['other']},
        ]:
            with self.subTest(change=change):
                self.contract.update(change)
                self.assertEqual(self.reason(), 'typed_nonhuman_request')
        self.contract['domains'] = ['visual_structure']
        for field, value in [
            ('allow_domains_override_subject_categories', False),
            ('allow_domains', []),
        ]:
            with self.subTest(field=field):
                original = copy.deepcopy(self.policy)
                self.policy[field] = value
                self.assertEqual(self.reason(), 'typed_nonhuman_request')
                self.policy.clear()
                self.policy.update(original)

    def test_actor_owner_is_still_typed_even_when_policy_allows_domain(self):
        self.catalog['aftermath_trace']['owners'] = ['actor']
        self.assertEqual(self.reason(), 'typed_nonhuman_request')

    def test_entry_tags_cannot_create_a_catalog_exception(self):
        self.entry['allow_domains_override_subject_categories'] = True
        self.entry['allow_domains'] = ['visual_structure']
        self.policy.pop('allow_domains_override_subject_categories')
        self.assertEqual(self.reason(), 'typed_nonhuman_request')

    def test_no_people_and_adult_restrictions_remain(self):
        self.contract['intent_constraints']['no_people'] = True
        self.assertEqual(self.reason(), 'explicit_no_people')
        self.contract['intent_constraints'].pop('no_people')
        self.entry['tags'].append('adult')
        self.assertEqual(self.reason(), 'adult_not_allowed')

    def test_exception_does_not_override_independent_domain_or_subject_denials(self):
        self.contract['domains'].append('product')
        self.assertEqual(generator.slot_block_reason(
            {'slot_catalog': self.catalog}, 'aftermath_trace', self.contract),
            'request_domain_denied')
        self.assertFalse(guard_policy(self.policy, self.contract))
        self.contract['domains'] = ['visual_structure']
        self.policy['deny_subject_categories'] = ['object']
        self.assertEqual(generator.slot_block_reason(
            {'slot_catalog': self.catalog}, 'aftermath_trace', self.contract),
            'subject_category_denied')


if __name__ == '__main__':
    unittest.main()
