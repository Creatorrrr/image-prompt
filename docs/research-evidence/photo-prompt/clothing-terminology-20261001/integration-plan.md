# 의류 시각 의미·후보팩 반영 계획

2026-10-01 · 연구 자료를 근거로 한 구현 계획 · 이 문서의 런타임 변경과 이미지 시험은 아직 실행하지 않았다.

**권장 순서는 문맥·소유 대상 정리 → 재사용/신설 결정 → 변형별 부품 작성 → 후보팩 노출·채택 확인 → 원본 픽셀 심사다.** 먼저 핵심 구조를 편입하고, 소재·장신구·신발, 전통·역사복식의 변형으로 확대한다. 1,151개 라벨을 한 번에 동의어로 넣는 방식은 이 계획에 포함하지 않는다.

## 반영 범위와 단계별 산출물

| 단계 | 작업 | 구체적 산출물 | 통과 조건 |
|---|---|---|---|
| 0. 뜻과 관측 범위 닫기 | 155개 레코드의 변형·부품·출처를 비교하고 702개 잔여 라벨을 분류 | 정의/소유자/변형/비시각 정보 장부, 재사용 결정표 | 편입할 항목마다 정의 근거·관찰 한계가 닫힘 |
| 1. 핵심 의복 구조 | P0의 넥라인·칼라·소매·여밈·주머니·봉제·핏·부착을 작은 묶음으로 작성 | wardrobe_style/garment_detail 후보와 선택 변형 프로필 | 부품 소유자·연결·불필요한 체형 변화 없음 |
| 2. 소재·장신구·신발 | 조직/표면/성분을 분리하고 미세 연결 구조 보강 | surface_material/wearable_accessory/footwear 후보 | 소재·성능 추정 없음, 정확한 상세 뷰의 게이트 |
| 3. 전통·역사 변형 | 현재 전통·역사·코스튬 데이터와 비교, 지역/시대별 표본의 범위 유지 | 소유 부품, 레이어, 여밈 방향, 변형별 후보 | 개별 표본의 특징을 전 범주에 일반화하지 않음 |
| 4. 로더·검색 표면 반영 | 확장 등록, 인덱스 재생성, source hash 연결 | candidate/visual-profile 인덱스와 maintenance sidecar | 중복 ID·누락 참조 없음, 현재 계약과 일치 |
| 5. 행동·픽셀 자격 확인 | 라우팅·후보팩·채택·생성을 별도로 심사 | 사례별 ID·prompt·hash·이미지·게이트 장부 | 해당 변형의 필수 게이트 전부 통과, 요청 잠금 유지 |

P0 79개, P1 67개, P2 9개는 연구 우선순위다. runtime 프로필/후보의 최종 개수는 재사용과 변형 분해 후에 결정한다. 조사 상태와 우선순위는 다른 축이다. P0라도 근거가 닫히지 않았으면 편입을 보류하고 근거 확인 작업을 먼저 한다.

첫 작성 묶음은 15개 [설계 예](profile-candidate-blueprints.json)의 관계다. 그 중 직접 근거가 충분한 관계부터 편입하고, 특징을 더 확인해야 하는 관계는 0단계에 남긴다. 이를 통해 22개 필수 부품·관계 게이트를 실제 데이터와 후보팩에서 연결할 수 있는지 먼저 확인한다. 15개 전체를 무조건 신규로 추가하지 않는다.

## 파일과 소유 위치

현행 로더는 prompt_generator.py의 RESEARCH_EXTENSION_FILENAMES와 VISUAL_OBLIGATION_EXTENSION_FILENAMES 목록으로 확장 파일을 병합한다. 파일을 assets에 저장하는 것만으로 자동 로딩되지 않는다. 실제 파일 목록과 검증 로직을 유지하면서 필요한 파일만 등록한다.

| 연구 모듈 | 현재 레코드 수 | 후보 확장 제안 | 프로필 확장 제안 |
|---|---:|---|---|
| garment_structure | 79 | photo_prompt_clothing_structure_extension.json | photo_prompt_visual_obligations_clothing_structure.json |
| textile_surface | 21 | photo_prompt_textile_surface_extension.json | photo_prompt_visual_obligations_textile_surface.json |
| accessory_structure | 36 | photo_prompt_accessory_structure_extension.json | photo_prompt_visual_obligations_accessory_structure.json |
| traditional_variants | 19 | photo_prompt_traditional_clothing_detail_extension.json | photo_prompt_visual_obligations_traditional_clothing_detail.json |

