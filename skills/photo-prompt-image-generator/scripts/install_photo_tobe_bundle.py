#!/usr/bin/env python3
"""Install the verified TO-BE release from an explicitly supplied offline bundle."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile
import tempfile

import photo_candidate_corpus as corpus
import photo_installed_h_f2 as installed
import install_photo_h_f2_runtime as installer

SKILL = Path(__file__).resolve().parents[1]
LOCK = SKILL / 'data/tobe-release-lock.json'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as source:
        for block in iter(lambda: source.read(8 * 1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def extract_members(stream, destination, prefixes):
    """Extract only regular files within exact allowed prefixes; reject escapes."""
    dest = Path(destination)
    seen = set()
    with tarfile.open(fileobj=stream, mode='r|') as tar:
        for member in tar:
            raw = member.name.rstrip('/')
            name = PurePosixPath(raw)
            if not raw or name.is_absolute() or '..' in name.parts or str(name) != raw:
                raise ValueError('unsafe bundle member: ' + member.name)
            if not any(name == prefix or prefix in name.parents for prefix in prefixes):
                continue
            if member.isdir():
                continue
            if not member.isfile() or name in seen:
                raise ValueError('unsupported or duplicate bundle member: ' + member.name)
            seen.add(name)
            target = dest.joinpath(*name.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            source = tar.extractfile(member)
            if source is None:
                raise ValueError('missing bundle member: ' + member.name)
            with target.open('xb') as out:
                shutil.copyfileobj(source, out, length=4 * 1024 * 1024)
            os.chmod(target, 0o644)
    return seen


def extract_zstd(archive, destination, prefixes):
    zstd = shutil.which('zstd')
    if not zstd:
        zstd = next((str(p) for p in (Path('/opt/homebrew/bin/zstd'),
                     Path('/usr/local/bin/zstd'), Path('/opt/homebrew/anaconda3/bin/zstd'))
                     if p.is_file() and os.access(p, os.X_OK)), None)
    if not zstd:
        raise ValueError('zstd is required to unpack the offline bundle')
    process = subprocess.Popen([zstd, '-q', '-d', '-c', str(archive)], stdout=subprocess.PIPE)
    try:
        if process.stdout is None:
            raise ValueError('could not open bundle stream')
        seen = extract_members(process.stdout, destination, prefixes)
        process.stdout.close()
        if process.wait() != 0:
            raise ValueError('bundle decompression failed')
        return seen
    except BaseException:
        if process.stdout:
            process.stdout.close()
        if process.poll() is None:
            process.terminate()
        process.wait()
        raise


def verify_source_index(assets, lock):
    manifest_path = Path(assets) / 'photo_candidate_search.json'
    if sha(manifest_path) != lock['source_manifest_sha256']:
        raise ValueError('source index manifest differs from the locked TO-BE source')
    manifest = json.loads(manifest_path.read_bytes())
    if (manifest.get('layout_id') != lock['source_layout_id']
            or manifest.get('corpus_sha256') != lock['source_corpus_sha256']):
        raise ValueError('source index binding changed')
    if corpus.digest(corpus.load(assets)) != lock['source_corpus_sha256']:
        raise ValueError('candidate source changed; rebuild its index rather than install an old one')
    rows = manifest['shards'] + [manifest['metadata']]
    expected = {}
    parent = PurePosixPath('photo_candidate_search_shards') / lock['source_layout_id']
    for row in rows:
        path = PurePosixPath(row['path'])
        if path.parent != parent or path in expected:
            raise ValueError('unsafe or duplicate source index member')
        expected[path] = row['sha256']
    return expected


def install_source_index(archive, assets, lock):
    assets = Path(assets).resolve()
    if sha(archive) != lock['source_index_archive_sha256']:
        raise ValueError('source index archive checksum mismatch')
    expected = verify_source_index(assets, lock)
    parent = assets / 'photo_candidate_search_shards'
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / lock['source_layout_id']
    if target.is_symlink():
        raise ValueError('source index destination is a symlink')
    if target.exists():
        if not all((assets / p).is_file() and not (assets / p).is_symlink()
                   and sha(assets / p) == digest for p, digest in expected.items()):
            raise ValueError('existing source index differs; preserve it for inspection')
        return {'installed': False, 'verified': len(expected)}
    with tempfile.TemporaryDirectory(prefix='.tobe-index-', dir=parent) as tmp:
        prefix = PurePosixPath('photo_candidate_search_shards') / lock['source_layout_id']
        seen = extract_zstd(archive, tmp, [prefix])
        if seen != set(expected):
            raise ValueError('source index archive member coverage mismatch')
        for path, digest in expected.items():
            if sha(Path(tmp).joinpath(*path.parts)) != digest:
                raise ValueError('source index member changed: ' + str(path))
        # Recheck source data after extraction and keep installation on one filesystem.
        if verify_source_index(assets, lock) != expected:
            raise ValueError('source changed during source index installation')
        os.rename(Path(tmp).joinpath(*prefix.parts), target)
    return {'installed': True, 'verified': len(expected)}


def install_bundle(bundle, *, source_index=None, assets=SKILL/'assets', destination=None, activate=True):
    lock = json.loads(LOCK.read_bytes())
    if lock.get('schema') != 'photo-tobe-release-bundle/v1':
        raise ValueError('unsupported TO-BE bundle lock')
    if sha(bundle) != lock['release_archive_sha256']:
        raise ValueError('TO-BE release archive checksum mismatch')
    verify_source_index(assets, lock)
    if destination is not None and activate:
        raise ValueError('custom destination requires --no-activate')
    with tempfile.TemporaryDirectory(prefix='photo-tobe-release-') as tmp:
        prefixes = [PurePosixPath('runtime/generations') / lock['native_generation_id'],
                    PurePosixPath('runtime/h-f2-generations') / lock['generation_id']]
        extract_zstd(bundle, tmp, prefixes)
        store = Path(tmp) / 'runtime'
        native, manifest, native_manifest = installed.release(store, lock['generation_id'], full=True)
        if manifest['native_generation_id'] != lock['native_generation_id'] or native.name != lock['native_generation_id']:
            raise ValueError('TO-BE release pairing changed')
        current = installed.read(SKILL / installed.CONFIG)
        if (current.get('generation_id') != lock['generation_id']
                or current.get('native_generation_id') != lock['native_generation_id']
                or current.get('code_sha256') != installed.digest(native_manifest['source']['code'])):
            raise ValueError('working skill selects a different release; do not overwrite it')
        index_result = install_source_index(source_index, assets, lock) if source_index else None
        result = installer.install(store, lock['generation_id'], destination=destination,
                                   skill_root=SKILL, activate=activate)
    return {'status': 'pass', 'release': result, 'source_index': index_result}


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--source-index', type=Path)
    parser.add_argument('--assets', type=Path, default=SKILL/'assets')
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--no-activate', action='store_true')
    args = parser.parse_args()
    print(json.dumps(install_bundle(args.bundle, source_index=args.source_index, assets=args.assets,
                                   destination=args.destination, activate=not args.no_activate), ensure_ascii=False))


if __name__ == '__main__':
    main()
