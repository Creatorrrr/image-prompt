"""Frozen-code controlled admission and lock checks; not actual request replay."""
import copy
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
HERE = OUT.parents[1]
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore'), str(ROOT)]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
import photo_search_layout as layout
import prompt_generator as generator
from tests.test_photo_semantic_evidence import core
from tests.test_photo_native_owner_selection import sign_core
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]

PREP = HERE / 'native-inputs/prepared/root-00000-00020-01'
verified = reviews.verify_batch(PREP / 'ASSIGNMENT.json', OUT / 'BATCH-WIRE-02.json', OUT / 'NOTE-WIRE-02.json')
assignment = reviews.read_json(PREP / 'ASSIGNMENT.json')
inp = reviews.artifact(ROOT, assignment['input'])
source = reviews.artifact(ROOT, inp['current_snapshot'])
# One candidate-free fixture declared for every source before testing any CID.
# It asserts no particular genre, lens, blur, atmosphere, laboratory or device
# identity. This is controlled engine evidence, not a real request/core freeze.
baseline = core(['generic_image', 'generic_camera', 'generic_scene'], role_bindings={
    'image': 'generic_image', 'recording_camera': 'generic_camera', 'scene': 'generic_scene'},
    open_dimensions=('style', 'camera', 'atmosphere', 'setting'))
sign_core(baseline)
controls = []
for cid, row in verified['records'].items():
    if row['proof'] is None:
        continue
    data = copy.deepcopy(source)
    record = copy.deepcopy(row['source_after'])
    record['content']['role_evidence'] = copy.deepcopy(row['proof'])
    data['candidates'][cid] = record
    guard = layout.guard_record(record, data)
    dim = row['source_after']['effects']['dimensions'][0]
    for label, rec in [('full', record), ('compact', guard)]:
        view = {**data, 'candidates': {**data['candidates'], cid: rec}}
        entry = c.entry(view, cid, realization_id='base')
        admission = native.admission(entry, baseline)
        assert admission['allowed'], (cid, label, admission)
        args = (view, baseline, {'subject_category': 'object', 'intent_constraints': {'domains': []}}, {'subject': {}}, '', entry)
        assert generator.core_entry_eligible(*args), (cid, label, 'open')
        locked = copy.deepcopy(baseline)
        locked['intent_lock']['open_dimensions'].remove(dim)
        locked['intent_lock']['locked_dimensions'].append(dim)
        sign_core(locked)
        assert not generator.core_entry_eligible(view, locked, args[2], args[3], '', entry), (cid, label, 'dimension_lock')
        dims, effects, graph = native.permission_scope(entry, baseline)
        anchored = copy.deepcopy(baseline)
        anchored['intent_lock']['semantic_anchors'] = [copy.deepcopy(effects[0])]
        sign_core(anchored)
        assert not generator.core_entry_eligible(view, anchored, args[2], args[3], '', entry), (cid, label, 'property_lock')
        controls.append({'ordinal': row['ordinal'], 'candidate_id': cid, 'view': label,
            'admission': True, 'open_full_consumer': True, 'locked_dimension_full_consumer': False,
            'actual_owner_property_anchor_full_consumer': False, 'effect_dimensions': dims})
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve(); assert path.is_relative_to(GEN)
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
report = {key: val for key, val in verified.items() if key != 'records'}
report.update(controls=controls, admission_checks=len(controls), full_consumer_checks=len(controls)*3,
    common_candidate_free_fixture_sha256=c.digest(baseline), used_frozen_modules=modules,
    boundary='Synthetic independently declared generic roles; no actual normalized request freeze/replay, public-pack runtime generation or pixels.',
    os_network_denied=True, provider_keys_removed=True, provider_calls=0, gemini_calls=0,
    root_semantic_acceptance_written=False, operational_native_qualified_count=0)
with (OUT / 'ROOT-CONTROLLED-VERIFICATION-02.json').open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2); stream.write('\n')
print(json.dumps({'shape_valid': True, 'source_proofs': 7, 'pending': 13,
    'admission_checks': len(controls), 'full_consumer_checks': len(controls)*3,
    'root_acceptance': False, 'operational_changes': 0}))
