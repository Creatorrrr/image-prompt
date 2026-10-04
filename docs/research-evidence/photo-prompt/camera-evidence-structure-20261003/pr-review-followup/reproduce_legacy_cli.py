"""Offline review reproduction using unchanged complete synthetic input copies."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
from unittest import mock


def main():
    p = argparse.ArgumentParser()
    for name in ('runtime', 'data', 'inputs', 'output'): p.add_argument('--' + name, type=Path, required=True)
    args = p.parse_args(); args.output.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(args.runtime / 'skills/photo-prompt-image-generator/scripts'))
    import generate_photo_prompt as cli
    import prompt_generator as pg
    import photo_camera_evidence as camera
    data = pg.load_runtime_data(args.data / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
    record = {'evidence_kind': 'Review reproduction/development; not blind evaluation',
              'runtime_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.runtime, text=True).strip(),
              'dictionary_hash': pg.dictionary_hash(data), 'quality_layers_loaded': pg.QUALITY_LAYERS_DATA_KEY in data,
              'semantic_entries': len(data[pg.SEMANTIC_INDEX_DATA_KEY]['entries']),
              'visual_profiles': len(data[pg.VISUAL_OBLIGATIONS_DATA_KEY]['profiles']),
              'provider_calls': 0, 'rendering_quality_evaluated': False, 'rows': []}
    for folder in sorted(args.inputs.iterdir()):
        if not folder.is_dir(): continue
        original = {x.name: x.read_bytes() for x in folder.glob('*.json')}
        raw = json.loads(original['authorial-core.json'])
        core = pg.normalize_authorial_core(raw,
            request_envelope=pg.normalize_request_envelope(json.loads(original['request-envelope.json'])),
            creative_control_snapshot=json.loads(original['creative-controls.json']))
        output = args.output / (folder.name + '.pack.json')
        argv = [arg for key in ('request-envelope', 'authorial-core', 'creative-controls', 'embodiment-review')
                for arg in ('--' + key + '-json', str(folder / (key + '.json')))]
        with mock.patch.object(pg, 'load_runtime_data', return_value=data), \
             mock.patch.object(pg, 'cached_gemini_client', side_effect=AssertionError('offline review reproduction')), \
             mock.patch.object(pg, 'embed_texts_with_gemini', side_effect=AssertionError('offline review reproduction')):
            cli.main(argv + ['--seed', '829', '--output-file', str(output)])
        pack = json.loads(output.read_bytes())[0]
        query, fields = pg.core_slot_focus_queries(data, core, 'camera_direction')
        unchanged = original == {x.name: x.read_bytes() for x in folder.glob('*.json')}
        assert unchanged
        record['rows'].append({'id': folder.name, 'core_sha256': core['canonical_sha256'],
            'baseline_sha256': hashlib.sha256(raw['baseline_prompt_en'].encode()).hexdigest(),
            'input_hashes': {k: hashlib.sha256(v).hexdigest() for k, v in original.items()},
            'inputs_unchanged': unchanged, 'legacy_owned_clauses': camera.legacy_camera_clauses(core, 'direction'),
            'query': query, 'query_fields': fields, 'pack_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'total_candidates': sum(len(s['candidates']) for s in pack['slots'].values()),
            'candidate_adoption': pack['core_retrieval']['candidate_adoption'],
            'public_order': pack['authorial_composition']['candidate_order']})
    (args.output / 'report.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'cases': len(record['rows']), 'owned_clause_queries': sum(
        'baseline_prompt_en.camera_clause' in r['query_fields'] for r in record['rows'])}), flush=True)


if __name__ == '__main__': main()
