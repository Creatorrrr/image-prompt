"""Fresh explicit literals after current whole-source review, not oldproof conversion.

Only mechanical RID/pointer/ID substitution and exact source quoting serialize
these individually reviewed selected layouts. No prior proof is loaded here.
The output remains unsigned until separate final source-unit review/checks.
"""
import copy,hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
GEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb')
sys.path[:0]=[str(GEN/'scripts'),str(GEN/'precore'),str(R)]
import photo_semantic_evidence as s
import photo_candidate_corpus as c
import photo_candidate_realizations as rr
assert Path(s.__file__).resolve().is_relative_to(GEN)
assert hashlib.sha256(Path(s.__file__).read_bytes()).hexdigest()=='6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
P=R/'native-inputs/prepared/review08250-17437-05'
I=json.loads((P/'INPUT.json').read_text());ASS=json.loads((P/'ASSIGNMENT.json').read_text());PACK=json.loads((P/'PREPARED-PACKET.json').read_text())
CID='cand_d15b4c6334a45b61a7407a022a2cc8e0';T=PACK['current_records'][CID];BEFORE=PACK['original_records'][CID];OLD=PACK['historical_compiled_rows'][CID];CAT=I['catalog_review']['after']
assert c.digest(I)=='faf550f8a11003978f6af3e25b505035b8a9654bcc31558c053e5c7251ae5160'
CHOICES=[('baseline',[]),('setback',['setback']),('help',['help']),('mouth_warmth',['mouth_warmth']),('cheek_warmth',['cheek_warmth']),('recovery',['recovery']),('setback_mouth_warmth',['setback','mouth_warmth']),('setback_cheek_warmth',['setback','cheek_warmth']),('setback_recovery',['setback','recovery']),('help_mouth_warmth',['help','mouth_warmth']),('help_cheek_warmth',['help','cheek_warmth']),('help_recovery',['help','recovery']),('mouth_warmth_recovery',['mouth_warmth','recovery']),('cheek_warmth_recovery',['cheek_warmth','recovery']),('setback_mouth_warmth_recovery',['setback','mouth_warmth','recovery']),('setback_cheek_warmth_recovery',['setback','cheek_warmth','recovery']),('help_mouth_warmth_recovery',['help','mouth_warmth','recovery']),('help_cheek_warmth_recovery',['help','cheek_warmth','recovery'])]
assert set(rr.ids(T))=={rid for rid,_ in CHOICES}
F=[];U=[];GS=[];MAPS={};LAYOUTS=[]
def fact(rid,key,p,q,d,t,prop,mode,value,req,typ=None):
 row=dict(id='g05_'+rid+'_'+key,realization_id=rid,pointer=p,quote=q,dimension=d,target=t,property=prop,mode=mode,value={'type':typ or prop+'/v1','value':value},requires=list(req))
 if mode=='effect':row.update(operation='set_value',receivers=[])
 assert q in s.positive_string(T,p,realization_id=rid),(rid,p,q)
 F.append(row);return row['id']
def unit(rid,p,refs,relation=None,rationale=None,guards=None):
 row=dict(realization_id=rid,pointer=p,quote=s.positive_string(T,p,realization_id=rid),fact_refs=list(refs),disposition='semantic_reference' if relation else ('semantic' if refs or guards else 'nonsemantic'))
 if relation:row.update(reference_relation=relation,retained_constraint_rationale=rationale)
 if guards:row['guard_refs']=guards
 U.append(row)
