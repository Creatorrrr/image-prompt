"""Advance primary refs/index while retaining all prior dirty/untracked bytes."""
from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess,sys,tempfile
PRIMARY=Path('/Users/chasoik/Projects/image-prompt');ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent

def git(*args,cwd=PRIMARY,env=None):return subprocess.check_output(['git',*args],cwd=cwd,env=env)
def digest(p):
    if p.is_symlink():return hashlib.sha256(p.readlink().as_posix().encode()).hexdigest()
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def main():
    before=json.loads((HERE/'PRIMARY-BEFORE.json').read_text());commit=sys.argv[1]
    assert git('rev-parse','HEAD').decode().strip()==before['head'],'Primary HEAD changed concurrently'
    assert git('write-tree').decode().strip()==before['index_tree'],'Primary index changed concurrently'
    original={row['path']:row for row in before['files']};drift=[]
    for name,row in original.items():
        path=PRIMARY/name
        exists=path.exists() or path.is_symlink()
        if row['kind']=='missing':ok=not exists
        else:ok=exists and digest(path)==row['sha256'] and stat.S_IMODE(path.lstat().st_mode)==row['mode']
        if not ok:drift.append(name)
    assert not drift,('Concurrent working-file changes; preserve and review before sync',drift)
    assert subprocess.run(['git','merge-base','--is-ancestor',before['head'],commit],cwd=PRIMARY).returncode==0
    # Current snapshot members remain exactly as they were. New committed files
    # are copied only when absent, or when the existing file equals old HEAD.
    changed=git('diff','--name-only','-z',before['head'],commit,cwd=ROOT).split(b'\0');updated=[];kept=[]
    for raw in changed:
        if not raw:continue
        name=raw.decode();src=ROOT/name;dst=PRIMARY/name
        if name in original:kept.append(name);continue
        if dst.exists():
            if digest(dst)==digest(src):continue
            old=subprocess.run(['git','show',before['head']+':'+name],cwd=PRIMARY,capture_output=True)
            assert old.returncode==0 and hashlib.sha256(old.stdout).hexdigest()==digest(dst),('New concurrent working-file change',name)
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);updated.append(name)
    real_index=Path(git('rev-parse','--git-path','index').decode().strip());real_index=real_index if real_index.is_absolute() else PRIMARY/real_index
    index_bytes=real_index.read_bytes();temporary=real_index.with_name('character-hair-merged.index');assert not temporary.exists()
    env=dict(os.environ,GIT_INDEX_FILE=str(temporary));subprocess.run(['git','read-tree',commit],cwd=PRIMARY,env=env,check=True)
    lock=real_index.with_name(real_index.name+'.lock');fd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
    ref_advanced=False
    try:
        assert real_index.read_bytes()==index_bytes,'Primary index changed before lock'
        with os.fdopen(fd,'wb') as f:f.write(temporary.read_bytes());f.flush();os.fsync(f.fileno())
        subprocess.run(['git','update-ref','refs/heads/main',commit,before['head']],cwd=PRIMARY,check=True);ref_advanced=True
        os.replace(lock,real_index)
    finally:
        if not ref_advanced and lock.exists():lock.unlink()
        if temporary.exists():temporary.unlink()
    assert git('rev-parse','HEAD').decode().strip()==commit
    assert not git('diff','--cached','--name-only').strip()
    for name,row in original.items():
        if row['kind']!='missing':assert digest(PRIMARY/name)==row['sha256'] and stat.S_IMODE((PRIMARY/name).lstat().st_mode)==row['mode']
    report={'head':commit,'previous_head':before['head'],'preserved_snapshot_paths':len(original),'preserved_sha_and_mode':True,'working_files_left_intact':kept,'new_committed_files_copied':updated,'index_updated_under_exclusive_git_lock':True,'stash_reset_clean_force_push_used':False}
    (HERE/'PRIMARY-SYNC-VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if not isinstance(v,list)}))
if __name__=='__main__':main()