위 파일명은 미래 제안이다. 현재 생성하지 않았다. 실제 소유 위치가 기존 확장과 같으면 기존 파일을 보강하며, 별도 원천 파일은 새 의미를 소유할 필요가 있을 때 만든다. prefix는 clt_g_/clt_t_/clt_a_/clt_r_ 등으로 분리하되 병합 ID 충돌을 먼저 검사한다. 설계 예의 clt_ ID는 예시 ID이며, 재사용 결정 후 사례의 기대 ID도 함께 확정한다.

실제 기존 파일/코드의 책임:

- [prompt_generator.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:155): 확장 목록과 현재 load_json/load_visual_obligation_registry 병합 경로. 필요한 등록만 변경하고 이 작업의 데이터 보강 때문에 랭킹·샘플링 알고리즘을 넓게 수정하지 않는다.
- [photo_candidate_semantics.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_candidate_semantics.py:23): 닫힌 runtime extension/bundle 필드, 유지보수 참조, 기존 후보 문맥 확장, 관계 검증.
- [visual_profile_contracts.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/visual_profile_contracts.py:104): 부품별 evidence field·instruction·render gate 계약.
- [build_semantic_index.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/build_semantic_index.py:299), [build_visual_profile_index.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py:99): 두 검색 표면의 재생성·캐시/해시 확인.
- assets의 photo_prompt_tags.json, photo_prompt_visual_obligations.json, 관련 확장 파일: 기존 동일 부품의 원천 소유 위치를 찾는 비교 기준.
- docs/research-evidence/photo-prompt/clothing-terminology-20261001/: 출처·조사 상태·판단 근거를 보관할 유지보수 자료. 런타임에 그대로 로드하지 않는다.

## 의미와 슬롯의 변환 규칙

| 연구 정보 | 실제 반영 위치 | 제한 |
|---|---|---|
| 품목/세트 | wardrobe_style, 문맥에 따라 costume_style | 품목과 문화/직업/스타일을 필요 없이 결합하지 않음 |
| 넥라인·칼라·소매·여밈·봉제·핏·착용 관계 | garment_detail | 소유 의복과 부착점 명시 |
| 조직·기모·광택·시어·패턴 | surface_material | 성분·제조법·성능과 분리 |
| 귀걸이·체인·머리·허리 장식·가방 | wearable_accessory | 대상과 접촉/연결을 지정 |
| 신발 품목·레이싱·굽·스트랩 | footwear | 장식과 구조 축을 독립 |
| 관찰 가능한 의복 비례 | 우선 garment_detail, 필요할 때만 silhouette_proportion | 기존 슬롯의 신체 형상 의미와 섞이지 않는지 검사 |
| 정의와 혼동 경계 | semantics.definition/contrast_examples/claim_limits | 좁은 표본 정의를 보편화하지 않음 |
| 구체적 필수 관계 | authored_components | variant별 필수 부품만. 특징 풀 전체를 conjunction으로 복사하지 않음 |
| 후보의 원자 명제·관계 | concept_units, relations | id/type/subject/object의 명시적 물건과 연결 |
| 출처·문화 범위·조사 상태 | maintenance sidecar + maintenance_ref | 닫힌 런타임 키에 임의 source_urls/research_status 필드를 추가하지 않음 |

현행 유지보수 참조 계약은 photo-extension-maintenance-ref/v1의 contract_version, record_id, sha256다. 출처 JSON과 데이터 소유 파일 사이의 해시를 고정한다. 인덱스나 compiled bundle을 별도의 정의 원천으로 손으로 수정하지 않는다.

### 기존 항목을 재사용하는 판단 순서

1. current-data-audit.json의 포인터에서 후보·프로필 원문을 읽는다. 어휘 일치는 비교 시작점이다.
2. 물건·부품 소유자·연결 대상·형상·요청 적용 범위·부정 대조를 비교한다.
3. 동일 의미라면 기존 candidate/profile ID를 보존한다. 의미가 같은 표현은 기존 후보의 paraphrases/contexts 확장으로 추가한다.
4. 물건, 소유자, 행동, 연결 대상이 바뀌면 새 후보를 만든다. bail/veil, skirt gore/bra bridge, shoe/fabric Oxford는 이 경우다.
5. 같은 품목의 비배타적 축은 별도 후보를 조합한다. Oxford+brogue, platform+wedge, halter+특정 neckline이 예다.
6. Y2K·코스튬·역사 파일의 항목도 형태가 같으면 재사용 후보지만, 해당 시대/스타일 태그·성별·배경까지 의미를 확장할 수 있다는 뜻은 아니다.

