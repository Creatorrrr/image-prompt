# 색 조합의 시각 의미·후보 데이터 강화 리서치

2026-10-06 KST · 참조 대화: [색 조합 제안](chatgpt-conversation://6ac3cf7c-44c8-83ee-99e2-f132b43020e7) · 연구와 반영 계획 완료 · 활성 데이터 반영·인덱스 재생성·이미지 생성 미실행

## 핵심 결론

색 이름의 목록보다 **색이 속하는 대상, 영역의 역할, 관계의 방향, 물체색·광원·보정의 구별**을 보강하는 것이 우선이다. 현재 색 관계 데이터의 기본 구조를 재사용하고, 100개 팔레트는 선택 가능한 구체적 적용 예시로 작성했다. “골드”, “네온”, “호텔 핑크”, “오방색” 같은 말만으로 이 예시의 물체·재질·면적·장소를 강제하지 않는다.

조사 패키지는 **13개 계열의 100개 배색 카드, 공통 원리를 다루는 16개 카드, 후보 초안 100개, 출처 37개, 313개 sRGB 색칩의 계산값, 컴파일 형식 예시 4개**를 포함한다. 100개 후보를 전부 새 entry로 추가하는 목표는 아니다. 정확한 기존 후보는 보강하고, 일반 관계는 재사용하며, 실제로 다른 색·소유·mechanism만 좁은 변형으로 채택한다.

[100개 카드](SEMANTIC-CARDS.md) · [후보 초안](CANDIDATE-DRAFTS.json) · [16개 원리](MECHANISM-CARDS.json) · [출처와 한계](SOURCES.md) · [반영 계획](IMPLEMENTATION-PLAN.md) · [현재 데이터 조사](CURRENT-DATA-AUDIT.json)

[색칩 검색·4개 비교 자료](PALETTE-ATLAS.html)에는 원래 색칩, owner 역할, 계산값, 출처의 확인 한계를 함께 넣었다. 파일·데이터·스크립트 구문을 검사했으나 브라우저의 로컬 file 주소 정책으로 실제 화면·상호작용은 검증하지 못했다.

## 1. 입력의 범위와 확인 수준

참조 대화를 직접 읽어 1–100번의 모든 표 행을 추출했다. 원래 대화의 별표는 사례 응용 32건을, 나머지 68건은 목적 설계안을 뜻한다. 이 구분은 원래 답변의 분류이며, 이번 조사에서 “32개 전체의 실제 사용 빈도를 검증했다”는 뜻은 아니다.

커넥터가 제공한 답변은 20,000자로 제한되어 끝의 활용 설명이 잘렸다. 그러나 100번 표 행까지는 완전했다. 대화에 연결된 sandbox HTML/JSON 파일과 인용 번호에 대응하는 원본 URL은 커넥터에 없었다. 따라서 [SEED-KEYWORDS.json](SEED-KEYWORDS.json)은 **표 행의 추출본**이고 원래 첨부 JSON의 동일 파일 복사본이 아니다. [REFERENCED-CONVERSATION.json](REFERENCED-CONVERSATION.json)에 받은 상태를 보존했다.

출처는 연구 초록, 색 공간·접근성 문서, 박물관·문화 기관, 브랜드 공식 자료, 조명·재료 문서, 제작자 인터뷰와 제조사의 배색 제안으로 구분했다. 일부 사이트의 직접 열기는 오류 또는 내비게이션만 반환해 검색에 노출된 공식 텍스트만 사용했다. 특히 영화 호텔 배색, 단청 측정값, 문화적 정확한 배치의 일부는 확인 제한을 남겼다. 이 조사는 원본 작품·영화 스틸의 색 픽셀 측정 또는 새 생성 이미지 판정을 수행하지 않았다.

## 2. 현재 저장소에서 확인한 범위

조사 당시 HEAD는 `900bf2efdd17fbc6a6ef3aa340f3526b1e01f223`이며 주 작업 폴더에는 다른 작업의 수정·미추적 파일이 있었다. 이번 연구는 전용 증거 폴더에 작성했다. 현재 원본·코드·두 인덱스 manifest 등 120개 파일의 SHA-256을 기록했다. 이는 별도 파일 백업이나 모든 미추적 파일·이미지·shard의 완전한 보호 목록은 아니다.

최종 재확인에서 120개 가운데 117개의 해시가 일치했고 `photo_contracts.py`, `prompt_generator.py`, `audit_composed_prompt.py`의 해시 변화가 감지되었다. 이번 작업의 작성 경로는 이 연구 폴더에 한정되며 해당 코드를 되돌리거나 수정하지 않았다. 처음 snapshot과 [SOURCE-DRIFT.json](SOURCE-DRIFT.json)을 함께 남겼다. 기존 원본 후보·프로필·인덱스 manifest의 해시는 유지되었고 최종 연구 검사는 현재 로더로 다시 수행한다. 구현 시작 시 새 기준을 기록해야 한다.

|현재 범위|확인한 수|의미|
|---|---:|---|
|색 관계 전용 프로필|64|무채색/단색, 명도·채도, 강조, 공간 배색, 색광, 보정의 기본 관계|
|색 관계 전용 후보|89|color 69, color_grading 10, lighting 10|
|합성하여 실제 로드한 color 후보|152|다른 원본의 팔레트·스타일 후보를 포함|
|color_grading 후보|67|보정·예외 처리 등|
|lighting 후보|206|색광 외의 조명 관계를 포함|
|surface_material / texture 후보|335 / 164|재질 효과는 실제 존재하는 이 슬롯을 검토|
|전체 로드 프로필|1,922|색 외의 원본까지 포함한 조사 시점 값|
|등록된 candidate / visual_profile extension|53 / 35|source manifest 기준|

현재 `photo_prompt_source_manifest.json`을 `photo_source_manifest.SourceFiles`가 읽고, 후보는 `prompt_generator.load_json`, 프로필은 `load_visual_obligation_registry`가 순서대로 합성한다. 폴더에 파일만 만들어 놓으면 자동 로드된다는 전제는 틀리다. 현재 색·조명 의미의 원본과 인덱스는 서로 다른 파일이며, 생성 인덱스는 직접 편집하는 데이터 원본이 아니다.

이미 `teal_orange`, `luxury_black_gold`, `greige_camel_cream_quiet_palette`, `pearl_ivory_champagne_gold_palette` 같은 후보가 있다. 일부는 구체적인 owner 관계보다 짧은 색·스타일 설명을 제공한다. 반면 `cr_*` 데이터는 관계를 더 자세히 정의하지만 특정 팔레트·actual core owner의 대응은 별도 작업이다.

비슷한 기존 후보가 정확한 재사용 대상이라는 뜻도 아니다. 예를 들어 81번의 블랙·옥스블러드·본과 가까운 `obsidian_antique_gold_oxblood_palette`는 골드를 포함한다. 이 후보를 통째로 채택하면 원래 세 색의 뜻이 바뀐다. [RUNTIME-MAPPING.json](RUNTIME-MAPPING.json)에 이 위험을 명시했다.

## 3. 근거가 요구하는 시각 의미의 구분

### 3.1 색의 의미와 설계 의도

색과 감정의 연상에는 공통성과 문화·언어·지역 차이가 함께 관찰된다. 색상만이 아니라 채도·밝기도 연구에서 구분된다. 따라서 “핑크=로맨스”, “녹색=치유”, “빨강=식욕”, “검정·골드=고급”을 보편적 hard rule로 작성하지 않는다. **표현하려는 경험은 설계 의도**, 실제 가시적 증거는 색 영역·질감·표정·공간 등에서 따로 다룬다. [색과 감정의 다국가 연구](https://pubmed.ncbi.nlm.nih.gov/32900287/), [색상·채도·밝기 실험](https://pubmed.ncbi.nlm.nih.gov/28612080/)

색의 상대적 지각은 주변과 배치 맥락에 영향을 받는다. 이번 계획은 이를 동일 색칩의 근접 배경·면적·경계 비교로 검토할 수 있게 하되, 객관적으로 같은 RGB를 썼다는 사실과 같은 외관으로 보인다는 판정을 분리한다. [Albers Foundation](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

### 3.2 HEX, 색 공간, 물리적 색

원래 313개 색 코드는 제안된 sRGB 근사값이다. 코드의 정확한 보존은 입력 출처를 보존하는 일이며, 브랜드 공식값·안료색·복원색·광원 스펙트럼을 인증하는 일이 아니다.

[SWATCH-METRICS.json](SWATCH-METRICS.json)에 선형 sRGB 상대휘도, Oklab L/a/b, Oklch C/h, 색쌍 대비와 좌표 거리 계산을 남겼다. 비교 좌표는 sRGB D65와 Oklab의 2021년 직접 변환 계수를 사용한다. 저채도 색의 hue 표시는 `C < 0.02`에서 비워 두었다. 이 문턱은 연구표의 표시 편의용 가정이며 활성 의미 분류 규칙이 아니다. `delta_oklab_x100`은 CIEDE2000이나 “조화 점수”가 아니다. [CSS Color 4](https://www.w3.org/TR/2026/CRD-css-color-4-20260930/), [Oklab 저자의 설명](https://bottosson.github.io/posts/oklab/)

예를 들어 20번 아쿠아·화이트·실버의 색칩 Oklab L 범위는 약 0.174이고, 78번 실버·아이스 블루·화이트는 약 0.171이다. 79번 라벤더·블루·코럴은 약 0.116이다. 이 값은 실패 판정이 아니라 **색뿐 아니라 경계·표면·역할을 명확히 보아야 할 검토 단서**다. 제안 색칩의 수치이고, 작품·재료·사진의 측정값이 아니다.

사진에서는 밝기, 반사, 그림자, 출력 공간과 화이트밸런스에 따라 같은 표면의 여러 픽셀 값이 달라진다. 표면색 요청과 특정 평면 RGB 일치 요구를 구분한다. [ICC의 화면 색 관리 설명](https://www.color.org/displaycalibration/)

### 3.3 금색·은색과 재질

9·11·14·15·78번은 금속 반사와 주변의 비금속 면을 연결하는 좋은 사례다. 그러나 골드색은 금속일 수도, 페인트·종이·직물일 수도 있다. 반사가 요구된 경우에만 같은 표면의 기하를 따르는 하이라이트·상대적 어둠·주변 면의 차이를 검증한다. 무광 금속을 거울처럼 만들지 않으며 사진으로 금 순도·황동 조성·플래티넘을 확정하지 않는다. [PBRT 반사·투과](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [코팅과 산란](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials)

아르데코는 검정·금색 한 조합으로 수렴하지 않는다. 15번의 차가운 백색·크리스털·플래티넘 계열은 별도 사례 맥락으로 유지한다. [V&A Art Deco fashion](https://www.vam.ac.uk/articles/art-deco-fashion)

### 3.4 물체색·두 색 광원·보정

65번의 따뜻한 피사체/차가운 배경과 66번의 창 쪽 푸른빛/램프 쪽 앰버빛은 다른 mechanism이다. 73·88번에서 두 빛이 요구되면 서로 다른 수신 영역과 차폐·형상에 따른 footprint가 필요하다. 파란 벽과 주황 의상만으로 광원 둘을 입증하지 않는다. 색광의 hue와 CCT·화이트밸런스도 같은 데이터가 아니다. [Rosco Filter Facts](https://us.rosco.com/sites/default/files/content/resource/2022-10/Rosco_FilterFacts09_22.pdf), [ARRI 색 제어 문서](https://www.arri.com/en/lighting/led-spotlights/orbiter/faq)

67번의 공통 녹색 경향, 69번의 따뜻한 보정과 남겨야 할 올리브, 72번의 무채색 범위와 한 빨간 owner는 각각 범위를 명시한다. split toning은 그림자/하이라이트 경향이며 공간 좌우의 색광과 다르다. 실제 사용한 필터·소프트웨어는 결과 픽셀만으로 확정하지 않는다. [Adobe split toning](https://helpx.adobe.com/premiere-elements/desktop/applying-special-effects/add-split-tone-effect.html)

### 3.5 색면·패턴·연속 변화

18번 체크는 같은 carrier 위의 가로·세로 선과 교차 관계, 19번은 띠의 반복, 57번은 직선·직각 경계와 독립 원색 면이 핵심이다. 색만 서로 다른 물체에 흩어 놓으면 이 관계를 충족하지 않는다. 59번의 색 충돌도 형태·패턴과 별도로 검토한다. [MoMA 자료](https://www.moma.org/docs/press_archives/7380/releases/MOMA_1995_0060_46.pdf), [Design Museum](https://designmuseum.org/memphis)

36·74·79번의 공간 경로 변화, 그림의 밝기에 따른 gradient mapping, 100번의 수치에 따른 색 매핑을 분리한다. 색을 결정하는 독립 변수와 적용 owner가 달라 같은 색 목록만으로 서로 대체할 수 없다.

### 3.6 식품·전통 공예·기능

49–56번에서는 식품과 컵·접시·포장을 별도 owner로 다룬다. 특히 50번의 코발트는 컵의 색이고 커피·크림의 색이 아니다. 재료와 경계를 알아볼 단서를 주되 색만으로 맛·배합량·신선도·영양·안전성을 확정하지 않는다.

91번 청자의 회녹색과 92번 백자 몸체의 코발트 문양은 같은 도자기 표면과 연결한다. 유약 외관·문양과 재료/소성의 사실 상태는 별도다. [Met의 청자 설명](https://www.metmuseum.org/ko/essays/goryeo-celadon), [국립중앙박물관 청화백자](https://www.museum.go.kr/ENG/contents/E0401000000.do?relicRecommendId=519677&schM=view)

89·90번은 문화 체계와 현대 응용·특정 건축물의 복원을 구분한다. 단청의 정확한 측정값은 확보한 보고서 소개만으로 알 수 없다. [문화 기관의 오방색 소개](https://www.korea.net/Events/Overseas/view?articleId=23083), [단청 연구 보고서의 범위](https://portal.nrich.go.kr/kor/originalUsrView.do?info_idx=8716&menuIdx=1046)

95–97번은 미국 OSHA의 해당 표지 관계를 참고한 시각 응용이다. 표지 패널·본문·문자·기호를 나누며, 제안 HEX를 실제 규격색으로 사용하지 않는다. 안전 지시 표지와 비상구·의무 표지의 체계를 혼합하지 않는다. [OSHA 1910.145](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.145)

98–100번은 중앙값을 갖는 발산형·순위 없는 범주형·연속량의 순차형을 분리한다. 100번의 다섯 색은 대표점이며 전체 연속 Viridis 함수가 아니다. 같은 색칠을 했다는 사실로 데이터 타입·범례·수치 정확성을 입증하지 않는다. 정보는 라벨·기호 등 추가 단서와 연결한다. [Matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html), [WCAG Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

## 4. 13개 계열별 보강 범위

|계열 / 원래 번호|우선 보강할 시각 구조|주요 혼동 경계|권장 반영|
|---|---|---|---|
|미니멀·뉴트럴 1–8|명도 층, 천·벽·프레임 분리, 단일 강조 owner|무채색과 저채도, 재질과 전역 필터|기존 관계 재사용 + 특정 팔레트의 owner 예시|
|클래식·장식 9–16|어두운 면, 밝은 면, 작은 금속 반사|골드색과 금속, 스타일과 진품/재료|재질 효과를 분리한 선택형 조합|
|패션·브랜드 17–24|같은 천의 격자·띠·트리밍, 색의 작은 기능 영역|브랜드 공식값·소속, 패턴과 색 목록|출처는 연구에, 색과 carrier만 후보에|
|자연·흙 25–32|잎·천·목재·돌의 국소색 경계|녹색=치유, 러스트색=실제 부식|현재 material owner가 있는 경우만 적용|
|장소·계절 33–40|벽·문·바닥·물·하늘, 공간 경로와 작은 장식|색=실제 장소/계절/축제|장소가 주어진 core에서 배색만 보강|
|파스텔·뷰티 41–48|비슷한 채도/명도의 서로 다른 면과 경계|성별·연령, 밝음=동일한 색, 저대비=무관찰|명도·윤곽 증거를 함께 유지|
|음식 49–56|과육·잎·크림·구운 면·용기 분리|색으로 성분·맛·식욕·건강 확정|식품 owner와 용기 owner를 구분|
|그래픽·아트 57–64|직각/선/패턴/종이/인쇄색의 위치|스타일명=완전 구조, 출력 방식 추론|구조·재질·제작 사실을 분리|
|영화·사진 65–72|피사체/배경, 빛 수신 면, 보정 범위|물체색=광원=토닝, 작품의 모든 버전|영화 사실은 좁게 유지; 68번 사실 대조 보충|
|사이버·기술 73–80|색광·발광면·반투명·금속·공간 gradient|네온색=발광, 크롬색=금속, 기술=접근성|공통 mechanism을 재사용하고 기구 자동 추가 방지|
|다크·고딕 81–88|어두운 면 분리·작은 반사·국소 색광|색=피·독성·질병·감정·부식 이력|가시적 표면과 서사 의도를 분리|
|전통·공예 89–94|다섯 색 면/띠, 도자기 몸체/문양, 칠의 안팎|문화 규범·복원·공정의 확정|시각 응용 우선, 사례 사실은 별도 근거|
|기능·정보 95–100|패널/라벨/기호, 값·중앙·범주의 매핑|법규·접근성·데이터 진실성|문맥 검증 전 의미 라우팅 보류|

## 5. 데이터 초안의 구조

각 P001–P100 카드는 원래 키워드, 설계 의도, 명시적 시각 관계, 모든 색칩과 그 역할, 선택 가능한 owner, 구체적 실패 대체물, 출처 범위, 기존 후보·관계의 연결과 반영 우선순위를 포함한다.

후보의 `entry_proposal`에는 `concept_units`, `relations`, `affected_dimensions`, `affected_properties`, 긍정 검색 문장이 있다. source URL, 문화적 해석, 실패 문장과 연구 상태는 wrapper에 유지한다. **target의 `research_owner_*`는 일부러 표시한 연구 placeholder다. 실제 core의 target/property로 치환하기 전에는 compatibility 검증이나 채택에 사용하지 않는다.** 문자열이 validator를 통과해도 실제 owner 결합은 입증되지 않는다.

8·9·66·92번은 현재 component compiler를 사용하는 네 가지 형식 예시로 작성했다. 16개 component의 evidence/gate 투영을 검사했지만 4개를 새 프로필로 만들 것을 권하는 목록은 아니다. 기존 관계를 재사용할 수 있으면 새 프로필을 만들지 않는다.

## 6. 회귀·이미지·채택의 완료 기준

[REGRESSION-PLAN.json](REGRESSION-PLAN.json)의 64건은 관계의 긍정 요청, 인접한 실패 대체물, 사용자 재정의, owner/property lock 변형을 구분한 작성자 작성 명세다. 실행한 64개 테스트나 독립 holdout으로 보고하지 않는다.

[PIXEL-QUALIFICATION-PLAN.json](PIXEL-QUALIFICATION-PLAN.json)은 16개 mechanism에 대한 비교를 제안한다. 독립 baseline A, 기존 데이터 B, 좁은 채택 데이터 C를 같은 사전 동결 core에 연결하고 실제 채택·literal prompt·원본 픽셀을 각각 확인한다. 문화·기능 표지·데이터 맵 세 시나리오는 필요한 문맥·owner 지원을 확인하기 전 보류한다. 제안된 팔당 3회는 미래 평가 설계이며 실제 이미지 수는 0이다.

검색 hit, 후보 노출, 선택, 프롬프트 구절, 이미지의 각 요구 gate, 사용자의 선호는 별도 증거다. 누락·합쳐짐·owner 교환·불명확한 필수 증거는 `partial_is_fail`로 실패다. 이미지 도구에 seed 기능이 없으면 동일 seed를 약속하지 않는다. stochastic 출력 하나가 더 예쁘다는 이유로 원인을 확정하지 않는다. 선택이 0건이면 기존 baseline을 그대로 유지하는 것도 유효하다.

## 7. 남은 불확실성과 채택 전 처리

- “많이 사용된다”는 빈도·시장 조사는 수행하지 않았다. 공식 사용 사례와 설계 의도가 확인된 경우만 해당 사실 범위로 표기한다.
- 32개의 원래 사례 응용 별표를 이번에 전부 동일 수준으로 재검증한 것으로 해석하지 않는다.
- 68번 호텔 배색의 구체적 장면/시대/의상 색 관계, 18번의 정확한 전통 체크 폭·간격, 90번의 복원 측정값은 보충 근거가 필요하다.
- exact palette name이나 브랜드/스타일/감정 키워드는 일괄 hard alias로 넣지 않는다.
- 수치 맵의 데이터 의미와 기능 표지의 규정 준수는 현재 generic color 관계의 자동 확장 대상이 아니다. 기존 color-coding·시간/연속 장면 제외 범위를 약화하지 않는다.
- 연구 초안의 owner/property 대응, 실제 retrieval와 runtime/pixel 효과는 아직 미검증이다. 이를 해결하는 순서와 제출 증거는 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 있다.
