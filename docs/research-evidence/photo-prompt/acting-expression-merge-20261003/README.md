# 연기 표정 데이터와 원격 표현 대안 수정의 머지 검증

로컬 `acbf5e89e8fd5c33e9ff295209211e485a0c64a2`와 원격 `3c3b3a649afc04a5b39abc23a0e57084ba34fec2`를 `git pull --no-rebase --no-commit origin main`으로 병합했다. 연기 표정의 문맥 가드·소유권·37개 후보·11개 프로필과 원격의 소품 접촉, 광학 효과, 재질 및 환경 표현 대안을 함께 유지했다.

## 충돌 해결과 원본 보존

충돌은 생성된 `photo_prompt_visual_profile_index.json` 한 파일이었다. 병합한 레지스트리에서 다시 생성하고, 양쪽 부모의 동일 텍스트·동일 모델·768차원 벡터를 재사용했다. 로컬에서 1,493개, 원격에서 1,496개가 호환되어 합계 1,507개 프로필 모두의 벡터를 확보했다. 제공자 호출은 필요하지 않았다. 최종 인덱스는 1,507개 프로필과 3,661개 정확 용어를 포함한다. 후보 의미 인덱스의 9,737개 항목도 실제 통합 사전의 해시·텍스트·벡터 차원과 일치한다.

현행 관측 갱신 전 양쪽의 원본·검증 자료 471개를 부모 Git blob과 대조해 모두 일치했다. 최종 상태에서는 470개가 바이트까지 동일하고 현행 관측 파일 한 개의 두 필드만 아래 사유로 갱신했다. 별도 중립 표정 조사 폴더의 26개 파일은 작업 전 SHA-256과 일치하며 커밋 범위에서 제외했다.

- [최종 부모 보존 증거](PARENT-PRESERVATION.json)
- [관측 갱신 전 부모 보존 증거](PARENT-PRESERVATION-BEFORE-OBSERVATION-REFRESH.json)
- [인덱스 재사용 계획](INDEX-REUSE-PLAN.json), [인덱스 검증](INDEX-VERIFICATION.json)
- [공백만 정리한 패키징 변경](PACKAGING-CORRECTIONS.json): 보고서의 마지막 빈 줄과 중단된 실행 로그의 공백을 정리했다. 원본 출력은 로컬 머지 자료에 보존하고 연구 패키지 매니페스트를 함께 갱신했다.

## 현행 사진 경계 관측값

원격은 현행 V6 사진 경계 관측을 갱신하는 의도를 포함한다. 통합 연기 사전은 전체 사전 및 소유권 정책의 해시를 바꾸므로, 처음 실행한 원본 경계 테스트 3개는 다시 바이트 불일치 오류를 냈다. 원격이 보존한 완전한 공개 팩과 통합 소스의 정상 CLI 출력을 비교하고, 통합 출력의 반복 바이트 일치 및 파생 해시 재계산을 확인했다.

64개 공개 후보 전체, 의미·조건, 부정 프롬프트, 동결 코어, 선택 권한과 나머지 공개 필드는 동일하다. 실제 차이는 `tags_hash`, `slot_corpus_sha256`, `slot_ownership_sha256`, 이들을 포함하는 검색 바인딩의 `canonical_sha256`, 최종 `pack_id` 다섯 곳이다. 이에 `photo_regression_baseline_v5.json`의 현행 `sha256`와 `pack_id` 두 값만 갱신했다. V1–V4의 과거 기준은 원격과 바이트까지 동일하며 원본 테스트와 fixture는 보존했다.

- [완전한 팩 비교](CURRENT-PHOTO-PACK-COMPARISON.json), [갱신 근거](BASELINE-REFRESH.json)
- [원격 완전한 팩](upstream-current-photo-pack.json), [통합 완전한 팩](merged-current-photo-pack.json), [통합 반복 출력](merged-current-photo-repeat.json)
- [갱신 전 현행 관측](photo-regression-v5.before.json), [갱신 전 오류](current-photo-baseline.log), [갱신 후 원본 테스트](current-photo-baseline-refreshed.log)

## 실행한 검증

선택한 33개 모듈의 246개 테스트와 원본 사진 경계 테스트 3개가 모두 통과했다. 로컬 연기 통합, 원격에서 추가한 14개 모듈, 공통 인덱스·시각 의미·V6 코어·소유권 경로를 포함한다. 모듈별 실행의 발견된 테스트 ID 멀티셋이 선택한 전체 범위와 일치하며 건너뛴 테스트는 없다. 사전 검증, 시각 인덱스 검사 및 의미 인덱스의 실제 전체 항목 대조도 통과했다. 이번 머지에서 전체 저장소 테스트를 다시 실행했다는 뜻은 아니다.

재실행: `.venv/bin/python docs/research-evidence/photo-prompt/acting-expression-merge-20261003/run_merge_tests.py --workers 6`.

[종합 영수증과 통합 소스 해시](MERGE-VERIFICATION.json), [246개 테스트 상세](FOCUSED-TESTS.json), [실행 로그](focused-tests-progress.log), [사전 검증](dictionary.log), [시각 인덱스 검사](visual-index-check.log).

이전 연구 및 3개 독립 이미지 사례의 기록은 각자의 원래 소스 동결 시점에 대한 증거다. 원래의 여섯 이미지와 세 사례는 모두 엄격한 픽셀 기준 실패 상태를 유지한다. 이 머지 검증은 추가 이미지 생성이나 새로운 픽셀 합격을 주장하지 않는다.
