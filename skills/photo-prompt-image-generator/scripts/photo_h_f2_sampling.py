"""One reproducible, uniform sample per H-F2 query after source-scope projection."""
import random
import photo_candidate_corpus as corpus

SCHEMA = 'photo-h-f2-sampling/v1'
WINDOWS = ((8, 4), (32, 8), (96, 12), (256, 16))


def policy(creativity):
    if type(creativity) is not int or not 0 <= creativity <= 3:
        raise ValueError('creativity must be an integer in 0..3')
    window, maximum = WINDOWS[creativity]
    return {'schema': SCHEMA, 'creativity': creativity,
            'rank_window': window, 'sample_limit': maximum,
            'algorithm': 'uniform_without_replacement', 'budget_scope': 'per_query'}


def sample(rows, creativity, seed, query_id, query_sha256):
    if type(seed) is not int or not 0 <= seed < 2**128:
        raise ValueError('sampling_seed must be an unsigned 128-bit integer')
    if not isinstance(query_id, str) or not query_id or not isinstance(query_sha256, str) or len(query_sha256) != 64:
        raise ValueError('exact query identity and hash required')
    settings = policy(creativity)
    unique = {}
    for row in rows:
        unique.setdefault(row['cid'], row)
    window = list(unique.values())[:settings['rank_window']]
    material = {'policy': settings, 'sampling_seed': seed,
                'query_id': query_id, 'query_sha256': query_sha256}
    scoped_seed = corpus.digest(material)
    rng = random.Random(int(scoped_seed, 16))
    chosen = rng.sample(window, min(settings['sample_limit'], len(window)))
    evidence = {**settings, 'seed_scope_sha256': scoped_seed,
                'window_ids': [row['id'] for row in window],
                'window_sha256': corpus.digest(window),
                'available': len(window), 'returned': len(chosen),
                'selected_ids': [row['id'] for row in chosen]}
    return chosen, evidence


def candidates(goal):
    """Read current sampled material and preserved historical top8 records."""
    return goal['candidates'] if 'candidates' in goal else goal['top8']
