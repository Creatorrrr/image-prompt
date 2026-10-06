from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import subprocess
import sys

root=Path(__file__).resolve().parent.parent
run=root/'run'; report=run/'management-report'
receipt=json.loads((run/'runtime_receipt.json').read_text(encoding='utf-8'))
assets=root/'runtime/generations'/receipt['generation_id']/'assets'
source_manifest=json.loads((assets/'photo_prompt_source_manifest.json').read_text(encoding='utf-8'))
report_manifest=json.loads((report/'manifest.json').read_text(encoding='utf-8'))
inventory=json.loads((report/'inventory.json').read_text(encoding='utf-8'))
reported_nodes={n['id']:n for n in inventory['nodes']}
reported_links=json.loads((report/'links.json').read_text(encoding='utf-8'))
plan=json.loads((run/'management-query-plan.json').read_text(encoding='utf-8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
escape=lambda s:str(s).replace('~','~0').replace('/','~1')
kinds={'photo_prompt_tags.json':'candidate','photo_prompt_visual_obligations.json':'visual_profile'}
kinds.update({row['file']:row['kind'] for row in source_manifest['sources']})
raw_nodes={}; refs={}; raw_bundles={}; candidates_by_id={}; file_evidence={}; patch_refs={}

def add(nid,record,filename,pointer):
    if nid in raw_nodes: raise ValueError('duplicate raw source identity '+nid)
    raw_nodes[nid]=record
    refs[nid]=[{'file':filename,'pointer':pointer}]

for filename,kind in sorted(kinds.items()):
    source_path=assets/filename
    if not source_path.is_file():continue
    source_bytes=source_path.read_bytes(); value=json.loads(source_bytes)
    report_bytes=(report/'inputs'/filename).read_bytes()
    file_evidence[filename]={'snapshot_path':str(source_path),'snapshot_sha256':sha(source_bytes),'report_copy_sha256':sha(report_bytes),'report_manifest_sha256':report_manifest['files'].get('inputs/'+filename),'exact_report_copy':source_bytes==report_bytes}
    if kind=='candidate':
        for slot,rows in value.get('slots',{}).items():
            for index,row in enumerate(rows):
                nid=f"slot:{slot}:{row['id']}"
                add(nid,row,filename,f'/slots/{escape(slot)}/{index}')
                candidates_by_id.setdefault(row['id'],[]).append(nid)
        for index,row in enumerate(value.get('visual_semantics',[])):
            nid='bundle:'+row['id'];add(nid,row,filename,f'/visual_semantics/{index}');raw_bundles[nid]=row
        for slot,patches in value.get('existing_slot_context_extensions',{}).items():
            for entry_id in patches:
                nid=f'slot:{slot}:{entry_id}'
                patch_refs.setdefault(nid,[]).append({'file':filename,'pointer':f'/existing_slot_context_extensions/{escape(slot)}/{escape(entry_id)}'})
    elif kind=='visual_profile':
        for index,row in enumerate(value.get('profiles',[])):
            add('profile:'+row['id'],row,filename,f'/profiles/{index}')
for nid,added in patch_refs.items():
    if nid in refs:refs[nid].extend(added)

members={};associations={};expected_edges=set()
for bid,row in raw_bundles.items():
    member_list=[]
    for entry_id in row.get('candidate_ids',[]):
        slot=row.get('candidate_slots',{}).get(entry_id)
        if slot:
            nid=f'slot:{slot}:{entry_id}'
            if nid not in raw_nodes:raise ValueError('unknown raw bundle candidate '+nid)
        else:
            possibilities=candidates_by_id.get(entry_id,[])
            if len(possibilities)!=1:raise ValueError('ambiguous raw bundle candidate '+entry_id)
            nid=possibilities[0]
        member_list.append(nid);expected_edges.add((nid,'member_of',bid))
    profile_ids=list(row.get('hard_profile_ids',[]))
    if row.get('hard_profile_id'):profile_ids.append(row['hard_profile_id'])
    if row.get('associated_profile_ids'):profile_ids.extend(row['associated_profile_ids'])
    profile_ids=sorted(set(profile_ids))
    for pid in profile_ids:
        nid='profile:'+pid
        if nid not in raw_nodes:raise ValueError('unknown raw bundle profile '+nid)
        expected_edges.add((bid,'associated_with',nid))
    members[bid]=sorted(set(member_list));associations[bid]=['profile:'+pid for pid in profile_ids]

actual_edges={(e['source'],e['type'],e['target']) for e in reported_links['edges']}
source_ref_failures=[]
checked_ids=set(plan['exposed_slot_candidate_ids'])|set(plan['profiles_to_query'])|set(plan['related_bundle_ids'])
for pid in plan['profiles_to_query']:
    for bid,pids in associations.items():
        if pid in pids:checked_ids.add(bid);checked_ids.update(members[bid])
normalize_refs=lambda rows:sorted((row['file'],row['pointer']) for row in rows)
for nid in sorted(checked_ids):
    node=reported_nodes.get(nid)
    if not node or nid not in raw_nodes or normalize_refs(node['source_refs'])!=normalize_refs(refs[nid]):
        source_ref_failures.append({'node_id':nid,'report_refs':node.get('source_refs') if node else None,'expected_refs':refs.get(nid)})
content_checks=[]
for nid in plan['exposed_slot_candidate_ids']:
    raw=raw_nodes[nid];reported=reported_nodes[nid]['record']
    for key in ('id','en','ko','concept_units','relations','affected_dimensions','affected_properties'):
        if key in raw:
            content_checks.append({'node_id':nid,'field':key,'matches':raw[key]==reported.get(key)})
content_failures=[row for row in content_checks if not row['matches']]
oracle={'independence':'Derived from registered immutable generation source files, raw candidate_ids/candidate_slots and hard_profile_id(s). Did not import maintenance graph/query/corpus helpers.','generation_id':receipt['generation_id'],'source_fingerprint':receipt['source_fingerprint'],'raw_bundle_count':len(raw_bundles),'raw_candidate_count':sum(n.startswith('slot:') for n in raw_nodes),'raw_profile_count':sum(n.startswith('profile:') for n in raw_nodes),'raw_expected_edge_count':len(expected_edges),'reported_edge_count':len(actual_edges),'missing_edges':sorted(expected_edges-actual_edges),'extra_edges':sorted(actual_edges-expected_edges),'source_references_checked_node_count':len(checked_ids),'source_reference_failures':source_ref_failures,'exposed_candidate_fields_checked':len(content_checks),'exposed_candidate_content_failures':content_failures,'source_files':file_evidence,'nodes':{nid:{'source_refs':refs[nid],'raw_source_record_sha256':sha(canon(raw_nodes[nid]))} for nid in sorted(checked_ids)},'raw_bundles':{bid:{'member_candidate_ids':members[bid],'associated_profile_ids':associations[bid],'source_refs':refs[bid]} for bid in sorted(set(plan['related_bundle_ids'])|{b for p in plan['profiles_to_query'] for b,v in associations.items() if p in v})}}
(run/'links_source_oracle.json').write_text(json.dumps(oracle,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'source_oracle_summary':{key:oracle[key] for key in ('raw_bundle_count','raw_candidate_count','raw_profile_count','raw_expected_edge_count','reported_edge_count','missing_edges','extra_edges','source_reference_failures','exposed_candidate_content_failures')}},ensure_ascii=False),flush=True)

def expected_paths(nid):
    out=[]
    if nid.startswith('slot:'):
        for bid,member_ids in members.items():
            if nid in member_ids:
                out.extend([[nid,bid,pid] for pid in associations[bid]] or [[nid,bid]])
    elif nid.startswith('profile:'):
        for bid,pids in associations.items():
            if nid in pids:
                out.extend([[cid,bid,nid] for cid in members[bid]] or [[bid,nid]])
    return sorted(out)

query_dir=run/'evidence/management-queries';query_dir.mkdir(parents=True,exist_ok=True)
cli=root/'tools/photo_data_maintenance/cli.py';python=root/'venv/bin/python'
query_nodes=plan['exposed_slot_candidate_ids']+plan['profiles_to_query']

def execute(nid):
    arg=['--candidate',nid] if nid.startswith('slot:') else ['--profile',nid.split(':',1)[1]]
    argv=[str(python),str(cli),'query','--report',str(report),*arg,'--source-root',str(root/'skill'),'--runtime-store',str(root/'runtime')]
    started=datetime.now(timezone.utc).isoformat()
    result=subprocess.run(argv,cwd=root,capture_output=True,text=True,encoding='utf-8')
    ended=datetime.now(timezone.utc).isoformat()
    label=sha(nid.encode())[:16]
    stdout=query_dir/(label+'.stdout.json');stderr=query_dir/(label+'.stderr.txt')
    stdout.write_text(result.stdout,encoding='utf-8');stderr.write_text(result.stderr,encoding='utf-8')
    value=json.loads(result.stdout) if result.returncode==0 else None
    expected=expected_paths(nid);failures=[]
    if result.returncode!=0:failures.append('CLI exit code is nonzero')
    else:
        paths=sorted(row['nodes'] for row in value['paths'])
        if paths!=expected:failures.append('Query paths differ from raw source references')
        if value['path_count']!=len(expected):failures.append('Path count differs')
        if value['generation_id']!=receipt['generation_id'] or value['source_fingerprint']!=receipt['source_fingerprint']:failures.append('Generation/source binding differs')
        if value['profile_activation']!='independent_request_evidence_only':failures.append('Profile activation boundary differs')
        for row in value['paths']:
            if row['meaning_support']!='not_inferred' or row['relation']!='via_bundle':failures.append('Association overclaims meaning')
            for identity,source_refs in row['source_refs'].items():
                if normalize_refs(source_refs)!=normalize_refs(refs[identity]):failures.append('Returned source refs differ for '+identity)
            for identity,entity_hash in row['entity_hashes'].items():
                if entity_hash!=reported_nodes[identity]['entity_sha256']:failures.append('Entity hash differs for '+identity)
    record={'node_id':nid,'argv':argv,'started_at_utc':started,'ended_at_utc':ended,'exit_code':result.returncode,'stdout_path':str(stdout),'stderr_path':str(stderr),'stdout_sha256':sha(result.stdout.encode()),'stderr_sha256':sha(result.stderr.encode()),'expected_path_count':len(expected),'actual_path_count':value.get('path_count') if value else None,'actual_freshness':value.get('freshness') if value else None,'failures':failures}
    return record,value

records=[];values={}
with ThreadPoolExecutor(max_workers=3) as pool:
    futures={pool.submit(execute,nid):nid for nid in query_nodes}
    for future in as_completed(futures):
        record,value=future.result();records.append(record);values[record['node_id']]=value
        if len(records)%20==0 or len(records)==len(query_nodes):print(json.dumps({'completed_queries':len(records),'total_queries':len(query_nodes),'query_failure_count':sum(bool(x['failures']) for x in records)}),flush=True)
records=sorted(records,key=lambda x:x['node_id'])
with (run/'management-query-commands.ndjson').open('w',encoding='utf-8') as f:
    for row in records:f.write(json.dumps(row,ensure_ascii=False)+'\n')
reverse_missing=[]
for nid in plan['exposed_slot_candidate_ids']:
    value=values[nid]
    if value:
        for path in value['paths']:
            endpoints=path['nodes']
            if len(endpoints)==3:
                reverse=values.get(endpoints[-1])
                if not reverse or endpoints not in [row['nodes'] for row in reverse['paths']]:reverse_missing.append(endpoints)
summary={'status':'PASS' if not any(row['failures'] for row in records) and not reverse_missing and not oracle['missing_edges'] and not oracle['extra_edges'] and not source_ref_failures and not content_failures and all(row['exact_report_copy'] for row in file_evidence.values()) else 'FAIL','candidate_queries':len(plan['exposed_slot_candidate_ids']),'profile_queries':len(plan['profiles_to_query']),'total_actual_cli_queries':len(records),'linked_exposed_candidates':len(plan['linked_exposed_candidate_ids']),'unlinked_exposed_candidates':len(plan['unlinked_exposed_candidate_ids']),'bidirectional_paths_checked':sum(values[nid]['path_count'] for nid in plan['exposed_slot_candidate_ids'] if values[nid]),'reverse_missing_paths':reverse_missing,'query_failures':[row for row in records if row['failures']],'pinned_report_query_freshness':'pinned_report; the separate --require-current normal query verifies the report generation against live isolated source.','source_oracle_file':str(run/'links_source_oracle.json'),'query_commands_file':str(run/'management-query-commands.ndjson'),'unlinked_does_not_imply_error':True,'meaning_support':'not_inferred','profile_activation':'independent_request_evidence_only'}
(run/'management-query-verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