COMMON_RATIONALE='Keep the same existing adult peer-rival and owned face, deliberate main_subject/primary_face application restriction without arbitrary identity, all adult body/face preservation and youthful-adult age E, haughty eyes/full facial baseline/poised bearing/fresh styling. One-up is optional already-declared context only. Four required groups and three independent optional groups remain; no second participant or childlike morphology from label/reference/face-size/hair. Canonical facts stay at exact same-RID normal fields, not borrowed into shorter local phrases.'
LOCAL={
'setback':'The local visible small setback belongs to this rival. No new actor/object/injury/humiliation/private feeling; any actually used concrete instrument must already be independently declared. Event is E, not an incoming setback P. No automatic tool inclusion.',
'help':'Same rival receives visible help from independently existing distinct helper; both paired action E owners and source disjoint guard remain. Any actually used concrete instrument must independently exist and retain its owner. A helper may be an independently named counterpart only with actual core identity. No separate counterpart, returned item, hand contact or new helper is compulsory.',
'mouth_warmth':'Brief local mouth-corner softening interrupts the smirk while same selected adult haughty eye baseline remains readable. Instruction supplies brief/local full E; gate retains readability only. Not whole-face-age proof, incoming eye-state P, global smile, gratitude, past event or mandatory cheek color.',
'cheek_warmth':'One bounded visible warm-color cue on this rival cheek, with cheek presence. Gate refers to that exact selected instruction, retaining locality/ownership and exclusions. No temperature, makeup pigment, diagnosis/private emotion, duplicate skin-state E or forced mouth softening.',
'recovery':'Visible attempt restores superior smirk OR poised composure at selected attempt phase, after independently declared prior disruption P. Gate constrains readable attempt/continuing baseline, not an independent full goal/whole-face age witness. No completed recovery, elapsed sequence, hidden suppression, or mandatory selected setback/warmth.'}
for rid,kinds in CHOICES:
 root='/content/realization_content/'+rid;ob=root+'/authored_components/obligations/0';ip=ob+'/instruction';gp=ob+'/render_gates';ids={}
 def a(key,p,q,d,t,prop,m,val,req,typ=None):
  ids[key]=fact(rid,key,p,q,d,t,prop,m,val,req,typ);return ids[key]
 a('present',ip,'already declared adult peer-rival role','subject','actor','entity.presence','prerequisite','present',[])
 a('face',ip,'already existing owned face','subject','actor_face','anatomy.face.presence','prerequisite','present',[ids['present']])
 a('adult',ip,'already declared adult peer-rival role','age','actor','age.declared','prerequisite','adult',[ids['present']])
 a('role',ip,'already declared adult peer-rival role','role','actor','participant.role.peer_rival','prerequisite','declared',[ids['present']])
 for key,target,prop in [('body_adult','actor','age.presentation.body'),('face_adult','actor_face','age.presentation.face')]:
  a(key,ip,'Preserve unmistakably adult body and face presentation','age',target,prop,'prerequisite','unmistakably_adult',[ids['present']]+([ids['face']] if target=='actor_face' else []))
 for key,target,prop in [('keep_body','actor','age.presentation.body'),('keep_face','actor_face','age.presentation.face')]:
  a(key,ip,'Preserve unmistakably adult body and face presentation','age',target,prop,'preservation','same',[ids['present']]+([ids['face']] if target=='actor_face' else []),'frozen_property_reference/v1')
 a('eyes',ip,'haughty half-lidded eyes','subject','actor_face','anatomy.eyes.presence','prerequisite','present',[ids['present'],ids['face']])
 for key,q in [('eyelids','owns the haughty eyelids'),('brow','haughty eyelids, brow, mouth'),('mouth','haughty eyelids, brow, mouth')]:
  a(key,gp+'/1/description',q,'subject','actor_face','anatomy.'+key+'.presence','prerequisite','present',[ids['present'],ids['face']])
 required=list(ids.values())
 for key,q,d,t,prop,val,p in [
  ('eye_effect','haughty half-lidded eyes','appearance','actor_face','eyes.structure.lid_opening','haughty_half_lidded',ip),
  ('style','fresh youthful adult styling','appearance','actor','presentation.fresh_youthful_adult_styling','fresh_youthful_adult_styling',ip),
  ('pose','poised bearing','pose','actor','body.pose.poised_bearing','poised',ip),
  ('age_effect','visibly youthful-adult age presentation','age','actor','age.presentation.youthful_adult','youth_appearing_adult',ip),
  ('expression','haughty smug poised baseline','expression','actor_face','face.expression.haughty_smug_baseline','haughty_smug_poised',gp+'/3/description')]:a(key,p,q,d,t,prop,'effect',val,required)
 common=list(ids.values())
 unit(rid,ip,[f['id'] for f in F if f['realization_id']==rid and f['pointer']==ip])
 unit(rid,ip,[ids['expression']],'selected_output_constraint',COMMON_RATIONALE+' The smug-poised instruction and haughty-eye clause are narrower than full facial haughty/smug/poised; exact full expression is at selected gate3.')
 gid='g05_'+rid+'_face_part_of_actor';source_cond=T['conditions'];rule=source_cond['native_guards']['rules'][0]
 GS.append({'schema':s.GUARD_SUPPORT_SCHEMA,'id':gid,'realization_id':rid,'pointer':gp+'/1/description','quote':'its face is explicitly part of that actor','mode':'prerequisite','guard':{'schema':source_cond['native_guards']['schema'],'declaring_candidate_id':CID,'declaring_realization_id':rid,'source_condition_index':0,'conditions_sha256':c.digest(source_cond),'rule_id':'rival_owned_face','rule_sha256':c.digest(rule)},'endpoints':{'left_role':{'candidate_id':CID,'target':'actor_face'},'right_role':{'candidate_id':CID,'target':'actor'}},'semantic_projection':{'dimension':'body_geometry','target':'actor_face','property':'anatomy.connection.face_part_of_actor'}})
 unit(rid,gp+'/1/description',[ids[k] for k in ['eyelids','brow','mouth']],guards=[gid])
 unit(rid,gp+'/1/description',[ids[k] for k in ['present','face','role','eye_effect','expression','pose']],'same_selected_owner',COMMON_RATIONALE+' Named eyelids/brow-region/mouth and face belong to same actor; direct guard support binds actual face part_of actor, no scalar entityID fact or eyebrow hair. Narrow anatomy phrase is not full expression.')
 unit(rid,gp+'/3/description',[ids['expression']])
 unit(rid,gp+'/3/description',[ids[k] for k in ['role','adult','style','age_effect']],'partial_restatement',COMMON_RATIONALE+' Fresh-only gate does not independently prove full youthful-adult styling or peer-rival role.')
 for prefix in ['/content/authored_components/obligations/0',ob]:
  for gi,keys in [(0,['adult','body_adult','face_adult','keep_body','keep_face','age_effect']),(1,['present','face','role','eyelids','brow','mouth','eye_effect','expression','pose']),(2,['style','eye_effect','expression','pose']),(3,['role','adult','expression','style','age_effect'])]:
   p=prefix+f'/render_gates/{gi}/description'
   if p in {gp+'/1/description',gp+'/3/description'}:continue
   unit(rid,p,[ids[k] for k in keys],'selected_output_constraint',COMMON_RATIONALE+' Local gate retains its exact age/owner/readability/optional and exclusion constraints without manufacturing absent complete qualifiers.')
 unit(rid,'/content/authored_components/obligations/0/instruction',common,'selected_output_constraint',COMMON_RATIONALE)
 unit(rid,'/content/semantics/definition',common,'partial_restatement',COMMON_RATIONALE)
 selectedrefs=[]
 for oi,kind in enumerate(kinds,1):
  op=root+f'/authored_components/obligations/{oi}/instruction';og=root+f'/authored_components/obligations/{oi}/render_gates/0/description';cr=root+f'/concept_units/{oi}'
  if kind=='setback':refs=[a('setback',op,'same declared rival experiences one visible small setback','event','actor','situation.small_setback','effect','visible_local_small_setback',required,'event.small_setback/v1')]
  elif kind=='help':
   hp=a('helper',op,'separately established helper','subject','helper','entity.presence','prerequisite','present',[ids['present']])
   refs=[hp,a('help_receive',op,'declared rival receives visible help from a separately established helper','action','actor','action.interaction.receives_help','effect','visible_help_from_bound_helper',required+[hp]),a('help_provide',op,'declared rival receives visible help from a separately established helper','action','helper','action.interaction.provides_help','effect','visible_help_to_bound_actor',required+[hp])]
  elif kind=='mouth_warmth':refs=[a('mouth_warmth',op,"brief local softening of the rival's mouth corner",'expression','actor_face','face.expression.mouth_corner_warm_crack','effect','brief_local_mouth_corner_softening',required)]
  elif kind=='cheek_warmth':
   cp=a('cheek',op,"rival's cheek",'subject','actor_face','anatomy.cheek.presence','prerequisite','present',[ids['present'],ids['face']])
   refs=[cp,a('cheek_color',op,"bounded visible warm-color cue appears on the rival's cheek",'appearance','actor_face','skin.color.localized_cheek_warm_color','effect','bounded_visible_local_cheek_color_warming',required+[cp])]
  else:
   assert kind=='recovery'
   pp=a('prior_disruption',op,'after a declared brief disruption','timing','actor','narrative.context.prior_disruption','prerequisite','declared',[ids['present']],'narrative.prior_disruption/v1')
   refs=[pp,a('recovery_expression',op,'visibly tries to restore the superior smirk or poised composure','expression','actor_face','face.expression.composure_recovery_attempt','effect','visible_attempt_to_restore_superior_smirk_or_poised_composure',required+[pp]),a('recovery_phase',op,'selected instant represents a recovery attempt','timing','actor','narrative.phase.recovery_attempt','effect','recovery_attempt',required+[pp])]
  unit(rid,op,refs)
  continuing=[ids['eye_effect'],ids['expression']] if kind in {'mouth_warmth','cheek_warmth','recovery'} else []
  if continuing:unit(rid,op,continuing,'selected_output_constraint',LOCAL[kind])
  unit(rid,og,refs+continuing,'selected_output_constraint',LOCAL[kind])
  unit(rid,cr,refs+continuing,'selected_output_constraint',LOCAL[kind]);selectedrefs+=refs
 for tail in ['/en','/embedding_text','/ko','/semantics/definition','/semantics/paraphrase_examples/0']:
  unit(rid,root+tail,common+selectedrefs,'selected_output_constraint',COMMON_RATIONALE+' Actual selected groups: '+(', '.join(kinds) or 'none')+'. '+ ' '.join(LOCAL[k] for k in kinds)+' Whole EN/KO bodies retain their exact common clauses; a shorter local eye-baseline fragment is never whole-face-age preservation evidence. Korean instrument clauses are read with the complete any-concrete-instrument existing-if-used condition; no instrument is made compulsory or newly created.')
 unit(rid,root+'/concept_units/0',common,'selected_output_constraint',COMMON_RATIONALE)
 descriptors=[('도도한','haughty_descriptor',['role','adult','expression']),('잘난 척하는','outward_smug_descriptor',['role','adult','expression']),('건방지고 도도하지만','outward_haughty_cheeky_descriptor',['adult','expression','age_effect']),('smug','outward_smug_descriptor',['role','adult','expression']),('haughty','haughty_descriptor',['role','adult','expression'])]
 for pi,(q,val,keys) in enumerate(descriptors):
  p='/content/semantics/paraphrase_examples/'+str(pi);ref=fact(rid,'descriptor_'+str(pi),p,q,'concept','actor','character.outward_descriptor','context',val,[ids['present']]);unit(rid,p,[ref]);unit(rid,p,[ids[k] for k in keys],'partial_restatement','Keep this exact outward descriptor/adult and any stated youthful-adult presentation. Rival alone is not peer, peer alone not rival, and neither a new person/private personality. Full canonical role/age/expression remain at their exact same-RID direct anchors; descriptor C cannot replace baseline E/P.')
 p='/content/semantics/paraphrase_examples/5';ref=fact(rid,'optional_one_up',p,'teasing one-up','event','actor','event.context.one_up','context','teasing_one_up',[ids['present']]);unit(rid,p,[ref])
 for prefix,ac in [('/content/authored_components',T['content']['authored_components']),(root+'/authored_components',T['content']['realization_content'][rid]['authored_components'])]:
  for oi,obl in enumerate(ac['obligations']):
   controls=[prefix+f'/obligations/{oi}/evidence/{ei}/field' for ei,_ in enumerate(obl['evidence'])]
   controls += [prefix+f'/obligations/{oi}/evidence/{ei}/requirement/must_not_contain/{j}' for ei,evidence in enumerate(obl['evidence']) for j,_ in enumerate(evidence['requirement'].get('must_not_contain',[]))]
   controls += [prefix+f'/obligations/{oi}/render_gates/{j}/review_scale' for j,_ in enumerate(obl['render_gates'])]
   for p in controls:
    if p in s.primary_paths(T,rid):unit(rid,p,[])
 assert {u['pointer'] for u in U if u['realization_id']==rid}==s.primary_paths(T,rid)
 bindings=[{'target':'actor','core_role':'main_subject','origin':'existing','introduced_by':None},{'target':'actor_face','core_role':'primary_face','origin':'existing','introduced_by':None}]
 if 'help' in kinds:bindings.append({'target':'helper','core_role':'secondary_subject','origin':'existing','introduced_by':None})
 MAPS[rid]={'schema':s.OWNER_SCHEMA,'bindings':bindings};LAYOUTS.append({'rid':rid,'selected':kinds})
