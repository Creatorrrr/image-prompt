"""Meaning/owner boundaries, opt-in all-of evidence, and generated source binding."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as g
import photo_candidate_semantics as cs
import audit_composed_prompt as audit
from photo_contracts import property_effects_allowed
from visual_profile_contracts import compile_visual_profile

EXT = 'photo_prompt_ethereal_gothic_scene_extension.json'


class EtherealGothicSceneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ext = json.loads((SKILL/'assets'/EXT).read_text())
        cls.data = g.load_json(SKILL/'assets/photo_prompt_tags.json')
        cls.full_registry = g.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']:p for p in cls.full_registry['profiles'] if p['id'].startswith('egr_profile_')}
        cls.registry = {**cls.full_registry, 'profiles':list(cls.profiles.values())}
        cls.entries = {e['id']:e for es in cls.ext['slots'].values() for e in es}

    def exact(self, text):
        return set(g.candidate_pack_auto_visual_obligation_matches(self.registry,[
            dict(source='concept_lock',text=text,polarity='required',mandatory=True)]))

    def test_narrow_bilingual_positives_negation_and_owner_context(self):
        for pid,p in self.profiles.items():
            owner = p['activation']['hard_activation']['required_any_groups'][0]['any_terms'][0]
            for term in p['activation']['exact_terms']:
                with self.subTest(profile=pid,term=term):
                    self.assertIn(pid,self.exact('The existing '+owner+' shows '+term))
                    self.assertNotIn(pid,self.exact('The existing '+owner+' is without '+term))

    def test_broad_genre_hardware_material_and_context_negatives_do_not_harden(self):
        for text in ['ethereal gothic portrait','quiet melancholic portrait','gothic fashion',
                     'Symbolist photographic adaptation','Art Nouveau', 'Rinpa', 'gold leaf',
                     'a golden control panel','a simple gold mosaic','black lace','tulle',
                     'a low bun','a blunt fringe','mume','camellia','magnolia',
                     'a black rose','a moody low-key image','fine grain','optical diffusion',
                     'matte blacks','a cool porcelain cup','an ordinary bubble tea',
                     'corrupted data file','a sleepy face','a menacing gaze']:
            with self.subTest(text=text): self.assertEqual(set(), self.exact(text))

    def test_bounded_surface_physical_botanical_and_light_owners_are_distinct(self):
        pairs=[('gold_ground_sparse_botanical_screen','mume_on_leafless_woody_branches'),
               ('gold_leaf_like_bounded_panel','gold_mosaic_tesserae'),
               ('gilded_artifact_branch','mume_on_leafless_woody_branches'),
               ('frost_on_petals','dew_on_petals'),
               ('dew_on_petals','dried_curled_petals'),
               ('neutral_lowered_upper_lids','closed_eyes_composed_repose')]
        for a,b in pairs:
            for yes,no in [(a,b),(b,a)]:
                p=self.profiles['egr_profile_'+yes]
                owner=p['activation']['hard_activation']['required_any_groups'][0]['any_terms'][0]
                with self.subTest(wanted=yes,wrong=no):
                    hits=self.exact('The existing '+owner+' shows '+p['activation']['exact_terms'][1])
                    self.assertIn('egr_profile_'+yes,hits)
                    self.assertNotIn('egr_profile_'+no,hits)
        slit=self.entries['egr_occluded_vertical_emissive_slit']
        self.assertTrue(any('occludes' in c for c in slit['concept_units']))
        self.assertEqual({'rear_aperture','main_subject'},{e['target'] for e in slit['affected_properties']})
        self.assertFalse(set(slit['affected_dimensions']) & {'appearance','expression','sexual_tone','identity'})

    def test_no_forced_nape_fringe_emotion_lining_or_species_from_styles(self):
        for e in self.entries.values():
            self.assertFalse(set(e['affected_dimensions']) & {'age','identity','species','role','event','count','sexual_tone'})
            self.assertTrue(all(effect['property']!='*' for effect in e['affected_properties']))
        self.assertNotEqual(self.entries['egr_nape_coiled_bun']['id'],'low_bun_hair')
        self.assertNotEqual(self.entries['egr_brow_level_blunt_fringe']['id'],'ca_blunt_fringe')
        for eid in ['egr_high_collar_lace_structure','egr_micropleated_tulle_panel','egr_matte_mourning_crape']:
            self.assertFalse(any('lining' in e['property'] for e in self.entries[eid]['affected_properties']))

    def test_cross_carrier_parent_property_locks_and_reference_hair_are_preserved(self):
        for eid in ['egr_nape_coiled_bun','egr_brow_level_blunt_fringe','egr_separate_cheek_tendrils','egr_attached_trailing_hair_ribbon']:
            e=self.entries[eid]
            lock=dict(contract_version='photo-intent-lock/v2',semantic_anchors=[
                dict(dimension='reference_use',target='main_subject',property='hair')])
            with self.subTest(candidate=eid):
                self.assertFalse(property_effects_allowed(lock,e['affected_dimensions'],e['affected_properties']))
        for e in self.entries.values():
            for effect in e['affected_properties']:
                owner=effect['target'] if effect['target']!='*' else 'main_subject'
                lock=dict(contract_version='photo-intent-lock/v2',semantic_anchors=[
                    dict(dimension='appearance',target=owner,property=effect['property'].split('.')[0])])
                with self.subTest(candidate=e['id'],property=effect['property']):
                    self.assertFalse(property_effects_allowed(lock,e['affected_dimensions'],e['affected_properties']))

    def test_palette_hues_remain_local_roles_without_inferred_material_or_skin(self):
        rows=[e for e in self.entries.values() if e['id'].startswith('egr_palette_')]
        self.assertEqual(20,len(rows))
        for e in rows:
            self.assertEqual(['color'],e['affected_dimensions'])
            self.assertEqual(3,len(e['concept_units']))
            self.assertFalse(any('skin' in u or 'face' in u for u in e['concept_units']))
            self.assertTrue(all(u.startswith(('the declared','a separate declared','the smaller declared')) for u in e['concept_units']))
            self.assertFalse(any(x['property'].startswith(('skin','hair','form','wardrobe.material')) for x in e['affected_properties']))

    def test_grain_particles_haze_still_air_and_diffusion_are_separate(self):
        particles=self.entries['egr_localized_suspended_particles']
        haze=self.entries['egr_localized_haze_depth']
        settled=self.entries['egr_still_air_hanging_elements']
        self.assertNotEqual(particles['affected_properties'],haze['affected_properties'])
        self.assertNotEqual(haze['affected_properties'],settled['affected_properties'])
        self.assertTrue(all(x['target']=='scene' for x in particles['affected_properties']))
        generic=self.entries['egr_restrained_diffusion_detail']
        self.assertFalse(any('halo' in u for u in generic['concept_units']))
        old=next(e for e in self.data['slots']['quality'] if e['id']=='pe_neutral_diffusion')
        self.assertTrue(any('halo' in u for u in old['concept_units']))

    def test_every_selected_profile_keeps_complete_native_gates_and_missing_evidence_fails(self):
        for pid,p in self.profiles.items():
            components=p['authored_components']['components']
            compiled=compile_visual_profile(p)
            self.assertEqual(len(components),len(compiled['required_evidence_fields']))
            self.assertEqual(len(components),len(compiled['render_gates']))
            self.assertTrue(all(c['render_gate']['review_scale']=='native' for c in components))
            result={'provenance':{'authorial_core':{
                'baseline_prompt_en':'A person examines the selected existing owners.',
                'intent_lock':{'open_dimensions':p['concept_candidate']['affected_dimensions'],'semantic_anchors':[]}}}}
            concepts=g.candidate_pack_visual_concept_candidates({g.VISUAL_OBLIGATIONS_DATA_KEY:{**self.registry,'profiles':[p]}},result,{},None,None,
                {'hits':[{'profile_id':pid,'optional_eligible':True,'match_basis':'embedding'}]})
            with self.subTest(profile=pid):
                self.assertIsNotNone(concepts)
                pack={'contract_version':'photo-candidate-pack/v6','visual_concept_candidates':concepts}
                evidence={c['evidence_field']:c['evidence_terms'][0] for c in components}
                prompt='; '.join(evidence.values())+'.'
                composed={'prompt_en':prompt,'chosen_visual_concept_ids':[concepts['candidates'][0]['id']],
                    'visual_obligation_evidence':{pid:evidence}}
                self.assertEqual([],audit.audit_visual_obligations(pack,composed,prompt))
                contract,errors=audit.derive_effective_visual_obligation_contract(pack,composed)
                self.assertEqual([],errors)
                self.assertTrue(contract['strict_gate_set'])
                self.assertEqual({c['render_gate']['id'] for c in components},set(contract['required_hard_gates']))
                broken=copy.deepcopy(composed)
                broken['visual_obligation_evidence'][pid].pop(components[-1]['evidence_field'])
                self.assertTrue(audit.audit_visual_obligations(pack,broken,prompt))
                self.assertEqual((None,[]),audit.derive_effective_visual_obligation_contract(pack,{'chosen_visual_concept_ids':[]}))

    def test_embedding_only_paraphrase_is_optional_and_stale_registry_is_rejected(self):
        target='egr_profile_occluded_vertical_emissive_slit'
        reg={**self.registry,'profiles':[self.profiles[target]]}
        idx=g.build_visual_profile_index_payload(reg,vectors={target:[1.,0.]},dimensions=2)
        text='Only the portions of a tall thin illuminated gap outside her silhouette remain visible.'
        self.assertNotIn(text,self.profiles[target]['activation']['exact_terms'])
        result=g.resolve_visual_profile_hits(reg,[dict(source='authorial_core_interpretation',text=text,polarity='advisory')],
            visual_profile_index=idx,query_text=text,query_vector=[1.,0.],adult_context=False)
        hit=next(h for h in result['hits'] if h['profile_id']==target)
        self.assertTrue(hit['optional_eligible']);self.assertFalse(hit['hard_eligible'])
        changed=copy.deepcopy(reg);changed['profiles'][0]['semantics']['definition']+=' changed'
        with self.assertRaisesRegex(ValueError,'registry_sha256'):
            g.validate_visual_profile_index_metadata(idx,changed,provider='gemini',model=g.SEMANTIC_MODEL_ID,dimensions=2)

    def test_all_bundles_are_optional_atomic_and_missing_member_is_not_exposable(self):
        all_bundles={b['id']:b for b in self.data['candidate_bundles']}
        for raw in self.ext['visual_semantics']:
            b=all_bundles[raw['id']]
            self.assertEqual('independent_request_evidence_only',b['profile_activation'])
            slots={};dimensions=set()
            for m in b['member_candidates']:
                dimensions.update(m['affected_dimensions'])
                slots.setdefault(m['slot'],{'candidates':[]})['candidates'].append({'id':m['id'],'applicability':{'status':'eligible'}})
            pack={'slots':slots,'authorial_core':{'intent_lock':{'open_dimensions':list(dimensions)}}}
            data={**self.data,'candidate_bundles':[b]}
            with self.subTest(bundle=b['id']):
                self.assertEqual(1,len(cs.public_bundles(data,pack)['candidates']))
                missing=copy.deepcopy(pack);next(iter(missing['slots'].values()))['candidates']=[]
                self.assertEqual([],cs.public_bundles(data,missing)['candidates'])

    def test_existing_context_additions_do_not_rewrite_original_meaning_or_guards(self):
        inventory=g.photo_source_manifest.SourceInventory.for_test(SKILL/'assets',candidate_files=tuple(
            filename for filename in g.RESEARCH_EXTENSION_FILENAMES if filename not in {EXT,'photo_prompt_visual_grammar_extension.json'}))
        old=g.load_json(SKILL/'assets/photo_prompt_tags.json',inventory=inventory)
        for slot,updates in self.ext['existing_slot_context_extensions'].items():
            before={e['id']:e for e in old['slots'][slot]}
            after={e['id']:e for e in self.data['slots'][slot]}
            for eid,addition in updates.items():
                keys=set(before[eid])-{'paraphrases','contextual_usage'}
                self.assertEqual({k:before[eid][k] for k in keys},{k:after[eid][k] for k in keys})
                self.assertTrue(set(addition.get('paraphrases',[]))<=set(after[eid].get('paraphrases',[])))

    def test_real_generated_indexes_bind_new_sources_and_maintenance_is_not_search_text(self):
        index=g.load_visual_profile_index(SKILL/'assets/photo_prompt_visual_profile_index.json',self.full_registry)
        self.assertTrue(set(self.profiles)<=set(index['entries']))
        semantic=g.load_semantic_index_payload(SKILL/'assets/photo_prompt_semantic_index.json')
        g.validate_semantic_index_metadata(semantic,self.data)
        for slot,es in self.ext['slots'].items():
            for e in es:
                self.assertIn('slot:'+slot+':'+e['id'],semantic['entries'])
                text=g.semantic_text_for_entry(e,slot)
                self.assertNotIn('https://',text)
                self.assertNotIn('partial evidence fails',text)
                self.assertNotIn('20261007',text)
        record_id=self.ext['maintenance_ref']['record_id']
        record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(record_id+'.json')).read_text())
        self.assertEqual(cs.digest(record),self.ext['maintenance_ref']['sha256'])
        self.assertTrue(record['maintenance_only'])


if __name__=='__main__':unittest.main()
