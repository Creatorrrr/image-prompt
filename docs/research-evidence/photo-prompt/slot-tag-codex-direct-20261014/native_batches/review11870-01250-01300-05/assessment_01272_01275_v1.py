"""Fresh manual leather, two selected toy alternatives, and air-light assessment. Unsigned."""
import json,gzip,hashlib
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'native_batches/review11870-01250-01300-05';D=R/'native-inputs/prepared/review11870-01250-01300-05';I=json.loads((D/'INPUT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()))
def dig(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def f(id,d,t,p,m,vt,v,ptr,q,req,rx=None,rid='base'):return dict(id=id,dimension=d,target=t,property=p,mode=m,value={'type':vt,'value':v},pointer=ptr,quote=q,realization_id=rid,requires=req,**({'operation':'set_value','receivers':rx}if m=='effect'else{}))
rows=[]
rows.append({'ordinal':1272,'candidate_id':'cand_4bf6badb8139555bbb907f10bf7f1ea6','manual_meaning':'Caller selects actual independently existing leather surface, leather identity stays fixed. Cracked physical surface texture is selected effect, not an already-cracked prerequisite. No position, garment, prop, foreground or background is fixed.','facts':[
 f('surfaceP','subject','surface','entity.presence','prerequisite','entity.presence/v1','present','/content/application_contract','actual existing leather surface',[]),
 f('leatherP','material','surface','surface.material','prerequisite','surface.material/v1','leather','/content/application_contract','actual existing leather surface',[]),
 f('leatherEn','material','surface','surface.material','prerequisite','surface.material/v1','leather','/content/en','leather',[]),
 f('crackedEn','material','surface','surface.texture','effect','surface.texture/v1','cracked','/content/en','cracked leather texture',['surfaceP','leatherP'],[]),
 f('leatherKo','material','surface','surface.material','prerequisite','surface.material/v1','leather','/content/ko','가죽',[]),
 f('crackedKo','material','surface','surface.texture','effect','surface.texture/v1','cracked','/content/ko','갈라진 가죽 질감',['surfaceP','leatherP'],[]),
 f('leatherEmb','material','surface','surface.material','prerequisite','surface.material/v1','leather','/content/embedding_text','leather',[]),
 f('crackedEmb','material','surface','surface.texture','effect','surface.texture/v1','cracked','/content/embedding_text','cracked leather texture',['surfaceP','leatherP'],[]),
 f('crackedApp','material','surface','surface.texture','effect','surface.texture/v1','cracked','/content/application_contract','select the cracked physical texture',['surfaceP','leatherP'],[])],
 'owner_bindings':{'surface':{'origin':'existing','selector':{'kind':'selected_existing_owner'},'introduced_by':None}},
 'role_intent':{'surface_material':{'fact_refs':['leatherP','leatherEn','leatherKo','leatherEmb'],'support_modes':['prerequisite'],'rationale':'Already independently declared leather identity at selected actual surface, not visual chemistry inference.'},'texture':{'fact_refs':['crackedEn','crackedKo','crackedEmb','crackedApp'],'support_modes':['effect'],'rationale':'Explicit physical crack texture, not image damage/grain.'}},
 'unit_plan':[('base','/content/en',['leatherEn','crackedEn']),('base','/content/ko',['leatherKo','crackedKo']),('base','/content/embedding_text',['leatherEmb','crackedEmb']),('base','/content/application_contract',['surfaceP','leatherP','crackedApp'])],
 'own_binding_review':'Own unrestricted optional/direct texture .42. Its empty subject_applicability supplies no default owner. Exact material identity remains independent P for every effect and cannot be bypassed by the new surface_material tag.',
 'guard_review':'No native source rule, source conditions {}, member {}, closure {}, profile none. Actual caller owner choice is required; sourceproof cannot manufacture owner selection. Whole material E and exact texture property remain locked unless opened.',
 'rejected':['No age, manufacture, cause, aftermath history, garment/prop type, new object, foreground/default primary surface or camera artifact.'],
 'technical_pending':'Unsigned until fresh native proof and actual consumer/locks; proposal discovery may remain owner-selection required.'})

# Each tuple below is an independently judged actual alternative, not a keyword-to-tag rule.
toyfacts=[];toyunits=[];toyroles=[]
for rid,prefix,typ,identity_quote,english,korean in [
 ('small_action_figure','fig','action_figure','action figure','a small action figure prop','작은 액션 피규어 소품'),
 ('small_doll','doll','doll','doll','a small doll prop','작은 인형 소품')]:
 p='/content/realization_content/'+rid
 toyfacts.append(f(prefix+'Type','subject','toy','props.type','prerequisite','props.type/v1',typ,p+'/en',identity_quote,[],rid=rid));toyroles.append(prefix+'Type')
 # Supplied exact positive occurrences express the same qualitative size and scene-prop role in each selected RID.
 plans=[('RootEn','/content/en','small','prop'),('RootKo','/content/ko','작은','소품'),('App','/content/application_contract','Select that same object as a small scene prop','Select that same object as a small scene prop'),('En',p+'/en','small','prop'),('Ko',p+'/ko','작은','소품'),('Emb',p+'/embedding_text','small','prop'),('Concept',p+'/concept_units/0','small','prop')]
 for suffix,ptr,smallquote,propquote in plans:
  sf=prefix+'Small'+suffix;pf=prefix+'Prop'+suffix
  toyfacts.extend([f(sf,'appearance','toy','object.geometry.size','effect','object.geometry.size/v1','small',ptr,smallquote,[prefix+'Type'],[],rid),f(pf,'role','toy','props.scene_role','effect','props.scene_role/v1','scene_prop',ptr,propquote,[prefix+'Type'],[],rid)])
  toyunits.append((rid,ptr,([prefix+'Type']if suffix=='En'else[])+[sf,pf]));toyroles.append(pf)
rows.append({'ordinal':1273,'candidate_id':'cand_4ec482ddc5985c25a539fdb006516d82','manual_meaning':'Original action-figure OR doll is exactly one selected existing toy identity per actual RID. Small qualitative size and scene-prop role are two actual selected effects on that same object; precise identity is independently frozen. Human applicability is not a claim that the toy is human.','facts':toyfacts,
 'owner_bindings':{'toy':{'origin':'existing','selector':{'kind':'selected_existing_owner'},'introduced_by':None}},
 'role_intent':{'prop':{'fact_refs':toyroles,'support_modes':['prerequisite','effect'],'rationale':'Exact branch toy identity and expressly selected scene-prop role. No combined toy type and no simultaneous two-toy reading.'}},'unit_plan':toyunits,
 'own_binding_review':'Own optional/direct prop .55 with empty subject_applicability, no additional identity or default owner. Intrinsic for_any human retained independently. New tag cannot bypass selected branch props.type P or source frozen_value rule.',
 'guard_review':'Mode one actual small_action_figure and small_doll branches, each exact v2 source_target toy props.type frozen_value (action_figure versus doll), current CID/RID pinned. Existing selected owner must independently carry that precise identity; no introduced toy. Both appearance/object.geometry.size and role/props.scene_role E preserved; no scalar pre-small/pre-prop P.',
 'rejected':['No living child, actual human toy, holder, manufacture, movement, invented count or comparative size ratio/depth basis. Absolute smallness is retained as appearance E without a scale_relation claim. No separately declared parts, connections or constructed shape feature to add an object_structure role from toy category alone.'],
 'technical_pending':'Fresh unsigned branch assessment; both exact RID fullunits including root OR and selected EN/KO/embedding/concept read. Branch-specific identity/actual one-choice rejection and every E lock need fresh native execution.'})

rows.append({'ordinal':1274,'candidate_id':'cand_4eca3c15abfe5bb1b596dee912726e77','manual_meaning':'Existing actual air volume and existing scene independently required. Select visible volumetric light beams within that air region together with stated dust-and-haze optical medium. No physical surface, emitter, separately resolved dust units or humidity follows.','facts':[
 f('airP','subject','air','entity.type','prerequisite','entity.type/v1','air_volume','/content/application_contract','independently declared existing air volume',[]),
 f('sceneP','subject','scene','entity.presence','prerequisite','entity.presence/v1','present','/content/application_contract','scene bound to scene',[]),
 f('beamEn','lighting','air','lighting.shape.volumetric_beams','effect','lighting.shape.volumetric_beams/v1','visible_volumetric_beams','/content/en','visible volumetric beams through dust and haze',['airP','sceneP'],[]),
 f('mediumEn','atmosphere','air','atmosphere.medium','effect','atmosphere.medium/v1','dust_and_haze_optical_medium','/content/en','through dust and haze',['airP','sceneP'],[]),
 f('beamKo','lighting','air','lighting.shape.volumetric_beams','effect','lighting.shape.volumetric_beams/v1','visible_volumetric_beams','/content/ko','먼지와 안개 속에 보이는 빛줄기',['airP','sceneP'],[]),
 f('mediumKo','atmosphere','air','atmosphere.medium','effect','atmosphere.medium/v1','dust_and_haze_optical_medium','/content/ko','먼지와 안개 속에',['airP','sceneP'],[]),
 f('beamApp','lighting','air','lighting.shape.volumetric_beams','effect','lighting.shape.volumetric_beams/v1','visible_volumetric_beams','/content/application_contract','Select visible volumetric beams',['airP','sceneP'],[]),
 f('mediumApp','atmosphere','air','atmosphere.medium','effect','atmosphere.medium/v1','dust_and_haze_optical_medium','/content/application_contract','the stated dust-and-haze air medium',['airP','sceneP'],[])],
 'owner_bindings':{'air':{'origin':'existing','selector':{'kind':'core_role','role':'light_receiver'},'introduced_by':None},'scene':{'origin':'existing','selector':{'kind':'core_role','role':'scene'},'introduced_by':None}},
 'role_intent':{'light_shape':{'fact_refs':['beamEn','beamKo','beamApp'],'support_modes':['effect'],'rationale':'Explicit volumetric rays inside declared actual air receiving region; no surface compulsory.'},'atmospheric_medium':{'fact_refs':['mediumEn','mediumKo','mediumApp'],'support_modes':['effect'],'rationale':'Declared dust-and-haze unresolved spatial optical medium, no resolved particle distribution.'}},
 'unit_plan':[('base','/content/en',['beamEn','mediumEn']),('base','/content/ko',['beamKo','mediumKo']),('base','/content/application_contract',['airP','sceneP','beamApp','mediumApp'])],
 'own_binding_review':'Own unrestricted optional/direct light_shape .8. No human gate. Empty binding cannot supply air or scene; exact independent P retained for both effects.',
 'guard_review':'Source conditions {}, member {}, no profile or required closure. Source positive identifies same air region receiving two E; scene is declared independent prerequisite, no invented part_of or forced disjoint relation. Native sourceproof and actual effect permission remain distinct.',
 'rejected':['No independently resolved dust motes/particle units; no lamp/source type, intensity, direction, color, scattering mechanism, chemistry, humidity, rain/weather, concert/interior location, cinematic genre or material-body contour from tags.'],
 'technical_pending':'Fresh assessment only. Air type custom P must be independently witnessed exactly; actual lighting+atmosphere permissions both required, no atmosphere context demotion.'})

def at(x,p):
 for k in p.strip('/').split('/'):x=x[int(k)]if isinstance(x,list)else x[k]
 return x
for r in rows:
 cid=r['candidate_id'];r.update(original_full=P['original_records'][cid],actual_current_full=P['current_records'][cid],compiled5B_full=P['historical_compiled_rows'][cid],original_compiled_locator=I['original_decisions'][cid],required_CID_closure=P['references'][cid],required_binding_closure=P['reference_bindings'][cid],complete_ownbindings={k:v for k,v in S['slot_bindings'].items()if v['candidate_id']==cid},revision=I['required_revisions'][cid],source_after=P['current_records'][cid],source_mutations=[],native_proof=None,signature=None,root_selected=False)
 for x in r['facts']:assert x['quote']in at(r['source_after'],x['pointer'])
 r['full_units']=[{'realization_id':rid,'pointer':ptr,'quote':at(r['source_after'],ptr),'fact_refs':refs}for rid,ptr,refs in r.pop('unit_plan')]
 r['full_after_reread']='Whole actual current source including original root languages, application, every selected branch/language/embedding/concept, conditions/effects, full 5B, ownbindings and closure directly reread; manual literal facts and complete units reread. No source change.'
b={'schema':'photo-fresh-native-source-fact-assessment/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','assignment_sha256':P['assignment_sha256'],'input_sha256':dig(I),'range':[1272,1275],'actual_whole_source_closure_and_prior_complete_read_count':3,'cumulative_complete_read_count':25,'next_unread':1275,'prepared_count':50,'rows':rows,'new_proofs':0,'signatures':0,'native_approved':0,'root_approved':0,'operating':0,'boundary':'Manual fresh source interpretation and unsigned literal facts. Previous04 row statuses have no approval authority; first20 native proof executions separate.'}
p=O/'ASSESSMENT-01272-01275-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(dig(b),hashlib.sha256(p.read_bytes()).hexdigest())
