"""Joint selected E assertions, isolated source declarations; no CID approval."""
import copy
import hashlib
from pathlib import Path
import tempfile
import unittest

from tests.test_photo_semantic_evidence import fact, seal, assertion, source, owner_map, core as base_core, A
from tests.photo_native_schema import slot
from tests.test_photo_native_compound_evidence import B, dependencies
from tests.test_photo_native_owner_selection import (P, texture_source, owner_core,
    sign_core, owner_pack, chosen_composition)
from tests.test_photo_native_source_guards_v2 import block, ep, relation
import photo_candidate_corpus as c
import photo_semantic_evidence as e
import photo_search_layout as layout
import photo_candidate_realizations as realizations
import prompt_generator as g
import audit_composed_prompt as audit
import audit_image_render_request as render


def variant(value='smooth', *, prop='texture.surface', operation='set_value',
            value_type=None, receivers=()):
    data=texture_source(B);record=data['candidates'][B]
    # Explicit fixture correction, not synonym/meaning inference. P/carrier stay fixed.
    record['content']['en']='Set '+value+' on the existing leather surface as the declared '+prop+'.'
    if receivers:record['content']['en']+=' Apply the same setting to the independently declared receiver surfaces.'
    proof=record['content']['role_evidence'];row=next(f for f in proof['facts'] if f['id']=='cracks')
    row.update(quote=value,property=prop,operation=operation,receivers=list(receivers))
    row['value']={'type':value_type or prop+'/v1','value':value}
    for receiver in receivers:
        proof['owner_maps']['base']['bindings'].append({'target':receiver,'origin':'existing','introduced_by':None,
            'selector':{'kind':'selected_existing_owner'}})
    record['effects']['properties'][0]['property']=prop
    return seal(data,{'texture':['cracks']},cid=B)


