# 시각 의미 데이터 현황과 개선안

작성일: 2026-10-02 · 기준 커밋: `0e5cc0d1968d5cfe83d1b63e9cfa198724ea9463`

**현재는 프로필을 더 많이 추가하기보다, 이미 있는 의미가 자연스러운 요청에서 정확하게 발견되고 적용되도록 보강하는 것이 우선이다.** 전수 점검에서 1,385개 프로필의 ID와 검색 인덱스는 일치했지만, 21개 프로필은 자체 구성 요소로 만든 문맥을 제외 조건 때문에 거부했다. 한국어 구성 요소 표현과 서로 반대인 의미를 구별하는 자료도 우선 보강 대상이다. 신규 데이터는 요청별 미충족 의미를 확인한 다음 추가하는 편이 좋다.

이번 작업은 분석과 개선안 작성이다. 운영 레지스트리, 스킬, 검색 인덱스는 수정하지 않았다. 이미지 생성·픽셀 심사·사용자 수용률은 측정하지 않았다.

**1. 분석 범위와 단위**

대상은 [photo-prompt-image-generator 스킬](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md)의 현재 로더가 읽는 기본 레지스트리와 확장 레지스트리 22개, 그리고 기존 `photo_prompt_visual_profile_index.json`이다. 저장소의 모든 이미지 스킬, 일반 사전, 품질 계층 전체를 합산한 결과는 아니다.

집계 단위는 **컴파일된 시각 의미 프로필 하나**다. 프로필 하나는 하나 이상의 필수 구성 요소, 프롬프트 증거, 렌더 검사 조건을 가진다. 키워드 하나, 독립된 시각 개념 하나, 검증된 이미지 하나와 같은 단위가 아니다. 별칭 개수나 파일 개수를 의미 범위로 환산하지 않았다.

현재 로더와 인덱스 검증 함수를 직접 사용했다. 저장된 768차원 벡터의 코사인 유사도는 로컬에서 계산했고, 질의 임베딩 API는 호출하지 않았다. 실제 resolver의 exact/BM25F 경로를 이용한 진단 28건을 별도로 실행했다. 원본 파일의 바이트 수와 SHA-256은 [출처 스냅샷](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/source-manifest.json)에 기록했다.

**2. 데이터 양과 증가 추이**

| 항목 | 현재 수량 | 해석 |
|---|---:|---|
| 운영 레지스트리 파일 | 23 | 기본 1개 + 확장 22개 |
| 프로필 / 고유 프로필 ID | 1,385 / 1,385 | ID 중복 없음 |
| exact 검색 행 / 정규화한 고유 검색어 | 3,305 / 3,305 | exact_terms 3,290개 + project alias 15개 |
| 카테고리 | 313 | 파일 단위와 다른 분류 |
| 구성 요소 그룹 | 3,289 | 프로필당 중앙값 2개, 범위 1–9개 |
| 프롬프트 증거 필드 | 3,330 | 존재 여부가 실제 증거 충족을 뜻하지 않음 |
| 렌더 검사 조건 | 3,349 | 존재 여부가 픽셀 통과를 뜻하지 않음 |
| authored_components로 작성한 프로필 | 1,033, 74.6% | 나머지 352개는 기존 명시적 필드 방식 |

Git에 저장된 당시 로더의 파일 목록과 실제 레지스트리를 읽어 비교했다. 과거 코드를 실행하지 않고 AST로 파일 목록만 추출했다.

| 저장된 소스 시점, KST | 커밋 | 파일 | 프로필 |
|---|---|---:|---:|
| 2026-09-06 12:01 | `c3f35a85` | 3 | 354 |
| 2026-09-12 23:29 | `b8378429` | 11 | 619 |
| 2026-09-27 18:21 | `89384cd9` | 15 | 960 |
| 2026-10-01 19:41 | `a1e08cc0` | 23 | 1,385 |
| 2026-10-02 09:00 | `0e5cc0d1` | 23 | 1,385 |

