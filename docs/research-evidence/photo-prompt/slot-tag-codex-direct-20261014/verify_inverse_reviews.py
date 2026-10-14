"""Read-only, manifest-bound checks of three authored inverse-review formats.

No discovery, inference, verdict conversion, source editing or publication occurs.
A successful result certifies mechanical bindings and declared coverage only.
See worker-notes/inverse-review-verifier-contract-20261014.md for the manifest,
and its contract-supplement-v2-20261014 note for the bounded wire revision.
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

SCHEMA = 'photo-direct-inverse-review-selection/v1'
CONTRACT_REVISION = 'bounded-wire-2'
BRANCH_CONCEPT_UNIT = re.compile(
    r'/effects/realizations/branches/(0|[1-9][0-9]*)/concept_units/(0|[1-9][0-9]*)')
FORMATS = {
    '09250-flat': 'photo-codex-direct-inverse-semantic-review-checkpoint/v1',
    '11870-slots': 'photo-inverse-direct-semantic-investigation/v1',
    '07250-rows': 'photo-direct-blind-inverse-adjudication/v1',
}
CID = re.compile(r'cand_[0-9a-f]{32}')
BID = re.compile(r'bind_[0-9a-f]{32}')
SHA = re.compile(r'[0-9a-f]{64}')
METADATA = frozenset({
    'activation', 'aliases', 'keywords', 'terms', 'concept_terms', 'match_terms',
    'any_terms', 'all_terms', 'exact_terms', 'evidence_terms', 'must_mention_any',
    'context_terms', 'project_glossary_aliases', 'evidence_fields',
    'required_evidence_fields', 'claim_limits', 'research_claim_limits',
    'negative', 'negative_prompt', 'negative_prompts', 'excludes', 'avoid',
    'avoid_terms', 'routing', 'routing_metadata', 'review', 'reviews',
    'review_metadata', 'facets', 'tags', 'slot_tags', 'retrieval_metadata',
    'source_id',
    'id', 'priority', 'priority_dimension', 'family_ids', 'topic_ids',
    'conditions', 'validation', 'validation_rules', 'provenance', 'acceptance',
    'applicability', 'retrieval_policy', 'affected_dimensions', 'affected_properties',
    'dimensions', 'properties', 'evidence_field', 'contract_version', 'schema',
    'ids', 'priority_dimensions', 'selection_contract', 'profile_activation',
    'adoption', 'source_sha256', 'schema_version',
    'confusion_boundaries', 'research_confusions', 'confounders', 'failure_modes',
    'excluded', 'exclusions', 'forbidden', 'research_source_urls',
    'reject_substitutes', 'contrast_examples', 'forbidden_prompt_terms',
    'runtime_forbidden_labels', 'role_evidence', 'semantic_review',
})


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def byte_digest(value):
    return hashlib.sha256(value).hexdigest()


def _unique_object(items):
    obj = {}
    for key, value in items:
        if key in obj:
            raise ValueError('duplicate JSON key: ' + key)
        obj[key] = value
    return obj


def load_json(raw):
    return json.loads(raw, object_pairs_hook=_unique_object,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def pointer(value, path):
    if not isinstance(path, str) or not path.startswith('/'):
        raise ValueError('absolute JSON pointer required')
    for encoded in path[1:].split('/'):
        if re.search(r'~(?![01])', encoded):
            raise ValueError('invalid pointer escape')
        key = encoded.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            if not re.fullmatch(r'0|[1-9][0-9]*', key):
                raise ValueError('noncanonical array index')
            value = value[int(key)]
        elif isinstance(value, dict):
            value = value[key]
        else:
            raise ValueError('pointer crosses scalar')
    return value


def branch_positive_binding(record, path, rids):
    """Resolve only a canonical branch's explicit positive concept-unit string."""
    match = BRANCH_CONCEPT_UNIT.fullmatch(path) if isinstance(path, str) else None
    if not match or not isinstance(record, dict):
        return None
    try:
        conditional = record['effects']['realizations']
        if conditional['mode'] not in {'one', 'optional'}:
            return None
        branches = conditional['branches']
        branch_index, unit_index = map(int, match.groups())
        branch = branches[branch_index]
        rid = branch['id']
        ids = [x['id'] for x in branches]
        value = branch['concept_units'][unit_index]
        if (len(ids) != len(set(ids)) or not isinstance(rid, str) or not rid.strip()
                or rid == 'base' or rid not in rids
                or not isinstance(value, str) or not value.strip()):
            return None
        return {'candidate_id': record['id'], 'source_sha256': digest(record),
                'pointer': path, 'surface': 'canonical_branch_concept_unit',
                'branch_index': branch_index, 'concept_unit_index': unit_index,
                'realization_id': rid}
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def positive_path(path, *, record=None, rids=()):
    """Excludes metadata, with one source/RID-bound branch-positive surface."""
    if branch_positive_binding(record, path, rids) is not None:
        return True
    if not isinstance(path, str) or not path.startswith('/content/'):
        return False
    bits = path[1:].split('/')
    for index, encoded in enumerate(bits):
        key = encoded.replace('~1', '/').replace('~0', '~').lower()
        if index and bits[index - 1] == 'realization_content':
            continue  # a selected actual RID may itself be named "negative", etc.
        if key in METADATA or key.endswith(('_id', '_ids')):
            return False
    return True


def references(value):
    candidates, bindings = set(), set()
    if isinstance(value, str):
        if CID.fullmatch(value):
            candidates.add(value)
        elif BID.fullmatch(value):
            bindings.add(value)
    elif isinstance(value, dict):
        for key, child in value.items():
            for item in (key, child):
                found_candidates, found_bindings = references(item)
                candidates.update(found_candidates)
                bindings.update(found_bindings)
    elif isinstance(value, list):
        for child in value:
            found_candidates, found_bindings = references(child)
            candidates.update(found_candidates)
            bindings.update(found_bindings)
    return candidates, bindings


def closure(source, cid):
    """Full CID and binding-definition closure, never a binding-as-identity shortcut."""
    records, bindings = source['candidates'], source['slot_bindings']
    seen, seen_bindings, pending = set(), set(), [('candidate', cid)]
    while pending:
        kind, ident = pending.pop()
        visited = seen if kind == 'candidate' else seen_bindings
        if ident in visited:
            continue
        visited.add(ident)
        value = (records if kind == 'candidate' else bindings)[ident]
        candidates, binding_ids = references(value)
        pending.extend(('candidate', x) for x in candidates if x not in seen)
        pending.extend(('binding', x) for x in binding_ids if x not in seen_bindings)
    seen.remove(cid)
    return ({x: digest(records[x]) for x in sorted(seen)},
            {x: digest(bindings[x]) for x in sorted(seen_bindings)})


