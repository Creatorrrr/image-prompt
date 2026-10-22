# 다크 판타지·그림다크 시각 의미와 후보 데이터 보강 리서치

조사일: 2026-10-22, Asia/Seoul. **연구·설계 산출물이며 운영 데이터 등록·임베딩·이미지 생성·활성화는 수행하지 않았다.**

## 결론

필요한 보강은 장르 형용사의 수보다 **장소·사물·신체의 성분과 소유 관계, 권력과 대가의 가시 정황, 비가시 의미의 판정 한계**에 있다. 다크 판타지와 그림다크를 검은 갑옷·성당·유혈의 한 묶음으로 학습시키면 장르 이해가 좋아지기보다 요청과 무관한 세부가 늘어날 수 있다.

이번에는 원 대화의 용어 247개 전부를 추적하고, 시각 의미 카드 72개, 한영 후보 초안 68개, 출처 46개, 한영 개발 평가 56개를 정리했다. 68개 초안은 32개 still·33개 proxy·3개 versioned 카드와 같은 집합이며 별도 신규 후보 68개를 추가 채택했다는 뜻이 아니다. 나머지 4개 카드는 문맥의 의미 경계를 위한 자료다.

원 용어의 분류는 still 27, proxy 65, versioned 15, advisory 36, context 82, sequence 20, nonvisual 2다. 이는 연구자가 정한 처리 경로이며 장르의 객관적 분할이나 단어 자체의 유일한 실현법이 아니다. 예컨대 psychopomp는 문맥적 안내자 개념이지만, 그 선택 실현으로 문 앞에서 방향을 안내하는 관계를 제안할 수 있다.

## 조사 범위와 근거

