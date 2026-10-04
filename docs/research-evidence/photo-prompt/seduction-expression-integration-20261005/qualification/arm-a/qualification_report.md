독립 Arm A의 전체 장면 픽셀 판정은 **FAIL**입니다. 이미지 생성 자체는 `image_gen.imagegen`으로 1회 성공했으며 원본 1237×1272 PNG를 바이트 그대로 저장했습니다. 고정한 7개 관찰 게이트 중 PASS 3, FAIL 2, UNOBSERVABLE 2입니다. `partial_is_fail`을 적용했고 미관찰을 성공으로 바꾸지 않았습니다.

무작위로 고른 도시 공공 실내 장소는 공공 수영장 분실물 창구입니다. 새 성인 이용자가 책상 위 안내지의 왼쪽 화살표와 벽의 오른쪽 화살표를 비교하는 순간이며, 눈꺼풀·홍채·입술·양손의 자기 접촉 차이는 에이전트가 일반 지식으로 고른 독립 시험 형태입니다. 참조 사진은 보이는 얼굴·머리에만 사용했고 원본의 나이·정체성·성격·체형을 추정하지 않았습니다. 새 주체는 프롬프트에서 29세 성인으로 설계했습니다.

| 고정 게이트 | 원본 픽셀 결과 | 관찰 근거 |
|---|---|---|
| 실내 공공 수영장·분실물 창구·화살표 관계 | PASS | 창구, 키 태그/수영모 트레이, 안내지 왼쪽 화살표, 벽 오른쪽 화살표가 함께 보임 |
| 양눈 open + actor-left upper lid가 더 낮음 | FAIL | 양눈은 열렸으나 화면 오른쪽의 actor-left 눈이 더 열려 있으며 지정한 비대칭을 충족하지 않음 |
| actor-right / 화면 왼쪽 홍채 이동 | FAIL | 두 홍채가 화면 오른쪽, 즉 actor-left 쪽을 향함 |
| 좁은 입술 틈 + 치아 가장자리 + 좌 입꼬리 lift | UNOBSERVABLE | 틈과 얇은 치아 경계는 보이나 작은 입꼬리 차이를 고개 roll과 구분하기 어려움 |
| 우 index의 자기 오른쪽 볼 접촉·작은 변형 | PASS | 자기 팔에 연결된 손끝이 아래 볼의 피부와 만나 작은 접촉 주름/변위를 형성함 |
| 좌 index의 자기 관자놀이 4–6cm 비접촉 | UNOBSERVABLE | 공기 간격과 소유 관계는 보이나 단일 비보정 사진에서 정확한 cm 길이를 검증할 수 없음 |
| 첨부의 보이는 얼굴·머리 외형 참고 | PASS | 짧은 어두운 bob/fringe와 보이는 얼굴 형태가 참조와 닮음; 정체성 증명은 아님 |

통합 데이터의 존재와 실행 단계는 별도로 검사했습니다. `se_profile_upper_lid_dominant_half_lid`, `se_profile_two_hands_different_heights`, `se_profile_cheek_fingertip_light_touch`는 작성 데이터에 존재하지만 이번 팩에서 해당 시각 프로필의 노출·선택·하드 활성은 모두 0/3입니다. 일반 후보에서는 대응하는 세 항목 중 상안검 형태와 양손 높이 후보 2/3이 노출되고 선택됐습니다. 양손 높이 후보의 관계는 픽셀에서 PASS이며 상안검 후보 전체 형태는 UNOBSERVABLE/strict failure입니다. 볼 접촉은 독립 기본 프롬프트에서 이미 작성한 형태라, 노출되지 않은 후보의 효과로 해석하지 않습니다.

pre-core 선택/몸동작 검증은 PASS(경고 없음), compose와 exact runtime audit도 PASS입니다. Compose의 미해결 후보 의도 경고 4개는 사용자 앵커가 자유 문장에서 문자 그대로 보존되었다는 권고 경고입니다. 첫 compose에서 빠진 `fetish=0` brief 항목만 명시해 고쳤으며 prompt/core/gates는 바꾸지 않았습니다. 일반 몸동작 리뷰는 5/5, schema failure 0이고 기술적으로 qualified입니다. 해당 공통 auditor의 종료값 1은 사용자 판단 pending/대표 승격 불가 상태를 보존한 결과이며, 독립 전체장면 FAIL 판정을 대신하지 않습니다.

모든 arm은 동일한 raw requester bytes를 사용하며 이 arm의 장소·역할·사건·형태 선택은 agent-owned로 유지했습니다. 독립 설계 이후 상위 지침의 quick memory pass에서 과거 작업의 registry 제목/키워드만 한 번 검색했습니다. rollout, 이전 프롬프트, fixture, 이전 연구 내용은 읽거나 설계에 사용하지 않았습니다. 코어가 고정된 뒤 현재 arm 팩과 고정된 통합 assets 및 필요한 스킬 문서만 읽었습니다. 다른 arm 출력, 이미지 CLI fallback, 추가 생성, 하위 에이전트는 사용하지 않았습니다. 활성 데이터 수정도 하지 않았습니다.

단일 통합 후 시험이므로 변경 전후의 인과적 향상을 증명하지 않습니다. 사용자 선호·수용 판단은 아직 받지 않았습니다.

- [원본 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/generated_original.png)
- [독립 설계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/independent-design.precore.json), [고정 게이트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/expected_pixel_gates.frozen.json), [코어](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/authorial_core.json)
- [후보팩](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/candidate_pack.json), [존재·노출·선택](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/source_exposure_selection.json), [최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/prompt_en.txt)
- [Compose audit](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/composed_audit.json), [Runtime request](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/runtime_request.json), [Runtime audit](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/runtime_audit.json)
- [엄격 픽셀 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/strict_pixel_review.json), [공통 몸동작 리뷰 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/embodiment_pixel_audit.json)
- [단일 호출 ledger](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/image_runs.ndjson), [독립 실행 manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/run_manifest.json), [요약 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-integration-20261005/qualification/arm-a/qualification_summary.json)
