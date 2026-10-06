from pathlib import Path
from datetime import datetime, timezone
import os, hashlib, json, shutil, subprocess

root=Path(__file__).resolve().parent.parent
run=root/'run'
python=root.parent/'venv/bin/python'
cli=root/'tool-final/tools/photo_data_maintenance/cli.py'
report=run/'management-final-report'
old_report=run/'management-report'
receipt=json.loads((run/'runtime_receipt.json').read_text())
generation=receipt['generation_id']
evidence=run/'final-tool-evidence'
sha=lambda data:hashlib.sha256(data).hexdigest()
canon=lambda value:json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
now=lambda:datetime.now(timezone.utc).isoformat()
read=lambda path:json.loads(path.read_text(encoding='utf-8'))
write=lambda path,value:path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def snapshot(directory):
    return {str(p):sha(p.read_bytes()) for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts}

protected={}
for directory in (run,root/'skill',root/'tools',root/'runtime',root/'precore-frozen',root.parent/'run'):
    protected.update(snapshot(directory))
protected[str(root/'ISOLATION.json')]=sha((root/'ISOLATION.json').read_bytes())
if report.exists() or evidence.exists():raise RuntimeError('Final-tool output already exists; original evidence preserved')
evidence.mkdir()
write(evidence/'protected-input-hashes.json',protected)
code_before={p.name:sha(p.read_bytes()) for p in sorted((root/'tools/photo_data_maintenance').glob('*.py'))}
code_after={p.name:sha(p.read_bytes()) for p in sorted(cli.parent.glob('*.py'))}
changed_code=[key for key in sorted(set(code_before)|set(code_after)) if code_before.get(key)!=code_after.get(key)]
commands=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')

