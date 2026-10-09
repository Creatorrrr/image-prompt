"""Use official builders and exact compatible caches in a reviewable staging directory."""
from pathlib import Path
import argparse
import datetime
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--source-root', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--checkpoint', type=Path, required=True)
parser.add_argument('--cache-index', type=Path, action='append', default=[])
args = parser.parse_args()
sys.path.insert(0, str(args.source_root/'scripts'))
import build_semantic_index as builder
import prompt_generator as pg
from photo_runtime_sources import capture_sources

before, _ = capture_sources(args.source_root)
builder.load_project_env()
data = pg.load_json(args.source_root/'assets/photo_prompt_tags.json')

def progress(done, total):
    if done == total or done % 50 == 0:
        print(f'Embedded or exactly reused {done}/{total}', flush=True)

payload = builder.build_resumable_index_payload(
    data, output=args.output, checkpoint=args.checkpoint,
    provider=pg.SEMANTIC_PROVIDER, model=pg.SEMANTIC_MODEL_ID,
    dimensions=pg.DEFAULT_SEMANTIC_DIMENSIONS, batch_size=1,
    request_interval=0.8, retry_attempts=4, retry_initial_delay=15.0,
    cache_indexes=args.cache_index, progress_callback=progress)
after, _ = capture_sources(args.source_root)
assert before == after, 'Concurrent source changed during staged index build; preserve output/checkpoint and rebuild against latest source.'
payload['created_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
pg.validate_semantic_index_metadata(payload, data)
builder.write_sharded_payload(args.output, payload, shard_count=16, keep_stale_generations=True)
reloaded = pg.load_semantic_index_payload(args.output)
pg.validate_semantic_index_metadata(reloaded, data)
assert set(reloaded['entries']) == {key for key, *_ in pg.iter_semantic_entries(data)}
print(json.dumps({'status':'PASS','entries':len(reloaded['entries']),
    'dictionary_hash':reloaded['dictionary_hash'],'provider':reloaded['provider'],
    'model':reloaded['embedding_model'],'dimensions':reloaded['embedding_dimensions'],
    'batch_size':1,'cache_indexes':[str(p) for p in args.cache_index]}, indent=2))
