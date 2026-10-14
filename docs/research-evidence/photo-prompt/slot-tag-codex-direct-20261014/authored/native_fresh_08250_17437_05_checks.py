"""Fresh05 independent literal cores and frozen consumers; research qualification only."""
import copy,hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
GEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb')
sys.path[:0]=[str(GEN/'scripts'),str(GEN/'precore')]
import photo_semantic_evidence as s
import photo_candidate_corpus as c
import photo_search_layout as layout
import prompt_generator as g
import audit_composed_prompt as audit

def assertion(aid,d,kind,**axes):
    return {'assertion_id':aid,'dimension':d,'polarity':'required','source_span_ids':['request'],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'literal':TEXT},'affected_dimensions':[d]}
def core(help=False,cheek=False,recovery=False):
    global TEXT
    TEXT='Ari is an already declared adult human person and a peer rival in this scene. No counterpart is specified. Ari has an already existing own face with eyes, eyelids, a brow region and a mouth. Ari body and face presentation are unmistakably adult and must remain so. Visible youthful-adult presentation, styling, expression, eye opening and bodily bearing are open.'
    if help:TEXT+=' Nox is a separately established helper, disjoint from Ari. Visible help activity is open.'
    if cheek:TEXT+=' The same existing face has a cheek region; its local visible cheek color is open.'
    if recovery:TEXT+=' A prior brief disruption is already declared as narrative context for Ari. A recovery-attempt instant is open.'
    rows=[assertion('actor','subject','owner',owner='ari',owner_kind='human'),assertion('actor_role','subject','role',owner='ari',role='main_subject'),assertion('face','subject','owner',owner='ari_face',owner_kind='face'),assertion('face_role','subject','role',owner='ari_face',role='primary_face'),assertion('part','subject','part_of',left='ari_face',right='ari')]
    specs=[('present','subject','ari','entity.presence','entity.presence/v1','present'),('face_present','subject','ari_face','anatomy.face.presence','anatomy.face.presence/v1','present'),('adult','age','ari','age.declared','age.declared/v1','adult'),('role','role','ari','participant.role.peer_rival','participant.role.peer_rival/v1','declared'),('body_adult','age','ari','age.presentation.body','age.presentation.body/v1','unmistakably_adult'),('face_adult','age','ari_face','age.presentation.face','age.presentation.face/v1','unmistakably_adult')]
    specs += [(part,'subject','ari_face','anatomy.'+part+'.presence','anatomy.'+part+'.presence/v1','present') for part in ['eyes','eyelids','brow','mouth']]
    if help:
        rows += [assertion('helper_owner','subject','owner',owner='nox',owner_kind='human'),assertion('helper_role','subject','role',owner='nox',role='secondary_subject'),assertion('helper_distinct','subject','disjoint',left='nox',right='ari')]
        specs.append(('helper','subject','nox','entity.presence','entity.presence/v1','present'))
    if cheek:specs.append(('cheek','subject','ari_face','anatomy.cheek.presence','anatomy.cheek.presence/v1','present'))
    if recovery:specs.append(('prior','timing','ari','narrative.context.prior_disruption','narrative.prior_disruption/v1','declared'))
    rows += [assertion(aid,d,'fact',owner=owner,property=prop,value_type=typ,value=val) for aid,d,owner,prop,typ,val in specs]
    anchors=[{'dimension':d,'target':owner,'property':prop} for aid,d,owner,prop,typ,val in specs if d in {'age','role','timing'}]
    frozen={'contract_version':'photo-authorial-core/v3','subject':TEXT,'baseline_prompt_en':TEXT,'request_binding':{'active_spans':[{'source_span_id':'request','text':TEXT}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['subject','role'],'open_dimensions':['age','appearance','expression','pose','action','event','timing'],'semantic_anchors':anchors}}
    s.frozen_witnesses(frozen);return frozen,[x[0] for x in specs]

# Independent exact requester meanings precede loading any candidate/proof.
CORES={};OBLIGATIONS={}
for key,h,ch,re in [('base',False,False,False),('setback',False,False,False),('help',True,False,False),('mouth',False,False,False),('cheek',False,True,False),('recovery',False,False,True),('help_cheek',True,True,False),('help_mouth',True,False,False),('help_recovery',True,False,True),('help_cheek_recovery',True,True,True),('help_mouth_recovery',True,False,True),('cheek_recovery',False,True,True),('mouth_recovery',False,False,True)]:
    CORES[key],OBLIGATIONS[key]=core(h,ch,re)
M=runpy.run_path(str(Path(__file__).with_name('native_fresh_08250_17437_05_author.py')))
sys.path[:0]=[str(GEN/'scripts'),str(GEN/'precore')]
T=M['T'];CID=M['CID'];CAT=M['CAT'];PROOF=M['PROOF'];CHOICES=M['CHOICES'];I=M['I'];P=M['P']
PROOF=copy.deepcopy(PROOF);PROOF['review']['native_review']['native_contract_sha256']=s.native_contract_sha256(PROOF)
REC=copy.deepcopy(T);REC['content']['role_evidence']=PROOF;DATA={'candidates':{CID:REC},'slot_catalog':CAT,'slot_bindings':{}}
s.validate(REC,CAT,corpus=DATA)
compact=layout.guard_record(REC,DATA);CD={**DATA,'candidates':{CID:compact}}
def eligible(entry,frozen):return g.core_entry_eligible(DATA,frozen,{'adult_allowed':True,'subject_category':'human','intent_constraints':{'subject_categories':['human'],'domains':[]}}, {'subject':{'tags':['human']}},'age_presentation',entry)
CASES=[];LOCKS=[];AUDITS=[];NEG=[]
common_ev={'adult_role_phrase':'The adult peer rival is unmistakably adult in body and face.','haughty_baseline_phrase':'The haughty baseline shows half-lidded eyes and poised bearing.','smug_expression_phrase':'The smug expression retains a superior smirk on Ari face.','adult_youthful_styling_phrase':'Fresh adult styling remains visible on Ari.','appearance_inference_exclusion_phrase':'Adult behavior carries this profile, not childlike proportions.'}
event_ev={'setback':('setback_selected_phrase','A small visible setback stays local to Ari.'),'help':('help_selected_phrase','The declared rival receives help from the established helper Nox.'),'mouth_warmth':('mouth_warmth_selected_phrase','Brief softening at the same rival mouth corner stays local.'),'cheek_warmth':('cheek_warmth_selected_phrase','A bounded visible cheek warmth on the same rival stays local.'),'recovery':('recovery_selected_phrase','The same rival tries to regain the superior smirk after declared disruption.')}
for rid,chosen in CHOICES:
    key=('_'.join(x for x in ['help' if 'help' in chosen else '', 'cheek' if 'cheek_warmth' in chosen else ('mouth' if 'mouth_warmth' in chosen else ''),'recovery' if 'recovery' in chosen else ''] if x)) or ('setback' if 'setback' in chosen else 'base')
    frozen=CORES[key]
    for form,entry in [('full',c.entry(DATA,CID,realization_id=rid)),('compact',c.entry(CD,CID,realization_id=rid))]:
        positive=s.admission(entry,frozen);assert positive['allowed'],(rid,form,positive)
        assert eligible(entry,frozen)
        CASES.append({'rid':rid,'form':form,'case':'exact_independent_core','allowed':True})
        for aid in OBLIGATIONS[key]:
            for defect in ['absent','wrong_owner','wrong_value']:
                bad=copy.deepcopy(frozen)
                if defect=='absent':bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['assertion_id']!=aid]
                elif defect=='wrong_value':next(x for x in bad['semantic_assertions'] if x['assertion_id']==aid)['axes']['value']='wrong'
                else:
                    bad['semantic_assertions'].append(assertion('unrelated','subject','owner',owner='unrelated',owner_kind='human'))
                    row=next(x for x in bad['semantic_assertions'] if x['assertion_id']==aid);row['axes']['owner']='unrelated'
                    bad['intent_lock']['semantic_anchors'].append({'dimension':row['dimension'],'target':'unrelated','property':row['axes']['property']})
                result=s.admission(entry,bad);assert not result['allowed'],(rid,form,aid,defect)
                CASES.append({'rid':rid,'form':form,'case':defect,'assertion_id':aid,'allowed':False})
        for aid in ['part']+(['helper_distinct'] if 'help' in chosen else []):
            bad=copy.deepcopy(frozen);bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['assertion_id']!=aid]
            assert not s.admission(entry,bad)['allowed'];CASES.append({'rid':rid,'form':form,'case':'missing_explicit_owner_relation','assertion_id':aid,'allowed':False})
        dims,props,_=s.permission_scope(entry,frozen)
        for p in props:
            bad=copy.deepcopy(frozen);bad['intent_lock']['semantic_anchors'].append(p)
            assert not s.property_scope_allowed(bad,dims,props) and not eligible(entry,bad),(rid,form,p)
            LOCKS.append({'rid':rid,'form':form,'kind':'property','property':p,'rejected':True})
        for dim in sorted(set(dims)):
            bad=copy.deepcopy(frozen);bad['intent_lock']['open_dimensions'].remove(dim);bad['intent_lock']['locked_dimensions'].append(dim)
            assert not eligible(entry,bad);LOCKS.append({'rid':rid,'form':form,'kind':'whole_dimension','dimension':dim,'rejected':True})
        # Matching current youthful-adult value does not grant an effect on its
        # independently locked property; no automatic age/appearance alias.
        bad=copy.deepcopy(frozen);bad['semantic_assertions'].append(assertion('fixed_current_age','age','fact',owner='ari',property='age.presentation.youthful_adult',value_type='age.presentation.youthful_adult/v1',value='youth_appearing_adult'));bad['intent_lock']['semantic_anchors'].append({'dimension':'age','target':'ari','property':'age.presentation.youthful_adult'})
        assert not s.property_scope_allowed(bad,dims,props);LOCKS.append({'rid':rid,'form':form,'kind':'same_value_locked_property','rejected':True})
        evidence={**common_ev,**dict(event_ev[k] for k in chosen)}
        prompt=' '.join(evidence.values());interp={'realization_id':rid,'selected_profile_contract':PROOF['profile_contracts'][rid],'selected_profile_evidence':evidence}
        audit.audit_selected_native_profile(entry,interp,prompt)
        for defect in ['missing_contract','wrong_contract','missing_common','missing_selected','foreign','nonliteral']:
            if defect=='missing_selected' and not chosen:continue
            bad=copy.deepcopy(interp)
            if defect=='missing_contract':bad.pop('selected_profile_contract')
            elif defect=='wrong_contract':bad['selected_profile_contract']['compiled_sha256']='0'*64
            elif defect=='missing_common':bad['selected_profile_evidence'].pop('adult_role_phrase')
            elif defect=='missing_selected':bad['selected_profile_evidence'].pop(event_ev[chosen[0]][0])
            elif defect=='foreign':bad['selected_profile_evidence']['foreign']='Unselected duty.'
            else:bad['selected_profile_evidence']['adult_role_phrase']='Absent exact phrase.'
            try:audit.audit_selected_native_profile(entry,bad,prompt)
            except ValueError:pass
            else:raise AssertionError((rid,form,defect))
            AUDITS.append({'rid':rid,'form':form,'case':defect,'rejected':True})
        AUDITS.append({'rid':rid,'form':form,'case':'complete_exact_selected_contract','allowed':True,'fields':len(evidence)})


