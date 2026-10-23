# Art Horror 시각 의미·후보 데이터 보강 연구

2026-10-23, Asia/Seoul. 대상은 [원 대화](https://chatgpt.com/c/6adaf50e-502c-83ee-894e-85601ea7cd1c)의 용어 **154개**, 영화 12편, 미술·퍼포먼스 사례 7개, 창작 조합 6개다. 연결 도구의 20,000자 제한은 크롬 렌더링 본문과 15개 표를 끝까지 읽어 보완했다. [브라우저 보완 기록](browser-supplement.json), [전체 키워드 대조](KEYWORD-ATLAS.md), [작품·조합 매핑](REFERENCE-MAPPING.md)을 보존했다.

연구의 중심 결론은 **Art Horror라는 상위 이름을 구체적인 형태·관계의 선택지로 풀되, 비평적 독법·시간·음향·사회적 사실을 이미지의 가시적 속성과 구별하는 것**이다. 자료를 많이 추가하는 것보다 이 구별이 검색 정밀도와 후보 사용의 정확성에 직접 연결된다.

이번 결과는 시각 관계 카드 64개, 문맥 카드 29개, 한영 후보 초안 64개, 관계 검증 조건 206개, 출처 47개, 평가 명세 113개다. 후보 초안은 시각 카드의 다른 표현이므로 두 수를 더해 독립 데이터 수로 주장하지 않는다. 모두 연구 초안이며 검색·native 자격·이미지 생성·픽셀 평가는 실행하지 않았다.

## 1. 개념을 잘못 합치면 어떤 문제가 생기는가

### Art Horror와 철학 용어 art-horror

Criterion의 기획은 공포와 형식적 혁신, 기묘한 아름다움이 함께 나타나는 작품군을 제시한다. Church의 연구는 elevated/post-horror의 취향·가치·수용 논쟁을 다룬다. 이를 ‘느림+고급스러움+저채도’라는 고정 묶음으로 변환하면 밝고 과장된 색채나 육체적 과잉을 사용하는 작품을 놓친다. [Criterion](https://www.criterionchannel.com/collections/H2JcvXA0/art-house-horror), [Church 출판사 설명](https://edinburghuniversitypress.com/book-post-horror.html).

Carroll의 철학적 논의에서는 괴물의 존재만큼 그 존재가 작품 세계의 정상 질서를 어떻게 어기는지가 중요하다. 예술영화라는 제작·비평 범주와 별도 의미로 보존해야 한다. 이번에 읽은 범위는 장 요약이며 그의 이론 전체를 검증한 것은 아니다. [Carroll 장 요약](https://www.cambridge.org/core/books/abs/classic-readings-on-monster-theory/nature-of-horror-from-the-philosophy-of-horror/221332574F0B76469FD2C61FDB9CAB3E).

**반영:** T001–T025는 의미 구별과 탐색의 안내다. 하나의 장르명이 고어·성적 표현·특정 팔레트·특정 스튜디오·의례·상실을 자동 삽입하게 만들지 않는다. A24 Horror는 대화의 본문에 등장한 회사 중심 통칭으로 보존하되, 154개 표 항목에 추가로 합산하지 않는다.

### 언캐니·불쾌한 골짜기·비체·그로테스크

|개념|구별되는 핵심|선택 가능한 가시적 실현|검증하면 안 되는 주장|
|---|---|---|---|
|Uncanny|익숙한 것에서의 낯섦|일상 거울의 손 상태가 실제 손과 어긋남; 기능적 비례가 바뀐 손잡이|실제 정신 상태·억압의 원인|
|Uncanny Valley|인간 유사성과 호감 반응에 관한 Mori의 가설|인공물의 피부 같은 표면과 기계 관절을 함께 보임|한 장에서 관객의 호감 곡선이나 운동의 섬뜩함 측정|
|Abjection|주체/객체 등 경계가 불안정해지는 이론|막의 안팎·용기와 유출 물질·외피와 내부가 드러나는 관계|피나 더러운 질감이 있으면 비체 경험이 성립한다는 판정|
|Grotesque|형태와 분류의 비정합|연속 외곽을 가진 이종 구조·과장된 조각 형상|혐오나 공포가 반드시 발생한다는 판정|

Freud Museum은 분신·인형·반사 등의 맥락을 설명하고, Mori 원문은 움직임을 외관과 별도 변수로 다룬다. Kristeva 출판사 설명의 핵심은 경계 문제이며, MoMA의 grotesque 정의는 형상의 비정합에 주목한다. [Freud Museum](https://www.freud.org.uk/2019/09/18/the-uncanny/), [Mori의 승인된 원문 번역](https://spectrum.ieee.org/the-uncanny-valley), [Kristeva](https://cup.columbia.edu/book/powers-of-horror/9780231214575/), [MoMA 용어집](https://www.moma.org/momaorg/shared/flattened_pages/moma_learning/glossary/).

**반영:** V01–V12를 중심으로 익숙한 기준·이상 부위·둘의 연결을 함께 기록한다. 의지·장애·흉터·비규범적 외모를 자동 공포 표식으로 만들지 않는다. 가시적 형태의 충족과 관객의 정서적 반응을 별도 평가한다.

### Weird·Eerie·Liminality·Sublime

Fisher의 정의에서 weird는 속하지 않는 존재의 출현에, eerie는 있어야 할 것이 없거나 없어야 할 것이 있는 상태에 초점이 있다. 빈 복도만으로 ‘없어졌어야 할 사람’을 인증할 수 없다. [출판사](https://repeaterbooks.com/product/the-weird-and-the-eerie/), [Fisher의 정의 인용과 발췌](https://thequietus.com/culture/books/mark-fisher-weird-eerie-kubrick-tarkovsky-nolan-review/).

V49의 식탁에는 의자·상차림·점유 상태를 함께 두어 공백의 기준을 만든다. V59는 어두운 문 내부를 **알 수 없음**으로 남긴다. 어둠을 빈방이나 괴물의 증거로 처리하지 않는다. Liminality의 사회적 이행과 Liminal Space의 공간 형태도 같은 항목으로 합치지 않는다. V18의 인물/건축 크기 비교는 숭고를 위한 한 가지 표현 제안이며, 숭고 경험 그 자체의 증거는 아니다.

## 2. 보강할 데이터 영역

|영역|중심 카드|실제로 기록할 것|현재의 취약한 축약을 막는 경계|
|---|---|---|---|
|낯익음과 어긋남|V01–V06, V55|실제 인물·반사·그림자·인공물의 주인과 대응|‘기괴한 분위기’만으로 이상 관계 충족 처리 금지|
|몸·막·물질|V07–V12, V43–V47|외피/내부, 접합부, 부착 이음선, 손상 소유자|천·조각·밀랍·분장·실제 허구 신체를 자동 교환 금지|
|관람 위치와 구도|V13–V18, V48–V49|시선의 출발/목표, 차폐면, 빈 영역, 같은 바닥과 크기 기준|대칭이나 빈 공간만으로 통제·실종·두려움 확정 금지|
|중첩된 매체|V19–V24, V50, V58, V60–V62|실제 방·그림·모형·스크린·종이의 별도 경계|그림 속 상처를 실제 사람에게 전이하거나 필름 흠집을 실제 벽으로 전이 금지|
|죽음·성물·의례|V25–V30, V52|용기와 내용물, 도상과 신체, 행렬의 방향과 무대|성스러움·기적·순교·모독 의도·희생 인과 자동 인증 금지|
|빛·색·공간 구조|V31–V36, V51, V59|받는 면별 조도/색, 문턱·분기·지지 경로|호러=어둠, 네온=지알로, 긴 복도=무한 공간으로 축약 금지|
|욕망·관계·생식 비평|V37–V42, C13–C18|거리·시선·물건의 재질과 별도 문맥|성별 외관·임신·가죽·가면에서 욕망·동의·괴물성 추정 금지|
|퍼포먼스·전시·기관|V53–V54, V61–V64, C26–C28|연기자/관객/작품/거래 매체의 별도 위치|정지 자세에서 부토·장시간 인내·관객의 공모·저주 인과 확정 금지|

카드마다 한영 문장, 원 대화 seed, 소유자, 방향 관계, 혼동 반례, 주장 한계, 개념 출처, 가능한 역할을 작성했다. [전체 카드](VISUAL-CARDS.md)와 [기계 판독 자료](semantic-cards.json)에 정확한 문장과 관계가 있다.

### 질감은 물질·촉각·정서의 세 층위로 분리

MoMA는 biomorphic을 유기적 형상을 연상시키는 추상 형태로 설명한다. Marks의 haptic visuality는 촉각적인 기억과 관객의 체화 경험을 다루며, 그 문화적·역사적 맥락도 중요하다. ‘실제 피부’, ‘만져지는 것 같은 표면’, ‘관객이 느낀 혐오’를 같은 속성으로 저장하면 안 된다. [MoMA](https://www.moma.org/collection/terms/biomorphic), [Marks](https://www.dukeupress.edu/The-Skin-of-the-Film).

이번 제안에서는 V11의 같은 천 위 젖음 경계, V17의 손목까지 이어지는 피부 주름, V54의 직물·사슬·받이 관계를 사용한다. 젖음·광택·섬유 뭉침은 기록할 수 있지만 냄새·차가움·통증·생체조직의 화학적 정체는 별도다.

### 빛과 색은 수식어보다 공간적 분포

명암법은 명도 대비를 통해 형태를 조직하는 넓은 범위이고, tenebrism은 주로 어두운 장면 속 일부 세부가 두드러지는 방식이다. [National Gallery의 명암법](https://www.nationalgallery.org.uk/paintings/glossary/chiaroscuro), [tenebrism](https://www.nationalgallery.org.uk/paintings/glossary/tenebrism).

V31은 얼굴·손의 하이라이트와 몸의 연결, V32는 문틀을 경계로 다른 공간에 속하는 색을 기록한다. 광원의 종류·배치·받는 면이 빠진 외관 문장에는 완결된 `lighting` 역할을 곧바로 승인하지 않는다. 더 좁은 light 역할이 맞는지 개별 검토한다. FilmColors의 자료는 《서스페리아》의 서로 다른 인화물과 공정의 출처까지 구별하므로, 작품명을 임의 RGB 팔레트로 고정하지 않는다. [FilmColors](https://filmcolors.org/galleries/suspiria-1977/).

### 미술·퍼포먼스는 장르 템플릿이 아니다

NCMA의 tableau vivant는 회화·조각 속 자세를 몸으로 구성하는 교육적 실천을 설명한다. Städel의 빈 행동주의 설명은 특정 시기·물질·행위를 기록한다. Japan Foundation의 부토 자료는 구체적인 창작자·아카이브에 기반한다. 자세 하나나 흰 분장을 이러한 전통 전체의 정의로 쓰지 않는다. [NCMA](https://learn.ncartmuseum.org/resources/developing-visual-literacy-tableaux-vivant/), [Städel](https://sammlung.staedelmuseum.de/en/person/viennese-actionism), [Japan Foundation](https://performingarts.jpf.go.jp/en/article/6981/).

《Rhythm 0》는 기록과 작가 증언을 통해 시간과 관객 참여를 논할 수 있는 사례다. 이 역사적 근거를 일반 장면 속 인물의 동의로 가져와서는 안 된다. 《Open Wound》의 직물·금속·기계·액체는 재료와 연결을 읽는 사례로 사용하며, 피부 같은 직물을 실제 사람 피부로 바꾸지 않는다. [MoMA의 작가 증언](https://www.moma.org/audio/playlist/243/3118), [Hyundai Artlab](https://artlab.hyundai.com/project/hyundai-commission-mire-lee).

## 3. 성적·폭력적 용어의 보존과 반영

원 대화의 성폭력·생식 강요·근친 금기·시체성애·vagina dentata·가학/피학·자기 훼손·식인·자기 식인·고문·고어·스플래터를 키워드 목록과 문맥 카드에 보존했다. 정의에서 중요한 **동의, 친족, 몸의 소유, 대상의 생사, 욕망, 행위자**를 지우고 약한 질감으로 바꾸지 않는다. 이러한 조건이 정지 이미지에서 보이지 않는다는 사실도 함께 저장한다.

Harrington의 gynaehorror와 Creed의 monstrous-feminine은 여성/생식적 몸에 대한 재현과 문화적 권력의 분석이다. 여성이나 임신한 신체의 외관 자체에 공포·비정상성을 붙이는 속성이 아니다. [Harrington 출판사 설명](https://www.routledge.com/Women-Monstrosity-and-Horror-Film-Gynaehorror-1st-Edition/Harrington/p/book/9781315546568?PageSpeed=noscript), [Creed 출판사 설명](https://www.routledge.com/The-Monstrous-Feminine-Film-Feminism-Psychoanalysis/Creed/p/book/9781003006756).

|구별|보존해야 할 의미|부족한 대체 증거|
|---|---|---|
|BDSM / 강압적 폭력|합의 조건과 권력 교환 / 동의 침해|끈·가죽·수동적 자세|
|신체 손상 / 자기 훼손|상처 상태 / 자신에게 가한 행위|상처만 있는 정지 이미지|
|시체성애 / 애도|죽은 몸을 향한 성적 욕망 / 상실 관계|해골·기념물·잠든 사람|
|식인 / 포식 은유|먹는 주체·인체라는 대상·소유 관계|붉은 음식·가족 식탁|
|신체 절단 / 조각 파손|인체 / 특정 재료의 인공물|돌·밀랍·상해 분장|
|고어 / 스플래터 / 고문 서사|가시적 손상 / 과잉된 볼거리의 조직 / 지배와 고통의 구조|피의 양 하나|

직접 보이는 허구 신체의 상처 V44와 보철 분장 V43, 돌 조각의 분절 V45는 독립 후보다. 요청의 의미를 약화하는 자동 대체를 허용하지 않는다. 자기 훼손 등은 소재의 정의와 비평적 문맥을 보존하며 실행 방법 데이터는 작성하지 않는다.

남성적 응시·scopophilia의 상세 이론은 Mulvey 원문을 충분히 다시 읽지 못했다. 따라서 V16/V39의 가시적 시선 관계는 제안하되, 이를 이론 전체의 판정기로 승인하지 않는다. 이는 연구 공백으로 남겼다.

## 4. 정지 이미지에서 보류할 것

|항목|스틸에서 가능한 기록|추가로 필요한 자료|
|---|---|---|
|롱테이크·고정 숏·느린 전진|거리·프레이밍·화면 안 구조|시간 연속 영상·카메라/편집 기록|
|변신·반복강박·시간 루프|현재 변형 경계·반복 무늬|같은 소유자를 이어 주는 전후 자료와 시간 순서|
|불연속 편집·연상 몽타주|한 장의 병치·종이 콜라주|숏/패널 순서와 이어지는 관계|
|아쿠스마틱·드론·소리 철수|소리 발생원일 수 있는 물체|실제 오디오·발생원과 이야기 세계의 관계|
|관객의 공모·저주·창작 강박|관람 위치·작품·라벨·단말|관객의 행위·작품 변화·인과·제도 문맥|
|의도·동의·혈연·사별·진단|사람과 물체의 현재 배치|명시적인 이야기/기록 근거|

Chion의 audio-vision은 소리와 영상이 함께 만드는 지각을 다룬다. 이어폰이나 라디오의 그림이 있다고 소리가 검증되는 것은 아니다. [Chion](https://cup.columbia.edu/book/audio-vision-sound-on-screen/9780231185882/), [카메라 움직임](https://filmglossary.ccnmtl.columbia.edu/term/camera-movement/), [롱테이크](https://filmglossary.ccnmtl.columbia.edu/term/long-take/).

## 5. 기존 저장소와의 관계

이번 조사에서 실제 후보 원문의 `en`, `ko`, `definition`, `aliases`를 읽고 문자열 출현을 관찰했다. [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)는 수치와 실제 CID, 재사용 후보를 정리한다. 단어가 없다는 사실은 의미가 없다는 증거가 아니며, 단어가 있다는 사실도 올바른 문맥·역할·native 자격이 있다는 증거가 아니다.

현재 존재하는 반사 불일치·축소 모형·성유물함·생물형 아치·분장 이음선은 우선 재사용 검토 대상으로 삼는다. 기존 카드가 비슷해도 새 문장의 추가 의미를 잘라서 덮어쓰지 않는다. 예를 들어 새틴 하이라이트는 젖음 경계와 다르고, 일반 거울 시선은 벽 틈을 통과하는 관찰 관계와 다르다.

정확한 반영 순서·파일 범위·회귀 기준은 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md), 비교 생성 설계는 [PIXEL-PLAN.md](PIXEL-PLAN.md)에 있다.

## 6. 확인 범위와 남은 공백

출처 47개는 원전 47권 완독을 뜻하지 않는다. 출판사 설명·기관 용어집·작가 증언·비평·검색에 노출된 공식 본문·서지 확인을 구분해 [source ledger](sources.json)에 적었다. 원 대화의 정의 154개 각각을 모두 독립적인 원전으로 검증한 것도 아니다.

Mulvey 원문 상세, Bataille/Bois/Krauss의 informe 원전, Camp·Decadence의 개별 이론, 일부 참고 작품의 상세 분석은 추가 문헌 검토 대상으로 남는다. 해당 용어는 삭제하지 않고 해석 범위를 제한했다. 작품의 실제 픽셀이나 전체 영화를 이번에 감상했다고 주장하지 않는다. 접근 실패와 출처 간 수치 차이는 [ACCESS-LIMITS.md](ACCESS-LIMITS.md)에 남겼다.
