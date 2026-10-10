"""Ordinary main fast-forward with exact restoration of intersecting local work."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import time
import sys

ROOT=Path('/Users/chasoik/Projects/image-prompt')
PUB=ROOT/'docs/research-evidence/photo-prompt/wardrobe-keyword-main-publication-20261010'
HOLDING=Path('/Users/chasoik/.codex/holding/wardrobe-main-publication-20261010')
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
from photo_runtime_sources import source_update, capture_sources
parser=argparse.ArgumentParser()
parser.add_argument('--commit',required=True)
parser.add_argument('--execute',action='store_true')
args=parser.parse_args()


def git(*arguments):
    return subprocess.check_output(['git',*arguments],cwd=ROOT).decode().strip()


def inspect(path):
    information=path.lstat()
    if path.is_symlink():
        body=str(path.readlink()).encode(); kind='symlink'
    elif path.is_file():
        body=path.read_bytes(); kind='file'
    else:
        raise ValueError('Unexpected existing path kind: '+str(path))
    return {'kind':kind,'mode':stat.S_IMODE(information.st_mode),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}


before=json.loads((PUB/'PRIMARY-BEFORE.json').read_text())
assert git('branch','--show-current')=='main'
assert git('rev-parse','HEAD')==before['head'],'primary HEAD changed since snapshot'
assert not git('diff','--cached','--name-only'),'preexisting staged work must remain isolated'
subprocess.run(['git','merge-base','--is-ancestor',before['head'],args.commit],cwd=ROOT,check=True)
changed=[value.decode() for value in subprocess.check_output(['git','diff','--name-only','-z',before['head'],args.commit],cwd=ROOT).split(b'\0') if value]
tracked={value.decode() for value in subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).split(b'\0') if value}
protected={row['path']:row for row in before['files']}
dirty={value.decode() for value in subprocess.check_output(['git','diff','--name-only','-z'],cwd=ROOT).split(b'\0') if value}
held=[]
for relative in changed:
    path=ROOT/relative
    if not path.exists() and not path.is_symlink(): continue
    if relative not in tracked or relative in dirty:
        row={'path':relative,**inspect(path),'tracked':relative in tracked}
        if relative in protected:
            assert all(row[key]==protected[relative][key] for key in ['kind','mode','bytes','sha256']),relative
        else:
            assert relative.startswith(str(PUB.relative_to(ROOT))+'/'),'unreviewed new local collision: '+relative
        held.append(row)
plan={'schema_version':'wardrobe-publication-main-advance/v1','base_commit':before['head'],'target_commit':args.commit,
      'holding':str(HOLDING),'protected_files':held,'held_count':len(held),'held_bytes':sum(row['bytes'] for row in held),
      'ordinary_fast_forward':True,'force_reset_stash_clean':False,'execute_requested':args.execute,
      'cooperative_source_update_barrier':True}
if not args.execute:
    (PUB/'PRIMARY-ADVANCE-PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'PLANNED','held_count':len(held),'held_bytes':plan['held_bytes']}))
    raise SystemExit(0)
assert not HOLDING.exists(),'holding already exists; inspect recovery before retry'
HOLDING.mkdir(parents=True)
(HOLDING/'RECOVERY-PLAN.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
moved=[]; merge_code=None; merge_output=''
before_source,_=capture_sources(SKILL)
with source_update(SKILL):
    try:
        for row in held:
            source=ROOT/row['path']; backup=HOLDING/'files'/row['path']; backup.parent.mkdir(parents=True,exist_ok=True)
            os.replace(source,backup)
            moved.append(row)
            assert all(inspect(backup)[key]==row[key] for key in ['kind','mode','bytes','sha256'])
        restored_paths=[row['path'] for row in held if row['tracked']]
        if restored_paths:
            subprocess.run(['git','restore','--source=HEAD','--worktree','--pathspec-from-file=-','--pathspec-file-nul'],
                cwd=ROOT,input=b'\0'.join(path.encode() for path in restored_paths)+b'\0',check=True)
        completed=subprocess.run(['git','merge','--ff-only','--no-edit',args.commit],cwd=ROOT,capture_output=True,text=True)
        merge_code=completed.returncode; merge_output=completed.stdout+completed.stderr
    finally:
        for row in moved:
            source=HOLDING/'files'/row['path']; destination=ROOT/row['path']; destination.parent.mkdir(parents=True,exist_ok=True)
            if destination.is_symlink(): destination.unlink()
            shutil.copy2(source,destination,follow_symlinks=False)
            assert all(inspect(destination)[key]==row[key] for key in ['kind','mode','bytes','sha256']),row['path']
        after_source,_=capture_sources(SKILL)
        assert after_source==before_source,'original runtime source changed during main integration'
        plan['original_runtime_source_before_after_exact']=True
        plan.update({'merge_exit_code':merge_code,'merge_output':merge_output,'restored_count':len(moved),
                     'current_main':git('rev-parse','main'),'index_staged_paths':git('diff','--cached','--name-only'),
                     'status':'PASS' if merge_code==0 and git('rev-parse','main')==args.commit else 'FAIL'})
        (PUB/'PRIMARY-ADVANCE.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
        (HOLDING/'RECOVERY-RESULT.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':plan['status'],'current_main':plan['current_main'],'restored_count':len(moved)}),flush=True)
if plan['status']!='PASS':
    print(merge_output,flush=True)
    raise SystemExit(1)
assert not plan['index_staged_paths']
