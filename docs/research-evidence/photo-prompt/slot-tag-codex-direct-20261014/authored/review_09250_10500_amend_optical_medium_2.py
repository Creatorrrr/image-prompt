"""Serialize two individually authored sparse rereviews; no registration or inference."""
import hashlib
import json
from pathlib import Path
import sys

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R))
import direct_review as dr
from photo_candidate_realizations import ids as realization_ids

TASK = '/root/review_09250_10500'
NAME = 'review_09250_10500_amend_optical_medium_2'
OUT = R / 'authored' / (NAME + '.json')
NOTE = R / 'worker-notes' / (NAME + '.json')
BEFORE = R / 'authored/review_09250_10500_10250_10500.json'
EXPECTED_BEFORE_RAW = '5fd00568685c48afac6b9c38698db7c2b1c2d11b4136a41afe1a03cbb43031e0'
PACKET = R / 'packets/10250-250.json'

# Each fact, role and rejected boundary below was individually authored after
# complete source and actual fullspec rereading, not selected by a classifier.
DECISIONS = [
    {
        'ordinal': 10376,
        'candidate_id': 'cand_03d2d6fcaaa7591b8d08b9321aaa0ce8',
        'meaning_summary': '기존의 명시된 밝은 광원이 카메라 광학 경로에 들어와 촬영 영상에 그 광원 방향의 발광 베일과 뒤 세부의 대비 감소를 만든다.',
        'roles': [{
            'slot_id': 'lens_artifact',
            'rationale': '카메라 경로와 captured image를 직접 명시한 베일형 광학 플레어이다. 인코딩·신호 처리 손상이나 공간의 실제 연무가 아니다.',
            'facts': [{
                'pointer': '/content/paraphrases/1',
                'quote': 'one declared bright source entering the camera path; a luminous veil across the captured image toward that source; reduced contrast in detail behind the veil',
                'dimension': 'camera', 'target': 'image',
                'property': 'image.optical_artifact.source_aligned_veiling_flare_contrast_loss'
            }]
        }],
        'rejected_boundaries': [
            'image_artifact는 인코딩·스캔·신호·처리 흔적이며 optical effects를 제외하므로 이 source의 광학 경로 플레어를 맡기지 않는다.',
            '실제 공간의 연무·화염막·전역 주황색 색보정과 구별한다. 다각형 고스트는 필수가 아니며, 새 광원·정확한 렌즈 모델·노출 설정을 추가하지 않는다.',
            '광원과 영상의 대비 베일 관계만 주장한다. 물리적 열·화학 반응·안전·소리·동기를 영상에서 확정하지 않는다.'
        ]
    },
    {
        'ordinal': 10423,
        'candidate_id': 'cand_85eb4ad2d30e54a3b8718ccdb6c929e3',
        'meaning_summary': '지면이나 물 가까이 낮게 뜬 안개·연무층에서 먼 물체의 대비가 낮아지고 가까운 경계는 더 읽히는 거리별 차폐를 표현한다. 안개·물안개라는 명시 상태를 유지한다.',
        'roles': [{
            'slot_id': 'atmospheric_medium',
            'rationale': '낮은 suspended haze와 거리별 대비 감쇠를 환경 매질의 공간 광학 상태로 직접 표현한다. 분리되어 보이는 개별 입자의 크기·수·분포가 양의 근거로 제시되지 않았다.',
            'facts': [{
                'pointer': '/content/en',
                'quote': 'a low suspended haze near the ground or water; distant objects losing contrast; nearer edges remaining more legible',
                'dimension': 'atmosphere', 'target': 'scene_air',
                'property': 'air.medium.low_suspended_haze_distance_attenuation_near_edges_legible'
            }]
        }, {
            'slot_id': 'spatial_depth',
            'rationale': '원경 물체의 낮은 대비와 근경 경계의 높은 가독성을 한 양의 필드에서 대조하여 장면 깊이에 따른 관계를 명시한다.',
            'facts': [{
                'pointer': '/content/en',
                'quote': 'a low suspended haze near the ground or water; distant objects losing contrast; nearer edges remaining more legible',
                'dimension': 'composition', 'target': 'objects_haze',
                'property': 'spatial.depth.distant_contrast_loss_nearer_legible_edges'
            }]
        }, {
            'slot_id': 'weather',
            'rationale': '한국어 양의 필드가 안개·해무·물안개를 직접 선언한다. 명시된 안개 상태만 유지하고 기상 원인이나 추가 지형을 추론하지 않는다.',
            'facts': [{
                'pointer': '/content/ko', 'quote': '안개·해무·물안개의 깊이 차폐',
                'dimension': 'atmosphere', 'target': 'scene',
                'property': 'weather.condition.declared_fog_or_mist'
            }]
        }],
        'rejected_boundaries': [
            'ambient_particle에 필요한 분리되어 보이는 입자 단위가 제시되지 않았다. droplet_haze라는 관계 주체나 물안개라는 이름만으로 개별 물방울 수·크기·분포를 만들지 않는다.',
            'atmospheric_medium 선택은 물리적으로 입자가 전혀 없다는 화학·물리 주장이 아니다. 관찰 근거가 개별 입자보다 안개층과 거리별 감쇠라는 뜻이다.',
            '흰 수증기·연기와 동의어로 쓰지 않는다. 해무라는 출처는 실제 연안 맥락이 있는 경우에만 유지하며 새 연안 위치를 넣지 않는다.',
            '선언된 안개·물안개 상태와 원근 대비 관계를 유지하되 정확한 물방울 크기·기상 원인·화학 정체·안전·과거·소리·냄새는 확정하지 않는다.'
        ]
    }
]