role_defs={'age_presentation':(['age.declared','age.presentation.body','age.presentation.face','age.presentation.youthful_adult'],['prerequisite','preservation','effect']),'expression':(['face.expression.haughty_smug_baseline','face.expression.mouth_corner_warm_crack','face.expression.composure_recovery_attempt'],['effect']),'eye_detail':(['eyes.structure.lid_opening'],['effect']),'presentation_style':(['presentation.fresh_youthful_adult_styling'],['effect']),'body_pose':(['body.pose.poised_bearing'],['effect']),'participant_role':(['participant.role.peer_rival'],['prerequisite']),'skin_tone':(['skin.color.localized_cheek_warm_color'],['effect']),'action':(['action.interaction.receives_help','action.interaction.provides_help'],['effect']),'relational_action':(['action.interaction.receives_help','action.interaction.provides_help'],['effect']),'narrative_phase':(['narrative.phase.recovery_attempt'],['effect']),'situation_context':(['situation.small_setback'],['effect'])}
ROLES={}
for tag,(props,modes) in role_defs.items():
 rows=[f for f in F if f['property'] in props and f['mode'] in modes];rids=[rid for rid,_ in CHOICES if any(f['realization_id']==rid for f in rows)]
 ROLES[tag]={'spec_sha256':c.digest(CAT[tag]),'scope':'whole_record' if len(rids)==18 else 'positive_alternative','realization_ids':rids,'fact_refs':[f['id'] for f in rows],'support_modes':modes}
