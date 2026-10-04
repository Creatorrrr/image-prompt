#!/usr/bin/env python3
"""Build research-only documents and proposals; never edits active assets/indexes."""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
def read(name):
    return json.loads((HERE / name).read_text())
def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

reference = read('REFERENCE-KEYWORDS.json')
audit = read('CURRENT-DATA-AUDIT.json')
inventory = read('CURRENT-INVENTORY.json')
snapshot = read('SOURCE-SNAPSHOT.json')
sources = read('SOURCES.json')['sources']
source_by_id = {r['id']: r for r in sources}
existing_keys = set(inventory['candidate_keys'])
existing_profiles = set(inventory['profile_ids'])
temporal = {24, 25, 26, 27, 28, 35, 81, 107, 108}
interpretive = set(range(1, 15)) | {33}
groups = [(1,14,'interpretation','해석·연출 의도'),(15,30,'eyes','눈·시선'),
          (31,39,'mouth','입·입꼬리'),(40,44,'head','머리·목'),
          (45,68,'pose','몸·지지·다리'),(69,82,'hands','손·접촉'),
          (83,96,'camera','샷·카메라·인물 프레이밍'),
          (97,108,'composition','구도·초점·시간'),(109,120,'lighting','조명')]

rows = []
for line in (HERE / 'TERM-SPECS.psv').read_text().splitlines():
    if not line or line.startswith('#'): continue
    cells = line.split('|')
    assert len(cells) == 9, (cells[0], len(cells))
    num = int(cells[0]); original = reference['rows'][num-1]
    g = next(g for g in groups if g[0] <= num <= g[1])
    current = audit['rows'][num-1]
    record = {
        'number': num, 'term': original['term'], 'category': g[3],
        'semantics_type': 'contextual_interpretation' if num in interpretive else ('temporal_or_state' if num in temporal else 'observable_configuration'),
        'component_policy': 'optional_examples_not_a_hard_recipe' if num in interpretive else 'requested_configuration_only',
        'observables_or_optional_examples_ko': cells[1].split(';'),
        'ownership_and_relations_ko': cells[2].split(';'),
        'confusion_boundaries_ko': cells[3].split(';'),
        'observability_gate_ko': cells[4],
        'existing_candidate_keys': list(filter(None, cells[5].split(','))),
        'existing_profile_ids': list(filter(None, cells[6].split(','))),
        'proposed_action_ko': cells[7], 'source_ids': cells[8].split(','),
        'source_scope': 'Sources support meanings or method distinctions; the observable decomposition and adoption design are analyst-authored proposals.',
        'current_inventory_probe': {
            'has_literal_or_substring_inventory_hit': bool(current['candidate_hits'] or current['profile_hits']),
            'candidate_hit_keys': [x['key'] for x in current['candidate_hits']],
            'profile_hit_ids': [x['id'] for x in current['profile_hits']],
            'boundary': 'Inventory text probe, not runtime routing, semantic equivalence, exposure, selection or render validation.'},
        'temporal_limits': ('Full order/duration/transition requires time evidence. A static state may be described, but does not establish the whole term.' if num in temporal else ('Tempo or internal interpretation is not established by a still image.' if num in interpretive else 'Current visible geometry only; do not infer internal state or hidden motion.')),
        'runtime_status': 'research_only_not_installed',
    }
    assert all(k in existing_keys for k in record['existing_candidate_keys'])
    assert all(k in existing_profiles for k in record['existing_profile_ids'])
    assert all(k in source_by_id for k in record['source_ids'])
    rows.append(record)
assert [r['number'] for r in rows] == list(range(1,121))
by_num = {r['number']:r for r in rows}
write('TERM-RESEARCH.json', {
    'schema_version':'seduction-term-research/v1', 'runtime_schema':False,
    'reference_conversation_id':reference['conversation_id'],
    'started_date_kst':'2026-10-04', 'completed_date_kst':'2026-10-05',
    'source_snapshot_head':snapshot['head'], 'term_count':120,
    'interpretive_terms':sorted(interpretive), 'explicit_temporal_terms':sorted(temporal),
    'terms':rows})

