# 캐릭터 헤어 main 병합 및 발행

`origin/main`을 fetch한 뒤 깨끗한 관리 worktree에서 `git pull --ff-only origin main`을 실행했다. 기준 커밋은 `791bd1ca3128627b9aefa22e0ab64041fe9c369f`이며 당시 원격과 로컬이 같았다. 새 브랜치는 `codex/character-hair-main-merge`이다. 현재 주 작업 공간의 다른 미완료 변경을 이 커밋에 포함하지 않았다.

## 양쪽 의도 보존

main의 기존 candidate/profile 원본을 기준으로 헤어 작업 전후의 변경 필드만 ID별로 합쳤다. base slots 5,527개 중 수분·리본 배색 항목 2개를 변경했고, base profiles 333개 중 해당 프로파일 2개를 변경했다. 다른 기록과 비기록 필드는 동일하며 삭제된 ID는 없다. 새 헤어 후보 111개와 프로파일 111개, 기존 후보 31개 설명 보강 및 두 유지보수 기록을 그대로 가져왔다. main의 등록 106행은 순서·값을 유지하고 새 두 원본을 각 kind 끝에 append했다.

명칭만으로 수분을 강제하지 않는 wet-look 경계, 시술명과 선택된 색 리본 무늬를 구분하는 balayage 경계, 같은 소유자·부위·속성 잠금, 선택적 프로파일 및 원본 픽셀의 all-of 조건을 유지했다. 원래의 과거 기준 fixture는 변경하지 않았다. 현재 등록 순서 검사에 main에 이미 발행된 VEL/fire/soil/electrical과 새 hair 등록을 정확한 순서로 추가했으며, 전체 비교 assertion을 유지했다.

재생성된 semantic index는 10,956개, visual profile index는 2,713개·5,282 exact term이다. 기존 main의 ID는 모두 유지했다. 기존 10,812개 후보와 2,600개 프로파일의 텍스트·벡터가 같다. 변경 텍스트는 후보 33개·프로파일 2개, 새 ID는 각각 111개다. 모든 벡터가 부모 캐시 중 하나의 정확히 같은 텍스트·provider·model·dimensions·recipe와 일치하며 추가 임베딩 요청은 0회다. 기존 primary의 10,999/2,756개 색인에는 다른 미완료 intellectual 작업이 포함돼 있으므로, 이번에 발행하는 main 색인과 구분한다. 관련 원본을 무단으로 함께 발행하지 않았다.

`BOTH-INTENTS-VERIFICATION.json`, `AUTHORED-MERGE.json`, `VECTOR-CACHE-INPUTS.json`, `CANDIDATE-VECTOR-REUSE.json`에 변경과 보존 근거를 기록했다. source 합성 이후 dictionary/index 체크와 명시적 런타임 발행을 통과했다. 병합 검증용 런타임은 다른 작업에 영향을 주지 않는 별도 저장소이며 generation은 `b22d462991e987fef060b4cf147eb6a401d4e1323d4458140d5fec101e2b881b`이다. 초기 자동 발행 두 작업의 경쟁으로 나온 pending 메시지도 로그에 남겨 두었고, 직후의 명시적 발행이 성공했음을 별도 확인했다.

## 이미지 근거와 범위

독립 세 에이전트의 참조 이미지·컨셉·프롬프트·동결 테스트·원본 4장·실패 리뷰·ledger를 보존했다. 원래 이미지 시험 generation은 `0a3b19f34fb2ef66f6406cbf4f38c9aac196ebc515b8bb918aa2d1c16fc40000`이다. 새 main 코퍼스로 이 기록을 재해석하지 않았다. 그 시험은 underlights와 보정 후 장식 접촉 등의 부분 반영을 확인했으며 헤어 all-of 통과는 0/3이다. 이번 Git 통합에서는 이미지나 새 API 렌더를 호출하지 않았다.

## 검사와 발행 기록

합친 원본·코드에서 전체 discovery 227개 모듈·1971개 테스트를 완료했다. 관련 7개 모듈·85개 검사는 모두 통과했다. 전체 실행은 과거 자료·픽셀 fixture 등 24개 모듈에서 실패했다. 해당 실패 사례는 수정하지 않은 기준 main의 별도 checkout에서도 모두 재현했다. `FULL-TEST-DISCOVERY.json`, `BASELINE-FAILURES.json`, `FAILURE-CLASSIFICATION.json`과 원본 로그를 보존했다. 선행 실패가 다른 원인을 가릴 수 있으므로 전체 suite PASS나 모든 원인 완전 분리를 주장하지 않는다.

주 작업 공간의 모든 당시 tracked modification과 비무시 untracked 파일 6,547개, 약 6.49GB에 대해 바이트·모드·symlink 대상으로 보존 해시를 만들었다. stage는 이번 작업의 원본·파생 색인·연구/렌더 근거와 관련 회귀 검사로 제한했다. 실행 로그·TSV의 원래 줄바꿈과 빈 필드, 프롬프트의 exact bytes는 보존했다. code/data 대상 staged whitespace 검사는 통과했다.

커밋 직전 원격 main을 다시 fetch하여 기준이 바뀌지 않았음을 확인한다. 검증된 범위만 커밋하고 일반 fast-forward push로 main을 갱신한다. 주 작업 공간은 원래 파일 바이트를 보존한 채 Git index를 전용 lock으로 갱신하고 main ref를 이전 HEAD 기준 compare-and-swap으로 전진시킨다. 실제 커밋·푸시와 최종 local/tracking/remote 관측은 작업 후 DELIVERY.json에 별도 기록한다.
