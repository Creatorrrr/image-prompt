import hashlib,json,subprocess
from pathlib import Path
R=Path('/workspace/scratch/ce8f20680f5a/image-prompt-ct073-after-3b481ca');W=Path('/workspace/scratch/ce8f20680f5a/recovery-after-reset-20261005');O=W/'ct073-latest-paired-review';B='3b481ca94fdbbeeb453e1d3ec657db0f5baf6a80';D='dc77d63ce26b9a39037b44e86554b76fe7eacf4c'
def read(p):return json.loads(p.read_bytes())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R,env={'PATH':'/usr/bin:/bin','GIT_NO_LAZY_FETCH':'1','GIT_TERMINAL_PROMPT':'0'})
def tree(rev):
 d={}
 for row in git('ls-tree','-rz',rev).split(b'\0'):
  if row:
   metadata,path=row.split(b'\t');mode,kind,bid=metadata.decode().split();d[path.decode()]=(mode,kind,bid)
 return d
checks={};seal_path=W/'ct073-latest-integration-20261006/TRANSPLANT-SEAL.json';seal=read(seal_path)
assert sha(seal_path.read_bytes())=='43afb3cb42b29fc1462017115e397067ff5d43b54c69a5010a325fd4ab08bfe8'
assert seal['base']==B and seal['reused_source']=='aaeabe17caa749215ca895c2dd17be4c1bb5efd0'
assert len(seal['files'])==len({x['path'] for x in seal['files']})==23
before,after=tree(B),tree(D)
assert git('rev-list','--parents','-1',D).decode().split()==[D,B]
assert git('rev-parse',D+'^{tree}').decode().strip()=='9d30471ee0b6717732a711402347b8d1e309bf7e'
changes={p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)}
assert changes=={x['path'] for x in seal['files']}
for row in seal['files']:
 raw=(R/row['path']).read_bytes()
 assert (len(raw),sha(raw),blob(raw))==(row['bytes'],row['sha256'],row['git_blob']),row['path']
 assert after[row['path']][2]==row['git_blob'],row['path']
checks['exact_23_overlay_matches_later_dc77_tree']=True
freeze=read(W/'fastening-before-baa-20261006/FROZEN_INPUT_HASHES.json');fp=Path(freeze['manifest_path']);fr=fp.parent
assert sha(fp.read_bytes())==freeze['manifest_sha256']=='4c1dc1bc6073a2566fae452e198008f8ddd1cf2f7cb53ca7c14e59e1a2fcfae4'
assert len(freeze['files'])==len({x['path'] for x in freeze['files']})==105
fmap={x['path']:x for x in freeze['files']}
for row in freeze['files']:
 p=Path(row['path']);assert not p.is_absolute() and '..' not in p.parts
 target=fr/p;raw=target.read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],row['path']
checks['original_frozen_input_files_verified']=105;checks['input_manifest_sha256']=freeze['manifest_sha256']
run_receipts={};command_count=0
for phase in ('before','after'):
 for stage in ('generation-adapter-v3','preflight-adapter-v3'):
  command_path=W/f'fastening-{phase}-3b481ca-20261006'/stage/'COMMANDS.json';rows=read(command_path)
  assert len(rows)==6 and {x['case'] for x in rows}=={f'case_{c}' for c in 'abcdef'}
  old_rows=read(W/f'fastening-{phase}-baa-20261006'/stage/'COMMANDS.json');oldmap={x['case']:x for x in old_rows}
  for row in rows:
   command=row['command'];assert row['cwd']==str(R) and row['returncode']==0 and row['status']=='completed' and row['blocked_attempt'] is False
   assert (row['source']==B) if phase=='before' else (row['source_parent']==B and row['staging_data_seal_sha256']==sha(seal_path.read_bytes()) and row['source_status']=='uncommitted exact DATA overlay on pinned parent')
   assert set(row['environment'])=={'PATH','PYTHONDONTWRITEBYTECODE','PYTHONPATH','RECOVERY_BLOCKED_EVENT_LOG'}
   assert row['environment']['PYTHONPATH']==str(W/'network-deny') and not Path(row['environment']['RECOVERY_BLOCKED_EVENT_LOG']).exists()
   oldcmd=oldmap[row['case']]['command'];a=command.copy();b=oldcmd.copy();a[0]=b[0]='PYTHON'
   if stage.startswith('generation'):
    assert command[1]=='skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py'
    assert command[command.index('--seed')+1]=='0'
    a[a.index('--output-file')+1]=b[b.index('--output-file')+1]='OUTPUT'
    p=Path(row['pack_path']);assert p==Path(command[command.index('--output-file')+1]) and sha(p.read_bytes())==row['pack_sha256']
    flags=('--authorial-core-json','--request-envelope-json','--creative-controls-json','--embodiment-review-json')
   else:
    assert command[1]=='skills/photo-prompt-image-generator/scripts/validate_precore_feature_selection.py'
    flags=('--authorial-core','--request-envelope','--embodiment-review','--selection')
   assert a==b,(phase,stage,row['case'])
   for flag in flags:
    assert command.count(flag)==1
    p=Path(command[command.index(flag)+1]);relative=str(p.relative_to(fr));assert relative in fmap and relative.startswith(row['case']+'/')
   assert (command_path.parent/(row['case']+'.stderr')).read_bytes()==b''
   command_count+=1
  run_receipts[f'{phase}/{stage}']=sha(command_path.read_bytes())
checks['successful_current_command_receipts_verified']=command_count;checks['commands_match_prior_excluding_python_and_output_paths']=True;checks['receipt_sha256']=run_receipts
receipt_path=W/'ct073-latest-actual-boundary/receipt.json';receipt=read(receipt_path);command=receipt['command'];raw=(receipt_path.parent/'pack.json').read_bytes()
assert receipt['source_parent']==B and receipt['overlay_seal_sha256']==sha(seal_path.read_bytes()) and receipt['returncode']==0
assert len(raw)==213313 and sha(raw)==receipt['pack_sha256']=='0b028da1680fd5cdb042b5e6eb711d33484c8c1276220e09b01239163219d037'
assert raw==(W/'ct073-actual-after-boundary-20261006/pack.json').read_bytes()
base=json.loads(git('show',B+':skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v24.json'))
a=base['command'].copy();b=command.copy();a[0]=b[0]='PYTHON';a[a.index('--output-file')+1]=b[b.index('--output-file')+1]='OUTPUT';assert a==b
for path,h in base['frozen_inputs'].items():assert sha((R/path).read_bytes())==h
assert not Path(receipt['environment']['RECOVERY_BLOCKED_EVENT_LOG']).exists()
checks['actual_frozen_boundary_generator_pack']={'bytes':len(raw),'sha256':sha(raw),'exact_previous_ct073_bytes':True,'command_matches_official_v24_fixture':True,'is_v25_validator_run':False}
checks['provider_calls_evidence']={'sealed_overlay':seal['provider_calls'],'embedding_attempts':seal['embedding_attempts'],'generation_receipt':receipt['provider_calls'],'network_guard_logs_present':False,'scope':'Reported zero calls; verified sanitized commands, unchanged real cache payload bindings, and no blocked-event logs. This review made no network/provider call.'}
report={'result':'PASS','source_parent':B,'later_data_source':D,'overlay_seal_sha256':sha(seal_path.read_bytes()),'checks':checks,'review_actions':{'production_edits':0,'tests_run':0,'provider_calls':0,'network_calls':0,'ref_changes':0}}
(O/'commands-inputs-source.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
