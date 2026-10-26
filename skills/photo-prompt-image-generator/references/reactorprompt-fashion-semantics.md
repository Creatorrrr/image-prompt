# ReactorPrompt fashion semantics and candidate package

This package records independently authored optional visual alternatives grounded in the fashion-related ReactorPrompt corpus. It is an advisory research/data-maintenance package: it does not define universal meanings for source terms, establish brand or historical truth, prove image quality, qualify native use, or record user acceptance.

## Frozen input and provenance

- The merged corpus contains 2,556 terms, 51,771 occurrence assignments, 49,974 distinct literal spans, and 2,974 source documents.
- Frozen source hashes: terms `720dd21d86150793cd9dc86ce02f1ad35a751fa6f4fe3b05708fea13878f70cb`; occurrences `0ad6a96779522c608a3d7ebfb448dfc906f8b3fcde20e0462e75f445d1589c75`; corpus `75fc5c60a1ba56ff47bc3a2dca97302765c3428d782cdb2f64120fe99409cbde`.
- Each card is backed by positive occurrence references in the sidecar. Its candidate provenance points to the enclosing raw document block by document SHA and character offsets. Full prompts and literal source quotes remain in the ignored raw corpus, not in the published assets.

## Package contents

- `photo_reactorprompt_fashion_semantics_20261025.json` contains all 2,556 per-term routes, card-level source/translation/owner/effects review, occurrence references, and existing-candidate triage.
- `photo_candidate_reactorprompt_fashion_20261025.json` contains 34 new authored optional visual candidates.
- `photo_candidate_reactorprompt_fashion_bindings_20261025.json` contains one optional binding for each new candidate.

### Card index

| Card | Authored alternative | Slot |
| --- | --- | --- |
| F001 | 도트 오프숄더 블라우스와 스커트 | `wardrobe_style` |
| F002 | 흰 티셔츠와 쇼츠의 캐주얼 착장 | `wardrobe_style` |
| F003 | 초콜릿 스웨이드 레이어드 룩 | `wardrobe_style` |
| F004 | 그레이 니트와 오픈 트렌치 레이어 | `wardrobe_style` |
| F005 | 그래픽 티셔츠와 레이어드 러플 스커트 | `wardrobe_style` |
| F006 | 세일러 칼라 블라우스와 플리츠 스커트 | `wardrobe_style` |
| F007 | 보타이와 핀스트라이프 조끼 착장 | `wardrobe_style` |
| F008 | 벨벳 하이로우 코트의 홀리데이 코스튬 | `wardrobe_style` |
| F009 | 블랙 새틴 테일러드 세트 | `wardrobe_style` |
| F010 | 그레이 울 수트와 버건디 장갑 | `wardrobe_style` |
| F011 | 컷아웃이 있는 네이비 원피스 수영복 | `wardrobe_style` |
| F012 | 아이보리 새틴 라운지 세트 | `wardrobe_style` |
| F013 | 레이스 캐미솔과 새틴 로브 레이어 | `wardrobe_style` |
| F014 | 화이트 저지 탑과 버건디 새틴 스커트 | `wardrobe_style` |
| F015 | 두 성인의 분리된 이브닝 착장 | `wardrobe_style` |
| F016 | 피치 블러셔와 절제된 글로시 립 메이크업 | `makeup_style` |
| F017 | 풍성한 흑발 웨이브와 자연스러운 잔머리 | `hair_style` |
| F018 | 면 옥스퍼드 셔츠의 보이는 조직 | `surface_material` |
| F019 | 치마 한 패널에 한정된 옅은 청록색 꽃무늬 | `surface_material` |
| F020 | 홀터톱 무늬가 이어지는 매듭 헤드스카프 | `surface_material` |
| F021 | 자연스러운 장력으로 밀착되는 면 깅엄 상의 | `surface_material` |
| F022 | 한쪽 셔링으로 드리우는 비대칭 시폰 스커트 패널 | `garment_fit` |
| F023 | 작은 빨간 티셔츠 그래픽에 한정된 바램 | `garment_state` |
| F024 | 앉은 자세의 둥근 치마 부피 | `garment_fit` |
| F025 | 넓은 거즈 소매와 시스루 숄 | `wardrobe_style` |
| F026 | 넓은 유카타 소매와 오비, 면 주름 | `wardrobe_style` |
| F027 | 등 뒤에서 큰 매듭을 이룬 기모노 오비 | `garment_detail` |
| F028 | 가슴·허리 자수의 치파오풍 홀터 드레스 | `wardrobe_style` |
| F029 | 파이핑·꽃무늬·옆트임 치파오 | `wardrobe_style` |
| F030 | 한쪽 어깨의 황동 시계장치 견장 하나 | `wearable_accessory` |
| F031 | 진주 단추와 브레이딩 장식 볼레로 | `garment_detail` |
| F032 | 흰 티셔츠 위에 입은 청록색 피나포어 | `wardrobe_layering` |
| F033 | 골지 니트 캐미솔의 동색 단추 플래킷 | `garment_detail` |
| F034 | 란제리 컵과 거싯의 불투명 안감 | `garment_detail` |

