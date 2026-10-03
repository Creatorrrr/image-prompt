#!/usr/bin/env python3
"""Check upstream authored meaning and local additions independently of Git diff size."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def additive(before, after, allowed, path=()):
    if before == after:
        return
    if isinstance(before, dict):
        assert isinstance(after, dict) and set(before) <= set(after), path
        for key, value in before.items():
            additive(value, after[key], allowed, (*path, key))
        for key in set(after) - set(before):
            assert key in allowed and isinstance(after[key], list) and after[key], (
                *path, key, 'unexpected new meaning field'
            )
    elif isinstance(before, list):
        assert isinstance(after, list), path
        if path and path[-1] in allowed:
            assert all(value in after for value in before), (*path, 'removed alternative')
        else:
            assert len(before) == len(after), path
            for i, (left, right) in enumerate(zip(before, after)):
                additive(left, right, allowed, (*path, str(i)))
    else:
        raise AssertionError((path, before, after))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--upstream', required=True)
    args = parser.parse_args()
    base = git('rev-parse', args.upstream).decode().strip()
    source = SKILL / 'scripts/prompt_generator.py'
    before_source = git('show', f'{base}:{source.relative_to(ROOT)}').decode()
    after_source = source.read_text()
    for name in ('photo_prompt_subculture_appearance_extension.json',
                 'photo_prompt_visual_obligations_subculture_appearance.json'):
        after_source = after_source.replace(f'    "{name}",\n', '')
    assert before_source == after_source, 'generator change exceeds generic registrations'
    tracked = git('ls-tree', '-r', '--name-only', base, '--', str(ASSETS.relative_to(ROOT))).decode().splitlines()
    with tempfile.TemporaryDirectory(prefix='appearance-upstream-authored-') as directory:
        prior_assets = Path(directory)
        for name in tracked:
            path = Path(name)
            if path.parent == ASSETS.relative_to(ROOT) and path.suffix == '.json' and path.name not in {
                'photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json',
            }:
                (prior_assets / path.name).write_bytes(git('show', f'{base}:{name}'))
        with patch.object(pg, 'RESEARCH_EXTENSION_FILENAMES', tuple(
            n for n in pg.RESEARCH_EXTENSION_FILENAMES if n != 'photo_prompt_subculture_appearance_extension.json'
        )), patch.object(pg, 'VISUAL_OBLIGATION_EXTENSION_FILENAMES', tuple(
            n for n in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES if n != 'photo_prompt_visual_obligations_subculture_appearance.json'
        )):
            old_data = pg.load_json(prior_assets / 'photo_prompt_tags.json')
            old_registry = pg.load_visual_obligation_registry(prior_assets / 'photo_prompt_visual_obligations.json')
    current = pg.load_runtime_data()
    registry = current[pg.VISUAL_OBLIGATIONS_DATA_KEY]
    old_profiles = {p['id']: p for p in old_registry['profiles']}
    new_profiles = {p['id']: p for p in registry['profiles']}
    assert set(old_profiles) <= set(new_profiles)
    altered_profiles = []
    allowed = {'paraphrase_examples', 'concept_terms', 'any_terms',
               'must_mention_any', 'match_terms', 'evidence_terms'}
    for profile_id, before in old_profiles.items():
        after = new_profiles[profile_id]
        additive(before, after, allowed, (profile_id,))
        if before != after:
            altered_profiles.append(profile_id)
    old_rows = {(slot, e['id']): e for slot, rows in old_data['slots'].items() for e in rows}
    new_rows = {(slot, e['id']): e for slot, rows in current['slots'].items() for e in rows}
    assert set(old_rows) <= set(new_rows)
    altered_rows = []
    for key, before in old_rows.items():
        after = new_rows[key]
        additive(before, after, {'paraphrases'}, key)
        if before != after:
            altered_rows.append(list(key))
    assert len(new_profiles) - len(old_profiles) == 46
    assert len(altered_profiles) == 36
    assert len(new_rows) - len(old_rows) == 45
    assert len(altered_rows) == 35
    illustration = ROOT / 'skills/subculture-illustration-image-generator/assets'
    for version in range(1, 9):
        path = illustration / f'photo_regression_baseline_v{version}.json'
        assert path.read_bytes() == git('show', f'{base}:{path.relative_to(ROOT)}')
    binding_path = illustration / 'universal_scene_baseline_v2.json'
    before_binding = json.loads(git('show', f'{base}:{binding_path.relative_to(ROOT)}'))
    after_binding = json.loads(binding_path.read_text())
    digest = hashlib.sha256((illustration.parent / 'scripts/validate_illustration_assets.py').read_bytes()).hexdigest()
    assert after_binding['validator_contract']['sha256'] == digest
    after_binding['validator_contract']['sha256'] = before_binding['validator_contract']['sha256']
    assert before_binding == after_binding
    record = {
        'status': 'PASS', 'upstream_commit': base,
        'upstream_profiles_preserved': len(old_profiles), 'new_profiles': 46,
        'existing_profiles_only_positive_alternatives_added': altered_profiles,
        'upstream_candidate_rows_preserved': len(old_rows), 'new_candidates': 45,
        'existing_candidates_only_paraphrases_added': altered_rows,
        'profile_definition_activation_owner_locks_gates_and_minima_preserved': True,
        'photo_baselines_v1_to_v8_byte_immutable': True,
        'universal_oracle_changes_only_validator_byte_binding': True,
        'current_visual_profiles': len(new_profiles),
        'current_semantic_index_entries': current[pg.SEMANTIC_INDEX_DATA_KEY]['entry_count'],
        'runtime_loader_and_both_indexes': 'PASS',
    }
    (HERE / 'UPSTREAM-PRESERVATION.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in record.items() if not isinstance(v, list)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
