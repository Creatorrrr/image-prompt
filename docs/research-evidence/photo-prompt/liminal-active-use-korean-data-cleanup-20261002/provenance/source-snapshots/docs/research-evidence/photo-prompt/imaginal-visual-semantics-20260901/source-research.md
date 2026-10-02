# 환상·착시·꿈 시각 의미와 후보팩 확장 리서치

- 조사일: 2026-09-01
- 대상: `photo-prompt-image-generator`
- 입력 범위: 참조 대화 「환상 관련 단어 조사」의 35개 분류와 핵심 50개
- 구현 목표: 넓은 환상 어휘를 한 장의 사진에서 반증 가능한 시각 계약, 선택 가능한 후보 묶음, 사용자 정의 우선 용어로 분리
- 비구현 범위: 이미지 생성, 임상 진단, 실제 초자연 현상 주장, 특정 작가의 화풍 복제, 사용자 미감 판정

## 1. 결론

`fantasy`, `dreamy`, `surreal`, `otherworldly`를 비슷한 빛·안개·파스텔 팔레트로 처리하면 후보팩은 풍부해 보이지만 의미 구별력은 약해진다. 이번 조사에서 환상 이미지를 가장 안정적으로 분해하는 축은 분위기가 아니라 다음 다섯 관계다.

1. **지각의 근거**: 외부 자극의 오인, 외부 자극 없는 주관적 지각, 꿈, 자연 광학, 허구 세계 규칙 중 무엇인가.
2. **깨지는 규칙**: 장소·시간의 불연속, 서로 맞지 않는 결합, 공유 경계의 이중 판독, 국소적으로는 맞지만 전체가 불가능한 연결, 반사 대응의 위반, 재료·형태의 연속 변신 중 무엇인가.
3. **현실 앵커**: 익숙한 방, 같은 인물, 반복 소품, 거울 가장자리, 전이 통로, 비인간 표면처럼 위반 전후를 비교할 기준이 있는가.
4. **관찰자 반응**: 놀람, 무심한 일상 지속, 꿈임을 알아차리는 자기 점검, 한 사람에게만 보이는 지각처럼 반응이 의미를 바꾸는가.
5. **촬영 혼동 통제**: 블러, 긴 노출, 이중 노출, 렌즈 플레어, 홀로그램, 안개, 단순 합성, 빈 공간만으로 의미를 대신하지 않는가.

이 축을 사용하면 정확 시각 계약, 후보팩, 자문형 검색, 비시각 상태를 분리할 수 있다.

## 2. 참조 대화 키워드의 데이터 라우팅

