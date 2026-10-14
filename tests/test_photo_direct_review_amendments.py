"""Offline isolated fixtures for sparse worker amendments; no corpus writes."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tests.test_photo_direct_review import review, decision
from tests.test_photo_candidate_corpus import fixture, A, B

PATH = review.HERE / 'delegated_amendments.py'
spec = importlib.util.spec_from_file_location('delegated_amendments', PATH)
amend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(amend)


class AmendmentsTests(unittest.TestCase):
    def setup_run(self, directory):
        root = Path(directory).resolve()
        here = root / 'run'
        for name in ('authored', 'packets', 'worker-notes', 'decisions'):
            (here / name).mkdir(parents=True)
        data = fixture()
        old = decision(data)
        data['candidates'][B] = {**copy.deepcopy(data['candidates'][A]), 'id': B}
        middle = 'cand_' + 'c' * 32
        data['candidates'][middle] = {**copy.deepcopy(data['candidates'][A]), 'id': middle}
        old['status'] = 'needs_boundary_review'
        old['uncertainties'] = [{'kind': 'fixture', 'detail': 'Original pending fixture.'}]
        original = {k: old[k] for k in amend.FIELDS}
        original_path = here / 'authored/original.json'
        authored_path = here / 'authored/amendment.json'
        note_path = here / 'worker-notes/note.json'
        packet = {'ids': [A, B], 'source_sha256': review.c.digest(data),
            'catalog_sha256': review.c.digest(data['slot_catalog']),
            'records': {cid: copy.deepcopy(data['candidates'][cid]) for cid in (A, B)},
            'references': {cid: review.closure(data, cid) for cid in (A, B)}}
        original_tuple = {'file': 'run/authored/original.json', 'item': 1,
                          'sha256': review.c.digest(original)}
        old.update(authored_decision=original_tuple, packet_sha256=review.c.digest(packet))
        replacement = copy.deepcopy(original)
        replacement.update(status='approved', uncertainties=[])
        entry = {'candidate_id': A, 'ordinal': 0, 'decision': replacement,
            'before_authored_file': 'run/authored/original.json',
            'before_authored_row_sha256': original_tuple['sha256'], 'reread_id': 'fixture-A',
            'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
            'source_reread_complete': True, 'reference_reread_complete': True,
            'source_record_sha256': review.binding(data, A)['source_record_sha256'],
            'after_proposal_reference_sha256': {}}
        document = {'schema': 'photo-codex-direct-review-amendment/v1',
            'source_sha256': review.c.digest(data), 'packet_sha256': review.c.digest(packet),
            'amendments': [entry]}
        note = {'task_name': 'worker', 'agent_id': '/root/worker', 'model': 'gpt-6.1-sol',
            'reasoning_effort': 'high', 'authored_paths': ['run/authored/amendment.json'],
            'complete_source_read': True, 'source_sha256': review.c.digest(data),
            'reread_ids': ['fixture-A'], 'packet_paths': ['run/packets/packet.json'],
            'packet_sha256': review.c.digest(packet), 'unresolved_ordinals': [],
            'approved_ordinals': [0], 'approved_count': 1, 'still_pending_count': 0,
            'directly_reread_count': 1}
        registry = {'assignments': {'worker': {'task_name': '/root/worker',
            'model': 'gpt-6.1-sol', 'reasoning_effort': 'high', 'start': 0, 'stop': 3}}}
        original_note = {'task_name': 'worker', 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
            'start': 0, 'stop': 1, 'complete_source_read': True, 'directly_reviewed_count': 1,
            'unresolved_ordinals': [0], 'packet_paths': ['run/packets/packet.json'],
            'authored_paths': ['run/authored/original.json']}
        old.update(schema=review.DELEGATED_SCHEMA, review_method='codex_subagent_direct_source_read',
            review_provenance={'assignment_id': 'worker', 'task_name': '/root/worker',
                'model': 'gpt-6.1-sol', 'reasoning_effort': 'high', 'range': [0, 1],
                'assignment_sha256': review.c.digest(registry['assignments']['worker']),
                'worker_note': {'file': 'run/worker-notes/original-note.json',
                                'sha256': review.c.digest(original_note)}})
        for path, value in [(here / 'worker-notes/original-note.json', original_note), (original_path, {'decisions': [original]}), (authored_path, document),
                (note_path, note), (here / 'ORDER.json', [A, middle, B]),
                (here / 'DELEGATION-ASSIGNMENTS.json', registry),
                (here / 'packets/packet.json', packet),
                (here / 'decisions/batch.json', {'decisions': [old]})]:
            review.write(path, value)
        return root, here, data, authored_path, note_path

    def context(self, root, here, data):
        from contextlib import ExitStack
        stack = ExitStack()
        stack.enter_context(patch.object(review, 'ROOT', root))
        stack.enter_context(patch.object(review, 'HERE', here))
        stack.enter_context(patch.object(review, 'source', return_value=data))
        return stack

    def prepare(self, here, authored, note):
        value = amend.normalize(review, authored, note, actor='/root')
        path = here / 'worker-notes/normalization.json'
        review.write(path, value)
        return path, value

    def test_sparse_wrapper_attribution_and_exact_item_extract(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, data, authored, note = self.setup_run(directory)
            with self.context(root, here, data), patch.object(review, 'verify', return_value={'ok': True}):
                path, manifest = self.prepare(here, authored, note)
                before_authored, before_note = authored.read_bytes(), note.read_bytes()
                result = amend.apply(review, path, actor='/root')
                self.assertEqual(result['revised'], 1)
                row = amend.read(review, here / 'decisions/batch.json')['decisions'][0]
                self.assertEqual(row['review_method'], 'codex_subagent_direct_source_read')
                self.assertEqual(row['review_provenance']['exact_reread_count'], 1)
                self.assertNotIn('range', row['review_provenance'])
                self.assertFalse(row['review_provenance']['root_all_worker_sources_read_claimed'])
                self.assertEqual(review.authored_item(amend.read(review, authored), 1)['status'], 'approved')
                review.validate_decision(row, data)
                self.assertEqual(authored.read_bytes(), before_authored)
                self.assertEqual(note.read_bytes(), before_note)
                with self.assertRaisesRegex(ValueError, 'never overwrite'):
                    amend.apply(review, path, actor='/root')

    def test_actual_full_verify_before_after_in_isolated_fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, data, authored, note = self.setup_run(directory)
            with self.context(root, here, data), patch.object(review.c, 'load', return_value=data):
                review.write(here / 'BASELINE.json', {'source_sha256': review.c.digest(data),
                    'catalog_sha256': review.c.digest(data['slot_catalog']), 'candidate_count': len(data['candidates'])})
                path, _ = self.prepare(here, authored, note)
                result = amend.apply(review, path, actor='/root')
                self.assertEqual(result['progress']['direct_approved_records'], 1)
                self.assertEqual(result['progress']['pending_decisions'], 0)
                self.assertEqual(result['progress']['errors'], {})

    def test_registered_row_worker_format_keeps_immutable_custom_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, data, authored, note_path = self.setup_run(directory)
            with self.context(root, here, data), patch.object(review, 'verify', return_value={}):
                original_doc = amend.read(review, authored)
                decision_row = original_doc['amendments'][0]['decision']
                old = amend.read(review, here / 'decisions/batch.json')['decisions'][0]
                history = {'rows': [{'ordinal': 0, 'registered_path': 'run/decisions/batch.json',
                    'registered_row': old, 'registered_row_sha256': review.c.digest(old)}]}
                history_path = here / 'worker-notes/history.json'; review.write(history_path, history)
                note = {'task_name': '/root/worker', 'agent_id': '/root/worker',
                    'model': 'gpt-6.1-sol', 'reasoning_effort': 'high',
                    'authored_paths': ['run/authored/amendment.json'], 'complete_source_reread': True,
                    'source_snapshot_sha256': review.c.digest(data),
                    'catalog_sha256': review.c.digest(data['slot_catalog']),
                    'directly_reread_ids': [A], 'directly_reread_ordinals': [0], 'directly_reread_count': 1,
                    'packet_path': 'run/worker-notes/history.json', 'pending_retained_ordinals': [],
                    'approved_amendment_count': 1, 'pending_retained_count': 0,
                    'bindings': [{**review.binding(data, A), 'ordinal': 0,
                        'amendment_row_sha256': review.c.digest(decision_row), 'amendment_status': 'approved',
                        'original_registered_row_sha256': review.c.digest(old),
                        'original_registered_file': 'run/decisions/batch.json', 'original_status': old['status'],
                        'original_authored_decision': old['authored_decision']}]}
                review.write(authored, {'decisions': [decision_row]}); review.write(note_path, note)
                before = history_path.read_bytes()
                path, manifest = self.prepare(here, authored, note_path)
                self.assertEqual(manifest['replacements'][0]['reread_artifact']['sha256'], review.c.digest(history))
                amend.apply(review, path, actor='/root')
                self.assertEqual(history_path.read_bytes(), before)
                # History artifact is distinct from the actual full source packet.
                self.assertNotEqual(manifest['replacements'][0]['packet']['file'], 'run/worker-notes/history.json')

    def test_actor_and_wrong_assignment_and_transfer_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, data, authored, note = self.setup_run(directory)
            with self.context(root, here, data):
                with self.assertRaisesRegex(ValueError, 'only root'):
                    amend.normalize(review, authored, note, actor='/root/worker')
                registry_path = here / 'DELEGATION-ASSIGNMENTS.json'
                original = amend.read(review, registry_path)
                for defect in ('task', 'model', 'effort', 'transfer', 'overlap'):
                    registry = copy.deepcopy(original)
                    if defect == 'task': registry['assignments']['worker']['task_name'] = '/root/foreign'
                    elif defect == 'model': registry['assignments']['worker']['model'] = 'foreign'
                    elif defect == 'effort': registry['assignments']['worker']['reasoning_effort'] = 'low'
                    elif defect == 'transfer': registry['reassignments'] = [{'from_assignment': 'worker', 'start': 0, 'stop': 1}]
                    else: registry['assignments']['overlap'] = copy.deepcopy(registry['assignments']['worker'])
                    review.write(registry_path, registry)
                    with self.subTest(defect=defect), self.assertRaises(ValueError):
                        amend.normalize(review, authored, note, actor='/root')

    def test_stale_note_authored_and_source_packet_tampering(self):
        for defect in ('note', 'authored', 'source', 'catalog', 'reference', 'packet'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                root, here, data, authored, note = self.setup_run(directory)
                with self.context(root, here, data):
                    path, manifest = self.prepare(here, authored, note)
                    if defect in {'note', 'authored'}:
                        target = note if defect == 'note' else authored
                        value = amend.read(review, target); value['extra'] = 'tampered'; review.write(target, value)
                    elif defect == 'source': data['candidates'][A]['content']['en'] = 'tampered'
                    elif defect == 'catalog': data['slot_catalog']['wardrobe_style']['description'] += ' changed'
                    elif defect == 'reference': data['candidates'][A]['content']['candidate_ref'] = B
                    else:
                        target = here / 'packets/packet.json'; value = amend.read(review, target)
                        value['records'][B]['content']['en'] = 'tampered unread packet record'; review.write(target, value)
                    with self.assertRaises(ValueError):
                        amend.manifest_entries(review, path, data)

    def test_status_and_new_ids_cannot_be_added_by_root_manifest(self):
        for defect in ('status', 'id', 'count'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                root, here, data, authored, note = self.setup_run(directory)
                with self.context(root, here, data):
                    path, manifest = self.prepare(here, authored, note)
                    if defect == 'status': manifest['replacements'][0]['decision']['status'] = 'needs_source_fix'
                    elif defect == 'id': manifest['replacements'][0]['candidate_id'] = B
                    else: manifest['replacements'].append(copy.deepcopy(manifest['replacements'][0]))
                    review.write(path, manifest)
                    with self.assertRaises(ValueError): amend.manifest_entries(review, path, data)

    def test_stale_compiled_row_and_original_author_tuple_rejected(self):
        for defect in ('row', 'tuple'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as directory:
                root, here, data, authored, note = self.setup_run(directory)
                with self.context(root, here, data), patch.object(review, 'verify', return_value={}):
                    path, _ = self.prepare(here, authored, note)
                    compiled = here / 'decisions/batch.json'; document = amend.read(review, compiled)
                    if defect == 'row': document['decisions'][0]['meaning_summary'] += ' stale'
                    else: document['decisions'][0]['authored_decision']['item'] = 2
                    review.write(compiled, document)
                    with self.assertRaisesRegex(ValueError, 'changed before'):
                        amend.apply(review, path, actor='/root')
                    self.assertFalse((here / 'revisions').exists())

    def test_failed_full_verification_rolls_back_and_preserves_history(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, data, authored, note = self.setup_run(directory)
            with self.context(root, here, data):
                path, _ = self.prepare(here, authored, note)
                compiled = here / 'decisions/batch.json'; before = compiled.read_bytes()
                with patch.object(review, 'verify', side_effect=[{}, ValueError('fixture full verification'), {}]):
                    with self.assertRaisesRegex(ValueError, 'fixture full verification'):
                        amend.apply(review, path, actor='/root')
                self.assertEqual(compiled.read_bytes(), before)
                archive = here / 'revisions/normalization'
                self.assertEqual((archive / 'batch.json').read_bytes(), before)
                audit = amend.read(review, archive / 'REVISION.json')
                self.assertEqual(audit['archive_hashes']['batch.json'], hashlib.sha256(before).hexdigest())
                self.assertTrue((archive / 'ROLLED-BACK.json').exists())
                with self.assertRaisesRegex(ValueError, 'never overwrite'):
                    amend.apply(review, path, actor='/root')

    def test_noncontiguous_exact_reread_set_and_counts(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, data, authored, note_path = self.setup_run(directory)
            with self.context(root, here, data):
                doc = amend.read(review, authored); second = copy.deepcopy(doc['amendments'][0])
                second.update(candidate_id=B, ordinal=2, reread_id='fixture-B',
                    source_record_sha256=review.binding(data, B)['source_record_sha256'])
                second['decision']['candidate_id'] = B
                old_path = here / 'authored/original.json'; olddoc = amend.read(review, old_path)
                old2 = copy.deepcopy(olddoc['decisions'][0]); old2['candidate_id'] = B
                olddoc['decisions'].append(old2); review.write(old_path, olddoc)
                second['before_authored_row_sha256'] = review.c.digest(old2)
                doc['amendments'].append(second); review.write(authored, doc)
                note = amend.read(review, note_path); note.update(reread_ids=['fixture-A', 'fixture-B'],
                    approved_ordinals=[0, 2], approved_count=2, directly_reread_count=2)
                review.write(note_path, note)
                entries = amend.origins(review, authored, note_path, data)
                self.assertEqual([e['ordinal'] for e in entries], [0, 2])
                note['directly_reread_count'] = 3; review.write(note_path, note)
                with self.assertRaisesRegex(ValueError, 'counts'):
                    amend.origins(review, authored, note_path, data)

    def test_pending_attestation_cannot_be_promoted_after_compilation(self):
        with tempfile.TemporaryDirectory() as directory:
            root, here, data, authored, note_path = self.setup_run(directory)
            with self.context(root, here, data), patch.object(review, 'verify', return_value={}):
                doc = amend.read(review, authored); doc['amendments'][0]['decision'].update(
                    status='needs_boundary_review', uncertainties=[{'kind': 'fixture', 'detail': 'Still pending.'}])
                review.write(authored, doc)
                note = amend.read(review, note_path); note.update(approved_ordinals=[], unresolved_ordinals=[0],
                    approved_count=0, still_pending_count=1); review.write(note_path, note)
                path, _ = self.prepare(here, authored, note_path); amend.apply(review, path, actor='/root')
                row = amend.read(review, here / 'decisions/batch.json')['decisions'][0]
                row.update(status='approved', uncertainties=[])
                with self.assertRaisesRegex(ValueError, 'exact worker'):
                    review.validate_decision(row, data)


class NativeProfileProposalTests(unittest.TestCase):
    def profile(self):
        from visual_profile_contracts import compile_visual_profile
        record = fixture()['candidates'][A]
        components = {'contract_version': 'photo-authored-visual-components/v1', 'components': [{
            'id': 'clothing', 'match_terms': ['glossy fabric'], 'evidence_field': 'clothing_phrase',
            'evidence_terms': ['fabric surface'], 'min_content_words': 2,
            'instruction': 'Keep this fabric surface owned by the selected clothing.',
            'render_gate': {'id': 'vo_clothing', 'review_scale': 'both',
                            'description': 'The selected clothing must visibly carry the fabric surface.'}}]}
        profile = {'authored_components': components, 'semantics': {}}
        profile['semantics']['component_semantics'] = compile_visual_profile(profile)['semantics']['component_semantics']
        record['content'] = profile
        after = copy.deepcopy(components)
        after['components'][0]['match_terms'] = ['smooth fabric']
        proposed = copy.deepcopy(profile); proposed['authored_components'] = after
        proposed['semantics'].pop('component_semantics')
        semantics = compile_visual_profile(proposed)['semantics']['component_semantics']
        corrections = [{'pointer': '/content/authored_components', 'before': components,
            'after': after, 'reason': 'Explicit fixture source gate repair.'},
            {'pointer': '/content/semantics/component_semantics',
             'before': profile['semantics']['component_semantics'], 'after': semantics,
             'reason': 'Keep exact native derived component projection consistent.'}]
        return record, corrections

    def test_exact_native_dict_values_and_source_immutability(self):
        record, corrections = self.profile(); before = copy.deepcopy(record)
        proposed = review.corrected_record(record, corrections)
        self.assertEqual(record, before)
        self.assertEqual(proposed['content']['authored_components'], corrections[0]['after'])
        self.assertEqual(proposed['content']['semantics']['component_semantics'], corrections[1]['after'])

    def test_foreign_components_malformed_types_new_refs_and_metadata_rejected(self):
        for defect in ('foreign', 'array', 'null', 'new_ref', 'unknown_ref', 'identity', 'missing_parent', 'old'):
            record, corrections = self.profile()
            if defect == 'foreign': corrections[1]['after']['groups'][0]['id'] = 'foreign'
            elif defect == 'array': corrections[0]['after'] = []
            elif defect == 'null': corrections[1]['after'] = None
            elif defect in {'new_ref', 'unknown_ref'}:
                corrections[0]['after']['components'][0]['match_terms'] = [B if defect == 'new_ref' else 'cand_' + 'e' * 32]
            elif defect == 'identity': corrections[0]['after']['id'] = 'foreign'
            elif defect == 'missing_parent': record['content'].pop('semantics')
            else: corrections[0]['before'] = {'not': 'exact source value'}
            with self.subTest(defect=defect), self.assertRaises(ValueError):
                review.corrected_record(record, corrections)

    def test_structural_validation_does_not_accept_profile_metadata_override(self):
        record, corrections = self.profile()
        corrections.append({'pointer': '/content/id', 'before': None, 'after': {'id': 'foreign'},
                            'reason': 'Fixture forbidden identity override.'})
        with self.assertRaises(ValueError): review.corrected_record(record, corrections)


if __name__ == '__main__':
    unittest.main()
