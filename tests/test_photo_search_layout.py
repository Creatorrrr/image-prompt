import gzip
import math
import tempfile
import zlib
import unittest
from pathlib import Path
from tests.test_photo_global_retrieval import GlobalDiscoveryTests
import photo_candidate_corpus as c
import photo_search_layout as layout
import photo_shared_views as views


class SearchLayoutTests(unittest.TestCase):
    def test_binary_postings_preserve_exact_tf_and_reject_foreign_ordinals(self):
        ids=['cand_a','cand_b'];rows={'x':[['cand_b',1.234567890123],['cand_a',2.0]],'y':[['cand_b',3.0]]}
        raw=layout.posting_bytes(rows,{cid:i for i,cid in enumerate(ids)})
        page=layout.PostingPage(zlib.decompress(raw),ids)
        self.assertEqual(dict((term,list(page[term])) for term in page),{term:[tuple(r) for r in sorted(values)] for term,values in rows.items()})
        self.assertEqual(page['x'][-1],('cand_b',1.234567890123))
        with self.assertRaises(ValueError):layout.PostingPage(zlib.decompress(raw),ids[:1])

    def test_layout_covers_source_once_and_never_activates_by_default(self):
        data=GlobalDiscoveryTests().data();source=views.source(data)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);manifest=layout.build(root,source,data['_global_index'],leaf_size=1)
            self.assertFalse((root/layout.MANIFEST).exists())
            meta=c.decode(gzip.decompress((root/manifest['metadata']['path']).read_bytes()))
            ids=[cid for s in meta['vector_shards'] for cid in s['ids']]
            self.assertEqual(sorted(ids),sorted(data['candidates']));self.assertEqual(len(ids),len(set(ids)))
            self.assertEqual(set(meta['payload_locator']),set(data['candidates']))
            self.assertEqual(meta['statistics']['document_count'],3)

    def test_cap_bound_contains_descendants_and_handles_opposites(self):
        for center,cosine in [([1.,0.],0.8),([0.,0.],-1.)]:
            node={'center':center,'radius_cos':cosine}
            for query in ([1.,0.],[-1.,0.],[0.,1.]):
                bound=layout.upper_bound(node,query)
                if cosine>0:
                    for vector in ([1.,0.],[.8,.6],[.8,-.6]):
                        self.assertGreaterEqual(bound+1e-12,math.sumprod(vector,query))
                else:self.assertEqual(bound,1.)
