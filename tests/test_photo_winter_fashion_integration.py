"""Winter morphology boundaries and optional-to-hard activation regressions."""
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(SCRIPTS))
import prompt_generator as pg

class WinterFashionIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=pg.load_visual_obligation_registry(ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json')
        cls.winter={p['id']:p for p in cls.registry['profiles'] if p['id'].startswith('winter_')}
        cls.index=pg.build_visual_profile_index_payload(cls.registry)
        cls.data=pg.load_json(ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')

    def resolve(self,text,adult=True):
        return pg.resolve_visual_profile_hits(self.registry,[{'source':'user_requirement','text':text,'polarity':'required'}],visual_profile_index=self.index,adult_context=adult)

    def test_complete_selected_clause_can_bind_its_own_variant(self):
        for ident in ['winter_wf21_v1','winter_wf25_v1','winter_wf30_v1','winter_wf51_v2','winter_wf59_v1','winter_wf68_v1','winter_wf70_v3']:
            with self.subTest(profile=ident):
                text=self.winter[ident]['semantics']['definition']
                hits=[h for h in self.resolve(text)['hits'] if h['profile_id']==ident]
                self.assertTrue(hits)
                self.assertTrue(hits[0]['hard_eligible'])

    def test_names_confounds_and_hidden_specs_do_not_bind_family_variants(self):
        texts=['winter fashion with a warm wool coat','a cashmere-colored camel coat','a puffer marked 700 fill power','a waterproof-looking jacket in snowfall','a corduroy panel beside a ribbed concrete wall','a printed picture of a cable braid on flat cloth','a coat and a scarf lying separately on a table','a closed one-way zipper','bare skin beside a dark stocking','an Aran island landscape','a needle darts beside an underarm seam','Mob wife styling with a pile coat']
        for text in texts:
            with self.subTest(text=text):
                hard=[h['profile_id'] for h in self.resolve(text)['hits'] if h['profile_id'].startswith('winter_') and h['hard_eligible']]
                self.assertEqual(hard,[])

    def test_alternative_and_negation_do_not_activate_selected_definition(self):
        ident='winter_wf30_v1'
        opposite=self.winter['winter_wf30_v2']['semantics']['definition']
        self.assertFalse(any(h['profile_id']==ident and h['hard_eligible'] for h in self.resolve(opposite)['hits']))
        own=self.winter[ident]['semantics']['definition']
        result=pg.resolve_visual_profile_hits(self.registry,[{'source':'user_requirement','text':own,'polarity':'excluded'}],visual_profile_index=self.index,adult_context=True)
        self.assertFalse(any(h['profile_id']==ident and h['hard_eligible'] for h in result['hits']))

    def test_explicit_adult_variants_are_ineligible_without_adult_context(self):
        for ident in ['winter_wf50_v1','winter_wf50_v2']:
            text=self.winter[ident]['semantics']['definition']
            self.assertFalse(any(h['profile_id']==ident and h['hard_eligible'] for h in self.resolve(text,False)['hits']))

    def test_embedding_discovery_cannot_create_a_hard_duty(self):
        profiles=list(self.winter.values())[:4]
        registry={**self.registry,'profiles':profiles}
        vectors={p['id']:[1.0 if j==i else 0.0 for j in range(4)] for i,p in enumerate(profiles)}
        index=pg.build_visual_profile_index_payload(registry,vectors=vectors,dimensions=4)
        for i,p in enumerate(profiles):
            result=pg.resolve_visual_profile_hits(registry,[{'source':'authorial_core_interpretation','text':p['semantics']['paraphrase_examples'][0],'polarity':'advisory'}],visual_profile_index=index,query_vector=vectors[p['id']],adult_context=True)
            hit=next(h for h in result['hits'] if h['profile_id']==p['id'])
            self.assertFalse(hit['hard_eligible'])
            self.assertTrue(hit['optional_eligible'])

    def test_surface_candidate_keeps_hidden_fill_spec_as_context(self):
        entry=next(e for e in self.data['slots']['surface_material'] if e['id']=='winter_wf04_v1_candidate')
        contexts=entry['contextual_usage']['contexts']
        self.assertEqual({c['id'] for c in contexts},{'wf02_specification_boundary','wf03_specification_boundary'})
        self.assertNotIn('fill power',entry['embedding_text'].casefold())
        self.assertNotIn('700',entry['en'])

    def test_owner_and_complete_effects_survive_compilation(self):
        lookups={e['id']:e for entries in self.data['slots'].values() for e in entries}
        for ident,required in {
            'winter_wf25_v1_candidate':['wardrobe.closure.toggle_loop_path'],
            'winter_wf21_v1_candidate':['wardrobe.material.openwork','wardrobe.coverage.transmission','wardrobe.layers.order'],
            'winter_wf59_v1_candidate':['wardrobe.layers.order','wardrobe.color.distribution'],
            'winter_wf70_v3_candidate':['wardrobe.structure.thumbhole_path','wardrobe.coverage.hand'],
        }.items():
            with self.subTest(candidate=ident):
                entry=lookups[ident]
                self.assertTrue(entry['relations'][0]['subject'])
                self.assertTrue(entry['relations'][0]['object'])
                properties={e['property'] for e in entry['affected_properties']}
                self.assertTrue(set(required)<=properties)
                self.assertNotIn('camera',entry['affected_dimensions'])
                self.assertNotIn('body_geometry',entry['affected_dimensions'])

if __name__=='__main__':unittest.main()
