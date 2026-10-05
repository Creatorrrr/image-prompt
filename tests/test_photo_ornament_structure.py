"""Owner/variant boundaries and native all-of obligations for ornament DATA."""
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(SCRIPTS))
import prompt_generator as g
import photo_candidate_semantics as semantics
import audit_composed_prompt as auditor
from photo_contracts import property_effects_allowed

ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
EXT='photo_prompt_ornament_structure_extension.json'

class OrnamentStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ext=json.loads((ASSETS/EXT).read_text())
        cls.data=g.load_json(ASSETS/'photo_prompt_tags.json')
        cls.registry=g.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
        cls.profiles={p['id']:p for p in cls.registry['profiles'] if p['id'].startswith('orn_profile_')}
        cls.entries={e['id']:e for es in cls.ext['slots'].values() for e in es}
        cls.maintenance=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance/ornament-structure-20261005-v1.json').read_text())

    def matches(self,text):
        reg={**self.registry,'profiles':list(self.profiles.values())}
        return set(g.candidate_pack_auto_visual_obligation_matches(reg,[dict(source='concept_lock',text=text,polarity='required',mandatory=True)]))

    def test_precise_variant_labels_route_and_negation_removes_authority(self):
        for p in self.profiles.values():
            owner=p['activation']['hard_activation']['required_any_groups'][0]['any_terms'][0]
            for term in p['activation']['exact_terms']:
                with self.subTest(profile=p['id'],term=term):
                    self.assertIn(p['id'],self.matches('The declared '+owner+' owner shows '+term))
                    self.assertNotIn(p['id'],self.matches('The declared '+owner+' owner is without '+term))

    def test_broad_styles_and_process_names_do_not_require_a_fixed_structure(self):
        for text in ['a gothic portrait','goth fashion','Gothic maximalism','Ornate Gothic','Neo-Baroque',
                     'an ornamental object','an intricate metal artifact','filigree','lace','brocade','damask',
                     'kitbash','body horror','gore','eroguro','tenebrism','chiaroscuro','engraving','etching',
                     'a quiet greenhouse portrait with ivy','a plain contemporary ceramics gallery']:
            with self.subTest(text=text):self.assertEqual(set(),self.matches(text))

    def test_all_required_components_are_distinct_native_gates(self):
        gate_ids=[]
        for p in self.profiles.values():
            components=p['authored_components']['components']
            with self.subTest(profile=p['id']):
                self.assertGreaterEqual(len(components),2)
                self.assertEqual(len(components),p['semantics']['component_semantics']['minimum_component_groups'])
                self.assertEqual(len(components),len(p['render_gates']))
                for c in components:
                    self.assertEqual('native',c['render_gate']['review_scale'])
                    self.assertIn('partial evidence fails',c['render_gate']['description'])
                    self.assertIn('occlusion is unobservable',c['render_gate']['description'])
                    gate_ids.append(c['render_gate']['id'])
        self.assertEqual(len(gate_ids),len(set(gate_ids)))

    def test_filigree_backing_and_lobe_count_are_separate_variants(self):
        for term,yes,no in [
            ('open-backed wire filigree jewelry','orn_profile_gd13','orn_profile_gd14'),
            ('wire filigree jewelry on a continuous backing','orn_profile_gd14','orn_profile_gd13'),
            ('three-lobed ornamental opening','orn_profile_gd46_three','orn_profile_gd46_four'),
            ('four-lobed ornamental opening','orn_profile_gd46_four','orn_profile_gd46_three')]:
            with self.subTest(term=term):
                self.assertIn(yes,self.matches('The jewelry ornament shows '+term))
                self.assertNotIn(no,self.matches('The jewelry ornament shows '+term))
        self.assertFalse(any('stone' in u for u in self.entries['orn_gd51']['concept_units']))
        self.assertNotIn('stone',self.entries['orn_gd51']['en'])

    def test_clothing_lining_body_and_fabric_effects_respect_parent_locks(self):
        for eid in ['orn_gd32','orn_gd33','orn_gd40','orn_gd41']:
            e=self.entries[eid]
            lock=dict(contract_version='photo-intent-lock/v2',open_dimensions=e['affected_dimensions'],
                semantic_anchors=[dict(dimension='appearance',target='main_subject',property='wardrobe')])
            with self.subTest(candidate=eid):
                self.assertFalse(property_effects_allowed(lock,e['affected_dimensions'],e['affected_properties']))
                self.assertFalse(set(e['affected_dimensions']) & {'body_geometry','sexual_tone','age','identity','count','event'})
        e=self.entries['orn_gd32']
        for prop in ['wardrobe.lining','wardrobe.opacity']:
            lock=dict(contract_version='photo-intent-lock/v2',open_dimensions=e['affected_dimensions'],
                semantic_anchors=[dict(dimension='appearance',target='main_subject',property=prop)])
            self.assertFalse(property_effects_allowed(lock,e['affected_dimensions'],e['affected_properties']))

    def test_object_and_wearable_carriers_have_different_effect_owners(self):
        for source in ['gd13','gd14','gd06']:
            jewelry=self.entries['orn_'+source];obj=self.entries['orn_'+source+'_object']
            self.assertEqual({'main_subject'},{x['target'] for x in jewelry['affected_properties']})
            self.assertEqual({'depicted_artifact'},{x['target'] for x in obj['affected_properties']})
            self.assertNotEqual(jewelry['relations'],obj['relations'])

    def test_reused_candidates_preserve_every_existing_field_except_added_context(self):
        with mock.patch.object(g,'RESEARCH_EXTENSION_FILENAMES',tuple(x for x in g.RESEARCH_EXTENSION_FILENAMES if x!=EXT)):
            old=g.load_json(ASSETS/'photo_prompt_tags.json')
        for slot,updates in self.ext['existing_slot_context_extensions'].items():
            before={e['id']:e for e in old['slots'][slot]};after={e['id']:e for e in self.data['slots'][slot]}
            for eid,addition in updates.items():
                keep=set(before[eid])-{'paraphrases','contextual_usage'}
                with self.subTest(candidate=eid):
                    self.assertEqual({k:before[eid][k] for k in keep},{k:after[eid][k] for k in keep})
                    self.assertTrue(set(before[eid].get('paraphrases',[]))<=set(after[eid]['paraphrases']))
                    self.assertTrue(set(addition['paraphrases'])<=set(after[eid]['paraphrases']))

    def test_optional_bundles_carry_complete_components_and_effect_union(self):
        all_bundles={b['id']:b for b in self.data['candidate_bundles']}
        for raw in self.ext['visual_semantics']:
            with self.subTest(bundle=raw['id']):
                self.assertTrue(raw['candidate_only'])
                bundle=all_bundles[raw['id']]
                self.assertEqual(len(raw['component_groups']),len(bundle['components']))
                eid=raw['candidate_ids'][0];self.assertEqual(self.entries[eid]['affected_properties'],bundle['member_candidates'][0]['affected_properties'])
                self.assertEqual(len(self.entries[eid]['concept_units']),len(bundle['components']))

    def test_current_generated_indexes_bind_every_new_source(self):
        idx=g.load_visual_profile_index(ASSETS/'photo_prompt_visual_profile_index.json',self.registry)
        self.assertTrue(set(self.profiles)<=set(idx['entries']))
        semantic=g.load_semantic_index_payload(ASSETS/'photo_prompt_semantic_index.json')
        g.validate_semantic_index_metadata(semantic,self.data)
        keys=set(semantic['entries'])
        for slot,es in self.ext['slots'].items():
            for e in es:self.assertIn('slot:'+slot+':'+e['id'],keys)

    def test_approximate_retrieval_never_creates_hard_authority(self):
        # Controlled vectors test the authority boundary, not embedding quality.
        for p in self.profiles.values():
            reg={**self.registry,'profiles':[p]}
            idx=g.build_visual_profile_index_payload(reg,vectors={p['id']:[1.0,0.0]},dimensions=2)
            result=g.resolve_visual_profile_hits(reg,[dict(source='authorial_core_interpretation',text='An existing ornament displays an unfamiliar related surface structure.',polarity='advisory')],
                visual_profile_index=idx,query_text='a previously unseen detailed object description',query_vector=[1.0,0.0],adult_context=False)
            with self.subTest(profile=p['id']):
                hit=next(x for x in result['hits'] if x['profile_id']==p['id'])
                self.assertTrue(hit['optional_eligible']);self.assertFalse(hit['hard_eligible'])

    def test_optional_selection_promotes_complete_gates_and_missing_component_fails(self):
        for p in self.profiles.values():
            pid=p['id'];reg={**self.registry,'profiles':[p]}
            result={'provenance':{'authorial_core':{'baseline_prompt_en':'An adult examines the declared existing ornament.',
                'intent_lock':{'open_dimensions':p['concept_candidate']['affected_dimensions'],'semantic_anchors':[]}}}}
            concepts=g.candidate_pack_visual_concept_candidates({g.VISUAL_OBLIGATIONS_DATA_KEY:reg},result,{},None,None,
                {'hits':[{'profile_id':pid,'optional_eligible':True,'match_basis':'embedding'}]})
            with self.subTest(profile=pid):
                self.assertIsNotNone(concepts)
                pack={'contract_version':'photo-candidate-pack/v6','visual_concept_candidates':concepts}
                candidate=concepts['candidates'][0];components=p['authored_components']['components']
                evidence={c['evidence_field']:c['evidence_terms'][0] for c in components};prompt='; '.join(evidence.values())+'.'
                composed={'prompt_en':prompt,'chosen_visual_concept_ids':[candidate['id']],'visual_obligation_evidence':{pid:evidence}}
                self.assertEqual([],auditor.audit_visual_obligations(pack,composed,prompt))
                effective,failures=auditor.derive_effective_visual_obligation_contract(pack,composed)
                self.assertEqual([],failures);self.assertTrue(effective['strict_gate_set'])
                self.assertEqual({c['render_gate']['id'] for c in components},set(effective['required_hard_gates']))
                broken=copy.deepcopy(composed);broken['visual_obligation_evidence'][pid].pop(components[-1]['evidence_field'])
                self.assertTrue(auditor.audit_visual_obligations(pack,broken,prompt))
                empty,failures=auditor.derive_effective_visual_obligation_contract(pack,{'chosen_visual_concept_ids':[]})
                self.assertIsNone(empty);self.assertEqual([],failures)

    def test_sources_and_nonvisual_claims_are_maintenance_only(self):
        self.assertEqual(semantics.digest(self.maintenance),self.ext['maintenance_ref']['sha256'])
        for slot,es in self.ext['slots'].items():
            for e in es:
                text=g.semantic_text_for_entry(e,slot)
                self.assertNotIn('https://',text)
                self.assertNotIn('RESEARCH_DRAFT',text)
                self.assertNotIn('user_judgment',text)
                self.assertNotIn('native scale',text)
                self.assertNotIn('historically authentic',text)

if __name__=='__main__':unittest.main()
