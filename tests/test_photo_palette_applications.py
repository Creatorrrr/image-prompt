"""Palette ownership, confounds, optionality, lock boundaries and live indexes."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL/'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as cs
from photo_contracts import property_effects_allowed
from visual_profile_contracts import compile_visual_profile


class PaletteApplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension=json.loads((SKILL/'assets/photo_prompt_palette_applications_extension.json').read_text())
        cls.full_registry=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.registry={**cls.full_registry,'profiles':[p for p in cls.full_registry['profiles'] if p['id'].startswith('pa_')]}
        cls.profiles={p['id']:p for p in cls.registry['profiles']}
        cls.index=pg.build_visual_profile_index_payload(cls.registry)
        cls.data=pg.load_json(SKILL/'assets/photo_prompt_tags.json')

    def hard_hits(self,text):
        result=pg.resolve_visual_profile_hits(self.registry,[{'source':'concept_lock','text':text,'polarity':'required','mandatory':True}],visual_profile_index=self.index,adult_context=False)
        return {r['profile_id'] for r in result['hits'] if r.get('hard_eligible')}

    def test_names_partial_components_negation_and_adjacent_scenes_do_not_harden(self):
        for text in ['Tiffany Blue','Black & Gold','Burberry check','De Stijl','청화백자','Viridis','오방색',
                     'blue cup beside a white vessel','a cyan shirt beside a magenta sign',
                     'a pale opaque gray plastic object','yellow paint beside a black wall',
                     'three primary-colored objects on separate tables']:
            with self.subTest(text=text):self.assertEqual(self.hard_hits(text),set())
        for p in self.profiles.values():
            complete=p['activation']['exact_terms'][0]
            with self.subTest(profile=p['id']):
                self.assertIn(p['id'],self.hard_hits(complete))
                self.assertNotIn(p['id'],self.hard_hits('not '+complete))
                for component in complete.split('; '):self.assertNotIn(p['id'],self.hard_hits(component))

    def test_same_carrier_and_mechanism_profiles_cannot_substitute_for_each_other(self):
        pairs=[('pa_blue_motif_white_ceramic','pa_reflective_translucent_owners'),
               ('pa_painted_emissive_owners','pa_bounded_metal_trim'),
               ('pa_crossing_lines_same_carrier','pa_primary_rectangles_orthogonal'),
               ('pa_ordered_background_gradient','pa_dark_oxblood_bone_owners')]
        for a,b in pairs:
            for wanted,other in [(a,b),(b,a)]:
                hits=self.hard_hits(self.profiles[wanted]['activation']['exact_terms'][0])
                self.assertIn(wanted,hits);self.assertNotIn(other,hits)

    def test_embedding_only_discovery_remains_advisory(self):
        target='pa_blue_motif_white_ceramic'
        vectors={p:([1.,0.] if p==target else [0.,1.]) for p in self.profiles}
        index=pg.build_visual_profile_index_payload(self.registry,vectors=vectors,dimensions=2)
        text='Painted blue floral marks follow one glossy white porcelain cup, with highlights crossing the decoration.'
        result=pg.resolve_visual_profile_hits(self.registry,[{'source':'authorial_core_interpretation','text':text,'polarity':'advisory'}],visual_profile_index=index,query_text=text,query_vector=[1.,0.],adult_context=False)
        hit=next(r for r in result['hits'] if r['profile_id']==target)
        self.assertFalse(hit['hard_eligible']);self.assertTrue(hit['optional_eligible'])

    def test_full_components_keep_all_evidence_and_native_gates(self):
        for p in self.profiles.values():
            compiled=compile_visual_profile(p)
            components=p['authored_components']['components']
            self.assertEqual([c['evidence_field'] for c in components],compiled['required_evidence_fields'])
            self.assertEqual([c['render_gate']['id'] for c in components],[g['id'] for g in compiled['render_gates']])
            broken=copy.deepcopy(p);broken['authored_components']['components'][0].pop('render_gate')
            with self.assertRaises(ValueError):compile_visual_profile(broken)

    def test_carrier_effects_preserve_reference_and_cross_dimension_property_locks(self):
        for rows in self.extension['slots'].values():
            for row in rows:
                dims=row['affected_dimensions'];effects=row['affected_properties']
                self.assertTrue(property_effects_allowed({'contract_version':'photo-intent-lock/v2','semantic_anchors':[]},dims,effects))
                reference={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'reference_use','target':'main_subject','property':'appearance.face_hair'}]}
                self.assertTrue(property_effects_allowed(reference,dims,effects))
                for effect in effects:
                    self.assertNotEqual(effect['property'],'*')
                    lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'appearance','target':'main_subject','property':effect['property']}]}
                    self.assertFalse(property_effects_allowed(lock,dims,effects))
                    parent=copy.deepcopy(lock);parent['semantic_anchors'][0]['property']=effect['property'].split('.')[0]
                    self.assertFalse(property_effects_allowed(parent,dims,effects))

    def test_bundle_exposure_requires_every_member_and_open_effect(self):
        for b in [b for b in self.data['candidate_bundles'] if b['id'].startswith('palette_relation_')]:
            self.assertEqual(b['profile_activation'],'independent_request_evidence_only')
            slots={};dims=set()
            for m in b['member_candidates']:
                dims.update(m['affected_dimensions']);slots.setdefault(m['slot'],{'candidates':[]})['candidates'].append({'id':m['id'],'applicability':{'status':'eligible'}})
            pack={'slots':slots,'authorial_core':{'intent_lock':{'open_dimensions':list(dims)}}}
            data={**self.data,'candidate_bundles':[b]}
            self.assertEqual(len(cs.public_bundles(data,pack)['candidates']),1)
            for d in dims:
                closed=copy.deepcopy(pack);closed['authorial_core']['intent_lock']['open_dimensions'].remove(d)
                self.assertEqual(cs.public_bundles(data,closed)['candidates'],[])
            missing=copy.deepcopy(pack);next(iter(missing['slots'].values()))['candidates']=[]
            self.assertEqual(cs.public_bundles(data,missing)['candidates'],[])

    def test_actual_cup_and_background_surface_color_locks_are_not_owner_prefix_aliases(self):
        for profile_id,target in [('pa_food_container_color_owners','coffee_cup'),('pa_ordered_background_gradient','background_panel')]:
            p=self.profiles[profile_id]['concept_candidate']
            lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'color','target':target,'property':'surface.local_color'}]}
            self.assertFalse(property_effects_allowed(lock,p['affected_dimensions'],p['affected_properties']))

    def test_source_receipt_and_held_claims_remain_outside_runtime(self):
        ref=self.extension['maintenance_ref']
        record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(ref['record_id']+'.json')).read_text())
        self.assertEqual(ref['sha256'],cs.digest(record));raw=copy.deepcopy(self.extension);raw.pop('maintenance_ref')
        self.assertEqual(record['authored_source_sha256'],cs.digest(raw))
        self.assertEqual(set(record['maintenance_only']['held_claims']),{'P068','P089','P090','P093','P094','P095','P096','P097','P098','P099','P100'})
        serialized=json.dumps(self.extension,ensure_ascii=False)
        self.assertNotIn('research_owner_',serialized);self.assertNotIn('http',serialized)
        oxblood=next(r for r in self.extension['slots']['color'] if 'oxblood' in r['id'])
        self.assertNotIn('gold',oxblood['en'])

    def test_interpretation_context_does_not_change_existing_effects_or_index_text(self):
        for slot,updates in self.extension['existing_slot_context_extensions'].items():
            for cid,update in updates.items():
                row=next(r for r in self.data['slots'][slot] if r['id']==cid)
                unchanged=copy.deepcopy(row);unchanged.pop('contextual_usage',None)
                self.assertEqual(pg.semantic_text_for_entry(row,slot),pg.semantic_text_for_entry(unchanged,slot))
                self.assertEqual(cs.semantic_source(row,slot,self.data['candidate_semantic_policy']),cs.semantic_source(unchanged,slot,self.data['candidate_semantic_policy']))
                for c in update['contexts']:self.assertEqual(c['activation_authority'],'interpretation_only_not_a_required_visual_recipe')

    def test_current_real_indexes_bind_all_added_sources(self):
        index=pg.load_semantic_index_payload(SKILL/'assets/photo_prompt_semantic_index.json')
        pg.validate_semantic_index_metadata(index,self.data)
        expected={f'slot:{slot}:{r["id"]}' for slot,rows in self.extension['slots'].items() for r in rows}
        self.assertTrue(expected<=set(index['entries']))
        visual=pg.load_visual_profile_index_payload(SKILL/'assets/photo_prompt_visual_profile_index.json')
        pg.validate_visual_profile_index_metadata(visual,self.full_registry)

if __name__=='__main__':unittest.main()
