# main 병합 검증

로컬 데이터 품질·양방향 관계 작업 `d9dc3df7012f395c48d536ee9df80df060cd24f9`와 팔레트 작업을 포함한 main `c4c0e4ed25981fc46c09de6e138247b5788ea43c`를 통합한다. 두 작업의 원본 기록과 동결 검증 결과는 덮어쓰지 않는다.

## 원본과 파생 데이터

- `FINAL-AUTHORED-MERGE.json`: main의 원본 대비 변경은 세 항목의 범위 제한 여섯 leaf 추가와 두 정비 참조의 record_id/sha256 네 leaf 갱신이다. 원래 정비 기록을 보존하고 새 기록으로 실제 authored body 해시를 연결했다. 팔레트 후보·프로필과 원본 등록 manifest는 main과 바이트 단위로 같다.
- `VECTOR-PRESERVATION.json`: 후보 인덱스 10,433개와 시각 프로필 2,206개의 ID·검색 텍스트·벡터가 main과 같다. provider/model/dimensions/text recipe를 검증한 뒤 모두 재사용했다.
- `FINAL-INDEX-REBUILD.log`: 원본을 병합하고 정비 참조를 바로잡은 뒤 canonical builder로 파생 인덱스를 만들고 런타임 세대를 게시했다. 네트워크와 추가 임베딩 호출은 차단했다. 이전 샤드는 삭제하지 않았다.
- 최종 병합 세대: `9b8855ab1cf3920b27ec6b8a307a87cc9199e347448ad06d6d42ad245a1c0fb7`.
- `final-report/`: 후보 10,397개·번들 988개·프로필 2,206개·명시적 edge 3,019개. 오류 0건, 의미 검토 후보 46건. 관계 경로를 후보 단독의 의미 충족으로 승격하지 않는다.
- `FINAL-CURRENT-QUERY.json`: 현재 로컬 원본·세대·도구·관리 CURRENT를 검증한 실제 조회. 결과의 `freshness`는 `current_verified`다.

## 검증 경계

main의 팔레트 V33 baseline·pack·proof와 `tests/photo_palette_history.py`를 그대로 유지한다. 이번 작업의 이전 V33 원본과 독립 QA 기록도 그대로 남긴다. 양쪽 원본은 각각의 실제 Python 환경과 원본 assertion으로 재현하며, 병합된 현재 원본은 후속 V34 경계에서 검증한다.

초기 병합 세대에서 관리·최신성 등 92개와 시각 조회·의무 적용 40개가 통과했다. 변경 영향을 받는 46개 모듈의 449개 검사로 과거·현재 경계와 데이터 범위를 확인했으며, 정비 참조의 낡은 authored body 해시를 발견해 새 기록으로 수정했다. 당시 원본 V32 28개·local V33 16개·upstream V33 9개 재현은 모두 통과했다.

최종 참조 수정은 실제로 로드한 runtime 데이터 전체를 바꾸지 않았으며(`MAINTENANCE-REFERENCE-REPAIR.json`), 대표 pack도 초기 병합 결과와 바이트 단위로 같다. 최종 세대에서 source regression의 다른 21개와 보완된 PHowner 10개, V34 mutation 14개, 실제 default/current receipt 및 원본 V32/V33 dispatch 2개, 대표 historical 구조 11개가 통과했다. 단계별 실행 로그와 미통과 최초 시도는 그대로 남긴다. `FINAL-VERIFICATION.json`은 이 증거를 집계한다.

기존 main의 전체 회귀에서는 다섯 모듈이 실패했다. 이 사실과 원본 재현은 [팔레트 main 검증](../color-palette-main-merge-20261007/README.md)에 보관되어 있다. 이번 검사에서도 같은 다섯 실패 사례가 남았다. character 모듈에는 현재 guard 검사 1개를 추가했으므로 테스트 수는 12→13이고 기존 실패 사례는 13개 그대로다. 최초 실행기의 test-count 비교 오류는 실패 로그를 바꾸지 않고 별도 집계에서 설명한다. 전체 suite가 통과했다고 표현하지 않는다.

`history-initial-qualification/`은 정비 참조 수정 전 V34의 실제 source/proof/code/pack/receipt/검사 결과다. 최초 세대 `2e6bc8...`의 결과를 최종 세대로 다시 표기하지 않는다. 최종 `history/`는 새 지문과 6 add·4 replace, 두 원본 정비 기록과 successor 기록의 연결을 별도로 인증한다.

5개 무작위 주제의 독립 프롬프트 검증은 [이전 QA 기록](../data-quality-links-20261007/README.md)에 남아 있다. 입력·출력·검증 세대는 원래 값 그대로다. 이번 병합의 검증과 혼동하지 않으며 이미지 생성이나 픽셀 품질을 증명하지 않는다.

## 주 작업 폴더 보존

`PRIMARY-PREFLIGHT.json`은 병합 전 주 작업 폴더의 수정·미추적 파일을 기록한다. `sync_primary.py`는 푸시된 main으로 fast-forward하기 직전 최신 바이트를 다시 기록하고, 충돌하는 이 작업 소유의 파일만 별도 백업한다. 다른 작업의 원본·테스트와 모든 기존 샤드를 보존한다. 주 작업 폴더의 별도 후보·프로필은 그 폴더의 인덱스 재생성에서만 사용하며 main qualification에 포함하지 않는다.

최종 동기화와 푸시 상태는 `PRIMARY-SYNC.json`과 `PUBLISH-RECEIPT.json`에 기록한다. 보고서의 `commit_observed`는 생성 당시 Git 관찰이며, 후속 커밋으로 다시 표기하지 않는다.
