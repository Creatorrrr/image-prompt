"""Root-only mechanical application of immutable, sparse worker amendments.

No source-reading claim is created for root. Normalization describes existing
worker attestations; it cannot grant a new approval, range or source reading.
No provider, network, git or canonical-asset writes are performed.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

MANIFEST_SCHEMA = 'photo-codex-sparse-amendment-normalization/v1'
PROVENANCE_SCHEMA = 'photo-codex-sparse-amendment-provenance/v1'
FIELDS = frozenset({'candidate_id', 'meaning_summary', 'recommended_kind', 'corrections',
    'roles', 'facts', 'rejected_boundaries', 'uncertainties', 'status', 'all_roles_considered'})
APPROVED = {'approved', 'diagnostic_reviewed'}


def read(review, path):
    return review.c.decode(path.read_bytes())


def link(review, path):
    return {'file': str(path.relative_to(review.ROOT)), 'sha256': review.c.digest(read(review, path))}


def checked_link(review, value, directory):
    if not isinstance(value, dict) or set(value) != {'file', 'sha256'}:
        raise ValueError('exact artifact link required')
    path = review.run_path(value['file'], directory)
    if link(review, path) != value:
        raise ValueError('amendment artifact changed after normalization')
    return path


def assignment(review, note, ordinal):
    registry = read(review, review.HERE / 'DELEGATION-ASSIGNMENTS.json')
    task = note['task_name']
    if note.get('agent_id') != (task if task.startswith('/') else '/root/' + task):
        raise ValueError('worker agent and task identity disagree')
    candidates = [(key, value) for key, value in registry['assignments'].items()
        if task in {value['task_name'], value['task_name'].rsplit('/', 1)[-1]}
        and value['start'] <= ordinal < value['stop']
        and not any(t['from_assignment'] == key and t['start'] <= ordinal < t['stop']
                    for t in registry.get('reassignments', []))]
    if len(candidates) != 1:
        raise ValueError('worker has no unique active assignment; transfers cannot be reused')
    key, value = candidates[0]
    if (note['model'] != value['model'] or note['model'] != 'gpt-6.1-sol'
            or note['reasoning_effort'] != value['reasoning_effort']
            or note['reasoning_effort'] != 'high'):
        raise ValueError('worker model/high assignment mismatch')
    return {'assignment_id': key, 'task_name': value['task_name'], 'model': value['model'],
            'reasoning_effort': value['reasoning_effort'], 'assignment_sha256': review.c.digest(value)}


def authored_tuple(review, file, cid, sha):
    path = review.run_path(file, 'authored')
    document = read(review, path)
    count = len(document['decisions'] if 'decisions' in document else document['amendments'])
    matches = [(n, review.authored_item(document, n)) for n in range(1, count + 1)
               if review.authored_item(document, n)['candidate_id'] == cid]
    if len(matches) != 1 or review.c.digest(matches[0][1]) != sha:
        raise ValueError('original authored item changed or is not unique')
    return {'file': str(path.relative_to(review.ROOT)), 'item': matches[0][0], 'sha256': sha}


def packet_binding(review, path, data, cid, *, cache=None):
    path = review.run_path(str(path), 'packets')
    if cache is None:
        cache = {}
    if path in cache:
        packet, result = cache[path]
        if cid not in packet['ids']:
            raise ValueError('complete source packet does not include amended CID')
        return result
    packet = read(review, path)
    if 'source_sha256' not in cache:
        cache['source_sha256'] = review.c.digest(data)
    if (packet['source_sha256'] != cache['source_sha256']
            or packet['catalog_sha256'] != review.c.digest(data['slot_catalog'])
            or len(packet['ids']) != len(set(packet['ids']))
            or set(packet['records']) != set(packet['ids'])
            or set(packet['references']) != set(packet['ids']) or cid not in packet['ids']):
        raise ValueError('complete source packet identity differs')
    # Every record in the full packet, not just the amended CID, is bound.
    for item in packet['ids']:
        if (packet['records'][item] != data['candidates'][item]
                or packet['references'][item] != review.closure(data, item)):
            raise ValueError('complete source packet or reference closure changed')
    result = link(review, path)
    cache[path] = packet, result
    return result


def exact_references(review, value):
    """Identity bookkeeping includes temporary explicit presentation bindings."""
    if isinstance(value, str) and (review.c.ID.fullmatch(value) or review.c.BINDING_ID.fullmatch(value)):
        return {value}
    if isinstance(value, dict):
        return set().union(*(exact_references(review, item) for pair in value.items() for item in pair)) if value else set()
    if isinstance(value, list):
        return set().union(*(exact_references(review, item) for item in value)) if value else set()
    return set()


def wrapper_attestation(note, entries):
    """Read explicitly authored note metadata; never manufacture a status.

    The later corrected-source format records exact reread bindings per row
    and explicit status_counts instead of three redundant summary lists.
    Both representations remain immutable and conflicting aliases fail.
    """
    if 'reread_ids' in note:
        return (note['reread_ids'], note['unresolved_ordinals'],
                note['approved_count'], note['still_pending_count'],
                note['approved_ordinals'], None)
    bindings = note.get('reread_candidates')
    if (note.get('complete_corrected_source_read') is not True
            or not isinstance(bindings, list) or len(bindings) != len(entries)
            or any(key in note for key in ('approved_count', 'still_pending_count', 'approved_ordinals'))):
        raise ValueError('explicit corrected-source reread bindings and counts required')
    counts = {}
    for binding, entry in zip(bindings, entries):
        for key in ('candidate_id', 'ordinal', 'reread_id', 'before_authored_row_sha256',
                    'source_record_sha256', 'after_proposal_sha256', 'role_spec_sha256',
                    'reference_sha256'):
            if key not in binding or key not in entry or binding[key] != entry[key]:
                raise ValueError('per-row note/document reread binding differs')
        if (entry.get('full_corrected_source_reread') is not True
                or not isinstance(entry.get('full_after_proposal_record'), dict)):
            raise ValueError('explicit complete corrected source reread required')
        status = entry['decision']['status']
        counts[status] = counts.get(status, 0) + 1
    if note.get('status_counts') != counts:
        raise ValueError('explicit worker status counts differ from authored statuses')
    approved = [entry['ordinal'] for entry in entries if entry['decision']['status'] in APPROVED]
    pending = [entry['ordinal'] for entry in entries if entry['decision']['status'] not in APPROVED]
    if sorted(note.get('unresolved_ordinals', [])) != sorted(pending):
        raise ValueError('explicit unresolved ordinal list differs')
    return ([entry['reread_id'] for entry in bindings], pending,
            len(approved), len(pending), approved,
            'root_verified_worker_per_row_reread_bindings_and_explicit_status_counts')


def origins(review, authored_path, note_path, data):
    """Interpret only the two frozen explicit worker formats, without rewriting."""
    authored_path = review.run_path(str(authored_path), 'authored')
    note_path = review.run_path(str(note_path), 'worker-notes')
    document, note = read(review, authored_path), read(review, note_path)
    if authored_path not in {review.run_path(v, 'authored') for v in note['authored_paths']}:
        raise ValueError('amendment authored document is not worker-attested')
    for name, expected in note.get('authored_file_sha256', {}).items():
        if hashlib.sha256(review.run_path(name, 'authored').read_bytes()).hexdigest() != expected:
            raise ValueError('frozen worker authored file changed')
    order = read(review, review.HERE / 'ORDER.json')
    result, packet_cache = [], {}
    if 'bindings' in note and 'decisions' in document and 'packet_path' not in note:
        # Later sparse rereviews bind the previous immutable authored items.
        # Root resolves the unchanged prior source packet; the note itself is
        # never rewritten to pretend it declared a packet file/hash.
        if (note.get('complete_source_reread') is not True or note.get('final_ready') is not True
                or note['source_snapshot_sha256'] != review.c.digest(data)
                or note['catalog_sha256'] != review.c.digest(data['slot_catalog'])):
            raise ValueError('explicit final full reread/source binding required')
        prior_path = review.run_path(note['before_authored_file'], 'authored')
        if review.c.digest(read(review, prior_path)) != note['before_authored_document_sha256']:
            raise ValueError('previous immutable authored document changed')
        decisions, entries = document['decisions'], note['bindings']
        if ([d['candidate_id'] for d in decisions] != note['directly_reread_ids']
                or [e['candidate_id'] for e in entries] != note['directly_reread_ids']
                or [e['ordinal'] for e in entries] != note['directly_reread_ordinals']):
            raise ValueError('exact sparse reread IDs/ordinals disagree')
        existing = compiled_rows(review)
        packets = {review.c.digest(read(review, p)): p for p in (review.HERE / 'packets').glob('*.json')}
        for n, (decision, entry) in enumerate(zip(decisions, entries), 1):
            cid = decision['candidate_id']
            previous = authored_tuple(review, entry['before_authored_file'], cid, entry['before_authored_row_sha256'])
            if (entry['before_authored_file'] != note['before_authored_file']
                    or previous['item'] != entry['before_authored_item']
                    or entry['proposed_decision_sha256'] != review.c.digest(decision)
                    or any(entry[k] != v for k, v in review.binding(data, cid).items())):
                raise ValueError('later sparse authored/source binding differs')
            prior = review.authored_item(read(review, prior_path), previous['item'])
            before = review.corrected_record(data['candidates'][cid], prior['corrections'])
            after = review.corrected_record(data['candidates'][cid], decision['corrections'])
            from photo_candidate_realizations import ids as realization_ids
            kind = entry['proposed_record_kind_change']
            if (entry['before_corrected_source_sha256'] != review.c.digest(before)
                    or entry['proposed_corrected_source_sha256'] != review.c.digest(after)
                    or entry['actual_realization_ids'] != realization_ids(after)
                    or set(kind) != {'pointer', 'before', 'after', 'reason'}
                    or kind['pointer'] != '/record_kind' or kind['before'] != before['record_kind']
                    or kind['after'] != decision['recommended_kind']
                    or not isinstance(kind['reason'], str) or not kind['reason'].strip()):
                raise ValueError('later sparse corrected source/kind proposal differs')
            old = existing[cid][2]
            result.append({'candidate_id': cid, 'ordinal': entry['ordinal'], 'item': n,
                'decision': decision, 'previous_authored': previous,
                'worker_before_row_sha256': None,
                'packet': packet_binding(review, packets[old['packet_sha256']], data, cid, cache=packet_cache),
                'packet_resolution': 'root_resolved_unchanged_prior_packet_from_explicit_source_closure_hashes',
                'proposed_record_kind_change': kind})
        pending = [e['ordinal'] for e in result if e['decision']['status'] not in APPROVED]
        approved_count, pending_count = note['approved_proposal_count'], note['pending_proposal_count']
    elif 'bindings' in note and 'decisions' in document:
        if (note.get('complete_source_reread') is not True
                or note['source_snapshot_sha256'] != review.c.digest(data)
                or note['catalog_sha256'] != review.c.digest(data['slot_catalog'])):
            raise ValueError('explicit full reread/source binding required')
        decisions, entries = document['decisions'], note['bindings']
        if ([d['candidate_id'] for d in decisions] != note['directly_reread_ids']
                or [e['candidate_id'] for e in entries] != note['directly_reread_ids']
                or [e['ordinal'] for e in entries] != note['directly_reread_ordinals']):
            raise ValueError('exact sparse reread IDs/ordinals disagree')
        history_path = review.run_path(note['packet_path'], 'worker-notes')
        history = read(review, history_path)['rows']
        if [r['ordinal'] for r in history] != note['directly_reread_ordinals']:
            raise ValueError('custom reread history differs from exact sparse IDs')
        packets = {review.c.digest(read(review, p)): p for p in (review.HERE / 'packets').glob('*.json')}
        for n, (decision, entry, old) in enumerate(zip(decisions, entries, history), 1):
            cid = decision['candidate_id']
            if (entry['amendment_row_sha256'] != review.c.digest(decision)
                    or entry['amendment_status'] != decision['status']
                    or old['registered_row_sha256'] != entry['original_registered_row_sha256']
                    or review.c.digest(old['registered_row']) != old['registered_row_sha256']
                    or old['registered_path'] != entry['original_registered_file']
                    or old['registered_row']['candidate_id'] != cid
                    or old['registered_row']['status'] != entry['original_status']
                    or old['registered_row']['authored_decision'] != entry['original_authored_decision']):
                raise ValueError('worker amendment or historical compiled row binding differs')
            binding = review.binding(data, cid)
            if any(entry[k] != v for k, v in binding.items()):
                raise ValueError('worker source/catalog/reference hashes changed')
            previous = authored_tuple(review, entry['original_authored_decision']['file'], cid,
                                      entry['original_authored_decision']['sha256'])
            if previous != entry['original_authored_decision']:
                raise ValueError('original authored tuple differs')
            result.append({'candidate_id': cid, 'ordinal': entry['ordinal'], 'item': n,
                'decision': decision, 'previous_authored': previous,
                'worker_before_row_sha256': entry['original_registered_row_sha256'],
                'packet': packet_binding(review, packets[old['registered_row']['packet_sha256']], data, cid, cache=packet_cache),
                'reread_artifact': link(review, history_path)})
        pending = note['pending_retained_ordinals']
        approved_count, pending_count = note['approved_amendment_count'], note['pending_retained_count']
    elif document.get('schema') == 'photo-codex-direct-review-amendment/v1':
        source_sha = review.c.digest(data)
        note_source = note.get('source_sha256')
        if (note.get('complete_source_read') is not True
                or note_source is not None and note_source != source_sha
                or document['source_sha256'] != source_sha):
            raise ValueError('explicit full reread/source binding required')
        if note_source is None and (document.get('source_snapshot_file_sha256') !=
                hashlib.sha256((review.HERE / 'SOURCE.json.gz').read_bytes()).hexdigest()
                or note.get('catalog_sha256') != review.c.digest(data['slot_catalog'])):
            raise ValueError('document-bound full snapshot and note catalog required')
        entries = document['amendments']
        reread_ids, pending, approved_count, pending_count, approved_ordinals, summary_resolution = wrapper_attestation(note, entries)
        if (len(set(reread_ids)) != len(reread_ids)
                or [e['reread_id'] for e in entries] != reread_ids):
            raise ValueError('exact sparse reread IDs disagree')
        for n, entry in enumerate(entries, 1):
            decision, cid = entry['decision'], entry['candidate_id']
            source_binding = review.binding(data, cid)
            if (decision['candidate_id'] != cid or entry['model'] != note['model']
                    or entry['reasoning_effort'] != note['reasoning_effort']
                    or entry['source_reread_complete'] is not True
                    or entry['reference_reread_complete'] is not True
                    or entry['source_record_sha256'] != source_binding['source_record_sha256']):
                raise ValueError('per-CID source reread attestation differs')
            resolution = {}
            if summary_resolution is not None:
                resolution['reread_metadata_resolution'] = summary_resolution
            if 'after_proposal_reference_sha256' in entry:
                if entry['after_proposal_reference_sha256'] != source_binding['reference_sha256']:
                    raise ValueError('per-CID source reread attestation differs')
            else:
                # These later notes attest original references and exact source
                # edits. Root proves that the edits preserve references; it does
                # not pretend the worker supplied a missing after-reference hash.
                proposed = review.corrected_record(data['candidates'][cid], decision['corrections'])
                if (entry.get('reference_sha256') != source_binding['reference_sha256']
                        or entry.get('catalog_sha256') != source_binding['catalog_sha256']
                        or exact_references(review, proposed) != exact_references(review, data['candidates'][cid])
                        or 'full_after_proposal_record' in entry
                        and entry['full_after_proposal_record'] != proposed):
                    raise ValueError('explicit original references or unchanged corrected references differ')
                resolution['reference_binding_resolution'] = 'root_verified_exact_edits_preserve_worker_attested_original_references'
            if ('after_proposal_sha256' in entry and entry['after_proposal_sha256'] !=
                    review.c.digest(review.corrected_record(data['candidates'][cid], decision['corrections']))):
                raise ValueError('explicit corrected full-source digest differs')
            if ('role_spec_sha256' in entry and entry['role_spec_sha256'] !=
                    {role['slot_id']: review.c.digest(data['slot_catalog'][role['slot_id']])
                     for role in decision['roles']}):
                raise ValueError('explicit selected role spec digests differ')
            if note_source is None:
                resolution['source_binding_resolution'] = 'root_verified_worker_document_full_snapshot_and_per_record_bindings'
            matches = [packet_binding(review, path, data, cid, cache=packet_cache) for path in note['packet_paths']
                       if cid in read(review, review.run_path(path, 'packets'))['ids']]
            if len(matches) != 1 or matches[0]['sha256'] != note['packet_sha256'] or document['packet_sha256'] != note['packet_sha256']:
                raise ValueError('explicit worker full packet hash differs')
            result.append({'candidate_id': cid, 'ordinal': entry['ordinal'], 'item': n,
                'decision': decision, 'previous_authored': authored_tuple(review,
                    entry['before_authored_file'], cid, entry['before_authored_row_sha256']),
                'worker_before_row_sha256': None, 'packet': matches[0],
                'reread_id': entry['reread_id'], **resolution})
        if sorted(approved_ordinals) != sorted(e['ordinal'] for e in result if e['decision']['status'] in APPROVED):
            raise ValueError('explicit approved ordinals disagree')
    else:
        raise ValueError('unsupported worker amendment attestation format')
    ids = [e['candidate_id'] for e in result]
    if (not ids or len(ids) != len(set(ids)) or len(result) != len(entries)
            or type(note['directly_reread_count']) is not int
            or note['directly_reread_count'] != len(result)
            or approved_count != sum(e['decision']['status'] in APPROVED for e in result)
            or pending_count != len(pending) or len(pending) != len(set(pending))
            or sorted(pending) != sorted(e['ordinal'] for e in result if e['decision']['status'] not in APPROVED)):
        raise ValueError('sparse reread counts/statuses disagree')
    for entry in result:
        if (type(entry['ordinal']) is not int or not 0 <= entry['ordinal'] < len(order)
                or order[entry['ordinal']] != entry['candidate_id']
                or set(entry['decision']) != FIELDS):
            raise ValueError('sparse CID/ordinal or authored fields disagree')
        entry['assignment'] = assignment(review, note, entry['ordinal'])
        proposed = review.corrected_record(data['candidates'][entry['candidate_id']], entry['decision']['corrections'])
        if 'amendments' in document:
            attested = document['amendments'][entry['item'] - 1]
            for field in ('conditions', 'effects'):
                key = 'after_proposal_' + field
                if key in attested and attested[key] != proposed[field]:
                    raise ValueError('attested after-proposal native value differs')
    return result


def compiled_rows(review):
    rows = {}
    for path in sorted((review.HERE / 'decisions').glob('*.json')):
        document = read(review, path)
        for offset, row in enumerate(document['decisions']):
            if row['candidate_id'] in rows:
                raise ValueError('duplicate existing canonical judgement')
            rows[row['candidate_id']] = (path, offset, row)
    return rows


def normalize(review, authored_path, note_path, *, actor):
    if actor != '/root':
        raise ValueError('only root may normalize/apply worker amendments')
    data, existing = review.source(), compiled_rows(review)
    authored_path = review.run_path(str(authored_path), 'authored')
    note_path = review.run_path(str(note_path), 'worker-notes')
    entries = origins(review, authored_path, note_path, data)
    replacements = []
    for entry in entries:
        path, offset, old = existing[entry['candidate_id']]
        if (old.get('review_method') != 'codex_subagent_direct_source_read'
                or old.get('review_provenance', {}).get('task_name') != entry['assignment']['task_name']
                or old['authored_decision'] != entry['previous_authored']
                or (entry['worker_before_row_sha256'] is not None
                    and review.c.digest(old) != entry['worker_before_row_sha256'])):
            raise ValueError('current compiled row differs from original worker binding')
        replacements.append({'candidate_id': entry['candidate_id'],
            'registered_file': str(path.relative_to(review.ROOT)), 'registered_item': offset + 1,
            'before_registered_row_sha256': review.c.digest(old), **entry})
    return {'schema': MANIFEST_SCHEMA, 'normalization_author': '/root',
        'worker_attestation': False, 'root_all_worker_sources_read_claimed': False,
        'source_sha256': review.c.digest(data), 'authored_document': link(review, authored_path),
        'worker_note': link(review, note_path), 'replacements': replacements}


def manifest_entries(review, manifest_path, data):
    manifest_path = review.run_path(str(manifest_path), 'worker-notes')
    manifest = read(review, manifest_path)
    if (set(manifest) != {'schema', 'normalization_author', 'worker_attestation',
            'root_all_worker_sources_read_claimed', 'source_sha256', 'authored_document',
            'worker_note', 'replacements'} or manifest['schema'] != MANIFEST_SCHEMA
            or manifest['normalization_author'] != '/root'
            or manifest['worker_attestation'] is not False
            or manifest['root_all_worker_sources_read_claimed'] is not False
            or manifest['source_sha256'] != review.c.digest(data)):
        raise ValueError('explicit root normalization boundary/source required')
    authored_path = checked_link(review, manifest['authored_document'], 'authored')
    note_path = checked_link(review, manifest['worker_note'], 'worker-notes')
    expected = origins(review, authored_path, note_path, data)
    selected = manifest['replacements']
    if len(selected) != len(expected):
        raise ValueError('normalization cannot expand or omit worker reread IDs')
    for entry, original in zip(selected, expected):
        if (set(entry) != set(original) | {'registered_file', 'registered_item', 'before_registered_row_sha256'}
                or any(entry[k] != v for k, v in original.items())):
            raise ValueError('normalization differs from explicit worker attestation')
        review.run_path(entry['registered_file'], 'decisions')
        if type(entry['registered_item']) is not int or entry['registered_item'] < 1:
            raise ValueError('exact previous compiled row location required')
    return manifest, authored_path, selected


def provenance(review, manifest_path, manifest, entry):
    return {'schema': PROVENANCE_SCHEMA, **entry['assignment'],
        'reread_candidate_id': entry['candidate_id'], 'reread_ordinal': entry['ordinal'],
        'exact_reread_count': len(manifest['replacements']),
        'normalization_manifest': link(review, manifest_path),
        'worker_note': manifest['worker_note'], 'authored_document': manifest['authored_document'],
        'packet': entry['packet'], 'root_all_worker_sources_read_claimed': False}


def validate_provenance(review, row, *, cache=None):
    claimed = row['review_provenance']
    path = checked_link(review, claimed['normalization_manifest'], 'worker-notes')
    key = ('sparse_amendment', path)
    if cache is not None and key in cache:
        manifest, authored_path, entries = cache[key]
    else:
        manifest, authored_path, entries = manifest_entries(review, path, review.source())
        if cache is not None:
            cache[key] = manifest, authored_path, entries
    matches = [entry for entry in entries if entry['candidate_id'] == row['candidate_id']]
    if len(matches) != 1:
        raise ValueError('CID was not explicitly reread')
    entry = matches[0]
    location = {'file': str(authored_path.relative_to(review.ROOT)), 'item': entry['item'],
                'sha256': review.c.digest(entry['decision'])}
    if (claimed != provenance(review, path, manifest, entry) or row['authored_decision'] != location
            or row['packet_sha256'] != entry['packet']['sha256']
            or any(row[k] != v for k, v in entry['decision'].items())):
        raise ValueError('compiled amendment differs from exact worker decision/status/attribution')


def apply(review, manifest_path, *, actor):
    if actor != '/root':
        raise ValueError('only root may normalize/apply worker amendments')
    manifest_path = review.run_path(str(manifest_path), 'worker-notes')
    data = review.source()
    manifest, authored_path, entries = manifest_entries(review, manifest_path, data)
    archive = review.HERE / 'revisions' / manifest_path.stem
    if archive.exists():
        raise ValueError('revision history already exists; never overwrite it')
    # Existing full snapshot/ledger verification remains mandatory.
    review.verify()
    existing = compiled_rows(review)
    originals, documents, changes = {}, {}, []
    proof_cache = {('sparse_amendment', manifest_path): (manifest, authored_path, entries)}
    binding_cache = {}
    for entry in entries:
        cid = entry['candidate_id']
        path, offset, old = existing[cid]
        if (str(path.relative_to(review.ROOT)) != entry['registered_file']
                or offset + 1 != entry['registered_item']
                or review.c.digest(old) != entry['before_registered_row_sha256']
                or old['authored_decision'] != entry['previous_authored']):
            raise ValueError('registered source judgement changed before amendment')
        new = {**review.binding(data, cid), **copy.deepcopy(entry['decision']),
            'schema': review.DELEGATED_SCHEMA, 'reviewer': 'Codex',
            'review_method': 'codex_subagent_direct_source_read', 'independent_human_review': False,
            'packet_sha256': entry['packet']['sha256'], 'authored_decision': {
                'file': str(authored_path.relative_to(review.ROOT)), 'item': entry['item'],
                'sha256': review.c.digest(entry['decision'])},
            'review_provenance': provenance(review, manifest_path, manifest, entry)}
        review.validate_decision(new, data, provenance_cache=proof_cache, binding_cache=binding_cache)
        originals.setdefault(path, path.read_bytes())
        documents.setdefault(path, read(review, path))['decisions'][offset] = new
        changes.append({'candidate_id': cid, 'before': old, 'after': new,
            'before_sha256': review.c.digest(old), 'after_sha256': review.c.digest(new)})
    archive.mkdir(parents=True, exist_ok=False)
    for path, body in originals.items():
        with (archive / path.name).open('xb') as output:
            output.write(body)
    review.write(archive / 'REVISION.json', {'schema': 'photo-codex-worker-amendment-revision/v1',
        'root_all_worker_sources_read_claimed': False, 'normalization_manifest': link(review, manifest_path),
        'archive_hashes': {p.name: hashlib.sha256(b).hexdigest() for p, b in originals.items()},
        'changes': changes, 'native_changes_applied': False, 'stage05_complete': False})
    try:
        for path, document in documents.items():
            review.write(path, document)
        result = review.verify()
    except Exception:
        for path, body in originals.items():
            path.write_bytes(body)
        review.write(archive / 'ROLLED-BACK.json', {'compiled_rows_restored': True})
        review.verify()
        raise
    review.write(archive / 'AFTER-VERIFICATION.json', result)
    return {'revised': len(changes), 'archive': str(archive.relative_to(review.ROOT)), 'progress': result}


def main():
    import direct_review as review
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['normalize', 'apply'])
    parser.add_argument('--actor', required=True, choices=['/root'])
    parser.add_argument('--authored')
    parser.add_argument('--worker-note')
    parser.add_argument('--manifest', required=True)
    args = parser.parse_args()
    if args.command == 'normalize':
        result = normalize(review, args.authored, args.worker_note, actor=args.actor)
        path = review.run_path(args.manifest, 'worker-notes')
        if path.exists():
            raise ValueError('normalization manifest already exists; never overwrite')
        review.write(path, result)
        print(json.dumps({'manifest': str(path), 'replacements': len(result['replacements'])}))
    else:
        print(json.dumps(apply(review, args.manifest, actor=args.actor)))


if __name__ == '__main__':
    main()
