"""Reproduce frozen baseline, rejected full proposal, and accepted subset offline.

Uses only committed baseline shards and the exact recorded vector cache. This
runner has no API branch and never changes source or index files. The original
evaluate_cycle.py remains the historical bounded full-proposal evaluator.
"""
from pathlib import Path
import argparse
import copy
import gzip
import hashlib
import json
import math
import sys
import tempfile

R = Path(__file__).resolve().parents[4]
A = R / 'skills/photo-prompt-image-generator/assets'
E = Path(__file__).resolve().parent
sys.path.insert(0, str(A.parent / 'scripts'))
import prompt_generator as g
from bm25f_retrieval import rank_bm25f


def materialize_index(data, baseline, cache):
    bm = g.build_semantic_bm25f_payload(data)
    entries = {}
    for key, kind, entry, slot in g.iter_semantic_entries(data):
        text = g.semantic_text_for_entry(entry, slot, kind=kind)
        if text == baseline['entries'][key]['text']:
            vector = baseline['entries'][key]['vector']
        else:
            record = cache[hashlib.sha256(text.encode()).hexdigest()]
            assert record['text'] == text and record['model'] == g.SEMANTIC_MODEL_ID
            assert record['dimensions'] == 768 and len(record['vector']) == 768
            vector = record['vector']
        entries[key] = {'kind': kind, 'slot': slot, 'id': entry['id'], 'text': text,
                        'vector': vector, 'bm25f_document': bm['documents'][key]}
    index = {'provider': g.SEMANTIC_PROVIDER, 'dictionary_hash': g.dictionary_hash(data),
             'semantic_text_recipe': g.SEMANTIC_TEXT_RECIPE_VERSION, 'embedding_model': g.SEMANTIC_MODEL_ID,
             'embedding_dimensions': 768, 'bm25f': {k: v for k, v in bm.items() if k != 'documents'}, 'entries': entries}
    g.validate_semantic_index_metadata(index, data)
    return index


def cosine(a, b):
    return sum(x*y for x, y in zip(a, b)) / (math.sqrt(sum(x*x for x in a)) * math.sqrt(sum(x*x for x in b)))


def replay_results(data, index, cache, queries, suffix):
    bm = g.semantic_bm25f_payload_from_index(index)
    dense, lexical = [], []
    for q in queries:
        record = cache[hashlib.sha256(q['query'].encode()).hexdigest()]
        assert record['text'] == q['query'] and record['model'] == g.SEMANTIC_MODEL_ID
        allowed = ['slot:' + q['slot'] + ':' + row['id'] for row in data['slots'][q['slot']]]
        scores = [{'id': key, 'score': round(cosine(record['vector'], index['entries'][key]['vector']), 12)} for key in allowed]
        scores.sort(key=lambda x: (-x['score'], x['id']))
        rank = next(i for i, row in enumerate(scores, 1) if row['id'] == q['target'])
        dense.append({**q, 'rank': rank, 'corpus_size': len(allowed), 'target_score': scores[rank-1]['score'], 'top5': scores[:5]})
        scores = rank_bm25f(bm, {'query': q['query']}, allowed_ids=allowed, limit=len(allowed))
        rank = next((i for i, row in enumerate(scores, 1) if row['document_id'] == q['target']), None)
        lexical.append({**q, 'rank': rank, 'corpus_size': len(allowed), 'top5': scores[:5]})
    for method, rows in [('dense', dense), ('lexical', lexical)]:
        assert json.loads((E / (method + '-' + suffix + '.json')).read_text()) == rows, (method, suffix)
    return len(dense) + len(lexical)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true', help='Compatibility spelling; every run is offline replay')
    parser.parse_args()
    freeze_bytes = (E / 'frozen-inventory-queries.json').read_bytes()
    assert hashlib.sha256(freeze_bytes).hexdigest() == '91b7ee50643c05af5370eff930808f55f18cff974a17b2e96d4ba30d8aa59d58'
    freeze = json.loads(freeze_bytes)
    decision_bytes = (E / 'acceptance-decisions.json').read_bytes()
    assert hashlib.sha256(decision_bytes).hexdigest() == (E / 'acceptance-sha256.txt').read_text().split()[0]
    decision = json.loads(decision_bytes)
    accepted_ids = set(decision['accepted_ids'])
    assert accepted_ids == {'spirit_jurisdiction_narrative_core'}
    baseline_data = json.loads(gzip.decompress((E / 'baseline-merged-data.json.gz').read_bytes()))
    assert g.dictionary_hash(baseline_data) == freeze['baseline_dictionary_hash']
    with tempfile.NamedTemporaryFile(dir=A, suffix='.json', delete=False) as f:
        path = Path(f.name)
        f.write((E / 'baseline-index-manifest.json').read_bytes())
    try:
        baseline_index = g.load_semantic_index(path, baseline_data)
    finally:
        path.unlink()
    cache = json.loads((E / 'new-vector-cache.json').read_text())
    attempts = json.loads((E / 'api-attempts.json').read_text())
    assert len(attempts) == 25 and all(row['status'] == 'completed' for row in attempts)
    assert len({row['sha256'] for row in attempts}) == 25
    assert sum(len(cache[row['sha256']]['text'].encode()) for row in attempts) == 9282
    full_data, accepted_data = copy.deepcopy(baseline_data), copy.deepcopy(baseline_data)
    for item in freeze['inventory']:
        for data, apply in [(full_data, True), (accepted_data, item['id'] in accepted_ids)]:
            rows = data['slots'][item['slot']]
            i = next(i for i, row in enumerate(rows) if row['id'] == item['id'])
            assert rows[i] == item['before']
            if apply:
                rows[i] = copy.deepcopy(item['proposed_after'])
    current_data = g.load_json(A / 'photo_prompt_tags.json')
    assert current_data == accepted_data, 'Current source must equal only the hash-bound accepted subset'
    full_index = materialize_index(full_data, baseline_index, cache)
    accepted_index = materialize_index(accepted_data, baseline_index, cache)
    assert full_index['dictionary_hash'] == json.loads((E / 'full-proposal-index-manifest.json').read_text())['dictionary_hash']
    assert accepted_index['dictionary_hash'] == decision['accepted_dictionary_hash']
    actual = g.load_semantic_index(A / 'photo_prompt_semantic_index.json', current_data)
    assert actual['entries'] == accepted_index['entries']
    assert sum(row['vector'] == baseline_index['entries'][key]['vector'] for key, row in actual['entries'].items()) == 10173
    count = 0
    for data, index, suffix in [(baseline_data, baseline_index, 'baseline'), (full_data, full_index, 'full-proposal'), (accepted_data, accepted_index, 'final')]:
        count += replay_results(data, index, cache, freeze['queries'], suffix)
    assert count == 132
    print('Verified all 132 frozen result rows, full rejected proposal and accepted physical index; zero API calls')


if __name__ == '__main__':
    main()
