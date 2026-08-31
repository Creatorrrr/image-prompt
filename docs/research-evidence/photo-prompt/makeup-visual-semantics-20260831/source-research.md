# 메이크업 시각 의미·후보팩 강화 리서치

- 조사일: 2026-08-31
- 적용 범위: `photo-prompt-image-generator`의 시각 의미 프로필, 후보 슬롯, 메이크업 계열 라우팅 및 회귀 테스트
- 검증 범위: 데이터 구조·라우팅·프롬프트 표현. 실제 생성 이미지의 픽셀 충족과 사용자 선호는 이번 조사 범위에서 검증하지 않음.

## 입력 경계

참조 대화에는 “여성의 메이크업을 표현하는 단어나 요소를 다양하게 조사해 달라”는 질문만 남아 있고, 그에 대한 조사 답변이나 첨부 파일은 없었다. 따라서 특정 누락 답변을 복원했다고 주장하지 않고, 그 질문이 요구하는 넓은 키워드 공간을 다음처럼 재구성했다.

- 전체 인상: 내추럴, 노메이크업 메이크업, 글램, 스모키, 에디토리얼
- 베이스: 커버리지, 색 균질화, 투명도, 피부 결, 표면 반사
- 눈썹: 방향, 아치, 밀도, 탈색, 결
- 아이섀도: 눈꺼풀·크리즈·아래 눈꺼풀의 색 배치와 그라데이션
- 아이라이너: 속눈썹선과의 관계, 선의 경로, 굵기, 끝점, 여백
- 속눈썹: 분리, 볼륨, 길이 분포, 군집, 색, 상·하 균형
- 치크: 볼 중심, 광대-관자, 눈 아래, 콧등 연결 등 색 분포
- 컨투어·하이라이트: 어두운 제품과 밝은 제품의 얼굴 면 배치
- 입술: 색 분포, 경계, 표면 마감
- 장식: 젬, 데칼, 포일, 페인팅, 코스메틱 점
- 마모: 새로 바른 상태, 리브드인 경계, 비·눈물, 전이·뭉침, 부분 소실

사용자 질문에는 여성이 언급되지만, 메이크업 자체의 시각 축은 성별·민족·연령을 소유하지 않는다. 후보 데이터는 `human` 전용으로 두고, 여성 피사체가 필요할 때는 별도 `subject` 계층이 소유하도록 했다.

## 근거가 지지하는 분해 방식

### 1. 얼굴 부위와 제품 기능을 먼저 분리한다

FDA의 제품 분류는 눈썹, 아이라이너, 아이섀도, 인조 속눈썹, 마스카라를 서로 다른 하위 범주로 두며, 비안구 메이크업에서도 블러셔, 파운데이션, 립스틱·글로스를 구분한다. 이 분류는 미학적 표준은 아니지만, `eye_makeup_line` 하나에 마스카라와 아래 속눈썹을 넣는 기존 소유권이 부정확하다는 강한 구조 근거가 된다.

