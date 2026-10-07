# P0와 main 통합 검증

작성일: 2026-10-07. 작업 기준과 가져온 `origin/main`은 `4c9a0054473c4383ca5287ca3bf294b277e5c6e7`로 같았다. 격리 작업 폴더에서 `git pull --ff-only origin main`을 실행했으며, 원격 소스 충돌은 없었다. 원격 main의 기존 작성 데이터와 계약을 유지하면서 로컬 P0 변경을 적용했다.

반영 범위는 의미 진단과 명확한 판정 이유, 작성 데이터의 보조 축, 감사된 입력만 받는 이미지 API 경로, 원본 바이트와 실행 기록 연결, 관련 테스트 및 이번 세션의 분석·계획·검증 기록이다. 원래 작성자의 동결 core, 사용자 정의 우선순위, 선택 후보의 advisory 권한을 유지한다. 다른 작업의 미커밋 등록표·시각 프로필·테스트는 게시 범위에서 제외했다. [구체적 파일 범위](./INTEGRATION_PREPARATION.json)에 원격 기준, 포함 파일과 제외 파일을 기록했다.

| 검증 | 결과 |
|---|---|
| 관련 회귀 테스트 | 194개 모두 통과, 실패·오류·skip 0개. 전체 저장소 suite 결과는 아님 |
| 소스 보존 | 실행 전후 기록한 해시 변화 0개. 스킬 전체 추적 파일도 staged 소스와 일치 |
| dictionary와 두 인덱스 | 검증 통과 |
| 의미 인덱스 재생성 | 원격 main 기준 10,493개. 정확한 입력과 벡터 공간이 맞는 기존 벡터만 재사용, 임베딩 호출 0회 |
| 실제 API CLI dry-run | 구성 감사 pass, 실행 감사 pass. quality 상태 warn을 그대로 기록 |
| 외부 호출 | API 키 조회·네트워크 연결·이미지 호출 0회 |
| 기존 작업 | 변경·미추적 파일 1,746개, 총 2,020,475,235바이트의 내용 해시 모두 유지 |

[회귀 결과와 고유 테스트 ID](./FOCUSED_REGRESSION.json), [회귀 로그](./FOCUSED_REGRESSION.log), [dictionary·runtime 검증](./SOURCE_VALIDATION.json), [인덱스 재생성](./INDEX_REBUILD.json), [API dry-run](./DRY_RUN.json), [원본 보존 확인](./PRIMARY_PREPUBLICATION_PRESERVATION.json), [원본 파일 해시](./PRIMARY_BEFORE_MANIFEST.json)를 보관한다. 이전 P0 기록은 당시 작업 폴더의 미커밋 데이터를 포함한 역사 기록으로 유지했고, 이번 결과는 원격 main에서 P0만 분리한 소스의 검증이다.

현재 검증한 generation은 `c6f410a9a0560c31fe9652221af611e1686429097194baa52bcdb27699e78c28`, source fingerprint는 `d403eeca758015b622520169a3e3e71ff174cbeed8f0bf92eab7a5945735ead2`다. 실제 이미지 생성과 픽셀 품질 평가는 수행하지 않았다.

현재 폴더 동기화는 기존 파일 바이트를 유지하며 게시 파일만 Git 인덱스에 맞춘 뒤 표준 fast-forward를 사용하는 방식이다. 이 방식의 원본 보존을 별도 Git 저장소에서 검증했다. 커밋·푸시와 동기화 후의 최종 원격 SHA 및 파일 해시 확인은 이 대화의 최종 응답과 `/var/folders/4x/l_6vrtjj4rsbvgmq7t6tfgsh0000gn/T/image-prompt-p0-main-merge-h_5_d5z7`의 `PUSH_VERIFICATION.json`, `PRIMARY_AFTER_SYNC.json`에 남긴다.

현재 스킬·테스트의 whitespace 검사는 통과했다. 중단된 과거 로그 2개의 마지막 공백은 당시 원본 바이트로 보존했다. [검사 결과](./DIFF_CHECK.json)에 해당 파일과 이유를 기록했다.
