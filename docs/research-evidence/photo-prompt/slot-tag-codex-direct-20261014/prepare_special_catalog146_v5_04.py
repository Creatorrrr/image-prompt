"""Prepare two fresh146 special reviews using the already approved snapshot.

Source reading can start immediately. Proof authoring must wait for root's
binding of the tested/published semantic-reference runtime generation.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/96c7c984127cfa006a18720577bd0bb4b9014394c718770ca9cc414580932aec'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import prepare_native_inputs as prep
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
OUT = HERE / 'native-inputs/08250-special-catalog146-v5-plan-04'


def read(name):
    return prep.reviews.read_json(HERE / name)


def ref(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(read(name))}


def save(name, value):
    path = OUT / name
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')
    return ref(str(path.relative_to(HERE)))


snapshot_name = 'native-inputs/11870-01250-01300-plan-04/CURRENT-PROPOSAL.json.gz'
source_approval_name = 'native-inputs/11870-01250-01300-plan-04/SOURCE-APPROVAL.json'
current = read(snapshot_name)
assert c.digest(current) == '88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8'
assert c.digest(current['slot_catalog']) == '3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645'
OUT.mkdir(exist_ok=False)
requirements = save('ROOT-REVIEW-REQUIREMENTS.json', {
    'schema': 'photo-root-native-review-requirements/v1', 'actor': '/root',
    'catalog': ref('CATALOG-FINAL-146-V5.json'), 'snapshot': ref(snapshot_name),
    '11128_prior_root_acceptance': ref('native_batches/review08250-11128-04/ROOT-ACCEPTANCE.json'),
    '17437_root_reopen': ref('native_batches/review08250-17437-03/ROOT-SEMANTIC-REOPEN-01.json'),
    '17437_independent_precision_review': ref('worker-notes/native-07250-special17437-03-independent-20261015.json'),
    '17437_reanchor_design': ref('authored/native_resolution_08250_17437_field_local_reanchor_design_01.json'),
    'validation_code_requirement': 'Begin source/fullspec reading only. Before authoring/submitting a fresh proof, use the exact tested and actually published semantic-reference runtime generation/hash subsequently supplied by root. Do not treat working-tree availability or the old96c preparer as that publication.',
    'requirements': [
        'Actually read complete original/current sources, exact old5B, actual ownbindings/closure, every common/selected branch/body/profile guard/effect, applicable whole146V5 specifications and relevant neighbors. Reuse unchanged complete spec reads only with exact bytes and explicit provenance; do not count hashes as new whole-catalog reads.',
        '11128 natural standing/walking KO quotes must themselves include 자연스럽게. Preserve adult P, wardrobe E, actual standing/walking posture and walking-only action E, reference/identity conditional preservation and exact original binding applicability. A prior positive research acceptance is history, not new146 proof.',
        '17437 all18 actual RIDs, exact optional independence, same owned face, atomically named eyes/eyelids/brow/mouth and cheek-only-six P remain. Brow is a brow region, not automatically eyebrow hair. Preserve youthful-adult age E separately from declared adulthood P, common adult body/face preservation, existing peer-rival, actual helper only in help branches, and independently declared prior disruption only in recovery branches.',
        '17437 cheek warmth remains exactly one visible local cheek-color E in each of six actual branches. No duplicate skin-state, thermal, cosmetics, blood-flow or private emotion. Keep all selected effects even if no displayed role supports them.',
        'Reanchor full canonical typed values in their own exact positive primary fields. All seven precision classes and any additional weak anchors require fresh manual resolution. Where a real partial restatement or output/owner reference remains, explicitly author one-hop semantic_reference units only after the new runtime is provided. Reference units never supply canonical facts, role evidence, new guards or permissions and cannot hide a new substantive local condition.',
        'Canonical fact anchors and references must be same CID/actualRID, distinct positive primary pointers; every fact still has a direct ordinary semantic unit. No metadata, foreign language/pointer qualifier borrowing, optional sibling, reference chain, self anchor, orphan, unreviewed source/E deletion or extra incoming haughty-eye P. Actual profile/render gate constraints remain independently preserved.',
        'Author fresh whole-source evidence after reads; do not copy/re-sign old proofs/catalog hashes/statuses. Preserve exact prior per-CID judgments and root reasons. Whole real owner aliases/part topology/exact receiver sets and whole E property/dimension locks stay strict. Shape and synthetic consumers do not prove semantic truth or pixels.',
        'No Gemini/provider/network, operating source/index/catalog publication, registry/global promotion or Git by reviewer. Root owns final acceptance and production integration.'
    ], 'prepared_count': 2, 'actual_read_count': 0, 'native_candidate_approvals': 0, 'operating_changes': 0, 'gemini_calls': 0})
results = []
for ordinal, prior_name, new_id in [
    (11128, 'native_batches/review08250-11128-04/BATCH.json', 'review08250-11128-05'),
    (17437, 'native_batches/review08250-17437-03/BATCH.json', 'review08250-17437-04')]:
    old = read(f'native-inputs/08250-special-quote-color-plan-03/PLAN-{ordinal}.json')
    prior = read(prior_name)
    assert len(prior['records']) == 1
    cid = old['assignment']['ids'][0]
    assert prior['records'][0]['candidate_id'] == cid
    plan = {key: copy.deepcopy(old[key]) for key in ['schema', 'actor', 'original_snapshot', 'order', 'original_selection', 'assignment']}
    plan.update(current_proposal=ref(snapshot_name), source_approval=ref(source_approval_name),
        catalog_approval=ref('NATIVE-CATALOG-APPROVAL-146-V5.json'),
        required_revisions={cid: {'prior_review': {'artifact': ref(prior_name), 'pointer': '/records/0', 'sha256': c.digest(prior['records'][0])},
            'memo_artifacts': [requirements], 'reason': 'Fresh146V5 and precisely grounded semantic evidence. Prior exact research judgments remain immutable; no automatic proof/catalog/status conversion.'}},
        reason='Fresh explicit146V5 special review, source unchanged from approved shared56-change snapshot. Source reads first; proof waits for root-provided published semantic-reference code.')
    plan_ref = save(f'PLAN-{ordinal}.json', plan)
    directory, receipt = prep.write_inputs(plan_ref, new_id, actor='/root')
    results.append({'ordinal': ordinal, 'plan': plan_ref, 'prepared_directory': str(directory.relative_to(ROOT)), 'prepared_count': receipt['prepared_count'], 'actual_read_count': 0})
modules = {}
for name, module in list(sys.modules.items()):
    if name.startswith('photo_') and getattr(module, '__file__', None):
        path = Path(module.__file__).resolve()
        assert path.is_relative_to(GEN)
        modules[name] = {'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
verification = save('ROOT-PREPARATION-VERIFICATION.json', {
    'schema': 'photo-root-special146-input-preparation-verification/v1', 'actor': '/root',
    'results': results, 'shared_snapshot': ref(snapshot_name), 'source_approval': ref(source_approval_name),
    'full18250_source_catalog_exact_input_validation': 'pass', 'prepared_count': 2, 'actual_read_count': 0,
    'candidate_native_approvals': 0, 'operating_changes': 0, 'source_records_changed_by_preparation': 0,
    'used_frozen_preparation_modules': modules, 'os_network_denied': True, 'provider_keys_removed': True, 'gemini_calls': 0})
print(json.dumps({'results': results, 'source_reads_from_preparation': 0, 'native_approvals': 0, 'verification': verification}))
