# 모델·에디토리얼·전문 촬영 용어의 시각 의미와 후보팩 보강 연구

모델·패션 촬영 데이터의 우선 보강 대상은 직업명이나 고급스러움을 강조하는 수식어의 수가 아니라, **촬영 목적에 맞게 무엇을 보여 주고, 어떤 관계를 유지하며, 무엇과 혼동하지 않아야 하는지**다. 모델의 소속·경력, 출판·광고의 용도, 제작 현장, 사진의 구성, 파일 납품 조건을 독립적으로 저장해야 한다. 같은 인물과 조명을 사용해도 목표 의상 디테일, 제품의 위계, 페이지 배치, 컷 간 연속성이 달라지면 다른 결과가 된다.

참조 자료의 13개 분류에서 261개 용어 행을 확보했다. `Controlled`, `Intentional`이 두 분류에 등장하므로 고유 표기는 259개다. 원문 항목은 [입력 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/input-inventory.json), 처리 판단은 [용어 분류표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/term-map.json)에 보존했다. 이 전체 목록을 외부 출처로 개별 인증한 것은 아니다. 핵심 경계에 관한 17개 1차·공식 자료를 확인하고, 데이터 구현에 영향을 주는 구분을 집중 검토했다.

산출물은 시각 관계 제안 24개, 후보 묶음 제안 15개, 설계 검증 사례 46개다. **모두 연구 초안이며 런타임에 통합하지 않았다.** 기존 소스에 대한 읽기 전용 조사와 정확 일치 진단은 수행했지만, 신규 후보 노출·선택·프롬프트 감사·이미지 생성·픽셀 평가는 실행하지 않았다. 이미지 생성 효과를 입증한 리서치라는 의미로 해석하면 안 된다.

## 근거에서 확인한 중요한 구분

