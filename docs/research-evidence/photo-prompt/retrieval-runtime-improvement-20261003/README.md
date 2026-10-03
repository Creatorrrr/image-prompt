# 동결 코어 후보 조회 개선 — 2026-10-03

검증 대상은 후보 도달과 텍스트 계약이다. 공급자 호출과 이미지 생성은 0회다. 렌더링 품질이나 독립 평가자의 픽셀 판정 개선으로 해석하지 않는다.

## 변경

1. `affected_properties`가 누락되거나 비어 있어도 기존 공통 속성 계약을 적용한다. 관련 차원의 부분 잠금에서 불명 효과를 적합하다고 표기하지 않는다. 잠금이 없는 입력, 다른 차원, 명시적 다른 대상/속성은 기존 계약대로 허용한다. 선택 감사는 DATA 원본을 다시 검사한다. DATA에 임의 속성 경로를 붙이지 않았다.
2. 이미 동결된 의미 근거로 발견한 후보를 슬롯별 상한 안에서 보존하고, 남은 예산을 슬롯 순환으로 배분한다. 총량 64, 중복 억제와 결정성을 유지한다. 최초 순환 배분에서 편집 효과의 두 번째 발견 후보가 밀려난 회귀를 확인하고 수정했다. 기존 3개 편집 사례와 기대값은 그대로다.
3. 기존 required subject assertion의 `axes.subject_category`를 전달한다. 지원 범주는 human/animal/object/food/plant/environment/sign/unknown이다. generic/nonhuman 전체를 object로 허용하지 않는다. 타입 충돌과 명시적 human/no-people 문맥을 검사한다. 독립 작성 단계의 지침도 추가했다.
4. 슬롯 차원과 속성 소유 근거를 focal 질의로 전달한다. 서로 다른 근거 문장은 별도로 조회하고, 의미 있는 원문 용어의 겹침을 검사한다. 전체 기본문을 슬롯마다 복제하지 않는다. 카메라 위치, 물체 방향, 배경 밝기가 주체 조명 방향의 근거로 섞이는 부정 대조를 포함한다.

공개 후보는 계속 optional이고 순서는 `seed_shuffled_non_preferential`이다. 아래 후보 집합과 개수는 표시 순위를 검색 순위로 사용하지 않았다. 원시 검색 순위는 별도 로그에 있다.

## 동일 DATA 비교

원본 runtime은 `f4094afc28403c12f7a88f1a4d9f06f66d5757ef`, 개선 runtime의 비교 시점은 `4233043042d39cfb3a48ade87aa0d59e13f9c8a0`이다. 이후 커밋은 증거·대조군·현재 출력 경계의 후속 검증을 추가한다. 비교에 사용한 런타임 파일 해시는 [metrics.json](metrics.json)에 기록했다.

양쪽 모두 production `load_runtime_data`로 quality layers를 로드했다. DATA는 main의 `6b9381a` 소스이며 docs-only `f4094afc`까지 통합했다. 9,739 semantic entries, 1,510 profiles이고, 합성 DATA 지문은 양쪽 모두 `e0868dd1867e27b47fe03d99abe7fdf87c784f45ba28688ef68af436899c8c62`이다. 24개 입력의 JSON 해시와 정규화된 코어 해시가 전후 동일하다. 원본·속성 보정 입력과 과거 실패 기록을 덮어쓰지 않았다.

| 측정 | 원본 runtime | 개선 runtime |
| --- | ---: | ---: |
| 001 light_direction 노출, 원본/속성 보정 | 0 / 0 | 2 / 2 |
| 001 역광 후보 도달, 원본/속성 보정 | 없음 / 없음 | backlight / pe_rear_rim |
| 006 올려다보기 후보 도달, 원본/속성 보정 | 0 / 0 | 0 / 1 |
| 007 focus 노출, 양쪽 arm | 0 | 2 |
| 009–012 texture 노출, 사례당·양쪽 arm | 0 | 1 |
| 새 범주 대조의 허용 대상 surface_material 개방 | 1/6 | 6/6 |
| animal/human/unknown 표면 슬롯 차단 유지 | 3/3 | 3/3 |
| 새 소유 근거 4건의 정확한 문구 전달 | 0/4 | 4/4 |
| 배경/다른 차원 부정 대조의 잘못된 합성 후보 노출 | 1 | 0 |
| 원문 그대로·후보 미채택 작성 감사 | — | 24/24 통과 |