# Draft source fields are kept separate from provenance and migration constraints.
NEW = [
    ('se_lash_occluded_upward_gaze','gaze_engagement',18,'턱을 내린 채 윗속눈썹 아래로 올려다보기',
     'upward target gaze beneath visible upper lashes with the chin pitched slightly down',
     ['the declared actor chin is pitched slightly downward','the eyes aim above the head-facing axis toward the specified target','upper lashes partially overlap the visible upper eye apertures','the specified eyes remain visibly open'],
     [('relative_direction','main_subject.eyes','core_declared_gaze_target'),('counterorientation','main_subject.head','main_subject.eyes')],
     [('expression','main_subject','eyes.gaze_direction'),('expression','main_subject','face.expression'),('pose','main_subject','head.orientation')],
     '인물의 눈·턱·속눈썹과 시선 목표가 core에 있고 얼굴 방향/표정 변경 차원이 열려 있어야 한다.',
     'ae_bashful_direct와 의미 단위·적용 범위가 같으면 신규 생성 대신 그 후보 보강으로 합친다.'),
    ('se_upper_lid_dominant_half_lid','expression',19,'윗눈꺼풀 중심으로 좁아진 열린 눈',
     'partly open eyes narrowed primarily by lower-positioned upper eyelid margins',
     ['upper eyelid margins cover more of the upper irises','the specified eyes retain visible open apertures','lower eyelid contours are comparatively open beneath the narrowed upper contours'],
     [('visible_configuration','main_subject.upper_eyelids','main_subject.irises')],
     [('expression','main_subject','face.expression')],
     '눈꺼풀 구분이 가능한 얼굴 크롭과 열린 눈 조건이 필요하다.',
     'pv_half_lidded는 넓은 의미로 유지한다. 윗눈꺼풀 변형을 별도 후보로 둘지 기존 하위 문맥으로 둘지 검토한다.'),
    ('se_eye_visible_through_own_hair','gaze_engagement',30,'자기 머리카락 사이로 식별되는 눈과 시선',
     'a readable target-facing eye aperture remains visible between strands of the same actor hair',
     ['existing hair strands overlap part of the declared actor eye region','the specified eye aperture and iris-direction cue remain visible','the hair and eye belong to the same actor'],
     [('partial_occlusion','main_subject.hair','main_subject.eye_region'),('directed_gaze','main_subject.eyes','core_declared_gaze_target')],
     [('expression','main_subject','eyes.gaze_direction'),('appearance','main_subject','hair')],
     '원래 모발 길이/배치가 가능한 경우만 적용; hair 경로는 보수적 제안이며 실제 잠금 경로와 대조 전 채택 금지.',
     '앞머리/부분 가림 후보들과 actor-owned eye readability 의미가 동일하면 기존 관계 보강으로 전환한다.'),
    ('se_edge_on_hand_to_camera','hand_pose',71,'카메라에 좁은 손날을 보이는 손',
     'the declared hand presents its narrow edge toward the camera while its wrist remains connected',
     ['the palm and dorsal planes lie oblique to the camera axis','the narrow radial or ulnar hand edge faces the camera as explicitly specified','the wrist and forearm connect to the same actor hand'],
     [('orientation_to','main_subject.declared_hand_plane','camera.axis'),('attached_to','main_subject.declared_hand','main_subject.declared_forearm')],
     [('pose','main_subject','body.hand_configuration')],
     '지정 손 소유와 카메라 기준이 고정되어야 하며 손 크기/비율은 바꾸지 않는다.',
     '손 회전·프로파일 손 후보에 이미 동일 관계가 있으면 alias/relations만 보강한다.'),
    ('se_two_hands_different_heights','hand_pose',72,'같은 사람의 양손을 서로 다른 높이에 놓기',
     'both hands of the same actor occupy distinct heights relative to the torso axis',
     ['both declared hands remain visibly attached to the same actor arms','the hands lie at different torso-relative heights','each hand retains its existing finger configuration'],
     [('height_difference','main_subject.left_hand','main_subject.right_hand'),('reference_axis','main_subject.hands','main_subject.torso')],
     [('pose','main_subject','body.hand_configuration'),('pose','main_subject','body.arm_configuration')],
     '두 손/팔과 몸통 축이 보이고 다른 인물 손을 대체 사용하지 않아야 한다.',
     'stacked hands나 교차 손목과 같지 않다. 기존 비대칭 손 배치가 같은 범위면 재사용한다.'),
    ('se_cheek_fingertip_light_touch','contact_point',73,'손끝으로 자기 볼 가볍게 접촉',
     'one or more fingertips lightly contact the same actor cheek with the palm remaining off the cheek',
     ['declared fingertips meet the same actor cheek surface','a visible gap separates the palm from the cheek','the finger hand and forearm remain continuous'],
     [('light_contact','main_subject.declared_fingertips','main_subject.declared_cheek')],
     [('pose','main_subject','body.contact_configuration'),('pose','main_subject','body.hand_configuration')],
     '주체/볼 좌우/손 소유를 고정하고 손끝-볼 접점을 확인한다.',
     'hand_touching_face의 넓은 하위형; temple touch나 chin support의 동의어로 만들지 않는다.'),
    ('se_hand_hover_below_chin','hand_pose',74,'턱 아래에 간격을 두고 놓은 자기 손',
     'the actor hand is placed below the chin with a visible air gap',
     ['the declared hand sits below the same actor chin','a visible gap separates the hand from the chin','the hand and forearm belong to the same actor'],
     [('below','main_subject.declared_hand','main_subject.chin'),('separated_by_visible_gap','main_subject.declared_hand','main_subject.chin')],
     [('pose','main_subject','body.hand_configuration'),('pose','main_subject','body.arm_configuration')],
     '턱-손 경계와 간격이 보이는 크롭; 실제 지지/접촉이 요청되면 이 후보 제외.',
     'pv_chin_support와 반대 접촉 조건이며 범용 hand-under-chin의 하드 동의어로 삼지 않는다.'),
    ('se_one_hand_behind_head','hand_pose',76,'한 손만 자기 뒤통수에 놓기',
     'exactly the specified one hand rests at the actor posterior head while the other arm retains its existing posture',
     ['the specified single hand lies at the same actor posterior head','its elbow forearm and wrist form one continuous arm chain','the other hand retains its existing posture'],
     [('placed_at','main_subject.declared_hand','main_subject.posterior_head'),('attached_to','main_subject.declared_hand','main_subject.declared_arm')],
     [('pose','main_subject','body.hand_configuration'),('pose','main_subject','body.arm_configuration')],
     '한 손의 laterality와 반대 손 잠금을 보존한다.',
     'pv_arms_behind_head는 양손 변형으로 유지. 후보 이름만 바꾸어 양손형을 재사용하지 않는다.'),
    ('se_lapel_fingertip_touch','contact_point',78,'자기 옷 라펠에 손끝만 가볍게 대기',
     'fingertips lightly meet the edge of an existing garment lapel',
     ['an existing lapel edge remains connected to the same actor garment','declared fingertips contact that lapel edge','fingertip pads meet one exposed side of the lapel edge'],
     [('light_contact','main_subject.declared_fingertips','core_existing_garment.lapel_edge')],
     [('pose','main_subject','body.contact_configuration'),('pose','main_subject','body.hand_configuration')],
     'core에 라펠 있는 옷이 이미 존재해야 함; 새 옷깃/재킷 생성 금지.',
     'pv_lapel_grip와 실제 pinch 유무로 구분한다.'),
    ('se_small_garment_fold_pinch','contact_point',79,'기존 옷감의 작은 접힌 부분을 손끝으로 집기',
     'a thumb and fingertip pinch a small visible fold of the existing garment fabric',
     ['opposing thumb and fingertip hold the same small cloth fold','cloth is visibly interposed between the fingertips','the fold continues into the existing garment','the existing garment remains connected around the small local fold'],
     [('pinches','main_subject.declared_thumb_and_finger','core_existing_garment.small_fold'),('part_of','core_existing_garment.small_fold','core_existing_garment')],
     [('pose','main_subject','body.hand_configuration'),('pose','main_subject','body.contact_configuration'),('appearance','main_subject','garment')],
     '기존 옷과 작은 변형 허용 범위가 필요; garment 경로는 실제 의복 잠금과 검토 전 채택 금지.',
     'pv_hem_hold와 fingers_pinching_thread는 재질/집는 부위가 달라 단순 alias로 병합하지 않는다.'),
    ('se_existing_pendant_fingertip_hold','contact_point',80,'기존 목걸이 펜던트 본체를 손끝으로 잡기',
     'fingertips hold the existing pendant body while it remains visibly connected to its necklace chain',
     ['declared fingertips contact and hold the existing pendant body','the pendant remains attached to the same necklace chain','the chain belongs to the same actor accessory','the hand belongs to that actor'],
     [('holds','main_subject.declared_fingertips','core_existing_pendant.body'),('attached_to','core_existing_pendant.body','core_existing_necklace.chain')],
     [('pose','main_subject','body.hand_configuration'),('pose','main_subject','body.contact_configuration')],
     'core에 펜던트/체인이 이미 있음; 액세서리 추가/분리 없이 가시적 접점만 바꿀 수 있어야 함.',
     '액세서리 외형 후보와 분리된 접촉 의미다. 기존 장신구 만짐 후보에 동일 관계가 있으면 보강으로 합친다.'),
     ('se_cornea_catchlight_without_wetness','light_shape',119,'각막 표면의 작은 광원 반사점',
     'a small bounded source reflection is visible on the specified corneal surface',
     ['a small bounded highlight lies on the specified actor corneal surface','iris and lid boundaries remain visible around the reflection','iris texture remains readable around the bounded source reflection'],
     [('reflected_on','core_declared_light','main_subject.declared_cornea')],
     [('lighting','main_subject','eyes.light_reflection')],
     '조명/반사 경로와 눈 소유를 고정; eyes.light_reflection은 신규 세분 경로 제안으로 잠금 매핑 검토 필수.',
     'glossy_wet_catchlight_eyes와 vertical pair는 더 좁거나 복합 조건이므로 순수 반사점 전체를 대체할 수 없다.'),
    ('se_gaze_at_existing_partner_lips_state','gaze_engagement',28,'기존 상대의 입술을 향한 현재 시선 상태',
     'the declared actor current gaze is aimed at the already present partner lip region',
     ['the declared actor eye direction points to the existing partner lip region','the target lips belong to that same existing partner','both actor eyes and target lip region remain spatially distinct'],
     [('directed_gaze','main_subject.eyes','core_existing_partner.lips')],
     [('expression','main_subject','eyes.gaze_direction')],
     'core에 상대가 이미 존재하고 입 위치가 정의됨; 자동 상대 추가·키스 동작 추가 금지.',
     'to_partner_face_then_away는 시간/대상이 달라 동일하지 않다. eye-to-lip 전체 용어는 이 정지 상태에 하드 alias로 넣지 않는다.'),
    ('se_beckon_shaped_finger_static_state','hand_pose',81,'손바닥 방향이 읽히는 굽힌 손가락의 정지 상태',
     'the specified finger is visibly flexed against a readable hand plane in a beckoning-shaped current state',
     ['the specified finger bends at its connected joints','the palm-facing direction is readable relative to the specified target','the remaining fingers retain their existing arrangement'],
     [('flexed_state','main_subject.declared_finger','main_subject.declared_hand_plane'),('orientation_to','main_subject.declared_hand_plane','core_declared_gesture_target')],
     [('pose','main_subject','body.hand_configuration')],
     '손/손가락 수/대상 방향 고정; 반복 굽힘이나 초대 성공을 주장하지 않음.',
     'beckoning이라는 포괄 의도와 정지 모양을 분리한다. 기존 finger-curled 후보가 있으면 재사용한다.'),
]

