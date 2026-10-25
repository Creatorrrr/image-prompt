# 수사물 관계 구현 개선·동일 3컨셉 재시험

2026-10-25. **신규 자료의 실제 프롬프트 반영은 3/3 장면에서 확인했다. 신규 기여 6개 중
사전 픽셀 기준을 완전히 충족한 것은 2개이며, 전체 장면의 관계 기준은 0/3 통과다.**
같은 컨셉·같은 첨부 이미지로 새 독립 에이전트 3개가 각각 한 번 생성했다.
각 에이전트는 다른 arm·이전 프롬프트·이전 후보를 보지 않았다. 부모의 닫힌 retry
projection으로 사건·참조 appearance·controls를 보존하고 허용된 지역 관계·구도를 바꿨다.

|장면|신규 수사물 자료 실제 노출¹|최종 신규 일반 기여|추가효과 전체 픽셀 통과|고정 장면 기준²|결과|
|---|---:|---:|---:|---:|---|
|A 금융 명세서·자금흐름 대조|5|2|0/2|4/5|연필 끝이 원 밖 왼쪽 칸에 닿음|
|B 기록보관소 적재장 봉인 조사|10|2|1/2|6/7|서기의 한 발이 카트 뒤에 가려짐|
|C 막배 후 매표소 사진 탐문|6|2|1/2|6/7|정확한 부두 표적을 보는 시선이 partial|

¹ 이전 수사물 연구 자료와 이번 보강 자료의 합계다. 이번 보강만 세면 A4/B6/C5.
² 서로 다른 장면 기준의 분모는 성능 비교용 점수가 아니다. partial/unobservable은
완전 기준을 통과하지 못한다. 사전 기준과 적용 가능한 formal gate를 약화하지 않았다.

## 원인과 반영한 개선

- A의 단서 query에는 긍정 목적 뒤에 법적·과학적 부정 한계가 붙어 material이 0개였다.
  긍정 시각 목적과 claim-limit 노트를 분리했다. 기존 scope/exclusion 엔진은 유지했다.
- A에 노출됐던 timeline source는 정확한 계좌 대조·연필 접촉을 돕는 자료가 아니었다.
  B의 기존 신규 source는 adult 조건과 camera/clipboard 역할을 요구했으나 해당 사실이
  없고 둘째 인물은 카트를 잡는 장면이었다. 원 조건을 삭제하지 않고 장면에 맞는 별도
  age-neutral 일반 관계 대안을 추가했다.
- C는 대화 표제 전체 `수사물 용어 정리`가 장르 query로 쓰여 주제 자료가 노출되지
  않았다. 완전한 실제 사용자 메시지를 보존하면서 정확한 장르 부분 문자열 `수사물`을
  기존 topic/query 기능에서 선택했다.
- 최신 스킬의 일반 연출 기여와 native 전체 계약 채택을 구분했다. 미승인 표시만으로
  허용된 일반 도움을 배제하지 않되, 기존 baseline의 특징은 신규 기여로 소급하지 않았다.

관계 대안 **18개**, 검색 제외 diagnostic **3개**, optional binding **39개**를 추가했다.
이 자료는 새 에이전트 코어·query 원문을 읽기 전에 이전 실패와 source 판단으로 고정했다.
기존 candidate·조건·효과·출처와 기존 binding/catalog/policy를 보존했다.

별도로 재시험에서 발견한 coordinator 오류도 수정했다. 같은 참조 appearance 사실이
request와 reference를 함께 인용할 때 새 request hash를 거부하던 문제다. 의미·참조는
그대로 두고 검증된 request_text 출처만 재바인딩한다. 관련 **49개 테스트**가 통과했다.
이는 이전 이미지 실패 원인으로 소급하지 않는 별도의 실행 오류다. 자세한 분석은
[DIAGNOSIS.md](DIAGNOSIS.md)에 있다.

## 실제 source → 프롬프트 → 도구 입력 → 이미지

|장면·source|baseline에 없던 최종 추가|직접 픽셀 관찰|
|---|---|---|
|A R03|종이 아래 바깥 모서리 지지와 두 손 사이 열린 표적 영역|손은 위·오른쪽 옆 가장자리를 잡음. 전체 추가효과 실패|
|A R04|종이 밖 책상에 손목을 받치고 연필을 원 안으로 연결|대각선 연필·손목 지지는 일부 보이나 끝은 다른 칸에 닿음. 전체 실패|
|B R07|두 절단 끝을 걸쇠 양옆으로 바깥 회전|절단 끝과 틈은 선명하지만 끝은 평평한 직선 상태. 추가 orientation 실패|
|B R08|카메라 렌즈를 눈금자 위에 두고 같은 틈을 향하게 배치|같은 절단 영역을 향한 위쪽 렌즈·그 아래 평행한 눈금자가 함께 보여 통과|
|C R16|사진 하단을 왼손으로 받침|하단 오른쪽 모서리를 받친 손·노출된 사진 얼굴·분리된 팔 역할이 보여 통과|
|C R18|지도를 카메라 쪽으로 돌리고 직원의 다른 전완을 표적 밖에 둠|지도 방향·손끝 접촉은 보이나 다른 전완이 프레임 밖. 전체 실패|

