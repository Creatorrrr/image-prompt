"""Validate preserved original documents cited by reviewed view overlays."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

DOCUMENTS = Path(__file__).resolve().parents[1] / 'data/provenance/reviewed-source-documents.json'
RAW = 'generated/trend-scout/raw/reactorprompt-fashion-20261025/corpus.jsonl#doc_id='
LOCATOR = re.compile(r'(?:' + re.escape(RAW) + r'|reactorprompt-document:)([0-9a-f]{64})(?:#.*)?\Z')


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
