"""Version maintenance provenance for the two reviewed candidate scope guards."""
from pathlib import Path
import copy
import hashlib
import json
import sys

E = Path(__file__).resolve().parent
W = E.parents[3]
S = W / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(S / 'scripts'))
import photo_candidate_semantics as cs
import prompt_generator as pg
from photo_runtime_sources import source_update

assert '--apply' in sys.argv, 'Explicit local repair invocation required'
assert (E / 'AFFECTED-REGRESSION-RESULT.json').exists(), 'Initial source verification must finish first'
assert (E / 'history-initial-qualification').is_dir(), 'Initial V34 evidence must be archived first'
store = Path.home() / '.cache/image-prompt/photo-data-quality-links-main-merge-20261007/runtime'
with source_update(S, store):
    before_data = pg.load_json(S / 'assets/photo_prompt_tags.json')
    results = []
    for name, slot, identity in [
        ('photo_prompt_photorealism_elements_extension.json', 'platform_framing', 'pr_casual_crop_subject_legibility_candidate'),
        ('photo_prompt_realistic_background_extension.json', 'motion', 'rb_shared_wind_response_candidate')]:
        path = S / 'assets' / name
        raw = path.read_bytes()
        value = json.loads(raw)
        original_ref = copy.deepcopy(value['maintenance_ref'])
        parent_path = W / 'docs/research-evidence/photo-prompt/extension-maintenance' / (original_ref['record_id'] + '.json')
        parent_raw = parent_path.read_bytes()
        parent = json.loads(parent_raw)
        assert cs.digest(parent) == original_ref['sha256']
        target = next(row for row in value['slots'][slot] if row['id'] == identity)
        assert target['kind'] == target['for_any'] == ['human']
        body = copy.deepcopy(value)
        body.pop('maintenance_ref')
        new_id = path.stem + '_data_quality_scope_20261007'
        record = copy.deepcopy(parent)
        record['record_id'] = new_id
        record['authored_source_sha256'] = cs.digest(body)
        revision = record['maintenance_only'].setdefault('source_revision', {})
        assert 'scope_correction' not in revision
        revision['scope_correction'] = {
            'schema': 'photo-maintenance-scope-correction/v1',
            'previous_maintenance_ref': original_ref,
            'previous_record_raw_sha256': hashlib.sha256(parent_raw).hexdigest(),
            'previous_scoped_source_raw_sha256': hashlib.sha256(raw).hexdigest(),
            'candidate': {'slot': slot, 'id': identity, 'kind': ['human'], 'for_any': ['human']},
            'reason': 'Bind the already reviewed human-only scope correction to its actual authored body without rewriting the original research record.',
            'verification': 'Existing research evidence retained; scope guards verified by independent prompt runs and tests. No new image or pixel verification is asserted.'}
        record_path = parent_path.parent / (new_id + '.json')
        record_bytes = (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode()
        assert not record_path.exists(), 'Successor record must not overwrite a prior outcome'
        record_path.write_bytes(record_bytes)
        value['maintenance_ref'] = dict(original_ref, record_id=new_id, sha256=cs.digest(record))
        cs.validate_extension_keys(value)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        assert parent_path.read_bytes() == parent_raw
        results.append({'source': str(path.relative_to(W)), 'previous_ref': original_ref,
                        'current_ref': value['maintenance_ref'], 'previous_source_raw_sha256': hashlib.sha256(raw).hexdigest(),
                        'current_source_raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'current_authored_body_sha256': cs.digest(body), 'successor_record': str(record_path.relative_to(W)),
                        'original_record_preserved': True})
    after_data = pg.load_json(S / 'assets/photo_prompt_tags.json')
    assert before_data == after_data, 'Maintenance metadata changed compiled candidate behavior'
report = {'schema': 'photo-scope-maintenance-ref-repair/v1', 'compiled_runtime_data_unchanged': True, 'sources': results}
(E / 'MAINTENANCE-REFERENCE-REPAIR.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report, ensure_ascii=False, indent=2))
