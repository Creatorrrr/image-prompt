# 시각 의미 카드

모든 문장과 관계는 연구 초안이다. 출처는 개념군 지원이며 출처의 문장을 복제한 것이 아니다. 선택된 카드의 모든 핵심 gate를 함께 판독해야 한다.

## esp_direct_handoff — 접선 중 직접 전달

두 사람에게 각각 이어지는 손이 두 사람 사이 봉투의 반대쪽 끝에 닿는다.

Two separately traceable hands touch opposite edges of one envelope between two people.

- 소유자/관계: A.hand → contacts → envelope.edge1; B.hand → contacts → envelope.edge2
- 관찰 gate: 손 두 개의 소유자가 분리됨; 같은 봉투의 양 끝 접촉이 함께 보임
- 혼동 경계: 데드 드롭; 완료된 소유권 이전
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: relational_action, contact_point
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_suspended_handoff — 건네다 멈춘 손

한 사람이 봉투를 내밀고 다른 사람의 펼친 손과 봉투 사이에는 빈틈이 보인다.

One person extends an envelope while the other person's open hand remains separated from it by a visible gap.

- 소유자/관계: A.hand → holds → envelope; B.hand → separated_from → envelope
- 관찰 gate: 보유한 손과 빈손 구별; 봉투와 수신 손 사이 간격
- 혼동 경계: 이미 전달된 물건; 망설임의 확정
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: relational_action, contact_point
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_concealment_cavity — 열린 은닉 물체

열린 일상 물건의 별도 안쪽 공간에 접힌 종이가 들어 있다.

An opened everyday container exposes a distinct inner cavity holding a folded paper.

- 소유자/관계: container.cavity → contains → paper; container.lid → separated_from → container.body
- 관찰 gate: 일상 물건의 외곽; 내부 공간과 종이의 경계
- 혼동 경계: 단순 옆에 놓인 종이; 범죄 용도 확정
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_drop_placement — 무인 보관 위치에 놓기

손이 열린 홈 안에 작은 꾸러미를 내려놓으며 꾸러미 가장자리와 홈의 턱이 함께 보인다.

A hand lowers a small packet into an open recess, with the packet edge and recess lip visible together.

- 소유자/관계: A.hand → holds → packet; packet → enters → recess
- 관찰 gate: 손-꾸러미 접촉; 꾸러미와 홈의 입구
- 혼동 경계: 나중의 회수; 직접 맞교환
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: relational_action, contact_point
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_drop_spike — 중공 스파이크 전시

뾰족한 용기가 열려 있고 분리된 뚜껑과 접힌 종이가 입구 옆에 놓인다.

A pointed container lies open beside its detached cap and a folded paper at the cavity mouth.

- 소유자/관계: spike.cavity → opens_at → spike.mouth; cap → separated_from → spike
- 관찰 gate: 외형과 열린 입구; 분리된 뚜껑
- 혼동 경계: 기능 절차 재현; 정확한 박물관 복제
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_pocket_litter — 생활 흔적 소지품

한 사람의 열린 케이스 속 칸에 사용 흔적이 있는 표와 영수증, 접힌 카드가 나뉘어 있다.

A person's open case contains used tickets, a receipt and a creased card in separate compartments.

- 소유자/관계: person.hand → holds → case; case → contains → tickets
- 관찰 gate: 한 소유자의 열린 케이스; 구분되는 종이 물품
- 혼동 경계: 위조 확정; 실제 경력이나 정체성
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_identity_comparison — 신분 자료 비교

이름이 다른 신분 카드 두 장과 별도의 인물 사진이 같은 탁자 위에 놓인다.

Two differently named identity cards lie beside a separate portrait photograph, all within the same tabletop view.

- 소유자/관계: card1 → beside → card2; photo → separate_from → card1
- 관찰 gate: 카드 두 장의 경계; 요청된 경우에만 다른 이름의 판독
- 혼동 경계: 이중간첩의 증거; 사진 속 인물과 현장 인물 동일시
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_redaction — 문서의 가림 영역

경계가 분명한 종이 위 인쇄된 여러 줄의 일부를 불투명 직사각형이 가린다.

Opaque rectangular bars interrupt several lines of printed text on a bounded sheet.

- 소유자/관계: bars → occlude → sheet.text
- 관찰 gate: 종이 경계; 문자 줄과 가림의 교차
- 혼동 경계: 검은 무늬; 법적 등급이나 삭제 성공
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_document_seal — 봉인된 봉투

접착 봉인이 봉투 덮개와 몸체를 연속해서 잇는 부분이 가까이 보인다.

An unbroken adhesive seal bridges the envelope flap and body in one close view.

- 소유자/관계: seal → bridges → envelope.flap; seal → bridges → envelope.body
- 관찰 gate: 봉인의 양쪽 접점; 연속 표면
- 혼동 경계: 열람 이력 부재; 위조 불가능성
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_opened_flap — 벌어진 봉투 덮개

봉투 덮개가 몸체에서 벌어져 가장자리의 접착 섬유가 드러난다.

An envelope flap is lifted away from the body with exposed adhesive fibers along its edge.

- 소유자/관계: flap → separated_from → envelope.body; fibers → located_on → flap.edge
- 관찰 gate: 들린 덮개와 본체 분리; 가장자리 섬유
- 혼동 경계: 몰래 개봉한 과정; 다시 봉한 시간 순서
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_number_pad — 숫자열 패드

작은 종이 패드의 맨 위 장에 다섯 자리 숫자 묶음이 열을 이루어 보인다.

A small paper pad shows repeated columns of five-digit groups on its top sheet.

- 소유자/관계: pad → supports → sheet; sheet → carries → number_groups
- 관찰 gate: 패드와 인쇄면 분리; 요청된 숫자 묶음의 배열
- 혼동 경계: 일회용 사용 증명; 난수나 해독 성공
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_microdot_comparison — 미세 점과 확대 매체

편지 위 작은 점과 미세 인쇄를 확대한 별도 테두리 삽입 화면이 가는 선으로 연결된다.

A tiny dot on a letter is linked by a thin line to a separately bounded magnified inset of miniature print.

- 소유자/관계: letter.dot → linked_to → inset; inset → depicts → miniature_print
- 관찰 gate: 원본 점의 위치; 확대 창의 테두리와 연결
- 혼동 경계: 방 안에 거대한 문자가 존재함; 실제 촬영 단일 프레임
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state
- 근거군: S01, S05, S19, S20, S21; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_analysis_comparison — 분석 자료 비교

앉은 사람이 서로 다른 도표 선이 있는 보고서 두 장 사이를 가리킨다.

A seated person points between two separate reports with visibly different chart traces.

- 소유자/관계: A.finger → points_toward → report1; report1 → separate_from → report2
- 관찰 gate: 각 문서 경계; 비교되는 서로 다른 흔적
- 혼동 경계: 교차검증 완료; 내용의 진실이나 독립성
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: relational_action, gaze_target
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_source_chain_board — 자료 출처 연결도

테두리가 있는 문서 복사본 세 개의 화살표가 하나의 출처 카드로 모인다.

Three bounded document copies are linked by arrows that converge on one clearly marked origin card.

- 소유자/관계: doc1.arrow → points_to → origin; doc2.arrow → points_to → origin; doc3.arrow → points_to → origin
- 관찰 gate: 자료와 출처 카드 구분; 화살표 종점
- 혼동 경계: 독립 출처 셋; 순환 보고 실제 발생
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: narrative_clue
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_burn_bag — 폐기 봉투에 담긴 종이

탁자 위 열린 종이 폐기 봉투에서 인쇄된 종이들이 일부 나온다.

Printed sheets project from an open paper disposal bag on a desk.

- 소유자/관계: bag → contains → sheets; bag → rests_on → desk
- 관찰 gate: 봉투 입구와 종이 경계; 종이의 일부가 내부에 위치
- 혼동 경계: 불타는 장면 의무; 기밀 폐기 완료
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_briefing_table — 보고 테이블의 위치 관계

서 있는 한 사람이 탁자 건너 앉은 두 사람을 마주하고 가운데 지도 한 장을 함께 본다.

One standing participant faces two seated listeners across a table with one shared map.

- 소유자/관계: speaker → faces → listener1; speaker → faces → listener2; map → rests_on → table
- 관찰 gate: 세 인물의 독립 몸; 공유 지도와 시선 대상
- 혼동 경계: 직급 확정; 안보 승인이나 동의
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: body_pose, gaze_target
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_threshold_departure — 문턱의 이동 순간

한 사람의 앞발이 문턱을 넘고 다른 사람은 안쪽에서 문을 잡고 있다.

A person's leading foot crosses a doorway threshold while a second person remains inside holding the door.

