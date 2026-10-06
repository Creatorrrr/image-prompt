# A arm 결과

**PASS — 비가 갠 돌다리의 출발 직전.** OS 난수로 3개 독립 여행 컨셉 중 선택했고, 후보 미노출 상태에서 기본안과 테스트를 동결했다. 생성 호출은 native `image_gen.imagegen` 1회이며 추가 생성은 중단했다.

- 원본 이미지: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/harry-potter-integration-20261006/render-tests/arm_a/image_attempt_1.png` (1536×1024, SHA-256 `53d2c1f01c4e72e4baa19eaf65d58bc919455d29b7a2ec359dd3b0d5bbe4572b`).
- 최종 프롬프트: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/harry-potter-integration-20261006/render-tests/arm_a/final_prompt.txt`.
- 후보/표현 추적: `candidate_expression_trace.json`; 픽셀 판정: `native_pixel_review.json`; 독립 호출 장부: `run_manifest.json`, `image_runs.ndjson`.

참조 얼굴/머리와 4개 외형 주제를 위한 5개 동결 gate, 15개 all-of 세부, 5개 embodiment gate가 같은 원본 이미지에서 통과했다. `appearance_h002`의 셔츠→니트 안층, 타이→셔츠 전면, 타이→니트 목선 아래, 니트→겉로브 안층 네 관계를 노출·채택·최종 문구·픽셀 단계로 분리해 남겼다. 대체 표현은 ‘한 사람의 칼라 셔츠 위에 타이를 늘어뜨리고 니트 목선이 이를 겹치며 긴 로브가 그 세 안층을 감싼다’이다. 정확한 retrieval trigger와 대체 표현의 반사실적 기여는 public pack에서 확인할 수 없다.

빗자루·흰 올빼미 편지·첨탑 석조 성은 독립 기본안에서 시험했고 모두 픽셀 PASS다. 해당 새 후보가 이 pack에 노출됐다는 증거는 없다. 필수 특징의 가림이나 실패는 없다. 부츠의 접지, 빗자루의 완전한 하단 끝, 일부 성의 최상단 끝은 프레임 밖이므로 그 비필수 세부는 별도 한계로 기록했다.

`audit_moe_render_review.py`는 `technical_qualified: true`, 실패·schema 오류 없음으로 판정했지만 사용자 수락이 미수신이어서 exit 1이다. 사용자 수락이나 보편적 데이터 성능을 PASS로 주장하지 않는다.