candidate_drafts = []
for ident,slot,num,ko,en,units,rels,effects,conditions,dedup in NEW:
    dims = list(dict.fromkeys(x[0] for x in effects))
    entry = {'id':ident,'ko':ko,'en':en,'weight':1,
             'tags':['human','portrait'], 'for_any':['human','portrait'],
             'aliases':[ko,en], 'keywords':[ko,en],
             'embedding_text':en + '; ' + '; '.join(units),
             'concept_units':units,
             'relations':[{'id':f'{ident}_r{i+1}','type':t,'subject':s,'object':o} for i,(t,s,o) in enumerate(rels)],
             'affected_dimensions':dims,
             'affected_properties':[{'dimension':d,'target':t,'property':p} for d,t,p in effects],
             'paraphrases':[ko,en]}
    assert slot+'.'+ident not in existing_keys
    candidate_drafts.append({'proposal_id':'draft:'+slot+'.'+ident,
        'status':'new_candidate_proposal_requires_dedup_and_effect_mapping', 'slot':slot,
        'reference_numbers':[num],'candidate_entry_template':entry,
        'source_ids':by_num[num]['source_ids'],
        'required_core_bindings_ko':conditions,'dedup_review_ko':dedup,
        'effect_mapping_status':'All target/property paths are proposed. Existing coarse paths are conservative; new paths and core_existing_* relations require an explicit owner/lock audit before activation.',
        'render_gate_ko':by_num[num]['observability_gate_ko'],
        'forbidden_interpretation_promotions_ko':by_num[num]['confusion_boundaries_ko']})

