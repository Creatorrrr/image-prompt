"""Candidate-free freeze, independent audit and replay of native typed witnesses."""
import argparse
import copy
import json
from pathlib import Path
import tempfile
import unittest
from tests.test_photo_workflow_precore import FIXTURE, preparation, files
from tests.test_photo_semantic_evidence import assertion, fact, source, owner_map, seal, A
from tests.photo_native_schema import slot
import photo_semantic_evidence as e
import photo_search_layout as layout
import photo_candidate_corpus as c
import prompt_generator as g
import audit_composed_prompt as audit


class NativeFactWireTests(unittest.TestCase):
    def inputs(self):
        raw=json.loads((FIXTURE/'authorial-core.json').read_bytes());raw.pop('creative_controls_sha256')
        owner=assertion('blanket_owner','owner',owner='main_subject',owner_kind='blanket')
        linen=assertion('blanket_material','fact',dimension='material',owner='main_subject',
            property='surface.material',value_type='surface.material/v1',value='linen')
        role=assertion('blanket_role','role',role='main_subject',owner='main_subject')
        for row in [owner,role,linen]:
            row['source_span_ids']=['topic'];row['evidence']={'material':'linen blanket'}
        raw['semantic_assertions'] += [owner,role,linen]
        raw['intent_lock']['locked_dimensions'].append('material')
        raw['intent_lock']['open_dimensions'].remove('material')
        raw['intent_lock']['semantic_anchors'].append({'anchor_id':'declared_linen',
            'source_text':'linen blanket','dimension':'material','prompt_evidence':'fine fibers'})
        return raw

    def freeze(self,directory,raw,request_text=None,control_overrides=None,selection_override=None,input_inventory=None):
        request=json.loads((FIXTURE/'request-envelope.json').read_bytes())
        if request_text is not None:
            request['request_text']=request_text;request['active_spans'][0]['end']=len(request_text)
        request_path=directory/'request';request_path.write_text(request['request_text'])
        spans=directory/'spans';spans.write_text(json.dumps([{key:row[key] for key in ['span_id','start','end']} for row in request['active_spans']]))
        run=directory/'run'
        inventory_path=None
        if input_inventory is not None:
            inventory_path=directory/'input-inventory.json';inventory_path.write_text(json.dumps(input_inventory))
        preparation.init(argparse.Namespace(input_inventory=inventory_path,request=request_path,spans=spans,whole_request=False,
            request_id=request['request_id'],run=run,mode='prompt_only'))
        controls=json.loads((FIXTURE/'creative-controls.json').read_bytes())
        context=directory/'context';context.write_text(json.dumps(controls['context']))
        overrides=directory/'overrides';overrides.write_text(json.dumps({**{key:row['value'] for key,row in controls['controls'].items()},**(control_overrides or {})}))
        preparation.controls(argparse.Namespace(run=run,context=context,overrides=overrides,seed=17))
        payloads={'core':raw,'selection':{'selected':json.loads((FIXTURE/'precore_feature_selection.json').read_bytes())['selected']},
                  'review':json.loads((FIXTURE/'embodiment-review.json').read_bytes())}
        if selection_override is not None:payloads['selection']={'selected':selection_override}
        payloads['review'].pop('prompt_sha256')
        paths={}
        for kind,value in payloads.items():
            paths[kind]=directory/(kind+'.json');paths[kind].write_text(json.dumps(value))
        args=argparse.Namespace(run=run,**paths);preparation.freeze(args)
        return run,args

    def test_candidate_free_build_independent_audit_and_raw_wire_receipt_replay(self):
        raw=self.inputs()
        with tempfile.TemporaryDirectory() as temp:
            run,args=self.freeze(Path(temp),raw);state=files.load_state(run)
            envelope,frozen,controls=files.verify_freeze(state)
            self.assertEqual(frozen['semantic_assertions'][-2:],raw['semantic_assertions'][-2:])
            self.assertTrue(audit.authorial_core_v3_semantic_contract_valid(frozen,creative_control_snapshot=controls))
            self.assertTrue(preparation.freeze(args)['reused'])
            self.assertEqual(files.verify_freeze(files.load_state(run))[1],frozen)
            replay=g.normalize_authorial_core(files.value(state,'authorial_core_input'),
                request_envelope=envelope,creative_control_snapshot=controls)
            self.assertEqual(replay['canonical_sha256'],frozen['canonical_sha256'])
            before=e.frozen_witnesses(frozen);after=e.frozen_witnesses(json.loads(json.dumps(frozen)))
            self.assertEqual(before,after)
            self.assertEqual(before['facts'][-1]['value'],{'type':'surface.material/v1','value':'linen'})

    def test_native_prerequisite_and_actual_light_effect_reach_full_runtime_permission_hook(self):
        with tempfile.TemporaryDirectory() as temp:
            run,_=self.freeze(Path(temp),self.inputs());_,frozen,controls=files.verify_freeze(files.load_state(run))
            rows=[fact('linen','material','main_subject','surface.material','prerequisite','linen',[],quote='linen'),
                  fact('side','lighting','main_subject','lighting.direction','effect','side',['linen'],
                       quote='side light',operation='set_value',receivers=[])]
            data=seal(source('side light on the already declared linen surface',rows,
                {'light_direction':slot('light_direction',['lighting'],property_prefixes=['lighting.direction'])},
                {'base':owner_map(('main_subject','main_subject'))}),{'light_direction':['side']});c.validate(data)
            contract,picked=g.frozen_core_context(data,frozen,controls)
            decisions=[]
            for view in [data,{**data,'candidates':{A:layout.guard_record(data['candidates'][A],data)}}]:
                entry=c.entry(view,A)
                decisions.append(g.core_entry_eligible(view,frozen,contract,picked,'',entry))
                receipt=e.admission(entry,frozen)
                self.assertEqual(receipt['resolved_frozen_facts'][0]['core_assertion_id'],'blanket_material')
                self.assertEqual(json.loads(json.dumps(receipt)),receipt)
            self.assertEqual(decisions,[True,True])
            locked=copy.deepcopy(frozen);locked['intent_lock']['open_dimensions'].remove('lighting')
            self.assertFalse(g.core_entry_eligible(data,locked,contract,picked,'',c.entry(data,A)))

    def test_independent_auditor_rejects_invalid_owner_alias_and_value_coercion(self):
        with tempfile.TemporaryDirectory() as temp:
            run,_=self.freeze(Path(temp),self.inputs());_,frozen,controls=files.verify_freeze(files.load_state(run))
            for defect in ['coercion','dangling_owner','foreign_span','unknown_schema']:
                value=copy.deepcopy(frozen);row=value['semantic_assertions'][-1]
                if defect=='coercion':row['axes']['value']={'literal':'linen'}
                elif defect=='dangling_owner':row['axes']['owner']='unbound_blanket'
                elif defect=='foreign_span':row['source_span_ids']=['missing']
                else:row['axes']['native_schema']='photo-frozen-semantics/v0'
                with self.subTest(defect=defect):
                    self.assertFalse(audit.authorial_core_v3_semantic_contract_valid(value,creative_control_snapshot=controls))


    def test_real_multiowner_freeze_exceeds_old_sixteen_row_limit_without_merging_owners(self):
        raw=self.inputs()
        statement='Alice and Bea each have a face, hands, a jacket and a mug beside the blanket.'
        request=raw['source_request']+' '+statement
        raw['source_request']=request;raw['baseline_prompt_en']+=' '+statement
        declarations=[('Alice','person','secondary_subject'),('Bea','person','relationship_target'),
            ('Alice-face','face','primary_face'),('Bea-face','face','secondary_face'),
            ('Alice-hands','hands','primary_hands'),('Bea-hands','hands','secondary_hands'),
            ('Alice-jacket','garment','primary_garment'),('Bea-jacket','garment','secondary_garment'),
            ('Alice-mug','prop','primary_prop'),('Bea-mug','prop','secondary_prop')]
        rows=[]
        for i,(owner,kind,role) in enumerate(declarations):
            rows += [assertion('multi_owner_'+str(i),'owner',owner=owner,owner_kind=kind),
                     assertion('multi_role_'+str(i),'role',role=role,owner=owner)]
        for i,(part,actor) in enumerate([('Alice-face','Alice'),('Bea-face','Bea'),('Alice-hands','Alice'),('Bea-hands','Bea'),
                    ('Alice-jacket','Alice'),('Bea-jacket','Bea'),('Alice-mug','Alice'),('Bea-mug','Bea')]):
            rows.append(assertion('multi_part_'+str(i),'part_of',left=part,right=actor))
        rows.append(assertion('multi_disjoint','disjoint',left='Alice',right='Bea'))
        for i,owner in enumerate(['Alice-face','Bea-face']):
            rows.append(assertion('multi_face_'+str(i),'fact',owner=owner,property='anatomy.face.presence',
                value_type='anatomy.face.presence/v1',value='present'))
        for row in rows:row['source_span_ids']=['topic'];row['evidence']={'declared_scene':statement}
        raw['semantic_assertions']+=rows
        self.assertGreater(len(raw['semantic_assertions']),16)
        with tempfile.TemporaryDirectory() as temp:
            run,args=self.freeze(Path(temp),raw,request);env,frozen,controls=files.verify_freeze(files.load_state(run))
            self.assertEqual(frozen['semantic_assertions'],raw['semantic_assertions'])
            self.assertTrue(audit.authorial_core_v3_semantic_contract_valid(frozen,creative_control_snapshot=controls))
            self.assertTrue(preparation.freeze(args)['reused'])
            graph=e.frozen_witnesses(frozen)['graph'];self.assertEqual(len(graph['owners']),11)
            self.assertEqual(graph['roles']['secondary_face'],'Bea-face')
            self.assertEqual(e.witnesses.owner_relation(graph,'primary_face','secondary_face'),'disjoint')
            self.assertEqual(g.normalize_authorial_core(files.value(files.load_state(run),'authorial_core_input'),
                request_envelope=env,creative_control_snapshot=controls)['canonical_sha256'],frozen['canonical_sha256'])

    def white_garment_selection(self):
        selection=json.loads((FIXTURE/'precore_feature_selection.json').read_bytes())['selected']
        selection[0].update(source_text='white linen robe',baseline_evidence='white linen robe',
            reason='The explicitly requested robe is the primary subject.')
        return selection

    def white_garment_inputs(self):
        # A separately authored user fixture: the blanket study becomes a white
        # linen robe study. Only color is prescribed within open appearance.
        raw=json.loads(json.dumps(self.inputs()).replace('linen blanket','white linen robe').replace('blanket','robe'))
        raw['semantic_assertions'][1]['axes']['owner_kind']='garment'
        role=assertion('garment_role','role',role='primary_garment',owner='main_subject')
        white=assertion('garment_white','fact',dimension='appearance',owner='main_subject',
            property='wardrobe.color',value_type='wardrobe.color/v1',value='white')
        for row in [role,white]:row['source_span_ids']=['topic'];row['evidence']={'garment':'white linen robe'}
        raw['semantic_assertions'] += [role,white]
        raw['intent_lock']['open_dimensions'].append('appearance')
        raw['intent_lock']['semantic_anchors'].append({'anchor_id':'white_garment',
            'source_text':'white linen robe','dimension':'appearance','target':'primary_garment',
            'property':'wardrobe.color','prompt_evidence':'white linen robe'})
        return raw

    def test_requester_partial_color_lock_freezes_white_fact_without_closing_neckline(self):
        raw=self.white_garment_inputs()
        with tempfile.TemporaryDirectory() as temp:
            run,args=self.freeze(Path(temp),raw,raw['source_request'],selection_override=self.white_garment_selection());env,frozen,controls=files.verify_freeze(files.load_state(run))
            self.assertIn('appearance',frozen['intent_lock']['open_dimensions'])
            self.assertNotIn('appearance',frozen['intent_lock']['locked_dimensions'])
            self.assertTrue(audit.authorial_core_v3_semantic_contract_valid(frozen,creative_control_snapshot=controls))
            self.assertTrue(preparation.freeze(args)['reused'])
            self.assertEqual(g.normalize_authorial_core(files.value(files.load_state(run),'authorial_core_input'),
                request_envelope=env,creative_control_snapshot=controls)['canonical_sha256'],frozen['canonical_sha256'])
            white=fact('white','appearance','garment','wardrobe.color','prerequisite','white',[],quote='white garment')
            neckline=fact('round','appearance','garment','wardrobe.neckline','effect','round',['white'],
                quote='round neckline',operation='set_value',receivers=[])
            data=seal(source('round neckline on the already white garment',[white,neckline],
                {'neckline':slot('neckline',['appearance'],property_prefixes=['wardrobe.neckline'])},
                {'base':owner_map(('garment','primary_garment'))}),{'neckline':['round']});c.validate(data)
            contract,picked=g.frozen_core_context(data,frozen,controls)
            receipts=[]
            for record in [data['candidates'][A],layout.guard_record(data['candidates'][A],data)]:
                view={**data,'candidates':{A:record}};entry=c.entry(view,A)
                receipts.append(e.admission(entry,frozen))
                self.assertTrue(g.core_entry_eligible(view,frozen,contract,picked,'',entry))
            self.assertEqual(receipts[0],receipts[1]);self.assertTrue(receipts[0]['allowed'])
            blue=fact('blue','appearance','garment','wardrobe.color','effect','blue',['white'],
                quote='blue',operation='set_value',receivers=[])
            color=seal(source('change the existing white garment to blue',[copy.deepcopy(white),blue],
                {'color':slot('color',['appearance'],property_prefixes=['wardrobe.color'])},
                {'base':owner_map(('garment','primary_garment'))}),{'color':['blue']});c.validate(color)
            self.assertTrue(e.admission(c.entry(color,A),frozen)['allowed'])
            self.assertFalse(g.core_entry_eligible(color,frozen,contract,picked,'',c.entry(color,A)))

    def test_partial_lock_requires_same_owner_and_nonbroader_fact_on_all_three_consumers(self):
        from photo_precore_bridge import load
        wire=load('photo_authoring_wire');raw=self.white_garment_inputs()
        with tempfile.TemporaryDirectory() as temp:
            run,_=self.freeze(Path(temp),raw,raw['source_request'],selection_override=self.white_garment_selection());_,frozen,controls=files.verify_freeze(files.load_state(run))
            for defect in ['no_anchor','wrong_owner','broader_property','advisory','part_only']:
                value=copy.deepcopy(frozen)
                if defect=='no_anchor':value['intent_lock']['semantic_anchors']=[row for row in value['intent_lock']['semantic_anchors'] if 'property' not in row]
                elif defect=='wrong_owner':value['intent_lock']['semantic_anchors'][-1]['target']='secondary_garment'
                elif defect=='broader_property':value['semantic_assertions'][-1]['axes']['property']='wardrobe'
                elif defect=='advisory':value['semantic_assertions'][-1]['polarity']='advisory'
                else:
                    owner=assertion('different_part','owner',owner='garment_part',owner_kind='garment')
                    part=assertion('part_relation','part_of',left='garment_part',right='main_subject')
                    for row in [owner,part]:row['source_span_ids']=['topic'];row['evidence']={'garment':'white linen robe'}
                    value['semantic_assertions'] += [owner,part]
                    value['semantic_assertions'][-3]['axes']['owner']='garment_part'
                with self.subTest(defect=defect):
                    self.assertRaises(ValueError,wire.normalize_semantic_assertions,value['semantic_assertions'],
                        envelope={'active_spans':value['request_binding']['active_spans']},intent_lock=value['intent_lock'],
                        baseline_prompt_en=value['baseline_prompt_en'])
                    self.assertFalse(audit.authorial_core_v3_semantic_contract_valid(value,creative_control_snapshot=controls))
                    self.assertRaises(ValueError,e.frozen_witnesses,value)
            # Explicit neutral role + exact equivalence can protect the same
            # property; an owned part above was deliberately insufficient.
            alias=copy.deepcopy(frozen)
            owner=assertion('alias_owner','owner',owner='garment_alias',owner_kind='garment')
            relation=assertion('same_garment','equivalent',left='garment_alias',right='main_subject')
            for row in [owner,relation]:row['source_span_ids']=['topic'];row['evidence']={'garment':'white linen robe'}
            alias['semantic_assertions'] += [owner,relation]
            alias['semantic_assertions'][-3]['axes']['owner']='garment_alias'
            self.assertTrue(e.frozen_witnesses(alias))
            self.assertTrue(audit.authorial_core_v3_semantic_contract_valid(alias,creative_control_snapshot=controls))
