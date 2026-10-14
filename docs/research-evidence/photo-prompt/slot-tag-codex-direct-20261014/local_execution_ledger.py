"""Append-only local inference accounting; importing this module never infers.

An unsuccessful provider call may have executed inputs before failing. Its exact
count is unknown, never zero. Planned runs are definitely unstarted; started runs
without a complete validated receipt remain unknown. No automatic retry exists.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def write_once(path, value):
    """Exclusive create + fsync, never replace an earlier artifact."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = canonical(value)
    with path.open('xb') as stream:
        stream.write(body)
        stream.flush()
        os.fsync(stream.fileno())
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return {'path': str(path.resolve()), 'sha256': hashlib.sha256(body).hexdigest()}


def read(path):
    return json.loads(Path(path).read_bytes())


class Ledger:
    def __init__(self, directory):
        self.directory = Path(directory).resolve()

    def _run(self, run_id):
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,95}', run_id):
            raise ValueError('unsafe run ID')
        return self.directory / run_id

    def plan(self, run_id, inputs, *, binding, space, kind='query'):
        if kind not in {'query', 'document'}:
            raise ValueError('unsupported inference kind')
        if space.get('provider') != 'embeddinggemma2-local':
            raise ValueError('ledger permits explicitly bound local inference only')
        if not inputs or any(not isinstance(x, str) or not x.strip() for x in inputs):
            raise ValueError('nonempty exact inputs required')
        run = self._run(run_id)
        # A reused run ID cannot create a fresh plan even after a failed call.
        run.mkdir(parents=True, exist_ok=False)
        plan = {'schema': 'photo-direct-local-plan/v1', 'run_id': run_id,
                'kind': kind, 'space': space, 'binding': binding,
                'expected_input_count': len(inputs),
                'input_sha256': [hashlib.sha256(t.encode()).hexdigest() for t in inputs]}
        write_once(run / 'planned.json', plan)
        return plan

    def start(self, run_id):
        run = self._run(run_id)
        plan = read(run / 'planned.json')
        if (run / 'outcome.json').exists():
            raise ValueError('run already has outcome')
        started = {'schema': 'photo-direct-local-start/v1', 'run_id': run_id,
                   'planned_sha256': digest(plan),
                   'started_at': datetime.now(timezone.utc).isoformat(),
                   'expected_input_count': plan['expected_input_count']}
        write_once(run / 'started.json', started)
        return started

    def finish(self, run_id, *, state, receipts, result_reference=None, error_type=None):
        run = self._run(run_id)
        plan = read(run / 'planned.json')
        started = read(run / 'started.json')
        if started['planned_sha256'] != digest(plan):
            raise ValueError('changed execution plan')
        if state not in {'complete', 'failed'}:
            raise ValueError('explicit complete/failed state required')
        ids = [r['input_index'] for r in receipts]
        if len(set(ids)) != len(ids) or any(type(i) is not int or not 0 <= i < plan['expected_input_count'] for i in ids):
            raise ValueError('duplicate/foreign receipt')
        for receipt in receipts:
            if (receipt.get('validated') is not True or type(receipt.get('cache_hit')) is not bool
                    or receipt.get('text_sha256') != plan['input_sha256'][receipt['input_index']]
                    or not re.fullmatch('[a-f0-9]{64}', str(receipt.get('trace_sha256', '')))):
                raise ValueError('validated exact execution receipt required')
        if state == 'complete' and (len(receipts) != plan['expected_input_count'] or not result_reference):
            raise ValueError('complete requires every execution receipt and saved result')
        outcome = {'schema': 'photo-direct-local-outcome/v1', 'run_id': run_id,
                   'planned_sha256': digest(plan), 'started_sha256': digest(started),
                   'state': state, 'expected_input_count': plan['expected_input_count'],
                   'confirmed_fresh_inference_count': sum(not r['cache_hit'] for r in receipts),
                   'confirmed_cache_hit_count': sum(r['cache_hit'] for r in receipts),
                   'exact_fresh_inference_count': sum(not r['cache_hit'] for r in receipts) if state == 'complete' else None,
                   'receipts': receipts, 'result_reference': result_reference,
                   'error_type': error_type}
        write_once(run / 'outcome.json', outcome)
        return outcome

    def summary(self):
        minimum = 0
        cache_hits = 0
        unknown = []
        planned = []
        for path in sorted(self.directory.glob('*/planned.json')):
            plan = read(path)
            run = path.parent
            if not (run / 'started.json').exists():
                planned.append(plan['run_id'])
                continue
            started = read(run / 'started.json')
            if started['planned_sha256'] != digest(plan):
                raise ValueError('ledger plan changed')
            if not (run / 'outcome.json').exists():
                unknown.append(plan['run_id'])
                continue
            outcome = read(run / 'outcome.json')
            if outcome['planned_sha256'] != digest(plan) or outcome['started_sha256'] != digest(started):
                raise ValueError('ledger trace chain changed')
            receipts = outcome['receipts']
            indices = [r['input_index'] for r in receipts]
            fresh = sum(r['cache_hit'] is False for r in receipts)
            hits = sum(r['cache_hit'] is True for r in receipts)
            if (len(indices) != len(set(indices))
                    or any(type(i) is not int or not 0 <= i < plan['expected_input_count'] for i in indices)
                    or any(r.get('validated') is not True or type(r.get('cache_hit')) is not bool
                           or r['text_sha256'] != plan['input_sha256'][r['input_index']]
                           or not re.fullmatch('[a-f0-9]{64}', str(r.get('trace_sha256', ''))) for r in receipts)
                    or outcome['confirmed_fresh_inference_count'] != fresh
                    or outcome['confirmed_cache_hit_count'] != hits
                    or outcome['expected_input_count'] != plan['expected_input_count']
                    or outcome['state'] not in {'complete', 'failed'}
                    or outcome['exact_fresh_inference_count'] != (fresh if outcome['state'] == 'complete' else None)
                    or (outcome['state'] == 'complete' and len(receipts) != plan['expected_input_count'])):
                raise ValueError('ledger outcome accounting changed')
            minimum += outcome['confirmed_fresh_inference_count']
            cache_hits += outcome['confirmed_cache_hit_count']
            if outcome['state'] != 'complete':
                unknown.append(plan['run_id'])
        return {'confirmed_minimum': minimum, 'exact_total': None if unknown else minimum,
                'confirmed_cache_hits': cache_hits, 'unknown_run_ids': unknown,
                'planned_unstarted_run_ids': planned,
                'scope': 'only runs recorded in this ledger; not historical/global totals'}
