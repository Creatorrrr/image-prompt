# 지적 인상·탐구 활동의 시각 의미와 후보 데이터 연구

조사일: 2026-10-05. 대상: 원 대화 「용어 조사 정리」의 **140개 용어**. 결과 상태: **연구·반영 설계 완료, 런타임 미반영, 이미지 미생성**.

## 연구 결론

가장 우선할 보강은 지적 분위기의 형용사나 안경·책 소품을 더 붙이는 일이 아니라 **인물의 손·시선이 특정 자료에 연결되고, 자료 사이의 같은 항목이 대응하며, 도구가 실제 접점을 갖는 의미 데이터**다. 기존 포즈·표정·촬영 데이터에는 재사용할 원자가 상당수 있지만, 이 원자를 모았다고 정독·교정·분석·검토라는 작업 관계가 자동 성립하지는 않는다.

따라서 반영을 세 층으로 설계했다.

1. **어휘와 주장 범위:** 18개 인상 형용사, 시간적 개념, 문화·성인·허구 표현을 관찰 형태와 분리한다. 추상 단어는 선택적 연출 문맥으로 쓰고 하나의 표정·의복을 필수화하지 않는다.
2. **형태·접촉·참조 관계:** 기존 원자를 재사용하고 페이지 고정, 펜의 비접촉, 안경의 상태, 문서 앵커, 비교 기준, 도구 접점을 세분화한다.
3. **활동 묶음과 구성:** 정독·판본 대조·교정·디버깅·분석 등은 인물–자료–기록의 연결을 갖는 선택적 후보로 구성한다. 사용자가 명시한 비대체적 관계만 정확한 소유자와 범위에 결속하여 required 의미로 검토한다.

**140개의 키워드가 140개의 새 후보나 프로파일을 뜻하지 않는다.** 이 패키지는 기존 후보 ID 60개와 프로파일 7개를 재사용 검토 대상으로 보존하고, 78개의 관계·구성 단위를 초안으로 제안한다. 78개 안에는 기존 항목의 좁은 변형, 관계 보강, 조합 제안이 함께 있으며 최종 증분 수량은 중복 제거와 효과 검토 후 결정한다.

## 조사 범위와 근거의 성격

원 대화는 `read_thread`의 캐시 응답이 20,000자에서 잘려 140개 전체를 얻지 못했다. 이미 열려 있던 원 대화의 Chrome 표에서 140행을 확인하고 뒤쪽 항목을 보완했다. 원 대화의 정의와 연출 제안은 [SOURCE-KEYWORDS.json](SOURCE-KEYWORDS.json)에 따로 보존했다. 원 대화의 제안을 검증된 사실로 취급하지 않았다.

외부 근거 **46개**는 사전 18개와 미술관·연구자·대학교·촬영 실무자·방법 문서·문화 기사 등 28개다. 읽기 상태는 본문 열람 34개, 연결된 사전 뜻 열람 3개, PDF 텍스트 열람 2개, 검색 발췌 6개, 검색 발췌 확인 후 본문 열람 실패 1개다. 상태·지원 주장·한계를 [SOURCES.json](SOURCES.json)에 기록했다. 기관의 원본 작품 픽셀을 계측하거나 별도 이미지 데이터셋을 수집한 연구는 아니다.

아래의 ‘제안’은 근거에서 뒷받침되는 뜻·원리·사례를 바탕으로 **이번 연구가 저작한 장면 설계**다. 예를 들어 NIST의 산점도 설명은 변수·관측의 관계를 뒷받침하지만, 성인이 펜으로 A=(2,3)을 가리키는 구체 장면 자체를 검증한 실험은 아니다. 어휘 근거, 장면 제안, 기존 데이터, 런타임 노출, 최종 이미지 결과를 각각 기록한다.

## 현재 데이터에서 확인한 것