GUARD_NEG=[]
for defect in ['foreign_cid','foreign_rid','wrong_condition_index','wrong_condition_sha','wrong_rule_sha','wrong_endpoint','metadata_anchor','missing_normal_guard_ref','guard_as_E']:
 rec=copy.deepcopy(REC);p=rec['content']['role_evidence'];support=p['guard_supports'][0]
 if defect=='foreign_cid':support['guard']['declaring_candidate_id']='cand_'+'0'*32
 elif defect=='foreign_rid':support['guard']['declaring_realization_id']='help'
 elif defect=='wrong_condition_index':support['guard']['source_condition_index']=1
 elif defect=='wrong_condition_sha':support['guard']['conditions_sha256']='0'*64
 elif defect=='wrong_rule_sha':support['guard']['rule_sha256']='0'*64
 elif defect=='wrong_endpoint':support['endpoints']['left_role']['target']='actor'
 elif defect=='metadata_anchor':support['pointer']='/content/runtime_expression/default_mode'
 elif defect=='missing_normal_guard_ref':
  next(u for u in p['source_units'] if u.get('guard_refs')==[support['id']]).pop('guard_refs')
 else:support['mode']='effect'
 p['review']['native_review']['native_contract_sha256']=s.native_contract_sha256(p)
 try:s.validate(rec,CAT,corpus={**DATA,'candidates':{CID:rec}})
 except ValueError as exc:GUARD_NEG.append({'case':defect,'rejected':True,'error':str(exc)})
 else:raise AssertionError(('missing_guard_rejection',defect))
