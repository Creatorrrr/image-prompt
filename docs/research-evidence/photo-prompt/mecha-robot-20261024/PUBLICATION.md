# 메카 연구·보완의 main 발행

이번 발행은 메카 출처 141개(긍정 107·진단 34), 선택적 바인딩 231개, 의미 카드 109개/방향 관계 420개/용어 라우트 323개와 샘플링 v2 및 재시도 보존 검증 보완을 담는다. primary 체크아웃의 다른 연구·코드·삭제·런타임 설정은 가져오지 않았다. 공유 지침에서는 샘플링 문단과 메카 참조만 수정했다.

저장소 main의 native V3 출처 형식을 유지했다. 이미지 시험의 설치 세대는 별도의 canonical transport 표현을 사용한다. A12의 저장소 원문 SHA는 `5c2bf0a1e8fcfedb9e66cf907d4daea8e8bd4b403faa072075f2a08cd43a10f6`, 시험 설치본 SHA는 `e59ab2eab2d390e7609b1e50e6e2f9289b553548286e9a26980c770ef6c20f55`로 표현층이 다르다. 두 표현의 전체 원문, conditions, effects, provenance가 동일함을 확인했다. 관련 없는 형식 변환 코드는 끌어오지 않았다.

발행 전 회귀 66개가 통과했고, 기존 실제 부모 실행을 부모 자신의 검증된 봉인 코드로 재감사해 composed/runtime PASS를 확인했다(이미지 호출 0). 기존 main의 109개 출처 모듈 바이트를 보존하고 메카 2개 모듈만 추가했다. 호환되는 로컬 EmbeddingGemma-2 레시피로 인덱스를 재생성했다. 기존 벡터 20,695개를 재사용하고 신규 107개를 계산했으며 전체 20,802개 양성 레코드/22,005개 전체 후보의 layout 검증을 통과했다. pull/통합 뒤의 최종 검증은 별도 `merge-validation.json`에 기록한다.

이번 Git 발행은 설치된 기본 런타임과 CURRENT를 변경하지 않는다. [2차 시험 결과](repair-round-2/REPAIR-RESULTS.md)의 0/3 엄격 통과, 미채택·미노출 및 후속 초안의 미검증 상태를 보존한다. [최종 픽셀 대조](repair-round-2/FINAL-RESULTS.json)와 [원문 보존 검증](publication-evidence/source-preservation-initial.json)을 함께 확인할 수 있다. 과거 76개 검증은 당시 설치 세대 기준이며 이번 source publication 66개 검증과 구분한다.

## 보존한 이미지

| 안 | 최초 원본 | 2차 원본 |
|---|---|---|
| A | [외골격 최초](publication-evidence/images/original-a.png) | [외골격 재시험](publication-evidence/images/repair-a.png) |
| B | [메카 조종석 최초](publication-evidence/images/original-b.png) | [메카 조종석 재시험](publication-evidence/images/repair-b.png) |
| C | [로봇 팔 최초](publication-evidence/images/original-c.png) | [로봇 팔 재시험](publication-evidence/images/repair-c.png) |

이미지 6장은 실제 반환 원본과 바이트가 같다. 첨부된 개인 참조 사진 자체는 복사하지 않았다. `publication-evidence/runs/`에는 실제 프롬프트·조회 자료·관리 입력/감사 기록을, `ledger-a/b/c.ndjson`에는 이전 실패와 이번 결과를 함께 보존했다. 기록 안의 절대 경로는 당시 provenance로 남겼으며 현재 보기용 상대 경로와 해시는 `portable-images.json`에 있다.

전체 코퍼스 백업·중복 스킬/모델·빌드·임시 세대 저장소는 커밋에서 제외했다. 큰 백업은 해시·크기·제외 이유를 `omitted-local-backups.json`에 남겼다. 실제 이미지와 고정 테스트·실패 증거는 캐시로 취급하지 않는다. 푸시의 live SHA 확인 후 전용 워크트리와 이번 작업의 불필요한 캐시만 정리한다.