ENRICH = [
 ('expression.ae_squinch',20,['lower eyelid margins sit raised toward the irises','both eyes remain visibly open','upper-lid closure is not the dominant source of narrowing'],
  [('visible_configuration','main_subject.lower_eyelids','main_subject.irises')],
  [('expression','main_subject','face.expression')], '현재 두 구성요소를 보존하며 lower/upper 경계를 보강. 움직였다/유지했다는 시간 주장은 추가하지 않는다.'),
 ('expression.pv_half_lidded',19,['eye apertures are reduced but remain open','upper and lower contributions remain unspecified unless independently visible'],
  [('visible_configuration','main_subject.eyelids','main_subject.eye_apertures')],
  [('expression','main_subject','face.expression')], '넓은 의미를 유지. 윗눈꺼풀 하위 변형을 범용 후보의 강제 정의로 덮어쓰지 않는다.'),
 ('expression.pv_asymmetric_mouth',32,['same actor lip corners differ in height or curvature','face pose is accounted for when reading asymmetry'],
  [('asymmetric_configuration','main_subject.left_lip_corner','main_subject.right_lip_corner')],
  [('expression','main_subject','face.expression')], 'Smirk 별칭을 단순 형태의 정확 동의어로 유지할지 검토. 평가 의미는 별도 문맥 후보에 남긴다.'),
 ('expression.playful_smirk',33,['a small requested lip-corner configuration remains visible','the playful or self-satisfied reading stays in requester context'],
  [('actor_owner','main_subject','main_subject.lip_corners')],
  [('expression','main_subject','face.expression')], '비대칭은 선택 대안으로 두고 내면 상태를 하드 증거로 만들지 않는다.'),
 ('expression.ae_lip_bite',38,['upper teeth visibly meet the same actor lower lip','the lower lip partly tucks beneath the tooth boundary'],
  [('contact','main_subject.upper_teeth','main_subject.lower_lip')],
  [('expression','main_subject','face.expression')], 'lip roll·lip press·tongue contact와 분리하며 행동 문맥을 보존한다.'),
 ('expression.ctx_c126',38,['the task-engaged actor retains the authored lower-lip bite form','gaze and hands remain attached to the frozen task'],
  [('actor_owner','main_subject','the authored task-concentration expression')],
  [('expression','main_subject','face.expression')], '원래 작업 집중 맥락/가드/행동을 보존. 유혹 후보로 전환하는 patch가 아니다.'),
 ('body_orientation.pv_shoulder_lower',52,['the specified shoulder girdle sits lower relative to the torso axis','the opposite shoulder and neck remain connected'],
  [('relative_height','main_subject.declared_shoulder','main_subject.torso_axis')],
  [('pose','main_subject','body.segment_orientation')], '옷의 dropped-shoulder seam 별칭을 신체 자세 exact cue로 섞지 않는다.'),
 ('hand_pose.tucking_hair_behind_ear',75,['the declared fingers meet the same actor hair near the same ear','hair strands continue toward the region behind that ear','the wrist and arm retain actor ownership'],
  [('contact','main_subject.declared_fingers','main_subject.hair_near_ear')],
  [('pose','main_subject','body.hand_configuration'),('pose','main_subject','body.contact_configuration')], '정지 상태에서는 현재 접촉만 주장. 고정된 헤어스타일의 변경 효과가 있으면 별도 appearance 잠금도 검사한다.'),
 ('hand_pose.reaching_toward_camera',82,['the declared actor arm extends toward the camera','the attached hand occupies a nearer depth plane than the torso','wrist elbow and shoulder remain continuous'],
  [('depth_nearer_than','main_subject.declared_hand','main_subject.torso'),('orientation_to','main_subject.declared_arm','camera')],
  [('pose','main_subject','body.hand_configuration'),('pose','main_subject','body.arm_configuration')], '기존 en 중심 레거시 항목에 단위/관계/효과를 추가. 실제 손 크기 변경은 제외한다.'),
 ('contact_point.pv_chin_support',74,['the actor chin visibly contacts the declared hand support surface','the hand forearm and torso form a readable support chain'],
  [('supports','main_subject.declared_hand','main_subject.chin')],
  [('pose','main_subject','body.contact_configuration'),('pose','main_subject','body.hand_configuration')], '기존 지지 의미는 유지하고 비접촉 hover·가벼운 접촉과 정확하게 분리한다.'),
 ('contact_point.pv_collarbone_touch',77,['fingers meet the same actor clavicle-region surface','existing garment coverage remains unchanged'],
  [('contact','main_subject.declared_fingers','main_subject.clavicle_region')],
  [('pose','main_subject','body.contact_configuration'),('pose','main_subject','body.hand_configuration')], '기존 relationship 효과를 삭제하는 안이 아님. 손/접촉 변경을 보수적으로 합산하고 원래 의복 조건 보존.'),
 ('contact_point.pv_lapel_grip',78,['the same actor fingers actually grip the existing garment lapel','cloth lies between the relevant fingers at the lapel edge'],
  [('grips','main_subject.declared_fingers','core_existing_garment.lapel')],
  [('pose','main_subject','body.contact_configuration'),('pose','main_subject','body.hand_configuration')], '집음은 유지. 단순 touch를 별칭으로 합치지 않는다. 의복 국소 변형이 있으면 appearance 효과 추가 검토.'),
 ('lighting.sff_pro_l01',115,['the key divides the same face into a lit side and a shadow side','the dividing boundary follows the face geometry'],
  [('illuminates','core_declared_key','main_subject.declared_face_side')],
  [('lighting','main_subject','face.illumination_pattern')], '현재 자료는 affected_properties가 없음. 광원/얼굴 owner와 잠금 경로를 먼저 확정한다.'),
 ('lighting.sff_pro_l05',116,['the off-axis nose shadow forms a small offset loop','a visible gap separates nose and cheek shadows'],
  [('separated_by_gap','main_subject.nose_shadow','main_subject.cheek_shadow')],
  [('lighting','main_subject','face.illumination_pattern')], '분리 간격을 보강하고 Rembrandt의 연결된 그림자와 구분한다.'),
 ('lighting.sff_pro_l07',117,['the face has unequal camera-projected sides due to head yaw','the camera-projected narrower face side receives the key','the broader side is relatively shadowed'],
  [('illuminates','core_declared_key','main_subject.camera_projected_narrow_face_side')],
  [('lighting','main_subject','face.illumination_pattern')], '항상 먼 볼이라는 축약을 좁은 투영 면 관계로 보강. 배우 좌우를 고정하지 않는다.'),
 ('lighting.sff_pro_l08',118,['the face has unequal camera-projected sides due to head yaw','the camera-projected broader face side receives the key','the narrower side is relatively shadowed'],
  [('illuminates','core_declared_key','main_subject.camera_projected_broad_face_side')],
  [('lighting','main_subject','face.illumination_pattern')], '넓게 비추는 관계와 실제 얼굴 폭 변경을 분리한다.'),
 ('light_shape.lit_clean_vertical_catchlight_pair',119,['two distinct source reflections form the already authored high-low pair','both reflections belong to the same specified corneal surface'],
  [('above','main_subject.upper_catchlight','main_subject.lower_catchlight')],
  [('lighting','main_subject','eyes.light_reflection')], '두 반사점이라는 좁은 기존 의미 유지. 모든 catchlight에 두 점을 강제하지 않는다.'),
 ('composition.pc_pc17_component_2',95,['the camera sees the main actor beyond a different actor foreground shoulder','the foreground shoulder retains secondary actor ownership'],
  [('beyond','main_subject.face','core_existing_secondary_actor.shoulder')],
  [('camera','camera','viewpoint'),('composition','scene','foreground_subject_relation')], '기존 camera/composition 차원을 보존하고 실제 camera/scene target mapping을 확인한다. 단독 자기어깨 포즈와 분리.'),
 ('expression.ae_sultry_variant',5,['the requester-selected current eye or lip configuration remains visible','the adult attraction context remains an independent prerequisite'],
  [('actor_owner','main_subject','the expressly selected current facial configuration')],
  [('expression','main_subject','face.expression'),('expression','main_subject','eyes.eyeline')], '기존 requires_all_tags=adult와 attraction 문맥 가드 보존. 날씨/졸림 음성례와 입 벌림 없는 대안 보강.'),
 ('expression.ae_coquettish_variant',3,['the chosen small smile or playful eye configuration remains visible','alternative forms are selected independently rather than jointly mandated'],
  [('actor_owner','main_subject','the selected playful facial configuration')],
  [('expression','main_subject','face.expression'),('expression','main_subject','eyes.eyeline')], '기존 성인 문맥 가드를 유지. 윙크/성별을 보편 정의에 추가하지 않는다.'),
 ('expression.ae_smolder_attraction',6,['the selected directed gaze and lip state remain visible','the attraction reading is anchored in the requester context'],
  [('directed_gaze','main_subject.eyes','core_declared_gaze_target')],
  [('expression','main_subject','face.expression'),('expression','main_subject','eyes.eyeline')], 'ae_smolder_anger와 형태/라벨 공유 때문에 분노 문맥이 침범하지 않도록 문맥 회귀 추가.'),
 ('expression.pv_parted_lips',34,['a visible opening separates upper and lower lip boundaries','jaw opening stays within the requested small gap','teeth and tongue visibility are independently specified'],
  [('separated_by_gap','main_subject.upper_lip','main_subject.lower_lip')],
  [('expression','main_subject','face.expression')], '현재 중립 형태를 보존하며 sexualized meaning·slack jaw 자동 전이를 배제.'),
]

# Reuse owner paths from authored source files. Store only relevant baseline fields.
owner_records = {}
for file in snapshot['files']:
    path = ROOT / file['path']
    if path.suffix != '.json': continue
    data = json.loads(path.read_text())
    for slot, slotdata in data.get('slots', {}).items():
        entries = slotdata if isinstance(slotdata,list) else slotdata.get('entries',[])
        for e in entries:
            if isinstance(e,dict) and 'id' in e:
                key = slot + '.' + e['id']
                owner_records.setdefault(key,[]).append((file['path'],e))

enrichments = []
for key,num,units,rels,effects,note in ENRICH:
    assert key in existing_keys and key in owner_records, key
    entries = owner_records[key]
    base = entries[-1][1]
    old_dims = base.get('affected_dimensions',[])
    old_props = base.get('affected_properties',[])
    proposed_props = list(old_props)
    for d,t,p in effects:
        e = {'dimension':d,'target':t,'property':p}
        if e not in proposed_props: proposed_props.append(e)
    proposed_dims = list(dict.fromkeys(old_dims + [e['dimension'] for e in proposed_props]))
    enrichments.append({'proposal_id':'enrich:'+key, 'candidate_key':key,
        'status':'existing_candidate_field_enrichment_proposal',
        'reference_numbers':[num], 'source_files':[x[0] for x in entries],
        'baseline_fields':{k:base.get(k) for k in ['concept_units','relations','affected_dimensions','affected_properties','requires_all_tags','requires_primary_any_tags','aliases']},
        'proposed_field_patch':{
            'concept_units':list(dict.fromkeys(base.get('concept_units',[]) + units)),
            'relations':base.get('relations',[]) + [{'id':f'se_r{i+1}','type':t,'subject':s,'object':o} for i,(t,s,o) in enumerate(rels)],
            'affected_dimensions':proposed_dims, 'affected_properties':proposed_props},
        'migration_note_ko':note,
        'source_ids':by_num[num]['source_ids'],
        'guard_policy':'Preserve executable guards and original context. Prose conditions are not executable guards. Do not broaden applicability to force retrieval.',
        'patch_policy':'Additive illustration only. Contradictory old units/aliases must be edited deliberately rather than blindly unioned; reviewed final fields must have one coherent meaning.',
        'effect_mapping_status':'Proposed targets/paths require actual core binding and lock inspection; parent paths remain conservative.'})

