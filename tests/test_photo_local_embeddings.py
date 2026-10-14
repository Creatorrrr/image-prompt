"""Backend isolation/cache evidence contracts, independent of model installation."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import photo_embedding_provider as p
import photo_local_embedding as local


class LocalEmbeddingContracts(unittest.TestCase):
    def setUp(self):
        self.lock={'schema':'photo-local-embedding-installation/v1','runtime':{'engine':'fixture'},
                   'space':{'provider':'embeddinggemma2-local','model':local.MODEL_ID,'dimensions':768,'revision':'fixture'}}
        self.patch=patch.object(local,'runtime_lock',return_value=self.lock);self.patch.start();self.addCleanup(self.patch.stop)
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.space=self.lock['space'];self.cache=Path(self.temp.name)

    def infer(self,texts,kind,space):
        rows=[]
        for encoded in local.model_inputs(texts,kind):
            v=[1.0]+[0.0]*767
            rows.append({'vector':v,'execution':{'schema':'photo-local-inference/v1','provider_executed':True,
                'space':space,'runtime':self.lock['runtime'],'installation_sha256':local.digest(self.lock),
                'kind':kind,'input_sha256':hashlib.sha256(encoded.encode()).hexdigest(),'vector_sha256':p.digest(v)}})
        return rows

    def test_batches_preserve_input_order_bindings_and_cache(self):
        with patch.object(local,'infer',side_effect=self.infer) as call:
            first=p.embed_many(['second','first'],[{'id':2},{'id':1}],self.cache,space=self.space)
            second=p.embed_many(['first','second'],[{'id':1},{'id':2}],self.cache,space=self.space)
        self.assertEqual(call.call_count,1)
        self.assertEqual([r['request']['binding']['id'] for r in first],[2,1])
        self.assertTrue(all(r['cache_hit'] for r in second))

    def test_document_and_query_never_share_cache_or_prefix(self):
        with patch.object(local,'infer',side_effect=self.infer) as call:
            a=p.embed('same',{},self.cache,space=self.space,kind='query')
            b=p.embed('same',{},self.cache,space=self.space,kind='document')
        self.assertEqual(call.call_count,2);self.assertNotEqual(a['execution']['input_sha256'],b['execution']['input_sha256'])

    def test_rehashed_vector_cannot_claim_old_execution(self):
        with patch.object(local,'infer',side_effect=self.infer):p.embed('test',{},self.cache,space=self.space)
        file=next(self.cache.glob('*/RESULT.json'));row=json.loads(file.read_bytes())
        row['vector']=[0.0,1.0]+[0.0]*766;row['vector_sha256']=p.digest(row['vector']);file.write_bytes(p.canonical_bytes(row))
        with self.assertRaises(ValueError):p.embed('test',{},self.cache,space=self.space)

    def test_gemini_evidence_cannot_be_used_for_local(self):
        with self.assertRaises(ValueError):p.validate_execution({'provider_executed':True,'http_status':200,'response_sha256':'a'*64},self.space,'test',[1.0]+[0.0]*767)

    def test_revision_mismatch_and_bad_cardinality_fail_closed(self):
        foreign={**self.space,'revision':'different'}
        with self.assertRaises(ValueError):p.embed('test',{},self.cache,space=foreign)
        with self.assertRaises(ValueError):p.embed_many(['test'],[],self.cache,space=self.space)

    def test_local_failure_is_recorded_and_does_not_call_gemini(self):
        with patch.object(local,'infer',side_effect=RuntimeError('OOM')):
            with self.assertRaises(RuntimeError):p.embed('test',{},self.cache,space=self.space)
        self.assertEqual(json.loads(next(self.cache.glob('*/ATTEMPT-*.json')).read_bytes())['state'],'failed')
        with patch.object(local,'infer',side_effect=self.infer):self.assertFalse(p.embed('test',{},self.cache,space=self.space)['cache_hit'])

    def test_prefixes_are_applied_exactly_once_by_the_adapter(self):
        self.assertEqual(local.model_inputs(['text'],'query'),['task: search result | query: text'])
        self.assertEqual(local.model_inputs(['text'],'document'),['title: none | text: text'])

    def test_import_does_not_import_torch_or_start_inference(self):
        code="import sys;sys.path.insert(0,"+repr(str(ROOT/'skills/photo-prompt-image-generator/scripts'))+");import photo_embedding_provider,photo_local_embedding;assert 'torch' not in sys.modules;assert photo_local_embedding._WORKER is None"
        subprocess.run([sys.executable,'-c',code],check=True)

    def test_local_document_index_rejects_gemini_execution(self):
        from tests.test_photo_global_retrieval import GlobalDiscoveryTests
        import photo_shared_views as views
        import photo_global_index as index
        data=GlobalDiscoveryTests().data();vectors=data['_global_index'];vectors['space']=self.space
        for row in vectors['entries'].values():row['embedding_execution']={'provider_executed':True,'http_status':200,'response_sha256':'a'*64}
        with self.assertRaises(ValueError):index.validate(vectors,views.source(data))

    def test_verified_model_cache_detects_subsequent_file_tampering(self):
        self.patch.stop()
        root=self.cache/'installation';package=root/'model';package.mkdir(parents=True)
        weight=package/'weights.bin';weight.write_bytes(b'original')
        files={'weights.bin':{'bytes':8,'sha256':hashlib.sha256(b'original').hexdigest()}}
        lock={'schema':'photo-local-embedding-installation/v1','space':{'model':local.MODEL_ID,'model_package_sha256':local.digest(files)},'files':files,'package':'model'}
        (root/'embedding-runtime.lock.json').write_text(json.dumps(lock))
        local.runtime_lock(root);weight.write_bytes(b'modified')
        with self.assertRaises(ValueError):local.runtime_lock(root)


if __name__=='__main__':unittest.main()
