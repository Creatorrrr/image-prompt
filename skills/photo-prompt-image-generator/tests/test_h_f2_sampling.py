"""Sampling invariants, independent of model calls and installed corpus size."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import photo_h_f2_sampling as sampling


def rows(count):
    return [{'id': f'cid{i}|base', 'cid': f'cid{i}', 'rid': 'base', 'rank': i + 1}
            for i in range(count)]


class Sampling(unittest.TestCase):
    def test_window_and_limit_for_all_levels(self):
        population = rows(400)
        for level, (window, maximum) in enumerate(((8, 4), (32, 8), (96, 12), (256, 16))):
            selected, proof = sampling.sample(population, level, 731, 'lighting', 'a' * 64)
            self.assertEqual(len(selected), maximum)
            self.assertEqual(proof['window_ids'], [r['id'] for r in population[:window]])
            self.assertTrue(all(r['rank'] <= window for r in selected))
            self.assertEqual(len({r['cid'] for r in selected}), maximum)

    def test_replay_and_new_seed_and_query_isolation(self):
        arguments = (rows(400), 3, 927, 'lighting', 'a' * 64)
        original = sampling.sample(*arguments)
        self.assertEqual(original, sampling.sample(*arguments))
        samples = {tuple(r['id'] for r in sampling.sample(rows(400), 3, seed, 'lighting', 'a' * 64)[0])
                   for seed in range(8)}
        self.assertGreater(len(samples), 1)
        self.assertNotEqual(original[1]['seed_scope_sha256'], sampling.sample(rows(400), 3, 927, 'camera', 'a' * 64)[1]['seed_scope_sha256'])

    def test_no_padding_and_duplicate_cids_have_no_extra_weight(self):
        population = rows(3)
        selected, proof = sampling.sample(population * 3, 3, 2, 'subject', 'b' * 64)
        self.assertEqual(len(selected), 3)
        self.assertEqual(proof['available'], 3)
        self.assertEqual(sampling.sample([], 3, 2, 'subject', 'b' * 64)[0], [])

    def test_sampling_does_not_reintroduce_filtered_sources(self):
        filtered = [r for r in rows(300) if r['rank'] % 7 == 0]
        for level in range(4):
            selected, _ = sampling.sample(filtered, level, 128, 'scope', 'c' * 64)
            self.assertTrue(all(r['rank'] % 7 == 0 for r in selected))

    def test_invalid_controls_and_seeds_fail(self):
        for level in (-1, 4, True, '2'):
            with self.assertRaises(ValueError):sampling.sample(rows(2), level, 0, 'scope', 'a' * 64)
        for seed in (-1, 2**128, True):
            with self.assertRaises(ValueError):sampling.sample(rows(2), 1, seed, 'scope', 'a' * 64)

    def test_historical_top8_remains_readable(self):
        self.assertEqual(sampling.candidates({'top8': rows(8)}), rows(8))
        self.assertEqual(sampling.candidates({'candidates': rows(16)}), rows(16))


if __name__ == '__main__':unittest.main()
