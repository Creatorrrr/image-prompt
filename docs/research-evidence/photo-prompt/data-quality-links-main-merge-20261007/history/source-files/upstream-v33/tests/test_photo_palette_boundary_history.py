"""Real V33 boundary, offline V32 replay, and source/mode/downgrade guards."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tests import photo_palette_history as history
from tests import photo_prompt_fixtures as fixtures

ROOT=Path(__file__).resolve().parents[1]
I=Path('skills/subculture-illustration-image-generator')
sys.path.insert(0,str(ROOT/I/'scripts'))
import validate_illustration_assets as validator

class PaletteBoundaryHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof,cls.parent=history.transition(ROOT)
        cls.baseline=json.loads((ROOT/I/'assets/photo_regression_baseline_v33.json').read_bytes())
        cls.raw=(ROOT/I/'assets/photo_regression_baseline_v33_pack.json').read_bytes()
        cls.pack=json.loads(cls.raw)[0]

    def setUp(self):
        temporary=tempfile.TemporaryDirectory(prefix='.palette-v33-boundary-',dir=ROOT)
        self.addCleanup(temporary.cleanup);self.repo=Path(temporary.name)/'tree';self.repo.mkdir()
        paths=set(self.proof['source_files_after'])|set(self.proof['active_shards_after'])|set(self.proof['retained_shards_before'])|set(self.proof['evidence_files'])
        paths.update(row['source_path'] for row in self.parent['members'])
        paths.update((history.PROOF.as_posix(),history.PARENT.as_posix(),self.proof['maintenance_successor']['path'],
                      'tests/photo_palette_history.py',(I/'assets/universal_scene_baseline_v2.json').as_posix()))
        paths.update(p.relative_to(ROOT).as_posix() for p in (ROOT/I/'assets').glob('photo_regression_baseline_v*.json'))
        for name in sorted(paths):
            destination=self.repo/name;destination.parent.mkdir(parents=True,exist_ok=True);os.link(ROOT/name,destination)

    @contextlib.contextmanager
    def changed(self,name,raw,mode=None):
        path=self.repo/name;original_mode=path.stat().st_mode&0o7777
        path.unlink()
        if raw is not None:path.write_bytes(raw);path.chmod(original_mode if mode is None else mode)
        try:yield path
        finally:
            path.unlink(missing_ok=True);os.link(ROOT/name,path)

    def qualify(self,receipt=None):
        history.qualify_current(validator,self.repo/I/'assets',self.repo,self.baseline,self.pack,self.raw,receipt)

    def test_default_real_cli_and_receipt_qualify_v33(self):
        result=validator.validate_photo_regression_baseline(ROOT/I/'assets')
        self.assertEqual('photo_regression_baseline/v33',result['schema'])
        self.assertEqual(self.proof['current_pack_sha256'],result['sha256'])

    def test_explicit_wrong_python_cannot_rebind_historical_receipt(self):
        wrong={'implementation':'cpython','python':[3,14,3],'unicode':'16.0.0'}
        with mock.patch.dict(os.environ,{'PHOTO_V32_PYTHON':'/explicit/wrong/python'}):
            with mock.patch.object(history.subprocess,'run',return_value=subprocess.CompletedProcess(
                    ['/explicit/wrong/python'],0,stdout=json.dumps(wrong),stderr='')) as run:
                with self.assertRaisesRegex(AssertionError,'Exact V32 Python/Unicode binding unavailable'):
                    history.resolve_v32_python(ROOT)
                run.assert_called_once()
                self.assertEqual('/explicit/wrong/python',run.call_args.args[0][0])

    def test_reviewed_optional_changes_preserve_frozen_meaning_and_existing_candidates(self):
        previous=json.loads((ROOT/I/'assets/photo_regression_baseline_v32_pack.json').read_bytes())[0]
        for field in ('authorial_core','creative_controls','intent_contract','intent_preservation','mandatory_intents','negative_en','embodiment_preflight','authorial_composition'):
            self.assertEqual(previous[field],self.pack[field],field)
        self.assertEqual(64,validator._public_photo_candidate_count(previous))
        self.assertEqual(64,validator._public_photo_candidate_count(self.pack))
        for slot,rows in previous['slots'].items():
            before={r['id']:r for r in rows['candidates']};after={r['id']:r for r in self.pack['slots'][slot]['candidates']}
            for name in before.keys()&after.keys():self.assertEqual(before[name],after[name])
        self.qualify()

    def test_parent_materialization_has_exact_bytes_and_modes_without_external_access(self):
        destination=self.repo.parent/'original-v32'
        with contextlib.ExitStack() as stack:
            calls=[stack.enter_context(mock.patch(name,side_effect=RuntimeError('external access'))) for name in (
                'subprocess.Popen','os.system','os.popen','socket.create_connection','socket.socket.connect','urllib.request.urlopen')]
            parent=history.materialize_v32_parent_source(destination,source_root=ROOT,link_verified=True)
            for row in parent['members']:
                p=destination/row['path'];self.assertEqual(row['sha256'],hashlib.sha256(p.read_bytes()).hexdigest())
                self.assertEqual(int(row['mode'][-3:],8),p.stat().st_mode&0o7777)
            for call in calls:call.assert_not_called()

    def test_unrelated_robe_source_drift_is_rejected(self):
        name='skills/photo-prompt-image-generator/assets/photo_prompt_religion_iconography_extension.json'
        with self.changed(name,(self.repo/name).read_bytes()+b' '):
            with self.assertRaisesRegex(validator.ValidationFailure,'unrelated authored DATA'):self.qualify()

    def test_missing_proof_cannot_downgrade_to_old_source(self):
        name=next(iter(history.EVOLVING));current=(self.repo/name).read_bytes()
        with self.changed(history.PROOF.as_posix(),None):
            self.assertTrue(history.context(self.repo))
            with self.assertRaises((OSError,AssertionError)):history.previous_payload(self.repo,name,current)

    def test_preserved_source_corruption_and_mode_drift_are_rejected(self):
        name='skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json'
        row=next(r for r in self.parent['members'] if r['path']==name)
        with self.changed(row['source_path'],(self.repo/row['source_path']).read_bytes()+b' '):
            with self.assertRaises(AssertionError):history.previous_payload(self.repo,name,(self.repo/name).read_bytes())
        with self.changed(name,(self.repo/name).read_bytes(),mode=0o600):
            with self.assertRaisesRegex(AssertionError,'mode drift'):history.previous_payload(self.repo,name,(self.repo/name).read_bytes())

    def test_symbolic_live_source_cannot_borrow_a_valid_payload(self):
        name='skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json'
        original=(self.repo/name).read_bytes();outside=self.repo.parent/'outside.json';outside.write_bytes(original)
        with self.changed(name,None) as path:
            path.symlink_to(outside)
            with self.assertRaises(AssertionError):history.previous_payload(self.repo,name,original)

    def test_receipt_generation_and_optional_pack_changes_cannot_be_rebound(self):
        receipt=json.loads((ROOT/history.PROOF.parent/'CURRENT-BOUNDARY-RECEIPT.json').read_bytes())
        for field in ('generation_id','source_fingerprint','algorithm_sha256'):
            wrong=copy.deepcopy(receipt);wrong[field]='0'*64
            with self.subTest(field=field),self.assertRaisesRegex(validator.ValidationFailure,'receipt source generation drift'):self.qualify(wrong)
        changed=copy.deepcopy(self.pack);changed['authorial_core']['baseline_prompt_en']+=' added reinterpretation'
        raw=json.dumps([changed],ensure_ascii=False,indent=2).encode()
        with self.assertRaisesRegex(validator.ValidationFailure,'frozen pack bytes drift'):
            history.qualify_current(validator,self.repo/I/'assets',self.repo,self.baseline,changed,raw)

if __name__=='__main__':unittest.main()
