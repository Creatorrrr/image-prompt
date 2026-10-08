직접 셀카 arm B는 **기술 감사 PASS, 공식 픽셀 조건 9/9 PASS, 새 데이터의 전체 픽셀 대응 PARTIAL, 사용자 수용 PENDING**이다. 최초 native 이미지 1회가 정상 반환되었고 추가 생성이나 API 전환은 하지 않았다. 새 후보의 촬영 팔·얼굴 지향은 보이지만 실제 기기와 렌즈 높이는 프레임 밖에 있어 확인할 수 없다.

![회전목마 수선 중 직접 셀카](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/generated-native-attempt-1.png)

독립 seed `35437455`로 일반지식에서 만든 네 대안 중 `carousel_repair`를 추첨했다. 푸른 저녁의 회전목마 수선 공간에서 부러진 붉은 목재를 가까이 보여주고, 뒤의 붉은 갈기와 금속 이음새·목재 가루·사포·전구를 연결했다. 작은 미소의 이유가 수선 상황에서 읽히도록 의미를 먼저 정했다. 직접 손에 든 초광각 셀카는 에이전트의 촬영 선택이다. 사용자가 카메라 방식·높이를 잠근 것으로 취급하지 않았다. [추첨 기록](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/random-concept-selection.json)

참조 이미지를 직접 보고 얼굴과 짧은 어두운 단발·성긴 앞머리만 활용했다. 실제 신원·나이·이력을 추정하지 않았다. 원래 JPEG path를 native `referenced_image_paths`에 넣었고 SHA-256 `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`가 요청·런타임·ledger에서 같다. 저장된 컨트롤 sensual=1, fetish=0, surreal=0, creativity=1 및 실제 authoring brief를 적용했다.

후보 접근 전에 neutral feature 9개, baseline, camera assertion, 두 active spans(`complex_topic`, `image_reference`), core/selection/embodiment review를 동결했다. camera assertion의 capture owner는 `unprescribed`, 방향·높이는 `open`이었다. V2에도 원문과 네 계약 hash가 같다. 초기 손 좌우 표기는 이후 open pose에서 actor-right 촬영/actor-left 제시로 정돈했고, 새 후보의 근사 eye-line 높이는 open camera에서 채택했다. 핵심 사건·참조·의미는 바뀌지 않았다. [동결 재사용 증거](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/phase1-v2-replay.json)

| 동결 계약 | SHA-256 |
|---|---|
| core | `720d758736dd21bcb79a9ee6e9f117b73305a67c8f3cdf31f02b6249e39150f5` |
| intent lock | `5cedcbeeb795ad74920c19bb71944c92aeb27e8e73597c9c85d86f1a3594d888` |
| envelope | `ab9cd6d4d88d7e20d68b04ed2d0d830f4d464965600b54ca9821006b24c78ac9` |
| controls | `9024a769d5e0bb9f7bec6aed5da0deea33e0796bf9542c90b16d9ffe4803456d` |

원래 run의 pack `91f07c256e8c73d3`에는 capture_context 슬롯이 없었고 새 조명 후보 `sf_173_base`만 노출됐다. 보류된 reserved/started payload는 호출하지 않았으며 원래 run의 실제 생성은 0회다. 원래 run·pack·감사를 보존했다. V2의 capture_mode 경로에서 같은 동결 core로 재조회한 결과는 다음과 같다. [원래 coverage gap](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/data-contribution.json), [V2 기여 기록](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/data-contribution-v2.json)

| 층위 | 실제 결과 |
|---|---|
| runtime generation | `8d793f025f759eb7f782d0a194f9dd7f0781370aaff2bbea331146e940c3ab2f` |
| source fingerprint | `fe7ac255143e52fe70b9c64cc7bd02961d176b0258f35a1769aeff6b562a825c` |
| V2 pack | `b889a5e9d99b64f2` / v6 |
| 새 후보 노출 | `slot:capture_mode:sf_071_base`, `slot:lighting:sf_173_base` |
| 새 후보 채택 | `slot:capture_mode:sf_071_base` |
| 새 profile 노출·채택 | 없음 |
| 기존 데이터 채택 | `visual-concept:pc_pc16_owner_relation`의 전체 4개 구성 요소 |

새 `sf_071` literal은 “Her extended right capture arm brings the phone lens to approximately the height of her eyes, and her face and gaze turn toward that self-held lens”이다. 근사 눈높이, 촬영 팔의 주체 소유, 얼굴의 렌즈 지향을 명시한다. 기존 `pc_pc16`은 제시 손의 소유·목재 접촉·가까운 깊이·표정 가림 없음에 기여한다. 회전목마·수선 사건·재료 연결·초광각 선택은 후보 접근 전의 기본 저작에서 왔다. 기존 `pc_*`를 이번 새 데이터로 계산하지 않았다.

