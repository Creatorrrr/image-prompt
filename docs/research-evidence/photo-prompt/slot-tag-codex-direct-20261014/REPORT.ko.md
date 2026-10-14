# Codex 직접 의미 검토 — 실행 현황

2026-10-14. 전체 5~8단계는 진행 중이다. Gemini와 다른 생성 모델을 호출하지 않는다. 의미와 태그는 Codex가 원문을 직접 읽고 작성하며 임베딩은 기존 로컬 EmbeddingGemma 2만 사용한다.

## 5A — 직접 검토 기반

전체 canonical 18,250개·관리 역할 139개·기존 binding 12,089개의 현재 원본을 `SOURCE.json.gz`, `ORDER.json`, `CATALOG.json`, `BASELINE.json`에 고정했다. corpus SHA는 `125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b`, 활성 local layout은 `f82ab43bc2a5a141ad1aedcc1f415b68737b9e5867af829a6c88d6750f27a285`다. 기본값과 index의 공간은 같은 `embeddinggemma2-local / google/embeddinggemma-2 / 768`이다. 모델·원본·활성 index를 이번 준비 단계에서 바꾸지 않았다.

`direct_review.py`는 전체 원문과 전이 참조를 펼치고, Codex가 명시적으로 작성한 `authored/`의 판정만 source-bound `decisions/`로 결합한다. 태그·의미·확정 상태에 대한 기본값을 만들지 않는다. 원문·참조·catalog 변경, 부정 문구 인용, 가짜 인용, wildcard 소유자, 존재하지 않는 분기, 사실과 역할의 불일치, 미해결 모호성 및 진단의 positive 역할을 거부한다. 등록된 판정은 작성 파일의 실제 항목·hash와 전체 입력 packet에도 연결된다. 기계 검사를 의미 정확도 증거로 계산하지 않는다.

API 키를 제거하고 macOS `sandbox-exec`의 `deny network*`로 차단한 상태에서 init·prepare·verify와 직접 검토 계약 테스트 12개를 실행했다. 테스트는 전부 통과했고 baseline 검증의 직접 승인 수는 0개다. 과거 Gemini 초안은 수입하지 않았으며 신규 외부 모델 호출·로컬 임베딩 추론·이미지 생성은 0건이다. 준비된 원문을 출력한 사실만으로 직접 심사 완료로 계산하지 않는다.

이 커밋 범위는 검토 도구·새 기준·검증 증거와 수정된 계획/현황 문서다. 기존 미커밋 의미 근거·잠금 관련 운영 코드와 다른 작업 파일은 포함하지 않는다. `PRESERVATION.json`에 커밋 전 경계와 보호 문서 hash를 기록했다. 운영 원본·실행 코드를 바꾸지 않아 이 준비 단계에서는 index 재빌드나 runtime publication을 하지 않았다.

## 5B~8 — 남은 범위

직접 검토 승인 수는 `PROGRESS.json`을 기준으로 한다. 유효한 기존 Codex 파일럿의 재사용 여부도 실제 원문·근거·조건·참조를 확인하기 전에는 계산하지 않는다. 5B의 전체 의미 심사, 5C의 전체 역할 역점검, 6단계 다대다 관계 적용, 7단계 로컬 검색·샤딩·runtime 검증, 8단계 표본 재검토·레거시 정리는 아직 완료하지 않았다.

후속 배치마다 실제 판정·근거·보류와 검증 결과를 저장하고 커밋한 뒤 진행한다. 최종 직접 검토 18,250/18,250·미해결 0건 이전에는 5단계 전체 완료로 표시하지 않는다. 같은 Codex의 텍스트 검토를 독립 사람·전문가·이미지 픽셀의 검증으로 표시하지 않는다.
