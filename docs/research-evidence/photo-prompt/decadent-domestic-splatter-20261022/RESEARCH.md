# 퇴폐미 × 가정 스릴러 × 스플래터: 데이터 강화 리서치

2026-10-22 KST. 참조: 「조합 용어 조사 설명」, conversation `6ad98465-2b84-83ee-b6b1-d949c7a5c1a7`.

핵심 제안은 **호사스러운 표면, 자율성을 제한하는 접근 관계, 몸의 경계와 결과를 서로 구별하면서 한 장면 안에서 연결하는 데이터**를 보강하는 것이다. `decadent + mansion + blood` 같은 조합 태그만 늘리면 누가 무엇을 소유·접촉·관찰하는지 사라진다. 반대로 모든 금기를 일반 소품으로 바꾸면 요청의 사건과 강도가 사라진다. 명시된 의미는 유지하고, 화면이 보여 주는 사실과 해석·시간·동의·진단을 따로 기록해야 한다.

이번 산출물은 **108개 의미 카드(가시 실현 86개와 문맥 전용 22개), 그중 86개 한영 후보 초안, 252개 관계 gate, 외부 출처 61개, 기존 CID 전체 스냅샷 28개, 평가 사례 88개/한영 질의 176개**다. 카드와 초안은 중첩하므로 합산하지 않는다. 모두 연구 자료이며 운영 CID/RID·검색 인덱스·native 승인으로 등록하지 않았다.

## 1. 원 대화에서 실제 확인한 범위

`read_thread`의 원 대화 답변은 20,000자에서 잘렸고 cursor가 없었다. 이후 브라우저에서 같은 대화의 렌더링 본문과 표 셀을 읽어 **17개 표의 데이터 189행 전체**를 확인했다. 조합 축 3·후속 용어 170·창작 조합 표현 8·참고 작품 8이다. 처음 잘렸던 시체상 무덤 설명도 확인했다. [대응표](KEYWORD-ATLAS.md), [원 bounded 반환본](REFERENCE-THREAD-BOUNDED.json), [브라우저 보완 기록](REFERENCE-BROWSER-SUPPLEMENT.json), [접근 범위](ACCESS-LIMITS.md)를 보존했다.

브라우저 보완본은 표의 명칭과 연구자의 설명 요약을 보존하며 원 답변 전체의 DOM 덤프는 아니다. 이후의 창작 조합명은 기존 장르명과, 참고 작품의 줄거리·비평은 영화 전체의 프레임 분석과 구별한다.

표의 용어가 여러 가지를 함께 쓴 경우 원 행을 유지했다. 예를 들어 Silk / Satin, Castration / Genital Mutilation은 원 목록의 한 행이지만 내부 의미를 같은 개념으로 합치지 않는다. 이번 189행은 독립 개념 수나 모든 정의의 검증 수가 아니다.

## 2. 세 축과 인접 장르를 나누는 방식

|축|문헌상 중심|보강할 가시 데이터|같은 것으로 취급하면 안 되는 것|
|---|---|---|---|
|Decadent Aesthetic|유미주의의 생활·실내로의 확장, 인공성·과잉·아이러니·욕망의 역사|금박의 층 손실, 파일의 마모, 과숙한 과일, 정렬된 진열과 흐트러진 부분|도덕적 타락·정신질환·검은 색조·19세기 저택을 필수 외형으로 고정|
|Domestic Thriller / Noir|집·직장·친밀한 관계의 위험과 권력|문턱·열쇠·돈·기록·통신 기기의 서로 다른 접근, 관찰과 보이는 반응|비싼 집·기혼 여성·폭행 상흔 하나를 장르 전체로 대체|
|Splatter Horror|직접 제시되는 신체 손상이라는 표현 축|신체 부분의 소유자, 실제 끝점, 공동, 연결/분리, 노출 범위|추적 구조인 슬래셔, 변형·자율성의 바디 호러, 반문화적 문학 계보인 스플래터펑크를 합침|

