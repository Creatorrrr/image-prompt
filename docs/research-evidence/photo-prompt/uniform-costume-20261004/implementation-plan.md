# 제복 코스튬 데이터 반영 계획

이 계획은 2026-10-04 연구 결과를 authored 시각 의미와 후보 원천에 반영하기 위한 작업 명세다. 이번 요청에서 활성 데이터는 수정하지 않았다. 생성된 `photo-candidate-pack/v6`를 직접 고치는 단계는 없다.

입력은 [145개 키워드 대조](keyword-assessments.json), [83개 관계 초안](relation-proposals.json), [30개 비교 풀](bundle-proposals.json), [출처 장부](sources.json), [59개 검증 요청 쌍](validation-cases.jsonl)이다. `U*`, `UB*`, `UV*`, `UC*`, `S*`는 연구 식별자이며 배포용 ID나 런타임 스키마가 아니다.

## 1. 반영의 우선순위와 작업 단위

| 순서 | 범위 | 우선 관계·대조 항목 | 완료 산출물 |
|---|---|---|---|
| P0 | 기존 관계 재사용과 핵심 구조 | 전복/철릭, 펠리스, 가짜 조끼, 칼라, 갑옷/직물, 앞치마, 코르셋, 헤짐/발광 | 중복을 제거한 candidate/profile 수정안과 좁은 활성화 테스트 |
| P1 | 1차 자료가 있는 기관·시대 버전 | AGSU/ASU, 수병 변천 일부, RCMP, JAL, 대한항공, 실제 간호/교정/사용인 유물 | 부품에 귀속된 배색·여밈·층과 단일 버전 선택 조합 |
| P2 | 계통·직급·직무 조건의 빈칸 | SQ 색-직급, 궁정 의례, 학교별 선 수, 수도회/학위 조건, 최신 경찰 개편 | 직접 근거 추가 확인, 조건화된 alias, 미확인 주장 제거 |
| P3 | 작품 판본과 요청된 무대 변형 | Trek, Wars, NieR, HP, Handmaid, 성인 무대/호러/사이버 | 판본별 공식 이미지 대조, 선택 변형, 소유·연령·신체 경계 테스트 |

P0부터 진행하면서 독립된 근거 확인을 수행할 수 있다. P2/P3 전체를 끝낼 때까지 이미 지지된 P0 관계를 묶어 둘 필요는 없다. 다만 특정 기관·연대·캐릭터 이름으로 정확한 복장을 hard 활성화하려면 그 버전의 근거가 선행되어야 한다.

‘83개를 모두 새로 추가’라는 수량 목표는 두지 않는다. 우선 재사용 12개는 기존 ID 보강이 기본이며, 근거 있는 46개도 동등 관계가 있으면 그 ID에 통합한다. 추가 검증 19개·디자인 5개·크롭 관찰 1개는 각각 사실성 문턱과 적용 범위가 다르다.

## 2. 1단계 — 원천·중복·근거를 고정

1. 최신 HEAD·dirty 경로·관련 authored 파일 해시를 새 작업 스냅샷으로 남긴다. 이번 `baseline-audit.json`을 현재 상태로 덮어쓰지 않는다.
2. 83개 관계를 **물건, 소유자, 방향 관계, 효과**로 현재 사전과 대조한다. alias가 달라도 이 네 값이 같으면 기존 후보·profile을 보강한다. 다른 물건이나 소유·효과는 독립 레코드로 남긴다.
3. 각 이름의 국가/기관·시대·직무/의례·계급·계절·매체/판본·재단 축 중 확인한 값만 보존한다. 서로 다른 출처의 일부를 조합해 존재하지 않는 전체 제복을 만들지 않는다.
4. 출처 종류를 실제 유물, 복제품, 합성 전시, 제작자 인터뷰, 공식 일러스트, 규정/제품 설명으로 구분한다. 승인 범위를 명시하고 불확실한 값은 런타임 이름·필수 구성에서 제외한다.

완료 조건: 우선 작업 항목마다 `기존 ID → 보강 관계 → 직접 근거 범위 → 배제할 가장 가까운 오답`이 연결된다. 정확한 이름별 착장의 전·후면을 확보하지 못하면 관계 후보만 유지하고 named-version hard profile은 보류한다.

## 3. 2단계 — authored 후보를 작성

### 파일 소유

기존 데이터의 소유 경계를 우선 사용한다. 아래 경로는 저장소 루트 기준이다.