[참조 대화](https://chatgpt.com/c/6ad8d93d-e51c-83ec-96a0-2aafa7512902)의 16개 용어 표 247행과 조합 예시 7행을 확인했다. 대화 도구의 본문은 20,000자에서 잘렸으므로 같은 대화의 로그인된 브라우저에서 뒤쪽 표와 마지막 항목 Forsaken까지 읽어 복원했다. 대화의 설명은 조사 입력이고 기존 인용번호는 새 연구의 검증 근거로 전용하지 않았다.

자료는 장르 작가·편집진, 대학·도서관, 미술관·문화유산 기관, 공식 사전, 당사자 단체와 국제기구의 정의 자료를 우선했다. [SOURCES.tsv](SOURCES.tsv)에 실제 읽은 범위와 접근 수준을 기록했다. 출처에서 확인한 정의와 아래에서 저술한 장면은 별개다. 예를 들어 미술관의 reliquary 설명은 ‘성유물과 용기는 다르다’는 구분을 지지하지만 O01의 창·뼈·금속함 배치가 우수한 생성 프롬프트임을 입증하지 않는다.

247개 개별 정의를 각각 독립 사전에서 재검증한 것은 아니다. 출처는 개념군과 주요 혼동 경계를 지지한다. 특히 oubliette의 개별 역사 사례, Goetia의 문헌/판본, abjection의 원전 이론, 일부 팬덤 장르명의 범위는 후속 조사 항목으로 명시한다. 역사적·의학적·법적 분류를 생성 이미지 외형에 부여하지 않는다.

## 1. 장르·정서와 구체적인 실현을 분리

Cambridge의 공개 요약은 dark fantasy의 용례 자체가 논쟁적이었음을 보여 준다. 이를 단일한 엄격 분류로 고정하지 않는다. Grimdark Magazine 편집진은 회색 도덕의 세계에서도 희망과 저항이 가능하다고 설명한다. [Cambridge](https://www.cambridge.org/core/books/abs/cambridge-companion-to-fantasy-literature/dark-fantasy-and-paranormal-romance/C693AFBD63366C6C17DAB48A53372918), [Grimdark Magazine](https://www.grimdarkmagazine.com/defining-grimdark-fantasy-and-sf-moving-to-an-inclusive-future/)

이에 따라 `dark fantasy`, `grimdark`, `Gothic`, `eldritch` 같은 라벨은 특정 팔레트·성별·상해·종족·건물을 자동 생성하는 스위치가 되지 않아야 한다. `Gothic`은 문학 장르, 건축/미술사, 갑옷, 현대 고스 복식의 문맥이 서로 다르다. 머리색·레이스 드레스를 고딕 서사의 대체 증거로 취급하지 않는다. British Library의 설명 역시 고딕을 단일 요소의 상자가 아닌 겹치는 특징의 가족으로 다룬다. [British Library](https://www.britishlibrary.cn/en/articles/gothic-motifs/)

| 보강할 축 | 표현 가능한 것 | 자동 확정하면 안 되는 것 | 연구 카드 |
|---|---|---|---|
| 두려움 | 문턱, 가림, 두 인물의 시선과 거리 | 악의·미래 사건·관객의 공포 | F11 |
| 숭고 | 같은 지면의 작은 비교자와 거대 구조 | 절대 치수·경외라는 감정 | D13~14 |
| 누미노스 | 인물과 떨어진 빛의 배치 | 실제 신성·신격화 | F07 |
| 퇴폐·몰락 | 권위 사물과 손상의 동시 노출 | 제도 부패·쇠망의 역사 | O09, R01 |
| 그림다크의 대가 | 승리 표지와 파괴·부축의 병치 | 승리의 가치·회복 불가능성 | R08 |
| 희망·저항 | 괴물의 외형과 차폐/도움의 관계 | 정체성의 악함·완결된 구원 | R07 |

작가 Abercrombie의 grit 논의는 거친 생활감과 윤리적 복잡성을 함께 다룬다. 후보 데이터에서는 장비의 수리, 노동과 보급, 제도의 자원 접근 같은 세부를 강화하고, `gritty → grain/진흙/성폭력`의 고정 치환을 피한다. [The Value of Grit](https://joeabercrombie.com/the-value-of-grit/)

## 2. 장소는 구조·기능·관계로 세분화

묘지 계열은 색감보다 공간 구조가 구별력을 준다. `crypt`의 건물 아래 위치, `catacomb`의 매장 감실과 연결 통로, `ossuary`의 유골 보관, `mausoleum`의 기념 묘 건축을 각각 다룬다. Paris Catacombs는 실제 납골장 사례지만 모든 지하 매장 공간이 동일한 역사·구조를 가진다는 근거는 아니다. [Catacombes de Paris](https://www.catacombes.paris.fr/en/history/ossuary)

| 개념 | 핵심 소유자·관계 | 가까운 오답 | 처리 |
|---|---|---|---|
| Necropolis | 여러 묘 건축과 그 사이의 보행 통로 | 돌집이 많은 일반 마을 | D01 |
| Crypt | 상부 건물 바닥/하부 묘실/연결 계단 | 단순 지하실 | D02; 실제 열린 시야나 모형 여부 명시 |
| Catacomb | 벽 매장 감실/통로/갈림 | 일반 광산 | D03; 감실형은 하나의 저술한 대안 |
| Ossuary | 유골/경계 있는 보관 공간 | 돌무더기·단순 해골 문양 | D04 |
| Charnel house | 독립 건물/입구/내부 보관대 | 평범한 창고 | D05; 기능은 문맥 |
| Sarcophagus | 돌관 몸체/맞는 돌뚜껑/이음 | 제단·목관 | D06 |
| Oubliette | 깊은 방/상부 개구부/접근 수단 | 수조·채광정 | D08; 역사 기능은 추가 확인 |
| 폐수도원 | 회랑/붕괴/생활 사물 | 공사 중인 건물 | D09; 버려진 기간은 미입증 |
| 모독된 성당 | 성소/제단/훼손 대상 | 지진·수리의 손상 | D10; 모독 의도는 문맥 |
| 저주받은 숲 | 인간 길/뿌리/표지의 관계 | 일반 울창한 숲 | D11; 길 이동·저주는 서사 |
| 역병 도시 | 경계/자원/기다리는 사람 | 관문·축제 대기열 | D12; 병원체·기근은 미입증 |

같은 표제의 반복 생성보다 **새 관계가 기존 후보에 없는지**를 먼저 본다. D01의 ‘묘 건축 사이 도시 통로’와 D04의 ‘뼈의 보관 배열’은 가까운 장르적 소재여도 서로 대체할 수 없다.

## 3. 사물은 용기·내용물·지지체·접점으로 분해

성유물과 성유물함은 각각 내용물과 용기다. 실제 미술관 자료에는 신체 모양 용기와 다양한 재질이 있지만 그 외형으로 기적이나 사령술을 확정할 수 없다. 향로도 용기만이 아니라 사슬의 양끝과 연기의 출발점이 중요하다. [Met의 성유물·성유물함 연구](https://www.metmuseum.org/essays/relics-and-reliquaries-in-medieval-christianity)

O01은 `유물 → 창을 통해 보임 → 용기`, O02는 `신체형 금속 용기 → 받침`, O03은 `손 → 위 고리 → 각 사슬 → 향로`, `연기 → 향로에서 출발`로 구분했다. 선택하지 않은 대안의 유물·재질·행동을 함께 요구하지 않는다. 세 사슬을 선언한 O03을 실제 반영할 때는 각 사슬의 양끝 또는 정확히 선언된 멤버 집합을 검토해야 한다.

가고일은 괴물 모양만으로 충분하지 않다. 건축 배수 기능과 장식 grotesque의 구분이 있어 O04는 입의 출수구와 벽 바깥으로 떨어지는 물길을 같은 시야에 둔다. 배수 없는 조각 요청에 물을 자동 추가하면 안 된다. [Historic England](https://heritagecalling.com/2018/10/26/a-brief-introduction-to-gargoyles/)

마도서는 책·페이지·도식·문자를 분리한다. ‘금단’과 ‘영혼을 손상하는 지식’은 문맥으로 남긴다. `sigil`, `seal`, `ward`는 기호, 물리적 봉함, 허구 차단막의 용례를 나눈다. 실제 문헌의 기호를 읽지 않은 상태에서 특정 고에티아 인장이나 권능으로 합성하지 않는다. [Grimoire](https://www.merriam-webster.com/dictionary/grimoire), [Sigil](https://www.merriam-webster.com/dictionary/sigil)

## 4. 마법과 괴물은 외형·작동·원전을 별도 층위로

Necromancy의 망자 교섭/점술 용례와 현대 판타지의 부활·조종은 구분한다. M01은 의식자와 특정 환영의 위치를 제안할 뿐 실제 대화·사망·소생 성공을 입증하지 않는다. M02~04는 매개에서 대상까지 경로, 영혼 연결의 양끝, 허구 경계의 접촉을 각각 분리했다. [Necromancy](https://www.merriam-webster.com/dictionary/necromancy)

Wight의 일반 어휘사, draugr의 사가 맥락, lich의 판본 규칙은 같은 ‘언데드 외형’으로 합치지 않는다. 특히 R10이 참조하는 D&D의 영혼함·재생은 2014 legacy 자료의 설정이다. 다른 판본이나 독자 세계관 리치에 자동 추가하지 않는다. Psychopomp 역시 안내 역할이며 살해자·심판자와 별개다. [Wight](https://www.merriam-webster.com/dictionary/wight), [Notre Dame의 draugr 논의](https://sites.nd.edu/manuscript-studies/tag/draugr/), [D&D 2014 Lich](https://www.dndbeyond.com/monsters/16943-lich), [Psychopomp](https://www.merriam-webster.com/dictionary/psychopomp)

관계 후보를 강화할 때 `body fusion`은 두 몸의 연속 조직 경계, `living armor`의 생체형 대안은 판 안쪽에서 같은 착용자 피부까지의 접점, `living architecture`는 석재에서 유기 내피로의 연결을 요구한다. 단순 겹침·담쟁이·갑옷 장식은 대체가 아니다. 생명·의식·영양 공유·기생의 생태 기능은 형태와 별도로 남긴다. 기존 바이오펑크 자료의 세포/기능 주장 한계를 보존한다. [BFI의 body horror 논의](https://www.bfi.org.uk/lists/10-great-body-horror-films)

## 5. 상징·빛·재질은 서로 다른 축

| 혼동쌍 | 데이터에서 분리할 것 | 카드 |
|---|---|---|
| Memento mori / Vanitas | 죽음 상기 vs 성취와 유한성의 병치 | O08 / O09 |
| Danse macabre / undead | 계층을 넘는 죽음의 알레고리 vs 생물/존재 설정 | O10 / R11 |
| Chiaroscuro / Tenebrism | 형태를 만드는 명암 vs 어둠이 지배하는 화면의 국소 빛 | F01 / F02 |
| Patina / Verdigris / iron rust | 넓은 표면층 vs 구리계 녹색 변화 vs 철 부식 | F03; chemistry unknown |
| Broken halo / occultation | 양쪽 끊긴 끝과 실제 틈 vs 머리카락에 가린 정상 고리 | O12 |
| Solar eclipse / red Moon | 태양 원반 가림 vs 달의 붉은 외형/월식 | F06은 후자; 별도 분기 필요 |
| Grit / grain | 삶·물성의 거침 vs 사진 입자 | R05와 매체 슬롯 별도 |
| Crepuscular / sinister | 박명의 빛/시간 vs 위협의 해석 | F05 / F11 |
| Putrescent / fetid | 부패 외형 vs 냄새 | 후자는 픽셀 PASS 없음 |
| Visceral / viscera | 본능적 강렬함 vs 내장이라는 해부 의미 | 자동 해부 확장 금지 |

위 구분은 [Science Museum](https://www.sciencemuseum.org.uk/objects-and-stories/memento-mori), [National Gallery의 vanitas](https://www.nationalgallery.org.uk/paintings/glossary/vanitas), [chiaroscuro](https://www.nationalgallery.org.uk/paintings/glossary/chiaroscuro), [tenebrism](https://www.nationalgallery.org.uk/paintings/glossary/tenebrism), [CCI 금속 보존 자료](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html), [NASA 월식 설명](https://science.nasa.gov/moon/eclipses/)의 정의·물성 맥락을 바탕으로 정리했다. 구체적인 소품 배열과 빛의 실현은 연구자의 제안이다.

## 6. 권력·폭력·성적 금기도 추적 범위 유지

원 대화의 성적 금기·폭력 36개 항목도 atlas에 모두 남겼다. 성적 관련 표 19개, 폭력 표 17개다. 이 항목들을 모호한 ‘어두운 분위기’ 하나로 희석하지 않는다. 동시에 **형태·사건·원인·의도·제도·동의·쾌락·혈연·생사를 서로 다른 의미**로 다룬다.

R02의 장부·잠긴 곡물·노동자·서기는 자원 접근의 정황을 보여줄 수 있지만 농노제·노예제·채무예속의 차이를 대체하지 못한다. ILO도 관련 개념들을 동일한 것으로 다루지 않는다. [ILO](https://www.ilo.org/resource/article/meanings-forced-labour)

X01~04는 옷 입은 성인의 시선·근접, 장갑의 재질/봉제, 제의적 군중, 혼례 정황의 선택형 후보다. 욕망·성적 행위·동의·강압을 외형으로 자동 판정하지 않는다. X05~08은 고문/BDSM/성폭력, 친족/시체/동물의 분류, 생식 통제/허구 성마법, 관계/복수의 시간 축을 각각 명시 문맥으로 남긴다. 이 네 카드는 시각 후보로 변환하지 않았다.

NCSF의 자료에서 명시적 사전 합의와 철회 가능성은 의상이나 몸짓으로 대체되지 않는다. UNFPA의 생식 강요 정의도 임신 외형보다 자율성 침해에 관한 것이다. 그러므로 collar·눈물·닮은 얼굴·장례·동물형 실루엣만으로 합의, 피해, 혈연, 시체 대상 욕망, 실제 동물과의 관계를 확정하지 않는다. [NCSF PDF](https://ncsfreedom.org/wp-content/uploads/2022/01/Best-Practices-for-Consent-to-Kink.pdf), [UNFPA](https://www.unfpa.org/swp2022/risk)

성적 장르도 한 스펙트럼으로 뭉개지 않는다. Erotic horror의 친밀감/위협, dark romance의 연애 중심 서사, psychosexual horror의 갈등, fetish aesthetic의 외형은 별도 경로다. BFI의 사례 논의는 암시·의상도 표현 재료가 될 수 있음을 보여주며 특정 노출/행위를 필수화하는 근거가 아니다. [BFI](https://www.bfi.org.uk/lists/10-great-erotic-horror-films)

## 7. 현재 데이터와의 비교에서 드러난 구체적 보강점

별도 [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)에 CID와 검토 내용을 기록했다. 조사 스냅샷은 후보 19,006개, binding 12,879개, manifest 모듈 49개다. 고정한 7개 field 계열의 어휘 진단에서는 247개 중 169개가 매칭 0이었다. 이는 **169개 의미의 부재·검색 실패·신규 후보 필요를 뜻하지 않는다.** aliases/다른 사실 필드·한영 변형과 실제 검색은 이 진단에 포함되지 않았다.

특히 `crypt` 부분 문자열의 세 hit는 `encrypted` 계열이었다. 반대로 `living armor`는 hit가 있어도 빈 갑옷의 자율 동작 프로파일이어서 생체 갑옷의 피부 접점과 의미가 달랐다. 유사어를 늘리는 것만으로 해결할 수 없는 차이다.

따라서 우선순위는 다음과 같다.

1. **P0의 구조와 관계:** 묘역/묘실/보관의 구분, 성유물과 용기, 향로 연결, 배수 관계, 상대 규모, 빛과 형태, 갑옷/생체/건축 접점.
2. **P0의 의미 경계:** 장르 자동 의무 금지, 명시된 기존 owner/락 보존, 동의·원인·역사·생사·후각·시간에 대한 비추론.
3. **P1의 장면 다양성:** 제도와 보급, 승리의 대가, 수호와 돌봄, 문턱/그림자/시선의 관계, 여러 장소·재질·카메라 거리 대안.
4. **후속 원전 조사:** 역사 기능이나 이론 정의가 아직 약한 항목, 판본별 괴물/마법의 분기. 불확실한 정의를 데이터 수로 메우지 않는다.

현재 카드의 P0/P1은 연구 순서다. 최종 CID 수와 역할 승인은 전체 소스·기존 의무·실제 효과를 검토한 뒤 결정한다. 새 데이터가 검색·프롬프트·픽셀·장면의 설득력을 개선했는지는 아직 실험하지 않았다.

## 다음 단계

[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)는 재사용 판단, 한영 소스 저술, 소유/효과 검토, 별도 인덱스, 자연어 검색, 대조 이미지, 설치/롤백까지의 완료 조건을 제시한다. [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv)는 NOT_RUN 개발 코호트이고 [PIXEL-PLAN.md](PIXEL-PLAN.md)는 이미지 생성 전 비교 설계다.
