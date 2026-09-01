# 판타지 용어 시각 의미·후보팩 확장 리서치

- 조사일: 2026-09-01
- 대상: `photo-prompt-image-generator`
- 입력 범위: 참조 대화 「판타지 용어 조사」에 정리된 장르, 세계 구조, 마법, 직업, 종족, 생물, 장소, 아이템, 서사 장치 키워드
- 구현 범위: 픽셀에서 반증 가능한 12개 정밀 시각 계약과 그 계약을 지원하는 후보팩·역할 장면군
- 비구현 범위: 이미지 생성, 렌더 판정, 사용자 취향 판정, 장르 전체를 하나의 외형으로 고정하는 규칙

## 1. 결론

판타지 용어는 이름의 유명도보다 관찰 가능한 구조에 따라 네 층으로 나누어야 한다.

1. **정확 시각 계약**: 형태의 연결 수, 경계, 재료 연속성, 행위자-대상 인과처럼 한 장의 이미지에서 참·거짓을 판정할 수 있는 개념.
2. **후보팩·역할 장면군**: 직업이나 세계관 용어를 의상 대신 반복 가능한 행위·매개체·결과 묶음으로 표현하는 개념.
3. **자문형 의미 검색**: 하이 판타지, 그림다크, 소드 앤 소서리처럼 정의가 중첩되고 작품별 구현이 달라 영감 후보로는 유용하지만 하드 픽셀 의무로 만들면 과잉 고정되는 개념.
4. **비시각 또는 사용자 정의 우선**: 하드/소프트 마법 체계, 운명, 선택받은 자, 마나, 레벨, 신성/악, 종족 정체성처럼 한 장의 외형이 사실을 증명할 수 없는 개념.

이번 확장은 1층의 12개 계약과 2층의 `소환사`, `연금술사` 역할 장면군을 구현한다. 3·4층은 검색 후보 또는 사용자 정의로 남긴다.

## 2. 참조 대화 키워드의 데이터 라우팅

| 대화의 키워드군 | 데이터 처리 | 이유 |
|---|---|---|
| High/Low/Epic/Heroic/Dark/Grimdark/Gothic/Cozy/Romantasy/Sword & Sorcery/Science Fantasy | 자문형 장르 후보 | 장르 경계가 역사·비평·시장 문맥에 따라 겹치며 단일 형태로 환원되지 않는다. |
| realm/plane/dimension/multiverse/portal/rift/nexus | `portal`만 좁은 관계 계약, 나머지는 후보 | 포털은 두 공간·경계·통과의 동시 증거를 요구할 수 있지만 realm/plane은 이미지에서 존재론을 증명할 수 없다. |
| wizard/sorcerer/warlock/witch/summoner/alchemist/necromancer | 역할별 인과 장면군 | 외모·로브·모자보다 수행자-매개체-결과가 강한 시각 증거다. 기존 witch와 necromancer 계약을 보존하고 summoner·alchemist를 추가한다. |
| spell/rune/glyph/sigil/magic circle/seal/ward/barrier | `magic circle`만 좁은 경계 계약, 나머지는 후보 | 닫힌 선의 안팎 차이와 효과 차단은 픽셀 판정 가능하다. 기호의 실제 효능·언어·의식 정확성은 판정할 수 없다. |
| golem/construct/automaton/living armor | golem·living armor 정밀 계약 | 재료 연속성, 빈 내부, 관절, 독립 행동의 결과를 한 프레임에서 확인할 수 있다. |
| dragon/wyvern/griffin/hippogriff/hydra/phoenix | wyvern·griffin·hippogriff·hydra 형태 계약, phoenix 인과 계약 | 좁은 형태·전환은 판정 가능하지만 광범위한 `dragon`은 문화·작품별 변이가 커 하드 고정하지 않는다. |
| familiar/companion/spirit animal | reciprocal familiar 관계 계약 | 특정 동물 종이나 검은 고양이 외형이 아니라 상호 주의·공유 신호·공동 과업이 관계를 증명한다. |
| elf/orc/dwarf/fairy/demon/angel/dragonkin | 자문형 후보와 사용자 정의 | 외형 고정은 작품별 설정을 침범하고 정체성·도덕성·가치 판단을 잘못 추론할 위험이 있다. |
| hard/soft magic, mana, soul, divine, chaos/order, time/space magic | 사용자 정의 우선 | 체계·출처·비용·윤리·능력은 한 장의 이미지로 검증할 수 없다. 가시적 행위 결과만 장면 후보가 될 수 있다. |
| chosen one, prophecy, quest, dungeon, guild, academy, court intrigue | 서사·장소 후보 | 장면은 제안할 수 있지만 역할·지위·운명·조직 소속을 픽셀만으로 단정하지 않는다. |

