# 추가 외형 관계 카드

연구 초안이며 현행 runtime schema가 아니다. 전체 사례 분해와 제안 관계를 구분해 채택한다.

## VD-001 · 닫힌 허리 베스트와 중앙의 안쪽 탑·넥타이

P0 · new_relation_trial · 키워드 K008, K009, K010, K011, K012, K015, K052, K053 · 기존 VEL-002, VEL-004, VEL-005, VEL-021, VEL-023

**소유자:** 같은 착용자의 재킷·탑·베스트·칼라·넥타이, 각각 독립 층

**선택된 뜻의 필수 구성:**

- The vest waist panel has a continuous closed front over the inner top.
- The side straps and panels ascend along the sides while the central upper-chest area retains the inner top and tie.
- The jacket opening reveals the selected inner layers without merging their edges.

**관계:**

- vest waist panel → lies_over → inner top waist region
- side straps → attach_to → vest side panels
- jacket opening → reveals → inner top and vest
- tie → lies_over → inner top central front

**사례 조건:** S02 문맥: 검정 베스트·흰색 U넥 골지 탑·검정 가죽 넥타이·파란 칼라·핀스트라이프 재킷을 사례 조건으로 보존한다. 닫힌 허리 앞판과 열린 상흉부 중앙은 서로 다른 영역이다.

**독립 선택/한계:** 일반형의 색·문양·버클 수·숨은 패드 치수는 요청에서 따로 정한다. busk, lacing, boning을 자동 추가하지 않는다.

**혼동 금지:**

- 닫힌 앞판을 중앙이 뚫린 하네스로 대체
- 탑을 제거하거나 베스트와 한 벌로 합침
- 닫힌 허리 조건을 가슴 중앙까지 완전 차폐로 확대

**현행 항목 검토:** slot:wardrobe_style:clt_ct023_v2, slot:wardrobe_style:y2kr_corset_top, slot:garment_detail:ccx_cc26_01

**자료:** A04, A06, R08

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-002 · 골지 높낮이·평면 줄무늬·봉제선의 별도 소유

P0 · extend_review · 키워드 K008, K009, K015, K181 · 기존 VEL-002, VEL-004, VEL-057

**소유자:** 골지 탑 표면, 재킷 인쇄/직조 무늬, 패널 봉제선

**선택된 뜻의 필수 구성:**

- Raised knit ribs and recessed channels repeat on the declared top surface.
- The selected stripe pattern follows the jacket panels without becoming raised knit ribs.
- Seams remain garment construction boundaries rather than skin marks.

**관계:**

- raised ribs → belong_to → top fabric
- pinstripes → follow_surface_of → jacket panels
- seam channels → divide → garment panels

**사례 조건:** K009의 U자 목선·흰 바탕·세로 골, S02 재킷의 핀스트라이프는 해당 사례 안에서 보존한다.

**독립 선택/한계:** 골 간격의 변화는 편직 종류·당김·관점에 따른 변형 후보다. 모든 골지를 일정 치수나 동일 신장률로 고정하지 않는다.

**혼동 금지:**

- 평면 스트라이프를 골지 돌출로 통과
- faille의 가로 직조 리브를 세로 니트로 자동 대체
- 주름·모공·피부 긁힘을 옷의 골로 통과

**현행 항목 검토:** y2kr_rib_tank, sw_rib, vg_faille_crossgrain_ribs_profile, slot:wardrobe_style:y2kr_rib_tank

**자료:** A01, A02, A03, A06

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-003 · 흘러내린 한쪽 끈과 반대쪽 지지의 비대칭

P0 · new_relation_trial · 키워드 K029, K030, K033 · 기존 VEL-011, VEL-012

**소유자:** 같은 드레스의 두 어깨끈과 앞뒤 몸판

**선택된 뜻의 필수 구성:**

- One strap has left its shoulder support and lies loosely on the outside of that upper arm.
- The opposite strap remains over its own shoulder.
- Both straps retain their declared garment attachment endpoints.

**관계:**

- fallen strap → rests_on → same-side upper arm
- retained strap → passes_over → opposite shoulder
- strap endpoints → attach_to → same garment panels

**사례 조건:** K030의 한쪽 상태와 다른 쪽 잔존 지지를 보존한다. 끈을 내린 행위자나 미래의 탈의는 주어지지 않았다.

**독립 선택/한계:** 끈의 좌우는 요청으로 결정한다. 끈 폭·소재·늘어진 곡선 크기는 독립 변수다.

**혼동 금지:**

- 원래 한 끈인 원숄더 디자인으로 대체
- 두 끈을 모두 어깨 아래로 내림
- 머리에 가린 끈을 흘러내린 끈으로 통과

**현행 항목 검토:** pfe_one_shoulder, slot:garment_detail:pfe_one_shoulder_candidate

**자료:** A04

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-004 · 레이스 구멍·의복 파임·원단 비침의 분리

P0 · extend_review · 키워드 K025, K027, K028, K031, K032, K034, K035, K037 · 기존 VEL-009, VEL-010, VEL-013, VEL-014

**소유자:** 레이스 띠, 바탕 원단, 목선의 열린 영역, 그 뒤의 지정 대상

**선택된 뜻의 필수 구성:**

- Openwork cells belong to the attached lace strip.
- The base garment remains a separate surface with its own opacity.
- A neckline opening exposes only its declared bounded region.

**관계:**

- lace strip → attaches_along → base garment edge
- openwork cells → interrupt → lace strip coverage
- neckline boundary → bounds → declared exposed region

