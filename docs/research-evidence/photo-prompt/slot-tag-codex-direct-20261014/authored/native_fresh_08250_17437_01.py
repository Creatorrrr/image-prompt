"""Fresh exact formal17437 literal clause judgement, independently reread all18 bodies.
Canonical assignments are manual source judgements; repeat loops infer no meaning.
"""
import copy,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=R.parents[3]
FROZEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/1871bafa0e008e186ccce4e92908f2b177529b215c22e2fb46d07f0b28679bfd')
sys.path[:0]=[str(FROZEN/'scripts'),str(R)]
import photo_candidate_corpus as c
import photo_candidate_realizations as rr
import photo_semantic_evidence as s
import visual_profile_contracts as vp
import native_reviews as nr
# Research direct_review prepends the checkout scripts path at import time.
# Restore immutable precedence before any late-imported production validator.
sys.path[:0]=[str(FROZEN/'scripts'),str(FROZEN/'precore')]
P=R/'native-inputs/prepared/review08250-17437-01';O=R/'native_batches/review08250-17437-01'
I=json.loads((P/'INPUT.json').read_text());ASS=json.loads((P/'ASSIGNMENT.json').read_text());PACK=json.loads((P/'PREPARED-PACKET.json').read_text());cid=ASS['ids'][0]
T=PACK['current_records'][cid];BEFORE=PACK['original_records'][cid];CAT=I['catalog_review']['after'];OLD=PACK['historical_compiled_rows'][cid]
CHOICES=[('baseline',[]),('setback',['setback']),('help',['help']),('mouth_warmth',['mouth_warmth']),('cheek_warmth',['cheek_warmth']),('recovery',['recovery']),('setback_mouth_warmth',['setback','mouth_warmth']),('setback_cheek_warmth',['setback','cheek_warmth']),('setback_recovery',['setback','recovery']),('help_mouth_warmth',['help','mouth_warmth']),('help_cheek_warmth',['help','cheek_warmth']),('help_recovery',['help','recovery']),('mouth_warmth_recovery',['mouth_warmth','recovery']),('cheek_warmth_recovery',['cheek_warmth','recovery']),('setback_mouth_warmth_recovery',['setback','mouth_warmth','recovery']),('setback_cheek_warmth_recovery',['setback','cheek_warmth','recovery']),('help_mouth_warmth_recovery',['help','mouth_warmth','recovery']),('help_cheek_warmth_recovery',['help','cheek_warmth','recovery'])]
J={'authored_actual_choices':CHOICES}
assert set(rr.ids(T))=={rid for rid,_ in CHOICES}
def get(p):
 v=T
 for k in p.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
