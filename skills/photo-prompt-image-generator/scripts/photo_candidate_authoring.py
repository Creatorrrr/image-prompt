"""Versioned editing source and grounded, non-authoritative search annotations.

No model, retrieval, publisher or operating source imports. Every native source
byte remains recoverable independently of the installed cache generation.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path

SCHEMA = 'photo-candidate-authoring/v1'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    path = Path(path)
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(value) + b'\n'
    path.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == '.gz' else raw)


def export(generation, output):
    generation, output = Path(generation), Path(output)
    if output.exists():
        raise ValueError('a versioned editing source already exists')
    source = read(generation/'source-manifest.json')
    header = read(generation/'source-header.json.gz')
    groups = {}
    metadata = {}
    for relative, expected in sorted(source['files'].items()):
        if not relative.startswith('body/'):
            continue
        path = generation/relative
        if file_sha(path) != expected:
            raise ValueError('sealed source changed')
        for cid, record in read(path).items():
            if cid in metadata:
                raise ValueError('duplicate CID')
            prefix = cid[5:7]
            groups.setdefault(prefix, {})[cid] = record
            metadata[cid] = {'record_kind': record['record_kind'], 'source_sha256': digest(record),
                             'RIDs': sorted(record['meaning']['primary']),
                             'retrieval_class': record['meaning']['retrieval_class'],
                             'existing_graph': bool(record['meaning']['graphs']),
                             'path': 'body/'+prefix+'.json.gz'}
    records = {cid: record for group in groups.values() for cid, record in group.items()}
    if digest({**header, 'candidates': records}) != source['source_sha256']:
        raise ValueError('editing source lost source/header closure')
    output.mkdir(parents=True)
    for prefix, group in sorted(groups.items()):
        write(output/'body'/(prefix+'.json.gz'), group)
    write(output/'header.json.gz', header)
    write(output/'records.json.gz', metadata)
    manifest = {'schema': SCHEMA, 'source_corpus_sha256': source['source_sha256'],
                'source_generation_id': generation.name, 'candidate_count': len(records),
                'positive_count': sum(r['retrieval_class'] == 'positive' for r in metadata.values()),
                'files': {str(p.relative_to(output)): file_sha(p) for p in sorted(output.rglob('*')) if p.is_file()},
                'annotation_authority': 'search interpretation only; native facts/permissions unchanged'}
    write(output/'manifest.json', manifest)
    verify(output)
    return manifest


class Source:
    def __init__(self, root):
        self.root = Path(root)
        self.manifest = read(self.root/'manifest.json')
        if self.manifest['schema'] != SCHEMA:
            raise ValueError('unsupported editing source')
        self.metadata = self.member('records.json.gz')
        self.header = self.member('header.json.gz')
        self.cache = {}

    def member(self, relative):
        path = self.root/relative
        if file_sha(path) != self.manifest['files'][relative]:
            raise ValueError('editing source member changed')
        return read(path)

    def record(self, cid):
        meta = self.metadata[cid]
        relative = meta['path']
        if relative not in self.cache:
            self.cache[relative] = self.member(relative)
        record = self.cache[relative][cid]
        if digest(record) != meta['source_sha256']:
            raise ValueError('editing source CID changed')
        return record


def verify(root):
    source = Source(root)
    for relative in source.manifest['files']:
        source.member(relative)
    records = {cid: source.record(cid) for cid in sorted(source.metadata)}
    if (len(records) != source.manifest['candidate_count'] or
            digest({**source.header, 'candidates': records}) != source.manifest['source_corpus_sha256']):
        raise ValueError('editing source closure changed')
    return {'status': 'PASS', 'candidates': len(records), 'files': len(source.manifest['files']),
            'source_corpus_sha256': source.manifest['source_corpus_sha256']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('export');p.add_argument('--generation', type=Path, required=True);p.add_argument('--output', type=Path, required=True)
    p = sub.add_parser('verify');p.add_argument('--source', type=Path, required=True)
    p = sub.add_parser('show');p.add_argument('--source', type=Path, required=True);p.add_argument('--cid', required=True)
    args = parser.parse_args()
    value = export(args.generation, args.output) if args.command == 'export' else verify(args.source) if args.command == 'verify' else Source(args.source).record(args.cid)
    print(json.dumps(value, ensure_ascii=False, indent=2))