| 대화의 키워드군 | 처리 | 이유 |
|---|---|---|
| dream logic, dream discontinuity, oneiric dream logic | 좁은 시각 계약 | 익숙한 기준과 한 개의 명확한 불연속·불일치가 동시에 보이면 반증 가능하다. |
| lucid dream, false awakening, shared dream, prophetic dream | 후보 또는 사용자 정의 | 자각·공유·예지는 내부 인식이나 서사 사실이며 한 프레임이 자동 증명하지 못한다. |
| optical illusion, ambiguous figure, figure-ground reversal | 좁은 시각 계약 | 같은 물리 자극과 공유 경계가 두 개의 완전한 판독을 지지해야 한다. |
| impossible object, impossible staircase, impossible architecture | 좁은 시각 계약 | 각 부분은 국소적으로 가능하지만 전체 연결이 하나의 시점에서 모순되어야 한다. |
| mirage, Fata Morgana, halo, sundog, Brocken spectre | 자연 광학 소유권 | 실제 대기광학 현상이다. 판타지 팔레트가 아니라 관측 기하·광원·대기 조건으로 다뤄야 한다. |
| visual hallucination, hypnagogic imagery | 후보 및 엄격한 한계 | 대응 외부 자극의 부재는 정지 픽셀만으로 확정하기 어렵다. 원인·진단·약물 사용을 추론하지 않는다. |
| afterimage, residual image | 후보 | 선행 자극과 시간 경과가 필요한 지각 현상이다. 정지 이미지의 유령상·모션 트레일과 구분이 어렵다. |
| surrealism, surreal photography | 후보팩 연구 축 | 초현실주의는 하나의 외형이 아니라 기대 교란, 파편화, 병치, 자동기술 등 여러 전략을 포함한다. |
| liminal space | 좁은 시각 계약 | 전이 기능, 예상 사용 흔적, 사용·점유의 공백, 익숙한 구조의 작은 편차를 함께 판정할 수 있다. |
| magical realism | 좁은 장면 관계 계약 | 현실적 일상, 한 개의 불가능 사건, 인물의 무심한 수용, 일상 행위에 남은 결과가 함께 있어야 한다. |
| mirror world, false reflection, delayed or independent reflection | 좁은 반사 관계 계약 | 실제 인물과 거울상을 같은 프레임에서 정렬한 뒤 한 가지 동작·시간 대응만 어긋나야 한다. |
| time loop, frozen time, temporal echo | 후보 | 반복·정지·역행은 시간 순서의 주장이다. 한 프레임에서는 복제 인물·고속 촬영·다중 노출과 혼동된다. |
| memory echo, memoryscape, false memory, nostalgia | 후보 | 기억의 진위와 주체는 픽셀로 판정할 수 없다. 같은 장소·사물 앵커의 시간층만 제안할 수 있다. |
| metamorphosis, visible mid-transformation | 좁은 시각 계약 | 한 주체의 출발·도착 상태와 연속 전환부가 동시에 보이면 정지 이미지에서도 반증 가능하다. |
| phantasmagoria | 문맥 제한 시각 계약 | 역사적 환등 투사 의미에서는 광원·투사면·유령상·크기 변화가 보인다. 단순 ‘기괴한 환영들’은 자문형이다. |
| apparition, phantom, specter, ghost | 기존 유령 계약 또는 후보 | 이전 인물 정체성과 존재 위반·국소 결과가 필요한 기존 `human_ghost_identity_breach`를 재사용한다. |
| pareidolia, faces in patterns | 좁은 시각 계약 | 실제 비얼굴 표면이 유지되면서 그 구성요소가 얼굴처럼 읽혀야 한다. 실제 얼굴·가면·그림은 실패다. |
| ethereal, dreamy, whimsical, mystical, celestial, otherworldly | 미감 후보 | 주관적 미감 방향이며 특정 색·빛·의상으로 하드 고정하지 않는다. |
| dark fantasy, cosmic fantasy, fairy-tale fantasy, portal fantasy | 장르 후보 | 작품·시장·문화별 범위가 겹친다. 장르명만으로 특정 생물·의상·도덕성·세계 구조를 강제하지 않는다. |
| glowing forest, floating island, crystal flower, liquid light | 일반 후보 | 개별 소재는 환상성을 도울 수 있지만 소재 하나가 꿈·초현실·마술적 사실주의를 증명하지 않는다. |

## 3. 권위 출처에서 추출한 시각 차원

### 3.1 꿈 논리는 흐림이 아니라 불연속·불일치·불확실성이다

