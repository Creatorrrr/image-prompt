"""Explicit bounded catalog/binding migration; no semantic qualification or IO on import.

The 149-spec catalog and every changed relationship are authored inputs. Existing
native v4 qualification and complete-corpus validation remain independent gates.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

import photo_candidate_corpus as c

SCHEMA = 'photo-scoped-slot-adoption/v1'
CATALOG_COUNT = 149
REVIEW_POLICY = '_slot_binding_review'
REVIEW_SCHEMA = 'photo-slot-binding-review/v1'
MANIFEST_FIELDS = frozenset({'schema', 'source_sha256', 'source_catalog_sha256',
    'reviewed_catalog_sha256', 'catalog', 'catalog_reason', 'catalog_source_citation',
    'binding_decisions'})
DECISION_FIELDS = frozenset({'action', 'before', 'after', 'reason', 'source_citation'})


def exact(left, right):
    return c.canonical_bytes(left) == c.canonical_bytes(right)


def binding_id(candidate_id, slot_id):
    return 'bind_' + c.digest({'candidate_id': candidate_id, 'slot_id': slot_id})[:32]


def _fields(value, fields, label):
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(label + ': exact fields required')


def _text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(label + ': explicit nonempty rationale/source citation required')


def _references(value, removed, pointer=''):
    """Include reference keys as well as values, matching the corpus validator."""
    found = []
    if isinstance(value, str) and value in removed:
        found.append({'pointer': pointer, 'binding_id': value})
    elif isinstance(value, dict):
        for key, child in value.items():
            escaped = key.replace('~', '~0').replace('/', '~1')
            if key in removed:
                found.append({'pointer': pointer + '/' + escaped, 'binding_id': key,
                              'location': 'object_key'})
            found.extend(_references(child, removed, pointer + '/' + escaped))
    elif isinstance(value, list):
        for n, child in enumerate(value):
            found.extend(_references(child, removed, pointer + '/' + str(n)))
    return found


class ReferenceBlocker(ValueError):
    def __init__(self, blockers):
        self.blockers = blockers
        super().__init__('removed binding references block migration: ' +
                         json.dumps(blockers, ensure_ascii=False, sort_keys=True))


def build_preview(source, manifest):
    """Pure explicit migration. Untouched rows are inherited without reapproval.

    Removals and deferrals are returned as externally storable decisions. A defer
    keeps the exact binding for reference integrity and marks it in a separate
    runtime review policy. A retain is a bounded relationship decision, never a
    native semantic qualification. Additions
