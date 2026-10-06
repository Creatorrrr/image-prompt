"""Consolidate independent evidence without changing frozen arm artifacts."""
from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone, timedelta

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
REL=HERE.relative_to(ROOT)
RUNS=HERE/'independent-runs'
def read(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def link(label,path):return f'[{label}]({PRIMARY/path.relative_to(ROOT)})'

adoption=read(HERE/'ADOPTION-MANIFEST.json')
index=read(HERE/'INDEX-REPORT.json')
cases=[
 {'arm':'arm1','label_ko':'모델 선박 포장 작업 · 금속 반사와 보라색 직물',
  'summary_path':RUNS/'arm1/arm_summary.json',
  'image_path':RUNS/'arm1/generated_images/boat-material-ownership-attempt2/native.png',
  'prompt_path':RUNS/'arm1/corrected-run/composed_prompt.json',
  'pack_path':RUNS/'arm1/corrected-run/candidate_pack.json',
  'trace_path':RUNS/'arm1/corrected-run/new_data_adoption_trace.json',
  'audit_path':RUNS/'arm1/corrected-run/moe_render_audit.json',
  'test_result_path':RUNS/'arm1/corrected-run/pixel_review.json',
  'ledger_path':RUNS/'arm1/image_runs.ndjson','selected_new_profiles':['pa_bounded_metal_trim'],
  'new_profile_gates':{'passed':2,'required':2},'synthetic_case_gates':{'passed':5,'required':5,'status':'PASS'},
  'new_data_end_to_end':'PASS_selected_visual_profile','image_calls':2,
  'peer_observation':'Gold-colored highlights remain on narrow boat railings, plaque fittings and box hinges, separate from the matte violet apron. Smooth violet hull glints differ from diffuse linen folds. The original control already contained gold details; no causal improvement is established.'},
 {'arm':'arm2','label_ko':'해변 천문대 문턱 정비 · 따뜻한 실내광과 푸른 외부광',
  'summary_path':RUNS/'arm2/arm2_completion_report.json',
  'image_path':RUNS/'arm2/generated_images/observatory-threshold-native-attempt-1/image.png',
  'prompt_path':RUNS/'arm2/prompt_en.generation3.txt',
  'pack_path':RUNS/'arm2/candidate_pack.generation3.json',
  'trace_path':RUNS/'arm2/palette_selection_and_coverage.generation3.json',
  'audit_path':RUNS/'arm2/moe_render_review_audit.json',
  'test_result_path':RUNS/'arm2/native_test_case_result.json',
  'ledger_path':RUNS/'arm2/image_runs.ndjson','selected_new_profiles':['pa_local_color_under_separate_lights'],
  'new_profile_gates':{'passed':3,'required':3},'synthetic_case_gates':{'passed':7,'required':8,'status':'FAIL_partial'},
  'new_data_end_to_end':'PASS_selected_visual_profile','image_calls':1,
  'peer_observation':'Warm lamp light is visible on inner floor, face and left garment surfaces; blue exterior light appears on the outer floor, door frame and hair rim. Intrinsic knit stripes and red object regions remain distinct. The small apron tab does not expose assessable weave. The outside wetness and changed stone joints also limit attribution of floor color solely to illumination.'},
 {'arm':'arm3','label_ko':'온실 차광막 수선 확인 · 같은 천의 교차선과 작은 빨강 예외',
  'summary_path':RUNS/'arm3/qualification_summary.final.json',
  'image_path':RUNS/'arm3/generated_images/greenhouse-grid-tab-native-2/arm3.png',
  'prompt_path':RUNS/'arm3/attempt-2/final_prompt.txt',
  'pack_path':RUNS/'arm3/candidate_pack.generation3.json',
  'trace_path':RUNS/'arm3/integration_trace.json',
  'audit_path':RUNS/'arm3/attempt-2/moe_render_audit.json',
  'test_result_path':RUNS/'arm3/attempt-2/pixel_test_review.json',
  'ledger_path':RUNS/'arm3/ledger/image_runs.ndjson','selected_new_profiles':[],
  'new_profile_gates':{'passed':0,'required':0,'status':'not_selected'},'synthetic_case_gates':{'passed':7,'required':8,'status':'FAIL_partial'},
  'new_data_end_to_end':'FAIL_coverage_gap_no_new_selection','image_calls':2,
  'peer_observation':'The original tab had an internal white X and failed the plain-face criterion on strict peer review. The second render removes the X but places the solid red rectangle on the curtain face above the hem rather than at the lower corner. Same-surface blue crossing lines and broad yellow ground remain visible. No cross-attempt composite PASS is permitted.'},
]

for case in cases:
    a=RUNS/case['arm']
    case['random_seed']=read(a/'randomization.json').get('seed', read(a/'test_case.json').get('seed'))
    case['image_sha256']=sha(case['image_path'])
    case['primary_image_copy']=str(PRIMARY/case['image_path'].relative_to(ROOT))
    ledger=[json.loads(line) for line in case['ledger_path'].read_text().splitlines() if line.strip()]
    assert len(ledger)==case['image_calls']
    assert max(row['image_call_count'] for row in ledger)==case['image_calls']
    assert all(row['skill_sha256']=='7dc4220b1dd784abe8ed7c93b84612d0472591c7753f0dcfda0c88da229ac857' for row in ledger)
    assert all(row['cross_arm_inputs_used'] is False for row in ledger)
    assert all(row['reference_sha256']==['048adbd3e4343a3725fec6aa0455aa1f367878560bc15d4493a18fde1ce8604c'] for row in ledger)
    audit=read(case['audit_path'])
    assert not audit['schema_failures'] and not audit['failed_hard_gates']
    assert audit['technical_qualified'] is True and audit['representative_eligible'] is False
    case['formal_hard_gates']={'passed':audit['required_hard_gate_count'],'required':audit['required_hard_gate_count'],'status':'PASS'}
    case['user_judgment']=audit['user_judgment']
    case['ordinary_new_candidates_selected']=0
    for key,value in list(case.items()):
        if isinstance(value,Path):case[key]=str(value)

report={
 'schema_version':'color-palette-integration-qualification/v1',
 'completed_at_kst':datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=9))).isoformat(),
 'primary_repository':str(PRIMARY),'isolated_worktree':str(ROOT),
 'adoption':{k:v for k,v in adoption.items() if k!='rows'},'index':index,
 'software_checks':{'scoped':{'tests':48,'passed':48,'errors':0},'contracts':{'tests':93,'passed':92,'errors':1,'preexisting_error':'clothing maintenance record lacks maintenance_only, reproduced without the new palette source'},
                    'full_suite':'not_passed; fail-fast historical-source mismatch also occurs for the pre-task manifest; interrupted earlier broad run preserved'},
 'native_image_calls':sum(c['image_calls'] for c in cases),'independent_arms':3,
 'selected_new_visual_profile_pixel_success_arms':2,
 'new_ordinary_candidate_selection_arms':0,
 'complete_synthetic_scenario_pass_arms':1,
 'new_visual_profile_gates_exercised':5,'new_visual_profile_gates_authored':30,
 'partial_is_fail':True,'cross_attempt_composite_pass':False,'user_acceptance':'not_yet_received',
 'improvement_claim':False,
 'final_source_revision_boundary':read(HERE/'FINAL-CARRIER-SCOPE-REPORT.json'),
 'experimental_boundary':'Agent-authored synthetic randomized scenarios, not user definitions or blind evidence of general improvement. Core/envelope/controls were frozen before candidate access. Property-scope and received-light coverage were corrected during evaluation, with every old artifact retained. Image tool seed is not controlled.',
 'remaining_coverage_and_fidelity':[
  'No new ordinary pal_app_ slot candidate was selected in these three cases. Existence/indexing does not qualify their image effect.',
  'The same-hue similarly narrow crossing-grid variant was not represented by a fitting new optional profile in the exposed bounded pack. The agent declined band/global-grade alternatives.',
  'Small textile accents can be too small to verify native weave; arm2 remains 7/8.',
  'A localized red rectangle is not equivalent to a corner replacement tab; arm3 remains 7/8 after one bounded follow-up.',
  'The retained historical regression system and old clothing maintenance record need separate reconciliation; fixtures were not weakened.',
  'Only five selected new profile gates were pixel-tested; the remaining authored gates and held claims are not rendered-qualified.'
 ],'cases':cases,
 'next_validation_plan':[
  {'work':'Crossing-grid variants','method':'Add reviewed same-hue/equal-width and unequal-width siblings only where meanings differ; preserve current narrower IDs. Freeze new multilingual full-scene holdouts before authoring aliases. Test same-carrier topology versus separate objects, stripe-only and projected-light confounds.'},
  {'work':'Ordinary palette candidate reach','method':'Diagnose frozen slot-focus grounding, palette-owner effect compatibility and bounded candidate exposure using the same saved cores. Add positive/adjacent/negative exposure cases before changing rank or source opt-in; do not force every palette into every scene.'},
  {'work':'Local textile and corner ownership','method':'Predeclare an assessable accent size and corner-to-tab topology while preserving qualitative area order. Review one saved image against the whole conjunction; keep each failed attempt and preserve user-owned reference constraints.'},
  {'work':'Held cultural/function/data claims','method':'Acquire scene-specific/primary source evidence and separate visible color application from provenance, jurisdiction and numerical mapping. Do not activate a broad label as a hard visual duty.'},
  {'work':'Comparative quality','method':'A future matched A/B/C render design must use the same frozen core and controls, retain raw attempts and obtain actual user preference. The current five renders establish no causal quality improvement.'}
 ]}
