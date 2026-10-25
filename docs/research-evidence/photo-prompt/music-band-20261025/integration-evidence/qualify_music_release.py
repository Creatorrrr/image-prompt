"""Reproducible whole-pool development probes, separate from image sampling."""
from pathlib import Path
import gc, hashlib, json, sys, time

gc.disable()
O = Path(__file__).resolve().parent
R = O.parent
S = R.parents[3] / 'skills/photo-prompt-image-generator'

def read(path):
    return json.loads(path.read_bytes())

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def main():
    started = time.monotonic()
    encode_only = '--encode-only' in sys.argv
    if '--active' in sys.argv:
        active = read(O / 'active-release-validation.json')
        assert active['status'] == 'pass'
        release = {'store': active['store'], **active['config']}
    elif (O / 'successor.json').exists():
        release = read(O / 'successor.json')
        assert release['status'] == 'staged_verified'
    else:
        assert encode_only
        base = read(O / 'release-base.json')
        release = {'store': base['store'], **base['config']}
    native = Path(release['store']) / 'generations' / release['native_generation_id']
    sys.path.insert(0, str(native / 'scripts'))
    from photo_h_f2_generation import Generation
    from photo_h_f2_encoder import LocalEncoder
    import photo_recall_first as rf
    queries = []
    for case in read(R / 'evaluation-cases.json'):
        for language in ('ko', 'en'):
            queries.append({'id': case['id'] + '-' + language,
                'language': language, 'text': case['query_' + language],
                'kind': 'authored_development_query',
                'target_research_cards': case['expected_research_card_ids'],
                'expected_route': case['expected_route'], 'holdout': False})
    for card in read(R / 'semantic-cards.json'):
        for language in ('ko', 'en'):
            queries.append({'id': 'literal-' + card['id'] + '-' + language,
                'language': language, 'text': card['phrase_' + language],
                'kind': 'literal_card_smoke', 'target_research_cards': [card['id']],
                'holdout': False})
    ordinary = [
        ('plant', 'A small potted plant on a quiet apartment windowsill.'),
        ('portrait', 'A close portrait beside a plain wall with soft window light.'),
        ('tea', 'A ceramic cup of tea on a wooden kitchen table.'),
        ('library', 'Two friends reading a book at a public library table.'),
        ('bicycle', 'A bicycle leaning against a brick wall after rain.'),
        ('cat', 'A sleeping cat curled on a woven blanket.')]
    queries.extend({'id': 'ordinary-' + key, 'language': 'en', 'text': text,
        'kind': 'ordinary_control', 'target_research_cards': [], 'holdout': False}
        for key, text in ordinary)
    write(O / 'qualification-queries.frozen.json', queries)
    query_sha = hashlib.sha256((O / 'qualification-queries.frozen.json').read_bytes()).hexdigest()
    binding = read(Path(release['store']) / 'h-f2-generations' /
        release['generation_id'] / 'manifest.json')['binding']
    cache = O / 'qualification-query-evidence.json'
    if cache.exists():
        encoded = read(cache)
        assert encoded['query_sha256'] == query_sha and encoded['binding'] == binding
    else:
        encoded = {'query_sha256': query_sha, 'binding': binding, 'rows': []}
        with LocalEncoder(S) as encoder:
            assert encoder.binding == binding
            for start in range(0, len(queries), 12):
                batch = queries[start:start + 12]
                for query, embedding in zip(batch,
                        encoder.encode([q['text'] for q in batch], 'query'), strict=True):
                    rf.check_embedding(embedding, binding, query['text'], 'query')
                    encoded['rows'].append({'id': query['id'], 'embedding': embedding})
                print('query embeddings', len(encoded['rows']), flush=True)
        write(cache, encoded)
    if encode_only:
        print(json.dumps({'status': 'query_embeddings_saved',
            'count': len(encoded['rows']), 'query_sha256': query_sha}), flush=True)
        return
    generation = Generation(release['store'], release['generation_id'], full=True)
    index = generation.index()
    mapping = read(O / 'card-candidate-map.json')
    new = read(O / 'new-native-records.json')
    positive = {cid for cid, row in new.items() if row['record_kind'] == 'visual_option'}
    diagnostics = set(new) - positive
    rows = []
    for query, embedding in zip(queries, encoded['rows'], strict=True):
        assert query['id'] == embedding['id']
        result = index.search(query['text'], embedding['embedding'], binding)
        assert result['lane_calls'] == {'BM25F': 1, 'local_cosine': 1}
        order = result['order']
        assert not any(row['cid'] in diagnostics for row in order)
        expected = {mapping[c] for c in query['target_research_cards']}
        ranks = {cid: next((i + 1 for i, row in enumerate(order)
            if row['cid'] == cid), None) for cid in sorted(expected)}
        observed = [rank for rank in ranks.values() if rank is not None]
        rows.append({**query, 'target_candidate_ranks': ranks,
            'target_any_rank': min(observed) if observed else None,
            'target_all_rank': max(observed) if len(observed) == len(expected) and expected else None,
            'top10': order[:10], 'new_at10': [row['cid'] for row in order[:10]
                if row['cid'] in positive], 'population': result['considered_CIDs'],
            'generation_id': generation.id,
            'route': 'whole_pool_probe_not_managed_sampling',
            'semantic_adoption': 'not_tested'})
        if len(rows) % 24 == 0:
            print('whole-pool probes', len(rows), flush=True)
    groups = {}
    for kind in ('authored_development_query', 'literal_card_smoke', 'ordinary_control'):
        group = [row for row in rows if row['kind'] == kind]
        target = [row for row in group if row['target_research_cards']]
        groups[kind] = {'count': len(group), 'with_target': len(target),
            'target_any_at8': sum(row['target_any_rank'] is not None and row['target_any_rank'] <= 8 for row in target),
            'target_any_at32': sum(row['target_any_rank'] is not None and row['target_any_rank'] <= 32 for row in target),
            'target_all_at32': sum(row['target_all_rank'] is not None and row['target_all_rank'] <= 32 for row in target),
            'new_at10_count': sum(bool(row['new_at10']) for row in group)}
    summary = {'status': 'complete', 'generation_id': generation.id,
        'query_count': len(rows), 'query_sha256': query_sha, 'groups': groups,
        'diagnostic_records_excluded_from_positive_pool': len(diagnostics),
        'baseline_search_executed': False, 'native_approval': False,
        'holdout_cases': 0, 'elapsed_seconds': time.monotonic() - started,
        'limits': 'Authored development queries and literal smoke probes. Exposure does not prove source fit, selection, image realization, causal gain, or user acceptance.'}
    write(O / 'retrieval-qualification.json', {'summary': summary, 'cases': rows})
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)

if __name__ == '__main__':
    main()