need a cited same-candidate source binding witnessing original role conditions,
weight and role; those fields cannot be rewritten by this migration.
"""
    c.validate(source)
    _fields(manifest, MANIFEST_FIELDS, 'scoped migration manifest')
    if (manifest['schema'] != SCHEMA or manifest['source_sha256'] != c.digest(source)
            or manifest['source_catalog_sha256'] != c.digest(source['slot_catalog'])):
        raise ValueError('exact original source/catalog digest required')
    catalog = manifest['catalog']
    if (not isinstance(catalog, dict) or len(catalog) != CATALOG_COUNT
            or manifest['reviewed_catalog_sha256'] != c.digest(catalog)):
        raise ValueError('entire reviewed 149-slot catalog and exact hash required')
    _text(manifest['catalog_reason'], 'catalog_reason')
    _text(manifest['catalog_source_citation'], 'catalog_source_citation')
    if not isinstance(manifest['binding_decisions'], list):
        raise ValueError('explicit binding_decisions list required')
    changed_slots = {tag for tag in set(source['slot_catalog']) | set(catalog)
                     if not exact(source['slot_catalog'].get(tag), catalog.get(tag))}
    affected = {bid for bid, row in source['slot_bindings'].items()
                if row['slot_id'] in changed_slots}
    proposed = copy.deepcopy(source)
    proposed['slot_catalog'] = copy.deepcopy(catalog)
    consumed, produced, deferred = set(), set(), []
    counts = dict.fromkeys(('retain', 'defer', 'remove', 'update', 'add'), 0)
    policy = copy.deepcopy(source['policies'].get(REVIEW_POLICY, {
        'schema': REVIEW_SCHEMA, 'deferred': {}, 'reviewed': {}}))
    _fields(policy, {'schema', 'deferred', 'reviewed'}, 'binding review policy')
    if (policy['schema'] != REVIEW_SCHEMA or
            any(not isinstance(policy[k], dict) for k in ('deferred', 'reviewed')) or
            set(policy['deferred']) & set(policy['reviewed'])):
        raise ValueError('invalid scoped binding review policy')
    for group in ('deferred', 'reviewed'):
        for bid, metadata in policy[group].items():
            _fields(metadata, {'reason', 'source_citation'}, 'binding review metadata')
            if bid not in source['slot_bindings']:
                raise ValueError('unknown source binding in review policy')
            for value in metadata.values():
                _text(value, 'binding review metadata')
    invariant_fields = ('candidate_id', 'role', 'conditions', 'weight')
    for decision in manifest['binding_decisions']:
        _fields(decision, DECISION_FIELDS, 'binding decision')
        _text(decision['reason'], 'binding reason')
        _text(decision['source_citation'], 'binding source_citation')
        action, before, after = (decision[k] for k in ('action', 'before', 'after'))
        if action not in counts:
            raise ValueError('unknown binding decision action')
        if action == 'add':
            if before is not None or not isinstance(after, dict):
                raise ValueError('add needs null before and exact after')
            witnesses = [row for bid, row in source['slot_bindings'].items()
                         if bid in decision['source_citation'] and
                         all(exact(row.get(k), after.get(k)) for k in invariant_fields)]
            if not witnesses:
                raise ValueError('add needs cited original binding conditions/weight/role witness')
        else:
            if not isinstance(before, dict):
                raise ValueError('existing binding needs exact before')
            bid = before.get('id')
            if bid in consumed or bid not in source['slot_bindings'] or not exact(before, source['slot_bindings'][bid]):
                raise ValueError('unique exact original before binding required')
            consumed.add(bid)
            policy['deferred'].pop(bid, None)
            policy['reviewed'].pop(bid, None)
            if action in {'retain', 'defer'}:
                if not exact(before, after):
                    raise ValueError('retain/defer must preserve exact binding')
            elif action == 'remove':
                if after is not None:
                    raise ValueError('remove needs null after')
                del proposed['slot_bindings'][bid]
                deferred.append(copy.deepcopy(decision))
            else:
                if (not isinstance(after, dict) or exact(before, after)
                        or any(not exact(before.get(k), after.get(k)) for k in invariant_fields)):
                    raise ValueError('update must preserve original candidate/conditions/weight/role')
                del proposed['slot_bindings'][bid]
        if action in {'add', 'update'}:
            bid = after.get('id')
            if (bid != binding_id(after.get('candidate_id'), after.get('slot_id'))
                    or bid in produced or bid in proposed['slot_bindings']):
                raise ValueError('unique deterministic candidate/slot binding identity required')
            produced.add(bid)
            proposed['slot_bindings'][bid] = copy.deepcopy(after)
        if action != 'remove':
            group = 'deferred' if action == 'defer' else 'reviewed'
            policy[group][after['id']] = {k: decision[k] for k in ('reason', 'source_citation')}
        if action == 'defer':
            deferred.append(copy.deepcopy(decision))
        counts[action] += 1
    if affected - consumed:
        raise ValueError('changed slot has unlisted affected binding decisions: ' +
                         ','.join(sorted(affected - consumed)))
    if REVIEW_POLICY in source['policies'] or policy['deferred'] or policy['reviewed']:
        proposed['policies'][REVIEW_POLICY] = policy
    removed = set(source['slot_bindings']) - set(proposed['slot_bindings'])
    blockers = _references({k: v for k, v in proposed.items() if k != 'slot_bindings'}, removed)
    # Other binding conditions may themselves contain a reference.
    blockers.extend(_references(proposed['slot_bindings'], removed, '/slot_bindings'))
    if blockers:
        raise ReferenceBlocker(blockers)
    c.validate(proposed)
    untouched = set(source['slot_bindings']) - consumed
    if (not exact(source['candidates'], proposed['candidates'])
            or not exact({k: v for k, v in source['policies'].items() if k != REVIEW_POLICY},
                         {k: v for k, v in proposed['policies'].items() if k != REVIEW_POLICY})
            or any(not exact(source['slot_bindings'][bid], proposed['slot_bindings'][bid])
                   for bid in untouched)):
        raise ValueError('inherited source preservation failed')
    return {'corpus': proposed, 'deferred_bindings': deferred, 'report': {
        'schema': SCHEMA, 'scope': 'catalog-and-explicit-bindings-only',
        'full_native_qualification': False, 'source_sha256': c.digest(source),
        'result_sha256': c.digest(proposed), 'catalog_sha256': c.digest(catalog),
        'catalog_count': len(catalog), 'changed_slot_ids': sorted(changed_slots),
        'affected_source_binding_count': len(affected), 'decisions': counts,
        'inherited_binding_count': len(untouched), 'candidate_count': len(source['candidates']),
        'deferred_binding_count': len(policy['deferred']),
        'reference_blockers': []}}


def _map_entries(text, field):
    """Locate exact raw JSON values, so inherited binding records stay byte-exact."""
    decoder = json.JSONDecoder()
    position = text.index('"' + field + '"')
    position = text.index('{', position) + 1
    entries = {}
    while True:
        while text[position].isspace() or text[position] == ',':
            position += 1
        if text[position] == '}':
            return entries
        key, end = decoder.raw_decode(text, position)
        position = end
        while text[position].isspace():
            position += 1
        if text[position] != ':':
            raise ValueError('invalid source map delimiter')
        position += 1
        while text[position].isspace():
            position += 1
        start = position
        _, position = decoder.raw_decode(text, position)
        entries[key] = text[start:position]


def _map_module(payload, original_raw, replacements, field):
    raw_rows = _map_entries(original_raw.decode('utf-8'), field)
    rows = []
    for bid, value in replacements.items():
        raw = raw_rows.get(bid)
        if raw is None or not exact(payload[field][bid], value):
            raw = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)
        rows.append('    ' + json.dumps(bid) + ': ' + raw)
    return ('{\n  "schema": ' + json.dumps(c.MODULE_SCHEMAS[field]) +
            ',\n  "' + field + '": {\n' + ',\n'.join(rows) + '\n  }\n}\n').encode('utf-8')


def stage_assets(assets, manifest, output_assets):
    """Write a fresh reviewable source directory. Never edit the operating root.

