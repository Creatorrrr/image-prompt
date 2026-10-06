# 팔레트 적용 데이터의 main 통합 기록

원격 main `96e20422316276a4e0b5ed97f44152e4931e7504`를 pull한 뒤, 검증된 팔레트 연구·후보·시각 의미 데이터를 그 위에 추가했다. 기존 main의 도포 뒷면 자료와 V32 기록을 보존하고, 기존 후보와 필수 의미를 유지한 V33 기준을 만들었다.

- 후보 37개, 시각 프로필 13개, 기존 후보 23개에 연결한 선택적 맥락 52개를 반영했다. 근거가 부족한 주장 11개는 보류했다.
- main의 의미 항목 10,396개와 시각 프로필 2,193개를 모두 유지했다. 정확한 텍스트·제공자·모델·차원에 맞는 벡터를 재사용해 10,433개/2,206개로 색인을 재생성했다. 임베딩 호출과 기존 샤드 삭제는 0건이다.
- V32의 논리 파일 1,369개와 원본 해시·모드·Git 출처를 보존했다. 변경한 기존 파일 7개만 별도로 보관했으며, V31의 원본 backing도 인증된 기록에서 복원한다. 기존 기록은 Python 3.12.14/Unicode 15.0.0 환경에서 그대로 재생한다. `PHOTO_V32_PYTHON`으로 같은 환경의 실행 파일을 지정할 수 있으며 버전이 다르면 거부한다.
- V33의 변경은 검토된 선택적 후보 목록과 색인 바인딩 15곳으로 한정했다. 기존 공통 후보, 요청 입력, 필수 의미, negative prompt, 공개 후보 수 64개는 보존했다. 현재 V33 기준은 작업 환경의 Python 3.14.3/Unicode 16.0.0에 바인딩되어 있다.

## 검증

데이터·등록·유지보수 관련 48개, V33 경계 9개, V32 경계 28개가 통과했다. V32의 공개 재생 진입점에서도 원래 pack과 receipt를 검증했다. 전체 208개 모듈 1,917개 테스트를 실행하고 최종 환경 보완 후 영향받은 두 모듈을 다시 실행했다. 추가된 실패와 오류는 0개다. 전체 결과는 **FAIL**이며, 팔레트 자료가 없는 원래 main에서도 동일하게 재현되는 기존 실패 모듈 5개가 남아 있다:

1. `test_photo_character_appearance_100` — 기존 프로필 보존 assertion의 13개 subtest.
2. `test_photo_krummholz_korean_alias_data_cleanup` — 과거 데이터와 현재 맥락 제한 기대값.
3. `test_photo_liminal_active_use_korean_data_cleanup` — 고정된 상태 집합 기대값.
4. `test_photo_protostar_korean_alias_data_cleanup` — 과거 데이터와 현재 맥락 제한 기대값.
5. `test_photo_shelf_return_korean_state_data_cleanup` — 과거/현재 유지 상태 기대값.

기존 실패를 통과시키기 위해 기대값이나 원본 기록을 완화하지 않았다. 자세한 실행 결과는 [FINAL-VERIFICATION.json](FINAL-VERIFICATION.json), [FULL-REGRESSION-RESULT.json](FULL-REGRESSION-RESULT.json), `UPSTREAM-*.json` 및 연결된 로그에 있다.

## 보존 및 이미지 검증 범위

`PRIMARY-BEFORE.json`은 원래 작업 폴더의 변경 파일 15개와 미추적 파일 1,577개의 관찰 시점 해시를 기록한다. 원래 폴더의 별도 연구·데이터 작업은 이 커밋에 포함하지 않는다. 동기화 직전에는 동시에 진행된 별도 분석 작업의 최신 내용을 다시 확인해 보존한다. 공유 작업 폴더의 파생 색인은 미커밋 데이터까지 포함해 재생성하므로, 깨끗한 main의 색인과 구별한다.

이전 3개 독립 에이전트의 이미지 생성 5회와 평가를 그대로 보관했다. 그 결과의 전체 조건 충족은 1/3 컨셉이었고, 일반 후보 노출 0/3의 공백도 남아 있다. 이번 Git 통합에서 이미지를 새로 생성하지 않았으며, 이전 이미지를 통합 후 새로 검증된 렌더나 사용자 승인으로 간주하지 않는다. 원래 절대 경로와 해시도 유지했다.

[MERGE-ADOPTION.json](MERGE-ADOPTION.json), [INDEX-REBUILD.json](INDEX-REBUILD.json), [V33-PALETTE-DATA-PROOF.json](V33-PALETTE-DATA-PROOF.json), [V32-PARENT-SOURCE.json](V32-PARENT-SOURCE.json)이 통합·보존 범위의 근거다.
