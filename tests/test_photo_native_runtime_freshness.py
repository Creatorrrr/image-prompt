"""Native-only snapshots fail closed and keep in-flight source immutable.

Synthetic vectors exercise integrity only; real provider proof is in the stage reports.
"""
import copy,json,os,shutil,tempfile,unittest
from pathlib import Path
from tests import test_photo_global_retrieval as fixtures
import photo_candidate_corpus as c
import photo_global_index as idx
import photo_runtime_sources as runtime
import photo_shared_views as views
from photo_global_index_storage import canonical_bytes

class NativeRuntimeFreshnessTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'source';self.store=Path(self.temp.name)/'runtime'
        for name in ['scripts','precore']:
            shutil.copytree(runtime.SKILL_ROOT/name,self.root/name,ignore=shutil.ignore_patterns('__pycache__'))
        self.assets=self.root/'assets';self.assets.mkdir()
        self.data=fixtures.GlobalDiscoveryTests().data();self.source=views.source(self.data)
        self.source['policies']['_quality_layers']={'adult_appeal':{'contextual_retrieval':{'contract_version':'photo-contextual-appeal/v2'}}}
        self.data['_global_index']['corpus_sha256']=c.digest(self.source)
        modules=[]
        for field,schema in c.MODULE_SCHEMAS.items():
            name='photo_candidate_'+field+'.json';modules.append({'file':name,'kind':field})
            (self.assets/name).write_bytes(c.canonical_bytes({'schema':schema,field:self.source[field]}))
        (self.assets/c.MANIFEST_NAME).write_bytes(c.canonical_bytes({'schema':c.MANIFEST_SCHEMA,'modules':modules}))
        idx.write(self.assets,self.data['_global_index'])
        self.provider=runtime.RuntimeSnapshotProvider(self.root,self.store)
        self.snapshot=self.provider.acquire()
    def test_snapshot_is_immutable_and_copy_is_independent(self):
        cid=next(iter(self.snapshot.data['candidates']))
        with self.assertRaises(runtime.FreshnessError):self.snapshot.data['candidates'][cid]['content']['en']='another owner'
        clone=copy.deepcopy(self.snapshot.data);clone['candidates'][cid]['content']['en']='another owner'
        self.assertNotEqual(clone['candidates'][cid],self.snapshot.data['candidates'][cid])
    def test_content_edit_with_same_mtime_never_assigns_old_generation(self):
        p=self.assets/'photo_candidate_candidates.json';st=p.stat();raw=p.read_bytes();assert b'camera left' in raw
        p.write_bytes(raw.replace(b'camera left',b'camera rite'));os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns))
        old=(self.provider.publisher.directory/'CURRENT.json').read_bytes()
        with self.assertRaises(runtime.FreshnessError):self.provider.acquire()
        self.assertEqual((self.provider.publisher.directory/'CURRENT.json').read_bytes(),old)
        with self.assertRaises(runtime.FreshnessError):self.provider.publisher.publish()
    def test_missing_required_shard_cannot_fall_back_to_old_snapshot(self):
        manifest=json.loads((self.assets/idx.MANIFEST).read_text());(self.assets/manifest['shards'][0]['path']).unlink()
        with self.assertRaises(runtime.FreshnessError):runtime.RuntimeSnapshotProvider(self.root,self.store).acquire()
    def test_corrupt_optional_lexical_cache_rebuilds_same_source(self):
        payload=self.snapshot.manifest['global_cache']['payload'];(self.store/payload['path']).write_bytes(b'broken')
        fresh=runtime.RuntimeSnapshotProvider(self.root,self.store).acquire()
        self.assertEqual(fresh.generation_id,self.snapshot.generation_id);self.assertEqual(fresh.cache_status,'fallback')
        self.assertEqual(fresh.data.lexical_index(),self.snapshot.data.lexical_index())
    def test_unfinished_edit_epoch_blocks_existing_current(self):
        with runtime.source_update(self.root,self.store):
            with self.assertRaises(runtime.FreshnessError):self.provider.acquire()
        self.assertEqual(self.provider.acquire().generation_id,self.snapshot.generation_id)
    def test_imported_implementation_cannot_relabel_edited_code(self):
        p=self.root/'scripts/prompt_generator.py';p.write_bytes(p.read_bytes()+b'\n# changed implementation\n')
        with self.assertRaises(runtime.FreshnessError):self.provider.acquire()
        with self.assertRaises(runtime.FreshnessError):self.provider.publisher.publish()
    def test_forged_pointer_and_old_receipt_are_rejected(self):
        p=self.provider.publisher.directory/'CURRENT.json';v=json.loads(p.read_text());v['generation_id']='a'*64;p.write_bytes(c.canonical_bytes(v))
        with self.assertRaises(runtime.FreshnessError):runtime.RuntimeSnapshotProvider(self.root,self.store).acquire()
        with self.assertRaises(runtime.FreshnessError):self.provider.from_receipt({'pack_id':'test'}, {'schema':'photo-runtime-receipt/v1'})
if __name__=='__main__':unittest.main()
