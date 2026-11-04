"""Validate preserved original documents cited by reviewed view overlays."""
from __future__ import annotations

import hashlib
import base64
import gzip
import json
from pathlib import Path
import re

DOCUMENTS = Path(__file__).resolve().parents[1] / 'data/provenance/reviewed-source-documents.json'
RAW = 'generated/trend-scout/raw/reactorprompt-fashion-20261025/corpus.jsonl#doc_id='
LOCATOR = re.compile(r'(?:' + re.escape(RAW) + r'|reactorprompt-document:)([0-9a-f]{64})(?:#.*)?\Z')
GIT_REGISTRY = Path(__file__).with_name('photo_reviewed_git_source_manifest.json')
GIT_LOCATOR = re.compile(r'git:([0-9a-f]{40}):([^#]+)#(/.*)\Z')


def _references(value):
    if isinstance(value, dict):
        locator = value.get('locator')
        if isinstance(locator, str) and (locator.startswith(RAW) or locator.startswith('reactorprompt-document:')):
            match = LOCATOR.fullmatch(locator)
            if not match:
                raise ValueError('invalid reviewed document locator')
            yield match.group(1), value.get('quote')
        for item in value.values():
            yield from _references(item)
    elif isinstance(value, list):
        for item in value:
            yield from _references(item)


def verify(overlays, documents_path=DOCUMENTS):
    references = list(_references(overlays))
    if not references:
        return {'documents': 0, 'quotes': 0}
    bundle = json.loads(Path(documents_path).read_bytes())
    if bundle.get('schema') != 'photo-reviewed-source-documents/v1' or not isinstance(bundle.get('documents'), dict):
        raise ValueError('invalid reviewed source documents')
    checked = set()
    for document_id, quote in references:
        row = bundle['documents'].get(document_id)
        if not isinstance(row, dict) or row.get('doc_id') != document_id or not isinstance(row.get('text'), str):
            raise ValueError('reviewed source document missing: ' + document_id)
        text = row['text']
        if hashlib.sha256(text.encode('utf-8')).hexdigest() != document_id:
            raise ValueError('reviewed source document changed: ' + document_id)
        if not isinstance(quote, str) or not quote or quote not in text:
            raise ValueError('reviewed source quote changed: ' + document_id)
        checked.add(document_id)
    return {'documents': len(checked), 'quotes': len(references)}


def _git_references(value):
    if isinstance(value, dict):
        locator = value.get('locator')
        if isinstance(locator, str) and locator.startswith('git:'):
            match = GIT_LOCATOR.fullmatch(locator)
            if not match:
                raise ValueError('invalid reviewed Git source locator')
            yield *match.groups(), value.get('quote')
        for item in value.values():
            yield from _git_references(item)
    elif isinstance(value, list):
        for item in value:
            yield from _git_references(item)


def _git_oid(kind, raw):
    return hashlib.sha1(kind.encode('ascii') + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def _tree_entries(raw):
    entries = {}
    position = 0
    try:
        while position < len(raw):
            space = raw.index(b' ', position)
            end = raw.index(b'\0', space + 1)
            name = raw[space + 1:end].decode('utf-8')
            oid = raw[end + 1:end + 21]
            if not name or name in entries or len(oid) != 20:
                raise ValueError('invalid Git tree entry')
            entries[name] = oid.hex()
            position = end + 21
    except (UnicodeDecodeError, ValueError):
        raise ValueError('invalid Git tree proof') from None
    return entries


def _source_blob(commit, path, commits, tree_cache):
    proof = commits.get(commit)
    if not isinstance(proof, dict) or not isinstance(proof.get('trees'), dict):
        raise ValueError('reviewed Git commit proof missing: ' + commit)
    try:
        raw_commit = base64.b64decode(proof['raw_base64'], validate=True)
    except (ValueError, TypeError, KeyError):
        raise ValueError('invalid reviewed Git commit proof') from None
    if _git_oid('commit', raw_commit) != commit:
        raise ValueError('reviewed Git commit proof changed: ' + commit)
    first = raw_commit.split(b'\n', 1)[0]
    if not re.fullmatch(rb'tree [0-9a-f]{40}', first):
        raise ValueError('invalid reviewed Git commit tree')
    oid = first[5:].decode('ascii')
    parts = path.split('/')
    if any(part in ('', '.', '..') for part in parts):
        raise ValueError('invalid reviewed Git source path')
    for part in parts:
        if oid not in tree_cache:
            try:
                raw = base64.b64decode(proof['trees'][oid], validate=True)
            except (ValueError, TypeError, KeyError):
                raise ValueError('reviewed Git tree proof missing: ' + oid) from None
            if _git_oid('tree', raw) != oid:
                raise ValueError('reviewed Git tree proof changed: ' + oid)
            tree_cache[oid] = _tree_entries(raw)
        try:
            oid = tree_cache[oid][part]
        except KeyError:
            raise ValueError('reviewed Git source not in commit: ' + path) from None
    return oid


def verify_git(overlays, registry=GIT_REGISTRY):
    """Check Git-origin evidence from preserved bytes without needing Git history."""
    references = list(_git_references(overlays))
    if not references:
        return {'documents': 0, 'quotes': 0}
    registry = Path(registry)
    manifest = json.loads(registry.read_bytes())
    if manifest.get('schema') != 'photo-reviewed-git-source-registry/v1':
        raise ValueError('invalid reviewed Git source registry')
    archive = (registry.parent / manifest['archive']).resolve()
    packed = archive.read_bytes()
    if hashlib.sha256(packed).hexdigest() != manifest['archive_sha256']:
        raise ValueError('reviewed Git source archive changed')
    bundle = json.loads(gzip.decompress(packed))
    sources = bundle.get('sources')
    if (bundle.get('schema') != 'photo-reviewed-git-sources/v1'
            or not isinstance(sources, dict) or len(sources) != manifest['source_files']):
        raise ValueError('invalid reviewed Git source archive')
    parsed = {}
    commits = bundle.get('commits')
    if not isinstance(commits, dict):
        raise ValueError('reviewed Git commit proofs missing')
    tree_cache = {}
    for commit, path, pointer, quote in references:
        key = commit + ':' + path
        if key not in parsed:
            entry = sources.get(key)
            if not isinstance(entry, dict) or not isinstance(entry.get('text'), str):
                raise ValueError('reviewed Git source missing: ' + key)
            raw = entry['text'].encode('utf-8')
            blob = _git_oid('blob', raw)
            if (hashlib.sha256(raw).hexdigest() != entry.get('sha256')
                    or blob != entry.get('git_blob_sha1')
                    or blob != _source_blob(commit, path, commits, tree_cache)):
                raise ValueError('reviewed Git source changed: ' + key)
            parsed[key] = json.loads(raw)
        value = parsed[key]
        try:
            for part in pointer.split('/')[1:]:
                part = part.replace('~1', '/').replace('~0', '~')
                value = value[int(part)] if isinstance(value, list) else value[part]
        except (KeyError, IndexError, TypeError, ValueError):
            raise ValueError('reviewed Git source pointer missing: ' + key + '#' + pointer) from None
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)
        if not isinstance(quote, str) or not quote or quote not in text:
            raise ValueError('reviewed Git source quote changed: ' + key + '#' + pointer)
    return {'documents': len(parsed), 'quotes': len(references)}