| 데이터 소유 | candidate 원천 | visual profile 원천 | 이번 관계 |
|---|---|---|---|
| 코스튬 조합·선택 변형 | `skills/photo-prompt-image-generator/assets/photo_prompt_costume_cosplay_extension.json` | `photo_prompt_visual_obligations_costume_cosplay.json` | 버전 조합, 앞치마·연미복·장교 모티프, 호러·사이버 선택 |
| 공통 의복 재단·겹침 | `photo_prompt_clothing_structure_extension.json` | `photo_prompt_visual_obligations_clothing_structure.json` | 여밈, 독립 상하의, 주머니, 깃, 긴/짧은 밑단 |
| 전통 의복 구조 | `photo_prompt_traditional_clothing_detail_extension.json` | `photo_prompt_visual_obligations_traditional_clothing_detail.json` | 전복·철릭·하카마·케바야 계열의 구체 구조 |
| 머리wear·견장·표식·소품 지지 | `photo_prompt_accessory_structure_extension.json` | `photo_prompt_visual_obligations_accessory_structure.json` | 모자, 부착 표식, 끈의 끝점·소유 |
| 무늬·광택·직물 표면 | `photo_prompt_textile_surface_extension.json` | `photo_prompt_visual_obligations_textile_surface.json` | 무늬 스케일, 광택/발광 구분, 표면 경계 |
| 종교의 명시 외형·도상 | `photo_prompt_religion_iconography_extension.json` | `photo_prompt_visual_obligations_religion_iconography.json` | 직접 종교 의미를 갖는 선택된 의복 관계; 일반 재단은 의복 소유 |
| 작품 인물의 외관 연결 | 기존 character appearance authored 원천을 먼저 확인 | `photo_prompt_visual_obligations_character_appearance.json` | 인물/판본 이름과 검증된 의복 관계의 연결; 신체·종 변경 금지 |

표에서 첫 행 이후의 파일명도 같은 assets 디렉터리 안에 있다. 후보를 기본 `photo_prompt_tags.json`에 중복 삽입하거나 각 파일에 같은 관계를 복제하지 않는다. 기관 버전 수가 커서 별도 uniform extension이 필요하면 근거·소유 경계를 먼저 정하고 일반 extension 등록으로 연결한다. 제복 전용 생성 분기·후보 수 채우기·고정 장면 템플릿을 추가하지 않는다.

### 후보 필드

`ko`, `en`, `aliases`, `keywords`, `embedding_text`에는 선택 결과의 구체적 형태를 적는다. `concept_units`는 다른 옷·인물로 대체할 수 없는 관찰 관계다. `relations`에는 해당 부품의 `declared_owner_scope`와 실제 부착/층/지지 관계를 둔다. 넓은 직업명만 새 exact alias에 넣지 않는다.

`garment_detail`, `wearable_accessory`, `surface_material`, 필요한 `costume_style`이 주 대상이다. 손에 든 물건은 명시된 경우 `prop`에 둔다. `subject`, `action`, `location`을 제복의 공통 필수로 확장하지 않는다. 높은 collar나 visor가 얼굴·머리를 가릴 수 있으므로 기존 외관 잠금과의 가림 충돌도 확인한다.

`affected_dimensions`는 실제 바뀌는 차원만 선언한다. 의복 관계는 appearance에 한정하며 `body_geometry`를 열지 않는다. `affected_properties`는 현재 core의 대상과 잠금 구조를 확인한 뒤 **실제 carrier**에 매핑한다. 이번 연구의 `request_supported_owner`와 임시 `wardrobe.*`/`prop.*` 경로를 그대로 배포하면 안 된다. 앞섶 선택이 피부색·체형·머리 길이 속성을 덮지 않는지 확인한다.

사전 적용성에서 종·연령·대상 수를 보존한다. 인간 예제의 `for_any=["human"]`을 기계/외계 인물에 복사하지 않는다. 성인 변형은 core가 지지하는 성인 맥락에서 선택하고, 일반 교복·수도복의 재사용 관계 전체에 성인/성적 의미를 부과하지 않는다.

완료 조건: 후보 하나가 만들어 내는 변화가 자기 소유의 시각 관계로 설명되고, 선택 전에는 다른 차원의 잠금과 충돌하지 않는다. 출처 URL·연구 상태·시대 정당화·검증 ledger는 후보 본문에 넣지 않는다.

## 4. 3단계 — 좁은 visual profile과 단일 버전 bundle