def pair(*,required=False,optional=False,value='smooth',prop='texture.surface',operation='set_value',
         value_type=None,receivers=(),receiver_b=None,guard=False):
    data=texture_source()
    if receivers:
        rec=data['candidates'][P];proof=rec['content']['role_evidence']
        rec['content']['en']+=' Apply the same cracked setting to independently declared receiver surfaces.'
        proof['facts'][-1]['receivers']=list(receivers)
        for receiver in receivers:proof['owner_maps']['base']['bindings'].append({'target':receiver,'origin':'existing',
            'introduced_by':None,'selector':{'kind':'selected_existing_owner'}})
        seal(data,{'texture':['cracks']},cid=P)
    data['candidates'][B]=variant(value,prop=prop,operation=operation,value_type=value_type,
        receivers=receivers if receiver_b is None else receiver_b)['candidates'][B]
    if guard:
        # Guard-only owner belongs to this source, never injected into a sibling proof.
        rec=data['candidates'][P];proof=rec['content']['role_evidence']
        proof['owner_maps']['base']['bindings'].append({'target':'holder','origin':'existing',
            'introduced_by':None,'selector':{'kind':'selected_existing_owner'}})
        rec['conditions']={'native_guards':block(relation('separate',ep('surface',P),ep('holder',P),'disjoint'))}
        seal(data,{'texture':['cracks']},cid=P)
    if required or optional:
        rec=data['candidates'][P];rec['record_kind']='visual_bundle'
        phrase='A cracked texture is applied to the existing leather surface.'
        if receivers:phrase+=' Apply that same cracked setting to the independently declared receiver surfaces.'
        rec['content']['components']=[{'id':'parent_texture','concept_units':[phrase],'minimum_realizations':1}]
        component=copy.deepcopy(next(f for f in rec['content']['role_evidence']['facts'] if f['id']=='cracks'))
        component.update(id='component_cracks',pointer='/content/components/0/concept_units/0',quote='cracked')
        rec['content']['role_evidence']['facts'].append(component)
        rec['content']['member_candidates']=[{'candidate_id':B,'adoption':'optional' if optional else 'required','requirements':{}}]
        dependencies(data,P,'base',[B])
        if optional:rec['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
        seal(data,{'texture':['cracks']},cid=P)
    c.validate(data)
    return data


def frozen(*,aliases=False):
    value=owner_core()
    if aliases:
        for name,original in [('coat_alias','coat_surface'),('bench_alias','bench_surface')]:
            value['semantic_assertions'] += [assertion('owner_'+name,'owner',owner=name,owner_kind='entity'),
                assertion('alias_'+name,'equivalent',left=name,right=original)]
    return sign_core(value)


def choices(data,core,*,other='coat_surface',receiver_alias=False,omit_child=False,rids=None):
    entries=[]
    for cid,rec in data['candidates'].items():
        if omit_child and cid==B:continue
        proof=rec['content']['role_evidence'];bindings=[];rid=(rids or {}).get(cid,'base')
        for row in proof['owner_maps'][rid]['bindings']:
            owner='coat_surface' if cid==P else other
            if row['target']=='holder':owner='bench_surface'
            if row['target']=='receiver_a':owner='bench_alias' if cid==B and receiver_alias else 'bench_surface'
            if row['target']=='receiver_b':owner='cloth_surface'
            bindings.append({'target':row['target'],'owner_id':owner})
        entries.append({'candidate_id':cid,'realization_id':rid,'meaning_sha256':proof['meaning_sha256'],
            'qualification_sha256':c.digest(proof),'bindings':bindings})
    return {'schema':e.OWNER_SELECTION_SCHEMA,'core_sha256':core['canonical_sha256'],
        'owner_graph_sha256':c.digest(e.frozen_witnesses(core)['graph']),'entries':entries}


def views(data):
    return [('full',data),('compact',{**data,'candidates':{cid:layout.guard_record(rec,data)
        for cid,rec in data['candidates'].items()}})]


class JointAssignmentTests(unittest.TestCase):
    def entries(self,view,selected,required=False,dependencies=None):
        return [c.entry(view,cid,realization_id='base',owner_selections=selected,
            dependency_selections=dependencies) for cid in ([P] if required else [P,B])]

    def check_joint(self,data,core,selected,allowed,*,required=False):
        before=c.canonical_bytes(data)
        for label,view in views(data):
            entries=self.entries(view,selected,required)
            with self.subTest(view=label):
                if allowed:e.validate_joint_effect_assignments(entries,core)
                else:
                    with self.assertRaisesRegex(ValueError,'conflicting joint effect assignment'):
                        e.validate_joint_effect_assignments(entries,core)
                if required:
                    self.assertEqual(e.admission(entries[0],core)['allowed'],allowed)
                    self.assertEqual(g.core_entry_eligible(view,core,{'subject_category':'object','intent_constraints':{'domains':[]}},
                        {'subject':{}},'',entries[0]),allowed)
                    if allowed:e.permission_scope(entries[0],core)
                    else:
                        with self.assertRaises(ValueError):
                            e.permission_scope(entries[0],core)
        self.assertEqual(c.canonical_bytes(data),before)

    def test_value_type_operation_receiver_conflicts_across_independent_and_required_sources(self):
        for required in [False,True]:
            for defect in ['value','type','operation','receiver']:
                kw={'value':'cracked'}
                if defect=='value':kw['value']='smooth'
                if defect=='type':kw['value_type']='texture.surface.other/v1'
                if defect=='operation':kw['operation']='relocate'
                if defect=='receiver':kw.update(receivers=('receiver_a',),receiver_b=())
                data=pair(required=required,**kw);core=frozen()
                with self.subTest(required=required,defect=defect):
                    self.check_joint(data,core,choices(data,core),False,required=required)

    def test_alias_conflict_disjoint_distinct_property_and_identical_assignments(self):
        for required in [False,True]:
            for case,allowed,kw,owner in [('alias_conflict',False,{},'coat_alias'),
                    ('disjoint',True,{},'bench_surface'),('same',True,{'value':'cracked'},'coat_surface'),
                    ('property',True,{'prop':'texture.explicit_secondary_setting'},'coat_surface')]:
                data=pair(required=required,**kw);core=frozen(aliases=True)
                with self.subTest(required=required,case=case):
                    self.check_joint(data,core,choices(data,core,other=owner),allowed,required=required)

    def test_receiver_alias_and_order_are_sets_without_literal_rewrite(self):
        for required in [False,True]:
            data=pair(required=required,value='cracked',receivers=('receiver_a','receiver_b'),
                receiver_b=('receiver_b','receiver_a'));core=frozen(aliases=True)
            self.check_joint(data,core,choices(data,core,receiver_alias=True),True,required=required)

    def test_optional_child_unselected_is_not_an_effect_and_selected_child_is_checked(self):
        data=pair(optional=True);core=frozen()
        for label,view in views(data):
            with self.subTest(view=label):
                entry=c.entry(view,P,realization_id='base',owner_selections=choices(data,core,omit_child=True))
                self.assertTrue(e.admission(entry,core)['allowed']);e.permission_scope(entry,core)
                selected=c.entry(view,P,realization_id='base',owner_selections=choices(data,core),dependency_selections={B:'base'})
                self.assertFalse(e.admission(selected,core)['allowed'])
                with self.assertRaisesRegex(ValueError,'conflicting joint effect assignment'):e.permission_scope(selected,core)

    def test_unresolved_discovery_is_search_only_while_final_is_strict(self):
        data=pair(required=True);core=frozen()
        for _,view in views(data):
            entry=c.entry(view,P,realization_id='base')
            self.assertTrue(e.admission(entry,core,allow_unselected=True)['search_only'])
            self.assertFalse(e.admission(entry,core)['allowed'])
            with self.assertRaises(ValueError):e.permission_scope(entry,core)

    def test_guard_only_owner_stays_source_owned_and_values_still_joint(self):
        data=pair(required=True,guard=True);core=frozen()
        selected=choices(data,core)
        self.check_joint(data,core,selected,False,required=True)
        bad=copy.deepcopy(selected);bad['entries'][1]['bindings'].append({'target':'holder','owner_id':'bench_surface'})
        self.assertFalse(e.admission(c.entry(data,P,realization_id='base',owner_selections=bad),core)['allowed'])

    def test_prerequisite_old_effect_new_is_not_a_joint_conflict_but_frozen_lock_still_applies(self):
        data=pair(value='smooth',prop='texture.other_setting')
        rec=data['candidates'][P];proof=rec['content']['role_evidence']
        rec['content']['en']+=' Its explicitly declared prior texture is smooth.'
        proof['facts'].append(fact('old','material','surface','texture.surface','prerequisite','smooth',[],quote='prior texture is smooth'))
        proof['facts'][-2]['requires'].append('old')
        seal(data,{'texture':['cracks']},cid=P);c.validate(data)
        core=frozen();core['semantic_assertions'].append(assertion('old_texture','fact',dimension='material',owner='coat_surface',
            property='texture.surface',value_type='texture.surface/v1',value='smooth'))
        core['intent_lock']['semantic_anchors'].append({'dimension':'material','target':'coat_surface','property':'texture.surface'})
        sign_core(core);selected=choices(data,core)
        for _,view in views(data):
            entries=self.entries(view,selected);e.validate_joint_effect_assignments(entries,core)
            self.assertTrue(e.admission(entries[0],core)['allowed'])
            dims,props,_=e.permission_scope(entries[0],core)
            self.assertFalse(e.property_scope_allowed(core,dims,props))

    def test_shared_child_exact_proof_and_closure_are_repeatable_not_silently_discarded(self):
        data=pair(required=True,value='cracked');other='cand_'+'c'*32
        data['candidates'][other]=copy.deepcopy(data['candidates'][P]);data['candidates'][other]['id']=other
        seal(data,{'texture':['cracks','component_cracks']},cid=other);c.validate(data)
        core=frozen();selected=choices(data,core);before=c.canonical_bytes(data)
        for _,view in views(data):
            entries=[c.entry(view,cid,realization_id='base',owner_selections=selected) for cid in [P,other]]
            e.validate_joint_effect_assignments(entries,core)
            for entry in entries:self.assertTrue(e.admission(entry,core)['allowed'])
            bad=copy.deepcopy(entries);proof=e.proof_of(bad[1]);proof['dependency_guards']['base'][0]['guard']['facts'][-1]['value']['value']='smooth'
            with self.assertRaises(ValueError):e.validate_joint_effect_assignments(bad,core)
        self.assertEqual(c.canonical_bytes(data),before)

    def test_only_actual_selected_branch_adds_its_required_child(self):
        data=pair(required=True);rec=data['candidates'][P];proof=rec['content']['role_evidence']
        own=copy.deepcopy(rec['effects']);facts=copy.deepcopy(proof['facts']);mapping=copy.deepcopy(proof['owner_maps']['base'])
        dep=copy.deepcopy(proof['dependencies']['base'])
        rec['effects']={'dimensions':[],'properties':[],'realizations':{'mode':'one','branches':[
            {'id':rid,'conditions':{},'context_terms':[],'member_candidate_ids':members,'effects':own}
            for rid,members in [('plain',[]),('with_child',[B])]]}}
        proof['facts']=[{**copy.deepcopy(row),'id':rid+'_'+row['id'],'realization_id':rid,
            'requires':[rid+'_'+reference for reference in row['requires']]}
            for rid in ['plain','with_child'] for row in facts]
        proof['owner_maps']={rid:copy.deepcopy(mapping) for rid in ['plain','with_child']}
        proof['dependencies']={'plain':[],'with_child':dep}
        seal(data,{'texture':[row['id'] for row in proof['facts'] if row['mode']=='effect']},cid=P);c.validate(data)
        core=frozen()
        for label,view in views(data):
            for rid,allowed in [('plain',True),('with_child',False)]:
                selected=choices(data,core,omit_child=rid=='plain',rids={P:rid})
                entry=c.entry(view,P,realization_id=rid,owner_selections=selected)
                with self.subTest(view=label,rid=rid):
                    self.assertEqual(e.admission(entry,core)['allowed'],allowed)
                    if allowed:e.permission_scope(entry,core)
                    else:
                        with self.assertRaises(ValueError):e.permission_scope(entry,core)

    def test_lazy_required_child_uses_sealed_compact_and_changed_guard_fails_closed(self):
        data=pair(required=True,value='cracked');core=frozen()
        for label,view in views(data):
            with self.subTest(view=label):
                self.assertEqual(realizations.eligible_ids(view,P,core,{'subject_category':'object','intent_constraints':{'domains':[]}},
                    {'subject':{}},check_effect_scope=False,allow_owner_selection_pending=True),['base'])
        bad=copy.deepcopy(views(data)[1][1]);bad['candidates'][B]['_semantic_evidence_guard']['facts'][-1]['value']['value']='smooth'
        self.assertEqual(realizations.eligible_ids(bad,P,core,{'subject_category':'object','intent_constraints':{'domains':[]}},
            {'subject':{}},check_effect_scope=False,allow_owner_selection_pending=True),[])

    def test_fixed_recording_camera_maps_compare_two_cids_without_dynamic_selections(self):
        data=None
        # Manual synthetic counterparts of the actual 50/24 issue; no actual proof copied.
        for cid,number,label in [(P,'50','standard'),(B,'24','wide-angle')]:
            rows=[fact('focal','camera','camera','lens.focal_length_mm','effect',number,[],
                quote=number+'mm',operation='set_value',receivers=[]),
                fact('class','camera','camera','lens.named_class','effect',
                    'standard' if number=='50' else 'wide_angle',[],quote=label,operation='set_value',receivers=[])]
            one=source('a '+number+'mm '+label+' lens',rows,
                {'lens':slot('lens',['camera'],property_prefixes=['lens.'])},
                {'base':owner_map(('camera','recording_camera'))})
            rec=one['candidates'].pop(A);rec['id']=cid;one['candidates'][cid]=rec
            seal(one,{'lens':['focal','class']},cid=cid)
            if data is None:data=one
            else:data['candidates'][cid]=rec
        c.validate(data);core=sign_core(base_core(['recording_camera_A'],role_bindings={'recording_camera':'recording_camera_A'}))
        for _,view in views(data):
            entries=[c.entry(view,cid,realization_id='base') for cid in [P,B]]
            self.assertTrue(all(e.admission(entry,core)['allowed'] for entry in entries))
            with self.assertRaisesRegex(ValueError,'conflicting joint effect assignment'):
                e.validate_joint_effect_assignments(entries,core)

    def test_part_of_is_not_equivalence_for_assignment_identity(self):
        data=pair(required=True);core=frozen()
        core['semantic_assertions'] += [assertion('coat_present','fact',dimension='subject',owner='coat',
            property='entity.presence',value_type='entity.presence/v1',value='present'),
            assertion('coat_leather','fact',dimension='material',owner='coat',property='surface.material',
                value_type='surface.material/v1',value='leather')]
        core['intent_lock']['semantic_anchors'].append({'dimension':'material','target':'coat','property':'surface.material'})
        sign_core(core)
        self.check_joint(data,core,choices(data,core,other='coat'),True,required=True)


class JointPublicPackTests(unittest.TestCase):
    def composed(self,pack,data,*,required=False,other='coat_surface'):
        composed=chosen_composition(pack,data)
        phrase=('A smooth texture is also assigned to that same existing secondary leather coat surface.'
            if other=='coat_surface' else 'A smooth texture is assigned to the separate existing background leather bench surface.')
        composed['prompt_en']+=' '+phrase
        composed['owner_selections']=choices(data,pack['authorial_core'],other=other)
        if required:
            evidence=composed['candidate_interpretations'] or [r for r in composed['creative_augmentation_brief']['decisions'] if r['candidate_id']==P]
            evidence[0].update(component_evidence={'parent_texture':'Cracked texture remains visible across the existing secondary leather coat.'},relation_evidence={})
        if not required:
            composed['chosen_candidate_ids'].append(B)
            row={'candidate_id':B,'realization_id':'base','artistic_interpretation':'Retain existing leather identity.',
                'transformation':'Assign explicitly declared smooth texture.','prompt_evidence':phrase,
                'affected_properties':[{'dimension':'material','target':other,'property':'texture.surface'}]}
            composed['candidate_interpretations'].append(row)
            for decision in composed['creative_augmentation_brief']['decisions']:
                if decision['candidate_id']==B:
                    decision.update(row,decision='transformed',rationale='Apply explicitly declared smooth texture.',affected_dimensions=['material'])
                    composed['candidate_interpretations']=[r for r in composed['candidate_interpretations'] if r['candidate_id']!=B]
        elif other!='coat_surface':
            evidence=composed['candidate_interpretations'] or [r for r in composed['creative_augmentation_brief']['decisions'] if r['candidate_id']==P]
            evidence[0]['affected_properties'].append({'dimension':'material','target':other,'property':'texture.surface'})
        composed['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(composed['prompt_en'].encode()).hexdigest()
        return composed

    def request(self,pack,composed,report):
        resolution=report.get('native_owner_resolution') or {}
        return {'schema_version':'photo-image-render-request/v2','pack_id':pack['pack_id'],
            'global_retrieval_sha256':pack['global_retrieval']['canonical_sha256'],
            'source_intent_lock_sha256':pack['authorial_core']['intent_lock']['canonical_sha256'],
            'source_embodiment_preflight_sha256':pack['embodiment_preflight']['canonical_sha256'],
            'runtime_prompt_en':composed['prompt_en']+'\n\nAvoid: '+composed['negative_en'],
            'runtime_negative_en':composed['negative_en'],'references':[],
            'audit_boundary':{'composed_prompt_audit_status':'pass','runtime_prompt_audit_status':'not_run','inherits_composed_prompt_pass':False},
            'native_owner_resolution_sha256':resolution.get('canonical_sha256'),
            'source_composed_sha256':resolution.get('composed_sha256')}

    def check_pack(self,required):
        data=pair(required=required)
        with tempfile.TemporaryDirectory() as temp:
            _,pack,runtime,query=owner_pack(Path(temp),data,bundle_refs=[P] if required else [])
            self.addCleanup(runtime.reader.close);before=c.canonical_bytes(pack)
            for other,allowed in [('coat_surface',False),('bench_surface',True)]:
                composed=self.composed(pack,runtime,required=required,other=other)
                report=audit.audit_composed_prompt(pack,composed,source_data=runtime,query_context=query)
                with self.subTest(required=required,other=other):
                    self.assertEqual(report['status'],'pass' if allowed else 'fail',report)
                    if not allowed:
                        self.assertTrue(any(f['check']=='native_joint_effect_assignments' or
                            'native' in f['check'] for f in report['failures']),report)
                        if not required:
                            self.assertTrue(any(f['check']=='native_joint_effect_assignments' and
                                'conflicting joint effect assignment' in f['reason'] for f in report['failures']),report)
                        self.assertNotIn('native_owner_resolution',report)
                    request=self.request(pack,composed,report)
                    with audit.bound_native_source(runtime,query):
                        result=render.audit_image_render_request(pack,composed,request)
                    self.assertEqual(result['status'],'pass' if allowed else 'fail',result)
                    if allowed:
                        unused=copy.deepcopy(composed);extra=copy.deepcopy(unused['owner_selections']['entries'][-1])
                        extra['candidate_id']='cand_'+'f'*32;unused['owner_selections']['entries'].append(extra)
                        self.assertTrue(audit.audit_native_adoptions(pack,unused,runtime))
                        rebound=copy.deepcopy(composed)
                        next(row for row in rebound['owner_selections']['entries'] if row['candidate_id']==B)['bindings'][0]['owner_id']='coat_surface'
                        with audit.bound_native_source(runtime,query):
                            stale=render.audit_image_render_request(pack,rebound,request)
                        self.assertTrue(any(f['check']=='native_owner_resolution' for f in stale['failures']))
            self.assertEqual(before,c.canonical_bytes(pack))

    def test_independent_chosen_union_final_and_fresh_runtime_reject_conflict(self):self.check_pack(False)
    def test_required_child_lazy_public_pack_and_fresh_runtime_reject_conflict(self):self.check_pack(True)


if __name__=='__main__':unittest.main()
