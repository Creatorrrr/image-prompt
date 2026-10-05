"""Write semantic probes and original-pixel plans without executing them."""
from __future__ import annotations
import csv, json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def table(name):
    with (HERE / name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

LOCK_PROBES = [
    ('L01', '은색만 허용하는 반지의 선재 형태를 개선해줘.', ['GD13', 'GD25', 'GD26'], 'Silver color/material locks reject gilding or gold overlay; filigree remains conditional on owner and topology.'),
    ('L02', '이 검은 직물의 색과 무늬는 그대로 두고 실의 고정 구조만 읽히게 해줘.', ['GD33', 'GD36', 'GD37'], 'No whitework recoloring or changed motif under a fixed cloth/pattern lock.'),
    ('L03', '피부를 드러내지 않는 안감 위의 브리지형 레이스를 보여줘.', ['GD32'], 'Lace negative space exposes lining, not new skin. Exposure remains locked.'),
    ('L04', '기존 체형을 유지하고 코르셋의 패널선과 앞 여밈만 선명하게 해줘.', ['GD40'], 'Garment construction effects cannot resize waist/bust/torso or alter pose.'),
    ('L05', '창 전체를 포함하는 현재 구도 안에서 판형 트레이서리 구멍을 읽히게 해줘.', ['GD43'], 'No automatic macro crop or lens change; if required plate detail remains unobservable, it does not pass.'),
    ('L06', '사람 없이 단독 금속 상자의 선재 장식만 보여줘.', ['GD13', 'GD14'], 'A wearable main_subject owner cannot add a person; ordinary object adapter must bind the existing object.'),
    ('L07', '종교적 의미를 추가하지 않고 장식 상자의 구획만 정밀하게 보여줘.', ['GD59'], 'Reliquary context cannot override a locked nonreligious concept.'),
    ('L08', '정지한 기계의 열린 덮개 안 구조만 보여줘.', ['GD63'], 'Exposed mechanisms do not create operation, sparks or a new action event.'),
    ('L09', '밝은 스튜디오 배경은 유지하고 성인 고스 의상만 자세히 보여줘.', ['GD52', 'GD56'], 'No cathedral/ruined castle default; generic goth does not become Gothic Lolita.'),
    ('L10', '실제 사진의 금속 표면을 자세히 보여주되 선묘 양식으로 바꾸지 마.', ['GD18'], 'Incised grooves and cross-hatching illustration have separate medium effects.'),
    ('L11', '현대 소품의 로카유 테두리만 보여줘. 시대 재현은 필요 없어.', ['GD07', 'GD53'], 'Motif morphology does not impose a historical room, date or class identity.'),
    ('L12', '재료·색·촬영 시점을 유지하고 패널 안의 작은 부품 관계만 개선해줘.', ['GD62', 'GD65', 'GD66'], 'Part topology cannot change lighting/viewpoint/material unless those properties are open.'),
]

CONTROLS = [
    ('N01', '필리그리처럼 보이는 평면 인쇄 문양을 연속된 판 위에 그려줘.', ['GO054','GO060'], 'Printed imitation is the requested form; it is not positive evidence of actual open wire topology.'),
    ('N02', '이 요청에서 filigree는 평면 인쇄 패턴이라는 뜻으로 쓸게.', ['GO054'], 'Requester definition wins. Local glossary cannot impose metal wire or holes.'),
    ('N03', '고딕 건축을 밝고 색채 풍부하게 보여줘.', ['GO017'], 'Gothic does not require dark palette, goth clothing, blood or a new person.'),
    ('N04', '고딕 로리타 패션을 입은 명시된 성인 모델.', ['GO089'], 'Age binding comes from requester fixture, not from the subgenre name; no sexual genre activation.'),
    ('N05', '천장의 부채꼴 리브 구조가 중심인 공간 사진.', ['GO050'], 'Environment subject guard stays in force; no fashion figure is added.'),
    ('N06', '해골 모형 하나만 있는 장식 반지의 사진.', ['GO102','GO103'], 'Memento-mori motif may be relevant; complete vanitas object set or death event is not inferred.'),
    ('N07', '장식 개수와 형태는 늘리지 말고 한 물건의 미세 홈을 읽히게 해줘.', ['GO014','GO015'], 'Micro-detail clarity does not imply maximalism, new ornaments or new props.'),
    ('N08', '관능·기괴·넌센스라는 단어가 역사적 문화 문맥에서 인용된 책 페이지.', ['GO111','GO112'], 'Quoted context is not an instruction to add sex, gore, body transformation or a new figure.'),
]

def main():
    probes = []
    for row in table('regression_pairs.tsv'):
        for side in ('a','b'):
            probes.append({'id': row['id'] + side.upper(), 'kind': 'NATURAL_LANGUAGE_MINIMAL_PAIR',
                'request_ko': row['request_' + side], 'unit_ids': row['units'].split(','),
                'candidate_review_leads': [x for x in row['draft_' + side].split(',') if x],
                'expected_distinction': row['expected_distinction'],
                'lead_policy': 'A lead is not an expected exposure claim. Verify bound owner, literal form, domain and all property effects before declaring eligibility. Wrong-owner candidates must be rejected even if their words overlap.',
                'status': 'PLANNED_NOT_RUN'})
    for id,request,drafts,expected in LOCK_PROBES:
        probes.append({'id': id, 'kind': 'PROPERTY_OWNER_AND_MEDIUM_LOCK', 'request_ko': request, 'candidate_review_leads': drafts, 'expected_distinction': expected, 'status': 'PLANNED_NOT_RUN'})
    for id,request,units,expected in CONTROLS:
        probes.append({'id': id, 'kind': 'CONTEXT_DEFINITION_AND_NEGATION_CONTROL', 'request_ko': request, 'unit_ids': units, 'expected_distinction': expected, 'status': 'PLANNED_NOT_RUN'})
    native = []
    for row in table('native_cases.tsv'):
        native.append({'id': row['id'], 'name_ko': row['name_ko'], 'request_ko': row['request_ko'],
            'unit_ids': row['units'].split(','), 'candidate_review_leads': [x for x in row['drafts'].split(',') if x],
            'all_of_required_if_bound': row['native_all_of'].split(';'),
            'reject_substitutes': row['failure_substitutes'].split(';'), 'claim_boundary': row['claim_boundary'],
            'review_scales': ['whole_frame_context','native_resolution_owner_crop_without_resampling'],
            'rule': 'All bound required predicates must be visible on the correct owner. Cropped/occluded/too-small predicates are UNOBSERVABLE_NOT_PASS. Partial required coverage is FAIL. A request trace or gate name is not pixel proof.',
            'status': 'PLANNED_NOT_RUN'})
    native[-1]['candidate_review_leads'] = []
    plan = {
        'status': 'PLANNED_NOT_RUN', 'semantic_probe_count': len(probes), 'native_case_count': len(native),
        'semantic_probes': probes, 'native_cases': native,
        'holdout_protocol': 'Reserve R14, R20, R24, R28, R29, R34 wording from positive aliases/embedding prototypes. Add independently authored Korean/English paraphrases after authoring freeze. Keep holdouts out of positive retrieval data.',
        'pipeline_checks': [
            'Authored shape, references, owner/property effect scope and narrowly selected hard variants.',
            'Stale registry/index rejection and regenerated hashes from adopted authored data.',
            'Actual eligible stable IDs exposed in request-specific v6 pack; candidate-only/advisory/required denominators separated.',
            'Selected or legitimately rejected optional candidates with complete joint effects preserved.',
            'Required literal meaning and owner relations remain in final prompt and actual runtime arguments.',
            'Original native images with all-of predicates, confounders and observability recorded.',
        ],
        'pilot': {
            'case_ids': ['H01','H02','H05','H06','H08','H09','H13','H14'],
            'arms': ['current_authored_baseline','adopted_authored_delta'], 'independent_repeats_per_arm': 3,
            'planned_image_count': 48, 'status': 'NOT_GENERATED',
            'controls': 'Same frozen requester meaning/core, provider/model/size/quality and compose protocol. Data/index corpus is the controlled delta. If a provider supplies no seed, record independent repeats, not seed-matched samples.',
            'success_reporting': 'Report exposure, selection, prompt delta, native all-of pass and intent-preservation rates separately. If the target delta is never exposed/selected/bound, do not claim a causal data improvement from pixels.',
        },
        'states': {'PASS': 'All required visible relations hold.', 'FAIL': 'A required visible relation is absent or wrong.', 'UNOBSERVABLE_NOT_PASS': 'Required relation cannot be assessed in the original pixels.', 'BLOCKED_UNSCORED': 'Generation unavailable or policy/moderation blocked; no image to score.'},
        'boundary': 'No semantic/runtime tests or image generation have been executed by this planner.',
    }
    write('REGRESSION-PLAN.json', plan)
    md = ['# 원본 픽셀 검증 계획', '', '**22개 사례 모두 PLANNED_NOT_RUN.** 먼저 8개 사례에서 현재 데이터/보강 데이터 두 arm을 각 3회 실행하는 48개 이미지 파일럿을 제안한다. 시드가 제공되지 않으면 독립 반복으로 기록한다.', '', '검증은 원래 전체 프레임과 같은 원본의 비재샘플링 crop을 함께 본다. required 관계의 부분 충족은 실패이며 가림·크롭·지나치게 작은 구조는 미통과다. 생성 차단과 픽셀 실패를 분리한다.', '']
    for case in native:
        md += [f"## {case['id']} {case['name_ko']}", '', case['request_ko'], '',
               '**모두 보여야 할 관계:** ' + '; '.join(case['all_of_required_if_bound']) + '.', '',
               '**대체 실패:** ' + '; '.join(case['reject_substitutes']) + '.', '',
               '**증거 한계:** ' + case['claim_boundary'] + '.', '']
    (HERE / 'PIXEL-QUALIFICATION-PLAN.md').write_text('\n'.join(md) + '\n')
    counts = json.loads((HERE / 'PACKAGE-COUNTS.json').read_text())
    counts.update(semantic_probes_planned=len(probes), native_cases_planned=len(native), pilot_images_planned=48, semantic_probes_executed=0)
    write('PACKAGE-COUNTS.json', counts)
    print(json.dumps({'semantic_probes_planned':len(probes), 'native_cases_planned':len(native), 'pilot_images_planned':48, 'executed':False}))

if __name__ == '__main__':
    main()
