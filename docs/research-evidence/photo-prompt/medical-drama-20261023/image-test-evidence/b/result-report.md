# Medical image test arm B — 평행봉 사이에서 발이 닿는 순간

전체 테스트: **FAIL**. 의료 재활 장면과 참조 외형은 읽히지만, 독립적으로 정한 좌우 발 배치와 A09의 치료사 통로 내부 위치를 모두 충족하지 못했다. 사용자 수용 판단은 pending이다.

- 도구: 내장 `image_gen.imagegen`, 실제 호출 **1회**, 재시도 0회. 관측된 이미지 모델명은 제공되지 않았다.
- 원본 픽셀: `image.png`; SHA256 `307e7fbb28b9e60a0d90936276c4a5d422903e9395f32ec8885dd12691c25ef4`.
- 독립 core SHA: `470e2d37a7b0441012a5d7917b7bcb55d7b6833cf18ef000d3c2f7f3510408d5`.
- H-F2 generation: `1d3013b5e422e72eb80bdd75189ebe25575ffa92aecc3378ed8ba79358b897bd`; 검색 5개(슬롯 3개 + 주제/기준 프롬프트), 반환 40개/서로 다른 source 40개.
- 구성 감사 PASS, 런타임/참조 감사 PASS. 구성 감사의 4개 경고는 독립 작성 근거로 보존된 intent coverage 경고이며 blocking failure는 없다.
- 새 의학 source 노출 8개: E09, C06, C01, C14, C05, A09, F08, E11. 실제 source-informed 사용은 A09 하나이다. `native_approval=false`이며 네이티브 전체 source 자격을 주장하지 않는다.
- 관리형 픽셀 리뷰 기록 감사 PASS (`record_valid=true`), 기술적 충족 판정 FAIL. 사용자 판단은 `pending/not_yet_received`로 유지된다.
- 실행 ledger run ID: `721bfe18312d200e`.

| 동결된 agent 테스트 | 관측 | 결과 |
|---|---|---|
| B1 같은 환자 양손과 서로 다른 평행봉 접점 | visible | PASS |
| B2 치료사 손→측면 gait-belt 손잡이→같은 환자 허리 | visible | PASS |
| B3 환자의 왼발이 오른발보다 앞 + 양발 바닥 지지 | visible | FAIL: 실제 오른발이 앞으로 나왔다 |
| B4 참조 얼굴·단발·앞머리의 읽을 수 있는 유사성 | visible | PASS: 정성적 외형 유사성 |
| B5 임상 재활 상황의 전체 가독성 | visible | PASS |
| A09 전체 source의 치료사 통로 내부 위치 | partial | FAIL: 뒤쪽 발과 오른쪽 레일 바닥 경계가 투영에서 모호하다 |

A09 `cand_a5140bd678bf5f49a95fc7588cee61d2` / source SHA `6623c01f221a8cb81858b9bf09212ddb177a94bf343d0ec9ab3405c3a228d73e`를 완전한 가시 의미로 검토했다. 독립 기준 프롬프트가 이미 환자·양손·두 봉·벨트 보조를 포함했고, 최종 구성은 “the therapist stands inside the right rail beside the patient, half a step behind his right hip”를 더했다. 실제 픽셀은 이 추가 관계를 완전히 입증하지 못하므로 A09 전체 case 역시 FAIL이다. E11은 보행기와 반대 손의 팔꿈치 근접까지 요구하여 대안으로만 비교했다. 현재 이미지의 벨트 접점만으로 E11을 사용했다고 주장하지 않는다.

따뜻한 창빛, 피부·면직물·금속 질감과 서로 연결된 임상 행동은 자연스럽다. 환자 실루엣이 먼저 읽히고 참조 여성의 얼굴은 오른쪽 위에서 관계를 이룬다. 첫 걸음, 회복 성공, 진단, 통증, 자격, 동의나 실제 치료 안전성은 정지 이미지로 판정하지 않았다. 발 좌우와 통로 위치는 사용자 요구로 승격한 제약이 아니라 사전에 동결한 agent 테스트 의무이다.

공유 checkout에서 각 arm의 입력·run·증거만 분리했다. manifest의 `worktree_id=image-prompt-primary-medical-b`는 arm-local provenance label이며 별도 Git worktree 생성 증거를 뜻하지 않는다. 다른 arm의 프롬프트·source 선택·이미지를 이 arm에 사용하지 않았다.

자세한 입력과 결과: `testcase-frozen.json`, `source-specific-gates-reviewed.json`, `new-medical-source-exposure.json`, `composition-comparison.md`, `final-prompt.txt`, `exact-runtime-request.json`, `pixel-review.json`, `managed-visual-review.json`, `run_manifest.json`, `image_runs.ndjson`.
