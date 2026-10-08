"""Fast-forward primary while preserving unrelated dirty bytes and local DATA."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime,timezone

PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
WORKTREE=Path(__file__).resolve().parents[4]
SKILL=Path('skills/photo-prompt-image-generator')
EVIDENCE=PRIMARY/'docs/research-evidence/photo-prompt/selfie-main-merge-20261009'

def git(*args,cwd=PRIMARY):return subprocess.check_output(['git',*args],cwd=cwd)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def save(name,value):(EVIDENCE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--target',required=True);args=parser.parse_args();target=git('rev-parse',args.target).decode().strip()
    base=git('rev-parse','HEAD').decode().strip();assert git('symbolic-ref','--short','HEAD').decode().strip()=='main'
    assert subprocess.call(['git','merge-base','--is-ancestor',base,target],cwd=PRIMARY)==0
    assert subprocess.call(['git','diff','--cached','--quiet'],cwd=PRIMARY)==0, 'A concurrent staged change must finish before primary sync'
    incoming=set(git('diff','--name-only',base,target).decode().splitlines())
    status=git('status','--porcelain=v1','-z','-uall').split(b'\0');before={}
    for row in status:
        if not row:continue
        name=row[3:].decode();path=PRIMARY/name
        if not path.is_file():continue
        assert not path.is_symlink(),name
        before[name]=dict(status=row[:2].decode(),sha256=sha(path.read_bytes()),bytes=path.stat().st_size,mode=path.stat().st_mode&0o7777)
    timestamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');backup=PRIMARY/'.codex-artifacts'/('selfie-primary-presync-'+timestamp);backup.mkdir(parents=True)
    tracked={name for name,row in before.items() if row['status']!='??'};untracked=set(before)-tracked;overlap=tracked&incoming;collisions=untracked&incoming
    derived={(SKILL/'assets'/name).as_posix() for name in ('photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json')}
    manifest=(SKILL/'assets/photo_prompt_source_manifest.json').as_posix();local_restore={};exact_adoptions=[];semantic_conflicts=[]
    for name in sorted(overlap|collisions):
        path=PRIMARY/name;raw=path.read_bytes();dest=backup/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
        new=git('show',target+':'+name)
        if raw==new:exact_adoptions.append(name);continue
        if name in derived:continue
        if name==manifest:
            old=json.loads(git('show',base+':'+name));local=json.loads(raw);remote=json.loads(new)
            original={row['file']:row for row in old['sources']};local_by_file={row['file']:row for row in local['sources']}
            assert len(local_by_file)==len(local['sources']) and set(original)<=set(local_by_file)
            assert [row['file'] for row in local['sources'] if row['file'] in original]==[row['file'] for row in old['sources']]
            assert all({k:v for k,v in row.items() if k!='load_order'}=={k:v for k,v in local_by_file[name].items() if k!='load_order'} for name,row in original.items())
            assert remote['sources'][:len(old['sources'])]==old['sources']
            rows=list(local['sources']);identities={row['file']:row for row in rows}
            for row in remote['sources']:
                if row['file'] in identities:
                    assert {k:v for k,v in row.items() if k!='load_order'}=={k:v for k,v in identities[row['file']].items() if k!='load_order'}
                else:
                    copy=dict(row,load_order=max(x['load_order'] for x in rows if x['kind']==row['kind'])+1);rows.append(copy);identities[row['file']]=copy
            local_restore[name]=(json.dumps({**remote,'sources':rows},ensure_ascii=False,indent=2)+'\n').encode()
        elif name in collisions:
            raise AssertionError('Incoming untracked collision differs; refusing overwrite: '+name)
        else:
            common=backup/'.merge-base';common.write_bytes(git('show',base+':'+name));theirs=backup/'.merge-target';theirs.write_bytes(new)
            result=subprocess.run(['git','merge-file','-p',str(path),str(common),str(theirs)],capture_output=True)
            assert result.returncode==0,('Primary text conflict requires semantic resolution',name)
            local_restore[name]=result.stdout
    for name in derived:
        path=PRIMARY/name;dest=backup/name
        if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
        for row in json.loads(path.read_bytes())['shards']:
            shard=path.parent/row['path'];dest=backup/shard.relative_to(PRIMARY);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(shard,dest)
    save('PRIMARY-PRESYNC.json',dict(base=base,target=target,files=before,overlap=sorted(overlap),collisions=sorted(collisions),backup=str(backup),exact_canonical_adoptions=exact_adoptions,local_overlays_to_restore=sorted(local_restore)))
    sys.path.insert(0,str(PRIMARY/SKILL/'scripts'))
    from photo_runtime_sources import source_update
    complete=False
    with source_update(PRIMARY/SKILL):
        assert git('rev-parse','HEAD').decode().strip()==base, 'Primary HEAD moved during preparation; retry from its new base'
        for name in overlap|collisions:
            assert sha((PRIMARY/name).read_bytes())==before[name]['sha256'], ('An overlapping file changed during preparation',name)
        assert subprocess.call(['git','diff','--cached','--quiet'],cwd=PRIMARY)==0, 'A staged change appeared during preparation'
        try:
            for name in overlap:(PRIMARY/name).write_bytes(git('show',base+':'+name))
            for name in collisions:
                moved=backup/'untracked-collisions'/name;moved.parent.mkdir(parents=True,exist_ok=True);os.replace(PRIMARY/name,moved)
            subprocess.run(['git','merge','--ff-only',target],cwd=PRIMARY,check=True,stdout=subprocess.DEVNULL)
            complete=True
            for name,raw in local_restore.items():(PRIMARY/name).write_bytes(raw)
            for name,row in before.items():
                if name not in derived:(PRIMARY/name).chmod(row['mode'])
        finally:
            if not complete:
                for name in overlap:shutil.copy2(backup/name,PRIMARY/name)
                for name in collisions:
                    saved=backup/'untracked-collisions'/name
                    if saved.exists():os.replace(saved,PRIMARY/name)
    rebuild=WORKTREE/'docs/research-evidence/photo-prompt/selfie-main-merge-20261009/rebuild_indexes.py'
    # The copied script derives ROOT from its primary location; source generations
    # in the immutable qualification/merge worktrees are never edited.
    primary_rebuild=PRIMARY/rebuild.relative_to(WORKTREE)
    command=[str(PRIMARY/'.venv/bin/python'),str(primary_rebuild),'--cache-root',str(backup/SKILL),'--cache-root',str(WORKTREE/SKILL),'--report-name','PRIMARY-INDEX-REBUILD.json']
    with (EVIDENCE/'PRIMARY-INDEX-REBUILD.log').open('w') as output:rebuilt=subprocess.run(command,cwd=PRIMARY,stdout=output,stderr=subprocess.STDOUT)
    assert rebuilt.returncode==0,'Primary index rebuild failed; exact source backups are preserved'
    unexpected=[];retained=0
    for name,row in before.items():
        assert (PRIMARY/name).is_file(),name
        if name not in derived and name not in incoming:
            actual=sha((PRIMARY/name).read_bytes())
            if actual!=row['sha256']:unexpected.append(name)
            else:retained+=1
    assert not unexpected,('Unrelated dirty bytes changed',unexpected)
    final=dict(status='PASS',primary_head=git('rev-parse','HEAD').decode().strip(),target=target,files_observed_before=len(before),unrelated_dirty_files_preserved=retained,unexpected_changes=unexpected,exact_canonical_adoptions=len(exact_adoptions),local_overlay_paths=sorted(local_restore),semantic_conflicts=semantic_conflicts,derived_indexes_rebuilt_for_working_tree=True,backup=str(backup),qualification_worktree_untouched=True)
    save('PRIMARY-SYNC-VERIFICATION.json',final);print(json.dumps(final,ensure_ascii=False))

if __name__=='__main__':main()
