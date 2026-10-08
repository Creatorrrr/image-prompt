from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg
from photo_contracts import property_effects_allowed
from photo_candidate_semantics import semantic_source
from visual_profile_contracts import compile_visual_profile


class PhotoElectricalRelationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source=json.loads((ASSETS/'photo_prompt_visual_obligations_electrical_relations.json').read_text())
        cls.profiles={p['id']:compile_visual_profile(p) for p in source['profiles']}
        cls.scoped={**source,'profiles':list(cls.profiles.values())}
        data=json.loads((ASSETS/'photo_prompt_electrical_relations_extension.json').read_text())
        cls.entries={r['id']:r for rows in data['slots'].values() for r in rows}

    def profile(self, slug):
        return self.profiles['electric_'+slug+'_relation']

    def hard(self, text):
        resolution=pg.resolve_visual_profile_hits(self.scoped,[{
            'source':'user_requirement','text':text,'polarity':'required'}])
        return {h['profile_id'] for h in resolution['hits'] if h.get('hard_eligible')}

    def test_generic_terms_metaphors_and_color_are_not_discharge_subtypes(self):
        for text in ['electricity','전기','번개','a spark between their personalities',
                     'electric-blue fabric','a lightning tattoo','a crown-shaped hairstyle',
                     'an ECG medical context','an energetic worker','a neon-colored coat']:
            with self.subTest(text=text): self.assertFalse(self.hard(text))

    def test_complete_owned_proposition_activates_only_its_declared_subtype(self):
        for slug in ['short_spark_gap','tip_local_corona','bounded_glow_tube',
                     'plasma_globe_center_radial','closed_circuit_loop','open_switch_gap']:
            p=self.profile(slug)
            with self.subTest(slug=slug): self.assertEqual(self.hard(p['semantics']['definition']),{p['id']})

    def test_missing_endpoints_cannot_complete_spark_bridge(self):
        p=self.profile('short_spark_gap')
        self.assertIsNotNone(pg.candidate_pack_visual_component_match(p,'A spark bridges metal terminals across an air gap.'))
        for text in ['A spark in dark air.', 'Metal terminals beside a spark print.',
                     'An air gap between two unluminous metal tips.',
                     'A spark behind one metal electrode.']:
            with self.subTest(text=text):self.assertIsNone(pg.candidate_pack_visual_component_match(p,text))

    def test_tube_glow_needs_enclosure_electrodes_and_interior_gas(self):
        p=self.profile('bounded_glow_tube')
        self.assertIsNotNone(pg.candidate_pack_visual_component_match(p,
            'A glass discharge tube has metal end caps enclosing luminous gas inside the tube.'))
        for text in ['A neon-colored coat with metal end caps.',
                     'A glass tube next to a glowing wire.',
                     'A gas glow in open air near two electrodes.']:
            with self.subTest(text=text):self.assertIsNone(pg.candidate_pack_visual_component_match(p,text))

    def test_printed_owner_confound_rejects_even_with_all_physical_words(self):
        for slug,prefix in [('short_spark_gap','printed spark'),
                            ('cloud_ground_branched_channel','printed lightning'),
                            ('closed_circuit_loop','printed circuit diagram')]:
            p=self.profile(slug);text=prefix+' depicting '+p['semantics']['definition']
            with self.subTest(slug=slug):
                self.assertIsNone(pg.candidate_pack_visual_component_match(p,text))
                self.assertFalse(self.hard(text))

    def test_similarity_cannot_turn_a_complete_owned_proposal_into_a_user_duty(self):
        p=self.profile('short_spark_gap');scope={**self.scoped,'profiles':[p]}
        index=pg.build_visual_profile_index_payload(scope,vectors={p['id']:[1.,0.]},dimensions=2)
        text='A spark bridges metal terminals across an air gap.'
        result=pg.resolve_visual_profile_hits(scope,[{'source':'authorial_core_interpretation',
            'text':text,'polarity':'advisory'}],visual_profile_index=index,
            query_text=text,query_vector=[1.,0.])
        hit=next(h for h in result['hits'] if h['profile_id']==p['id'])
        self.assertFalse(hit['hard_eligible']);self.assertTrue(hit['optional_eligible'])

    def test_partial_locks_and_moving_carriers_cannot_bypass_conservative_effects(self):
        for eid,dimension,prop in [('electric_radial_static_hair','appearance','hair.geometry'),
            ('electric_static_cling_cloth','appearance','wardrobe.contact_state'),
            ('electric_skin_lichtenberg_fern_pattern','appearance','skin.marking'),
            ('electric_cloud_ground_branched_channel','lighting','source.geometry'),
            ('electric_closed_circuit_loop','setting','apparatus.topology')]:
            entry=self.entries[eid]
            lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[
                {'dimension':dimension,'target':'requester_owned_object','property':prop}]}
            with self.subTest(candidate=eid):
                self.assertFalse(property_effects_allowed(lock,entry['affected_dimensions'],entry['affected_properties']))
                lock['semantic_anchors'][0]['dimension']='material'
                self.assertFalse(property_effects_allowed(lock,entry['affected_dimensions'],entry['affected_properties']))

    def test_family_splits_do_not_share_incompatible_connections_or_owners(self):
        voltage=self.entries['electric_meter_voltage_parallel']['concept_units']
        current=self.entries['electric_meter_current_series']['concept_units']
        self.assertTrue(any('in parallel' in u for u in voltage));self.assertFalse(any('in series' in u for u in voltage))
        self.assertTrue(any('in series' in u for u in current));self.assertFalse(any('in parallel' in u for u in current))
        barrier=self.entries['electric_fantasy_external_barrier']
        armor=self.entries['electric_fantasy_surface_armor']
        self.assertIn('separate_from',{r['type'] for r in barrier['relations']})
        self.assertIn('follows',{r['type'] for r in armor['relations']})
        for bad_id in ['electric_meter_probes_same_nodes','electric_fantasy_spear_blade_whip',
                       'electric_fantasy_barrier_armor_shell','electric_fictional_crown_altar_mark']:
            self.assertNotIn(bad_id,self.entries)

    def test_device_glow_keeps_reference_face_and_hair_locks_but_declares_new_owner_scope(self):
        lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[
            {'dimension':'appearance','target':'main_subject','property':p}
            for p in ['face.features','hair.shape','facial_appearance','hairstyle']]}
        for eid in ['electric_short_spark_gap','electric_tip_local_corona','electric_bounded_glow_tube']:
            entry=self.entries[eid]
            with self.subTest(candidate=eid):
                self.assertIn('setting',entry['affected_dimensions'])
                self.assertIn('lighting',entry['affected_dimensions'])
                self.assertTrue(property_effects_allowed(lock,entry['affected_dimensions'],entry['affected_properties']))
        hair=self.entries['electric_radial_static_hair']
        self.assertFalse(property_effects_allowed(lock,hair['affected_dimensions'],hair['affected_properties']))

    def test_deferred_purpose_and_history_do_not_leak_into_positive_search_text(self):
        for eid,entry in self.entries.items():
            source=semantic_source(entry)
            projection=json.dumps({k:source.get(k) for k in ['concept_units','relations']},ensure_ascii=False)
            for term in ['http://','https://','source_id','research_only','runtime_ready',
                         'electroejaculation','electrical torture','successful treatment']:
                with self.subTest(candidate=eid,term=term):self.assertNotIn(term,projection)
        for eid in ['electric_metaphoric_interpersonal_spark','electric_erotic_electrostimulation_context',
                    'electric_brief_staccato_flash','electric_fantasy_overcharge_exhaustion']:
            self.assertNotIn(eid,self.entries)

    def test_unreferenced_component_and_fabricated_gate_projection_fail_compilation(self):
        p=copy.deepcopy(self.profile('plasma_globe_center_radial'))
        p.pop('required_evidence_fields');p.pop('evidence_requirements');p.pop('render_gates');p.pop('composition_instruction')
        p['semantics'].pop('component_semantics')
        p['authored_components']['obligations'][0]['component_ids']=['different_globe']
        with self.assertRaisesRegex(ValueError,'unknown components'):compile_visual_profile(p)
        p=copy.deepcopy(self.profile('short_spark_gap'));p['render_gates'][0]['description']='a different duty without its electrodes'
        with self.assertRaisesRegex(ValueError,'conflicts'):compile_visual_profile(p)


if __name__=='__main__':unittest.main()
