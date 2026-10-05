이 보고서의 픽셀 판정과 generic gate 수치는 arm 작성자의 원래 자기 검토입니다. Coordinator의 별도 판정을 합치거나 대신 사용하지 않습니다.

Arm 1의 내장 이미지 생성은 1회 성공했지만, 외형 all-of 검증은 FAIL입니다. 최종 프롬프트와 정확한 런타임 입력 감사는 PASS, 실제 키워드 픽셀 판정은 2/7 PASS·5/7 FAIL·0 UNOBSERVABLE입니다. 요청자의 수락은 아직 없습니다.

독립 난수 `7926664881701043627`로 바닷가 천문관 투영실에서 별 투영기 램프를 점검하는 가상의 30대 성인 보존가를 선택했습니다. 보브, 앞머리, 베레모, 안경, 귀 장신구와 모든 구체 장면은 에이전트 선택입니다. 원 요청은 byte-exact 상태로 유지됐고, 얼굴 참조 외에 이미지 입력을 추가하지 않았습니다. 후보·프로필 접근 전에 core, baseline, 신체 검토와 9개 중립 관찰 범주를 고정하고 검증했습니다.

| 외형 키워드 | 결과 | 실제 픽셀 |
|---|---|---|
| 턱 길이의 blunt bob | FAIL | 작은 보브는 보이나 끝이 가늘게 흩어져 blunt cut이 부분 충족입니다. |
| 눈썹 높이 일자 앞머리 | FAIL | 길이가 다른 곡선형 see-through 가닥이며 공통 일자 끝선이 없습니다. |
| 얇은 둥근 금색 안경 | PASS | 두 렌즈 테두리, 코 다리, 눈의 가독성이 같은 얼굴에서 보입니다. |
| 버건디 베레모 | PASS | 둥근 납작 크라운과 머리에 붙은 하단 경계, 왼쪽 기울기가 보입니다. |
| 오른쪽 귀 뒤로 넘긴 머리 | FAIL | 노출된 것은 피사체의 왼쪽 귀이고 오른쪽 귀는 머리카락에 가려집니다. |
| 오른쪽 상부 귀의 silver cuff | FAIL | cuff 형태는 보이나 지정 반대 귀에 놓였습니다. |
| 같은 오른쪽 귓불의 teardrop earring | FAIL | 드롭과 귀 연결은 보이나 지정 반대 귀에 놓였습니다. |

엄격한 활성 pack 렌더 게이트는 5개입니다. 손·팔 소유, 관절과 도달, 지지, 접촉은 4/5 PASS이고, 지정한 오른쪽 귀의 관계를 보여주지 못해 `embodiment_visibility_and_projection`은 FAIL입니다. 렌더 검토 스키마 실패는 0개입니다. 별도 render-repair 계약이 없으므로 rr 게이트는 해당하지 않습니다. 부분 충족이나 다른 쪽 귀의 대체 증거를 PASS로 올리지 않았습니다.

| 통합 프로필 | 소스 매칭 | 일반 후보 노출 | 시각 프로필 노출 | 선택 | 활성 게이트 |
|---|---|---|---|---|---|
| ca_compact_bob | 독립 외형과 일치 | 없음 | 없음 | 없음 | 0 |
| ca_blunt_fringe | 독립 외형과 일치 | 없음 | 없음 | 없음 | 0 |
| ca_spectacle_frame | 독립 외형과 일치 | 없음 | 없음 | 없음 | 0 |
| clothing_ct108_v2 | stud connector를 지정하지 않아 부분 매칭 | 없음 | 없음 | 없음 | 0 |