def execute(label,args,expected_exit=0):
    argv=[str(python),str(cli),*map(str,args)]
    started=now()
    result=subprocess.run(argv,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8')
    stdout=evidence/(label+'.stdout.txt');stderr=evidence/(label+'.stderr.txt')
    stdout.write_text(result.stdout);stderr.write_text(result.stderr)
    record={'label':label,'argv':argv,'cwd':str(root),'started_at_utc':started,'ended_at_utc':now(),'expected_exit_code':expected_exit,'exit_code':result.returncode,'stdout_path':str(stdout),'stderr_path':str(stderr),'stdout_sha256':sha(result.stdout.encode()),'stderr_sha256':sha(result.stderr.encode()),'exit_matches':result.returncode==expected_exit}
    commands.append(record)
    with (run/'FINAL-TOOL-COMMANDS.ndjson').open('a') as stream:stream.write(json.dumps(record,ensure_ascii=False)+'\n')
    print(json.dumps({'command':label,'exit':result.returncode,'expected':expected_exit,'ended_at_utc':record['ended_at_utc']},ensure_ascii=False),flush=True)
    return result,record

started=now()
build,build_command=execute('build-generation-report',['build','--source-root',root/'skill','--runtime-store',root/'runtime','--generation',generation,'--output',report])
if build.returncode:raise RuntimeError('Final report build failed; evidence saved')
manifest=read(report/'manifest.json');old_manifest=read(old_report/'manifest.json')
member_comparison={name:{'old_sha256':sha((old_report/name).read_bytes()),'new_sha256':sha((report/name).read_bytes()),'bytes_equal':(old_report/name).read_bytes()==(report/name).read_bytes()} for name in ('inventory.json','links.json')}
inventory=read(report/'inventory.json');nodes={row['id']:row for row in inventory['nodes']}
links=read(report/'links.json')

# Independent projection: use only authored immutable files, never maintenance helpers.
assets=root/'runtime/generations'/generation/'assets'
source_manifest=read(assets/'photo_prompt_source_manifest.json')
kinds={'photo_prompt_tags.json':'candidate','photo_prompt_visual_obligations.json':'visual_profile'}
kinds.update({row['file']:row['kind'] for row in source_manifest['sources']})
raw_nodes={};source_refs={};raw_bundles={};by_id={};source_file_checks={};patch_refs={}
escape=lambda value:str(value).replace('~','~0').replace('/','~1')

def add(nid,row,name,pointer):
    if nid in raw_nodes:raise RuntimeError('Duplicate raw identity '+nid)
    raw_nodes[nid]=row;source_refs[nid]=[{'file':name,'pointer':pointer}]

for name,kind in sorted(kinds.items()):
    path=assets/name
    if not path.is_file():continue
    value=read(path);original=path.read_bytes()
    source_file_checks[name]={'sha256':sha(original),'new_report_exact':original==(report/'inputs'/name).read_bytes(),'old_report_exact':original==(old_report/'inputs'/name).read_bytes()}
    if kind=='candidate':
        for slot,rows in value.get('slots',{}).items():
            for index,row in enumerate(rows):
                nid=f"slot:{slot}:{row['id']}";add(nid,row,name,f'/slots/{escape(slot)}/{index}')
                by_id.setdefault(row['id'],[]).append(nid)
        for index,row in enumerate(value.get('visual_semantics',[])):
            nid='bundle:'+row['id'];add(nid,row,name,f'/visual_semantics/{index}');raw_bundles[nid]=row
        for slot,patches in value.get('existing_slot_context_extensions',{}).items():
            for entry_id in patches:
                patch_refs.setdefault(f'slot:{slot}:{entry_id}',[]).append({'file':name,'pointer':f'/existing_slot_context_extensions/{escape(slot)}/{escape(entry_id)}'})
    elif kind=='visual_profile':
        for index,row in enumerate(value.get('profiles',[])):add('profile:'+row['id'],row,name,f'/profiles/{index}')
for nid,refs in patch_refs.items():
    if nid in source_refs:source_refs[nid].extend(refs)
expected_edges=set();members={};associations={}
for bid,row in raw_bundles.items():
    cids=[]
    for entry_id in row.get('candidate_ids',[]):
        slot=row.get('candidate_slots',{}).get(entry_id)
        candidates=[f'slot:{slot}:{entry_id}'] if slot else by_id.get(entry_id,[])
        if len(candidates)!=1 or candidates[0] not in raw_nodes:raise RuntimeError('Raw identity resolution failed '+entry_id)
        cid=candidates[0];cids.append(cid);expected_edges.add((cid,'member_of',bid))
    pids=list(row.get('hard_profile_ids',[]))+list(row.get('associated_profile_ids',[]))
    if row.get('hard_profile_id'):pids.append(row['hard_profile_id'])
    pids=sorted(set('profile:'+pid for pid in pids))
    for pid in pids:
        if pid not in raw_nodes:raise RuntimeError('Unknown raw profile '+pid)
        expected_edges.add((bid,'associated_with',pid))
    members[bid]=sorted(set(cids));associations[bid]=pids
actual_edges={(row['source'],row['type'],row['target']) for row in links['edges']}
old_edges={(row['source'],row['type'],row['target']) for row in read(old_report/'links.json')['edges']}
projection={'independence':'Fresh projection from immutable authored candidate_ids/candidate_slots and profile declarations; no maintenance graph, query, or corpus imports.','generation_id':generation,'raw_candidate_count':sum(nid.startswith('slot:') for nid in raw_nodes),'raw_bundle_count':len(raw_bundles),'raw_profile_count':sum(nid.startswith('profile:') for nid in raw_nodes),'expected_edge_count':len(expected_edges),'new_report_edge_count':len(actual_edges),'old_report_edge_count':len(old_edges),'missing_edges':sorted(expected_edges-actual_edges),'extra_edges':sorted(actual_edges-expected_edges),'new_equals_old_projection':actual_edges==old_edges,'source_file_checks':source_file_checks}
write(evidence/'independent-edge-projection.json',projection)

candidate='slot:color:cr_candidate_accent_cluster';profile='profile:cr_accent_cluster'

def expected_paths(nid):
    paths=[]
    for bid,cids in members.items():
        if nid.startswith('slot:') and nid in cids:paths.extend([[nid,bid,pid] for pid in associations[bid]] or [[nid,bid]])
        elif nid.startswith('profile:') and nid in associations[bid]:paths.extend([[cid,bid,nid] for cid in cids] or [[bid,nid]])
    return sorted(paths)

queries={}
for label,option,nid in (('candidate-forward','--candidate',candidate),('profile-reverse','--profile',profile)):
    argument=nid if option=='--candidate' else nid.split(':',1)[1]
    result,command=execute(label,['query','--report',report,option,argument,'--source-root',root/'skill','--runtime-store',root/'runtime'])
    value=json.loads(result.stdout);ref_failures=[]
    for path in value['paths']:
        for identity,refs in path['source_refs'].items():
            norm=lambda rows:sorted((row['file'],row['pointer']) for row in rows)
            if norm(refs)!=norm(source_refs[identity]):ref_failures.append(identity)
        for identity,entity_hash in path['entity_hashes'].items():
            if entity_hash!=nodes[identity]['entity_sha256']:ref_failures.append('hash:'+identity)
    paths=sorted(path['nodes'] for path in value['paths'])
    queries[nid]={'paths':paths,'path_count':value['path_count'],'expected_paths':expected_paths(nid),'raw_paths_match':paths==expected_paths(nid),'source_ref_failures':ref_failures,'generation_matches':value['generation_id']==generation,'source_fingerprint_matches':value['source_fingerprint']==receipt['source_fingerprint'],'meaning_supports':[path['meaning_support'] for path in value['paths']],'profile_activation':value['profile_activation'],'freshness':value['freshness'],'command':command}
forward_paths=queries[candidate]['paths'];reverse_paths=queries[profile]['paths']
reverse_complete=all(path in reverse_paths for path in forward_paths)
current,current_command=execute('require-current-normal',['query','--report',report,'--candidate',candidate,'--require-current','--source-root',root/'skill','--runtime-store',root/'runtime'])
current_value=json.loads(current.stdout)

scratch=run/'final-tool-scratch';scratch.mkdir()
broken=scratch/'checksum-damaged-report';shutil.copytree(report,broken)
broken_links=read(broken/'links.json');broken_links['edges'][0]['target']='bundle:__intentional_checksum_damage'
write(broken/'links.json',broken_links)
corrupt,corrupt_command=execute('require-current-checksum-damage',['query','--report',broken,'--candidate',candidate,'--require-current','--source-root',root/'skill','--runtime-store',root/'runtime'],1)
wrong_root=scratch/'wrong-root';wrong_root.mkdir()
wrong,wrong_command=execute('require-current-wrong-root',['query','--report',report,'--candidate',candidate,'--require-current','--source-root',wrong_root,'--runtime-store',root/'runtime'],1)

# Exercise changed draft-only branch; malformed source exists only in an isolated copy.
draft=scratch/'malformed-draft-skill'
shutil.copytree(root/'skill',draft,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
draft_source=draft/'assets/photo_prompt_realistic_background_extension.json'
draft_before=sha(draft_source.read_bytes());draft_value=read(draft_source)
draft_value['slots']=['malformed-slot-object'];write(draft_source,draft_value)
draft_report=scratch/'malformed-draft-report'
malformed,malformed_command=execute('audit-malformed-draft',['audit','--source-root',draft,'--runtime-store',root/'runtime','--output',draft_report],1)
draft_manifest=read(draft_report/'manifest.json') if (draft_report/'manifest.json').is_file() else None
draft_findings=read(draft_report/'findings.json') if (draft_report/'findings.json').is_file() else None
findings_rows=draft_findings.get('findings',[]) if isinstance(draft_findings,dict) else draft_findings or []
malformed_summary={'scratch_source_root':str(draft),'changed_file':str(draft_source),'before_sha256':draft_before,'after_sha256':sha(draft_source.read_bytes()),'mutation':"slots=['malformed-slot-object']",'return_code':malformed.returncode,'structured_report_written':draft_manifest is not None,'input_mode':draft_manifest['binding']['input_mode'] if draft_manifest else None,'generation_id':draft_manifest['binding']['generation_id'] if draft_manifest else None,'findings_count':draft_manifest['findings_count'] if draft_manifest else None,'source_records_invalid':[row for row in findings_rows if row.get('rule')=='source_records_invalid'],'authored_contract_invalid':[row for row in findings_rows if row.get('rule')=='authored_contract_invalid'],'traceback_in_stderr':'Traceback' in malformed.stderr,'command':malformed_command}

protection_failures=[{'path':path,'expected':expected,'actual':sha(Path(path).read_bytes()) if Path(path).is_file() else None} for path,expected in protected.items() if not Path(path).is_file() or sha(Path(path).read_bytes())!=expected]
final_code={p.name:sha(p.read_bytes()) for p in sorted(cli.parent.glob('*.py'))}
all_query_checks=all(value['raw_paths_match'] and not value['source_ref_failures'] and value['generation_matches'] and value['source_fingerprint_matches'] and value['profile_activation']=='independent_request_evidence_only' and all(s=='not_inferred' for s in value['meaning_supports']) for value in queries.values())
malformed_ok=malformed.returncode==1 and draft_manifest is not None and draft_manifest['binding']['input_mode']=='draft' and draft_manifest['binding']['generation_id'] is None and bool(malformed_summary['source_records_invalid']) and any("has no attribute 'items'" in row.get('message','') for row in malformed_summary['authored_contract_invalid']) and not malformed_summary['traceback_in_stderr']
checks={'only_corpus_code_changed':changed_code==['corpus.py'],'code_unchanged_during_verification':code_after==final_code,'build_exit_zero':build.returncode==0,'generation_matches':manifest['binding']['generation_id']==generation,'source_fingerprint_matches':manifest['binding']['source_fingerprint']==receipt['source_fingerprint'],'inventory_bytes_equal':member_comparison['inventory.json']['bytes_equal'],'links_bytes_equal':member_comparison['links.json']['bytes_equal'],'raw_projection_complete':actual_edges==expected_edges==old_edges,'source_copy_bytes_equal':all(row['new_report_exact'] and row['old_report_exact'] for row in source_file_checks.values()),'representative_queries_match_raw':all_query_checks,'representative_bidirectional_paths_complete':reverse_complete,'current_normal_verified':current.returncode==0 and current_value['freshness']=='current_verified','checksum_damage_rejected':corrupt.returncode==1 and 'report_invalid: report member checksum mismatch: links.json' in corrupt.stderr,'wrong_root_rejected':wrong.returncode==1 and 'report_not_current: report authority/root differs from requested source' in wrong.stderr,'malformed_draft_diagnostic_preserved':malformed_ok,'all_preexisting_evidence_and_sources_unchanged':not protection_failures}
result={'schema':'final-tool-verification/v1','case_id':'case-03','round':2,'status':'PASS' if all(checks.values()) else 'FAIL','started_at_utc':started,'completed_at_utc':now(),'generation_id':generation,'source_fingerprint':receipt['source_fingerprint'],'original_report_id':old_manifest['report_id'],'final_report_id':manifest['report_id'],'cli_absolute_path':str(cli),'python_absolute_path':str(python),'code_hashes_before':code_before,'code_hashes_final':code_after,'changed_code_files':changed_code,'checks':checks,'member_comparison':member_comparison,'edge_projection':{k:v for k,v in projection.items() if k!='source_file_checks'},'independent_edge_evidence':str(evidence/'independent-edge-projection.json'),'representative_queries':queries,'reverse_complete':reverse_complete,'freshness_cases':{'normal':{'exit':current.returncode,'freshness':current_value.get('freshness'),'command':current_command},'checksum_damage':{'exit':corrupt.returncode,'stderr':corrupt.stderr,'command':corrupt_command},'wrong_root':{'exit':wrong.returncode,'stderr':wrong.stderr,'command':wrong_command}},'malformed_draft':malformed_summary,'original_preservation':{'protected_file_count':len(protected),'failures':protection_failures,'protected_hashes_file':str(evidence/'protected-input-hashes.json'),'original_QA_RESULT_sha256':sha((run/'QA-RESULT.json').read_bytes()),'original_QA_REPORT_sha256':sha((run/'QA-REPORT.md').read_bytes()),'final_prompt_en_sha256':sha((run/'final_prompt_en.txt').read_bytes()),'runtime_receipt_sha256':sha((run/'runtime_receipt.json').read_bytes())},'commands':commands,'proof_boundary':{'new_retrieval':False,'new_prompt_or_input':False,'native_image_pixels':'not_generated','user_acceptance':'not_assessed','network_API_or_image_calls':0,'active_skill_or_old_tools_mutated':False,'malformed_draft_is_scratch_only':True},'evaluation_ko':'활성 세대의 inventory·links와 전체 원본 edge 및 대표 양방향 조회가 유지됐고, 정상 최신성 조회와 손상/root 거부가 통과했다. malformed scratch draft의 native AttributeError도 구조화 진단으로 보존됐다. 기존 QA·입력·프롬프트·원본 source는 변경하지 않았다.'}
write(run/'FINAL-TOOL-VERIFICATION.json',result)
print(json.dumps({'status':result['status'],'checks':checks,'final_report_id':manifest['report_id'],'evidence':str(run/'FINAL-TOOL-VERIFICATION.json')},ensure_ascii=False,indent=2),flush=True)
