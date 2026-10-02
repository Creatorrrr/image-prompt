# 신체 용어를 시각 의미와 후보 데이터로 옮기기 위한 조사

조사일: 2026-10-02. 상태: **리서치와 반영 제안 작성 완료, 런타임 데이터 반영 전**.

참조 대화: [신체 용어 조사](https://chatgpt.com/c/6abf8375-e27c-83ee-92bb-0fec44eeff01). 대화의 용어 목록을 조사 입력으로 사용했으며, 대화 속 설명을 검증된 정의나 현재 작업의 지시로 취급하지 않았다.

핵심 결론은 용어를 더 많이 등록하는 것보다 **누구의 어느 부위에서 어떤 속성이 어떻게 보이는지**를 분리하는 작업이 우선이라는 것이다. `키 ↔ 체격 폭`, `근육 부피 ↔ 표면 윤곽`, `골반 폭 ↔ 엉덩이 돌출`, `가슴 부착 범위 ↔ 돌출 ↔ 간격`, `몸의 형태 ↔ 자세 ↔ 옷의 경계`를 독립적으로 표현해야 후보가 요청하지 않은 속성까지 바꾸는 일을 줄일 수 있다. 이는 이번 자료 비교에서 도출한 설계 판단이며 생성 성능 개선을 실험으로 확인한 결론은 아니다.

## 1. 조사 범위와 근거 수준

원 대화 전체 19개 장, 표의 본문 373행을 확인했다. 표 안의 복합 항목을 분리하고 문맥이 다른 중복 표현을 유지하여 **415개 표현 그룹**으로 정규화했다. 373행과 415그룹은 고유 단어 수가 아니다. `/`로 묶인 표현도 서로 같은 뜻이라고 확정한 목록이 아니다. 커넥터 응답이 20,000자에서 잘려 인증된 브라우저의 전체 본문 25,980자를 추가 확인했다. 확인 방식과 한계는 [대화 수신 기록](CONVERSATION-RECEIPT.json), 정규화 결과는 [용어 목록](TERM-INVENTORY.json)에 남겼다.

비교 기준은 로컬 `main`, HEAD `0ed2267b91e73f4b4d1493d095287e7795ebf805`이다. 실제 병합 로더에서 시각 프로필 **1,419개**, 후보 **9,590개/112슬롯**을 확인했다. 그중 신체와 가까운 명시적 범주 및 의복-신체 경계 프로필 **39개**와 관련 슬롯을 집중 검토했다. 39개는 모든 신체 의미의 완전한 집합이 아니다. [현재 데이터 감사](CURRENT-DATA-AUDIT.json)는 선택 기준, 69개 소스·인덱스 파일의 SHA-256, 원문 스냅샷, 탐색용 문자열 프로브를 포함한다.

출처 47건을 검토했다. 본문 36건, 공개 초록 1건, PDF 텍스트 1건을 직접 확인했고, 검색 발췌 7건·검색 초록 1건·과거 검색 발췌 1건은 근거 강도를 낮춰 표시했다. 의학·계측 자료는 부위와 측정 경계, 사전은 용법과 다의성, 업체 피팅 자료는 의복과 신체의 관계, 창작 도구 자료는 제작 변수의 범위를 확인하는 데 사용했다. 실제 모델의 검색·프롬프트·이미지 품질을 입증하는 출처는 아니다. [출처별 근거와 제한](SOURCE-NOTES.md), [기계 판독 출처 목록](SOURCES.json)을 함께 참조한다.

## 2. 같은 데이터로 합치면 안 되는 다섯 종류

| 종류 | 예 | 반영 위치와 원칙 |
|---|---|---|
| 관찰 가능한 형태·관계 | 어깨 폭, 가슴 돌출, 피부의 패임, 손가락 길이 | 대상·부위·속성·연결·보기 조건을 갖춘 프로필과 후보 |
| 실측·내부량 | 허리둘레, WHR, 체지방률, lean mass | 연구용 지식. 명시된 측정값과 외관 설명을 분리 |
| 업계·스타일 분류 | petite size, plus-size model, Kibbe, 골격 스타일 | 분류 체계의 문맥. 단일 신체 형태로 자동 번역하지 않음 |
| 평가·사회적 표현 | sexy, callipygian, 베이글, twink | 문맥·어감·복합 함의를 보존. 관찰 형태와 개인 속성의 추정을 분리 |
| 제작·표현 방식 | morph target, shader, chibi, heroic proportion | 제작 설명 또는 사용자가 선택한 양식. 형상·렌더 결과의 별도 검증 필요 |

계측은 기준점과 자세를 갖는 절차다. 사진의 가로 폭은 둘레가 아니며, 사진만으로 구성량을 확정할 수 없다. CDC도 BMI가 지방·근육·뼈와 지방 위치를 구별하지 않는다는 제한을 설명한다. 여기서는 그 제한을 외관 설명과 수치 추정을 구별하는 근거로 사용한다. [ISO 7250 공개 초록](https://www.iso.org/standard/65246.html), [NHANES 계측 매뉴얼](https://wwwn.cdc.gov/nchs/data/nhanes/public/2021/manuals/2021-Anthropometry-Procedures-Manual-508.pdf), [CDC BMI 설명](https://www.cdc.gov/bmi/about/index.html).

시각 의미 레코드의 권장 구조는 `요청에서 명시된 대상 → 부위/소유자 → 속성 축 → 비교 기준 → 관찰 구성요소 → 자세·시점·가림 조건 → 가까운 반례 → 증거 구절 → 픽셀 게이트`다. 예를 들어 넓은 골반의 소유자는 하의가 아니라 인물의 골반 부위이며, 앞뒤 돌출이 아니라 가로 폭을 비교한다. 현재 작성한 [91개 의미 제안](SEMANTIC-PROPOSALS.json)은 이 구분을 기록하는 연구 스키마다. 그대로 런타임에 가져오는 확장 파일은 아니다.

## 3. 키·프레임·마른 체격·볼륨

`petite`, `slender`, `stocky`, `wiry`, `willowy`, `curvy`, `voluptuous`를 하나의 마른/큰 몸 축으로 합치면 안 된다. 출판사 사전의 체격 용어는 가로 두께뿐 아니라 조밀함, 길이 인상, 근육 윤곽, 평가적 어감 등을 포함한다. 의류 업체의 petite는 자체 신장·의복 비율 체계다. 이를 인체 전체의 보편 기준으로 옮길 수 없다. [Cambridge 체격 어휘](https://dictionaryblog.cambridge.org/2012/05/07/body-shapes/), [stocky](https://www.merriam-webster.com/dictionary/stocky), [Lands End 사이즈 체계](https://www.landsend.co.uk/Bottoms/co/mobile-size-chart-women-bottoms.html).

| 표현군 | 필요한 분해 | 가까운 혼동 | 기존 데이터와 제안 |
|---|---|---|---|
| petite / compact | 신장 비교, 골격·몸통 규모, 사지 길이 | 키가 작음 = 마름, 또는 petite 옷을 듦 = 작은 인물 | `compact_adult_frame` 후보가 짧은 신장과 프레임을 묶는다. 별도 속성으로 분리 검토 |
| slim / slender / thin | 몸통과 사지의 가로 볼륨, 부위 간 연속성 | 키가 큼, 검은 옷, 광각만으로 가늘어 보임 | `slender_linear_build` 보강. 건강·체중·매력을 추가하지 않음 |
| stocky / thickset | 길이에 비해 두툼한 몸통·사지 | 작은 키만 있음, 큰 옷, 근육 홈만 있음 | `stocky_build` 신규 축 제안. 골격·지방·근육 원인은 단정하지 않음 |
| wiry / sinewy | 가는 볼륨 + 국소 근육·힘줄 윤곽 | 머리카락의 wiry, 실제 힘·민첩성 | `wiry_definition` 제안. 능력의 주장은 별도 |
| willowy / lanky | 몸통에 대한 긴 사지 + 가로 두께 | 전체 크기나 신발 효과만 있음 | `willowy_long_limb_proportion`과 연결해 중복 검토 |
| curvy | 상체·허리·골반의 윤곽 관계 | 특정 체중, 큰 가슴 하나 | `curvilinear_figure_relation` 유지·문맥 보강 |
| full-figured / voluptuous | 여러 부위의 부드러운 볼륨 분포 | busty만으로 전신 볼륨을 대표 | `soft_full_figure_volume`의 기존 다부위 계약을 보존 |

`gaunt`, `emaciated`, `scrawny` 등의 평가·상태 어감을 긍정 검색 텍스트에서 신체 가치 판단으로 복제하지 않는다. 실제 요청이 특정 형태를 뜻하면 visible contour, bony landmarks 등의 명시된 속성만 기술한다. 표현 자체의 용법은 연구 문맥에 보존한다. `lean`은 체격 외에도 기대기 동작이나 경영 등의 뜻을 가지므로 대상과 속성 문맥을 확인한다. [lean](https://www.merriam-webster.com/dictionary/lean).

## 4. 전신 실루엣과 비율

이미 hourglass·top/bottom hourglass·triangle·inverted triangle·rectangle·oval·diamond·spoon 관계가 있다. 같은 분류 이름을 더 만드는 것보다 상체·허리·골반의 비교 부위, 앞뒤 깊이, 하이힙의 위치와 자세 조건을 보강하는 편이 우선이다. 계측 기반 체형 분류도 측정 위치에 영향을 받을 수 있다는 연구 초록이 확인되었다. 원문 전체를 확인하지 못했으므로 특정 임계값이나 분류 변경률은 가져오지 않는다. [분류 신뢰성 연구](https://www.tandfonline.com/doi/full/10.1080/00140139.2021.1902572).

비율은 최소한 `신장`, `머리/전신`, `몸통/다리`, `상·하완`, `대퇴/하퇴`, `흉곽/허리/골반`을 구분한다. `long legs`를 high-waist clothing으로 대신하지 않는다. anatomical waist level과 waistband level도 다른 소유자다. 머리 수를 세는 예술적 관례는 기준점을 적은 양식 옵션으로만 다루며 현실 인체의 정상 범위를 대신하지 않는다. [계측 표준 공개 초록](https://www.iso.org/standard/65246.html), [Proko의 이상화 비율 설명](https://www.proko.com/course-lesson/human-proportions-idealistic-figures/).

몸이 실제로 좁아지는 관계와 옷이 좁아지는 관계가 같은 `silhouette_proportion` 슬롯에 섞여 있다. 후보의 `body_geometry` 소유권과 garment appearance의 완전한 효과를 재검토해야 한다. 이것은 슬롯 이름만 보고 몸의 속성을 변경해도 된다고 판단할 수 없는 사례다.

## 5. 근육: 부피·윤곽·혈관·줄무늬·힘주기

해부 자료는 근육의 위치와 연결을, 경기 규칙은 근육량·분리도·등의 폭과 깊이 등 관찰 축을 구별하는 근거를 제공한다. 경기 부문의 기준을 보편적 미적 기준으로 사용하지 않는다. [OpenStax 상지 근육](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs), [하지 근육](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs), [NPC Figure 규칙](https://npcnewsonline.com/official-npc-figure-division-rules/).

권장 축은 다음과 같다.

- **Volume:** 명시된 근육 부위의 부피와 관절 연결. 큰 부피와 부드러운 윤곽이 동시에 가능하다.
- **Definition/separation:** 같은 부피에서 읽히는 근육 평면과 경계. 작은 부피에서도 가능하다.
- **Vascularity:** 피부 위에서 읽히는 표재 혈관의 경로. 문신·근육 홈과 구분한다.
- **Striation:** 해당 근육 표면의 미세 반복 선. 옷 조직·튼살과 구분한다.
- **Flex state:** 현재 힘을 준 상태와 편안한 상태. 체형 자체와 분리한다.

현행 `toned_muscular_build`는 절제된 윤곽·힘줄 중심으로 비교적 구체적이다. 그 계약을 큰 근육량까지 확장하지 않고 definition의 주 소유자로 보강하는 방향을 제안한다. `muscle_volume`을 별도로 검토한다. `잔근육`, `마른탄탄`, `brawny`, `beefy`는 각 속성의 조합 후보이지만 모두 같은 exact 별칭으로 묶지 않는다. 조명·포즈가 윤곽을 바꿀 수 있으므로 비교 사례는 같은 상태를 기록해야 한다.

## 6. 목·어깨·흉곽·등의 국소 축

어깨 폭은 양쪽 끝점의 가로 관계이고, 어깨 경사는 목 뿌리에서 끝점까지의 높이 변화다. 흉곽 폭은 어깨 폭·가슴 돌출·등 근육 폭과 다르다. 등 폭과 등 뒤쪽 깊이도 따로 읽어야 한다. 국소 연결은 해부 위치 자료를 기반으로 제안하되, 사진에서 뼈의 실제 치수나 질환을 진단하지 않는다. [해부 위치 용어](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [상지와 어깨 근육](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs).

`직각어깨`는 slope 문맥, `태평양 어깨`·`어깨깡패`는 주로 width 평가 문맥의 연구 후보로 남긴다. 한국어의 고정 뜻을 외부 사전으로 확정한 것은 아니다. 어깨 패드를 몸의 폭으로, 높은 옷깃을 짧은 목으로, 견갑골 음영을 질환으로 읽지 않는 반례가 필요하다.

기존 `clavicle_supraclavicular_hollow`는 쇄골 선과 위쪽 오목함을 연결한다. `scapular_relief`, `neck_proportion`, `ribcage_width/depth`, `back_width_depth`가 보강 축이다. 필요한 보기 때문에 요청의 얼굴 클로즈업을 전신으로 바꾸는 후보는 부적합으로 처리해야 한다.

## 7. 가슴: 국소 형태를 전신 체형과 분리

유방의 구성은 흉근과 동일하지 않다. 가슴의 임상 계측 연구는 기저 폭·돌출·유륜 크기·유두 돌출 등의 개별 치수를 다룬다. 이 자료를 서로 다른 속성이 있다는 근거로 사용하며 특정 집단의 평균값이나 이상 비율을 생성 기본값으로 가져오지 않는다. [Cleveland Clinic 유방 해부](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [Huang 외, 2017](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0172122).

| 축 | 비교 기준과 관찰 대상 | 실패·혼동 경계 |
|---|---|---|
| Prominence/volume | 양쪽 가슴 볼륨과 흉곽·자연 허리 | 전신 hourglass 또는 cup letter로 대신할 수 없음 |
| Root width | 각 가슴의 흉벽 부착 범위, 내측~외측 | 양쪽 사이 간격·외측 한쪽 확장과 같지 않음 |
| Root height | 흉벽에 붙는 세로 범위 | high-set 위치·상부 fullness·상체 길이와 같지 않음 |
| Projection | 흉벽 기저에서 앞쪽 윤곽까지 | 넓은 기저, 상체 숙임, 컵 문자와 같지 않음 |
| Fullness | 위/아래·내/외측의 볼륨 분포 | 전체 크기로 분포를 자동 확정하지 않음 |
| Spacing/orientation | 양쪽 내측 윤곽과 몸통 중심 | 브라 압박·팔 위치로 만든 간격을 자연 형태로 확정하지 않음 |
| Vertical relation | 아래 주름과 윤곽·유두의 위치 관계 | 나이·출산·수술 이력을 추정하지 않음 |
| Asymmetry | 같은 상태의 좌우 형태·위치 차이 | 회전·가림·조명 차이와 구별 |
| Nipple/areola | 유두 돌출과 주변 유륜면·색 경계 | 흥분·임신·수유 이력과 분리 |

Root width와 height는 피팅 분야의 부착 범위 설명을 보조 근거로 사용한다. 현행 본문을 직접 확인한 업체 자료는 각 가슴 전체의 내외측 범위와 spacing을 구별한다. 임상 표준의 확정 정의로 취급하지 않는다. `breast_root_height`는 특히 경계 가림이 많아 P2의 조건부 항목으로 두었다. [Billy's Bras의 부착 범위 설명](https://billysbras.com/blogs/billys-bra-blog/understanding-root-width-and-breast-shape).

Sister sizing은 band와 cup의 결합 체계에 관한 것이며 cup 문자 단독은 절대 볼륨을 규정하지 않는다. 검토한 업체 페이지의 숫자 예시가 서로 일관되지 않아 예시 숫자는 옮기지 않았다. [Bravissimo sister sizing](https://www.bravissimo.com/sister-sizes/). 유두의 현재 외형은 중립 해부 문맥에서 기술할 수 있지만 그 형태가 개인 이력을 입증하지 않는다. [유두 해부 설명](https://my.clevelandclinic.org/health/body/nipple).

현행 `bust_prominence_relation`을 국소 가슴 볼륨의 소유자로 유지한다. `curvilinear_figure_relation`의 `글래머 체형` 별칭은 현행 전신 곡선 계약에 묶여 있다. 한국어 가슴 중심 뜻과의 충돌 가능성은 실제 발견한 설계 이슈다. 사용자가 뜻을 정의하면 그 정의가 우선한다. 이번 조사만으로 기존 별칭을 삭제하거나 가슴 뜻으로 바꾸지 않는다. 후속 단계에서 문맥 분리와 기존 요청의 의미 변경 영향을 검토한다.

## 8. 허리·복부·배꼽

허리의 정면 폭과 측면 깊이는 구분한다. 둘레·WHR은 측정값이다. 복부도 상부/하부 돌출, 중앙선·근육 구획, 배꼽의 표면 형태, 자세에서 생기는 접힘을 독립적으로 다룬다. 복직근·중앙선·힘줄 구획의 해부 연결은 구성요소 제안의 근거이며 실제 체지방률이나 힘의 수치를 뜻하지 않는다. [복벽 근육](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax).

`11자 복근`·`왕자 복근`은 선의 위치와 분할 패턴을 묘사한 문맥 후보로 관리한다. `V-line`은 하복부 윤곽·턱선·의복 V넥·등 V taper를 구분한다. 배꼽은 함몰/돌출·주변 피부 연결만으로 기술하고 병력이나 수술 여부를 추정하지 않는다.

`seated_skin_folds`는 접힘의 원인이 되는 자세가 이미 core에 있을 때 노출 가능한 표면 후보다. `compression_contour`는 옷 밴드와 신체의 연동 효과를 가진다. 이를 appearance 후보로만 선언하면 몸 형태 잠금을 우회할 수 있어 **소유권 검토가 끝나기 전에는 반영하지 않는다**. 단순히 검은 선을 추가하는 방식도 피부 접힘의 성공이 아니다.

## 9. 골반·엉덩이·사지

`wide hips`와 `projecting buttocks`는 정면 가로 폭과 측면 뒤쪽 깊이라는 다른 축이다. 후자는 골반 기울기·허리 과신전·패딩의 효과를 구별해야 한다. 엉덩이 상/하부 fullness, gluteal fold, midline cleft도 각각 볼륨 분포·허벅지 접힘 경계·정중선 골로 소유자가 다르다. [하지 근육과 연결](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).

Hip dips는 자연적인 바깥 윤곽의 들어감으로 설명된다. 현행 `lateral_waist_hip_contour_transition`에는 그 표현이 있지만 허리 오목함부터 골반·바깥 허벅지까지의 더 넓은 전환을 요구한다. `hip dip만, 허리 잘록함 필요 없음` 요청에 전체 전환을 강제할 수 있으므로 국소 indentation 계약의 분리 가능성을 검토한다. 기존 ID를 무조건 중복 생성하는 방안은 아니다. [Cleveland Clinic hip dips](https://health.clevelandclinic.org/hip-dips).

허벅지·종아리는 부위의 횡단 볼륨, 끝쪽으로의 taper, 근육 윤곽을 분리한다. 손은 palm/finger 길이 관계, 관절 마디, 혈관·힘줄을 분리한다. 발은 plantar arch와 dorsal instep, 하중 상태, 신발을 구분한다. X/O 다리의 사진상 정렬은 현재 자세의 투영 관계이며 병명이나 보행 능력의 판단이 아니다.

기존 `inner_thigh_negative_space`의 핵심은 가까운 양발, 허벅지 안쪽 경계, 실제 배경의 연결이다. 다리를 크게 벌리거나 치맛자락 틈·칠한 선으로 대신하면 통과하지 않는다. 공간 관계와 자세를 함께 요구하는 후보는 현재 `body_pose=pose` 소유권에 몸 형상 변경 효과를 숨기지 않도록 분리 검토한다.

## 10. 얼굴 국소 형태

11개 기존 얼굴형 프로필은 유지한다. 전신 의미의 확장을 이유로 얼굴형을 재정의할 필요는 없다. 다음 보강은 눈 개구의 가로/세로 비율, 눈 사이 간격, 눈꺼풀 접힘, 코의 부위별 돌출·폭, 입술 붉은 면의 두께, 귀의 부착, 같은 보기에서의 비대칭이다.

Adobe의 얼굴 편집 도구도 눈 크기·높이·폭·기울기·간격 등을 다른 제어로 다룬다. 이는 속성을 나눌 참고이며 해당 도구의 조작이 현실 형태나 자연스러움을 보장한다는 근거가 아니다. [Adobe Face-Aware Liquify](https://www.adobe.com/learn/photoshop/web/face-aware-liquify).

눈을 크게 뜬 상태와 고정 눈 형태, lip overline과 입술 윤곽, nose shading과 돌출, 얼굴 회전과 실제 비대칭을 구별한다. 기존 `upper_lip_philtral_contour`는 인중 능선·중앙 골·Cupid's bow의 연결을 유지한다. 얼굴 참고 이미지를 신장·체격·가슴의 변경 근거로 사용하지 않는다. 얼굴 형태에서 인종·정체성·성격을 추정하는 레코드를 만들지 않는다.

## 11. 피부·표면·체모

피부 용어는 **색/색소의 분포**, **표면 부조**, **반사·광택**, **털**을 구별해야 한다. 관찰형태 용어와 진단명도 분리한다. [DermNet 형태 용어](https://dermnetnz.org/topics/terminology).

| 축 | 후보 단위 | 구별해야 할 근접 반례 |
|---|---|---|
| 보이는 피부색 | 부위별 색 + 조명·화이트밸런스 조건 | 조명·태닝·메이크업을 민족/국적으로 번역 |
| 색소 패턴 | 바탕 위의 점/반점, 경계, 분포 | 그림자·문신·인쇄·질환명 |
| Microrelief | 모공·미세 요철, 피부의 연속성 | 노이즈·샤픈·필터·플라스틱 표면 |
| Striae | 길쭉한 띠, 색과 국소 질감 | 셀룰라이트·그린 선·의복 주름 |
| Cellulite | 작은 패임과 울퉁불퉁한 부조 | 선형 띠·퀼팅·픽셀 노이즈 |
| Scar-like relief | 국소 선/면의 색·높낮이 차이 | 원인·기간·수술 이력의 자동 추정 |
| Folds/wrinkles | 방향, 위치, 자세와 접힘 관계 | 나이·생활 습관·수분 상태의 확정 |
| Body hair | 섬유 굵기/색, 밀도/길이, 부위/상태 | 수염을 전신 털로 확대, 호르몬·위생 추정 |

튼살의 선형 패턴과 cellulite의 패임은 자료에서도 구별된다. 발생 원인이나 임신 이력을 이미지에서 단정하지 않는다. [AAD 튼살 설명](https://www.aad.org/public/cosmetic/scars-stretch-marks/stretch-marks-why-appear), [DermNet cellulite](https://dermnetnz.org/topics/cellulite). 가는 vellus와 굵고 색이 있는 terminal hair 구분은 검색 발췌 수준의 보조 근거이며, 이 차이만으로 나이·성별·호르몬을 결정하지 않는다. [DermNet 털 관련 설명](https://dermnetnz.org/topics/skin-changes-at-puberty).

기존 후보에 실제 피부 질감, peach fuzz, 거위 피부, 태닝 선, 국소 체모, 튼살과 유사한 선 등이 이미 존재한다. 검색어 `hairy`가 없다고 체모 데이터가 없다고 결론낼 수 없다. 부위·밀도·길이·표면의 중복을 전 후보 코퍼스에서 확인한 후 기존 ID를 보강해야 한다.

## 12. 옷과 몸의 경계 및 성인 용어

원 대화에 있는 성인 용어를 연구 범위에서 누락하지 않았다. 다만 부위 이름, 현재 형태, 노출의 경계, 의복 접촉, 평가·사회적 함의는 다른 데이터다. 조사 목록에 있다는 이유만으로 이미지의 가림을 제거하거나 행위를 추가하지 않는다.

`sideboob`와 `underboob`는 가슴의 측면/하부와 의복 경계의 관계다. `cleavage`는 가슴 사이의 보이는 관계이며 일반적인 분할·광물 등의 다른 뜻도 있다. `camel toe`의 사전적 의복 용법은 천이 만드는 국소 골과 윤곽으로, 일반 봉제선이나 맨살 해부 구조와 같지 않다. [sideboob](https://www.merriam-webster.com/dictionary/sideboob), [underboob](https://www.merriam-webster.com/dictionary/underboob), [cleavage](https://www.merriam-webster.com/dictionary/cleavage), [camel toe](https://www.merriam-webster.com/dictionary/camel%20toe).

현행 `pfe_lateral_chest`와 `pfe_lower_chest`는 같은 불투명 상의의 중앙 가림을 유지하고, 옷 경계 밖의 국소 윤곽을 팔·등 또는 복부와 구별하는 계약이 있다. 이를 재사용한다. 현재 exact 활성화는 좁은 구성요소 문장에 묶여 있으며, 넓은 은어를 즉시 새 exact alias로 등록하는 계획은 아니다.

`fabric_body_outline`은 불투명 옷의 접촉 윤곽, `sheer_layering`은 천 섬유와 그 뒤 신체의 광학적 겹침이다. 같은 타이트핏이 두 뜻을 모두 보장하지 않는다. `bulge`와 중앙 crease는 의복 표면에서 평가하고 신체의 실제 치수나 상태를 확정하지 않는다. Underbutt·옆 엉덩이 노출·중앙 골은 하의 밑단·옆선·정중선의 서로 다른 관계로 추가 연구·조건부 반영한다.

중립 해부 용어에서는 vulva가 외부 구조이며 vagina는 내부 구조라는 차이, penis의 shaft/glans/foreskin, 외부 scrotum과 내부 testes, perineal region의 위치를 보존한다. [외음부 해부](https://my.clevelandclinic.org/health/body/vulva), [음경 해부](https://my.clevelandclinic.org/health/body/penis). 현재 보이는 포피 형태와 circumcision 이력은 같지 않다. 치수·현재 상태를 기술하는 요청과 원인·이력을 추정하는 요청도 구별한다. P4의 해부 레코드는 **명시적 중립 해부 문맥에서 검토할 제안**이며 일반 사진 후보로 자동 활성화하지 않는다.

`thicc`는 사람의 곡선만 아니라 남성의 두툼한 체격, 동물·물건에 대한 유머 용법도 있다. `well-endowed`는 재정·가슴·음경의 여러 뜻이 있으므로 부위를 단어 하나로 선택할 수 없다. [thicc](https://www.merriam-webster.com/slang/thicc), [well-endowed](https://www.merriam-webster.com/dictionary/well-endowed). `bear/otter/twink/femboy/MILF/DILF` 등은 커뮤니티·연령 인상·표현 방식·관계의 복합 항목이다. 외관 후보가 성적 지향, 가족 관계, 정체성, 고정 해부 구성을 자동 확정하지 않도록 문맥 레코드에 남긴다. 개별 의미 근거는 twink의 사전 검색 발췌 외에 충분히 확보하지 못했으므로 추가 조사 대상으로 표시했다.

## 13. 한국어 압축 표현과 업계 분류

한국어 표현은 원 대화의 용례를 보존하되 공신력 있는 사전 정의를 확보하지 못한 항목을 영어 표현의 무조건 동의어로 만들지 않는다.

| 표현 | 이번 조사에서의 분해 후보 | exact 반영 전 필요한 경계 |
|---|---|---|
| 여리여리·호리호리·늘씬 | 좁은 볼륨, 긴 사지, 부드러운 인상 | 각 조합은 같지 않음; health/strength 추정 제외 |
| 마른탄탄·잔근육 | 좁은 볼륨 + 국소 definition | 큰 muscle mass와 분리 |
| 다부진·옹골찬·떡대 | 조밀한 폭/길이 관계, 넓은 체격 | 키·근력·성격의 자동 부여 제외 |
| 직각어깨·태평양 어깨 | 경사와 폭의 별도 축 | 옷 패드·shrug·몸통 기울기 반례 |
| 글래머 | 가슴 중심/전신 곡선의 문맥 후보 | 현행 exact 별칭과 요청 정의의 충돌 검토 |
| 육덕·육감적 | 다부위 soft volume 또는 평가 문맥 | 같은 체중·같은 hourglass로 환원하지 않음 |
| 베이글 | 얼굴 인상+국소 체격의 복합 사회적 표현 | 음식 동음어, 얼굴과 몸의 독립 소유권 |
| S라인·X라인 | 특정 전신 윤곽 또는 구도 | 호가스 구도·상품명·의복선과 분리 |
| 애플힙·복숭아힙 | 국소 projection·상/하부 fullness 후보 | 칭찬 표현으로부터 수치나 단일 모양을 만들지 않음 |
| 꿀벅지·롱다리 | 평가어와 부위 볼륨/길이 관계 | 근육/지방 구성·매력의 확정 제외 |

Kibbe는 창시자의 이미지·스타일 시스템 맥락, Straight/Wave/Natural은 해당 스타일 분류의 맥락으로 보관한다. 이 분류를 임상 해부나 체형의 필수 조건으로 바꾸지 않는다. Somatotype도 사용자에게 정해진 대사·식이·운동 결과를 부여하는 근거로 쓰지 않는다. [Kibbe 창시자 설명](https://davidkibbe.co/about/), [골격 스타일 협회 설명](https://www.fashion.or.jp/kokkaku/), [NASM의 개별 평가 설명](https://www.nasm.org/resource-center/blog/nutrition/what-is-a-mesomorph-diet).

## 14. 자세·신체 차이·보조 장치·3D

자연스러운 비대칭, 한쪽 체중 이동, 몸통 회전, 골반 기울기, 근육 힘주기, 피부 압박은 현재 상태를 먼저 기술한다. 기존 contrapposto·tribhanga·serpentinata 등 명명된 자세는 그 계약을 유지하고, 모든 표면 변화를 해당 포즈 이름으로 묶지 않는다.

사지 차이와 보철은 명시된 신체 구성·장치 연결을 보존한다. residual limb→socket→prosthetic segment의 실제 연결을 읽는 게이트를 제안한다. 이동 보조 장치는 몸의 접촉·지지 관계까지 보아야 한다. 장치만 옆에 놓인 모습은 같은 뜻이 아니다. 사용자별 실제 장치·자세는 다양하므로 출처의 일반 설명을 단일 기본 포즈로 쓰지 않는다. [Össur 보철 안내](https://www.ossur.com/en-gb/prosthetics/information/guide-to-prosthetic-legs), [WHO 휠체어 제공 지침](https://www.who.int/publications/i/item/9789240074521).

Morph target·shape key·blend shape·rig·normal/displacement map·shader는 제작 변수다. 부분 morph와 전신 morph를 구별하는 문서는 있어도 변수를 변경했다는 사실만으로 최종 픽셀의 형태가 검증된 것은 아니다. MetaHuman의 현재 세부 API는 공개 fetch 결과로 검증하지 못했고 Blender 문서는 회수에 실패했으므로 구체 파라미터를 제안하지 않는다. [DAZ morph 설명](https://docs.daz3d.com/public/software/dazstudio/4/userguide/creating_content/modeling/tutorials/pbms/start), [MetaHuman 제작 안내](https://www.metahuman.com/en-US/create).

## 15. 제안 산출물과 아직 확정하지 않은 부분

구체 형상 제안 **91개**, 같은 의미를 후보로 옮기기 위한 초안 **91개**, 실측·분류·다의성·제작 문맥을 위한 **11개 지식/문맥 레코드**, 제안 상태의 회귀 사례 **70개**를 작성했다. 91개 중 15개는 기존 프로필의 소유자를 명시적으로 재사용한다. 나머지 76개는 신규 프로필 생성이 확정된 수가 아니라 전체 코퍼스 중복 검토가 필요한 축이다.

4개 후보안은 현재 슬롯 차원과 완전한 효과가 맞지 않아 소유권 분리 검토를 표시했다: band compression, thigh-gap relation, nail geometry, pose-dependent surface change. 모두 연구 경로의 symbolic target/property를 사용한다. 실제 core의 대상과 프로젝트의 canonical property에 바인딩하기 전에는 export할 수 없다. 정확한 가중치와 별칭도 아직 정하지 않았다.

415그룹은 전부 보존·라우팅 방침을 갖지만 415개의 완성된 런타임 의미를 만들었다는 뜻은 아니다. [COVERAGE-MAP.json](COVERAGE-MAP.json)의 장별 연결은 탐색을 위한 관련 축이며 검증된 동의어 매핑이 아니다. 개별 표현의 뜻·부위·문맥을 검토하는 절차를 후속 계획에 포함했다.

추가 근거가 필요한 항목은 한국어 압축어의 사전·용례, 일부 커뮤니티 은어, root-height의 더 강한 공개 근거, 발 아치·눈꺼풀·귀 부착 같은 세부 형상 자료, shape-key의 현재 공식 문서다. 검색 발췌만 확인한 자료를 본문 검증으로 격상하지 않았다. 원 대화가 주장한 통용성도 검증 완료로 간주하지 않았다.

시각 성능 검증은 아직 실행하지 않았다. 현재 파일은 출처와 데이터 설계의 근거이며 retrieval recall, 후보 채택, prompt fidelity, runtime audit, pixels, 사용자 수용은 별도다. 반영 순서·소유권·호환성·회귀/렌더 평가 계획은 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 있다.
