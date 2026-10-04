"""Development controls for complete capture clauses, not new blind scores."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import generate_photo_prompt as cli
import photo_camera_evidence as camera
import prompt_generator as pg

AUTHOR = ROOT / 'tests/fixtures/photo_prompt/camera_authoring_path_v1/en_open'


def inputs_for(clause):
    rows = {key: json.loads((AUTHOR / (key + '.json')).read_bytes()) for key in
            ('authorial-core', 'request-envelope', 'creative-controls', 'embodiment-review')}
    rows['authorial-core']['semantic_assertions'] = []
    rows['authorial-core']['baseline_prompt_en'] += ' ' + clause
    rows['embodiment-review']['prompt_sha256'] = hashlib.sha256(
        rows['authorial-core']['baseline_prompt_en'].encode()).hexdigest()
    return rows


class CameraClausePolarityTests(unittest.TestCase):
    def extract(self, text, axis='direction'):
        return camera.legacy_camera_clauses({'subject': 'a linen blanket', 'baseline_prompt_en': text}, axis)

    def test_suffix_negation_cannot_be_projected_as_positive_direction(self):
        for suffix in ('under no circumstances', 'by no means', 'on no account',
                       'in no way', 'at no time', 'at no point', 'in no case', 'not at all', 'never'):
            with self.subTest(suffix=suffix):
                self.assertEqual(self.extract('The camera points upward ' + suffix + '.'), [])

    def test_same_capture_conflicting_coordinations_keep_the_tail_until_abstention(self):
        for clause in (
            'The camera looks upward and downward.',
            'The camera looks upward and looks downward.',
            'The camera looks upward and it faces downward.',
            'The camera looks upward and the camera points downward.',
            'The camera looks upward, with its lens aimed downward.',
            'The camera points left and right.',
            'The camera faces forward and backward.',
            'The camera points horizontally forward and backward.',
            'The camera points forward upward and downward.',
            'The camera points upward downward.',
            'The camera is above the shelf and looks upward and downward at once.',
        ):
            with self.subTest(clause=clause): self.assertEqual(self.extract(clause), [])

    def test_unselected_direction_choices_or_temporal_sequence_are_not_one_capture(self):
        for clause in (
            'The camera points upward or downward.',
            'The camera points upward or looks downward.',
            'The camera points upward or it looks downward.',
            'The camera points upward or its lens is aimed downward.',
            'The camera points upward or the camera is tilted downward.',
            'The camera points upward then downward.',
            'The camera points upward left or downward right.',
            'The camera points horizontally forward or backward.',
            'The camera points upward, alternatively downward.',
        ):
            with self.subTest(clause=clause): self.assertEqual(self.extract(clause), [])

    def test_local_uncertainty_and_negative_continuations_cannot_leave_positive_prefixes(self):
        for clause in (
            'The camera points upward perhaps.',
            'The camera points upward apparently.',
            'The camera allegedly taking this photograph points upward.',
            'The camera looks upward and might point downward.',
            'The camera looks upward and is possibly aimed downward.',
            'The camera looks upward and seems to face downward.',
            'The camera points upward with uncertainty.',
            'The camera points upward unless it faces downward.',
            'The camera points upward, with its lens not aimed upward.',
        ):
            with self.subTest(clause=clause): self.assertEqual(self.extract(clause), [])

    def test_foreign_subject_or_target_orientation_does_not_contradict_the_capture(self):
        for clause, expected in (
            ('The camera points horizontally forward toward a backward-pointing arrow.',
             'The camera points horizontally forward toward a backward-pointing arrow'),
            ('The camera points upward left toward a downward-facing arrow.',
             'The camera points upward left toward a downward-facing arrow'),
            ('The camera looks upward toward a downward-pointing arrow.',
             'The camera looks upward toward a downward-pointing arrow'),
            ('The camera looks upward and a worker faces downward.', 'The camera looks upward'),
            ('The camera looks upward while a worker might look downward.', 'The camera looks upward'),
            ('The camera looks upward and downward-facing arrows hang nearby.', 'The camera looks upward'),
            ('The camera looks upward and the worker looks downward under no circumstances.', 'The camera looks upward'),
        ):
            with self.subTest(clause=clause): self.assertEqual(self.extract(clause), [expected])

    def test_compatible_diagonal_and_repeated_predicates_preserve_complete_literal_clause(self):
        for clause in ('The camera points horizontally forward.',
                       'The camera points upward left.',
                       'The camera looks upward and left.',
                       'The camera looks upward and it points upward.',
                       'The camera is below the shelf and looks upward.',
                       'Keep the camera below the shelf and aim it horizontally forward.'):
            with self.subTest(clause=clause): self.assertEqual(self.extract(clause), [clause[:-1]])

    def test_actual_core_normalization_keeps_review_inputs_but_retrieval_abstains(self):
        for clause in ('The camera points upward under no circumstances.',
                       'The camera looks upward and downward.',
                       'The camera points horizontally forward and backward.',
                       'The camera points upward left or downward right.'):
            rows = inputs_for(clause); untouched = copy.deepcopy(rows)
            core = pg.normalize_authorial_core(rows['authorial-core'],
                request_envelope=pg.normalize_request_envelope(rows['request-envelope']),
                creative_control_snapshot=rows['creative-controls'])
            query, fields = pg.core_slot_focus_queries(
                {'candidate_semantic_policy': {'slot_dimensions': {'camera_direction': ['camera']}}}, core, 'camera_direction')
            self.assertEqual(self.extract(core['baseline_prompt_en']), [])
            self.assertNotIn('baseline_prompt_en.camera_clause', fields)
            self.assertFalse(any(clause[:-1] in q for q in query))
            self.assertEqual(core['baseline_prompt_en'], rows['authorial-core']['baseline_prompt_en'])
            self.assertEqual(rows, untouched)

    def test_two_camera_legacy_abstains_but_explicit_structured_capture_owner_remains(self):
        # Explicit independently declared capture evidence can select one camera;
        # a legacy clause cannot choose an unselected alternative or owner.
        core = {'semantic_assertions': [], 'subject': 'a linen blanket',
                'baseline_prompt_en': 'The camera points upward or downward.'}
        self.assertEqual(camera.legacy_camera_clauses(core, 'direction'), [])
        core = copy.deepcopy(json.loads((ROOT / 'tests/fixtures/photo_prompt/camera_authoring_path_v1/en_up/authorial-core.json').read_bytes()))
        core['baseline_prompt_en'] += ' Another camera points downward.'
        self.assertEqual(camera.legacy_camera_clauses(core, 'direction'), [])
        evidence = core['semantic_assertions'][0]['evidence']
        self.assertEqual(camera.authored_camera_query(core, 'direction'),
                         ([evidence['owner_phrase'] + ' | ' + evidence['direction_phrase']], ['semantic_assertions.camera_axis_evidence']))


class CameraClausePublicLegacyTests(unittest.TestCase):
    def test_legacy_public_cli_preserves_complete_inputs_and_optional_order_contract(self):
        data = pg.load_runtime_data()
        self.assertIn(pg.QUALITY_LAYERS_DATA_KEY, data)
        original = {p.name: p.read_bytes() for p in AUTHOR.glob('*.json')}
        for clause in ('The camera points upward under no circumstances.',
                       'The camera looks upward and downward.',
                       'The camera points horizontally forward and backward.',
                       'The camera points upward left or downward right.',
                       'The camera looks upward toward the blanket.'):
            rows = inputs_for(clause)
            with self.subTest(clause=clause), tempfile.TemporaryDirectory() as directory:
                folder = Path(directory); argv = []
                for name, payload in rows.items():
                    path = folder / (name + '.json'); path.write_text(json.dumps(payload))
                    argv += ['--' + name + '-json', str(path)]
                before = {p.name: p.read_bytes() for p in folder.glob('*.json')}
                output = folder / 'pack.json'
                with mock.patch.object(pg, 'load_runtime_data', return_value=data), \
                     mock.patch.object(pg, 'cached_gemini_client', side_effect=AssertionError('offline legacy control')), \
                     mock.patch.object(pg, 'embed_texts_with_gemini', side_effect=AssertionError('offline legacy control')):
                    self.assertEqual(cli.main(argv + ['--seed', '829', '--output-file', str(output)]), 0)
                pack = json.loads(output.read_bytes())[0]
                self.assertLessEqual(sum(len(s['candidates']) for s in pack['slots'].values()), 64)
                self.assertEqual(pack['core_retrieval']['candidate_adoption'], 'optional')
                self.assertEqual(pack['authorial_composition']['candidate_order'], 'seed_shuffled_non_preferential')
                for name, payload in before.items(): self.assertEqual((folder / name).read_bytes(), payload)
        self.assertEqual(original, {p.name: p.read_bytes() for p in AUTHOR.glob('*.json')})


if __name__ == '__main__': unittest.main()
