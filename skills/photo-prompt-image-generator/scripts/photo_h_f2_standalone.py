#!/usr/bin/env python3
"""Worker launched with the verified installed H-F2 code and interpreter."""
import argparse
import json
from pathlib import Path
import sys

import prompt_generator as generator
from photo_camera_evidence import CAMERA_AXES, camera_authoring_declaration, require_camera_evidence
import photo_slot_expression as expression
import photo_h_f2_queries as queries
from photo_h_f2_generation import Generation
from photo_h_f2_workflow import search_material
from photo_h_f2_receipts import issue
from photo_runtime_sources import RuntimeSnapshotProvider
from photo_validation_context import build
from photo_recall_generation import read, write


def main():
    p = argparse.ArgumentParser(allow_abbrev=False)
    for name in ('request-envelope-json', 'authorial-core-json', 'creative-controls-json',
                 'embodiment-review-json', 'slot-expression-plan-json', 'output-directory',
                 'installed-store', 'installed-generation', 'installed-skill'):
        p.add_argument('--' + name, required=True)
    p.add_argument('--query-cache', type=Path)
    p.add_argument('--require-camera-evidence', action='append', choices=CAMERA_AXES, default=[])
    p.add_argument('--new-author-camera-evidence', action='store_true')
    a = p.parse_args()
    envelope = generator.load_request_envelope_arg(a.request_envelope_json)
    controls = read(a.creative_controls_json)
    core = generator.load_authorial_core_arg(a.authorial_core_json, request_envelope=envelope,
                                             creative_control_snapshot=controls)
    require_camera_evidence(core, a.require_camera_evidence)
    lock = core['intent_lock']
    declared = 'camera' in set(lock['locked_dimensions']) | set(lock['open_dimensions'])
    camera_authoring_declaration(core, required=a.new_author_camera_evidence and declared)
    embodiment = read(a.embodiment_review_json)
    generator.photo_embodiment.build_policy(core, embodiment)
    plan = read(a.slot_expression_plan_json)
    # Validate the authored plan against the installed neutral catalog before
    # opening the candidate pool, exactly as the managed path does.
    from photo_workflow import neutral_slot_catalog
    catalog = neutral_slot_catalog()
    queryset = queries.prepare(core, controls, catalog, plan)
    output = Path(a.output_directory).resolve()
    if output.exists():
        raise ValueError('output directory already exists; choose a new directory')
    generation = Generation(a.installed_store, a.installed_generation)
    provider = RuntimeSnapshotProvider(store=Path(a.installed_store))
    snapshot = provider.load_generation(generation.manifest['native_generation_id'])
    if expression.specification(snapshot.data['slot_catalog']) != catalog:
        raise ValueError('H-F2 and native catalog differ')
    context = build(snapshot.data, core, controls, embodiment)
    validation_receipt = provider.receipt(snapshot, context)
    material = search_material(generation, queryset,
        a.query_cache or Path(a.installed_store) / 'h-f2-query-cache', output / 'raw',
        skill=Path(a.installed_skill), creativity=generator.creative_controls.runtime_values(controls)['creativity'])
    receipt = issue(generation, material, output / 'raw', context, validation_receipt)
    result = {'schema': 'photo-h-f2-standalone-result/v1', 'generation_id': generation.id,
              'native_generation_id': generation.manifest['native_generation_id'],
              'validation_context': context, 'validation_receipt': validation_receipt,
              'material': material, 'material_receipt': receipt,
              'raw_directory': str(output / 'raw'), 'native_approval': False}
    write(output / 'result.json', result)
    print(json.dumps({'status': 'pass', 'result': str(output / 'result.json'),
        'generation_id': generation.id, 'searched_queries': len(queryset['slots']),
        'searched_slots': sum(v == 'slot' for v in queryset['query_scopes'].values()),
        'native_approval': False}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, OSError, TypeError, json.JSONDecodeError) as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        raise SystemExit(1)
