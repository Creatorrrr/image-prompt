Arm B의 독립 광학 시험실 컨셉으로 V6 프롬프트 작성, 원본 이미지 1회 생성, 전체 픽셀 기준 판정을 완료했다. **전체 기술 자격은 FAIL**이다. 길이·좁은 폭·얼굴/머리 참고는 읽히지만 `sinewy` 표면 윤곽, 양손의 허리 높이 접촉, 작은 부품을 막 놓은 순간은 충족되지 않았다. 사용자 수용 판단은 pending이다.

| 판정 집합 | 통과 | 실패 | 전체 |
|---|---:|---:|---:|
| 독립 동결 초기 기준 | 3 | 3 | 6 |
| 채택한 `bm_long_limb_build` 프로필 | 4 | 0 | 4 |
| 신체 관계 기준 | 4 | 1 | 5 |
| 합집합 | 11 | 4 | 15 |

| 기준 | 판정 | 원본 픽셀 근거 |
|---|---|---|
| B1 길이 비율 | PASS | 몸통을 기준으로 길게 이어지는 다리와 가까운 팔을 비교할 수 있고 머리·양발이 모두 들어온다. |
| B2 좁은 가로 폭 | PASS | 어깨·골반과 위팔·허벅지의 가로 윤곽이 좁고 가늘게 읽힌다. 긴 다리와 별도로 판정했다. |
| B3 얕은 근육/힘줄 윤곽 | FAIL | 가까운 위팔·전완은 주로 매끈한 표면과 조명 그라데이션이다. 얕고 긴 근육·힘줄 윤곽을 조명에서 분리하기 어렵고 먼 위팔은 일부 가려진다. |
| B4 얼굴·머리 참고 | PASS | 짙은 단발·이마 잔가닥·큰 눈·입술·부드러운 얼굴 윤곽이 원본에서 비교 가능하다. |
| B5 양손 접촉 | FAIL | 두 손은 다른 조절부에 닿지만 가까운 손은 골반 부근, 휠 손은 가슴 높이로 나타나 양손의 허리 높이 조건을 벗어난다. |
| B6 광학 장면과 순간 | FAIL | 분할 거울·원형 짐벌·작업등과 인물의 접촉은 읽힌다. 새로 놓인 작은 부품을 기존 브래킷과 특정하여 연결할 수 없어 placement pause는 불관측이다. |
| 프로필 component_1: 몸통 기준 | PASS | 같은 인물의 몸통 길이와 사지가 같은 전신 구도에서 비교된다. |
| 프로필 component_2: 사지 길이 | PASS | 가까운 팔 전체 연결과 양쪽 다리의 상·하부 길이 관계가 보인다. 가려진 먼 위팔의 수치를 추정하지 않는다. |
| 프로필 component_3: 사지 폭 | PASS | 노출된 팔·허벅지·아래 다리의 가는 가로 윤곽을 옷 주름과 분리해 볼 수 있다. |
| 프로필 owner_state | PASS | 보이는 팔·다리 연결은 중앙의 같은 인물에 속한다. 거울 속 외관은 같은 인물의 반사로 읽힌다. |
| 신체 소유 관계 | PASS | 손과 다리는 중앙 인물의 연결된 부위이다. |
| 관절 연결과 도달 | PASS | 조절부까지 팔과 손이 무리한 교차·늘어남 없이 이어진다. 대상의 잘못된 높이는 별도 실패이다. |
| 지지와 균형 | PASS | 양쪽 신발이 바닥에 닿고 다리가 서 있는 몸을 지지한다. |
| 접촉과 공간 | FAIL | 낮게 앞으로 나온 두 조절부와 양손 허리 높이, 놓인 작은 부품의 공간 배치가 원본에 보존되지 않았다. |
| 가시성과 투영 | PASS | 얼굴·두 접촉·몸통·다리·양발이 판정 가능한 전신 구도이다. 작성한 near-frontal보다 몸이 더 비스듬하고 먼 위팔은 일부 가려지는 편차가 있다. |

이 기준은 서브에이전트가 작성한 합성 시험이며 실제 사용자의 체형 정의가 아니다. 초기 기준을 생성 후 완화하거나 바꾸지 않았다. `partial_is_fail=true`에 따라 불명확한 표면과 불관측 순간을 실패로 남겼다. 작성한 인물 나이는 28세이며 참고와 결과 픽셀에서 수치 나이나 정체성을 인증하지 않는다. 참고는 보이는 얼굴·머리 외관에만 사용했다.

