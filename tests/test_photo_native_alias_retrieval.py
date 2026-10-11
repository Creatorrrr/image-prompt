"""Real source aliases must reach their owning slot without changing caps."""
import json
import shutil
from pathlib import Path
import sys
import tempfile
import unittest
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as g


class PhotoNativeAliasRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = g.load_json(SKILL / 'assets/photo_prompt_tags.json')
        cls.expectations = json.loads((ROOT / 'tests/fixtures/photo_prompt/native_alias_v1/source_aliases.json').read_text())
        cls.index = g.build_core_slot_index(json.dumps(cls.data['slots'], ensure_ascii=False,
            sort_keys=True, separators=(',', ':')))

    def test_native_aliases_are_authored_and_return_their_source_identity_within_cap(self):
        for expected in self.expectations:
            with self.subTest(alias=expected['native_alias']):
                slot = expected['slot']
                entries = self.data['slots'][slot]
                source = next(entry for entry in entries if entry['id'] == expected['id'])
                self.assertIn(expected['native_alias'], source['aliases'])
                self.assertEqual(g.candidate_pack_slot_limit(slot), expected['slot_limit'])
                allowed = [f"slot:{slot}:{entry['id']}" for entry in entries]
                for spelling in (expected['native_alias'],
                        unicodedata.normalize('NFD', expected['native_alias'])):
                    ranked = g.rank_bm25f(self.index, {'slot_focus': spelling},
                        allowed_ids=allowed, limit=expected['slot_limit'])
                    self.assertIn(expected['document_id'], [row['document_id'] for row in ranked])

    def test_semantic_and_visual_indexes_use_the_current_tokenizer(self):
        from bm25f_retrieval import BM25F_TOKENIZER_RECIPE_VERSION
        for name in ('photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json'):
            with self.subTest(index=name):
                manifest = json.loads((SKILL / 'assets' / name).read_text())
                self.assertEqual(manifest['bm25f']['tokenizer_recipe'], BM25F_TOKENIZER_RECIPE_VERSION)

    def test_historical_tokenizer_archive_and_transition_remain_hash_bound(self):
        from tests import photo_prompt_fixtures as fixtures
        _, parent = fixtures._v29_transition(ROOT)
        source = 'skills/photo-prompt-image-generator/scripts/bm25f_retrieval.py'
        row = next(row for row in parent['members'] if row['path'] == source)
        proof = fixtures.NATIVE_ALIAS_TOKENIZER_PROOF
        archive = Path(json.loads((ROOT / proof).read_text())['archive_path'])
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            for relative in (Path(source), proof, archive):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / relative, target)
            current = (root / source).read_bytes()
            self.assertEqual(fixtures._native_alias_previous_tokenizer(root, row, current), root / archive)
            self.assertIsNone(fixtures._native_alias_previous_tokenizer(root, row, current + b'\n'))
            for relative in (archive, proof):
                path = root / relative
                original = path.read_bytes()
                path.write_bytes(original + b'\n')
                with self.subTest(path=relative), self.assertRaises(AssertionError):
                    fixtures._native_alias_previous_tokenizer(root, row, current)
                path.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
