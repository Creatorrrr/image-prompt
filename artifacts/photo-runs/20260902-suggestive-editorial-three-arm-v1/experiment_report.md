# 암시적 성인 에디토리얼 시각 의미 3-arm 검증 보고서

## 결론

시각 의미와 후보팩 데이터 구현은 완료했고, 새로 만든 좁은 시각 계약을 서로 다른 무작위 복합 장면 세 개에서 독립적으로 시험했다. 각 arm은 첨부 이미지를 `appearance_reference`로만 사용하고, 프롬프트를 고정한 뒤 built-in image generation을 정확히 한 번 호출했다.

- Arm 01: `10/10 PASS` — 자기주도 랩드레스 여밈, 단일 가림-드러남 경계, 확산창광, 침실 맥락, 직물 물리
- Arm 02: `5/5 PASS` — 완전한 성인 전신, 연속 불투명 S자 가림 경로, 양쪽 윤곽 연속성, 방향성 형태광과 네거티브 스페이스
- Arm 03: `0/10 evaluated` — 프롬프트·런타임 감사 PASS 후 유일한 생성 호출이 입력 moderation에서 차단됨
- 전체: 요청 gate 25개 중 15개 평가, `15/15 PASS`, 10개 `UNSCORED`

따라서 두 성공 렌더는 해당 조건에서 기술적으로 자격을 얻었지만, 3-arm 전체 판정은 `incomplete_due_to_one_generation_safety_block`이다. `UNSCORED`는 품질 0점이나 픽셀 실패가 아니다. 사용자 미감 판단은 세 결과 모두 `pending`이다.

## 데이터 반영

### 시각 계약 4개

- `adult_everyday_controlled_reveal_moment`
- `strategic_coverage_figure_study`
- `underwear_as_outerwear_layer_system`
- `soft_window_private_room_adult_portrait`

각 계약은 명백한 성인 조건, 서로 다른 5개 구성요소 그룹, literal prompt evidence, 5개 thumbnail/native gate, 최소 5개 실패 대체물을 가진다. `은꼴사`, `대꼴사`, `야짤`, `세미 누드`, `임플라이드 누드`, `부두아르`처럼 넓거나 유통 맥락에 의존하는 표현은 단독 hard activation으로 만들지 않았다.

### 후보 원자와 프리셋

- 동작 5개
- 가림·프레이밍 5개
- 의복 디테일 6개
- 표면·재질 4개
- 프리셋 4개

총 20개 후보 원자와 4개 후보팩 프리셋을 사전에 추가했다. 집중 테스트는 모든 원자와 프리셋이 사전 및 semantic index에서 도달 가능하며, 좁은 exact 표현만 대응 프로필에 hard route되는지 검사한다. 독립 이미지 arm은 이 가운데 프로필의 관찰 가능한 관계를 대상으로 하며, 20개 후보 원자 각각의 픽셀 자격을 주장하지 않는다.

### 생성 인덱스

- visual profile index: 323 profiles / 1,667 exact terms / Gemini 768d
- semantic index: 8,021 entries / 16 shards / Gemini 768d
- dictionary version: `1.43`

## 독립성·계보

- 기준 revision: `401f450e4c0ec32ef79c502e3c6a6666c9a106c4`
- 참조 이미지 SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
- 각 arm: 별도 request envelope, authorial core, visual intent, v6 candidate pack, composed prompt, render request, ledger, manifest, review
- 이미지 호출: 총 3회, 성공 2회, safety block 1회
- 재시도 0회, fallback 0회, cross-arm input 0회

참조 이미지는 보이는 성인 얼굴 비율, 긴 짙은 웨이브 헤어, 보이는 자연스러운 피부 질감에만 사용했다. 정체성, 동일인, 생체정보, 보호 특성, 건강, 매력, 성격, 직업, 민족, 국적, 관계는 추론하거나 평가하지 않았다.

## 픽셀 재검토

### Arm 01 — 확산창광 랩드레스 여밈

