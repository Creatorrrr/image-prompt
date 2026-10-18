"""Freeze source-only strata and existing evaluation before new scores exist."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
E = Path(__file__).parent
S = ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0, str(S/'scripts'))
from photo_candidate_authoring import Source, read, write, digest, file_sha

assert not (E/'FREEZE.json').exists(), 'never overwrite a frozen experiment'
source = Source(S/'candidate-authoring/v1')
prior = Path('/Users/chasoik/.codex/worktrees/slot-search-relevance/image-prompt/docs/research-evidence/photo-prompt')
evaluation = read(prior/'d1-s-full-corpus-execution-20261018/EVALUATION-MANIFEST.json')
labels = read(prior/'d1-s-full-corpus-execution-20261018/LABEL-REUSE.json')
queries = read(prior/'d1-s-query-rrf-field-ablation-20261018/QUERIES.json')
assert len(labels['eligible']) == 671 and len(evaluation['positive_pairs']) == 126 and len(queries['goals']) == 67
mapped = Counter()
for row in labels['eligible']:
    record = source.record(row['cid']);rid = row['rid']
    assert rid in record['meaning']['primary']
    assert row['source_sha256'] in {digest(record), record['meaning']['origin']['source_record_sha256']}, row['cid']
    units = {p: record['meaning']['literals'][uid] for p, uid in record['meaning']['evidence'][rid].items()}
    for quote in row['label']['decision']['source_quotes']:
        actual = units[quote['pointer']]
        assert quote['quote'] in actual, (row['cid'], quote['pointer'])
        mapped['exact' if actual == quote['quote'] else 'substring'] += 1
write(E/'baseline/LABELS.json.gz', labels)
write(E/'baseline/EVALUATION.json', evaluation)
write(E/'baseline/QUERIES.json.gz', {'binding': queries['binding'], 'goals': {
    key: {'text': value['historical']['text'], 'row': value['historical']['row'],
          'goal_sha256': value['goal_sha256']} for key, value in queries['goals'].items()}})
fresh = Path.home()/'.cache/image-prompt/h-f2-default-install-20261018/parity-inputs'
for name in ['GOALS.json', 'QUERIES.json', 'JUDGMENTS.json', 'TOP8.json']:
    write(E/'baseline'/('FRESH-'+name+'.gz'), read(fresh/name))

quotas = {'visual_option': 48, 'visual_profile': 24, 'visual_bundle': 12,
          'relationship_mechanism': 6, 'relationship_concept': 3, 'diagnostic': 3}
positive_cids = {p[1] for p in evaluation['positive_pairs']}
selected = {}
seed = 'candidate-semantic-renewal-20261018-v1'

def order(cid):
    return hashlib.sha256((seed+'|'+cid).encode()).hexdigest()

for kind, count in quotas.items():
    candidates = [cid for cid, row in source.metadata.items() if row['record_kind'] == kind]
    chosen = [cid for cid in sorted(candidates, key=order) if source.metadata[cid]['existing_graph']]
    for cid in chosen:
        selected[cid] = 'existing_reviewed_graph'
    target = min(count, max(len(chosen), int(count*.75)))
    for cid in sorted(candidates, key=order):
        if len(chosen) >= target:
            break
        if cid in positive_cids and cid not in chosen:
            chosen.append(cid);selected[cid] = 'existing_known_positive'
    for cid in sorted(candidates, key=order):
        if len(chosen) >= count:
            break
        if cid not in chosen:
            chosen.append(cid);selected[cid] = 'fixed_seed_stratum_sample'
    assert len(chosen) == count
assert len(selected) == 96
write(E/'PILOT.json', {'schema': 'photo-source-review-pilot/v1', 'seed': seed,
    'quotas': quotas, 'candidates': {cid: {**source.metadata[cid], 'selection': selected[cid]} for cid in sorted(selected)},
    'known_positive_CIDs': len(set(selected)&positive_cids),
    'existing_graphs': sum(source.metadata[cid]['existing_graph'] for cid in selected),
    'new_scores_seen': False})

def decode(value, pool):
    if isinstance(value, dict):
        if set(value) == {'$literal'}:
            return pool[value['$literal']]
        return {k: decode(v, pool) for k, v in value.items() if not k.startswith('_')}
    if isinstance(value, list):
        return [decode(v, pool) for v in value]
    return value

catalog = {key: {k: row[k] for k in ['id', 'description', 'description_ko', 'includes', 'excludes']}
           for key, row in source.header['slot_catalog'].items()}
packets = [[] for _ in range(4)]
for i, cid in enumerate(sorted(selected, key=lambda cid: (source.metadata[cid]['record_kind'], order(cid)))):
    record = source.record(cid);m = record['meaning']
    packets[i%4].append({'candidate_id': cid, 'source_sha256': digest(record), 'record_kind': record['record_kind'],
        'retrieval_class': m['retrieval_class'], 'native_contract': decode(record['native']['tree'], m['literals']),
        'primary_units': {rid: {p: m['literals'][uid] for p, uid in units.items()} for rid, units in m['primary'].items()},
        'conditions': record['conditions'], 'effects': record['effects']})
for i, packet in enumerate(packets):
    write(E/'review-inputs'/('batch-%02d.json' % (i+1)), {'schema': 'photo-source-only-review-input/v1',
        'candidate_count': len(packet), 'catalog': catalog, 'candidates': packet,
        'no_queries_labels_or_rankings': True})
write(E/'CRITERIA.json', {'schema': 'photo-source-renewal-criteria/v1', 'K': 8, 'positive_pairs': 126,
    'supported_goals': 40, 'all_queries': 67, 'expected_baseline': {'FIT8': 55, 'goals8': 28},
    'minimum_C': {'FIT8': 62, 'goals8': 28, 'additional_FIT_vs_B': 1},
    'precision_is_not_a_gate': True, 'unjudged_is_not_negative': True,
    'score_policy': 'whole positive pool;H-only;F2 weights/normalization;RRF10;one lane each;CID dedup;actual RID;top8',
    'pilot_CIDs': 96, 'full_rollout_only_if_pilot_passes': True, 'CURRENT': 'unchanged', 'Gemini_calls': 0,
    'source_quote_mapping': dict(mapped), 'new_scores_seen': False})
files = [E/'PILOT.json', E/'CRITERIA.json', *sorted((E/'baseline').glob('*')),
         *sorted((E/'review-inputs').glob('*')), ROOT/'docs/plans/candidate-semantic-renewal.md',
         S/'scripts/photo_candidate_review.py', S/'scripts/photo_candidate_documents.py',
         S/'candidate-authoring/v1/manifest.json', S/'retrieval-runtime.json']
write(E/'FREEZE.json', {'files': {str(p.relative_to(ROOT)): file_sha(p) for p in files},
    'pilot_source_only': True, 'new_scores_seen': False})
print(json.dumps({'status': 'PASS', 'pilot_CIDs': 96, 'label_rows': 671,
    'source_quote_mapping': dict(mapped), 'known_positive_CIDs': len(set(selected)&positive_cids),
    'existing_graphs': sum(source.metadata[cid]['existing_graph'] for cid in selected), 'packets': [len(p) for p in packets]}, ensure_ascii=False))
