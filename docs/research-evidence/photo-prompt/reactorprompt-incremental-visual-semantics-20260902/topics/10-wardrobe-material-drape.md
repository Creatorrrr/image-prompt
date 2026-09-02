# 10. 의상 실루엣·구성·소재·질감·드레이프·스타일링

## 결론

- **결정: `proposed`**. 이 문서는 연구·설계 결과이며 런타임 자산, 생성 인덱스, 스크립트, 테스트, 픽스처에는 아무 변경도 적용하지 않았다.
- 924개 비어 있지 않은 프롬프트를 전수 스캔한 결과 의상 명사는 775개 레코드에 나타났고, 의복과 70자 이내에 소재명이 함께 나타나는 고정 휴리스틱은 377개를 찾았다. 의상은 이 코퍼스의 주변 장식이 아니라 반복되는 주요 시각축이다.
- 그러나 **프롬프트의 소재명과 픽셀에서 관찰 가능한 소재 증거는 같지 않다**. 14개 게시물의 실제 이미지 28장을 검토했을 때 실루엣, 층 경계, 여밈, 주름 방향, 투과와 불투명 층의 대비는 비교적 잘 읽혔다. 반면 `silk`, `cotton`, `suede`, `faux shearling`, `chiffon` 같은 정확한 섬유·재료 조성은 단일 사진만으로 확정할 수 없었다.
- 현행 베이스라인에는 이미 21개의 직접적인 의복/소재 하드 프로필과 `wardrobe_style` 78개, `garment_detail` 86개, `surface_material` 137개, `texture` 134개의 후보가 있다. 주요 공백은 후보 수가 아니라, **같은 의복의 실루엣·구성·층·표면·드레이프·힘·조명 증거를 한 소유 관계로 묶는 타입형 중간 표현**이다.
- 따라서 새 기본 의상 취향이나 광범위한 소재 하드 라우팅을 추가하지 않는다. 먼저 post-core advisory 계약 `photo-wardrobe-material-relation/v1`을 제안하고, 기존 후보들을 `garment_id`와 `component_id`로 결속한다. 하드 프로필은 정확한 요청 문구가 `satin directional luster`나 `velvet pile/nap`처럼 비대체적이고 관찰 가능한 경우에만 좁게 검토한다.
- 픽셀 판정은 `thumbnail`의 전체 실루엣/층 순서와 `native`의 직조·편성·오픈워크·봉제·파일/냅·가장자리 증거를 분리하되, 활성 프로필은 **모든 게이트가 한 결과에 공존해야 한다**. 일부만 보이면 실패이며, 필요한 영역이 가려지거나 해상도가 부족하면 `UNSCORED`다.
- 이미지에서 실제 신분, 직업, 문화적 진정성, 국적·민족성, 가격·브랜드·희소성, 섬유 조성, 성격, 매력, 건강, 신체 가치 또는 정체성을 추론하지 않는다. 보고서의 사람 관련 표현은 보이는 의복, 포즈, 동작, 표면과 공간 관계에만 한정한다.

## 범위와 표본 방법

### 고정 근거

