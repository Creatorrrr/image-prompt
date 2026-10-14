"""Read-only integrity checks for explicit latest native source reviews.

Shape validity never changes a worker's status. Root acceptance is a separate
immutable artifact. Actor declarations bind the collaboration protocol; they
are not cryptographic authentication. No history, source, registry or runtime
file is written, and no semantic values or binding policy are inferred.
"""
from __future__ import annotations
import argparse
import copy
import gzip
import hashlib
import json
from pathlib import Path

import direct_review as dr
import photo_semantic_evidence as native

INPUT = 'photo-codex-native-review-input/v1'
ASSIGNMENT = 'photo-codex-native-review-assignment/v1'
BATCH = 'photo-codex-native-review-batch/v1'
NOTE = 'photo-codex-native-review-note/v1'
ACCEPTANCE = 'photo-codex-native-review-acceptance/v1'
LATEST = 'photo-codex-latest-native-reviews/v1'
STATUSES = frozenset({'approved', 'diagnostic_reviewed', 'pending'})
PRODUCTION_COUNT = 18250


def exact(a, b):
    return dr.c.canonical_bytes(a) == dr.c.canonical_bytes(b)


def fields(value, expected, label):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(label + ': exact fields required')


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + ': explicit text required')


def sha(value):
    return isinstance(value, str) and len(value) == 64 and all(x in '0123456789abcdef' for x in value)


def read_json(path):
    raw = path.read_bytes()
    return dr.c.decode(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)


def path_in(root, value):
    text(value, 'artifact file')
    path = (Path(root) / value).resolve()
    if not path.is_relative_to(Path(root).resolve()):
        raise ValueError('artifact escapes evidence root')
    return path


def artifact(root, ref):
    fields(ref, {'file', 'file_sha256', 'sha256'}, 'artifact binding')
    path = path_in(root, ref['file']); raw = path.read_bytes(); value = read_json(path)
    if (not sha(ref['file_sha256']) or not sha(ref['sha256'])
            or hashlib.sha256(raw).hexdigest() != ref['file_sha256']
            or dr.c.digest(value) != ref['sha256']):
        raise ValueError('artifact bytes or canonical digest changed')
    return value


def pointer_parts(path):
    if not isinstance(path, str) or not path.startswith('/'):
        raise ValueError('explicit non-root JSON pointer required')
    parts = path[1:].split('/')
    if any('~' in part.replace('~0', '').replace('~1', '') for part in parts):
        raise ValueError('invalid JSON pointer escape')
    return [part.replace('~1', '/').replace('~0', '~') for part in parts]


def apply_delta(before, changes):
    """Exact authored subtree edits only; lists must be replaced as whole values."""
    if not isinstance(changes, list):
        raise ValueError('explicit source delta list required')
    result = copy.deepcopy(before); seen = []
    for change in changes:
        fields(change, {'pointer', 'before_exists', 'before', 'after_exists', 'after', 'reason'}, 'source delta')
        text(change['reason'], 'source delta reason'); parts = pointer_parts(change['pointer'])
        if any(parts[:len(p)] == p or p[:len(parts)] == parts for p in seen):
            raise ValueError('overlapping or duplicate source delta')
        seen.append(parts); parent = result
        for key in parts[:-1]:
            if not isinstance(parent, dict) or key not in parent:
                raise ValueError('source delta missing object parent')
            parent = parent[key]
        if not isinstance(parent, dict) or any(type(change[k]) is not bool for k in ('before_exists', 'after_exists')):
            raise ValueError('source delta must address an object field')
        key = parts[-1]; exists = key in parent
        if (change['before_exists'] != exists or exists and not exact(parent[key], change['before'])
                or not exists and change['before'] is not None
                or not change['after_exists'] and change['after'] is not None):
            raise ValueError('source delta exact before mismatch')
        if change['after_exists']:
            if exists and exact(parent[key], change['after']):
                raise ValueError('source delta must describe an actual explicit change')
            parent[key] = copy.deepcopy(change['after'])
        elif exists:
            del parent[key]
        else:
            raise ValueError('source delta cannot delete an absent field')
    return result


