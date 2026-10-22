# 러브크래프트적 공포: 시각 의미·후보 데이터 보강 조사

조사일: 2026-10-22. 참조: [러브크래프트 공포 용어 정리](https://chatgpt.com/c/6ad9bf09-c888-83ec-a092-36fbff61fd93).

## 결론과 범위

가장 먼저 강화할 부분은 **한영 의미의 일치, 관계 양끝의 명시, 원전별 대상·판본, 정지 이미지에서 입증할 수 없는 주장과의 경계**다. 기존의 촉수·거석·심해·불가능 공간을 비슷한 문장으로 더 늘리는 방식의 효용은 작다. 기록 매체의 대응, 다른 몸 비례에 맞춘 생활 공간, 원전의 구체적인 물건 구조, 비적대적 접촉처럼 장면의 관계를 바꾸는 자료가 더 유용하다.

이번 결과는 연구 자료와 반영 계획이다. 운영 의미 레지스트리·후보·binding·검색 인덱스·설치본·CURRENT를 이 작업에서 수정하지 않았다. 실제 검색, 임베딩, 이미지 생성, 픽셀 평가, 커밋·푸시는 실행하지 않았다. 기존 데이터의 manifest 등록은 확인했지만 native qualification이나 현재 설치본 채택을 확인한 것은 아니다.

참조 대화는 도구 응답이 20,000자에서 잘려 브라우저의 렌더링된 표와 본문으로 보완했다. **13개 주제의 용어 표 16개, 항목 185개**를 순서 그대로 보존했다. 별도의 혼동 정정 9행·작품 안내 12행·창작 조합 6행은 용어 개수에 합산하지 않았다. `/`로 묶인 복합 항목은 원 항목 하나로 세며 독립 동의어가 검증됐다는 뜻은 아니다.

## 조사 근거의 강도

45개 출처에 접근했고, 44개는 정의·해당 장면·편집 설명 또는 출판사 소개의 한정된 범위를 읽었다. 전 작품·전 비평서 정독이나 185개 정의 각각의 독립 검증은 아니다. [출처 장부](SOURCES.tsv)의 `review_level`, `review_locator`, `claim_limit`이 실제 근거 범위다.

주요 근거는 러브크래프트 원전·작가 에세이·편지 전사본, 체임버스 원전, Chaosium의 게임 설명, SCP의 자체 용어 정의다. 생물과 재료 어휘는 Smithsonian·OpenStax·사전 출판사, 숭고·비체는 Tate의 용어 설명으로 보완했다. 출판사 소개만 읽은 《The Age of Lovecraft》는 관련 비평의 존재를 확인하는 데 사용했으며 개별 장의 논증으로 인용하지 않는다. 《The Ballad of Black Tom》의 지정 출판사 URL은 현재 ‘더 이상 이용할 수 없음’을 반환해 작품 내용의 근거에서 제외했다.

직접 가져오기에 실패한 여섯 출처는 웹 도구의 본문으로 정의·해당 절을 확인했다. 반대로 Cambridge·Tate는 직접 읽기는 성공하고 웹 도구는 403을 반환했다. 접근 수단별 성공 여부를 분리했으며 실패 응답을 본문 확인으로 세지 않았다. 원문 전체와 사이트 이미지는 이 폴더에 복제하지 않았다. 원문 임시 캐시는 재생성에 필요하지 않다.

## 기존 소스에서 확인한 상황

기준 시점의 `photo_cosmic_horror_semantics_20261021.json`에는 180개 카드, `photo_cosmic_relation_semantics_20261021.json`에는 24개 관계 변형이 있었다. 대응 후보·binding 모듈이 authored manifest에 들어 있다. 새 연구의 84개 카드는 그 개수에 합산할 신규 카드 수가 아니다.

이번 카드의 분류는 재사용 7, 정교화 28, 신규 제안 22, 문맥 유지 21, 보류 6이다. 가시 후보 초안은 앞의 세 분류에 해당하는 57개이며 의미 카드와 중첩된다. 기존 의미 카드 80개와 대응 후보 원본 79개를 전체 record·binding·해시와 함께 저장했다. C028은 의미 레지스트리에는 있지만 이번 card_id 직접 매핑에서 후보를 찾지 못했다. 이것은 코퍼스 전체에 변형 의미가 없다는 증거가 아니다.

현재 후보 모듈의 지정 primary field 전체를 대상으로 한 어휘 진단은 [CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json)에 있다. 정확한 substring 부재는 별칭·관계 표현·간접 의미의 부재를 뜻하지 않으며, 일치 역시 후보 적합성을 뜻하지 않는다. 조사 중 다른 작업의 소스 변경이 관찰됐으므로 숫자는 해당 파일의 hash에 묶인 snapshot으로만 사용한다. 실제 검색 성능이나 활성 설치본은 별도 검증 대상이다.

### 우선 수정할 데이터 품질

| 근거 사례 | 확인한 문제 또는 한계 | 반영 제안 |
|---|---|---|
| C126 | 영어는 시연자·장치·관중 및 향하는 관계를 서술하지만 한국어는 제목·주의문 중심이다 | 세 소유자와 두 관계를 양쪽 언어에 모두 명시 |
| C119 | 영어에 촉수 머리·비늘 몸·길고 좁은 날개가 있지만 한국어에 해당 형태가 빠진다 | R22의 우상과 R23의 점토 부조를 별개 실현으로 검토 |
| C169 | 영어의 소켓 3개·케이블 2개·장치 2개가 한국어에 보존되지 않는다 | R39처럼 케이블마다 양끝·장치 소유자를 따로 쓰기 |
| C173 | `boundary between adult`는 경계의 다른 쪽을 직접 명명하지 않는다 | 참가자·집단·간격 두 끝을 명시한 완전 관계로 재서술 |
| C174 | `local_field differs between document_a`만으로 비교의 두 문서·두 필드가 드러나지 않는다 | R09처럼 같은 ID와 서로 다른 두 필드를 완전한 명제로 쓰기 |
| C120/C170 | 전신의 오중 수량과 한 시점의 가시성이 별개다 | R24 전체 수량과 R25 국소 분기를 다른 계약으로 검토. 가려진 수량은 통과 금지 |
| C104/C169 | 금속 원통과 투명 뇌 병이 혼동될 수 있다 | 정본 외관 R39와 창작 변형 R40에 별도 판본·주장 한계 |

위 내용은 저장된 source text의 직접 비교다. 실제 번역 검색 실패·렌더 실패·엔진 결함이 재현됐다는 주장은 아니다. 원본은 [existing-source-mapping.json](existing-source-mapping.json)에서 확인할 수 있다.

## 분야별 조사 결과

### 1. 장르·철학을 장면에 연결하는 방법

코스미시즘·우주의 무관심·인간중심주의 해체는 관점이며 촉수·암흑·악의·허무주의와 동의어가 아니다. 저자의 에세이는 발현하는 매체, 반응, 주어진 조건에서의 결과를 구분하므로, 추상어를 하나의 고정 외형으로 바꾸기보다 **선택한 상황에서 무엇이 누구에게 어떤 관계로 보이는지**를 작성하는 근거로 삼는다. [Notes on Writing Weird Fiction](https://www.hplovecraft.com/writings/texts/essays/nwwf.aspx), [Chaosium의 신화 소개](https://cthulhuwiki.chaosium.com/the-mythos/)

R01은 같은 바닥에서 사람과 석문을 비교한다. R02는 생물의 눈이 작은 배 대신 다른 생태를 향하게 한다. 전자는 크기 관계, 후자는 방향 관계만 검증한다. 무관심·두려움·인간의 무가치함을 픽셀 사실로 판정하지 않는다. 사람 없는 요청에는 기존 C178의 비인간 기준물도 재사용할 수 있다. 장르명 하나가 매번 사람을 생성하게 해서는 안 된다.

### 2. 지식과 기록이 만드는 공포

신규 보강은 기록물이 장식으로 머무르지 않도록 한다. R06은 점토 부조와 종이 스케치의 대응 표식, R08은 회화와 사진의 동일 포즈·배경, R09는 같은 사건 ID와 다른 날짜, R10은 두 종이 위 필적의 국소 대응, R11은 독립된 두 침대-탁자-스케치 묶음이다. [크툴루의 부름](https://www.hplovecraft.com/writings/texts/fiction/cc.aspx), [픽맨의 모델](https://www.hplovecraft.com/writings/texts/fiction/pm.aspx), [시간의 그림자](https://www.hplovecraft.com/writings/texts/fiction/sot.aspx)

각 대응에는 최소 두 매체와 비교 가능한 국소 표식이 필요하다. 닮은 두 그림만으로는 독립된 꿈·실제 사진·시간 이동·저자 동일성을 입증할 수 없다. 글자를 요구한 후보는 원본 해상도에서 실제로 읽혀야 한다. 정확한 글자가 핵심이 아닌 요청에는 R06/R08처럼 형태 표식을 선택할 수 있지만, 이미 선택한 정확한 날짜 의무를 임의의 그림으로 대체해서는 안 된다.

집착·정신 붕괴·자아 해체·정신 교환은 K03에, 액자서사·지연 폭로·제한 시점·회복 없는 생존은 K04에 보존했다. 여러 액자를 그리면 액자서사가 되거나, 특정 표정으로 의학적 상태가 증명되는 것은 아니다. SAN도 실제 정신질환을 모형화하는 장치가 아니라는 게임 제작사의 설명을 따른다. [Chaosium SAN Q&A](https://www.chaosium.com/blogfrom-the-qa-what-is-the-sanity-san-mechanic-in-call-of-cthulhu/)

### 3. 공간·깊은 시간·장소

R03의 덮인 지층, R15의 사람이 엎드려야 하는 통로, R16의 얼음-석벽 경계는 몸 비례와 겹침을 보여준다. 수억 년·인류 이전·봉인 기간을 사진만으로 입증하지 않는다. R17의 수중성은 수면·입자·기포·물체의 관계에 두며 청록색 보정과 구분한다. [광기의 산맥](https://www.hplovecraft.com/writings/texts/fiction/mm.aspx), [이름 없는 도시](https://www.hplovecraft.com/writings/texts/fiction/nc.aspx)

비유클리드 기하·고차원 설정·불가능 도형·더치 앵글·광각 왜곡은 따로 다룬다. 실제 구면·쌍곡 기하는 평행선 공준과 관련된 수학이며 논리 오류가 아니다. R19는 네 연결부가 모두 드러나는 불가능 계단의 선택 실현이고, R20은 창과 문 너머의 상충하는 공간, R21은 온전한 벽과 부속지의 접점이다. 어느 것도 고차원 물리의 실증은 아니다. [기하 강의 개요](https://www.math.brown.edu/bhassett/teaching/366spring03/366advert.html), [마녀집의 꿈](https://www.hplovecraft.com/writings/texts/fiction/dwh.aspx), [에리히 잔의 음악](https://www.hplovecraft.com/writings/texts/fiction/mez.aspx)

지명별 소품 묶음도 고정하지 않는다. 인스머스의 항구 생활 동선은 R12, 아름다운 꿈의 도시는 R13, 체임버스의 호수·두 태양·검은 별 도상은 R14다. 드림랜드를 항상 어둡고 황폐하게 만들거나 렝을 단일 지도에 고정하지 않는다. 카르코사 도상의 검은 별을 블랙홀의 과학 시각화로 취급하지 않는다. [카다스](https://www.hplovecraft.com/writings/texts/fiction/dq.aspx), [The King in Yellow](https://www.gutenberg.org/cache/epub/8492/pg8492-images.html)

### 4. 이름보다 먼저 보존할 생물 구조

| 대상 | 선택해서 보여줄 요소 | 구분해야 할 것 |
|---|---|---|
| 크툴루 우상 R22 | 작은 입체상·촉수 머리·비늘 몸·길고 좁은 등 날개 | 점토 부조 R23의 rudimentary wings, 실제 본체, 후대 조형 |
| 엘더 싱 R24/R25 | 통 몸통·오중 능선·별 모양 상부 기관, 한 줄기의 다섯 분기 | Elder Gods, 일반 불가사리 얼굴, 가려진 뒷면 수량 |
| 쇼고스 R26 | 연속 덩어리와 표면에 박힌 눈, 같은 몸의 돌출부 | 여러 개체, 떠 있는 눈, 시간적 생성·소멸 |
| 미고 R27 | 갑각 유사 몸·관절 부위·등 막날개·더듬이 타원체 머리 | 필수 버섯갓, 인간 머리, fungal 명칭만으로 생물 동정 |
| 딥 원 R28 | 몸 비늘·목의 아가미 같은 틈·손가락 사이 막 | 인간의 인종·얼굴·계급으로 판정하는 혈통과 퇴화 |
| 이스 점유 몸 R29 | 원뿔 몸과 네 뿌리, 두 집게와 다른 말단 | 네 개의 동일 머리 또는 인간형, 정신 교환의 입증 |
| 나이트건트 R30 | 빛 아래 드러난 매끈한 앞면·뿔·목·날개 접점 | 가면·등 돌린 얼굴·암부, 전신의 모든 정본 세부 |

이 표의 범위는 해당 작품의 국소 구조와 선택형 실현이다. 어떤 사진도 이 표의 모든 생물을 한꺼번에 요구하지 않는다. [광기의 산맥](https://www.hplovecraft.com/writings/texts/fiction/mm.aspx), [어둠 속의 속삭임](https://www.hplovecraft.com/writings/texts/fiction/wid.aspx), [인스머스의 그림자](https://www.hplovecraft.com/writings/texts/fiction/soi.aspx), [시간의 그림자](https://www.hplovecraft.com/writings/texts/fiction/sot.aspx), [카다스](https://www.hplovecraft.com/writings/texts/fiction/dq.aspx)

신격 이름에는 생물처럼 확정된 표준 도해가 없는 경우가 많다. 아자토스의 꿈 우주 등식, 슈브 니구라스의 고정 염소 몸, 하스터=황색의 왕, 다곤/히드라의 보편 해부학은 그대로 승인하지 않았다. K08–K11은 원전·저자·후대 RPG의 판본을 구분한다. 특히 아자토스 시의 꿈·피리·우주 법칙 이미지는 널리 유통되는 각성 시 우주 소멸의 정설을 직접 명시하지 않는다. [Fungi from Yuggoth XXII](https://www.hplovecraft.com/writings/texts/poetry/p289.aspx)

### 5. 표면과 물성 어휘

비늘(squamous)과 주름(rugose)은 서로 다른 국소 구조다. R34는 같은 몸의 이웃 영역에서 구별하도록 설계했다. R33은 균사체와 물체의 접점을 보여주며 버섯갓·발광·독성을 자동으로 붙이지 않는다. R35는 촉수의 뿌리와 말단을 확인하되 흡반·대상 감기·성적 행위를 촉수의 기본 의미로 만들지 않는다. 실제 두족류도 팔·촉수·흡반의 배열이 생물별로 다르다. [squamous](https://www.merriam-webster.com/dictionary/squamous), [rugose](https://ahdictionary.com/word/search.html?q=rugose), [OpenStax 균류](https://openstax.org/books/biology-2e/pages/24-1-characteristics-of-fungi), [Smithsonian 두족류](https://ocean.si.edu/ocean-life/invertebrates/octopuses-squids-and-relatives)

R36은 표면 하이라이트·내부 입자·지지면 변형을 구분한다. ‘gelatinous’의 느낌이 실제 점성계수·살아 있는 원형질·특정 세포 구성을 입증하지 않는다. Ichor에도 검정·점성·독성은 필수 뜻으로 들어 있지 않으므로 R45의 금색 액체는 명시적인 창작 선택으로 기록했다. 소유자의 틈→액체→받침의 연속성이 색보다 먼저다. [ichor](https://dictionary.cambridge.org/us/dictionary/english/ichor)

색 역시 물체 고유색·표면 반사·광원·받은 빛·전체 보정으로 나눠야 한다. 「우주에서 온 색채」에 자홍색을 고정하거나 자홍색이 가시역 밖 색을 물리적으로 재현한다고 주장하지 않는다. Fetid·gibbering·ululation은 후각/오디오 문맥으로 보존하고 녹색 안개나 열린 입을 해당 감각의 픽셀 PASS로 삼지 않는다. [fetid](https://www.merriam-webster.com/dictionary/fetid), [ululation](https://www.merriam-webster.com/dictionary/ululation)

### 6. 금서·유물·표식의 구체 구조

네크로노미콘은 실제 오컬트 문헌이 아니라 작가가 만든 가공 저자·번역·출판사를 갖춘 서사 장치다. R46은 본문과 주석의 다른 문자 영역, R47은 별개의 책과 각 서지 카드의 대응을 제안한다. 아랍 문자처럼 보이는 글자·낡은 가죽·해골 표지가 정본 진품을 뜻하지 않는다. 다른 금서들의 최초 작가·최초 작품·판본은 별도 미해결 조사로 남겼다. [History of the Necronomicon](https://www.hplovecraft.com/writings/texts/fiction/hn.aspx), [작가 편지](https://www.hplovecraft.com/creation/necron/letters.aspx)

R39의 뇌 원통은 닫힌 금속 외피, 삼각 배열 소켓 3개, 두 케이블과 두 장치다. 내부 뇌가 보이지 않는 것이 원전 외관과 충돌하지 않는다. R40의 투명 용기와 보이는 뇌는 창작 변형으로 분리한다. ‘disembodied consciousness’의 의식·생존·통신 기능은 두 실현 모두에서 사진만으로 증명되지 않는다. [어둠 속의 속삭임](https://www.hplovecraft.com/writings/texts/fiction/wid.aspx)

R48은 거의 검고 붉은 줄이 있는 불규칙 다면체, 중앙 금속 띠, 상자 벽까지 이어지는 일곱 지지대, 바닥에서 뜬 간격을 포함한다. 면 개수를 명칭에서 추론하지 않는다. 일곱 지지대의 양끝이 가려지면 수량과 연결 전체는 미판정이다. 원전 물건의 발광·예지·소환 효능은 구조와 별개다. [The Haunter of the Dark](https://www.hplovecraft.com/writings/texts/fiction/hd.aspx)

R49의 가지형 표식은 편지를 소개한 아카이브 설명에 근거한 도식 제안이다. 도판을 정밀 계측하지 않았으므로 획수·각도·정확한 복제를 승인하지 않는다. R50은 체임버스의 검은 잠금 장신구와 외투의 부착을 보존하며 후대 삼지 문양을 필수로 두지 않는다. [Elder Sign 설명](https://www.hplovecraft.com/life/myths.aspx), [체임버스 원전](https://www.gutenberg.org/cache/epub/8492/pg8492-images.html)

### 7. 의례·폭력·성·생식 용어

참조 대화의 관련 용어 13개와 신체·죽음·폭력 17개를 누락하지 않고 경로에 남겼다. 나체·접촉·집단 배치·인신공희·희생 거래·종말론적 믿음은 같은 뜻이 아니다. R52–R55는 선·물건·참가자·석대·예복의 배치라는 선택 가능한 부분만 작성하고 동의·신앙·성행위·소환 성공은 독립 문맥으로 둔다.

식인·시체 섭식·유골·인간 가축·해부 표본도 구분했다. 뼈더미는 사육이나 식인을 입증하지 않고, 시신 곁에 있다는 사실은 시체성애를 입증하지 않는다. 《The Loved Dead》는 C. M. Eddy Jr.와 러브크래프트의 협업·개작 맥락으로 기록했다. [The Loved Dead](https://www.hplovecraft.com/writings/texts/fiction/ld.aspx), [벽 속의 쥐](https://www.hplovecraft.com/writings/texts/fiction/rw.aspx)

이종 생식·혼종·근친상간·근친교배·생식 강요·괴물적 탄생은 다른 주장이다. 라비니아 임신의 구체적 성행위와 동의를 원전의 명시 사실로 확정하지 않는다. 인스머스의 가정 강압은 폭력적 권력 장악 뒤 특정 가정이 손님을 받아야 한다는 증언의 문맥으로 기록하되 사진만으로 가해·동의를 판정하지 않는다. [던위치의 공포](https://www.hplovecraft.com/writings/texts/fiction/dh.aspx), [인스머스의 그림자](https://www.hplovecraft.com/writings/texts/fiction/soi.aspx)

원전의 인종주의·우생학적 퇴화 관점은 문학사적 맥락으로 남기며 중립적인 사람 외형 분류로 재사용하지 않는다. Monstrous-Feminine과 퀴어·페미니즘 재해석은 이론 원저 및 작품 전문 검토가 필요한 보류 항목이다. 원전의 괴물을 무조건 적대로 만들지 않도록 R38의 돌봄 관계를 대안으로 작성했지만 이를 실제 공생의 과학적 입증이나 특정 현대 작품의 재현이라고 부르지 않는다.

## 자료가 반영되는 단위

데이터 단위는 `요청 전체 문맥 → 의미/판본 → 선택한 가시 실현 → 소유자 → 방향 관계 → 혼동 경계 → 픽셀 판정`이다. 예를 들어 ‘뇌 원통’에서 바로 유리 뇌 병을 검색·채택하지 않고, 원전 금속 외관인지 창작 변형인지 먼저 구분한다. 선택 후에만 그 실현의 전체 부품·소켓·케이블 연결 의무를 전달한다.

84개 카드와 57개 초안의 JSON은 운영 importer 형식이 아닌 research schema다. 슬롯은 현재 catalog에 존재하는 이름으로만 제안했지만 슬롯 일치가 role approval이나 수정 권한은 아니다. `reuse`도 그대로 복사한다는 뜻이 아니라 완전 소스 검토 후 기존 CID를 유지할지 결정하는 우선 제안이다. 변경된 문장·조건·효과는 새 qualification과 필요 시 인덱스 갱신을 요구한다.

## 검증과 남은 경계

구조 검사는 185개 경로의 누락·중복, 84개 카드의 source/owner/관계 참조, 57개 초안의 연구 전용 상태, 현 catalog 슬롯, 기존 record 해시, 80개 평가 사례/160개 한영 입력의 참조, 비가시 문맥의 후보 전환 차단을 확인한다. 일부러 손상시킨 참조·관계·권한·PASS 주장을 거부하는 mutation 검사도 포함한다. 이것은 의미 번역의 완벽함·검색 성능·미술적 품질을 자동 증명하지 않는다.

[EVALUATION-CASES.tsv](EVALUATION-CASES.tsv)의 양성 30·경계 26·일반 12·비가시/미해결 12사례는 모두 NOT_RUN이다. [PIXEL-PLAN.md](PIXEL-PLAN.md)의 최초 12사례×3안=36장도 미실행이다. 일부분이나 가림은 `UNOBSERVABLE_NOT_PASS`, 전체 사례는 `partial_is_fail`을 적용한다. 거부·오류로 이미지가 없으면 `BLOCKED_UNSCORED`로 남긴다.

미해결 서지·이론 항목과 도판 검증은 [ACCESS-LIMITS.md](ACCESS-LIMITS.md)에, 구체적인 적용 순서·대상 파일·완료 기준·되돌리기 방식은 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 있다.
