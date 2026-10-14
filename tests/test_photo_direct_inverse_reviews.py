"""Offline structural fixtures shaped like the three actual inverse workers.

Fixture literals are authored here; no canonical reviews are generated, changed,
validated or semantically approved by this suite.
"""
import copy
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/verify_inverse_reviews.py'
SPEC = importlib.util.spec_from_file_location('inverse_review_verifier', TOOL)
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)
CIDS = ['cand_' + str(x) * 32 for x in [1, 2, 3]]
BID = 'bind_' + '1' * 32
TASKS = ['/root/review_09250_10500', '/root/review_11870_12250', '/root/review_07250_08250']


class Fixture:
    def __init__(self, root, *, binding=False, branch_units=False, realization_mode='one'):
        self.root = Path(root)
        self.objects, self.encodings = {}, {}
        self.binding = binding
        self.source = {'schema': 'isolated-source-fixture/v1', 'candidates': {},
                       'slot_catalog': {}, 'slot_bindings': {}, 'policies': {}}
        for n, cid in enumerate(CIDS):
            content = {'en': 'The declared actor wears a white garment.',
                       'concept_units': ['white garment on the declared actor'],
                       'evidence_terms': ['a misleading discovery alias'],
                       'realization_content': {'short': {'en': 'A short garment.'},
                                               'long': {'en': 'A long garment.'}} if n == 2 else {}}
            if n == 0:
                content['member_candidate_ids'] = [CIDS[1]]
                if binding:
                    content['member_binding_ids'] = [BID]
            effects = {'dimensions': ['appearance'], 'properties': [
                {'dimension': 'appearance', 'target': '한양 주인공', 'property': 'wardrobe.color'}]}
            if n == 2:
                effects['realizations'] = {'mode': realization_mode, 'branches': [
                    {'id': 'short', 'effects': {'dimensions': ['pose'], 'properties': [
                        {'dimension': 'pose', 'target': '한양 주인공', 'property': 'pose.standing'}]}},
                    {'id': 'long', 'effects': {'dimensions': [], 'properties': []}}]}
            if n == 2 and branch_units:
                for branch in effects['realizations']['branches']:
                    branch['concept_units'] = ['The declared actor wears a white garment in this selected branch.']
                    branch['conditions'] = {'gate': 'This is a prerequisite, not a positive clause.'}
                    branch['context_terms'] = ['declared garment']
                    branch['evidence_terms'] = ['white garment alias']
            self.source['candidates'][cid] = {'id': cid, 'record_kind': 'visual_option', 'content': content,
                                             'conditions': {'for_any': ['human']}, 'effects': effects,
                                             'provenance': [{'source': 'isolated-authored-' + str(n), 'sha256': 'f' * 64}]}
        if binding:
            self.source['slot_bindings'][BID] = {'id': BID, 'candidate_id': CIDS[1],
                                                'slot_id': 'alpha', 'conditions': {'for_any': ['human']}}
        for slot in ['alpha', 'beta', 'gamma']:
            self.source['slot_catalog'][slot] = {'id': slot, 'dimensions': ['appearance'], 'owners': ['entity'],
                'property_prefixes': ['wardrobe.'], 'description': 'Garment color on an explicitly declared owner.'}
        self.source_sha = v.digest(self.source)
        self.catalog_sha = v.digest(self.source['slot_catalog'])
        self.proposal = {'schema': 'proposal-fixture/v1', 'catalog': copy.deepcopy(self.source['slot_catalog']),
                         'original_catalog_sha256': self.catalog_sha,
                         'proposed_catalog_sha256': self.catalog_sha}
        self.plan = {'schema': 'photo-direct-inverse-query-plan/v1', 'source_sha256': self.source_sha,
                     'catalog_sha256': self.catalog_sha, 'binding_sha256': v.digest(self.source['slot_bindings']),
                     'index_sha256': 'a' * 64, 'index_source_sha256': 'b' * 64,
                     'space': {'fixture': True}, 'space_sha256': v.digest({'fixture': True}),
                     'queries': []}
        self.search = {'schema': 'photo-direct-inverse-search-results/v1', **{k: self.plan[k] for k in [
            'source_sha256', 'catalog_sha256', 'binding_sha256', 'index_sha256', 'index_source_sha256', 'space', 'space_sha256']},
                       'searches': []}
        for slot, spec in self.source['slot_catalog'].items():
            query = {'slot_id': slot, 'specification': copy.deepcopy(spec), 'fields': {'slot_focus': spec['description'], 'global_context': ''},
                     'text_sha256': v.digest(spec['description']), 'binding': {'slot_spec_sha256': v.digest(spec)}}
            self.plan['queries'].append(query)
            lanes = {'bm25f': {'ranks': [{'document_id': CIDS[0]}]}, 'embedding': {'ranks': [{'document_id': CIDS[1]}]}}
            self.search['searches'].append({'slot_id': slot, 'lanes': lanes, 'rrf': [{'document_id': CIDS[2]}],
                'query_sha256': query['text_sha256'], 'slot_spec_sha256': query['binding']['slot_spec_sha256'],
                'search_scope': 'whole_shared_positive_corpus', 'tag_admission_filter': False,
                'source_ids': {cid: {'authored_record_sha256': v.digest(row)} for cid, row in self.source['candidates'].items()}})
        self.plan['canonical_sha256'] = v.digest(self.plan)
        self.search['plan_sha256'] = self.plan['canonical_sha256']
        self.add('source', 'SOURCE.json.gz', self.source, 'gzip-json')
        self.add('plan', 'query-plan.json', self.plan)
        self.add('search', 'search.json', self.search)
        self.add('proposed', 'PROPOSED.json', self.proposal)
        self.delegation = {'schema': 'photo-codex-inverse-review-delegation/v1',
                          'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
                          'review_method': 'codex_subagent_direct_source_read',
                          'source_sha256': self.source_sha, 'catalog_sha256': self.catalog_sha,
                          'slot_count': 3, 'positive_count': 3,
                          'search_file': 'search.json', 'search_file_sha256': self.sha('search'),
                          'plan_file': 'query-plan.json', 'plan_file_sha256': self.sha('plan'),
                          'prepared_is_not_direct_read': True, 'canonical_changes_allowed': False,
                          'model_or_network_calls_allowed': False,
                          'assignments': [{'task': task, 'start': n, 'stop': n + 1} for n, task in enumerate(TASKS)]}
        self.add('delegation', 'DELEGATION.json', self.delegation)
        self.add('packet', 'packet.json', {'prepared_is_not_review': True, 'read_claim_at_preparation': False})
        self.make_reviews()
        self.manifest = {'schema': v.SCHEMA, 'artifacts': {},
                         'inputs': {'delegation': 'delegation', 'source': 'source', 'plan': 'plan',
                                    'search': 'search', 'proposed_catalog': 'proposed'},
                         'reviews': [{'artifact': 'a', 'format': '09250-flat', 'task': TASKS[0], 'range': [0, 1]},
                                     {'artifact': 'b', 'format': '11870-slots', 'task': TASKS[1], 'range': [1, 2]},
                                     {'artifact': 'c', 'format': '07250-rows', 'task': TASKS[2], 'range': [2, 3], 'impact': 'impact'}]}
        self.seal()

    def add(self, ident, path, value, encoding='json'):
        self.objects[ident] = (path, value)
        self.encodings[ident] = encoding

    def raw(self, ident):
        value = self.objects[ident][1]
        if self.encodings[ident] == 'bytes':
            return value
        raw = json.dumps(value, ensure_ascii=False, indent=2).encode() + b'\n'
        return gzip.compress(raw, mtime=0) if self.encodings[ident] == 'gzip-json' else raw

    def sha(self, ident):
        return hashlib.sha256(self.raw(ident)).hexdigest()

    def evidence(self, cid):
        return {'pointer': '/content/en', 'quote': self.source['candidates'][cid]['content']['en']}

    def fact(self, cid):
        return {**self.evidence(cid), 'dimension': 'appearance', 'target': '한양 주인공', 'property': 'wardrobe.color'}

    def make_reviews(self):
        raws_a, raws_b, raws_c, logs_b = [], [], [], []
        for index, (cid, record) in enumerate(self.source['candidates'].items()):
            refs, bindings = v.closure(self.source, cid)
            rids = list(v.realization_effects(record))
            sha = v.digest(record)
            raws_a.append({'slot_ordinal': 0, 'slot_id': 'alpha', 'candidate_id': cid, 'record_kind': record['record_kind'],
                'actual_realization_ids': rids, 'direct_full_source_read': True,
                'direct_full_required_reference_closure_read': True, 'meaning_summary': 'Authored fixture judgment.',
                'evidence': self.evidence(cid), 'individual_judgment': 'Fixture fit, not a corpus judgment.',
                'baseline_139_semantic_verdict': 'fit', 'proposed_141_semantic_verdict': 'fit',
                'fit_fact': self.fact(cid), 'native_conditions_as_read': copy.deepcopy(record['conditions']),
                'native_effects_as_read': copy.deepcopy(record['effects']),
                'source_binding': {'candidate_id': cid, 'source_record_sha256': sha,
                                   'catalog_sha256': self.catalog_sha, 'reference_sha256': refs},
                'reference_ids_actually_read': list(refs)})
            logid = 'slot1-' + cid
            anchor = {**self.evidence(cid), 'candidate_id': cid, 'source_sha256': sha}
            raws_b.append({'candidate_id': cid, 'authored_status': 'fit', 'actual_record_kind': record['record_kind'],
                'meaning': 'Authored fixture judgment.', 'source_anchor': anchor,
                'positive_slot_evidence': [anchor], 'owner': '한양 주인공', 'asserted_property': 'wardrobe.color',
                'asserted_dimension': 'appearance', 'actual_realization_ids': rids, 'role_scope': 'Declared actor only.',
                'conditions_exact': copy.deepcopy(record['conditions']), 'effects_exact': copy.deepcopy(record['effects']),
                'closure_read_id': logid, 'source_corrections': []})
            logs_b.append({'read_id': logid, 'slot_index': 1, 'slot_id': 'beta', 'candidate_id': cid,
                'complete_semantic_source_read': True, 'source_sha256': sha, 'closure_complete': True,
                'closure_ids': list(refs), 'closure_sha256': refs, 'binding_ids': list(bindings),
                'actual_realization_ids': rids, 'exact_duplicate_of': None,
                'all_distinct_semantic_fields_conditions_effects_alternatives_read': True})
            fact_c = self.fact(cid)
            fact_c['owner'] = fact_c.pop('target')
            raws_c.append({'label': '2.' + str(index), 'slot_ordinal': 2, 'slot_id': 'gamma', 'candidate_id': cid,
                'judgement': 'fit', 'meaning_judgement': 'Authored fixture judgment.', 'evidence': [fact_c],
                'actual_record_kind': record['record_kind'], 'actual_realization_ids': rids,
                'actual_root_effects': copy.deepcopy(record['effects']),
                'actual_effects_by_realization': v.realization_effects(record),
                'intrinsic_conditions': copy.deepcopy(record['conditions']),
                'complete_blinded_semantic_body_conditions_effects_and_required_closure_read': True,
                'source_sha256': sha, 'reference_sha256': refs, 'binding_sha256': bindings})
        self.a = {'schema': v.FORMATS['09250-flat'], 'task_name': TASKS[0], 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
            'assigned_slot_range': [0, 1], 'completed_slot_range': [0, 1],
            'complete_source_read_for_completed_checkpoint': True, 'source_sha256': self.source_sha,
            'baseline_catalog_sha256': self.catalog_sha, 'proposed_catalog_sha256': self.catalog_sha,
            'search_result_sha256': self.sha('search'), 'query_plan_sha256': self.sha('plan'),
            'directly_reviewed_slot_candidate_pairs': 3, 'directly_read_unique_parent_records': 3,
            'directly_read_unique_records_including_closure': 3,
            'packet': {'path': 'packet.json', 'raw_sha256': self.sha('packet'), 'canonical_sha256': v.digest(self.objects['packet'][1])},
            'actual_read_ledger': [{'candidate_id': cid, 'source_record_sha256': v.digest(rec), 'direct_complete_read': True}
                                   for cid, rec in self.source['candidates'].items()],
            'slot_reviews': [{'slot_ordinal': 0, 'slot_id': 'alpha', 'complete_top3_union_review': True,
                'complete_baseline_spec_and_query_plan_read': True, 'complete_proposed_141_spec_read': True,
                'baseline_spec_sha256': v.digest(self.source['slot_catalog']['alpha']),
                'proposed_spec_sha256': v.digest(self.source['slot_catalog']['alpha']),
                'baseline_query_sha256': self.plan['queries'][0]['text_sha256'],
                'top3': v._top3(self.search['searches'][0]), 'candidate_ids': CIDS, 'slot_candidate_pair_count': 3}],
            'individual_reviews': raws_a}
        self.b = {'schema': v.FORMATS['11870-slots'], 'task_name': TASKS[1], 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
            'assigned_sorted139_range': [1, 2], 'completed_contiguous_sorted139_range': [1, 2],
            'input_hashes': {**{self.objects[k][0]: {'bytes_sha256': self.sha(k)} for k in ['source', 'plan', 'search', 'proposed']},
                             'source_canonical_sha256': self.source_sha, 'catalog139_canonical_sha256': self.catalog_sha,
                             'proposed141_catalog_canonical_sha256': self.catalog_sha},
            'slot_reviews': [{'sorted139_slot_index': 1, 'slot_id': 'beta',
                'spec139': copy.deepcopy(self.source['slot_catalog']['beta']),
                'spec139_sha256': v.digest(self.source['slot_catalog']['beta']),
                'query_fields': self.plan['queries'][1]['fields'],
                'proposal141_spec_sha256': v.digest(self.source['slot_catalog']['beta']),
                'proposal141_spec_exact_equal_to139': True, 'proposal141_change_impact': 'No fixture change.',
                'discovery_top3_by_lane': v._top3(self.search['searches'][1]), 'discovery_union': CIDS,
                'individual_judgments': raws_b}], 'direct_read_log': logs_b}
        self.c = {'schema': v.FORMATS['07250-rows'], 'task_name': TASKS[2], 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
                  'slot_start': 2, 'slot_stop': 3, 'baseline_source_sha256': self.source_sha,
                  'baseline_catalog_sha256': self.catalog_sha, 'baseline_index_sha256': self.search['index_sha256'],
                  'packet_path': 'packet.json', 'rows': raws_c}
        self.add('a', 'inverse_09250_000_047.checkpoint-000-006.json', self.a)
        self.add('b', 'inverse_11870_047_094.json', self.b)
        self.add('c', 'inverse_07250_094_139.094_104.json', self.c)
        refs, bindings = v.closure(self.source, CIDS[0])
        self.impact = {'schema': 'photo-inverse-checkpoint-scope/v1', 'task_name': TASKS[2], 'slot_start': 2, 'slot_stop': 3,
            'immutable_adjudication_path': self.objects['c'][0], 'adjudication_sha256': v.digest(self.c),
            'slot_candidate_pairs': 3, 'direct_candidate_unique_sources': 3,
            'required_closure_unique_sources': len(refs), 'combined_unique_semantic_sources_read': 3,
            'required_source_binding_definitions_read': len(bindings), 'judgements': {'fit': 3},
            'operational_native_qualified_count': 0, 'stage5c_complete': False,
            'proposed_141_impact': {'gamma': 'Authored impact is preserved, not converted to a second verdict.'}}
        self.add('impact', 'inverse_07250_094_139.094_104.impact.json', self.impact)

    def seal(self):
        for ident, (name, value) in self.objects.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            raw = self.raw(ident)
            path.write_bytes(raw)
            desc = {'path': name, 'encoding': self.encodings[ident], 'byte_sha256': v.byte_digest(raw), 'size_bytes': len(raw)}
            if self.encodings[ident] != 'bytes':
                desc['canonical_sha256'] = v.digest(value)
            previous = self.manifest['artifacts'].get(ident, {})
            desc.update({k: val for k, val in previous.items() if k in ['initial_hash_witness', 'mutable_auxiliary']})
            self.manifest['artifacts'][ident] = desc
        self.path = self.root / 'selection.json'
        self.path.write_bytes(v.canonical(self.manifest) + b'\n')
        self.manifest_sha = v.byte_digest(self.path.read_bytes())

    def run(self):
        return v.verify(self.path, root=self.root, manifest_sha256=self.manifest_sha)


class DirectInverseReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.f = Fixture(self.temp.name)

    def codes(self, result):
        return {x['code'] for x in result['failures']}

    def test_three_real_worker_shapes_preserve_literals_and_counts(self):
        result = self.f.run()
        self.assertEqual(result['failures'], [])
        self.assertEqual(result['counts']['actual_claimed_slot_candidate_pairs'], 9)
        self.assertEqual(result['counts']['unique_parent_sources'], 3)
        self.assertEqual(result['counts']['unique_required_closure_sources'], 1)
        self.assertEqual(result['counts']['actual_read_ledger_occurrences'], 9)
        self.assertEqual(result['selected_reviews'][0]['raw_artifact'], self.f.a)
        self.assertEqual(result['normalized_rows_preserving_raw'][3]['raw'], self.f.b['slot_reviews'][0]['individual_judgments'][0])
        self.assertEqual(result['normalized_rows_preserving_raw'][3]['verdicts'], {'baseline': 'fit'})
        for key in ['root_personally_read_all_worker_sources_claimed', 'final_semantic_correctness_proved',
                    'automatic_tag_or_native_qualification', 'runtime_core_verified']:
            self.assertIs(result[key], False)

    def test_literal_verdicts_not_fit_nonfit_unfit_defer_pending_hold_remain_exact(self):
        a, b, c = self.f.a['individual_reviews'], self.f.b['slot_reviews'][0]['individual_judgments'], self.f.c['rows']
        for row, verdict in zip(a, ['not_fit', 'defer', 'pending']):
            row['baseline_139_semantic_verdict'] = row['proposed_141_semantic_verdict'] = verdict
            row['fit_fact'] = None
        for row, verdict in zip(b, ['nonfit', 'pending', 'defer']): row['authored_status'] = verdict
        for row, verdict in zip(c, ['unfit', 'hold', 'pending']): row['judgement'] = verdict
        self.f.impact['judgements'] = {'unfit': 1, 'hold': 1, 'pending': 1}
        self.f.impact['adjudication_sha256'] = v.digest(self.f.c)
        self.f.seal(); result = self.f.run()
        self.assertEqual(result['failures'], [])
        self.assertEqual([r['raw']['judgement'] for r in result['normalized_rows_preserving_raw'][6:]], ['unfit', 'hold', 'pending'])

    def test_metadata_only_fit_fails_separately_without_changing_verdict(self):
        row = self.f.a['individual_reviews'][0]
        row['fit_fact'].update(pointer='/content/evidence_terms/0', quote='a misleading discovery alias')
        self.f.seal(); result = self.f.run()
        self.assertIn('metadata_only_primary_fit', self.codes(result))
        self.assertEqual(len(result['metadata_only_primary_fit_failures']), 2)
        self.assertEqual(result['normalized_rows_preserving_raw'][0]['raw']['baseline_139_semantic_verdict'], 'fit')
        v.canonical(result)  # even failing reports with set differences must serialize

    def test_metadata_labels_all_excluded_but_concept_units_and_relation_sentences_retained(self):
        for label in ['activation', 'match_terms', 'any_terms', 'all_terms', 'exact_terms', 'evidence_terms',
                      'must_mention_any', 'context_terms', 'project_glossary_aliases', 'aliases', 'keywords',
                      'terms', 'concept_terms', 'family_ids', 'topic_ids', 'priority_dimension', 'claim_limits',
                      'research_claim_limits', 'confusion_boundaries', 'evidence_fields']:
            with self.subTest(label=label): self.assertFalse(v.positive_path('/content/' + label + '/0'))
        self.assertTrue(v.positive_path('/content/concept_units/0'))
        self.assertTrue(v.positive_path('/content/embedding_text'))
        self.assertTrue(v.positive_path('/content/member_candidates/0/requirements/concept_units/0'))
        self.assertTrue(v.positive_path('/content/relations/0/subject'))
        self.assertTrue(v.positive_path('/content/realization_content/negative/en'))

    def test_unselected_file_does_not_count_as_read_or_complete(self):
        (self.f.root / 'inverse_999_all_complete.json').write_text('{invalid JSON')
        self.f.manifest['reviews'] = self.f.manifest['reviews'][:1]
        self.f.seal(); result = self.f.run()
        self.assertEqual(result['failures'], [])
        self.assertEqual(result['counts']['actual_claimed_slot_candidate_pairs'], 3)
        self.assertEqual(result['counts']['actual_claimed_slots'], 1)

    def test_manifest_hash_mandatory(self):
        with self.assertRaisesRegex(ValueError, 'manifest byte SHA'):
            v.verify(self.f.path, root=self.f.root, manifest_sha256='0' * 64)

    def test_byte_and_canonical_binding_checked_before_any_review(self):
        for field in ['byte_sha256', 'canonical_sha256']:
            with self.subTest(field=field):
                f = Fixture(self.f.root)
                f.manifest['artifacts']['a'][field] = '0' * 64
                f.path.write_bytes(v.canonical(f.manifest))
                f.manifest_sha = v.byte_digest(f.path.read_bytes())
                result = f.run()
                self.assertIn('artifact_' + field, self.codes(result))
                self.assertEqual(result['normalized_rows_preserving_raw'], [])

    def test_prepared_packet_never_substitutes_missing_actual_pair(self):
        self.f.a['individual_reviews'].pop()
        self.f.seal(); result = self.f.run()
        self.assertIn('top3_pair_coverage', self.codes(result))
        self.assertEqual(result['selected_reviews'][0]['prepared_assignment_pairs_from_search'], 3)
        self.assertEqual(result['selected_reviews'][0]['actual_claimed_slot_candidate_pairs'], 2)

    def test_duplicate_pair_and_overlapping_selection_fail(self):
        self.f.a['individual_reviews'].append(copy.deepcopy(self.f.a['individual_reviews'][0]))
        self.f.manifest['reviews'].append(copy.deepcopy(self.f.manifest['reviews'][0]))
        self.f.seal(); result = self.f.run()
        self.assertIn('duplicate_review_pair', self.codes(result))
        self.assertIn('overlapping_selected_review_pairs', self.codes(result))

    def test_wrong_task_model_effort_and_range_fail(self):
        for key, value, code in [('task_name', 'different', 'worker_task'), ('model', 'another', 'worker_model'),
                                 ('reasoning_effort', 'low', 'worker_effort'), ('completed_slot_range', [0, 2], 'worker_range')]:
            with self.subTest(key=key):
                old = self.f.a[key]; self.f.a[key] = value; self.f.seal()
                self.assertIn(code, self.codes(self.f.run()))
                self.f.a[key] = old

    def test_exact_kind_conditions_effects_and_rids_are_checked(self):
        row = self.f.a['individual_reviews'][0]
        for key, value, code in [('record_kind', 'entity_bundle', 'record_kind'),
                                 ('native_conditions_as_read', {}, 'conditions_exact'),
                                 ('native_effects_as_read', {'dimensions': [], 'properties': []}, 'effects_exact'),
                                 ('actual_realization_ids', ['invented'], 'actual_realization_ids')]:
            with self.subTest(key=key):
                old = row[key]; row[key] = value; self.f.seal()
                self.assertIn(code, self.codes(self.f.run())); row[key] = old

    def test_source_record_and_closure_hashes_no_stale_bindings(self):
        row = self.f.a['individual_reviews'][0]
        row['source_binding']['source_record_sha256'] = '0' * 64
        row['source_binding']['reference_sha256'][CIDS[1]] = '1' * 64
        self.f.seal(); codes = self.codes(self.f.run())
        self.assertIn('row_source_hash', codes); self.assertIn('complete_reference_closure', codes)

    def test_binding_only_child_closure_requires_explicit_read_declaration(self):
        f = Fixture(self.f.root, binding=True)
        result = f.run()
        self.assertIn('missing_binding_read_declaration', self.codes(result))
        # The 11870 source-bound binding-ID declaration and 07250 full binding
        # hash map are accepted; 09250 cannot silently invent a read declaration.
        self.assertFalse(any(x['context'].startswith(('b:', 'c:')) and 'binding' in x['code'] for x in result['failures']))
        f.a['individual_reviews'][0]['binding_sha256'] = {BID: v.digest(f.source['slot_bindings'][BID])}
        f.seal(); self.assertEqual(f.run()['failures'], [])

    def test_binding_definition_hash_change_is_detected(self):
        f = Fixture(self.f.root, binding=True)
        f.a['individual_reviews'][0]['binding_sha256'] = {BID: v.digest(f.source['slot_bindings'][BID])}
        f.c['rows'][0]['binding_sha256'][BID] = '0' * 64
        f.impact['adjudication_sha256'] = v.digest(f.c)
        f.seal(); self.assertIn('complete_binding_closure_hashes', self.codes(f.run()))

    def test_binding_resolution_adds_child_to_full_closure(self):
        source = copy.deepcopy(self.f.source)
        source['candidates'][CIDS[0]]['content'].pop('member_candidate_ids')
        source['candidates'][CIDS[0]]['content']['members'] = [BID]
        source['slot_bindings'][BID] = {'id': BID, 'candidate_id': CIDS[2], 'conditions': {'x': True}}
        refs, bindings = v.closure(source, CIDS[0])
        self.assertEqual(refs, {CIDS[2]: v.digest(source['candidates'][CIDS[2]])})
        self.assertEqual(bindings, {BID: v.digest(source['slot_bindings'][BID])})

    def test_wrong_quote_noncanonical_index_and_foreign_rid_fail(self):
        row = self.f.a['individual_reviews'][0]
        for evidence in [{'pointer': '/content/en', 'quote': 'not present'},
                         {'pointer': '/content/concept_units/00', 'quote': 'white'},
                         {'pointer': '/conditions/for_any/0', 'quote': 'human'}]:
            with self.subTest(evidence=evidence):
                row['evidence'] = evidence; self.f.seal()
                self.assertTrue({'exact_pointer_quote', 'invalid_evidence_pointer', 'evidence_source_body_pointer'} & self.codes(self.f.run()))
        row = self.f.a['individual_reviews'][2]
        row['evidence'] = {'pointer': '/content/realization_content/long/en', 'quote': 'A long garment.'}
        row['actual_realization_ids'] = ['short']
        self.f.seal(); self.assertIn('evidence_actual_rid', self.codes(self.f.run()))

    def test_fit_dimension_property_prefix_and_concrete_named_owner(self):
        row = self.f.a['individual_reviews'][0]
        row['fit_fact'].update(dimension='lighting', property='wardrobeish.color', target='*')
        self.f.seal(); codes = self.codes(self.f.run())
        self.assertTrue({'fit_dimension_spec', 'fit_property_prefix', 'fit_owner_literal'} <= codes)

    def test_per_rid_effects_keep_root_and_only_actual_branch(self):
        effects = v.realization_effects(self.f.source['candidates'][CIDS[2]])
        self.assertEqual(list(effects), ['short', 'long'])
        self.assertEqual(effects['short']['dimensions'], ['appearance', 'pose'])
        self.assertEqual(effects['long']['dimensions'], ['appearance'])
        self.f.c['rows'][2]['actual_effects_by_realization']['long']['dimensions'].append('pose')
        self.f.impact['adjudication_sha256'] = v.digest(self.f.c)
        self.f.seal(); self.assertIn('per_rid_effects', self.codes(self.f.run()))

    def test_impact_canonical_link_and_counts_not_byte_hash(self):
        self.f.impact['adjudication_sha256'] = self.f.sha('c')
        self.f.impact['direct_candidate_unique_sources'] = 999
        self.f.seal(); codes = self.codes(self.f.run())
        self.assertTrue({'impact_adjudication_canonical', 'impact_count'} <= codes)

    def test_undeclared_packet_and_worker_auxiliary_fail_without_reading(self):
        self.f.a['packet']['path'] = 'not-selected.py'
        self.f.b['input_hashes']['unselected-note.md'] = {'bytes_sha256': '0' * 64}
        self.f.seal(); self.assertIn('undeclared_or_ambiguous_reference', self.codes(self.f.run()))

    def test_mutable_writer_cannot_be_newly_frozen_without_initial_witness(self):
        self.f.add('writer', 'author.py', b'print("never executed")\n', 'bytes')
        self.f.seal(); self.assertIn('missing_initial_auxiliary_hash_witness', self.codes(self.f.run()))
        self.f.add('initial', 'initial.json', {'closed_writer_sha256': self.f.sha('writer')})
        self.f.seal()
        self.f.manifest['artifacts']['writer']['initial_hash_witness'] = {'artifact': 'initial', 'pointer': '/closed_writer_sha256'}
        self.f.seal(); self.assertEqual(self.f.run()['failures'], [])
        self.f.objects['writer'] = ('author.py', b'print("changed later")\n')
        self.f.seal(); self.assertIn('closed_initial_auxiliary_mutated', self.codes(self.f.run()))

    def test_unselected_prior_read_and_reuse_cycles_fail(self):
        self.f.a['actual_read_ledger'][0]['read_origin'] = 'prior_frozen_inverse_fullread'
        logs = self.f.b['direct_read_log']
        logs[0]['exact_duplicate_of'] = 'never-selected'
        logs[1]['exact_duplicate_of'] = logs[2]['read_id']
        logs[2]['exact_duplicate_of'] = logs[1]['read_id']
        self.f.seal(); codes = self.codes(self.f.run())
        self.assertTrue({'unselected_prior_read', 'reuse_source_identity', 'read_reuse_cycle'} <= codes)

    def test_11870_explicit_later_chunk_field_variant_preserves_original(self):
        chunk = self.f.b
        chunk['parent_assigned_sorted139_range'] = chunk.pop('assigned_sorted139_range')
        slot = chunk['slot_reviews'][0]
        slot['proposal141_spec'] = copy.deepcopy(slot['spec139'])
        for row in slot['individual_judgments']:
            row['full_source_read_id'] = row.pop('closure_read_id')
            row['role_scope_and_prerequisites'] = row.pop('role_scope')
        for log in chunk['direct_read_log']:
            log['full_semantic_source_conditions_effects_alternatives_read'] = log.pop('complete_semantic_source_read')
            log.pop('all_distinct_semantic_fields_conditions_effects_alternatives_read')
            log['complete_required_closure_read'] = log.pop('closure_complete')
            log['frozen_binding_ids'] = log.pop('binding_ids')
            log['realization_ids'] = log.pop('actual_realization_ids')
            log['duplicate_record_equal_to'] = log.pop('exact_duplicate_of')
        self.f.seal(); result = self.f.run()
        self.assertEqual(result['failures'], [])
        self.assertEqual(result['selected_reviews'][1]['raw_artifact'], chunk)
        chunk['direct_read_log'][0]['actual_realization_ids'] = ['invented']
        self.f.seal()
        self.assertIn('conflicting_compatibility_fields', self.codes(self.f.run()))

    def test_exact_prior_read_reuse_counts_are_distinct_from_unique_sources(self):
        # Two explicitly selected slots of this same worker reuse the exact first
        # slot's full-source read IDs; no prepared packet is used as a witness.
        self.f.delegation['assignments'] = [
            {'task': TASKS[0], 'start': 0, 'stop': 1},
            {'task': TASKS[1], 'start': 1, 'stop': 3}]
        self.f.b['assigned_sorted139_range'] = [1, 3]
        self.f.b['completed_contiguous_sorted139_range'] = [1, 3]
        extra_slot = copy.deepcopy(self.f.b['slot_reviews'][0])
        extra_slot.update(sorted139_slot_index=2, slot_id='gamma',
                          spec139=copy.deepcopy(self.f.source['slot_catalog']['gamma']),
                          spec139_sha256=v.digest(self.f.source['slot_catalog']['gamma']),
                          query_fields=self.f.plan['queries'][2]['fields'],
                          proposal141_spec_sha256=v.digest(self.f.source['slot_catalog']['gamma']))
        for row in extra_slot['individual_judgments']:
            row['closure_read_id'] = row['closure_read_id'].replace('slot1-', 'slot2-')
        extra_logs = copy.deepcopy(self.f.b['direct_read_log'])
        for log in extra_logs:
            log['exact_duplicate_of'] = log['read_id']
            log['read_id'] = log['read_id'].replace('slot1-', 'slot2-')
            log['slot_index'], log['slot_id'] = 2, 'gamma'
        self.f.b['slot_reviews'].append(extra_slot)
        self.f.b['direct_read_log'].extend(extra_logs)
        self.f.manifest['reviews'] = self.f.manifest['reviews'][:2]
        self.f.manifest['reviews'][1]['range'] = [1, 3]
        self.f.seal(); result = self.f.run()
        self.assertEqual(result['failures'], [])
        self.assertEqual(result['counts']['declared_read_reuse_occurrences'], 3)
        self.assertEqual(result['counts']['actual_claimed_slot_candidate_pairs'], 9)
        self.assertEqual(result['counts']['unique_parent_sources'], 3)
        self.assertEqual(result['selected_reviews'][1]['prepared_assignment_pairs_from_search'], 6)

    def test_nonfit_metadata_anchor_is_not_promoted_to_primary_fit(self):
        row = self.f.a['individual_reviews'][0]
        row['evidence'] = {'pointer': '/content/evidence_terms/0', 'quote': 'a misleading discovery alias'}
        row['baseline_139_semantic_verdict'] = row['proposed_141_semantic_verdict'] = 'not_fit'
        row['fit_fact'] = None
        self.f.seal(); result = self.f.run()
        self.assertEqual(result['failures'], [])
        self.assertEqual(result['metadata_only_primary_fit_failures'], [])

    def test_row_lane_positions_and_proposal_fit_property_scope(self):
        self.f.a['individual_reviews'][0]['top3_lane_positions'] = {'dense': [1]}
        self.f.a['individual_reviews'][0]['fit_fact']['property'] = 'wardrobe'
        self.f.a['slot_reviews'][0]['proposed_spec_sha256'] = '0' * 64
        self.f.seal(); codes = self.codes(self.f.run())
        self.assertIn('row_lane_positions', codes)
        self.assertIn('proposed_spec_hash', codes)
        # The exact prefix stem is allowed by the existing direct-review owner/
        # property contract; no stricter punctuation rename is introduced.
        self.assertNotIn('fit_property_prefix', codes)

    def test_bound_input_hash_change_and_missing_11870_file_binding_fail(self):
        self.f.a['source_sha256'] = '0' * 64
        self.f.b['input_hashes'].pop('query-plan.json')
        self.f.seal(); codes = self.codes(self.f.run())
        self.assertIn('worker_input_binding', codes)
        self.assertIn('missing_worker_file_input_binding', codes)

    def test_selection_requires_nonempty_explicit_review_scope(self):
        self.f.manifest['reviews'] = []
        self.f.seal()
        with self.assertRaisesRegex(ValueError, 'nonempty reviews'):
            self.f.run()

    def test_duplicate_json_keys_nan_traversal_and_symlinks_reject(self):
        for raw in [b'{"a":1,"a":2}', b'{"x":NaN}']:
            with self.subTest(raw=raw), self.assertRaises(ValueError): v.load_json(raw)
        self.f.manifest['artifacts']['a']['path'] = '../outside.json'
        self.f.path.write_bytes(v.canonical(self.f.manifest)); self.f.manifest_sha = v.byte_digest(self.f.path.read_bytes())
        self.assertIn('artifact_load', self.codes(self.f.run()))
        link = self.f.root / 'linked.json'; link.symlink_to(self.f.root / 'search.json')
        self.f.manifest['artifacts']['a']['path'] = 'linked.json'
        self.f.path.write_bytes(v.canonical(self.f.manifest)); self.f.manifest_sha = v.byte_digest(self.f.path.read_bytes())
        self.assertIn('artifact_load', self.codes(self.f.run()))

    def test_revision2_query_sha256_explicit_alias_and_conflicts(self):
        slot = self.f.a['slot_reviews'][0]
        slot['query_sha256'] = slot.pop('baseline_query_sha256')
        self.f.seal(); result = self.f.run()
        self.assertEqual(result['failures'], [])
        self.assertEqual(result['contract_revision'], 'bounded-wire-2')
        self.assertNotIn('baseline_query_sha256', result['selected_reviews'][0]['raw_artifact']['slot_reviews'][0])
        slot['baseline_query_sha256'] = '0' * 64
        self.f.seal(); self.assertIn('conflicting_compatibility_fields', self.codes(self.f.run()))
        slot.pop('baseline_query_sha256')
        slot['query_sha256'] = '0' * 64
        self.f.seal(); self.assertIn('worker_query_hash', self.codes(self.f.run()))

    def test_revision2_proposed_impact_exact_six_fields_and_raw_preservation(self):
        impact = {'schema': 'photo-inverse-proposed141-impact/v1', 'task_name': TASKS[2],
                  'slot_start': 2, 'slot_stop': 3, 'review': 'Authored fixture impact prose.',
                  'new_141_native_runtime_completeness_claim': False}
        self.f.objects['impact'] = (self.f.objects['impact'][0], impact)
        self.f.seal(); result = self.f.run()
        self.assertEqual(result['failures'], [])
        summary = result['selected_reviews'][2]
        self.assertEqual(summary['raw_impact'], impact)
        contract = summary['impact_validation_contract']
        self.assertIs(contract['authored_adjudication_hash_present'], False)
        self.assertIs(contract['authored_read_counts_present'], False)
        self.assertNotIn('adjudication_sha256', summary['raw_impact'])
        self.assertEqual(summary['actual_claimed_slot_candidate_pairs'], 3)
        for key, wrong, code in [('task_name', 'wrong', 'impact_task'),
                                 ('slot_stop', 4, 'impact_range'),
                                 ('review', '', 'proposed_impact_review'),
                                 ('new_141_native_runtime_completeness_claim', True, 'proposed_impact_completeness_boundary')]:
            with self.subTest(key=key):
                saved = impact[key]; impact[key] = wrong; self.f.seal()
                self.assertIn(code, self.codes(self.f.run())); impact[key] = saved
        impact['adjudication_sha256'] = '0' * 64
        self.f.seal(); self.assertIn('proposed_impact_fields', self.codes(self.f.run()))

    def test_revision2_unknown_or_incomplete_impact_not_silently_accepted(self):
        self.f.impact['schema'] = 'unknown-impact/v99'
        self.f.seal(); self.assertIn('impact_schema', self.codes(self.f.run()))
        self.f.objects['impact'] = (self.f.objects['impact'][0], {
            'schema': 'photo-inverse-proposed141-impact/v1', 'task_name': TASKS[2],
            'slot_start': 2, 'slot_stop': 3, 'review': 'Only prose, boundary omitted.'})
        self.f.seal(); self.assertIn('proposed_impact_fields', self.codes(self.f.run()))

    def test_revision2_per_rid_dimensions_set_comparison_preserves_every_literal(self):
        # Source root order and worker derived order differ; neither is rewritten.
        actual = {'base': {'dimensions': ['material', 'action', 'timing'], 'properties': []}}
        expected = {'base': {'dimensions': ['action', 'timing', 'material'], 'properties': []}}
        checker = v.Verifier(self.f.root, self.f.path, self.f.manifest_sha)
        saved_actual, saved_expected = copy.deepcopy(actual), copy.deepcopy(expected)
        checker.validate_per_rid_effects(actual, expected, 'isolated ordering')
        self.assertEqual(checker.failures, [])
        self.assertEqual(actual, saved_actual); self.assertEqual(expected, saved_expected)
        self.f.c['rows'][2]['actual_effects_by_realization']['short']['dimensions'].reverse()
        self.f.impact['adjudication_sha256'] = v.digest(self.f.c)
        self.f.seal(); result = self.f.run()
        self.assertEqual(result['failures'], [])
        self.assertEqual(result['normalized_rows_preserving_raw'][8]['raw'], self.f.c['rows'][2])

    def test_revision2_dimensions_duplicates_foreign_ids_and_property_changes_still_fail(self):
        expected = {'base': {'dimensions': ['appearance', 'pose'], 'properties': [
            {'dimension': 'appearance', 'target': 'same actor', 'property': 'wardrobe.color'}]}}
        variations = []
        for dims in [['appearance', 'appearance', 'pose'], ['appearance', 'lighting'],
                     ['appearance'], ['appearance', 1]]:
            variations.append({'base': {'dimensions': dims, 'properties': copy.deepcopy(expected['base']['properties'])}})
        changed_owner = copy.deepcopy(expected); changed_owner['base']['properties'][0]['target'] = 'another actor'
        variations.extend([changed_owner, {'foreign_rid': copy.deepcopy(expected['base'])}])
        for actual in variations:
            with self.subTest(actual=actual):
                checker = v.Verifier(self.f.root, self.f.path, self.f.manifest_sha)
                checker.validate_per_rid_effects(actual, expected, 'isolated adversarial')
                self.assertIn('per_rid_effects', self.codes(checker.report({})))
        reversed_properties = {'base': {'dimensions': ['appearance'], 'properties': [
            {'dimension': 'appearance', 'target': 'same actor', 'property': 'wardrobe.color'},
            {'dimension': 'appearance', 'target': 'same actor', 'property': 'wardrobe.neckline'}]}}
        actual = copy.deepcopy(reversed_properties); actual['base']['properties'].reverse()
        checker = v.Verifier(self.f.root, self.f.path, self.f.manifest_sha)
        checker.validate_per_rid_effects(actual, reversed_properties, 'property order remains exact')
        self.assertIn('per_rid_effects', self.codes(checker.report({})))

    def test_revision2_canonical_branch_positive_quote_binds_source_and_only_actual_rid(self):
        f = Fixture(self.f.root, branch_units=True, realization_mode='optional')
        row = f.b['slot_reviews'][0]['individual_judgments'][2]
        path = '/effects/realizations/branches/0/concept_units/0'
        quote = f.source['candidates'][CIDS[2]]['effects']['realizations']['branches'][0]['concept_units'][0]
        anchor = {'pointer': path, 'quote': quote, 'candidate_id': CIDS[2],
                  'source_sha256': v.digest(f.source['candidates'][CIDS[2]])}
        row['source_anchor'], row['positive_slot_evidence'] = anchor, [copy.deepcopy(anchor)]
        f.seal(); result = f.run()
        self.assertEqual(result['failures'], [])
        norm = result['normalized_rows_preserving_raw'][5]
        self.assertEqual(norm['raw'], row)
        self.assertEqual(norm['rids'], ['base', 'short', 'long'])
        bindings = norm['branch_positive_evidence_bindings']
        self.assertEqual(len(bindings), 1)
        self.assertEqual(bindings[0], {'candidate_id': CIDS[2], 'source_sha256': anchor['source_sha256'],
            'pointer': path, 'surface': 'canonical_branch_concept_unit', 'branch_index': 0,
            'concept_unit_index': 0, 'realization_id': 'short'})
        self.assertFalse(v.positive_path(path))  # no unbound path-only approval
        self.assertTrue(v.positive_path(path, record=f.source['candidates'][CIDS[2]], rids=row['actual_realization_ids']))
        # Identical text in two branches still binds the chosen source branch.
        long_path = '/effects/realizations/branches/1/concept_units/0'
        self.assertEqual(v.branch_positive_binding(f.source['candidates'][CIDS[2]], long_path, row['actual_realization_ids'])['realization_id'], 'long')

    def test_revision2_branch_evidence_wrong_hash_wrong_rid_and_noncanonical_index_fail(self):
        for variation in ['wrong_hash', 'missing_rid', 'explicit_wrong_rid', 'noncanonical_index', 'missing_branch']:
            with self.subTest(variation=variation):
                f = Fixture(self.f.root, branch_units=True)
                row = f.b['slot_reviews'][0]['individual_judgments'][2]
                anchor = {'pointer': '/effects/realizations/branches/0/concept_units/0',
                    'quote': f.source['candidates'][CIDS[2]]['effects']['realizations']['branches'][0]['concept_units'][0],
                    'candidate_id': CIDS[2], 'source_sha256': v.digest(f.source['candidates'][CIDS[2]])}
                if variation == 'wrong_hash': anchor['source_sha256'] = '0' * 64
                elif variation == 'missing_rid': row['actual_realization_ids'] = ['long']
                elif variation == 'explicit_wrong_rid': anchor['realization_id'] = 'long'
                elif variation == 'noncanonical_index': anchor['pointer'] = '/effects/realizations/branches/00/concept_units/0'
                elif variation == 'missing_branch': anchor['pointer'] = '/effects/realizations/branches/7/concept_units/0'
                row['source_anchor'], row['positive_slot_evidence'] = anchor, [copy.deepcopy(anchor)]
                f.seal(); result = f.run(); codes = self.codes(result)
                self.assertEqual(result['status'], 'failed')
                self.assertTrue({'row_source_hash', 'actual_realization_ids', 'branch_positive_explicit_rid',
                                 'evidence_source_body_pointer', 'branch_positive_rid_binding'} & codes)

    def test_revision2_effect_metadata_is_never_a_branch_positive_fact(self):
        f = Fixture(self.f.root, branch_units=True)
        row = f.b['slot_reviews'][0]['individual_judgments'][2]
        paths = ['/effects/dimensions/0', '/effects/properties/0/property',
                 '/effects/realizations/branches/0/id',
                 '/effects/realizations/branches/0/conditions/gate',
                 '/effects/realizations/branches/0/context_terms/0',
                 '/effects/realizations/branches/0/evidence_terms/0',
                 '/effects/realizations/branches/0/effects/properties/0/property']
        for path in paths:
            with self.subTest(path=path):
                anchor = {'pointer': path, 'quote': v.pointer(f.source['candidates'][CIDS[2]], path),
                          'candidate_id': CIDS[2], 'source_sha256': v.digest(f.source['candidates'][CIDS[2]])}
                row['source_anchor'], row['positive_slot_evidence'] = anchor, [copy.deepcopy(anchor)]
                f.seal(); codes = self.codes(f.run())
                self.assertIn('metadata_only_primary_fit', codes)
                self.assertIn('evidence_source_body_pointer', codes)

    def test_no_directory_discovery_api_is_used(self):
        with mock.patch.object(Path, 'iterdir', side_effect=AssertionError('directory scan')), \
             mock.patch.object(Path, 'glob', side_effect=AssertionError('glob scan')), \
             mock.patch.object(Path, 'rglob', side_effect=AssertionError('recursive scan')):
            self.assertEqual(self.f.run()['failures'], [])

    def test_prepared_assignment_scope_is_separate_from_selected_checkpoint(self):
        self.f.delegation['assignments'] = [
            {'task': TASKS[0], 'start': 0, 'stop': 1},
            {'task': TASKS[1], 'start': 1, 'stop': 3}]
        self.f.b['assigned_sorted139_range'] = [1, 3]
        self.f.manifest['reviews'] = self.f.manifest['reviews'][:2]
        self.f.seal(); result = self.f.run()
        self.assertEqual(result['failures'], [])
        summary = result['selected_reviews'][1]
        self.assertEqual(summary['prepared_assignment_pairs_from_search'], 6)
        self.assertEqual(summary['actual_claimed_slot_candidate_pairs'], 3)
        self.assertEqual(summary['selected_range'], [1, 2])
        self.assertEqual(summary['delegated_range'], [1, 3])

    def test_exact_json_types_and_orphan_read_log_rejected(self):
        self.f.a['directly_reviewed_slot_candidate_pairs'] = 3.0
        orphan = copy.deepcopy(self.f.b['direct_read_log'][0])
        orphan['read_id'] = 'orphan'
        self.f.b['direct_read_log'].append(orphan)
        self.f.seal(); codes = self.codes(self.f.run())
        self.assertIn('worker_read_count', codes)
        self.assertIn('orphaned_or_missing_read_log', codes)

    def test_output_requires_explicit_new_json_and_never_overwrites(self):
        result = self.f.run()
        v.write_output(result, 'new-verification.json', root=self.f.root)
        self.assertEqual(json.loads((self.f.root / 'new-verification.json').read_text()), result)
        with self.assertRaises(FileExistsError): v.write_output(result, 'new-verification.json', root=self.f.root)
        for name in ['CURRENT.json', '../outside.json', 'result.txt']:
            with self.subTest(name=name), self.assertRaises(ValueError): v.write_output(result, name, root=self.f.root)


if __name__ == '__main__':
    unittest.main()
