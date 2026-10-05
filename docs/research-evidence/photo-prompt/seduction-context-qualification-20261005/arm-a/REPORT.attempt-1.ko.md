첫 네이티브 이미지 생성은 출력 단계의 moderation_blocked 오류(sexual)로 차단되어 이미지가 반환되지 않았다. 실제 호출은 1회이며 원본 이미지 경로나 해시는 없다.

7개 장면 관찰 게이트와 5개 신체 연결 게이트는 모두 UNOBSERVABLE로 보존한다. 픽셀 점수, 이미지의 유혹적인 인상 또는 사용자 수용을 판정하지 않았다. 프롬프트 및 런타임 감사 PASS는 생성 이미지의 성공을 뜻하지 않는다.

원본 오류는 native_attempt_1_error.json, 첫 호출 기록은 runs/image_runs.ndjson 및 run_manifest.attempt-1.json에 보존되어 있다.
