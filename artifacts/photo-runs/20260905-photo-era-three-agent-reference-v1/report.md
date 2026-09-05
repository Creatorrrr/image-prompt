# 사진 시대 시각 의미·후보팩 구현 및 독립 렌더 검증

## 결론

구조 및 프롬프트 계층은 구현·검증되었지만 전체 렌더 승격 판정은 `revise`다. 세 하드 프로필 모두 v6 후보팩과 합성 프롬프트에 정상 결합됐고 프롬프트·런타임 감사도 모두 통과했다. 실제 저장 픽셀에서는 미니랩 직광 인화물과 스마트폰 초광각 근원근이 각각 5/5를 통과했지만, 알부민 카드 마운트는 이미지층 한정 광택과 전반적 미세 크랙/섬유가 분리되어 보이지 않아 3/5로 실패했다. 총점은 13/15이지만 `partial_is_fail`이므로 기술 통과는 2/3 프로필이다.

별도로 새 후보 원소는 등록·색인됐으나 이번 세 랜덤 복합 요청의 공개 v6 후보 표면에는 요청한 8개 중 0개가 노출됐다. 하드 시각 의미 활성화 성공과 후보 원소 노출 실패는 서로 다른 결과로 유지한다.

## 데이터 반영

- 시각 의미 확장: `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_photo_era.json`
  - 18개 좁은 프로필
  - 프로필마다 5개 필수 구성요소, 5개 프롬프트 증거 필드, 5개 픽셀 게이트, 5개 근접 대체물 거부
- 후보팩 확장: `skills/photo-prompt-image-generator/assets/photo_prompt_photo_era_extension.json`
  - 새 후보 59개
- 기존 세피아 후보 교정: `skills/photo-prompt-image-generator/assets/photo_prompt_tags.json`
  - `sepia`를 `sepia_treatment_without_age_claim`으로 바꿔 세피아 색조만으로 연대를 주장하지 않도록 함
- 제안서 총계: 후보 60개, 시대/공정/출력/열화 계열 23개
- 런타임 로더: `skills/photo-prompt-image-generator/scripts/prompt_generator.py`
- 재생성 색인:
  - 시각 프로필 354개, 정확 용어 1,758개
  - 의미 항목 8,142개, Gemini embedding 768차원
  - dictionary hash `7b892ae82b33f86d15c3c9cb64ffc6f45547cf5e7afd12b3e398584dce968c8a`

## 소스 및 회귀 계약

- 조사 근거 27건: `docs/research-evidence/photo-prompt/photo-era-visual-semantics-20260905/evidence.jsonl`
- 상세 근거 보고서: `docs/research-evidence/photo-prompt/photo-era-visual-semantics-20260905/report-source.md`
- 후보·프로필 제안: `docs/research-evidence/photo-prompt/photo-era-visual-semantics-20260905/candidate-data-proposal.json`
- 라우팅 계약 71건: `docs/research-evidence/photo-prompt/photo-era-visual-semantics-20260905/routing-regression-proposal.jsonl`
- 구현 테스트: `tests/test_photo_era_visual_semantics.py`
- 해시 결합 3-arm 픽스처: `tests/fixtures/photo_prompt/photo_era_three_arm_pixel_test_cases_v1.jsonl`

검증 결과:

- 사전 메타데이터: PASS
- 현재 장면 표현 감사: 112/112 PASS
- 시각 프로필 색인 검사: PASS
- 의미 색인 검사: PASS
- 사진 시대 집중 테스트: 8 tests 및 214 subtests PASS
- 프리셋 모순 검사: 2,118 생성, 위반 0
- 일반화: 79/79 PASS
- 기존 일반 홀드아웃: 24/24 PASS
- 도메인 홀드아웃 v2: 6/6 PASS
- 프리셋 없는 의미 검색 홀드아웃 v4: 22/22 PASS
- 더 넓은 관련 유지보수 묶음: 93 PASS, 7 FAIL, 1 SKIP, 465 subtests PASS
  - 5개 실패는 기존 `nurse` exact route가 얀데레 양성·음성 케이스에 `clinical_nursing_duty_system`을 추가 활성화하는 충돌이다.
  - 1개 얀데레 합성 실패는 같은 추가 프로필의 하위 결과다.
  - 나머지 1개는 기존 시각 검색 픽스처의 baseline prompt가 현재 최소 48단어 계약보다 짧아서 발생한다.
  - 깨끗한 기준 커밋 `290d4271...`에서 5개 라우팅 충돌과 48단어 오류를 별도 재현했다. 이번 사진 시대 파일과 무관하므로 범위를 넓혀 수정하지 않았다.