write('CANDIDATE-DRAFTS.json', {
    'schema_version':'seduction-candidate-research-drafts/v1','runtime_schema':False,
    'active_installation_performed':False,
    'new_candidate_proposal_count':len(candidate_drafts),'existing_candidate_enrichment_count':len(enrichments),
    'dedup_policy':'Prefer existing IDs and owner files. New records below are proposals, not proof that no semantically equivalent record exists.',
    'positive_retrieval_text_policy':'Only visible definitions, units and narrow positive paraphrases enter future embeddings. Research provenance, claim limits and negative examples stay in evidence or appropriate exclusion fields.',
    'new_candidate_proposals':candidate_drafts, 'existing_candidate_enrichments':enrichments})

profile_drafts = []
for draft in candidate_drafts[:12]:
    entry = draft['candidate_entry_template']; num=draft['reference_numbers'][0]
    ident='se_profile_' + entry['id'][3:]
    assert ident not in existing_profiles
    groups_ = [{'id':f'c{i+1}','any_terms':[u]} for i,u in enumerate(entry['concept_units'])]
    comps = [{'id':g['id'],'match_terms':g['any_terms'], 'evidence_field':g['id']+'_phrase',
              'evidence_terms':g['any_terms'],'min_content_words':3,
              'instruction':'Keep this current visible relation on the frozen actor: '+g['any_terms'][0],
              'render_gate':{'id':'vo_'+ident+'_'+g['id'],'review_scale':'native',
                             'description':g['any_terms'][0]}} for g in groups_]
    profile = {'id':ident,'category':'observable_portrait_configuration',
        'activation':{'exact_terms':[entry['ko'],entry['en']], 'requires_adult_character':False,
            'semantic_discovery_requires_component_evidence':True},
        'semantics':{'definition':entry['en'], 'paraphrase_examples':entry['paraphrases'],
            'visual_components':entry['concept_units'],
            'component_semantics':{'minimum_component_groups':len(groups_),
                'required_group_ids':[g['id'] for g in groups_], 'groups':groups_},
            'contrast_examples':by_num[num]['confusion_boundaries_ko'],
            'claim_limits':['Visible geometry on the frozen actor only; no inferred emotion, consent, health or relationship history.',
                'Retain frozen crop, existing entities and exclusions; hidden required evidence is UNOBSERVABLE.',
                'Every independently requested component must pass; partial_is_fail.']},
        'concept_candidate':{'concept_terms':entry['paraphrases']+entry['concept_units']},
        'runtime_expression':{'default_mode':'definition_with_optional_label','prompt_label_terms':[],
            'forbidden_prompt_terms':[],'runtime_forbidden_labels':[]},
        'reject_substitutes':by_num[num]['confusion_boundaries_ko'],
        'authored_components':{'contract_version':'photo-authored-visual-components/v1','components':comps}}
    profile_drafts.append({'proposal_id':'draft:'+ident, 'status':'narrow_profile_template_requires_context_and_owner_review',
        'reference_numbers':[num], 'candidate_key':draft['slot']+'.'+entry['id'],
        'profile_template':profile, 'source_ids':draft['source_ids'],
        'required_context_before_activation_ko':draft['required_core_bindings_ko'],
        'install_blocker':'Core entity/owner checks and target-property mapping must be implemented with already supported contracts before this template can activate; exact text alone does not create missing entities.'})

PROFILE_ENRICH = [
 ('ae_profile_squinch',20,'아랫눈꺼풀 중심과 윗눈꺼풀 닫힘의 구분을 추가하고 단일 사진에서는 실제 이동/유지 시간을 요구하지 않음'),
 ('contrapposto_weight_shift',45,'지지 발/자유 다리·골반/어깨 대응과 전신 관찰 유지;S 윤곽 대체를 PASS로 보지 않음'),
 ('pv_profile_chin_support',74,'접촉·하중 지지와 hover/light touch의 차이를 독립 증거로 검사'),
 ('pv_profile_reverse_chair',68,'등받이 방향과 좌면 지지를 보존하며 straddle 다리 배치를 자동 요구하지 않음'),
 ('pv_profile_chair_straddle',68,'다리의 등받이/좌면 양옆 배열과 골반 지지를 검사하며 reverse orientation과 구분'),
 ('pc_pc17_owner_relation',95,'전경 shoulder는 secondary actor 소유;주인공 자기 어깨 포즈와 좌표/초점 경계 보강'),
 ('rembrandt_face_light_pattern',113,'triangle의 shadow-side와 camera-near/far 구분을 유지;가려진 코-볼 연결은 미관찰'),
 ('butterfly_face_light_pattern',114,'중앙 코밑 그림자와 loop/clamshell 구분;나비 장신구가 프로필을 활성화하지 않게 검사'),
 ('split_face_light_pattern',115,'반쪽 명암 경계와 makeup/occlusion 구분;short/broad는 별도 좌표 축'),
 ('loop_face_light_pattern',116,'코/볼 그림자의 분리 간격을 원본 얼굴에서 검사;삼각광 대체는 실패'),
 ('short_face_light_orientation_relation',117,'카메라 투영 폭으로 좁은 면을 정의하고 얼굴 회전/좌우 반전 교차 검사'),
 ('broad_face_light_orientation_relation',118,'카메라 투영 폭으로 넓은 면을 정의;실제 얼굴 폭 변경 금지'),
 ('controlled_languid_movement_display',10,'선택된 미완료 동작/지지를 보존하고 느린 속도/지속 전체는 시간 증거 없으면 미검증'),
 ('sv_tongue_lip_boundary',35,'혀의 구강 연속성·같은 입술 접점을 보강;lip-lick 이동 완료는 단일 사진으로 PASS 불가'),
]
profile_enrich = []
for ident,num,note in PROFILE_ENRICH:
    assert ident in existing_profiles,ident
    profile_enrich.append({'profile_id':ident,'reference_numbers':[num],
        'proposal_ko':note,'source_ids':by_num[num]['source_ids'],
        'preservation_policy':'Preserve stable ID, existing supported definition, exclusions and authored components; change only reviewed missing distinctions.'})
write('PROFILE-DRAFTS.json', {'schema_version':'seduction-profile-research-drafts/v1','runtime_schema':False,
    'relation_contract_version':'photo-visual-relation/v1',
    'new_narrow_profile_proposal_count':len(profile_drafts),'existing_profile_enrichment_count':len(profile_enrich),
    'new_profile_proposals':profile_drafts,'existing_profile_enrichments':profile_enrich,
    'broad_label_rule':'No new exact hard profile for seductive, coquettish, sultry, smoldering, bedroom eyes, provocative, commanding, femme fatale or smirk.',
    'static_time_rule':'No exact hard promotion of the whole temporal term from one current state.'})

