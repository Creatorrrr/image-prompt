import copy
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as semantics

class HistoricalWomenswearTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension=json.loads((SKILL/'assets/photo_prompt_historical_womenswear_extension.json').read_text())
        raw=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.registry={**raw,'profiles':[p for p in raw['profiles'] if p['id'].startswith('hw_')]}
        cls.index=pg.build_visual_profile_index_payload(cls.registry)
        cls.data=pg.load_json(SKILL/'assets/photo_prompt_tags.json')
    def hard_hits(self,text):
        result=pg.resolve_visual_profile_hits(self.registry,[{'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}],visual_profile_index=self.index,adult_context=True)
        return {h['profile_id'] for h in result['hits'] if h.get('match_basis')=='exact' and h.get('hard_eligible')}
    def test_complete_forms_and_missing_relations(self):
        self.assertEqual(len(self.registry['profiles']),24)
        for p in self.registry['profiles']:
            with self.subTest(profile=p['id']):
                for term in p['activation']['exact_terms']:
                    self.assertIn(p['id'],self.hard_hits(term))
                parts=p['activation']['exact_terms'][0].split('; ')
                if len(parts)>1:
                    self.assertNotIn(p['id'],self.hard_hits('; '.join(parts[:-1])))
    def test_homonyms_and_broad_names_remain_advisory(self):
        cases=['ruffled clown collar','avian feather ruff','broderie anglaise eyelet blouse',
               'morning walk in a black dress','glass cloche on a table','camera reticle',
               '한복','개량한복','장옷','쓰개치마','당의','robe à la française',
               'robe à l’anglaise','polonaise','qipao','1920s','lingerie dress','panniers']
        for text in cases:
            with self.subTest(text=text): self.assertEqual(self.hard_hits(text),set())
    def test_fitted_back_and_lifted_overskirt_can_coexist(self):
        profiles={p['id']:p for p in self.registry['profiles']}
        ids=['hw_anglaise_fitted_back','hw_polonaise_three_lifts']
        text='; '.join(profiles[i]['activation']['exact_terms'][0] for i in ids)
        self.assertTrue(set(ids)<=self.hard_hits(text))
    def test_embedding_only_discovery_does_not_impose_a_variant(self):
        for profile in self.registry['profiles']:
            with self.subTest(profile=profile['id']):
                vectors={p['id']:([1.0,0.0] if p['id']==profile['id'] else [0.0,1.0]) for p in self.registry['profiles']}
                index=pg.build_visual_profile_index_payload(self.registry,vectors=vectors,dimensions=2)
                phrase=profile['semantics']['paraphrase_examples'][0]
                resolution=pg.resolve_visual_profile_hits(self.registry,[{'source':'authorial_core_interpretation','text':phrase,'polarity':'advisory'}],visual_profile_index=index,query_text=phrase,query_vector=[1.0,0.0],adult_context=True)
                hit=next(h for h in resolution['hits'] if h['profile_id']==profile['id'])
                self.assertEqual(hit['match_basis'],'embedding')
                self.assertFalse(hit['hard_eligible'])
                self.assertTrue(hit['optional_eligible'])
    def test_real_merged_entries_and_optional_scope_guards(self):
        own={b['id'] for b in self.extension['visual_semantics']}
        bundles=[b for b in self.data['candidate_bundles'] if b['id'] in own]
        self.assertEqual(len(bundles),24)
        merged={f"slot:{slot}:{e['id']}":e for slot,es in self.data['slots'].items() for e in es}
        for b in bundles:
            with self.subTest(bundle=b['id']):
                self.assertEqual(b['profile_activation'],'independent_request_evidence_only')
                slots={}
                for m in b['member_candidates']:
                    self.assertIn(m['id'],merged)
                    self.assertTrue(m['affected_dimensions'])
                    self.assertNotIn('body_geometry',m['affected_dimensions'])
                    slots.setdefault(m['slot'],{'candidates':[]})['candidates'].append({'id':m['id'],'applicability':{'status':'eligible'}})
                dims={d for m in b['member_candidates'] for d in m['affected_dimensions']}
                pack={'slots':slots,'authorial_core':{'intent_lock':{'open_dimensions':list(dims)}}}
                data={**self.data,'candidate_bundles':[b]}
                self.assertEqual(len(semantics.public_bundles(data,pack)['candidates']),1)
                closed=copy.deepcopy(pack);closed['authorial_core']['intent_lock']['open_dimensions']=[]
                self.assertEqual(semantics.public_bundles(data,closed)['candidates'],[])
                missing=copy.deepcopy(pack);next(iter(missing['slots'].values()))['candidates'].pop()
                self.assertEqual(semantics.public_bundles(data,missing)['candidates'],[])
    def test_variant_discovery_requires_more_than_a_bare_garment_family(self):
        profile=next(p for p in self.registry['profiles'] if p['id']=='hw_qipao_1920_loose')
        for term in ['qipao','cheongsam','치파오','창파오']:
            with self.subTest(bare_family=term):
                self.assertIn(term,profile['concept_candidate']['concept_terms'])
                self.assertIsNone(pg.candidate_pack_visual_component_match(profile,term))
        for term in ['loose cheongsam','1920s cheongsam','넉넉한 치파오']:
            with self.subTest(variant=term):
                self.assertIsNotNone(pg.candidate_pack_visual_component_match(profile,term))
                self.assertNotIn(profile['id'],self.hard_hits(term))
    def test_source_binding_and_real_index(self):
        ref=self.extension['maintenance_ref']
        record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(ref['record_id']+'.json')).read_text())
        self.assertEqual(ref['sha256'],semantics.digest(record))
        raw=copy.deepcopy(self.extension);raw.pop('maintenance_ref')
        self.assertEqual(record['authored_source_sha256'],semantics.digest(raw))
        index=pg.load_semantic_index_payload(SKILL/'assets/photo_prompt_semantic_index.json')
        pg.validate_semantic_index_metadata(index,self.data)
        expected={f"slot:{slot}:{e['id']}" for slot,es in self.extension['slots'].items() for e in es}
        self.assertEqual(len(expected),50)
        self.assertTrue(expected<=set(index['entries']))
if __name__=='__main__': unittest.main()
