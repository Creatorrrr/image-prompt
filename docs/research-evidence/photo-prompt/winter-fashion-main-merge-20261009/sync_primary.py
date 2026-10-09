"""Advance main by fast-forward while preserving all existing dirty/untracked bytes."""
from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess,sys

PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
WORK=Path('/Users/chasoik/.codex/worktrees/winter-fashion-main-merge-20261009/image-prompt')
OUT=PRIMARY/'docs/research-evidence/photo-prompt/winter-fashion-main-merge-20261009'

def git(*args,env=None):return subprocess.check_output(['git','-c','core.fsmonitor=false',*args],cwd=PRIMARY,env=env)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def observe(p):
    if p.is_symlink():return {'type':'symlink','target':os.readlink(p)}
    if not p.exists():return {'type':'deleted'}
    return {'type':'file','sha256':sha(p),'mode':stat.S_IMODE(p.stat().st_mode),'size':p.stat().st_size}

def main():
    target=git('rev-parse',sys.argv[1]).decode().strip()
    before=json.loads((OUT/'PRIMARY-BEFORE.json').read_text())
    old=git('rev-parse','HEAD').decode().strip()
    assert old==before['head'],'Primary HEAD advanced concurrently; refresh and integrate before syncing'
    assert git('symbolic-ref','--short','HEAD').decode().strip()=='main'
    assert subprocess.run(['git','diff','--cached','--quiet'],cwd=PRIMARY).returncode==0,'Concurrent staged changes must remain untouched'
    assert subprocess.run(['git','merge-base','--is-ancestor',old,target],cwd=PRIMARY).returncode==0
    drift=[name for name,row in before['files'].items() if observe(PRIMARY/name)!=row]
    assert not drift,('Concurrent file drift requires refresh, never restoration',drift)
    updated=[];protected=[]
    incoming=[raw.decode() for raw in git('diff','--name-only','-z',old,target).split(b'\0') if raw]
    for name in incoming:
        src=WORK/name;dst=PRIMARY/name
        if name in before['files']:
            protected.append(name);continue
        if not src.exists():raise RuntimeError('Unexpected deletion in publication: '+name)
        if dst.exists():
            if sha(src)==sha(dst):continue
            old_blob=subprocess.run(['git','show',old+':'+name],cwd=PRIMARY,capture_output=True)
            assert old_blob.returncode==0 and hashlib.sha256(old_blob.stdout).hexdigest()==sha(dst),('Concurrent new file collision',name)
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);updated.append(name)
    index=Path(git('rev-parse','--git-path','index').decode().strip())
    if not index.is_absolute():index=PRIMARY/index
    old_index=index.read_bytes()
    temporary=index.with_name('winter-fashion-fast-forward.index')
    assert not temporary.exists()
    env={**os.environ,'GIT_INDEX_FILE':str(temporary)}
    subprocess.run(['git','read-tree',target],cwd=PRIMARY,env=env,check=True)
    lock=index.with_name(index.name+'.lock')
    fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
    ref_advanced=False
    try:
        assert index.read_bytes()==old_index,'Concurrent Git index mutation detected'
        assert git('rev-parse','HEAD').decode().strip()==old,'Concurrent main update detected'
        with os.fdopen(fd,'wb') as stream:
            stream.write(temporary.read_bytes());stream.flush();os.fsync(stream.fileno())
        subprocess.run(['git','update-ref','-m','merge winter fashion: Fast-forward preserving dirty work','refs/heads/main',target,old],cwd=PRIMARY,check=True)
        ref_advanced=True
        os.replace(lock,index)
    finally:
        if not ref_advanced and lock.exists():lock.unlink()
        if temporary.exists():temporary.unlink()
    assert git('rev-parse','HEAD').decode().strip()==target
    assert not git('diff','--cached','--name-only').strip()
    after_drift=[name for name,row in before['files'].items() if observe(PRIMARY/name)!=row]
    assert not after_drift,('Protected file drift after synchronization',after_drift)
    result={'status':'pass','previous_main':old,'main':target,'merge_kind':'fast_forward','separate_merge_commit':False,'preserved_byte_mode_paths':len(before['files']),'unexpected_protected_changes':after_drift,'protected_incoming_paths':protected,'new_committed_files_copied':updated,'git_index_replaced_under_exclusive_lock':True,'force_push_reset_stash_clean_used':False}
    (OUT/'PRIMARY-SYNC-VERIFICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},ensure_ascii=False))

if __name__=='__main__':main()
