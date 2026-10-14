"""Candidate-independent requests declared before loading the fresh source proof."""
import copy,gzip,hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
GEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/2ad7b2bfd3f4d730985c23ed89e3513a326a0a2ceea22aecfe28cb5d05c98ac9')
sys.path[:0]=[str(GEN/'scripts'),str(GEN/'precore')]
import photo_semantic_evidence as s
import photo_candidate_corpus as c
import photo_search_layout as layout
import prompt_generator as g

def assertion(aid,kind,dimension='subject',**axes):
    return {'assertion_id':aid,'dimension':dimension,'polarity':'required','source_span_ids':['request'],
            'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},
            'evidence':{'literal':TEXT},'affected_dimensions':[dimension]}

def core(state,*,overlap=False,other=False):
    global TEXT
    TEXT='The main subject is an already established adult human person A. The outfit, posture and activity remain open.'
    if state=='known_present':TEXT+=' Existing reference appearance fixes black hair, and requester identity is person_A. Preserve both.'
    elif state=='known_absent':TEXT+=' No reference appearance or requester-fixed identity is established.'
    else:TEXT+=' The presence or absence of reference appearance and requester-fixed identity has not been reviewed.'
    if overlap:TEXT+=' The already specified pencil-skirt outfit is fixed as part of reference appearance.'
    if other:TEXT+=' Another already established person B is a different person.'
    sha=hashlib.sha256(TEXT.encode()).hexdigest()
    request={'request_sha256':sha,'request_envelope_sha256':hashlib.sha256(('independent request envelope '+TEXT).encode()).hexdigest(),
             'input_inventory':{'schema':'photo-request-input-inventory/v1','complete':True,'items':[{'id':'request','kind':'request_text','sha256':sha}]},
             'active_spans':[{'source_span_id':'request','text':TEXT}]}
    rows=[assertion('owner','owner',owner='person_A',owner_kind='human'),
          assertion('role','role',owner='person_A',role='main_subject'),
          assertion('presence','fact',owner='person_A',property='entity.presence',value_type='entity.presence/v1',value='present'),
          assertion('adult','fact',dimension='age',owner='person_A',property='age.declared',value_type='age.declared/v1',value='adult')]
    if other:rows.append(assertion('other','owner',owner='person_B',owner_kind='human'))
    anchors=[]
    if state=='known_present':
        rows += [assertion('hair_color','fact',dimension='appearance',owner='person_A',property='appearance.hair_color',value_type='appearance.hair_color/v1',value='black',scope_kinds=['reference_appearance'],source_input_ids=['request']),
                 assertion('identity','fact',dimension='identity',owner='person_A',property='subject.identity',value_type='subject.identity/v1',value='person_A',scope_kinds=['requester_identity'],source_input_ids=['request'])]
        anchors.append({'dimension':'appearance','target':'person_A','property':'appearance.hair_color'})
    if overlap:
        rows.append(assertion('fixed_wardrobe','fact',dimension='appearance',owner='person_A',property='wardrobe.ensemble',value_type='wardrobe.ensemble/v1',value='pencil_skirt',scope_kinds=['reference_appearance'],source_input_ids=['request']))
        anchors.append({'dimension':'appearance','target':'person_A','property':'wardrobe.ensemble'})
    frozen={'contract_version':'photo-authorial-core/v3','subject':TEXT,'baseline_prompt_en':TEXT,'request_binding':request,
            'semantic_assertions':rows,'user_exclusions':[],
            'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['subject','age','identity','count','concept'],
                           'open_dimensions':['appearance','pose','action','camera','lighting','material','composition','timing','event','relationship','role','body_geometry'],'semantic_anchors':anchors}}
    for scope in ['reference_appearance','requester_identity']:
        facts=s.frozen_witnesses(frozen)['facts']
        items=[{k:x[k] for k in ['assertion_id','dimension','target','property','value']} for x in facts if scope in x.get('scope_kinds',[])]
        inventory={'schema':'photo-frozen-scope-inventory/v1','complete':True,'input_binding':s.witnesses.input_binding(request),
                   'reviewed_input_ids':['request'],'state':state,'items':items}
        rows.append(assertion('scope_'+scope,'scope_inventory',owner='person_A',scope_kind=scope,inventory=s.witnesses.canonical(inventory)))
    s.frozen_witnesses(frozen)
    return frozen