- 소유자/관계: A.foot → crosses → threshold; B.hand → contacts → door
- 관찰 gate: 문턱과 발의 교차; 문의 손 접촉
- 혼동 경계: 탈출 성공; 구조인지 강제 이동인지
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: relational_action, contact_point
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_cash_envelope — 현금과 봉투의 관계

한 사람이 든 봉투에서 지폐 여러 장이 나오며 다른 사람의 손과 떨어져 있다.

Several banknotes extend from an envelope held by one person, apart from another person's hand.

- 소유자/관계: A.hand → holds → envelope; envelope → contains → banknotes
- 관찰 gate: 봉투와 지폐의 연결; 서로 다른 손
- 혼동 경계: 뇌물; 포섭 동기나 수락
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_kompromat_display — 사진을 제시하는 배치

한 사람이 탁자 건너 상대를 향해 테두리가 있는 사진을 들어 보인다.

One person holds a bounded photograph toward another person across a table.

- 소유자/관계: A.hand → holds → photo; photo.face → oriented_toward → B
- 관찰 gate: 사진 매체 경계; 제시 방향과 수신 인물
- 혼동 경계: 사진의 진위; 협박·성행위·동의의 확정
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: relational_action, contact_point
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_document_case — 잠금장치 있는 서류 케이스

단단한 직사각 케이스가 경첩을 중심으로 열려 안감과 내부 서류 더미가 보인다.

A rigid rectangular case opens on hinges, exposing its lining and a stack of papers inside.

- 소유자/관계: case.lid → hinged_to → case.body; case.body → contains → papers
- 관찰 gate: 경첩과 열린 내부; 서류의 수납 상태
- 혼동 경계: 폭발물이나 무기 추정; 소유자의 직업
- 주장 한계: Appearance does not prove secrecy, authenticity, allegiance, authorization, a previous/later act or successful communication.
- 제안 role: prop_state, prop_placement
- 근거군: S01, S05, S19, S20, S21; Draft semantic review required

## esp_earpiece_contact — 귀와 손과 이어피스

손끝이 같은 사람의 귀 입구에 자리한 이어피스에 닿는다.

A fingertip touches the earpiece seated at the same person's ear opening.

- 소유자/관계: A.finger → contacts → earpiece; earpiece → seated_at → A.ear
- 관찰 gate: 손-팔-몸 소유자 연결; 장치와 귀의 접점
- 혼동 경계: 귀 긁기; 실제 통화나 지시 청취
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: contact_point, hand_pose
- 근거군: S03, S06, S07, S08, S15; Draft semantic review required

## esp_receiver_pose — 수화기 청취 자세

한 손이 수화기를 들고 위쪽은 같은 사람 귀 옆, 아래쪽은 입 옆에 놓인다.

One hand holds a telephone receiver with its upper end beside the same person's ear and lower end beside the mouth.

- 소유자/관계: A.hand → holds → receiver; receiver.upper → beside → A.ear; receiver.lower → beside → A.mouth
- 관찰 gate: 손과 얼굴의 소유자; 양쪽 수화기 끝의 위치
- 혼동 경계: 시대가 다른 단말 혼합; 들리는 대화
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: contact_point, hand_pose
- 근거군: S03, S06, S07, S08, S15; Draft semantic review required

## esp_button_lens — 단추 위치의 렌즈

착용자 코트 앞면의 단추형 하우징 하나 안에 작은 유리 렌즈가 자리한다.

A small glass lens sits within one coat-button housing on the wearer's front.

- 소유자/관계: lens → inside → button_housing; button_housing → attached_to → coat.front
- 관찰 gate: 하우징과 코트 부착; 렌즈 경계가 읽히는 크기
- 혼동 경계: 평범한 단추 반사; 정확한 F-21 작동
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: wearable_accessory
- 근거군: S03, S06, S07, S08, S15; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_watch_camera — 손목시계형 카메라

손목에 얹힌 둥근 카메라 몸체에 작은 렌즈가 있고 스트랩이 같은 손목을 감싼다.

A wrist-mounted round camera body shows a small lens and a strap continuing around the same wrist.

- 소유자/관계: lens → part_of → camera; camera.strap → encircles → A.wrist
- 관찰 gate: 렌즈와 몸체; 스트랩과 손목의 연속성
- 혼동 경계: 시간 표시 기능; 비밀 촬영 성공
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: wearable_accessory
- 근거군: S03, S06, S07, S08, S15; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_reel_console — 릴 장치와 헤드폰

녹음기 위 별도 릴 두 개가 있고 케이블이 장치에서 착용한 헤드폰까지 이어진다.

Two separate reels sit on a recorder while a cable runs from the recorder to worn headphones.

- 소유자/관계: reel1 → mounted_on → recorder; cable → connects → headphones
- 관찰 gate: 릴과 장치 경계; 장치에서 헤드폰까지 경로
- 혼동 경계: 테이프가 돈다는 시간 주장; 도청된 음성
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: prop_placement
- 근거군: S03, S06, S07, S08, S15; Draft semantic review required

## esp_monitor_boundary — 감시 화면의 매체 경계

모니터 테두리 안에 작은 인물 영상이 있고 주위 방은 별도 공간으로 보인다.

A person's small image appears inside a monitor bezel while the surrounding room remains separate.

- 소유자/관계: monitor.bezel → bounds → display; display → depicts → person_image
- 관찰 gate: 화면 테두리; 영상 속 인물과 실내 인물 구분
- 혼동 경계: 실제 방에 인물이 중복됨; 실시간 연결
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: prop_placement
- 근거군: S03, S06, S07, S08, S15; Draft semantic review required

## esp_camera_target — 렌즈가 향한 대상

카메라 몸체와 렌즈 축이 보이는 거리 공간 건너 별도 인물을 향한다.

A camera body and its lens axis face a separate person across the visible street space.

- 소유자/관계: camera.lens_axis → points_toward → B; A.hand → holds → camera
- 관찰 gate: 장치와 대상 분리; 렌즈 방향을 읽는 공간
- 혼동 경계: 떠다니는 시선 광선; 실제 촬영 여부
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: gaze_target
- 근거군: S03, S06, S07, S08, S15; Draft semantic review required

## esp_window_observer — 창과 관찰자의 깊이

어두운 실내 인물이 커튼 가장자리 너머 창밖 별도 인물을 본다.

A person inside a dim room looks past the edge of a curtain toward a separate figure outside the window.

- 소유자/관계: A.gaze → passes → curtain_edge; A → inside → window; B → outside → window
- 관찰 gate: 실내외 경계; 관찰자와 대상의 다른 깊이
- 혼동 경계: 두 인물 합성; 감시 의도의 확정
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: body_pose, gaze_target
- 근거군: S03, S06, S07, S08, S15; Draft semantic review required

## esp_mirror_attention — 거울 속 대상에 향한 시선

한 사람의 눈이 뒤쪽 다른 사람의 반사가 담긴 벽 거울을 향한다.

A person's eyes turn toward a wall mirror containing a bounded reflection of another person behind them.

- 소유자/관계: A.gaze → toward → mirror; mirror → reflects → B
- 관찰 gate: 거울 테두리; 직접 인물과 대응 반사
- 혼동 경계: 얼굴 방향만의 설명; 기하적으로 불가능한 반사
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: gaze_target
- 근거군: S03, S06, S07, S08, S15; Draft semantic review required

## esp_tail_spacing — 거리에 따른 두 인물 배치

별도 보행자 두 명이 같은 방향을 향하고 둘 사이에 보도 구간이 보인다.

Two separate walkers face the same direction with a clear stretch of pavement between them.

- 소유자/관계: A → behind → B; A.foot → supported_by → pavement
- 관찰 gate: 보행 방향; 독립 몸과 거리
- 혼동 경계: 미행의 동기; 지속적으로 따라왔다는 이력
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: body_pose
- 근거군: S03, S06, S07, S08, S15; Draft semantic review required

## esp_concealed_device_view — 가구 경계의 소형 장치

열린 가구 패널 안 공간에 전선 달린 작은 장치가 일부 들어가 있다.

An opened furniture panel exposes a small wired device partly recessed inside the cavity.

- 소유자/관계: panel → opens_to → cavity; device → partly_inside → cavity
- 관찰 gate: 열린 패널과 공간; 장치와 전선
- 혼동 경계: 도청·폭발 기능; 설치 방법 전체
- 주장 한계: A visible device, indicator or image does not prove sound, transmission, recording, tracking, identity or covert intent.
- 제안 role: prop_placement
- 근거군: S03, S06, S07, S08, S15; Draft semantic review required

## esp_three_quarter — 사선으로 선 몸

