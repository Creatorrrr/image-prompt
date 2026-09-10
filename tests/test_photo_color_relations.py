"""Color contracts: narrow activation, opposite directions, optional ownership and index integrity."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as cs
from visual_profile_contracts import compile_visual_profile


class ColorRelationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension=json.loads((SKILL/'assets/photo_prompt_color_relations_extension.json').read_text())
        raw=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.registry={**raw,'profiles':[p for p in raw['profiles'] if p['id'].startswith('cr_')]}
        cls.profiles={p['id']:p for p in cls.registry['profiles']}
        cls.index=pg.build_visual_profile_index_payload(cls.registry)
        cls.data=pg.load_json(SKILL/'assets/photo_prompt_tags.json')

    def hits(self,text):
        result=pg.resolve_visual_profile_hits(self.registry,[{'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}],visual_profile_index=self.index,adult_context=False)
        return {h['profile_id'] for h in result['hits'] if h.get('match_basis')=='exact' and h.get('hard_eligible')}

    def test_complete_relation_required_and_negation_excluded(self):
        for p in self.profiles.values():
            text=p['activation']['exact_terms'][0]
            with self.subTest(profile=p['id']):
                self.assertIn(p['id'],self.hits(text))
                self.assertNotIn(p['id'],self.hits('not '+text))
                for component in text.split('; '):
                    self.assertNotIn(p['id'],self.hits(component))

    def test_broad_names_and_confounds_never_harden(self):
        for text in ['monochrome','Monochromatic','high contrast black and white','Analogous','Triadic',
                     'Split Complementary','Complementary','Bi-Color Lighting','tunable white fixture',
                     '두 색 옷을 입은 사람','a striped red blue shirt in white daylight',
                     'warm feeling','RGB','Kelvin','60–30–10 Rule','Color Pop','Color Discord',
                     'Selective Color','Photoshop Selective Color adjustment','Gradient','Gradient Mapping',
                     'Color Arc','Palette Inversion','equiluminance','Simultaneous Contrast',
                     '따뜻한 피사체 차가운 배경','웜쿨 대비','색 반복','배경 컬러 워시']:
            with self.subTest(text=text):self.assertEqual(self.hits(text),set())

    def test_opposite_directions_and_distinct_mechanisms_do_not_cross_harden(self):
        pairs=[('warm_subject','cool_subject'),('warm_foreground','cool_foreground'),
               ('warm_highlights','cool_highlights'),('vivid_on_muted','muted_on_vivid'),
               ('high_chroma','low_chroma'),('high_value_contrast','low_value_contrast'),
               ('dark_on_dark','light_on_light'),('accent_cluster','scattered_accent'),
               ('colored_key','colored_fill'),('chromatic_subject','neutral_subject'),
               ('horizontal_bands','vertical_bands'),('radial_color','concentric_color'),
               ('complex_subject','complex_background'),('duotone','tritone'),
               ('spatial_gradient','gradient_mapping'),('triadic','split_complementary'),
               ('monochromatic','achromatic'),('two_color_lights','duotone'),
               ('restricted_subject','restricted_background'),('square','tetradic_rectangle')]
        for a,b in pairs:
            for selected,other in [(a,b),(b,a)]:
                with self.subTest(selected=selected):
                    hits=self.hits(self.profiles['cr_'+selected]['activation']['exact_terms'][0])
                    self.assertIn('cr_'+selected,hits)
                    self.assertNotIn('cr_'+other,hits)

    def test_semantic_similarity_is_advisory_even_for_close_visual_query(self):
        target='cr_muted_on_vivid'
        vectors={pid:([1.,0.] if pid==target else [0.,1.]) for pid in self.profiles}
        index=pg.build_visual_profile_index_payload(self.registry,vectors=vectors,dimensions=2)
        query='A grayish lavender coat sits against brilliantly colored painted walls.'
        result=pg.resolve_visual_profile_hits(self.registry,[{'source':'authorial_core_interpretation','text':query,'polarity':'advisory'}],visual_profile_index=index,query_text=query,query_vector=[1.,0.],adult_context=False)
        hit=next(h for h in result['hits'] if h['profile_id']==target)
        self.assertFalse(hit['hard_eligible']);self.assertTrue(hit['optional_eligible'])

    def test_selected_components_and_native_thumbnail_gates_compile_together(self):
        for p in self.profiles.values():
            with self.subTest(profile=p['id']):
                compiled=compile_visual_profile(p);serialized=json.dumps(compiled,ensure_ascii=False)
                for c in p['authored_components']['components']:
                    self.assertIn(c['evidence_terms'][0],serialized)
                    self.assertIn(c['render_gate']['id'],serialized)
                bad=copy.deepcopy(p)
                bad['authored_components']['components'][1]['evidence_field']=bad['authored_components']['components'][0]['evidence_field']
                with self.assertRaises(ValueError):compile_visual_profile(bad)

    def test_bundles_require_members_and_every_affected_open_dimension(self):
        for b in [b for b in self.data['candidate_bundles'] if b['id'].startswith('cr_')]:
            with self.subTest(bundle=b['id']):
                self.assertEqual(b['profile_activation'],'independent_request_evidence_only')
                slots={};dims=set()
                for member in b['member_candidates']:
                    dims.update(member['affected_dimensions'])
                    slots.setdefault(member['slot'],{'candidates':[]})['candidates'].append({'id':member['id'],'applicability':{'status':'eligible'}})
                pack={'slots':slots,'authorial_core':{'intent_lock':{'open_dimensions':list(dims)}}}
                data={**self.data,'candidate_bundles':[b]}
                self.assertEqual(len(cs.public_bundles(data,pack)['candidates']),1)
                for dim in dims:
                    closed=copy.deepcopy(pack);closed['authorial_core']['intent_lock']['open_dimensions'].remove(dim)
                    self.assertEqual(cs.public_bundles(data,closed)['candidates'],[])
                missing=copy.deepcopy(pack);next(iter(missing['slots'].values()))['candidates'].clear()
                self.assertEqual(cs.public_bundles(data,missing)['candidates'],[])

    def test_source_binding_and_unmeasurable_or_sequence_concepts_excluded(self):
        ref=self.extension['maintenance_ref']
        record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(ref['record_id']+'.json')).read_text())
        self.assertEqual(ref['sha256'],cs.digest(record))
        raw=copy.deepcopy(self.extension);raw.pop('maintenance_ref')
        self.assertEqual(record['authored_source_sha256'],cs.digest(raw))
        for family in ['equiluminance','simultaneous_contrast','palette_continuity','palette_progression','palette_shift','palette_inversion','color_motif','color_coding']:
            coverage=record['maintenance_only']['family_coverage'][family]
            self.assertEqual(coverage['candidates'],[]);self.assertEqual(coverage['profiles'],[])
        for slot,entries in self.extension['slots'].items():
            for e in entries:
                self.assertNotIn('http',e['embedding_text'])
                if slot=='lighting':self.assertEqual(set(e['affected_dimensions']),{'lighting','color'})

    def test_real_indexes_cover_authored_data_and_are_current(self):
        index=pg.load_semantic_index_payload(SKILL/'assets/photo_prompt_semantic_index.json')
        pg.validate_semantic_index_metadata(index,self.data)
        ids={f"slot:{slot}:{e['id']}" for slot,entries in self.extension['slots'].items() for e in entries}
        self.assertTrue(ids<=set(index['entries']))
        raw=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        vindex=json.loads((SKILL/'assets/photo_prompt_visual_profile_index.json').read_text())
        pg.validate_visual_profile_index_metadata(vindex,raw)

if __name__=='__main__':unittest.main()
