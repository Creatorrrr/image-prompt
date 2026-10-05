B안의 최종 결과는 `blocked_unscored`다. 고정된 원본 입력으로 내장 `image_gen.imagegen`을 2회 호출했으며, 첫 출력 차단 후 부모가 승인한 한 번의 동일 입력 재시도도 출력 단계에서 차단됐다. 반환된 이미지는 0개다. `generated_original.png` 또는 대체 이미지를 만들지 않았고, 픽셀 점수와 전체 인상은 평가하지 않았다. API 전환이나 추가 호출은 없었다.

독립 장면은 저녁 공연이 끝난 아르데코 극장 발코니의 두 성인이다. 가까운 얼굴 사이 거리, 서로에게 향한 시선, 여성의 오른손 끝과 상대 남성의 왼쪽 안쪽 손목 사이 가벼운 접촉, 이미 돌아선 상대의 얼굴과 상체가 대화의 유혹적인 멈춤을 만든다. 초상은 관찰 가능한 얼굴·짧은 짙은 단발·앞머리만 참고했으며, 초상에서 나이·몸·성격·전기를 추론하지 않았다. 두 성인은 장면에서 작성한 성인 설정이다.

사전 코어, 기본 프롬프트, 특징 선택, 신체 검토, 관찰 게이트를 후보 접근 전에 고정했다. 요청 계보는 새 장면이므로 null이다. sensual=3과 fetish=0은 부모가 정한 실험 값이며 사용자가 직접 지정한 숫자가 아니다. 저장된 creativity=1을 유지했다. 주 장면의 가까운 거리와 손목 접촉은 검색 결과 이전에 존재했다.

| 증거 층 | 결과 | 한계 |
|---|---|---|
| 사전 특징 선택 | PASS, 경고 0 | 선택·문자열 결합 검증 |
| 구성 감사 | PASS | 후보 부족으로 독립 문장을 보존했다는 경고 4개 |
| 정확한 런타임·참조 감사 | 두 시도 모두 PASS | 입력·참조 바이트 검증 |
| 시각 프로필 적용 | 8개 노출, pfe_face_garment 1개 채택 | 얼굴과 네크라인 동시 가독성을 돕는 보조 광학 관계 |
| 일반 슬롯 후보 | 64개 노출, 시선 후보 1개 채택 | 프롬프트 적용 증거만 확인 |
| 도구 출력 | 2회 모두 moderation_blocked | 원본 이미지 없음 |
| 픽셀·전체 인상·사용자 수용 | UNOBSERVABLE / 미수신 | 점수 없음 |

채택한 일반 후보는 `slot:expression:engaged_lowered_lid_target_gaze`다. 전체 원본 행을 읽은 뒤 기존 낮은 윗눈꺼풀 시선에 “her lower lids remain gently taut, coherent catchlights stay present, and both irises fix on this same adult companion”을 추가했다. 같은 상대를 향한 깨어 있는 눈의 구성 요소를 명시한 실제 문장 변경이다. 이것이 이미지를 개선했다는 인과 증거는 없다.

선택한 `pfe_face_garment`는 이미 작성된 얼굴과 와인색 실크 네크라인을 한 프레임에서 구분해 읽도록 하는 보조 프로필이다. 세 구성 의무와 세 렌더 게이트를 모두 확인했고, 그 의무 문장이 최종 프롬프트에 문자 그대로 들어 있다. 유혹을 정의하는 프로필로 보고하지 않는다. 노출된 8개 프로필 중 핵심적인 가까운 거리·상호 주의·의미 있는 손목 접촉을 직접 결합한 프로필은 없었다. 별도 `visual_profile_trace.json`과 `slot_candidate_trace.json`에 노출, 전체 채택 계약, 원본 자료, 문장 증거, 거절 이유를 분리했다. 성인 축의 12개 반환 후보는 채택하지 않았으며 해당 검색 레인은 keyword, semantic_candidate_coverage는 0이었다. 공개 프로필의 hybrid 출처 표기만으로 실제 임베딩 실행을 증명하지 않는다.

| 호출 | 실행 ID | 결과·단계 | 요청 ID |
|---|---|---|---|
| 1 | 6c764da64568cca7 | moderation_blocked / output / sexual | e323b175-1f83-4c12-8fd3-b2c9051bf985 |
| 2 | 9ddbf55a0f0d9a98 | moderation_blocked / output / sexual | 29cb1b07-e1ac-40d5-9a36-c7a9f97a9b5a |