- 출처: [FDA Cosmetic Product Categories and Codes](https://www.fda.gov/cosmetics/registration-listing-cosmetic-product-facilities-and-products/cosmetic-product-categories-and-codes)
- 데이터 영향: `eye_makeup_line`, `lash_style`, `eyeshadow_style`, `brow_style`, `cheek_makeup`, `complexion_coverage`, `lip_finish`

### 2. 커버리지와 마감은 독립 축이다

CHANEL의 파운데이션 가이드는 커버리지를 light/medium/full로, 마감을 matte/satin/luminous로 별도 선택하게 한다. 따라서 “얼마나 가리는가”와 “빛을 어떻게 반사하는가”를 한 `skin_finish` 후보로 합치지 않고 `complexion_coverage`와 `skin_finish`로 분리했다. 이 자료는 제품 선택 가이드이므로 보편적 인지 임계값이나 피부 가치 판단에는 사용하지 않았다.

- 출처: [CHANEL Find Your Perfect Foundation](https://www.chanel.com/ca-en/makeup/find-your-perfect-foundation/)
- 데이터 영향: `sheer_translucent_complexion_coverage`, `light_selective_complexion_evening`, `medium_buildable_complexion_coverage`, `full_opaque_complexion_coverage`, `selective_spot_concealment`

### 3. 메이크업은 색만이 아니라 모양·질감·위치다

CVPR 2021 연구는 실제 메이크업 전이를 색 변환만으로 다룰 수 없고 패턴의 shape, texture, location을 별도 처리해야 한다고 설명한다. CVPR 2020 PSGAN은 부분 영역과 농도를 제어하는 전이를 다룬다. ACCV 2020 연구도 identity, lip, eye, face makeup을 분리된 구성으로 모델링한다. 이 연구들은 생성 모델의 성공이 곧 사람의 미적 인식 기준임을 뜻하지 않지만, 후보팩에서 부위·배치·패턴을 독립적으로 소유해야 한다는 근거가 된다.

- 출처: [Lipstick Ain't Enough, CVPR 2021](https://openaccess.thecvf.com/content/CVPR2021/html/Nguyen_Lipstick_Aint_Enough_Beyond_Color_Matching_for_In-the-Wild_Makeup_Transfer_CVPR_2021_paper.html)
- 출처: [PSGAN, CVPR 2020](https://openaccess.thecvf.com/content_CVPR_2020/html/Jiang_PSGAN_Pose_and_Expression_Robust_Spatial-Aware_GAN_for_Customizable_Makeup_CVPR_2020_paper.html)
- 출처: [Local Facial Makeup Transfer, ACCV 2020](https://openaccess.thecvf.com/content/ACCV2020/html/Sun_Local_Facial_Makeup_Transfer_via_Disentangled_Representation_ACCV_2020_paper.html)
- 데이터 영향: 모든 모듈형 메이크업 슬롯, 특히 `makeup_decoration`

### 4. 피부 마감은 조명과 분리된 광학 증거가 필요하다

파운데이션층 연구는 실제 피부 위 제품층의 reflectance, transmittance, 도포량을 공간 맵으로 다룬다. 피부 글로스 연구는 표면 specular reflection과 subsurface diffuse reflection, 조명 기하를 구분한다. 따라서 `glass_skin_specular_diffuse_balance`는 “반짝임” 한 단어가 아니라 넓은 확산광, 얼굴 면을 따르는 제한된 정반사, 남아 있는 모공·미세결, 조명·과노출 혼동 방지를 동시에 요구한다.

- 출처: [Foundation reflectance/transmittance distribution, Optics Express 2022](https://pubmed.ncbi.nlm.nih.gov/35299429/)
- 출처: [High sensitivity optical measurement of skin gloss](https://pmc.ncbi.nlm.nih.gov/articles/PMC5611917/)
- 데이터 영향: `glass_skin_specular_diffuse_balance`, `skin_finish`, `complexion_coverage`

### 5. 구체적 스타일명은 보이는 관계로 번역한다

MAKE UP FOR EVER Academy의 교육 범주는 complexion/eye/lip을 분리하고, smoky lash line, graphic liner, false lashes, eyeshadow gradients, makeup-no-makeup, contouring/highlighting을 별도 기술로 다룬다. Maybelline의 cut crease 예시는 밝은 mobile lid와 더 짙은 crease 위 색 사이의 깨끗한 경계를 핵심 관계로 설명한다. 이 자료들은 실무 예시이며 보편적 인식 표준은 아니므로, 스타일명을 그대로 합격 조건으로 쓰지 않고 관찰 가능한 구성으로만 추상화했다.

- 출처: [MAKE UP FOR EVER Academy brochure](https://academy.makeupforever.com/on/demandware.static/-/Library-Sites-AcademySharedLibrary/en_IM/v1755272468628/PDF/Brochure_Academy_en.pdf)
- 출처: [Maybelline cut crease tutorial](https://www.maybelline.com/makeup-tips/eye/eyeshadow-makeup-tutorials/cut-crease-eyeshadow-tutorial)
- 데이터 영향: `smoky_eye_diffused_gradient`, `cut_crease_lid_separation`, `graphic_negative_space_eyeliner`, `no_makeup_makeup_layering`, `contour_highlight_cosmetic_sculpting`

### 6. 치크와 립은 색 이름보다 분포가 핵심이다

NARS의 블러시 예시는 볼 중심, 광대-관자, 양 볼과 콧등을 잇는 W형 등 서로 다른 배치를 제시한다. L'Oréal의 blurred lip 예시는 중앙에 가장 진한 색을 두고 바깥으로 확산하며 단단한 경계를 남기지 않는다고 설명한다. 이 자료에서 특정 얼굴형에 대한 “보정” 또는 “어울림” 판단은 채택하지 않고, 오직 색이 놓이는 좌표와 경계만 사용했다.

- 출처: [NARS How To Wear Blush](https://www.narscosmetics.com/USA/blog/how-to-wear-blush)
- 출처: [L'Oréal How To Create Blurred Lips](https://www.lorealparisusa.com/beauty-magazine/makeup/lip-makeup/how-to-create-blurred-lips)
- 데이터 영향: `cheek_makeup`, `sunburn_blush_cross_face_distribution`, `lip_color_placement`, `gradient_lip_center_distribution`

### 7. 마모는 스타일이 아니라 시간에 따른 제품층 상태다

파운데이션 마모 연구는 마스크 접촉 뒤 색 전이와 얼굴 위 제품층 저하를 주요 관찰 대상으로 둔다. 이 축은 “그런지” 같은 분위기와 분리해 coverage loss, patchiness, agglomeration, transfer처럼 보이는 제품층 증거를 소유해야 한다.

- 출처: [A preliminary study to understand the effects of mask on tinted face cosmetics](https://pubmed.ncbi.nlm.nih.gov/33651451/)
- 데이터 영향: `makeup_wear_state`

### 8. 글래스 스킨의 유행 설명은 광학 연구로 제한한다

Maybelline 자료는 glass skin makeup을 smooth/luminous/dewy/reflective로 소개하고 커버리지와 광택 제품을 함께 설명한다. 다만 “poreless”, “healthy”, “youthful” 같은 마케팅·가치 표현은 후보나 게이트에 넣지 않았다. 광학 연구와 결합해 모공·미세결을 반드시 남기고, 유분 핫스팟·플라스틱 보정·과노출을 실패 대체물로 명시했다.

- 출처: [Maybelline glass skin makeup tutorial](https://www.maybelline.com/makeup-tips/face/face-artistry-makeup-tutorials/how-to-get-glass-skin-with-makeup)
- 데이터 영향: `glass_skin_specular_diffuse_balance`

## 후보팩 소유권

| 슬롯 | 소유하는 질문 | 소유하지 않는 것 | 후보 수 |
|---|---|---|---:|
| `complexion_coverage` | 제품층이 피부를 얼마나/어디까지 가리는가 | 광택, 피부 건강, 피부색 가치 | 5 |
| `skin_finish` | 피부 표면이 빛을 어떻게 보이는가 | 커버리지 양 | 기존 20 |
| `brow_style` | 눈썹 털 방향·모양·대비 | 아이라인·아이섀도 | 기존 5 |
| `eyeshadow_style` | 눈꺼풀·크리즈·아래 눈꺼풀의 색 배치 | 선, 속눈썹 | 6 |
| `eye_makeup_line` | 아이라이너의 경로·여백·끝점 | 마스카라·속눈썹 가닥 | 5 |
| `lash_style` | 속눈썹 가닥의 분리·볼륨·길이·색 | 아이라인 선 | 6 |
| `cheek_makeup` | 치크 색의 얼굴 위 분포 | 얼굴형, 실제 염증 | 6 |
| `face_sculpting` | 어두운/밝은 제품의 얼굴 면 배치 | 타고난 골격, 조명 그림자 | 5 |
| `makeup_decoration` | 피부 위 부착·페인팅 패턴 | 타투, 로고, 하이라이트 오인 | 5 |
| `lip_color_placement` | 입술 안쪽-바깥쪽 색 분포와 경계 | 표면 광택 | 5 |
| `lip_finish` | 매트·밤·스테인·글로스·새틴 표면 | 색 분포와 립 라인 | 5 |
| `makeup_wear_state` | 시간·접촉·물에 따른 제품층 변화 | 원래 의도한 스타일명 | 6 |

기존 `makeup_style`은 전체 룩을 위한 레거시 집합으로 유지하되, 세부 표현은 위 슬롯이 우선 소유한다. 기존 `eye_makeup_line`에 있던 `colored_mascara_accent`, `lower_lash_statement_detail`은 `lash_style`로 이동했다. `lip_finish`의 경계 중심 후보는 실제 표면 마감 후보로 교체하고, 경계·분포는 `lip_color_placement`가 소유한다.

## 하드 시각 의미 프로필

다음 8개는 exact/contextual term이 요청에 직접 등장할 때만 하드 의무가 된다. 임베딩·BM25F 유사도는 선택 후보일 뿐 하드 의무로 승격되지 않는다.

1. `no_makeup_makeup_layering`: 얇거나 선택적 커버리지 + 피부 변화 유지 + 모든 포인트의 절제 + 맨얼굴/풀 글램/보정 혼동 방지
2. `smoky_eye_diffused_gradient`: 속눈썹선 최심부 + 연속 그라데이션 + 아이 영역 통일 + 멍/다크서클/라이너 단독 방지
3. `cut_crease_lid_separation`: 크리즈 경계 + 두 색면 대비 + 경계 연속성 + 자연 주름/플로팅 라인/헤일로 방지
4. `graphic_negative_space_eyeliner`: 떠 있는 선 + 연속 피부 여백 + 정리된 끝점 + 끊긴 라인/주름 그림자 방지
5. `glass_skin_specular_diffuse_balance`: 넓은 확산광 + 제한된 정반사 + 미세결 유지 + 유분/과노출/플라스틱 보정 방지
6. `gradient_lip_center_distribution`: 안쪽 중심 최심부 + 바깥 연속 감쇠 + 부드러운 경계 + 풀 커버/투톤/조명 방지
7. `sunburn_blush_cross_face_distribution`: 양쪽 높은 볼 + 콧등 연결 + 부드러운 화장 경계 + 실제 화상/발진/붉은 조명 방지
8. `contour_highlight_cosmetic_sculpting`: 국소 어두운 제품 + 국소 밝은 제품 + 얼굴 면 정렬·블렌딩 + 골격/그림자/후처리 방지

## 주요 혼동 경계

| 목표 | 통과에 필요한 보이는 관계 | 실패 대체물 |
|---|---|---|
| 스모키 아이 | 속눈썹선에서 시작해 위·바깥으로 농도가 연속 감소 | 두꺼운 아이라인, 다크서클, 멍, 안와 그림자 |
| 컷 크리즈 | mobile lid와 crease 위 색 사이의 정리된 경계 | 자연 쌍꺼풀선, 플로팅 라이너, 헤일로 아이 |
| 네거티브 스페이스 라이너 | 라인과 눈꺼풀 사이 연속된 맨피부 여백 | 끊긴 아이라인, 누락 픽셀, 아이섀도 컷아웃 |
| 글래스 스킨 | 넓은 확산광과 면을 따르는 제한된 정반사, 남은 모공 | 유분 핫스팟, 과노출, 링라이트 점, 피부 보정 |
| 그라데이션 립 | 같은 색이 안쪽 중심에서 바깥으로 감쇠 | 균일 풀 립, 두 색 옴브레, 입 안 그림자 |
| 선번 블러시 | 양 볼과 콧등을 잇는 화장 색 분포 | 실제 화상·발진·열감, 붉은 조명, 볼만 붉음 |
| 컨투어·하이라이트 | 같은 조명 아래 국소 제품 배치가 양쪽 면에서 읽힘 | 강한 측광, 타고난 골격, 수술 추론, 전역 닷지번 |

## 연구 제한과 재사용 규칙

- FDA 분류는 제품 범주 근거이지 미적 의미 표준이 아니다.
- CV 연구의 partial-region/pattern 제어는 데이터 소유권을 지지하지만, 생성 결과의 인간 인식 합격을 증명하지 않는다.
- 브랜드·아카데미 자료는 실무 배치 예시이며 유행명이나 보편적 선호를 확정하지 않는다.
- 여성만 포함한 연구 표본이나 마케팅의 여성 대상 표현은 성별·연령·민족 기본값으로 전환하지 않는다.
- “healthy”, “youthful”, “flattering”, “imperfection” 같은 가치·건강·매력도 표현은 런타임 후보와 픽셀 게이트에서 제외한다.
- 피부 광학은 조명, 카메라, 톤 매핑의 영향을 받으므로 실제 이미지 합격은 네이티브 픽셀과 썸네일을 모두 봐야 한다.
- 이번 변경은 이미지 생성을 수행하지 않았다. 프로필/후보/프롬프트 테스트 통과는 픽셀 재현 성공이나 사용자 선호를 의미하지 않는다.