- [Hobson et al., Dream bizarreness and the activation-synthesis hypothesis](https://pubmed.ncbi.nlm.nih.gov/3449484/)는 꿈의 기이함을 불연속, 불일치, 불확실성으로 분해한다.
- [The Met, Dream States](https://www.metmuseum.org/exhibitions/listings/2016/dream-states)는 사진가들이 카메라의 사실 기록을 변형해 꿈을 ‘묘사’하기보다 환기해 왔음을 설명한다.
- 데이터 결정: 한 장면에는 익숙한 방향 앵커, 한 개의 지배적 불연속 또는 불일치, 그 위반을 국소화하는 접합부, 같은 인물·사물의 연속성을 둔다.
- 혼동 경계: 소프트 포커스, 파스텔, 안개, 떠 있는 물체, 잠든 인물만으로는 꿈 논리를 충족하지 않는다.

### 3.2 자각몽은 꿈 제어가 아니라 꿈임을 아는 메타인식이 핵심이다

- [Baird et al., The cognitive neuroscience of lucid dreaming](https://pmc.ncbi.nlm.nih.gov/articles/PMC6451677/)는 자각몽을 진행 중인 꿈에서 자신이 꿈꾸고 있음을 알아차리는 현상으로 정의한다.
- 데이터 결정: `lucid dream`은 자동 하드 계약으로 만들지 않는다. 후보팩은 반복되는 현실 앵커, 꿈 이상을 의도적으로 점검하는 행위, 한 개의 제한된 변화 제어를 제안할 수 있지만 그것만으로 실제 인식 상태를 증명했다고 하지 않는다.
- 혼동 경계: 눈을 뜬 인물, 밝은 이마, 공중 부양, 손을 바라보는 포즈, 일반 꿈 풍경은 자각의 증거가 아니다.

### 3.3 착시와 환시는 자극 관계가 다르다

- [Visual Hallucinations in the Psychosis Spectrum...](https://pmc.ncbi.nlm.nih.gov/articles/PMC4141306/)는 시각 환시를 대응 외부 자극 없이 깨어 있을 때 경험하는 지각, 시각 착시를 외부 자극에 의해 유발되지만 보통 지각과 다른 경험으로 구분한다.
- 데이터 결정: `visual hallucination`은 후보형 주관 시점 장치로만 둔다. 한 관찰자의 반응, 다른 관찰자·카메라·물리 흔적과의 불일치, 국소적 주관 오버레이를 제안할 수 있지만 원인·질환·약물·성격을 추론하지 않는다.
- 혼동 경계: 화면 글리치, VFX 왜곡, 색수차, 유령, 꿈, 파레이돌리아, 광학 착시를 환시와 같은 뜻으로 병합하지 않는다.

### 3.4 모호 도형은 같은 자극이 두 판독을 지지해야 한다

- [Ambiguous Figures – What Happens in the Brain When Perception Changes But Not the Stimulus](https://pmc.ncbi.nlm.nih.gov/articles/PMC3309967/)는 시각 정보가 그대로인 동안 지각이 자발적으로 뒤바뀌는 모호 도형을 다룬다.
- [Figure-ground perception](https://www.scholarpedia.org/article/Figure-ground_perception)은 공유 경계가 어느 영역에 할당되는지에 따라 서로 다른 형상이 되는 도형-배경 반전을 설명한다.
- 추출 차원: 한 개의 공유 윤곽, 두 개의 완전한 판독, 바뀌지 않는 물리 표식, 어느 한쪽이 도형이 될 때 다른 쪽이 배경이 되는 관계, 축소판에서도 남는 이중 판독.
- 혼동 경계: 두 그림을 나란히 놓기, 투명도 합성, 단순 콜라주, 숨은 그림 하나, 윤곽이 겹치지 않는 이중 노출은 실패한다.

### 3.5 불가능 도형은 국소적 가능성과 전역적 모순을 동시에 보존한다

- [Penrose & Penrose, Impossible objects: a special type of visual illusion](https://pubmed.ncbi.nlm.nih.gov/13536303/)은 개별 부분은 보통의 3차원 물체처럼 받아들일 수 있지만 잘못 연결된 전체가 불가능 구조가 되는 도형을 제시했다.
- 추출 차원: 전체 연결이 보이는 단일 시점, 각 구간의 자연스러운 깊이 단서, 전역 폐회로 또는 모순 연결, 일관된 재료·빛·접촉, 모순 접합부의 가독성.
- 혼동 경계: 단순 기울어진 방, 중력 무시 부유물, 랜덤 계단, 건축 콜라주, 한 각도에서만 이어 보이는 실제 분리 조형물을 ‘실제 불가능 물체’라고 부르는 것은 분리한다.
- 표현 경계: 특정 작가의 고유 화풍을 요구하거나 복제하지 않고 일반적인 불가능 연결 원리만 사용한다.

### 3.6 리미널 공간은 빈 복도 하나가 아니라 전이와 기대 위반의 관계다

- [Diel & Lewis, Structural deviations drive an uncanny valley of physical places](https://doi.org/10.1016/j.jenvp.2022.101844)는 익숙한 장소 구성에서의 구조적 편차가 장소의 기묘함과 연결되고, 인터넷에서 리미널 공간이라 불리는 이미지가 연구 후보가 될 수 있음을 보인다.
- [Thinking on Thresholds](https://www.cambridge.org/core/books/thinking-on-thresholds/introduction/99793B07E500C6A2B4EBB5093B678792)는 문턱과 전이 공간의 불확정성·중간 상태를 다룬다.
- 추출 차원: 통로·대합실·수영장·상가처럼 전이 또는 집단 사용 기능, 익숙한 안내·가구·조명, 기대 인구와 실제 점유의 공백, 사용 직전·직후 흔적, 작지만 판독 가능한 구조·시간 편차.
- 혼동 경계: 폐허, 어두운 빈방, 공포 괴물, 노란색 복도, 무한 공간 하나만으로는 충분하지 않다. 리미널은 반드시 공포일 필요도 없다.

### 3.7 마술적 사실주의는 현실과 마법의 무심한 공존 방식이다

- [Cambridge, Magical Realism and Literature](https://www.cambridge.org/core/books/abs/magical-realism-and-literature/introduction/1A17BC1D603AF34F3A67989354559CF2)는 마술적 사실주의가 정의 논쟁을 가지면서도 초자연적 사건을 완전히 자연스러운 일처럼 취급하는 핵심을 제시한다.
- 추출 차원: 구체적인 일상 노동·가정·거리, 한 개의 불가능 사건, 주변 인물의 과장되지 않은 일상 지속, 불가능 사건이 일상 사물에 남긴 물리 결과, 현실적인 재료·빛·카메라.
- 혼동 경계: 비밀 마법 세계, 주문 전투, 포털 구경꾼, 공포 반응, 꿈 연출, 판타지 의상, 무관한 초현실 콜라주는 실패한다.
- 문화 경계: 특정 지역·민족·종교의 세계관을 장르 외형으로 일반화하지 않는다.

### 3.8 거울 환상은 정상 대응을 먼저 세운 뒤 한 규칙만 어긋나야 한다

- [OpenStax, The Law of Reflection](https://openstax.org/books/college-physics/pages/25-2-the-law-of-reflection)은 평면 거울의 광선 대응과 물체·상 위치 관계를 설명한다.
- 추출 차원: 실제 인물과 거울상이 같은 프레임에 있음, 거울면·가장자리·주변 표식으로 정렬 가능, 한 가지 동작·시선·시간 위상만 어긋남, 나머지 자세·의복·방 구조는 정상 대응, 양쪽에 서로 다른 물리 결과.
- 혼동 경계: 쌍둥이, 두 번째 인물, 워프 거울, 단순 좌우 반전, 일반 거울 셀피, 이중 노출, 거울 바깥 유령은 실패한다.

### 3.9 파레이돌리아는 실제 비얼굴 표면이 끝까지 남아야 한다

- [Face pareidolia in the brain](https://pmc.ncbi.nlm.nih.gov/articles/PMC7774913/)은 구름·그림자·풍경·집의 패턴에서 얼굴을 보는 경향을 얼굴 파레이돌리아로 설명한다.
- 추출 차원: 구름·목재·암석·건물·얼룩 같은 비얼굴 원천, 원천의 실제 구성요소가 눈·코·입 관계로 읽힘, 원천 정체성이 계속 판독됨, 실제 얼굴과 비얼굴 사이의 모호성, 인위적 눈·입 추가 없음.
- 혼동 경계: 사람 얼굴, 가면, 조각, 낙서 얼굴, 디지털 스티커, 명백히 그린 표정, 얼굴만 보이고 원천이 사라진 이미지는 실패한다.

### 3.10 변신은 두 상태의 병치가 아니라 한 몸의 연속 전환이다

- [The Met, Marey Chronophotograph](https://www.metmuseum.org/art/collection/search/265094)는 한 판 위의 다중 노출로 운동의 여러 단계를 연결한 사진적 선례를 설명한다. 이 자료는 판타지 변신의 정의가 아니라 정지 이미지에 시간 단계를 보존하는 시각 방법의 근거다.
- [MoMA, American Surrealist Photography](https://www.moma.org/calendar/exhibitions/422)는 사진 몽타주·인쇄 과정이 익숙한 몸과 사물을 변형·파편화하는 데 사용되었음을 설명한다.
- 추출 차원: 한 주체의 정체성·질량 연속성, 분명한 출발 상태, 분명한 도착 상태, 서로 맞물린 재료·해부·위상 전환부, 방향을 알려주는 잔류물·접촉·움직임.
- 혼동 경계: 전후 인물 두 명, 코스튬 교체, 동물과 사람의 겹침, 신체 일부에 붙인 장식, 완성 상태 하나, 피·상처만으로 변신을 대신하는 장면은 실패한다.

### 3.11 판타스마고리아는 유령 존재가 아니라 투사 매체와 연속 쇼다

- [Science Museum Group, Phantasmagoria magic lantern](https://collection.sciencemuseumgroup.org.uk/objects/co8001421/phantasmagoria-magic-lantern)은 하나 이상의 환등기로 벽·연기·반투명 스크린에 유령·해골·악마 이미지를 투사하고, 이동식 투사기로 크기를 바꾸거나 영상을 빠르게 전환한 역사적 공연을 설명한다.
- 추출 차원: 실제 투사 장치 또는 빛 경로, 벽·연기·반투명 스크린, 서로 다른 크기·위치의 연속 유령상, 공연 공간의 깊이, 투사상과 물리 공간의 구분.
- 혼동 경계: 실제 유령 장면, 홀로그램 하나, 안개 속 실루엣, 일반 공포 콜라주, 프로젝터만 있는 빈 무대는 실패한다.

### 3.12 초현실주의는 단일 스타일이 아니라 기대를 깨는 전략군이다

- [Getty AAT, Surrealism](https://www.getty.edu/vow/AATFullDisplay?subjectid=300021512)는 현실을 본능·무의식·꿈과 결합하는 국제적 지적·예술 운동으로 설명한다.
- [The Met, Surrealism Beyond Borders](https://www.metmuseum.org/exhibitions/listings/2021/surrealism-beyond-borders)는 파편화·병치·자동기술·대안 질서 등 지역과 시대를 넘는 여러 전략을 제시한다.
- 데이터 결정: `surreal`, `surrealism` 자체를 하나의 하드 시각 프로필로 만들지 않는다. 후보팩에는 현실적 평범함, 한 개의 기대 위반, 물리적 접합, 명확한 개념 관계를 분리해 제공한다.
- 혼동 경계: 녹는 시계, 거대한 달, 눈 달린 물체 같은 유명 모티프 목록을 보편 정답으로 저장하지 않는다.

### 3.13 신기루·잔상은 실제 현상이며 환상 장르의 자동 증거가 아니다

- [WMO International Cloud Atlas, Mirage](https://cloudatlas.wmo.int/en/mirage.html)는 신기루를 먼 물체의 상이 대기 굴절로 왜곡·반전·상승하는 광학 현상으로 정의하고 Fata Morgana를 복잡한 상층 신기루로 설명한다.
- [The human brain mechanisms of afterimages](https://pmc.ncbi.nlm.nih.gov/articles/PMC12424661/)는 잔상을 선행 광원이 사라진 뒤에도 나타나는 일반적 시각 착시로 다룬다.
- 데이터 결정: 신기루는 자연환경 광학 데이터가 소유하고, 잔상은 선행 자극·시간 문맥이 명시될 때만 후보로 제안한다. 둘 다 `fantasy`나 `hallucination`의 자동 하드 증거가 아니다.

## 4. 구현할 정밀 시각 계약

| 프로필 ID | 핵심 판정 | 가장 가까운 실패 대체물 |
|---|---|---|
| `oneiric_dream_logic_discontinuity` | 익숙한 앵커 + 한 불연속/불일치 + 국소 접합 + 연속 주체 | 흐림, 파스텔, 떠 있는 소품 |
| `ambiguous_figure_ground_dual_read` | 공유 경계 + 두 완전 판독 + 동일 자극 | 나란한 두 그림, 단순 겹침 |
| `impossible_object_global_connection` | 국소 가능 구간 + 전역 모순 연결 + 단일 시점 | 랜덤 계단, 부유 건축 |
| `liminal_transition_use_gap` | 전이 기능 + 익숙한 사용 표식 + 점유 공백 + 시간 잔류 | 빈방, 폐허, 괴물 |
| `magical_realism_matter_of_fact_anomaly` | 일상 + 한 불가능 사건 + 무심한 지속 + 일상 결과 | 주문 전투, 꿈, 공포 반응 |
| `mirror_reflection_action_mismatch` | 정상 정렬 + 한 행동/시간 불일치 + 나머지 정상 대응 | 쌍둥이, 워프 거울, 이중 노출 |
| `face_pareidolia_embedded_nonface_pattern` | 비얼굴 원천 + 얼굴 판독 + 원천 정체성 유지 | 실제 얼굴, 가면, 그린 얼굴 |
| `continuous_metamorphosis_source_target_bridge` | 한 주체 + 출발/도착 + 연속 전환부 + 방향 흔적 | 코스튬 교체, 전후 병치 |
| `phantasmagoria_projected_spectral_sequence` | 투사 장치/경로 + 투사면 + 연속 유령상 + 공연 깊이 | 실제 유령, 홀로그램, 안개 실루엣 |

각 계약은 좁은 다국어 정확어, 최소 다섯 구성요소, 다섯 근거 문구, 썸네일·원본 렌더 게이트, 인접 실패 대체물을 가진다. 직접 정확어만 요청 범위의 하드 의무를 만들며, BM25F·임베딩 발견은 선택 가능한 후보로만 남는다.

## 5. 후보팩 확장 원칙

고립된 환상 소품을 늘리는 대신 다음 묶음을 추가한다.

`현실 앵커 → 규칙 위반 → 비교 접합부 → 관찰자/대상 반응 → 국소 결과`

주요 후보 묶음은 다음과 같다.

- 꿈 논리: 반복 방향 소품, 익숙한 방, 한 개의 장소 접합, 같은 인물·사물의 연속성, 접합부의 일관된 빛.
- 모호 도형: 공유 윤곽 물체, 두 판독이 가능한 네거티브 스페이스, 동일 자극을 보존하는 정면 구도.
- 불가능 구조: 완전한 연결을 보여주는 단일 시점, 국소 원근이 맞는 계단·보·통로, 전역 폐회로 접합.
- 리미널: 전이 통로, 안내·가구·조명의 정상 사용 표식, 직전·직후 흔적, 점유 공백, 해소되지 않은 다음 경로.
- 마술적 사실주의: 평범한 노동자·가족·승객, 일상 과업, 한 개의 불가능 사건, 놀라지 않고 이어지는 행위, 같은 사물에 남는 결과.
- 거울 불일치: 거울 가장자리와 정렬 표식, 실제 인물과 거울상을 함께 담는 구도, 한 개의 동작 위상 차이, 나머지 반사의 정상성.
- 파레이돌리아: 목재·구름·암석·건물 같은 비얼굴 표면, 얼굴 관계를 만드는 실제 부품, 원천과 얼굴의 이중 판독.
- 변신: 한 주체 전신, 출발 재료/형태, 도착 재료/형태, 연속 위상·해부 접합, 시작점 잔류물.
- 판타스마고리아: 환등기·빛 경로·투사면, 크기가 다른 연속 유령상, 투사 매체가 보이는 공연 공간.
- 자문형 후보: 자각몽 자기 점검, 한 사람에게만 보이는 주관 오버레이, 같은 앵커의 시간층, 같은 장소의 기억층, 자연 광학 신기루.

## 6. 의도적으로 하드닝하지 않는 용어

- `fantasy`, `dream`, `dreamscape`, `dreamworld`, `oneiric`, `dreamy`, `ethereal`, `otherworldly`, `mystical`, `whimsical`.
- `lucid dream`, `false awakening`, `shared dream`, `prophetic dream`, `visual hallucination`, `afterimage`, `memory echo`, `time loop`.
- `surreal`, `surrealism`, `dark fantasy`, `cosmic fantasy`, `fairy-tale fantasy`, `magical`, `celestial`, `astral`.
- `mirage`, `Fata Morgana`, `aurora`, `halo`, `sundog`, `bioluminescence`, `iridescence`는 자연 현상 또는 재료·빛 데이터가 우선 소유한다.
- `phantom`, `apparition`, `ghost`, `specter`는 이전 인물 정체성이 필요한 기존 유령 계약과 문맥을 대조한다.

이 용어들은 검색과 창작 후보에는 유용하지만 하나의 색, 조명, 의상, 생물, 정신 상태, 도덕성으로 환원하지 않는다.

## 7. 검증 설계

### 7.1 패키지와 인덱스

- JSON 원본과 연구 JSONL이 파싱되어야 한다.
- 모든 새 프로필은 구성요소·근거·렌더 게이트·실패 대체물을 완전하게 가져야 한다.
- 후보 ID와 게이트 ID는 전역에서 중복되지 않아야 한다.
- 시각 프로필 인덱스는 레지스트리 해시와 정확어 집합을 재현해야 한다.
- 후보 의미 인덱스는 사전 버전·항목 수·샤드 해시와 일치해야 한다.

### 7.2 직접 활성화와 인접 부정

- `dream logic scene`, `ambiguous figure`, `impossible object`, `liminal space`, `magical realism`, `independent reflection`, `face pareidolia`, `visible metamorphosis`, `phantasmagoria projection`은 각 한 프로필만 직접 활성화해야 한다.
- broad `dream`, `dreamy`, `lucid dream`, `hallucination`, `surrealism`, `otherworldly`, `time loop`, `memory echo`, `mirror`, `transformation`, `ghost`, `mirage`, `ethereal`은 이번 새 하드 계약을 강제하지 않아야 한다.
- `empty room`, `abandoned mall`, `twin portrait`, `double exposure`, `painted face`, `costume change`, `projector on a stage` 같은 가까운 대체물도 새 프로필을 직접 활성화하지 않아야 한다.

### 7.3 검색 경계

- 구성요소 설명의 BM25F·임베딩 히트는 선택 가능한 `visual_concept_candidate`여야 하며 하드 근거나 렌더 게이트를 만들지 않아야 한다.
- 정확어의 부정과 요청자 정의는 레지스트리 기본 의미보다 우선해야 한다.
- 사용자 정의가 `liminal`, `metamorphosis`, `phantasmagoria`를 다른 뜻으로 한정하면 기본 프로필이 그 정의를 덮어쓰지 않아야 한다.

### 7.4 증거 계층

- 레지스트리·인덱스·테스트 통과는 패키지 구조와 프롬프트 가능성의 증거다.
- 실제 이미지의 이중 판독, 불가능 연결, 반사 정렬, 연속 변신은 렌더 픽셀을 따로 검사해야 한다.
- 환상성·몽환성·아름다움·불안감은 사용자 미감 판단이며 자동 계약이 승인할 수 없다.
- 이번 작업은 이미지 생성을 요청받지 않았으므로 렌더와 사용자 판단은 미평가로 남긴다.

## 8. 안전·문화·재사용 경계

- 환시·꿈·파레이돌리아 표현에서 질환, 약물 사용, 위험성, 성격, 지능을 추론하지 않는다.
- 리미널·마술적 사실주의·초현실주의를 특정 국가·민족·종교의 보편 미감으로 환원하지 않는다.
- 역사적 환등기, 작품, 박물관 소장품의 구도·장식·이미지·텍스트를 복제하지 않는다.
- 특정 작가 이름을 스타일 프롬프트로 만들지 않고 일반 관계·기하·촬영 원리만 추출한다.
- 실재 자연광학을 초자연 현상이라고 주장하지 않으며, 허구 효과와 관측 현상을 데이터 소유권에서 구분한다.
