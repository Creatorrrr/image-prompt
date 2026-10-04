"""Replay frozen independent cores; retain all original native artifacts."""
from pathlib import Path
import copy
import hashlib
import json
import sys

root = Path(sys.argv[1]).resolve()
evidence = Path(__file__).resolve().parent.parent
qual = evidence / 'qualification'
skill = root / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(skill / 'scripts'))
import prompt_generator as generator

def read(path):
    value = json.loads(path.read_text())
    return value[0] if isinstance(value, list) else value

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                   separators=(',', ':')).encode()).hexdigest()

def slots(pack):
    return {entry['id']: entry for slot in pack['slots'].values()
            for entry in slot['candidates']}

final_data = generator.load_runtime_data()
frozen_assets = qual / 'frozen-source-v1/skills/photo-prompt-image-generator/assets'
frozen_data = generator.load_json(frozen_assets / 'photo_prompt_tags.json')
output = qual / 'final-v2-retrieval-replay'
output.mkdir(exist_ok=True)
reports = []
for arm in ['arm-a', 'arm-b', 'arm-c']:
    arm_root = qual / arm
    old = read(arm_root / 'candidate_pack.json')
    core = copy.deepcopy(old['authorial_core'])
    controls = copy.deepcopy(old['creative_controls'])
    review = copy.deepcopy(old['embodiment_preflight']['baseline_review'])
    seed = old['provenance']['seed']
    current = generator.generate_candidate_pack(final_data, core, controls, review, seed=seed)
    selected = json.loads((arm_root / 'image_runs.ndjson').read_text().splitlines()[0])['chosen_candidate_ids']
    old_slots, current_slots = slots(old), slots(current)
    comparisons = []
    for candidate_id in selected:
        _, slot, entry_id = candidate_id.split(':', 2)
        before = next(row for row in frozen_data['slots'][slot] if row['id'] == entry_id)
        after = next(row for row in final_data['slots'][slot] if row['id'] == entry_id)
        comparisons.append({
            'candidate_id': candidate_id,
            'merged_entry_unchanged': before == after,
            'merged_entry_sha256_v1': digest(before),
            'merged_entry_sha256_v2': digest(after),
            'exposed_in_original_pack': candidate_id in old_slots,
            'exposed_in_final_replay': candidate_id in current_slots,
            'pack_candidate_surface_unchanged': old_slots.get(candidate_id) == current_slots.get(candidate_id),
        })
    record = {
        'arm': arm,
        'frozen_native_revision': 'qualification-v1',
        'replay_revision': 'final-v2',
        'original_pack_id': old['pack_id'],
        'replayed_pack_id': current['pack_id'],
        'seed': seed,
        'core_unchanged': old['authorial_core'] == current['authorial_core'],
        'baseline_prompt_unchanged': old['authorial_core']['baseline_prompt_en'] == current['authorial_core']['baseline_prompt_en'],
        'controls_unchanged': old['creative_controls'] == current['creative_controls'],
        'selected_candidate_checks': comparisons,
        'new_se_visual_profile_exposed_count': sum('se_profile_' in row.get('profile_id', row.get('id', '')) for row in current.get('visual_concept_candidates', {}).get('candidates', [])),
        'native_image_calls': 0,
        'boundary': 'Retrieval and source compatibility replay only. The three preserved images were generated with qualification-v1. No native result is attributed to final-v2.',
    }
    (output / (arm + '-candidate-pack.json')).write_text(json.dumps(current, ensure_ascii=False, indent=2) + '\n')
    reports.append(record)
    print(json.dumps(record, ensure_ascii=False), flush=True)
(output / 'REPLAY-SUMMARY.json').write_text(json.dumps(reports, ensure_ascii=False, indent=2) + '\n')
assert all(r['core_unchanged'] and r['baseline_prompt_unchanged'] and r['controls_unchanged']
           and all(c['merged_entry_unchanged'] and c['exposed_in_final_replay']
                   and c['pack_candidate_surface_unchanged'] for c in r['selected_candidate_checks'])
           for r in reports)
