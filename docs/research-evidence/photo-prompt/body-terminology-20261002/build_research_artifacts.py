"""Compile research proposals only. Never writes assets, indexes, packs or prompts."""
from pathlib import Path
from collections import Counter
import csv
import json
import re

OUT = Path(__file__).resolve().parent

def read(name):
    return json.loads((OUT / name).read_text())

def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')

def rows(name):
    with (OUT / name).open() as f:
        return list(csv.DictReader(f, delimiter='|'))

sources = read('SOURCES.json')
extra_sources = [
    dict(id='S46', title='Understance former bra filtering taxonomy',
         url='https://understance.com/collection/bras?breast_fullness=Top-full&sort_by=featured&view_all=false',
         kind='manufacturer_fit', access_status='historical_search_excerpt',
         supported_dimension='과거 제품 필터에서 projection·fullness·root width를 별도 축으로 취급',
         limitations='과거 크롤의 공개 검색 발췌만 확인. 현재 본문은 영업 종료 안내로 전환되어 현행 제품 체계의 근거로 채택하지 않음.'),
    dict(id='S47', title="Billy's Bras: Understanding Root Width and Breast Shape",
         url='https://billysbras.com/blogs/billys-bra-blog/understanding-root-width-and-breast-shape',
         kind='retailer_fit_education', access_status='full_page',
         supported_dimension='가슴 부착 범위의 내외측 폭·root height와 spacing·projection의 구별',
         limitations='소매업체의 피팅 설명으로 임상 규격이나 보편적 미적 기준이 아님. 이미지는 검사하지 않았고 공개 본문 형태 설명만 이용.'),
]
for source in extra_sources:
    source['source_support_does_not_establish'] = ['retrieval_quality', 'rendered_quality', 'user_acceptance']
    if source['id'] not in {s['id'] for s in sources['sources']}:
        sources['sources'].append(source)
save('SOURCES.json', sources)
source_by_id = {s['id']: s for s in sources['sources']}
access_labels = dict(full_page='공개 본문 확인', full_public_abstract='공개 초록 확인',
    pdf_text='PDF 텍스트 확인', search_excerpt='검색 발췌만 확인',
    search_abstract='검색 초록만 확인', historical_search_excerpt='과거 검색 발췌만 확인')
notes = ['# 출처별 근거와 제한', '', '2026-10-02 확인. URL은 연구 provenance이며 검색 prototype이나 런타임 텍스트가 아니다.', '',
    '공개 본문 36건·공개 초록 1건·PDF 텍스트 1건, 검색 발췌 7건·검색 초록 1건·과거 검색 발췌 1건이다. 검색 발췌만 확보한 자료는 세부 정의를 확정하는 단독 근거로 쓰지 않는다.', '']
for source in sources['sources']:
    notes += ['## ' + source['id'] + ' — ' + source['title'], '',
        '[' + source['title'] + '](' + source['url'] + ')', '',
        '- 확인: ' + access_labels[source['access_status']] + '.',
        '- 조사에 사용한 범위: ' + source['supported_dimension'] + '.',
        '- 한계: ' + source['limitations'], '']
notes += ['## 아직 충분히 확보하지 못한 근거', '',
    '한국어 압축어의 확정 사전 정의, 일부 커뮤니티 은어의 개별 용법, root-height 및 세부 국소 형태의 추가 공개 근거, Blender shape-key와 MetaHuman 세부 API의 현행 본문은 추가 확인이 필요하다.', '',
    '출처는 관찰 축과 의미 경계를 작성하는 근거다. retrieval·prompt·runtime·pixels·사용자 수용을 통과했다는 증거가 아니다.', '']
(OUT / 'SOURCE-NOTES.md').write_text('\n'.join(notes))

