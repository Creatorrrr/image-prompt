arm-1 결과는 **픽셀 FAIL**입니다. 후보 조합과 정확한 런타임 audit은 PASS이고, built-in `image_gen.imagegen` 실제 호출 1회로 첫 이미지를 생성·보존했습니다. 재생성은 하지 않았습니다. 사용자 수용은 대기 상태입니다.

seed 2389700930으로 독립 작성한 8개 장면 중 index 1을 선택했습니다. 컨셉은 새 시민도서관의 건축 투어 시작 직전, 현대 구조적 테일러링을 입은 성인 착용자의 정면에 가까운 휴지 순간입니다. 참조는 보이는 얼굴·머리 외관에만 쓰며 신원·민족·성격·체형·실제 나이를 추론하지 않았습니다.

pre-core는 후보 조회 전에 고정했고 9개 feature category 검증이 경고 없이 PASS했습니다. 고정 원문 envelope 및 원 core 파일은 유지했습니다. semantic pack은 정확히 1개이며 실제 provenance도 semantic입니다. 데이터 freeze의 8개 runtime 파일 해시를 다시 확인했습니다.

노출·채택된 새 slot은 `clt_ct036_v1`(sweetheart), `clt_ct109_v2`(중앙 pendant), `clt_ct116_v1`(bail/chain passage)의 3개입니다. 대응 visual concept 3개도 명시적으로 opt-in해 5개 native gates를 활성화했습니다. 새 clothing bundle은 0개 노출됐습니다. princess seam, gigot sleeve, welt pocket, piping, inverted box pleat, Derby의 별도 새 후보는 이 한 팩에 노출되지 않았습니다. 이 용어들은 후보를 강제 주입하지 않고 독립 baseline의 사전 기준으로 평가했습니다.

| 사전 키워드 | 원본 픽셀 결과 |
| --- | --- |
| princess seam | PASS |
| sweetheart neckline | PASS |
| gigot sleeve | PASS |
| welt pocket | PASS |
| piping | PARTIAL: 밝은 테두리의 둥근 코드 단면이 확정되지 않음 |
| inverted box pleat | PASS |
| pendant bail | PARTIAL: 작은 연결부에서 열린 bail 및 체인 관통 구조를 확정할 수 없음 |
| Derby | PASS |

`partial_is_fail`에 따라 전체 테스트는 FAIL입니다. 프로필 hard gates는 3 PASS / 2 FAIL, embodiment gates는 3 PASS / 2 FAIL입니다. 두 embodiment 실패는 중요한 jewelry contact와 visibility가 불확정하다는 뜻이며 신체 변형을 진단한 것이 아닙니다. render review audit의 `schema_failures`는 빈 배열이고, qualification은 `failed_technical_hard_gates`입니다. 원본에서 관심 부위만 자른 분석 crop을 사용했으며 resize/sharpening 및 원본 변경은 하지 않았습니다.

- 실제 보존 이미지: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/clothing-terminology-20261001/qualification/arm-1/generated_image-1.png` (1024×1536)
- 이미지 SHA256: `d7ee8deeccb03d6c19499cd5c97cc865bf585af154c5ee9ec8ed88b8e955dc52`
- 최종 prompt SHA256: `b335c8ff356b32ea2a794a9498ed647c043ae45b5457528cdac158defb49a498`
- negative SHA256: `e07b39f8a2f7fe22f63e52888e7f910466604e887c062466ef8309d2a80a375b`
- runtime prompt SHA256: `f2ca88b4a05af75a679772a72cb3cfbad6e118b5fc2e1f9271ed19e36830d25d`
- composed 파일 SHA256: `2844ad3fa5a028669cd28e46d0a2e75b8c2c0cfc9ef468e1715c221707c24352`
- pack 파일 SHA256: `ce30ef78f36a2a89b80040149b70eaa7449dbfce9fd5c14bb3d4bcf7c7d74a60`
- core 파일 SHA256: `3587926470ee3e0a69970282b786cdc80c6d3f643566d0a5309a380969f6b039`
- normalized canonical core SHA256: `848f627aa50bd40815279b461113a793eb3a91348e0948490002e9984545fc50`
- canonical intent lock SHA256: `74821341b4549e97341fd6b4ebfbafe751340283cfba78b53ed68761c907b18e`
- run ID: `5091c6927cf3de1a`

세부 evidence는 `pixel_review.json`, `render_review_audit.json`, `exposure_adoption.json`, `artifact_hashes.json`에, 실제 attempt는 `image_runs.ndjson`과 `run_manifest.json`에 보존했습니다. source 데이터/코드의 공통 변경이나 다른 arm 자료 접근은 하지 않았습니다.