def verify_catalog(original, current, authored, root):
    fields(authored, {'before', 'after', 'changes', 'reviewer', 'whole_catalog_reviewed', 'provenance'}, 'catalog review')
    text(authored['reviewer'], 'catalog reviewer')
    if (authored['whole_catalog_reviewed'] is not True or not authored['provenance']
            or not isinstance(authored['provenance'], list)
            or not exact(authored['before'], original) or not exact(authored['after'], current)):
        raise ValueError('full exact before/after catalog and authored review provenance required')
    for ref in authored['provenance']: artifact(root, ref)
    result = apply_delta(original, authored['changes'])
    if not exact(result, current):
        raise ValueError('catalog additions/changes lack exact authored delta')
    import photo_slot_semantics
    for tag, spec in current.items():
        if not isinstance(spec, dict) or spec.get('id') != tag or not dr.c.TAG_ID.fullmatch(tag):
            raise ValueError('catalog spec identity mismatch')
        photo_slot_semantics.validate(tag, spec, set(current), dr.c.strings)
        dr.c.strings(spec['dimensions'], tag + '.dimensions')
        dr.c.validate_effects({'dimensions': spec['dimensions'], 'properties': []}, tag)


def compiled_bytes(root, here, locator, original_source_sha256, cid):
    """Resolve only an explicit current file or root-bound exact archived copy."""
    base = {'file', 'file_sha256', 'item', 'row_sha256'}
    if not isinstance(locator, dict) or set(locator) not in (base, base | {'archive'}):
        raise ValueError('original compiled locator: exact fields required')
    declared = path_in(root, locator['file'])
    if not declared.is_relative_to(Path(here).resolve() / 'decisions'):
        raise ValueError('original locator must address actual compiled decisions, never authored items')
    archived = locator.get('archive')
    if archived is None:
        if hashlib.sha256(declared.read_bytes()).hexdigest() != locator['file_sha256']:
            raise ValueError('original compiled artifact bytes changed; explicit archive evidence required')
        return read_json(declared)
    fields(archived, {'artifact', 'revision', 'normalization_manifest'}, 'explicit compiled archive')
    doc = artifact(root, archived['artifact']); revision = artifact(root, archived['revision'])
    manifest = artifact(root, archived['normalization_manifest'])
    archive_path = path_in(root, archived['artifact']['file'])
    revision_path = path_in(root, archived['revision']['file'])
    manifest_path = path_in(root, archived['normalization_manifest']['file'])
    if (not archive_path.is_relative_to(Path(here).resolve() / 'revisions')
            or not manifest_path.is_relative_to(Path(here).resolve() / 'worker-notes')
            or manifest_path.suffix != '.json'
            or archive_path.parent != Path(here).resolve() / 'revisions' / manifest_path.stem
            or revision_path != archive_path.parent / 'REVISION.json'
            or archive_path.name != declared.name
            or archived['artifact']['file_sha256'] != locator['file_sha256']):
        raise ValueError('compiled archive directory/name/exact original bytes mismatch')
    fields(revision, {'schema', 'root_all_worker_sources_read_claimed', 'normalization_manifest',
                      'archive_hashes', 'changes', 'native_changes_applied', 'stage05_complete'}, 'amendment revision')
    if (revision['schema'] != 'photo-codex-worker-amendment-revision/v1'
            or revision['root_all_worker_sources_read_claimed'] is not False
            or revision['native_changes_applied'] is not False or revision['stage05_complete'] is not False
            or revision['normalization_manifest'] != {'file': archived['normalization_manifest']['file'],
                                                       'sha256': archived['normalization_manifest']['sha256']}
            or revision['archive_hashes'].get(declared.name) != locator['file_sha256']):
        raise ValueError('exact root revision archive/hash/manifest binding required')
    fields(manifest, {'schema', 'normalization_author', 'worker_attestation', 'root_all_worker_sources_read_claimed',
                      'source_sha256', 'authored_document', 'worker_note', 'replacements'}, 'root normalization manifest')
    if (manifest['schema'] != 'photo-codex-sparse-amendment-normalization/v1'
            or manifest['normalization_author'] != '/root' or manifest['worker_attestation'] is not False
            or manifest['root_all_worker_sources_read_claimed'] is not False
            or manifest['source_sha256'] != original_source_sha256):
        raise ValueError('original source and explicit root normalization authority required')
    for key, folder in (('authored_document', 'authored'), ('worker_note', 'worker-notes')):
        link = manifest[key]; fields(link, {'file', 'sha256'}, 'normalization linked artifact')
        linked = path_in(root, link['file'])
        if (not linked.is_relative_to(Path(here).resolve() / folder)
                or dr.c.digest(read_json(linked)) != link['sha256']):
            raise ValueError('root normalization linked immutable artifact changed')
    replacements = [r for r in manifest['replacements'] if r.get('candidate_id') == cid]
    changes = [r for r in revision['changes'] if r.get('candidate_id') == cid]
    if len(replacements) != 1 or len(changes) != 1:
        raise ValueError('archive must bind one exact original registered row')
    entry, change = replacements[0], changes[0]
    fields(change, {'candidate_id', 'before', 'after', 'before_sha256', 'after_sha256'}, 'archived row change')
    if (entry['registered_file'] != locator['file'] or entry['registered_item'] != locator['item']
            or entry['before_registered_row_sha256'] != locator['row_sha256']
            or change['before_sha256'] != locator['row_sha256']
            or dr.c.digest(change['before']) != change['before_sha256']
            or dr.c.digest(change['after']) != change['after_sha256']
            or change['before']['candidate_id'] != cid or change['after']['candidate_id'] != cid
            or entry['previous_authored'] != change['before']['authored_decision']
            or any(not exact(change['after'].get(k), value) for k, value in entry['decision'].items())):
        raise ValueError('archive revision/normalization original file/item/row mapping mismatch')
    if (type(locator['item']) is not int or not 1 <= locator['item'] <= len(doc['decisions'])
            or not exact(doc['decisions'][locator['item'] - 1], change['before'])):
        raise ValueError('archive actual compiled item differs from preserved before row')
    return doc


