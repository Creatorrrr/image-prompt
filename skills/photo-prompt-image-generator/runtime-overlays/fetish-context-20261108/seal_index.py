#!/usr/bin/env python3
"""Bind a built research index into a code-staged H-F2 generation, without activation."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
OUT = Path(os.environ.get('FETISH_CONTEXT_OUTPUT', str(ROOT / 'generated/fetish-hf2-integration-20261108'))).resolve()
STORE = OUT / os.environ.get('FETISH_CONTEXT_STORE', 'code-store')
lock = json.loads((OUT / 'input-lock.json').read_bytes())
base = json.loads((Path(__file__).resolve().parent / 'BASE.json').read_bytes())
config = SKILL / 'retrieval-runtime.json'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def guard():
    assert sha(config) == lock['config_sha256'], 'active runtime changed'
    for name, digest in lock['source_sha256'].items():
        assert sha(SKILL / 'assets' / name) == digest, 'context source changed'
    assert sha(OUT / 'research-context-index.json.gz') == lock['context_index_sha256']
    assert base['generation_id'] == lock['base_generation']

guard()
generations = list((STORE / 'h-f2-generations').iterdir())
assert len(generations) == 1
old = generations[0]
old_manifest = json.loads((old / 'manifest.json').read_bytes())
native = STORE / 'generations' / old_manifest['native_generation_id']
sys.path.insert(0, str(native / 'scripts'))
import photo_candidate_corpus as c
from photo_installed_h_f2 import release
import photo_h_f2_research_context as research
from photo_h_f2_generation import Generation
assert c.digest(old_manifest) == old.name
assert sha(native / 'scripts/photo_h_f2_research_context.py') == sha(Path(__file__).resolve().parent / 'scripts/photo_h_f2_research_context.py')
with gzip.open(OUT / 'research-context-index.json.gz', 'rt', encoding='utf-8') as f:
    data = json.load(f)
assert c.digest(data) == lock['context_index_canonical_sha256']
manifest = dict(old_manifest)
manifest['files'] = dict(manifest['files'])
manifest['files'][research.FILE] = lock['context_index_sha256']
manifest['research_context'] = {'schema': research.SCHEMA, 'file': research.FILE,
    'rows': lock['rows'], 'canonical_sha256': lock['context_index_canonical_sha256'],
    'context_only': True, 'native_approval': False}
generation = c.digest(manifest)
destination = STORE / 'h-f2-generations' / generation
if destination.exists():
    raise FileExistsError(destination)
with tempfile.TemporaryDirectory(prefix='.research-seal-', dir=STORE / 'h-f2-generations') as tmp:
    stage = Path(tmp) / 'generation'
    shutil.copytree(old, stage, ignore=shutil.ignore_patterns('manifest.json'), copy_function=os.link)
    shutil.copyfile(OUT / 'research-context-index.json.gz', stage / research.FILE)
    (stage / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
    guard()
    os.rename(stage, destination)
release(STORE, generation, full=True)
verified = Generation(STORE, generation, full=True)
assert research.load(verified)['schema'] == research.SCHEMA
guard()
result = {'status': 'staged_verified_inactive', 'generation_id': generation,
          'native_generation_id': manifest['native_generation_id'], 'parent_generation_id': lock['base_generation'],
          'research_rows': lock['rows'], 'document_embeddings': lock['document_embeddings'],
          'research_index_sha256': lock['context_index_sha256'], 'candidate_index_unchanged': True}
(OUT / os.environ.get('FETISH_CONTEXT_STAGED', 'staged.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
