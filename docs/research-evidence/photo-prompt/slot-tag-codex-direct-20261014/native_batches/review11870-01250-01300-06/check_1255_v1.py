"""Fresh repaired1255 full/compact actual oldbinding consumption, all E/Rx and grounded aliases/ancestors."""
from pathlib import Path
OLD=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05');base=OLD/'check_01255_01260_v1.py';exec(compile(base.read_text().split('cases=[]',1)[0],str(base),'exec'))
O=R/'native_batches/review11870-01250-01300-06';D=R/'native-inputs/prepared/review11870-01250-01300-06';I=json.loads((D/'INPUT.json').read_text());repair=json.loads((O/'REPAIRED-1255-v1.json').read_text());assert c.digest(repair)=='aacff0b64234dc0f5da148f9fa39b4aa29bc3b97243ed4f6a620fab50247b90e';J={'records':[repair['record']]};S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()))
import photo_search_layout as layout
import photo_role_proposals as proposals
TEXT='Independent synthetic request: existing actual holder H and existing actual held object O are independently present and explicitly distinct. Same holder/object selected. No already-held, near-self-placed or neutral-presentation effect state is frozen. For explicit alias/ancestor controls, AH and AO name exactly H and O; H is a component of actual declared PH, O a component of actual declared PO. These grounded relations are extra controlled requests, not inferred source anatomy or source-generated witnesses. No real request, runtime or pixels are asserted.'
holding=core(['H','O'],[],[presence('H'),presence('O')],[('disjoint','H','O')],['action','composition','role'])
contract={'subject_category':'human','adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[]}};picked={'subject':{'kind':['human'],'tags':['human']}}
def choose(k,view='full',mapping=HB):
 e=entry(1255,'base',True)
 if mapping is not False:e,k=selected(e,k,mapping)
 else:k=copy.deepcopy(k)
 e.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);return e,k
e,k=choose(holding);dims,props,graph=n.permission_scope(e,k);checks=[]
for view in ['full','compact']:
 z,k=choose(holding,view);receipt=n.admission(z,k);assert receipt['allowed'];assert generator.core_entry_eligible(S,k,contract,picked,z['_presentation_role'],z);assert n.property_scope_allowed(k,z['affected_dimensions'],z['affected_properties'],record=z);checks.append({'case':'independent_normal_actual_selected_P_guard_consumer','view':view,'admission':receipt,'same_oldbinding_consumer_allowed':True})
 for role in ['action','prop_placement','prop_state','relational_action']:
  assert generator.core_entry_eligible(S,k,contract,picked,role,z);checks.append({'case':'each_actual_samefact_role_same_oldbinding','view':view,'role':role,'allowed':True})
 for prop in props:
  bad=copy.deepcopy(holding);bad['intent_lock']['semantic_anchors']=[copy.deepcopy(prop)];zz,kk=choose(bad,view);assert not n.property_scope_allowed(kk,zz['affected_dimensions'],zz['affected_properties'],record=zz);assert not generator.core_entry_eligible(S,kk,contract,picked,zz['_presentation_role'],zz);checks.append({'case':'each_actualE_target_Rx_property_lock','view':view,'anchor':prop,'consumer_denied':True})
 for dim in dims:
  bad=copy.deepcopy(holding);bad['intent_lock']['open_dimensions'].remove(dim);bad['intent_lock']['locked_dimensions'].append(dim);zz,kk=choose(bad,view);assert not generator.core_entry_eligible(S,kk,contract,picked,zz['_presentation_role'],zz);checks.append({'case':'each_whole_E_dimension_lock','view':view,'dimension':dim,'consumer_denied':True})
 for a in holding['semantic_assertions']:
  if a['axes']['kind']not in ['fact','disjoint']:continue
  bad=copy.deepcopy(holding);bad['semantic_assertions']=[x for x in bad['semantic_assertions']if x['assertion_id']!=a['assertion_id']];zz,kk=choose(bad,view);receipt=n.admission(zz,kk);assert not receipt['allowed'];assert not generator.core_entry_eligible(S,kk,contract,picked,zz['_presentation_role'],zz);checks.append({'case':'exact_P_selectedpresence_or_source_disjoint_missing','view':view,'removed':a,'admission':receipt})
 zz,kk=choose(holding,view,False);receipt=n.admission(zz,kk);assert not receipt['allowed'];checks.append({'case':'actual_owner_choice_missing','view':view,'admission':receipt})
 for domain in ['product','jewelry','food','wildlife']:
  dc={'subject_category':'human','domains':[domain],'adult_allowed':False,'intent_constraints':{'subject_categories':['human'],'domains':[domain]}};assert not generator.core_entry_eligible(S,k,dc,picked,z['_presentation_role'],z);checks.append({'case':'exact_ownbinding_deny_domain','view':view,'domain':domain,'denied':True})
 dc={'subject_category':'object','adult_allowed':False,'intent_constraints':{'subject_categories':['object'],'domains':[]}};assert not generator.core_entry_eligible(S,k,dc,{'subject':{'kind':['object'],'tags':['object']}},z['_presentation_role'],z);checks.append({'case':'oldbinding_human_category_not_waived','view':view,'denied':True})
 extended=core(['H','O','AH','AO','PH','PO'],[],[presence('H'),presence('O'),presence('PH'),presence('PO')],[('disjoint','H','O'),('equivalent','AH','H'),('equivalent','AO','O'),('part_of','H','PH'),('part_of','O','PO')],['action','composition','role'])
 zz,kk=choose(extended,view);receipt=n.admission(zz,kk);assert receipt['allowed'];assert generator.core_entry_eligible(S,kk,contract,picked,zz['_presentation_role'],zz);checks.append({'case':'actual_declared_aliases_and_part_ancestors_positive','view':view,'core':extended,'admission':receipt})
 for prop in props:
  for kind,prefix in [('alias','A'),('ancestor','P')]:
   anchor={**prop,'target':prefix+prop['target']};bad=copy.deepcopy(extended);bad['intent_lock']['semantic_anchors']=[anchor];zz,kk=choose(bad,view);gg=n.frozen_witnesses(kk)['graph'];assert n.witnesses.owner_relation(gg,prop['target'],anchor['target'])=='overlap';assert not n.property_scope_allowed(kk,zz['affected_dimensions'],zz['affected_properties'],record=zz);assert not generator.core_entry_eligible(S,kk,contract,picked,zz['_presentation_role'],zz);checks.append({'case':'every_E_Rx_actual_grounded_'+kind+'_lock','view':view,'anchor':anchor,'actual_owner_relation':'overlap','consumer_denied':True})
