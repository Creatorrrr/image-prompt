from pathlib import Path
from datetime import datetime, timezone
import os, hashlib, json, subprocess

root=Path(__file__).resolve().parent.parent;run=root/'run'
python=root.parent/'venv/bin/python';cli=root/'tool-final/tools/photo_data_maintenance/cli.py'
report=run/'management-final-report';old_report=run/'management-report';evidence=run/'final-tool-evidence'
sha=lambda data:hashlib.sha256(data).hexdigest()
canon=lambda value:json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
now=lambda:datetime.now(timezone.utc).isoformat()
read=lambda path:json.loads(path.read_text(encoding='utf-8'))
write=lambda path,value:path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt=read(run/'runtime_receipt.json');generation=receipt['generation_id']
manifest=read(report/'manifest.json');old_manifest=read(old_report/'manifest.json')
inventory=read(report/'inventory.json');nodes={row['id']:row for row in inventory['nodes']};links=read(report/'links.json')
protected=read(evidence/'protected-input-hashes.json')
commands=[json.loads(line) for line in (run/'FINAL-TOOL-COMMANDS.ndjson').read_text().splitlines()]
if len(commands)!=6:raise RuntimeError('Unexpected previous command state')
code_before={p.name:sha(p.read_bytes()) for p in sorted((root/'tools/photo_data_maintenance').glob('*.py'))}
code_after={p.name:sha(p.read_bytes()) for p in sorted(cli.parent.glob('*.py'))}
changed_code=[key for key in sorted(set(code_before)|set(code_after)) if code_before.get(key)!=code_after.get(key)]
member_comparison={name:{'old_sha256':sha((old_report/name).read_bytes()),'new_sha256':sha((report/name).read_bytes()),'bytes_equal':(old_report/name).read_bytes()==(report/name).read_bytes()} for name in ('inventory.json','links.json')}
# Execute only the self-contained raw projection section of our retained harness.
original_harness=(run/'verify_final_tool.py').read_text()
section=original_harness.split('# Independent projection:',1)[1].split('\nqueries={}',1)[0]
exec('# Independent projection:'+section)
queries={}
for label,nid in (('candidate-forward',candidate),('profile-reverse',profile)):
    value=read(evidence/(label+'.stdout.txt'));ref_failures=[]
    for path in value['paths']:
        for identity,refs in path['source_refs'].items():
            norm=lambda rows:sorted((row['file'],row['pointer']) for row in rows)
            if norm(refs)!=norm(source_refs[identity]):ref_failures.append(identity)
        for identity,entity_hash in path['entity_hashes'].items():
            if entity_hash!=nodes[identity]['entity_sha256']:ref_failures.append('hash:'+identity)
    paths=sorted(path['nodes'] for path in value['paths'])
    queries[nid]={'paths':paths,'path_count':value['path_count'],'expected_paths':expected_paths(nid),'raw_paths_match':paths==expected_paths(nid),'source_ref_failures':ref_failures,'generation_matches':value['generation_id']==generation,'source_fingerprint_matches':value['source_fingerprint']==receipt['source_fingerprint'],'meaning_supports':[path['meaning_support'] for path in value['paths']],'profile_activation':value['profile_activation'],'freshness':value['freshness'],'command':next(row for row in commands if row['label']==label)}
reverse_complete=all(path in queries[profile]['paths'] for path in queries[candidate]['paths'])
current_value=read(evidence/'require-current-normal.stdout.txt')
corrupt_stderr=(evidence/'require-current-checksum-damage.stderr.txt').read_text()
wrong_stderr=(evidence/'require-current-wrong-root.stderr.txt').read_text()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')