첫 시점 대비 1,031개 증가했다. 증가율은 291.2%, 규모는 약 3.91배다. 이는 몇 개의 커밋 스냅샷이며, 일별 증가율이나 사용량 추이가 아니다. 증가한 수량만으로 의미 정확도나 이미지 품질 향상을 결론 내릴 수 없다.

**3. 파일별 분포: 의미의 크기가 다른 자료가 함께 있다**

아래 파일명은 공통 접두사 `photo_prompt_visual_obligations_`와 확장자 `.json`을 생략했다. `기본`만 `photo_prompt_visual_obligations.json`이다. 한국어 exact 열은 검색어 또는 project alias에 한글이 하나라도 있는 프로필 수다. 구성 요소 제한 열은 `semantic_discovery_requires_component_evidence=true`인 프로필 수다.

| 파일 계열 | 프로필 | 비중 | 구성 요소 그룹 | 그룹 중앙값 | 한국어 exact | 구성 요소 제한 |
|---|---:|---:|---:|---:|---:|---:|
| 기본 | 333 | 24.0% | 1,539 | 5 | 333 | 289 |
| y2k | 306 | 22.1% | 313 | 1 | 0 | 0 |
| clothing_structure | 157 | 11.3% | 160 | 1 | 157 | 157 |
| costume_cosplay | 87 | 6.3% | 87 | 1 | 87 | 87 |
| accessory_structure | 68 | 4.9% | 69 | 1 | 68 | 68 |
| swimwear | 65 | 4.7% | 130 | 2 | 0 | 65 |
| color_relations | 64 | 4.6% | 128 | 2 | 0 | 0 |
| textile_surface | 38 | 2.7% | 39 | 1 | 38 | 38 |
| palace_fortification | 34 | 2.5% | 102 | 3 | 34 | 34 |
| realistic_background | 32 | 2.3% | 96 | 3 | 0 | 0 |
| portrait_fashion_exposure | 28 | 2.0% | 84 | 3 | 0 | 0 |
| historical_womenswear | 24 | 1.7% | 50 | 2 | 24 | 24 |
| traditional_clothing_detail | 24 | 1.7% | 26 | 1 | 24 | 24 |
| editing_effects | 22 | 1.6% | 44 | 2 | 22 | 0 |
| model_editorial | 21 | 1.5% | 63 | 3 | 0 | 0 |
| photo_era | 18 | 1.3% | 90 | 5 | 18 | 18 |
| opening_era | 16 | 1.2% | 64 | 4 | 16 | 16 |
| portrait_composition | 16 | 1.2% | 64 | 4 | 16 | 0 |
| photorealism_elements | 12 | 0.9% | 48 | 4 | 0 | 0 |
| poverty | 9 | 0.6% | 45 | 5 | 9 | 9 |
| everyday_scene | 7 | 0.5% | 28 | 4 | 0 | 0 |
| reactorprompt | 3 | 0.2% | 15 | 5 | 3 | 3 |
| tactile_reality | 1 | 0.1% | 5 | 5 | 1 | 1 |
| 합계 | **1,385** | **100%** | **3,289** | **2** | **850** | **833** |

기본 파일은 프로필의 24.0%이지만 구성 요소 그룹의 46.8%를 담는다. 반대로 Y2K 파일은 프로필의 22.1%, 구성 요소 그룹의 9.5%다. 원자적인 의복·물체 형태와 여러 관계를 함께 요구하는 장면·조명 프로필이 섞여 있기 때문이다. 구성 요소 그룹도 저마다 의미의 크기가 달라서 완전한 범위 지표는 아니지만, 프로필 개수만 세는 것보다 이 차이를 잘 드러낸다.

전체 669개, 48.3%는 그룹 하나짜리다. 모든 그룹이 필수인 프로필은 1,337개, 96.5%다. 복합 프로필을 조건 없이 쪼개거나 일부 그룹만으로 성공 처리하면 원래 의미가 달라질 수 있다.

