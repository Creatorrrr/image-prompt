# A 독립 재시험 결과

인물 중심 의전 풍자 `silence_award`를 원본 참조와 최신 스킬로 한 번 생성했다. 최초 독립 baseline SHA `c46f1ba2f90d62c5a409abb3134c4d58d2a9117947ba182f8c4bd7432dc901b7`는 봉투 교정 과정에서도 그대로 유지했다. 실제 도구에 보낸 최종 프롬프트 SHA는 `6caf0028341c848c1cc00e02b840575e73bb967d0c7d4c906a76ef35eedea8f4`로 감사본과 같다.

최종 설치 릴리스 `af8d87...`에서 5개 질의가 40건/39개 고유 소스를 반환했고 전부 검토했다. 신규 소스는 V090 표어판, V019 암부 얼굴 2개다. 10개 완성 사진 대안을 비교해 B1을 골랐다. 신규 완전 후보/native 계약 채택은 **0개**다. V090의 일반적인 글자-물리 운반체 경계 속성만 기존 빈 액자 아랫레일의 `APPROVED` 인쇄로 참고했으며, 성인 전경 인물과 직사각 표어판의 전체 실현을 채택했다고 주장하지 않는다. V019는 닫힌 나이 범위와 참조 얼굴 가시성 때문에 미채택했다.

원본 `APPROVED` 글자는 아랫레일 안에 읽혀 일반 속성의 프롬프트→실제 입력→픽셀 전이는 확인됐다. 원래 있던 빈 표창판·로제트·올리브 재킷·자·빈 액자·참조 얼굴/머리는 신규 전이에서 제외했다.

엄격한 픽셀 판정은 **FAIL**이다. 자의 양끝, 표창판의 양 상단 모서리와 사무관의 연결 팔은 함께 보이지만, 미리 검토한 정확한 자 중앙 잡기 대신 화면상 중앙 오른쪽을 잡았다. managed embodiment 5게이트 중 4 PASS/1 FAIL이고, 리뷰 기록 감사는 유효하다. 시선도 측정 손보다 사무관 얼굴 방향에 가까워 전체 프롬프트 충실도에서 별도로 FAIL로 남겼다. 생성·기록 성공과 전체 픽셀 충족/사용자 수락을 구분했다.

실제 native 호출은 **1회**, ledger 1행 `d1905a21c6d1125b`이다. 도구 응답에 실제 모델 ID가 없어 **unknown**으로 기록했다. 사용자 수락은 pending이다. 주제 문구 교정과 새 샘플 seed가 함께 달라져 전후 노출 차이를 주제 수정 단독효과로 주장하지 않는다.

- 원본: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/marine-literature-retest-20261024-a-v5/original.png`
- 원본 SHA: `865ea1145dfbeb099ef3d055624e01b3e5512f4f8069799437a0ef2d52584dc1` (1237×1272 PNG, 도구 반환 파일과 바이트 동일)
- 완성 대안/소스 검토: `composition-comparison.md`, `source-review-v5.json`
- source→literal→actual tool→pixels: `source-prompt-transfer-v5.json`
- 실제 도구 입력: `actual-tool-input.json`
- 픽셀 관찰: `original-pixel-review.json`
- managed 리뷰: `visual-review.json`, `review-audit-output.json`
- 실행 기록: `image_runs.ndjson`
