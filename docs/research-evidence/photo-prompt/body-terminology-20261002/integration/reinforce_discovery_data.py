"""Add ordinary morphology readings without promoting them to exact aliases."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
PROFILE = ASSETS / 'photo_prompt_visual_obligations_body_morphology.json'
CANDIDATE = ASSETS / 'photo_prompt_body_morphology_extension.json'

READINGS = {
    'shoulder_width': ['broad shoulders relative to the upper torso', 'narrow shoulders relative to the upper torso', '넓은 어깨와 몸통의 폭 비교', '좁은 어깨와 몸통의 폭 비교'],
    'shoulder_slope': ['gently sloping shoulders from neck to shoulder tips', 'level shoulder line with a shallow neck-to-shoulder descent', '완만하게 내려가는 어깨선', '수평에 가까운 어깨 경사'],
    'muscle_volume': ['moderate regional muscle volume', 'large muscle bulk with soft surface definition', 'small muscle volume with clear surface definition', '적당한 근육 부피', '큰 근육 부피와 부드러운 표면'],
    'torso_limb_ratio': ['long legs relative to the torso', 'short legs relative to the torso', 'long torso with shorter leg segments', '몸통보다 길게 읽히는 다리 비율', '상체와 다리 길이의 상대 비율'],
    'finger_proportion': ['long fingers relative to a short palm', 'short fingers relative to a long palm', 'finger length compared with connected palm length', '손바닥에 비해 긴 손가락', '손바닥 길이와 손가락 길이 비교'],
    'knuckle_relief': ['prominent rounded finger knuckles', 'raised finger-joint contours', 'subtle knuckle relief at connected finger joints', '도드라진 손마디 윤곽', '연결된 손가락 관절의 솟은 마디'],
    'compression_contour': ['shallow skin groove along a waistband contact edge', 'belt indentation with neighboring skin displacement', 'a garment band pressing into the local skin contour', '허리밴드 접촉 경계의 얕은 피부 압흔', '벨트 경계에서 밀리는 국소 몸 윤곽'],
    'pose_surface_change': ['skin folds on the compressed flank during a side bend', 'localized skin creases tied to a current lean', 'surface deformation at a loaded body region', '측굴로 압축되는 옆구리 피부 주름', '현재 하중과 구부림에 따른 표면 변화'],
    'skin_fold_wrinkle': ['short skin folds on a bent torso', 'localized fold ridges on flexed skin', '구부린 몸통에서 모이는 피부 주름'],
    'body_hair_fiber': ['fine short lightly pigmented vellus body hair', 'coarse longer pigmented terminal body hair', 'body-hair strands visibly rooted in the skin', '가늘고 짧은 솜털', '굵고 길며 색이 짙은 국소 체모'],
    'body_hair_distribution': ['localized forearm hair distribution', 'a sparse patch of body hair on an upper arm', '팔 피부 위 국소 체모의 분포'],
    'vascular_surface': ['branching superficial veins beneath local skin', 'visible dorsal-hand veins with continuous courses', 'localized blue-green vessel paths under intact skin', '손등 피부 아래 이어지는 표재 정맥', '피부 아래 갈라지는 혈관 경로'],
}

def add(values, additions):
    for value in additions:
        if value.casefold() not in {v.casefold() for v in values}:
            values.append(value)

profiles = json.loads(PROFILE.read_text())
candidates = json.loads(CANDIDATE.read_text())
by_profile = {p['id']: p for p in profiles['profiles']}
by_candidate = {e['id']: e for entries in candidates['slots'].values() for e in entries}
for axis, readings in READINGS.items():
    add(by_profile['bm_' + axis]['semantics']['paraphrase_examples'], readings)
    add(by_candidate['bm_' + axis]['paraphrases'], readings)

# Pore microrelief and follicular piloerection are separate visible properties.
pid = 'bm_skin_piloerection'
units = ['raised follicular skin relief',
         'upright hairs attached within the same local skin patch',
         'local continuity between follicles and neighboring skin']
effects = [dict(dimension='appearance', target='main_subject', property='body.skin_region.piloerection_relief')]
if pid not in by_profile:
    p = copy.deepcopy(by_profile['bm_skin_relief_texture'])
    p['id'] = pid
    p['activation']['exact_terms'] = ['adult skin piloerection', 'visible goosebumps on adult skin', '성인 피부의 털세움 소름']
    p['semantics']['definition'] = ('A localized adult skin patch shows raised follicular relief and attached upright hairs, '
        'with continuous neighboring skin visible in the current view.')
    p['semantics']['paraphrase_examples'] = ['skin goosebumps with visible follicular elevations',
        'local piloerection relief and standing body-hair fibers', '피부 모낭 부위의 솟은 요철과 서 있는 털']
    p['semantics']['visual_components'] = units
    groups = [dict(id=f'component_{i+1}', any_terms=[unit]) for i,unit in enumerate(units)]
    groups.append(p['semantics']['component_semantics']['groups'][-1])
    p['semantics']['component_semantics']['groups'] = groups
    p['semantics']['contrast_examples'] = ['Pore openings, random noise or follicular keratin plugs alone do not establish piloerection.']
    p['semantics']['claim_limits'].append('Visible bumps alone do not diagnose a skin condition or prove cold, emotion or physiological cause.')
    p['concept_candidate'] = dict(concept_terms=['skin piloerection', 'skin goosebumps', *units],
        core_assertion_discovery=True, affected_dimensions=['appearance'], affected_properties=effects)
    p['runtime_expression']['prompt_label_terms'] = ['localized skin piloerection']
    p['composition_instruction'] = 'On the same adult skin region show ' + '; '.join(units) + '; preserve the stated current view and pose.'
    p['evidence_requirements'] = {field:dict(min_content_words=2, must_mention_any=groups[i]['any_terms'])
        for i,field in enumerate(p['required_evidence_fields'])}
    p['render_gates'] = [dict(id=f'vo_{pid}_{g["id"]}', review_scale='native',
        description='The same adult skin region visibly establishes ' + g['any_terms'][0] + '.') for g in groups]
    profiles['profiles'].append(p)
if pid not in by_candidate:
    candidates['slots']['skin_finish'].append(dict(id=pid, ko='국소 피부의 솟은 모낭 요철과 털세움',
        en='localized skin piloerection with raised follicular relief and upright attached hairs',
        weight=0.5, tags=['human', 'skin_region'], for_any=['human'], aliases=['skin goosebumps', '피부 소름 요철'],
        keywords=units, paraphrases=['goosebumps on a local skin patch', 'raised follicular bumps with fine standing hairs', '국소 피부의 솟은 모낭 요철'],
        embedding_text='localized skin piloerection; ' + '; '.join(units), concept_units=units,
        relations=[dict(id='skin_hair_attachment', type='has_visible_property', subject='main_subject',
            object='raised follicular skin relief with upright attached hairs')], affected_dimensions=['appearance'],
        affected_properties=effects, core_assertion_discovery=True))
for path, payload in [(PROFILE, profiles), (CANDIDATE, candidates)]:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
print('Reviewed paraphrase families:', len(READINGS), '; distinct new piloerection profile/candidate:', pid)