**사례 조건:** 원문이 명시한 가슴골은 지우지 않고 나머지 의복 가림도 남긴다. 레이스의 빈 셀은 그 아래 바탕층에 가려질 수 있다.

**독립 선택/한계:** 꽃무늬·스캘럽 한 가지를 모든 lace trim의 필수 도안으로 고정하지 않는다. 투과도는 해당 원단/영역에만 적용한다.

**혼동 금지:**

- 레이스 프린트를 실제 구멍으로 통과
- 레이스 띠 때문에 드레스 전체를 투명화
- 일반 neckline에 추가 파임/가슴골을 발명

**현행 항목 검토:** lace_trim_attached_edge, slot:garment_detail:lace_trim_edge, decolletage_neckline_exposure

**자료:** A03, A05, A06, R07

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-005 · 젖음·밀착·반사·부분 비침의 조건부 결합

P0 · claim_guard · 키워드 K016, K017, K018, K019, K020, K021, K022, K023, K024, K026, K035, K036, K037, K038, K039, K040, K042 · 기존 VEL-006, VEL-007, VEL-008, VEL-014, VEL-015, VEL-016, VEL-017

**소유자:** 지정된 원단/머리/피부의 국소 영역과 광원·겹침 경로

**선택된 뜻의 필수 구성:**

- Wetness, adherence, surface reflection and light transmission remain separate selected properties.
- Any transmitted underlying color passes through the declared cloth region while its textile boundary stays visible.
- Highlight placement follows the local surface orientation and the declared light-view geometry.

**관계:**

- wet region → belongs_to → declared material owner
- cloth overlap → changes_path_through → selected textile layers
- highlight → is_received_on → source-facing local surface

**사례 조건:** K042의 wet OR clingy를 AND로 바꾸지 않는다. K035/037의 약한 비침은 유지하되 젖음 하나만으로 추가 비침을 만들지 않는다.

**독립 선택/한계:** 젖어 어두워지는 영역·늘어진 주름·겹쳐 덜 비침은 선택된 소재와 장면의 실현 예다. 무광, 가죽 결, 주름 산의 밝음을 전 소재의 법칙으로 만들지 않는다.

**혼동 금지:**

- wet를 transparent로 자동 동의어화
- 반사 띠를 젖음의 유일한 증거로 삼음
- 능선은 언제나 밝고 골은 언제나 어둡다고 강제
- NIR/UV 투과 연구를 가시광 노출 증거로 전용

**현행 항목 검토:** pfe_opaque_fit, satin_directional_luster_drape_surface, wet_damp_clumped_hair_state

**자료:** A03, A05, A06, A08, R11, R12, R20

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-006 · 거울의 결로 표면과 얼굴 초점의 다른 경로

P0 · new_relation_trial · 키워드 K041, K043, K059, K061, K077, K079 · 기존 VEL-018, VEL-025, VEL-030, VEL-031

**소유자:** 거울 전면의 결로 패치, 거울 반사 경로, 인물 얼굴

**선택된 뜻의 필수 구성:**

- Condensation droplets or a scattering haze occupy a localized patch of the mirror surface.
- The reflected image loses local contrast through that patch rather than the whole scene acquiring uniform blur.
- The requested face-focus hierarchy remains readable through the selected usable viewing region.

**관계:**

- condensation patch → lies_on → mirror front surface
- scattering patch → attenuates → local reflected image contrast
- selected focus → prioritizes → requested face plane

**사례 조건:** K043의 김 서림·물방울 소유자를 거울로 유지하고 K079의 얼굴 주 초점을 별도로 보존한다.

**독립 선택/한계:** 물막이 항상 희거나 불투명한 것은 아니다. 닦인 영역·흐른 자국·방울 크기는 원문/선택에 있을 때만 사용한다.

**혼동 금지:**

- 렌즈 디포커스를 거울 결로로 통과
- 얼굴 자체를 얼룩/백색 막으로 덮음
- 거울이 김 서렸다는 이유로 젖은 의상을 추가

**현행 항목 검토:** slot:texture:condensation_window_smear_texture, rb_glass_reflection_transmission

**자료:** A06, A07, A09

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-007 · 초커 앞의 열린 금속 고리와 부착점

P0 · new_relation_trial · 키워드 K046, K047 · 기존 VEL-020

**소유자:** 초커 띠, 그 앞 중앙의 고리, 고리 안의 실제 배경/띠

**선택된 뜻의 필수 구성:**

- A rigid circular metal perimeter is attached at the front center of the declared choker band.
- Its center is an actual aperture rather than a solid round medallion.
- The band follows the neck while the rigid ring retains its own shape.

**관계:**

- ring fitting → attaches_to → choker front center
- ring perimeter → bounds → open aperture
- choker band → follows_contour_of → neck

**사례 조건:** S04의 검정 띠와 은색 O-ring은 사례값이다. 고리 안으로 보이는 대상은 실제 시점·겹침에 맞춘다.

**독립 선택/한계:** 금속 반사와 얕은 접촉 그림자는 광원/시점에 따른 실현 단서다. 고리가 있다고 사슬·견인·조임을 추가하지 않는다.

**혼동 금지:**

- 단단한 원판 팬던트로 대체
- 귀걸이/손가락 고리를 목의 고리로 통과
- 고리 중앙에 검정 색칠만 해서 구멍처럼 처리

**현행 항목 검토:** slot:wearable_accessory:ctx_c019, slot:wearable_accessory:y2kr_grommet, slot:wearable_accessory:y2kr_tattoo_choker

