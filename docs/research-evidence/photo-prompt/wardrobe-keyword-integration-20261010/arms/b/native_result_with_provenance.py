#!/usr/bin/env python3
"""Use the official native-result transition and enrich its first recorder call."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
PROJECT_ROOT = Path('/Users/chasoik/Projects/image-prompt')
SCRIPTS = PROJECT_ROOT / 'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0, str(SCRIPTS))

import photo_workflow as workflow
import generate_images_via_api as api_adapter


def argument_values(flags: list[str], name: str) -> list[str]:
    return [flags[i + 1] for i, value in enumerate(flags[:-1]) if value == name]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--ledger', type=Path, required=True)
    parser.add_argument('--result', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    arm_dir = Path(__file__).resolve().parent
    for path in (args.run, args.ledger, args.result, args.manifest):
        if not path.resolve().is_relative_to(arm_dir):
            raise ValueError('arm_local_paths_required')
    state = workflow.load_state(args.run)
    workflow.ensure(state)
    receipt = workflow.value(state, 'runtime_receipt')
    frozen = workflow.value(state, 'freeze_receipt')
    provenance = json.loads((arm_dir / 'input_provenance.json').read_text())
    skill_sha = next(row['sha256'] for row in provenance['inputs']
                     if row['path'] == 'skills/photo-prompt-image-generator/SKILL.md')
    current_skill_sha = hashlib.sha256((PROJECT_ROOT / 'skills/photo-prompt-image-generator/SKILL.md').read_bytes()).hexdigest()
    if current_skill_sha != skill_sha:
        raise ValueError('frozen_skill_changed')
    reference_hashes = [row['sha256'] for row in workflow.value(state, 'native_plan')['references']]
    source_ref = 'generation:' + receipt['generation_id'] + ';source_fingerprint:' + receipt['source_fingerprint']
    official_record = api_adapter.record
    recorder_calls = 0

    def record_with_provenance(flags: list[str]):
        nonlocal recorder_calls
        recorder_calls += 1
        if recorder_calls != 1:
            raise ValueError('one_recorder_call_required')
        expected = {
            '--tool': 'image_gen',
            '--generation-environment': 'native_imagegen',
            '--image-call-count': '1',
            '--composer': 'agent',
            '--audit-status': 'pass',
            '--authorial-core-sha256': frozen['contracts']['core'],
            '--intent-lock-sha256': frozen['contracts']['intent_lock'],
            '--ledger': str(args.ledger),
        }
        for name, value in expected.items():
            if argument_values(flags, name) != [value]:
                raise ValueError('original_recorder_binding_mismatch:' + name)
        if argument_values(flags, '--reference-sha256') != reference_hashes:
            raise ValueError('original_reference_binding_mismatch')
        additions = [
            '--arm-id', 'b',
            '--worktree-id', str(PROJECT_ROOT),
            '--skill-sha256', skill_sha,
            '--source-ref', source_ref,
            '--candidate-pack-version', 'v6',
            '--independent-no-cross-arm-inputs',
            '--manifest', str(args.manifest),
        ]
        if any(name in flags for name in ('--arm-id', '--worktree-id', '--skill-sha256', '--source-ref', '--candidate-pack-version', '--manifest', '--independent-no-cross-arm-inputs')):
            raise ValueError('unexpected_preexisting_independent_provenance')
        enriched = list(flags) + additions
        (arm_dir / 'exact_recorder_arguments.json').write_text(json.dumps({
            'schema_version': 'arm-local-official-recorder-call/v1',
            'workflow_transition': 'photo_workflow.native_result',
            'recorder': 'generate_images_via_api.record -> record_image_run.py',
            'original_flags': flags,
            'added_independent_flags': additions,
            'exact_flags': enriched,
            'actual_image_call_count': 1,
        }, ensure_ascii=False, indent=2) + '\n')
        return official_record(enriched)

    api_adapter.record = record_with_provenance
    result = workflow.native_result(args)
    if result.get('status') == 'attempt_recorded' and recorder_calls != 1:
        raise ValueError('missing_official_recorder_call')
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError, KeyError, TypeError, RuntimeError) as error:
        print(json.dumps({'status': 'error', 'code': getattr(error, 'code', 'arm_local_native_record_failed'), 'detail': str(error)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
