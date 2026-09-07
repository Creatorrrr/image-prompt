# 가난·빈곤 개념군 시각 의미·후보팩 강화 리서치

- 조사일: 2026-09-07
- 참조 대화: `가난 관련어 조사` (`6a9d9711-b7c4-83e8-9da1-f9be3540b5a3`)
- 대상: `photo-prompt-image-generator`의 시각 의미 계약, 후보팩 데이터, 라우팅·픽셀 평가 설계
- 결정 상태: `proposed`
- 변경 경계: 조사 산출물만 작성했다. 런타임 레지스트리·후보 확장·생성 인덱스·테스트는 수정하지 않았고 이미지 생성도 수행하지 않았다.

## 산출물

- `report-source.md`: 조사 결론, 저장소 공백, 개념별 설계 원칙, 혼동 경계, 구현·픽셀 검증 순서
- `candidate-data-proposal.json`: 10개 시각 계약, 60개 후보 원자, 7개 보류 번들, 출처 결합과 평가 계약
- `evidence.jsonl`: 공식·1차 출처 20건을 추상화 차원, 연결 후보·계약, 사진의 입증 한계와 함께 고정한 근거 원장
- `routing-regression-proposal.jsonl`: exact-positive 20건, broad-advisory 4건, hard-negative 10건으로 구성한 34개 제안 회귀

## 1. 결론

`가난`, `빈곤`, `궁핍`, `극빈`을 `낡은 옷 + 더러운 얼굴 + 빈 그릇 + 회갈색 톤`으로 묶는 데이터는 강화가 아니라 오염이다. 빈곤은 한 사람의 외모가 아니라 **자원·서비스·시간·선택·접근권이 제한되는 관계**이며, 여러 공식 지표도 소득 하나가 아닌 식량, 주거, 에너지, 교육, 위생, 디지털 연결, 사회 참여처럼 서로 다른 결핍을 구분한다.

후보팩은 다음 두 층으로 나누는 것이 적절하다.

1. **분류·해석 층**: 절대적 빈곤, 상대적 빈곤, 다차원 빈곤, 기아, 근로빈곤, 노숙, 빈곤의 대물림처럼 통계·기간·가구·지역 맥락이 필요한 용어를 advisory 또는 citation-only로 유지한다.
2. **사진 가능한 사건 층**: 한 프레임에서 확인 가능한 `제약 원인 → 동일 주체의 선택·대응 → 즉시 결과`만 정확 구문으로 hard profile 후보화한다.

이번 조사 결과는 다음 구현 재료를 제공한다.

- P0 시각 계약 9개, P1 시각 계약 1개
- 계약별 6개씩 총 60개 후보 원자
- 단일 사진 hard 승격을 보류한 7개 후보 번들
- broad/advisory, exact-positive, confusion-negative를 포함한 34개 라우팅 회귀안
- food-access, energy-affordability, working-income의 독립 3-arm 픽셀 검증안

핵심 사건 사슬은 다음과 같다.

```text
명시된 기본 필요 또는 참여 목표
→ 추적 가능한 자원·서비스·접근 제약
→ 동일 성인의 선택·분배·수선·대응 행동
→ 충족된 쪽과 미뤄지거나 차단된 쪽
→ 같은 프레임에 남는 즉시 결과
```

한 요소라도 빠지면 `partial_is_fail`이다. 빈 그릇, 낡은 옷, 추운 청색광, 야간노동, 반지하, 동전, 쇼윈도는 각각 다른 이유로 나타날 수 있으므로 단독 증거가 아니다.

## 2. 조사 범위와 증거 경계

### 포함

- 참조 대화의 한국어·영어 키워드와 시각 소재
- 2026-09-07 현재 저장소의 프로필·연구 확장 구조와 중복 여부
- 국제기구·정부·공식 통계의 빈곤, 식량, 주거, 에너지, 노동, 시간, 교통, 디지털 접근 정의
- 빈곤 이미지의 낙인·대상화·아동 재현 경계
- 현재 v6 구조에 맞는 정확 활성, 후보 원자, 혼동 경계, 회귀·픽셀 평가 설계

### 제외

- 특정 국가·민족·인종·성별·연령·장애·직업을 빈곤의 외형으로 지정하는 규칙
- 실제 사람의 건강, 영양상태, 소득, 채무, 주거 상태, 노숙 여부를 이미지에서 진단하는 규칙
- 읽을 수 있는 청구서 문구·은행잔액·가격 숫자만으로 통과하는 게이트
- 실존 구호기관, 공공기관, 브랜드, 로고, 실제 사례의 재현
- 런타임 소스 적용, 임베딩 생성, 이미지 생성, 픽셀 PASS 주장

