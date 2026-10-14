"""Explicit isolated existing-carrier application, not an actual CID approval.

No operating source/index/runtime is modified. Original 1272 bytes are embedded
only to bind the manual fixture correction; source modes below are authored.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from tests.test_photo_semantic_evidence import A,source,fact,owner_map,seal,core,assertion,reviewed_source
from tests.test_photo_native_compound_evidence import dependencies,B
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_semantic_evidence as e
import photo_search_layout as layout
import photo_role_proposals as roles
import prompt_generator as g
import audit_composed_prompt as audit

P='cand_4bf6badb8139555bbb907f10bf7f1ea6'
ORIGINAL={'conditions':{},'content':{'embedding_text':'cracked leather texture','en':'cracked leather texture',
 'ko':'cracked leather texture','tags':['leather','vintage','texture']},'effects':{'dimensions':['material'],'properties':[]},
 'id':P,'provenance':[{'sha256':'ff0629c4c823cdcf5b2ff19b1ffaf7e605d6808922d69ba6cd962a4525bf1734',
 'source':'slot:texture:cracked_leather_texture'}],'record_kind':'visual_option'}
ORIGINAL_SHA='ec33f6feefdd422d122c4a7b71972bc5d132b190e6dc8da2d3bf6b59c2989513'
ORIGINAL_MEANING='90bb27d0eaca5367b51884cb507744c07acfbc9bf2c0ce49fd03cb28b4883ce8'


def texture_source(cid=P):
    rows=[fact('present','subject','surface','entity.presence','prerequisite','present',[],quote='existing'),
          fact('leather','material','surface','surface.material','prerequisite','leather',[],quote='leather'),
          fact('cracks','material','surface','texture.surface','effect','cracked',['present','leather'],
               quote='cracked',operation='set_value',receivers=[])]
    mapping={'schema':e.SELECTOR_OWNER_SCHEMA,'bindings':[{'target':'surface','origin':'existing',
        'introduced_by':None,'selector':{'kind':'selected_existing_owner'}}]}
    data=source('A cracked texture is applied to the existing leather surface, preserving its carrier and leather identity.',
        rows,{'texture':slot('texture',['material'],property_prefixes=['texture.'])},{'base':mapping},
        correction={'before_sha256':ORIGINAL_MEANING,'after_sha256':'pending',
                    'rationale':'Isolated manually authored existing-application fixture; coarse original effects refined, no operating source correction.'})
    rec=data['candidates'].pop(A);rec['id']=cid;data['candidates'][cid]=rec
    rec['content']['role_evidence']['review']['original_review']['source_record_sha256']=ORIGINAL_SHA
    return seal(data,{'texture':['cracks']},cid=cid)


def sign_core(frozen):
    frozen.pop('canonical_sha256',None);frozen.pop('core_id',None)
    frozen['canonical_sha256']=c.digest(frozen);frozen['core_id']=frozen['canonical_sha256'][:16]
    return frozen


def owner_core():
    owners=['actor_A','coat_surface','bench_surface','cloth_surface','coat']
    values=[(dim,owner,prop,value) for owner,material in [('coat_surface','leather'),('bench_surface','leather'),('cloth_surface','cotton')]
        for dim,prop,value in [('subject','entity.presence','present'),('material','surface.material',material)]]
    frozen=core(owners,values,[('part_of','coat_surface','coat'),('disjoint','coat','bench_surface'),
        ('disjoint','cloth_surface','coat'),('disjoint','cloth_surface','bench_surface')])
    frozen['intent_lock']['locked_dimensions'].remove('material');frozen['intent_lock']['open_dimensions'].append('material')
    frozen['intent_lock']['semantic_anchors']=[{'dimension':'material','target':owner,'property':'surface.material'}
        for owner in ['coat_surface','bench_surface','cloth_surface']]
    return sign_core(frozen)


def selections(data,frozen,owner='coat_surface',cid=P,rid='base'):
    p=data['candidates'][cid]['content']['role_evidence']
    return {'schema':e.OWNER_SELECTION_SCHEMA,'core_sha256':frozen['canonical_sha256'],
        'owner_graph_sha256':c.digest(e.frozen_witnesses(frozen)['graph']),
        'entries':[{'candidate_id':cid,'realization_id':rid,'meaning_sha256':p['meaning_sha256'],
            'qualification_sha256':c.digest(p),'bindings':[{'target':'surface','owner_id':owner}]}]}


class OwnerSelectorTests(unittest.TestCase):
    def views(self,data):
        return [data,{**data,'candidates':{cid:layout.guard_record(rec,data) for cid,rec in data['candidates'].items()}}]
    def entry(self,data,frozen,owner='coat_surface',**kwargs):
        return c.entry(data,P,realization_id='base',owner_selections=selections(data,frozen,owner),**kwargs)
    def permitted(self,data,frozen,entry):
        return g.core_entry_eligible(data,frozen,{'subject_category':'object','intent_constraints':{'domains':[]}}, {'subject':{}},'',entry)

    def test_real_source_before_binding_and_no_coarse_effect_autofill(self):
        self.assertEqual(c.digest(ORIGINAL),ORIGINAL_SHA);self.assertEqual(e.meaning_sha256(ORIGINAL),ORIGINAL_MEANING)
        data=texture_source();c.validate(data)
        proof=data['candidates'][P]['content']['role_evidence']
        self.assertEqual(proof['schema'],'photo-candidate-role-evidence/v4')
        self.assertEqual(proof['review']['source_correction']['before_sha256'],ORIGINAL_MEANING)
        self.assertEqual(ORIGINAL['effects']['properties'],[])
        bad=copy.deepcopy(data);bad['candidates'][P]['effects']=copy.deepcopy(ORIGINAL['effects'])
        seal(bad,{'texture':['cracks']},cid=P);self.assertRaises(ValueError,c.validate,bad)

    def test_secondary_background_explicit_choice_full_compact_and_same_typed_witnesses(self):
        data=texture_source();frozen=owner_core();expected=[]
        for view in self.views(data):
            for owner in ['coat_surface','bench_surface']:
                # Request object comes from full source proof hash, even for a compact view.
                entry=c.entry(view,P,realization_id='base',owner_selections=selections(data,frozen,owner))
                receipt=e.admission(entry,frozen);self.assertTrue(receipt['allowed'],receipt)
                self.assertEqual(receipt['owner_resolution']['bindings'][0]['owner_id'],owner)
                self.assertEqual({row['owner'] for row in receipt['resolved_frozen_facts']},{owner})
                self.assertTrue(self.permitted(view,frozen,entry))
                self.assertEqual(e.permission_scope(entry,frozen)[1],[{'dimension':'material','target':owner,'property':'texture.surface'}])
                self.assertNotIn('foreground_surface',e.frozen_witnesses(frozen)['graph']['roles'])
                expected.append(receipt)
        self.assertEqual(expected[:2],expected[2:])

    def test_missing_choice_remains_search_only_and_final_is_denied_even_with_one_owner(self):
        data=texture_source();frozen=core(['sole_surface'],[('subject','sole_surface','entity.presence','present'),('material','sole_surface','surface.material','leather')],role_bindings={})
        frozen['intent_lock']['locked_dimensions'].remove('material');frozen['intent_lock']['open_dimensions'].append('material')
        frozen['intent_lock']['semantic_anchors']=[{'dimension':'material','target':'sole_surface','property':'surface.material'}];sign_core(frozen)
        entry=c.entry(data,P,realization_id='base')
        self.assertFalse(e.admission(entry,frozen)['allowed'])
        probe=e.admission(entry,frozen,allow_unselected=True)
        self.assertTrue(probe['allowed']);self.assertTrue(probe['search_only'])
        self.assertEqual(probe['reason'],'explicit_existing_owner_selection_required')
        self.assertEqual(entry['owner_selection_requirements']['nodes'][0]['targets'],['surface'])
        self.assertFalse(self.permitted(data,frozen,entry))
        self.assertTrue(g.core_entry_eligible(data,frozen,{'subject_category':'object','intent_constraints':{'domains':[]}}, {'subject':{}},'',entry,allow_owner_selection_pending=True))
        proposal=roles.propose(data,'texture',P,[])
        self.assertEqual(proposal['native_qualification'],'qualified');self.assertEqual(proposal['applicability_status'],'review_required')
        self.assertIn('owner_selection_requirements',proposal)

    def test_wrong_missing_stale_extra_or_duplicate_bindings_fail_without_defaults(self):
        data=texture_source();frozen=owner_core()
        for defect in ['empty','missing','owner','role_word','core','graph','source','proof','rid','cid','extra','duplicate','unknown','schema']:
            choice=selections(data,frozen);row=choice['entries'][0]
            if defect=='empty':choice={}
            elif defect=='missing':row['bindings']=[]
            elif defect=='owner':row['bindings'][0]['owner_id']='unknown_owner'
            elif defect=='role_word':row['bindings'][0]['owner_id']='foreground_surface'
            elif defect=='core':choice['core_sha256']='0'*64
            elif defect=='graph':choice['owner_graph_sha256']='0'*64
            elif defect=='source':row['meaning_sha256']='0'*64
            elif defect=='proof':row['qualification_sha256']='0'*64
            elif defect=='rid':row['realization_id']='foreign'
            elif defect=='cid':row['candidate_id']=B
            elif defect=='extra':row['bindings'].append({'target':'foreign','owner_id':'bench_surface'})
            elif defect=='duplicate':row['bindings'].append(copy.deepcopy(row['bindings'][0]))
            elif defect=='unknown':choice['default_owner']='coat_surface'
            else:choice['schema']='guessed'
            with self.subTest(defect=defect):self.assertFalse(e.admission(c.entry(data,P,realization_id='base',owner_selections=choice),frozen)['allowed'])

    def test_owner_kind_names_and_noncanonical_presence_cannot_invent_material_or_anatomy(self):
        data=texture_source();frozen=owner_core()
        self.assertFalse(e.admission(self.entry(data,frozen,'cloth_surface'),frozen)['allowed'])
        for defect in ['missing','advisory','wrong_dimension','wrong_type','wrong_value','unlocked']:
            bad=copy.deepcopy(frozen);row=next(x for x in bad['semantic_assertions'] if x['axes'].get('owner')=='coat_surface' and x['axes'].get('property')=='entity.presence')
            if defect=='missing':bad['semantic_assertions'].remove(row)
            elif defect=='advisory':row['polarity']='advisory'
            elif defect=='wrong_dimension':row['dimension']='appearance';row['affected_dimensions']=['appearance']
            elif defect=='wrong_type':row['axes']['value_type']='presence/v1'
            elif defect=='wrong_value':row['axes']['value']='planned'
            else:bad['intent_lock']['locked_dimensions'].remove('subject')
            sign_core(bad)
            with self.subTest(defect=defect):
                # Invalid core fixtures can fail before binding as intended.
                try:choice=selections(data,bad)
                except ValueError:continue
                self.assertFalse(e.admission(c.entry(data,P,realization_id='base',owner_selections=choice),bad)['allowed'])

    def test_locked_samevalue_parent_alias_and_unknown_owner_overlap_are_not_permissions(self):
        data=texture_source()
        for lock_owner,prop,allowed in [('coat_surface','texture.surface',False),('coat','texture',False),
            ('bench_surface','texture.surface',True),('cloth_surface','texture.surface',True),('unrelated','texture.surface',False)]:
            frozen=owner_core();frozen['intent_lock']['semantic_anchors'].append({'dimension':'material','target':lock_owner,'property':prop})
            sign_core(frozen);entry=self.entry(data,frozen)
            with self.subTest(owner=lock_owner,property=prop):self.assertEqual(self.permitted(data,frozen,entry),allowed)
        frozen=owner_core();frozen['intent_lock']['open_dimensions'].remove('material');frozen['intent_lock']['locked_dimensions'].append('material');sign_core(frozen)
        self.assertFalse(self.permitted(data,frozen,self.entry(data,frozen)))

    def test_v2_fixed_and_v3_fixed_are_equivalent_and_cannot_be_overridden(self):
        data=reviewed_source();before=copy.deepcopy(data['candidates'][A]['content']['role_evidence'])
        frozen=sign_core(core(['main_subject']))
        old=e.admission(c.entry(data,A),frozen);c.validate(data)
        self.assertEqual(data['candidates'][A]['content']['role_evidence'],before)
        proof=data['candidates'][A]['content']['role_evidence'];proof['owner_maps']['base']={'schema':e.SELECTOR_OWNER_SCHEMA,
            'bindings':[{'target':'main_subject','origin':'existing','introduced_by':None,'selector':{'kind':'core_role','role':'main_subject'}}]}
        seal(data,{'surface_material':['satin']});c.validate(data)
        self.assertEqual(e.admission(c.entry(data,A),frozen),old)
        wrong=selections(data,frozen,owner='main_subject',cid=A);wrong['entries'][0]['bindings'][0]['target']='main_subject'
        self.assertFalse(e.admission(c.entry(data,A,owner_selections=wrong),frozen)['allowed'])

    def test_selected_selector_is_exact_existing_only_and_does_not_hide_footprint(self):
        for defect in ['default','unknown','origin','creator','selector_fields','missing_receiver','count_effect']:
            data=texture_source();p=data['candidates'][P]['content']['role_evidence'];row=p['owner_maps']['base']['bindings'][0]
            if defect=='default':row['selector']['default']='foreground_surface'
            elif defect=='unknown':row['selector']['kind']='guess_owner'
            elif defect=='origin':row['origin']='introduced';row['introduced_by']='cracks'
            elif defect=='creator':p['facts'][-1]['operation']='add_entity'
            elif defect=='selector_fields':row['selector']['role']='foreground_surface'
            elif defect=='missing_receiver':p['facts'][-1]['receivers']=['receiver']
            else:data['candidates'][P]['effects']['dimensions'].append('count');data['candidates'][P]['effects']['properties'].append({'dimension':'count','target':'surface','property':'entity.count'})
            seal(data,{'texture':['cracks']},cid=P)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)


def frozen_owner_run(directory):
    from tests import test_photo_native_fact_wire as wire_fixture
    from tests.test_photo_workflow_precore import files
    helper=wire_fixture.NativeFactWireTests();raw=helper.inputs()
    statement=('An existing secondary leather coat and an existing background leather bench remain beside the linen blanket. '
               'The coat and bench are separate from the blanket and from each other.')
    raw['source_request']+=' '+statement;raw['baseline_prompt_en']+=' '+statement
    raw['subject']+=' with an existing secondary leather coat and background leather bench'
    raw['intent_lock']['locked_dimensions'].remove('material');raw['intent_lock']['open_dimensions'].append('material')
    next(row for row in raw['intent_lock']['semantic_anchors'] if row['anchor_id']=='declared_linen').update(target='main_subject',property='surface.material')
    declarations=[]
    for index,owner in enumerate(['coat_surface','bench_surface']):
        declarations += [assertion('owner_'+owner,'owner',owner=owner,owner_kind='surface'),
            assertion('present_'+owner,'fact',owner=owner,dimension='subject',property='entity.presence',value_type='entity.presence/v1',value='present'),
            assertion('material_'+owner,'fact',owner=owner,dimension='material',property='surface.material',value_type='surface.material/v1',value='leather')]
        raw['intent_lock']['semantic_anchors'].append({'anchor_id':'material_'+owner,'source_text':statement,
            'dimension':'material','target':owner,'property':'surface.material','prompt_evidence':statement})
    for index,(left,right) in enumerate([('coat_surface','bench_surface'),('coat_surface','main_subject'),('bench_surface','main_subject')]):
        declarations.append(assertion('separate_'+str(index),'disjoint',left=left,right=right))
    for row in declarations:row['source_span_ids']=['topic'];row['evidence']={'declared':statement}
    raw['semantic_assertions']+=declarations
    run,_=helper.freeze(directory,raw,raw['source_request'],control_overrides={'sensual':0,'fetish':0})
    _,frozen,controls=files.verify_freeze(files.load_state(run))
    return run,frozen,controls


def owner_pack(directory,source_data=None,*,bundle_refs=()):
    from tests import test_photo_global_retrieval as retrieval_fixture
    from tests.test_photo_slot_queries import synthetic_set
    from tests.test_photo_workflow_precore import FIXTURE,files
    import photo_shared_views as views
    import photo_global_index as index
    from photo_search_reader import SearchReader,LazyRuntimeData
    run,frozen,controls=frozen_owner_run(directory)
    data=texture_source() if source_data is None else source_data
    data['policies']=views.source(retrieval_fixture.GlobalDiscoveryTests().data())['policies']
    data['policies']['bundle_refs']=list(bundle_refs)
    data['policies']['_quality_layers']={'adult_appeal':{'contextual_retrieval':{'contract_version':'photo-contextual-appeal/v2'}}}
    vectors={'schema':index.SCHEMA,'space':index.SPACE,'query_recipe':index.QUERY_RECIPE,'corpus_sha256':c.digest(data),'entries':{}}
    for cid,record in data['candidates'].items():
        recipe,text=index.text(record);vectors['entries'][cid]={'id':cid,'recipe':recipe,'text':text,
            'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':[1.0]+[0.0]*767}
    assets=directory/'synthetic-search';layout.build(assets,data,vectors,activate=True)
    runtime=LazyRuntimeData(SearchReader(assets)).for_core(frozen)
    query=synthetic_set(frozen,controls,data['slot_catalog'],['texture'])
    pack=g.generate_candidate_pack(runtime,frozen,controls,files.value(files.load_state(run),'embodiment_review'),
        seed=5,query_context=query,requested_slots=['texture'])
    return run,pack,runtime,query


def chosen_composition(pack,data,owner='coat_surface'):
    from tests.photo_native_runtime import compose_native
    composed=compose_native(pack);phrase=('Cracked texture remains visible across the existing secondary leather coat.' if owner=='coat_surface'
        else 'Cracked texture remains visible across the existing background leather bench.')
    composed['prompt_en']+=' '+phrase;composed['chosen_candidate_ids']=[P]
    row={'candidate_id':P,'realization_id':'base','artistic_interpretation':'Preserve the existing leather carrier identity',
        'transformation':'Render local cracks on the selected leather surface','prompt_evidence':phrase,
        'affected_properties':[{'dimension':'material','target':owner,'property':'texture.surface'}]}
    composed['candidate_interpretations']=[row]
    for decision in composed['creative_augmentation_brief']['decisions']:
        if decision['candidate_id']==P:
            decision.update(row,decision='transformed',rationale='Apply the declared cracked surface without replacing its leather carrier.',affected_dimensions=['material'])
            composed['candidate_interpretations']=[]
    composed['owner_selections']=selections(data,pack['authorial_core'],owner)
    composed['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(composed['prompt_en'].encode()).hexdigest()
    return composed


class OwnerSelectionPackTests(unittest.TestCase):
    def test_real_freeze_retrieval_public_pack_stays_immutable_and_composed_audit_resolves(self):
        from tests.test_photo_workflow_precore import files
        with tempfile.TemporaryDirectory() as temp:
            run,pack,runtime,query=owner_pack(Path(temp));before=c.canonical_bytes(pack)
            self.assertIn(P,pack['candidate_pool']);self.assertNotIn('owner_selections',pack)
            self.assertEqual(pack['candidate_pool'][P]['applicability']['status'],'review_required')
            self.assertEqual(pack['candidate_pool'][P]['owner_selection_requirements']['nodes'][0]['targets'],['surface'])
            self.assertTrue(audit.authorial_core_v3_semantic_contract_valid(pack['authorial_core'],creative_control_snapshot=pack['creative_controls']))
            receipts=[]
            for owner in ['coat_surface','bench_surface']:
                composed=chosen_composition(pack,runtime,owner)
                report=audit.audit_composed_prompt(pack,composed,source_data=runtime,query_context=query)
                self.assertEqual(report['status'],'pass',report)
                receipt=report['native_owner_resolution'];self.assertEqual(receipt['composed_sha256'],c.digest(composed))
                self.assertEqual(receipt['nodes'][0]['bindings'][0]['owner_id'],owner)
                receipts.append(receipt['canonical_sha256'])
            self.assertNotEqual(*receipts);self.assertEqual(before,c.canonical_bytes(pack))
            self.assertNotIn('owner_selections',files.verify_freeze(files.load_state(run))[1])
            runtime.reader.close()


class EffectAssignmentIntegrityTests(unittest.TestCase):
    def data(self):
        data=reviewed_source();proof=data['candidates'][A]['content']['role_evidence']
        other=copy.deepcopy(proof['facts'][0]);other['id']='satin_second_language';proof['facts'].append(other)
        # Two independent authored literal anchors, one exact assignment.
        seal(data,{'surface_material':['satin','satin_second_language']})
        return data

    def test_equal_multilingual_effect_assignments_pass_full_and_compact(self):
        data=self.data();c.validate(data)
        for rec in [data['candidates'][A],layout.guard_record(data['candidates'][A],data)]:
            entry=c.entry({**data,'candidates':{A:rec}},A)
            self.assertTrue(e.admission(entry,core(['main_subject']))['allowed'])

    def test_conflicting_effect_value_type_operation_or_receiver_rejected(self):
        for field in ['value','type','operation','receivers']:
            data=self.data();row=data['candidates'][A]['content']['role_evidence']['facts'][1]
            if field=='value':row['value']['value']='rough'
            elif field=='type':row['value']['type']='other/v1'
            elif field=='operation':row['operation']='add_entity'
            else:
                row['receivers']=['receiver'];data['candidates'][A]['content']['role_evidence']['owner_maps']['base']['bindings'].append(
                    {'target':'receiver','core_role':'secondary_subject','origin':'existing','introduced_by':None})
            seal(data,{'surface_material':['satin','satin_second_language']})
            with self.subTest(field=field):
                self.assertRaisesRegex(ValueError,'conflicting effect assignment',c.validate,data)
                guard=e.compact(self.data()['candidates'][A],self.data())
                guard['facts']=[{key:value for key,value in fact.items() if key not in {'pointer','quote'}} for fact in data['candidates'][A]['content']['role_evidence']['facts']]
                guard['owner_maps']=copy.deepcopy(data['candidates'][A]['content']['role_evidence']['owner_maps'])
                guard['compact_sha256']=c.digest({key:value for key,value in guard.items() if key!='compact_sha256'})
                with self.assertRaisesRegex(ValueError,'conflicting effect assignment'):
                    e._selected_contract(guard,'base',guard['effect_sets']['base'])

    def test_receiver_order_is_preserved_but_unique_set_equality_is_required(self):
        data=self.data();p=data['candidates'][A]['content']['role_evidence']
        for row,receivers in zip(p['facts'],[['receiver1','receiver2'],['receiver2','receiver1']]):row['receivers']=receivers
        p['owner_maps']['base']['bindings'] += [{'target':name,'core_role':role,'origin':'existing','introduced_by':None}
            for name,role in [('receiver1','secondary_subject'),('receiver2','scene')]]
        seal(data,{'surface_material':['satin','satin_second_language']});c.validate(data)
        self.assertEqual(p['facts'][1]['receivers'],['receiver2','receiver1'])
        p['facts'][1]['receivers']=['receiver1','receiver1'];seal(data,{'surface_material':['satin','satin_second_language']})
        self.assertRaises(ValueError,c.validate,data)

    def test_distinct_properties_allow_explicit_partial_assignments(self):
        data=self.data();p=data['candidates'][A]['content']['role_evidence'];p['facts'][1]['property']='surface.material.finish'
        p['facts'][1]['value']={'type':'surface.material.finish/v1','value':'satin'}
        data['candidates'][A]['effects']['properties'].append({'dimension':'material','target':'main_subject','property':'surface.material.finish'})
        seal(data,{'surface_material':['satin','satin_second_language']});c.validate(data)

    def test_frozen_prerequisite_old_value_is_not_an_effect_conflict(self):
        data=self.data();p=data['candidates'][A]['content']['role_evidence'];row=p['facts'][1]
        row['mode']='prerequisite';row.pop('operation');row.pop('receivers');row['value']['value']='cotton'
        p['facts'][0]['requires']=[row['id']]
        seal(data,{'surface_material':['satin','satin_second_language']});c.validate(data)


class OwnerSelectionClosureTests(unittest.TestCase):
    def compound(self,optional):
        data=reviewed_source();child=texture_source(B);data['slot_catalog'].update(child['slot_catalog'])
        data['candidates'][B]=child['candidates'][B]
        # Refresh catalogue attestations, not semantic modes or facts.
        seal(data,{'texture':['cracks']},cid=B)
        parent=data['candidates'][A];parent['record_kind']='visual_bundle'
        parent['content']['member_candidates']=[{'candidate_id':B,'adoption':'optional' if optional else 'required','requirements':{}}]
        dependencies(data,A,'base',[B])
        if optional:parent['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
        seal(data,{'surface_material':['satin']});c.validate(data)
        return data

    def test_selected_child_scope_and_receiver_resolve_with_full_compact_parity(self):
        for optional in [False,True]:
            data=self.compound(optional);frozen=owner_core();choice=selections(data,frozen,cid=B)
            # Fixed-role parent uses an independently declared role, never a default for child.
            choice=selections(data,frozen,cid=B)
            for record in [data['candidates'][A],layout.guard_record(data['candidates'][A],data)]:
                view={**data,'candidates':{**data['candidates'],A:record}}
                if optional:
                    plain=c.entry(view,A,realization_id='base')
                    self.assertTrue(e.admission(plain,frozen)['allowed'])
                    self.assertNotIn('texture.surface',{p['property'] for p in e.permission_scope(plain,frozen)[1]})
                entry=c.entry(view,A,realization_id='base',dependency_selections={B:'base'},owner_selections=choice)
                result=e.admission(entry,frozen);self.assertTrue(result['allowed'],result)
                props=e.permission_scope(entry,frozen)[1]
                self.assertIn({'dimension':'material','target':'coat_surface','property':'texture.surface'},props)
                self.assertEqual(result['dependencies'][0]['admission']['owner_resolution']['bindings'][0]['owner_id'],'coat_surface')
            from photo_shared_views import materialize_member
            self.assertEqual(materialize_member(data,{'candidate_id':B},realization_id='base',owner_selections=choice)['_native_owner_selections'],choice)

    def test_receiver_and_alias_use_exact_graph_and_atomic_presence(self):
        data=texture_source();p=data['candidates'][P]['content']['role_evidence'];p['facts'][-1]['receivers']=['receiver']
        p['owner_maps']['base']['bindings'].append({'target':'receiver','origin':'existing','introduced_by':None,'selector':{'kind':'selected_existing_owner'}})
        seal(data,{'texture':['cracks']},cid=P);c.validate(data)
        frozen=owner_core();choice=selections(data,frozen);choice['entries'][0]['bindings'].append({'target':'receiver','owner_id':'bench_surface'})
        entry=c.entry(data,P,realization_id='base',owner_selections=choice)
        self.assertTrue(e.admission(entry,frozen)['allowed']);self.assertEqual({x['target'] for x in e.permission_scope(entry,frozen)[1]},{'coat_surface','bench_surface'})
        frozen['intent_lock']['semantic_anchors'].append({'dimension':'material','target':'bench_surface','property':'texture.surface'});sign_core(frozen)
        choice=selections(data,frozen);choice['entries'][0]['bindings'].append({'target':'receiver','owner_id':'bench_surface'})
        self.assertFalse(g.core_entry_eligible(data,frozen,{}, {'subject':{}},'',c.entry(data,P,realization_id='base',owner_selections=choice)))
        data=texture_source();frozen=owner_core()
        frozen['semantic_assertions'] += [assertion('owner_alias','owner',owner='coat_alias',owner_kind='entity'),
            assertion('declared_alias','equivalent',left='coat_alias',right='coat_surface')];sign_core(frozen)
        self.assertTrue(e.admission(c.entry(data,P,realization_id='base',owner_selections=selections(data,frozen,'coat_alias')),frozen)['allowed'])

    def test_selection_bounds_64_entries_and_32_bindings_are_separate(self):
        data=texture_source();frozen=owner_core();choice=selections(data,frozen);template=choice['entries'][0]
        choice['entries']=[{**copy.deepcopy(template),'candidate_id':'cand_'+format(i,'032x')} for i in range(64)]
        self.assertEqual(len(e.validate_owner_selections(choice,frozen,e.frozen_witnesses(frozen)['graph'])),64)
        choice['entries'].append({**copy.deepcopy(template),'candidate_id':'cand_'+format(64,'032x')})
        self.assertRaises(ValueError,e.validate_owner_selections,choice,frozen,e.frozen_witnesses(frozen)['graph'])
        choice=selections(data,frozen);choice['entries'][0]['bindings']=[{'target':'surface_'+str(i),'owner_id':'coat_surface'} for i in range(32)]
        e.validate_owner_selections(choice,frozen,e.frozen_witnesses(frozen)['graph'])
        choice['entries'][0]['bindings'].append({'target':'surface_32','owner_id':'coat_surface'})
        self.assertRaises(ValueError,e.validate_owner_selections,choice,frozen,e.frozen_witnesses(frozen)['graph'])


class OwnerSelectionFinalAuditTests(unittest.TestCase):
    def test_missing_wrong_unused_and_post_audit_rebinding_are_rejected_without_pack_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            _,pack,data,query=owner_pack(Path(temp));self.addCleanup(data.reader.close);before=c.canonical_bytes(pack)
            original=chosen_composition(pack,data);report=audit.audit_composed_prompt(pack,original,source_data=data,query_context=query)
            self.assertEqual(report['status'],'pass',report)
            for defect in ['missing','wrong','unused','receipt_input','stale_graph','changed_prompt_receipt']:
                composed=copy.deepcopy(original)
                if defect=='missing':composed.pop('owner_selections')
                elif defect=='wrong':composed['owner_selections']['entries'][0]['bindings'][0]['owner_id']='main_subject'
                elif defect=='unused':composed['owner_selections']['entries'].append({**copy.deepcopy(composed['owner_selections']['entries'][0]),'candidate_id':B})
                elif defect=='receipt_input':composed['native_owner_resolution']=report['native_owner_resolution']
                elif defect=='stale_graph':composed['owner_selections']['owner_graph_sha256']='0'*64
                else:
                    composed['prompt_en']+=' A small additional reflection.'
                    composed['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(composed['prompt_en'].encode()).hexdigest()
                changed=audit.audit_composed_prompt(pack,composed,source_data=data,query_context=query)
                with self.subTest(defect=defect):
                    if defect=='changed_prompt_receipt':
                        self.assertEqual(changed['status'],'pass',changed)
                        self.assertNotEqual(changed['native_owner_resolution']['composed_sha256'],report['native_owner_resolution']['composed_sha256'])
                    else:self.assertEqual(changed['status'],'fail',changed)
            self.assertEqual(before,c.canonical_bytes(pack))

    def test_real_runtime_request_reaudits_exact_public_pack_and_composed_mapping(self):
        import audit_image_render_request as render
        with tempfile.TemporaryDirectory() as temp:
            _,pack,data,query=owner_pack(Path(temp));self.addCleanup(data.reader.close)
            composed=chosen_composition(pack,data)
            with audit.bound_native_source(data,query):
                report=audit.audit_composed_prompt(pack,composed);self.assertEqual(report['status'],'pass',report)
                receipt=report['native_owner_resolution']
                request={'native_owner_resolution_sha256':receipt['canonical_sha256'],'source_composed_sha256':receipt['composed_sha256']}
                # Other transport/reference checks remain active; assert this boundary specifically.
                result=render.audit_image_render_request(pack,composed,request)
                self.assertFalse(any(x['check']=='native_owner_resolution' for x in result['failures']),result)
                for field in ['native_owner_resolution_sha256','source_composed_sha256']:
                    bad={**request,field:'0'*64};result=render.audit_image_render_request(pack,composed,bad)
                    with self.subTest(field=field):self.assertTrue(any(x['check']=='native_owner_resolution' for x in result['failures']))
                changed=chosen_composition(pack,data,'bench_surface')
                result=render.audit_image_render_request(pack,changed,request)
                self.assertTrue(any(x['check']=='native_owner_resolution' for x in result['failures']))

class OwnerSelectionProfileTests(unittest.TestCase):
    def test_selected_profile_choices_keep_descriptor_and_strict_source_obligations(self):
        from tests.test_photo_native_v4_guards import profile_source,NativeV4ProfileTests
        data=profile_source();proof=data['candidates'][A]['content']['role_evidence']
        for mapping in proof['owner_maps'].values():
            mapping['schema']=e.SELECTOR_OWNER_SCHEMA
            for row in mapping['bindings']:
                role=row.pop('core_role');row['selector']={'kind':'selected_existing_owner'} if row['target']=='surface' else {'kind':'core_role','role':role}
        seal(data,{'light_direction':[f['id'] for f in proof['facts'] if f['mode']=='effect']});c.validate(data)
        frozen=owner_core();choices=NativeV4ProfileTests().choices(data,frozen)
        self.assertTrue(choices['profiles'][0]['choices'])
        alone=next(x for x in choices['profiles'][0]['choices'] if x['realization_id']=='alone')
        self.assertIn('owner_selection_requirements',alone)
        self.assertEqual(alone['owner_selection_requirements']['nodes'][0]['targets'],['surface'])
        selection=selections(data,frozen,cid=A,rid='alone')
        for rec in [data['candidates'][A],layout.guard_record(data['candidates'][A],data)]:
            entry=c.entry({**data,'candidates':{A:rec}},A,realization_id='alone',owner_selections=selection)
            self.assertTrue(e.admission(entry,frozen)['allowed'])
            self.assertEqual(e.permission_scope(entry,frozen)[1],[{'dimension':'lighting','target':'coat_surface','property':'lighting.direction'}])
            interpretation={'realization_id':'alone','selected_profile_contract':entry['_selected_profile_contract'],
                'selected_profile_evidence':{'side_light_phrase':'Side light grazes the declared linen surface from the left.'}}
            audit.audit_selected_native_profile(entry,interpretation,interpretation['selected_profile_evidence']['side_light_phrase'])
            interpretation['selected_profile_contract']['sha256']='0'*64
            self.assertRaises(ValueError,audit.audit_selected_native_profile,entry,interpretation,'Side light grazes the declared linen surface from the left.')
        pack={'native_profile_choices':choices,'authorial_core':frozen}
        audit.audit_native_profile_choices(pack,{'chosen_candidate_ids':[A]},data,{A},{A:{'realization_id':'alone'}})


class OwnerSelectionWorkflowTests(unittest.TestCase):
    def test_successful_audit_freezes_mapping_failed_audit_can_be_corrected_and_runtime_rechecks(self):
        from types import SimpleNamespace
        from tests.test_photo_workflow_precore import files
        from tests.test_photo_workflow_state import workflow
        import photo_workflow_worker as worker
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp);run,pack,data,query=owner_pack(directory);self.addCleanup(data.reader.close)
            with files.locked_state(run) as state:
                files.commit_stage(run,state,'pack_bound',{'pack':files.encode(pack),'runtime_receipt':files.encode({})})
            composed=chosen_composition(pack,data);path=directory/'composed.json'
            def direct_worker(state,**kwargs):
                return {'composed_audit':audit.audit_composed_prompt(files.value(state,'pack'),files.value(state,'composed'),source_data=data,query_context=query)}
            bad=copy.deepcopy(composed);bad.pop('owner_selections');path.write_text(json.dumps(bad))
            with mock.patch.object(worker,'audit_bound',side_effect=direct_worker):
                self.assertEqual(workflow.compose_audit(argparse.Namespace(run=run,composed=path))['status'],'fail')
                self.assertNotIn('composed',files.load_state(run)['artifacts'])
                path.write_text(json.dumps(composed));result=workflow.compose_audit(argparse.Namespace(run=run,composed=path))
                self.assertEqual(result['status'],'pass',result)
                self.assertEqual(workflow.compose_audit(argparse.Namespace(run=run,composed=path))['status'],'pass')
                changed=chosen_composition(pack,data,'bench_surface');path.write_text(json.dumps(changed))
                with self.assertRaisesRegex(ValueError,'owner_selection_rebinding_requires_new_run'):
                    workflow.compose_audit(argparse.Namespace(run=run,composed=path))
            parameters=directory/'parameters.json';parameters.write_text(json.dumps({'references':[]}))
            snapshot=SimpleNamespace(data=data,query_context=query)
            with mock.patch('photo_runtime_sources.RuntimeSnapshotProvider.from_receipt',return_value=snapshot):
                result=workflow.prepare_render(argparse.Namespace(run=run,parameters=parameters,lane='native',model=None,size=None))
                self.assertEqual(result['status'],'pass',result)
                state=files.load_state(run);request=files.value(state,'render_request');receipt=files.value(state,'composed_audit')['native_owner_resolution']
                self.assertEqual(request['native_owner_resolution_sha256'],receipt['canonical_sha256'])
                self.assertEqual(request['source_composed_sha256'],receipt['composed_sha256'])
                self.assertEqual(c.canonical_bytes(files.value(state,'pack')),c.canonical_bytes(pack))
                with files.locked_state(run) as state:
                    stored=files.value(state,'composed_audit');stored['native_owner_resolution']['canonical_sha256']='0'*64
                    files.commit_stage(run,state,'composition_audited',{'composed_audit':files.encode(stored)})
                result=worker.audit_bound(files.load_state(run),runtime=True)
                self.assertEqual(result['composed_audit']['status'],'fail')
                self.assertTrue(any(x['check']=='native_owner_resolution' for x in result['composed_audit']['failures']))
            parameters.write_text(json.dumps({'references':[],'native_owner_resolution_sha256':'0'*64}))
            with self.assertRaisesRegex(ValueError,'explicit_transport_parameters_required'):
                workflow.prepare_render(argparse.Namespace(run=run,parameters=parameters,lane='native',model=None,size=None))

class AtomicPrerequisiteTests(unittest.TestCase):
    def test_body_parts_exact_list_does_not_gain_subset_or_role_name_entailment(self):
        rows=[fact('parts','subject','carrier','body.parts','prerequisite',['mouth','lips'],[],quote='mouth and lips'),
            fact('light','lighting','carrier','lighting.direction','effect','side',['parts'],quote='Side light',operation='set_value',receivers=[])]
        mapping={'schema':e.SELECTOR_OWNER_SCHEMA,'bindings':[{'target':'carrier','origin':'existing','introduced_by':None,
            'selector':{'kind':'selected_existing_owner'}}]}
        data=seal(source('Side light reaches an existing carrier with mouth and lips.',rows,
            {'light_direction':slot('light_direction',['lighting'],property_prefixes=['lighting.direction'])},{'base':mapping}),{'light_direction':['light']})
        c.validate(data)
        for parts,allowed in [(['mouth','lips'],True),(['mouth','lips','eyes'],False),(['lips','mouth'],False)]:
            frozen=sign_core(core(['face_owner'],[('subject','face_owner','entity.presence','present'),('subject','face_owner','body.parts',parts)],role_bindings={}))
            choice=selections(data,frozen,'face_owner',cid=A);choice['entries'][0]['bindings'][0]['target']='carrier'
            for rec in [data['candidates'][A],layout.guard_record(data['candidates'][A],data)]:
                with self.subTest(parts=parts,compact='_semantic_evidence_guard' in rec):
                    entry=c.entry({**data,'candidates':{A:rec}},A,realization_id='base',owner_selections=choice)
                    self.assertEqual(e.admission(entry,frozen)['allowed'],allowed)


class OwnerSelectionOptionalBoundaryTests(unittest.TestCase):
    def test_pending_does_not_promote_incompatible_role(self):
        data=texture_source();data['slot_catalog']['light_direction']=slot('light_direction',['lighting'],property_prefixes=['lighting.'])
        seal(data,{'texture':['cracks']},cid=P)
        proposal=roles.propose(data,'light_direction',P,[])
        self.assertEqual(proposal['applicability_status'],'incompatible')
        self.assertEqual(proposal['semantic_fit']['reason'],'reviewed_complete_meaning_does_not_support_role')

    def test_optional_selector_child_is_not_required_when_its_parent_alone_is_adopted(self):
        from tests.photo_native_runtime import compose_native
        phrase='A cracked texture accents the existing linen blanket.'
        f=fact('parent_cracks','material','surface','texture.surface','effect','cracked',['parent_linen'],quote=phrase,operation='set_value',receivers=[])
        data=source(phrase,[fact('parent_linen','material','surface','surface.material','prerequisite','linen',[],quote='existing linen blanket'),f],{'texture':slot('texture',['material'],property_prefixes=['texture.'])},
            {'base':owner_map(('surface','main_subject'))})
        rec=data['candidates'].pop(A);rec['id']=P;rec['record_kind']='visual_bundle';data['candidates'][P]=rec
        rec['content']['components']=[{'id':'parent_texture','concept_units':[phrase],'minimum_realizations':1}]
        other=copy.deepcopy(f);other.update(id='component_cracks',pointer='/content/components/0/concept_units/0')
        rec['content']['role_evidence']['facts'].append(other)
        child=texture_source(B);data['candidates'][B]=child['candidates'][B]
        seal(data,{'texture':['cracks']},cid=B)
        rec['content']['member_candidates']=[{'candidate_id':B,'adoption':'optional','requirements':{}}]
        dependencies(data,P,'base',[B]);rec['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
        seal(data,{'texture':['parent_cracks','component_cracks']},cid=P);c.validate(data)
        with tempfile.TemporaryDirectory() as temp:
            _,pack,runtime,query=owner_pack(Path(temp),data,bundle_refs=[P]);self.addCleanup(runtime.reader.close)
            self.assertIn('owner_selection_requirements',pack['candidate_pool'][P])
            composed=compose_native(pack);evidence=phrase+' Subtle raking highlights reveal fine ridges.';composed['prompt_en']+=' '+evidence;composed['chosen_candidate_ids']=[P]
            interpretation={'candidate_id':P,'artistic_interpretation':'Keep the independently declared linen carrier.',
                'transformation':'Use the directly authored fine texture.', 'prompt_evidence':evidence,'realization_id':'base',
                'affected_properties':[{'dimension':'material','target':'main_subject','property':'texture.surface'}],
                'component_evidence':{'parent_texture':evidence},'relation_evidence':{}}
            composed['candidate_interpretations']=[interpretation]
            for decision in composed['creative_augmentation_brief']['decisions']:
                if decision['candidate_id']==P:
                    decision.update(interpretation,decision='transformed',rationale='Retain only the parent texture.',affected_dimensions=['material'])
                    composed['candidate_interpretations']=[]
            composed['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(composed['prompt_en'].encode()).hexdigest()
            result=audit.audit_composed_prompt(pack,composed,source_data=runtime,query_context=query)
            self.assertEqual(result['status'],'pass',result)
            self.assertNotIn('native_owner_resolution',result)
            chosen=composed['candidate_interpretations'] or [row for row in composed['creative_augmentation_brief']['decisions'] if row['candidate_id']==P]
            chosen[0]['dependency_selections']={B:'base'}
            result=audit.audit_composed_prompt(pack,composed,source_data=runtime,query_context=query)
            self.assertEqual(result['status'],'fail',result)
            child_evidence='Subtle raking highlights expose cracked texture on the existing secondary leather coat.'
            composed['prompt_en']+=' '+child_evidence
            composed['owner_selections']=selections(data,pack['authorial_core'],cid=B)
            chosen[0]['affected_properties'].append({'dimension':'material','target':'coat_surface','property':'texture.surface'})
            composed['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(composed['prompt_en'].encode()).hexdigest()
            result=audit.audit_composed_prompt(pack,composed,source_data=runtime,query_context=query)
            self.assertEqual(result['status'],'pass',result)
            self.assertEqual([row['candidate_id'] for row in result['native_owner_resolution']['nodes']],[B])
            self.assertEqual(len(result['native_owner_resolution']['selected_closures'][0]['effect_closure']),2)
