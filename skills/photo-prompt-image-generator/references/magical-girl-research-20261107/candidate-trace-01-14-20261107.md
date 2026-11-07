# 마법소녀 후보 01–14절 추적표

원문 대조 원장 source-reconciliation.json의 기존 행·근거 상태를 기계적으로 연결했다. Diagnostic 243개는 근거·원문·검토 상태용이며 바인딩이 없다. 양성 선택 후보 183개는 관찰 가능한 선택적 시각 표현으로만 작성했고 181개 고유 행에 직접 연결했다. 각 표현은 원문 단어의 모든 변형, 장르 전체 또는 외부 근거의 검증 범위를 대변하지 않는다.

의상·소품·관계의 기재된 요소가 가려지면 픽셀 판정 불가다. 원문에 제시된 서사·이전 사건·초능력·재질 성분·연령을 이미지에서 사실로 추론하지 않는다. 기존 후보의 의미·조건·효과·바인딩은 각 진단 레코드의 원장 포인터에 보존되고 기존 연구의 미검증·미완료 상태가 그대로 유지된다. 생성된 양성 후보의 픽셀 검증은 아직 수행되지 않았다.

실제 검색에는 manifest 통합과 대응하는 전체 후보별 retrieval view, 검색 인덱스·임베딩 재생성 및 런타임 검증이 추가로 필요하다. Diagnostic은 양성 뷰를 만들거나 자동 선택하지 않는다.

