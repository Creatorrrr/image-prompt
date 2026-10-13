import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from tests.test_photo_global_retrieval import GlobalDiscoveryTests
from tests.test_photo_slot_queries import synthetic_set
from tests.photo_native_runtime import compose_native
import prompt_generator as g
import photo_candidate_corpus as c
import photo_shared_views as views
import photo_search_layout as layout
import photo_runtime_sources as runtime
import audit_global_retrieval as audit
import audit_composed_prompt


class NativeSlotWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GlobalDiscoveryTests.setUpClass();cls.core=GlobalDiscoveryTests.core;cls.controls=GlobalDiscoveryTests.controls
        path=Path('docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en/embodiment-review.json')
        cls.embodiment=json.loads(path.read_text())

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)/'source';self.store=Path(self.temp.name)/'runtime'
        for name in ('scripts','precore'):shutil.copytree(runtime.SKILL_ROOT/name,self.root/name,ignore=shutil.ignore_patterns('__pycache__'))
        assets=self.root/'assets';assets.mkdir();fixture=GlobalDiscoveryTests().data();source=views.source(fixture)
        source['policies']['_quality_layers']={'adult_appeal':{'contextual_retrieval':{'contract_version':'photo-contextual-appeal/v2'}}}
        fixture['_global_index']['corpus_sha256']=c.digest(source);modules=[]
        for field,schema in c.MODULE_SCHEMAS.items():
            name='photo_candidate_'+field+'.json';modules.append({'file':name,'kind':field});(assets/name).write_bytes(c.canonical_bytes({'schema':schema,field:source[field]}))
        (assets/c.MANIFEST_NAME).write_bytes(c.canonical_bytes({'schema':c.MANIFEST_SCHEMA,'modules':modules}))
        layout.build(assets,source,fixture['_global_index'],activate=True)
        self.provider=runtime.RuntimeSnapshotProvider(self.root,self.store);self.provider.publisher.publish();self.snapshot=self.provider.acquire()
        self.context=synthetic_set(self.core,self.controls,self.snapshot.data['slot_catalog'],['lighting','light_type','color'])

    def pack(self):
        return g.generate_candidate_pack(self.snapshot.data,self.core,self.controls,self.embodiment,seed=5,query_context=self.context,requested_slots=['lighting','light_type','color'])

    def test_pack_receipt_fresh_worker_and_independent_audit(self):
        pack=self.pack();self.assertEqual(pack['contract_version'],'photo-candidate-pack/v8')
        receipt=self.provider.receipt(self.snapshot,pack)
        new=runtime.RuntimeSnapshotProvider(self.root,self.store);snap=new.from_receipt(pack,receipt)
        self.assertEqual(audit.audit(pack,snap.data,snap.query_context),[])
        composed=compose_native(pack);report=audit_composed_prompt.audit_composed_prompt(pack,composed,source_data=snap.data,query_context=snap.query_context)
        self.assertEqual(report['status'],'pass',report)

    def test_foreign_proposal_and_old_pack_are_rejected(self):
        pack=self.pack();p=copy.deepcopy(pack);pid=next(iter(p['role_proposals']));p['role_proposals'][pid]['conditions']={}
        self.assertTrue(audit.audit(p,self.snapshot.data,self.context))
        p=copy.deepcopy(pack);p['contract_version']='photo-candidate-pack/v7'
        self.assertRaises(ValueError,runtime.photo_native_pack.validate,p)

    def test_unpublished_source_is_blocked_without_eager_bootstrap(self):
        other=runtime.RuntimeSnapshotProvider(self.root,self.store/'empty')
        self.assertRaises(runtime.FreshnessError,other.acquire)

    def test_composer_view_exposes_request_roles_for_untagged_candidates(self):
        import compose_pack_view as view
        pack=self.pack();overview=view.build_view(pack)
        self.assertEqual(overview['contract_version'],'photo-composer-view/v4')
        cid='cand_'+'b'*32
        row=next(r for r in overview['candidate_catalog'] if r['id']==cid)
        self.assertEqual(row['role_tags'],['color','light_type','lighting'])
        detail=view.build_view(pack,[cid])['candidates'][0]
        self.assertEqual(detail['role_bindings'],[])
        self.assertEqual({r['target_slot_id'] for r in detail['role_proposals']},set(row['role_tags']))
