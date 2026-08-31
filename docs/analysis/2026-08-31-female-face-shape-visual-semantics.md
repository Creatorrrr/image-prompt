# 여성 얼굴형 표현의 시각 의미 데이터화와 후보팩 설계

작성일: 2026-08-31  
적용 대상: `photo-prompt-image-generator` 시각 의무 레지스트리와 후보팩  
판정 범위: 얼굴형을 만드는 관찰 가능한 윤곽·폭·세로·깊이 관계. 신원, 성격, 건강, 민족성, 매력도 판정은 범위 밖이다.

## 적용 결과

- 얼굴형 합성 관계 11개를 요청 시에만 활성화되는 `face_shape_relation` 후보 슬롯으로 추가했다.
- 같은 11개 관계를 정확한 문맥 표현에만 반응하는 하드 시각 프로필로 추가했다.
- 이마·관자·광대·볼·하악·턱끝·얼굴 세로 구간·측면 돌출을 분리하는 지역 원자 16개를 `anatomical_connection`에 추가했다.
- 얼굴 외곽을 실제로 관찰할 수 있게 하는 프레이밍 원자 6개를 `subject_framing`에 추가했다.
- 일반 프리셋에는 `face_shape_relation`을 자동 선택 항목으로 넣지 않았다. 정확한 요청 또는 후속 검색·선택이 있을 때만 후보가 된다.

## 핵심 의미 모델

얼굴형 라벨은 최종 증거가 아니라 다음 다섯 관계를 묶는 진입점이다.

1. 전체 외곽: 헤어라인, 양쪽 관자, 볼 외곽, 턱 모서리, 턱끝이 한 프레임에서 보인다.
2. 세로 관계: 얼굴 길이가 폭과 비교해 짧은지, 비슷한지, 적당히 긴지, 뚜렷이 긴지 선언한다.
3. 가로 폭 소유권: 이마·관자, 광대, 하악각 중 어디가 가장 넓거나 서로 비슷한지 선언한다.
4. 하안면 종결: 턱선이 각지거나 둥글거나 좁아지는 방식과 턱끝 폭·형태를 한 연속 윤곽으로 선언한다.
5. 혼동 통제: 머리카락, 표정, 메이크업, 그림자, 카메라 거리·원근, 크롭이 해부학적 관계를 대신하지 못하게 한다.

모든 하드 프로필은 이 다섯 그룹, 다섯 프롬프트 증거 필드, 다섯 픽셀 게이트를 갖는다. 특정 수치 비율은 넣지 않았다.

## 합성 프로필과 구분 경계

| 프로필 | 가시적 중심 관계 | 반드시 구분할 대상 |
|---|---|---|
| `oval_face_contour_relation` | 적당히 긴 세로, 광대 부근이 약간 가장 넓고 둥근 턱으로 완만히 좁아짐 | 둥근형, 장방형, 헤어가 만든 타원 |
| `round_compact_face_relation` | 길이와 폭이 비슷하고 볼 폭에서 짧고 둥근 턱선으로 이어짐 | 볼살 하나, 미소 압축, 근접 광각 |
| `oblong_elongated_face_relation` | 세로가 뚜렷이 길고 이마·광대·하악 폭이 비교적 평행하며 하부가 부드럽게 끝남 | 슬픈 표정의 관용구, 직사각형의 넓고 각진 턱 |
| `square_face_contour_relation` | 길이와 폭이 비슷하고 이마·광대·하악 폭 및 넓은 턱 모서리가 비교적 유지됨 | 사각 프레임, 강한 그림자, 둥근 볼 |
| `rectangular_face_contour_relation` | 사각형의 평행 폭과 넓은 각진 턱을 유지하면서 세로가 더 김 | 장방형의 부드러운 하부, 세로 크롭 |
| `triangle_lower_face_dominant_relation` | 이마·관자보다 하악 폭이 넓어 아래쪽으로 외곽이 벌어짐 | 배 과일·체형, 넓은 턱끝 하나 |
| `diamond_zygomatic_dominant_relation` | 광대 가로 폭이 가장 넓고 이마와 턱 양방향으로 좁아짐 | 광대 전방 돌출 하나, 하이라이트, 보석 |
| `upper_face_to_chin_taper_relation` | 이마·상부 관자가 하악보다 넓고 좁은 턱으로 계속 좁아짐 | 하트 아이콘, 가르마·헤어라인 하나, 다이아몬드형 |
| `v_tapered_lower_face_relation` | 양쪽 광대 아래에서 하악 폭이 줄고 좁은 턱끝까지 연속 수렴 | 브이넥·사타구니 V-line, 뾰족한 턱 하나 |
| `u_rounded_lower_face_relation` | 광대 아래에서도 하악 폭을 유지하다 넓고 둥근 호로 턱끝에 연결 | U 그래픽, 넓은 턱끝 하나, 전체 둥근 얼굴 |
| `cjk_seed_face_relation` | 타원형 상·중안면과 그보다 강한 하안면 수렴, 작고 둥글거나 부드럽게 뾰족한 턱 | 완만한 계란형, 일반 V형, 수술·민족성·미적 가치 추론 |

`heart-shaped face`와 `inverted triangle face`는 상부 폭 우세와 턱 수렴이 겹치므로 하나의 관계 프로필로 묶고, 중앙 헤어라인 돌출은 선택적 단서로 남겼다. `V-line`, `U-line`, `瓜子脸`은 문맥과 문화권에서 의미가 달라질 수 있어 런타임에는 라벨을 보내지 않고 분해된 윤곽 문장만 사용한다. 한국어 `갸름하다`는 길고 가는 인상을 주는 넓은 합성 표현이므로 정확 하드 트리거로 승격하지 않고 후보 검색 의미에만 남겼다.

