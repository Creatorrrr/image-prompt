"""Eighteen actual-RID manual clause-fact inventory; no automatic classification.

Exact literal blueprints below are authored semantic decisions. Loops only
expand the explicitly listed repeated source strings and verify shape/quotes.
"""
import copy,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(Path.cwd()/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import photo_candidate_realizations as rr
import photo_semantic_evidence as s
import visual_profile_contracts as vp
J=json.loads((R/'authored/native_resolution_08250_revision3_sources.json').read_text())
cid='cand_d15b4c6334a45b61a7407a022a2cc8e0';T=J['resolution_proposed_records'][cid]
CAT=json.loads((R/'CATALOG-FINAL-142.json').read_text())
def get(p):
 v=T
 for k in p.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
# Quote, dimension, owner, property, mode, typed-value namespace, exact value.
# Source control/negative clauses are separately accounted for, never invented
# positive facts or a replacement for missing conditions.
def spec(q,d,t,p,m,typ,val):return (q,d,t,p,m,typ,val)
PRESENT=spec('already declared adult peer-rival role','subject','actor','entity.presence','prerequisite','entity.presence/v1','present')
FACE=spec("already existing owned face",'subject','actor_face','entity.presence','prerequisite','entity.presence/v1','present')
ADULT=spec('adult','age','actor','age.declared','prerequisite','age.declared/v1','adult')
ROLE=spec('already declared adult peer-rival role','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared')
BODY=spec('unmistakably adult body','age','actor','age.presentation.body','prerequisite','age.presentation.body/v1','unmistakably_adult')
FACEAGE=spec('adult body and face presentation','age','actor_face','age.presentation.face','prerequisite','age.presentation.face/v1','unmistakably_adult')
BODYKEEP=spec('Preserve unmistakably adult body and face presentation','age','actor','age.presentation.body','preservation','frozen_property_reference/v1','same')
FACEKEEP=spec('Preserve unmistakably adult body and face presentation','age','actor_face','age.presentation.face','preservation','frozen_property_reference/v1','same')
EYES=spec('haughty half-lidded eyes','appearance','actor_face','eyes.structure.lid_opening','effect','eyes.structure.lid_opening/v1','haughty_half_lidded')
EXPR=spec('a smug poised facial baseline','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','smug_poised')
POSE=spec('poised bearing','pose','actor','body.pose.poised_bearing','effect','body.pose.poised_bearing/v1','poised')
STYLE=spec('fresh youthful adult styling','appearance','actor','presentation.fresh_youthful_adult_styling','effect','presentation.fresh_youthful_adult_styling/v1','fresh_youthful_adult_styling')
EN=[PRESENT,FACE,ADULT,ROLE,BODY,FACEAGE,BODYKEEP,FACEKEEP,EYES,EXPR,POSE,STYLE]
KO=[
 spec('이미 선언된 성인 또래 라이벌 역할','subject','actor','entity.presence','prerequisite','entity.presence/v1','present'),
 spec('그 인물에게 속한 기존 얼굴','subject','actor_face','entity.presence','prerequisite','entity.presence/v1','present'),
 spec('성인','age','actor','age.declared','prerequisite','age.declared/v1','adult'),
 spec('이미 선언된 성인 또래 라이벌 역할','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),
 spec('몸과 얼굴의 명백한 성인 표현','age','actor','age.presentation.body','prerequisite','age.presentation.body/v1','unmistakably_adult'),
 spec('몸과 얼굴의 명백한 성인 표현','age','actor_face','age.presentation.face','prerequisite','age.presentation.face/v1','unmistakably_adult'),
 spec('몸과 얼굴의 명백한 성인 표현을 보존','age','actor','age.presentation.body','preservation','frozen_property_reference/v1','same'),
 spec('몸과 얼굴의 명백한 성인 표현을 보존','age','actor_face','age.presentation.face','preservation','frozen_property_reference/v1','same'),
 spec('도도하게 반쯤 감긴 눈','appearance','actor_face','eyes.structure.lid_opening','effect','eyes.structure.lid_opening/v1','haughty_half_lidded'),
 spec('잘난 듯 침착한 얼굴 기본선','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','smug_poised'),
 spec('도도하게 균형 잡힌 태도','pose','actor','body.pose.poised_bearing','effect','body.pose.poised_bearing/v1','poised'),
 spec('산뜻하고 젊은 성인의 차림','appearance','actor','presentation.fresh_youthful_adult_styling','effect','presentation.fresh_youthful_adult_styling/v1','fresh_youthful_adult_styling')]
ROOTDEF=[
 spec('already declared unmistakably adult peer rival','subject','actor','entity.presence','prerequisite','entity.presence/v1','present'),FACE,ADULT,
 spec('already declared peer-rival role is a prerequisite','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),EYES,EXPR,POSE,STYLE]
GATES=[[
 spec('declared peer rival','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),ADULT,
 spec('unmistakably adult in body and face presentation','age','actor','age.presentation.body','prerequisite','age.presentation.body/v1','unmistakably_adult'),
 spec('unmistakably adult in body and face presentation','age','actor_face','age.presentation.face','prerequisite','age.presentation.face/v1','unmistakably_adult')],[
 spec('already declared peer-rival actor','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),
 spec('haughty eyelids, brow, mouth','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_owned_facial_baseline'),POSE],[
 spec('Fresh youthful styling remains adult','appearance','actor','presentation.fresh_youthful_adult_styling','effect','presentation.fresh_youthful_adult_styling/v1','fresh_youthful_adult_styling'),
 spec('haughty half-lidded eyes','appearance','actor_face','eyes.structure.lid_opening','effect','eyes.structure.lid_opening/v1','haughty_half_lidded'),
 spec('smug poised bearing','pose','actor','body.pose.poised_bearing','effect','body.pose.poised_bearing/v1','smug_poised')],[
 spec('adult peer','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),ADULT,
 spec('haughty smug poised baseline','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised'),
 spec('fresh styling','appearance','actor','presentation.fresh_youthful_adult_styling','effect','presentation.fresh_youthful_adult_styling/v1','fresh_styling')]]
PARAPHRASES=[[
 spec('성인','age','actor','age.declared','prerequisite','age.declared/v1','adult'),
 spec('라이벌','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),
 spec('도도한','concept','actor','character.outward_descriptor','context','character.outward_descriptor/v1','haughty_descriptor')],[
 spec('성인','age','actor','age.declared','prerequisite','age.declared/v1','adult'),
 spec('라이벌','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),
 spec('잘난 척하는','concept','actor','character.outward_descriptor','context','character.outward_descriptor/v1','outward_smug_descriptor')],[
 spec('성인','age','actor','age.declared','prerequisite','age.declared/v1','adult'),
 spec('건방지고 도도하지만','concept','actor','character.outward_descriptor','context','character.outward_descriptor/v1','outward_haughty_cheeky_descriptor'),
 # Substantive unresolved effect: do not disguise this as styling/context.
 spec('앳돼 보이는 성인 인물','age','actor','age.presentation.youthful_adult','effect','age.presentation.youthful_adult/v1','youth_appearing_adult')],[
 spec('adult','age','actor','age.declared','prerequisite','age.declared/v1','adult'),
 spec('rival','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),
 spec('smug','concept','actor','character.outward_descriptor','context','character.outward_descriptor/v1','outward_smug_descriptor')],[
 spec('adult','age','actor','age.declared','prerequisite','age.declared/v1','adult'),
 spec('peer','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),
 spec('haughty','concept','actor','character.outward_descriptor','context','character.outward_descriptor/v1','haughty_descriptor')],[
 spec('teasing one-up','event','actor','event.context.one_up','context','event.context.one_up/v1','optional_already_declared_teasing_one_up')]]
MOUTH=[
 spec("brief local softening of the rival's mouth corner",'expression','actor_face','face.expression.mouth_corner_warm_crack','effect','face.expression.mouth_corner_warm_crack/v1','brief_local_mouth_corner_softening'),
 spec('adult haughty eye baseline remains readable','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','continuing_haughty_eye_baseline'),
 spec('adult','age','actor','age.declared','prerequisite','age.declared/v1','adult')]
MOUTHKO=[
 spec('입꼬리의 짧고 국소적인 부드러워짐','expression','actor_face','face.expression.mouth_corner_warm_crack','effect','face.expression.mouth_corner_warm_crack/v1','brief_local_mouth_corner_softening'),
 spec('성인다운 도도한 눈의 기본선은 읽힌다','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','continuing_haughty_eye_baseline'),
 spec('성인다운','age','actor','age.declared','prerequisite','age.declared/v1','adult')]
MOUTHGATE=[
 spec('Local mouth-corner softening','expression','actor_face','face.expression.mouth_corner_warm_crack','effect','face.expression.mouth_corner_warm_crack/v1','brief_local_mouth_corner_softening'),
 spec('continuing haughty adult eye baseline','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','continuing_haughty_eye_baseline'),
 spec('adult','age','actor','age.declared','prerequisite','age.declared/v1','adult')]

# Explicit quote-specific refinements discovered during manual recheck.
# 'adult peer' does not by itself assert a rival; common peer-rival prerequisite
# is separately supported by the complete positive application instruction.
GATES[3][0]=spec('adult peer','role','actor','participant.role.peer','prerequisite','participant.role.peer/v1','declared')
PARAPHRASES[4][1]=spec('peer','role','actor','participant.role.peer','prerequisite','participant.role.peer/v1','declared')
# Adult-looking eye baseline is not independent biological/declared age proof.
MOUTH[2]=spec('adult haughty eye baseline remains readable','age','actor_face','age.presentation.face','preservation','frozen_property_reference/v1','same')
MOUTHKO[2]=spec('성인다운 도도한 눈의 기본선은 읽힌다','age','actor_face','age.presentation.face','preservation','frozen_property_reference/v1','same')
MOUTHGATE[2]=spec('continuing haughty adult eye baseline','age','actor_face','age.presentation.face','preservation','frozen_property_reference/v1','same')
MOUTHGATE[0]=spec('Local mouth-corner softening','expression','actor_face','face.expression.mouth_corner_warm_crack','effect','face.expression.mouth_corner_warm_crack/v1','local_mouth_corner_softening')
AGE=spec('visibly youthful-adult age presentation','age','actor','age.presentation.youthful_adult','effect','age.presentation.youthful_adult/v1','youth_appearing_adult')
EN.append(AGE);ROOTDEF.append(AGE);GATES[0].append(AGE);GATES[3].append(AGE)
KO.append(spec('외관상 연령 표현을 앳돼 보이는 성인으로 나타내','age','actor','age.presentation.youthful_adult','effect','age.presentation.youthful_adult/v1','youth_appearing_adult'))
SETBACK=[spec('same declared rival experiences one visible small setback','event','actor','event.small_setback','effect','event.small_setback/v1','visible_local_small_setback')]
SETBACKKO=[spec('같은 라이벌에게 국소적인 작은 차질이 보인다','event','actor','event.small_setback','effect','event.small_setback/v1','visible_local_small_setback')]
SETBACKGATE=[spec('selected small setback is legible on the declared rival','event','actor','event.small_setback','effect','event.small_setback/v1','visible_local_small_setback')]
HELP=[
 spec('separately established helper','subject','helper','entity.presence','prerequisite','entity.presence/v1','present'),
 spec('declared rival receives visible help from a separately established helper','action','actor','action.interaction.receives_help','effect','action.interaction.receives_help/v1','visible_help_from_bound_helper'),
 spec('declared rival receives visible help from a separately established helper','action','helper','action.interaction.provides_help','effect','action.interaction.provides_help/v1','visible_help_to_bound_actor')]
HELPKO=[
 spec('별도로 이미 정해진 도움 제공자','subject','helper','entity.presence','prerequisite','entity.presence/v1','present'),
 spec('정해진 라이벌이 별도로 이미 정해진 도움 제공자에게 도움을 받는다','action','actor','action.interaction.receives_help','effect','action.interaction.receives_help/v1','visible_help_from_bound_helper'),
 spec('정해진 라이벌이 별도로 이미 정해진 도움 제공자에게 도움을 받는다','action','helper','action.interaction.provides_help','effect','action.interaction.provides_help/v1','visible_help_to_bound_actor')]
HELPGATE=[
 spec('separately declared helper','subject','helper','entity.presence','prerequisite','entity.presence/v1','present'),
 spec('Help has a separately declared helper and the same rival as recipient','action','actor','action.interaction.receives_help','effect','action.interaction.receives_help/v1','visible_help_from_bound_helper'),
 spec('Help has a separately declared helper and the same rival as recipient','action','helper','action.interaction.provides_help','effect','action.interaction.provides_help/v1','visible_help_to_bound_actor')]
CHEEK=[
 spec("bounded visible warm-color cue appears on the rival's cheek",'appearance','actor_face','skin.state.localized_cheek_warm_color','effect','skin.state.localized_cheek_warm_color/v1','bounded_visible_local_cheek_color_warming'),
 spec('smug haughty baseline remains legible','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','continuing_smug_haughty_baseline')]
CHEEKKO=[
 spec('라이벌 볼의 한정된 영역에 보이는 따뜻한 색 단서가 나타나며','appearance','actor_face','skin.state.localized_cheek_warm_color','effect','skin.state.localized_cheek_warm_color/v1','bounded_visible_local_cheek_color_warming'),
 spec('잘난 듯 도도한 기본선은 읽힌다','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','continuing_smug_haughty_baseline')]
CHEEKGATE=[
 # 'The bounded cheek cue' is an anaphor for the exact selected cheek-color
 # manifestation, not an independent diagnosis or an inferred new hue.
 spec('The bounded cheek cue belongs to the same adult rival','appearance','actor_face','skin.state.localized_cheek_warm_color','effect','skin.state.localized_cheek_warm_color/v1','bounded_visible_local_cheek_color_warming'),
 spec('adult rival','age','actor','age.declared','prerequisite','age.declared/v1','adult')]
RECOVERY=[
 spec('after a declared brief disruption','timing','actor','narrative.context.prior_disruption','prerequisite','narrative.prior_disruption/v1','declared'),
 spec('visibly tries to restore the superior smirk or poised composure','expression','actor_face','face.expression.composure_recovery_attempt','effect','face.expression.composure_recovery_attempt/v1','visible_attempt_to_restore_superior_smirk_or_poised_composure'),
 spec('selected instant represents a recovery attempt','timing','actor','narrative.phase.recovery_attempt','effect','narrative.phase.recovery_attempt/v1','recovery_attempt')]
RECOVERYKO=[
 spec('이미 이야기상 정해진 짧은 흔들림 뒤','timing','actor','narrative.context.prior_disruption','prerequisite','narrative.prior_disruption/v1','declared'),
 spec('우월한 미소나 도도한 태도를 되찾으려는 시도가 보인다','expression','actor_face','face.expression.composure_recovery_attempt','effect','face.expression.composure_recovery_attempt/v1','visible_attempt_to_restore_superior_smirk_or_poised_composure'),
 spec('선택한 순간은 회복 시도를 나타내며','timing','actor','narrative.phase.recovery_attempt','effect','narrative.phase.recovery_attempt/v1','recovery_attempt')]
RECOVERYGATE=[
 spec('A recovery attempt is readable on the same rival','expression','actor_face','face.expression.composure_recovery_attempt','effect','face.expression.composure_recovery_attempt/v1','visible_attempt_to_restore_selected_facial_composure'),
 spec('A recovery attempt is readable on the same rival','timing','actor','narrative.phase.recovery_attempt','effect','narrative.phase.recovery_attempt/v1','recovery_attempt'),
 spec('adult haughty baseline remains identifiable','age','actor_face','age.presentation.face','preservation','frozen_property_reference/v1','same'),
 spec('haughty baseline remains identifiable','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','continuing_haughty_baseline')]
EVENT_SPECS={'setback':(SETBACK,SETBACKKO,SETBACKGATE),'help':(HELP,HELPKO,HELPGATE),'mouth_warmth':(MOUTH,MOUTHKO,MOUTHGATE),'cheek_warmth':(CHEEK,CHEEKKO,CHEEKGATE),'recovery':(RECOVERY,RECOVERYKO,RECOVERYGATE)}
facts=[];units=[];ledger=[];summaries=[];owner_maps={};roles={}
for rid,chosen in J['authored_actual_choices']:
 root='/content/realization_content/'+rid
 refs={key:rid+'_'+key for key in ['present','face','adult','role','body_adult','face_adult','keep_body','keep_face']}
 anchorpath=root+'/concept_units/0';anchor_specs=[PRESENT,FACE,ADULT,ROLE,BODY,FACEAGE,BODYKEEP,FACEKEEP]
 def add(p,sp,id=None,requires=None):
  q,d,t,prop,mode,typ,val=sp
  row={'id':id or rid+'_f'+str(len(facts)+1),'realization_id':rid,'pointer':p,'quote':q,'dimension':d,'target':t,'property':prop,'mode':mode,'value':{'type':typ,'value':val},'requires':[] if requires is None else list(requires)}
  if mode=='effect':row.update(operation='set_value',receivers=[])
  s._fact_valid(row);assert q in s.positive_string(T,p,realization_id=rid),(rid,p,q)
  facts.append(row);return row
 for key,sp in zip(refs,anchor_specs):
  req=[] if key=='present' else [refs['present']]
  if key in ['face_adult','keep_face']:req.append(refs['face'])
  add(anchorpath,sp,refs[key],req)
 required=list(refs.values())
 if 'help' in chosen:
  ci=chosen.index('help')+1;p=root+'/concept_units/'+str(ci)
  refs['helper']=rid+'_existing_helper';add(p,HELP[0],refs['helper'],[refs['present']]);required.append(refs['helper'])
 if 'recovery' in chosen:
  ci=chosen.index('recovery')+1;p=root+'/concept_units/'+str(ci)
  refs['prior_disruption']=rid+'_prior_disruption';add(p,RECOVERY[0],refs['prior_disruption'],[refs['present']]);required.append(refs['prior_disruption'])
 templates={}
 english_paths=['/content/authored_components/obligations/0/instruction',root+'/authored_components/obligations/0/instruction',root+'/en',root+'/embedding_text',root+'/concept_units/0',root+'/semantics/definition']
 for p in english_paths:templates[p]=list(EN)
 templates['/content/semantics/definition']=list(ROOTDEF)
 for p in [root+'/ko',root+'/semantics/paraphrase_examples/0']:templates[p]=list(KO)
 for prefix in ['/content/authored_components',root+'/authored_components']:
  for gi,gs in enumerate(GATES):templates[prefix+f'/obligations/0/render_gates/{gi}/description']=list(gs)
 for pi,ps in enumerate(PARAPHRASES):templates['/content/semantics/paraphrase_examples/'+str(pi)]=list(ps)
 for ci,k in enumerate(chosen,1):
  ens,kos,gs=EVENT_SPECS[k]
  for p in [root+'/en',root+'/embedding_text',root+'/semantics/definition']:templates[p]+=ens
  for p in [root+'/ko',root+'/semantics/paraphrase_examples/0']:templates[p]+=kos
  for p in [root+'/concept_units/'+str(ci),root+f'/authored_components/obligations/{ci}/instruction']:templates[p]=list(ens)
  templates[root+f'/authored_components/obligations/{ci}/render_gates/0/description']=list(gs)
 for p,specs in templates.items():
  for sp in specs:
   if p==anchorpath and sp in anchor_specs:continue
   if 'helper' in refs and p==root+'/concept_units/'+str(chosen.index('help')+1) and sp==HELP[0]:continue
   if 'prior_disruption' in refs and p==root+'/concept_units/'+str(chosen.index('recovery')+1) and sp==RECOVERY[0]:continue
   mode=sp[4];target=sp[2]
   req=required if mode=='effect' else ([refs['face']] if target=='actor_face' else [refs['present']])
   add(p,sp,requires=req)
 paths=s.primary_paths(T,rid);nonsemantic={}
 for prefix,ac in [('/content/authored_components',T['content']['authored_components']),(root+'/authored_components',T['content']['realization_content'][rid]['authored_components'])]:
  for oi,ob in enumerate(ac['obligations']):
   for ei,e in enumerate(ob['evidence']):
    base=f'{prefix}/obligations/{oi}/evidence/{ei}';nonsemantic[base+'/field']='Schema field identifier, not positive evidence.'
    for ni in range(len(e['requirement'].get('must_not_contain',[]))):nonsemantic[base+f'/requirement/must_not_contain/{ni}']='Negative lexical exclusion, not positive age/person evidence.'
   for gi in range(len(ob['render_gates'])):nonsemantic[f'{prefix}/obligations/{oi}/render_gates/{gi}/review_scale']='Review-scale schema label.'
 assert paths==set(templates)|set(nonsemantic),(rid,paths-set(templates)-set(nonsemantic))
 for p in sorted(paths):
  fs=[f for f in facts if f['realization_id']==rid and f['pointer']==p]
  units.append({'realization_id':rid,'pointer':p,'quote':get(p),'fact_refs':[f['id'] for f in fs],'disposition':'semantic' if fs else 'nonsemantic'})
  if not fs:assert p in nonsemantic;ledger.append({'rid':rid,'pointer':p,'quote':get(p),'clause_kind':'schema_or_negative_control','reason':nonsemantic[p]})
 active=[f for f in facts if f['realization_id']==rid];ids={f['id'] for f in active};assert all(set(f['requires'])<=ids for f in active)
 bindings=[{'target':'actor','core_role':'main_subject','origin':'existing','introduced_by':None},{'target':'actor_face','core_role':'primary_face','origin':'existing','introduced_by':None}]
 if 'help' in chosen:bindings.append({'target':'helper','core_role':'secondary_subject','origin':'existing','introduced_by':None})
 owner_maps[rid]={'schema':s.OWNER_SCHEMA,'bindings':bindings};s._validate_owner_map(owner_maps[rid],active)
 actual=rr.effects(T,rid);mini={'facts':active,'owner_maps':{rid:owner_maps[rid]},'effect_sets':{rid:actual}}
 s._selected_contract(mini,rid,actual)
 compiled=vp.compile_visual_profile(T['content']['realization_content'][rid])
 assert len(compiled['required_evidence_fields'])==5+len(chosen)
 assert not any(f['target']=='helper' for f in active) or 'help' in chosen
 summaries.append({'rid':rid,'chosen':chosen,'fact_count':len(active),'source_unit_count':len(paths),'mode_counts':{m:sum(f['mode']==m for f in active) for m in sorted(s.MODES)},'owner_map':owner_maps[rid],'dependencies':[],'effect_sets':actual,'current_selected_contract_passed_in_isolation':True,'compiled_required_fields':compiled['required_evidence_fields'],'complete_native_proof':False})
# Direct role decisions against final142 full specs. The peer-rival prerequisite
# never certifies a visually inferred relationship or a second participant.
role_specs={
 'age_presentation':('age',['age.declared','age.presentation.body','age.presentation.face','age.presentation.youthful_adult'],['prerequisite','preservation','effect']),
 'expression':('expression',['face.expression.haughty_smug_baseline','face.expression.mouth_corner_warm_crack','face.expression.composure_recovery_attempt'],['effect']),
 'eye_detail':('appearance',['eyes.structure.lid_opening'],['effect']),
 'presentation_style':('appearance',['presentation.fresh_youthful_adult_styling'],['effect']),
 'body_pose':('pose',['body.pose.poised_bearing'],['effect']),
 'participant_role':('role',['participant.role.peer_rival','participant.role.peer'],['prerequisite']),
 'skin_condition':('appearance',['skin.state.localized_cheek_warm_color'],['effect']),
 'action':('action',['action.interaction.receives_help','action.interaction.provides_help'],['effect']),
 'relational_action':('action',['action.interaction.receives_help','action.interaction.provides_help'],['effect']),
 'narrative_phase':('timing',['narrative.phase.recovery_attempt'],['effect'])}
for tag,(dim,props,modes) in role_specs.items():
 fs=[f for f in facts if f['dimension']==dim and f['property'] in props and f['mode'] in modes]
 if not fs:continue
 spec=CAT[tag];assert dim in spec['dimensions'],(tag,dim)
 assert all(any(f['property']==p.rstrip('.') or f['property'].startswith(p if p.endswith('.') else p+'.') for p in spec['property_prefixes']) for f in fs),(tag,spec['property_prefixes'])
 rids=[rid for rid,_ in J['authored_actual_choices'] if any(f['realization_id']==rid for f in fs)]
 roles[tag]={'spec_sha256':c.digest(spec),'scope':'whole_record' if len(rids)==18 else 'positive_alternative','realization_ids':rids,'fact_refs':[f['id'] for f in fs],'support_modes':modes}
out={'schema':'native-manual-clause-fact-inventory-draft/v1','task_name':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high','candidate_id':cid,'source_proposal_meaning_sha256':s.meaning_sha256(T),'catalog_sha256':c.digest(CAT),'actual_RIDs_total':18,'actual_authored_fact_count':len(facts),'source_unit_count':len(units),'facts':facts,'source_units':units,'nonsemantic_unit_dispositions':ledger,'roles':roles,'owner_maps':owner_maps,'effect_sets':{rid:rr.effects(T,rid) for rid,_ in J['authored_actual_choices']},'dependencies':{rid:[] for rid,_ in J['authored_actual_choices']},'reference_sha256':{},'summaries':summaries,'status':'manual_18RID_fact_inventory_draft_not_a_complete_native_proof','native_proof_attached':False,'operating_native_qualified_count':0,'current_full_native_contract_unsupported':['conditions.native_guards','visual_profile realization_content','MAX_REALIZATIONS8/MAX_FACTS128/MAX_UNITS256'],'root_resource_proposal_not_implemented':{'maxRID':32,'maxUnits':2048,'maxFacts':4096},'qualification_issues':[{'actual_selected_RIDs':[rid for rid,chosen in J['authored_actual_choices'] if 'setback' in chosen],'exact_pointer':'/content/realization_content/setback/concept_units/1','exact_quote':'The same declared rival experiences one visible small setback.','actual_property':'event.small_setback','semantically_applicable_role':'situation_context','role_property_prefixes':CAT['situation_context']['property_prefixes'],'issue':'Local small setback is a concrete circumstance, not a specific newly invented action mechanism or central narrative. Current effect property event.small_setback does not satisfy final142 situation_context prefix. Do not fabricate a role fact with a different actual property. Root may adjudicate an exact source/fact property spelling correction to situation.small_setback with identical local-event meaning.'}],'proof_boundary':'Exact quote/shape/same-RID requires/owned footprint/isolated selected contract and compiler checks do not certify semantic accuracy or new guard enforcement.'}
(R/'authored/native_resolution_08250_revision3_facts.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'facts':len(facts),'source_units':len(units),'RID_count':len(summaries),'by_RID':[{k:v for k,v in x.items() if k in ['rid','fact_count','source_unit_count']} for x in summaries],'roles':list(roles),'native_approved':0},ensure_ascii=False,indent=2))