카테고리 기준 상위 네 묶음은 `observable_fashion_and_object_morphology` 306개, `clothing_visible_relation` 287개, `costume_cosplay_visible_relation` 87개, `swimwear_selected_visible_relation` 65개다. 합계 745개, 53.8%로 패션·의복·물체 형태 계열의 비중이 크다. 첫 묶음에는 기기와 물체도 포함되므로 전부 의복으로 해석해서는 안 된다.

313개 카테고리 중 276개, 88.2%는 프로필 하나만 가진다. 반면 이들이 차지하는 프로필 비중은 19.9%다. 현재 category는 서로 다른 수준의 분류를 섞고 있어 관리용 분포를 한눈에 보기 어렵다. 개별 의미를 유지하면서 별도의 상위 도메인 매핑을 만드는 것이 적절하다.

**판단 한계:** 실제 요청 빈도나 사용 로그는 분석하지 않았다. 지금의 비중만으로 패션에 과투자했거나 생활 장면이 부족하다고 확정할 수 없다. `everyday_scene` 7개와 `photorealism_elements` 12개만 보고 부족분을 정하면, 기본 레지스트리·일반 사전·품질 계층·일반 assertion이 이미 지원하는 의미를 다시 만들 수 있다.

**4. 구조는 정상이고, 의미 접근에는 보강할 지점이 있다**

현재 로더의 검증과 인덱스 메타데이터 검증은 통과했다. 레지스트리 해시, 프로필별 검색 텍스트, 검색 정책과 기존 인덱스가 일치한다. 프로필 ID 중복, 서로 다른 프로필 사이의 exact 검색어 충돌, 렌더 gate ID 충돌은 각각 0건이다. 정규화한 definition 또는 전체 positive 검색 텍스트가 똑같은 프로필 쌍도 없다.

이 결과는 데이터와 인덱스의 구조적 일관성에 대한 결과다. 모든 의미 정의가 정확하거나 모든 요청과 이미지에서 잘 작동한다는 결과는 아니다.

| 언어·접근 항목 | 프로필 수 | 비율 / 분모 | 의미 |
|---|---:|---|---|
| 한국어 exact / alias가 있음 | 850 | 61.4% / 1,385 | 없는 535개가 곧 검색 불가능한 것은 아님 |
| positive 의미 검색 텍스트에 한글이 있음 | 1,319 | 95.2% / 1,385 | 정의·paraphrase·구성 요소·support cue 중 하나 이상 |
| 모든 구성 요소 그룹에 한국어 대안이 있음 | 620 | 44.8% / 1,385 | 그룹별 literal 증거 표현의 완성도와 관련 |
| 구성 요소 증거를 요구하는 discovery 프로필 | 833 | 60.1% / 1,385 | 후보 발견에도 구성 요소 문맥이 필요 |
| 위 833개 중 한국어 구성 요소 표현이 전혀 없음 | 272 | 32.7% / 833 | 우선 조사할 한국어 증거 경로 |
| 모든 exact 검색어가 10단어 이상 | 620 | 44.8% / 1,385 | 영문 공백 단위 계산, 한국어 형태소 길이 지표 아님 |

한국어 paraphrase가 임베딩·BM25F 후보 발견을 돕더라도, literal 구성 요소 제한을 자동으로 충족시키지는 않는다. 다만 실제 스킬은 먼저 요청 의미와 영어 baseline을 확정하므로, 한국어 구성 요소 표현이 없다는 사실만으로 실사용 실패라고 단정하지 않았다. 자연스러운 한국어 요청 → 데이터 조회 전 baseline → 구성 요소 증거 경로를 함께 평가해야 한다.

긴 exact 문장은 완전한 시각 관계를 좁게 지정하려는 설계일 수 있다. definition 전체를 exact에도 넣은 프로필은 778개, 56.2%다. 짧은 일반 키워드를 exact alias에 일괄 추가하면 원래 선택 사항이던 세부 관계가 강제될 수 있다. **자연스러운 한국어·영어 표현은 paraphrase와 positive discovery 표현에 먼저 추가하고, exact 확장은 의미가 확정되는 경우에만 한다.**

