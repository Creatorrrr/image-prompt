"""Run the canonical index builders with embedding/network access disabled."""
from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--source-root', type=Path, required=True)
parser.add_argument('--runtime-store', type=Path, required=True)
args = parser.parse_args()
root = args.source_root.resolve()
os.environ['PHOTO_RUNTIME_STORE'] = str(args.runtime_store.resolve())
sys.path.insert(0, str(root / 'scripts'))

def prohibit_network(event, arguments):
    if event in {'socket.connect', 'socket.getaddrinfo'}:
        raise RuntimeError('Offline index rebuild attempted network access')

sys.addaudithook(prohibit_network)
import build_semantic_index as semantic
import build_visual_profile_index as visual

def prohibit_embeddings(*arguments, **keywords):
    raise RuntimeError('Exact vector reuse precondition failed; no embedding request allowed')

semantic.embed_texts_with_gemini = prohibit_embeddings
visual.embed_texts_with_gemini = prohibit_embeddings
semantic.load_project_env = lambda: None
visual.load_project_env = lambda: None
sys.argv = ['build_semantic_index.py', '--tags', str(root / 'assets/photo_prompt_tags.json'),
            '--output', str(root / 'assets/photo_prompt_semantic_index.json'),
            '--batch-size', '1', '--no-runtime-publication', '--keep-stale-generations']
assert semantic.main() == 0
sys.argv = ['build_visual_profile_index.py', '--registry', str(root / 'assets/photo_prompt_visual_obligations.json'),
            '--output', str(root / 'assets/photo_prompt_visual_profile_index.json'),
            '--batch-size', '1', '--no-runtime-publication']
assert visual.main() == 0
from photo_runtime_sources import SnapshotPublisher
import json
result = SnapshotPublisher(root, args.runtime_store).publish()
print(json.dumps({'runtime_publication': result, 'embedding_api_calls': 0}, ensure_ascii=False))
