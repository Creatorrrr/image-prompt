# 욕망 개념군 시각 의미·후보팩 강화 리서치

- 조사일: 2026-09-01
- 참조 대화: `욕망 관련 개념 조사` (`6a96aa3f-6878-83ee-84c8-b5c6ab7ac451`)
- 대상: `photo-prompt-image-generator`의 시각 의미 계약과 후보팩 데이터
- 결정 상태: 연구 완료, 런타임 적용 전 제안
- 적용 상태: 미적용. 이 문서는 런타임 레지스트리·인덱스·생성기를 수정하지 않는다.
- 검증 경계: 문헌 근거와 저장소 중복·공백을 확인했다. 프롬프트 생성, 이미지 렌더, 픽셀 판정, 사용자 판정은 아직 수행하지 않았다.

## 1. 결론

욕망 개념군을 하나의 `desire expression`이나 응시·미소·붉어진 얼굴로 묶으면 안 된다. 욕망은 대체로 눈에 직접 보이는 표정이 아니라, **무엇을 향하는지, 현재 접근 가능한지, 어떤 행동을 하는지, 무엇과 충돌하는지, 어떤 결과가 생기는지**를 통해 제한적으로 관찰할 수 있는 관계·사건이다.

후보팩의 기본 단위는 다음 사건 사슬이어야 한다.

```text
식별 가능한 대상 또는 목표
→ 현재 접근·소유·분배·통제 상태
→ 동일 인물의 접근·획득·저항·제시·재분배 행동
→ 장벽·소유자·청중·장기 목표·피영향자
→ 즉시 보이는 성공·차단·불균형·반응·잔여물
```

이번 연구는 이 원칙으로 즉시 후보화할 수 있는 P0 시각 계약 9개를 제안한다.

1. `inaccessible_target_longing_relation`
2. `temptation_goal_conflict_choice`
3. `repeated_acquisition_without_use_cycle`
4. `excess_accumulation_overflow_event`
5. `other_owned_object_covetous_approach`
6. `pleonexia_unfair_share_taking_event`
7. `public_recognition_bid_audience_response`
8. `next_milestone_ambition_pursuit`
9. `resource_control_acquisition_event`

범용 키워드 `욕망`, `desire`, `greed`, `longing`, `ambition`, `power`, `obsession`만으로는 이 계약들을 강제하지 않는다. 정확하고 사건적인 구문만 hard activation 후보이며, BM25F·임베딩 유사도만으로 찾은 프로필은 advisory로 남긴다.

## 2. 참조 대화 키워드의 의미군 재분류

참조 대화의 한·영 키워드를 그대로 동의어 목록으로 사용하지 않고, 장면에서 검증 가능한 구조가 같은지에 따라 다시 분류했다.

| 의미군 | 대표 키워드 | 시각화 판단 |
|---|---|---|
| 중립적 바람 | 욕구, 욕망, 바람, 소망, need, want, desire, wish | 너무 넓다. hard profile 금지 |
| 접근 불가능한 대상 | 열망, 갈망, 갈구, longing, yearning, Sehnsucht | 대상·거리·장벽·불완전 접근이 명시될 때만 후보화 |
| 보상 접근과 갈등 | 욕동, 충동, craving, appetite, urge, impulse, temptation | 보상 단서와 상충 목표, 저항 또는 실행 결과가 함께 보일 때만 후보화 |
| 획득·축적 | 물욕, 소유욕, 축적욕, 탐심, 탐욕, greed, avarice, acquisitiveness, insatiability | 성격 판정 금지. 반복 획득·미사용·용량 초과 같은 사건으로만 후보화 |
| 타인의 몫 | 선망, covetousness, cupidity, pleonexia | 소유 경계 또는 분배 규칙과 침범 행동이 명시될 때만 후보화 |
| 인정·지위 | 인정욕, 명예욕, 과시욕, 허영, status seeking | 청중에게 제시하는 행동과 청중의 독립 반응이 필요 |
| 성취·확장 | 성취욕, 야심, 야망, ambition, striving | 구체적 다음 목표·진척·현재 행동이 필요. 성공 후 기쁨과 분리 |
| 권력·통제 | 권력욕, 지배욕, 통제욕, 정복욕, power seeking | 자원·접근권의 통제권을 얻는 사건과 피영향자가 필요. 포즈·키 차이 금지 |
| 쾌락·성적 접근 | 쾌락욕, 탐닉, 욕정, lust, kāma | 즐거움은 욕망과 다르다. 성인 대상 행동은 기존 제한 프로필 재사용 |
| 집착·임상 용어 | 집착, 강박, obsession, fixation, compulsion | 정지 이미지에서 임상 상태나 성격을 추론하지 않는다. broad hard route 금지 |
| 철학·종교 계보 | conatus, epithymia, taṇhā, lobha | 정의·연구 계보용. 종교 도상이나 성격 표지를 자동 삽입하지 않는다 |
| 결과 상태 | 보상, 충족, 만족, 지족, liking, satisfaction | 욕망 그 자체가 아니라 결과·평가 상태. 관찰 가능한 수용·중단·공유 행동으로 별도 연구 |

