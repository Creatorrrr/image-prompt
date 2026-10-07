"""Data-only ownership specificity and unchanged source-intent contracts."""
from pathlib import Path
import hashlib
import json
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/motion-artifact-owner-data-cleanup-20261001'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator
import photo_candidate_semantics as semantics


class MotionArtifactOwnerDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
        cls.acceptance = json.loads((EVIDENCE / 'acceptance-decisions.json').read_text())
        # This oracle freezes the 20261001 ownership revision. Exclude only
        # later additive motion/ethereal paraphrase overlays and the dependent
        # cute context overlay; current merged data is tested independently.
        filenames = tuple(name for name in generator.RESEARCH_EXTENSION_FILENAMES
                          if name not in {'photo_prompt_motion_graphics_extension.json',
                                          'photo_prompt_cute_visual_forms_extension.json',
                                          'photo_prompt_ethereal_gothic_scene_extension.json',
                                          'photo_prompt_visual_grammar_extension.json'})
        inventory = generator.photo_source_manifest.SourceInventory.for_test(ASSETS, candidate_files=filenames)
        cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json', inventory=inventory)
        cls.rows = {(slot, row['id']): row for slot, rows in cls.data['slots'].items() for row in rows}

    def test_inventory_and_diagnostics_remain_frozen(self):
        self.assertEqual(hashlib.sha256((EVIDENCE / 'frozen-inventory-queries.json').read_bytes()).hexdigest(), '8268cabc6289f8be2acaf06215895cf7c66b55abb3948a4c221db09dcf2041f3')
        self.assertEqual(len(self.frozen['inventory']), 40)
        self.assertEqual(len(self.frozen['queries']), 20)
        self.assertEqual(sum(q['kind'] == 'positive' for q in self.frozen['queries']), 10)
        self.assertEqual(self.frozen['maximum_paid_calls'], 28)
        self.assertEqual(hashlib.sha256((EVIDENCE / 'acceptance-decisions.json').read_bytes()).hexdigest(), '73e4ab31bf7497bc205df57606df666cb54fe7a04bc6831e18ba45b2602b8e74')

    def test_thirty_six_retained_rows_are_exact(self):
        kept = [r for r in self.frozen['inventory'] if r['decision'] == 'keep' or r['id'] in self.acceptance['reverted_to_baseline']]
        self.assertEqual(len(kept), 36)
        for row in kept:
            self.assertEqual(self.rows[row['slot'], row['id']], row['before'], row['id'])

    def test_four_changes_are_only_component_owner_objects(self):
        fixed = [r for r in self.frozen['inventory'] if r['decision'] == 'fix' and r['id'] in self.acceptance['accepted_ids']]
        self.assertEqual(len(fixed), 4)
        for row in fixed:
            current = self.rows[row['slot'], row['id']]
            self.assertEqual(current, row['proposed_after'], row['id'])
            self.assertEqual({k: v for k, v in current.items() if k != 'relations'}, {k: v for k, v in row['before'].items() if k != 'relations'})
            self.assertEqual(len(current['relations']), 1)
            self.assertEqual({k: v for k, v in current['relations'][0].items() if k != 'object'}, {k: v for k, v in row['before']['relations'][0].items() if k != 'object'})

    def test_subject_and_light_motion_retain_stationary_references(self):
        person = self.rows['motion', 'pe_moving_subject_streak']
        lights = self.rows['motion', 'pe_light_trails']
        self.assertEqual(person['relations'][0]['object'], 'moving_subject_light_or_camera')
        self.assertEqual(lights['relations'][0]['object'], 'moving_subject_light_or_camera')
        self.assertIn('stationary scene anchors remain comparatively stable', person['concept_units'])
        self.assertIn('stationary objects remain distinguishable from that path', lights['concept_units'])

    def test_camera_sweep_radial_and_rotational_owners_are_distinct(self):
        expected = {'pe_camera_sweep': 'stationary_scene_edge_traces_in_image_plane', 'pe_radial_zoom': 'shared_radial_image_center', 'pe_rotation_arc': 'common_image_rotation_center'}
        for eid, owner in expected.items():
            self.assertEqual(self.rows['motion', eid]['relations'][0]['object'], owner)
        self.assertIn('central subject form remains more readable than outer traces', self.rows['motion', 'pe_radial_zoom']['concept_units'])

    def test_moire_owner_is_narrowed_and_restored_artifact_rows_stay_exact(self):
        expected = {'pe_jpeg_edge_blocks': 'block_edges_gradients_or_repeated_pattern', 'pe_gradient_banding': 'block_edges_gradients_or_repeated_pattern', 'pe_moire_on_pattern': 'repeated_pattern_image_regions'}
        for eid, owner in expected.items():
            self.assertEqual(self.rows['quality', eid]['relations'][0]['object'], owner)
        self.assertIn('the blocks remain image marks rather than scene objects', self.rows['quality', 'pe_jpeg_edge_blocks']['concept_units'])
        self.assertIn('band boundaries remain separate from object contours', self.rows['quality', 'pe_gradient_banding']['concept_units'])
        self.assertIn('interference remains localized to the patterned region', self.rows['quality', 'pe_moire_on_pattern']['concept_units'])

    def test_panning_flash_and_ambiguous_tonal_owners_stay_exact(self):
        expected = {'pe_tracked_subject_background_trace': 'tracked_subject_and_background', 'pe_flash_core_shutter_trace': 'ambient_trace_and_flash_endpoint'}
        for eid, owner in expected.items():
            self.assertEqual(self.rows['motion', eid]['relations'][0]['object'], owner)
        for eid in ['pe_negative_tones', 'pe_solarized_contours']:
            self.assertEqual(self.rows['quality', eid]['relations'][0]['object'], 'image_plane_tone_steps')

    def test_runtime_projection_retains_complete_effects_and_relations(self):
        for row in self.frozen['inventory']:
            current = self.rows[row['slot'], row['id']]
            projected = semantics.semantic_source(current, row['slot'], self.data['candidate_semantic_policy'])
            self.assertEqual(projected['relations'], current['relations'])
            self.assertEqual(current.get('affected_properties'), row['before'].get('affected_properties'))
            self.assertEqual(current.get('concept_units'), row['before'].get('concept_units'))

    def test_original_research_provenance_is_immutable(self):
        path = ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance/photo-editing-effects-20261001-v2.json'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), 'f6c9e6f18f2932b09520f66a73d1dba83afb4e1e34501f88ea9472092f9ecf27')
        self.assertNotIn('authored_source_sha256', json.loads(path.read_text()))


if __name__ == '__main__':
    unittest.main()