**자료:** A06, R11

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-008 · 초커 또는 넥 아머의 대안과 사례 보석

P1 · context_guard · 키워드 K048, K051 · 기존 VEL-020, VEL-022

**소유자:** 선택된 목 장식 또는 보호판, 앞 중앙 장식

**선택된 뜻의 필수 구성:**

- Only the chosen collar-band or neck-armor realization occupies the specified neck region.
- A source-case central gem belongs to that chosen accessory and has a visible mounting.

**관계:**

- chosen accessory → surrounds → declared neck region
- central gem → mounts_on → chosen accessory front

**사례 조건:** S03의 엘프 문양, 깊은 청/남청 보석, 허벅지 일부 보호판은 해당 원문 문맥값이다.

**독립 선택/한계:** 일반 넥 아머에 엘프 문양·청색 보석을 필수화하지 않는다. 초커 OR 넥 아머 선택을 유지한다.

**혼동 금지:**

- 대안 두 물건을 무조건 동시 착용
- 넥 아머에 원문 없는 보호 성능을 부여
- 일부 허벅지 보호판을 전신 중갑으로 확대

**현행 항목 검토:** slot:wearable_accessory:royal_crest_choker

**자료:** R16, A06

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-009 · 장식 사슬의 끝점·중력 곡선·부품별 반사

P1 · extend_review · 키워드 K049, K050, K053 · 기존 VEL-021

**소유자:** 의복의 두 부착점과 그 사이 사슬, 버클

**선택된 뜻의 필수 구성:**

- The selected chain has visible attachment endpoints on the declared garment hardware.
- The loose span sags between its supports while the links remain distinct from the flexible strap.
- Buckles connect their own strap ends and panels.

**관계:**

- chain endpoint A → attaches_to → garment anchor A
- chain endpoint B → attaches_to → garment anchor B
- loose chain span → hangs_between → two garment anchors

**사례 조건:** S03 허리·골반의 느슨한 장식 연결과 S02 버클은 소유자와 위치를 섞지 않는다.

**독립 선택/한계:** 사슬의 모양은 길이·끝점 높이·자세에 따른다. 한 끝에 매단 펜던트는 별도 대안으로 다룬다.

**혼동 금지:**

- 사슬이 허공에 뜸
- 끝점 없이 늘어진 선만 그려 연결로 통과
- 느슨한 장식을 팽팽한 구속 사슬로 전환

**현행 항목 검토:** slot:wearable_accessory:y2kr_chain_strap, slot:wearable_accessory:unif_lapel_chain_separate_inner_neck

**자료:** A04, R17

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-010 · 침구 눌림과 휴식 자세의 국소 대응

P0 · new_relation_trial · 키워드 K054, K055, K056, K057, K065 · 기존 VEL-024, VEL-028

**소유자:** 누운 인물의 머리·등/어깨, 베개·시트의 해당 접촉 패치

**선택된 뜻의 필수 구성:**

- The resting body has the selected support contacts without floating or penetrating.
- The soft bedding depression occurs directly under the declared contact patch.
- The adjacent bedding remains relatively less compressed and traceable as the same surface.

**관계:**

- head or shoulder → rests_on → selected pillow patch
- body contact patch → deforms → local bedding region
- free hand → remains_near → declared head or neck position

**사례 조건:** S03의 베개·긴 은백색 머리 퍼짐은 사례 조건이다. 손을 목 근처에 둔 휴식을 목 압박으로 바꾸지 않는다.

**독립 선택/한계:** 모든 supine 자세에 베개·긴 머리·침대나 접촉 주름을 추가하지 않는다. 우연히 시선이 만남·잠들기 전은 서사다.

**혼동 금지:**

- 빈 곳의 주름을 신체 접촉 흔적으로 통과
- 베개가 몸을 관통
- 누운 자세에 반드시 고개/시선 방향을 한 가지로 고정

**현행 항목 검토:** pv_profile_supine, pv_profile_side_lying

**자료:** A04, R17

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-011 · 작은 입술 틈·치아 비노출·자연 비대칭

P0 · new_relation_trial · 키워드 K069, K070, K071, K072, K196, K197, K198, K207, K208, K211 · 기존 VEL-028, VEL-029, VEL-058, VEL-059, VEL-060

**소유자:** 같은 초상 인물의 입술·턱·눈꺼풀과 별도의 어깨/골반

**선택된 뜻의 필수 구성:**

- The lips retain a small gap without a large jaw drop.
- In the S07 case the teeth remain concealed while the requested quiet expression persists.
- Source-specified small shoulder and pelvic asymmetries survive anatomy-defect exclusions.

**관계:**

- lip gap → belongs_to → subject mouth
- teeth → remain_occluded_by → selected lip-jaw configuration
- hands and shoulders → remain_connected_in → declared towel-holding posture

**사례 조건:** 1–2 mm는 요청 수치로 보존하지만 픽셀 스케일 없는 사진으로 실측 PASS를 주장하지 않는다. S07 치아 비노출을 모든 parted lips의 뜻으로 일반화하지 않는다.

**독립 선택/한계:** 편안한 눈꺼풀은 반쯤 감은 눈·졸음의 고정 형상이 아니다. 미세 비대칭의 방향/크기도 요청 범위다.

**혼동 금지:**

- 치아를 보여주는 큰 웃음으로 바꿈
- small gap를 밀리미터 계측 성공으로 보고
- broken wrist 제외를 강제 양손 대칭으로 처리

