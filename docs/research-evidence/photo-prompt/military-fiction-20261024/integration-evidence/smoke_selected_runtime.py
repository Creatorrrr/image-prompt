"""Six cached-query operational probes of the finally selected release."""
import gc
gc.disable()
import json, sys
from pathlib import Path

O = Path(__file__).resolve().parent
R = O.parent
ROOT = Path('/Users/chasoik/Projects/image-prompt')
read = lambda path: json.loads(path.read_bytes())
release = read(O / 'rebase-selected/successor.json')
installed = read(O / 'rebase-selected/install-active.json')
config = read(ROOT / 'skills/photo-prompt-image-generator/retrieval-runtime.json')
assert installed['status'] == 'pass'
assert config['generation_id'] == release['generation_id']
store = Path(installed['store'])
native = store / 'generations' / config['native_generation_id']
sys.path.insert(0, str(native / 'scripts'))
from photo_h_f2_generation import Generation
import photo_recall_first as recall

generation = Generation(store, config['generation_id'], full=False)
binding = read(generation.root / 'manifest.json')['binding']
cache = read(O / 'qualification-query-evidence.json')
assert cache['binding'] == binding
queries = read(O / 'qualification-queries.frozen.json')
embeddings = {row['id']: row['embedding'] for row in cache['rows']}
cards = {row['id']: row for row in read(R / 'semantic-cards.json')}
texts = [cards[card][language] for card, language in [
    ('V01', 'positive_en'), ('V58', 'positive_en'),
    ('V75', 'positive_ko'), ('V83', 'positive_en')]]
chosen = [next(query for query in queries if query['text'] == text) for text in texts]
chosen += [next(query for query in queries if query['id'] == qid)
    for qid in ['ordinary-portrait', 'ordinary-cat']]
mapping = read(O / 'card-candidate-map.json')
new = read(O / 'new-native-records.json')
positive = {cid for cid, row in new.items() if row['record_kind'] == 'visual_option'}
diagnostic = set(new) - positive
index = generation.index()
rows = []
for query in chosen:
    embedding = embeddings[query['id']]
    recall.check_embedding(embedding, binding, query['text'], 'query')
    result = index.search(query['text'], embedding, binding)
    assert result['lane_calls'] == {'BM25F': 1, 'local_cosine': 1}
    assert result['considered_CIDs'] == installed['positive_CIDs']
    assert not diagnostic & {row['cid'] for row in result['order']}
    target = {mapping[card] for card in query['target_research_cards']}
    rank = next((i + 1 for i, row in enumerate(result['order']) if row['cid'] in target), None)
    if target:
        assert rank is not None, 'Registered positive source missing from whole pool'
    rows.append({'id': query['id'], 'query': query['text'], 'target_rank': rank,
        'new_military_at10': [row['cid'] for row in result['order'][:10] if row['cid'] in positive],
        'considered_CIDs': result['considered_CIDs']})
out = {'status': 'pass', 'generation_id': generation.id, 'cases': rows,
    'cached_query_vectors': 6, 'new_embedding_calls': 0,
    'route': 'whole_pool_operational_probe_not_managed_sampling',
    'limits': 'Six known development queries on the selected merged pool; not a repeated 262-query qualification, holdout or image-quality result.'}
(O / 'runtime-smoke.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(out, ensure_ascii=False, indent=2))