서 있는 인물의 몸통이 카메라에서 일부 돌아 재킷 앞면과 한쪽 옆면이 함께 보인다.

A standing person's torso turns partway from the camera, showing the front and one side of the jacket.

- 소유자/관계: A.torso → turned_relative_to → camera
- 관찰 gate: 몸통 두 면; 카메라 기준 회전
- 혼동 경계: 스리쿼터 길이 크롭; 얼굴 각도와 몸통 각도 동일시
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_profile — 측면의 얼굴

얼굴이 옆으로 보여 한쪽 눈과 코에서 턱까지 이어진 윤곽이 드러난다.

The face is presented from the side, with one eye and a continuous nose-to-chin contour.

- 소유자/관계: camera → views_side_of → A.face
- 관찰 gate: 단일 측면 윤곽; 눈의 가시 상태
- 혼동 경계: 사선 얼굴; 관찰 대상의 방향
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_back_view — 등을 향한 시점

카메라가 인물 등을 향해 코트 뒷판과 목덜미가 보인다.

The camera faces the person's back, showing the rear coat panels and nape.

- 소유자/관계: camera → views_back_of → A
- 관찰 gate: 뒷판 구조; 몸 앞뒤 구분
- 혼동 경계: 얼굴 익명성의 보장; 떠난다는 시간
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_contrapposto — 한 다리에 체중을 둔 자세

서 있는 몸이 한 다리에 실리고 반대 무릎은 이완되며 골반과 어깨 경사가 대응한다.

One leg bears the standing body while the other knee relaxes, with opposed hip and shoulder tilt.

- 소유자/관계: A.support_leg → supports → A.pelvis; A.free_leg → relaxed_relative_to → A.support_leg
- 관찰 gate: 지지 발과 바닥; 골반·어깨 기울기
- 혼동 경계: S자 실루엣만; 양발 균등 지지
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_s_curve — S자 윤곽

몸통에서 골반까지 보이는 바깥 윤곽이 번갈아 굽는다.

The body's visible outer contour bends in alternating directions through torso and hips.

- 소유자/관계: A.contour → curves_through → A.torso; A.contour → curves_through → A.hips
- 관찰 gate: 연속된 윤곽; 구부러진 영역 구분
- 혼동 경계: 체중 다리의 자동 지정; 성격이나 성적 의도
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_squared_stance — 정면을 향한 상체

양 어깨와 가슴 면이 같은 맞은편 인물을 향한다.

Both shoulders and the chest plane face the same opposing person.

- 소유자/관계: A.chest → faces → B; A.shoulders → aligned_toward → B
- 관찰 gate: 어깨·가슴 방향; 상대 위치
- 혼동 경계: 카메라 정면과 혼동; 권력의 확정
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_wall_lean — 벽에 기댄 어깨

한쪽 어깨와 등 윗부분이 벽에 닿고 양발은 바닥에 놓인다.

One shoulder and upper back contact a wall while both feet remain on the floor.

- 소유자/관계: A.shoulder → contacts → wall; A.feet → supported_by → floor
- 관찰 gate: 어깨와 벽 접촉; 발의 지지
- 혼동 경계: 벽 앞에 떠 있는 몸; 피로 원인
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_mid_stride — 한 걸음 중간

보행자의 한 발은 지지하고 다른 발은 앞으로 들리며 코트 자락이 뒤로 남는다.

One foot supports the walker while the other foot lifts forward, with the coat hem trailing behind.

- 소유자/관계: A.support_foot → contacts → ground; A.free_foot → ahead_of → A.pelvis
- 관찰 gate: 서로 다른 발 상태; 지면 접촉
- 혼동 경계: 정지 자세의 속도 단정; 이전 이동 경로
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_upright_seated — 등을 세워 앉기

골반이 의자 좌판에 놓이고 몸통이 그 위로 곧게 선다.

A person's pelvis rests on a chair and the torso rises upright above it.

- 소유자/관계: A.pelvis → supported_by → chair.seat
- 관찰 gate: 골반과 좌판; 몸통의 연속성
- 혼동 경계: 서 있는 몸의 겹침; 충성이나 통제력
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_crossed_legs — 다리를 교차해 앉기

골반을 좌판에 둔 채 한쪽 허벅지가 다른 쪽 위를 무릎 부근에서 교차한다.

One thigh crosses over the other above the knees while the pelvis remains on the chair seat.

- 소유자/관계: A.thigh1 → crosses_over → A.thigh2; A.pelvis → supported_by → chair
- 관찰 gate: 두 다리의 몸 연결; 교차 위치
- 혼동 경계: 꼬인 추가 다리; 단순 발목 교차
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_forward_lean — 앞으로 기울인 상체

골반은 의자에 지지된 채 앉은 몸통이 탁자 쪽으로 기울어진다.

A seated torso inclines toward the table while the pelvis stays supported by the chair.

- 소유자/관계: A.torso → inclines_toward → table; A.pelvis → supported_by → chair
- 관찰 gate: 좌판 지지; 몸통과 탁자 간격
- 혼동 경계: 협박 의도; 몸통이 탁자를 통과함
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_crouch — 낮게 웅크린 몸

굽힌 무릎이 골반을 발뒤꿈치 가까이 낮추고 양발이 땅에 닿는다.

Bent knees lower the pelvis close to the heels while both feet meet the ground.

- 소유자/관계: A.knees → connected_upward_to → A.pelvis; A.knees → connected_downward_to → A.feet; A.feet → contacts → ground
- 관찰 gate: 무릎-골반-발 관절 사슬; 지면 지지
- 혼동 경계: 무릎 꿇기와 자동 동의어; 은신의 성공
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_over_shoulder_glance — 몸과 다른 방향으로 돌아본 고개

몸통이 앞을 향한 채 고개가 한쪽 어깨 위로 뒤를 돌아본다.

The torso faces forward while the head turns back above one shoulder.

- 소유자/관계: A.head → turned_relative_to → A.torso
- 관찰 gate: 같은 몸의 목 연결; 머리와 몸 방향 차이
- 혼동 경계: 오버숄더 숏; 모든 반대 방향 시선
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose, gaze_target
- 근거군: S16, S08; Draft semantic review required

## esp_sideways_glance — 곁눈질

얼굴은 대체로 앞을 향하고 보이는 눈동자는 한쪽으로 치우친다.

The face stays mostly forward while the visible pupils shift toward one side.

- 소유자/관계: A.pupils → offset_within → A.eyes
- 관찰 gate: 눈 흰자와 동공의 위치; 얼굴 축 유지
- 혼동 경계: 얼굴 전체 회전; 의심이나 거짓말
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: gaze_direction
- 근거군: S16, S08; Draft semantic review required

## esp_offscreen_gaze — 화면 밖 시선

인물의 보이는 눈이 화면 한쪽 바깥을 향하고 대상은 화면에 없다.

A person's visible eyes point past one edge of the image without a depicted target.

- 소유자/관계: A.gaze → toward → frame_outside
- 관찰 gate: 눈 방향; 화면 밖 종점 표기
- 혼동 경계: 보이지 않는 표적의 확정; 카메라 응시
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: gaze_direction
- 근거군: S16, S08; Draft semantic review required

## esp_downcast_gaze — 아래쪽 시선

눈이 얼굴 아래 놓인 종이 쪽으로 향한다.

The eyes angle down toward a paper below the face.

- 소유자/관계: A.gaze → toward → paper; paper → below → A.face
- 관찰 gate: 시선과 아래 종이; 종이 소유자 분리
- 혼동 경계: 슬픔의 확정; 고개만 숙임
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: gaze_direction, gaze_target
- 근거군: S16, S08; Draft semantic review required

## esp_chin_down — 턱을 낮춘 응시

턱은 아래로 기울고 눈은 앞사람을 향해 올라간다.

The chin tilts down while the eyes lift toward a person ahead.

- 소유자/관계: A.chin → lowered_relative_to → A.neck; A.gaze → toward → B
- 관찰 gate: 턱의 각과 눈 방향 분리; 앞사람 위치
- 혼동 경계: 아래만 보는 시선; 적대감 확정
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: gaze_direction, gaze_target
- 근거군: S16, S08; Draft semantic review required

## esp_listening_tilt — 귀 쪽으로 기울인 고개

수화기가 있는 쪽으로 고개가 조금 기울어진다.

A head inclines slightly toward the side where a receiver is held.

- 소유자/관계: A.head → tilts_toward → receiver
- 관찰 gate: 기울어진 머리; 장치의 실제 위치
- 혼동 경계: 말소리의 존재; 복종이나 수락
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose, gaze_target
- 근거군: S16, S08; Draft semantic review required

## esp_restrained_smile — 작은 입가 변화

