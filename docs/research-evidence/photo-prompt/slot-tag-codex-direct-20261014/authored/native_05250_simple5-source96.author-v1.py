"""Five new individually authored source96 native proofs; no operating adoption."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review05250-simple5-149-01';O=R/'native_batches/review05250-simple5-149-01';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')];import photo_semantic_evidence as n
sys.path.insert(0,str(R));import native_reviews as nr
assert nr.native is n
def H(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def raw(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.load(gzip.open(p) if str(p).endswith('.gz') else open(p))
def artifact(ref):
 assert raw(ref['file'])==ref['file_sha256'];x=read(ref['file']);assert H(x)==ref['sha256'];return x
def save(name,x):
 p=O/name;assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');return {'file':str(p),'file_sha256':raw(p),'sha256':H(x)}
assert raw(n.__file__)=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
A=read(D/'ASSIGNMENT.json');I=artifact(A['input']);P=read(D/'PREPARED-PACKET.json');S=artifact(I['current_snapshot']);original=artifact(I['original_snapshot'])
assert H(S)=='b1c48c867ce0a94d5648b0bfb7935605e4d7708951b36268930ea26523746092'
assert A['task_name']=='/root/review_05250_06250' and A['model']=='gpt-6.1-sol' and A['reasoning_effort']=='high'
assert P['assignment_sha256']==H(A) and P['input_sha256']==H(I)
proposals=read(R/'authored/native_05250_simple5-source-applications-source84-149-v1.json');by={r['ordinal']:r for r in proposals['records']}
catalog=S['slot_catalog'];assert H(catalog)=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
LOCATION={
6131:('Select its location as a card-tournament ruling-table setting unrelated to any proprietary game.','card_tournament_ruling_table_unrelated_to_any_proprietary_game'),
6162:('Select its location as a giant-machine maintenance hangar unrelated to any proprietary design.','giant_machine_maintenance_hangar_unrelated_to_any_proprietary_design'),
6191:('Select its location as the administrative hall at a secret-realm entrance in a fictional xianxia sect.','administrative_hall_at_secret_realm_entrance_in_fictional_xianxia_sect'),
6214:('a cafe service-counter location','cafe_service_counter')}
BASIS={
6131:'Select the full card-tournament ruling-table location, including the unrelated-to-any-proprietary-game limit, as setting E on the same independently established scene. No players, ruling result, brand or separate table entity is introduced.',
6162:'Select the full giant-machine maintenance-hangar location, including its unrelated-to-proprietary-design limit, as setting E. Hangar purpose does not establish a visible giant machine, worker, repair action or launch.',
6191:'Select the administrative hall at a secret-realm entrance in a fictional xianxia sect as one complete setting E. Entrance adjacency and sect fiction are retained in that value, without a visible portal, registration action or world-rule system.',
6214:'The root-selected bounded quiet-as-scene-atmosphere interpretation is explicit. Location, this cafe-closing event phase just before closing, and visually subdued quiet atmosphere are three actual E. No measured silence, private emotion, absent customers, dim light, closing action, night or clock time is supplied. Corrected KO and alias are explicit current source, not presumed old text.',
6220:'Preserve original style/image_plane/image.detail E and same whole_image relation. Continuous rendered contours and readable small surface details are two separate literal PR requirements on that same independent image; no physical topology change or arbitrary object receiver. A merely present image or an arbitrary same-value sentinel does not satisfy those exact PR values.'}
rows=[];readrows=[]
for cid,ordinal in zip(A['ids'],A['ordinals']):
 b=original['candidates'][cid];a=S['candidates'][cid];p=by[ordinal]
 assert b==P['original_records'][cid]==p['whole_original'] and a==P['current_records'][cid]==p['whole_proposed_after']
 loc=I['original_decisions'][cid];old=read(loc['file'])['decisions'][loc['item']-1]
 assert raw(loc['file'])==loc['file_sha256'] and H(old)==loc['row_sha256'] and old==P['historical_compiled_rows'][cid]==p['provenance']['historical_5B']
 assert artifact(I['original_packets'][cid])['records'][cid]==b
 own={k:v for k,v in S['slot_bindings'].items() if v['candidate_id']==cid};assert own==p['own_bindings_unchanged']
 assert n.referenced_records(a,S)==P['references'][cid]==P['reference_bindings'][cid]=={}
 target='image_plane' if ordinal==6220 else 'scene';role='image' if ordinal==6220 else 'scene';kind='image' if ordinal==6220 else 'scene'
 carrier='independently declared existing whole-image context' if ordinal==6220 else 'independently declared existing scene context'
 facts=[]
 def add(fid,pointer,quote,dim,prop,mode,vt,value,requires,**extra):
  text=n.positive_string(a,pointer,realization_id='base');assert quote in text
  f={'id':fid,'realization_id':'base','pointer':pointer,'quote':quote,'dimension':dim,'target':target,'property':prop,'mode':mode,'value':{'type':vt,'value':value},'requires':requires,**extra};facts.append(f)
 add('carrier_present','/content/application_contract',carrier,'subject','entity.presence','prerequisite','entity.presence/v1','present',[])
 add('carrier_kind','/content/application_contract',carrier,'subject','entity.type','prerequisite','entity.type/v1',kind,[])
 need=['carrier_present','carrier_kind']
 if ordinal!=6220:
  quote,value=LOCATION[ordinal];add('locationE','/content/application_contract',quote,'setting','setting.location','effect','setting.location/v1',value,need,operation='set_value',receivers=[])
  E=['locationE']
  if ordinal==6214:
   add('phaseE','/content/application_contract','the cafe-closing event phase just before closing','timing','timing.event_phase','effect','timing.event_phase/v1','cafe_closing_just_before',need,operation='set_value',receivers=[])
   add('quietE','/content/application_contract','quiet means the proposed visually subdued atmosphere of this scene','atmosphere','mood.quiet','effect','mood.quiet/v1','visually_subdued_scene_atmosphere',need,operation='set_value',receivers=[]);E+=['phaseE','quietE']
 else:
  add('contoursPR','/content/concept_units/0','object contours remain continuous','style','image.contour.continuity','preservation','image.contour.continuity/v1','continuous',need)
  add('detailsPR','/content/concept_units/1','small surface details remain readable','style','image.small_surface_detail.readability','preservation','image.small_surface_detail.readability/v1','readable',need)
  add('edgeE','/content/en','clean continuous photographic edges','style','image.detail','effect','image.detail/v1','clean_continuous_photographic_edges',need+['contoursPR','detailsPR'],operation='set_value',receivers=[])
  add('whole_scopeC','/content/application_contract','on the same actual image addressed by the original applies_to whole_image relation','style','image.effect_scope','context','image.effect_scope/v1','whole_image',need);E=['edgeE']
 units=[{'realization_id':'base','pointer':'/content/application_contract','quote':a['content']['application_contract'],'fact_refs':[f['id'] for f in facts if f['pointer']=='/content/application_contract'],'disposition':'semantic'}]
 if ordinal==6220:units.append({'realization_id':'base','pointer':'/content/application_contract','quote':a['content']['application_contract'],'fact_refs':['edgeE','contoursPR','detailsPR'],'disposition':'semantic_reference','reference_relation':'selected_output_constraint','retained_constraint_rationale':'The complete application repeats the selected original edge-rendering E and requires both contour-continuity and detail-readability PR on the same image. Their ordinary facts are directly anchored to the exact EN and separate concept_units. This reference adds no new fact or permission, and retains every original image.detail/whole-image/actual-scope lock and negative bound.'})
 for key in ['en','ko','embedding_text']:
  pointer='/content/'+key
  if ordinal==6220 and key=='en':units.append({'realization_id':'base','pointer':pointer,'quote':a['content'][key],'fact_refs':['edgeE'],'disposition':'semantic'})
  else:units.append({'realization_id':'base','pointer':pointer,'quote':a['content'][key],'fact_refs':E+(['contoursPR','detailsPR'] if ordinal==6220 and key=='embedding_text' else []),'disposition':'semantic_reference','reference_relation':'partial_restatement','retained_constraint_rationale':'The exact local field retains its own complete location/phase/quiet or edge-rendering clauses only. Independent carrier presence/type and same-owner/whole-scope requirements are anchored to the ordinary full application contract. No qualifier absent from this local field is promoted into a new fact. All local negative limits and the disclosed quiet interpretation remain binding.'})
 if ordinal==6220:
  units += [{'realization_id':'base','pointer':'/content/concept_units/0','quote':a['content']['concept_units'][0],'fact_refs':['contoursPR'],'disposition':'semantic'},
            {'realization_id':'base','pointer':'/content/concept_units/1','quote':a['content']['concept_units'][1],'fact_refs':['detailsPR'],'disposition':'semantic'},
            {'realization_id':'base','pointer':'/content/relations/0/subject','quote':a['content']['relations'][0]['subject'],'fact_refs':['edgeE'],'disposition':'semantic_reference','reference_relation':'partial_restatement','retained_constraint_rationale':'The exact relation subject restates the same clean-edge rendering E; its target is bound by the complete relation and ordinary App same-image clause.'},
            {'realization_id':'base','pointer':'/content/relations/0/object','quote':'whole_image','fact_refs':['whole_scopeC'],'disposition':'semantic_reference','reference_relation':'same_selected_owner','retained_constraint_rationale':'This is the whole-image endpoint of the original applies_to relation, explicitly bound to that same independent image in the ordinary App. It creates no other image or physical object and does not move the original image_plane effect.'},
            {'realization_id':'base','pointer':'/content/relations/0/type','quote':'applies_to','fact_refs':[],'disposition':'nonsemantic'}]
 roles={'image_detail':['edgeE']} if ordinal==6220 else {'location':['locationE']}
 if ordinal==6214:roles.update(narrative_phase=['phaseE'],mood=['quietE'])
 proof={'schema':n.SCHEMA,'meaning_sha256':n.meaning_sha256(a),'catalog_sha256':H(catalog),'complete':True,'facts':facts,'source_units':units,
  'roles':{k:{'spec_sha256':H(catalog[k]),'scope':'whole_record','realization_ids':['base'],'fact_refs':v,'support_modes':['effect']} for k,v in roles.items()},
  'owner_maps':{'base':{'schema':n.OWNER_SCHEMA,'bindings':[{'target':target,'core_role':role,'origin':'existing','introduced_by':None}]}},
  'effect_sets':{'base':n.effect_set(a,'base')},'dependencies':{'base':[]},'reference_sha256':{},'guard_sets':{'base':n.source_guard_set(a,'base',S)},'profile_contracts':{'base':None},
  'review':{'basis':BASIS[ordinal]+' The explicit selected existing scene/image address is independently grounded. Both carrier presence and type are exact P, not invented from a role or candidate and not a pre-frozen desired location/rendering. Every E has target-only Rx[] because this selected contract changes the same scene or whole image rather than separately owned physical objects. All original dimensions, properties, intrinsic primary-tag gates and old binding conditions remain. Full original/current/exact5B/ownbindings/emptyclosure and exact origin entries were reread for the source proposal and exact source96 afters reread now; fixed149 used and necessary neighbor fullspecs remain exact. Negative limits remain in whole App semantic/reference units. In6220 the applies_to token is connector-only; the complete same-image relation is positively retained by whole_scopeC and App, never discarded. All required PRs remain PR; no sentinel trait is used as a positive role fact.',
   'whole_source_reviewed':True,'source_correction':{'before_sha256':n.meaning_sha256(b),'after_sha256':n.meaning_sha256(a),'rationale':BASIS[ordinal]+' Use only the exact root-selected source96 after; no new source change is authored inside this proof.'},
   'original_review':{'candidate_id':cid,'source_record_sha256':old['source_record_sha256'],'catalog_sha256':old['catalog_sha256'],'decision_sha256':loc['row_sha256'],'artifact':loc['file']+'#item='+str(loc['item'])},
   'native_review':{'reviewer':A['task_name'],'method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
 proof['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(proof)
 rec=copy.deepcopy(a);rec['content']['role_evidence']=proof;n.validate(rec,catalog,corpus={**S,'candidates':{**S['candidates'],cid:rec}})
 delta=[]
 for field in ['conditions','effects']:
  if b[field]!=a[field]:delta.append({'pointer':'/'+field,'before_exists':True,'before':b[field],'after_exists':True,'after':a[field],'reason':'Exact root-selected source96 effect/condition refinement; original effect dimensions and6220 original property address retained.'})
 for key in sorted(set(b['content'])|set(a['content'])):
  if b['content'].get(key)!=a['content'].get(key):delta.append({'pointer':'/content/'+key,'before_exists':key in b['content'],'before':b['content'].get(key),'after_exists':key in a['content'],'after':a['content'].get(key),'reason':'Exact root-selected source96 App or explicit6214 KO/alias repair; not an implicit source change.'})
 assert nr.apply_delta(b,delta)==a
 req=I['required_revisions'][cid]
 rows.append({'candidate_id':cid,'ordinal':ordinal,'status':'approved','rationale':BASIS[ordinal],'source_before':b,'source_after':a,'delta':delta,'original_compiled':loc,'proof':proof,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':req['prior_review'],'memo_artifacts':req['memo_artifacts'],'rationale':BASIS[ordinal]+' Fresh direct source-native judgment; root acceptance and operating qualification remain separate.'}})
 readrows.append({'ordinal':ordinal,'candidate_id':cid,'source_original_sha256':H(b),'source_current_sha256':H(a),'original_compiled':loc,'whole_ownbindings':own,'closure':{},'full_primary_paths':sorted(n.primary_paths(a,'base')),'proof_native_contract_sha256':proof['review']['native_review']['native_contract_sha256']})
O.mkdir(parents=True,exist_ok=True)
B={'schema':nr.BATCH,'task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment_sha256':H(A),'input_sha256':H(I),'prepared_count':5,'actual_read_count':5,'records':rows};bp=save('BATCH.json',B)
N={'schema':nr.NOTE,'task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment_sha256':H(A),'input_sha256':H(I),'batch_sha256':H(B),'prepared_count':5,'actual_read_count':5,'whole_source_read_ids':A['ids'],'whole_dependency_read_ids':A['ids']};np=save('NOTE.json',N)
ra=save('READ-AUDIT-v1.json',{'schema':'photo-source96-simple5-direct-read-audit/v1','task':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'source_sha256':H(S),'catalog_sha256':H(catalog),'source_proposal':{'file':str(R/'authored/native_05250_simple5-source-applications-source84-149-v1.json'),'raw_sha256':raw(R/'authored/native_05250_simple5-source-applications-source84-149-v1.json')},'whole_original_current_5B_ownbindings_closure_origin_reviewed':5,'source96_exact_after_reread':5,'new_unique_bulk_count':0,'fresh_native_proofs':5,'reused_proofs':0,'rows':readrows,'boundary':'Source-native draft and structural validation only until actual full/compact admission, all original property/whole/alias/ancestor locks, source primary-tag gates and6220 literal PR controls complete. No real requester, pixels or root acceptance. Source proposal fact plan was not automatically converted: carrier type P, exact cafe-qualified phase quote, and same-image context relation are newly directly judged source facts.'})
v=nr.verify_batch(str(D/'ASSIGNMENT.json'),bp['file'],np['file']);v={k:val for k,val in v.items() if k!='records'};v['read_audit']=ra;vp=save('VERIFICATION-v1.json',v)
print(json.dumps({'batch':bp,'note':np,'read_audit':ra,'verification':vp,'statuses':v['statuses'],'shape_valid':v['shape_valid'],'actual_runtime_checks_pending':True},ensure_ascii=False))
