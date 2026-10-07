"""Replay failed unchanged assertions against exact remote main DATA and code."""
from __future__ import annotations
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from tests import photo_ethereal_history_v35 as history

TARGETS = [
    'tests.test_photo_shelf_return_korean_state_data_cleanup.ShelfReturnKoreanStateDataCleanupTests.test_historical_merged_state_and_current_eleven_keeps_are_exact',
    'tests.test_photo_krummholz_korean_alias_data_cleanup.KrummholzKoreanAliasDataCleanupTests.test_historical_merged_state_and_current_ten_keeps_are_exact',
    'tests.test_photo_protostar_korean_alias_data_cleanup.ProtostarKoreanAliasDataCleanupTests.test_historical_merged_state_and_current_nineteen_keeps_are_exact',
    'tests.test_photo_liminal_active_use_korean_data_cleanup.LiminalActiveUseKoreanDataCleanupTests.test_complete_merged_state_and_twenty_one_keeps_remain_exact',
    'tests.test_photo_render_repair',
]
PREFIXES = [
    'docs/research-evidence/photo-prompt/shelf-return-korean-state-data-cleanup-20261001/',
    'docs/research-evidence/photo-prompt/krummholz-korean-alias-data-cleanup-20261001/',
    'docs/research-evidence/photo-prompt/protostar-korean-alias-data-cleanup-20261001/',
    'docs/research-evidence/photo-prompt/liminal-active-use-korean-data-cleanup-20261002/',
    'docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004/',
    'tests/fixtures/photo_prompt/',
]

def main():
    root = ROOT / '.codex-artifacts/ethereal-upstream-failure-baseline'
    if root.exists():
        for row in history.parent_manifest(ROOT)['members']:
            path = root / row['path']
            assert path.is_file() and not path.is_symlink()
            assert history.digest(path.read_bytes()) == row['sha256']
            assert path.stat().st_mode & 0o7777 == int(row['mode'][-3:], 8)
    else:
        history.materialize_original(root, source_root=ROOT, link_verified=True)
    names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', history.PIN], cwd=ROOT, text=True).splitlines()
    required = {t.rsplit('.', 2)[0].replace('.', '/') + '.py' for t in TARGETS[:-1]}
    required.update({'tests/test_photo_render_repair.py', 'tests/photo_prompt_fixtures.py', 'tests/__init__.py'})
    selected = required | {n for n in names if any(n.startswith(p) for p in PREFIXES)}
    for name in sorted(selected):
        raw = subprocess.check_output(['git', 'show', history.PIN + ':' + name], cwd=ROOT)
        path = root / name
        if path.exists():
            assert path.read_bytes() == raw, ('Original main replay payload differs', name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
    env = os.environ.copy()
    env.update(PYTHONPATH=str(root) + os.pathsep + str(root / 'tests'), GEMINI_API_KEY='', GOOGLE_API_KEY='')
    with tempfile.TemporaryDirectory(prefix='ethereal-upstream-baseline-runtime-') as store:
        env['PHOTO_RUNTIME_STORE'] = store
        setup = "import sys; sys.path.insert(0,'skills/photo-prompt-image-generator/scripts'); from photo_runtime_sources import SnapshotPublisher; SnapshotPublisher().publish()"
        subprocess.run([sys.executable, '-c', setup], cwd=root, env=env, check=True, stdout=subprocess.DEVNULL)
        with (HERE / 'UPSTREAM-OTHER-FAILURES-final.log').open('w') as log:
            result = subprocess.run([sys.executable, '-m', 'unittest', '-v', *TARGETS], cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
    metadata = dict(source_pin=history.PIN, source_tree=history.TREE, exact_original_runtime_and_data=True, unchanged_test_assertions=True, materialized_parent_members=1522, additional_committed_files=len(selected), targets=TARGETS, exit_code=result.returncode, log='UPSTREAM-OTHER-FAILURES-final.log')
    (HERE / 'UPSTREAM-OTHER-FAILURES-final.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata))

if __name__ == '__main__':
    main()
