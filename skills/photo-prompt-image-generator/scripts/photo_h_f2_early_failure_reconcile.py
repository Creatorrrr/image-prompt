"""Close ONLY the three independently observed 2026-11-07 pre-search failures.

This is an offline evidence checker, not a search retry or a general recovery
mechanism. The pinned observations are local copies of Codex command records;
they are not cryptographically signed by Codex. See the accompanying note.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path

GEN = '05eeb9e7620231c6911d559ec159f86189bf0fc90ec198cd41258f718ea0d604'
NATIVE = '7bf18c2e1c9c248095c3dcd8c5dccf8ad6ccfb5b25c6b7692819109a1242b4f1'
PROFILES = {
 '7c2ac14c093d43e1a152e7a87b5733c4': ('arm1/run-v2', '53600e7e31fab97e94294f3a96f7dcfbfc54bf17fe26ff3557b7b18826bc4e5d', 'exec-8f17f008-bf1e-4a56-b44a-9fc7b08bfe5e', 5, {13352}, None),
 '84208705e4a94d59b287317be30536e9': ('arm2/run', '4e92aa786518121f44c0a27c8cbb23505b76c83e63af095195e6ae5b827aa9ea', 'exec-a5996461-fbcd-45bc-a5c5-94ac7868ed2a', 8, {12059, 12963}, None),
 'e8bce063283342839227e379adb135da': ('arm3/run', 'ec98a070398c8d7fa6229387312a2d676c5b8e65b6a399a0d7302c53d026b898', 'exec-0c624137-a62d-49bc-abb1-88bca9ae87ab', 5, {12915, 15548}, '85a54b22492d36ce290b2182c212a31fd9147865a2eefc8a0edf025d4613579a'),
}
ORIGINAL_BINDINGS = {
 '7c2ac14c093d43e1a152e7a87b5733c4': ('d19f42b38a5d077864d9fbf5a2a8c087a6616ab499edcab011d3ccbffa0b7ee6','78e9045be1a4dbb9af827a5a5a05a34eae3559731b61163d29cd8d3c749e053d'),
 '84208705e4a94d59b287317be30536e9': ('add075b94d8e5886cb58f1100c9d0862c7ee27d5088d4785131e964421b99948','4129902f6a1332ea33e0e50faacbc688cca035383fd8f333f2816d68982f225e'),
 'e8bce063283342839227e379adb135da': ('c2b59145516a060a091a464c37b8d2a60ab05e19bbffe30d34c4399222835e56','fc6e6e84785447e489c5c64e238000ef963bcb4a3375f64a02984b471292dfbc'),
}
CODE = {'photo_h_f2_workflow.py':'bbf133596a002f353fa7fa73625a428bf0f18185aeb67ad190fb99f23be99fe2',
        'photo_h_f2_encoder.py':'7e9c80d40ec21faa9d9d24e46c74bec1a94a83e3e1920fb9baea4adbbd050b22',
        'photo_local_embedding.py':'d105e323587a65d72a8b413ff62ce628a198161d8a97dfdcbc621acbceb9583e'}

def sha(raw):
 return hashlib.sha256(raw).hexdigest()

def digest(value):
 return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',', ':'),allow_nan=False).encode())

def require(condition, reason):
 if not condition: raise ValueError(reason)

def read(path):
 raw=path.read_bytes()
 return json.loads(raw),sha(raw)

def verify_observation(path, expected_hash, expected_id, run, *, resume=False):
 obs,h=read(path)
 require(h==expected_hash,'observation hash changed')
 e=obs.get('execution',{}); output=e.get('output',{})
 require(obs.get('schema')=='codex-command-observation/v1' and obs.get('source_tool')=='mcp__codex_app__read_thread' and obs.get('retrieved_with_outputs') is True,'untrusted observation')
 require(e.get('id')==expected_id and e.get('type')=='commandExecution' and e.get('status')=='failed' and e.get('exitCode')==(130 if resume else 2),'unexpected command result')
 require(output.get('truncated') is False and isinstance(output.get('text'),str),'incomplete command output')
 require(('resume' if resume else 'retrieve')+' --run '+str(run) in e.get('command',''),'command run mismatch')
 text=output['text']
 if resume:
  require('KeyboardInterrupt' in text and 'provider.from_receipt' in text,'resume interruption evidence missing')
 else:
  require('photo_local_embedding.py' in text and 'runner=ModelRunner(runtime_lock())' in text and 'ValueError: unsafe local model package' in text,'pre-search worker failure missing')
 return h

def no_live_pid(pid):
 try: os.kill(pid,0)
 except ProcessLookupError: return True
 except PermissionError: return False
 return False

def verify(root, run):
 root=Path(root).resolve(); run=Path(run).resolve(); tests=root/'generated/magical-girl-tests'
 state,sh=read(run/'workflow.json'); rid=state.get('run_id');require(rid in PROFILES,'unsupported run')
 rel,obs_sha,obs_id,total,pids,resume_sha=PROFILES[rid]
 require(run==(tests/rel).resolve(),'run path changed')
 require(state.get('phase')=='slot_intents_authored' and not state.get('operations') and not ({'pack','h_f2_material','h_f2_receipt'} & set(state.get('artifacts',{}))),'run already issued material or invoked image')
 for artifact in state.get('artifacts',{}).values():
  path=Path(artifact['path']).resolve()
  require(path.is_relative_to(run) and path.is_file() and sha(path.read_bytes())==artifact.get('sha256'),'bound run artifact changed')
 stage=run/'.staging/h-f2';j,jh=read(stage/'transaction.json');pre,ph=read(stage/'preflight.json')
 require((jh,ph)==ORIGINAL_BINDINGS[rid],'original transaction or preflight changed')
 require(j.get('state')=='started' and j.get('generation_id')==GEN and pre.get('generation_id')==GEN and pre.get('run_id')==rid,'transaction binding mismatch')
 require(j.get('preflight_sha256')==digest(pre) and j.get('query_set_sha256')==pre.get('query_set_sha256'),'preflight or query binding mismatch')
 require(pre.get('validation_receipt',{}).get('generation_id')==NATIVE,'native generation mismatch')
 require(not (stage/'material.json').exists() and not list(stage.rglob('*.npz')),'material or raw scores exist')
 require({x.name for x in stage.iterdir()}=={'transaction.json','preflight.json','progress.json','progress-events.jsonl'},'unexpected staging artifact')
 events_raw=(stage/'progress-events.jsonl').read_bytes();events=[json.loads(x) for x in events_raw.splitlines()]
 require(events and {x.get('pid') for x in events}==pids,'unexpected process history')
 require(all(x.get('completed_queries')==0 and x.get('total_queries') in {0,total} and x.get('stage') in {'initializing','embedding','failed'} for x in events),'search activity cannot be excluded')
 embedding=[x for x in events if x.get('stage')=='embedding']
 require(len(embedding)==1 and any(x.get('pid')==embedding[0]['pid'] and x.get('stage')=='failed' and x.get('status')=='failed' for x in events) and all(no_live_pid(pid) for pid in pids),'failure phase or process termination not verified')
 progress,progress_h=read(stage/'progress.json');require(progress=={k:v for k,v in events[-1].items() if k!='elapsed_seconds'},'progress disagrees with event log')
 obs_path=run.parent/'codex-retrieve-observation.json'
 oh=verify_observation(obs_path,obs_sha,obs_id,Path('generated/magical-girl-tests')/rel)
 resume_h=None
 if resume_sha:
  resume_h=verify_observation(run.parent/'codex-resume-observation.json',resume_sha,'exec-0aaf9aca-6683-4d88-a264-9256d253f1cb',Path('generated/magical-girl-tests')/rel,resume=True)
 native=Path.home()/'.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations'/NATIVE/'scripts'
 skill=root/'generated/magical-girl-hf2-20261107/test-skill/scripts'
 for name,expected in CODE.items():
  path=(skill if name=='photo_local_embedding.py' else native)/name
  require(sha(path.read_bytes())==expected,'bound runtime code changed')
 return {'schema':'photo-h-f2-early-failure-reconciliation/v1','run_id':rid,'run':str(run),'outcome':'closed_before_index_search',
         'generation_id':GEN,'native_generation_id':NATIVE,'query_set_sha256':j['query_set_sha256'],
         'total_queries':total,'completed_queries':0,'material_issued':False,'managed_image_operations':0,
         'evidence_sha256':{'workflow':sh,'transaction':jh,'preflight':ph,'progress':progress_h,'events':sha(events_raw),'retrieve_observation':oh,'resume_observation':resume_h,'runtime_code':CODE},
         'limits':'Pinned local Codex observations are unsigned; closure is bounded to the observed executions and snapshot. This receipt is not search material or native approval.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--run',type=Path,required=True);p.add_argument('--receipt',type=Path,required=True);a=p.parse_args()
 run=a.run.resolve();destination=a.receipt.resolve()
 require(not destination.is_relative_to(run),'receipt must be outside the original run')
 require(destination.parent.is_dir(),'receipt parent must already exist')
 with (run/'.LOCK').open('rb') as lock:
  fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  result=verify(a.root,run);raw=(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
  if destination.exists(): require(destination.read_bytes()==raw,'existing receipt differs')
  else:
   with destination.open('xb') as out: out.write(raw);out.flush();os.fsync(out.fileno())
  fcntl.flock(lock,fcntl.LOCK_UN)
 print(json.dumps({'status':'reconciled','receipt':str(destination),'sha256':sha(raw)}))

if __name__=='__main__': main()
