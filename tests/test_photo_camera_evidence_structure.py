"""Complete author inputs and compositional camera/negative-scope regressions."""
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

AUTHOR_INPUTS = ROOT / 'tests/fixtures/photo_prompt/camera_authoring_path_v1'
V2 = ROOT / 'tests/fixtures/photo_prompt/camera_owned_clause_independent_v2.json'
V2_HASH = '8ad46e1ac0448dddc3503299b4b5b24e786a04902c41143f455d9c960a5a9a07'


def read_inputs(name='en_up'):
    p = AUTHOR_INPUTS / name
    return {key: json.loads((p / (key + '.json')).read_text()) for key in
            ('request-envelope', 'authorial-core', 'creative-controls', 'embodiment-review')}


def normalize(inputs):
    return pg.normalize_authorial_core(inputs['authorial-core'],
        request_envelope=pg.normalize_request_envelope(inputs['request-envelope']),
        creative_control_snapshot=inputs['creative-controls'])


class CameraAuthoringStructureTests(unittest.TestCase):
    def test_complete_written_inputs_are_hash_frozen_without_helper_inference(self):
        manifest = json.loads((AUTHOR_INPUTS / 'AUTHORSHIP.json').read_text())
        for name, sha in manifest['files'].items():
            self.assertEqual(hashlib.sha256((AUTHOR_INPUTS / name).read_bytes()).hexdigest(), sha)
        for name in ('en_up', 'ko_down', 'en_open'):
            core = normalize(read_inputs(name))
            camera.camera_authoring_declaration(core, required=True)
            self.assertEqual(core['baseline_prompt_en'], read_inputs(name)['authorial-core']['baseline_prompt_en'])

    def test_requested_axes_use_only_their_owner_and_axis_evidence(self):
        core = normalize(read_inputs('ko_down'))
        old = copy.deepcopy(core)
        data = {'candidate_semantic_policy': {'slot_dimensions': {'camera_direction': ['camera'], 'camera_height': ['camera']}}}
        for axis in camera.CAMERA_AXES:
            query, fields = pg.core_slot_focus_queries(data, core, 'camera_' + axis)
            ev = core['semantic_assertions'][0]['evidence']
            self.assertEqual(query, [ev['owner_phrase'] + ' | ' + ev[axis + '_phrase']])
            self.assertEqual(fields, ['semantic_assertions.camera_axis_evidence'])
            self.assertNotIn(ev[('height' if axis == 'direction' else 'direction') + '_phrase'], query[0])
        self.assertEqual(core, old)

    def test_partial_lock_handoff_cannot_demote_the_existing_requested_axis(self):
        inputs = read_inputs()
        inputs['authorial-core']['semantic_assertions'][0]['axes']['direction_requirement'] = 'open'
        inputs['authorial-core']['semantic_assertions'][0]['axes']['capture_owner'] = 'unprescribed'
        inputs['authorial-core']['semantic_assertions'][0]['evidence'] = {}
        with self.assertRaisesRegex(ValueError, 'conflicts with existing requester property locks'):
            normalize(inputs)

    def test_missing_wrong_target_and_unbound_axis_evidence_are_rejected(self):
        for mutation in ('missing', 'target', 'literal', 'bound'):
            inputs = read_inputs()
            core = inputs['authorial-core']
            if mutation == 'missing': core['intent_lock']['semantic_anchors'].pop()
            if mutation == 'target': core['intent_lock']['semantic_anchors'][-1]['target'] = 'background_camera'
            if mutation == 'literal': core['semantic_assertions'][0]['evidence']['direction_phrase'] = 'a nonexistent direction phrase'
            if mutation == 'bound': core['semantic_assertions'][0]['evidence']['direction_phrase'] = 'small variations in the ceramic surface'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): normalize(inputs)

    def test_incomplete_and_list_valued_requirement_declarations_fail_closed(self):
        for value in (None, ['requested'], 'unknown'):
            inputs = read_inputs(); axes = inputs['authorial-core']['semantic_assertions'][0]['axes']
            if value is None: axes.pop('height_requirement')
            else: axes['height_requirement'] = value
            with self.subTest(value=value), self.assertRaises(ValueError): normalize(inputs)

    def test_unrequested_axis_does_not_require_camera_prose_or_create_locks(self):
        inputs = read_inputs('en_open'); core = normalize(inputs)
        self.assertEqual(core['semantic_assertions'][0]['evidence'], {})
        self.assertEqual(pg.intent_property_locks(core['intent_lock']), [])
        self.assertNotIn('camera', core['baseline_prompt_en'].lower())

    def test_review_protocol_metadata_cannot_opt_in_an_unrelated_camera_observation(self):
        core = normalize(read_inputs('en_open'))
        entry = {'id': 'optical_axis', 'label': 'Camera axis calibration',
                 'prompt': 'optical camera axis alignment', 'keywords': ['camera axis'],
                 'affected_dimensions': ['camera'], 'affected_properties': [],
                 'core_assertion_discovery': True}
        corpus = {'camera_direction': [entry]}
        index = pg._core_slot_index(json.dumps(corpus, sort_keys=True))
        data = {'candidate_semantic_policy': {'core_assertion_discovery': {
            'minimum_shared_content_words': 2, 'maximum_per_assertion': 4, 'maximum_candidates': 8}}}
        self.assertEqual(pg.candidate_pack_assertion_discovery(data, core,
            {'slot:camera_direction:optical_axis': entry}, index), [])

    def test_public_new_author_mode_rejects_omitted_declaration_before_data(self):
        inputs = read_inputs(); inputs['authorial-core']['semantic_assertions'] = []
        with tempfile.TemporaryDirectory() as folder:
            args = []
            for key, payload in inputs.items():
                path = Path(folder) / (key + '.json'); path.write_text(json.dumps(payload))
                args += ['--' + key + '-json', str(path)]
            with mock.patch.object(cli.generator, 'load_runtime_data') as load:
                with self.assertRaisesRegex(ValueError, 'separate direction/height declaration'):
                    cli.main(args + ['--new-author-camera-evidence'])
                load.assert_not_called()

    def test_redaction_does_not_resurrect_a_partial_owned_axis_query(self):
        core = normalize(read_inputs()); core['user_exclusions'] = ['upward']
        data = {'candidate_semantic_policy': {'slot_dimensions': {'camera_direction': ['camera']}}}
        self.assertEqual(pg.core_slot_focus_queries(data, core, 'camera_direction'), ([], []))

    def test_requester_excluded_axis_has_no_positive_handoff(self):
        inputs = read_inputs('en_open')
        request = inputs['authorial-core']['source_request'] + ' Do not tilt the capture camera downward.'
        envelope = inputs['request-envelope']
        envelope['request_text'] = request
        envelope['request_sha256'] = hashlib.sha256(request.encode()).hexdigest()
        envelope['active_spans'][0].update(text=request, end=len(request))
        controls = pg.creative_controls.resolve(request, context=inputs['creative-controls']['context'], seed=47)
        inputs['creative-controls'] = controls
        raw = inputs['authorial-core']
        raw['source_request'], raw['creative_controls_sha256'] = request, controls['canonical_sha256']
        for row in raw['interpretation_provenance'] + raw['intent_lock']['semantic_anchors']:
            row['source_text'] = request
        raw['user_exclusions'] = ['tilt the capture camera downward']
        raw['semantic_assertions'][0]['axes']['direction_requirement'] = 'excluded'
        core = normalize(inputs)
        data = {'candidate_semantic_policy': {'slot_dimensions': {'camera_direction': ['camera']}}}
        self.assertEqual(pg.core_slot_focus_queries(data, core, 'camera_direction'),
                         ([], ['semantic_assertions.camera_axis_excluded']))
        self.assertEqual(pg.intent_property_locks(core['intent_lock']), [])


