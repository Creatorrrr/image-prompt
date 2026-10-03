"""Reviewed, idempotent authored-data changes; no generated index is edited here."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
from visual_profile_contracts import compile_visual_profile


def unique(rows):
    return list(dict.fromkeys(rows))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def effect(dimension, prop):
    return [{'dimension': dimension, 'target': 'main_subject', 'property': prop}]


# New entries describe narrowly specified observable relations. Their names are
# technical names, not automatic aliases for the broader original slang.
# Each component tuple is (English observation, equivalent English, Korean).
UNITS = [
    ('sv_upward_pupils', 'SV01', 'expression', 'expression', 'face.expression',
     '같은 인물의 양쪽 눈 안에서 위로 놓인 동공', 'upward pupils within both eye apertures',
     [
      ('both pupils sit toward the upper part of their eye apertures', 'both pupils sit high inside the eye openings', '양쪽 눈동자가 각 눈의 개안부 위쪽에 놓인다'),
      ('lower sclera is visible beneath both pupils', 'visible white sclera below each raised pupil', '올라간 양쪽 동공 아래로 흰자위가 보인다'),
      ('both eyes belong to the same actor', 'the same face owns both visible eyes', '두 눈이 같은 인물의 얼굴에 연결된다')],
     ['head tilt with centered pupils', 'one obscured eye', 'upward-facing head alone']),
    ('sv_inward_pupils', 'SV02', 'expression', 'expression', 'face.expression',
     '양쪽 눈동자가 각 눈의 코 쪽으로 모인 현재 배치', 'bilateral nasal-side pupil placement',
     [
      ('each pupil sits toward the nasal side of its own eye aperture', 'both pupils move toward their respective inner eye corners', '각 동공이 자기 눈의 코 쪽 가장자리에 가깝다'),
      ('both eye apertures and their inner corners remain visible', 'two readable eye openings retain their nasal corner landmarks', '양쪽 개안부와 안쪽 눈구석이 함께 보인다'),
      ('both eyes belong to the same actor', 'the same face owns both visible eyes', '두 눈이 같은 인물의 얼굴에 연결된다')],
     ['ordinary side gaze of both eyes', 'diagnosis from pupil placement', 'one eye duplicated']),
    ('sv_left_right_pupil_relation', 'SV03', 'expression', 'expression', 'face.expression',
     '명시한 좌우 동공 위치 차이', 'explicit actor-relative left-right pupil difference',
     [
      ('the actor-left pupil has its explicitly chosen position within its eye aperture', 'the left eye retains its stated pupil position', '인물 기준 왼쪽 동공이 지정한 눈 안 위치에 놓인다'),
      ('the actor-right pupil has its separately chosen position within its eye aperture', 'the right eye retains its separately stated pupil position', '인물 기준 오른쪽 동공이 별도로 지정한 눈 안 위치에 놓인다'),
      ('both visible pupil positions belong to one face in the same frame', 'one actor shows both specified eye positions simultaneously', '한 얼굴의 두 동공 배치가 같은 화면에 함께 보인다')],
     ['random asymmetry without specified laterality', 'head perspective mistaken for eye position', 'two different actors']),
    ('sv_tongue_lip_boundary', 'SV08', 'expression', 'expression', 'face.expression',
     '같은 입의 혀가 명시한 위치에서 입술 경계를 넘은 형태', 'tongue crossing the lip boundary of the same mouth',
     [
      ('the tongue visibly crosses the outer lip boundary', 'tongue projects beyond the lip edge', '혀가 입술의 바깥 경계를 넘어 보인다'),
      ('the visible tongue remains connected to the same actor mouth', 'one tongue continues out of its own mouth', '보이는 혀가 같은 인물의 입 안에서 이어진다'),
      ('tongue position and protrusion extent follow the explicitly chosen variant', 'the selected tongue placement and visible extent remain readable', '혀의 위치와 밖으로 나온 길이가 명시한 변형을 따른다')],
     ['tongue wholly inside the mouth', 'detached tongue prop', 'automatic small centered tongue variant']),
    ('sv_local_cheek_redness', 'SV09', 'skin_condition', 'appearance', 'face',
     '지정한 볼 피부의 국소 붉은 색', 'localized reddish cheek-surface color',
     [
      ('a reddish patch occupies the specified cheek skin', 'local red color is visible on the chosen cheek surface', '지정한 볼 피부에 국소적인 붉은 색이 보인다'),
      ('the color follows the same actor cheek surface', 'the reddish area remains on its own facial skin', '붉은 영역이 같은 인물의 볼 피부 면을 따른다')],
     ['red lighting over the entire frame', 'illness or emotion inferred from color', 'unrequested makeup cause']),
    ('sv_pupil_heart_motif', 'SV12', 'eye_detail', 'appearance', 'face',
     '지정한 매체 위에서 동공 영역 안에 놓인 하트 문양', 'pupil-contained heart motif on an explicitly chosen carrier',
     [
      ('the chosen heart motif remains within the specified pupil region', 'a small heart is contained inside each requested pupil area', '하트 문양이 지정한 동공 영역 안에 놓인다'),
      ('the visible eye contours continue around the pupil motif', 'natural eye outlines and iris boundaries surround the small heart', '하트 주변으로 눈 윤곽과 홍채 경계가 이어진다'),
      ('the motif carrier is explicitly selected for the same actor eyes', 'the declared contact lens or other stated carrier places the motif on those eyes', '같은 인물의 눈 문양을 담는 렌즈 등 매체가 별도로 지정된다')],
     ['heart replacing the whole eye', 'heart-shaped catchlight substituted for a lens motif', 'unrequested contact lenses or medium change']),
    ('sv_seated_knees_apart', 'SV15', 'body_pose', 'pose', 'body.support_and_configuration',
     '좌면에 골반을 지지하고 무릎을 떨어뜨린 앉은 자세', 'seated separated knees with visible pelvis support',
     [
      ('the pelvis rests on the specified seat surface', 'the chosen sitting surface supports the pelvis', '골반이 지정한 좌면에 닿아 지지된다'),
      ('the two bent knees remain laterally separated', 'both flexed knees are apart in the seated pose', '앉은 자세에서 굽힌 양 무릎이 좌우로 떨어져 있다'),
      ('each leg connects to the same pelvis and keeps its chosen foot support', 'both connected legs retain separately stated foot contacts', '두 다리가 같은 골반에서 이어지고 지정한 발 지지를 유지한다')],
     ['standing feet apart', 'chair straddle without requested chair relation', 'disconnected knee or foot']),
    ('sv_supported_m_legs', 'SV17', 'body_pose', 'pose', 'body.support_and_configuration',
     '골반과 발 지지가 보이는 정면 앉은 M형 굽힌 양다리', 'front-view seated M-shaped bent legs with pelvis and foot support',
     [
      ('the seated pelvis rests below two raised separated bent knees', 'the low supported pelvis lies between higher flexed knees', '지지된 낮은 골반 양옆으로 굽힌 두 무릎이 높게 떨어져 있다'),
      ('each thigh continues through its own knee into its own shin and foot', 'both connected upper and lower leg segments remain individually traceable', '각 허벅지가 자기 무릎과 정강이와 발로 이어진다'),
      ('the pelvis and both feet retain their specified support contacts', 'the sitting surface and separate foot contacts remain readable', '좌면의 골반 지지와 양발의 개별 지지가 함께 보인다'),
      ('the already selected frontal view shows the connected leg contours as an M', 'the stated front view makes the two bent-leg outlines read as an M-like shape', '이미 선택한 정면 시점에서 연결된 다리 윤곽이 M형으로 읽힌다')],
     ['standing wide stance', 'letter M prop', 'knees cropped away', 'changed camera view to force the silhouette']),
    ('sv_supine_limb_spread', 'SV18', 'body_pose', 'pose', 'body.support_and_configuration',
     '등이 지지된 같은 인물의 양팔과 양다리 벌림', 'four-limb spread on a specified supine support',
     [
      ('the back of the same actor torso contacts the chosen support', 'the reclining actor retains posterior torso support', '같은 인물의 등 쪽 몸통이 지정한 지지 면에 닿는다'),
      ('both connected arms extend apart from that torso', 'the two actor-owned arms separate across the support', '그 몸통에 연결된 두 팔이 서로 벌어진다'),
      ('both connected legs extend apart from that pelvis', 'the two actor-owned legs separate across the support', '같은 골반에서 이어진 두 다리가 서로 벌어진다')],
     ['one arm and one leg only', 'arms belonging to a second actor', 'standing stance substituted for supine support']),
    ('sv_padded_garment_contour', 'SV24', 'garment_detail', 'appearance', 'body.garment',
     '명시된 의복 패딩이 만드는 바깥 윤곽', 'outer contour contributed by the declared garment padding',
     [
      ('the specified padding belongs inside the already chosen garment', 'the declared garment contains the requested padding', '패딩이 이미 선택한 의복의 지정된 안쪽 부분에 속한다'),
      ('the garment outer contour reflects that specified padding', 'the padded clothing shell has the selected exterior contour', '의복의 바깥 윤곽에 지정한 패딩 형태가 드러난다'),
      ('the actor anatomical proportions remain separately specified', 'the padded garment contour is separate from bodily volume', '패딩 의복 외곽과 인물의 신체 양감이 별도로 구분된다')],
     ['anatomical enlargement', 'before-after photo edit claim', 'unrequested padded costume']),
    ('sv_lower_abdominal_skin_marking', 'SV26', 'body_marking', 'appearance', 'body.markings',
     '배꼽 기준 위치가 명시된 하복부 피부 문양', 'navel-relative lower-abdominal skin marking',
     [
      ('the marking lies on the same adult lower-abdominal skin', 'the chosen motif sits directly on the declared adult lower belly skin', '선택한 문양이 같은 성인의 하복부 피부에 놓인다'),
      ('the navel and marking have the explicitly selected spatial relation', 'the skin design keeps its specified distance and direction from the navel', '배꼽과 문양이 지정한 방향과 거리 관계를 유지한다'),
      ('the marking follows the continuous skin surface inside the existing wardrobe boundaries', 'the motif follows the same belly skin while the chosen garment coverage stays fixed', '문양이 이어진 피부 면을 따르고 기존 의복 경계를 유지한다')],
     ['symbol on clothing', 'generic upper-arm tattoo', 'automatic exposure or glowing heart motif']),
    ('sv_declared_skin_motif_topology', 'SV27', 'body_marking', 'appearance', 'body.markings',
     '이미 선택한 피부 문양의 명시된 선 연결과 대칭', 'explicit line topology and symmetry of the chosen skin motif',
     [
      ('the skin motif retains the explicitly chosen connected and disconnected elements', 'the requested open and closed shapes retain their separate line connections', '피부 문양의 열린 선과 닫힌 도형이 지정한 연결과 분리를 유지한다'),
      ('the motif follows the separately selected symmetry and color', 'the chosen symmetry relation and pigment color remain visible', '문양의 지정한 대칭 관계와 색이 보인다'),
      ('all motif elements occupy the same declared skin carrier', 'every selected shape belongs to the same skin design', '선택한 모든 도형이 같은 피부 문양에 속한다')],
     ['universal heart silhouette', 'unrequested bilateral symmetry', 'floating disconnected prop instead of skin marking']),
]

DIMENSION_CONTEXT = {
 'expression': ['eye', 'eyes', 'pupil', 'mouth', 'tongue', 'face', 'actor', '눈', '동공', '혀', '입'],
 'pose': ['pose', 'actor', 'person', 'seated', 'leg', 'legs', 'support', '자세', '다리', '무릎', '골반'],
 'appearance': ['actor', 'person', 'adult', 'eye', 'skin', 'garment', 'cheek', '성인', '피부', '문양', '의복', '눈'],
}


def profile_and_candidate(unit):
    pid, draft, slot, dim, prop, ko, en, components, substitutes = unit
    observation = '; '.join(c[0] for c in components)
    alternatives = [en, ko, '; '.join(c[1] for c in components), '; '.join(c[2] for c in components)]
    compiled_components = []
    for i, terms in enumerate(components, 1):
        compiled_components.append({
            'id': f'component_{i}', 'match_terms': list(terms),
            'evidence_field': f'component_{i}_phrase', 'evidence_terms': list(terms),
            'min_content_words': 3,
            'instruction': f'Keep the declared actor, carrier and current configuration: {terms[0]}.',
            'render_gate': {'id': f'vo_{pid}_{i}', 'review_scale': 'native',
                'description': f'{terms[0]}. Inspect the original pixels; every component is required, partial evidence fails, and a hidden prerequisite is unobservable.'},
        })
    profile = {
        'id': pid, 'category': 'observable_slang_component_relation',
        'activation': {'exact_terms': [en, ko], 'requires_adult_character': True,
            'semantic_discovery_requires_component_evidence': True,
            'hard_activation': {'contract_version': 'photo-visual-hard-activation/v1',
                'required_any_groups': [{'id': 'declared_carrier_context', 'any_terms': DIMENSION_CONTEXT[dim]}]}},
        'semantics': {'definition': observation, 'paraphrase_examples': alternatives[2:],
            'visual_components': [c[0] for c in components], 'contrast_examples': substitutes,
            'claim_limits': [
                'Preserve the same declared actor, carrier, existing medium, view, garment coverage, count and property locks.',
                'The technical relation is one observable component, not a synonym for every original genre, event, role or evaluative meaning of a slang word.',
                'A still image establishes current visible geometry only; it does not establish identity, emotion, health, desire, consent, action history or user acceptance.',
                'Every required relation must pass in original pixels; occlusion is unobservable and partial evidence fails.']},
        'concept_candidate': {'concept_terms': unique(alternatives + [c[0] for c in components]),
            'core_assertion_discovery': True, 'affected_dimensions': [dim], 'affected_properties': effect(dim, prop)},
        'runtime_expression': {'default_mode': 'definition_with_optional_label', 'prompt_label_terms': [],
            'forbidden_prompt_terms': [], 'runtime_forbidden_labels': []},
        'authored_components': {'contract_version': 'photo-authored-visual-components/v1', 'components': compiled_components},
        'reject_substitutes': substitutes,
    }
    # compile is a validation step. Persist only the single authored owner, not
    # a second manually editable copy of its derived evidence/gate fields.
    compile_visual_profile(profile)
    candidate = {
        'id': pid, 'ko': ko, 'en': observation, 'weight': 0.5,
        'tags': ['human', 'adult', 'age_context_only', 'observable_relation'], 'for_any': ['human'],
        'paraphrases': alternatives, 'keywords': [c[0] for c in components],
        'embedding_text': ' '.join(alternatives + [observation]),
        'concept_units': [c[0] for c in components],
        'relations': [{'id': 'declared_carrier_owner', 'type': 'declared_owner_scope',
            'subject': 'main_subject', 'object': observation}],
        'affected_dimensions': [dim], 'affected_properties': effect(dim, prop), 'core_assertion_discovery': True,
    }
    return profile, candidate


# Full equivalent observations, never a bare adjective, body-part noun or event.
ALTERNATIVES = {
 'pv_half_lidded': ['윗눈꺼풀과 아랫눈꺼풀 사이가 좁아졌지만 동공이 부분적으로 보이는 눈', 'partly open eyes with reduced lid apertures and partly visible pupils'],
 'pv_parted_lips': ['윗입술과 아랫입술 사이에 작은 틈이 보이는 현재 입 형태', 'a small visible separation between the upper and lower lip margins'],
 'ae_slack_jaw': ['턱이 아래로 내려가 작은 입술 틈보다 크게 열린 입', 'a dropped lower jaw with a mouth aperture larger than a slight lip part'],
 'ae_deadpan_form': ['입꼬리는 수평이고 눈썹 윤곽은 과장되지 않은 얼굴', 'level mouth corners with comparatively unaccented eyebrow contours'],
 'pv_double_v': ['같은 인물의 두 손에서 각각 검지와 중지가 V를 만들고 별개의 손목과 팔로 이어지는 자세', 'two separate actor-owned V hands with index-middle splits and continuous wrists and arms'],
 'pv_v_sign': ['검지와 중지는 벌어지고 약지와 새끼손가락은 접히며 엄지가 붙어 있는 한 손의 V', 'one connected hand separates the index and middle fingers while ring and little fingers fold beside an attached thumb'],
 'pv_wide_stance': ['같은 인물의 두 발이 바닥에 닿은 채 좌우 지지 폭을 넓힌 서 있는 자세', 'a standing base with both actor-owned feet grounded and laterally spaced'],
 'pv_chair_straddle': ['골반은 의자 좌면에 닿고 의자 구조의 양옆에 다리가 하나씩 이어진 앉은 자세', 'a supported chair straddle with the pelvis on the seat and one connected leg on each side of the chair structure'],
 'pv_supine': ['등 쪽 몸통이 지지 면에 닿고 앞몸통은 그 면의 반대쪽을 향하는 누운 자세', 'a reclining actor with posterior torso contact and the anterior torso facing away from the support'],
 'soft_full_figure_volume': ['성인 위팔과 몸통, 골반과 허벅지의 둥근 양감이 한 시점에서 연속되고 허리 경계도 읽히는 체형', 'continuous rounded soft volume across adult upper arms torso hips and thighs with a distinct readable waist contour'],
 'ne_regional_soft_volume': ['같은 성인의 지정 부위가 둥글게 나오고 이웃 부위 윤곽에 자연스럽게 이어진 형태', 'a named adult region has rounded outward volume joined continuously to its neighboring contour'],
 'ne_regional_contour_transition': ['같은 성인 몸통의 지정 구간 안에서 오목한 선과 볼록한 선이 이어지는 윤곽', 'a specified adult torso segment joins concave and convex curves along one continuous regional outline'],
 'bm_abdominal_projection': ['같은 성인의 상복부와 하복부가 이어지는 옆몸통 선을 기준으로 각각 앞으로 나온 관계', 'separately readable upper and lower belly projections along the same adult continuous side-torso contour'],
 'bm_breast_fullness': ['같은 성인의 가슴을 위아래와 안팎 구간으로 나눠 각 부위 양감을 구별하는 형태', 'upper lower medial and lateral fullness partitions of the same adult breast region'],
 'bm_breast_root_width': ['같은 흉벽 위에서 가슴의 안쪽 부착점부터 바깥 부착점까지 읽히는 가로 범위', 'medial-to-lateral breast attachment extent on the same declared chest wall'],
 'bm_breast_spacing': ['같은 성인의 몸통 정중선을 기준으로 양쪽 가슴 안쪽 경계의 간격과 방향이 보이는 관계', 'bilateral medial breast contours spaced and oriented around the same adult torso centerline'],
 'bm_breast_asymmetry': ['같은 성인의 한 시점에서 왼쪽과 오른쪽 가슴의 지정한 양감이나 위치 차이를 비교하는 관계', 'the selected left-right breast volume or position difference within one adult body and the same view'],
 'bm_gluteal_projection': ['같은 성인의 골반 기준 뒤쪽 둔부 돌출이 허벅지 부착으로 이어지는 윤곽', 'posterior gluteal projection anchored to the same adult pelvis and continuing into the thigh attachment'],
 'bm_gluteal_fullness': ['같은 성인의 이어진 뒤쪽 둔부 윤곽에서 위와 아래 구간의 양감이 구별되는 형태', 'separately readable upper and lower gluteal fullness along the same adult continuous posterior contour'],
 'bm_fabric_body_outline': ['불투명한 같은 의복 면이 신체에 닿는 구간에서 몸의 윤곽을 전하는 형태', 'the continuous opaque garment surface transmits the outline at its declared body-contact region'],
 'bm_garment_bulge': ['같은 불투명 의복의 지정 접촉 부위에 국소적으로 솟은 원단 면', 'a localized outward fabric projection at the specified contact on the same opaque garment'],
 'bm_garment_central_crease': ['이어진 불투명 의복 면 가운데 주름과 그 양옆의 한 쌍 윤곽이 구별되는 형태', 'one continuous opaque garment has a central crease and two separately readable adjoining contours'],
}

PROFILE_CANDIDATE_MAP = {
 'pv_profile_double_v': 'pv_double_v', 'pv_profile_v_sign': 'pv_v_sign',
 'pv_profile_chair_straddle': 'pv_chair_straddle', 'pv_profile_supine': 'pv_supine',
 'soft_full_figure_volume': 'soft_full_figure_volume',
 **{k: k for k in ALTERNATIVES if k.startswith(('bm_', 'ne_'))},
}

COMPONENT_ALTERNATIVES = {
 'pv_profile_double_v': [
   ['each hand separately forms an index-middle V', '각 손에서 검지와 중지가 독립된 V를 만든다'],
   ['each wrist continues through its own forearm to the same actor', '별개의 두 손목이 각각 같은 인물의 팔로 이어진다'],
   ['the chosen palm orientation stays readable on each hand', '각 손바닥의 지정한 방향이 구별된다']],
 'pv_profile_v_sign': [
   ['the index-middle pair forms a separated V', '검지와 중지가 벌어진 V를 만든다'],
   ['the ring and little fingers remain folded', '약지와 새끼손가락이 접힌 채 보인다'],
   ['the distinct thumb joins the same palm', '구별되는 엄지가 같은 손바닥에 붙어 있다'],
   ['the specified palm facing direction remains visible', '지정한 손바닥 방향이 보인다']],
 'ne_regional_soft_volume': [
   ['the named region belongs to one adult actor', '지정한 몸 부위가 같은 성인에게 속한다'],
   ['rounded local volume projects from that region', '그 지정 부위에 둥근 국소 양감이 나온다'],
   ['the rounded outline continues into adjacent regional contours', '둥근 외곽이 인접 부위의 윤곽으로 이어진다']],
 'ne_regional_contour_transition': [
   ['the specified torso segment belongs to the same adult', '지정한 몸통 구간이 같은 성인에게 속한다'],
   ['concave and convex contours both occur in that segment', '그 구간 안에 오목한 선과 볼록한 선이 모두 있다'],
   ['the concave and convex curves join along one regional outline', '오목함과 볼록함이 같은 국소 외곽선으로 이어진다']],
}


def main():
    ledger = {'schema_version': 'photo-slang-integration-receipt/v1', 'new_profiles': [],
              'new_candidates': [], 'alternative_candidate_ids': [], 'alternative_profile_ids': [],
              'component_alternatives': [], 'contract_corrections': [], 'held_drafts': []}
    profiles, slots = [], {}
    for unit in UNITS:
        p, c = profile_and_candidate(unit)
        profiles.append(p); slots.setdefault(unit[2], []).append(c)
        ledger['new_profiles'].append({'id': p['id'], 'draft_id': unit[1]})
        ledger['new_candidates'].append({'id': c['id'], 'slot': unit[2], 'draft_id': unit[1]})

    overlays = {}
    candidate_owners = {}
    for file in [ASSETS / 'photo_prompt_tags.json', *sorted(ASSETS.glob('*_extension.json'))]:
        if file.name == 'photo_prompt_slang_visual_extension.json': continue
        for slot, rows in json.loads(file.read_text()).get('slots', {}).items():
            for entry in rows:
                candidate_owners[entry['id']] = (slot, file.name)
    for cid, alternatives in ALTERNATIVES.items():
        if cid not in candidate_owners:
            raise ValueError(f'Missing reviewed candidate owner: {cid}')
        slot, owner = candidate_owners[cid]
        overlays.setdefault(slot, {})[cid] = {'paraphrases': alternatives}
        ledger['alternative_candidate_ids'].append({'id': cid, 'slot': slot, 'owner': owner, 'added': alternatives})
    write(ASSETS / 'photo_prompt_slang_visual_extension.json', {
        'schema_version': 'photo-prompt-research-extension/v1', 'slots': slots,
        'existing_slot_context_extensions': overlays})
    write(ASSETS / 'photo_prompt_visual_obligations_slang_visual.json', {
        'schema_version': 'photo-visual-obligation-registry-extension/v1',
        'relation_contract_version': 'photo-visual-relation/v1', 'profiles': profiles})

    for file in [ASSETS / 'photo_prompt_visual_obligations.json', *sorted(ASSETS.glob('photo_prompt_visual_obligations_*.json'))]:
        if file.name == 'photo_prompt_visual_obligations_slang_visual.json': continue
        data = json.loads(file.read_text()); changed = False
        for profile in data.get('profiles', []):
            pid = profile['id']; cid = PROFILE_CANDIDATE_MAP.get(pid)
            if cid:
                profile['semantics']['paraphrase_examples'] = unique(profile['semantics'].get('paraphrase_examples', []) + ALTERNATIVES[cid])
                ledger['alternative_profile_ids'].append({'id': pid, 'owner': file.name, 'added': ALTERNATIVES[cid]})
                changed = True
            if pid in COMPONENT_ALTERNATIVES:
                components = profile['authored_components']['components']
                assert len(components) == len(COMPONENT_ALTERNATIVES[pid]), pid
                for component, alternatives in zip(components, COMPONENT_ALTERNATIVES[pid]):
                    component['match_terms'] = unique(component['match_terms'] + alternatives)
                    component['evidence_terms'] = unique(component['evidence_terms'] + alternatives)
                # These fields are regenerated from authored_components at load.
                for key in ('required_evidence_fields', 'evidence_requirements', 'render_gates', 'composition_instruction'):
                    profile.pop(key, None)
                profile['semantics'].pop('component_semantics', None)
                compile_visual_profile(profile)
                ledger['component_alternatives'].append(pid); changed = True
            if pid == 'composite_overwhelmed_expression':
                correct_composite(profile)
                ledger['contract_corrections'].append({'id': pid, 'owner': file.name,
                    'reason': 'The original genre label has multiple visible variants. Small symmetric O mouth, tiny centered tongue, blush, fatigue and no-smirk were unjustified universal requirements.'})
                changed = True
            if pid in ('soft_full_figure_volume', 'bust_prominence_relation'):
                # A limits disclaimer is not a visible required prompt phrase.
                key = 'neutral_separation_phrase' if pid == 'soft_full_figure_volume' else 'whole_body_separation_phrase'
                group_id = 'neutral_separation' if pid == 'soft_full_figure_volume' else 'whole_body_separation'
                group = next(g for g in profile['semantics']['component_semantics']['groups'] if g['id'] == group_id)
                profile['semantics']['visual_components'] = [g['any_terms'][0] for g in profile['semantics']['component_semantics']['groups']]
                profile['evidence_requirements'][key]['must_mention_any'] = group['any_terms'][:2]
                profile['concept_candidate']['affected_dimensions'] = ['body_geometry']
                profile['concept_candidate']['affected_properties'] = effect('body_geometry', 'body')
                if pid == 'bust_prominence_relation':
                    additions = ['같은 성인의 양측 가슴이 흉곽 바탕과 자연 허리를 기준으로 앞과 옆으로 두드러지는 관계',
                        'both adult breast contours project forward and laterally relative to the same ribcage and natural waist']
                    profile['semantics']['paraphrase_examples'] = unique(profile['semantics']['paraphrase_examples'] + additions)
                    ledger['alternative_profile_ids'].append({'id': pid, 'owner': file.name, 'added': additions})
                ledger['contract_corrections'].append({'id': pid, 'owner': file.name,
                    'reason': 'Evidence now uses the existing positive contour-relation group rather than requiring a nonvisual disclaimer; body effects are explicitly conservative.'})
                changed = True
        if changed: write(file, data)
    ledger['held_drafts'] = ['SV11', 'SV13', 'SV14', 'SV22', 'SV23', 'SV25']
    write(Path(__file__).with_name('authored-change-receipt.json'), ledger)
    print(json.dumps({k: len(v) for k, v in ledger.items() if isinstance(v, list)}, ensure_ascii=False))


def correct_composite(profile):
    semantics = profile['semantics']
    semantics['definition'] = 'One declared adult face simultaneously shows upward or explicitly asymmetric pupil placement, an open mouth and a tongue crossing its lip boundary; their chosen visible variants remain independent.'
    semantics['paraphrase_examples'] = [
        '한 성인의 얼굴에서 위쪽 또는 명시한 비대칭 눈동자 배치, 벌어진 입, 입술 밖 혀가 동시에 보이는 복합 표정',
        'one adult face simultaneously shows upward or specified asymmetric pupils, an open mouth and a tongue beyond the lips',
        'eyes rolled upward with a dropped open jaw and the tongue visibly crossing the lip boundary on the same adult face',
        'upward pupils with a small rounded open mouth and an external tongue tip in the same expression',
    ]
    semantics['visual_components'] = ['specified upward or left-right pupil geometry', 'selected mouth opening', 'connected tongue beyond the lip boundary', 'all components on the same adult face simultaneously']
    # Partial geometry may propose an optional concept, as in the existing
    # frozen routing contract. Complete rendered qualification still requires
    # eyes, mouth and tongue together through the five evidence fields/gates.
    semantics['component_semantics'] = {'minimum_component_groups': 2,
        'required_group_ids': ['upward_eye_configuration'],
        'groups': [
            {'id': 'upward_eye_configuration', 'any_terms': ['동공이 위', '눈동자가 위', '눈동자가 비대칭', '위를 향한 눈동자', '비대칭 위쪽 시선', 'pupils drift upward', 'asymmetric upward eyes', 'eyes rolled upward', 'upward eye drift', 'both pupils sit high inside the eye openings']},
            {'id': 'open_mouth', 'any_terms': ['둥글게 벌린 입', '크게 벌어진 입', '턱이 내려간 입', 'small rounded open mouth', 'round open mouth', 'open mouth', 'dropped open jaw', 'jaw lowers beneath a visibly open mouth']},
            {'id': 'external_tongue_tip', 'any_terms': ['혀끝이 입술 밖', '혀가 입술 경계를 넘', 'tongue tip past the lips', 'external tongue tip', 'tongue protrudes', 'tongue visibly crosses the outer lip boundary', 'tongue projects beyond the lip edge']},
        ]}
    semantics['contrast_examples'] = ['ordinary eye contact with a closed mouth', 'tongue entirely inside an open mouth', 'components assigned to separate faces', 'genre label without observable component realization']
    semantics['claim_limits'] = [
        'The original ahegao genre term can denote a stylized depiction of sexual ecstasy. Neutral facial geometry is a partial visual projection, not a complete synonym or evidence of that event.',
        'Brow state, mouth size, tongue position, cheek color and fatigue are independent variant choices; the label does not make one variant universally mandatory.',
        'Facial configuration alone does not establish an event, sexual activity, consent, wardrobe, emotion, or a medical or psychological state.',
        'Preserve the requesting user meaning and exclusions independently of the selected runtime description; forbidden labels are not erased from meaning retrieval.',
    ]
    profile['concept_candidate'] = {'concept_terms': semantics['paraphrase_examples'] + semantics['visual_components'],
        'core_assertion_discovery': True, 'affected_dimensions': ['expression'],
        'affected_properties': effect('expression', 'face.expression')}
    profile['composition_instruction'] = 'Show the specified eye placement, chosen mouth opening and connected external tongue simultaneously on the same declared adult face. Retain the requested mouth size, tongue placement and extent; choose brow contour and cheek color only from the frozen core or a separately accepted option.'
    profile['required_evidence_fields'] = ['adult_safe_context_phrase', 'eye_configuration_phrase', 'open_mouth_phrase', 'external_tongue_tip_phrase', 'simultaneous_expression_phrase']
    profile['evidence_requirements'] = {
        'adult_safe_context_phrase': {'min_content_words': 3, 'must_mention_any': ['adult', 'mid-twenties'], 'must_not_contain': ['girl', 'teen', 'schoolgirl']},
        'eye_configuration_phrase': {'min_content_words': 3, 'must_mention_any': ['upward eye drift', 'pupils drift upward', 'asymmetric upward', 'eyes rolled upward', 'pupils sit high', 'specified asymmetric pupils']},
        'open_mouth_phrase': {'min_content_words': 3, 'must_mention_any': ['open mouth', 'open jaw', 'mouth opening', 'small open O', 'rounded-open mouth']},
        'external_tongue_tip_phrase': {'min_content_words': 3, 'must_mention_any': ['tongue tip crosses', 'tongue tip past', 'external tongue tip', 'tongue tip outside', 'tongue crosses', 'tongue crossing', 'tongue projects beyond', 'tongue visibly crossing']},
        'simultaneous_expression_phrase': {'min_content_words': 4, 'must_mention_any': ['simultaneously', 'same expression', 'coexist', 'at once', 'same adult face']},
    }
    profile['render_gates'] = [
        {'id': 'vo_overwhelmed_adult_safe_context', 'review_scale': 'both', 'description': 'The authored fictional adult context remains consistent with the depicted subject; visible appearance alone does not verify real age or identity.'},
        {'id': 'vo_overwhelmed_eye_configuration', 'review_scale': 'native', 'description': 'The same face shows the specified upward or actor-relative asymmetric pupil positions inside readable eye apertures.'},
        {'id': 'vo_overwhelmed_open_mouth', 'review_scale': 'native', 'description': 'The mouth is visibly open with the chosen size and jaw configuration; small-O and large openings are distinct allowed variants.'},
        {'id': 'vo_overwhelmed_external_tongue_tip', 'review_scale': 'native', 'description': 'The tongue visibly crosses the lip boundary and continues into its own mouth with the chosen placement and extent.'},
        {'id': 'vo_overwhelmed_components_coexist', 'review_scale': 'both', 'description': 'The specified eyes, open mouth and external tongue coexist on the same adult face in the same frame; partial evidence fails and occluded components are unobservable.'},
    ]
    profile['reject_substitutes'] = ['ordinary_eye_contact_only', 'tongue_wholly_inside_mouth', 'closed_mouth_with_tongue', 'components_on_different_actors', 'occluded_required_component']


if __name__ == '__main__': main()
