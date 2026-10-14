"""Integrity gates for authored direct review, without invoking a model."""
import copy
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/direct_review.py'
spec = importlib.util.spec_from_file_location('direct_review', PATH)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
from tests.test_photo_candidate_corpus import fixture, A, B


def decision(data):
    record = data['candidates'][A]
    record['content'] = {'en': 'a glossy fabric surface', 'confounders': ['not a leather coat']}
    tag = 'wardrobe_style'
    data['slot_catalog'][tag]['dimensions'] = ['appearance']
    data['slot_catalog'][tag]['property_prefixes'] = ['wardrobe.']
    fact = {'pointer': '/content/en', 'quote': 'glossy fabric', 'dimension': 'appearance',
        'target': 'main_subject', 'property': 'wardrobe.style'}
    return {**review.binding(data, A), 'schema': review.SCHEMA, 'reviewer': 'Codex',
        'review_method': 'codex_direct_source_read', 'independent_human_review': False,
        'meaning_summary': 'Fixture judgement for contract rejection tests, not a corpus approval.',
        'recommended_kind': 'visual_option', 'corrections': [], 'roles': [{
            'slot_id': tag, 'semantic_role': data['slot_catalog'][tag]['semantic_role'],
            'scope': 'whole_record', 'realization_ids': ['base'], 'rationale': 'Authored fixture rationale.',
            'evidence': [fact]}], 'facts': [{**fact, 'realization_id': 'base'}],
        'rejected_boundaries': ['A negative coat example cannot supply a positive garment.'],
        'uncertainties': [], 'status': 'approved', 'all_roles_considered': True,
        'authored_decision': {'file': 'test.json', 'item': 1, 'sha256': 'b' * 64}, 'packet_sha256': 'c' * 64}