- Seed: `13389124217090213127`
- 콘셉트: 커튼 확산광이 드는 사적 침실에서 성인 여성이 불투명 딥플럼 랩드레스를 스스로 여미는 미완 순간
- 결과: `10/10 PASS`

썸네일에서도 성인 피사체, 얼굴, 양손의 허리끈 동작, 몸통, 창·커튼·침대·거울·슬리퍼가 함께 읽힌다. 한 개의 짙은 랩 라펠 경계가 목선에서 허리까지 이어지고, 원본에서는 안팎 겹침, 접촉 그림자, 허리끈 장력과 중력 주름이 보인다. 왼쪽의 보이는 창과 반투명 커튼은 얼굴에서 방 안쪽으로 부드러운 방향성 광량 변화를 만든다.

![Arm 01](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-suggestive-editorial-three-arm-v1/arm-01-window-reveal/final.png)

### Arm 02 — 코발트 S자 전략적 가림 피겨 스터디

- Seed: `1949316982481159071`
- 콘셉트: 석회석 사이클로라마의 성인 전신과 연속된 불투명 코발트 S자 조형 스크린
- 결과: `5/5 PASS`

머리부터 두 부츠까지 한 프레임에 남고, 하나의 불투명 S자 형상이 상단에서 바닥까지 끊기지 않는다. 어깨·허리·엉덩이·다리 윤곽은 스크린 양쪽에서 자연스럽게 이어진다. 표면 질감, 바닥 접촉과 그림자 때문에 소프트웨어 검열 바로 읽히지 않으며, 창의 사선광과 팔·허리·다리 사이의 네거티브 스페이스가 입체 형태를 유지한다.

![Arm 02](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-suggestive-editorial-three-arm-v1/arm-02-figure-coverage/final.png)

### Arm 03 — 레이어드 패션 물리 거울 셀피

- Seed: `980534469`
- 콘셉트: 부티크 호텔 드레싱룸의 불투명 새틴 기반층, 별도 차콜 턱시도 외층, 교차 여밈과 물리 거울 셀피 토폴로지
- 결과: `10/10 UNSCORED`

후보팩, composed prompt, 직렬화된 render request 감사까지 통과했지만 단 한 번의 built-in 생성 호출이 입력 단계 `sexual` moderation으로 차단됐다. preview와 로컬 이미지가 없으므로 레이어 교차·여밈·거울 프레임·손-기기 접촉·반사 시선 가운데 어느 것도 픽셀로 판정하지 않았다. 독립성 규칙에 따라 재시도나 다른 공급자 fallback은 하지 않았다.

## 검증 경계

- 새 집중 테스트: 8개 PASS, skip 없음
- 사전 validator: PASS
- visual profile index current check: PASS
- semantic index: 현재 사전 해시와 일치하는 8,021 entries / 16 shards
- composed prompt audit: 3/3 PASS
- serialized render request audit: 3/3 PASS
- 픽셀: 성공 렌더 2개에서 `15/15 PASS`; 차단 렌더 1개의 10개 gate는 `UNSCORED`
- 사용자 미감: `pending`

긴 관련 회귀군 63개는 `failures=6, errors=1`을 보고했다. 6개 실패는 이번 diff가 건드리지 않은 HEAD의 `clinical_nursing_duty_system` 넓은 exact term `nurse`/`간호사`와 기존 얀데레 픽스처 기대값 사이의 충돌이다. 1개 오류는 역시 수정하지 않은 검색 테스트 helper가 현재 48단어 최소치보다 짧은 `baseline_prompt_en`을 만드는 문제다. 이 기준선 문제를 새 집중 테스트 PASS와 합쳐 전체 회귀 PASS로 주장하지 않는다. 같은 실행의 사전 validator, visual index current check, scene-expression 112/112와 `git diff --check`는 통과했다.

상세 연구는 `docs/analysis/2026-09-02-suggestive-editorial-visual-semantics.md`, 해시 고정 테스트 입력은 `tests/fixtures/photo_prompt/suggestive_editorial_three_arm_pixel_cases_v1.jsonl`, root의 기계 판정은 `coordination/root_pixel_review.json`에 있다.