audit = read('CURRENT-DATA-AUDIT.json')
specs = rows('PROPOSAL-SPECS.psv')
profile_ids = {p['id'] for p in audit['selected_profiles']}
# The authoritative ownership comes from the corpus, never from a guessed slot name.
root = OUT.parents[3]
tags = json.loads((root / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json').read_text())
dimensions = tags['candidate_semantic_policy']['slot_dimensions']
semantics, candidates = [], []
coupled = {
    'compression_contour': ['appearance', 'body_geometry'],
    'thigh_gap': ['body_geometry', 'pose'],
    'nail_shape': ['body_geometry'],
    'pose_surface_change': ['pose', 'body_geometry', 'appearance'],
}
for spec in specs:
    parts = spec['components'].split(';')
    existing = [x for x in spec['existing_profiles'].split(',') if x]
    assert set(existing) <= profile_ids, (spec['id'], existing)
    primary_dimensions = dimensions[spec['slot']]
    complete_dimensions = coupled.get(spec['id'], primary_dimensions)
    incompatible = not set(complete_dimensions) <= set(primary_dimensions)
    groups = [dict(id=f"{spec['id']}_c{i + 1}", positive_visual_phrase=part)
              for i, part in enumerate(parts)]
    proposal = dict(
        id='body_research_' + spec['id'], status='research_proposal_not_implemented',
        batch=spec['batch'], owner=spec['owner'], property_axis=spec['property'],
        definition_ko=spec['ko'], definition_en=spec['en'],
        proposed_action='review_and_enrich_existing_owner' if existing else 'review_new_axis_after_deduplication',
        existing_profile_ids=existing, source_refs=spec['sources'].split(','),
        source_access=[dict(id=s, status=source_by_id[s]['access_status']) for s in spec['sources'].split(',')],
        detailed_morphology_evidence_status='additional focused sources required' if spec['id'] in
            ('vascular_surface', 'breast_root_height', 'navel_shape', 'foot_arch_instep', 'nail_shape', 'eyelid_fold', 'ear_attachment')
            else 'cross-domain authoring basis; operational gates remain proposals',
        source_basis='자료는 용어·위치·차원 구분을 뒷받침한다. 아래 게이트와 속성 경로는 프로젝트를 위한 저자 제안이며 출처의 생성 성능 실험이 아니다.',
        component_groups=groups,
        directed_relations=[dict(subject=spec['owner'], relation='has_visible_property', object=part)
                            for part in parts],
        required_view_state=spec['view'], closest_counterexample=spec['closest_counterexample'],
        proposed_render_gates=[dict(id=g['id'], required=True,
            description='Verify the visible owner and ' + g['positive_visual_phrase'],
            review_scale='native' if spec['batch'] in ('P3', 'P4') else 'both') for g in groups],
        activation_plan=dict(exact_terms_status='not_proposed_for_automatic_activation_yet',
            lexical_input='Explicit requester meaning or a narrow reviewed phrase with owner and region.',
            context='Bind the actual actor and region from the frozen core; retain garment, pose and reference locks.',
            indirect_hits='advisory_until_opt_in',
            scope='explicit neutral adult context required' if spec['batch'] == 'P4' else 'request-supported adult appearance'),
        forbidden_inferences=['health or numerical body composition from appearance',
            'personal history or identity from local morphology', 'unrequested changes to other properties'],
        assessment_policy=dict(partial_is_fail=True, occluded_required_component='unassessable_not_success',
            blocked_render='unscored_attempt', user_acceptance='separate_not_received'),
        export_allowed=False,
    )
    semantics.append(proposal)
    properties = [dict(dimension=dimension, target='ACTOR_FROM_FROZEN_CORE:' + spec['owner'],
                       property='research.' + spec['owner'] + '.' + spec['property'])
                  for dimension in complete_dimensions]
    candidates.append(dict(
        id='body_candidate_proposal_' + spec['id'], status='research_candidate_draft_not_implemented',
        semantic_proposal_id=proposal['id'], batch=spec['batch'], preferred_existing_slot=spec['slot'],
        slot_declared_dimensions=primary_dimensions, complete_effect_dimensions=complete_dimensions,
        affected_properties=properties,
        property_namespace_status='symbolic_research_paths_require_canonical_binding_before_export',
        ownership_review='split_support_or_review_ownership_before_admission' if incompatible else 'compatible_at_dimension_level_only',
        positive_candidate_text=dict(ko=spec['ko'], en=spec['en'],
            paraphrases=[spec['ko'], spec['en']],
            keywords=parts, embedding_text=spec['en'], concept_units=parts,
            directed_relations=proposal['directed_relations']),
        alias_policy='labels are scoped paraphrases for review; broad inventory expressions are not copied as exact aliases',
        conditions=['The named actor and region are grounded in the frozen core.',
            'Every affected property is open or explicitly requester-required.',
            'The necessary view and state fit the locked framing, pose and coverage.',
            'No optional candidate is used as evidence of its own prerequisite.'],
        admission_status='ownership_split_required' if incompatible else
            ('explicit_context_review_required' if spec['batch'] == 'P4' else 'schema_and_dedup_review_required'),
        source_refs=proposal['source_refs'], export_allowed=False,
    ))

knowledge = [
    ('composition_measurements', 'body composition / fat mass / lean mass / BMI / circumference / WHR',
     'measurement_or_internal_quantity', ['S01', 'S02', 'S03', 'S04'],
     '실측·장비·측정 프로토콜을 요구하는 항목. 사진의 폭·깊이·표면 묘사와 수치 추정을 분리.'),
    ('size_market', 'petite / tall / plus-size / curve model / runway model / commercial model',
     'industry_size_or_role', ['S08'], '브랜드·모델 활동 분류. 성인 신장·체격의 구체 형태는 별도 요청에서 결정.'),
    ('style_taxonomies', 'Kibbe / Straight Wave Natural / ectomorph mesomorph endomorph',
     'framework_label', ['S35', 'S36', 'S37'], '분류 체계·스타일 설명 맥락을 유지. 생리·체중 변화·특정 신체 치수를 자동 확정하지 않음.'),
    ('evaluative_lexicon', 'slim / shapely / callipygian / voluptuous / perky / gaunt / scrawny',
     'evaluative_and_morphological_components', ['S05', 'S43', 'S44', 'S45'],
     '시각 형태와 칭찬·비하·감각적 평가를 분리. 어감은 provenance 문맥에 두고 positive shape text에는 구체 형태만 남김.'),
    ('korean_compressed', '글래머 / 육덕 / 베이글 / 꿀벅지 / 애플힙 / S라인 / 어깨깡패',
     'conversation_scoped_provisional', [], '원 대화의 표현은 보존. 공신력 있는 한국어 정의를 확보하지 못한 항목은 unconditional exact alias 보류.'),
    ('adult_polysemy', 'thicc / well-endowed / well-hung / stacked / hunk / beefcake',
     'polysemous_context_label', ['S24', 'S25'], '사람·물건·경제·부위와 실제 속성 문맥을 확인. 단어만으로 기관이나 신체 전체를 변경하지 않음.'),
    ('community_labels', 'bear / otter / twink / femboy / MILF / DILF / silver fox / androgynous',
     'community_or_presentation_context', ['S41'], '각 표현의 복합 함의를 구분. 성적 지향·성별 정체성·가족 관계·고정 해부 구성을 외관에서 추정하지 않음. twink 외 항목의 개별 사전 근거는 추가 필요.'),
    ('breast_fit_sizes', 'cup size / sister size / underbust circumference',
     'garment_fit_measurement', ['S15', 'S16', 'S47'], 'band·체계·기저 폭·projection과 분리. cup 문자만으로 절대 가슴 볼륨이나 pixel duty를 만들지 않음.'),
    ('genital_history', 'circumcised / uncircumcised / testes / erection / genital measurements',
     'internal_history_or_state', ['S30', 'S31'], '내부 구조·이력·현재 외형·상태를 구분. 중립 해부 요청에 맞는 부분만 다루며 사진에서 치수나 원인을 추정하지 않음.'),
    ('digital_workflow', 'morph target / shape key / blend shape / rig / shader / normal map',
     'authoring_workflow', ['S33', 'S34'], '제작 변수 이름과 최종 관찰 형태를 분리. 특정 도구 파라미터 조합의 재현성을 주장하지 않음.'),
    ('art_proportions', 'idealized / heroic / caricature / chibi / exaggerated hourglass',
     'request_owned_stylization', ['S32'], '사용자가 선택한 매체·양식에만 적용. 예술적 등신과 현실 인체 분포를 혼합하지 않음.'),
]
save('SEMANTIC-PROPOSALS.json', dict(schema_version='body-semantic-research-proposals/v1',
    status='research_only', notes=['This is not the runtime registry schema.', 'No automatic activation or export is authorized by this file.'],
    proposals=semantics, knowledge_and_context_records=[dict(id='body_context_' + k, expressions=e,
        lane=l, source_refs=s, decision=d, export_allowed=False) for k, e, l, s, d in knowledge]))
save('CANDIDATE-PROPOSALS.json', dict(schema_version='body-candidate-research-proposals/v1',
    status='research_only', notes=['This is not a candidate-pack or dictionary extension.',
        'Canonical targets, properties, weights, guards and deduplication remain implementation work.'],
    candidates=candidates))
catalog = ['# 91개 구체 형상·관계 축의 검토안', '',
    '각 항목은 연구 제안이다. 기존 owner가 없는 항목도 전체 코퍼스 중복 검토 전에는 신규 프로필로 확정되지 않는다. 게이트는 저자가 제안한 검증 기준이며 실제 픽셀 검증은 미실행이다.', '']
for batch in ('P1', 'P2', 'P3', 'P4'):
    catalog += ['## ' + batch, '']
    for p in (p for p in semantics if p['batch'] == batch):
        catalog += ['### ' + p['id'].removeprefix('body_research_') + ' — ' + p['definition_ko'], '',
            '- 관찰 형태: ' + p['definition_en'],
            '- 소유자/속성: `' + p['owner'] + '` / `' + p['property_axis'] + '`.',
            '- 구성요소: ' + '; '.join(g['positive_visual_phrase'] for g in p['component_groups']) + '.',
            '- 보기·상태: ' + p['required_view_state'] + '.',
            '- 가까운 반례: ' + p['closest_counterexample'] + '.',
            '- 기존 소유자: ' + (', '.join('`' + x + '`' for x in p['existing_profile_ids']) or '전체 코퍼스 대조 후 결정') + '.',
            '- 자료: ' + ', '.join('[' + s + '](' + source_by_id[s]['url'] + ')' for s in p['source_refs']) + '.',
            '- 세부 근거 상태: ' + p['detailed_morphology_evidence_status'] + '.', '']
(OUT / 'AXIS-CATALOG.md').write_text('\n'.join(catalog))

cases = []
for spec in rows('REGRESSION-SPECS.psv'):
    cases.append(dict(id=spec['id'], status='proposed_not_run', kind=spec['kind'],
        requester_text=spec['request'], expected_behavior=spec['expectation'],
        proposal_ids=['body_research_' + x for x in spec['proposal_ids'].split(',') if x],
        assertion_authority='frozen requester semantics; proposed behavior is not an observation of current runtime'))
(OUT / 'REGRESSION-CASES.jsonl').write_text(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in cases))

inventory = read('TERM-INVENTORY.json')
for term in inventory['terms']:
    term['routing_recommendation'] = term['routing_recommendation'].replace('정례', '긍정 사례')
    expression = term['expression'].lower()
    if any(token in expression for token in ('circumference', 'underbust', 'arm span', 'inseam', 'waist-to-hip ratio')):
        term['lane'] = 'knowledge_only'
        term['routing_recommendation'] = '실측 정의와 관찰 형태를 분리. 사진에서 수치·측정 결과를 확정하지 않음.'
save('TERM-INVENTORY.json', inventory)

# Chapter bundles are navigation links, never equivalence or activation mappings.
chapter_families = {
    1: ['stature_scale', 'compact_frame', 'waist_width_depth'],
    2: ['stature_scale', 'stocky_build', 'slender_build', 'wiry_definition', 'soft_volume', 'long_limb_build'],
    3: ['curvilinear_relation', 'torso_limb_ratio', 'waist_level', 'head_body_ratio'],
    4: [],
    5: ['muscle_volume', 'muscle_definition', 'vascular_surface', 'muscle_striation'],
    6: ['shoulder_width', 'shoulder_slope', 'ribcage_width', 'ribcage_depth', 'neck_proportion', 'back_width_depth'],
    7: ['bust_prominence', 'breast_root_width', 'breast_root_height', 'breast_projection', 'breast_fullness', 'breast_spacing', 'nipple_projection', 'areolar_surface'],
    8: ['waist_width_depth', 'abdominal_projection', 'seated_skin_folds', 'abdominal_segmentation', 'abdominal_v_boundary', 'navel_shape'],
    9: ['hip_width', 'gluteal_projection', 'gluteal_fullness', 'gluteal_fold', 'gluteal_cleft', 'hip_dip_local', 'back_dimples'],
    10: ['thigh_volume', 'calf_contour', 'limb_alignment', 'thigh_gap', 'finger_proportion', 'knuckle_relief', 'foot_arch_instep', 'nail_shape'],
    11: ['eye_aperture', 'eyelid_fold', 'eye_spacing', 'nose_projection', 'lip_volume', 'philtral_contour', 'ear_attachment', 'facial_asymmetry'],
    12: ['skin_tone_appearance', 'skin_pigment_pattern', 'skin_relief_texture', 'striae_surface', 'cellulite_relief', 'body_hair_fiber', 'body_hair_distribution'],
    13: ['curvilinear_relation', 'bust_prominence', 'shoulder_width', 'gluteal_projection'],
    14: [],
    15: ['neckline_exposure', 'lateral_chest_boundary', 'lower_chest_boundary', 'cleavage_relation', 'fabric_body_outline', 'sheer_layering', 'garment_bulge', 'garment_central_crease'],
    16: ['vulvar_topology', 'penile_topology', 'scrotal_testis_boundary', 'perineal_location'],
    17: ['pose_surface_change', 'limb_difference', 'prosthetic_connection', 'mobility_contact'],
    18: ['head_body_ratio', 'torso_limb_ratio'], 19: [],
}
coverage = []
for term in inventory['terms']:
    related = chapter_families[term['section']]
    coverage.append(dict(term_id=term['id'], expression=term['expression'], chapter=term['section'],
        lane=term['lane'], related_axis_proposal_ids=['body_research_' + x for x in related],
        relation='chapter_navigation_only_not_synonym_equivalence',
        status='requires_term_level_review_before_runtime_export',
        decision=term['routing_recommendation'], runtime_alias_authorized=False))
save('COVERAGE-MAP.json', dict(schema_version='body-term-research-navigation/v1',
    limitations=['All 415 expression groups have a disposition. This does not mean all have a complete runtime profile.',
        'Chapter links are family navigation, not term-by-term verified semantic matches.'], terms=coverage))
print(json.dumps(dict(sources=len(sources['sources']), source_access=dict(Counter(s['access_status'] for s in sources['sources'])),
    semantic_proposals=len(semantics), existing_profile_reuse=sum(bool(p['existing_profile_ids']) for p in semantics),
    candidates=len(candidates), ownership_splits=[c['id'] for c in candidates if c['admission_status']=='ownership_split_required'],
    context_records=len(knowledge), regression_cases=len(cases), inventory=len(coverage),
    batch_counts=dict(Counter(p['batch'] for p in semantics))), ensure_ascii=False))