## 폭과 돌출을 분리한 이유

정면의 광대 가로 폭과 3/4·측면의 광대 전방 돌출은 서로 다른 축이다. 높은 광대, 강한 하이라이트, 움푹한 볼은 다이아몬드형의 광대 폭 우세를 대신할 수 없다. 같은 이유로 정면 턱끝 폭과 측면 턱끝 돌출도 별도 후보로 분리했다.

추가된 지역 원자는 다음을 포함한다.

- 이마 폭, 이마 세로 구간, 헤어라인 윤곽
- 관자 충만·오목 전환
- 광대 가로 폭, 광대 전방 돌출, 볼 연부조직 충만·오목
- 하악각 사이 폭, 하악각 정의, 턱끝 폭·형태, 턱 세로 구간, 턱끝 전후 돌출
- 헤어라인·눈썹·코밑·턱끝으로 정의한 얼굴 세로 구간
- 이마에서 턱끝까지의 측면 곡률

## 관찰·렌더 판정 경계

첨부 이미지는 성인 동아시아 여성의 정면 중립 표정에 가까운 헤드앤숄더 인물사진이다. 긴 검은 웨이브 헤어, 비교적 매끄러운 이마-관자-볼 전환, 광대 부근의 폭, 부드럽게 좁아지는 하악과 작고 둥근 턱끝을 외관 참고로 사용할 수 있다. 이 관찰은 신원 확인이나 생체 인식 주장이 아니다.

다섯 렌더 팔은 첨부 이미지를 `appearance_reference`로만 사용한다. 일반적으로 보이는 성인 외관과 헤어·눈·피부 인상은 참고하되, 각 실험의 목표 얼굴 윤곽 관계가 우선한다. 따라서 결과는 “같은 사람” 여부가 아니라 다음 픽셀 증거로 판정한다.

- 썸네일: 전체 얼굴 외곽과 목표 폭 계층이 첫눈에 읽히는가.
- 네이티브: 턱 모서리, 턱끝 종결, 관자·광대 경계가 머리카락·메이크업·그림자에 의해 가짜로 만들어지지 않았는가.
- 양쪽 규모: 목표 세로 관계와 하안면 흐름이 복잡한 장면·의상·소품 경쟁 속에서도 동시에 유지되는가.
- 실패는 `partial`로 승격하지 않는다. 다섯 게이트 중 하나라도 보이지 않거나 대체물로만 보이면 해당 팔은 실패다.
- 사용자 취향은 별도이며, 기술 게이트 통과가 사용자의 미적 선호를 증명하지 않는다.

## 회귀·혼동 테스트

정확 긍정은 한국어·영어·중국어·일본어의 얼굴 문맥 표현으로 한 프로필만 활성화되는지 확인한다. 하드 네거티브는 타원형 몸, 원형 거울, 사각 프레임, 직사각 문, 배 과일, 삼각 로고, 다이아몬드 목걸이, 하트 아이콘, 슬픔을 뜻하는 `long face`, 브이넥, 신체 V-line, U자 파이프, 광대 clown, 볼살·뾰족 턱·높은 광대 단일 단서를 포함한다.

다섯 독립 렌더 케이스는 서로 다른 의미 프로필과 장면 도메인, 시드를 갖는다. 각 팔은 다른 팔의 프롬프트·팩·이미지·리뷰를 보지 않고 하나의 복잡한 사진 콘셉트를 저작한다.

## 근거 자료

- [Elements of Morphology: Standard Terminology for the Head and Face](https://pmc.ncbi.nlm.nih.gov/articles/PMC2778021/)
- [Standardized Human Face Shape Analysis and Nomenclature](https://pubmed.ncbi.nlm.nih.gov/26662189/)
- [An Automatic Facial Landmarking for 3D Facial Data](https://pmc.ncbi.nlm.nih.gov/articles/PMC10292572/)
- [Genetic and Environmental Influences on Facial Shape](https://pmc.ncbi.nlm.nih.gov/articles/PMC5008732/)
- [Three-Dimensional Analysis of Facial Depth](https://pmc.ncbi.nlm.nih.gov/articles/PMC3815515/)
- [The Effect of Focal Length on Perception of Attractiveness](https://pmc.ncbi.nlm.nih.gov/articles/PMC4760932/)
- [Three-Dimensional Evaluation of Facial Morphology During Smile](https://pmc.ncbi.nlm.nih.gov/articles/PMC8479441/)
- [Three-Dimensional Facial Asymmetry in a Normal Population](https://pubmed.ncbi.nlm.nih.gov/24406564/)
- [Facial Shape Classification in Asian Women](https://pmc.ncbi.nlm.nih.gov/articles/PMC7605391/)
- [한국어기초사전: 갸름하다](https://krdict.korean.go.kr/eng/dicSearch/SearchView?ParaWordNo=21242)
- [Morphological Characteristics of the Melon-Seed Face](https://med.wanfangdata.com.cn/Paper/Detail?dbid=WF_QK&id=PeriodicalPaper_symrzxwkzz201005005)
- [Surgical Correction of the Lower Face: V-line and U-line Contours](https://pmc.ncbi.nlm.nih.gov/articles/PMC4236372/)
- [Anthropometric Study of Facial Morphology in Japanese Women](https://www.jstage.jst.go.jp/article/sccj1979/21/3/21_3_232/_pdf)
