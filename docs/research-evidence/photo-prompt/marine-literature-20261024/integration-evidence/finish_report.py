from pathlib import Path
import json,hashlib,subprocess
O=Path(__file__).resolve().parent;Q=O.parent;R=O.parents[4];S=R/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(Path(p).read_bytes())
images=read(O/'image-tests-summary.json');registration=read(O/'registered-data-verification.json');assert registration['status']=='pass'
selected=read(S/'retrieval-runtime.json');dedicated=read(O/'install-copy.json');sealed=[read(O/d/'successor.json') for d in ['union-release','final-release']]
state={'schema':'marine-literature-integration-final-state/v1','source_registration':'PASS','working_dictionary_validation':read(O/'working-dictionary-validation.json'),'working_source_and_layout_binding':registration,'dedicated_test_install':dedicated,'image_tests':images,'default_runtime_promotion':'HELD_NOT_SELECTED','default_config_written_by_this_task':False,'current_default_config_observed':selected,'sealed_integration_candidates_not_selected':sealed,'disposition_reason':['Current independent images adopt0new visual candidates; new-data pixel effect is NOT_DEMONSTRATED.','All3managed technical qualifications are fail; no native approval granted.','Concurrent selected releases advanced during integration. Their data and selector are preserved; do not overwrite with a stale successor.'],'native_approval_granted':False,'semantic_duplicate_absence_claimed':False,'user_acceptance':'PENDING','commit_performed':False,'push_performed':False,'head_at_final_observation':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()}
current_manifest=read(Path(dedicated['store'])/'generations'/selected['native_generation_id']/'assets/photo_candidate_corpus_manifest.json')
state['current_default_has_marine_module']=any(m['file']=='photo_candidate_marine_literature_20261024.json' for m in current_manifest['modules'])
(O/'FINAL-STATE.json').write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
rows={x['arm']:x for x in images['cases']}
text=f'''# 해병문학 데이터 반영 및 독립 이미지 검증 결과

2026-10-24 KST · **소스·파생 인덱스 반영 완료 / 테스트용 실행본 설치 완료 / 생성3회 완료 / 기본 실행본 승격 보류**

신규 데이터가 이미지에 실제로 적용됐다는 검증은 **0/3으로 미입증**이다. 세 arm의 신규 후보 채택이 모두0이었다. 그림에 군대 부조리 풍자가 나타나는 것과, 이번 신규 데이터가 그 결과를 만들었다는 주장은 별개다. 세 이미지의 managed 기록은 유효하지만 최종 `technical_qualification=fail`이며, 사용자 수락은 아직 없다.

## 실제 데이터 변경

- 시각 의미 카드96개, 원래 입력247행과 출처20개를 보존했다. 관찰 구성요소·owner/carrier/target 방향 관계·혼동 경계·필수 관찰 그룹·비시각 주장 한계를 함께 둔다.
- 긍정 시각 후보87개를 새 CID로 등록하고, 기존 경례·뒷짐·로우앵글3개를 재사용한다. 선택형 binding166개를 추가했다.
- 원래 입력247행은 각각 diagnostic 레코드로도 보존했다. 민감한30행의 원뜻도 삭제하지 않는다. diagnostic247개는 긍정 index에 들어가지 않는다.
- 순서형 T001–T004, 문패 V064, 내용물 미확정 메뉴 V074는 긍정 후보로 승격하지 않았다. 그림 한 장으로 소리·시간·원인·강요·실제 소속·물질 정체를 확정하지 않는다.
- 기존 후보의 조건·효과를 약화하거나 인물 이름/장르명을 고정된 외형 묶음으로 바꾸지 않았다. 의미 중복이 전혀 없다는 주장도 하지 않는다. 연구 graph는 검토 메타데이터이며 전체96개가 자동 관계 검증이나 픽셀 qualification을 받은 것은 아니다.

등록 파일:

- [시각 후보+문맥 레코드]({S/'assets/photo_candidate_marine_literature_20261024.json'})
- [슬롯 연결]({S/'assets/photo_candidate_marine_literature_bindings_20261024.json'})
- [시각 의미·입력 경로·출처]({S/'assets/photo_marine_literature_semantics_20261024.json'})

새334개 레코드와166개 연결은 등록 원본과 정확히 같고, 보호 기준선을 다시 잡은 뒤 보호한 기존 모듈의 내용 변동은0개였다. 소스 manifest에는 새 후보·연결 모듈2개만 추가했다. working source118개 파일과 파생 index의 closure도 동일하다. 전체 working 후보22,849개·binding17,760개에 대한 dictionary 검증은 오류0이었다. 이 전체 숫자에는 다른 주제의 기존 작업도 포함된다. 확인 후 다른 작업을 되돌리거나 stage/commit/push하지 않았다.

## 실행본과 설치 범위

원래 working source는 v3이고 선택된 관리 실행본은 v4여서 둘을 섞지 않았다. 각 새 레코드의 literal 소유·원문을 정확히 변환해 native snapshot과 왕복 비교했고, 기존 코드·source·catalog·policy·binding·호환 벡터를 보존했다. 모델/recipe 이름만 바꿔 벡터를 재사용하지 않았다.

실제 테스트 설치본:

- H-F2 generation: `{dedicated['generation_id']}`
- native dependency: `7907fa1dcf32e7a0915a7f1a2833408f3bef41f62ee2371cdafbf44657ac0e74`
- store: `{dedicated['store']}`
- 긍정20,710 CID /20,712 RID. 원래 소스21,706개 +새334개. 신규 시각87개 모두 index에 있으며 diagnostic 누출0개다.
- 실제 설치본의 model checksum, deployed `Generation`·`RuntimeSnapshotProvider`, pinned Python/NumPy·실제 recorder를 검증했다. 새 실행은 explicit store/generation에 고정했다.

동시에 기본 선택본에 campus·romcom·mecha 자료가 추가되는 상황을 관찰했다. 이를 덮지 않도록 두 통합 후보도 별도 제작·봉인·83개 질의 검증까지 마쳤으나, 기본 선택본으로 활성화하지 않았다. 이번 작업에서 기본 selector를 쓴 횟수는0이다. **현재 기본 선택본은 신규 해병문학 자료의 운영 승격 증거가 아니며, 신규 자료는 working source/index와 위 테스트용 설치본에 반영된 상태다.** 원본 픽셀 qualification 없이 기본 실행본에 승격했다고 보고하지 않는다.

상태별 실제 근거는 [FINAL-STATE.json](integration-evidence/FINAL-STATE.json)과 각 install/build/qualification 기록에 있다.

## 검색과 독립 장면의 차이

한영80개 +일반 대조3개를 실제 실행했다. 테스트 설치본에서 특정 카드가 기대된64개 중 top-8은58개(90.625%), top-32는61개다. 일부 경계 비교 질의도 포함되어 있으므로 의미 정확도나 독립 holdout 점수로 해석하지 않는다. 제안한95% 목표는 달성했다고 표시하지 않는다. 별도 통합 후보의 top-8은57개와58개였다. 세 버전 모두 diagnostic 긍정 누출은0이었다.

일반 대조3개 중2개는 기존 top-10 순서가 그대로였다. 피아노 대조는9/10 overlap이고 신규 해병문학 후보는 top-10에 없었다. 이 차이를 숨기거나 전체 회귀 합격으로 표시하지 않았다. 낮은 순위 사례와 원질의는 [RETRIEVAL-FOLLOWUP.json](integration-evidence/RETRIEVAL-FOLLOWUP.json)에 있다.

각 arm은 소수 슬롯2개와 topic/baseline2개의 독립 lane을 검색했고, 반환된32개 occurrence의 전체 source·조건·효과·claim limits를 검토했다. 최종 신규 노출은 A0/B1/C0개였다. B의 V060 컨테이너 탑은 예비 바퀴 장면에 무관해 채택하지 않았다. rank-32 창 안의 존재와 창에서8개를 샘플링해 실제 전달된 후보를 구분했다. 조회·게이트·샘플 seed를 점수에 맞춰 재작성하지 않았다.

## 실제 생성과 원본 픽셀

세 독립 agent 모두 최신 SKILL SHA `{images['cases'][0]['skill_sha256']}`를 사용했다. 요청 원문과 첨부 참조는 공통이며, 난수·컨셉·baseline/core·소수 슬롯·테스트 게이트는 후보 조회 전에 각각 작성했다. controls는 기본값 sensual1/fetish0/creativity1/surreal0이다. 서로의 장면/후보/결과를 공유해 컨셉을 바꾸지 않았다.

실제 builtin 이미지 호출은 각1회, 총3회다. fallback·재생성은0회다. 세 프로젝트 사본은 tool-returned 원본과 byte hash가 같고 root도 원본 전체를 `view_image(detail=original)`로 관찰했다. 실제 응답에 model ID가 없어 observed model은 null로 둔다. workflow의 기본 model/size 메타데이터를 실제 도구에 전달된 값 또는 실제 출력 크기의 증거로 사용하지 않았다.

|arm|컨셉|동결 관찰 게이트|전체 정확성 판정|신규 CID 노출/활용|
|---|---|---|---|---|
|A|병영 검열 쿠튀르|5/5 visible|FAIL: 오른손 검사/왼손 지지와 군화 방향이 좌우 반전. 특정 장르 전체의 고유성 미확정|0/0|
|B|예비 바퀴에 과잉 의전|4/5 PASS|FAIL: 같은 깃발의 그늘이 예비 바퀴에 닿는 관계 미확인|1/0|
|C|침수 생활관 고무보트 검열|4/5 PASS|FAIL: 선체와 바닥의 접지가 가려짐|0/0|

A의 다섯 동결 관찰 게이트는 한 손 지지/다른 손 검사만 요구했기 때문에 통과하지만, 전체 prompt와 managed embodiment는 해부학적 좌우까지 평가해 fail이다. 이 둘을 합쳐5/5를 전체 정확성 합격으로 제시하지 않는다. B의 검은 타이어 표면이나 도로 그림자를 깃발→바퀴 그늘의 증거로 대체하지 않는다. C는 보트 접지가 보이지 않으므로 떠 있다고 단정하지도 않는다. `partial_is_fail`·`UNOBSERVABLE_NOT_PASS`를 유지했다.

### A — 병영 검열 쿠튀르

[정확한 실행 prompt]({rows['a']['prompt']}) · [agent 보고]({Q/'image-tests/a/arm-report.json'}) · 실제 크기 {rows['a']['actual_dimensions'][0]}×{rows['a']['actual_dimensions'][1]}

![A: 병영 검열 쿠튀르]({rows['a']['image']})

### B — 예비 바퀴의 의전

[정확한 실행 prompt]({rows['b']['prompt']}) · [agent 보고]({Q/'image-tests/b/report.md'}) · 실제 크기 {rows['b']['actual_dimensions'][0]}×{rows['b']['actual_dimensions'][1]}

![B: 예비 바퀴의 의전]({rows['b']['image']})

### C — 침수 생활관의 고무보트 검열

[정확한 실행 prompt]({rows['c']['prompt']}) · [agent 보고]({Q/'image-tests/c/arm-report.md'}) · 실제 크기 {rows['c']['actual_dimensions'][0]}×{rows['c']['actual_dimensions'][1]}

![C: 침수 생활관 고무보트 검열]({rows['c']['image']})

## 기록의 한계와 후속 계획

참조는 보이는 얼굴·단발 외형을 안내했다. 실제 신원·나이·군 복무·성격은 확인하지 않았다. 군복·기호·부조리한 군 의전은 보이지만, 특정 팬 판본/캐릭터나 해병문학 전체의 유일한 외형을 입증하지 않는다. 신규 자료가0개 채택된 이번 이미지를 신규96카드의 품질 인증으로 쓰지 않는다.

원문 파일/해시는 agent dispatch 전에 준비했으나 공식 neutral envelope init은 dispatch 후, core 작성을 보류한 상태에서 완료됐다. 따라서 init이 dispatch 이전이었다는 주장은 하지 않는다. 실제 core/게이트의 pre-candidate freeze는 보존했다. 첫 retrieval은 staging store에 모델 상대경로 실체가 없어 실패했고, 동일 generation의 실제 설치 store로 수정해 성공했다. 실패 시 이미지 호출은0이었다. B 최초 stderr는 tool 반환에서 일부 잘려 byte-exact 전체 캡처라고 주장하지 않는다.

B의 사람이 읽는 `final-prompt.txt` export에는 실행 문자열 뒤에 LF가 하나 더 있었다. 원본 export를 보존하고 verified render_request에서 정확한 runtime 문자열을 [prompt.runtime.exact.txt]({rows['b']['prompt']})로 별도 추출했다. 문자열을 조용히 trim해 같은 hash인 것처럼 처리하지 않았다. 실제 실행 prompt/참조/도구 입력의 해시와 이 차이를 함께 기록했다.

대규모 acyclic JSON 처리의 cyclic GC 비용을 표본에서 확인해 후반 CLI에 allocation-scheduling wrapper를 사용했다. 이 helper는 원래 dispatcher의 Python launcher에 `gc.disable()`만 추가하고 기존 native 코드·모든 validator/assert·환경변수 제거를 유지한다. 스킬/후보/핵심 코드 파일은 이 최적화를 위해 수정하지 않았다. 근거와 helper는 integration-evidence 안에 있다.

[독립 검색 분석과 후속 개선 계획](INDEPENDENT-RETRIEVAL.md)에 다음을 구체화했다: 검색용 주제에서 실행 지시를 분리하는 회귀 검증, 순위 창/샘플/적합성/채택의 별도 측정, 실제 신규 관찰 계약을 요구하는 독립 fixture, 낮은 순위6건의 한영·문맥 구분, source→prompt→실제 도구 입력→원본 픽셀을 잇는 재검증. 신규라는 이유로 가산점이나 강제 채택을 넣지 않는다.

원래 [평가 사례](evaluation-cases.json)의 NOT_RUN 값은 최초 연구 설계 시점의 fixture 이력이다. 실제 실행 결과는 후속 qualification 파일에 보존했다. 이번 작업에서 commit/push는 수행하지 않았다.
'''
(Q/'INTEGRATION-RESULTS.md').write_text(text)
p=Q/'README.md';s=p.read_text().replace('**연구 완료 · 데이터 반영 및 독립 이미지 검증 진행 중**','**소스·인덱스 반영과 독립 이미지3개 검증 완료 · 신규 픽셀 반영 미입증**')
s=s.replace('실제 검색과 설치를 검증하고 있다.','실제 검색과 테스트용 설치를 검증했다. 기본 실행본 승격은 보류했다.')
footer='\n[최종 원본·정확한 prompt·판정·후속 계획](INTEGRATION-RESULTS.md): 이미지3회 생성, 신규 후보 활용0/3, managed technical qualification 합격0/3. 소스/인덱스 반영과 운영 기본 선택은 별도 상태다.\n'
if footer not in s:s+=footer
p.write_text(s)
print('final state and report written')