입꼬리만 조금 올라가고 얼굴의 다른 부분은 비교적 움직임이 적다.

The mouth corners lift slightly while the rest of the face remains comparatively still.

- 소유자/관계: A.mouth_corners → raised_relative_to → A.mouth_center
- 관찰 gate: 입가의 국소 변화; 치아 노출 의무 없음
- 혼동 경계: 속마음·배신; 미소가 없는 얼굴
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: expression
- 근거군: S16, S08; Draft semantic review required

## esp_tense_jaw — 긴장된 턱선

입술이 맞닿고 볼 아래 턱선이 팽팽해 보인다.

The lips press together and the jaw contour appears taut beneath the cheek.

- 소유자/관계: A.upper_lip → contacts → A.lower_lip; A.jaw → beneath → A.cheek
- 관찰 gate: 입술 접촉; 턱선의 국소 긴장
- 혼동 경계: 공포·분노의 확정; 의학적 진단
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: expression
- 근거군: S16, S08; Draft semantic review required

## esp_cuff_adjustment — 소맷부리를 정리하는 손

한 손이 같은 착용자의 반대쪽 손목 소맷부리를 집는다.

One hand pinches the opposite sleeve cuff at the same wearer's wrist.

- 소유자/관계: A.hand1 → pinches → A.sleeve2.cuff; A.sleeve2.cuff → around → A.wrist2
- 관찰 gate: 양손의 소유자; 손끝과 커프 접촉
- 혼동 경계: 다른 사람 소매 정리; 커프링크스 착용 의무
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: hand_pose, contact_point
- 근거군: S16, S08; Draft semantic review required

## esp_lapel_hold — 라펠을 잡은 손

손가락이 같은 착용자의 재킷 접힌 라펠 가장자리를 잡는다.

Fingers grip the folded lapel edge on the same wearer's jacket.

- 소유자/관계: A.hand → grips → A.jacket.lapel
- 관찰 gate: 라펠 접힘; 손의 접점
- 혼동 경계: 셔츠 칼라; 재킷 전체를 벗는 동작
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: hand_pose, contact_point
- 근거군: S16, S08; Draft semantic review required

## esp_loose_tie — 느슨한 넥타이 매듭

손이 열린 칼라 아래 넥타이 매듭을 잡아 목과 매듭 사이 간격이 보인다.

A hand holds the tie knot below an open collar, leaving a visible gap at the neck.

- 소유자/관계: A.hand → holds → tie.knot; tie.knot → below → shirt.collar
- 관찰 gate: 매듭과 칼라 분리; 접촉하는 손
- 혼동 경계: 이미 옷을 벗었다는 시간; 친밀한 의도
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: hand_pose, contact_point
- 근거군: S16, S08; Draft semantic review required

## esp_pocket_hand — 주머니에 들어간 손

팔뚝이 코트 주머니 입구까지 이어지고 손 일부는 주머니에 들어가 있다.

A forearm leads into a coat pocket opening with the hand partly enclosed by the pocket.

- 소유자/관계: A.forearm → continues_into → pocket; pocket → partly_encloses → A.hand
- 관찰 gate: 팔과 입구의 연결; 포켓 경계
- 혼동 경계: 손 절단; 숨긴 무기 추정
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: hand_pose, contact_point
- 근거군: S16, S08; Draft semantic review required

## esp_folded_arms — 가슴 앞에서 교차한 팔

같은 사람 가슴 앞에서 팔뚝 두 개가 교차하고 각 팔꿈치가 어깨로 이어진다.

Two forearms cross in front of the same person's chest with each elbow traceable to its shoulder.

- 소유자/관계: A.forearm1 → crosses → A.forearm2
- 관찰 gate: 각 팔의 연결; 가슴 앞 깊이
- 혼동 경계: 소유자 뒤섞임; 방어적 태도 확정
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: body_pose
- 근거군: S16, S08; Draft semantic review required

## esp_glasses_adjustment — 안경에 닿은 손

손끝이 같은 사람 코 위에 놓인 안경의 브리지에 닿는다.

A fingertip touches the bridge of glasses resting on the same person's nose.

- 소유자/관계: A.finger → contacts → glasses.bridge; glasses → rests_on → A.nose
- 관찰 gate: 손끝과 브리지; 안경과 얼굴의 배치
- 혼동 경계: 눈 찌르기; 변장 증명
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: hand_pose, contact_point
- 근거군: S16, S08; Draft semantic review required

## esp_glove_removal — 장갑을 당기는 손

맨손가락이 다른 손을 아직 덮고 있는 장갑의 커프를 당긴다.

Bare fingers pull the cuff of a glove that still covers the other hand.

- 소유자/관계: A.hand1 → pulls → glove.cuff; glove → covers → A.hand2
- 관찰 gate: 맨손과 장갑 낀 손; 당기는 접점
- 혼동 경계: 완전히 벗은 장갑; 피부를 당김
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: hand_pose, contact_point
- 근거군: S16, S08; Draft semantic review required

## esp_glass_stem — 스템을 잡은 손

손가락이 잔 볼 아래 가는 스템을 감싸고 볼은 손바닥과 떨어져 있다.

Fingers encircle the narrow stem below a glass bowl, keeping the bowl separate from the palm.

- 소유자/관계: A.fingers → grip → glass.stem; glass.bowl → above → glass.stem
- 관찰 gate: 스템의 연속성; 손가락과 잔 소유자
- 혼동 경계: 유리 파손; 음료 내용이나 약물
- 주장 한계: Pose, direction and surface tension remain visible facts; emotion, intention, skill, trust and narrative history remain contextual.
- 제안 role: hand_pose, contact_point
- 근거군: S16, S08; Draft semantic review required

## esp_face_to_face — 마주 선 두 사람

별도의 두 몸통이 빈 간격을 두고 서로 마주한다.

Two separate torsos face each other across an unoccupied gap.

- 소유자/관계: A.torso → faces → B.torso
- 관찰 gate: 두 몸 경계; 방향과 간격
- 혼동 경계: 이미 접촉; 대립의 원인
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: body_pose
- 근거군: S08, S16, S23; Draft semantic review required

## esp_side_by_side — 나란한 두 사람

두 사람이 옆에 서서 같은 방향을 향한다.

Two people stand next to each other facing the same direction.

- 소유자/관계: A → beside → B; A.torso → parallel_to → B.torso
- 관찰 gate: 두 몸 경계; 각자의 방향
- 혼동 경계: 연인·동료 신분; 시선 방향 강제
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: body_pose
- 근거군: S08, S16, S23; Draft semantic review required

## esp_back_to_back — 등을 맞댄 두 사람

두 사람이 반대 방향을 향하고 등 윗부분이 서로 닿는다.

Two people face opposite ways with upper backs in visible contact.

- 소유자/관계: A.upper_back → contacts → B.upper_back
- 관찰 gate: 등의 접점; 반대 몸 방향
- 혼동 경계: 떨어진 포스터 합성; 공동 충성
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: relational_action, contact_point
- 근거군: S08, S16, S23; Draft semantic review required

## esp_whisper_proximity — 귓가 가까운 입

한 사람 입이 상대 귀 가까이에 있고 작은 틈이 보인다.

One person's mouth is close to another person's ear with a visible gap.

- 소유자/관계: A.mouth → near → B.ear
- 관찰 gate: 입과 귀의 다른 소유자; 간격
- 혼동 경계: 입맞춤; 실제 말·동의
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: relational_action, contact_point
- 근거군: S08, S16, S23; Draft semantic review required

## esp_other_tie — 상대 타이를 정리하는 손

한 사람이 상대 칼라 아래 넥타이 매듭을 집는다.

One person pinches another person's tie knot below that person's collar.

- 소유자/관계: A.hand → pinches → B.tie.knot; B.tie.knot → below → B.collar
- 관찰 gate: 행위자의 손; 상대의 매듭
- 혼동 경계: 자기 타이; 배려나 지배
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: relational_action, contact_point
- 근거군: S08, S16, S23; Draft semantic review required

## esp_ballroom_hold — 춤의 두 접점

성인 두 사람이 한 쌍의 손을 맞잡고 다른 손은 상대 등 윗부분에 놓인다.

Two adults join one pair of hands while another hand rests on the partner's upper back.

- 소유자/관계: A.hand1 → joins → B.hand1; A.hand2 → contacts → B.upper_back
- 관찰 gate: 맞잡은 두 손; 등 접촉과 팔 연속성
- 혼동 경계: 중복 팔; 연애·비밀 거래
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: relational_action, contact_point
- 근거군: S08, S16, S23; Draft semantic review required

## esp_divergent_gazes — 가까운 몸과 다른 시선