existing_slot_context_extensions는 의미가 같은 표현과 선택 문맥을 덧붙이는 표면이다. 기존 항목의 효과 범위를 넓히거나 가드를 없애는 용도로 사용하지 않는다. 프로필 exact_terms나 project_glossary_aliases의 보강은 별도 hard 활성화 검토를 거친다.

## 프로필과 optional bundle 작성

각 연구 레코드는 ‘관련 용어군’이다. family의 모든 terms_for_research를 exact_terms/aliases로 복사하지 않는다. 예를 들어 CT의 neckline_basic 안에서 V와 scoop은 대안이며, CT의 bra_family 안에서 low bridge와 longline band도 별개다.

반영 단위는 아래의 순서로 닫는다.

1. 선택한 품목·변형·sense를 지정한다.
2. 필수 물건과 관계를 최소 부품으로 분리한다.
3. 각 부품의 영문 표현·한글 표현·비용어 paraphrase를 작성한다.
4. generic label, 비슷한 다른 물건, 프린트 흉내, 가림, 다른 소유자를 reject substitute로 남긴다.
5. 실제 요청 근거로 활성화되는 조건을 작성한다. 넓은 스타일 요청, 후보 검색 결과, 후보 선택만으로 hard 조건을 만들지 않는다.
6. 실제 이미지에서 확인 가능한 관계만 render gate에 둔다. 내부 소재·성능은 claim limit 또는 메타데이터로 남긴다.

관계가 복합적이면 여러 후보를 묶은 optional bundle을 사용한다. source-hash-bound candidate_ids/candidate_slots/component_groups/confusion_boundaries/relations를 작성한다. 연관 hard_profile_id는 요청 증거를 대신하지 않는다. bundle이 발견되거나 채택됐다는 사실만으로 관련 hard 프로필을 활성화하지 않는다.

의복 제품 사진처럼 인물이 없는 요청도 고려한다. 관계의 소유자는 먼저 의복/장신구이며, 모든 후보에 for_any=human을 일괄 붙이지 않는다. 사람이 입은 상태의 접촉이 정의인 경우에는 그 조건을 좁게 설정한다. 속옷 구조의 시험은 우선 flatlay로 설계하고, 착용 시험을 추가하는 경우에는 요청이 정한 성인·노출·구도를 보존한다.

설계 예의 weight=0.35는 임시 검토 값이다. 실제 편입에서는 같은 슬롯의 인접 항목과 선택 분포를 비교해 값을 정한다. 신규 후보를 무조건 높은 점수로 올려 노출을 강제하는 것은 품질 확인이 아니다.

## 세부 조사 후속 작업

702개 잔여 항목은 원 대화에서 누락시키지 않고 coverage-ledger.json의 keyword_id로 추적한다. 모두 새 프로필이 필요한 것은 아니다. ‘이미 있는 동등 의미 / 시각 부품 필요 / 변형 구분 필요 / 비시각 메타데이터 / 동의어 재확인’으로 분류한 뒤 필요한 항목만 추가 작성한다.

| 후속 작업군 | 우선 질문 | 필요한 근거 | 편입 차단 조건 |
|---|---|---|---|
| 상품명 겹침 | bustier/corset, balloon/bishop, fedora/trilby, bag types가 어느 용례에서 겹치는가 | 여러 제작자 구조 설명과 패턴/표본 | 겹치는 이름을 잘못 배타적 정의로 만듦 |
| 소매·칼라 세부 | 재단 경로, 칼라 stand, 라펠 junction, 손목 마감이 실제로 어떻게 다른가 | 제작자 패턴·봉제 교육·기술 도표 | 단어 설명만 있고 연결 경로가 없음 |
| 소재 세부 | 섬유, 조직, 상업 원단명, 마감의 어느 층인가 | CottonWorks 개별 항목·직편물 제작 자료 | 광택/색을 제조법·성분의 증거로 사용 |
| 레이스·자카드·기모 | 바탕망·모티프 연결·파일/골·직편물 변형이 무엇인가 | 제조 구조와 매크로 표본 | 원거리 착용 사진만으로 세부 조직 판정 |
| 체인·클라스프 | 링크 위상과 실제 통과·맞물림이 어떻게 다른가 | Rio Grande 원 도표·공급자 제작 안내 | 접근 불가한 PDF를 읽은 것으로 취급 |
| 안경·시계 | 프레임/브리지/템플, 케이스/베젤/다이얼 부품과 기능의 경계 | 제조자 부품도 | 보호 성능·감별·기계 기능을 외관 게이트로 설정 |
| 한복 세부 부품 | 섶·무·배래·회장·말기·대님·주머니의 위치와 시대 변형 | 한국 학술·박물관 개별 항목과 소장 표본 | 부품·시대·성별이 다른 표본을 단일형으로 묶음 |
| 아시아 전통 세트 | ao dai, hanfu, kurta, lehenga 등 품목/세트/천이 어떻게 구분되는가 | 현지 박물관·문화기관·제작자 구조 자료 | 일반화된 ‘동양풍’ 이미지가 정의를 대신함 |
| 중동·아프리카·유럽·아메리카 | 로브·머리 덮개·직물·세트의 층위와 지역 변형은 무엇인가 | 현지 기관·소장품·개별 제작 자료 | 국적·종교·민족을 착용자 추론으로 편입 |
| 역사·종교복·갑옷 | 시대별 원본/재현, 외층/내부판, 유사 명칭의 부위가 무엇인가 | 박물관 소장 정보·보존/구성 연구 | 판타지 재현이나 표본 한 점을 보편 정의로 삼음 |

