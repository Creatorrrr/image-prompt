"""Root's literal seven native judgements and thirteen explicit pending rows.

Root directly read all20 whole originals/current records, exact original5B,
own bindings and empty closures. Main full specs and relevant contrast specs
were read. The values/roles/owners/modes below are manual, not 5B conversion.
Research files only; no operating source writes or semantic inference loop.
"""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[2]
ROOT = HERE.parents[3]
GEN = Path.home() / '.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2'
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
sys.path.insert(0, str(HERE))
import native_reviews as reviews
sys.path[:0] = [str(GEN / 'scripts'), str(GEN / 'precore')]
OUT = Path(__file__).resolve().parent
PREP = HERE / 'native-inputs/prepared/root-00000-00020-01'
assignment = reviews.read_json(PREP / 'ASSIGNMENT.json')
inp = reviews.artifact(ROOT, assignment['input'])
packet = reviews.read_json(PREP / 'PREPARED-PACKET.json')
current = reviews.artifact(ROOT, inp['current_snapshot'])
catalog = current['slot_catalog']
approval = reviews.read_json(HERE / 'native-inputs/root-00000-00020-plan-01/SOURCE-APPROVAL.json')
deltas = {row['candidate_id']: row['delta'] for row in approval['changes']}
# ordinal, exact role, dimension, local owner, frozen fixed role, literal effects,
# literal whole-source interpretation; all selected manually by root.
JUDGEMENTS = [
    (3, 'genre', 'style', 'image', 'image', [('genre.selection', 'photo.genre/v1', 'fantasy', 'fantasy', '판타지')],
     '판타지/장르 선택만 image style 효과로 지정한다. 판타지 생물·마법 사건·세계 법칙·시대·장소는 선언하지 않는다.'),
    (4, 'genre', 'style', 'image', 'image', [('genre.selection', 'photo.genre/v1', 'fine_art', 'fine art', '파인아트')],
     '파인아트/사진 작업의 장르만 image style 효과로 지정한다. gallery 태그를 화랑 장소·매체·미술 운동의 긍정 근거로 쓰지 않는다.'),
    (5, 'motion_rendering', 'camera', 'image', 'image', [('image.motion.rendering', 'image.motion.rendering/v1', 'motion_blur', 'motion blur', '모션 블러')],
     '영상 면의 모션 블러를 선택한다. 물리 동작·주체의 속도·이동 방향·패닝·촬영자 움직임·candid 이력을 추론하지 않는다.'),
    (9, 'lens', 'camera', 'camera', 'recording_camera', [('lens.focal_length_mm', 'lens.focal_length_mm/v1', 50, '50mm', '50mm'), ('lens.named_class', 'lens.named_class/v1', 'standard', 'standard', '표준')],
     '기록 카메라의 렌즈 초점거리50mm와 명시된 standard/표준 명명 분류를 함께 선택한다. 센서별 실제 화각·거리·조리개·심도·초점면을 추가하지 않는다.'),
    (16, 'mood', 'atmosphere', 'scene', 'scene', [('mood.proposed_reading', 'mood.proposed_reading/v1', 'focused', 'focused atmosphere', '집중한 분위기')],
     '집중감 있는 장면 분위기의 선택이다. 한국어 뜻에 맞춰 영어를 명료화했고 광학 초점·특정 표정·인물의 실제 내면은 주장하지 않는다. contextual 역할과 실제 atmosphere 선택 효과를 구별한다.'),
    (17, 'lens', 'camera', 'camera', 'recording_camera', [('lens.focal_length_mm', 'lens.focal_length_mm/v1', 24, '24mm', '24mm'), ('lens.named_class', 'lens.named_class/v1', 'wide_angle', 'wide-angle', '광각')],
     '기록 카메라의 렌즈 초점거리24mm와 명시된 wide-angle/광각 분류를 함께 선택한다. 센서 크기·실제 화각·거리·카메라 높이·왜곡·신체 과장을 추가하지 않는다.'),
    (18, 'location', 'setting', 'scene', 'scene', [('setting.location.kind', 'setting.location.kind/v1', 'laboratory', 'a laboratory', '실험실')],
     '실험실이라는 물리 장소 종류를 scene setting 효과로 선택한다. 연구원·실험 행위·구체 장비·의료 목적·멸균·안전 등급·광원을 태그에서 발명하지 않는다.'),
]
PENDING = {
    0: '네온 광원 의미는 직접 읽었으나 실제 광원 carrier와 적용·보존/선택 범위를 아직 완전한 native 계약으로 정하지 않았다. 네온색·간판·도시·새 장치를 추가하지 않는다.',
    1: 'lab LED의 LED 광원은 명시됐지만 lab 수식과 실제 광원 소유/적용 범위는 재심사가 필요하다. 실험실 장소나 임상 성능을 추론하거나 lab 뜻을 지우지 않는다.',
    2: '소프트박스 장치/광원 수정자의 의미와 실제 carrier 적용을 정하지 않았다. 이름만으로 화면 그림자 경계·각크기·거리·새 장치를 확정하지 않는다.',
    6: 'flash와 hard의 두 실제 광원/광질 의미를 유지해야 한다. 실제 소유/적용 범위를 완전한 계약으로 정하지 않아 보류한다. 정면·밝기·색을 추가하지 않는다.',
    7: '조명 맥락의 fluorescent 광원 의미와 물체 형광색/도료 의미를 구별해야 한다. 정확한 광원 carrier 적용 미확정으로 보류한다. 색편이·깜빡임·병원을 추론하지 않는다.',
    8: '여행 사진의 장르는 장치나 매체가 아니다. 실제 여행 이력/장소를 만들지 않으면서 전체 작업 주제와 적용을 보존하는 계약을 별도로 심사한다.',
    10: '반려동물 사진의 실제 주제 의무를 generic genre 값 하나로 잃거나 반려동물/주인을 새로 추가할 수 없다. 주제 전제와 적용 범위를 보류한다.',
    11: 'golden hour 짧은 본문은 실제 자연광 하루 시점과 모방 조명 처리를 구별하지 않는다.144V4 time_of_day는 의도 명료화를 요구하므로 옛5B 승인을 재사용하지 않는다.',
    12: '창을 통한 빛과 soft 광질을 모두 보존하되 실제 광원/통로 소유·적용 범위가 필요하다. 창/커튼/실내/입사 방향을 새로 만들지 않는다.',
    13: '음식 사진의 실제 음식 주제를 generic style로 지우거나 새 음식·그릇·조리 동작을 만들 수 없다. 전체 적용 전제의 직접 심사를 보류한다.',
    14: '디젤펑크 감성은 미감 선택이지만 현재 원본의 setting 효과는 그대로 채택할 수 없다. literal style 효과 보정과 실제 적용 명세를 먼저 심사한다.',
    15: '거리 사진 작업 장르를 실제 도시·군중·비연출 이력으로 확대하지 않는다. 전체 작업 주제/적용 전제와 genre 선택을 별도 심사한다.',
    19: '인테리어 사진의 실제 공간 주제를 generic genre 값으로 없애거나 방·가구를 새로 만들지 않는다. 전제와 선택 효과를 별도 심사한다.',
}
judgements = {row[0]: row for row in JUDGEMENTS}
rows = []
for ordinal, cid in enumerate(assignment['ids']):
    before = packet['original_records'][cid]; after = packet['current_records'][cid]
    assert packet['references'][cid] == packet['reference_bindings'][cid] == {}
    old = packet['historical_compiled_rows'][cid]; loc = inp['original_decisions'][cid]
    proof = None
    if ordinal in judgements:
        _, role, dimension, target, core_role, effects, rationale = judgements[ordinal]
        facts = []
        for lang, quote_index in [('en', 3), ('ko', 4)]:
            for index, effect in enumerate(effects):
                prop, value_type, value = effect[:3]; quote = effect[quote_index]
                assert quote in after['content'][lang]
                facts.append({'id': lang + str(index), 'realization_id': 'base', 'pointer': '/content/' + lang,
                    'quote': quote, 'dimension': dimension, 'target': target, 'property': prop,
                    'mode': 'effect', 'value': {'type': value_type, 'value': value},
                    'operation': 'set_value', 'receivers': [], 'requires': []})
        correction = {'before_sha256': native.meaning_sha256(before), 'after_sha256': native.meaning_sha256(after), 'rationale': rationale}
        proof = {'schema': native.SCHEMA, 'meaning_sha256': native.meaning_sha256(after),
            'catalog_sha256': c.digest(catalog), 'complete': True, 'facts': facts,
            'roles': {role: {'spec_sha256': c.digest(catalog[role]), 'scope': 'whole_record', 'realization_ids': ['base'],
                'fact_refs': [fact['id'] for fact in facts], 'support_modes': ['effect']}},
            'owner_maps': {'base': {'schema': 'photo-native-owner-bindings/v2', 'bindings': [
                {'target': target, 'core_role': core_role, 'origin': 'existing', 'introduced_by': None}]}},
            'source_units': [{'realization_id': 'base', 'pointer': '/content/' + lang, 'quote': after['content'][lang],
                'fact_refs': [fact['id'] for fact in facts if fact['pointer'] == '/content/' + lang], 'disposition': 'semantic'} for lang in ['en', 'ko']],
            'effect_sets': {'base': copy.deepcopy(after['effects'])}, 'dependencies': {'base': []}, 'reference_sha256': {},
            'guard_sets': {'base': {'source_conditions': [{}, {}], 'member_conditions': {}}}, 'profile_contracts': {'base': None},
            'review': {'basis': rationale, 'whole_source_reviewed': True, 'source_correction': correction,
                'original_review': {'candidate_id': cid, 'source_record_sha256': old['source_record_sha256'],
                    'catalog_sha256': old['catalog_sha256'], 'decision_sha256': loc['row_sha256'], 'artifact': loc['file'] + '#item=' + str(loc['item'])},
                'native_review': {'reviewer': '/root', 'method': 'codex_direct_source_read', 'native_contract_sha256': ''}}}
        proof['review']['native_review']['native_contract_sha256'] = native.native_contract_sha256(proof)
    else:
        rationale = PENDING[ordinal]
    requirement = inp['required_revisions'][cid]
    rows.append({'candidate_id': cid, 'ordinal': ordinal, 'status': 'approved' if proof else 'pending',
        'rationale': rationale, 'source_before': before, 'source_after': after,
        'delta': deltas.get(cid, []), 'original_compiled': loc, 'proof': proof,
        'dependency_records': {}, 'reference_bindings': {}, 'source_reread_complete': True,
        'reference_reread_complete': True, 'revision': {'prior_review': requirement['prior_review'],
            'memo_artifacts': requirement['memo_artifacts'], 'rationale': rationale}})
batch = {'schema': reviews.BATCH, 'task_name': '/root', 'model': assignment['model'],
    'reasoning_effort': assignment['reasoning_effort'], 'assignment_sha256': c.digest(assignment),
    'input_sha256': assignment['input']['sha256'], 'prepared_count': 20, 'actual_read_count': 20, 'records': rows}
note = {'schema': reviews.NOTE, 'task_name': '/root', 'model': assignment['model'],
    'reasoning_effort': assignment['reasoning_effort'], 'assignment_sha256': c.digest(assignment),
    'input_sha256': assignment['input']['sha256'], 'batch_sha256': c.digest(batch), 'prepared_count': 20,
    'actual_read_count': 20, 'whole_source_read_ids': assignment['ids'], 'whole_dependency_read_ids': assignment['ids']}
for name, value in [('BATCH.json', batch), ('NOTE.json', note)]:
    with (OUT / name).open('xb') as stream: stream.write(c.canonical_bytes(value) + b'\n')
print(json.dumps({'actual_read': 20, 'root_authored_proofs': 7, 'pending': 13,
    'new_facts': sum(len(row['proof']['facts']) for row in rows if row['proof']), 'operating_changes': 0}))
