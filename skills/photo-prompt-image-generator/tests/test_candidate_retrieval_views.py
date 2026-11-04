"""Search views preserve source/RID boundaries and one dense vote per document."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import photo_candidate_retrieval_views as views


class ViewContracts(unittest.TestCase):
    def setUp(self):
        self.record={'id':'cand_a','record_kind':'visual_option','content':{'en':'A strap joins the bag to the opposite shoulder.','ko':'끈이 가방과 반대쪽 어깨를 잇는다.'},'effects':{'dimensions':['relationship'],'properties':[]}}
        self.row={'id':views.view_id('cand_a','base','whole'),'candidate_id':'cand_a','realization_id':'base','key':'whole','kind':'whole','source_record_sha256':views.digest(self.record),'text_en':self.record['content']['en'],'text_ko':self.record['content']['ko'],'source_quotes':[{'pointer':'/content/en','quote':self.record['content']['en']}]}
        self.module={'schema':views.SCHEMA,'recipe':views.RECIPE,'views':[self.row]}

    def test_stale_source_and_diagnostics_fail(self):
        changed=copy.deepcopy(self.record);changed['content']['en']='A different relation.'
        with self.assertRaisesRegex(ValueError,'stale'):views.validate(self.module,{'cand_a':changed})
        changed=copy.deepcopy(self.record);changed['record_kind']='diagnostic'
        with self.assertRaisesRegex(ValueError,'diagnostic'):views.validate(self.module,{'cand_a':changed})

    def test_partial_modules_cannot_claim_complete_coverage(self):
        another=copy.deepcopy(self.record);another['id']='cand_b'
        with self.assertRaisesRegex(ValueError,'coverage'):views.validate(self.module,{'cand_a':self.record,'cand_b':another})
        views.validate(self.module,{'cand_a':self.record,'cand_b':another},require_complete=False)

    def test_views_cannot_grant_native_authority_or_admit_unknown_source_kinds(self):
        with self.assertRaisesRegex(ValueError,'no native approval'):
            views.validate({**self.module,'native_approval':True},{'cand_a':self.record})
        row={**self.row,'native_approval':True}
        with self.assertRaisesRegex(ValueError,'no native approval'):
            views.validate({**self.module,'views':[row]},{'cand_a':self.record})
        record=copy.deepcopy(self.record);record['record_kind']='historical_evidence'
        with self.assertRaisesRegex(ValueError,'unknown positive'):
            views.validate(self.module,{'cand_a':record})

    def test_sibling_realization_cannot_supply_quote(self):
        record=copy.deepcopy(self.record)
        record['effects']['realizations']={'mode':'one','branches':[{'id':'left'},{'id':'right'}]}
        record['content']['realization_content']={'left':{'en':'Left relation.'},'right':{'en':'Right relation.'}}
        row=copy.deepcopy(self.row);row.update(realization_id='left',source_record_sha256=views.digest(record),id=views.view_id('cand_a','left','whole'),source_quotes=[{'pointer':'/content/realization_content/right/en','quote':'Right relation.'}])
        with self.assertRaisesRegex(ValueError,'sibling'):views.validate({**self.module,'views':[row]},{'cand_a':record},require_complete=False)

    def test_more_views_do_not_sum_or_multiply_dense_votes(self):
        rows=[{'id':'a1','candidate_id':'a','realization_id':'base'},{'id':'a2','candidate_id':'a','realization_id':'base'},{'id':'b1','candidate_id':'b','realization_id':'base'}]
        dense,witness=views.pool_scores(rows,[.5,.5,.7],['a|base','b|base'])
        self.assertEqual(dense,[.5,.7]);self.assertEqual(witness[0]['view_id'],'a1')
        self.assertEqual(witness[0]['considered_views'],2)

    def test_rid_boundaries_and_missing_population_fail(self):
        rows=[{'id':'a1','candidate_id':'a','realization_id':'left'}]
        with self.assertRaisesRegex(ValueError,'foreign'):views.pool_scores(rows,[.5],['a|right'])
        with self.assertRaisesRegex(ValueError,'lacks'):views.pool_scores(rows,[.5],['a|left','a|right'])

    def test_dense_documents_keep_one_lexical_identity_and_exclude_review_text(self):
        relation=copy.deepcopy(self.row)
        relation.update(id=views.view_id('cand_a','base','relation'),key='relation',kind='relation',
                        context_ko='검수 전용 경계',native_approval=False)
        module={**self.module,'views':[relation,self.row]}
        documents=views.documents(module,{'cand_a':self.record},['cand_a|base'])
        self.assertEqual(len(documents),2)
        self.assertEqual({row['document_id'] for row in documents},{'cand_a|base'})
        self.assertTrue(all(row['text']==views.document_text(self.row) for row in documents))
        self.assertNotIn('검수 전용',documents[0]['text'])
        self.assertEqual(documents,views.documents({**module,'views':list(reversed(module['views']))},
                                                  {'cand_a':self.record},['cand_a|base']))
        with self.assertRaisesRegex(ValueError,'population'):
            views.documents(module,{'cand_a':self.record},['cand_b|base'])

    def test_contract_values_cannot_replace_positive_source_evidence(self):
        row=copy.deepcopy(self.row)
        row['source_quotes']=[{'pointer':'/effects/dimensions/0','quote':'relationship'}]
        with self.assertRaisesRegex(ValueError,'positive content'):
            views.validate({**self.module,'views':[row]},{'cand_a':self.record})
        record=copy.deepcopy(self.record);record['id']='cand_b'
        with self.assertRaisesRegex(ValueError,'identity'):
            views.validate(self.module,{'cand_a':record})

    def test_nonfinite_and_non_numeric_dense_scores_fail(self):
        from fractions import Fraction
        row={'id':'a1','candidate_id':'a','realization_id':'base'}
        dense,_=views.pool_scores([row],[Fraction(1,2)],['a|base'])
        self.assertEqual(dense,[.5])
        for invalid in (float('nan'),float('inf'),True,'0.5'):
            with self.subTest(score=invalid),self.assertRaisesRegex(ValueError,'finite'):
                views.pool_scores([row],[invalid],['a|base'])


if __name__=='__main__':unittest.main()
