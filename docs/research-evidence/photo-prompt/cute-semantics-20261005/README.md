# 귀여운 요소의 시각 의미·후보팩 보강 리서치

2026-10-05 KST · 상태: **리서치와 반영 계획 완료 / 런타임 미반영**

참조 대화 **[귀여운 요소 조사](https://chatgpt.com/c/6ac250ed-78e4-83ee-832a-15b3ead6f3e5)**의 140개 항목을 원래 번호 그대로 조사했다. 용어를 추가하는 데서 그치지 않고, 실제 보여야 할 성분, 소유자와 접촉 대상, 혼동되는 형태, 기존 후보와의 관계, 반영할 파일과 검증 조건으로 나눴다.

핵심 방향은 **표정의 복합 형태, 손가락·손·물체의 접촉, 서로 다른 주체의 관계, 귀여움과 다른 표현의 대비**를 보강하는 것이다. 넓은 `귀여움`을 특정 얼굴·의상·나이·색으로 고정하지 않는다.

|산출물|내용|
|---|---|
|[REPORT.md](REPORT.md)|출처를 검토한 상세 결과, 현재 데이터의 강점과 빈틈, 분야별 보강 방향|
|[MATRIX.md](MATRIX.md)|140개 전체: 관찰 성분·관계·오인 사례·현재 후보 ID·반영 경로|
|[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)|실제 파일별 작업 순서, 보류 조건, 데이터·후보팩·이미지 검증 기준|
|[SOURCES.md](SOURCES.md)|30건의 1차 자료·공식 문서·사전·창작자 사례와 주장 범위|
|[SEMANTIC-UNITS.json](SEMANTIC-UNITS.json)|140개 의미 레코드와 출처 역할·소유·효과 매핑 제안|
|[CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json)|78개 후보 설명·조합·변형 보강안. 런타임 스키마로 직접 로드할 수 없음|
|[CANDIDATE-DETAILS.md](CANDIDATE-DETAILS.md)|대표 14건의 구체적인 한·영 설명, 손가락 접점·소유·매체·적용 조건|
|[REGRESSION-PROPOSALS.json](REGRESSION-PROPOSALS.json)|각 항목의 긍정·오인·맥락 사례, 총 420건. 실행 전 제안|
|[PIXEL-QUALIFICATION-PLAN.json](PIXEL-QUALIFICATION-PLAN.json)|18개 A/B 이미지 검증안과 후보팩의 부정 대조 조건. 실행 전 제안|

현재 checkout에서 로더로 읽은 작성 데이터는 112개 슬롯, 후보 9,949건, 시각 프로필 1,774건이다. 이번 조사에서는 67개 키워드에 재사용할 후보를 수동으로 연결했다. 이는 전체 의미의 완전한 지원이나 실제 후보팩 노출을 뜻하지 않는다. 동일 단어가 의복·해부·동작·카메라의 다른 의미로 연결되는 경우도 별도로 기록했다.

구조 검증은 통과했다. 140개 번호, 출처 참조, 현재 후보 ID, 기존 파일·슬롯, 78개 초안, 420개 회귀안, 18개 이미지 계획의 무결성을 확인했다. 효과 속성의 런타임 적합성, 인덱스 갱신, 후보팩 노출·선택, 원본 이미지의 형태, 귀여움에 대한 사용자 평가는 아직 검증하지 않았다. 작성 데이터·코드·생성 인덱스는 이번 작업에서 수정하지 않았다.

`SOURCE-KEYWORDS.json`은 원래 대화의 수집 목록, `ANNOTATIONS.tsv`는 이번 연구자가 작성한 관찰·혼동 주석이다. `EXISTING-COVERAGE.json`과 `CHECKOUT-SNAPSHOT.json`은 현재 작성 데이터 대조와 해시 증거, `RUNTIME-MAPPING.json`은 실제 소유 파일과 아직 심사하지 않은 속성 제안이다. `VALIDATION.json`과 `MANIFEST.json`에서 검증 범위와 파일 해시를 확인할 수 있다.

재생성은 저장소 루트에서 다음 명령으로 수행한다. 산출물은 이 리서치 디렉터리에만 쓴다.

```sh
python3 docs/research-evidence/photo-prompt/cute-semantics-20261005/build_package.py
```

작성 데이터 대조를 새로 해야 할 때만 `audit_existing.py`를 먼저 실행한다. 이 명령은 새 checkout의 대조 결과·스냅샷으로 두 파일을 갱신하므로, 다른 시점의 증거를 유지하려면 디렉터리를 먼저 별도로 보존한다.