**5. 우선 수정할 자기 모순 21건**

전수 진단에서 각 프로필의 구성 요소 그룹 `any_terms` 첫 표현을 연결해 문맥을 만들고 현재 `visual_profile_context_applicability`에 넣었다. 이때 positive context 추가 요구는 끄고, 기존 제외 조건은 유지했다. 1,385개 중 21개, 1.5%가 `request_exclusion`으로 거부됐다.

| 사례 | 자기 문맥에 등장한 제외어 | 왜 문제가 되는가 |
|---|---|---|
| 패닝 | `camera shake` | “흔들림 대신 능동적으로 추적한다”는 설명이 흔들림 요청으로 취급됨 |
| 후막 동조 플래시 | `light painting`, `double exposure` | 다른 기법과 구별하는 문장이 제외 조건에 걸림 |
| 하이라이트 할레이션 | `fog` | 확산 효과와 안개의 구별 설명이 제외 조건에 걸림 |
| 혼합 광원 화이트밸런스 | `split toning`, `gradient map` | 실제 광원 관계와 후처리를 구별하는 문장이 거부됨 |
| 네거티브 필 | `underexposure` | 빛의 차폐와 전체 노출 부족을 구별하는 문장이 거부됨 |

전체 ID·제외어·재현 문맥은 [21건 진단 원문](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/source-component-context-conflicts.json)에 있다.

현재 [제외 조건 처리](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:9647)는 제외어의 출현을 검사하며, 해당 문장의 긍정·부정 역할을 여기서 구분하지 않는다. 패닝 프로필에는 `rather than uniform camera shake ...`가 포함돼 있다. resolver 진단에서도 구성 요소를 모두 제공한 패닝 사례가 후보에서 빠졌다.

이는 데이터에서 파생한 문맥의 자기 일관성 문제다. 21개 모두가 모든 실제 요청에서 실패한다는 뜻은 아니다. 그러나 저자가 제공한 의미 설명이 eligibility 검사와 충돌하므로, 신규 프로필을 늘리기 전에 수정할 근거가 충분하다.

수정은 두 층으로 나눈다.

1. **데이터 보강:** positive discovery/component 표현은 실제로 보여야 할 관계를 긍정형으로 기술한다. 잘못된 대체 표현과 비교 설명은 contrast/reject 자료에도 보존한다. 부정을 지우면 의미가 달라지는 정의는 유지하고 문장을 개별 검토한다.
2. **공통 처리 개선:** 제외어가 실제로 요구되는지, 다른 의미와 구별하기 위해 부정되는지 처리한다. 기존 negation helper는 `rather than` 같은 모든 대비 구문을 해결하지 않으므로 단순 함수 교체로 끝내지 않는다. 실제 제외 대상의 긍정 요청과 target 자체의 부정 요청을 함께 회귀 검사한다.

이번 개선안에서 운영 코드 수정은 제안이며 실행하지 않았다. 발견률을 올리기 위해 구성 요소 제한이나 제외 조건을 일괄 해제해서는 안 된다.

**6. 유사한 프로필은 삭제보다 구별 자료가 필요하다**

저장된 벡터 1,385개는 모두 768차원이고 유한한 비영 벡터다. 서로 다른 프로필 쌍의 코사인 유사도가 0.90 이상인 쌍은 70개, 0.95 이상은 6개, 0.99 이상은 0개다.

0.95 이상 여섯 쌍은 정의를 읽어 보면 동일 자료가 아니라 **주체·역할·방향이 반대인 의미**다.

