# 물 관련 시각 의미·후보 데이터 확장 리서치

조사일: 2026-10-06, Asia/Seoul. 기준 대화: [물 관련 용어 조사](chatgpt-conversation://6ac3cfe8-8cf8-83e8-8f33-a78930a7f379).

이번 확장은 **물이 어떤 대상과 어느 경계에서 만나는지, 그 결과 무엇이 보이는지**를 데이터로 만드는 데 초점을 둔다. 물 관련 이름이 검색되는 것과 올바른 형태·소유 관계가 선택되고 사진에 남는 것은 별도 문제다. 물의 물성·지형·생물뿐 아니라 관능·죽음·폭력·공포·의례·상징·의성어도 원 목록에 유지했다.

원 대화의 24개 표, 345개 용어 행과 마지막 7개 조합 예시를 확인했다. `read_thread`는 답변을 20,000자로 잘라 20번째 분야 중간에서 끝냈다. 읽기 전용 브라우저에서 마지막 24번째 표까지 확인해 표의 후반부를 회수했다. [SEED-INVENTORY.json](SEED-INVENTORY.json)은 345행의 원 설명을 보존한다. 원 답변의 전체 산문을 원본 파일로 회수한 것은 아니며, 캐시 산문과 회수한 표의 범위를 [SOURCE-CONVERSATION.json](SOURCE-CONVERSATION.json)에 구분했다.

## 1. 조사 결과와 채택 상태

|산출물|수량|의미|
|---|---:|---|
|원 대화 용어 행|345|각 행을 연구 카드에 연결; 동의어 345개라는 뜻이 아님|
|연구 카드|192|관찰 요소·관계·오인 경계·출처 범위·반영 경로|
|시각 구조 카드와 후보 초안|117|현재 슬롯에 배치하는 제안; owner/property 검증 전|
|형태 가족 카드|45|서로 다른 상태·객체를 유지하고 더 작은 후보로 나눌 대상|
|맥락 카드|30|성분·과정·기원·감각·문화·심리처럼 외관만으로 확정할 수 없는 뜻|
|공개 출처|45|본문, 검색 excerpt, 논문 abstract, 제목 용례를 구분|
|선택 검토 묶음|11|고정 장면이나 일괄 채택 레시피가 아님|
|회귀·픽셀 평가 그룹|각 16|작성된 평가 계획; 실행된 테스트 또는 이미지가 아님|
|형식 프로토타입|4|현행 component compiler의 3개 component → 3개 evidence field → 3개 gate 투영만 확인|

345행의 라우팅 완료는 모든 과학적 주장·특정 종·의례·진단·픽셀 효과가 검증됐다는 뜻이 아니다. 특히 1차 자료가 없는 외형 제안은 카드에 별도로 표시했다. [SOURCES.md](SOURCES.md)의 근거 범위와 [SEMANTIC-CARDS.md](SEMANTIC-CARDS.md)의 개별 오인 경계를 함께 읽어야 한다.

이 연구 작업은 활성 원본, index, 후보팩 생성 경로를 수정하지 않았다. 후보 노출·선택·프롬프트 반영·이미지 생성은 모두 `NOT_PERFORMED`다. 공유 checkout의 다른 변경은 진행 중이므로 저장소 전체의 무변경을 주장하지 않는다. [기준점 차이](LIVE-DRIFT-NOTE.md)를 함께 남겼다. 이번 결과는 반영 전에 검토할 연구 패키지다.

## 2. 현재 데이터에서 발견한 강화 지점

현행 중앙 source manifest가 등록한 확장 파일과 root dictionary/profile을 조사했다. 최초에는 90개 원본 JSON과 12,011개 candidate/profile을 읽었으며, 조사 중 다른 live source 변경이 진행되어 최신 catalog를 다시 작성했다. 정확한 파일·레코드·관련 문자열 수는 [EXISTING-DATA-CATALOG.json](EXISTING-DATA-CATALOG.json)의 `audited_file_count`, `all_record_count`, `related_records`와 source hash를 기준으로 한다. 영문 단어 앞의 경계를 검사해 `driver`가 `river`로 잘못 분류되는 경우도 제거했다. 이 수치는 원본 문자열 조사이며 실제 의미 검색 성능·후보 노출·채택 성공률이 아니다.

|기존 구조|관찰한 상태|반영 방향|
|---|---|---|
|`underwater_caustics`, `underwater_caustic_light`, `surface_caustic_light` 등|광학 명칭과 짧은 label 후보가 여러 슬롯에 있음|수면·빛·수광면 관계를 별도 원본 의미로 작성하고 기존 label의 뜻·슬롯을 보존|
|`sparkling_water_reflection_highlights`|수면의 반사 반짝임 후보가 있음|윤슬·물비늘의 같은 현상을 검토해 한국어 의미와 물결 facet 관계를 보강|
|`wet_damp_clumped_hair_state`|뭉침·부피·부착을 요구하는 기존 시각 profile이 있음|물 밖의 젖은 머리는 재사용; 수중에서 퍼지는 머리는 다른 상태의 sibling으로 설계|
|`sw_wet`, `sw_candidate_wet`|수영복 천 위 방울과 그 사이 원단 결을 다룸|피부·유리·일반 천의 물방울로 소유 범위를 자동 확대하지 않음|
|`sheer_garment_optical_layering`|섬유와 아래층의 부분 투과 관계가 있음|젖음·밀착·비침을 독립 속성으로 유지; 투과 변형은 별도 문맥에서만 채택|
|`intertidal_high_low_exposure_zonation`|상·중·하 대상의 연속 해안 profile이 있음|같은 명세를 중복 생성하지 않고 물선·젖음·기질·생물 소유 관계를 보존|
|자연환경의 습지·산호초·맹그로브·빙하 후보|일부 연결 구조와 장면 후보가 이미 있음|단순 장소 이름을 더 추가하기보다 root–stem–leaf, channel–bar–rejoin 같은 구조를 분해|
|`sw_wetsuit`|선택한 panel·입구 관계의 profile이 있음|드라이슈트의 seal, regulator–hose–mouth, tewak–net 관계를 별도로 작성|
|`ghost_ship_former_vessel_breach`|유령선의 물리적 선체와 초현실 단절을 다룸|일반 난파·침몰·수몰 실내에는 재사용하지 않음|

`snell`, `backscatter`, `marine snow`, `crown splash`, `pancake`, `biofluorescence`, `haenyeo`, `테왁`, `윤슬`, `halocline` 문자열은 조사한 원본 레코드에서 직접 대응을 찾지 못했다. `meniscus`는 초현실 계열에서 발견됐으나 보통 물–유리 경계의 대응으로 볼 수 없다. [LEXICAL-GAP-AUDIT.json](LEXICAL-GAP-AUDIT.json)은 이 조사 방식을 명시한다. 다른 언어·형태적 표현의 존재 가능성이 있어 이 결과를 '런타임이 이 현상을 생성하지 못한다'는 결론으로 쓰지 않는다.

## 3. 물 의미를 구성하는 독립 축

원본 이름을 하나의 넓은 `water` tag로 모으면 소유·재료·기원·동작이 서로 오염된다. 다음 축을 별도로 작성하고, 요청된 관계만 연결한다.

|축|구체적인 데이터|대표 경계|
|---|---|---|
|상태·기원·성분|액체/얼음/기체, 지표/지하/빗물/융수, 염분·처리·용도|맑은 물 ≠ 음용수·담수·증류수|
|상·경계|공기–물, 물–유리, 물–천, 물–피부, 물–침전물|물방울 ≠ 기포; 결로 ≠ 유리 안의 물|
|표면 형태|bead, film, rivulet, jet, splash, crown, foam|젖음 ≠ 광택·투과·밀착|
|수면 운동|파문, 풍파, 너울, 쇄파, 처오름, 되흐름, 항적|물결 ≠ 물 전체의 이동; 항적의 선박 소유|
|광학|반영, 굴절, 수면 glitter, caustic, shaft, scatter, attenuation|빛의 광원·경로·수광면이 다름|
|공간 topology|합류·분기·재합류·격리·연결·퇴적 장벽|망상하천 ≠ 삼각주; 하구 ≠ 삼각주|
|생물 구조|기질–뿌리/holdfast–줄기–잎, 몸–팔–촉완–빨판|해초 ≠ 해조류; 해파리 ≠ 빗해파리|
|인간·장비|몸–수면, 발–fin, cylinder–hose–mouth, float–net–diver|프리다이빙 ≠ 스쿠버; 젖은 몸 ≠ 익수|
|흔적·시간|물얼룩·침수선·salt deposit·녹·건열·표착물|현재 물선 ≠ 과거 침수선; 시간적 과정은 외관과 분리|
|감각·문화·해석|의성어, 냄새, 성적 관심, 공포, 의례, 상징|맥락은 보존하되 욕망·동의·진단·효험을 픽셀 사실로 만들지 않음|

USGS는 경도를 용존 칼슘·마그네슘과, 탁도를 부유 입자에 의한 산란과 연결한다. 따라서 water clarity와 화학 품질을 하나의 시각 속성으로 저장하지 않는다. [USGS 경도](https://www.usgs.gov/water-science-school/science/hardness-water), [USGS 용어집](https://www.usgs.gov/water-science-school/science/water-science-glossary).

## 4. 가장 먼저 보강할 물성과 경계

**방울·수막·물길은 서로 다른 외형 단위다.** W004/W019는 둥근 액체 cap과 부착 표면, W020은 연속 얇은 막과 소재 결, W022는 출발점에서 이어지는 작은 유동 경로를 다룬다. 같은 젖은 표면이라도 이들이 모두 동시에 있어야 할 이유는 없다. 표면장력·응집·부착은 형상을 설명하는 관련 물리이며, 외관을 통해 접촉각·화학적 소수성 값을 역추정하는 계약은 만들지 않는다. [USGS 표면장력](https://www.usgs.gov/water-science-school/science/surface-tension-and-water), [응집·부착](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water).

**결로와 메니스커스의 핵심은 위치다.** W014의 방울은 지정된 차가운 표면, 예를 들어 컵의 바깥 면에 속한다. W007의 굽은 액면은 같은 컵의 안쪽 벽과 이어진다. 컵 밖 방울이 존재한다고 안쪽 물의 곡률을 만족한 것으로 기록하거나, 물을 담은 컵만으로 결로를 의무화하지 않는다. 다공성 재료의 W006은 물 접촉 부위와 이어지는 damp front를 요구하며, 종이 위를 흐르는 물줄기와 종이 내부의 번짐을 나눈다.

**수증기와 흰 plume을 나눈다.** W013은 비가시적 기체·과정의 맥락 카드다. 눈에 보이는 안개·결로 방울을 기체 자체의 관찰 증거로 쓰지 않는다. 온천과 간헐천은 출수점·물줄기·응결된 mist를 따로 작성한다. 발생 온도·습도·주기는 관련 계측 없이 hard pixel gate가 되지 않는다.

**포말은 기포 집단이며 오염 판정이 아니다.** W027은 물속 기체 pocket, W028은 모인 작은 기포의 patch, W024는 공기 중 비말이다. 바다 거품은 유기물을 포함한 물의 교란과 연결되며, 흰 foam 자체가 오염을 증명하지 않는다. [NOAA 해양 거품](https://oceanservice.noaa.gov/facts/seafoam.html).

## 5. 수중 광학을 이름보다 빛의 경로로 강화

|카드|같이 기록할 관계|실패 또는 오인 사례|
|---|---|---|
|W046 윤슬|광원 → 물결 facet → 카메라에 보이는 반사|수중 발광 점, 물에 뿌린 glitter|
|W047 반영|실물 → 같은 수면 평면의 상|수중 실물의 굴절상, 다른 인물의 무근거 반영|
|W048 굴절|같은 물체 → 수면 교차 → 겉보기 변위|실제 절단·복제 물체·추가 팔다리|
|W049 카우스틱|광원 → 굽은 수면 → 지정된 수광면|수면 반짝임만 존재, 수광면과 무관한 tattoo·발광|
|W050 스넬의 창|수중 위보기 → 바깥 풍경 투과 영역 + 주변 수면 반사|잠수정 창·어안 카메라를 고정 전형으로 추가|
|W051 shaft|광원 → 부유 입자 → 보이는 광로|흐릿한 물을 무조건 굵은 빛기둥으로 채움|
|W052 후방산란|카메라 조명 → 전경 입자 → 관찰되는 잡광|음향 해저 backscatter, 기포·snow와 무조건 동일시|
|W053 감쇠|서로 다른 물 경로 길이 → 신호·색·대비 차이|수중 전체에 파란 필터 하나만 적용|
|W054/W055 발광·형광|생물의 발광 또는 외부 여기광과 재방출을 각각 연결|caustic·반사·무지갯빛을 모두 self-emission으로 저장|
|W190 오버언더|한 수면 → 수상·수중 영역 + 동일 객체의 연결|상하 콜라주, 두 수면, 절단된 같은 몸|

윤슬의 사전 의미는 햇빛이나 달빛에 반짝이는 잔물결이다. W046은 이 정의를 물결 facet의 반사 형태로 투영한 연구자 명세다. [국립국어원](https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&pageIndex=1&qna_seq=320787&searchCondition=&searchKeyword=).

굴절·전반사의 설명은 OpenStax와 PBRT를 대조했다. 스넬의 창의 사진 명세는 이 광학을 바탕으로 한 연구자 추론이며, source가 제시한 유일한 카메라 레시피로 보고하지 않는다. 평탄 수면과 시점이 바뀌면 보이는 경계도 달라진다. [OpenStax](https://openstax.org/books/university-physics-volume-3/pages/1-4-total-internal-reflection), [PBRT](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission).

Akkaynak–Treibitz의 수중 영상 모델은 감쇠와 후방산란을 별도 항으로 다룬다. 이번에는 공개 검색에 노출된 저자 abstract를 확인했으며 PDF 전문 열기는 실패했다. 수치·실험 결과·모델의 세부 식을 직접 검증했다는 주장을 하지 않는다. 후보 데이터에는 물 경로·광원·수광면의 분리만 사용하고 자세한 보정 모델은 구현 범위 밖에 둔다. [저자 논문 링크](https://csms.haifa.ac.il/profiles/tTreibitz/webfiles/revised-underwater-image.pdf).

## 6. 강·해안 지형은 연결 차이가 의미

합류부 W064는 두 incoming channel과 하나의 joined downstream을, 망상하천 W070은 사주 사이 분기와 재합류를 요구한다. 우각호 W069는 현재 본류와 옛 굽이 사이의 격리된 공간을 다룬다. 삼각주와 하구는 각각 퇴적 지형과 물이 만나는 수역의 성격이며 등가 별칭이 아니다. [NPS 하천 지형](https://www.nps.gov/subjects/geology/fluvial-landforms.htm), [NOAA 하구](https://oceanservice.noaa.gov/facts/estuary.html).

해안의 사취는 한쪽 해안에서 돌출하고, 육계사주는 두 육지를 잇고, 장벽섬은 외해와 안쪽 수역을 나눈다. W075–W078은 연결 endpoint와 물의 양쪽 위치를 데이터로 둔다. 이름을 하나 더 추가하는 것보다 한 프레임에서 해당 연결이 읽히는지가 중요하다. [NPS 퇴적 해안 지형](https://home.nps.gov/articles/sandy-coast-landforms.htm).

조간대는 이미 강한 profile이 있으므로 현재 수면에서 상·중·하 노출대를 잇는 구조를 보존한다. 조석의 시간적 주기와 현재 장면의 노출 정도를 분리한다. 사진 한 장으로 만조 극점·사리·조금·정확한 조위까지 확정하지 않는다. [NOAA 조석](https://oceanservice.noaa.gov/facts/tides.html).

이안류 W169는 좁은 seaward corridor와 주변 쇄파대, corridor를 따라가는 표면 tracer를 다룬다. 방향성의 시각 제안이며 진단·유속 측정은 아니다. 배수구 vortex와 다른 카드로 둔다. [NOAA 이안류](https://oceanservice.noaa.gov/facts/ripcurrent.html).

## 7. 얼음·심해는 이름이 만드는 잘못된 장면을 교정

해빙은 바닷물이 얼어 생기는 얼음이고 빙산·빙하의 육지 기원과 다르다. 팬케이크 아이스 W042에는 평평한 둥근 원반과 솟은 perimeter rim, 원반 사이 물을 함께 둔다. 얼음의 이동 상태·정착 상태·발생 기원은 다른 의미 축이다. [NSIDC](https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice).

열수분출 W088은 해저 opening에 붙은 particle plume이다. 블랙 스모커를 불·연기로 바꾸지 않는다. 염수호 W089는 해저 함몰부의 pool boundary를 유지하며, 수중에 대기 호수를 추가하는 대체를 거부한다. 밀도·염도는 계측 또는 관측 맥락이다. [NOAA 열수](https://oceanservice.noaa.gov/facts/vents.html), [NOAA 염수호 관측](https://oceanexplorer.noaa.gov/multimedia/daily-image-media-20200917/).

마린 스노 W090는 수주 속 불규칙한 입자 집단을 다루며, 얼음 눈이나 모든 기포로 치환하지 않는다. 침강 과정과 입자의 화학·생물학적 정체는 정지 영상에서의 관찰 범위를 넘어설 수 있다. [NOAA 마린 스노](https://oceanservice.noaa.gov/facts/marinesnow.html).

## 8. 수중 생물의 소유와 접합

**켈프–해초–맹그로브를 구분한다.** W092는 holdfast–stipe–blade, W093은 rooted seafloor meadow, W094는 물–노출 뿌리–수간–수관의 연결이다. 해조류의 holdfast를 잘피의 뿌리와 같은 구조로 저장하지 않는다. floating leaf가 바닥에 이어지는 부엽식물과 자유 부유 식물도 서로 다른 카드에서 분해한다. [NOAA 켈프](https://oceanservice.noaa.gov/facts/kelp.html), [Smithsonian 해초](https://ocean.si.edu/ocean-life/plants-algae/seagrass-and-seagrass-beds).

**해파리와 빗해파리는 다른 구조다.** W100은 bell과 종별 부속지, W101은 몸에 이어진 comb rows를 다룬다. Smithsonian은 빗살판 열의 무지갯빛을 외부 빛의 산란과 연결하며 생물발광과 구분한다. [Smithsonian](https://ocean.si.edu/ocean-life/invertebrates/jellyfish-and-comb-jellies).

**문어·오징어·갑오징어·앵무조개는 팔 수만 비교하는 이름 목록이 아니다.** 몸통–머리–팔/촉완–빨판, 지느러미 margin, 외부 shell aperture를 따로 기록한다. 가려진 팔을 보였다고 추론하거나 squid의 두 긴 촉완을 동일 길이 열 팔로 바꾸지 않는다. 종별 미세 배열과 비가시적 부품은 추가 자료와 가시성 검토 전 hard duty가 아니다. [Smithsonian 두족류](https://ocean.si.edu/ocean-life/invertebrates/octopuses-squids-and-relatives).

가오리·해마·갑각류·어군은 같은 몸의 연결과 개체 경계를 먼저 확보한다. 해마·일부 갑각류의 정확한 종별 근거는 추가 확인 대상으로 남겼다. 연구자의 익숙한 외형 지식만으로 모든 종의 전형을 결정하지 않는다.

## 9. 잠수·젖은 몸·직물의 교차 오류

스노클링은 수면 호흡 변형에서 snorkel–mouth와 air opening–waterline 관계를, 스쿠버는 cylinder–regulator hose–mouth와 장비 부착을 분리한다. 프리다이빙은 숨참기 맥락이지만 정지 사진이 숨참기 지속시간을 증명하지 않는다. fin은 같은 발·다리로 이어져야 한다. [PADI 장비 맥락](https://www.padi.com/help/scuba-certification-faq).

W151의 테왁–망사리–작업자는 부유체·그물주머니·접촉의 세 관계다. 박 소장품과 후대 foam 변형을 섞어 보편 모양으로 고정하지 않는다. 해녀의 나이·직업 정체·작업 능력을 장비와 얼굴의 인상으로 판정하지 않는다. [국립해양박물관](https://www.mmk.or.kr/?folder=collection&idx=53&page=view), [UNESCO](https://ich.unesco.org/en/RL/culture-of-jeju-haenyeo-women-divers-01068).

물 밖 W156의 damp bundle은 중력·부착·부피 감소와 연결된다. 물속 W157의 hair는 같은 scalp에 연결된 상태로 수중 공간에 퍼진다. 기존 뭉침 profile을 넓혀 두 상태를 모두 만족시킬 수 있다고 가정하지 않는다. 젖은 섬유의 모임은 Nature의 연구 abstract를 관련 근거로 확인했으며, 특정 수중 헤어 배열은 연구자 명세로 유지한다. [Bico 등](https://www.nature.com/articles/432690a).

직물에는 wetness, contact/clinging, transmission, fiber continuity를 독립적으로 둔다. 현재 `sw_wet`는 천의 물방울·원단 결이며 투명화 명세가 아니다. W161은 밀착·주름·솔기, W162는 지정된 천과 아래 표면의 광학 투과 변형이다. 섬유와 seam이 사라진 투명 몸은 실패이며, 불투명 의복 요청을 비침으로 변경하는 것도 실패다.

미술사 wet drapery는 실제 젖은 옷만을 가리키지 않는다. Met의 설명은 몸 윤곽을 드러내는 밀착 주름의 표현을 다룬다. 조각·회화·실제 젖은 천의 판본과 재료를 분리한다. [Met](https://www.metmuseum.org/essays/classical-art-and-modern-dress).

## 10. 관능·폭력·공포·문화·소리를 보존하는 방식

스키니 디핑, 목욕·수중 누드, 샤워, 젖은 T셔츠, Aquaphilia, WAM을 조사·coverage에서 제외하지 않았다. 재료·노출·행위·욕망·동의는 별개 의미다. W163/W165는 이름에서 임의의 노출·성행위·관계를 발생시키지 않고 원 요청의 내용을 보존하는 맥락 경로다. W161/W162처럼 관찰 가능한 천의 밀착·투과는 별도로 표현한다.

Aquaphilia는 공개 갤러리의 전시 제목 사용을 확인했을 뿐 보편 성적 정의나 진단을 확인한 것으로 보고하지 않는다. UMD는 자사 용례에서 water-only wetlook과 다른 물질의 messy를 나눈다. 이를 출처가 있는 당사자 정의로 보존하며 인구 집단 전체의 관심·빈도·고정 장면으로 확대하지 않는다. [갤러리 제목 용례](https://hatrockcontemporary.com.au/exhibitions/18-aquaphilia/works/), [UMD 당사자 정의](https://umd.net/termsofservice).

익수·익사·침몰·전복·좌초·수장·물고문·혈액 확산도 coverage에 유지했다. WHO의 drowning 정의는 immersion/submersion으로 인한 호흡장애 과정이며 사망 결과와 다르다. 정지한 수중 몸이나 기포만으로 이를 진단하지 않는다. 물고문은 의미·기록 맥락을 보존한 카드이며 실행 방법이나 질식 조건을 후보화하지 않았다. [WHO](https://www.who.int/news-room/fact-sheets/detail/drowning), [OHCHR 기록 자료](https://www.ohchr.org/sites/default/files/documents/publications/2022-06-29/Istanbul-Protocol_Rev2_EN.pdf).

공포 단어는 viewer effect·당사자 표현·진단을 나눈다. 수몰 실내와 정체불명 형체의 구조는 시각 카드로, 공포나 개인 심리 자체는 맥락 카드로 유지한다. 용왕·용궁·물귀신·의례 이름은 provenance이고 요청에 없는 고정 외형을 만들지 않는다. 초기 여성–새 세이렌과 인어형 해석은 서로 다른 판본이다. [용신 신앙](https://encykorea.aks.ac.kr/Article/E0039556), [RMG 인어·세이렌](https://www.rmg.co.uk/stories/art-culture/what-mermaid).

찰랑·출렁·일렁·넘실은 물체·수면 규모·반영 왜곡에 따른 시각 번역을 분해한다. 졸졸·콸콸·퐁당·첨벙·찰박은 소리 맥락을 유지하며, 실제 요청된 흐름·충돌·얕은 접촉을 사진으로 번역한다. 냄새와 음량을 직접 pixel gate로 쓰지 않는다.

## 11. 후보 초안을 읽는 방법과 남은 확인

[CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json)은 117개 visual 카드만 투영한다. 현재의 슬롯별 dimension은 읽었지만 effect의 실제 target/property는 아직 매핑하지 않았다. `affected_properties_proposal: []`는 '영향이 없다'는 판정이 아니라 **매핑되지 않아 채택하면 안 되는 상태**다. 출처·카드 ID·오인 예시·실패 기록은 positive retrieval text에 섞지 않았다.

45개 family 카드는 서로 다른 지형·동작·소재를 같은 entry의 aliases로 합치지 말라는 명세다. 30개 context 카드는 원 의미를 유지하는 research glossary다. 일부 맥락이 실제 장면의 관찰 의무를 포함하면 해당 relation을 새 원자 후보로 작성할 수 있지만, 맥락 label 자체가 anatomy·pose·노출·재난·행위를 강제하지 않는다.

다음 구현은 117개를 일괄 추가하는 작업이 아니다. 먼저 P0 인터페이스·광학·물 밖/물속 헤어·직물 lock 경계에서 재사용·수정·sibling을 확정하고, 원본 schema·loader·owner·effects·동결 요청과 대조한다. [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 파일 배치, 단계별 산출물과 완료 기준을 구체화했다.