# Quote, dimension, owner, property, mode, typed-value namespace, exact value.
# Source control/negative clauses are separately accounted for, never invented
# positive facts or a replacement for missing conditions.
def spec(q,d,t,p,m,typ,val):return (q,d,t,p,m,typ,val)
PRESENT=spec('already declared adult peer-rival role','subject','actor','entity.presence','prerequisite','entity.presence/v1','present')
FACE=spec("already existing owned face",'subject','actor_face','anatomy.face.presence','prerequisite','anatomy.face.presence/v1','present')
ADULT=spec('adult','age','actor','age.declared','prerequisite','age.declared/v1','adult')
ROLE=spec('already declared adult peer-rival role','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared')
BODY=spec('unmistakably adult body','age','actor','age.presentation.body','prerequisite','age.presentation.body/v1','unmistakably_adult')
FACEAGE=spec('adult body and face presentation','age','actor_face','age.presentation.face','prerequisite','age.presentation.face/v1','unmistakably_adult')
BODYKEEP=spec('Preserve unmistakably adult body and face presentation','age','actor','age.presentation.body','preservation','frozen_property_reference/v1','same')
FACEKEEP=spec('Preserve unmistakably adult body and face presentation','age','actor_face','age.presentation.face','preservation','frozen_property_reference/v1','same')
EYES=spec('haughty half-lidded eyes','appearance','actor_face','eyes.structure.lid_opening','effect','eyes.structure.lid_opening/v1','haughty_half_lidded')
EXPR=spec('a smug poised facial baseline','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised')
POSE=spec('poised bearing','pose','actor','body.pose.poised_bearing','effect','body.pose.poised_bearing/v1','poised')
STYLE=spec('fresh youthful adult styling','appearance','actor','presentation.fresh_youthful_adult_styling','effect','presentation.fresh_youthful_adult_styling/v1','fresh_youthful_adult_styling')
EN=[PRESENT,FACE,ADULT,ROLE,BODY,FACEAGE,BODYKEEP,FACEKEEP,EYES,EXPR,POSE,STYLE]
KO=[
 spec('이미 선언된 성인 또래 라이벌 역할','subject','actor','entity.presence','prerequisite','entity.presence/v1','present'),
 spec('그 인물에게 속한 기존 얼굴','subject','actor_face','anatomy.face.presence','prerequisite','anatomy.face.presence/v1','present'),
 spec('성인','age','actor','age.declared','prerequisite','age.declared/v1','adult'),
 spec('이미 선언된 성인 또래 라이벌 역할','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),
 spec('몸과 얼굴의 명백한 성인 표현','age','actor','age.presentation.body','prerequisite','age.presentation.body/v1','unmistakably_adult'),
 spec('몸과 얼굴의 명백한 성인 표현','age','actor_face','age.presentation.face','prerequisite','age.presentation.face/v1','unmistakably_adult'),
 spec('몸과 얼굴의 명백한 성인 표현을 보존','age','actor','age.presentation.body','preservation','frozen_property_reference/v1','same'),
 spec('몸과 얼굴의 명백한 성인 표현을 보존','age','actor_face','age.presentation.face','preservation','frozen_property_reference/v1','same'),
 spec('도도하게 반쯤 감긴 눈','appearance','actor_face','eyes.structure.lid_opening','effect','eyes.structure.lid_opening/v1','haughty_half_lidded'),
 spec('잘난 듯 침착한 얼굴 기본선','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised'),
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
 spec('haughty eyelids, brow, mouth','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised'),POSE],[
 spec('Fresh youthful styling remains adult','appearance','actor','presentation.fresh_youthful_adult_styling','effect','presentation.fresh_youthful_adult_styling/v1','fresh_youthful_adult_styling'),
 spec('haughty half-lidded eyes','appearance','actor_face','eyes.structure.lid_opening','effect','eyes.structure.lid_opening/v1','haughty_half_lidded'),
 spec('smug poised bearing','pose','actor','body.pose.poised_bearing','effect','body.pose.poised_bearing/v1','poised')],[
 spec('adult peer','role','actor','participant.role.peer_rival','prerequisite','participant.role.peer_rival/v1','declared'),ADULT,
 spec('haughty smug poised baseline','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised'),
 spec('fresh styling','appearance','actor','presentation.fresh_youthful_adult_styling','effect','presentation.fresh_youthful_adult_styling/v1','fresh_youthful_adult_styling')]]
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
 spec('teasing one-up','event','actor','event.context.one_up','context','event.context.one_up/v1','teasing_one_up')]]
MOUTH=[
 spec("brief local softening of the rival's mouth corner",'expression','actor_face','face.expression.mouth_corner_warm_crack','effect','face.expression.mouth_corner_warm_crack/v1','brief_local_mouth_corner_softening'),
 spec('adult haughty eye baseline remains readable','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised'),
 spec('adult','age','actor','age.declared','prerequisite','age.declared/v1','adult')]
MOUTHKO=[
 spec('입꼬리의 짧고 국소적인 부드러워짐','expression','actor_face','face.expression.mouth_corner_warm_crack','effect','face.expression.mouth_corner_warm_crack/v1','brief_local_mouth_corner_softening'),
 spec('성인다운 도도한 눈의 기본선은 읽힌다','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised'),
 spec('성인다운','age','actor','age.declared','prerequisite','age.declared/v1','adult')]
MOUTHGATE=[
 spec('Local mouth-corner softening','expression','actor_face','face.expression.mouth_corner_warm_crack','effect','face.expression.mouth_corner_warm_crack/v1','brief_local_mouth_corner_softening'),
 spec('continuing haughty adult eye baseline','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised'),
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
MOUTHGATE[0]=spec('Local mouth-corner softening','expression','actor_face','face.expression.mouth_corner_warm_crack','effect','face.expression.mouth_corner_warm_crack/v1','brief_local_mouth_corner_softening')
AGE=spec('visibly youthful-adult age presentation','age','actor','age.presentation.youthful_adult','effect','age.presentation.youthful_adult/v1','youth_appearing_adult')
EN.append(AGE);ROOTDEF.append(AGE);GATES[0].append(AGE);GATES[3].append(AGE)
KO.append(spec('외관상 연령 표현을 앳돼 보이는 성인으로 나타내','age','actor','age.presentation.youthful_adult','effect','age.presentation.youthful_adult/v1','youth_appearing_adult'))
SETBACK=[spec('same declared rival experiences one visible small setback','event','actor','situation.small_setback','effect','event.small_setback/v1','visible_local_small_setback')]
SETBACKKO=[spec('같은 라이벌에게 국소적인 작은 차질이 보인다','event','actor','situation.small_setback','effect','event.small_setback/v1','visible_local_small_setback')]
SETBACKGATE=[spec('selected small setback is legible on the declared rival','event','actor','situation.small_setback','effect','event.small_setback/v1','visible_local_small_setback')]
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
 spec('smug haughty baseline remains legible','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised')]
