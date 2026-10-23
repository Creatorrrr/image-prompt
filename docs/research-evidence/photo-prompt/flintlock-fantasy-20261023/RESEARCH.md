# 플린트록 판타지 시각 의미·후보 보강 리서치

조사일: 2026-10-23, Asia/Seoul. 대상 저장소: `/Users/chasoik/Projects/image-prompt`.

핵심 제안은 **장르명 하나를 늘리는 대신, 총기의 구분 축·가시 부품·사람과 장비의 소유 관계·집단과 건축의 공간 관계를 보강**하는 것이다. 국가·신분·동의·실제 기능·시간적 결과는 별도 문맥으로 남긴다. 결과는 연구 파일이며 운영 데이터 반영이나 성능 향상 실적이 아니다.

## 1. 참조 대화와 조사 범위

참조는 [플린트록 판타지 조사](chatgpt-conversation://6adaf52d-728c-83e8-8f50-62a93a082bc4)이다. 처음에는 `read_thread`의 항목당 20,000자 제한으로 12-2절 중간까지 읽혔다. **이후 사용자의 요청대로 로그인된 Google Chrome에서 원문 17절 전체와 마지막 여덟 장르 조합을 확인해 누락을 해소했다.** Chrome browser API는 연결되지 않았지만 native accessibility로 대화를 읽을 수 있었다. 초기 조각은 `reference-excerpt.md`, 회수한 후반 표제·용어와 설명 요약은 `reference-chrome-supplement.md`, 접근 이력은 `REFERENCE-ACCESS.json`에 보존했다. 후반 파일은 원문 전체의 byte-exact DOM export는 아니다.

원문의 1~12절은 장르, 화기, 병과·대형, 포병·요새, 해군, 병참, 마법, 정치·무역, 도시·지식·미학이다. 13절은 성적 관계·사교·금기·젠더, 14절은 폭력·전쟁 피해·의학·신체 공포, 15절은 비유럽 확장, 16절은 대표작 아홉 개, 17절은 창작 조합 여덟 개다. 초기 조각에서 추출한 경로, 크롬에서 회수한 경로, 독립 보충 용어는 origin으로 구분했다.

외부 출처는 57건이다. 본문을 연 48건과 검색 색인만 확인한 9건을 구분했다. 후자의 원인은 403·429·500·timeout 또는 검색 텍스트/PDF까지만 읽은 범위이다. 작품 자료는 소개·용어집·서지 범위이며 작품 전문/게임 플레이를 검토하지 않았다. **원전 이미지·도판의 직접 픽셀 검토는 수행하지 않았다.** 따라서 박물관의 소장명·설명 확인과 미세 부품 고증 승인을 구분한다. 출처별 주장 범위·접근 상태·연대 제한은 `SOURCES.tsv`와 `sources.json`을 따른다.

## 2. 먼저 바로잡을 분류 체계

플린트록 판타지의 대표 환경은 근세적 총포와 환상 요소의 공존이다. Texas A&M의 장르 설명도 이를 강조한다. 이것은 전열보병·나폴레옹·프랑스·어두운 전쟁터를 모든 요청에 의무화하는 규격이 아니다. [Texas A&M, Django Wexler Collection](https://findingaids.library.tamu.edu/index.php/django-wexler-collection)

| 구분 축 | 의미 | 가시 근거 후보 | 피할 오판 |
|---|---|---|---|
| 점화 방식 | matchlock / wheellock / snaphaunce / flintlock / caplock | 심지, 외부 wheel, 분리된 덮개, flint-cock-frizzen-pan, 해머와 뇌관 돌기 | 모두 오래된 총이라는 이유로 한 구조에 혼합 |
| 총열 내부 | smoothbore / rifled | 직접 보이는 총강·단면 모형의 홈 | 외부 나선 장식이나 길이로 강선 판정 |
| 장전 위치 | muzzle-loading / breech-loading | 선택한 모델의 구조·명시된 단면/학습 모형 | 초기 후장식이면 현대 연발총이라고 판단 |
| 무기 형식 | musket / pistol / carbine / blunderbuss | 전신 비례, 손잡이, 총열·총구·격발부 | rifle=현대 자동소총, carbine=항상 강선 |
| 역사적 소장/제식 | Brown Bess / Charleville / Baker 등 | 특정 실물·모델·연도·명문·박물관 기록 | 일반 장총 silhouette만으로 특정 제식 확정 |
| 상태·결과 | 미장전, 불발, 지연발화, 사격 성공 | 선언 문맥·순차 기록·동영상 등 추가 근거 | 연기 한 장으로 모든 시간 상태를 판정 |

NIJ는 flintlock의 frizzen이 타격면과 접시 덮개 역할을 합친 점을 snaphaunce와의 중요한 차이로 설명한다. 내부 강선과 초기 후장식은 별도 축이다. 구체 학습 모형을 제안한 A07/A08도 실물 사진과 표현 층을 분리했다. [NIJ, Ignition Systems](https://nij.ojp.gov/nij-hosted-online-training-courses/firearms-examiner-training/module-03/ignition-systems), [Royal Armouries, Waterloo 1815](https://royalarmouries.org/objects-and-stories/stories/waterloo-1815)

## 3. 역사 자료가 주는 시각적 구별과 채택 한계

### 총기·부속품: A01–A08, B01–B08

총열·총상만 있는 후보로는 수석식을 구별하기 어렵다. A01은 부싯돌의 물림, 별도 얕은 접시, 프리즌의 위치를 같은 lock의 관계로 묶었다. A02·A03·A04·A06은 다른 점화 방식을 별도 대안으로 둔다. 스냅헌스·미켈레트의 정밀 구조는 실물 도판을 보완하기 전 채택 보류다.

B04는 socket이 총열 둘레를 감싸며 칼날이 열린 총구를 막지 않는 관계를 제안한다. B05는 종이 포장과 구형 금속 탄환을 분리한다. 닫힌 포장으로 내용물·화학 조성·장전 완료를 단정하지 않는다. 1743년 주머니 자료와 후기 뇌관총의 탄약 자료도 연대가 다르다. [NAM, 1704 dog-lock musket](https://collection.nam.ac.uk/detail.php?acc=1984-08-96-1), [NAM, 1743 cartridge pouch — 색인 확인](https://collection.nam.ac.uk/detail.php?acc=1963-10-331-1)

비유럽 표본은 별도 계보와 provenance를 보존해야 한다. Met의 1784–85년 오스만 miquelet gun과 Walters의 장식총은 좋은 비교 자료다. 특히 Walters 표본은 총 자체가 1732/33년, 현재 lock은 1861/62년이다. 현재 모습을 하나의 당대 원형으로 복제하면 연대 오류가 된다. 금 상감은 miquelet이라는 기계 구조의 가시 증거가 아니다. [Met, Miquelet Gun](https://www.metmuseum.org/art/collection/search/30605), [Walters, Gun 51.84](https://art.thewalters.org/object/51.84/)

### 대형·복식·병과: C01–C08

전열·종대·방진은 군복 색이 아니라 **횡방향 폭·깊이·중심의 빈 공간·총구의 지향**으로 구분한다. 방진은 네 면과 바깥 방향이 읽혀야 한다. 한 면만 보이는 좁은 크롭은 방진 전체의 통과 증거가 아니다. 산병 배치는 병사별 간격과 엄폐물 소유를 다루며, 모든 산병을 라이플병으로 분류하지 않는다.

흉갑기병은 천 코트 바깥의 별도 흉갑과 말의 관계, 후사르풍 pelisse는 한쪽 어깨에 걸린 겉재킷과 속재킷의 층을 검토한다. 이것은 특정 연대·군적·계급의 자동 판정이 아니다. NAM 자료도 용기병의 역할 변화와 여러 기병 유형을 구별한다. 후기 1848/1854년 표본을 1815년 복식 정답으로 그대로 옮기지 않는다. [NAM, Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles)

### 포병·요새: D01–D08

요새는 높고 뾰족한 성보다 **낮게 돌출된 보루, 본체와 분리된 외보, 사이의 해자, 바깥 완사면**이라는 관계가 중요하다. 보루는 enceinte에 붙고, ravelin은 앞쪽에서 분리되며, glacis는 바깥 지면까지 완만하게 이어진다. 별 모양 문양이나 지도 전체의 장식만으로 이 관계를 대체하지 않는다. [Vauban, Bastion](https://sites-vauban.org/en/resources/glossary/bastion), [Ravelin](https://sites-vauban.org/en/resources/glossary/demi-lune-or-ravelin), [Glacis](https://sites-vauban.org/ressources/glossaire/glacis)

포탄은 실체탄·폭발탄·canister·포도탄·유산탄·연결탄을 분리한다. D02의 닫힌 구체는 바깥 형태만 확인할 수 있어 내부가 찼다는 판정을 하지 않는다. D03/D04는 내부를 보여 주기 위해 명시적인 교육 단면 모형으로 제안했다. NPS의 사례는 19세기이므로 전체 18세기에 보급됐다는 근거로 쓰지 않는다. RCA 페이지의 중심 유물 사진은 WW1 포탄이므로 초기 구형 유산탄의 외형 정답이 아니다. [NPS, Types of Rounds](https://www.nps.gov/fosc/learn/education/artshot.htm), [RCA Museum, Shrapnel Round](https://en.rcamuseum.com/a-rusty-shrapnel-round/)

### 범선·해군: E01–E08

현측포에서는 선체의 긴 축과 사격 방향이 다르다. 포문·포신·갑판·연기의 접점이 같은 배에 속해야 한다. carronade의 짧고 굵은 포신과 슬라이드 포가는 장포신 함포와 별도 실현이다. E04의 단단한 bar와 E05의 유연한 chain도 구별하며, **chain shot의 직접 소장 원전은 아직 확보하지 못해 E05를 보류**했다. [RMG, Carronade](https://www.rmg.co.uk/stories/maritime-history/what-was-carronade), [RMG, Bar shot](https://www.rmg.co.uk/collections/objects/rmgc-object-36875)

사략선의 경계는 선박의 검은 깃발보다 위임·허가·나포 제도에 있다. E06의 허구 문서와 봉인은 그 제도를 시각적으로 암시하는 선택안일 뿐 실제 허가의 유효성을 증명하지 않는다. 승선 배치도 공격·구조·교역을 외형만으로 구분할 수 없다. [US NHHC, Privateers — 색인 확인](https://www.history.navy.mil/our-collections/art/exhibits/conflicts-and-operations/the-war-of-1812/privateers.html)

### 병참·노동·통신: F01–F08

장르를 전투뿐 아니라 적재·수송·세탁·판매·문서 전달·신호 장치로 확장한다. F03/F04는 사람의 손·젖은 천·통·음식 그릇의 접점을 각각 구체화했다. 종군 민간인을 매춘부로 일괄 번역하는 대신 실제 노동과 계약·군적·가족·성적 관계를 분리한다. 미국 독립혁명 박물관의 자료는 바느질·세탁·식품 판매의 역할을 명시한다. NPS 세탁부 자료의 후기 제도·도구는 따로 연대를 관리한다. [Museum of the American Revolution, Camp Followers](https://www.amrevmuseum.org/virtualexhibits/picturing-washington-s-army/pages/campfollowers), [NPS, Army Laundress](https://www.nps.gov/articles/000/the-army-laundress.htm)

F06은 탑·중앙 보·관절형 끝팔·피벗을 제안한다. Science Museum의 원전은 1792년 고안된 시스템을 재현한 **1933년 모형**이다. 그 모형의 관절 배치와 실제 원거리 메시지 전달 성공은 별개다. [Science Museum Group, Chappe model](https://collection.sciencemuseumgroup.org.uk/objects/co48224/one-model-of-chappe-semaphore-tower)

### 도시·정치·옷·상징: G01–G09

정치 상징은 부착 위치·형태·문자처럼 보이는 부분과 정치적 의미를 나눠 저장한다. G01의 삼색 리본, G02의 인쇄 낱장, G03의 허구 회사 표지, G04의 장부는 각각 구체적 형태다. 국적·충성·공화주의·과세·수탈·실제 재산권은 따로 근거가 필요하다. 회사군을 외국인 용병만의 집단으로 고정하지 않는다. [Met, Revolutionary Cap](https://www.metmuseum.org/art/collection/search/689887), [LOC, Broadsides](https://www.loc.gov/static/collections/broadsides-and-other-printed-ephemera/articles-and-essays/introduction-to-printed-ephemera-collection/the-popularity-of-broadsides.html), [NAM, Company Armies](https://www.nam.ac.uk/explore/armies-east-india-company)

커피하우스는 유럽 사교계에만 한정하지 않는다. 커피의 교역·순례·사회적 교류 맥락을 보충하여 비유럽 도시·민간 생활의 구성을 열어 둔다. 로코코는 금색 자체보다 비대칭 S/C 곡선과 자연 모티프를 구별한다. 드레스의 앞트임/속치마와 등 주름은 서로 다른 관찰 방향이므로 G07/G09로 분리했다. 이것을 귀족·성인 연령·직업·성적 의도의 근거로 쓰지 않는다. [British Museum, Coffee — 색인 확인](https://www.britishmuseum.org/exhibitions/life-cup-coffee-culture-islamic-world), [V&A, Rococo](https://www.vam.ac.uk/articles/the-rococo-style-an-introduction), [Met, Robe](https://www.metmuseum.org/art/collection/search/159432)

### 화약과 마법: H01–H08

작품 사례는 마법의 밀도와 기술의 관계가 다양하다는 근거로 사용한다. 《Promise of Blood》의 화약 마법사, 《Shadow Campaigns》의 미묘한 마법, 《Temeraire》의 공중 군단을 하나의 공통 마법 규칙으로 합치지 않는다. 이번의 부유 알갱이·발광 곡선·장벽·신호 원반·용의 승무원 발판은 **연구자가 만든 선택적 창작 실현**이다. 원전에 정확히 그 형상이 있다고 주장하지 않는다. [Brian McClellan](https://www.brianmcclellan.com/promise-of-blood), [Django Wexler](https://djangowexler.com/series/the-shadow-campaigns/), [His Majesty’s Dragon, publisher](https://www.penguinrandomhouse.com/books/122950/his-majestys-dragon-by-naomi-novik/)

소유자 검토의 핵심은 매개→작용점→대상→경계다. 치유자의 손과 환자의 팔, 용 몸과 외부 마구, 발판과 승무원은 각각 독립된 endpoint다. 빛·뼈·연기만으로 치유 성공·부활·의식·탄도 변화·동의를 입증하지 않는다.

### 크롬 회수 후 보강한 복식·공간·의학·지역: J01–J16

삼각모/이각모/샤코는 챙의 접힘과 높은 몸체를, coatee는 앞 밑단과 뒤 꼬리를, gorget은 목 아래 별도 현수판과 양 끝 구멍을 구별한다. 조끼·무릎바지·목천·stays·panniers·높인 허리선은 각 착용 부위와 의복 층이 다르다. 현대 three-piece suit나 몸에 붙은 조끼형 앞패널을 18세기의 별도 조끼로 자동 재사용하지 않는다. 후기 hourglass corset을 모든 stays의 정답으로 삼지 않는다. [Met, Eighteenth-Century Dress](https://www.metmuseum.org/essays/eighteenth-century-european-dress), [V&A, City & Commerce](https://www.vam.ac.uk/audioguide/europeaudio/tour/5/), [NAM, Gorget](https://collection.nam.ac.uk/detail.php?acc=1986-12-33-1)

J14는 flying ambulance를 날개 없는 역사적 구호마차로 다룬다. RCPSG 자료에 있는 두 바퀴·완충 내부·뒷문·들것 출입이라는 구조가 근거이며, 현대 구급차/monitor를 포함한 기존 후보는 역사적 정답으로 대체하지 않는다. J16의 로더넘은 사각 유리병·유리 마개·박물관 표찰의 층으로 제안했다. 표찰이나 액체색이 실제 성분·용량·의존·효능을 증명하지 않는다. [RCPSG, Waterloo medicine](https://heritageblog.rcpsg.ac.uk/2015/06/09/medicine-and-surgery-at-the-battle-of-waterloo/), [Science Museum, Laudanum Bottle](https://collection.sciencemuseumgroup.org.uk/objects/co8345344/bottle-of-laudanum)

J15는 오스만 표본과 별개로, 마이소르의 1793–94년 총에서 호랑이 머리 cock과 장식 총열을 확인한 뒤 만든 제안이다. 기술 이전·왕실 표상·전리품 provenance를 보존하되 모든 남아시아 무기에 같은 장식을 강제하지 않는다. 동아시아 화승총도 넓은 화약 판타지의 별도 경로로 둔다. 같은 시대라는 이유로 수석식을 자동 장착하지 않는다. [Met, Mysore Blunderbuss](https://www.metmuseum.org/art/collection/search/24490), [국사편찬위원회, 조총과 홍이포](https://contents.history.go.kr/front/kc/printViewPopup.do?levelId=kc_i305630)

## 4. 성적 관계·폭력·예속을 다루는 데이터 방식

I09–I12와 I17–I21은 성·폭력·정체·제도·비평·작품 차이를 문맥 카드로 보존한다. 다음은 서로 다른 개념이며 자동 동의어가 아니다.

| 연구 개념 | 보존할 의미 차이 | 외형만으로 판정할 수 없는 것 |
|---|---|---|
| prostitution / brothel / courtesan / mistress | 거래 행위·장소·사회적 역할·지속 관계의 차이; 시대별 뜻 추가 조사 필요 | 의복·돈·침대에서 직업, 대가, 관계, 동의 확정 |
| camp follower / sutler / 군영 노동자 | 군을 따라 생활하는 넓은 집단과 구체 판매/노동 역할 | 가족·군적·성매매를 한 분류로 결합 |
| charm / compulsion / consent | 허구 능력·강제 작용·동의의 독립성 | 눈빛·노출·수동 자세·마법 빛에서 의사와 원인 확정 |
| slavery / captivity / forced labour / abolition | 제도·구금 상태·노동 강제·법/운동 변화의 차이 | 피부색·족쇄·노동 자세에서 법적 신분·범죄·해방 확정 |
| execution / torture / massacre / dismemberment | 행위·목적·규모·신체 변화와 시점의 차이 | 기구·혈흔·상처에서 사망·가해자·의도·전후 순서 확정 |
| amputation / surgical instrument / healing | 신체 상태·기구·치료 행위/결과의 차이 | 톱 또는 빛 하나로 절단·감염·통증·회복 성공 확정 |

Hogarth 자료는 18세기 성매매를 다루지만 풍자와 도덕극이라는 표현 층이 있다. 소장 유물의 알려진 노예무역 맥락과 새 사진 속 사람의 정체도 별개다. 기구 전시 F07/F08은 사람이나 사건을 자동 추가하지 않는다. [Soane Museum, Hogarth](https://www.soane.org/features/hogarth-101), [RMG, Leg-irons](https://www.rmg.co.uk/collections/objects/rmgc-object-254405), [Science Museum, Hand-bone Saw](https://collection.sciencemuseumgroup.org.uk/objects/co167835/benjamin-bell-type-metacarpal-amputation-saw-europe-1780-1850)

크롬에서 회수한 몰리 하우스와 royal mistress의 구별을 별도로 보강했다. London Museum은 몰리 하우스를 주로 사교·음주·춤·젠더 표현을 위한 만남의 공간으로 설명하며, 사료가 형사재판 기록에 편중된 한계도 밝힌다. Versailles는 퐁파두르의 정부·친구·조언자·후원자 역할과 관계의 시기별 변화를 다룬다. 각각 장소=성매매, 인물=성적 역할 하나로 축소하는 것을 막는 근거다. [London Museum](https://www.londonmuseum.org.uk/blog/molly-houses-queer-subculture-georgian-london/), [Versailles, Pompadour](https://en.chateauversailles.fr/discover/history/great-characters/madame-pompadour)

실제 바다호스의 약탈·성폭력·민간인 피해 기록도 대조했다. 사건의 역사적 기록을 보존하는 일과 새 이미지에서 가해자·강제·원인·사망을 판정하는 일은 다르다. war trauma/moral injury/reproductive coercion은 현대 분석어로 보존하며 당시 인물의 실제 어휘 또는 외형 진단으로 쓰지 않는다. [NAM, Peninsular War](https://www.nam.ac.uk/explore/peninsular-war)

이 표는 법률·의학 판단이나 모든 용어의 역사적 정의를 완료한 사전이 아니다. 시각 후보에 잘못 실리는 추론을 분리한 연구 결과다. 시대·지역별 사회사 원전과 사건별 전문 조사는 후속 필요 항목으로 남겼다. 모든 후보의 연령·동의·강제·노출·상처는 실제 요청 범위와 독립 자격을 따라 검토한다.

## 5. 현행 후보에서 확인한 보강 지점

연구 기준 authored manifest에는 **20,341 source, 15,120 binding, 149 slot**이 있었다. 최초 고정 어휘 감사는 44건/수동 13건, 크롬 회수 후 추가 감사는 40건/수동 13건이다. 중복을 제거한 수동 검토는 **25 source**다. 이는 20,341개 전체의 의미 동등성 심사나 retrieval 측정이 아니다. 원문 전체·hash는 `existing-source-mapping.json`, `existing-source-supplement.json`에 있다.

1. 보루/외보 CID는 이미 본체 부착·해자 건너 분리·입구 차폐라는 EN 관계를 갖는다. KO는 제목형 축약이므로 기존 CID의 번역/embedding/효과 범위를 보정하는 것이 우선이다.
2. 포대 CID도 포좌·흉벽·포문 정렬을 이미 갖는다. 이를 새 장르 태그만 붙인 중복 후보로 늘리지 않는다.
3. 휠록 전시 CID의 alias에 플린트록이 포함되지만, 본문은 wheel 구조다. alias 검색 노출과 positive flintlock 의미를 혼동하지 않는다.
4. 일반 총기 정물의 embedding은 현대 slide·cylinder·receiver를 포함한다. 넓은 firearm alias만으로 역사 화기의 정답이라고 판정하면 안 된다.
5. 삼각모는 소품이고 pirate tag는 직업 증명이 아니다. 흉갑+러프의 기존 완전 bundle에서는 러프를 삭제해 흉갑기병이라고 재명명하지 않는다.
6. 왕실 근위 제복의 princess/royal 문맥과 실제 guard를 보존한다. 일반 장교·회사군으로 강제 확장하지 않는다.
7. camera bayonet와 data cartridge 등 다의어 일치를 포함해, 어휘만 일치한 나머지 31건은 defer로 기록했다.

추가 감사에서는 엠파이어 이음선, 별도 열린 조끼, 화장대/문 너머 침대의 완전 공간 후보를 재사용/보정 대상으로 찾았다. 반대로 겉치마 폭은 숨은 파니에 후프를 증명하지 않으며, 조끼형 붙박이 패널·현대 구급차/monitor는 별도 반례다. 영어 동사 stays를 의복으로 잘못 세는 탐색도 제외했다.

신규 81개 CID를 추가하자는 결론이 아니다. 81개 시각 초안의 처리 제안은 new 52, refine 6, reuse 1, defer 22이다. 이 수치는 **카드/초안 단위**이며 기존 CID 단위 수와 다르다. 문맥 21개는 별도로 유지한다. 모든 초안의 native 자격·검색·픽셀·사용자 수용은 아직 미검증이다.

## 6. 실제 부족분과 우선순위

| 우선 | 작업 | 이유 |
|---|---|---|
| P0 | A01/B01/B04/B05/B06의 부품과 소유 관계 | 수석식 요청을 현대 총기/넓은 genre 후보로 대체하는 오판 방지 |
| P0 | D01/D05/D06 기존 CID의 KO·전체 의미 보존 | 이미 있는 좋은 관계를 중복보다 먼저 살림 |
| P0 | C01/C02/C03 대형 구분 | 인물 수·방향·깊이·빈 중심이라는 어려운 관계를 직접 검증 |
| P0 | F03/F04 노동·생활, F06 통신 | 장르를 전투·제복으로만 축소하지 않음 |
| P0 | I군의 비가시 주장 경계 | 장르·옷·기구가 신분/동의/원인을 만드는 회귀 방지 |
| P1 | 오스만 표본·역사 제식·복식·포차·해군 연결탄 | 정확한 실물 도판/연대·물리 연결 보완 후 채택 |
| P1 | H군 마법 실현 | requester가 선택한 매개·작용점·대상 안에서만 창작 |
| 보류 | chain shot·풍상 도식·세부 공성/정치/성적 역할의 역사 정의 | 직접 원전이나 정의가 충분하지 않은 범위를 명시적으로 남김 |

22개 카드는 정밀 도판·물리 관계·특정 원전 보완이 추가로 필요하다. 이 22개 이외의 카드도 source-image/native 검토를 통과한 것은 아니다. 원문의 대표작 아홉 개와 조합 여덟 개는 I20/I21로 보존하고 `SCENE-DIRECTIONS.md`에서 실제 장면 관계로 연결했다. 자세한 수행 순서·대상 파일·통과 조건은 `IMPLEMENTATION-PLAN.md`, 실제 이미지 검증 설계는 `PIXEL-PLAN.md`에 있다.