## 3. 권위 출처와 추출한 시각 차원

### 3.1 장르 경계는 하드 계약이 아니다

- [The Encyclopedia of Science Fiction — Fantasy](https://sf-encyclopedia.com/entry/fantasy)는 fantasy를 광범위한 초자연·비현실 서사 영역으로 다루며, high/low 구분도 보편적으로 엄밀한 형태 분류가 아님을 보여준다.
- [Heroic Fantasy](https://sf-encyclopedia.com/entry/heroic_fantasy), [Sword and Sorcery](https://sf-encyclopedia.com/entry/sword_and_sorcery), [Science Fantasy](https://sf-encyclopedia.com/entry/science_fantasy)는 용어가 역사적으로 겹치고 다른 비평 범주와 경쟁해 왔음을 보여준다.
- 데이터 결정: 장르명은 BM25F·임베딩 후보 검색과 프리셋 조합에만 사용한다. `high fantasy = 성/엘프/로브`, `grimdark = 검은 갑옷/피`, `cozy = 파스텔/찻잔` 같은 단일 외형 규칙은 만들지 않는다.

### 3.2 포털은 “고리”가 아니라 두 공간을 잇는 통과 관계다

- [The Encyclopedia of Science Fiction — Parallel Worlds](https://sf-encyclopedia.com/entry/parallel_worlds)는 다른 세계로의 이동·방문 관계를 핵심으로 다룬다.
- [The Encyclopedia of Science Fiction — Stargates](https://sf-encyclopedia.com/entry/stargates)는 포털 장치를 이동을 가능하게 하는 관문으로 설명하며, 익숙한 고리 외형이 서사·제작상의 관습일 수 있음을 보여준다.
- 추출 차원: 완전한 경계, 가까운 공간, 물질적으로 다른 먼 공간, 경계면을 통과하는 한 대상의 일관된 가림, 경계에 국소화된 빛·먼지·반사·왜곡.
- 혼동 경계: 발광 고리, 거울, 창문, 장식 아치, 동일 공간을 보여주는 구멍은 실패한다.

### 3.3 소환은 동반자 배치가 아니라 도착 인과다

- [Folger Shakespeare Library — Macbeth 4.1](https://www.folger.edu/explore/shakespeares-works/macbeth/read/4/1/)에는 수행자가 출현체를 불러내는 장면 구조가 있다. 이 자료는 현대 판타지 직업의 보편 정의가 아니라 “행위자-출현체” 관계의 역사적 사례로만 사용한다.
- 추출 차원: 살아 있는 수행자, 한정된 소환원, 별도로 몸을 가진 도착체, 손짓·시선·방향 반응, 접촉 그림자·밀린 먼지 같은 국소 결과.
- 혼동 경계: 반려동물과 나란히 선 인물, 빈 마법진, 일반 오라, 복제된 시전자, 시체 반응은 실패한다. 시체·유해 앵커는 기존 `necromancer_dead_causality`로 분리한다.

### 3.4 연금술은 병과 로브가 아니라 재료 변환 공정이다

- [Science History Institute — Transmutations: Alchemy in Art](https://www.sciencehistory.org/visit/exhibitions/museum-transmutations-alchemy-in-art/)는 연금술 작업이 증류·야금·가열 장치와 노동 과정으로 표현되어 왔고, 희화화와 성실한 작업 묘사가 공존함을 설명한다.
- 추출 차원: 수행자의 조작, 연결된 레토르트·도가니·용기·이동 경로, 동시에 비교되는 입력/출력 재료, 색·질감·상·결정 구조의 국소 변화, 응축액·슬래그·침전·열 변색.
- 혼동 경계: 병을 든 의상 초상, 포션 정물, 입력/출력 없는 색연기, 현대 실험실 분위기만 있는 인물은 실패한다.
- 안전 경계: 실제 화학 조리법·폭발·독극물 제조·읽을 수 있는 수식은 후보에 넣지 않는다.

### 3.5 골렘은 비생물 재료의 조립된 몸과 과업 결과다

- [Jewish Museum in Prague — The Golem of Prague](https://www.jewishmuseum.cz/novinka/the-golem-of-prague-the-legend-of-rabbi-loew-s-creation/)와 [Old-New Synagogue](https://www.jewishmuseum.cz/en/explore/sites/old-new-synagogue/)는 프라하 전승 속 골렘을 점토로 만든 인공 존재, 생명을 얻어 명령을 수행하고 공동체를 보호하는 존재로 설명하면서 역사적 사실과 전설을 구분한다.
- 추출 차원: 비생물 재료로 조립된 한 몸, 몸통-팔다리-관절의 재료 연속성, 이음선·맞물린 블록·다져진 점토, 접촉 그림자와 독립 움직임, 옮긴 짐·열린 길 같은 과업 결과.
- 문화·재사용 경계: 프라하 전승의 신성한 글자, 유물 외형, 장식, 특정 인물 이야기를 복제하지 않는다. 런타임은 원본 허구 구축물의 추상적 활성화 관계만 사용한다.
- 혼동 경계: 조각상, 돌 갑옷을 입은 사람, 금속 로봇, 돌무더기, 빛나는 글자만 있는 장면은 실패한다.

### 3.6 살아 있는 갑옷은 “빈 내부 + 관절 + 독립 결과”다

- [The Metropolitan Museum of Art — Arms and Armor bulletin](https://resources.metmuseum.org/resources/metpublications/pdf/Arms_and_Armor_The_Metropolitan_Museum_of_Art_Bulletin_v_32_no_4_1973_1974.pdf)과 [Renaissance Armor educator resource](https://www.metmuseum.org/-/media/files/learn/for-educators/publications-for-educators/renaissance.pdf)는 겹판, 가동 리벳, 바이저, 건틀릿 등 착용 갑옷의 관절 구조를 설명한다.
- 출처가 뒷받침하는 것은 갑옷의 외부 구조다. 자율성은 판타지용 원본 설계이며 박물관 자료의 역사 사실로 주장하지 않는다.
- 추출 차원: 완전한 투구-몸통-팔-다리 껍질, 주요 관절의 겹판, 열린 바이저/목/건틀릿 틈의 빈 부피, 접지된 자율 움직임, 문·사물·먼지에 남긴 결과.
- 혼동 경계: 갑옷을 입은 기사, 마네킹, 휴머노이드 로봇, 잘린 빈 갑옷, 떠다니는 투구·건틀릿은 실패한다.

### 3.7 와이번은 좁은 기본 토폴로지만 제공하고 사용자 정의를 우선한다

- [British Museum — signet-ring with wyvern](https://www.britishmuseum.org/collection/object/H_AF-619)은 와이번을 독수리 발과 뱀 꼬리를 가진 문장학적 날개 달린 용으로 기술한다.
- 런타임 기본값: 머리 하나, 몸통 하나, 날개 둘, 골반에 연결된 뒷다리 둘, 별도 앞다리 없음, 긴 꼬리 하나.
- 이 기본값은 모든 문화·게임·작품을 대표하지 않는다. 요청자가 다른 정의를 제공하면 그 정의가 항상 우선한다.
- 혼동 경계: 네 다리 날개용, 새, 날개 없는 뱀, 여섯 팔다리 키메라, 다리 수가 가려진 크롭은 실패한다.

### 3.8 그리핀과 히포그리프는 뒤 절반으로 분리한다

- [The Metropolitan Museum of Art — Griffin](https://www.metmuseum.org/art/collection/search/472849)은 그리핀을 사자의 몸과 뒷다리, 독수리의 머리와 날개가 결합된 존재로 설명한다.
- [Project Gutenberg — Orlando Furioso](https://www.gutenberg.org/cache/epub/615/pg615-images.html)의 Canto IV는 히포그리프의 앞부분을 그리핀 계통, 나머지를 암말로 묘사한다. [Princeton University Art Museum — Ruggero Riding the Hippogriff](https://artmuseum.princeton.edu/art/collections/objects/7971?field_tms_obj_subjects_target_id=627)도 히포그리프를 말과 그리핀의 교차로 설명한다.
- 공통 전면: 독수리 머리·갈고리 부리·깃털 날개·조류형 앞부분.
- 그리핀 후면: 사자 몸통·뒷다리·발·꼬리.
- 히포그리프 후면: 말 몸통·뒷다리·발굽·말꼬리.
- 혼동 경계: 말 후면 그리핀, 사자 후면 히포그리프, 말 머리 페가수스, 날개 달린 사자, 붙여 놓은 동물 콜라주는 실패한다.

### 3.9 히드라는 “머리 개수”보다 한 몸과 분리된 목 뿌리가 중요하다

- [The Metropolitan Museum of Art — Hydra](https://www.metmuseum.org/art/collection/search/625055)는 여러 머리와 재생 전승을 설명한다.
- 한 장의 정지 이미지에서 재생 능력은 자동 증명되지 않으므로 하드 게이트에서 제외한다. 절단과 재생의 동시 사건을 명시한 요청에서만 별도 전환 증거가 필요하다.
- 추출 차원: 한 몸통·골반·팔다리 체계, 세 개 이상의 완전한 목 경로, 같은 어깨 체계에 분리된 목 뿌리, 분리된 턱·방향·실루엣, 접지와 규모.
- 혼동 경계: 뱀 다발, 복제된 몸 여러 개, 장식 머리 후광, 케르베로스형 짧은 목, 합쳐진 목 뿌리는 실패한다.

### 3.10 피닉스는 불새 외형이 아니라 재생의 연결된 상태 변화다

- [The Metropolitan Museum of Art — phoenix dress entry](https://www.metmuseum.org/art/collection/search/158944)와 [A Medieval Bestiary](https://resources.metmuseum.org/resources/metpublications/pdf/A_Medieval_Bestiary_The_Metropolitan_Museum_of_Art_Bulletin_v_44_no_1_Summer_1986.pdf)는 피닉스의 죽음·소진과 재에서의 새 출현이라는 순환 전승을 다룬다.
- 추출 차원: 이전 상태의 재 둥지/탄 흔적/소진된 몸, 새로 출현하는 한 마리, 재-불씨 섬유-깃털의 연속 전환, 상승 방향, 국소 열·그을림·밀린 재.
- 혼동 경계: 불꽃색 새, 불길을 통과하는 새, 서로 무관한 새 두 마리, 재만 있는 장면, 떨어져 있는 재와 깃털은 실패한다.

### 3.11 사역마는 특정 동물이 아니라 상호 협업 관계다

- [Folger Shakespeare Library — Witches, familiars, and historical accusation](https://www.folger.edu/blogs/shakespeare-and-beyond/recipe-witches-macbeth-witchcraft/)은 동물 조력자 이미지가 고양이에 한정되지 않았고 실제 박해·고발 문맥과 연결되어 있음을 보여준다.
- 런타임은 역사적 고발이나 악마화가 아니라 원본 허구의 협업 관계만 사용한다.
- 추출 차원: 수행자, 별도 몸의 동물형/영체 조력자, 양방향 주의, 공유 토큰·실·반사·소리·빛 경로, 열린 걸쇠·찾은 사물·운반 샘플·결계 반응 같은 공동 결과.
- 혼동 경계: 고양이와 함께 선 마녀, 카메라를 보는 동물, 장식 까마귀, 일반 동반자, 종 고정관념은 실패한다.

### 3.12 마법진은 복제 가능한 의식 도식이 아니라 국소 규칙 경계다

- [Wellcome Collection — manuscript of conjuration circles](https://wellcomecollection.org/works/egcdd88a)는 원·라멘·구속 관계를 포함한 역사 자료를 목록화한다.
- 데이터는 역사 도식이나 실행 지침을 복제하지 않고 “닫힌 경계”라는 추상 구조만 사용한다.
- 추출 차원: 잘리지 않은 닫힌 선, 실제 바닥·벽·테이블·사물 표면에 맞는 원근, 안팎 상태 차이, 선에서 정확히 멈추거나 굽는 효과, 먼지·액체·그림자·그을림·접촉 흔적.
- 혼동 경계: 장식 러그, 포털 고리, 후광, 표면 없는 글리프 구름, 복제된 의식 도식은 실패한다.

## 4. 구현된 하드 계약

| 프로필 ID | 핵심 판정 | 가장 가까운 실패 대체물 |
|---|---|---|
| `fantasy_portal_two_world_threshold` | 두 공간 + 완전한 경계 + 통과 가림 + 국소 결과 | 발광 고리, 거울, 창문 |
| `summoner_distinct_entity_arrival` | 수행자 + 한정 소환원 + 별도 도착체 + 방향 반응 + 결과 | 동반자 초상, 빈 원, 시체 반응 |
| `alchemist_material_transmutation_process` | 조작 + 연결 장치 + 전후 재료 + 변환부 + 잔류물 | 포션 정물, 색연기, 실험실 의상 |
| `golem_constructed_material_agency` | 조립 재료 몸 + 연속 관절 + 동작 + 과업 결과 | 조각상, 로봇, 돌무더기 |
| `living_armor_hollow_articulated_agency` | 완전한 갑옷 + 관절 + 빈 내부 + 자율 결과 | 착용 기사, 마네킹, 로봇 |
| `wyvern_two_leg_wing_tail_topology` | 날개 2 + 뒷다리 2 + 앞다리 0 + 꼬리 1 | 네 다리 용, 새, 뱀 |
| `griffin_eagle_lion_topology` | 독수리 전면 + 사자 후면 + 연속 접합 | 히포그리프, 날개 사자 |
| `hippogriff_eagle_horse_topology` | 독수리 전면 + 말 후면 + 연속 접합 | 그리핀, 페가수스 |
| `hydra_multi_neck_single_body` | 한 몸 + 분리 목 3개 이상 + 분리 뿌리 | 뱀 다발, 복제 몸, 케르베로스 |
| `phoenix_rebirth_causal_cycle` | 이전 재 상태 + 한 새 몸 + 연속 전환 + 상승 | 일반 불새, 불날개 |
| `familiar_practitioner_reciprocal_bond` | 두 참여자 + 상호 주의 + 공유 신호 + 공동 과업 | 펫 초상, 장식 동물 |
| `magic_circle_local_rule_boundary` | 닫힌 표면 경계 + 안팎 차이 + 선의 차단 + 흔적 | 러그, 포털 링, 후광 |

각 계약은 다음을 모두 가진다.

- 5개 필수 구성요소 그룹
- 서로 다른 근거 문구 5개
- 썸네일·원본 크기 렌더 게이트 5개
- 최소 5개 실패 대체물
- 인접 개념과 일반어를 막는 직접 용어 경계
- 요청자 정의가 레지스트리 기본값보다 우선한다는 전역 선행 규칙

## 5. 후보팩 확장

### 5.1 후보 구성 원칙

고립 명사를 추가하지 않고 다음 묶음으로 추가한다.

`주체 → 행동 → 매개 소품 → 장소 → 물리 효과 → 사후 흔적`

이 구조는 “판타지 분위기”를 쌓는 대신 한 프레임의 관찰 가능한 사건을 만든다.

### 5.2 추가된 묶음

- 소환/포털: `summoner_practitioner_role_model`, `summoning_distinct_entity_arrival`, `bounded_summoning_anchor_prop`, `summoning_observation_chamber`, `summoned_entity_contact_shadow_forming`, `summoning_displaced_dust_trace`.
- 연금술: `alchemist_practitioner_role_model`, `distilling_visible_material_transition`, `alchemical_retort_crucible_prop`, `alchemist_heatwork_lab`, `transmutation_boundary_material_gradient`, `transmutation_before_after_trace`.
- 구축물: `constructed_golem_subject`, `hollow_living_armor_subject`, 각각의 과업 행동과 `fantasy_construct_test_court`, `golem_task_material_trace`.
- 생물 형태: wyvern, griffin, hippogriff, hydra 주체와 형태가 가려지지 않는 회전·펼침 행동.
- 피닉스: 이전 재 상태와 새 몸을 함께 보존하는 주체·상승 행동·재-깃털 흔적.
- 사역마: 특정 종 대신 양방향 신호와 공동 과업을 요구하는 행동·공유 토큰.
- 마법진: 표면에 고정된 선에서 효과가 멈추는 행동·물리 효과.

### 5.3 역할 장면군

`소환사`와 `연금술사`는 각각 고정 주체 `identity_core`와 네 장면 변형을 가진다.

- 소환사: 별도 존재 도착, 이세계 횡단, 도착 안정화, 귀환 해제.
- 연금술사: 연결 증류, 전후 샘플 검사, 출력물 냉각, 정제소 공정 감사.

역할은 성인 원본 허구 캐릭터로 제한하고 실제 의식 지침, 화학 조리법, 희생·피해, 프랜차이즈 정체성을 배제한다. 의상·얼굴·성별·민족성·매력도는 역할의 증거가 아니다.

## 6. 의도적으로 하드닝하지 않은 항목

- `fantasy`, `high fantasy`, `low fantasy`, `epic fantasy`, `dark fantasy`, `grimdark`, `cozy fantasy`, `romantasy`, `sword and sorcery`.
- `wizard`, `sorcerer`, `warlock`, `mage`의 보편 외형 구분. 작품 설정이나 요청자 정의 없이는 로브·지팡이·나이·성별로 구분하지 않는다.
- `dragon`의 보편 다리·날개 수. wyvern만 좁은 기본 토폴로지를 제공한다.
- `elf`, `orc`, `dwarf`, `fairy`, `angel`, `demon`, `beastkin`의 정체성·도덕성·가치·종족 고정 외형.
- `hard magic`, `soft magic`, `mana`, `divine`, `arcane`, `soul`, `curse`, `blessing`의 실제 효능과 체계.
- `chosen one`, `prophecy`, `level`, `class`, `quest`, `guild rank`, `noble blood`, `good/evil alignment`의 서사 사실.

이 항목들은 후보 검색·조합의 어휘가 될 수 있지만 그 자체로 새 하드 시각 프로필을 활성화하지 않는다.

## 7. 검증 설계

### 7.1 패키지·스키마

- 세 JSON 원본이 파싱되고 사전 스키마를 통과해야 한다.
- 프로필 인덱스는 원본 레지스트리 해시와 일치해야 한다.
- 후보 의미 인덱스는 태그 버전·후보 수·샤드 매니페스트와 일치해야 한다.
- 프로필 ID, 게이트 ID, 후보 ID, 역할 장면 ID는 중복되지 않아야 한다.

### 7.2 직접 활성화

- `차원문`, `소환사`, `연금술사`, `골렘`, `living armor`, `wyvern`, `griffin`, `hippogriff`, `hydra monster`, `phoenix rebirth`, `사역마`, `마법진`이 의도한 단일 프로필로 라우팅되어야 한다.

### 7.3 인접 부정 예시

- `portal site`, `login portal`, `mirror`, `glowing ring`은 포털 프로필을 활성화하지 않는다.
- `companion portrait`, `empty magic circle`, `necromancer`, `corpse`는 소환사 프로필을 활성화하지 않는다.
- `potion bottle`, `chemist portrait`, `colored smoke`는 연금술사 프로필을 활성화하지 않는다.
- `statue`, `robot`, `armored knight`, `mannequin`은 골렘·살아 있는 갑옷 프로필을 활성화하지 않는다.
- `dragon`, `pegasus`, `cerberus`, `fire bird`, `cat`, `circular rug`은 인접 환상생물·사역마·마법진 프로필을 활성화하지 않는다.
- 광범위 장르·직업·종족명은 이번 12개 프로필 어느 것도 강제하지 않는다.

### 7.4 렌더·사용자 판정 경계

- 레지스트리·인덱스·프롬프트 테스트 통과는 데이터 계약이 조립된 증거다.
- 실제 생성 이미지가 구성요소와 게이트를 만족하는지는 별도 렌더 검토가 필요하다.
- 사용자 의도·미감·세계관 적합성은 사용자 판정이며 자동 테스트가 대신할 수 없다.
- 이번 조사에서는 이미지 생성을 수행하지 않았으므로 pixel PASS나 사용자 승인으로 승격하지 않는다.

## 8. 재사용 및 저작권 경계

- 출처에서 추출한 것은 일반적인 형태·관계·공정 차원뿐이다.
- 박물관 소장품의 장식, 원고 도식, 작품 구도, 고유 캐릭터, 문장, 사진을 복제하지 않는다.
- 모든 후보는 원본 허구 디자인, 무브랜드, 읽을 수 없는 문자, 비지시적 마법을 기본으로 한다.
- 역사적 전승과 현대 장르 관습을 혼동하지 않으며, 출처가 말하지 않은 판타지 자율성은 원본 설계라고 명시한다.

