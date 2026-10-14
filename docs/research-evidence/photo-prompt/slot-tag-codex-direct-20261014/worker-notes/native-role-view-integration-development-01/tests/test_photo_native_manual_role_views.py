"""Source-qualified views of unchanged facts; synthetic review, no corpus approval."""
import copy
import unittest
from unittest import mock
from tests.test_photo_semantic_evidence import (A,source,fact,owner_map,seal,reattest,core,reviewed_source,assertion)
from tests.photo_native_schema import slot
from tests import test_photo_native_existing_member_scope as scoped
import photo_candidate_corpus as c
import photo_semantic_evidence as e
import photo_semantic_role_views as v
import photo_search_layout as layout
import photo_role_proposals as proposals


def attach(data,role,refs,facets,*,cid=A,view_id='manual_facet'):
    """Explicit fixture authoring; hashes only bind these literal chosen facts.

    This helper is not a production proof converter. The source, selected facet
    and canonical facts/modes below are explicitly authored before it is called.
    """
    rec=data['candidates'][cid];proof=rec['content']['role_evidence']
    rows=[next(row for row in proof['facts'] if row['id']==fid) for fid in refs]
    rid=rows[0]['realization_id'];anchors=[];endpoints=[];required=set()
    def requirements(row):
        for ref in row['requires']:
            if ref not in required:
                required.add(ref);requirements(next(x for x in proof['facts'] if x['id']==ref))
    for row in rows:
        unit=next(x for x in proof['source_units'] if x['realization_id']==rid and x['pointer']==row['pointer'] and x['disposition']=='semantic')
        text=e.positive_string(rec,row['pointer'],realization_id=rid);facet=facets[row['id']]
        start=text.index(facet,text.index(row['quote']))
        anchors.append({'fact_id':row['id'],'pointer':row['pointer'],'source_unit_sha256':c.digest(unit),
            'full_field_sha256':c.digest(text),'facet_quote':facet,'start':start,'stop':start+len(facet)})
        endpoints.append({'fact_id':row['id'],'position':'target'})
        endpoints += [{'fact_id':row['id'],'position':'receiver','index':i} for i in range(len(row.get('receivers',[])))]
        requirements(row)
    view={'schema':v.SCHEMA,'id':view_id,'candidate_id':cid,'realization_id':rid,'role_id':role,
        'spec_sha256':c.digest(data['slot_catalog'][role]),
        'canonical_fact_refs':[{'fact_id':row['id'],'fact_sha256':c.digest(row),'mode':row['mode']} for row in rows],
        'normal_anchors':anchors,'endpoint_refs':endpoints,'requires_refs':sorted(required),
        'whole_closure_sha256':c.digest({key:proof[key] for key in v.CLOSURE_FIELDS}),
        'manual_semantic_facet':'The exact selected positive facet supports this reviewed role.',
        'whole_value_retained':'Retain every original fact mode, complete typed value, operation, target, receiver and requirement.',
        'manual_boundary_rationale':'No unmentioned strike, new owner, body part or unrelated clause is inferred.'}
    proof.setdefault('manual_role_views',[]).append(view)
    proof['roles'][role].setdefault('view_refs',[]).append(view_id);reattest(data,cid)
    return data


def interaction_source(*,mode='effect',role_kind='direct'):
    text='An existing actor and existing gavel. The actor announces while holding the gavel. Holding elsewhere is unrelated.'
    rows=[fact('actorP','subject','actor','entity.presence','prerequisite','present',[],quote='existing actor'),
        fact('gavelP','subject','gavel','entity.presence','prerequisite','present',[],quote='existing gavel'),
        fact('announce','action','actor','action.announcing',mode,'announcing_while_holding_same_gavel',['actorP','gavelP'],
            quote='announces while holding the gavel',operation='set_value',receivers=['gavel'])]
    data=source(text,rows,{
        'relational_action':slot('relational_action',['relationship'],property_prefixes=['interaction.'],semantic_role=role_kind),
        'declaration_action':slot('declaration_action',['action'],property_prefixes=['action.announcing'],semantic_role=role_kind)},
        {'base':owner_map(('actor','main_subject'),('gavel','primary_prop'))})
    seal(data,{'relational_action':['announce'],'declaration_action':['announce']})
    return attach(data,'relational_action',['announce'],{'announce':'holding the gavel'})


def interaction_core():
    return core(['actor_A','gavel_A'],[('subject',owner,'entity.presence','present') for owner in ['actor_A','gavel_A']],
        [('disjoint','actor_A','gavel_A')],role_bindings={'main_subject':'actor_A','primary_prop':'gavel_A'})


