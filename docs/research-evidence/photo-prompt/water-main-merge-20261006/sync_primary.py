"""Fast-forward published main while retaining every pre-existing dirty byte."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
HERE=Path(__file__).resolve().parent


def git(*args):
    return subprocess.check_output(['git',*args],cwd=PRIMARY).decode().strip()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--target',required=True)
    parser.add_argument('--qualified-root',type=Path,required=True)
    args=parser.parse_args()
    state=json.loads((HERE/'PREFLIGHT.json').read_text())
    assert git('rev-parse','HEAD')==state['head']
    assert git('branch','--show-current')=='main'
    assert git('write-tree')==state['index_tree'], 'Unrelated staged work changed'
    assert git('ls-remote','origin','refs/heads/main').split()[0]==args.target
    subprocess.run(['git','merge-base','--is-ancestor',state['head'],args.target],cwd=PRIMARY,check=True)
    drift=[name for name,expected in state['dirty_file_sha256'].items() if sha(PRIMARY/name)!=expected]
    assert not drift, f'Concurrent primary changes need reconciliation: {drift}'
    target_names=set(subprocess.check_output(['git','ls-tree','-r','--name-only','-z',args.target],cwd=PRIMARY).decode().split('\0'))
    changed=set(subprocess.check_output(['git','diff','--name-only','-z',state['head'],args.target],cwd=PRIMARY).decode().split('\0'))
    tracked=[name for name in state['modified_tracked'] if name in changed]
    untracked=[name for name in state['untracked'] if name in target_names]
    blocked=sorted(set(tracked+untracked))
    backup=PRIMARY/'.codex-artifacts/water-main-primary-sync'
    assert not backup.exists(), 'A prior sync backup exists; inspect before reuse'
    original=backup/'original';hold=backup/'untracked-hold'
    for name in blocked:
        p=PRIMARY/name
        if p.is_file():
            q=original/name;q.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,q);assert sha(q)==state['dirty_file_sha256'][name]
    if tracked:
        subprocess.run(['git','restore','--source=HEAD','--worktree','--',*tracked],cwd=PRIMARY,check=True)
    for name in untracked:
        p=PRIMARY/name
        if p.exists():
            q=hold/name;q.parent.mkdir(parents=True,exist_ok=True)
            p.rename(q)
    try:
        subprocess.run(['git','merge','--ff-only',args.target],cwd=PRIMARY,check=True,stdout=subprocess.DEVNULL)
    finally:
        for name in blocked:
            saved=original/name;dest=PRIMARY/name
            if saved.is_file():
                dest.parent.mkdir(parents=True,exist_ok=True)
                if sha(dest)!=sha(saved):
                    temporary=dest.with_name(dest.name+'.water-sync-tmp')
                    assert not temporary.exists()
                    shutil.copy2(saved,temporary);os.replace(temporary,dest)
            elif state['dirty_file_sha256'][name] is None and dest.is_file():
                dest.unlink()
    assert git('rev-parse','HEAD')==args.target
    preserved=[name for name,expected in state['dirty_file_sha256'].items() if sha(PRIMARY/name)==expected]
    assert len(preserved)==len(state['dirty_file_sha256'])
    # Copy only new evidence owned by this merge. The local preflight and
    # source backup remain local; existing evidence is never overwritten.
    source=args.qualified_root/'docs/research-evidence/photo-prompt/water-main-merge-20261006'
    for p in source.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts:continue
        q=HERE/p.relative_to(source)
        if q.exists():assert sha(q)==sha(p), f'Evidence collision: {q}'
        else:
            q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    result={'schema':'water-primary-sync/v1','head':args.target,'origin_main':git('rev-parse','origin/main'),
            'primary_main_fast_forwarded':True,'dirty_files_preserved_before_index_rebuild':len(preserved),
            'all_original_dirty_bytes_preserved':True,'temporarily_saved_tracked':len(tracked),
            'temporarily_saved_untracked_collisions':len(untracked),'backup':str(backup),
            'working_draft_source_policy':'Original unrelated draft sources remain exact. Rebuild only the two derived indexes for this working corpus; canonical V30 qualification belongs to the clean published tree.'}
    (HERE/'PRIMARY-SYNC.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