ROLES['anatomical_connection']={'spec_sha256':c.digest(CAT['anatomical_connection']),'scope':'whole_record','realization_ids':[rid for rid,_ in CHOICES],'fact_refs':[],'guard_refs':[g['id'] for g in GS],'support_modes':['prerequisite']}
LOC=I['original_decisions'][CID]
PROOF={'schema':s.SCHEMA,'meaning_sha256':s.meaning_sha256(T),'catalog_sha256':c.digest(CAT),'complete':True,'facts':F,'source_units':U,'guard_supports':GS,'owner_maps':MAPS,'roles':ROLES,'effect_sets':{rid:s.effect_set(T,rid) for rid,_ in CHOICES},'dependencies':{rid:[] for rid,_ in CHOICES},'reference_sha256':{},'guard_sets':{rid:s.source_guard_set(T,rid,{'candidates':{CID:T},'slot_bindings':{}}) for rid,_ in CHOICES},'profile_contracts':{rid:rr.profile_contract(T,rid) for rid,_ in CHOICES},'review':{'basis':'Fresh formal05 original/current/whole exact5B/item188/ownbindings and empty closure; all18 selected whole bodies, all204 precision occurrences reviewed with bounded exact/RID-prefix repeat factoring. Scalar facts have exact normal primary anchors; local partial meanings use one-hop references; existing actual face part_of actor is a source-guard prerequisite, not a scalar identity or mutation. All actual E/owners/modes/requirements and adult/bodyface preservation remain. Source unchanged from exact INPUT. Separate final whole-unit review/checks precede submission.','whole_source_reviewed':True,'source_correction':{'before_sha256':s.meaning_sha256(BEFORE),'after_sha256':s.meaning_sha256(T),'rationale':'Exact root-selected proposed source of formal05, not operating canonical application. Common baseline and explicit independent actual18 choices preserve youthful-adult age E, body/face adult prerequisites/preservation, help/setback/local color/mouth/recovery conditions. No worker source mutation.'},'original_review':{'candidate_id':CID,'source_record_sha256':OLD['source_record_sha256'],'catalog_sha256':OLD['catalog_sha256'],'decision_sha256':LOC['row_sha256'],'artifact':LOC['file']+'#item='+str(LOC['item'])},'native_review':{'reviewer':'/root/review_08250_09250','method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
if __name__=='__main__':
 out=R/'authored/native_fresh_08250_17437_05_unsigned.json';assert not out.exists();out.write_text(json.dumps({'proof_draft':PROOF,'selected_layouts':LAYOUTS,'source_after':T,'unsigned':True,'candidate_native_approval':False},ensure_ascii=False,indent=2)+'\n');print(len(F),len(U),len(GS),hashlib.sha256(out.read_bytes()).hexdigest())
