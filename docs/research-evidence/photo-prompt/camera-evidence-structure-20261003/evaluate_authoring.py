"""Replay complete authored inputs through the actual public CLI, offline.

No core helper, prose padding, subject/anchor inference or fixture repair. Failure
inputs remain unchanged. Source/type passes are separate from author ownership.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from unittest import mock


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for arg in ('runtime-repo', 'data-repo', 'inputs', 'output'):
        p.add_argument('--' + arg, type=Path, required=True)
    p.add_argument('--request-axis-review', type=Path,
                   help='Separate semantic review of source requests; never infer required axes from author declarations.')
    args = p.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    scripts = args.runtime_repo / 'skills/photo-prompt-image-generator/scripts'
    sys.path.insert(0, str(scripts))
    import prompt_generator as pg
    import generate_photo_prompt as cli
    import validate_precore_feature_selection as feature
    new_mode = '--new-author-camera-evidence' in (scripts / 'generate_photo_prompt.py').read_text()
    report = {'runtime_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.runtime_repo, text=True).strip(),
              'runtime_sources': {x.name: sha(x) for x in scripts.glob('*.py')}, 'provider_calls': 0,
              'pixel_quality_evaluated': False, 'complete_author_inputs': True,
              'new_author_cli_mode_supported': new_mode, 'rows': []}
    axis_review = json.loads(args.request_axis_review.read_text()) if args.request_axis_review else None
    if axis_review:
        report['request_axis_review'] = axis_review
        report['request_axis_review_sha256'] = sha(args.request_axis_review)
    cache = []
    real_loader = pg.load_runtime_data
    def load_data(*unused, **kwargs):
        if not cache:
            cache.append(real_loader(args.data_repo / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json'))
        return cache[0]
    keys = ('request-envelope', 'authorial-core', 'creative-controls', 'embodiment-review')
    for folder in sorted(args.inputs.iterdir()):
        if not folder.is_dir() or not (folder / 'authorial-core.json').exists(): continue
        original = {x.name: x.read_bytes() for x in folder.iterdir() if x.is_file()}
        row = {'id': folder.name, 'input_hashes': {k: hashlib.sha256(v).hexdigest() for k, v in original.items()}}
        core_raw = json.loads(original['authorial-core.json'])
        argv = [arg for key in keys for arg in ('--' + key + '-json', str(folder / (key + '.json')))]
        outfile = args.output / (folder.name + '.pack.json')
        if new_mode: argv += ['--new-author-camera-evidence']
        if axis_review:
            row['request_axis_requirements'] = axis_review['cases'][folder.name]
            for axis, state in row['request_axis_requirements'].items():
                if state == 'requested': argv += ['--require-camera-evidence', axis]
        argv += ['--seed', '829', '--output-file', str(outfile)]
        try:
            env = pg.normalize_request_envelope(json.loads(original['request-envelope.json']))
            controls = json.loads(original['creative-controls.json'])
            core = pg.normalize_authorial_core(core_raw, request_envelope=env, creative_control_snapshot=controls)
            row['core_sha256'] = core['canonical_sha256']
            row['baseline_sha256'] = hashlib.sha256(core['baseline_prompt_en'].encode()).hexdigest()
            row['property_locks'] = pg.intent_property_locks(core['intent_lock'])
            catalog = args.runtime_repo / 'skills/photo-prompt-image-generator/precore/visual_feature_catalog.json'
            row['feature_selection'] = feature.validate_selection(json.loads(catalog.read_bytes()), catalog.read_bytes(),
                json.loads(original['precore_feature_selection.json']), json.loads(original['request-envelope.json']),
                core_raw, json.loads(original['embodiment-review.json']))
            with mock.patch.object(pg, 'load_runtime_data', side_effect=load_data), \
                 mock.patch.object(pg, 'cached_gemini_client', side_effect=AssertionError('offline authoring replay')), \
                 mock.patch.object(pg, 'embed_texts_with_gemini', side_effect=AssertionError('offline authoring replay')):
                cli.main(argv)
            pack = json.loads(outfile.read_text())[0]
            row.update(error=None, pack_sha256=sha(outfile), total_candidates=sum(len(s['candidates']) for s in pack['slots'].values()),
                       candidate_adoption=pack['core_retrieval']['candidate_adoption'],
                       candidate_order=pack['authorial_composition']['candidate_order'])
            row['axes'] = {}
            for axis in ('direction', 'height'):
                query, fields = pg.core_slot_focus_queries(cache[0], core, 'camera_' + axis)
                candidates = pack['slots'].get('camera_' + axis, {}).get('candidates', [])
                row['axes'][axis] = {'query': query, 'query_fields': fields,
                    'candidates': [{'entry_id': c['entry_id'], 'label': c.get('label'),
                                    'applicability': c.get('applicability')} for c in candidates]}
        except (ValueError, KeyError, FileNotFoundError, SystemExit) as exc:
            row['error'] = str(exc)
        row['all_input_bytes_unchanged'] = original == {x.name: x.read_bytes() for x in folder.iterdir() if x.is_file()}
        assert row['all_input_bytes_unchanged']
        report['rows'].append(row)
    if cache:
        data = cache[0]
        report.update(data_dictionary_hash=pg.dictionary_hash(data), quality_layers_loaded=pg.QUALITY_LAYERS_DATA_KEY in data,
                      semantic_entries=len(data[pg.SEMANTIC_INDEX_DATA_KEY]['entries']),
                      visual_profiles=len(data[pg.VISUAL_OBLIGATIONS_DATA_KEY]['profiles']))
    report['summary'] = {'inputs': len(report['rows']), 'admitted': sum(r.get('error') is None for r in report['rows']),
                         'unchanged_inputs': sum(r['all_input_bytes_unchanged'] for r in report['rows'])}
    (args.output / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['summary']), flush=True)


if __name__ == '__main__': main()
