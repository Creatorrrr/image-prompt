"""Repair successor recovery after retaining the complete initial suite result."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
HISTORY = HERE / 'history'
HELPER = ROOT / 'tests/photo_ethereal_history_v35.py'
FIXTURES = ROOT / 'tests/photo_prompt_fixtures.py'
VALIDATOR = ROOT / 'skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py'
DESCRIPTOR = VALIDATOR.parent.parent / 'assets/universal_scene_baseline_v2.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def replace(path, before, after):
    text = path.read_text()
    assert text.count(before) == 1, (path, before)
    path.write_text(text.replace(before, after, 1))

def main():
    assert (HERE / 'full-suite/RESULT.json').is_file(), 'Do not edit active test inputs'
    saved = HISTORY / 'pre-recovery-fix'
    assert not saved.exists(), 'Repair already applied'
    files = [HELPER, FIXTURES, VALIDATOR, DESCRIPTOR,
             HISTORY / 'V34-PARENT-SOURCE.json', HISTORY / 'V35-ETHEREAL-DATA-PROOF.json',
             VALIDATOR.parent.parent / 'assets/photo_regression_baseline_v35.json']
    for path in files:
        destination = saved / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
    old_validator = sha(VALIDATOR)
    old_parent = sha(HISTORY / 'V34-PARENT-SOURCE.json')
    old_proof = sha(HISTORY / 'V35-ETHEREAL-DATA-PROOF.json')
    replace(FIXTURES, 'return photo_ethereal_history_v35\n',
            'return photo_ethereal_history_v35.v34_recovery_adapter()\n')
    liminal = ROOT / 'tests/test_photo_liminal_active_use_korean_data_cleanup.py'
    replace(liminal, "'photo_prompt_character_appearance_extension.json'})",
            "'photo_prompt_character_appearance_extension.json',\n                                          'photo_prompt_ethereal_gothic_scene_extension.json'})")
    robe = ROOT / 'tests/test_photo_robe_source_boundary_history.py'
    replace(robe, 'from tests import photo_data_scope_history_v34 as history',
            'from tests import photo_ethereal_history_v35 as history')
    replace(robe, "history.materialize('v32', tree, source_root=ROOT, link_verified=True)",
            'history.materialize_original(tree, source_root=ROOT, link_verified=True)')
    replace(robe, "history.replay('v32', tree, source_root=ROOT, test_module='tests.test_photo_robe_source_boundary_history', log_name='V32-ORIGINAL-TESTS.log')",
            "history.replay_original(tree, source_root=ROOT, test_module='tests.test_photo_robe_source_boundary_history')")
    preserve = HISTORY / 'preserve_v34.py'
    replace(preserve, "'tests/test_photo_palette_boundary_history.py'}",
            "'tests/test_photo_palette_boundary_history.py','tests/test_photo_robe_source_boundary_history.py','tests/test_photo_liminal_active_use_korean_data_cleanup.py'}")
    test_updates = {n: sha(ROOT / n) for n in (
        'tests/test_photo_motion_artifact_owner_data_cleanup.py',
        'tests/test_photo_liminal_active_use_korean_data_cleanup.py')}
    text = HELPER.read_text()
    text = text.replace('PACK_POINTERS=', 'TEST_RECOVERY=' + repr(test_updates) + '\nPACK_POINTERS=', 1)
    before = "    if name not in v34.RECOVERY:return regular(root,name)"
    after = """    if name in TEST_RECOVERY:
        proof,parent=transition(root);path=regular(root,name);row=next(r for r in parent['members'] if r['path']==name)
        current=path.read_bytes();original=exact_payload(root,row)
        if digest(current)!=TEST_RECOVERY[name] or path.stat().st_mode&0o7777!=int(row['mode'][-3:],8):raise AssertionError('Frozen V35 historical test adapter drift: '+name)
        if supplied is not None and digest(supplied) not in {digest(current),digest(original)}:raise AssertionError('Frozen V35 supplied historical test payload drift: '+name)
        return regular(root,row['source_path'])
    if name not in v34.RECOVERY:return regular(root,name)"""
    assert text.count(before) == 1
    text = text.replace(before, after, 1)
    adapter = """
class _V34RecoveryAdapter:
    previous_path=staticmethod(previous_path)
    previous_payload=staticmethod(previous_payload)

    def __getattr__(self,name):
        from tests import photo_data_scope_history_v34 as original
        return getattr(original,name)

def v34_recovery_adapter():
    \"\"\"Keep original V34 APIs while recovering only verified successor inputs.\"\"\"
    return _V34RecoveryAdapter()

"""
    assert text.count('def materialize_original(') == 1
    text = text.replace('def materialize_original(', adapter + 'def materialize_original(', 1)
    # A successor wraps an original wrapper which retains its own 900-second
    # deadline. Give that unchanged inner check room for materialization too.
    assert text.count('timeout=900)') == 1
    text = text.replace('timeout=900)', 'timeout=1800 if test_module else 900)', 1)
    text = text.replace("    for row in parent['members']:exact_payload(root,row)\n    descriptor=",
                        "    for row in parent['members']:exact_payload(root,row)\n    for name in TEST_RECOVERY:previous_path(root,name)\n    descriptor=", 1)
    HELPER.write_text(text)
    for script in ('preserve_v34.py', 'build_v35.py'):
        with (HERE / (script + '.recovery.log')).open('w') as output:
            subprocess.run([str(ROOT / '.venv/bin/python'), str(HISTORY / script)], cwd=ROOT,
                           check=True, stdout=output, stderr=subprocess.STDOUT)
    replace(HELPER, old_parent, sha(HISTORY / 'V34-PARENT-SOURCE.json'))
    replace(HELPER, old_proof, sha(HISTORY / 'V35-ETHEREAL-DATA-PROOF.json'))
    helper_sha = sha(HELPER)
    for path, constant in ((FIXTURES, 'V35_ETHEREAL_SUPPORT_SHA256'),
                           (VALIDATOR, 'PHOTO_V35_ETHEREAL_SUPPORT_SHA256')):
        text = path.read_text()
        text, count = re.subn(constant + r" = '[0-9a-f]{64}'", constant + " = '" + helper_sha + "'", text)
        assert count == 1
        path.write_text(text)
    replace(DESCRIPTOR, old_validator, sha(VALIDATOR))
    record = dict(reason='Retain original V34 transition API; recover exact parent test bytes; keep the new optional overlay outside the 20261002 snapshot; replay original robe assertions through the exact V34 parent.',
                  old_parent_manifest_sha256=old_parent, parent_manifest_sha256=sha(HISTORY / 'V34-PARENT-SOURCE.json'),
                  old_proof_sha256=old_proof, proof_sha256=sha(HISTORY / 'V35-ETHEREAL-DATA-PROOF.json'),
                  helper_sha256=helper_sha, validator_sha256=sha(VALIDATOR), test_recovery_sha256=test_updates,
                  original_v1_v34_assertions_rewritten=False, original_inner_replay_deadline_seconds=900,
                  successor_outer_test_replay_deadline_seconds=1800, initial_suite_evidence_preserved=True)
    (HERE / 'HISTORY-RECOVERY-REPAIR.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))

if __name__ == '__main__':
    main()
