# arm-05 — alpine treeline ecotone gradient

기술 판정은 **PASS**다. 한 번 생성한 동일 PNG에서 target hard gate 5/5와 shared gate 5/5가 모두 통과했다. 사용자 미적 판단과 사용자 체감상 외관 유사도는 아직 `pending`이다.

## 독립 콘셉트

- 배정 키워드: `alpine treeline ecotone gradient`
- 시드: `966840007`
- 시드 장면: 밤사이 진눈깨비가 지난 뒤 첫빛이 드는 구름 낀 화산성 고개에서, 성인 산악 지도 제작자가 접은 등고선 지도를 읽는 환경 다큐멘터리 사진
- 구성 원칙: 인물은 오른쪽 약 1/4의 medium-full 크기, 환경 전이 구조는 나머지 프레임의 주 피사체
- 독립성: 다른 arm의 코어·프롬프트·후보팩·이미지·리뷰를 입력으로 사용하지 않았다.

## preflight

- raw requester envelope는 바꾸지 않았다.
- coordinator post-core recipe 진단에서 키워드는 정확히 `고산 수목한계 전이지대` 한 개 mixin으로 라우팅됐고, 배정된 6개 canonical candidate ID가 모두 대응 슬롯에 존재했다.
- v6의 locked/non-open 슬롯 public masking을 우회하거나 pack JSON에 ID를 수동 삽입하지 않았다.
- hard profile `alpine_treeline_forest_krummholz_tundra_gradient` 한 개가 활성화됐다.
- selected pack: `candidate_pack_final.json`, pack ID `cd19129a5efcb7e1`, SHA-256 `1ef1e906…acefa`.
- composed audit: blocking failure 0, PASS. 243단어가 권장 길이를 넘는 비차단 예산 경고는 hard evidence 보존 때문에 유지했다.
- runtime audit: PASS. exact intent-lock, negative bytes, appearance-reference path/SHA가 결속됐다.
- 초기 setup 부족 pack과 공개-slot 강제 점검 pack은 `preflight.json`에 실패·superseded 증거로 보존했다.

## 생성

- 도구: built-in `image_gen`
- 이미지 호출: 정확히 1회
- 의미 재시도: 0회
- 픽셀 재시도: 0회
- 원본 도구 경로: `/Users/chasoik/.codex/generated_images/01a05ba7-ac51-70f2-a6a2-5d14f5deed4e/exec-79c066a6-108f-4fb2-8f52-f4b306216ab0.png`
- workspace 보존 경로: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-05/render.png`
- 출력: 1537×1023 PNG, SHA-256 `6840602b277c8bcc5b3b84a14337c33e5389bf4f76609e9c4739bdb772cb0297`

## 픽셀 판정

| gate | scale | 판정 | 한 이미지에서 관찰한 근거 |
|---|---|---:|---|
| `vo_natural_treeline_lower_forest` | thumbnail | PASS | 좌하단 사면 기저에 조밀하고 연속적인 침엽수 수관림이 형성됨 |
| `vo_natural_treeline_sparse_transition` | both | PASS | 중간 사면으로 갈수록 직립 수목이 짧아지고 간격이 넓어짐 |
| `vo_natural_treeline_krummholz` | native | PASS | 직립 수목 위에 낮고 편향된 회녹색 목본 매트 띠가 넓게 이어짐 |
| `vo_natural_treeline_tundra` | both | PASS | 낮은 목본 띠 위 능선이 무수목 저생 식생·노출암 지대로 계속됨 |
| `vo_natural_treeline_non_inference` | native | PASS | 한 그루 왜소목·벌채선·설선이 아니라 네 단계가 같은 사면에 공존함 |
| `shared_single_saved_image` | both | PASS | SHA가 고정된 한 PNG만 high/original로 검토함 |
| `shared_environment_primary_legibility` | thumbnail | PASS | 환경 구배가 프레임 대부분을 차지하고 인물은 오른쪽 약 1/4에 머묾 |
| `shared_reference_appearance_continuity` | both | PASS | 성인 외관, 일반적 얼굴 인상, 자연 피부, 길고 짙은 부드러운 웨이브 머리가 보임 |
| `shared_reference_non_occlusion` | both | PASS | 인물이 오른쪽 전경에 제한되어 네 환경 단계가 각각 남아 있음 |
| `shared_photographic_coherence` | native | PASS | 원근·손과 지도 접촉·젖은 셸·배낭·진눈깨비·광원·사면 규모가 한 촬영으로 연결됨 |

review auditor 결과는 `technical_qualified=true`, `failed_hard_gates=[]`, `schema_failures=[]`다. `representative_eligible=false`는 기술 실패가 아니라, 이 비-moe visual contract에서 요청 사용자의 직접 판단이 아직 없기 때문이다.

## 외관 참고 경계

참고 JPEG는 새 이미지의 일반적 성인 외관 가이드로만 사용했다. 편집 대상이나 동일인 증거로 다루지 않았고, 생체 신원·보호 특성·건강·매력·성격·사회적 지위를 추론하지 않았다. 소스의 의상·장신구를 복제 의무로 사용하지 않았다.

## 증거 파일

- `preflight.json`: route/canonical data/hard profile/초기 setup 실패 경계
- `composed_prompt.json`, `composed_audit.json`: 최종 프롬프트와 blocking audit
- `runtime_request.json`, `runtime_audit.json`: 실제 런타임 텍스트와 reference 결속
- `render.png`: 같은 이미지 한 장의 픽셀 증거
- `pixel_review.json`, `pixel_review_audit.json`: 5 target + 5 shared gate와 review audit
- `run_manifest.json`, `image_runs.ndjson`: 1회 호출·독립성·lineage 기록
- `artifact_hashes.json`: 입력부터 출력까지 해시와 치수
