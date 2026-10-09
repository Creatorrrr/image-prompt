"""Snapshot dirty and untracked primary files without modifying them."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, stat, subprocess

PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
HERE=Path(__file__).resolve().parent
PREFIX='docs/research-evidence/photo-prompt/autumn-fashion-main-merge-20261009/'

def git(*args):
    return subprocess.check_output(['git','-c','core.fsmonitor=false',*args],cwd=PRIMARY)

def digest(p):
    if p.is_symlink():return hashlib.sha256(p.readlink().as_posix().encode()).hexdigest()
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def main():
    head=git('rev-parse','HEAD').decode().strip();tree=git('write-tree').decode().strip()
    staged=[s.decode() for s in git('diff','--cached','--name-only','-z').split(b'\0') if s]
    assert not staged,('Concurrent staged work must remain intact',staged)
    names=set()
    for args in [('diff','--name-only','-z'),('ls-files','--others','--exclude-standard','-z')]:
        names.update(r.decode() for r in git(*args).split(b'\0') if r)
    files=[]
    for name in sorted(names):
        if name.startswith(PREFIX):continue
        p=PRIMARY/name
        if not p.exists() and not p.is_symlink():files.append({'path':name,'kind':'missing'});continue
        files.append({'path':name,'kind':'symlink' if p.is_symlink() else 'file',
                      'sha256':digest(p),'bytes':p.lstat().st_size,'mode':stat.S_IMODE(p.lstat().st_mode)})
    assert git('rev-parse','HEAD').decode().strip()==head and git('write-tree').decode().strip()==tree
    payload={'schema':'autumn-publication-primary-preservation/v1','observed_at':datetime.now(timezone.utc).isoformat(),
             'head':head,'index_tree':tree,'staged_paths':staged,'files':files}
    initial=HERE/'PRIMARY-START.json'
    if initial.exists():
        old=json.loads(initial.read_text());current={r['path']:r for r in files};previous={r['path']:r for r in old['files']}
        drift=[n for n in previous if previous[n]!=current.get(n)]
        (HERE/'PRIMARY-CONCURRENT-DRIFT.json').write_text(json.dumps({'previous_head':old['head'],'current_head':head,
            'changed_or_now_clean_paths':drift,'new_dirty_or_untracked_paths':sorted(set(current)-set(previous)),
            'changed_bytes_not_overwritten':True,'new_snapshot_used_for_sync':True},indent=2)+'\n')
    (HERE/'PRIMARY-BEFORE.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'head':head,'preserved_paths':len(files),'preserved_bytes':sum(r.get('bytes',0) for r in files)}))

if __name__=='__main__':main()