cid=e['id'];rec=S['candidates'][cid];guard=layout.guard_record(rec,S);qualifications={}
for tag in ['action','prop_placement','prop_state','relational_action']:
 full=n.qualification(I['catalog_review']['after'][tag],rec,'base',source_data=S);compact=n.qualification(I['catalog_review']['after'][tag],guard,'base',source_data=S);assert full==compact and full['status']=='eligible';qualifications[tag]=full
assert qualifications['relational_action']['matched_manual_role_views'];noauthority=[n.qualification(I['catalog_review']['after']['relational_action'],x,'base')['status']for x in [rec,guard]];assert noauthority==['review_required','review_required'];proposal=proposals.propose(S,'relational_action',cid,[],realization_ids=['base']);assert proposal['semantic_fit']['status']=='review_required'
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out={'schema':'photo-native-targeted-actual-quote-repair-check/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','input_sha256':c.digest(I),'repair_sha256':c.digest(repair),'source_after_sha256':c.digest(repair['record']['source_after']),'frozen_generation':str(G),'module_paths_sha256':mods,'independent_core':holding,'expanded_dimensions':dims,'expanded_properties':props,'checks':checks,'case_count':len(checks),'fullcompact_source_qualification':qualifications,'missing_fullsource_authority':noauthority,'discovery_proposal':proposal,'all_passed':True,'source_changed':False,'other49_revalidated_as_new':False,'root_acceptance':0,'operating':0,'boundary':'Only1255 fresh repaired source proof and actual controlled fullcompact oldbinding/eachrole/P/guard/every E+Rx property/alias/ancestor/wholelock tested. Concrete synthetic independent core, not actual request/freeze/runtime/render/pixels. Unchanged49 prior evidence reused without new read/signature claim. No source/code/Git/model/network mutation.'}
p=O/'CHECKS-1255-v1.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(c.digest(out),hashlib.sha256(p.read_bytes()).hexdigest(),len(checks),len(props))
