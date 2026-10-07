case-02 round-2 검증 결과는 technical audit·graph accuracy·freshness·request/meaning fidelity PASS, artistic judgement PARTIAL이다. 같은 동결 영어 baseline을 보존했고 초기 run에는 쓰기하지 않았다. 이미지 픽셀과 사용자 수용 증거는 없다.

| 구분 | 판정 | 현재 stage의 독립 근거 |
| --- | --- | --- |
| technical audit | PASS | pre-core valid=true, composed status=pass와 failures=[], 자유 서술 보존 경고 7건 |
| graph accuracy | PASS | 슬롯 후보 64개: 연결 16개·정상 미연결 48개; 원본 재구성 2,971개 간선과 13,517개 노드의 양방향 목록 일치 |
| freshness | PASS | 현재 조회 3건 성공, scratch 손상 보고서와 wrong root 실제 거부 |
| request/meaning fidelity | PASS | 구리·리넨·접힘·이른 아침·자연광·사람 제외 및 기존 controls/features/embodiment/core 의미 보존 |
| artistic judgement | PARTIAL | 형태·결·빛의 관계는 맞지만 reflection 문구의 광학적 소유가 다의적이고 픽셀 검증 없음 |

ISOLATION.json의 입력 11개와 sealed runtime 멤버 165개, 관리 도구 코드 8개를 해시로 대조했다. 복사된 초기 입력에는 기술 사본이 없어 이전과 동일한 2개 표기 교정을 별도 사본으로 재현했다: catalog_path canonical identifier와 user_exclusions의 people → 사람. corrected core 파일 해시는 `3144e0a3b9ad8762fd2e4bb7fd96ed9d4298f31987175d0911cd8a35f03f6231`이며 normalized core hash는 처음과 동일한 `9d3e741fa81d1fa1bbd9fd216a8eccac07e74aace348999713c5119c05a38032`이다. 영어 baseline과 요청 의미를 바꾸지 않았다.

실제 로컬 lexical 실행은 generation `db193081d04dba97d754e8809cebfb67a97133c7162a5429da965d53e9c88462`, pack `5439f63faea1192b`를 생성했다. generation은 제공된 수정 세대와 일치하며 receipt observation의 root는 이 round-2/skill이다. 모든 runtime 및 관리 명령은 round-2/runtime을 지정했다. 기존 case-02/venv Python만 재사용했고 다른 사례·기본 checkout·메모리·테스트·coordinator runtime-base에는 접근하지 않았다.

패치된 human receiver 두 후보는 source에서 `kind=[human]`, `for_any=[human]`을 가진다: `pr_casual_crop_subject_legibility_candidate`와 `rb_shared_wind_response_candidate`. 둘 다 이 no-people/object core의 ordinary 슬롯과 augmentation에 노출되지 않았다. 이 정물 사례에서 첼로 hard obligation이나 첼로 clarification은 활성화되지 않았다. 첼로의 긍정 연주 동작 사례까지 이 실행으로 검증했다고 주장하지 않는다.

새 sampled JPEG 후보 `pr_jpeg_edge_blocking_candidate`는 format 효과를 선언하지만 이 core의 format 차원은 열리지 않았다. 재게시 파일/스크린 맥락도 없다. 노출된 eligible 표지는 최종 채택 권한이 아니므로 실제 구성에서 그 후보를 명시 거부했다. 이 관찰은 patch-scope-observations.json에 남겼으며 전체 의미를 맞추기 위해 core나 baseline을 바꾸지 않았다.

독립 그래프 검사는 관리 링크 모듈을 import하지 않고 round-2 원본 JSON의 candidate_ids/candidate_slots 및 복수·단수 hard profile 선언을 재구성했다. 원본 source와 report inputs 96개 파일의 바이트 해시도 비교했다. 노출 후보 16개의 명시 연결과 48개의 정상 미연결, 관련 profile 30개 역방향 및 전체 incoming/outgoing이 일치했다. 리넨 후보의 현재 조회는 path_count=0으로 정상 성공했다.

연결 후보 mg_collage_edges와 profile mg_collage_edges_relation의 역조회는 동일한 candidate → bundle → profile 경로를 반환했다. meaning_support=not_inferred, review=unreviewed, profile_activation=independent_request_evidence_only를 유지한다. 이 경로는 전체 bundle component/relation 충족이나 필수 profile 활성화를 증명하지 않는다. 모든 optional 후보·bundle·visual concept은 비채택이고 effective_visual_contract_sha256=null이다.

손상 검사는 round-2 scratch의 복사 보고서에만 했다. links.json에 한 바이트 줄바꿈을 추가하면 파싱된 JSON은 같지만 `report_invalid: report member checksum mismatch: links.json`으로 거부한다. 다른 scratch root를 지정한 정상 보고서 조회도 `report_not_current: report authority/root differs from requested source`로 거부했다. 최종 확인에서 정상 report, 동결 입력, sealed member 해시는 여전히 동일했다.

구리의 둥근 볼륨과 리넨의 평평한 층, 사용 흔적과 건조한 직물 결은 하나의 조용한 정물 방향을 만든다. 창가라는 익숙한 배치는 결점이 아니며 creativity=1의 절제된 선택에 맞는다. PARTIAL의 핵심은 soft window reflection이 구리 곡면에서 리넨의 윗 접힘에도 이어진다는 한 문장이 광학적 소유와 매체를 명확히 구분하지 않는다는 점이다. 금속에 비친 창의 영상, 창에서 천으로 오는 확산광, 금속에서 천으로 되비친 빛 중 무엇이 연결되는지 다의적이다. 잘 생성되면 자연스러운 광량 관계로 읽힐 수 있지만, 천에 금속 같은 반사 영상이나 광택을 만들 수도 있어 이 문구만으로 사진적 물리의 명료성을 PASS로 평가하지 않았다. 아침 시간과 주전자의 기능 형태, 실제 직물 결 및 재질별 광택의 픽셀 생존도 확인하지 않았다.

위 PARTIAL은 문장을 바꾸거나 더 기발한 장치를 추가하라는 필수 요구가 아니다. 기술 audit 통과, 작성된 텍스트의 시각적 명료성, 실제 이미지의 물리·재질·구도, 인간의 선호를 각각 구분한 판단이다.

최종 영어 프롬프트는 처음 동결한 116단어와 바이트가 같다. SHA-256은 `a65bebbd01c69cf6be67c2550f4f71d6cb0e7f4100d8efd9b733c7151fbf7b4e`이다.

An object-only still-life photograph of an old copper kettle beside a length of linen that lies folded, lit by natural light in the early morning. Both rest on a pale stone windowsill. The kettle's curved flank carries small rubbed patches and darkened seams; the linen's stacked folds reveal a coarse, dry weave. A soft window reflection runs along the copper curve and falls across the upper fold, making the metal's rounded volume answer the fabric's flat layers. The kettle holds the visual center, with a small interval of stone separating it from the linen. Cool, quiet shadows remain readable against a plain, dim interior background, while the warm copper and off-white cloth retain their natural colors.

상세 결과·절대 경로·파일 SHA-256은 QA-RESULT.json에, 실행 증거는 각 *-command.json과 *-stdout.log/*-stderr.log에 저장했다.