class BoundedCameraStructureTests(unittest.TestCase):
    def extract(self, text, axis='direction'):
        return camera.legacy_camera_clauses({'subject': 'a folded paper ornament', 'baseline_prompt_en': text}, axis)

    def test_prior_v2_stays_frozen_and_is_a_development_control(self):
        self.assertEqual(hashlib.sha256(V2.read_bytes()).hexdigest(), V2_HASH)
        for row in json.loads(V2.read_text())['cases']:
            core = {'subject': row['subject'], 'baseline_prompt_en': row['baseline_prompt_en']}
            for axis in camera.CAMERA_AXES:
                actual = camera.legacy_camera_clauses(core, axis)
                with self.subTest(case=row['id'], axis=axis):
                    if row[axis]:
                        self.assertTrue(actual)
                        self.assertTrue(all(any(span in clause for clause in actual) for span in row[axis]))
                        self.assertTrue(all(row['expected_owner'] in clause for clause in actual))
                    else: self.assertEqual(actual, [])
                    self.assertTrue(all(clause in row['baseline_prompt_en'] for clause in actual))

    def test_np_modifier_predicates_and_shared_subject_coordination_compose(self):
        text = 'The camera that takes this picture is placed above the ornament and looks downward toward it, while the child points upward.'
        self.assertEqual(self.extract(text), ['The camera that takes this picture is placed above the ornament and looks downward toward it'])
        self.assertEqual(self.extract(text, 'height'), self.extract(text))

    def test_foreign_actor_or_foreign_lens_cannot_inherit_camera_ownership(self):
        for text in (
            'The camera taking this picture is below the ornament and the worker looks upward.',
            "The camera taking this picture is below the ornament, with the toy's lens aimed upward.",
            'For the camera recording this image, a worker raises a spare lens upward.',
            'The camera taking this picture is below the ornament and a lens on the table points upward.',
        ):
            with self.subTest(text=text): self.assertEqual(self.extract(text), [])

    def test_low_height_and_a_locally_owned_horizontal_lens_are_distinct_axes(self):
        text = 'The camera that records this scene rests ten centimeters above the ground, with its lens aimed straight ahead horizontally.'
        clauses = self.extract(text)
        self.assertEqual(clauses, self.extract(text, 'height'))
        self.assertTrue(clauses)
        self.assertNotIn('upward', clauses[0])

    def test_aiming_above_or_below_does_not_claim_camera_height(self):
        for command in ('Aim', 'Point', 'Tilt'):
            for direction in ('above', 'below'):
                text = f'{command} the camera {direction} the ornament.'
                with self.subTest(text=text):
                    self.assertEqual(self.extract(text, 'height'), [])
                    self.assertTrue(self.extract(text, 'direction'))

    def test_local_negative_tail_preserves_disjoint_positive_geometry(self):
        text = 'The camera capturing this image is close to the floor and faces horizontally forward, without an upward tilt.'
        expected = ['The camera capturing this image is close to the floor and faces horizontally forward']
        self.assertEqual(self.extract(text), expected)
        self.assertEqual(self.extract(text, 'height'), expected)

    def test_conflicting_negative_modal_or_unresolved_capture_stays_unresolved(self):
        for text in (
            'The camera taking this picture looks upward, without an upward tilt.',
            'The camera allegedly recording this scene points upward.',
            'The camera presumably making this image points upward.',
            'The camera taking this picture does not look upward and looks downward.',
            'The camera capturing this scene looks downward rather than upward.',
        ):
            with self.subTest(text=text): self.assertEqual(self.extract(text), [])

    def test_quoted_and_depicted_capture_descriptions_cannot_supply_owner(self):
        for text in (
            "A placard reads 'The camera taking this photo points upward'.",
            'The camera taking this photo is on display pointing upward.',
            'A displayed camera recording the scene is pointed upward.',
        ):
            with self.subTest(text=text): self.assertEqual(self.extract(text), [])