for defect in ['missing_canonical_normal','self_reference','foreign_rid_reference','missing_actual_age_E','changed_guard','changed_profile','unselected_helper']:
 rec=copy.deepcopy(REC);p=rec['content']['role_evidence']
 if defect=='missing_canonical_normal':p['source_units']=[u for u in p['source_units'] if not(u['realization_id']=='baseline' and u['pointer'].endswith('/render_gates/3/description') and u['disposition']=='semantic')]
 elif defect=='self_reference':next(u for u in p['source_units'] if u['realization_id']=='baseline' and u['pointer'].endswith('/obligations/0/instruction') and u['disposition']=='semantic_reference')['fact_refs']=['g05_baseline_style']
 elif defect=='foreign_rid_reference':next(u for u in p['source_units'] if u['disposition']=='semantic_reference')['fact_refs']=['g05_help_expression']
 elif defect=='missing_actual_age_E':p['facts']=[f for f in p['facts'] if f['property']!='age.presentation.youthful_adult']
 elif defect=='changed_guard':p['guard_sets']['baseline']['source_conditions'][0]={}
 elif defect=='changed_profile':p['profile_contracts']['baseline']['compiled_sha256']='0'*64
 else:p['owner_maps']['baseline']['bindings'].append({'target':'helper','core_role':'secondary_subject','origin':'existing','introduced_by':None})
 p['review']['native_review']['native_contract_sha256']=s.native_contract_sha256(p)
 try:s.validate(rec,CAT,corpus={**DATA,'candidates':{CID:rec}})
 except ValueError as exc:NEG.append({'case':defect,'rejected':True,'error':str(exc)})
 else:raise AssertionError(('missing_shape_rejection',defect))
