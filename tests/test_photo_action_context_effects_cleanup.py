"""Bounded DATA consistency tests, not claims of rendered image quality."""
from pathlib import Path
import copy
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/action-context-effects-cleanup-20261001'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator
import photo_candidate_semantics as semantics


class ActionContextEffectsCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = generator.load_json(ASSETS / 'photo_prompt_tags.json')
        # Keep the exact historical cleanup oracle before the later grammar overlay.
        inventory = generator.photo_source_manifest.SourceInventory.for_test(
            ASSETS, candidate_files=tuple(name for name in generator.RESEARCH_EXTENSION_FILENAMES
                if name != 'photo_prompt_visual_grammar_extension.json'))
        cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json', inventory=inventory)
        cls.frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
        cls.before = {(x['slot'], x['id']): x['before'] for x in cls.frozen['inventory']}

    def row(self, slot, entry_id):
        return next(x for x in self.data['slots'][slot] if x['id'] == entry_id)

    def test_frozen_inventory_and_queries_are_unchanged(self):
        raw = (EVIDENCE / 'frozen-inventory-queries.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), '8a2143ddc3ed0f8f85ad0bef6a47bb45cd4d6ff1dc84d78c8701bb757b93fc4a')
        self.assertEqual(len(self.frozen['inventory']), 52)
        self.assertEqual(len(self.frozen['queries']), 32)
        self.assertEqual([sum(x['stage'] == s for x in self.frozen['inventory']) for s in [1, 2, 3]], [24, 16, 12])

    def test_all_thirty_six_keep_decisions_are_exactly_preserved(self):
        rows = [r for r in self.frozen['inventory'] if r['decision'] == 'keep']
        self.assertEqual(len(rows), 36)
        for r in rows:
            self.assertEqual(self.row(r['slot'], r['id']), r['before'], r['id'])

    def test_later_grammar_context_preserves_every_prior_meaning_and_effect(self):
        for record in self.frozen['inventory']:
            old = self.row(record['slot'], record['id'])
            live = next(x for x in self.current['slots'][record['slot']] if x['id'] == record['id'])
            retained = set(old) - {'paraphrases', 'contextual_usage'}
            self.assertEqual({k: live.get(k) for k in retained}, {k: old[k] for k in retained})
            self.assertTrue(set(old.get('paraphrases', [])) <= set(live.get('paraphrases', [])))

    def test_action_captions_remove_only_comparison_or_rewrite_prose(self):
        mirror = self.row('action', 'mirror_selfie')
        self.assertIn('reflective plane', mirror['embedding_text'])
        self.assertIn('reflected body', mirror['embedding_text'])
        self.assertNotIn('front-camera', mirror['embedding_text'])
        self.assertEqual(self.row('action', 'poised_standing')['embedding_text'], 'standing upright with poised dignity')
        for eid in ['mirror_selfie', 'poised_standing']:
            a, b = copy.deepcopy(self.row('action', eid)), copy.deepcopy(self.before['action', eid])
            a.pop('embedding_text'); b.pop('embedding_text')
            self.assertEqual(a, b)

    def test_bilingual_relational_geometry_is_preserved(self):
        umbrella = self.row('relational_action', 'holding_umbrella_over_partner')
        self.assertIn('기울여', umbrella['ko'])
        self.assertIn('tilted toward the partner', umbrella['en'])
        seating = self.row('relational_action', 'two_people_sitting_without_words')
        self.assertIn('마주 앉아', seating['ko'])
        self.assertIn('face to face', seating['en'])
        for eid in ['holding_umbrella_over_partner', 'two_people_sitting_without_words']:
            a, b = copy.deepcopy(self.row('relational_action', eid)), copy.deepcopy(self.before['relational_action', eid])
            a.pop('en'); b.pop('en')
            self.assertEqual(a, b)

    def test_compound_situation_aliases_retain_keywords_and_rendering(self):
        expected = {'morning_commute_rush': 'morning commute rush', 'last_train_wait': 'last train waiting', 'rain_walk': 'rain walk'}
        for eid, alias in expected.items():
            a, b = copy.deepcopy(self.row('situation_context', eid)), copy.deepcopy(self.before['situation_context', eid])
            self.assertIn(alias, a['aliases'])
            self.assertTrue(any(any('\uac00' <= c <= '\ud7a3' for c in term) for term in a['aliases']))
            a.pop('aliases'); b.pop('aliases')
            self.assertEqual(a, b)

    def test_nine_effect_owner_relations_match_candidate_scope(self):
        owners = {'pe_uniform_image_blur': 'image_plane', 'pe_fabric_detail': 'fabric_regions_in_image_plane', 'pe_wide_tonal_detail': 'image_plane_brightness_ranges', 'pe_red_edge_halation': 'film_like_bright_dark_image_edges', 'pe_watercolor_print': 'depicted_paper_surface', 'pe_charcoal_print': 'depicted_paper_surface', 'pe_pencil_print': 'depicted_paper_surface', 'pe_torn_paper_edge': 'depicted_paper_edge', 'pe_cyanotype_paper': 'depicted_paper_surface'}
        rows = [r for r in self.frozen['inventory'] if r['stage'] == 3 and r['decision'] == 'fix']
        self.assertEqual(len(rows), 9)
        for r in rows:
            e = self.row(r['slot'], r['id'])
            self.assertEqual(e['relations'][0]['object'], owners[r['id']])
            original = copy.deepcopy(r['before'])
            original['relations'][0]['object'] = owners[r['id']]
            self.assertEqual(e, original, r['id'])

    def test_discovery_and_property_locks_survive_source_projection(self):
        for r in self.frozen['inventory']:
            if r['stage'] != 3:
                continue
            e = self.row(r['slot'], r['id'])
            self.assertEqual(e['affected_dimensions'], r['before']['affected_dimensions'])
            self.assertEqual(e['affected_properties'], r['before']['affected_properties'])
            self.assertEqual(e['core_assertion_discovery'], r['before']['core_assertion_discovery'])
            projected = semantics.semantic_source(e, r['slot'], self.data['candidate_semantic_policy'])
            self.assertEqual(projected['affected_properties'], e['affected_properties'])
            self.assertEqual(projected['relations'], e['relations'])

    def test_prior_thirty_seven_published_source_rows_are_preserved(self):
        evidence = json.loads((ROOT / 'docs/research-evidence/photo-prompt/main-data-integration-20261001/source-preservation.json').read_text())
        self.assertEqual(len(evidence['preserved_rows']), 37)
        cache = {}
        for r in evidence['preserved_rows']:
            if r['file'] not in cache:
                cache[r['file']] = json.loads((ROOT / r['file']).read_text())
            row = next(x for x in cache[r['file']]['slots'][r['slot']] if x['id'] == r['id'])
            digest = hashlib.sha256(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            self.assertEqual(digest, r['sha256'], r['id'])


if __name__ == '__main__':
    unittest.main()
