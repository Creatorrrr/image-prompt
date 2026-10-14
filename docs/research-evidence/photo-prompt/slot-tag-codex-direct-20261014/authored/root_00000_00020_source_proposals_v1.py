"""Serialize five literal root-authored corrections after complete source reads.

No native proof, tag decision, read-to-approval conversion or operating write.
The other fifteen sources are explicitly retained for separate native review.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]


def read(name):
    data = (HERE / name).read_bytes()
    return json.loads(gzip.decompress(data) if data[:2] == b'\x1f\x8b' else data)


def sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


source = read('SOURCE.json.gz')
current = read('native-inputs/11870-01250-01300-plan-03/CURRENT-PROPOSAL.json.gz')
order = read('ORDER.json')
catalog = read('CATALOG-FINAL-144-V4.json')
assert sha(current) == '30924a72de7d3011af26b7ef7c0192ff12edd732131f3c18ed29748e805d5477'
# Every value, property, target, role and boundary is a literal manual judgement.
choices = [
    (5, 'motion_rendering', 'camera', 'image', [('image.motion.rendering', {'type': 'image.motion.rendering/v1', 'value': 'motion_blur'})], None,
     '영상 면의 모션 블러를 camera 효과로 명시한다. 물리 동작·속도·방향·패닝·촬영자의 움직임·비연출 이력은 선택하지 않는다.'),
    (9, 'lens', 'camera', 'camera', [('lens.focal_length_mm', {'type': 'lens.focal_length_mm/v1', 'value': 50}), ('lens.named_class', {'type': 'lens.named_class/v1', 'value': 'standard'})], None,
     '본문이 직접 선언한 50mm와 standard/표준의 명명 분류를 모두 보존한다. 모든 센서에서 표준 화각이라는 보편 명제나 센서 크기·거리·조리개·심도·초점면을 추가하지 않는다.'),
    (16, 'mood', 'atmosphere', 'scene', [('mood.proposed_reading', {'type': 'mood.proposed_reading/v1', 'value': 'focused'})], 'focused atmosphere',
     '한국어 집중한 분위기가 지정한 장면 분위기 뜻으로 영어를 명료화한다. 광학 초점이나 인물의 실제 내면·직업·특정 표정은 선언하지 않는다. atmosphere의 실제 선택 효과를 context라는 이름으로 지우지 않는다.'),
    (17, 'lens', 'camera', 'camera', [('lens.focal_length_mm', {'type': 'lens.focal_length_mm/v1', 'value': 24}), ('lens.named_class', {'type': 'lens.named_class/v1', 'value': 'wide_angle'})], None,
     '24mm와 wide-angle/광각의 명명 분류를 함께 보존한다. 센서나 화각 수치·거리·로우앵글·왜곡 정도·신체 과장을 계산하거나 추가하지 않는다.'),
    (18, 'location', 'setting', 'scene', [('setting.location.kind', {'type': 'setting.location.kind/v1', 'value': 'laboratory'})], None,
     '실험실이라는 물리 장소 종류의 setting 선택을 구체화한다. 연구원·실험 행위·특정 장비·의료 목적·멸균·안전 등급·조명을 태그에서 추론하지 않는다.'),
]
records = []
for ordinal, role, dimension, owner, values, english, reason in choices:
    cid = order[ordinal]
    before = current['candidates'][cid]
    assert before == source['candidates'][cid]
    after = copy.deepcopy(before)
    if english is not None:
        after['content']['en'] = english
    after['effects'] = {'dimensions': [dimension], 'properties': [
        {'dimension': dimension, 'target': owner, 'property': prop} for prop, _ in values]}
    records.append({'ordinal': ordinal, 'candidate_id': cid, 'source_original_full': before,
        'source_after_proposed_full': after, 'source_before_sha256': sha(before), 'source_after_proposed_sha256': sha(after),
        'literal_future_effect_values': [{'dimension': dimension, 'target': owner, 'property': prop,
            'mode': 'effect', 'operation': 'set_value', 'value': val, 'receivers': [], 'requires': []} for prop, val in values],
        'role_for_individual_native_review': role, 'role_spec_sha256': sha(catalog[role]),
        'reason': reason, 'old_compiled_row': read('decisions/batch_00000_00020.json')['decisions'][ordinal],
        'original_own_bindings': {bid: row for bid, row in source['slot_bindings'].items() if row['candidate_id'] == cid},
        'direct_reference_closure': {}, 'whole_source_before_read': True,
        'whole_selected_after_manually_authored': True, 'native_approved': False})
output = {'schema': 'photo-root-manual-whole-source-correction-proposals/v1', 'actor': '/root',
    'catalog_sha256': sha(catalog), 'source_snapshot_sha256': sha(current), 'records': records,
    'actual_whole_original_current_own_binding_and_exact5B_reads': list(range(20)),
    'read_boundary': 'All20 complete original/current sources, exact compiled5B rows and own bindings were directly read by root. Large pretty output was not counted as complete; the compact bounded redisplays supply the full rows. Main full specs were read; no fresh whole144 or full native proof read is claimed.',
    'other15_not_qualified_by_this_proposal': [i for i in range(20) if i not in {5, 9, 16, 17, 18}],
    'unresolved_boundaries': [
        '0/1/2/6/7/12: source-device/modifier naming and independently declared actual light ownership need an explicit complete native application; lab supplies no laboratory scene or clinical capability.',
        '10/13/19: pet/food/interior photographic themes must not be silently lost in a generic style label or used to add undeclared entities/places. Actual thematic prerequisite versus scene mutation needs individual adjudication.',
        '11: short golden hour does not settle actual day phase versus imitation lighting treatment under144V4. The old5B time_of_day approval is retained as history, not promoted.',
        '3/4/8/14/15: prior genre/aesthetic meaning remains available for fresh final-catalog native review; old proof hashes/statuses are not automatically updated.'
    ], 'source_after_personal_reread': False, 'canonical_changes': 0, 'native_proofs_written': 0,
    'candidate_tag_approvals': 0, 'gemini_calls': 0}
target = HERE / 'authored/root_00000_00020_source_proposals_v1.json'
with target.open('xb') as stream:
    stream.write(json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode() + b'\n')
print(json.dumps({'file': str(target.relative_to(ROOT)), 'sha256': sha(output), 'whole_before_reads': 20,
    'literal_source_correction_proposals': 5, 'native_approved': 0}))
