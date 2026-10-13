"""Complete existing-relation migration and native scope regressions."""
import copy
import gzip
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import photo_global_index as index
import photo_slot_queries as queries
from tests.test_photo_global_retrieval import GlobalDiscoveryTests


class TaxonomyMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GlobalDiscoveryTests.setUpClass()
        cls.source=c.load(ROOT/'skills/photo-prompt-image-generator/assets')
        cls.evidence=ROOT/'docs/research-evidence/photo-prompt/slot-taxonomy-revision-20261013'
        cls.before=c.decode(gzip.decompress((cls.evidence/'CORPUS-BEFORE.json.gz').read_bytes()))
        cls.target=json.loads((cls.evidence/'TARGET-CATALOG.json').read_text())
        cls.ledger=list(map(json.loads,(cls.evidence/'BINDING-MIGRATION.jsonl').read_text().splitlines()))

    def test_all_canonical_ids_and_positive_texts_survive_without_cloning(self):
        self.assertEqual(set(self.source['candidates']),set(self.before['candidates']))
        self.assertEqual(len(self.source['candidates']),18250)
        for cid,record in self.source['candidates'].items():
            self.assertEqual(record['record_kind'],self.before['candidates'][cid]['record_kind'])
            self.assertEqual(index.text(record),index.text(self.before['candidates'][cid]),cid)

    def test_every_old_relation_has_one_traceable_primary_and_preserved_policy(self):
        self.assertEqual({r['old_binding_id'] for r in self.ledger},set(self.before['slot_bindings']))
        for row in self.ledger:
            before=self.before['slot_bindings'][row['old_binding_id']]
            for bid in row['new_binding_ids']:
                current=self.source['slot_bindings'][bid]
                self.assertEqual(current['candidate_id'],before['candidate_id'])
                self.assertEqual(current['conditions']['subject_applicability'],before['conditions']['subject_applicability'])
                self.assertEqual(current['weight'],before['weight'])

    def test_catalog_has_explicit_flat_roles_without_retired_aliases(self):
        self.assertEqual(set(self.source['slot_catalog']),set(self.target))
        self.assertEqual(len(self.target),136)
        for role,spec in self.source['slot_catalog'].items():
            self.assertTrue(spec['dimensions'],role)
            self.assertTrue(spec['description_ko'],role)
            self.assertNotEqual(spec['description'],role.replace('_',' '))
            self.assertTrue(set(spec['property_prefixes'])>=set(self.target[role]['property_prefixes']))
        core,controls=GlobalDiscoveryTests.core,GlobalDiscoveryTests.controls
        retired=set(self.before['slot_catalog'])-set(self.target)
        for role in retired:
            with self.assertRaises(ValueError):queries.inputs(core,controls,self.source['slot_catalog'],role)

    def test_intrinsic_conditions_survive_the_role_move(self):
        for cid,record in self.before['candidates'].items():
            for key in c.INTRINSIC_CONDITION_FIELDS & set(record['content']):
                original=record['content'][key];current=self.source['candidates'][cid]['conditions'][key]
                self.assertEqual(set(original) if isinstance(original,list) else original,
                                 set(current) if isinstance(current,list) else current,(cid,key))

    def test_shared_framing_keeps_objects_eligible_and_human_body_guarded(self):
        import prompt_generator as g
        spec=self.source['slot_catalog']['subject_framing']
        self.assertIsNone(g.slot_block_reason(self.source,'subject_framing',{'subject_category':'object','domains':['product']}))
        self.assertIsNone(g.entry_block_reason({'tags':['object']},'subject_framing',
            {'adult_allowed':False,'intent_constraints':{'no_people':True}},catalog=self.source['slot_catalog']))
        bid='bind_0c8db7bd03c15f79b68d2d844b3f2f05'
        binding=self.source['slot_bindings'][bid]
        self.assertEqual(binding['slot_id'],'subject_framing')
        from photo_global_retrieval import guard_policy
        self.assertFalse(guard_policy(binding['conditions']['subject_applicability'],{'subject_category':'object','domains':['product']}))

    def test_feathers_and_declared_fantasy_keep_their_actual_meaning(self):
        roles=lambda cid:{b['slot_id'] for b in self.source['slot_bindings'].values() if b['candidate_id']==cid}
        feather='cand_8baa17bfe3615ef688c36a738303e535'
        self.assertEqual(roles(feather),{'species_marker','texture'})
        fantasy='cand_d0ea20c766a9599eaa25c91f363105fc'
        self.assertEqual(roles(fantasy),{'genre'})

    def test_recorded_image_softness_does_not_invent_optical_or_air_carriers(self):
        for short in ['00452495','1652909e','98c31436','9e6e9ad9','dd1a8d43']:
            cid=next(cid for cid in self.source['candidates'] if cid[5:13]==short)
            effects=self.source['candidates'][cid]['effects']
            self.assertNotIn('atmosphere',effects['dimensions'])
            self.assertFalse(any(p['target'] in {'optical_path','scene_air'} for p in effects['properties']))
            self.assertIn({'dimension':'style','property':'image.detail','target':'image_plane'},effects['properties'])

    @classmethod
    def tearDownClass(cls):
        del cls.source,cls.before
