"""Rebuild official indexes from authored sources with exact-input cached vectors."""
import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--workspace', type=Path, required=True)
parser.add_argument('--label', required=True)
args = parser.parse_args()
workspace = args.workspace.resolve()
skill = workspace / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(skill / 'scripts'))
import build_semantic_index as builder
import prompt_generator as generator
from photo_runtime_sources import source_update

main = Path('/Users/chasoik/Projects/image-prompt')
integration = Path('/Users/chasoik/.codex/worktrees/summer-fashion-integration-20261009/image-prompt')
evidence = main / 'docs/research-evidence/photo-prompt/summer-fashion-publication-20261009'
cache = Path('/Users/chasoik/.cache/image-prompt/summer-fashion-publication-20261009')
cache.mkdir(parents=True, exist_ok=True)
assets = skill / 'assets'
data = generator.load_json(assets / 'photo_prompt_tags.json')
expected = builder.base_payload(data, generator.SEMANTIC_PROVIDER, generator.SEMANTIC_MODEL_ID, 768)
rows = generator.iter_semantic_entries(data)
texts = {key: generator.semantic_text_for_entry(entry, slot, kind=kind) for key, kind, entry, slot in rows}
matched = {}
cache_report = []
cache_roots = (workspace, integration, main) if args.label == 'feature' else (cache / 'feature-indexes', integration, main)
for root in cache_roots:
    index = root / 'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json'
    payload = builder.load_payload(index)
    if not payload or not builder.metadata_matches(payload, expected):
        continue
    count = 0
    for key, row in payload['entries'].items():
        if key in texts and row.get('text') == texts[key] and isinstance(row.get('vector'), list) and len(row['vector']) == 768:
            matched[key] = row
            count += 1
    cache_report.append(dict(path=str(index), manifest_sha256=hashlib.sha256(index.read_bytes()).hexdigest(), exact_input_matches=count))
    del payload
missing = sorted(set(texts) - set(matched))
print(json.dumps(dict(label=args.label, semantic_rows=len(rows), exact_cached=len(matched), missing=len(missing)), ensure_ascii=False), flush=True)
reviewed_reused_ids = {'fit_ff09_v1_candidate', 'fit_ff52_v1_candidate', 'fit_ff52_v2_candidate',
                      'clt_ct031_v1', 'clt_ct064_v1', 'clt_ct064_v2', 'clt_ct065_v2'}
assert all(key.rsplit(':', 1)[-1] in reviewed_reused_ids for key in missing), 'Unreviewed embedding delta: ' + ', '.join(missing[:12])
checkpoint = cache / (args.label + '-exact-input-checkpoint.json')
builder.write_payload(checkpoint, {**expected, 'entries': matched}, compact=True)
del matched
builder.load_project_env()
embedding_calls = 0
embed = builder.embed_texts_with_gemini
def counted_embed(*positional, **keyword):
    global embedding_calls
    embedding_calls += 1
    return embed(*positional, **keyword)
builder.embed_texts_with_gemini = counted_embed
payload = builder.build_resumable_index_payload(data, output=assets / 'photo_prompt_semantic_index.json', checkpoint=checkpoint,
    provider=generator.SEMANTIC_PROVIDER, model=generator.SEMANTIC_MODEL_ID, dimensions=768, batch_size=1,
    request_interval=0, retry_attempts=0, retry_initial_delay=0, cache_indexes=[])
payload['created_at'] = datetime.now(timezone.utc).isoformat()
with source_update(skill):
    manifest = builder.write_sharded_payload(assets / 'photo_prompt_semantic_index.json', payload, shard_count=16, keep_stale_generations=True)
del payload
command = [sys.executable, str(skill / 'scripts/build_visual_profile_index.py'), '--no-runtime-publication']
for root in cache_roots:
    command.extend(['--cache-index', str(root / 'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json')])
log = evidence / (args.label + '-visual-build.log')
with log.open('w') as stream:
    completed = subprocess.run(command, cwd=workspace, stdout=stream, stderr=subprocess.STDOUT)
assert completed.returncode == 0, 'Official visual builder failed: ' + str(log)
visual = json.loads((assets / 'photo_prompt_visual_profile_index.json').read_text())
result = dict(label=args.label, workspace=str(workspace), semantic_entries=manifest['entry_count'],
    semantic_dictionary_hash=manifest['dictionary_hash'], visual_profiles=visual.get('entry_count'),
    semantic_exact_input_cache_sources=cache_report, new_semantic_embedding_inputs=missing, new_semantic_embedding_calls=embedding_calls,
    checkpoint=str(checkpoint), visual_build_log=str(log), boundary='Only provider/model/dimensions-compatible full exact input vectors are reused; indexes/BM25F are rebuilt from the current authored sources.')
(evidence / (args.label + '-index-rebuild.json')).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False), flush=True)
