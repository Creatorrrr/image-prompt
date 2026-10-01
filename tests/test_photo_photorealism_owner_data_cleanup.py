"""Image-layer ownership with intact conditions and versioned source binding."""
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/photorealism-owner-data-cleanup-20261001'
SOURCE = ASSETS / 'photo_prompt_photorealism_elements_extension.json'
MAINTENANCE = ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator
import photo_candidate_semantics as semantics


class PhotorealismOwnerDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
        cls.acceptance = json.loads((EVIDENCE / 'acceptance-decisions.json').read_text())
        cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.rows = {(slot, row['id']): row for slot, rows in cls.data['slots'].items() for row in rows}

    def test_inventory_and_primary_diagnostics_are_frozen(self):
        self.assertEqual(hashlib.sha256((EVIDENCE / 'frozen-inventory-queries.json').read_bytes()).hexdigest(), '5933a0670c24b6a234c744f7675b26280981345e9020b9b89c2f43042572af0d')
        self.assertEqual(len(self.frozen['inventory']), 19)
        self.assertEqual(sum(q['kind'] == 'positive' for q in self.frozen['queries']), 4)
        self.assertEqual(sum(q['kind'] == 'near_miss' for q in self.frozen['queries']), 3)
        self.assertEqual(self.frozen['maximum_paid_calls'], 24)
        self.assertEqual(hashlib.sha256((EVIDENCE / 'acceptance-decisions.json').read_bytes()).hexdigest(), 'ecad6b01809f784c7dc275d20efb1ffa599bf851d1c5e7458978249af42eb415')
        self.assertEqual(self.acceptance['accepted_ids'], ['pr_jpeg_edge_blocking_candidate'])

    def test_historical_rubric_inputs_remain_unexecuted_exploratory_records(self):
        path = ROOT / 'docs/research-evidence/photo-prompt/photorealism-elements-20260923/evaluation-cases.jsonl'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), 'dff7dbdd8419ab40df88dc29e8eb21a2c5397a7eced2622edb8279eb475977cc')
        originals = {r['id']: r for line in path.read_text().splitlines() if line.strip() for r in [json.loads(line)]}
        historical = [q for q in self.frozen['queries'] if q['kind'] == 'historical_diagnostic']
        self.assertEqual(len(historical), 12)
        for query in historical:
            original = query['historical_record']
            self.assertEqual(original, originals[original['id']])
            self.assertEqual(query['query'], original['input'])
            self.assertEqual(original['execution_status'], 'not_run')
            self.assertEqual(original['result'], 'unscored')

    def test_eighteen_keeps_and_all_non_owner_fields_are_exact(self):
        kept = [r for r in self.frozen['inventory'] if r['decision'] == 'keep' or r['id'] in self.acceptance['reverted_to_baseline']]
        self.assertEqual(len(kept), 18)
        for row in self.frozen['inventory']:
            current = self.rows[row['slot'], row['id']]
            expected = row['proposed_after'] if row['id'] in self.acceptance['accepted_ids'] else row['before']
            self.assertEqual(current, expected)
            self.assertEqual({k: v for k, v in current.items() if k != 'relations'}, {k: v for k, v in row['before'].items() if k != 'relations'})
            if row['decision'] == 'keep':
                self.assertEqual(current, row['before'])
            else:
                self.assertEqual({k: v for k, v in current['relations'][0].items() if k != 'object'}, {k: v for k, v in row['before']['relations'][0].items() if k != 'object'})

    def test_deferred_noise_owner_keeps_original_conditions(self):
        row = self.rows['grain_profile', 'pr_shadows_local_digital_noise_candidate']
        self.assertEqual(row['relations'][0]['object'], 'the selected visible subject and its directly related scene surfaces')
        self.assertTrue(row['en'].startswith('If the selected digital capture is dim,'))
        self.assertIn('fine luminance or chroma noise concentrates in darker regions', row['concept_units'])
        self.assertIn('critical subject edges and face remain readable', row['concept_units'])

    def test_compression_owner_keeps_explicit_context_and_local_edges(self):
        row = self.rows['format', 'pr_jpeg_edge_blocking_candidate']
        self.assertEqual(row['relations'][0]['object'], 'high_contrast_edges_of_the_compressed_image')
        self.assertIn('a file screen or repost context is explicit', row['concept_units'])
        self.assertIn('slight ringing or blocking sits near high-contrast edges', row['concept_units'])
        self.assertIn('compression does not conceal the main gesture', row['concept_units'])

    def test_deferred_film_owner_keeps_original_two_layer_conditions(self):
        row = self.rows['film_emulation', 'pr_film_grain_print_scan_scope_candidate']
        self.assertEqual(row['relations'][0]['object'], 'the selected visible subject and its directly related scene surfaces')
        self.assertIn('grain belongs to the photographic picture area', row['concept_units'])
        self.assertIn('any specks remain on the print or scan layer', row['concept_units'])
        self.assertIn('the look does not imply an actual film capture history', row['concept_units'])
        self.assertTrue(any(q['assessment_role'] == 'grain without required print/dust control' for q in self.frozen['queries']))

    def test_physical_print_and_mixed_surveillance_camcorder_scopes_stay_exact(self):
        for eid in ['pr_instant_print_material_object_candidate', 'pr_fixed_surveillance_observation_candidate', 'pr_camcorder_still_temporal_container_candidate']:
            row = next(r for r in self.frozen['inventory'] if r['id'] == eid)
            self.assertEqual(self.rows[row['slot'], eid], row['before'])
        physical = self.rows['prop', 'pr_instant_print_material_object_candidate']
        self.assertIn('card thickness edges and hand support are visible', physical['concept_units'])

    def test_runtime_relation_projection_preserves_each_complete_component(self):
        for row in self.frozen['inventory']:
            current = self.rows[row['slot'], row['id']]
            projected = semantics.semantic_source(current, row['slot'], self.data['candidate_semantic_policy'])
            self.assertEqual(projected['relations'], current['relations'])
            self.assertEqual(current['concept_units'], row['before']['concept_units'])
            self.assertEqual(current['affected_dimensions'], row['before']['affected_dimensions'])

    def test_current_source_binding_is_versioned_without_rewriting_original(self):
        old_path = MAINTENANCE / 'photo_prompt_photorealism_elements_extension.json'
        self.assertEqual(hashlib.sha256(old_path.read_bytes()).hexdigest(), '95c15bfffeaaabb7f2b3cf5364ff560482bf4910628214958da0143140b6b81f')
        old = json.loads(old_path.read_text())
        raw = json.loads(SOURCE.read_text())
        ref = raw.pop('maintenance_ref')
        current = json.loads((MAINTENANCE / (ref['record_id'] + '.json')).read_text())
        self.assertNotEqual(ref['record_id'], old['record_id'])
        self.assertEqual(semantics.digest(raw), current['authored_source_sha256'])
        self.assertEqual(semantics.digest(current), ref['sha256'])
        self.assertEqual(current['maintenance_only']['source_revision']['accepted_candidate_ids'], self.acceptance['accepted_ids'])
        self.assertEqual({k: v for k, v in current['maintenance_only'].items() if k != 'source_revision'}, old['maintenance_only'])


if __name__ == '__main__':
    unittest.main()