**현행 항목 검토:** ae_profile_lip_press, ae_profile_lip_tighten, contrapposto_weight_shift

**자료:** A07, R05

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-012 · 머리 방향·안구 시선·거울 목표의 독립 축

P0 · extend_review · 키워드 K056, K059, K060, K061, K065, K066, K067, K068, K069, K072, K077, K127 · 기존 VEL-025, VEL-026, VEL-028, VEL-030, VEL-043

**소유자:** 실제 머리, 두 눈의 시선 방향, 렌즈 또는 자신의 거울상 위치

**선택된 뜻의 필수 구성:**

- The selected gaze target is retained independently of head orientation.
- A reflected-face target corresponds to the same depicted actor rather than a second person.
- A raised chin may coexist with eyes directed toward the declared interlocutor.

**관계:**

- eyes → look_toward → selected target
- head orientation → belongs_to → same actor
- mirror image → corresponds_to → depicted actor

**사례 조건:** S07은 렌즈, S06은 자기 거울상, S14는 상대 인물을 목표로 한다. 얼굴을 보는 POV의 목표도 유지한다.

**독립 선택/한계:** 눈·머리 방향이 항상 일치해야 한다는 규칙을 만들지 않는다. 시선 머묾·움직임을 따라가지 않음은 정지 이미지로 시간 검증되지 않는다.

**혼동 금지:**

- 거울 안 두 번째 인물 생성
- 턱을 든다는 이유로 상대를 향한 안구 방향까지 위로 이동
- 직접 응시를 동의/욕망/적대로 동의어화

**현행 항목 검토:** slot:gaze_target:head_eye_counterorientation_relation, slot:gaze_engagement:pv_gaze_direct

**자료:** A07, A11, R04, R05

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-013 · 시점 높이·거리·촬영 방향·초점의 네 가지 보존

P0 · extend_review · 키워드 K073, K074, K075, K076, K078, K079, K080, K081, K082, K117, K212 · 기존 VEL-030, VEL-031, VEL-042, VEL-060

**소유자:** capture camera, 상대 얼굴, 접촉/가림의 필수 경계

**선택된 뜻의 필수 구성:**

- Camera height is specified relative to the declared observer and subject.
- The camera axis retains its named face target.
- Viewing distance, projected proportions and the selected focus plane are recorded separately.

**관계:**

- camera optical axis → points_toward → declared face target
- camera viewpoint → has_height_relative_to → observer or subject
- focus plane → prioritizes → declared face and necessary relation

**사례 조건:** S15 바닥 가까운 눈 위치와 얼굴을 올려다봄은 비성적 시점이다. K079 얼굴 초점을 재질 강조를 이유로 옮기지 않는다.

**독립 선택/한계:** 같은 framing은 크롭으로도 만들 수 있으므로 close-up만으로 실제 거리 실측을 주장하지 않는다. 렌즈 초점거리만으로 원근을 확정하지 않는다.

**혼동 금지:**

- 카메라 저각을 옷 안쪽 시선으로 바꿈
- 얼굴을 확대/재설계해 가까움처럼 처리
- 거울 초점과 거울 표면 초점을 같은 평면으로 자동 취급

**현행 항목 검토:** slot:camera_height:water_w191

**자료:** A07, R13

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-014 · 반투명 방어막·공격 경로·충돌 영역의 깊이 순서

P0 · new_relation_trial · 키워드 K104, K105, K106, K107, K108, K109, K110, K111, K112, K113 · 기존 VEL-038, VEL-039, VEL-040

**소유자:** 시전자/지팡이, 방어막, 뒤의 인물, 충돌점·입자

**선택된 뜻의 필수 구성:**

- The selected barrier lies between the incoming effect and the protected figure.
- The figure remains partly readable behind the barrier surface.
- The localized impact zone occurs where the incoming path meets that surface rather than on the figure.

**관계:**

- incoming effect → meets → barrier contact zone
- barrier → lies_in_front_of → protected figure
- impact particles → originate_near → declared contact zone
- cloak attachment → remains_on → same actor shoulder

**사례 조건:** S10의 teen/young adult 혼용은 비성적 판타지 액션으로만 유지한다. white-gold 입자는 해당 충돌 효과의 색 조건이다.

**독립 선택/한계:** 막의 문양·형태, 모든 입자의 초점 차이·속도는 고정하지 않는다. 원문 없는 신체 명중은 추가하지 않는다.

**혼동 금지:**

- 방어막을 인물 뒤 장식으로 이동
- 투명 원을 만들고 공격 경로는 몸에 명중
- 입자를 모두 같은 전경층에 겹쳐 관통

**현행 항목 검토:** slot:ambient_particle:egr_localized_suspended_particles

**자료:** A05, A06, A07, R04

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-015 · 등 뒤 기계 장비의 연결과 원문 색 변형

P1 · extend_review · 키워드 K083, K084, K085, K086, K087, K088, K089, K090, K091, K092, K093, K094, K182, K183, K190, K202 · 기존 VEL-032, VEL-033, VEL-037, VEL-057, VEL-058, VEL-059

**소유자:** 기계식 등 장비, 그 지지 프레임, 같은 인물의 외부 갑옷

**선택된 뜻의 필수 구성:**

- The external back equipment is connected to a visible support on the same torso.
- Equipment arms remain distinct from biological limbs.
- The specified prop count, carried state and support connections are independently preserved.

**관계:**

