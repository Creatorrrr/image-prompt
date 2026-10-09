# 가을 패션 반영·생성 검증 증거

[사람이 읽는 최종 보고서](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-09-autumn-fashion-integration-and-native-tests.md)와 [FINAL-RESULTS.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-integration-20261009/FINAL-RESULTS.json)이 현재 결론이다. 원본 연구·maintenance·작성 시점의 상태값은 과거 기록으로 보존했으며 최종 결과로 다시 쓰지 않았다.

데이터는 신규 후보·프로필 각각 112개, 기존 계약 재사용 17개다. 실제 native 호출은 3회, 추가 호출은 0회다. 현재 hard 기준은 1개 사례 PASS·2개 FAIL이며, 신규 후보의 관계는 채택된 2개 중 1개 PASS다. 신규 visual profile은 검색 결과에 노출되지 않아 픽셀 인증 0개다. 사용자 판단은 아직 없다.

| 증거 | 위치 |
|---|---|
| 원본·native 프롬프트 | images/ 및 prompts/ |
| 347개 용어의 반영 위치 | term-runtime-map.json |
| 원본 작성·재사용 결정 | runtime-integration.json, author_autumn_fashion.py |
| 보호한 초기 작업 | PRIMARY-BEFORE.json, PRIMARY-TRACKED-BEFORE.zip |
| 주 폴더 최종 검사 | PRIMARY-FINAL-DICTIONARY.log, PRIMARY-DELIVERY-AUTUMN-TESTS.log |
| 주 폴더 runtime publication | PRIMARY-DELIVERY-RUNTIME.log |
| 전달 직전 동시 변경 보존 | PRIMARY-DELIVERY-CONCURRENCY.json |
| 관련 82개와 추가 embedding 경계 1개 | focused-tests.log, embedding-paraphrase-tests.log |
| 전체 실행·실패 구분 | full-suite-parallel/summary.json, FULL-SUITE-CLASSIFICATION.json |
| 변경 전 재현 | BASELINE-BEFORE-AUTUMN.json, baseline-*-failures.result.json |
| 부모의 직접 원본 확인 | ROOT-NATIVE-REVIEW.json |
| exact 파일·입력·호출 수 검증 | DELIVERY-VALIDATION.json, build_final_delivery.py |
| 정확한 복사 원장 | ARM-1/2/3-DELIVERY-COPY.json, EVIDENCE-DELIVERY-COPY.json |

각 arm의 장부·독립 manifest v2·frozen core·감사·모든 미실행 수정 준비는 [주 폴더의 run 디렉터리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/autumn-fashion-integration-20261009)에 있다. 2번의 폐기된 초기 컨셉도 arm_2에 보존되어 있으나 native 호출은 없다.

Frozen JSON의 경로를 치환하지 않았다. 원본 경로와 runtime snapshot은 `/Users/chasoik/.codex/worktrees/autumn-fashion-20261009/image-prompt`에 보존되어 있다. 동일 snapshot의 대용량 중복 파일은 주 폴더로 다시 복사하지 않았다. 이 디렉터리의 images/는 도구가 반환한 원본과 같은 SHA-256의 복사본이다.

생성 장부의 success는 이미지 반환 사실이다. 이미지 품질·의미 관계 PASS와 동일한 상태값으로 해석하지 않는다. 스킬·검색 제어 코드는 변경하지 않았으며 커밋·푸시·PR은 수행하지 않았다.
