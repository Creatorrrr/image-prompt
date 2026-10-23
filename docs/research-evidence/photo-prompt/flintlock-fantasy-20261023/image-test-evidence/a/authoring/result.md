# Arm A — powderhouse artificer

실제 native 이미지 1회 생성은 성공했고, 고정 prospective 테스트 전체는 **FAIL**입니다. 정식 review-audit는 `status=pass`, `record_valid=true`, `technical_qualification=fail`을 반환했으며 workflow는 `review_record_validated`입니다. 모델 식별자는 응답에 없어 unknown으로 유지합니다. 첨부 얼굴 참조는 실제 `referenced_image_paths` payload에 포함됐으며, 생성된 저장 파일을 native 1536×1024로 직접 검사했습니다. 사용자 수용은 pending입니다.

## 독립성 및 고정 조건

일반 지식으로 만든 3개 완전 장면 중 seed `11434847005915700646`, 단일 draw `2`로 약제·화약 공방의 수석식 장치와 병 속 날씨 부적을 선택했습니다. 다른 arm의 파일·프롬프트·창작 결과를 읽지 않았습니다. frozen core `d27cb511b1bcbe919a8b47e883b3edcb2c835756c38f429f19dcca9f1b05f0cf`와 최종 prompt `132909030bcea7a497b1a5d401aa6275c179cbd94d24412186b38a913f7585c3`는 유지했습니다. 재검색·재생성은 없습니다.

## 데이터부터 픽셀까지

| 층 | 관찰 |
|---|---|
| 실행 세대 | 명시적 H-F2 `87ba6e2c8e0fbeabc22e20946ce4396a2f6d54c153f4c3e9bd5a3cdd079beaa5`; 기본 포인터 미변경 |
| 발급·노출 | 전체 27 distinct sources / 32 occurrences 검토. 신규 Flintlock B02 `cand_a87082f30f7752278e4d9b09e1867bac`가 두 질의에 노출 |
| 의미 검토 | curved wooden grip, one short barrel, external flint-gripping lock beside that same barrel; source SHA `68e026371fb9f7b38d90966f01a8765813e39e55e9a2c3a4712589fd617be2e6` |
| 사용 | B02 두 occurrence는 inspiration_only. native whole-source adoption/qualification은 하지 않음. 나머지 issued material은 비교 후 skip |
| 실제 prompt literal | “Its curved walnut grip sits below one short barrel; the external flint-gripping lock is visibly attached beside that barrel.” |
| 픽셀 | 외부 lock/수석/동일 총열의 연결은 보임. 곡선 wooden grip도 보이나 총구가 우측 프레임 밖이며 총열 전체와 짧음을 확인할 수 없어 B02 전체 case FAIL |
| 수용 | requesting-user feedback 아직 없음, pending |

F02는 출처 교정 중인 비채택 항목이고, A01/H08 등 미발급 후보도 선택하지 않았습니다. 이번 이미지는 데이터 추가의 인과적 개선 비교나 신규 전체 52개 qualification이 아닙니다.

## 사전 고정 테스트 결과

| 고정 gate | 판정 | 직접 관찰 |
|---|---|---|
| reference_appearance | PASS | 참조 얼굴 비율·짧은 검은 bob·wispy bangs의 외관 연속성. 정체·정확한 나이는 추정하지 않음 |
| flintlock_mechanism | PASS | wooden stock, flint-gripping cock, open frizzen, shallow pan이 함께 보임 |
| working_magic | PASS | 유리병 안 cloud와 forked blue lightning의 묘사가 보임 |
| coexistence_relation | PASS | 인물의 손·시험 레버·수석식 장치·병 속 효과가 같은 작업대 시험 장면을 구성. 눈은 카메라를 봐 원한 시선 관계는 약해짐 |
| body_contact | FAIL | 오른손이 레버 뒤에 쉬지 않고 레버에 닿음. 왼손 지지대 접촉·lock clearance는 보이나 전체 conjunction 실패 |
| whole_image | PASS | 인물 중심 사진이며 얼굴·장치·병 효과를 볼 충분한 픽셀 확보 |
| B02-R1 | FAIL / partial | 곡선 grip은 보이지만 총열 끝·총구가 잘려 short-barrel 전체 관계 미확인 |
| B02-R2 | PASS | 수석을 물린 외부 lock이 같은 총열 옆에 연결됨 |
| B02-N-barrel | FAIL / partial | 한 총열이 보이나 전체 끝과 짧음을 검증할 수 없음 |

`partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 적용했습니다. 정식 embodiment review는 ownership/reach/support 3 PASS, intended contact와 full-pistol visibility 2 FAIL로 제출했습니다. 실제 초자연적 인과나 발화 기능·통 내용물·고증은 정지 픽셀에서 확정하지 않습니다.

## 산출물

- 실제 prompt: `authoring/final-prompt.txt`
- 고정 사전 criteria: `authoring/prospective_pixel_gates.json`, `authoring/prospective-issued-source-gates.json`
- 직접 검사: `authoring/saved-image-inspection.json`
- 상세 testcase: `authoring/testcase-result.json`
- source→pixels: `authoring/source-to-pixel-trace.json`
- 정식 검토: `authoring/visual-review.json`, `authoring/review-audit-output.json`
- native 실행 기록: `image_runs.ndjson`, `run_manifest.json`
- 저장 이미지: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/flintlock-fantasy-20261023-a/returned-image.png`
- 원본: `/Users/chasoik/.codex/generated_images/01a167b4-399e-7bb1-be05-2d980b1f74bd/exec-9a2b5c2f-2332-45f2-84b7-f198e7c7cef7.png`
- 두 파일 동일 SHA256: `3719e798f46f1d7e48b211ecd150305d31e053af65dd4c1e0fa92338dfd6001e`
