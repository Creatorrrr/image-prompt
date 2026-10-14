"""Every actual expanded property/receiver and whole dimension lock, plus actual oldbinding negatives. No source/proof changes."""
from pathlib import Path
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05')
base=O/'check_01250_01255_v1.py';prefix=base.read_text().split('cases=[',1)[0]
exec(compile(prefix,str(base), 'exec'))
configs=[(1250,face,[]),(1251,imageface,[]),(1252,face,[]),(1253,counter,COUNTER_BINDINGS),(1254,charm,[])]
contract={'subject_category':'human','adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}}
records=[]
def chosen(ordinal,k,mapping,binding=True,view='full'):
 e=entry(ordinal,binding)
 if mapping:e,k=selected(e,k,mapping)
 e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None)
 return e,k
for ordinal,k,mapping in configs:
 e,k=chosen(ordinal,k,mapping);ds,ps,_=n.permission_scope(e,k);slot=e['_presentation_role'];expected=[]
 for prop in ps:
  for view in ['full','compact']:
   locked=copy.deepcopy(k);locked.pop('canonical_sha256',None);locked['intent_lock']['semantic_anchors']=[copy.deepcopy(prop)]
   z,locked=chosen(ordinal,locked,mapping,view=view)
   assert not n.property_scope_allowed(locked,z['affected_dimensions'],z['affected_properties'],record=z),(ordinal,view,prop)
   assert not generator.core_entry_eligible(S,locked,contract,picked,slot,z),(ordinal,'consumerproperty',view,prop)
   expected.append({'case':'each_actual_effect_target_or_receiver_property_lock','view':view,'anchor':prop,'permission_denied':True,'actual_oldbinding_consumer_denied':True})
 for dim in ds:
  for view in ['full','compact']:
   locked=copy.deepcopy(k);locked.pop('canonical_sha256',None);locked['intent_lock']['open_dimensions'].remove(dim);locked['intent_lock']['locked_dimensions'].append(dim)
   z,locked=chosen(ordinal,locked,mapping,view=view)
   assert not n.property_scope_allowed(locked,z['affected_dimensions'],z['affected_properties'],record=z),(ordinal,dim,view)
   assert not generator.core_entry_eligible(S,locked,contract,picked,slot,z),(ordinal,'consumerdimension',view,dim)
   expected.append({'case':'each_whole_effect_dimension_lock','view':view,'dimension':dim,'permission_denied':True,'actual_oldbinding_consumer_denied':True})
 for assertion_row in k['semantic_assertions']:
  axes=assertion_row['axes']
  if axes['kind']not in ['fact','disjoint']:continue
  bad=copy.deepcopy(k);bad.pop('canonical_sha256',None);bad['semantic_assertions']=[x for x in bad['semantic_assertions']if x['assertion_id']!=assertion_row['assertion_id']]
  for view in ['full','compact']:
   z,badf=chosen(ordinal,bad,mapping,view=view)
   assert not generator.core_entry_eligible(S,badf,contract,picked,slot,z),(ordinal,'missing independent witness',view,assertion_row)
   expected.append({'case':'missing_independent_frozen_fact_or_disjoint_guard','view':view,'removed':assertion_row,'actual_oldbinding_consumer_denied':True})
 records.append({'ordinal':ordinal,'expanded_dimensions':ds,'expanded_properties':ps,'tests':expected})
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
body={'schema':'photo-native-every-effect-owner-lock-research-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','checkpoint_sha256':c.digest(J),'input_sha256':c.digest(I),'frozen_generation':str(G),'module_paths_sha256':mods,'records':records,'actual_expanded_property_count':sum(len(r['expanded_properties'])for r in records),'actual_effect_dimension_count':sum(len(r['expanded_dimensions'])for r in records),'test_cases':sum(len(r['tests'])for r in records),'all_passed':True,'no_source_proof_status_changes':True,'root_accepted':0,'operating':0,'boundary':'Controlled independent synthetic cores. Every actual E target+Rx property and whole dimension denied in full/compact through permission and actualoldbindingconsumer; removing every explicit P/disjoint witness rejects. Not real core freeze/runtime/pixels/acceptance.','fixture_literal_reuse':{'file':str(base),'file_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'range':'exactdefinitions before cases list, manually reread fixture meaning, no oldresults/status conversion.'}}
p=O/'CHECKS-01250-01255-ALL-E-RX-v1.json';assert not p.exists();p.write_text(json.dumps(body,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(body),hashlib.sha256(p.read_bytes()).hexdigest(),body['actual_expanded_property_count'],body['test_cases'])