## 독립 실험 설계

- 서로 다른 세 범주에서 프로필을 난수 선택: `random_selection.json`
- 공통 소스 스냅샷: `source_snapshot.json`
- 각 서브에이전트는 자신의 폴더만 사용했고 다른 arm의 프롬프트·팩·이미지·판정을 읽지 않음
- 각 arm은 core v3를 먼저 고정한 뒤 post-core 시각 intent를 만들고 v6 후보팩을 정확히 하나 배출
- 첨부 이미지는 보이는 성인 외형 참조만 사용
- built-in image generation 호출은 arm당 정확히 1회, 총 3회
- 이미지 재시도 0회, fallback 0회
- 프롬프트/런타임 감사, 픽셀 판정, 사용자 판단을 분리

Arm 1은 첫 candidate-pack 실행 전 입력 검증에서 시각 intent의 정확 앵커가 부족해 거부됐다. core·seed는 바꾸지 않고 binding 문구만 교정한 뒤 첫 팩을 배출했다. 이는 이미지 재시도나 두 번째 팩 배출은 아니지만 실행 무결성 기록에 보존했다.

## 실험 결과

| Arm | 랜덤 복합 컨셉 | 프로필 | 프롬프트/런타임 | 픽셀 | 후보 원소 노출 |
|---|---|---|---|---:|---|
| 1 | 정전 중 이동식 극장 소품 보관소에서 보존용 경사광으로 발굴지 알부민 마운트 검사 | `albumen_card_mount_print_material_relation` | PASS / PASS | 3/5 FAIL | 0/3 FAIL |
| 2 | 앨범 페이지의 1990년대 후반 생일 파티 정리 중 케이크 전달 미니랩 스냅 | `late_century_minilab_flash_print_relation` | PASS / PASS | 5/5 PASS | 0/3 FAIL |
| 3 | 침수된 지하 연산 보관소에서 기후모델 테이프를 회수하는 초광각 근원근 장면 | `smartphone_ultrawide_near_far_perspective_relation` | PASS / PASS | 5/5 PASS | 0/2 FAIL |

Arm 1 실패 근거:

1. 대각선 경사광이 사진층과 크림색 마운트를 함께 지나므로 광택이 사진층에만 귀속됐다고 볼 수 없다.
2. 네이티브 이미지와 확대 크롭 모두 사진층 전체의 가는 크랙 네트워크나 미세 종이 섬유를 별도 단서로 보여주지 못한다.

루트 검토는 15개 게이트 모두에서 각 독립 서브에이전트와 일치했다. 상세 판정은 `coordinator/coordinator_pixel_review.json`, 실행 독립성·해시는 `coordinator/execution_integrity.json`에 있다.

## 이미지 및 arm 기록

- Arm 1: `arm-1/final.png`, `arm-1/arm_result.json`, `arm-1/pixel_review.json`
- Arm 2: `arm-2/final.png`, `arm-2/arm_result.json`, `arm-2/pixel_review.json`
- Arm 3: `arm-3/final.png`, `arm-3/arm_result.json`, `arm-3/pixel_review.json`

각 폴더에는 고정 요청, authorial core, 시각 intent, v6 후보팩, 합성 프롬프트, 런타임 요청, 감사 결과, 1행 생성 원장, 매니페스트와 이미지 SHA-256이 함께 보존돼 있다.

## 증거 경계와 판정

- 패키지: PASS — 데이터, 로더, 색인, 라우팅/부정 회귀가 유효함
- 프롬프트: PASS — 세 팩 모두 지정 하드 프로필 1개와 5개 게이트를 포함하고 합성·런타임 감사 통과
- 후보 공개 표면: FAIL — 새로 추가한 요청 후보 원소 8개가 세 랜덤 팩에서 모두 미노출
- 렌더: FAIL — 2/3 프로필, 13/15 게이트만 통과
- 사용자 판단: UNSCORED — 아직 요청 사용자 평가가 없음
- 최종 결정: `revise`

다음 수정 대상은 두 가지로 한정한다: 후보 원소의 공개 v6 검색 노출을 강화하고, 알부민 프로필에서 사진층 한정 광택과 전면 미세 크랙을 더 강하게 공존시키는 합성 표현을 개선한다. 이번 세 이미지를 재생성해 성공처럼 바꾸지 않았으며 실패 이미지를 그대로 보존했다.
