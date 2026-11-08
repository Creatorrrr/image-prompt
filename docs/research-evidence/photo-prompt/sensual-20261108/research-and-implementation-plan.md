# Sensual 용어 기반 시각 의미 리서치와 반영 계획

조사일: 2026-11-08. 대상: [Sensual 용어 조사](https://chatgpt.com/c/6aeef5b5-a008-83ee-b9ff-96eeeed214c6)의 사용자 질문과 답변 및 첨부 용어집. 작업 범위는 리서치와 계획이다. 이 문서의 예시와 inventory는 실제 후보 팩, 인덱스, 정책, 모델 출력이 아니다.

## 1. 범위와 추적성

대화는 질문 1개와 응답 1개로, 도구의 응답이 잘려 Chrome에서 전체 답변과 첨부를 확인했다. [원본 첨부 스냅샷](source-glossary.md)의 SHA-256은 `67ed1545614b6d242b35420ae1209526378332faa58d5b32085c9f0d22a5ac3a`이다. [행 목록](term-inventory.csv)은 첨부 1~14절의 표 320행과 본문에 독립 행으로 나타난 `coy`, `languorous`, `over-the-knee boots` 3행, 총 323행이다. 이는 **행 수이지 서로 다른 개념 수가 아니다**. 슬래시로 병합된 항목은 분해가 남아 있고, 대화 본문은 일부를 별도 행으로 나눈다. 15절의 비교표·여섯 조합은 독립 키워드 수에 중복하지 않고 대조와 평가에 사용한다. 목록 전부의 출처와 기존 후보 대응은 아직 검토 전이며 기본 상태를 그렇게 표시했다. 본문과 첨부의 모든 문장 차이에 대한 자동 대조는 수행하지 않았다.

| 범주 | 원문 대응 범위 | 연구·구현 관점 |
|---|---|---|
| 1 의미 | sensual, sensuous, sensuality, allure, erotic 등 | 어휘 의미와 평가적 뉘앙스; 단일 외형·강도 사다리 금지 |
| 2 장르·분위기 | languid, boudoir, glamour, pin-up, burlesque, noir, nude 등 | 양식·서사·착의 상태를 분리; 시대·장소·전형은 선택적 |
| 3 얼굴 | 시선, 눈꺼풀, 입 모양, 해석적 표정 | 보이는 방향·형태와 분위기/의도를 분리 |
| 4 자세·동작 | 체중, 몸 방향, 기대기, 누움, 교차, 손, 춤 | 체중·지지점·신체 부위·이동의 순간 및 프레임 분리 |
| 5 외형 | 신체 윤곽·피부·헤어·메이크업 | 부위·형태·표면 마감·제작법 분리 |
| 6~9 복식 | 실루엣, 개방, 의복, 속옷, 파츠, 봉제 | 의복 유형·위치·범위·파츠 관계와 실제 가시성 분리 |
| 10~11 액세서리·소재 | 스타킹·신발·장갑·금속물·섬유·직물 | 치수·연결·재료·구조·표면·비침 독립 |
| 12 조명·감각 | 명암·광질·심도·색·소리·향 | 사진에 보이는 빛과 비시각적 소리·향의 단서 분리 |
| 13 페티시·BDSM | 관심·관계·역할·소품·동의 | 명시적 의미와 물체 외형 분리. 대화에서 요청한 범위를 임의로 누락하지 않음 |
| 14 인접 개념 | 관음, 강압, 폭력, 상처 분장, 고어 | 관점·사건·서사와 분장·질감·의상 손상 분리 |

## 2. 출처를 통해 확인한 내용과 설계상 결론

1. **뜻의 겹침과 차이.** [Cambridge sensuous](https://dictionary.cambridge.org/us/dictionary/english/sensuous)는 감각적 즐거움과 sensual과 겹치는 용례를 함께 제시한다. sensual/sensuous를 상호 배타적 분류나 단일 강도 척도로 취급하지 않는다. 단어 자체의 의미, 사용자가 의도한 성적 함축, 구체적인 시각적 선택은 각각 보존한다. `sensory`도 중립적 감각 영역을 가질 수 있다. 영어 `sultry`의 날씨 용례, `gore`의 브라 부품/손상 용례, `cuff`의 소맷단/구속구, `scene`의 장면/활동은 맥락별 뜻을 유지한다.
2. **역사적 의복을 범용 규칙으로 만들지 않는다.** [V&A Victorian underwear](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)는 특정 시대 코르셋의 앞중심 busk, 지지용 boning, 뒤 lacing을 구별한다. [Met의 18세기 busk](https://www.metmuseum.org/art/collection/search/84189)는 보이지 않는 단단한 목재 부품의 사례다. 따라서 busk가 항상 보이는 앞 잠금 장치라는 가정은 오류다. 시대·형식·공개 사진에서 보이는지와 출처를 별도로 둔다. [V&A underwear collection](https://www.vam.ac.uk/collections/underwear)은 보호·보온·형태 변경·노출 같은 여러 기능을 기록한다. 속옷을 단일 성적 의미나 특정 신체 형태로 고정하지 않는다.
3. **재단과 결과를 구별한다.** [Met의 Vionnet 드레스](https://www.metmuseum.org/art/collection/search/158999)는 bias cut과 천의 유연한 흐름, 등 쪽 절개 및 드레이프의 특정 사례다. 사진에서 보이는 주름만으로 직물의 재단 방향을 입증할 수 없으며, 카울넥·bias cut·draping을 동일한 개념으로 합치지 않는다. [Met의 Galliano 드레스](https://www.metmuseum.org/art/collection/search/762084)는 이 계열 실루엣의 역사적 재해석을 보여 주는 특정 사례이지 모든 slip dress의 필수 형태는 아니다.
4. **신체 균형과 움직임.** [National Gallery contrapposto](https://www.nationalgallery.org.uk/paintings/glossary/contrapposto)는 몸의 각 부분이 서로 반대 방향으로 균형을 이루는 원리를 설명한다. `weight shift`만 발견되면 지탱 다리와 어깨·골반 관계가 명확하지 않을 수 있다. `S-curve`와 개념을 연결할 수 있어도 동의어로 합치지 않는다. 단일 프레임에서 `body roll`의 전체 시간적 순서를 입증하기 어려우므로 움직임의 이름과 한 순간의 자세를 구분한다.
5. **광질·대비·색·심도.** [Adobe Lightroom의 빛 설명](https://lightroom.adobe.com/academy/genres/food/love-the-light)은 soft light가 방향성을 가질 수 있고 광원의 상대 크기가 그림자 경계에 영향을 줌을 설명한다. `soft=어둡다/그림자 없다`, `hard=밝다`로 고정하지 않는다. [National Gallery chiaroscuro](https://www.nationalgallery.org.uk/paintings/glossary/chiaroscuro)와 [tenebrism](https://www.nationalgallery.org.uk/paintings/glossary/tenebrism)은 관련되지만 후자는 주로 어두운 화면의 제한된 부분을 부각하는 별도 용례다. [Nikon의 심도 설명](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/what-is-aperture)과 [bokeh 설명](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/bokeh-for-beginners)에 따라 얕은 심도는 선명한 거리 범위, bokeh는 흐려진 영역의 성질로 분리하며 점광원 원형을 필수로 두지 않는다. 광원·렌즈 수치와 후처리 여부는 사진의 외형만으로 단정하지 않는다.
6. **패션 맥락의 다의성.** [Museum at FIT의 Sheathed in Sex](https://exhibitions.fitnyc.edu/power-mode/sex/)는 의상과 힘·성적 의미의 관계를 전시 맥락에서 다룬다. [FIT Gothic: Dark Glamour](https://www.fitnyc.edu/museum/exhibitions/gothic-dark-glamour.php)는 고딕을 패션과 문화의 범주로 살핀다. 코르셋·하네스·검은색·가죽은 단독으로 특정 관계·취향·동의의 증거가 아니다. 핀업·벌레스크·카바레는 역사와 수행 맥락이 다르며 한 포즈나 노출량으로 정의하지 않는다.
7. **관계의 지식과 관찰 가능성.** [NCSF Consent Counts 용어집](https://ncsfreedom.org/wp-content/uploads/2019/12/Consent-Counts-Statement.pdf)은 top/bottom의 행위 역할과 D/s 관계를 구별한다. [NCSF의 동의 정책 예시](https://ncsfreedom.org/wp-content/uploads/2021/07/SAMPLE-Consent-Policy-Kink.pdf)는 몸짓이나 과거 행동으로 동의를 판정하지 않도록 한다. 이는 해당 단체의 정책 예시이며 모든 공동체의 유일한 운영 규칙이라는 주장은 아니다. 관심·역할·사전 협의·동의는 이미지 단서와 분리된 맥락으로 기록한다. 구속구·시선·상처 분장·찢어진 옷을 보고 원인·권력관계·실제 피해를 역추론하지 않는다.
8. **관찰의 한계.** [Smithsonian 사진 자료 읽기](https://americanhistory.si.edu/sites/default/files/PrimarySources.pdf)는 사진의 프레임과 촬영자 선택 및 외부 맥락의 중요성을 설명한다. 직물의 화학적 재료, 보이지 않는 안감, 동작의 전체 경과, 향·목소리·의도·동의는 사진 한 장에서 일반적으로 판정할 수 없다. `미관찰`은 `없음`이나 `실패`와 다르다. 명시적 요청·신뢰할 만한 별도 자료로 알려진 사실과 픽셀에서 확인되는 사실을 나눠 유지한다.

원문이 인용한 브라 구조의 Wacoal과 새틴의 CottonWorks는 이번 도구에서 각각 접근 오류/403이었다. 원문의 표기와 기존 인용이 그 세부 정의를 새로 검증한 증거가 되지는 않는다. 브랜드별 bra, 고정 스타킹, 재료 표면, 메이크업, 향·소리 및 일부 장르·비시각 항목은 개념별 직접 출처를 추가해야 한다.

## 3. 시각 의미 모델: 각 축을 조합 가능하게

아래 필드는 연구 설계 제안이며 현재 엔진이 모두 이해하는 스키마라는 뜻이 아니다.

- **의미·용례:** `term_id`, 원문 섹션/행/표현, 정확한 언어별 표기, `sense_id`, 정의, register, 시기·문화·분야, 좁은 동의어, 인접어·구별, 직접 근거와 근거 범위, 검토 상태. `glamour`의 영어 뜻과 한국어 통용 의미를 섞지 않는다.
- **가시 형태:** 인물·의복·소품의 소유자, 신체/의복 부위, 형태, 방향, 길이, 범위, 접촉점, 겹침, 비침, 광택, 표면 패턴, 시선 대상, 프레임과 가림. 다른 인물의 옷이나 손과 잘못 결합하지 않도록 owner를 표시한다.
- **재료의 계층:** `fiber= silk/spandex`, `weave=satin`, `surface_structure=velvet pile/mesh/lace`, `material=latex/PVC/leather`, `finish=patent/wet-look/matte`, `transparency=sheer/opaque`로 개념 종류를 분리한다. 실제로 조합 가능한 예와 불확실한 관찰은 별도다. `wet-look`은 실제 젖음이 아니다.
- **구조와 관계:** `overbust`/`underbust`의 수직 범위, `cup`/`center gore`/`underband`/`wings`와 연결, `eyelet`-`lacing`의 통과, `garter strap`-`clip`-`stocking top`의 연결, 허리 높이와 leg opening 높이를 독립 축으로 기록한다. 실체의 존재와 사진에서 보임은 별도다.
- **스타일·정서와 매체:** `sensual`, `intimate`, `sultry`, `noir`, `fetishwear`, `implied nudity`, `erotica`를 동일한 라벨 축에 넣지 않는다. 각 개념은 분위기·관계·미학·의복·시점·매체 성격 중 자신의 종류를 가진다. 하나의 관능적 느낌에 특정 체형, 성별, 포즈, 조명, 노출을 기본값으로 강제하지 않는다.
- **맥락과 근거의 경계:** 후각·음성·기능·역사·취향·관계·동의·진단은 근거에 따라 맥락에 저장하고, 눈에 보이는 예시는 가능할 때 별개로 둔다. `미상`, `가려짐`, `해당 없음`, `명시된 비가시 사실`은 구별한다. 단순한 메타데이터나 검색 별칭은 생성 요구 또는 native 승인 권한이 아니다.

## 4. 후보 작성 및 대조 예시

아래는 본 연구에서 작성한 **선택적 후보 원형**이다. 각 표현은 개념의 유일한 정의가 아니며 이미지 검증 전이다. 각 후보는 한국어·영어로 독립적으로 완결되고, 요청과 source에 맞는 소유자·관계·가시성 조건을 가질 때만 검토한다.

| 대상 | 하나의 시각적 실현 예 | 확인 조건과 혼동 대조 |
|---|---|---|
| Contrapposto | 서 있는 성인의 한쪽 다리에 체중이 실리고 골반과 어깨의 기울기가 서로 다르게 보인다 | 발·골반·어깨가 보일 때 검토; 단순한 세로 S자와 동의어 아님 |
| Half-lidded/direct gaze | 눈꺼풀이 일부 내려온 눈이 렌즈를 향한다 | 눈꺼풀 형태와 시선 대상 둘 다 보여야 함; 감정 증거 아님 |
| Over-shoulder | 몸통은 옆으로 향하고 얼굴은 어깨 너머 카메라 쪽을 향한다 | 얼굴·어깨·몸통 방향이 보임; 길이·샷 크기는 독립 |
| Back lacing | 의복 뒤쪽 두 가장자리의 구멍을 끈이 교차해 연결한다 | 뒤쪽·두 가장자리·끈이 보여야 함; lace 원단과 구별 |
| Bra anatomy | 두 컵 사이의 앞중심 연결부와 컵 아래 밴드가 보인다 | 컵·연결부·밴드가 보임; `gore`의 손상 의미와 구별 |
| Stocking support | 허리쪽 스트랩 끝 클립이 별도 스타킹의 윗단에 연결된다 | 스트랩·클립·윗단·착용자가 모두 보여야 함; thigh-high 자체가 가터 고정을 뜻하지 않음 |
| High waist/high cut | 하의의 허리선이 높고 다리 개구부도 골반 위쪽으로 올라간다 | 두 경계를 각각 판정; 한 축만 요청되면 다른 축 강제 금지 |
| Satin / velvet | 한 의복의 넓고 부드러운 반사 띠와 다른 직물의 방향에 따라 달라지는 파일 음영이 나란히 보인다 | 실제 섬유 성분은 별도 출처 필요; 반사만으로 소재 확정 금지 |
| Sheer panel | 불투명 몸판 사이의 비치는 패널을 통해 아래층의 색과 경계가 보인다 | 패널 경계와 아래층이 보임; mesh/lace 무늬를 필수로 추가하지 않음 |
| Lip/face | 입술 사이에 작은 틈이 있고 턱이 자연스럽게 놓여 있다 | 입술의 외형만; 욕망·의도·호흡의 증거 아님 |
| Lighting | 측면 창 방향의 부드러운 빛이 얼굴에 완만한 그림자 경계를 만든다 | 광원 방향과 그림자 경계 분리; 광량이나 색온도 강제 금지 |
| Framing | 전경 문틀 일부가 인물을 둘러싸는 화면 | 문틀·인물의 상대 위치 확인; 실제 무단 관찰을 뜻하지 않음 |
| Fetishwear | 스트랩이 어깨와 몸통을 가로질러 금속 고리에서 만난다 | 위치·연결부가 보임; 관심·관계·구속을 자동 생성하지 않음 |
| Injury SFX | 의상 표면에 붉은 얼룩이 있고 피부에는 멍처럼 보이는 분장이 있다 | 픽셀은 색·형태만 확인; 실제 부상이나 사건의 원인은 별도 |

검색의 진단 쌍은 `sensuous/sensual/sensory`, `languid/sultry`, `gore/center gore`, `cuffs/shirt cuffs`, `thigh-high/stay-up/garter`, `high-waist/high-cut`, `busk/lacing`, `lace/lacing`, `silk/satin`, `latex/PVC/wet-look`, `soft/hard light`, `chiaroscuro/tenebrism`, `shallow DoF/bokeh`, `consent/visible pose`, `voyeuristic framing/voyeurism`을 포함한다. 같은 현상에 맞는 복수 후보와 가려져 판단할 수 없는 후보도 정답 집합에 포함한다.

## 5. 현재 프로젝트 확인

2026-11-08 점검에서 `assets/photo_candidate_corpus_manifest.json`은 172개 모듈을 가리키며 누락 파일은 없었다. 후보 모듈에서 28,546개 후보를 읽어 [20개 용어의 단순 어휘 스크린](lexical-screen.csv)을 만들었다. 예를 들면 `sensual` 2, `corset` 98, `satin` 139, `gore` 40, `coercion` 238이다. 후보 content의 EN/KO/definition/aliases에서 정확 영어 문자열 경계를 찾은 수치이며 중의어·부정문·템플릿·중복을 포함한다. `finger waves`나 `sensuous`가 0이라는 것은 철자 변형이나 의미상의 부재가 아니라 이 검색 조건의 미일치다. 샘플 CID는 수동 대조의 시작점이지 정답이 아니다. 사용자 요청 전체의 검색 재현율이나 후보 품질은 측정하지 않았다.

실제 후보는 `photo-candidate-module/v3`의 `candidates`에 `content`, `conditions`, `effects`, `provenance` 등을 두고 별도 `photo-candidate-slot-bindings/v3`가 연결된다. 코스프레 후속 예시에서는 의미 카드와 context-only 파일이 별도로 존재하고 후보에 `research_semantics`와 `application_contract`도 담긴다. 따라서 제안한 연구 필드를 파일에 적는 것과 검색·표시에 실제로 쓰이는 것은 다르다. 코드의 로더, release 빌더와 표시 경로를 확인해 각 필드의 소비 여부를 검증해야 한다. 특히 context view는 파일 존재만으로 활성 검색이나 표시에서 사용된다고 가정하지 않는다.

설치 runtime 점검은 `pass`; H-F2 generation `05eeb9e7620231c6911d559ec159f86189bf0fc90ec198cd41258f718ea0d604`, native `7bf18c2e1c9c248095c3dcd8c5dccf8ad6ccfb5b25c6b7692819109a1242b4f1`이다. 점검 범위는 dependencies와 installed recorder이며, 현 소스와 설치 릴리스의 일치, 이번 용어 검색, 시각적 품질을 보증하지 않는다. 작업 시작 시 다른 작업의 대규모 변경·삭제가 이미 있었으므로 이 조사에서는 이들을 변경하거나 복구하지 않았다.

## 6. 빠짐없이 반영하기 위한 단계별 계획

1. **원문 대조와 개념 분해.** 323행 각각을 추적하고 슬래시·혼합 의미를 `parent_row_id + sense_id`로 분해한다. 대화 본문과 첨부의 차이, 본문에서 개별 행으로 나뉜 항목, 15절 비교·조합을 상호 참조한다. 중복 개념은 ID를 합치되 원문 포인터는 모두 보존한다. 사용자 의도상 요청된 범주는 빠뜨리지 않되 현 단계에서 `visual`, `context`, `both`, `needs_review`는 수동 확정한다. 소리·향·관계처럼 시각적 단서가 제한되는 항목도 삭제 대신 근거와 상태를 둔다. 행 수·분해 수·중복 수·미처리 수를 검산한다.
2. **개별 근거 검토.** 의미별로 사전·박물관·전문기관·제작자의 직접 출처를 확보하고, 정확히 입증한 속성과 언어/시대/상품별 불확실성을 기록한다. 위 2절의 출처는 관련 범주 전체에 일괄 상속하지 않는다. 찾지 못한 항목은 `needs_evidence`와 필요한 증거를 명시한다. 원문만이 출처인 항목을 독립 검증 완료로 보지 않는다.
3. **전체 기존 자산 대조.** 각 뜻/속성별로 관련 기존 CID, RID, content, conditions, effects, application contract, bindings, provenance와 현재 검색 뷰를 열어 `exact`, `partial`, `conflict`, `absent`, `unresolved` 판정과 근거 포인터를 남긴다. 단순 문자열 일치만으로 `exact`라 하지 않는다. 이미 충분한 후보는 연결해 중복 증식을 피한다. 소유자 관계와 동일 CID 내 realization 차이를 개별 검토한다.
4. **의미·후보·맥락·검색 레이어 작성.** 개념의 정의와 경계는 연구 registry, 시각적으로 선택 가능한 완결 명제는 candidate와 optional binding, 불가시적 의미는 provenance가 있는 context-only view에 둔다. 검색 alias/paraphrase는 기존 CID의 실제 의미에 맞는 것만 기록한다. source 조건과 application contract를 누락하지 않으며 제안된 metadata가 인덱서에 실제로 읽히는지 검증한다. 연구 맥락은 native 자격이나 자동 채택 권한을 주지 않는다. 의미/후보/context 각각 별도 검증, ID 충돌·dangling reference·source hash를 검사한다.
5. **현 release를 기준으로 고정 평가.** 기존 활성 generation과 manifest, 모델·설정·동시 변경을 고정하고 기존군 및 새 질의를 사전 작성한다. 각 세부 범주에서 EN/KO·별칭·직접 요청·유사어·복합 질의·명시적 배제·소유자 2명·가림/미상·비시각 의미 사례를 포함하고 적합·부적합·판단불가와 이유를 평가 전에 동결한다. 개발에 사용한 질의와 별도 보류 질의를 분리한다. 기준선이 충분히 성공하는 사례도 포함하여 과잉 변형을 본다.
6. **인덱스와 회귀.** 소스 스냅샷의 provenance·해시를 봉인하고 프로젝트가 실제로 사용하는 H-F2 파이프라인으로 비활성 generation을 빌드한다. 동일 코퍼스 설정과 질의로 baseline/new를 비교하고, 가능한 경우 lexical/dense/hybrid와 실제 최종 결과를 따로 기록한다. Recall@K, MRR/nDCG, 충돌·오탐·제외 위반, 지연과 크기를 측정한다. global 검색 및 실제 qualification 조건을 유지하고 기존 주제 회귀도 본다. 실패와 미해결은 변경 내역에 남긴다.
7. **설치와 별도 이미지 평가.** 소스·manifest 동시 변경 여부, 현재 활성 포인터, 이전 release 복구 방법을 재확인한 뒤 비활성 generation으로 런타임 테스트한다. 활성화 여부는 해당 작업 범위에서 별도로 결정한다. 설치 성공은 retrieval 성공과 구분한다. 이미지 비교는 별도의 고정된 요청·제어 값·모델 조건에서 수행하고 각 부위의 보임/가림/오류, 선택 편향·거절·반복 수를 기록한다. 전체 prompt 작성, 사용자 채택, 픽셀의 실제 개선과 인과적 기여는 서로 다른 판정이다.

### 수용 기준과 미해결

모든 원문 행은 분해 또는 중복 관계와 최종 처분을 가지며, 각 개념은 관련 직접 근거 또는 보류 이유, 기존 CID/RID 대조 결과, 적용될 레이어가 있어야 한다. 데이터 무결성 및 검색 회귀 기준은 평가를 시작하기 전에 정하고, 실패 시 개선 없이 통과로 기술하지 않는다. 이미지 개선 주장은 별도의 대조 실험과 관찰 결과가 있어야 한다.

현재 완료한 것은 원문과 첨부 확인, 323행 추적 목록, 범주별 출처 조사, 20개 표본의 어휘 스크린, 스키마·runtime 기초 확인과 구현 계획이다. **행별 독립 출처 검증, 본문-첨부 완전 자동 대조, 개념 분해, 기존 후보의 의미적 전수 대조, 새 데이터/인덱스 제작, 검색 회귀 및 이미지 비교는 미완료다.** 기존 `fashion-visual-semantics-research-plan-20261108.md`는 관련 연구이나 해당 문서의 비-BDSM 범위를 이 요청에 적용하지 않는다.