- 대상 스킬 기준 리비전: `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- 매니페스트: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- 매니페스트 SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- 갤러리 스냅샷 SHA-256: `35142b192966bd01eefa7c7cfdc05e7ca83a2f1c2ac43a7e34e6e693689cc64f`
- 번역 스냅샷 SHA-256: `d2483fc1eefc941ddf2a51137ac2114cea0de61e8be3c152c00d49cfe5ce6586`
- 범위: 1,182개 게시물, 4,908개 이미지, 924개 비어 있지 않은 프롬프트, 904개 고유 프롬프트 본문, 258개 프롬프트 누락, ID 1565–2746.
- 브리프가 고정한 authored-source SHA-256:
  - 시각 의무: `64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc`
  - 태그/후보: `5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00`
  - 품질 레이어: `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f`
  - 생성 시각 프로필 인덱스: `4d674dc00cfa05897f837a7b53410d18766edb8556b1378190523e6e4d1b6626`
- 생성 인덱스는 파생물로만 보았고 authored source로 사용하지 않았다. 공유 작업 트리의 무관한 변경은 보존했다.

### 프롬프트 전수 스캔

매니페스트에서 `prompt`가 있고 `prompt_missing == false`인 924개 레코드를 모두 읽었다. 다음의 겹치는 휴리스틱을 사용했다.

1. 의복 명사: dress, skirt, blouse, shirt, jacket, coat, trousers, jeans, uniform, robe, bodysuit, corset 등.
2. 소재/섬유: cotton, denim, leather, silk, satin, chiffon, linen, wool, velvet, lace, organza, mesh, knit, brocade 등.
3. 구성: seam, stitch, hem, neckline, collar, cuff, zipper, button, panel, lining, strap, bodice, closure 등.
4. 표면: weave, woven, ribbed, knit, embroidery, lace, quilt, fray, wrinkle, nap, grain, matte, glossy, sheer 등.
5. 드레이프: fold, drape, pleat, gather, cling, billow, pool, tension 등.
6. 실루엣/핏: fitted, loose, oversized, cropped, high-waisted, tailored, structured, voluminous, flared 등.
7. 인접 관계: 소재↔의복 70자, 드레이프↔의복 80자, 표면↔의복 80자, 실루엣↔의복 80자 이내.
8. 별도 관계: 광학 직물, 층 토폴로지, 소재-조명 반응, 마모 상태, 의복 운동.

계수는 모두 **프롬프트 텍스트 존재 증거**이며 픽셀 구현 성공률이 아니다. 범주가 서로 겹치므로 합산하지 않았다. `top`, `panel`, `grain`, `texture`, `tension`처럼 사진·위치·세트에도 쓰이는 단어가 있어 고정 근접창만으로 의미를 확정하지 않았다.

### 픽셀 표본

- 표본: **14개 게시물의 실제 코퍼스 이미지 28장**.
- 선택법: 의상/소재 관계가 풍부한 양성 후보와 인접 혼동 사례를 ID 앞·중간·뒤 구간에서 고른 뒤, 각 게시물에서 매니페스트 순서상 처음 다운로드된 2장을 검사했다.
- ID: `1712, 1903, 1909, 2103, 2121, 2215, 2297, 2326, 2481, 2548, 2554, 2629, 2703, 2744`.
- 전체 28장을 동일 크기 접촉 시트에서 먼저 비교하고, 소재 경계가 핵심인 `1712/1903/1909/2103/2121/2215/2297/2326/2481/2548/2554/2629/2703/2744`의 대표 이미지를 원본 크기로 다시 확인했다.
- 이 표본은 4,908장 전체의 빈도 추정치가 아니다. 프롬프트가 풍부한 패션/인물 장면을 의도적으로 과대표집했다.

## 프롬프트 측 발견과 계수

### 관계 휴리스틱 매치

| 프롬프트 측 휴리스틱 | 매치 레코드 | 해석 경계 |
|---|---:|---|
| 의복 명사 1개 이상 | 775 | 의복이 언급됐다는 뜻뿐이며 구조 증거를 보장하지 않음 |
| 소재↔의복 70자 이내 | 377 | 소재명이 해당 의복을 수식할 가능성이 높지만 조성 진위를 보장하지 않음 |
| 구성어와 의복어 동시 존재 | 443 | 같은 의복의 구성인지 문장 단위 확인이 필요 |
| 표면↔의복 80자 이내 | 549 | `texture`, `glossy`, `grain`의 촬영/피부/배경 용례가 섞일 수 있음 |
| 실루엣↔의복 80자 이내 | 492 | 인체 실루엣, 프레이밍, 포즈와 혼동 가능 |
| 드레이프↔의복 80자 이내 | 251 | 주름이 의복 자체인지 앉은 자세·압박·바람 결과인지 별도 판정 필요 |
| 광학 직물 관계 | 232 | sheer/mesh/lace와 층·의복어의 근접 관계 |
| 소재↔조명 반응 | 188 | 실제 표면 반응인지 단순 하이라이트 지시인지 확인 필요 |
| 명시적 층 토폴로지 | 38 | `layered over/under`, `underlayer`, `overlay`, 층 경계 등 |
| 마모 상태↔의복 | 35 | frayed/distressed/wrinkled/wet/stained 등의 의복 근접 관계 |
| 의복 운동 관계 | 32 | 흐름·펄럭임·바람과 의복 부위가 근접한 경우 |

### 자주 나타난 명시 단어

레코드별 중복을 제거한 단어 존재 수다. 이것도 의미 성공률이 아니다.

- 의복: `dress 204`, `skirt 167`, `shirt 93`, `shorts 87`, `sleeve 85`, `blouse 65`, `jacket 44`, `uniform 43`, `blazer 39`, `cardigan 38`, `jeans 32`, `trousers 32`, `hem 30`.
- 소재/구조: `lace 102`, `knit 95`, `satin 78`, `ribbed 74`, `leather 68`, `cotton 64`, `denim 59`, `metallic 32`, `velvet 22`, `silk 17`, `linen 14`, `wool 14`, `chiffon 12`, `mesh 10`, `organza 9`.
- 구성: `neckline 120`, `straps 94`, `collar 80`, `panels 63`, `seams 51`, `belt 47`, `button 41`, `bodice 34`, `hem 30`, `cuffs 23`, `stitching 15`, `waistband 12`.
- 드레이프/변형: `folds 138`, `pleated 78`, `gathered 54`, `draped 30`, `folded 27`, `drape 18`, `wrinkles 23`, `creases 18`, `distressed 10`, `frayed 4`.

### 프롬프트 문법에서 반복된 유용한 관계

1. **전체 실루엣 + 지역 구성 + 국소 표면**: 예를 들어 드레스 전체 윤곽, 보디스/허리/밑단 연결, 레이스 구멍이나 새틴 광택을 따로 서술한다.
2. **층 대비**: 투명 오버레이와 불투명 안감, 카디건과 이너 톱, 레이스와 바탕 천처럼 서로 다른 층을 경계로 증명한다.
3. **힘의 결과**: 앉은 자세의 무릎 주름, 허리의 장력, 손/가방 접촉에 의한 압박, 바람에 따른 밑단 이동을 요청한다.
4. **소재-조명 결속**: 새틴의 방향성 광택, 벨벳 냅 방향, 시어 원단의 투과, 가죽의 국소 반사를 조명과 함께 쓴다.
5. **혼동 대체물 배제**: 프린트 레이스, 전체 레이스, 유리/투명 몸, 장식 선, 끊긴 여밈, 프레이밍으로 가려진 구조를 명시한다.

반대로 `elegant`, `luxury`, `soft`, `flowy`, `fitted`, `silky`, `textured` 같은 집합 형용사만 있는 경우는 어떤 구조·표면·힘 관계를 보여야 하는지 결정하지 못한다.

## 픽셀 측 관찰과 표본 ID

아래는 실제 전달된 코퍼스 픽셀에 한정한 관찰이다. 프롬프트에 적힌 섬유명이나 실제 상품·브랜드·신분을 픽셀 사실로 바꾸지 않았다.

| ID | 검사 수 | 픽셀에서 보인 의상·소재 관계 |
|---:|---:|---|
| 1712 | 2 | 검은 상의의 광택 있는 띠, 반복 버클/스터드, 반투명 소매/외층이 분리된다. 반투명 면은 보이지만 직조를 확정할 만큼의 구조는 약해 `sheer textile`과 매끈한 투명 면의 혼동 대조로 유용하다. |
| 1903 | 2 | 매끈한 밝은 의복에 주름을 따라 이동하는 넓은 방향성 하이라이트, 허리에서 방사되는 주름, 어깨·허리의 돌출 장식 경계가 보인다. 정확한 satin/silk 조성은 픽셀만으로 확정할 수 없다. |
| 1909 | 2 | 바깥층의 짧고 조밀한 파일처럼 보이는 가장자리, 매끈한 갈색 외피, 세로 골지 상의, 청색 바지의 솔기·주름이 서로 다른 표면군으로 분리된다. `faux` 여부나 실제 섬유 조성은 비시각적이다. |
| 2103 | 2 | 흰 상의의 세로 리브와 소매 투과, 러플 칼라·커프, 비대칭 밑단과 중력 주름이 읽힌다. 흰색과 역광만으로 투명성을 판정하지 않고 리브/가장자리와 몸판 대비를 함께 볼 수 있다. |
| 2121 | 2 | 바탕 캐미솔과 네크라인의 좁은 오픈워크 트림, 매듭, 큰 루프의 카디건 표면이 분리된다. 레이스 트림과 니트 구조의 양성 사례이며 얕은 심도에서도 연결 경계가 남는다. |
| 2215 | 2 | 검은 스트랩리스 의복의 전체적인 몸통 윤곽과 매트한 넓은 면은 읽히지만 긴 밑단 전체는 프레임 밖이다. `long dress`나 전체 드레이프를 평가하기에는 구조 증거가 부족한 프레이밍 대조다. |
| 2297 | 2 | 청색 카디건의 세로 리브, 흰 이너의 레이스 가장자리, 흰 하의의 여러 겹 밑단과 압축 주름이 구분된다. 프롬프트의 cotton/chiffon/lace/tulle 각각의 조성은 픽셀로 분해되지 않지만 층 순서와 질량 차이는 읽힌다. |
| 2326 | 2 | 흰 모자의 해진 가장자리와 금속 스터드, 겹쳐 입은 두 상의, 분홍 가방의 스트랩/버클은 보인다. 높은 근접 셀피 크롭 때문에 청바지 구조와 가방의 전체 구성은 일부만 보여 “모든 솔기/질감” 요청이 증거 예산과 충돌한다. |
| 2481 | 2 | 밝은 블라우스의 모인 소매와 오픈워크 칼라, 노란 하의의 반복 플리츠, 양말 끝의 좁은 레이스 띠가 읽힌다. cotton/velvet 같은 정확한 소재명은 육안 구조만으로 확정하지 않았다. |
| 2548 | 2 | 상체의 성형 솔기, 사선 어깨 띠, 꽃무늬 오버레이와 매끈한 불투명 언더스커트의 두 밑단이 분리된다. 레이스 계열 표면과 새틴 계열 광택의 층 대비는 강하지만, 모든 실 교차가 썸네일에서 보이지는 않는다. |
| 2554 | 2 | 불투명 몸판, 빛을 통과시키는 부풀린 소매, 검은 오픈워크 숄더 패널, 큰 반투명 보우, 여러 겹 검은 하의가 한 프레임에 공존한다. 투과·오픈워크·불투명 층의 경계가 가장 강한 양성 사례다. |
| 2629 | 2 | 청색 바지의 솔기·포켓·해진 밑단과 주름, 파란 부츠의 균일한 매트 표면이 보인다. denim 계열 구조는 비교적 강하지만 suede는 짧은 냅의 방향 변화가 충분히 드러나지 않아 정확한 소재 판정이 어렵다. |
| 2703 | 2 | 어두운 매끈한 상체와 서로 다른 색·투과도를 가진 여러 겹의 가벼운 하의가 분리되고, 각 층의 중력 주름과 가장자리가 보인다. tulle/organza 명칭 자체보다 “얇은 망상 층의 반복”이 관찰 가능한 핵심이다. |
| 2744 | 2 | 흰 셔츠와 청색 니트 조끼의 네크라인·암홀·층 경계가 보이고, 조끼의 미세 리브가 셔츠의 평활한 면과 대비된다. 강한 햇빛/그림자 때문에 셔츠의 정확한 cotton weave는 제한적이다. |

### 표본에서 드러난 전역·지역·국소 계층

- **전역**: 드레스/바지/상의의 전체 외곽선, 길이, 부피 배분, 층의 큰 순서가 첫눈 판독을 지배했다.
- **지역**: 네크라인, 어깨 띠, 허리 접합, 커프, 밑단, 오버레이/안감 경계가 의복 타입을 결정했다.
- **국소**: 리브, 오픈워크 셀, 실 교차, 파일/냅, 프레이, 스티치, 미세 광택은 지역 구조가 먼저 살아 있을 때만 의미를 강화했다.
- 국소 텍스처가 선명해도 전체 의복이 크롭되면 길이·연속성·실루엣 계약을 증명하지 못했고, 반대로 전체 실루엣이 보여도 작은 트림·냅·봉제 구조는 `native`에서만 판정 가능했다.

## 프롬프트/픽셀 정렬과 발산

### 정렬이 강했던 조건

1. **서로 다른 층이 실제 경계를 가질 때**: 2121, 2297, 2548, 2554, 2703.
2. **구성선이 전체 형태와 연결될 때**: 1903의 방사 주름, 2481의 플리츠, 2548의 보디스 솔기와 밑단.
3. **표면 반응이 조명·주름 방향을 따를 때**: 1903의 넓은 광택 흐름, 2554의 소매 투과, 1909의 파일/외피 대비.
4. **마모·트림이 소유 경계에 붙을 때**: 2326의 모자 프레이와 스터드, 2121의 네크라인 트림.

### 발산과 혼동

1. **정확한 섬유명 과잉 주장**: 한 장의 합성 이미지에서 cotton, silk, polyester, faux/real, suede를 확정할 수 없다. 시각 계약은 우선 `crisp plain-weave-like`, `directional lustrous`, `short matte nap-like`, `openwork`처럼 관찰 가능한 표면 클래스로 저장해야 한다.
2. **샷 스케일 충돌**: 2326은 모자와 상체 표면은 강하지만 청바지와 가방 전체 구성을 증명하지 못한다. 한 프레임에 전체 실루엣과 현미경 수준 실 교차를 모두 요구하지 말고 P0 증거 영역을 정해야 한다.
3. **포즈가 만든 가짜 핏/드레이프**: 앉기, 무릎 굽힘, 팔의 압박, 몸통 비틀림은 같은 의복의 주름과 외곽선을 크게 바꾼다. 소재 유연성과 포즈 압박을 분리해야 한다.
4. **조명이 만든 가짜 소재**: 강한 스펙큘러, 블룸, 클리핑은 평활한 합성 표면을 satin/latex처럼 보이게 하고, 평면 조명은 실제 리브·냅을 지운다.
5. **프린트와 구조 혼동**: 레이스 무늬, 자수 무늬, 타탄, 브로케이드가 평면 프린트로 대체될 수 있다. native에서 구멍, 실 높이, 능직 대각, 바탕 직조, 국소 장력 중 해당 증거가 필요하다.
6. **투명성 대체**: 피부가 보인다는 사실만으로 시어 직물을 증명할 수 없다. 직물 가장자리/봉제선/직조와 겹침에 따른 불투명도 변화가 함께 있어야 한다.
7. **스타일 라벨의 비시각적 누수**: “luxury”, “business”, “school”, “traditional”, “romantic”은 가격·직업·기관·문화·관계를 픽셀에서 확정하지 못한다. 요청 의미는 보존하되 판정은 가시 구조로 제한해야 한다.

## 기존 데이터 중복과 소유층

### 베이스라인 authored source의 강점

기준 리비전에서 직접적인 의복/소재 범주 하드 프로필은 21개다.

- 일반/제도/광학: `school_uniform_institutional_system`, `one_piece_dress_construction`, `sheer_garment_optical_layering`, `military_uniform_duty_system`, `wearable_protective_armor_system`, `commercial_appeal_revealing_armor`.
- 문화 한정 의복 토폴로지: `qipao_standing_collar_diagonal_closure_system`, `kebaya_front_open_blouse_sarong_system`, `nivi_sari_continuous_pleat_pallu_system`, `andean_poncho_central_opening_panel_system`, `west_african_grand_boubou_volume_system`.
- 일반 구성 토폴로지: `button_down_collar_fastening`, `cold_shoulder_cutout_topology`, `wrap_front_overlap_closure`, `bifurcated_one_piece_jumpsuit`, `culotte_cropped_wide_leg_topology`, `capri_trouser_below_knee_clear_ankle_gap`, `gathered_ankle_voluminous_trouser`, `balloon_curved_leg_tapered_hem`, `wrap_skirt_overlap_closure`, `lace_trim_attached_edge`.

이 프로필들은 정확 용어 활성화, 가시 성분 그룹, 혼동 대체물, 프롬프트 증거 필드, thumbnail/native 게이트를 이미 갖는다. 특히 `one_piece_dress_construction`, `sheer_garment_optical_layering`, `wrap_front_overlap_closure`, `lace_trim_attached_edge`는 이번 코퍼스에서 반복된 연속성·층·경계·오픈워크 문제와 직접 겹친다.

기준 리비전의 후보 슬롯은 다음 규모다.

| 슬롯 | 항목 수 | 현재 역할 |
|---|---:|---|
| `wardrobe_style` | 78 | 전체 앙상블/스타일 조합 |
| `garment_detail` | 86 | 여밈, 층, 트림, 주름, 구조 디테일 |
| `surface_material` | 137 | 표면/재료 클래스와 일부 광학·역학 반응 |
| `texture` | 134 | 국소 질감, 실·파일·프린트·마모 증거 |

`photo_prompt_quality_layers.json`은 `portrait_editorial`에 `material styling`을 두고, `material_world` 경로에서 네 슬롯을 함께 검색한다. `photographic_integration`은 공유 조명, 반사색, 접촉 그림자, 주름·마모 같은 물성 흔적을 요구한다. 이 기능은 좋은 사진적 통합 지원이지만 의복 구조의 의미 소유자는 아니다.

### 구조적 공백

1. 네 후보 슬롯이 평면 목록으로 풍부하지만, **같은 의복·같은 부위·같은 층을 가리킨다는 타입형 결속**이 없다.
2. `surface_material`의 소재명, `texture`의 국소 표면, `garment_detail`의 구조, `wardrobe_style`의 앙상블이 독립 선택되면 서로 다른 의복의 증거가 잘못 합쳐질 수 있다.
3. 드레이프에는 `support point`, 중력, 장력, 압축, 바람, 움직임 단계의 소유 필드가 없다. `flowing folds`는 인과 없이 쉽게 장식 문구가 된다.
4. 정확한 소재명과 픽셀에서 확인 가능한 `appearance class`가 분리되지 않는다.
5. 전신 실루엣과 native 국소 증거 사이의 **증거 예산/프레이밍 우선순위**가 데이터로 표현되지 않는다.
6. 생성 프로필 인덱스는 검색 파생물이며 이 공백의 소유층이 아니다.

### 권장 소유 경계

| 의미 | 소유층 | 규칙 |
|---|---|---|
| 사용자가 명시한 의복/소재/스타일 | pre-pack authorial core와 semantic anchor | 요청 문구를 보존한다. v6 intent-lock에서는 지원되지 않는 `wardrobe` 차원을 새로 만들지 말고 `appearance` 등 지원 차원과 리터럴 증거로 결속한다. |
| 정확하고 비대체적인 의복 의미 | `photo_prompt_visual_obligations.json` | exact/request-scoped 하드 프로필만. 모든 성분과 게이트가 활성 결과에 공존한다. |
| 앙상블/구성/표면/질감 아이디어 | `photo_prompt_tags.json` | post-core advisory. BM25F/embedding-only 히트는 의무나 게이트를 만들지 않는다. |
| 사진적 표면 가시화 | `photo_prompt_quality_layers.json` | 조명, 샷 스케일, 환경 결속, 물성 흔적을 지원하되 소재 정체를 정의하지 않는다. |
| 검색 | 생성 시각 프로필/의미 인덱스 | authored source에서 재생성되는 파생물. 직접 편집 금지. |
| 실제 구현 판정 | pixel review ledger/held-out 결과 | prompt/audit PASS와 분리. thumbnail/native와 사용자 판단도 분리. |

## 제안 시각 의미 성분과 혼동 경계

| 관찰 성분 | 저장할 관계 | 주요 혼동 음성 |
|---|---|---|
| 전체 의복 실루엣 | 외곽선, 길이, 상·중·하 부피 분포, 좌우 비대칭 | 몸 포즈, 렌즈 왜곡, 크롭, 그림자가 만든 외곽선 |
| 의복 토폴로지 연속성 | 네크라인→몸판→허리→밑단 또는 몸판→크로치→두 다리 경로 | 매칭 세퍼레이트, 가려진 연결, 프린트된 가짜 선 |
| 부품·패널 | 패널 ID, 경계 경로, 인접 부품, 몸 부위 | 그림자, 액세서리, 배경 선 |
| 여밈·부착 | 단추/지퍼/끈/봉제의 source→target 결속과 장력 | 장식 단추, 떠 있는 끈, 닫힘과 무관한 보우 |
| 층 순서 | outer/inner, overlap, underlayer, 보이는 경계 | 하나의 프린트 면, 그림자 띠, 피부/투명 아티팩트 |
| 가장자리·밑단 | 자유 가장자리, 접힌 가장자리, 봉제된 가장자리, 두께 | 흐림/헤일로, 머리카락, 배경 테두리 |
| 직물 구조 | woven/knit/nonwoven/openwork/unknown과 보이는 실/셀 방향 | 인쇄 격자, 노이즈, 업스케일 샤프닝 |
| 국소 표면 릴리프 | 리브, 자수 실 높이, 브로케이드 보충사, 파일/냅 | 평면 프린트, 조명 패턴, 필름 그레인 |
| 광학 반응 | 불투명도, 투과, 방향성 광택, 확산, 겹침 밀도 | 과노출, 블룸, 유리, 젖음, 피부 투명화 |
| 역학/드레이프 | 굽힘 반경, 주름 밀도, 주름 방향, 회복, 처짐 | `flowy` 형용사만, 무작위 주름 텍스처 |
| 힘 소유 | 중력, 지지점, 신체/소품 압축, 인장, 바람, 운동 방향 | 포즈와 무관한 떠 있는 옷, 원인 없는 펄럭임 |
| 핏·접촉 | 느슨/밀착 영역, 압력점, 장력선, 여유량 변화 | 신체 형상 추론, 보정 필터, 그림자만으로 만든 핏 |
| 움직임 단계 | 정지/들림/펄럭임/가라앉음, 선행 가장자리, 뒤따르는 층 | 모션 블러만, 머리카락만 움직임, 중력 반대 주름 |
| 마모·상태 | 건조/젖음, 주름, 프레이, 필링, 얼룩의 위치와 원인 | 전역 노이즈, 인쇄된 손상, 배경 오염 |
| 스타일링 관계 | tucked/untucked, open/closed, over/under, attached/detached | 단순 근접 배치, 가려진 레이어, 임의 액세서리 |
| 증거 스케일 | silhouette/region/native-detail의 우선순위와 최소 화면 점유 | 모든 디테일을 한 원거리 프레임에 요구 |

### 추론 상한

- 픽셀은 “새틴처럼 방향성 광택이 있는 매끄러운 표면”을 지지할 수 있지만 실제 silk 섬유, 가격, 브랜드, 진품 여부를 증명하지 않는다.
- uniform/costume/traditional label은 보이는 의복 시스템을 기술할 뿐 실제 직업, 학교, 군 소속, 국적, 민족성, 종교, 계층, 문화적 진정성을 증명하지 않는다.
- 핏과 실루엣은 의복-포즈-카메라 관계로만 기술하고 신체 건강, 이상적 비율, 매력, 가치 또는 정체성으로 바꾸지 않는다.

## 후보팩/데이터 제안

### 1. `photo-wardrobe-material-relation/v1` advisory 계약

새 후보 단어를 대량 추가하는 대신 기존 네 슬롯의 선택을 다음 post-core 타입형 관계로 결속한다.

```json
{
  "contract_version": "photo-wardrobe-material-relation/v1",
  "status": "advisory",
  "source_core_sha256": "<frozen core hash>",
  "garments": [
    {
      "garment_id": "g1",
      "garment_type": "<request literal or candidate class>",
      "label_provenance": "request_exact | authorial_observation | advisory_candidate",
      "priority": "P0 | P1 | optional",
      "silhouette": {
        "outer_contour": "<observable outline>",
        "length_landmarks": ["<visible landmark>"],
        "volume_distribution": ["<upper/mid/lower relation>"],
        "pose_camera_confounds": ["<confound>"],
        "required_view": "full | three_quarter | regional"
      },
      "components": [
        {
          "component_id": "g1-c1",
          "role": "bodice | sleeve | panel | waistband | hem | trim | lining",
          "boundary_path": "<traceable visible path>",
          "layer_index": 0,
          "attached_to": ["<component id>"],
          "closure_relation": "<source -> target or null>"
        }
      ],
      "material": {
        "requested_label": "<literal or null>",
        "visual_class": "woven | knit | nonwoven | openwork | pile_nap | smooth_lustrous | unknown",
        "fiber_claim_status": "request_label_only | externally_known | visually_unresolved",
        "surface_cues": ["<weave/rib/open cell/thread relief/nap cue>"],
        "optical_behavior": ["opaque | translucent | directional_luster | diffuse_matte"],
        "mechanical_behavior": ["crisp_fold | fluid_fold | elastic_recovery | structured_volume"],
        "confidence": "high | medium | low",
        "confusion_negatives": ["<false substitute>"],
        "evidence_scale": "thumbnail | native | both"
      },
      "drape": {
        "gravity_direction": "<frame-relative vector>",
        "support_points": ["<body/prop/closure point>"],
        "tension_sources": ["<closure/stretch/contact>"],
        "compression_zones": ["<visible zone>"],
        "motion_driver": "none | body_motion | wind | object_contact",
        "leading_edge": "<component id or null>",
        "fold_response": "<observable fold path>"
      },
      "styling_relations": [
        {"type": "over | under | tucked_into | open_over | attached_trim", "target_garment_id": "<id>"}
      ]
    }
  ],
  "proof_budget": {
    "primary_scale": "silhouette | construction | material_detail",
    "minimum_visible_regions": ["<region ids>"],
    "thumbnail_gates": ["<all-of gate ids>"],
    "native_gates": ["<all-of gate ids>"]
  },
  "inference_ceiling": "visible_garment_relations_only"
}
```

이 계약은 사용자 의미를 새로 만들지 않는다. frozen core의 요청을 보존하고, post-core 후보를 채택할 때만 같은 의복/부위로 결속한다. 점수·순위는 공개 의무가 아니며 선택하지 않은 후보는 아무 게이트도 만들지 않는다.

### 2. 기존 후보를 관계 노드로 재사용

새 평면 후보보다 다음 기존 계열을 관계형으로 묶는 것이 우선이다.

- 구성: `one_piece_continuous_bodice_to_hem`, `wrap_front_diagonal_overlap_tie`, `pleat_fold_ridge_valley_geometry`, `lace_trim_edge`.
- 표면: `woven_poplin_crisp_fold_surface`, `rib_knit_stretch_recovery_surface`, `fluid_satin_luster_drape_surface`, `fine_wool_cashmere_matte_pile_surface`.
- 질감: `suede_nap_texture`, `soft_velvet_pile_texture`, `crochet_loop_texture`, `embroidered_thread_texture`.
- 상태/힘: `wrinkled_linen_texture`, `damp_fabric_edges`, `static_cling_fabric`, `sunlit_fabric_weave`, `sheet_fold_contact_shadow_surface`.

각 선택에는 `garment_id`, `component_id`, `affected_dimensions`, `surface_owner`, `force_owner`, `required_view`, `confusion_negatives`를 붙인다. `wardrobe_style`은 앙상블만, `garment_detail`은 구조만, `surface_material`은 표면/광학/역학만, `texture`는 국소 증거만 소유하게 한다.

### 3. 좁은 exact 하드 프로필 후보

다음 두 프로필은 일반적인 `silk`, `soft`, `luxury`, `flowy`, `velvet` 단독어가 아니라 정확한 비대체적 요청 문구에만 적용하는 설계 후보다.

#### `satin_directional_luster_drape_surface`

- exact 후보 문구: `satin directional luster`, `satin sheen following folds`, `새틴 방향성 광택`, `주름을 따르는 새틴 광택`.
- 필수 성분: 연속된 의복 표면, 주름/곡률 방향, 그 방향을 따라 이동하는 넓고 매끄러운 하이라이트, 어두운 면에서 남는 재료 연속성, 가장자리/봉제 경계.
- 혼동 음성: 전역 블룸, 젖은 피부, 금속/비닐, 무작위 흰 줄, 과노출, 배경 실크 드레이프.
- 하드 게이트: thumbnail의 매끄러운 전체 표면/드레이프, native의 하이라이트-주름 동조와 경계 연속성, 두 스케일 모두에서 표면이 한 의복에 소유됨.

#### `velvet_pile_nap_direction_surface`

- exact 후보 문구: `velvet pile direction`, `velvet nap changing with direction`, `벨벳 파일 방향`, `방향에 따라 달라지는 벨벳 냅`.
- 필수 성분: 짧은 파일/냅처럼 보이는 미세 표면, 방향 변화에 따른 밝고 어두운 영역, 접힘/압박에서의 국소 변화, 의복 가장자리와 봉제 연속성.
- 혼동 음성: 평평한 검은 매트 천, 사진 노이즈, 스웨이드 라벨만, 전역 그라디언트, 피부/머리카락 광택.
- 하드 게이트: thumbnail의 벨벳 계열 부피·톤 흐름, native의 짧은 파일/방향 변화·압박 반응, 한 의복 표면의 연속성.

두 후보 모두 실제 섬유 조성이나 가격을 판정하지 않는다. BM25F/embedding-only 근접 히트는 advisory로만 남는다. 렌더 캘리브레이션과 독립 held-out 없이 registry 승격하지 않는다.

### 4. quality layer 제안

`portrait_editorial` 아래에 의미가 아닌 촬영 지원 refinement `wardrobe_material_proof`를 제안한다.

- P0가 실루엣이면 네크라인·허리·밑단 또는 허리·크로치·두 다리의 필요한 랜드마크를 한 프레임에 남긴다.
- P0가 표면이면 한 국소 영역을 native에서 실/셀/리브/냅/봉제선이 읽힐 크기로 확보하고, 다른 영역의 전체 의복 의미를 과도하게 주장하지 않는다.
- P0가 층이면 서로 다른 두 가장자리와 겹침 방향, 각 층의 불투명도/주름 반응을 함께 보여준다.
- 같은 조명 아래에서 의복과 주변 표면의 반사·투과를 결속하되, 조명이 소재 정체를 대신하지 않는다.

## 회귀 및 held-out 테스트

### 패키지/구조 테스트

1. 모든 `garment_id`, `component_id`, `attached_to`, `target_garment_id` 참조가 닫혀 있어야 한다.
2. 한 표면 후보는 정확히 하나의 `garment_id/component_id` 소유자를 가져야 한다.
3. `fiber_claim_status=visually_unresolved`일 때 실제 섬유 조성·가격·진품 표현을 런타임 증거로 올리지 않는다.
4. 하드 프로필은 exact/request-scoped 경로만 의무와 게이트를 만들고 BM25F/embedding-only 결과는 선택 전까지 advisory다.
5. `proof_budget.primary_scale`과 최소 가시 영역이 맞지 않으면 compose 전에 경고하거나 하드 프로필에서 fail-closed한다.
6. 생성 인덱스는 authored registry/tag source에서만 재생성되며 직접 수정하지 않는다.

### 프롬프트 행동 causal pairs

| 변화 쌍 | 보존해야 할 것 | 달라져야 할 것 |
|---|---|---|
| 같은 셔츠, woven poplin ↔ rib knit | 셔츠 토폴로지/색/포즈 | 직조/리브, 주름 반경, 신축 장력 |
| 같은 드레스, matte crepe ↔ directional satin-like | 실루엣/여밈/조명 위치 | 광택 흐름과 표면 미세결 |
| 같은 레이스 무늬, print ↔ attached openwork trim | 바탕 의복/무늬 위치 | 실제 구멍, 부착선, 자유 가장자리 |
| 같은 투명도, glass-like sheet ↔ sheer textile | 투과량/배경 | 직물 가장자리, 직조, 겹침 밀도 |
| 같은 의복, standing ↔ seated | 소재/구성 | 접촉 압박과 포즈 유래 주름만 |
| 같은 의복, still air ↔ crosswind | 구성/소재 | leading edge, 뒤따르는 층, 힘 방향 |
| 같은 벨벳 계열 표면, 정면광 ↔ 사광 | 냅/구성 | 방향성 밝기와 미세 그림자 |
| 같은 전체 의상, full-length ↔ close crop | 요청 의미 | 각 샷이 증명할 수 있는 게이트 범위 |

### 코퍼스 회귀 픽스처 후보

- `1903`: 매끄러운 방향성 광택과 방사 주름의 양성. 전역 블룸이나 금속광만 남으면 음성.
- `2103`: 리브/가장자리/부분 투과가 공존하는 시어 상의 양성. 흰 과노출 또는 투명 몸만이면 음성.
- `2121`: 다른 바탕 천에 붙은 좁은 오픈워크 트림과 니트 루프 양성. 프린트 레이스/전체 레이스/평면 리브 음성.
- `2297`: 카디건-이너-여러 겹 하의 순서 양성. 한 흰 덩어리 또는 그림자 띠만이면 음성.
- `2326`: 모자 프레이/스터드 국소 양성인 동시에 전체 청바지·가방 구조 판정의 하드 음성.
- `2481`: 플리츠 ridge/valley 반복과 소매 gather 양성. 인쇄된 세로 줄 또는 무작위 주름 음성.
- `2548`: 꽃무늬 상층과 매끈한 불투명 하층의 두 밑단 양성. 레이스 프린트와 한 층만이면 음성.
- `2554`: 불투명 몸판, 투과 소매, 오픈워크 숄더, 반투명 보우의 다중 층 양성. 유리/블룸/경계 없는 투명화 음성.
- `2629`: 바지의 솔기·포켓·프레이 양성, suede 냅 판정은 음성/미결. 파란 매트 색만으로 냅 PASS 금지.
- `2703`: 여러 투과 층의 독립 가장자리와 중력 주름 양성. 모션 블러나 투명 노이즈 층 음성.
- `2744`: 셔츠-니트 조끼 경계와 표면 대비 양성. 파란색 페인트 패치나 한 평면 음성.

### thumbnail all-of 게이트

1. 요청된 전체 의복 타입 또는 우선 실루엣이 첫눈에 읽힌다.
2. 중요한 outer/inner 층 순서와 최소 두 개의 경계가 분리된다.
3. 소재 행동이 의복 전체 질량과 일치한다. 가벼운 층은 무거운 판처럼, 구조적 층은 연기처럼 보이지 않는다.
4. 포즈·크롭·배경·그림자가 요청 실루엣을 대신하지 않는다.
5. 광학/운동 프로필이면 투과·광택·leading edge가 한 의복에 소유된다.

### native all-of 게이트

1. 요청한 직조/편성/오픈워크/파일/자수 중 해당 미세 구조가 실제 표면에 남는다.
2. 봉제선, 여밈, 트림 부착, 밑단과 패널 경계가 연결되고 떠 있거나 융합되지 않는다.
3. 주름은 지지점·장력·압축·중력·바람 중 선언된 원인과 방향이 일치한다.
4. 광택/투과/냅 변화는 접힘, 겹침, 조명 방향에 따라 일관되며 전역 필터처럼 붙지 않는다.
5. 프레이, 주름, 필링, 젖음 같은 상태 변화는 국소 소유와 경계를 가진다.
6. 정확한 섬유·가격·브랜드·문화·직업·정체성의 비시각적 추론이 판정에 들어가지 않는다.

활성 하드 프로필은 thumbnail/native의 필요한 게이트가 모두 통과해야 한다. 부분 구현은 실패다. 필요한 영역이 크롭·가림·해상도로 판정 불가하면 0점이 아니라 `UNSCORED`다. 사용자 미적 판단은 별도이며 이 연구에서는 `UNSCORED`다.

## 한계와 경계 결정

- 픽셀 표본은 28장/14게시물로 요구 최소치를 넘지만 패션·인물 프롬프트를 의도적으로 많이 골랐다. 4,908장 전체의 구현 빈도나 생성기 일반 성능을 말하지 않는다.
- 코퍼스 이미지는 실제 의류 시편이 아니라 전달된 이미지다. 촉감, 섬유 조성, 제조법, 진품성, 가격, 내구성은 사진만으로 확인하지 않았다.
- 프롬프트 계수는 정규식/문자 근접 휴리스틱이다. 다의어와 장면 내 다른 표면이 섞일 수 있어 모두 prompt-side 탐색 근거로만 사용했다.
- 각 게시물의 첫 2장을 본 결정적 표본이라 동일 프롬프트의 전체 변동성을 측정하지 않는다. 반복 생성·독립 블라인드 평가도 수행하지 않았다.
- 새 이미지 생성, pack 생성, prompt audit, runtime request, render gate 실행, 사용자 수용 평가는 하지 않았다. 따라서 package/prompt/render/user 모든 승격 증거는 아직 없다.
- 현행 데이터의 강한 중복 때문에 새 후보 단어의 수량 확대는 우선순위가 아니다. 타입형 소유 관계와 confusion holdout을 먼저 적용한 뒤, 구조 검증과 독립 렌더 검증을 거쳐야 한다.
- 최종 경계 결정은 **`proposed`**다. 가장 작은 재사용 가능한 변화는 새 글로벌 스타일 기본값이 아니라 `garment -> component -> material behavior -> force/drape -> proof scale` 관계를 post-core advisory 데이터로 추가하는 것이다.

## 증거 부록

### 표본 이미지 경로

모든 경로의 기준 디렉터리는 `generated/reactorprompt-export-20260902-incremental/`이다.

- `images/1712_DZAPLGXmrtc_01.jpg`, `images/1712_DZAPLGXmrtc_02.jpg`
- `images/1903_DZuB8XHmv97_01.jpg`, `images/1903_DZuB8XHmv97_02.jpg`
- `images/1909_DZt68dkmugh_01.jpg`, `images/1909_DZt68dkmugh_02.jpg`
- `images/2103_DaeuWCbmkn_01.jpg`, `images/2103_DaeuWCbmkn_02.jpg`
- `images/2121_DaiPCsRmumH_01.jpg`, `images/2121_DaiPCsRmumH_02.jpg`
- `images/2215_Da9br-QmrnQ_01.jpg`, `images/2215_Da9br-QmrnQ_02.jpg`
- `images/2297_DbcrE0YGs_G_01.jpg`, `images/2297_DbcrE0YGs_G_02.jpg`
- `images/2326_DbiZ4y3GrIt_01.jpg`, `images/2326_DbiZ4y3GrIt_02.jpg`
- `images/2481_DcBobVmmrBX_01.jpg`, `images/2481_DcBobVmmrBX_02.jpg`
- `images/2548_DcQw_tAmtY0_01.jpg`, `images/2548_DcQw_tAmtY0_02.jpg`
- `images/2554_DcQJjwRGoam_01.jpg`, `images/2554_DcQJjwRGoam_02.jpg`
- `images/2629_DcgO61yGnce_01.jpg`, `images/2629_DcgO61yGnce_02.jpg`
- `images/2703_DcqDNQgGtIw_01.jpg`, `images/2703_DcqDNQgGtIw_02.jpg`
- `images/2744_Dcx0mrdmn5__01.jpg`, `images/2744_Dcx0mrdmn5__02.jpg`

매니페스트에 기록된 각 파일의 전체 SHA-256을 그대로 소유 근거로 사용했으며, 빠른 대조용 앞 12자 예시는 `1712/01=67fdee746167`, `1903/01=6703a655a627`, `2103/01=a3ea483a7da3`, `2554/01=f4914b308036`, `2703/01=1da495787f2f`, `2744/01=df061fa40d0c`이다.

### 핵심 명령

```bash
# 코퍼스 크기와 비어 있지 않은 prompt 수
jq '[.[] | select(.prompt and (.prompt_missing | not))] | length' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

