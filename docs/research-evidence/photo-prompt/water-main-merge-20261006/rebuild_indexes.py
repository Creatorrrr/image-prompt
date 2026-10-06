"""Rebuild merged authored data using only exact compatible cached vectors."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache-root', type=Path, action='append', required=True)
    parser.add_argument('--report-dir', type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[4]
    skill = repo / 'skills/photo-prompt-image-generator'
    assets = skill / 'assets'
    here = args.report_dir or Path(__file__).resolve().parent
    here.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault('PHOTO_RUNTIME_STORE', str(repo / '.codex-artifacts/water-main-runtime'))
    sys.path.insert(0, str(skill / 'scripts'))
    import build_semantic_index as builder
    import prompt_generator as pg
    from photo_runtime_sources import source_update
    from build_semantic_index import write_sharded_payload

    data = pg.load_json(assets / 'photo_prompt_tags.json')
    out = assets / 'photo_prompt_semantic_index.json'
    caches = [root / 'assets/photo_prompt_semantic_index.json' for root in args.cache_root] + [out]
    checkpoint = repo / '.codex-artifacts/water-merge-semantic.partial'
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    # Multiple sides may contain different versions of one stable identity.
    # Select the version whose complete text matches this merged corpus.
    expected = builder.base_payload(data, pg.SEMANTIC_PROVIDER,
                                    pg.SEMANTIC_MODEL_ID, pg.DEFAULT_SEMANTIC_DIMENSIONS)
    cache_payloads = [builder.load_payload(path) for path in caches]
    cache_payloads = [payload for payload in cache_payloads if payload and builder.metadata_matches(payload, expected)]
    exact = {}
    for key, kind, entry, slot in pg.iter_semantic_entries(data):
        text = pg.semantic_text_for_entry(entry, slot, kind=kind)
        for cached in reversed(cache_payloads):
            row = cached['entries'].get(key)
            if row and row.get('text') == text and len(row.get('vector') or []) == pg.DEFAULT_SEMANTIC_DIMENSIONS:
                exact[key] = row
                break
    checkpoint.write_text(json.dumps(dict(expected, entries=exact), ensure_ascii=False))
    with patch.object(builder, 'embed_texts_with_gemini', side_effect=AssertionError('Uncached text needs explicit genuine embedding; refusing invented vectors')) as calls:
        payload = builder.build_resumable_index_payload(
            data, output=out, checkpoint=checkpoint, provider=pg.SEMANTIC_PROVIDER,
            model=pg.SEMANTIC_MODEL_ID, dimensions=pg.DEFAULT_SEMANTIC_DIMENSIONS,
            batch_size=1, request_interval=0, retry_attempts=1,
            retry_initial_delay=0, cache_indexes=[])
        assert calls.call_count == 0
    payload['created_at'] = datetime.now(timezone.utc).isoformat()
    with source_update(skill):
        write_sharded_payload(out, payload, shard_count=16, keep_stale_generations=True)
    cmd = [sys.executable, str(skill / 'scripts/build_visual_profile_index.py')]
    for root in args.cache_root:
        cmd.extend(['--cache-index', str(root / 'assets/photo_prompt_visual_profile_index.json')])
    cmd.extend(['--batch-size', '1', '--no-runtime-publication'])
    result = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    (here / 'visual-index-build.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    assert 'embedded ' not in result.stdout, 'New visual embeddings were unexpectedly required'
    visual = json.loads((assets / 'photo_prompt_visual_profile_index.json').read_text())
    report = {
        'semantic_entries': len(payload['entries']),
        'semantic_embedding_calls': 0, 'visual_embedding_calls': 0,
        'provider': payload['provider'], 'model': payload['embedding_model'],
        'dimensions': payload['embedding_dimensions'],
        'cache_rule': 'Exact complete text, identity, provider, model and dimensions; different cached versions of one identity are selected by actual merged text',
        'semantic_manifest_sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
        'visual_manifest_sha256': hashlib.sha256((assets / 'photo_prompt_visual_profile_index.json').read_bytes()).hexdigest(),
        'old_shards_retained': True,
    }
    (here / 'INDEX-REBUILD.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
