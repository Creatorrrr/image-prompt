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

class PalaceFortificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension=json.loads((SKILL/'assets/photo_prompt_palace_fortification_extension.json').read_text())
        registry=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.registry={**registry,'profiles':[p for p in registry['profiles'] if p['id'].startswith('pf_')]}
        cls.index=pg.build_visual_profile_index_payload(cls.registry)
        cls.data=pg.load_json(SKILL/'assets/photo_prompt_tags.json')

    def hard_hits(self,text):
        result=pg.resolve_visual_profile_hits(self.registry,[{'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}],visual_profile_index=self.index,adult_context=False)
        return {h['profile_id'] for h in result['hits'] if h.get('match_basis')=='exact' and h.get('hard_eligible')}

    def test_complete_relations_without_person_and_component_omission(self):
        for p in self.registry['profiles']:
            with self.subTest(profile=p['id']):
                for text in p['activation']['exact_terms']:
                    self.assertIn(p['id'],self.hard_hits(text))
                parts=p['activation']['exact_terms'][0].split('; ')
                for i in range(len(parts)):
                    self.assertNotIn(p['id'],self.hard_hits('; '.join(parts[:i]+parts[i+1:])))

    def test_homonyms_negation_and_broad_style_do_not_impose_geometry(self):
        cases=['I keep a notebook near a glass curtain wall','palace hotel lobby','a portcullis emblem on a banner',
               'castle','palace','고성','궁전','성채','enfilade','window seat','boiserie',
               'modern tourists at Neuschwanstein','a bright Gothic chapel','Rococo fashion editorial',
               'a palace without a moat','rubble masonry on a maintained house','a star-shaped roof',
               '금박 없는 회색 로코코 살롱','사람 없는 요새','나스르 궁전']
        for text in cases:
            with self.subTest(text=text):self.assertEqual(self.hard_hits(text),set())

    def test_gate_and_bridge_are_distinct_and_can_coexist(self):
        ps={p['id']:p for p in self.registry['profiles']}
        ids=['pf_portcullis','pf_drawbridge']
        for pid in ids:self.assertEqual(self.hard_hits(ps[pid]['activation']['exact_terms'][0]),{pid})
        self.assertTrue(set(ids)<=self.hard_hits('; '.join(ps[i]['activation']['exact_terms'][0] for i in ids)))

    def test_retrieval_never_hardens_an_advisory_interpretation(self):
        profile=self.registry['profiles'][0]
        vectors={p['id']:([1.,0.] if p['id']==profile['id'] else [0.,1.]) for p in self.registry['profiles']}
        index=pg.build_visual_profile_index_payload(self.registry,vectors=vectors,dimensions=2)
        text=profile['semantics']['paraphrase_examples'][0]
        result=pg.resolve_visual_profile_hits(self.registry,[{'source':'authorial_core_interpretation','text':text,'polarity':'advisory'}],visual_profile_index=index,query_text=text,query_vector=[1.,0.],adult_context=False)
        hit=next(h for h in result['hits'] if h['profile_id']==profile['id'])
        self.assertFalse(hit['hard_eligible']);self.assertTrue(hit['optional_eligible'])

    def test_bundle_scopes_and_missing_members(self):
        own={b['id'] for b in self.extension['visual_semantics']}
        bundles=[b for b in self.data['candidate_bundles'] if b['id'] in own]
        self.assertEqual(len(bundles),len(own))
        for b in bundles:
            with self.subTest(bundle=b['id']):
                self.assertEqual(b['profile_activation'],'independent_request_evidence_only')
                slots={}
                for m in b['member_candidates']:
                    self.assertTrue(set(m['affected_dimensions'])<= {'setting','composition'})
                    slots.setdefault(m['slot'],{'candidates':[]})['candidates'].append({'id':m['id'],'applicability':{'status':'eligible'}})
                pack={'slots':slots,'authorial_core':{'intent_lock':{'open_dimensions':['setting','composition']}}}
                data={**self.data,'candidate_bundles':[b]}
                self.assertEqual(len(semantics.public_bundles(data,pack)['candidates']),1)
                closed=copy.deepcopy(pack);closed['authorial_core']['intent_lock']['open_dimensions']=[]
                self.assertEqual(semantics.public_bundles(data,closed)['candidates'],[])
                missing=copy.deepcopy(pack);missing['slots']['location']['candidates']=[]
                self.assertEqual(semantics.public_bundles(data,missing)['candidates'],[])

    def test_provenance_does_not_enter_runtime_candidate_fields(self):
        ref=self.extension['maintenance_ref']
        record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance'/(ref['record_id']+'.json')).read_text())
        self.assertEqual(ref['sha256'],semantics.digest(record))
        raw=copy.deepcopy(self.extension);raw.pop('maintenance_ref')
        self.assertEqual(record['authored_source_sha256'],semantics.digest(raw))
        for slot,rows in self.extension['slots'].items():
            for row in rows:
                self.assertFalse({'source_ids','historical_scope','claim_limits','source_role','candidate_status'}&set(row))
                self.assertNotIn('identity',row['affected_dimensions'])

if __name__=='__main__':unittest.main()
