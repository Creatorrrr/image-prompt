"""Pure isolated fixtures, mocked inference receipts; never real model evidence."""
from contextlib import ExitStack
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
sys.path.insert(0, str(EVIDENCE))
import inverse_role_search as inverse
import local_execution_ledger as ledger_module
import photo_candidate_corpus as corpus_module
import photo_embedding_provider as provider
import photo_global_index as documents
import photo_local_embedding as local
import photo_search_layout as layout
import photo_search_reader as readers
import photo_sharded_search as sharded

SPACE = {'provider': 'embeddinggemma2-local', 'model': 'fixture-only-no-model', 'dimensions': 768}
INSTALLATION = {'space': SPACE, 'runtime': {'fixture_only': True}, 'lock_sha256': '1' * 64}
FILES = {'fixture-source.json': '2' * 64}


def vector(a, b=0):
    return [a, b] + [0.] * 766


def slot(name):
    return {'id': name, 'description': 'Visible hair color of an actor.',
            'description_ko': '행위자의 보이는 머리색이며 배경색은 제외한다.',
            'dimensions': ['appearance'], 'semantic_role': 'direct', 'owners': ['actor'],
            'property_prefixes': ['hair.color'], 'includes': ['Visible hair color'],
            'excludes': ['Background color / 배경색'], 'neighbors': [],
            'core_fields': ['subject'], 'applicability': {}, 'priority': 'support'}


def fixture():
    catalog = {'hair_color': slot('hair_color'), 'skin_tone': slot('skin_tone')}
    rows = {}
    # The best vector and strongest lexical record deliberately have NO tag in
    # slot_bindings. Per-tag admission would drop them and fail the oracle.
    for n, text in [(1, 'Visible hair color actor'), (2, 'unbound hair color actor'),
                    (3, 'background color'), (4, 'visible hair color diagnostic')]:
        cid = 'cand_' + f'{n:032x}'
        rows[cid] = {'id': cid, 'record_kind': 'diagnostic' if n == 4 else 'visual_option',
                     'conditions': {}, 'effects': {},
                     'content': {'en': text, 'ko': '머리색' if n != 3 else '배경색',
                                 'aliases': [text], 'definition': text},
                     'provenance': [{'source': 'fixture:' + str(n), 'sha256': str(n) * 64}]}
    corpus = {'schema': corpus_module.SCHEMA, 'candidates': rows, 'slot_catalog': catalog,
              'slot_bindings': {'fixture-binding': {'candidate_id': 'cand_' + f'{1:032x}', 'slot_id': 'hair_color'}},
              'policies': {'visual_meaning_contract': {}, 'relationship_graph': {}, 'bundle_refs': []}}
    vectors = {'schema': documents.SCHEMA, 'space': SPACE, 'corpus_sha256': inverse.digest(corpus), 'entries': {}}
    for n, v in [(1, vector(.7, .7)), (2, vector(1)), (3, vector(-1))]:
        cid = 'cand_' + f'{n:032x}'
        recipe, text = documents.text(rows[cid])
        vectors['entries'][cid] = {'id': cid, 'recipe': recipe, 'text': text,
                                  'text_sha256': hashlib.sha256(text.encode()).hexdigest(), 'vector': v,
                                  'embedding_execution': {'mocked_fixture_document_trace': True}}
    return corpus, vectors


class InverseFixtureTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.temp = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        # Guard the real worker even when future imports change.
        self.infer = self.stack.enter_context(patch.object(local, 'infer', side_effect=AssertionError('model worker forbidden')))
        for module in (provider, documents, layout, readers):
            self.stack.enter_context(patch.object(module, 'validate_space', return_value=SPACE))
        for module in (provider, documents, layout):
            self.stack.enter_context(patch.object(module, 'validate_execution', return_value=None))
        import numpy
        self.stack.enter_context(patch.object(local, 'numpy_runtime', return_value=numpy))
        self.corpus, vectors = fixture()
        layout.build(self.temp, self.corpus, vectors, leaf_size=1, activate=True)
        self.reader = readers.SearchReader(self.temp)
        self.addCleanup(self.reader.close)
        self.plan = inverse.make_plan(self.corpus, self.reader, SPACE, installation=INSTALLATION,
                                      source_files=FILES, expected_slot_count=2)

    def test_native_two_lanes_match_source_rebuilt_full_scan_and_ignore_tags(self):
        query = inverse.role_input(self.corpus['slot_catalog'], 'hair_color')
        result = inverse.search_one(self.corpus, self.reader, query, vector(1), limit=3, oracle=True)
        self.assertEqual(result['full_scan_oracle']['state'], 'passed')
        self.assertEqual(result['lanes']['embedding']['ranks'][0]['document_id'], 'cand_' + f'{2:032x}')
        self.assertNotIn('cand_' + f'{4:032x}', result['union_candidate_ids'])
        self.assertGreater(result['reader_io_after']['vector_reads'], 0)
        self.assertTrue(result['source_ids']['cand_' + f'{2:032x}']['source_ids'])
        self.infer.assert_not_called()

    def test_full_scan_rejects_dropped_pool_and_duplicate_ids(self):
        original = self.reader.meta
        for ids in [[original['positive_ids'][0]], [*original['positive_ids'], original['positive_ids'][0]]]:
            self.reader.meta = {**original, 'positive_ids': ids}
            with self.assertRaisesRegex(ValueError, 'positive pool'):
                inverse.whole_pool(self.corpus, self.reader)
        self.reader.meta = original

    def test_oracle_catches_lexical_tag_partition(self):
        original = sharded.lexical_rank
        one = {'cand_' + f'{1:032x}'}
        with patch.object(sharded, 'lexical_rank', side_effect=lambda r, f, a, l: original(r, f, one, l)):
            with self.assertRaisesRegex(ValueError, 'BM25F lane replay'):
                inverse.search_one(self.corpus, self.reader, self.plan['queries'][0], vector(1), oracle=True)

    def test_cosine_lane_failure_propagates_without_lexical_admission(self):
        with patch.object(sharded, 'cosine_rank', side_effect=RuntimeError('fixture lane failure')):
            with self.assertRaisesRegex(RuntimeError, 'fixture lane failure'):
                inverse.search_one(self.corpus, self.reader, self.plan['queries'][0], vector(1))

    def test_duplicate_lane_and_fusion_faults_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            inverse.fusion([[{'document_id': 'x'}, {'document_id': 'x'}]])
        with patch.object(inverse, 'fusion', return_value=[]):
            with self.assertRaisesRegex(ValueError, 'RRF'):
                inverse.search_one(self.corpus, self.reader, self.plan['queries'][0], vector(1))

    def test_cosine_proof_catches_dropped_embedding_lane(self):
        original = sharded.cosine_rank
        def drop(*args):
            rows, proof = original(*args)
            return rows[1:], proof
        with patch.object(sharded, 'cosine_rank', side_effect=drop):
            with self.assertRaises(ValueError):
                inverse.search_one(self.corpus, self.reader, self.plan['queries'][0], vector(1))

    def test_candidate_free_bilingual_exact_boundaries(self):
        text = self.plan['queries'][0]['text']
        self.assertIn('Visible hair color of an actor.', text)
        self.assertIn('행위자의 보이는 머리색', text)
        self.assertIn('Background color / 배경색', text)
        self.assertNotIn('fixture-binding', text)
        self.assertNotIn('cand_', text)
        self.assertIsNone(self.plan['queries'][0]['binding']['scene_context'])
        changed = copy.deepcopy(self.corpus)
        changed['slot_bindings'] = {}
        self.assertEqual(inverse.role_input(changed['slot_catalog'], 'hair_color'), self.plan['queries'][0])

    def test_current_139_catalog_inputs_are_candidate_free_and_deterministic(self):
        # This only serializes authored definitions. It is no real inference or
        # semantic retrieval evidence and does not open an installed model.
        catalog = json.loads((EVIDENCE / 'CATALOG.json').read_bytes())
        self.assertEqual(len(catalog), 139)
        rows = [inverse.role_input(catalog, s) for s in sorted(catalog)]
        self.assertEqual(rows, [inverse.role_input(catalog, s) for s in sorted(catalog)])
        self.assertEqual(len({r['slot_id'] for r in rows}), 139)
        for row in rows:
            self.assertEqual(row['specification']['owners'], catalog[row['slot_id']]['owners'])
            self.assertEqual(row['specification']['property_prefixes'], catalog[row['slot_id']]['property_prefixes'])
            self.assertEqual(row['specification']['excludes'], catalog[row['slot_id']]['excludes'])
            self.assertNotIn('cand_', row['text'])
        self.infer.assert_not_called()

    def test_plan_rejects_source_index_space_and_query_mutations(self):
        for field, value in [('source_sha256', 'x'), ('index_sha256', 'x'), ('space_sha256', 'x')]:
            plan = copy.deepcopy(self.plan)
            plan[field] = value
            with self.assertRaises(ValueError):
                inverse.validate_plan(plan, self.corpus, self.reader, INSTALLATION, FILES, expected_slot_count=2)
        plan = copy.deepcopy(self.plan)
        plan['queries'][0]['text'] += 'scene injection'
        with self.assertRaises(ValueError):
            inverse.validate_plan(plan, self.corpus, self.reader, INSTALLATION, FILES, expected_slot_count=2)
        with self.assertRaises(ValueError):
            inverse.make_plan(self.corpus, self.reader, {**SPACE, 'provider': 'gemini'},
                              installation=INSTALLATION, source_files=FILES, expected_slot_count=2)

    def _execution_patches(self, output):
        inverse.write_once(output / 'query-plan.json', self.plan)
        self.stack.enter_context(patch.object(inverse, 'evidence_directory', side_effect=Path))
        self.stack.enter_context(patch.object(inverse, 'require_local', return_value=INSTALLATION))
        self.stack.enter_context(patch.object(inverse, 'source_file_hashes', return_value=FILES))
        self.stack.enter_context(patch.object(corpus_module, 'load', return_value=self.corpus))
        self.stack.enter_context(patch.object(readers, 'SearchReader', return_value=self.reader))
        validate = inverse.validate_plan
        self.stack.enter_context(patch.object(inverse, 'validate_plan', side_effect=lambda *a: validate(*a, expected_slot_count=2)))

    def test_execution_gate_and_durable_ledger_precede_mock_provider(self):
        output = self.temp / 'evidence'
        self._execution_patches(output)
        with self.assertRaisesRegex(ValueError, 'counter hook'):
            inverse.execute_queries(self.temp, output, 'fixture')
        called = []
        def account_before_provider(details):
            self.assertEqual(details['expected_input_count'], 2)
            summary = ledger_module.Ledger(details['ledger_directory']).summary()
            self.assertIsNone(summary['exact_total'])
            self.assertEqual(summary['unknown_run_ids'], ['fixture'])
            self.assertEqual(called, [])
        def fake(texts, bindings, cache, *, space, kind):
            called.append(True)
            run = output / 'execution-ledger' / 'fixture'
            self.assertTrue((run / 'planned.json').is_file())
            self.assertTrue((run / 'started.json').is_file())
            self.assertEqual(kind, 'query')
            self.assertEqual(space, SPACE)
            rows = []
            for index, (text, binding) in enumerate(zip(texts, bindings, strict=True)):
                request = {'schema': 'photo-local-embedding-request/v1', 'text': text,
                           'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
                           'space': space, 'binding': binding, 'kind': kind}
                rows.append({'request': request, 'vector': vector(1), 'vector_sha256': inverse.digest(vector(1)),
                             'execution': {'explicit_mocked_fixture_trace': True, 'input_index': index},
                             'cache_hit': index == 1})
            return rows
        with patch.object(provider, 'embed_many', side_effect=fake):
            result = inverse.execute_queries(self.temp, output, 'fixture', execution_enabled=True,
                                             before_start=account_before_provider)
        self.assertEqual(len(result['rows']), 2)
        summary = ledger_module.Ledger(output / 'execution-ledger').summary()
        self.assertEqual(summary['exact_total'], 1)
        self.assertEqual(summary['confirmed_cache_hits'], 1)
        self.assertEqual(len(called), 1)
        with self.assertRaises(FileExistsError):
            inverse.execute_queries(self.temp, output, 'fixture', execution_enabled=True, before_start=lambda d: None)
        self.infer.assert_not_called()

    def test_counter_callback_failure_prevents_provider_and_retains_unknown(self):
        output = self.temp / 'evidence'
        self._execution_patches(output)
        def failed_counter(details):
            raise RuntimeError('fixture accounting unavailable')
        with patch.object(provider, 'embed_many') as provider_call:
            with self.assertRaisesRegex(RuntimeError, 'accounting unavailable'):
                inverse.execute_queries(self.temp, output, 'counter-failed',
                                        execution_enabled=True, before_start=failed_counter)
            provider_call.assert_not_called()
        summary = ledger_module.Ledger(output / 'execution-ledger').summary()
        self.assertIsNone(summary['exact_total'])
        self.assertEqual(summary['unknown_run_ids'], ['counter-failed'])
        self.infer.assert_not_called()

    def test_failed_mock_inference_is_unknown_and_never_reported_zero(self):
        output = self.temp / 'evidence'
        self._execution_patches(output)
        with patch.object(provider, 'embed_many', side_effect=RuntimeError('mock partial failure')) as fake:
            with self.assertRaisesRegex(RuntimeError, 'mock partial failure'):
                inverse.execute_queries(self.temp, output, 'failed-fixture', execution_enabled=True, before_start=lambda d: None)
            fake.assert_called_once()
        summary = ledger_module.Ledger(output / 'execution-ledger').summary()
        self.assertIsNone(summary['exact_total'])
        self.assertEqual(summary['unknown_run_ids'], ['failed-fixture'])
        self.infer.assert_not_called()

    def test_mocked_result_binding_and_invalid_trace_are_rejected(self):
        query = self.plan['queries'][0]
        request = {'schema': 'photo-local-embedding-request/v1', 'text': query['text'],
                   'text_sha256': query['text_sha256'], 'space': SPACE,
                   'binding': {**query['binding'], 'inverse_plan_sha256': self.plan['canonical_sha256']},
                   'kind': 'query'}
        row = {'request': request, 'vector': vector(1), 'vector_sha256': inverse.digest(vector(1)),
               'execution': {'explicit_mocked_fixture_trace': True}, 'cache_hit': True}
        inverse.validate_result(self.plan, row, query)
        changed = copy.deepcopy(row)
        changed['request']['binding']['slot_spec_sha256'] = 'foreign'
        with self.assertRaisesRegex(ValueError, 'binding'):
            inverse.validate_result(self.plan, changed, query)
        with patch.object(provider, 'validate_execution', side_effect=ValueError('mock invalid trace')):
            with self.assertRaisesRegex(ValueError, 'mock invalid trace'):
                inverse.validate_result(self.plan, row, query)


