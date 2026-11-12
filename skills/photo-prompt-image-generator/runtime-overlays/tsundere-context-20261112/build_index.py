#!/usr/bin/env python3
"""Build an inactive, standalone advisory index; never mutate a runtime store."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys

OVERLAY = Path(__file__).resolve().parent
SKILL = OVERLAY.parents[1]
ROOT = SKILL.parents[1]
STORE = Path.home() / '.cache/image-prompt/photo-shared-runtime/h-f2-installed'
BASE = '763c9e9032cdb8969fa1c1650697ccb24aaf1962798bf527ad980d39ade27bb7'
LEGACY = 'adbfbd2bedaf0be8948fc802305a5112b854ebf9d9143993cb1065ef533d391e'
LEGACY_SHA = 'fdbb29d99d7a26f77b810678c8408ef07479b4caa7b8722a794fc50a81ed9755'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

p = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
p.add_argument('--output', required=True, type=Path, help='new empty output directory')
a = p.parse_args()
out = a.output.resolve()
# Do not permit outputs inside the installed store or any generation.
if out == STORE or STORE in out.parents:
    raise ValueError('output must be outside installed store')
out.mkdir(parents=True, exist_ok=False)
base_path = STORE / 'h-f2-generations' / BASE
legacy_path = STORE / 'h-f2-generations' / LEGACY
base = json.loads((base_path / 'manifest.json').read_bytes())
old = json.loads((legacy_path / 'manifest.json').read_bytes())
assert base['binding'] == old['binding']
legacy_file = legacy_path / 'research-context-index.json.gz'
assert sha(legacy_file) == LEGACY_SHA == old['files']['research-context-index.json.gz']
assert old['research_context']['rows'] == 28
native = STORE / 'generations' / base['native_generation_id']
sys.path[:0] = [str(OVERLAY / 'scripts'), str(native / 'scripts'), str(SKILL / 'scripts')]
import photo_h_f2_research_context as lane
from bm25f_retrieval import build_bm25f_index
from photo_tsundere_context_search import _load, _load_prose
from photo_candidate_corpus import digest

assets = SKILL / 'assets'
table, table_digest = _load(assets)
prose, prose_digest = _load_prose(assets)
# The original local research directory is ignored by Git. Keep exact, hash-
# checked snapshots with this overlay so a clean checkout can rebuild the lane.
table_snapshot = OVERLAY / 'source-snapshots/source-tables.json'
prose_snapshot = OVERLAY / 'source-snapshots/source-prose.json'
raw_table = table_snapshot.read_bytes()
raw_prose = prose_snapshot.read_bytes()
assert hashlib.sha256(raw_table).hexdigest() == table['source']['source_table_sha256']
assert hashlib.sha256(raw_prose).hexdigest() == prose['source']['sha256']
tables = json.loads(raw_table)
snapshot = {f"T{t['table']:02d}-{i:02d}": cells for t in tables for i, cells in enumerate(t['rows'], 1)}
assert len(snapshot) == 346 and all(snapshot[r['term_id']] == r['source_cells'] for r in table['views'])
paragraphs = json.loads(raw_prose)
assert all(paragraphs[r['source_location']['snapshot_item_1based'] - 1]['text'] == r['context_ko']
           for r in prose['views'])
assert len(prose['views']) == 91
review_name = 'photo_tsundere_109_reviewed_proposals_20261112.json'
review_path = assets / review_name
review_hash = sha(review_path)
review = json.loads(review_path.read_bytes())
review_rows = {r['source_row_id']: r for r in review['rows']}
followups = [r for r in table['views'] if 'followup_review' in r]
assert len(followups) == len(review_rows) == len(review['rows']) == 109
assert review['native_approval'] is False and review['automatic_activation'] is False
assert review['source_table_sha256'] == table['source']['source_table_sha256']
for row in followups:
    meta, reviewed = row['followup_review'], review_rows[row['term_id']]
    assert meta['review_file'] == review_name and meta['review_sha256'] == digest(reviewed)
    assert meta['native_approval'] is False and reviewed['source_cells'] == row['source_cells']
    for field in ('meaning_ko', 'observation_limit_ko', 'medium_requirements', 'candidate_disposition'):
        assert meta[field] == reviewed[field]
rows = table['views'] + prose['views']
assert len(rows) == 437 and len({r['id'] for r in rows}) == 437
sources = {
 'table': {'url': table['source']['url'], 'snapshot': table['source']['source_table_snapshot'],
           'snapshot_sha256': table['source']['source_table_sha256'], 'view_sha256': table_digest,
           'qualification': table['source']['qualification']},
 'prose': {'url': prose['source']['url'], 'snapshot': prose['source']['snapshot'],
           'snapshot_sha256': prose['source']['sha256'], 'view_sha256': prose_digest,
           'qualification': 'original conversation, not independent evidence'},
}
data = {'schema': lane.TS_SCHEMA, 'binding': base['binding'], 'rows': rows, 'sources': sources,
        'table_ids': [[t['table'], i] for t in tables for i in range(1, len(t['rows']) + 1)],
        'lexical_index': build_bm25f_index(lane.ts_documents(rows), policy=lane.TS_POLICY,
                                           lexicon=lane.TS_LEXICON)}
target = out / lane.TS_FILE
with target.open('wb') as raw:
    with gzip.GzipFile(fileobj=raw, mode='wb', mtime=0) as zipped:
        zipped.write(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
# Verify input hashes again after construction; this is a build, not a seal.
assert sha(assets / 'photo_tsundere_research_context_views_20261112.json') == table_digest
assert sha(assets / 'photo_tsundere_prose_context_20261112.json') == prose_digest
assert sha(table_snapshot) == sources['table']['snapshot_sha256']
assert sha(prose_snapshot) == sources['prose']['snapshot_sha256']
assert sha(review_path) == review_hash
lock = {'schema': 'photo-h-f2-tsundere-context-build/v1', 'base_generation': BASE,
        'native_generation': base['native_generation_id'], 'legacy_generation': LEGACY,
        'legacy_index_sha256': LEGACY_SHA, 'legacy_descriptor': old['research_context'],
        'rows': 437, 'table_rows': 346, 'prose_rows': 70, 'extracted_expressions': 21,
        'sources': sources, 'followup_review_file': review_name,
        'followup_review_sha256': review_hash, 'followup_review_rows': len(followups),
        'index_sha256': sha(target), 'canonical_sha256': digest(data),
        'overlay_code_sha256': sha(OVERLAY / 'scripts/photo_h_f2_research_context.py'),
        'status': 'built_unsealed_inactive'}
(out / 'build-lock.json').write_text(json.dumps(lock, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(lock, ensure_ascii=False, indent=2))
