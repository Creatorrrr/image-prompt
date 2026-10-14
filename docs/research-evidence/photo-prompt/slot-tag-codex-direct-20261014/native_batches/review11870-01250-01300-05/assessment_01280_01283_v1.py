"""Fresh manual selected ghost association, seasonal scene, and affect; unsigned."""
import json,gzip,hashlib
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'native_batches/review11870-01250-01300-05';D=R/'native-inputs/prepared/review11870-01250-01300-05';I=json.loads((D/'INPUT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()))
def dig(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def f(id,d,t,p,m,vt,v,ptr,q,req,rx=None):return dict(id=id,dimension=d,target=t,property=p,mode=m,value={'type':vt,'value':v},pointer=ptr,quote=q,realization_id='base',requires=req,**({'operation':'set_value','receivers':rx}if m=='effect'else{}))
scene={'scene':{'origin':'existing','selector':{'kind':'core_role','role':'scene'},'introduced_by':None}}
rows=[]
rows.append({'ordinal':1280,'candidate_id':'cand_a4264973dbb75e66a503644e2bdbf55c','manual_meaning':'Independently existing scene receives room-with-window setting AND authored ghost-bride association. Ghost association is actual selected conceptual meaning, never already-frozen context, P or optional deletion. It does not introduce ghost/bride/haunting/history/visible supernatural detail.','facts':[
 f('sceneP','subject','scene','entity.presence','prerequisite','entity.presence/v1','present','/content/application_contract','independently declared existing scene',[]),
 f('placeEn','setting','scene','setting.location','effect','setting.location/v1','room_with_window','/content/en','a ghost-bride window room',['sceneP'],[]),
 f('assocEn','concept','scene','narrative.association','effect','narrative.association/v1','authored_ghost_bride_association','/content/en','ghost-bride',['sceneP'],[]),
 f('placeKo','setting','scene','setting.location','effect','setting.location/v1','room_with_window','/content/ko','창가 방',['sceneP'],[]),
 f('assocKo','concept','scene','narrative.association','effect','narrative.association/v1','authored_ghost_bride_association','/content/ko','유령 신부의',['sceneP'],[]),
 f('placeEmb','setting','scene','setting.location','effect','setting.location/v1','room_with_window','/content/embedding_text','a ghost-bride window room',['sceneP'],[]),
 f('assocEmb','concept','scene','narrative.association','effect','narrative.association/v1','authored_ghost_bride_association','/content/embedding_text','ghost-bride',['sceneP'],[]),
 f('placeApp','setting','scene','setting.location','effect','setting.location/v1','room_with_window','/content/application_contract','select the stated room-with-window setting',['sceneP'],[]),
 f('assocApp','concept','scene','narrative.association','effect','narrative.association/v1','authored_ghost_bride_association','/content/application_contract','its authored ghost-bride association',['sceneP'],[])],
 'owner_bindings':scene,'role_intent':{'location':{'fact_refs':['placeEn','placeKo','placeEmb','placeApp'],'support_modes':['effect'],'rationale':'Explicit physical room-with-window place on actual scene, retaining separate authored ghost association E.'}},
 'unit_plan':[('/content/en',['placeEn','assocEn']),('/content/ko',['placeKo','assocKo']),('/content/embedding_text',['placeEmb','assocEmb']),('/content/application_contract',['sceneP','placeApp','assocApp'])],
 'own_binding_review':'Own unrestricted optional/direct location .58. No source/native/member conditions, no requiredclosure/profile. Existing scene exact neutralP independently consumed.',
 'guard_review':'Both setting and concept selected E retained on same actual scene. Concept dimension often protected and must stay consumer-denied when locked; sourceproof may qualify source meaning without opening it. Authored association is not an independently frozen world/history fact.',
 'rejected':['No bride/ghost/apparition, actual haunting, earlier death/marriage event, visible supernatural detail, persistent world rule, concrete local action/event, central narrative relationship, occasion or declared offscreenparticipant. Title-like association alone is not narrative_core, visibleclue, world, genre or surreal scene law. Association E remains untagged, not demoted/deleted.'],
 'technical_pending':'Unsigned source assessment. Actual concept+setting permission/locks must be checked; no ordinary protected concept permission invented for positiveconsumer.'})
rows.append({'ordinal':1281,'candidate_id':'cand_a4438b65dd42584e8bbdce1be798ccf6','manual_meaning':'Same independently existing scene receives beach-shoreline place and summer seasonal timing. Explicit seasonal contextual role is real selected timing E; neither summer nor shoreline is required as preexisting state.','facts':[
 f('sceneP','subject','scene','entity.presence','prerequisite','entity.presence/v1','present','/content/application_contract','independently declared scene',[]),
 f('placeEn','setting','scene','setting.location','effect','setting.location/v1','beach_shoreline','/content/en','beach shoreline',['sceneP'],[]),
 f('seasonEn','timing','scene','timing.season','effect','timing.season/v1','summer','/content/en','summer',['sceneP'],[]),
 f('placeKo','setting','scene','setting.location','effect','setting.location/v1','beach_shoreline','/content/ko','해변 물가',['sceneP'],[]),
 f('seasonKo','timing','scene','timing.season','effect','timing.season/v1','summer','/content/ko','여름',['sceneP'],[]),
 f('placeEmb','setting','scene','setting.location','effect','setting.location/v1','beach_shoreline','/content/embedding_text','beach shoreline',['sceneP'],[]),
 f('seasonEmb','timing','scene','timing.season','effect','timing.season/v1','summer','/content/embedding_text','summer',['sceneP'],[]),
 f('placeApp','setting','scene','setting.location','effect','setting.location/v1','beach_shoreline','/content/application_contract','Select beach-shoreline setting',['sceneP'],[]),
 f('seasonApp','timing','scene','timing.season','effect','timing.season/v1','summer','/content/application_contract','summer seasonal timing',['sceneP'],[])],
 'owner_bindings':scene,'role_intent':{'location':{'fact_refs':['placeEn','placeKo','placeEmb','placeApp'],'support_modes':['effect'],'rationale':'Actual selected beach shoreline setting on existing scene.'},'season':{'fact_refs':['seasonEn','seasonKo','seasonEmb','seasonApp'],'support_modes':['effect'],'rationale':'Explicit summer season, not inferred from beach and not frozen context despite contextual slot role.'}},
 'unit_plan':[('/content/en',['placeEn','seasonEn']),('/content/ko',['placeKo','seasonKo']),('/content/embedding_text',['placeEmb','seasonEmb']),('/content/application_contract',['sceneP','placeApp','seasonApp'])],
 'own_binding_review':'Own unrestricted optional/direct location .52; source conditions/member {}, no closure/profile. No human/swimmer prerequisite from portrait metadata.',
 'guard_review':'Neutral existing sceneP only; two mutable effects in setting/timing. Actual same scene selector, no geography/weather/temperature/holiday facts and no fake pre-summer P.',
 'rejected':['No swimmer, country, weather, measured heat, vacation/travel event, newbeachobject or portraitsubject.'],
 'technical_pending':'Unsigned until fullcompact actualconsumer/P/each whole setting/timing dimension and property checks.'})
rows.append({'ordinal':1282,'candidate_id':'cand_a73d6bd56d5158ed942b5f533c803c08','manual_meaning':'Glitch anxiety selects affective atmosphere for independently existing scene. Current corrected embedding explicitly rejects robot proof/identity/anchor; glitch mood does not authorize image signal artifacts, robot entity or private diagnosis.','facts':[
 f('sceneP','subject','scene','entity.presence','prerequisite','entity.presence/v1','present','/content/application_contract','independently declared scene',[]),
 f('moodEn','atmosphere','scene','mood.atmosphere','effect','mood.atmosphere/v1','glitch_anxiety','/content/en','glitch anxiety',['sceneP'],[]),
 f('moodKo','atmosphere','scene','mood.atmosphere','effect','mood.atmosphere/v1','glitch_anxiety','/content/ko','글리치 불안감',['sceneP'],[]),
 f('moodEmb','atmosphere','scene','mood.atmosphere','effect','mood.atmosphere/v1','glitch_anxiety','/content/embedding_text','glitch anxiety as an affective mood',['sceneP'],[]),
 f('moodApp','atmosphere','scene','mood.atmosphere','effect','mood.atmosphere/v1','glitch_anxiety','/content/application_contract','Glitch anxiety is a mood selection',['sceneP'],[])],
 'owner_bindings':scene,'role_intent':{'mood':{'fact_refs':['moodEn','moodKo','moodEmb','moodApp'],'support_modes':['effect'],'rationale':'Declared proposed affective reading of scene; no private diagnosis or actual measured air state.'}},
 'unit_plan':[('/content/en',['moodEn']),('/content/ko',['moodKo']),('/content/embedding_text',['moodEmb']),('/content/application_contract',['sceneP','moodApp'])],
 'own_binding_review':'Own unrestricted optional/contextual mood .66. Contextual role label is not proof that actual selected mood is pre-frozen context; precise actualscene P and atmosphere E retained.',
 'guard_review':'No source/native/member conditions or profile/closure. Mood E remains actualmutable atmosphere at scene, no camera/style effect from glitch token, no diagnosedactualanxiety.',
 'rejected':['No actualrobot, robotidentity, realityanchor relationship, particular encoding/signal artifact, physicalhaze/airhumidity, private mentalstate or clinicaldiagnosis. Originalbadembedding robot-proof implication not inherited into corrected current meaning.'],
 'technical_pending':'Unsigned until fresh fullcompact nativeproof/actualconsumer/atmosphereproperty and wholelocks. All semantic sourcecorrections exactly INPUT current, no further change.'})
for r in rows:
 cid=r['candidate_id'];r.update(original_full=P['original_records'][cid],actual_current_full=P['current_records'][cid],compiled5B_full=P['historical_compiled_rows'][cid],original_compiled_locator=I['original_decisions'][cid],required_CID_closure=P['references'][cid],required_binding_closure=P['reference_bindings'][cid],complete_ownbindings={k:v for k,v in S['slot_bindings'].items()if v['candidate_id']==cid},revision=I['required_revisions'][cid],source_after=P['current_records'][cid],source_mutations=[],native_proof=None,signature=None,root_selected=False)
 for x in r['facts']:assert x['quote']in r['source_after']['content'][x['pointer'].split('/')[-1]]
 r['full_units']=[{'realization_id':'base','pointer':p,'quote':r['source_after']['content'][p.split('/')[-1]],'fact_refs':refs}for p,refs in r.pop('unit_plan')]
 r['full_after_reread']='Full original/current/ENKOembeddingApp/exact5B/ownbindings/emptyclosure/SHAequalwholeorigin/pinned04 completefacts+units+roles+maps+guards+review read. All manual literal facts/fullunits and unchanged after reread. No source edit.'
b={'schema':'photo-fresh-native-source-fact-assessment/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','assignment_sha256':P['assignment_sha256'],'input_sha256':dig(I),'range':[1280,1283],'actual_whole_source_closure_and_prior_complete_read_count':3,'cumulative_complete_read_count':33,'next_unread':1283,'prepared_count':50,'rows':rows,'new_proofs':0,'signatures':0,'native_approved':0,'root_approved':0,'operating':0,'boundary':'Three manually judged unsigned assessments, distinct from prior30verifiedproofs. Contextual slots do not turn selected association/season/mood into no-op.1299 actualinput remains pending.'}
p=O/'ASSESSMENT-01280-01283-v1.json';assert not p.exists();p.write_text(json.dumps(b,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(dig(b),hashlib.sha256(p.read_bytes()).hexdigest())
