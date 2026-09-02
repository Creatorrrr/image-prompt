# 사진 조명 시각 의미·후보팩 3-arm 평가

- 실행일: 2026-09-02
- 참조 이미지: `shared/reference.jpeg`
- 참조 범위: 보이는 성인 외형만 사용. identity, same-person, biometric, protected-trait 판단 없음.
- 정책: arm별 입력 동결, 기록된 native imagegen 1회, retry/fallback/cross-arm input 0, `partial_is_fail`.

## 구현 결과

- 신규 hard visual profile 22개와 기존 3개 재사용 경계를 registry에 반영했다.
- 12개 coherent lighting cluster, 84개 후보를 extension에 반영했다.
- visual profile index는 300 profiles / 1,568 exact terms로 재생성했다.
- semantic index는 7,974 entries / 768 dimensions / 16 shards로 재생성했다.
- focused 회귀 10개와 관련 조명 의미 회귀 21개, 총 31개가 통과했다.
- 각 cluster의 7개 후보는 완전 구성요소 query에서 BM25F top 14 안에 모두 검색됐다.

## 독립 생성 결과

| Arm | 무작위 복합 컨셉 | 목표 hard profile | 프롬프트/런타임 | 픽셀 게이트 | 공개 후보팩의 목표 cluster/anchor |
|---|---|---|---|---:|---|
| A | 진눈깨비 속 폐쇄 케이블카 신호실에서 기상 일지를 수작업 제본 | `motivated_practical_mixed_interior_relation` | PASS / PASS | 5/5 PASS | FAIL: 미노출·선택 불가 |
| B | 해안 안개 수확 시설에서 메쉬를 수리하고 응축수를 채집 | `volumetric_occluded_light_shafts` | PASS / PASS | 1/5 FAIL | FAIL: 미노출·선택 불가 |
| C | 거울 징 실험실에서 반사막의 동심 파문을 작동 | `film_halation_highlight_edge_relation` | PASS / PASS | 5/5 PASS | FAIL: 미노출·선택 불가 |

총 15개 strict gate 중 11개가 통과했다. Arm B는 장애물 후보는 보이지만, 독립된 빛기둥과 어두운 틈, 공기 중의 제한된 광 경로, 표면에 닿는 bounded shaft가 없어 4개 gate를 실패했다.

## 증거 층 판정

1. 소스·데이터: PASS — 22 profiles, 12 clusters, 84 candidates가 파싱·병합·인덱싱된다.
2. 후보 검색: PASS — focused BM25F 회귀에서 cluster별 7/7 후보가 top 14 안에 든다.
3. 공개 후보팩 표면: FAIL — 세 arm 모두 hard profile과 5개 gate는 노출되지만, 요청한 cluster ID와 forced anchor candidate ID는 public v6 pack에 나타나지 않아 composer 선택 증거가 없다.
4. 프롬프트·런타임: PASS — 3/3 composed audits, 3/3 render-request audits.
5. 렌더 픽셀: PARTIAL/REVISE — A와 C만 5/5; B는 1/5. 전체 11/15.
6. 사용자 판단: PENDING — 기술 판정과 별도다.

따라서 이 실행은 hard-profile 경로가 두 조명 의미를 실제 픽셀에 전달할 수 있다는 증거이지만, 3개 의미 전부의 성공이나 신규 candidate record의 공개 후보팩 선택 성공을 증명하지 않는다.

## 아티팩트

- `shared/root_pixel_cross_review.json`: root의 native/thumbnail 교차판정
- 각 `arm-*/arm_result.json`: 에이전트별 독립 결과
- 각 `arm-*/candidate_pack.json`, `composed_prompt.json`, `render_request.json`: 데이터→프롬프트→런타임 계보
- 각 `arm-*/pixel_review.json`: gate별 픽셀 근거
- 각 `arm-*/image_runs.ndjson`, `run_manifest.json`: 이미지 호출 원장과 독립성 기록
