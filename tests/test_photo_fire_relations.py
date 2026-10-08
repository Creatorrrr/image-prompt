"""Fire meaning/owner regressions; these do not prove rendered fidelity."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
from photo_contracts import property_effects_allowed
from visual_profile_contracts import compile_visual_profile,hard_activation_is_supported


class FireRelationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension=json.loads((SKILL/'assets/photo_prompt_fire_relations_extension.json').read_text())
        cls.candidates={c['id']:c for rows in cls.extension['slots'].values() for c in rows}
        cls.authored=json.loads((SKILL/'assets/photo_prompt_visual_obligations_fire_relations.json').read_text())['profiles']
        cls.profiles={p['id']:compile_visual_profile(p) for p in cls.authored}

    def supported(self,p,text):
        return hard_activation_is_supported(p,text,matches=pg.intent_alias_matches,is_negated=pg.intent_term_is_negated)

    def test_whole_realization_only_and_negation(self):
        for p in self.authored:
            whole=p['activation']['exact_terms'][0]
            with self.subTest(profile=p['id']):
                self.assertTrue(self.supported(p,whole))
                self.assertFalse(self.supported(p,'not '+whole))
                self.assertFalse(self.supported(p,p['semantics']['paraphrase_examples'][0]))
                self.assertFalse(self.supported(p,p['semantics']['visual_components'][0]))

    def test_fire_flare_and_nonvisual_labels_create_no_exact_duties(self):
        for term in ['불','화염','불꽃','파란 불','flare','corona','filament','heat',
                     'cool flame','flashover','backdraft','pyrolysis','thermal runaway',
                     '온도','악취','불에 대한 열정','안전한 거리']:
            with self.subTest(term=term):
                self.assertFalse(any(self.supported(p,term) for p in self.authored))

    def test_natural_owned_components_enable_optional_discovery(self):
        cases={
          'F001':('A candle wick has a flame above the wick and a liquid wax pool.', 'An electric candle beside a glossy glass pool.'),
          'F004':('A source fire emits detached sparks with dark air separating them.', 'A bright source has translucent flare ghosts in the lens.'),
          'F039':('A fire beside the water casts a broken elongated reflection on the reflective water surface.', 'An orange lamp beside a dry metallic plate.'),
          'F041':('A hot surface has a background edge through hot air with localized waviness.', 'Heat shimmer is suggested by uniform lens blur.'),
          'F105':('The glass blowpipe has a glass gather attached and a shaping tool touching the gather.', 'A detached glass orb sits beside a hollow pipe.'),
          'F136':('A lava flow has a darker lava crust with orange gaps within the crust.', 'An orange flame above cold dark rocks.'),
        }
        for uid,(positive,negative) in cases.items():
            p=self.profiles['fire_rel_'+uid.lower()]
            with self.subTest(unit=uid):
                self.assertIsNotNone(pg.candidate_pack_visual_component_match(p,positive))
                self.assertIsNone(pg.candidate_pack_visual_component_match(p,negative))
                self.assertFalse(self.supported(p,positive))

    def test_carriers_cannot_bypass_camera_air_or_body_property_locks(self):
        for eid,target,prop in [
          ('fire_f041','heated_air_path','refractive_structure'),
          ('fire_f041','image_plane','optical.apparent_distortion'),
          ('fire_f059','main_subject','hair'),
          ('fire_f149','main_subject','body.skin'),
          ('fire_f150','main_subject','wardrobe.coverage'),
        ]:
            c=self.candidates[eid]
            lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'appearance','target':target,'property':prop}]}
            with self.subTest(candidate=eid,property=prop):
                self.assertFalse(property_effects_allowed(lock,c['affected_dimensions'],c['affected_properties']))
                moved=copy.deepcopy(c['affected_properties'])
                for row in moved:row['dimension']='material'
                self.assertFalse(property_effects_allowed(lock,['material'],moved))

    def test_optical_identity_reuse_keeps_the_original_effects(self):
        data=pg.load_json(SKILL/'assets/photo_prompt_tags.json')
        entries={c['id']:c for rows in data['slots'].values() for c in rows}
        for uid,eid in [('F131','pe_veiling_flare'),('F132','pe_aligned_ghosts'),('F133','pe_horizontal_anamorphic_streak')]:
            with self.subTest(unit=uid):
                self.assertNotIn('fire_'+uid.lower(),self.candidates)
                self.assertEqual(entries[eid]['affected_properties'],[{'dimension':'camera','target':'image_plane','property':'optical.lens_artifact'}])
                self.assertTrue(any(r['id']=='fire_'+uid.lower()+'_boundary' for r in entries[eid]['contextual_usage']['contexts']))
        self.assertNotIn('fire_f127',self.candidates)

    def test_existing_inventory_keeps_meaning_with_only_four_context_additions(self):
        files=tuple(n for n in pg.RESEARCH_EXTENSION_FILENAMES
                    if n!='photo_prompt_fire_relations_extension.json')
        inventory=pg.photo_source_manifest.SourceInventory.for_test(SKILL/'assets',candidate_files=files)
        before=pg.load_json(SKILL/'assets/photo_prompt_tags.json',inventory=inventory)
        current=pg.load_json(SKILL/'assets/photo_prompt_tags.json')
        additions={(slot,eid):addition
                   for slot,updates in self.extension['existing_slot_context_extensions'].items()
                   for eid,addition in updates.items()}
        self.assertEqual(set(additions),{
            ('subject','coronal_mass_ejection_observation_subject'),
            ('lens_artifact','pe_veiling_flare'),
            ('lens_artifact','pe_aligned_ghosts'),
            ('lens_artifact','pe_horizontal_anamorphic_streak'),
        })
        for slot,rows in before['slots'].items():
            actual={r['id']:r for r in current['slots'][slot]}
            for old in rows:
                key=(slot,old['id']);new=actual[old['id']]
                with self.subTest(slot=slot,candidate=old['id']):
                    if key not in additions:
                        self.assertEqual(new,old)
                        continue
                    self.assertEqual({k:v for k,v in new.items() if k not in {'paraphrases','contextual_usage'}},
                                     {k:v for k,v in old.items() if k not in {'paraphrases','contextual_usage'}})
                    prior=old.get('paraphrases',[])
                    self.assertEqual(new['paraphrases'][:len(prior)],prior)
                    self.assertEqual(new['paraphrases'][len(prior):],
                                     [p for p in additions[key]['paraphrases'] if p not in prior])
                    usage=old.get('contextual_usage',{});updated=new['contextual_usage']
                    self.assertEqual({k:v for k,v in updated.items() if k!='contexts'},
                                     {k:v for k,v in usage.items() if k!='contexts'})
                    prior_contexts=usage.get('contexts',[])
                    self.assertEqual(updated['contexts'][:len(prior_contexts)],prior_contexts)
                    self.assertEqual(updated['contexts'][len(prior_contexts):],additions[key]['contexts'])

    def test_unseen_source_and_channel_metadata_do_not_get_native_gates(self):
        for pid,absent in [('fire_rel_f038','vo_fire_f038_3'),('fire_rel_f118','vo_fire_f118_3'),('fire_rel_f130','vo_fire_f130_2')]:
            p=self.profiles[pid]
            with self.subTest(profile=pid):
                self.assertNotIn(absent,{g['id'] for g in p['render_gates']})
                self.assertEqual(len(p['required_evidence_fields']),3)
        channel=self.profiles['fire_rel_f130']
        self.assertIn('cannot be verified from the hue alone',channel['render_gates'][-1]['description'])

    def test_directed_connections_distinguish_fire_particles_and_residue(self):
        for eid,expected in [
          ('fire_f001',('anchors','wick','flame')),
          ('fire_f004',('emits','source','burning_particle')),
          ('fire_f005',('releases','source','fuel_fragment')),
          ('fire_f149',('rests_on','wax_deposit','selected_skin_patch')),
        ]:
            c=self.candidates[eid]
            with self.subTest(candidate=eid):
                self.assertIn(expected,{(r['type'],r['subject'],r['object']) for r in c['relations']})
        self.assertNotEqual(self.candidates['fire_f004']['affected_dimensions'],self.candidates['fire_f052']['affected_dimensions'])
        self.assertEqual(self.candidates['fire_f030']['affected_properties'][0]['property'],'motion.particle_trails')

    def test_context_only_processes_and_motives_stay_out_of_runtime_ids(self):
        deferred=['F009','F010','F017','F018','F027','F043','F044','F055','F066','F069','F072','F073','F076','F088','F091','F103','F109','F117','F122','F129','F135','F151','F154','F155']
        for uid in deferred:
            with self.subTest(unit=uid):
                self.assertNotIn('fire_'+uid.lower(),self.candidates)
                self.assertNotIn('fire_rel_'+uid.lower(),self.profiles)

    def test_bellows_graph_uses_the_declared_fire_bed_without_inventing_a_forge(self):
        c=self.candidates['fire_f097']
        self.assertIn('the same fire bed',c['en'])
        self.assertIn(('directed_at','outlet','declared_fire_bed'),
                      {(r['type'],r['subject'],r['object']) for r in c['relations']})
        self.assertFalse(any(r['object']=='forge' for r in c['relations']))
        self.assertIn('outlet directed_at declared_fire_bed',
                      self.profiles['fire_rel_f097']['render_gates'][-1]['description'])


if __name__=='__main__':unittest.main()
