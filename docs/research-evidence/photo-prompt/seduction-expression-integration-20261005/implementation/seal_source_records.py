"""Preserve prior maintenance evidence and seal each authored source separately."""
from pathlib import Path
import copy
import hashlib
import json
import sys

ROOT = Path(sys.argv[1]).resolve()
BASELINE = Path('/Users/chasoik/.codex/worktrees/seduction-paraphrases/image-prompt')
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
RECORDS = HERE.parent.parent / 'extension-maintenance'

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x): return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def write(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')

applied = read(HERE / 'APPLIED-CHANGES-FINAL.json')
integration = read(HERE / 'MAINTENANCE-RECORD-FINAL.json')
for name in applied['authored_files']:
    path = ASSETS / name
    source = read(path)
    if source.get('schema_version') != 'photo-prompt-research-extension/v1':
        continue
    assert sha(path) == applied['source_hashes_after'][name]
    source.pop('maintenance_ref', None)
    previous_ref = integration['previous_maintenance_refs'].get(name)
    if previous_ref:
        previous = read(RECORDS / (previous_ref['record_id'] + '.json'))
        assert digest(previous) == previous_ref['sha256']
        record = copy.deepcopy(previous)
    else:
        record = {'maintenance_only': True}
    record.update({
        'record_id': 'seduction-expression-integration-20261005-' + path.stem,
        'authored_source_sha256': digest(source),
        'runtime_keys': sorted(source),
        'seduction_integration_record_id': integration['record_id'],
        'seduction_integration_record_sha256': digest(integration),
        'prior_maintenance_reference': previous_ref,
        'preserved_prior_maintenance_fields': bool(previous_ref),
    })
    record_path = RECORDS / (record['record_id'] + '.json')
    write(record_path, record)
    source['maintenance_ref'] = {'contract_version': 'photo-extension-maintenance-ref/v1',
                                 'record_id': record['record_id'], 'sha256': digest(record)}
    write(path, source)
    applied['source_hashes_after'][name] = sha(path)

# Exact raw before/after rows bind reversible scope projection in historical tests.
rows = []
for key in integration['candidate_metadata_updated']:
    slot, entry_id = key.split('.', 1)
    matches = []
    for name in applied['authored_files']:
        before_path = BASELINE / 'skills/photo-prompt-image-generator/assets' / name
        if not before_path.is_file():
            continue
        before_source, after_source = read(before_path), read(ASSETS / name)
        before = next((r for r in before_source.get('slots', {}).get(slot, []) if r['id'] == entry_id), None)
        if before is None:
            continue
        after = next(r for r in after_source['slots'][slot] if r['id'] == entry_id)
        changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        assert set(changed) <= {'concept_units', 'relations', 'affected_dimensions', 'affected_properties', 'core_assertion_discovery'}
        assert sha(before_path) == integration['baseline_source_sha256'][name]
        matches.append({'file': name, 'slot': slot, 'id': entry_id, 'changed_fields': changed,
                        'before': before, 'after': after, 'baseline_source_sha256': sha(before_path)})
    assert len(matches) == 1, key
    rows += matches
delta = {'contract_version': 'seduction-source-scope-delta/v1',
         'integration_record_id': integration['record_id'],
         'integration_record_sha256': digest(integration),
         'metadata_rows': rows,
         'limits': 'Historical projection reverses only these exact metadata fields. Authored labels, aliases, eligibility guards and the historical expected values stay exact.'}
delta_path = ROOT / 'tests/fixtures/photo_prompt/seduction_expression_scope_delta.json'
write(delta_path, delta)
write(HERE / 'AUTHORED-SCOPE-DELTA.json', delta)
applied['final_revision'] = 'final-v3'
write(HERE / 'APPLIED-CHANGES-FINAL.json', applied)
print(json.dumps({'per_source_records': 6, 'scope_delta_rows': len(rows),
                  'scope_delta_canonical_sha256': digest(delta), 'scope_delta_file_sha256': sha(delta_path)}, ensure_ascii=False))