일반 후보 `bm_wiry_definition`은 좁은 가로 폭과 소유 관계는 보이지만 국소 근육면·힘줄 윤곽의 실현이 실패했다. `willowy_long_limb_proportion`과 opt-in `bm_long_limb_build`의 길이·폭·소유 관계는 통과했다. 후보 노출, 채택, 문자 감사와 픽셀 실현은 각각 별도 근거이다.

`slender_linear_build`는 기존 `owner_separation` component terms가 같은 뷰의 몸통·사지 가로 폭 비교를 요구하지만 evidence-must-mention terms는 높이·근육·가슴·골반을 별도로 선언하거나 건강·체중·매력 추론을 보고하는 문구를 요구하는 불일치가 있다. 이 optional 프로필은 거절하고 프롬프트에 보고용 문장을 넣지 않았다. 독립적으로 고정한 B2는 유지했으며 그 픽셀 판정은 PASS이다. 이 제한을 기록하면서 운영 데이터를 변경하지 않았다.

프롬프트 감사와 정확한 런타임 요청 감사는 PASS이다. `render_review_audit.json`은 schema failure 0개, 누락 기준 0개이며 `embodiment_contact_and_space`의 픽셀 실패를 보존하여 `failed_technical_hard_gates`로 반환한다. CLI 종료 코드 1은 기록 형식 오류나 이미지 생성 오류가 아니라 기술 자격 실패에 따른 결과이다. 생성 원장 status `success`는 이미지가 생성·저장됐다는 뜻이며 전체 픽셀 자격과 별도이다.

동결 입력 14개와 운영 입력 92개를 종료 시 다시 해시 검증하여 모두 일치했다. 실제 `image_gen.imagegen` 호출은 1회이며 추가 생성이나 이미지 편집을 하지 않았다. 다른 arm의 작성물은 읽지 않았다. 전체/원본 뷰에서 동일한 저장 이미지 바이트를 판정했으며 확대 생성물로 원본 증거를 대체하지 않았다.

한 컨셉·한 이미지의 관찰 결과이다. 비교 기준 이미지나 데이터 변경 ablation이 없으므로 데이터 보강의 고립된 인과 효과나 모든 생성의 안정성으로 일반화할 수 없다.

| 저장 근거 | 파일 |
|---|---|
| 독립 추첨·뜻 해석 | `random_draw.json`, `meaning_resolution.json` |
| 최초 동결 | `freeze_manifest.json`, `authorial_core.json`, `initial_pixel_gates.json` |
| 실제 사용자 요청 / 합성 시험 분리 | `request_envelope.json`, `actual_user_authorization.txt`, `synthetic_test_case.txt` |
| 정확한 독립 프롬프트 | `standalone_prompt_en.txt`, `standalone_negative_en.txt` |
| V6 노출·선택 근거 | `candidate_pack.json`, `composer_view.json`, detail views, `candidate_choice_provenance.json` |
| 문자·런타임 감사 | `composed_audit.json`, `runtime_audit.json`, `image_render_request.json`, `native_image_args.json` |
| 저장 원본 | `generated_images/optical-bay-attempt-01.png` (1024×1536) |
| 생성 시도·원장 | `native_attempt_01.result_metadata.json`, `image_runs.ndjson`, `run_manifest.json` |
| 전체 픽셀 판정 | `pixel_test_review.json`, `render_review.json`, `combined_pixel_review.json`, `render_review_audit.json` |
| 종료 무결성 | `completion_integrity.json` |

Pack ID `563f01179649424d`, run ID `6264e473d86a7e26`. Exact positive prompt SHA256 `4f3c000b47ee9ee1bb44cc558cd34f728f7659ee4132ea4fe0a350c3faf81041`. Exact runtime prompt SHA256 `1709930ade5275e92f14746772f0599b98963177e2d492fad44a6bdfa4143ec0`. Saved native PNG SHA256 `a06b1b31592b418025b36404decc9333a16e33ba647edd7fe5f249395f2b9d4a`. Candidate pack file SHA256 `c47bdadf8abdf7867034d2c4e71c019add1f472b9af5cf074b3711863a87b719`.
