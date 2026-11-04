"""Protect marine source meanings and diagnostic boundaries during publication."""
import copy
import json
from pathlib import Path
import sys
import unittest

SKILL = Path(__file__).resolve().parents[1]
RESEARCH = SKILL.parents[1] / 'docs/research-evidence/photo-prompt/marine-literature-20261024'
sys.path.insert(0, str(SKILL / 'scripts'))
import photo_global_index as projection


def read(path):
    return json.loads(path.read_bytes())


class MarineSourceBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.current = read(SKILL / 'assets/photo_candidate_marine_literature_20261024.json')['candidates']
        cls.before = read(RESEARCH / 'retest-20261024/source.before.json')['candidates']
        cls.sidecar = read(SKILL / 'assets/photo_marine_literature_semantics_20261024.json')

    def test_discovery_repair_preserves_the_complete_original_contracts(self):
        self.assertTrue(set(self.before) <= set(self.current))
        added = set(self.current) - set(self.before)
        self.assertEqual(added, {
            'cand_03072f5d07a551b89a6a904b06597af8',
            'cand_d6b7aef69fbf5ef08505306abd576a06',
            'cand_f2b565fff25951e7b0e86d41179ecada',
        })
        self.assertTrue(all(self.current[cid]['record_kind'] == 'visual_option' for cid in added))
        visual_count = 0
        for cid, old in self.before.items():
            new = copy.deepcopy(self.current[cid])
            # Reviewed wording can improve while record ownership and source
            # contracts remain the same.
            new['content']['en'] = old['content']['en']
            new['content']['ko'] = old['content']['ko']
            if old['record_kind'] != 'visual_option':
                self.assertEqual(new, old, cid)
                continue
            visual_count += 1
            self.assertTrue(set(old['content'].get('aliases', [])) <= set(new['content']['aliases']), cid)
            for field in ('aliases', 'definition'):
                new['content'][field] = old['content'][field]
            metadata = new['content']['research_semantics']
            self.assertIn(metadata.pop('label_en'), self.current[cid]['content']['aliases'])
            self.assertIn('No native or pixel approval', metadata.pop('render_planning')['status'])
            if cid == 'cand_3dbf62efcc8151f4b33526fd1af47aba':
                self.assertEqual(metadata['relations'][-1],
                                 {'subject': 'lines', 'predicate': 'separate_from', 'object': 'runner'})
                metadata['relations'] = old['content']['research_semantics']['relations']
            self.assertEqual(new, old, cid)
        self.assertEqual(visual_count, 87)

    def test_research_routes_do_not_create_positive_approval(self):
        routes = self.sidecar['keyword_routes']
        self.assertEqual(len(routes), 247)
        self.assertTrue(all(not row['hard_activation'] and not row['automatic_bundle'] for row in routes))
        for record in self.current.values():
            if record['record_kind'] == 'visual_option':
                meaning = record['content']['research_semantics']
                self.assertIs(meaning['native_approval'], False)
                self.assertTrue(record['content']['en'].strip())
                self.assertTrue(record['content']['ko'].strip())
                self.assertTrue(meaning['proposal_en'].strip())
                self.assertTrue(meaning['proposal_ko'].strip())
                owners = {owner['id'] for owner in meaning['owners']}
                for edge in meaning['relations']:
                    self.assertIn(edge['subject'], owners)
                    self.assertIn(edge['object'], owners)
                self.assertTrue(all(group['required'] and group['render_gate'] for group in meaning['components']))
        self.assertEqual(sum(r['record_kind'] != 'visual_option' for r in self.current.values()), 247)

    def test_bindings_remain_optional_and_owned_by_registered_sources(self):
        bindings = read(SKILL / 'assets/photo_candidate_marine_literature_bindings_20261024.json')['slot_bindings']
        self.assertEqual(len(bindings), 172)
        reused = set(read(RESEARCH / 'integration-evidence/source-registration.json')['reused_existing_ids'].values())
        for binding in bindings.values():
            self.assertEqual(binding['role'], 'optional')
            self.assertIn(binding['candidate_id'], set(self.current) | reused)
        self.assertEqual(len(self.sidecar['cards']), 96)

    def test_real_positive_projection_excludes_diagnostics_and_review_metadata(self):
        docs = projection.documents({'candidates': self.current})
        self.assertEqual(set(docs), {cid for cid, row in self.current.items() if row['record_kind'] == 'visual_option'})
        self.assertEqual(len(docs), 90)
        record = copy.deepcopy(next(row for row in self.current.values() if row['record_kind'] == 'visual_option'))
        marker = 'REVIEW_METADATA_IS_NOT_POSITIVE_EVIDENCE_47291'
        record['content']['research_semantics']['render_planning']['status'] = marker
        record['content']['research_semantics']['relations'].append({'subject': marker, 'predicate': marker, 'object': marker})
        self.assertNotIn(marker, projection.text(record)[1])


if __name__ == '__main__':
    unittest.main()
