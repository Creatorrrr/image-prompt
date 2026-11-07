# 코스프레 데이터 반영 및 검증 상태

작성일 2026-11-06. [조사 및 계획](../../../research/cosplay-visual-semantics-research-plan-20261106.md)의 356개 표 행은 `inventory.json`과 시각 의미 레지스트리의 `source_term_inventory`에 추적한다. 356은 표 행의 개수이고 신규 시각 후보의 수가 아니다. 용어의 개별 정의·기존 후보 재사용·차이와 추가 근거에 대한 전수 검토는 아직 하지 않았다. 새 사례와 연결한 49개 행도 전체 의미가 구현됐다는 주장이 아니다.

소스에는 새 선택적 시각 명제 48개, 의미 경계 진단 15개, 선택적 바인딩 48개, 전체 명제 뷰 48개와 코스프레 맥락 뷰 48개를 작성했다. 후보·진단·바인딩의 구조, 참조, 뷰의 문장·해시 검증과 corpus load를 통과했다. `test_candidate_retrieval_views.py`와 `test_h_f2_complete_meaning.py`는 9 passed, 12 skipped, 4 subtests passed다. 스킵된 항목은 통과가 아니다.

영문 토큰 겹침 조사 `lexical-neighbors.json`은 의미 동등성 심사가 아니다. 가장 가까운 예로 새 C01은 기존 `cand_828caec7c92258ab873ddda2d9004140`의 원피스 몸통–다리 연결과 매우 비슷하고 캣수트 명칭이 명시된 점이 다르다. C13은 기존 `cand_f1544c08152351d8bb255f67ee1c40c8`의 바니 칼라·커프스 문장과 겹치되 기존 후보는 몸판 가장자리와의 구별을 추가로 요구한다. 두 쌍의 순위 영향과 중복 해소는 추가 검토가 필요하다. 점수·부분 텍스트만으로 전체 조건과 효과가 같다고 확정하지 않는다.

H-F2 `02329ce6b6d82034e8444d916e9ed3073738d33c7582a5874da0e2f2dd58ec21`, native `3f89e4be96d6853b156bf9838877e73555b1661f6757f88939d349c7eeaf1101`을 설치했다. 기존 봉인 세대에서 출발했고 신규 positive 48개와 뷰 96개의 임베딩을 포함해 전체 검증했다. 진단은 positive 문서에 포함하지 않는다. 설치된 `--check-runtime`은 통과했다. 원본 등록·검색 결과·프롬프트 사용·픽셀 적합·인과 개선을 별도 증거로 다룬다.

검색 비교와 세 독립 이미지 테스트는 완료 후 이 문서에 별도 추가한다.

## 개발 검색 진단

작성자가 후보 내용을 알고 만든 한영 질의 5개에서 지정 신규 후보가 모두 1위였다. 견갑골 해부학 및 카페 서버 대조 질의 2개는 이전 세대와 새 세대의 top-10 후보 ID와 순서가 같았다. 실제 같은 저장된 query embedding을 사용해 BM25F·local cosine을 실행했다. 상세는 `generated/cosplay-hf2-v2-20261106/retrieval-summary.json`과 양쪽 `evaluation-*.json`이다. 이 검사는 독립 holdout이 아니며 전 영역 검색 성능이나 회귀 부재를 보장하지 않는다.

## 세 독립 이미지 시험

각 테스트는 동일 사용자 요청과 참조 이미지에서 서로 다른 콘셉트·독립 baseline과 검색 질의를 검색 전에 동결했고 설치 세대 `02329ce6…`에서 검색했다. 각자 1회 생성했으며 새 후보들은 H-F2 자료를 `inspiration_only`로 검토해 저자 문구에 반영한 것으로, native 선택은 모두 0건이다. 합성과 렌더 사전 감사는 모두 통과했고 사용자 의도 보존에 관한 경고 각 4건이 있었다. 인물의 연령을 사진만으로 확정하지 않고 비성적 콘셉트를 사용했다.

- A 천문대: `generated/cosplay-test-a-authoring/result.png`, `final-prompt.txt`, `pixel-observation.md`. 열린 책을 한 손으로 받치고 다른 손으로 세운 지팡이를 잡는 새 사례가 보인다. 목 보호구와 별도 흉갑의 앞·옆은 보이나 목 뒤 경로는 미관찰이다.
- B 변신 히로인: `generated/photo-runs/cosplay-20261106-b/image.png`, `pixel-observation.md`, `generated/photo-runs/cosplay-20261106-b-preparation/final-prompt.txt`. baseline에도 별 마법봉은 있었고 검색 후 다섯 갈래 별과 가느다란 봉이 구체화됐다. 별·봉·손의 연결이 보인다.
- C 고딕 자동인형: `generated/cosplay-c-precore-20261106/image.png`, `final-prompt.txt`, `pixel-observation.md`. 태엽과 한 손의 접점이 보인다. 다른 손은 상자의 오른쪽 옆면/아래 가장자리 부근이어서 밑면 지지는 확인되지 않는다. 해당 신규 후보의 전체 관계는 부분 관찰이고 pass가 아니다.

각 도구 응답이 실제 파일 경로를 제공했지만 브리지가 `preview_only`로 기록해 정상 native-result 재연결은 `native_operation_not_started`, review-audit은 `review_result_not_bound_to_observed_attempt`로 거부됐다. 원본 파일·사전 감사·시각 관찰은 남아 있지만 관리형 픽셀 감사가 통과한 것은 아니다. 추가 호출이나 원기록 조작은 하지 않았다. baseline 이미지나 눈가림 대조가 없고 반복도 없으므로 새 데이터의 인과적 개선과 사용자 수용은 미평가다.
