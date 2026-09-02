# 촬영 요소 시각 의미·후보팩 연구 기록

## 목적

이 기록은 카메라·렌즈·초점·셔터·조명·광학 필터·화이트밸런스·톤 응답 키워드를 장비 이름이나 분위기 라벨이 아니라, 이미지에서 직접 확인 가능한 관계로 변환한다. 런타임의 단일 소스 오브 트루스는 `assets/photo_prompt_visual_obligations.json`이며 이 문서는 근거와 적용 경계만 보존한다.

첨부 인물 이미지는 보이는 성인 외형의 유일한 참조로만 사용한다. 신원, 동일인 여부, 인종·국적, 성격, 직업, 건강, 매력도 같은 비시각 속성을 추론하지 않는다. 테스트에서는 얼굴 구조, 눈의 형태와 간격, 얼굴 길이, 하관·턱 폭, 성인 연령감을 보존하고 장면·동작·의상·조명만 바꾼다.

## 1. 근거에서 추출한 관찰 단위

| 축 | 근거가 지지하는 관찰 | 런타임 변환 |
|---|---|---|
| 원근 | 초점거리 자체보다 카메라 거리, 화각, 전경·원경 상대 크기와 수렴선이 공간 인상을 만든다. | 광각 근접 원근과 망원 거리 압축을 서로 다른 관계형 프로필로 분리한다. |
| 심도 | 선명면 앞뒤의 흐림은 장면 깊이에 따라 연속적으로 변하며 전경·배경 보케가 다를 수 있다. | 얕은 심도는 ‘배경 흐림’이 아니라 선명면·전경 이행·후경 이행·경계 연속성으로 판정한다. |
| 다중 초점 | 고정된 프레임의 서로 다른 초점 이미지를 정렬·혼합하면 확장 심도 합성이 된다. | 포커스 스택은 전·중·후경 동시 선명도와 정렬·블렌드 경계를 모두 요구한다. |
| 분할 초점 | 한 프레임 안에서 매우 가까운 면과 먼 면이 선명하고 중간 심도는 더 부드러울 수 있다. | 스플릿 디옵터를 딥 포커스·포커스 스택·분할 화면과 구별한다. |
| 패닝 | 추적된 핵심은 상대적으로 선명하고 환경은 이동 방향으로 흐르며, 전부 흐리면 실패일 수 있다. | 피사체 핵심, 평행 배경 스트리크, 보조 움직임, 단일 이동 벡터를 hard gate로 둔다. |
| 후막 동조 | 느린 주변광 노출 뒤 노출 종료 시점의 플래시가 최종 위치를 고정하므로 궤적이 종점으로 들어간다. | 종점 앞 연속 궤적·선명 종점·주변광 맥락·도착 방향을 동시에 요구한다. |
| 롤링 셔터 | 행별 판독 시간 차가 빠른 움직임에서 기하학적 스큐를 만들며 전역 모션 블러와 다르다. | 반복 수직선의 일관된 기울기, 이동체 전단, 남은 국소 선명도를 요구한다. |
| 인물 조명 | 렘브란트 조명은 그림자 쪽 눈 아래의 제한된 삼각광으로 정의할 수 있다. | 높은 비축 키, 연결된 코·볼 그림자, 삼각광, 읽히는 그림자 쪽 눈을 요구한다. |
| 상하 조명 | 클램셸은 상부 키와 약한 하부 필의 수직 관계로 눈·턱 그림자를 연다. | 두 광원 관계, 위·아래 캐치라이트, 완전히 사라지지 않은 입체 그림자를 요구한다. |
| 감산 조명 | 네거티브 필은 어두운 면이 반사광을 흡수해 특정 쪽 그림자만 깊게 한다. | 가까운 흡광면, 반사 필 감소, 국소 그림자 심화, 안정된 키 노출을 요구한다. |
| 광학 확산 | 디퓨전 필터는 실광원·정반사 주변에 국소 헤일레이션을 만들면서 겉보기 초점 디테일을 유지할 수 있다. | 광원 고정 헤일로, 인접 대비 확산, 초점면 디테일을 요구하고 안개·전역 블러·필름 헤일레이션과 분리한다. |
| 혼합 광원 | 서로 다른 색온도의 실제 광원은 방향·감쇠·가림에 맞는 공간별 색 반응을 만든다. | 두 식별 광원, 공간 분리, 중성 기준, 재질 정체성 보존을 요구한다. |
| 톤 응답 | 하이라이트 보존은 단순 저대비가 아니라 흰색에 접근하는 점진적 숄더와 주변 질감 보존으로 보인다. | 작은 클립 중심, 여러 밝기 단계, 하이라이트 질감·색·중간톤 생존을 요구한다. |

## 2. 1차 소스