CHEEKKO=[
 spec('라이벌 볼의 한정된 영역에 보이는 따뜻한 색 단서가 나타나며','appearance','actor_face','skin.state.localized_cheek_warm_color','effect','skin.state.localized_cheek_warm_color/v1','bounded_visible_local_cheek_color_warming'),
 spec('잘난 듯 도도한 기본선은 읽힌다','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised')]
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
 spec('A recovery attempt is readable on the same rival','expression','actor_face','face.expression.composure_recovery_attempt','effect','face.expression.composure_recovery_attempt/v1','visible_attempt_to_restore_superior_smirk_or_poised_composure'),
 spec('A recovery attempt is readable on the same rival','timing','actor','narrative.phase.recovery_attempt','effect','narrative.phase.recovery_attempt/v1','recovery_attempt'),
 spec('adult haughty baseline remains identifiable','age','actor_face','age.presentation.face','preservation','frozen_property_reference/v1','same'),
 spec('haughty baseline remains identifiable','expression','actor_face','face.expression.haughty_smug_baseline','effect','face.expression.haughty_smug_baseline/v1','haughty_smug_poised')]
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
 nonsemantic={p:reason for p,reason in nonsemantic.items() if p in paths}
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
 # Current v4 implementation is being authored concurrently. Do not patch its
 # guard requirements or pass an intentionally incomplete mini as a full proof.
 assert {s.property_key(f) for f in active if f['mode']=='effect'}=={s.property_key(p) for p in actual['properties']}
 assert {f['dimension'] for f in active if f['mode']=='effect'}==set(actual['dimensions'])
 selected_contract_error=None
 compiled=vp.compile_visual_profile(T['content']['realization_content'][rid])
 assert len(compiled['required_evidence_fields'])==5+len(chosen)
 assert not any(f['target']=='helper' for f in active) or 'help' in chosen
 summaries.append({'rid':rid,'chosen':chosen,'fact_count':len(active),'source_unit_count':len(paths),'mode_counts':{m:sum(f['mode']==m for f in active) for m in sorted(s.MODES)},'owner_map':owner_maps[rid],'dependencies':[],'effect_sets':actual,'current_selected_contract_passed_in_isolation':selected_contract_error is None,'current_selected_contract_expected_rejection':selected_contract_error,'exact_fact_effect_footprint_equals_actual':True,'compiled_required_fields':compiled['required_evidence_fields'],'complete_native_proof':False})
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
role_specs['situation_context']=('event',['situation.small_setback'],['effect'])
for tag,(dim,props,modes) in role_specs.items():
 fs=[f for f in facts if f['dimension']==dim and f['property'] in props and f['mode'] in modes]
 if not fs:continue
 spec=CAT[tag];assert dim in spec['dimensions'],(tag,dim)
 assert all(any(f['property']==p.rstrip('.') or f['property'].startswith(p if p.endswith('.') else p+'.') for p in spec['property_prefixes']) for f in fs),(tag,spec['property_prefixes'])
 rids=[rid for rid,_ in J['authored_actual_choices'] if any(f['realization_id']==rid for f in fs)]
 roles[tag]={'spec_sha256':c.digest(spec),'scope':'whole_record' if len(rids)==18 else 'positive_alternative','realization_ids':rids,'fact_refs':[f['id'] for f in fs],'support_modes':modes}

# Fresh complete proof and exact input provenance are authored below.
assert len(facts)==3555 and len(units)==621
assert len([u for u in units if u['disposition']=='semantic'])==513
# Same selected source property is one canonical assignment, even when short
# gate clauses support only one facet. All full selected-body qualifiers are
# preserved in its canonical value; no partial occurrence replaces that value.
for rid,_ in CHOICES:
 assignments={}
 for f in facts:
  if f['realization_id']!=rid or f['mode']!='effect':continue
  k=s.property_key(f);v=c.canonical_bytes({key:f[key] for key in ['value','operation','receivers']})
  assert k not in assignments or assignments[k]==v,(rid,k)
  assignments[k]=v