`activation.exact_terms`는 검증된 의미 구문을 사용한다. `semantic_discovery_requires_component_evidence=true`를 유지하고 `hard_activation`은 그 관계의 독립 선택 증거를 요구한다. 임베딩·BM25F의 유사 발견은 advisory로 남긴다. `전복`, `경찰`, `군복`, `JAL`, `2B` 단독 이름에서 새로운 전신 필수 조합을 모두 활성화하지 않는다.

`semantics`에는 정의·가까운 반례·주장 한계를 작성한다. `authored_components`에는 실제 필요한 구성 요소의 `match_terms`, 고유 `evidence_field`, 관계를 직접 기술하는 `evidence_terms`, 충분한 내용어와 `instruction`을 넣는다. 구성 수를 연구 초안의 두 개로 무조건 고정하지 않는다. 더 복잡한 연결은 필요한 만큼, 하나의 원자 관계는 최소한의 독립 증거로 설계한다.

`render_gate.review_scale`은 native이며, 한 부품만 있거나 연결이 틀리면 FAIL이다. 가려졌거나 프레임 밖이면 UNOBSERVABLE로 기록하고 그 gate를 통과로 집계하지 않는다. 다음은 서로 다른 판단이다.

| 판단 | 예 | 필요한 증거 |
|---|---|---|
| 레이블 검색 | `pelisse` 후보가 발견됨 | 랭크·슬롯·적용성 |
| 선택 관계 | 어깨에 걸친 코트 선택 | 실제 채택 기록과 선택 근거 |
| prompt 표현 | 빈 소매·지지끈을 명시 | 구성 evidence field와 지시 |
| 실제 픽셀 | 빈 소매와 지지끈이 같은 코트에 보임 | native 이미지 검사 |
| 역사 판본 | 정확한 c1820 유물 재현 | 그 유물의 전후면·연대 근거 |

30개 `UB` 비교 풀을 런타임 bundle로 복사하지 않는다. AGSU/ASU, 봄/가을 무늬 면, 스커트/바지, 초기/후기 DS9, 훈련/경기 장비처럼 대안인 부분을 나누고, **하나의 지원되는 버전 안의 동시 선택 부품**만 실제 `visual_semantics` 묶음으로 만든다. concrete `candidate_ids`, 슬롯 참조, 필요한 `hard_profile_ids`, same-frame owner를 연결한다.

bundle은 선택형이며 구성 profile은 개별 요청 근거로 활성화한다. broad 역할 profile의 안전 시연·환자 확인·교통 통제·장비 점검 조건은 유지한다. 군복의 가상 표식 기본과 명시 역사 유물의 실제 표식 선택이 충돌하는 경우는 실제 재현 요청을 보존하도록 데이터 조건을 검증한다.

완료 조건: 단일 관계 요청이 같은 가족의 다른 관계를 강제하지 않고, named-version alias가 검증하지 않은 구성·행동을 추가하지 않는다. bundle 참조는 닫혀 있고 대안 부품이 한 인물의 필수 조건에 동시에 들어가지 않는다.

## 5. 4단계 — 근거를 더 확보할 구체 항목

| 항목 | 다음에 확보할 직접 자료 | 확인하려는 구체 차이 | 확인 전 처리 |
|---|---|---|---|
| 동다리 연대·황색 철릭 | 복식 유물 목록·유물 번호·앞뒤 도판 | 배색 경계와 연대/역할의 실제 대응 | 구조 후보만 사용 |
| 돌만·펠리스·하이랜드·플라스트론 | 연대별 박물관 전후면 | 브레이드, 어깨 지지, 스포런, 가슴판 배색 | 기관·연대 exact 별칭 보류 |
| 초기 수병·데님·1973 | NHHC 해당 규정의 원문·도판 | 칼라·커프스·여밈·모자·하의 | 확인한 연도 차이만 유지 |
| 사막 비행복·초기 가죽·Pan Am | NASM 해당 유물과 항공사 자료 | 재질 외형·포켓·모자·견장 | K-2B/Northwest 사례를 전이하지 않음 |
| 스위스 2025·영국/네덜란드 궁정 | 공식 발표 사진·각 기관의 의례복 도판 | 앞섶·소매·조끼·바지·색 배치 | 발표 존재와 형상 확인을 분리 |
| 한국 경찰 2026 | 접근 가능한 동일 공식 발표 원문·첨부 디자인 | 셔츠/조끼/재킷·배색·도입 범위 | 메타데이터 상태 유지 |
| 홍콩 소방·현대 Met·학생 간호복 | 해당 기관 공식 모델/대학 복제 자료 | 정복/근무/PPE, 지정 색·표식 | 다른 나라 자료로 승인 금지 |
| SQ 색-직급 | 공식 직급별 동일 시대 전신 이미지 또는 명시 표 | 네 색의 정확한 직급 대응 | 색과 구조는 별도 선택 |
| 호텔 벨홉·검정 조리복 | 해당 호텔/제조사 실제 제품과 시점 | 모자·깃·재킷 길이·여밈 | 일반 디자인 가설 유지 |
| 수단·검정 수도복·수녀복·tam | 교단/대학의 직접 안내와 유물 | 계급·교단·학위에 따른 부품 | 넓은 이름의 필수 구성 금지 |
| Trek 12개 버전 | 공식 제작 자료·확대 전후면·에피소드/영화 범위 | TNG 재단, 초기/후기 DS9, 2009 질감, 회색 정복 | 검증된 부품 관계만 유지 |
| Wars Phase/Scout/First Order | 공식 databank 이미지·제작 의상 도판 | 눈/입/턱 면, 판의 연결, 채색 위치 | 헬멧 판본 hard 별칭 보류 |
| NieR 4역할 | 같은 매체의 공식 전신 설정 이미지 | 눈가리개·앞뒤 개구부·하의·소매·부츠 | 2B 상체 관찰만 지지 |
| Handmaid 3계층 | Ane Crabtree 인터뷰 실제 구간·공식 전후면 | bonnet/망토/여밈, 겨울/여름 | 인터뷰 색인과 완전 검증 분리 |

