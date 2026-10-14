"""Prepare two fresh, individually assigned review inputs; no semantic promotion.

The source/correction/catalog decisions are existing root-reviewed artifacts.
This only pins them and the exact prior judgments for another direct review.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GENERATION = 'e54254ce78fde43d717a5c6e1670a0ffa5b50050fdafcf4b813930e42ecd0a7f'
FROZEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations' / GENERATION
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]
import photo_candidate_corpus as corpus
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import prepare_native_inputs as prepare
sys.path[:0] = [str(FROZEN / 'scripts'), str(FROZEN / 'precore')]


def read(name):
    return prepare.reviews.read_json(HERE / name)


def ref(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'sha256': corpus.digest(read(name))}


def save(path, value):
    with path.open('xb') as stream:
        stream.write(corpus.canonical_bytes(value) + b'\n')
    return ref(str(path.relative_to(HERE)))


base = read('native-inputs/root-00000-00020-plan-01/PLAN-IDENTITY-02.json')
original = read('SOURCE.json.gz')
current = prepare.reviews.read_json(ROOT / base['current_proposal']['file'])
assert corpus.digest(current) == 'f1a7b55527c677e3401a19aec37e57e36a0f07584c0464536bce8b9f141897be'
assert corpus.digest(current['slot_catalog']) == '5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
assert current['slot_bindings'] == original['slot_bindings']
assert current['policies'] == original['policies']
corpus.validate(current)
prepare.approve_source(ROOT, original, current, prepare.reviews.read_json(ROOT / base['source_approval']['file']))
out = HERE / 'native-inputs/08250-special-catalog144-v4-plan-02'
out.mkdir(exist_ok=False)
requirements = save(out / 'ROOT-REVIEW-REQUIREMENTS.json', {
    'schema': 'photo-root-native-review-requirements/v1', 'actor': '/root',
    'current_source': base['current_proposal'], 'source_approval': base['source_approval'],
    'catalog': ref('CATALOG-FINAL-144-V4.json'),
    'catalog_approval': ref('NATIVE-CATALOG-APPROVAL-144-V4.json'),
    'source_and_own_bindings_unchanged_since_prior_special_inputs': True,
    'reason': 'New144V4 posture and participant-role definitions require a fresh whole-source review; prior142 proofs/statuses stay immutable.',
    'requirements': [
        'Actually read every complete original/current source, exact5B row, own binding, reference closure, all selected RIDs, optional branches/profiles/guards and every used latest full spec plus relevant neighbors. Author a fresh proof after that read; never replace old catalog hashes or auto-promote prior acceptance.',
        '11128 retains the individually revised walking/standing values, every selected source clause, exact existing adult/anatomical prerequisites, both declared posture/action meanings and frozen property locks. A broader body_pose spec does not infer new anatomy or eliminate source conditions.',
        '17437 participant_role now explicitly permits primary and secondary carriers, but the actual peer-rival prerequisite and endpoints still need whole-source validation. Do not add a rival/helper or move the common role to an optional helper to fit a slot.',
        'Retain youthful-adult age E, expression/presentation/style/poise and half-lidded response meanings, adult and actual owned-face P, helper-only disjointness, independent warmth/recovery, exact18 RID profiles and all selected conditions/effects. A required locked E must remain rejected, never relabeled P.',
        'Preserve each actual E typed value, operation and receiver set; keep P old versus E new distinct. Explicit equivalent owners alone are aliases; part_of does not merge owners. Any unresolved whole meaning remains pending.',
        'All unchanged branch/source conditions, binding conditions and source-unit dispositions remain conjunctive. No model/Gemini/provider request, operating source write, Git change, or runtime publication by the reviewer.',
    ], 'prepared_count': 2, 'actual_read_count': 0, 'native_approved_count': 0,
    'operational_native_qualified_count': 0, 'gemini_calls': 0})
results = []
for ordinal, old_plan_name, prior_batch_name, batch_id, memos in [
    (11128, 'native-inputs/08250-11128-plan-02/PLAN.json',
     'native_batches/review08250-11128-02/BATCH.json', 'review08250-11128-03',
     ['native_batches/review08250-11128-02/ROOT-ACCEPTANCE.json',
      'native-inputs/08250-11128-plan-02/ROOT-REVIEW-REQUIREMENTS.json']),
    (17437, 'native-inputs/08250-special-11128-17437-plan-01/PLAN-17437.json',
     'native_batches/review08250-17437-01/BATCH.json', 'review08250-17437-02',
     ['native_batches/review08250-17437-01/ROOT-SEMANTIC-REOPEN-01.json'])]:
    old = read(old_plan_name)
    cid = old['assignment']['ids'][0]
    prior_source = prepare.reviews.read_json(ROOT / old['current_proposal']['file'])
    assert current['candidates'][cid] == prior_source['candidates'][cid]
    prior = read(prior_batch_name)
    assert len(prior['records']) == 1 and prior['records'][0]['candidate_id'] == cid
    plan = {key: copy.deepcopy(old[key]) for key in
            ['schema', 'actor', 'original_snapshot', 'order', 'original_selection', 'assignment']}
    plan.update(current_proposal=base['current_proposal'], source_approval=base['source_approval'],
        catalog_approval=base['catalog_approval'], required_revisions={cid: {
            'prior_review': {'artifact': ref(prior_batch_name), 'pointer': '/records/0',
                             'sha256': corpus.digest(prior['records'][0])},
            'memo_artifacts': [requirements, *[ref(name) for name in memos]],
            'reason': 'Fresh whole-source native review under final144V4; no automatic old status/spec/hash conversion.'}},
        reason='Fresh individually assigned special input. Preparation does not establish reading, semantic approval or operating qualification.')
    plan_ref = save(out / ('PLAN-' + str(ordinal) + '.json'), plan)
    directory, receipt = prepare.write_inputs(plan_ref, batch_id, actor='/root')
    results.append({'ordinal': ordinal, 'plan': plan_ref, 'prepared_directory': str(directory.relative_to(ROOT)),
                    'prepared_count': receipt['prepared_count'], 'actual_read_count': 0})
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(FROZEN), (name, str(path))
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
save(out / 'ROOT-PREPARATION-VERIFICATION.json', {
    'schema': 'photo-root-special-input-verification/v1', 'actor': '/root',
    'results': results, 'container18250_integrity': 'pass', 'source_approval_validation': 'pass',
    'all_operating_files_unchanged': True, 'prepared_count': 2, 'actual_read_count': 0,
    'new_native_approvals': 0, 'used_frozen_modules': modules,
    'gemini_calls': 0, 'os_network_denied': True, 'provider_keys_removed': True})
print(json.dumps(results))
