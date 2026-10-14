"""Exact58 proof reuse and12 positive-contract pending records. No resigning."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review05250-diagnostic70-149-02';O=R/'native_batches/review05250-diagnostic70-149-02'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
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
A=read(D/'ASSIGNMENT.json');I=artifact(A['input']);P=read(D/'PREPARED-PACKET.json');before=artifact(I['original_snapshot']);current=artifact(I['current_snapshot']);order=artifact(I['order'])
assert H(current)=='b1c48c867ce0a94d5648b0bfb7935605e4d7708951b36268930ea26523746092'
assert A['task_name']=='/root/review_05250_06250' and A['model']=='gpt-6.1-sol' and A['reasoning_effort']=='high'
assert P['assignment_sha256']==H(A) and P['input_sha256']==H(I) and A['ids']==P['ids']==I['ids']
oldpath=R/'native_batches/review05250-diagnostic70-149-01/BATCH.json';old=read(oldpath)
assert raw(oldpath)=='895cd62700f3c0a9ba0b3c1652173d1052b0667f919d9897657da4c54786e97e'
oldby={r['candidate_id']:r for r in old['records']}
FIVE={12027,12038,12049,12051,12093};SEVEN={12005,12023,12034,12050,12082,12156,12159};HOLDS=FIVE|SEVEN
rechecks={o:read(R/f'authored/native_diag70_05250_recheck7.{o}.memo-v1.json') for o in SEVEN}
rows=[];audits=[]
for cid,ordinal in zip(A['ids'],A['ordinals']):
 prior=oldby[cid];b=before['candidates'][cid];a=current['candidates'][cid]
 assert order[ordinal]==cid and b==prior['source_before']==P['original_records'][cid] and a==P['current_records'][cid]
 expected=copy.deepcopy(prior['source_after'])
 if ordinal in SEVEN:expected['record_kind']='visual_option';assert a==rechecks[ordinal]['unselected_minimal_alternatives'][1]['whole_after']
 assert a==expected
 own={k:v for k,v in current['slot_bindings'].items() if v['candidate_id']==cid};assert own=={} and n.referenced_records(a,current)=={} and P['references'][cid]==P['reference_bindings'][cid]=={}
 loc=I['original_decisions'][cid];compiled=read(loc['file'])['decisions'][loc['item']-1]
 assert raw(loc['file'])==loc['file_sha256'] and H(compiled)==loc['row_sha256'] and compiled==P['historical_compiled_rows'][cid]
 assert artifact(I['original_packets'][cid])['records'][cid]==b
 rev=I['required_revisions'][cid];previous=artifact(rev['prior_review']['artifact'])
 for part in rev['prior_review']['pointer'].strip('/').split('/'):previous=previous[int(part)] if isinstance(previous,list) else previous[part]
 assert H(previous)==rev['prior_review']['sha256']
 for ref in rev['memo_artifacts']:artifact(ref)
 row=copy.deepcopy(prior);row['source_after']=a;row['original_compiled']=loc
 if ordinal in HOLDS:
  row['status']='pending';row['proof']=None
  if ordinal in SEVEN:
   reason='Root selected kind-only positive recovery, preserving the exact original definition/conditions/effects and all other fields. '+rechecks[ordinal]['why_prior_nonsemantic_basis_is_not_sufficient']+' '+rechecks[ordinal]['unselected_minimal_alternatives'][1]['remaining_gap']
  else:reason=prior['rationale']+' This exact positive pending body and null proof are retained from01; the new source does not resolve its full positive fact/owner/mode/effect/obligation contract.'
  row['rationale']=reason
  row['delta']=[{'pointer':'/record_kind','before_exists':True,'before':'diagnostic','after_exists':True,'after':'visual_option','reason':'Root-selected positive contract recovery only; no positive meaning or condition removed and full native contract remains pending.'}]
 else:
  assert prior['status']=='diagnostic_reviewed' and a==prior['source_after'] and a['record_kind']=='diagnostic'
  assert H(current['slot_catalog'])==prior['proof']['catalog_sha256']
  rec=copy.deepcopy(a);rec['content']['role_evidence']=row['proof'];n.validate(rec,current['slot_catalog'],corpus={**current,'candidates':{**current['candidates'],cid:rec}})
  assert row['proof']==prior['proof']
  row['rationale']=prior['rationale']+' Exact whole source/catalog/empty closure and complete old proof are unchanged; retain this individual semantic judgment under the new input without new proof, signature or semantic-read credit.'
 row['revision']={'prior_review':rev['prior_review'],'memo_artifacts':rev['memo_artifacts'],'rationale':row['rationale']}
 rows.append(row);audits.append({'ordinal':ordinal,'candidate_id':cid,'prior_source_sha256':H(prior['source_after']),'current_source_sha256':H(a),'proof_sha256':H(row['proof']) if row['proof'] else None,'old_proof_sha256':H(prior['proof']) if prior['proof'] else None,'reuse58':ordinal not in HOLDS,'withdrawn_old_nonsemantic_proof':ordinal in SEVEN,'old_pending5_unchanged':ordinal in FIVE,'whole_kind_changed_after_direct_reread':ordinal in SEVEN,'fresh_signature_count':0,'new_unique_bulk_count':0})
assert len(rows)==70 and sum(r['status']=='diagnostic_reviewed' for r in rows)==58 and sum(r['proof'] is None for r in rows)==12
O.mkdir(parents=True,exist_ok=True)
batch={'schema':nr.BATCH,'task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment_sha256':H(A),'input_sha256':H(I),'prepared_count':70,'actual_read_count':70,'records':rows}
bp=save('BATCH.json',batch)
# Exact raw JSON proof value bytes, retaining original dict order/indentation.
dec=json.JSONDecoder()
def field(text,key):
 pos=text.index('{')+1
 while True:
  while text[pos].isspace() or text[pos]==',':pos+=1
  k,end=dec.raw_decode(text,pos);pos=end
  while text[pos].isspace():pos+=1
  assert text[pos]==':';pos+=1
  while text[pos].isspace():pos+=1
  start=pos;_,pos=dec.raw_decode(text,pos)
  if k==key:return text[start:pos]
def elements(text):
 pos=1;out=[]
 while True:
  while text[pos].isspace() or text[pos]==',':pos+=1
  if text[pos]==']':return out
  start=pos;_,pos=dec.raw_decode(text,pos);out.append(text[start:pos])
oldrows=elements(field(oldpath.read_text(),'records'));newrows=elements(field(Path(bp['file']).read_text(),'records'))
for k,row in enumerate(rows):
 if row['ordinal'] not in HOLDS:
  oldraw=field(oldrows[k],'proof');newraw=field(newrows[k],'proof');assert oldraw.encode()==newraw.encode()
  audits[k]['exact_raw_proof_value_bytes_reused']=True;audits[k]['raw_proof_value_sha256']=hashlib.sha256(newraw.encode()).hexdigest()
note={'schema':nr.NOTE,'task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment_sha256':H(A),'input_sha256':H(I),'batch_sha256':H(batch),'prepared_count':70,'actual_read_count':70,'whole_source_read_ids':A['ids'],'whole_dependency_read_ids':A['ids']};np=save('NOTE.json',note)
ra=save('READ-AUDIT-v1.json',{'schema':'photo-source96-diagnostic70-proof-reuse-audit/v1','task':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'input_sha256':H(I),'source96_sha256':H(current),'prior_batch_raw_sha256':raw(oldpath),'earlier_actual_whole_source_scope':70,'current_kind_changed_whole_after_reread_count':7,'current_kind_changed_ordinals':sorted(SEVEN),'unchanged_whole_body_reuse_count':63,'exact_raw_proof_reuse_count':58,'new_proof_signatures':0,'new_unique_bulk_count':0,'withdrawn_old_proofs_count':7,'unchanged_pending_count':5,'pending_total':12,'rows':audits,'boundary':'Seven selected kind-only afters were directly reread now; the original seven whole source/provenance/parent-purpose rechecks and earlier70 full read remain history.63 exact unchanged bodies reuse prior actual reading.58 proofs retain identical raw value bytes and signatures; no new semantic read/signature credit. Pending12 preserve all positive obligations; no native positive approval.'})
v=nr.verify_batch(str(D/'ASSIGNMENT.json'),bp['file'],np['file']);v={k:val for k,val in v.items() if k!='records'};v['read_audit']=ra;vf=save('VERIFICATION-v1.json',v)
print(json.dumps({'batch':bp,'note':np,'read_audit':ra,'verification':vf,'statuses':v['statuses'],'shape_valid':v['shape_valid'],'root_accepted':v['root_accepted'],'native_module':{'file':n.__file__,'sha256':raw(n.__file__)}},ensure_ascii=False))