bundles_raw = [
 ('se_option_lash_gaze_lapel',[18,31,78],['gaze_engagement.se_lash_occluded_upward_gaze','expression.pv_smile_closed','contact_point.se_lapel_fingertip_touch'], '턱/눈 반대 방향·작은 닫힌 미소·기존 라펠 접촉을 각각 선택할 수 있는 초상 대안'),
 ('se_option_small_asymmetry',[16,32,109],['gaze_engagement.pv_side_eye','expression.pv_asymmetric_mouth','lighting.lit_window_large_soft_source'],'옆 시선·비대칭 입·부드러운 광원을 독립 선택하는 대안'),
 ('se_option_squinch_reflection',[20,119],['expression.ae_squinch','light_shape.se_cornea_catchlight_without_wetness'],'스퀸치의 열린 눈과 작은 눈 표면 반사를 함께 읽을 수 있는 대안'),
 ('se_option_seated_support',[55,58,69],['contact_point.pv_seated_palm_brace','body_pose.perched_edge_sit_grounded_support','hand_pose.pv_relaxed_fingers'],'좌면 가장자리·뒤쪽 손 지지·다른 손 이완을 선택할 수 있는 대안'),
 ('se_option_chin_hover',[31,74,83],['expression.pv_smile_closed','hand_pose.se_hand_hover_below_chin','shot_scale.close_up_face_shot'],'턱 아래 비접촉 손과 작은 닫힌 미소를 보여주는 얼굴 크롭 대안'),
 ('se_option_one_hand_head',[15,44,76],['gaze_engagement.pv_gaze_direct','body_orientation.axial_elongation_relaxed_shoulders','hand_pose.se_one_hand_behind_head'],'한 손만 뒤통수에 두고 목 축/직접 시선을 별도로 선택하는 대안'),
 ('se_option_own_shoulder',[50,85,113],['body_orientation.looking_back_over_shoulder_orientation','shot_scale.medium_close_chest_up_shot','lighting.lit_rembrandt_cheek_triangle_key'],'자기 어깨 너머 돌아봄과 그림자 쪽 삼각광을 선택할 수 있는 대안'),
 ('se_option_existing_partner_ots',[95,96,105],['partner_framing.pc_pc17_component_1','composition.pc_pc17_component_2','focus.pc_pc17_component_4'],'이미 존재하는 상대 어깨 전경과 주체 얼굴 초점의 대안'),
 ('se_option_short_loop',[83,116,117],['shot_scale.close_up_face_shot','lighting.sff_pro_l05','lighting.sff_pro_l07'],'좁은 투영 얼굴 면에 loop 패턴을 선택하는 대안'),
 ('se_option_existing_pendant',[31,80,109],['expression.pv_smile_closed','contact_point.se_existing_pendant_fingertip_hold','lighting.lit_window_large_soft_source'],'기존 펜던트 본체 접점·닫힌 미소·부드러운 빛을 선택할 수 있는 대안'),
]
newkeys={r['slot']+'.'+r['candidate_entry_template']['id'] for r in candidate_drafts}
bundle_drafts=[]
for ident,nums,keys,proposition in bundles_raw:
    assert all(k in existing_keys | newkeys for k in keys),keys
    entry={'id':ident,'candidate_only':True,'primary_visual_proposition':proposition,
        'candidate_ids':[k.split('.',1)[1] for k in keys],
        'candidate_slots':{k.split('.',1)[1]:k.split('.',1)[0] for k in keys},
        'hard_profile_ids':[],
        'component_groups':[{'id':f'option_{i+1}','visible_evidence':[by_num[n]['observables_or_optional_examples_ko'][0]]} for i,n in enumerate(nums)],
        'source_keywords':[by_num[n]['term'] for n in nums],
        'confusion_boundaries':['Broad mood wording does not require this complete combination.','Only independently supported or explicitly adopted components may affect the core.','Missing entities and locked dimensions cannot be added through a bundle.'],
        'relations':[{'id':'owner_scope','type':'declared_owner_scope','subject':'core_frozen_entities','object':'only the explicitly selected component relations'}]}
    bundle_drafts.append({'proposal_id':'draft:bundle:'+ident,'reference_numbers':nums,'candidate_keys':keys,
        'bundle_entry_template':entry,'source_ids':sorted(set(s for n in nums for s in by_num[n]['source_ids'])),
        'adoption_policy':'Optional shortlist only. Compile using existing candidate_only behavior and independent_request_evidence_only profile activation; never turn seductive into every component here.',
        'compatibility_review':'All selected components need a shared actor/target, valid effects and readable framing. Variants may remain separate options rather than be adopted together.'})
write('BUNDLE-DRAFTS.json', {'schema_version':'seduction-optional-bundle-research/v1','runtime_schema':False,
    'bundle_count':len(bundle_drafts),'bundles':bundle_drafts})

# 120 coverage probes are a review matrix, not 120 executed tests.
coverage=[]
for r in rows:
    coverage.append({'id':f'T{r["number"]:03d}','reference_number':r['number'],
        'positive_request_ko':f'요청된 인물/장면의 {r["term"]}를 표현한다. {r["observables_or_optional_examples_ko"][0]}.',
        'negative_or_counterexample_ko':r['confusion_boundaries_ko'][0],
        'expected_semantics_type':r['semantics_type'],
        'review_assertions':['요청 전체·부정·사용자 정의로 의미를 먼저 결정','existing/new proposal IDs로 기대 의미를 지정;배열 순서/점수는 판정 근거 아님',r['observability_gate_ko']],
        'status':'proposed_coverage_probe_not_an_executed_test'})

