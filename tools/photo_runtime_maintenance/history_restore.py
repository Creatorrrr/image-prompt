"""Exact original-cache ZIP recovery, independent of historical Python/Git availability."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import stat
import tempfile
import unicodedata
import zipfile

import bundles
from deferred_restore import publish_exclusive
import history_proof
from history_state import E, ROOT, new, targets
import state

ARCHIVE = E/'BYTECODE-RECOVERY.zip'
SEAL = E/'BYTECODE-RECOVERY-LOCK.json'


def restore_zip(archive,seal,destination):
    archive=Path(archive);destination=Path(destination)
    if destination.exists() or destination.is_symlink():raise FileExistsError('restore destination exists')
    if archive.is_symlink() or state.sha(archive)!=seal['archive_sha256']:raise ValueError('archive hash differs')
    if not 0<len(seal['files'])<=228 or sum(r['bytes'] for r in seal['files'].values())>5063794:
        raise ValueError('recovery closure exceeds reviewed budget')
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();folded=[unicodedata.normalize('NFD',n).casefold() for n in names]
        if len(names)!=len(set(names)) or len(folded)!=len(set(folded)) or set(names)!=set(seal['files']):
            raise ValueError('duplicate, colliding or missing recovery members')
        payloads={}
        for member in z.infolist():
            bundles.safe_name(member.filename)
            row=seal['files'][member.filename];mode=member.external_attr>>16
            if stat.S_IFMT(mode)!=stat.S_IFREG or (mode&0o777)!=row['mode']:
                raise ValueError('nonregular member or permission mismatch')
            if member.file_size!=row['bytes']:raise ValueError('member size differs')
            raw=z.read(member)
            if hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('member hash differs')
            payloads[member.filename]=raw
        destination.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.history-recovery-',dir=destination.parent) as temp:
            staged=Path(temp)/'root';staged.mkdir()
            for name,raw in payloads.items():
                p=staged/name;p.parent.mkdir(parents=True,exist_ok=True)
                with p.open('xb') as stream:stream.write(raw)
                p.chmod(seal['files'][name]['mode'])
            publish_exclusive(staged,destination)
    return destination


def load_seal():
    checkpoint=state.read(E/'STAGE03.json')
    if state.sha(SEAL)!=checkpoint['seal_sha256']:raise ValueError('recovery seal changed')
    return state.read(SEAL)


def prove():
    if (E/'STAGE03.json').exists() or ARCHIVE.exists() or SEAL.exists():
        raise FileExistsError('recovery proof already exists')
    rows=history_proof.load_lock()['rows'];frozen={r['path']:r for r in targets()}
    for row in rows:
        if state.stamp(ROOT/row['path'])!=frozen[row['path']]['before']:
            raise ValueError('cache changed before original-byte archival')
    seal=bundles.pack(ARCHIVE,{r['path']:ROOT/r['path'] for r in rows})
    for row in rows:seal['files'][row['path']]['mode']=row['mode']
    seal.update(schema='photo-original-history-bytecodes/v1',cache_code_executions=0)
    with tempfile.TemporaryDirectory(prefix='history-recovery-proof-') as temp:
        temp=Path(temp);zip_root=restore_zip(ARCHIVE,seal,temp/'zip')
        compiled=history_proof.compile_rows(rows,temp/'compiled')
        for row in rows:
            for root in (zip_root,compiled):
                p=root/row['path']
                if state.sha(p)!=row['sha256'] or p.stat().st_mode&0o777!=row['mode']:
                    raise ValueError('recovery byte/permission mismatch')
    new(SEAL,seal)
    new(E/'STAGE03.json',{'status':'PASS','files':len(rows),'original_bytes':sum(r['bytes'] for r in rows),
        'archive_bytes':ARCHIVE.stat().st_size,'archive_sha256':seal['archive_sha256'],
        'seal_sha256':state.sha(SEAL),'backends':['original-byte ZIP','Git source recompile'],
        'cache_code_executions':0,'Gemini_calls':0,'CURRENT_writes':0})
    print('stage 3 recovery PASS:',len(rows),'files; archive',ARCHIVE.stat().st_size,'bytes',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['prove','restore'])
    p.add_argument('destination',nargs='?',type=Path);a=p.parse_args()
    prove() if a.command=='prove' else restore_zip(ARCHIVE,load_seal(),a.destination)