- equipment arms → attach_to → back frame
- back frame → mounts_on → same actor external armor
- declared weapons → remain_in → selected held holstered or mounted state

**사례 조건:** S16 검정·흰색·은색 외장과 작은 주황 관절 발광은 해당 사례 변형에만 둔다. 붉은 코드/기계 발광과 색 소유자를 분리한다.

**독립 선택/한계:** 장비 수와 방향, 색을 미래 무장의 보편 형상으로 고정하지 않는다. 등 연결이 읽히지 않으면 실제 연결 PASS를 주장하지 않는다.

**혼동 금지:**

- 장비 팔을 추가 신체 팔로 합침
- 본체와 떨어진 부유 장비로 대체
- 두 권총을 양손 사격 상태로 자동 강화

**현행 항목 검토:** slot:prop:real_holstered_service_pistol, slot:action:carrying_holstered_real_sidearm

**자료:** A04, A06, R16

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-016 · 접촉을 만드는 신발과 별도의 지지 발

P0 · new_relation_trial · 키워드 K080, K081, K082, K114, K115, K117, K118, K119, K120 · 기존 VEL-030, VEL-041, VEL-042

**소유자:** 서 있는 인물 A의 접촉 신발, 낮은 위치의 상대 B 윗가슴 의복, A의 다른 발과 바닥

**선택된 뜻의 필수 구성:**

- The declared shoe contacts the declared upper-chest clothing patch of the other actor.
- That local soft cloth patch responds at the same contact location.
- The other foot supports the standing actor on the floor independently of the contact shoe.

**관계:**

- actor A contact shoe → contacts → actor B upper-chest clothing patch
- actor A other foot → rests_on → floor
- actor A support leg → supports → actor A torso
- observer eye viewpoint → belongs_to → actor B

**사례 조건:** S15는 비성적 강압 문맥으로만 보존한다. 접촉 도구가 신발이라는 뒤쪽 분해의 추가값은 원문 인증 전 사례 주장으로 기록한다.

**독립 선택/한계:** 힘의 수치, 통증, 호흡 손상, 반복 타격, 노출을 추가하지 않는다. 장래 중립 검증은 별도 성인 가상 인물과 비성적 장면으로 설계한다.

**혼동 금지:**

- 손 접촉으로 신발 접촉을 대체
- 접촉 발에 모든 체중을 이전
- 바닥 지지 발을 상대 몸 위로 이동
- 낮은 카메라만 있고 실제 접촉은 없음

**현행 항목 검토:** slot:contact_point:pv_foot_wall

**자료:** A04, R17

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-017 · 접촉·누름·제한·지속 압력의 증거 단계

P0 · claim_guard · 키워드 K115, K116, K118, K120, K182, K183 · 기존 VEL-041, VEL-042, VEL-057

**소유자:** 맞닿은 두 표면, 국소 변형, 동작 제한 관계, 별도의 시간 구간

**선택된 뜻의 필수 구성:**

- Contact is recorded at the named surfaces rather than inferred from projected overlap.
- A selected pressing depiction retains a local contact-response cue on the soft receiver.
- Steady duration and force magnitude remain unmeasured from one still image.

**관계:**

- declared effector → contacts → declared receiver patch
- local response → belongs_to → receiver surface
- temporal claim → requires → specified multi-frame evidence

**사례 조건:** holds down의 강압 의미를 자발적 휴식으로 순화하지 않는다. 한 프레임에서는 제약을 읽히는 배치만 검토하며 실제 움직임 제한 실험을 했다고 주장하지 않는다.

**독립 선택/한계:** 그림자가 어둡다고 큰 힘으로 판정하지 않는다. 정적 균형과 실제 동적 하중은 별도다.

**혼동 금지:**

- 화면상의 겹침을 실제 접촉으로 통과
- 단단한 접촉 그림자만으로 힘/시간을 정량화
- 정지 이미지로 반복 유지·호흡 영향까지 PASS

**현행 항목 검토:** slot:contact_point:no_contact_just_close

**자료:** A04, A11, R17

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-018 · 질책 손과 얼굴 사이의 가시적인 간격

P0 · new_relation_trial · 키워드 K121, K122, K123, K124, K125, K126, K127, K128, K129, K130, K131, K132 · 기존 VEL-043, VEL-044

**소유자:** 발화자 손, 상대 얼굴, 두 인물의 문턱 위치

**선택된 뜻의 필수 구성:**

- The raised or extended hand and the other actor face remain separated by a readable gap.
- Both endpoints and the intervening space are framed together.
- The dialogue or rebuff context remains separate from physical striking.

**관계:**

- speaker hand → remains_separated_from → other actor face
- visible interval → lies_between → same hand and same face
- actors → occupy_sides_of → declared threshold

**사례 조건:** S14의 비성적 언쟁, 치켜든 턱, 상한 자존심은 신체 부상·폭행으로 바꾸지 않는다. 문턱은 source-case 공간값이다.

**독립 선택/한계:** 손을 가리거나 화면 밖으로 보내 비접촉을 통과시키지 않는다. 원근상 겹쳐 경계가 확인되지 않으면 미관찰이다.

**혼동 금지:**

- 손이 얼굴을 누르는 접촉으로 변경
- 두 끝점 중 하나를 가려 무접촉으로 통과
- wounded disbelief를 멍/출혈로 해석

**현행 항목 검토:** slot:contact_point:no_contact_just_close

**자료:** A07, R04, R05

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-019 · 내려든 검·장갑 벗기·발도의 현재 상태

