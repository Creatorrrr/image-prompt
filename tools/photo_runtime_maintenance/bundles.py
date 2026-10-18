"""Deterministic, hash-checked, non-overwriting offline source/evidence bundles."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
import zipfile

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
    return {'archive_sha256': sha(destination), 'files': sealed}


def safe_name(name):
    p = PurePosixPath(name)
    if not name or p.is_absolute() or '..' in p.parts or '\\' in name or str(p) != name:
        raise ValueError('unsafe archive member')


def restore(archive, seal, destination):
    """Extract verified regular files only, into a new root; never overwrite work."""
    archive, destination = Path(archive), Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ValueError('restore destination must not exist')
    if sha(archive) != seal['archive_sha256']:
        raise ValueError('archive hash mismatch')
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
