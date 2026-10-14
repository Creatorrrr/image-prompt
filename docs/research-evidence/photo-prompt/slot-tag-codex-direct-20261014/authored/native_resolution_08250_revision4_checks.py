"""Independent literal request fixtures and existing permission primitives only.

No fabricated complete proof, production admission, model or code mutation.
"""
import copy,json,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(Path.cwd()/'skills/photo-prompt-image-generator/scripts'))
import photo_semantic_evidence as s
import photo_candidate_corpus as c
from photo_contracts import property_effects_allowed
F=json.loads((R/'authored/native_resolution_08250_revision4_facts.json').read_text())
V3=json.loads((R/'authored/native_resolution_08250_revision3_facts.json').read_text())
assert len(F['facts'])==len(V3['facts'])==3555
fact_deltas=[]
for ix,(old,new) in enumerate(zip(V3['facts'],F['facts'])):
 if old!=new:
  assert old['property']=='event.small_setback' and new['property']=='situation.small_setback'
  a=copy.deepcopy(old);a['property']=new['property'];assert a==new
  fact_deltas.append({'pointer':'/facts/'+str(ix)+'/property','fact_id':new['id'],'before':old['property'],'after':new['property'],'reason':'Root-approved property spelling only; exact source, mode, owner, typed value, operation, receivers, requires and selected scope unchanged.'})
