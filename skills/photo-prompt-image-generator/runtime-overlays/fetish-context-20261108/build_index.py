#!/usr/bin/env python3
"""Build a sealed H-F2 research index from reviewed context rows, without activation."""
import gzip
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
OVERLAY = Path(__file__).resolve().parent
STORE = Path.home() / '.cache/image-prompt/photo-shared-runtime/h-f2-installed'
OUT = Path(os.environ.get('FETISH_CONTEXT_OUTPUT', str(ROOT / 'generated/fetish-hf2-integration-20261108'))).resolve()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

config_path = SKILL / 'retrieval-runtime.json'
config_bytes = config_path.read_bytes()
base = json.loads((OVERLAY / 'BASE.json').read_bytes())
baseline = STORE / 'h-f2-generations' / base['generation_id']
manifest = json.loads((baseline / 'manifest.json').read_bytes())
native = STORE / 'generations' / manifest['native_generation_id']
sys.path[:0] = [str(OVERLAY / 'scripts'), str(native / 'scripts'), str(SKILL / 'scripts')]
import photo_h_f2_research_context as ctx
from photo_h_f2_encoder import LocalEncoder
from bm25f_retrieval import build_bm25f_index
from photo_research_context_search import load_records

OUT.mkdir(parents=True, exist_ok=True)
target = OUT / 'research-context-index.json.gz'
if target.exists():
    raise FileExistsError(target)
records = load_records()
rows = [r for r in records.values() if r['tags'] == ['fetish']]
assert len(rows) == 28 and all(r['context_only'] and not r['native_approval'] for r in rows)
rows.sort(key=lambda row: row['id'])
inputs = [ctx.text(row) for row in rows]
with LocalEncoder(native) as encoder:
    assert encoder.binding == manifest['binding']
    embedded = encoder.encode(inputs, 'document')
for row, embedding in zip(rows, embedded, strict=True):
    row['vector'] = embedding['vector']
    row['embedding_execution'] = embedding['execution']
data = {'schema': ctx.SCHEMA, 'binding': manifest['binding'], 'rows': rows,
        'lexical_index': build_bm25f_index(ctx.documents(rows), policy=ctx.POLICY)}
assert config_path.read_bytes() == config_bytes, 'active configuration changed during embedding'
assert all(sha(SKILL / 'assets' / r['source_file']) == r['source_sha256'] for r in rows), 'research source changed during embedding'
with gzip.open(target, 'wt', encoding='utf-8') as stream:
    json.dump(data, stream, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
from photo_candidate_corpus import digest
lock = {'schema': 'fashion-research-context-build-lock/v1',
        'base_generation': base['generation_id'], 'native_generation': manifest['native_generation_id'],
        'config_sha256': hashlib.sha256(config_bytes).hexdigest(),
        'source_sha256': {r['source_file']: r['source_sha256'] for r in rows},
        'context_index_sha256': sha(target), 'context_index_canonical_sha256': digest(data),
        'rows': len(rows), 'document_embeddings': len(embedded)}
(OUT / 'input-lock.json').write_text(json.dumps(lock, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(lock, ensure_ascii=False), flush=True)
