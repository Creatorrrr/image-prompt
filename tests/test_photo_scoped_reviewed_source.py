"""Bounded accepted6220 adoption gates; never write operating or root stage."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

HELPER = Path(__file__).resolve().parents[1] / (
    'docs/research-evidence/photo-prompt/slot149-reduced-adoption-20261015/apply_reviewed6220.py')
spec = importlib.util.spec_from_file_location('apply_reviewed6220_test', HELPER)
adoption = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adoption)


class ReviewedSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original, cls.row, cls.inventory = adoption.accepted_inputs()
        cls.source = copy.deepcopy(cls.original)
        cls.source['slot_catalog'] = adoption.reviews.artifact(
            adoption.ROOT, cls.inventory['current_source'])['slot_catalog']
        bid = next(iter(cls.source['slot_bindings']))
        cls.source['policies']['_slot_binding_review'] = {
            'schema': 'photo-slot-binding-review/v1', 'reviewed': {},
            'deferred': {bid: {'reason': 'Deferred ambiguity', 'source_citation': 'authored/test'}}}

    def test_exact_accepted_proof_passes_current_full_corpus_validation(self):
        proposed = adoption.build_proposal(self.source, self.original, self.row, self.inventory)
        selected = proposed['candidates'][adoption.CID]
        self.assertEqual(selected['content']['role_evidence'], self.row['proof'])
        plain = copy.deepcopy(selected)
        del plain['content']['role_evidence']
        self.assertEqual(plain, self.row['source_after'])
        for field in ('conditions', 'effects', 'provenance'):
            self.assertEqual(selected[field], self.row['source_before'][field])
        for field in ('slot_catalog', 'slot_bindings', 'policies'):
            self.assertEqual(proposed[field], self.source[field])
        self.assertEqual(sum(record != self.source['candidates'][cid]
                             for cid, record in proposed['candidates'].items()), 1)

    def test_unrelated_source_edit_rejected(self):
        source = copy.deepcopy(self.source)
        other = next(cid for cid in source['candidates'] if cid != adoption.CID)
        source['candidates'][other]['content']['en'] = 'unreviewed change'
        with self.assertRaisesRegex(ValueError, 'exact18250 original'):
            adoption.build_proposal(source, self.original, self.row, self.inventory)

    def test_original_conditions_effects_provenance_are_invariant(self):
        for field in ('conditions', 'effects', 'provenance'):
            row = copy.deepcopy(self.row)
            row['source_after'][field] = {'changed': True}
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'preserve original'):
                adoption.build_proposal(self.source, self.original, row, self.inventory)

    def test_nonempty_dependency_rejected_without_expanding_review(self):
        row = copy.deepcopy(self.row)
        row['proof']['dependencies']['base'] = ['unreviewed']
        with self.assertRaisesRegex(ValueError, 'dependency free'):
            adoption.build_proposal(self.source, self.original, row, self.inventory)

    def test_current_catalog_must_match_root_inventory(self):
        inventory = {**self.inventory, 'catalog_sha256': '0' * 64}
        with self.assertRaisesRegex(ValueError, 'current149 catalog'):
            adoption.build_proposal(self.source, self.original, self.row, inventory)

    def test_mutated_inventory_cannot_transfer_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'inventory.json'
            path.write_text('{}')
            with mock.patch.object(adoption, 'INVENTORY', path):
                with self.assertRaisesRegex(ValueError, 'inventory04 changed'):
                    adoption.accepted_inputs()

    def test_operating_assets_guard_runs_before_any_writer(self):
        with self.assertRaisesRegex(ValueError, 'only staged assets'):
            adoption.apply_staged(adoption.ROOT / 'skills/photo-prompt-image-generator/assets',
                                  '/tmp/never-written-selected6220-report.json')


if __name__ == '__main__':
    unittest.main()