P1 · extend_review · 키워드 K087, K095, K096, K097, K098, K099, K100, K101, K102, K103, K133, K137, K138, K139 · 기존 VEL-032, VEL-033, VEL-034, VEL-035, VEL-036, VEL-045, VEL-046

**소유자:** 검/장갑/칼집/손의 독립 연결과 현재 배치

**선택된 뜻의 필수 구성:**

- A lowered sword points toward the floor with its holding arm down beside the actor.
- A glove-removal state retains the pulling hand, the glove edge and the other wrist.
- A partially drawn prop remains aligned with its storage opening without being converted to a discharged or striking state.

**관계:**

- holding hand → grips → declared prop
- glove-removal hand → grasps → other glove edge
- partly drawn blade → continues_into → same sheath opening

**사례 조건:** S09 전투 후 정리 동작과 S19 발도 도중은 서로 다른 사례다. 느리게·막 끝난이라는 시간 수식은 별도 서사로 유지한다.

**독립 선택/한계:** 세 상태를 한 인물/한 손에 무조건 동시 합치지 않는다. 재장전의 기술 절차나 실제 무기 성능은 연구 범위가 아니다.

**혼동 금지:**

- 내려든 검을 상대 조준 상태로 변경
- 장갑 벗김을 상대 손목 잡기로 대체
- 발도 순간을 찌르기/발사 결과로 확대

**현행 항목 검토:** slot:action:carrying_holstered_real_sidearm

**자료:** A04, A11

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-020 · 유리 파편과 불투명 잔해의 재질 대비

P1 · new_relation_trial · 키워드 K112, K134, K135, K136, K140, K141, K142, K143, K144 · 기존 VEL-039, VEL-045

**소유자:** 지정된 유리 파편과 별도의 불투명 잔해, 그 근처 파손 물체

**선택된 뜻의 필수 구성:**

- The broken glass retains angular transparent or reflective fragment surfaces.
- The selected opaque rubble remains a different material with traceable broken faces.
- Damage belongs to the declared environment object rather than the character body.

**관계:**

- glass fragments → belong_to → declared broken glass object
- opaque rubble → belongs_to → declared damaged structure
- fragment reflection → receives → local light

**사례 조건:** 원문의 일부 파손·아주 옅은 먼지와 S16의 도시 폐허/검은 연기는 규모와 소유자를 분리한다.

**독립 선택/한계:** 모든 유리 모서리의 반짝임이나 모든 돌의 무광을 의무화하지 않는다. 빛·거칠기·오염 상태에 따라 가시 단서를 정한다.

**혼동 금지:**

- 회색 불투명 자갈을 유리 파편으로 통과
- 환경 잔해를 인체에 박힌 파편으로 전환
- 약한 먼지를 짙은 연막/대형 화재로 확대

**현행 항목 검토:** rb_glass_reflection_transmission

**자료:** A06, R11, R12

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-021 · 유리에 눌린 접촉을 가까움·반사와 구별

P0 · new_relation_trial · 키워드 K169, K173, K183 · 기존 VEL-054, VEL-057

**소유자:** 지정된 신체/의복 부분, 유리면, 실제 접촉 패치

**선택된 뜻의 필수 구성:**

- The declared contacting part meets the glass plane rather than stopping across a visible gap.
- A pressed depiction has a bounded local contact-response cue, consistent with the stated material.
- Reflected overlap is recorded as an optical image and does not substitute for contact geometry.

**관계:**

- declared body or cloth patch → contacts → glass plane
- local flattening or cloth compression → belongs_to → contacting soft patch
- reflection → is_optical_image_of → nearby scene

**사례 조건:** K169 분해의 바로 가까이에 놓임 OR 반사 겹침만으로 pressed를 통과시키지 않는다. 원래의 접촉 의도는 보존한다.

**독립 선택/한계:** 원문에 없는 강한 변형, 밀어붙인 행위자, 부상은 추가하지 않는다. 지정된 접촉 부위는 frozen core로 해결한다.

**혼동 금지:**

- 유리와 떨어져 있는 근접 초상으로 대체
- 반사 얼굴을 실제 유리 접촉 얼굴로 통과
- 모든 접촉을 심한 얼굴 변형으로 과장

**현행 항목 검토:** rb_glass_reflection_transmission

**자료:** A04, A06, A07, R11

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-022 · 수중·닫힌 용기·막힌 경로와 갇힘 서사

P0 · context_guard · 키워드 K166, K167, K168, K170, K171, K172, K174 · 기존 VEL-052, VEL-055

**소유자:** 용기 경계, 내부 인물과 물, 요청된 이동 경로의 장벽

**선택된 뜻의 필수 구성:**

- The underwater setting has declared water and container cues on their own carriers.
- The chamber boundaries remain continuous where shown.
- If confinement is requested, a declared attempted path meets its blocking boundary rather than relying only on absent exits in a crop.

**관계:**

- container boundaries → enclose → selected interior
- water cues → belong_to → selected interior medium
- declared attempted path → meets → blocking boundary

**사례 조건:** 갇힘/불안 설정은 서사로 남긴다. 열린 출구가 프레임에 없다는 사실로 실제 탈출 불가·질식·사망을 인증하지 않는다.

**독립 선택/한계:** 일반 수중 초상에는 막힌 경로·공포·구조를 발명하지 않는다. 경로는 요청이 갇힘을 요구하고 명확한 관계가 있을 때만 검증 대상으로 둔다.

**혼동 금지:**