| 원문 행 | 표제 | 진단 CID | 연결된 양성 CID (슬롯) |
|---|---|---|---|
| MG-01-001 | 마법소녀 | `cand_61c616eda6ce7b912d6a635f462f3f83` | 없음 — 원문·조건만 기록 |
| MG-01-002 | 마조코·마녀소녀 | `cand_37a31a563c8a0dea33943d1cc856940a` | 없음 — 원문·조건만 기록 |
| MG-01-003 | 샐리형 | `cand_1148b19f8a82c583923f7b442c09ed4d` | 없음 — 원문·조건만 기록 |
| MG-01-004 | 아코형 | `cand_8e181c1f17a878b78fa653da4af23022` | 없음 — 원문·조건만 기록 |
| MG-01-005 | 변신 히로인 | `cand_74704e42dfbf7f4f7696a80013145773` | 없음 — 원문·조건만 기록 |
| MG-01-006 | 일상 마법형 | `cand_37fb3f9a9369fec3ccbb1f771ca612e3` | 없음 — 원문·조건만 기록 |
| MG-01-007 | 마법 아이돌형 | `cand_c7b5b219f77cd3c35227bb4f3385d050` | 없음 — 원문·조건만 기록 |
| MG-01-008 | 마법 전사형 | `cand_5c6a8d57ae16a4740c7fc194aeadc600` | 없음 — 원문·조건만 기록 |
| MG-01-009 | 팀형 마법소녀 | `cand_e89f3bc5a17328607774c96d683c9d03` | 없음 — 원문·조건만 기록 |
| MG-01-010 | 견습 마녀형 | `cand_6cbe6c4204fcb9dc25772e8fcee2de60` | 없음 — 원문·조건만 기록 |
| MG-01-011 | 성인 마법소녀·마법 히로인 | `cand_28d52ec227196cd7c00cdbcb956d766e` | 없음 — 원문·조건만 기록 |
| MG-01-012 | 마법소년 | `cand_69ed8a1b12499db06d6c1b6759860cc8` | 없음 — 원문·조건만 기록 |
| MG-01-013 | 젠더벤딩·성별 전환 | `cand_8a17810979d5a6d925d7a8b83217770c` | 없음 — 원문·조건만 기록 |
| MG-01-014 | 다크 마법소녀 | `cand_0f658f550915c09c8602cda6217d7348` | 없음 — 원문·조건만 기록 |
| MG-01-015 | 장르 해체·전복 | `cand_81cf1224095ec9f9bc4d05b662a83a30` | 없음 — 원문·조건만 기록 |
| MG-01-016 | 메타·패러디 마법소녀 | `cand_bc6266ea930ba0d42029d9460f7f1351` | 없음 — 원문·조건만 기록 |
| MG-02-001 | 비밀 정체 | `cand_1a54d4f491ec1dee4433749e6c7b4891` | 없음 — 원문·조건만 기록 |
| MG-02-002 | 이중생활 | `cand_fef1037edac8823707dfe21873656d8b` | 없음 — 원문·조건만 기록 |
| MG-02-003 | 선택받은 자 | `cand_ba4546586caf69c0349ad030c2587081` | 없음 — 원문·조건만 기록 |
| MG-02-004 | 마법의 계승 | `cand_897c47d8741398089e7c696dbaa4b23f` | 없음 — 원문·조건만 기록 |
| MG-02-005 | 계약 | `cand_049dd53a915412bb4c45462f3a65f980` | 없음 — 원문·조건만 기록 |
| MG-02-006 | 소원과 대가 | `cand_5d270c36c25f6b9153f3904727fe15d3` | 없음 — 원문·조건만 기록 |
| MG-02-007 | 각성 | `cand_54bd4d92d451798a13aaf5a1dde0a138` | 없음 — 원문·조건만 기록 |
| MG-02-008 | 마력 | `cand_0ec96912a53b8217e4c97a6b5572ad62` | 없음 — 원문·조건만 기록 |
| MG-02-009 | 속성 | `cand_52ec4a87c101a998f7d693b46f4c454c` | 없음 — 원문·조건만 기록 |
| MG-02-010 | 마력원·코어 | `cand_2c8fd95d0dcaafeb42c638eb9abc8042` | 없음 — 원문·조건만 기록 |
| MG-02-011 | 마력 고갈 | `cand_6ac2f45e7bce94f0b04219eeceb233ea` | 없음 — 원문·조건만 기록 |
| MG-02-012 | 활동 시간 제한 | `cand_4c288f68b8a443413f0b81feb1189a96` | 없음 — 원문·조건만 기록 |
| MG-02-013 | 봉인·해방 | `cand_51a68e350be390fc01fdbb4a751c34d0` | 없음 — 원문·조건만 기록 |
| MG-02-014 | 정화·치유 | `cand_d2d03b0e1a9b34cdc0c283de777106a9` | 없음 — 원문·조건만 기록 |
| MG-02-015 | 결계 | `cand_a7dc8901173fc4bfff77535ece25618d` | 없음 — 원문·조건만 기록 |
| MG-02-016 | 필살기·결정기 | `cand_968c10ba5b6f1c4555bb029999e342f5` | 없음 — 원문·조건만 기록 |
| MG-02-017 | 합체기·연계기 | `cand_cf13037e5a4de4897fe9516f7015893f` | 없음 — 원문·조건만 기록 |
| MG-02-018 | 상위 폼·강화 형태 | `cand_743021f677e71e15a2e6eb943402be1d` | 없음 — 원문·조건만 기록 |
| MG-02-019 | 회차별 적 | `cand_c2ad9386e70bae6df6a256474136a777` | 없음 — 원문·조건만 기록 |
| MG-02-020 | 라이벌·전향 동료 | `cand_01b7892bad505c4fb1d0d31a97536f4a` | 없음 — 원문·조건만 기록 |
| MG-02-021 | 타임루프 | `cand_b0194f2af81a7c1a6ef9abca2c3bbd21` | 없음 — 원문·조건만 기록 |
| MG-02-022 | 희생·구원 | `cand_af42629d353735ba395efda34cc9ab5f` | 없음 — 원문·조건만 기록 |
| MG-03-001 | 변신 | `cand_323652d2a3f93e81e3da7c6cfb9f3698` | 없음 — 원문·조건만 기록 |
| MG-03-002 | 변신 시퀀스 | `cand_4318a7fea777f8f1b9d8a95486d0d978` | 없음 — 원문·조건만 기록 |
| MG-03-003 | 변신 뱅크 | `cand_baee90bdc52cddb84c191fa20148ebd9` | 없음 — 원문·조건만 기록 |
| MG-03-004 | 변신 주문·구호 | `cand_3ac71b639ebabfdd2891fa3d1f75c16b` | 없음 — 원문·조건만 기록 |
| MG-03-005 | 나노리 | `cand_6a009ea5f2dd9186fe68dcc67a9470e8` | 없음 — 원문·조건만 기록 |
| MG-03-006 | 결정 대사 | `cand_be4e9fe62213f98db3d3ffefcfec3f8b` | 없음 — 원문·조건만 기록 |
| MG-03-007 | 추상 변신 공간 | `cand_5754e6564b417b24dd25842067f6099d` | `cand_07d56b2a54e5af5c60c60421255d4779` (background_element) |
| MG-03-008 | 실루엣 변신 | `cand_f7dc2ef84d3030b73ee13249b9d05b4e` | `cand_a487dc3f1e96b50ff17a12a09ab10f2b` (transformation_stage) |
| MG-03-009 | 빛의 리본 | `cand_517222625d1dbc77f5b57e023cb7ac80` | `cand_2265384bee4dc976674cc7cd7e8cf204` (light_shape), `cand_6f8642dac4cf5bfedd5bc0885c162ed2` (transformation_stage) |
| MG-03-010 | 입자 실체화 | `cand_d44351ba1ff76308409ba66b97a95c23` | `cand_8803cccf55410776f6a7a20c3975ae85` (transformation_stage) |
| MG-03-011 | 파츠 생성·장착 | `cand_1dd675794ffe92f3a544af99b640456f` | `cand_55ba0a2db06e03f386990a2806a128f2` (transformation_stage) |
| MG-03-012 | 디테일 인서트 | `cand_08a008b46044b4a3f63e698bed7da46f` | 없음 — 원문·조건만 기록 |
| MG-03-013 | 변신 완료 포즈 | `cand_9353890d726d7de8649409aaae85a1d0` | `cand_b6cc3817bc81a2f121ca24bbcc1dad7a` (body_pose) |
| MG-03-014 | 변신 해제 | `cand_8ff992482d2fe196be5872b18ddcf1b9` | 없음 — 원문·조건만 기록 |
| MG-03-015 | 변신 중단·불완전 변신 | `cand_7465f333f6fa534bfe85336ad21e7dc6` | 없음 — 원문·조건만 기록 |
| MG-04-001 | 세일러 전사풍 | `cand_277ccd1778aa99a132f47778c1a05047` | `cand_a41e8676c2d2a1c0ba49e141866be4fa` (wardrobe_style) |
| MG-04-002 | 동화·공주풍 | `cand_e5ef970adaf551b61da57098167342ef` | `cand_6187b94e67a4a95db588ea0f96388df9` (wardrobe_style) |
| MG-04-003 | 아이돌·무대복풍 | `cand_e642710dcb6c7c5656a98fc939533998` | `cand_fdc277cea4919de328f0a8c50bf50df3` (wardrobe_style) |
| MG-04-004 | 마녀풍 | `cand_309bedcb613553b35476559052595a01` | `cand_4f109e10032791e82faf71d33d3584ec` (wardrobe_style) |
| MG-04-005 | 스위트·로리타풍 | `cand_17727a0ec459d8084726b9d7a31d9192` | `cand_a01714328997c6c36356729698d29923` (wardrobe_style) |
| MG-04-006 | 고딕풍 | `cand_665d65e2955624cae44589d19b16cc57` | `cand_2d5aa7a4a8ba17c9b23968a411337621` (wardrobe_style) |
| MG-04-007 | 기사·갑주형 | `cand_5484b291370dc859fe1fa1a961df1310` | `cand_927bd4f6133e14792b605d5e1184f14a` (wardrobe_style) |
| MG-04-008 | 사이버·기계형 | `cand_e7421cad81cbe803b51ca6485c103685` | `cand_effbac1efd9950224f8af07b280cab54` (garment_detail) |
| MG-04-009 | 일상복 결합형 | `cand_ea8e87d3d5ef9d4974bb4620cd2fcbee` | `cand_b85e64e496e4560c5e9c00db4529ad85` (wardrobe_style) |
| MG-04-010 | 피트 앤 플레어 | `cand_39a5a20e7abba597112ee59e5819626a` | `cand_c115ab4b0a5a847ebd0b9f9dc709a86d` (silhouette_proportion) |
| MG-04-011 | A라인 | `cand_3c7ef6b5187ce21added4d0fcca26491` | `cand_e9dae66c61bd2ad37fba07a5a6332ccd` (silhouette_proportion) |
| MG-04-012 | 벨·컵케이크 실루엣 | `cand_24801d283c533cba9c5a019bc7fbf4aa` | `cand_882756b780101e2c5956aed7c2f5d038` (silhouette_proportion) |
| MG-04-013 | 비대칭 디자인 | `cand_7fa6d7466984392ffad1604dc5caa83c` | `cand_6807f6d0fb8e467465d7da4f1eaa52a4` (garment_detail) |
| MG-05-001 | 트윈테일 | `cand_cf97879e5a5294ed15a48356841ba054` | `cand_351f14aa3e194e790434914802045367` (hair_style) |
| MG-05-002 | 사이드 포니테일 | `cand_0e2a39bda43a6f7cc128ee978eeb25b2` | `cand_a02924adbc44249c7ec646be2252639e` (hair_style) |
| MG-05-003 | 오당고·더블 번 | `cand_efc5f9592c309b1d6070afb4c3774ee9` | `cand_05a7372d06d0e1992be1a0667025b13c` (hair_style), `cand_bf7713320390bf5734e546f5f341a940` (hair_style) |
| MG-05-004 | 드릴 컬 | `cand_47228a646258271614e3b4745237ac31` | `cand_73b0120e8eb18d2a100b9d6aa89b99ad` (hair_style) |
| MG-05-005 | 히메컷 | `cand_959caa7c3786174fefbc61eb9d92dfa5` | `cand_79cf9fd8caf5fa348ed85d8165573e96` (hair_style) |
| MG-05-006 | 아호게 | `cand_abc81e2181694ec8050a4eabe4b7e36e` | `cand_88495b86bea355b44e23311391e01355` (hair_style) |
| MG-05-007 | 그라데이션·투톤 헤어 | `cand_83c3eaa93f8b9610029a5ac47c0d3dae` | `cand_5c76604aa9c94b2153e86528a75ae53c` (hair_color) |
| MG-05-008 | 헤어 보 | `cand_e1fce90793d952622ecfdcc47d743478` | `cand_632253c30cdc53114520a50635162642` (wearable_accessory) |
| MG-05-009 | 티아라 | `cand_94e74d16f2f3cbbae2c77a68b72ded5c` | `cand_14d4ac9bb57e6790858dcc4bbf748c4e` (wearable_accessory) |
| MG-05-010 | 서클릿 | `cand_cd6eac1f2cd4b26d9473aebfc24f22d8` | `cand_93d77ae611cbf7f2ee7b21af5362198f` (wearable_accessory) |
| MG-05-011 | 헤드드레스 | `cand_619c2b6bff6a9e05bed8d32b57e0a76f` | `cand_ca8cc8dff4dab5c873816cdda5828bf5` (wearable_accessory) |
| MG-05-012 | 보닛 | `cand_a98fcfcd598a425caa08f4c90f9866a4` | `cand_65bc3c3519a93040fa1db5f0df39d98f` (wearable_accessory) |
| MG-05-013 | 위치 햇·미니햇 | `cand_05173c0f937d234ea25186e2bc6e7b5e` | `cand_c46a34556b695526a1e7bba8d3f98b6b` (wearable_accessory) |
| MG-05-014 | 광륜 | `cand_0a47e797292a69ea83f00249cc912f16` | `cand_060960933c75a600816f540cd58a3052` (light_shape) |
| MG-05-015 | 이마 보석·페이스 마크 | `cand_9f3c8ea487de8bb09494bb33d52ed0b9` | `cand_e7559685b8f6b7219224fd8895d9cc54` (body_marking) |
| MG-05-016 | 별·하트 캐치라이트 | `cand_595b276b3b8da5f26a37e601cc557958` | `cand_cd40982e0708fee6842fea3e9c58db9b` (eye_detail), `cand_40a7294c9ed3bb7fa8c1fa6595dc75cc` (eye_detail) |
| MG-05-017 | 오드아이 | `cand_73229e36bdc9d0e424bf639274f880ba` | `cand_ff8e745a419784b6c593d9b96033886f` (eye_detail) |
| MG-05-018 | 글리터 메이크업 | `cand_b870eb35161b55574cbe7b685a58cb1f` | `cand_152f96f8689bc128a5e7cd6a8fb7ca3c` (eye_detail) |
| MG-05-019 | 그라데이션 아이메이크업 | `cand_bdc99b2b92a8f04706cb2a03d8574241` | `cand_3a8e77a30767d925d6ceb74c0306abf6` (eye_detail) |
| MG-05-020 | 눈물 자국·무너진 화장 | `cand_66f5fe59d7d33c8f0a227804e98f82ad` | `cand_619c75412c01ba2eaf86e31b688d3306` (makeup_wear_state) |
| MG-06-001 | 보디스 | `cand_8b6289eb1c0f3762c051d7502269df6b` | `cand_181d844ae51a9c1bbd1a9bbf60560e2f` (garment_detail) |
| MG-06-002 | 요크 | `cand_6f5b9ffd882c379c305f47367a8a6b99` | `cand_181d844ae51a9c1bbd1a9bbf60560e2f` (garment_detail) |
| MG-06-003 | 세일러 칼라 | `cand_fe86da276b21e09c32a95334218a8914` | `cand_b2e828b16555118cf34e822b6d45708b` (garment_detail) |
| MG-06-004 | 피터팬 칼라 | `cand_b00ffe7f7e5873fbdf5fb39df0486c53` | `cand_f421baecbfe5a06ae07b6c4f74627d66` (garment_detail) |
| MG-06-005 | 스탠드 칼라 | `cand_261998b7291728a37f96f3c317e14757` | `cand_1ea205fd3b7482c343c97975a34c3f32` (garment_detail) |
| MG-06-006 | 초커 | `cand_8253ae84085cd70042f9ab281bbfffca` | `cand_414ab4e03b8646822b9c994cb2289297` (wearable_accessory) |
| MG-06-007 | 가슴 리본 | `cand_658b01cfaca9dfb2ab39dc0357186fe0` | `cand_8602406d1879788d9c7f7edacdf98edb` (garment_detail) |
| MG-06-008 | 브로치 | `cand_02c56410e5de418e380c77b30ba18bda` | `cand_8602406d1879788d9c7f7edacdf98edb` (garment_detail) |
| MG-06-009 | 스위트하트 네크라인 | `cand_e8fee47e30fc3d611e67c7688c9a27ea` | `cand_6ac0dee2ee1acd07ba4cdc98fd8e6010` (garment_detail) |
| MG-06-010 | 오프숄더·스트랩리스 | `cand_be3b00182a449357f13b79bd3de7e42b` | `cand_14d53f2ecc7f954acdf618a429126b49` (garment_detail), `cand_2978cac27aa329e75def439fc5fa4780` (garment_detail) |
| MG-06-011 | 키홀 컷아웃 | `cand_ec980691a7520c1c3560ad0c6d228b48` | `cand_6f38ddcf80da3fdf738bae9f5f2b44bc` (garment_detail) |
| MG-06-012 | 코르셋 | `cand_779d4e521c1659dba3835df90aaec3a2` | `cand_12822d1cb105b6aae64fedd4cd6c5f05` (garment_detail) |
| MG-06-013 | 뷔스티에 | `cand_874e2c4ed4db01bf44745317a7dd9b1c` | `cand_83a840f7885ca420a6b7855110101da1` (wardrobe_style) |
| MG-06-014 | 바스크 보디스 | `cand_4c6d9cc5ac32b491c5c08c3b53ca7366` | `cand_aea0d2cc24c6e6f9fb1144b46b830763` (garment_detail) |
| MG-06-015 | 페플럼 | `cand_495acbc2dbcc23a22794936c658e1e56` | `cand_403a34f285ae292426cbfe4ea9988ddb` (garment_detail) |
| MG-06-016 | 새시·허리띠 | `cand_17d9fd8da8ce09e0e4db0239dfb2cefa` | `cand_4b59d5b2237756b78bd3b292d0e0a377` (wearable_accessory) |
| MG-06-017 | 허리 뒤 리본 | `cand_07b4d026c56ea127676c54cd2d3189da` | `cand_aafec32f8dbfdc531aed66b6b4355cc8` (garment_detail) |
| MG-06-018 | 레오타드 | `cand_55dd03337d8e4beba58ff12e9e4587e1` | `cand_442717cfbcee9afaf142ed3c88759f3b` (wardrobe_style) |
| MG-06-019 | 보디슈트·캣슈트 | `cand_737b4c8fb16c0a4c3a4c4063b0afb37a` | `cand_8b02eb8cb1ddab03675f922819e0c083` (wardrobe_style) |
| MG-07-001 | 퍼프 슬리브 | `cand_069b618a5fa05472af35117722852827` | `cand_86088583e99fabce45a946e5fe101bca` (garment_detail) |
| MG-07-002 | 벨 슬리브 | `cand_72396182d3fbbd85c15977073eaaa2d1` | `cand_8e5864bc695081b43a09344d200e00a0` (garment_detail) |
| MG-07-003 | 비숍 슬리브 | `cand_e919b5e0a5674f8ff8c2f2f6ee0fe6c3` | `cand_96a31ad55469b191a3ef71dc9a202cc6` (garment_detail) |
| MG-07-004 | 분리형 소매 | `cand_7ec20e90778b3aca58fe1a2c686e34cd` | `cand_32aeb1c7163006bfdde09204cd657668` (garment_detail) |
| MG-07-005 | 커프스 | `cand_d3f4a40ea9a6254f052d07e3d48d6bb9` | `cand_74f639d5e620157154a3d971f96f2b1e` (wearable_accessory) |
| MG-07-006 | 리스트 커프 | `cand_4ac115e55bf113903457e2f69ca0be8d` | `cand_74f639d5e620157154a3d971f96f2b1e` (wearable_accessory) |
| MG-07-007 | 오페라 글러브 | `cand_0f1f015efa436290d90f4aa992849cff` | `cand_1755aba35ab30c6ce71aefe7b5ea9b2b` (wearable_accessory) |
| MG-07-008 | 핑거리스 글러브 | `cand_e6378f07d5fb3dcfb1b67dd4bb29a3df` | `cand_5f573215937cb268efbb224c6a89d50f` (wearable_accessory) |
| MG-07-009 | 건틀릿 | `cand_540e93e71aa7ab7213eec74934d53d60` | `cand_8e075cb465fcea5d5681df1034112316` (wearable_accessory) |
| MG-07-010 | 에폴레트 | `cand_6c62cc41440a5cf0e82771cc7fb7d9ce` | `cand_0172ff14180e00321bff1f3c41e85ca1` (garment_detail) |
| MG-07-011 | 폴드런 | `cand_6800718a01072ae5128f2f3022c47a00` | `cand_7cefa87f8922137309def78677a29c3f` (garment_detail) |
| MG-07-012 | 케이프·케이플릿 | `cand_914f7009ebd38b3710721d89b3e5e9ae` | `cand_49bec3e28bd38ccf1ac1f4acbd70bccd` (wardrobe_layering) |
| MG-07-013 | 볼레로 | `cand_a2b8f698a5ced6933c18d9e95fd19ea0` | `cand_9eb21c6f56030f41af8be12fe8362c14` (wardrobe_layering) |
| MG-08-001 | 플레어 스커트 | `cand_797ddd19e2c59e18445e84b8ece8c358` | `cand_68dcb1ce208a05de68d4d4fca11a5068` (wardrobe_style) |
| MG-08-002 | 서클 스커트 | `cand_07978304883cc233058050306a6840a6` | 없음 — 원문·조건만 기록 |
| MG-08-003 | 플리츠 스커트 | `cand_037996aeeaf47fec32daf816c6f866de` | `cand_02d1fda7581db93b73258c08eea24c7e` (garment_detail) |
| MG-08-004 | 박스 플리츠 | `cand_923c64453d3b6f4756f7b112b0309151` | `cand_0393ea06330f88fecf80d8e2fc89fc0d` (garment_detail) |
| MG-08-005 | 티어드 스커트 | `cand_cf5429ba53b1cec15045ee2d0d172f2d` | `cand_0c6397ed444f5618b83c7b247e71983a` (garment_detail) |
| MG-08-006 | 페탈 스커트 | `cand_ee70bd778a0922bbdee379dfade8067e` | `cand_b4ef031124bd588f2b935328a0e5f5c9` (garment_detail) |
| MG-08-007 | 벌룬 스커트 | `cand_3359272d5538f099ee3c120112229f69` | `cand_a865622dde18a88334aa157a528357c6` (garment_detail) |
| MG-08-008 | 비대칭·하이로 밑단 | `cand_444211da3217de39984138e42fe040fa` | `cand_76798b79b1e3da84a1586d483e45dad4` (garment_detail) |
| MG-08-009 | 오버스커트 | `cand_fe2935ff0dbe7a42302a4108e9d7101e` | `cand_2c55dcf8b2b19c50f8e792b15765c25e` (wardrobe_layering) |
| MG-08-010 | 페티코트 | `cand_ede5e7c16259a19df1fd34092600597a` | `cand_2c55dcf8b2b19c50f8e792b15765c25e` (wardrobe_layering), `cand_5f7f64741ad213bb5a254cb96424da55` (wardrobe_layering) |
| MG-08-011 | 파니에 | `cand_1796c515200afb052bea213878dc0c25` | `cand_2066a502cf4a69dc08141eaae9f6affd` (garment_detail) |
| MG-08-012 | 케이지 크리놀린 | `cand_3f3987169eff5fe64688cec6303e12c3` | `cand_15ed7a150b02a14de3e146013e30a7cd` (wardrobe_layering) |
| MG-08-013 | 버슬 | `cand_20ff5dbf4c5f45e898ee0596067c7967` | `cand_e7da74abdb95aefe36d1ba727a48700a` (silhouette_proportion) |
| MG-08-014 | 트레인 | `cand_b3112af8ef54acc43883856f4aaab9cd` | `cand_90b5baa5820027d17aa13d7458d8933c` (garment_detail) |
| MG-08-015 | 블루머·드로어즈 | `cand_4c75c3e3307dab8c09433f1e2d02f631` | `cand_3ab459b9294d1612edee871e79cd9349` (wardrobe_layering) |
| MG-08-016 | 커버 쇼츠·스코트 | `cand_3f66d2cb0444237487cd9f49baf6e700` | `cand_d2985797e0e0627b529b0f006d97a0dc` (wardrobe_layering), `cand_01f7ea547cb8dacdfb848669d8474ee5` (wardrobe_layering) |
| MG-09-001 | 니삭스 | `cand_40b3a56ee4be2a44c8c8fa6d38394de6` | `cand_acfada8df9f0f5fc60896a58bcf21b0e` (wearable_accessory) |
| MG-09-002 | 오버니 삭스 | `cand_fd756b409bc7ec8e5db5e8abe3fdecaa` | `cand_dc490a71fca06d0254a49e36d35b8a70` (garment_detail) |
| MG-09-003 | 사이하이 스타킹 | `cand_22b39c9afa8c7322f04a0dc336c433d0` | `cand_2e587d30fbd42bb363fa4e30a6ab18c2` (garment_detail) |
| MG-09-004 | 타이츠·팬티스타킹 | `cand_68a366398d9ba707b8934ef9dd34e46d` | `cand_49d81be3677e6247d1e3dc89e6544d1e` (wearable_accessory) |
| MG-09-005 | 홀드업·스테이업 | `cand_b99697877a45d3a20c4f992b48aa9dc8` | `cand_d7cf94a3e9e4182aad3525bae3a505e5` (wearable_accessory) |
| MG-09-006 | 피시넷 | `cand_f6173dbeab8b61559ef9fe8f0501720d` | `cand_8105c226089a93804ef20c479a5796ee` (surface_material) |
| MG-09-007 | 허벅지 가터 | `cand_2e8cb70b5a3da70f35bf3edbd8513530` | `cand_57b898efe7e000139fc9659a322d1407` (wearable_accessory) |
| MG-09-008 | 가터벨트 | `cand_a6bbdec9ccfc756250ac9dbbb976a084` | `cand_1e39ca94ee3dca48f4157fe83cf82cdc` (wardrobe_layering) |
| MG-09-009 | 앵클·니하이·사이하이 부츠 | `cand_88f05a7cb5ca8ea7921c068fa72a79c3` | `cand_7c881d0953b74c8d8f2e9bdf54532250` (footwear) |
| MG-09-010 | 메리제인 | `cand_fd885aa1517c94a7cacc232d799ff513` | `cand_2f2bea4e52d476580c9cdc0bfd9c94dd` (footwear) |
| MG-09-011 | 플랫폼 슈즈 | `cand_e754e0cebfdfc5cd216cdd5188dab694` | `cand_0d915cf2ecebe22fd71dda695e802e1a` (footwear) |
| MG-09-012 | 스틸레토·블록힐 | `cand_92f9384616c81426cea51fca5999d279` | `cand_296645424687e7b880b70955119df37a` (footwear) |
| MG-09-013 | 부츠 커버·게이터 | `cand_07aa98b3e336fcafb8c6facd3f11571d` | `cand_5429010232af40cd9c384ea1d909ae7b` (wearable_accessory) |
| MG-09-014 | 짝다리 의상 | `cand_992baa9a24b594029f5cac5e26b78d47` | `cand_7c881d0953b74c8d8f2e9bdf54532250` (footwear) |
| MG-10-001 | 프릴·러플 | `cand_66322b13e8d085812a936a413be7b535` | `cand_fd98f12b416efdf57143d80ceb638235` (garment_detail) |
| MG-10-002 | 플라운스 | `cand_38e935d9e5e498b3304ff136fa0e6fd7` | `cand_66e7f4107709419ef3be41a058cf6604` (garment_detail) |
| MG-10-003 | 레이스 | `cand_798b2cebe0a373ca3573751cb0fed113` | `cand_96d2800728329f000166e835eaa13d5b` (surface_material) |
| MG-10-004 | 리본·보 | `cand_565d00bfd04804738ff352e82ae1ba8a` | `cand_a54fda17ae0b929f9b970355d54439c5` (garment_detail) |
| MG-10-005 | 로제트 | `cand_b867f1104ae0aa7bc0f525bab0a12ae8` | `cand_6a02e727604f6f3c9753f38fbf201554` (garment_detail) |
| MG-10-006 | 스캘럽 가장자리 | `cand_35fc1199adb738ce69ee2e4cb2229f56` | `cand_a7388b91f42dca440394a29b5d324396` (garment_detail) |
| MG-10-007 | 파이핑 | `cand_a816f2eb4384520b677b57ba8bba2196` | `cand_04bf1925f2816a9422d7c49eef3b0f6f` (garment_detail) |
| MG-10-008 | 레이스업·레이싱 | `cand_c00ebf57e069daa5aecf5be5410e78eb` | `cand_fe844d60e18e8a506741fd4379e08d91` (garment_detail) |
| MG-10-009 | 보닝 | `cand_0ea2ccdf34fac5efeafbcb25f2c92f93` | 없음 — 원문·조건만 기록 |
| MG-10-010 | 자수·아플리케 | `cand_545f0369720c1588ca9fad12c80a04b2` | `cand_aa6607e709ff224e3e5d92e11b2c100f` (surface_pattern) |
| MG-10-011 | 튤 | `cand_03d46598e5e1e9ecf5679288010da25d` | `cand_58c4af090f90616823e5e7b61ade93b0` (surface_material) |
| MG-10-012 | 오간자 | `cand_95bdacd7d12e547ef74fdd5ea86ffdae` | `cand_676dd14312654c04663ac689f0b0cd5f` (surface_material) |
| MG-10-013 | 시폰 | `cand_fe15839e8d15c6c8cdf0c8abe3ca45e9` | `cand_91fadf5bbc2ad291d7c364b4345d92d1` (surface_material) |
| MG-10-014 | 새틴 | `cand_ce04250b97f9f1ad616b450790853ab4` | `cand_2ab08ab2e2ee8791f554a4122ced5a83` (surface_material) |
| MG-10-015 | 벨벳 | `cand_4aebf7d1a68a8a97f40011eb0285baa5` | `cand_2437dc9c2c4fa74db81272e06072cc5e` (surface_material) |
| MG-10-016 | 라메·메탈릭 직물 | `cand_c58a57d9308570d817d88caff79a18fb` | 없음 — 원문·조건만 기록 |
| MG-10-017 | 이리데슨트 | `cand_4d3878845c8083c9fce70c8eecdb4059` | `cand_454c538e702f87a1e5cd82e01b06e689` (surface_material) |
| MG-10-018 | 스팽글·라인스톤 | `cand_9163c5fa5027d19d19208e3a7101122b` | `cand_0ae05106c9e715c8b4c765bfb0a5a564` (surface_material) |
| MG-10-019 | 카보숑·패싯 커팅 | `cand_0a78352bc8d52ba7036984dbf1b78d23` | `cand_f9b61feab45641fbb2b141b8840ed10d` (garment_detail), `cand_d6c9c96567931ef4f6d88c76186e7221` (garment_detail) |
| MG-11-001 | 하트 | `cand_59a735731a3d649f836655b166e3bc52` | `cand_2d5340c89a2f6af6f2ac080aef2d4030` (garment_detail) |
| MG-11-002 | 별 | `cand_4b3489d95a21ac006ace31326b422711` | `cand_f58cf309dab66899be50149dc154da3f` (prop) |
| MG-11-003 | 초승달·태양 | `cand_b78229835ae5d617451151d9e462ebf5` | `cand_7f3e1a0abde6b8891bbea6e5f8940e76` (wearable_accessory) |
| MG-11-004 | 꽃·장미·꽃봉오리 | `cand_0f3cd96b72e49cf9f48f4c0e8a8d45f2` | `cand_d9816b788d2751e6ea1e2ec63b7aa12d` (garment_detail) |
| MG-11-005 | 나비 | `cand_be2c3fd3e32348f528c72cd0443f3ba5` | `cand_0d4a0d388a7470077d09c0b6791552c2` (wearable_accessory) |
| MG-11-006 | 날개·깃털 | `cand_be586e07f7642a19a259f218db20b266` | `cand_83fbf9218ec47d0bb23e9be3279aff92` (wearable_accessory) |
| MG-11-007 | 보석·결정 | `cand_fff271590eea537d6e60ab0dbc2da404` | `cand_5e0ef9a141e5883be6b62421988f8c94` (prop) |
| MG-11-008 | 열쇠·자물쇠 | `cand_e1fc26ca9ca75f8f50a054e4bb33027d` | `cand_015038e12630d54f2570cbc89bc611c4` (prop) |
| MG-11-009 | 시계·모래시계 | `cand_48870707d2248b239607e99e171c1f82` | `cand_0b4248112a185670971c034b898063d7` (prop) |
| MG-11-010 | 음표·악기 | `cand_0c4cf1706ff8597d97a6c79372bb05cd` | `cand_bf3e9a1f5b59da2e8d412cebe5cf1773` (garment_detail) |
| MG-11-011 | 트럼프 문양·타로 이미지 | `cand_fb26cdd47409fdd837ba09e93fd118fc` | `cand_3def0ea724ff5baa13883e14bcb19717` (surface_pattern) |
| MG-11-012 | 동물 모티프 | `cand_97a18bce294a1622718571a9d16bf2c0` | `cand_2de4b0fe8bfae4ffbb15fa0528e65f46` (wearable_accessory) |
| MG-11-013 | 시그니처 컬러 | `cand_ed1e76df826a2e8760ad7054f5726833` | 없음 — 원문·조건만 기록 |
| MG-11-014 | 반전 문양 | `cand_d24161a9f19c8c7681a9ab42a43a8454` | 없음 — 원문·조건만 기록 |
| MG-12-001 | 완드 | `cand_4b5ae11778c48afa74f5f2a8a10a655a` | `cand_803af52f62740248ce4ff2d146560a69` (prop) |
| MG-12-002 | 로드·스태프 | `cand_5eda868dc616b567d0bd701043b25487` | `cand_9b54a40456d2bea0ac5ac0febc02b3a7` (prop) |
| MG-12-003 | 셉터·홀 | `cand_6b3495accf7042e8572b783539b9ddd6` | `cand_e0c16b1e16a2d3b7bc0cd01b14b6e0be` (prop) |
| MG-12-004 | 변신 콤팩트 | `cand_cda7e4e51bb52ed524d88ca9f98187f6` | `cand_f7491e0b3ae885ca6d68352bfa96ad13` (prop) |
| MG-12-005 | 변신 브로치·펜던트 | `cand_511fc7c1a731a6514080bf5ff9d54433` | `cand_afb2a156e99097abf6c155a9efa6b257` (wearable_accessory) |
| MG-12-006 | 변신 펜·코스메틱 아이템 | `cand_9f92bea9b8ff0850a2658c1b1d1f0982` | `cand_e19db83e2241223aa1c3190c3097632f` (prop) |
| MG-12-007 | 링·팔찌·전자 장치 | `cand_00cc1d48bbde7a41cfa2e455fa9cf2b7` | `cand_dff91437a9a6384b48a4561853340f7f` (wearable_accessory) |
| MG-12-008 | 애뮬릿·부적 | `cand_3d3e086bb3a479420f633e228ae3a53a` | `cand_869d31d725ed88cd5dfc5164aa381649` (prop) |
| MG-12-009 | 마법 카드·덱 | `cand_9de1ba94b1bbda59117c806d8f452b49` | `cand_7fe70544f2be846d86fcc9d31cbdbba2` (prop) |
| MG-12-010 | 마법서·그리모어 | `cand_6db761282cf5b02b321d49249487bfff` | `cand_e521eec74597e02fa5abaf64322d8d55` (prop) |
| MG-12-011 | 마법궁·마법화살 | `cand_f4594abcba339b8e4e4f5df30058c58c` | `cand_44f1a71a7d4432d3a7c85966eb57750d` (prop) |
| MG-12-012 | 마법검·레이피어·창 | `cand_1a29e79107660d977cb6c1a59ed374ba` | `cand_0fabc34a1bf7dcaa30138bd73d1c3878` (prop) |
| MG-12-013 | 낫 | `cand_6b3cbb2063976942f5b082903103f936` | `cand_e0c3fdf1ae44771764a4825cb2452087` (prop) |
| MG-12-014 | 마법총·마력포 | `cand_177201884a5a2bf05fb04f0d2721a339` | `cand_4583891cb63da4a6d28d74b400b2e006` (prop) |
| MG-12-015 | 리본 무기·마법 사슬 | `cand_26c3be501665f009d64b3770d34aa1e5` | `cand_53447e14ac468ffa2c2f0de834fe32ce` (prop) |
| MG-12-016 | 마법 방패·배리어 | `cand_1fb32a5295732378ed1fca5edcfa03ce` | `cand_930d5de467c1554455b68b2df1fb642e` (prop), `cand_b682f243a842489290d474289badc2ab` (light_shape) |
| MG-12-017 | 마이크·악기형 무기 | `cand_baf690e312cff9d296f1431f75275ac0` | `cand_90927887279b129b8971672314e60f4d` (prop) |
| MG-12-018 | 빗자루 | `cand_89563aecbd5dd00c09e08050812ac3fc` | `cand_f66bca4d8ea4a102c82c1b53b11ef675` (prop) |
| MG-12-019 | 마스코트·사역마 | `cand_0a6d309db7400006fe5484fc42e6eee3` | `cand_0449b1a035c4d4a62b7e4f928926595e` (prop) |
| MG-13-1-001 | 키메 포즈 | `cand_ee41a81d6a1c3aab37d1ae33afc1d7c8` | 없음 — 원문·조건만 기록 |
| MG-13-1-002 | 지팡이 들어 올리기 | `cand_9d7c698d6883c94c00f725645df83dc7` | `cand_b3cc5396b54e47727897307f6e69a311` (body_pose) |
| MG-13-1-003 | 허리에 손 | `cand_366dfd728d2cfbd323e0058832b8b3b7` | `cand_c7b97229ce5821909981bdd1953052af` (hand_pose) |
| MG-13-1-004 | 콘트라포스토 | `cand_a12ac354cf14fe29d9feaedb42d714f7` | `cand_8001c3960e01b96e267dea37be4f3c7b` (body_pose) |
| MG-13-1-005 | 얼굴 주변 손동작 | `cand_86f475cf31867299b3005db401ed9e2a` | `cand_2548357c8da5e2c75ffab8d68c1b0379` (hand_pose) |
| MG-13-1-006 | V 사인·윙크 | `cand_e6e65b43156262bb869a010170adc529` | `cand_8bd14348b8166bad11ed7c467bbdf1de` (expression) |
| MG-13-1-007 | 핑거 하트·핸드 하트 | `cand_bce98e7099348e7d11f7ec4112b625e4` | `cand_e808066f1767552a7f363f5ca5fc8537` (hand_pose) |
| MG-13-1-008 | 어깨 너머 돌아보기 | `cand_6dd34296cadce53d24113d5738df0247` | `cand_57b6795992430780f1304aefa1e6673d` (body_pose) |
| MG-13-1-009 | 커트시 | `cand_dc65f7801c6657d7a4707dbb9b1ae9d2` | `cand_797d573120616409daa7242542b09a6c` (body_pose) |
| MG-13-1-010 | 회전 자세 | `cand_6a3b090b55479e4f696119cd582f162f` | 없음 — 원문·조건만 기록 |
| MG-13-2-001 | 전방 시전 | `cand_43c275560f814c4cb6c6452ecc754a30` | `cand_788450963b01cc734029fdb74b9de746` (body_pose) |
| MG-13-2-002 | 양손 시전 | `cand_11ad1f3658d93ec1849146c2eba95bcd` | `cand_954e6014d22ae3a47ffe1d917d6ba5a0` (hand_pose) |
| MG-13-2-003 | 마법진 전개 | `cand_a51dc7b75761d9569dffda2fde57bc19` | `cand_13d45123835feb0dd741d4309ae1c93e` (light_shape) |
| MG-13-2-004 | 원드 트월 | `cand_562adf026cdaffca586036855085ce7e` | 없음 — 원문·조건만 기록 |
| MG-13-2-005 | 차지 자세 | `cand_20b51cf033b07c82128331a4066fc80f` | `cand_05b3c2bee3335a55923e507c9239e443` (body_pose) |
| MG-13-2-006 | 공중 부유 | `cand_1307497b2134717785973fb1cba15ded` | `cand_4ce95db2c66838fda74d7b152eb3e777` (body_pose) |
| MG-13-2-007 | 발끝을 뻗은 도약 | `cand_b4f148781189d07e212ffe8d23f8c626` | 없음 — 원문·조건만 기록 |
| MG-13-2-008 | 급강하·돌진 | `cand_c6868c2f20758596d4e60390f9f769a4` | 없음 — 원문·조건만 기록 |
| MG-13-2-009 | 한쪽 무릎 착지 | `cand_c5e74f4cff5ce3286467cdee9b1e5256` | `cand_973c69077d2300cba63d9649c3e797ae` (body_pose) |
| MG-13-2-010 | 방어·보호 자세 | `cand_398308dec2bf23aa2dc72419a73d3950` | `cand_905317bed637e87e188c95d13f649983` (body_pose) |
| MG-13-2-011 | 등 맞대기 | `cand_7a8a9eb6cfbb3d04be6e1a667cbea9f8` | `cand_74bf6a46f476b53a92404ff7ba48acd1` (relational_action) |
| MG-13-2-012 | 합동 시전 | `cand_18f021c891ba352848ef72d6f26a51d7` | `cand_582d2dea065398aa14e724a5fd3b68a8` (relational_action) |
| MG-13-3-001 | 기도·소망 자세 | `cand_c33a7282d74d58847e04ad746f0bce7c` | `cand_193fae44e26fdb64527d3bfd067ab487` (hand_pose) |
| MG-13-3-002 | 결의의 응시 | `cand_13d845d65d17e5477e079ab1cfaa2a7e` | `cand_e03d2f46d900f62d7a00b61f23f3f6a7` (expression) |
| MG-13-3-003 | 놀람·망설임 | `cand_7ddf13ffbbea5ca1ee46d164fefec024` | `cand_23374ed0faf4b6f389e953cc36973c29` (expression) |
| MG-13-3-004 | 탈진·주저앉기 | `cand_bdd0747845e3f6779983fb07708b67ac` | `cand_34ddc5ffdbe571fa1a126b6f4cac06a3` (body_pose) |
| MG-13-3-005 | 부서진 도구를 붙잡기 | `cand_6a1096b27346a7e6910abf583e254035` | `cand_fa6268104b3047738a7d336864cdcbdc` (prop_state) |
| MG-13-3-006 | 눈물 속 미소 | `cand_8995cf6ea225040021ab37861d9d63d1` | `cand_f96ce412a96cb47efb510fabc2f01d37` (expression) |
| MG-14-001 | 마법진 | `cand_c2830f043cb410871d917d78bc2a063b` | `cand_13d45123835feb0dd741d4309ae1c93e` (light_shape) |
| MG-14-002 | 시질·문장 | `cand_6efe24e6279f6e13073b215baf84c38b` | `cand_aee00be0bf13b71292ed219643aab694` (light_shape) |
| MG-14-003 | 스파클 | `cand_6098ae520457dd5fa96e3264e115ccfb` | `cand_ca644bc1c59d487a6b59473812d9ad25` (light_shape) |
| MG-14-004 | 오라 | `cand_85fd5014ceccf9ffb02e6132111ffd1b` | `cand_e436dc0919c90fc5df3366609c12bb51` (lighting) |
| MG-14-005 | 스타버스트 | `cand_6b47c3fec41ddb56c7f19e87e0282866` | `cand_3d50af9cbd2c533b48b626fef7495b33` (light_shape) |
| MG-14-006 | 모션 트레일 | `cand_e3ef825378e33fd523300bbb01fa6600` | `cand_328aaabded56df34b26c272fa710c6b3` (light_shape) |
| MG-14-007 | 림 라이트 | `cand_f38b607fbb13f3a212e9ae4d1ef31f22` | `cand_7fa69c1a1df9f1858866d3d9a03e9a90` (light_direction) |
| MG-14-008 | 블룸·글로 | `cand_d9d192a237d23a18b6c937916ba7aa97` | `cand_bbb28bb03fd3e819cdb96c09f33b428d` (lens_artifact) |
| MG-14-009 | 로 앵글·하이 앵글 | `cand_6f8411bb96b52b6497a0bc6bd7cff129` | `cand_dd2822e59126d9d74d77dfc8685efe80` (composition) |
| MG-14-010 | 단축법 | `cand_a9bafc95a57de1851187a8a236240c54` | `cand_1baebc879115941b56985239dbf2354f` (composition) |
| MG-14-011 | 예비동작 | `cand_703c586a7512b091bfca622f3ad19b7a` | 없음 — 원문·조건만 기록 |
| MG-14-012 | 팔로스루 | `cand_9c8a3b6d79a593dec8111d5f91d7f018` | 없음 — 원문·조건만 기록 |
| MG-14-013 | 오버래핑 액션 | `cand_53aa99a0fcac0fe46ad03d635ee44885` | 없음 — 원문·조건만 기록 |
| MG-14-014 | 스미어 프레임 | `cand_8a782fd9bc9cf218eb9bff990fdfb72a` | 없음 — 원문·조건만 기록 |
| MG-14-015 | 포즈 홀드 | `cand_b30193c4d35e2208f8e04766d362cd9f` | 없음 — 원문·조건만 기록 |
