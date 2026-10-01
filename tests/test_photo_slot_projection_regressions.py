"""Review counterexamples for the advisory frozen-core evidence projector.

These exercise production helpers, not the oracle-query benchmark harness.
"""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0, str(SCRIPTS))
import photo_contracts
import slot_retrieval as evidence


class SlotProjectionRegressionTests(unittest.TestCase):
    def core(self, baseline, **kwargs):
        return {
            'baseline_prompt_en': baseline,
            'intent_lock': {'locked_dimensions': ['lighting', 'camera', 'pose'],
                            'open_dimensions': ['appearance', 'framing'],
                            'semantic_anchors': []},
            **kwargs,
        }

    def positive(self, baseline, slot, **kwargs):
        return evidence.positive_evidence(evidence.project(self.core(baseline, **kwargs), slot))

    def test_negated_and_contrast_lighting_are_not_positive(self):
        for baseline in (
            'The dark monitors in the background do not emit blue light.',
            'An unlit magnifying lamp lies outside the slab area and is not the light source.',
            'She holds a folded reflector at her side rather than using it to light her face.',
            'There is no neon light.',
            'The torch never illuminates the face.',
            'Without blue light on the subject.',
            'Use daylight instead of flash illumination.',
        ):
            with self.subTest(baseline=baseline):
                positive = ' '.join(self.positive(baseline, 'lighting'))
                self.assertNotIn('blue light', positive)
                self.assertNotIn('light source', positive)
                self.assertNotIn('light her face', positive)
                self.assertNotIn('neon', positive)
                self.assertNotIn('torch', positive)
                self.assertNotIn('flash', positive)

    def test_positive_half_of_contrast_is_retained_without_overhead(self):
        baseline = 'The camera observes from a slightly raised angle, not vertically overhead.'
        result = ' '.join(self.positive(baseline, 'camera_direction'))
        self.assertIn('slightly raised angle', result)
        self.assertNotIn('overhead', result)

    def test_bare_inactive_lighting_state_is_not_positive(self):
        for baseline in ('The light is off.', 'The light remains off.',
                         'The light must stay off.'):
            self.assertEqual(self.positive(baseline, 'lighting'), [], baseline)
        self.assertTrue(self.positive('The light is off-camera and illuminates the actor.', 'lighting'))

    def test_depictions_and_camera_objects_are_not_positive(self):
        for baseline in (
            'A poster shows a standing violinist.',
            'A painting depicts a seated woman.',
            'A photograph portrays a kneeling man.',
            'A poster shows a violinist, standing beside a chair.',
        ):
            self.assertEqual(self.positive(baseline, 'body_pose'), [], baseline)
        self.assertEqual(self.positive('A miniature camera charm sits among the watch parts; it is an object, not the taking camera.', 'lens'), [])
        self.assertEqual(self.positive('She is holding a telephoto camera.', 'lens'), [])
        self.assertEqual(self.positive('A camera charm has a tiny telephoto lens.', 'lens'), [])
        self.assertTrue(self.positive('Warm light falls on the painted ceramic mug.', 'lighting'))

    def test_bounded_inflections_avoid_word_stem_false_hits(self):
        for slot, text in (
            ('lighting', 'She leans lightly against a rail.'),
            ('lighting', 'A lightweight paper kite hangs in the room.'),
            ('body_pose', 'The house is situated beside a river.'),
            ('prop', 'The restaurant opens at noon.'),
            ('body_pose', 'A runner discusses a standalone test.'),
        ):
            self.assertEqual(self.positive(text, slot), [], (slot, text))
        for slot, text in (
            ('lighting', 'Soft light illuminates the table.'),
            ('body_pose', 'She sits in a chair and leans forward.'),
            ('prop', 'She carries a ceramic mug.'),
        ):
            self.assertTrue(self.positive(text, slot), (slot, text))

    def test_lens_and_direction_anchor_evidence_are_separate(self):
        lens = 'The taking camera uses a 50 mm lens.'
        direction = 'The camera faces the reader straight on at eye height.'
        core = self.core(lens + ' ' + direction)
        core['intent_lock']['semantic_anchors'] = [
            {'anchor_id': 'lens', 'dimension': 'camera', 'prompt_evidence': lens},
            {'anchor_id': 'direction', 'dimension': 'camera', 'prompt_evidence': direction},
        ]
        for slot, wanted, unwanted in (('lens', '50 mm', 'straight on'),
                                        ('camera_direction', 'straight on', '50 mm')):
            result = evidence.project(core, slot)
            positive = ' '.join(evidence.positive_evidence(result))
            self.assertIn(wanted, positive)
            self.assertNotIn(unwanted, positive)
            ids = [r.get('anchor_id') for r in result['evidence'] if r.get('positive_spans')]
            self.assertNotIn('direction' if slot == 'lens' else 'lens', ids)

    def test_optical_adjunct_is_separated_from_camera_geometry(self):
        baseline = 'The photograph is framed at eye level with a wide-angle lens.'
        self.assertNotIn('wide-angle', ' '.join(self.positive(baseline, 'camera_direction')))
        self.assertNotIn('eye level', ' '.join(self.positive(baseline, 'lens')))

    def test_shared_camera_dimension_keeps_property_lock_local(self):
        core = self.core('The camera faces straight on. The taking camera uses a 50 mm lens.', intent_lock={
            'locked_dimensions': [], 'open_dimensions': ['camera'],
            'semantic_anchors': [{'anchor_id': 'direction', 'dimension': 'camera',
                                  'target': 'camera', 'property': 'direction',
                                  'prompt_evidence': 'The camera faces straight on.'}]})
        lens = evidence.project(core, 'lens')
        direction = evidence.project(core, 'camera_direction')
        self.assertEqual(lens['locked_dimensions'], [])
        self.assertEqual(lens['open_dimensions'], ['camera'])
        self.assertFalse(any(r['ownership'] == 'requester_locked' for r in lens['evidence']))
        self.assertTrue(any(r['ownership'] == 'requester_locked' for r in direction['evidence']))

    def test_camera_property_and_narrow_anchor_do_not_author_lens_exclusions(self):
        for property_scoped in (True, False):
            anchor = {'anchor_id': 'direction', 'dimension': 'camera',
                      'prompt_evidence': 'The camera faces straight on.'}
            if property_scoped:
                anchor.update({'target': 'camera', 'property': 'direction'})
            core = self.core('The camera faces straight on. The lens avoids distortion, without telephoto compression.', intent_lock={
                'locked_dimensions': [] if property_scoped else ['camera'],
                'open_dimensions': ['camera'] if property_scoped else [],
                'semantic_anchors': [anchor]})
            self.assertEqual(evidence.conflict_reasons(core, {'en': 'telephoto compression'}, 'lens'), [])
            core['request_binding'] = {'active_spans': [{'text': 'Use a lens without telephoto compression.'}]}
            self.assertEqual(evidence.conflict_reasons(core, {'en': 'telephoto compression'}, 'lens'), ['explicit_baseline_exclusion'])

    def test_camera_direction_retains_supported_relational_phrasing(self):
        for baseline in ('We view the runner entirely from her side.',
                         'The camera observes from a little above the player.'):
            self.assertTrue(self.positive(baseline, 'camera_direction'), baseline)

    def test_dimensions_use_v3_vocabulary_and_framing_ownership(self):
        mapped = {d for dims in evidence.SLOT_DIMENSIONS.values() for d in dims}
        self.assertLessEqual(mapped, photo_contracts.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
        self.assertNotIn('prop', evidence.dimension_for_slot('prop'))
        self.assertEqual(evidence.dimension_for_slot('shot_scale'), ('framing',))
        core = self.core('The portrait is framed waist-up.', intent_lock={
            'locked_dimensions': ['framing'], 'open_dimensions': ['camera'],
            'semantic_anchors': [{'anchor_id': 'crop', 'dimension': 'framing',
                                  'prompt_evidence': 'framed waist-up'}]})
        result = evidence.project(core, 'subject_framing')
        self.assertEqual(result['locked_dimensions'], ['framing'])
        self.assertTrue(any(r.get('anchor_id') == 'crop' for r in result['evidence']))

    def test_casefold_anchor_and_assertion_matching_preserves_ownership(self):
        core = self.core('Soft window light illuminates the table.', semantic_assertions=[{
            'assertion_id': 'source', 'dimension': 'lighting', 'polarity': 'required',
            'evidence': {'source_phrase': 'soft window light'}}])
        core['intent_lock']['semantic_anchors'] = [{
            'anchor_id': 'window', 'dimension': 'lighting', 'prompt_evidence': 'soft window light'}]
        before = copy.deepcopy(core)
        rows = evidence.project(core, 'lighting')['evidence']
        owned = [r for r in rows if r['ownership'] == 'requester_locked']
        self.assertEqual(len(owned), 2)
        self.assertTrue(all(r.get('positive_spans') for r in owned))
        self.assertEqual(core, before)

    def test_negated_and_depicted_substrings_cannot_reenter_through_anchors(self):
        for baseline, slot, dimension, phrase in (
            ('The monitors do not emit blue light.', 'lighting', 'lighting', 'blue light'),
            ('A poster shows a standing violinist.', 'body_pose', 'pose', 'standing violinist'),
        ):
            core = self.core(baseline, semantic_assertions=[{
                'assertion_id': 'bad', 'dimension': dimension, 'polarity': 'required',
                'evidence': {'source_phrase': phrase}}])
            core['intent_lock']['semantic_anchors'] = [{
                'anchor_id': 'bad', 'dimension': dimension, 'prompt_evidence': phrase}]
            self.assertEqual(evidence.positive_evidence(evidence.project(core, slot)), [])

    def test_explicit_user_exclusions_do_not_inflate_overlap(self):
        core = self.core('A blue neon glow lights the scene.', user_exclusions=['blue neon glow'])
        spans = evidence.positive_evidence(evidence.project(core, 'lighting'))
        self.assertEqual(evidence.evidence_overlap({'en': 'blue neon glow'}, spans), 0)

    def test_candles_and_street_lamp_false_conflicts_are_removed(self):
        candles = self.core('She turned off the lamp and the candles glow softly on the table.')
        self.assertEqual([r['entity'] for r in evidence.inactive_entities(candles['baseline_prompt_en'])], ['lamp'])
        self.assertEqual(evidence.conflict_reasons(candles, {'en': 'The candles glow softly on the table.'}, 'lighting'), [])
        street = self.core('A quiet street without traffic under warm street lamps.')
        self.assertEqual(evidence.conflict_reasons(street, {'en': 'warm street lamps'}, 'lighting'), [])

    def test_copula_and_inactive_state_variants_have_local_entities(self):
        for text, expected in (
            ('The computer monitors behind are off.', 'monitors'),
            ('The lamps remain off.', 'lamps'),
            ('The lamps stay off.', 'lamps'),
            ('The lamp was off.', 'lamp'),
            ('The lamps were off.', 'lamps'),
            ('The desk lamp is unplugged.', 'lamp'),
            ('An unplugged desk lamp rests on the table.', 'lamp'),
            ('An unlit magnifying lamp lies beside the slab.', 'lamp'),
            ('The timetable display is dark.', 'display'),
            ('The lamp must remain switched off.', 'lamp'),
        ):
            with self.subTest(text=text):
                rows = evidence.inactive_entities(text)
                self.assertIn(expected, [r['entity'] for r in rows])
                self.assertEqual(evidence.conflict_reasons(self.core(text), {'en': f'The {expected} emits light.'}, 'lighting'), ['inactive_entity_as_active_source'])
                self.assertTrue(all(r['evidence'] in text for r in rows))

    def test_locked_request_exclusions_are_checked_without_baseline_repetition(self):
        core = self.core('Cool twilight illumination covers the passenger.', request_binding={
            'active_spans': [{'text': 'No glowing screen or lamp lights the face.'}]})
        self.assertIn('explicit_baseline_exclusion', evidence.conflict_reasons(core, {'en': 'The lamp lights the face.'}, 'lighting'))
        core['request_binding']['active_spans'] = [{'text': 'The computer monitors behind are off.'}]
        self.assertIn('inactive_entity_as_active_source', evidence.conflict_reasons(core, {'en': 'The computer monitors emit blue light.'}, 'lighting'))

    def test_open_authorial_state_does_not_become_requester_exclusion(self):
        core = self.core('The lamp is switched off.', intent_lock={
            'locked_dimensions': [], 'open_dimensions': ['lighting'], 'semantic_anchors': []})
        entry = {'en': 'The lamp emits light.'}
        self.assertEqual(evidence.conflict_reasons(core, entry, 'lighting'), [])
        core['request_binding'] = {'active_spans': [{'text': 'The lamp remains off.'}]}
        self.assertEqual(evidence.conflict_reasons(core, entry, 'lighting'), ['inactive_entity_as_active_source'])

    def test_no_cross_source_entity_resolution(self):
        core = self.core('The desk lamp is off.', request_binding={
            'active_spans': [{'text': 'The ceiling lamp illuminates the room.'}]})
        self.assertEqual(evidence.conflict_reasons(core, {'en': 'The ceiling lamp illuminates the room.'}, 'lighting'), [])

    def test_spatial_off_color_and_negated_activity_are_not_conflicts(self):
        for baseline in ('The lamp is off-white.', 'The lamp is off camera.',
                         'The lamp is off-camera.', 'The lamp is off the table.'):
            self.assertEqual(evidence.inactive_entities(baseline), [], baseline)
        for label in ('The lamp casts a sharp shadow.', 'The lamp does not emit light.',
                      'The lamp emits no light.'):
            self.assertEqual(evidence.conflict_reasons(self.core('The lamp is switched off.'), {'en': label}, 'lighting'), [])

    def test_exclusion_relation_order_is_preserved(self):
        core = self.core('An adult keeps their hands low.', request_binding={
            'active_spans': [{'text': 'An adult, without hands above the head.'}]})
        self.assertEqual(evidence.conflict_reasons(core, {'en': 'the head above the hands'}, 'body_pose'), [])
        self.assertEqual(evidence.conflict_reasons(core, {'en': 'hands above the head'}, 'body_pose'), ['explicit_baseline_exclusion'])
        self.assertEqual(evidence.conflict_reasons(core, {'en': 'without hands above the head'}, 'body_pose'), [])

    def test_direct_human_material_representations_are_not_human(self):
        for subject in ('An adult man in bronze, standing on a plinth', 'An adult woman in marble'):
            self.assertEqual(evidence.direct_subject_categories(subject), [], subject)
        self.assertEqual(evidence.direct_subject_categories('An adult woman in bronze-colored clothing'), ['human'])

    def test_frozen_bakery_retains_locked_sunlight_and_camera_anchor(self):
        baseline = ('A torn loaf of bread lies on an empty bakery counter with no people, and crumbs spread around the torn loaf. '
                    'Direct midday sunlight crosses its crust and draws a crisp edge on the wooden surface. '
                    'The tablet beside it is dark and does not emit blue light. '
                    'The taking camera looks slightly down across the counter with a broad view of the empty bakery and ordinary proportional depth.')
        core = self.core(baseline)
        core['intent_lock']['semantic_anchors'] = [
            {'anchor_id': 'sun', 'dimension': 'lighting', 'prompt_evidence': 'Direct midday sunlight crosses its crust'},
            {'anchor_id': 'view', 'dimension': 'camera', 'prompt_evidence': 'looks slightly down across the counter'},
        ]
        for slot in ('lighting', 'light_type', 'light_shape', 'light_direction'):
            result = evidence.project(core, slot)
            owned = [r for r in result['evidence'] if r.get('anchor_id') == 'sun']
            self.assertEqual(len(owned), 1, slot)
            self.assertIn('Direct midday sunlight crosses its crust', owned[0]['positive_spans'])
            self.assertEqual(owned[0]['ownership'], 'requester_locked')
            self.assertNotIn('blue light', ' '.join(evidence.positive_evidence(result)))
        self.assertTrue(evidence.positive_evidence(evidence.project(core, 'camera_direction')))
        self.assertEqual(evidence.positive_evidence(evidence.project(core, 'lens')), [])

    def test_frozen_prism_retains_beam_prop_and_framing_evidence(self):
        baseline = ('Three clear glass prisms rest on a matte tabletop with no people or plants. '
                    'The prisms refract a narrow white beam into separated spectral bands, with transparent glass edges remaining clear against the dark surface. '
                    'A miniature camera charm rests nearby but is not the taking camera. '
                    'The photograph shows the full arrangement from an oblique tabletop viewpoint, retaining both the incoming white beam and its separated colors in one physically coherent composition.')
        core = self.core(baseline, intent_lock={
            'locked_dimensions': ['lighting', 'framing'], 'open_dimensions': ['camera', 'appearance', 'action', 'setting'],
            'semantic_anchors': [
                {'anchor_id': 'beam', 'dimension': 'lighting', 'prompt_evidence': 'a narrow white beam'},
                {'anchor_id': 'frame', 'dimension': 'framing', 'prompt_evidence': 'shows the full arrangement'},
                {'anchor_id': 'view', 'dimension': 'camera', 'property': 'viewpoint.direction', 'target': 'taking_camera',
                 'prompt_evidence': 'an oblique tabletop viewpoint'},
            ]})
        for slot, phrase in (('lighting', 'a narrow white beam'), ('subject_framing', 'shows the full arrangement')):
            result = evidence.project(core, slot)
            self.assertIn(phrase, evidence.positive_evidence(result))
            self.assertTrue(any(r['ownership'] == 'requester_locked' and phrase in r['positive_spans'] for r in result['evidence']))
        self.assertIn('Three clear glass prisms rest on a matte tabletop', evidence.positive_evidence(evidence.project(core, 'prop')))
        self.assertTrue(evidence.positive_evidence(evidence.project(core, 'camera_direction')))
        self.assertEqual(evidence.positive_evidence(evidence.project(core, 'lens')), [])

    def test_single_family_typed_evidence_does_not_require_known_cues(self):
        for dimension, slot, phrase in (
            ('lighting', 'lighting', 'A pale ribbon sweeps across the tiles'),
            ('pose', 'body_pose', 'Her weight settles into one hip'),
            ('composition', 'composition', 'The two figures occupy opposite thirds'),
            ('framing', 'subject_framing', 'Only her face and neck occupy the image'),
        ):
            with self.subTest(slot=slot):
                self.assertFalse(evidence._has_slot_cue(phrase, slot), 'The control must remain outside the cue vocabulary')
                core = self.core(phrase + '.', intent_lock={
                    'locked_dimensions': [dimension], 'open_dimensions': [],
                    'semantic_anchors': [{'anchor_id': 'unfamiliar', 'dimension': dimension, 'prompt_evidence': phrase}],
                }, semantic_assertions=[{'assertion_id': 'unfamiliar', 'dimension': dimension, 'polarity': 'required',
                                        'evidence': {'source_phrase': phrase.lower()}}])
                before = copy.deepcopy(core)
                result = evidence.project(core, slot)
                owned = [r for r in result['evidence'] if r['ownership'] == 'requester_locked']
                self.assertEqual(len(owned), 2)
                self.assertTrue(all(r['positive_spans'] for r in owned))
                self.assertEqual(core, before)

    def test_unknown_typed_phrases_keep_negative_and_depicted_source_roles(self):
        phrase = 'a pale ribbon sweeps across the tiles'
        for baseline in ('No one says that a pale ribbon sweeps across the tiles.',
                         'A mural behind her shows that a pale ribbon sweeps across the tiles.'):
            core = self.core(baseline, semantic_assertions=[{
                'assertion_id': 'typed', 'dimension': 'lighting', 'polarity': 'required',
                'evidence': {'source_phrase': phrase}}])
            core['intent_lock']['semantic_anchors'] = [{'anchor_id': 'typed', 'dimension': 'lighting', 'prompt_evidence': phrase}]
            result = evidence.project(core, 'lighting')
            self.assertEqual(evidence.positive_evidence(result), [])
            self.assertEqual(len([r for r in result['evidence'] if r['ownership'] == 'requester_locked']), 2)

    def test_depicted_artifacts_with_intervening_words_are_not_scene_evidence(self):
        for slot, baseline in (
            ('body_pose', 'A poster behind her shows a standing dancer.'),
            ('body_pose', 'The illustration above the desk depicts a kneeling dancer.'),
            ('lighting', 'A small photo of a sunlit beach is pinned to the wall.'),
            ('lighting', 'An image beside the door portrays soft daylight.'),
            ('lighting', 'A mural of a moonlit village covers the wall.'),
            ('body_pose', 'A poster depicts a seated pianist and a standing dancer.'),
        ):
            self.assertEqual(self.positive(baseline, slot), [], baseline)
        self.assertTrue(self.positive('Soft daylight falls across the poster behind her.', 'lighting'))
        self.assertEqual(evidence.clauses('She holds the table and the chair.'), ['She holds the table and the chair'])

    def test_dark_background_and_negative_adjunct_preserve_positive_prefix(self):
        for slot, baseline, phrase in (
            ('lighting', 'A single softbox lights her face against a dark background.', 'A single softbox lights her face'),
            ('lighting', 'Soft daylight fills the room with no harsh shadows.', 'Soft daylight fills the room'),
            ('lighting', 'Warm sunlight reaches the wall without blue spill.', 'Warm sunlight reaches the wall'),
            ('prop', 'A brass urn rests on a dark shelf with no people nearby.', 'A brass urn rests on a dark shelf'),
            ('body_pose', 'She sits in a dark dress without a hat.', 'She sits in a dark dress'),
        ):
            positive = ' '.join(self.positive(baseline, slot))
            self.assertIn(phrase, positive, baseline)
            self.assertNotIn('no harsh shadows', positive)
            self.assertNotIn('blue spill', positive)
            self.assertNotIn('no people', positive)

    def test_camera_geometry_needs_a_taking_view_relation(self):
        for slot, baseline in (
            ('camera_direction', 'She looks down at the letter.'),
            ('camera_direction', 'Warm light falls from above.'),
            ('camera_height', 'A lamp hangs above the reader.'),
            ('camera_direction', 'The camera records a woman who looks down at a letter.'),
            ('camera_direction', 'The camera observes a woman looking down at a letter.'),
            ('camera_direction', 'The photograph shows warm light falling from above.'),
            ('camera_height', 'The camera records a lamp hanging above the reader.'),
        ):
            self.assertEqual(self.positive(baseline, slot), [], baseline)
        for slot, baseline in (
            ('camera_direction', 'The taking camera looks slightly down across the counter.'),
            ('camera_direction', 'The taking camera looks directly down from above.'),
            ('camera_direction', 'We view the runner entirely from her side.'),
            ('camera_direction', 'The scene is photographed from above.'),
            ('camera_direction', 'The taking camera stays at eye level with natural perspective and a clearly recognizable room behind her.'),
            ('camera_direction', 'The taking camera records an eye-level side view, keeping his face and the repaired corner legible together.'),
            ('camera_height', 'The camera is placed slightly above the reader.'),
        ):
            self.assertTrue(self.positive(baseline, slot), baseline)

    def test_user_exclusion_boundaries_do_not_match_inside_words(self):
        for phrase in ('Fine texture catches soft light.', 'Broad context remains visible under warm light.'):
            self.assertTrue(self.positive(phrase, 'lighting', user_exclusions=['text']), phrase)
        self.assertEqual(self.positive('TEXT glows on the wall.', 'lighting', user_exclusions=['text']), [])

    def test_compound_light_sources_keep_word_boundaries(self):
        for word in ('sunlight', 'candlelight', 'lamplight', 'moonlight', 'firelight', 'spotlights'):
            self.assertTrue(self.positive(f'{word} reaches the subject.', 'lighting'), word)
        for word in ('lightweight', 'lightly', 'lighthearted'):
            self.assertEqual(self.positive(f'A {word} object lies nearby.', 'lighting'), [], word)

    def test_optical_adjunct_retains_governing_negative_or_object_role(self):
        for baseline in ('Do not shoot at eye level with a wide-angle lens.',
                         'She holds a camera with a telephoto lens.',
                         'A camera charm with a miniature lens lies nearby.'):
            core = self.core(baseline)
            core['intent_lock']['semantic_anchors'] = [{
                'anchor_id': 'lens', 'dimension': 'camera',
                'prompt_evidence': 'wide-angle lens' if 'wide-angle' in baseline else
                                   'telephoto lens' if 'telephoto' in baseline else 'miniature lens'}]
            self.assertEqual(evidence.positive_evidence(evidence.project(core, 'lens')), [], baseline)
        positive = self.positive('The photograph is framed at eye level with a wide-angle lens, not a telephoto lens.', 'lens')
        self.assertIn('wide-angle', ' '.join(positive))
        self.assertNotIn('telephoto', ' '.join(positive))

    def test_comma_coordinated_light_does_not_require_a_known_finite_verb(self):
        for conjunction, predicate in (('and', 'spills across'), ('but', 'bathes'), ('while', 'envelops')):
            phrase = f'the pale daylight {predicate} the page'
            baseline = f'The desk lamp is unplugged, {conjunction} {phrase}.'
            core = self.core(baseline, semantic_assertions=[{
                'assertion_id': 'daylight', 'dimension': 'lighting', 'polarity': 'required',
                'evidence': {'source_phrase': phrase}}])
            core['intent_lock']['semantic_anchors'] = [
                {'anchor_id': 'daylight', 'dimension': 'lighting', 'prompt_evidence': phrase}]
            result = evidence.project(core, 'lighting')
            self.assertIn(phrase, evidence.positive_evidence(result), baseline)
            owned = [r for r in result['evidence'] if r['ownership'] == 'requester_locked']
            self.assertEqual(len(owned), 2)
            self.assertTrue(all(r['positive_spans'] == [phrase] for r in owned))

    def test_comma_coordinated_depiction_keeps_its_enclosing_artifact_role(self):
        for predicate in ('spills across', 'falls across'):
            phrase = f'the pale daylight {predicate} the painted page'
            core = self.core(f'A poster depicts a seated reader, and {phrase}.')
            core['intent_lock']['semantic_anchors'] = [
                {'anchor_id': 'painted_light', 'dimension': 'lighting', 'prompt_evidence': phrase}]
            self.assertEqual(evidence.positive_evidence(evidence.project(core, 'lighting')), [])

    def test_optical_adjunct_inherits_only_its_own_coordinated_clause(self):
        self.assertTrue(self.positive('The lamp is unplugged, and the scene is photographed at eye level with a wide-angle lens.', 'lens'))
        self.assertEqual(self.positive('The scene is illuminated, and she carries a camera with a telephoto lens.', 'lens'), [])

    def test_camera_relative_and_lighting_participles_are_not_geometry(self):
        for slot, baseline in (
            ('camera_direction', 'The camera faces a lamp that shines from above.'),
            ('camera_direction', 'The camera faces her, lit from the side.'),
            ('camera_direction', 'The camera observes a statue, illuminated from behind.'),
            ('camera_direction', 'The camera faces a model, backlit from below.'),
            ('camera_direction', 'The camera faces a poster that shows an overhead view.'),
            ('camera_height', 'The camera faces a lamp that hangs above the reader.'),
        ):
            self.assertEqual(self.positive(baseline, slot), [], baseline)
        self.assertTrue(self.positive('The camera observes from above, while the lamp lights her face.', 'camera_direction'))

    def test_primary_output_modifiers_do_not_create_a_depicted_object(self):
        for baseline in (
            'The photograph clearly shows soft daylight across the room.',
            'The final image shows soft daylight across the room.',
            'This resulting photograph clearly captures soft daylight across the room.',
        ):
            self.assertTrue(self.positive(baseline, 'lighting'), baseline)
        for baseline in (
            'The photograph on the wall clearly shows soft daylight across the room.',
            'The framed image shows soft daylight across the room.',
            'The final image clearly shows a poster that depicts a sunlit landscape.',
        ):
            self.assertEqual(self.positive(baseline, 'lighting'), [], baseline)


    def test_coordinated_negative_list_cannot_reenter_through_locked_anchor(self):
        baseline = 'The portrait uses window daylight without a flash, a softbox, and the ring light.'
        core = self.core(baseline, intent_lock={'locked_dimensions':['lighting'], 'open_dimensions':[],
            'semantic_anchors':[{'anchor_id':'negative-source','dimension':'lighting','prompt_evidence':'the ring light'}]},
            semantic_assertions=[{'assertion_id':'negative-source','dimension':'lighting','polarity':'required',
                                 'evidence':{'source_phrase':'the ring light'}}])
        positive = ' '.join(evidence.positive_evidence(evidence.project(core, 'lighting')))
        self.assertIn('window daylight', positive)
        self.assertNotIn('ring light', positive)
        self.assertNotIn('softbox', positive)

    def test_negative_enumeration_scope_carries_through_multiple_coordinators(self):
        baseline = 'The scene uses window daylight without a flash, and a softbox, and the ring light.'
        positive = ' '.join(self.positive(baseline, 'lighting'))
        self.assertIn('window daylight', positive)
        self.assertNotIn('softbox', positive)
        self.assertNotIn('ring light', positive)

    def test_negative_contrast_list_does_not_make_last_item_positive(self):
        for phrase in ('rather than', 'instead of'):
            baseline = f'The portrait uses window daylight {phrase} a flash, a softbox, and the ring light.'
            positive = ' '.join(self.positive(baseline, 'lighting'))
            self.assertIn('window daylight', positive)
            self.assertNotIn('ring light', positive)

    def test_enumeration_fix_preserves_independent_daylight_and_positive_list(self):
        baseline = 'The desk lamp is unplugged, and the pale daylight spills across the page.'
        self.assertIn('the pale daylight spills across the page', ' '.join(self.positive(baseline, 'lighting')))
        positive = ' '.join(self.positive('The portrait uses window daylight, a softbox, and the ring light.', 'lighting'))
        self.assertIn('ring light', positive)
        positive = ' '.join(self.positive('Without a flash or ring light. Pale daylight crosses the page.', 'lighting'))
        self.assertIn('Pale daylight', positive)


if __name__ == '__main__':
    unittest.main()
