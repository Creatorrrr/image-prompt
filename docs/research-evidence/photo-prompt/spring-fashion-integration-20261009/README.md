# 봄 패션 실제 반영 및 native 테스트 증거

소스·검색 반영 및 독립 arm 3개의 실제 생성·픽셀 테스트를 완료했다. 관찰 실패는 보존했고 사용자 판단은 pending이다.

- [최종 보고서](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md)
- [원 리서치](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-09-spring-fashion-visual-semantics-research.md)
- [281건 실제 ID 대응 및 현재 runtime](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/runtime-integration.json)
- [키워드 coverage](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/COVERAGE.json)
- [소스 통합 영수증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/PRIMARY-SOURCE-INTEGRATION.json)
- [단수 lookup V2 교정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/PRIMARY-LOOKUP-CORRECTION.json)
- [primary index 설치](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/PRIMARY-INDEX-INSTALL.json)
- [최종 runtime freshness](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/FINAL-RUNTIME-FRESHNESS.json)
- [소프트웨어 테스트 요약](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/TEST-SUMMARY.json)
- [기존 authored/source/작업 보존](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/FINAL-PRESERVATION.json)
- [세 native 테스트 정규화 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/FINAL-NATIVE-TESTS.json)
- [coordinator 직접 픽셀 관찰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/COORDINATOR-PIXEL-REVIEW.json)
- [동결 입력 및 호출 바인딩](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/INDEPENDENT-ARM-BINDINGS.json)
- [배달 PNG 원본 동일성](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/NATIVE-IMAGE-COPIES.json)

| arm | 개별 testcase | 신규 요소 all-of | 실제 hard set |
| --- | --- | --- | --- |
| A 강변 공방 | [TESTCASE](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/knit_layer/TESTCASE.md) | 4/5 FAIL | 11/11 PASS |
| B 옥상 청사진 | [TESTCASE](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/bodice_hem/TESTCASE.md) | 9/9 PASS | 8/8 PASS |
| C 비 뒤 선착장 | [TESTCASE](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-integration-20261009/arms/ornament_shoe/TESTCASE.md) | 10/10 PASS | 8/10 FAIL |

B는 별도 레이스 끝의 축소 관찰 실패가 있다. 모든 authorial 세부 관찰이 완전히 통과했다고 선언하지 않는다. 신규 Spring 프로필의 정식 opt-in/native hard 검증은 A의 `spring_sf057_02`에 한정된다. B/C는 실제 선택 bundle의 사전 보충 관찰이며 associated profile을 승격하지 않았다.

`finalize_native_evidence.py`는 arm마다 동결 12파일·managed 24파일, actual 1행 ledger, reference·skill·runtime·prompt·PNG hash와 리뷰 gate 집합을 검증한다. 내부 managed ledger와 독립 ledger는 동일한 실제 호출을 각각 기록하므로 이중 합산하지 않는다. 코드가 픽셀을 분류하는 것은 아니며 직접 관찰은 별도 JSON에 있다. `verify_preservation.py`는 기존 작업 보존 경계를 검사한다.