# These requester requirements are fully declared independently, before any
# candidate/old proof is loaded. No core value is copied from a candidate.
CORES={state:core(state) for state in ['known_absent','known_present','unknown']}
CORES['same_value_overlap']=core('known_present',overlap=True)
CORES['other']=core('known_present',other=True)
CASES=[('known_absent',CORES['known_absent'],True),('known_present',CORES['known_present'],True),
       ('unknown',CORES['unknown'],False),('same_value_overlap',CORES['same_value_overlap'],False)]
for defect in ['presence_absent','adult_absent','adult_wrong_value','presence_wrong_owner','adult_wrong_owner','role_absent',
               'scope_absent','scope_wrong_owner','scope_wrong_item_value','scope_incomplete','input_stale','reviewed_input_missing','input_inventory_absent']:
    frozen=copy.deepcopy(CORES['other'] if defect.endswith('wrong_owner') and not defect.startswith('scope') else CORES['known_present'])
    if defect in ['presence_absent','adult_absent','role_absent']:
        frozen['semantic_assertions']=[x for x in frozen['semantic_assertions'] if x['assertion_id']!=defect.split('_')[0]]
    elif defect=='adult_wrong_value':next(x for x in frozen['semantic_assertions'] if x['assertion_id']=='adult')['axes']['value']='child'
    elif defect in ['presence_wrong_owner','adult_wrong_owner']:
        next(x for x in frozen['semantic_assertions'] if x['assertion_id']==defect.split('_')[0])['axes']['owner']='person_B'
        s.frozen_witnesses(frozen)
    elif defect=='scope_absent':frozen['semantic_assertions']=[x for x in frozen['semantic_assertions'] if x['axes']['kind']!='scope_inventory']
    elif defect=='input_inventory_absent':frozen['request_binding'].pop('input_inventory')
    else:
        row=next(x for x in frozen['semantic_assertions'] if x['assertion_id']=='scope_reference_appearance');payload=json.loads(row['axes']['inventory'])
        if defect=='scope_wrong_owner':row['axes']['owner']='unbound_other'
        elif defect=='scope_wrong_item_value':payload['items'][0]['value']['value']='white'
        elif defect=='scope_incomplete':payload['complete']=False
        elif defect=='input_stale':payload['input_binding']['input_inventory_sha256']='0'*64
        elif defect=='reviewed_input_missing':payload['reviewed_input_ids']=[]
        row['axes']['inventory']=s.witnesses.canonical(payload)
    CASES.append((defect,frozen,False))