### 2.1 전체 키워드 커버리지

아래 표는 참조 대화의 압축 키워드와 10개 원형을 누락 없이 구현 경로에 배치한 것이다. 같은 행에 있다는 이유만으로 런타임 동의어로 등록하지 않는다.

| 처리 | 한글 키워드 | 외국어·철학 키워드 | 제안 경로 |
|---|---|---|---|
| broad advisory | 욕구, 욕망, 욕심, 바람, 소망 | Need, Want, Desire, Wish | 장면 대상·관계가 추가될 때까지 hard profile 없음 |
| broad advisory + 좁은 접근 불가 사건 | 열망, 갈망, 갈구 | Longing, Yearning | `inaccessible_target_longing_relation`은 정확 사건 구문만 |
| broad advisory + 목표 갈등 사건 | 욕동, 충동, 동기, 유혹 | Appetite, Drive, Urge, Impulse, Craving | `temptation_goal_conflict_choice`는 보상·상충 목표·결과가 모두 있을 때만 |
| 도메인별 구체화 | 생존욕, 애정욕 | Need, appetite | 음식·물·쉼터 또는 성인 관계처럼 실제 대상이 지정된 기존/향후 프로필 사용 |
| 기존 프로필 재사용 | 욕정 | Lust | 성인 대상의 관찰 가능한 유혹 행동만 `target_directed_seductive_display`; 사적 욕망·동의 추론 금지 |
| P1 보류 | 쾌락욕, 탐닉 | Kāma | 즐거움 결과와 접근 욕망을 분리한 도메인별 사건 연구가 먼저 필요 |
| broad advisory + 다음 이정표 사건 | 야심, 야망, 성취욕, 확장욕, 초월욕 | Ambition | `next_milestone_ambition_pursuit`은 이전 완료·다음 목표·현재 진척이 있을 때만 |
| P1 보류 | 승부욕, 경쟁심, 우월욕 | competition, superiority striving | 동일 기준·경쟁 규칙·현재 점수·후속 행동을 분리한 연구 필요 |
| broad advisory + 청중 인정 사건 | 인정욕, 명예욕, 허영, 과시욕 | status seeking, vanity | `public_recognition_bid_audience_response`; 실제 사회적 지위 판정 금지 |
| broad advisory + 획득/용량 사건 | 물욕, 소유욕, 축적욕, 독점욕, 탐심, 탐욕, 과욕 | Greed, Avarice, Acquisitiveness, Rapacity, Insatiability | `repeated_acquisition_without_use_cycle` 또는 `excess_accumulation_overflow_event`은 정확 사건 구문만 |
| broad advisory + 소유 경계 사건 | 선망 | Covetousness, Cupidity | `other_owned_object_covetous_approach`; 응시만으로 활성화 금지 |
| broad advisory + 분배 침범 사건 | 과욕, 탐욕 | Pleonexia | `pleonexia_unfair_share_taking_event`; 분배 규칙·타인의 부족이 함께 보여야 함 |
| broad advisory + 자원 통제 사건 | 권력욕, 지배욕, 통제욕, 정복욕 | power seeking, domination, control, conquest | `resource_control_acquisition_event`; 포즈·제복·높이만으로 활성화 금지 |
| P1 보류 | 질투, 선망, 결핍 | envy, jealousy, lack | 비교 기준, 기존 관계, 상실 위협, 건설적/악의적 후속 행동을 분리한 연구 필요 |
| hard profile 금지 | 집착, 강박 | Obsession, Fixation, Compulsion | 임상·성격 판정 금지. 반복 획득 사건과도 분리 |
| 결과 상태·별도 연구 | 보상, 충족, 만족, 지족 | reward, fulfillment, satisfaction, contentment | 결과 수용·중단·공유 같은 보이는 행동으로 별도 설계 |
| 계보만 유지 | 해당 없음 | Epithymia, Taṇhā, Lobha, Conatus | citation/advisory only. 자동 도상·인물형·hard profile 없음 |

## 3. 근거가 지지하는 핵심 구분

### 3.1 욕망은 표정보다 대상 지향적 행동 경향에 가깝다

Stanford Encyclopedia of Philosophy의 욕망 개관은 행동 기반 설명을 주요 이론군으로 다루되, 행동만으로 욕망 전체를 환원할 수 없다는 한계도 함께 설명한다. 따라서 사진 한 장에서는 내적 욕망을 선언하지 않고, **대상 지향 행동과 상황 관계가 실제 픽셀에 존재하는 범위**만 계약해야 한다.