두 사람 몸은 가깝고 각자는 서로 다른 보이는 지점을 바라본다.

Two people stand close while looking at two different visible points.

- 소유자/관계: A → near → B; A.gaze → toward → target1; B.gaze → toward → target2
- 관찰 gate: 몸 간격; 다른 두 시선 종점
- 혼동 경계: 불충·배신; 같은 대상 응시
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: body_pose, gaze_target
- 근거군: S08, S16, S23; Draft semantic review required

## esp_seated_standing — 앉고 선 높이 차이

앉은 사람이 탁자 건너 선 사람을 마주한다.

A seated person faces a standing person across a table.

- 소유자/관계: A.pelvis → supported_by → chair; B.feet → supported_by → floor
- 관찰 gate: 각자 지지면; 탁자와 높이
- 혼동 경계: 심문 확정; 직급 자동 지정
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: body_pose, gaze_target
- 근거군: S08, S16, S23; Draft semantic review required

## esp_threshold_standoff — 문을 사이에 둔 두 사람

두 사람이 출입구 반대쪽에서 서로 마주한다.

Two people face each other from opposite sides of a doorway.

- 소유자/관계: A → on_side1_of → doorframe; B → on_side2_of → doorframe; A.torso → faces → B.torso
- 관찰 gate: 문틀 경계; 인물의 반대쪽 위치
- 혼동 경계: 출구 봉쇄 성공; 이전 감금
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: body_pose
- 근거군: S08, S16, S23; Draft semantic review required

## esp_supported_walk — 다른 몸에 체중을 기대기

한 사람 팔이 동행인 어깨 위에 놓이고 동행인은 옆몸을 받친다.

One person's arm rests over a companion's shoulder while the companion supports the torso at the side.

- 소유자/관계: A.arm → over → B.shoulder; B.hand → supports → A.torso
- 관찰 gate: 어깨 접점; 몸통 받침과 발 지지
- 혼동 경계: 무관한 포옹; 부상·취함 원인
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: relational_action, contact_point
- 근거군: S08, S16, S23; Draft semantic review required

## esp_lowered_weapon — 아래로 향한 소품 무기

손이 소품 권총을 들고 총구는 상대와 떨어져 바닥을 향한다.

A hand holds a prop pistol with its muzzle pointing toward the ground away from the other person.

- 소유자/관계: A.hand → holds → prop_pistol; prop_pistol.muzzle → points_toward → ground
- 관찰 gate: 손과 소품; 총구 방향
- 혼동 경계: 발포; 항복이나 안전 증명
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: hand_pose, prop_placement
- 근거군: S08, S16, S23; Draft semantic review required

## esp_raised_hands — 들어 보인 두 손

양손이 어깨 위로 올라가 손바닥이 보이고 팔뚝이 같은 몸으로 이어진다.

Both hands rise above the shoulders with palms visible and forearms traceable to the same body.

- 소유자/관계: A.hand1 → above → A.shoulder1; A.hand2 → above → A.shoulder2
- 관찰 gate: 두 손의 팔 연결; 손바닥
- 혼동 경계: 항복 의도; 비무장 보장
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: body_pose
- 근거군: S08, S16, S23; Draft semantic review required

## esp_restrained_seated — 연결된 수갑과 앉은 몸

앉은 성인 손목의 수갑 두 개가 몸 앞에서 짧은 사슬로 연결된다.

A seated adult's wrists sit inside two cuffs linked by a short chain in front of the body.

- 소유자/관계: cuff1 → encircles → A.wrist1; cuff2 → encircles → A.wrist2; chain.end1 → attached_to → cuff1; chain.end2 → attached_to → cuff2
- 관찰 gate: 두 손목 소유자; 수갑-사슬 양 끝
- 혼동 경계: 고문·성적 상황 자동 부여; 시야 밖 결박
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: body_pose, contact_point
- 근거군: S08, S16, S23; Draft semantic review required

## esp_head_lowered — 숙인 고개와 지지된 몸

앉은 인물 고개가 앞으로 내려가고 팔뚝은 허벅지 위에 놓인다.

A seated person's head drops forward while the forearms rest on the thighs.

- 소유자/관계: A.head → inclines_toward → A.chest; A.forearms → rests_on → A.thighs
- 관찰 gate: 목 연결; 팔 지지
- 혼동 경계: 사망·고문 이후; 감정 확정
- 주장 한계: Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.
- 제안 role: body_pose
- 근거군: S08, S16, S23; Draft semantic review required

## esp_three_piece — 별도 조끼가 있는 스리피스

열린 재킷 안쪽 별도 단추 조끼와 그 아래 어울리는 바지가 보인다.

A separate buttoned waistcoat sits beneath an open jacket above matching trousers.

- 소유자/관계: waistcoat → beneath → jacket; waistcoat → above → trousers
- 관찰 gate: 조끼 가장자리; 의복 층 구분
- 혼동 경계: 전술 베스트; 붙은 가짜 앞판
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: wardrobe_layering, garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_single_breasted — 한 줄 단추 여밈

재킷이 한 줄 세로 단추와 좁은 앞판 겹침으로 여며진다.

A jacket closes with one visible vertical row of buttons and a narrow front overlap.

- 소유자/관계: front1 → overlaps → front2; buttons → aligned_on → front1
- 관찰 gate: 한 줄 배열; 앞판 겹침
- 혼동 경계: 단추가 반드시 하나; 열린 재킷 판정
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_double_breasted — 두 줄 단추와 넓은 겹침

넓게 겹친 재킷 앞판에 단추 두 줄이 놓인다.

Two button columns flank a broad overlapping jacket front.

- 소유자/관계: button_col1 → beside → button_col2; front1 → broadly_overlaps → front2
- 관찰 gate: 두 단추 열; 앞판 겹침
- 혼동 경계: 피코트로 한정; 단추로 계급 추정
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_notch_lapel — 홈이 파인 라펠

칼라와 접힌 라펠이 V자 홈을 사이에 두고 만난다.

The collar and folded lapel meet at a visible V-shaped notch.

- 소유자/관계: collar → meets_at_notch → lapel
- 관찰 gate: 칼라 접합부; 홈의 열린 각
- 혼동 경계: 재킷 앞 V 전체; 피크드 끝
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_peak_lapel — 위로 솟은 라펠 끝

접힌 라펠 끝이 칼라 옆에서 위로 뾰족하게 솟는다.

The folded lapel ends in an upward-pointing tip beside the collar.

- 소유자/관계: lapel.tip → points_above → collar.junction
- 관찰 gate: 끝 방향; 칼라 접합부
- 혼동 경계: 노치 홈; 견장
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_shawl_lapel — 연속된 숄 라펠

둥근 라펠 가장자리가 재킷 여밈 주변으로 연속해서 이어진다.

A rounded lapel edge curves continuously around the jacket opening.

- 소유자/관계: lapel.edge → continuous_around → jacket.opening
- 관찰 gate: 둥근 선의 연속; 접합부
- 혼동 경계: 별도 숄; 피크드 끝
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_structured_shoulder — 각을 잡은 어깨

재킷 어깨선이 단단한 모서리를 이루고 소매로 내려간다.

The jacket shoulder line forms a firm edge before turning into the sleeve.

- 소유자/관계: jacket.shoulder → joins → jacket.sleeve
- 관찰 gate: 어깨-소매 전환; 의복 외곽
- 혼동 경계: 패드 재료 확정; 인물의 타고난 어깨
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail, garment_fit
- 근거군: S11, S18, S24; Draft semantic review required

## esp_tuxedo_facing — 별도 마감의 디너 재킷

매끈한 마감이 디너 재킷 라펠을 덮고 몸판 천과 대비된다.

Smooth facing covers the dinner jacket lapels and contrasts with the body cloth.

- 소유자/관계: facing → covers → lapel; facing → different_from → jacket.body_cloth
- 관찰 gate: 라펠과 몸판; 표면 차이
- 혼동 경계: 검정 수트면 모두 턱시도; 브랜드 복제
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: wardrobe_style, garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_ivory_dinner — 아이보리 재킷과 어두운 바지

아이보리 디너 재킷 아래 별도 어두운 바지가 보인다.

An ivory dinner jacket sits above separate dark trousers.

- 소유자/관계: ivory_jacket → above → dark_trousers
- 관찰 gate: 두 의복; 명도 차이
- 혼동 경계: 전체 흰 수트; 특정 인물
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: wardrobe_style, garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_bow_tie — 매듭과 두 날개

셔츠 칼라의 보타이에 가운데 매듭과 접힌 날개 둘이 보인다.

A tied bow has a central knot and two folded wings at the shirt collar.