M=runpy.run_path(str(Path(__file__).with_name('native_fresh_08250_11128_05.py')))
sys.path[:0]=[str(GEN/'scripts'),str(GEN/'precore')]
CID=M['CID'];CAT=M['CAT'];PROOF=M['PROOF'];P=M['P'];O=M['O'];nr=M['nr'];I=M['I']
AFTER=copy.deepcopy(M['AFTER']);AFTER['content']['role_evidence']=PROOF
current=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()))
OWN={bid:b for bid,b in current['slot_bindings'].items() if b['candidate_id']==CID};BID=next(iter(OWN))
CORPUS={'slot_catalog':CAT,'slot_bindings':OWN,'candidates':{CID:AFTER}}
s.validate(AFTER,CAT,corpus=CORPUS)
GUARDED={**CORPUS,'candidates':{CID:layout.guard_record(AFTER,CORPUS)}}
RESULT=[];LOCKS=[];AUDITS=[];BINDING=[];SHAPE_NEGATIVES=[]
contract={'adult_allowed':True,'subject_category':'human','intent_constraints':{'subject_categories':['human'],'domains':[]},'domains':[]}
picked={'subject':{'tags':['human']}}
for rid in ['standing','walking']:
    compact=c.entry(GUARDED,CID,BID,realization_id=rid)
    full=c.entry(CORPUS,CID,BID,realization_id=rid);full['_semantic_evidence_guard']=PROOF
    for form,entry in [('full',full),('compact',compact)]:
        for name,frozen,expected in CASES:
            receipt=s.admission(entry,frozen);eligible=g.core_entry_eligible(CORPUS,frozen,contract,picked,'wardrobe_style',entry)
            assert receipt['allowed'] is expected,(rid,form,name,receipt)
            assert eligible is expected,(rid,form,name,'whole_consumer',eligible)
            RESULT.append({'rid':rid,'form':form,'case':name,'allowed':receipt['allowed'],'whole_consumer_allowed':eligible})
        good=CORES['known_present'];receipt=s.admission(entry,good)
        prompt='The previously established black hair color and person_A requester identity remain unchanged.'
        evidence={'scope_preservation_evidence':{'scope_reference_appearance':{'hair_color':{'owner':'person_A','value':{'type':'appearance.hair_color/v1','value':'black'},'prompt_evidence':prompt}},
                   'scope_requester_identity':{'identity':{'owner':'person_A','value':{'type':'subject.identity/v1','value':'person_A'},'prompt_evidence':prompt}}}}
        s.audit_scope_preservation(receipt,evidence,prompt);AUDITS.append({'rid':rid,'form':form,'case':'exact_final_preservation','passed':True})
        for defect in ['missing','wrong_owner','wrong_value','nonliteral']:
            bad=copy.deepcopy(evidence)
            if defect=='missing':bad={}
            elif defect=='wrong_owner':bad['scope_preservation_evidence']['scope_reference_appearance']['hair_color']['owner']='person_B'
            elif defect=='wrong_value':bad['scope_preservation_evidence']['scope_reference_appearance']['hair_color']['value']['value']='white'
            else:bad['scope_preservation_evidence']['scope_reference_appearance']['hair_color']['prompt_evidence']='invented absent phrase'
            try:s.audit_scope_preservation(receipt,bad,prompt)
            except ValueError:AUDITS.append({'rid':rid,'form':form,'case':defect,'rejected':True})
            else:raise AssertionError(('preservation_not_rejected',rid,form,defect))
        for dimension,prop in [('appearance','wardrobe.ensemble'),('pose','body.pose')]+([('action','action.walking')] if rid=='walking' else []):
            for kind in ['whole_dimension','exact_property','same_value_property']:
                frozen=copy.deepcopy(CORES['known_absent'])
                if kind=='whole_dimension':
                    frozen['intent_lock']['open_dimensions'].remove(dimension);frozen['intent_lock']['locked_dimensions'].append(dimension)
                else:frozen['intent_lock']['semantic_anchors']=[{'dimension':dimension,'target':'person_A','property':prop}]
                if kind=='same_value_property':
                    value={'wardrobe.ensemble':'pencil_skirt','body.pose':'natural_'+rid,'action.walking':'walking'}[prop]
                    # A requester-owned existing exact value is independently
                    # declared; matching it never grants mutation permission.
                    frozen['semantic_assertions'].append({'assertion_id':'fixed_value','dimension':dimension,'polarity':'required','source_span_ids':['request'],
                        'axes':{'native_schema':'photo-frozen-semantics/v1','kind':'fact','owner':'person_A','property':prop,'value_type':prop+'/v1','value':value},
                        'evidence':{'literal':frozen['baseline_prompt_en']},'affected_dimensions':[dimension]})
                    if dimension not in frozen['intent_lock']['locked_dimensions']:frozen['intent_lock']['locked_dimensions'].append(dimension)
                assert not g.core_entry_eligible(CORPUS,frozen,contract,picked,'wardrobe_style',entry)
                LOCKS.append({'rid':rid,'form':form,'kind':kind,'dimension':dimension,'property':prop,'rejected':True})
        for case,override in [('adult_guard_false',{'adult_allowed':False}),('wrong_category',{'subject_category':'object'}),
                              ('denied_product_domain',{'domains':['product'],'intent_constraints':{'subject_categories':['human'],'domains':['product']}})]:
            assert not g.core_entry_eligible(CORPUS,CORES['known_absent'],{**contract,**override},picked,'wardrobe_style',entry)
            BINDING.append({'rid':rid,'form':form,'case':case,'rejected':True})