class DirectReviewTests(unittest.TestCase):
    def primitive_proposal(self):
        from tests.test_photo_realization_content import source
        data = source(); row = decision(data)
        proposed = source()['candidates'][A]
        original = data['candidates'][A]
        original['effects'] = {'dimensions': [], 'properties': []}
        row.update(review.binding(data, A))
        row['corrections'] = [
            {'pointer': '/effects', 'before': copy.deepcopy(original['effects']),
             'after': copy.deepcopy(proposed['effects']), 'reason': 'Explicitly split two source alternatives.'},
            {'pointer': '/content/realization_content', 'before': None,
             'after': copy.deepcopy(proposed['content']['realization_content']),
             'reason': 'Select the corresponding positive body without another choice.'}]
        fact = {'pointer': '/content/realization_content/standing/en', 'quote': 'standing adult',
                'dimension': 'appearance', 'target': 'main_subject', 'property': 'wardrobe.style'}
        row['roles'][0].update(scope='positive_alternative', realization_ids=['standing'], evidence=[fact])
        row['facts'] = [{**fact, 'realization_id': 'standing'}]
        return data, row

    def test_structured_proposals_bind_exact_before_and_leave_sources_immutable(self):
        data, row = self.primitive_proposal(); before = copy.deepcopy(data)
        review.validate_decision(row, data)
        self.assertEqual(data, before)
        row['corrections'][0]['before']['dimensions'] = ['pose']
        with self.assertRaisesRegex(ValueError, 'exact source value'):
            review.validate_decision(row, data)

    def test_branch_positive_evidence_cannot_qualify_another_branch(self):
        data, row = self.primitive_proposal()
        row['roles'][0]['realization_ids'] = ['walking']
        row['facts'][0]['realization_id'] = 'walking'
        with self.assertRaisesRegex(ValueError, 'different realization'):
            review.validate_decision(row, data)
        # This also applies to facts not selected as role evidence.
        row['roles'][0]['realization_ids'] = ['standing']
        row['facts'] = [{**row['roles'][0]['evidence'][0], 'realization_id': 'standing'},
                        row['facts'][0]]
        with self.assertRaisesRegex(ValueError, 'different realization'):
            review.validate_decision(row, data)

    def test_one_role_can_have_distinct_owned_evidence_for_each_actual_branch(self):
        data, row = self.primitive_proposal()
        standing = {**row['roles'][0]['evidence'][0], 'realization_id': 'standing'}
        walking = {**standing, 'pointer': '/content/realization_content/walking/en',
                   'quote': 'walking adult', 'realization_id': 'walking'}
        row['roles'][0].update(scope='whole_record', realization_ids=['standing', 'walking'],
                              evidence=[standing, walking])
        row['facts'] = [standing, walking]
        review.validate_decision(row, data)
        row['roles'][0]['evidence'] = [standing]
        with self.assertRaisesRegex(ValueError, 'each selected role realization'):
            review.validate_decision(row, data)
        row['roles'][0]['evidence'] = [standing, {**walking, 'realization_id': 'invented'}]
        with self.assertRaisesRegex(ValueError, 'foreign realization'):
            review.validate_decision(row, data)

    def test_structured_proposals_cannot_invent_a_reference_or_replace_metadata(self):
        for defect in ['candidate', 'component', 'identity', 'guard', 'unknown_conditions', 'untyped']:
            data, row = self.primitive_proposal()
            effects, content = row['corrections']
            if defect == 'candidate':
                effects['after']['realizations']['branches'][0]['member_candidate_ids'] = [B]
            elif defect == 'component':
                effects['after']['realizations']['branches'][0]['component_units'] = {'invented': ['new']}
            elif defect in {'identity', 'guard'}:
                content['after']['standing']['id' if defect == 'identity' else 'conditions'] = 'foreign'
            elif defect == 'unknown_conditions':
                row['corrections'].append({'pointer': '/conditions', 'before': {},
                    'after': {'id': B}, 'reason': 'Fixture foreign metadata.'})
            else:
                effects['after'] = ['pose']
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                review.validate_decision(row, data)

    def delegated_fixture(self, directory):
        root = Path(directory).resolve()
        here = root / 'run'
        for name in ('authored', 'packets', 'worker-notes'):
            (here / name).mkdir(parents=True)
        assignment = {'task_name': '/root/review_test', 'model': 'gpt-6.1-sol',
            'reasoning_effort': 'high', 'start': 0, 'stop': 2}
        note = {'task_name': '/root/review_test', 'model': 'gpt-6.1-sol',
            'reasoning_effort': 'high', 'start': 0, 'stop': 1,
            'complete_source_read': True, 'directly_reviewed_count': 1,
            'unresolved_ordinals': [], 'packet_paths': ['run/packets/test.json'],
            'authored_paths': ['run/authored/test.json']}
        packet = {'ids': [A]}
        review.write(here / 'DELEGATION-ASSIGNMENTS.json', {'assignments': {'review_test': assignment}})
        review.write(here / 'ORDER.json', [A, B])
        review.write(here / 'packets/test.json', packet)
        review.write(here / 'worker-notes/test.json', note)
        return root, here, note, packet

    def test_delegated_review_is_attributed_and_source_range_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, note, packet = self.delegated_fixture(directory)
            with patch.object(review, 'ROOT', root), patch.object(review, 'HERE', here):
                data = fixture(); row = decision(data)
                row['authored_decision']['file'] = 'run/authored/test.json'
                row['packet_sha256'] = review.c.digest(packet)
                row.update(schema=review.DELEGATED_SCHEMA, review_method='codex_subagent_direct_source_read')
                row['review_provenance'] = review.delegated_provenance(
                    'run/worker-notes/test.json', 'run/authored/test.json', row['packet_sha256'], A)
                review.validate_decision(row, data)
                self.assertEqual(row['review_provenance']['task_name'], '/root/review_test')
                with self.assertRaisesRegex(ValueError, 'assigned range'):
                    review.delegated_provenance('run/worker-notes/test.json',
                        'run/authored/test.json', row['packet_sha256'], B)

    def test_same_worker_can_have_distinct_nonoverlapping_assignments(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, note, packet = self.delegated_fixture(directory)
            with patch.object(review, 'ROOT', root), patch.object(review, 'HERE', here):
                path = here / 'DELEGATION-ASSIGNMENTS.json'
                registry = review.c.decode(path.read_bytes())
                first = registry['assignments']['review_test'];first['stop'] = 1
                registry['assignments']['review_next'] = {**first, 'start': 1, 'stop': 2}
                review.write(path, registry)
                provenance = review.delegated_provenance('run/worker-notes/test.json',
                    'run/authored/test.json', review.c.digest(packet), A)
                self.assertEqual(provenance['assignment_id'], 'review_test')

    def test_short_worker_task_name_resolves_its_later_range(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, note, packet = self.delegated_fixture(directory)
            with patch.object(review, 'ROOT', root), patch.object(review, 'HERE', here):
                path = here / 'DELEGATION-ASSIGNMENTS.json'
                registry = review.c.decode(path.read_bytes())
                first = registry['assignments']['review_test'];first['stop'] = 1
                registry['assignments']['review_next'] = {**first, 'start': 1, 'stop': 2}
                review.write(path, registry)
                note.update(task_name='review_test', start=1, stop=2)
                packet['ids'] = [B]
                review.write(here / 'worker-notes/test.json', note)
                review.write(here / 'packets/test.json', packet)
                provenance = review.delegated_provenance('run/worker-notes/test.json',
                    'run/authored/test.json', review.c.digest(packet), B)
                self.assertEqual(provenance['assignment_id'], 'review_next')

    def test_immutable_invocation_cache_hashes_the_complete_packet_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, note, packet = self.delegated_fixture(directory)
            packet_sha = review.c.digest(packet)
            with patch.object(review, 'ROOT', root), patch.object(review, 'HERE', here), \
                    patch.object(review.c, 'digest', wraps=review.c.digest) as digest:
                cache = {}
                for _ in range(2):
                    review.delegated_provenance('run/worker-notes/test.json',
                        'run/authored/test.json', packet_sha, A, cache=cache)
                self.assertEqual(sum(call.args[0] == packet for call in digest.call_args_list), 1)

    def test_reassigned_tail_cannot_be_registered_by_the_old_worker(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, note, packet = self.delegated_fixture(directory)
            with patch.object(review, 'ROOT', root), patch.object(review, 'HERE', here):
                path = here / 'DELEGATION-ASSIGNMENTS.json'
                registry = review.c.decode(path.read_bytes())
                registry['reassignments'] = [{'from_assignment':'review_test', 'start':0, 'stop':1,
                                             'to_assignment':'new_worker'}]
                review.write(path, registry)
                with self.assertRaisesRegex(ValueError, 'explicitly reassigned'):
                    review.delegated_provenance('run/worker-notes/test.json',
                        'run/authored/test.json', review.c.digest(packet), A)

    def test_delegated_worker_cannot_claim_another_model_or_incomplete_read(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, note, packet = self.delegated_fixture(directory)
            with patch.object(review, 'ROOT', root), patch.object(review, 'HERE', here):
                for key, value in [('model', 'gemini'), ('complete_source_read', False),
                                   ('directly_reviewed_count', 0), ('unresolved_ordinals', [2]),
                                   ('stop', 3)]:
                    changed = {**note, key: value}
                    review.write(here / 'worker-notes/test.json', changed)
                    with self.assertRaisesRegex(ValueError, 'identity, assigned range|unique dispatched'):
                        review.delegated_provenance('run/worker-notes/test.json',
                            'run/authored/test.json', review.c.digest(packet), A)

    def test_complete_snapshot_catches_unreviewed_records_and_binding_changes(self):
        data = fixture();data['candidates'][B] = {**copy.deepcopy(data['candidates'][A]), 'id':B}
        baseline = {'source_sha256':review.c.digest(data),
                    'catalog_sha256':review.c.digest(data['slot_catalog']), 'candidate_count':2}
        review.assert_source_snapshot(data, copy.deepcopy(data), baseline, [A, B])
        for changed in ['unreviewed_candidate', 'binding']:
            current = copy.deepcopy(data)
            if changed == 'unreviewed_candidate':current['candidates'][B]['content']['en'] = 'changed'
            else:next(iter(current['slot_bindings'].values()))['weight'] = 0.75
            with self.subTest(changed=changed), self.assertRaisesRegex(ValueError, 'snapshot changed'):
                review.assert_source_snapshot(data, current, baseline, [A, B])
        with self.assertRaisesRegex(ValueError, 'exactly once'):
            review.assert_source_snapshot(data, copy.deepcopy(data), baseline, [A, A])

    def test_claim_limit_cannot_supply_a_positive_role_fact(self):
        data = fixture();row = decision(data)
        data['candidates'][A]['content']['semantics'] = {'claim_limits':['glossy fabric is not proven']}
        row.update(review.binding(data, A))
        row['roles'][0]['evidence'][0].update(pointer='/content/semantics/claim_limits/0')
        with self.assertRaisesRegex(ValueError, 'not positive evidence'):
            review.validate_decision(row, data)

    def test_incorrect_claim_limit_can_be_corrected_without_becoming_positive_evidence(self):
        data = fixture();row = decision(data)
        record = data['candidates'][A]
        record['content']['semantics'] = {'claim_limits':['An unrelated belt must be present.']}
        row.update(review.binding(data, A))
        row['corrections'] = [{'pointer':'/content/semantics/claim_limits/0',
            'before':'An unrelated belt must be present.',
            'after':'Preserve the already declared garment surface.',
            'reason':'Repair a source-specific copied guard without adding a belt.'}]
        review.validate_decision(row, data)
        row['roles'][0]['evidence'][0].update(pointer='/content/semantics/claim_limits/0',
                                             quote='garment surface')
        with self.assertRaisesRegex(ValueError, 'not positive evidence'):
            review.validate_decision(row, data)

    def test_attested_pending_judgement_cannot_be_promoted_to_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, note, packet = self.delegated_fixture(directory)
            with patch.object(review, 'ROOT', root), patch.object(review, 'HERE', here):
                review.write(here / 'worker-notes/test.json', {**note, 'unresolved_ordinals': [0]})
                data = fixture(); row = decision(data)
                row['authored_decision']['file'] = 'run/authored/test.json'
                row['packet_sha256'] = review.c.digest(packet)
                row.update(schema=review.DELEGATED_SCHEMA, review_method='codex_subagent_direct_source_read',
                           status='needs_boundary_review', uncertainties=[{'kind':'owner', 'detail':'Not resolved.'}])
                row['review_provenance'] = review.delegated_provenance(
                    'run/worker-notes/test.json', 'run/authored/test.json', row['packet_sha256'], A)
                review.validate_decision(row, data)
                row.update(status='approved', uncertainties=[])
                with self.assertRaisesRegex(ValueError, 'cannot be counted as approved'):
                    review.validate_decision(row, data)

    def test_changed_worker_attestation_invalidates_compiled_review(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, note, packet = self.delegated_fixture(directory)
            with patch.object(review, 'ROOT', root), patch.object(review, 'HERE', here):
                data = fixture(); row = decision(data)
                row['authored_decision']['file'] = 'run/authored/test.json'
                row['packet_sha256'] = review.c.digest(packet)
                row.update(schema=review.DELEGATED_SCHEMA, review_method='codex_subagent_direct_source_read')
                row['review_provenance'] = review.delegated_provenance(
                    'run/worker-notes/test.json', 'run/authored/test.json', row['packet_sha256'], A)
                review.write(here / 'worker-notes/test.json', {**note, 'extra_note': 'changed'})
                with self.assertRaisesRegex(ValueError, 'changed after review'):
                    review.validate_decision(row, data)

    def test_delegated_document_cannot_escape_run_or_omit_attribution(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, note, packet = self.delegated_fixture(directory)
            with patch.object(review, 'ROOT', root), patch.object(review, 'HERE', here):
                with self.assertRaisesRegex(ValueError, 'outside'):
                    review.delegated_provenance('run/worker-notes/test.json',
                        'elsewhere.json', review.c.digest(packet), A)
                data = fixture(); row = decision(data)
                row.update(schema=review.DELEGATED_SCHEMA, review_method='codex_subagent_direct_source_read')
                with self.assertRaisesRegex(ValueError, 'invalid direct decision'):
                    review.validate_decision(row, data)

    def test_source_mutation_invalidates_decision(self):
        data = fixture(); row = decision(data)
        review.validate_decision(row, data)
        data['candidates'][A]['content']['en'] = 'matte cloth'
        with self.assertRaisesRegex(ValueError, 'changed after review'):
            review.validate_decision(row, data)

    def test_catalog_mutation_invalidates_decision(self):
        data = fixture(); row = decision(data)
        data['slot_catalog']['wardrobe_style']['description'] += ' changed'
        with self.assertRaisesRegex(ValueError, 'changed after review'):
            review.validate_decision(row, data)

    def test_transitive_reference_mutation_invalidates_decision(self):
        data = fixture()
        data['candidates'][B] = {**copy.deepcopy(data['candidates'][A]), 'id': B}
        data['candidates'][A]['content']['canonical_candidate_ref'] = B
        row = decision(data)
        # Preserve reference after the fixture's content replacement.
        data['candidates'][A]['content']['canonical_candidate_ref'] = B
        row.update(review.binding(data, A))
        data['candidates'][B]['conditions'] = {'requires_adult_context': True}
        with self.assertRaisesRegex(ValueError, 'changed after review'):
            review.validate_decision(row, data)

    def test_negative_quote_cannot_qualify_role(self):
        data = fixture(); row = decision(data)
        row['roles'][0]['evidence'][0].update(pointer='/content/confounders/0', quote='leather coat')
        with self.assertRaisesRegex(ValueError, 'not positive evidence'):
            review.validate_decision(row, data)

    def test_wrong_quote_is_rejected(self):
        data = fixture(); row = decision(data)
        row['roles'][0]['evidence'][0]['quote'] = 'blue coat'
        with self.assertRaisesRegex(ValueError, 'quote differs'):
            review.validate_decision(row, data)

    def test_wildcard_owner_cannot_be_approved(self):
        data = fixture(); row = decision(data)
        row['roles'][0]['evidence'][0]['target'] = '*'
        with self.assertRaisesRegex(ValueError, 'concrete'):
            review.validate_decision(row, data)

    def test_foreign_realization_cannot_be_approved(self):
        data = fixture(); row = decision(data)
        row['roles'][0]['realization_ids'] = ['invented_branch']
        with self.assertRaisesRegex(ValueError, 'role contract'):
            review.validate_decision(row, data)

    def test_unresolved_ambiguity_is_never_approved(self):
        data = fixture(); row = decision(data)
        row['uncertainties'] = [{'kind': 'visual_semantic_ambiguity', 'detail': 'Unknown carrier.'}]
        with self.assertRaisesRegex(ValueError, 'unresolved'):
            review.validate_decision(row, data)

    def test_diagnostic_cannot_gain_positive_roles(self):
        data = fixture(); row = decision(data)
        row.update(recommended_kind='diagnostic', status='diagnostic_reviewed')
        with self.assertRaisesRegex(ValueError, 'diagnostic cannot'):
            review.validate_decision(row, data)

    def test_external_model_result_is_not_direct_review(self):
        data = fixture(); row = decision(data)
        row['review_method'] = 'provider_text_review'
        with self.assertRaisesRegex(ValueError, 'direct reviewer'):
            review.validate_decision(row, data)

    def test_role_needs_matching_explicit_branch_fact(self):
        data = fixture(); row = decision(data)
        row['facts'][0]['target'] = 'background'
        with self.assertRaisesRegex(ValueError, 'explicitly authored branch fact'):
            review.validate_decision(row, data)

    def test_source_correction_requires_complete_exact_before_string(self):
        data = fixture(); row = decision(data)
        row['corrections'] = [{'pointer': '/content/en', 'before': 'glossy fabric',
            'after': 'matte fabric', 'reason': 'Incomplete before text is forbidden.'}]
        with self.assertRaisesRegex(ValueError, 'exact current text'):
            review.validate_decision(row, data)


if __name__ == '__main__':
    unittest.main()
