"""Mechanical unsigned draft serializer only. Every meaning/fact/role/condition/mode/owner supplied explicitly by literal author."""
import json,hashlib,copy,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');AD=R/'authored';IP=AD/'native_11870_01500_02250.inputs-146v5.json';assert hashlib.sha256(IP.read_bytes()).hexdigest()=='9d8c7497a70fa0d145af47cc2d25aa73e273c11432baf2d06483e6b2cfb8497c';I=json.loads(IP.read_text());CAT=I['catalog_full'];ROWS=[]
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def F(i,d,t,p,mode,typ,value,req,evidence,op=None,receivers=None):return {'id':i,'actual_realization_id':'base','dimension':d,'target':t,'property':p,'mode':mode,'typed_value':{'type':typ,'value':value},'requires':req,'positive_evidence':[{'pointer':'/content/'+field,'positive_quote':q}for field,q in evidence],'operation':op,'receivers':receivers}
def O(t,selector,role,why):return {'target':t,'selector_proposal':selector,'explicit_neutral_core_role':role,'rationale':why}
def B(tag,refs,modes,conditions,weight,semantic,why):return {'slot_id':tag,'fact_refs':refs,'support_modes':modes,'scope':'whole_record','actual_realization_ids':['base'],'role':'optional','semantic_role':semantic,'conditions_proposal':conditions,'weight_proposal':weight,'rationale':why,'status':'unsigned_manual_proposal_only'}
def E(d,t,p):return {'dimension':d,'target':t,'property':p}
def row(n,meaning,changes,effects,owners,facts,units,bindings,binding_review,guard_review,pending,rejected,conditions=None):
 cid=I['ids'][n-1500];v=I['records'][cid];after=copy.deepcopy(v['actual_current_full']);delta=[]
 for key,value in changes.items():delta.append({'pointer':'/content/'+key,'before_exists':key in after['content'],'before':after['content'].get(key),'after_exists':True,'after':value,'reason':'Individual source-preserving application or faithful language clarification proposal. '+meaning});after['content'][key]=value
 if effects is not None and effects!=after['effects']:delta.append({'pointer':'/effects','before_exists':True,'before':after['effects'],'after_exists':True,'after':effects,'reason':'Individually authored complete mutation intent; no empty/coarse effect waiver.'});after['effects']=effects
 if conditions is not None and conditions!=after['conditions']:delta.append({'pointer':'/conditions','before_exists':True,'before':after['conditions'],'after_exists':True,'after':conditions,'reason':'Individually authored intrinsic and exact owner/typed prerequisites, not inferred from tags.'});after['conditions']=conditions
 for f in facts:
  assert f['mode']in ['effect','prerequisite','preservation','context']
  if f['mode']=='effect':assert f['operation'] and isinstance(f['receivers'],list)
  else:assert f['operation']is None and f['receivers']is None
  for ev in f['positive_evidence']:assert ev['positive_quote']in after['content'][ev['pointer'][9:]],(n,f['id'],ev)
 ids={f['id']for f in facts};assert all(set(f['requires'])<=ids for f in facts);assert all(set(b['fact_refs'])<=ids for b in bindings)
 for key,refs in units.items():assert isinstance(after['content'][key],str)and set(refs)<=ids
 ROWS.append({'ordinal':n,'candidate_id':cid,'status':'unsigned_literal_native_draft_pending_root_review','whole_meaning':meaning,'original_full':v['original_full'],'actual_current_full':v['actual_current_full'],'corrected5B_full':v['corrected5B_full'],'compiled5B_full':v['compiled5B_full'],'compiled5B_locator':v['compiled5B_locator'],'original_sha256':v['original_sha256'],'actual_current_sha256':v['actual_current_sha256'],'proposed_source_after':after,'proposed_source_after_sha256':digest(after),'exact_source_correction_proposals':delta,'actual_realization_ids':v['current_actual_rids'],'original_full_closure':v['original_closure'],'actual_current_full_closure':v['actual_current_closure'],'corrected5B_full_closure':v['corrected5B_closure'],'owner_binding_proposals':owners,'literal_native_facts':facts,'whole_positive_source_units':[{'pointer':'/content/'+k,'quote':after['content'][k],'actual_realization_id':'base','fact_refs':refs}for k,refs in units.items()],'binding_proposals':bindings,'own_binding_manual_classification_and_migration':binding_review,'source_intrinsic_guard_manual_review':guard_review,'pending':pending,'rejected_boundaries':rejected,'native_proof':None,'signature':None,'root_selected':False,'automatic_approval_or_mode_owner_role_generation':False})
def emit(a,b):
 assert [r['ordinal']for r in ROWS]==list(range(a,b))
 for r in ROWS:print(json.dumps({'ordinal':r['ordinal'],'whole_after':r['proposed_source_after'],'facts':r['literal_native_facts'],'units':r['whole_positive_source_units'],'owners':r['owner_binding_proposals'],'roles':r['binding_proposals'],'pending':r['pending']},ensure_ascii=False,indent=2))
