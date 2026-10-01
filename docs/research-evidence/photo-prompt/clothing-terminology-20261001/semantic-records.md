# 의류 시각 의미 레코드 초안

2026-10-01 · 연구 설계 자료 · 런타임 미반영 · 모든 노출/채택/픽셀 평가는 미실행.

용어군은 동의어 묶음이 아니다. 각 레코드의 특징과 영문 후보는 대안 변형을 포함하며, 실제 반영 전에 변형별 필수 부품을 따로 작성한다.

출처의 제한된 확인 사실은 [sources.json](sources.json)에 있으며, 아래 표현·경계·뷰·슬롯 선택은 연구자가 작성한 적용안이다.

## CT001 — 헨리의 부분 여밈

- 원문 분류: 1-1 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: Henley shirt, Henley, placket
- 소유 대상: `shirt` · 특징 풀: 목 아래 짧은 세로 플래킷 / 몸판 중간에서 끝나는 버튼 줄
- 혼동 경계: 칼라와 전면 전체 버튼 여밈은 별도 조건이다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S44](https://www.seamwork.com/sewing-tutorials/learn-to-sew-a-raglan-t-shirt)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a collarless shirt with a short button placket
- 후보 표현 B: a round-neck top with a partial center-front button opening
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT002 — 셔츠 칼라와 버튼다운

- 원문 분류: 1-1 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: Oxford shirt, button-down shirt, dress shirt
- 소유 대상: `shirt` · 특징 풀: 목둘레에 부착된 접힌 칼라 / 칼라 끝을 몸판에 고정하는 버튼은 선택 변형
- 혼동 경계: Oxford라는 직물·신발 의미와 button-front 여밈을 구분한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a shirt with collar points buttoned to the chest
- 후보 표현 B: a woven shirt with a fold-over collar and front button band
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT003 — 캠프칼라 셔츠

- 원문 분류: 1-1 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: camp-collar shirt, camp collar
- 소유 대상: `shirt` · 특징 풀: 벌어진 앞목 / 몸판 위로 누운 열린 칼라
- 혼동 경계: 봉제 방식과 오픈 넥라인을 동일한 조건으로 합치지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a shirt with a flat open camp collar
- 후보 표현 B: an open-neck shirt with collar wings lying on the chest
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT004 — 캐미솔·탱크·튜브톱

- 원문 분류: 1-1 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: camisole, tank top, tube top, sleeveless
- 소유 대상: `top` · 특징 풀: 어깨 끈의 폭과 위치 / 소매 유무 / 스트랩리스 상부 가장자리
- 혼동 경계: sleeveless가 자동으로 spaghetti strap 또는 strapless를 뜻하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a camisole suspended by narrow shoulder straps
- 후보 표현 B: a strapless tube-shaped top with an uninterrupted upper edge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 10개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT005 — 페플럼의 부착 위치

- 원문 분류: 1-1 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: peplum top, peplum
- 소유 대상: `bodice` · 특징 풀: 몸판 허리선에 연결된 짧은 플레어 / 연결선 아래 바깥으로 퍼지는 천
- 혼동 경계: 별도 스커트나 임의 허리 러플로 치환하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `front_waist`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a short flared peplum attached at the bodice waist
- 후보 표현 B: a fitted top with a waist-mounted flounce
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT006 — 가디건·풀오버

- 원문 분류: 1-2 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: cardigan, pullover, sweater, jumper
- 소유 대상: `knit_top` · 특징 풀: 앞목에서 밑단까지 열리는 앞판 또는 닫힌 몸판 / 여밈 유무
- 혼동 경계: 니트 소재가 앞트임 형식을 대신하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `front_torso`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: an open-front knitted cardigan
- 후보 표현 B: a closed-front knitted pullover
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 9개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT007 — 후드·스웨트 구조

- 원문 분류: 1-2 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: hoodie, sweatshirt, zip-up hoodie
- 소유 대상: `sweat_top` · 특징 풀: 목둘레에 연결된 후드 / 전면 지퍼 유무 / 손목과 밑단의 리브
- 혼동 경계: 후드가 있는 모든 옷을 스웨트셔츠로 고정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S04](https://cottonworks.com/encyclopedia-item/2-x-2-rib/)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a sweatshirt with a hood attached at the neckline
- 후보 표현 B: a hooded top with a full center-front zipper
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 4개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT008 — 케이블 니트

- 원문 분류: 1-2 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: cable-knit sweater, cable knit
- 소유 대상: `knit_panel` · 특징 풀: 로프처럼 교차하는 융기 띠 / 반복 교차 위치
- 혼동 경계: 납작하게 인쇄한 로프 그림은 실제 융기 조직의 대체가 아니다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S03](https://cottonworks.com/encyclopedia-item/jacquard-knitting/), [S04](https://cottonworks.com/encyclopedia-item/2-x-2-rib/)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: raised cable-knit braids crossing along the sweater
- 후보 표현 B: interlaced knitted ridges running down the front panel
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT009 — 트렌치의 독립 부품

- 원문 분류: 1-3 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: trench coat, storm flap, epaulette, D-ring
- 소유 대상: `coat` · 특징 풀: 어깨에 연결된 탭 / 등의 덮개 / 허리 벨트와 D형 고리
- 혼동 경계: 특정 브랜드의 모든 부품을 모든 트렌치에 강제하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S34](https://www.burberryplc.com/company/history/170-years-of-burberry)
- 시험 뷰: `front_and_back`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a trench coat with shoulder epaulettes and a belted waist
- 후보 표현 B: a rear storm flap lying over the coat back
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT010 — 봄버 재킷의 가장자리

- 원문 분류: 1-3 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: bomber jacket, flight jacket
- 소유 대상: `jacket` · 특징 풀: 짧은 재킷 몸판 / 손목과 허리 밑단의 모아지는 마감
- 혼동 경계: 가죽·항공 직업·특정 패치는 이름만으로 필수가 아니다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S04](https://cottonworks.com/encyclopedia-item/2-x-2-rib/)
- 시험 뷰: `front_torso`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a short jacket with gathered ribbed cuffs and hem
- 후보 표현 B: a zip-front bomber with a banded waistband
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT011 — 케이프·클록·판초

- 원문 분류: 1-3 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: cape, cloak, poncho, mantle
- 소유 대상: `outer_layer` · 특징 풀: 어깨 지지 / 팔을 싸는 소매 또는 팔의 통과 구멍 / 앞트임 또는 머리 통과 구멍
- 혼동 경계: 길이만으로 세 품목을 완전히 구분하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S29](https://www.vam.ac.uk/articles/the-syon-cope)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a shoulder-supported cape falling over the arms
- 후보 표현 B: a poncho with a central head opening and continuous side drape
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 4개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT012 — 싱글·더블브레스트

- 원문 분류: 1-3 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: blazer, single-breasted, double-breasted
- 소유 대상: `jacket` · 특징 풀: 앞판 겹침 폭 / 하나 또는 두 열의 버튼 배치 / 라펠
- 혼동 경계: 장식 버튼 열만으로 작동 여밈을 보장하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_torso`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a jacket with two visible columns of front buttons
- 후보 표현 B: a single-breasted jacket with a narrow front overlap
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 9개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT013 — 바지 다리선

- 원문 분류: 1-4, 3-1 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: straight-leg, tapered, bootcut, flare, wide-leg
- 소유 대상: `trousers` · 특징 풀: 무릎 대비 밑단 폭 / 허벅지부터 밑단까지의 여유 / 양 다리의 분리
- 혼동 경계: 밑단 폭 변화와 착용자 다리 체형은 다른 변수다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S18](https://www.levi.com/US/en_US/features/men-jeans-guide)
- 시험 뷰: `full_lower`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: trousers narrowing from knee to ankle
- 후보 표현 B: bootcut trousers widening below the knee
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 15개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT014 — 밑위·기장

- 원문 분류: 1-4, 3-1 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: high-rise, mid-rise, low-rise, cropped, ankle-length
- 소유 대상: `trousers` · 특징 풀: 허리밴드가 놓이는 위치 / 밑단과 발목의 거리
- 혼동 경계: 하이웨이스트를 다리 연장·허리 축소로 번역하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S18](https://www.levi.com/US/en_US/features/men-jeans-guide), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `full_lower`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a waistband sitting above the natural waist
- 후보 표현 B: cropped trouser hems ending above the ankles
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 67개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT015 — 카고 주머니

- 원문 분류: 1-4 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: cargo pants, cargo pocket, utility pocket
- 소유 대상: `trousers` · 특징 풀: 다리 바깥면의 패치 포켓 / 입구 위 덮개 / 필요 시 주머니 거싯
- 혼동 경계: 카고의 군인 정체성·내용물·수납 기능은 별도다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S43](https://www.seamwork.com/sewing-tutorials/conquering-the-welt)
- 시험 뷰: `side_lower_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: flapped patch pockets sewn onto the outer trouser legs
- 후보 표현 B: raised cargo pockets attached at thigh level
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT016 — 오버롤·멜빵바지

- 원문 분류: 1-4 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: overalls, dungarees, bib overall, salopettes
- 소유 대상: `trousers` · 특징 풀: 허리에서 가슴으로 올라오는 비브 / 비브에 연결된 어깨 스트랩 / 분리된 다리
- 혼동 경계: 단순 서스펜더 바지와 비브 구조를 구분한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: trouser overalls with a chest bib and shoulder straps
- 후보 표현 B: a bib panel attached above the trouser waistband
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT017 — 스커트 윤곽

- 원문 분류: 1-5 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: A-line skirt, pencil skirt, circle skirt, mermaid skirt
- 소유 대상: `skirt` · 특징 풀: 허리부터 밑단까지의 폭 변화 / 하부에서 퍼지기 시작하는 위치
- 혼동 경계: A-line과 원형 재단은 같은 정보가 아니다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `full_lower`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a skirt gradually widening from waist to hem
- 후보 표현 B: a narrow skirt flaring below the knees
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT018 — 스커트 레이어

- 원문 분류: 1-5 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: wrap skirt, tiered skirt, pleated skirt, skort
- 소유 대상: `skirt` · 특징 풀: 겹치는 앞판 / 단을 이루는 연결선 / 필요 시 안쪽 반바지
- 혼동 경계: wrap은 단순 사선 무늬가 아니다. skort 내부는 가려질 수 있다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_lower`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a wrap skirt with one front panel overlapping the other
- 후보 표현 B: a skirt with separate gathered horizontal tiers
- 기존 데이터 비교 포인터: exact profile 1개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT019 — 점프수트·롬퍼·보디수트

- 원문 분류: 1-6 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: jumpsuit, romper, playsuit, bodysuit, unitard
- 소유 대상: `one_piece` · 특징 풀: 몸판과 하의의 연속 연결 / 분리된 다리 부분의 길이 / 개구와 몸에 붙는 정도
- 혼동 경계: 길이·여유·가랑이 연결을 따로 적고 상품명이 겹칠 수 있음을 남긴다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a one-piece garment with a torso joined to long trouser legs
- 후보 표현 B: a short-legged romper with a continuous bodice
- 기존 데이터 비교 포인터: exact profile 1개 / candidate lexical 9개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT020 — 슬립·랩·셔츠 드레스

- 원문 분류: 1-6 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: slip dress, wrap dress, shirt dress
- 소유 대상: `dress` · 특징 풀: 상체 지지 방식 / 앞판 중첩과 묶음 / 셔츠 칼라·플래킷
- 혼동 경계: 광택만으로 slip dress, 버튼만으로 shirt dress 전체를 판정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a wrap dress with overlapping front panels tied at the side
- 후보 표현 B: a dress suspended by narrow shoulder straps
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 7개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT021 — 수트와 개별 재킷

- 원문 분류: 1-6 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: suit, two-piece suit, three-piece suit, tuxedo
- 소유 대상: `ensemble` · 특징 풀: 재킷·하의·선택적 베스트를 개별 소유자로 구분 / 서로 대응하는 천과 색
- 혼동 경계: 단일 재킷을 수트 전체와 동일시하거나 체형을 자동 조정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a coordinated jacket and trouser ensemble
- 후보 표현 B: a three-piece suit with a separate waistcoat beneath the jacket
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT022 — 브라 형태 변수

- 원문 분류: 1-7 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: bra, bralette, balconette, plunge bra, longline bra
- 소유 대상: `bra` · 특징 풀: 컵의 윗선 / 중앙 브리지 높이 / 밴드의 세로 폭 / 끈 유무
- 혼동 경계: 컵 크기·가슴 형상·지지력·underwire 존재를 명칭 하나로 확정하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S10](https://clothhabit.com/bra-anatomy/)
- 시험 뷰: `garment_flatlay`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a bra with a low center bridge and distinct cups
- 후보 표현 B: a longline bra band extending below the cups
- 기존 데이터 비교 포인터: exact profile 1개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT023 — 코르셋·뷔스티에

- 원문 분류: 1-7 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: corset, bustier, corset top, stays
- 소유 대상: `structured_top` · 특징 풀: 길이 / 컵 경계 / 보닝 채널 / 선택한 버스크·레이싱 여밈
- 혼동 경계: 상품 분류가 겹친다. 잘록한 체형만으로 코르셋 구조를 대신하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S11](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S10](https://clothhabit.com/bra-anatomy/)
- 시험 뷰: `garment_flatlay`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a structured top with visible vertical boning channels
- 후보 표현 B: a corset front closed by paired busk hooks
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 52개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT024 — 잠옷·로브·슬립

- 원문 분류: 1-7 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: nightgown, chemise, robe, peignoir, pyjamas
- 소유 대상: `sleepwear` · 특징 풀: 원피스 또는 상하 분리 / 앞을 여미는 로브 / 벨트 연결
- 혼동 경계: 잠옷 이름으로 노출·성적 상황·착용자의 성향을 추가하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a loose robe wrapped and tied at the waist
- 후보 표현 B: a separate pajama shirt and trouser set
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 40개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT025 — 가터와 서스펜더의 문맥

- 원문 분류: 1-7, 4-2 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: garter, garter belt, suspenders, stockings
- 소유 대상: `legwear_or_waist_support` · 특징 풀: 허리 벨트에서 스타킹 윗단으로 이어지는 끈 / 허벅지 고리 / 바지 멜빵은 별도
- 혼동 경계: 영국 suspenders와 바지 braces/미국 suspenders의 대상 차이를 해소한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S10](https://clothhabit.com/bra-anatomy/), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `garment_flatlay`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: suspender straps joining a waist belt to stocking tops
- 후보 표현 B: a separate garter band encircling the thigh
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 8개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT026 — 스포츠 저지와 원단

- 원문 분류: 1-8 · 우선순위: P0 · 제안 슬롯: `wardrobe_style`
- 관련 용어: jersey, sports jersey, track jacket, leggings
- 소유 대상: `sports_garment` · 특징 풀: 품목 형태와 직물 조직을 별도 기술 / 팀 표시가 요청되었는지
- 혼동 경계: jersey fabric으로 유니폼 번호·로고를 자동 추가하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S03](https://cottonworks.com/encyclopedia-item/jacquard-knitting/), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_torso`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a sports jersey with the requested front number
- 후보 표현 B: a plain jersey-knit top without team markings
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 8개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT027 — 어댑티브 의류

- 원문 분류: 1-8 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: adaptive clothing, magnetic closure
- 소유 대상: `garment_closure` · 특징 풀: 요청된 접근 여밈 위치 / 열린 상태에서 실제 여밈 부품
- 혼동 경계: 닫힌 버튼 외관으로 자석·착용자의 장애·착용 편의성을 판정하지 않는다
- 출처 범위: `product_example` · 조사 상태: `variant_example_only_design_unqualified` · [S33](https://usa.tommy.com/en/tommy-adaptive/mens-adaptive/tops/regular-fit-brushed-cotton-shirt/MW46777-YBR.html)
- 시험 뷰: `closure_open_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: an opened shirt placket revealing magnetic fasteners
- 후보 표현 B: a garment with accessible front closure tabs
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT028 — 기능성·작업복

- 원문 분류: 1-8 · 우선순위: P1 · 제안 슬롯: `wardrobe_style`
- 관련 용어: workwear, PPE, rainwear, wetsuit, compression wear
- 소유 대상: `functional_garment` · 특징 풀: 외부 테이프·반사띠·재킷/수트 구조 / 요청된 활동 맥락
- 혼동 경계: 방수·인증·압박 성능·직업은 정지 이미지로 확정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S34](https://www.burberryplc.com/company/history/170-years-of-burberry), [S38](https://cottonworks.com/learning-hub/denim/denim-basics/)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: workwear with reflective strips sewn across the jacket
- 후보 표현 B: a close-fitting full-body wetsuit silhouette
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT029 — 몸판과 비브

- 원문 분류: 2-1 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: bodice, panel, yoke, bib, gusset
- 소유 대상: `garment_body` · 특징 풀: 옷 몸통 영역 / 분리 봉제 경계 / 목·어깨 쪽 요크 또는 가슴 비브
- 혼동 경계: bodice는 보디수트 품목이 아니다. yoke의 위치는 앞/뒤 변형으로 지정한다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf), [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `front_and_back`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a shoulder yoke joined to the shirt back
- 후보 표현 B: a distinct chest bib panel attached to the garment
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 31개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT030 — 고어·고데·브라 고어

- 원문 분류: 2-1 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: gore, godet, bridge, cradle
- 소유 대상: `skirt_or_bra` · 특징 풀: 스커트 세로 패널 / 하부 삽입 쐐기 / 브라 두 컵 사이 연결부
- 혼동 경계: 혈흔 문맥 gore 및 서로 다른 의복 소유자와 충돌하지 않게 sense를 분리한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S10](https://clothhabit.com/bra-anatomy/)
- 시험 뷰: `garment_flatlay`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a triangular godet inserted into the skirt seam
- 후보 표현 B: the small bridge joining the two bra cups
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT031 — 프린세스 심과 다트

- 원문 분류: 2-1 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: princess seam, dart, bust dart, waist dart
- 소유 대상: `bodice_panel` · 특징 풀: 다트는 한 점으로 좁아지는 봉제 접힘 / 프린세스는 곡선 패널 연결선
- 혼동 경계: 일반 주름·인쇄 선·프린세스 라인 드레스 전체와 구분한다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S41](https://www.sewing.org/files/guidelines/11_310_princess_seams.pdf), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `front_torso_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: curved princess seams joining the bodice panels
- 후보 표현 B: a short tapered dart ending near the bust
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT032 — 안감·페이싱·심지

- 원문 분류: 2-1 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: lining, facing, interfacing, interlining
- 소유 대상: `garment_internal` · 특징 풀: 안쪽을 덮는 층 / 개구 가장자리 안쪽의 부분 층 / 층 사이 보강재
- 혼동 경계: 겉옷의 빳빳함만으로 내부 심지를 판정하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `inside_garment_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: an inside facing finishing the neckline edge
- 후보 표현 B: a separate lining visible inside the opened jacket
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 47개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT033 — 결과 바이어스

- 원문 분류: 2-1 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: grainline, warp, weft, bias cut
- 소유 대상: `fabric_panel` · 특징 풀: 결 방향과 절단 방향 / 천 패널의 드레이프
- 혼동 경계: 인쇄 사선이나 부드러운 주름만으로 45도 재단을 확정하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a fabric panel cut diagonally across the woven grain
- 후보 표현 B: a bias-cut skirt falling in fluid diagonal folds
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT034 — 기본 넥라인 경계

- 원문 분류: 2-2 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: crew neck, jewel neckline, round neck, U-neck, V-neck, scoop neck
- 소유 대상: `top_opening` · 특징 풀: 목 개구의 둥근 곡선 또는 V 꼭짓점 / 목과 개구의 거리
- 혼동 경계: 넥라인은 부착 칼라와 독립이며 jewel/crew 같은 중첩 명칭은 수치 없는 절대 경계로 묶지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a neckline forming a clear centered V
- 후보 표현 B: a broad rounded scoop opening below the base of the neck
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT035 — 스퀘어·보트넥

- 원문 분류: 2-2 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: square neck, boat neck, bateau
- 소유 대상: `top_opening` · 특징 풀: 스퀘어의 모서리와 수평 밑선 / 보트의 넓고 얕은 가로 개구
- 혼동 경계: 넓다는 이유로 오프숄더와 동일시하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a square neckline with distinct lower corners
- 후보 표현 B: a wide shallow boat neckline spanning the collarbones
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT036 — 스위트하트

- 원문 분류: 2-2 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: sweetheart neckline
- 소유 대상: `bodice_opening` · 특징 풀: 중앙으로 들어가는 낮은 골 / 좌우 두 개의 둥근 상부 곡선
- 혼동 경계: 원단의 하트 무늬나 단순 깊은 V로 대체하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a sweetheart neckline with two curved lobes and a center dip
- 후보 표현 B: a bodice edge shaped into paired rounded arcs
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT037 — 카울·키홀

- 원문 분류: 2-2 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: cowl neck, keyhole neckline
- 소유 대상: `top_opening` · 특징 풀: 목 아래 늘어진 천 접힘 / 메인 넥라인 아래의 작은 독립 개구
- 혼동 경계: 드레이프와 cutout을 합치거나 천 주름을 목걸이로 치환하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a cowl neckline draping in loose fabric folds
- 후보 표현 B: a small keyhole opening below the neckline
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT038 — 홀터·원숄더·오프숄더

- 원문 분류: 2-2 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: halter neck, one-shoulder, off-the-shoulder, cold shoulder
- 소유 대상: `top_support` · 특징 풀: 목 둘레로 연결된 지지 / 한쪽 어깨 지지 / 상부 가장자리의 어깨 아래 위치 / 독립 어깨 컷아웃
- 혼동 경계: 홀터는 개구 모양과 완전한 동의어가 아니다. 끈과 소매는 따로 잠근다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_and_back_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a halter strap passing around the back of the neck
- 후보 표현 B: a neckline resting below both shoulders with attached sleeves
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 8개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT039 — 하이넥 계열

- 원문 분류: 2-2 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: turtleneck, mock neck, funnel neck
- 소유 대상: `neck_band` · 특징 풀: 목을 둘러싸는 세로 천 높이 / 접혀 돌아가는 밴드 여부 / 벌어지는 상부
- 혼동 경계: 모든 높은 목둘레를 stand collar로 자동 변환하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a high neck band folded back around the neck
- 후보 표현 B: an upright mock neck with an unfolded upper edge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT040 — 칼라의 구조

- 원문 분류: 2-3 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: collar, collar stand, point collar, spread collar
- 소유 대상: `shirt_collar` · 특징 풀: 목둘레 받침 / 뒤집힌 칼라 날개 / 칼라 끝 사이의 벌어짐
- 혼동 경계: 목 개구의 형태·button front와 다른 변수다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `collar_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a fold-over collar mounted on a narrow collar stand
- 후보 표현 B: widely spaced collar points framing the front opening
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT041 — 스탠드·피터팬·세일러 칼라

- 원문 분류: 2-3 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: stand collar, Mandarin collar, Peter Pan collar, sailor collar
- 소유 대상: `garment_collar` · 특징 풀: 선 목 밴드 / 둥근 칼라 끝 / 등 쪽 큰 네모 flap와 앞쪽 연결
- 혼동 경계: 세일러 칼라로 학생·해군 정체성이나 국적을 추론하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `front_and_back_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a flat collar with rounded Peter Pan ends
- 후보 표현 B: a sailor collar with a broad rectangular back panel
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT042 — 라펠 분기

- 원문 분류: 2-3 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: lapel, notch lapel, peak lapel, shawl lapel, gorge
- 소유 대상: `jacket_front` · 특징 풀: 앞판이 밖으로 접히는 영역 / 칼라와 만나는 notch/상향 point/연속 곡선
- 혼동 경계: 재킷 라펠과 독립 숄을 구분한다. 한쪽 미세 모서리는 원거리 게이트로 삼지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `collar_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: notched lapels with a visible step at the collar junction
- 후보 표현 B: continuous rounded shawl lapels following the jacket opening
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT043 — 러프·자보·타이 칼라

- 원문 분류: 2-3 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: ruff, jabot, pussy-bow collar, ascot, cravat
- 소유 대상: `neck_accessory_or_trim` · 특징 풀: 목 둘레의 주름 고리 / 가슴 앞의 프릴 / 목 리본 매듭과 내려오는 끝
- 혼동 경계: 넥라인·목걸이·탈착 장식·칼라 일부의 소유자를 구분한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S27](https://fashionhistory.fitnyc.edu/passementerie/), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a pleated ruff encircling the neck
- 후보 표현 B: a fabric bow tied at the blouse neckline with hanging ends
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT044 — 래글런·셋인·드롭숄더

- 원문 분류: 2-4 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: raglan, set-in sleeve, drop shoulder, armhole
- 소유 대상: `sleeve_attachment` · 특징 풀: 래글런은 목에서 겨드랑이로 연결되는 선 / 셋인은 암홀 경계 / 드롭은 팔 쪽으로 내려간 어깨 봉제
- 혼동 경계: 배색·포즈·넓은 어깨만으로 소매 재단을 대체하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf), [S44](https://www.seamwork.com/sewing-tutorials/learn-to-sew-a-raglan-t-shirt)
- 시험 뷰: `front_upper_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: diagonal raglan seams running from neck to underarm
- 후보 표현 B: a dropped shoulder seam positioned below the shoulder point
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT045 — 돌먼·기모노 소매

- 원문 분류: 2-4 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: dolman sleeve, batwing sleeve, kimono sleeve
- 소유 대상: `sleeve_body_joint` · 특징 풀: 몸판과 소매의 연속 영역 / 넓고 낮은 겨드랑이 / 끝으로 좁아지는 변형
- 혼동 경계: 품목 kimono·오비·일본풍 프린트가 필수가 아니다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `arms_apart_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a batwing sleeve with a deep low underarm
- 후보 표현 B: a cut-on sleeve continuing from the bodice without a standard armhole seam
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT046 — 퍼프와 기고

- 원문 분류: 2-4 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: puff sleeve, leg-of-mutton sleeve, gigot sleeve
- 소유 대상: `sleeve` · 특징 풀: 위팔 볼륨 / 아래팔까지의 폭 변화 / 모아지는 연결 위치
- 혼동 경계: 한쪽의 부풀어 보이는 주름만으로 전체 소매를 분류하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S06](https://fashionhistory.fitnyc.edu/leg-of-mutton-sleeves/)
- 시험 뷰: `full_arm_side`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a full upper sleeve tapering closely to the wrist
- 후보 표현 B: a short puff sleeve gathered into the shoulder and sleeve edge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT047 — 비숍·벨·벌룬 소매

- 원문 분류: 2-4 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: bishop sleeve, bell sleeve, balloon sleeve
- 소유 대상: `sleeve` · 특징 풀: 손목 앞 볼륨과 좁은 커프 / 아래로 퍼지는 열린 끝 / 전체 부피
- 혼동 경계: bishop와 balloon의 상품 명명 중첩을 허용하고 손목 마감으로 후보를 구체화한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S08](https://www.fitnyc.edu/museum/exhibitions/statement-sleeves/index.php), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `full_arm_side`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a full bishop sleeve gathered into a narrow wrist cuff
- 후보 표현 B: an open bell sleeve widening toward its lower edge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT048 — 플러터·튤립 소매

- 원문 분류: 2-4 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: flutter sleeve, tulip sleeve, petal sleeve
- 소유 대상: `sleeve_edge` · 특징 풀: 짧고 자유롭게 퍼지는 천 / 꽃잎처럼 겹치는 끝 패널
- 혼동 경계: 어깨 러플 장식과 작동하는 소매 개구를 구분한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_upper_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: short flutter sleeves with loose flared edges
- 후보 표현 B: two overlapping petal-shaped sleeve panels
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT049 — 커프의 겹침·여밈

- 원문 분류: 2-4 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: cuff, barrel cuff, French cuff, double cuff, cufflink
- 소유 대상: `shirt_sleeve_end` · 특징 풀: 손목 끝 밴드 / 접힌 이중 층 / 맞닿는 끝과 커프링크
- 혼동 경계: 팔찌 cuff와 소매 cuff는 다른 소유자다. French cuff를 특정 국가 사람과 연결하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `wrist_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a folded double cuff joined by a cufflink
- 후보 표현 B: a buttoned cuff band at the sleeve end
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT050 — 소매 길이

- 원문 분류: 2-4 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: cap sleeve, short sleeve, three-quarter sleeve, bracelet sleeve, long sleeve
- 소유 대상: `sleeve` · 특징 풀: 소매 끝과 위팔·팔꿈치·손목의 관계 / 팔을 따라 연속인 천
- 혼동 경계: 포즈에 의해 소매가 올라간 것을 원래 기장으로 판정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `full_arm_side`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: sleeves ending just above the wrists
- 후보 표현 B: three-quarter sleeves ending between elbow and wrist
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT051 — 여밈 부품 분기

- 원문 분류: 2-5 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: button, buttonhole, snap, press stud, hook and eye
- 소유 대상: `garment_closure` · 특징 풀: 단추와 구멍의 짝 / 맞물리는 스냅 두 반쪽 / 훅과 고리
- 혼동 경계: 장식 단추·리벳·스냅 외관을 실제 작동 방식과 동일시하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `closure_open_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a button aligned with its stitched buttonhole
- 후보 표현 B: an opened edge showing paired hook-and-eye fasteners
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 31개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT052 — 지퍼 노출

- 원문 분류: 2-5 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: zipper, invisible zipper, exposed zipper, zipper pull
- 소유 대상: `garment_closure` · 특징 풀: 맞물린 치열 / 슬라이더와 풀 / 치열을 숨기는 접힌 가장자리
- 혼동 경계: 보이지 않는 지퍼를 외관 사진만으로 PASS 처리하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `closure_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: an exposed zipper with visible teeth and slider
- 후보 표현 B: a concealed zipper seam with only the small pull visible
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 14개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT053 — 플래킷과 플라이

- 원문 분류: 2-5 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: placket, button placket, fly, zip fly, button fly
- 소유 대상: `shirt_or_trousers` · 특징 풀: 상의 개구 보강 밴드 / 바지 앞 개구를 덮는 천
- 혼동 경계: 전면 버튼 줄과 바지 fly를 같은 소유자로 묶지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S18](https://www.levi.com/US/en_US/features/men-jeans-guide)
- 시험 뷰: `closure_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a narrow button placket running down the shirt front
- 후보 표현 B: a trouser fly covered by an overlapping fabric flap
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT054 — 프로그·토글 여밈

- 원문 분류: 2-5 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: frog closure, Chinese frog, loop closure, toggle
- 소유 대상: `garment_closure` · 특징 풀: 두 앞판에 각각 연결된 끈 고리·매듭 또는 막대 / 서로 맞물리는 짝
- 혼동 경계: 장식 매듭 한 개와 실제 여밈의 두 끝점을 구분한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S23](https://www.roots.gov.sg/ich-landing/ich/cheongsam-tailoring), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `closure_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: paired knotted frogs bridging the garment opening
- 후보 표현 B: a toggle passing through a cord loop on the opposite front panel
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT055 — 레이싱과 아이렛

- 원문 분류: 2-5 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: lacing, lace-up, eyelet, grommet
- 소유 대상: `garment_opening` · 특징 풀: 양쪽 가장자리 구멍 / 구멍을 통과해 반복 교차하는 끈 / 선택한 조임 지점
- 혼동 경계: 천 위의 X 무늬나 단순 끈 리본을 레이싱으로 대신하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S11](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `closure_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: cord lacing crossing between two rows of eyelets
- 후보 표현 B: a lace threaded through reinforced garment openings
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 8개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT056 — 스트랩·슬라이더·버클

- 원문 분류: 2-5 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: strap, slider, buckle, D-ring, adjuster
- 소유 대상: `garment_or_bag_strap` · 특징 풀: 끈의 두 부착 끝점 / 길이 조절 고리 / 버클에 통과하는 끈
- 혼동 경계: 공중에 뜬 하드웨어·끊긴 끈·물건 소유자 전환을 실패로 둔다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S10](https://clothhabit.com/bra-anatomy/), [S34](https://www.burberryplc.com/company/history/170-years-of-burberry)
- 시험 뷰: `hardware_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a shoulder strap passing through an adjustment slider
- 후보 표현 B: a belt threaded through a buckle attached at its end
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 64개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT057 — 타이와 드로스트링

- 원문 분류: 2-5 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: tie, drawstring, drawcord, casing
- 소유 대상: `garment_edge` · 특징 풀: 노출 매듭 / 터널 안으로 들어가는 끈 / 출구 두 개와 모아지는 가장자리
- 혼동 경계: 같은 끈 외관이어도 외부 벨트·내부 casing은 다른 관계다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `front_waist`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a drawstring emerging from two waistband openings
- 후보 표현 B: a fabric tie joining the garment fronts in a visible knot
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT058 — 주머니의 입구·부착

- 원문 분류: 2-6 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: patch pocket, welt pocket, jet pocket, in-seam pocket
- 소유 대상: `garment_pocket` · 특징 풀: 몸판 위 패치 경계 / 개구 가장자리 웰트 / 기존 옆솔기에 놓인 입구
- 혼동 경계: 외관 입구와 내부 포켓백·실제 수납 가능성을 분리한다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S43](https://www.seamwork.com/sewing-tutorials/conquering-the-welt), [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `pocket_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a patch pocket stitched around three outer edges
- 후보 표현 B: a narrow welt framing a slit pocket opening
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT059 — 플랩·벨로즈 포켓

- 원문 분류: 2-6 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: flap pocket, bellows pocket, gusset pocket
- 소유 대상: `garment_pocket` · 특징 풀: 입구 위 덮개 / 측면 거싯이 만드는 입체 돌출
- 혼동 경계: 장식 덮개 아래 포켓 존재·고정 부품 작동을 별도로 확인한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S43](https://www.seamwork.com/sewing-tutorials/conquering-the-welt), [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `pocket_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a pocket flap overlapping the pocket mouth
- 후보 표현 B: a raised pocket with folded side gussets
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT060 — 허리밴드와 벨트고리

- 원문 분류: 2-6 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: waistband, belt loop, paperbag waist
- 소유 대상: `trousers_or_skirt` · 특징 풀: 상부 띠 / 허리밴드에 두 끝이 연결된 고리 / 끈 위로 모인 천
- 혼동 경계: 벨트고리를 벨트 자체나 몸의 허리 경계와 동일시하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `front_waist_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: belt loops attached above and below the waistband
- 후보 표현 B: a gathered paperbag edge rising above a tied waist
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 32개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT061 — 헴·슬릿·벤트

- 원문 분류: 2-6 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: hem, slit, vent, kick pleat
- 소유 대상: `garment_lower_edge` · 특징 풀: 마감 가장자리 / 봉제가 중단된 개구 / 겹치는 vent 천
- 혼동 경계: 찢어진 손상·무늬·다리의 벌어진 자세와 구분한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `back_lower_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a side slit opening upward from the skirt hem
- 후보 표현 B: overlapping fabric panels forming a back vent
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 76개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT062 — 트레인·꼬리·비대칭 밑단

- 원문 분류: 2-6 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: train, tailcoat tail, high-low hem, drop-tail hem
- 소유 대상: `garment_hem` · 특징 풀: 몸판과 연결된 뒤쪽 연장 / 앞뒤 기장 차이 / 지면 접촉 여부
- 혼동 경계: 뒤로 늘어진 천을 독립 스카프·그림자·배경으로 바꾸지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `side_full`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a dress train continuing from the rear hem onto the floor
- 후보 표현 B: a shirt hem cut longer at the back than at the front
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT063 — 플리츠 방향

- 원문 분류: 2-7 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: knife pleat, box pleat, inverted pleat, accordion pleat
- 소유 대상: `fabric_fold` · 특징 풀: 같은 방향 접힘 또는 마주보는 접힘 / 산과 골의 반복 / 접힘 고정 위치
- 혼동 경계: 인쇄 세로줄·랜덤 주름·개더를 플리츠 위상으로 대체하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `fold_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: parallel knife pleats folding in the same direction
- 후보 표현 B: paired folds meeting to form an inverted box pleat
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT064 — 개더·셔링·스모킹

- 원문 분류: 2-7 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: gather, shirring, smocking, ruche
- 소유 대상: `fabric_panel` · 특징 풀: 모아진 분량 / 평행 봉제 줄 / 선택한 자수 연결 패턴
- 혼동 경계: smocking의 모든 변형을 탄성사 셔링 또는 벌집 무늬로 치환하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S31](https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring), [S32](https://arxiv.org/abs/2401.05533)
- 시험 뷰: `stitch_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: parallel rows of stitching gathering the waist panel
- 후보 표현 B: decorative smocking stitches joining small fabric pleats
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 4개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT065 — 러플과 플라운스

- 원문 분류: 2-7 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: ruffle, frill, flounce
- 소유 대상: `garment_trim` · 특징 풀: 부착 가장자리에 모아진 천 / 자유 가장자리의 물결 / 부착 위치
- 혼동 경계: 목·소매·밑단 사이 소유자 이동을 막고 재단 방식은 외관과 구분한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `trim_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a gathered ruffle attached along the sleeve edge
- 후보 표현 B: a flared flounce sewn around the skirt hem
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT066 — 파이핑·바인딩·웰트

- 원문 분류: 2-7 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: piping, binding, welt, tape
- 소유 대상: `seam_or_edge` · 특징 풀: 봉제 사이 돌출한 둥근 선 / 원단 가장자리를 감싼 띠 / 주머니 입구 띠
- 혼동 경계: 같은 색 선이라고 seam piping·edge binding·pocket welt를 동의어로 합치지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S43](https://www.seamwork.com/sewing-tutorials/conquering-the-welt)
- 시험 뷰: `edge_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: rounded piping inserted between two garment panels
- 후보 표현 B: a narrow binding wrapping around the neckline edge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 15개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT067 — 아플리케·자수·컷워크

- 원문 분류: 2-7 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: appliqué, embroidery, cutwork, broderie anglaise
- 소유 대상: `fabric_surface` · 특징 풀: 겉에 덧댄 조각 경계 / 실 땀 / 천을 뚫은 구멍과 마감
- 혼동 경계: 프린트 무늬로 입체 조각·실·실제 개구를 대체하지 않는다
- 출처 범위: `product_example` · 조사 상태: `variant_example_only_design_unqualified` · [S24](https://www.roots.gov.sg/Collection-landing/listing/1148958), [S29](https://www.vam.ac.uk/articles/the-syon-cope), [S30](https://data.fitzmuseum.cam.ac.uk/id/object/117565)
- 시험 뷰: `stitch_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: fabric appliqué shapes stitched onto the outer panel
- 후보 표현 B: embroidered cutwork holes edged with small stitches
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 29개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT068 — 술·프린지·브레이드

- 원문 분류: 2-7 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: tassel, fringe, braid, passementerie, cord
- 소유 대상: `garment_or_accessory_trim` · 특징 풀: 한 뭉치의 실 끝 / 가장자리를 따라 늘어선 다수 끝 / 엮인 띠
- 혼동 경계: 독립 술과 연속 프린지의 위치·개수는 요청 변형에 맞춘다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S21](https://encykorea.aks.ac.kr/Article/E0012731), [S27](https://fashionhistory.fitnyc.edu/passementerie/)
- 시험 뷰: `trim_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a single thread tassel hanging from a knotted cord
- 후보 표현 B: a row of fringe attached along the garment edge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 8개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT069 — 스팽글·비드·스터드

- 원문 분류: 2-7 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: sequin, paillette, bead, stud, rivet
- 소유 대상: `garment_surface` · 특징 풀: 납작한 반사 디스크 / 입체 비드 / 금속 돌출 장식 또는 고정점
- 혼동 경계: 금속 광택 하나로 장식·리벳·보석을 동일시하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S45](https://www.firemountaingems.pro/learn/reference/essential-resources/encyclobeadia/)
- 시험 뷰: `stitch_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: small flat sequins overlapping across the fabric
- 후보 표현 B: raised beads stitched along the collar edge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT070 — 컵과 컵 솔기

- 원문 분류: 2-8 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: cup, cup seam, foam cup, molded cup
- 소유 대상: `bra_cup` · 특징 풀: 두 컵의 경계 / 선택한 컵 패널 연결선 / 매끈한 컵 표면
- 혼동 경계: 매끈한 표면만으로 내부 폼·패딩·제조법을 확정하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S10](https://clothhabit.com/bra-anatomy/)
- 시험 뷰: `garment_flatlay`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: visible curved seams dividing the bra cup panels
- 후보 표현 B: two distinct cups joined at the center bridge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 35개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT071 — 브리지·프레임·밴드

- 원문 분류: 2-8 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: bridge, gore, frame, cradle, band, wing, underband
- 소유 대상: `bra` · 특징 풀: 컵 사이 연결 / 컵 아래 연속 프레임 여부 / 등 쪽 밴드
- 혼동 경계: frameless 변형에 연속 프레임을 강제하거나 strap을 band로 바꾸지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S10](https://clothhabit.com/bra-anatomy/)
- 시험 뷰: `front_and_back_flatlay`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a bridge joining the two cups above the underband
- 후보 표현 B: a continuous cradle frame surrounding the lower cup edges
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 425개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT072 — 와이어·보닝 채널

- 원문 분류: 2-8 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: underwire, wire casing, boning, busk
- 소유 대상: `bra_or_corset` · 특징 풀: 컵 아래 곡선 casing / 세로 보닝 채널 / 버스크의 짝 훅
- 혼동 경계: 채널 외관과 실제 금속·내부 지지 성능은 다른 증거다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S10](https://clothhabit.com/bra-anatomy/), [S11](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)
- 시험 뷰: `garment_flatlay`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a curved underwire casing beneath each bra cup
- 후보 표현 B: vertical boning channels running down the structured bodice
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT073 — 브라 스트랩의 연결

- 원문 분류: 2-8 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: strap, ring, slider, strap adjuster, hook-and-eye closure
- 소유 대상: `bra_strap` · 특징 풀: 컵·등 밴드에 붙는 끈 끝 / 링과 슬라이더 / 등 여밈
- 혼동 경계: 링은 떠 있는 장식이 아니며 끈 조절 상태로 실제 지지력을 판단하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S10](https://clothhabit.com/bra-anatomy/)
- 시험 뷰: `back_hardware_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a bra strap passing through a ring and slider
- 후보 표현 B: hook-and-eye rows aligned across the back band opening
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 56개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT074 — 핏과 여유분

- 원문 분류: 3-1 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: fitted, slim fit, regular fit, relaxed fit, oversized, boxy, bodycon
- 소유 대상: `garment_silhouette` · 특징 풀: 몸과 천 사이 여유 / 어깨·몸판·팔의 폭 / 윤곽을 따르는 정도
- 혼동 경계: 옷의 핏을 사람의 체형 변경이나 특정 치수의 증거로 번역하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S18](https://www.levi.com/US/en_US/features/men-jeans-guide), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: an oversized shirt with broad loose panels
- 후보 표현 B: a close-fitting dress following the torso without changing its shape
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 76개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT075 — 의복 허리선

- 원문 분류: 3-1 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: empire waist, drop waist, natural waist, princess line
- 소유 대상: `dress_construction` · 특징 풀: 가슴 아래·자연 허리·엉덩이 쪽의 연결 위치 / 허리 가로 봉제 유무
- 혼동 경계: empire는 체형·임신을 의미하지 않는다. princess seam과 princess line은 분리한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S41](https://www.sewing.org/files/guidelines/11_310_princess_seams.pdf), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `front_torso`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a dress with the skirt joined immediately below the bust
- 후보 표현 B: a dropped waist seam placed below the natural waist
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 11개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT076 — 미니·미디·맥시 기장

- 원문 분류: 3-1 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: mini, midi, maxi, knee-length, tea-length, floor-length
- 소유 대상: `garment_hem` · 특징 풀: 밑단과 무릎·종아리·발목·지면의 관계
- 혼동 경계: 브랜드별 길이 명명의 중첩을 허용하고 신장·사진 크기로 고정 cm를 추정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a midi hem ending between knee and ankle
- 후보 표현 B: a floor-length skirt reaching the ground
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 28개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT077 — 드레이프와 구조감

- 원문 분류: 3-1 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: draped, structured, bias-cut, asymmetric
- 소유 대상: `fabric_shape` · 특징 풀: 자유 접힘 / 자립하는 천 경계 / 앞뒤/좌우 비대칭
- 혼동 경계: structured 외관만으로 심지·보닝·재질을 확정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `front_torso`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a draped panel hanging in loose folds
- 후보 표현 B: a structured jacket front retaining a crisp edge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 36개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT078 — 섬유와 표면 분리

- 원문 분류: 3-2 · 우선순위: P0 · 제안 슬롯: `surface_material`
- 관련 용어: cotton, silk, wool, linen, polyester, nylon, rayon, viscose, acrylic
- 소유 대상: `fabric_material` · 특징 풀: 사용자가 지정한 섬유 메타데이터 / 별도로 지정한 조직·광택·두께
- 혼동 경계: 일반 사진으로 혼방비·실크/합성·울/아크릴의 진위를 판정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S38](https://cottonworks.com/learning-hub/denim/denim-basics/)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a silk-fiber satin specified by material metadata
- 후보 표현 B: a matte linen-look fabric with visible slub texture
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 78개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT079 — 시어와 투명도

- 원문 분류: 3-2 · 우선순위: P0 · 제안 슬롯: `surface_material`
- 관련 용어: sheer, transparent, semitransparent, opaque
- 소유 대상: `fabric_visibility` · 특징 풀: 아래층이 읽히는 정도 / 조명·겹수·배경의 조건
- 혼동 경계: chiffon·organza·mesh라는 이름이 모든 광조건에서 동일 투명도를 보장하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S24](https://www.roots.gov.sg/Collection-landing/listing/1148958)
- 시험 뷰: `layered_fabric_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a sheer outer panel revealing a separate lining beneath
- 후보 표현 B: an opaque fabric panel concealing the layer behind it
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT080 — 가죽·스웨이드·비닐 외관

- 원문 분류: 3-2 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: leather, faux leather, suede, nubuck, patent leather, PVC, latex
- 소유 대상: `surface_finish` · 특징 풀: 매끈한 입자 표면 / 짧은 기모 / 강한 반사면
- 혼동 경계: 광택으로 천연/인조·PVC/라텍스 화학 성분을 확정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `surface_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a suede-like surface with short diffuse nap
- 후보 표현 B: a patent-finish surface reflecting sharp highlights
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 52개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT081 — 퍼·깃털

- 원문 분류: 3-2 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: fur, faux fur, shearling, feather, marabou
- 소유 대상: `surface_or_trim` · 특징 풀: 연속 털 섬유 / 구분되는 깃대와 깃가지 / 부착된 테두리
- 혼동 경계: 천연 종·원산지·털 성분은 외관 게이트의 대상이 아니다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S17](https://www.villagehatshop.com/pages/hat-glossary)
- 시험 뷰: `surface_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a furry trim made of dense projecting fibers
- 후보 표현 B: individual feathers attached along the garment edge
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 6개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT082 — 신축·기능성 성분

- 원문 분류: 3-2 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: spandex, elastane, Lycra, neoprene, microfiber, technical fabric
- 소유 대상: `material_metadata` · 특징 풀: 요청된 재료명 / 눈에 보이는 두께·겉감·봉제 별도
- 혼동 경계: 타이트한 핏으로 신축율·압박·방수·흡한 성능을 판정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S38](https://cottonworks.com/learning-hub/denim/denim-basics/), [S33](https://usa.tommy.com/en/tommy-adaptive/mens-adaptive/tops/regular-fit-brushed-cotton-shirt/MW46777-YBR.html)
- 시험 뷰: `garment_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a close-fitting panel with its stretch material separately specified
- 후보 표현 B: a thick smooth neoprene-like garment surface
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT083 — 평직·바스켓·옥스퍼드 조직

- 원문 분류: 3-3 · 우선순위: P0 · 제안 슬롯: `surface_material`
- 관련 용어: plain weave, basket weave, Oxford, poplin, broadcloth
- 소유 대상: `fabric_weave` · 특징 풀: 실의 상하 교차 / 묶음 교차 / 소형 반복 단위
- 혼동 경계: 셔츠와 신발 Oxford를 조직명과 구분한다. 매끈함만으로 정확한 교차를 PASS 처리하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a macro view of alternating plain-weave yarn crossings
- 후보 표현 B: paired warp yarns creating an Oxford-style basket texture
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT084 — 트윌·헤링본·셰브론

- 원문 분류: 3-3 · 우선순위: P0 · 제안 슬롯: `surface_material`
- 관련 용어: twill, herringbone, chevron, gabardine
- 소유 대상: `fabric_weave` · 특징 풀: 사선 능선 / 방향 반전 지점 / V 꼭짓점의 연속 또는 어긋남
- 혼동 경계: 프린트 지그재그와 실제 조직의 사선을 독립한다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: fine diagonal twill ridges across the fabric
- 후보 표현 B: opposing herringbone diagonals meeting with a small offset
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 10개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT085 — 새틴·새틴 외관

- 원문 분류: 3-3 · 우선순위: P0 · 제안 슬롯: `surface_material`
- 관련 용어: satin, sateen
- 소유 대상: `fabric_weave_or_look` · 특징 풀: 긴 뜨임의 표면과 매끄러운 반사 / warp/weft-faced 변형
- 혼동 경계: 실크=새틴, 광택=새틴 조직이라는 역추론을 금지한다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S02](https://cottonworks.com/encyclopedia-item/satin/)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a satin-like surface with broad smooth highlights
- 후보 표현 B: a close-up of long float yarns on the woven face
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 20개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT086 — 데님·샴브레이

- 원문 분류: 3-3 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: denim, chambray, selvedge denim
- 소유 대상: `fabric_weave` · 특징 풀: 사선 또는 평직 교차 / 염색 경·다른 위사의 색 / 선택한 셀비지 가장자리
- 혼동 경계: 파랑·워싱·캡처 시대가 조직을 대신하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S38](https://cottonworks.com/learning-hub/denim/denim-basics/), [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: denim twill with visible diagonal yarn lines
- 후보 표현 B: a chambray-like plain weave mixing colored and pale yarns
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 21개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT087 — 저지·리브·인터록

- 원문 분류: 3-3 · 우선순위: P0 · 제안 슬롯: `surface_material`
- 관련 용어: jersey, rib knit, interlock, 2x2 rib
- 소유 대상: `fabric_knit` · 특징 풀: 편물 루프 / 세로 골 / 앞뒤 면 차이
- 혼동 경계: 스포츠 품목 jersey와 조직을 분리한다. 신축은 움직임 자료가 필요하다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S03](https://cottonworks.com/encyclopedia-item/jacquard-knitting/), [S04](https://cottonworks.com/encyclopedia-item/2-x-2-rib/)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: vertical rib-knit ridges separated by recessed channels
- 후보 표현 B: a macro view of small knitted loops on the fabric face
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 9개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT088 — 자카드·도비

- 원문 분류: 3-3 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: jacquard, dobby, brocade, damask
- 소유 대상: `fabric_pattern_structure` · 특징 풀: 조직에 들어간 패턴 / 빛 방향에 따라 보이는 대비 / 편물/직물 문맥
- 혼동 경계: 작은/큰 무늬 크기만으로 기계나 제조법을 확정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S03](https://cottonworks.com/encyclopedia-item/jacquard-knitting/), [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a pattern formed by contrasting woven surface textures
- 후보 표현 B: a jacquard-knit panel with integrated colored motifs
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 9개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT089 — 벨벳·코듀로이

- 원문 분류: 3-3 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: velvet, velour, corduroy
- 소유 대상: `pile_fabric` · 특징 풀: 짧고 촘촘한 기모 / 코듀로이의 평행 융기 골 / 광방향 변화
- 혼동 경계: 기모 외관과 섬유 성분·직편물 제조법을 구분한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `surface_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: parallel raised corduroy wales across the fabric
- 후보 표현 B: a dense velvet-like nap changing sheen with the folds
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 26개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT090 — 메시·튤·레이스

- 원문 분류: 3-3 · 우선순위: P0 · 제안 슬롯: `surface_material`
- 관련 용어: mesh, tulle, net, lace, Chantilly lace, guipure
- 소유 대상: `openwork_fabric` · 특징 풀: 열린 망눈 / 모티프 연결 / 바탕망의 유무
- 혼동 경계: 모든 lace를 투명 흰 꽃무늬로 고정하지 않는다. 세부 레이스 종류는 조직 확인 후 잠근다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S24](https://www.roots.gov.sg/Collection-landing/listing/1148958), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: lace motifs linked by bars without a continuous ground net
- 후보 표현 B: a fine tulle mesh with evenly spaced open cells
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 34개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT091 — 얇은 직물의 드레이프

- 원문 분류: 3-3 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: chiffon, organza, georgette, taffeta
- 소유 대상: `light_fabric` · 특징 풀: 유연/빳빳한 주름 / 반사 / 시어 조건 / 결의 세부
- 혼동 경계: 광택·시어·드레이프의 조합이 제조법 또는 섬유를 확정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `layered_fabric_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a crisp sheer panel holding angular folds
- 후보 표현 B: a soft translucent panel falling in small fluid folds
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 3개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT092 — 질감의 반복

- 원문 분류: 3-3 · 우선순위: P2 · 제안 슬롯: `surface_material`
- 관련 용어: piqué, seersucker, terry, waffle, fleece
- 소유 대상: `textured_fabric` · 특징 풀: 작은 반복 요철 / 오돌토돌한 띠 / 루프 파일 / 기모
- 혼동 경계: piqué 직편물·seersucker 변형은 명칭별 추가 직접 출처 확인 후 확정한다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S38](https://cottonworks.com/learning-hub/denim/denim-basics/), [S04](https://cottonworks.com/encyclopedia-item/2-x-2-rib/)
- 시험 뷰: `textile_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: alternating smooth and puckered fabric bands
- 후보 표현 B: small looped piles covering a terry-like surface
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT093 — 스트라이프와 조직 방향

- 원문 분류: 3-4 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: stripe, pinstripe, chalk stripe, railroad stripe
- 소유 대상: `fabric_pattern` · 특징 풀: 색 선 폭·간격 / 선의 진행 방향 / 패널에서 끊기는 지점
- 혼동 경계: 사선 프린트가 바이어스 재단 또는 트윌 조직을 뜻하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `front_torso_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: narrow evenly spaced stripes running down the panel
- 후보 표현 B: broad horizontal color bands across the garment
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT094 — 체크의 격자

- 원문 분류: 3-4 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: check, gingham, plaid, tartan, windowpane, glen plaid
- 소유 대상: `fabric_pattern` · 특징 풀: 두 방향 선의 교차 / 작은/큰 격자 / 중첩 패턴
- 혼동 경계: 특정 tartan의 집단·혈통·인증은 단순 색 격자로 판정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S01](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)
- 시험 뷰: `pattern_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a two-color grid of small repeated checks
- 후보 표현 B: fine lines forming large windowpane squares
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 4개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT095 — 하운즈투스·도트

- 원문 분류: 3-4 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: houndstooth, polka dot, argyle
- 소유 대상: `fabric_pattern` · 특징 풀: 톱니처럼 꺾인 체크 / 둥근 점 / 다이아몬드 반복과 선
- 혼동 경계: 해상도 부족으로 사라진 모티프를 선명한 정의의 증거로 삼지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `pattern_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: repeating broken checks with pointed extensions
- 후보 표현 B: evenly spaced round polka dots across the panel
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT096 — 플로럴·페이즐리·애니멀

- 원문 분류: 3-4 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: floral, paisley, leopard print, zebra print, snakeskin print
- 소유 대상: `fabric_pattern` · 특징 풀: 식물 모티프 / 휘어진 물방울 / 반점·줄·비늘 표현
- 혼동 경계: 애니멀 프린트는 실제 동물 가죽·털 재료와 다르다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary), [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `pattern_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: curved teardrop paisley motifs repeated on the cloth
- 후보 표현 B: a leopard-style spot pattern printed on smooth fabric
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 3개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT097 — 프린트·엠보스·퀼팅

- 원문 분류: 3-4 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: printed, embossed, quilted, embroidered
- 소유 대상: `fabric_surface` · 특징 풀: 평면 색면 / 눌린 요철 / 봉제선 사이 충전 부피 / 실 땀
- 혼동 경계: 시각 무늬와 제조법을 분리하고 충전재 재질은 가려진다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S30](https://data.fitzmuseum.cam.ac.uk/id/object/117565)
- 시험 뷰: `surface_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: stitched quilting lines dividing softly raised panels
- 후보 표현 B: an embossed surface with shallow relief rather than flat ink
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT098 — 워싱·디스트레스·염색

- 원문 분류: 3-4 · 우선순위: P1 · 제안 슬롯: `surface_material`
- 관련 용어: stonewash, acid wash, distressed, tie-dye, ombré, dip-dye
- 소유 대상: `fabric_finish` · 특징 풀: 국소 마모·해진 실 / 묶은 듯한 색 분포 / 연속 그라데이션
- 혼동 경계: 외관으로 특정 화학 처리·공정·새것/낡은 것의 실제 이력을 보장하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S38](https://cottonworks.com/learning-hub/denim/denim-basics/)
- 시험 뷰: `surface_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: localized worn patches exposing frayed denim yarns
- 후보 표현 B: a continuous color gradient fading along the fabric
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 4개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT099 — 모자 크라운·브림

- 원문 분류: 4-1 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: crown, brim, hatband, crease, fedora, trilby
- 소유 대상: `hat` · 특징 풀: 머리를 감싸는 크라운 / 둘레 챙의 폭·방향 / 움푹 들어간 주름
- 혼동 경계: fedora/trilby의 지역 명칭 중첩을 허용하고 고정 인치 경계를 보편화하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S16](https://www.villagehatshop.com/blogs/the-hat-files/anatomy-of-a-hat), [S17](https://www.villagehatshop.com/pages/hat-glossary)
- 시험 뷰: `hat_three_quarter`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a creased crown surrounded by a narrow turned-down brim
- 후보 표현 B: a ribbon band encircling the base of the hat crown
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 42개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT100 — 크라운 형태

- 원문 분류: 4-1 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: boater, bowler, pork pie, pillbox, top hat, cloche
- 소유 대상: `hat` · 특징 풀: 평평/둥근/움푹 들어간 상부 / 높이 / 챙 유무
- 혼동 경계: 착용자의 성별·시대·계급은 형상 외의 요청 문맥이다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S16](https://www.villagehatshop.com/blogs/the-hat-files/anatomy-of-a-hat), [S17](https://www.villagehatshop.com/pages/hat-glossary)
- 시험 뷰: `hat_three_quarter`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a flat-topped crown above a horizontal brim
- 후보 표현 B: a small brimless pillbox with straight sides
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 6개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT101 — 캡 패널과 바이저

- 원문 분류: 4-1 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: baseball cap, flat cap, newsboy cap, visor, beret
- 소유 대상: `headwear` · 특징 풀: 앞쪽만 돌출하는 바이저 / 봉제 패널 / 머리 위 덮개 유무
- 혼동 경계: 360도 brim과 앞쪽 visor를 구분하고 패널 수는 선택 변형으로 둔다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S17](https://www.villagehatshop.com/pages/hat-glossary)
- 시험 뷰: `hat_three_quarter`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a paneled cap with a short front visor
- 후보 표현 B: a sun visor with an open top above the headband
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT102 — 헤어 장식의 부착

- 원문 분류: 4-1 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: headband, hairpin, barrette, fascinator, tiara, hair comb
- 소유 대상: `hair_accessory` · 특징 풀: 머리띠·핀·빗의 지지 부위 / 머리 위 장식 / 머리카락 접촉
- 혼동 경계: 머리 위에 떠 있는 장식이나 머리카락 자체와 장식의 혼합을 실패로 둔다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S17](https://www.villagehatshop.com/pages/hat-glossary), [S22](https://www.vam.ac.uk/articles/kimono)
- 시험 뷰: `head_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a fascinator mounted on a small headband
- 후보 표현 B: a barrette clasping a visible section of hair
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 10개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT103 — 베일·윔플·코이프

- 원문 분류: 4-1, 5-5 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: veil, wimple, coif, snood
- 소유 대상: `head_or_neck_covering` · 특징 풀: 머리에서 드리운 천 / 턱/목을 감싸는 천 / 머리카락 주머니 또는 두건
- 혼동 경계: veil과 bail을 분리한다. snood의 머리/목 용례는 문맥을 지정한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S17](https://www.villagehatshop.com/pages/hat-glossary)
- 시험 뷰: `head_and_neck`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a veil draped from the head over the shoulders
- 후보 표현 B: a wimple wrapping beneath the chin and around the neck
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT104 — 스카프·숄·스톨

- 원문 분류: 4-2 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: scarf, shawl, stole, neck tie, bandana
- 소유 대상: `cloth_accessory` · 특징 풀: 목 또는 어깨에 놓인 천 / 묶인 위치 / 양끝 드레이프
- 혼동 경계: stole은 종교복의 좁은 띠와 패션 숄을 별도 sense로 둔다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S17](https://www.villagehatshop.com/pages/hat-glossary), [S29](https://www.vam.ac.uk/articles/the-syon-cope)
- 시험 뷰: `front_upper`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a shawl spread across both shoulders
- 후보 표현 B: a narrow scarf tied around the neck with two hanging ends
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 18개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT105 — 벨트·새시·하네스

- 원문 분류: 4-2 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: belt, sash, cummerbund, harness
- 소유 대상: `waist_or_torso_accessory` · 특징 풀: 허리 둘레 띠 / 묶은 매듭 / 상체를 가로지르는 스트랩과 결합부
- 혼동 경계: 장식 허리띠와 구조적 하네스의 경로를 혼합하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S34](https://www.burberryplc.com/company/history/170-years-of-burberry), [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)
- 시험 뷰: `front_and_back_torso`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a fabric sash wrapped and tied around the waist
- 후보 표현 B: a torso harness with connected shoulder and chest straps
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 47개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT106 — 장갑·미튼

- 원문 분류: 4-2 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: glove, mitten, fingerless glove, opera glove
- 소유 대상: `handwear` · 특징 풀: 손가락별 구획 또는 합친 구획 / 손목 위 연장 / 손가락 노출
- 혼동 경계: 착용 포즈 때문에 손가락이 합쳐 보이는 경우 구획은 별도 확인한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `hands_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: fingerless gloves exposing the fingertips
- 후보 표현 B: mittens with a single shared finger compartment
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT107 — 양말·스타킹·타이츠

- 원문 분류: 4-2 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: sock, stocking, tights, pantyhose, leg warmer
- 소유 대상: `legwear` · 특징 풀: 발을 감싸는지 / 허리까지 연속인지 / 다리 부분만 감싸는지
- 혼동 경계: 가려진 허리 연결은 추측하지 않는다. 피부색과 투명도는 별도 변수다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `garment_flatlay`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: separate stockings ending at the upper thighs
- 후보 표현 B: leg warmers covering the lower legs without enclosing the feet
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 6개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT108 — 귀걸이의 연결

- 원문 분류: 4-3 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: stud, hoop, huggie, drop earring, dangle earring, ear cuff
- 소유 대상: `ear_jewelry` · 특징 풀: 귓불 또는 귓바퀴와 접촉 / 고리·돌출 장식·매달린 연결
- 혼동 경계: 귀에 붙은 귀걸이와 공중 장식·헤어 핀을 구분한다. 실제 피어싱을 외관만으로 확정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S14](https://johnatencio.com/pages/glossary), [S45](https://www.firemountaingems.pro/learn/reference/essential-resources/encyclobeadia/)
- 시험 뷰: `ear_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a hoop earring contacting the lower earlobe
- 후보 표현 B: a suspended drop linked beneath an ear stud
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT109 — 목걸이 길이·형상

- 원문 분류: 4-3 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: choker, collar necklace, pendant, lariat, sautoir, Y-necklace
- 소유 대상: `neck_jewelry` · 특징 풀: 목과 닿는 위치 / 가슴으로 떨어지는 길이 / 펜던트 또는 Y 분기
- 혼동 경계: 고정 cm·모든 라리엇의 동일 clasp·성적 용례를 자동으로 붙이지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S14](https://johnatencio.com/pages/glossary), [S46](https://products.riogrande.com/content/Instruction-Sheets/Guide-To-Jewelery-Chain-IS.pdf)
- 시험 뷰: `neck_and_chest_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a Y-shaped necklace with a single drop below the junction
- 후보 표현 B: a pendant suspended at the center of a neck chain
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 9개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT110 — 목걸이 레이어

- 원문 분류: 4-3 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: layered necklace, multi-strand necklace, torque, torc
- 소유 대상: `neck_jewelry` · 특징 풀: 분리된 체인 경로 또는 같은 끝점의 여러 줄 / 단단한 열린 고리
- 혼동 경계: 별개 목걸이와 한 다중 스트랜드 목걸이의 끝점 연결을 구분한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S14](https://johnatencio.com/pages/glossary), [S45](https://www.firemountaingems.pro/learn/reference/essential-resources/encyclobeadia/)
- 시험 뷰: `neck_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: two separate necklaces lying at different heights
- 후보 표현 B: a rigid open neck ring with distinct end terminals
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 4개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT111 — 반지 형상과 위치

- 원문 분류: 4-4 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: ring, band, signet ring, solitaire, halo, stacking ring
- 소유 대상: `finger_jewelry` · 특징 풀: 손가락을 둘러싸는 shank / 상부 head / 큰 중심석 또는 주변 석
- 혼동 경계: solitaire/halo는 배치이고 prong/bezel은 고정 방식이다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S12](https://4cs.gia.edu/en-us/blog/guide-to-ring-settings/)
- 시험 뷰: `ring_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a ring band encircling the finger beneath a raised head
- 후보 표현 B: a central stone surrounded by a halo of smaller stones
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT112 — 팔찌·뱅글·커프

- 원문 분류: 4-4 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: bracelet, bangle, cuff, tennis bracelet, charm bracelet
- 소유 대상: `wrist_jewelry` · 특징 풀: 유연한 링크 / 닫힌 단단한 고리 / 열린 단단한 고리 / 달린 참
- 혼동 경계: 소매 cuff와 분리하고 소유 손목·개방부를 명시한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S14](https://johnatencio.com/pages/glossary), [S45](https://www.firemountaingems.pro/learn/reference/essential-resources/encyclobeadia/)
- 시험 뷰: `wrist_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: an open rigid cuff wrapping around the wrist
- 후보 표현 B: small charms hanging from a linked bracelet
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT113 — 바디체인·브로치

- 원문 분류: 4-4 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: body chain, anklet, brooch, lapel pin, cameo brooch
- 소유 대상: `body_or_garment_jewelry` · 특징 풀: 목/허리/몸통 경로와 연결점 / 발목 고리 / 옷 표면에 고정된 장식
- 혼동 경계: 브로치와 펜던트는 착용 대상·부착점이 다르다. 체인으로 체형을 바꾸지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S14](https://johnatencio.com/pages/glossary), [S45](https://www.firemountaingems.pro/learn/reference/essential-resources/encyclobeadia/)
- 시험 뷰: `front_torso_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a brooch pinned to the jacket lapel
- 후보 표현 B: a body chain linking a neck loop to a waist chain
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT114 — 프롱·베젤·플러시

- 원문 분류: 4-5 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: prong setting, claw setting, bezel setting, flush setting
- 소유 대상: `gem_setting` · 특징 풀: 석 가장자리로 구부러진 금속 팔 / 둘레 rim / 밴드에 가깝게 묻힌 상면
- 혼동 경계: 희미한 반짝임만으로 고정 구조·안전성·보석 등급을 판정하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S12](https://4cs.gia.edu/en-us/blog/guide-to-ring-settings/)
- 시험 뷰: `setting_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: narrow prongs curling over the gemstone edge
- 후보 표현 B: a continuous bezel rim encircling the stone perimeter
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT115 — 채널·파베·텐션

- 원문 분류: 4-5 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: channel setting, pavé setting, tension setting
- 소유 대상: `gem_setting` · 특징 풀: 평행 금속 벽 사이 석의 줄 / 작은 석의 촘촘한 배열 / 서로 반대쪽 밴드 끝의 접촉
- 혼동 경계: 파베 외관과 실제 미세 비드·물리 압력에 의한 고정은 다른 증거다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S12](https://4cs.gia.edu/en-us/blog/guide-to-ring-settings/)
- 시험 뷰: `setting_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a row of small stones held between two parallel metal rails
- 후보 표현 B: closely packed small stones covering the visible ring surface
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT116 — 펜던트 베일의 연결

- 원문 분류: 4-5 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: bail, jump ring, pendant mount
- 소유 대상: `pendant_jewelry` · 특징 풀: 펜던트 윗부분의 연결 고리 / 체인/코드 통과 / 접촉하는 두 대상
- 혼동 경계: 머리에 쓰는 veil과 분리한다. jump ring이 bail 전체와 항상 동의어는 아니다
- 출처 범위: `direct_feature` · 조사 상태: `limited_retrieval_design_unqualified` · [S45](https://www.firemountaingems.pro/learn/reference/essential-resources/encyclobeadia/), [S46](https://products.riogrande.com/content/Instruction-Sheets/Guide-To-Jewelery-Chain-IS.pdf)
- 시험 뷰: `pendant_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a pendant bail with the necklace chain passing through it
- 후보 표현 B: a small connector loop joining the pendant to the cord
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT117 — 체인 링크 위상

- 원문 분류: 4-5 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: cable chain, curb chain, Figaro chain, rope chain, box chain, snake chain
- 소유 대상: `jewelry_chain` · 특징 풀: 링크의 윤곽 / 맞물리는 방향 / 크기 반복 / 원통처럼 보이는 표면
- 혼동 경계: 작은 해상도에서 이름별 미세 위상을 확정하지 않는다. 표면 질감만으로 링크 연결을 대신하지 않는다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S46](https://products.riogrande.com/content/Instruction-Sheets/Guide-To-Jewelery-Chain-IS.pdf)
- 시험 뷰: `chain_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: alternating long and short links in a Figaro-style chain
- 후보 표현 B: oval cable links visibly interlocking with adjacent links
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT118 — 장신구 클라스프

- 원문 분류: 4-5 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: lobster clasp, spring ring clasp, toggle clasp, box clasp
- 소유 대상: `jewelry_closure` · 특징 풀: 맞물리는 끝 고리 / 레버 또는 원형 개구 / 막대가 통과하는 고리
- 혼동 경계: 목 뒤에 가려진 clasp를 정면 이미지에서 PASS 처리하지 않는다
- 출처 범위: `family_context` · 조사 상태: `limited_retrieval_design_unqualified` · [S45](https://www.firemountaingems.pro/learn/reference/essential-resources/encyclobeadia/)
- 시험 뷰: `clasp_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a toggle bar passed through a circular clasp ring
- 후보 표현 B: a lobster clasp hooked onto the opposite end ring
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT119 — 보석 윤곽과 컷

- 원문 분류: 4-5 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: round, oval, pear, marquise, emerald cut, princess cut, cabochon
- 소유 대상: `gem` · 특징 풀: 외곽 윤곽 / 면의 계단/삼각 배치 / 매끈한 돔
- 혼동 경계: emerald는 보석 종·윤곽·면 배치 sense를 구분한다. 실제 캐럿·등급은 제외한다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S13](https://www.gia.edu/gia-news-research-value-factors-gem-cutting-styles-definitions)
- 시험 뷰: `gem_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a pear-shaped stone with one rounded and one pointed end
- 후보 표현 B: a smooth domed cabochon without visible facets
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 25개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT120 — 카메오·인탈리오

- 원문 분류: 4-5 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: cameo, intaglio, carved gem
- 소유 대상: `gem_relief` · 특징 풀: 바탕 위로 올라오는 조각 / 아래로 파인 조각 / 가장자리 그림자
- 혼동 경계: 평면 인쇄 초상이나 보석 감별을 대신하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S13](https://www.gia.edu/gia-news-research-value-factors-gem-cutting-styles-definitions)
- 시험 뷰: `gem_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a raised cameo relief standing above its background
- 후보 표현 B: an intaglio figure cut below the polished surface
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT121 — 보석·금속 재료

- 원문 분류: 4-5 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: diamond, ruby, sapphire, emerald, pearl, gold, silver, platinum, rhinestone
- 소유 대상: `jewelry_material` · 특징 풀: 사용자가 지정한 재료 메타데이터 / 별도의 색·윤곽·반사 표면
- 혼동 경계: 광택과 색으로 천연/합성·금속 순도·출처·등급을 증명하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S40](https://4cs.gia.edu/en-us/blog/ten-tips-buying-jewelry/), [S13](https://www.gia.edu/gia-news-research-value-factors-gem-cutting-styles-definitions)
- 시험 뷰: `gem_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a red faceted stone with its material specified separately
- 후보 표현 B: a silver-colored metal band with smooth highlights
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 20개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT122 — 옥스퍼드·더비·브로그

- 원문 분류: 4-6 · 우선순위: P0 · 제안 슬롯: `footwear`
- 관련 용어: Oxford, Derby, brogue, wingtip
- 소유 대상: `shoe` · 특징 풀: 아이렛 페이싱과 뱀프의 위아래 연결 / 천공 장식 / 윙팁 패널
- 혼동 경계: 브로그 천공은 장식 축이며 옥스퍼드/더비의 레이싱 축과 공존할 수 있다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S15](https://www.crockettandjones.com/blogs/the-article/the-derby-the-unsung-hero-of-footwear)
- 시험 뷰: `shoe_top_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: Derby eyelet facings stitched over the vamp
- 후보 표현 B: closed Oxford lacing with facings joined beneath the vamp
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT123 — 몽크·로퍼

- 원문 분류: 4-6 · 우선순위: P1 · 제안 슬롯: `footwear`
- 관련 용어: monk strap, loafer, penny loafer, tassel loafer
- 소유 대상: `shoe` · 특징 풀: 뱀프 위 스트랩·버클 / 끈 없는 입구 / 패니 띠 또는 술
- 혼동 경계: 로퍼·몽크의 모양과 가죽 종류·격식은 별도다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S15](https://www.crockettandjones.com/blogs/the-article/the-derby-the-unsung-hero-of-footwear), [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `shoe_three_quarter`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a monk shoe closed by a buckle strap across the vamp
- 후보 표현 B: a loafer with a narrow slot in its vamp strap
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT124 — 뮬·슬링백·슬라이드

- 원문 분류: 4-6 · 우선순위: P0 · 제안 슬롯: `footwear`
- 관련 용어: mule, slingback, slide, clog, pump
- 소유 대상: `shoe` · 특징 풀: 뒤꿈치 덮개 유무 / 뒤를 지나는 스트랩 / 상부와 발등 연결
- 혼동 경계: mule은 앞이 열려 있어야 한다는 규칙이 아니다. 제조자의 앞코 정의도 다른 브랜드 전체에 강제하지 않는다.
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `shoe_side`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a backless mule leaving the heel uncovered
- 후보 표현 B: a slingback strap passing behind the heel
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 3개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT125 — 샌들 스트랩

- 원문 분류: 4-6 · 우선순위: P0 · 제안 슬롯: `footwear`
- 관련 용어: sandal, Mary Jane, T-strap, ankle strap, flip-flop
- 소유 대상: `shoe_strap` · 특징 풀: 발등 횡단 / 세로 T 경로 / 발목 고리 / 발가락 사이 분기
- 혼동 경계: T-strap·Mary Jane·ankle strap을 서로 배타적 품목으로 강제하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `shoe_top_and_side`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a T-shaped strap joining the toe area to an instep strap
- 후보 표현 B: an ankle strap connected to the shoe sides
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT126 — 부츠의 기장·개구

- 원문 분류: 4-6 · 우선순위: P1 · 제안 슬롯: `footwear`
- 관련 용어: ankle boot, Chelsea boot, chukka, knee-high boot, over-the-knee boot
- 소유 대상: `boot` · 특징 풀: 발목/무릎 대비 샤프트 높이 / 옆 탄성 거싯 / 레이싱 또는 지퍼
- 혼동 경계: 부츠 품목으로 승마·군인·보호 성능을 자동 확정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S15](https://www.crockettandjones.com/blogs/the-article/the-derby-the-unsung-hero-of-footwear), [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `shoe_side_full`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a Chelsea boot with elastic side panels
- 후보 표현 B: a boot shaft ending just below the knee
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT127 — 스니커·에스파드리유

- 원문 분류: 4-6 · 우선순위: P1 · 제안 슬롯: `footwear`
- 관련 용어: sneaker, trainer, espadrille, moccasin
- 소유 대상: `shoe` · 특징 풀: 상부와 솔 연결 / 로프처럼 엮인 솔 테두리 / 외부 봉제 형태
- 혼동 경계: 미끄럼 성능·운동 종목·손바느질 공정을 외관에서 보장하지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `shoe_side`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a shoe with woven rope covering the sole edge
- 후보 표현 B: a low sneaker upper attached to a continuous rubber-like sole
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT128 — 뱀프·쿼터·텅·솔

- 원문 분류: 4-7 · 우선순위: P0 · 제안 슬롯: `footwear`
- 관련 용어: vamp, quarter, tongue, outsole, insole, welt, last, shank
- 소유 대상: `shoe` · 특징 풀: 앞 발등 상부 / 뒤·측면 패널 / 끈 아래 텅 / 접지 바닥
- 혼동 경계: last와 내부 shank는 일반 외관에서 확정할 수 없다. 반지 shank와 구분한다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `shoe_top_and_side`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a tongue panel lying beneath the shoelaces
- 후보 표현 B: a quarter panel wrapping around the back of the heel
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 40개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT129 — 토박스 윤곽

- 원문 분류: 4-7 · 우선순위: P1 · 제안 슬롯: `footwear`
- 관련 용어: round toe, square toe, pointed toe, almond toe, peep toe
- 소유 대상: `shoe_toe` · 특징 풀: 정면 외곽의 곡선·각·점 / 발가락 쪽 작은 개구
- 혼동 경계: 촬영 원근·발 자세 때문에 실제 폭·발 모양을 확정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `shoe_top`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a square toe with a broad straight front edge
- 후보 표현 B: a small peep-toe opening at the front of the shoe
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT130 — 굽·플랫폼·웨지

- 원문 분류: 4-7 · 우선순위: P0 · 제안 슬롯: `footwear`
- 관련 용어: stiletto, block heel, kitten heel, wedge, platform, flatform
- 소유 대상: `shoe_sole` · 특징 풀: 뒤 굽의 폭 / 앞밑창 두께 / 뒤부터 앞까지 연결된 웨지 / 기울기
- 혼동 경계: platform과 wedge는 독립 축으로 공존한다. 절대 cm는 스케일 없이 판정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `shoe_side`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a thick forefoot platform combined with a separate block heel
- 후보 표현 B: a continuous wedge sole rising toward the heel
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 39개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT131 — 가방 형상·휴대 방식

- 원문 분류: 4-8 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: tote, satchel, hobo, crossbody, shoulder bag, top-handle bag
- 소유 대상: `bag` · 특징 풀: 몸체의 강성·곡선 / 핸들 위치 / 긴 스트랩의 몸 가로지름
- 혼동 경계: crossbody는 휴대 관계로 여러 몸체 형태와 공존하며 브랜드 분류는 중첩된다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S19](https://www.coach.com/stories/guides/how-to-choose-a-bag-for-work), [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `full_torso_and_bag`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a bag strap crossing from one shoulder to the opposite hip
- 후보 표현 B: a structured bag body supported by two top handles
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 9개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT132 — 가방 개구·하드웨어

- 원문 분류: 4-8 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: bucket bag, clutch, drawstring bag, frame bag, turnlock
- 소유 대상: `bag` · 특징 풀: 입구와 프레임 / 끈 조임 / 플랩과 잠금 부품 / 지지 방식
- 혼동 경계: 닫힌 외관으로 내부 수납칸·잠금 성능을 추정하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S19](https://www.coach.com/stories/guides/how-to-choose-a-bag-for-work), [S39](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)
- 시험 뷰: `bag_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a bucket-shaped bag gathered by a drawstring opening
- 후보 표현 B: a bag flap closed by a visible turnlock fitting
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT133 — 백팩·벨트백

- 원문 분류: 4-8 · 우선순위: P1 · 제안 슬롯: `wearable_accessory`
- 관련 용어: backpack, rucksack, belt bag, fanny pack, bum bag
- 소유 대상: `bag_support` · 특징 풀: 등에 놓인 몸체와 두 어깨 끈 / 허리/가슴을 두르는 고정 끈
- 혼동 경계: 이름만으로 착용 위치를 고정하지 않는다. 벨트백을 어깨에 멘 변형은 관계를 따로 적는다
- 출처 범위: `family_context` · 조사 상태: `limited_retrieval_design_unqualified` · [S19](https://www.coach.com/stories/guides/how-to-choose-a-bag-for-work)
- 시험 뷰: `back_and_side`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a backpack supported by two attached shoulder straps
- 후보 표현 B: a belt bag secured by a strap around the waist
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 2개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT134 — 안경·시계의 부위

- 원문 분류: 4-8 · 우선순위: P2 · 제안 슬롯: `wearable_accessory`
- 관련 용어: eyeglasses, sunglasses, frame, bridge, temple, watch, bezel, dial, crown
- 소유 대상: `accessory` · 특징 풀: 안경 브리지와 다리 접촉 / 시계 문자판·베젤·밴드
- 혼동 경계: UV 보호·도수·방수·진품·기계식 성능은 사진에서 확정하지 않는다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S12](https://4cs.gia.edu/en-us/blog/guide-to-ring-settings/), [S45](https://www.firemountaingems.pro/learn/reference/essential-resources/encyclobeadia/)
- 시험 뷰: `accessory_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: glasses resting on the nose with temples extending over the ears
- 후보 표현 B: a watch dial surrounded by a bezel and joined to a wrist band
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 332개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT135 — 저고리의 독립 부위

- 원문 분류: 5-1 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: jeogori, 길, 깃, 동정, 고름, 끝동
- 소유 대상: `jeogori` · 특징 풀: 몸판과 소매 / 깃에 얹힌 동정 / 앞을 여미는 고름 / 선택한 끝동
- 혼동 경계: 모든 저고리가 짧은 여성 현대형·흰 동정·특정 배색이라는 고정을 피한다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S20](https://encykorea.aks.ac.kr/Article/E0049084)
- 시험 뷰: `front_upper_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a jeogori collar edged with a separate dongjeong strip
- 후보 표현 B: goreum ties attached to the overlapping jacket fronts
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 10개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT136 — 치마·바지·두루마기

- 원문 분류: 5-1 · 우선순위: P1 · 제안 슬롯: `costume_style`
- 관련 용어: chima, baji, durumagi, hanbok
- 소유 대상: `hanbok_garment` · 특징 풀: 치마의 상부와 풍성한 아래판 / 분리된 바지 다리 / 위에 겹쳐지는 긴 겉옷
- 혼동 경계: hanbok이라는 넓은 이름에 특정 성별·민족·날짜·모든 액세서리를 묶지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S20](https://encykorea.aks.ac.kr/Article/E0049084), [S21](https://encykorea.aks.ac.kr/Article/E0012731)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a long chima joined to its upper waist band
- 후보 표현 B: a durumagi outer robe layered over separate inner garments
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 35개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT137 — 노리개의 부착·구성

- 원문 분류: 5-1 · 우선순위: P0 · 제안 슬롯: `wearable_accessory`
- 관련 용어: norigae, 노리개, 띠돈, 끈목, 매듭, 주체, 술
- 소유 대상: `hanbok_accessory` · 특징 풀: 고름 또는 치마허리의 상부 고리 / 끈·매듭·패물·아래 술
- 혼동 경계: 가슴 중앙 펜던트·허공 장식·목걸이로 옮기지 않는다. 패물 재료는 메타데이터다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S21](https://encykorea.aks.ac.kr/Article/E0012731)
- 시험 뷰: `front_waist_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a norigae hanging from the goreum with knot and tassel below
- 후보 표현 B: a waist-mounted ornament suspended from a connecting cord
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 49개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT138 — 한복 머리·주머니 장신구

- 원문 분류: 5-1 · 우선순위: P2 · 제안 슬롯: `wearable_accessory`
- 관련 용어: gat, jokduri, hwagwan, binyeo, daenggi, bokjumeoni
- 소유 대상: `hanbok_accessory` · 특징 풀: 머리에 놓이거나 머리카락에 연결되는 대상 / 허리에 매단 주머니
- 혼동 경계: 각 전통품목의 시대별 형태와 착용 맥락은 추가 표본 확인 후 잠근다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S20](https://encykorea.aks.ac.kr/Article/E0049084), [S21](https://encykorea.aks.ac.kr/Article/E0012731)
- 시험 뷰: `accessory_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a hair ribbon attached to the end of the braid
- 후보 표현 B: a fabric pouch suspended from a waist cord
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 8개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT139 — 기모노 여밈·오비

- 원문 분류: 5-2 · 우선순위: P0 · 제안 슬롯: `costume_style`
- 관련 용어: kimono, obi, yukata, haori
- 소유 대상: `japanese_garment` · 특징 풀: 착용자 왼쪽이 오른쪽을 덮는 앞판 / 허리 오비 / 직선 연결
- 혼동 경계: 관찰자 좌우·거울 반전과 구분한다. yukata/haori의 고유 차이는 별도 검증한다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S22](https://www.vam.ac.uk/articles/kimono)
- 시험 뷰: `front_and_back_full`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a kimono wrapped wearer-left over wearer-right and secured by an obi
- 후보 표현 B: an obi sash surrounding the kimono at the waist
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 7개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT140 — 치파오·청삼의 변형

- 원문 분류: 5-2 · 우선순위: P1 · 제안 슬롯: `costume_style`
- 관련 용어: qipao, cheongsam, Chinese frog, Mandarin collar
- 소유 대상: `dress` · 특징 풀: 선택한 스탠드 칼라 / 사선 여밈과 짝 프로그 / 옆 개구
- 혼동 경계: 몸에 붙는 롱드레스 하나로 모든 시대·지역의 청삼을 정의하지 않는다
- 출처 범위: `family_context` · 조사 상태: `limited_retrieval_design_unqualified` · [S23](https://www.roots.gov.sg/ich-landing/ich/cheongsam-tailoring)
- 시험 뷰: `front_full_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a cheongsam with an angled front opening and knotted frogs
- 후보 표현 B: a dress with a short upright collar and a visible side slit
- 기존 데이터 비교 포인터: exact profile 1개 / candidate lexical 4개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT141 — 케바야 표본의 연결

- 원문 분류: 5-2 · 우선순위: P1 · 제안 슬롯: `costume_style`
- 관련 용어: kebaya, kerosang, kebaya sarong, sarong
- 소유 대상: `kebaya_ensemble` · 특징 풀: 앞이 열린 블라우스 / 서로 이어지는 브로치 / 허리에 감싼 아래 천
- 혼동 경계: 세 kerosang은 특정 Straits 표본 변형이다. 모든 케바야의 공통 필수 조건으로 삼지 않는다
- 출처 범위: `product_example` · 조사 상태: `variant_example_only_design_unqualified` · [S24](https://www.roots.gov.sg/Collection-landing/listing/1148958)
- 시험 뷰: `front_full_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: an open-front kebaya joined by three linked kerosang brooches
- 후보 표현 B: a kebaya blouse layered above a wrapped sarong
- 기존 데이터 비교 포인터: exact profile 1개 / candidate lexical 6개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT142 — 사리의 드레이프 선택

- 원문 분류: 5-2 · 우선순위: P1 · 제안 슬롯: `costume_style`
- 관련 용어: sari, saree, pallu
- 소유 대상: `draped_cloth` · 특징 풀: 몸 둘레에 감기는 천 경로 / 선택한 어깨 드레이프 / 허리 주름
- 혼동 경계: 모든 사리에 한 드레이프·노출·장신구를 강제하지 않는다. 지역 변형 선택 후 구조를 확정한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S25](https://designmuseum.org/exhibitions/beazley-designs-of-the-year/fashion/the-sari-series)
- 시험 뷰: `front_and_back_full`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a sari cloth wrapped around the lower body with a selected shoulder drape
- 후보 표현 B: a visible pallu continuing from the wrapped cloth over one shoulder
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT143 — 아시아 전통복의 세트 분기

- 원문 분류: 5-2 · 우선순위: P2 · 제안 슬롯: `costume_style`
- 관련 용어: ao dai, ao yem, salwar kameez, kurta, lehenga, dupatta, hanfu, deel, chut thai
- 소유 대상: `regional_ensemble` · 특징 풀: 상의·하의·겉층·띠를 개별 소유자로 분리 / 선택한 시대·지역 변형
- 혼동 경계: 용어군은 동의어가 아니다. 개별 박물관/현지 기관 근거와 필수 부품은 추가 조사 후 편입한다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S07](https://fashionhistory.fitnyc.edu/dictionary/)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a long split tunic worn over separate trousers
- 후보 표현 B: a three-part ensemble with a separately draped scarf
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 8개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT144 — 로브와 머리 덮개 분리

- 원문 분류: 5-3 · 우선순위: P2 · 제안 슬롯: `costume_style`
- 관련 용어: abaya, kaftan, thobe, djellaba, burnous
- 소유 대상: `regional_robe` · 특징 풀: 앞트임·소매·후드·길이의 선택 변수 / 별도 머리 덮개
- 혼동 경계: 검정·특정 신앙·국적·성별을 필수 조합으로 삼지 않는다. 개별 지역 정의는 보강 필요하다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S07](https://fashionhistory.fitnyc.edu/dictionary/)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a long robe with a distinct front opening and separate head covering
- 후보 표현 B: a hooded outer robe with wide sleeves
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 4개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT145 — 머리 덮개의 범위

- 원문 분류: 5-3 · 우선순위: P2 · 제안 슬롯: `wearable_accessory`
- 관련 용어: hijab, niqab, chador, keffiyeh, turban
- 소유 대상: `head_covering` · 특징 풀: 머리·목·얼굴을 덮는 범위 / 보이는 개구 / 감긴 천 경로
- 혼동 경계: 의복 이름을 착용자의 종교·국적 확정으로 연결하지 않는다. 지역·활용 변형의 출처가 필요하다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S17](https://www.villagehatshop.com/pages/hat-glossary)
- 시험 뷰: `head_and_neck`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a headscarf covering the hair and neck while leaving the face open
- 후보 표현 B: cloth wrapped in overlapping layers around the head
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT146 — 아프리카 복식·직물 경계

- 원문 분류: 5-3 · 우선순위: P2 · 제안 슬롯: `costume_style`
- 관련 용어: kente, dashiki, boubou, agbada
- 소유 대상: `regional_textile_or_garment` · 특징 풀: 천·상의·로브·세트의 층위 분리 / 요청된 직조/자수/패널
- 혼동 경계: 켄테는 다른 의복명과 동의어가 아니다. UNESCO 본문 차단으로 세부 문화·조직 정의는 보류한다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S36](https://ich.unesco.org/en/RL/craftsmanship-of-traditional-woven-textile-kente-02130)
- 시험 뷰: `full_front_and_macro`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a selected robe with separately specified textile panels
- 후보 표현 B: a tunic with a requested embroidered neckline border
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT147 — 유럽·아메리카 복식 분기

- 원문 분류: 5-3 · 우선순위: P2 · 제안 슬롯: `costume_style`
- 관련 용어: dirndl, lederhosen, kilt, poncho, huipil, rebozo, charro suit
- 소유 대상: `regional_ensemble` · 특징 풀: 개별 품목과 세트 구성 / 앞치마·셔츠·스커트 또는 하의 관계
- 혼동 경계: 한 장식·색·민속무늬를 지역 전체의 유일한 형상으로 일반화하지 않는다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S07](https://fashionhistory.fitnyc.edu/dictionary/), [S09](https://seamsfriendly.com/pages/fashion-glossary)
- 시험 뷰: `full_front`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a skirt ensemble with a separate waist-tied apron
- 후보 표현 B: a shoulder-draped cloth accessory worn over a distinct blouse
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 11개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT148 — 고대 드레이프 복식

- 원문 분류: 5-4 · 우선순위: P1 · 제안 슬롯: `costume_style`
- 관련 용어: peplos, chiton, himation, toga, stola
- 소유 대상: `ancient_draped_garment` · 특징 풀: 선택한 상부 오버폴드 / 어깨 고정 / 몸을 감싸는 패널과 띠
- 혼동 경계: 이번 직접 확인은 peplos 중심이다. toga 등 모든 품목을 같은 어깨 천으로 합치지 않는다
- 출처 범위: `direct_feature` · 조사 상태: `source_feature_checked_design_unqualified` · [S26](https://fashionhistory.fitnyc.edu/peplos/)
- 시험 뷰: `front_and_back_full`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a peplos overfold hanging below paired shoulder fastenings
- 후보 표현 B: a wrapped rectangular garment gathered beneath a waist belt
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT149 — 역사복식의 지지·층

- 원문 분류: 5-4 · 우선순위: P1 · 제안 슬롯: `costume_style`
- 관련 용어: stays, farthingale, crinoline, bustle, petticoat
- 소유 대상: `historical_support_or_layer` · 특징 풀: 몸판 또는 스커트 아래 지지 위치 / 전체 둘레 볼륨과 뒤쪽 볼륨의 차이
- 혼동 경계: 겉 실루엣이 특정 내부 재료·구조의 존재를 보장하지 않는다. 시대 변형을 지정한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S11](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)
- 시험 뷰: `side_full_and_flatlay`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a skirt silhouette with volume concentrated at the rear
- 후보 표현 B: a separate underskirt layer visible beneath the outer hem
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 5개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT150 — 역사 재킷·드레스

- 원문 분류: 5-4 · 우선순위: P2 · 제안 슬롯: `costume_style`
- 관련 용어: doublet, jerkin, robe à la française, robe à l'anglaise, redingote, pelisse
- 소유 대상: `historical_garment` · 특징 풀: 시대 지정 몸판·소매·앞트임·뒤 주름 / 구체적 표본 참조
- 혼동 경계: 당대 원본·재현·판타지 변형은 별도로 기록한다. 개별 명칭의 구조는 직접 출처 확인 필요하다
- 출처 범위: `source_expand_required` · 조사 상태: `additional_primary_definition_required` · [S07](https://fashionhistory.fitnyc.edu/dictionary/), [S11](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)
- 시험 뷰: `front_and_back_full`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a selected historical coat with explicitly described front and back panels
- 후보 표현 B: a gown with a specified rear pleat arrangement
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 4개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT151 — 코프·달마티카 표본

- 원문 분류: 5-5 · 우선순위: P1 · 제안 슬롯: `costume_style`
- 관련 용어: cope, dalmatic, chasuble, alb, stole, cassock
- 소유 대상: `liturgical_garment` · 특징 풀: 망토형 외층 / 독립 소매가 있는 표본 / 앞뒤 장식 패널과 별도 띠
- 혼동 경계: 이번 표본은 cope/dalmatic 중심이다. 모든 종교·직위·시대의 예복을 동일화하지 않는다
- 출처 범위: `product_example` · 조사 상태: `variant_example_only_design_unqualified` · [S29](https://www.vam.ac.uk/articles/the-syon-cope), [S30](https://data.fitzmuseum.cam.ac.uk/id/object/117565)
- 시험 뷰: `front_and_back_full`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a ceremonial cope draped over the shoulders
- 후보 표현 B: a dalmatic with decorated front, back and sleeve panels
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT152 — 메일·판금·라멜라

- 원문 분류: 5-5 · 우선순위: P0 · 제안 슬롯: `costume_style`
- 관련 용어: mail, chainmail, plate armour, lamellar, brigandine
- 소유 대상: `armour` · 특징 풀: 맞물린 고리 망 / 단단한 판과 연결부 / 소판의 반복
- 혼동 경계: 메일과 판금은 공존할 수 있다. 라멜라/브리간딘 연결과 내부판 정의는 별도 보강한다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S28](https://royalarmouries.org/objects-and-stories/stories/the-hundred-years-war-1337-1453)
- 시험 뷰: `armour_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: interlocking metal rings forming a flexible mail mesh
- 후보 표현 B: rigid armor plates overlapping at articulated joints
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 24개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT153 — 갑옷의 부위 소유자

- 원문 분류: 5-5 · 우선순위: P1 · 제안 슬롯: `garment_detail`
- 관련 용어: cuirass, breastplate, pauldron, vambrace, gauntlet, greave, gorget
- 소유 대상: `armour_component` · 특징 풀: 가슴·어깨·아래팔·손·정강이·목의 개별 방어판 / 관절 연결
- 혼동 경계: 목 gorget와 역사 윔플 용례를 분리하고 착용 부위가 바뀌면 다른 후보다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S28](https://royalarmouries.org/objects-and-stories/stories/the-hundred-years-war-1337-1453), [S17](https://www.villagehatshop.com/pages/hat-glossary)
- 시험 뷰: `full_and_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a pauldron attached over the shoulder joint
- 후보 표현 B: a greave covering the front of the lower leg
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 1개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT154 — 넣어 입기의 부위 관계

- 원문 분류: 6 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: half tuck, full tuck, French tuck, 반만 넣어 입기
- 소유 대상: `top_hem_and_waistband` · 특징 풀: 어느 앞/옆 부분이 허리밴드 아래에 들어갔는지 / 나머지 밑단의 바깥 경로
- 혼동 경계: half와 French의 상품/사용 명칭 중첩을 허용하고 요청이 잠근 좌우·앞뒤를 바꾸지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S42](https://archive.lib.msu.edu/DMC/extension_publications/NCR443/e443-1980.pdf)
- 시험 뷰: `front_waist_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: only the front center of the shirt tucked beneath the waistband
- 후보 표현 B: one front panel tucked in while the other hangs outside
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

## CT155 — 의복·장신구 레이어 순서

- 원문 분류: 6 · 우선순위: P0 · 제안 슬롯: `garment_detail`
- 관련 용어: layering, over, under, attached to, worn with
- 소유 대상: `multi_garment_scene` · 특징 풀: 안쪽·바깥쪽 개별 물건 / 부착과 단순 접촉의 차이 / 가려진 경계
- 혼동 경계: 상의 속 구조를 보기 위해 요청하지 않은 탈의·노출·촬영 변경을 자동 추가하지 않는다
- 출처 범위: `family_context` · 조사 상태: `family_context_checked_design_unqualified` · [S05](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [S10](https://clothhabit.com/bra-anatomy/)
- 시험 뷰: `front_torso_detail`. 원래 요청 구도를 변경할 권한은 포함하지 않는다.
- 후보 표현 A: a separate camisole worn beneath an open shirt
- 후보 표현 B: a pendant hanging over the outer blouse layer
- 기존 데이터 비교 포인터: exact profile 0개 / candidate lexical 0개. 재사용 확정 전 의미·부위·owner 대조 필요.