현재 registry 1,671개와 index 1,671개의 바인딩은 맞습니다. 일반 후보 64개와 시각 프로필 후보 8개가 노출됐으나 위 세 신규 프로필은 0/3 노출·0/3 선택입니다. 노출된 prism-edge 효과는 광학 장소에 추가할 수 있었지만 머리 구조의 가독성을 개선하지 않아 거절했습니다. 그 밖의 노출된 backless·정서·초현실 후보도 이 장면에 필요한 의미가 아니어서 선택하지 않았습니다. source에 존재한다는 사실과 실제 노출·선택·픽셀 기여를 분리합니다. 기존 안경 형상이 렌더됐다는 사실은 신규 데이터의 retrieval 성공을 증명하지 않습니다.

전체 이미지는 따뜻한 작업실과 차가운 항구 배경 사이에서 얼굴, brass lamp와 카메라 시선이 연결된 차분한 인물 사진으로 읽힙니다. 외형 충실도와 별도로 작업 분위기와 얼굴 참조는 유지됐습니다. 관능 1의 은은한 친밀감은 읽히지만 사용자 선호 판정은 아닙니다.

원본은 `native_result.png`(1237 × 1272), 프롬프트는 `prompt_en.txt`, negative는 `negative_en.txt`, 실제 전달 문자열은 `runtime_prompt_en.txt`에 있습니다. `native_tool_args.json`, `runtime_request.json`, 각 감사, `frozen_pixel_criteria.json`, `self_pixel_review.json`, `image_runs.ndjson`, `run_manifest.json`과 `source_snapshot.json`에 exact inputs·hashes·provenance를 보존했습니다. 다른 arm의 입력이나 결과를 사용하지 않았고, data 수정·index 재생성·재시도·CLI/API fallback·commit·push를 수행하지 않았습니다.

이 결과는 단일 7-keyword 장면에 대한 검증이며 전체 100건의 native qualification을 뜻하지 않습니다.

실행 접근 이력에 한 가지 한계가 있습니다. developer의 quick-memory-pass 지시에 따라 core 고정 전에 `MEMORY.md`에서 `precore|request_envelope|photo-prompt-image-generator`의 일치 행을 한 번 rg 검색했습니다. 출력 범위는 1097, 1101, 2304, 2316, 2935, 2943, 2985행의 rollout 포인터·작업 흐름 키워드뿐이었고, 실제 이전 prompt/profile/pack/render나 rollout summary는 읽지 않았습니다. 장면·외형·후보의 영감으로 채택한 내용은 없습니다. 다만 photo 스킬의 엄격한 pre-core 허용목록에는 memory 접근이 없으므로 clean strict whitelist로 주장할 수 없습니다. `operational_memory_access.json`에 이 운영 접근과 실제 이미지 입력을 분리해 기록했습니다. 입력으로 사용하지 않았다는 설명은 에이전트 선언이며 hashes만으로 독립 증명되지 않습니다. 고정된 core나 이미지 bytes는 변경하지 않았습니다.

작성자 자기 검토는 `self_pixel_review.json`으로 byte-exact 복원했습니다. 이전 author artifact hash `fb085f919b88d75c5402850276eb56db7c0739066e040b1cf7620fb210e5ec83`과 복원본 hash가 같습니다. 복원 경위는 `self_review_recovery.json`에 있습니다. Coordinator가 남긴 `independent_pixel_review.json`과 별도 `../coordinator-native-inspection/arm-1-coordinator-review.json`은 그대로 보존합니다.

총 PASS 수는 양쪽 모두 2/7이지만 판정 근거의 불일치를 유지합니다. 작성자는 명시한 blunt-cut 보브를 FAIL, 베레모 크라운을 PASS, 반대쪽 귀의 cuff/drop을 FAIL로 기록했습니다. Coordinator는 고정된 compact relation을 PASS, 완전한 베레모 크라운을 FAIL, 필요한 쪽 귀의 cuff/drop을 UNOBSERVABLE로 기록했습니다. Generic visibility 해석도 다르며 원래 작성자 4/5 PASS·1 FAIL을 바꾸지 않았습니다. Coordinator 수치는 root의 전달 메시지에 따른 설명이고, 복원에 coordinator의 JSON 판정을 사용하지 않았습니다.
