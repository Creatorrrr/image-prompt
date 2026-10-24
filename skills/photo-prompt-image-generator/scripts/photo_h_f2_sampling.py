"""Retain the best eligible source and sample diversity once per H-F2 query."""
import random
import photo_candidate_corpus as corpus

SCHEMA = 'photo-h-f2-sampling/v2'
WINDOWS = ((8, 4), (32, 8), (96, 12), (256, 16))


def policy(creativity):
    if type(creativity) is not int or not 0 <= creativity <= 3:
        raise ValueError('creativity must be an integer in 0..3')
    window, maximum = WINDOWS[creativity]
    return {'schema': SCHEMA, 'creativity': creativity,
            'rank_window': window, 'sample_limit': maximum,
            'algorithm': 'rank_anchor_plus_uniform_without_replacement',
            'anchor_limit': 1, 'budget_scope': 'per_query'}


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
    # Source-scope projection has already determined eligibility. Retain that
    # first ranked source without consulting its CID, origin, age or topic.
    # Diversity uses only the remaining positions and the same total budget.
    anchor = window[:1]
    chosen = anchor + rng.sample(window[1:], min(settings['sample_limit'] - len(anchor), max(0, len(window) - 1)))
    evidence = {**settings, 'seed_scope_sha256': scoped_seed,
                'window_ids': [row['id'] for row in window],
                'window_sha256': corpus.digest(window),
                'available': len(window), 'returned': len(chosen),
                'anchor_ids': [row['id'] for row in anchor],
                'selected_ids': [row['id'] for row in chosen]}
    return chosen, evidence


def candidates(goal):
    """Read current sampled material and preserved historical top8 records."""
    return goal['candidates'] if 'candidates' in goal else goal['top8']