| 프로필 쌍 | 유사도 | 유지해야 하는 구별 |
|---|---:|---|
| cr_warm_highlights / cr_cool_highlights | 0.9879 | 따뜻한 하이라이트·차가운 그림자 / 반대 배치 |
| top_hourglass_silhouette_relation / bottom_hourglass_silhouette_relation | 0.9753 | 성인 실루엣의 위쪽 우세 / 아래쪽 우세 |
| cr_warm_foreground / cr_cool_foreground | 0.9749 | 따뜻한 전경·차가운 원경 / 반대 배치 |
| broad_face_light_orientation_relation / short_face_light_orientation_relation | 0.9705 | 카메라에 넓게 보이는 볼에 주광 / 좁게 보이는 볼에 주광 |
| cr_colored_key / cr_colored_fill | 0.9665 | 색이 있는 주광 / 색이 있는 보조광 |
| cr_complex_subject / cr_complex_background | 0.9640 | 색상군이 더 많은 피사체 / 색상군이 더 많은 배경 |

이 수치는 문서 벡터의 근접성이다. 질의 벡터를 만들거나 실제 오검색률을 측정한 결과가 아니다. 따라서 유사도 임계값으로 자동 병합하면 필요한 의미를 잃는다. 역할과 방향을 명시하는 positive 표현, 한국어 대조 문장, 잘못된 owner와 역방향 관계를 넣은 negative 사례를 추가하는 편이 좋다.

**7. 실제 resolver 진단의 결과와 한계**

다양한 파일에서 8개 의미를 골라 세 종류의 요청을 실행하고, 넓은 스타일 요청·부정 요청 4건을 추가했다. 총 28건이다. 대상은 렘브란트 조명, 레이서백, 패닝, 붉은 물체만 컬러로 남기는 효과, 폴더폰, 의복 구조, 인물 구도, 카페 픽업 대기 장면이다.

| 진단 조건 | 목표 후보 발견 | 목표 exact hard | 용도 |
|---|---:|---:|---|
| 자연스러운 요청 문장만, baseline 없음 | 5/8 | 1/8 | 초기 발견·제한 조건을 드러내는 스트레스 진단 |
| 레지스트리의 exact 표현 사용 | 8/8 | 8/8 | 기존 등록과 exact 연결 확인 |
| 자연 문장 + 레지스트리 구성 요소 문맥 | 7/8 | 1/8 | 구성 요소가 있을 때 eligibility 연결 확인 |
| 넓은 의미·부정 대조 4건 | 해당 없음 | 0/4 | 검사한 사례에서 강제 적용 없음 |

예를 들어 렘브란트 자연 문장은 필터 적용 전 BM25F 순위가 1위였지만 구성 요소 제한 뒤에는 목표 후보가 없었다. 구성 요소 문맥을 제공하면 선택 가능한 후보로 발견됐다. 패닝은 구성 요소 문맥을 제공해도 앞의 자기 모순 때문에 빠졌다. 의복 구조와 카페 사례는 필터 적용 전후 후보 풀이 달라져 순위가 달라졌으므로, 필터 전 순위를 최종 검색 성능으로 쓰지 않았다.

**이 수치를 전체 스킬의 정확도로 읽으면 안 된다.** baseline 없는 요청은 정상적인 공개 생성 경로의 authorial core가 아니다. exact/component 대조는 운영 자료에서 답을 가져왔으므로 독립 holdout도 아니다. 사례는 수작업으로 골랐고 실제 수요 가중치가 없다. 질의 임베딩, 전체 core/envelope 감사, 후보 채택, 생성 프롬프트 감사, 이미지 생성과 픽셀 검사는 이번 진단에 포함하지 않았다. 재현 자료는 [resolver 진단 결과](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/retrieval-probes.json)다.

**8. 실행 우선순위**

운영 자료를 수정하기 전에 비교용 독립 요청과 기대 의미를 먼저 고정한다. 아래는 그 준비 이후의 구현 우선순위다.

