# Gaslamp Fantasy 시각 의미·후보 데이터 상세 조사

2026-10-23 KST. 이 문서는 **조사와 반영 설계의 결과**다. 현재 운영 후보·인덱스·설치본을 개선했다는 실행 보고가 아니다.

## 1. 결론

가장 큰 보강 지점은 황동·안개·고딕 같은 수식어의 수가 아니라 **기능을 가진 물건, 그 물건의 소유자, 연결되는 대상, 한 프레임에 확인할 수 있는 상태**다. 다음 네 층을 함께 설계해야 한다.

1. **형태:** 광원/하우징, 치마 지지/실루엣, 명함/수첩, 사진 면/반사면처럼 실제로 구별되는 성분.
2. **관계:** 허리→걸쇠→체인→도구, 손→판→연필→종이, 전원→리드선→전극→표본의 연결.
3. **문맥:** 시대·계급·직업·법률·종교·동의·성적 경제·신분·생사. 외형의 의미와 관련되지만 외형만으로 확정하지 않는 사실.
4. **검증:** 원문/외부 출처, 기존 source, 의미 카드, 후보 선택, literal prompt, native pixels, 사용자 판단을 별개로 기록.

장르를 통일된 소품 묶음으로 구현하면 밝은 사교 장면·노동·도시 행정·비기계적 마법이 지워진다. 창작자 [Girl Genius FAQ](https://www.girlgeniusonline.com/info/faq.php)는 기계·인공생명·비행선과 과학/마법의 혼합을 직접 설명한다. 따라서 ‘Gaslamp는 마법만, Steampunk는 기계만’이라는 배타적 판정을 데이터 규칙으로 채택하면 안 된다. 이것은 하나의 원작 사례이며 장르 전체의 필수 사양도 아니다.

## 2. 크롬에서 확인한 원문 전체 범위

[참조 대화](https://chatgpt.com/c/6adaf513-0f18-83ee-9cc2-538c6c088add)의 최초 `read_thread`는 20,000자에서 잘렸다. 이후 사용자의 지시에 따라 **로그인된 Google Chrome 앱에서 1~15절의 전체 표와 마지막 문단을 확인했다.** Chrome 확장 연결 대신 native 앱의 렌더링된 접근성 트리를 읽었다. 처음 시도한 인앱 브라우저의 로그인 한계는 Chrome에서 해소됐다.

- **217개 표 행 전체**를 연결했다: 용어 191개, 저술된 제도/산업 설정 10개, 작품 9개, 창작 조합 7개.
- 11절 23행의 성·욕망 항목, 12절 18행의 폭력·제도 항목을 모두 포함한다. Brothel 설명도 복원했다.
- BDSM/합의와 강제, 관음, 근친 금기, 시체성애적 모티프, 생식 공포, 식인, 시체 도굴, 혈마법, 채무 예속, 식민 수탈 등 실제 원문 표제를 확인했다.
- 처음 반환된 Markdown excerpt와 초기 접근 한계는 과거 획득 기록으로 보존한다. 현재 coverage는 **화면의 전체 표 217행**을 뜻하며 숨은 source 팝오버나 모든 출처 페이지를 완독했다는 뜻이 아니다.
- 맨틀·가스 저장조·플랑셰트·페퍼스 고스트 등 원문 표제로 없는 보완 개념과 모든 구체 장면의 저술 provenance는 계속 구분한다.

[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md)에 각 행을 연결했다. `/`로 묶인 표제를 여러 키워드로 부풀리지 않았다. [reference-browser-access.json](reference-browser-access.json), [reference-browser-tail.tsv](reference-browser-tail.tsv), [reference-complete-rows.json](reference-complete-rows.json)이 복원 범위와 정규화 방식을 기록한다. 원문 내용과 각 외부 주장의 독립 검증은 별도다.

## 3. 출처 사용 원칙과 한계

[sources.json](sources.json)에 외부 자료 44건의 URL·기관·읽은 구절·접근 상태·지원 범위를 기록했다. 박물관/도서관/기록관·공식 창작자 설명·연구 초록·선택한 소설 원문을 우선했다.

`body`도 전체 사이트나 모든 도판을 완독했다는 의미가 아니다. 출처별 locator에 적힌 설명/구절을 읽은 범위다. Smithsonian 골상학 모형, 일부 기록관·Auckland 자료는 공식 검색 색인까지만 읽었고 open 오류를 남겼다. Dúchas는 채록 목록만 확인했으며 개별 설화의 규칙은 검증하지 않았다. PDF는 텍스트를 읽었으며 도판 픽셀은 검토하지 않았다. 원문 217행 모두의 정의·작품 설명을 독립 검증한 것도 아니다.

외부 근거는 물건·개념·역사·문학 사례의 범위를 지원한다. 카드에 적힌 정확한 사람 수·손 위치·카메라에서 보이는 배치는 대부분 **저술한 선택적 실현**이다. 실제 역사형을 채택할 때는 지역·연대·소장품을 추가로 고정해야 한다.

## 4. 도시의 빛을 공급 구조로 확장

[National Gas Museum](https://www.nationalgasmuseum.org.uk/discover/gas-lighting/)의 설명을 기준으로 노출 불꽃과 후대 맨틀을 구분한다. [제조 설명](https://www.nationalgasmuseum.org.uk/discover/making-gas-from-coal/)은 조명과 생산 설비를 별도로 연결할 근거다.

| 설계 단위 | 눈에 보여야 할 관계 | 잘못된 대체 | 남는 문맥 |
|---|---|---|---|
| 가스등 G03/G04 | 광원→버너→하우징; 선택 판본별 노출 불꽃/맨틀 | 노란 전구·촛불·석유 심지를 같은 것처럼 처리 | 연료·밝기의 측정값·정확한 연대 |
| 점등원 G05 | 성인→봉→등 개구부의 접점 | 봉을 든 사람만, 끝이 등과 단절 | 직업·점등 전후·순찰 일정 |
| 제조소 G06 | retort→연결 배관→응축기의 기능 관계 | 굴뚝 하나, 일반 보일러 | 실제 공정 작동·연료 조성 |
| 저장/공급 G07 | 저장 용기→공급선→거리 서비스 구역 | 제조소·수압탱크와 합침 | 저장조 세부 구조·실제 압력 |
| 정비 G85 | 작업자→도구→가상 배관의 열린 이음부 | 무작위 톱니·빛만 추가 | 수리 성공·에너지 원천·노동 제도 |

G85는 역사 사실이 아닌 창작용 확장이다. 가스등의 도시가 마법을 다룰 때 생산·수리·유통·요금·안전의 관계를 설계할 수 있지만, 이를 모든 Gaslamp 요청에 강제하지 않는다. 안개의 가시 밀도와 독성/악취/질병 원인은 서로 다른 필드로 보존한다.

## 5. 건축과 사회를 거리·출입·노동으로 연결

빈민가·구빈원·살롱·클럽을 벽 재료나 옷차림 하나로 판정하면 사회적 의미를 왜곡한다. [National Trust의 호출 설비](https://www.nationaltrust.org.uk/discover/history/art-collections/country-house-communication-through-the-ages)는 공간과 노동을 연결하는 구체적인 사례다.

- 밀집 주거: 공용 통로·여러 문·공동 계단을 묘사하고 빈곤/이민/범죄성은 별도 문맥으로 둔다.
- 사용인: 호출 레버·전선·종·서비스 구역은 가시 구조다. 고용 지위·복종·착취·임금은 의상만으로 확정하지 않는다.
- 클럽/사교: 문지기·방문자·명함·문턱은 배제의 가능한 장면이다. 실제 자격이나 차별 원인은 별도 문맥이다.
- 구빈원: 시설 이름·연대·기록이 필요하다. 침상이나 벽만으로 교도소/작업장과 구별했다고 평가하지 않는다.
- 온실: 구조 프레임·유리·식재·통로를 중립 단위로 둔다. 감금·독초·식민 수집이 필요한 경우 각각 추가한다.
- 고딕 리바이벌/아르누보: [고딕 부흥의 역사](https://www.nationaltrust.org.uk/discover/history/architecture/what-is-gothic-revival)와 [아르누보의 유기적 선](https://www.metmuseum.org/essays/art-nouveau)을 구분한다. 장식 사진만으로 건립 연대·종교·지역까지 판정하지 않는다.

가정교사·유급 동반인·작위·젠트리·신흥 부자·후원·사교 데뷔는 선언된 역할/관계다. 책·안경·비싼 옷이 그 신분의 직접 증거가 되지 않도록 G24/G25를 문맥으로 남겼다.

## 6. 복식은 기능과 실루엣을 나누어 강화

[V&A의 복식 자료](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)를 참조해 몸통 지지, 치마 둘레 지지, 뒤 돌출을 서로 다른 실현으로 나눴다. 실제 내부 장치와 겉에서 관찰되는 실루엣의 검토도 분리한다.

| 단위 | 핵심 차이 | 반영 판단 |
|---|---|---|
| Corset/stays | 몸통 패널·지지와 속옷 겹침 | 현대 뷔스티에 상의와 의미를 분리; 통증·압박 강도·성적 의미 자동 부여 금지 |
| Cage crinoline | 허리에서 몸 둘레로 퍼지는 치마 지지 | 기존 실루엣 CID 재사용; 내부 후프 실현은 별도 선택 |
| Bustle | 착용자 기준 뒤쪽에 집중된 돌출 | 기존 owner 관계 보존; 일반 영어 bustle의 분주함과 구별 |
| Chatelaine | 같은 허리 걸쇠에서 체인·도구가 이어짐 | 기존 두 CID의 관계를 잇는 동일-owner 증거 보강 |
| Reticule/lorgnette | 조임끈 가방/손잡이 렌즈의 물건 구조 | 목걸이 도구·샤틀렌·단안 망원경과 혼동하지 않음 |
| 애도복/jet | 물성·색·의례의 층 분리 | 검정·무광·보석만으로 사별·재료 정체·애도 단계 판정 금지 |

[FIDM의 샤틀렌 자료](https://fidmmuseum.org/learn/articles/chatelaine-purse)는 다중 도구와 단일 주머니 변형을 구분한다. 이 차이는 candidate 단위의 경계를 정할 근거가 된다. 모든 도구를 한 장면에 늘리는 방식으로 확장하지 않는다.

방문 명함과 무도회 순서 수첩도 따로 둔다. [Prague 박물관](https://www.muzeumprahy.cz/en/for-schools-museum-on-line-on-line-exhibitions-asking-for-a-dance/)의 자료는 수첩·연필과 1882년 사례를 지원한다. 선택한 국가·행사·연도를 섞지 않고, 이름이나 춤 순서를 읽는 것은 별도 exact-text 평가로 둔다.

## 7. 추모·심령·환영은 ‘어느 면에 있는가’를 명시

[SMG의 모발 브로치](https://collection.sciencemuseumgroup.org.uk/objects/co156284/brooch-containing-human-hair-europe-1701-1900)와 [FIDM의 모발 공예](https://asufidmmuseum.asu.edu/learn/articles/hairwork-diadem)는 물질과 사회적 용도를 구분할 단서를 준다. 모발 공예를 모두 사망자의 유품으로 취급하지 않는다. 검은 옷도 사망 여부나 과부 신분의 증거가 아니다.

심령 관련 데이터는 다음 구분이 중요하다.

1. **자동서기:** 손→작은 판→연필→종이의 연결. [NPS 소장품 설명](https://www.nps.gov/long/blogs/planchette.htm)은 바퀴/연필 구멍을 설명한다. 알파벳판의 포인터와 섞지 않는다.
2. **심령 사진:** 두 형상이 실물 인화물의 경계 안에 존재하는가. [사진 박물관 자료](https://blog.scienceandmediamuseum.org.uk/photography-a-z-ghosts-spirit-photography/)는 유령 같은 형태와 사진적 과정을 구분할 근거다. 사진 외부 공간의 유령과 별도 후보로 둔다.
3. **무대 환영:** 광원/원상→기울어진 투명 판→상이 연결되는가. [Science World](https://www.scienceworld.ca/resource/peppers-ghost-hologram-illusion/)의 시연은 반사 원리를 지원한다. 현대 기기나 홀로그램을 역사 장면에 자동 삽입하지 않는다.
4. **거울 불일치:** 실제 공간의 원상·반사면·대응 배경이 충분히 보이는가. 《Dracula》의 선택 구절은 한 문학 규칙의 사례다. 거울 시야 밖 인물이 안 보이는 정상적인 기하와 구별해야 한다.
5. **비가시 주장:** 자동성·교신 성공·빙의·최면·사후 상태·과거 기억은 물건과 자세만으로 통과시키지 않는다.

타로는 선택한 덱의 연대와 도상을 기록한다. [V&A](https://www.vam.ac.uk/articles/tarot-cards)의 여러 소장품 캡션은 ‘모든 시대에 같은 현대 덱’이라는 정규화를 피할 근거다. 전통/결사/종교를 한 의례 도형으로 병합하는 작업은 추가 사료 조사 전 보류한다.

## 8. 마법은 행위자·대상·매체·가시 효과로 분해

- **인장:** 어디에 새겨져 있는지 표면 소유자를 명시한다.
- **결계:** 경계·저지 대상·접점·바닥을 같이 보이게 한다. 선만 있어도 보호 효과가 증명되는 것은 아니다.
- **공감주술:** 대응하는 두 물건을 구분한다. 천 조각과 의복이 동일한 물리 물건으로 합쳐지지 않도록 graph를 분리했다.
- **계약:** 두 당사자가 같은 문서에 연결되는 관계는 시각화할 수 있다. 영혼·기억·시간이라는 대가, 자발성, 법적 효력은 문맥이다.
- **진명/geas/저주:** 효과 조건·의무·세대·시간은 별도의 설정이다. 이름표나 상처가 그 의미의 증거가 되지 않는다.
- **사령술:** 죽은 자에게 질문, 사체의 운동, 생명 복귀, 인격 복귀를 분리한다.
- **construct/automaton:** 만들어진 존재의 범주와 실제 기계 링크의 하위 유형을 분리한다. 모든 construct에 황동·톱니를 넣지 않는다.

이 장의 구체 형상은 출처가 인증한 표준 마법이 아니라 저술한 판타지 실현이다. 전통·문화·판본의 공통 규칙으로 승격하지 않는다.

## 9. 기괴한 과학·의학의 실제 주장 범위

[NLM 전시](https://www.nlm.nih.gov/exhibition/frankenstein/exhibition3.html)는 갈바니즘과 생명 실험의 역사·문학적 접점을 설명한다. 전극·리드선·가상 표본의 연결은 그릴 수 있지만 생명이나 인격의 복귀를 한 화면으로 증명할 수는 없다. 《Frankenstein》 5장의 선택 구절도 읽었으며 목의 볼트나 번개 기계가 모든 원문 기반 장면의 의무라는 결론은 내리지 않았다.

골상학은 **역사적 모형/담론**으로 저장한다. 구획 머리가 보인다고 인물의 실제 성격·범죄성·인종적 본질을 추론하지 않는다. 소장품 본문/도판 접근이 부족해 구체 도표의 native 등록은 보류 대상으로 표시했다.

[SMG의 laudanum 약병](https://collection.sciencemuseumgroup.org.uk/objects/co112895/glass-bottle-of-laudanum)은 사각병·마개·라벨이라는 구체 물건을 지원한다. 라벨 판독·실제 내용물·복용·의존·독살을 따로 기록한다. 생기론, 물리학/오컬트의 에테르, 마취제 ether, 퇴화/atavism 담론도 서로 다른 문맥 의미다.

해부 강의실은 좌석·시연대·관찰 시선, vivisection은 살아 있는 대상과 절차, reanimation은 시간적 상태 변화가 핵심이다. 교육용 모형을 썼다면 그 결과를 실제 시신이나 생체해부의 이미지 증거라고 보고하지 않는다.

## 10. 욕망·성적 경제·폭력을 삭제하지 않는 방식

성인 친밀함, 드미몽드, courtesan, brothel, 구속, 성적 강요, 가학·착취를 조사 범위에서 제외하지 않았다. 크롬에서 후반 표제를 확인한 뒤 G90~G112로 관음·페티시즘·합의된 BDSM·친족/혼인·시체성애적 모티프·생식 공포·시체 공급·훼손·혈마법·채무/협박·식민/제도 폭력의 경계를 보강했다. 성폭력 같은 상위 사건 분류는 원문의 세부 강제/착취와 구분해 기록한다.

| 의미 층 | 저장할 내용 | 시각화 가능한 부분 | 자동 추론하지 않을 내용 |
|---|---|---|---|
| 친밀함/욕망 | 성인 선언·관계·요청된 긴장 | 거리·시선·접촉·반응 | 동의·욕망·과거 관계 |
| 성적 경제 | 직업·후원·보수·의존 | 거래 매체/공간의 저술 장면 | 드레스만으로 성매매·계급 판정 |
| 구속/감금 | 장치·행동 제한·출입 조건 | 손목→커프→연결부→고정점, 내외 방향 | 성적 목적·동의·다른 출구 부재·지속 시간 |
| 상처/유혈 | 소유자·부위·형태·현재 상태 | 가상 상처·얼룩·직물 손상 | 성분·원인·가해자·살인 의도 |
| 성폭력/가학/강압 | 사건·동의·권력·의도 | 요청된 사건 중 실제 관찰 가능한 접점 | 표정·노출·속박만으로 범죄·쾌락·동의 확정 |

[Historic England](https://historicengland.org.uk/research/inclusive-heritage/lgbtq-heritage-project/law-and-oppression/criminal-desires/)와 [Parliament의 역사 개요](https://www.parliament.uk/about/living-heritage/transformingsociety/private-lives/relationships/overview/propertychildren/)를 통해 시대·관할·제도에 따라 억압과 권리가 달랐다는 맥락을 보존한다. 의상이나 동성 동석을 성적 지향의 실제 증거로 만들지 않는다. 장르나 후보 검색 자체가 성인 나이·동의·성적 강도를 판정하지도 않는다.

추가로 [Parliament의 성적 규율 설명](https://www.parliament.uk/about/living-heritage/transformingsociety/private-lives/relationships/overview/sexualbehaviour19thcentury/)과 [Foundling Museum 전시](https://foundlingmuseum.org.uk/event/the-fallen-woman/)를 읽어 제도·낙인과 실제 인물을 구분했다. [시체 도굴의 의회 역사](https://www.parliament.uk/about/living-heritage/transformingsociety/private-lives/death-dying/dying-and-death/bodysnatching/)는 도굴·살인·제도적 시신 공급을 합치지 않을 근거다. `resurrectionist`를 부활 마법사로 잘못 번역하는 대조 질의를 추가했다.

## 11. 기존 데이터에서 확인한 구체적 문제와 재사용

조사 당시 manifest source: **20,341 candidates / 15,120 bindings**. 27개 지정 어휘군을 조사했고 full record·conditions·effects·binding 30개를 snapshot으로 남겼다. 현재 설치본이나 검색 상위 결과의 개수는 아니다.

- `gaslamp/gaslight`의 세 일치는 모두 gaslighting 관련이다. 장르 후보의 기존 coverage로 세면 안 된다.
- `bustle` 다섯 일치 중 일반 시장의 분주함도 포함된다. 양의 일치 수가 복식 의미의 충실도를 말하지 않는다.
- `calling card`의 기존 두 일치는 플레잉 카드와 시그넷 토큰이다. 방문 명함/무도회 순서 카드로 재명명하면 안 된다.
- 기존 크리놀린/버슬은 owner 관계가 이미 있다. 이를 없던 것으로 주장하지 않고 내부 받침·가시 실루엣·방향을 나누어 보완한다.
- 샤틀렌의 두 기존 CID는 고리/체인 문장을 담는다. 같은 허리 고리를 가리키는지 실제 native owner map에서 연결할 필요가 있다.
- 모발 로켓 CID는 이미 힌지·체인·비애도 대조까지 담는다. 복제보다 재사용이 적절하다.
- 기존 온실 후보는 성인과 빗장을 함께 보여주는 완전 실현이다. 일반 온실로 슬쩍 축소하지 않는다.
- 기존 요정 계약 후보는 두 당사자/공유 문서를 담지만 effects가 여러 차원·소유자에 넓게 펼쳐져 있다. 실제 변경 대상과 property로 좁히는 수작업 검토가 필요하다.
- 플랑셰트·갈바니즘 등의 어휘 0 일치는 **신규 후보 필요를 입증한 것과 다르다**. generic writing, lab apparatus, reflection과 full meaning 비교 후 결정한다.

원문·조건·효과·연결 snapshot과 18개 제안은 [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)를 참조한다. 모든 20,341개의 의미를 수작업 완독한 조사는 아니다.

## 12. 산출물의 의미와 다음 단계

113개 카드의 `still/proxy/context` 구분과 한영 후보 초안 79개는 **연구 데이터**다. 실제 CID/RID, native owner/permission 자격, rank, prompt transport, 이미지가 아니다. 각 카드의 `gates`는 선택한 실현을 검토할 조건이며 장르명으로 일괄 활성화하지 않는다.

원 대화 13절의 면허·산업·기반시설·망자 법률·상속·유물 거래·초자연 노동·반식민 마법·관료제·평판 마법을 G97/G102~G108로 연결했다. 영지의 선택을 다루는 [작가 공식 소개](https://ajlancaster.com/books/the-stariel-series/lord-of-stariel/)와 [섭정기 기관/공급의 공식 소개](https://www.panmacmillan.com/authors/zen-cho/sorcerer-to-the-crown/9781447299462), [1912년 카이로의 공식 소개](https://us.macmillan.com/books/9781250807731/amasterofdjinn/)는 서로 다른 세계/시대 대조를 지원한다. 9개 작품을 모두 읽거나 내용 전체를 검증한 것은 아니다. 작품명은 설정의 참고 문맥이며 등장인물·복식·서사를 자동 복제할 활성화어로 쓰지 않는다.

원문 7개 조합은 [SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md)에서 가시 장면과 남는 문맥으로 나눴다. 한 컷에 보이지 않는 사회 제도·영혼·기억·역사의 주장을 소품으로 통과시키지 않는다.

실제 반영은 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)의 P0→P1 단계를 따른다. 평가 질의와 [PIXEL-PLAN.md](PIXEL-PLAN.md)는 준비됐지만 실행하지 않았다. 연구 구조 PASS와 실제 검색/이미지/사용자 수용 PASS를 분리해서 보고한다.
