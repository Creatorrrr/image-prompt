import hashlib,json
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]; run=root/'run'; case=root.parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sealed(p):
 manifest=read(p); checked=[]
 for row in manifest['files']:
  f=Path(row['path']);assert f.is_relative_to(case)
  assert sha(f)==row['sha256'], ('frozen evidence mutated',str(f))
  checked.append({'path':str(f),'sha256':row['sha256']})
 return {'manifest':str(p),'checked_count':len(checked),'all_equal':True,'files':checked}
seals=[sealed(case/'run/ROUND-1-FROZEN.json'),sealed(run/'ROUND-2-FROZEN.json')]
source_proofs=[]
for parent in [case,root]:
 isolation=read(parent/'ISOLATION.json'); refs=isolation.get('runtime_members',{})
 if not refs: refs=isolation.get('source_members',{})
 checked=[]
 for rel,meta in refs.items():
  f=parent/'skill'/rel; expected=meta['sha256'] if isinstance(meta,dict) else meta
  assert sha(f)==expected,('original skill mutated',str(f));checked.append(str(f))
 source_proofs.append({'root':str(parent/'skill'),'checked_count':len(checked),'all_equal':True})
codes=read(run/'final-tool-code-hashes.json');original={f.name:sha(f) for f in (root/'tools/photo_data_maintenance').glob('*.py')};final={f.name:sha(f) for f in (root/'tool-final/tools/photo_data_maintenance').glob('*.py')}
assert original==codes['original_tool_code']==read(root/'ISOLATION.json')['tool_code']
assert final==codes['final_tool_code']
old_report=run/'maintenance-report';new_report=run/'management-final-report';old_manifest=read(old_report/'manifest.json');new_manifest=read(new_report/'manifest.json');receipt=read(run/'candidate_pack.runtime-receipt.json')
assert old_manifest['binding']==new_manifest['binding']
assert new_manifest['binding']['generation_id']==receipt['generation_id']
member_comparison=[]
for name in ['inventory.json','links.json']:
 a=old_report/name;b=new_report/name;assert a.read_bytes()==b.read_bytes()
 member_comparison.append({'name':name,'bytes_equal':True,'old_sha256':sha(a),'new_sha256':sha(b)})
for rel,digest in new_manifest['files'].items():
 f=new_report/rel;assert f.resolve().is_relative_to(new_report.resolve());assert sha(f)==digest
assert (run/'exposed-query-evidence.json').read_bytes()==(run/'final-tool-exposed-query-evidence.json').read_bytes()
previous_independent=read(run/'independent-source-link-check.json');new_independent=read(run/'final-tool-independent-source-link-check.json')
independent_bytes_equal=(run/'independent-source-link-check.json').read_bytes()==(run/'final-tool-independent-source-link-check.json').read_bytes()
proof_row_fields=['source_checks','source_files','candidate_source_checks']
for key in set(previous_independent)|set(new_independent):
 if key in proof_row_fields:
  canonical=lambda rows: sorted(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')) for row in rows)
  assert canonical(previous_independent[key])==canonical(new_independent[key]),('source proof differs',key)
 else:assert previous_independent[key]==new_independent[key],('independent projection differs',key)
independent=read(run/'final-tool-independent-source-link-check.json')
assert independent['status']=='PASS'
assert independent['raw_reference_ambiguities_global']==[]
forward=read(run/'final-tool-command-logs/final-tool-candidate-current.stdout');reverse=read(run/'final-tool-command-logs/final-tool-profile-reverse.stdout')
assert forward['paths']==reverse['paths'];assert forward['freshness']=='current_verified';assert forward['profile_activation']=='independent_request_evidence_only'
assert all(x['meaning_support']=='not_inferred' for x in forward['paths'])
baseline=(run/'baseline_prompt_en.txt').read_bytes();finalprompt=(run/'final_prompt_en.txt').read_bytes();assert baseline==finalprompt
composed=read(run/'composed_prompt.json');assert composed['chosen_candidate_ids']==[] and composed['chosen_visual_concept_ids']==[]
wrongroot=run/'final-tool-scratch/wrong-source-root'
for rel,meta in read(root/'ISOLATION.json')['runtime_members'].items():
 assert sha(wrongroot/rel)==meta['sha256']
result={'schema':'independent-final-tool-preservation/v1','checked_at_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','frozen_evidence':seals,'source_roots':source_proofs,'original_tool_code_equal':True,'final_tool_code_equal':True,'same_generation_and_binding':True,'generation_id':receipt['generation_id'],'source_fingerprint':new_manifest['binding']['source_fingerprint'],'report_member_comparison':member_comparison,'new_manifest_members_verified':len(new_manifest['files']),'exposed_query_bytes_equal':True,'independent_source_check_bytes_equal':independent_bytes_equal,'independent_edge_query_projection_equal':True,'independent_source_proof_rows_equal_after_order_normalization':True,'representative_bidirectional_paths_equal':True,'baseline_and_final_prompt_bytes_equal':True,'new_retrieval_or_authorship_performed':False,'wrong_root_is_byte_identical_clone':True,'scope':'case-05 only; original inputs, core, packs, receipts, QA and skill files unchanged'}
(run/'final-tool-preservation-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['frozen_evidence']},ensure_ascii=False,indent=2))
