"""Fail-closed receipt, closure and dispatch boundaries for explicit replay."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import native_replay as replay


def put(path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value))
    return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def fixture(root):
    store = root/'store'
    run = root/'run'
    code = b'# preserved implementation\n'
    asset = b'original asset'
    source = {'code':{'scripts/photo_workflow.py':hashlib.sha256(code).hexdigest()}}
    manifest = {'schema':'photo-runtime-generation/v3','source':source,
        'source_fingerprint':replay.digest(source),'algorithm_sha256':'algorithm',
        'search_layout':{'layout_sha256':'layout','corpus_sha256':'corpus'},
        'members':{name:{'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)} for name,raw in
                   [('scripts/photo_workflow.py',code),('assets/data.json',asset)]}}
    gid = replay.digest(manifest)
    generation = store/'generations'/gid
    put(generation/'manifest.json',manifest)
    (generation/'scripts').mkdir()
    (generation/'scripts/photo_workflow.py').write_bytes(code)
    (generation/'assets').mkdir()
    (generation/'assets/data.json').write_bytes(asset)
    pack = {'global_retrieval':{'corpus_sha256':'corpus','canonical_sha256':'retrieval'},
            'authorial_core':{'canonical_sha256':'core'},'provenance':{'tags_hash':'tags'}}
    receipt = {'schema':'photo-runtime-receipt/v3','generation_id':gid,'request_id':'a'*32,
        'pack_sha256':replay.digest(pack),'source_fingerprint':manifest['source_fingerprint'],
        'algorithm_sha256':'algorithm','search_layout_sha256':'layout','bindings':replay.pack_bindings(pack)}
    receipt['canonical_sha256'] = replay.digest(receipt)
    put(store/'receipts'/('a'*32+'.json'),receipt)
    workflow = {'artifacts':{'pack':put(run/'pack.json',pack),
                             'runtime_receipt':put(run/'receipt.json',receipt)},
        'source_binding':{'runtime_store':str(store),'generation_id':gid,
                          'source_fingerprint':manifest['source_fingerprint']}}
    put(run/'workflow.json',workflow)
    return run,store,generation


class ReplayBoundary(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='test-explicit-replay-')
        self.addCleanup(self.temp.cleanup)
        self.run,self.store,self.generation = fixture(Path(self.temp.name))

    def test_valid_receipt_and_full_closure_are_read_only(self):
        before = {str(p):p.read_bytes() for p in Path(self.temp.name).rglob('*') if p.is_file()}
        result = replay.inspect_run(self.run,full=True)
        self.assertEqual(result['status'],'PASS')
        self.assertEqual(result['code_files'],1)
        self.assertTrue(result['full_member_hashes_verified'])
        self.assertEqual(before,{str(p):p.read_bytes() for p in Path(self.temp.name).rglob('*') if p.is_file()})

    def test_artifact_bytes_changed(self):
        (self.run/'pack.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'artifact_changed'):
            replay.inspect_run(self.run)

    def test_valid_artifact_checksum_does_not_bypass_receipt_pack_binding(self):
        workflow = replay.read(self.run/'workflow.json')
        workflow['artifacts']['pack'] = put(self.run/'pack.json',{'changed':True})
        put(self.run/'workflow.json',workflow)
        with self.assertRaisesRegex(ValueError,'receipt_pack_mismatch'):
            replay.inspect_run(self.run)

    def test_missing_original_issued_receipt(self):
        next((self.store/'receipts').iterdir()).unlink()
        with self.assertRaisesRegex(ValueError,'missing_or_symlink_file'):
            replay.inspect_run(self.run)

    def test_forged_issued_copy(self):
        put(next((self.store/'receipts').iterdir()),{'forged':True})
        with self.assertRaisesRegex(ValueError,'original_issued_receipt'):
            replay.inspect_run(self.run)

    def test_run_generation_override(self):
        workflow = replay.read(self.run/'workflow.json')
        workflow['source_binding']['generation_id'] = 'b'*64
        put(self.run/'workflow.json',workflow)
        with self.assertRaisesRegex(ValueError,'run_binding_mismatch'):
            replay.inspect_run(self.run)

    def test_manifest_tampering(self):
        manifest = replay.read(self.generation/'manifest.json')
        manifest['algorithm_sha256'] = 'changed'
        put(self.generation/'manifest.json',manifest)
        with self.assertRaisesRegex(ValueError,'generation_checksum'):
            replay.inspect_run(self.run)

    def test_declared_code_tampering(self):
        (self.generation/'scripts/photo_workflow.py').write_text('raise SystemExit(99)')
        with self.assertRaisesRegex(ValueError,'code_checksum'):
            replay.inspect_run(self.run)

    def test_undeclared_code(self):
        (self.generation/'scripts/unlisted.py').write_text('raise SystemExit(99)')
        with self.assertRaisesRegex(ValueError,'executable_closure'):
            replay.inspect_run(self.run)

    def test_full_check_detects_changed_assets(self):
        (self.generation/'assets/data.json').write_bytes(b'modified asset')
        self.assertFalse(replay.inspect_run(self.run)['full_member_hashes_verified'])
        with self.assertRaisesRegex(ValueError,'member_checksum'):
            replay.inspect_run(self.run,full=True)

    def test_member_symlink_even_with_equal_bytes(self):
        path = self.generation/'assets/data.json'
        raw = path.read_bytes()
        alternate = Path(self.temp.name)/'other'
        alternate.write_bytes(raw)
        path.unlink()
        path.symlink_to(alternate)
        with self.assertRaisesRegex(ValueError,'symlink_member'):
            replay.inspect_run(self.run)

    def test_parent_generation_symlink(self):
        directory = self.store/'generations'
        directory.rename(self.store/'other-generations')
        directory.symlink_to(self.store/'other-generations',target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink_generation_directory'):
            replay.inspect_run(self.run)

    def test_member_traversal_and_absolute_path_rejected(self):
        for name in ('../escape','/tmp/escape','assets/../escape','assets\\escape'):
            with self.subTest(name=name),self.assertRaisesRegex(ValueError,'unsafe_member'):
                replay.member(self.generation,name)

    def test_failed_frozen_worker_never_falls_back(self):
        process = subprocess.CompletedProcess([],2,'','missing original dependency')
        with patch.object(replay.subprocess,'run',return_value=process) as child:
            result = replay.audit(self.run)
        self.assertEqual(result['status'],'DEFER')
        self.assertEqual(child.call_count,1)
        self.assertEqual(result['reason'],'original_frozen_audit_unavailable')

    def test_worker_gets_only_verified_generation_no_live_module_path(self):
        process = subprocess.CompletedProcess([],0,json.dumps({'status':'PASS',
            'generation_id':self.generation.name}),'')
        with patch.dict(os.environ,{'GEMINI_API_KEY':'test','PYTHONPATH':'/untrusted'}),patch.object(
                replay.subprocess,'run',return_value=process) as child:
            result = replay.audit(self.run)
        command = child.call_args.args[0]
        self.assertEqual(command[-3:],[str(self.generation.resolve()),str(self.run.resolve()),self.generation.name])
        self.assertIn('-I',command)
        self.assertNotIn('GEMINI_API_KEY',child.call_args.kwargs['env'])
        self.assertNotIn('PYTHONPATH',child.call_args.kwargs['env'])
        self.assertIn('(deny network*)',command[2])
        self.assertTrue(result['live_source_fallback_denied'])


if __name__ == '__main__':
    unittest.main()