| 순서 | 작업 | 첫 작업 범위 | 완료 기준 |
|---|---|---|---|
| 1 | 자기 문맥·제외 조건 충돌 해소 | 발견된 21개 + 공통 polarity 처리 | 타당한 positive component 문맥의 자기 거부 해소; 실제 제외 요청과 target 부정 요청은 계속 차단 |
| 2 | 한국어 접근 보강 | guarded 272개 중 검토한 첫 50개 | 그룹별 자연스러운 한·영 표현과 독립 요청 대조; exact 오강제 증가 없음 |
| 3 | 반대 의미 구별 | 유사도 0.95 이상 6쌍 | 주체·역할·방향을 바꾼 대조 요청에서 분리; 두 의미 모두 유지 |
| 4 | 관리용 도메인과 범위표 | 1,385개 ID의 외부 매핑 | 현재 ID/category 보존; 상위 영역·하위 영역·의미 단위별 조회 가능 |
| 5 | 근거·검증 상태 연결 | 위 보강 대상부터 기존 연구 증거 연결 | 출처와 검증 단계가 프로필 ID·버전으로 추적됨 |
| 6 | 확인된 빈 영역만 신규 작성 | 실제 요청에서 재현한 미충족 의미 | 기존 자료와 중복 없음; 완전한 의미·혼동 경계·증거·픽셀 기준 포함 |

50개는 첫 검토 배치의 제안이며, 이번에 보강했거나 품질을 인증한 수량이 아니다. 선택 순서는 실제 요청 증거가 있으면 사용 빈도·영향도를 반영한다. 없으면 자기 모순 여부, literal 표현의 한국어 공백, 반대 의미와의 혼동 가능성으로 정하고 수요 추정이라고 표기하지 않는다.

1,033개는 authored_components에서 증거·지시문·gate를 함께 생성한다. 나머지 352개는 수정할 때 같은 방식으로 점진 이관할 수 있지만, 표현·강제 조건·review scale이 보존되는지 먼저 비교해야 한다. 전체 일괄 이관은 첫 과제가 아니다.

claim_limits가 없는 332개, affected_dimensions/affected_properties 또는 core_assertion_discovery가 없는 프로필도 모두 오류로 분류하지 않았다. 각각 의미 범위와 기존 경로를 검토해야 한다. typed visual_relation이 있는 프로필은 3개지만 다른 프로필도 자연어 evidence·gate에 owner 관계를 담을 수 있다. 단순 필드 존재율로 관계 데이터가 없다고 결론 내리지 않는다.

**9. 보강할 데이터 한 묶음의 기준**

기존 [작성·컴파일 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/visual_profile_contracts.py)과 [유지보수 지침](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/maintenance.md)을 사용한다. 새로운 검색용 필드를 임의로 만드는 것보다 현재 allowlist와 계약에 맞추는 것이 먼저다.

| 자료 | 작성 원칙 | 기존 위치 / 산출물 |
|---|---|---|
| 정확한 의미 | 무엇이 누구에게 어떤 관계로 보여야 하는지 설명 | semantics.definition |
| 자연스러운 요청 표현 | 짧은 한국어·영어 문장, 의미를 넓히지 않는 변형 | semantics.paraphrase_examples |
| 구성 요소 | 필수 관계별 그룹과 한·영 positive 대안; 단어 하나로 복합 의미를 충족하지 않음 | authored_components / component_semantics |
| exact 표현 | 별칭만으로 의미가 확정될 때 등록; 넓은 스타일어로 하위 형태를 강제하지 않음 | activation.exact_terms / 검토한 alias |
| 혼동 경계 | 비슷한 물체, 반대 방향, 틀린 owner, 부분적인 충족 | contrast_examples / reject_substitutes |
| 적용 범위 | 실제 바꿀 차원·속성과 문맥 조건만 선언 | concept_candidate / activation |
| 프롬프트 증거 | label 대신 실제 보이는 형상·접촉·방향을 요구 | required_evidence_fields / compiled instruction |
| 렌더 판정 | native/thumbnail/both 구분, 필수 조건과 실패 조건 | render_gates |
| 연구·검증 출처 | source ID, URL·발행/확인일, 근거 범위, 검증 단계 | 운영 검색 밖의 docs manifest/ledger |