그림에서 보이지 않는 봉제 내부·지퍼·연대·재질 성능은 설명으로 추론하여 채우지 않는다. 정면만 확인한 버전에서 뒷면 closure를 주장하려면 별도 뒷면 자료를 확보한다. 소재 명칭은 소장/제작 기록의 사실과 이미지의 광택·직조 관찰을 분리한다.

## 6. 5단계 — 두 index와 maintenance 연결 갱신

authored 파일을 먼저 안정적으로 합친 후 derived index를 생성한다. 변경된 후보와 profile의 ID·텍스트가 각각 semantic index와 visual profile index에 있어야 한다. generated index 충돌에 한쪽 파일을 선택하는 방식은 사용하지 않는다.

관련 도구:

- `skills/photo-prompt-image-generator/scripts/build_semantic_index.py`
- `skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py`
- `skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py`
- `skills/photo-prompt-image-generator/scripts/photo_candidate_semantics.py`
- `docs/research-evidence/photo-prompt/extension-maintenance/`의 해당 authored 변경 ledger

index 생성은 기존 provider/model/dimensions/text recipe가 맞는 벡터를 재사용한다. 새 임베딩은 batch size 1로 수행하고 ID 변경 없이 정확히 동일 텍스트인 벡터를 다시 호출하지 않는다. semantic manifest/shard 세대와 registry SHA, maintenance record의 authored source SHA를 함께 검증한다. 새 source를 등록한다면 등록 이후 merged corpus와 두 index를 재생성한다.

계획 단계에서는 이 작업을 실행하지 않는다. 기존 파일과 변경될 텍스트를 확인한 다음 도구의 dry-run/check를 먼저 사용하고, 새 임베딩 호출이 필요한 범위를 산정한다.

완료 조건: merged candidate·registry 전체에 대해 index 메타데이터와 닫힌 참조가 통과하며 stale hash/누락 ID가 없다. 팩 하나의 생성 성공을 사전 전체 index 검증으로 대신하지 않는다.

## 7. 6단계 — 반영 후 검증

### 필요한 기존 검증군

변경된 소유 범위에 해당하는 테스트만 먼저 실행한다. 우선 연관 경로:

```text
tests/test_photo_costume_cosplay_semantics.py
tests/test_photo_clothing_terminology_semantics.py
tests/test_photo_traditional_clothing_semantics.py
tests/test_photo_role_garment_candidate_expansion.py
tests/test_photo_womens_professional_uniform_visual_semantics.py
tests/test_photo_candidate_semantics.py
tests/test_photo_visual_profile_retrieval.py
tests/test_photo_visual_obligations.py
tests/test_photo_semantic_index.py
```

새 profile 수에 따른 fixture 상수는 실제 추가·통합 결과로 갱신한다. 후보 수만 세는 테스트를 새로 늘리기보다 관계 activation·owner·대안·잠금·원천 hash의 실제 실패를 검증한다. 다른 concurrent 작업에서 바뀐 수를 이 연구의 성과로 기록하지 않는다.

### 새 비교 요청의 기대값

