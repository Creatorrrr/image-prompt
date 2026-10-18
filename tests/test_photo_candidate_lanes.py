import copy
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/photo-prompt-image-generator/scripts'))
from photo_candidate_authoring import digest, file_sha
from photo_candidate_lane_documents import project, verify
from photo_candidate_lane_generation import accepted_reviews, verify_files
from tests.test_photo_candidate_authoring import fixture


class IndependentLanes(unittest.TestCase):
    def source(self):
        record,review=fixture()
        review['realizations']['base']['search_aliases']=[{'text':'rear stocking line','anchors':review['realizations']['base']['anchors']}]
        fields={'labels':['original cue'],'core_meaning':[],'aliases':[]}
        return record,review,fields

    def test_sparse_additions_do_not_change_D1_dense_input(self):
        record,review,fields=self.source();before=copy.deepcopy(record)
        result=project('original cue',fields,record,'base',arm='D1',review=review,catalog={})
        self.assertEqual(result['text'],'original cue')
        self.assertEqual(result['dense_additions'],[])
        self.assertEqual(result['fields']['aliases'],['rear stocking line'])
        self.assertEqual(result['fields']['core_meaning'],[review['realizations']['base']['summary_en']])
        self.assertEqual(record,before);self.assertEqual(fields['aliases'],[])

    def test_D1b_dense_keeps_whole_summary_but_excludes_alias(self):
        record,review,fields=self.source()
        summary=review['realizations']['base']['summary_en']+' The source does not establish physical stitching.'
        review['realizations']['base']['summary_en']=summary
        result=project('original cue',fields,record,'base',arm='D1b',review=review,catalog={})
        self.assertEqual(result['text'],'original cue\n'+summary)
        self.assertNotIn('rear stocking line',result['text'])
        self.assertEqual(result['dense_additions'][0]['review_sha256'],digest(review))

    def test_unreviewed_candidate_preserves_both_inputs(self):
        record,_,fields=self.source()
        for arm in ['D1','D1b']:
            result=project('original cue',fields,record,'base',arm=arm)
            self.assertEqual(result['text'],'original cue');self.assertEqual(result['fields'],fields)

    def test_forged_sparse_and_dense_values_are_rejected_independently(self):
        record,review,fields=self.source()
        valid=project('original cue',fields,record,'base',arm='D1',review=review,catalog={})
        for target in ['fields','text','provenance']:
            bad=copy.deepcopy(valid)
            if target=='fields':bad['fields']['aliases'].append('unapproved unrelated surface')
            elif target=='text':bad['text']+='\nunapproved text'
            else:bad['sparse_additions'][0]['anchors'][0]['quote']='fabricated physical seam'
            with self.assertRaises(ValueError):verify(bad,'original cue',fields,record,'base',arm='D1',review=review,catalog={})

    def test_cross_RID_source_and_unapproved_review_rejected(self):
        record,review,fields=self.source()
        with self.assertRaises(ValueError):project('original cue',fields,record,'other',arm='D1',review=review,catalog={})
        approval={'status':'PASS','reviews':{record['id']:{'sha256':digest(review),'source_sha256':digest(record)}}}
        accepted_reviews({record['id']:review},approval)
        review['realizations']['base']['summary_en']='unapproved replacement'
        with self.assertRaises(ValueError):accepted_reviews({record['id']:review},approval)

    def test_native_source_or_baseline_token_loss_is_not_masked_by_lane_split(self):
        record,review,fields=self.source()
        with self.assertRaises(ValueError):project('different cue',fields,record,'base',arm='D1',review=review,catalog={})
        record['meaning']['retrieval_class']='diagnostic';review['source_sha256']=digest(record)
        with self.assertRaises(ValueError):project('original cue',fields,record,'base',arm='D1',review=review,catalog={})

    def test_member_seal_rejects_tamper_traversal_and_linked_parent(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder).resolve();(root/'inside').mkdir();p=root/'inside/value';p.write_text('sealed')
            seal={'inside/value':file_sha(p)};verify_files(root,seal)
            p.write_text('tampered')
            with self.assertRaises(ValueError):verify_files(root,seal)
            with self.assertRaises(ValueError):verify_files(root,{'../value':'0'*64})
            (root/'link').symlink_to(root/'inside',target_is_directory=True)
            with self.assertRaises(ValueError):verify_files(root,{'link/value':file_sha(p)})


if __name__=='__main__':unittest.main()