# Fresh signatures let structural adversaries reach the intended check; they
# never repair meaning. No altered proof is written as a new source artifact.
for defect in ['missing_direct_anchor','reference_self','reference_foreign_rid','missing_pose_ko_natural_quote','stale_relation_signature']:
    bad=copy.deepcopy(AFTER);proof=bad['content']['role_evidence']
    if defect=='missing_direct_anchor':
        proof['source_units']=[u for u in proof['source_units'] if not(u['realization_id']=='standing' and u['pointer']=='/content/realization_content/standing/en' and u['disposition']=='semantic')]
    elif defect=='reference_self':
        next(u for u in proof['source_units'] if u['disposition']=='semantic_reference' and u['pointer']=='/content/realization_content/standing/ko')['fact_refs']=['standing_pose_ko']
    elif defect=='reference_foreign_rid':next(u for u in proof['source_units'] if u['disposition']=='semantic_reference')['fact_refs']=['walking_adult']
    elif defect=='missing_pose_ko_natural_quote':
        next(f for f in proof['facts'] if f['id']=='standing_pose_ko')['quote']='absent naturalness qualifier'
    else:next(u for u in proof['source_units'] if u['disposition']=='semantic_reference')['retained_constraint_rationale']='Changed manual interpretation without fresh signature.'
    if defect!='stale_relation_signature':proof['review']['native_review']['native_contract_sha256']=s.native_contract_sha256(proof)
    try:s.validate(bad,CAT,corpus={**CORPUS,'candidates':{CID:bad}})
    except ValueError:SHAPE_NEGATIVES.append({'case':defect,'rejected':True})
    else:raise AssertionError(('shape_not_rejected',defect))

verification=nr.verify_batch(P/'ASSIGNMENT.json',O/'BATCH.json',O/'NOTE.json')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
modules={name:{'file':str(Path(mod.__file__).resolve()),'raw_sha256':sha(mod.__file__)} for name,mod in sorted(sys.modules.items()) if getattr(mod,'__file__',None) and (name.startswith('photo_') or name in {'prompt_generator','audit_composed_prompt','visual_profile_contracts'})}
for name,row in modules.items():assert Path(row['file']).is_relative_to(GEN),(name,row['file'])
REPORT={'schema':'photo-native-fresh-special-check/v1','task_name':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high',
        'candidate_id':CID,'ordinal':11128,'frozen_generation':GEN.name,'actual_loaded_modules':modules,
        'candidate_independent_requests_built_before_candidate_proof_load':True,'core_fixtures':CORES,'facts':len(PROOF['facts']),'units':len(PROOF['source_units']),
        'full_compact_admission_and_consumer_cases':RESULT,'property_and_whole_locks':LOCKS,'final_preservation_cases':AUDITS,'original_binding_consumers':BINDING,
        'reference_and_anchor_shape_negatives':SHAPE_NEGATIVES,'verify_batch':verification,
        'source_after_exact_input':M['AFTER']==M['PACK']['current_records'][CID],'shape_does_not_prove_semantic_entailment_or_pixels':True,
        'network_denied':True,'operating_native_qualified_count':0}
out=R/'authored/native_fresh_08250_11128_05_checks.json';assert not out.exists();out.write_text(json.dumps(REPORT,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'admission_and_whole_cases':len(RESULT),'lock_cases':len(LOCKS),'final_preservation':len(AUDITS),'actual_binding':len(BINDING),'shape_negatives':len(SHAPE_NEGATIVES),'report_raw_sha256':sha(out),'batch_raw_sha256':sha(O/'BATCH.json'),'verify_batch':verification.get('shape_valid')}))