- 근거: [Stanford Encyclopedia of Philosophy, Desire](https://plato.stanford.edu/entries/desire/)
- 데이터 함의: `yearning expression`, `greedy eyes`, `ambitious look` 같은 얼굴 라벨은 hard profile이 될 수 없다.

### 3.2 wanting, liking, learning은 같은 것이 아니다

Berridge·Robinson·Aldridge는 보상 과정에서 cue-triggered `wanting`, hedonic `liking`, learning을 구분한다. 어떤 대상을 다시 획득하려는 행동이 그 대상을 실제로 즐기는 장면과 같지 않을 수 있다.

- 근거: [Berridge, Robinson & Aldridge, 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2756052/)
- 데이터 함의: 새 대상을 획득하면서 이전 동일 대상이 미개봉·미사용으로 남은 사건은 `wanting ≠ liking`의 제한적 시각 대리물이 될 수 있다. 이것을 중독이나 성격으로 판정해서는 안 된다.

### 3.3 유혹은 강한 욕망이 아니라 목표 갈등 사건이다

Hofmann 등은 일상 욕망을 욕망 강도, 다른 목표와의 충돌, 저항, 행동 실행으로 나누어 기록했다. 후보팩에서 `temptation`을 단순 음식 클로즈업이나 매혹적인 표정으로 표현하면 갈등 구조가 사라진다.

- 근거: [Hofmann et al., Everyday Temptations](https://doi.org/10.1037/a0026545)
- 데이터 함의: 즉시 보상 단서와 장기 목표 표지, 같은 인물의 멈춘 선택 행동, 저항 또는 실행 결과가 함께 필요하다.

### 3.4 얼굴만으로 내적 상태를 고정하지 않는다

Goel 등의 연구에서 감정 추론은 얼굴 단독보다 상황 단서에 크게 의존했다. 이 결과를 특정 욕망 장면의 직접 검증으로 과장할 수는 없지만, 얼굴 라벨을 hard evidence로 쓰지 말아야 한다는 경계 근거가 된다.

- 근거: [Goel et al., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10948792/)
- 데이터 함의: 모든 제안 프로필은 표정을 optional detail로만 취급하고, 사건의 필수 구성요소에는 넣지 않는다.

### 3.5 권력과 지위는 다른 관계다

권력 연구는 권력을 가치 있는 자원이나 처벌·보상을 제공하거나 보류해 타인의 상태를 바꿀 수 있는 상대적 능력으로 설명한다. 반면 지위는 타인의 눈에 비친 존중·위신과 연결된다.

- 근거: [Keltner, Gruenfeld & Anderson, 2003](https://doi.org/10.1037/0033-295X.110.2.265), [Magee & Galinsky, 2008](https://doi.org/10.5465/19416520802211628)
- 데이터 함의: `public_recognition_bid_audience_response`에는 청중 반응이, `resource_control_acquisition_event`에는 자원·통제자·피영향자가 필요하다. 왕좌·낮은 카메라·키 차이는 어느 쪽도 단독 증거가 아니다.

### 3.6 야심은 성공 후 표정이 아니라 다음 목표를 향한 진행이다

목표 설정 연구는 구체적이고 도전적인 목표, 목표 몰입, 피드백, 노력과 지속을 핵심 메커니즘으로 다룬다.

- 근거: [Locke & Latham, 2006](https://doi.org/10.1111/j.1467-8721.2006.00449.x)
- 데이터 함의: 기존 `achievement_reward_smile`은 성공 후 결과 프로필로 유지하고, 야심 후보는 완료 이정표·다음 이정표·진척 피드백·현재 행동을 보여야 한다.

### 3.7 탐욕·과욕은 얼굴이 아니라 “충분함 이후의 추가 획득” 사건이다

탐욕 연구는 더 많이 원함과 충분하지 않다는 불만족을 중심으로 개념을 정리하지만, 이는 사람의 성향을 사진에서 판독해도 된다는 뜻이 아니다. 고전적 `pleonexia`는 특히 정당한 몫보다 더 많이 취하는 분배 관계로 좁힐 수 있다.

- 근거: [Greed review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10903135/), [Aristotle, Nicomachean Ethics, Book V](https://classics.mit.edu/Aristotle/nicomachaen.5.v.html)
- 데이터 함의: 용량 초과, 미사용 중복, 타인의 할당분 침범처럼 **규칙과 결과가 보이는 사건**만 후보화한다. `greedy person`이라는 성격 라벨은 출력하지 않는다.

### 3.8 임상적 집착·강박은 정지 이미지로 판정하지 않는다

NIMH는 OCD의 강박사고를 침투적·원치 않는 생각, 강박행동을 반복적이고 시간 소모적이거나 고통을 유발하는 행동으로 설명한다. 한 장면의 반복 배열이나 강한 응시만으로 이 시간적·임상적 기준을 입증할 수 없다.

- 근거: [NIMH, Obsessive-Compulsive Disorder](https://www.nimh.nih.gov/health/publications/obsessive-compulsive-disorder-when-unwanted-thoughts-or-repetitive-behaviors-take-over)
- 데이터 함의: `obsession`, `compulsion`, `OCD`는 hard profile을 활성화하지 않는다. 반복 획득 장면도 임상 진단과 분리한다.

### 3.9 철학·종교 용어는 시각 프리셋이 아니다

`conatus`, `epithymia`, `taṇhā`는 서로 다른 철학·종교 전통의 개념이다. 각 출처는 계보와 정의를 설명하지만, 특정 의상·상징·인종·종교 도상으로 번역하라는 근거를 제공하지 않는다.

- 근거: [SEP, Spinoza's Psychological Theory](https://plato.stanford.edu/entries/spinoza-psychological/), [Plato, Republic Book IV](https://classics.mit.edu/Plato/republic.5.iv.html), [SuttaCentral, Taṇhā Sutta](https://suttacentral.net/an4.199/en/sujato)
- 데이터 함의: 이 용어들은 citation lineage와 advisory retrieval에만 남기고, hard visual profile이나 자동 종교 도상을 만들지 않는다.

## 4. 현재 저장소의 재사용 지점과 공백

| 기존 항목 | 재사용 범위 | 재사용하면 안 되는 범위 |
|---|---|---|
| `achievement_reward_smile` | 성공 결과, 결과 지향 시선, 성공 후 후속 흔적 | 야심·성취욕의 진행 장면 전체 |
| `target_directed_seductive_display` | 성인 대상이 분명한 유혹 행동과 즉시 반응 | 동의·사적 의도·성적 욕망의 내면 판정 |
| `yandere_affection_control_relation` | 정확한 yandere 원형의 애정 표면+경계 침범 | 일반 집착, 소유욕, OCD, 질투 |
| `decadent_languor_environment` | 닳은 사치, 사건 잔여물, 미완 행동 | 쾌락주의·탐닉·욕망 일반 |
| `conspicuous_original_house_code_display` | 문자 없는 독창 표장과 사치품의 공개적 두드러짐 | 인정욕·지위 추구 관계 전체 |
| `quiet_yearning` 후보 | 약한 분위기 보조 | 대상 없는 표정만으로 `longing` 충족 |
| `multi_observer_recognition_cue`, `press_lens_attention_cluster`, `crowd_path_opening_for_subject` | 인정·지위 장면의 청중 반응 | 힘·권력·우월성 판정 |
| `security_verify_credential_control_gate`, `security_credential_reader_entry_log_set`, `controlled_facility_access_lobby` | 접근 통제의 구체적 소품·공간 | 권력욕 일반 또는 직업적 경비 업무를 권력 추구로 판정 |

현재 가장 큰 공백은 다음과 같다.

- 욕망 대상과 접근 장벽을 함께 고정하는 계약이 없다.
- `wanting`과 `liking`의 차이를 사건으로 표현하는 후보가 없다.
- 유혹의 목표 갈등과 저항 단계를 표현하는 후보가 없다.
- 탐욕·과욕·소유욕을 성격 표정이 아닌 획득·축적 사건으로 제한하는 계약이 없다.
- 지위 추구와 권력 획득을 서로 다른 관계로 고정하는 계약이 없다.
- 성공 결과와 다음 이정표 추구를 분리하는 계약이 없다.
- `pleonexia`를 공평한 분배선의 침범 사건으로 제한하는 계약이 없다.

## 5. P0 시각 의미 계약

아래의 필수 그룹은 모두 `literal components → confusion negatives → render gates` 순서로 설계한다. 한 그룹이라도 픽셀에서 확인되지 않으면 partial fail이다.

### P0-1. `inaccessible_target_longing_relation`

**의미 범위**  
현재 접근할 수 없는 구체적 대상·사람·장소를 향한 제한적 longing 사건. 내적 감정 자체가 아니라 대상, 장벽, 미완 접근을 표현한다.

**필수 구성요소**

1. 동일 프레임에서 식별 가능한 목표 대상 또는 대상의 연속성 단서
2. 목표와 인물을 분리하는 물리적·절차적 장벽 또는 명백한 거리
3. 인물의 대상 지향 접근 행동: 손을 뻗음, 막힌 진입 시도, 닫히는 출발 지점으로 이동
4. 접근 실패나 지연의 즉시 결과: 닫힌 문, 떠나는 교통수단, 손이 닿지 않는 틈

**혼동 금지**

- 창밖을 보는 쓸쓸한 인물
- 대상 없는 슬픈 표정·향수·기다림
- 장례·상실·이별로 자동 해석되는 장면
- 단순히 먼 풍경을 감상하는 인물

**정확 활성 구문 예시**

- `an adult reaching toward a clearly inaccessible target across a closing barrier`
- `접근할 수 없는 대상을 향해 막힌 채 손을 뻗는 성인`

`longing`, `yearning`, `갈망` 단독은 advisory다.

### P0-2. `temptation_goal_conflict_choice`

**의미 범위**  
즉시 보상과 더 장기적인 목표가 같은 순간에 충돌하고, 동일 인물이 저항하거나 실행하는 사건.

**필수 구성요소**

1. 즉시 보상 단서
2. 상충하는 장기 목표를 나타내는 구체적 도구·진척물·약속 표지
3. 두 경로 사이에서 멈추거나 한쪽으로 움직이는 동일 인물의 손·몸 행동
4. 두 경로를 동시에 수행하기 어려운 공간·시간 구성
5. 저항 또는 실행의 즉시 결과

**혼동 금지**

- 단순한 메뉴 선택이나 두 상품 비교
- 음식 또는 사치품 단독 클로즈업
- 유혹적인 얼굴·성적 포즈
- 장기 목표 표지 없이 망설이는 사람

**정확 활성 구문 예시**

- `a visible immediate reward conflicting with the same adult's marked long-term goal, with resistance or enactment shown`
- `즉시 보상과 표시된 장기 목표가 충돌하고 저항 또는 실행이 보이는 선택 사건`

### P0-3. `repeated_acquisition_without_use_cycle`

**의미 범위**  
이미 획득한 동일 계열 대상이 미개봉·미사용 상태인데 같은 인물이 또 하나를 획득하는 단일 사건. 반복적 wanting의 관찰 가능한 대리물이며 중독·강박 진단이 아니다.

**필수 구성요소**

1. 동일 계열의 이전 획득물 여러 개
2. 이전 획득물의 미개봉·미사용 상태
3. 같은 인물이 새 동일 계열 대상을 결제·수령·포장하는 현재 행동
4. 이전 획득물과 새 획득물을 한 관계로 읽게 하는 깊이·동선 연결
5. 보관 공간·주의·사용의 불균형을 보여 주는 즉시 결과

**혼동 금지**

- 상점 재고, 창고 업무, 촬영 소품 관리
- 합리적 비축, 재난 대비, 공동구매
- 수집품을 정리·감상·사용하는 장면
- 반복 배열만으로 OCD·중독·탐욕을 진단

### P0-4. `excess_accumulation_overflow_event`

**의미 범위**  
명시된 저장·사용 용량이 이미 충족된 뒤에도 추가 자원이 들어와 넘침·밀려남이 발생하는 사건.

**필수 구성요소**

1. 경계가 보이는 저장·사용 용량
2. 이미 충분히 채워진 기존 자원
3. 동일 인물의 추가 투입·반입 행동
4. 넘침, 떨어짐, 다른 필수품의 밀려남 중 하나
5. 추가 획득과 용량 초과가 한 인과선으로 보이는 구도

**혼동 금지**

- 정상적인 팬트리 보충
- 이사·재고 조사·아카이브 작업
- 풍성함을 보여 주는 정물
- 빈곤·재난 대비를 과욕으로 오독

### P0-5. `other_owned_object_covetous_approach`

**의미 범위**  
타인 소유가 명확한 단일 대상에 대해 다른 인물이 공개적인 청구·교환 제안·경계 침범을 시도하고 소유자가 반응하는 사건.

**필수 구성요소**

1. 단일 핵심 대상
2. 기존 소유자를 명확히 하는 착용·보관·손의 접촉·소유 맥락
3. 다른 인물의 대상 지향 청구·교환 제안·손 뻗기 행동
4. 소유자의 보호·거절·고려 등 즉시 반응
5. 두 인물과 대상의 소유 경계가 읽히는 삼각 구도

**혼동 금지**

- 눈길만으로 선망·질투를 판정
- 선물 전달, 정상적 구매, 공동 사용
- 자신의 물건을 감상하는 소유자
- 경계 침범만으로 절도·범죄를 단정

### P0-6. `pleonexia_unfair_share_taking_event`

**의미 범위**  
동일 분배 시스템에서 표시된 자기 몫을 넘어 타인의 할당분을 가져가 즉시 불균형을 만드는 사건.

**필수 구성요소**

1. 하나의 분배 시스템과 서로 구분되는 동등·지정 몫
2. 각 몫의 수령자 또는 수혜 관계
3. 한 인물이 자기 경계를 넘어 추가 몫을 이동시키는 현재 행동
4. 다른 몫에 생긴 빈자리·부족·차단
5. 침범 행동과 피해 몫이 한 화면에서 연결되는 구도

**혼동 금지**

- 배분 담당자의 실수
- 합의된 재분배·기부·양보
- 동일 인물이 여러 사람 몫을 운반하는 업무
- 단순히 큰 몫을 가진 인물

### P0-7. `public_recognition_bid_audience_response`

**의미 범위**  
인물이 자신의 작업·성과·역할 표지를 특정 청중에게 공개하고, 청중의 독립적인 주의·인정 반응과 즉시 결과가 생기는 사건. 지위 추구의 제한적 장면이며 내적 허영을 판정하지 않는다.

**필수 구성요소**

1. 인물과 인물이 제시하는 구체적 작업·성과·역할 표지
2. 해당 인물의 공개·입장·발표 행동
3. 식별 가능한 다수 청중의 서로 독립적인 시선·렌즈·길 열기·환영 반응
4. 주목, 입장 허용, 시상, 소개 중 하나의 즉시 결과
5. 제시 행동이 청중 반응의 원인으로 읽히는 구도

**혼동 금지**

- 우연히 배경에 있는 군중
- 인물과 무관한 기자·카메라
- 유명인처럼 보이는 의상이나 낮은 앵글
- 청중 반응 없는 로고·사치품 과시

### P0-8. `next_milestone_ambition_pursuit`

**의미 범위**  
이미 완료한 이정표 뒤에 더 구체적인 다음 목표를 설정하고 현재 행동과 자원을 투입하는 진행 사건.

**필수 구성요소**

1. 완료가 보이는 이전 이정표
2. 구체적으로 구분되는 다음 이정표
3. 현재 진척 피드백
4. 동일 인물의 다음 단계 작업
5. 시간·도구·훈련·재료 중 하나의 실제 투입

**혼동 금지**

- 기존 `achievement_reward_smile`과 같은 성공 후 축하
- 일상적 작업 장면
- 목표 없는 열정적 표정
- 텍스트만 가득한 비가시적 계획표

### P0-9. `resource_control_acquisition_event`

**의미 범위**  
가치 있는 자원이나 접근권의 기존 통제 구조에서, 다른 인물이 통제권을 넘겨받거나 쟁취하려 하고 피영향자의 접근 상태가 즉시 바뀌는 사건.

**필수 구성요소**

1. 가치 있는 구체적 자원·접근권
2. 기존 통제자 또는 통제 시스템
3. 다른 인물의 통제권 청구·이관·탈취 시도
4. 해당 자원에 의존하는 피영향자 또는 경로
5. 허용·보류·차단·재지정 중 하나의 즉시 결과

**혼동 금지**

- 경비원·관리자의 통상 업무
- 합의된 협업 인계
- 왕좌, 제복, 높은 의자, 낮은 앵글만 있는 권력 포즈
- 폭력·정복·지배 성격을 자동 추론

## 6. P1·보류 범위

### P1: 도메인 제약을 추가한 뒤 후보화

| 개념 | 보류 이유 | 다음 연구 조건 |
|---|---|---|
| cue-triggered craving | 단일 이미지가 중독·임상 상태로 과해석되기 쉬움 | 중립적 반복 접근 사건과 임상 금지어 회귀 세트 |
| hedonism / pleasure seeking | 즐거움 결과와 욕망 과정이 쉽게 섞임 | 감각 대상·접근 행동·직전/직후를 분리한 사건 설계 |
| envy / upward comparison | 시선과 표정만으로 악의·결핍을 추론하기 쉬움 | 동일 기준·비교 결과·건설적/악의적 후속 행동 분리 |
| expansion / transcendence | 대상이 추상적이고 종교 도상 편향 가능 | 훈련·학습·탐험처럼 구체적 도메인별 목표 |
| satisfaction / contentment | 내면 상태이며 정지 이미지 증거가 약함 | 획득 중단·충분한 몫 수용·공유 같은 행위 결과 |

### hard profile 금지

- `욕망`, `desire`, `need`, `want`, `wish`, `hope` 단독
- `greed`, `longing`, `ambition`, `power`, `envy`, `jealousy` 단독
- `obsession`, `fixation`, `compulsion`, `OCD`, `addiction` 단독
- `conatus`, `epithymia`, `taṇhā`, `lobha`, `kāma` 단독
- `greedy eyes`, `lustful face`, `ambitious expression`, `powerful pose` 같은 표정·포즈 라벨

## 7. 후보팩 데이터 설계

후보는 프로필의 모든 필수 그룹을 한 항목에 몰아넣지 않고, 각 슬롯에서 서로 보완되도록 구성한다. 다만 단일 후보만 선택돼도 위험한 내면 판정이 생기지 않도록 후보 문구 자체를 관찰 가능한 명사·동작으로 제한한다.

| 프로필 | `action` | `prop` / `location` | `composition` | `social_cue` / `aftermath_trace` |
|---|---|---|---|---|
| inaccessible longing | 닫히는 장벽을 향한 미완 접근 | 투명 장벽, 닫히는 출발 게이트 | 인물–장벽–대상 삼각선 | 닿지 않은 간극 |
| temptation conflict | 보상과 목표 사이의 멈춘 손 | 즉시 보상+장기 목표 도구 쌍 | 상호 배타적 두 경로 | 저항 후 남은 보상 또는 실행 후 멈춘 진척 |
| acquisition without use | 미사용 중복을 두고 새 항목 수령 | 미개봉 동일 계열 묶음 | 과거 획득–현재 인물–새 획득 깊이선 | 개봉·사용 흔적 부재 |
| overflow accumulation | 가득 찬 용기에 추가 투입 | 명확한 용량 경계 | 추가 투입과 넘침의 한 인과선 | 떨어짐·밀려남 |
| covetous approach | 타인 소유물에 청구·교환 제안 | 소유자 접촉이 분명한 물건 | 행위자–물건–소유자 삼각선 | 소유자의 보호·거절 |
| pleonexia | 할당선 너머 몫을 이동 | 표시된 동일 몫 세트 | 위에서 읽히는 분배 경계 | 타인 몫의 빈자리 |
| recognition bid | 결과물 공개·입장·발표 | 작업·성과·역할 표지 | 발표자–결과물–청중 반응 호 | 다중 시선, 렌즈, 길 열기 |
| ambition pursuit | 완료 표시 뒤 다음 단계 작업 | 문자 없는 이정표·진척 보드 | 과거–현재–다음 진행축 | 갱신된 진척 흔적 |
| resource control | 접근 토큰 청구·재지정 | 통제 토큰·자원 배분 장치 | 자원–통제자–피영향자 축 | 허용·보류·차단 결과 |

### 후보 작성 규칙

1. 실재 상표·로고·문자 판독에 의존하지 않는다.
2. `greedy`, `obsessed`, `powerful`, `lustful` 같은 성격·내면 형용사를 후보 문구에 넣지 않는다.
3. `same adult`, `same allocation system`, `clearly other-owned`, `visible capacity boundary`처럼 관계를 명시한다.
4. 세부 소품이 작은 경우 해당 세부를 프레임의 전용 가시 영역에 둔다.
5. 인물 표정은 선택적 보조 신호이며 필수 그룹을 대체하지 않는다.
6. 장면의 윤리적·법적 판단, 정신건강 상태, 동의, 사적 의도는 출력하지 않는다.

## 8. 활성화 정책

### 정확·문맥 활성화

hard profile은 다음을 모두 만족할 때만 후보가 된다.

- 구문이 특정 사건을 명시한다.
- 프로필 필수 그룹을 프롬프트에서 실제로 배치할 수 있다.
- 다른 기존 프로필과 충돌하지 않는다.
- 성인 관계가 필요한 경우 성인임이 명시된다.
- broad keyword가 아니라 프로필 소유의 관계어가 존재한다.

### advisory retrieval

- broad alias hit
- BM25F hit
- embedding similarity hit
- 철학·종교 계보 용어
- 임상·성격 용어
- 표정·포즈만 있는 구문

이 경우 후보는 검색 힌트로만 사용할 수 있고, 런타임 hard obligation을 추가하지 않는다.

### 충돌 우선순위

1. 안전·연령·비동의 추론 금지
2. exact relationship profile
3. exact event profile
4. 기존 구체 프로필 재사용
5. broad alias advisory
6. BM25F·embedding advisory

## 9. 회귀 테스트 설계

각 프로필은 최소 `좁은 양성 2 + broad 음성 2 + 혼동 음성 3 + 검색 경로 2`를 가진다.

### 공통 판정

- exact narrow positive: 기대 프로필 하나만 hard activation
- broad keyword: hard activation 0
- BM25F-only: optional suggestion, hard activation 0
- embedding-only: optional suggestion, hard activation 0
- unrelated existing profile: 변화 없음
- 임상·철학 용어: auto visual profile 0

### 핵심 혼동 쌍

| 목표 | 반드시 실패해야 하는 혼동 장면 |
|---|---|
| inaccessible longing | 창밖을 보는 슬픈 초상, 먼 풍경 감상, 일반 대기 |
| temptation conflict | 일반 상품 비교, 메뉴 선택, 보상 단독 클로즈업 |
| acquisition without use | 상점 재고, 업무용 비축, 사용 중인 컬렉션 |
| overflow accumulation | 정상 팬트리 보충, 재난 대비, 이사 박스 |
| covetous approach | 선물 교환, 소유자의 자기 물건 감상, 정상 구매 |
| pleonexia | 합의 재분배, 배분 실수, 여러 몫 운반 업무 |
| recognition bid | 우연한 군중, 인물과 무관한 기자, 사치품 단독 |
| ambition pursuit | 성공 축하, 일상 업무, 목표 없는 결연한 표정 |
| resource control | 통상 접근 관리, 협업 인계, 왕좌·제복 포즈 |

구체 입출력 회귀 사례는 `candidate-data-proposal.json`에 구조화했다.

## 10. 픽셀 평가 계약

프롬프트 문자열과 런타임 활성화가 맞아도 픽셀에서 필수 관계가 읽히지 않으면 통과가 아니다.

```json
{
  "policy": "partial_is_fail",
  "independent_generation_per_arm": 1,
  "cross_arm_input_reuse": false,
  "prompt_pass_is_pixel_pass": false,
  "runtime_pass_is_pixel_pass": false,
  "user_judgment_is_separate": true
}
```

각 이미지에서 다음을 독립 판정한다.

1. 대상·자원·몫이 실제로 식별되는가
2. 소유·접근·분배·통제 관계가 한 프레임에서 읽히는가
3. 현재 행동의 시작점과 목표점이 보이는가
4. 장벽·청중·소유자·피영향자 같은 상대 항이 보이는가
5. 차단·저항·넘침·빈자리·허용 같은 즉시 결과가 보이는가
6. 필수 세부가 너무 작거나 가려지지 않았는가
7. 금지한 표정·포즈 대체물만 남지 않았는가

한 차원이라도 실패하면 해당 arm 전체를 fail로 기록한다. 수정은 실패한 가시 차원만 대상으로 하며, 다른 arm의 이미지나 프롬프트를 입력으로 재사용하지 않는다.

## 11. 구현 순서 제안

1. P0 9개 중 먼저 `temptation_goal_conflict_choice`, `pleonexia_unfair_share_taking_event`, `public_recognition_bid_audience_response` 세 개를 독립 arm으로 프로토타입한다. 서로 다른 구조(내적 갈등의 외화, 분배 침범, 청중 관계)를 검증하기 좋다.
2. 각 프로필에 정확 구문과 broad 음성 회귀를 먼저 추가한다.
3. 후보 확장 파일에 관찰 가능한 후보만 추가하고, 생성 인덱스는 빌드 스크립트로 다시 만든다.
4. 프롬프트·런타임 테스트 통과 후 arm별 한 장을 독립 생성한다.
5. `partial_is_fail` 픽셀 판정을 수행한다.
6. 통과한 프로필만 런타임 레지스트리에 승격하고, 나머지는 연구 제안 상태로 유지한다.

## 12. 출처 목록과 근거 경계

| ID | 출처 | 직접 지지하는 내용 | 지지하지 않는 내용 |
|---|---|---|---|
| S01 | [SEP, Desire](https://plato.stanford.edu/entries/desire/) | 욕망 이론, 행동 경향 설명과 한계 | 특정 사진 구도 |
| S02 | [Berridge et al., 2009](https://pmc.ncbi.nlm.nih.gov/articles/PMC2756052/) | wanting/liking/learning 구분 | 미사용 물건 장면의 직접 검증 |
| S03 | [Hofmann et al., 2012](https://doi.org/10.1037/a0026545) | 욕망 강도·목표 갈등·저항·실행 | 제안한 소품의 직접 검증 |
| S04 | [Goel et al., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10948792/) | 감정 추론에서 상황 단서의 중요성 | 욕망 9개 프로필의 정확도 |
| S05 | [Roberts, Emotions of Absence](https://onlinelibrary.wiley.com/doi/full/10.1111/sjp.12387) | 부재한 대상과 longing의 관계 | 장벽 구도의 직접 검증 |
| S06 | [Greed review](https://pmc.ncbi.nlm.nih.gov/articles/PMC10903135/) | 더 많이 원함·충분하지 않음의 개념 | 개인의 탐욕 성향 판독 |
| S07 | [Aristotle, Ethics V](https://classics.mit.edu/Aristotle/nicomachaen.5.v.html) | 자기 몫보다 더 취하는 분배 문제 | 현대 행동 진단 |
| S08 | [Locke & Latham, 2006](https://doi.org/10.1111/j.1467-8721.2006.00449.x) | 구체 목표·몰입·피드백·지속 | 야심이라는 성격 판독 |
| S09 | [Keltner et al., 2003](https://doi.org/10.1037/0033-295X.110.2.265) | 자원 제공·보류와 상대적 권력 | 왕좌·앵글의 권력 의미 |
| S10 | [Magee & Galinsky, 2008](https://doi.org/10.5465/19416520802211628) | 권력과 지위 구분 | 사진 한 장의 지위 판정 |
| S11 | [Han, Nunes & Drèze, 2010](https://journals.sagepub.com/doi/abs/10.1509/jmkg.74.4.015) | 브랜드 두드러짐과 지위 신호 | 실재 로고 복제, 보편적 허영 판정 |
| S12 | [NIMH, OCD](https://www.nimh.nih.gov/health/publications/obsessive-compulsive-disorder-when-unwanted-thoughts-or-repetitive-behaviors-take-over) | 강박사고·행동의 임상적 시간·고통 경계 | 정지 이미지 진단 |
| S13 | [SEP, Spinoza](https://plato.stanford.edu/entries/spinoza-psychological/) | conatus 개념 계보 | 특정 시각 상징 |
| S14 | [Plato, Republic IV](https://classics.mit.edu/Plato/republic.5.iv.html) | epithymia의 철학적 맥락 | 특정 인물·의상 프리셋 |
| S15 | [SuttaCentral, AN 4.199](https://suttacentral.net/an4.199/en/sujato) | taṇhā의 불교 문헌 계보 | 종교 도상 자동 삽입 |

S01–S15는 개념 구분과 안전 경계를 지지한다. P0의 구체적 카메라 구도·소품 조합은 이 근거를 후보팩의 관찰 가능한 데이터로 번역한 **설계 추론**이며, 아직 이미지 실험으로 검증된 사실이 아니다.
