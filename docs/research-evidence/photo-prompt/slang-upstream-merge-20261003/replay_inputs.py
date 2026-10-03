"""Requery all frozen arms and the existing sibling boundary after merging."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INITIAL = HERE.parent / 'slang-integration-20261003'
GENERATOR = ROOT / 'skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py'
BOUNDARY = ROOT / 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v8.json'


def read(path):
    return json.loads(path.read_text())


def run(command, name):
    env = os.environ.copy()
    env['GEMINI_API_KEY'] = ''; env['GOOGLE_API_KEY'] = ''
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
    (HERE / f'{name}.log').write_text(result.stdout + result.stderr)
    assert result.returncode == 0, f'{name}: {result.stderr}'
    return read(HERE / f'{name}.json')[0]


def arm(number):
    folder = INITIAL / f'tests/agent-{number}'
    previous = read(folder / 'candidate_pack.json')[0]
    name = f'arm-{number}-pack'
    command = [sys.executable, str(GENERATOR)]
    inputs = {}
    for flag, filename in (
        ('request-envelope-json', 'request_envelope.json'),
        ('authorial-core-json', 'authorial_core.json'),
        ('creative-controls-json', 'creative_controls.json'),
        ('embodiment-review-json', 'embodiment_review.json'),
    ):
        command += ['--' + flag, str(folder / filename)]
        inputs[filename] = hashlib.sha256((folder / filename).read_bytes()).hexdigest()
    command += ['--seed', str(previous['provenance']['seed']), '--output-file', str(HERE / f'{name}.json')]
    current = run(command, name)
    for field in ('authorial_core', 'creative_controls', 'embodiment_preflight', 'negative_en'):
        assert current[field] == previous[field], (number, field)
    ordinary = {row['id'] for slot in current['slots'].values() for row in slot['candidates']}
    optional = {row['id'] for row in current.get('visual_concept_candidates', {}).get('candidates', [])}
    bundles = {row['id'] for row in current.get('candidate_bundles', {}).get('candidates', [])}
    expected = {
        1: ['visual-concept:composite_overwhelmed_expression', 'bundle:pv_bundle_double_v'],
        2: ['slot:body_pose:sv_supported_m_legs', 'visual-concept:soft_full_figure_volume', 'visual-concept:rb_support_compression'],
        3: ['slot:eye_detail:sv_pupil_heart_motif', 'slot:body_marking:sv_lower_abdominal_skin_marking', 'slot:body_marking:sv_declared_skin_motif_topology'],
    }[number]
    exposure = {value: value in ordinary | optional | bundles for value in expected}
    assert all(exposure.values()), (number, exposure)
    return {'arm': number, 'original_pack_id': previous['pack_id'], 'merged_pack_id': current['pack_id'],
            'same_four_inputs_sha256': inputs, 'same_seed': True,
            'core_controls_embodiment_negative_unchanged': True,
            'target_meanings_exposed': exposure,
            'adoption_claim': 'Exposure only. Original native adoption, prompt and pixel verdicts remain archived.',
            'native_image_calls': 0}


def boundary():
    previous = read(BOUNDARY)
    command = list(previous['command'])
    name = 'boundary-pack'
    command[command.index('--output-file') + 1] = str(HERE / f'{name}.json')
    pack = run(command, name)
    raw = (HERE / f'{name}.json').read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    contract = {k: pack.get(k) for k in ('authorial_core', 'creative_controls', 'embodiment_review', 'authorial_composition', 'negative_en')}
    digest = hashlib.sha256(json.dumps(contract, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    assert digest == previous['preserved_contract_sha256']
    assert all(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected for path, expected in previous['frozen_inputs'].items())
    assert pack['negative_en'] == previous['negative_en']
    assert sum(len(slot['candidates']) for slot in pack['slots'].values()) == previous['public_candidate_count']
    return {'record': str(BOUNDARY.relative_to(ROOT)), 'record_sha256': hashlib.sha256(BOUNDARY.read_bytes()).hexdigest(),
            'previous_pack_sha256': previous['sha256'], 'merged_pack_sha256': sha,
            'candidate_pack_bytes_unchanged': sha == previous['sha256'],
            'frozen_scene_contract_and_inputs_preserved': True, 'pack_id': pack['pack_id']}


if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = [pool.submit(arm, number) for number in (1, 2, 3)]
        boundary_job = pool.submit(boundary)
        arms = [job.result() for job in jobs]
        result = {'schema_version': 'photo-slang-merged-retrieval/v1', 'arms': arms,
                  'boundary': boundary_job.result(), 'native_calls': 0}
    (HERE / 'RETRIEVAL.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'arms': len(arms), 'all_targets_exposed': True, 'boundary': result['boundary'], 'native_calls': 0}))
