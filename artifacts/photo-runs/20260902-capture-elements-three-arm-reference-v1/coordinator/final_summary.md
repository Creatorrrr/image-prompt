# 촬영 요소 시각 의미 3-arm 렌더 검증

## 데이터 적용

- 런타임 시각 의미 레지스트리에 촬영·광학·조명·톤 관계형 프로필 14개를 추가했다.
- 각 프로필은 5개 필수 성분 그룹, 5개 literal prompt evidence 필드, 5개 same-image hard pixel gate, 인접 대체 실패 경계를 가진다.
- 좁은 exact term만 hard obligation을 만들고 BM25F·embedding은 선택 전 optional candidate로만 남는다.
- 현재 공유 작업공간 전체는 동시 진행된 별도 조명 변경을 포함해 300 profiles, 1,568 exact terms, 7,974 semantic entries이며 dictionary, visual index, semantic index 검사가 모두 통과한다. 이 총계 전체를 이 작업의 기여로 주장하지 않는다.

## 실험 규약

- SHA-256 seed `12979636043140343144`로 motion, portrait-light, optics/tone 층에서 하나씩 선택했다.
- 각 팔은 profile assignment를 읽기 전에 서로 다른 복잡한 장면과 authorial core를 고정했다.
- 첨부 JPEG는 보이는 성인 얼굴 구조, 눈 형태·간격, 얼굴 길이, 하관·턱 폭, 헤어라인, 긴 어두운 웨이브 헤어에만 사용했다.
- 각 포함 팔은 built-in image generation 1회, retry 0, fallback 0, sibling input 0이다.
- package, prompt, runtime, rendered pixels, requesting-user judgment는 서로 대체할 수 없는 별도 증거 층이다.

## 결과

| 팔 | 무작위 복잡 장면 | 프로필 | prompt/runtime | 픽셀 게이트 | 기술 판정 |
|---|---|---|---|---:|---|
| arm-01r | 원형 지하 기록보관소의 이동 트롤리와 황동 리본 분류 장치 | `panning_subject_tracking_motion_relation` | PASS / PASS | 3/5 | FAIL |
| arm-02 | 폭우 속 고가 교통 분기점의 빗물 수문 핸드휠 | `rembrandt_face_light_pattern` | PASS / PASS | 0/5 | FAIL |
| arm-03 | 폭풍 해안의 황동 선박 종·청색 유리 부표 인양 | `highlight_rolloff_tone_response` | PASS / PASS | 5/5 | PASS |

집계는 arm 1/3 PASS, hard gates 8/15 PASS다. `partial_is_fail`이므로 전체 render-fidelity 평가는 FAIL이며 재검증 전 promotion하지 않는다.

### arm-01r — panning

- PASS: 추적된 얼굴·몸통·장치 핵심이 읽힌다.
- PASS: 배경 기록 선반과 조명이 주로 평행한 횡방향 streak를 만든다.
- FAIL: 리본·기어·바퀴·머리카락에서 독립적으로 읽히는 국소·회전 모션 블러가 없다.
- FAIL: 보조 움직임이 없어서 배경과 같은 단일 이동 벡터를 두 번째 단서로 확인할 수 없다.
- PASS: 전역 카메라 흔들림, 방사형 줌, 장식 speed line 대체는 아니다.

Render: `arm-01r/generated_images/quiet-archival-mechanism/arm-01r.png`  
SHA-256: `91ebf30df80f0a5fda36bd97afe56c2e2c10e697ab171320578fbde382b0863e`

### arm-02 — Rembrandt face light

- 얼굴은 거의 정면의 평평한 beauty illumination으로 읽힌다.
- 높은 비축 key, 연결된 nose-cheek shadow, 반대쪽 볼의 제한된 inverted triangle, 모델링된 shadow-side eye, substitute rejection이 모두 실패했다.

Render: `arm-02/render.png`  
SHA-256: `94bf3357871ff613283b6b9056868bdfe81c7de830b1cc92ee0408ca4359c0b0`

### arm-03 — highlight rolloff

- 근백색 anchor, 여러 밝기 단계의 shoulder, 작은 clip core, 주변 질감·색·중간톤 생존, flat/glow/HDR 대체 거부가 모두 통과했다.
- exact-white는 210 / 1,572,351 pixels (`0.0134%`)이며 최대 4-connected exact-white component는 14 pixels다.

Render: `arm-03/render.png`  
SHA-256: `069d9475763b7b2f1d3bfab0966928e13cb464b3abd884c6a034b77aafea437c`

## 무결성 경계

- 최초 arm-01은 이미지 호출 전에 broad search로 sibling snippet을 노출해 실격했고 결과 집합에서 제외했다. 깨끗한 arm-01r로 교체했다.
- arm-02는 sibling output을 읽지 않았고 concept도 pre-assignment에 고정했지만, schema 진단 중 shared implementation을 읽어 stricter protocol deviation으로 기록한다.
- arm-02와 arm-03의 post-assignment 변경은 허용 schema label mapping뿐이며 원래 장면·행동·evidence 문구와 최초·최종 hash를 모두 보존한다.
- 세 포함 팔 모두 manifest의 `cross_arm_inputs_used`는 false다. 이 사실은 프로토콜 위반 부재나 픽셀 성공과 같은 뜻이 아니다.

## 결론과 다음 최소 수정점

- 14개 프로필의 데이터·후보팩·라우팅 구조는 구현 및 검증됐다.
- 실제 픽셀 근거가 있는 것은 선택된 3개 프로필뿐이다. 나머지 11개는 structural/prompt-qualified이지 pixel-qualified가 아니다.
- 다음 렌더 수정은 panning에서 ribbon tabs·wheel·loose hair의 국소 motion을 같은 횡벡터로 강화하고, Rembrandt에서 fill을 낮춰 joined nose-cheek shadow와 bounded far-cheek triangle을 먼저 확보하는 두 좁은 축으로 제한한다.
- 요청 사용자의 미적 수락과 참조 외형 만족도는 아직 `UNSCORED / not_yet_received`다.

## 증거 파일

- `tests/fixtures/photo_prompt/capture_elements_three_arm_pixel_test_cases_v1.jsonl`
- `coordinator/execution_integrity.json`
- `arm-01r/arm_report.md`
- `arm-02/arm_report.md`
- `arm-03/arm_report.md`