assert len(fact_deltas)==48
def assertion(id,dim,axes,evidence):return {'assertion_id':id,'dimension':dim,'polarity':'required','source_span_ids':['request'],'axes':{'native_schema':'photo-frozen-semantics/v1',**axes},'evidence':{'literal':evidence},'affected_dimensions':[dim]}
def owner(id,kind,evidence):return assertion(id+'_owner','subject',{'kind':'owner','owner':id,'owner_kind':kind},evidence)
def role(id,kind,evidence):return assertion(id+'_'+kind,'subject',{'kind':'role','role':kind,'owner':id},evidence)
def frozen(id,dim,own,prop,typ,value,evidence):return assertion(id,dim,{'kind':'fact','owner':own,'property':prop,'value_type':typ,'value':value},evidence)
def anchor(id,dim,own,prop,evidence):return {'anchor_id':id,'dimension':dim,'target':own,'property':prop,'source_text':evidence,'prompt_evidence':evidence}
REQUEST='Photograph Iri, an explicitly adult person with unmistakably adult body and face presentation. Iri is already declared a peer and peer rival as a scene role; no counterpart is specified. Iri has an existing face that belongs to Iri. Preserve the declared adult status and the unmistakably adult body and face presentation. Leave visible youthful-adult age presentation, styling, facial expression, eyelid opening and whole-body bearing open. Do not infer biological or numeric age or child or teen morphology.'
HELP_REQUEST='Jan is an already established helper, distinct from Iri. Jan may visibly help Iri, with help activity left open.'
RECOVERY_REQUEST='A prior brief disruption is already declared as story context for Iri. A recovery attempt at the selected instant is open; the past disruption need not be visible now.'
def core_for(help_selected=False,recovery_selected=False):
 text=REQUEST+(' '+HELP_REQUEST if help_selected else '')+(' '+RECOVERY_REQUEST if recovery_selected else '')
 rows=[owner('iri','person','Iri'),role('iri','main_subject','Iri'),owner('iri_face','face','existing face'),role('iri_face','primary_face','existing face'),assertion('face_belongs_to_iri','subject',{'kind':'part_of','left':'iri_face','right':'iri'},'existing face that belongs to Iri'),
 frozen('iri_presence','subject','iri','entity.presence','entity.presence/v1','present','Iri'),frozen('face_presence','subject','iri_face','entity.presence','entity.presence/v1','present','existing face'),
 frozen('declared_adult','age','iri','age.declared','age.declared/v1','adult','explicitly adult person'),
 frozen('adult_body','age','iri','age.presentation.body','age.presentation.body/v1','unmistakably_adult','unmistakably adult body and face presentation'),
 frozen('adult_face','age','iri_face','age.presentation.face','age.presentation.face/v1','unmistakably_adult','unmistakably adult body and face presentation'),
 frozen('declared_peer','role','iri','participant.role.peer','participant.role.peer/v1','declared','already declared a peer and peer rival'),
 frozen('declared_peer_rival','role','iri','participant.role.peer_rival','participant.role.peer_rival/v1','declared','already declared a peer and peer rival')]
 anchors=[anchor('declared_age','age','iri','age.declared','explicitly adult person'),anchor('body_range','age','iri','age.presentation.body','unmistakably adult body and face presentation'),anchor('face_range','age','iri_face','age.presentation.face','unmistakably adult body and face presentation')]
 if help_selected:
  rows += [owner('jan','person','Jan'),role('jan','secondary_subject','Jan'),assertion('helper_distinct','subject',{'kind':'disjoint','left':'jan','right':'iri'},'distinct from Iri'),frozen('helper_presence','subject','jan','entity.presence','entity.presence/v1','present','already established helper')]
 if recovery_selected:
  rows.append(frozen('prior_disruption','timing','iri','narrative.context.prior_disruption','narrative.prior_disruption/v1','declared','prior brief disruption is already declared'))
  anchors.append(anchor('prior_context','timing','iri','narrative.context.prior_disruption','prior brief disruption is already declared'))
 return {'contract_version':'photo-authorial-core/v3','baseline_prompt_en':text,'request_binding':{'active_spans':[{'span_id':'request','text':text}]},'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['subject','role'],'open_dimensions':['age','appearance','expression','pose','action','event','timing'],'semantic_anchors':anchors},'semantic_assertions':rows}
def frozen_obligations_match(rid,core):
 # Reuses the current neutral reader and exact typed matching semantics without
 # claiming its output is a fully sealed/admitted candidate proof.
 try:w=s.frozen_witnesses(core)
 except ValueError:return False
 owners={'actor':'iri','actor_face':'iri_face','helper':'jan'}
 for f in F['facts']:
  if f['realization_id']!=rid or f['mode'] not in {'prerequisite','preservation'}:continue
  matches=[x for x in w['facts'] if x['dimension']==f['dimension'] and x['property']==f['property'] and x['target']==owners[f['target']]]
  if len(matches)!=1:return False
  if f['mode']=='prerequisite' and matches[0]['value']!=f['value']:return False
 return True
def permission(core,dims,props):
 if not set(dims)<=set(core['intent_lock']['open_dimensions']):return False
 try:graph=s.frozen_witnesses(core)['graph']
 except ValueError:return False
 return property_effects_allowed(core['intent_lock'],dims,props,owner_graph=graph)
cases=[]
for row in F['summaries']:
 rid=row['rid'];chosen=row['chosen'];core=core_for('help' in chosen,'recovery' in chosen)
 assert frozen_obligations_match(rid,core),rid
 props=copy.deepcopy(row['effect_sets']['properties']);owners={'actor':'iri','actor_face':'iri_face','helper':'jan'}
 for p in props:p['target']=owners[p['target']]
 dims=row['effect_sets']['dimensions'];assert permission(core,dims,props)
 negatives=[]
 obligations=['iri_presence','face_presence','declared_adult','adult_body','adult_face','declared_peer','declared_peer_rival']+(['helper_presence'] if 'help' in chosen else [])+(['prior_disruption'] if 'recovery' in chosen else [])
 for aid in obligations:
  bad=copy.deepcopy(core);bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['assertion_id']!=aid];assert not frozen_obligations_match(rid,bad),(rid,aid)
  wrong=copy.deepcopy(core);f=next(x for x in wrong['semantic_assertions'] if x['assertion_id']==aid)
  # A separately specified existing unrelated owner is not the affected owner.
  wrong['baseline_prompt_en']+=' Rui is an unrelated comparison person.';wrong['request_binding']['active_spans'][0]['text']=wrong['baseline_prompt_en']
  wrong['semantic_assertions'].append(owner('rui','person','Rui'))
  f['axes']['owner']='rui'
  if f['dimension'] not in wrong['intent_lock']['locked_dimensions']:
   wrong['intent_lock']['semantic_anchors'].append(anchor('wrong_'+aid,f['dimension'],'rui',f['axes']['property'],'Rui'))
  assert not frozen_obligations_match(rid,wrong),(rid,'wrongowner',aid)
  negatives.append({'assertion_id':aid,'absence_rejected':True,'wrong_owner_rejected':True})
 locks=[]
 for ix,p in enumerate(props):
  bad=copy.deepcopy(core);bad['intent_lock']['semantic_anchors'].append(anchor('effect_lock_'+str(ix),p['dimension'],p['target'],p['property'],'Iri' if p['target']!='jan' else 'Jan'))
  assert not permission(bad,dims,props),(rid,p)
  locks.append({'effect':p,'property_lock_rejected':True})
 age_locked=copy.deepcopy(core);age_locked['intent_lock']['open_dimensions'].remove('age');age_locked['intent_lock']['locked_dimensions'].append('age');assert not permission(age_locked,dims,props)
 appearance_locked=copy.deepcopy(core);appearance_locked['intent_lock']['open_dimensions'].remove('appearance');appearance_locked['intent_lock']['locked_dimensions'].append('appearance');assert not permission(appearance_locked,dims,props)
 # No cross-dimension alias is invented: isolate just the age effect.
 age_only=[p for p in props if p['dimension']=='age'];assert permission(appearance_locked,['age'],age_only)
 same=copy.deepcopy(core);same['intent_lock']['semantic_anchors'].append(anchor('same_age_value','age','iri','age.presentation.youthful_adult','Iri'));same['semantic_assertions'].append(frozen('already_youthful_adult','age','iri','age.presentation.youthful_adult','age.presentation.youthful_adult/v1','youth_appearing_adult','Iri'))
 assert not permission(same,dims,props)
 cases.append({'rid':rid,'independently_authored_request_fixture':core,'all_frozen_requirements_match_exactly':True,'missing_wrong_owner_negatives':negatives,'all_actual_property_lock_negatives':locks,'whole_age_lock_rejected':True,'whole_appearance_lock_rejected_by_existing_appearance_effects':True,'age_only_is_not_automatically_appearance_effect':True,'same_value_does_not_bypass_age_property_lock':True,'no_common_second_person':('secondary_subject' not in s.frozen_witnesses(core)['graph']['roles']) if 'help' not in chosen else 'selected helper only'})