노출 증가가 의미 정확도나 채택 가능성의 증가와 같지는 않다. 예를 들어 원본 010의 ikat 질감은 요청에 부적절할 수 있다. 모든 노출 ID와 적합성 표기는 [metrics.json](metrics.json)에 남겼다.

과거 진단에서 원본/속성 보정 입력의 적합성 변경 **22건**을 초기 동일 DATA에서 재현했다. annotation 수정만 적용한 단계에서는 후보 ID 집합이 같고, 부분 잠금 arm에서 불명 효과 표기 91건이 추가로 eligible→ineligible가 됐다. 잠금 없는 arm의 표기는 바뀌지 않았다. 최신 DATA의 수정 전 비교에서는 21건이다. 과거 011의 silhouette 행이 최신 팩에 노출되지 않아 생긴 차이이며, 과거 22건을 최신 결과로 대체하지 않았다.

예산 고갈의 역사적 직접 추적은 007–012의 **6건**이다. 전체 12건의 원인을 예산으로 분류하지 않았다. 최신 비교의 총 후보 수는 수정 전 두 arm 모두 `[64,56,64,54,64,64,64,64,64,64,64,64]`, 수정 후에는 24건 모두 64다. 006의 카메라 후보 탈락은 해당 슬롯 처리 시 예산 0의 문제가 아니다.

## 남은 한계와 비용

- 원본 006은 여전히 실패한다. 현재 DATA의 올바른 broad 순위는 1/2/4이고, 원본의 focal 교집합은 전후 모두 0이다. 역사적 생산 추적의 1/2/5는 다른 DATA 시점의 기록으로 보존한다. 속성 보정 arm에서는 세 올바른 후보가 교집합에 들어오고 한 후보가 노출된다. 해당 49개 camera_direction 행은 효과 속성 범위가 없으므로 관련 부분 잠금에서는 계속 ineligible다. 도달과 채택 가능성을 분리했다.
- 과거 동결 object 코어에는 새 타입 전달이 없다. 009–012의 surface_material은 전후 모두 0이다. 이 입력에 타입을 덧붙이거나 요청에 object 별칭을 넣지 않았다. 새 범주 대조의 적합 결과는 예산 배분 전에 측정했다.
- 더 많은 슬롯을 먼저 조회하므로 조회 작업량은 늘어난다. 이 문서는 지연 시간 개선을 주장하지 않는다. 같은 64개 안에서 앞선 슬롯의 약한 대안 일부가 사라진다. 명시적 발견 후보의 손실은 기존 편집 대조로 검증했다.
- [새 대조군](../../../../tests/fixtures/photo_prompt/retrieval_runtime_holdout_v1.json)은 진단 12건과 별도로 첫 런타임 패치 전에 동결했다. SHA-256은 `bde3f5e98974bf7fc7fd4ef995c928c2e7aceea8f20883c9c50b5795105abdf3`이다. 같은 실행자가 작성했으므로 별도 평가자의 blind holdout이라고 주장하지 않는다. 후속 소유 차원/동등 경로 대조는 추가 검사로 구분한다.

## 현재 출력 경계와 역사 보존

기존 사진 V5의 입력으로 원본 출력 해시 `292672e1…`를 그대로 재현했다. 개선 출력은 `dd334295…`이며, 슬롯 수가 22→39가 됐다. 코어·creative controls·authorial composition·부정문과 네 입력 파일은 그대로이고 후보 수는 64다. 이전 바이트만 요구하던 형제 일러스트 검증기의 실패 로그를 보존했다.