- 소유자/관계: bow.knot → between → bow.wings; bow → at → shirt.collar
- 관찰 gate: 매듭과 날개; 목 위치
- 혼동 경계: 일반 리본; 성별·직업
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_cummerbund — 허리의 주름 밴드

수평 주름 밴드가 셔츠와 바지 사이 허리를 감싼다.

A horizontal pleated band wraps the waist between shirt and trousers.

- 소유자/관계: band → below → shirt; band → above → trousers; band → encircles → waist
- 관찰 gate: 별도 밴드; 주름과 허리
- 혼동 경계: 벨트; 코르셋
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_trench_assembly — 벨트와 플랩이 있는 트렌치

트렌치코트 견장과 겹친 가슴 플랩, 허리 고리를 지나는 벨트가 보인다.

A trench coat shows epaulettes, an overlapping chest flap and a belt passing through waist loops.

- 소유자/관계: epaulettes → attached_to → coat.shoulders; belt → passes_through → coat.loops
- 관찰 gate: 견장 부착; 플랩 층; 벨트-고리 연결
- 혼동 경계: 모든 긴 레인코트; 모든 트렌치의 필수 역사형
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: wardrobe_style, garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_plain_raincoat — 장식이 적은 레인코트

긴 레인코트에 매끈한 앞여밈과 장식이 적은 어깨 면이 보인다.

A long raincoat has a smooth front placket and an unadorned shoulder area.

- 소유자/관계: placket → part_of → coat.front
- 관찰 gate: 앞판과 여밈; 긴 외곽
- 혼동 경계: 방수 성능; 견장 자동 부착
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_pea_coat — 짧은 겹여밈 외투

짧은 외투가 허벅지 위에서 끝나고 넓은 라펠과 단추 두 줄이 보인다.

A short coat ends at the upper thighs with broad lapels and two button columns.

- 소유자/관계: coat.hem → near → A.upper_thigh; buttons → on → coat.front
- 관찰 gate: 길이; 라펠과 여밈
- 혼동 경계: 긴 오버코트; 해군 직업
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_turtleneck — 목을 감싸 접힌 니트

니트 칼라가 목을 감싸 올라와 바깥으로 접힌다.

A knitted collar rises around the neck and folds back over itself.

- 소유자/관계: collar → encircles → A.neck; collar.edge → folds_over → collar.body
- 관찰 gate: 목과 천 경계; 접힘
- 혼동 경계: 스탠드 칼라; 검정색 의무
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_open_cardigan — 앞이 열린 카디건

니트 앞 가장자리 둘 사이로 별도 안쪽 셔츠가 보인다.

Two knitted front edges frame a separate shirt underneath.

- 소유자/관계: cardigan.edges → frame → shirt
- 관찰 gate: 별도 두 의복; 열린 앞면
- 혼동 경계: 재킷 라펠; 분석관 신분
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_field_pockets — 플랩 주머니 야전형 재킷

골반 길이 재킷 가슴과 아래 앞판에 덮개 주머니들이 달린다.

A hip-length jacket has flap pockets on the chest and lower front.

- 소유자/관계: pockets → attached_to → jacket.front
- 관찰 gate: 주머니 몸체와 플랩; 재킷 경계
- 혼동 경계: 군 소속; 방탄 성능
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_bomber_cuffs — 허리와 손목의 시보리

짧은 재킷이 손목과 허리 골지 밴드로 모인다.

A short jacket gathers into ribbed bands at the wrists and waist.

- 소유자/관계: sleeve → gathers_into → cuff; body → gathers_into → waistband
- 관찰 gate: 손목 밴드; 허리 밴드
- 혼동 경계: 비행 자격; 패딩 의무
- 주장 한계: Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.
- 제안 role: garment_detail
- 근거군: S11, S18, S24; Draft semantic review required

## esp_slip_dress — 슬립형 외출 드레스

가는 어깨끈이 단순한 외출 드레스 몸판을 받친다.

Thin shoulder straps support a simple outer dress body.

- 소유자/관계: straps → support → dress.bodice; straps → over → A.shoulders
- 관찰 gate: 어깨끈 연결; 외출 의복 경계
- 혼동 경계: 속옷 자동 판정; 새틴·실크 의무
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_bias_drape — 몸을 따라 흐르는 드레이프

대각 주름이 드레스 허리에서 골반을 따라 내려온다.

Diagonal folds fall from the dress waist across the hips.

- 소유자/관계: folds → run_across → skirt; skirt → falls_from → waist
- 관찰 gate: 주름 방향; 같은 의복 연속 표면
- 혼동 경계: 주름만으로 재단 방향 입증; 물결 무늬
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail, garment_fit
- 근거군: S09, S12, S13, S23, S25; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_halter_support — 목 뒤로 이어지는 홀터

몸판 끝이 목 뒤 밴드로 올라가고 어깨 바깥은 드러난다.

Bodice edges rise to a band behind the neck leaving the outer shoulders uncovered.

- 소유자/관계: bodice.edges → join → neckband; neckband → behind → A.neck
- 관찰 gate: 몸판-밴드 연결; 어깨와 끈 경계
- 혼동 경계: 일반 어깨끈; 노출 의도
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_backless_boundary — 등의 열린 의복 경계

등의 열린 면이 목 여밈과 아래 드레스 허리 가장자리 사이에 있다.

The back opening lies between a neck fastening and a lower dress waist edge.

- 소유자/관계: neck_fastening → above → back_opening; waist_edge → below → back_opening
- 관찰 gate: 같은 사람의 등; 의복 양 경계
- 혼동 경계: 앞 가슴 파임; 투명 패널
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_slit_edge — 치마 트임의 두 끝

마감된 치마 가장자리 둘이 갈라져 같은 착용자의 한 다리 일부가 보인다.

Two finished skirt edges separate beside one leg, revealing a wedge of the same wearer's leg.

- 소유자/관계: skirt.edge1 → separated_from → skirt.edge2; opening → reveals → A.leg
- 관찰 gate: 마감된 양 끝; 다리 소유자
- 혼동 경계: 찢긴 천; 추가 다리
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_off_shoulder — 어깨 아래 네크라인

네크라인이 양 어깨점 아래에 놓이고 소매는 위팔에서 시작한다.

The neckline lies below both shoulder points while sleeves start around the upper arms.

- 소유자/관계: neckline → below → A.shoulder_points; sleeves → around → A.upper_arms
- 관찰 gate: 어깨와 네크라인; 소매 시작점
- 혼동 경계: 모든 끈 없는 드레스; 벗는 중
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_sheer_layer — 비치는 천과 아래층

경계가 있는 얇은 천 너머로 별도 불투명 안감 윤곽이 보인다.

A bounded thin fabric layer reveals the outline of an opaque lining beneath it.

- 소유자/관계: sheer_layer → over → lining; lining → visible_through → sheer_layer
- 관찰 gate: 천 끝과 안감; 층 구분
- 혼동 경계: 피부 노출 자동 부여; 섬유 확정
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: wardrobe_layering, garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_illusion_panel — 망사 패널의 경계

미세 망사가 네크라인 개구를 잇고 솔기가 불투명 드레스 판과 연결한다.

Fine mesh spans a neckline opening with seams joining it to opaque dress panels.

- 소유자/관계: mesh → spans → neckline.opening; seam.side1 → joins → mesh; seam.side2 → joins → dress
- 관찰 gate: 망사 조직; 양 끝 솔기
- 혼동 경계: 빈 개구; 피부 자체
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_corset_structure — 패널과 보닝 통로

몸통에 맞는 의복에 수직 통로와 끈 여밈이 보인다.

A fitted torso garment shows vertical channels and a laced closure.

- 소유자/관계: channels → run_along → garment.panels; lacing → bridges → garment.edges
- 관찰 gate: 수직 구조; 끈과 양쪽 가장자리
- 혼동 경계: 모든 뷔스티에 의무 구조; 고통
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_stocking_support — 스타킹을 잇는 스트랩

성인 착용자 허리 벨트에서 내려온 스트랩이 스타킹 윗끝에 연결된다.

A strap descends from an adult wearer's waist belt and clips to a stocking top.

- 소유자/관계: strap → connects → waistbelt; clip.upper → attached_to → strap; clip.lower → attached_to → stocking
- 관찰 gate: 벨트-스트랩-클립-스타킹 경로; 같은 소유자
- 혼동 경계: 바지 서스펜더; 떠 있는 클립
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_stocking_seam — 스타킹 뒤쪽 세로선

한 다리를 덮는 스타킹 뒤쪽 표면을 따라 가는 선이 내려간다.

A narrow line runs down the rear surface of a stocking covering one leg.

