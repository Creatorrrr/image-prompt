"""Narrow diagnostic replay with the new cute candidate/profile overlay disabled.

This is not a complete historical checkout. It checks unchanged source/fixture
failures independently of the added overlay without altering workspace files.
"""
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / 'skills/photo-prompt-image-generator/scripts')]
import prompt_generator as pg

NAMES = [
    'tests.test_photo_nape_effect_scope.PhotoNapeEffectScopeTests.test_both_source_surfaces_declare_nape_and_preserve_original_effect',
    'tests.test_photo_nape_effect_scope.PhotoNapeEffectScopeTests.test_nape_parent_and_declared_leaf_are_protected',
    'tests.test_photo_textile_opacity_effect_scope.PhotoTextileOpacityEffectScopeTests.test_matching_sources_append_opacity_preserving_family_owner_and_carrier',
    'tests.test_photo_textile_opacity_effect_scope.PhotoTextileOpacityEffectScopeTests.test_canonical_opacity_and_ancestor_locks_reject',
    'tests.test_photo_character_appearance_100.CharacterAppearance100Tests.test_all_previous_profiles_keep_meaning_activation_effects_and_native_gates',
    'tests.test_photo_liminal_active_use_korean_data_cleanup.LiminalActiveUseKoreanDataCleanupTests.test_complete_merged_state_and_twenty_one_keeps_remain_exact',
    'tests.test_photo_nape_metadata_boundary_history.NapeMetadataBoundaryHistoryTests.test_registered_version_replay_and_all_legacy_artifacts_are_unchanged',
]

candidate_files = tuple(n for n in pg.RESEARCH_EXTENSION_FILENAMES
                        if n != 'photo_prompt_cute_visual_forms_extension.json')
profile_files = tuple(n for n in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES
                      if n != 'photo_prompt_visual_obligations_cute_visual_forms.json')
with mock.patch.object(pg, 'RESEARCH_EXTENSION_FILENAMES', candidate_files), \
     mock.patch.object(pg, 'VISUAL_OBLIGATION_EXTENSION_FILENAMES', profile_files):
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromNames(NAMES))

baseline = json.loads((HERE / 'BASELINE.json').read_text())
sources = {}
for name in ('photo_prompt_subculture_appearance_extension.json',
             'photo_prompt_visual_obligations_subculture_appearance.json',
             'photo_prompt_textile_surface_extension.json',
             'photo_prompt_visual_obligations_textile_surface.json',
             'photo_prompt_visual_obligations_palace_fortification.json'):
    path = ROOT / 'skills/photo-prompt-image-generator/assets' / name
    if not path.exists():
        continue
    relative = str(path.relative_to(ROOT))
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    sources[relative] = {'initial_sha256': baseline['authored_files'].get(relative),
                         'current_sha256': actual,
                         'unchanged_from_initial': baseline['authored_files'].get(relative) == actual}

lineage = []
assets = ROOT / 'skills/subculture-illustration-image-generator/assets'
for version in range(8, 17):
    path = assets / f'photo_regression_baseline_v{version}.json'
    data = json.loads(path.read_text())
    bound = data.get('historical_baseline', {})
    predecessor = assets / bound.get('path', '')
    if predecessor.is_file():
        actual = hashlib.sha256(predecessor.read_bytes()).hexdigest()
        if actual != bound.get('sha256'):
            lineage.append({'version': version, 'predecessor': bound['path'],
                            'expected_sha256': bound.get('sha256'), 'actual_sha256': actual})

record = {
    'diagnostic': 'new cute candidate/profile overlays disabled in memory only',
    'not_a_complete_historical_checkout': True,
    'test_names': NAMES,
    'tests_run': result.testsRun,
    'failures': [{'test': t.id(), 'traceback': trace} for t, trace in result.failures],
    'errors': [{'test': t.id(), 'traceback': trace} for t, trace in result.errors],
    'unchanged_relevant_authored_sources': sources,
    'preexisting_modified_lineage_files': [
        n for n in baseline['status'].splitlines()
        if 'skills/subculture-illustration-image-generator/assets/photo_regression_baseline_' in n],
    'current_lineage_hash_mismatches': lineage,
    'limitation': 'The two enriched pose/expression files and regenerated indexes remain current; '
                  'the observed failures concern separate unchanged sources or existing lineage fixtures.',
}
(HERE / 'EXISTING-FAILURE-REPLAY.json').write_text(
    json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print('Diagnostic replay completed:', result.testsRun, 'tests,', len(result.failures),
      'subtest failures,', len(result.errors), 'errors; no source files changed.')
