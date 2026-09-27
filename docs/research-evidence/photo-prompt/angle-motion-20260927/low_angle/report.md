# 로우 앵글 독립 테스트

로우 앵글 고정 4개 픽셀 기준의 all-of 결과는 **PASS**입니다. 전체 복합 장면과 embodiment 5개 실효 hard gate도 PASS이며, **사용자 미적 판정은 pending**입니다. native imagegen 1회 결과를 수정하거나 재생성하지 않았습니다.

- seed: `14321191467143688212`
- pack: `482fc3c82b9776b0`; prompt: `3fe38fdf5b833854`; runtime prompt: `1d480ad445215d74`; run: `6cb6497278c7f7b2`
- 이미지: [generated.png](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/generated.png) — 1024×1536 PNG, SHA-256 `97f8ec5f8c17f908c2ebb083084ee8f3d83c499f01f0ae5fcffee6a114a8ac84`
- native 반환 원본: `/Users/chasoik/.codex/generated_images/01a0e22c-34a0-76e3-8dd9-c792e697446c/exec-ce58a19b-632a-4f4a-aef8-bc97bdf2cf01.png`
- 참조: 실제 `referenced_image_paths`에 전달, SHA-256 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`

독립 랜덤 추첨은 유리 온실, 작업면 닦기, weathered galvanized metal, cool overcast side daylight를 골랐습니다. 낮은 시점에서 접촉을 볼 수 있도록 닦는 면을 작업대의 수직 앞면으로 정리했습니다. 오른손 천 접촉, 왼손 여분 타월, 양발 돌바닥 지지와 직립 몸통을 core 전에 검토했습니다. 9개 neutral category는 draft 전에 선택했고, precore validator는 valid=true 및 warnings=[]였습니다. 사용자 정의는 없으며 로우 앵글은 일반 지식으로 해석했습니다. 부수적인 랜덤 장면은 사용자 정의·semantic assertion으로 넣지 않았습니다.

| 구분 | 판정 | 확인 범위 |
|---|---|---|
| focal coverage | covered | 카메라 required typed assertion의 고정 문구 4개 |
| composition 감사 | PASS | 고정 core·anchor·후보 선택·최종 literal evidence |
| exact runtime 감사 | PASS | 실제 prompt/negative·intent/embodiment binding·참조 파일 bytes |
| 저장 | success | native 반환 경로에서 원본 byte-copy, SHA 일치 |
| 키워드 픽셀 | PASS | 고정 카메라 4 components, 원본 및 341×512 축소 |
| 전체 장면 픽셀 | PASS | 고정 랜덤 장면 8 components |
| embodiment 감사 | technical_qualified=true | 현재 이미지에 대한 5개 검토 기록, schema 및 gate 누락 없음 |
| 사용자 미적 판정 | pending | 직접 사용자 결정이 아직 없음 |

카메라 픽셀 검토에서는 큰 전경 부츠와 위로 후퇴하는 몸, 턱 아래의 좁은 면과 작업대 밑면, 머리 위 유리 지붕과 철제 리브, 위쪽으로 후퇴하는 복수 기둥을 확인했습니다. 기울어진 프레임이나 넓은 렌즈 효과만으로 통과시키지 않았습니다. 원본 검토는 양손의 각 역할과 천·금속 경계, 여분 타월, 양발 접촉 그림자를 확인했고 축소 검토도 지지와 낮은 투영을 유지했습니다. 금속 앞면의 젖은 반사와 수직 수분 줄무늬는 고정 장면의 moisture cue로 판정했습니다. 실제 카메라 높이와 초점거리 수치를 이미지에서 증명하지 않습니다.

| 채택 후보 | 선택 이유 | 픽셀 근거 |
|---|---|---|
| `slot:subject_framing:full_body_framing` | 바닥 지지와 몸의 원근, 지붕을 같은 프레임에서 읽기 | 머리·두 부츠·지붕이 모두 포함됨 |
| `slot:lighting:rb_window_room_gradient_candidate` | 기존 흐린 측광을 얼굴·천·금속·뒤 구조에 연결 | 앞 소매와 금속 테두리보다 뒤 리브가 어둡게 읽힘 |
| `slot:composition:third_grid_off_center_subject` | 인물과 작업대의 깊이 관계를 한쪽 배치와 대각선으로 구체화 | 왼쪽 인물과 오른쪽 대각 작업대, 접촉 손이 연결됨 |

사실적 피부·신체 실루엣, 인격, 동행자, 다른 소품 동작, 앉은 테이블 구도 등 요청 의미를 바꾸는 optional clarification은 거절했습니다. 카메라가 닫힌 dimension이므로 별도 eye-focus/hero-camera 후보를 채택하지 않았고, 지지 자세를 바꾸는 contrapposto도 거절했습니다. 선택된 visual-concept는 없으며 gate를 추가로 활성화하지 않았습니다.

composition 감사의 5개 경고는 후보 탐색에서 uncovered였던 필수 anchor가 자유 서술로 그대로 보존되었다는 정보입니다. blocking failure는 없습니다. pixel-review 감사의 exit code 1은 `visual_technical_qualified_user_judgment_pending`을 유지하는 계약상 종료이며 기술 gate 실패가 아닙니다. 감사 자체는 픽셀을 자동 추론하거나 사용자 취향을 대신 판정하지 않습니다.

핵심 실패는 기록되지 않았습니다. 동작은 단일 사진의 접촉과 상태로 확인했고 시간에 걸친 닦기 운동 자체는 증명하지 않습니다. 참조 비교는 보이는 얼굴·머리 외형에 한하며 실제 정체성·개인 나이·직업·몸 형태를 추론하지 않습니다.

[고정 core](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/authorial_core.json), [core freeze](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/core_freeze.json), [기준](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/test_case.json), [키워드 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/keyword_pixel_results.json), [전체 장면](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/scene_pixel_review.json), [pixel review 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/pixel_review_audit.json), [최종 영문 prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/final_prompt_en.txt), [원 요청](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/source_request.txt), [후보 노출·결정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/candidate_exposure.json), [ledger 1행](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/image_runs.ndjson), [manifest v2](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/run_manifest.json), [summary](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/arm_summary.json)에 근거를 보존했습니다. 최초 freeze 파일 해시를 다시 읽어 모두 불변임을 확인했습니다. 다른 arm·이전 실험·메모리 입력은 사용하지 않았습니다. 현재 skill source snapshot identity는 `sha256:f4b8ef255c401742b987cf18ca0446d3a5cd647f36b578f79e4a9e1046c2a172`입니다.

Source bytes 298개 파일을 [source_snapshot.tar.gz](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/source_snapshot.tar.gz)로 보존했습니다. archive SHA-256은 `e86cb0b64f7350a7ee3928af27303de7fe0c88c0328687014e5ec04783fb5b2d`입니다.
