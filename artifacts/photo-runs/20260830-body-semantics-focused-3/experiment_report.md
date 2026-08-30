# 여성 신체 시각 의미 3키워드 집중 렌더 테스트

## 결론

테스트 케이스와 프롬프트 경로는 정상 작동했지만, 렌더 충실도는 **3건 중 1건만 통과**했다. 따라서 세 키워드가 이미지 생성에서 충분히 검증됐다고 볼 수 없으며 결정은 `revise`다.

| 키워드 | 랜덤 복합 콘셉트 | 최종 게이트 | 기술 판정 |
|---|---|---:|---|
| `contrapposto_weight_shift` | 야간 Ro-Ro 페리 차량갑판 loadmaster 점검 | 3/4 | FAIL — 골반·어깨 counter-tilt 불명확 |
| `body_bounded_negative_space` | 폐관측소의 자오선 분쟁 조사 | 1/4 | FAIL — 실제 팔·허리 대신 코트 절개가 여백을 소유 |
| `upper_lip_philtral_contour` | 달 종자 보관소의 발아 스캔 | 4/4 | PASS |

모든 arm은 서로 다른 새 에이전트 컨텍스트와 파일 디렉터리를 사용했다. 각 에이전트는 요청 봉투, 배정 키워드, 시드, 일반지식만으로 8개 후보를 만들고 난수 선택한 뒤 authorial core를 동결했다. 저장소 프로필과 후보팩은 그 이후에만 읽었다.

## 추가된 회귀 계약

`tests/fixtures/photo_prompt/body_semantics_pixel_test_cases_v1.jsonl`에 전신·영역·국소 스케일을 각각 대표하는 세 행을 추가했다. 각 행은 정확한 hard-profile 활성어, 레지스트리 render gate 전체, thumbnail/native 검수 스케일, false substitute, 얼굴 참조의 appearance-only 역할, 그리고 `한 이미지에서 모든 게이트 통과` 규칙을 가진다.

`tests/test_photo_body_aesthetic_semantics.py`는 다음을 검증한다.

- 정확히 세 프로필만 선택됐는지
- 활성 문구가 하나의 정확한 프로필로만 route되는지
- fixture의 gate/reject set이 레지스트리와 정확히 같은지
- 단어 존재나 부분 통과가 이미지 합격으로 바뀌지 않는지
- 전신·영역·국소 스케일과 중립적 비추론 경계가 모두 있는지

관련 회귀군 50개가 통과했고, 최종 상태에서 집중 테스트 8개와 시각 프로필 검색 테스트 12개를 각각 다시 실행해 통과했다.

## 독립 렌더 결과

### 1. Contrapposto — FAIL

- Pack `01e98ff747195536`; 최종 이미지 `arm-1-contrapposto/attempt-2.png`
- 지지 다리, 자유 다리, 전신 crop은 통과했다.
- 조끼·머리카락·클립보드·커버올 때문에 골반선과 어깨선이 thumbnail에서 반대 방향으로 기울었다고 단정할 수 없다.
- 동일 실패만 겨냥한 1회 수리 후에도 `vo_contrapposto_counter_tilt`가 실패했다.

### 2. Arm–waist body-bounded negative space — FAIL

- Pack `42ac3b8c1c72c009`; 최종 이미지 `arm-2-arm-waist-negative-space/attempt-2.png`
- 큰 삼각형 자체는 thumbnail에서 읽혔다.
- 그러나 안쪽 경계는 실제 허리 윤곽이 아니라 코트 flap/절개이며, plumb line도 배경 패치를 가로질렀다.
- 이는 fixture가 명시적으로 거부한 `garment_cutout_or_shadow` 대체물이다. 1회 수리 후 1/4 게이트만 통과했다.

### 3. Upper-lip philtral contour — PASS

- Pack `bc2da31d2a6a73ac`; 최종 이미지 `arm-3-philtral-contour/attempt-1.png`
- 두 인중 기둥, 중앙 홈, 윗입술의 두 봉우리와 중앙 dip, 코·입 주변의 일관된 표면 구조가 한 이미지에 공존했다.
- `256×320` 전체 thumbnail에서도 paired upper-lip arc가 남았다.
- 1차 이미지에서 4/4를 통과해 수리 렌더를 하지 않았다.

## 증거 층과 한계

- Package: PASS — JSONL 파싱, 50개 관련 회귀, 최종 8개 집중 회귀와 12개 시각 프로필 검색 회귀.
- Prompt: PASS — 세 v6 pack 모두 정확한 hard profile을 포함했고 composed/runtime audit이 통과했다.
- Generation: PASS — 총 5개의 native 이미지가 저장됐고 각 시도와 `retry_of`가 공용 ledger에 기록됐다.
- Pixels: FAIL aggregate — 1/3만 모든 게이트 통과.
- User: PENDING — 얼굴 외형 유사성, 심미성, 선호도는 요청자 판단 전까지 미확정이다.

첨부 이미지는 모든 arm에서 `facial_appearance_only`로 사용했다. 신원, 인종·민족, 건강, 신체 가치 또는 생체 동일성 주장은 하지 않는다.
