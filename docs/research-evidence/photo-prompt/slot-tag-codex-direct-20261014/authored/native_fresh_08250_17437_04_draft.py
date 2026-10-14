"""Fresh literal146V5 source inventory. Pending anatomy-role representation.

No prior proof is loaded. Repetition serializes explicitly reviewed RID layouts;
it does not classify source language. This draft is not a native batch approval.
"""
import copy,hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
GEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/2ad7b2bfd3f4d730985c23ed89e3513a326a0a2ceea22aecfe28cb5d05c98ac9')
sys.path[:0]=[str(GEN/'scripts'),str(GEN/'precore'),str(R)]
import photo_candidate_corpus as c
import photo_candidate_realizations as rr
import photo_semantic_evidence as s
import visual_profile_contracts as vp
import native_reviews as nr
sys.path[:0]=[str(GEN/'scripts'),str(GEN/'precore')]
assert Path(s.__file__).is_relative_to(GEN)
assert hashlib.sha256(Path(s.__file__).read_bytes()).hexdigest()=='0f4a974435f7cb9e71a23a726f092bff73d0dd61bb9deb3df2537f59d5be15e4'
P=R/'native-inputs/prepared/review08250-17437-04'
I=json.loads((P/'INPUT.json').read_text());ASS=json.loads((P/'ASSIGNMENT.json').read_text());PACK=json.loads((P/'PREPARED-PACKET.json').read_text())
CID=ASS['ids'][0];T=PACK['current_records'][CID];BEFORE=PACK['original_records'][CID];OLD=PACK['historical_compiled_rows'][CID];CAT=I['catalog_review']['after']
assert c.digest(CAT)=='3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645'
CHOICES=[('baseline',[]),('setback',['setback']),('help',['help']),('mouth_warmth',['mouth_warmth']),('cheek_warmth',['cheek_warmth']),('recovery',['recovery']),('setback_mouth_warmth',['setback','mouth_warmth']),('setback_cheek_warmth',['setback','cheek_warmth']),('setback_recovery',['setback','recovery']),('help_mouth_warmth',['help','mouth_warmth']),('help_cheek_warmth',['help','cheek_warmth']),('help_recovery',['help','recovery']),('mouth_warmth_recovery',['mouth_warmth','recovery']),('cheek_warmth_recovery',['cheek_warmth','recovery']),('setback_mouth_warmth_recovery',['setback','mouth_warmth','recovery']),('setback_cheek_warmth_recovery',['setback','cheek_warmth','recovery']),('help_mouth_warmth_recovery',['help','mouth_warmth','recovery']),('help_cheek_warmth_recovery',['help','cheek_warmth','recovery'])]
assert set(rr.ids(T))=={rid for rid,_ in CHOICES}
F=[];U=[];MAPS={};READ=[]
def add(rid,key,p,q,d,t,prop,mode,value,requires,typ=None):
    f={'id':rid+'_'+key,'realization_id':rid,'pointer':p,'quote':q,'dimension':d,'target':t,'property':prop,'mode':mode,'value':{'type':typ or prop+'/v1','value':value},'requires':list(requires)}
    if mode=='effect':f.update(operation='set_value',receivers=[])
    assert q in s.positive_string(T,p,realization_id=rid),(p,q)
    F.append(f);return f['id']
def unit(rid,p,refs,relation=None,why=None):
    u={'realization_id':rid,'pointer':p,'quote':s.positive_string(T,p,realization_id=rid),'fact_refs':list(refs),'disposition':'semantic_reference' if relation else ('semantic' if refs else 'nonsemantic')}
    if relation:u.update(reference_relation=relation,retained_constraint_rationale=why)
    U.append(u)