- Nikon, “10 Tips for Better Camera Panning”: 추적 피사체의 일부 선명도, 방향성 흐림, 느린 셔터, 후막 동조 종점의 관계. https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/10-tips-for-better-camera-panning
- Nikon, “Flash Points: The Control of Light”: 후막 동조에서는 주변광 이동이 먼저 기록되고 플래시가 노출 끝에서 피사체를 고정한다. https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/flash-points-the-control-of-light
- Nikon Photography Glossary, “Rembrandt Lighting”: 그림자 쪽 눈 아래의 다이아몬드형 조명 영역과 측면 키·약한 반대쪽 광원 관계. https://www.nikonusa.com/learn-and-explore/photography-glossary/index.page
- Sony, “Focal Length”: 짧은 초점거리의 넓은 화각과 긴 초점거리에서 먼 대상이 크게 보이는 관계. https://www.sony.com/electronics/support/articles/00267921
- Sony Group, “Alpha 9 III Global Shutter”: 롤링 셔터 판독이 빠른 피사체에서 왜곡을 만들고 글로벌 셔터가 이를 제거하는 경계. https://www.sony.com/en/SonyInfo/technology/stories/entries/9M3_global-shutter/
- Adobe Photoshop, “Create composite images with extended depth of field”: 서로 다른 초점 지점의 정렬 이미지들을 `Stack Images`로 혼합하는 확장 심도 합성. https://helpx.adobe.com/photoshop/desktop/create-masks/blend-images/create-a-composite-with-extended-depth-of-field.html
- ZEISS, “Depth of Field and Bokeh”: 전경·배경 디포커스의 비대칭 가능성, 구면수차와 흐림 원형의 밝기 분포. https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-depth-of-field-and-bokeh.pdf
- ARRI, “Lighting Handbook”: 키·필·반사·광원 위치를 통한 조명 제어의 실무 경계. https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf
- Tiffen, “Diffusion Guide”: 실광원·정반사 주변의 국소 헤일레이션과 전체 겉보기 선명도 유지의 구분. https://tiffen.com/pages/diffusion-guide
- Canon, “Digital Cinema Cameras”: Log·HDR이 밝은 영역 정보와 자연스러운 톤 재현을 보존하는 목적. https://global.canon/en/technology/canon-tech/tech/cinema-camera/

## 3. 반영한 프로필

1. `wide_angle_near_field_perspective`
2. `telephoto_distance_compression_relation`
3. `shallow_depth_focus_falloff_relation`
4. `focus_stacked_extended_depth_composite`
5. `split_diopter_dual_focus_planes`
6. `panning_subject_tracking_motion_relation`
7. `rear_curtain_flash_motion_trace`
8. `rolling_shutter_readout_skew`
9. `rembrandt_face_light_pattern`
10. `clamshell_dual_source_portrait_light`
11. `negative_fill_shadow_deepening_relation`
12. `diffusion_filter_highlight_halation`
13. `mixed_illuminant_white_balance_relation`
14. `highlight_rolloff_tone_response`

각 프로필은 좁은 다국어 exact term, 다섯 개의 동시 성분 그룹, 인접 혼동 예시, 선택 가능한 비선호 순서 `concept_terms`, 다섯 개의 프롬프트 증거 필드, thumbnail/both/native 픽셀 게이트, 구체적 대체 실패를 가진다. exact term만 자동 hard obligation이 되고, BM25F·임베딩 유사도는 선택 전까지 optional candidate에 머문다.

## 4. 의도적으로 hard profile로 만들지 않은 항목

- 정확한 카메라·센서·렌즈 모델, 센서 크기, 초점거리 수치, 조리개 수치
- MTF 수치, 비트 심도, 코덱, Log/RAW/ACES 파이프라인 이름
- 특정 필름 스톡·필름 시뮬레이션·제조사 색과학 이름
- 촬영자, 실제 촬영 시점, 공개 이력, 희소성, 장비 소유권

이 값들은 보이는 결과를 제약하는 메타데이터나 선택 후보가 될 수 있지만 그 자체가 픽셀 성공을 증명하지 않는다. exact 장비 라벨이 필요한 경우에도 요청 잠금으로 보존하고, 시각 평가는 실제 관계형 게이트로 수행한다.

## 5. 평가 규칙

- 한 프로필의 모든 hard gate는 같은 최종 이미지에서 공존해야 한다.
- `partial`, 누락, 판단 불가, 근거 없는 판정은 실패다.
- 패키지·라우팅·프롬프트 감사 PASS는 픽셀 PASS가 아니다.
- 이미지가 생성되지 않으면 품질 0점이 아니라 `UNSCORED`다.
- 에이전트 픽셀 판정과 요청 사용자의 선호·수락은 별도 증거다.
- 재시도는 실패한 관계만 수리할 때에만 허용되며, 이번 3-arm 독립 시험은 팔마다 입력을 동결하고 1회 생성만 기록한다.
