"""Collect concrete native artifacts, human review and execution boundaries."""
import hashlib
import json
import re
from pathlib import Path
import shutil

E=Path(__file__).resolve().parent
P=Path('/Users/chasoik/Projects/image-prompt')
Q=E/'qualification'
def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

images={
 'A-mirror.png':Q/'arm-a/native_attempt_1/original.png',
 'B-orchard.png':Q/'arm-b/generated_images/orchard-boundary-20261006/native_attempt_1.png',
 'C-junction-initial.png':Q/'arm-c/generated_images/archive-lift-tissue-metal-attempt-1/native_original.png',
 'C-junction-corrected.png':Q/'arm-c/generated_images/archive-lift-tissue-metal-attempt-2/native_original.png',
}
(E/'images').mkdir(exist_ok=True)
for name,path in images.items():
 shutil.copy2(path,E/'images'/name)
 if sha(path)!=sha(E/'images'/name):raise RuntimeError('Media copy changed bytes')

prompts={
 'A.txt':Q/'arm-a/final_prompt_en.txt',
 'B.txt':Q/'arm-b/final_prompt.txt',
 'C-initial.txt':Q/'arm-c/revised-retrieval/prompt_en.txt',
 'C-corrected.txt':Q/'arm-c/correction-attempt-2/prompt_en.txt',
}
(E/'prompts').mkdir(exist_ok=True)
for name,path in prompts.items():shutil.copy2(path,E/'prompts'/name)

ref=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
(E/'reference').mkdir(exist_ok=True);shutil.copy2(ref,E/'reference/portrait.jpeg')
save(E/'ORIGINAL-REFERENCE.json',{'actual_attached_path':str(ref),'preserved_copy':str(E/'reference/portrait.jpeg'),'sha256':sha(ref),'scope':'Visible face/hair appearance for a fictional subject; no biography or identity inference.'})

