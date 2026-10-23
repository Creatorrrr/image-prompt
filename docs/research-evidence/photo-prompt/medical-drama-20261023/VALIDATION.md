# 연구 무결성 검증

상태: `STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE`. 구조 검사 31/31 통과.

검사 범위는 원문 행 보존, 출처 접근 범위, 카드/경로 역참조, 한영 완전 문장, 소유·관계 노드, 정본 조건·효과 복사, 평가 입력 상태, 문서 링크와 파일 해시다. 임상 정확성 전체·실제 검색·native 승인·생성 이미지 성공을 검증한 것이 아니다.

보호 파일 13483개 중 변경 4개, 누락 0개. 읽은 코퍼스 payload 모듈의 현재 해시 변화 0개. HEAD 변경: False.

공유 checkout에서 관측한 변경은 별도 기록하며 reset/revert하지 않았다. 반영 직전에 manifest와 selected runtime을 다시 기준화한다. 원 코퍼스 스캔 중 manifest의 별도 전후 해시는 저장하지 않았으므로, payload의 해시 일치만으로 전체 manifest의 원자적 스냅샷을 주장하지 않는다.

- `skills/photo-prompt-image-generator/retrieval-runtime.json`
- `skills/photo-prompt-image-generator/references/maintenance.md`
- `skills/photo-prompt-image-generator/assets/photo_candidate_search.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json`

이미지·임베딩 호출 0회. 운영 파일 변경·등록·설치·활성화·commit/push를 수행하지 않았다. 읽기 전용 recorder/dependency 검사는 [runtime-readonly-check.json](runtime-readonly-check.json)에 별도 기록했다.

기계 판독 결과는 [VALIDATION.json](VALIDATION.json), 수량은 [SUMMARY.json](SUMMARY.json), 파일 해시는 [SHA256SUMS](SHA256SUMS)를 참조한다.