- 크롭에서 출구 부재를 물리적 감금 증거로 통과
- 닫힌 챔버를 우주 유해환경 habitat으로 자동 전환
- 물방울만으로 인물이 수중에 있다고 확정

**현행 항목 검토:** slot:location:hr_sealed_habitat_external_limit

**자료:** A05, A07, R18

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-023 · 붉은 얼룩·빛 기호·기계 발광·반사 수신면

P0 · new_relation_trial · 키워드 K019, K040, K146, K149, K154, K155, K173, K185, K188, K201, K214, K215 · 기존 VEL-006, VEL-017, VEL-047, VEL-054, VEL-057, VEL-059, VEL-060

**소유자:** 공중 코드 기호, 기계 틈의 광원, 근처 금속 수신면, 표면 얼룩

**선택된 뜻의 필수 구성:**

- Airborne red symbols remain separated luminous shapes rather than surface smears.
- The subtle machine light originates inside its declared seam or aperture.
- Any red reflection belongs to the adjacent receiver surface and follows the selected light geometry.

**관계:**

- code symbols → occupy → declared air volume
- machine seam light → emits_from → machine aperture
- emitted light → is_received_on → adjacent metal edge
- stain → adheres_to → separate specified surface

**사례 조건:** S16 no blood 아래에도 붉은 코드·진홍 기계 발광은 남긴다. S18 dark red stains는 혈액인지 원문 문맥 없이 판정하지 않는다.

**독립 선택/한계:** 코드 문자의 정확한 텍스트가 없으면 읽히는 임의 주문/문장을 추가하지 않는다. 빨강 하나로 광원 또는 혈액을 진단하지 않는다.

**혼동 금지:**

- no blood 때문에 붉은 광원까지 삭제
- 코드 입자를 피부의 혈흔으로 대체
- 기계 틈이 아니라 인물 피부를 자체 발광체로 만듦
- 반사 색을 재질의 본래 색으로 확정

**현행 항목 검토:** slot:light_type:status_led_glow, slot:ambient_particle:egr_localized_suspended_particles

**자료:** A06, R11, R12

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-024 · 양손 타월 윗단 장력·중앙 가림·수영복 가시 창

P0 · new_relation_trial · 키워드 K069, K071, K196, K197, K198, K207, K208, K209, K210, K211 · 기존 VEL-028, VEL-029, VEL-058, VEL-059, VEL-060

**소유자:** 동일 타월의 양쪽 손잡힘, 가로 윗단, 중앙/아랫단, 뒤의 수영복

**선택된 뜻의 필수 구성:**

- Each hand grips a declared point on the same towel upper edge.
- The upper edge is tensioned between the hands while the central and lower towel area hangs in front of the torso and pelvis.
- The selected towel coverage remains continuous across the specified front region.
- Only the source-specified small shoulder-strap window of the swimsuit remains visible.

**관계:**

- left hand → grips → same towel upper-edge point A
- right hand → grips → same towel upper-edge point B
- towel front panel → occludes → declared torso and pelvis front
- visible shoulder strap → belongs_to → swimsuit behind towel

**사례 조건:** S07 윗가슴 아래부터 허벅지 위쪽까지의 전면 가림, 대부분 가려진 산호색 수영복과 좁은 어깨끈은 사례 조건이다. 양손·자연스러운 높이 차이도 유지한다.

**독립 선택/한계:** 타월이 몸을 감싸는 변형과 양손으로 앞에 드는 변형은 별도다. 원문에 없는 배면 전체 가림·젖음·타월 크기 수치를 강제하지 않는다.

**혼동 금지:**

- 양팔 벌림 때문에 타월 중앙을 열어 전면을 노출
- 타월을 두 개로 나눔
- 수영복 대신 맨 피부를 가시 창으로 통과
- 몸에 두른 타월로 양손 지지 관계를 대체

**현행 항목 검토:** water_rel_w159, slot:garment_detail:water_w159

**자료:** A04, A06, A07

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-025 · 형태 오류 배제 아래 남아야 할 미세 비대칭

P0 · claim_guard · 키워드 K003, K055, K069, K072, K119, K120, K182, K198, K207, K208, K212, K216 · 기존 VEL-001, VEL-024, VEL-028, VEL-042, VEL-057, VEL-058, VEL-059, VEL-060

**소유자:** 주체의 관절 연결, 각 손과 타월, 좌우 지지/어깨 높이

**선택된 뜻의 필수 구성:**

- Wrists and shoulders retain anatomically coherent connections for the selected action.
- The request-specific small asymmetries are preserved rather than repaired into forced symmetry.
- Support leg and body alignment remain separate from style or attitude labels.

**관계:**

- hand → connects_through → same-arm wrist and elbow
- upper arm → connects_to → same actor shoulder
- selected asymmetry → belongs_to → declared pose or face property

**사례 조건:** K207/208은 생성된 형태 결함 제외이며 부상 설정이 아니다. S07의 미세 골반 이동·어깨 높이 차이와 S08의 참조 얼굴 자연 비대칭을 보존한다.

**독립 선택/한계:** 일반 균형을 contrapposto로 통일하지 않는다. 신체/표정 참조의 각도와 투영은 따로 검토한다.

**혼동 금지:**

- 자연 비대칭을 탈구로 오인
- 좋은 해부학을 이유로 요청된 한쪽 지지를 양쪽 동등 지지로 변경
- 비대칭 명칭만으로 관절 연결 결함을 허용

