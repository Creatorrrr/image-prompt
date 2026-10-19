"""Exact pytest cache ZIP recovery, independent of Git and the old pytest environment."""
from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

import bundles
import history_restore
import pytest_proof
from pytest_state import E, ROOT, new, targets
import state

ARCHIVE=E/'BYTECODE-RECOVERY.zip'
SEAL=E/'BYTECODE-RECOVERY-LOCK.json'


def restore_zip(archive,seal,destination):
    if not 0<len(seal['files'])<=65 or sum(r['bytes'] for r in seal['files'].values())>807566:
        raise ValueError('pytest recovery exceeds reviewed budget')
    return history_restore.restore_zip(archive,seal,destination)


def load_seal():
    if state.sha(SEAL)!=state.read(E/'STAGE03.json')['seal_sha256']:raise ValueError('recovery seal changed')
    return state.read(SEAL)


def prove():
    if (E/'STAGE03.json').exists() or ARCHIVE.exists() or SEAL.exists():raise FileExistsError('recovery already recorded')
    rows=pytest_proof.load_lock()['rows'];frozen={r['path']:r for r in targets()}
    for row in rows:
        if state.stamp(ROOT/row['path'])!=frozen[row['path']]['before']:raise ValueError('cache changed')
    seal=bundles.pack(ARCHIVE,{r['path']:ROOT/r['path'] for r in rows})
    for row in rows:seal['files'][row['path']]['mode']=row['mode']
    seal.update(schema='photo-original-pytest-cache/v1',cache_code_executions=0)
    with tempfile.TemporaryDirectory(prefix='pytest-recovery-') as temp:
        temp=Path(temp);raw=restore_zip(ARCHIVE,seal,temp/'zip');compiled=pytest_proof.compile_rows(rows,temp/'git')
        for row in rows:
            for root in (raw,compiled):
                p=root/row['path']
                if state.sha(p)!=row['sha256'] or p.stat().st_mode&0o777!=row['mode']:raise ValueError('exact recovery differs')
    new(SEAL,seal)
    new(E/'STAGE03.json',{'status':'PASS','files':len(rows),'original_bytes':sum(r['bytes'] for r in rows),
        'archive_bytes':ARCHIVE.stat().st_size,'seal_sha256':state.sha(SEAL),'archive_sha256':seal['archive_sha256'],
        'backends':['original bytes','Git source + pinned pytest writer/reader'],
        'cache_code_executions':0,'Gemini_calls':0,'CURRENT_writes':0})
    print('stage 3 PASS;',len(rows),'files; recovery archive',ARCHIVE.stat().st_size,'bytes',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prove','restore']);p.add_argument('destination',nargs='?');a=p.parse_args()
    prove() if a.command=='prove' else restore_zip(ARCHIVE,load_seal(),a.destination)