def compiled_review(root, here, locator, original, cid, packet_ref, source_sha256, catalog_sha256, binding_cache):
    doc = compiled_bytes(root, here, locator, source_sha256, cid)
    if type(locator['item']) is not int or not 1 <= locator['item'] <= len(doc['decisions']):
        raise ValueError('original compiled item missing')
    row = doc['decisions'][locator['item'] - 1]
    if (dr.c.digest(row) != locator['row_sha256'] or row['candidate_id'] != cid
            or row['source_record_sha256'] != dr.c.digest(original['candidates'][cid])
            or row['catalog_sha256'] != catalog_sha256
            or row['reference_sha256'] != dr.binding(original, cid, cache=binding_cache)['reference_sha256']):
        raise ValueError('original compiled row/source/catalog/reference binding changed')
    packet = artifact(root, packet_ref)
    if (packet_ref['sha256'] != row['packet_sha256'] or packet.get('source_sha256') != source_sha256
            or packet.get('catalog_sha256') != catalog_sha256 or cid not in packet.get('ids', [])
            or not exact(packet.get('records', {}).get(cid), original['candidates'][cid])
            or not exact(packet.get('references', {}).get(cid), dr.closure(original, cid))):
        raise ValueError('original compiled review lacks its exact full historical source packet')
    authored = row['authored_decision']; authored_path = path_in(root, authored['file'])
    if not authored_path.is_relative_to(Path(here).resolve() / 'authored'):
        raise ValueError('historical authored provenance escapes authored evidence')
    item = dr.authored_item(read_json(authored_path), authored['item'])
    if dr.c.digest(item) != authored['sha256'] or any(not exact(row.get(k), value) for k, value in item.items()):
        raise ValueError('original compiled review differs from immutable authored judgement')
    return row


def validate_assignment_identity(assignment):
    """Declarations preserve known child assignment and unknown parent session.

    This validates authored identity fields; it does not observe a model session.
    """
    text(assignment['task_name'],'assigned task')
    pair=(assignment['model'],assignment['reasoning_effort'])
    expected=(('session_model_unspecified','session_effort_unspecified') if assignment['task_name']=='/root'
              else ('gpt-6.1-sol','high'))
    if pair!=expected:raise ValueError('exact root unspecified session or child gpt-6.1-sol/high assignment required')