def realization_effects(record):
    effects = record['effects']
    branches = effects.get('realizations', [])
    if isinstance(branches, dict):
        # Native source stores the realization mode beside a branches list.
        branches = branches['branches']
    mode = effects.get('realizations', {}).get('mode', 'optional')
    result = {}
    if not branches or mode == 'optional':
        result['base'] = {k: copy.deepcopy(effects.get(k, [])) for k in ['dimensions', 'properties']}
    for branch in branches:
        selected = {}
        branch_effects = branch['effects']
        for key in ['dimensions', 'properties']:
            selected[key] = []
            for value in effects.get(key, []) + branch_effects.get(key, []):
                if value not in selected[key]:
                    selected[key].append(copy.deepcopy(value))
        selected['dimensions'] = sorted(selected['dimensions'])
        result[branch['id']] = selected
    return result


def _list_ids(value):
    return [x['document_id'] if isinstance(x, dict) else x for x in value]


def _top3(search):
    return {'bm25f': _list_ids(search['lanes']['bm25f']['ranks'][:3]),
            'dense': _list_ids(search['lanes']['embedding']['ranks'][:3]),
            'rrf': _list_ids(search['rrf'][:3])}


def _jsonable(value):
    if isinstance(value, set):
        return [_jsonable(x) for x in sorted(value)]
    if isinstance(value, (list, tuple)):
        return [_jsonable(x) for x in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


def _literal_name(value):
    return isinstance(value, str) and bool(value.strip()) and '*' not in value and not value.endswith('.')


class Verifier:
    def __init__(self, root, manifest, manifest_sha256):
        self.root_given = Path(root).absolute()
        self.root = self.root_given.resolve()
        self.manifest_path = self.safe_path(manifest)
        raw = self.manifest_path.read_bytes()
        if not SHA.fullmatch(manifest_sha256) or byte_digest(raw) != manifest_sha256:
            raise ValueError('selection manifest byte SHA mismatch')
        self.manifest = load_json(raw)
        if not isinstance(self.manifest, dict) or self.manifest.get('schema') != SCHEMA:
            raise ValueError('unsupported selection schema')
        if (not isinstance(self.manifest.get('artifacts'), dict) or not self.manifest['artifacts']
                or not isinstance(self.manifest.get('inputs'), dict)
                or set(self.manifest['inputs']) != {'delegation', 'search', 'plan', 'source', 'proposed_catalog'}
                or not isinstance(self.manifest.get('reviews'), list) or not self.manifest['reviews']):
            raise ValueError('selection requires explicit artifacts, five inputs and nonempty reviews')
        self.manifest_sha256 = manifest_sha256
        self.failures = []
        self.artifacts = {}
        self.by_path = {}
        self.rows = []
        self.reads = []
        self.summaries = []
        self.actual_pairs = []
        self.source_hashes = {}
        self.closure_cache = {}

    def safe_path(self, name):
        p = Path(name)
        if '..' in p.parts:
            raise ValueError('parent traversal disallowed')
        if p.is_absolute() and p.is_relative_to(self.root_given):
            p = self.root / p.relative_to(self.root_given)
        p = p if p.is_absolute() else self.root / p
        resolved = p.resolve()
        if not resolved.is_relative_to(self.root):
            raise ValueError('artifact outside selected root')
        # No symlink-based redirection even to another file within the root.
        q = p
        while q != self.root and q != q.parent:
            if q.is_symlink():
                raise ValueError('symlink artifact disallowed')
            q = q.parent
        return resolved

    def check(self, condition, code, context='', **details):
        if not condition:
            self.failures.append({'code': code, 'context': context, **_jsonable(details)})
        return bool(condition)

    def equal(self, actual, expected, code, context=''):
        return self.check(canonical(_jsonable(actual)) == canonical(_jsonable(expected)),
                          code, context, actual=actual, expected=expected)

    def field(self, obj, names, context, *, optional=False):
        present = [key for key in names if key in obj]
        if not present:
            if optional:
                return None
            raise KeyError('missing explicit field: ' + '/'.join(names))
        value = obj[present[0]]
        for key in present[1:]:
            self.equal(obj[key], value, 'conflicting_compatibility_fields', context + ':' + key)
        return value

    def artifact(self, ident):
        return self.artifacts[ident]['value']

    def declared_reference(self, path, context):
        """Find an already-selected artifact, without opening or probing that path."""
        p = Path(path)
        names = [p] if p.is_absolute() else [self.root / p, self.manifest_path.parent / p]
        matches = {self.by_path[str(x.absolute())] for x in names if str(x.absolute()) in self.by_path}
        if not self.check(len(matches) == 1, 'undeclared_or_ambiguous_reference', context, path=path):
            return None
        return self.artifacts[next(iter(matches))]

    def load_artifacts(self):
        for ident, desc in self.manifest['artifacts'].items():
            try:
                path = self.safe_path(desc['path'])
                if not self.check(str(path) not in self.by_path, 'duplicate_artifact_path', ident):
                    continue
                raw = path.read_bytes()
                self.equal(byte_digest(raw), desc['byte_sha256'], 'artifact_byte_sha256', ident)
                if 'size_bytes' in desc:
                    self.equal(len(raw), desc['size_bytes'], 'artifact_size', ident)
                encoding = desc['encoding']
                if encoding == 'bytes':
                    value = None
                elif encoding in ('json', 'gzip-json'):
                    value = load_json(gzip.decompress(raw) if encoding == 'gzip-json' else raw)
                    self.equal(digest(value), desc['canonical_sha256'], 'artifact_canonical_sha256', ident)
                else:
                    raise ValueError('unknown artifact encoding')
                self.artifacts[ident] = {'path': str(path), 'byte_sha256': byte_digest(raw),
                                         'canonical_sha256': digest(value) if value is not None else None,
                                         'size_bytes': len(raw), 'value': value, 'descriptor': desc}
                self.by_path[str(path)] = ident
            except (KeyError, ValueError, OSError, TypeError) as exc:
                self.check(False, 'artifact_load', ident, detail=str(exc))
        # A newly measured mutable writer cannot establish its own historical hash.
        for ident, artifact in self.artifacts.items():
            desc = artifact['descriptor']
            if Path(artifact['path']).suffix == '.py' or desc.get('mutable_auxiliary'):
                try:
                    witness = desc['initial_hash_witness']
                    self.check(witness['artifact'] != ident, 'self_attested_initial_hash', ident)
                    declared = pointer(self.artifact(witness['artifact']), witness['pointer'])
                    self.equal(artifact['byte_sha256'], declared, 'closed_initial_auxiliary_mutated', ident)
                except (KeyError, ValueError, TypeError, IndexError) as exc:
                    self.check(False, 'missing_initial_auxiliary_hash_witness', ident, detail=str(exc))

    def inputs(self):
        ids = self.manifest['inputs']
        self.delegation, self.search, self.plan, self.source, self.proposed = [
            self.artifact(ids[k]) for k in ['delegation', 'search', 'plan', 'source', 'proposed_catalog']]
        d, s, p = self.delegation, self.search, self.plan
        self.equal(d['schema'], 'photo-codex-inverse-review-delegation/v1', 'delegation_schema')
        self.equal(s['schema'], 'photo-direct-inverse-search-results/v1', 'search_schema')
        self.equal(p['schema'], 'photo-direct-inverse-query-plan/v1', 'plan_schema')
        self.equal(d['model'], 'gpt-6.1-sol', 'delegation_model')
        self.equal(d['reasoning_effort'], 'high', 'delegation_effort')
        self.equal(d['review_method'], 'codex_subagent_direct_source_read', 'delegation_method')
        for key, val in [('prepared_is_not_direct_read', True), ('canonical_changes_allowed', False),
                         ('model_or_network_calls_allowed', False)]:
            self.equal(d[key], val, 'delegation_boundary', key)
        self.source_sha = digest(self.source)
        self.catalog = self.source['slot_catalog']
        self.catalog_sha = digest(self.catalog)
        self.proposed_catalog = self.proposed['catalog']
        self.proposed_sha = digest(self.proposed_catalog)
        self.slots = sorted(self.catalog)
        self.equal(self.proposed['original_catalog_sha256'], self.catalog_sha, 'proposal_original_catalog')
        self.equal(self.proposed['proposed_catalog_sha256'], self.proposed_sha, 'proposal_catalog')
        self.equal(len(self.slots), d['slot_count'], 'delegation_slot_count')
        for key, actual in [('original_slot_count', len(self.catalog)), ('proposed_slot_count', len(self.proposed_catalog))]:
            if key in self.proposed:
                self.equal(self.proposed[key], actual, 'proposal_slot_count', key)
        positives = sorted(cid for cid, row in self.source['candidates'].items() if row['record_kind'] != 'diagnostic')
        self.equal(len(positives), d['positive_count'], 'delegation_positive_count')
        for key, actual in [('source_sha256', self.source_sha), ('catalog_sha256', self.catalog_sha)]:
            for label, obj in [('delegation', d), ('search', s), ('plan', p)]:
                self.equal(obj[key], actual, 'input_binding_' + key, label)
        for key in ['binding_sha256', 'index_sha256', 'index_source_sha256', 'space_sha256', 'space']:
            self.equal(s[key], p[key], 'search_plan_binding', key)
        self.equal(s['binding_sha256'], digest(self.source['slot_bindings']), 'source_binding_digest')
        self.equal(s['space_sha256'], digest(s['space']), 'space_digest')
        plan_without_hash = {k: v for k, v in p.items() if k != 'canonical_sha256'}
        self.equal(p['canonical_sha256'], digest(plan_without_hash), 'plan_declared_canonical')
        self.equal(s['plan_sha256'], p['canonical_sha256'], 'search_plan_canonical')
        for key, input_key in [('search_file', 'search'), ('plan_file', 'plan')]:
            a = self.artifacts[ids[input_key]]
            ref = self.declared_reference(d[key], 'delegation.' + key)
            if ref:
                self.equal(ref['path'], a['path'], 'delegation_input_path', key)
            self.equal(d[key + '_sha256'], a['byte_sha256'], 'delegation_input_bytes', key)
        self.equal([x['slot_id'] for x in p['queries']], self.slots, 'sorted_plan_slots')
        self.equal([x['slot_id'] for x in s['searches']], self.slots, 'sorted_search_slots')
        self.searches = {x['slot_id']: x for x in s['searches']}
        self.queries = {x['slot_id']: x for x in p['queries']}
        for slot in self.slots:
            sr, query = self.searches[slot], self.queries[slot]
            self.equal(sr['query_sha256'], query['text_sha256'], 'saved_query_binding', slot)
            self.equal(sr['slot_spec_sha256'], query['binding']['slot_spec_sha256'], 'saved_spec_binding', slot)
            self.equal(query['binding']['slot_spec_sha256'], digest(query['specification']), 'query_spec_digest', slot)
            self.equal(sr['search_scope'], 'whole_shared_positive_corpus', 'search_scope', slot)
            self.equal(sr['tag_admission_filter'], False, 'search_tag_admission_filter', slot)
            for lane, lane_ids in _top3(sr).items():
                self.equal(len(lane_ids), len(set(lane_ids)), 'duplicate_top3_lane_id', slot + '.' + lane)
                self.check(set(lane_ids) <= set(positives), 'nonpositive_top3_id', slot + '.' + lane)
            for cid in set(sum(_top3(sr).values(), [])):
                self.equal(sr['source_ids'][cid]['authored_record_sha256'], self.record_sha(cid), 'search_record_hash', slot + ':' + cid)
        self.assignments = {x['task']: [x['start'], x['stop']] for x in d['assignments']}
        self.equal(len(self.assignments), len(d['assignments']), 'duplicate_task_assignment')
        assigned = [i for bounds in self.assignments.values() for i in range(*bounds)]
        self.equal(sorted(assigned), list(range(len(self.slots))), 'assignment_partition')

    def required_closure(self, cid):
        if cid not in self.closure_cache:
            self.closure_cache[cid] = closure(self.source, cid)
        return self.closure_cache[cid]

    def record_sha(self, cid):
        if cid not in self.source_hashes:
            self.source_hashes[cid] = digest(self.source['candidates'][cid])
        return self.source_hashes[cid]

    def check_worker_bindings(self, data, fmt, context):
        ids = self.manifest['inputs']
        if fmt == '11870-slots':
            hashes = data['input_hashes']
            for path, value in hashes.items():
                if isinstance(value, dict):
                    artifact = self.declared_reference(path, context)
                    if artifact:
                        self.equal(value['bytes_sha256'], artifact['byte_sha256'], 'worker_input_bytes', context + ':' + path)
                else:
                    expected = {'source_canonical_sha256': self.source_sha,
                                'catalog139_canonical_sha256': self.catalog_sha,
                                'proposed141_catalog_canonical_sha256': self.proposed_sha}
                    if path in expected:
                        self.equal(value, expected[path], 'worker_input_canonical', context + ':' + path)
            selected_input_paths = {self.artifacts[ids[k]]['path'] for k in ['source', 'plan', 'search', 'proposed_catalog']}
            declared_input_paths = set()
            for path, val in hashes.items():
                if isinstance(val, dict):
                    artifact = self.declared_reference(path, context + '.required_inputs')
                    if artifact:
                        declared_input_paths.add(artifact['path'])
            self.check(selected_input_paths <= declared_input_paths, 'missing_worker_file_input_binding', context)
            for key in ['source_canonical_sha256', 'catalog139_canonical_sha256', 'proposed141_catalog_canonical_sha256']:
                self.check(key in hashes, 'missing_worker_input_binding', context + ':' + key)
        else:
            bindings = [('source_sha256' if fmt == '09250-flat' else 'baseline_source_sha256', self.source_sha),
                        ('baseline_catalog_sha256', self.catalog_sha)]
            if fmt == '09250-flat':
                bindings += [('proposed_catalog_sha256', self.proposed_sha),
                             ('search_result_sha256', self.artifacts[ids['search']]['byte_sha256']),
                             ('query_plan_sha256', self.artifacts[ids['plan']]['byte_sha256'])]
            else:
                bindings += [('baseline_index_sha256', self.search['index_sha256'])]
            for key, val in bindings:
                self.equal(data[key], val, 'worker_input_binding', context + ':' + key)
        if 'packet' in data:
            packet = data['packet']
            a = self.declared_reference(packet['path'], context + '.packet')
            if a:
                self.equal(packet['raw_sha256'], a['byte_sha256'], 'packet_bytes', context)
                self.equal(packet['canonical_sha256'], a['canonical_sha256'], 'packet_canonical', context)
        if 'packet_path' in data:
            self.declared_reference(data['packet_path'], context + '.packet_path')

    def parse(self, selection):
        ident, fmt = selection['artifact'], selection['format']
        data = self.artifact(ident)
        self.equal(data['schema'], FORMATS[fmt], 'worker_schema', ident)
        self.equal(data['task_name'], selection['task'], 'worker_task', ident)
        self.equal(data['model'], self.delegation['model'], 'worker_model', ident)
        self.equal(data['reasoning_effort'], self.delegation['reasoning_effort'], 'worker_effort', ident)
        assignment = self.assignments[selection['task']]
        bounds = selection['range']
        self.check(isinstance(bounds, list) and len(bounds) == 2 and all(type(x) is int for x in bounds)
                   and assignment[0] <= bounds[0] < bounds[1] <= assignment[1], 'selected_range', ident)
        self.check_worker_bindings(data, fmt, ident)
        if fmt == '09250-flat':
            self.equal(data['assigned_slot_range'], assignment, 'worker_assignment', ident)
            self.equal(data['completed_slot_range'], bounds, 'worker_range', ident)
            self.equal(data['complete_source_read_for_completed_checkpoint'], True, 'checkpoint_read_claim', ident)
            slots, raw_rows = data['slot_reviews'], data['individual_reviews']
            ledger = data['actual_read_ledger']
        elif fmt == '11870-slots':
            if 'assigned_sorted139_range' in data:
                self.equal(data['assigned_sorted139_range'], assignment, 'worker_assignment', ident)
            elif 'parent_assigned_sorted139_range' in data:
                parent_range = data['parent_assigned_sorted139_range']
                self.check(isinstance(parent_range, list) and len(parent_range) == 2
                           and all(type(x) is int for x in parent_range)
                           and assignment[0] <= parent_range[0] <= bounds[0] < bounds[1] <= parent_range[1] <= assignment[1],
                           'worker_parent_subrange', ident)
            else:
                self.check(False, 'missing_worker_assignment', ident)
            self.equal(data['completed_contiguous_sorted139_range'], bounds, 'worker_range', ident)
            slots = data['slot_reviews']
            raw_rows = [dict(x, __slot__=slot) for slot in slots for x in slot['individual_judgments']]
            ledger = data['direct_read_log']
        else:
            self.equal([data['slot_start'], data['slot_stop']], bounds, 'worker_range', ident)
            slots, raw_rows, ledger = [], data['rows'], []
        normalized = []
        logs = {}
        for entry in ledger:
            cid = entry['candidate_id']
            hash_value = entry.get('source_record_sha256', entry.get('source_sha256'))
            self.equal(hash_value, self.record_sha(cid), 'read_record_hash', ident + ':' + cid)
            flag = self.field(entry, ['direct_complete_read', 'complete_semantic_source_read',
                                      'full_semantic_source_conditions_effects_alternatives_read'], ident + ':' + cid)
            self.equal(flag, True, 'read_complete_claim', ident + ':' + cid)
            if 'record_kind' in entry:
                self.equal(entry['record_kind'], self.source['candidates'][cid]['record_kind'], 'ledger_record_kind', ident + ':' + cid)
            read_id = entry.get('read_id', ident + ':' + cid)
            self.check(read_id not in logs, 'duplicate_read_id', ident + ':' + read_id)
            logs[read_id] = entry
            self.reads.append({'artifact': ident, 'read_id': read_id, 'candidate_id': cid,
                               'source_sha256': hash_value, 'reuse_of': self.field(entry, ['exact_duplicate_of', 'duplicate_record_equal_to'], ident + ':' + cid, optional=True),
                               'read_origin': entry.get('read_origin'), 'task': selection['task'], 'range': bounds, 'raw': copy.deepcopy(entry)})
        for raw_with_slot in raw_rows:
            raw = dict(raw_with_slot)
            slot_row = raw.pop('__slot__', None)
            cid = raw['candidate_id']
            if fmt == '11870-slots':
                ordinal, slot = slot_row['sorted139_slot_index'], slot_row['slot_id']
                row_read_id = self.field(raw, ['closure_read_id', 'full_source_read_id'], ident + ':' + cid)
                log = logs.get(row_read_id)
                self.check(log is not None, 'missing_row_read_log', ident + ':' + cid)
                log = log or {}
                norm = {'ordinal': ordinal, 'slot_id': slot, 'cid': cid,
                        'kind': raw['actual_record_kind'], 'rids': raw['actual_realization_ids'],
                        'conditions': raw['conditions_exact'], 'effects': raw['effects_exact'],
                        'record_hash': raw['source_anchor']['source_sha256'],
                        'closure_hashes': log.get('closure_sha256', {}),
                        'binding_ids': self.field(log, ['binding_ids', 'frozen_binding_ids'], ident + ':' + cid, optional=True), 'binding_hashes': None,
                        'read_flags': ([log.get('complete_semantic_source_read'), log.get('closure_complete'),
                                       log.get('all_distinct_semantic_fields_conditions_effects_alternatives_read')]
                                       if 'complete_semantic_source_read' in log else
                                       [log.get('full_semantic_source_conditions_effects_alternatives_read'),
                                        log.get('complete_required_closure_read')]),
                        'evidence': [raw['source_anchor']] + raw.get('positive_slot_evidence', []),
                        'verdicts': {'baseline': raw['authored_status']},
                        'facts': [dict(x, dimension=raw['asserted_dimension'], target=raw['owner'],
                                       property=raw['asserted_property']) for x in raw.get('positive_slot_evidence', [])]}
                self.equal(log.get('candidate_id'), cid, 'row_log_candidate', ident + ':' + cid)
                self.equal(log.get('slot_id'), slot, 'row_log_slot', ident + ':' + cid)
                self.equal(log.get('slot_index'), ordinal, 'row_log_ordinal', ident + ':' + cid)
                self.equal(sorted(log.get('closure_ids', [])), sorted(norm['closure_hashes']), 'read_closure_ids', ident + ':' + cid)
                self.equal(self.field(log, ['actual_realization_ids', 'realization_ids'], ident + ':' + cid), norm['rids'], 'read_log_rids', ident + ':' + cid)
            elif fmt == '09250-flat':
                b = raw['source_binding']
                norm = {'ordinal': raw['slot_ordinal'], 'slot_id': raw['slot_id'], 'cid': cid,
                        'kind': raw['record_kind'], 'rids': raw['actual_realization_ids'],
                        'conditions': raw['native_conditions_as_read'], 'effects': raw['native_effects_as_read'],
                        'record_hash': b['source_record_sha256'], 'closure_hashes': b['reference_sha256'],
                        'binding_ids': raw.get('binding_ids_actually_read'),
                        'binding_hashes': raw.get('binding_sha256'),
                        'read_flags': [raw['direct_full_source_read'], raw['direct_full_required_reference_closure_read']],
                        'evidence': [raw['evidence']],
                        'verdicts': {'baseline': raw['baseline_139_semantic_verdict'], 'proposed': raw['proposed_141_semantic_verdict']},
                        'facts': [raw['fit_fact']] if raw.get('fit_fact') else []}
                self.equal(b['candidate_id'], cid, 'source_binding_candidate', ident + ':' + cid)
                self.equal(b['catalog_sha256'], self.catalog_sha, 'source_binding_catalog', ident + ':' + cid)
                self.equal(sorted(raw['reference_ids_actually_read']), sorted(norm['closure_hashes']), 'reference_read_ids', ident + ':' + cid)
            else:
                norm = {'ordinal': raw['slot_ordinal'], 'slot_id': raw['slot_id'], 'cid': cid,
                        'kind': raw['actual_record_kind'], 'rids': raw['actual_realization_ids'],
                        'conditions': raw['intrinsic_conditions'], 'effects': raw['actual_root_effects'],
                        'record_hash': raw['source_sha256'], 'closure_hashes': raw['reference_sha256'],
                        'binding_ids': None, 'binding_hashes': raw['binding_sha256'],
                        'read_flags': [raw['complete_blinded_semantic_body_conditions_effects_and_required_closure_read']],
                        'evidence': raw['evidence'], 'facts': raw['evidence'],
                        'verdicts': {'baseline': raw['judgement']}}
                self.validate_per_rid_effects(raw['actual_effects_by_realization'],
                                             realization_effects(self.source['candidates'][cid]), ident + ':' + cid)
                self.reads.append({'artifact': ident, 'read_id': ident + ':' + str(norm['ordinal']) + ':' + cid,
                                   'candidate_id': cid, 'source_sha256': raw['source_sha256'],
                                   'reuse_of': None, 'read_origin': 'full_read_claim_no_reuse_identity',
                                   'task': selection['task'], 'range': bounds, 'raw': copy.deepcopy(raw)})
            norm.update({'artifact': ident, 'format': fmt, 'raw': raw})
            meaning_key = {'09250-flat': 'individual_judgment', '11870-slots': 'meaning', '07250-rows': 'meaning_judgement'}[fmt]
            self.check(isinstance(raw.get(meaning_key), str) and bool(raw[meaning_key].strip()), 'missing_authored_meaning', ident + ':' + cid)
            self.validate_row(norm, bounds)
            normalized.append(norm)
            self.rows.append(norm)
            self.actual_pairs.append((norm['ordinal'], cid))
        if fmt == '11870-slots':
            used_logs = [self.field(x['raw'], ['closure_read_id', 'full_source_read_id'], ident) for x in normalized]
            self.equal(set(used_logs), set(logs), 'orphaned_or_missing_read_log', ident)
            self.equal(len(used_logs), len(set(used_logs)), 'shared_read_id_without_explicit_reuse', ident)
        self.validate_slots(slots, normalized, fmt, bounds, ident)
        expected_pairs = {(i, cid) for i in range(*bounds) for cid in set(sum(_top3(self.searches[self.slots[i]]).values(), []))}
        actual = [(x['ordinal'], x['cid']) for x in normalized]
        self.equal(set(actual), expected_pairs, 'top3_pair_coverage', ident)
        self.equal(len(actual), len(set(actual)), 'duplicate_review_pair', ident)
        parent_ids = {x['cid'] for x in normalized}
        closure_ids = set().union(*(set(x['closure_hashes']) for x in normalized)) if normalized else set()
        binding_ids = set().union(*(set(self.required_closure(x)[1]) for x in parent_ids)) if parent_ids else set()
        if fmt == '09250-flat':
            ledger_ids = [x['candidate_id'] for x in ledger]
            self.equal(set(ledger_ids), parent_ids | closure_ids, 'actual_read_ledger_coverage', ident)
            self.equal(len(ledger_ids), len(set(ledger_ids)), 'duplicate_ledger_candidate', ident)
            for key, count in [('directly_reviewed_slot_candidate_pairs', len(actual)),
                               ('directly_read_unique_parent_records', len(parent_ids)),
                               ('directly_read_unique_records_including_closure', len(parent_ids | closure_ids))]:
                self.equal(data[key], count, 'worker_read_count', ident + ':' + key)
        if fmt == '07250-rows':
            impact_contract = self.validate_impact(selection, data, normalized, parent_ids, closure_ids, binding_ids)
        for note in selection.get('notes', []):
            self.artifacts[note]  # explicit presence, hash already verified; no completion inference
        assigned_pairs = {(i, cid) for i in range(*assignment) for cid in set(sum(_top3(self.searches[self.slots[i]]).values(), []))}
        if fmt == '09250-flat':
            if 'assigned_slot_candidate_pairs_prepared' in data:
                self.equal(data['assigned_slot_candidate_pairs_prepared'], len(assigned_pairs), 'prepared_assignment_pair_count', ident)
            if 'assigned_unique_parent_records_prepared' in data:
                self.equal(data['assigned_unique_parent_records_prepared'], len({cid for _, cid in assigned_pairs}), 'prepared_assignment_parent_count', ident)
            for key, origin in [('new_unique_records_directly_read', 'new_direct_fullread'),
                                ('reused_prior_frozen_direct_read_records', 'prior_frozen_inverse_fullread')]:
                if key in data:
                    self.equal(data[key], sum(x.get('read_origin') == origin for x in ledger), 'declared_read_origin_count', ident + ':' + key)
        summary = {'artifact': ident, 'format': fmt, 'task': selection['task'], 'selected_range': bounds,
                   'delegated_range': assignment, 'prepared_assignment_pairs_from_search': len(assigned_pairs),
                   'actual_claimed_slot_candidate_pairs': len(actual), 'expected_selected_pairs': len(expected_pairs),
                   'unique_parent_sources': len(parent_ids), 'unique_closure_sources': len(closure_ids),
                   'closure_sources_additional_to_parents': len(closure_ids - parent_ids),
                   'unique_sources_including_closure': len(parent_ids | closure_ids),
                   'unique_binding_definitions': len(binding_ids),
                   'raw_artifact': copy.deepcopy(data)}
        if fmt == '07250-rows':
            summary['raw_impact'] = copy.deepcopy(self.artifact(selection['impact']))
            summary['impact_validation_contract'] = impact_contract
        self.summaries.append(summary)

    def validate_row(self, norm, bounds):
        context = norm['artifact'] + ':' + str(norm['ordinal']) + ':' + norm['cid']
        ordinal, cid = norm['ordinal'], norm['cid']
        self.check(type(ordinal) is int and bounds[0] <= ordinal < bounds[1], 'row_range', context)
        self.equal(norm['slot_id'], self.slots[ordinal], 'row_slot_ordinal', context)
        record = self.source['candidates'][cid]
        self.equal(record['id'], cid, 'source_record_identity', context)
        if 'top3_lane_positions' in norm['raw']:
            positions = {lane: [i + 1 for i, value in enumerate(ids) if value == cid]
                         for lane, ids in _top3(self.searches[norm['slot_id']]).items()}
            positions = {lane: indexes for lane, indexes in positions.items() if indexes}
            self.equal(norm['raw']['top3_lane_positions'], positions, 'row_lane_positions', context)
        self.check(record['record_kind'] != 'diagnostic', 'diagnostic_review_pair', context)
        self.equal(norm['kind'], record['record_kind'], 'record_kind', context)
        self.equal(norm['record_hash'], self.record_sha(cid), 'row_source_hash', context)
        self.equal(norm['conditions'], record['conditions'], 'conditions_exact', context)
        self.equal(norm['effects'], record['effects'], 'effects_exact', context)
        self.equal(norm['rids'], list(realization_effects(record)), 'actual_realization_ids', context)
        self.check(all(x is True for x in norm['read_flags']), 'complete_read_claim', context)
        refs, bindings = self.required_closure(cid)
        self.equal(norm['closure_hashes'], refs, 'complete_reference_closure', context)
        if norm['binding_hashes'] is not None:
            self.equal(norm['binding_hashes'], bindings, 'complete_binding_closure_hashes', context)
        elif bindings or norm['binding_ids'] is not None:
            self.equal(sorted(norm['binding_ids'] or []), sorted(bindings), 'binding_read_declaration', context)
            self.check(norm['binding_ids'] is not None, 'missing_binding_read_declaration', context)
        if norm['binding_ids'] is not None:
            self.equal(len(norm['binding_ids']), len(set(norm['binding_ids'])), 'duplicate_binding_read_id', context)
        norm['branch_positive_evidence_bindings'] = []
        for evidence in norm['evidence']:
            binding = self.validate_quote(record, evidence, norm['rids'], context)
            if binding is not None and binding not in norm['branch_positive_evidence_bindings']:
                norm['branch_positive_evidence_bindings'].append(binding)
        allowed = {'09250-flat': {'fit', 'not_fit', 'defer', 'pending'},
                   '11870-slots': {'fit', 'nonfit', 'pending', 'defer'},
                   '07250-rows': {'fit', 'unfit', 'hold', 'pending', 'defer'}}[norm['format']]
        for basis, verdict in norm['verdicts'].items():
            self.check(verdict in allowed, 'unknown_authored_verdict', context, verdict=verdict)
            if verdict != 'fit':
                continue
            self.check(bool(norm['facts']), 'fit_without_manual_fact', context + ':' + basis)
            slot_spec = (self.catalog if basis == 'baseline' else self.proposed_catalog).get(norm['slot_id'])
            self.check(slot_spec is not None, 'fit_slot_missing_spec', context + ':' + basis)
            for fact in norm['facts']:
                binding = self.validate_quote(record, fact, norm['rids'], context)
                if binding is not None and binding not in norm['branch_positive_evidence_bindings']:
                    norm['branch_positive_evidence_bindings'].append(binding)
                self.check(positive_path(fact.get('pointer'), record=record, rids=norm['rids']), 'metadata_only_primary_fit', context + ':' + basis,
                           pointer=fact.get('pointer'), quote=fact.get('quote'), authored_verdict=verdict)
                dim, owner, prop = fact.get('dimension'), fact.get('target', fact.get('owner')), fact.get('property')
                self.check(_literal_name(owner), 'fit_owner_literal', context + ':' + basis, owner=owner)
                self.check(_literal_name(prop), 'fit_property_literal', context + ':' + basis, property=prop)
                if slot_spec:
                    self.check(dim in slot_spec['dimensions'], 'fit_dimension_spec', context + ':' + basis, dimension=dim)
                    self.check(isinstance(prop, str) and any(prop == x.rstrip('.') or prop.startswith(x if x.endswith('.') else x + '.')
                               for x in slot_spec['property_prefixes']), 'fit_property_prefix', context + ':' + basis, property=prop)

    def validate_quote(self, record, evidence, rids, context):
        try:
            path, quote = evidence['pointer'], evidence['quote']
            binding = branch_positive_binding(record, path, rids)
            self.check((isinstance(path, str) and path.startswith('/content/')) or binding is not None,
                       'evidence_source_body_pointer', context, pointer=path)
            if isinstance(path, str) and BRANCH_CONCEPT_UNIT.fullmatch(path):
                self.check(binding is not None, 'branch_positive_rid_binding', context, pointer=path)
            if binding is not None and 'realization_id' in evidence:
                self.equal(evidence['realization_id'], binding['realization_id'], 'branch_positive_explicit_rid', context)
            value = pointer(record, path)
            self.check(isinstance(value, str) and isinstance(quote, str) and bool(quote.strip()) and quote in value,
                       'exact_pointer_quote', context, pointer=path, quote=quote)
            if 'candidate_id' in evidence:
                self.equal(evidence['candidate_id'], record['id'], 'evidence_candidate', context)
            if 'source_sha256' in evidence:
                self.equal(evidence['source_sha256'], digest(record), 'evidence_record_hash', context)
            bits = path.split('/')
            if 'realization_content' in bits:
                i = bits.index('realization_content')
                self.check(len(bits) > i + 1 and bits[i + 1] in rids, 'evidence_actual_rid', context, pointer=path)
            return binding
        except (KeyError, ValueError, IndexError, TypeError) as exc:
            self.check(False, 'invalid_evidence_pointer', context, detail=str(exc))

    def validate_slots(self, slots, rows, fmt, bounds, ident):
        if fmt == '07250-rows':
            self.equal(sorted({x['ordinal'] for x in rows}), list(range(*bounds)), 'completed_slot_coverage', ident)
            return
        ordinal_key = 'slot_ordinal' if fmt == '09250-flat' else 'sorted139_slot_index'
        self.equal([x[ordinal_key] for x in slots], list(range(*bounds)), 'completed_slot_coverage', ident)
        for slot in slots:
            ordinal, slot_id = slot[ordinal_key], slot['slot_id']
            context = ident + ':' + slot_id
            self.equal(slot_id, self.slots[ordinal], 'slot_summary_ordinal', context)
            if fmt == '09250-flat':
                self.equal(slot['complete_top3_union_review'], True, 'slot_complete_claim', context)
                self.equal(slot['complete_baseline_spec_and_query_plan_read'], True, 'baseline_spec_read_claim', context)
                self.equal(slot['complete_proposed_141_spec_read'], True, 'proposal_spec_read_claim', context)
                self.equal(slot['baseline_spec_sha256'], digest(self.catalog[slot_id]), 'baseline_spec_hash', context)
                self.equal(slot['proposed_spec_sha256'], digest(self.proposed_catalog[slot_id]), 'proposed_spec_hash', context)
                self.equal(self.field(slot, ['baseline_query_sha256', 'query_sha256'], context),
                           self.queries[slot_id]['text_sha256'], 'worker_query_hash', context)
                actual_lanes = {k: _list_ids(v) for k, v in slot['top3'].items()}
                declared_ids = slot['candidate_ids']
                self.equal(slot['slot_candidate_pair_count'], len([x for x in rows if x['ordinal'] == ordinal]), 'slot_pair_count', context)
            else:
                self.equal(slot['spec139'], self.catalog[slot_id], 'baseline_spec_exact', context)
                self.equal(slot['spec139_sha256'], digest(self.catalog[slot_id]), 'baseline_spec_hash', context)
                self.equal(slot['query_fields'], self.queries[slot_id]['fields'], 'worker_query_fields', context)
                self.equal(slot['proposal141_spec_sha256'], digest(self.proposed_catalog[slot_id]), 'proposed_spec_hash', context)
                if 'proposal141_spec' in slot:
                    self.equal(slot['proposal141_spec'], self.proposed_catalog[slot_id], 'proposed_spec_exact', context)
                self.equal(slot['proposal141_spec_exact_equal_to139'], self.catalog[slot_id] == self.proposed_catalog[slot_id], 'proposal_spec_equality', context)
                actual_lanes = slot['discovery_top3_by_lane']
                declared_ids = slot['discovery_union']
            self.equal(actual_lanes, _top3(self.searches[slot_id]), 'worker_top3_lanes', context)
            self.equal(set(declared_ids), set(sum(_top3(self.searches[slot_id]).values(), [])), 'slot_declared_union', context)
            self.equal(len(declared_ids), len(set(declared_ids)), 'slot_duplicate_union_id', context)

    def validate_per_rid_effects(self, actual, expected, context):
        # Source/worker literals are retained. Only dimension-list ordering is
        # semantically irrelevant here; properties and every other field stay exact.
        def dimensions_as_unique_set(value):
            if not isinstance(value, dict):
                return None
            normalized = copy.deepcopy(value)
            for effects in normalized.values():
                if not isinstance(effects, dict) or set(effects) != {'dimensions', 'properties'}:
                    return None
                dims = effects['dimensions']
                if (not isinstance(dims, list) or any(not isinstance(x, str) for x in dims)
                        or len(dims) != len(set(dims))):
                    return None
                effects['dimensions'] = sorted(dims)
            return normalized
        actual_sets, expected_sets = dimensions_as_unique_set(actual), dimensions_as_unique_set(expected)
        self.check(actual_sets is not None and expected_sets is not None
                   and canonical(actual_sets) == canonical(expected_sets), 'per_rid_effects', context,
                   actual=actual, expected=expected,
                   comparison='unique dimension IDs as set; all other fields exact')

    def validate_impact(self, selection, data, rows, parents, refs, bindings):
        ident = selection['artifact']
        impact = self.artifact(selection['impact'])
        if impact.get('schema') == 'photo-inverse-proposed141-impact/v1':
            required = {'schema', 'task_name', 'slot_start', 'slot_stop', 'review',
                        'new_141_native_runtime_completeness_claim'}
            self.equal(set(impact), required, 'proposed_impact_fields', ident)
            self.equal(impact['task_name'], data['task_name'], 'impact_task', ident)
            self.equal([impact['slot_start'], impact['slot_stop']], selection['range'], 'impact_range', ident)
            self.check(isinstance(impact['review'], str) and bool(impact['review'].strip()),
                       'proposed_impact_review', ident)
            self.equal(impact['new_141_native_runtime_completeness_claim'], False,
                       'proposed_impact_completeness_boundary', ident)
            return {'schema': impact['schema'], 'binding': 'explicit selected artifact plus task/range',
                    'authored_adjudication_hash_present': False, 'authored_read_counts_present': False,
                    'review_prose_semantically_reinterpreted': False}
        self.equal(impact['schema'], 'photo-inverse-checkpoint-scope/v1', 'impact_schema', ident)
        self.equal(impact['task_name'], data['task_name'], 'impact_task', ident)
        self.equal([impact['slot_start'], impact['slot_stop']], selection['range'], 'impact_range', ident)
        artifact = self.declared_reference(impact['immutable_adjudication_path'], ident + '.impact')
        if artifact:
            self.equal(artifact['path'], self.artifacts[ident]['path'], 'impact_adjudication_path', ident)
        self.equal(impact['adjudication_sha256'], self.artifacts[ident]['canonical_sha256'], 'impact_adjudication_canonical', ident)
        for key, value in [('slot_candidate_pairs', len(rows)), ('direct_candidate_unique_sources', len(parents)),
                           ('required_closure_unique_sources', len(refs)), ('combined_unique_semantic_sources_read', len(parents | refs)),
                           ('required_source_binding_definitions_read', len(bindings))]:
            self.equal(impact[key], value, 'impact_count', ident + ':' + key)
        self.equal(impact['judgements'], dict(Counter(x['raw']['judgement'] for x in rows)), 'impact_verdict_counts', ident)
        self.equal(impact['operational_native_qualified_count'], 0, 'impact_native_boundary', ident)
        self.equal(impact['stage5c_complete'], False, 'impact_stage_boundary', ident)
        return {'schema': impact['schema'], 'binding': 'selected artifact and authored adjudication hash',
                'authored_adjudication_hash_present': True, 'authored_read_counts_present': True,
                'review_prose_semantically_reinterpreted': False}

    def reuse(self):
        by_id = {}
        for read in self.reads:
            self.check(read['read_id'] not in by_id, 'global_duplicate_read_id', read['read_id'])
            by_id[read['read_id']] = read
        reuse_count, unspecified = 0, 0
        for read in self.reads:
            origin = read['read_origin']
            target = read['reuse_of']
            if target:
                reuse_count += 1
                prior = by_id.get(target)
                self.check(prior is not None, 'unselected_prior_read', read['read_id'], prior_read_id=target)
                if prior:
                    self.equal([prior['candidate_id'], prior['source_sha256']], [read['candidate_id'], read['source_sha256']], 'reuse_source_identity', read['read_id'])
                    self.check(prior['read_id'] != read['read_id'], 'self_read_reuse', read['read_id'])
                    self.equal(prior['task'], read['task'], 'reuse_worker_identity', read['read_id'])
                    earlier = prior['range'][1] <= read['range'][0] or (prior['artifact'] == read['artifact'] and self.reads.index(prior) < self.reads.index(read))
                    self.check(earlier, 'reuse_not_prior_read', read['read_id'])
            elif origin == 'prior_frozen_inverse_fullread':
                reuse_count += 1
                # Old format has no read ID. Only an earlier explicitly selected frozen
                # checkpoint for this exact worker/CID/hash may witness its declaration.
                prior = [p for p in self.reads if p['artifact'] != read['artifact'] and
                         p['candidate_id'] == read['candidate_id'] and p['source_sha256'] == read['source_sha256']
                         and p['task'] == read['task'] and p['range'][1] <= read['range'][0]
                         and p['read_origin'] != 'prior_frozen_inverse_fullread'
                         and p['reuse_of'] is None]
                self.check(bool(prior), 'unselected_prior_read', read['read_id'])
            elif origin == 'full_read_claim_no_reuse_identity':
                unspecified += 1
        # exact_duplicate_of cycles cannot certify a fresh direct read.
        for read in self.reads:
            trail, cursor = set(), read
            while cursor and cursor['reuse_of']:
                if cursor['read_id'] in trail:
                    self.check(False, 'read_reuse_cycle', read['read_id'])
                    break
                trail.add(cursor['read_id'])
                cursor = by_id.get(cursor['reuse_of'])
        return {'declared_read_reuse_occurrences': reuse_count,
                'read_occurrences_without_reuse_identity': unspecified,
                'actual_read_ledger_occurrences': len(self.reads)}

    def run(self):
        self.load_artifacts()
        if self.failures:
            return self.report({})  # never adjudicate rows from unbound bytes
        try:
            self.inputs()
        except (KeyError, ValueError, TypeError, IndexError) as exc:
            self.check(False, 'invalid_input_contract', detail=str(exc))
        if self.failures:
            return self.report({})
        for selected in self.manifest['reviews']:
            try:
                self.parse(selected)
            except (KeyError, ValueError, TypeError, IndexError) as exc:
                self.check(False, 'invalid_worker_contract', selected.get('artifact', ''), detail=str(exc))
        self.equal(len(self.actual_pairs), len(set(self.actual_pairs)), 'overlapping_selected_review_pairs')
        reuse = self.reuse()
        parent_ids = {x['cid'] for x in self.rows}
        closure_ids = set().union(*(set(x['closure_hashes']) for x in self.rows)) if self.rows else set()
        counts = {'actual_claimed_slot_candidate_pairs': len(self.actual_pairs),
                  'distinct_slot_candidate_pairs': len(set(self.actual_pairs)),
                  'actual_claimed_slots': len({i for i, _ in self.actual_pairs}),
                  'unique_parent_sources': len(parent_ids), 'unique_required_closure_sources': len(closure_ids),
                  'unique_sources_including_closure': len(parent_ids | closure_ids), **reuse}
        return self.report(counts)

    def report(self, counts):
        return {'schema': 'photo-direct-inverse-review-verification/v1',
                'contract_revision': CONTRACT_REVISION,
                'selection_manifest': str(self.manifest_path.relative_to(self.root)),
                'selection_manifest_byte_sha256': self.manifest_sha256,
                'status': 'failed' if self.failures else 'passed', 'failures': self.failures,
                'metadata_only_primary_fit_failures': [x for x in self.failures if x['code'] == 'metadata_only_primary_fit'],
                'counts': counts, 'selected_reviews': self.summaries,
                'normalized_rows_preserving_raw': self.rows,
                'selected_artifacts': {k: {a: v for a, v in item.items() if a not in ('value', 'descriptor')}
                                       for k, item in self.artifacts.items()},
                'root_personally_read_all_worker_sources_claimed': False,
                'worker_read_claims_independently_observed': False,
                'physical_read_io_count_independently_measured': False,
                'initial_hash_witness_historical_authenticity_independently_proved': False,
                'owner_to_spec_semantic_equivalence_inferred': False,
                'final_semantic_correctness_proved': False,
                'automatic_tag_or_native_qualification': False,
                'new_proposed_catalog_search_executed': False,
                'runtime_core_verified': False, 'pixels_verified': False,
                'model_or_network_calls': 0,
                'discovery_directory_scan_used': False,
                'verdicts_modified_or_approved': False}


def verify(manifest, *, root, manifest_sha256):
    return Verifier(root, manifest, manifest_sha256).run()


def write_output(result, output, *, root):
    """Explicit new immutable result only; never updates a pointer or registry."""
    root_given = Path(root).absolute()
    root = root_given.resolve()
    path = Path(output)
    if '..' in path.parts:
        raise ValueError('output parent traversal disallowed')
    if path.is_absolute() and path.is_relative_to(root_given):
        path = root / path.relative_to(root_given)
    path = path if path.is_absolute() else root / path
    evidence_dir = (root / result['selection_manifest']).parent.resolve()
    if not path.resolve().is_relative_to(evidence_dir) or path.suffix != '.json' or 'CURRENT' in path.name.upper():
        raise ValueError('output must be a new selected JSON under root, excluding CURRENT')
    q = path.parent
    while q != root and q != q.parent:
        if q.is_symlink():
            raise ValueError('symlink output directory disallowed')
        q = q.parent
    with path.open('xb') as handle:
        handle.write(canonical(result) + b'\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--manifest-sha256', required=True)
    parser.add_argument('--output', help='explicit new immutable verification JSON; omitted means no write')
    args = parser.parse_args(argv)
    result = verify(args.manifest, root=args.root, manifest_sha256=args.manifest_sha256)
    if args.output:
        write_output(result, args.output, root=args.root)
    print(json.dumps({'status': result['status'], 'failure_count': len(result['failures']), 'counts': result['counts']}, ensure_ascii=False))
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
