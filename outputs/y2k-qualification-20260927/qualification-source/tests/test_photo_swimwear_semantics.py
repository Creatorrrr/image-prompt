import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL/'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as cs
from visual_profile_contracts import compile_visual_profile


class SwimwearSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension=json.loads((SKILL/'assets/photo_prompt_swimwear_extension.json').read_text())
        raw=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.registry={**raw,'profiles':[p for p in raw['profiles'] if p['id'].startswith('sw_')]}
        cls.profiles={p['id']:p for p in cls.registry['profiles']}
        cls.index=pg.build_visual_profile_index_payload(cls.registry)
        cls.data=pg.load_json(SKILL/'assets/photo_prompt_tags.json')

    def hits(self,text):
        resolved=pg.resolve_visual_profile_hits(self.registry,[{'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}],visual_profile_index=self.index,adult_context=True)
        return {h['profile_id'] for h in resolved['hits'] if h.get('match_basis')=='exact' and h.get('hard_eligible')}

    def test_complete_relations_activate_but_single_components_do_not(self):
        for p in self.profiles.values():
            phrase=p['activation']['exact_terms'][0]
            with self.subTest(profile=p['id']):
                self.assertIn(p['id'],self.hits(phrase))
                for component in phrase.split('; '):
                    self.assertNotIn(p['id'],self.hits(component))
                self.assertNotIn(p['id'],self.hits('not '+phrase))

    def test_broad_labels_and_unrelated_contexts_do_not_harden(self):
        for phrase in ['swimwear','수영복','비키니','원피스 수영복','high-waisted bikini',
                       'high-leg','bandeau','halter','bikini armor','chainmail bikini',
                       '원피스 드레스','modest swimwear','UPF 50','removable pads',
                       'terry towel','ribbed scarf','cat eye sunglasses','nylon rope',
                       '1964 monokini','Brazilian','sports bra','leotard','wet hair']:
            with self.subTest(phrase=phrase): self.assertEqual(self.hits(phrase),set())

    def test_independent_axes_do_not_activate_their_confounds(self):
        pairs=[('sw_bandeau','sw_strapless'),('sw_triangle','sw_string'),
               ('sw_highleg','sw_midlowrise'),('sw_scoop','sw_scoopback'),
               ('sw_tankini','sw_onepiece'),('sw_swimdress','sw_wrapcover'),
               ('sw_cutout','sw_mesh'),('sw_shirred','sw_crinkle'),
               ('sw_wet','sw_finish'),('sw_rashguard','sw_surfsuit'),
               ('sw_jane','sw_springsuit'),('sw_crochet','sw_coverup'),
               ('sw_wrapfront','sw_twist'),('sw_boyleg','sw_highleg')]
        for a,b in pairs:
            for selected,other in [(a,b),(b,a)]:
                with self.subTest(selected=selected,other=other):
                    hits=self.hits(self.profiles[selected]['activation']['exact_terms'][0])
                    self.assertIn(selected,hits)
                    self.assertNotIn(other,hits)

    def test_bandeau_and_halter_relations_can_coexist(self):
        ids=['sw_bandeau','sw_halter']
        phrase='; '.join(self.profiles[i]['activation']['exact_terms'][0] for i in ids)
        self.assertTrue(set(ids)<=self.hits(phrase))

    def test_semantic_discovery_does_not_grant_hard_authority(self):
        selected='sw_rashguard'
        vectors={pid:([1.,0.] if pid==selected else [0.,1.]) for pid in self.profiles}
        index=pg.build_visual_profile_index_payload(self.registry,vectors=vectors,dimensions=2)
        query='the rashguard is a separate sleeved swim top with its own hem, beside a paddleboard'
        result=pg.resolve_visual_profile_hits(self.registry,[{'source':'authorial_core_interpretation','text':query,'polarity':'advisory'}],visual_profile_index=index,query_text=query,query_vector=[1.,0.],adult_context=True)
        hit=next(h for h in result['hits'] if h['profile_id']==selected)
        self.assertFalse(hit['hard_eligible'])
        self.assertTrue(hit['optional_eligible'])

    def test_selected_variants_keep_literal_evidence_and_gates_together(self):
        for p in self.profiles.values():
            with self.subTest(profile=p['id']):
                compiled=compile_visual_profile(p)
                rendered=json.dumps(compiled,ensure_ascii=False)
                for component in p['authored_components']['components']:
                    self.assertIn(component['evidence_terms'][0],rendered)
                    self.assertIn(component['render_gate']['id'],rendered)
                mutation=copy.deepcopy(p)
                mutation['authored_components']['components'][1]['evidence_field']=mutation['authored_components']['components'][0]['evidence_field']
                with self.assertRaises(ValueError): compile_visual_profile(mutation)

    def test_optional_bundle_needs_all_members_and_open_dimensions(self):
        own={b['id'] for b in self.extension['visual_semantics']}
        for b in [b for b in self.data['candidate_bundles'] if b['id'] in own]:
            with self.subTest(bundle=b['id']):
                self.assertEqual(b['profile_activation'],'independent_request_evidence_only')
                slots={}
                for m in b['member_candidates']:
                    if m['entry_id'].startswith('sw_candidate_'):
                        self.assertNotIn('body_geometry',m['affected_dimensions'])
                    else:
                        self.assertEqual(m['entry_id'],'high_rise_waist_navel_relation')
                    slots.setdefault(m['slot'],{'candidates':[]})['candidates'].append({'id':m['id'],'applicability':{'status':'eligible'}})
                dims={d for m in b['member_candidates'] for d in m['affected_dimensions']}
                pack={'slots':slots,'authorial_core':{'intent_lock':{'open_dimensions':list(dims)}}}
                data={**self.data,'candidate_bundles':[b]}
                self.assertEqual(len(cs.public_bundles(data,pack)['candidates']),1)
                closed=copy.deepcopy(pack);closed['authorial_core']['intent_lock']['open_dimensions']=[]
                self.assertEqual(cs.public_bundles(data,closed)['candidates'],[])
                missing=copy.deepcopy(pack);next(iter(missing['slots'].values()))['candidates'].pop()
                self.assertEqual(cs.public_bundles(data,missing)['candidates'],[])

    def test_maintenance_and_source_binding(self):
        ref=self.extension['maintenance_ref']
        record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(ref['record_id']+'.json')).read_text())
        self.assertEqual(ref['sha256'],cs.digest(record))
        raw=copy.deepcopy(self.extension);raw.pop('maintenance_ref')
        self.assertEqual(record['authored_source_sha256'],cs.digest(raw))
        for absent in ['sw_internal','sw_performance','sw_fibers','sw_era','sw_monokini','sw_coverage','sw_highrise']:
            self.assertNotIn(absent,self.profiles)
        members={m['entry_id'] for b in self.data['candidate_bundles'] if b['id']=='sw_bundle_highrise_classic' for m in b['member_candidates']}
        self.assertIn('high_rise_waist_navel_relation',members)

    def test_real_index_contains_new_candidates(self):
        index=pg.load_semantic_index_payload(SKILL/'assets/photo_prompt_semantic_index.json')
        pg.validate_semantic_index_metadata(index,self.data)
        ids={f"slot:{slot}:{e['id']}" for slot,entries in self.extension['slots'].items() for e in entries}
        self.assertTrue(ids<=set(index['entries']))

if __name__=='__main__': unittest.main()
