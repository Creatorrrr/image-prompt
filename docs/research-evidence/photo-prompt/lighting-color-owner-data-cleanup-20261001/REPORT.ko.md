# 색조 영역과 국부 조명 owner 정비

## 결과

고정한 40행 중 5행의 `relations[0].object`만 수정하고 35행은 그대로 유지했다.

- warm-highlight/cool-shadow: 물체 색 계열 대신 영상의 밝은 계조·어두운 계조 영역
- teal-shadow/orange-midtones: 그림자 계조와 선택된 중간톤 영역
- red-object splash: 선택한 빨간 물체와 무채색으로 남는 나머지 영상 영역
- cheek triangle: 그림자 쪽 뺨의 눈 아래 국부 영역
- silhouette: 어두운 피사체 내부·외곽과 밝은 배경의 관계

원래 개념 단위와 라벨에 이미 있던 소유 범위를 명시했다. 영어·한국어 라벨, 별칭, 개념 단위, 가중치, 적용 조건, 영향 속성은 바꾸지 않았다. S-curve의 input-to-output tone 관계는 구현 의미와 충돌하지 않아 유지했다. 물리적 광원·반사 조명 및 composition 관계도 그대로다. ceiling-bounce에 천장이 화면 안에 보여야 한다는 조건을 추가하지 않았다.

불변 연구 provenance 기록은 원래 연구 원장을 결속하므로 그대로 유지했다. `pe_bundle_red_splash_detail`, `pe_bundle_warm_luminous_skin`의 해당 member owner만 원본 행에서 정상적으로 파생된다.

## 사전 고정 진단

영어 양성 7개와 near-miss 7개를 고정했다. 독립 사전 검토에서 중립 그림자, 중간톤 압축, 천장 반사에 관한 세 문구를 명확히 한 뒤 고정했으며, 평가 후 문구는 바꾸지 않았다.

| 항목 | 결과 |
| --- | --- |
| Dense 양성 | 7/7이 1위로 유지 |
| Lexical 양성 | 6/7이 1위, warm split-tone은 기존 3위 유지 |
| Dense near-miss | silhouette q10 8→9, 나머지 6개 동일, 상승 없음 |
| Lexical target 순위 | 14개 전부 동일 |
| 상위 5개 ID 순서 | 두 방식의 14개 검색문 전부 동일 |

기존 한계는 남는다. 물체 자체의 teal/orange 색을 묻는 q04가 tonal-region 후보를 dense·lexical 모두 1위로 찾고, 주변도 컬러인 빨간 우산 q06이 dense에서 red-splash를 1위로 찾는다. 밝은 피사체/어두운 배경으로 반전한 q10도 lexical에서 silhouette가 1위다. 따라서 결과는 원본 소유 관계의 정확성 개선이며, 검색이 이런 의미 차이를 해결했다거나 최종 이미지가 좋아졌다는 주장이 아니다. 함께 존재할 수 있는 효과를 강제로 배제하는 필터도 추가하지 않았다.

## 독립 검증과 비용

독립 read-only 검토가 40개 baseline 행, 5개 수정·35개 보존, 두 bundle 파생, 실제 index/BM25와 모든 56개 baseline/final method-query 결과 행을 재현했다. 10,174개 문서 중 5개만 새 벡터이며 10,169개는 baseline과 정확히 같다.

새 문서 5개와 검색문 14개, 총 19개 입력(UTF-8 5,295 bytes)을 각 한 번 처리했다. 실패나 재시도는 없다. 추가 보수적 비용 상한은 $0.0311296, 추적 누적은 $1.0502144다. 실제 청구액이 아니며 별도 upstream 작업의 비용은 대조하지 않았다.

현재 dictionary metadata, 변경 없는 visual-profile index, DATA/background 133개와 effect/bundle/profile 40개, 총 173개 관련 테스트가 통과했다. 최신 main pull 이후의 검증과 정상 push/remote 확인은 별도 publication 단계로 남아 있다. 전체 저장소 테스트 또는 렌더링 품질의 통과로 확대 해석하지 않는다.

## 재현

이 사이클의 publication commit checkout에서 API 키 없이 다음 명령을 실행한다. 이후 main의 다른 DATA 수정이 반영된 상태는 이 고정 snapshot과 같지 않다.

`python3 docs/research-evidence/photo-prompt/lighting-color-owner-data-cleanup-20261001/evaluate_cycle.py --replay`
