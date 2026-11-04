import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import photo_candidate_retrieval_views as views
import photo_replay_reviewed_view_overlay as replay


class ReviewedViewOverlayTest(unittest.TestCase):
    def test_apply_is_idempotent_and_rejects_changed_sources(self):
        record = {'id': 'c1', 'record_kind': 'visual_option', 'content': {'en': 'blue coat', 'ko': '파란 코트'}, 'effects': {}}
        key = 'reviewed:base:whole'
        row = {'id': views.view_id('c1', 'base', key), 'candidate_id': 'c1', 'realization_id': 'base', 'key': key,
               'kind': 'whole', 'source_record_sha256': views.digest(record), 'text_en': 'blue coat', 'text_ko': '파란 코트',
               'source_quotes': [{'pointer': '/content/en', 'quote': 'blue coat'}], 'native_approval': False}
        module = {'schema': views.SCHEMA, 'recipe': views.RECIPE, 'native_approval': False, 'views': []}
        overlay = {'schema': 'photo-reviewed-view-overlay/v1', 'items': [{'candidate_id': 'c1', 'source_record_sha256': views.digest(record), 'views': [row]}]}
        first, actions = replay.apply(module, {'c1': record}, overlay)
        self.assertEqual([x['status'] for x in actions], ['added'])
        second, actions = replay.apply(first, {'c1': record}, overlay)
        self.assertEqual(first, second)
        self.assertEqual([x['status'] for x in actions], ['already_present'])
        changed = copy.deepcopy(record); changed['content']['en'] = 'red coat'
        with self.assertRaisesRegex(ValueError, 'candidate.*changed'):
            replay.apply(module, {'c1': changed}, overlay)
        altered = copy.deepcopy(first); altered['views'][0]['text_en'] = 'unrelated'
        with self.assertRaisesRegex(ValueError, 'differs'):
            replay.apply(altered, {'c1': record}, overlay)

    def test_registered_followups_are_ordered_idempotent_and_source_bound(self):
        record = {'id': 'c1', 'record_kind': 'visual_option',
                  'content': {'en': 'blue coat', 'ko': '파란 코트'}, 'effects': {}}
        records = {'c1': record}
        module = {'schema': views.SCHEMA, 'recipe': views.RECIPE, 'native_approval': False, 'views': []}

        def overlay(key, kind):
            row = {'id': views.view_id('c1', 'base', key), 'candidate_id': 'c1',
                   'realization_id': 'base', 'key': key, 'kind': kind,
                   'source_record_sha256': views.digest(record), 'text_en': 'blue coat',
                   'text_ko': '파란 코트', 'source_quotes': [{'pointer': '/content/en', 'quote': 'blue coat'}],
                   'native_approval': False}
            return json.dumps({'schema': 'photo-reviewed-view-overlay/v1', 'items': [
                {'candidate_id': 'c1', 'source_record_sha256': views.digest(record), 'views': [row],
                 'evidence': [{'locator': 'reactorprompt-document:' + '0' * 64, 'quote': 'historical'}]}]}).encode()

        first, second = overlay('whole', 'whole'), overlay('context', 'context')
        hashes = [hashlib.sha256(x).hexdigest() for x in (first, second)]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'second.json').write_bytes(second)
            registry = root / 'manifest.json'
            registry.write_text(json.dumps({'schema': 'photo-reviewed-view-replay-sequence/v1', 'overlays': [
                {'path': 'first.json', 'sha256': hashes[0]}, {'path': 'second.json', 'sha256': hashes[1]}]}))
            result, stages = replay.apply_registered(module, records, first, hashes[0], root=root, manifest=registry)
            self.assertEqual([stage['added'] for stage in stages], [1, 1])
            again, stages = replay.apply_registered(result, records, first, hashes[0], root=root, manifest=registry)
            self.assertEqual(result, again)
            self.assertEqual([stage['already_present'] for stage in stages], [1, 1])
            single, stages = replay.apply_registered(module, records, first, hashes[0], root=root, manifest=registry,
                                                      followups=False)
            self.assertEqual(len(single['views']), 1)
            self.assertEqual(len(stages), 1)
            (root / 'second.json').write_bytes(b'{}')
            with self.assertRaisesRegex(ValueError, 'registered overlay hash mismatch'):
                replay.apply_registered(module, records, first, hashes[0], root=root, manifest=registry)


if __name__ == '__main__':
    unittest.main()