예를 들어 “패닝”은 피사체 핵심의 상대적 선명함, 평행한 배경 궤적, 실제 움직임의 방향 일치 등을 positive 구성 요소로 보강할 수 있다. “카메라 흔들림과 다르다”는 대조 근거는 유지하되, 제외어 출현 자체가 positive 문맥을 거부하지 않도록 함께 검토한다. “따뜻한 전경”은 전경=따뜻함, 원경=차가움이라는 owner 연결을 명시하고, 반대 배치와 전체 웜 필터를 각각 대조한다. 이 예시는 작성 방향이며 운영 데이터에 추가한 내용은 아니다.

연구 출처는 이미 여러 docs 증거에 존재한다. 운영 JSON에 URL이 없다는 이유로 무출처라고 판정하지 않았다. 보강할 것은 외부 증거와 현재 profile ID 사이의 일관된 연결이다. URL·provenance·claim limit·반례를 positive 임베딩 텍스트에 섞어서 검색을 풍부하게 만들지 않는다. 현재 [검색 텍스트 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_visual_retrieval.py)은 positive 의미만 포함한다.

검증 상태도 하나의 “완료” 값으로 합치지 않는다. `authored`, `indexed`, `retrieved`, `adopted`, `prompt_checked`, `rendered`, `pixel_reviewed`, `user_accepted`를 증거 파일·버전·날짜와 연결한다. 이 명칭은 외부 관리 원장의 제안이며 운영 스키마에 추가한 필드가 아니다. 증거가 없는 상태는 미확인으로 남긴다.

**10. 신규 영역 선정 방법**

관리용 표는 상위 도메인 → 하위 도메인 → 의미 단위로 만든다. 상위 도메인 예시는 인물·외형, 의복·물체 구조, 조명·색 관계, 광학·촬영, 재질·표면, 구도·공간, 장면·행동·접촉, 시대·문화 맥락이다. 의미 단위는 물체 형태, 두 대상의 관계, 복합 장면, 편집 효과 등을 구별한다. 이 매핑은 실제 정의를 읽어 작성하고 현재 category를 자동 치환하지 않는다.

다음으로 요청 × 시각 요구 표를 만든다. 요청 하나를 관찰 가능한 관계로 분해하고, 각 관계가 기본/확장 레지스트리, 일반 사전, 품질 계층, 일반 typed assertion 중 어디서 지원되는지 기록한다. 상태는 기존 지원, 표현 보강 필요, 혼동 경계 보강 필요, 신규 의미 필요, 이미지 확인 필요로 나눈다.

생활 장면의 물건 건네기·잡기·대기, 피사체와 재질의 접촉, 조명과 표면 반응, 전경과 원경의 공간 관계는 조사 후보가 될 수 있다. 그러나 이 보고서는 해당 영역이 현재 전부 없다고 판정하지 않았다. 요청에서 필수인 관계가 기존 자료로 해결되지 않는다는 재현 근거가 있을 때 신규 프로필을 작성한다. 분야별 동일 개수 할당은 권장하지 않는다.

**11. 개선 효과를 검증하는 실험 설계**

현재 자료의 자기 일관성 진단과 별개로, 데이터 수정 전에 독립적인 요청과 기대 의미를 고정한다. 실제 스킬 계약에 따라 요청 의미와 baseline을 데이터 조회 전에 작성하고, 조회된 자료로 baseline을 소급해 맞추지 않는다. 기존 holdout의 기대값도 개선한 데이터에 맞춰 바꾸지 않는다.

첫 50개에 대한 예시 배치는 의미 보존 paraphrase 5건 + 가까운 잘못된 의미 2건 + owner/방향 반전 1건, 프로필당 8건으로 총 400건이다. 이는 앞으로 만들 실험의 제안 수량이며 이번 측정 수량이 아니다. 한국어와 영어, 짧은 표현과 완전한 관계 설명을 나누어 집계한다.

