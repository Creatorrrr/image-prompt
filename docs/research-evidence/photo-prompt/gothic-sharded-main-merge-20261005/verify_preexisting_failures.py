"""Replay unchanged failing assertions on the sealed origin V21 source."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PIN = '726c51b015294930f0ad98ca126cde11e6caead2'
sys.path[:0] = [str(ROOT / 'tests'), str(ROOT)]
import photo_prompt_fixtures as fixtures


def main():
    with tempfile.TemporaryDirectory(prefix='origin-v21-failure-replay-') as saved:
        target = Path(saved)
        fixtures.materialize_v21_parent_source(target, source_root=ROOT)
        names = [
            'tests/test_photo_character_appearance_100.py',
            'tests/test_photo_clothing_terminology_semantics.py',
            'tests/test_subculture_illustration_photo_boundary.py',
            'tests/test_photo_liminal_active_use_korean_data_cleanup.py',
            'tests/photo_prompt_fixtures.py', 'tests/__init__.py',
            'tests/fixtures/photo_prompt/seduction_expression_scope_delta.json',
            'docs/research-evidence/photo-prompt/uniform-costume-integration-20261004/authored-candidate-delta.json',
            'docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/INTEGRATION-LEDGER.json',
            'docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/main-merge/UPSTREAM-EFFECT-ADDITIONS.json',
            'docs/research-evidence/photo-prompt/character-appearance-100-20261004/BASELINE-REGISTRY.json',
            'docs/research-evidence/photo-prompt/character-appearance-100-20261004/INTEGRATION-MAINTENANCE.json',
            'docs/research-evidence/photo-prompt/character-appearance-100-20261004/CHARACTER-CASEBOOK.json',
            'docs/research-evidence/photo-prompt/clothing-terminology-20261001/runtime-integration.json',
        ]
        names.extend(str(p.relative_to(ROOT)) for p in
                     (ROOT / 'skills/subculture-illustration-image-generator/scripts').glob('*.py'))
        names.extend(subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', PIN, '--',
            'docs/research-evidence/photo-prompt/liminal-active-use-korean-data-cleanup-20261002',
            'docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/baseline'],
            cwd=ROOT, text=True).splitlines())
        for module in ('clothing_structure', 'textile_surface', 'accessory_structure', 'traditional_clothing_detail'):
            ext = json.loads((target / f'skills/photo-prompt-image-generator/assets/photo_prompt_{module}_extension.json').read_bytes())
            names.append('docs/research-evidence/photo-prompt/extension-maintenance/' + ext['maintenance_ref']['record_id'] + '.json')
        bindings = {}
        for name in names:
            raw = subprocess.check_output(['git', 'show', f'{PIN}:{name}'], cwd=ROOT)
            if name not in (fixtures.V17_PARENT_VALIDATOR, 'tests/photo_prompt_fixtures.py'):
                assert raw == (ROOT / name).read_bytes(), name
            out = target / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(raw)
            bindings[name] = hashlib.sha256(raw).hexdigest()
        code = '''
import json,re,sys,unittest
from pathlib import Path
re._MAXCACHE=200000
sys.path[:0]=['tests','.']
ids=['test_photo_character_appearance_100.CharacterAppearance100Tests.test_all_previous_profiles_keep_meaning_activation_effects_and_native_gates',
     'test_photo_clothing_terminology_semantics.ClothingTerminologySemanticsTests.test_authored_sources_and_generated_indexes_bind_every_registered_variant',
     'test_subculture_illustration_photo_boundary.SubcultureIllustrationPhotoBoundaryTests.test_illustration_modules_do_not_import_photo_runtime',
     'test_photo_liminal_active_use_korean_data_cleanup.LiminalActiveUseKoreanDataCleanupTests.test_complete_merged_state_and_twenty_one_keeps_remain_exact']
result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(ids))
Path(sys.argv[1]).write_text(json.dumps({'source_pin':sys.argv[2],'tests_run':result.testsRun,
    'failures':[{'test':str(test),'traceback':tb} for test,tb in result.failures],
    'errors':[{'test':str(test),'traceback':tb} for test,tb in result.errors],
    'was_successful':result.wasSuccessful()},indent=2)+'\\n')
'''
        with (HERE / 'origin-preexisting-failure-replay.log').open('w') as log:
            completed = subprocess.run([sys.executable, '-c', code, str(HERE / 'ORIGIN-PREEXISTING-FAILURES.json'), PIN],
                cwd=target, stdout=log, stderr=subprocess.STDOUT, timeout=180)
        assert completed.returncode == 0
        result = json.loads((HERE / 'ORIGIN-PREEXISTING-FAILURES.json').read_bytes())
        result['unchanged_test_and_fixture_bindings'] = bindings
        (HERE / 'ORIGIN-PREEXISTING-FAILURES.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps({'source_pin': PIN, 'tests_run': result['tests_run'],
            'failures': len(result['failures']), 'errors': len(result['errors'])}))


if __name__ == '__main__':
    main()
