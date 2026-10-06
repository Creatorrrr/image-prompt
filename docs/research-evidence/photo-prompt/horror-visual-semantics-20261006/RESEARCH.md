# 호러 시각 의미·후보팩 확장 리서치

2026-10-06 KST · 참조 대화: [호러 요소 조사](chatgpt-conversation://6ac3d144-ccfc-83ee-9e05-2f1a96060604)

## 결과와 반영 범위

참조 대화 17절의 표 249행과 본문의 리미널 스페이스 1행을 모두 대조했다. 이를 **250개 의미 카드, 161개 후보 초안, 21개 기존 데이터 인접 매핑, 12개 선택형 묶음, 12개 소유자별 팔레트**로 정리했다. 후보 초안 중 155개는 시각적 실현 제안, 6개는 문화·판본 근거를 더 확인해야 하는 보류안이다.

이 연구의 주요 제안은 **정상 기준 → 국소 이상 → 비교 대상과 소유자 → 관찰 위치 → 혼동 배제 → 이미지 증거**의 구조를 데이터에 추가하는 것이다. 예컨대 “무서운 유령”이라는 라벨을 늘리는 대신, “실제 입은 무표정인데 같은 사람의 거울 속 입만 웃고, 다른 반사 기하는 정상”이라는 비교 계약을 만든다. 이것은 호러의 보편 정의가 아니라 특정 요청에 사용할 수 있는 선택형 실현이다.

활성 원본, source manifest, 검색 인덱스, 후보팩 생성기에는 적용하지 않았다. 문헌 확인, 제안의 구조 검증, 검색 성능, 후보 노출, 최종 이미지 성공은 각각 다른 상태로 기록한다.

- 상세 카드: [SEMANTIC-CARDS.md](SEMANTIC-CARDS.md), [SEMANTIC-UNITS.json](SEMANTIC-UNITS.json)
- 초안: [CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json), [BUNDLE-DRAFTS.json](BUNDLE-DRAFTS.json), [PALETTE-DRAFTS.json](PALETTE-DRAFTS.json)
- 원본 배치와 기존 ID: [RUNTIME-MAPPING.json](RUNTIME-MAPPING.json)
- 실행 순서: [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)
- 출처별 읽기 범위와 한계: [SOURCES.md](SOURCES.md)

## 1. 입력과 근거를 어떻게 확보했는가

대화 도구의 20,000자 제한은 12절 시작에서 본문을 잘랐다. 같은 대화를 로그인된 브라우저에서 열어 17절 끝까지 읽고 모든 표의 키워드와 링크를 추출했다. 입력 전사는 [SEED-INVENTORY.json](SEED-INVENTORY.json), 도구 수신 앞부분은 [REFERENCE-PREVIEW.md](REFERENCE-PREVIEW.md)에 보존했다. 뒤쪽을 추측해서 채우지 않았다.

출처 레코드는 35개다. 본문 일부를 읽은 자료 21개, 초록 확인 3개, 검색 요약 확인 1개, 메타데이터만 확인 6개, 조회 실패 2개, 이번 턴에서 링크만 보존한 자료 1개, 원 대화 1개로 구분한다. **35개 모두를 전문 검증한 것이 아니며, 250개 키워드 전체의 사실 검증도 아니다.** 각 카드의 장면 구성은 독자적으로 작성한 제안이고, 출처가 추천한 장면이라는 뜻이 아니다.

주요 교정 근거는 다음과 같다.

| 확인한 구분 | 근거 | 데이터에 미치는 영향 |
|---|---|---|
| terror와 horror의 구분은 특정 문학적 논의이며, 고딕은 과거·공간·권력·욕망의 관계도 포함한다. | [British Library, John Bowen](https://www.britishlibrary.cn/en/articles/gothic-motifs/) | 고딕 건축·검정 의복·직접 충격을 하나의 hard 정의로 묶지 않는다. |
| uncanny valley는 인간 유사성에 관한 가설이다. | [Mori의 저자 승인 번역, IEEE](https://ieeexplore.ieee.org/document/6213238) | 모든 언캐니를 동일 프로필로 만들지 않고 인간형의 국소 불일치와 일반적인 익숙함의 어긋남을 분리한다. |
| 포크 호러에는 풍경의 고립과 공동체 질서의 위협 관계가 있다. | [BFI, Adam Scovell](https://www.bfi.org.uk/features/where-begin-with-folk-horror) | 들판·꽃·의식 소품보다 주민-방문자-경계-탈출 경로를 먼저 표현한다. |
| 코즈믹 공포는 미지와 자연법칙의 붕괴를 다루는 작가적 이론을 포함한다. | [Lovecraft의 원 에세이](https://www.hplovecraft.com/writings/texts/essays/shil.aspx) | 거대한 괴물이나 촉수 외형만으로 축소하지 않는다. 이 연구의 반사 불일치는 별도 설계다. |
| 도깨비는 자연물·생활물건의 변신과 변화무쌍한 형상을 포함한다. | [한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0015527) | 망자의 영혼·일본 오니·단일 뿔 외형과 자동 병합하지 않는다. |
| 장산범은 뉴미디어 도시괴담의 연구 대상이다. | [KCI 논문 초록](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002335450) | 고대 전승의 고정 요괴로 승격하지 않고 매체·판본 정보를 연구 sidecar에 둔다. |
| 요괴 회화에는 의인화된 도구·동물이 함께 나타난다. | [Met 소장품 해설](https://www.metmuseum.org/art/collection/search/853224), [Hyogo 역사박물관](https://rekihaku.pref.hyogo.lg.jp/en/digital_museum/ebanashi/sakuhin/ka0014/) | 생활도구 구조와 생명 단서가 이어지는 후보를 작성하되 한국 도깨비의 문화 분류와는 별개로 유지한다. |
| high-key/low-key는 조명 관계이며 깊은 공간과 deep focus는 다른 개념이다. | [Yale: mise-en-scene](https://filmanalysis.yale.edu/mise-en-scene/), [cinematography](https://filmanalysis.yale.edu/cinematography/) | 고노출·저노출·초점 흐림을 의미의 대용물로 사용하지 않는다. |
| diegetic 여부와 화면 안/밖 여부는 다른 축이다. | [Yale: sound](https://filmanalysis.yale.edu/sound/) | 화면 밖 발소리를 비디제틱으로 오분류하지 않고 음향은 정지 이미지 gate에서 분리한다. |
| monstrous-feminine는 젠더와 몸의 괴물화에 관한 비평 개념이다. | [Freud Museum의 Creed 연구 해설](https://www.freud.org.uk/whats-on/on-demand/courses/the-monstrous-feminine/) | 여성·임신·성적 욕망 그 자체를 괴물성으로 자동 분류하지 않는다. |

바디 호러의 변형·붕괴 사례와 에로틱 호러의 매혹·위협·의복 관습은 [BFI body horror](https://www.bfi.org.uk/lists/10-great-body-horror-films), [BFI erotic horror](https://www.bfi.org.uk/lists/10-great-erotic-horror-films)를 확인했다. 상처의 임상 분류나 모든 작품의 필요조건을 검증한 자료로 확대 사용하지 않는다.

## 2. 현재 저장소에서 확인한 빈틈

연구 시점 실제 로더가 읽은 값은 후보 10,089개, 슬롯 112개, 시각 의미 프로필 1,922개, 묶음 후보 990개다. 원본이 여러 extension과 manifest로 구성되고, 인덱스는 sharded manifest를 사용하는 현재 체크아웃 기준이다.

기존 데이터에서 확인한 관련 프로필은 다음과 같다.

| 실제 ID | 이미 보존하는 의미 | 이번 제안에서 구별할 관계 |
|---|---|---|
| `human_ghost_identity_breach` | 생전 정체, 불가능한 현현, 국소 결과, 촬영 혼동 통제 | 거울 속 표정 불일치·추가 인원·부유 발 등 개별 실현은 별도 선택이다. |
| `uncanny_coherence_mismatch` | 인간 유사 기준과 국소 채널 불일치 | 일반 공간의 낯익음 어긋남이나 모든 괴물 얼굴로 넓히지 않는다. |
| `liminal_transition_use_gap` | 유지된 서비스 기능, 기대 사용의 부재, 전이 경계 | 폐허·귀신 복도·어두운 방을 같은 의미로 편입하지 않는다. |
| `phantasmagoria_projected_spectral_sequence` | 장치·광로·받는 면을 가진 유령 환등 공연 | 실제 유령·홀로그램·안개 실루엣과 분리한다. |
| `ghost_ship_former_vessel_breach` | 같은 배의 물질 선체와 유령성 단절 | 일반 난파선이나 안개 낀 빈 배로 대체하지 않는다. |
| `lens_ghosting_flare_alignment` | 광원과 정렬된 광학 고스트 | 유령 출몰의 homonym hard-negative로 보존한다. |
| `pc_pc24_owner_relation` | 국소 광학 위치·색 분리 | 화면의 광학 이상을 초자연 정체로 자동 읽지 않는다. |

위 7개는 **ID·영문·exact term 중심의 제한된 어휘 검색 결과**다. 검색에 잡힌 후보 86개·프로필 7개·묶음 8개를 “전체 호러 데이터의 총량”으로 부르지 않는다. 이외 조명·카메라·색·재질의 재사용 후보는 별도 [REUSE-CRAFT-CATALOG.json](REUSE-CRAFT-CATALOG.json)으로 조사했다. 신규 초안과 기존 원본의 의미상 중복 여부는 반영 전 전체 로더를 대상으로 다시 판정한다.

기존 `appearing_only_in_reflection`와 `reflection_only_apparition_wide_capture`는 현실 공간 부재와 반사에만 있는 현현을 이미 다룬다. **그 반사 현현을 곧바로 표정 불일치로 덮어쓰면 원래 의미가 사라진다.** 두 관계는 인접하지만 별도 계약이다. 동일한 이유로 인접 ID 21개는 동의어 병합 지시가 아니다.

## 3. 강화할 공포 메커니즘

### 3.1 정상 기준과 국소 이상

이미지의 대부분이 정상으로 유지될수록 무엇이 어긋났는지 구체적으로 비교할 수 있다. 이것은 지각 효과의 경험적 보장이 아니라 데이터 실현을 선명하게 만드는 설계 원칙이다.

- 반사: 실제 얼굴·복장·거울 면이 대응하되 반사 속 입 또는 손의 특정 상태만 다르다.
- 그림자: 몸과 그림자의 연결, 광원 방향을 유지하되 그림자의 손 자세만 다르다.
- 도플갱어: 같은 외형 두 인물을 실제 공간에 따로 두고 행동을 다르게 한다. 거울·쌍둥이를 비교 음성으로 둔다.
- 반투명: 뒤 구조가 몸을 통과해 읽히지만 몸 윤곽과 주변 가림 순서는 유지된다.
- 부유: 발과 바닥의 틈, 바닥의 그림자, 지지 구조를 함께 확인한다.
- 사용 부재: 준비된 서비스 공간에 기대 사용자가 없고 최근 사용 흔적이 남는다.
- 공간 모순: 하나의 정상 연결 공간 안에서 경로·인원·방향이 서로 맞지 않는다.
- 기록 모순: 실제 장소와 화면의 촬영 영역·시점 대응을 확보하고 추가 존재나 동작 차이를 둔다.

이 비교 관계는 broad label을 고정 이미지로 번역하는 규칙이 아니다. 사용자가 정확한 관계를 요구했거나 optional 후보를 선택한 경우에만 완전한 증거를 요구한다.

### 3.2 정보의 양보다 접근 가능성

복도·다락·지하실·숲은 장소명만으로 공포를 만들지 않는다. 보이는 출구, 가려진 접근로, 인물과 통로의 거리, 몸이 통과할 여유를 다룬다. 네거티브 스페이스는 빈 영역의 기능과 연결하고, 전경 가림은 필요한 비교 대상까지 지우지 않도록 한다.

딥 포커스로 관객이 뒤쪽 이상을 먼저 보는 관계와, 얕은 심도로 뒤쪽 정체를 읽지 못하는 관계는 서로 다른 선택이다. 한 요청에서 후자의 흐림을 선택하고 전자의 배경 확인 gate를 PASS로 판정할 수 없다.

### 3.3 밝은 호러와 색의 소유자

12개 팔레트의 HEX 값은 원 대화가 구성한 예시를 그대로 전사했다. 이 값의 보편 심리 효과는 검증하지 않았다. 새 제안은 각 색을 **배경·깊이 층·피부·천·금속·광원·화면 면**에 배정하는 것이다.

한 점 적색은 적색의 양과 시선 중심을 제한하고, 따뜻한 촛불은 빛이 닿는 국소 영역과 밖의 차가운 공간을 나눈다. 방송 신호색·노이즈는 모니터 면 안에 유지한다. 밝은 포크 호러는 꽃 색보다 주민-방문자 자리 관계가 먼저다.

### 3.4 얼굴·신체·재질

창백함과 푸른 조명, 눈가 그림자와 안구 변형, 가면과 무안면, 젖은 머리와 검은 덩어리, 반투명 몸과 투명 의복을 혼동하지 않도록 각 요소의 소유자와 경계를 명시했다.

신체 호러는 정상 부위·변형 부위·중간 연결을 다룬다. 기생은 숙주-다른 생물의 접점, 융합은 유기물-금속의 연속 접합, 액화는 몸의 지지 상실과 연결된 풀을 요구한다. 피·절단·참수·박피·내장 노출·부패도 입력에서 제거하지 않았으며 서로 다른 연구 정의와 시각/맥락 범위를 남겼다.

외형에서 실제 건강 상태·죽음의 원인·장애·악의·성적 동의를 추정하지 않는다. 이것은 요청을 덜 표현하는 제약이 아니라, 데이터의 의미를 임의로 바꾸지 않는 경계다.

### 3.5 민속·매체 판본

도깨비·망자의 영혼·일본 요괴·되살아난 시체를 한 ghost 태그로 합치면 주체가 바뀐다. 구미호의 인간 모방과 특정 여우 해부학, 강시의 물질적 몸과 영화 관복·부적·도약을 구분한다. 쿠치사케온나는 [Nichibun의 실제 전승 기록](https://www.nichibun.ac.jp/cgi-bin/YoukaiDB3/simsearch.cgi?ID=0210016)에서도 여러 서술이 변주되므로 무기·대처법을 하나로 합치지 않는다.

처녀귀신·물귀신·유레이·장산범·구울·페낭갈란의 특정 외형 후보 6개는 판본 근거 보류 상태다. 분류 전체를 삭제한 것이 아니라 고정 외형의 live 채택을 유보한 것이다. 총각귀신·객귀·무주고혼 등의 맥락 항목도 유지하고, 고정 외형이 없다면 억지로 subject 후보를 만들지 않는다.

밴시는 죽음의 예고와 울음의 관계이며 [Maynooth 도서관 해설](https://mulibrarytreasures.wordpress.com/2024/10/18/the-tale-of-the-banshee/)을 확인했다. 수면 침입 악령은 [succubus](https://www.merriam-webster.com/dictionary/succubus), [incubus](https://www.merriam-webster.com/dictionary/incubus)의 전승 정의와 연구 맥락으로 보존한다.

### 3.6 욕망·권력·금기의 범위

사이코섹슈얼 호러·흡혈의 매혹·관음·fetish 의복·구속은 성인 주체, 시선·접근·접점·이동 한계로 분해했다. 성적 폭력, 가족 내부 금기, 생식 통제, 네크로필리아, 식인, Eros/Thanatos, monstrous-feminine 등은 분석 범주와 원 정의를 남겼다.

매혹과 강압, 의복 재질과 동의, 애도와 시체 대상 욕망은 서로 대체하지 않는다. 비평 용어를 optional 장식 후보로 만들지 않는다. 연구 정의를 보존하는 일과 실제 이미지 실현·API 실행·출력 판정은 따로 진행한다.

### 3.7 정지 이미지가 증명하지 못하는 항목

오래 멈춤, 경련, 역방향 이동, 관절별 지연, 반사 지연, 플리커, rack focus, long take, jump cut, jump scare, slow burn, 소리와 입 모양의 불일치는 시간 증거가 필요하다. 정지 이미지의 잔상이나 열린 입은 이 과정을 검증하지 않는다.

| 처리 | 의미 카드 수 | 반영 방향 |
|---|---:|---|
| 시각적 실현 제안 | 155 | optional 후보·필요한 구체 관계 profile |
| 기존 인접 데이터 검토 | 21 | 동의어 여부와 원 의도를 먼저 검토 |
| 특정 문화·외형 판본 보류 | 6 | 원형 또는 작품 판본 근거 확보 후 채택 |
| 비시각 맥락 | 19 | definition/contrast 또는 별도 연구 맥락 유지 |
| 비평·자율성·금기 맥락 | 9 | 관계 정의 보존, 자동 장식 선택으로 바꾸지 않음 |
| 시간 과정 | 16 | 영상 순서·동작 설명으로 보존 |
| 소리·음향 과정 | 18 | 음향 데이터와 동기화된 영상 검증으로 보존 |
| 참조 조합 예시 | 6 | 고정 프리셋 대신 12개 선택형 묶음에 대응 |
| 합계 | 250 | 입력 누락 없이 처리 |

음향의 발생원·거리·입력·처리·시간을 따로 보존하고, 정지 이미지에는 필요한 경우 종의 타종 상태·보이는 라디오·듣는 인물의 시선 등 **다른 시각 후보**를 제안한다. 대체 시각 단서가 실제 소리의 성공 증거는 아니다.

## 4. 데이터 구조 제안

연구 JSON은 runtime 스키마가 아니다. 원본으로 옮길 때 다음처럼 투영한다.

1. 넓은 개념은 정의·문맥·contrast로 보존한다. 후보와 인덱스 검색 결과는 advisory다.
2. 구체적인 관계는 짧은 `concept_units`와 방향 있는 `relations`로 나눈다. owner와 property 검토 정보는 별도 계획 metadata에 두며 unsupported 키를 runtime에 넣지 않는다.
3. hard 의미의 근거는 원 요청·정확한 definition·frozen assertion 또는 선택된 opt-in 계약이다. “호러/무섭다/유령”만으로 새 관계를 전부 활성화하지 않는다.
4. 공동 비교 증거는 `photo-authored-visual-components/v2`의 단일 또는 결합 obligation으로 작성한다. source에는 생성형 `required_evidence_fields`나 `render_gates`를 중복 작성하지 않는다.
5. 선택형 묶음은 선택했을 때 모든 멤버·관계를 보존한다. associated profile이 자동으로 hard 권한을 얻지 않는다.
6. 원문·저자·URL·문화/매체 판본·조회 실패·research status는 이 evidence 디렉터리에 둔다. retired runtime metadata 키를 다시 도입하지 않는다.

[PROFILE-PROTOTYPES.json](PROFILE-PROTOTYPES.json)에는 거울 표정 불일치·독립된 그림자 자세·공동체 경계의 v2 compiler 예시 3개를 작성했다. compiler projection 검증은 실제 registry 유효성·검색·후보팩 선택·이미지 성공을 의미하지 않는다.

## 5. 검증과 다음 반영 순서

구조 검증은 seed-의미-candidate-bundle 연결, 중복 ID, source ID, 현재 기존 ID, 후보 entry의 연구 정보 혼입, v2 compiler projection, 기존 파일 해시 보존을 확인한다. 실행 결과는 [VALIDATION.json](VALIDATION.json)에 기록한다.

검증 중 기존 파일 7개가 시작 시점과 다른 해시로 바뀌었고, authored assets와 인덱스는 같은 해시였다. 새 연구 디렉터리 외에는 이 작업에서 파일을 작성하지 않았다. 변경 감지 범위와 후속 대조 조건은 [SOURCE-DRIFT-NOTE.md](SOURCE-DRIFT-NOTE.md)에 남겼다. 구조 검증 통과를 모든 기존 파일의 불변 증명으로 보고하지 않는다.

[REGRESSION-PLAN.json](REGRESSION-PLAN.json)은 데이터에서 만든 개발 검증 728건과 전역 혼동 통제 14건의 **계획**이다. 독립 holdout은 아직 0건이며 742건이 PASS한 상태가 아니다. 영어 component 문장을 그대로 사용한 개발 query는 독립 일반화 증거로 계산하지 않는다.

[PIXEL-QUALIFICATION-PLAN.json](PIXEL-QUALIFICATION-PLAN.json)은 22개 원본 이미지 검증 그룹이다. render 0회다. 비교 대상이 함께 보이지 않으면 UNOBSERVABLE_NOT_PASS, 부분 충족은 실패, 생성 차단은 BLOCKED_UNSCORED로 기록한다. 한 장의 기묘한 분위기를 데이터 전체의 성공으로 확대하지 않는다.

권장 순서는 **기존 의미 보존·중복 정리 → 거울/그림자/기록/신체 연결 같은 구체 관계 → 조명·색·공간 조합 → 문화 판본 확보 → 검색·선택·이미지 검증**이다. 실제 파일과 완료 조건은 반영 계획에 명시했다.
