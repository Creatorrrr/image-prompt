# Ethereal / Gothic DATA와 main 병합 검증

원격 main `f6b2f88fc9adeae0dfe59b78a7a0ecafc7b4c03a`와 이번 작업 커밋
`b93bcbbb76cf33669f9edc341ca7d449e8fe4fde`의 의도를 함께 유지한다.
원래 작업 폴더에 남아 있던 다른 미커밋 변경은 별도 보존본과 대조한다.

## 반영 범위

- 후보 60개, 시각 프로필 41개, 선택용 번들 68개, 기존 후보 문맥 5개를 반영한다.
- main의 기존 authored JSON 100개를 바꾸지 않고 등록 행 2개를 추가한다.
- 스킬, 사진 런타임, V1–V34 회귀 기준까지 포함한 원본 파일 192개가 그대로다.
- 원래 리서치와 네이티브 이미지 실험 증거 282개가 작업 커밋과 바이트 단위로 같다.
- 다른 작업의 intellectual 관찰 데이터와 로컬 프로필 수정은 이번 공개 데이터에 섞지 않는다.

## 검색 인덱스와 실험 증거

공개할 인덱스는 후보 엔트리 10,493개, 시각 프로필 2,247개다. 기존 후보 벡터
10,428개와 시각 프로필 벡터 2,206개를 정확히 재사용했다. 긍정 텍스트가 달라진
기존 엔트리는 검토한 5개뿐이며, 새 항목의 벡터도 호환되는 기존 캐시에서 가져왔다.
병합 중 임베딩 API 호출은 0회다. 비교 조건은 ID, 전체 긍정 텍스트와 해시,
provider, model, dimensions, recipe다. 이전 샤드는 보존했다.

현재 공개 데이터의 generation은
`2dfe223389fdc84663d95d1357c17a8d417af3c54f671f3f2b3157696459f585`이며
source fingerprint는
`c9e6c1bc0495eca0d047f90e519c3936e474e460819becf751c6c4330dba5c2f`다.
앞선 이미지 실험에는 다른 미공개 데이터도 포함돼 있었으므로 그 generation과 구별한다.

고정된 A/B/C 입력을 바꾸지 않고 병합 후 정상 CLI로 재검색한 3건은 통과했다.
이는 후보 검색 증거다. 이미지 생성은 추가 실행하지 않았으며, 원래의 네이티브
DATA 판정 **A PASS / B FAIL / C FAIL**과 사용자 판단 대기 상태는 그대로다.

## 과거 기준 보존

V1–V34 기준, 원본 검증 문장, 기존 지원 코드와 증거 해시를 바꾸지 않았다.
V35는 정확한 main 부모 트리의 1,522개 파일을 인증하여 옛 검증을 재현한다.
변경되는 파일만 원본 backing으로 보존하고 나머지는 해시와 모드가 같은 파일을 재사용한다.

현재 V35 pack에서 달라진 부분은 검토된 7곳이다. 검색 해시 4곳, pack ID,
tags hash, 선택용 light_shape 후보 한 자리다. 마지막 항목은 이미 main에 있던
`monitor_rectangle_glow`에서 `sparkling_water_reflection_highlights`로 바뀌었다.
전체 코퍼스 통계 변화에 따른 선택용 후보 변화이며, 나머지 후보와 core, control,
composition, negative, 시각 의무는 그대로다. 공개 후보 수 64도 유지했다.

첫 전체 실행에서 V35 복구 지원 모듈이 V34의 transition API까지 대체한 오류와
새 문맥을 옛 snapshot에서 제외한 테스트의 원본 복구 누락을 발견했다. 원본 V34
API를 그대로 전달하고 인증된 successor 입력만 복구하도록 수정했다. robe 검증은
원본 main 트리를 통해 재현한다. liminal snapshot에서는 이번 선택용 확장만 제외한다.
두 변경 모두 원본 테스트 바이트를 별도로 보존했다.

재현 환경의 절대 `PYTHONPATH`가 중첩된 검증 트리 대신 상위 tests 패키지를 다시
불러오는 연결부 오류도 발견했다. 이는 V35 하네스에서 추가한 오류다. 해당 재귀
프로세스 34개를 종료하고, 각 subprocess의 작업 폴더에 맞는 상대 경로를 사용하도록
수정했다. 원본 검증 문장을 바꾸지 않고 올바른 원본 모듈을 실행한다.
새 외부 테스트 래퍼의 실행 제한은 1,800초이며, 내부 원본 검사의 900초 제한은
유지한다. 첫 실패 로그와 수정 전 proof/support 파일도 보존했다.

## 확인된 결과와 제한

| 검사 | 결과 |
| --- | --- |
| DATA와 등록 관련 집중 검사 | 45개 PASS |
| V35 복구와 V34 API, photorealism/cello 관련 재검사 | 18개 PASS |
| 준비 단계에서 막혔던 horror / water / runtime 과거 검사 | 9 + 7 + 6개 PASS |
| 원본 robe / palette / data-scope 검증 재현 | 3개 PASS |
| 현재 V35 pack/receipt 검증 | PASS |
| main 원본과 기존 실험 증거 보존 | PASS |
| 병합 후 고정된 세 컨셉 후보 재검색 | 3개 PASS |

첫 전체 실행은 214개 모듈에서 1,939개를 발견하고 1,917개를 실행했다.
22개는 위의 과거 연결 문제로 준비 단계에서 막혔으며, 수정 후 모두 실행해 통과했다.
전체 결과를 PASS로 표시하지 않는다. character 프로필 원본 비교의 13개 subtest,
shelf-return / krummholz / protostar의 번들 snapshot 차이, liminal의 후속 확장 차이는
정확한 원격 main 데이터와 원본 검증 문장에서도 재현됐다. 이번 선택용 확장을
liminal snapshot에서 제외한 뒤에도 같은 종류의 기존 실패가 남는다.

렌더 복구 4건의 오류는 같은 이름의 illustration/photo 감사 모듈이 임포트 순서에
따라 섞이는 기존 테스트 문제다. 원격 main의 원본 코드와 동일한 모듈 임포트 순서로
4건 모두 재현했다. 현재 모듈을 독립 실행하면 10개 모두 통과한다. 이 병합에서
사진 런타임이나 원본 감사 모듈을 변경하지 않았다.

과거 wrapper 재검사 결과와 최종 공개 변경 범위는 `MERGE-VERIFICATION.json`에 기록한다.
원래 작업 폴더를 맞춘 결과는 로컬 `PRIMARY-SYNC-VERIFICATION.json`에 기록한다.
그 폴더의 미공개 데이터가 함께 존재하는 현재 generation은 공개할 깨끗한 generation과
다를 수 있으며, 폴더를 맞춘 후 해당 입력에 맞게 인덱스를 다시 검증한다.

주요 증거: `FINAL-SCOPE-VERIFICATION.json`, `INDEX-REBUILD.json`,
`history/INDEX-VECTOR-PRESERVATION.json`, `HISTORY-RECOVERY-REPAIR.json`,
`full-suite/RESULT.json`, `UPSTREAM-CHARACTER-BASELINE-final.log`,
`UPSTREAM-OTHER-FAILURES-final.log`, `UPSTREAM-LIMINAL-final.log`,
`UPSTREAM-RENDER-FULL-IMPORT-ORDER-final.log`, `REPLAY-IMPORT-PATH-REPAIR.json`,
`ORIGINAL-WRAPPERS-import-fixed.log`.