## Keyword routing and review decisions

Every term has exactly one route. A positive occurrence supports a candidate only when its own source span, owner, garment or accessory role, and relation fit that candidate. A term route to a candidate means bounded source support; it does not assert that the keyword and the candidate have identical meanings.

| Route disposition | Terms |
| --- | ---: |
| `action_not_static_apparel_candidate` | 30 |
| `brand_reference_only_no_brand_truth` | 33 |
| `contextual_only_no_positive_candidate` | 53 |
| `negative_only_diagnostic_no_positive_candidate` | 20 |
| `positive_beauty_vocabulary_without_matching_source_clause` | 113 |
| `positive_visual_vocabulary_reviewed_no_standalone_candidate` | 2,001 |
| `source_positive_support_for_bounded_optional_candidate` | 306 |

The positive vocabulary without a standalone candidate, negative-only terms, contextual-only terms, brand references, and action terms retain explicit non-positive dispositions. Brand mentions do not become claims about authenticity or logos. Negative or contextual evidence is not promoted into positive candidate support.

Whole-source candidate comparisons produced 32 close historical leads; none was reused. Three additional author-triage rows record two non-reuse leads and one held name-only traditional knot term. Working-tree-only candidates are not dependencies.

Existing-candidate comparison records refer to the historical sealed snapshot H-F2 `f5905cd6954bd25e4d396d58ce7cbb4ceda1ed94e971c1001a5bf849c961a940` / native `2884a17d1bd1680c92d58a69349c4dc260c40cb178cfe7469cfdaff3ca71a1ab`, manifest SHA-256 `2d95ec19111795d820a205c0674c3d77786c08f6f153caca987bc8c45747fbaf`. This is comparison provenance only, not a claim of current runtime membership.

## Validation and qualification boundary

- 34 candidates and 34 bindings; 2,556 unique term routes; each route target resolves to its cited card/candidate and correct binding slot.
- Each candidate has positive source references; source document hashes, offsets, enclosing provenance blocks, Korean/English endpoint parity, conditions/effects parity, effects dimensions, and V3 content/condition/effects contracts were checked.
- The sidecar records independent source/bilingual/owner/effects review. Native approval is `false`; pixel qualification is `NOT_RUN`. No native role evidence, image result, pixel gate, or user acceptance is claimed.

## Final module hashes

The frozen module SHA-256 values are:

| Module | SHA-256 |
|---|---|
| `photo_reactorprompt_fashion_semantics_20261025.json` | `9455892d5ee630e5ef8162d553b59b0d4cab82d17a0cca875ec60e1dd9f007a6` |
| `photo_candidate_reactorprompt_fashion_20261025.json` | `ea981c8297a923ae408849f4d2a661e13607e06cc1aaf828bd8ee41f337c35fa` |
| `photo_candidate_reactorprompt_fashion_bindings_20261025.json` | `52610431be7aacf59d941d0ff91e037c406904bad7c6e0760c2dbc818e96ee7b` |

The sidecar also stores frozen source hashes and the historical comparison witness.