class PublicCameraAuthoringPathTests(unittest.TestCase):
    def test_full_frozen_author_inputs_run_public_cli_with_production_quality_layers(self):
        data = pg.load_runtime_data()
        self.assertIn(pg.QUALITY_LAYERS_DATA_KEY, data)
        with tempfile.TemporaryDirectory() as folder:
            for name in ('en_up', 'ko_down', 'en_open'):
                source = AUTHOR_INPUTS / name
                before = {p.name: p.read_bytes() for p in source.iterdir() if p.is_file()}
                output = Path(folder) / (name + '.json')
                args = [arg for key in ('request-envelope', 'authorial-core', 'creative-controls', 'embodiment-review')
                        for arg in ('--' + key + '-json', str(source / (key + '.json')))]
                with mock.patch.object(pg, 'load_runtime_data', return_value=data), \
                     mock.patch.object(pg, 'cached_gemini_client', side_effect=AssertionError('offline authoring path')), \
                     mock.patch.object(pg, 'embed_texts_with_gemini', side_effect=AssertionError('offline authoring path')):
                    self.assertEqual(cli.main(args + ['--new-author-camera-evidence', '--seed', '829', '--output-file', str(output)]), 0)
                pack = json.loads(output.read_text())[0]
                self.assertEqual(pack['core_retrieval']['candidate_adoption'], 'optional')
                self.assertLessEqual(sum(len(s['candidates']) for s in pack['slots'].values()), 64)
                self.assertEqual(pack['authorial_composition']['candidate_order'], 'seed_shuffled_non_preferential')
                self.assertEqual({p.name: p.read_bytes() for p in source.iterdir() if p.is_file()}, before)


if __name__ == '__main__': unittest.main()
