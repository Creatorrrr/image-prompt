import copy
import os
import tempfile
import unittest
from pathlib import Path
from tests.test_photo_global_retrieval import GlobalDiscoveryTests
import photo_candidate_corpus as c
import photo_search_layout as layout
from photo_search_reader import SearchReader,LazyRuntimeData
import photo_shared_views as views


class SearchReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name)
        self.data=GlobalDiscoveryTests().data();layout.build(self.root,views.source(self.data),self.data['_global_index'],leaf_size=1,activate=True)
        self.reader=SearchReader(self.root,cache_limit=4000)

    def test_initialization_reads_no_payload_posting_or_vector(self):
        data=LazyRuntimeData(self.reader)
        self.assertEqual(self.reader.metrics['vector_reads'],0);self.assertEqual(self.reader.metrics['payload_reads'],0)
        self.assertEqual(len(data['candidates']),3)
        self.assertNotIn('_global_index',data)

    def test_payload_is_original_immutable_and_eviction_is_bounded(self):
        cid=next(iter(self.data['candidates']));value=self.reader.record(cid)
        self.assertEqual(value,self.data['candidates'][cid]);self.assertRaises(ValueError,value.__setitem__,'content',{})
        for i in range(3):self.reader.block('vector',i)
        vector=self.reader.block('vector',0)
        self.assertTrue(vector.readonly);self.assertRaises(TypeError,vector.__setitem__,0,0.5)
        self.assertLessEqual(self.reader.cache_bytes,4000)
        self.assertEqual(self.reader.record(cid),value)

    def test_same_mtime_tamper_and_missing_unread_shard_fail(self):
        p=self.root/self.reader.meta['vector_shards'][0]['path'];st=p.stat();raw=p.read_bytes()
        p.write_bytes(raw[:-1]+bytes([raw[-1]^1]));os.utime(p,ns=(st.st_atime_ns,st.st_mtime_ns))
        self.assertRaises(ValueError,self.reader.check_presence)
        self.assertRaises(ValueError,self.reader.block,'vector',0)
        (self.root/self.reader.meta['vector_shards'][1]['path']).unlink()
        self.assertRaises(ValueError,self.reader.check_presence)

    def test_layout_metadata_corruption_is_not_ignored(self):
        p=self.root/self.reader.manifest['metadata']['path'];p.write_bytes(b'broken')
        self.assertRaises(ValueError,SearchReader,self.root)

    def test_leaf_reads_one_extent_and_reuses_bounded_pinned_descriptors(self):
        first=self.reader.meta['vector_shards'][0];second=self.reader.meta['vector_shards'][1]
        self.assertEqual(first['path'],second['path'])
        full_size=(self.root/first['path']).stat().st_size;before=self.reader.metrics['vector_bytes']
        self.reader.block('vector',0)
        self.assertEqual(self.reader.metrics['vector_bytes']-before,first['bytes'])
        self.assertLess(first['bytes'],full_size);self.assertEqual(len(self.reader.descriptors),1)
        self.reader.block('vector',1);self.assertEqual(len(self.reader.descriptors),1)
        self.reader.close();self.assertEqual(len(self.reader.descriptors),0)
