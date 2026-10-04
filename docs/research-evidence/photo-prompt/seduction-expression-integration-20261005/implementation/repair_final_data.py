"""Finalize authoring repairs while retaining the image-test source revision."""
from pathlib import Path
import copy
import hashlib
import json
import sys

ROOT = Path(sys.argv[1])
BASELINE = Path('/Users/chasoik/.codex/worktrees/seduction-paraphrases/image-prompt')
HERE = Path(__file__).resolve().parent
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'

def read(p): return json.loads(p.read_text())
def write(p, x): p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')
def digest(x): return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

tags_path = ASSETS / 'photo_prompt_tags.json'
tags = read(tags_path)
before = read(BASELINE / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
preserved = next(row for row in before['slots']['expression'] if row['id'] == 'playful_smirk')
index = next(i for i, row in enumerate(tags['slots']['expression']) if row['id'] == 'playful_smirk')
tags['slots']['expression'][index] = copy.deepcopy(preserved)
write(tags_path, tags)

relation_path = ASSETS / 'photo_prompt_reactorprompt_visual_relations_extension.json'
relation = read(relation_path)
entry = next(row for row in relation['slots']['gaze_target'] if row['id'] == 'head_eye_counterorientation_relation')
original_relation = copy.deepcopy(entry)
entry.update({
    'concept_units': [
        'the head turns toward one stated direction',
        'the irises point toward a second specified target',
        'both directions belong to the same connected head and eyes',
    ],
    'relations': [
        {'id': 'se_head_eye_direction_difference', 'type': 'counterorientation', 'subject': 'main_subject.head', 'object': 'main_subject.eyes'},
        {'id': 'se_counteroriented_eye_target', 'type': 'directed_gaze', 'subject': 'main_subject.eyes', 'object': 'the specified existing gaze target'},
    ],
    'affected_dimensions': ['pose', 'expression'],
    'affected_properties': [
        {'dimension': 'pose', 'target': 'main_subject', 'property': 'head.orientation'},
        {'dimension': 'expression', 'target': 'main_subject', 'property': 'eyes.gaze_direction'},
    ],
    'core_assertion_discovery': True,
})
for key in ('en', 'ko', 'aliases', 'keywords', 'tags', 'for_any', 'weight'):
    assert entry.get(key) == original_relation.get(key), key

record = read(HERE / 'MAINTENANCE-RECORD.json')
record.update({
    'schema_version': 'photo-extension-maintenance/v1',
    'record_id': 'seduction-expression-integration-20261005-v2',
    'maintenance_only': True,
    'final_repairs': [
        {'candidate': 'expression.playful_smirk', 'change': 'Restore the exact previously published authored row; equivalent paraphrases stay in the additive extension.'},
        {'candidate': 'gaze_target.head_eye_counterorientation_relation', 'change': 'Declare existing head/iris directions, actor ownership and both property effects; retain original labels and aliases.'},
        {'change': 'Seal runtime extension references with canonical JSON SHA-256 in the expected external evidence registry.'},
    ],
    'qualification_revision': 'qualification-v1 is retained under qualification/frozen-source-v1; selected candidate meanings are checked against this final revision separately.',
})
record['candidate_metadata_updated'] = [key for key in record['candidate_metadata_updated'] if key != 'expression.playful_smirk'] + ['gaze_target.head_eye_counterorientation_relation']
record['baseline_source_sha256'][relation_path.name] = hashlib.sha256((BASELINE / 'skills/photo-prompt-image-generator/assets' / relation_path.name).read_bytes()).hexdigest()
record['previous_maintenance_refs'][relation_path.name] = relation.get('maintenance_ref')
record_path = HERE.parent.parent / 'extension-maintenance' / (record['record_id'] + '.json')
record_path.parent.mkdir(exist_ok=True)
write(record_path, record)
write(HERE / 'MAINTENANCE-RECORD-FINAL.json', record)
reference = {'contract_version': 'photo-extension-maintenance-ref/v1', 'record_id': record['record_id'], 'sha256': digest(record)}
applied = read(HERE / 'APPLIED-CHANGES.json')
applied['authored_files'].append(relation_path.name)
for name in applied['authored_files']:
    path = ASSETS / name
    payload = relation if path == relation_path else read(path)
    if payload.get('schema_version') == 'photo-prompt-research-extension/v1':
        payload['maintenance_ref'] = reference
        write(path, payload)
    applied['source_hashes_after'][name] = hashlib.sha256(path.read_bytes()).hexdigest()
applied['implementation_root'] = str(ROOT.resolve())
applied['final_revision'] = 'final-v2'
applied['existing_candidate_guards_and_labels_preserved'] = record['candidate_metadata_updated']
write(HERE / 'APPLIED-CHANGES-FINAL.json', applied)
print(json.dumps({'final_root': str(ROOT), 'legacy_row_restored': True, 'direction_scope_completed': True, 'maintenance_record': str(record_path), 'canonical_record_sha256': reference['sha256']}))