| 단계 | 평가할 것 | 통과 기준 또는 보고 방식 |
|---|---|---|
| 등록·인덱스 | ID·텍스트·메타데이터·벡터 갱신 | 현재 validator 통과, 입력 버전 일치 |
| eligibility | 자기 문맥, positive/negative 대비, 구성 요소 제한 | 타당한 자기 문맥 거부 없음; 명시적 제외·target 부정은 적용 안 됨 |
| 후보 발견 | 목표 의미가 optional 후보로 보이는가 | 언어·영역·문장 유형별 target recall과 오후보율 보고 |
| exact hard | 명시적 의미 확정과 좁은 alias | 계약상 확정된 검사 요청은 100%; 대조군의 잘못된 hard 적용은 0건을 배치 통과 기준으로 설정 |
| 후보 채택 | 고정된 core와 열려 있는 범위에 맞는가 | optional 후보 발견과 채택을 따로 집계 |
| 프롬프트 | 실제 구성 요소·owner·부정 경계가 반영되는가 | 기존 literal evidence 및 composed audit 통과 |
| 생성·픽셀 | 조건이 실제 이미지에 모두 보이는가 | 해당 gate의 native/thumbnail 기준; 부분 충족은 실패 |
| 사용자 수용 | 요청자가 결과를 받아들이는가 | 별도 직접 확인, 자동 추정 안 함 |

100%와 0건은 고정된 회귀 배치의 목표다. 전체 자연어 일반화 성능이나 실제 이미지 성공률을 보장하는 수치가 아니다. 후보 발견률은 현재 28건 진단을 기준 성능으로 사용하지 않고 새 독립 배치에서 전후 비교한다.

운영 레지스트리가 바뀌면 기존 절차로 인덱스를 갱신하고 관련 회귀를 실행한다. 렌더 검증은 고정된 요청·프롬프트·이미지 해시·reviewer 증거를 보관한다. 현재 [렌더 검토 감사](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_moe_render_review.py)는 실제 review 입력을 검증하는 단계이므로, 데이터 등록이나 resolver 통과를 픽셀 성공으로 대체할 수 없다. 이 보고서 작성 중 이미지 생성 실험은 하지 않았다.

**12. 재현 자료와 다음 작업 묶음**

첫 작업 묶음은 **독립 요청 고정 → 21개 자기 모순 수리 → 첫 50개 언어 표현 보강 → 반대 의미 6쌍 대조 검증**으로 제안한다. 상위 도메인·연구 원장은 이를 관리하는 작업으로 함께 진행하고, 신규 프로필 수 증가는 범위표에서 확인한 미충족 관계에 한정한다.

분석 결과와 코드는 다음 파일에 남겼다.

- [전수 지표 JSON](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/metrics.json), [파일별 분포 CSV](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/source-distribution.csv), [카테고리 분포 CSV](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/category-distribution.csv)
- [프로필별 목록 CSV](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/profile-inventory.csv), [근접 벡터 쌍 JSON](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/near-duplicate-vector-pairs.json)
- [전수 분석 코드](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/analyze.py), [resolver 진단 코드](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/retrieval_probes.py), [실행 결과를 포함한 노트북](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-02-visual-semantics-data-audit/visual-semantics-audit.ipynb)

전수 분석은 NumPy가 있는 Python으로 실행한다. resolver 진단은 표준 라이브러리와 운영 코드만 사용하며, 이번 환경에서 약 134초가 걸렸다. 두 스크립트는 이 분석 디렉터리의 산출물만 다시 쓴다. 오래된 source-manifest와 맞는지 확인하기 전에 재실행하면 스냅샷이 갱신되므로, 기존 결과를 보존할 필요가 있으면 먼저 복사한다.

```sh
cd /Users/chasoik/Projects/image-prompt
/Users/chasoik/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 docs/analysis/2026-10-02-visual-semantics-data-audit/analyze.py
python3 docs/analysis/2026-10-02-visual-semantics-data-audit/retrieval_probes.py
```

노트북은 저장된 전수 결과의 집계, 원본 SHA-256 일치, source 파생 자기 모순, resolver 조건별 결과를 다시 검사한다. 출력은 실제 실행 결과이며, 전체 resolver 28건을 노트북 안에서 반복 실행하지는 않는다.