sources.json의 index_only/blocked/search_excerpt_only는 직접 본문 확인을 먼저 시도할 조사 큐다. 동일 기관의 접근 가능한 다른 원자료를 찾되, 출처가 바뀌면 새 source_id를 만들고 그 자료의 실제 지지 범위를 다시 기록한다.

## 라우팅·후보팩·픽셀 검증 계획

[qualification-plan.json](qualification-plan.json)에 61개 계약 사례와 12개 최초 생성 arm을 설계했다. 현재는 planned_not_executed다. 설계 예 15개 각각에 한/영 명시 관계와 부정 사례를 두고, gore/bail/Oxford/kimono sleeve/jersey/cuff/stole의 다른 문맥, 소재의 역추론, broad style, optional-only, 인물 없음, 몸·좌우·구도 잠금 등을 더했다.

### 1. 현재 기준선부터 보존

변경 전 HEAD, 모든 원천 파일 해시, 인덱스 메타데이터, 관련 테스트·라우팅 fixture 결과를 기록한다. 기존 실패가 있으면 변경 전후 동일 사례를 대조한다. 전체 저장소가 현재 모두 통과한다고 가정하지 않는다.

기존 관련 테스트를 먼저 사용하고, 새 의미 분기/오탐 경계만 실제 테스트로 추가한다.

- tests/test_photo_visual_obligations.py
- tests/test_photo_visual_profile_retrieval.py
- tests/test_photo_candidate_semantics.py
- tests/test_photo_womens_casualwear_visual_semantics.py
- tests/test_photo_womens_activewear_visual_semantics.py
- tests/test_photo_body_shape_semantics.py
- tests/test_photo_traditional_clothing_semantics.py
- tests/test_photo_historical_womenswear_semantics.py
- tests/test_photo_costume_cosplay_semantics.py
- tests/test_photo_y2k_visual_semantics.py

위 목록을 무조건 전부 반복 실행하는 규칙으로 만들지 않는다. 실제 반영 파일과 영향을 받는 분기를 기준으로 선택하고, 새 실패·변경·미해결 우려가 있을 때 넓힌다.

### 2. 검색 표면과 계약 확인

현재 CLI의 확인된 기능을 사용한다.

- build_semantic_index.py --dry-run: 새 원천의 예정 메타데이터와 누락 벡터 수를 먼저 확인. 실제 재생성 시 호환 벡터를 재사용하고, 필요한 신규 임베딩 호출만 한다.
- build_visual_profile_index.py --cache-index PATH: 호환 캐시를 이용해 재생성.
- build_visual_profile_index.py --check: 재생성된 인덱스와 실제 레지스트리의 정합성 확인.
- 병합 데이터에서 중복 ID, 미해결 참조, 허용되지 않은 extension/bundle 키, 차원 범위, source hash projection을 검사.

semantic builder에는 이 조사에서 확인한 --check 옵션이 없다. 메타데이터 비교와 실제 병합 검색 테스트로 의미 인덱스의 정합성을 확인한다.

### 3. 후보팩에 실제로 도달하는지 확인

v6 요청 envelope와 독립적으로 작성·고정한 authorial core를 사용한다. 생성 턴에서는 데이터 검색 전 초기 의미와 요청 잠금을 먼저 확정한다. 현재 연구에서 만든 후보 문구를 그 초기 의미의 출처로 뒤늦게 넣지 않는다.

사례마다 다음을 별도 기록한다.

- 요청과 byte-grounded active spans, core/hash.
- 선택된 intended sense와 required/advisory profile IDs.
- 후보팩의 실제 candidate IDs와 bundle IDs, 존재하지 않으면 absence.
- 최종 저작 프롬프트가 채택한 ID·관계와 채택하지 않은 항목.
- requester-locked body, camera, action, clothing, exposure, direction 유지 여부.