- 소유자/관계: stocking → covers → A.leg; line → on → stocking.rear
- 관찰 gate: 다리와 천 경계; 뒤쪽 선 경로
- 혼동 경계: 실제 봉제 확정; 문신
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_opera_gloves — 팔꿈치 위 긴 장갑

한 장갑이 손과 팔뚝을 연속해서 덮고 팔꿈치 위에서 끝난다.

A continuous glove covers hand and forearm and ends above the elbow.

- 소유자/관계: glove → covers → A.hand; glove → covers → A.forearm; glove.edge → above → A.elbow
- 관찰 gate: 손부터 팔까지 천; 끝단과 팔꿈치
- 혼동 경계: 긴 소매; 분리된 팔
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_chest_rig — 수납 패널과 스트랩

파우치 달린 얕은 패널이 몸통을 도는 어깨 스트랩에 매달린다.

A shallow pouch panel hangs from shoulder straps that continue around the torso.

- 소유자/관계: pouches → attached_to → panel; straps → support → panel
- 관찰 gate: 패널과 파우치; 스트랩 경로
- 혼동 경계: 방탄판 존재; 모든 전술 베스트
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: wearable_accessory
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_plate_carrier — 판 수납 외피

몸통 캐리어에 넓은 직사각 앞 포켓과 그 위 여밈 가장자리가 보인다.

A torso carrier shows a broad rectangular front pocket with a closure edge above it.

- 소유자/관계: front_pocket → part_of → carrier; closure → above → front_pocket
- 관찰 gate: 외피와 포켓; 여밈 경계
- 혼동 경계: 방탄판 실제 존재; 방호 성능
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: wearable_accessory
- 근거군: S09, S12, S13, S23, S25; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_catsuit — 밀착된 긴 일체형

밀착 일체형 의복이 몸통에서 양쪽 긴 다리로 이어진다.

A fitted one-piece garment continues from the torso into both full-length legs.

- 소유자/관계: garment.torso → continues_into → garment.legs
- 관찰 gate: 몸통-다리 연속 천; 긴 끝단
- 혼동 경계: 보디수트와 동의어; 방호 성능
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail, garment_fit
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_bodysuit — 몸통과 다리 개구의 일체형

몸통 의복이 별도 스타킹 위 허벅지 상부 다리 개구 둘에서 끝난다.

A torso garment ends around two upper-thigh leg openings above separate stockings.

- 소유자/관계: garment.body → ends_at → leg_openings; stockings → separate_from → garment
- 관찰 gate: 몸통과 개구; 스타킹 별도 경계
- 혼동 경계: 긴 캣수트; 누드
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail, garment_fit
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_jumpsuit — 여유 있는 긴 일체복

한 의복이 셔츠 같은 몸통과 긴 바지를 잇고 골반에 여유 주름이 생긴다.

A single garment joins a shirt-like torso to full-length trouser legs with loose hip folds.

- 소유자/관계: garment.torso → joins → garment.trouser_legs
- 관찰 gate: 허리 연속성; 여유 주름
- 혼동 경계: 항상 밀착형; 잠입 기능
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: garment_detail, garment_fit
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_fashion_harness — 장식 하네스의 연결

장식 스트랩들이 의복 위를 지나 앞쪽 링에서 만난다.

Decorative straps cross over a garment and meet at a front ring.

- 소유자/관계: straps → over → garment; straps → join_at → ring
- 관찰 gate: 스트랩과 링; 별도 의복 층
- 혼동 경계: 홀스터·안전 하네스 성능; 성행위
- 주장 한계: Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.
- 제안 role: wearable_accessory
- 근거군: S09, S12, S13, S23, S25; Draft semantic review required

## esp_oxford_closure — 옥스퍼드의 닫힌 끈 구조

구두 아일렛 판이 뱀프 아래에서 연결되어 좁은 닫힌 끈 개구가 보인다.

The shoe's eyelet facings join beneath the vamp, leaving a narrow closed lacing opening.

- 소유자/관계: facings → joined_beneath → vamp
- 관찰 gate: 아일렛 판 부착; 뱀프 경계
- 혼동 경계: 토 장식으로 구별; 더비와 동의어
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: footwear, garment_detail
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_derby_closure — 더비의 열린 끈 구조

아일렛 판 둘이 구두 뱀프 위에 놓이고 사이 간격이 보인다.

Two eyelet facings sit on top of the shoe vamp with a visible gap between them.

- 소유자/관계: facings → stitched_above → vamp
- 관찰 gate: 판의 상하 층; 사이 간격
- 혼동 경계: 옥스퍼드; 브로그 무늬
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: footwear, garment_detail
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_cufflink_bridge — 커프를 잇는 커프링크스

작은 잠금 장식이 손목의 접힌 커프 가장자리 둘을 잇는다.

A small fastener bridges two folded cuff edges at the wrist.

- 소유자/관계: fastener → bridges → cuff.edges; cuff → around → A.wrist
- 관찰 gate: 양 커프 끝; 잠금 장식 연결
- 혼동 경계: 재킷 단추; 허공 장식
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: wearable_accessory
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_tie_bar_anchor — 타이 바의 위치

수평 금속 바가 넥타이를 가로지르고 한쪽 끝이 아래 셔츠 여밈에 닿는다.

A horizontal metal bar crosses the tie with one end meeting the shirt placket beneath.

- 소유자/관계: bar → crosses → tie; bar.end → meets → shirt.placket
- 관찰 gate: 타이와 셔츠의 별도 층; 바의 위치
- 혼동 경계: 검증되지 않은 숨은 클립; 장식만으로 고정 성능
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: wearable_accessory
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_ring_on_finger — 손가락의 밴드 반지

장식 적은 가는 밴드 반지가 한 손의 특정 손가락을 감싼다.

A plain narrow band encircles a specified finger on one hand.

- 소유자/관계: band → encircles → A.finger
- 관찰 gate: 반지와 손가락 경계; 손의 소유자
- 혼동 경계: 법적 혼인; 충성이나 위장 관계
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: wearable_accessory
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_lanyard_card — 목걸이 끈과 출입증

목걸이 고리에서 내려온 끈의 클립이 가슴 앞 출입증 카드에 연결된다.

A neck loop descends to a clip attached to a bounded ID card on the chest.

- 소유자/관계: lanyard → around → A.neck; clip.upper → attached_to → lanyard; clip.lower → attached_to → card
- 관찰 gate: 목-끈-클립-카드 경로; 카드 경계
- 혼동 경계: 보안 인가; 진짜 이름이나 소속
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: wearable_accessory
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_shoulder_holster — 어깨 스트랩과 홀스터

스트랩이 어깨를 지나 갈비 옆 별도 홀스터로 내려간다.

A strap crosses the shoulder and descends to a separate holster beside the ribs.

- 소유자/관계: strap → over → A.shoulder; strap → connects → holster; holster → beside → A.ribs
- 관찰 gate: 어깨에서 집까지 경로; 몸과 집 경계
- 혼동 경계: 패션 하네스; 무기 숨김 또는 사용
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: wearable_accessory
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_crossbody_bag — 몸을 가로지른 가방 끈

가방 끈 하나가 어깨에서 몸통을 지나 반대 골반의 가방으로 이어진다.

One bag strap crosses the torso from a shoulder to a bag resting at the opposite hip.

- 소유자/관계: strap → crosses → A.torso; strap → connects → bag; bag → at → A.opposite_hip
- 관찰 gate: 끈의 양 끝; 가방과 몸 경계
- 혼동 경계: 끊긴 스트랩; 운반 내용
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: wearable_accessory
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_glossy_folds — 천 주름의 넓은 하이라이트

넓고 부드러운 하이라이트가 매끈한 한 천 판의 굽은 주름을 따른다.

Broad soft highlights follow the curved folds of one smooth fabric panel.

- 소유자/관계: highlights → follow → fabric.folds
- 관찰 gate: 같은 천의 주름과 빛; 넓은 반사 띠
- 혼동 경계: 실크 섬유 확정; PVC·라텍스와 동의어
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: surface_material, texture
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_velvet_pile — 짧은 파일과 방향 명암

천 표면에 짧고 부드러운 파일이 있고 이웃한 주름 방향마다 명암 패치가 달라진다.

A fabric surface shows a short soft pile whose light-dark patches change across adjacent fold directions.

- 소유자/관계: pile → on → fabric.surface; patches → follow → fold_directions
- 관찰 gate: 파일이 보이는 크기; 서로 다른 주름 방향
- 혼동 경계: 색무늬; 벨벳 섬유 조성
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: surface_material, texture
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_patent_reflection — 가죽형 표면의 선명 반사

구두 갑피의 매끈한 코팅 표면에 선명한 빛 반사가 걸린다.

