# 해리포터 외형 리서치와 데이터 반영 방향

2026-10-06 KST · 요청한 리서치·반영 계획 작성 완료 · 활성 데이터 반영 전

참조 대화의 외형 용어를 **작품/인물/판본을 설명하는 사례 자료**와 **다른 장면에도 재사용할 수 있는 관찰 가능한 형태·관계**로 나눴다. 이름이나 분위기를 늘리는 것보다, 동일한 몸·옷·소품에 어떤 부품이 어떻게 연결되어 있는지와 무엇으로 잘못 대체되기 쉬운지를 강화하는 것이 효과적이다.

이번 산출물은 수신한 키워드 표 **149행 → 시각 의미 단위 120개 → 후보 초안 111개·선택형 묶음 8개**다. 출처 기록 46개, 회귀 명세 제안 1,080건, 원본 이미지 검증 계획 20개 그룹을 함께 작성했다. 이 수치는 활성 profile 증가량이나 통과한 테스트 수가 아니다.

원 참조 답변은 read_thread의 메시지당 20,000자 제한으로 마지막 예시 부분이 잘렸다. 보이는 표 149행은 모두 연결했지만 원 대화 전체·인용 URL 전체를 회수했다고 주장하지 않는다. 직접 찾은 원 출처와 수신본을 구분했다. [수신 범위](REFERENCE-PREVIEW.md), [149행 대조](KEYWORD-AUDIT.md).

## 1. 재검증에서 얻은 중요한 구분

|문제|조사 결과|데이터에 필요한 처리|
|---|---|---|
|마법사 로브와 영화 교복|원작의 기본 로브와 영화의 셔츠·넥타이·니트·로브는 같은 층 구조가 아니다.|H001 기본 로브와 H002 같은 착용자의 층 관계를 구분. 일반 robe에 모든 교복 부품을 의무화하지 않음.|
|기숙사색|원작의 배색과 상품/영화에서 보이는 색은 판본이 다를 수 있다.|색 이름보다 tie/knit edge/hood inside/crest의 지역 배치가 필요. H003–H007.|
|래번클로|원작 blue/bronze와 eagle는 공식 자료에서 확인. 공식 상품 tie는 navy/silver다.|상품 소재·색을 모든 영화 원본 사양으로 옮기지 않음. 완전한 영화 검증에는 해당 편 스틸이 필요.|
|머리의 어수선함|짧은 끝의 방향, 넓은 부피와 잔머리, 긴 거친 장발·수염, 큰 웨이브는 서로 다르다.|H037–H041 별도 구조. 동물의 bushy tail을 scalp hair에 재사용하지 않음.|
|나르시사 투톤|원작 금발/영화 투톤의 차이 확인. 직접 본 홍보 사진에서는 어두운 윗부분·앞 롤, 밝은 옆·아래쪽이 읽힌다.|H043에 색 영역 위치를 명시. 좌우 반반, darker roots, 얼굴 둘레 highlight와 구분. 보이지 않는 뒤쪽은 미확인.|
|무도회 예복|원작 청보라색과 영화 분홍색·실크/시폰·층이 다르다.|H024–H026에 tier topology, transmission, palette version을 분리. 색만으로 동일 예복을 검색하지 않음.|
|플뢰르 결혼식 문양|공식 설명은 흰 튈과 **검정 불사조 두 문양이 만드는 하트**다.|H028의 두 문양·같은 몸판·공동 윤곽 관계. swan으로 잘못 굳히거나 실제 날개/아플리케 제작을 추정하지 않음.|
|루나 파티복|공식 스틸의 짧은 드레스·바깥으로 뻗는 세 층은 일반 긴 tiered skirt와 다르다.|H027의 층 수·입체 돌출·짧은 실루엣을 선택형 sibling으로 검토. H080 별 귀걸이는 별도.|
|죽음을 먹는 자 가면|제작 자료는 4편 부분 덮임/5편 전체 덮임과 개별 문양의 변화를 설명한다.|H075–H076에 덮임, 실제 구멍, 새김, 반사 면을 구분. 전체 얼굴 동일 복제를 피함.|
|인공 눈·손·의족|눈 자리, 팔 끝, 다리 끝에 이어진 부품은 파란 눈·장갑·지팡이·독립 소품과 다르다.|H061–H063, H118은 carrier/endpoint/interface를 요구. 마법 작동·실제 질환 판정은 별개.|
|표식|해골·뱀은 팔 피부 문양과 하늘 표식에서 owner·scale·surface가 다르다.|H065는 아래팔 피부의 문양 관계만. 같은 그림이라도 한 profile로 자동 통합하지 않음.|
|혼성 생물|켄타우로스, 히포그리프, 그리핀, 페가수스의 접합·앞뒤 몸·날개·다리 수가 다르다.|H071–H074에 해부 연결과 오인 경계. 기존 hippogriff 구조를 재사용하되 실제 효과 매핑 심사.|
|유령·후드·부유|투명성, 채도 저하, 얼굴 가림, 지면 간격은 독립 속성이다.|H066/H067. 뿌연 배경이나 잘린 발을 부유·투명성 증거로 삼지 않음.|
|보가트·변장·TS|흉내 낸 모습, 다른 인물의 얼굴을 취한 변장, 팬 성별 재해석은 별개다.|H091/H092는 해석 경계. 한 장면의 의복이나 장발이 변신 과정·몸의 성별을 증명하지 않음.|