cases=[
 {'arm':'A','topic':'거울 속 국소 손동작 불일치','scene':'침수된 창고에서 사진 상자를 구하는 인물','new_selected':['slot:reflection_logic:hr_uncanny_familiar_discrepancy'],'new_registered_profile_exposed':False,'selected_new_topic_predicates_passed':3,'selected_new_topic_predicates_total':3,'hard_passed':10,'hard_total':10,'technical_qualified':True,'native_calls':1,'display_image':'images/A-mirror.png','prompt':'prompts/A.txt','report':'qualification/arm-a/qualification_report.md','proof_limits':['New candidate semantics were adopted and seen; the new hvr profile itself was not exposed or qualified.','An existing compatible uncanny profile supplies the formal visual gates.','Quiet to moderate horror; exact floor level and every incidental detail remain unproven.']},
 {'arm':'B','topic':'밝은 과수원의 공동체·방문자·이동 경계','scene':'통행권을 돌려준 방문자 앞에서 공동체가 출구를 닫는 장면','new_selected':['visual-concept:hvr_profile_folk_horror_collective_boundary'],'new_registered_profile_exposed':True,'selected_new_topic_predicates_passed':3,'selected_new_topic_predicates_total':3,'hard_passed':8,'hard_total':8,'technical_qualified':True,'native_calls':1,'display_image':'images/B-orchard.png','prompt':'prompts/B.txt','report':'qualification/arm-b/qualification_report.md','proof_limits':['Initial blind retrieval missed the focal meaning; repaired development replay exposed it with identical frozen inputs.','Exact crescent, bowl material, gaze and all authorial details are not fully realized.','Moderate restrained unease; pixels do not prove every off-frame route impassable.']},
 {'arm':'C','topic':'유기 조직에서 금속으로 이어지는 접합','scene':'기록 보관소 승강기 권양 장치와 연결된 전완','new_selected':['slot:anatomical_connection:hr_bodily_fusion_shared_junction','slot:ambient_particle:hr_haze_light_volume','visual-concept:hvr_profile_bodily_fusion_shared_junction'],'new_registered_profile_exposed':True,'selected_new_topic_predicates_passed':2,'selected_new_topic_predicates_total':2,'hard_passed':6,'hard_total':7,'technical_qualified':False,'native_calls':2,'display_image':'images/C-junction-corrected.png','first_image':'images/C-junction-initial.png','prompt':'prompts/C-corrected.txt','report':'qualification/arm-c/qualification_summary.json','failed_gate':'embodiment_support_and_balance','failure_classification':'UNOBSERVABLE_NOT_PASS','proof_limits':['Initial blind retrieval missed the focal meaning; repaired development replay exposed it.','Both attempts preserve the new junction predicates; hip-to-rail compression/counterforce remains concealed or inferred.','First and corrected images both fail overall strict qualification. No gate was removed and no further generation was made.']},
]
root_review={
 'reviewer':'root independent inspection of actual saved native pixels',
 'reference_path':str(ref),'reference_sha256':sha(ref),
 'images':[{'name':name,'path':str(path),'sha256':sha(path)} for name,path in images.items()],
 'observations':{
  'A':'I inspected native and thumbnail pixels. Two real hands support the wet open carton, while the matched framed reflection has a raised open palm. Face, short dark bob, clothing and carton remain comparable. The localized reflection proposition is visible.',
  'B':'I inspected native pixels. Opposed resident rows face the controlled inner lane and near visitor, who is forward of their shared arrangement at the token stand. Dense orchard margins, stonework and a rope limit the displayed route. The intended collective boundary is visible, with restrained horror and incidental-detail limits.',
  'C_first':'I inspected native pixels. Warm skin/vein-like paths progress into bronze ridges and the same band reaches the drum. The source junction is visible. A declared hip-to-guardrail contact is not visible.',
  'C_corrected':'I inspected the corrected native pixels. Rail/post hardware was added and the junction remains intact. The actual compressed hip contact patch is still obscured; added hardware does not prove the load-bearing support relation.',
 },
 'agrees_with_agent_technical_verdicts':{'A':True,'B':True,'C_first':True,'C_corrected':True},
 'calibration':'Ordinary off-frame support need not be photographed; a consequential counterforce must be assessable. This follows the current embodiment-preflight reference. Source code validates the submitted record, not the pixels.',
 'user_judgment':'not_yet_received','fear_strength':'Qualitative reviewer impression, not a calibrated measurement or user acceptance.',
}
save(E/'ROOT-PIXEL-REVIEW.json',root_review)

counts=read(E/'FINAL-DATA-COUNTS.json')
publication=read(E/'PRIMARY-RUNTIME-PUBLICATION-FINAL.json')
live_state=read(E/'PRIMARY-LIVE-STATE.json')
summary={'status':'completed_data_integration_and_three_arm_native_testing_with_one_strict_failure','data_counts':counts,'source_publication':publication,'cases':cases,'actual_native_calls':4,'baseline_only_native_calls':0,'fallback_calls':0,'code_validation':{'focused_scope_tests':75,'full_run_passed':74,'full_run_setup_errors':1,'missing_reference_record':'Existing external maintenance records were not copied into the isolated test worktree.','reference_recheck_passed':1,'aggregate_scope_result':'75 tests passed across full run and narrow reference recheck; no test weakening or source/code change.','new_horror_guard_tests':10,'source_validator':'pass'},'frozen_inputs':read(E/'INPUT-REPLAY-INTEGRITY.json'),'user_judgment':'not_yet_received','generalization_boundary':'Three initial independently authored scenes found retrieval gaps. The replay after source repair is development verification, not a fresh blind holdout. These cases do not establish native qualification for every one of the 155 authored profiles.','process_deviation':read(E/'INDEPENDENCE-RECORD.json')['envelope_delivery_note']}
summary['publication_scope']='source_publication records the actual qualification snapshot; current_primary_state records the newer validated live publication after unrelated concurrent edits.'
summary['current_primary_state']=live_state
summary['code_validation']['current_primary_horror_guard_recheck']={'tests':10,'passed':10,'log':'primary-live-horror-recheck.log','counts_as_additional_unique_tests':False}
summary['code_validation']['current_primary_source_validator']='pass'
save(E/'RESULT.json',summary)
d=read(E/'ADOPTION-MAP.json');d['counts']['native_rendered_units']=4;d['native_qualification_summary']={'central_cases':3,'new_profile_native_cases':2,'new_candidate_native_case':1,'auxiliary_candidate_observed':['hr_haze_light_volume'],'overall_passed_cases':2,'overall_failed_cases':1,'actual_calls':4};save(E/'ADOPTION-MAP.json',d)