special_raw = [
 ('B01','소프트한 초상, sultry한 여름 공기. 인물 표정은 중립 고정.','날씨 sultry에서 성인 유혹 표정 프로필/후보를 강제하지 않음',[5]),
 ('B02','숯불이 smoldering하고, 인물은 미소 없이 책을 읽는다.','물체 연소와 인물 smolder-attraction 분리',[6]),
 ('B03','분노를 억누르는 smoldering look. 끌림이나 플러팅은 없다.','ae_smolder_anger 유지;끌림 후보 제외',[6]),
 ('B04','정치적으로 provocative한 광고 포스터의 인물은 정장 차림이다.','의복/노출/성적 행동을 추가하지 않음',[11]),
 ('B05','commanding한 지휘자. 카메라 높이와 턱은 그대로 유지.','권위 라벨로 low angle/chin lift를 강제하지 않음',[12]),
 ('B06','침대가 없는 사무실 초상. bedroom eyes는 반쯤 열린 눈의 인상으로만.','장소/잠옷/졸림을 추가하지 않음',[14]),
 ('B07','왼쪽 입꼬리가 조금 높은 비대칭 미소. 비웃거나 우쭐한 태도는 아니다.','pv_asymmetric_mouth 형태 유지;smirk 평가 강제 금지',[32,33]),
 ('B08','작업에 집중하며 아랫입술을 살짝 문다. 플러팅은 없다.','ctx_c126 문맥/행동 보존',[38]),
 ('B09','아랫눈꺼풀이 조금 올라간 열린 눈. 윗눈꺼풀 강한 닫힘 없음.','squinch와 upper-lid variant의 후보/프로필 구분',[19,20]),
 ('B10','윗눈꺼풀이 내려온 열린 눈. 아랫눈꺼풀 상승은 없다.','upper-lid variant 유지;squinch 강제 제외',[19,20]),
 ('B11','턱을 낮추고 카메라보다 위 목표를 본다. 카메라는 눈높이 고정.','chin down와 eye up을 분리;high-angle 추가 금지',[18,41,89]),
 ('B12','턱은 정면 그대로, 눈만 아래 책을 본다.','downcast와 chin tuck 독립',[17,41]),
 ('B13','한쪽 눈만 윙크하고 다른 눈은 열려 있다. 오른눈은 머리카락에 완전히 가려짐.','두눈 조건이 가려지면 UNOBSERVABLE;임의 PASS 금지',[22,30]),
 ('B14','드롭 숄더 티셔츠를 입되 양쪽 어깨는 수평 자세다.','의복 봉제선에서 pv_shoulder_lower 활성화 금지',[52]),
 ('B15','왼쪽 어깨만 낮춘 인물. 옷 봉제선은 일반 어깨선.','몸 자세를 의복 oversized로 바꾸지 않음',[52]),
 ('B16','인물 한 명이 자기 오른어깨 너머 렌즈를 돌아본다.','secondary shoulder/두번째 인물/OTS 카메라 추가 금지',[50,95]),
 ('B17','기존 두 인물 중 A의 어깨 전경 너머 B의 얼굴을 본다.','어깨 A와 얼굴 B 소유를 유지;자기어깨 포즈로 대체 금지',[50,95]),
 ('B18','무릎 위 three-quarter shot, 몸은 정면 그대로.','MFS crop와 3/4 body yaw 분리',[48,87]),
 ('B19','몸은 three-quarter turn, 머리부터 발끝까지 보인다.','방위각과 full-shot coverage 유지',[48,88]),
 ('B20','발이 프레임 밖인 CU에서 contrapposto의 체중 지지까지 확인하라.','crop 충돌을 기록;발 지지 전체 PASS 금지;임의 full shot 변경 금지',[45,83]),
 ('B21','턱 아래 손을 2cm 띄워 놓되 받치지 않는다.','hover 후보;chin-support 프로필 활성화 금지',[74]),
 ('B22','턱을 손에 실제로 받치고, 전완은 테이블에 놓는다.','actual chin/hand/forearm support chain;hover로 대체 금지',[74]),
 ('B23','오른손만 뒤통수, 왼손은 주머니 고정.','one-hand variant 유지;양손형으로 왼손 변경 금지',[76]),
 ('B24','라펠에 손끝만 댄다. 집거나 옷을 당기지 않는다.','touch/grip 구분;피복 유지',[78,79]),
 ('B25','손끝으로 기존 펜던트 본체를 잡는다. 새 액세서리는 없다.','기존 체인/장식/손 소유;없으면 결손 문맥 기록',[80]),
 ('B26','손은 카메라 쪽으로 뻗지만 손 크기와 원래 손가락 수는 고정.','foreshortening vs morphology lock 분리',[82]),
 ('B27','카메라는 수평. 머리만 왼쪽으로 기울이고 다리는 대각으로 뻗는다.','head roll/leg diagonal로 Dutch 활성화 금지',[40,66,93]),
 ('B28','손이 보이지 않는 관찰자 POV. 새 전경 손을 넣지 않는다.','POV 손전경 하위형을 보편화하지 않음',[94]),
 ('B29','같은 인물과 거울 속 반사를 유지하며 반사 속 눈만 목표를 본다.','mirror owner·반사 좌표와 direct gaze 구분',[15,103]),
 ('B30','앞 사람 어깨는 흐리고 뒷 사람 얼굴은 선명한 OTS. 앞 어깨 접촉 미세 형태는 요구 안 함.','target focus 합법;흐린 앞 어깨에 다른 필수 접점 추가 금지',[95,105]),
 ('B31','loop lighting이며 코 그림자와 볼 그림자 사이에 간격이 남는다.','Rembrandt triangle로 대체하지 않음',[113,116]),
 ('B32','같은 loop 광원에서 머리 yaw를 반대로 바꾸고 short/broad를 비교한다.','카메라 투영 좁은/넓은 면을 재바인딩;고정 배우 좌우 금지',[116,117,118]),
 ('B33','나비 모양 헤어핀을 단 정면 초상. 조명은 평평한 창광.','butterfly hair clip에서 butterfly lighting 활성화 금지',[114]),
 ('B34','눈 표면 작은 캐치라이트 한 점. 젖음·눈물·두 점 반사는 제외.','순수 반사점 유지;복합 wet-eye/vertical-pair 강제 금지',[119]),
 ('B35','사용자 정의: 이 요청에서 sultry는 덥고 습한 공기, 인물 표정은 열린 밝은 미소.','사용자 정의 우선;사전/기존 후보로 표정 덮어쓰기 금지',[5]),
 ('B36','작은 닫힌 미소를 유지하고 눈 시선만 변경 가능. 다른 표정·포즈는 고정.','broad face.expression 효과가 잠금과 충돌하면 거절;세분 매핑 없이 예외 허용 금지',[15,31]),
]
special=[{'id':ident,'request_ko':req,'expected_result_ko':exp,'reference_numbers':nums,
          'status':'proposed_contract_regression_not_executed'} for ident,req,exp,nums in special_raw]
for n in sorted(temporal):
    special.append({'id':f'TIME-{n:03d}', 'request_ko':f'단일 사진으로 {by_num[n]["term"]}의 전체 시간 의미를 보여준다.',
        'expected_result_ko':by_num[n]['observability_gate_ko']+';현재 상태와 전체 시간 의미의 판정을 분리',
        'reference_numbers':[n],'status':'proposed_temporal_boundary_regression_not_executed'})
write('REGRESSION-PLAN.json', {'schema_version':'seduction-regression-plan/v1','runtime_schema':False,
    'coverage_probe_count':len(coverage),'cross_boundary_case_count':len(special),
    'executed_test_count':0,'coverage_probes':coverage,'cross_boundary_cases':special,
    'holdout_policy':'전 문장을 인덱스/alias에 넣지 않는다. 의미 보강 후 처음 쓰는 한/영 패러프레이즈를 추가해 과적합을 검사한다.',
    'pack_policy':'현재 64개 후보 상한을 유지. 노출/채택은 stable candidate key와 profile ID로 검사;관련 단어 점수로 성공을 대체하지 않는다.'})

