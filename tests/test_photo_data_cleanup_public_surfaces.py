"""Final production pack surfaces, distinct from the intermediate term helper."""
from pathlib import Path
import importlib.util
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'docs/research-evidence/photo-prompt/published-data-v6-surface-audit-20261001'
spec=importlib.util.spec_from_file_location('data_surface_replay',EVIDENCE/'replay_public_surfaces.py')
replay=importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)


class DataCleanupPublicSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=replay.runtime_data()
        cls.contract=json.loads((EVIDENCE/'generated-contract-result.json').read_text())
        cls.audit=json.loads((EVIDENCE/'projection-audit.json').read_text())

    def candidate(self,slot,eid,control=None):
        entry=next(r for r in self.data['slots'][slot]if r['id']==eid)
        result=replay.build_state(self.data,entry,slot,eid,self.contract,control)
        self.assertIsNotNone(result['candidate'])
        self.assertIsNotNone(result['detail'])
        return result['candidate']

    def test_audit_covers_fifty_eight_published_rows_and_not_the_deferred_trial(self):
        self.assertEqual(len(self.audit['rows']),58)
        self.assertNotIn('reef_flat_crest_forereef_wave_gradient',{r['id']for r in self.audit['rows']})
        full=json.loads((EVIDENCE/'full-public-pack-audit.json').read_text())
        self.assertEqual(full['case_count'],58)
        multi=json.loads((EVIDENCE/'multichoice-full-public-pack-audit.json').read_text())
        self.assertEqual({r['id']for r in multi['cases']},{'mirror_selfie','poised_standing','harbor_fisherman'})

    def test_harbor_source_korean_label_does_not_imply_final_korean_units(self):
        row=next(r for r in self.data['slots']['subject']if r['id']=='harbor_fisherman')
        self.assertEqual(row['ko'],'동틀 무렵 항구에 있는 어부')
        final=self.candidate('subject','harbor_fisherman','auto_mechanic')
        self.assertEqual(final['concept_units'],['a harbor fisherman at dawn'])
        self.assertEqual(final['concept_terms'],final['concept_units'])
        self.assertNotIn('label_ko',final)

    def test_crochet_source_korean_label_preserves_english_final_unit(self):
        final=self.candidate('texture','crochet_loop_texture')
        row=next(r for r in self.data['slots']['texture']if r['id']=='crochet_loop_texture')
        self.assertEqual(final['concept_units'],[row['en']])
        self.assertEqual(final['concept_terms'],final['concept_units'])
        self.assertNotIn('label_ko',final)

    def test_jpeg_repaired_owner_survives_final_semantic_overlay(self):
        final=self.candidate('format','pr_jpeg_edge_blocking_candidate')
        self.assertEqual(final['relations'][0]['object'],'high_contrast_edges_of_the_compressed_image')
        self.assertIn('a file screen or repost context is explicit',final['concept_units'])
        self.assertIn('compression does not conceal the main gesture',final['concept_units'])
        self.assertEqual(final['semantic_surface_version'],'photo-candidate-semantic-surface/v1')


if __name__=='__main__':unittest.main()
