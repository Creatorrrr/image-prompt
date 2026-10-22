# 메디컬 호러 main 반영

메디컬 호러의 의미 카드 86개·한영 경로 181개, 새 시각 후보 61개와 문맥/진단/보류 기록 23개, 선택적 연결 183개를 반영한다. 기존 봉합선·배양 용기 후보 2개는 그대로 재사용한다. 장르 이름은 고정된 시각 의무를 활성화하지 않으며, 모든 새 소스의 native_approval은 false다.

공유 기본 체크아웃의 다른 주제 데이터와 코드 수정은 제외하고, 별도 워크트리에서 원격 main의 원본 모듈과 정책을 보존한 채 메디컬 호러 모듈 2개만 manifest에 추가했다. 이 조합의 검색 인덱스는 검증된 기존 벡터와 정확히 일치하는 의료 후보 캐시로 재구성했다. 설치된 실행 세대 선택과 전역 CURRENT는 이 게시 작업에서 변경하지 않는다. 원격 main 갱신은 커밋 후 실제 pull로 다시 병합한다.

## 이미지 테스트의 실제 결과

아래는 앞서 독립 에이전트 3개가 각각 한 번씩 생성한 결과다. 이번 Git 게시 과정에서 추가 이미지를 생성하지 않았다. 세 사례 모두 PARTIAL이며 엄격한 전체 사례 판정은 FAIL이다.

| 콘셉트 | 보이는 내용 | 남은 실패 | 신규 소스 기여 |
|---|---|---|---|
| 퇴원 창구 | 빈 봉투·유리 너머 차트·출구 빗장 | 봉투 지지와 좌우 손, 제한적인 호러 강도 | 새 후보 미채택 |
| 진단 스캐너 | 링·플랫폼·문 관계와 손바닥 접촉 | 플랫폼이 인물 대신 카메라 쪽으로 뻗음 | 새 후보 미채택 |
| 동결보관실 | 투명 표본·액면·서리 대비·표본 위에서 멈춘 손 | 좌우 손 반전, 현미경 지지점 가림 | A08 창작 참고. 보이는 장비군은 실현됐으나 전체 소스 관계는 PARTIAL |

### A: 퇴원 창구

[프롬프트](publication-evidence/arms/a/final-prompt.txt) · [에이전트 보고서](publication-evidence/arms/a/arm-a-report.md)

![퇴원 창구](publication-evidence/arms/a/generated-image.png)

### B: 진단 스캐너

[프롬프트](publication-evidence/arms/b/final-prompt.txt) · [에이전트 보고서](publication-evidence/arms/b/REPORT.md)

![진단 스캐너](publication-evidence/arms/b/image.png)

### C: 동결보관실

[프롬프트](publication-evidence/arms/c/final-prompt.txt) · [에이전트 보고서](publication-evidence/arms/c/report.md) · [신규 A08 전체 관계 판정](publication-evidence/arms/c/source-contribution-gates.review.json)

![동결보관실](publication-evidence/arms/c/rendered/cryobank-thaw-anomaly.png)

세 이미지의 원래 검색은 설치 세대 `3ed7d4cd1bacbf4bea873116a5ff51b113e6f9ed5b983889d85f84933fd533b5`에 고정됐다. 이를 이번에 정리한 main 조합의 새 실행 결과로 보고하지 않는다. 검색 노출, 원본의 native 자격, 창작 참고, 프롬프트 운반, 이미지 충족과 사용자 수용은 별도의 증거다. A/B의 임상 코어를 새 데이터의 효과로 돌리지 않으며, C도 전체 소스 통과나 인과적 품질 향상을 입증하지 않는다.

## 보존과 검증

최초 연구 파일과 기존 integration-evidence는 역사적 기록으로 바이트 그대로 보존한다. 원래 NOT_RUN과 후속 실제 실행을 혼동하지 않는다. 특히 종료 시 공통 코드·스킬에 동시 변경이 관측된 기록을 PASS로 고치지 않았다. [기존 최종 보고서](integration-evidence/FINAL-RESULTS.md)의 절대 경로는 당시 실행의 위치이며, 이 문서의 상대 링크가 게시된 이미지·프롬프트의 저장 위치다.

[원본 실행 보관 목록](publication-evidence/arm-archive.json)은 `.staging`, `__pycache__`와 일시적인 빈 잠금 파일을 제외한 3개 실행 파일의 원래 해시를 보유한다. 매니페스트·원장·리비전·전체 소스 검토와 실제 이미지를 바이트 그대로 보관했으며, 사용자의 입력 JPEG는 복사하지 않고 원래 참조 해시를 유지했다.

[게시 조합 인덱스 검증](publication-evidence/index-build.json)과 [게시 검증 결과](publication-evidence/validation.json)에 최종 후보 수, 소스 보존, 물리 인덱스 closure 및 검사 범위를 남긴다. 커밋·원격 SHA·정리 완료는 푸시 후 기본 작업공간의 `generated/maintenance/medical-horror-publication-20261022/`에 별도 기록한다.