def execute(label,args,expected_exit):
    argv=[str(python),str(cli),*map(str,args)];started=now()
    result=subprocess.run(argv,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8')
    stdout=evidence/(label+'.stdout.txt');stderr=evidence/(label+'.stderr.txt')
    stdout.write_text(result.stdout);stderr.write_text(result.stderr)
    record={'label':label,'argv':argv,'cwd':str(root),'started_at_utc':started,'ended_at_utc':now(),'expected_exit_code':expected_exit,'exit_code':result.returncode,'stdout_path':str(stdout),'stderr_path':str(stderr),'stdout_sha256':sha(result.stdout.encode()),'stderr_sha256':sha(result.stderr.encode()),'exit_matches':result.returncode==expected_exit}
    commands.append(record)
    with (run/'FINAL-TOOL-COMMANDS.ndjson').open('a') as stream:stream.write(json.dumps(record,ensure_ascii=False)+'\n')
    print(json.dumps({'command':label,'exit':result.returncode,'expected':expected_exit},ensure_ascii=False),flush=True)
    return result,record

draft=run/'final-tool-scratch/malformed-draft-skill'
draft_source=draft/'assets/photo_prompt_realistic_background_extension.json'
draft_before=sha(draft_source.read_bytes());draft_source.chmod(0o644)
draft_value=read(draft_source);draft_value['slots']=['malformed-slot-object'];write(draft_source,draft_value)
draft_report=run/'final-tool-scratch/malformed-draft-report'
malformed,malformed_command=execute('audit-malformed-draft',['audit','--source-root',draft,'--runtime-store',root/'runtime','--output',draft_report],1)
draft_manifest=read(draft_report/'manifest.json') if (draft_report/'manifest.json').is_file() else None
draft_findings=read(draft_report/'findings.json') if (draft_report/'findings.json').is_file() else None
findings_rows=draft_findings.get('findings',[]) if isinstance(draft_findings,dict) else draft_findings or []
malformed_summary={'scratch_source_root':str(draft),'changed_file':str(draft_source),'before_sha256':draft_before,'after_sha256':sha(draft_source.read_bytes()),'mutation':"slots=['malformed-slot-object']",'return_code':malformed.returncode,'structured_report_written':draft_manifest is not None,'input_mode':draft_manifest['binding']['input_mode'] if draft_manifest else None,'generation_id':draft_manifest['binding']['generation_id'] if draft_manifest else None,'findings_count':draft_manifest['findings_count'] if draft_manifest else None,'source_records_invalid':[row for row in findings_rows if row.get('rule')=='source_records_invalid'],'authored_contract_invalid':[row for row in findings_rows if row.get('rule')=='authored_contract_invalid'],'traceback_in_stderr':'Traceback' in malformed.stderr,'command':malformed_command}
# Independent fallback inventory check, skipping only the single malformed source.
expected_draft_nodes={nid:record for nid,record in raw_nodes.items() if source_refs[nid][0]['file']!='photo_prompt_realistic_background_extension.json'}
draft_nodes={node['id']:node['record'] for node in read(draft_report/'inventory.json')['nodes']} if draft_manifest else {}
malformed_summary['fallback_raw_inventory_matches']=draft_nodes==expected_draft_nodes
malformed_summary['fallback_raw_node_count']=len(expected_draft_nodes)
malformed_summary['returned_inventory_node_count']=len(draft_nodes)
protection_failures=[{'path':path,'expected':expected,'actual':sha(Path(path).read_bytes()) if Path(path).is_file() else None} for path,expected in protected.items() if not Path(path).is_file() or sha(Path(path).read_bytes())!=expected]
final_code={p.name:sha(p.read_bytes()) for p in sorted(cli.parent.glob('*.py'))}
all_query_checks=all(value['raw_paths_match'] and not value['source_ref_failures'] and value['generation_matches'] and value['source_fingerprint_matches'] and value['profile_activation']=='independent_request_evidence_only' and all(s=='not_inferred' for s in value['meaning_supports']) for value in queries.values())
malformed_ok=malformed.returncode==1 and draft_manifest is not None and draft_manifest['binding']['input_mode']=='draft' and draft_manifest['binding']['generation_id'] is None and bool(malformed_summary['source_records_invalid']) and any("has no attribute 'items'" in row.get('message','') for row in malformed_summary['authored_contract_invalid']) and not malformed_summary['traceback_in_stderr'] and malformed_summary['fallback_raw_inventory_matches']
command_map={row['label']:row for row in commands}
checks={'only_corpus_code_changed':changed_code==['corpus.py'],'code_unchanged_during_verification':code_after==final_code,'build_exit_zero':command_map['build-generation-report']['exit_code']==0,'generation_matches':manifest['binding']['generation_id']==generation,'source_fingerprint_matches':manifest['binding']['source_fingerprint']==receipt['source_fingerprint'],'inventory_bytes_equal':member_comparison['inventory.json']['bytes_equal'],'links_bytes_equal':member_comparison['links.json']['bytes_equal'],'raw_projection_complete':actual_edges==expected_edges==old_edges,'source_copy_bytes_equal':all(row['new_report_exact'] and row['old_report_exact'] for row in source_file_checks.values()),'representative_queries_match_raw':all_query_checks,'representative_bidirectional_paths_complete':reverse_complete,'current_normal_verified':command_map['require-current-normal']['exit_code']==0 and current_value['freshness']=='current_verified','checksum_damage_rejected':command_map['require-current-checksum-damage']['exit_code']==1 and 'report_invalid: report member checksum mismatch: links.json' in corrupt_stderr,'wrong_root_rejected':command_map['require-current-wrong-root']['exit_code']==1 and 'report_not_current: report authority/root differs from requested source' in wrong_stderr,'malformed_draft_diagnostic_preserved':malformed_ok,'all_preexisting_evidence_and_sources_unchanged':not protection_failures}
result={'schema':'final-tool-verification/v1','case_id':'case-03','round':2,'status':'PASS' if all(checks.values()) else 'FAIL','started_at_utc':commands[0]['started_at_utc'],'completed_at_utc':now(),'generation_id':generation,'source_fingerprint':receipt['source_fingerprint'],'original_report_id':old_manifest['report_id'],'final_report_id':manifest['report_id'],'cli_absolute_path':str(cli),'python_absolute_path':str(python),'code_hashes_before':code_before,'code_hashes_final':code_after,'changed_code_files':changed_code,'checks':checks,'member_comparison':member_comparison,'edge_projection':{k:v for k,v in projection.items() if k!='source_file_checks'},'independent_edge_evidence':str(evidence/'independent-edge-projection.json'),'representative_queries':queries,'reverse_complete':reverse_complete,'freshness_cases':{'normal':{'exit':command_map['require-current-normal']['exit_code'],'freshness':current_value.get('freshness'),'command':command_map['require-current-normal']},'checksum_damage':{'exit':command_map['require-current-checksum-damage']['exit_code'],'stderr':corrupt_stderr,'command':command_map['require-current-checksum-damage']},'wrong_root':{'exit':command_map['require-current-wrong-root']['exit_code'],'stderr':wrong_stderr,'command':command_map['require-current-wrong-root']}},'malformed_draft':malformed_summary,'harness_recovery':{'status':'recovered','issue':'Initial harness stopped before the malformed audit because copied immutable source retained read-only permissions. Only the scratch source file was chmod 0644; completed build/query commands and original evidence were preserved.','original_harness_path':str(run/'verify_final_tool.py'),'original_harness_sha256':sha((run/'verify_final_tool.py').read_bytes()),'recovery_harness_path':str(Path(__file__))},'original_preservation':{'protected_file_count':len(protected),'failures':protection_failures,'protected_hashes_file':str(evidence/'protected-input-hashes.json'),'original_QA_RESULT_sha256':sha((run/'QA-RESULT.json').read_bytes()),'original_QA_REPORT_sha256':sha((run/'QA-REPORT.md').read_bytes()),'final_prompt_en_sha256':sha((run/'final_prompt_en.txt').read_bytes()),'runtime_receipt_sha256':sha((run/'runtime_receipt.json').read_bytes())},'commands':commands,'proof_boundary':{'new_retrieval':False,'new_prompt_or_input':False,'native_image_pixels':'not_generated','user_acceptance':'not_assessed','network_API_or_image_calls':0,'active_skill_or_old_tools_mutated':False,'malformed_draft_is_scratch_only':True},'evaluation_ko':'활성 세대의 inventory·links와 전체 원본 edge 및 대표 양방향 조회가 유지됐고, 정상 최신성 조회와 손상/root 거부가 통과했다. malformed scratch draft의 native AttributeError도 구조화 진단으로 보존됐다. 기존 QA·입력·프롬프트·원본 source는 변경하지 않았다.'}
write(run/'FINAL-TOOL-VERIFICATION.json',result)
print(json.dumps({'status':result['status'],'checks':checks,'malformed_draft':{k:v for k,v in malformed_summary.items() if k!='command'},'final_report_id':manifest['report_id'],'evidence':str(run/'FINAL-TOOL-VERIFICATION.json')},ensure_ascii=False,indent=2),flush=True)
