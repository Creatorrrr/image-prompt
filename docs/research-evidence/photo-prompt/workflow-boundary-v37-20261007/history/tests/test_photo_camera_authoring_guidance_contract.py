"""Pure camera-contract witnesses; no candidate DATA or runtime imports.

These are new synthetic fixtures, not reconstructions of lost experiment inputs.
"""
from __future__ import annotations
import ast
import copy
from pathlib import Path
import re
import unittest

SOURCE = Path(__file__).resolve().parents[1] / 'skills/photo-prompt-image-generator/scripts'
NS = {'re': re}
exec(compile((SOURCE / 'photo_contracts.py').read_text(), str(SOURCE / 'photo_contracts.py'), 'exec'), NS)


def load_pure(filename, names):
    rows = [node for node in ast.parse((SOURCE / filename).read_text()).body
            if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in rows} == names
    future = ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0)
    module = ast.fix_missing_locations(ast.Module(body=[future] + rows, type_ignores=[]))
    exec(compile(module, str(SOURCE / filename), 'exec'), NS)


load_pure('prompt_generator.py', {'normalize_intent_lock', 'normalize_list', 'clean_spaces',
    'authorial_request_content_words', 'request_envelope_active_texts', 'request_scope_contains',
    'authorial_core_intent_dimension_scope'})
NS.update(CAMERA_AXES=('direction', 'height'), AUTHORING_MARKER='camera_axis_review_v1')
load_pure('photo_camera_evidence.py', {'camera_authoring_declaration', 'require_camera_evidence'})


def fixture(requested=('direction', 'height'), *, whole=False, absent=False):
    text = 'An ordinary still-life photograph of a ceramic vase resting on a wooden table'
    phrases = {'direction': 'looks from the side', 'height': 'at waist height'}
    camera = ('The camera looks from the side at waist height' if len(requested) == 2
              else 'The camera looks from the side' if 'direction' in requested
              else 'The camera is at waist height' if 'height' in requested else '')
    if whole:
        camera += ' with a level 50 mm lens four meters away; keep the whole camera setup fixed'
    if camera:
        text += '. ' + camera
    anchors = [{'anchor_id': name, 'dimension': name, 'source_text': phrase, 'prompt_evidence': phrase}
               for name, phrase in [('concept', 'ordinary still-life photograph'),
                                    ('subject', 'ceramic vase'), ('event', 'resting on a wooden table')]]
    if whole:
        anchors.append({'anchor_id': 'whole_camera', 'dimension': 'camera',
                        'source_text': camera, 'prompt_evidence': camera})
    else:
        anchors.extend({'anchor_id': 'camera_' + axis, 'dimension': 'camera', 'target': 'camera',
                        'property': 'viewpoint.' + axis, 'source_text': phrases[axis], 'prompt_evidence': phrases[axis]}
                       for axis in requested)
    lock = {'contract_version': 'photo-intent-lock/v2', 'priority': 'requesting_user',
            'semantic_anchors': anchors, 'locked_dimensions': ['concept', 'subject', 'event'] + (['camera'] if whole else []),
            'open_dimensions': [] if whole or absent else ['camera']}
    declaration = {'dimension': 'camera', 'polarity': 'required' if whole else 'advisory',
        'axes': {'camera_axis_review': 'camera_axis_review_v1', 'capture_owner': 'camera' if requested else 'unprescribed',
                 **{axis + '_requirement': 'requested' if axis in requested else 'open' for axis in ('direction', 'height')}},
        'evidence': {'owner_phrase': 'The camera', **{axis + '_phrase': phrases[axis] for axis in requested}} if requested else {}}
    return {'contract_version': 'photo-authorial-core/v3', 'baseline_prompt_en': text,
            'intent_lock': lock, 'semantic_assertions': [] if absent else [declaration]}, {
            'active_spans': [{'span_id': 'topic', 'text': text}]}


def normalize(core, envelope):
    return NS['normalize_intent_lock'](core['intent_lock'], envelope=envelope,
        baseline_prompt_en=core['baseline_prompt_en'], minimum_open_dimensions=0,
        allowed_dimensions=NS['AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS'])


def allows(core, prop):
    return NS['property_effects_allowed'](core['intent_lock'], ['camera'],
        [{'dimension': 'camera', 'target': 'camera', 'property': prop}])