### 증거 층

| 층 | 이번 결과 |
|---|---|
| 참조 대화 관찰 | 포괄어와 식량·돈·주거·에너지·노동·선택·도시·역사·재질·존엄의 핵심어군을 추출 |
| 외부 정의·측정 근거 | 국제기구·정부·공식 통계와 재현 윤리 자료를 교차 확인 |
| 현재 저장소 검사 | 333개 visual-obligation 프로필과 20개 연구 확장의 visual semantics 102개를 검사했으나 poverty 계열 프로필·후보는 0개 |
| 설계 | 10개 프로필, 60개 후보, 7개 보류 번들, 34개 회귀안 작성 |
| 구현·패키지 테스트 | 수행하지 않음 |
| 생성 전달·픽셀 | 수행하지 않음 |
| 사용자 판단 | 대기 |

## 3. 최신 정의에서 얻은 설계 원칙

### 3.1 금액 기준은 메타데이터이며 외형이 아니다

[World Bank의 2025년 갱신](https://www.worldbank.org/en/news/factsheet/2025/06/05/june-2025-update-to-global-poverty-lines)은 2021 PPP 기준 국제 극빈선을 1인당 하루 3달러로 바꾸었고, 개별 국가 판단에는 국가 빈곤선이 더 적절하다고 명시한다. 참조 대화가 사용한 2.15달러는 현재 헤드라인 기준이 아니다.

데이터 함의:

- 금액·소득선·`absolute poverty`는 분류 메타데이터다.
- 현금 몇 장, 동전, 빈 지갑은 소득 빈곤의 hard evidence가 아니다.
- 국가·시대·가구 규모가 없는 숫자를 런타임 시각 문법으로 만들지 않는다.

### 3.2 빈곤은 여러 결핍의 중첩이다

[UNDP 2025 Global MPI](https://hdr.undp.org/content/2025-global-multidimensional-poverty-index-mpi)는 건강, 교육, 생활수준 아래 영양, 아동 사망, 취학, 조리연료, 위생, 식수, 전기, 주거, 자산을 별도 지표로 둔다. [OHCHR의 빈곤 정의](https://docstore.ohchr.org/SelfServices/FilesHandler.ashx?enc=2H6doNlv%2FGZH6sbI%2FuOPmUKCWSAIK7WcG6zIYSUAA%2BCs18dBw4td%2FMYxllFpqI%2F%2Bf4ew4ABya%2F7q0HHXmFPU0w%3D%3D)도 자원뿐 아니라 역량, 선택, 안전, 권력의 지속적 박탈을 포함한다.

데이터 함의:

- `poverty` 하나가 식량·주거·에너지 프로필을 동시에 강제하면 안 된다.
- 사용자가 어떤 결핍을 뜻하는지 core에서 명확히 한 뒤 가장 좁은 계약을 선택한다.
- 다차원 빈곤은 한 장면의 hard profile이 아니라 여러 독립 결핍의 조합·보고 층이다.

### 3.3 식량 불안은 경험의 심각도 사슬이며, 한 장의 빈 접시가 아니다

[FAO FIES](https://www.fao.org/measuring-hunger/access-to-food/applying-the-fies/)는 자원 부족 때문에 음식 걱정, 영양가 있는 음식 접근 실패, 식단 다양성 감소, 끼니 거름, 섭취량 감소, 식량 소진, 배고프지만 먹지 못함, 하루 종일 먹지 못함을 구분한다. 이 항목들은 회고 기간을 가진 자기보고이므로 그대로 픽셀 판정이 되지는 않는다.

데이터 함의:

- 사진은 `식량 접근 제약`, `구매 축소`, `남은 양 분배`, `소진 흔적`까지만 표현한다.
- 걱정, 만성성, 영양 충분성, 하루 전체의 굶음은 한 프레임에서 주장하지 않는다.
- `빈 그릇`, `작은 식사`, `저렴한 음식`은 단독 게이트에서 제외한다.

### 3.4 기근·영양실조는 사진 콘셉트명이 아니라 복합 판정이다

[IPC](https://www.ipcinfo.org/famine-facts/)는 기근을 식량 박탈·생계 붕괴, 급성 영양실조, 사망이 함께 충족되는 지역 단위 분류로 다룬다. [WHO](https://www.who.int/health-topics/malnutrition)는 영양실조가 부족뿐 아니라 과잉과 불균형도 포함하며, 저영양 역시 측정과 건강 맥락이 필요하다고 설명한다.

데이터 함의:

- `기근`, `기아`, `아사`, `영양실조`는 broad hard activation 금지다.
- 마른 몸, 피로한 얼굴, 피부·입술·손톱 상태로 빈곤이나 영양상태를 추론하지 않는다.
- 명시적 허구 장면이라도 식량 접근 사건을 묘사할 뿐, IPC/의학 분류를 픽셀 PASS로 주장하지 않는다.

### 3.5 물질적 박탈은 “선택하지 않음”과 “감당할 수 없음”을 구분한다

[Eurostat의 현행 지표 설명](https://ec.europa.eu/eurostat/cache/metadata/en/sdg_01_10_esmsip2.htm)은 체납, 적절한 난방, 정기적인 단백질 식사, 낡은 가구·옷 교체, 맞는 신발, 인터넷, 여가·사회적 만남 등을 `감당할 수 없어` 누리지 못하는 항목으로 측정한다.

데이터 함의:

- 낡은 가구·옷 자체가 아니라 `필수 교체 필요 → 자원 제약 → 국소 수선 → 계속 사용` 관계가 필요하다.
- 미니멀리즘, 검소함, 지속가능성, 빈티지 패션, 수선 취미와 분리한다.
- 체납 고지서의 읽을 수 있는 문구를 요구하지 말고, 두 필수 지출과 실제 선택 결과를 한 장면에 둔다.

### 3.6 주거·에너지 빈곤은 건축 양식이 아니라 서비스·비용·거주 가능성 문제다

[OHCHR의 적정 주거 기준](https://www.ohchr.org/Documents/Publications/FS21_rev_1_Housing_en.pdf)은 점유 안정성, 서비스·인프라, 비용 적정성, 거주 가능성, 접근성, 위치, 문화적 적절성을 구분한다. [European Commission의 energy poverty 설명](https://energy.ec.europa.eu/topics/markets-and-consumers/energy-consumers-and-prosumers/energy-poverty_en)은 겨울 난방뿐 아니라 여름철 적정 실내온도 유지도 문제로 본다.

데이터 함의:

- 흙바닥·자연재료·낡은 벽을 문화와 무관한 빈곤 기호로 만들지 않는다.
- 주거 프로필은 결함의 물리적 원인, 생활공간에 미치는 결과, 현재의 완화 행동을 연결한다.
- 에너지 프로필은 고장·재난 정전·겨울 코지 연출과 구분하고, 서비스/비용 제약과 실제 적응을 함께 요구한다.

### 3.7 일한다는 사실과 근로빈곤은 다르다

[ILOSTAT](https://ilostat.ilo.org/data/snapshots/working-poverty-rate/)은 working poverty를 취업자 중 빈곤선 아래에서 사는 사람의 비율로 정의한다. 야간근무, 작업복, 거친 손, 긴 노동시간만으로는 가구 소득선을 알 수 없다.

데이터 함의:

- `night shift worker`나 배달가방을 근로빈곤의 동의어로 만들지 않는다.
- 명시적 `working poor` 장면은 유급 노동 결과, 보상 자원, 기본비용, 남는 부족을 한 관계로 구성한다.
- 특정 직업·계층·성별·이주 상태를 저임금의 기본값으로 두지 않는다.

### 3.8 시간·교통·디지털 빈곤은 각각 다른 접근 제약이다

[UN Women](https://knowledge.unwomen.org/sites/default/files/Headquarters/Attachments/Sections/Library/Publications/2019/World-survey-on-the-role-of-women-in-development-2019.pdf)은 time poverty를 과도한 유급·무급 돌봄·가사노동 때문에 휴식과 여가 시간이 부족한 상태로 설명한다. [UK Department for Transport](https://www.gov.uk/government/publications/transport-and-inequality)는 교통 불평등에서 비용, 지리적 접근성, 시간, 신뢰성을 구분한다. [ITU](https://www.itu.int/itu-d/sites/priorities/affordable-connectivity/)는 기기와 통신서비스가 소득 대비 감당 가능하고 재정적 곤란을 초래하지 않는 연결성을 목표로 둔다.

데이터 함의:

- 시간 빈곤은 지속시간이 핵심이므로 단일 사진 hard profile 승격을 보류한다.
- 교통 프로필은 단순 기다림이 아니라 비용·접근 장벽과 놓친 경로를 보여야 한다.
- 디지털 프로필은 깨진 휴대폰·오류 화면이 아니라 비용 또는 공유·시간 제한과 중단된 필수 과업을 연결해야 한다.

### 3.9 노숙·주거불안은 거리 생활 한 종류가 아니다

[OECD Toolkit to Combat Homelessness](https://www.oecd.org/en/publications/oecd-toolkit-to-combat-homelessness_0fec780e-en/full-report/measurement-definitions-data-and-drivers_ad1a5f41.html)은 국제적으로 통일된 정의가 없으며, 거리 생활 외에도 긴급·임시숙소, 기관 체류, 비정형 거처, 지인 집 임시 거주를 구분한다. 국내에서도 [국토교통부 주거취약계층 안내](https://www.molit.go.kr/USR/policyTarget/dtl.jsp?idx=982)는 쪽방·고시원·여인숙·비닐하우스·노숙인 시설·컨테이너·움막·PC방 등 여러 거처와 일정 거주기간을 함께 사용한다.

데이터 함의:

- `homeless person = 거리의 누더기 차림` 프로필을 금지한다.
- 반지하·고시원·쪽방은 한국 맥락의 장소 후보일 뿐 거주자 외모나 빈곤을 자동 증명하지 않는다.
- 임시 거주와 주거불안은 기간·점유 상태가 중요하므로 단일 사진 hard profile을 보류한다.

### 3.10 상대적 빈곤과 사회적 배제는 비교·참여 장벽이 필요하다

[Eurostat](https://ec.europa.eu/eurostat/cache/metadata/en/sdg_01_10_esmsip2.htm)은 상대적 소득 빈곤을 국가 중위소득 기반으로 측정하면서 물질·사회적 박탈과 저노동강도를 별도 차원으로 둔다. 한국 [국가통계연구원 지표](https://sri.kostat.go.kr/boardDownload.es?bid=246&list_no=442421&seq=4)도 균등화 처분가능소득 중위값의 50%를 상대빈곤 기준으로 삼는다. 따라서 상대빈곤·물질박탈·사회적 배제를 같은 시각 기호로 합치지 않는다.

데이터 함의:

- 쇼윈도 밖 인물은 멋진 대비 구도일 수 있지만 상대적 박탈의 충분조건이 아니다.
- 같은 활동·서비스에 대한 정상 접근, 구체적 비용/절차 장벽, 차단된 참여 결과가 함께 보여야 한다.
- 보호특성·외모·의복 때문에 배제된 것으로 자동 해석하지 않는다.

### 3.11 생리용품 빈곤·아동빈곤은 별도 보호 경계가 필요하다

[UNICEF menstrual hygiene guidance](https://www.unicef.org/wash/menstrual-hygiene)는 제품뿐 아니라 물·위생·사생활·시설·사회적 지지를 함께 다룬다. [UNICEF ethical reporting guidelines](https://www.unicef.org/media/reporting-guidelines)는 아동의 존엄, 사생활, 안전, 맥락, 비고정관념을 우선한다.

데이터 함의:

- period poverty는 제품 클로즈업이나 옷 얼룩으로 표현하지 않는다.
- 기본 후보는 명시적 성인 요청에서 제품·시설·사생활·물 접근의 제약을 다룬다.
- child poverty는 연령 라우팅이지 빈곤 시각 프로필이 아니다. 아동을 고통의 상징으로 자동 삽입하지 않는다.

### 3.12 존엄은 고통을 지우는 필터가 아니라 재현 방식이다

[Dóchas Code의 illustrative guide](https://dochas.ie/wp-content/uploads/2026/02/Illustrative_Guide_to_the_Dochas_Code_of_Conduct_on_Images_and_Messages.pdf)는 개인의 고통만 확대하지 말고 원인·제도·지역 공동체의 행동을 보여주며, 대상화와 과도한 취약성 크롭을 피하라고 안내한다. [Joseph Rowntree Foundation의 anti-stigma 프로젝트](https://www.jrf.org.uk/power-and-participation/visual-empathy-capturing-poverty-through-a-stigma-free-lens)는 당사자 관점, 같은 눈높이, 힘·연결·일상적 행위를 포함하는 원칙을 제시한다.

데이터 함의:

- `존엄`은 미소를 강제하는 분위기 후보가 아니다.
- 동일 인물의 문제 해결, 수선, 분배, 협력, 선택권을 보존하는 행동으로 구현한다.
- 인물 없이 사물·서비스·경계의 관계를 보여주는 대안 후보도 제공한다.

## 4. 참조 대화 키워드 처리 지도

| 의미군 | 대표 키워드 | 제안 처리 |
|---|---|---|
| 포괄 빈곤 | 가난, 빈곤, 궁핍, 빈궁, 곤궁, 극빈, destitution, indigence, penury | broad advisory; 독립 hard profile 금지 |
| 금전·채무 | 무일푼, 빈털터리, 빚, 채무, 체납, 연체, 미납, 압류, 파산 | 금융·법적 상태는 비시각; 기본 필요 trade-off 사건만 exact profile |
| 식량 접근 | 허기, 굶주림, 식량난, food insecurity, meal skipping, rationing | resource constraint가 명시된 구매·분배 사건만 exact profile |
| 기아·건강 | 기아, 아사, 기근, 영양실조, undernutrition, malnutrition, famine | 통계·의학 분류; hard route 금지, 신체 외형 금지 |
| 물질적 박탈 | 닳음, 기움, 중고, hand-me-down, wear and tear | 재질 후보만 advisory; 교체 불가+수선+계속 사용 exact profile |
| 생활비 제약 | 생활고, 생계난, bare minimum, subsistence, living hand to mouth | 두 필수 필요 사이의 실제 선택·미룸 사건으로 exact profile |
| 주거 | 주거빈곤, 반지하, 고시원, 쪽방, 판잣집, slum, tenement | 장소와 빈곤 분리; 거주 가능성 결함·완화 관계만 exact profile |
| 에너지 | 에너지빈곤, fuel poverty, 추위, 난방비, 단전 | 비용/서비스 제약+실내 대응 exact profile; 청색광·외투 단독 금지 |
| 근로 | 근로빈곤, working poor, 저임금, 일용직, 야간근무, 투잡 | 직업/시간대는 advisory; 유급노동+기본비용 부족 exact profile |
| 시간 | 시간빈곤, 과로, 돌봄, 휴식 부족 | duration 필요; sequence-only 후보, 단일사진 hard 보류 |
| 교통 | 교통빈곤, 교통비, 첫차, 막차 | 비용/접근 장벽+놓친 필수 이동 exact profile |
| 디지털 | 디지털빈곤, 깨진 스마트폰, 공유기기, 인터넷 | 비용/공유 제한+중단된 필수 과업 P1 exact profile |
| 의료·생리 | 의료 접근 빈곤, 병원비, period poverty | 민감한 explicit-only 후보; 진단·신체표지 금지 |
| 상대적 박탈 | 상대적 빈곤, 상대적 박탈, 쇼윈도, 유리장벽 | 정상 참여와 구체적 장벽이 같이 보일 때 exact profile |
| 사회적 배제 | 사회적 배제, 주변화, 소외, disenfranchisement | broad advisory; 경제적 참여 장벽만 제한적으로 후보화 |
| 시간적 구조 | 만성빈곤, 일시적 빈곤, 빈곤의 덫, 악순환, 대물림 | 단일사진 hard 금지; 다중시점 서사 연구 필요 |
| 지역·인구 | 도시빈곤, 농촌빈곤, 아동빈곤, 노인빈곤 | setting/age modifier일 뿐 빈곤 외형을 공급하지 않음 |
| 감정 | 불안, 수치, 체념, 절박, 무력, 외로움, 희망 | atmosphere advisory; 얼굴·자세로 빈곤 판정 금지 |
| 가치·대응 | 생존, 버팀, endurance, making do, 존엄 | agency-preserving action 후보; 빈곤 증거 자체는 아님 |
| 역사 기관 | poorhouse, workhouse, almshouse, breadline, soup kitchen, relief station | 정확한 시대·지역 연구가 있는 경우에만 context candidate |

## 5. 현재 저장소의 재사용 지점과 공백

2026-09-07 현재 authored registry에는 333개 프로필이 있고, 20개 `*_extension.json` 파일에 들어 있는 `visual_semantics` 합계는 102개다. `poverty`, `빈곤`, `가난`, `궁핍`, `food insecurity`, `energy poverty`, `working poor`, `time poverty`, `transport poverty`, `digital poverty`를 직접 소유하는 프로필·확장 후보는 없다.

기존 항목은 일부 관계 문법만 재사용할 수 있다.

| 기존 항목 | 재사용 가능한 것 | 재사용하면 안 되는 것 |
|---|---|---|
| `retail_browse_source_selection_relation` | 진열 원위치, 손-상품 접촉, 선택 결과 공백 | 예산 제약·식량 불안·빈곤 의미 |
| `transit_waiting_departure_relation` | 교통 경계, 차량 상태, 이동 방향 | 운임 부족·교통빈곤 의미 |
| 의상 수선·접촉 마모 후보 | 국소 마모, 물성에 맞는 수선, 계속 사용 흔적 | 계층·위생·빈곤·성격 추론 |
| `inaccessible_target_longing_relation` | 장벽-대상-행동 구도 | 상대적 박탈·사회적 배제 의미 |
| `repeated_acquisition_without_use_cycle` | 자원 흐름과 결과를 한 프레임에 묶는 문법 | 부족과 과잉 획득의 혼동 |
| `pleonexia_unfair_share_taking_event` | 분배선·몫·결과 관계 | 부족한 사람을 탐욕스럽다고 오독 |
| `resource_control_acquisition_event` | 접근권·자원·피영향자 관계 | 빈곤 당사자에게 권력욕을 부여 |

공백은 다음과 같다.

- 음식 부재가 아니라 자원 제약에 의한 구매 축소·분배를 소유하는 계약이 없다.
- 월세·식비·난방·교통처럼 두 기본 필요 사이의 실제 trade-off 계약이 없다.
- 에너지 서비스/비용 제약과 실내 대응을 연결하는 계약이 없다.
- 거주 중인 집의 결함 원인·결과·완화 행동을 묶는 계약이 없다.
- 유급 노동과 기본비용 부족을 분리해 보여주는 계약이 없다.
- 교통·디지털 접근의 비용 장벽을 일반 대기·기기 고장과 구분하는 계약이 없다.
- 마모를 빈곤 기호로 만들지 않으면서 교체 지연·수선·계속 사용을 묶는 계약이 없다.
- 동일 활동에 대한 정상 접근과 비용 장벽을 비교하는 상대적 박탈 계약이 없다.
- 낙인을 막는 composition/capture guard가 poverty 계열에 없다.

## 6. 제안 시각 의미 계약

구체 필드, exact 구문, candidate ID, source binding은 `candidate-data-proposal.json`에 있다.

| 우선순위 | 프로필 ID | 한 프레임의 필수 명제 | 대표 혼동 |
|---|---|---|---|
| P0 | `food_access_budget_choice_event` | 기본 식품, 유한한 지불자원, 되돌리는 행동, 줄어든 구매 결과 | 식단 선택, 쿠폰 사용, 일반 장보기 |
| P0 | `household_food_depletion_portioning_event` | 거의 소진된 동일 공급원, 실제 분배, 여러 몫, 분배 후 잔량 | 테이스팅 메뉴, meal prep, 다이어트 |
| P0 | `basic_needs_budget_tradeoff_deferral` | 두 기본 필요, 제한된 자원, 하나의 선택, 다른 하나의 즉시 미룸 | 가계부 취미, 투자, 비필수 쇼핑 |
| P0 | `household_energy_affordability_coping_relation` | 점유 주거, 비활성 서비스, 비용/공급 제약, 실내 대응, 방 전체 결과 | 고장, 재난 정전, 코지 겨울, 청색 톤 |
| P0 | `occupied_housing_habitability_mitigation_relation` | 점유 주거, 추적 가능한 결함, 생활 영향, 완화 행동, 남은 결함 | 폐허, 공사장, 러스틱 인테리어 |
| P0 | `working_income_essential_cost_gap_relation` | 유급 노동 결과, 보상, 기본비용, 남은 부족, 동일 성인의 대응 | 야간노동 초상, 바쁜 직장인, 검소함 |
| P0 | `transport_affordability_access_barrier_event` | 필수 이동, 비용/접근 장벽, 동일 성인의 실패 행동, 출발 결과 | 일반 대기, 막차 감성, 지갑 분실 |
| P0 | `material_replacement_deferral_repair_cycle` | 필수품의 국소 마모, 교체 제약, 수선, 계속 사용 | 빈티지 패션, 업사이클링, 취미 수선 |
| P0 | `relative_participation_affordability_barrier` | 같은 활동의 정상 접근, 구체 장벽, 차단된 참여, 즉시 결과 | 쇼윈도 감상, 외로움, 보호특성 차별 |
| P1 | `digital_connectivity_affordability_workaround_event` | 필수 디지털 과업, 비용/시간/공유 제한, 우회 행동, 중단 결과 | 기기 고장, 비밀번호 오류, 디지털 디톡스 |

### 공통 하드 규칙

1. broad term은 exact hard activation을 만들지 않는다.
2. exact-positive는 원인, 행동, 결과를 모두 포함해야 한다.
3. 프로필은 `definition_only`를 기본으로 하며 `poor person`, `poverty face`, `starving body`, `slum dweller` 같은 사람 라벨을 런타임 문구에서 금지한다.
4. 숫자·가독 텍스트는 보조 단서일 수 있으나 유일한 evidence field나 render gate가 될 수 없다.
5. 표정, 체형, 피부, 위생, 보호특성, 직업, 지역, 건축 양식, 색보정은 필수 구성요소가 될 수 없다.
6. 모든 인물 기본 후보는 명백한 성인으로 두고, 아동·노인·특정 인구집단은 요청이 명시한 경우에만 별도 경계를 거친다.
7. 사람을 포함하는 구도는 가능한 한 같은 눈높이, 행동 중인 주체, 맥락이 보이는 프레이밍을 사용한다.

## 7. P1·후보팩 전용 보류 번들

다음은 검색·구성 보조 가치는 있지만 단일 사진 hard profile로 승격하면 과장이 발생한다.

| 번들 ID | 후보 구성 | 승격 보류 이유 |
|---|---|---|
| `time_poverty_sequence_only` | 유급노동, 무급 돌봄·가사, 반복 시간표지, 사라진 휴식 구간 | 지속시간과 누적 부담이 핵심 |
| `period_material_facility_access_gap` | 명시적 성인, 제품, 물·위생·사생활 시설, 접근 장벽 | 민감정보·신체표지 위험; 제품 하나로 불충분 |
| `water_sanitation_access_gap` | 물 공급원, 왕복 경로, 저장, 공유 시설, 실제 사용 제약 | 안전성·30분 거리·지속성은 한 장으로 판정 불가 |
| `healthcare_cost_deferral_explicit_only` | 일반적 의료 접근 지점, 비용 trade-off, 연기된 비식별 절차 | 진단·의료 필요·경제상태 추론 위험 |
| `temporary_housing_insecurity_sequence` | 임시 거처, 개인물품 이동, 반복 이동, 점유 불안정 맥락 | 임시성·평소 거처 부재는 기간 자료 필요 |
| `community_food_access_distribution` | 공급, 배분 규칙, 성인 참여자 역할, 수령·보충 흐름 | 기관 이용만으로 빈곤 판정 불가; 수동적 수혜자 프레임 위험 |
| `historical_relief_institution_context` | breadline, poorhouse, workhouse, almshouse, relief station | 시대·국가·제도별 의미가 다르고 일반 빈곤 프리셋이 아님 |

## 8. 후보팩 데이터 설계

각 hard profile은 다음 6개 슬롯을 가진다.

- `subject`: 빈곤 외모가 아니라 사건에 참여하는 명백한 성인 또는 인물 없는 자원 시스템
- `action`: 선택·분배·수선·완화·우회처럼 결과를 만드는 동작
- `location`: 제약 원인과 결과가 한 프레임에 드러나는 생활·서비스 경계
- `prop`: 비식별·무상표·문자 비의존 자원/서비스 단서
- `composition`: 원인–행동–결과를 한 방향축이나 삼각관계로 묶는 구도
- `aftermath_trace`: 선택 뒤 남은 부족, 미뤄진 필요, 소진, 차단, 계속 사용 흔적

총 60개 항목은 다음 품질 규칙을 따른다.

- 모든 ID는 `pov_` 접두사를 사용한다.
- `poverty`, `poor`, `destitute`, `starving`, `slum`은 candidate `en`, alias, embedding text에 사람 속성으로 넣지 않는다.
- candidate는 반드시 하나 이상의 proposed profile을 `for_any`로 참조한다.
- source ID는 근거가 직접 지지하는 차원만 연결한다.
- 지역·시대·인구 속성은 candidate에 고정하지 않는다.
- 표정과 색감 후보는 0개다. 감정·톤은 core의 별도 open dimension으로 남긴다.

## 9. 라우팅·회귀 설계

`routing-regression-proposal.jsonl`은 34개 케이스를 담는다.

### 통과해야 하는 층

- exact-positive가 오직 자기 프로필만 hard activate
- broad `가난`, `빈곤`, `기아`, `생활고`, `precarity`, `working poor`는 정의 없는 상태에서 hard profile 0개
- component-rich paraphrase는 BM25F/embedding optional candidate로만 노출
- exact-negative와 negation은 hard activation 0개
- 욕망·일반 장보기·교통 대기·수선 문화·코지 겨울·폐허 탐험이 poverty 프로필로 bleed하지 않음

### 구현 시 필요한 테스트

1. extension schema와 candidate ID/slot 참조 무결성
2. registry exact-term 전역 유일성
3. visual-profile index stale-hash 실패와 batch-size 1 재생성
4. 정확 positive 2개 이상, broad advisory 1개 이상, 인접 hard negative 3개 이상/프로필
5. BM25F 문서가 `claim limits`, `source titles`, `ethical policy`를 positive prototype으로 사용하지 않음
6. optional selection 전에는 render gate가 생기지 않고, 선택 후에는 전체 게이트가 합쳐짐
7. readable text를 제거해도 핵심 관계가 유지되는 prompt-level mutation
8. 표정·체형·색감만 남긴 mutation이 fail

## 10. 독립 픽셀 검증 제안

이미지 생성은 이번 조사 범위 밖이다. 구현 후 첫 검증은 서로 독립적인 3개 arm으로 제한한다.

| Arm | 요청 의미 | 가장 중요한 게이트 | 필수 hard negative |
|---|---|---|---|
| A | 기본 식품을 살 예산이 부족해 한 품목을 되돌리고 줄어든 장바구니로 결제를 끝내는 성인 | 지불자원–되돌림–줄어든 결과가 동일 인물·동선에 연결 | 일반 가격 비교, 다이어트 장보기, 쿠폰 사용 |
| B | 점유 중인 집에서 난방비/서비스 제약 때문에 한 구역에 생활을 모으고 외풍을 막는 성인들 | 비활성 난방원–실내 대응–방 전체 온도 결과 | 고장 난 보일러, 정전 재난, 코지 겨울 인테리어 |
| C | 유급 교대가 끝났지만 보상이 기본비용을 충족하지 못해 다음 대응을 정리하는 성인 | 실제 노동 결과–보상–기본비용–남은 부족 | 야간근무 초상, 배달가방, 피곤한 표정만 |

실험 규칙:

- 각 arm은 원 요청 span, authorial core, candidate pack, composed prompt, runtime request를 독립 동결한다.
- 동일 모델·설정, arm당 1회, 재시도 0회, 대체 모델 0회다.
- prompt/audit, delivery/block, thumbnail gates, native gates, user judgment를 분리한다.
- 한 gate라도 실패하면 arm FAIL이며 blocked render는 unscored다.
- 세 arm 모두 strict PASS하고 별도 user judgment를 받아야 `promote`를 검토한다.

## 11. 리서치 gap matrix와 정지 판단

| 주장군 | 핵심 근거 | 신뢰도 | 남은 공백 | 결정 |
|---|---|---:|---|---|
| 빈곤은 금액 외 다차원 결핍 | World Bank, UNDP, OHCHR | 높음 | 국가별 지표 차이 | broad term 분해 |
| 식량 접근 심각도 | FAO FIES, IPC | 높음 | 사진으로 기간·원인 입증 불가 | 사건 대리물만 P0 |
| 물질·에너지 박탈 | Eurostat, EC | 높음 | 지역별 필요품 차이 | exact 관계 P0 |
| 적정 주거 | OHCHR, OECD, 국토부 | 높음 | 점유·기간·안전성의 사진 한계 | habitability P0, housing insecurity 보류 |
| 근로빈곤 | ILOSTAT | 높음 | 가구 소득선의 비시각성 | 명시 core+관계 P0 |
| 교통·디지털 접근 | DfT, ITU | 중상 | 비용과 기술 장애 혼동 | transport P0, digital P1 |
| 시간·생리·의료 | UN Women, UNICEF | 중상 | duration·민감정보·진단 위험 | 후보 전용 |
| 낙인 없는 재현 | Dóchas, JRF, UNICEF | 중상 | 생성 이미지에 당사자 공동설계 불가 | composition guard+user judgment |

추가 broad 검색은 P0 구조를 바꿀 가능성이 낮다. 남은 공백은 출처 부족보다 **단일 이미지의 관찰 한계**에서 생긴다. 따라서 조사 정지 조건을 충족했다. 다음 유의미한 단계는 더 많은 동의어 수집이 아니라 제안 데이터의 구현, 정확/BM25F 회귀, 그리고 독립 픽셀 실험이다.

## 12. 구현 순서 제안

1. `candidate-data-proposal.json`의 P0 9개만 새 research extension과 authored registry에 옮긴다.
2. broad terms는 exact alias가 아니라 advisory semantic text로 넣고, exact activation은 component-rich event phrase만 사용한다.
3. 60개 후보 중 프로필별 6개를 함께 추가하되, 후보 단독으로 hard profile을 활성화하지 못하게 한다.
4. anti-stigma 공통 guard를 프로필별 `reject_substitutes`, composition instruction, runtime expression에 반복 가능하게 적용한다.
5. `routing-regression-proposal.jsonl`을 실제 unittest fixture로 변환하고 focused tests를 먼저 통과시킨다.
6. visual/semantic index를 실제 배치 크기 1로 재생성하고 registry/hash/holdout을 검증한다.
7. 승인된 경우에만 3-arm 렌더를 수행한다. 픽셀 결과와 사용자 판단 전에는 `implemented`를 넘어선 개선 주장을 하지 않는다.

## 13. 최종 판정

`proposed`

문헌 근거, 저장소 공백, 시각 계약, 후보 데이터, 회귀 및 픽셀 검증 계획은 준비되었다. 런타임 반영·패키지 검증·생성·픽셀·사용자 판단은 아직 수행되지 않았으므로 구현 또는 품질 향상을 주장하지 않는다.
