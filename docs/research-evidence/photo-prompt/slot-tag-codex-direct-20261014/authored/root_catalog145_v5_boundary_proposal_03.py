"""Serialize root's exact object/material boundary refinement for peer review.

This is a new immutable research proposal. It does not approve a catalog,
change a worker input, re-sign a proof, or touch any operating asset.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


name = 'authored/native_catalog_v5_gap_proposal_02.json'
path = HERE / name
proposal = json.loads(path.read_bytes())
assert hashlib.sha256(path.read_bytes()).hexdigest() == '98e8d0fb4dda2e27b045efbb9612fb72da1eeccbaa77e9d461d8c0f8b8d54bb2'
before = json.loads((HERE / 'CATALOG-FINAL-144-V4.json').read_bytes())
after = copy.deepcopy(proposal['proposed_catalog'])
assert digest(after) == '33c58e7ef18f1e5c165427266ffa0775af8db9c13c87c48b02aa2b6b5159a108'
after['object_structure']['excludes'].append(
    'Macroscopic form of a free fluid, coherent material mass or transient material body is material_form when that material body is the actual declared carrier. A separately identified vessel, fixture, discrete object or constructed item keeps its own object_structure scope. Do not duplicate the same contour merely by renaming its carrier object or matter.')
after['object_structure']['neighbors'].append('material_form')
old_exclusion = after['material_form']['excludes'][0]
assert old_exclusion == 'Constructed/bounded physical-object or fixture geometry and part assembly already owned by object_structure; garment form/construction or anatomy already owned by their specialized roles. Do not duplicate the same fact by renaming its owner matter.'
after['material_form']['excludes'][0] = (
    'Geometry or part assembly of a separately identified discrete object, vessel, fixture or constructed item belongs to object_structure; garment construction and anatomy retain their specialized roles. A material-body contour is not a container or emitter-housing contour. Softness alone does not turn a constructed object or textile panel into a free material mass. Preserve the actual declared carrier and do not duplicate the same contour by renaming it object or matter.')
assert len(after) == 145
changed = sorted(key for key in after if before.get(key) != after[key])
assert changed == ['age_presentation', 'gaze_target', 'material_form', 'object_structure', 'proxemics', 'skin_finish', 'space_condition']
out = {'schema': 'photo-root-catalog-boundary-proposal/v1', 'actor': '/root',
    'research_only': True, 'prior_proposal': {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': digest(proposal)},
    'prior_catalog_sha256': digest(before), 'proposed_catalog': after,
    'proposed_catalog_sha256': digest(after), 'proposed_count': 145,
    'changed_or_new_specs': changed,
    'exact_refinement_from_proposal02': {
        'object_structure_added_exclusion': after['object_structure']['excludes'][-1],
        'object_structure_added_neighbor': 'material_form',
        'material_form_replacement_exclusion_before': old_exclusion,
        'material_form_replacement_exclusion_after': after['material_form']['excludes'][0]},
    'root_reason': 'The existing general physical-object wording and the proposed bounded material-body wording could otherwise overlap. Keep a named material body and a separate vessel/discrete structured object distinct by their actual source carrier; deformation or softness alone is not a new generic material role. Both definitions explicitly prevent same-contour duplication.',
    'root_direct_read_scope': {
        'all144_existing_summary_descriptions_dimensions_owners_prefixes': True,
        'complete_six_proposal02_after_specs_and_previous_specs': True,
        'actual_eight_complete_source_records_and_own_bindings_read': True,
        'actual_eight_historical5B_records_read_in_this_session': True,
        '1295_complete_owner_scope_revision_previously_directly_read': True,
        'fresh_all145_fullspec_read_claimed': False},
    'not_a_candidate_review': 'Actual eight witnesses motivate slot boundaries; this proposal grants no per-CID proof, mode, tag, source correction, identity, count, introduction or permission. Their full-source unresolved clauses remain unresolved.',
    'independent_review_required_before_catalog_input_approval': True,
    'current144_catalog_or_worker_inputs_changed': False,
    'old_proofs_statuses_or_acceptances_changed': False,
    'operational_changes': 0, 'gemini_calls': 0, 'provider_network_calls': 0}
target = HERE / 'authored/root_catalog145_v5_boundary_proposal_03.json'
with target.open('x') as stream:
    json.dump(out, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
print(json.dumps({'file': str(target.relative_to(ROOT)), 'catalog_count': 145, 'catalog_sha256': digest(after), 'proposal_sha256': digest(out), 'approved': False}))
