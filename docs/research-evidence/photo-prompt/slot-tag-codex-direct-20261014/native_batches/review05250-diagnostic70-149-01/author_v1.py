"""Serialize the worker's 70 individually authored, directly read judgments.
No semantic classifier, model call or operating source mutation.
"""
import copy,gzip,hashlib,json,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review05250-diagnostic70-149-01';O=R/'native_batches/review05250-diagnostic70-149-01';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')];import photo_semantic_evidence as n
assert hashlib.sha256(Path(n.__file__).read_bytes()).hexdigest()=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
sys.path.insert(0,str(R));import native_reviews as nr
assert nr.native is n

def h(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def raw(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.load(gzip.open(p) if str(p).endswith('.gz') else open(p))
def save(name,data):
 p=O/name;assert not p.exists(),str(p)+' already frozen';p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');return {'file':str(p),'file_sha256':raw(p),'sha256':h(data)}
def artifact(ref):
 assert raw(ref['file'])==ref['file_sha256'];v=read(ref['file']);assert h(v)==ref['sha256'];return v
A=read(D/'ASSIGNMENT.json');I=artifact(A['input']);P=read(D/'PREPARED-PACKET.json');before=artifact(I['original_snapshot']);current=artifact(I['current_snapshot']);order=artifact(I['order']);assert h(current)== '08c699d25b3b6117c26f1ab6f05175b7db013ad17c69e44a9d2fd7acbcb5ea9c'
assert A['task_name']=='/root/review_05250_06250' and A['model']=='gpt-6.1-sol' and A['reasoning_effort']=='high' and P['prepared_count']==70
assert P['assignment_sha256']==h(A) and P['input_sha256']==h(I) and A['ids']==I['ids']==P['ids']
oldp=R/'authored/native_diag70_05250_read-packet-v1.json';old=read(oldp);oldby={r['candidate_id']:r for r in old['records']}
notes=[R/'authored/native_diag70_05250_000_015.review-v1.json',R/'authored/native_diag70_05250_015_047.review-v1.json',R/'authored/native_diag70_05250_047_070.review-v1.json'];manual={r['ordinal']:r for p in notes for r in read(p)['rows']}
# Explicitly selected manual HOLD identities; other65 retain the already authored individual reasons.
HOLDS={12027,12038,12049,12051,12093}
assert len(manual)==70 and {o for o,m in manual.items() if m['retain_diagnostic_recommendation'] is None}==HOLDS
selected=read(R/'native-inputs/root-diagnostic-kind-source-plan-18/ROOT-SOURCE-SELECTION.json');selection={r['ordinal']:r for r in selected['selected']}
origin=read(old['origin']['file']);catalog=artifact(I['catalog_review']['provenance'][0]) if False else current['slot_catalog']
assert h(catalog)==old['catalog149_sha256'];assert h(catalog)==h(read(R/'CATALOG-FINAL-149-V6.json'))
audit_rows=[];rows=[];unit_count=0
for cid,ordinal in zip(A['ids'],A['ordinals']):
 assert order[ordinal]==cid and cid==manual[ordinal]['candidate_id']
 prior=oldby[cid];b=before['candidates'][cid];a=current['candidates'][cid]
 assert b==prior['original']==P['original_records'][cid] and a==P['current_records'][cid]
 # Exact canonical equality licenses reuse of prior actual whole-source reading.
 expected_after=copy.deepcopy(prior['current66'])
 if ordinal in HOLDS:expected_after['record_kind']='visual_option';assert a==selection[ordinal]['after'] and b==selection[ordinal]['before']
 assert a==expected_after
 loc=I['original_decisions'][cid];assert {k:loc[k] for k in ['file','item','row_sha256']}=={k:prior['original5B'][k] for k in ['file','item','row_sha256']}
 compiled=read(loc['file']);assert raw(loc['file'])==loc['file_sha256'];oldrow=compiled['decisions'][loc['item']-1];assert h(oldrow)==loc['row_sha256'] and oldrow==prior['original5B']['row']==P['historical_compiled_rows'][cid]
 packet=artifact(I['original_packets'][cid]);assert packet['records'][cid]==b and h(packet)==oldrow['packet_sha256']
 own_before={k:v for k,v in before['slot_bindings'].items() if v['candidate_id']==cid};own_after={k:v for k,v in current['slot_bindings'].items() if v['candidate_id']==cid}
 assert own_before==own_after==prior['own_original_bindings']==prior['own_current_bindings']=={}
 refs=n.referenced_records(a,current);assert refs=={} and P['references'][cid]==P['reference_bindings'][cid]=={}
 # Previously read exact origin and parent entries remain exactly byte-equivalent.
 entry=origin
 for part in prior['origin']['pointer'].strip('/').split('/'):entry=entry[int(part)] if isinstance(entry,list) else entry[part]
 assert entry==prior['origin']['record'] and h(entry)==b['provenance'][0]['sha256']==prior['origin']['canonical_sha256']
 rev=I['required_revisions'][cid];previous=artifact(rev['prior_review']['artifact'])
 for part in rev['prior_review']['pointer'].strip('/').split('/'):previous=previous[int(part)] if isinstance(previous,list) else previous[part]
 assert h(previous)==rev['prior_review']['sha256'] and previous==oldrow
 for ref in rev['memo_artifacts']:artifact(ref)
 reason=manual[ordinal]['reason']
 if ordinal in HOLDS:
  reason='Root research source kind restoration directly reread: only diagnostic -> visual_option changed; all original definition, conditions, effects, provenance and other fields are exactly retained. '+selection[ordinal]['reason']+' '+manual[ordinal]['reason']+' Complete positive owner/fact/unit/mode/operation/value/all-Rx and obligation contract remains pending; no native proof, arbitrary branch, feature, channel, participant or E0 shortcut is authored.'
 proof=None
 if ordinal not in HOLDS:
  assert manual[ordinal]['retain_diagnostic_recommendation'] is True and b==a and a['record_kind']=='diagnostic'
  rids=n.realizations.ids(a);assert rids==['base']
  units=[{'realization_id':'base','pointer':p,'quote':n.positive_string(a,p,realization_id='base'),'fact_refs':[],'disposition':'nonsemantic'} for p in sorted(n.primary_paths(a,'base'))];unit_count+=len(units)
  proof={'schema':n.SCHEMA,'meaning_sha256':n.meaning_sha256(a),'catalog_sha256':h(catalog),'complete':True,'facts':[],'roles':{},'owner_maps':{'base':{'schema':n.OWNER_SCHEMA,'bindings':[]}},'source_units':units,'effect_sets':{'base':n.effect_set(a,'base')},'dependencies':{'base':[]},'reference_sha256':refs,'guard_sets':{'base':n.source_guard_set(a,'base',current)},'profile_contracts':{'base':n.realizations.profile_contract(a,'base')},'review':{'basis':'Fresh native semantic review against exact whole source/original5B/empty ownbindings and closure, exact original node or confounder and its full parent purpose, and relevant full149 specs. '+reason+' Every full primary text string is retained as a nonsemantic routing/check/contrast definition in this actual source context; no current visual fact is asserted. This decision is not based on kind/header, empty effects, metadata role or unfilled actual request alone. Exact equality with the directly read immutable earlier70 packet is explicitly audited; root kind-restored5 remain separate pending.','whole_source_reviewed':True,'source_correction':None,'original_review':{'candidate_id':cid,'source_record_sha256':oldrow['source_record_sha256'],'catalog_sha256':oldrow['catalog_sha256'],'decision_sha256':loc['row_sha256'],'artifact':loc['file']+'#item='+str(loc['item'])},'native_review':{'reviewer':A['task_name'],'method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
  proof['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(proof)
  record=copy.deepcopy(a);record['content']['role_evidence']=proof;n.validate(record,catalog,corpus={**current,'candidates':{**current['candidates'],cid:record}})
 delta=[] if ordinal not in HOLDS else [{'pointer':'/record_kind','before_exists':True,'before':'diagnostic','after_exists':True,'after':'visual_option','reason':'Root explicitly restores positive source kind only, preserving whole positive requirements and leaving complete native contract pending.'}]
 row={'candidate_id':cid,'ordinal':ordinal,'status':'pending' if ordinal in HOLDS else 'diagnostic_reviewed','rationale':reason,'source_before':b,'source_after':a,'delta':delta,'original_compiled':loc,'proof':proof,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':rev['prior_review'],'memo_artifacts':rev['memo_artifacts'],'rationale':'Fresh native judgment under the exact new root input, preserving the precise original5B and prior individual read history. '+reason}}
 rows.append(row);audit_rows.append({'candidate_id':cid,'ordinal':ordinal,'prior_actual_read_source_sha256':h(prior['current66']),'new_source_sha256':h(a),'whole_original_reuse_exact':True,'current_reuse_except_explicit_kind_only':True,'exact_compiled_row_reuse':True,'exact_origin_reuse':True,'all_ownbindings_and_requiredclosure_empty':True,'fresh_changed_record_whole_reread':ordinal in HOLDS,'new_status':row['status'],'primary_nonsemantic_unit_count':len(proof['source_units']) if proof else None})
assert len(rows)==70 and sum(r['status']=='diagnostic_reviewed' for r in rows)==65 and sum(r['proof'] is None for r in rows)==5
read_audit={'schema':'photo-native-diagnostic70-exact-read-reuse-audit/v1','task':A['task_name'],'model':A['model'],'effort':A['reasoning_effort'],'assignment_sha256':h(A),'input_sha256':h(I),'source_current_sha256':h(current),'actual_full_source_scope_count':70,'new_distinct_source_bodies_read':5,'earlier_actual_direct_read_count':70,'bulk8000_addition':0,'earlier_packet':{'file':str(oldp),'raw_sha256':raw(oldp)},'earlier_individual_reviews':[{'file':str(p),'raw_sha256':raw(p)} for p in notes],'kind_changed_ordinals':sorted(HOLDS),'ordinary_nonsemantic_primary_units':unit_count,'rows':audit_rows,'boundaries':['65 exact-equal source/original5B/origin bodies reuse actual prior complete reading; not falsely counted as new text reads.','Five changed full current records and before/after source selection were directly reread; kind only changed, full positive obligations remain pending.','All30 previously directly read relevant full149 specs remain exactly current; no claim that all149 specs were newly read.','Exact archive/family/policies/compatibility/guards/three full parentprofiles and20 separate scene examples were previously directly read. Hash/locator identity is not semantic approval.','Related parent purpose is semantic provenance context; it does not introduce source guards, optional-member roles or E.'],'module_files':{'native':{'file':n.__file__,'sha256':raw(n.__file__)},'native_reviews':{'file':nr.__file__,'sha256':raw(nr.__file__)}}}
ra=save('READ-AUDIT-v1.json',read_audit)
batch={'schema':nr.BATCH,'task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment_sha256':h(A),'input_sha256':h(I),'prepared_count':70,'actual_read_count':70,'records':rows};bp=save('BATCH.json',batch)
note={'schema':nr.NOTE,'task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment_sha256':h(A),'input_sha256':h(I),'batch_sha256':h(batch),'prepared_count':70,'actual_read_count':70,'whole_source_read_ids':A['ids'],'whole_dependency_read_ids':A['ids']};np=save('NOTE.json',note)
verified=nr.verify_batch(str(D/'ASSIGNMENT.json'),bp['file'],np['file']);v={k:value for k,value in verified.items() if k!='records'};v['read_audit']=ra;v['boundary']='Sparse70 original verifier and65 source-proof validations only. No positive native approval, core/admission/fullcompact/consumer/render/operating/root acceptance.';vf=save('VERIFICATION-v1.json',v)
print(json.dumps({'artifacts':[bp,np,ra,vf],'statuses':v['statuses'],'actual_read_count':v['actual_read_count'],'ordinary_units':unit_count,'shape_valid':v['shape_valid'],'root_accepted':v['root_accepted'],'operational_native_qualified_count':v['operational_native_qualified_count']},ensure_ascii=False))