각 신규 CID와 설치 source hash, baseline에 없는 exact final literal, 실제 native payload
문자열, 참조 파일 hash, 저장 이미지 hash를 root가 대조했다. 여섯 literal 모두 최종
프롬프트와 실제 도구 입력에 존재했다. source별 관찰 기준은 호출 전에 고정했다.
[문장·source 대조](integration-evidence/root-source-chain.preimage.json),
[도구 입력 대조](integration-evidence/root-native-input-checks.json),
[root 이미지 판정](integration-evidence/root-pixel-protocol.frozen.json)에 연결돼 있다.

채택 모드는 모두 일반적인 `inspiration_only`다. 총 일반 기여는 8개이며 그중 이번
보강 6개, 기존 일반 자료 2개다. **native 전체 source 계약 선택·승인은 0개**다.
픽셀 2개 통과를 전체 계약 승인이나 모든 수사물 자료의 품질 보증으로 바꾸지 않았다.

## 이전 실패와의 비교

A의 정확한 연필 표적 접촉은 다시 실패했다. 글자·그럴듯한 필기 자세가 맞아도
실제 끝의 위치는 틀릴 수 있었다. B의 이전 불명확한 절단 틈은 이번에는 읽혔고,
조사자의 두 발과 카트 지지도 보였다. 그러나 서기의 나머지 발이 가려져 전체 지지는
실패했다. C의 이전 사진/펜 좌우 반전, 불명확한 펜 간격, 다른 지도 분기 접촉은
이번에 의도한 관계로 관찰됐다. 정확한 같은 표적 시선은 여전히 부분 관찰이다.

같은 컨셉을 재개발한 한 장씩의 시험이다. 코어·query·자료·연출이 함께 바뀌었고,
untouched baseline 재렌더와 독립 holdout은 없다. 특정 source가 개선을 일으켰다는
인과 결론이나 사용자 수용 여부를 주장하지 않는다.

## 검증과 실행본

개발 질의 18개, 일반 대조 6개, scope 경계 6개를 전후 각각 실행해 **60회** 검증했다.
개발 질의 18/18에서 새 target이 raw 상위 8개에 노출됐고 일반 대조에는 새 material이
섞이지 않았다. 부정/제한 query의 제외 투영과 diagnostic 3개 제외는 유지됐다.
이는 노출·범위 검증이며 실제 채택이나 픽셀 증거로 대신 쓰지 않았다.
실제 arm의 검색·샘플은 각각 1회, 질의는 A5/B8/C8이었다. B 손 역할 질의는
`source_witnesses_only`로 material 0개를 유지했고 다른 질의에서 기여를 골랐다.

세 arm 모두 같은 최신 스킬 SHA `d666eb93…`, H-F2 `0c489235…`, native `409e65bb…`를
사용했다. 구성·실제 입력 감사는 모두 통과했다. 최종 실패 리뷰가 정상 형식으로
기록된 것과 픽셀 기술 자격이 실패한 것은 구분했다. 후보 재추첨·품질 재생성·외부
유료 API 호출은 없었다. native 실제 생성은 각 1회, 총 3회였다.

공유 release의 동시 source 갱신을 보존한 뒤 coordinator 한 파일만 변경했다.
21,614개 document vector는 그대로 유지했으며 원래 실행본의 모든 source/index
member를 보존했다. 설치·recording preflight와 member 대조가 통과했고 native CURRENT는
쓰지 않았다. commit/push는 하지 않았다.

## 결과 데이터와 다음 검증 과제

`photo_investigative_relation_repair_semantics_20261025.json`에 시험된 6개 source의 관찰
결과를 연결했고, 별도 `photo_investigative_relation_repair_pixel_evidence_20261025.json`에
문장·입력·이미지 hash와 실패 위치를 남겼다. 나머지 12개는 미시험 상태이며 모든
source는 native qualification을 얻지 않은 상태로 유지했다. 시험된 불변 corpus source 원문은 수정하지 않았다.

다음 개발 가설은 (A) 자연스러운 연필 접촉 위치에 선택 항목을 배치하는 구도,
(B) 서기의 몸·발을 상자 투영 밖으로 이동하는 지지 배치와 절단 끝 회전의 개별 검증,
(C) 사진/지도 사이의 시선 경쟁 해소와 다른 전완의 프레임 공간 확보다.
이 가설들은 이번 결과로 검증된 해결책이 아니다. 추가 이미지 호출은 하지 않았다.

## 이미지·프롬프트·증거

- A [이미지](../image-test-evidence/retest/a/image.png), [프롬프트](../image-test-evidence/retest/a/final-prompt.txt), [root 판정](integration-evidence/root-pixel-review-a.json)
- B [이미지](../image-test-evidence/retest/b/image.png), [프롬프트](../image-test-evidence/retest/b/final-prompt.txt), [root 판정](integration-evidence/root-pixel-review-b.json)
- C [이미지](../image-test-evidence/retest/c/image.png), [프롬프트](../image-test-evidence/retest/c/final-prompt.txt), [root 판정](integration-evidence/root-pixel-review-c.json)

집계 JSON과 공식 review/ledger 무결성 대조는 `integration-evidence/FINAL.json`에 있다.


공식 독립 결과: [A FINAL](../image-test-evidence/retest/a/FINAL-RESULT.json),
[B FINAL](../image-test-evidence/retest/b/FINAL-RESULT.json),
[C FINAL](../image-test-evidence/retest/c/FINAL-RESULT.json).


Publication note: original absolute paths and hashes in immutable records are historical. `publication-evidence/durable-export.json` maps them to versioned portable evidence. Reproducible staging/runtime copies are excluded.
