# 참조 대화의 범위 대조

대화 ID `6ada2ca9-1618-83ee-a5f8-f03f49b24312`, 제목 ‘아톰펑크 용어 조사’. `read_thread`는 assistant 본문을 20,000자에서 잘랐고 `truncated`를 반환했다. 같은 대화의 로그인된 Chrome 렌더링에서 모든 표 행과 마지막 항목 `Robot Uprising`까지 읽어 나머지를 확인했다. 대화를 새로 생성하거나 메시지를 보내지 않았다.

## 용어표

| 원문 표 | 항목 수 | 이 패키지 ID |
|---|---:|---|
| 장르·인접 개념 | 14 | A001~014 |
| 에너지·과학 낙관 | 17 | A015~031 |
| 우주·교통·장비 | 14 | A032~045 |
| 컴퓨터·로봇·조작계 | 17 | A046~062 |
| 건축·도시 | 14 | A063~076 |
| 형태·색·재료 | 14 | A077~090 |
| 소비·생활·광고 | 13 | A091~103 |
| 패션·헤어 | 11 | A104~114 |
| 성인 시각문화·비평 | 14 | A115~128 |
| 음악·그래픽·매체 | 12 | A129~140 |
| 냉전·사회 통제 | 15 | A141~155 |
| 핵전쟁·민간 피해 | 17 | A156~172 |
| 괴수·실험·폭력 | 19 | A173~191 |
| 합계 | **191** | 13개 용어표 전체 |

원문 labels는 `research_context.py`에 보존하고 한국어/영어 이름을 따로 저장했다. 원문의 정의와 인용번호는 검증된 출처로 자동 계승하지 않았다. 참조 대화는 조사 항목의 출발점이고, 새 출처 장부의 접근 범위가 별도 근거다.

## 작품 9개

| 원문 작품 | 연구에서의 위치 | 이번 근거 범위 |
|---|---|---|
| The Invincible | 후대 아톰펑크·탐사·철학적 과학 모험 | S43 공식 소개, atompunk tools 표현; 플레이/모든 장비 픽셀 확인 아님 |
| Fallout 시리즈 | 복고 제품·광고와 핵전후 세계의 분기 | S47 공식 상품 설명의 제한된 연결; 원 대화의 팬 모드 소개를 시리즈 전체 근거로 사용하지 않음 |
| Atomic Heart | 허구의 1955 소비에트 영감 자동화 | S44 publisher 설명; JS-only 공식 사이트는 본문 근거로 계상하지 않음 |
| Forbidden Planet (1956) | 당시 복고 SF 원형·로봇·행성 기지·전자 음향 | S32 LOC essay 텍스트; 영화 전체 관람 아님 |
| The Jetsons | 밝은 가정 자동화의 인접 참고 | S46 Paley 에피소드 기록; 모든 소품·의상 고증 미실행 |
| Godzilla (1954) | 핵 공포·괴수와 도시 규모 | S42 licensor synopsis; 실제 피폭 인과의 근거 아님 |
| Dr. Strangelove (1964) | 지휘체계·핵전멸 블랙코미디 | S45 Sony synopsis; 원탁만으로 전략을 증명하지 않음 |
| Barbarella (1968) | 성인 SF·캠프·인공 세트의 인접 분기 | S31 영화제 설명; 의상·행위의 통합 복원 미실행 |
| The Atomic Cafe (1982) | 역사 아카이브의 편집·홍보와 피해의 대비 | S33 LOC essay; 특정 장면 전체 영상 확인 아님 |

작품별 고유 디자인·브랜드·캐릭터를 일반 후보의 필수 요소로 넣지 않는다. 작품·판본을 직접 재현할 후속 요청이 있으면 그 판본의 원본 프레임을 따로 확인한다.

## 창작 조합 9개

다음은 원 대화가 제안한 조합이다. 공식 하위 장르명이 아니며 이번 리서치의 Q01~18 역시 연구자가 새로 저술한 대안이다.

| 원문 조합 | 반영 경로 | 사진에서 확정하지 않을 부분 |
|---|---|---|
| 밝고 유쾌한 미래 생활 | Q01/Q02, L06/M11/S05 | 실제 자동화 성능·가족 관계·음악 |
| 풍요 속에 숨은 불안 | Q17, B08/R01/X08 | 동조·재교육·정치적 충성 |
| 기업이 소유한 미래 | R02/L08/X08 | 기업 소유·시민권·연애 관리의 제도적 사실 |
| 소비에트 우주 유토피아 | Q03, B09/M03/X01 | 실제 소련 사회·중앙컴퓨터의 행복 계산 |
| 에로틱하고 캠프한 우주 활극 | Q15/Q16, V01/V04/X05 | 욕망·성적 관계·동의·관객의 캠프 경험 |
| 의료·실험 호러 | H01/H06/X11 | 실험 동의·수명 연장·인격/기억 자산 |
| 핵 괴수·바디 호러 | Q18, H02/H03/H04/X11 | 실제 피폭·돌연변이 원인·군산복합체 인과 |
| 쇠락한 미래의 우울함 | Q18/R07 | 과거의 반복 방송·실제 핵전쟁·주민 사망 |
| 잔혹한 블랙코미디 | X06/X12, L08 | 실제 고어·치명적 사고·편집/음악의 웃음 효과 |

성인·폭력·정치·피해 관련 조합도 기록을 삭제하지 않았다. 다만 모든 조합을 긍정 still 후보로 자동 변환하지 않고, 필요한 매체와 비가시 주장 경계를 남겼다.

## 원문 검색 묶음 6개

| 묶음 | 원문 예 | 연결 카드 |
|---|---|---|
| 도시·건축 | Googie architecture, Atomic Age architecture, mid-century roadside architecture, space age pavilion, Soviet modernism, world's fair futurism | B01~10, X01 |
| 실내·소품 | atomic pattern, starburst clock, Sputnik chandelier, Formica diner, pastel appliances, mid-century dream kitchen | F01~09, L01/L06 |
| 기계·인터페이스 | vacuum tube computer, SAGE control room, analog control console, Nixie tube display, retro robot, atomic car concept | E03/E05, M01~12 |
| 우주 이미지 | finned rocket, wheel space station, moon dome, bubble helmet, raygun gothic, 1950s space illustration | S01~11, G02, X01 |
| 패션·성인 문화 | space age fashion, atomic age pin-up, cheesecake photography, beefcake photography, Miss Atomic Bomb, Barbarella costume, space age bachelor pad | W01~09, V01~05, L07, X05 |
| 불안·호러 | civil defense film, fallout shelter interior, nuclear test mannequins, atomic monster, 1950s science fiction horror, Cold War propaganda | R01~07, H01~06, X06~12 |

이 표현은 검색·비교용 문구다. 뜻을 확인하지 않은 신규 별칭을 일괄 등록하거나 장르/의무의 두 번째 authority로 사용하지 않는다.
