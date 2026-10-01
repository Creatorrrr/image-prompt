#!/usr/bin/env python3
"""Simulate a published clone lacking private refs/objects; read-only validation."""
from pathlib import Path
from types import SimpleNamespace
from unittest import mock
import json
import cycle_common as c


def main():
    original_git = c.git
    original_run = c.subprocess.run
    calls = []

    def no_private_git(*args):
        calls.append(list(args))
        if any('data-reef-wave-deferred-20261001' in arg or '1f7e4915dadb840f84b2f9c427449d5f0a876f05' in arg for arg in args):
            raise AssertionError('Private historical Git ref/object lookup attempted')
        return original_git(*args)

    def missing_private_ref(command, *args, **kwargs):
        if command[:3] == ['git', 'rev-parse', '--verify'] and command[-1] == 'refs/heads/data-reef-wave-deferred-20261001':
            return SimpleNamespace(returncode=1, stdout=b'')
        return original_run(command, *args, **kwargs)

    with mock.patch.object(c, 'git', side_effect=no_private_git), mock.patch.object(c.subprocess, 'run', side_effect=missing_private_ref):
        frozen = c.load_freeze()
        states = c.states_from_freeze(frozen)
        cache = c.load_reused_cache(frozen)
        index, shards = c.load_baseline_index(frozen, states['baseline'])
        old = c.read_json(c.E / 'preparation-revisions/revision-01-frozen-inventory-queries.json')
        c.require(frozen['inventory'] == old['inventory'], 'Inventory/proposal values changed during packaging')
        c.require([{k:v for k,v in q.items() if k != 'source_snapshot_file'} for q in frozen['queries']] == old['queries'], 'Probe values/provenance changed during packaging')
        c.require({h:{k:v for k,v in p.items() if k != 'source_snapshot_file'} for h,p in frozen['reused_cache_provenance'].items()} == old['reused_cache_provenance'], 'Cache provenance changed during packaging')
        c.require(frozen['fresh_document'] == old['fresh_document'] and frozen['state_dictionary_hashes'] == old['state_dictionary_hashes'], 'Source/state payload changed during packaging')
        c.require(c.sha((c.E / 'reused-vector-cache.json').read_bytes()) == old['artifact_sha256']['reused-vector-cache.json'], 'Reused cache bytes changed')
    print(json.dumps({
        'status':'pass_private_ref_and_objects_simulated_absent',
        'freeze_sha256':c.sha((c.E/'frozen-inventory-queries.json').read_bytes()),
        'private_git_lookups':0, 'allowed_public_git_lookups':calls,
        'exact_included_cache_sources':len({p['source_snapshot_file'] for p in frozen['reused_cache_provenance'].values()}),
        'exact_included_query_inventories':len({q['source_snapshot_file'] for q in frozen['queries']}),
        'validated_cache_records':len(cache), 'validated_baseline_documents':len(index['entries']),
        'validated_baseline_shards':len(shards), 'inventory_rows':len(frozen['inventory']),
        'queries':len(frozen['queries']), 'planned_result_rows':180,
        'pending_document_sha256':frozen['fresh_document']['sha256'],
        'pending_document_utf8_bytes':frozen['fresh_document']['utf8_bytes'],
        'maximum_attempts':frozen['maximum_paid_attempts'],
        'proposal_query_vector_values_and_original_provenance_unchanged':True,
        'api_calls':0, 'runtime_or_source_writes':0,
    }, indent=2))


if __name__ == '__main__':
    main()
