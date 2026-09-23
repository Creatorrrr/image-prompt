# 실사 이미지 요소의 시각 의미·후보팩 보강 연구

- 조사일: 2026-09-23
- 참조 대화: [실사 이미지 요소 조사](chatgpt-conversation://6ab33f23-a8bc-83e8-abb9-8e41f2af7191)의 1~40절
- 대상: `skills/photo-prompt-image-generator`
- 상태: **이 문서는 구현 전 연구 스냅샷**. 후속 운영 반영과 세 이미지 실험은 [구현·검증 보고서](implementation-report.md)에 기록한다.
- 동반 파일: `coverage-map.json`(40절), `sources.json`(26개 1차·공식 자료), `visual-proposals.json`(21개 제안), `candidate-bundles.json`(14개 상황별 묶음), `evaluation-cases.jsonl`(검증 명세)

## 결론

실사감을 높인다고 알려진 단어를 추가하는 것만으로는 프롬프트의 의미나 결과 품질을 보증할 수 없다. 이번 연구는 **촬영 위치 → 광학/노출 → 광원과 재질 → 행동/접촉 → 처리/출력물**의 관찰 가능한 관계를 후보 데이터의 단위로 삼는다. `photorealistic`, `8K`, `RAW DSLR`, 기종명, 특정 필름명은 이 관계를 대신할 수 없다. 다만 이 설계가 실제 생성 모델에서 더 좋은 이미지를 만든다는 인과 효과는 아직 시험하지 않았다.

참조 대화가 인용한 [Qwen의 공식 prompt rewriter](https://huggingface.co/Qwen/Qwen-Image-2.1-PE-T2I/blob/main/system_prompt.txt)는 프레임 위치, 표면 재질, 빛, 그림자, 반사를 명시하도록 설계되어 있다. [Midjourney 공식 가이드](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics)도 피사체·매체·환경·조명·색·구도를 명료하게 쓰고 긴 나열을 경계한다. 이것은 **제작사 권고**이지, 개별 키워드의 보편적 효과 순위나 이 저장소의 성능 증거는 아니다. [GenEval](https://arxiv.org/abs/2310.11513)과 [T2I-CompBench](https://arxiv.org/abs/2307.06350)가 별도 축으로 다루는 객체 수·속성 결합·공간 관계는 실제 픽셀에서 따로 검증해야 한다.

## 현재 저장소 기준선과 중복 방지

이번 조사 시점의 운영 자산에는 visual obligation 프로필 **333개**와 후보 슬롯 **111개**가 있다. 이 중 `medium` 57개, `genre` 56개, `capture_context` 76개, `camera_type` 25개, `lens` 33개, `focus` 20개, `motion` 44개, `grain_profile` 7개, `film_emulation` 18개, `surface_material` 141개다. 이는 현재 소스의 개수이며 후보팩 노출·사용 빈도·생성 성공률이 아니다.

이미 있는 hard profile을 재사용해야 한다. 원근에는 `wide_angle_near_field_perspective`, `telephoto_distance_compression_relation`; 초점에는 `shallow_depth_focus_falloff_relation`; 움직임에는 `panning_subject_tracking_motion_relation`, `rear_curtain_flash_motion_trace`, `rolling_shutter_readout_skew`; 빛에는 `mixed_illuminant_white_balance_relation`, `highlight_rolloff_tone_response`, `motivated_practical_mixed_interior_relation`; 필름/광학에는 `film_halation_highlight_edge_relation`, `diffusion_filter_highlight_halation`; 깊이와 반사에는 `three_plane_depth_chain`, `wet_surface_light_reflection_owner_relation`이 존재한다. 시대 데이터의 연구 제안과 현재 구현 상태는 [사진 시대 연구](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/photo-era-visual-semantics-20260905/report-source.md)에서, 사용 흔적·배경 관계의 연구/구현 범위는 [현실적 배경 연구](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/realistic-background-20260912/report.md)와 [후속 구현 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/realistic-background-implementation-20260912/report.md)에서 별도로 확인한다.

`coverage-map.json`은 참조 대화의 40절 모두를 `reuse`, `extend`, `advisory`, `metadata_only`, `governance`, `method_only` 등으로 매핑한다. 같은 의미를 다른 별칭으로 중복 등록하는 일보다 **서로 가까운 시각 결과의 구별**을 우선한다.

## 핵심 구분과 보정

| 참조 키워드군 | 관찰 가능한 증거와 owner | 혼동하면 안 되는 것 | 데이터 처리 |
|---|---|---|---|
| 24/35/85mm, full-frame | 화각·카메라 거리·피사체/배경 상대 크기 | mm/센서 이름이 원근을 직접 인증 | 거리 관계 프로필 재사용 + 장비는 후보/메타 |
| f/1.4, bokeh, missed focus | 초점 대상, 전·후경 이행, 경계 연속성 | 전역 블러, 인물 모드 마스크 오류 | 기존 초점 프로필 + 행동 대상 가독성 |
| 셔터, handheld, panning | 선명한 핵심과 움직임 방향별 흐림 | 전체 흔들림, 롤링 셔터 기울기 | 원인·움직이는 owner 분리 |
| natural/practical/mixed light | 실제 광원, 수광면, 그림자 방향과 색 | 색보정만으로 광원 존재 주장 | 기존 조명 프로필 재사용 |
| clipped highlights, HDR | 어디에 노출을 맞췄는지, 어떤 영역에서 정보 손실이 생겼는지 | 흰색 전체 클립, 평탄한 전역 HDR | 새 `pr_scene_owned_exposure_tradeoff` |
| pores, asymmetry, flyaways | 보이는 크기·광원·두피 부착·움직임의 원인 | 모든 인물에게 잡티·비대칭·헝클어짐 강제 | 조건부 인물 후보 |
| fabric wrinkles, wear | 봉제선·관절·손·접촉면에 귀속된 재질 반응 | 전역 그런지·의복과 무관한 주름 | 새 직물/표면 관계 |
| contact shadow, reflection | 같은 물체·지지면·광원·반사면의 일치 | 그림자 스티커, 없는 물체의 반사 | 새 접점 관계 + 기존 반사 프로필 |
| grain, sensor noise, JPEG | 이미지층 입자, 암부 휘도/색 노이즈, 재압축 경계 | 서로의 원인을 바꿔 부르기 | 매체별 optional 후보 |
| 35mm, instant, CCD, CCTV, DV | 사진/인화물/영상 프레임의 촬영·출력·유통 단서 | 특정 연도·기종·진품 인증 | 상황 묶음 + provenance 경계 |
| documentary, photojournalistic | 관찰 거리·동작·현장 맥락 | 실제 사건·비연출·보도 진정성 주장 | 시각 스타일과 검증 메타 분리 |

### 원근과 심도

카메라가 고정된 상태에서 초점거리만 바꾸면 화각과 프레이밍이 바뀐다. 같은 인물 크기를 유지하려고 카메라를 움직일 때 피사체와 배경의 상대 크기가 바뀐다. 그래서 `35mm lens` 한 단어 대신 카메라 위치, 인물의 크기, 가까운 물체와 먼 구조물의 크기 관계를 함께 기록한다. [Nikon 초점거리 설명](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/understanding-focal-length)과 [Adobe 조리개·심도 안내](https://www.adobe.com/creativecloud/photography/hub/guides/relationship-aperture-and-focal-length.html)는 화각과 심도 효과를 뒷받침한다. 다만 동일한 수치가 모든 센서·거리·출력에서 동일한 시각 결과를 뜻하지 않는다.

`eyes in sharp focus`도 모든 이미지의 기본 의무로 두지 않는다. [Nikon의 인물 안내](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits)는 전형적인 인물 사진에서 눈 초점을 권하지만, 손의 작업, 뒷모습, 실루엣, 반사 피사체 등에는 다른 초점 대상이 더 중요하다. 새 제안 `pr_focus_plane_subject_falloff`는 **요청 의미를 증명하는 물체와 그 앞뒤 깊이**를 지정한다.

### 빛·노출·색

[ARRI 조명 핸드북](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)은 hard/soft를 광원 세기보다 그림자 경계 및 광원의 상대 크기로 설명한다. 따라서 작은 창가 인물에게 `warm practical light`를 적을 경우, 화면 안의 램프와 밝아진 얼굴·탁자 면의 방향, 창에서 들어온 차가운 빛, 그 사이의 그림자가 함께 있어야 한다. 색온도 숫자만 맞고 물체별 색 반응이 다르면 의미가 무너진다.

`slightly blown highlights`를 일반적 실사 규칙으로 만들지 않는다. 새 노출 관계는 **노출 owner**를 정하고, 밝은 창의 일부에서는 클립을 허용하되 필요한 주피사체와 공간 경계는 보존한다. [Apple의 계산사진 설명](https://www.apple.com/uk/newsroom/2020/10/apple-announces-iphone-12-and-iphone-12-mini-a-new-era-for-iphone-with-5g/)은 스마트폰의 지역별 톤·질감 처리를 보여 준다. 그러므로 현대 스마트폰 사진을 항상 저다이내믹레인지·노이즈·클리핑으로 묘사하는 것도 오류다.

렌즈 결함 역시 원인별로 나눈다. [Tiffen의 확산 필터 안내](https://tiffen.com/pages/diffusion-guide)는 광원 주변의 광학 확산을, [Sony의 글로벌 셔터 설명](https://www.sony.com/en/SonyInfo/technology/stories/entries/9M3_global-shutter/)은 순차 판독 센서에서 빠른 움직임이 기하학적 스큐를 만들 수 있음을 뒷받침한다. 확산 필터의 bloom, 필름 halation, 센서의 rolling-shutter skew, 단순 카메라 기울기를 하나의 `imperfection`으로 섞지 않는다.

### 피부·머리·직물·표면

`visible pores`는 얼굴이 충분히 크게 보이고 조명이 실제로 피부 세부를 드러내는 경우에만 관찰 가능하다. 스냅의 작은 얼굴에 미세 모공을 필수 픽셀 게이트로 요구하면 검증할 수 없는 계약이 된다. [Adobe Lightroom의 Texture·Clarity 제어](https://helpx.adobe.com/lightroom/desktop/edit-photos/edit-photos.html)는 질감과 가장자리 대비가 서로 다른 처리 축임을 보여 준다. 이는 거친 노이즈를 피부 세부로 인정하지 않는 근거다. 주근깨, 비대칭, 흉터, 결점은 개인 외형이나 사용자 요청을 임의로 바꾸는 기본 옵션이 아니다.

직물의 주름은 재질 이름만으로 끝나지 않는다. 굽은 팔꿈치에서 소매 봉제선으로 이어지는 접힘처럼 **힘의 시작점과 진행 방향**을 제안한다. 사용 흔적도 유리잔의 손이 닿는 가장자리, 자주 여닫는 손잡이, 물체가 놓인 바닥에 귀속한다. [Disney의 측정 기반 재질 반응 연구](https://disneyanimation.com/publications/physically-based-shading-at-disney/)는 거칠기와 반사 응답을 구분하는 물리적 배경을 제공하지만, 특정 프롬프트가 실제 물질을 재현한다는 증거는 아니다.

### 필름·디지털·영상의 서로 다른 결함

[Adobe의 RAW 설명](https://helpx.adobe.com/camera-raw/desktop/get-started/overview-and-setup/introduction-camera-raw.html)에서 RAW는 센서 데이터와 처리 가능한 메타데이터다. `RAW DSLR`만으로 특정 톤이나 무보정 이력을 주장하면 안 된다. [Adobe의 노이즈 설명](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/retouch-photos.html)은 디지털 휘도 노이즈와 색 노이즈를 구별한다. 필름 입자와 스캔 먼지는 다시 별개의 이미지층·출력층이다. [Kodak 기술 자료](https://www.kodak.com/content/products-brochures/Film/kodak-essential-reference-guide-for-filmmakers.pdf)는 할레이션 방지층처럼 필름 구조 차이를 설명한다. 필름명은 `-like` 룩 후보로만 둔다.

즉석사진은 흰 테두리 필터보다 **이미지면을 가진 카드라는 물체**가 먼저다. [Polaroid의 공정 설명](https://support.polaroid.com/hc/en-us/articles/115012396647-What-happens-when-I-insert-a-Polaroid-film-pack-into-my-camera)은 카드·약제·현상의 관계를 보여 준다. [Adobe의 JPEG 자료](https://helpx.adobe.com/sg/photoshop-elements/using/jpeg-artifacts-removal-photoshop-elements.html)는 재압축 손상이 글자·직선·고대비 경계에 두드러질 수 있음을 설명한다. CCTV와 캠코더는 모두 낮은 화질을 가질 수 있지만, CCTV에는 고정 관찰 위치와 감시 구역의 구조가 있고 홈비디오에는 시간 속 행동과 프레임 컨테이너가 있다. [Axis 영상 품질 가이드](https://help.axis.com/en-us/troubleshooting-image-quality)는 화질 제한이 목적과 촬영 조건에 달림을, [Sony의 60i/60p 설명](https://www.sony.com/electronics/support/camcorders-and-video-cameras-tape-camcorders/ccd-trv98/articles/00017421)은 비디오 주사 방식의 차이를 설명한다. 인터레이스 흔적은 모든 캠코더 프레임의 필수 요소가 아니다.

### 실제 기록의 진정성

`documentary`나 `photojournalistic`은 스타일 후보일 수 있다. 그러나 실제 보도·비연출·현장 증거는 생성 이미지의 픽셀에서 인증할 수 없다. [AP 보도 원칙](https://www.ap.org/about/news-values-and-principles/telling-the-story/)은 사건 연출과 사진 조작을 제한하고, [World Press Photo 검증 절차](https://www.worldpressphoto.org/contest/verification-process)는 원본 파일, 전후 프레임, 캡션 및 외부 사실 확인을 요구한다. 따라서 `pr_documentary_authenticity_boundary`는 픽셀 프로필이 아니라 **설명·메타데이터 경계**다. 합성 결과는 명시적으로 가상 또는 다큐멘터리 스타일이라고 표현한다.

### ‘통제된 불완전성’의 한계

참조 대화의 “2~4개 정도”와 별점 순위는 검증된 효과량이 아니다. `pr_conditional_imperfection_budget`는 숫자 할당량 대신 **선택된 매체와 장면에서 원인이 있는 결함 하나가 필요한지**를 판단하도록 설계했다. 깨끗한 광고·제품 사진, 과학 기록, 맑고 건조한 야외 사진은 결함 없이도 사진적일 수 있다. [Stability의 SDXL 가이드](https://stability.ai/sdxl-aws-documentation)는 `high quality` 같은 과잉 수식어의 필요성이 낮다고 설명하지만, 모든 모델에서 `8K`나 `masterpiece`의 효과가 항상 0이라는 주장은 아니다.

## 구조화 데이터 설계

21개 제안은 `visual-proposals.json`에 **owner, 필수 시각 성분, 인접 오탐, 짧은 영어 후보 표현, 기존 프로필, 권장 슬롯, 출처**를 보존한다. 이 중 디지털 노이즈, JPEG 재압축, 필름 입자 3개는 매체에 맞는 optional 후보이며, `pr_documentary_authenticity_boundary`와 `pr_conditional_imperfection_budget` 2개는 provenance/후보 선택 규칙이다. 이 5개를 새 픽셀 hard profile로 승격하지 않는다. 어떤 제안도 현재 레지스트리에 등록하지 않았다.

| 우선 | 제안 ID | 새로 필요한 관찰 경계 | 우선 재사용할 기존 계약 |
|---|---|---|---|
| P0 | `pr_environmental_portrait_subject_place`, `pr_observed_action_trace` | 인물·장소·행동 대상과 결과 | `three_plane_depth_chain`, `peak_action_event_phase` |
| P0 | `pr_camera_distance_subject_scale`, `pr_focus_plane_subject_falloff` | shot size와 공간비, 초점 대상/깊이 | `wide_angle_near_field_perspective`, `shallow_depth_focus_falloff_relation` |
| P0 | `pr_scene_owned_exposure_tradeoff` | 창/실내의 노출 소유와 손실 범위 | `highlight_rolloff_tone_response` |
| P0 | `pr_skin_detail_lighting_scale`, `pr_fabric_tension_fold_attachment`, `pr_surface_wear_contact_owner` | 피부의 판정 크기, 주름의 장력, 마모의 접촉 위치 | `sheer_complexion_texture_preservation`, `surface_material` 후보 |
| P0 | `pr_object_contact_shadow_support`, `pr_reflection_scene_binding` | 중력·지지·광원·반사 대상의 결합 | `wet_surface_light_reflection_owner_relation` |
| P1 | `pr_hair_strand_owner_and_cause`, `pr_casual_crop_subject_legibility` | 두피 부착·바람 원인, 잘림 뒤에도 의미 보존 | `asymmetric_counterbalance_relation` |
| P1 | `pr_shadows_local_digital_noise`, `pr_jpeg_edge_blocking`, `pr_film_grain_print_scan_scope` | 센서·압축·필름·출력층 분리 | `early_2000s_compact_digicam_social_repost`, `physical_print_scan_material_context` |
| P1 | `pr_instant_print_material_object`, `pr_fixed_surveillance_observation`, `pr_camcorder_still_temporal_container`, `pr_atmospheric_distance_contrast` | 인화물 물체, 고정 감시, 영상 시간, 먼 공간 대비 | `physical_print_scan_material_context`, `three_plane_depth_chain` |

14개 묶음은 `candidate-bundles.json`에 있다. 깨끗한 스튜디오/패션/제품과 저조도 스마트폰/거리 스냅/디카 재게시/필름 인화/CCTV/캠코더/풍경을 별도 조건으로 두어 한 장에 모든 결함을 누적하지 않게 한다. 묶음의 슬롯 seed ID는 현재 사전의 실제 ID로 대조하지만 **후보팩에 노출됐다는 뜻은 아니다**. 후보는 우선순위 없는 선택지다. 초기 요청은 독립적으로 해석하고 사용자 잠금 차원을 동결한 뒤, 열린 차원에서만 후보를 선택한다.

## 구현·검증 순서

1. **소스/경계 정리:** 기존 프로필을 확장 가능한 경우 신규 hard profile로 복제하지 않는다. 후보 표현과 장비/시대 메타데이터를 분리하고 소스 ID를 유지한다. 새 hard profile이 정말 필요하면 연구 제안의 3~4개 관찰 조건을 기존 계약 형식에 맞는 다섯 개 구성요소 그룹·프롬프트 증거·render gate로 구체화한다.
2. **좁은 라우팅:** `photorealistic`, `realistic`, `35mm`, `85mm`, `RAW DSLR`, `film look`, `HDR`, `candid`, `documentary`, `8K` 단독 입력은 신규 hard 의무를 만들지 않는다. 사용자가 관계를 명시하거나 다섯 성분이 충분히 있을 때만 exact/context activation을 검토한다.
3. **검색·노출:** 제안이 실제 운영 자산에 들어갈 때 소스 해시와 시각 프로필 인덱스를 재생성하고, 검색 결과뿐 아니라 공개 후보팩의 candidate ID와 선택 가능 범위를 확인한다. BM25F/embedding 유사도만으로 hard 의무를 승격하지 않는다.
4. **프롬프트 감사:** 한 묶음의 선택 항목이 사용자 잠금 차원을 바꾸지 않는지, 반사·그림자·재질의 owner가 같은지, 원인/결과가 영어 문장에 실제로 쓰였는지 검사한다.
5. **픽셀 평가:** 축소 크기에서 shot size·행동·광원/공간을, 원본 크기에서 피부/직물·접점·반사·노이즈의 owner를 확인한다. 필수 성분은 같은 최종 이미지에서 모두 보여야 한다. `partial_is_fail`; 이미지가 없으면 `UNSCORED`. 사용자 선호와 기술 판정을 따로 보존한다.
6. **효과 비교:** 깨끗한 스튜디오, 낮 카페, 저조도 폰, 거리 스냅, 작업장 환경 인물, 디카 재게시, 물체 사진, 원경 풍경의 8장면군에서 A=현재 데이터, B=일반 실사 품질어, C=이번 관계 데이터의 3조건×3반복을 제안한다(총 72장 파일럿). 모델·버전·비율·참조·잠금 의도를 고정하고 가능한 경우 반복 시드를 짝짓는다. B/C의 길이·추가 객체 수를 기록하여 정보량 차이를 따로 본다. 이 숫자는 검정력을 보증하지 않는다.

`evaluation-cases.jsonl`의 positive/near-miss는 **앞으로 적용할 평가 명세**이지 실제 이미지 점수가 아니다. 이 단계에서 수행한 것은 JSON 구조, 참조 ID, 현재 슬롯 ID 대조, 40절 범위 및 신규 제안의 중복 ID 검증뿐이다. 운영 데이터, 검색 인덱스, 후보팩 노출, 이미지 렌더, 블라인드 픽셀 리뷰, 사용자 수락은 수행하지 않았다.