# prompt 레코드를 모두 읽은 뒤 garment/material/construction/surface/drape/silhouette
# 정규식과 70/80자 근접창으로 겹치는 match count를 산출했다.
python - <<'PY'
import json, re
rows = [r for r in json.load(open(
    'generated/reactorprompt-export-20260902-incremental/manifest.json'))
    if r.get('prompt') and not r.get('prompt_missing')]
assert len(rows) == 924
# 각 분류의 정규식 span을 만들고 두 span 사이 문자가 70 또는 80 이하인지 검사.
PY

# 기준 리비전 authored source의 직접 의복/소재 하드 프로필 수
git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:\
skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json \
  | jq '[.profiles[] | select(.category | test(
      "^garment_|garment_construction|material_optics|culture_bounded_garment_system|institutional_garment|wearable_protective_system|adult_fantasy_garment_mixin"
    ))] | length'

# 기준 리비전 후보 슬롯 규모
git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:\
skills/photo-prompt-image-generator/assets/photo_prompt_tags.json \
  | jq '.slots | {
      wardrobe_style:(.wardrobe_style|length),
      garment_detail:(.garment_detail|length),
      surface_material:(.surface_material|length),
      texture:(.texture|length)
    }'
```

### 외부 1차/권위 자료

- [ASTM D1388-23 — Standard Test Method for Stiffness of Fabrics](https://store.astm.org/standards/d1388): 직물의 굽힘 길이와 굽힘 강성을 별도 측정한다. 여기서는 `flowy/stiff` 라벨 대신 굽힘 반경, 주름 밀도, 지지점과 중력 반응을 분리해야 한다는 근거로만 사용했다. 사진이 ASTM 물성을 측정했다고 주장하지 않는다.
- [NIST — Measuring Up: Light Reflection and Transmission](https://www.nist.gov/news-events/news/2022/01/measuring-light-reflection-and-transmission): 표면 반사와 재료 투과가 외관 인지에 관여하고 조명/측정 조건에 영향을 받는다는 권위 자료다. 소재 표면과 조명 소유를 분리하는 근거로 사용했다.
- [The Metropolitan Museum of Art — The Care and Handling of Art Objects, Flat Textiles](https://resources.metmuseum.org/resources/metpublications/pdf/The_Care_and_Handling_of_Art_Objects_Practices_in_The_Metropolitan_Museum_of_Art_2019.pdf): warp/weft 기반 직조 구조와 lace/felt 같은 비직조 예외를 설명한다. `woven`, `openwork`, `pile`을 한 `texture` 라벨로 합치지 않고 native 구조 증거로 나누는 근거로 사용했다.

외부 자료는 안정된 물성·광학·직물 구조 용어의 경계를 정하는 데만 사용했다. 특정 문화 의복, 실제 섬유 조성, 사람의 신분·정체성 또는 이 코퍼스의 품질을 외부 자료로 추정하지 않았다.