def rawsha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert not OUT.exists() and not NOTE.exists(), 'immutable artifacts already exist'
    assert rawsha(BEFORE) == EXPECTED_BEFORE_RAW, 'original frozen file changed'
    data = dr.source()
    packet = json.loads(PACKET.read_text())
    previous = json.loads(BEFORE.read_text())['decisions']
    order = json.loads((R / 'ORDER.json').read_text())
    assert packet['source_sha256'] == dr.c.digest(data)
    assert packet['catalog_sha256'] == dr.c.digest(data['slot_catalog'])
    assert set(packet['records']) == set(packet['ids']) == set(packet['references'])
    for cid in packet['ids']:
        assert packet['records'][cid] == data['candidates'][cid]
        assert packet['references'][cid] == dr.closure(data, cid)
    amendments = []
    bindings = []
    for authored in DECISIONS:
        ordinal, cid = authored['ordinal'], authored['candidate_id']
        assert order[ordinal] == cid
        original = previous[ordinal - 10250]
        assert original['candidate_id'] == cid and original['status'] == 'approved'
        assert realization_ids(data['candidates'][cid]) == ['base']
        decision = {k: authored[k] for k in ('candidate_id', 'meaning_summary', 'rejected_boundaries')}
        decision.update(recommended_kind='visual_option', corrections=[], roles=[], facts=[],
                        uncertainties=[], status='approved', all_roles_considered=True)
        for role in authored['roles']:
            decision['facts'].extend(dict(fact, realization_id='base') for fact in role['facts'])
            decision['roles'].append(dict(slot_id=role['slot_id'],
                semantic_role=data['slot_catalog'][role['slot_id']]['semantic_role'],
                scope='whole_record', realization_ids=['base'], rationale=role['rationale'],
                evidence=role['facts']))
        binding = dr.binding(data, cid)
        item = len(amendments) + 1
        full = {**decision, **binding, 'schema': dr.SCHEMA, 'reviewer': 'Codex',
            'review_method': 'codex_direct_source_read', 'independent_human_review': False,
            'authored_decision': {'file': str(OUT.relative_to(dr.ROOT)), 'item': item,
                                  'sha256': dr.c.digest(decision)},
            'packet_sha256': dr.c.digest(packet)}
        dr.validate_decision(full, data)
        reread_id = f'review_09250_10500_optical_medium_{ordinal}_full_reread'
        entry = dict(reread_id=reread_id, candidate_id=cid, ordinal=ordinal,
            task_name=TASK, model='gpt-6.1-sol', reasoning_effort='high',
            source_reread_complete=True, reference_reread_complete=True,
            source_record_sha256=binding['source_record_sha256'],
            catalog_sha256=binding['catalog_sha256'],
            after_proposal_reference_sha256=binding['reference_sha256'],
            before_authored_file=str(BEFORE.relative_to(dr.ROOT)),
            before_authored_item=ordinal - 10250 + 1,
            before_authored_row_sha256=dr.c.digest(original),
            before_authored_file_raw_sha256=rawsha(BEFORE),
            before_status=original['status'], actual_realization_ids=['base'],
            corrected_role_spec_sha256={role['slot_id']: dr.c.digest(data['slot_catalog'][role['slot_id']])
                                       for role in decision['roles']},
            full_packet_sha256=dr.c.digest(packet),
            after_proposal_conditions=data['candidates'][cid]['conditions'],
            after_proposal_effects=data['candidates'][cid]['effects'], decision=decision)
        amendments.append(entry)
        bindings.append({k: v for k, v in entry.items() if k != 'decision'})
    document = dict(schema='photo-codex-direct-review-amendment/v1',
        source_sha256=dr.c.digest(data), catalog_sha256=dr.c.digest(data['slot_catalog']),
        packet_sha256=dr.c.digest(packet), amendments=amendments)
    OUT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n')
    note = dict(task_name=TASK, agent_id=TASK, model='gpt-6.1-sol', reasoning_effort='high',
        status='final_ready_frozen_sparse_amendment', final_ready=True,
        packet_paths=['packets/10250-250.json'],
        authored_paths=[str(OUT.relative_to(R)), str(Path(__file__).relative_to(R))],
        complete_source_read=True, complete_source_reread=True,
        directly_reread_count=2, directly_reread_candidate_ids=[e['candidate_id'] for e in amendments],
        reread_ids=[e['reread_id'] for e in amendments],
        approved_count=2, still_pending_count=0, approved_ordinals=[10376,10423], unresolved_ordinals=[],
        source_sha256=dr.c.digest(data), catalog_sha256=dr.c.digest(data['slot_catalog']),
        packet_sha256=dr.c.digest(packet),
        authored_file_sha256={str(OUT.relative_to(R)): rawsha(OUT),
                             str(Path(__file__).relative_to(R)): rawsha(Path(__file__))},
        immutable_original_file=str(BEFORE.relative_to(R)),
        immutable_original_raw_sha256=rawsha(BEFORE),
        complete_reread_bindings=bindings,
        actual_fullspec_reread_ids=['lens_artifact','image_artifact','atmospheric_medium',
                                   'ambient_particle','spatial_depth','weather'],
        validation={'direct_review_validate_decision': 'passed_2_of_2',
                    'full_250_record_packet_and_reference_closure_binding': 'passed',
                    'original_raw_sha256_unchanged': True,
                    'original_status_to_proposed_status': 'approved_to_approved_2_of_2'},
        specific_qualification_issues=[
            'Two complete frozen records including all content, contextual usage/limits, conditions, effects, provenance and reference closure were actually reread, and all six relevant fullslot contracts actually reread. Both reference closures are empty; this is a complete empty closure, not skipped reference reading.',
            '10376 replaces image_artifact with lens_artifact; optical camera-path evidence excludes encoding/signal/processing ownership. 10423 replaces ambient_particle with atmospheric_medium, preserves independently evidenced spatial_depth and declared weather, and narrows weather positive evidence to the exact Korean declaration.',
            'These are semantic role amendments only. Native conditions/effects are attested unchanged; existing optical.lens_artifact and particle_structure source effects do not by themselves prove native qualification for the new facts. Parent must perform subsequent canonical/native conversion and qualification. Catalog applicability proposals are separate and unapplied.',
            'Original 250-item authored JSON, original literal script, original worker note, source, canonical records, catalog, registration and Git were not edited. No model, image, embedding or network calls were made; direct_review validation runs offline with provider variables removed.',
            'No source corrections are proposed for these two records; all positive quotes bind exactly to the current frozen source. Actual record_kind visual_option and actual realization base are verified for both.'
        ],
        related_boundary_followup_candidates=[
            {'ordinal':10288, 'finding':'Previously directly read condensed spring mist has the same unresolved-medium versus individually distinguishable-particle boundary. Listed for new full reread, not automatically amended.'},
            {'ordinal':10350, 'finding':'Previously directly read smoke wisp has the same continuous-medium versus individually distinguishable-particle boundary. Listed for new full reread, not automatically amended.'},
            {'ordinal':10382, 'finding':'Previously directly read dense ceiling smoke and lower-room legibility have the same spatial-medium versus individually distinguishable-particle boundary. Listed for new full reread, not automatically amended.'}
        ],
        no_automatic_tag_classifier=True, no_registration=True, no_canonical_or_source_mutation=True)
    NOTE.write_text(json.dumps(note, ensure_ascii=False, indent=2) + '\n')
    assert rawsha(BEFORE) == EXPECTED_BEFORE_RAW
    print(json.dumps({'authored':str(OUT.relative_to(R)), 'raw_sha256':rawsha(OUT),
        'note':str(NOTE.relative_to(R)), 'note_raw_sha256':rawsha(NOTE),
        'actual_reread_count':2,'approved_to_approved_count':2,'validation':'passed'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
