"""Spring lookup labels discover optional, complete, owner-bound visible variants."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as cs
from photo_contracts import property_effects_allowed


class SpringFashionSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.full_registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.full_registry['profiles'] if p['id'].startswith('spring_sf')}
        cls.candidates = {r['id']: (slot, r) for slot, rows in cls.data['slots'].items()
                          for r in rows if r['id'].startswith('spf_sf')}
        cls.registry = {**cls.full_registry, 'profiles': [p for pid, p in cls.profiles.items()
                        if any(pid.startswith('spring_'+family+'_') for family in ['sf007','sf057','sf086','sf107'])]}
        cls.index = pg.build_visual_profile_index_payload(cls.registry)

    def hard(self, text, source='concept_lock', polarity='required'):
        result = pg.resolve_visual_profile_hits(self.registry,
            [{'source': source, 'text': text, 'polarity': polarity,
              'priority': 'critical', 'mandatory': polarity == 'required'}],
            visual_profile_index=self.index, adult_context=True)
        return {h['profile_id'] for h in result['hits'] if h.get('hard_eligible')}

    def test_added_variant_pairs_have_complete_compiled_native_contracts(self):
        self.assertEqual(len(self.profiles), 276)
        self.assertEqual(len(self.candidates), 276)
        for pid, p in self.profiles.items():
            with self.subTest(profile=pid):
                self.assertTrue(p['required_evidence_fields'])
                self.assertTrue(p['render_gates'])
                self.assertTrue(all(g['review_scale'] == 'native' for g in p['render_gates']))
                self.assertEqual(set(p['concept_candidate']['affected_dimensions']),
                                 set(self.candidates[pid.replace('spring_', 'spf_')][1]['affected_dimensions']))
                self.assertNotIn('body_geometry', p['concept_candidate']['affected_dimensions'])
                self.assertNotIn('identity', p['concept_candidate']['affected_dimensions'])

    def test_complete_variant_exact_routing_negation_and_advisory_boundaries(self):
        for p in self.registry['profiles']:
            text = p['activation']['exact_terms'][0]
            with self.subTest(profile=p['id']):
                self.assertEqual(self.hard(text), {p['id']})
                self.assertNotIn(p['id'], self.hard('not ' + text))
                self.assertNotIn(p['id'], self.hard(text, 'authorial_core_interpretation', 'advisory'))

    def test_labels_hidden_material_and_support_claims_never_harden(self):
        for text in ['sweetheart neckline','스위트하트넥','straight-across neckline',
                     'pointelle knit','포인텔','shirring','ruching','smocking','gathers',
                     'Mary Jane','메리제인','slingback','cotton','linen','silk','rayon',
                     'bias cut','braless','internal padding','underwire support']:
            with self.subTest(label=text):
                self.assertEqual(self.hard(text), set())

    def test_partial_geometry_and_owner_substitution_do_not_activate(self):
        for pid in ['spring_sf007_01','spring_sf057_01','spring_sf107_02','spring_sf107_3']:
            p = self.profiles[pid]
            text = p['activation']['exact_terms'][0]
            with self.subTest(profile=pid):
                for boundary in ['; ', ' and ']:
                    if boundary in text:
                        for part in text.split(boundary):
                            self.assertNotIn(pid, self.hard(part))
                changed = text.replace('same shoe', 'different shoe').replace('selected top', 'background banner').replace('in the top', 'in the background net').replace('bodice', 'poster')
                self.assertNotEqual(changed, text)
                self.assertNotIn(pid, self.hard(changed))

    def test_pointelle_requires_actual_yarn_rims_and_continuous_repeat(self):
        p = self.profiles['spring_sf057_01']
        text = p['activation']['exact_terms'][0]
        self.assertIn('yarn', text)
        self.assertIn('complete rims', text)
        self.assertTrue(pg.candidate_pack_visual_component_match(p, text))
        for substitute in ['Small eyelet-like holes repeat in a geometric pattern within the knitted top surface.',
                           'Printed dots repeat in a geometric pattern on the top.',
                           'Circular punched holes repeat in a woven sheet.',
                           'A wide mesh net appears behind a plain solid top.']:
            self.assertIsNone(pg.candidate_pack_visual_component_match(p, substitute))

    def test_optional_bundles_and_property_locks_keep_owners_and_siblings_separate(self):
        bundles = [b for b in self.data['candidate_bundles'] if b['id'].startswith('spf_sf')]
        self.assertEqual(len(bundles), 276)
        for b in bundles:
            with self.subTest(bundle=b['id']):
                self.assertEqual(b['adoption'], 'optional')
                self.assertEqual(b['profile_activation'], 'independent_request_evidence_only')
                self.assertEqual(len(b['associated_profile_ids']), 1)
                self.assertEqual(len(b['member_candidates']), 1)
        for slot, candidate in self.candidates.values():
            semantic = cs.semantic_source(candidate, slot, self.data['candidate_semantic_policy'])
            for effect in semantic['affected_properties']:
                lock = {'contract_version':'photo-intent-lock/v2','semantic_anchors':[effect]}
                with self.subTest(candidate=candidate['id'], property=effect['property']):
                    self.assertFalse(property_effects_allowed(lock, semantic['affected_dimensions'], semantic['affected_properties']))

    def test_source_maintenance_hashes_bind_each_added_record_and_prior_record(self):
        for filename in pg.RESEARCH_EXTENSION_FILENAMES:
            ext = json.loads((ASSETS / filename).read_text())
            added = [r for rows in ext.get('slots', {}).values() for r in rows if r['id'].startswith('spf_sf')]
            if not added:
                continue
            ref = ext['maintenance_ref']
            record = json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(ref['record_id']+'.json')).read_text())
            raw = copy.deepcopy(ext); raw.pop('maintenance_ref')
            self.assertEqual(cs.digest(record), ref['sha256'])
            self.assertEqual(cs.digest(raw), record['authored_source_sha256'])
            lineage = [record]
            cursor = record
            while cursor.get('prior_maintenance_ref'):
                parent_ref = cursor['prior_maintenance_ref']
                cursor = json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(parent_ref['record_id']+'.json')).read_text())
                self.assertEqual(cs.digest(cursor), parent_ref['sha256'])
                lineage.append(cursor)
            for r in added:
                bound = next(ancestor['candidate_record_sha256'][r['id']] for ancestor in lineage
                             if r['id'] in ancestor.get('candidate_record_sha256', {}))
                self.assertEqual(cs.digest(r), bound)
            prior = record.get('prior_maintenance_ref')
            if prior:
                parent = json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(prior['record_id']+'.json')).read_text())
                self.assertEqual(cs.digest(parent), prior['sha256'])

    def test_real_indexes_cover_new_geometry_and_keyword_discovery_and_reject_stale(self):
        semantic = pg.load_semantic_index_payload(ASSETS/'photo_prompt_semantic_index.json')
        pg.validate_semantic_index_metadata(semantic, self.data)
        visual = pg.load_visual_profile_index(ASSETS/'photo_prompt_visual_profile_index.json', self.full_registry)
        self.assertTrue(set(self.profiles) <= set(visual['entries']))
        self.assertTrue({f'slot:{slot}:{cid}' for cid, (slot, _) in self.candidates.items()} <= set(semantic['entries']))
        bm25f = pg.semantic_bm25f_payload_from_index(semantic, copy_values=False)
        for query, cid in [('Sweetheart neckline','spf_sf007_01'),('Pointelle knit','spf_sf057_01'),
                           ('메리제인','spf_sf107_02'),('Mary Jane','spf_sf107_02'),('Slingback','spf_sf107_3')]:
            rows = pg.rank_bm25f(bm25f, {'active_request':query}, limit=40)
            with self.subTest(query=query):
                self.assertIn(f'slot:{self.candidates[cid][0]}:{cid}', {r['document_id'] for r in rows})
        stale = dict(visual); stale['registry_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'registry_sha256'):
            pg.validate_visual_profile_index_metadata(stale, self.full_registry)


if __name__ == '__main__':
    unittest.main()
