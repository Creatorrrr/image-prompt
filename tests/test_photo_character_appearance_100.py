"""Character research must preserve reusable meaning and owner boundaries."""
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path
from tests import photo_prompt_fixtures as fixtures

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
ASSETS=SKILL/'assets'
RUN=ROOT/'docs/research-evidence/photo-prompt/character-appearance-100-20261004'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
import photo_contracts as contracts

class CharacterAppearance100Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
        cls.profiles={p['id']:p for p in cls.registry['profiles']}
        cls.new_ids=[p['id'] for p in json.loads((ASSETS/'photo_prompt_visual_obligations_character_appearance.json').read_text())['profiles']]
        cls.thin=dict(cls.registry,profiles=[cls.profiles[p] for p in cls.new_ids])
        cls.thin_index=pg.build_visual_profile_index_payload(cls.thin)
        cls.receipt=json.loads((RUN/'INTEGRATION-MAINTENANCE.json').read_text())
        cls.cases=json.loads((RUN/'CHARACTER-CASEBOOK.json').read_text())['cases']

    def hard(self,text,source='user_requirement',polarity='required'):
        result=pg.resolve_visual_profile_hits(self.thin,[{'text':text,'source':source,'polarity':polarity}],
            visual_profile_index=self.thin_index,adult_context=False)
        return {h['profile_id'] for h in result['hits'] if h['hard_eligible']}

    def test_complete_multilingual_relations_and_every_component_removal(self):
        for pid in self.new_ids:
            p=self.profiles[pid];groups=p['semantics']['component_semantics']['groups']
            for language in range(3):
                phrases=[g['any_terms'][language] for g in groups]
                with self.subTest(profile=pid,language=language):
                    self.assertEqual(pg.candidate_pack_visual_component_match(p,'; '.join(phrases)),'component_semantics')
                for missing in range(len(groups)):
                    with self.subTest(profile=pid,language=language,missing=missing):
                        self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(t for n,t in enumerate(phrases) if n!=missing)))

    def test_each_research_case_links_to_real_runtime_owners(self):
        self.assertEqual(len(self.cases),100)
        self.assertEqual(len({c['id'] for c in self.cases}),100)
        self.assertEqual(len({(c['group'],c['name_en']) for c in self.cases}),100)
        groups={g:sum(c['group']==g for c in self.cases) for g in {c['group'] for c in self.cases}}
        self.assertEqual(set(groups.values()),{20})
        used=set()
        for c in self.cases:
            with self.subTest(case=c['id']):
                self.assertEqual(c['evidence_state'],'PUBLISHER_PIXELS_OBSERVED')
                self.assertEqual(len(c['decomposed_elements']),5)
                self.assertTrue(c['observable_relations_ko'])
                self.assertTrue(c['unobservable_and_confusions_ko'])
                self.assertTrue(c['runtime_links'])
                self.assertEqual(len(c['artwork_sha256']),64)
                self.assertFalse(c['named_character_routing'])
                for link in c['runtime_links']:
                    self.assertIn(link['profile_id'],self.profiles)
                    used.add(link['profile_id'])
        self.assertTrue(set(self.new_ids)<=used)

    def test_all_previous_profiles_keep_meaning_activation_effects_and_native_gates(self):
        before=json.loads((RUN/'BASELINE-REGISTRY.json').read_text())['profiles']
        self.assertEqual(len(before),1622)
        original_cello_activation=self._authenticated_v34_cello_activation()
        for p in before:
            q=self.profiles[p['id']]
            with self.subTest(profile=p['id']):
                for field in ('activation','render_gates','required_evidence_fields','composition_instruction'):
                    actual=(original_cello_activation if field=='activation'
                            and p['id']=='cello_endpin_seated_bowed'
                            and original_cello_activation is not None else q[field])
                    self.assertEqual(p[field],actual)
                for field in ('definition','visual_components','contrast_examples','claim_limits'):
                    self.assertEqual(p['semantics'].get(field),q['semantics'].get(field))
                for field in ('affected_dimensions','affected_properties','core_assertion_discovery'):
                    self.assertEqual(p.get('concept_candidate',{}).get(field),q.get('concept_candidate',{}).get(field))
                a=p['semantics']['component_semantics'];b=q['semantics']['component_semantics']
                self.assertEqual(a['minimum_component_groups'],b['minimum_component_groups'])
                self.assertEqual(a['required_group_ids'],b['required_group_ids'])
                self.assertEqual([g['id'] for g in a['groups']],[g['id'] for g in b['groups']])
                for ga,gb in zip(a['groups'],b['groups']):
                    self.assertTrue(set(ga['any_terms'])<=set(gb['any_terms']))
                for field,req in p['evidence_requirements'].items():
                    new=q['evidence_requirements'][field]
                    self.assertEqual(req['min_content_words'],new['min_content_words'])
                    self.assertTrue(set(req['must_mention_any'])<=set(new['must_mention_any']))

    def _authenticated_v34_cello_activation(self):
        if not fixtures._v34_scope_context(ROOT):
            return None
        support=fixtures._v34_scope_support(ROOT)
        name='skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json'
        # The complete live registry and immutable transition proof must match
        # before a historical comparison can read the original activation.
        original=json.loads(support.previous_payload(ROOT,name,(ROOT/name).read_bytes()))
        return next(p['activation'] for p in original['profiles']
                    if p['id']=='cello_endpin_seated_bowed')

    def test_current_cello_activation_matches_authenticated_v34_scope_guard(self):
        original=self._authenticated_v34_cello_activation()
        current=self.profiles['cello_endpin_seated_bowed']['activation']
        if original is None:
            before=json.loads((RUN/'BASELINE-REGISTRY.json').read_text())['profiles']
            self.assertEqual(next(p['activation'] for p in before
                                  if p['id']=='cello_endpin_seated_bowed'),current)
            return
        support=fixtures._v34_scope_support(ROOT)
        proof,_=support.transition(ROOT)
        name='skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json'
        changes=proof['source_leaf_delta'][name]
        self.assertEqual([r['pointer'] for r in changes],[
            '/profiles/114/activation/exclude_if_any_terms',
            '/profiles/114/activation/hard_activation'])
        expected=copy.deepcopy(original)
        for change in changes:
            self.assertEqual('add',change['operation'])
            key=change['pointer'].rsplit('/',1)[1]
            self.assertNotIn(key,expected)
            expected[key]=change['after']
        self.assertEqual(expected,current)
        self.assertEqual('photo-visual-hard-activation/v1',current['hard_activation']['contract_version'])
        self.assertEqual(['cello_instrument','active_bowing','seated_support'],
            [group['id'] for group in current['hard_activation']['required_any_groups']])

    def test_existing_alternatives_remain_full_relations(self):
        for row in self.receipt['existing_owner_enrichments']:
            p=self.profiles[row['profile_id']]
            for language in ('en','ko'):
                parts=row[f'component_alternatives_{language}']
                with self.subTest(profile=p['id'],language=language):
                    self.assertEqual(pg.candidate_pack_visual_component_match(p,'; '.join(parts)),'component_semantics')

    def test_names_neither_create_hard_relations_nor_enter_positive_prototypes(self):
        texts=[pg.visual_profile_semantic_text(self.profiles[pid]).casefold() for pid in self.new_ids]
        exact={t.casefold() for pid in self.new_ids for t in self.profiles[pid]['activation']['exact_terms']}
        for c in self.cases:
            with self.subTest(case=c['id']):
                self.assertFalse(self.hard(c['name_en']))
                self.assertFalse(self.hard(c['name_ko']))
                self.assertNotIn(c['name_en'].casefold(),exact)
                self.assertNotIn(c['name_ko'].casefold(),exact)
                # Multiword names have no ambiguous ordinary-word interpretation.
                if ' ' in c['name_en']:
                    self.assertFalse(any(c['name_en'].casefold() in t for t in texts))
                self.assertFalse(any(c['name_ko'].casefold() in t for t in texts))

    def test_exact_relations_require_declared_carrier_and_requester_selection(self):
        context='hair glasses cap garment skin mouth mask cover a nonhuman creature machine '
        for pid in self.new_ids:
            term=self.profiles[pid]['activation']['exact_terms'][0]
            with self.subTest(profile=pid):
                self.assertIn(pid,self.hard(context+term))
                self.assertNotIn(pid,self.hard(context+term,source='authorial_core_interpretation',polarity='advisory'))
                self.assertNotIn(pid,self.hard(context+term,polarity='excluded'))
                self.assertNotIn(pid,self.hard(context+'no '+term))
        self.assertNotIn('ca_rigid_limb_joint',self.hard('a human portrait with rigid limb segments with exposed joint interfaces'))
        self.assertNotIn('ca_coiled_head_elements',self.hard('a human portrait with paired coiled horn-like head contours'))

    def test_embedding_and_semantic_paraphrases_are_advisory(self):
        p=self.profiles['ca_forked_tail'];thin=dict(self.registry,profiles=[p])
        index=pg.build_visual_profile_index_payload(thin,vectors={p['id']:[1.0,0.0]},dimensions=2)
        text=p['semantics']['paraphrase_examples'][-1]
        result=pg.resolve_visual_profile_hits(thin,[{'text':text,'source':'authorial_core_interpretation','polarity':'advisory'}],
            visual_profile_index=index,query_vector=[1.0,0.0],adult_context=False)
        hit=next(h for h in result['hits'] if h['profile_id']==p['id'])
        self.assertEqual(hit['match_basis'],'embedding')
        self.assertFalse(hit['hard_eligible'])
        self.assertTrue(hit['optional_eligible'])

    def test_neighbor_carriers_and_shapes_do_not_supply_the_selected_relation(self):
        cases=[
            ('ca_rigid_limb_joint','a rigid armor section covers the selected hand surface; that hand armor continues to its own wrist section'),
            ('ca_hanging_hair_braid','a decorative garment cord shows repeated crossing strands; a separate tassel continues from the end of that same cord'),
            ('ca_braided_decorative_cord','one selected hanging hair section shows repeated strand crossings; those crossings form a continuous braid along that hanging hair length'),
            ('ca_cap_projections','two horn-like elements curl around their own centers beside the selected nonhuman head; each curl retains nested curved contours with intervening gaps'),
            ('ca_body_fur_ruff','soft fiber tips form a distinct strip along the selected garment edge; the fiber strip remains separate from the adjacent main cloth panel'),
            ('ca_garment_pile_trim','the declared creature neck fur spreads outward around the neck region; the ruff tips remain continuous with the body fur surface'),
            ('ca_facial_color_mask','one cloth band spans both eye regions; the band leaves the selected lower face outside its coverage'),
            ('ca_drawn_cover_face','one iris carries one selected color over its full visible region; the other iris carries a different selected color over its full visible region'),
            ('ca_rectangular_tooth_row','multiple tooth crowns have pointed triangular silhouettes; the row belongs to the visible mouth'),
            ('ca_animal_head_mask','a separate mask sits beside the temple or upper side of the head; the wearer eye regions remain outside that mask coverage'),
            ('ca_lower_face_wrap','one cloth band spans both eye regions; the band leaves the selected lower face outside its coverage'),
            ('ca_garment_color_panels','the left and right hair regions carry different stated colors; a spatial division rather than lighting separates the regions'),
            ('ca_closed_body_rings','a separate bracelet has a closed yellow ring; the bracelet is worn around a leg'),
            ('ca_forearm_blade','a hand grips the sword handle; the separate blade extends away from that handle'),
            ('ca_forked_tail','two separately rooted tails hang behind the body; each has only one terminal tip'),
            ('ca_polygon_shell','two straps suspend a backpack from the shoulders; the backpack is separate from the animal body'),
        ]
        for pid,text in cases:
            with self.subTest(profile=pid):self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles[pid],text))

    def test_effects_obey_the_actual_carrier_and_parent_locks(self):
        for pid,dim,parent in [
            ('ca_compact_bob','appearance','hair.style'),
            ('ca_garment_color_panels','appearance','wardrobe.color'),
            ('ca_surface_line_motif','appearance','body.skin_region'),
            ('ca_rigid_limb_joint','body_geometry','body.limbs'),
            ('ca_membrane_wings','body_geometry','body.appendages'),
            ('ca_rectangular_tooth_row','appearance','face.dental'),
        ]:
            candidate=self.profiles[pid]['concept_candidate']
            lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':dim,'target':'main_subject','property':parent}]}
            with self.subTest(profile=pid):
                self.assertFalse(contracts.property_effects_allowed(lock,candidate['affected_dimensions'],candidate['affected_properties']))
                disguised=[dict(e,dimension='material') for e in candidate['affected_properties']]
                self.assertFalse(contracts.property_effects_allowed(lock,['material'],disguised))

    def test_unseen_or_separate_owners_do_not_get_reconstructed_from_biography(self):
        by_id={c['id']:c for c in self.cases}
        self.assertNotIn('ca_rigid_limb_joint',by_id['C058']['new_profile_ids'])
        self.assertNotIn('sca_f05',by_id['C017']['existing_profile_ids'])
        self.assertNotIn('sca_g08',by_id['C020']['existing_profile_ids'])
        self.assertNotIn('ca_bushy_tail',by_id['C031']['new_profile_ids'])
        self.assertNotIn('sca_f14',by_id['C046']['existing_profile_ids'])
        self.assertNotIn('costume_ccx_cc35_01',by_id['C056']['existing_profile_ids'])
        self.assertNotIn('sca_h19',by_id['C100']['existing_profile_ids'])
        self.assertNotIn('ca_fan_ribs',self.new_ids)

    def test_new_relations_keep_native_all_of_observation_gates(self):
        for pid in self.new_ids:
            p=self.profiles[pid]
            with self.subTest(profile=pid):
                self.assertEqual(len(p['render_gates']),len(p['required_evidence_fields']))
                for gate in p['render_gates']:
                    self.assertEqual(gate['review_scale'],'native')
                    self.assertIn('partial evidence fails',gate['description'])
                    self.assertIn('hidden components are unobservable',gate['description'])
                self.assertEqual(p['semantics']['component_semantics']['minimum_component_groups'],2)
                self.assertEqual(len(p['semantics']['component_semantics']['required_group_ids']),2)

    def test_existing_dictionary_hash_and_generated_indexes_are_valid(self):
        data=pg.load_runtime_data()
        # A later additive domain may legitimately change the full dictionary
        # hash and profile count. Validate the current binding and preserve
        # every original identity instead of pinning unrelated future data.
        pg.validate_semantic_index_metadata(data[pg.SEMANTIC_INDEX_DATA_KEY],data)
        current_ids={p['id'] for p in data[pg.VISUAL_OBLIGATIONS_DATA_KEY]['profiles']}
        before=json.loads((RUN/'BASELINE-REGISTRY.json').read_text())['profiles']
        self.assertTrue({p['id'] for p in before}<=current_ids)
        self.assertTrue(set(self.new_ids)<=current_ids)
        self.assertTrue(set(self.new_ids)<=set(data[pg.VISUAL_PROFILE_INDEX_DATA_KEY]['entries']))

if __name__=='__main__':unittest.main()