[최종 프롬프트](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/final-prompt-v2.txt)는 composed prompt 3234바이트에 저장용 마지막 newline 1바이트를 가진다. 실제 도구에 보낸 원문은 [exact runtime prompt](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/exact-runtime-prompt-v2.txt) 3793바이트이며 SHA-256 `a9dca317de0006b598dcee6b1a8391db7fe38ac274473fcf7c38f4b1b49cd033`이다. pack negative가 정확히 포함되었고 [런타임 요청](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/exact-runtime-request-v2.json)·[불변 runtime receipt](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/exact-runtime-receipt-v2.json)·native plan의 바인딩을 검사했다. 구성 감사는 PASS이고 candidate coverage 밖의 4개 사용자 의미를 자유 서술/assertion으로 보존했다는 quality warnings는 유지했다.

실제 native 호출은 `2026-10-08T13:23:25.869Z`–`2026-10-08T13:24:12.866Z`의 1회다. 이미지 원본은 **1237×1272 PNG**, SHA-256 `d04c54288782034f2402d025c4b4b614c4a23876977d3be3ce14952603ba6b26`이며 반환 원본과 arm 복사본이 byte-identical이다. 실제 모델명은 도구 결과에 없어 `null`로 기록했다. [원본 이미지](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/generated-native-attempt-1.png), [반환·보존 기록](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/native-result-metadata.json), [단일 ledger row](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/image_runs.ndjson), [독립 manifest](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/run_manifest.json)

아래는 생성 전 이미 고정된 4개 기존 visual gates와 5개 embodiment gates만 판정한 결과다. 전체 native pixels와 311×320 thumbnail을 직접 읽었다. 좌표는 원본의 좌상단 원점 `(x0,y0,x1,y1)` 근사 영역이며 관절 각도·물리 거리 측정값은 아니다. 상세 원본 증거와 각 한계는 [픽셀 관찰 기록](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/pixel-observations-v2.json)에 있다.

| 공식 gate | 판정 | 확인 scale | 원본 위치 | 실제 픽셀 증거 |
|---|---|---|---|---|
| `vo_pc_pc16_owner_relation_1` (주체 손의 전방 제시) | PASS | native + thumbnail | display_arm_hand [671, 814, 1218, 1272]; capture_arm [0, 548, 497, 1272] | 우측 제시 손·소매의 연결과 좌측 촬영 팔이 구분된다. |
| `vo_pc_pc16_owner_relation_2` (손과 물체 접촉) | PASS | native | finger_wood_contact [863, 849, 1100, 1073]; wood_fragment [813, 669, 995, 986] | 붉은 목재와 엄지·반대쪽 굽힌 손가락의 접촉 경계가 보인다. |
| `vo_pc_pc16_owner_relation_3` (가까운 손·물체의 깊이) | PASS | native + thumbnail | display_arm_hand [671, 814, 1218, 1272]; face_and_expression [355, 250, 800, 648]; horse_repair_context [800, 45, 1237, 856] | 전경의 큰 손·목재, 얼굴, 뒤 작업대·말의 층이 나뉜다. |
| `vo_pc_pc16_owner_relation_4` (표정 영역 가림 없음) | PASS | native + thumbnail | wood_fragment [813, 669, 995, 986]; face_and_expression [355, 250, 800, 648] | 목재와 그립은 얼굴 우하단에 있고 두 눈과 작은 미소가 읽힌다. |
| `embodiment_body_ownership` (신체 소유) | PASS | native | capture_arm [0, 548, 497, 1272]; display_arm_hand [671, 814, 1218, 1272]; standing_torso_waist [236, 557, 880, 1272] | 각 팔은 같은 인물의 서로 다른 어깨·소매에서 이어진다. |
| `embodiment_joint_chain_and_reach` (관절 연쇄·도달) | PASS | native | capture_arm [0, 548, 497, 1272]; display_arm_hand [671, 814, 1218, 1272]; standing_torso_waist [236, 557, 880, 1272] | 한 팔의 전방 확장과 반대 팔의 굽힌 제시 자세가 공존한다. |
| `embodiment_support_and_balance` (지지·균형) | PASS | native | standing_torso_waist [236, 557, 880, 1272]; horse_repair_context [800, 45, 1237, 856] | 허리까지의 직립 자세가 자연스럽고 큰 목마는 작업대 쪽에 놓인다. |
| `embodiment_contact_and_space` (접촉·공간) | PASS | native | finger_wood_contact [863, 849, 1100, 1073]; wood_fragment [813, 669, 995, 986]; face_and_expression [355, 250, 800, 648] | 손가락이 목재의 칠한 몸통을 잡고 부러진 끝·표정은 분리된다. |
| `embodiment_visibility_and_projection` (가시성·투영) | PASS | native | capture_arm [0, 548, 497, 1272]; display_arm_hand [671, 814, 1218, 1272]; face_and_expression [355, 250, 800, 648]; horse_repair_context [800, 45, 1237, 856] | 촬영 팔, 그립, 얼굴, 뒤 수선 공간의 전후 관계가 함께 보인다. |

