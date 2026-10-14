"""Mechanical wire only. No facts, decisions or statuses are generated here."""
import json,gzip,hashlib,sys,copy
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review11870-01250-01300-04';O=R/'native_batches/review11870-01250-01300-04'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import photo_candidate_realizations as real
I=json.loads((D/'INPUT.json').read_text());A=json.loads((D/'ASSIGNMENT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));CAT=I['catalog_review']['after'];CH=c.digest(CAT)
assert CH=='3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645'
assert c.digest(I)=='3fd6d324114f6d5816d2328f528e9d3ceaaf459d401e312ba7c263b846fd7e69'
assert c.digest(S)=='88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8'
assert c.digest(A)=='e9d026cec722ba3044a6edf8a092a59ace719f48b14eb05cb4877a5a77d203ad'
ROWS=[];CHECKS=[]
def F(fid,ptr,q,d,t,p,mode,vt,value,requires,operation=None,receivers=None):
 f={'id':fid,'realization_id':'base','pointer':'/content/'+ptr,'quote':q,'dimension':d,'target':t,'property':p,'mode':mode,'value':{'type':vt,'value':value},'requires':requires}
 if mode=='effect':
  assert operation is not None and receivers is not None
  f.update(operation=operation,receivers=receivers)
 return f
def unit(ptr,refs):return (ptr,refs)
def delta(before,after,reason):
 return [{'pointer':'/'+field,'before_exists':True,'before':before[field],'after_exists':True,'after':after[field],'reason':reason}for field in ['content','conditions','effects','provenance','record_kind']if before[field]!=after[field]]
def owner_map(owners):
 return {'schema':n.SELECTOR_OWNER_SCHEMA,'bindings':[{'target':target,'selector':{'kind':'selected_existing_owner'}if role is None else {'kind':'core_role','role':role},'origin':'existing','introduced_by':None}for target,role in owners]}
def row(ordinal,status,rationale,facts=None,roles=None,owners=None,units=None):
 cid=A['ids'][ordinal-1250];before=P['original_records'][cid];after=P['current_records'][cid];old=P['historical_compiled_rows'][cid];revision=I['required_revisions'][cid];proof=None
 assert before['id']==after['id']==cid
 assert real.ids(after)==['base']
 if status=='approved':
  assert facts is not None and roles is not None and owners is not None and units is not None
  proof={'schema':n.SCHEMA,'meaning_sha256':n.meaning_sha256(after),'catalog_sha256':CH,'complete':True,'facts':facts,'roles':{tag:{'spec_sha256':c.digest(CAT[tag]),'scope':'whole_record','realization_ids':['base'],'fact_refs':refs,'support_modes':modes}for tag,refs,modes in roles},'owner_maps':{'base':owner_map(owners)},'source_units':[{'realization_id':'base','pointer':'/content/'+ptr,'quote':after['content'][ptr],'fact_refs':refs,'disposition':'semantic'}for ptr,refs in units],'effect_sets':{'base':{'dimensions':sorted(after['effects']['dimensions']),'properties':sorted(after['effects']['properties'],key=n.property_key)}},'dependencies':{'base':[]},'reference_sha256':{},'guard_sets':{'base':{'source_conditions':[after['conditions'],{}],'member_conditions':{}}},'profile_contracts':{'base':None},'review':{'basis':rationale,'whole_source_reviewed':True,'source_correction':None if n.meaning_sha256(before)==n.meaning_sha256(after)else {'before_sha256':n.meaning_sha256(before),'after_sha256':n.meaning_sha256(after),'rationale':'Fresh direct reread of the complete exact formal04 assigned after, with all source qualifications and selected effects retained. '+rationale},'original_review':{'candidate_id':cid,'source_record_sha256':old['source_record_sha256'],'catalog_sha256':old['catalog_sha256'],'decision_sha256':I['original_decisions'][cid]['row_sha256'],'artifact':I['original_decisions'][cid]['file']+'#item='+str(I['original_decisions'][cid]['item'])},'native_review':{'reviewer':'/root/review_11870_12250','method':'codex_subagent_direct_source_read','native_contract_sha256':''}}}
  proof['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(proof)
  record=copy.deepcopy(after);record['content']['role_evidence']=proof
  n.validate(record,CAT,catalog_sha256=CH,corpus=S)
  CHECKS.append({'ordinal':ordinal,'full_source_validation':True,'proof_sha256':c.digest(proof),'native_signature':proof['review']['native_review']['native_contract_sha256']})
 ROWS.append({'candidate_id':cid,'ordinal':ordinal,'status':status,'rationale':rationale,'source_before':before,'source_after':after,'delta':delta(before,after,'Exact formal04 INPUT assignment, complete direct semantic reread. '+rationale),'original_compiled':I['original_decisions'][cid],'proof':proof,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':revision['prior_review'],'memo_artifacts':revision['memo_artifacts'],'rationale':'Fresh individual formal04 decision; no old-status/proof conversion. '+rationale}})
