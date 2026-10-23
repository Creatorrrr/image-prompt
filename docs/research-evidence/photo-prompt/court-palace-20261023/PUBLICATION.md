# 궁중물 source·검증 결과 발행

1차 및 Chrome 전체 재검토 후 2차 작업을 함께 발행한다. 최종 원 항목은 본문 621개 + 표 밖 문맥 1개로 총 622개다. 열 머리글을 용어로 센 이전 623개 집계는 당시 기록으로 보존한다.

시각 대안 51개·진단 61개로 후보 112개, 선택적 연결 107개다. 기존 후보 4개는 검토된 한영·시각 표현만 수정하며 조건·효과·provenance는 유지한다. 기존 고증 보류 복합 카드 40개는 보류 상태다.

- [전체 대화 재검토·보강·적용 계획과 결과](full-review-r2/REPORT.md)
- [관측 요소·연결·혼동 경계와 출처](full-review-r2/RESEARCH-CATALOG.md)
- [1차 결과](INTEGRATION-AND-IMAGE-TESTS.md)
- [이식한 시험 증거 경로와 hash](EVIDENCE-PATH-MAP.json)

| 회차 | 실제 생성 | 신규 구조 통과 | 전체 기준/저술 장면 완전 충족 |
|---|---|---|---|
| 1차 | 3회, 재시도 0 | 1/3 | 0/3 |
| 2차 | 3회, 재시도 0 | 2/3 | 0/3 |

2차 새 후보 자연 검색 노출은 0/3이다. 직접 원본을 읽은 후 반영한 시험과 자연 검색을 구분한다. B는 core/baseline/slot-plan 고정 뒤 이전 회차 요약이 비의도적으로 노출되어 postcore까지 완전 미노출이었다고 주장하지 않는다. 사용자 수락과 고증은 별도이며 baseline 생성 비교가 없어 인과적 개선을 주장하지 않는다.

## 저장소에서 바로 볼 수 있는 2차 결과

- A: [프롬프트](full-review-r2/prompts/A.txt), [이미지](image-test-evidence/court-palace-20261023-r2-a/result.png), [보고서](image-test-evidence/court-palace-20261023-r2-a/REPORT.md)
- B: [프롬프트](full-review-r2/prompts/B.txt), [이미지](image-test-evidence/court-palace-20261023-r2-b/images/royal-music-salon-r2-b.png), [보고서](image-test-evidence/court-palace-20261023-r2-b/REPORT.md)
- C: [프롬프트](full-review-r2/prompts/C.txt), [이미지](image-test-evidence/court-palace-20261023-r2-c/corrected-run/images/court-ottoman-c-r2.png), [보고서](image-test-evidence/court-palace-20261023-r2-c/corrected-run/REPORT.md)

원본 보고서·receipt·ledger의 절대 경로와 hash는 당시 증거로 그대로 보존했다. 사본의 저장소 경로는 EVIDENCE-PATH-MAP.json에 연결한다. 역사적 checksum은 당시 snapshot용이며, 이후 수정된 시각 sidecar·공유 manifest·로컬 runtime 설정 전체가 아직 같은 바이트라는 뜻이 아니다. 이 발행본의 checksum은 PUBLICATION-SHA256SUMS로 별도 검증한다.

모델 사본·중단 빌드·successor-store·중복 인덱스 빌드 캐시는 발행하지 않는다. 원격 푸시 검증 이후 이번 작업의 중복 임시 데이터만 제거한다. 실제 이미지와 검증 증거 및 사용 중인 설치 runtime은 보존한다.
