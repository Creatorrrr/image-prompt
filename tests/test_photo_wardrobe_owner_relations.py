"""Wardrobe ownership, selected variants and scoped source uncertainty."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg
from photo_contracts import property_effects_allowed
from photo_candidate_semantics import digest


class WardrobeOwnerRelationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = json.loads((ASSETS / 'photo_prompt_wardrobe_owner_relations_extension.json').read_text())
        cls.entries = {e['id']: e for rows in cls.extension['slots'].values() for e in rows}
        full = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in full['profiles'] if p['id'].startswith('wkr_')}
        cls.registry = {**full, 'profiles': list(cls.profiles.values())}
        cls.index = pg.build_visual_profile_index_payload(cls.registry)

    def hard(self, text, source='concept_lock', polarity='required'):
        hits = pg.resolve_visual_profile_hits(self.registry, [
            {'source': source, 'text': text, 'polarity': polarity,
             'priority': 'critical', 'mandatory': polarity == 'required'}
        ], visual_profile_index=self.index, adult_context=True)
        return {r['profile_id'] for r in hits['hits'] if r.get('hard_eligible')}

    def test_complete_relation_has_one_owner_and_no_sibling_obligation(self):
        for pid, profile in self.profiles.items():
            with self.subTest(profile=pid):
                text = profile['activation']['exact_terms'][0]
                self.assertEqual(self.hard(text), {pid})
                self.assertNotIn(pid, self.hard('not ' + text))
                self.assertNotIn(pid, self.hard(text, 'authorial_core_interpretation', 'advisory'))

    def test_family_labels_and_incomplete_layers_do_not_harden(self):
        for text in ['baby tee', 'button-down', 'bandeau', 'balletcore', 'gothic',
                     'satin', 'silk', 'cream', 'detached sleeves', 'tray handoff',
                     'a pendant', 'Mary Jane shoes', 'kimono inspired',
                     'a dark blazer', 'a red dress', 'a red light',
                     'blue background and ivory paint', 'shirt front buttons']:
            with self.subTest(text=text):
                self.assertEqual(self.hard(text), set())
        pid = 'wkr_wk007_selected_relation'
        p = self.profiles[pid]
        self.assertEqual(len(p['authored_components']['components']), 2)
        for component in p['authored_components']['components']:
            self.assertIsNone(pg.candidate_pack_visual_component_match(p, component['evidence_terms'][0]))

    def test_selected_sleeve_does_not_merge_bodice_transmission_or_neck_support(self):
        detached = self.entries['wkr_wk032_selected_relation_candidate']
        joined = self.entries['wkr_wk074_selected_relation_candidate']
        self.assertIn('upper-arm band', detached['en'])
        self.assertIn('gap from the bodice', detached['en'])
        self.assertIn('joining boundary', joined['en'])
        self.assertNotEqual(detached['relations'], joined['relations'])
        self.assertIn('material', detached['affected_dimensions'])
        for entry in [detached, joined]:
            lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [
                {'dimension': 'material', 'target': 'main_subject', 'property': 'wardrobe.material.transmission'}]}
            self.assertFalse(property_effects_allowed(lock, entry['affected_dimensions'], entry['affected_properties']))
        halter = self.entries['wkr_wk026_halter_candidate']
        spaghetti = self.entries['wkr_wk026_spaghetti_candidate']
        self.assertIn('neck', halter['relations'][0]['object'])
        self.assertIn('shoulders', spaghetti['relations'][0]['object'])
        self.assertNotEqual(halter['relations'], spaghetti['relations'])

    def test_natural_discovery_keeps_partial_parts_optional_and_distinct(self):
        examples = {
            'wkr_wk074_selected_relation': 'black velvet bodice and sheer organza sleeves',
            'wkr_wk085_selected_relation': 'a chain draped between two brooches',
            'wkr_wk095_selected_relation': 'compressed folds of a seated skirt on a bench seat',
        }
        for pid, text in examples.items():
            with self.subTest(profile=pid):
                self.assertEqual(pg.candidate_pack_visual_component_match(self.profiles[pid], text), 'component_semantics')
                self.assertFalse(self.hard(text))
                profile = self.profiles[pid]
                self.assertTrue(all(g['review_scale'] == 'native' for g in profile['render_gates']))
        layered = self.profiles['wkr_wk007_selected_relation']
        for partial in ['a ribbed top', 'rolled sleeves']:
            self.assertIsNone(pg.candidate_pack_visual_component_match(layered, partial))
        complete = 'a ribbed top beneath an open shirt with rolled sleeves'
        self.assertEqual(pg.candidate_pack_visual_component_match(layered, complete), 'component_semantics')
        self.assertFalse(self.hard(complete))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['wkr_wk023_scoop'], 'crew neck'))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['wkr_wk026_halter'], 'spaghetti straps'))

    def test_single_accent_print_and_camera_effects_preserve_cross_carrier_locks(self):
        accent = self.entries['wkr_wk070_selected_relation_candidate']
        lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [
            {'dimension': 'appearance', 'target': 'main_subject', 'property': 'wardrobe.color'}]}
        self.assertFalse(property_effects_allowed(lock, accent['affected_dimensions'], accent['affected_properties']))
        self.assertIn('One saturated red fabric plane', accent['en'])
        self.assertIn('remaining garment panels stay black', accent['en'])
        jersey = self.entries['wkr_wk061_selected_relation_candidate']
        self.assertIn('text', jersey['affected_dimensions'])
        self.assertIn('front panel', jersey['en'])
        camera = self.entries['wkr_wk104_selected_relation_candidate']
        lock['semantic_anchors'] = [{'dimension': 'camera', 'target': 'camera', 'property': 'viewpoint'}]
        self.assertFalse(property_effects_allowed(lock, camera['affected_dimensions'], camera['affected_properties']))

    def test_nonworn_and_two_actor_states_are_not_worn_or_single_hand_substitutes(self):
        blazer = self.entries['wkr_wk011_selected_relation_candidate']
        self.assertEqual(blazer['relations'][0]['type'], 'rests_on')
        self.assertIn('bedside surface', blazer['en'])
        self.assertIn('worn blouse remains separate', blazer['en'])
        tray = self.entries['wkr_wk091_selected_relation_candidate']
        self.assertEqual(len(tray['relations']), 2)
        self.assertEqual(tray['relations'][0]['subject'], 'one tray')
        self.assertEqual(tray['relations'][1]['subject'], 'same tray opposite edge')
        self.assertIn('giver', tray['relations'][0]['object'])
        self.assertIn('receiver', tray['relations'][1]['object'])
        self.assertIn('two distinct permitted human actors', json.dumps(tray['contextual_usage']))
        self.assertNotIn('count', tray['affected_dimensions'])
        hem = self.entries['wkr_wk088_selected_relation_candidate']
        self.assertIn('pinch_and_pull_down', [r['type'] for r in hem['relations']])
        self.assertIn('material', hem['affected_dimensions'])
        self.assertNotIn('relationship', hem['affected_dimensions'])

    def test_variant_relations_and_optional_bundles_are_complete(self):
        for entry in self.entries.values():
            with self.subTest(candidate=entry['id']):
                self.assertTrue(entry['relations'])
                for relation in entry['relations']:
                    self.assertTrue(relation['subject'])
                    self.assertTrue(relation['object'])
                    self.assertNotIn('_or_', relation['type'])
                self.assertFalse({'identity','age','species','body_geometry'} & set(entry['affected_dimensions']))
                self.assertNotIn('http', json.dumps(entry))
        for bundle in self.extension['visual_semantics']:
            with self.subTest(bundle=bundle['id']):
                self.assertTrue(bundle['candidate_only'])
                self.assertEqual(len(bundle['candidate_ids']), 1)
                profile = self.profiles[bundle['hard_profile_ids'][0]]
                self.assertEqual(len(profile['render_gates']), len(bundle['component_groups']))
                self.assertTrue(all(g['review_scale']=='native' for g in profile['render_gates']))
        self.assertEqual(len(self.entries),146)

    def test_seed_uncertainty_and_history_remain_external(self):
        serialized = json.dumps(self.extension,ensure_ascii=False)
        for annotation in ['wk002_','wk014_','wk016_','wk069_','wk079_','wk086_','wk120_']:
            self.assertNotIn(annotation, serialized.lower())
        self.assertNotIn('Deep teal, muted sage, charcoal blue, soft ivory, and forest green',serialized)
        self.assertNotIn('source_keyword_ids',serialized)
        self.assertNotIn('exclusions',self.extension)
        e=copy.deepcopy(self.extension);ref=e.pop('maintenance_ref')
        record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/f"{ref['record_id']}.json").read_text())
        self.assertEqual(ref['sha256'],digest(record))
        self.assertEqual(record['authored_source_sha256'],digest(e))
        profile_source=json.loads((ASSETS/'photo_prompt_visual_obligations_wardrobe_owner_relations.json').read_text())
        self.assertEqual(record['profile_source_sha256'],digest(profile_source))

    def test_retained_identities_have_bounded_complete_endpoint_contracts(self):
        bundles = {row['id']: row for row in self.extension['visual_semantics']}
        for number, existing in [('024','clt_ct037_v1'),('029','clt_ct047_v1')]:
            pid = f'wkr_wk{number}_retained_relation'
            with self.subTest(profile=pid):
                self.assertEqual(bundles[pid+'_bundle']['candidate_ids'],[existing])
                self.assertNotIn(existing,self.entries)
                self.assertEqual(self.hard(self.profiles[pid]['activation']['exact_terms'][0]),{pid})
        for family in ['cowl neckline','bishop sleeve']:
            self.assertEqual(self.hard(family),set())

    def test_retained_cowl_cannot_bypass_the_material_drape_owner(self):
        source=json.loads((ASSETS/'photo_prompt_clothing_structure_extension.json').read_text())
        entry=next(row for row in source['slots']['garment_detail'] if row['id']=='clt_ct037_v1')
        lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[
            {'dimension':'material','target':'main_subject','property':'wardrobe.drape'}]}
        self.assertFalse(property_effects_allowed(lock,entry['affected_dimensions'],entry['affected_properties']))
        unrelated={'contract_version':'photo-intent-lock/v2','semantic_anchors':[
            {'dimension':'material','target':'background_wall','property':'surface.paint'}]}
        self.assertTrue(property_effects_allowed(unrelated,entry['affected_dimensions'],entry['affected_properties']))


if __name__=='__main__': unittest.main()
