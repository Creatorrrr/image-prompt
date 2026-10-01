"""Keep existing narrative role bindings intact in actual final V6 semantics."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/narrative-unit-data-cleanup-20261001'
PUBLIC = ROOT / 'docs/research-evidence/photo-prompt/published-data-v6-surface-audit-20261001'
spec = importlib.util.spec_from_file_location('narrative_unit_surface', PUBLIC / 'replay_public_surfaces.py')
surface = importlib.util.module_from_spec(spec)
spec.loader.exec_module(surface)
import photo_candidate_semantics as semantics


class NarrativeUnitDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
        cls.data = surface.runtime_data()
        cls.rows = {(s, r['id']): r for s, rows in cls.data['slots'].items() for r in rows}
        cls.targets = [r for r in cls.frozen['inventory'] if r['decision'] == 'fix']
        cls.decision = json.loads((EVIDENCE / 'acceptance-decisions.json').read_text())
        cls.accepted_ids = set(cls.decision['accepted_ids'])
        cls.contract = json.loads((PUBLIC / 'generated-contract-result.json').read_text())

    def test_exact_frozen_inventory_independent_queries_and_budget(self):
        self.assertEqual(hashlib.sha256((EVIDENCE / 'frozen-inventory-queries.json').read_bytes()).hexdigest(),
                         '91b7ee50643c05af5370eff930808f55f18cff974a17b2e96d4ba30d8aa59d58')
        self.assertEqual(len(self.frozen['inventory']), 9)
        self.assertEqual(len(self.targets), 3)
        self.assertEqual(len(self.frozen['queries']), 22)
        self.assertEqual(sum(q['authorship'] == 'independent_reviewer' for q in self.frozen['queries']), 18)
        self.assertEqual(self.frozen['maximum_paid_calls'], 26)
        self.assertAlmostEqual(self.frozen['maximum_additional_cost_usd'], .0425984)
        self.assertEqual(self.frozen['automatic_retries'], 0)
        self.assertEqual(hashlib.sha256((EVIDENCE / 'acceptance-decisions.json').read_bytes()).hexdigest(),
                         'c0ed5fe34073754b91766bc108e7bb54374cb03b81673ab5946cc5929bbf61f5')
        self.assertEqual(self.accepted_ids, {'spirit_jurisdiction_narrative_core'})
        self.assertEqual(set(self.decision['reverted_to_baseline']),
                         {'management_world_narrative_core', 'media_mix_narrative_core'})

    def test_complete_current_raw_extension_has_only_one_accepted_unit(self):
        expected = json.loads((EVIDENCE / 'baseline-raw-extension.json').read_text())
        for target in self.targets:
            row = next(r for r in expected['slots'][target['slot']] if r['id'] == target['id'])
            self.assertEqual(row, target['before'])
            if target['id'] in self.accepted_ids:
                row['concept_units'] = [row['en']]
        current = json.loads((ASSETS / 'photo_prompt_cjk_worldbuilding_extension.json').read_text())
        self.assertEqual(current, expected)
        self.assertNotIn('maintenance_ref', current)

    def test_all_prior_fields_and_six_keeps_are_exact(self):
        for item in self.frozen['inventory']:
            with self.subTest(entry=item['id']):
                current = self.rows[item['slot'], item['id']]
                if item['id'] not in self.accepted_ids:
                    self.assertEqual(current, item['before'])
                else:
                    self.assertEqual(current, item['proposed_after'])
                    self.assertEqual({k: v for k, v in current.items() if k != 'concept_units'}, item['before'])
                    self.assertEqual(current['concept_units'], [item['before']['en']])

    def test_actual_final_pack_and_details_preserve_accepted_provenance_binding(self):
        for target in self.targets:
            if target['id'] not in self.accepted_ids:
                continue
            with self.subTest(entry=target['id']):
                slot, eid = target['slot'], target['id']
                old = surface.build_state(self.data, target['before'], slot, eid, self.contract)
                new = surface.build_state(self.data, self.rows[slot, eid], slot, eid, self.contract)
                self.assertIsNotNone(old['candidate'])
                self.assertNotIn('concept_units', old['candidate'])
                self.assertEqual(new['candidate']['concept_units'], [target['before']['en']])
                self.assertEqual(new['candidate']['concept_terms'], [target['before']['en']])
                self.assertEqual(new['candidate']['relations'], [])
                self.assertEqual(new['candidate']['affected_dimensions'], ['concept'])
                self.assertEqual(new['candidate']['adoption'], 'optional')
                self.assertEqual(new['candidate']['semantic_surface_version'], 'photo-candidate-semantic-surface/v1')
                self.assertIsNotNone(new['detail'])

    def test_rejected_rows_are_exact_baseline_and_explicitly_unresolved(self):
        for target in self.targets:
            if target['id'] in self.accepted_ids:
                continue
            with self.subTest(entry=target['id']):
                self.assertEqual(self.rows[target['slot'], target['id']], target['before'])
                self.assertNotIn('concept_units', self.rows[target['slot'], target['id']])
                self.assertIn('unresolved', self.decision['reverted_rationale'][target['id']])

    def test_immutable_full_proposal_preserves_all_three_attempted_units(self):
        expected = json.loads((EVIDENCE / 'baseline-raw-extension.json').read_text())
        for target in self.targets:
            row = next(r for r in expected['slots'][target['slot']] if r['id'] == target['id'])
            self.assertEqual(row, target['before'])
            row['concept_units'] = [row['en']]
        self.assertEqual(json.loads((EVIDENCE / 'full-proposal-raw-extension.json').read_text()), expected)

    def test_short_controls_already_export_complete_existing_labels(self):
        for item in self.frozen['inventory']:
            if item['decision'] != 'keep':
                continue
            with self.subTest(entry=item['id']):
                row = self.rows[item['slot'], item['id']]
                self.assertEqual(semantics.semantic_source(row, item['slot'], self.data['candidate_semantic_policy'])['concept_units'], [row['en']])

    def test_coexistence_is_preserved_without_global_exclusion(self):
        queries = self.frozen['queries']
        self.assertEqual(sum(q['kind'] == 'coexistence_control' for q in queries), 6)
        self.assertEqual(sum(q['kind'] == 'conflation_contrast' for q in queries), 6)
        coexistence = {q['family']: q for q in queries if q['kind'] == 'coexistence_control' and q['language'] == 'en'}
        self.assertIn('single fictional visual provenance', coexistence['spirit_jurisdiction']['assessment_role'])
        self.assertIn('share infrastructure', coexistence['management_world']['assessment_role'])
        self.assertIn('One adult performer', coexistence['media_mix']['assessment_role'])
        for target in self.targets:
            self.assertFalse(any(any(m['entry_id'] == target['id'] for m in b['member_candidates'])
                                 for b in self.data['candidate_bundles']))

    def test_prior_record_context_repair_is_unchanged(self):
        old = json.loads((EVIDENCE / 'baseline-raw-extension.json').read_text())
        row = next(r for r in old['slots']['capture_context'] if r['id'] == 'spirit_jurisdiction_capture_context')
        self.assertEqual(self.rows['capture_context', row['id']], row)
        self.assertEqual(row['concept_units'], [row['en']])


if __name__ == '__main__':
    unittest.main()