for rid,selected in CHOICES:
    root='/content/realization_content/'+rid
    ip=root+'/authored_components/obligations/0/instruction';gp=root+'/authored_components/obligations/0/render_gates'
    ids={}
    def a(k,p,q,d,t,prop,mode,val,req,typ=None):
        ids[k]=add(rid,k,p,q,d,t,prop,mode,val,req,typ);return ids[k]
    a('present',ip,'already declared adult peer-rival role','subject','actor','entity.presence','prerequisite','present',[])
    a('face',ip,'already existing owned face','subject','actor_face','anatomy.face.presence','prerequisite','present',[ids['present']])
    a('adult',ip,'already declared adult peer-rival role','age','actor','age.declared','prerequisite','adult',[ids['present']])
    a('role',ip,'already declared adult peer-rival role','role','actor','participant.role.peer_rival','prerequisite','declared',[ids['present']])
    for k,t,prop in [('body_adult','actor','age.presentation.body'),('face_adult','actor_face','age.presentation.face')]:
        a(k,ip,'Preserve unmistakably adult body and face presentation','age',t,prop,'prerequisite','unmistakably_adult',[ids['present']]+([ids['face']] if t=='actor_face' else []))
    for k,t,prop in [('keep_body','actor','age.presentation.body'),('keep_face','actor_face','age.presentation.face')]:
        a(k,ip,'Preserve unmistakably adult body and face presentation','age',t,prop,'preservation','same',[ids['present']]+([ids['face']] if t=='actor_face' else []),'frozen_property_reference/v1')
    a('eyes',ip,'haughty half-lidded eyes','subject','actor_face','anatomy.eyes.presence','prerequisite','present',[ids['present'],ids['face']])
    for k,q in [('eyelids','owns the haughty eyelids'),('brow','haughty eyelids, brow, mouth'),('mouth','haughty eyelids, brow, mouth')]:
        a(k,gp+'/1/description',q,'subject','actor_face','anatomy.'+k+'.presence','prerequisite','present',[ids['present'],ids['face']])
    required=list(ids.values())
    a('eye_effect',ip,'haughty half-lidded eyes','appearance','actor_face','eyes.structure.lid_opening','effect','haughty_half_lidded',required)
    a('style',ip,'fresh youthful adult styling','appearance','actor','presentation.fresh_youthful_adult_styling','effect','fresh_youthful_adult_styling',required)
    a('pose',ip,'poised bearing','pose','actor','body.pose.poised_bearing','effect','poised',required)
    a('age_effect',ip,'visibly youthful-adult age presentation','age','actor','age.presentation.youthful_adult','effect','youth_appearing_adult',required)
    # The full exact qualifier is at this gate, not borrowed into the narrower
    # anatomy gate or the instruction's smug-poised phrase.
    a('expression',gp+'/3/description','haughty smug poised baseline','expression','actor_face','face.expression.haughty_smug_baseline','effect','haughty_smug_poised',required)
    common_keys=['present','face','adult','role','body_adult','face_adult','keep_body','keep_face','eyes','eyelids','brow','mouth','eye_effect','style','pose','age_effect','expression']
    common=[ids[k] for k in common_keys]
    at_ip=[f['id'] for f in F if f['realization_id']==rid and f['pointer']==ip]
    unit(rid,ip,at_ip)
    unit(rid,ip,[ids['expression']],'selected_output_constraint',
         'This complete common instruction binds a smug poised facial baseline to the same actor whose eyes are haughty and half-lidded. The independently complete haughty/smug/poised facial assignment is grounded in this selected profile gate3. Preserve existing-role and owned-face application restrictions, explicit adult preservation, optional existing one-up context only, and all three independent optional groups. No narrower phrase here independently supplies missing qualifiers; no new identity, actor or counterpart is created.')
    unit(rid,gp+'/1/description',[ids[k] for k in ['eyelids','brow','mouth']])
    unit(rid,gp+'/1/description',[ids[k] for k in ['present','face','role','eye_effect','expression','pose']],'same_selected_owner',
         'Named existing eyelids, brow region and mouth remain owned by the same rival face, explicitly part of that actor. The whole face part_of actor condition is retained in the exact source owner_relation guard. The narrower haughty-part description constrains the already selected facial baseline and bearing; it is not a complete independent haughty/smug/poised E anchor. No eyebrow hair, extra face or counterpart is inferred. Anatomical ownership tag certification is separately pending because scalar fact_refs cannot cite a relation guard.')
    unit(rid,gp+'/3/description',[ids['expression']])
    unit(rid,gp+'/3/description',[ids[k] for k in ['role','adult','style','age_effect']],'partial_restatement',
         'This gate retains mandatory common adult-peer, fresh styling and visibly youthful-adult presentation, with incidents optional unless selected and morphology/reference/label substitutions rejected. The full fresh youthful adult styling value has its own direct instruction anchor. The adult-peer fragment is not treated as a new independently frozen peer-rival value or a second entity.')
    for prefix in ['/content/authored_components/obligations/0',root+'/authored_components/obligations/0']:
        # The selected normal gate1/gate3 are handled separately above.
        for gi,ks,why in [
            (0,['adult','body_adult','face_adult','keep_body','keep_face','age_effect'],'The same existing rival stays unmistakably adult in body and face, with visibly youthful-adult presentation. Declared adulthood and requester identity are preserved; biological/numeric age and child/teen morphology remain excluded.'),
            (1,['present','face','role','eyelids','brow','mouth','eye_effect','expression','pose'],'This common gate repeats explicit own-face/actor part ownership and named haughty eyelids, brow region, mouth and bearing. Its narrow part phrase is an owner/readability condition on the selected full facial baseline, not independent full E evidence. Exact owner_relation source guard remains mandatory; no automatic counterpart or eyebrow hair.'),
            (2,['style','eye_effect','expression','pose'],'Fresh youthful styling remains adult and haughty half-lidded eyes/smug poised bearing stay readable on the same rival. The exact complete youthful-adult styling selection is separately grounded; no private disposition is inferred.'),
            (3,['role','adult','expression','style','age_effect'],'Common adult-peer, haughty smug poised baseline, fresh styling and youthful-adult presentation stay mandatory. Incidents remain optional and hair/face-size/reference/label shortcuts do not suffice. Full role and styling are supported at separate exact canonical fields.')]:
            p=prefix+f'/render_gates/{gi}/description'
            if p in {gp+'/1/description',gp+'/3/description'}:continue
            unit(rid,p,[ids[k] for k in ks],'selected_output_constraint',why)
    unit(rid,'/content/authored_components/obligations/0/instruction',common,'selected_output_constraint',
         'The complete common instruction constrains this actual same-RID selection: existing declared actor/owned face and deliberate role restrictions, adult body/face preservation, youthful-adult appearance, haughty eyes, smug poised baseline, bearing and fresh adult styling. Actual events arise only from selected independent groups. One-up remains optional already established context; no childlike morphology or arbitrary identity/second participant is authorized.')
    unit(rid,'/content/semantics/definition',common,'partial_restatement',
         'The common definition restates the same existing adult peer-rival/owned-face selection, full visible baseline, deliberate existing-owner restriction, four required groups and three independently optional groups. It grants no new one-up event or second participant; the definition is not another canonical assignment.')
    optional={}
    for oi,kind in enumerate(selected,1):
        op=root+f'/authored_components/obligations/{oi}/instruction';og=root+f'/authored_components/obligations/{oi}/render_gates/0/description';cr=root+f'/concept_units/{oi}'
        refs=[]
        if kind=='setback':
            refs=[a('setback',op,'same declared rival experiences one visible small setback','event','actor','situation.small_setback','effect','visible_local_small_setback',required,'event.small_setback/v1')]
            rationale='Exactly one visible local small setback belongs to this declared rival. All exclusions of new actor/object/injury/humiliation/private feeling remain, and any actually used concrete instrument must already be independently established. This is selected E, not an incoming setback prerequisite or a permission to create a tool.'
        elif kind=='help':
            hp=a('helper',op,'separately established helper','subject','helper','entity.presence','prerequisite','present',[ids['present']])
            recv=a('help_receive',op,'declared rival receives visible help from a separately established helper','action','actor','action.interaction.receives_help','effect','visible_help_from_bound_helper',required+[hp])
            give=a('help_provide',op,'declared rival receives visible help from a separately established helper','action','helper','action.interaction.provides_help','effect','visible_help_to_bound_actor',required+[hp])
            refs=[hp,recv,give]
            rationale='This selected visible help has separately established helper and same rival recipient. Both actual action footprints remain, with existing helper/recipient ownership distinct and disjoint guard mandatory. Optional instruments are existing if used; no new helper, returned object, hand contact or separate counterpart is required. A helper may equal an independently named counterpart only when the core explicitly establishes that identity. [] receivers on each paired assignment adds no third affected owner.'
        elif kind=='mouth_warmth':
            refs=[a('mouth_warmth',op,"brief local softening of the rival's mouth corner",'expression','actor_face','face.expression.mouth_corner_warm_crack','effect','brief_local_mouth_corner_softening',required)]
            rationale='Brief local mouth-corner softening remains on the same rival and interrupts the superior smirk while the selected adult haughty eye baseline stays readable. Full brief value is anchored at this selected instruction; local gate softening is its readability condition. No incoming haughty-eye prerequisite, full face-age proof from an eye fragment, global generic smile, gratitude, prior event or forced cheek-color E is introduced.'
        elif kind=='cheek_warmth':
            cp=a('cheek',op,"rival's cheek",'subject','actor_face','anatomy.cheek.presence','prerequisite','present',[ids['present'],ids['face']])
            ce=a('cheek_color',op,"bounded visible warm-color cue appears on the rival's cheek",'appearance','actor_face','skin.color.localized_cheek_warm_color','effect','bounded_visible_local_cheek_color_warming',required+[cp])
            refs=[cp,ce]
            rationale='One bounded visible warm-color cheek cue belongs to this same rival; canonical local color is grounded in the positive selected instruction. Cheek-only P is explicit here. The bounded-cue gate constrains owner/locality and excludes global grading, cosmetic pigment, literal heat and private emotion; it does not independently name warm color. Smug haughty baseline remains legible; no mouth softening, skin-state duplicate, temperature, diagnosis or gratitude is added.'
        else:
            assert kind=='recovery'
            prior=a('prior_disruption',op,'after a declared brief disruption','timing','actor','narrative.context.prior_disruption','prerequisite','declared',[ids['present']],'narrative.prior_disruption/v1')
            attempt=a('recovery_expression',op,'visibly tries to restore the superior smirk or poised composure','expression','actor_face','face.expression.composure_recovery_attempt','effect','visible_attempt_to_restore_superior_smirk_or_poised_composure',required+[prior])
            phase=a('recovery_phase',op,'selected instant represents a recovery attempt','timing','actor','narrative.phase.recovery_attempt','effect','recovery_attempt',required+[prior])
            refs=[prior,attempt,phase]
            rationale='The exact restoration goal (superior smirk OR poised composure) and recovery-attempt instant are supported in selected instruction. Independent already declared prior disruption stays P even when another optional group is selected. Local gate requires readable attempt and identifiable continuing adult haughty baseline; it is not independent full-goal evidence or whole-face adult preservation evidence. No completed recovery, elapsed sequence, hidden suppression or simultaneous setback/warmth prerequisite is inferred.'
        optional[kind]=refs
        unit(rid,op,refs)
        continuing=[ids['eye_effect'],ids['expression']] if kind in {'mouth_warmth','cheek_warmth','recovery'} else []
        if continuing:unit(rid,op,continuing,'selected_output_constraint',rationale)
        unit(rid,og,refs+continuing,'selected_output_constraint',rationale)
        unit(rid,cr,refs+continuing,'selected_output_constraint',rationale)
    all_selected=common+[f for refs in optional.values() for f in refs]
    # Each field below was directly read with its actual complete selected body,
    # including language-specific exclusions. No sibling is used as evidence.
    for tail in ['/en','/embedding_text','/ko','/semantics/definition','/semantics/paraphrase_examples/0']:
        unit(rid,root+tail,all_selected,'selected_output_constraint',
             'The complete selected body repeats the common baseline and exactly these selected optional groups: '+(', '.join(selected) or 'none')+'. Keep all existing actor/face/role and adult body/face preservation constraints, actual anatomy ownership, age E distinct from declared adult P, and actual selected event/action/warmth/recovery outputs. Every optional clause retains its owner/readability/exclusion duty as separately documented by its same-RID instruction/gate units. No narrower eye-baseline fragment substitutes for whole-face preservation or full expression. The Korean body is a same-selected-output constraint, not an assertion that every English canonical qualifier occurs independently in a shorter Korean fragment.')
    unit(rid,root+'/concept_units/0',common,'selected_output_constraint',
         'This exact common full instruction repeats the selected baseline and existing-role/owner restrictions, adult preservation and all independent optional-choice limits. Canonical full expression is at the selected gate3, not inferred from a narrow anatomy fragment.')
    # Short paraphrases retain their outward descriptor/context locally; they
    # refer to the full role/age/baseline without manufacturing peer from rival.
    paras=[('도도한','haughty_descriptor',['role','adult','expression']),('잘난 척하는','outward_smug_descriptor',['role','adult','expression']),('건방지고 도도하지만','outward_haughty_cheeky_descriptor',['adult','expression','age_effect']),('smug','outward_smug_descriptor',['role','adult','expression']),('haughty','haughty_descriptor',['role','adult','expression'])]
    for pi,(quote,value,ks) in enumerate(paras):
        pp='/content/semantics/paraphrase_examples/'+str(pi)
        f=add(rid,'descriptor_'+str(pi),pp,quote,'concept','actor','character.outward_descriptor','context',value,[ids['present']])
        unit(rid,pp,[f]);unit(rid,pp,[ids[k] for k in ks],'partial_restatement',
             'This short actual paraphrase keeps its stated adult/outward descriptor and, where present, youthful-adult appearance. A rival-only phrase does not independently prove peer, a peer-only phrase does not prove rival, and no descriptor proves private personality. It partially restates the separately and exactly grounded common role/facial selection on this same RID; it creates no counterpart or additional frozen scalar role requirement.')
    pp='/content/semantics/paraphrase_examples/5'
    f=add(rid,'optional_one_up',pp,'teasing one-up','event','actor','event.context.one_up','context','teasing_one_up',[ids['present']])
    unit(rid,pp,[f])
    non=[]
    for prefix,ac in [('/content/authored_components',T['content']['authored_components']),(root+'/authored_components',T['content']['realization_content'][rid]['authored_components'])]:
        for oi,ob in enumerate(ac['obligations']):
            for ei,e in enumerate(ob['evidence']):
                non.append(prefix+f'/obligations/{oi}/evidence/{ei}/field')
                non += [prefix+f'/obligations/{oi}/evidence/{ei}/requirement/must_not_contain/{n}' for n in range(len(e['requirement'].get('must_not_contain',[])))]
            non += [prefix+f'/obligations/{oi}/render_gates/{gi}/review_scale' for gi in range(len(ob['render_gates']))]
    paths=s.primary_paths(T,rid)
    for p in non:
        if p in paths:unit(rid,p,[])
    assert {u['pointer'] for u in U if u['realization_id']==rid}==paths,(rid,paths-{u['pointer'] for u in U if u['realization_id']==rid})
    bindings=[{'target':'actor','core_role':'main_subject','origin':'existing','introduced_by':None},{'target':'actor_face','core_role':'primary_face','origin':'existing','introduced_by':None}]
    if 'help' in selected:bindings.append({'target':'helper','core_role':'secondary_subject','origin':'existing','introduced_by':None})
    MAPS[rid]={'schema':s.OWNER_SCHEMA,'bindings':bindings}
    active=[f for f in F if f['realization_id']==rid]
    assert {s.property_key(f) for f in active if f['mode']=='effect'}=={s.property_key(p) for p in rr.effects(T,rid)['properties']}
    assignments={}
    for f in active:
        if f['mode']!='effect':continue
        k=s.property_key(f);v=c.canonical_bytes({a:f[a] for a in ['value','operation','receivers']})
        assert k not in assignments or assignments[k]==v
        assignments[k]=v
    READ.append({'realization_id':rid,'selected_groups':selected,'facts':len(active),'primary_paths':len(paths),'full_source_units':sum(u['realization_id']==rid for u in U),'all_actual_effects_preserved':True,'scalar_assignment_conflicts':0,'anatomical_role_guard_only_pending':True})

