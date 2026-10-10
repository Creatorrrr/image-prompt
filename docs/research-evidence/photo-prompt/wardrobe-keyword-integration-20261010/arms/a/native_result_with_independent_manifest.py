#!/usr/bin/env python3
"""Arm-local metadata adapter; keep the official native result path intact."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

REPO = Path('/Users/chasoik/Projects/image-prompt')
ARM = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / 'skills/photo-prompt-image-generator/scripts'))
import photo_workflow as workflow


def add_metadata(flags: list[str], metadata: list[tuple[str, str | None]]) -> None:
    """Append only missing recorder metadata; refuse a conflicting old value."""
    old = list(flags)
    for key, value in metadata:
        positions = [i for i, item in enumerate(flags) if item == key]
        if value is None:
            if len(positions) > 1:
                raise ValueError('duplicate independent recorder flag')
            if not positions:
                flags.append(key)
        elif positions:
            observed = [flags[i + 1] for i in positions]
            if value not in observed:
                raise ValueError('conflicting independent recorder metadata: ' + key)
        else:
            flags.extend([key, value])
    if flags[:len(old)] != old:
        raise ValueError('official recorder arguments changed')


def metadata_for_run(run: Path) -> list[tuple[str, str | None]]:
    state = workflow.load_state(run)
    provenance = json.loads((ARM / 'input_provenance.json').read_text())
    source = state['source_binding']
    plan = workflow.value(state, 'native_plan')
    original = workflow.load_state(ARM / 'run')
    calls = sum(len(op['attempts']) for s in (original, state) for op in s['operations'])
    if calls != 1:
        raise ValueError('this arm is authorized for exactly one actual invocation')
    if provenance['independent_no_cross_arm_inputs'] is not True:
        raise ValueError('missing independent authoring declaration')
    skill = REPO / provenance['skill_path']
    if hashlib.sha256(skill.read_bytes()).hexdigest() != provenance['frozen_skill_sha256']:
        raise ValueError('frozen skill changed')
    if [r['sha256'] for r in plan['references']] != [r['sha256'] for r in provenance['references']]:
        raise ValueError('native reference metadata changed')
    snapshot = 'generation:' + source['generation_id'] + ';source_fingerprint:' + source['source_fingerprint']
    return [
        ('--arm-id', 'a'),
        ('--worktree-id', provenance['worktree_id']),
        ('--skill-sha256', provenance['frozen_skill_sha256']),
        ('--source-ref', snapshot),
        ('--candidate-pack-version', 'v6'),
        *[('--reference-sha256', r['sha256']) for r in plan['references']],
        ('--image-call-count', str(calls)),
        ('--independent-no-cross-arm-inputs', None),
        ('--manifest', str(ARM / 'run_manifest.json')),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path)
    parser.add_argument('--ledger', type=Path)
    parser.add_argument('--result', type=Path)
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    if args.check_only:
        base = ['--tool', 'image_gen', '--generation-environment', 'native_imagegen', '--status', 'success']
        flags = list(base)
        example = [('--arm-id', 'a'), ('--candidate-pack-version', 'v6'), ('--image-call-count', '1'),
                   ('--independent-no-cross-arm-inputs', None), ('--manifest', str(ARM / 'run_manifest.json'))]
        identity = id(flags)
        add_metadata(flags, example)
        once = list(flags)
        add_metadata(flags, example)
        assert flags == once and id(flags) == identity and flags[:len(base)] == base
        print(json.dumps({'status':'pass', 'scope':'argument augmentation only; no invocation and no ledger append',
                          'original_arguments_preserved':True, 'idempotent':True, 'official_native_result':'unchanged',
                          'official_recorder':'record_image_run.py', 'tool':'image_gen', 'generation_environment':'native_imagegen'}))
        return 0
    if not all((args.run, args.ledger, args.result)):
        parser.error('--run, --ledger and --result are required')
    args.run = args.run.resolve()
    if args.run != (ARM / 'requalification_run').resolve():
        raise ValueError('adapter is restricted to this arm requalification run')
    metadata = metadata_for_run(args.run)
    official_update = workflow.update_operation

    def update_with_metadata(run, identifier, event):
        if event.get('ledger_args'):
            # The list is the same object the official native_result passes to
            # the official recorder. Persist it before that first append so a
            # recovery uses identical arguments, without an extra append.
            add_metadata(event['ledger_args'], metadata)
        return official_update(run, identifier, event)

    workflow.update_operation = update_with_metadata
    result = workflow.native_result(SimpleNamespace(run=args.run, ledger=args.ledger.resolve(), result=args.result.resolve()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
