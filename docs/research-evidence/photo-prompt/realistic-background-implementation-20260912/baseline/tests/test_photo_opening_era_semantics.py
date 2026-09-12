import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as semantics

class OpeningEraTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = json.loads((SKILL / 'assets/photo_prompt_opening_era_extension.json').read_text())
        raw = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.registry = {**raw, 'profiles': [p for p in raw['profiles'] if p['id'].startswith('opening_')]}
        cls.index = pg.build_visual_profile_index_payload(cls.registry)
        cls.tags = pg.load_json(SKILL / 'assets/photo_prompt_tags.json')
    def hits(self, text):
        r = pg.resolve_visual_profile_hits(self.registry, [{'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}], visual_profile_index=self.index, adult_context=True)
        return {h['profile_id'] for h in r['hits'] if h.get('match_basis') == 'exact' and h.get('hard_eligible') is True}
    def test_complete_relations_and_partial_boundaries(self):
        self.assertEqual(len(self.registry['profiles']),16)
        for p in self.registry['profiles']:
            with self.subTest(profile=p['id']):
                self.assertEqual(len(p['render_gates']),4)
                self.assertEqual(self.hits(p['activation']['exact_terms'][0]), {p['id']})
                parts=p['activation']['exact_terms'][0].split('; ')
                for n in (1,2,3):
                    self.assertNotIn(p['id'],self.hits('; '.join(parts[:n])))
    def test_broad_labels_do_not_establish_relations(self):
        for term in ['개화기','대한제국','경성','양산','양산시','대량 양산','정관헌','석조전','빈티지','retro','1920s','한복','커피','전화기']:
            with self.subTest(term=term): self.assertEqual(self.hits(term),set())
    def test_candidates_available_in_merged_public_data(self):
        self.assertEqual(len(self.extension['visual_semantics']),16)
        rows={r['id']:(slot,r) for slot,rs in self.extension['slots'].items() for r in rs}
        merged={r['id']:(slot,r) for slot,rs in self.tags['slots'].items() for r in rs}
        self.assertEqual(len(rows),64)
        for key,(slot,row) in rows.items():
            self.assertIn(key,merged)
            self.assertEqual(merged[key][0],slot)
            self.assertEqual(merged[key][1]['en'],row['en'])
        for bundle in self.extension['visual_semantics']:
            self.assertEqual(len(bundle['candidate_ids']),4)
            self.assertTrue(set(bundle['candidate_ids']) <= set(rows))
            self.assertEqual(bundle['activation_mode'],'component_complete_exact_only')

    def test_optional_bundle_scope_and_missing_member_fail_closed(self):
        ids={b['id'] for b in self.extension['visual_semantics']}
        bundles=[b for b in self.tags['candidate_bundles'] if b['id'] in ids]
        self.assertEqual(len(bundles),16)
        for b in bundles:
            with self.subTest(bundle=b['id']):
                self.assertEqual(b['profile_activation'],'independent_request_evidence_only')
                dims={d for m in b['member_candidates'] for d in m['affected_dimensions']}
                slots={}
                for m in b['member_candidates']:
                    slots.setdefault(m['slot'],{'candidates':[]})['candidates'].append({'id':m['id'],'applicability':{'status':'eligible'}})
                pack={'slots':slots,'authorial_core':{'intent_lock':{'open_dimensions':list(dims)}}}
                data={**self.tags,'candidate_bundles':[b]}
                exposed=semantics.public_bundles(data,pack)['candidates']
                self.assertEqual(len(exposed),1)
                self.assertEqual(exposed[0]['source_contract_sha256'],semantics.digest(b))
                closed=copy.deepcopy(pack);closed['authorial_core']['intent_lock']['open_dimensions']=[]
                self.assertEqual(semantics.public_bundles(data,closed)['candidates'],[])
                missing=copy.deepcopy(pack);next(iter(missing['slots'].values()))['candidates'].pop()
                self.assertEqual(semantics.public_bundles(data,missing)['candidates'],[])
    def test_maintenance_hash_and_index_coverage(self):
        ref=self.extension['maintenance_ref']
        p=ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance' / (ref['record_id']+'.json')
        record=json.loads(p.read_text())
        self.assertEqual(ref['sha256'],semantics.digest(record))
        source=copy.deepcopy(self.extension);source.pop('maintenance_ref')
        self.assertEqual(record['authored_source_sha256'],semantics.digest(source))
        idx=pg.load_semantic_index_payload(SKILL/'assets/photo_prompt_semantic_index.json')
        pg.validate_semantic_index_metadata(idx,self.tags)
        expected={f"slot:{slot}:{r['id']}" for slot,rows in self.extension['slots'].items() for r in rows}
        self.assertTrue(expected <= set(idx['entries']))

    def test_embedding_paraphrase_hits_remain_optional(self):
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

if __name__ == '__main__': unittest.main()