ROLES={}
role_specs={
 'age_presentation':(['age.declared','age.presentation.body','age.presentation.face','age.presentation.youthful_adult'],['prerequisite','preservation','effect']),
 'expression':(['face.expression.haughty_smug_baseline','face.expression.mouth_corner_warm_crack','face.expression.composure_recovery_attempt'],['effect']),
 'eye_detail':(['eyes.structure.lid_opening'],['effect']),
 'presentation_style':(['presentation.fresh_youthful_adult_styling'],['effect']),
 'body_pose':(['body.pose.poised_bearing'],['effect']),
 'participant_role':(['participant.role.peer_rival'],['prerequisite']),
 'skin_tone':(['skin.color.localized_cheek_warm_color'],['effect']),
 'action':(['action.interaction.receives_help','action.interaction.provides_help'],['effect']),
 'relational_action':(['action.interaction.receives_help','action.interaction.provides_help'],['effect']),
 'narrative_phase':(['narrative.phase.recovery_attempt'],['effect']),
 'situation_context':(['situation.small_setback'],['effect'])}
for tag,(properties,modes) in role_specs.items():
    fs=[f for f in F if f['property'] in properties and f['mode'] in modes]
    rids=[rid for rid,_ in CHOICES if any(f['realization_id']==rid for f in fs)]
    ROLES[tag]={'spec_sha256':c.digest(CAT[tag]),'scope':'whole_record' if len(rids)==18 else 'positive_alternative','realization_ids':rids,'fact_refs':[f['id'] for f in fs],'support_modes':modes}