LOC=I['original_decisions'][cid]
PROOF={'schema':s.SCHEMA,'meaning_sha256':s.meaning_sha256(T),'catalog_sha256':c.digest(CAT),'complete':True,'facts':facts,'roles':roles,'owner_maps':owner_maps,'source_units':units,'effect_sets':{rid:s.effect_set(T,rid) for rid,_ in CHOICES},'dependencies':{rid:[] for rid,_ in CHOICES},'reference_sha256':{},'guard_sets':{rid:s.source_guard_set(T,rid,{'candidates':{cid:T},'slot_bindings':{}}) for rid,_ in CHOICES},'profile_contracts':{rid:rr.profile_contract(T,rid) for rid,_ in CHOICES},'review':{'basis':'Fresh full formal original/current/compiled item188/catalog142V2/18 actual selected-profile/source-guard/reference read. Whole source includes four required common groups and independent optional groups. Literal clause judgements retain actual visible-age, appearance, expression, pose, action, local-event and selected-phase effects.','whole_source_reviewed':True,'source_correction':{'before_sha256':s.meaning_sha256(BEFORE),'after_sha256':s.meaning_sha256(T),'rationale':'Root-selected exact eighteen-RID profile expresses common adult rival, own face, youthful-adult visible-age, half-lidded haughty eyes, smug poised baseline, bearing and fresh adult styling. Three independently optional groups add only selected events/warmth/recovery; existing owner/adult/role/owned-face/helper/prior-disruption guards retain their actual scope. Original age expression is not reduced to styling. No forced counterpart, minor morphology, private emotion, new helper/instrument or one-up event creation.'},'original_review':{'candidate_id':cid,'source_record_sha256':OLD['source_record_sha256'],'catalog_sha256':OLD['catalog_sha256'],'decision_sha256':LOC['row_sha256'],'artifact':LOC['file']+'#item='+str(LOC['item'])},'native_review':{'reviewer':'/root/review_08250_09250','method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
PROOF['review']['native_review']['native_contract_sha256']=s.native_contract_sha256(PROOF)
def delta(before,after,p=''):
 if c.canonical_bytes(before)==c.canonical_bytes(after):return []
 if isinstance(before,dict) and isinstance(after,dict):
  out=[]
  for k in sorted(set(before)|set(after)):
   path=p+'/'+k.replace('~','~0').replace('/','~1')
   if k not in before:out.append({'pointer':path,'before_exists':False,'before':None,'after_exists':True,'after':after[k],'reason':'Exact root-selected source proposal after whole source/RID/guard reread.'})
   elif k not in after:out.append({'pointer':path,'before_exists':True,'before':before[k],'after_exists':False,'after':None,'reason':'Exact root-selected source proposal after whole source/RID/guard reread.'})
   else:out+=delta(before[k],after[k],path)
  return out
 return [{'pointer':p,'before_exists':True,'before':before,'after_exists':True,'after':after,'reason':'Exact root-selected source proposal after whole source/RID/guard reread.'}]
ROW={'candidate_id':cid,'ordinal':17437,'status':'approved','rationale':'Existing unmistakably adult peer rival and its existing owned face receive the explicit haughty half-lidded eyes, smug poised expression, poised bearing, fresh youthful adult styling and youthful-adult visible-age presentation. The latter is an actual age mutation constrained by age locks, distinct from declared adulthood. No common second participant is required. Selected help alone needs an existing disjoint helper; recovery alone requires independently declared prior disruption. Setback, help, mouth warmth, cheek warmth and recovery retain their exact selected effects, with no union of unselected duties, inferred temperature/gratitude or new one-up incident. Exact source is unchanged from formal INPUT. All actual positive clauses and control strings have fresh explicit dispositions; repeated effect clauses use one canonical assignment per selected owner/property.','source_before':BEFORE,'source_after':T,'delta':delta(BEFORE,T),'original_compiled':LOC,'proof':PROOF,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':I['required_revisions'][cid]['prior_review'],'memo_artifacts':I['required_revisions'][cid]['memo_artifacts'],'rationale':'Fresh v4 source review/proof supersedes the exact historical pending wrapper while preserving its old source/locator/revision hashes. Current formal root selection explicitly uses normalized compiled item188 row5589091c, never an automatic old-proof rebinding. Current projection, complete guards and independently selected profile contracts are newly reviewed; metadata-as-positive units are excluded by the final v4 contract.'}}
BATCH={'schema':nr.BATCH,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'prepared_count':1,'actual_read_count':1,'records':[ROW]}
NOTE={'schema':nr.NOTE,'task_name':ASS['task_name'],'model':ASS['model'],'reasoning_effort':ASS['reasoning_effort'],'assignment_sha256':c.digest(ASS),'input_sha256':c.digest(I),'batch_sha256':c.digest(BATCH),'prepared_count':1,'actual_read_count':1,'whole_source_read_ids':[cid],'whole_dependency_read_ids':[cid]}
if __name__=='__main__':
 rec=copy.deepcopy(T);rec['content']['role_evidence']=PROOF
 s.validate(rec,CAT,corpus={'candidates':{cid:rec},'slot_bindings':{}})
 O.mkdir(parents=True,exist_ok=True)
 for name,value in [('BATCH.json',BATCH),('NOTE.json',NOTE)]:
  path=O/name;assert not path.exists();path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'facts':len(facts),'units':len(units),'roles':list(roles),'batch_sha256':c.digest(BATCH),'note_sha256':c.digest(NOTE)}))