noage=core_for();noage['adult_allowed']=True;noage['semantic_assertions']=[x for x in noage['semantic_assertions'] if x['assertion_id']!='declared_adult'];assert not frozen_obligations_match('baseline',noage)
out={'schema':'native-resolution-revision4-isolated-checks/v1','task_name':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high','fact_inventory_count':3555,'source_units':1011,'actual_RIDs':18,'fact_property_exact_deltas':fact_deltas,'checks':cases,'adult_permission_without_declared_age_rejected':True,'boundary':'Independent literal minimal core fixtures; exact frozen-obligation matcher plus current neutral reader/property permission primitives. Not full/compact v4 admission, source guard enforcement, final audit or an approved native proof.','production_native_qualified_count':0,'observed_code_sha256':{str(Path(x.__file__)):hashlib.sha256(Path(x.__file__).read_bytes()).hexdigest() for x in [s,c]},'current_caps':{'rids':s.MAX_REALIZATIONS,'facts':s.MAX_FACTS,'units':s.MAX_UNITS}}
(R/'authored/native_resolution_08250_revision4_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'RIDs':len(cases),'fact_property_deltas':len(fact_deltas),'missing_wrongowner_cases':sum(2*len(x['missing_wrong_owner_negatives']) for x in cases),'effect_lock_negatives':sum(len(x['all_actual_property_lock_negatives']) for x in cases),'age_locked_negatives':18,'same_value_lock_negatives':18,'actual_native_approved':0}))
