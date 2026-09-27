"""Owner-scoped portrait contracts and optional relational candidate adoption."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import photo_candidate_semantics as cs
import prompt_generator as pg
from visual_profile_contracts import compile_visual_profile


class PortraitCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ext = json.loads((SKILL / 'assets/photo_prompt_portrait_composition_extension.json').read_text())
        cls.raw = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.registry = {**cls.raw, 'profiles': [p for p in cls.raw['profiles'] if p['id'].startswith('pc_')]}
        cls.index = pg.build_visual_profile_index_payload(cls.registry)
        cls.data = pg.load_json(SKILL / 'assets/photo_prompt_tags.json')
        cls.bundles = [b for b in cls.data['candidate_bundles'] if b['id'].startswith('pc_bundle_')]

    def hard(self, text, adult=True):
        result = pg.resolve_visual_profile_hits(
            self.registry,
            [{'source': 'concept_lock', 'text': text, 'polarity': 'required', 'priority': 'critical', 'mandatory': True}],
            visual_profile_index=self.index, adult_context=adult)
        return {h['profile_id'] for h in result['hits'] if h.get('match_basis') == 'exact' and h.get('hard_eligible')}

    def test_complete_owner_relation_is_exact_and_partial_or_negated_is_not(self):
        self.assertEqual(len(self.registry['profiles']), 16)
        for profile in self.registry['profiles']:
            with self.subTest(profile=profile['id']):
                for full in profile['activation']['exact_terms']:
                    self.assertEqual(self.hard(full), {profile['id']})
                    self.assertEqual(self.hard('not ' + full), set())
                    if not full.isascii():
                        self.assertEqual(self.hard(full + ' 제외'), set())
                for component in profile['authored_components']['components']:
                    self.assertEqual(self.hard(component['evidence_terms'][0]), set())
                for label in profile['semantics']['paraphrase_examples']:
                    self.assertEqual(self.hard(label), set())

    def test_camera_direction_owner_and_optical_confusions_do_not_harden(self):
        cases = [
            'three-quarter-length portrait', 'side-profile close-up', 'across the street',
            'a subject looking back over their own shoulder', 'a road with a triangular sign',
            'body diagonal while all room uprights remain vertical', 'a cloudy glass vase',
            'background bokeh around a sharp face', 'a sharp direct face beside an unreadable mirror',
            'a warped central face', 'panning shot with blurry face and sharp background',
            'a diagonally running subject in a level scene', 'an architectural photograph without people',
            '맞은편', '거울', '반사', '동행자', '실제 연인', '예쁘다', '유행하는 구도',
        ]
        for query in cases:
            with self.subTest(query=query):
                self.assertEqual(self.hard(query), set())

    def test_english_negation_of_nonascii_terms_is_shared_and_local(self):
        for term in ['거울 반사', '시선 앞 여백', '光学反射']:
            self.assertTrue(pg.intent_term_is_negated('not ' + term, term))
            self.assertTrue(pg.intent_term_is_negated('without ' + term, term))
            self.assertFalse(pg.intent_term_is_negated('a portrait showing ' + term, term))
            self.assertFalse(pg.intent_term_is_negated('not a blur; portrait showing ' + term, term))

    def test_all_component_gates_survive_compilation_and_duplicate_owner_evidence_fails(self):
        gates = []
        for profile in self.registry['profiles']:
            compiled = compile_visual_profile(profile)
            self.assertEqual(len(compiled['required_evidence_fields']), 4)
            self.assertEqual(len(compiled['render_gates']), 4)
            gates.extend(g['id'] for g in compiled['render_gates'])
            bad = copy.deepcopy(profile)
            bad['authored_components']['components'][1]['evidence_field'] = bad['authored_components']['components'][0]['evidence_field']
            with self.assertRaises(ValueError):
                compile_visual_profile(bad)
        self.assertEqual(len(gates), len(set(gates)))
        self.assertEqual(len(gates), 64)

    def test_age_and_biography_are_not_inferred_from_generic_composition(self):
        for profile in self.registry['profiles']:
            self.assertFalse(profile['activation']['requires_adult_character'])
        for rows in self.ext['slots'].values():
            for entry in rows:
                self.assertFalse(set(entry['affected_dimensions']) & {'age', 'identity', 'role', 'species'})

    def test_bundles_require_every_visible_member_and_open_dimension(self):
        self.assertEqual(len(self.bundles), 42)
        for bundle in self.bundles:
            with self.subTest(bundle=bundle['id']):
                self.assertEqual(bundle['adoption'], 'optional')
                self.assertEqual(bundle['profile_activation'], 'independent_request_evidence_only')
                slots = {}
                dims = set()
                for member in bundle['member_candidates']:
                    dims.update(member['affected_dimensions'])
                    slots.setdefault(member['slot'], {'candidates': []})['candidates'].append(
                        {'id': member['id'], 'applicability': {'status': 'eligible'}})
                pack = {'slots': slots, 'authorial_core': {'intent_lock': {'open_dimensions': sorted(dims)}}}
                data = {**self.data, 'candidate_bundles': [bundle]}
                self.assertEqual(len(cs.public_bundles(data, pack)['candidates']), 1)
                for member in bundle['member_candidates']:
                    bad = copy.deepcopy(pack)
                    rows = bad['slots'][member['slot']]['candidates']
                    rows[:] = [x for x in rows if x['id'] != member['id']]
                    self.assertEqual(cs.public_bundles(data, bad)['candidates'], [])
                for dimension in dims:
                    bad = copy.deepcopy(pack)
                    bad['authorial_core']['intent_lock']['open_dimensions'].remove(dimension)
                    self.assertEqual(cs.public_bundles(data, bad)['candidates'], [])

    def test_bilingual_retrieval_keeps_directed_atomic_relations(self):
        atoms = [e for rows in self.ext['slots'].values() for e in rows]
        self.assertEqual(len(atoms), 156)
        self.assertEqual(len({e['id'] for e in atoms}), 156)
        for entry in atoms:
            self.assertEqual(entry['concept_units'], [entry['en']])
            self.assertTrue(entry['relations'])
            self.assertTrue(any(any('\uac00' <= c <= '\ud7a3' for c in s) for s in entry['aliases']))
            self.assertIn(entry['en'], entry['embedding_text'])
            self.assertNotIn('http', entry['embedding_text'])

    def test_series_trend_and_source_provenance_remain_maintenance_only(self):
        ref = self.ext['maintenance_ref']
        record = json.loads((ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance' / (ref['record_id'] + '.json')).read_text())
        self.assertEqual(ref['sha256'], cs.digest(record))
        source = copy.deepcopy(self.ext)
        source.pop('maintenance_ref')
        self.assertEqual(record['authored_source_sha256'], cs.digest(source))
        deferred = {p['id'] for p in record['maintenance_only']['deferred_proposals']}
        self.assertEqual(deferred, {'PS01', 'PS02', 'PS03', 'PS04', 'PS05', 'PM01', 'PM02', 'PM03'})
        self.assertNotIn('sources.json', json.dumps(self.ext))
        self.assertFalse(any('ps0' in e['id'] or 'pm0' in e['id'] for rows in self.ext['slots'].values() for e in rows))

    def test_reflected_focus_is_visible_and_not_an_unobservable_distance_gate(self):
        profile = next(p for p in self.registry['profiles'] if p['id'] == 'pc_pc22_owner_relation')
        gate = profile['authored_components']['components'][3]['render_gate']['description']
        self.assertIn('resolved', gate)
        self.assertNotIn('virtual-image distance', gate)

    def test_real_generated_indexes_cover_current_source(self):
        semantic = pg.load_semantic_index_payload(SKILL / 'assets/photo_prompt_semantic_index.json')
        pg.validate_semantic_index_metadata(semantic, self.data)
        expected = {f"slot:{slot}:{e['id']}" for slot, rows in self.ext['slots'].items() for e in rows}
        self.assertTrue(expected <= set(semantic['entries']))
        visual = json.loads((SKILL / 'assets/photo_prompt_visual_profile_index.json').read_text())
        pg.validate_visual_profile_index_metadata(visual, self.raw)


if __name__ == '__main__':
    unittest.main()