LOC=I['original_decisions'][CID]
PROOF={'schema':s.SCHEMA,'meaning_sha256':s.meaning_sha256(T),'catalog_sha256':c.digest(CAT),'complete':True,'facts':F,'roles':ROLES,'owner_maps':MAPS,'source_units':U,'effect_sets':{rid:s.effect_set(T,rid) for rid,_ in CHOICES},'dependencies':{rid:[] for rid,_ in CHOICES},'reference_sha256':{},'guard_sets':{rid:s.source_guard_set(T,rid,{'candidates':{CID:T},'slot_bindings':{}}) for rid,_ in CHOICES},'profile_contracts':{rid:rr.profile_contract(T,rid) for rid,_ in CHOICES},'review':{'basis':'Fresh original/current source, actual18 selected bodies/conditions/effects/profile, exact normalized compiled item188, empty ownbinding/reference closure and full146V5 used specs/neighbor read. All204 prior precision entries were individually displayed and manually judged in four bounded views. This unsigned batch-independent proof draft tests exact field-local anchors and one-hop retained constraints; anatomical_connection role remains outside current scalar fact_refs contract and prevents candidate approval. No prior proof loaded or converted.','whole_source_reviewed':True,'source_correction':{'before_sha256':s.meaning_sha256(BEFORE),'after_sha256':s.meaning_sha256(T),'rationale':'Exact formal root-selected proposal: retain common adult peer-rival/owned face, adult-range preservation, youthful-adult visible age E, eye/expression/style/bearing E and independently selected event/help/local warmth/recovery. No worker source change.'},'original_review':{'candidate_id':CID,'source_record_sha256':OLD['source_record_sha256'],'catalog_sha256':OLD['catalog_sha256'],'decision_sha256':LOC['row_sha256'],'artifact':LOC['file']+'#item='+str(LOC['item'])},'native_review':{'reviewer':'/root/review_08250_09250','method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
PROOF['review']['native_review']['native_contract_sha256']=s.native_contract_sha256(PROOF)
GAP={'slot_id':'anatomical_connection','semantic_fit':True,'proof_role_certified':False,'source_pointer_template':'/content/realization_content/{RID}/authored_components/obligations/0/render_gates/1/description','quote':'its face is explicitly part of that actor','actual_source_guard':T['conditions']['native_guards']['rules'][0],'reason':'The full spec includes actual owned anatomical part/whole continuity. Source explicitly requires this existing face part_of actor relation, and owner_relation consumes it. Current roles require scalar fact_refs; there is no guard-reference role path. Fabricating a scalar fact/value or fixed actor identity would strengthen or misrepresent the same actual relation. Keep source guard and all E intact; candidate approval remains pending bounded role-evidence contract disposition.'}
if __name__=='__main__':
    rec=copy.deepcopy(T);rec['content']['role_evidence']=PROOF
    s.validate(rec,CAT,corpus={'candidates':{CID:rec},'slot_bindings':{}})
    out=R/'authored/native_fresh_08250_17437_04_draft.json';assert not out.exists()
    out.write_text(json.dumps({'schema':'photo-native-pending-proof-research/v1','task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'candidate_id':CID,'status':'pending_role_evidence_contract','proof_is_not_submitted_native_approval':True,'proof_draft':PROOF,'role_gap':GAP,'actual18_read_inventory':READ,'canonical_or_operating_mutations':0},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'facts':len(F),'units':len(U),'roles':list(ROLES),'draft_raw_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
