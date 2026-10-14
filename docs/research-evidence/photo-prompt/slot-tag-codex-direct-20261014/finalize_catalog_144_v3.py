"""Serialize root's explicit acceptance of the independently reviewed144 R02.

This approves the catalog as fresh direct-review input, not corpus activation.
Root authored/reread all12 changed specs and the whole source witnesses; the
independent sol/high worker read every full144 spec. No old proof is re-signed.
"""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(HERE), str(ROOT / 'skills/photo-prompt-image-generator/scripts')]
import native_reviews as reviews
import photo_candidate_corpus as corpus


def read(path):
    return json.loads(path.read_bytes())


def raw_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': raw_sha(path), 'sha256': corpus.digest(read(path))}


def save(name, value):
    path = HERE / name
    with path.open('xb') as stream:
        stream.write(corpus.canonical_bytes(value) + b'\n')
    return artifact(path)


proposal_path = HERE / 'CATALOG-PROPOSED-144-V3-R02.json'
opinion_path = HERE / 'worker-notes/native-evidence-whole144-r02-taxonomy-review-20261015.json'
integrity_path = HERE / 'worker-notes/native-evidence-taxonomy144-r02-integrity-20261015.json'
expected = {
    proposal_path: 'b272b5b9329fab88bb54f5a33b694a36a9dfe1fe2ec90460aecbc5b4e10ed74e',
    opinion_path: '6a349422fef25aede7c12d437c0ce16522ce4a11ab67bb6c831b04ec1b41e905',
    integrity_path: '7651ec1b111d5ac88f4f2d1f88b8eb131fbbcb9c2c9253deda2c6d784f0a3552',
}
for path, sha in expected.items():
    if raw_sha(path) != sha:
        raise ValueError('reviewed input changed: ' + str(path))
before = read(HERE / 'CATALOG.json')
previous = read(HERE / 'CATALOG-FINAL-142-V2.json')
after = read(proposal_path)
old_review = read(HERE / 'CATALOG-FINAL-142-V2-REVIEW.json')
delta = read(HERE / 'CATALOG-PROPOSED-144-V3-R02-DELTA.json')
opinion = read(opinion_path)
assert old_review['before'] == before and old_review['after'] == previous
assert len(after) == 144 and len(previous) == 142 and len(before) == 139
assert corpus.digest(after) == '20ba9b75b3afa86ec02a1aa7a7d750eda86ca61c99573d03c94ea12ea9375c39'
assert opinion['catalog']['canonical_sha256'] == corpus.digest(after)
old_reasons = {row['pointer'][1:]: row['reason'] for row in old_review['changes']}
new_reasons = {row['pointer'][1:]: row['reason'] for row in delta['changes']}
changed = [key for key in sorted(set(before) | set(after)) if before.get(key) != after.get(key)]
review = {
    'reviewer': 'Codex/root with gpt-6.1-sol/high delegated whole144 review',
    'whole_catalog_reviewed': True, 'before': copy.deepcopy(before), 'after': copy.deepcopy(after),
    'changes': [{'pointer': '/' + key, 'before_exists': key in before, 'before': before.get(key),
                 'after_exists': key in after, 'after': after.get(key),
                 'reason': new_reasons[key] if key in new_reasons else old_reasons[key]} for key in changed],
    'provenance': [artifact(HERE / name) for name in [
        'CATALOG-FINAL-142-V2-REVIEW.json', 'CATALOG-FINAL-142-V2-ACCEPTANCE.json',
        'CATALOG-PROPOSED-144-V3-R02.json', 'CATALOG-PROPOSED-144-V3-R02-DELTA.json',
        'CATALOG-PROPOSED-144-V3-R02-SOURCE-EVIDENCE.json',
        'CATALOG-PROPOSED-144-V3-SOURCE-EVIDENCE.json',
        'worker-notes/native-evidence-whole142-taxonomy-checkpoint-20261014.json',
        'worker-notes/native-evidence-whole144-taxonomy-review-20261014.json',
        'worker-notes/native-evidence-whole144-r02-taxonomy-review-20261015.json',
        'worker-notes/native-evidence-taxonomy144-r02-integrity-20261015.json']],
}
reviews.verify_catalog(before, after, review, ROOT)
catalog_ref = save('CATALOG-FINAL-144-V3.json', after)
review_ref = save('CATALOG-FINAL-144-V3-REVIEW.json', review)
acceptance_ref = save('CATALOG-FINAL-144-V3-ACCEPTANCE.json', {
    'schema': 'photo-codex-final-catalog-acceptance/v1', 'actor': '/root',
    'status': 'final_for_fresh_native_direct_reviews_not_canonical_application',
    'catalog': catalog_ref, 'catalog_count': 144, 'catalog_ids': sorted(after),
    'catalog_sha256': corpus.digest(after), 'original_catalog_sha256': corpus.digest(before),
    'previous_catalog': artifact(HERE / 'CATALOG-FINAL-142-V2.json'), 'review': review_ref,
    'changed_from_previous': sorted(new_reasons), 'new_slots_from_previous': 2,
    'root_personally_reread_all_twelve_complete_specifications': True,
    'root_personally_read_all144_specs_in_this_revision': False,
    'delegated_whole_catalog_review': artifact(opinion_path),
    'root_review': 'Accept the12 bounded actual-carrier definitions and independent whole144 review. Preserve intrinsic source conditions, exact P/owner/receiver/part/branch facts and permission locks. Body orientation, nonhuman-primary companionship and standalone garment scope are deliberate normative choices, without inventing positive corpus examples. The lone dove and synthetic fiber sheen are negative controls. New catalog identity authorizes only freshly bound direct review; no old source/proof/status is converted.',
    'historical_reviews_changed': False, 'native_requalification_required': True,
    'operational_catalog_changed': False, 'operational_native_qualified_records': 0,
    'stages05_08_complete': False, 'gemini_calls': 0,
})
approval = {
    'schema': 'photo-codex-native-input-catalog-approval/v1', 'actor': '/root',
    'status': 'final_approved', 'catalog': catalog_ref, 'catalog_count': 144,
    'catalog_ids': sorted(after), 'catalog_sha256': corpus.digest(after), 'review': review,
    'reason': 'Root explicitly accepts immutable144-v3 after direct12-delta/source review and delegated whole144 field/boundary review. Fresh input only; retain all intrinsic guards and manual native source qualification. No automatic role, proof, old hash or operating activation.',
}
approval_ref = save('NATIVE-CATALOG-APPROVAL-144-V3.json', approval)
print(json.dumps({'catalog': catalog_ref, 'review': review_ref, 'acceptance': acceptance_ref,
                  'native_input_approval': approval_ref, 'changes_from139': len(changed),
                  'canonical_mutations': 0, 'candidate_proofs_approved': 0}))
