# arm B 결과

콘셉트: 비가 갠 유리 지붕 대합실의 임시 촬영 세트에서 빈티지 조명의 각도를 조절하는 성인 패션 화보. Seed 739821.

결과: **UNSCORED — 도구 출력 단계 차단**. 실제 image_gen 호출 1회. 반환 이미지와 로컬 원본 경로가 없으므로 native/thumbnail 픽셀 검토를 하지 않았고 재시도와 CLI 대체도 하지 않았다.

precore 검증, composed 감사, 정확한 런타임 입력 감사는 모두 PASS. 이것은 픽셀 구현 성공을 뜻하지 않는다. 원장과 독립 manifest는 recorder 검증을 통과했다.

전체 visual profile 후보 8개, 신규 패션 owner profile 후보 6개가 노출되었다. focal mesh/navel profile 2개 중 abdominal mesh 1개를 전체 3개 component/gate와 함께 채택했다. navel 후보는 원단 없이 uncovered 상태를 요구하므로 독립 기준인 메시를 통해 보이는 실제 배꼽과 맞지 않아 거절했다. 배꼽 의미는 pre-core typed assertion으로 유지했다. 일반 후보 5개를 채택했고 creative 후보 6개는 모두 거절했다.

| 목표 판정 | 결과 |
| --- | --- |
| 한정된 복부 피부 위 실제 fine mesh 망눈 | UNSCORED |
| bodice hem 아래·trouser waistband 위 실제 배꼽 | UNSCORED |
| 메시 옆 연속된 불투명 원단 커버리지 | UNSCORED |
| 성인 얼굴·머리 참고 범위 | UNSCORED |
| 오른손 lamp tilt knob 접촉과 지지 | UNSCORED |
| 얼굴·복부 패널 가시성 | UNSCORED |

차단 정보: HTTP 400, moderation_blocked, output stage, sexual. Request ID 04e1b08d-87f1-4c70-b8e9-8db1b2360246.

정확한 프롬프트는 prompt_en.txt, 런타임 바이트는 runtime_prompt.txt, reference 경로/hash/tool 입력은 render_request.json, 상세 차단 응답은 native_tool_error.json에 보존했다. 첨부 사진은 실제 도구 입력에 전달했으며 얼굴·머리의 보이는 외양 참고로만 사용했다.
