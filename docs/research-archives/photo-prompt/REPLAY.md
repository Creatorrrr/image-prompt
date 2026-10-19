# 현재 검색과 과거 재현의 경계

현재 기본 검색은 설치된 H 단독+F2다. `retrieval-runtime.json`과 run별 binding이
실제 실행 버전을 고르며, 이 문서나 유지보수 도구는 기본 검색에 자동 연결되지 않는다.

## 명시적인 과거 실행 검증

`tools/photo_runtime_maintenance/native_replay.py`는 이미 pack과 원래 native receipt가
있는 run을 대상으로 한다. 원래 저장된 receipt와 pack·source binding·세대 manifest·
코드 전체 집합을 확인한 뒤, 해당 세대의 봉인 소스로 감사를 실행한다.

```sh
python3 -B tools/photo_runtime_maintenance/native_replay.py inspect --run RUN
python3 -B tools/photo_runtime_maintenance/native_replay.py verify --run RUN
python3 -B tools/photo_runtime_maintenance/native_replay.py audit --run RUN
```

- `inspect`: 원래 발행된 receipt와 세대·코드의 일관성. 구성/의미 감사 완료를 뜻하지 않는다.
- `verify`: 위 검사에 전체 manifest member의 크기·SHA 검사를 더한다.
- `audit`: 검증한 원래 소스로 native receipt 재계산과 composed audit를 수행한다.
  정상 H-F2 검색이나 H-F2 receipt 전부를 검사하는 명령은 아니다.

감사는 pinned Python으로 격리 실행한다. 네트워크·원래 프로젝트와 공유 runtime
쓰기·현재 scripts/precore 읽기를 OS 수준에서 막고 API 키와 외부 Python 경로를
제거한다. 새 임베딩 요청도 차단한다. 세대나 의존성이 없거나 원문이 변조되면
거부/보류하고 다른 세대나 현재 소스로 넘어가지 않는다. 새 generation·CURRENT·
receipt는 만들지 않는다. 원래 run의 경로와 내용을 고치지 않는다.

실행 가능한 코드는 검토한 설치본 94개 및 보존된 native 세대 74개의 코드 집합으로
제한한다. 자체 manifest/receipt를 맞췄어도 미등록 코드 집합은 실행하지 않는다.
미등록 세대는 inspect/verify로 자료를 확인할 수 있지만 audit는 추가 출처 검토까지
보류한다. 검증한 소스 대신 미등록 bytecode·확장 모듈을 읽는 경로도 차단한다.

실제 검증한 것은 기존 설치 run 1건의 원래 native receipt·구성 감사다. 원래 store가
없는 과거 실행 41건을 새로 복원하거나 모두 재현한 것으로 해석하지 않는다.

## 과거 Gemini 증거 읽기

`historical_evidence.py`는 기존 `RESULT.json`과 같은 디렉터리에 보관된 원시 응답만
검증한다. 원래 운영 source archive의 provider 검증기를 임시 루트에 복원하며,
현재 공용 provider를 import하지 않는다. 원래 archive와 source lock은 수정하지 않는다.

```sh
python3 -B tools/photo_runtime_maintenance/historical_evidence.py \
  --result RESULT_JSON --output /tmp/new-history-check.json
```

동일 실행에 `--result`는 최대 3건이다. 요청 text hash, vector hash, 원래 실행 증거,
원시 응답의 요청 연결과 body SHA를 확인한다. 결과는 과거 보관 증거의 일관성이다.
새 Gemini 요청·재시도·key 조회·모델 추론·재임베딩 기능은 없다.

## 보존하거나 보류한 기존 로직

현재 `photo_embedding_provider.py`는 로컬 공용 기능과 과거 space/증거/transport를
함께 갖고 있다. `atomic`·벡터/space 검증·로컬 batching과 캐시는 현재 호출자가
사용한다. Gemini 기록 해석은 신규 원격 호출과 구분해 보존한다.

`activate_local_embeddings.py`, `qualify_local_embeddings.py`, `qualify_local_hybrid.py`의
기존 계약도 유지했다. 실제 activation·rollback·Gemini transport를 실행하지 않았다.
이 도구들을 이번 문서의 읽기 전용 명령과 같은 것으로 간주하지 않는다.

미사용 후보 9개, provider 본문 이동·기본값 변경, 기존 공개 native routing 변경은
이번에 적용하지 않았다. 코드 전체를 묶는 기존 source/algorithm 검증이 통제된
소스 변경을 거부했다. CURRENT·봉인 세대·지문 검사를 바꾸지 않는 조건에 따라
보류했다. 제거 proposal patch는 연구 증거에만 보관하며 자동 적용하지 않는다.

기존 native 공개 명령은 원래 경로를 유지한다. 별도 재현 도구의 성공을 기존
CURRENT와 작업 소스가 새로 일치하게 되었다는 증거로 사용하지 않는다.
작업 소스 77개와 CURRENT 세대 74개의 기존 차이도 이번 작업에서 고치지 않았다.

실제 처리와 제한은
`docs/research-evidence/photo-prompt/runtime-logic-cleanup-20261019/REPORT.md`를 따른다.
