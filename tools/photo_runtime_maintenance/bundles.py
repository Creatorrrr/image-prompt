"""Deterministic, hash-checked, non-overwriting offline source/evidence bundles."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
import zipfile
from contextlib import contextmanager

from state import read, sha, write


def pack(destination, members):
    destination = Path(destination)
    if destination.exists():
        raise ValueError('bundle already exists')
    destination.parent.mkdir(parents=True, exist_ok=True)
    sealed = {}
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for relative, source in sorted(members.items()):
            safe_name(relative)
            p = Path(source)
            if p.is_symlink() or not p.is_file():
                raise ValueError('only regular files can be archived')
            raw = p.read_bytes()
            member = zipfile.ZipInfo(relative, (1980, 1, 1, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = (stat.S_IFREG | (p.stat().st_mode & 0o777)) << 16
            z.writestr(member, raw, compresslevel=9)
            sealed[relative] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    seal = {'archive_sha256': sha(destination), 'files': sealed}
    return split_archive(destination,seal) if destination.stat().st_size>32*1024*1024 else seal


def split_archive(archive, seal, chunk_bytes=32*1024*1024):
    """Keep Git members below 32 MiB; the joined ZIP retains its exact hash."""
    archive = Path(archive)
    if sha(archive)!=seal['archive_sha256'] or type(chunk_bytes) is not int or chunk_bytes<=0:
        raise ValueError('invalid split source or budget')
    parts = []
    with archive.open('rb') as stream:
        while raw := stream.read(chunk_bytes):
            part = archive.with_name(archive.name+'.part'+str(len(parts)+1).zfill(3))
            with part.open('xb') as out:
                out.write(raw)
            parts.append({'name':part.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    archive.unlink()
    return {**seal,'parts':parts}


@contextmanager
def joined_archive(archive,seal):
    archive = Path(archive)
    if 'parts' not in seal:
        yield archive
        return
    names = [p['name'] for p in seal['parts']]
    if len(names)!=len(set(names)) or not names:
        raise ValueError('invalid split archive closure')
    with tempfile.TemporaryDirectory(prefix='photo-archive-join-') as temp:
        target = Path(temp)/'joined.zip'
        with target.open('xb') as out:
            for row in seal['parts']:
                safe_name(row['name'])
                if '/' in row['name']:
                    raise ValueError('split member must be a sibling')
                p = archive.with_name(row['name'])
                if p.is_symlink() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:
                    raise ValueError('split archive part mismatch')
                with p.open('rb') as source:
                    shutil.copyfileobj(source,out)
        yield target


def safe_name(name):
    p = PurePosixPath(name)
    if not name or not p.parts or p.is_absolute() or '..' in p.parts or '\\' in name or str(p) != name:
        raise ValueError('unsafe archive member')


def restore(archive, seal, destination):
    """Extract verified regular files only, into a new root; never overwrite work."""
    archive, destination = Path(archive), Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ValueError('restore destination must not exist')
    with joined_archive(archive,seal) as joined:
        if sha(joined) != seal['archive_sha256']:
            raise ValueError('archive hash mismatch')
        return _restore_zip(joined,seal,destination)


def _restore_zip(archive,seal,destination):
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        if len(names) != len(set(names)) or set(names) != set(seal['files']):
            raise ValueError('archive member closure mismatch')
        for member in z.infolist():
            safe_name(member.filename)
            mode = member.external_attr >> 16
            if stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                raise ValueError('non-regular archive member')
            raw = z.read(member)
            expected = seal['files'][member.filename]
            if len(raw) != expected['bytes'] or hashlib.sha256(raw).hexdigest() != expected['sha256']:
                raise ValueError('archive member hash mismatch')
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='.restore-', dir=destination.parent) as tmp:
            staged = Path(tmp)/'root'
            staged.mkdir()
            for member in z.infolist():
                p = staged/member.filename
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(z.read(member))
                p.chmod((member.external_attr >> 16) & 0o777 or 0o644)
            staged.rename(destination)
    return destination


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', type=Path, required=True)
    p.add_argument('--lock', type=Path, required=True)
    p.add_argument('--destination', type=Path, required=True)
    a = p.parse_args()
    restore(a.archive, read(a.lock), a.destination)
    print('verified restoration complete:', a.destination)
