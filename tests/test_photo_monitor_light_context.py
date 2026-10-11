"""A declared monitor can illuminate human and object primary subjects."""
import copy
from pathlib import Path
import unittest
from unittest.mock import patch

from tests import photo_prompt_fixtures as fixtures
import prompt_generator as generator

ASSETS = Path(__file__).resolve().parents[1] / 'skills/photo-prompt-image-generator/assets'


class PhotoMonitorLightContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with patch.object(generator, 'get_gemini_api_key', side_effect=AssertionError('No key access')), \
             patch.object(generator, 'embed_texts_with_gemini', side_effect=AssertionError('No embedding calls')):
            cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
            cls.data[generator.QUALITY_LAYERS_DATA_KEY] = generator.load_quality_layers(ASSETS / 'photo_prompt_quality_layers.json')
        cls.entry = generator.candidate_pack_slot_entry_by_id(cls.data, 'light_type', 'monitor_glow')

    def inputs(self, category='object', *, typed=True, location='a dim office beside a monitor', excluded=False):
        subject = 'one adult woman' if category == 'human' else 'one white ceramic cup'
        request = f'Photograph {subject} in {location}; other photographic choices are free.'
        if excluded:
            request += ' Exclude monitor glow.'
        baseline = (f'A photograph shows {subject} in {location}. The primary subject stays clearly '
            'separate from the surrounding desk and background. Soft local illumination reveals the '
            'visible surfaces without changing their material identity. A stable camera view retains '
            'a quiet ordinary room, a supported primary subject and distinct surrounding objects '
            'within one coherent photographic frame.')
        raw = fixtures.core(request, subject=subject, setting=location, event='a supported subject remains in the room',
            interpreted_intent='A source-owned office photographic study',
            visual_priorities=('separate surrounding objects', 'coherent photographic frame'),
            baseline_prompt_en=baseline,
            anchor_evidence=('A photograph shows', subject, 'a supported primary subject'),
            exclusions=('monitor glow',) if excluded else ())
        if typed:
            raw['semantic_assertions'] = [{'assertion_id': 'primary_subject', 'dimension': 'subject',
                'polarity': 'required', 'source_span_ids': ['scope_1'], 'affected_dimensions': ['subject'],
                'axes': {'subject_category': category}, 'evidence': {'subject': subject}}]
        controls = generator.creative_controls.resolve(request,
            context={'subject_category': 'human' if category == 'human' else 'nonhuman', 'no_people': False},
            overrides={'sensual': 0, 'fetish': 0, 'surreal': 0, 'creativity': 1}, seed=73)
        raw['creative_controls_sha256'] = controls['canonical_sha256']
        core = generator.normalize_authorial_core(raw,
            request_envelope=generator.normalize_request_envelope(fixtures.envelope(request)),
            creative_control_snapshot=controls)
        contract, picked = generator.frozen_core_context(self.data, core, controls)
        self.assertFalse(contract['no_people'])
        return core, contract, picked

    def allowed(self, inputs, *, entry=None, data=None):
        return generator.core_slot_entry_eligible(self.data if data is None else data,
            *inputs, 'light_type', self.entry if entry is None else entry)

    def prior_context_rule_data(self):
        data = {**self.data, 'coherence_rules': copy.deepcopy(self.data['coherence_rules'])}
        rule = next(row for row in data['coherence_rules']['slot_context_rules'] if row['id'] == 'monitor_glow_needs_tech')
        rule['requires_context_any'].remove('monitor')
        return data

    def test_both_source_conditions_are_needed_for_a_declared_monitor_object_scene(self):
        inputs = self.inputs()
        self.assertTrue(self.allowed(inputs))
        prior_entry = copy.deepcopy(self.entry)
        prior_entry['requires_primary_any_tags'].remove('monitor')
        self.assertFalse(self.allowed(inputs, entry=prior_entry))
        self.assertFalse(self.allowed(inputs, data=self.prior_context_rule_data()))

    def test_typed_legacy_humans_and_existing_technology_context_keep_monitor_light(self):
        for typed in (True, False):
            for location in ('a dim office beside a monitor', 'a quiet technology laboratory'):
                with self.subTest(typed=typed, location=location):
                    inputs = self.inputs('human', typed=typed, location=location)
                    self.assertTrue(self.allowed(inputs))
                    if location == 'a quiet technology laboratory':
                        prior_entry = copy.deepcopy(self.entry)
                        prior_entry['requires_primary_any_tags'].remove('monitor')
                        self.assertTrue(self.allowed(inputs, entry=prior_entry, data=self.prior_context_rule_data()))

    def test_missing_or_explicitly_excluded_monitor_stays_blocked(self):
        self.assertFalse(self.allowed(self.inputs(location='a quiet indoor room')))
        self.assertFalse(self.allowed(self.inputs(excluded=True)))


if __name__ == '__main__':
    unittest.main()
