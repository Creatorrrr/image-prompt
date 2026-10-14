"""Prepare full sources and validate authored Codex decisions; never infer tags.

No provider, embedding, network, subprocess reviewer or model is imported here.
Mechanical acceptance of an authored decision is not an accuracy measurement.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import gzip
import hashlib
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import photo_candidate_corpus as c

SCHEMA = 'photo-codex-direct-review/v1'
DELEGATED_SCHEMA = 'photo-codex-direct-review/v2'
NEGATIVE = frozenset({'confusion_boundaries', 'research_confusions', 'confounders',
    'failure_modes', 'excluded', 'exclusions', 'forbidden', 'avoid', 'negative',
    'research_source_urls', 'tags', 'facets', 'reject_substitutes', 'contrast_examples',
    'forbidden_prompt_terms', 'runtime_forbidden_labels', 'role_evidence', 'semantic_review',
    'claim_limits', 'research_claim_limits'})


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    body = c.canonical_bytes(value) + b'\n'
    temporary = path.with_name(path.name + '.pending')
    temporary.write_bytes(body)
    temporary.replace(path)


def references(value):
    if isinstance(value, str) and c.ID.fullmatch(value):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from references(key)
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


def closure(data, cid):
    found, pending = {}, [cid]
    while pending:
        item = pending.pop()
        if item in found:
            continue
        record = data['candidates'][item]
        found[item] = record
        pending.extend(set(references(record)) - set(found))
    found.pop(cid)
    return dict(sorted(found.items()))


def binding(data, cid, *, cache=None):
    key = (id(data), cid)
    if cache is not None and key in cache:
        return cache[key]
    record = data['candidates'][cid]
    catalog_key = (id(data), 'catalog_sha256')
    catalog_sha256 = (cache[catalog_key] if cache is not None and catalog_key in cache
                      else c.digest(data['slot_catalog']))
    result = {'candidate_id': cid, 'source_record_sha256': c.digest(record),
        'catalog_sha256': catalog_sha256,
        'reference_sha256': {key: c.digest(row) for key, row in closure(data, cid).items()}}
    if cache is not None:
        cache[catalog_key] = catalog_sha256
        cache[key] = result
    return result


def pointer(record, path, *, positive=False):
    if not isinstance(path, str) or not path.startswith('/content/'):
        raise ValueError('expected primary content JSON pointer')
    keys = [key.replace('~1', '/').replace('~0', '~') for key in path[1:].split('/')]
    if positive and (set(keys) & NEGATIVE or (keys[1] == 'activation' and
            (len(keys) < 4 or keys[2] not in {'exact_terms', 'project_glossary_aliases'}))):
        raise ValueError('negative, routing or review metadata is not positive evidence')
    value = record
    try:
        for key in keys:
            if isinstance(value, list):
                if not key.isdigit() or str(int(key)) != key:
                    raise ValueError('noncanonical array index')
                value = value[int(key)]
            else:
                value = value[key]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError('missing source pointer') from exc
    if not isinstance(value, str):
        raise ValueError('pointer must address a complete source string')
    return value


def corrected_record(record, corrections):
    result = copy.deepcopy(record)
    if not isinstance(corrections, list):
        raise ValueError('corrections must be a list')
    seen = set()
    for change in corrections:
        if set(change) != {'pointer', 'before', 'after', 'reason'}:
            raise ValueError('invalid correction fields')
        path = change['pointer']
        if path in seen or not all(isinstance(change[k], str) and change[k].strip()
                for k in ('before', 'after', 'reason')):
            raise ValueError('duplicate or empty source correction')
        seen.add(path)
        # Exact source corrections may repair a negative/claim-limit clause;
        # that clause still cannot qualify a positive fact or role.
        if pointer(result, path) != change['before']:
            raise ValueError('source correction is not bound to exact current text')
        keys = [key.replace('~1', '/').replace('~0', '~') for key in path[1:].split('/')]
        value = result
        for key in keys[:-1]:
            value = value[int(key)] if isinstance(value, list) else value[key]
        key = keys[-1]
        value[int(key) if isinstance(value, list) else key] = change['after']
    return result


def validate_fact(fact, record, catalog, slot=None):
    if set(fact) != {'pointer', 'quote', 'dimension', 'target', 'property'}:
        raise ValueError('invalid source fact fields')
    if not isinstance(fact['quote'], str) or not fact['quote'].strip() or fact['quote'] not in pointer(
            record, fact['pointer'], positive=True):
        raise ValueError('quote differs from positive source')
    for key in ('target', 'property'):
        if (not isinstance(fact[key], str) or not fact[key].strip() or '*' in fact[key]
                or fact[key].endswith('.')):
            raise ValueError('fact owner/property must be concrete')
    from photo_contracts import AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS
    if fact['dimension'] not in AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS:
        raise ValueError('unknown effect dimension')
    if slot is not None:
        spec = catalog[slot]
        if fact['dimension'] not in spec['dimensions'] or not any(
                fact['property'] == prefix.rstrip('.') or fact['property'].startswith(
                    prefix if prefix.endswith('.') else prefix + '.')
                for prefix in spec['property_prefixes']):
            raise ValueError('fact is outside role property contract')


def validate_decision(row, data, *, provenance_cache=None, binding_cache=None):
    required = {'schema', 'reviewer', 'review_method', 'independent_human_review',
        'candidate_id', 'source_record_sha256', 'catalog_sha256', 'reference_sha256',
        'meaning_summary', 'recommended_kind', 'corrections', 'roles', 'facts',
        'rejected_boundaries', 'uncertainties', 'status', 'all_roles_considered',
        'authored_decision', 'packet_sha256'}
    delegated = isinstance(row, dict) and row.get('schema') == DELEGATED_SCHEMA
    if delegated:
        required.add('review_provenance')
    if not isinstance(row, dict) or set(row) != required:
        raise ValueError('invalid direct decision fields')
    if (row['schema'] != (DELEGATED_SCHEMA if delegated else SCHEMA) or row['reviewer'] != 'Codex'
            or row['review_method'] != ('codex_subagent_direct_source_read' if delegated
                                       else 'codex_direct_source_read')
            or row['independent_human_review'] is not False):
        raise ValueError('direct reviewer identity/method required')
    if delegated:
        validate_review_provenance(row, cache=provenance_cache)
    cid = row['candidate_id']
    if cid not in data['candidates']:
        raise ValueError('unknown candidate')
    expected = binding(data, cid, cache=binding_cache)
    if any(row[key] != value for key, value in expected.items()):
        raise ValueError('source, references or catalog changed after review')
    if (not isinstance(row['meaning_summary'], str) or not row['meaning_summary'].strip()
            or row['all_roles_considered'] is not True
            or row['status'] not in {'approved', 'diagnostic_reviewed', 'needs_source_fix',
                                     'needs_boundary_review'}):
        raise ValueError('meaning and explicit review status required')
    authored = row['authored_decision']
    if not isinstance(authored, dict) or set(authored) != {'file', 'item', 'sha256'} or not isinstance(
            authored['file'], str) or not authored['file'] or not isinstance(authored['item'], int) or authored['item'] < 1:
        raise ValueError('authored decision location required')
    if not isinstance(row['packet_sha256'], str) or not re.fullmatch('[0-9a-f]{64}', row['packet_sha256']):
        raise ValueError('complete source packet binding required')
    if row['recommended_kind'] not in c.KINDS:
        raise ValueError('unknown reviewed record kind')
    record = corrected_record(data['candidates'][cid], row['corrections'])
    catalog = data['slot_catalog']
    from photo_candidate_realizations import ids
    known_rids = set(ids(record))
    if not all(isinstance(row[key], list) for key in ('roles', 'facts', 'uncertainties', 'rejected_boundaries')):
        raise ValueError('review arrays required')
    if not row['rejected_boundaries'] or not all(isinstance(v, str) and v.strip()
                                              for v in row['rejected_boundaries']):
        raise ValueError('explicit rejected-confusion reasoning required')
    for issue in row['uncertainties']:
        if not isinstance(issue, dict) or set(issue) != {'kind', 'detail'} or not issue['detail']:
            raise ValueError('explicit uncertainty classification required')
    if row['status'] in {'approved', 'diagnostic_reviewed'} and row['uncertainties']:
        raise ValueError('unresolved issues cannot be approved')
    diagnostic = row['recommended_kind'] == 'diagnostic'
    if diagnostic and (row['roles'] or row['facts']):
        raise ValueError('diagnostic cannot acquire positive roles/effects')
    if row['status'] == 'approved' and (diagnostic or not row['roles'] or not row['facts']):
        raise ValueError('positive approval needs owned roles and facts')
    if row['status'] == 'diagnostic_reviewed' and not diagnostic:
        raise ValueError('diagnostic status/kind mismatch')
    seen = set()
    for role in row['roles']:
        if not isinstance(role, dict) or set(role) != {'slot_id', 'semantic_role', 'scope',
                'realization_ids', 'rationale', 'evidence'}:
            raise ValueError('invalid role decision')
        tag = role['slot_id']
        if tag in seen or tag not in catalog:
            raise ValueError('duplicate or unknown role')
        seen.add(tag)
        if (role['semantic_role'] != catalog[tag]['semantic_role']
                or role['scope'] not in {'whole_record', 'positive_alternative'}
                or not isinstance(role['rationale'], str) or not role['rationale'].strip()
                or not isinstance(role['realization_ids'], list) or not role['realization_ids']
                or len(role['realization_ids']) != len(set(role['realization_ids']))
                or not set(role['realization_ids']) <= known_rids
                or role['scope'] == 'whole_record' and set(role['realization_ids']) != known_rids
                or not isinstance(role['evidence'], list) or not role['evidence']):
            raise ValueError('role contract, scope or evidence missing')
        for fact in role['evidence']:
            validate_fact(fact, record, catalog, tag)
            for rid in role['realization_ids']:
                if not any({k: v for k, v in item.items() if k != 'realization_id'} == fact
                           and item['realization_id'] == rid for item in row['facts']):
                    raise ValueError('role evidence must be an explicitly authored branch fact')
    for fact in row['facts']:
        if not isinstance(fact, dict) or 'realization_id' not in fact or fact['realization_id'] not in known_rids:
            raise ValueError('fact must name an actual source realization')
        validate_fact({k: v for k, v in fact.items() if k != 'realization_id'}, record, catalog)
    return row


def run_path(value, directory):
    if not isinstance(value, str):
        raise ValueError('review artifact path must be a string')
    path = Path(value)
    if not path.is_absolute():
        path = (HERE / path if path.parts and path.parts[0] in
                {'authored', 'packets', 'worker-notes'} else ROOT / path)
    path = path.resolve()
    if not path.is_relative_to(HERE / directory):
        raise ValueError('review artifact is outside its assigned directory')
    return path


def delegated_provenance(note_path, authored_path, packet_sha256, cid, *, cache=None):
    """Bind an explicit worker attestation to a real dispatched assignment.

    This proves attribution and range integrity, not semantic accuracy or that
    the writer actually read the source. The writer must perform that review.
    """
    note_path = run_path(str(note_path), 'worker-notes')
    authored_path = run_path(str(authored_path), 'authored')
    def read(path):
        if cache is None:
            return c.decode(path.read_bytes())
        if path not in cache:
            cache[path] = c.decode(path.read_bytes())
        return cache[path]
    note = read(note_path)
    registry_document = read(HERE / 'DELEGATION-ASSIGNMENTS.json')
    registry = registry_document['assignments']
    start, stop = note['start'], note['stop']
    if not isinstance(start, int) or not isinstance(stop, int):
        raise ValueError('worker review range must be integer ordinals')
    matches = [(key, assignment) for key, assignment in registry.items()
               if note['task_name'] in {key, assignment['task_name']}
               and assignment['start'] <= start < stop <= assignment['stop']]
    if len(matches) != 1:
        raise ValueError('worker has no unique dispatched assignment')
    assignment_id, assignment = matches[0]
    order = read(HERE / 'ORDER.json')
    ordinal = order.index(cid)
    if any(transfer['from_assignment'] == assignment_id
           and transfer['start'] <= ordinal < transfer['stop']
           for transfer in registry_document.get('reassignments', [])):
        raise ValueError('review range was explicitly reassigned to another worker')
    unresolved = note['unresolved_ordinals']
    if (not isinstance(start, int) or not isinstance(stop, int)
            or not assignment['start'] <= start < stop <= assignment['stop']
            or cid not in order[start:stop]
            or note['model'] != assignment['model'] or note['model'] != 'gpt-6.1-sol'
            or note['reasoning_effort'] != assignment['reasoning_effort']
            or note['complete_source_read'] is not True
            or note['directly_reviewed_count'] != stop - start
            or not isinstance(unresolved, list) or len(set(unresolved)) != len(unresolved)
            or any(not isinstance(n, int) or not start <= n < stop for n in unresolved)):
        raise ValueError('worker identity, assigned range or complete review does not match')
    if authored_path not in {run_path(value, 'authored') for value in note['authored_paths']}:
        raise ValueError('authored document is not attested by this worker')
    packets = [read(run_path(value, 'packets')) for value in note['packet_paths']]
    if not any(c.digest(packet) == packet_sha256 and cid in packet['ids'] for packet in packets):
        raise ValueError('complete source packet is not attested by this worker')
    return {'assignment_id': assignment_id, 'task_name': assignment['task_name'],
        'model': assignment['model'], 'reasoning_effort': assignment['reasoning_effort'],
        'range': [start, stop], 'assignment_sha256': c.digest(assignment),
        'worker_note': {'file': str(note_path.relative_to(ROOT)), 'sha256': c.digest(note)}}


def validate_review_provenance(row, *, cache=None):
    provenance = row['review_provenance']
    if not isinstance(provenance, dict) or set(provenance) != {
            'assignment_id', 'task_name', 'model', 'reasoning_effort', 'range',
            'assignment_sha256', 'worker_note'}:
        raise ValueError('delegated review attribution is required')
    expected = delegated_provenance(provenance['worker_note']['file'],
        row['authored_decision']['file'], row['packet_sha256'], row['candidate_id'], cache=cache)
    if provenance != expected:
        raise ValueError('worker note or dispatched assignment changed after review')
    note_path = run_path(provenance['worker_note']['file'], 'worker-notes')
    note = (cache[note_path] if cache is not None else c.decode(note_path.read_bytes()))
    order_path = HERE / 'ORDER.json'
    order = (cache[order_path] if cache is not None else c.decode(order_path.read_bytes()))
    pending = order.index(row['candidate_id']) in note['unresolved_ordinals']
    if pending != (row['status'] not in {'approved', 'diagnostic_reviewed'}):
        raise ValueError('unresolved worker judgement cannot be counted as approved')


def source():
    return c.decode(gzip.decompress((HERE / 'SOURCE.json.gz').read_bytes()))


def assert_source_snapshot(data, current, baseline, order):
    if (c.digest(data) != baseline['source_sha256']
            or c.digest(current) != baseline['source_sha256']
            or c.digest(data['slot_catalog']) != baseline['catalog_sha256']):
        raise ValueError('complete frozen/current source or binding snapshot changed')
    if (len(order) != len(set(order)) or set(order) != set(data['candidates'])
            or len(order) != baseline['candidate_count']):
        raise ValueError('frozen order does not cover canonical IDs exactly once')


def initialize():
    if (HERE / 'BASELINE.json').exists():
        raise ValueError('baseline already exists; never overwrite reviewed input')
    data = c.load(SKILL / 'assets')
    config = c.decode((SKILL / 'embedding-default.json').read_bytes())
    manifest = c.decode((SKILL / 'assets/photo_candidate_search.json').read_bytes())
    if config['provider'] != 'embeddinggemma2-local' or config['space'] != manifest['space']:
        raise ValueError('matching local default and active index required')
    body = c.canonical_bytes(data)
    (HERE / 'SOURCE.json.gz').write_bytes(gzip.compress(body, mtime=0))
    order = sorted(data['candidates'], key=lambda cid: (
        data['candidates'][cid]['record_kind'] != 'visual_option',
        len(c.canonical_bytes(data['candidates'][cid])), cid))
    write(HERE / 'ORDER.json', order)
    write(HERE / 'CATALOG.json', data['slot_catalog'])
    owners = {}
    modules = c.decode((SKILL / 'assets' / c.MANIFEST_NAME).read_bytes())['modules']
    for item in modules:
        if item['kind'] == 'candidates':
            for cid in c.decode((SKILL / 'assets' / item['file']).read_bytes())['candidates']:
                owners[cid] = item['file']
    write(HERE / 'BASELINE.json', {'schema': 'photo-codex-direct-baseline/v1',
        'source_sha256': c.digest(data), 'catalog_sha256': c.digest(data['slot_catalog']),
        'candidate_count': len(data['candidates']), 'binding_count': len(data['slot_bindings']),
        'slot_count': len(data['slot_catalog']), 'layout_id': manifest['layout_id'],
        'space': manifest['space'], 'payload_owners': owners,
        'review_method': 'codex_direct_source_read', 'historical_model_drafts_imported': 0,
        'external_model_calls': 0, 'native_changes_applied': False})
    return {'initialized': True, 'candidate_count': len(order), 'semantic_approvals': 0}


def prepare(start, count):
    data = source()
    order = c.decode((HERE / 'ORDER.json').read_bytes())
    if start < 0 or count < 1 or start + count > len(order):
        raise ValueError('invalid complete source range')
    ids = order[start:start + count]
    packet = {'schema': 'photo-codex-direct-source-packet/v1', 'start': start,
        'ids': ids, 'source_sha256': c.digest(data),
        'catalog_sha256': c.digest(data['slot_catalog']),
        'records': {cid: data['candidates'][cid] for cid in ids},
        'references': {cid: closure(data, cid) for cid in ids}}
    path = HERE / 'packets' / f'{start:05d}-{count:03d}.json'
    if path.exists() and c.decode(path.read_bytes()) != packet:
        raise ValueError('existing full source packet differs')
    write(path, packet)
    return {'packet': str(path.relative_to(ROOT)), 'packet_sha256': c.digest(packet), 'ids': ids}


def verify():
    data = source()
    current = c.load(SKILL / 'assets')
    baseline = c.decode((HERE / 'BASELINE.json').read_bytes())
    order = c.decode((HERE / 'ORDER.json').read_bytes())
    assert_source_snapshot(data, current, baseline, order)
    accepted, pending, errors = {}, [], {}
    packets = {}
    provenance_cache = {}
    binding_cache, authored_documents = {}, {}
    for path in sorted((HERE / 'packets').glob('*.json')):
        packet = c.decode(path.read_bytes())
        key = c.digest(packet)
        if key in packets:
            raise ValueError('duplicate source packet')
        packets[key] = packet
    for path in sorted((HERE / 'decisions').glob('*.json')):
        document = c.decode(path.read_bytes())
        for number, row in enumerate(document['decisions'], 1):
            try:
                # Complete current/frozen source equality above includes every
                # record, catalog, policy and binding, even outside reviewed IDs.
                validate_decision(row, data, provenance_cache=provenance_cache,
                                  binding_cache=binding_cache)
                if row['candidate_id'] in accepted or row['candidate_id'] in pending:
                    raise ValueError('duplicate decision for one canonical candidate')
                location = row['authored_decision']
                authored_path = (ROOT / location['file']).resolve()
                if not authored_path.is_relative_to(HERE / 'authored'):
                    raise ValueError('authored judgement must be stored in this direct-review run')
                if authored_path not in authored_documents:
                    authored_documents[authored_path] = c.decode(authored_path.read_bytes())
                authored_document = authored_documents[authored_path]
                authored = authored_document['decisions'][location['item'] - 1]
                if location['sha256'] != c.digest(authored) or any(row[k] != v for k, v in authored.items()):
                    raise ValueError('compiled row differs from explicitly authored decision')
                packet = packets[row['packet_sha256']]
                cid = row['candidate_id']
                if (cid not in packet['ids'] or packet['records'][cid] != data['candidates'][cid]
                        or packet['references'][cid] != closure(data, cid)):
                    raise ValueError('packet does not bind the complete candidate and references')
                if row['status'] in {'approved', 'diagnostic_reviewed'}:
                    accepted[cid] = row
                else:
                    pending.append(cid)
            except (ValueError, KeyError, TypeError) as exc:
                errors[f'{path.name}:{number}'] = str(exc)
    result = {'schema': 'photo-codex-direct-progress/v1', 'records': len(data['candidates']),
        'direct_approved_records': len(accepted), 'pending_decisions': len(pending),
        'unreviewed_records': len(data['candidates']) - len(accepted) - len(pending),
        'approved_ids': sorted(accepted), 'pending_ids': sorted(pending), 'errors': errors,
        'source_review_coverage_complete': len(accepted) == len(data['candidates']) and not errors,
        'native_qualification_status': 'not_certified_by_this_ledger',
        'stage05_complete': False,
        'boundary': 'Authored Codex decisions checked mechanically; no independent human or pixel verification.'}
    result['approved_review_methods'] = dict(Counter(row['review_method'] for row in accepted.values()))
    write(HERE / 'PROGRESS.json', result)
    if errors:
        raise ValueError(str(errors))
    return {key: value for key, value in result.items() if key not in {'approved_ids', 'pending_ids'}}


def register(packet_path, authored_path, worker_note=None):
    """Bind authored semantic decisions to sources; no missing judgement defaults."""
    data = source()
    packet_path, authored_path = Path(packet_path).resolve(), Path(authored_path).resolve()
    if not packet_path.is_relative_to(HERE / 'packets') or not authored_path.is_relative_to(HERE / 'authored'):
        raise ValueError('packet and authored decisions must belong to this run')
    packet = c.decode(packet_path.read_bytes())
    authored = c.decode(authored_path.read_bytes())
    required = {'candidate_id', 'meaning_summary', 'recommended_kind', 'corrections',
        'roles', 'facts', 'rejected_boundaries', 'uncertainties', 'status', 'all_roles_considered'}
    rows = []
    provenance_cache = {}
    binding_cache = {}
    for number, decision in enumerate(authored['decisions'], 1):
        if set(decision) != required or decision['candidate_id'] not in packet['ids']:
            raise ValueError('explicit authored meaning, roles and status required for packet ID')
        cid = decision['candidate_id']
        row = {**binding(data, cid, cache=binding_cache), **decision, 'schema': SCHEMA, 'reviewer': 'Codex',
            'review_method': 'codex_direct_source_read', 'independent_human_review': False,
            'packet_sha256': c.digest(packet), 'authored_decision': {
                'file': str(authored_path.relative_to(ROOT)), 'item': number, 'sha256': c.digest(decision)}}
        if worker_note is not None:
            row.update(schema=DELEGATED_SCHEMA, review_method='codex_subagent_direct_source_read',
                review_provenance=delegated_provenance(worker_note, authored_path, c.digest(packet), cid,
                                                       cache=provenance_cache))
        validate_decision(row, data, provenance_cache=provenance_cache, binding_cache=binding_cache)
        rows.append(row)
    if len({row['candidate_id'] for row in rows}) != len(rows):
        raise ValueError('duplicate authored candidate')
    path = HERE / 'decisions' / authored_path.name
    result = {'schema': 'photo-codex-direct-decision-batch/v1', 'decisions': rows}
    if path.exists() and c.decode(path.read_bytes()) != result:
        raise ValueError('existing decision differs; invalidate and record a correction explicitly')
    write(path, result)
    return verify()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('init')
    view = sub.add_parser('prepare')
    view.add_argument('--start', type=int, required=True)
    view.add_argument('--count', type=int, required=True)
    sub.add_parser('verify')
    registration = sub.add_parser('register')
    registration.add_argument('--packet', required=True)
    registration.add_argument('--authored', required=True)
    registration.add_argument('--worker-note')
    args = parser.parse_args()
    result = (initialize() if args.command == 'init' else prepare(args.start, args.count)
        if args.command == 'prepare' else register(args.packet, args.authored, args.worker_note)
        if args.command == 'register' else verify())
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
