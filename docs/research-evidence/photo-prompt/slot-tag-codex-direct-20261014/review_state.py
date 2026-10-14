"""Count explicit source judgements without promoting pending rows to approval."""

ACCEPTED = frozenset({'approved', 'diagnostic_reviewed'})
PENDING = frozenset({'needs_source_fix', 'needs_boundary_review'})


def partition(rows):
    accepted, pending, all_rows = {}, {}, {}
    for row in rows:
        cid, status = row['candidate_id'], row['status']
        if cid in all_rows:
            raise ValueError('duplicate canonical judgement')
        if status not in ACCEPTED | PENDING:
            raise ValueError('unknown review status')
        all_rows[cid] = row
        (accepted if status in ACCEPTED else pending)[cid] = row
    return accepted, pending, all_rows


def coverage(order, rows):
    accepted, pending, all_rows = partition(rows)
    if len(order) != len(set(order)) or not set(all_rows) <= set(order):
        raise ValueError('review IDs differ from canonical order')
    missing = [n for n, cid in enumerate(order) if cid not in all_rows]
    unfinished = [n for n, cid in enumerate(order) if cid not in accepted]
    return {
        'accepted': accepted, 'pending': pending, 'all': all_rows,
        'registered_source_judgements': len(all_rows),
        'accepted_source_judgements': len(accepted),
        'pending_source_judgements': len(pending),
        'unreviewed_source_records': len(missing),
        'first_unreviewed_order_offset': missing[0] if missing else len(order),
        'first_unfinished_order_offset': unfinished[0] if unfinished else len(order),
        'source_review_approval_complete': len(accepted) == len(order),
    }
