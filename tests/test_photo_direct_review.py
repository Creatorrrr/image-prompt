"""Integrity gates for authored direct review, without invoking a model."""
import copy
import importlib.util
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/direct_review.py'
spec = importlib.util.spec_from_file_location('direct_review', PATH)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
from tests.test_photo_candidate_corpus import fixture, A, B


def decision(data):
    record = data['candidates'][A]
    record['content'] = {'en': 'a glossy fabric surface', 'confounders': ['not a leather coat']}
    tag = 'wardrobe_style'
    data['slot_catalog'][tag]['dimensions'] = ['appearance']
    data['slot_catalog'][tag]['property_prefixes'] = ['wardrobe.']
    fact = {'pointer': '/content/en', 'quote': 'glossy fabric', 'dimension': 'appearance',
        'target': 'main_subject', 'property': 'wardrobe.style'}
    return {**review.binding(data, A), 'schema': review.SCHEMA, 'reviewer': 'Codex',
        'review_method': 'codex_direct_source_read', 'independent_human_review': False,
        'meaning_summary': 'Fixture judgement for contract rejection tests, not a corpus approval.',
        'recommended_kind': 'visual_option', 'corrections': [], 'roles': [{
            'slot_id': tag, 'semantic_role': data['slot_catalog'][tag]['semantic_role'],
            'scope': 'whole_record', 'realization_ids': ['base'], 'rationale': 'Authored fixture rationale.',
            'evidence': [fact]}], 'facts': [{**fact, 'realization_id': 'base'}],
        'rejected_boundaries': ['A negative coat example cannot supply a positive garment.'],
        'uncertainties': [], 'status': 'approved', 'all_roles_considered': True,
        'authored_decision': {'file': 'test.json', 'item': 1, 'sha256': 'b' * 64}, 'packet_sha256': 'c' * 64}


class DirectReviewTests(unittest.TestCase):
    def test_source_mutation_invalidates_decision(self):
        data = fixture(); row = decision(data)
        review.validate_decision(row, data)
        data['candidates'][A]['content']['en'] = 'matte cloth'
        with self.assertRaisesRegex(ValueError, 'changed after review'):
            review.validate_decision(row, data)

    def test_catalog_mutation_invalidates_decision(self):
        data = fixture(); row = decision(data)
        data['slot_catalog']['wardrobe_style']['description'] += ' changed'
        with self.assertRaisesRegex(ValueError, 'changed after review'):
            review.validate_decision(row, data)

    def test_transitive_reference_mutation_invalidates_decision(self):
        data = fixture()
        data['candidates'][B] = {**copy.deepcopy(data['candidates'][A]), 'id': B}
        data['candidates'][A]['content']['canonical_candidate_ref'] = B
        row = decision(data)
        # Preserve reference after the fixture's content replacement.
        data['candidates'][A]['content']['canonical_candidate_ref'] = B
        row.update(review.binding(data, A))
        data['candidates'][B]['conditions'] = {'requires_adult_context': True}
        with self.assertRaisesRegex(ValueError, 'changed after review'):
            review.validate_decision(row, data)

    def test_negative_quote_cannot_qualify_role(self):
        data = fixture(); row = decision(data)
        row['roles'][0]['evidence'][0].update(pointer='/content/confounders/0', quote='leather coat')
        with self.assertRaisesRegex(ValueError, 'not positive evidence'):
            review.validate_decision(row, data)

    def test_wrong_quote_is_rejected(self):
        data = fixture(); row = decision(data)
        row['roles'][0]['evidence'][0]['quote'] = 'blue coat'
        with self.assertRaisesRegex(ValueError, 'quote differs'):
            review.validate_decision(row, data)

    def test_wildcard_owner_cannot_be_approved(self):
        data = fixture(); row = decision(data)
        row['roles'][0]['evidence'][0]['target'] = '*'
        with self.assertRaisesRegex(ValueError, 'concrete'):
            review.validate_decision(row, data)

    def test_foreign_realization_cannot_be_approved(self):
        data = fixture(); row = decision(data)
        row['roles'][0]['realization_ids'] = ['invented_branch']
        with self.assertRaisesRegex(ValueError, 'role contract'):
            review.validate_decision(row, data)

    def test_unresolved_ambiguity_is_never_approved(self):
        data = fixture(); row = decision(data)
        row['uncertainties'] = [{'kind': 'visual_semantic_ambiguity', 'detail': 'Unknown carrier.'}]
        with self.assertRaisesRegex(ValueError, 'unresolved'):
            review.validate_decision(row, data)

    def test_diagnostic_cannot_gain_positive_roles(self):
        data = fixture(); row = decision(data)
        row.update(recommended_kind='diagnostic', status='diagnostic_reviewed')
        with self.assertRaisesRegex(ValueError, 'diagnostic cannot'):
            review.validate_decision(row, data)

    def test_external_model_result_is_not_direct_review(self):
        data = fixture(); row = decision(data)
        row['review_method'] = 'provider_text_review'
        with self.assertRaisesRegex(ValueError, 'direct reviewer'):
            review.validate_decision(row, data)

    def test_role_needs_matching_explicit_branch_fact(self):
        data = fixture(); row = decision(data)
        row['facts'][0]['target'] = 'background'
        with self.assertRaisesRegex(ValueError, 'explicitly authored branch fact'):
            review.validate_decision(row, data)

    def test_source_correction_requires_complete_exact_before_string(self):
        data = fixture(); row = decision(data)
        row['corrections'] = [{'pointer': '/content/en', 'before': 'glossy fabric',
            'after': 'matte fabric', 'reason': 'Incomplete before text is forbidden.'}]
        with self.assertRaisesRegex(ValueError, 'exact current text'):
            review.validate_decision(row, data)


if __name__ == '__main__':
    unittest.main()