write(HERE/'QUALIFICATION-REPORT.json',report)
write(HERE/'ROOT-PIXEL-REVIEW.json',{'schema_version':'color-palette-coordinator-native-review/v1','reviewer':'root','reviewed_native_files':[{'arm':c['arm'],'image_path':c['image_path'],'image_sha256':c['image_sha256'],'observations':c['peer_observation'],'new_data_status':c['new_data_end_to_end'],'synthetic_status':c['synthetic_case_gates']} for c in cases], 'user_acceptance':'not_yet_received'})

text=[
 '# 배색 데이터 반영과 독립 이미지 테스트 결과',
 '',
 '2026-10-06 착수 · 2026-10-07 완료. 주 작업 폴더에 활성 데이터와 두 인덱스를 반영했습니다. 독립 에이전트 3개가 첨부 사진을 활용해 네이티브 이미지를 총 5회 생성했습니다.',
 '',
 '**새 시각 프로필의 검색 → 선택 → 이미지 표현은 2개 컨셉에서 확인했습니다. 합성 테스트 전체 통과는 1개이며, 나머지 2개에는 필수 세부 조건 실패가 남았습니다.** 일반 `pal_app_` 후보는 세 컨셉에서 채택되지 않았으므로 이미지 효과가 검증됐다고 보고하지 않습니다.',
 '',
 '## 활성 데이터',
 '',
 f"연구 카드 100개 중 37개를 좁은 후보로 추가하고, 52개는 기존 관계 후보 23개의 선택적 문맥으로 보강했습니다. 새 시각 프로필은 13개, opt-in 이미지 게이트는 30개입니다. 문화·영화의 특정 사례·표지 기능·수치 데이터의 11개 주장은 보류 기록을 유지했습니다.",
 '',
 link('후보 원본',ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_palette_applications_extension.json')+' · '+link('시각 의미 원본',ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_palette_applications.json')+' · '+link('100개 채택/보류 대조',HERE/'ADOPTION-MANIFEST.json'),
 '',
 '팔레트 이름은 선택적 검색에 쓰입니다. 실제 요청의 완전한 관계 또는 적합한 명시적 선택만 필수 표현을 만듭니다. 속성 범위가 `*`였을 때 참조 얼굴/머리 보존 조건과 무관한 색 선택까지 차단되는 문제를 발견해, 실제 표면·의상·배경·광원·보정 경로로 좁혔습니다. parent/cross-dimension 잠금 검사는 유지했습니다. 고정된 연구 예시 물체를 사용자 요구나 실제 core owner로 위장하지 않았습니다.',
 '',
 '이미지 생성 후 컵/배경 그라데이션의 실제 `surface.local_color` 잠금 경로를 추가 보완했습니다. 생성에 쓰인 generation 3와 마지막 활성 generation은 구분해 보존했습니다. 세 이미지에서 선택한 금속/수신 광 프로필의 원문·효과·게이트가 동일함을 직렬화 해시로 확인했습니다. 마지막에 수정한 미선택 컵/그라데이션 항목은 소프트웨어 잠금 검사만 통과했고 픽셀 검증은 수행하지 않았습니다.',
 '',
 f"semantic index는 {index['semantic']['current_entries']:,}개, visual index는 {index['visual']['current_entries']:,}개입니다. 기존 {index['semantic']['unchanged_text_and_vector']:,}개 의미 벡터와 {index['visual']['unchanged_text_and_vector']:,}개 시각 벡터의 문장/수치가 그대로 유지됐으며 삭제된 entry/shard는 없습니다. provider/model/dimensions는 Gemini / gemini-embedding-2 / 768입니다.",
 '',
 '## 독립 테스트',
 '',
 '설치된 최신 스킬과 같은 SHA-256 원문, 동일 사진, byte-exact 사용자 envelope를 고정했습니다. 각 에이전트는 별도 RNG seed로 독립 컨셉을 선택하고 core/controls/embodiment/중립 feature selection을 먼저 동결했습니다. 다른 arm의 컨셉·프롬프트·이미지를 입력으로 사용하지 않았다는 선언과 해시를 보존했습니다. 수정된 데이터로 replay할 때에도 이 입력 해시는 유지됐습니다. 선언과 해시는 절차 증거이며 모델 내부 지식의 독립성을 수학적으로 증명하지는 않습니다.',
 '',
 '|컨셉|새 데이터의 실제 선택/픽셀|합성 조건|실제 호출|',
 '|---|---|---|---|',
 '|모델 선박 포장 · 반사 금속/보라 직물|pa_bounded_metal_trim · 2/2 PASS|5/5 PASS|2|',
 '|천문대 문턱 정비 · 따뜻한 실내/푸른 외부|pa_local_color_under_separate_lights · 3/3 PASS|7/8 FAIL · 작은 빨강 탭의 직조 불명확|1|',
 '|온실 차광막 · 교차선/작은 빨강 예외|노출 2개, 선택 0개 · 통합 coverage gap|7/8 FAIL · 모서리 탭 대신 앞면 패치|2|',
 '',
 '최종 pack/composed/runtime 감사는 세 arm 모두 PASS입니다. 저장 이미지의 formal embodiment/선택된 opt-in 게이트는 각각 7/7, 8/8, 5/5였으며, 이 수치를 별도 합성 시나리오의 전체 성공과 혼동하지 않았습니다. 사용자 판단은 모두 `not_yet_received`이고 대표 승격은 false입니다. 일부 moe audit exit 1은 사용자 판단 대기 상태이며, schema failure/failed formal gate는 0개입니다.',
 '',
 '각각의 이미지가 갖춘 조건만 판정했습니다. 첫 사진의 조건과 두 번째 사진의 조건을 합쳐 PASS로 만들지 않았습니다. 온실 첫 사진의 내부 X 스티치는 엄격한 peer review에서 실패로 정정했고 원래 리뷰도 역사 기록으로 보존했습니다. 후속 사진에서는 X가 사라졌지만 위치가 어긋나 여전히 FAIL입니다.',
 '']
