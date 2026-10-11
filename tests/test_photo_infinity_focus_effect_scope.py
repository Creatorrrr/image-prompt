"""Distant lens focus preserves requested camera viewpoint properties."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import photo_candidate_semantics as semantics
import photo_contracts as contracts
import prompt_generator as generator


class PhotoInfinityFocusEffectScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with patch.object(generator, 'get_gemini_api_key', side_effect=AssertionError('No key access')), \
             patch.object(generator, 'embed_texts_with_gemini', side_effect=AssertionError('No embedding calls')):
            cls.data = generator.load_json(SKILL / 'assets/photo_prompt_tags.json')
        cls.entry = generator.candidate_pack_slot_entry_by_id(cls.data, 'focus', 'infinite_focus')
        cls.source = semantics.semantic_source(cls.entry, 'focus', cls.data['candidate_semantic_policy'])

    @staticmethod
    def lock(property_path, target='camera', dimension='camera'):
        return {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [
            {'dimension': dimension, 'target': target, 'property': property_path},
        ]}

    def allowed(self, property_path, target='camera', dimension='camera', source=None):
        source = self.source if source is None else source
        return contracts.property_effects_allowed(
            self.lock(property_path, target, dimension),
            source['affected_dimensions'], source.get('affected_properties', []),
        )

    def test_optional_focus_remains_available_under_requested_height_or_direction(self):
        for path in ('viewpoint.height', 'viewpoint.direction'):
            with self.subTest(protected_property=path):
                self.assertTrue(self.allowed(path))

    def test_requested_lens_focus_and_parent_properties_stay_protected(self):
        for path in ('focus.distance', 'focus', '*'):
            with self.subTest(protected_property=path):
                self.assertFalse(self.allowed(path))
        self.assertFalse(self.allowed('focus.distance', dimension='style'))
        self.assertTrue(self.allowed('focus.distance', target='secondary_camera'))

    def test_removing_the_authored_effect_reproduces_unrelated_viewpoint_rejection(self):
        prior_entry = copy.deepcopy(self.entry)
        prior_entry.pop('affected_dimensions')
        prior_entry.pop('affected_properties')
        prior_source = semantics.semantic_source(prior_entry, 'focus', self.data['candidate_semantic_policy'])
        self.assertFalse(self.allowed('viewpoint.height', source=prior_source))
        self.assertFalse(self.allowed('viewpoint.direction', source=prior_source))


if __name__ == '__main__':
    unittest.main()