def verify_batch(assignment_path, batch_path, note_path, *, root=None, here=None):
    root = Path(root or dr.ROOT).resolve(); here = Path(here or dr.HERE).resolve()
    assignment = read_json(path_in(root, str(assignment_path)))
    fields(assignment, {'schema', 'actor', 'task_name', 'model', 'reasoning_effort', 'ids', 'ordinals', 'input'}, 'root assignment')
    if assignment['schema'] != ASSIGNMENT or assignment['actor'] != '/root':
        raise ValueError('exact root authored assignment required')
    validate_assignment_identity(assignment)
    inp = artifact(root, assignment['input'])
    fields(inp, {'schema', 'actor', 'ids', 'original_snapshot', 'current_snapshot', 'order',
                 'catalog_review', 'original_decisions', 'original_packets', 'required_revisions'}, 'native input')
    if inp['schema'] != INPUT or inp['actor'] != '/root':
        raise ValueError('root-authored native input required')
    original = artifact(root, inp['original_snapshot']); current = artifact(root, inp['current_snapshot'])
    for snapshot in (original, current):
        fields(snapshot, dr.c.CORPUS_FIELDS, 'full corpus snapshot')
        if (snapshot['schema'] != dr.c.SCHEMA
                or any(not isinstance(snapshot[k], dict) for k in ('candidates','slot_catalog','slot_bindings','policies'))
                or any(not dr.c.ID.fullmatch(cid) or not isinstance(record, dict) or record.get('id') != cid
                       for cid, record in snapshot['candidates'].items())):
            raise ValueError('full snapshot canonical identity inventory invalid')
    order = artifact(root, inp['order']); ids = assignment['ids']; ordinals = assignment['ordinals']
    if (not isinstance(ids, list) or not ids or len(ids) != len(set(ids)) or ids != inp['ids']
            or not isinstance(ordinals, list) or len(ordinals) != len(ids)
            or any(type(o) is not int or o < 0 or o >= len(order) for o in ordinals)
            or [order[o] for o in ordinals] != ids or len(order) != len(set(order))
            or set(order) != set(original['candidates']) or set(order) != set(current['candidates'])
            or set(inp['original_decisions']) != set(ids) or set(inp['original_packets']) != set(ids)
            or not set(inp['required_revisions']) <= set(ids)):
        raise ValueError('exact source inventory/assigned ID ordinal/input closure required')
    verify_catalog(original['slot_catalog'], current['slot_catalog'], inp['catalog_review'], root)
    batch = read_json(path_in(root, str(batch_path))); note = read_json(path_in(root, str(note_path)))
    fields(batch, {'schema', 'task_name', 'model', 'reasoning_effort', 'assignment_sha256', 'input_sha256',
                   'prepared_count', 'actual_read_count', 'records'}, 'worker native batch')
    fields(note, {'schema', 'task_name', 'model', 'reasoning_effort', 'assignment_sha256', 'input_sha256',
                  'batch_sha256', 'prepared_count', 'actual_read_count', 'whole_source_read_ids', 'whole_dependency_read_ids'}, 'worker read attestation')
    for value, schema in ((batch, BATCH), (note, NOTE)):
        if (value['schema'] != schema or any(value[k] != assignment[k] for k in ('task_name', 'model', 'reasoning_effort'))
                or value['assignment_sha256'] != dr.c.digest(assignment)
                or value['input_sha256'] != assignment['input']['sha256']
                or type(value['prepared_count']) is not int or value['prepared_count'] != len(ids)):
            raise ValueError('worker task/input/assignment/prepared-count binding changed')
    if note['batch_sha256'] != dr.c.digest(batch) or not isinstance(batch['records'], list):
        raise ValueError('native batch/read-note binding changed')
    rows = batch['records']
    if len(rows) != len(ids) or [r['candidate_id'] for r in rows] != ids:
        raise ValueError('every prepared candidate needs an explicit status row')
    original_sha256 = dr.c.digest(original); original_catalog_sha256 = dr.c.digest(original['slot_catalog']); binding_cache = {}
    read_ids, dependency_read_ids, reviewed, status_counts = [], [], {}, dict.fromkeys(STATUSES, 0)
    for cid, ordinal, row in zip(ids, ordinals, rows):
        fields(row, {'candidate_id', 'ordinal', 'status', 'rationale', 'source_before', 'source_after', 'delta',
                     'original_compiled', 'proof', 'dependency_records', 'reference_bindings',
                     'source_reread_complete', 'reference_reread_complete', 'revision'}, 'native review row')
        text(row['rationale'], 'individual native judgement')
        if type(row['ordinal']) is not int or row['ordinal'] != ordinal or row['status'] not in STATUSES:
            raise ValueError('explicit native status/ordinal required; shape does not approve')
        if any(type(row[k]) is not bool for k in ('source_reread_complete', 'reference_reread_complete')):
            raise ValueError('explicit complete-reading booleans required')
        if row['source_reread_complete']: read_ids.append(cid)
        if row['reference_reread_complete']: dependency_read_ids.append(cid)
        if row['status'] != 'pending' and not (row['source_reread_complete'] and row['reference_reread_complete']):
            raise ValueError('approval requires attested whole source and dependency reading')
        before, after = row['source_before'], row['source_after']
        fields(after, {'id', 'record_kind', 'content', 'conditions', 'effects', 'provenance'}, 'native full after source')
        if not isinstance(after['content'], dict) or not isinstance(after['provenance'], list):
            raise ValueError('native source content/provenance types invalid')
        if (not exact(before, original['candidates'][cid]) or not exact(after, current['candidates'][cid])
                or not exact(apply_delta(before, row['delta']), after)
                or after['id'] != cid or after['record_kind'] not in dr.c.KINDS
                or after['provenance'][:len(before['provenance'])] != before['provenance']):
            raise ValueError('full source before/after/delta/identity/original provenance mismatch')
        dr.c.validate_conditions(after['conditions'], cid); dr.c.validate_effects(after['effects'], cid)
        loc = row['original_compiled']
        if not exact(loc, inp['original_decisions'][cid]):
            raise ValueError('worker changed root-assigned original compiled locator')
        old = compiled_review(root, here, loc, original, cid, inp['original_packets'][cid], original_sha256, original_catalog_sha256, binding_cache)
        # Follow candidate references AND explicit binding guards, including CIDs
        # reached only through binding definitions. Never infer/retarget bindings.
        ref_hashes = native.referenced_records(after, current)
        closure = {key: current['candidates'][key] for key in ref_hashes if dr.c.ID.fullmatch(key)}
        closure_bindings = {key: current['slot_bindings'][key] for key in ref_hashes if dr.c.BINDING_ID.fullmatch(key)}
        dependencies = row['dependency_records']
        if not isinstance(dependencies, dict) or set(dependencies) != set(closure):
            raise ValueError('complete native reference source closure required')
        for key, reference in dependencies.items():
            plain = copy.deepcopy(reference); plain['content'].pop('role_evidence', None)
            expected = copy.deepcopy(closure[key]); expected['content'].pop('role_evidence', None)
            if not exact(plain, expected):
                raise ValueError('native dependency full source changed')
        if not exact(row['reference_bindings'], closure_bindings):
            raise ValueError('complete exact dependency binding definitions required')
        required = inp['required_revisions'].get(cid)
        revision = row['revision']
        if required is not None:
            fields(required, {'prior_review', 'memo_artifacts', 'reason'}, 'required native revision')
            text(required['reason'], 'revision requirement')
            fields(required['prior_review'], {'artifact', 'pointer', 'sha256'}, 'prior immutable native judgement')
            previous = artifact(root, required['prior_review']['artifact'])
            for part in pointer_parts(required['prior_review']['pointer']):
                try: previous = previous[int(part)] if isinstance(previous, list) else previous[part]
                except (KeyError, IndexError, TypeError, ValueError) as exc:
                    raise ValueError('prior native judgement pointer missing') from exc
            if (dr.c.digest(previous) != required['prior_review']['sha256'] or not required['memo_artifacts']):
                raise ValueError('required revision needs exact prior judgement and explicit memo binding')
        if revision is not None:
            fields(revision, {'prior_review', 'memo_artifacts', 'rationale'}, 'worker revision')
            text(revision['rationale'], 'worker revision rationale')
            if (required is None or not exact(revision['prior_review'], required['prior_review'])
                    or not exact(revision['memo_artifacts'], required['memo_artifacts'])):
                raise ValueError('worker revision must match explicit root-required revision')
            for ref in revision['memo_artifacts']: artifact(root, ref)
        elif required is not None:
            raise ValueError('explicit worker revision required; frozen shape-valid proof cannot waive memo')
        proof = row['proof']
        if proof is None:
            if row['status'] != 'pending':
                raise ValueError('explicit native proof required for approval')
        else:
            if not (row['source_reread_complete'] and row['reference_reread_complete']):
                raise ValueError('new native proof requires complete source and dependency read attestation')
            if not isinstance(proof, dict) or proof.get('schema') != native.SCHEMA:
                raise ValueError('native v4 proof required; no version fallback')
            provenance = proof.get('review', {}).get('original_review')
            expected = {'candidate_id': cid, 'source_record_sha256': old['source_record_sha256'],
                        'catalog_sha256': old['catalog_sha256'], 'decision_sha256': loc['row_sha256'],
                        'artifact': loc['file'] + '#item=' + str(loc['item'])}
            if not exact(provenance, expected):
                raise ValueError('native proof must preserve actual original compiled file#item provenance')
            nr = proof.get('review', {}).get('native_review', {})
            method = ('codex_direct_source_read' if assignment['task_name'] == '/root'
                      else 'codex_subagent_direct_source_read')
            if nr.get('reviewer') != assignment['task_name'] or nr.get('method') != method:
                raise ValueError('native proof reviewer/method must match the exact root or child assignment')
            correction = proof.get('review', {}).get('source_correction')
            if native.meaning_sha256(before) != native.meaning_sha256(after):
                if not isinstance(correction, dict) or correction.get('before_sha256') != native.meaning_sha256(before):
                    raise ValueError('native full-meaning correction must retain exact original hash')
            elif correction is not None:
                raise ValueError('unchanged full meaning cannot claim correction')
            record = copy.deepcopy(after); record['content']['role_evidence'] = proof
            corpus = {**current, 'candidates': {**current['candidates'], **copy.deepcopy(dependencies), cid: record}}
            native.validate(record, current['slot_catalog'], corpus=corpus)
            if row['status'] == 'approved' and (after['record_kind'] == 'diagnostic' or not proof['roles'] or not proof['facts']):
                raise ValueError('positive native approval needs explicit positive roles and facts')
            if row['status'] == 'diagnostic_reviewed' and (after['record_kind'] != 'diagnostic' or proof['roles'] or proof['facts']):
                raise ValueError('diagnostic native judgement cannot have positive roles/facts')
        status_counts[row['status']] += 1; reviewed[cid] = copy.deepcopy(row)
    actual = len(read_ids)
    if (any(type(v['actual_read_count']) is not int or v['actual_read_count'] != actual for v in (batch, note))
            or note['whole_source_read_ids'] != read_ids or note['whole_dependency_read_ids'] != dependency_read_ids):
        raise ValueError('prepared count and actual complete read attestation differ')
    return {'schema': 'photo-codex-native-batch-verification/v1', 'assignment_sha256': dr.c.digest(assignment),
            'input_sha256': assignment['input']['sha256'], 'batch_sha256': dr.c.digest(batch),
            'note_sha256': dr.c.digest(note), 'original_source_sha256': dr.c.digest(original),
            'current_source_sha256': dr.c.digest(current), 'catalog_sha256': dr.c.digest(current['slot_catalog']),
            'policies_sha256': dr.c.digest(current['policies']),
            'prepared_count': len(ids), 'actual_read_count': actual, 'statuses': status_counts,
            'records': reviewed, 'shape_valid': True, 'root_accepted': False,
            'operational_native_qualified_count': 0, 'semantic_accuracy_certified': False}