Existing module ownership is preserved. Only catalog/binding modules with actual
changes get new bytes; unchanged files are copied exactly, and inherited binding
record values retain their original bytes even inside changed modules.
"""
    from photo_candidate_sources import SourceInventory
    assets, output_assets = Path(assets).resolve(), Path(output_assets).resolve()
    if output_assets.exists() or assets == output_assets or assets in output_assets.parents:
        raise ValueError('output-assets must be a fresh directory outside operating assets')
    inventory = SourceInventory.load(assets)
    names = [c.MANIFEST_NAME] + [name for name, _ in inventory.rows]
    raw = {name: (assets / name).read_bytes() for name in names}
    source = c.load(assets)
    preview = build_preview(source, manifest)
    result, changed = preview['corpus'], []
    output = dict(raw)
    binding_files = [name for name, kind in inventory.rows if kind == 'slot_bindings']
    catalog_files = [name for name, kind in inventory.rows if kind == 'slot_catalog']
    policy_files = [name for name, kind in inventory.rows if kind == 'policies']
    if len(catalog_files) != 1 or not binding_files:
        raise ValueError('one catalog owner and existing binding modules required')
    owner, payloads, assigned = {}, {}, {name: {} for name in binding_files}
    for name in binding_files:
        payloads[name] = c.decode(raw[name])
        for bid in payloads[name]['slot_bindings']:
            owner[bid] = name
    moved_owner = {d['after']['id']: owner[d['before']['id']]
                   for d in manifest['binding_decisions'] if d['action'] == 'update'}
    for bid, row in result['slot_bindings'].items():
        name = owner.get(bid) or moved_owner.get(bid) or binding_files[
            int(hashlib.sha256(bid.encode()).hexdigest(), 16) % len(binding_files)]
        assigned[name][bid] = row
    for name in binding_files:
        if not exact(payloads[name]['slot_bindings'], assigned[name]):
            output[name] = _map_module(payloads[name], raw[name], assigned[name], 'slot_bindings')
    name = catalog_files[0]
    if not exact(source['slot_catalog'], result['slot_catalog']):
        output[name] = (json.dumps({'schema': c.MODULE_SCHEMAS['slot_catalog'],
            'slot_catalog': result['slot_catalog']}, ensure_ascii=False, indent=2,
            allow_nan=False) + '\n').encode('utf-8')
    if not exact(source['policies'], result['policies']):
        owners = [name for name in policy_files if REVIEW_POLICY in c.decode(raw[name])['policies']]
        if len(owners) > 1 or (not owners and len(policy_files) != 1):
            raise ValueError('unambiguous review policy module owner required')
        name = owners[0] if owners else policy_files[0]
        payload = c.decode(raw[name])
        replacement = {**payload['policies'], REVIEW_POLICY: result['policies'][REVIEW_POLICY]}
        output[name] = _map_module(payload, raw[name], replacement, 'policies')
    if any((assets / name).read_bytes() != content for name, content in raw.items()):
        raise ValueError('source files changed during staged migration')
    output_assets.mkdir(parents=True)
    for name, content in output.items():
        (output_assets / name).write_bytes(content)
        if content != raw[name]:
            changed.append(name)
    if not exact(c.load(output_assets), result):
        raise ValueError('staged full corpus differs from preview')
    preview['report']['changed_files'] = sorted(changed)
    preview['report']['source_files_sha256'] = {name: hashlib.sha256(value).hexdigest()
                                              for name, value in raw.items()}
    return preview


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', required=True, type=Path)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--report', required=True, type=Path)
    parser.add_argument('--deferred', required=True, type=Path)
    parser.add_argument('--output-assets', type=Path,
                        help='stage full validated source in a fresh directory; omit for preview only')
    args = parser.parse_args(argv)
    assets = args.assets.resolve()
    for path in (args.report.resolve(), args.deferred.resolve()):
        if path == assets or assets in path.parents:
            parser.error('report and deferred outputs must be outside operating assets')
    if args.report.resolve() == args.deferred.resolve():
        parser.error('report and deferred outputs must be distinct')
    manifest = c.decode(args.manifest.read_bytes())
    if args.output_assets:
        preview = stage_assets(args.assets, manifest, args.output_assets)
    else:
        preview = build_preview(c.load(args.assets), manifest)
    for path, value in [(args.report, preview['report']),
                        (args.deferred, {'schema': SCHEMA, 'source_sha256': manifest['source_sha256'],
                                         'binding_decisions': preview['deferred_bindings']})]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(preview['report'], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
