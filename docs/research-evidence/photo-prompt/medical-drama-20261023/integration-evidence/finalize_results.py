from pathlib import Path
import datetime,hashlib,json
O=Path(__file__).resolve().parent;D=O.parent;ROOT=O.parents[4]
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ref=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
refsha=sha(ref);expected={'a':'037e3b078985989065707e3f01e968ce817e7806f689c49656b7d8a7235f6626','b':'470e2d37a7b0441012a5d7917b7bcb55d7b6833cf18ef000d3c2f7f3510408d5','c':'80d34d0acad9aa5928c1d028ff5c862d82a4c5f1431ac5977207277573636b8b'}
arm={};checks={}
for k in 'abc':
 r=ROOT/'generated/photo-runs'/('medical-drama-20261023-native-'+k);w=read(r/'workflow.json');m=read(r/'run_manifest.json');core=read(Path(w['artifacts']['authorial_core_normalized']['path']));a=read(Path(w['artifacts']['review_audit']['path']))['visual'];rows=[json.loads(x) for x in (r/'image_runs.ndjson').read_text().splitlines() if x.strip()]
 checks[k]={
  'one_actual_recorded_attempt':len(rows)==1 and rows[0]['image_call_count']==m['image_call_count']==1,
  'ledger_manifest_identity_matches':rows[0]['run_id']==m['ledger_run_id'],
  'same_original_reference':m['reference_sha256']==[refsha] and rows[0]['reference_sha256']==[refsha],
  'original_frozen_core':m['authorial_core_sha256']==core['canonical_sha256']==expected[k],
  'frozen_intent_lock':m['intent_lock_sha256']==core['intent_lock']['canonical_sha256'],
  'no_cross_arm_inputs':m['cross_arm_inputs_used'] is False,
  'latest_skill_snapshot_bound':m['skill_sha256']=='f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089',
  'image_hashes_match_saved_originals':all(sha(Path(x['path']))==x['sha256'] for x in m['image_hashes']),
  'same_sealed_test_generation':w['h_f2_binding']['generation_id']=='1d3013b5e422e72eb80bdd75189ebe25575ffa92aecc3378ed8ba79358b897bd',
  'managed_review_completed':w['phase']=='review_record_validated' and not a['schema_failures'],
  'pending_user_judgment':a['user_judgment']['source']=='not_yet_received',
  'expected_technical_result':a['technical_qualified']==(k=='a')}
 assert all(checks[k].values()),checks[k]
 arm[k]={'manifest':str(r/'run_manifest.json'),'ledger_run_id':m['ledger_run_id'],'image_path':m['image_paths'][0],'image_sha256':m['image_hashes'][0]['sha256'],'recorded_tool_calls':1,'whole_case':'pass' if k=='a' else 'fail','technical_qualified':a['technical_qualified'],'user_acceptance':'pending','coordinator_viewed_original_pixels':True}
