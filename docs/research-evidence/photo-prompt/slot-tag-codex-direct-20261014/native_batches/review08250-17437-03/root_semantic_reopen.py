"""Preserve shape-passing03 and explicitly hold its field-local evidence.

Root read all seven representative issue classes with their exact full fields,
not all3633 raw occurrences. Mechanical204-identity checks do not enlarge that
read claim. No source, proof, signature or native acceptance is rewritten.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
HERE = OUT.parents[1]
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]


def read(name):
    return reviews.read_json(HERE / name)


def ref(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(read(name))}


def at(value, pointer):
    for part in reviews.pointer_parts(pointer):
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


assignment = HERE / 'native-inputs/prepared/review08250-17437-03/ASSIGNMENT.json'
verification = reviews.verify_batch(str(assignment.relative_to(ROOT)), str((OUT / 'BATCH.json').relative_to(ROOT)), str((OUT / 'NOTE.json').relative_to(ROOT)))
batch = reviews.read_json(OUT / 'BATCH.json')
assert c.digest(batch) == 'ec9c490f374da25e3859cbdfc0411122ed6229229edd2701bca0395a8e34840d'
assert len(batch['records']) == 1 and batch['records'][0]['status'] == 'approved'
record = batch['records'][0]
proof, source = record['proof'], record['source_after']
assert len(proof['facts']) == 3633 and len(proof['source_units']) == 621
memo_name = 'worker-notes/native-07250-special17437-03-independent-20261015.json'
design_name = 'authored/native_resolution_08250_17437_field_local_reanchor_design_01.json'
memo, design = read(memo_name), read(design_name)
assert ref(memo_name)['file_sha256'] == '8e10e3415f251ddad4c2963445ff31362c59ba8bac184fb9f5d54c7077987ffd'
assert ref(design_name)['file_sha256'] == '2c8bde29804a6232dfa3af28ca07a1e8b44e010f01d457aa4328ba38690965cd'
facts = {row['id']: row for row in proof['facts']}
issue_ids, representatives = [], []
for finding in memo['evidence_precision_findings']:
    issue_ids.append(finding['id'])
    for row in finding['representative_exact_facts']:
        assert proof['facts'][row['index']] == row['fact'] == facts[row['fact']['id']]
        assert at(source, row['fact']['pointer']) == row['whole_named_source_field']
        representatives.append({'issue': finding['id'], 'fact_id': row['fact']['id'], 'exact_fact_and_entire_field': True})
for row in design['exact_occurrence_designs']:
    assert facts[row['original_fact_id']] == row['before']
    assert c.digest(row['before']) == row['original_fact_sha256']
    assert c.digest(row['source_unit_before']) == row['source_unit_before_sha256']
assert len(issue_ids) == 7 and len(design['exact_occurrence_designs']) == 204
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(GEN), (name, str(path))
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
report = {'schema': 'photo-root-native-semantic-reopen/v1', 'actor': '/root',
    'candidate_id': record['candidate_id'], 'ordinal': 17437,
    'batch': ref('native_batches/review08250-17437-03/BATCH.json'),
    'independent_memo': ref(memo_name), 'proposed_reanchor_design': ref(design_name),
    'pure_frozen_shape_verification': verification,
    'root_decision': 'hold_field_local_evidence_revision_before_acceptance',
    'root_acceptance_written': False, 'worker_positive_status_preserved_unchanged': True,
    'seven_precision_classes': issue_ids, 'exact_representatives_checked': representatives,
    'mechanically_pinned_occurrence_designs': 204,
    'root_read_boundary': 'Root read seven issue classes, their representative complete actual facts/full source fields, class policies, preservation rules and bounded protocol design. Root does not claim3633 raw fact/621 raw unit direct reread or all204 occurrence designs personally read.',
    'decision_reason': 'Whole-source anaphora is legitimate and the common/selected source supplies strong intended values. The current strict field-local facts cannot independently import full peer, color, expression, adult-face, youthful-styling, recovery-goal or brief qualifiers absent from their own field/quote. Reanchor canonical full-value evidence and explicitly retain the narrower referential/readability/owner/exclusion duty; do not remove source meaning, E or preservation.',
    'next_contract_boundary': 'A bounded single-hop semantic_reference unit is separately being implemented and must pass root review, regressions and actual metadata publication before use. It grants no automatic natural-language entailment, candidate tag or permission. New146V5 input also requires explicit fresh review;03 is not converted.',
    'canonical_sources_proofs_statuses_or_signatures_changed': False,
    'native_candidate_approvals': 0, 'operational_native_qualification': 0,
    'frozen_modules': modules, 'os_network_denied': True, 'provider_keys_removed': True,
    'gemini_calls': 0, 'local_inference_calls': 0}
path = OUT / 'ROOT-SEMANTIC-REOPEN-01.json'
with path.open('xb') as stream:
    stream.write(c.canonical_bytes(report) + b'\n')
print(json.dumps({'worker_batch_shape': 'pass', 'precision_classes': 7, 'mechanical_occurrence_identity_checks': 204, 'root_acceptance': False, 'operational_changes': 0}))
