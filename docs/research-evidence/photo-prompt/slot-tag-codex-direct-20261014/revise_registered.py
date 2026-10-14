"""Rebind explicit root rereviews while retaining the original registered rows.

This never creates a meaning, role or correction. Root must actually read the
whole affected source before supplying a replacement authored judgement.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

import direct_review as review


AUTHORED_FIELDS = frozenset({'candidate_id', 'meaning_summary', 'recommended_kind',
    'corrections', 'roles', 'facts', 'rejected_boundaries', 'uncertainties',
    'status', 'all_roles_considered'})


def replace_row(old, decision, authored_path, item, data):
    if set(decision) != AUTHORED_FIELDS or decision['candidate_id'] != old['candidate_id']:
        raise ValueError('replacement must explicitly judge the same canonical candidate')
    result = copy.deepcopy(old)
    result.pop('review_provenance', None)
    result.update(copy.deepcopy(decision), schema=review.SCHEMA,
        review_method='codex_direct_source_read', reviewer='Codex', independent_human_review=False,
        authored_decision={'file': str(authored_path.relative_to(review.ROOT)),
                          'item': item, 'sha256': review.c.digest(decision)})
    review.validate_decision(result, data)
    return result


def apply(authored_path, manifest_path):
    authored_path = review.run_path(str(authored_path), 'authored')
    manifest_path = Path(manifest_path).resolve()
    if not manifest_path.is_relative_to(review.HERE):
        raise ValueError('revision manifest must stay in this evidence run')
    authored = json.loads(authored_path.read_text())['decisions']
    manifest = json.loads(manifest_path.read_text())
    if (manifest['root_directly_reread_complete_sources'] is not True
            or not manifest['reason'] or len(authored) != len(manifest['replacements'])
            or len({row['candidate_id'] for row in authored}) != len(authored)):
        raise ValueError('explicit root reread attestation and unique replacements required')
    review.verify()
    data = review.source()
    by_id = {row['candidate_id']: (number, row) for number, row in enumerate(authored, 1)}
    selected = {row['candidate_id']: row for row in manifest['replacements']}
    if set(by_id) != set(selected):
        raise ValueError('manifest and authored replacement IDs disagree')
    originals, documents, changes = {}, {}, []
    for path in sorted((review.HERE / 'decisions').glob('*.json')):
        document = json.loads(path.read_text())
        for offset, old in enumerate(document['decisions']):
            cid = old['candidate_id']
            if cid not in selected:
                continue
            if any(change['candidate_id'] == cid for change in changes):
                raise ValueError('duplicate existing canonical judgement')
            if review.c.digest(old) != selected[cid]['before_registered_row_sha256']:
                raise ValueError('registered source judgement changed before revision')
            number, decision = by_id[cid]
            new = replace_row(old, decision, authored_path, number, data)
            originals.setdefault(path, path.read_bytes())
            documents.setdefault(path, document)['decisions'][offset] = new
            changes.append({'candidate_id': cid, 'registered_file': str(path.relative_to(review.ROOT)),
                'before': old, 'after': new, 'before_sha256': review.c.digest(old),
                'after_sha256': review.c.digest(new)})
    if {change['candidate_id'] for change in changes} != set(selected):
        raise ValueError('replacement ID is not registered')
    archive = review.HERE / 'revisions' / manifest_path.stem
    if archive.exists():
        raise ValueError('revision history already exists; never overwrite it')
    archive.mkdir(parents=True)
    for path, body in originals.items():
        (archive / path.name).write_bytes(body)
    audit = {'schema': 'photo-codex-root-rereview-revision/v1',
        'root_all_worker_sources_read_claimed': False,
        'root_directly_reread_complete_sources': True, 'reason': manifest['reason'],
        'manifest_file': str(manifest_path.relative_to(review.ROOT)),
        'authored_file': str(authored_path.relative_to(review.ROOT)),
        'archive_hashes': {path.name: hashlib.sha256(body).hexdigest() for path, body in originals.items()},
        'changes': changes, 'native_changes_applied': False, 'stage05_complete': False}
    review.write(archive / 'REVISION.json', audit)
    try:
        for path, document in documents.items():
            review.write(path, document)
        result = review.verify()
    except Exception:
        for path, body in originals.items():
            path.write_bytes(body)
        review.verify()
        raise
    review.write(archive / 'AFTER-VERIFICATION.json', result)
    return {'revised': len(changes), 'archive': str(archive.relative_to(review.ROOT)),
            'registered_files': [str(path.relative_to(review.ROOT)) for path in documents],
            'progress': result}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--authored', required=True)
    parser.add_argument('--manifest', required=True)
    args = parser.parse_args()
    print(json.dumps(apply(args.authored, args.manifest), ensure_ascii=False))
