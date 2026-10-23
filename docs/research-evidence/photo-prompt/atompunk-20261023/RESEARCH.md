# 아톰펑크 시각 의미·후보 데이터 보강 리서치

조사일 2026-10-23, Asia/Seoul. 참조: [아톰펑크 용어 조사](https://chatgpt.com/c/6ada2ca9-1618-83ee-a5f8-f03f49b24312). **연구와 반영 계획을 작성한 상태이며 운영 데이터에는 등록하지 않았다.**

이번 보강의 핵심은 원자력 아이콘을 더 붙이는 것이 아니라, 장면을 구별하는 **형태·소유·연결·규모·매체·작동 주장**을 분리하는 것이다. 미국 도로변 소비문화, 소비에트 우주개발, 탐사 장비, 밝은 생활 자동화, 민방위와 공포를 선택 가능한 방향으로 남겨야 한다. 모두를 구기 다이너·차폐 계기함·핵폐허의 한 조합으로 고정하면 표현 범위가 오히려 좁아진다.

## 범위와 산출물

원 대화의 용어표 13개 **191행**, 작품 참고 9개, 창작 조합 9개와 검색 묶음 6개를 확인했다. 슬래시로 묶인 원문 항목은 한 행으로 보존했다. `Mini Dress / Shift Dress`, `Atomic Battery / RTG`, `Showgirl / Burlesque`를 동의어로 인정한 것은 아니다. [원문 범위 대조](REFERENCE-COVERAGE.md)에 별도로 적었다.

| 산출물 | 내용 | 의미 |
|---|---|---|
| [키워드 지도](KEYWORD-ATLAS.md) | 191개 용어의 처리 경로 | 하나의 단어가 새 후보 하나 또는 하드 의무 하나라는 뜻이 아님 |
| [상세 카드](VISUAL-CARDS.md) / [JSON](semantic-cards.json) | 101개: still 64, proxy 20, versioned 4, context 12, audio/temporal 1 | 관찰할 성분·소유자·방향 관계·혼동 경계·주장 한계 |
| [후보 구조 초안](candidate-drafts.json) | 88개 | 운영 로더 형식이 아니며 native source proof·CID/RID·검색 영수증 없음 |
| [한영 장면 제안](REALIZATIONS.tsv) | 18개 | 88개 구조 초안을 조합한 예시; 수를 합산해 106개 신규 후보로 보고하지 않음 |
| [출처 장부](SOURCES.tsv) | 53개 항목 | 52개는 범위가 제한된 본문/초록/메타데이터/검색 발췌 근거, 1개는 접근 실패 |
| [기존 자료 대조](EXISTING-DECISIONS.tsv) / [원문·해시](existing-source-mapping.json) | 23개 기존 레코드 | 재사용·세분·비동치·오탐 검토 제안이며 채택 승인이 아님 |
| [평가 사례](EVALUATION-CASES.tsv) | 60사례, 한영 120질의 | 개발 24·경계 16·일반 대조 12·비가시 대조 8, 전부 NOT_RUN |
| [반영 계획](IMPLEMENTATION-PLAN.md) / [픽셀 비교 계획](PIXEL-PLAN.md) | 단계별 파일·완료 조건·회귀·롤백 | 실제 검색·이미지·설치 전에 필요한 작업을 구분 |

P0 60개·P1 41개는 조사 카드의 우선순위다. P0에는 자동 시각 후보를 만들지 않는 문맥 카드도 포함된다. 88개 초안은 영어 성분·방향 그래프와 한국어 장면을 갖지만 **선택한 전체 소스의 자연스러운 한영 문장과 완전한 효과·조건은 구현 전에 다시 저술·검토해야 한다.**

모드에서 `still`은 현재 형상을 관찰할 수 있다는 뜻이지 용어의 역사·작동·원인까지 증명한다는 뜻이 아니다. `proxy`는 재료·기능·정체성을 확정하지 않은 외형 제안, `versioned`는 지정 판본과 대조할 필요가 있는 항목이다. `context`와 `audio_temporal`은 긍정 정지사진 구조 초안을 만들지 않는다. 원본 이미지 검토가 없는 판본을 이미 고증 완료로 취급하지 않는다.

## 1. 장르를 한 가지 외형으로 고정하지 않기

초기 아톰펑크 기획은 1945~1965를 문화적 참조점으로 삼으면서 소비에트 스타일·구기·우주개발·정치적 불안도 함께 언급했다. 하나의 역사적 선언을 모든 작품의 엄격한 연대와 필수 성분으로 적용하지 않는다. 특히 그 글의 ‘pre-digital’ 표현을 당시에 디지털 계산기가 없었다는 역사적 사실로 정규화하면 안 된다. 실제 SAGE는 대형 진공관 계산·관제 시스템이었다. [초기 기획](https://www.wired.com/2008/12/here-comes-atom/), [SAGE](https://www.computerhistory.org/revolution/real-time-computing/6/122).

현행 `world` 후보 `cand_9263bb1075a65f8e944e2c61fa7f4bde`는 구기·원자/초기 우주시대 인프라·낙관과 위험을 결합한 **구체적인 선택지**다. 이 소스와 번들을 보존하고, 순수 탐사·소비에트 전시관·밝은 주방 같은 다른 선택지를 추가하는 편이 좋다. 기존 소스를 짧게 추려 모든 아톰펑크의 정의로 바꾸지 않는다. 공식 소개에서 탐사 도구를 아톰펑크라고 부르는 《The Invincible》도 범위를 비교하는 근거다. [공식 소개](https://11bitstudios.com/games/the-invincible/).

## 2. 실제 기술과 허구 장치를 구별하기

| 구분 | 데이터에 필요한 가시 요소 | 넘지 않을 주장 |
|---|---|---|
| 원자로 E01 | 밀폐 용기·서비스 플랜지·배관 종단·계기 랙 | 냉각탑을 원자로 자체로 취급하거나 외관으로 핵반응을 확인하지 않음 |
| RTG E02 | 방열핀 전원통·별도 탐사 장비·양끝이 보이는 케이블 | RTG는 붕괴열을 쓰는 전원; 제어봉·연쇄반응 원자로로 바꾸지 않음 |
| 계수기 E05 / 선량계 E06 | 본체↔케이블↔분리 프로브, 또는 가슴에 고정된 작은 배지 | 검출과 개인 누적 선량을 구분; 눈금·진단·안전을 외형으로 확정하지 않음 |
| 안개상자 E07 | 투명 벽·어두운 바닥·낮은 층의 응결 궤적·측면광 | 입자를 직접 찍은 네온 광선으로 표현하지 않음 |
| 체렌코프 실현 E08 | 수면 아래 국소 청자색 빛·같은 수조의 반사 | 모든 방사성 물질의 보편 발광 또는 진공 광속 초과가 아님 |
| Nucleon E03 | 전방 객실·후방 동력부·전시대의 축소모형 | 1958년 3/8 모형을 실주행 핵자동차로 보고하지 않음 |
| NERVA / Orion X02 | 시험 설비 제안과 추진 원리 문맥을 분리 | 핵열·핵펄스·현대 Orion 유인선은 다른 것; Orion 소장품 판본은 접근 실패로 보류 |

기술 구분의 근거: [NASA RTG](https://science.nasa.gov/planetary-science/programs/radioisotope-power-systems/power-radioisotope-thermoelectric-generators/), [IOP 안개상자](https://www.iop.org/explore-physics/physics-around-you/understanding-surroundings/cloud-chamber), [DOE 체렌코프광](https://www.energy.gov/ne/articles/cherenkov-radiation-explained), [Henry Ford 모형](https://www.thehenryford.org/collections/explore/artifact/278186). 장면에서 제안한 모든 외형이 이 자료의 특정 유물과 동일하다는 뜻은 아니다.

## 3. 장치의 내부 구조와 물리 관계를 구체화하기

진공관 M01은 유리 외피·내부 전극판·작은 필라멘트·소켓으로, 닉시관 M07은 **겹친 숫자 전극 중 하나의 주황빛 발광**으로 구별한다. 주황색이라는 공통점만으로 두 장치를 합치지 않는다. 닉시관 분해 관찰은 전극 구조를 확인할 수 있는 일차 사례다. [분해 기록](https://www.evilmadscientist.com/2007/nixie-tube-take-apart/).

CRT 외형 M05, 오실로스코프 파형 M06, 레이더 표시 M10, 대형 계산실 M03은 다른 수준의 항목이다. 두꺼운 캐비닛이 화면 기술의 단서일 수 있어도 계산 방식이나 SAGE 시스템 전체를 보증하지 않는다. 자기테이프 M09는 양쪽 릴과 중앙 헤드까지의 경로, 천공카드 M08은 실제 구멍과 인쇄의 차이가 핵심이다. 아날로그 계산은 연속량을 쓰는 방식의 문제여서 ‘오래된 컴퓨터’와 같지 않다. [Science Museum의 서로 다른 아날로그 계산 사례](https://blog.sciencemuseum.org.uk/back-to-the-future-of-computing/).

서비스 로봇 M11의 품질 기준은 ‘가정용 로봇’이라는 이름보다 **같은 팔의 집게→쟁반 가장자리→쟁반 위 컵의 지지**가 읽히는가에 있다. 안드로이드·여성형 인공체·사이보그는 인간형 외피, 생물과 기계의 접점, 성별 표현을 구별한다. 인격·성별 정체성·성적 관계·의식은 시각 형상으로 확정하지 않는다.

## 4. 건축·장식은 서로 다른 구조로 저술하기

구기 B01은 지붕 돌출·지지선·유리벽·자동차 시선의 간판이 결합하는 분기다. LA Conservancy가 설명한 극적 지붕·유리벽·밝은 간판은 좋은 근거지만, 모든 구기 건물에 같은 색과 장식이 있는 것은 아니다. [Johnie's](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/).

- 나비 지붕 B02: 양끝이 높고 중앙이 낮다. 중앙이 높은 박공과 반대다.
- 절판 지붕 B03: 평면 판의 반복된 마루·골. 단일 V자와 같지 않다.
- 지오데식 형상 B04: 반구 표면의 삼각 골격과 공통 접점. 기밀 돔과 구별한다.
- 모노레일 B07: 하나의 가이드빔과 차체의 관계. 걸침형·현수형을 분기한다.
- 소비에트 영감 B09: 공공 광장·구조 베이·우주 도상의 구체적인 조합을 제안하되 지역·시대가 다른 실제 건축 전체를 하나로 일반화하지 않는다. [Zimmerli의 생활·우주 도상 자료](https://zimmerli.rutgers.edu/node/332).

장식도 원자 타원 궤도 F01 / 평면 스타버스트 F02 / 전구 달린 입체 막대 조명 F03을 분리한다. **실제 스푸트니크 S01의 네 안테나는 샹들리에의 다방향 전구와 다른 구조다.** 강낭콩형 F04의 오목 홈과 부메랑형 F09의 꺾인 두 팔도 서로 대체하지 않는다. 원자 도상과 생물형 곡선이 함께 쓰인 디자인 맥락은 [Nuclear Museum 자료](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/)로 확인했다. 돔의 삼각 구조는 [Fuller Institute](https://www.bfi.org/about-fuller/geodesic-domes/)로 보강했고 홍보성 강도 수치는 채택하지 않았다.

## 5. 생활·패션·매체의 소유 범위를 지키기

파스텔은 장면 전체 색보정과 물체의 도장색을 구별하고, 투톤은 **같은 가전의 상하 패널과 그 사이 몰딩**으로 묶는다. 크롬·PVC·유리섬유·Formica는 반사나 표면만으로 실제 조성을 확정하지 않는다. 특히 Formica 상표와 일반 적층판을 구별한다. 제조 공정의 근거가 없으면 `proxy`로 유지한다.

1947 이후 뉴 룩 W01은 잘록한 의복 허리와 풍성한 치마, 우주 시대 분기 W04는 직선 또는 각진 패널과 짧은 길이를 다룬다. ‘미니’는 길이, ‘시프트’는 구조다. 의복의 모양을 인물의 신체 비율 변경으로 구현하면 안 된다. 흰색·은색, 평평한 부츠·고글·헬멧과 재료 실험은 V&A의 구체적인 1960년대 사례가 뒷받침한다. [V&A](https://www.vam.ac.uk/articles/an-introduction-to-1960s-fashion).

성인 시각문화는 삭제하지 않았다. 핀업은 인쇄물이라는 매체와 등장 성인을 분리하고, 수영복·광택 의상·공연 세트를 구체적으로 제안했다. Miss Atomic Bomb V03은 **원피스 앞면의 솜 같은 버섯구름 장식**이며 실제 폭발이나 비키니가 아니다. UNLV 목록의 넓은 연대 범위와 도서관 전시 설명의 역사적 사진을 구분했다. [UNLV 소장 목록](https://special.library.unlv.edu/node/58463), [도서관의 전시 설명](https://thelibrarydistrict.org/blogs/post/miss-atomic-bomb-icon-of-the-atomic-age/).

불릿 브라 W03은 원뿔형 컵과 원형 기계 봉제의 의복 구조를 [Pitt Rivers 소장품 설명](https://web.prm.ox.ac.uk/bodyarts/index.php/permanent-body-arts/reshaping-and-piercing/150-reshaping-breasts.html)으로 보강했다. 실제 신체를 원뿔형으로 바꾸거나 니트 위 실루엣만으로 특정 속옷을 확정하지 않는다. BDSM의 동의 개념은 [NCSF 문헌](https://ncsfreedom.org/wp-content/uploads/2019/12/Consent-Counts-Statement-summary.pdf)의 범위로 기록하되 장식·포즈만으로 개별 관계를 판정하지 않는다.

음악·성적 해방·성적 대상화·인공 연인·BDSM·성적 강압·고어는 원문 범위를 보존한다. 다만 소리, 관계, 동의, 비평적 효과와 표현 목적은 현재 보이는 물체와 별도다. 캠프 역시 과장·인위성·연극성 등의 해석 틀이지 단순 노출·네온·낮은 품질의 동의어가 아니다. [Met 전시 틀](https://www.metmuseum.org/exhibitions/listings/2019/camp-notes-on-fashion/).

## 6. 역사적 피해와 SF 괴수를 혼동하지 않기

민방위 대피소 R03은 밀폐된 낮은 방·침상·밀폐 비축물·라디오의 현재 배치, 시험 마을 R06은 모형 주택·시험 인형·계측의 관계를 다룬다. 원본 사진과 작동·피해 자료를 확인하기 전 특정 실험 판본을 완전 고증했다고 부르지 않는다. [National Archives의 자료와 캡션](https://www.archives.gov/education/lessons/fallout-docs).

버섯구름 모양만으로 핵폭발을, 먼지로 방사성 낙진을, 창백한 피부로 피폭 피해를, 눈으로 핵겨울을 확정할 수 없다. Downwinders와 우라늄광 주변 주민의 피해는 실제 기록과 환경 문맥으로 다루고, 사람의 외형을 괴수화하는 기술로 대체하지 않는다. 핵겨울은 후대 기후 연구의 맥락을 보존한다. [NPS](https://www.nps.gov/mapr/learn/historyculture/downwinders.htm), [EPA](https://www.epa.gov/navajo-nation-uranium-cleanup/section-32-33-mines), [NASA 연구 초록](https://ntrs.nasa.gov/citations/19840033254).

가상 괴수 H02는 건물과의 크기 관계, 거대 곤충 H03은 세 몸마디·여섯 다리·한 쌍 더듬이를 명시한다. 원문에 곤충과 함께 예시된 거미는 분류상 별도이며 여덟 다리 분기로 다룬다. 《고지라》의 핵 공포 맥락은 작품 해석의 근거이지 현실 피폭이 즉각 거대화를 일으킨다는 근거가 아니다. [Janus의 작품 소개](https://www.janusfilms.com/films/1856).

## 기존 코퍼스와의 실제 차이

조사 시점 manifest에는 75개 모듈, 20,054개 레코드와 14,687개 binding이 있었다. 이 중 **정확한 아톰펑크 태그/번들 계열은 5개: visual option 4개와 bundle 1개**다. 5개는 ‘전체 관련 의미가 5개뿐’이라는 뜻이 아니다. [스냅샷](CORPUS-SNAPSHOT.json).

고정 positive field `content.en/ko/aliases`에서 191개 항목을 문자 경계로 진단했을 때 146개가 0건이었다. 이것은 정식 검색 결과도 의미상 부재의 증거도 아니다. 별칭·단어의 유무가 아니라 전체 원문과 선택된 관계를 검토해야 한다. 별도 느슨한 이웃 탐색에서는 `monochrome`의 `chrome`이 금속 몰딩 이웃으로 잡혔고, ‘mid-century’ 거리사진 양식이 건축의 대안처럼 보였다. 이들은 명시적으로 부적합 처리했다. [감사 방법과 결과](LEXICAL-AUDIT.json), [23개 판단](EXISTING-DECISIONS.tsv).

우선 재사용할 것은 펜슬 치마의 좁은 윤곽, 점프슈트의 몸통~다리 연속 구성처럼 실제 의미가 맞는 자료다. 신규 제안은 기존 것과 **어느 owner·endpoint·형태·매체·기능이 다른지**를 밝힌 뒤 만든다. 기존 바늘 계측함 하나를 모든 원자력 장면의 대체물로 쓰거나, 단순한 크롬 구체를 위성·몰딩·방열핀으로 재사용하지 않는다.

이번 검증은 [연구 구조 검사](VALIDATION.json)까지다. 실제 후보 등록·검색 평가·이미지 생성·픽셀 구현·설치·커밋·푸시·사용자 수용은 수행하지 않았다. 다음 작업의 구체적인 순서는 [반영 계획](IMPLEMENTATION-PLAN.md)에 적었다.
