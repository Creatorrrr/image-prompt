"""Verify historical candidate provenance using preserved source evidence.

The archive contains original sealed body shards, not an executable old
search index. No active runtime, source record or archive is modified.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile

import photo_candidate_corpus as corpus

REGISTRY = Path(__file__).with_name('photo_legacy_evidence_manifest.json')
SOURCE = re.compile(r'^installed-h-f2-canonical-candidate:([0-9a-f]{64})/(cand_[0-9a-f]{32})$')


def digest(value):
    data = json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode()
    return hashlib.sha256(data).hexdigest()


def file_sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def _check_archive(entry, expected):
    archive = Path(entry['archive']).expanduser()
    override = os.environ.get('PHOTO_LEGACY_EVIDENCE_DIR')
    if override:
        archive = Path(override).expanduser() / archive.name
    if not archive.is_file() or file_sha(archive) != entry['archive_sha256']:
        raise ValueError('legacy candidate evidence archive missing or changed: ' + str(archive))
    zstd = shutil.which('zstd')
    if not zstd:
        # Desktop-launched processes may have a minimal PATH even though the
        # package is installed in its normal local Homebrew location.
        for candidate in ('/opt/homebrew/bin/zstd', '/usr/local/bin/zstd',
                          '/opt/homebrew/anaconda3/bin/zstd'):
            if Path(candidate).is_file() and os.access(candidate, os.X_OK):
                zstd = candidate
                break
    if not zstd:
        raise ValueError('zstd executable is required for legacy candidate evidence')
    process = subprocess.Popen([zstd, '-q', '-d', '-c', str(archive)], stdout=subprocess.PIPE)
    assert process.stdout is not None
    manifest = source_manifest = locator = None
    wanted = {}
    found = set()
    metadata_seen = set()
    try:
        with tarfile.open(fileobj=process.stdout, mode='r|') as tar:
            for item in tar:
                name = item.name
                if name in ('manifest.json', 'source-manifest.json', 'body-locator.json.gz'):
                    if not item.isfile() or name in metadata_seen:
                        raise ValueError('invalid legacy source archive metadata')
                    metadata_seen.add(name)
                    stream = tar.extractfile(item)
                    if stream is None:
                        raise ValueError('missing legacy archive metadata')
                    raw = stream.read()
                    if name == 'manifest.json':
                        manifest = json.loads(raw)
                        if digest(manifest) != entry['generation_id']:
                            raise ValueError('legacy source manifest identity mismatch')
                    else:
                        if manifest is None or hashlib.sha256(raw).hexdigest() != manifest['files'][name]:
                            raise ValueError('legacy source metadata hash mismatch: ' + name)
                        if name == 'source-manifest.json':
                            source_manifest = json.loads(raw)
                        else:
                            locator = json.loads(gzip.decompress(raw))
                            for cid in expected:
                                if cid not in locator:
                                    raise ValueError('legacy source candidate is missing: ' + cid)
                                wanted.setdefault(locator[cid]['path'], []).append(cid)
                elif name in wanted:
                    if not item.isfile() or manifest is None or source_manifest is None or locator is None:
                        raise ValueError('legacy source shard appears before its metadata')
                    stream = tar.extractfile(item)
                    if stream is None:
                        raise ValueError('missing legacy source shard')
                    raw = stream.read()
                    actual = hashlib.sha256(raw).hexdigest()
                    if actual != manifest['files'].get(name) or actual != source_manifest['files'].get(name):
                        raise ValueError('legacy source shard hash mismatch: ' + name)
                    shard = json.loads(gzip.decompress(raw))
                    for cid in wanted.pop(name):
                        record = shard[cid]
                        actual_record = digest(record)
                        if (record.get('id') != cid or actual_record != locator[cid]['sha256']
                                or any(actual_record != h for h in expected[cid])):
                            raise ValueError('legacy candidate provenance mismatch: ' + cid)
                        found.add(cid)
        process.stdout.close()
        if process.wait() != 0:
            raise ValueError('could not decompress legacy source archive')
    except BaseException:
        process.stdout.close()
        if process.poll() is None:
            process.terminate()
        process.wait()
        raise
    if wanted or found != set(expected):
        raise ValueError('legacy source archive is incomplete')
    return len(found)


def verify(records, registry=REGISTRY):
    """Verify each saved old-generation provenance without opening that runtime."""
    groups = {}
    for cid, record in records.items():
        for entry in record.get('provenance', []):
            source = entry.get('source', '')
            match = SOURCE.fullmatch(source)
            if not match:
                if source.startswith('installed-h-f2-canonical-candidate:'):
                    raise ValueError('invalid legacy candidate provenance: ' + cid)
                continue
            generation, source_cid = match.groups()
            expected_hash = entry.get('sha256')
            if cid != source_cid or not isinstance(expected_hash, str) or not re.fullmatch('[0-9a-f]{64}', expected_hash):
                raise ValueError('invalid legacy candidate provenance: ' + cid)
            groups.setdefault(generation, {}).setdefault(cid, []).append(expected_hash)
    if not groups:
        return {'archives': 0, 'candidates': 0}
    data = json.loads(Path(registry).read_bytes())
    if data.get('schema') != 'photo-legacy-evidence-registry/v1':
        raise ValueError('unsupported legacy evidence registry')
    entries = data['archives']
    by_generation = {row['generation_id']: row for row in entries}
    if len(by_generation) != len(entries):
        raise ValueError('duplicate legacy evidence generation')
    count = 0
    for generation, expected in groups.items():
        if generation not in by_generation:
            raise ValueError('legacy source archive is not registered: ' + generation)
        count += _check_archive(by_generation[generation], expected)
    return {'archives': len(groups), 'candidates': count}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(corpus.load(args.assets)['candidates']), ensure_ascii=False))
