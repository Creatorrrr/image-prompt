# 스페이스 호러: 시각 의미와 후보 데이터 강화 연구

2026-10-22. [참조 대화](https://chatgpt.com/c/6ada0050-0814-83ec-9e08-64f95a15d94e)의 **핵심 180항목·보조 어휘 20개**를 조사 범위로 삼았다. 번호 전체는 [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md), 실제 장면 제안은 [VISUAL-CARDS.md](VISUAL-CARDS.md), 문맥 구분은 [CONTEXT-DISTINCTIONS.md](CONTEXT-DISTINCTIONS.md)에 있다. 작품 8개와 조합 8개의 적용 범위는 [SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md)에 남겼다.

이번 강화의 중심은 **우주선이라는 물리적 경계, 생존 계통의 의존 관계, 생물과 장치의 접점, 관측과 해석의 차이**다. 기존 코스믹·바디·SCP·리미널 연구에 우주 배경 단어를 붙이는 방식으로는 압력 전이실, 생명유지 고장, 표본 이동 방향, 표류의 연결 단절이 충분히 표현되지 않는다.

64개 의미 카드 중 61개를 한영 후보 초안으로 만들었다. 나머지 V41·V47·V61은 생체 해부·생식 강압·시신 자원화의 **정황**만 제안하므로 양성 후보로 보류했다. 해당 주제 자체는 원문 경로와 D10·D11·D18에서 유지했다. 초안 숫자는 운영 후보 수가 아니며, 카드 수와 합산하지 않는다.

## 조사 방법과 증거 범위

1. `read_thread`로 대화를 읽고 20,000자에서 후반이 잘린 사실을 확인했다. 로그인된 Chrome의 실제 대화 표에서 180개 원문 라벨, 보조 어휘, 작품·조합 표를 복원했다. 캐시와 원문 번호를 보존했다. 후반 대화 전체의 원문 바이트를 파일로 내보낸 것은 아니다.
2. NASA·ESA의 기술 설명, 생물학 교육기관 설명, 원논문 초록, Mori·Bostrom의 원문 정의, 제작자 설명, SF 사전과 영화 비평을 비교했다. [sources.json](sources.json)은 **36개 조사 기록**이며 29개는 본문·초록·공식 소개 범위, 5개는 검색 발췌, 2개는 접근 실패다. 본문 29개 중에도 저서 전체 독해나 모든 기술 기준 검토가 아닌 범위가 있다.
3. 출처가 설명한 정의와 이 연구가 저술한 장면을 분리했다. 카드의 구체적인 도구·문 위치·인원·윤곽은 대부분 선택형 구성안이다. NASA 설명이 허구 장면의 정확성을 승인하거나 BFI 비평이 보편 장르 외형을 정한 것은 아니다.
4. 현재 manifest의 후보 19,801개, 연결 14,246개, 모듈 67개를 읽었다. 양성 본문의 지정 필드 7개에 대한 45개 어휘 검사와 보조 변형 18개 검사를 수행했다. 후보 40개의 전체 레코드와 연결을 별도 스냅샷으로 남겼다. 실제 검색·임베딩·순위 평가를 실행한 것은 아니다.

원문 200개를 각각 독립 사전에서 검증한 것은 아니다. 개념군의 중요한 구분을 독립 자료로 확인하고, 세부 가설·판본·비평 원전의 남은 조사 범위를 기록했다. 특히 전문 미독 자료가 필요한 생식 도상·Blindsight의 의식 논증·대우주 종말 가설을 승인된 시각 사실로 만들지 않았다.

## 1. 장르를 장소·위협·해석으로 분해한다

`Space Horror`는 우주 환경과 지원 불가·취약한 거주 조건이 작용하는 범위다. `Cosmic Horror`는 인간의 인식과 가치가 흔들리는 방식이며 지구에서도 성립한다. `SF Horror`는 더 넓은 과학기술적 설정을 포함한다. `Gothic SF`는 비밀·과거·폐쇄·귀환의 서사와 연결되며 첨탑 장식만의 분류가 아니다. [SFE Horror in SF](https://sf-encyclopedia.com/entry/horror_in_sf), [Gothic SF](https://sf-encyclopedia.com/entry/gothic_sf), [BFI 작품 비교](https://www.bfi.org.uk/lists/10-great-lovecraftian-horror-films)

데이터에서는 장르를 문맥 레코드 D01에 둔다. 우주복·촉수·초록빛·고어·성적 상징·불가능한 공간을 한꺼번에 활성화하지 않는다. 장르와 별개로 사용자가 실제 지정한 관계를 해석하고, 그 이후 선택 가능한 장면 재료를 제시한다. 코스믹 공포는 필요조건이 아니고 전투·생존·노동·유령·생식 공포가 독립적으로 결합할 수 있다.

## 2. 생존 공포의 중심은 압력과 생명유지의 연결이다

진공, 감압, 저산소증, CO2 축적, ebullism, 감압병, 압력손상은 같은 사건명이 아니다. ECLSS도 산소통 하나가 아니라 공기 정화·산소 생성·환기·물 회수 등의 연결이다. 따라서 `oxygen remaining`과 `scrubber failed`는 양립 가능한 설정이다. [NASA Spacesuits](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/), [NASA ECLSS](https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/)

V01은 두 압력 경계를 가진 전이실, V02는 양쪽 계기의 다른 표시, V03은 외피 관통, V04는 장치와 분리된 유로, V05는 서로 다른 재생 계통의 연결을 제안한다. 각각 **방/해치/안팎**, **계기/해치**, **선체/구멍/외부**, **장치/호스/커플링**을 분리해 기록한다. 기침하거나 쓰러진 인물 하나를 `hypercapnia`, `hypoxia`, `decompression sickness`의 만능 표현으로 등록하지 않는다.

화면에 쓰인 압력·CO2 수치는 **묘사된 계기 값**이다. 실제 물리량이나 임상 진단이 입증된 것은 아니다. 인체 위기의 과학적 정확성과 사진에서 읽히는 긴장감을 별도 평가한다.

## 3. 무중력·화재·열·잔해에는 환경 조건이 필요하다

무중량은 중력 소멸과 다르다. V16은 공통 아래쪽이 없는 인물·도구와 제어 접촉을 함께 제안한다. V17은 붙은 방울과 따로 떠 있는 액체를 분리한다. `red`는 물질의 색이고 실제 혈액의 출처·인간 종·치명상을 자동 증명하지 않는다. [NASA Microgravity](https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/)

정지·비대류 조건의 구형 촛불 실험을 모든 우주선 화재에 일반화하면 안 된다. V06은 **가압·환기 조건을 정한 허구 장면**이며 실제 유동·연료 특성은 별도 검토한다. 방열판은 태양전지판이나 호일 단열재와 구별해야 한다. V07의 외형은 장치 식별을 돕지만 온도·열 제거 성공을 증명하지 않는다. [NASA 촛불 비교](https://www.nasa.gov/image-article/candle-flame-1g-vs-microgravity/), [ESA Thermal Control](https://www.esa.int/Enabling_Support/Space_Engineering_Technology/Thermal_Control)

V10은 단일 파편과 차폐 손상이다. 케슬러 증후군은 **충돌이 추가 충돌을 유발하는 시간적 연쇄**이므로 잔해 구름 한 장으로 충족되지 않는다. 방사선은 장면의 초록 안개를 사실로 요구할 수 없고, V11의 선량계·차폐 구획은 위험 대응의 정황으로 남는다. [ESA 잔해 FAQ](https://www.esa.int/Space_Safety/Space_Debris/Space_Debris_FAQ_Frequently_asked_questions), [NASA 위험 개요](https://www.nasa.gov/hrp/hazards/)

## 4. 연결과 이탈은 같은 EVA 후보가 아니다

기존 EVA 후보는 압력복·배낭·안전줄을 포함한다. V14는 **허리 연결부에서 선체까지 끊기지 않은 줄**, V15는 **몸 쪽 연결은 남고 선체에 닿지 않는 자유 끝**을 다룬다. 한 후보의 `tether`를 반대로 해석하면 명백한 관계 모순이 된다.

표류 후보도 줄 끝이 화면 밖이면 이탈을 통과시키면 안 된다. 자유 카라비너가 보여도 다른 추진장치가 없는지, 인물이 실제 멀어지는지까지 증명하지 않는다. 연결부 판독성과 전체 구도의 긴장감은 따로 평가한다. 기술 장비를 모두 보여주기 위한 과도한 근접 구도를 보편값으로 삼지 않는다.

## 5. 장소 이름보다 기능·인원 부재·흔적을 정밀하게 다룬다

`Derelict`의 노후·불능, `Ghost Ship`의 인원 부재와 남은 작동, `Haunted Spaceship`의 초자연적 개입은 분리한다. V18의 보수판과 손상, V19의 사람이 없는 배식, V20의 거울 불일치는 서로 다른 선택이다. 마지막 사례가 유령인지 환각인지 합성인지도 외형만으로 결정되지 않는다. [BFI Alien의 노동 공간](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver), [Event Horizon 비평](https://www.bfi.org.uk/lists/10-great-lovecraftian-horror-films)

세대우주선의 세대 계승과 동면선의 장기 수면은 다르다. V21의 열린 캡슐과 V22의 생활 흔적은 이 설정을 돕는 **정황**이다. 가족사진은 혈연을, 빈 캡슐은 사망을 증명하지 않는다. BDO도 거대함 때문에 지능이 없다는 뜻이 아니다. V26은 비교 가능한 척도, V27은 유적층과 표지의 구별만 다룬다. [Generation Starships](https://sf-encyclopedia.com/entry/generation_starships), [BDO](https://sf-encyclopedia.com/entry/big_dumb_objects)

## 6. 외계 생태는 부착·성장·편익·통제의 축으로 나눈다

기생체의 접점, 포식기생의 최종 숙주 사망, 넓은 공생과 상리공생, 공간적 만연, 체내 감염은 다른 의미다. V31의 부착, V32의 경계 밖으로 나온 작은 몸, V33의 양쪽 포트 연결, V34의 덕트와 선실에 걸친 분포를 분리했다. [Kentucky 포식기생 설명](https://entomology.mgcafe.uky.edu/ef018), [Utah 공생 설명: 검색 발췌 범위](https://learn.genetics.utah.edu/content/symbiosis/examples/)

외계 종이므로 사람을 감염시킬 수 있다는 전제도 과학적 사실이 아니다. 포식기생의 생활사나 상호 이익은 후속 관찰·설정이 필요하다. 군체 의식·군집 지능·초개체도 하나의 반응이나 가는 실만으로 증명되지 않는다. 비인간형 외형과 비의식적 지성 역시 별개다. Blindsight는 작가의 소개 범위만 읽었으므로 세부 의식 논증을 검증했다고 하지 않는다. [작가 소개](https://www.rifters.com/blindsight/BS_main.htm)

## 7. 오염과 격리에는 이동 방향·경계·운반자가 필요하다

전방 오염은 지구에서 목적지로, 역방향 오염은 귀환 표본 등을 통한 지구 쪽으로 향하는 경로다. V35는 도구와 현지 토양, V36은 귀환 캡슐과 외부 실험실, V37은 격리 경계를 통과하는 운반자·용기를 구분했다. 장갑·더러움·경고 표지 하나로 실제 미생물 오염이나 위반을 확정하지 않는다. [NASA JPL 구현 설명](https://planetaryprotection.jpl.nasa.gov/mission-implementation)

기존 `cross-world return quarantine bay`에는 특정 primary tag 조건이 있다. 우주 검역을 추가한다는 이유로 그 조건을 삭제하지 않는다. 기존 재료가 가진 세계관을 보존하거나 새로운 독립 장면을 만든다. V37도 닫힌 용기를 옮기는 장면만 보이므로 누출·감염 완료의 대체 증거가 아니다.

## 8. 바디·생식·성적 공포는 대상을 생략하지 않는다

V38의 조직 융합은 포옹·겹침과 다르며 두 몸과 접합부가 동시에 보여야 한다. V39의 층이 벗겨진 형태는 현재 상태이며 유전적 돌연변이나 시간적 변신을 자동 증명하지 않는다. Dead Space 제작자는 작품별 인체 재배열과 손상 층을 설명하지만 이를 모든 생물의 기준으로 확대하지 않는다. [EA Motive 제작 설명](https://www.ea.com/able/news/inside-dead-space-2-new-necromorph-nightmare)

생식 공포에는 강제 수정·기생 배태·산란·출생·출산 통제·우생학·인공 자궁·혈연 금기·성적 도상·성폭력 알레고리·유혹이 모두 남는다. **외형, 행위, 발생 원인, 의도, 동의, 혈연**을 각각 기록한다. 임신 외형은 강제성을, 산란관은 성폭력을, 근접한 인물은 유혹·친밀함의 동의를 증명하지 않는다. High Life 비평은 작품 속 감금과 생식 권력 관계의 사례이지 일반 인물의 실제 이력 근거가 아니다. [BFI High Life](https://www.bfi.org.uk/sight-and-sound/reviews/high-life-review-claire-denis-probes-outer-reaches-human-taboos)

V42의 허구 인공 발생 용기는 자궁외 양 태아 지지 실험과 구별한다. 해당 2017 논문은 인간의 수정부터 출생까지 완전 체외 발생이 달성됐다는 근거가 아니다. V45의 유기 출입구는 상징적 도상 가능성에 대한 초안이며 Creed 전문·개별 도판 검토를 더 해야 한다. `Monstrous-feminine`를 여성성 자체의 병리·악으로 고정하지 않는다. [원논문 초록](https://www.nature.com/articles/ncomms15112), [Creed 출판사: 검색 목차 범위](https://www.routledge.com/link/link/p/book/9780367209452)

## 9. 심리·AI·복제는 보이는 몸과 작동의 증거를 분리한다

고립·단조로움·감각박탈·일주기 불일치·의심·기억상실·죄책감·의식 지속은 별개다. NASA의 구체적인 위험 연구를 `우주에 가면 광기에 빠진다`는 규칙으로 바꾸지 않는다. V51의 열린 눈은 의식이 수십 년 지속됐다는 증거가 아니다. [NASA 고립 연구](https://www.nasa.gov/hrp/hazard-isolation-and-confinement/)

V48은 열린 합성 외피와 손으로 이어지는 부품, V49는 승무원과 화물의 차단, V50은 독립된 닮은 몸 두 개를 제안한다. 이것으로 목표 불일치·충성·사람 여부·의식 연속성·악의가 입증되는 것은 아니다. Uncanny Valley는 인간 유사성 반응에 관한 가설이며 언캐니 일반과 다르다. [Mori의 승인 번역](https://spectrum.ieee.org/the-uncanny-valley)

## 10. 신호·기록·번역의 위험을 기호 모양으로 고정하지 않는다

조난 신호·반복 비콘·유인·금지 지식·현실 정보 위험·허구 인지재해·밈 감염·정보 무기·기술 흔적·번역 함정은 작동 층위가 다르다. V52의 재생 장치와 수신기, V53의 화면과 두 반응, V54의 원문과 다른 두 출력은 **매개체와 해석의 정황**이다.

Bostrom의 정보 위험 정의는 정보 유통으로 해가 가능해지는 문제다. 기호를 보자마자 초자연적 손상이 생긴다는 허구 인지재해와 등치하지 않는다. 바실리스크도 이번 문맥은 정보 무기 모티프이며 도마뱀 후보로 연결하지 않는다. 통신 지연·간섭·정전·AI 봉쇄는 원인이 다르다. [정보 위험 원문 정의](https://nickbostrom.com/information-hazards.pdf), [NASA 통신 지연·간섭](https://www.nasa.gov/missions/tech-demonstration/space-communications-7-things-you-need-to-know/)

## 11. 시공간·대우주 가설에는 별도 증거 방식이 필요하다

블랙홀의 중심 어두운 영역, 지평선, 렌즈상, 원반, 특이점은 동의어가 아니다. V55는 원반이 있는 선택형 시각화이며 V56은 허구 선체 변형이다. V57은 의도된 투영 모순, V58은 경계 안 다른 풍경이다. 실제 곡률 공간이나 어안 왜곡을 공포의 불가능 기하와 혼동하지 않는다. [NASA Anatomy](https://science.nasa.gov/universe/black-holes/anatomy/)

시간 지연·루프·인과 고리·misjump는 현재 사진에 쓰인 시계 숫자나 같은 얼굴로 검증되지 않는다. 여러 상태를 보여야 한다면 명시적인 시퀀스로 분리하고 단일 사진 평가와 합산하지 않는다. 페르미 역설·거대한 침묵·필터·암흑의 숲·동물원 가설·심시간·열적 죽음·거짓 진공은 설명·가설·세계관으로 보존한다. 어두운 별하늘이나 붉은 파동을 가설의 확정된 외형으로 만들지 않는다. [SETI의 문제와 관측 한계](https://www.seti.org/research/seti-101/fermi-paradox/)

## 12. 기업·식민·식인 공포와 미학은 관계를 통해 전달한다

V60의 공급 접근권 비대칭은 생명유지 독점의 단서일 수 있지만 정상 안전관리와도 구별해야 한다. 수탈·식민주의·비동의 실험·무기화·제의 희생·식인·시신 자원화는 각각 **누가 누구/무엇을 어떤 경로로 다루는가**가 다르다. 먹는 대상의 종과 기원, 죽음, 제의 목적·강압을 일반 식사나 제단으로 대체하지 않는다. V61의 정황을 양성 후보에서 보류한 이유다. [Alien 노동 비평](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver), [High Life 비평](https://www.bfi.org.uk/sight-and-sound/reviews/high-life-review-claire-denis-probes-outer-reaches-human-taboos)

Cassette Futurism은 테이프·CRT·물리 조작계의 기능적 조합으로, industrial decay는 마모와 임시 수리의 구체적인 대비로 보강한다. 소음·정적·기록의 진위·화면 밖 실제 존재는 단일 사진의 관찰을 넘는다. 숭고·언캐니·weird/eerie·liminal은 같은 검정 팔레트 레시피가 아니다. Fisher의 책은 출판사 소개와 발췌 검색 범위, 숭고는 미술관 검색 발췌 범위로 조사했으므로 전문 독해의 결론과 구분한다. [Repeater 소개](https://repeaterbooks.com/product/the-weird-and-the-eerie/), [미술관 숭고 설명](https://www.nationalgalleries.org/art-and-artists/glossary-terms/sublime)

## 데이터 반영의 결론

**우선 등록할 것은 압력 경계·연결/이탈·장치 의존·표본 이동·선체 조직 통합처럼 현재 프레임에서 구별되는 관계다.** 철학·의식·강압·과거·감염 원인은 문맥과 주장 한계에 보존한다. 기존 자료의 의미·조건·효과를 검토한 뒤 `reuse / refine / new / context / defer`로 처리한다. 정확한 파일·순서·판정 기준은 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 있다.

현재 완료된 것은 연구·초안·증거 스냅샷·평가 설계다. 운영 소스 등록, 새 인덱스, 실제 후보 노출, 생성 이미지, 픽셀 구현, 미적 개선, 사용자 수용은 별도 단계이며 이번에는 실행하지 않았다.