Domestic Noir의 제안자 Julia Crouch는 집뿐 아니라 직장과 관계를 포함한다. 따라서 가정 스릴러용 새 후보가 범죄자·피해 여성·부유층 저택을 자동 추가하면 의미를 좁히게 된다. [Crouch의 원문](https://juliacrouch.co.uk/blog/genre-bender)

유미주의는 그림과 문학뿐 아니라 의복·가구·실내·생활양식에 걸쳤다. 또한 데카당스에는 캠프·웃음·아이러니를 강조하는 연구도 있다. **모든 퇴폐 장면을 무기력·우울·고어로만 표현하는 데이터는 부족하다.** 과하게 정돈된 작은 사물, 훼손된 부분과 온전한 부분의 대비, 통제된 조명·제스처 같은 대안을 유지한다. [V&A](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [Cambridge 연구](https://www.cambridge.org/core/journals/victorian-literature-and-culture/article/decadence/2621A4931E82EFF8948DCCE2DB7A3423)

지알로는 이탈리아어의 일반 범죄물 용법과 해외 영화비평상의 특정 전통을 구분한다. 검은 장갑·네온·불완전 목격은 선택 가능한 관습이다. 그랑기뇰은 공연의 역사, 뉴 프렌치 익스트리미티는 비평적으로 묶인 영화들의 계보, 에로 그로 난센스는 근대 대중문화와 정치·소비·몽타주의 맥락을 가진다. 이를 하나의 `잔혹한 퇴폐 스타일`로 합치면 검색과 번역이 거칠어진다. [BFI 지알로](https://www.bfi.org.uk/features/where-begin-giallo), [Exeter Press](https://www.exeterpress.co.uk/products/grand-guignol-1), [BFI 신체 자율성](https://www.bfi.org.uk/features/pleasures-pain-new-french-extremity), [Silverberg 발췌본 인쇄 28–29쪽](https://content.ucpress.edu/pages/8868/8868.ch01.pdf)

이 문헌들은 개념과 구분을 지원한다. 아래의 정확한 물건·손의 위치·조명·관계 그래프는 이번에 저술한 창작 제안이며 해당 작품이나 역사 공간의 정본 디자인이 아니다.

## 3. 우선 보강할 아홉 영역

### A. 호사·인공성·쇠락: 13개 카드

마모를 무조건 `old texture`로 넣지 말고 **어느 재료의 어느 층이 어떻게 달라 보이는지** 구분한다. 액자에는 남은 금빛 층·손실 부위·바탕이, 벨벳 의자에는 파일·눌린 구역·주변 파일이 필요하다. 같은 현상을 피부 손상에 전용하면 안 된다.

특히 `tarnished gold-leaf surface`라는 기존 짧은 후보 표현은 검토가 필요하다. 순금 자체는 부식하지 않지만 금 합금의 은/구리 성분이나 도금의 기재는 변색할 수 있다. 따라서 `금이 녹슬었다`보다 **금박 손실 / 오염 / 기재 노출 / 합금·기재 변색**을 구별하는 후보가 정확하다. 사진으로 성분을 인증하는 것은 별도 문제다. [Canadian Conservation Institute](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html)

바로크·로코코·아르누보·고딕 리바이벌은 따로 유지한다. A11은 건축·조각·극적 빛의 결합, A12는 비대칭 곡선 패널, A13은 구조와 장식이 합쳐진 난간이다. 하나를 선택했다고 다른 세 양식이 동시에 의무가 되지 않는다. [바로크](https://www.rijksmuseum.nl/en/collection/node/Baroque--7ce3f58e9fcb4702b31ff783fb88c963), [로코코](https://www.rijksmuseum.nl/en/collection/node/Rococo--c40f1414283f45da861eeb4103b94d73), [아르누보](https://www.vam.ac.uk/articles/art-nouveau-an-international-style), [고딕 리바이벌](https://www.vam.ac.uk/articles/stained-glass-gothic-revival-and-beyond/)

### B. 접근·자율성·노동 동선: 14개 카드

핵심 단위는 `통제적인 사람`이라는 외모가 아니라 **소지자 손→열쇠→구체적 출입 경계**, **손→돈→지갑→다른 손의 접근**이다. 표정 하나가 없어도 접근 배치는 보일 수 있고, 그 배치만으로 장기적인 학대는 확정할 수 없다. 실제 강압적 통제는 반복과 영향의 문제를 포함한다. [Home Office 지침](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

공간 후보는 앙필라드의 시선 축, 문 표면 빗장과 받이, 서비스 계단의 갈림, 호출 벨의 연결을 구체화한다. 귀족과 하인의 역할은 복식이나 성별로 인증하지 않는다. [Met 전시 설계](https://www.metmuseum.org/ko/press-releases/visitors-to-versailles-2018-exhibitions), [National Trust의 통신·동선](https://www.nationaltrust.org.uk/discover/history/art-collections/country-house-communication-through-the-ages)

부두아르·침실·살롱·저장실·다락·지하실·납골 공간을 같은 장소로 합치지 않는다. 특정 방을 요청했을 때 그 방의 기능·기하를 지원할 수 있어야 하며, 이름만으로 성행위·감금·시신을 추가하지 않는다. 방 이름 전체의 독립 사전 검증은 남아 있다.

### C. 시선·감시·기록의 차이: 10개 카드

거울은 `인물→거울 안 반사→실제 대상`의 대응, 모니터는 `화면 경계→표식이 대응하는 실제 문`, 열쇠구멍은 `물리적 문→구멍 내부 가장자리→한정된 시야`가 필요하다. 가려진 목격은 **가려진 부분을 알 수 없다는 사실**까지 보존해야 한다. [BFI 지알로](https://www.bfi.org.uk/features/where-begin-giallo), [Freud Museum](https://www.freud.org.uk/2019/09/18/the-uncanny/)

기록 손상은 종이가 뜯긴 것, 반사로 가려진 것, 표기가 지워진 것, 서로 다른 이름이 적힌 것을 구분한다. 가계도·가족사진은 친족 진위·부재자의 사망·불륜을 인증하지 않는다. 기존 목격 후보도 단편을 완전 사건으로 바꾸지 않도록 조건과 효과를 검토해야 한다.

### D. 직물·표면·몸의 분리: 10개 카드

**실크는 재료, 새틴은 직조 구조의 층위**다. 다마스크의 광택 대비와 브로케이드의 장식 실을 하나의 `silk texture`로 합치지 않는다. D02·D03의 구체적 외관은 각각 한 가지 제안이며 모든 다마스크·브로케이드가 그 모습이라는 규칙이 아니다. 실제 섬유·직조 확인에는 물체와 분석 정보가 필요하다. [Met 의복 기록](https://www.metmuseum.org/art/collection/search/82495), [직물 보존 분석](https://www.metmuseum.org/perspectives/tibetan-thangka-textile-conservation)

찢어진 소매 아래 온전한 피부, 레이스 구멍 너머 피부, 장갑과 별도 빈 장갑, 도자기 인형의 관절을 구분한다. 이 영역의 실패는 몸과 의복의 소유자가 뒤섞이거나 일반 패션이 박피·절단·페티시 진단으로 변하는 것이다. 향수 분무는 입자와 방향만 보이고 냄새·기억·악취 은폐는 보이지 않는다.

### E. 만찬·의례·노출 강도: 8개 카드

좌석·공용 접시·손·덮개·메뉴·냅킨·용기의 관계를 보강한다. 닫힌 덮개 안 내용물은 미확정으로 남긴다. 붉은 액체·과일 과육·식기는 그 자체로 혈액·인육·내장이 아니다.

동시에 **모든 직접적인 신체 표현을 음식이나 붉은 얼룩으로 대체해서는 안 된다.** 요청이 허구 세계의 실제 신체 분리를 뜻하면 F01의 실제 형상을 검토해야 하고, 무대 분장 E08/F10은 그 요청의 충족이 아니다. 무대는 공연 맥락을 요청한 경우의 별도 실현안이다. [Grand-Guignol](https://www.exeterpress.co.uk/products/grand-guignol-1), [BFI 바디 호러](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### F. 신체 결과·경계·현재 단계: 10개 카드

분리된 부분의 양 끝점, 피부층과 아래 표면, 공동 밖의 분리 내부 구조, 아직 조직으로 붙은 외부화, 두 몸의 연속 조직, 한 몸의 변형 경계를 따로 설계했다. **분리와 연결, 의복과 피부, 모형과 신체, 가림과 부재**는 다른 상태다. 행위 방법·의료 절차는 연구 카드의 범위가 아니다.

현재 corpus의 `cand_0319d46abb0753fd80ede0a2a7c34c67`는 Dismemberment / Decapitation / Evisceration을 함께 명명하지만 긍정 본문이 설명하는 것은 신체와 분리 부분의 간격이다. **이것만으로 내부 구조와 공동이 필요한 적출 의미까지 충족한다고 볼 수 없다.** 기존 후보를 삭제하자는 결론이 아니라 개념·분기·역할의 정밀화가 필요한 구체적 사례다.

괴사는 조직 사망의 의학적 개념이다. 어두운 색·화장·피부색은 괴사 진단이 아니다. 허구에서 그 상태가 명시된 경우에도 픽셀은 선언된 외관의 구현만 평가한다. [MedlinePlus](https://www.medlineplus.gov/ency/article/002266.htm)

### G. 수집·애도·해부 모형: 15개 카드

가장 밀도가 높은 신규 조사 영역이다. 분더카머에는 자연물·공예·과학 도구의 구분과 진열 칸·서랍·분류표가 있고, 이는 소유욕·인간 수집을 자동 의미하지 않는다. [Met Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

모발 장신구는 기념 방식이지만 살아 있는 연인·친구 사이에도 교환됐다. G01은 기명 추모 표식이 있는 변형, G02는 모발만 있는 비애도 가능 대조다. 눈 미니어처는 그려진 눈이며 적출 눈이나 감시 장치가 아니다. [모발 브로치](https://www.metmuseum.org/art/collection/search/16805), [눈 브로치](https://www.metmuseum.org/art/collection/search/825835)

해부학적 비너스는 교육용 밀랍 모형이며 La Specola의 Venere는 층을 분리할 수 있는 사례다. 에코르셰도 청동상·도면으로 존재한다. 피부가 없는 형상이라고 실제 박피 피해자로 분류하면 매체와 의미를 모두 잃는다. [소장기관 설명](https://www.sma.unifi.it/vp-167-anatomia-umana.html), [Met 청동상](https://www.metmuseum.org/art/collection/search/195365), [Met 도면 해설](https://www.metmuseum.org/art/collection/search/355650)

인피 장정의 인간 유래는 외형적 가죽 무늬가 아니라 별도의 검사·출처 증거 문제다. 특히 Harvard의 **2026년 갱신 FAQ는** 옛 정신병원 환자 가설을 확정하지 않으며, 신원·정확한 채취 경위를 미확정으로 남긴다. 2024년 분리된 피부는 2025년 별도 위원회로 이관됐다. 따라서 옛 서사를 실제 확인 사실처럼 데이터에 넣으면 안 된다. [Harvard Library의 현재 설명](https://ask.library.harvard.edu/faq/82429)

시체상 무덤은 조각 매체이고, 모든 transi가 같은 상하 이중상 구성을 가진 것은 아니다. 존 배릿 사례는 일반 배치와 다른 점이 연구된다. 바니타스는 사치·쾌락과 죽음·덧없음 도상의 관계이며 메멘토 모리는 더 넓은 죽음 상기의 기능이다. [V&A 보존 기록](https://www.vam.ac.uk/__data/assets/pdf_file/0005/177215/17132_file.pdf), [배릿 연구 초록](https://www.tandfonline.com/doi/abs/10.1080/00681288.2019.1642013), [National Gallery 정물 해설](https://www.nationalgallery.org.uk/paintings/jan-jansz-treck-vanitas-still-life)

### H. 비평·권력·금기·비가시 주장: 22개 카드

비체·언캐니·카니발레스크·괴물적 여성성은 외모 분류가 아니라 비평적 관점이다. 예를 들어 비체는 단순한 오염물의 양이 아니라 주체와 대상 경계에 관한 논의이고, 괴물적 여성성은 여성의 생식성을 괴물화하는 재현 자체를 분석한다. [Kristeva 출판사 설명](https://cup.columbia.edu/book/powers-of-horror/9780231214575/), [Creed 새 판 소개](https://www.routledge.com/link/link/p/book/9780367209452)

가스라이팅과 DARVO는 구분한다. 전자는 현실 판단을 흔드는 조작, 후자는 책임 추궁에 대한 부인·공격·역할 역전의 순서다. Freyd는 DARVO의 사용도 특정 과거 행위의 유죄 증거가 아니라고 명시한다. 표정이나 부인 한 번으로 판단하는 후보를 만들면 안 된다. [제안자의 설명과 경고](https://www.jjfreyd.com/darvo/)

성적 욕망·억압·페티시·관음·가학/피학, 합의된 BDSM, 성적 강압·파트너 성폭력·재생산 강압, 근친과 가족 내 성적 학대, 시체성애, 성적 식인, 흡혈, 집단 성적 의례, 수간·동물성애를 용어 기록에서 삭제하지 않았다. **행위·관심·친족·동의·생사·대상 종을 별도 주장으로 보존**했다. 일반 접촉·소품·의복이 그 주장을 대체할 수 없기 때문에 해당 부분은 문맥 카드에 놓았다. 명시된 요청 의미를 일상 장면으로 다시 쓰라는 뜻이 아니다. [역사적 성 담론의 범위](https://doi.org/10.1017/9781108550826.013), [NCSF 동의 원칙](https://ncsfreedom.org/wp-content/uploads/2019/12/Consent-Counts-Statement.pdf), [WHO 정의](https://www.who.int/health-topics/violence-against-women/), [WHO 재생산 강압 설명](https://www.afro.who.int/sites/default/files/2020-06/Clinical%20Handook%20for%20Women%20Web%20final%20signed_0.pdf)

반대로 신체 분리·피부층·공동·융합처럼 현재 형태로 관찰 가능한 폭력/신체 결과는 F 카드에 구체적으로 남겼다. 어떤 단어가 불편하다는 이유로 모두 문맥 전용이 된 것은 아니다. 관찰 불가 판단과 생성 서비스의 출력 허용 판단도 서로 다르다.

### I. 명암·재현·구도·기록 매체: 6개 카드

브라우저에서 추가로 확인한 서사·시각·음향 용어를 반영했다. I01은 형태를 모델링하는 명암, I02는 넓은 어둠 속 선택적 밝음, I03은 활인화와 재현 이미지, I04는 내부 프레임, I05는 기록 매체, I06은 식탁·시선·신체 결과의 초점 위계다. 화자의 신뢰성과 초점화는 H20, 소리·공감각·시간은 H21, 창작 조합명과 작품의 지위는 H22에서 분리했다.

[보완 연구](REFERENCE-EXTENSIONS.md)에 성유물함, 서사 정보 제한, 명암법/테네브리즘, 활인화/폴리, 원 대화의 제안 조합명 8개 및 참고 작품 8개를 상세히 대조했다. 제안명은 정식 장르가 아니고 작품 소개를 읽은 것은 전편·프레임 관찰이 아니다. 조합명마다 필요한 관계와 남는 서사 경계를 연결했다.

## 4. 기존 corpus의 실제 관찰과 데이터 결정

[원문 관찰](CORPUS-FINDINGS.md) 당시 후보는 19,275개, 긍정 19,029개, diagnostic 246개, 모듈 55개였다. 지정 3개 본문 필드에서 퇴폐/유미주의 0, 수집·해부학 희귀명 0, 바니타스/애도명 0, 강압 관련 7, 재질명 47, 신체 손상명 6, 지알로/기뇰 2개였다. **어휘 검사이며 실제 검색을 실행한 수치가 아니다.**

중요한 반례는 기존 `cand_eb165802b276591084b42c4285daa130`다. `vanitas`라는 단어가 없어도 새 음식·시든 꽃·꺼진 촛불의 관계가 이미 들어 있다. 반대로 keyhole 일치에는 의복 구멍이 포함된다. 0건을 신규 필요의 근거로 삼거나, 이름이 있다고 의미 전체가 있다고 판단하면 둘 다 오류다.

28개 선택 CID의 전체 원문·intrinsic conditions/effects·binding을 [JSON 스냅샷](existing-source-mapping.json)에 보존했다. 재사용 우선 의미, 정제할 의미, 이 요청과 맞지 않는 이웃을 구분했다. 다만 실제 native 증거·role qualification·선택 branch의 전체 closure 검토는 하지 않았다. 구현 시 다음 결정으로 확정한다.

|결정|요건|
|---|---|
|reuse|기존 긍정 원문이 같은 물건·소유자·관계·현재 상태를 지원하며 조건/효과/역할도 맞음|
|refine|의미는 인접하지만 끝점·매체·분리 상태·재료 층위·번역·guard 적용이 불충분함|
|new|기존 source 전체를 대조해도 완전한 관계를 충족할 수 없음|
|context|존재하는 의미가 서사·비평·동의·권리·감각·시간이며 시각 프록시와 구별돼야 함|
|defer|원 대화 복원·원전·번역·상태/소유자·증거가 부족함|

`reject_neighbor`는 선택한 오탐의 연구 표시다. 실제 반영 결정에서는 부적합 이웃으로 제외하고 필요한 관계를 위 다섯 가지로 판단한다. 기존 항목 삭제를 뜻하지 않는다.

## 5. 한영 데이터 저술과 검증의 단위

`owner → property/part → directed relation → visible state`가 최소 단위다. 예를 들어 C01은 사람을 보는 시선 일반과 거울 반사 일반을 각각 등록하고 끝낼 수 없다. 실제 관찰자·거울 경계·반사·대응하는 실제 대상이 연결되어야 한다. F03은 신체 부분이 바깥에 있다는 사실만으로 부족하고 내부 구조·공동·분리 상태가 필요하다.

한영에는 같은 소유자, 물건 수, 매체, 위치, 연결/분리 상태, 현재 단계가 남아야 한다. `붉은 액체→blood`, `모발 로켓→mourning`, `단정한 성인→abusive spouse`, `청동 에코르셰→flayed victim` 같은 번역은 의미를 추가한다. 한영 초안은 이 원칙으로 저술했지만 **독립 번역 검토는 미실행**이다.

모든 가시 카드의 관계 gate는 양 끝점·소유자 연속성을 요구한다. `partial_is_fail`과 `UNOBSERVABLE_NOT_PASS`를 둔다. 이는 연구 평가 원칙이며 운영의 executable source effect/guard나 native proof를 자동 생성하지 않는다. 출처 링크도 빠진 source fact를 대신 지원할 수 없다.

## 6. 충분성·한계·다음 단계

이번 범위는 단어 나열을 넘어 가시 관계, 반례, 기존 원문, 반영 결정, 개발 평가 사례까지 연결했다. 원 대화 표의 189행은 모두 한 개 이상의 경로를 가진다. 22개 문맥 카드는 긍정 시각 후보를 만들지 않는다. 단어별 독립 사전 검증이나 원전 전문 61권 완독, 운영 품질 향상의 확인은 아니다.

Williams 원문 논증, 스플래터펑크·그랑담 기뇰의 세부 역사, 방 기능/건축 명칭의 개별 사전 대조, 역사적 성과학 용법과 현대 정의의 세부 대조, 한영 독립 검토가 남아 있다. 불확정 항목은 검증된 것처럼 승격하지 않고 source별 read_scope·limits로 남겼다.

실제 반영은 [구현 계획](IMPLEMENTATION-PLAN.md)의 원문 심사→별도 source 작성→격리 인덱스→실제 한영 검색→독립 이미지 비교→선택적 설치 순서로 진행한다. [장면 설계](SCENE-BLUEPRINTS.md)와 [픽셀 계획](PIXEL-PLAN.md)을 함께 사용한다. 이 문서를 생성하거나 구조 검사에 통과한 것은 그 후속 단계의 실행 증거가 아니다.
