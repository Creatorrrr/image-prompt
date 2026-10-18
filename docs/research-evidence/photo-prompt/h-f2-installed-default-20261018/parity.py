"""Recheck prior eight-goal quality in the skill-owned numerical runtime.

Archived inputs are copied to the private parity-inputs directory first. The
runtime reads no research checkout/build cache and reuses all64 judgments.
"""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
E = Path(__file__).parent
C = Path('/Users/chasoik/.cache/image-prompt/h-f2-default-install-20261018')
sys.path.insert(0, str(ROOT/'skills/photo-prompt-image-generator/scripts'))
from photo_installed_h_f2 import default_store, read, release
config = read(ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json')
native, _, _ = release(default_store(), config['generation_id'])
sys.path.insert(0, str(native/'scripts'))
import photo_candidate_corpus as corpus
import photo_recall_first as rf
from photo_recall_generation import write, file_sha
from photo_h_f2_generation import Generation
from photo_h_f2_workflow import search_material
from photo_h_f2_receipts import audit_packet
import numpy as np

inputs = C/'parity-inputs'
goals = read(inputs/'GOALS.json')['goals']
queries = read(inputs/'QUERIES.json')
generation = Generation(default_store(), config['generation_id'], full=True)
cache = C/'parity-query-cache'
cache.mkdir(exist_ok=True)
for goal in goals:
    text = goal['query']
    row = queries['rows'][goal['goal_id']]
    rf.check_embedding(row, generation.binding, text, 'query')
    key = corpus.digest({'text': text, 'binding': generation.binding})
    write(cache/(key+'.json'), {'text': text, 'binding': generation.binding, 'row': row})
queryset = {'recipe': 'photo-h-f2/v1', 'origin': 'previous frozen synthetic quality benchmark',
            'slots': {g['goal_id']: {'text': g['query']} for g in goals}}
output = C/'parity-raw'
assert not output.exists(), 'retain previous parity evidence instead of repeating search'
packet = search_material(generation, queryset, cache, output)
audit_packet(generation, packet, output)
expected = read(inputs/'TOP8.json')['goals']
exact_orders = exact_bm25 = exact_dense = 0
max_dense_difference = 0.
for goal in goals:
    key = goal['goal_id']
    assert [(r['cid'], r['rid']) for r in packet['goals'][key]['top8']] == [(r['cid'], r['rid']) for r in expected[key]]
    with np.load(output/(rf.sha(key)+'.npz')) as new, np.load(inputs/(key+'-raw.npz')) as old:
        assert np.array_equal(new['order'], old['order_document_positions'])
        exact_orders += 1
        exact_bm25 += int(np.array_equal(new['bm25'], old['bm25']))
        exact_dense += int(np.array_equal(new['cosine'], old['cosine']))
        max_dense_difference = max(max_dense_difference, float(np.max(np.abs(new['cosine']-old['cosine']))))
judgments = read(inputs/'JUDGMENTS.json')['rows']
lookup = {(r['goal_id'], r['cid'], r['rid'], r['source_sha256']): r for r in judgments}
keys = [(g, r['cid'], r['rid'], r['source_sha256']) for g, result in packet['goals'].items() for r in result['top8']]
assert len(keys) == 64 and set(keys) == set(lookup)
materials = {k[0] for k in keys if lookup[k]['contribution'] == 'concrete_material'}
feasible = {k[0] for k in keys if lookup[k]['contribution'] == 'concrete_material' and lookup[k]['application'] == 'feasible_for_sketch'}
assert (len(materials), len(feasible)) == (7, 4)
assert all(q['cache_hit'] for q in packet['queries'].values())
report = {'status': 'PASS', 'numpy': np.__version__, 'full_orders_exact': exact_orders,
          'raw_BM25_bitwise_equal': exact_bm25, 'raw_cosine_bitwise_equal': exact_dense,
          'maximum_cosine_absolute_difference': max_dense_difference,
          'top8_connections_equal': 64, 'reused_judgments': 64,
          'creative_material_goals': 7, 'feasible_goals': 4,
          'sketch_requests': len({r['case_id'] for r in read(inputs/'SKETCHES.json')['rows']}),
          'BM25F_calls': 8, 'local_cosine_calls': 8, 'new_inference': 0,
          'new_semantic_judgments': 0, 'CURRENT_writes': 0, 'Gemini_calls': 0,
          'inputs': {p.name: file_sha(p) for p in sorted(inputs.iterdir())}}
write(E/'PARITY.json', report)
print(json.dumps(report, ensure_ascii=False, indent=2))