**현행 항목 검토:** contrapposto_weight_shift, slot:gaze_target:head_eye_counterorientation_relation

**자료:** A07, R17

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-026 · 감정·역할 분해를 선택 가능한 연기 예시로 유지

P1 · authoring_guidance · 키워드 K001, K002, K003, K004, K062, K064, K065, K066, K067, K068, K072, K083, K090, K100, K101, K103, K106, K121, K123, K124, K125, K128, K129, K130, K139, K145, K156, K157, K159, K161, K162, K163, K166, K167, K168, K174, K177, K179, K204, K211 · 기존 VEL-001, VEL-027, VEL-028, VEL-032, VEL-035, VEL-038, VEL-043, VEL-044, VEL-045, VEL-047, VEL-051, VEL-052, VEL-055, VEL-056, VEL-057, VEL-059, VEL-060

**소유자:** 요청된 정서/역할, 독립 외형 단서와 그 장면 맥락

**선택된 뜻의 필수 구성:**

- The requested affect or role remains an authored semantic layer.
- One compatible acting realization may support it without becoming its unique exact geometry.
- Alternative meanings and nonsexual distress contexts remain distinct.

**관계:**

- selected acting cue → supports → authored scene meaning
- context → qualifies → cue interpretation
- alternative affect option → remains_distinct_from → other option

**사례 조건:** 32개 해석 예시를 예시로 유지한다. 관능/몽환/경멸/불안과 눈꺼풀/입꼬리의 한 형태를 동의어로 만들지 않는다.

**독립 선택/한계:** 같은 의미의 다른 연기가 허용된다. 필요한 경우 원래 사건·반응·결과를 readable prose로 보존하며 예시의 기계적 강제는 피한다.

**혼동 금지:**

- pensive를 느린 눈 움직임 실측으로 통과
- 직접 시선을 자신감·동의의 충분조건으로 사용
- 고통/소진을 쾌락이나 자발적 복종으로 재해석

**현행 항목 검토:** 후보가 아닌 authoring/claim guard

**자료:** R05, A11

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-027 · 참조 외형 비례·투영 변화·성인 대상 조건

P1 · claim_guard · 키워드 K003, K212, K216, K217 · 기존 VEL-001, VEL-060

**소유자:** 요청된 주체 수/성인 설정, 참조의 보이는 얼굴·머리, 촬영 방향

**선택된 뜻의 필수 구성:**

- The depicted subject count remains the declared count.
- Adult status remains an explicit subject setting independent of facial appearance inference.
- Visible reference proportions are reviewed under compatible head orientation and perspective before claiming a redesign.

**관계:**

- reference proportions → guide → requested visible face appearance
- head orientation → changes_projection_of → same face
- adult setting → belongs_to → declared subject

**사례 조건:** FACE=LOCKED의 요청된 외형 유지와 ONE ADULT WOMAN의 한 명·성인 설정을 각각 보존한다. 실제 신원/법적 나이는 사진에서 인증하지 않는다.

**독립 선택/한계:** 표정·빛·고개 회전에 의한 apparent ratio 차이를 실제 골격 변경으로 단정하지 않는다. 근거 없는 비율 수치/생체 측정은 추가하지 않는다.

**혼동 금지:**

- 카메라 원근을 얼굴폭 확대 재설계로 보정
- 청순함을 아동 외형으로 변경
- 성인 외형처럼 보임을 실제 성인 확인으로 주장

**현행 항목 검토:** 후보가 아닌 authoring/claim guard

**자료:** A07, R05

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.


## VD-028 · 부정 조건의 소유 범위와 긍정 형상 보존

P0 · negative_firewall_plan · 키워드 K189, K190, K191, K192, K193, K194, K195, K196, K197, K198, K199, K200, K201, K202, K203, K204, K205, K206, K207, K208, K007, K027, K031, K042, K048, K066, K157, K163, K209, K210, K213, K214, K215 · 기존 VEL-003, VEL-010, VEL-014, VEL-020, VEL-028, VEL-049, VEL-052, VEL-058, VEL-059, VEL-060

**소유자:** 원래 부정 지시의 대상과 동시에 보존해야 할 의상·표정·장비·색

**선택된 뜻의 필수 구성:**

- Each exclusion retains its source owner, context and polarity.
- Allowed garment fit, slit, weapon, colored light and quiet expression remain intact under their relevant exclusions.
- OR alternatives remain alternatives, and source-specific coverage does not become a universal rule.

**관계:**

- source exclusion → constrains → its declared target property
- retained positive component → coexists_with → scoped exclusion
- alternative options → remain_in → authored OR relation

**사례 조건:** 20개 원래 부정 지시를 positive retrieval로 뒤집지 않는다. no gore/no blood 아래 전투 장비·붉은 빛은 남기고, 노골적 표현 금지 아래 원래 핏/슬릿은 남긴다.

**독립 선택/한계:** 타월·갑옷·상처 배제·소재 불투명을 다른 원자료에 전파하지 않는다. 제외조건을 더 안전한 새로운 장면으로 바꾸는 대신 원래 허용된 형상을 보존한다.

**혼동 금지:**

- nudity/lingerie 같은 부정 토큰을 새 후보 검색 요청으로 사용
- no blood로 모든 빨강을 제거
- 관능성 배제로 모든 표정을 삭제
- 원문의 OR를 all-of로 강제

**현행 항목 검토:** pfe_slit, pfe_opaque_fit, slot:light_type:status_led_glow

**자료:** A06, A10, R02

**픽셀 gate:** Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.