[출력 계약 차이](photo-boundary-contract-delta.json)와 실제 [후속 출력](photo-boundary-after-pack.json)을 기록하고 별도 `photo_regression_baseline_v6.json`을 추가했다. V1–V5 파일은 수정하지 않았다. 새 검증은 V5의 해시 계보, 이전과 같은 실행 명령, 동결 입력 바이트, **원본 출력에서 계산한** 장면/작성 계약 해시를 검사한 다음 현재 바이트를 검사한다. 바이트 해시를 새로 계산해도 바뀐 장면은 허용되지 않는 부정 대조를 포함한다. 픽셀 판정·기존 의미 기대값은 바꾸지 않았다. 일러스트의 descriptive validator binding은 실제 소스 해시 한 값만 갱신했고, oracle·crosswalk·기대 결과·역사적 렌더 라벨은 그대로다.

## 검사와 재현

최종 검사 집계와 누락 자료의 원본 재현은 [test-summary.json](test-summary.json)에 기록했다. 현재 발견되는 **1,284개 테스트/144개 모듈**을 모두 실행했고 누락·중복 실행 ID는 0이다. 최초 최종 발견 1,278개에 후속 기준서 대조 6개를 추가하고, 보강된 소유 대조 모듈은 다시 실행해 최종 결과를 선택했다. 1,279개 메서드는 성공했고 5개 메서드는 기존 자료 누락으로 성공하지 못했다(실패 subtest 10건·오류 1건). 선택된 모든 모듈의 photo runtime/DATA 파일 해시는 최종 파일과 동일하다.

전체 검사는 모듈마다 새 offline 프로세스로 실행하며, 공급자 키를 프로세스 환경에서 제거하고 실행한 테스트 ID와 런타임/DATA 파일 해시를 저장한다. 완전 통과로 표시하지 않는다. 현재 저장 환경에는 기존 한국 감성 JPEG, 메이크업 코어/관찰 JSON, 빈곤 PNG, rare-photo 입력 JSON이 누락돼 있다. 이로 인한 실패 10건과 오류 1건은 최신 원본 main에서도 재현된다. 편집 효과 14개, 개선 대조 17개, 후속 경계 부정 대조 6개, 기존 경계 37개 및 일러스트 universal 대조 43개는 통과했다. 실제 이미지 생성과 픽셀 후속 검증은 실행하지 않았다.

저장된 `diagnostic-evidence.tar.gz`에는 frozen inputs, 원시 조회·24개 팩의 전후 결과, 단계별/최종 검사 로그와 수정 전 실패가 들어 있다. `SHA256SUMS`로 내용을 확인한다. 비교를 재현하려면 사양의 두 역사 arm을 추출하거나 이 아카이브의 `frozen` 폴더를 사용한다.

```bash
.venv/bin/python docs/research-evidence/photo-prompt/retrieval-runtime-improvement-20261003/evaluate.py \
  --runtime-repo /path/to/before-or-after \
  --data-repo /path/to/pinned-main \
  --frozen-inputs /path/to/extracted/frozen --output /tmp/retrieval-replay

.venv/bin/python docs/research-evidence/photo-prompt/retrieval-runtime-improvement-20261003/evaluate_holdouts.py \
  --runtime-repo /path/to/before-or-after --test-repo /path/to/implementation \
  --data-repo /path/to/pinned-main --output /tmp/retrieval-holdouts.json

.venv/bin/python docs/research-evidence/photo-prompt/retrieval-runtime-improvement-20261003/audit_replay.py \
  --repo /path/to/implementation --packs /tmp/retrieval-replay --output /tmp/retrieval-audits.json

.venv/bin/python docs/research-evidence/photo-prompt/retrieval-runtime-improvement-20261003/run_tests.py \
  --repo /path/to/implementation --output /tmp/retrieval-tests --workers 4
```

첫 탐색 검사와 최종 검사를 구분한다. 최초 대조의 rank spy 설정 오류, 잘못 지정한 두 테스트 모듈명, 경계 검증기의 후속 source binding 오류도 로그에서 제거하지 않았다. 최초 전체 실행 중 진행된 보완은 최종 소스로 다시 검사했고, 비교의 근거는 최신 `release-before`/`release-after` 및 소스 해시다.

원본 사양: [FOLLOWUP_SPEC.md](../renewed-blind-scene-retrieval-20261003/FOLLOWUP_SPEC.md), [상향 시점 생산 추적](../renewed-framing-optical-coverage-20261003/upward-view-production-trace.md).