review={'schema':'medical-drama-independent-image-results/v1','completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arms':arm,'verification':{'status':'PASS','checks':checks},'actual_tool_calls':3,'delivered_images':3,'retries':0,'fallbacks':0,'topic_visible':{'passed':3,'total':3,'evidence':'A: operating team, lamp, operating table and separate trolley. B: parallel bars, two-actor support and gait belt in rehabilitation room. C: cuff measurement encounter and examination couch.'},'reference_appearance':{'passed':3,'total':3,'scope':'Qualitative visible face/hair resemblance; no identity, occupation or age proof.'},'strict_whole_cases':{'passed':1,'total':3},'new_source_usage':{'arms_with_new_source_inspiration':2,'arms_with_new_source_exposure':3,'distinct_new_sources_retained':3,'complete_new_source_propositions_visible':1,'source_results':{'A09':{'arm':'b','status':'partial_fail','evidence':'Therapist complete inside-lane placement remains ambiguous at rear foot/right rail floor boundary.'},'D06':{'arm':'c','status':'pass','evidence':'Wide upper-arm cuff, continuous hose, cuff-edge coupling and separate tabletop monitor socket are visible together.'},'A01':{'arm':'c','status':'partial_fail','evidence':'Actual desk open-end boundary and across-that-end seating relation are hidden by foreground patient/crop.'}},'native_approval':False},'coordinator_pixel_findings':{'a':{'status':'pass','evidence':'Right hand/arm connects to overhead lamp handle; empty table light pool, colleague hand/attention, separate trolley and reference-like bob/face coexist. Colleague fingertips overlap upper diffuse pool edge; no strict wholly-outside claim.'},'b':{'status':'fail','evidence':'Both rail grips and gait-belt grip read clearly. Actor-relative right foot is forward instead of frozen left, and therapist full inside-lane relation remains partial.'},'c':{'status':'fail','evidence':'Cuff/hose/monitor connection and supported forearm read clearly. Clinician hand is curled instead of frozen open; specific desk-end boundary cannot be established.'}},'evidence_boundary':'Three authored cases, no before/after causal improvement estimate, independent holdout or medical correctness qualification. Partial or unobservable required relations fail. User judgment remains pending.'}
(O/'independent-image-results.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
summary=read(O/'integration-summary.json');summary['image_tests']=review;summary['final_default_exposure']=read(O/'current-default-medical-exposure.json');summary['concurrent_source_observation']=read(O/'concurrent-source-drift.json');(O/'integration-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
p=D/'INTEGRATION-RESULTS.md';raw=p.read_text();raw=raw.replace('세 독립 에이전트의\n이미지 테스트는 아래 기록과 별도로 진행 중이며 결과를 받은 뒤 이 문서를 갱신한다.','세 독립 에이전트가\n참조 이미지를 사용해 각각 1회 생성했고, 원본 픽셀과 모든 실행 기록을 검토했다.\n의학 주제·참조 외모는 3/3에서 읽히며, 전체 필수 관계는 1/3 통과다.')
raw=raw.replace('결과: 진행 중. 각 팔은 기본 제공 이미지 도구 1회만 호출하며 재생성·대체 제공자는 없다.','결과: 완료. 기본 제공 `image_gen` 도구를 팔마다 1회, 총 3회 호출했다.\n원본 3장을 저장했으며 재생성·대체 제공자는 없다. 관측된 이미지 모델명은 제공되지\n않았으므로 특정 모델명으로 추정하지 않았다. 세 팔의 구성·런타임·리뷰 기록 감사는\n통과했다. 모든 팔에 남은 4개 intent coverage 경고는 비차단 작성 근거 경고로 보존했다.\n관리형 기술적 픽셀 충족은 A PASS, B/C FAIL이다.')
raw+='''

## 생성 결과와 픽셀 판정

| 팔 | 독립 콘셉트 | 새 후보 노출 / 사용 | 원래 테스트 | 전체 판정 |
| --- | --- | --- | --- | --- |
| A | 다음 환자 전 수술등을 맞추는 두 의료진 | 5 / 0 | 5/5 | PASS; 기존 R01 수술등·수술대·별도 기구대 3/3 |
| B | 평행봉과 보조벨트로 지지하는 재활 보행 | 8 / 1 (A09) | 4/5 | FAIL; 왼발 대신 오른발이 앞, 치료사 통로 안쪽 위치 일부 불명확 |
| C | 외래 혈압 측정과 마주 보는 진료 | 4 / 2 (D06, A01) | 4/5 | FAIL; 펼친 손 대신 말린 손, 책상 열린 끝의 배치 가림 |

새 후보의 완전한 관계는 D06의 커프–호스–모니터 연결에서 확인했다. B의 A09와 C의
A01은 일부 관계가 읽혀도 전체 소스 충족은 실패다. A의 성공은 기존 후보 R01을 활용한
성공이며 신규 데이터의 픽셀 재현 성공으로 세지 않는다. 따라서 새 후보를 쓴 두 팔 중
그 후보들의 모든 관계를 함께 통과한 팔은 없다. 원본 이미지 세 장의 전체 주제는
명확하며, 이는 모든 세부 관계가 충족됐다는 판정과 구분된다.

조정자가 원본 세 장을 직접 보고 팔별 관찰을 대조했다. A의 동료 손끝은 빛 영역
위쪽 경계와 겹치므로 손 전체가 빛 영역 밖에 있다는 주장은 하지 않는다. C의 첫 인상에서
A01을 통과로 보았던 관찰은 실제 책상 끝 경계를 다시 추적한 뒤 partial/fail로 정정했고,
`image-test-evidence/c/observation-correction.json`에 전후 관찰을 보존했다.

참조 외모 비교는 얼굴·눈·앞머리·짧은 보브의 정성적 유사성 관찰이다. 실제 인물의
동일성·나이·직업이나 치료의 적절성·성공을 판정하지 않는다. 사용자 수락은 세 장 모두
pending이다. 실패 결과도 원본 그대로 보존했고 추가 생성하지 않았다.

### 결과 파일

- 전체 정확한 프롬프트: `PROMPTS.md`
- 조정자 집계·이미지 해시·원장 검사: `integration-evidence/independent-image-results.json`
- A: `image-test-evidence/a/result-summary.json`, `pixel-test-review.json`
- B: `image-test-evidence/b/result-report.md`, `pixel-review.json`
- C: `image-test-evidence/c/result-report.md`, `pixel-review.json`

각 팔의 `run_manifest.json`과 `image_runs.ndjson`에서 1개 시도, 실제 이미지 해시,
원래 코어·의도 잠금·참조 해시, 스킬 스냅샷과 같은 고정 검색 버전을 확인했다.
서로 다른 에이전트/팔별 폴더를 사용했으며 별도 Git worktree 세 개를 만들었다는 뜻은
아니다. 생성·기록 성공 상태와 픽셀 충족 판정도 구분한다.

작업 도중 기본 실행 버전은 다른 병행 반영을 포함한
`d63b465fe1471d65ffdf0765b2d67dcc4b9d88b85202866093100f1564aa2240`으로 갱신됐다.
이 최신 기본 버전에서도 신규 양성 후보 99개 전부가 존재하며 신규 150개 전체 본문이
이번 작업 소스와 완전히 같음을 재확인했다. 이미지 테스트는 최초에 명시한
`1d3013b5e422e72eb80bdd75189ebe25575ffa92aecc3378ed8ba79358b897bd`에 그대로 고정했다.
검사 근거는 `integration-evidence/current-default-medical-exposure.json`이다.

## 관찰에서 도출한 다음 개선 대상

1. 수술등 조절 손잡이–손–팔–조명 대상의 완전한 신규 후보가 실제로 유용한지 별도
   소스/중복 검토를 한다. 이번 A에서 새 후보를 선택한 것으로 소급하지 않는다.
2. 보행 통로 안쪽 위치는 두 발과 양 레일의 바닥 경계를 한 시점에 분리해 보이는
   배치로 개선한다. 좌우 발의 주체 기준 방향을 유지한다.
3. 진료실 후보의 책상 열린 끝은 경계가 가려지지 않는 전체 배치를 설계하고, 열린 손의
   손가락 상태를 함께 보이게 한다. 일반적인 맞은편 착석으로 정의를 약화하지 않는다.

위 항목은 이번 결과에 대한 다음 검토 대상이며, 현재 후보·프롬프트·이미지의 요구를
이미지에 맞추어 사후 변경한 것이 아니다. 새 리비전이나 재생성의 결과는 아직 없다.
'''
for k,title in [('a','수술실 준비'),('b','재활 보행'),('c','외래 혈압 측정')]:raw+='\n\n'+title+'\n\n!['+title+']('+arm[k]['image_path']+')\n'
p.write_text(raw)
print(json.dumps({'verification':'PASS','actual_calls':3,'images':3,'strict_whole_case_pass':1,'new_source_complete_visible':['D06'],'report':str(p)},ensure_ascii=False))
