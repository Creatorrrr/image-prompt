import copy
import unittest
from tests.test_photo_candidate_corpus import fixture, A, X
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_role_proposals as roles
import photo_slot_semantics as semantics
import photo_native_pack


class SemanticRoleTests(unittest.TestCase):
    def hair_spec(self):
        row = slot('hair_color',['appearance'],property_prefixes=['hair.color'],evidence_terms=['hair color'])
        row['owners']=['actor'];return row

    def test_shared_appearance_dimension_does_not_make_cuff_hair_color(self):
        record={'effects':{'dimensions':['appearance'],'properties':[{'dimension':'appearance','target':'main_subject','property':'wardrobe.cuffs.attachment'}]}}
        fit=semantics.fit(self.hair_spec(),record,'A white cuff joins the garment sleeve')
        self.assertEqual(fit['status'],'incompatible');self.assertEqual(fit['matched_properties'],[])

    def test_explicit_hair_owner_and_color_property_can_fit_without_a_tag(self):
        record={'effects':{'dimensions':['appearance'],'properties':[{'dimension':'appearance','target':'main_subject','property':'hair.color'}]}}
        fit=semantics.fit(self.hair_spec(),record,'Hair color bounded to a red fringe')
        self.assertEqual(fit['status'],'eligible')
        other=copy.deepcopy(record);other['effects']['properties'][0]['target']='background'
        self.assertEqual(semantics.fit(self.hair_spec(),other,'Hair color bounded to a red fringe')['status'],'incompatible')

    def test_meaning_word_alone_and_wildcard_effects_need_review(self):
        for properties in ([],[{'dimension':'appearance','target':'main_subject','property':'*'}]):
            record={'effects':{'dimensions':['appearance'],'properties':properties}}
            self.assertEqual(semantics.fit(self.hair_spec(),record,'hair color')['status'],'review_required')

    def test_same_lighting_dimension_does_not_approve_pattern_as_direction(self):
        spec=slot('light_direction',['lighting'],property_prefixes=['lighting.direction'],evidence_terms=['side light'])
        record={'effects':{'dimensions':['lighting'],'properties':[{'dimension':'lighting','target':'main_subject','property':'lighting.pattern'}]}}
        self.assertEqual(semantics.fit(spec,record,'dappled light through leaves')['status'],'incompatible')

    def test_intrinsic_conditions_and_effects_survive_other_role_proposal(self):
        data=fixture();data['candidates'][A]['conditions']={'for_any':['human']}
        before=c.digest(data);proposal=roles.propose(data,'garment_detail',A,[X])
        self.assertIsNone(proposal['source_binding_id'])
        self.assertEqual(proposal['conditions'],{'for_any':['human']})
        self.assertEqual(proposal['effects'],data['candidates'][A]['effects'])
        self.assertEqual(c.digest(data),before)

    def test_declared_role_condition_cannot_be_bypassed_by_new_request_proposal(self):
        data=fixture();proposal=roles.propose(data,'wardrobe_style',A,[])
        self.assertEqual(proposal['applicability_status'],'incompatible')
        self.assertEqual(proposal['semantic_fit']['reason'],'declared_role_conditions_not_satisfied')

    def test_intrinsic_override_and_duplicate_effect_owner_are_rejected(self):
        for field,value in [('for_any',['object']),('effects',{'dimensions':['style'],'properties':[]})]:
            data=fixture()
            if field=='effects':data['slot_bindings'][X][field]=value
            else:data['slot_bindings'][X]['conditions'][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):c.validate(data)

    def test_duplicate_candidate_slot_with_different_adoption_role_is_rejected(self):
        data=fixture();data['slot_bindings']['bind_'+'b'*32]={**copy.deepcopy(data['slot_bindings'][X]),'id':'bind_'+'b'*32,'role':'other'}
        self.assertRaises(ValueError,c.validate,data)

    def test_old_native_corpus_and_v8_pack_are_rejected(self):
        data=fixture();data['schema']='photo-candidate-corpus/v1'
        self.assertRaises(ValueError,c.validate,data)
        self.assertRaises(ValueError,photo_native_pack.role_cards,{'contract_version':'photo-candidate-pack/v8'})

    def test_context_role_is_distinct_from_direct_visual_role(self):
        spec=slot('declared_background',['identity'],semantic_role='contextual',property_prefixes=['identity.background'],evidence_terms=['from'])
        record={'effects':{'dimensions':['identity'],'properties':[]}}
        fit=semantics.fit(spec,record,'declared from India')
        self.assertEqual(fit['semantic_role'],'contextual');self.assertEqual(fit['status'],'review_required')
