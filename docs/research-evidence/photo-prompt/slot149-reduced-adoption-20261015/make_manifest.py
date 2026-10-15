"""Serialize fixed, bounded authored relation decisions; never infer new meanings."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import photo_scoped_slot_adoption as adoption


def main():
    source = c.load(ROOT / 'skills/photo-prompt-image-generator/assets')
    assert c.digest(source) == '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
    catalog_path = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/CATALOG-FINAL-149-V6.json'
    catalog = json.loads(catalog_path.read_text())
    assert c.digest(catalog) == 'd9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
    reviews = json.loads((HERE / 'REVIEWED-BINDINGS.json').read_text())
    rows = reviews['rows']
    assert len(rows) == 42 and len({r['candidate_id'] for r in rows}) == 40
    selected = {}
    for row in rows:
        record = source['candidates'][row['candidate_id']]
        assert c.digest(record) == row['source_record_sha256']
        value = source
        for key in row['source_pointer'].strip('/').split('/'):
            value = value[int(key)] if isinstance(value, list) else value[key]
        assert value == row['literal_quote']
        assert record['conditions'] == row['intrinsic_conditions']
        assert record['effects'] == row['current_effects']
        if row['existing_binding_id']:
            selected[row['existing_binding_id']] = row
    changed = {tag for tag in source['slot_catalog'] if source['slot_catalog'][tag] != catalog[tag]}
    decisions = []
    for bid, before in sorted(source['slot_bindings'].items()):
        if before['slot_id'] not in changed:
            continue
        row = selected.get(bid)
        retain = row is not None and row['decision'] == 'retained_binding'
        reason = (row['reason'] if row else
                  'Changed role scope; not individually reviewed in the bounded sample. '
                  'Preserve exact dependency reference and defer this presentation relation.')
        decisions.append(dict(action='retain' if retain else 'defer', before=before,
                              after=before, reason=reason,
                              source_citation='REVIEWED-BINDINGS.json#' + bid if row else
                              'CATALOG-FINAL-149-V6.json#' + before['slot_id'] + '; PLAN.ko.md bounded deferral'))
    for row in rows:
        if row['decision'] != 'positive_literal_only':
            continue
        # These two literal tags are descriptive metadata, never native effect
        # qualification. Existing source/role guards and native review stay in force.
        assert row['slot_id'] in {'air_humidity', 'material_thickness'}
        witness = source['slot_bindings'][row['template_binding_id']]
        assert witness['candidate_id'] == row['candidate_id']
        assert all(witness[k] == row[k] for k in ('conditions', 'role', 'semantic_role', 'weight'))
        assert set(source['candidates'][row['candidate_id']]['effects']['dimensions']) & set(catalog[row['slot_id']]['dimensions'])
        after = {**witness, 'id': adoption.binding_id(row['candidate_id'], row['slot_id']),
                 'slot_id': row['slot_id']}
        decisions.append(dict(action='add', before=None, after=after,
                              reason=row['reason'] + ' Root accepts literal tag metadata only; no new effect/owner/adoption permission.',
                              source_citation='REVIEWED-BINDINGS.json#' + row['source_pointer'] + '; witness ' + row['template_binding_id']))
    manifest = dict(schema=adoption.SCHEMA, source_sha256=c.digest(source),
                    source_catalog_sha256=c.digest(source['slot_catalog']),
                    reviewed_catalog_sha256=c.digest(catalog), catalog=catalog,
                    catalog_reason='Use the already frozen final149 scope; preserve unchanged104 and defer unreviewed changed-role relations.',
                    catalog_source_citation=str(catalog_path.relative_to(ROOT)),
                    binding_decisions=decisions)
    preview = adoption.build_preview(source, manifest)
    assert preview['report']['decisions'] == {'retain': 19, 'defer': 3489, 'remove': 0, 'update': 0, 'add': 2}
    for name, value in [('MIGRATION.json', manifest), ('STAGE02.json', preview['report'])]:
        (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(preview['report']))


if __name__ == '__main__':
    main()
