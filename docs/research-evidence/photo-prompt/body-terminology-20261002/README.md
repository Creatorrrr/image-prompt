# 신체 용어 조사와 데이터 보강 계획

2026-10-02. 최초 조사에서는 연구 문서와 제안만 작성했다. 이후 사용자 요청에 따라 데이터와 검색 인덱스를 실제 반영하고 독립 이미지 시험을 진행했다. 최신 실행 기록은 [통합·검증 기록](integration/README.md)을 참조한다. 아래 기준선과 제안 70사례는 최초 조사 시점의 기록이다.

먼저 [상세 조사 보고서](RESEARCH.md), 이어서 [단계별 반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다. 원 대화의 19개 장을 기반으로 415개 표현 그룹을 정리하고 출처 47건을 검토했다. 현재 로더 기준 1,419개 시각 프로필과 9,590개 후보를 기준선으로 삼았다.

| 산출물 | 내용 |
|---|---|
| [SOURCE-NOTES.md](SOURCE-NOTES.md), [SOURCES.json](SOURCES.json) | 출처 47건, 확인 범위와 주장 한계 |
| [TERM-INVENTORY.json](TERM-INVENTORY.json) | 373개 표 행에서 정규화한 415개 표현 그룹 |
| [CONVERSATION-RECEIPT.json](CONVERSATION-RECEIPT.json) | 커넥터 절단과 브라우저 전체 확인 기록 |
| [CURRENT-DATA-AUDIT.json](CURRENT-DATA-AUDIT.json) | 병합 코퍼스 기준선, 집중 점검 프로필 39개, 소스 69건 해시 |
| [SEMANTIC-PROPOSALS.json](SEMANTIC-PROPOSALS.json) | 형상·관계 축 91개, 지식/문맥 레코드 11개 |
| [AXIS-CATALOG.md](AXIS-CATALOG.md) | 91개 축을 사람에게 읽기 좋은 부위·구성요소·반례·출처 형태로 정리 |
| [CANDIDATE-PROPOSALS.json](CANDIDATE-PROPOSALS.json) | 후보 초안 91개, 차원·효과·조건·소유권 검토 상태 |
| [PROPOSAL-SPECS.psv](PROPOSAL-SPECS.psv) | 구체 축의 저작 입력. `\|`로 구분한 저작 입력 |
| [EXISTING-OWNER-MAP.json](EXISTING-OWNER-MAP.json) | 재사용 대상으로 명시한 15개 프로필의 현재 소유 파일 |
| [COVERAGE-MAP.json](COVERAGE-MAP.json) | 전체 표현의 라우팅 방침과 장별 관련 축. 동의어 확정 매핑이 아님 |
| [REGRESSION-CASES.jsonl](REGRESSION-CASES.jsonl), [REGRESSION-SPECS.psv](REGRESSION-SPECS.psv) | 긍정·반례·다의성·잠금·해부·픽셀 판정의 제안 70사례, 미실행 |
| [VALIDATION.json](VALIDATION.json) | 파일·참조·초안 구조·기준선 보존의 실제 검사 결과 |

91개 축 중 15개는 기존 프로필 재사용을 명시했다. 나머지는 전체 코퍼스의 중복 검토가 필요하며 신규 프로필 개수의 확정값이 아니다. 후보 4개는 현재 슬롯 차원보다 넓은 효과가 있어 소유권 분리 검토를 표시했다. 모든 연구 초안은 `export_allowed=false`이며 실제 core target/property에 바인딩하기 전에는 런타임에 옮길 수 없다.

반영 우선순위는 P1 기본 형상·혼동 24개 → P2 국소 형태·상태 35개 → P3 피부·체모·옷 경계 19개 → P4 명시적 해부·의복·장치 문맥 13개다. 근거가 부족한 한국어 압축어와 일부 은어는 정의를 추가 확인한 뒤 exact 별칭 승격을 검토한다.

## 재현

저작 입력을 수정한 뒤 이 디렉터리에만 연구 JSON을 재생성하고 검증할 수 있다. 첫 명령은 연구 산출물을 덮어쓰므로 독립적으로 편집한 결과가 있으면 먼저 보존한다. 실제 데이터 감사 재실행은 현재 기준선을 다시 만드는 작업이므로 기존 증거 파일을 보존한 뒤 별도 비교 작업으로 한다.

```bash
.venv/bin/python docs/research-evidence/photo-prompt/body-terminology-20261002/build_research_artifacts.py
.venv/bin/python docs/research-evidence/photo-prompt/body-terminology-20261002/validate_research_artifacts.py
```

검증 스크립트는 문서·참조·현재 소스 해시를 확인한다. 검색 평가·runtime audit·렌더·사용자 수용을 실행하지 않는다.
