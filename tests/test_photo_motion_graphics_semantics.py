from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as generator
import audit_composed_prompt as auditor
from photo_contracts import property_effects_allowed


class PhotoMotionGraphicsSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.registry = generator.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}
        cls.source = json.loads((ASSETS / 'photo_prompt_visual_obligations_motion_graphics.json').read_text())
        cls.extension = json.loads((ASSETS / 'photo_prompt_motion_graphics_extension.json').read_text())
        cls.index = generator.load_visual_profile_index(ASSETS / 'photo_prompt_visual_profile_index.json', cls.registry)
        cls.semantic_index = generator.load_semantic_index_payload(ASSETS / 'photo_prompt_semantic_index.json')
        generator.validate_semantic_index_metadata(cls.semantic_index, cls.data)

    def isolated(self, pid):
        return {**self.registry, 'profiles': [self.profiles[pid]]}

    def test_bilingual_qualified_exact_and_negation_boundary_for_every_new_meaning(self):
        for source in self.source['profiles']:
            registry = self.isolated(source['id'])
            index = generator.build_visual_profile_index_payload(registry)
            for term in source['activation']['exact_terms']:
                with self.subTest(pid=source['id'], term=term):
                    rows = [{'source':'concept_lock', 'text':term, 'polarity':'required', 'mandatory':True}]
                    hit = generator.resolve_visual_profile_hits(registry, rows, visual_profile_index=index, adult_context=False)['hits'][0]
                    self.assertTrue(hit['hard_eligible'])
                    negative = [{'source':'concept_lock', 'text':'without '+term, 'polarity':'required', 'mandatory':True}]
                    rejected = generator.resolve_visual_profile_hits(registry, negative, visual_profile_index=index, adult_context=False)
                    self.assertFalse(any(h['hard_eligible'] for h in rejected['hits']))

    def test_embedding_only_equivalents_remain_optional_for_every_new_meaning(self):
        # Controlled vectors exercise authority, not real embedding quality.
        for source in self.source['profiles']:
            registry = self.isolated(source['id'])
            index = generator.build_visual_profile_index_payload(registry, vectors={source['id']:[1.0,0.0]}, dimensions=2)
            for text in source['semantics']['paraphrase_examples'][:2]:
                with self.subTest(pid=source['id'], text=text):
                    result = generator.resolve_visual_profile_hits(registry,
                        [{'source':'authorial_core_interpretation','text':text,'polarity':'advisory'}],
                        visual_profile_index=index, query_text='unseen descriptive equivalent', query_vector=[1.0,0.0], adult_context=False)
                    hit = next(h for h in result['hits'] if h['profile_id']==source['id'])
                    self.assertEqual(hit['match_basis'],'embedding')
                    self.assertTrue(hit['optional_eligible'])
                    self.assertFalse(hit['hard_eligible'])

    def test_broad_process_names_and_adjacent_owners_do_not_create_new_hard_duties(self):
        registry={**self.registry, 'profiles':[self.profiles[p['id']] for p in self.source['profiles']]}
        index=generator.build_visual_profile_index_payload(registry)
        for text in ['motion graphics', 'glow tracking echo loop', 'ordinary face contours',
                     'normal optical perspective', 'sound responsive animation', 'political data corruption',
                     '종이 없는 보통 인물 사진', '일반적인 한 사람의 얼굴과 머리카락']:
            with self.subTest(text=text):
                result=generator.resolve_visual_profile_hits(registry,[{'source':'concept_lock','text':text,'polarity':'required','mandatory':True}],visual_profile_index=index,adult_context=False)
                self.assertFalse(any(h['hard_eligible'] for h in result['hits']))

    def test_paraphrases_reach_both_real_indexes_without_entering_exact_lookup(self):
        exact={(row['profile_id'],row['term']) for row in self.index['exact_lookup']}
        for source in self.source['profiles']:
            pid=source['id']; paraphrases=source['semantics']['paraphrase_examples'][:2]
            self.assertTrue(all(text in self.index['entries'][pid]['text'] for text in paraphrases))
            self.assertTrue(all((pid,text) not in exact for text in paraphrases))
        for slot, entries in self.extension['slots'].items():
            for candidate in entries:
                indexed=self.semantic_index['entries'][f"slot:{slot}:{candidate['id']}"]
                self.assertTrue(all(text in indexed['text'] for text in candidate['paraphrases'][:2]))
                self.assertTrue(all(text in generator.semantic_bm25f_fields_for_entry(candidate,slot)['paraphrases'] for text in candidate['paraphrases'][:2]))
                self.assertGreater(indexed['bm25f_document']['fields']['paraphrases']['length'],0)
        changed=copy.deepcopy(self.registry)
        changed['profiles'][0]['semantics']['paraphrase_examples'].append('a new semantic variant')
        with self.assertRaisesRegex(ValueError,'registry_sha256'):
            generator.validate_visual_profile_index_metadata(self.index,changed)

    def test_optional_selection_promotes_every_component_and_missing_evidence_fails(self):
        for pid in ['mg_paper_cut_relation','mg_radial_repeat_relation','mg_silhouette_clip_relation',
                    'mg_text_on_path_relation','mg_offset_contours_relation','mg_stepped_copies_relation']:
            with self.subTest(pid=pid):
                registry=self.isolated(pid)
                profile=self.profiles[pid]
                result={'provenance':{'authorial_core':{'baseline_prompt_en':'An adult viewing the displayed artwork.',
                         'intent_lock':{'open_dimensions':['composition','material'],'semantic_anchors':[]}}}}
                data={generator.VISUAL_OBLIGATIONS_DATA_KEY:registry}
                concepts=generator.candidate_pack_visual_concept_candidates(data,result,{},None,None,
                            {'hits':[{'profile_id':pid,'optional_eligible':True,'match_basis':'embedding'}]})
                self.assertIsNotNone(concepts)
                pack={'contract_version':'photo-candidate-pack/v6','visual_concept_candidates':concepts}
                candidate=concepts['candidates'][0]
                obligation=candidate['opt_in_contract']['obligation']
                components=profile['authored_components']['components']
                evidence={c['evidence_field']:c['evidence_terms'][0] for c in components}
                prompt='; '.join(evidence.values())+'.'
                composed={'prompt_en':prompt,'chosen_visual_concept_ids':[candidate['id']],
                          'visual_obligation_evidence':{pid:evidence}}
                self.assertEqual(auditor.audit_visual_obligations(pack,composed,prompt),[])
                effective,failures=auditor.derive_effective_visual_obligation_contract(pack,composed)
                self.assertEqual(failures,[])
                self.assertEqual(set(effective['required_hard_gates']),{c['render_gate']['id'] for c in components})
                self.assertTrue(effective['strict_gate_set'])
                empty,failures=auditor.derive_effective_visual_obligation_contract(pack,{'chosen_visual_concept_ids':[]})
                self.assertIsNone(empty);self.assertEqual(failures,[])
                broken=copy.deepcopy(composed)
                broken['visual_obligation_evidence'][pid].pop(components[-1]['evidence_field'])
                self.assertTrue(auditor.audit_visual_obligations(pack,broken,prompt))

    def test_artifact_effect_cannot_bypass_its_property_lock_and_bundles_keep_all_of(self):
        source=self.extension['slots']['prop'][0]
        effect=source['affected_properties'][0]
        lock={'contract_version':'photo-intent-lock/v2','open_dimensions':['material','composition'],'semantic_anchors':[
            {**effect,'meaning':'preserve this artifact finish'}]}
        self.assertFalse(property_effects_allowed(lock,source['affected_dimensions'],source['affected_properties']))
        for bundle in self.extension['visual_semantics']:
            compiled=next(b for b in self.data['candidate_bundles'] if b['id']==bundle['id'])
            self.assertEqual(compiled['adoption'],'optional')
            self.assertEqual(compiled['profile_activation'],'independent_request_evidence_only')
            expected=[unit for member in compiled['member_candidates'] for unit in member['concept_units']]
            actual=[item['visible_evidence'][0] for item in bundle['component_groups']]
            self.assertEqual(expected,actual)
            self.assertTrue(all(set(group)=={'id','visible_evidence'} for group in bundle['component_groups']))


if __name__ == '__main__':
    unittest.main()