현재 체크아웃의 generator에 등록된 authored 파일 **83개**를 한 번씩 읽어 후보 `(slot,id)` **9,949개**, 프로파일 레코드 **1,774개**를 조사했다. 그 시점의 HEAD·dirty 상태·파일 해시는 [CHECKOUT-SNAPSHOT.json](CHECKOUT-SNAPSHOT.json)에 있다. 공유 체크아웃에는 다른 작업의 수정이 있어 구현 착수 시 다시 대조해야 한다.

NFKC·casefold 후 원 대화의 라벨과 positive 라벨·별칭·키워드를 **동일 문자열로 비교**하면 후보 라벨이 맞는 용어는 22/140, 프로파일의 exact 라벨이 맞는 용어는 0/140이다. 이 수치는 의미 충족률·검색 recall·후보팩 노출률이 아니다. 언어 표현이 달라도 이미 충분한 원자가 있을 수 있고, 같은 단어여도 다른 의미일 수 있다. [EXISTING-COVERAGE.json](EXISTING-COVERAGE.json)에 비교법과 원 레코드를 보존했다.

| 조사 사례 | 확인한 데이터 | 보강 방향 |
|---|---|---|
| 손끝 맞대기 / 손깍지 | `pv_steepled_fingers`, `pv_interlaced_fingers`에 손 형태·소유·연속성 존재 | 재사용. 지능·권력·책략 별칭을 손 원자에 추가하지 않음 |
| 턱 지지 / 읽기 | `pv_chin_support`, `pv_book_read`에 지지와 동작 구성 존재 | 엄지–턱 아래·검지–뺨 변형, 페이지 앵커, 시선–행 관계 추가 검토 |
| 입술 압착 / 오므림 | `ae_lip_press`, `ae_purse`, `ae_pucker`가 별도 형태 | 원 대화의 혼합 설명을 나누고 유사어를 무차별 교차 등록하지 않음 |
| Reflective | 반사 금속·거울 재료와 exact 문자열 충돌 | 성찰 문맥과 반사 재료 문맥을 다른 뜻으로 처리 |
| Three-quarter view | 광대 전방 돌출 형태가 라벨 일치에 잡힘 | `camera_direction`의 `eye_level_three_quarter` 재사용. 해부 형태를 각도로 활성화하지 않음 |
| 어깨너머 / 환경 초상 | portrait 원자에 실제 어깨 소유·장소 구성 존재 | 인물 수·공유 문서·손 접점·크롭 관계를 추가 검토 |
| 반사 레이어 | `window_reflection_layering`은 추상 라벨, 별도 배경 후보에는 반사·투과 의미 존재 | `rb_glass_reflection_transmission_candidate` 재사용과 문서 참조 결속 |
| 렘브란트 광 | `rembrandt_face_light_pattern` 프로파일 존재 | 새 조명 ID 중복 대신 작업 자료 가독성을 함께 보존 |
| 칠판 설명 | `teaching_at_blackboard`는 넓은 동작 라벨 | 손의 지시 끝–특정 보드 노드–청자 지향 연결 |

후보 이름이 그럴듯하거나 `concept_units`가 있다는 이유만으로 데이터가 충분하다고 판정하지 않았다. 실제 소유자·접촉·관계·효과·문맥을 [TERM-DECISIONS.json](TERM-DECISIONS.json)의 재사용 레코드에 연결했다.

## 1. 지적 인상을 만드는 어휘: 의미를 보존하되 형상을 강제하지 않기

