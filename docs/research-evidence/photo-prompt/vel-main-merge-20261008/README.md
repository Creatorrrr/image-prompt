# VEL 데이터 및 테스트 main 통합

2026-10-08. main pull은 성공했으며 당시 원격 main과 로컬 main은 모두 629bf4a8이었다. 이번 커밋은 시각 의미 24개의 대체 표현 96개, 기존 후보 34개의 표현 112개, 새 관계 후보·프로필 13쌍과 관련 연구·실행 근거를 포함한다.

liminal의 과거 전체 데이터 비교와 현재 22개 검토 항목 검증을 분리한 수정도 포함한다. 추가로 V35 경계 테스트 2개가 최신 파일을 과거 입력으로 복사하는 문제를 수정했다. 당시 승인된 입력 2개를 b93bcbbb의 Git 이력에서 복원했고, 기존 V35 코드·기대 해시·proof는 그대로 유지한다. 파일 변조·권한 변조·symlink·음수 조건 변조·부모 이력 변조를 거부하는 검사는 유지한다.

## 검증

- 대상 테스트 12개 통과.
- V35 경계 테스트 7개 통과.
- dictionary validator 및 양쪽 인덱스를 깊게 확인하는 runtime publication 통과.
- 이전 단계의 변경 관련 고유 테스트 최종 판정 184개 통과 기록은 보존한다. 위 19개 재검증과 같은 전체 suite 실행으로 합산하지 않는다.
- 런타임·테스트·새 보고서의 엄격한 whitespace 검사를 통과했다. 원본 조사 자료의 CSV CRLF, Markdown 줄바꿈과 저장한 diff의 문맥 공백은 원문 bytes로 보존했다.

첨부한 원본 reference JPEG와 runtime cache는 커밋에서 제외하고 로컬에 보존한다. 실제 반환 이미지·프롬프트·감사·픽셀 판정과 차단 결과는 포함한다. 두 이미지는 일부 관계가 실패했으며, 한 시도는 출력 차단이었다. 데이터 통합을 픽셀 전부 통과나 사용자 선호 승인으로 재해석하지 않는다.

주 작업 공간은 검토된 커밋으로 fast-forward하고 이미 존재하는 로컬 데이터 보강과 테스트 변경을 세 방향으로 병합한다. 등록 목록은 파일 identity와 기존 로컬 순서를 유지한다. 합쳐진 현재 데이터의 인덱스는 provider·model·dimensions·text가 같은 벡터만 재사용해 canonical builder로 재생성하고 확인한다. 이 과정에서 unrelated dirty/untracked 파일을 삭제하거나 포괄적으로 stage하지 않는다.

[커밋 범위](COMMIT-SCOPE.json) · [V35 입력 출처](V35-FIXTURE-PROVENANCE.json) · [대상 검증](targeted-tests.log) · [V35 검증](ethereal-history-tests-fixed.log) · [runtime publication](runtime-publication.json)

main 반영 및 push 이후의 실제 ref와 원본 보존 검증은 별도의 로컬 PRIMARY-SYNC-VERIFICATION.json, PRIMARY-INDEX-REBUILD.json, PUSH-VERIFICATION.json에 기록한다.
