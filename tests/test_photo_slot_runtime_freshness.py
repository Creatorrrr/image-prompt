import copy
import os
from pathlib import Path
from tests import test_photo_slot_workflow as fixture
import photo_runtime_sources as runtime


class SlotRuntimeFreshnessTests(fixture.NativeSlotWorkflowTests):
    def test_acquire_does_not_read_unneeded_vector_or_payload_bodies(self):
        fresh=runtime.RuntimeSnapshotProvider(self.root,self.store);snapshot=fresh.acquire()
        self.assertEqual(snapshot.data.reader.metrics['vector_reads'],0)
        self.assertEqual(snapshot.data.reader.metrics['payload_reads'],0)
        self.assertEqual(snapshot.data.reader.metrics['posting_reads'],0)

    def test_same_mtime_source_change_is_blocked_and_old_snapshot_stays_immutable(self):
        p=self.root/'assets/photo_candidate_candidates.json';st=p.stat();raw=p.read_bytes()
        p.write_bytes(raw.replace(b'camera left',b'camera rite'));os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns))
        self.assertRaises(runtime.FreshnessError,self.provider.acquire)
        self.assertRaises(runtime.FreshnessError,self.provider.publisher.publish)
        cid=next(iter(self.snapshot.data['candidates']))
        self.assertRaises(runtime.FreshnessError,self.snapshot.data['candidates'][cid].__setitem__,'content',{})

    def test_missing_unread_shard_and_cached_vector_tampering_are_blocked(self):
        row=self.snapshot.data.reader.meta['vector_shards'][0]
        self.snapshot.data.reader.block('vector',0)
        p=self.snapshot.root/'assets'/row['path'];st=p.stat();raw=p.read_bytes()
        p.chmod(0o644);p.write_bytes(raw[:-1]+bytes([raw[-1]^1]));os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns))
        self.assertRaises((ValueError,runtime.FreshnessError),self.provider.load_generation,self.snapshot.generation_id)
        live=self.root/'assets'/self.snapshot.data.reader.meta['vector_shards'][0]['path'];live.unlink()
        self.assertRaises(runtime.FreshnessError,self.provider.acquire)

    def test_pending_epoch_and_source_race_preserve_current(self):
        before=(self.provider.publisher.directory/'CURRENT.json').read_bytes()
        with runtime.source_update(self.root,self.store):self.assertRaises(runtime.FreshnessError,self.provider.acquire)
        self.assertEqual(before,(self.provider.publisher.directory/'CURRENT.json').read_bytes())
        def edit():
            p=self.root/'assets/photo_candidate_candidates.json';p.write_bytes(p.read_bytes()+b'\n')
        self.assertRaises(runtime.FreshnessError,self.provider.publisher.publish,before_publish=edit)
        self.assertEqual(before,(self.provider.publisher.directory/'CURRENT.json').read_bytes())
