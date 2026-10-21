# 리미널·드림코어 시각 의미 / 후보 데이터 강화 리서치

2026-10-22 · 기준 대화: [리미널 용어 조사 설명](https://chatgpt.com/c/6acda685-7d7c-83e8-874d-db3910ed868e)

리미널 데이터를 강화할 때 가장 효과적인 단위는 장르명이나 소품의 수가 아니라 **기능이 읽히는 장소와 현재 상태의 어긋남**, 그리고 그 어긋남을 확인할 수 있는 **소유자·표면·접속·비교 관계**다. 따뜻한 드림코어, 기묘한 편집 사진, 물과 타일의 공간, 기록 매체의 오류를 별개 축으로 유지해야 선택 폭이 늘어난다. 이를 한 종류의 어두운 복도나 괴물로 수렴시키면 데이터가 늘어도 의미는 약해진다.

이번 산출물은 조사와 도입 설계다. 200개 원래 항목에 200개 의미 카드를 대응시켰고, 가시 형태로 분해할 수 있는 128개에 후보 구조 초안을 작성했다. 추가로 32개 한영 장면 실현안, 기존 CID 23개와의 통합 판단, 개발·대조 평가 48개를 준비했다. 원 대화의 민감한 항목까지 모두 분류에 남겼으며, 신체 상태·장면 관계와 진단·의도·동의·생사 같은 해석을 구별했다. 실제 후보 등록·인덱스 생성·검색 실행·이미지 생성의 완료를 뜻하지 않는다.

## 근거를 다시 읽으면서 달라진 점

| 판단 | 확인한 근거 | 데이터에 반영할 결정 |
|---|---|---|
| 비어 있음 하나만으로 리미널의 모든 뜻을 설명할 수 없다. | liminal의 중간 상태 용법과 Augé의 이동·소통·소비 관계는 서로 다른 개념이다. | L001~L004를 동의어 한 묶음으로 만들지 않는다. 통로·문턱·대기 기능은 개별 가시 관계로 둔다. |
| 무인은 공포의 보편 규칙이 아니다. | Diel·Lewis 연구는 구조 일탈을 다루며 공적/사적 실내에서 사람 존재의 효과도 달랐다. | 빈 공간·점유·구조 일탈을 독립 속성으로 둔다. 무인 필터를 장르 전체에 걸지 않는다. |
| 따뜻한 Dreamcore는 독립적인 목표다. | Song 외 연구는 선정 이미지 18장에 대한 449명 평가에서 기묘한 축과 편안한 축을 구분했다. | 공포 강도를 높이는 방식만으로 개선을 정의하지 않는다. E02에 편안한 대조군을 유지한다. |
| Poolrooms는 괴물 없이도 성립하는 공간 연구의 좋은 참조다. | 작가 Pike의 연작과 개발사 POOLS의 설명이 서로 다른 매체에서 물·공간을 다룬다. | 아치 접속·수면선·잠긴 문·수광면을 늘리고 추격자·음향은 별도 선택으로 둔다. |
| Weirdcore의 상투적 소품은 필요조건이 아니다. | r/weirdcore는 해당 커뮤니티의 편집 사진 기준을 설명하면서 눈·빨간 글자·그림자·리미널의 과도한 반복을 경계한다. | 눈을 넣는 것과 이미지/문장의 관계를 구분한다. 한 커뮤니티 규칙은 전 세계 장르 규격으로 쓰지 않는다. |

용어와 연구의 출처는 [Merriam-Webster](https://www.merriam-webster.com/dictionary/liminal), [Augé 저자 발췌](https://www.versobooks.com/en-gb/blogs/news/introduction-to-the-second-edition-of-non-places), [Diel·Lewis 저장소](https://orca.cardiff.ac.uk/id/eprint/151790/), [Song 외 연구](https://journals.sagepub.com/doi/abs/10.1177/02762374251356955), [Pike](https://www.jaredpike.art/projects/dream-pools/), [POOLS](https://store.steampowered.com/app/2663530/POOLS/), [커뮤니티 자체 규칙](https://www.reddit.com/r/weirdcore/)에서 각각 확인했다. 이 근거를 일반 인구의 취향·인과관계·생성 이미지 성공률로 확대하지 않는다.

## 범위와 증거 층위

원 대화의 표는 1~200번이다. `read_thread`에서 잘린 부분은 동일 대화의 브라우저 표로 확인했다. 원 대화의 설명은 조사 출발점이며, 그 안의 내부 인용번호를 검증된 새 출처로 재사용하지 않았다. 실제 읽은 41개 출처의 접근 수준은 [SOURCES.tsv](SOURCES.tsv), 실패·제한은 [ACCESS-LIMITS.md](ACCESS-LIMITS.md)에 기록했다. 모든 장면 제안은 연구자가 저술한 응용이며 기관·작가가 그 구성을 필수라고 정의했다는 뜻이 아니다.

| 모드 | 항목 수 | 실제 후보로 옮길 범위 |
|---|---:|---|
| still | 73 | 현재 화면에서 보이는 소유자·형상·연결. |
| proxy | 54 | 보이는 단서만. 시간·원인·정체·감정은 별도 한계로 남김. |
| versioned | 1 | 특정 출처·판본의 설정을 고른 경우만. |
| advisory | 49 | 해석·장르·감정·사회 개념. 명칭만으로 하드 의무를 만들지 않음. |
| audio | 13 | 소리의 실제 검증은 오디오 경로. 몰소프트 1개와 159~170번 12개 포함. |
| sequence | 10 | 이동·변화·반복·지속 시간의 증거를 요구함. |

128개 구조 초안에는 완성된 한영 번역·현재 native source-unit 증거·정식 effects/guards·역할 승인·검색 receipt·픽셀 리뷰가 아직 없다. 32개 한영 실현안은 그중 일부를 구체화하고 복합 항목의 대안도 제시한다. 둘의 수를 합쳐 160개의 신규 후보가 확정됐다고 계산하면 안 된다.

## 현재 저장소에서 실제 확인한 상태

조사 시작 HEAD는 `ffa6f724324bfe0256208fb202568ce00cd9f040`이다. 기존 dirty/untracked 작업이 있어 연구 폴더만 새로 만들었다. 시작 시점 추적 파일 3,634개의 SHA-256과 상태는 [BASELINE.json](BASELINE.json)에 기록했다. 종료 시 대조 결과는 VALIDATION.json에 별도로 남긴다.

현재 authored manifest를 읽으면 후보 18,801개, binding 12,629개다. 후보 중 diagnostic 126개를 제외하면 positive CID는 18,675개로, 작업 트리 검색 manifest의 metadata count와 수가 일치한다. 수의 일치는 검색 closure나 품질 검증을 대신하지 않는다. 설치 문서는 실제 realization document 18,677개를 명시하므로 CID 수와 RID 수를 혼용하지 않는다.

작업 트리 검색 공간은 `embeddinggemma2-local` / `google/embeddinggemma-2` / 768차원이다. 설치 포인터는 H-F2 세대 `13d885356aa63c72ec29b0409e8cce23469b3cbc0f9c0adbaf840ff7584d70db`를 가리켰다. 읽기 전용 `--check-runtime`은 설치 recorder·Python·NumPy 및 새 기록 형식 지원을 PASS했다. 이 결과는 검색·임베딩 추론·후보 의미 승인·이미지 품질의 PASS가 아니다.

Liminal/Dreamcore 등 10개 영문 패턴을 전체 candidate content에 대조하면 45개가 맞았다. 출처의 제외문·진단·다른 맥락도 포함하므로 45개를 적합 후보 수로 부를 수 없다. [EXISTING-CORPUS-AUDIT.json](EXISTING-CORPUS-AUDIT.json)에 원문·조건·binding을 보존했다.

추가로 visual_option의 다섯 primary text field에 12개 원자 패턴을 대조했다. 결과는 caustic 6, film-grain 5, CCTV/surveillance-view 8, negative-space 19 등이다. `tracking`은 태양 관측에도 맞았고 `compression`은 물리 압축 문맥에도 맞았다. freestanding-door·submerged-stairs·poolrooms·blurred-face·contradictory-gravity의 해당 정확 패턴은 0건이었다. 이는 **이번 어휘로 맞지 않았다는 결과**이며 의미상 부재나 실제 검색 실패의 증거는 아니다. 전체 결과는 [PRIMITIVE-LEXICAL-AUDIT.json](PRIMITIVE-LEXICAL-AUDIT.json)에 있다.

## 분야별 보강 방향

### 1. 유지관리된 공간, 사용 부재, 구조 일탈

기존 `between_use_transition_place`는 전이 기능·정상 사용 단서·예상 사용의 부재·전후 흔적·미해결 경로라는 특수 실현을 이미 갖는다. 이를 버리고 새 liminal 프로파일을 복제할 이유는 없다. 반대로 그 다섯 요소를 모든 리미널 개념의 정의로 강제해서도 안 된다. 기존 `exact_terms`에 넓은 리미널 명칭이 포함되므로 실제 독립 코어 활성 경로를 검사해야 한다.

보강 단위는 빈 복도, 대기 시설, 닫힌 몰, 준비된 연회장, 모델하우스, 서비스 구역의 경계 등이다. 각 경우에 정상 사용을 읽히게 하는 단서가 다르다. 예를 들어 문 닫힌 점포와 켜진 안내판은 현재 상태의 대비이지만 영구 폐업을 입증하지 않는다. 뜨거운 듯한 컵도 직전 사람이 떠났음을 입증하지 않는다. 장소 원자는 재사용하고, 그런 대비를 연결하는 작은 관계 후보를 더하는 편이 낫다.

### 2. Poolrooms의 물·타일·광학·접속

우선 추가할 관계는 `수면 → 같은 계단의 어느 단을 가로지르는가`, `문틀·손잡이 → 같은 물 부피 아래에 있는가`, `아치 → 두 공간을 실제 개구부로 잇는가`, `반사 → 어느 실제 아치를 비추는가`, `빛무늬 → 어느 수광면에 놓이는가`다. R06~R13에 독립 한영 대안을 작성했다.

‘검은 물’, ‘깊은 물’, ‘무한 수심’, ‘침수된 통로’, ‘물 빠진 수영장’은 분리해야 한다. 수면 아래가 안 보이는 것은 실제 수심 정보가 부족하다는 뜻이다. 부피가 불가능하다는 설정은 건물 외형과 내부의 동일 기준 비교가 필요하다. 물결빛도 벽에 인쇄된 무늬와 동일하지 않다. [OpenStax](https://openstax.org/books/university-physics-volume-3/pages/1-3-refraction)는 매질 경계의 빛 경로를 설명하며, 이 연구의 개별 환상 장면을 보증하는 자료는 아니다.

### 3. 따뜻한 꿈 풍경과 공간적 불가능

들판·집·파스텔 노을·커다란 식물·하늘 돔·문·부유 지형은 조합 가능한 선택지다. R14는 따뜻한 방향을 남기고, R15의 벽 없는 문은 같은 잔디가 문 안팎으로 이어지는 대안으로 작성했다. 문이라는 이유만으로 포털을 더하지 않는다. R17의 거대 식물은 비교 인물의 발과 식물 밑동이 같은 지면에 보여야 하고, R18의 부유 지형은 밑면과 공기 간격이 필요하다.

재귀 모형은 거울 반사와 다르고, 두 유사 문은 공간 루프를 입증하지 않는다. 서로 다른 중력은 각 인물의 국소 접지를 따로 추적해야 한다. 불가능한 계단은 모든 접속점이 가려진 사진으로 통과시키면 안 된다. Escher의 [Relativity에 대한 미술관 설명](https://escherinhetpaleis.nl/en/about-escher/masterpieces/relativity)은 이와 같은 다중 중력의 시각 참조다. 수학의 비유클리드 기하학과 동일한 개념으로 저장하지 않는다.

### 4. 얼굴, 몸, 반사, 기록 표면의 소유자

L129 무안면은 실제 얼굴 표면의 형상, L130 먼 실루엣은 식별 거리, L138 블러는 기록 표면의 변화, L139 천은 별개 물질의 가림이다. 이 넷을 `faceless` 한 태그로 묶으면 시각 의미가 무너진다. 도플갱어는 두 위치의 인물과 실제 바닥을 보존하고 거울 속 영상과 구별한다. 마네킹의 이음새는 생명 여부나 움직임의 증거가 아니다.

몸과 건축의 융합도 살색 벽지·붙여 둔 장식·연속된 유기 형상 중 무엇인지 선택해야 한다. 분절은 초현실적인 무상처 분리와 신체 손상을 나눈다. 여기서 신체 형상의 고증·owner graph를 다루는 것과 실제 생물학·병리·상해 이력을 판정하는 것은 별개다. [Freud Museum](https://www.freud.org.uk/2019/09/18/the-uncanny/)과 [Met의 초현실주의 설명](https://www.metmuseum.org/essays/surrealism)은 개념·미술사 맥락으로 사용했다.

### 5. 매체 오류와 실제 공간의 변화

필름 입자, VHS tracking풍 가로띠, 신호의 색 정렬 차이, CRT 주사선, 디지털 블록은 서로 다른 표현이다. 특히 `실제 방 → 모니터/TV 물체 → 그 안의 기록 이미지 → 캡션`을 네 층으로 구분한다. 화면 안 오류를 채택했다고 벽·문·신체가 찢어지는 효과까지 가져오면 안 된다.

R28~R30은 오류를 표시 영상에 한정한다. 전체 이미지 오버레이를 원할 때는 다른 효과 대상으로 저술한다. 실제 촬영 원인·codec·테이프 열화 이력은 유사한 픽셀만으로 확정하지 않는다. [AVAA tracking](https://www.avartifactatlas.com/artifacts/tracking_error.html), [Y/C delay](https://www.avartifactatlas.com/artifacts/yc_delay_error.html), [block noise](https://www.avartifactatlas.com/artifacts/block_noise.html), [sub-sampling](https://www.avartifactatlas.com/artifacts/sub-sampling_artifact.html)의 설명은 기술 범위를 한정하는 근거다. 개별 영상 오류 사례를 모든 JPEG 원인으로 일반화하지 않았다.

### 6. 텍스트·규칙·환경 서사

번호 반복은 같은 화면의 두 문에 실제로 읽히는 글자가 있어야 한다. 화살표는 표적과 함께 보여야 하고, 벽화 출구는 그림의 경계가 보여야 한다. 정교한 설명이 있어도 표지가 흐리면 텍스트 관계는 통과하지 못한다. 정체불명 문자로 명시적인 문장 모순을 대체하면 안 된다.

가상 문장은 현장 간판과 후처리 캡션을 구분했다. `YOU HAVE BEEN HERE BEFORE`는 보는 사람의 실제 기억을 안다는 사실이 아니라 자막 장치다. 환경 서사도 의자·서류·얼룩의 배치를 제안할 수 있지만 사건의 원인을 자동 확정하지 않는다. [Brehmer의 공개 에세이](https://arxiv.org/html/2309.01763v1)는 존재·부재와 설명되지 않은 행위자의 해석을 논하는 참고이며, 보편적인 관객 반응을 입증한 실험이 아니다.

### 7. 사적 경계, 관능, 폭력, 의료·생식의 맥락

185~200번을 생략하지 않고 모두 별도 카드로 남겼다. 관능적 언캐니·꿈속 노출·페티시적 사물·관음 시점·성적 위협은 같은 뜻이 아니다. 성인이라는 사실, 부드러운 재질, 노출, 구속, 가림, 수중 인체는 각각 동의·욕망·사망의 증거가 될 수 없다.

R31은 찻잔의 용도와 재질의 충돌만 구체화했다. [MoMA의 Object 설명](https://www.moma.org/collection/works/80997)이 다루는 촉각적 양가성을 출발점으로 삼았으며 일반 재질 선호를 페티시로 분류하지 않는다. R32는 유기체풍 방의 연속 형상이다. 자궁 비유와 실제 생식 사건은 별개다. [BFI의 body-horror 비평](https://www.bfi.org.uk/lists/10-great-body-horror-films)은 장르·자율성 맥락에 한정했고, [Whitney 전시 기록](https://whitney.org/exhibitions/abject-art)은 전시 존재 확인에만 사용했다.

### 8. 정지 이미지로 대체할 수 없는 자료

형광등 버즈, 공조음, 잔향, 테이프 히스, 와우·플러터, 비동기 발소리는 소리 자료가 필요하다. [AVAA의 wow/flutter 설명](https://www.avartifactatlas.com/artifacts/wow_and_flutter.html)을 화면 왜곡의 다른 이름으로 저장하지 않는다. 느린 카메라 부유·롱테이크·경계 이동·노클립·시간 루프는 연속 증거가 필요하다. 사진에서는 기구·반사·흔적을 대응시킬 수 있지만 소리·시간 변화의 PASS로 사용하지 않는다.

Kenopsia·Anemoia는 창작 감정어이고, 자각몽은 꿈이라는 인식과 조절 능력을 구분해야 한다. [Koenig 공식 출판사](https://www.simonandschuster.com/books/The-Dictionary-of-Obscure-Sorrows/John-Koenig/9781501153648), [저자 kenopsia 정의](https://dictionaryofobscuresorrows.com/post/27720773573/kenopsia), [Horton 논의](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2020.00259/full)를 확인했다. 창작 카드에서 임상 진단이나 개인 경험을 자동 추론하지 않는다.

## 충분한 보강의 기준

후보 수의 고정 목표보다 다음 차이를 실제로 구분할 수 있어야 한다.

1. 같은 장소에서도 유지관리된 부재·폐허·정상 이용을 다르게 검색하고 선택할 수 있는가.
2. 같은 물에서도 얕음·침수·반사·불투명·배수·공간 연결을 나누는가.
3. 같은 얼굴 비식별에서도 무안면·거리·천·기록 블러가 바뀌지 않는가.
4. 오류가 실제 공간·광학·매체·화면·캡션 중 어느 층에 있는지 유지하는가.
5. 장르명을 빼고 자연어로 관계를 설명해도 적합한 후보가 발견되는가.
6. 따뜻한 방향·평범한 장소·제품·진료 등의 대조군이 불필요한 호러로 변하지 않는가.
7. 보이지 않는 연결·시간·소리·의도에 PASS를 부여하지 않는가.

각 항목을 어디에 반영하고 어떤 순서로 검사할지는 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md), 실제 픽셀 검토 설계는 [PIXEL-PLAN.md](PIXEL-PLAN.md)에 정리했다. 세부 항목은 [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md), 재사용 판단은 [existing-source-mapping.json](existing-source-mapping.json)에서 확인할 수 있다.
