# 선 표현 조사와 중립적 재서술: 시각 의미·후보팩 강화 연구

2026-10-03 · 연구 및 반영 설계 · 실행 데이터 변경 없음

이번 조사에서 데이터 강화의 중심은 **표현을 구성하는 뜻을 분해하고, 각 뜻의 소유자·관계·관찰 조건·한계를 명시하는 것**이다. 형태어는 기존 신체 계약에 연결하고, 시선·표정은 현재 행동과 인상 평가를 분리하며, 장르·역할·동의·이력은 요청이 알려 준 맥락에 남겨야 한다. 중립적 문장으로 바꾸면서 원문에 없는 체형이나 동기를 채우면 데이터가 풍부해지는 대신 의미가 바뀐다.

이 문서의 시각 구성요소·후보 정의·검증 기준은 연구자가 설계한 제안이다. 외부 자료는 해당 어휘·개념의 범위를 뒷받침한다. 외부 사전이나 논문이 이 저장소의 프로필, 검색 결과, 이미지 성공을 검증한 것으로 취급하지 않는다.

## 1. 조사 범위와 근거

참조한 대화는 [선 표현 조사 and neutral descriptions](chatgpt-conversation://6abf91b4-b870-83ee-b77e-49f3bd1387b9)이다. 제목의 ‘선’ 때문에 선화·윤곽선 기법으로 추정하지 않고 실제 두 턴을 읽었다. 첫 요청은 성적·비하적 언어, 성인 소설·커뮤니티 용어와 중립적 재서술이고, 후속 요청은 외모·육체 형태 표현에 집중한다.

| 조사 산출물 | 수량 | 수량의 의미 |
| --- | ---: | --- |
| 원 대화의 키워드 그룹 | 181 | 표의 행 단위; 고유 단어·고유 뜻의 개수가 아님 |
| 원 대화의 작성 예시 | 25 | assistant가 작성한 재서술; 현재 사용자의 정의가 아님 |
| 표현별 판단 기록 | 206 | 모든 추출 행에 보존할 뜻·추가하면 안 되는 뜻·반영/보류 결정 연결 |
| 외부 자료 기록 | 85 | 사전 항목·공동체 용례·기관 자료·연구 논문; 접근 방식 별도 표시 |
| 관찰·관계 단위 초안 | 44 | 기존 계약 재사용과 신규 검토를 묶은 연구 단위; 신규 프로필 44개가 아님 |
| 맥락 기록 초안 | 12 | 평가·언어·역할·장르·목적·내면·대상화·동의·이력·시간·다의어·예시 |
| 후보 초안 | 24 | 실제 슬롯과 효과 축을 대조한 검토용 정의; 런타임 입력 불가 |
| 회귀 제안 | 84 | 구현 후 수행할 정책·팩·픽셀 사례; 이번 실행에서 통과한 테스트가 아님 |

원 대화의 인용 표시는 외부 URL 없이 캐시된 `chatgpt-content-reference`였다. 이를 독립 근거로 승격하지 않았다. [대화 영수증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/CONVERSATION-RECEIPT.json), [원문 행 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/TERM-INVENTORY.json), [외부 자료와 접근 한계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/SOURCES.md)를 따로 보존했다.

외부 근거 범위는 솔직하게 제한했다. 키워드 181행 중 90행에는 관련 어휘 항목이 연결돼 있지만 행에 묶인 모든 철자·다의어가 검증된 것은 아니다. 4행은 피팅 형태 분류의 근거, 9행은 대상화 분석 개념의 근거이며, 78행은 직접 외부 근거를 아직 연결하지 못했다. 특히 한국어 인터넷 표현·비유와 일부 부위 속어는 넓은 exact 별칭 추가를 보류한다. 이 행들도 어떤 관찰 축으로 분해할지와 어떤 뜻을 만들면 안 되는지는 개별 기록했다. 외부 근거 없는 별칭과 기존의 좁은 관찰 계약 재사용은 다른 결정이다.

Merriam-Webster·Cambridge의 자체 항목은 어휘 범위, Fanlore·Wiktionary는 해당 공동체와 사전의 기록된 용례, Understance는 해당 브랜드의 피팅 분류에 사용했다. Fanlore의 일부 페이지는 직접 접근이 403이라 검색 발췌만 활용했다. Langton의 추가 대상화 차원은 원저를 읽지 않고 Stanford Encyclopedia의 설명에 의존하므로 이차 근거라고 표시했다. 사용 빈도·시대별 대표성·최초 발생·보편적 인체 분류는 이번 근거로 주장하지 않는다.

## 2. 현재 데이터와 중복 처리

조사 시작 스냅샷은 `main`, HEAD `0ed2267b91e73f4b4d1493d095287e7795ebf805`의 작업 트리다. 기존 미커밋 신체 형태 작업을 포함한 병합 로더 기준 프로필 1,496개, 일반 후보 9,664개, 슬롯 112개였다. 원격 main 또는 배포된 데이터의 수치로 해석하면 안 된다.

별도 [신체 용어 연구](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/body-terminology-20261002/README.md)는 다른 대화 `6abf8375-e27c-83ee-92bb-0fec44eeff01`를 조사한 자료다. 그 연구와 진행 중인 `bm_` 통합을 비교했다. 이번 44개 단위 중 28개는 이미 존재하는 프로필을 참조하며, 중복을 제거한 참조 프로필은 42개다. 참조는 의미의 완전한 동의어 관계를 뜻하지 않는다. 예를 들어 목선 노출은 중앙 가슴 사이 관계와 관련 있지만 동일한 계약은 아니다.

| 의미 축 | 우선 비교할 실제 계약 | 강화할 데이터 |
| --- | --- | --- |
| 살집·연속 곡선·지역적 큰 가슴 | `soft_full_figure_volume`, `curvilinear_figure_relation`, `bust_prominence_relation` | 대상 범위와 크기/곡선의 독립성; 평가어와 형태어 분리 |
| 키·폭·사지 길이 | `slender_linear_build`, `bm_stature_scale`, `bm_compact_frame`, `bm_stocky_build`, `bm_long_limb_build` | 비교 기준·해당 구간·키와 비율의 교차 사례 |
| 가슴의 부착·돌출·분포 | `bm_breast_root_width`, `bm_breast_root_height`, `bm_breast_projection`, `bm_breast_fullness`, `bm_breast_spacing` | 부착 폭/높이·크기·깊이·분포·방향을 분리하는 패러프레이즈 |
| 하체의 폭·깊이·볼륨 | `bm_hip_width`, `bm_gluteal_projection`, `bm_gluteal_fullness`, `bm_thigh_volume` | 골반 폭과 후방 돌출을 서로 바꾸지 않는 대비 사례 |
| 국소 패임·다리 사이 공간 | `bm_hip_dip_local`, `inner_thigh_negative_space` | 부위와 자세·연속 배경 조건의 분리 |
| 입술·눈 | `bm_lip_volume`, `bm_eye_aperture`, 기존 pose vocabulary 후보 | 정지 구조와 현재 표정·시선의 분리 |
| 피부 | `bm_cellulite_relief`, `bm_striae_surface`, `bm_skin_tone_appearance`, `bm_skin_relief_texture` | 표면 증거와 원인·이력·건강 추론의 분리 |
| 의복의 윤곽·광학·지역적 노출 | `bm_fabric_body_outline`, `sheer_garment_optical_layering`, `pfe_lateral_chest`, `pfe_lower_chest` | 직물·부위·가장자리의 연결과 넓은 속어의 범위 차이 |
| 초대·장난스러운 상호작용 | `target_directed_seductive_display`, `playful_flirtation_interaction` | 주체·동일 대상·사건·대상에 연결된 결과 유지 |

파일별 소유권, 실제 계약 원문, 후보가 존재하는 슬롯과 시작 해시는 [현재 데이터 감사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/CURRENT-DATA-AUDIT.json)에 기록했다. 조사 도중 74개 추적 입력 중 7개 파일의 해시가 달라졌다. 이번 작성 도구의 수정 범위는 이 리서치 폴더이며 기존 변경을 되돌리지 않았다. 이름이 참조된 프로필·후보는 패키지 검증 시 최신 병합 데이터에서 존재를 재확인했다. 초기 exact 진단은 초기 스냅샷의 관찰로 남긴다.

## 3. 형태 표현에서 유지해야 할 독립 축

`plump`, `fleshy`, `curvaceous`, `voluptuous`, `buxom`, `zaftig`, `Rubenesque`, `thicc`를 ‘풍만한 여성 몸매’라는 하나의 프로토타입으로 합치면 지칭 범위·살집·곡선·평가·다의성이 사라진다. `fleshy`는 지칭한 대상의 살집, `curvaceous`는 곡선, `busty`는 가슴의 상대적 크기를 우선 보존하는 쪽이 정확하다. `buxom`의 오래된 복종 관련 뜻은 현대 체형 의미와 섞지 않는다. `thicc`의 기록에는 여성 외의 근육질 인물·동물·물체 용례도 있다. [Merriam-Webster fleshy](https://www.merriam-webster.com/dictionary/fleshy), [curvaceous](https://www.merriam-webster.com/dictionary/curvaceous), [busty](https://www.merriam-webster.com/dictionary/busty), [buxom](https://www.merriam-webster.com/dictionary/buxom), [thicc](https://www.merriam-webster.com/slang/thicc).

따라서 검색 문서는 ‘누구의 어느 구간이 무엇에 비해 어떻게 보이는가’를 중심으로 만든다. ‘큰 가슴’은 허리·골반 확대의 전제가 아니며, ‘곡선 있는 몸통’은 모래시계나 큰 가슴을 필수로 만들지 않는다. `well-endowed`는 자원·가슴·음경 등의 문맥이 있어 소유자와 대상 부위가 먼저 확정돼야 한다. `boobs` 같은 부위명은 형태·크기·행동을 제공하지 않는다. [well-endowed](https://www.merriam-webster.com/dictionary/well-endowed), [boob](https://www.merriam-webster.com/dictionary/boob).

피팅 분류에서 부착 폭, 앞쪽 돌출, 상하·안팎 볼륨 분포는 비교할 만한 독립 축이다. 다만 브랜드의 피팅 가이드는 의학적 보편 분류의 증거가 아니다. 작은 전체 볼륨과 깊은 돌출, 넓은 부착 폭과 얕은 돌출 같은 교차 사례를 함께 두어 검색·후보가 한 축을 다른 축으로 대체하는지 검증한다. 부착 높이는 현재 계약을 좁게 재사용하되 외부 근거를 추가 확보하기 전 넓은 별칭 승격을 보류한다. [Understance Branatomy](https://blogs.understance.com/branatomy).

`petite`, `slender`, `willowy`, `stocky`는 키·폭·사지 비율을 같은 방법으로 묶지 않는다. 특히 `petite`는 작은 체형의 형용사와 작은 키에 맞는 의류 범주를 구분해야 한다. `ripped`의 근육 선명도와 `jacked`의 근육 발달도 크기·정의·힘이라는 별도 축으로 다룬다. `sinewy`의 강인함 비유를 모든 힘줄·혈관이 드러나야 하는 시각 의무로 만들지 않는다. [petite](https://www.merriam-webster.com/dictionary/petite), [willowy](https://www.merriam-webster.com/dictionary/willowy), [stocky](https://www.merriam-webster.com/dictionary/stocky), [ripped](https://www.merriam-webster.com/dictionary/ripped), [jacked](https://www.merriam-webster.com/dictionary/jacked), [sinewy](https://www.merriam-webster.com/dictionary/sinewy).

`callipygian`은 둔부 형태를 미적으로 평가하는 말이므로 구체적인 큰 크기·원형·후방 깊이를 발명하지 않는다. `snatched` 역시 좁은 허리 외에 전체 외관·얼굴의 정돈된 인상과 동사 뜻이 기록돼 있다. 한국어 ‘도톰한’, ‘매끈한’, ‘찰진’도 부위·외곽·표면·물성이 실제로 무엇을 수식하는지 분리해야 한다. [callipygian](https://www.merriam-webster.com/dictionary/callipygian), [Wiktionary snatched](https://en.wiktionary.org/wiki/snatched).

## 4. 표정·시선·평가를 분리하는 방법

`pouty`를 항상 두꺼운 입술이나 현재 입 내밂으로 바꾸면 의미가 줄거나 늘어난다. 불만스러워 보인다는 인상, 입술의 현재 모양, 원래 볼륨을 각각 기록한다. `doe-eyed`의 큰 눈과 순진해 보이는 인상도 별개다. `bedroom eyes`의 암시적 평가는 반쯤 감은 눈이라는 유일한 형태로 정의되지 않는다. [pouty](https://www.merriam-webster.com/dictionary/pouty), [doe-eyed](https://www.merriam-webster.com/dictionary/doe-eyed), [bedroom eyes](https://en.wiktionary.org/wiki/bedroom_eyes).

얼굴 움직임에서 감정을 추론하는 연구 검토도 표정 형태와 특정 감정이 일대일이라는 가정을 지지하지 않는다. 이 자료를 사용하는 범위는 ‘현재 관찰과 내면 판정을 분리하자’는 것이다. 모든 감정 표현이 무의미하다거나, 사용자가 명시한 감정 서술을 지우자는 결론은 아니다. [Barrett et al., Emotional Expressions Reconsidered, 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6640856/).

`leer`, `ogle`에서는 보는 주체, 대상, 눈·머리 방향, 부정적 또는 관심의 평가, 지속·반복 정보를 분해한다. 현재 방향은 관찰할 수 있지만 ‘오래’, ‘반복해서’, ‘욕망을 가지고’라는 뜻 전체가 한 사진에서 검증되지는 않는다. 기존 `pv_side_eye`, `pv_half_lidded`, `same_adult_target_coordinated_gaze`를 좁은 요소로 재사용하고, 미소나 곁눈질에 새 관계·동기 hard 의무를 붙이지 않는다. [leer](https://www.merriam-webster.com/dictionary/leer), [ogle](https://www.merriam-webster.com/dictionary/ogle).

`bombshell`이나 `bimbo`의 평가를 금발·큰 가슴·모래시계·복종·지능이라는 고정 외형으로 풀지 않는다. `down bad`는 강한 호감 외에 절망·병이나 부상 등의 상태 용례도 있으므로 모두 성적 관심으로 해석하면 안 된다. `gooner`의 활동 참여·비하적 확장과 `Gooner`의 축구 문맥은 casefold 뒤에도 구분해야 한다. 실제 상태·지속·진단을 정지 얼굴에서 판정하지 않는다. [bombshell](https://www.merriam-webster.com/dictionary/bombshell), [bimbo](https://www.merriam-webster.com/dictionary/bimbo), [down bad](https://www.merriam-webster.com/dictionary/down%20bad), [gooner](https://en.wiktionary.org/wiki/gooner), [Gooner](https://en.wiktionary.org/wiki/Gooner).

## 5. 의복·부위·시간 표현의 범위

중앙 가슴 사이 관계인 `cleavage`는 쇄골·어깨·상부 가슴을 드러내는 목선과 같은 뜻이 아니다. 넓은 `sideboob`, `underboob`의 지역·시점·부위 의미는 기존 `pfe_` 프로필의 특정 불투명 중심 몸판·옆 가장자리·밑단 구조보다 넓다. 외부 용례는 확인했지만 해당 단어를 기존 좁은 프로필의 exact alias로 바로 넣는 것은 보류한다. 정확한 옷 구조가 원문에 있는 경우 기존 계약을 재사용하고, 일반 지역 의미의 소유 범위는 따로 검토한다. [cleavage](https://www.merriam-webster.com/dictionary/cleavage), [sideboob](https://en.wiktionary.org/wiki/sideboob), [underboob](https://en.wiktionary.org/wiki/underboob).

`cameltoe`에는 옷으로 드러나는 국소 외곽과 실제 부위명 뜻이 기록돼 있고, 띄어 쓴 `camel toe`에는 배구 손가락 용례도 있다. 모두 ‘옷 중앙의 주름’으로 순화하면 부위·원인·다의성이 사라진다. 의복으로 덮인 외곽 요청은 실제 의복과 해당 지역의 연결을 유지하고, 부위명 문맥과 비신체 용례는 따로 기록한다. [cameltoe](https://en.wiktionary.org/wiki/cameltoe), [camel toe](https://en.wiktionary.org/wiki/camel_toe).

`supple`은 굽힘·움직임의 유연성, `resilient`·`springy`는 변형 후 회복, `jiggly`는 작은 반복 움직임에 관한 의미가 있다. 현재 눌림은 접촉과 변형을 함께 보여 줄 수 있지만 복원·지속·반복이라는 물성 전체는 시간 자료가 필요하다. 이 표현들을 둥근 체형·피부 광택으로 대체하고 동등한 뜻이라고 주장하지 않는다. `flabby`·`doughy`의 재료·논증·음식·얼굴 문맥도 분리한다. [Cambridge supple](https://dictionary.cambridge.org/dictionary/english/supple), [Merriam-Webster resilient](https://www.merriam-webster.com/dictionary/resilient), [Cambridge springy](https://dictionary.cambridge.org/dictionary/english/springy?topic=flexible-loose-and-yielding), [jiggle](https://www.merriam-webster.com/dictionary/jiggle), [flabby](https://www.merriam-webster.com/dictionary/flabby), [Collins doughy](https://www.collinsdictionary.com/us/dictionary/english/doughy).

튼살은 선형 띠, 셀룰라이트의 겉모습은 국소 요철이라는 표면 계약으로 연결할 수 있다. 사진에서 원인·임신·체중 변화·건강을 채우지 않는다. ‘우윳빛’, ‘매끈한’, ‘촉촉해 보이는’은 겉보기 색, 미세 지형, 반사광을 별개 축으로 다루며 실제 수분·촉감의 증거로 승격하지 않는다. 기관 자료는 표면 설명의 범위를 참고했으며 의료 판단에는 사용하지 않았다. [American Academy of Dermatology, stretch marks](https://www.aad.org/public/cosmetic/scars-stretch-marks/stretch-marks-why-appear), [DermNet, cellulite](https://dermnetnz.org/topics/cellulite).

## 6. 장르·역할·동의·대상화 기록

`lewd`, `bawdy`, `ribald`, `risqué`, `salacious` 등의 상당수는 표현·유머·내용·행동에 대한 평가다. 강한 표현을 어느 정도 노출한 몸·큰 부위·특정 표정으로 고정하지 않는다. `innuendo`와 `double entendre`는 말의 암시와 복수 해석이므로 이미지에 발화·텍스트 또는 명시된 사건이 없는 상황에서 고정 인체 장면으로 옮길 수 없다. [lewd](https://www.merriam-webster.com/dictionary/lewd), [bawdy](https://www.merriam-webster.com/dictionary/bawdy), [ribald](https://www.merriam-webster.com/dictionary/ribald), [innuendo](https://www.merriam-webster.com/dictionary/innuendo), [double entendre](https://www.merriam-webster.com/dictionary/double%20entendre).

`thirst trap`은 주목·매력을 끌려는 게시 목적과 결부된다. 목적이 명시돼도 모든 사진이 셀카·야간·노출·큰 체형인 것은 아니다. 기존 `mature_nightlife_thirst_trap_context`는 가능한 야간 구성 하나이지 용어 전체 정의가 아니다. 게시 목적은 core에 보존하고 현재 시선·구도·의복 후보는 요청에 맞춰 각각 고른다. [Cambridge thirst trap](https://dictionary.cambridge.org/dictionary/english/thirst-trap).

PWP·citrus scale·idfic·darkfic·Dead Dove는 작품의 초점·역사적 내용 분류·독자 관계·메타태그를 구분한다. `darkfic`을 검은 의상으로, `Dead Dove`를 항상 특정 내용으로, `idfic`을 항상 성적 작품으로 바꾸지 않는다. 해당 기록은 공동체 용례 수준이며 전 공동체에서 동일하다는 주장이나 현재 수위 정책의 근거가 아니다. [Fanlore PWP](https://fanlore.org/wiki/PWP), [Citrus Scale](https://www.fanlore.org/wiki/Citrus_Scale), [Idfic](https://fanlore.org/wiki/Idfic), [Darkfic](https://next.fanlore.org/wiki/Dark%21fic), [Dead Dove](https://fanlore.org/wiki/Dead_Dove).

dominant/submissive는 명시된 관계 역학, top/bottom은 특정 활동 역할로 분리한다. 큰 체격·위쪽 위치·콜라·밧줄·가죽이 해당 역할·취향·합의를 증명하지 않는다. 실제 물체 후보는 착용자·재질·잠금·고정점·제한되는 부위의 연결을 소유한다. 역할과 합의는 요청이 알려 준 조건으로 따로 유지한다. NCSF 자료는 그 조직의 용어·합의 구분에 사용했으며 오래된 법률 논의는 이번 설계에 채택하지 않았다. [NCSF Consent Counts Statement](https://ncsfreedom.org/wp-content/uploads/2019/12/Consent-Counts-Statement.pdf).

`dub-con`, `non-con`의 허구 서사 조건은 각각 불확실·부재라는 정보다. 중립 재서술 과정에서 이를 자동 합의로 고치지 않는다. 현실 합의·법적 상태를 사진으로 판정하지도 않는다. NTR·bimbofication·aftercare는 이전 관계나 상태·선행 사건·이후 행동이라는 이력 근거가 필요하다. 세 인물·금발·담요 하나로 이력을 입증할 수 없다. [Fanlore dub-con](https://www.fanlore.org/wiki/Dub_con), [non-con](https://fanlore.org/wiki/Non-con), [Wiktionary netorare](https://en.wiktionary.org/wiki/%E5%AF%9D%E5%8F%96%E3%82%89%E3%82%8C), [bimbofication](https://en.wiktionary.org/wiki/bimbofication).

대상화 10차원은 시각 기본형 10개로 만들기 어렵다. Nussbaum의 수단화·자율성 부정·행위성 부정·교환 가능성·침해 가능성·소유·주관성 부정과, Langton에 관한 이차 자료의 몸/외관 환원·침묵 강요를 각각 맥락 기록으로 둔다. 명시된 선택을 무시하는 행동, 발언을 끊는 행동 등 구체 사건은 분해할 수 있지만 정지·닫힌 입·얼굴 크롭·접촉만으로 분석 범주를 판정하지 않는다. 분석 자체도 모든 맥락의 동일한 도덕 판정으로 단순화하지 않는다. [Nussbaum, Objectification, 1995](https://r.jordan.im/download/ethics/nussbaum1995.pdf), [Stanford Encyclopedia, Feminist Perspectives on Objectification](https://plato.stanford.edu/entries/feminism-objectification/).

## 7. 중립 재서술의 보존 장부

재서술은 원문 → 문맥과 소유자 → 의미 원자 → 관찰 가능한 문장과 별도 맥락 → 보존/미검증/누락 장부 순서로 설계한다. 원자는 소유자, 대상 부위, 속성, 비교 기준, 주체-행동-대상, 화자의 평가, 시간·이력으로 나눈다.

보존 상태를 세 가지로 구분한다. `visible_current`는 현재 모습에서 확인 가능한 뜻, `attributed_context`는 화자·게시 목적·서사에 귀속시켜 보존한 뜻, `unverified_in_single_frame`는 한 사진으로 확인할 수 없는 시간·내면·이력이다. 이는 런타임의 새 스키마가 아니라 이번 반영 설계의 검토 장부다. 관찰 절만 남겨 놓고 원문의 모든 뜻을 보존했다고 주장하지 않는다.

| 원 표현·문맥 | 중립적인 관찰 절의 예 | 별도 유지하거나 확인해야 할 정보 |
| --- | --- | --- |
| 성인 인물의 busty figure | 몸통에 비해 가슴의 볼륨이 두드러진다 | 컵 수치·허리·골반·노출을 추가하지 않음 |
| callipygian이라는 평가 | 구체 형태가 없다면 새 크기 묘사를 작성하지 않음 | 화자는 둔부의 형태를 미적으로 평가한다 |
| 얇은 입술을 현재 내민 성인 얼굴 | 얇은 입술이 현재 조금 앞으로 나와 있다 | 원래 두께와 현재 동작;불만·욕망은 명시된 경우 별도 |
| doe-eyed라는 인상 | 원문이 지정한 큰 눈 개구를 기술 | 순진해 보인다는 화자 평가;실제 성격·나이 아님 |
| 성인 A가 B를 leering이라고 평가받는 문맥 | A의 눈과 머리가 B 쪽을 향한다 | 부정적 시선 평가·동기·지속은 원문 근거에 귀속 |
| thrift/성적 의미 없는 Gooner 문맥 | 요청된 축구 응원 행동과 장면 | 명칭의 축구 뜻;성적 행위자로 변환하지 않음 |
| 주목 목적 게시 사진 | 요청된 카메라 방향과 의복·구도를 기술 | 게시 목적은 명시된 사실;야간·노출이 정의는 아님 |
| 역할을 상징하는 콜라를 명시 | 착용자의 목에 부착된 장식·재질·잠금을 기술 | 명시 역할 상징을 별도 보존;장식만으로 추정하지 않음 |
| 특정 옷 구조와 sideboob를 함께 명시 | 같은 몸판 옆 가장자리와 해당 바깥 부위 윤곽을 기술 | 구조가 없는 일반 용어에는 해당 옷을 발명하지 않음 |
| springy라고 서술한 표면 | 요청된 현재 눌림이 있으면 그 순간만 기술 | 힘 제거 뒤 복원은 시간 자료가 없으면 미검증 |
| 원칙을 포기하는 인물의 타락 | 요청된 선택·현재 행동을 기술 | 이익·원칙 포기라는 서사;신체 변형을 추가하지 않음 |
| 얼굴이 잘린 의복 상세 구도 | 화면 경계와 의복 부위를 기술 | 크롭만으로 인격·가치 환원이라는 판단을 추가하지 않음 |

이 표의 문장은 반영 원칙을 설명하기 위해 새로 작성한 예시다. 실제 요청에 자동 삽입할 패러프레이즈, 사용자가 채택한 문장, 이미지 검증 결과가 아니다.

## 8. 후보팩에 반영할 구체 범위

[의미 단위](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/SEMANTIC-UNITS.json)는 정의·구성요소·시점·혼동 대상·관찰 게이트·근거·기존 owner·반영 결정이 묶인 연구 초안이다. [후보 24개](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/CANDIDATE-DRAFTS.json)는 실제 슬롯, 필요한 core 전제, 바꾸는 dimension/property/target, 대비 사례와 보류 이유를 포함한다. 대상은 미결정 placeholder이며, 속성명은 현재 런타임 속성 목록에 매핑하기 전 제안 이름이다. JSON을 운영 파일에 직접 복사할 수 없다.

신체·표면·의복의 좁은 절 9개와 별칭 범위 검토 2개는 기존 계약을 먼저 사용한다. 시선·눈꺼풀의 3개는 기존 후보를 좁게 재사용한다. 현재 입 동작 1개, 대상 결속 시선 1개, 목 장식·재료·중앙 경계 3개는 중복·소유 범위 검토 후 반영한다. 나머지 5개는 복수 dimension 효과 때문에 보류한다.

보류 대상은 초대 동작 NC10, 제안/물림 NC11, 구속 물체 NC14, 접촉 변형 NC23, 사건 후 돌봄 NC24다. 예를 들어 `wearable_accessory`는 현재 `appearance`를 소유하지만 구속 후보는 실제로 `pose`와 `action`도 바꿀 수 있다. `body_pose`에 넣은 변형 후보도 `body_geometry`·`appearance` 효과를 숨길 수 없다. 단순 슬롯 분할만으로 모든 전제가 충족되는 것은 아니므로 각 후보의 전체 효과와 frozen core 적합성을 검증한다.

관련 자료는 검색의 양의 정의·구성요소·패러프레이즈를 보강하는 데 쓴다. 출처 URL, category ID, 반례, `claim_limits`, 장르·비하 표현 자체를 양의 시각 프로토타입으로 넣지 않는다. 정확한 문맥에 직접 요청된 뜻과 advisory BM25F/embedding 검색 결과의 권한을 유지한다. 미선택 후보는 새 의무를 만들지 않으며, 선택된 후보는 전체 opt-in 계약과 잠금 적합성을 만족해야 한다.

## 9. 실행한 진단과 반영 전 검증

최초 스냅샷의 resolver에 인위적인 source row를 넣어 exact-only 진단 12개를 실행했다. BM25F·embedding, 유효한 전체 frozen core, 실제 후보팩, 런타임 프롬프트, 이미지 생성은 이 진단의 범위가 아니다. [원 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/EXACT-ROUTING-DIAGNOSTICS.json).

`busty figure`, `curvy figure`는 각각 해당 큰 가슴·몸통 곡선 프로필을 required로 반환했고, 부정된 busty·장갑 재료의 supple는 신체 hard hit가 없었다. 특히 ‘이익 때문에 원칙을 포기한 성인 인물의 타락’도 `embodied_corruption_transition`을 required로 반환했다. 이는 넓은 문맥 표현과 신체 변화 계약 사이의 **어휘 라우팅 충돌 후보**다. 전체 생성 흐름의 확정 버그로 부르지 않는다. 이후 파일 해시 변화가 있었고 해당 프로필 activation은 별도 확인 시 바뀌지 않았지만, 현재 전체 core에서 같은 결과가 나는지는 다시 검증해야 한다.

[회귀 84개](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/REGRESSION-PROPOSALS.json)는 `PROPOSED_NOT_RUN`이다. 구현 후 도덕/신체 타락·정의 우선·부정·다의어·형태 축 독립·대상 뒤집기·역할/합의·시간 한계·속성 잠금·64개 후보 예산·부정 예제 검색 오염·부분 픽셀 충족을 검증한다. 세부 순서와 파일별 변경안은 [반영 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/IMPLEMENTATION-PLAN.md)에 있다.

[패키지 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/VALIDATION.json)은 모든 행의 결정 연결, source/unit 참조, 실제 owner·슬롯·재사용 후보의 존재, 속성 효과 축, 복수 축 보류, 비수출 상태를 확인했다. 구조 검증은 PASS이며 입력 스냅샷은 `INPUT_DRIFT_REVIEW_REQUIRED`다. 이는 연구 결과를 검토할 수 있다는 뜻이며 운영 반영·검색 성능·픽셀·사용자 선호의 통과 판정은 아니다.