class CameraAuthoringGuidanceContractTests(unittest.TestCase):
    def test_separate_axes_protect_only_prescribed_properties(self):
        for axes in [('direction',), ('height',), ('direction', 'height'), ()]:
            with self.subTest(requested=axes):
                core, envelope = fixture(axes)
                normalize(core, envelope)
                NS['camera_authoring_declaration'](core, required=True)
                NS['require_camera_evidence'](core, list(axes))
                for axis in ('direction', 'height'):
                    self.assertEqual(allows(core, 'viewpoint.' + axis), axis not in axes)
                self.assertTrue(allows(core, 'viewpoint.roll'))
                self.assertTrue(allows(core, 'lens.focal_length'))

    def test_combined_paths_pass_declaration_but_lose_leaf_guards(self):
        for prop, direction, height in [('viewpoint.direction_height', True, True),
                                        ('viewpoint.direction.height', False, True)]:
            with self.subTest(property=prop):
                core, envelope = fixture()
                core['intent_lock']['semantic_anchors'][3:] = [{'anchor_id': 'combined', 'dimension': 'camera',
                    'target': 'camera', 'property': prop, 'source_text': 'looks from the side at waist height',
                    'prompt_evidence': 'looks from the side at waist height'}]
                normalize(core, envelope)
                NS['camera_authoring_declaration'](core, required=True)
                NS['require_camera_evidence'](core, ['direction', 'height'])
                self.assertEqual(allows(core, 'viewpoint.direction'), direction)
                self.assertEqual(allows(core, 'viewpoint.height'), height)

    def test_broad_viewpoint_is_not_a_lossless_partial_axis_repair(self):
        core, envelope = fixture()
        core['intent_lock']['semantic_anchors'][3:] = [{'anchor_id': 'broad', 'dimension': 'camera',
            'target': 'camera', 'property': 'viewpoint', 'source_text': 'looks from the side at waist height',
            'prompt_evidence': 'looks from the side at waist height'}]
        normalize(core, envelope)
        with self.assertRaisesRegex(ValueError, 'viewpoint anchor'):
            NS['camera_authoring_declaration'](core, required=True)
        self.assertFalse(allows(core, 'viewpoint.roll'))

    def test_noncanonical_target_fails_declaration_and_capture_guards(self):
        core, envelope = fixture()
        for anchor in core['intent_lock']['semantic_anchors'][3:]:
            anchor['target'] = 'capture_camera'
        normalize(core, envelope)
        NS['require_camera_evidence'](core, ['direction', 'height'])
        with self.assertRaisesRegex(ValueError, 'viewpoint anchor'):
            NS['camera_authoring_declaration'](core, required=True)
        self.assertTrue(allows(core, 'viewpoint.direction'))
        self.assertTrue(allows(core, 'viewpoint.height'))

    def test_whole_and_absent_camera_keep_dimension_closure(self):
        for core, envelope in [fixture(whole=True), fixture((), absent=True)]:
            normalize(core, envelope)
            NS['camera_authoring_declaration'](core, required=bool(core['semantic_assertions']))
            NS['require_camera_evidence'](core, ['direction', 'height'] if core['semantic_assertions'] else [])
            scope = NS['authorial_core_intent_dimension_scope'](core)
            self.assertIn('camera', scope['closed_dimensions'])
            self.assertNotIn('camera', scope['open_dimensions'])

    def test_anchor_bound_does_not_relax_other_requirements(self):
        core, envelope = fixture()
        for count in (0, 1, 16, 17):
            with self.subTest(rows=count):
                changed = copy.deepcopy(core)
                rows = changed['intent_lock']['semantic_anchors']
                # Structural capacity fixture only, never an adapter for a real request.
                while len(rows) < count:
                    i = len(rows)
                    rows.append({'anchor_id': 'structural_' + str(i), 'dimension': 'camera', 'target': 'camera',
                                 'property': 'fixture.property_' + str(i), 'source_text': 'ceramic vase', 'prompt_evidence': 'ceramic vase'})
                del rows[count:]
                if count == 16:
                    self.assertEqual(len(normalize(changed, envelope)['semantic_anchors']), 16)
                else:
                    with self.assertRaisesRegex(ValueError, 'locked dimension' if count == 1 else 'one to sixteen'):
                        normalize(changed, envelope)


if __name__ == '__main__':
    unittest.main()