ROLE=[]
for rid,_ in CHOICES:
 for tag,role in PROOF['roles'].items():
  for form,data in [('full',DATA),('compact',CD)]:
   result=s.qualification(CAT[tag],data['candidates'][CID],rid)
   expected=rid in role['realization_ids']
   assert (result['status']=='eligible')==expected,(rid,tag,form,result)
   ROLE.append({'rid':rid,'tag':tag,'form':form,'eligible':expected,'guard_refs':result.get('guard_refs',[])})
# Existing current value cannot waive closed actual dimension either.
for rid,_ in CHOICES:
 for form,data in [('full',DATA),('compact',CD)]:
  key=next(k for k in CORES if k=='base')
  entry=c.entry(data,CID,realization_id=rid)
  selected=dict(CHOICES)[rid]
  if selected:continue
  frozen=copy.deepcopy(CORES[key]);frozen['semantic_assertions'].append(assertion('same_age','age','fact',owner='ari',property='age.presentation.youthful_adult',value_type='age.presentation.youthful_adult/v1',value='youth_appearing_adult'))
  frozen['intent_lock']['open_dimensions'].remove('age');frozen['intent_lock']['locked_dimensions'].append('age')
  assert not eligible(entry,frozen)
  LOCKS.append({'rid':rid,'form':form,'kind':'same_value_closed_age_dimension','rejected':True})
mods={name:{'file':str(Path(mod.__file__).resolve()),'raw_sha256':hashlib.sha256(Path(mod.__file__).read_bytes()).hexdigest()} for name,mod in sorted(sys.modules.items()) if getattr(mod,'__file__',None) and (name.startswith('photo_') or name in ['prompt_generator','audit_composed_prompt','visual_profile_contracts'])}
assert all(Path(x['file']).is_relative_to(GEN) for x in mods.values())
assert mods['photo_semantic_evidence']['raw_sha256']=='6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
report={'schema':'photo-native-fresh05-independent-consumer-check/v1','candidate_id':CID,'frozen_generation':str(GEN),'actual_loaded_modules':mods,'candidate_independent_cores_built_before_candidate_load':True,'core_fixtures':CORES,'full_compact_admission_consumer_cases':CASES,'lock_negatives':LOCKS,'profile_audits':AUDITS,'shape_negative_cases':NEG,'guard_provenance_negative_cases':GUARD_NEG,'full_compact_role_cases':ROLE,'source_units':len(PROOF['source_units']),'scalar_facts':len(PROOF['facts']),'guard_supports':len(PROOF['guard_supports']),'all_actual_rids':[rid for rid,_ in CHOICES],'own_oldbindings':{},'own_oldbinding_test_count':0,'oldbinding_boundary':'Complete original/current ownbindings empty: no invented old binding consumer case. Source role restrictions remain actual existing-owner map.','root_acceptance':False,'operating_native_qualified_count':0,'provider_model_network_calls':0,'scope':'Actual frozen full/compact validation and synthetic independent-core consumer/locks/role/profile/guard tests. No actual requester, pixels, root semantic acceptance, optional unselected instrument application or publication proved.'}
out=R/'authored/native_fresh_08250_17437_05_checks.json';assert not out.exists();out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'cases':len(CASES),'locks':len(LOCKS),'profile_audits':len(AUDITS),'shape_negatives':len(NEG),'guard_negatives':len(GUARD_NEG),'role_cases':len(ROLE),'report_raw_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