def surface_view_source(*,cid=A):
    # The literal optical-response E supports this visual appearance facet,
    # without becoming a material substitution or an invented relationship.
    data=scoped.scope_source(cid=cid);spec=data['slot_catalog']['surface_material']
    spec.update(description='Visible optical response of an actual existing surface.',
        description_ko='실제 기존 표면의 가시적인 광학 반응.',dimensions=['appearance'],property_prefixes=['surface.presentation'],
        includes=['The explicitly rendered glossy response.'],excludes=['An inferred material replacement.'])
    seal(data,{'surface_material':['gloss']},cid=cid)
    return attach(data,'surface_material',['gloss'],{'gloss':'glossy'},cid=cid)


class NativeManualRoleViewTests(unittest.TestCase):
    def test_full_compact_and_proposal_use_same_fact_without_permission_projection(self):
        data=interaction_source();c.validate(data);rec=data['candidates'][A];guard=layout.guard_record(rec,data)
        results=[e.qualification(data['slot_catalog']['relational_action'],row,source_data=data) for row in [rec,guard]]
        self.assertEqual(*results);self.assertEqual(results[0]['status'],'eligible')
        self.assertEqual(results[0]['matched_properties'],[{'dimension':'action','target':'actor','property':'action.announcing'}])
        self.assertEqual(results[0]['matched_manual_role_views'][0]['fact']['receivers'],['gavel'])
        self.assertNotIn('manual_role_views',e.proof_of(guard));self.assertIn('manual_role_view_bindings',e.proof_of(guard))
        proposal=proposals.propose(data,'relational_action',A,[])
        self.assertEqual(proposal['semantic_fit'],{**results[0],'semantic_role':'direct','owner_scope':['fixture_owner']})
        frozen=interaction_core();entry=c.entry(data,A,realization_id='base')
        self.assertTrue(e.admission(entry,frozen)['allowed'])
        dims,props,_=e.permission_scope(entry,frozen);self.assertEqual(dims,['action'])
        self.assertEqual({row['target'] for row in props},{'actor_A','gavel_A'})
        self.assertNotIn('relationship',dims)

    def test_no_external_full_source_authority_never_certifies_compact_or_full_view(self):
        data=interaction_source();rec=data['candidates'][A];guard=layout.guard_record(rec,data)
        for row in [rec,guard]:
            result=e.qualification(data['slot_catalog']['relational_action'],row)
            self.assertEqual(result['status'],'review_required');self.assertEqual(result['reason'],'manual_role_view_full_source_authority_required')
        fake={**data,'candidates':{A:guard}}
        self.assertNotEqual(e.qualification(data['slot_catalog']['relational_action'],guard,source_data=fake)['status'],'eligible')
        self.assertRaises(TypeError,e.qualification,data['slot_catalog']['relational_action'],guard,expected_binding=e.proof_of(guard)['manual_role_view_bindings'])

    def test_out_of_prefix_requires_own_explicit_view_and_exact_role_usage(self):
        for defect in ['absent','no_refs','wrong_ref','orphan','other_role','other_fact','empty','empty_refs']:
            data=interaction_source();p=data['candidates'][A]['content']['role_evidence']
            if defect=='absent':p.pop('manual_role_views');p['roles']['relational_action'].pop('view_refs')
            elif defect=='no_refs':p['roles']['relational_action'].pop('view_refs')
            elif defect=='wrong_ref':p['roles']['relational_action']['view_refs']=['unknown']
            elif defect=='orphan':p['manual_role_views'].append({**copy.deepcopy(p['manual_role_views'][0]),'id':'unreferenced'})
            elif defect=='other_role':p['roles']['declaration_action']['view_refs']=p['roles']['relational_action'].pop('view_refs')
            elif defect=='other_fact':p['roles']['relational_action']['fact_refs']=['actorP']
            elif defect=='empty':p['manual_role_views']=[]
            else:p['roles']['relational_action']['view_refs']=[]
            reattest(data)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)

    def test_recomputed_compact_hashes_never_replace_actual_full_source_binding(self):
        data=interaction_source();guard=layout.guard_record(data['candidates'][A],data)
        for defect in ['value','view_ids','role','catalog','receiver','closure','provenance','source']:
            bad=copy.deepcopy(guard);p=e.proof_of(bad);receipt=p['manual_role_view_bindings']
            if defect=='value':receipt['bindings'][0]['fact']['value']['value']='striking'
            elif defect=='view_ids':receipt['bindings'][0]['view_id']='forged_view'
            elif defect=='role':p['roles']['relational_action']['view_refs']=['forged_view']
            elif defect=='catalog':receipt['bindings'][0]['spec_sha256']='0'*64
            elif defect=='receiver':receipt['bindings'][0]['fact']['receivers']=[]
            elif defect=='closure':receipt['bindings'][0]['whole_closure_sha256']='0'*64
            elif defect=='provenance':p['qualification_sha256']='0'*64
            else:p['meaning_sha256']='0'*64
            receipt['receipt_sha256']=c.digest({k:x for k,x in receipt.items() if k!='receipt_sha256'})
            p['compact_sha256']=c.digest({k:x for k,x in p.items() if k!='compact_sha256'})
            with self.subTest(defect=defect):
                self.assertNotEqual(e.qualification(data['slot_catalog']['relational_action'],bad,source_data=data)['status'],'eligible')
        wrong=copy.deepcopy(data);wrong['candidates'][A]['provenance'][0]['sha256']='0'*64
        self.assertNotEqual(e.qualification(data['slot_catalog']['relational_action'],data['candidates'][A],source_data=wrong)['status'],'eligible')

    def test_native_whole_validation_runs_before_view_compiler(self):
        for defect in ['source','missing_E','owner','guard','unit','proof_signature']:
            data=interaction_source();rec=data['candidates'][A];p=rec['content']['role_evidence']
            if defect=='source':rec['content']['en']='No original actor or holding clause.'
            elif defect=='missing_E':p['facts']=[row for row in p['facts'] if row['id']!='announce']
            elif defect=='owner':p['owner_maps']['base']['bindings'].pop()
            elif defect=='guard':p['guard_sets']['base']['source_conditions']=[]
            elif defect=='unit':p['source_units'][0]['quote']='holding the gavel'
            else:p['review']['native_review']['native_contract_sha256']='0'*64
            if defect!='proof_signature':reattest(data)
            with self.subTest(defect=defect),mock.patch.object(v,'validate_full_views',wraps=v.validate_full_views) as call:
                self.assertRaises(ValueError,c.validate,data);self.assertEqual(call.call_count,0)

    def test_facet_needs_exact_ordinary_canonical_quote_occurrence(self):
        for defect in ['outside_quote','wrong_offset','other_field','reference','metadata','unit_hash','guard_id']:
            data=interaction_source();rec=data['candidates'][A];p=rec['content']['role_evidence'];view=p['manual_role_views'][0];a=view['normal_anchors'][0]
            if defect=='outside_quote':
                a.update(facet_quote='Holding elsewhere',start=rec['content']['en'].index('Holding elsewhere'));a['stop']=a['start']+len(a['facet_quote'])
            elif defect=='wrong_offset':a['start']=True
            elif defect=='other_field':a['pointer']='/content/ko'
            elif defect=='reference':p['source_units'][0]['disposition']='semantic_reference'
            elif defect=='metadata':a['pointer']='/content/activation/exact_terms/0'
            elif defect=='unit_hash':a['source_unit_sha256']='0'*64
            else:view['canonical_fact_refs'][0]['fact_id']='guard_only_support'
            reattest(data)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)

    def test_all_original_positions_requires_modes_and_sentinel_boundaries(self):
        for defect in ['receiver','requires','value','operation','mode','fact_hash','sentinel']:
            data=interaction_source();p=data['candidates'][A]['content']['role_evidence'];view=p['manual_role_views'][0];row=p['facts'][-1]
            if defect=='receiver':view['endpoint_refs'].pop()
            elif defect=='requires':view['requires_refs'].pop()
            elif defect=='value':row['value']['value']='announcing_without_holding'
            elif defect=='operation':row['operation']='relocate'
            elif defect=='mode':row['mode']='context';row.pop('operation');row.pop('receivers')
            elif defect=='fact_hash':view['canonical_fact_refs'][0]['fact_sha256']='0'*64
            else:row['value']={'type':'frozen_property_reference/v1','value':'same'};view['canonical_fact_refs'][0]['fact_sha256']=c.digest(row)
            reattest(data)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)
        for mode,kind in [('prerequisite','direct'),('preservation','direct'),('context','contextual')]:
            data=interaction_source(mode=mode,role_kind=kind);c.validate(data)
            result=e.qualification(data['slot_catalog']['relational_action'],data['candidates'][A],source_data=data)
            self.assertEqual(result['status'],'eligible');self.assertEqual(result['support_modes'],[mode])
        self.assertRaises(ValueError,c.validate,interaction_source(mode='context'))

    def test_E_and_actual_receivers_stay_subject_to_equal_value_and_property_locks(self):
        data=interaction_source();entry=c.entry(data,A,realization_id='base')
        for owner in ['actor_A','gavel_A']:
            frozen=interaction_core();frozen['intent_lock']['semantic_anchors']=[{'dimension':'action','target':owner,'property':'action.announcing'}]
            self.assertFalse(e.property_scope_allowed(frozen,entry['affected_dimensions'],entry['affected_properties'],record=entry))
        frozen=interaction_core();frozen['semantic_assertions'].append(assertion('old_E','fact',dimension='action',owner='actor_A',property='action.announcing',value_type='action.announcing/v1',value='announcing_while_holding_same_gavel'))
        frozen['intent_lock']['locked_dimensions'].append('action');frozen['intent_lock']['open_dimensions'].remove('action')
        self.assertFalse(e.property_scope_allowed(frozen,entry['affected_dimensions'],entry['affected_properties'],record=entry))

    def test_view_does_not_change_each_member_P_PR_or_quantified_guards(self):
        data=surface_view_source();c.validate(data);frozen=scoped.scope_core();mapping=scoped.choices(data,frozen)
        for entry in scoped.entries(data,frozen,mapping=mapping):
            result=e.admission(entry,frozen);self.assertTrue(result['allowed'],result);self.assertEqual(len(result['resolved_frozen_facts']),4)
            self.assertEqual({p['target'] for p in e.permission_scope(entry,frozen)[1]},{'coat_A','glove_A'})
        for defect in ['P','PR','relation']:
            bad=scoped.scope_core()
            if defect=='relation':bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['assertion_id']!='owned_1']
            else:
                prop='entity.kind' if defect=='P' else 'entity.presence'
                bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if not(x['axes'].get('owner')=='glove_A' and x['axes'].get('property')==prop)]
            scoped.neutral.reseal(bad)
            if defect=='PR':mapping=scoped.choices(data,frozen)
            else:mapping=scoped.choices(data,bad)
            with self.subTest(defect=defect):self.assertFalse(e.admission(scoped.entries(data,bad,mapping=mapping)[0],bad)['allowed'])

    def test_absent_view_fields_preserve_old_literal_qualification_and_hash_recipe(self):
        data=reviewed_source();rec=data['candidates'][A];p=rec['content']['role_evidence'];before=c.canonical_bytes(p)
        expected={'status':'eligible','reason':'source_reviewed_mode_specific_evidence','native_qualification':'qualified',
            'matched_properties':[{'dimension':'material','target':'main_subject','property':'surface.material'}],
            'meaning_terms':[],'fact_refs':['satin'],'support_modes':['effect']}
        self.assertEqual(e.qualification(data['slot_catalog']['surface_material'],rec),expected)
        self.assertEqual(e.qualification(data['slot_catalog']['surface_material'],layout.guard_record(rec,data),source_data=data),expected)
        self.assertNotIn('manual_role_view_bindings',e.compact(rec,data));self.assertEqual(before,c.canonical_bytes(p))
        material={key:value for key,value in p.items() if key!='review'}
        material['review_bindings']={key:p['review'].get(key) for key in ['original_review','source_correction']}
        self.assertEqual(e.native_contract_sha256(p),c.digest(material))

    def test_opt_in_caps_and_whole_spec_source_pins_fail_without_truncation(self):
        for defect in ['overflow','duplicate','spec','closure','rid','fullfield','pointer']:
            data=interaction_source();p=data['candidates'][A]['content']['role_evidence'];view=p['manual_role_views'][0]
            if defect=='overflow':p['manual_role_views']=[{**copy.deepcopy(view),'id':'view_'+str(i)} for i in range(129)]
            elif defect=='duplicate':p['manual_role_views'].append(copy.deepcopy(view))
            elif defect=='spec':data['slot_catalog']['relational_action']['excludes'].append('new explicit boundary');p['catalog_sha256']=c.digest(data['slot_catalog'])
            elif defect=='closure':view['whole_closure_sha256']='0'*64
            elif defect=='rid':view['realization_id']='sibling'
            elif defect=='fullfield':view['normal_anchors'][0]['full_field_sha256']='0'*64
            else:view['normal_anchors'][0]['pointer']='/content/realization_content/sibling/en'
            reattest(data)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)


if __name__=='__main__':unittest.main()