발·촬영 손·기기 본체는 crop 밖이다. 보이는 직립 몸통과 팔 연쇄는 모순 없이 읽히며, 공식 게이트의 가시성·소유·도달·그립은 관찰 가능하다. 이 판정으로 실제 발바닥 접촉이나 프레임 밖의 기기 접촉을 확인했다고 주장하지 않는다. [공식 visual review](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/visual-review-v2.json)와 [managed moe/visual review audit](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/run_v2/revisions/3c73938f05684afb9102dc5335a84ab0/review_audit.json)는 schema failures·failed gates가 각각 빈 배열이고 `visual_technical_qualified_user_judgment_pending`이다. 감사 도구는 기록의 유효성을 검사하며 픽셀 판정은 이 arm의 직접 관찰에 따른다.

새 데이터에 대한 독립 주제 관찰은 공식 9개 gate와 별도다. 새 hard gate를 추가하지 않았다.

| 독립 주제 관찰 | 상태 | 근거·한계 |
|---|---|---|
| `sf_071` source/literal/런타임 연결 | PASS | 실제 노출→채택→exact runtime 문구가 연결됨 |
| 촬영 팔의 전방 투영 | PASS | native `[0,548,497,1272]`의 팔이 화면 밖 촬영 위치로 이어짐 |
| 얼굴·시선의 렌즈 방향 | PASS | native 얼굴 `[355,250,800,648]`, 눈 `[465,340,738,416]`이 관찰자 방향으로 향함 |
| 근사 eye-line의 시각 일치성 | PARTIAL | 대화하는 듯한 높이는 자연스럽지만 active lens 자체는 보이지 않음 |
| 실제 렌즈 높이·촬영 손/기기 접촉 | UNOBSERVABLE | 카메라와 촬영 손이 프레임 밖 |
| 초광각 의도의 투영 | 부분 지지 | 전경 손·팔 확대와 후경 작업 공간은 보임; 실제 렌즈 종류는 UNOBSERVABLE |
| `0.5` 기기 배율 | 미선택 / UNOBSERVABLE | 입력으로 채택하지 않았고 raster에서 측정값으로 주장하지 않음 |
| 새 데이터 전체 픽셀 대응 | PARTIAL | 보이는 팔·얼굴 방향과 물리 카메라 사실의 증명 범위가 다름 |

독립 artist notes에서는 얼굴→큰 전경 그립→목마의 계층과 붉은 칠의 재료 연결이 장점이다. 이미지의 작은 미소와 수선 공간은 휴식 중 셀카로 읽힌다. 목마가 선택한 actor-right 대신 actor-left 뒤에 놓였고 이음새는 임시 clamp보다 금속 bridge plate/brace처럼 보인다. 이것은 open 저작 세부의 작은 차이이며 공식 gate 실패가 아니다. 실제 수선 전후 역사와 피로감은 픽셀만으로 확정되지 않는다. [이미지 기반 artist notes](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/artist-notes-v2.json)

최초 visual-review wire의 사용자 판단 null은 enum 검증에서 거절되어 `pending`/`not_applicable`로 바로잡았다. 이미지·증거·9개 판정은 바꾸지 않았다. 최초 generation에는 render_repair contract가 없어 generic repair review는 **NOT_APPLICABLE**이다. 해당 auditor의 탐색 호출은 lineage target 부족으로 거절됐으며 그 실패 기록을 PASS로 바꾸지 않았다. 실제 image-render-request 감사와 적용 가능한 moe/visual/embodiment 감사는 PASS다. [wire 수정 기록](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/review-wire-correction.json), [generic 감사 적용 범위](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/generic-repair-review-applicability.json)

마지막 18개 파일·hash·gate-set·단일 호출·source 바인딩 검사는 PASS다. display prompt의 저장 newline에 대한 초기 검증 가정만 수정했고 런타임 문구를 바꾸지 않았다. 사용자 직접 판단은 아직 없으며 `representative_eligible=false`로 유지한다. 기술/픽셀/사용자 수용을 구분한 기계 판독 결과는 [qualification.json](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/qualification.json), 최종 일관성 증거는 [delivery verification](/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt/docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/arms/ultrawide/final-delivery-verification.json)에 있다.