1–18번은 서로 바꾸어 쓸 단순 동의어가 아니다. 예를 들어 **reflective**는 생각과 빛 반사의 뜻이 공존하고, **introspective**는 자기 생각·감정을 살피는 뜻이며, **pedantic**은 세부·학식을 과도하게 내세우는 비판적 함의를 갖는다. **measured** 역시 신중한 대응과 실제 측정 문맥을 나누어야 한다. [Merriam-Webster: reflective](https://www.merriam-webster.com/dictionary/reflective), [introspective](https://www.merriam-webster.com/dictionary/introspective), [pedantic](https://www.merriam-webster.com/dictionary/pedantic), [measured](https://www.merriam-webster.com/dictionary/measured).

데이터 설계에서는 뜻과 연출 선택을 분리한다. ‘분석적’에 비교표를 제안할 수 있지만 비교표를 필수화하거나 분석 능력을 판정해서는 안 된다. ‘교수풍’에 자료를 가리키는 자세를 제안할 수 있지만 나이·성별·트위드·교수 직업을 강제하지 않는다. 지적 사고를 강조하는 `cerebral`이라는 말만으로 관능적 의상을 삭제하거나 얼굴을 무표정으로 만들지도 않는다.

책·안경은 문화적 연상 요소일 수 있지만 능력의 측정값은 아니다. 학자의 역사적 초상에서도 책을 든 Erasmus와 Homer 흉상에 손을 놓은 Aristotle처럼 상징 조직이 다르다. 이 사례는 연출의 다양성을 넓히는 참고이며 실물 인물의 지능을 평가하는 자료가 아니다. [National Gallery: Erasmus](https://www.nationalgallery.org.uk/paintings/hans-holbein-the-younger-erasmus), [Met: Aristotle with a Bust of Homer](https://www.metmuseum.org/art/collection/search/437394).

반영: 18개를 일괄 표정 slot으로 추가하지 않는다. 뜻·문맥의 어휘 레코드와 선택 가능한 활동 묶음을 연결한다. `positive definition / paraphrases / components`에는 실제 뜻과 형상을, 혼동·정체성 추론 한계에는 별도 필드를 사용한다.

## 2. 사유 포즈: 접촉을 가진 지지 사슬

19–36번의 핵심은 ‘생각하는 포즈’라는 이름보다 **무엇이 무엇을 받치는가**다. 턱 괴기는 손–턱 접촉에 더해 팔꿈치 또는 전완의 받침이 필요하고, 교차 지지는 받치는 전완–반대 팔꿈치–그 손–턱이 하나의 사슬이다. 페이지 고정과 페이지 모서리 들기 역시 책과 종이의 지지·연결이 다르다. 이 구체 사슬은 이번 연구의 형태 설계다.

국립중앙박물관의 반가사유상 설명은 오른발–왼 무릎, 오른손 손가락–뺨 관계를 명시한다. 이 중립 기하와 불교적 도상은 별도 층이다. [Pensive Bodhisattva 소장 설명](https://www.museum.go.kr/ENG/contents/E0201070000.do?relicId=17730&schM=view&showHallId=631120).

로댕형 자세는 작품 맥락을 참고하되 ‘Thinker’라는 말만으로 누드나 조각 매체를 강제하지 않는다. 이 패키지의 반대 허벅지–팔꿈치–턱 조합은 원 대화의 연출 분해를 저작된 지지 관계로 구체화한 것이며, 이번 조사에서 작품 원본 관절 좌표를 직접 검수한 것은 아니다. [Musée Rodin: The Thinker](https://www.musee-rodin.fr/en/musee/collections/oeuvres/thinker).

우선 보강할 미시 관계는 다음과 같다.

- **펜:** hover는 펜 끝과 종이의 간격, 필기는 실제 접촉. 동일 순간·동일 손에 둘을 모두 요구하지 않는다.
- **페이지:** margin press, corner pinch, page-root attachment를 나눈다. 본문 가림은 별도 크롭·가림 제약이다.
- **안경:** 착용 / 벗어 듦 / 브리지 접촉 / 프레임 너머 시선은 물체 상태·접점·시선 관계가 다르다. 원한 프레임 디자인을 보존한다.
- **좌우·소유:** 한 인물의 양손, 다른 두 인물의 손, 오른발–왼 무릎은 독립 binding이다. 좌우를 없애거나 손을 늘려 해결하지 않는다.

## 3. 설명 몸짓과 얼굴: 시간·문맥을 형상과 분리

37–42번의 도상·은유·지시·비트는 배타적인 네 클래스보다 **겹칠 수 있는 차원**으로 다루는 편이 근거에 맞다. 비트는 발화와 시간적 강조 관계를 가지므로 단일 열린 손 스틸을 성공 증거로 쓸 수 없다. 실제 지시도 검지뿐 아니라 몸이나 도구로 할 수 있다. 이 연구는 후보팩에 유용한 ‘문서 특정 노드를 펜으로 가리키는’ 좁은 변형부터 제안한다. [McNeill: Gesture, pp. 3–4](https://mcneilllab.uchicago.edu/pdfs/gesture.a_psycholinguistic_approach.cambridge.encyclop.pdf).

43–60번은 국소 얼굴·눈 방향과 실제 이해·알고 있음·엄정함의 평가를 분리한다. 눈썹의 한쪽 상승, 미간 접근, 입술 압착은 기술 가능한 형태다. ‘이해의 미소’나 ‘알고 있다는 듯’은 문맥에 둔다. FACS는 관찰 가능한 얼굴 움직임을 기술하는 방법으로 참고하되, 이 조사에서 매뉴얼 전체나 코더 인증을 확인하지 않았으므로 임의 AU 번호·지능 분류를 붙이지 않는다. [FACS 공식 설명](https://www.paulekman.com/facial-action-coding-system/).

위를 보는 눈을 회상·거짓말의 코드로 쓰지 않는다. 해당 방향과 기만을 연결하는 특정 NLP 주장에 대해 세 연구가 근거를 찾지 못했다는 원 논문을 확인했다. 이를 ‘모든 시선과 모든 인지가 무관하다’는 주장으로 확대하지도 않는다. [Wiseman et al., 2012](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0040259).

단일 이미지에서 검증을 보류할 명확한 시간 개념은 비트 몸짓(40), 발견 전환(57), 자료–화자의 시선 교대(59), 랙 포커스(82)다. 반추·걷다가 멈춤·무표정한 재치·산책 중 사유는 스틸 종점을 연출할 수 있어도 반복·이전 사건·발화 내용을 입증하지는 못한다.

## 4. 촬영·구성·광학: 작업 증거가 보이는 프레임

61–84번은 카메라 높이·방향·숏 크기·주관 시점·인원 수·깊이 배치·초점 상태를 나누어야 한다. `three-quarter view`는 얼굴 방향이고 `three-quarter length`는 크롭이다. 어깨너머 숏은 전경 어깨 소유자와 그 너머 주체를 필요로 하므로, 1인 고정 요청에 동료를 추가하는 후보로 사용할 수 없다. POV는 눈 위치 부근의 시점이며 관찰자 얼굴 전체를 자동 추가하지 않는다. [Yale: Cinematography](https://filmanalysis.yale.edu/cinematography/).

삼분할·유도선·여백은 선택한 의미 앵커를 보이게 하는 구성 수단이다. 예를 들어 look room은 현재 시선 방향과 같은 쪽 공간을 남기는 연구 단위로, 일반적인 빈 공간과 구별한다. 얼굴–손–자료 삼각 배치는 이번 저작 구성명이며 표준 용어라고 주장하지 않는다. [Adobe: composition](https://www.adobe.com/creativecloud/photography/discover/photo-composition.html), [leading lines](https://www.adobe.com/creativecloud/photography/discover/leading-lines-photography.html).

이번 후보 설계는 **깊이 배치와 선명도 규칙을 따로 보관**한다. 전경 손·중경 얼굴·후경 보드가 있으면 깊이 배치는 성립할 수 있다. 그 세 층의 필수 상세가 모두 읽혀야 한다는 요청은 별도의 deep-focus 의무다. 얕은 초점이 고정된 상태에서는 필수 얼굴·접점·자료를 가능한 가까운 초점면에 배치하거나 충돌을 알려야 한다. `f/숫자`와 조명 이름은 원본 픽셀의 성공 판정이 아니다. [Yale: Mise-en-scène](https://filmanalysis.yale.edu/mise-en-scene/), [Cinematography](https://filmanalysis.yale.edu/cinematography/).

반사 장면은 실물 인물, 그 인물의 반사상, 유리를 투과해 보이는 자료, 유리 면의 위치를 나눈다. 반사 얼굴을 추가 실제 인물로 세거나 무작위 이중 얼굴을 만드는 것으로 만족하지 않는다. 이는 기존 배경의 반사·투과 의미를 작업 참조 관계에 결속하는 제안이다.

## 5. 조명·의상·소품: 독립 축과 자료 가독성

85–96번에서 로키는 단순 검정, 하이키는 흰 종이의 날림이 아니다. 화면 속 스탠드와 가까운 화면은 각각 광원 위치·조사 면의 관계를 가져야 한다. 렘브란트 광은 어두운 쪽 뺨의 빛 삼각형과 코·뺨 그림자의 연결로 점검하고, 카메라 쪽 얼굴의 broad/short 면적과는 분리한다. [Yale: 조명 구성](https://filmanalysis.yale.edu/mise-en-scene/), [Profoto / Hannah Couzens: Rembrandt light](https://www.profoto.com/bg/en/still-photography/tips-tricks/how-to-create-rembrandt-light/).

셔츠·니트는 실제 두 층의 칼라·목둘레·커프스 경계, 팔꿈치 패치는 소매의 특정 부위에 붙은 별도 면이다. 트위드 직물은 재질, 패치는 의복 구조, 교수풍은 문화적 연출 문맥으로 분리한다. Harris Tweed의 지역·생산 조건을 일반 직물의 픽셀만으로 추론하지 않는다. [Harris Tweed Authority: weaving 설명](https://www.harristweed.org/journal/word-of-the-week-greasy-and-woven-tweed/).

프레임·하이넥·절제된 팔레트는 선택적 모습이다. 이들을 지능·직업·성적 지향의 판정 속성으로 넣지 않는다. 밝은 얼굴을 만들기 위해 필수 화면 텍스트를 날리거나 안경 반사로 눈 방향을 가리는 후보 역시 다른 required 의미를 훼손할 수 있다.

## 6. 가장 큰 보강 축: 자료의 흔적과 실제 작업 관계

97–124번은 아래의 반복 가능한 구조로 다듬는 것이 유효하다. 장면마다 많은 소품을 늘리기보다 **소수의 정확한 대응**을 먼저 만든다.

| 활동군 | 필요한 관찰 단위 | 주요 실패·추가 근거 |
|---|---|---|
| 정독·주석·판본 비교 | 원문 행, 밑줄, 여백 주석, 두 판본의 같은 문단, 손·눈의 target | 책만 병치하거나 낙서를 늘리는 경우. 독서 기록의 역사 사례는 [Darwin notebooks](https://www.darwinproject.ac.uk/people/about-darwin/what-darwin-read/darwin-s-reading-notebooks) 참고 |
| 교정·유도 | 페이지 지지, 펜 접촉, 취소선–대체어, 전후 식의 연결 | pen hover와 실제 writing 혼동. 처음에는 `x+3=7 → x=4`처럼 독립 검증 가능한 짧은 fixture |
| 디버깅 | 같은 파일·행의 코드와 traceback, 조사 중인 상태, 입력 손 | 코드 화면만으로 디버깅 판정. [Python errors](https://docs.python.org/3/tutorial/errors.html), [pdb](https://docs.python.org/3/library/pdb.html)로 파일·실행 위치의 대응 설계 |
| 데이터 분석 | 같은 관측의 원자료 행, 좌표, 축·단위, 선택 점 | 그래프와 값 불일치, 상관→인과 비약. [NIST scatter plot](https://www.itl.nist.gov/div898/handbook/eda/section3/scatterp.htm) 참고 |
| 실험·측정 | 하나의 장치·지점, 도구 접점, 같은 식별자의 기록 | 가운·장치 군집으로 직업·실험 성공 추론. 장치별 정확성·단위 fixture 추가 필요 |
| 도면·모형 | 같은 접합부의 2D/3D 식별자, 지시 도구, 상대 척도 | 무관한 청사진과 모형을 병치. 구조 안전·설계 정확성은 별도 |
| 복기 | 체스 칸 또는 바둑 교차점, 같은 위치의 기록, 현재 지시 | 두 보드 규칙 혼합. [FIDE Article 2.1](https://handbook.fide.com/chapter/E012023), [AGA concise rules](https://www.usgo-archive.org/files/pdf/conciserules.pdf)로 최소 배치 검토 |
| 작품·악보·번역 | 공통 형식 요소, 특정 마디, 짧은 원문/번역문의 정해진 대응 | 미술 감식·음악 능력·번역 정확성을 소품으로 판정. 악보 작업 흔적 사례는 [LOC Beethoven sketch](https://www.loc.gov/collections/moldenhauer-archives/articles-and-essays/guide-to-archives/beethovens-das-schweigen/)의 검색 발췌만 확인 |
| 토론·설명·동료 검토 | 기존 actor A/B, 같은 근거, 서로 다른 메모, 보드 노드와 손, 리뷰 comment anchor | 상대 인원 추가·손 소유자 교체·이해/동의 판정 |
| 야간·산책·필사·자연 스케치 | 현재 장소·받침·도구 상태·원 대상과 기록 대응 | 밤샘 시간·사고 내용·역사 신분·종 식별 자동 부여 |

‘누적 작업’도 커피잔이나 구겨진 종이의 양 대신 v1/v2/v3의 같은 문단 변경으로 저작한다. 일반적인 분위기 이미지와 정확한 text 요구는 나누어 평가한다. exact text가 요청되면 문구·행·기호의 원본 가독성까지 의무로 포함하고, 읽히지 않으면 실패다. exact text를 요청하지 않은 이미지에서 자잘한 글자의 정답성을 사후 필수로 추가하지 않는다.

**고증 미완료 항목:** 123번 선비·문인 필사는 중립 붓 접촉·원문 대응까지 제안했다. 특정 시대의 복식·책·문방 도구·계층 고증을 완료한 자료는 아니다. 109–111의 구체 장치·측량·설계, 114–115의 음악·번역 정답, 112의 합법 기보도 각각 작은 검증 fixture가 필요하다. 문화적 이름만으로 사실성을 인증하지 않는다.

## 7. 문화·성인 매력·위험 서사: 기본 작업 관계를 지우지 않기

125–127의 다크 아카데미아·긱 시크, 130의 오피스 사이렌은 당시 패션 문화의 근거로 활용한다. 2020년·2024년 보도를 2026년의 유행 강도나 모든 사람이 따르는 복장 규칙으로 쓰지 않는다. 밝은 학구풍은 원 대화의 연출 변형으로 표시한다. [Vogue: Dark academia 기사](https://www.vogue.com/article/from-tiktok-to-depop-fashions-new-trend-funnel), [Geek-chic frames](https://www.vogue.com/article/geek-chic-bayonetta-glasses-renaissance-gabbriette-bella-hadid-miu-miu), [Office siren, 2024](https://www.vogue.com/article/office-siren-girlhood-trend-patriarchy).

128번 sapiosexual은 지성에 대한 성적 매력의 용어다. 실제 인물 사진에서 해당 지향을 판정하는 시각 클래스를 만들지 않는다. 대신 요청이 성인 간 공동 독서·대화·호감을 연출하길 명시하면 서로 향한 현재 반응과 같은 자료의 참조를 별도 저작할 수 있다. 이는 실제 동의·욕망·관계 이력을 증명하는 사진 라벨이 아니다. [Merriam-Webster: sapiosexual section](https://www.merriam-webster.com/wordplay/merriam-websters-short-list-of-gender-and-identity-terms/gender-dysphoria-gender-identity-disorder).

129–132는 성인·의상·관능 축과 독서 활동 축을 독립시킨다. 일반 독서와 명시 관능 의상 변형의 **같은 손 역할·같은 책·같은 문단**을 고정하여 스타일 변화가 작업 관계를 지우는지 확인한다. 기본값으로 노출·체형·어린 학생 외양을 추가하지 않는다.

133–140는 요청된 허구·역사·매체의 경계를 보존한다. 손끝 맞대기는 책략가나 범죄 증거가 아니고, 실험실 외양은 정신 건강 진단이 아니다. 심문실·감금·위험 흔적은 명시된 서사에서 받아야 하며 조명·줄무늬 그림자·얼룩만으로 사건을 추론하지 않는다. 전쟁 상황실은 같은 지도 영역과 시점 보고서의 대응으로 설계하고 현재 작전 정확성을 주장하지 않는다. [GOV.UK: historic Map Room](https://www.gov.uk/government/news/secret-war-rooms).

법과학 검토는 포장·사진·기록의 같은 식별자를 먼저 강화한다. NISTIR 7928은 생물학적 증거의 포장·봉인·추적 지침이며 2013년 자료다. 모든 증거를 비닐에 넣는 장식적 연출을 피하고, 해당 증거 종류의 fixture를 선택한다. 봉인 모습은 유죄·진품·법적 적합성을 판정하는 근거가 아니다. [NISTIR 7928](https://nvlpubs.nist.gov/nistpubs/ir/2013/NIST.IR.7928.pdf).

## 실제 데이터에 반영할 단위

78개 초안에는 각각 positive query 형태, 구성요소, directed 관계, actor/document/tool 역할, 제안 slot·owner, 효과 차원의 검토 범위, claim limit, 근거, 채택 조건이 있다. [CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json)의 스키마는 **연구 제안용**이다. 현재 `photo-candidate-pack/v6`나 executable registry로 바로 입력하면 안 된다. 관계 predicate는 설명용 graph이며 현재 런타임 enum을 새로 정의한 결과가 아니다.

| 제안 owner | 초안 수 | 역할 |
|---|---:|---|
| pose vocabulary | 9 | 국소 접촉·지지·명시 포즈의 좁은 변형 |
| intellectual activity, 새 owner 후보 | 50 | 문서 앵커·도구·작업·공유 근거 관계. 기존 owner에 흡수 가능한 항목은 먼저 재사용 |
| portrait composition | 7 | 필수 앵커의 크롭·깊이·시점·여백 |
| realistic background | 1 | 반사·투과와 작업 자료의 연결 |
| lighting | 2 | 기존 렘브란트 재사용 조합·화면광 관계 |
| clothing structure / accessory structure | 2 / 1 | 의복 층·패치·선택 프레임 |
| contextual appeal | 3 | 명시 성인·매력·독서의 독립 축 |
| violence/crime | 3 | 명시 허구 대치·위험 흔적·제한 공간의 기존 작업 관계 보존 |

이 배치는 최종 저장 위치 확정이 아니라 **중복·의미 소유 검토 출발점**이다. 특히 새 activity 파일은 50개를 무조건 추가할 이유가 아니다. 활동·도구 묶음의 중복을 판단하고, 참조 관계가 기존 데이터로 표현되지 않는 항목만 그 owner에 둔다.

## 검증과 판정 경계

반영 순서와 완료 조건은 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에, 구체 프로브는 [REGRESSION-PLAN.json](REGRESSION-PLAN.json)에 있다. 의미·문맥·소유·잠금 사례 82개, native 이미지 all-of 판정 묶음 16개를 계획했다. 테스트나 생성이 이미 성공했다는 뜻은 아니다.

판정은 다음 순서로 분리한다: **연구 근거 → authored 데이터 → 검색 문맥 → 프로파일 노출 → 후보 노출 → 선택/정당한 거절 → 효과·잠금 → 최종 프롬프트 관계 보존 → 원본 픽셀 → 사용자 수용**. required 요소는 가려지거나 잘리거나 읽히지 않으면 통과하지 않는다. 한 이미지의 required 요소를 전부 만족해야 하며 **partial_is_fail**로 평가한다. optional 후보는 전부 거절되어도 정상이다.

이번 연구 패키지 검증은 140개 결정의 누락·중복, 근거 참조, 78개 단위 관계, 기존 ID 참조, 구현 계획 연결, 파일 무결성을 확인하는 범위다. 실제 resolver 동작·candidate pack/v6의 노출·선택·이미지 품질은 구현 후 별도 증거로 남겨야 한다.
