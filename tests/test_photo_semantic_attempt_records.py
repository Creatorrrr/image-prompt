"""Fault injection for the existing embedding builder; no real API or key."""
from __future__ import annotations

import base64
import contextlib
import copy
import hashlib
import io
import json
import math
import multiprocessing
import os
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import sys
SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0, str(SCRIPTS))
import build_semantic_index as builder
import prompt_generator as generator

MODEL, DIMS, TEXT = 'gemini-embedding-2', 768, ' exact synthetic input\n가짜 문서 '
VALUES = [0.123456789, -0.987654321] + [0.0] * 766
RAW = json.dumps({'embeddings': [{'values': VALUES}], 'usageMetadata': {'promptTokenCount': 7}},
                 ensure_ascii=False, indent=2).encode('utf-8')


def mock_builder_process(checkpoint, result_path, name, data, ready, wrote, release, install_output=False):
    """A separate POSIX process with a fake sender and real filesystem/locks."""
    def deny_network(event, arguments):
        if event.startswith('socket.'):
            raise AssertionError('Mock process forbids network')
    sys.addaudithook(deny_network)
    expected_hash = generator.dictionary_hash(data)
    output = checkpoint.parent / 'index.out'
    real_write = builder.write_payload
    def send(texts, *, raw_response_callback, **kwargs):
        with (checkpoint.parent / 'mock-calls.jsonl').open('a') as stream:
            stream.write(json.dumps({'process': name, 'texts': texts}) + '\n')
        raw_response_callback(200, RAW)
        return [VALUES]
    def write(path, payload, **kwargs):
        if path == (output if install_output else checkpoint):
            wrote.set()
            if name == 'A' and not release.wait(5):
                raise AssertionError('Fixture release timeout')
        result = real_write(path, payload, **kwargs)
        if path == output:
            assert json.loads(output.read_text())['dictionary_hash'] == expected_hash
        return result
    def progress(done, total):
        if done == total:
            assert json.loads(checkpoint.read_text())['dictionary_hash'] == expected_hash
    try:
        ready.set()
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=send), \
             mock.patch.object(builder, 'write_payload', side_effect=write):
            if install_output:
                code = builder.build_and_write_index(mock_build_args(checkpoint, output), data)
                result = {'ok': code == 0, 'return_code': code, 'dictionary_hash': expected_hash}
            else:
                payload = builder.build_resumable_index_payload(data, output=output,
                    checkpoint=checkpoint, provider='gemini', model=MODEL, dimensions=DIMS,
                    batch_size=1, request_interval=0, retry_attempts=0, retry_initial_delay=0,
                    progress_callback=progress, record_embedding_attempts=True)
                result = {'ok': True, 'dictionary_hash': payload['dictionary_hash'],
                          'texts': [row['text'] for row in payload['entries'].values()]}
    except BaseException as exc:
        result = {'ok': False, 'error_type': type(exc).__name__}
    result_path.write_text(json.dumps(result))


def mock_build_args(checkpoint, output):
    return SimpleNamespace(output=output, checkpoint=checkpoint, tags=checkpoint.parent / 'fixture-tags.json',
        provider='gemini', model=MODEL, dimensions=DIMS, batch_size=1, request_interval=0,
        retry_attempts=0, retry_initial_delay=0, no_cache=False, progress=False, shard_count=2,
        keep_stale_generations=True, keep_checkpoint=False, no_runtime_publication=True, record_embedding_attempts=True)


class SemanticAttemptRecordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.checkpoint = Path(self.temp.name) / 'index.partial'
        self.identity, self.record, self.raw = builder.request_record_paths(
            self.checkpoint, TEXT, 'gemini', MODEL, DIMS)
        self.calls = []

    def once(self):
        return builder.embed_recorded_once(TEXT, checkpoint=self.checkpoint,
            provider='gemini', model=MODEL, dimensions=DIMS)

    def sender(self, texts, *, raw_response_callback, **kwargs):
        self.assertEqual(texts, [TEXT])
        self.assertEqual(kwargs['retry_attempts'], 0)
        self.assertTrue(self.record.exists())
        self.assertEqual(json.loads(self.record.read_text())['state'], 'started')
        self.calls.append(texts)
        raw_response_callback(200, RAW)
        return [[round(v, 6) for v in VALUES]]

    def test_success_raw_is_exact_and_second_run_never_calls_sender(self):
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=self.sender) as send:
            self.assertEqual(self.once(), [round(v, 6) for v in VALUES])
            self.assertEqual(self.once(), [round(v, 6) for v in VALUES])
            send.assert_called_once()
        receipt = json.loads(self.raw.read_text())
        self.assertEqual(base64.b64decode(receipt['body_base64']), RAW)
        self.assertEqual(receipt['body_sha256'], hashlib.sha256(RAW).hexdigest())
        self.assertEqual(self.raw.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.record.stat().st_mode & 0o777, 0o600)

    def test_attempt_write_failure_before_commit_makes_zero_transport_calls(self):
        with mock.patch.object(builder, 'atomic_write', side_effect=OSError('fixture precommit')), \
             mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            with self.assertRaises(OSError): self.once()
            send.assert_not_called()
        self.assertFalse(self.record.exists())
        # The first run never reached the durable pre-send boundary or network.
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=self.sender) as send:
            self.once(); send.assert_called_once()

    def test_attempt_write_failure_after_commit_blocks_rerun_before_transport(self):
        real = builder.atomic_write
        def interrupted(path, raw):
            real(path, raw)
            raise OSError('fixture postcommit')
        with mock.patch.object(builder, 'atomic_write', side_effect=interrupted), \
             mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            with self.assertRaises(OSError): self.once()
            send.assert_not_called()
        with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            with self.assertRaisesRegex(RuntimeError, 'no raw response'): self.once()
            send.assert_not_called()
        self.assertEqual(json.loads(self.record.read_text())['state'], 'unknown')

    def test_fault_just_before_transport_leaves_unknown_and_never_resends(self):
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=OSError('fixture before HTTP')) as send:
            with self.assertRaises(RuntimeError): self.once()
            with self.assertRaisesRegex(RuntimeError, 'no resend'): self.once()
            send.assert_called_once()
        self.assertEqual(self.calls, [])
        self.assertEqual(json.loads(self.record.read_text())['state'], 'unknown')

    def test_fault_just_after_response_before_raw_save_never_resends(self):
        def responded(*args, **kwargs):
            self.calls.append('HTTP200 fixture')
            raise OSError('fixture before raw hook')
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=responded) as send:
            with self.assertRaises(RuntimeError): self.once()
            with self.assertRaises(RuntimeError): self.once()
            send.assert_called_once()
        self.assertFalse(self.raw.exists())
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(json.loads(self.record.read_text())['state'], 'unknown')

    def test_sender_returning_vector_without_raw_is_unknown_and_blocks_resend(self):
        with mock.patch.object(builder, 'embed_texts_with_gemini', return_value=[VALUES]) as send:
            for _ in range(2):
                with self.assertRaises(RuntimeError): self.once()
            send.assert_called_once()
        self.assertEqual(json.loads(self.record.read_text())['state'], 'unknown')

    def test_raw_save_failure_before_commit_never_resends(self):
        real = builder.atomic_write
        def interrupted(path, raw):
            if path == self.raw: raise OSError('fixture raw precommit')
            return real(path, raw)
        with mock.patch.object(builder, 'atomic_write', side_effect=interrupted), \
             mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=self.sender) as send:
            with self.assertRaises(RuntimeError): self.once()
            with self.assertRaises(RuntimeError): self.once()
            send.assert_called_once()
        self.assertFalse(self.raw.exists())
        self.assertEqual(json.loads(self.record.read_text())['state'], 'unknown')

    def test_raw_save_failure_after_commit_recovers_without_resend(self):
        real = builder.atomic_write
        def interrupted(path, raw):
            real(path, raw)
            if path == self.raw: raise OSError('fixture raw postcommit')
        with mock.patch.object(builder, 'atomic_write', side_effect=interrupted), \
             mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=self.sender) as send:
            with self.assertRaises(RuntimeError): self.once()
            send.assert_called_once()
        self.assertEqual(json.loads(self.record.read_text())['state'], 'response_saved')
        with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            self.assertEqual(self.once(), [round(v, 6) for v in VALUES])
            send.assert_not_called()

    def test_state_updates_fail_but_valid_raw_recovers_without_resend(self):
        real = builder.atomic_write
        def interrupted(path, raw):
            if path == self.record and json.loads(raw)['state'] != 'started':
                raise OSError('fixture state update failed')
            return real(path, raw)
        with mock.patch.object(builder, 'atomic_write', side_effect=interrupted), \
             mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=self.sender) as send:
            with self.assertRaises(RuntimeError): self.once()
            send.assert_called_once()
        self.assertEqual(json.loads(self.record.read_text())['state'], 'started')
        self.assertTrue(self.raw.exists())
        with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            self.assertEqual(self.once(), [round(v, 6) for v in VALUES])
            send.assert_not_called()
        self.assertEqual(json.loads(self.record.read_text())['state'], 'succeeded')

    def test_confirmed_HTTP_failure_is_saved_and_never_automatically_retried(self):
        def failed(texts, *, raw_response_callback, **kwargs):
            self.calls.append('fixture HTTP503')
            raw_response_callback(503, b'{"error":{"code":503}}')
            raise RuntimeError('fixture503')
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=failed) as send:
            with self.assertRaises(RuntimeError): self.once()
            with self.assertRaises(RuntimeError): self.once()
            send.assert_called_once()
        self.assertEqual(json.loads(self.record.read_text())['state'], 'failed')

    def test_invalid_success_raw_is_preserved_and_blocks_resend(self):
        for values in (VALUES[:-1], [True] + VALUES[1:], [math.inf] + VALUES[1:]):
            with self.subTest(values_type=type(values[0]).__name__), tempfile.TemporaryDirectory() as directory:
                checkpoint = Path(directory) / 'index.partial'
                def invalid(texts, *, raw_response_callback, **kwargs):
                    raw_response_callback(200, json.dumps({'embeddings': [{'values': values}]}).encode())
                    return [values]
                with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=invalid) as send:
                    for _ in range(2):
                        with self.assertRaises(RuntimeError):
                            builder.embed_recorded_once(TEXT, checkpoint=checkpoint,
                                provider='gemini', model=MODEL, dimensions=DIMS)
                    send.assert_called_once()

    def test_missing_raw_even_after_success_marks_unknown_without_resend(self):
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=self.sender): self.once()
        self.raw.unlink()
        with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            with self.assertRaisesRegex(RuntimeError, 'no raw response'): self.once()
            send.assert_not_called()
        self.assertEqual(json.loads(self.record.read_text())['state'], 'unknown')

    def test_corrupt_record_or_raw_never_calls_sender(self):
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=self.sender): self.once()
        original = self.raw.read_bytes(); self.raw.write_bytes(b'{}')
        with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            with self.assertRaises(RuntimeError): self.once()
            send.assert_not_called()
        self.raw.write_bytes(original); self.record.write_bytes(b'broken JSON')
        with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            with self.assertRaises(ValueError): self.once()
            send.assert_not_called()

    def test_null_or_nonobject_attempt_record_is_not_treated_as_unstarted(self):
        self.record.parent.mkdir(parents=True)
        for value in (None, [], 'fixture'):
            with self.subTest(value_type=type(value).__name__):
                self.record.write_text(json.dumps(value))
                with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
                    with self.assertRaises(RuntimeError): self.once()
                    send.assert_not_called()

    def test_stopped_or_corrupt_state_is_not_promoted_by_valid_raw(self):
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=self.sender): self.once()
        original = json.loads(self.record.read_text())
        raw_bytes = self.raw.read_bytes()
        for state in ('failed', 'unknown', 'invalid-state', None, [], {}, 'missing'):
            with self.subTest(state=state):
                row = {**original, 'state': state}
                if state == 'missing': del row['state']
                self.record.write_bytes(builder.canonical_bytes(row))
                record_bytes = self.record.read_bytes()
                with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
                    with self.assertRaisesRegex(RuntimeError, 'no resend'): self.once()
                    send.assert_not_called()
                self.assertEqual(self.record.read_bytes(), record_bytes)
                self.assertEqual(self.raw.read_bytes(), raw_bytes)

    def test_broken_links_and_nonregular_evidence_block_send_and_overwrite(self):
        for artifact in ('record', 'raw', 'lock', 'directory'):
            for entry_type in ('dangling', 'live', 'nonregular'):
                with self.subTest(artifact=artifact, entry_type=entry_type), tempfile.TemporaryDirectory() as directory:
                    checkpoint = Path(directory) / 'index.partial'
                    _, record, raw = builder.request_record_paths(checkpoint, TEXT, 'gemini', MODEL, DIMS)
                    path = {'record': record, 'raw': raw, 'lock': record.with_suffix('.lock'),
                            'directory': record.parent}[artifact]
                    path.parent.mkdir(parents=True, exist_ok=True)
                    target = Path(directory) / 'link-target'
                    if entry_type == 'live':
                        if artifact == 'directory': target.mkdir()
                        else: target.write_bytes(b'preserved fixture')
                    if entry_type != 'nonregular':
                        path.symlink_to(target, target_is_directory=artifact == 'directory')
                    elif artifact == 'directory':
                        path.write_bytes(b'existing non-directory fixture')
                    else:
                        path.mkdir()
                    before = path.lstat()
                    with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
                        with self.assertRaises((RuntimeError, OSError)):
                            builder.embed_recorded_once(TEXT, checkpoint=checkpoint,
                                provider='gemini', model=MODEL, dimensions=DIMS)
                        send.assert_not_called()
                    self.assertEqual(path.lstat().st_ino, before.st_ino)
                    self.assertEqual(path.lstat().st_mode, before.st_mode)
                    if entry_type == 'live':
                        if artifact == 'directory': self.assertEqual(list(target.iterdir()), [])
                        else: self.assertEqual(target.read_bytes(), b'preserved fixture')

    def test_attempt_ancestors_are_synced_before_sender(self):
        checkpoint = Path(self.temp.name) / 'new' / 'nested' / 'index.partial'
        _, record, _ = builder.request_record_paths(checkpoint, TEXT, 'gemini', MODEL, DIMS)
        synced = set()
        real_fsync = os.fsync
        def trace(fd):
            real_fsync(fd)
            info = os.fstat(fd)
            synced.add((info.st_dev, info.st_ino))
        def send(texts, *, raw_response_callback, **kwargs):
            for ancestor in (record.parent.resolve(), *record.parent.resolve().parents):
                info = ancestor.stat()
                self.assertIn((info.st_dev, info.st_ino), synced)
            raw_response_callback(200, RAW)
            return [VALUES]
        with mock.patch.object(os, 'fsync', side_effect=trace), \
             mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=send) as sender:
            builder.embed_recorded_once(TEXT, checkpoint=checkpoint,
                provider='gemini', model=MODEL, dimensions=DIMS)
            sender.assert_called_once()

    def test_concurrent_same_input_has_only_one_mock_transport_call(self):
        entered, release = threading.Event(), threading.Event()
        def slow(*args, **kwargs):
            entered.set()
            self.assertTrue(release.wait(3))
            return self.sender(*args, **kwargs)
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=slow) as send, \
             ThreadPoolExecutor(max_workers=2) as pool:
            first = pool.submit(self.once)
            self.assertTrue(entered.wait(3))
            second = pool.submit(self.once)
            release.set()
            self.assertEqual(first.result(3), second.result(3))
            send.assert_called_once()

    def check_two_process_builds(self, different, *, install=False, separate_checkpoint=False):
        context = multiprocessing.get_context('fork')
        with tempfile.TemporaryDirectory() as directory:
            release = context.Event()
            processes, ready, wrote, results, checkpoints, data_rows = [], [], [], [], [], []
            for name in ('A', 'B'):
                label = 'synthetic row ' + (name if different else 'same')
                data = {'version': 'fixture', 'slots': {'prop': [{'id': 'target', 'en': label}]}}
                data_rows.append(data)
                checkpoints.append(Path(directory) / ((name if separate_checkpoint else 'index') + '.partial'))
                ready.append(context.Event()); wrote.append(context.Event())
                results.append(Path(directory) / (name + '-result.json'))
                processes.append(context.Process(target=mock_builder_process,
                    args=(checkpoints[-1], results[-1], name, data, ready[-1], wrote[-1], release, install)))
            try:
                processes[0].start()
                self.assertTrue(wrote[0].wait(5))
                if install: self.assertTrue(checkpoints[0].exists())
                processes[1].start()
                self.assertTrue(ready[1].wait(5))
                # A pauses at the real checkpoint/manifest write while holding its locks.
                self.assertFalse(wrote[1].wait(0.2))
            finally:
                release.set()
                for process in processes:
                    if process.pid is not None:
                        process.join(5)
                        if process.is_alive():
                            process.terminate(); process.join(5)
            for process, result_path, data in zip(processes, results, data_rows):
                self.assertEqual(process.exitcode, 0)
                result = json.loads(result_path.read_text())
                self.assertTrue(result['ok'], result)
                self.assertEqual(result['dictionary_hash'], generator.dictionary_hash(data))
                if not install:
                    row = generator.iter_semantic_entries(data)[0]
                    self.assertEqual(result['texts'], [generator.semantic_text_for_entry(row[2], row[3], kind=row[1])])
            calls = (Path(directory) / 'mock-calls.jsonl').read_text().splitlines()
            self.assertEqual(len(calls), 2 if different else 1)
            payload = builder.load_payload(Path(directory) / 'index.out') if install else json.loads(checkpoints[0].read_text())
            self.assertEqual(payload['dictionary_hash'], generator.dictionary_hash(data_rows[1]))
            row = generator.iter_semantic_entries(data_rows[1])[0]
            self.assertEqual(payload['entries'][row[0]]['text'], generator.semantic_text_for_entry(row[2], row[3], kind=row[1]))
            if install: self.assertTrue(all(not checkpoint.exists() for checkpoint in checkpoints))

    def test_two_process_builds_serialize_checkpoint_for_same_and_different_input(self):
        for different in (False, True):
            with self.subTest(different=different):
                self.check_two_process_builds(different)

    def test_two_process_output_install_and_cleanup_hold_both_locks(self):
        for different, separate in ((False, False), (True, False), (True, True)):
            with self.subTest(different=different, separate_checkpoint=separate):
                self.check_two_process_builds(different, install=True, separate_checkpoint=separate)

    def test_output_save_failure_recovers_without_resend_before_cleanup(self):
        data = {'version': 'fixture', 'slots': {'prop': [{'id': 'target', 'en': 'synthetic output recovery'}]}}
        output = self.checkpoint.with_suffix('.out')
        args = mock_build_args(self.checkpoint, output)
        real_write = builder.write_payload
        def response(texts, *, raw_response_callback, **kwargs):
            raw_response_callback(200, RAW)
            return [VALUES]
        def interrupted(path, payload, **kwargs):
            if path == output: raise OSError('fixture final manifest interrupted')
            return real_write(path, payload, **kwargs)
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=response) as send:
            with mock.patch.object(builder, 'write_payload', side_effect=interrupted):
                with self.assertRaises(OSError): builder.build_and_write_index(args, data)
            self.assertTrue(self.checkpoint.exists())
            self.assertEqual(builder.build_and_write_index(args, data), 0)
            send.assert_called_once()
        self.assertFalse(self.checkpoint.exists())
        self.assertEqual(builder.load_payload(output)['dictionary_hash'], generator.dictionary_hash(data))

    def test_checkpoint_failure_reexecution_recovers_target_and_preserves_other_vector(self):
        data = {'version': 'fixture', 'slots': {'prop': [
            {'id': 'target', 'en': 'synthetic target'}, {'id': 'kept', 'en': 'synthetic kept'}]}}
        rows = generator.iter_semantic_entries(data)
        seed = builder.base_payload(data, 'gemini', MODEL, DIMS)
        kept = rows[1]; key, kind, entry, slot = kept
        seed['entries'] = {key: {'kind': kind, 'slot': slot, 'id': entry['id'],
            'text': generator.semantic_text_for_entry(entry, slot, kind=kind), 'vector': [0.2] + [0.0] * 767}}
        builder.write_payload(self.checkpoint, seed)
        def build():
            return builder.build_resumable_index_payload(data, output=self.checkpoint.with_suffix('.out'),
                checkpoint=self.checkpoint, provider='gemini', model=MODEL, dimensions=DIMS,
                batch_size=1, request_interval=0, retry_attempts=0, retry_initial_delay=0, record_embedding_attempts=True)
        def response(texts, *, raw_response_callback, **kwargs):
            raw_response_callback(200, RAW)
            return [[round(v, 6) for v in VALUES]]
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=response) as send:
            with mock.patch.object(builder, 'write_payload', side_effect=OSError('fixture checkpoint save')):
                with self.assertRaises(OSError): build()
            result = build()
            send.assert_called_once()
        self.assertEqual(result['entries'][key]['text'], seed['entries'][key]['text'])
        self.assertEqual(result['entries'][key]['vector'], seed['entries'][key]['vector'])
        self.assertEqual(result['entries'][rows[0][0]]['vector'], [round(v, 6) for v in VALUES])
        self.assertEqual(json.loads(self.checkpoint.read_text())['entries'][rows[0][0]]['vector'],
                         [round(v, 6) for v in VALUES])

    def test_unknown_later_row_blocks_new_earlier_row_before_any_send(self):
        data = {'version': 'fixture', 'slots': {'prop': [
            {'id': 'new', 'en': 'new synthetic row'}, {'id': 'unknown', 'en': 'unknown synthetic row'}]}}
        rows = generator.iter_semantic_entries(data)
        key, kind, entry, slot = rows[1]
        text = generator.semantic_text_for_entry(entry, slot, kind=kind)
        with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=OSError('fixture stop')):
            with self.assertRaises(RuntimeError):
                builder.embed_recorded_once(text, checkpoint=self.checkpoint,
                    provider='gemini', model=MODEL, dimensions=DIMS)
        with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            with self.assertRaises(RuntimeError):
                builder.build_resumable_index_payload(data, output=self.checkpoint.with_suffix('.out'),
                    checkpoint=self.checkpoint, provider='gemini', model=MODEL, dimensions=DIMS,
                    batch_size=1, request_interval=0, retry_attempts=0, retry_initial_delay=0, record_embedding_attempts=True)
            send.assert_not_called()

    def test_fsync_failure_windows_never_duplicate_transport(self):
        import core_slot_index_storage
        real_fsync = core_slot_index_storage.os.fsync
        ancestry_syncs = len(self.record.parent.resolve().parents) + 1
        for fail_at in range(1, ancestry_syncs + 7):
            with self.subTest(fsync_call=fail_at), tempfile.TemporaryDirectory() as directory:
                checkpoint = Path(directory) / 'index.partial'
                calls, syncs = [], []
                def sender(texts, *, raw_response_callback, **kwargs):
                    calls.append('fixture transport')
                    raw_response_callback(200, RAW)
                    return [VALUES]
                def interrupted(fd):
                    syncs.append(fd)
                    if len(syncs) == fail_at: raise OSError('fixture fsync interrupted')
                    return real_fsync(fd)
                def invoke():
                    return builder.embed_recorded_once(TEXT, checkpoint=checkpoint,
                        provider='gemini', model=MODEL, dimensions=DIMS)
                with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=sender), \
                     mock.patch.object(core_slot_index_storage.os, 'fsync', side_effect=interrupted):
                    with self.assertRaises((OSError, RuntimeError)): invoke()
                with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=sender) as send:
                    if fail_at in (ancestry_syncs + 2, ancestry_syncs + 3):
                        with self.assertRaises(RuntimeError): invoke()
                        send.assert_not_called()
                    else:
                        self.assertEqual(invoke(), [round(v, 6) for v in VALUES])
                        self.assertEqual(send.call_count, 1 if fail_at <= ancestry_syncs + 1 else 0)
                self.assertEqual(len(calls), 0 if fail_at == ancestry_syncs + 2 else 1)

    def test_builder_rejects_nonzero_retry_or_multitext_before_sender(self):
        for batch, retries in ((2, 0), (1, 4)):
            with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
                with self.assertRaises(ValueError):
                    builder.build_resumable_index_payload({'slots': {}}, output=self.checkpoint,
                        checkpoint=self.checkpoint, provider='gemini', model=MODEL, dimensions=DIMS,
                        batch_size=batch, request_interval=0, retry_attempts=retries, retry_initial_delay=0, record_embedding_attempts=True)
                send.assert_not_called()

    def test_default_parser_keeps_legacy_retry_and_requires_explicit_safe_mode(self):
        parser = builder.build_argument_parser()
        args = parser.parse_args([])
        self.assertEqual((args.batch_size, args.retry_attempts, args.record_embedding_attempts), (1, 4, False))
        args = parser.parse_args(['--record-embedding-attempts'])
        with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
            with self.assertRaisesRegex(ValueError, 'retry-attempts=0'):
                builder.build_and_write_index(args, {'slots': {}})
            send.assert_not_called()
        args = parser.parse_args(['--record-embedding-attempts', '--retry-attempts', '0'])
        self.assertEqual((args.batch_size, args.retry_attempts, args.record_embedding_attempts), (1, 0, True))

    def test_unselected_mode_preserves_batch_retry_cache_writer_and_permissions(self):
        data = {'version': 'fixture', 'slots': {'prop': [{'id': str(i), 'en': 'synthetic ' + str(i)} for i in range(3)]}}
        output = self.checkpoint.with_suffix('.out')
        calls = []
        real_write = builder.write_payload
        def legacy_write(path, payload, *, compact=False):
            return real_write(path, payload, compact=compact)
        def send(texts, **kwargs):
            self.assertNotIn('raw_response_callback', kwargs)
            self.assertEqual(kwargs['retry_attempts'], 4)
            calls.append(len(texts))
            return [[round(v, 6) for v in VALUES] for _ in texts]
        def build():
            return builder.build_resumable_index_payload(data, output=output, checkpoint=self.checkpoint,
                provider='gemini', model=MODEL, dimensions=DIMS, batch_size=2, request_interval=0,
                retry_attempts=4, retry_initial_delay=0)
        before_umask = os.umask(0o022)
        try:
            with mock.patch.object(builder, 'embed_texts_with_gemini', side_effect=send), \
                 mock.patch.object(builder, 'file_lock', side_effect=AssertionError('Legacy path must not lock')), \
                 mock.patch.object(os, 'fsync', side_effect=AssertionError('Legacy path must not fsync')), \
                 mock.patch.object(builder, 'write_payload', side_effect=legacy_write):
                first = build(); second = build()
                self.assertEqual(first, second)
                self.assertEqual(calls, [2, 1])
                manifest = builder.write_sharded_payload(output, second, shard_count=2)
            self.assertEqual(self.checkpoint.stat().st_mode & 0o777, 0o644)
            self.assertEqual(output.stat().st_mode & 0o777, 0o644)
            for row in manifest['shards']:
                self.assertEqual((output.parent / row['path']).stat().st_mode & 0o777, 0o644)
            self.assertEqual(list(Path(self.temp.name).glob('*.embedding-attempts')), [])
        finally:
            os.umask(before_umask)

    def test_legacy_sender_still_retries_with_cached_client(self):
        client = mock.Mock()
        client.models.embed_content.side_effect = [RuntimeError('503 fixture'),
            SimpleNamespace(embeddings=[SimpleNamespace(values=VALUES)])]
        with mock.patch.object(generator, 'get_gemini_api_key', return_value='mock-only'), \
             mock.patch.object(generator, 'cached_gemini_client', return_value=client) as cache:
            self.assertEqual(generator.embed_texts_with_gemini([TEXT], model=MODEL, dimensions=DIMS,
                retry_attempts=4, retry_initial_delay=0), [[round(v, 6) for v in VALUES]])
        self.assertEqual(client.models.embed_content.call_count, 2)
        cache.assert_called_once_with('mock-only')
        client.close.assert_not_called()

    def test_recorded_namespace_cannot_fall_back_to_unselected_sender(self):
        data = {'version': 'fixture', 'slots': {'prop': [{'id': 'target', 'en': 'synthetic namespace'}]}}
        output = self.checkpoint.with_suffix('.out')
        for protected_path in (self.checkpoint, output):
            directory = protected_path.with_name(protected_path.name + '.embedding-attempts')
            directory.mkdir()
            before = directory.stat().st_ino
            with mock.patch.object(builder, 'embed_texts_with_gemini') as send:
                with self.assertRaisesRegex(ValueError, 'no unrecorded resume'):
                    builder.build_resumable_index_payload(data, output=output, checkpoint=self.checkpoint,
                        provider='gemini', model=MODEL, dimensions=DIMS, batch_size=2, request_interval=0,
                        retry_attempts=4, retry_initial_delay=0)
                args = mock_build_args(self.checkpoint, output)
                args.record_embedding_attempts = False
                with self.assertRaisesRegex(ValueError, 'no unrecorded resume'):
                    builder.build_and_write_index(args, data)
                send.assert_not_called()
            self.assertEqual(directory.stat().st_ino, before)
            directory.rmdir()

    def test_missing_key_diagnostic_is_allowlisted_without_leaking_other_errors(self):
        missing = 'GEMINI_API_KEY or GOOGLE_API_KEY is required for Gemini semantic embeddings.'
        data = {'version': 'fixture', 'slots': {'prop': [{'id': 'target', 'en': 'synthetic config failure'}]}}
        for message in (missing, 'GEMINI_API_KEY private fixture error'):
            with self.subTest(known_diagnostic=message == missing), tempfile.TemporaryDirectory() as directory:
                checkpoint = Path(directory) / 'index.partial'
                args = mock_build_args(checkpoint, checkpoint.with_suffix('.out'))
                stderr = io.StringIO()
                with mock.patch.object(generator, 'get_gemini_api_key', side_effect=RuntimeError(message)) as getter, \
                     mock.patch('google.genai.Client') as client, contextlib.redirect_stderr(stderr):
                    self.assertEqual(builder.build_and_write_index(args, data), 1)
                    getter.assert_called_once(); client.assert_not_called()
                    initial_error = stderr.getvalue()
                    row = generator.iter_semantic_entries(data)[0]
                    text = generator.semantic_text_for_entry(row[2], row[3], kind=row[1])
                    _, record, raw = builder.request_record_paths(checkpoint, text, 'gemini', MODEL, DIMS)
                    before = record.read_bytes()
                    self.assertEqual(json.loads(before)['state'], 'unknown')
                    self.assertFalse(raw.exists())
                    self.assertEqual(builder.build_and_write_index(args, data), 1)
                    getter.assert_called_once(); client.assert_not_called()
                    self.assertEqual(record.read_bytes(), before)
                self.assertEqual(missing in initial_error, message == missing)
                self.assertNotIn('private fixture error', initial_error)
                self.assertIn('no automatic retry', initial_error)

    def test_real_SDK_mock_transport_captures_raw_before_success_or_failure(self):
        import httpx
        from google import genai
        real_client = genai.Client
        for status in (200, 503):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                checkpoint = Path(directory) / 'index.partial'
                observed = []
                body = RAW if status == 200 else b'{"error":{"code":503,"message":"fixture","status":"UNAVAILABLE"}}'
                def transport(request):
                    observed.append(request)
                    return httpx.Response(status, content=body)
                def factory(**kwargs):
                    self.assertEqual(kwargs['api_key'], 'mock-only')
                    options = kwargs['http_options']
                    self.assertEqual(options.retry_options.attempts, 1)
                    self.assertIs(options.client_args['follow_redirects'], False)
                    options.client_args.update(transport=httpx.MockTransport(transport), trust_env=False)
                    return real_client(**kwargs)
                def invoke():
                    return builder.embed_recorded_once(TEXT, checkpoint=checkpoint,
                        provider='gemini', model=MODEL, dimensions=DIMS)
                with mock.patch.object(generator, 'get_gemini_api_key', return_value='mock-only'), \
                     mock.patch('google.genai.Client', side_effect=factory):
                    if status == 200:
                        self.assertEqual(invoke(), [round(v, 6) for v in VALUES]); invoke()
                    else:
                        for _ in range(2):
                            with self.assertRaises(RuntimeError): invoke()
                self.assertEqual(len(observed), 1)
                identity, record, raw_path = builder.request_record_paths(checkpoint, TEXT, 'gemini', MODEL, DIMS)
                self.assertEqual(base64.b64decode(json.loads(raw_path.read_text())['body_base64']), body)
                self.assertNotIn('mock-only', record.read_text())
                self.assertNotIn('mock-only', raw_path.read_text())
                if status == 200:
                    request_body = json.loads(observed[0].content)
                    self.assertNotIn('taskType', json.dumps(request_body))
                    self.assertIn(TEXT, json.dumps(request_body, ensure_ascii=False).replace('\\n', '\n'))


if __name__ == '__main__':
    unittest.main()
