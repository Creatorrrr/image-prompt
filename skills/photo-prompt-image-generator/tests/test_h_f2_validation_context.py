"""Wire separation and record compatibility; source/semantic replay is qualified separately."""
from pathlib import Path
import copy
import os
import sys
import unittest

SKILL = Path(__file__).resolve().parents[1]
NATIVE = Path(os.environ.get('PHOTO_H_F2_TEST_NATIVE', SKILL))
sys.path.insert(0, str(NATIVE / 'scripts'))
import photo_candidate_corpus as corpus
import photo_validation_context as context
import record_image_run as recorder


def fixture():
    value = {'contract_version': context.SCHEMA, 'pack_id': None}
    for name in ('authorial_core', 'creative_controls', 'embodiment_preflight',
                 'intent_preservation', 'authorial_composition', 'negative_intent_guard',
                 'global_retrieval', 'provenance'):
        value[name] = {}
    value['pack_id'] = corpus.digest(value)[:16]
    return value


class Context(unittest.TestCase):
    def test_distinct_wire_type_and_derived_record_label(self):
        value = fixture()
        self.assertIs(context.validate(value), value)
        self.assertEqual(recorder.candidate_pack_version(value), 'h-f2-v2')
        self.assertEqual(recorder.candidate_pack_version({'contract_version': 'photo-candidate-pack/v10'}), 'v10')

    def test_native_inventory_cannot_be_smuggled_into_context(self):
        for name in context.FORBIDDEN:
            value = fixture(); value[name] = {}; value['pack_id'] = corpus.digest(dict(value, pack_id=None))[:16]
            with self.subTest(name=name), self.assertRaises(ValueError):context.validate(value)
            with self.assertRaises(ValueError):recorder.candidate_pack_version(value)

    def test_mutation_and_missing_contract_fail(self):
        value = fixture(); value['creative_controls']['creativity'] = 3
        with self.assertRaises(ValueError):context.validate(value)
        value = fixture(); del value['embodiment_preflight']; value['pack_id'] = corpus.digest(dict(value, pack_id=None))[:16]
        with self.assertRaises(ValueError):context.validate(value)

    def test_unknown_and_historical_labels_do_not_become_new_contexts(self):
        for value in (None, [], {}, {'contract_version': 'photo-candidate-pack/v9'}):
            self.assertFalse(context.is_context(value))
            with self.assertRaises(ValueError):recorder.candidate_pack_version(value)


if __name__ == '__main__':unittest.main()