A shoe upper carries a sharp light reflection across a smooth coated surface.

- 소유자/관계: reflection → on → shoe.upper
- 관찰 gate: 갑피 외곽; 표면 반사
- 혼동 경계: 실제 가죽 판정; 젖은 표면으로 고정
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: surface_material, texture
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_ripstop_grid — 보강 격자의 표면

가는 굵은 보강 실들이 천 판 위에 반복 사각 격자를 만든다.

Fine thicker threads form a repeating square grid across a fabric panel.

- 소유자/관계: reinforcement_threads → cross_over → fabric.ground
- 관찰 gate: 바탕 천과 굵은 실; 격자 반복
- 혼동 경계: 찢김 방지 성능; 체크 인쇄
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: surface_pattern
- 근거군: S07, S09, S14, S15, S17; HOLD exact specimen/material/function equivalence; plate/detail review required

## esp_pinstripe — 가는 세로줄

가는 평행 밝은 줄이 어두운 재킷 판을 세로로 지난다.

Fine parallel light stripes run down one dark jacket panel.

- 소유자/관계: stripes → run_down → jacket.panel
- 관찰 gate: 가는 선과 바탕; 같은 판의 방향
- 혼동 경계: 헤링본; 인물 키 확정
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: surface_pattern
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_herringbone — 방향을 번갈아 꺾는 조직

짧은 사선 골이 방향을 번갈아 꺾어 한 천에 V자 열을 반복한다.

Short diagonal ribs alternate direction in repeated V-shaped rows across one fabric.

- 소유자/관계: diagonal_ribs → alternate_across → fabric
- 관찰 gate: 반복 V; 직물 표면에 고정
- 혼동 경계: 핀스트라이프; 섬유 조성
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: surface_pattern
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_slickback — 뒤로 정돈된 머리

머리카락이 드러난 이마에서 정수리 쪽으로 연속해서 뒤로 넘어간다.

Hair strands sweep back from an exposed forehead toward the crown in one continuous direction.

- 소유자/관계: hair.strands → sweep_from → A.forehead
- 관찰 gate: 이마 경계; 뒤로 향한 흐름
- 혼동 경계: 젖었다는 원인; 악역의 신분
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: hair_style
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_blunt_bob — 수평 끝선 단발

단발이 턱 옆에서 비교적 곧고 무딘 끝선으로 끝난다.

A bob ends in a relatively straight blunt edge beside the jaw.

- 소유자/관계: hair.edge → beside → A.jaw
- 관찰 gate: 머리 끝선; 턱과 길이 관계
- 혼동 경계: 픽시 컷; 가발 판정
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: hair_style
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_finger_waves — 머리 표면의 연속 S굴곡

촘촘한 머리 능선이 머리 옆 표면에 번갈아 S자 굴곡을 만든다.

Close-set hair ridges form alternating S-shaped waves along the side of the head.

- 소유자/관계: hair.ridges → run_along → A.head.side
- 관찰 gate: 표면 능선; 연속 굴곡
- 혼동 경계: 느슨한 컬; 정확한 시대
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: hair_style
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_chignon — 뒤쪽에 모은 머리 매듭

머리카락이 머리 뒤쪽의 작은 말린 매듭으로 모인다.

Hair gathers into a compact rolled knot at the back of the head.

- 소유자/관계: hair → gathers_into → knot; knot → at → A.head.back
- 관찰 gate: 머리에서 매듭의 연속; 뒤쪽 위치
- 혼동 경계: 포니테일; 가발 접합
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: hair_style
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_stubble — 피부 위 짧은 수염

턱과 아래 볼 피부에서 짧게 나뉜 수염이 올라온다.

Short separated hairs project from the chin and lower cheek skin.

- 소유자/관계: short_hairs → project_from → A.chin_skin
- 관찰 gate: 털과 피부 경계; 짧은 길이
- 혼동 경계: 면도한 날짜; 장기 임무
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: facial_hair
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_winged_liner — 눈 바깥으로 뻗는 선

어두운 선이 윗속눈썹 가장자리를 따라 눈 바깥꼬리 너머로 뻗는다.

A dark line follows the upper lash edge and extends beyond the outer eye corner.

- 소유자/관계: liner → follows → A.upper_lash_edge; liner.tip → beyond → A.outer_eye_corner
- 관찰 gate: 눈과 선의 경계; 바깥 연장
- 혼동 경계: 해부학적 눈매; 인종이나 의도
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: eye_makeup_line
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_smoky_gradient — 눈가의 번진 색 경계

눈꺼풀 주변 색이 속눈썹 선 바깥으로 부드럽게 옅어진다.

Pigment around the eyelid fades into a soft graded edge beyond the lash line.

- 소유자/관계: pigment → on → A.eyelid; gradient → extends_from → lash_line
- 관찰 gate: 눈가 색; 점진 경계
- 혼동 경계: 멍; 검정색 고정
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: makeup_style
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_bold_lip — 선명한 입술색

선명한 입술색이 같은 얼굴의 보이는 입술 윤곽을 따른다.

A saturated lip color follows the visible lip contour on the same face.

- 소유자/관계: pigment → follows → A.lip_contour
- 관찰 gate: 입술 경계; 주변 피부와 대비
- 혼동 경계: 성격·성적 동의; 붉은색 고정
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: lip_color_placement
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_wig_boundary — 가발 제작물의 경계

별도 헤어피스가 인물 머리 옆 받침에 놓여 안쪽 캡이 보인다.

A separate hairpiece rests beside a person's head on a stand, with its inner cap visible.

- 소유자/관계: hairpiece.cap → inside → hairpiece; hairpiece → supported_by → stand
- 관찰 gate: 별도 제작물; 안쪽 캡
- 혼동 경계: 착용 머리는 모두 가발; 신원 변경 성공
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: prop_state
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_prosthetic_edge — 부착 분장 조각

작업대의 형태 있는 분장 조각에 얇은 가장자리가 보이고 옆에 피부색 안료 병이 놓인다.

A shaped makeup piece on a worktable shows a thin edge beside skin-tone pigment jars.

- 소유자/관계: piece.edge → part_of → piece; piece → rests_on → worktable
- 관찰 gate: 별도 조각과 얇은 끝; 작업대 경계
- 혼동 경계: 실제 상해; 안료만으로 입체 변화
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: prop_state
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_smudged_makeup — 화장 표면의 번짐

어두운 색소가 한 눈 아래 피부에서 불규칙한 줄로 번진다.

Dark pigment extends below one eye in uneven streaks on the skin.

- 소유자/관계: pigment.streaks → below → A.eye
- 관찰 gate: 색소와 피부; 국소 줄
- 혼동 경계: 눈물·폭력의 원인; 상처
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: makeup_wear_state
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_wrinkled_suit — 옷 표면의 구김

재킷 팔꿈치와 허리에 불규칙 구김이 모이고 천 표면은 끊어지지 않는다.

Irregular creases gather at the jacket elbow and waist without breaking the fabric surface.

- 소유자/관계: creases1 → at → jacket.elbow; creases2 → at → jacket.waist
- 관찰 gate: 구김 위치; 천의 연속성
- 혼동 경계: 찢김; 임무 시간
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: garment_state
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_torn_edge — 천의 찢긴 경계

소매의 불규칙 개구 양쪽에 갈라진 올풀림 실이 보인다.

An irregular opening in a sleeve has separated frayed threads along both edges.

- 소유자/관계: threads → project_from → sleeve.torn_edges
- 관찰 gate: 찢긴 양 끝; 천과 피부 구별
- 혼동 경계: 마감된 슬릿; 상해 원인
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: garment_state
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_wet_patch — 국소 젖은 듯한 표면

코트의 어두운 불규칙 패치가 주변 마른 듯한 천과 광택이 다르다.

A darker irregular patch on a coat changes sheen relative to the adjacent dry-looking cloth.

- 소유자/관계: patch → on → coat.surface; patch → differs_from → adjacent_cloth
- 관찰 gate: 같은 천의 국소 변화; 명도와 광택
- 혼동 경계: 물 종류·피; 비를 맞은 이력
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: surface_moisture
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required

## esp_surface_abrasion — 피부의 국소 거친 자국

작은 불규칙 붉은 패치가 이어진 볼 피부의 일부에 보인다.

A small irregular reddish patch interrupts otherwise continuous cheek skin.

- 소유자/관계: patch → on → A.cheek_skin
- 관찰 gate: 국소 표면 변화; 피부 소유자
- 혼동 경계: 고문 증거; 의학적 진단·원인
- 주장 한계: Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.
- 제안 role: texture
- 근거군: S07, S09, S14, S15, S17; Draft semantic review required