for c in cases:
 text += ['### '+c['label_ko'],'',
          link('최종 프롬프트',Path(c['prompt_path']))+' · '+link('테스트케이스',RUNS/c['arm']/'test_case.json')+' · '+link('검색/선택/효과/owner 추적',Path(c['trace_path']))+' · '+link('픽셀 결과',Path(c['test_result_path']))+' · '+link('arm 전체 결과',Path(c['summary_path'])),'',
          '!['+c['label_ko']+']('+c['primary_image_copy']+')','']
text += ['## 검증과 한계','',
         '변경 관련 48개 검사는 모두 통과했습니다. 검색·core·후보·인덱스 계약 93개에서는 92개 통과, 기존 의복 maintenance record의 `maintenance_only` 누락 1개 오류가 재현됐습니다. 새 팔레트 원본을 제외한 원래 inventory에서도 같은 오류가 발생함을 기록했습니다.',
         '',
         '전체 회귀의 fail-fast 확인은 역사 V24–V31 source 보존 경계에서 중단됐습니다. 작업 전 manifest bytes를 최초 SHA와 일치하게 복원해 대조했으며 이 원래 manifest도 이전 보존 체계에 승인되지 않습니다. 기존 dirty 상태의 불일치로 구분하고 역사 fixture나 의복 기록을 임의로 고치지 않았습니다. 전체 suite PASS는 확인하지 않았습니다.',
         '',
         '첫 선박 control에도 골드 디테일이 있었습니다. 이미지 도구의 seed를 통제하지 않았고 A/B/C 반복 비교·사용자 선호 판단을 수행하지 않았으므로 데이터만의 인과적 개선이나 일반화된 품질 향상은 주장하지 않습니다. HEX는 연구의 sRGB 근삿값이고 사진 픽셀의 정확한 색이나 실제 금속/도자기의 화학적 조성·인물의 실제 정체성을 검증하지 않습니다.',
         '',
         link('현재 원본/인덱스 무결성',HERE/'FINAL-SOURCE-INTEGRITY.json')+' · '+link('인덱스 재생성/벡터 보존',HERE/'INDEX-REPORT.json')+' · '+link('기존 오류 재현',HERE/'BASELINE-FAILURE.json')+' · '+link('역사 source 기존 불일치 대조',HERE/'HISTORICAL-BASELINE-DIAGNOSTIC.json')+' · '+link('전체 구조화 결과',HERE/'QUALIFICATION-REPORT.json'),
         '',
         '## 결과를 반영한 다음 검증 계획','',
         '1. 같은 색/유사 선폭의 교차 그리드와 불균등 체크를 다른 변형으로 다룹니다. 기존 좁은 ID를 느슨하게 바꾸지 않고, 같은 carrier/교차 방향/폭·간격이 각각 읽히는 변형을 검토합니다. 새 구어체 holdout은 데이터 수정 전에 동결합니다.',
         '2. 일반 팔레트 후보의 slot-focus grounding, 실제 owner/property 적합성, 제한된 후보 노출을 따로 조사합니다. 같은 저장 core로 positive/adjacent/negative 노출 검사를 먼저 만들고, 부적합한 팔레트를 모든 복잡한 장면에 강제로 노출하지 않습니다.',
         '3. 작은 직물 강조는 native에서 확인 가능한 크기와 면적 역할을 사전 조정합니다. 모서리 탭은 모서리·연결·탭 자체의 동시 조건으로 판단하며 단순 빨강 패치로 대체하지 않습니다.',
         '4. 보류 11개는 구체 장면/primary source/관할/데이터 타입을 보충한 뒤 가시적 색 응용과 출처·기능·수치 의미를 분리합니다.',
         '5. 품질 개선 비교가 필요할 때 같은 core/controls로 A/B/C와 반복 샘플을 설계하고 실제 사용자 선호를 별도로 받습니다. 이번 결과는 해당 비교를 대신하지 않습니다.',
         '',
         '주 작업 폴더의 기존 변경과 오래된 shard는 보존했습니다. commit/push/PR은 생성하지 않았습니다. 동결 arm JSON의 worktree 경로는 hash-bound 원문 보존을 위해 그대로 두었고, 이 보고서의 링크는 주 작업 폴더에 복사한 동일 바이트 결과를 가리킵니다.']
(HERE/'README.md').write_text('\n'.join(text)+'\n')
print(json.dumps({'arms':3,'native_calls':report['native_image_calls'],'new_profile_pixel_success_arms':2,'full_synthetic_pass_arms':1,'report':str(HERE/'README.md')},ensure_ascii=False))