pixel_raw = [
 ('V01',[19,20,31,83],'정체성 참조 없는 성인 CU, 작은 닫힌 미소 고정. 스퀸치와 윗눈꺼풀 중심 변형을 비교.', ['아랫눈꺼풀 중심/윗눈꺼풀 중심 구분','열린 양눈','입꼬리 잠금 보존']),
 ('V02',[71,73,74,85],'성인 MCU에서 턱 아래 비접촉 손 또는 손끝 볼 접촉을 독립 장면으로 선택. 손날이 읽힌다.', ['같은 손-전완 소유','선택된 gap 또는 fingertip-cheek contact','손의 카메라 상대 평면']),
 ('V03',[15,44,76,85],'성인 MCU, 오른손만 뒤통수에 두고 왼손은 허리에 고정. 직접 시선과 목 축.', ['오른손-팔꿈치-뒤통수 관계','왼손 잠금','목-머리-어깨 연속성']),
 ('V04',[78,79,80,85],'이미 라펠·펜던트가 있는 옷차림. 라펠 touch/원단 pinch/펜던트 hold를 분리된 하위 장면으로 검사.', ['이미 존재하는 의복/장신구','선택 손끝-목표 접점','옷감/체인 연결·피복 보존']),
 ('V05',[45,46,64,67,88],'성인 전신, 콘트라포스토 지지와 발목/발끝 변형 중 요청된 하나만 선택. 얼굴 미세 조건은 별도.', ['지지 발/자유 다리와 하중 경로','골반/어깨 균형','선택 발목/발끝 소유']),
 ('V06',[50,95,105],'이미 존재하는 두 성인 OTS와 한 성인 자기어깨 돌아보기는 별도 장면. 초점은 주체 얼굴.', ['자기/상대 어깨 소유 구분','프레임 인물수 보존','시선/초점 대상']),
 ('V07',[113,116,117,118],'성인 얼굴 CU, loop/Rembrandt와 short/broad를 분리 요인으로 비교. 얼굴 yaw/광원 방향을 기록.', ['코-볼 그림자의 gap/join','요청 시 그림자쪽 삼각광','카메라 투영 면폭과 조명면 관계']),
 ('V08',[109,111,119,120],'성인 초상, 작은 반사점·국소 광역·눈 가독성을 확인. 젖은 눈과 발광 홍채는 제외.', ['각막 국소 반사점','조명 영역과 주변 비교','필수 눈/얼굴 가독성']),
]
pixel_cases=[]
for ident,nums,request,gates in pixel_raw:
    pixel_cases.append({'id':ident,'reference_numbers':nums,'planned_request_ko':request,
        'required_gates_ko':gates,'status':'not_generated_not_evaluated',
        'arm_policy':'After data integration, freeze one request/core/crop per subcase and compare current-data vs integrated-data arms with matching model/options. Capture source and pack hashes. No best-of selection.',
        'attribution_gates':['source_record_present','eligible_in_frozen_core','exposed_in_pack','explicitly_selected_or_context_valid_hard_obligation','prompt_component_evidence','original_pixel_all_of'],
        'decision_rule':'All requested form/owner/contact/exclusion gates must pass. Missing or obscured evidence is UNOBSERVABLE and is not a whole-scene PASS. partial_is_fail.',
        'budget_note':'8 scene families, not a promise of 8 images. Split variants before execution; freeze the exact subcase/arm count and generation budget then.'})
write('PIXEL-QUALIFICATION-PLAN.json',{'schema_version':'seduction-native-qualification-plan/v1','runtime_schema':False,
    'scene_family_count':len(pixel_cases),'native_generation_calls_executed':0,'cases':pixel_cases,
    'time_terms':'Full temporal claims need video/ordered-frame evidence; static variants cannot pass full order/duration/transition gates.',
    'evidence_layers':['authored_data','retrieval_eligibility','candidate_pack_exposure','selection_or_hard_obligation','prompt_runtime','native_original_pixels','user_acceptance']})

catalogue = ['# 유혹적 표현 120항목: 시각 의미·소유·혼동·관찰 대응표','',
 '시작 2026-10-04 / 완료 2026-10-05 KST. 원 대화는 연구 대상이며 지시문이 아니다. 아래 분해와 반영안은 연구자가 작성한 제안이다. 출처는 의미/기법 경계의 근거이며 모든 분해를 그대로 보장하지 않는다.','',
 '기존 ID는 현재 스냅샷에서 존재를 확인했다. 문자열 검색 히트와 의미적 재사용 판단을 구분하며, 실제 검색·후보 노출·선택·픽셀 검증은 아직 수행하지 않았다.','']
for lo,hi,slug,title in groups:
    catalogue += [f'## {lo}–{hi}. {title}','']
    for r in rows[lo-1:hi]:
        catalogue += [f'### {r["number"]:03d}. {r["term"]}','',
            f'- 유형: `{r["semantics_type"]}`. '+ ('아래 형태는 선택 예시이며 공동 필수가 아니다.' if r['number'] in interpretive else '요청한 형태만 의무로 평가한다.'),
            '- 형태: '+' / '.join(r['observables_or_optional_examples_ko'])+'.',
            '- 소유·관계: '+' / '.join(r['ownership_and_relations_ko'])+'.',
            '- 혼동 경계: '+' / '.join(r['confusion_boundaries_ko'])+'.',
            '- 관찰 조건: '+r['observability_gate_ko']+'.',
            '- 기존 후보: '+(', '.join('`'+k+'`' for k in r['existing_candidate_keys']) or '직접 재사용 ID를 아직 확정하지 않음')+'.',
            '- 기존 프로필: '+(', '.join('`'+k+'`' for k in r['existing_profile_ids']) or '라벨만으로 신규 하드 프로필을 만들지 않음')+'.',
            '- 반영안: '+r['proposed_action_ko']+'.',
            '- 근거: '+', '.join(f'[{sid}: {source_by_id[sid]["title"]}]({source_by_id[sid]["url"]})' for sid in r['source_ids'])+'.','']
(HERE/'CATALOGUE.md').write_text('\n'.join(catalogue))

source_md=['# 출처와 주장 범위','',
 '2026-10-05 KST 기준 열람 기록. 출처의 어휘/기법 정의와 이 패키지의 관찰 단위·데이터 설계 제안을 분리한다. 실사 이미지 품질이나 사용자 수용을 입증하는 출처 목록이 아니다. 직접 인용은 사용하지 않았다.','',
 '| ID | 근거 | 지지하는 주장 | 한계/열람 방식 |','|---|---|---|---|']
for s in sources:
    source_md.append(f'| {s["id"]} | [{s["title"]}]({s["url"]}) | {s["supported_claim"]} | {s["limitations"]} / `{s["access_method"]}` |')
(HERE/'SOURCES.md').write_text('\n'.join(source_md)+'\n')

summary={
    'reference_terms':120,'sources':len(sources),'interpretive_terms':len(interpretive),
    'explicit_temporal_terms':len(temporal),
    'inventory_candidate_count':snapshot['loaded_candidate_count'],'inventory_profile_count':snapshot['loaded_profile_count'],
    'literal_or_substring_probe_hit_count':sum(r['current_inventory_probe']['has_literal_or_substring_inventory_hit'] for r in rows),
    'unique_reuse_candidate_keys':len({k for r in rows for k in r['existing_candidate_keys']}),
    'unique_reuse_profile_ids':len({k for r in rows for k in r['existing_profile_ids']}),
    'new_candidate_proposals':len(candidate_drafts),'existing_candidate_enrichment_proposals':len(enrichments),
    'new_narrow_profile_proposals':len(profile_drafts),'existing_profile_enrichment_proposals':len(profile_enrich),
    'optional_bundle_proposals':len(bundle_drafts),'coverage_probes':len(coverage),'cross_boundary_proposed_cases':len(special),
    'native_scene_families':len(pixel_cases),'active_asset_edits':0,'runtime_tests_executed':0,'native_generations_executed':0,
}
write('PACKAGE-SUMMARY.json',summary)
print(json.dumps(summary,ensure_ascii=False))
