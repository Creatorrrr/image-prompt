"""Version an accepted source binding without modifying its historical record."""
from pathlib import Path
import copy, hashlib, json, sys

ROOT = Path(__file__).resolve().parents[4]
EVIDENCE = Path(__file__).resolve().parent
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
SOURCE = ASSETS / 'photo_prompt_photorealism_elements_extension.json'
MAINTENANCE = ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import photo_candidate_semantics as semantics
import prompt_generator as generator

frozen = json.loads((EVIDENCE / 'frozen-inventory-queries.json').read_text())
accepted = json.loads((EVIDENCE / 'acceptance-decisions.json').read_text())
assert accepted['accepted_ids'], 'No accepted source change needs a new binding'
old_ref = frozen['provenance_binding']['baseline_ref']
old_path = MAINTENANCE / (old_ref['record_id'] + '.json')
old_bytes = old_path.read_bytes()
assert hashlib.sha256(old_bytes).hexdigest() == frozen['provenance_binding']['baseline_record_file_sha256']
old_record = json.loads(old_bytes)
assert semantics.digest(old_record) == old_ref['sha256']
text = SOURCE.read_text()
raw = json.loads(text)
for row in frozen['inventory']:
    current = next(r for r in raw['slots'][row['slot']] if r['id'] == row['id'])
    expected = row['proposed_after'] if row['id'] in accepted['accepted_ids'] else row['before']
    assert current == expected
before_hash = generator.dictionary_hash(generator.load_json(ASSETS / 'photo_prompt_tags.json'))
assert before_hash == accepted['accepted_dictionary_hash']
authored = copy.deepcopy(raw)
authored.pop('maintenance_ref')
record = copy.deepcopy(old_record)
record['record_id'] = 'photo_prompt_photorealism_elements_extension_data_cleanup_20261001_cycle07'
record['authored_source_sha256'] = semantics.digest(authored)
record['maintenance_only']['source_revision'] = {
    'baseline_commit': frozen['baseline_commit'],
    'previous_ref': old_ref,
    'previous_authored_source_sha256': old_record['authored_source_sha256'],
    'frozen_plan_sha256': hashlib.sha256((EVIDENCE / 'frozen-inventory-queries.json').read_bytes()).hexdigest(),
    'evidence_directory': str(EVIDENCE.relative_to(ROOT)),
    'accepted_candidate_ids': accepted['accepted_ids'],
    'field': 'relations[0].object',
    'reason': 'Align accepted image-layer ownership with original component intent; all other row fields and original research coverage remain exact.',
    'qualification_limit': 'Source binding and DATA validation only. No new research, image generation, pixel qualification or real-capture provenance claim.',
}
new_ref = {**old_ref, 'record_id': record['record_id'], 'sha256': semantics.digest(record)}
new_path = MAINTENANCE / (record['record_id'] + '.json')
if new_path.exists():
    assert json.loads(new_path.read_text()) == record, 'Existing version differs; review before any write'
else:
    new_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
if raw['maintenance_ref'] != new_ref:
    assert raw['maintenance_ref'] == old_ref
    at = text.index('"maintenance_ref"')
    start = text.index('{', at)
    parsed, length = json.JSONDecoder().raw_decode(text[start:])
    assert parsed == old_ref
    segment = text[start:start + length]
    for key in ['record_id', 'sha256']:
        old_value = json.dumps(old_ref[key], ensure_ascii=False)
        assert segment.count(old_value) == 1
        segment = segment.replace(old_value, json.dumps(new_ref[key], ensure_ascii=False))
    changed = text[:start] + segment + text[start + length:]
    expected_raw = copy.deepcopy(raw)
    expected_raw['maintenance_ref'] = new_ref
    assert json.loads(changed) == expected_raw
    SOURCE.write_text(changed)
final = json.loads(SOURCE.read_text())
assert final.pop('maintenance_ref') == new_ref
assert semantics.digest(final) == record['authored_source_sha256']
assert old_path.read_bytes() == old_bytes
assert generator.dictionary_hash(generator.load_json(ASSETS / 'photo_prompt_tags.json')) == before_hash
(EVIDENCE / 'maintenance-binding-reconciliation.json').write_text(json.dumps({
    'previous_ref': old_ref,
    'new_ref': new_ref,
    'new_authored_source_sha256': record['authored_source_sha256'],
    'original_record_byte_identical': True,
    'original_coverage_unchanged': True,
    'accepted_candidate_ids': accepted['accepted_ids'],
    'runtime_dictionary_hash_unchanged_by_binding': before_hash,
    'extra_embedding_calls': 0,
}, indent=2) + '\n')
print('Versioned source binding verified; original record and runtime text preserved')
