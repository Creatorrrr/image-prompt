"""Reject rewrites of frozen request, main lineage and recovery payloads."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from tests import photo_ethereal_history_v35 as history
from tests import photo_data_scope_history_v34 as previous

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/history.ILL/'scripts'))
import validate_illustration_assets as validator


class EtherealV35BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proof,cls.parent=history.transition(ROOT)
        cls.assets=ROOT/history.ILL/'assets'
        cls.baseline=json.loads((cls.assets/'photo_regression_baseline_v35.json').read_text())
        cls.raw=(cls.assets/'photo_regression_baseline_v35_pack.json').read_bytes()
        cls.pack=json.loads(cls.raw)[0]

    def test_previous_scene_inputs_hard_contract_and_all_other_candidates_are_preserved(self):
        old=json.loads((self.assets/'photo_regression_baseline_v34_pack.json').read_text())
        reconstructed=copy.deepcopy(old)
        previous._apply(reconstructed,self.proof['reviewed_pack_delta'],validator._require)
        self.assertEqual(reconstructed,[self.pack])
        for field in ['authorial_core','creative_controls','embodiment_review','authorial_composition','negative_en','visual_obligations']:
            self.assertEqual(old[0].get(field),self.pack.get(field))
        self.assertEqual(64,validator._public_photo_candidate_count(self.pack))

    def test_rehashed_pack_with_changed_negative_or_core_cannot_qualify(self):
        for key,value in [('negative_en','changed negative'),('authorial_core',{})]:
            pack=copy.deepcopy(self.pack);pack[key]=value
            raw=(json.dumps([pack],ensure_ascii=False,indent=2)+'\n').encode()
            baseline={**self.baseline,'sha256':history.digest(raw)}
            with self.subTest(key=key),self.assertRaisesRegex(validator.ValidationFailure,'frozen pack'):
                history.qualify_current(validator,self.assets,ROOT,baseline,pack,raw)

    def test_rehashed_baseline_cannot_rebind_parent_lineage(self):
        baseline=copy.deepcopy(self.baseline)
        baseline['ethereal_data_transition']['previous_qualified_commit']='0'*40
        with self.assertRaisesRegex(validator.ValidationFailure,'lineage'):
            history.qualify_current(validator,self.assets,ROOT,baseline,self.pack,self.raw)

    def recovery_tree(self,root):
        name=(history.PHOTO/'photo_prompt_source_manifest.json').as_posix()
        parent=next(r for r in self.parent['members'] if r['path']==name)
        original=next(r for r in previous.source_manifest('v32',ROOT)['members'] if r['path']==name)
        paths={history.PARENT.as_posix(),history.PROOF.as_posix(),name,parent['source_path'],original['source_path'],(previous.BASE/'SOURCE-V32.json').as_posix()}
        for path in paths:
            target=root/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/path,target)
        return name,original

    def test_live_drift_cannot_use_valid_original_recovery(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary).resolve();name,original=self.recovery_tree(root)
            recovered=history.previous_path(root,name)
            self.assertEqual(history.digest(recovered.read_bytes()),original['sha256'])
            path=root/name;path.write_bytes(path.read_bytes()+b' ')
            with self.assertRaisesRegex(AssertionError,'retained live source'):
                history.previous_path(root,name)

    def test_original_bytes_and_mode_cannot_be_replaced_by_live_successor(self):
        for mode in ['bytes','mode','symlink']:
            with self.subTest(mode=mode),tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary).resolve();name,row=self.recovery_tree(root);p=root/row['source_path']
                if mode=='bytes':p.write_bytes(p.read_bytes()+b' ')
                elif mode=='mode':p.chmod(0o600)
                else:p.unlink();p.symlink_to(root/name)
                with self.assertRaisesRegex(AssertionError,'payload or mode drift|symlink'):
                    history.previous_path(root,name)

    def test_v34_transition_api_remains_the_original_scope_proof(self):
        from tests import photo_prompt_fixtures as fixtures
        support=fixtures._v34_scope_support(ROOT)
        proof,parent=support.transition(ROOT)
        self.assertEqual(proof['schema'],'photo-data-scope-transition/v34')
        self.assertIn('source_leaf_delta',proof)
        self.assertEqual((proof,parent),previous.transition(ROOT))
        self.assertEqual(support.PROOF_SHA256,previous.PROOF_SHA256)

    def test_historical_test_recovery_requires_the_declared_live_adapter(self):
        name='tests/test_photo_motion_artifact_owner_data_cleanup.py'
        row=next(r for r in self.parent['members'] if r['path']==name)
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary).resolve()
            for path in [history.PARENT.as_posix(),history.PROOF.as_posix(),name,row['source_path']]:
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/path,target)
            original=history.previous_path(root,name)
            self.assertEqual(history.digest(original.read_bytes()),row['sha256'])
            live=root/name;live.write_bytes(live.read_bytes()+b'\n# rewritten assertions\n')
            with self.assertRaisesRegex(AssertionError,'historical test adapter drift'):
                history.previous_path(root,name)


if __name__=='__main__':unittest.main()