[validation-cases.jsonl](validation-cases.jsonl)의 59개 쌍은 단순한 ‘옳음/틀림’뿐 아니라 둘 다 유효한 대안 버전도 포함한다. 각 쌍에서 다른 활성화·부품·소유·근거 수준이 유지되어야 한다.

- 같은 의미의 한/영 관계 구문: 같은 후보·profile 의미에 도달하는지 확인한다.
- 직업명·색상·캐릭터 이름만 있는 요청: 새로운 형태 family 전체나 업무 action이 hard 활성화되지 않아야 한다.
- 동음이의어·부정·변경된 소유자: 전복 요리, 옆 사람의 견장, 배경의 줄무늬는 착용자의 관계 증거가 아니다.
- 같은 기관의 다른 시대·직급·하의: 후보 검색·선택·prompt의 부품을 혼합하지 않아야 한다.
- appearance가 잠긴 core: 의복 후보가 신체·나이·종·인원·자세·카메라 잠금을 열지 않아야 한다.
- 근접 semantic hit: BM25F/embedding은 advisory이며, 정확한 관계의 선택 근거와 분리해야 한다.
- 누락 bundle 멤버·닫힌 차원·충돌 속성: 잘못된 묶음을 후보팩에 채워 넣지 않아야 한다.

retrieval의 top-k·eligible set, exact/advisory 판정, adoption 기록, prompt 구성 증거를 각각 남긴다. 검색어 hit만 확인하거나 결과 문자열에 `uniform`이 있다는 이유로 통과하지 않는다. 같은 core/request/controls에서 새 팩을 생성하여 계약 버전·pack identity·서명 변경을 정상 경로에서 확인하고 저장된 팩의 내용을 편집하지 않는다.

완료 조건: 선택된 관계의 필수 구성 누락·타인 소유·버전 혼합·잠금 위반은 0건이다. 미확인 이름별 프로필이 0개 존재하는지가 아니라, 미확인 사실이 hard 의무로 승격된 사례가 0건인지 검증한다.

## 8. 7단계 — native 이미지 평가와 전달

이미지 평가는 후속 이미지 생성 범위가 정해질 때 별도로 수행한다. 대표군은 전복 겹침, 펠리스 빈 소매, 주아브 가짜 조끼, 정복 배색, NASA 직물/압력복, 시대별 수병 칼라, 앞치마/원피스, JAL 판본, 케바야, 수도복 끈, DS9 요크, 장갑/직물 관절을 우선한다.

각 이미지에서 실제 선택한 gate만 평가한다. 모든 83개 연구 관계를 한 이미지의 필수 요소로 요구하지 않는다. 정면·뒤 closure·모자 없음 등 검증할 대상이 보이는 적절한 프레임은 요청의 카메라 잠금이 허용하는 경우에만 선택한다. 요청이 해당 요소를 가리는 구도라면 관찰 불가로 보고하며 구도를 임의 변경해 PASS를 만들지 않는다.

평가 상태는 `PASS`, `FAIL`, `UNOBSERVABLE`로 기록한다. 한 gate의 부분 충족은 FAIL이다. required gate가 UNOBSERVABLE이면 qualification 성공으로 집계하지 않는다. 데이터 validator·unit test·prompt audit·API 생성 완료와 native 픽셀 성공, 사용자의 최종 수용을 각각 기록한다.

최종 전달에는 authored 수정 목록, 기존 관계 재사용/새 관계 수, 근거 보류 항목, 실행한 검증·미실행 경계, 이미지 qualification, commit/push/PR 상태를 구분한다. 전체 profile 수 증가를 곧바로 더 나은 시각 결과로 표현하지 않는다.

## 9. 이번 연구 파일 검증

이번 요청에서는 다음의 로컬 검증만 수행한다.

```bash
python3 docs/research-evidence/photo-prompt/uniform-costume-20261004/build_research_artifacts.py
python3 docs/research-evidence/photo-prompt/uniform-costume-20261004/build_validation_plan.py
python3 docs/research-evidence/photo-prompt/uniform-costume-20261004/validate_research_artifacts.py
```

이 스크립트들은 이 연구 디렉터리 안에만 결과를 쓴다. validator는 145개 원형 보존·출처/관계/비교 풀/검증 쌍 참조·소유·native gate 정책·재사용 ID 존재·초안의 provenance 분리 등을 확인한다. 웹 주장 자체의 사실 검증, 실제 런타임 schema 적합성·검색·이미지 성공을 이 검사로 주장하지 않는다. 결과는 [validation-report.json](validation-report.json)에 있다.
