"""Preserve the existing record-versus-rite meaning through final V6 semantics."""
from pathlib import Path
import copy,hashlib,importlib.util,json,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
EVIDENCE=ROOT/'docs/research-evidence/photo-prompt/jurisdiction-record-unit-data-cleanup-20261001'
PUBLIC=ROOT/'docs/research-evidence/photo-prompt/published-data-v6-surface-audit-20261001'
spec=importlib.util.spec_from_file_location('record_unit_surface',PUBLIC/'replay_public_surfaces.py');surface=importlib.util.module_from_spec(spec);spec.loader.exec_module(surface)
import photo_candidate_semantics as semantics


class JurisdictionRecordUnitDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen=json.loads((EVIDENCE/'frozen-inventory-queries.json').read_text())
        cls.data=surface.runtime_data()
        cls.rows={(s,r['id']):r for s,rows in cls.data['slots'].items()for r in rows}
        cls.target=next(r for r in cls.frozen['inventory']if r['decision']=='fix')
        cls.contract=json.loads((PUBLIC/'generated-contract-result.json').read_text())

    def test_frozen_inventory_queries_and_attempt_cap(self):
        self.assertEqual(hashlib.sha256((EVIDENCE/'frozen-inventory-queries.json').read_bytes()).hexdigest(),'573fec0781a16fe87a1f888b58719f0878e6052272a57eea6795855d60d6281f')
        self.assertEqual(len(self.frozen['inventory']),10)
        self.assertEqual(len(self.frozen['queries']),8)
        self.assertEqual(sum(q['authorship']=='independent_reviewer'for q in self.frozen['queries']),6)
        self.assertEqual(self.frozen['maximum_paid_calls'],10)
        self.assertEqual(hashlib.sha256((EVIDENCE/'acceptance-decisions.json').read_bytes()).hexdigest(),'d5e32513ec9b645ef5e5c578a826db0518c806e748fa84eb0ed6d1835d834932')

    def test_raw_extension_changes_only_one_new_verbatim_unit(self):
        before=json.loads((EVIDENCE/'baseline-raw-extension.json').read_text());expected=copy.deepcopy(before)
        row=next(r for r in expected['slots']['capture_context']if r['id']==self.target['id']);row['concept_units']=[row['en']]
        current=json.loads((ASSETS/'photo_prompt_cjk_worldbuilding_extension.json').read_text())
        self.assertEqual(current,expected)
        self.assertNotIn('maintenance_ref',current)

    def test_all_nine_keeps_and_every_existing_target_field_are_exact(self):
        for row in self.frozen['inventory']:
            current=self.rows[row['slot'],row['id']]
            self.assertEqual(current,row['proposed_after'])
            if row['decision']=='keep':self.assertEqual(current,row['before'])
        current=self.rows['capture_context',self.target['id']]
        self.assertEqual({k:v for k,v in current.items()if k!='concept_units'},self.target['before'])

    def test_long_original_sentence_is_intact_not_reworded_or_split(self):
        row=self.rows['capture_context',self.target['id']]
        self.assertEqual(len(row['en'].split()),25)
        self.assertEqual(row['concept_units'],[self.target['before']['en']])
        self.assertIn('non-sacred numbering, maps, handoff envelopes, and material traces rather than living rites, divine names, or sacred objects',row['concept_units'][0])
        self.assertEqual(semantics.semantic_source(row,'capture_context',self.data['candidate_semantic_policy'])['concept_units'],row['concept_units'])

    def test_actual_production_pack_and_detail_restore_the_full_contrast(self):
        slot=self.target['slot'];eid=self.target['id']
        old=surface.build_state(self.data,self.target['before'],slot,eid,self.contract)
        new=surface.build_state(self.data,self.rows[slot,eid],slot,eid,self.contract)
        self.assertIsNotNone(old['candidate']);self.assertIsNotNone(new['candidate'])
        self.assertNotIn('concept_units',old['candidate'])
        self.assertNotIn('semantic_surface_version',old['candidate'])
        self.assertTrue({'divine','sacred','rites'}.issubset(old['candidate']['concept_terms']))
        self.assertEqual(new['candidate']['concept_units'],[self.target['before']['en']])
        self.assertEqual(new['candidate']['concept_terms'],new['candidate']['concept_units'])
        self.assertEqual(new['candidate']['semantic_surface_version'],'photo-candidate-semantic-surface/v1')
        self.assertIsNotNone(new['detail'])

    def test_punk_long_labels_keep_existing_authored_keyword_units_and_bundles(self):
        for row in self.frozen['inventory']:
            if not row['id'].startswith('punk_'):continue
            current=self.rows[row['slot'],row['id']]
            self.assertTrue(semantics.semantic_source(current,row['slot'],self.data['candidate_semantic_policy'])['concept_units'])
            self.assertTrue(any(any(m['entry_id']==row['id']for m in b['member_candidates'])for b in self.data['candidate_bundles']))

    def test_coexisting_display_is_not_a_low_rank_or_global_exclusion(self):
        probes=self.frozen['queries']
        self.assertEqual(sum(q['kind']=='coexistence_control'for q in probes),2)
        self.assertEqual(sum(q['kind']=='ritual_contrast'for q in probes),2)
        self.assertTrue(all('no low-rank requirement'in q['assessment_role']for q in probes if q['kind']=='coexistence_control'))
        self.assertFalse(any(b['member_candidates'] and any(m['entry_id']==self.target['id']for m in b['member_candidates'])for b in self.data['candidate_bundles']))


if __name__=='__main__':unittest.main()
