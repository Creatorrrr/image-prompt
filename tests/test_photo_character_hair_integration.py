"""Behavioral boundaries for reviewed regional hair relations."""
import copy,json,sys,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ASSETS.parent/'scripts'))
import photo_candidate_semantics as cs
import photo_contracts as contracts
import prompt_generator as pg
from visual_profile_contracts import compile_visual_profile,validate_visual_profile_source

class CharacterHairIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=json.loads((ASSETS/'photo_prompt_character_hair_extension.json').read_text())
        cls.visual=json.loads((ASSETS/'photo_prompt_visual_obligations_character_hair.json').read_text())
        cls.base=json.loads((ASSETS/'photo_prompt_visual_obligations.json').read_text())
        cls.entries=[e for rows in cls.source['slots'].values() for e in rows]
        cls.profiles={p['id']:compile_visual_profile(p) for p in cls.visual['profiles']}
        # Limit the fixture to the affected profiles while executing the real
        # hard-activation algorithm, rather than repeating the source aliases.
        cls.boundary_registry=copy.deepcopy(cls.base)
        cls.boundary_registry['profiles']=[compile_visual_profile(p) for p in cls.base['profiles']
            if p['id'] in {'wet_damp_clumped_hair_state','balayage_ribbon_color_placement'}]

    def matches(self,text):
        return set(pg.candidate_pack_auto_visual_obligation_matches(self.boundary_registry,[
            {'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}]))

    def test_dry_styling_and_method_names_do_not_assert_water_or_ribbon_pattern(self):
        for text in ['portrait with dry gel styled wet-look hair','balayage hair with a length gradient',
                     'a person holds two wet ribbons beside their hair']:
            with self.subTest(text=text):self.assertEqual(self.matches(text),set())
        self.assertEqual(self.matches('rain-damp hair in a portrait'),{'wet_damp_clumped_hair_state'})

    def test_selected_ribbons_can_coexist_with_a_length_gradient(self):
        self.assertEqual(self.matches('selected balayage ribbon pattern and an ombre hair gradient'),
                         {'balayage_ribbon_color_placement'})
        p=next(p for p in self.boundary_registry['profiles'] if p['id']=='balayage_ribbon_color_placement')
        self.assertNotIn('full_width_ombre_gradient',p['reject_substitutes'])
        self.assertNotIn('no full-width',p['composition_instruction'])

    def test_parent_locks_apply_to_every_new_relation_and_cannot_change_carrier(self):
        lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[
            {'dimension':'appearance','target':'main_subject','property':'hair'}]}
        other=copy.deepcopy(lock);other['semantic_anchors'][0]['target']='secondary_subject'
        for e in self.entries:
            with self.subTest(candidate=e['id']):
                self.assertFalse(contracts.property_effects_allowed(lock,e['affected_dimensions'],e['affected_properties']))
                self.assertTrue(contracts.property_effects_allowed(other,e['affected_dimensions'],e['affected_properties']))
                changed=[dict(row,dimension='material') for row in e['affected_properties']]
                self.assertFalse(contracts.property_effects_allowed(lock,['material'],changed))

    def test_profile_adoption_keeps_whole_relation_and_native_visibility_gates(self):
        for raw in self.visual['profiles']:
            with self.subTest(profile=raw['id']):
                validate_visual_profile_source(raw)
                p=self.profiles[raw['id']]
                self.assertTrue(p['evidence_requirements'])
                self.assertTrue(all(g['review_scale']=='native' for g in p['render_gates']))
                self.assertIn('unobservable',p['render_gates'][0]['description'])
                self.assertNotIn('render_gates',raw)
                self.assertNotIn('component_semantics',raw['semantics'])

    def test_new_names_remain_optional_and_do_not_add_appearance_duties(self):
        registry=dict(self.boundary_registry,profiles=list(self.profiles.values()))
        for text in ['jellyfish cut','box braids','underlights','Wet-look finish','a graduation ceremony with ribbons']:
            with self.subTest(text=text):
                self.assertEqual(pg.candidate_pack_auto_visual_obligation_matches(registry,[
                    {'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}]),{})

    def test_maintenance_hash_and_source_registrations_are_resolvable(self):
        reference=self.source['maintenance_ref']
        record_path=ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/ (reference['record_id']+'.json')
        record=json.loads(record_path.read_text())
        self.assertEqual(reference['sha256'],cs.digest(record))
        body={k:v for k,v in self.source.items() if k!='maintenance_ref'}
        self.assertEqual(record['authored_source_sha256'],cs.digest(body))
        manifest=json.loads((ASSETS/'photo_prompt_source_manifest.json').read_text())
        for name,kind in [('photo_prompt_character_hair_extension.json','candidate'),
                          ('photo_prompt_visual_obligations_character_hair.json','visual_profile')]:
            self.assertEqual(len([r for r in manifest['sources'] if r['file']==name and r['kind']==kind]),1)

if __name__=='__main__':unittest.main()
