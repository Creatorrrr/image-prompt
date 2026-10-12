"""Native optional selection preserves requester duties and the baseline."""
import copy,tempfile,unittest
from pathlib import Path
from tests import photo_api_fixtures as fixtures
from tests import photo_native_runtime as authored
import audit_composed_prompt as ca
import photo_candidate_corpus as c

class PhotoAuthorshipPolicyTests(unittest.TestCase):
    @staticmethod
    def composed(pack):return authored.compose_native(pack)
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        paths=fixtures.write_valid_inputs(Path(self.temp.name))
        self.pack=fixtures._template['pack'];self.composed=self.composed(self.pack)
        self.snapshot=fixtures._verified
    def audit(self,pack,composed):
        return ca.audit_composed_prompt(pack,composed,source_data=self.snapshot.data,query_context=self.snapshot.query_context)
    def test_declining_every_optional_candidate_preserves_frozen_baseline(self):
        report=self.audit(self.pack,self.composed)
        self.assertEqual(report['status'],'pass',report['failures'])
        self.assertEqual(self.composed['prompt_en'],self.pack['authorial_core']['baseline_prompt_en'])
    def test_hash_rewritten_foreign_candidate_cannot_replace_authored_owner(self):
        altered=copy.deepcopy(self.pack);row=next(iter(altered['candidate_pool'].values()))
        row['authored_record']['content']['en']='the opposite owner at camera right'
        self.assertEqual(self.audit(altered,self.composed)['status'],'fail')
    def test_omitting_requester_anchor_fails_even_with_optional_candidates_rejected(self):
        composed=copy.deepcopy(self.composed);core=self.pack['authorial_core']
        anchor=core['intent_lock']['semantic_anchors'][0]['prompt_evidence']
        composed['prompt_en']=composed['prompt_en'].replace(anchor,'unrelated substitution')
        self.assertEqual(self.audit(self.pack,composed)['status'],'fail')
