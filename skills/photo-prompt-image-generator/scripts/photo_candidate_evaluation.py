"""Known-positive recall only. Unjudged and creative false hits incur no penalty."""
from collections import defaultdict
import math


def measure(orders, pairs, k=8):
    pairs = [tuple(p) for p in pairs]
    if not pairs or len(pairs) != len(set(pairs)) or type(k) is not int or k <= 0:
        raise ValueError('unique nonempty positive population and budget required')
    groups = defaultdict(set)
    for goal, cid, rid in pairs:
        if goal not in orders:
            raise ValueError('missing evaluated goal')
        groups[goal].add(cid+'|'+rid)
    hits = {}
    retrieved = []
    for goal, positives in groups.items():
        order = orders[goal]
        if len(order) != len(set(order)):
            raise ValueError('duplicate document in returned order')
        found = positives & set(order[:k])
        hits[goal] = len(found)
        retrieved.extend((goal, value) for value in sorted(found))
    count = sum(hits.values())
    return {'positive_pairs': len(pairs), 'supported_goals': len(groups), 'retrieved_positive_pairs': count,
            'recall_at_k': count/len(pairs), 'goals_with_positive_at_k': sum(v > 0 for v in hits.values()),
            'macro_goal_recall': math.fsum(hits[g]/len(groups[g]) for g in sorted(groups))/len(groups),
            'per_goal_hits': hits, 'retrieved': [list(p) for p in sorted(retrieved)]}


def qualified(a, b, c, criteria):
    if len({v['positive_pairs'] for v in [a,b,c]}) != 1 or len({v['supported_goals'] for v in [a,b,c]}) != 1:
        raise ValueError('incomparable recall denominators')
    minimum = criteria['minimum_C']
    checks = {'recall_gain': c['retrieved_positive_pairs'] >= minimum['FIT8'],
              'goal_coverage': c['goals_with_positive_at_k'] >= minimum['goals8'],
              'data_increment': c['retrieved_positive_pairs']-b['retrieved_positive_pairs'] >= minimum['additional_FIT_vs_B']}
    return {'status': 'PASS' if all(checks.values()) else 'HOLD', 'checks': checks,
            'C_minus_A_FIT8': c['retrieved_positive_pairs']-a['retrieved_positive_pairs'],
            'C_minus_B_FIT8': c['retrieved_positive_pairs']-b['retrieved_positive_pairs'],
            'C_minus_A_recall_percentage_points': 100*(c['recall_at_k']-a['recall_at_k'])}