원작 로브: [J.K. Rowling Clothing](https://www.harrypotter.com/writing-by-jk-rowling/clothing). 배색: [Colours](https://www.harrypotter.com/writing-by-jk-rowling/colours), [Ravenclaw](https://www.harrypotter.com/house/ravenclaw), [상품 tie](https://harrypottershop.co.uk/products/ravenclaw-house-tie). 교복 재설계는 [Jany Temime 인터뷰](https://fashionista.com/2017/06/jany-temime-harry-potter-costume-designer-interview)에 있다.

원작/영화 외형 대조: [공식 비교](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films). 예복·불사조 문양·세 층 드레스: [공식 의상 소개](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films). 경기복·후일담: [Studio Costumes](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/).

가면: [제작 설명](https://www.harrypotter.com/features/death-eater-masks-and-costumes). 분장·생물: [Creature Effects](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/creature-effects/), [press pack](https://www.wbstudiotour.co.uk/press-office/wbstl-press-pack/). 표식: [Dark Mark](https://www.harrypotter.com/fact-file/magical-miscellany/the-dark-mark). 자세한 출처별 한계는 [SOURCES.md](SOURCES.md)에 있다.

## 2. 시리즈별로 확장할 실제 의미 축

같은 인물을 한 묶음으로 등록하는 방식은 눈색·옷·머리·시기를 잘못 합칠 수 있다. 아래 축을 개별 구조로 다루고, 인물명과 편수는 provenance에 둔다.

|범위|형태로 나눌 대상|대표 카드|추가 확인할 사례|
|---|---|---|---|
|1편|교복 층, 원형/반달 안경, 각진 이마 흉터, 앞니, 가르마, 번, 수염, 문장 니트, 머리 감싼 천|H002, H008, H023, H037–H055, H058, H109|해그리드 실제 moleskin 재질·퀴렐 터번/어깨 연결·플리트윅 scale|
|2편|누빔 조끼·문장·술·한쪽 장갑, 긴 옅은 머리, 단순 천옷, 큰 옆귀, 고양이 얼굴 변형, 뱀·거미 구조|H012–H016, H036, H069–H074, H115|고양이 분장의 정확한 털색·몸/코스튬 연결, 소품 제작과 생물 표면 구분|
|3편|후드 지퍼·별도 내부층, 헌 재단, 렌즈 확대, 다중 장신구, 모래시계 목걸이, 보가트 착의, 후드/부유, 혼성 생물|H018–H019, H050, H067–H072, H077, H088, H111|루핀 변형체의 영화 전용 sparse-fur 구조·시리우스 줄무늬·낡은 옷의 실제 색|
|4편|capelet, 군복형 재단, formal coat, 예복 판본, 세로 주름/가로 층, 레이스, 인공 눈/의족, 뱀형 코, 부분 가면, 대체 손|H009–H011, H024–H033, H059–H064, H075|크룸/세드릭/플뢰르 무도회 세부와 리타 원작/영화 전체 색 묶음|
|5편|분홍 의상, 단계 변화, 펑크 머리·군복 재단 코트, broad robe/trousers, 검정 코르셋/레이스, 배색/장신구|H030–H035, H044, H078–H079, H112|벨라트릭스 코르셋의 앞뒤 실제 여밈; 구체 handbag/neck bow|
|6편|검정 정장, 셔츠 흐트러짐, 투톤의 위치, 후기 로브, 손의 변색, 큰 콧수염, 입체 드레스, 장식 안경, 사자 모자, 보호대|H018, H027, H043, H047, H060, H080–H082|슬러그혼 책의 수염/눈색, 손의 국소 상태, 머리 뒤쪽 등 보이지 않는 부위|
|7편 1부|결혼식 판본, 두 불사조 문양의 하트, 튈, 하객 러플, 문양 코트, 작은 비즈 가방|H026, H028, H083, H099, H101, H114|하객복·들러리복 정확한 색/재단, 제노필리우스 문양, 실제 봉제 공정|
|7편 2부|변장 문맥, 귀·코·턱의 개체차, 군집 owner, 성인 복식/소품·책 에필로그 차이|H070, H092, H107, H119|변장을 한 장면의 인물 정체성 판정과 분리; 특정 얼굴 전체 비율|
|신비한 동물/무대|petrol coat, roomy cloth tailoring, shoulder emphasis/metallic thread sheen, short vs long ponytail, 캐스트별 학교복|H010, H085, H089–H090, H112|퀴니의 정확한 coat ombre, 티나 큰 칼라, 무대판 생산/캐스트별 뒤묶음·프로모 차이|

이 목록은 폭력·상처·비인간 변형을 빼지 않았다. 흉터의 선·표식의 carrier·보철 연결·피부 변색·눈/코의 구조·털·사지를 중립적인 시각 관계로 남겼다. 부상 원인, 실제 건강, 마법 능력, 계급·순혈·성격은 외형의 결과로 자동 판정하지 않는다.

## 3. 팬 창작: 확인한 사례와 선택형 재해석

노벨피아의 [악역영애 말포이](https://novelpia.com/novel/3291)는 특정 팬소설이다. 작품 소개에서 작가 고속도루, 카리나라는 이름, TS 태그와 2021년 공지 기록을 확인했다. 정확한 최초 게시일·전 장의 외형·모든 해외 팬아트와의 파생 관계는 조사하지 못했다.

최근 원 게시물은 web 도구에서 403이 나왔지만, in-app browser에서는 직접 공개 그림이 표시됐다. 따라서 검색 요약만 보고 이미지 관찰을 했다고 쓴 것은 아니다.

|원 게시물|이번에 보이는 것으로 기록한 것|일반화하면 안 되는 것|
|---|---|---|
|[Grizz](https://x.com/grizz056/status/1766771258178613565), 2024-03-10 KST|긴 옅은 머리·초록/회색 교복 방향·다른 머리/표정 상태, 어두운 손톱 사례|2026년에 처음 생긴 개념, 모든 여성형의 눈색·하의·나이|
|[REDTEN](https://x.com/redteneri/status/2102398387194626330), 2026-09-22 KST|긴 옅은 금발·초록 홍채·어두운 고리 귀걸이·초록/회색 층|고리 귀걸이가 공식 필수 설정, 표정이 실제 오만/성격 증거|
|[masoq](https://x.com/masoq095/status/2105042738517295257), 표시 날짜 2026-09-30 KST|긴 밝은 머리·초록 로브 안쪽·회색 니트/치마·여러 포즈|9월 29일이라는 다른 시간대의 요약을 KST로 복사, 모든 팬 해석은 치마여야 한다는 규칙|

이 세 사례는 목적에 맞춘 관찰 표본이며 유행 빈도나 인기도 순위를 계산한 표본이 아니다. [Know Your Meme](https://knowyourmeme.com/memes/malfoid-female-draco-malfoy)는 원 게시물 발견과 용례 확인에 사용했다. 전체 유행의 최초 기원·노벨피아 작품에서의 직접 파생을 증명하는 근거로 쓰지 않았다.

재사용할 수 있는 팬 관련 형태는 다음과 같다.

- **머리**: 길이/흐름 H036, dry slick-back H040, ringlet H042, 색 위치 H043, 밝고 노란 기가 약한 hue H120을 독립 선택.
- **교복**: 같은 wearer 층 H002, 후드 안쪽 H003, tie surface H004, knit edge H005. 이 선택이 치마·바지·몸 비율까지 정하지 않는다.
- **장식**: 고리 귀걸이 H087, 손톱색 H108, 리본 고정부 H106. 리본/링렛은 이번 조사에서 **디자인 제안**이며 세 작가의 고정 공통 규격으로 확인한 것이 아니다.
- **표정·포즈**: eyelid openness와 mouth-corner asymmetry H093, crossed arms와 head direction H094, 상대 시선·소품 소유 H095. 같은 얼굴·같은 몸의 관계로 쓴다.
- **성인 정장/드레스 방향**: 별도의 명시적 성인 판본/요청 아래 H010/H031/H097을 조합한다. 학교복·장발·TS라는 이름에서 성인 여부를 추정하지 않는다.

TS/genderbend, 악역영애, 카리나라는 이름은 해석·작품 경계 H091에 둔다. 외형의 일괄 alias나 신체 변화의 hard obligation으로 만들지 않는다. 무대 성인 장발 H085, 보가트 착의 H092와도 구분한다.

## 4. 기존 데이터에서 확인한 실제 빈틈

조사 당시 HEAD는 900bf2efdd17fbc6a6ef3aa340f3526b1e01f223다. 작업 디렉터리는 다른 작업의 미커밋 파일·인덱스·생성 shard를 포함한다. 읽기 전용으로 현재 registry를 로드했으며 **1,922 profiles**, 원본 후보 entries **10,089개**를 확인했다. 이는 현재 원본 로드의 수치로, 모든 generated index/retrieval/이미지의 정합성 PASS가 아니다. [시점·해시](CHECKOUT-SNAPSHOT.json).

이 리서치는 실제 기존 profile 60개, 후보 14개와 연결했다. 연결은 관련성/재사용 후보이며 동등성을 모두 승인한 개수가 아니다.

|현행 데이터|왜 그대로 합치면 의미가 바뀌는가|반영 제안|
|---|---|---|
|wireframe_round_glasses / ca_spectacle_frame|후보는 원형, profile은 rim/bridge 관계. 반달형과 전부 같지 않음.|H048/H049의 기본 topology 재사용 + shape modifier/sibling.|
|slicked_back_wet|wet state가 포함된다.|H040 dry swept-back을 sibling으로 검토. 기존 wet 의미를 지우지 않음.|
|ca_irregular_scar_lines|두 선 경로 교차가 조건이다.|H058의 비교차 각진 연결 선을 별도 구조로.|
|ca_bushy_tail|nonhuman tail이 owner다.|H038 scalp hair에 tail profile을 재사용하지 않음.|
|clothing_ct018_v2|일반 gathered horizontal tiers.|H027의 세 입체 projecting tiers를 variant로 분리.|
|clothing_ct043_v1|목 둘레의 ruff.|H013 chest-hanging jabot은 별도.|
|costume_ccx_cc26_02|코르셋 뒤의 lacing.|H103 일반 lacing/앞 여밈/보이지 않는 뒤를 구분.|
|clothing_ct090_v2 / costume_ccx_cc27_01|망사 셀, tutu의 허리 아래 층 구조가 서로 다름.|H099의 selected carrier에 맞게 재사용. 모든 튈 드레스가 tutu는 아님.|
|ca_animal_head_mask|wearer 얼굴을 감싼 외부 mask.|H082 머리 위의 모형 모자는 carrier·coverage가 다름.|
|ri_centaur_*|특정 조각의 절단된 팔/무릎 형식.|H071의 완전한 인간/말 접합을 기존 예술판본에 덮어쓰지 않음.|
|hippogriff_eagle_horse_topology|정확한 topology는 이미 있음. 현재 concept_candidate에 명시적 affected properties가 없음.|H072를 복제하기보다 owner/effects mapping부터 심사.|
|bm_prosthetic_connection|성인·잔존 사지·소켓·보철 연결이라는 범위.|H062는 기존 guard 유지. H063 마법 대체 손에 현대 소켓을 강제하지 않음.|
|human_ghost_identity_breach|formerly-living identity와 impossible presence 의미를 함께 다룸.|H066 투명 효과만으로 범위를 약화하지 않음.|
|playful_smirk / silver_blonde_gothic_hair|표정/머리색에 별도 해석·genre가 결합돼 있음.|H093/H120의 중립 국소 형태를 검토하고 기존 interpretive 의미는 유지.|

현재 원본 자산에서 주요 Harry Potter/Hogwarts/Malfoy 등 명칭의 전용 세트를 찾지 못했다. 이는 **일반 구조 데이터가 없다는 뜻이 아니다**. 새 캐릭터 이름 preset을 만드는 것보다 정확한 원자·carrier·관계와 버전 메타데이터를 보강하는 편이 현행 구조에 맞는다.

## 5. 추가한 연구 데이터의 내용과 수용 경계

[상세 카드](SEMANTIC-CARDS.md)는 각 단위에 한국어·영어의 고유명사 없는 요소 분해, 3개 관찰 명세, owner/carrier, directed relation 초안, 오인 경계, source 상태, 관련 profile/후보, 반영 처분을 제공한다.

[후보 초안](CANDIDATE-DRAFTS.json)은 label만 두지 않고 concept_units와 relations, 긍정 검색 텍스트, 슬롯/속성 효과 제안을 붙였다. 출처·캐릭터·편수·실패 상태·반례는 긍정 검색 텍스트에서 분리했다. [선택형 묶음](BUNDLE-DRAFTS.json)은 8개이며 association이나 선택 자체가 hard activation이 되지 않는다.

149행의 근거 상태는 **일부 사실 재확인 76행, 특정 사례 세부를 추가 확인할 lead 43행, 원 대화의 디자인 제안 10행, 일반 형태/기존 데이터 대조 20행**으로 구분했다. 76행도 그 행의 모든 수식어·재질·몸 비율·연결을 확인한 것은 아니다. 정확한 범위는 [SEED-COVERAGE.json](SEED-COVERAGE.json)에 있다.

색이나 파트를 보았다고 실제 fiber, 제작 공정, 마법 작동이나 변신 이력을 확인한 것은 아니다. 공식 기사도 오류가 있을 수 있다. Firenze 인용의 책명 표기는 원문 대조 전 보류했으며, replica 페이지의 상충하는 크기/chain 길이는 invariants에서 제외했다.

H052 teeth를 eye_detail에, H108 nails를 face makeup에 무리하게 넣는 방식은 채택하지 않는다. 관련 기본 slot이 있더라도 실제 carrier/property 경로를 확정해야 한다. 독립 prop·nonhuman body·투명 효과·여러 인물은 같은 main_subject appearance 경로로 일괄 처리할 수 없다.

## 6. 반영 순서

1. **재사용 가능한 기본 구조 보강**: 안경, 칼라, 레이스/튈, 플리츠, 벨벳, 기본 prop grip, broad robe 등 기존 ID·guard·owner를 유지한다. 같은 구조의 온전한 한국어/영어 표현과 문맥만 보강한다.
2. **새 연결·모양과 sibling**: shirt/tie/knit/robe의 같은 wearer 층, 후드 안팎, 각진 흉터, 위치가 지정된 투톤, ring-hourglass necklace, tier geometry, mask coverage/motif를 작성한다.
3. **판본·미확정 owner·팬 변형**: cast/film/book/source를 보존하면서 case evidence를 보충한다. 성별/정체성/변신명에서 신체·옷·눈색을 자동 추가하는 활성화는 만들지 않는다.
4. **원본에서 인덱스 재생성**: 채택한 긍정 문자열과 실제 source hashes를 기준으로 semantic/visual indexes를 재생성한다. compatible cached vectors만 재사용한다.
5. **frozen request/core → pack 노출 → 실제 채택/효과 → 프롬프트 → 원본 픽셀**을 단계별 검증한다. 해당 관계의 검색 성공이 생성 품질 성공을 대신하지 않는다.

파일별 배치·의존성·완료 조건·실행할 검증은 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 정리했다. 이번 턴에서 활성 원본/런타임/인덱스 수정, 후보팩 생성, native generation, commit/push는 실행하지 않았다. 현재 산출물은 연구용이며 실제 채택 상태와 혼동하지 않는다.

## 7. 검증의 현재 범위

연구 JSON 13개, 참조 ID/source 연결, 149행 coverage, 실제 기존 ID 연결과 문서 링크의 구조 검증을 통과했다. [검증 기록](VALIDATION.json)에 범위를 남겼다. H002/H058/H077의 3개 [프로토타입](PROFILE-PROTOTYPES.json)은 각 3개 component에서 evidence fields·instructions·native gates가 만들어지는 compiler 투영을 통과했다. 이것은 실제 registry 활성화·검색 노출·이미지 통과 증거가 아니다.

연구 시작 시 기록한 원본·코드 98개와 generated index manifest 2개의 해시는 검증 시점에도 동일했다. 모든 기존 untracked 파일·shard의 완전한 바이트 보존을 검사한 것은 아니다. 연구 폴더 외 원본·런타임·인덱스는 이 작업에서 수정하지 않았다.

1,080개 [회귀 명세](REGRESSION-PLAN.json)는 같은 연구 카드에서 파생된 검증 설계이며 독립 holdout이나 실행한 테스트가 아니다. [PIXEL-QUALIFICATION-PLAN.json](PIXEL-QUALIFICATION-PLAN.json)의 20개 그룹도 아직 실행하지 않았다. 직접 본 공식 스틸 2개·팬 게시물 3개의 source pixels를 새 생성 이미지의 native-pixel PASS로 보고하지 않는다.

이미지 단계에서는 선택된 구조·소유·연결을 모두 원본 픽셀에서 확인한다. 부분만 만족하면 실패, 필수 가림은 UNOBSERVABLE_NOT_PASS, 생성 차단은 BLOCKED_UNSCORED로 구분한다. 실제 결과에 대한 사용자 미감 평가는 pending이다.
