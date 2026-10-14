"""Root's explicit humidity addition and bilingual occasion-boundary repair.

This serializes a new research proposal after direct definition/source reads.
It neither approves a catalog nor converts any proof or operating asset.
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


def artifact(name):
    path = HERE / name
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


fixed = json.loads((HERE / 'authored/root_catalog145_v5_boundary_proposal_03.json').read_bytes())
assert digest(fixed) == 'a80ab9a85881fbc4533f3bb88855da4344a80c54b12938065c826c27dfca4ee2'
peer_name = 'worker-notes/native-12250-root145-v5-independent-20261015.json'
peer_path = HERE / peer_name
peer = json.loads(peer_path.read_bytes())
assert hashlib.sha256(peer_path.read_bytes()).hexdigest() == '40193e7a226ef536b2701a7d3051e34646d341be4f1f1ebb236145e09fa1806c'
before = json.loads((HERE / 'CATALOG-FINAL-144-V4.json').read_bytes())
after = copy.deepcopy(fixed['proposed_catalog'])
assert len(after) == 145
# Root read this complete proposed definition and the complete actual4948
# original/current/5B/own-binding record before selecting the exact literal.
after['air_humidity'] = copy.deepcopy(peer['separate_4948_air_humidity_opinion']['proposed_full_spec_research_only'])
after['atmospheric_medium']['excludes'].append(
    'An explicitly humid or dry air state without a stated spatial optical response belongs to air_humidity. Air humidity alone establishes neither fog, attenuation, visible droplets nor wet surfaces.')
after['atmospheric_medium']['neighbors'].append('air_humidity')
# The prior English definition already excludes arbitrary process steps. Its
# Korean explanation contradicted that boundary by saying generic preparation,
# review and work stages are included; its exclusion repeated that same phrase.
old_occasion_ko = after['occasion_context']['description_ko']
old_occasion_excludes = copy.deepcopy(after['occasion_context']['excludes'])
assert '현재 일반 준비·검토·작업 단계도 포함' in old_occasion_ko
after['occasion_context']['description_ko'] = (
    '명시된 행사·의례·계기·일정이 장면에 부여하는 맥락. 일반 준비·검토·작업의 진행 단계 자체를 행사나 계기로 확대하지 않으며, 행사 맥락과 과정 시점은 별도로 판정한다.')
after['occasion_context']['excludes'] = [
    'An arbitrary preparation, review or work-process stage alone does not establish an occasion, ceremony or scheduled event. A genuinely declared event may coexist with its separately stated process or narrative phase.',
    'Do not infer an event, real ceremony, participant role or completed occurrence from a ritual-like style, location, object, generic activity or provenance label alone.']
for key in ['narrative_phase', 'procedure_step']:
    assert key not in after['occasion_context']['neighbors']
    after['occasion_context']['neighbors'].append(key)
changed = sorted(key for key in after if before.get(key) != after[key])
assert changed == ['age_presentation', 'air_humidity', 'atmospheric_medium', 'gaze_target', 'material_form', 'object_structure', 'occasion_context', 'proxemics', 'skin_finish', 'space_condition']
assert len(after) == 146
assert sum(after[key] == value for key, value in before.items()) == 136
report = {'schema': 'photo-root-catalog-boundary-proposal/v1', 'actor': '/root', 'research_only': True,
    'prior_fixed145_proposal': artifact('authored/root_catalog145_v5_boundary_proposal_03.json'),
    'independent_fixed145_review_and_separate_humidity_opinion': artifact(peer_name),
    'prior_approved144_catalog_sha256': digest(before), 'proposed_catalog': after,
    'proposed_catalog_sha256': digest(after), 'proposed_count': 146,
    'changed_or_new_specs_from144': changed, 'exact_unchanged_existing_specs_from144': 136,
    'new_slots': ['material_form', 'air_humidity'],
    'new_changes_from_fixed145': {
        'air_humidity': 'Root explicitly selects the independently proposed full bounded definition after reading all of it and actual4948; this is a new general role, not a special mushroom slot.',
        'atmospheric_medium': 'Keep spatial optical response separate from explicitly declared humidity, with a reciprocal exclusion and neighbor only.',
        'occasion_context': {'before_description_ko': old_occasion_ko, 'before_excludes': old_occasion_excludes,
            'root_reason': 'Repair a real bilingual contradiction; keep the existing English event/occasion meaning. Generic process steps alone remain with their own roles, while an actual occasion may coexist with a stated process phase. No intrinsic/binding/domain gate is removed.'}},
    'root_read_scope': {
        'prior_fixed145_and_eight_witnesses': 'Pinned root03 and independent81-spec review; no new full145 or146 read count inferred.',
        'full_humidity_air_medium_surface_moisture_weather_thermal_space_condition_specs_directly_read': True,
        'complete_actual4948_original_current_5B_ownbinding_directly_read': True,
        'full_current_occasion_context_directly_read': True,
        'root_authored_exact_new_air_medium_and_occasion_boundaries': True,
        'fresh_all146_fullspec_read_claimed': False},
    'independent_new_definition_review_required': True, 'catalog_input_approval': None,
    'not_a_candidate_review': 'All actual source clauses, existing guards, owner/receiver evidence, P/E/preservation, exact mode and permission obligations remain independently reviewed. This grants no per-CID tag or proof.',
    'old_proofs_statuses_acceptances_changed': False, 'current_worker_inputs_changed': False,
    'operational_changes': 0, 'gemini_calls': 0, 'network_calls': 0}
target = HERE / 'authored/root_catalog146_v5_humidity_proposal_04.json'
with target.open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
print(json.dumps({'file': str(target.relative_to(ROOT)), 'catalog_count': len(after), 'catalog_sha256': digest(after), 'proposal_sha256': digest(report), 'approved': False}))
