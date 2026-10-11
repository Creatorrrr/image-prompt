"""Current prerequisites and prior authored meanings remain independently bound."""
import copy
import json
from pathlib import Path
import unittest

from tests.photo_source_history import before_stage05_subject_context, subject_context_transition

ROOT = Path(__file__).resolve().parents[1]


class PhotoSubjectContextSourceHistoryTests(unittest.TestCase):
    def test_all_reviewed_sources_reconstruct_the_bound_predecessor(self):
        transition = subject_context_transition()
        self.assertEqual(len(transition['sources']), 12)
        self.assertEqual(sum(len(s['updates']) for s in transition['sources'].values()), 139)
        self.assertEqual(sum(len(s['additions']) for s in transition['sources'].values()), 5)
        for name, item in transition['sources'].items():
            with self.subTest(source=name):
                current = json.loads((ROOT / item['source_file']).read_text())
                previous = before_stage05_subject_context(current, item['source_file'])
                for update in item['updates']:
                    row = next(r for r in previous['slots'][update['slot']] if r['id'] == update['id'])
                    old_fields = update['fields']
                    self.assertTrue(set(old_fields) <= {'primary_context_alternatives', 'tags'})
                    for field, change in old_fields.items():
                        self.assertEqual(field in row, change['before']['present'])
                        self.assertEqual(row.get(field), change['before']['value'])

    def test_undeclared_candidate_text_and_alias_edits_cannot_be_projected_away(self):
        item = subject_context_transition()['sources']['photo_prompt_natural_environment_extension.json']
        current = json.loads((ROOT / item['source_file']).read_text())
        for field, value in [('en', 'an unrelated storm device'), ('aliases', ['unreviewed alias'])]:
            altered = copy.deepcopy(current)
            altered['slots']['subject'][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, 'Unreviewed current source'):
                before_stage05_subject_context(altered, item['source_file'])

    def test_a_prerequisite_or_added_carrier_change_requires_another_sealed_transition(self):
        item = subject_context_transition()['sources']['photo_prompt_tags.json']
        current = json.loads((ROOT / item['source_file']).read_text())
        for entry_id, field, value in [
            (item['updates'][0]['id'], 'primary_context_alternatives', []),
            ('teacup_vessel_subject', 'en', 'a renamed coffee cup'),
        ]:
            altered = copy.deepcopy(current)
            next(r for r in altered['slots']['subject'] if r['id'] == entry_id)[field] = value
            with self.subTest(entry=entry_id), self.assertRaisesRegex(AssertionError, 'Unreviewed current source'):
                before_stage05_subject_context(altered, item['source_file'])

    def test_live_maintenance_reference_cannot_skip_its_predecessor(self):
        item = subject_context_transition()['sources']['photo_prompt_imaginal_extension.json']
        current = json.loads((ROOT / item['source_file']).read_text())
        current['maintenance_ref'] = item['prior_maintenance_ref']
        with self.assertRaisesRegex(AssertionError, 'maintenance chain changed'):
            before_stage05_subject_context(current, item['source_file'])
