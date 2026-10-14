"""Bounded actual full/compact/old-binding consumption; synthetic core only."""
from fixture_v1 import *
J=json.loads((O/'BATCH.json').read_text());row=J['records'][0];cid=row['candidate_id'];proof=row['proof'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=proof;S['candidates'][cid]=rec;n.validate(rec,S['slot_catalog'],corpus=S);compact=n.compact(rec,S)
TEXT='Independent synthetic request: existing scene S is explicitly declared at scene role with entity.presence=present. Weather is not pre-frozen. Atmosphere weather selection is open; no umbrella, safety fact, wet surface, humidity or temperature is declared. This is an isolated test core, not real user/runtime evidence.'
core=make_core(TEXT,['S'],[('scene','S')],[('subject','S','entity.presence','entity.presence/v1','present')],[],['atmosphere'])
wrong_owner=make_core(TEXT,['S','T'],[('scene','S')],[('subject','T','entity.presence','entity.presence/v1','present')],[],['atmosphere'])
norole=make_core(TEXT,['S'],[],[('subject','S','entity.presence','entity.presence/v1','present')],[],['atmosphere'])
cases=[('existing_scene_no_weather_or_umbrella_P',core,True),('missing_scene_presence',remove(core,'fact','entity.presence'),False),('wrong_presence_value',change(core,'entity.presence','absent'),False),('other_owner_presence_cannot_transfer',wrong_owner,False),('scene_core_role_missing',norole,False)]
ad=[]
for label,k,want in cases:
 for view in ['full','compact']:
  e=entry(J,1257,binding=True);e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);got=n.admission(e,k);assert got['allowed']==want,(label,view,got);ad.append({'case':label,'view':view,'expected':want,'result':got,'core':k})
e=entry(J,1257,binding=True);bid=e['binding_id'];assert S['slot_bindings'][bid]=={'candidate_id':cid,'conditions':{'subject_applicability':{}},'id':bid,'role':'optional','semantic_role':'direct','slot_id':'weather','weight':.82}
consumer=[]
for label,k,want in cases:
 got=generator.core_entry_eligible(S,k,contract('human'),picked('human'),'weather',e);assert got==want,(label,got);consumer.append({'case':'actual_old_binding_'+label,'allowed':got,'expected':want})
ds,ps,g=n.permission_scope(e,core);assert n.property_scope_allowed(core,ds,ps,record=e)
locked=copy.deepcopy(core);locked['intent_lock']['semantic_anchors'].append({'dimension':'atmosphere','target':'S','property':'weather.precipitation'});dl,pl,_=n.permission_scope(e,locked);assert not n.property_scope_allowed(locked,dl,pl,record=e);assert not generator.core_entry_eligible(S,locked,contract('human'),picked('human'),'weather',e)
closed=copy.deepcopy(core);closed['intent_lock']['open_dimensions']=[];closed['intent_lock']['locked_dimensions'].append('atmosphere');assert not generator.core_entry_eligible(S,closed,contract('human'),picked('human'),'weather',e)
foreign=copy.deepcopy(core);foreign['intent_lock']['semantic_anchors'].append({'dimension':'atmosphere','target':'T','property':'weather.precipitation'});assert generator.core_entry_eligible(S,foreign,contract('human'),picked('human'),'weather',e)
# Weather binding is actually unrestricted; do not invent product/human gate as a negative.
assert generator.core_entry_eligible(S,core,contract('object',['product']),picked('object'),'weather',e)
assert {f['target']for f in proof['facts']}=={'scene'};assert len(compact['facts'])==3 and 'source_units'not in compact
negative=[]
def reject(label,change):
 r=copy.deepcopy(rec);p=r['content']['role_evidence'];change(p);p['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(p)
 try:n.validate(r,S['slot_catalog'],corpus=S)
 except ValueError as exc:negative.append({'case':label,'rejected':True,'reason':str(exc)})
 else:raise AssertionError(label)
reject('partial_app_quote_instead_of_whole',lambda p:p['source_units'][-1].update(quote='Apply the stated light-drizzle weather'))
reject('reference_to_same_field_scene_fact',lambda p:p['source_units'][-1].update(fact_refs=['sceneP']))
reject('canonical_EN_without_direct_anchor',lambda p:p['source_units'][0].update(fact_refs=[]))
reject('invented_reference_relation',lambda p:p['source_units'][-1].update(reference_relation='complete_restatement'))
reject('duplicated_reference',lambda p:p['source_units'].append(copy.deepcopy(p['source_units'][-1])))
reject('reference_foreign_RID_fact',lambda p:p['facts'][1].update(realization_id='other'))
out={'schema':'photo-native-single-source-isolated-verification/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'batch_sha256':c.digest(J),'full_source_validation':True,'compact_projection':compact,'admission_assertions':ad,'admission_count':len(ad),'actual_own_binding':{'id':bid,'record':S['slot_bindings'][bid]},'actual_binding_consumer_assertions':consumer,'whole_effect_locks':{'expanded_dimensions':ds,'expanded_properties':ps,'open_allowed':True,'same_actual_scene_weather_anchor_denied':True,'whole_atmosphere_closed_denied':True,'foreign_owner_anchor_not_transferred':True,'unrestricted_object_product_category_allowed':True},'sourceunit_negative_assertions':negative,'source_reference_tests':len(negative),'all_passed':True,'module_paths_sha256':modules(),'frozen_generation':str(G),'root_acceptance_count':0,'operational_native_qualified_count':0,'real_request_core_freeze_runtime_render_pixels':False,'boundary':'Fresh full sourceproof and compact structure plus actual original binding controlled-synthetic consumer/permission tests. No root/operating/runtime/source update. Semantic interpretation manually reviewed; shape tests do not establish it.','os_network_denied':True,'provider_keys_absent':True,'network_model_Git_changes':0};f=O/'CHECKS-v1.json';assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(out),hashlib.sha256(f.read_bytes()).hexdigest(),len(ad),len(consumer),len(negative))
