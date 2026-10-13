import copy
import hashlib
import math
import random
import tempfile
import unittest
from pathlib import Path
from tests.test_photo_global_retrieval import GlobalDiscoveryTests
from tests.photo_slot_oracle import full_scan
import photo_candidate_corpus as c
import photo_global_index as idx
import photo_search_layout as layout
import photo_sharded_search as search
import photo_shared_views as views
from photo_search_reader import SearchReader


class ShardedSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.source=views.source(GlobalDiscoveryTests().data());self.source['candidates']={};self.source['slot_bindings']={}
        entries={};rng=random.Random(302)
        for n in range(48):
            cid='cand_'+f'{n:032x}';record={'id':cid,'record_kind':'visual_option','content':{'en':('left lighting blue' if n%2 else 'right red light'),'ko':'빛 조명'},'conditions':{},'effects':{'dimensions':['lighting'],'properties':[]},'provenance':[{'source':'test','sha256':'a'*64}]}
            self.source['candidates'][cid]=record;recipe,text=idx.text(record)
            v=[1. if n<24 else -1.,rng.uniform(-.03,.03),rng.uniform(-.03,.03)]+[0.]*765
            entries[cid]={'id':cid,'recipe':recipe,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':v}
        self.index={'schema':idx.SCHEMA,'space':idx.SPACE,'query_recipe':idx.QUERY_RECIPE,'corpus_sha256':c.digest(self.source),'entries':entries}
        layout.build(Path(self.temp.name),self.source,self.index,leaf_size=4,activate=True)
        self.reader=SearchReader(self.temp.name);self.lexical=idx.lexical(self.source)

    def test_both_lanes_equal_full_scan_and_skip_irrelevant_vector_shards(self):
        allowed=set(self.source['candidates']);fields={'global_context':'blue light','slot_focus':'빛 left lighting'};vector=[1.]+[0.]*767
        expected=full_scan(self.lexical,self.index['entries'],fields,vector,allowed,limit=12)
        self.assertEqual(search.lexical_rank(self.reader,fields,allowed,12),expected['bm25f'])
        hits,proof=search.cosine_rank(self.reader,vector,allowed,12)
        self.assertEqual(hits,expected['embedding']);self.assertTrue(search.audit_cosine(self.reader,vector,allowed,hits,proof))
        self.assertLess(len(proof['visited_leaves']),len(self.reader.meta['vector_shards']))

    def test_allowed_subset_empty_and_opposite_query_preserve_exact_rank(self):
        for allowed in [set(),set(list(self.source['candidates'])[::3])]:
            vector=[-1.]+[0.]*767;fields={'slot_focus':'right light'}
            expected=full_scan(self.lexical,self.index['entries'],fields,vector,allowed,limit=48)
            hits,proof=search.cosine_rank(self.reader,vector,allowed,48)
            self.assertEqual(hits,expected['embedding']);search.audit_cosine(self.reader,vector,allowed,hits,proof)
            self.assertEqual(search.lexical_rank(self.reader,fields,allowed,48),expected['bm25f'])

    def test_forged_skip_and_score_are_rejected(self):
        allowed=set(self.source['candidates']);vector=[1.]+[0.]*767
        hits,proof=search.cosine_rank(self.reader,vector,allowed,12)
        changed=copy.deepcopy(proof);changed['visited_leaves']=[];changed['skipped_nodes']=[{'node':0,'reason':'score_bound'}]
        self.assertRaises(ValueError,search.audit_cosine,self.reader,vector,allowed,[],changed)
        changed=copy.deepcopy(hits);changed[0]['score']=.5
        self.assertRaises(ValueError,search.audit_cosine,self.reader,vector,allowed,changed,proof)

    def test_worst_case_streams_every_extent_with_bounded_cache(self):
        reader=SearchReader(self.temp.name,cache_limit=30000);self.addCleanup(reader.close)
        allowed=set(self.source['candidates']);vector=[1.]+[0.]*767
        expected=full_scan(self.lexical,self.index['entries'],{'slot_focus':'light'},vector,allowed,limit=48,minimum=-1.)
        hits,proof=search.cosine_rank(reader,vector,allowed,48,minimum=-1.)
        self.assertEqual(hits,expected['embedding']);self.assertEqual(len(proof['visited_leaves']),len(reader.meta['vector_shards']))
        self.assertEqual(reader.metrics['vector_bytes'],sum(row['bytes'] for row in reader.meta['vector_shards']))
        self.assertLessEqual(reader.metrics['cache_peak_bytes'],30000)
        self.assertTrue(search.audit_cosine(reader,vector,allowed,hits,proof))
