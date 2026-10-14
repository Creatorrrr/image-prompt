"""Isolated source-local guard contracts. Passing fixtures do not approve a CID."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from tests.test_photo_semantic_evidence import A,source,fact,seal,core,assertion,owner_map
from tests.test_photo_native_compound_evidence import B,dependencies
from tests.test_photo_native_owner_selection import sign_core
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_semantic_evidence as e
import photo_search_layout as layout
import photo_shared_views as views
import prompt_generator as g
import audit_composed_prompt as audit


def ep(target,cid=A):return {'kind':'source_target','candidate_id':cid,'target':target}
def block(*rules):return {'schema':e.SOURCE_TARGET_GUARD_SCHEMA,'rules':list(rules)}
def relation(fid,left,right,kind='part_of'):
    return dict(id=fid,kind='owner_relation',relation=kind,left=left,right=right)
def value(fid,owner,dim,prop,val):
    return dict(id=fid,kind='frozen_value',owner=owner,dimension=dim,property=prop,value={'type':prop+'/v1','value':val})
def selected_map(*targets):
    return {'schema':e.SELECTOR_OWNER_SCHEMA,'bindings':[dict(target=t,origin='existing',introduced_by=None,
        selector={'kind':'selected_existing_owner'}) for t in targets]}


def hands_source(cid=A):
    rows=[fact(t+'_kind','subject',t,'entity.kind','prerequisite',kind,[]) for t,kind in
          [('hand_a','hand'),('hand_b','hand'),('mug','mug')]]
    rows.append(fact('holding','pose','hand_a','body.pose','effect','cupped',[],operation='set_value',receivers=['hand_b','mug']))
    data=source('The existing mug is cupped by existing hand A and hand B, both parts of the same existing holder.',
        rows,{'pose':slot('pose',['pose'],property_prefixes=['body.pose'])},
        {'base':selected_map('hand_a','hand_b','mug','holder')})
    rec=data['candidates'].pop(A);rec['id']=cid;data['candidates'][cid]=rec
    rec['conditions']={'native_guards':block(relation('a_holder',ep('hand_a',cid),ep('holder',cid)),
        relation('b_holder',ep('hand_b',cid),ep('holder',cid)),relation('two_hands',ep('hand_a',cid),ep('hand_b',cid),'disjoint'))}
    return seal(data,{'pose':['holding']},cid=cid)


def hands_core():
    owners=['main','secondary','background','a2','b2','mug2','a3','b3','mug3']
    values=[('subject',o,'entity.presence','present') for o in owners]
    values += [('subject',o,'entity.kind',kind) for o,kind in [('a2','hand'),('b2','hand'),('mug2','mug'),('a3','hand'),('b3','hand'),('mug3','mug')]]
    edges=[('part_of','a2','secondary'),('part_of','b2','secondary'),('disjoint','a2','b2'),
           ('part_of','a3','background'),('part_of','b3','background'),('disjoint','a3','b3'),
           ('disjoint','main','secondary'),('disjoint','main','background'),('disjoint','secondary','background')]
    return sign_core(core(owners,values,edges,role_bindings={}))


def choices(data,frozen,bindings=None,cid=A,rid='base'):
    p=data['candidates'][cid]['content']['role_evidence']
    bindings=bindings or dict(hand_a='a2',hand_b='b2',mug='mug2',holder='secondary')
    return {'schema':e.OWNER_SELECTION_SCHEMA,'core_sha256':frozen['canonical_sha256'],
        'owner_graph_sha256':c.digest(e.frozen_witnesses(frozen)['graph']),
        'entries':[dict(candidate_id=cid,realization_id=rid,meaning_sha256=p['meaning_sha256'],qualification_sha256=c.digest(p),
            bindings=[dict(target=t,owner_id=o) for t,o in bindings.items()])]}


class SourceTargetGuardTests(unittest.TestCase):
    def entries(self,data,**kwargs):
        c.validate(data)
        return [c.entry(data,A,realization_id=kwargs.pop('rid','base'),**kwargs),
            c.entry({**data,'candidates':{**data['candidates'],A:layout.guard_record(data['candidates'][A],data)}},A,realization_id='base',**kwargs)]
    def eligible(self,data,frozen,entry,**kwargs):
        return g.core_entry_eligible(data,frozen,{'subject_category':'object','intent_constraints':{'domains':[]}}, {'subject':{}},'',entry,**kwargs)
    def test_secondary_and_background_full_compact_guard_only_holder_and_permission(self):
        data=hands_source();frozen=hands_core();p=data['candidates'][A]['content']['role_evidence']
        self.assertNotIn('holder',{f['target'] for f in p['facts']})
        expected=[]
        for mapping in [None,dict(hand_a='a3',hand_b='b3',mug='mug3',holder='background')]:
            for entry in self.entries(data,owner_selections=choices(data,frozen,mapping)):
                result=e.admission(entry,frozen);self.assertTrue(result['allowed'],result)
                self.assertEqual(len(result['native_guards']['rules']),3)
                self.assertTrue(self.eligible(data,frozen,entry))
                self.assertEqual({p['target'] for p in e.permission_scope(entry,frozen)[1]},set((mapping or dict(hand_a='a2',hand_b='b2',mug='mug2')).values())-{'background'})
                expected.append(result)
        self.assertEqual(expected[0],expected[1]);self.assertEqual(expected[2],expected[3])
    def test_wrong_unknown_reversed_equivalent_and_missing_disjoint_relations_deny(self):
        data=hands_source()
        for defect in ['wrong_holder','same_hand','no_part','reverse','no_disjoint','equivalent_not_part']:
            frozen=hands_core();bindings=dict(hand_a='a2',hand_b='b2',mug='mug2',holder='secondary')
            if defect=='wrong_holder':bindings['holder']='background'
            elif defect=='same_hand':bindings['hand_b']='a2'
            else:
                rows=frozen['semantic_assertions']
                if defect=='no_disjoint':rows[:]=[x for x in rows if not (x['axes'].get('kind')=='disjoint' and x['axes'].get('left')=='a2')]
                else:
                    row=next(x for x in rows if x['axes'].get('kind')=='part_of' and x['axes'].get('left')=='a2')
                    if defect=='no_part':rows.remove(row)
                    elif defect=='reverse':
                        row['axes']['left'],row['axes']['right']=row['axes']['right'],row['axes']['left']
                        frozen['semantic_assertions']=[x for x in rows if x['axes'].get('kind')!='disjoint']
                    else:
                        # Isolated alias-versus-part control, with contradictory
                        # disjoint scope removed rather than inventing a witness.
                        rows.remove(row);bindings['hand_a']='secondary'
                        frozen['semantic_assertions']=[x for x in rows if x['axes'].get('property')!='entity.kind']
                        bindings['hand_b']='b2'
                        # Missing P is also a valid independent rejection; the
                        # dedicated relation-only control below isolates self.
                sign_core(frozen)
            with self.subTest(defect=defect):
                for entry in self.entries(data,owner_selections=choices(data,frozen,bindings)):
                    self.assertFalse(e.admission(entry,frozen)['allowed'])
                    self.assertRaises(ValueError,e.permission_scope,entry,frozen)
                    self.assertFalse(self.eligible(data,frozen,entry))
    def test_missing_mapping_search_only_but_fixed_false_guard_still_denies(self):
        data=hands_source();frozen=hands_core()
        for entry in self.entries(data):
            self.assertFalse(e.admission(entry,frozen)['allowed'])
            self.assertTrue(e.admission(entry,frozen,allow_unselected=True)['search_only'])
            self.assertTrue(self.eligible(data,frozen,entry,allow_owner_selection_pending=True))
            self.assertRaises(ValueError,e.permission_scope,entry,frozen)
        p=data['candidates'][A]['content']['role_evidence'];p['owner_maps']['base']['bindings'][-1]['selector']={'kind':'core_role','role':'main_subject'}
        frozen['semantic_assertions'].append(assertion('main_role','role',role='main_subject',owner='main'))
        data['candidates'][A]['conditions']['native_guards']['rules'].append(value('fixed_false',ep('holder'),'subject','entity.presence','absent'))
        seal(data,{'pose':['holding']});sign_core(frozen)
        for entry in self.entries(data):self.assertFalse(e.admission(entry,frozen,allow_unselected=True)['allowed'])
    def test_schema_namespace_guard_inventory_and_introduced_origin_are_exact(self):
        for defect in ['version','extra','endpoint_extra','unknown_cid','unknown_target','unused','optional_injection','introduced']:
            data=hands_source();p=data['candidates'][A]['content']['role_evidence'];b=data['candidates'][A]['conditions']['native_guards']
            if defect=='version':b['schema']='photo-native-source-guards/v9'
            elif defect=='extra':b['fallback']=True
            elif defect=='endpoint_extra':b['rules'][0]['left']['role']='primary_hands'
            elif defect=='unknown_cid':b['rules'][0]['right']['candidate_id']=B
            elif defect=='unknown_target':b['rules'][0]['left']['target']='missing'
            elif defect=='unused':p['owner_maps']['base']['bindings'].append(dict(target='unused',origin='existing',introduced_by=None,selector={'kind':'selected_existing_owner'}))
            elif defect=='optional_injection':
                data['candidates'][A]['conditions']={};p['owner_maps']['base']['bindings'][-1]['target']='holder'
            else:
                row=p['owner_maps']['base']['bindings'][-1];row.update(origin='introduced',introduced_by='creator',selector={'kind':'core_role','role':'main_subject'})
            with self.subTest(defect=defect):
                try:seal(data,{'pose':['holding']})
                except ValueError:continue
                self.assertRaises(ValueError,c.validate,data)
    def test_anonymous_and_forged_member_and_presentation_frames_fail(self):
        data=hands_source();frozen=hands_core();choice=choices(data,frozen)
        for entry in self.entries(data,owner_selections=choice):
            for defect in ['anonymous','foreign_root','presentation','mutated_binding']:
                bad=copy.deepcopy(entry);cond={'native_guards':block(value('fake',ep('holder'),'subject','entity.presence','present'))}
                if defect=='anonymous':bad['_native_extra_conditions']=[cond]
                elif defect=='foreign_root':bad['_native_guard_root']={**entry,'_realization_id':'foreign'}
                else:
                    bad['_role_conditions']=cond
                    if defect=='mutated_binding':bad['_native_presentation_guard']={'record':{'id':'bad','candidate_id':A,'conditions':cond},'sha256':'0'*64}
                with self.subTest(defect=defect):self.assertFalse(e.admission(bad,frozen)['allowed'])
    def test_receiver_lock_and_property_prerequisite_old_value_keep_distinct_modes(self):
        data=hands_source();frozen=hands_core();frozen['intent_lock']['semantic_anchors']=[{'dimension':'pose','target':'mug2','property':'body.pose'}];sign_core(frozen)
        for entry in self.entries(data,owner_selections=choices(data,frozen)):
            self.assertTrue(e.admission(entry,frozen)['allowed'])
            self.assertFalse(self.eligible(data,frozen,entry))
        frozen['intent_lock']['semantic_anchors']=[]
        # Exact same target/property frozen old and effect new are different modes.
        frozen['intent_lock']['locked_dimensions'].append('pose');frozen['intent_lock']['open_dimensions'].remove('pose')
        frozen['semantic_assertions'].append(assertion('old_pose','fact',dimension='pose',owner='a2',property='body.pose',value_type='body.pose/v1',value='open'))
        p=data['candidates'][A]['content']['role_evidence'];data['candidates'][A]['content']['en']+=' Starting from the declared open pose.'
        p['facts'].append(fact('old','pose','hand_a','body.pose','prerequisite','open',[],quote='open'))
        seal(data,{'pose':['holding']});sign_core(frozen)
        for entry in self.entries(data,owner_selections=choices(data,frozen)):
            self.assertTrue(e.admission(entry,frozen)['allowed']);self.assertFalse(self.eligible(data,frozen,entry))
    def test_frozen_entity_relation_uses_explicit_alias_only_and_v1_remains_literal(self):
        data=hands_source();frozen=hands_core();frozen['semantic_assertions'] += [
            assertion('holder_alias_owner','owner',owner='secondary_alias',owner_kind='entity'),
            assertion('holder_alias','equivalent',left='secondary_alias',right='secondary'),
            assertion('frozen_link','fact',dimension='relationship',owner='mug2',property='relationship.fixture_holder',value_type='entity.owner_id/v1',value='secondary_alias')]
        frozen['intent_lock']['locked_dimensions'].append('relationship')
        data['candidates'][A]['conditions']['native_guards']['rules'].append(dict(id='link',kind='frozen_entity_relation',left=ep('mug'),right=ep('holder'),dimension='relationship',property='relationship.fixture_holder',value_type='entity.owner_id/v1'))
        seal(data,{'pose':['holding']});sign_core(frozen)
        for entry in self.entries(data,owner_selections=choices(data,frozen)):
            self.assertTrue(e.admission(entry,frozen)['allowed'])
        for invalid in ['a2','unknown']:
            bad=copy.deepcopy(frozen);bad['semantic_assertions'][-1]['axes']['value']=invalid;sign_core(bad)
            for entry in self.entries(data,owner_selections=choices(data,bad)):self.assertFalse(e.admission(entry,bad)['allowed'])




def compound(optional=False):
    data=hands_source();child=hands_source(B);data['candidates'][B]=child['candidates'][B]
    parent=data['candidates'][A];parent['record_kind']='visual_bundle'
    parent['content']['member_candidates']=[dict(candidate_id=B,adoption='optional' if optional else 'required',requirements={},
        conditions={'native_guards':block(relation('shared_holder',ep('hand_a',B),ep('holder')))})]
    dependencies(data,A,'base',[B])
    if optional:parent['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
    return seal(data,{'pose':['holding']})


def compound_choices(data,frozen,background=False):
    result=choices(data,frozen)
    other=choices(data,frozen,dict(hand_a='a3',hand_b='b3',mug='mug3',holder='background') if background else None,cid=B)
    result['entries']+=other['entries']
    return result


class SourceGuardCompoundTests(unittest.TestCase):
    entries=SourceTargetGuardTests.entries
    eligible=SourceTargetGuardTests.eligible
    def test_member_pointer_origin_and_selected_child_namespace_full_compact_materialized(self):
        data=compound();frozen=hands_core();choice=compound_choices(data,frozen)
        for entry in self.entries(data,owner_selections=choice):
            result=e.admission(entry,frozen);self.assertTrue(result['allowed'],result)
            trace=result['dependencies'][0]['admission']['native_guards']['rules'][-1]
            self.assertEqual(trace['declaring_candidate_id'],A);self.assertEqual(trace['activation_candidate_id'],B)
            member=views.materialize_member(data,data['candidates'][A]['content']['member_candidates'][0],
                realization_id='base',owner_selections=choice,guard_root=entry)
            self.assertTrue(e.admission(member,frozen)['allowed']);self.assertTrue(self.eligible(data,frozen,member))
            self.assertEqual(r.eligible_ids(data,A,frozen,{'subject_category':'object'},{'subject':{}},owner_selections=choice),['base'])
        import photo_candidate_semantics as semantics
        with mock.patch.object(g,'frozen_core_context',return_value=({'subject_category':'object','intent_constraints':{'domains':[]}}, {'subject':{}})):
            row=semantics.native_bundle_view(data,c.entry(data,A,realization_id='base'),{'authorial_core':frozen,'creative_controls':{}},'base',owner_selections=choice)
            self.assertEqual(row['applicability']['status'],'eligible')
            self.assertEqual(row['member_candidates'][0]['id'],B)
            bad=semantics.native_bundle_view(data,c.entry(data,A,realization_id='base'),{'authorial_core':frozen,'creative_controls':{}},'base',owner_selections=compound_choices(data,frozen,True))
            self.assertEqual(bad['applicability']['status'],'ineligible')
        for entry in self.entries(data,owner_selections=compound_choices(data,frozen,True)):
            self.assertFalse(e.admission(entry,frozen)['allowed']);self.assertRaises(ValueError,e.permission_scope,entry,frozen)
        pointer=data['candidates'][A]['content']['member_candidates'][0]
        standalone=views.materialize_member(data,pointer,realization_id='base',owner_selections=choice)
        self.assertFalse(e.admission(standalone,frozen)['allowed'])
    def test_optional_child_no_implicit_guard_binding_effect_or_namespace_adoption(self):
        data=compound(True);frozen=hands_core()
        for entry in self.entries(data,owner_selections=choices(data,frozen)):
            result=e.admission(entry,frozen);self.assertTrue(result['allowed'],result);self.assertEqual(result['dependencies'],[])
        for entry in self.entries(data,owner_selections=compound_choices(data,frozen,True),dependency_selections={B:'base'}):
            self.assertFalse(e.admission(entry,frozen)['allowed'])
        # Optional child cannot be adopted by adding a common endpoint alone.
        data['candidates'][A]['conditions']['native_guards']['rules'].append(relation('cannot_adopt',ep('hand_a',B),ep('holder')))
        seal(data,{'pose':['holding']});self.assertRaises(ValueError,c.validate,data)
    def test_required_child_common_and_actual_branch_guards_conjoin_with_presentation(self):
        data=compound();rec=data['candidates'][A]
        rec['conditions']['native_guards']['rules'].append(relation('required_child',ep('hand_a',B),ep('holder')))
        seal(data,{'pose':['holding']});frozen=hands_core();choice=compound_choices(data,frozen)
        for entry in self.entries(data,owner_selections=choice):self.assertTrue(e.admission(entry,frozen)['allowed'])
        bid='bind_'+'d'*32
        data['slot_bindings'][bid]=dict(id=bid,candidate_id=B,slot_id='pose',role='optional',semantic_role='direct',weight=1,
            conditions={'subject_applicability':{},'native_guards':block(value('wrong_kind',ep('mug',B),'subject','entity.kind','stone'))})
        pointer=rec['content']['member_candidates'][0];pointer['binding_id']=bid
        seal(data,{'pose':['holding']});choice=compound_choices(data,frozen)
        for entry in self.entries(data,owner_selections=choice):self.assertFalse(e.admission(entry,frozen)['allowed'])
        # Presentation binding cannot borrow the member pointer's parent namespace.
        data['slot_bindings'][bid]['conditions']['native_guards']=block(value('parent_leak',ep('holder'),'subject','entity.presence','present'))
        seal(data,{'pose':['holding']});self.assertRaises(ValueError,c.validate,data)
    def test_final_audit_rebuilds_member_origin_and_rejects_wrong_holder(self):
        data=compound();frozen=hands_core();pack={'authorial_core':frozen}
        composed={'chosen_candidate_ids':[A],'candidate_interpretations':[dict(candidate_id=A,realization_id='base')],
            'owner_selections':compound_choices(data,frozen),'prompt_en':'The existing mug is cupped by both hands of the same holder.'}
        with mock.patch.object(g,'frozen_core_context',return_value=({'subject_category':'object','intent_constraints':{'domains':[]}}, {'subject':{}})):
            self.assertEqual(audit.audit_native_adoptions(pack,composed,data),[])
            composed['owner_selections']=compound_choices(data,frozen,True)
            self.assertTrue(audit.audit_native_adoptions(pack,composed,data))


class SourceGuardPackTransportTests(unittest.TestCase):
    def texture_guard(self):
        from tests import test_photo_native_owner_selection as fixtures
        data=fixtures.texture_source();cid=fixtures.P
        data['candidates'][cid]['conditions']={'native_guards':block(value('actual_material',ep('surface',cid),'material','surface.material','leather'))}
        seal(data,{'texture':['cracks']},cid=cid)
        return data
    def test_real_lazy_retrieval_immutable_pack_compose_and_runtime_fresh_receipt(self):
        from tests import test_photo_native_owner_selection as fixtures
        data=self.texture_guard()
        with mock.patch.object(fixtures,'texture_source',return_value=data):
            fixtures.OwnerSelectionPackTests.test_real_freeze_retrieval_public_pack_stays_immutable_and_composed_audit_resolves(self)
            fixtures.OwnerSelectionFinalAuditTests.test_real_runtime_request_reaudits_exact_public_pack_and_composed_mapping(self)
    def test_real_workflow_failure_correction_success_rebind_and_runtime_equality(self):
        from tests import test_photo_native_owner_selection as fixtures
        with mock.patch.object(fixtures,'texture_source',return_value=self.texture_guard()):
            fixtures.OwnerSelectionWorkflowTests.test_successful_audit_freezes_mapping_failed_audit_can_be_corrected_and_runtime_rechecks(self)
    def test_profile_selected_rid_v2_guards_full_compact_choice_and_final(self):
        from tests import test_photo_native_owner_selection as fixtures
        from tests import test_photo_native_v4_guards as profiles
        # This independent fixture selects a leather carrier. Reread its actual
        # positive clauses and author leather consistently, rather than retaining
        # the original helper's linen wording with a contradictory leather guard.
        def leather(value):
            if isinstance(value,str):return value.replace('linen surface','leather surface')
            if isinstance(value,list):return [leather(x) for x in value]
            if isinstance(value,dict):return {key:leather(x) for key,x in value.items()}
            return value
        data=leather(profiles.profile_source());rec=data['candidates'][A];p=rec['content']['role_evidence']
        rec['conditions']={'native_guards':block(value('profile_material',ep('surface'),'material','surface.material','leather'))}
        for mapping in p['owner_maps'].values():
            mapping['schema']=e.SELECTOR_OWNER_SCHEMA
            for row in mapping['bindings']:
                role=row.pop('core_role');row['selector']={'kind':'selected_existing_owner'} if row['target']=='surface' else {'kind':'core_role','role':role}
        seal(data,{'light_direction':[f['id'] for f in p['facts'] if f['mode']=='effect']});c.validate(data)
        frozen=fixtures.owner_core();profile_choices=profiles.NativeV4ProfileTests().choices(data,frozen)
        alone=next(row for row in profile_choices['profiles'][0]['choices'] if row['realization_id']=='alone')
        self.assertEqual(alone['owner_selection_requirements']['nodes'][0]['targets'],['surface'])
        selection=fixtures.selections(data,frozen,cid=A,rid='alone')
        phrase='Side light grazes the declared leather surface from the left.'
        for record in [rec,layout.guard_record(rec,data)]:
            entry=c.entry({**data,'candidates':{A:record}},A,realization_id='alone',owner_selections=selection)
            self.assertTrue(e.admission(entry,frozen)['allowed']);self.assertEqual(e.permission_scope(entry,frozen)[0],['lighting'])
            interpretation={'realization_id':'alone','selected_profile_contract':entry['_selected_profile_contract'],
                'selected_profile_evidence':{'side_light_phrase':phrase}}
            audit.audit_selected_native_profile(entry,interpretation,phrase)
            interpretation['selected_profile_contract']['sha256']='0'*64
            self.assertRaises(ValueError,audit.audit_selected_native_profile,entry,interpretation,phrase)
        bad=c.entry(data,A,realization_id='alone',owner_selections=fixtures.selections(data,frozen,'cloth_surface',cid=A,rid='alone'))
        self.assertFalse(e.admission(bad,frozen)['allowed'])
        audit.audit_native_profile_choices({'native_profile_choices':profile_choices,'authorial_core':frozen},
            {'chosen_candidate_ids':[A]},data,{A},{A:{'realization_id':'alone'}})


class SourceGuardBranchAndPreservationTests(unittest.TestCase):
    def test_selected_source_branch_and_presentation_each_have_exact_actual_rid(self):
        data=hands_source();rec=data['candidates'][A];p=rec['content']['role_evidence']
        rec['effects']['realizations']={'mode':'one','branches':[dict(id=rid,conditions={'native_guards':block(value('branch_kind',ep('mug'),'subject','entity.kind',kind))},
            context_terms=[],effects={'dimensions':[],'properties':[]}) for rid,kind in [('good','mug'),('bad','stone')]]}
        original=copy.deepcopy(p['facts']);p['facts']=[]
        for rid in ['good','bad']:
            for row in original:p['facts'].append({**copy.deepcopy(row),'id':row['id']+'_'+rid,'realization_id':rid})
        p['owner_maps']={rid:copy.deepcopy(p['owner_maps']['base']) for rid in ['good','bad']}
        seal(data,{'pose':['holding_good','holding_bad']});c.validate(data);frozen=hands_core()
        for view in [data,{**data,'candidates':{A:layout.guard_record(rec,data)}}]:
            for rid,allowed in [('good',True),('bad',False)]:
                entry=c.entry(view,A,realization_id=rid,owner_selections=choices(data,frozen,rid=rid))
                self.assertEqual(e.admission(entry,frozen)['allowed'],allowed)
                if allowed:self.assertEqual(e.admission(entry,frozen)['native_guards']['rules'][-1]['declaring_realization_id'],'good')
            stale=choices(data,frozen,rid='good');entry=c.entry(view,A,realization_id='bad',owner_selections=stale)
            self.assertFalse(e.admission(entry,frozen)['allowed'])
        bid='bind_'+'e'*32
        data['slot_bindings'][bid]=dict(id=bid,candidate_id=A,slot_id='pose',role='optional',semantic_role='direct',weight=1,
            conditions={'subject_applicability':{},'native_guards':block(value('presentation_kind',ep('mug'),'subject','entity.kind','stone'))})
        entry=c.entry(data,A,bid,realization_id='good',owner_selections=choices(data,frozen,rid='good'))
        self.assertFalse(e.admission(entry,frozen)['allowed']);self.assertRaises(ValueError,e.permission_scope,entry,frozen)
    def test_required_child_actual_rid_discovery_probe_and_strict_choice(self):
        data=compound();child=data['candidates'][B];p=child['content']['role_evidence']
        child['effects']['realizations']={'mode':'one','branches':[dict(id=rid,conditions={},context_terms=[],effects={'dimensions':[],'properties':[]}) for rid in ['one','two']]}
        original=copy.deepcopy(p['facts']);p['facts']=[]
        for rid in ['one','two']:
            for row in original:p['facts'].append({**copy.deepcopy(row),'id':row['id']+'_'+rid,'realization_id':rid})
        p['owner_maps']={rid:copy.deepcopy(p['owner_maps']['base']) for rid in ['one','two']}
        seal(data,{'pose':['holding_one','holding_two']},cid=B);dependencies(data,A,'base',[B]);seal(data,{'pose':['holding']});c.validate(data)
        frozen=hands_core();pending=c.entry(data,A,realization_id='base')
        self.assertTrue(e.admission(pending,frozen,allow_unselected=True)['search_only'])
        # Explicit owners on root and child are bound to actual child RID.
        choice=choices(data,frozen);choice['entries']+=choices(data,frozen,cid=B,rid='two')['entries']
        selected=c.entry(data,A,realization_id='base',dependency_selections={B:'two'},owner_selections=choice)
        self.assertTrue(e.admission(selected,frozen)['allowed'])
        self.assertTrue(e.permission_scope(selected,frozen)[0])
        missing=c.entry(data,A,realization_id='base',owner_selections=choice)
        self.assertFalse(e.admission(missing,frozen)['allowed'])
        self.assertRaises(ValueError,e.permission_scope,missing,frozen)
    def test_preservation_uses_nonrecursive_whole_selected_scope_and_final_literal_evidence(self):
        from tests.test_photo_native_v4_guards import scoped_core,preserve,guarded
        frozen=scoped_core();rule=preserve();rule.pop('owner_role');rule['owner']=ep('actor')
        data=guarded([]);data['candidates'][A]['conditions']={'native_guards':block(rule)}
        seal(data,{'test_role':['effect']});c.validate(data)
        for view in [data,{**data,'candidates':{A:layout.guard_record(data['candidates'][A],data)}}]:
            entry=c.entry(view,A,realization_id='base');receipt=e.admission(entry,frozen)
            self.assertTrue(receipt['allowed'],receipt);self.assertEqual(e.permission_scope(entry,frozen)[0],['pose'])
            self.assertTrue(e.admission(entry,scoped_core('known_absent',has_value=False))['allowed'])
            item=e.frozen_witnesses(frozen)['scope_inventories'][0]['inventory']['items'][0];phrase='The same ivory skin tone is preserved.'
            interpretation={'scope_preservation_evidence':{'scope':{item['assertion_id']:{'owner':item['target'],'value':item['value'],'prompt_evidence':phrase}}}}
            e.audit_scope_preservation(receipt,interpretation,phrase)
            self.assertRaises(ValueError,e.audit_scope_preservation,receipt,{},phrase)
            for bad in [scoped_core('unknown'),scoped_core(complete=False),scoped_core(host_complete=False)]:
                self.assertFalse(e.admission(entry,bad)['allowed']);self.assertRaises(ValueError,e.permission_scope,entry,bad)
        # A child guard must see the parent's changed receiver in the same whole root.
        parent=guarded([],prop='skin.tone',target='face',role='primary_face');child=copy.deepcopy(data['candidates'][A]);child['id']=B
        # Explicit same source-local map target in the different child CID.
        child['conditions']['native_guards']['rules'][0]['owner']['candidate_id']=B
        parent['candidates'][B]=child;parent['slot_catalog']['child_pose']={**data['slot_catalog']['test_role'],'id':'child_pose'}
        child['content']['role_evidence']['roles']={};seal(parent,{'child_pose':['effect']},cid=B)
        rec=parent['candidates'][A];rec['record_kind']='visual_bundle';rec['content']['member_candidates']=[dict(candidate_id=B,adoption='required',requirements={})]
        dependencies(parent,A,'base',[B]);seal(parent,{'test_role':['effect']});c.validate(parent)
        entry=c.entry(parent,A,realization_id='base');self.assertFalse(e.admission(entry,frozen)['allowed']);self.assertRaises(ValueError,e.permission_scope,entry,frozen)
    def test_v1_entity_owner_value_stays_literal_while_v2_uses_exact_graph_alias(self):
        from tests.test_photo_native_v4_guards import guarded,block as v1block
        frozen=core(['actor_A','actor_B','actor_alias'],[],[('equivalent','actor_alias','actor_B')])
        frozen['semantic_assertions'].append(assertion('literal_link','fact',dimension='relationship',owner='actor_A',property='relationship.fixture_peer',value_type='entity.owner_id/v1',value='actor_alias'))
        frozen['intent_lock']['locked_dimensions'].append('relationship')
        rule=dict(id='literal',kind='frozen_entity_relation',left_role='main_subject',right_role='secondary_subject',dimension='relationship',property='relationship.fixture_peer',value_type='entity.owner_id/v1')
        data=guarded([rule]);entry=c.entry(data,A,realization_id='base')
        self.assertFalse(e.admission(entry,frozen)['allowed'])
        frozen['semantic_assertions'][-1]['axes']['value']='actor_B';self.assertTrue(e.admission(entry,frozen)['allowed'])


# Exact historical source snapshots; corrections below are isolated, manually
# authored test applications, never operating source/proof migration.
ORIGINAL_CASES={'1278': {'record': {'conditions': {'for_any': ['human']}, 'content': {'en': 'blank face with warm helpful hands', 'ko': '무표정하지만 손은 따뜻한 인상', 'tags': ['human', 'expression']}, 'effects': {'dimensions': ['expression'], 'properties': []}, 'id': 'cand_7f96b80af091533cb700db081b3dbbaf', 'provenance': [{'sha256': '5d6b0f287b1f40261fe387a0b9f8cd00e288e4043957c86edd7746b2850cc356', 'source': 'slot:expression:blank_face_warm_hands'}], 'record_kind': 'visual_option'}, 'sha256': '690b386d8d6aeb930a6b4bded24c5aa5d32aba4086f13519b7ac015e01adcda3'}, '1296': {'record': {'conditions': {}, 'content': {'embedding_text': 'warm mug held in both hands', 'en': 'warm mug held in both hands', 'ko': '두 손으로 감싼 따뜻한 머그', 'tags': ['prop', 'mug', 'home', 'cafe']}, 'effects': {'dimensions': [], 'properties': []}, 'id': 'cand_1b714a345bd35bc08d6592bf94caca29', 'provenance': [{'sha256': 'cffaff26c43d18fd73d70832a72eed7ded0b87bb6de3d653c1df1db5c8675c74', 'source': 'slot:prop:warm_mug_held_prop'}], 'record_kind': 'visual_option'}, 'sha256': '6a1960fe44859e6ab5c7e23b6e3be0af47c07daba4fdfd320798796561cb5032'}}


class SourceGuardOriginalCaseTests(unittest.TestCase):
    def test_1296_historical_hash_existing_only_both_hands_and_warmth_effect_fixture(self):
        original=ORIGINAL_CASES['1296'];self.assertEqual(c.digest(original['record']),original['sha256'])
        cid=original['record']['id'];data=hands_source(cid);rec=data['candidates'][cid];p=rec['content']['role_evidence']
        rec['content']['en']+=' The mug has declared warm physical temperature.'
        rec['effects']['dimensions'].append('material');rec['effects']['properties'].append(dict(dimension='material',target='mug',property='temperature.state'))
        p['facts'].append(fact('warmth','material','mug','temperature.state','effect','warm',[],quote='warm physical temperature',operation='set_value',receivers=[]))
        data['slot_catalog']['fixture_temperature']=slot('fixture_temperature',['material'],property_prefixes=['temperature.state'])
        p['review']['original_review']['source_record_sha256']=original['sha256']
        p['review']['source_correction']={'before_sha256':e.meaning_sha256(original['record']),'after_sha256':'pending',
            'rationale':'Isolated manually authored existing-only application; exact original snapshot retained. Warmth is an effect, not pre-existing or sensory proxy.'}
        seal(data,{'pose':['holding'],'fixture_temperature':['warmth']},cid=cid);c.validate(data);frozen=hands_core()
        self.assertEqual(original['record']['effects']['properties'],[])
        choice=choices(data,frozen,cid=cid)
        for view in [data,{**data,'candidates':{cid:layout.guard_record(rec,data)}}]:
            entry=c.entry(view,cid,realization_id='base',owner_selections=choice)
            self.assertTrue(e.admission(entry,frozen)['allowed']);self.assertEqual(e.permission_scope(entry,frozen)[0],['material','pose'])
        p['facts']=[f for f in p['facts'] if f['id']!='warmth'];p['roles'].pop('fixture_temperature')
        seal(data,{'pose':['holding']},cid=cid);self.assertRaises(ValueError,c.validate,data)
    def test_1278_historical_hash_same_character_face_and_hand_region_no_measured_heat(self):
        original=ORIGINAL_CASES['1278'];self.assertEqual(c.digest(original['record']),original['sha256']);cid=original['record']['id']
        rows=[fact('face','subject','face','anatomy.face.presence','prerequisite','present',[]),
            fact('hands','subject','hands','entity.kind','prerequisite','hand_region',[]),
            fact('blank','expression','face','expression.face','effect','blank',[],operation='set_value',receivers=[]),
            fact('warm_helpful','expression','hands','expression.hand_presentation','effect','warm_helpful_impression',[],operation='set_value',receivers=[])]
        data=source('The existing character has a blank face with warm helpful hands as a presentation impression.',rows,
            {'fixture_expression':slot('fixture_expression',['expression'],property_prefixes=['expression.'])},
            {'base':selected_map('face','hands','character')})
        rec=data['candidates'].pop(A);rec['id']=cid;data['candidates'][cid]=rec
        rec['conditions']={'for_any':['human'],'native_guards':block(relation('face_owner',ep('face',cid),ep('character',cid)),
            relation('hand_owner',ep('hands',cid),ep('character',cid)),relation('regions',ep('face',cid),ep('hands',cid),'disjoint'))}
        p=rec['content']['role_evidence'];p['review']['original_review']['source_record_sha256']=original['sha256']
        p['review']['source_correction']={'before_sha256':e.meaning_sha256(original['record']),'after_sha256':'pending',
            'rationale':'Isolated manually authored existing-character presentation; no measured heat or concrete helping action, no aggregate-to-two-owner invention.'}
        seal(data,{'fixture_expression':['blank','warm_helpful']},cid=cid);c.validate(data)
        frozen=core(['secondary_character','face_region','hand_region'],
            [('subject',o,'entity.presence','present') for o in ['secondary_character','face_region','hand_region']]+
            [('subject','face_region','anatomy.face.presence','present'),('subject','hand_region','entity.kind','hand_region')],
            [('part_of','face_region','secondary_character'),('part_of','hand_region','secondary_character'),('disjoint','face_region','hand_region')],role_bindings={})
        frozen['intent_lock']['open_dimensions'].append('expression')
        sign_core(frozen);choice=choices(data,frozen,dict(face='face_region',hands='hand_region',character='secondary_character'),cid=cid)
        for view in [data,{**data,'candidates':{cid:layout.guard_record(rec,data)}}]:
            entry=c.entry(view,cid,realization_id='base',owner_selections=choice)
            self.assertTrue(e.admission(entry,frozen)['allowed']);self.assertEqual(e.permission_scope(entry,frozen)[0],['expression'])
            self.assertTrue(all(f['dimension']!='material' for f in p['facts']))
            self.assertTrue(g.core_entry_eligible(view,frozen,{'subject_category':'human','adult_allowed':True,'intent_constraints':{'domains':[]}},
                {'subject':{'tags':['human']}},'',entry))
            self.assertFalse(g.core_entry_eligible(view,frozen,{'subject_category':'object'},{'subject':{}},'',entry))
        self.assertEqual(original['record']['effects']['properties'],[])


class SourceGuardExactBoundaryTests(unittest.TestCase):
    def test_explicit_alias_of_selected_holder_passes_and_equivalent_is_not_part(self):
        data=hands_source();frozen=hands_core();frozen['semantic_assertions'] += [
            assertion('alias_owner','owner',owner='holder_alias',owner_kind='entity'),
            assertion('alias_relation','equivalent',left='holder_alias',right='secondary')]
        sign_core(frozen);selection=choices(data,frozen,dict(hand_a='a2',hand_b='b2',mug='mug2',holder='holder_alias'))
        self.assertTrue(e.admission(c.entry(data,A,realization_id='base',owner_selections=selection),frozen)['allowed'])
        from tests.test_photo_native_v4_guards import guarded
        data=guarded([]);rec=data['candidates'][A];p=rec['content']['role_evidence']
        rec['conditions']={'native_guards':block(relation('strict_part',ep('region'),ep('actor')))}
        p['owner_maps']['base']['bindings']+=owner_map(('region','primary_face'))['bindings']
        seal(data,{'test_role':['effect']});c.validate(data)
        frozen=core(['actor_A','face_A'],[],[('equivalent','face_A','actor_A')])
        result=e.admission(c.entry(data,A,realization_id='base'),frozen)
        self.assertFalse(result['allowed']);self.assertEqual(result['reason'],'native_owner_relation_unverified')
    def test_exact_named_unicode_targets_and_malformed_typed_rules_do_not_guess_aliases(self):
        data=hands_source();rec=data['candidates'][A];p=rec['content']['role_evidence'];name='왼손 Owner-A'
        for f in p['facts']:
            if f['target']=='hand_a':f['target']=name
        for row in rec['effects']['properties']:
            if row['target']=='hand_a':row['target']=name
        p['owner_maps']['base']['bindings'][0]['target']=name
        for rule in rec['conditions']['native_guards']['rules']:
            if rule['left']['target']=='hand_a':rule['left']['target']=name
        seal(data,{'pose':['holding']});c.validate(data);frozen=hands_core()
        choice=choices(data,frozen,{name:'a2','hand_b':'b2','mug':'mug2','holder':'secondary'})
        self.assertTrue(e.admission(c.entry(data,A,realization_id='base',owner_selections=choice),frozen)['allowed'])
        for field,bad in [('relation',{}),('left',{'kind':'source_target','candidate_id':A,'target':'*'}),('right',{'kind':'source_target','candidate_id':A,'target':'holder.'})]:
            rule=relation('invalid',ep('hand_a'),ep('holder'));rule[field]=bad
            with self.subTest(field=field):self.assertRaises(ValueError,e.validate_source_guards,block(rule))
        rules=[relation('r'+str(i),ep('hand_a'),ep('holder')) for i in range(64)]
        e.validate_source_guards(block(*rules));self.assertRaises(ValueError,e.validate_source_guards,block(*rules,relation('overflow',ep('hand_a'),ep('holder'))))
    def test_stale_core_graph_source_proof_rid_and_unused_bindings_reject(self):
        data=hands_source();frozen=hands_core()
        for field in ['core','graph','meaning','qualification','rid','cid','extra','duplicate']:
            selection=choices(data,frozen);row=selection['entries'][0]
            if field in {'core','graph'}:selection['core_sha256' if field=='core' else 'owner_graph_sha256']='0'*64
            elif field in {'meaning','qualification'}:row[field+'_sha256']='0'*64
            elif field=='rid':row['realization_id']='stale'
            elif field=='cid':row['candidate_id']=B
            elif field=='extra':row['bindings'].append(dict(target='unused',owner_id='main'))
            else:row['bindings'].append(copy.deepcopy(row['bindings'][0]))
            with self.subTest(field=field):
                entry=c.entry(data,A,realization_id='base',owner_selections=selection)
                self.assertFalse(e.admission(entry,frozen)['allowed']);self.assertRaises(ValueError,e.permission_scope,entry,frozen)
    def test_record_aware_property_audit_rebuilds_full_compound_from_bound_source(self):
        data=compound();frozen=hands_core();selection=compound_choices(data,frozen)
        with audit.bound_native_source(data):
            token=audit._BOUND_OWNER_SELECTIONS.set(selection)
            try:
                self.assertTrue(audit.native_property_effects_allowed(frozen,['pose'],[dict(dimension='pose',target='a2',property='body.pose')],candidate_id=A,realization_id='base'))
                selection['entries'][1]['bindings'][-1]['owner_id']='background'
                self.assertFalse(audit.native_property_effects_allowed(frozen,['pose'],[dict(dimension='pose',target='a2',property='body.pose')],candidate_id=A,realization_id='base'))
            finally:audit._BOUND_OWNER_SELECTIONS.reset(token)
        # No v2 guard: retain the old unique non-base RID inference exactly.
        from tests import test_photo_native_owner_selection as legacy
        data=legacy.texture_source();cid=legacy.P;rec=data['candidates'][cid];p=rec['content']['role_evidence']
        rec['effects']['realizations']={'mode':'one','branches':[dict(id='named',conditions={},context_terms=[],effects={'dimensions':[],'properties':[]})]}
        for f in p['facts']:f['realization_id']='named'
        p['owner_maps']={'named':p['owner_maps']['base']};seal(data,{'texture':['cracks']},cid=cid)
        frozen=legacy.owner_core();selection=legacy.selections(data,frozen,rid='named')
        with audit.bound_native_source(data):
            token=audit._BOUND_OWNER_SELECTIONS.set(selection)
            try:self.assertTrue(audit.native_property_effects_allowed(frozen,['material'],[dict(dimension='material',target='surface',property='texture.surface')],candidate_id=cid))
            finally:audit._BOUND_OWNER_SELECTIONS.reset(token)


if __name__=='__main__':unittest.main()