**용도와 스타일을 분리해야 한다.** Models.com은 editorial, advertising, lookbook, cover 등 작업 종류를 구분하며 미게재 테스트·개인 작업은 자체 데이터베이스에서 Other로 분류하도록 안내한다. 이는 “에디토리얼처럼 연출한 테스트 사진”의 스타일 설명과 “실제로 게재된 editorial 작업”의 기록이 다를 수 있다는 근거다. 기관별 데이터 분류를 모든 촬영의 미적 정의로 확장해서는 안 된다. [S01](https://help.models.com/article/60/choosing-the-correct-client-date-and-title-when-uploading-a-new-work)

**서사는 에디토리얼만의 독점 속성이 아니다.** Adobe의 교육 자료는 편집 사진의 이야기·콘셉트·주변 맥락을 강조한다. 그러나 Prada의 2025 캠페인은 각 이미지와 연결된 문학적 인물 이야기를 공식적으로 제시한다. 따라서 `editorial = narrative`, `campaign = narrative 없음`의 배타적 분류는 성립하지 않는다. 데이터에서는 유통 목적과 서사 구조가 동시에 존재하도록 설계하는 편이 적절하다. [S02](https://www.adobe.com/creativecloud/photography/type/editorial-photography.html), [S15](https://www.prada.com/hk/en/pradasphere/campaigns/2025/ss-woman.html)

**Editorial 내부에서도 문맥이 갈린다.** 패션 화보, 인물 기사, 뉴스·보도, 스톡 라이선스의 editorial은 같은 단어를 공유한다. Adobe Stock의 안내에는 비연출 뉴스·보도 이미지가 포함된다. 패션 화보의 연출·후보정 관행을 editorial 전체의 의무로 만들 수 없다. 이번 연구의 주 대상은 패션·인물·브랜드 촬영이며, 보도 이미지의 편집 기준을 새로 규정하지 않는다. [S13](https://helpx.adobe.com/uk/stock/contributor/help/editorial-requirements.html)

**Digitals와 test shoot는 구별해야 한다.** Elite의 지원 지침은 전신·근접·측면 사진, 정면 자연광, 화장 없는 단순한 구성을 제시하고 Select 역시 지원 시 화장 없는 자연스러운 모습을 요구한다. 이는 캐스팅 자료를 위한 구체적인 기관 사례다. `Agency Test`라는 제작 목적만으로 동일한 조명과 스타일을 강제할 근거는 부족하다. `Polaroids` 역시 캐스팅 기록의 관용 표현인지, 실제 즉석 필름의 테두리·재질을 말하는지 먼저 구분해야 한다. [S03](https://elitemodelmanagement.com/get-scouted.web), [S04](https://apply.selectmodel.com/advice)

**전문적 인상은 관계로 분해할 수 있지만 경력은 인증할 수 없다.** Getty가 설명하는 contrapposto의 핵심은 한 다리에 하중을 둔 자세다. Nikon의 작가 인터뷰는 인물과의 협력, 포즈 변주, 전달할 이미지 묶음의 계획을 설명한다. 여기서 도출할 수 있는 데이터 방향은 지지·관절 연결·시선·의상 가독성이다. 고정된 체형, 무표정, 특정 시선으로 전문 모델 여부를 판정하는 기준은 도출되지 않는다. [S05](https://www.getty.edu/education/for_teachers/curricula/sculpture/background1.html), [S06](https://www.nikonusa.com/learn-and-explore/c/ideas-and-inspiration/the-portrait-as-assignment-documentary-and-more)

참조 자료에 있는 “professional fashion model 같은 표현이 생성 결과의 차이를 더 명확히 한다”는 설명은 이번 연구에서 성능 사실로 채택하지 않았다. 모델·버전·프롬프트·참조·반복 표본에 따른 비교가 필요하다. 수식어 자체의 효과와 구체적인 관계 데이터의 효과도 별도로 검증해야 한다.

**피부 질감과 보정 이력은 다르다.** Adobe는 주파수 분리에서 미세 질감과 넓은 색·톤 정보를 구분하고, Healing Brush에서는 주변의 질감·명암과 맞추는 복원 과정을 설명한다. 연구상 필요한 것은 지정 부위에서 질감과 톤이 각각 읽히는지다. 결과에 모공이 있다는 이유로 “무보정” 또는 “특정 프로그램을 사용했다”고 판정할 수 없다. [S10](https://www.adobe.com/products/photoshop/frequency-separation.html), [S11](https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html)

**표지·인쇄용이라는 말에는 서로 다른 검증이 필요하다.** 사진 안의 문구 여백과 중앙 접힘에 대한 배치는 시각·레이아웃 문제다. bleed·slug 및 해상도·누락 폰트·연결 파일·넘친 텍스트 검사는 문서와 파일의 기술 문제다. `premium magazine print quality`라는 프롬프트 문구가 후자를 충족시키지는 않는다. [S08](https://helpx.adobe.com/indesign/desktop/print/page-set-up-and-printer-marks/print-bleed-and-slug-areas.html), [S09](https://helpx.adobe.com/indesign/desktop/print/preflight/configure-and-use-the-preflight-panel.html)

## 전체 용어의 데이터 역할

아래 구분은 새 최상위 런타임 enum을 추가하라는 제안이 아니다. 연구 분류이며 실제 반영에서는 기존 필드와 intent dimension에 맞게 변환해야 한다.

| 원문 분류 | 행 수 | 권장 처리 | 피해야 할 자동 변환 |
|---|---:|---|---|
| 모델의 종류·활동 영역 | 23 | 역할·촬영 목적, 필요한 경우 부위/행동에 관한 후보 | agency→특정 외모, fit→fitness |
| 모델 업계 실무 | 20 | 캐스팅 자료·포트폴리오·제작 목적·예약 정보 분리 | test→자연광 무보정 |
| Editorial 계열 | 20 | 출판 문맥, 단일 이미지/연작/지면 산출물 구분 | editorial→강한 무표정·하드광 |
| 광고·브랜드 촬영 | 20 | 캠페인 목적, 제품/인물 위계, 사용 형식 | campaign→항상 로고·제품 클로즈업 |
| 제작 역할 | 22 | 크레딧/역할 메타데이터; 현장 묘사는 별도 후보 | 스태프 이름→완성 사진에 장비 삽입 |
| 사전 제작 과정 | 22 | 기획·참조·일정·테스트 과정 구분 | call sheet→고급스러운 시각 품질 |
| 모델 존재감·태도 | 20 | 요청 문맥의 주관적 목표, 구체적인 자세·시선 관계 | poised→왕족 복식, fierce→항상 찡그림 |
| 포즈·신체 사용 | 25 | 연결된 관절, 하중, 투영된 선·간격, 움직임의 상태 | elongation→신체 비율 변조 |
| 에디토리얼 시각 요소 | 19 | 관계·구도·연출 후보 또는 연작 차원의 계약 | narrative ambiguity→아무런 관계 없는 소품 |
| 전문적인 결과물 | 22 | 미감 목표와 납품 요구를 따로 저장 | publication-ready→파일 검사 통과 |
| 업계 권위·위상 | 16 | 출처가 필요한 경력·게재·유통 정보 | prestige→특정 얼굴·민족·체형 |
| 선택·후반작업 | 16 | 선택 메타데이터, 표면 효과, 실제 작업 이력 분리 | texture→unretouched 인증 |
| 비즈니스 용어 | 16 | 계약·권리·승인·산출물 정보 | 라이선스·동의를 픽셀로 판정 |

`Professional-grade`, `Refined`, `Sophisticated`, `Commanding Presence` 등의 평가는 문맥에 따라 유효한 요청이다. 그러나 수식어를 좁은 시각 프로필의 exact alias로 바로 묶으면 해석권이 데이터로 넘어간다. 먼저 이번 요청의 구체적인 목표를 정하고, 그 목표를 지지하는 선택적 시각 관계를 사용해야 한다.

`Micro-expression`은 특별히 주의할 사례다. 정지 사진은 미묘한 표정의 한 상태를 표현할 수 있지만 짧은 지속 시간이나 비자발성을 증명하지 못한다. 데이터 초안은 미세한 입술·눈 주변 변화처럼 지정된 보이는 상태만 다루고, 시간적 판정은 시퀀스 또는 영상 증거로 남긴다. 이 구분은 진단 용도의 표정 해석 모델을 제안하는 것이 아니다.

`Usage`, `Exclusivity`, `Model Release` 등은 사진 외부의 정보다. ASMP의 라이선스 안내도 계약의 권한 범위와 저작권 소유를 구분한다. 이번 데이터에서 이 용어들은 비시각 메타데이터로 유지하며, 개별 계약의 유효성이나 최신 지역별 법률 요건은 판단하지 않는다. [S12](https://www.asmp.org/wp-content/uploads/ASMP_Legal-Jump-start_2020-03.pdf)

## 현재 저장소에서 확인한 강점과 빈틈

[읽기 전용 조사 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/repo-audit.json)는 사용한 소스 파일들의 SHA-256, git HEAD, 조사한 레코드의 JSON pointer, 정확 일치 진단을 보존한다. 메인 시각 프로필 파일은 333개, 확장 파일을 합친 실제 로더 결과는 566개였다. 메인 파일만 검색한 결과를 전체 데이터 개수로 보고하지 않았다.

| 기존 위치·ID | 관찰한 상태 | 보강 방향 |
|---|---|---|
| `slots.medium/fashion_editorial` | 영어 장르명과 fashion/editorial 태그 | 이름을 유지하고 환경 관계·지면 사용 등 필요한 후보를 별도 연결 |
| `slots.medium/lookbook` | brand lookbook photograph 수준 | 의상 특징의 owner, 가림 관계, 여러 컷의 정보 차이를 추가 |
| `slots.medium/campaign_photo` | advertising campaign photograph 수준 | 제품/인물 중심 여부를 요청에서 정하고 선택 가능한 위계로 구현 |
| `slots.action/posing_editorial` | strong editorial attitude | 강함을 기본으로 고정하지 않고 연결된 몸·의상의 관찰 관계로 세분화 |
| `slots.action/poised_standing` | royal/princess 태그와 upright standing | 일반적 poised를 이 항목에 병합하지 않음; 역할 침범과 앉은 자세 누락 방지 |
| `slots.mood/professional_poised` | professionally poised, work/portrait 태그 | 분위기 보조어로 남기고 실제 지지 관계와 분리 |
| `slots.quality/editorial_quality` | premium magazine print quality | 미감 표현과 기술 납품 검증을 분리 |
| `contrapposto_weight_shift` | 기존 좁은 시각 의미 계약 | 재사용; 새 이름의 중복 프로필 생성 불필요 |
| `contact_sheet_selection_context` | 선택 표시가 있는 컨택트 시트 계약 | 컨택트 시트의 객체·선택 관계를 재사용 |
| `clamshell_dual_source_portrait_light` | 상부 키/하부 필의 기존 조명 계약 | beauty라는 말만으로 강제하지 않고 구체 조명 요청 때 재사용 |
| `sheer_complexion_texture_preservation` | 얇은 피부 표현의 기존 보존 계약 | 범위가 맞을 때 재사용; 일반 직물 질감으로 무작정 확장하지 않음 |

16개 표현의 로컬 정확 일치 진단에서 `contrapposto`, `콘트라포스토`, `contact-sheet selection photograph`, `clamshell dual-source portrait light`는 기대하는 기존 hard profile로 연결됐다. `professional model`, `agency model`, `fashion editorial`, `lookbook`, `campaign`, `print-ready` 등은 exact hard profile을 생성하지 않았다. 넓은 표현이 hard 계약을 만들지 않는 것은 보존할 경계다.

이 결과는 BM25F/embedding 검색에서 관련 후보가 전혀 없다는 증거가 아니다. 또한 v6 후보팩의 실제 노출률이나 채택률 측정도 아니다. 이번 조사는 “어느 authored 레코드를 보강할지”를 위한 기준점이며, 후보 노출 실패를 입증한 실행 결과로 확대하지 않는다.

## 보강할 시각 관계

모든 신규 관계는 다음 구조로 기술했다.

- **대상**: 얼굴 전체가 아니라 특정 메이크업 부위, 의상 전체가 아니라 여밈·옆선처럼 검증할 owner.
- **범위**: 한 이미지, 여러 이미지, 페이지 배치 중 어디서 성립하는지.
- **관계**: 인물–의상–손의 가림, 제품–배경의 분리, 광원–형태, 컷 간 연속성.
- **관찰 조건**: 구성요소 모두가 같은 대상에서 읽히는지.
- **혼동 사례**: 근처 색, 과한 선명도, 장비 수, 비슷한 분위기로 대체하는 실패.
- **해석 한계**: 실제 경력·동의·보정 이력·사용 장비·납품 적합성은 이미지에서 인증하지 않음.

이 구조와 다음 게이트는 외부 표준을 그대로 옮긴 것이 아니라 **출처를 참고하여 작성한 프로젝트용 설계 제안**이다. 각 제안의 source ID는 출발 원리를 뒷받침하며, 완성된 게이트나 생성 효과까지 외부에서 검증했다는 뜻이 아니다.

| 제안 | 핵심 관찰 관계 | 실패 대체물 | 범위 |
|---|---|---|---|
| 정면 캐스팅 기록 (`mep_casting_front`) | adult face and visible hair; front-facing capture | 뷰티 광고의 강한 색조 메이크업 / 즉석사진 흰 테두리만 있는 화보 | single_image |
| 측면 캐스팅 기록 (`mep_casting_profile`) | adult head and neck; side view | 정면 사진의 옆머리 / 원근으로 겹친 두 얼굴 윤곽 | single_image |
| 전신 캐스팅 기록 (`mep_casting_full_length`) | adult full body and clothing; head-to-feet record | 전신이 잘린 뷰티 크롭 / 원근 과장으로 비율이 크게 변한 사진 | single_image |
| 의상 핵심 디테일과 손의 분리 (`mep_garment_clearance`) | declared garment feature and hands; occlusion relation | 버튼을 가린 채 멋진 손 포즈 / 의상이 사라진 얼굴 중심 크롭 | single_image |
| 의상 옆선·두께 읽기 (`mep_garment_side_depth`) | garment side panel and body; oblique depth | 정면 무늬만 보임 / 몸통과 골반이 물리적으로 분리됨 | single_image |
| 움직임과 직물 지연 (`mep_garment_movement`) | moving person and attached garment; one motion phase | 정지 인물 뒤의 무관한 천 / 모든 방향으로 터진 주름 | single_image |
| 제품 중심의 시각 위계 (`mep_product_hero`) | declared hero product; salience hierarchy | 얼굴만 선명하고 제품이 흐림 / 손에 잡혔지만 제품의 주요 형태가 가림 | single_image |
| 주얼리 착용 접점 (`mep_jewelry_contact`) | jewel and wearing body part; contact and highlight | 피부와 금속이 융합됨 / 광점만 있고 장신구 형태가 없음 | single_image |
| 메이크업 디테일의 부위 소유권 (`mep_beauty_detail`) | requested makeup feature; face-region scope | 배경 색을 아이섀도 성공으로 판정 / 다른 부위에만 동일한 색이 있음 | single_image |
| 헤어 볼륨과 외곽 분리 (`mep_hair_outline`) | hair mass and background; silhouette and strands | 머리 뒤의 후광만 있음 / 모발이 배경에 녹아 형태가 안 보임 | single_image |
| 표지 사진의 지정 문구 영역 (`mep_cover_copy_space`) | subject and nominated future text region; layout-compatible photograph | 머리 위 아주 작은 틈 / 여백이 있지만 필수 제품을 잘라냄 | single_image |
| 펼침면 중앙부 보호 (`mep_spread_gutter`) | critical subject features and center fold band; two-page placement | 가로 사진이라는 이유만으로 DPS 통과 / 중앙 접힘에 눈·제품이 잘림 | layout |
| 인물 행동과 환경의 관계 (`mep_environment_relation`) | subject action and relevant environment; contextual relationship | 무관한 고급 배경 / 소품만으로 실제 직업을 확정 | single_image |
| 사지와 몸통의 그래픽 간격 (`mep_graphic_pose`) | connected limbs and torso; projected negative-space shape | 옷 무늬의 삼각형 / 관절이 뒤집힌 채 실루엣만 맞음 | single_image |
| 시선 방향과 화면 내 목표 (`mep_gaze_target`) | visible eyes head and target; gaze alignment | 무조건 카메라 응시 / 목표와 반대인 눈 방향 | single_image |
| 차분한 자세의 지지 관계 (`mep_poised_support`) | body and support surface; balanced stillness | 무조건 무표정 / 허공에 떠 있는 지지 발 | single_image |
| 동작 전환의 미완 상태 (`mep_in_between`) | body action and displaced material; visible incomplete action | 단순 모션 블러 / 정적 포즈에 candid 라벨만 붙임 | single_image |
| 피부·직물의 국소 질감 (`mep_surface_texture`) | declared skin or textile patch; local surface-frequency relation | 균일한 노이즈 오버레이 / 피부는 플라스틱인데 배경 직물만 선명 | single_image |
| 국소 흐트러짐과 정돈의 대비 (`mep_selective_imperfection`) | one specified irregular feature and surrounding structure; local contrast | 전체 흐림·인체 오류 / 여러 무관한 결함을 창의성으로 판정 | single_image |
| 지정한 두 요소의 병치 (`mep_visual_juxtaposition`) | two declared visual elements; contrast with relationship | 무관한 소품 나열 / 색 차이만으로 서사 완성 주장 | single_image |
| 테더 촬영 검토 장면 (`mep_tether_review`) | camera preview and reviewing person; production activity | 노트북만 있는 사진 / 장비가 많다는 이유로 전문성 성공 | single_image |
| 의상 피팅의 실제 조정 (`mep_fitting_adjustment`) | fitter hands and garment on wearer; contact adjustment | 재킷 입은 인물만 / 천에 닿지 않는 핀·손 | single_image |
| 룩북의 컷 간 일관성과 변주 (`mep_series_lookbook`) | ordered collection images; cross-frame continuity | 단일 사진 / 같은 사진의 복제 격자 | series |
| 서사 시퀀스 (`mep_series_story`) | ordered photographs and recurring subject or motif; temporal or conceptual progression | 서로 무관한 화보 모음 / 한 장을 여러 컷이라고 부름 | series |

전체 영어 구성요소, affected dimensions, 활성화 조건, source ID, 한계는 [시각 관계 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/visual-proposals.json)에 있다. `scope`, `source_ids`, `verification_status`는 연구용 필드이며 현재 런타임 스키마에 바로 넣을 수 있다고 가정하지 않는다.

### 의상과 포즈

`Garment-aware`의 실용적 정의는 “옷을 잘 아는 모델”이 아니라 **요청한 의상 특징이 손·팔·가방·머리카락에 가리지 않고 보이는 상태**다. 예를 들어 재킷 여밈을 보여 줄 때는 단추줄과 손의 화면 영역을 분리한다. 소매 끝이 목표라면 손목과 커프스가 접하는 부분을 보존한다. 모델의 얼굴이 훌륭하게 나와도 지정 의상 부위가 가려지면 해당 목표는 실패다.

상품 촬영에서 미세 디테일과 질감을 조명으로 드러내고 반복 촬영의 일관성을 유지한다는 원리는 Profoto의 flat lay 자료에서도 확인된다. 이를 착용 인물 촬영에 적용하는 구체적인 손·옆선·접점 계약은 본 연구의 확장 설계다. flat lay 자료가 모든 on-model 촬영 구도를 인증하는 것은 아니다. [S07](https://www.profoto.com/us/en/studio-solutions/flat-lay/light-shaping-flat-lay/)

`Elongation`이나 `Line Extension`은 요청에 따라 연결된 팔·다리·목선이 화면에서 길게 읽히는 배치가 될 수 있다. 이를 특정 체형으로 변경하거나 신체 연결을 끊는 명령으로 만들지 않는다. `S-Curve`는 인체 자세·도로 구도·톤 커브를 가리킬 수 있으므로 공통 alias로 묶지 않는다. `Broken Line`도 꺾인 투영선의 연출과 해부학적 파손을 분리한다.

`Controlled`라는 표현이 들어 있어도 모든 신체가 정적이어야 하는 것은 아니다. 움직이는 의상 촬영은 한 운동 위상, 연결된 직물, 지지 또는 공중 상태의 일관성을 요구한다. 프롬프트의 물리적 검토와 실제 픽셀의 사지·직물 검토를 별도로 남겨야 한다.

### 표정·태도

`Poised`, `Composed`, `Self-possessed`는 같은 사람의 서 있는 자세·앉은 자세·행동 장면 모두에 사용될 수 있다. 신규 후보는 무표정이나 카메라 응시를 필수값으로 넣지 않고, 보이는 지지와 요청한 정지 상태를 기술한다. 특정 포즈가 정서나 직업을 유일하게 지시한다고 가정하지 않는다.

`Aloof`, `Detached`, `Deadpan`, `Fierce`의 세밀한 표정 체계는 이번에 새 hard 프로필로 만들지 않는다. 이런 표현이 실제 요청의 핵심이면 사용자가 지정한 목표 또는 독립 해석을 먼저 눈·입 주변의 보이는 변화로 작성한다. 기존 감정 의미 데이터와의 중복·충돌을 후속 단계에서 조사한다. “fierce editorial stare”를 모든 editorial의 기본값으로 삼는 것은 피한다.

### 뷰티·헤어·파츠

뷰티 후보는 **초점 부위와 표면 효과의 결합**으로 모델링한다. 파란 아이라이너의 owner는 배경이나 의상이 아니라 지정된 눈 가장자리다. 피부 질감 목표가 볼에 있고 입술에는 매끈한 마감을 원한다면 두 범위는 양립할 수 있다. 전역 스무딩 제거 규칙으로 미감 전체를 바꾸면 안 된다.

헤어 촬영에서는 외곽 실루엣, 볼륨의 밝고 어두운 면, 서로 연결된 모발 그룹을 본다. 광원의 위치와 피사체 방향이 조형적 명암을 만든다는 기술적 원리는 Profoto의 작가 사례가 뒷받침한다. 하지만 장비명이 같은 것, 후광만 있는 것, 긴 머리가 있는 것은 요청한 헤어 형태의 증거가 아니다. [S14](https://www.profoto.com/gr/en/still-photography/tips-tricks/lighting-artistic-portraits-Profoto-D2/ImportedBlogPage)

파츠 모델은 손·발 등의 부위 중심이라는 맥락이다. 사진이 부위를 강조한다고 실제 부위 전문 모델의 직업이 확인되는 것은 아니다. 주얼리 후보는 금속과 피부의 접점·분리된 윤곽·형태를 보존하는 반사를 제안하지만, 보석 진위·가격·정확한 재질은 별도 제품 근거가 필요하다.

### 지면과 연작

`Magazine Cover`에는 표지용 사진 한 장, 타이포가 들어간 표지 디자인, 실제 잡지를 찍은 사진이라는 서로 다른 산출물이 있다. 문구 없는 원사진 요청에 로고를 넣거나, 디자인 요청을 빈 여백만 있는 사진으로 대체하면 실패다. 여백의 위치·크기·중요 피사체와의 관계는 실제 템플릿이나 요청에서 정한다.

DPS는 가로 비율이 아니라 두 페이지의 배치 문제다. 중앙 접힘의 손실 영역을 먼저 정의하고 그 범위에 필수 얼굴·상품 디테일이 들어오는지 확인한다. 의도적으로 중앙을 가르는 디자인도 가능하므로 “항상 중앙을 비운다”는 전역 규칙을 만들지 않는다.

`Lookbook`의 한 컷은 의상 정보를 잘 보여 줄 수 있다. 컬렉션 전체의 일관성을 주장하려면 복수 이미지의 크기·배경·조명·색 관계를 비교해야 한다. `Fashion Story`의 시퀀스는 컷마다 역할과 반복 anchor를 가지며, 같은 이미지를 복제한 contact-sheet 형태로 대체할 수 없다. 단일 이미지용 core에 정면·측면·전신의 서로 다른 촬영을 동시에 요구하지 않는다.

### 제작 현장

Capture One의 작가 workflow는 테더링 중 초점·노출을 확인하고 팀이 프리뷰를 함께 검토하는 사례를 보여 준다. 다른 뷰티 workflow 자료는 촬영부터 RAW 처리·피부 작업·출력까지 단계를 구분한다. 두 자료는 구버전임을 명시하므로 현재 기능·속도·장비 호환성 근거로 사용하지 않았다. [S16](https://www.captureone.com/blog/fashion-photography-workflow), [S17](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow)

여기서 만들 수 있는 것은 **제작 과정 자체를 묘사하는 후보**다. 카메라–프리뷰–검토 행동이 연결되어야 하며, 책상 위 노트북만으로 테더 검토를 판정하지 않는다. `professional shoot`라는 말만 있는 완성 화보에 케이블·스태프를 자동으로 삽입하지 않는다. 제작 직군의 이름을 여러 개 적었다고 결과 이미지의 품질 게이트가 통과하지도 않는다.

## 후보 묶음 설계

후보 묶음은 같은 이미지 또는 같은 산출물에서 함께 성립하는 관계만 결합해야 한다. 후보 수를 늘리기 위해 서로 독립적인 좋은 요소를 무작위로 합치는 방식은 잘못된 owner, 모순된 동작, 필요하지 않은 사람·장비를 추가하기 쉽다.

| 묶음 | 조합 목적 | 주요 제한 |
|---|---|---|
| 정면 디지털 기록 | 모델의 현재 정면 기록사진 | 한 장 전신·측면·정면을 동시에 요구하지 않음 |
| 캐스팅 3뷰 세트 | 정면·측면·전신의 분리된 세 컷 | 별도 이미지 ID 및 인물·의상 연속성 검토 필요 |
| 의상 디테일 우선 룩북 컷 | 특정 의상의 여밈과 옆선 제시 | 앞·옆선이 함께 읽히는 실제 의상인지 먼저 확인 |
| 움직이는 의상의 패션 컷 | 걷기/회전과 직물 움직임 | 하나의 주 동작과 같은 시점으로 제한 |
| 주얼리 중심 광고 컷 | 명시된 주얼리의 착용 형태와 가독성 | 제품을 바꾸거나 실제 브랜드 인증을 주장하지 않음 |
| 국소 메이크업 화보 | 특정 부위 메이크업과 질감 | 동일 얼굴 부위에서 질감과 메이크업 양립성 검토 |
| 헤어 형태 중심 컷 | 요청한 헤어 형태의 외곽·볼륨 | 조명은 형태를 드러내는 수단으로만 선택 |
| 표지용 원사진 | 지정 여백이 있는 표지용 사진 | 표지 완성본 요청이면 별도 타이포 제작 계약 필요 |
| 펼침면 배치안 | 두 페이지 템플릿에 맞춘 배치 | 템플릿에서 중앙 손실 영역을 정하고 배치 후 검사 |
| 환경과 행동이 연결된 인물 컷 | 인물의 작업/상황을 보여주는 한 장 | 주 행동 하나와 관련 환경 하나로 관계를 분명히 함 |
| 조형 포즈의 편집 사진 | 지지가 분명한 각진 정지 포즈 | 현재 인체 구조와 요청된 접근성·자세 제한을 보존 |
| 촬영 현장의 검토 장면 | 디지털 테크/촬영팀의 프리뷰 검토 | BTS가 주제일 때만 활성화 |
| 피팅 현장의 접촉 조정 | 착용자와 스타일리스트의 의상 조정 | 손-의상 접점과 도구·사람 수를 코어에서 명시 |
| 패션 연작 구성 | 연속 모티프와 컷 역할을 가진 연작 | 각 컷을 별도 코어로 동결하고 연속성은 세트에서 판정 |
| 일관된 카탈로그 세트 | 분리된 정면·옆면 등 제품 자료 | 잠근 항목의 컷 간 차이를 검증하며 상품 정보는 컷마다 추가 |

[후보 묶음 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/candidate-bundles.json)은 각 묶음의 component ID, scope, 차원, 요청 조건, 충돌 조건을 보존한다. 예를 들어 제품이 주 목표인 묶음에는 단순히 “광고”라는 라벨보다 제품 형태와 초점 위계가 들어간다. 어떤 장면에서도 쓸 수 있는 만능 editorial bundle은 만들지 않았다.

관계 후보의 영어 표현은 다음과 같이 쓸 수 있다. 이것은 완성 프롬프트나 렌더 실행 자료가 아니라 국소 표현 예시다.

> The declared garment closure or seam is visible along its intended length; the hands occupy separate image regions from that feature; the garment keeps plausible folds and contact with the body.

이 표현에서 의상 이름, 위치, 모델의 행동, 카메라를 새로 정하는 권한은 후보 데이터에 없다. 앞서 동결한 의도가 재킷 여밈을 보여 주려는 것인지 확인한 다음 해당 관계만 적용한다. 후보가 닫힌 pose 차원을 변경한다면 반려해야 한다. 필요한 의미가 이미 코어에 잠겨 있으면 그 의미를 동일하게 보존하는 표현의 보조로만 사용한다.

`reject_substitutes`와 반례 문장은 연구·감사용이다. 이를 그대로 “No ...” 또는 “Avoid ...” 형태의 런타임 프롬프트에 복사하지 않는다. 예시에서 필요한 가독성을 양의 공간 관계로 표현한 이유도 여기에 있다.

## 런타임 데이터에 반영할 순서

**1. 기존 항목의 범위부터 정리한다.** `fashion_editorial`, `lookbook`, `campaign_photo`의 ID를 유지하고 실제 데이터가 지원하는 언어·관계·요청 문맥을 보강한다. `posing_editorial`은 무조건 강렬함을 뜻하지 않게 optional 하위 후보와 분리하는 방향을 검토한다. `poised_standing`의 royal/princess 맥락은 일반 professional 표현과 섞지 않는다.

**2. 단일 이미지 관계부터 좁게 추가한다.** 우선순위는 의상 디테일 가독성, 제품 위계, 구체 부위의 메이크업/질감, 정면·측면·전신 캐스팅 기록이다. 각 항목에는 정확한 owner, 의무 구성요소, 부위가 가려지는 반례, 한국어·영어 표현을 넣는다. 중국어·일본어는 단순 음역 alias를 늘리기보다 요청 문맥과 반례를 확보한 뒤 추가한다.

**3. 기존 의미는 다시 만들지 않는다.** 콘트라포스토·컨택트 시트·클램셸·얇은 피부 표현 등은 기존 profile ID를 재사용한다. 새 캐스팅 기록과 클램셸을 기본 결합하지 않는다. 새 질감 관계도 기존 makeup 프로필이 담당하는 한계를 확인하고 확장해야 한다.

**4. 현재 필드에 맞게 컴파일한다.** 기존 `authored_components` 또는 해당 레지스트리 형식으로 의미·evidence·render gate를 옮기고, 후보 source에는 `concept_units`, `relations`, affected dimensions를 넣는다. 이번 연구 JSON은 이 런타임 계약과 구별되는 스키마다. 이름만 바꾸어 assets에 복사하면 안 된다.

허용 차원에서 얼굴 표면은 `appearance`/`material`, 페이지 배치는 `composition`/`format`, 질감·색·조명은 해당 기존 차원으로 매핑한다. `skin_finish`, `retouching`, `publication_status` 같은 연구 필드명을 임의의 새로운 최상위 intent dimension으로 추가하지 않는다. 실제 `photo_contracts.py`의 허용 집합을 기준으로 검증한다.

**5. 근거와 후보의 권한을 분리한다.** research source URL·기관·용어의 시장 지위를 runtime 의미 권한으로 전송하지 않는다. broad/approximate retrieval은 advisory다. 정확한 요청과 충분한 구성요소가 뒷받침될 때만 hard duty를 만든다. 묶음 선택은 모든 component evidence와 관계 evidence를 요구하고, 일부만 채택한 채 나머지 게이트를 생략할 수 없게 한다.

**6. 인덱스와 노출을 따로 확인한다.** authored 변경이 완료되면 영향받은 인덱스·해시를 새로 생성한다. 그 다음 실제 v6 pack → compact view → candidate detail → composed audit를 통해 노출·선택·표현을 각각 기록한다. 인덱스에 ID가 있다는 사실만으로 개선을 보고하지 않는다. 무관한 holdout·기존 실패·golden 기대값은 이번 연구에 맞춰 바꾸지 않는다.

시리즈와 레이아웃 관계는 후순위다. 단일 사진의 검증 루틴에 억지로 끼우면 “한 장으로 연속성 PASS”라는 잘못된 계약이 생긴다. 산출물 ID·컷 역할·템플릿을 갖춘 별도 검증 단위를 준비한 다음 통합한다.

## 검증 설계와 통과 조건

[46개 사례](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/evaluation-cases.jsonl)는 사람이 작성한 설계 사례다. 신규 구현에 대해 실행하지 않았으며, 독립적으로 숨겨 둔 holdout도 아니다. 사례를 학습·개발에 사용한 후 같은 사례 통과만으로 일반화 성능을 주장하면 안 된다.

| 검증 층 | 확인할 것 | 통과해도 아직 모르는 것 |
|---|---|---|
| 리서치 자료 무결성 | ID·출처·참조·차원·범위·상태 일치 | 의미 품질·실제 노출 |
| authored/runtime 스키마 | 컴파일·계약·기존 데이터 호환 | 후보팩에서의 노출 |
| 검색·후보 노출 | 관련 후보가 실제 pack/view에 존재 | 최종 사용 여부 |
| 선택·프롬프트 감사 | 대상·관계 문구 보존, 열린 차원만 변경 | 실제 이미지의 재현 |
| 원본/축소 픽셀 검토 | 해당 owner의 모든 관찰 조건 | 사용자 선호·인과적 개선 |
| 통제 비교·사용자 평가 | 기준 대비 재현과 선호 | 다른 주제·모델 전체에 대한 일반화 |

반례는 단순한 무관 문장뿐 아니라 **같은 분위기이지만 핵심 관계가 빠진 근접 실패**를 포함해야 한다. 파란 배경만 있고 아이라이너는 검은 사진, 손이 단추줄을 가린 강렬한 포즈, 플라스틱 피부 옆 선명한 니트, 전신 기록에서 잘린 발, 제품이 흐린 고급스러운 얼굴 사진 등이 해당한다.

의상 후보는 지정 부위 전체의 가독성, 제품 후보는 선언된 제품의 윤곽·특징, 피부 후보는 선언된 표면 영역을 검사한다. 다른 이미지나 다른 부위의 성공을 합쳐 통과시키지 않는다. 선택된 필수 게이트는 `all-of`로 평가하고, partial·누락·판정 불가는 자격 통과로 세지 않는다. 생성 실패·차단으로 이미지가 없는 경우는 시각 품질 점수와 구분하여 `UNSCORED`로 남긴다.

후속 이미지 실험은 아래 여섯 계열을 처음부터 고정할 것을 제안한다. 단일 이미지와 시리즈는 비용·표본 단위가 다르므로 첫 비교에서는 앞의 다섯 계열을 우선하고 시리즈는 별도 평가한다.

| 계열 | 핵심 의미 | 가까운 혼동 |
|---|---|---|
| 캐스팅 정면/전신 | 요청한 기록 범위·단순한 표현 | 즉석 필름 테두리·일반 뷰티 |
| 재킷 룩북 | 단추·옆선과 손의 분리 | 강한 포즈·가려진 여밈 |
| 주얼리 광고 | 제품 접점·형태·초점 | 광점·얼굴 중심 크롭 |
| 뷰티 화보 | 지정 메이크업 부위와 질감 | 배경 색·전역 노이즈 |
| 표지용 원사진 | 지정 문구 영역·피사체 보존 | 임의 로고·단순 넓은 배경 |
| 룩북/서사 시리즈 | 반복 anchor와 정보 변화 | 복제 격자·무관한 사진 모음 |

기준 조건은 동일한 원 요청, 참조 자산, 생성 모델·버전·해상도와 가능한 seed를 사용한다. 지원되지 않는 seed 고정은 했다고 기록하지 않는다. 각 계열에서 둘 이상의 독립적인 요청을 잡고 반복 생성 수를 사전에 정한다. baseline은 현재 데이터를, treatment는 보강 데이터를 사용하며 최종 프롬프트 차이와 후보 선택 이력을 남긴다. 한 번의 보기 좋은 결과로 인과적 개선을 판단하지 않는다.

새 예제를 만든 사람에게 새 후보를 미리 보여 주고 baseline도 만들게 하면 격리된 비교가 아니다. 후속 실행에서는 저장소 자료를 보지 않은 작성 단계에서 요청 의미와 기본 코어를 먼저 동결해야 한다. 이 연구를 이미 읽은 작성자의 즉석 재작성은 pre-pack 독립 baseline의 증거로 사용할 수 없다.

주요 지표는 (a) 관련 후보 노출률, (b) 명시적 채택률, (c) owner별 모든 게이트 충족률, (d) 닫힌 차원 침범률, (e) 사람의 선호다. 노출과 채택의 분모, 생성 실패 수, 판정 불가 수를 따로 보고한다. 장르명 때문에 외모·포즈·사람 수가 바뀌거나, 인쇄 사양·시리즈 연속성을 단일 이미지로 통과시키는 사례가 하나라도 발견되면 그 계약을 승격하지 않는다.

## 우선순위와 남은 불확실성

가장 먼저 반영할 묶음은 **의상 가독성, 제품 중심 관계, 캐스팅 기록, 국소 메이크업·질감**이다. 요청 빈도에 대한 측정 데이터는 없으므로 이 순서는 시장 수요 순위가 아니라, 기존 데이터의 추상성·관찰 가능성·검증 난이도를 종합한 설계 판단이다.

다음은 표지용 원사진, 헤어 형태, 연결된 그래픽 포즈, 전환 동작이다. 제작 현장 후보는 BTS 요청에 한정한다. 시리즈·DPS는 산출물 검증 구조가 필요하므로 더 뒤에 둔다. 유명 잡지나 브랜드명을 하나의 고정 룩으로 환원하는 후보는 이번에 추가하지 않는다. 출판사·브랜드별로도 시대·캠페인·작가·이미지마다 시각 문법이 다르기 때문이다.

`Blue-chip Editorial`, `Hand Discipline`, `Profile Control`, `Skin Retention` 등 모든 표현에 통일된 업계 정의가 있다는 증거를 확보한 것은 아니다. 분류표는 이런 용어를 삭제하지 않고 맥락 보조어 또는 연구 제안으로 남긴다. 출처가 약한 표현을 hard alias로 승격하지 않는 것이 현재로서는 적절하다.

17개 자료는 용어의 핵심 구분과 기술적 원리를 지지한다. 자료에서 사진의 생성 성능을 측정한 것은 아니며, 이미지 자체를 체계적으로 표본 추출하여 미감을 코딩한 연구도 수행하지 않았다. 특히 주얼리·헤어·손 포즈의 세부 게이트는 공통 사진 원리를 바탕으로 만든 설계이므로 후속 실제 이미지 검토가 필요하다.

## 산출물과 재현

- [원문 13개 분류·261행](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/input-inventory.json)
- [259개 고유 표기의 처리 판단](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/term-map.json)
- [17개 출처와 사용 한계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/sources.json)
- [24개 시각 관계 제안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/visual-proposals.json)
- [15개 후보 묶음](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/candidate-bundles.json)
- [기존 슬롯 매핑과 반영 우선순위](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/integration-plan.json)
- [46개 설계 검증 사례](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/evaluation-cases.jsonl)
- [기존 데이터와 정확 일치 진단](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/repo-audit.json)
- [읽기 전용 조사 스크립트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/audit_repository.py)
- [산출물 무결성 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/validation.json)
- [산출물 검사 스크립트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/model-editorial-professional-20260912/validate_research.py)

저장소와 인덱스를 변경하지 않는 조사 재현 명령:

```bash
.venv/bin/python docs/research-evidence/photo-prompt/model-editorial-professional-20260912/audit_repository.py
```

이 명령은 현재 checkout을 다시 읽어 연구 폴더의 `repo-audit.json`을 갱신한다. 과거 결과를 고정 보존해야 할 때는 기존 JSON을 별도로 복사한 후 실행한다. 신규 후보팩을 생성하거나 웹·이미지 API를 호출하지 않는다.

## 출처

자료 열람 기준일은 2026-09-12다. 발행일이 확인되지 않은 웹 문서는 추측 날짜로 확정하지 않았다. 검색의 crawl 날짜는 발행일이 아니다. 날짜를 추정한 구버전 Capture One 자료는 현행 제품 기능이 아닌 workflow의 역사적 사례에만 사용했다.

- **S01** Models.com. [Choosing the correct client, date and title when uploading a new work](https://help.models.com/article/60/choosing-the-correct-client-date-and-title-when-uploading-a-new-work). 미표기. 사용 범위: 작업 유형 분류와 unpublished/test 작업의 Other 분류. 한계: 기관별 분류이며 보편적 화풍 정의가 아님.
- **S02** Adobe. [Bring narratives to life with editorial photography](https://www.adobe.com/creativecloud/photography/type/editorial-photography.html). 미표기. 사용 범위: 출판·콘셉트·이야기 및 맥락 중심의 편집 사진. 한계: 교육용 설명이며 모든 editorial의 촬영·보정 방식을 규정하지 않음.
- **S03** Elite Model Management. [Get scouted: Guide for images](https://elitemodelmanagement.com/get-scouted.web). 미표기. 사용 범위: 전신·근접·측면, 정면 자연광, 화장 없는 단순 사진을 요구하는 기관 사례. 한계: 기관별 지원 지침; 모든 모델·사진에 일반화하지 않음.
- **S04** Select Model Management. [Apply: Advice](https://apply.selectmodel.com/advice). 미표기. 사용 범위: 지원 사진과 오픈콜에서 화장 없는 자연스러운 모습을 선호하는 사례. 한계: 사진 구성 전체의 표준을 제공하지 않음.
- **S05** Getty. [Working with Sculpture: About Sculpture in Western Art](https://www.getty.edu/education/for_teachers/curricula/sculpture/background1.html). 미표기. 사용 범위: 한 다리에 하중을 둔 contrapposto. 한계: 포즈 정의 근거이며 직업적 능력·성격 근거가 아님.
- **S06** Nikon / Malike Sidibe. [The Portrait as Assignment, Documentary and More](https://www.nikonusa.com/learn-and-explore/c/ideas-and-inspiration/the-portrait-as-assignment-documentary-and-more). 미표기. 사용 범위: 시리즈의 일관성과 변주, 모델과 협력하는 디렉팅. 한계: 단일 작가 사례; 고정된 프로 모델 포즈 표준 아님.
- **S07** Profoto. [Light shaping for flat lay photography](https://www.profoto.com/us/en/studio-solutions/flat-lay/light-shaping-flat-lay/). 미표기. 사용 범위: 제품 디테일·질감과 일관된 조명 운용. 한계: 장비 공급자 자료; on-model 전체 표준이나 성능 비교 아님.
- **S08** Adobe. [Print bleed and slug areas in InDesign](https://helpx.adobe.com/indesign/desktop/print/page-set-up-and-printer-marks/print-bleed-and-slug-areas.html). 열람 페이지의 현행 문서. 사용 범위: bleed와 slug 및 출력 영역의 구분. 한계: 특정 프린터 요구값은 별도; 시각적 여백이 기술 적합성을 보장하지 않음.
- **S09** Adobe. [Configure preflight panel in InDesign](https://helpx.adobe.com/indesign/desktop/print/preflight/configure-and-use-the-preflight-panel.html). 열람 페이지의 현행 문서. 사용 범위: 폰트·링크·넘친 텍스트·해상도 등 출력 검사. 한계: 검사 프로필 범위만 검증하며 미적 품질은 검증하지 않음.
- **S10** Adobe. [How to use frequency separation in Photoshop](https://www.adobe.com/products/photoshop/frequency-separation.html). 미표기. 사용 범위: 질감·미세 디테일과 색·톤을 구분하는 편집 기법. 한계: 결과 이미지로 사용 기법을 역추론할 수 없음.
- **S11** Adobe. [Retouch large areas with Healing Brush in Photoshop](https://helpx.adobe.com/photoshop/desktop/repair-retouch/clean-restore-images/healing-brush-tool.html). 열람 페이지의 현행 문서. 사용 범위: 주변 질감·조명·톤을 맞추는 부분 복원. 한계: 피부의 유일한 미감 기준이나 보정 이력 증거가 아님.
- **S12** ASMP. [ASMP Guides: Legal Jump-start](https://www.asmp.org/wp-content/uploads/ASMP_Legal-Jump-start_2020-03.pdf). 2020-03 (파일명). 사용 범위: Chapter 3의 라이선스 범위·기간·소유권 구분. 한계: 미국 중심의 역사적 실무 안내; 최신 개별 법률 자문이나 지역별 계약 기준으로 사용하지 않음.
- **S13** Adobe Stock. [Editorial Requirements](https://helpx.adobe.com/uk/stock/contributor/help/editorial-requirements.html). 2021-05-16 (검색 메타데이터). 사용 범위: 뉴스·공익 기록을 포함하는 stock editorial 맥락. 한계: 플랫폼 정책과 패션 에디토리얼 미감을 혼합하지 않음; 현행 제출 자격은 본 연구 대상 아님.
- **S14** Profoto / Lindsay Adler. [3 photography tips for lighting artistic portraits](https://www.profoto.com/gr/en/still-photography/tips-tricks/lighting-artistic-portraits-Profoto-D2/ImportedBlogPage). 2021-10-26. 사용 범위: 광원의 위치·크기·인물 방향과 조형적 얼굴 명암의 관계. 한계: 기술 사례; 해당 장비·화풍의 강제 선택 근거 아님.
- **S15** Prada. [Spring/Summer 2025 Woman: Acts Like Prada](https://www.prada.com/hk/en/pradasphere/campaigns/2025/ss-woman.html). 2025 캠페인. 사용 범위: 캠페인에도 인물 페르소나와 문학적 이야기의 결합이 존재. 한계: 광고에는 서사가 없다는 이분법의 반례; 시장 전체 빈도 추정 아님.
- **S16** Capture One. [Capture One Pro in the fashion industry](https://www.captureone.com/blog/fashion-photography-workflow). 약 2016 (검색 추정; 정확일 미확인). 사용 범위: 테더링 중 팀이 촬영 이미지를 검토하고 그레이드하는 workflow. 한계: 기술 workflow 사례; 현행 버전 UI·속도·카메라 호환성의 근거 아님.
- **S17** Capture One / Michael Woloszynowicz. [Portrait and beauty retouching workflow](https://www.captureone.com/blog/portrait-and-beauty-retouching-workflow). 약 2017 (검색 추정; 정확일 미확인). 사용 범위: 테더 촬영부터 최종 출력까지 이어지는 뷰티 작업 단계. 한계: 작가별 과정; 보정 프로그램 사용 여부는 픽셀만으로 증명 불가.
