"""Recompute a management-batch report from validated, authored decisions only."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

import direct_review as review
from review_state import partition


def validate_coverage(order, rows, start, stop, expected_total, *, allow_sparse=False):
    if len(rows) != expected_total or not set(rows) <= set(order):
        raise ValueError('coverage count or canonical IDs do not match')
    if not 0 <= start < stop <= len(order) or not set(order[start:stop]) <= set(rows):
        raise ValueError('requested batch contains unreviewed IDs')
    prefix = next((n for n, cid in enumerate(order) if cid not in rows), len(order))
    if not allow_sparse and prefix != expected_total:
        raise ValueError('coverage does not match the explicitly reviewed order')
    return prefix


def summarize(start, stop, expected_total, *, allow_sparse=False):
    progress = review.verify()
    if (progress['direct_approved_records'] != expected_total
            or progress['pending_decisions'] and not allow_sparse):
        raise ValueError('unexpected coverage or unresolved source decisions')
    baseline = json.loads((review.HERE / 'BASELINE.json').read_text())
    frozen = review.source()
    current = review.c.load(review.SKILL / 'assets')
    if review.c.digest(current) != baseline['source_sha256']:
        raise ValueError('native source changed; ledger-only reporting is invalid')
    order = json.loads((review.HERE / 'ORDER.json').read_text())
    source_rows = []
    for path in sorted((review.HERE / 'decisions').glob('*.json')):
        for row in json.loads(path.read_text())['decisions']:
            source_rows.append(row)
    rows, pending, all_rows = partition(source_rows)
    prefix = validate_coverage(order, rows, start, stop, expected_total, allow_sparse=allow_sparse)
    previous = defaultdict(set)
    for binding in frozen['slot_bindings'].values():
        previous[binding['candidate_id']].add(binding['slot_id'])
    proposals, roles, links, kind_changes = [], Counter(), Counter(), []
    for cid in order[start:stop]:
        row = rows[cid]
        if row['status'] not in {'approved', 'diagnostic_reviewed'}:
            raise ValueError('batch contains unresolved judgement')
        tags = {role['slot_id'] for role in row['roles']}
        if len(tags) != len(row['roles']):
            raise ValueError('duplicate proposed relationship')
        roles.update(tags)
        proposal = {'candidate_id': cid,
            'retain': sorted(tags & previous[cid]), 'add': sorted(tags - previous[cid]),
            'remove': sorted(previous[cid] - tags), 'corrections': row['corrections']}
        original_kind = frozen['candidates'][cid]['record_kind']
        if row['recommended_kind'] != original_kind:
            change = {'candidate_id': cid, 'before': original_kind,
                      'after': row['recommended_kind'], 'reason': row['meaning_summary']}
            proposal['record_kind_change'] = change
            kind_changes.append(change)
        proposals.append(proposal)
        links.update({key: len(proposal[key]) for key in ('retain', 'add', 'remove')})
    defaults = json.loads((review.SKILL / 'embedding-default.json').read_text())
    index = json.loads((review.SKILL / 'assets/photo_candidate_search.json').read_text())
    if defaults['space'] != baseline['space'] or index['space'] != baseline['space']:
        raise ValueError('embedding space drifted')
    if index['layout_id'] != baseline['layout_id']:
        raise ValueError('active index changed during source review')
    protected = {
        'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':
            'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359',
        'docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':
            '0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b',
    }
    for path, digest in protected.items():
        if hashlib.sha256((review.ROOT / path).read_bytes()).hexdigest() != digest:
            raise ValueError('protected concurrent work changed')
    issues = json.loads((review.HERE / 'NATIVE-QUALIFICATION-ISSUES.json').read_text())
    count = stop - start
    summary = {'schema': 'photo-codex-direct-batch-summary/v1',
        'range_start': start, 'range_stop': stop, 'source_records_directly_read': count,
        'direct_semantic_decisions': count, 'native_qualified_records_claimed': 0,
        'native_tags_applied': False, 'source_corrections_applied': False,
        'source_unchanged': True, 'role_proposals': sum(roles.values()),
        'role_distribution': dict(sorted(roles.items())),
        'single_role_records': sum(len(rows[cid]['roles']) == 1 for cid in order[start:stop]),
        'multiple_role_records': sum(len(rows[cid]['roles']) > 1 for cid in order[start:stop]),
        'records_with_text_correction_proposals': sum(bool(x['corrections']) for x in proposals),
        'text_field_correction_proposals': sum(len(x['corrections']) for x in proposals),
        'relationship_proposals': dict(links), 'source_sha256': baseline['source_sha256'],
        'external_model_calls': 0, 'local_embedding_inferences': 0,
        'cumulative_direct_semantic_records': expected_total,
        'remaining_unreviewed_records': progress['unreviewed_records'],
        'stage05_complete': False, 'stages06_08_complete': False}
    verification = {'schema': 'photo-direct-batch-verification/v1',
        'source_range': [start, stop], 'source_and_references_bound': True,
        'decisions_match_order_exactly': True,
        'authored_items_packet_hashes_and_positive_quotes_valid': True,
        'direct_semantic_records': count, 'role_proposals': sum(roles.values()),
        'text_correction_fields_proposed': summary['text_field_correction_proposals'],
        'duplicate_decisions': 0, 'unresolved_semantic_decisions': 0,
        'open_native_qualification_issues': sum(x['status'] == 'open' for x in issues['issues']),
        'native_role_qualification_complete': False,
        'native_sources_and_bindings_unchanged': True, 'protected_documents_unchanged': True,
        'external_model_calls': 0, 'local_embedding_inferences': 0,
        'stage05_complete': False, 'stages06_08_complete': False,
        'remaining_unreviewed': progress['unreviewed_records'], 'next_order_offset': expected_total}
    if pending:
        summary['cumulative_pending_source_judgements'] = len(pending)
        verification['cumulative_pending_source_judgements'] = len(pending)
    if kind_changes:
        summary['record_kind_change_proposals'] = kind_changes
        summary['reviewed_diagnostic_records'] = sum(
            rows[cid]['recommended_kind'] == 'diagnostic' for cid in order[start:stop])
        summary['reviewed_positive_records'] = count - summary['reviewed_diagnostic_records']
        verification['record_kind_changes_proposed'] = len(kind_changes)
        verification['record_kind_changes_applied'] = False
    if allow_sparse or any(row['review_method'] != 'codex_direct_source_read' for row in rows.values()):
        summary['batch_review_methods'] = dict(Counter(rows[cid]['review_method'] for cid in order[start:stop]))
        summary['cumulative_review_methods'] = dict(Counter(row['review_method'] for row in rows.values()))
        summary['contiguous_reviewed_prefix'] = prefix
        summary['coverage_is_contiguous_prefix'] = prefix == expected_total
        summary['root_personally_read_all_worker_sources_claimed'] = False
        verification['next_order_offset'] = prefix
        verification['coverage_is_contiguous_prefix'] = prefix == expected_total
        verification['worker_attribution_and_note_hashes_valid'] = True
    stem = f'{start:05d}-{stop:05d}'
    for name, value in [(f'BATCH-{stem}-SUMMARY.json', summary),
                        (f'BATCH-{stem}-CHANGE-PROPOSALS.json', proposals),
                        (f'STAGE05B-{stem}-VERIFICATION.json', verification)]:
        path = review.HERE / name
        if path.exists() and json.loads(path.read_text()) != value:
            raise ValueError('existing batch report differs; preserve its history explicitly')
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, required=True)
    parser.add_argument('--stop', type=int, required=True)
    parser.add_argument('--expected-total', type=int, required=True)
    parser.add_argument('--allow-sparse', action='store_true')
    args = parser.parse_args()
    print(json.dumps(summarize(args.start, args.stop, args.expected_total,
                               allow_sparse=args.allow_sparse), ensure_ascii=False))