optional 요청에서는 모든 제안 후보가 채택될 필요가 없다. ‘실제 노출’과 ‘의미가 맞는 채택’을 따로 보고하며, 노출/채택이 안 된 묶음을 보강 효과의 성공 사례로 계산하지 않는다.

### 4. 명시 관계의 독립 시험과 holdout

15개 설계 예의 정확 문구는 계약 probe다. 이를 실제 사용자 언어 전체에 대한 일반화 증거로 삼지 않는다. 구현 전 다른 사람이 쓸 법한 비동일 paraphrase를 별도로 작성하고, source aliases에 그대로 넣지 않은 holdout으로 유지한다.

한글/영문, 명칭/부품 설명, 단독 구조/복합 레이어, 긍정/부정, 인물/제품, 지정 변형/미지정 변형을 대조한다. 부정·다른 sense 사례에서 false hard activation 목표는 0이며, 몸·촬영 잠금 이탈도 0을 요구한다. 실패 항목은 수정 후 해당 영향 범위를 다시 확인한다.

### 5. 12개 이미지 arm

첫 묶음은 스위트하트, 기고 소매, 프린세스 심, 웰트, 파이핑, 보닝 채널 외관, 헤링본 조직, bail, 더비, 동정, 노리개, 기모노 여밈이다. 세부 구조의 조건이 닫힌 항목만 실행한다.

각 arm의 주 비교는 최초 1회 생성, 성공 이미지만 골라내는 재시도 0회로 설계한다. 도구 차단·호출 오류는 시도 상태이며 품질 FAIL과 구분한다. 이후 수정 실험은 새 버전·새 arm으로 기록한다.

- 요청된 관계가 동시에 보이는 시험 구도를 사전에 정한다. 원래 사용자 구도에 대한 성공 주장과는 구분한다.
- prompt/negative 바이트, 요청/core/pack/source hash, 도구·모델·횟수, 출력 이미지와 시도 장부를 보존한다.
- native 픽셀에서 부품의 소유자·연결·형상을 게이트별로 판정한다.
- 2/3 게이트처럼 일부만 통과하면 해당 arm은 FAIL이다. 12개 arm 평균으로 실패를 가리지 않는다.
- 내부 재료·실제 성능·보석 감별은 픽셀 성공 항목에 넣지 않는다.
- 노출, 채택, prompt 계약, 픽셀, 사용자 판단을 같은 PASS로 합치지 않는다.
- 후속 데이터/별칭/검색 표면이 바뀌면 이전 source hash의 픽셀 결과를 새 버전의 자격 증거로 일반화하지 않는다.

최초 arm은 절대적 보강 효과나 인과 개선율을 증명하지 않는다. ‘보강으로 전보다 좋아졌다’는 비교를 하려면 동일 요청·core·모델·시험 조건에서 변경 전후를 별도 비교하는 실험을 추가한다.

## 완료 조건과 진행 장부

각 편입 단위의 상태는 다음 순서로 남긴다.

definition_closed → data_authored → schema_valid → routing_qualified → exposed → adoption_observed → pixel_qualified → user_judgment_pending/accepted

순서는 작업 관리 상태이며 앞 단계를 뒷 단계의 증거로 대체하지 않는다. 기능/성분처럼 픽셀로 닫을 수 없는 항목은 metadata_only로 별도 종결한다. 숨은 내부를 억지로 pixel_qualified로 만들지 않는다.

이번 연구를 반영한 묶음의 완료 조건은 다음과 같다.

- 편입된 모든 단위의 출처 범위·sense·소유자·선택 변형·혼동 경계가 작성됨.
- 기존 항목 재사용/신설 이유와 실제 source file·candidate/profile ID가 장부에 연결됨.
- 영향을 받는 계약·라우팅·문맥 충돌·잠금 사례가 통과함.
- 해당 시험 묶음의 신규/보강 항목 노출·채택 유무가 실제 ID로 기록됨.
- ‘픽셀 자격’을 붙인 변형은 필수 관계 전부 통과했고, 미시험 변형은 미시험 상태로 남음.
- 남은 용어는 coverage-ledger에서 확인 가능하며, 완료된 것으로 덮어 쓰지 않음.

작업량은 155개 레코드를 일괄 신규 데이터 155개로 계산하지 않는다. 0단계의 재사용 결정과 변형별 분해가 끝나면 후보 수·프로필 수·실험 수를 확정할 수 있다. 현재 계획의 최소 첫 검토 묶음은 15개 설계 예, 계약 사례 61개, 조건을 닫은 최초 이미지 arm 최대 12개다.
