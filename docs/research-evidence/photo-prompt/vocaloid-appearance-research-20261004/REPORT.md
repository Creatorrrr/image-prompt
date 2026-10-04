# 보컬로이드 외형 데이터 강화 리서치

2026-10-04 · `/Users/chasoik/Projects/image-prompt`

참조 대화 [보컬로이드 외형 요소 조사](chatgpt-conversation://6ac1910a-eff8-83ee-9e25-7fc4df001776)의 키워드를 공식 그림과 현재 저장소에 대조했다. 강화의 중심은 **같은 부품이 어디에 붙고, 어느 표면에 놓이며, 어떤 다른 형태와 구분되는지**다. 캐릭터명을 외형 전체의 단축키로 등록하거나 의상·머리·색·신체 비율을 한꺼번에 묶으면 판본 혼합과 잘못된 owner 전이가 생긴다.

연구 범위는 72개 용어와 102개 디자인 사례다. 72개 전부에 구성요소, 방향 있는 관계, 소유자, 혼동 경계, 현재 프로파일, 후보 속성 제안, 원본 픽셀 게이트를 작성했다. 여기에 판본별 추가 관계 24개, 후보 원본 초안 14개, 시각 프로파일 예시 3개, 추상 표현 경계 6개, 반영 후 검증 계획을 더했다. **이번 산출물은 연구·반영 계획이며 활성 runtime 데이터가 아니다.**

## 1. 조사 범위와 증거 수준

원 대화는 connector의 20,000자 미리보기가 잘려 있어 실제 브라우저에 표시된 17개 표의 후반부까지 읽었다. 기본 디자인 52행, 음성 판본·연도별 행사 의상·게임 의상 50행으로 총 102행이다. ZOLA의 여러 인물, Una의 두 디자인 등 합성 행이 있으므로 이를 정확히 102명의 개인이나 전체 VOCALOID 카탈로그로 세지 않는다. [공식 역사 카탈로그](https://www.vocaloid.com/anniversary/voicebank/)도 훨씬 넓은 제품군을 다룬다.

|항목|확인 결과|의미|
|---|---:|---|
|원 대화 디자인 사례|102행|기본 52행 + 추가 50행|
|원 대화의 서로 다른 URL|96개|같은 합성 그림을 사용하는 행은 출처를 공유|
|원문 공식 이미지|91개|8장 contact sheet에서 전체 윤곽 검토|
|원문 공식 HTML|3개|Snow 안내 + Tianyi/Yanhe 상품 페이지; 전신 그림의 증거와 다름|
|원문 Fandom 출처|2개|OLIVER/SONiKA; 일차 자료로 세지 않음|
|추가 공식 이미지|7개|유카리 2011 설정 3장 + 공식 역사 썸네일 4장|
|개별 원본 해상도 확인|34개|원문 27개 + 추가 7개; 작은 원본은 세부 판정 한계 유지|
|이미지 수신·해시 기록|98개|공식 이미지의 URL·해상도·bytes·SHA-256 기록|

처음 접근하지 못한 Tianyi/Yanhe URL 두 개는 TLS 검증을 유지한 다른 Python 환경으로 재확인했다. 상품 HTML에는 정밀 전신 그림이 없었다. 따라서 **페이지 접근 성공을 외형 세부 확인으로 세지 않았다.** 공식 역사 카탈로그의 200px V3 썸네일을 보완했지만 V5 Lite 외형을 대신 확정하지 않았다. OLIVER의 작은 공식 썸네일은 한쪽 눈의 흰 덮임까지만 보이며, SONiKA는 원문이 지정한 초기 3D 판본과 구슬 목걸이까지 일차 자료로 확정하지 못했다.

증거는 다음 단계로 구분한다. 출처의 상품·판본 식별 → 출처 그림의 관찰 → authored 구조 정의 → 검색/후보 노출 → 선택 및 프롬프트 증거 → 생성 이미지의 원본 픽셀 → 사용자 수용. 앞 단계의 성공은 뒤 단계의 성공을 뜻하지 않는다. 특히 34개 원본 확인은 **공식 source art 검토**이며 새로 생성한 이미지의 합격 기록이 아니다.

전체 영수증은 [SOURCE-RECEIPTS.json](SOURCE-RECEIPTS.json), 보완 자료는 [SUPPLEMENTAL-SOURCES.json](SUPPLEMENTAL-SOURCES.json), 원본 관찰·수정은 [SOURCE-REVIEW.md](SOURCE-REVIEW.md)에 있다. 원본 bytes는 임시 캐시에 보관하고 저장소에는 출처·해시·관찰 기록을 남겼다.

## 2. 현재 데이터와 대조한 결과

현재 loader에 등록된 원본을 읽기 전용으로 집계했다. 시각 프로파일 **1,671개**, 일반 후보 **9,840개 / 112개 슬롯**이다. 후보 수는 병합 후 slot/id 기준이다. 현재 작업 트리의 미커밋 캐릭터 외형 보강도 포함한 시점 값이며, 옛 메모의 프로파일 수를 재사용하지 않았다.

|72개 원문 용어의 처리|개수|비율|해석|
|---|---:|---:|---|
|기존 구조 재사용|24|33.3%|중복 프로파일 추가보다 의미·검색 회귀 확인이 먼저|
|기존 범위 보강/변형|15|20.8%|carrier, 방향, subtype, 조건을 보강하되 기존 범위 보존|
|새 관찰 구조 제안|26|36.1%|기존 정의로 직접 설명되지 않는 연결·표면·지역 배치|
|경계부터 해결|7|9.7%|연령·매체·실제 소품 정체성의 잘못된 전이를 먼저 차단|

이는 **정의 대조 결과**다. 검색 재현율이나 렌더 성공률을 측정한 비율이 아니다. 새 구조 26개가 곧 새 runtime 프로파일 26개라는 뜻도 아니다. carrier별 sibling, 공통 modifier, 기존 프로파일 보강으로 다시 중복을 제거한다.

|원문 범주|용어 수|핵심 강화점|
|---|---:|---|
|머리·얼굴|17|지역 길이, 묶임점 높이, 나선 개수, 염색 배치, 피부 표식의 carrier|
|신체·비율|9|매체·연령·기준점, 의복 윤곽과 몸 윤곽의 분리|
|의복|24|상의-소매 접속, bounded opening, 허리 기준 밑단, rear panel, 레이어/단의 차이|
|장치·장식·소품|22|귀-입 연결, 평면 무늬와 실물 장비, 외부 날개, 별도 소품/동료 owner|

72개 상세 카드와 프로파일 ID의 교차표는 [KEYWORD-RESEARCH.md](KEYWORD-RESEARCH.md)에 있다. 기계가 읽을 수 있는 [KEYWORD-RESEARCH.json](KEYWORD-RESEARCH.json)은 연구용 schema를 사용한다.

## 3. 반영 가치가 높은 구조

### 머리: 전체 스타일명보다 지역 배치

기존 `bilateral_twin_tail_gather`는 좌우 묶임점과 각 다발의 연속성을 이미 정의한다. high twin tail은 귀보다 높은 묶임점이라는 modifier다. 기존 모든 트윈테일에 high를 기본값으로 넣지 않는다. `sca_h05`의 양쪽 나선과 `sca_h06`의 단일 포니 나선도 서로 대안이며 단어 drill만으로 둘을 함께 강제할 수 없다.

가장 명확한 새 형태는 **짧은 후두부 + 얼굴 양옆의 긴 두 sidelock**이다. [유카리 제작자의 2011 자료 목록](https://vocalomakets.com/configuration)과 [모발 전후면 설정](https://vocalomakets.com/images/yukari_100_01.png)에서 직접 확인했다. 기존 `hime_cut_structural`은 긴 뒷머리를 유지하는 정의여서 대체로 쓸 수 없다. 새 프로파일은 regional length partition만 담당하고 보라색·토끼 후드·장치를 자동 추가하지 않는다.

뿌리-끝 옴브레(`sca_h21`), 좌우 분할(`sca_h19`), 겉-안쪽 층(`sca_h20`)은 서로 다른 관계다. 색 순서·구획·가림 관계를 따로 유지한다. 반대로 렌의 짧은 뒤묶음과 Tianyi의 looped braid는 현재 일차 자료에서 고정점/교차 구조를 충분히 확인하지 못했으므로 추가 자료를 확보한 뒤 사례 자격을 부여한다.

### 표면 무늬: 도상의 배열과 장비 기능을 분리

|형태|필수 구조|혼동 대상으로부터의 차이|반영 대상|
|---|---|---|---|
|이퀄라이저 무늬|같은 간격의 세로 열 + 높이 차이 + 같은 옷 면|같은 길이 줄, 실제 음향 표시창|`garment_detail`, 표면 배열 프로파일|
|건반무늬|긴 밝은 칸 + 한쪽에 어긋난 짧은 어두운 칸 + 평면 carrier|흑백 줄, 실제 키보드 악기|`garment_detail`, 인쇄 topology|
|패널무늬|작은 사각 테두리 + 내부 선/점/숫자형 도상 + 지정 옷 면|돌출 단추, 별도 태블릿|`garment_detail`, 평면 panel layout|
|뺨 도상|지정 피부 위치 + 경계가 읽히는 도상|모자 표식, 홍채 무늬, 상처 원인|`body_marking`, 피부 carrier|

MAYU의 [패키지 그림](https://rsc-net.vocaloid.com/assets/image_files/1059d8dcbca298af9a7bfb39c9e101dd/MAYU_600.png)에서는 치마 끝의 건반형 무늬가 보인다. Sapphire의 [공식 일러스트](https://rsc-net.vocaloid.com/assets/image_files/955552af036589ab6bcd22e16fbf76f1/Sapphire_VOCALOID_SHOP.png)는 몸 밖의 고리형 건반 배치다. 같은 keyboard 단어라도 owner, 평면/공간 배치, 부착 관계가 다르다. `midi_controller_external_sound_source`를 둘에 공통 적용하면 실제 장비와 음향 소스를 잘못 추가한다.

UNI의 치마 블록 열, 미쿠/렌의 소매 패널도 새 시각 구조를 만들 가치가 있다. 밝은 테두리·작은 버튼 모양만으로 작동 화면, 소리 반응, 전원, 자체 발광을 도출하지 않는다. 이런 기능은 요청에 명시된 경우 별도 뜻과 증거를 가진다.

### 의복: 겉모양과 접속을 동시에 정의

`sca_g01`은 몸판과 분리 소매 사이의 간격을 이미 정의한다. 오프숄더, 콜드숄더, 홀터넥, 스트랩리스는 각각 다른 천 연결 경로다. 어깨가 보인다는 결과만으로 한 종류로 통합하지 않는다.

새로 추가할 중요한 차이는 **crop 길이와 피부 간격**, **두 벌 사이 간격과 한 벌의 bounded opening**, **긴 rear panel과 floor train/정장 tailcoat**다. crop top이 높은 하의로 피부를 완전히 가려도 crop 길이는 성립한다. 반대로 한 벌의 중앙 구멍은 crop top이 아니다. `pfe_midriff`와 `sw_cutout`의 기존 성인/수영복 범위를 일반 상의 길이나 모든 코스튬으로 넓혀 쓰지 않는다.

티어드의 수평 단, 같은 허리에서 겹친 layer, ruffle의 모인 가장자리, flounce의 재단에 의한 퍼짐, 실제 lace의 openwork도 분리한다. `clothing_ct090_v1`의 무망 guipure 형태를 모든 lace에 강제하지 않는다. 튀튀 역시 선택한 short/multilayer variant를 정의하며 발레 의상 전체를 하나로 단순화하지 않는다. [PNB의 의상 자료](https://www.pnb.org/blog/wardrobe-types-of-tutus/)는 긴 Romantic과 여러 짧은 Classical subtype을 구분한다. [V&A의 실제 튀튀 보존 사례](https://www.vam.ac.uk/articles/conserving-a-ballet-tutu)는 패널·천·봉제 증거를 따로 확인할 보완 일차 자료다. [Met의 obi 자료](https://www.metmuseum.org/art/collection/search/45185)는 실제 의복 체계와 idol costume의 obi-like 띠를 구분하는 참고 자료다.

### 장치: 정확한 접속과 외부 carrier

`sca_x16`은 두 earcup과 돌출 조립체를 정의하지만 입까지 이어지는 boom을 보장하지 않는다. headset에는 **earpiece → connected boom → 같은 얼굴의 mouth-adjacent endpoint**를 추가해야 한다. 각진 머리 고리, 귀 장치, 팔 원형 장비, 모자 도상도 carrier별로 나눈다.

[이로하 V2 패키지](https://www.ah-soft.com/images/products/iroha/v2_iroha_box.jpg)의 팔 원형 장비는 큰 외곽 원·안쪽 동심원·팔 지지를 함께 관찰할 수 있는 사례다. 단순 background speaker나 떠 있는 원으로 대체하면 실패다. [레이싱 미쿠 2017 피규어](https://www.goodsmile.com/gsc-webrevo-sdk-storage-prd/product/image/product/20170818/6655/47064/large/169cf2378d214a6f623e2e92513e9845.jpg)의 투명 날개 판은 외부 부속이다. 회로처럼 보이는 선은 실제 전자 기능, 얇은 판은 생물의 날개 관절을 입증하지 않는다.

막 날개와 얇은 판 날개를 `ca_membrane_wings` 같은 creature 신체 프로파일에 자동 연결하지 않는다. costume의 외부 support, 골격/막 또는 얇은 판, 가장자리, 선택한 transmission에 각각 증거가 필요하다. 등 뒤가 가려져 부착이 안 보이면 `UNOBSERVABLE`이다.

### 신체·독립 소품: 적용 범위를 먼저 해결

현재 body morphology 프로파일은 activation에서 adult를 요구한다. 작은 체구, 등신, 긴 다리, 가는 사지 등은 같은 시점의 anatomical endpoints와 기준물, 매체를 필요로 한다. 공식 chibi나 피규어의 크고 둥근 머리를 사진 속 사람의 체형·연령으로 자동 변환하지 않는다. `bm_long_limb_build`는 long/slender를 함께 요구하므로 다리 길이 하나만 요청한 경우 가늘기까지 묶으면 안 된다.

현재 `candidate_semantic_policy.slot_dimensions.prop`는 빈 배열이다. 독립 봉제인형·canopy·몸에서 떨어진 장식에는 아직 자동 채택할 effect scope가 없다. 그러므로 이 연구에서 작성한 prop 관계는 advisory 자료로 유지하고 실제 request의 named owner/target/property를 해결한 뒤 채택 경로를 검증한다. 빈 scope를 일괄 appearance로 채우는 방식은 제안하지 않는다.

[NurseRobot 공식 그림](https://rsc-net.vocaloid.com/assets/image_files/19c33bbd96b4575d4060be63cdf94cb5/TTNurseRobot_TypeT.png)에서는 인물의 등 장치와 옆 둥근 로봇, 코드가 따로 보인다. 제품명/서사의 android 설명은 노출된 기계 관절을 입증하지 않는다. 주황 광택 다리 착용물도 불투명 표면의 하이라이트이며 자체 발광으로 자동 바꾸지 않는다. 어떤 부품에 코드가 보인다면 모든 주변 물체를 no-tether floating으로 묶을 수 없다. 정확한 원 출처 URL과 해시는 source receipt를 기준으로 삼는다.

## 4. 원문을 그대로 반영하면 생기는 오류

|원문 요약/이름|일차 그림 관찰|데이터 처리|
|---|---|---|
|Luka 기본 검정 부츠/민소매 요약|노랑·금색 부츠와 회색 어깨 패널/위팔 부속|해당 기본 3면도 판본의 색·coverage를 수정|
|MEIKO high collar/dark-red boots 요약|목 뒤 지지의 짧은 붉은 상의, 갈색 부츠|목선 topology와 신발 색을 수정|
|렌의 짧은 뒤묶음|제공된 3면도에서 독립 묶임점 불확정|키워드 구조 제안은 유지, 이 사례의 PASS는 보류|
|堕悪天使 모듈명|녹색 양쪽 drill과 검정 머리 부속; 날개는 미확인|이름으로 wings를 추가하지 않음|
|Racing2015의 창 같은 실루엣|공식 제품 설명은 parasol 소품|형태 비유와 실제 무기 정체성을 분리|
|Fukase 붉은 얼굴 도형|붉은 표면 도상|피·상처·건강/정신 상태 추론 제외|
|NurseRobot라는 제품/캐릭터명|옷·등 장치·별도 동료가 관찰됨|인체를 드러난 로봇 관절로 자동 변경하지 않음|
|공식 chibi 그림의 큰 머리|축약 매체의 비율|adult/body profile 또는 아동 연령으로 자동 전이하지 않음|

기본 수정의 원본은 [Luka 3면도](https://piapro.net/images/official_cos_luka.jpg), [MEIKO 3면도](https://piapro.net/images/official_cos_meiko.jpg), [Len 3면도](https://piapro.net/images/official_cos_len.jpg)다. 우산 정체성은 [Good Smile의 공식 제품 설명](https://www.goodsmile.com/en/product/2739/Nendoroid%2BRacing%2BMiku%2B2015%2BVer.)과 대조했다. 세부 관찰과 해상도 한계는 [SOURCE-REVIEW.md](SOURCE-REVIEW.md)에 개별 기록했다.

## 5. 판본·연도·표현 매체를 보강하는 방법

연구용 variant key는 `case_label + source_id + representation`이다. 상품 판본, 연도별 행사 디자인, 게임 모듈, 기본 설정화, 패키지, chibi, figure를 각각 보존한다. 원문에 판본이 불명확하면 미세 색/부속을 확정하지 않는다.

Snow Miku의 의상은 연도별 주제 디자인이며 [공식 안내](https://snowmiku.com/2026/info_snowmiku.html)는 2012년부터의 공모와 2026년 patisserie 주제를 따로 설명한다. 2010의 흰/연파랑 기본복에 2026의 디저트 모자·밑단 도상을 기본 요소처럼 합쳐 넣지 않는다. 연도별 전체 outfit을 positive alias로 자동 활성화하기보다 모자 부착, 표면 도상, 비대칭 밑단 같은 일반 관계를 추출한다.

[VOCALOMAKETS 설정 목록](https://vocalomakets.com/configuration)은 2011과 이후 판본을 나눠 보여주고, [gynoid 공식 소재 목록](https://www.gynoid.co.jp/news/view/56/)도 상품/발표 시점에 따라 자료를 구분한다. [SEGA 모듈 목록](https://miku.sega.jp/FT/module/)은 게임 모델 자료다. 하나의 이름 아래 모든 자료를 합쳐 appearance truth로 사용하면 안 된다. GUMI V4 등의 Adult/Power/Sweet는 [음성 상품 판본명](https://www.ssw.co.jp/products/vocaloid4/megpoid/)으로 기록하고 인물의 연령·체형·성격으로 옮기지 않는다.

판본에서 얻은 추가 lead 24개는 [DESIGN-RELATION-LEADS.md](DESIGN-RELATION-LEADS.md)에 있다. 예를 들어 Snow2026의 모자에 얹은 디저트형 도상, Racing2017의 별도 날개 판, Snow2025의 좌우 다른 다리 장식, LUMi의 canopy/소매 띠는 서로 다른 연결 규칙이다. 미세 접속·무늬는 coarse source에서 확정하지 않고 확대 자료를 선행한다.

## 6. 후보 데이터와 시각 의미 데이터에 각각 반영할 것

|층|작성할 데이터|필요한 이유|
|---|---|---|
|일반 후보 원본|`concept_units`, typed `relations`, `affected_dimensions`, `affected_properties`, positive paraphrases|노출된 후보 자체에 실제 형태·연결·변경 범위를 제공|
|시각 프로파일|문맥/owner activation, 의미·반례, `authored_components`의 evidence phrase·instruction·native gate|선택된 의미의 필수 조건과 관찰 기준을 일관되게 컴파일|
|optional bundle|`candidate_ids`, `candidate_slots`, associated profile IDs, directed owner relations|서로 관련된 조건을 같은 realization에 연결하되 자동 승격하지 않음|
|연구 provenance|case/version/representation, URL, 해시, 관찰 한계|출처·판본을 추적; positive embedding에 섞지 않음|
|generated index|qualify한 authored data에서 재생성|원본 의미·registry hash와 맞는 exact/BM25F/embedding 검색|

현재 실행 순서는 [prompt_generator.py:10171](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:10171)의 `retrieve_core_slots` → `candidate_pack_resolve_visual_profiles` → obligations/concepts/clarification → immutable `photo-candidate-pack/v6`다. resolver는 첫 슬롯 후보의 라벨만 보는 것이 아니라 **전체 frozen request/core**와 registry-bound index를 기준으로 한다. 후보팩은 편집할 원본 데이터셋이 아니다. [retrieval 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/retrieval-contract.md)에 따라 pre-core 독립성과 post-core 검사를 유지한다.

후보 prototype 14개는 [CANDIDATE-PROTOTYPES.json](CANDIDATE-PROTOTYPES.json)에 있다. character name, module name, URL, 반례를 positive alias/embedding text에 넣지 않았다. `semantic_source`가 그대로 공개할 수 있는 `concept_units`와 directed `relations`를 작성했다. 범위가 미해결인 독립 prop와 body geometry는 이 14개에 섞지 않았다.

시각 프로파일 예시 3개는 [PROFILE-PROTOTYPES.json](PROFILE-PROTOTYPES.json)의 regional hair, headset boom, equalizer motif다. 실제 `authored_components` compiler로 evidence fields·composition instruction·native gates를 컴파일할 수 있음을 확인했다. associated `hard_profile_ids`는 연결 정보이며, optional bundle이 존재하거나 선택되었다는 이유만으로 프로파일을 의무로 승격하지 않는다. 문맥과 독립 component evidence가 별도로 필요하다.

`미래적인`, `고딕한`, `노출이 있는`, `요염한`, `불길한`, `인형 같은` 표현은 [ABSTRACT-TERMS.json](ABSTRACT-TERMS.json)에 필요한 선택 속성과 추론 경계를 기록했다. 평가어를 단일 고정 의상·체형·표정으로 치환하지 않는다.

## 7. 반영 계획과 이번 검증의 경계

실행 파일·단계·성공 기준은 [INTEGRATION-PLAN.md](INTEGRATION-PLAN.md)에 정리했다. 순서는 일차 자료/판본 확정 → 기존 정의와 중복 제거 → P0 구조·후보를 함께 작성 → index 재생성 → 36개 문맥/owner holdout → 원본 픽셀 비교다. P1의 재질/장식 정밀 자료와 P2의 age/medium/prop scope는 각각 선행 조건을 해결한 뒤 진행한다.

이번에 실제 확인한 것은 다음과 같다.

- 원문 용어 72개, 사례 102행, source URL·ID, 기존 프로파일 교차표의 일관성.
- 캐시에 보관한 source bytes 100개(이미지 98 + 보완 HTML 2)의 SHA-256 일치.
- 일반 후보 초안 14개의 entry 구조·현재 slot dimension과의 일치·optional semantic source 보존.
- authored profile 예시 3개와 optional bundle 예시 3개의 실제 compiler 통과.
- 작업 시작에 저장한 기존 파일 86개의 SHA-256이 끝까지 동일함.

36개 holdout과 8개 pixel family는 [VALIDATION-PLAN.md](VALIDATION-PLAN.md)에 **계획만** 작성했다. runtime 원본 반영, active index load qualification, 새 embedding 호출, 실제 검색 비교, 이미지 생성·합격 판정, commit/push는 수행하지 않았다. [VALIDATION-SUMMARY.json](VALIDATION-SUMMARY.json)의 PASS는 연구 산출물과 prototype 구조 검증 결과다.