class LedgerTests(unittest.TestCase):
    def test_append_only_unknown_partial_receipts_document_and_exact_counts(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = ledger_module.Ledger(temp)
            ledger.plan('started', ['x'], binding={}, space=SPACE)
            ledger.start('started')
            self.assertIsNone(ledger.summary()['exact_total'])
            ledger.plan('document', ['a', 'b'], binding={}, space=SPACE, kind='document')
            ledger.start('document')
            receipt = {'input_index': 0, 'validated': True, 'cache_hit': False,
                       'text_sha256': hashlib.sha256(b'a').hexdigest(), 'trace_sha256': 'a' * 64}
            ledger.finish('document', state='failed', receipts=[receipt], error_type='MockFailure')
            summary = ledger.summary()
            self.assertEqual(summary['confirmed_minimum'], 1)
            self.assertIsNone(summary['exact_total'])
            self.assertEqual(summary['unknown_run_ids'], ['document', 'started'])
            with self.assertRaises(FileExistsError):
                ledger.start('started')
            with self.assertRaises(FileExistsError):
                ledger.finish('document', state='failed', receipts=[])

    def test_duplicate_receipt_and_incomplete_success_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = ledger_module.Ledger(temp)
            ledger.plan('mock', ['a'], binding={}, space=SPACE)
            ledger.start('mock')
            with self.assertRaises(ValueError):
                ledger.finish('mock', state='complete', receipts=[], result_reference={'fixture': True})
            with self.assertRaises(ValueError):
                ledger.finish('mock', state='failed', receipts=[{'input_index': 0}, {'input_index': 0}])


if __name__ == '__main__':
    unittest.main()