두 번째 실행의 retry_of는 첫 실행 ID와 연결됐다. 누적 호출 수는 2이며 두 시도의 코어·팩·최종 프롬프트·네이티브 인자·참조·게이트 바이트는 동일하다. 오류는 실제 내장 도구가 던진 원본 문자열을 exact_string으로 보존했다. 출력 단계의 sexual 분류는 반환된 도구 정보다. 특정 문구나 보이지 않은 출력의 어떤 부분이 원인인지는 확인할 수 없다.

전체 이미지 인상을 먼저 관찰한 뒤 강도 라벨과 비교하는 절차는 이미지가 없어 수행할 수 없었다. 따라서 인상이 유혹적이었다거나 아니었다는 판단도 없으며, 실제 욕구·동의·참조 인물의 의도를 주장하지 않는다.

| 독립 관찰 게이트 | 결과 |
|---|---|
| B01 — The primary subject is visibly a photographic adult portrayal with the portrait-visible face and short dark bob/fringe carried through. Adult authorship is stated in the prompt; age is not inferred from the reference. | UNOBSERVABLE |
| B02 — One identifiable adult companion shares the foreground interaction; the woman's attention can be traced to that same companion. | UNOBSERVABLE |
| B03 — Their faces are within approximately one hand breadth with the gap clearly visible; bodies are oriented toward each other. | UNOBSERVABLE |
| B04 — Both faces visibly direct their gaze toward each other rather than the capture camera or an unrelated object. | UNOBSERVABLE |
| B05 — Her right fingertips visibly touch the exposed inner surface of his left wrist above the cuff; the touched wrist belongs to the companion and both forearm chains are legible. Partial or occluded contact fails. | UNOBSERVABLE |
| B06 — The companion has already turned his face and upper chest toward her and shows a small answering facial response; a future or inferred response fails. | UNOBSERVABLE |
| B07 — The woman shows a poised small half-smile with subtly parted lips or comparable suspended facial affect; the image reads as a held interpersonal pause rather than a neutral activity. | UNOBSERVABLE |
| B08 — The theater balcony / evening threshold remains readable but subordinate; waist-up composition shows both faces and contact together with coherent hands and material behavior. | UNOBSERVABLE |

| 정확한 계약 게이트 | 결과 |
|---|---|
| vo_pfe_face_garment_1 | UNOBSERVABLE |
| vo_pfe_face_garment_2 | UNOBSERVABLE |
| vo_pfe_face_garment_3 | UNOBSERVABLE |
| embodiment_body_ownership | UNOBSERVABLE |
| embodiment_joint_chain_and_reach | UNOBSERVABLE |
| embodiment_support_and_balance | UNOBSERVABLE |
| embodiment_contact_and_space | UNOBSERVABLE |
| embodiment_visibility_and_projection | UNOBSERVABLE |

점수는 양쪽 모두 null이며, 0/8 픽셀 실패로 해석하지 않는다. 첫 호출 직후 저장한 렌더 검토 감사는 결과 경로·해시·픽셀 증거가 없어서 닫힌 실패 상태를 반환했다. 해당 감사와 검토를 attempt1_unavailable 파일로 보존했으며, 이는 관찰된 이미지 결함 판정이 아니다. 최종 차단 상태와 무점수 게이트 목록은 `blocked_render_review.json`에 있다.

첫 시도의 매니페스트는 `run_manifest_attempt1.json`, 동일 입력 재시도 매니페스트는 `run_manifest_attempt2.json`에 보존했다. `image_runs.ndjson`에는 두 실제 호출만 있으며 `run_manifest_all_attempts.json`이 누적 상태와 frozen binding을 연결한다. 부모가 제공한 원본 참조는 main `98ca92a070a6127a2e03877ec8a5d3f0dfda0467`이다. 런타임·주 저장소 소스를 편집하거나 다른 실험안 자료를 읽지 않았다.

최종 프롬프트: [final_prompt.txt](final_prompt.txt). 상세 결과: [RESULT-SUMMARY.json](RESULT-SUMMARY.json). 원본 오류: [1회차](native_attempt_1_error_evidence.json), [2회차](native_attempt_2_error_evidence.json). 모든 산출물 해시는 [ARTIFACT-SHA256.json](ARTIFACT-SHA256.json)에 있다.
