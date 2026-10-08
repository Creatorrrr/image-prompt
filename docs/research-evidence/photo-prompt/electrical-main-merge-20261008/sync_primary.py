"""Fast-forward primary, restore independent local edits, rebuild exact indexes."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone

PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
MERGE=Path('docs/research-evidence/photo-prompt/electrical-main-merge-20261008')
SKILL=Path('skills/photo-prompt-image-generator')

def git(*args): return subprocess.check_output(['git',*args],cwd=PRIMARY)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(name,data): (PRIMARY/MERGE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def main():
    p=argparse.ArgumentParser();p.add_argument('--target',required=True);p.add_argument('--worktree',type=Path,required=True);a=p.parse_args()
    target=git('rev-parse',a.target).decode().strip();base=git('rev-parse','HEAD').decode().strip()
    assert git('symbolic-ref','--short','HEAD').decode().strip()=='main'
    subprocess.run(['git','merge-base','--is-ancestor',base,target],cwd=PRIMARY,check=True)
    assert not git('diff','--cached','--name-only').strip(),'Concurrent staged work requires separate index preservation'
    incoming=set(git('diff','--name-only',base,target).decode().splitlines())
    before={}
    for row in git('status','--porcelain=v1','-z','-uall').split(b'\0'):
        if not row:continue
        name=row[3:].decode();path=PRIMARY/name
        if not path.is_file():continue
        assert not path.is_symlink(),name
        before[name]={'status':row[:2].decode(),'sha256':sha(path),'mode':path.stat().st_mode&0o7777}
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup=PRIMARY/'.codex-artifacts'/('electrical-primary-sync-'+stamp);backup.mkdir(parents=True)
    tracked={name for name,row in before.items() if row['status']!='??'}
    overlap=tracked&incoming;collisions=(set(before)-tracked)&incoming
    derived={(SKILL/'assets'/name).as_posix() for name in ('photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json')}
    manifest=(SKILL/'assets/photo_prompt_source_manifest.json').as_posix()
    restore={};adopted=[]
    for name in sorted(overlap|collisions):
        path=PRIMARY/name;destination=backup/name;destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,destination)
        raw=path.read_bytes();new=git('show',target+':'+name)
        if raw==new:adopted.append(name);continue
        if name in derived:continue
        if name==manifest:
            local=json.loads(raw);remote=json.loads(new);local_rows={row['file']:row for row in local['sources']}
            assert len(local_rows)==len(local['sources'])
            rows=list(local['sources'])
            for row in remote['sources']:
                if row['file'] in local_rows:
                    assert {k:v for k,v in row.items() if k!='load_order'}=={k:v for k,v in local_rows[row['file']].items() if k!='load_order'},row['file']
                else:
                    appended=dict(row,load_order=max(x['load_order'] for x in rows if x['kind']==row['kind'])+1)
                    rows.append(appended);local_rows[row['file']]=appended
            restore[name]=raw if rows==local['sources'] else (json.dumps({**remote,'sources':rows},ensure_ascii=False,indent=2)+'\n').encode()
        elif name in collisions:
            raise AssertionError('Different untracked collision requires semantic review: '+name)
        else:
            ancestor=backup/'.ancestor';ancestor.write_bytes(git('show',base+':'+name))
            theirs=backup/'.incoming';theirs.write_bytes(new)
            result=subprocess.run(['git','merge-file','-p',str(path),str(ancestor),str(theirs)],capture_output=True)
            assert result.returncode==0,('Semantic overlap requires review',name)
            restore[name]=result.stdout
    for name in derived:
        path=PRIMARY/name;destination=backup/name
        if not destination.exists():destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,destination)
        for row in json.loads(path.read_text())['shards']:
            src=path.parent/row['path'];dst=backup/src.relative_to(PRIMARY);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
    save('PRIMARY-PRESYNC.json',{'base':base,'target':target,'backup':str(backup),'dirty_files':before,
                              'incoming_paths':sorted(incoming),'tracked_overlap':sorted(overlap),
                              'untracked_collisions':sorted(collisions),'exact_adoptions':adopted,
                              'local_restore_paths':sorted(restore)})
    sys.path.insert(0,str(PRIMARY/SKILL/'scripts'))
    from photo_runtime_sources import source_update
    done=False
    with source_update(PRIMARY/SKILL):
        try:
            for name in overlap:(PRIMARY/name).write_bytes(git('show',base+':'+name))
            for name in collisions:
                dst=backup/'untracked-collisions'/name;dst.parent.mkdir(parents=True,exist_ok=True);os.replace(PRIMARY/name,dst)
            subprocess.run(['git','merge','--ff-only',target],cwd=PRIMARY,check=True,stdout=subprocess.DEVNULL)
            done=True
            for name,raw in restore.items():(PRIMARY/name).write_bytes(raw)
            for name,row in before.items():(PRIMARY/name).chmod(row['mode'])
        finally:
            if not done:
                for name in overlap:shutil.copy2(backup/name,PRIMARY/name)
                for name in collisions:
                    old=backup/'untracked-collisions'/name
                    if old.exists():os.replace(old,PRIMARY/name)
    command=[str(PRIMARY/'.venv/bin/python'),str(PRIMARY/MERGE/'rebuild_indexes.py'),
             '--cache-root',str(backup/SKILL),'--cache-root',str(a.worktree/SKILL),
             '--report-name','PRIMARY-INDEX-REBUILD.json']
    with (PRIMARY/MERGE/'primary-index-rebuild.log').open('w') as output:
        result=subprocess.run(command,cwd=PRIMARY,stdout=output,stderr=subprocess.STDOUT)
    assert result.returncode==0,'Rebuild failed; authored files and vectors retained in preservation backup'
    changed=[];missing=[];retained=0
    for name,row in before.items():
        path=PRIMARY/name
        if not path.is_file():missing.append(name);continue
        if name not in derived:
            if sha(path)!=row['sha256']:changed.append(name)
            else:retained+=1
    assert not changed and not missing,(changed,missing)
    final={'status':'PASS','base':base,'primary_head':git('rev-parse','HEAD').decode().strip(),'target':target,
           'dirty_files_observed_before':len(before),'non_derived_dirty_files_byte_identical':retained,
           'changed_non_derived':changed,'missing':missing,'exact_adoptions':len(adopted),
           'local_manifest_order_and_unpublished_sources_preserved':True,
           'derived_indexes_rebuilt':True,'backup':str(backup),'primary_runtime':json.loads((PRIMARY/MERGE/'PRIMARY-INDEX-REBUILD.json').read_text())['runtime']}
    save('PRIMARY-SYNC-VERIFICATION.json',final);print(json.dumps(final,ensure_ascii=False))


if __name__=='__main__':main()
