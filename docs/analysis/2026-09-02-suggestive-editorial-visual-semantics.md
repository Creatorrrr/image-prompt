# 암시적 성인 에디토리얼 시각 의미·후보팩 구현

## 상태와 범위

- 상태: `implemented`, 픽셀 검증은 별도의 세 독립 arm에서 판정한다.
- 범위: 명백한 성인의 비노골적 패션·라이프스타일·피겨 스터디 표현만 다룬다.
- 넓은 반응·유통 용어인 `은꼴사`, `대꼴사`, `야짤`과 범위가 넓은 `세미 누드`, `임플라이드 누드`, `부두아르`는 단독 hard exact term으로 추가하지 않는다.
- 이미지에서 동의, 실제 촬영 관계, 숨은 의도, 성격, 정체성, 동일인 여부, 보편적 매력을 추론하지 않는다.

## 구현한 좁은 시각 계약

| 프로필 | 반드시 같은 이미지에 보여야 하는 관계 | 실패 대체물 |
|---|---|---|
| `adult_everyday_controlled_reveal_moment` | 명백한 성인, 자기주도 미완 일상 동작, 그 동작이 직접 바꾸는 한 개의 안정된 가림-드러남 경계, 어깨·쇄골·옆선·등선 또는 별도 기반층 중 한정된 목표 관계, 얼굴·동작·장소를 보존한 전체 프레임, 직물 물리, 축소 화면의 얼굴-경계 이중 초점, 경계를 닫으면 의미가 사라지는 반사실적 필요성 | 노출만, 불투명 의복끼리의 일반 겹침, 기존 벌어짐 옆의 무관한 손짓, 축소하면 사라지는 가장자리, 경계를 닫아도 평범한 패션 사진으로 그대로인 경우, 몸 파편 크롭, 몰래 촬영한 듯한 시점 |
| `strategic_coverage_figure_study` | 명백한 성인 인체, 비노골적 가림의 주된 운반체인 불투명 드레이프·랩·통합 형태, 연속된 가림 경로, 별도 완전 불투명 전신 의복이 없는 비중복 필요성, 가림체 양쪽의 윤곽 연속성, 방향성 형태광과 인체 경계 네거티브 스페이스, 머리·몸통·지지·사지가 함께 보이는 인체 연구 | 노골적 해부학, 이미 보디수트·드레스로 완전히 가린 인물 앞의 장식 가림판, 가림판을 제거해도 같은 사진, 검열 바, 검은 오려낸 실루엣, 몸 일부 크롭 |
| `underwear_as_outerwear_layer_system` | 명백한 성인 패션 피사체, 구조가 보이는 브라렛·캐미솔·슬립·보디수트 기반층, 별도 외층, 추적 가능한 레이어 교차·밑단·끈·라펠·여밈, 에디토리얼·룩북·공적 패션 맥락 | 언더웨어 단독, 수영복 단독, 우연히 보이는 끈, 피부에 칠한 듯한 시스루, 액세서리만 있는 스타일링 |
| `soft_window_private_room_adult_portrait` | 명백한 성인, 읽히는 침실·호텔 객실·드레싱 공간, 보이는 창과 반투명 커튼의 방향성 확산광, 자기주도 단장·옷 정리·공간 동작, 두께·겹침·접촉 그림자가 보이는 직물 관계 | 침실만, 란제리만, 평평한 하이키 노출, 수동적으로 누운 포즈, 문틈·숨은 카메라 시점 |

정확한 좁은 표현만 hard obligation이 된다. BM25F·embedding으로 발견된 인접 표현과 넓은 은어는 optional candidate로만 남는다.

## 후보 원자

### 자기주도 동작

- `shirt_cuff_adjustment_mid_action`
- `hair_tie_mid_action`
- `jewelry_fastening_mirror_action`
- `curtain_draw_window_pause`
- `jacket_lapel_settle_action`

동작은 손-대상 접촉, 미완 상태, 이미 정돈된 부분과 아직 정돈 중인 부분을 함께 요구한다. 팔을 올리거나 가슴에 손을 둔 정지 포즈는 대체할 수 없다.

### 가림·프레이밍 토폴로지

- `single_edge_layered_reveal_topology`
- `sheet_drape_stable_coverage_path`
- `forearm_coverage_contour_continuity`
- `environmental_three_quarter_face_body_context`
- `camera_acknowledged_observer_frame`

가림은 면적이 아니라 한 개의 추적 가능한 경계, 가림체 접촉, 가림체 양쪽 윤곽, 중력과 접촉 그림자로 판정한다. `camera_acknowledged_observer_frame`은 보이는 카메라 인지 단서일 뿐 실제 동의의 증명이 아니다.

### 의복 레이어와 표면

- `single_edge_layered_reveal_garment`
- `sheet_drape_stable_coverage_detail`
- `lace_edge_over_opaque_base`
- `visible_bralette_tailored_blazer_layer`
- `camisole_slip_over_shirt_layer`
- `waistband_reveal_outer_garment_edges`
- `sheet_fold_contact_shadow_surface`
- `ribbed_knit_body_boundary_surface`
- `lace_opaque_layer_separation_surface`
- `curtain_diffused_window_gradient_surface`

레이스·시스루·새틴이라는 소재 이름만으로는 충분하지 않다. 기반층, 가장자리, 실 구조, 두께, 미세 그림자, 여밈과 겹침 순서가 이미지에서 분리되어야 한다.