readme='''# 호러 데이터 반영과 독립 이미지 검증\n\n시각 의미와 후보 데이터를 주 작업 폴더에 반영하고 현재 실행용 버전으로 게시했다. 세 독립 에이전트가 첨부 사진을 활용해 서로 다른 복잡한 장면을 작성·생성했고, 원본 픽셀을 검증했다. 핵심 주제는 세 장면에서 확인됐다. 전체 필수 검증은 A/B 통과, C 미통과다.\n\n## 실제 반영\n\n- 새 후보 155개, 새 시각 의미 프로필 155개, 선택형 묶음 11개.\n- 전체 후보 10,403개, 시각 의미 프로필 2,236개, 묶음 1,007개. 두 인덱스를 현재 데이터에 맞춰 갱신했다.\n- 기존 유사 항목 21개를 완전한 동의어로 치환하지 않았다. 조사상의 조합 예시 6개는 선택형 묶음에 대응한다. 나머지 68개는 비시각적 맥락·소리·시간 변화·비평 주제·미검증 문화 변형으로 보존했다. 민속 변형 6개와 이를 요구하는 묶음 1개는 보류했다.\n- 후보에는 한국어 해석, 영어의 관찰 가능한 전체 명제, 구성 요소, 관계, 속성 범위 및 혼동 경계를 넣었다. 장르명이나 근접 검색이 사용자 요구를 새로 만들지 않는다. 선택하면 모든 비교 대상과 구성 요소를 보존해야 한다.\n\n[반영 대응표](ADOPTION-MAP.json) · [실행 버전](PRIMARY-RUNTIME-PUBLICATION-FINAL.json) · [소스 해시](INTEGRATED-SOURCE-HASHES-FINAL.json)\n\n## 검색에서 발견한 문제와 보완\n\n첫 독립 검색에서 A는 새 거울 후보를 찾았지만 B/C는 해당 공동체 경계·조직/금속 접합 프로필을 찾지 못했다. 추가 인물·물체를 주 피사체 변경으로 너무 넓게 선언한 속성 범위와, 구성 요소당 한 개의 긴 표현만 허용한 발견 어휘가 원인이었다. 실제 변경 대상의 범위와 15개 주요 관계의 일반적인 대체 표현을 보완했다. 강제 활성화 용어, 선택 후 모든 증거 요건, 원본 픽셀 기준은 그대로 유지했다.\n\n요청·코어·창작 설정을 바꾸지 않고 새 게시 버전으로 다시 검색하자 B/C의 핵심 프로필이 노출됐다. 초기 실패도 보존했다. 이 재실행은 보완 후 개발 검증이며 새 블라인드 표본으로 주장하지 않는다.\n\n[초기 보완 기록](ADMISSION-REVISION.initial.json) · [추가 소유자 범위 기록](ADMISSION-REVISION.json) · [입력 바이트 동일성](INPUT-REPLAY-INTEGRITY.json) · [독립성 기록](INDEPENDENCE-RECORD.json)\n\n## 원본 이미지 결과\n\n| 테스트 | 이번 추가 데이터의 핵심 관계 | 필수 픽셀 검증 | 전체 기술 판정 |\n|---|---|---|---|\n| A — 침수 창고와 거울 | 실제 두 손의 상자 지지 / 반사 속 펼친 손의 불일치, 새 후보 구성 요소 3/3 | 10/10 | 통과 |\n| B — 밝은 과수원의 공동체 | 공동체의 안쪽 경계 / 바깥 방문자 / 제한된 이동 경로, 새 프로필 3/3 | 8/8 | 통과 |\n| C — 승강기와 신체·금속 접합 | 같은 몸에서 피부·금속 구조가 연속, 새 프로필 2/2 | 첫 결과와 교정본 모두 6/7 | 실패 |\n\nC는 골반이 가드레일에 눌려 지탱되는 접촉을 확인할 수 없어 `UNOBSERVABLE_NOT_PASS`다. 한 번 교정해 지지물을 추가했지만 실제 접촉은 계속 가려졌다. 두 시도의 원본·감사·ledger를 보존했다.\n\nA는 새 후보를 실제로 채택했지만 새 `hvr_profile_`는 노출되지 않았다. 기존의 호환되는 언캐니 프로필이 정식 픽셀 기준을 제공했고, 새 후보의 세 구성 요소와 관계는 별도로 확인했다. B/C는 새 시각 의미 프로필의 전체 계약을 실제로 선택했다.\n\n![A — 거울의 손동작 불일치](images/A-mirror.png)\n\n[A 프롬프트](prompts/A.txt) · [A 전체 증거](qualification/arm-a/qualification_report.md)\n\n![B — 공동체와 이동 경계](images/B-orchard.png)\n\n[B 프롬프트](prompts/B.txt) · [B 전체 증거](qualification/arm-b/qualification_report.md)\n\n![C — 연속된 조직/금속 접합, 교정본](images/C-junction-corrected.png)\n\n[C 교정 프롬프트](prompts/C-corrected.txt) · [C 첫 이미지](images/C-junction-initial.png) · [C 전체 증거](qualification/arm-c/qualification_summary.json) · [두 시도 비교](qualification/arm-c/correction-attempt-2/attempt_comparison.json)\n\n## 검증 범위\n\n실제 네이티브 호출은 총 4회(A 1, B 1, C 2)이며, 반환된 실제 파일을 같은 바이트로 보존했다. 첨부 사진 SHA256은 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이고 얼굴·머리 외관을 참고했다. 피사체의 설정과 사건은 창작이다. 각 팔은 데이터 열람 전에 독립 장면과 입력을 동결했으며 다른 팔의 장면을 읽지 않았다. 요청 봉투는 에이전트 생성 후 전달됐지만 전원이 작성 전에 기다렸다. 이 순서 차이는 독립성 기록에 명시했다.\n\n입력 감사와 코드 검증은 픽셀 판단과 구분했다. A/B의 픽셀 감사 종료 코드 1은 사용자 평가 대기를 포함한 도구 계약이며, 기록된 기술 자격은 충족한다. C는 실제 필수 게이트 미충족이다. 사용자 판단은 세 경우 모두 `not_yet_received`다. 공포 강도는 검토자의 정성 평가로 A/B의 인상은 절제된 수준이다. 그릇 재질·정확한 군중 배열·시선·층수·브레이크 미끄러짐 등 모든 서사 세부가 완전히 구현됐다고 주장하지 않는다.\n\n후보 계약·시각 의미·실행 버전 신선도·새 호러 데이터에 대한 75개 테스트 범위를 확인했다. 전체 실행에서 74개 통과, 기존 유지보수 근거 파일 누락에 따른 실행 환경 오류 1개가 있었으며 해당 파일을 복사한 후 같은 테스트가 통과했다. 새 호러 전용 테스트는 10개이며 구성 요소 누락·잘못된 비교 대상·광범위 용어의 강제 활성화·잠긴 속성 침범을 검증한다. 소스 검증도 통과했다.\n\n[전체 결과 JSON](RESULT.json) · [루트 원본 픽셀 검토](ROOT-PIXEL-REVIEW.json) · [회귀 실행](focused-regression-final.log) · [누락 파일 재확인](maintenance-reference-recheck.log) · [새 호러 검증](horror-data-tests-final.log) · [소스 검증](source-validation-final.log)\n\n현재 생성 사례는 세 핵심 주제와 보조 안개 관계까지 확인한다. 다른 151개 시각 해석의 네이티브 판정은 후속 검증 범위다. 기존 조사에서 계획한 22개 픽셀 그룹 전체가 완료됐다는 의미로 해석하지 않는다. 고유한 요청과 더 단순한 비교 구도로 새 표본을 작성해 확장하고, C는 지지 접촉을 가리지 않는 시점으로 물리적 관계부터 확인하는 것이 다음 단계다.\n'''
readme=readme.replace('[실행 버전](PRIMARY-RUNTIME-PUBLICATION-FINAL.json)', '[이미지 검증에 사용한 게시 버전](PRIMARY-RUNTIME-PUBLICATION-FINAL.json)')
readme=readme.replace('## 검색에서 발견한 문제와 보완', '''## 최종 실행 버전 확인

이미지 검증 기록은 실제 사용한 고정 버전 `d947d6b6`에 연결돼 있다. 반영 후 다른 작업에서 기존 색 관계·의복 표면 데이터 등 15개 파일이 변경됐으며 이 변경은 보존했다. 현재 주 작업 폴더는 새 게시 버전 `11a2c533`(revision 11)으로 실행되고, 현재 소스와 실행 버전의 일치 및 소스 검증을 확인했다. 이번 호러 소스 두 파일과 `SKILL.md`는 이미지 검증에 사용한 버전과 바이트가 같다. 현재 주 작업 폴더에서도 호러 전용 테스트 10개가 모두 통과했다. 이전 이미지의 검색 영수증을 새 버전으로 다시 해석하지 않았다.

[현재 주 작업 폴더 상태](PRIMARY-LIVE-STATE.json) · [최종 전달 확인](DELIVERY-VALIDATION.json) · [현재 소스 검증](primary-live-source-validation.log) · [현재 호러 테스트 재확인](primary-live-horror-recheck.log)

## 검색에서 발견한 문제와 보완''')
target=P/'docs/research-evidence/photo-prompt/horror-integration-20261006'
readme=re.sub(r'\]\(([^)]+)\)',lambda m: ']('+str(target/m.group(1))+')' if not m.group(1).startswith(('/', 'https://', 'http://')) else m.group(0),readme)
(E/'README.md').write_text(readme,encoding='utf-8')

# Source/receipt paths inside historical records intentionally stay bound to the
# actual worker/worktree and its immutable store. The primary copy is a mirror.
shutil.copytree(E,target,dirs_exist_ok=True,ignore=shutil.ignore_patterns('runtime-store','__pycache__','*.pyc'))
records=[]
for path in E.rglob('*'):
 if not path.is_file() or 'runtime-store' in path.relative_to(E).parts or '__pycache__' in path.parts or path.suffix=='.pyc':continue
 relative=path.relative_to(E);destination=target/relative
 if sha(path)!=sha(destination):raise RuntimeError('Evidence mirror mismatch: '+str(relative))
 records.append({'relative_path':str(relative),'sha256':sha(path)})
save(target/'EVIDENCE-MIRROR.json',{'source':str(E),'primary_copy':str(target),'immutable_runtime_store':str(E/'runtime-store'),'historical_record_paths':'preserved, not rewritten','files':records})
print(json.dumps({'primary_report':str(target/'README.md'),'mirrored_files':len(records),'native_calls':4,'technical_case_passes':2,'technical_case_failures':1}))