def verify_acceptance(root, ref, verified):
    acceptance = artifact(root, ref)
    fields(acceptance, {'schema', 'actor', 'assignment_sha256', 'input_sha256', 'batch_sha256',
                        'note_sha256', 'reviews', 'reason'}, 'root native batch acceptance')
    text(acceptance['reason'], 'root acceptance reason')
    if (acceptance['schema'] != ACCEPTANCE or acceptance['actor'] != '/root'
            or any(acceptance[k] != verified[k] for k in ('assignment_sha256', 'input_sha256', 'batch_sha256', 'note_sha256'))
            or acceptance['reviews'] != {cid: {'review_sha256': dr.c.digest(row), 'status': row['status']}
                                         for cid, row in verified['records'].items()}):
        raise ValueError('separate root acceptance must bind every exact worker judgement/status')
    return acceptance


def verify_latest(manifest_path, *, root=None, here=None, expected_count=PRODUCTION_COUNT):
    """Pure full-inventory gate for a future adoption-v2 consumer. No registry writes."""
    root = Path(root or dr.ROOT).resolve(); here = Path(here or dr.HERE).resolve()
    manifest = read_json(path_in(root, str(manifest_path)))
    fields(manifest, {'schema', 'actor', 'original_snapshot', 'current_snapshot', 'order', 'batches', 'reason'}, 'latest native review manifest')
    text(manifest['reason'], 'latest selection reason')
    if manifest['schema'] != LATEST or manifest['actor'] != '/root':
        raise ValueError('explicit root latest-native selection required')
    original = artifact(root, manifest['original_snapshot']); current = artifact(root, manifest['current_snapshot']); order = artifact(root, manifest['order'])
    for snapshot in (original,current):
        fields(snapshot,dr.c.CORPUS_FIELDS,'latest full corpus snapshot')
        if snapshot['schema'] != dr.c.SCHEMA: raise ValueError('latest full current corpus schema required')
    if (type(expected_count) is not int or expected_count < 1 or len(order) != expected_count
            or len(order) != len(set(order)) or set(order) != set(current['candidates']) or not manifest['batches']):
        raise ValueError('all18250 exact IDs/full current source required')
    combined = {}; history = []
    for entry in manifest['batches']:
        fields(entry, {'assignment', 'batch', 'note', 'acceptance'}, 'latest accepted batch')
        for key in ('assignment', 'batch', 'note'): artifact(root, entry[key])
        verified = verify_batch(*(entry[k]['file'] for k in ('assignment', 'batch', 'note')), root=root, here=here)
        verify_acceptance(root, entry['acceptance'], verified)
        if (verified['original_source_sha256'] != dr.c.digest(original)
                or verified['policies_sha256'] != dr.c.digest(current['policies'])
                or verified['catalog_sha256'] != dr.c.digest(current['slot_catalog'])
                or set(combined) & set(verified['records'])):
            raise ValueError('latest batches conflict, overlap or bind stale original source/policies/catalog')
        combined.update(verified['records']); history.append(verified)
    if set(combined) != set(order) or any(r['status'] == 'pending' for r in combined.values()):
        raise ValueError('exact latest native inventory with pending0 required')
    # Historical whole snapshots stay as actually read. Reuse is allowed only
    # when each contributing full CID and its complete reference closure equals
    # the final root snapshot, with exactly the accepted latest child proofs.
    qualified = {**current, 'candidates': {**current['candidates']}}
    for cid, row in combined.items():
        if not exact(row['source_after'], current['candidates'][cid]):
            raise ValueError('latest candidate full after source differs from final current source')
        hashes = native.referenced_records(current['candidates'][cid], current)
        refs = {key: current['candidates'][key] for key in hashes if dr.c.ID.fullmatch(key)}
        bindings = {key: current['slot_bindings'][key] for key in hashes if dr.c.BINDING_ID.fullmatch(key)}
        if set(row['dependency_records']) != set(refs) or not exact(row['reference_bindings'], bindings):
            raise ValueError('latest full reference closure or guard binding differs from final current source')
        for child, reference in row['dependency_records'].items():
            plain = copy.deepcopy(reference); plain['content'].pop('role_evidence', None)
            expected = copy.deepcopy(refs[child]); expected['content'].pop('role_evidence', None)
            if not exact(plain, expected):
                raise ValueError('latest dependency full source differs from final current source')
            if not exact(reference.get('content', {}).get('role_evidence'), combined[child]['proof']):
                raise ValueError('dependency proof differs from root-accepted latest child review')
        record = copy.deepcopy(row['source_after'])
        record['content']['role_evidence'] = copy.deepcopy(row['proof'])
        qualified['candidates'][cid] = record
    for record in qualified['candidates'].values():
        native.validate(record, current['slot_catalog'], corpus=qualified)
    return {'schema': 'photo-codex-latest-native-verified/v1', 'manifest_sha256': dr.c.digest(manifest),
            'original_source_sha256': dr.c.digest(original),
            'current_source_sha256': dr.c.digest(current), 'catalog_sha256': dr.c.digest(current['slot_catalog']),
            'policies_sha256': dr.c.digest(current['policies']),
            'records': combined, 'batch_verifications': history, 'pending_count': 0,
            'root_accepted': True, 'production_count_gate': expected_count == PRODUCTION_COUNT,
            'operational_native_qualified_count': 0, 'canonical_applied': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assignment'); parser.add_argument('--batch'); parser.add_argument('--note')
    parser.add_argument('--latest-manifest')
    args = parser.parse_args()
    if args.latest_manifest:
        if any((args.assignment, args.batch, args.note)): parser.error('choose latest manifest or one batch')
        result = verify_latest(args.latest_manifest)
    else:
        if not all((args.assignment, args.batch, args.note)): parser.error('explicit assignment, batch and note required')
        result = verify_batch(args.assignment, args.batch, args.note)
    print(json.dumps({k:v for k,v in result.items() if k not in {'records', 'batch_verifications'}}, sort_keys=True))


if __name__ == '__main__': main()