## 후보팩

- `adult_controlled_reveal_window_editorial`
- `strategic_coverage_figure_study_editorial`
- `underwear_outerwear_layered_editorial`
- `soft_window_private_room_editorial`

각 팩은 주 장면 하나, 자기주도 동작 하나, 가림 또는 레이어 관계 하나, 대표 소재 하나, 촬영 방식 하나를 우선한다. 여러 노출 경계와 여러 영웅 소재를 동시에 쌓지 않는다.

2026-09-02 회귀 수정에서는 `adult_controlled_reveal_window_editorial`의 동작을 실제 라펠-기반층 접촉이 있는 `jacket_lapel_settle_action`으로 좁혔고, `strategic_coverage_figure_study_editorial`은 불투명 드레이프가 주된 가림 운반체가 되도록 후보를 제한했다. 기존의 `camera_acknowledged_observer_frame`과 `forearm_coverage_contour_continuity`는 유효한 일반 후보로 남지만 이 두 프리셋의 기본 조합에서는 제외했다.

## 2026-09-02 실패 회귀와 개선 경계

- 이전 생성물은 프롬프트·런타임 감사가 통과했지만 사용자가 요청한 은근한 가림-드러남 효과가 실제 픽셀에서 보이지 않는다고 판정했다. 이 사용자 판정은 기술 게이트와 별개의 최종 증거로 보존한다.
- 원인은 넓은 은어의 미등록이 아니라, 기존 계약이 `어떤 경계가 존재함`만 요구하고 그 경계의 목표·행동 인과·축소 화면 현저성·반사실적 필요성을 요구하지 않은 데 있었다.
- 피겨 스터디 계약도 불투명 보디수트가 이미 모든 가림을 담당한 상태의 장식 스크린을 허용했다. 이제 가림체가 주된 비중복 운반체여야 하며, 제거하면 전략적 가림 명제가 사라져야 한다.
- 요청자가 어떤 지각 효과에 `초점`을 명시했는데도 그 의미가 uncovered이면 렌더를 진행하지 않는다. 정확히 동결된 코어가 좁은 프로필의 모든 관찰 요소를 이미 분해한 경우에만 request-scoped visual intent로 묶고, 그렇지 않으면 코어를 다시 만들거나 확인을 받는다.
- 이 수정은 `은꼴사`를 보편적 정의나 exact alias로 승격하지 않는다. 이번 검증은 그 넓은 표현을 명백한 성인의 비노골적 `행동-경계-한정 목표-현저성-필요성` 관계로 요청 범위 안에서만 분해한다.

## 근거가 데이터에 미친 영향

- 국내 바디프로필 연구: 포즈·표정·스타일·촬영 맥락을 사람의 정체성이나 가치와 분리했다.
- 다중 단서 콘텐츠 분석: 신체 크롭·포즈·표정·노출을 독립 단서로 두고 한 단서만으로 hard 의미를 만들지 않았다.
- FIT의 노출·가림 및 란제리 전시: 노출량보다 의복 경계, 직물 흐름, 기반층과 외층의 관계를 계약화했다.
- 부분 가림 지각 연구: 가림체 양쪽 윤곽 연속성을 피겨 스터디 게이트로 사용하되 관능성의 증거라고 확대하지 않았다.
- 확산광·플래시 자료: 커튼 확산창광과 하드플래시를 서로 다른 캡처 소유자로 유지했다.

상세 출처와 한계는 `docs/research-evidence/photo-prompt/research_evidence.jsonl`의 `suggestive_editorial_semantics_*` 행에 기록한다.

## 참조 이미지 경계

- 파일: `/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg`
- SHA-256: `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`
- 허용 범위: 보이는 성인 얼굴 비율, 긴 짙은 웨이브 헤어, 보이는 자연스러운 피부 질감.
- 금지 주장: 정체성, 동일인, 생체정보, 보호 특성, 매력도, 성격, 직업, 민족, 국적, 관계.

## 독립 세 arm 검증 규칙

1. 각 arm은 같은 원문 요청과 참조 이미지 해시를 사용하지만 별도의 request envelope, authorial core, pack, composed prompt, render request, 이미지와 manifest를 가진다.
2. 다른 arm의 프롬프트, 후보팩, 메시지, 이미지와 판정은 입력으로 사용하지 않는다.
3. 각 arm은 한 번만 생성한다. 다른 스타일을 얻기 위한 재시도는 하지 않는다.
4. 모든 해당 프로필 게이트를 thumbnail/native 선언에 맞춰 검사한다.
5. `partial`, 누락, 판정 불가는 실패다. 생성 차단은 `UNSCORED`이며 품질 0점이 아니다.
6. prompt/runtime audit PASS는 pixel PASS가 아니다. 사용자 미감 판단은 별도로 `pending`으로 남긴다.

세 arm의 검증 조합은 다음과 같이 분리한다.

- Arm A: `adult_everyday_controlled_reveal_moment` + `soft_window_private_room_adult_portrait`
- Arm B: `strategic_coverage_figure_study`
- Arm C: `underwear_as_outerwear_layer_system` + 기존 `mirror_selfie_reflection_device_topology`

각 서브에이전트는 배정된 계약 안에서 장면·소품·시간·보조 촬영 결정을 독립적으로 랜덤화하고 그 seed를 기록한다.
