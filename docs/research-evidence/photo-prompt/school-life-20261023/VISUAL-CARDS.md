# 의미 카드와 선택적 실현

이 문서의 구도·소유 그래프·한영 문장은 연구자가 저술한 제안이다. source_ids는 주제·혼동 경계의 근거이며 모든 배치의 실물 고증을 증명하지 않는다.
visible은 제안한 성분의 가시성, proxy는 비가시 개념의 선택적 대리 장면이다. proxy가 그 원개념을 증명하지 않는다.

## S01 홈룸 교실 배치

- 분류/우선순위: `visible` / P0
- 원 항목: 76, 199, 206
- 근거 범위: S01, S04
- EN 제안: Rows of individual desks face the board at the front, with a continuous side aisle between the desks and the classroom windows.
- KO 제안: 개별 책상 열이 교실 앞 칠판을 향하고 책상과 창문 사이에 옆 통로가 이어진다.
- 소유/관계: desks → face → board; aisle → between_endpoint_A → desks; aisle → between_endpoint_B → windows
- 혼동 경계: 강의실·학원·회사 교육실과 동일 판정 금지; 학교급은 외형으로 확정 불가
- 원본 픽셀 gate: 칠판 방향·책상 열·창문·통로가 한 프레임에서 식별됨
- 제안 슬롯: location, object_structure; scope: school unspecified

## S02 창가 맨 뒷자리

- 분류/우선순위: `visible` / P0
- 원 항목: 77, 206
- 근거 범위: S01
- EN 제안: One occupied desk is beside the windows in the final row, with the rear wall immediately behind it and the teaching board across the room.
- KO 제안: 선택한 책상이 창가 마지막 열에 있고 바로 뒤 뒷벽과 방 건너 앞 칠판이 보인다.
- 소유/관계: desk → beside → windows; desk → in_front_of → rear_wall; desk → faces → board
- 혼동 경계: 창가라는 증거만으로 마지막 줄 PASS 금지
- 원본 픽셀 gate: 창문·뒷벽·앞 방향·동일 책상 위치 모두 보임
- 제안 슬롯: composition, prop_placement; scope: authored school scene

## S03 방송실의 작업 접점

- 분류/우선순위: `visible` / P0
- 원 항목: 78, 208
- 근거 범위: S01, S04
- EN 제안: A seated operator faces a desk microphone and mixer, with one hand on a fader and a cable visibly joining the microphone to the desk equipment.
- KO 제안: 앉은 조작자 앞에 탁상 마이크와 믹서가 있고 한 손이 페이더에 닿으며 마이크 케이블이 장비에 이어진다.
- 소유/관계: operator → touches → fader; microphone → cabled_to → mixer
- 혼동 경계: 소리·방송 송출·말 내용은 정지사진으로 확인 못함
- 원본 픽셀 gate: 손·페이더·마이크·케이블 양끝의 작업 관계
- 제안 슬롯: location, prop, contact_point; scope: authored school scene

## S04 옥상 출입 경계

- 분류/우선순위: `visible` / P0
- 원 항목: 79, 198
- 근거 범위: S01
- EN 제안: A flat school rooftop is bordered by a continuous fence, and a stairwell door opens onto the same roof surface.
- KO 제안: 평평한 학교 옥상 둘레에 연속된 울타리가 있고 계단실 문이 같은 옥상 바닥으로 열린다.
- 소유/관계: fence → bounds → roof; door → opens_onto → roof
- 혼동 경계: 옥상 자유출입·자살 장소·고백을 자동 부여하지 않음
- 원본 픽셀 gate: 옥상 바닥·계단실·출입문·가장자리 경계
- 제안 슬롯: location, space_condition; scope: fictional school rooftop

## S05 보건실과 상담 공간 분리

- 분류/우선순위: `visible` / P0
- 원 항목: 35, 80
- 근거 범위: S05, S15
- EN 제안: A screened examination bed stands beside a basic care desk while an open chair faces the desk from the visitor side.
- KO 제안: 가림막이 있는 진찰 침대 옆에 기본 처치 책상이 있고 방문자 의자가 책상 반대편을 향한다.
- 소유/관계: screen → beside → bed; visitor_chair → faces → care_desk
- 혼동 경계: 보건교사·상담교사 자격·질병·상담 비밀을 외형으로 확정하지 않음
- 원본 픽셀 gate: 침대·가림막·책상·방문자 동선 구분
- 제안 슬롯: location, prop; scope: authored health room

## S06 동아리 활동방

- 분류/우선순위: `visible` / P0
- 원 항목: 81, 121, 122
- 근거 범위: S02
- EN 제안: A shared worktable holds an unfinished club project, with the matching tools stored on a shelf beside the table.
- KO 제안: 공용 작업대 위에 미완성 동아리 작업물이 있고 그 작업에 맞는 도구가 옆 선반에 놓여 있다.
- 소유/관계: project → rests_on → table; tools → stored_on → shelf
- 혼동 경계: 빈 방에 club 태그만 붙여 동아리 활동 증명 금지
- 원본 픽셀 gate: 작업물·도구·공용 작업면의 일치
- 제안 슬롯: location, prop_placement; scope: authored club scene

## S07 음악 합주 공간

- 분류/우선순위: `visible` / P0
- 원 항목: 82, 134
- 근거 범위: S01, S02
- EN 제안: Chairs and music stands form a semicircle around a conductor stand, with wind instruments and percussion occupying distinct positions.
- KO 제안: 의자와 보면대가 지휘대 둘레 반원으로 놓이고 관악기와 타악기가 서로 다른 자리를 차지한다.
- 소유/관계: music_stands → face → conductor_stand; percussion → behind → wind_positions
- 혼동 경계: 취주악·밴드·오케스트라의 편성을 한 단어로 합치지 않음
- 원본 픽셀 gate: 악기 종류·보면대 방향·지휘 위치
- 제안 슬롯: location, prop; scope: authored music scene

## S08 과학 실습대

- 분류/우선순위: `visible` / P0
- 원 항목: 82, 172
- 근거 범위: S01, S08
- EN 제안: A laboratory bench supports a clamped glass vessel, a tray and a sink, with the clamp attached to a stable stand on that bench.
- KO 제안: 실습대 위 유리 용기가 고정대 집게로 지지되고 트레이와 싱크가 같은 작업대에 배치된다.
- 소유/관계: clamp → holds → vessel; stand → rests_on → bench; sink → within → bench
- 혼동 경계: 연기·색 액체만으로 위험실험·불법연구·감염 확정 금지
- 원본 픽셀 gate: 집게 지지·용기·작업대의 물리 연속성
- 제안 슬롯: location, object_structure; scope: authored laboratory

## S09 미술 실기 작업대

- 분류/우선순위: `visible` / P1
- 원 항목: 22, 82, 135
- 근거 범위: S01, S08
- EN 제안: An easel holds a canvas facing a still-life arrangement, and a paint-covered palette rests within the painter's reach.
- KO 제안: 이젤의 캔버스가 정물 배치를 향하고 물감 팔레트가 작업자의 손이 닿는 곳에 있다.
- 소유/관계: easel → supports → canvas; canvas → faces → still_life; palette → within_reach → painter
- 혼동 경계: 작품 수준·천재성·입시 합격은 외형에서 판정하지 않음
- 원본 픽셀 gate: 정물→캔버스 방향·지지·도구 접근
- 제안 슬롯: location, prop, action; scope: authored art class

## S10 도서관 서가와 열람석

- 분류/우선순위: `visible` / P0
- 원 항목: 83, 13, 186
- 근거 범위: S05, S22
- EN 제안: A reading table sits between shelving aisles, with open books on the table and a clear walking route along the shelves.
- KO 제안: 서가 통로 사이 열람대에 펼친 책이 놓이고 서가를 따라 걸을 수 있는 동선이 이어진다.
- 소유/관계: books → rest_on → table; aisle → runs_along → shelves
- 혼동 경계: 오래된 책만으로 비밀결사·학문 수준·저주를 확정하지 않음
- 원본 픽셀 gate: 서가·열람석·열린 책·통로의 깊이
- 제안 슬롯: location, spatial_depth; scope: library unspecified

## S11 체육관 경기 공간

- 분류/우선순위: `visible` / P0
- 원 항목: 84, 95, 103
- 근거 범위: S01, S02
- EN 제안: A marked court occupies a gym floor, with a freestanding bench outside the sideline and spectator seating beyond it.
- KO 제안: 표시선이 있는 체육관 코트 바깥에 벤치가 있고 그 뒤에 관람석이 놓인다.
- 소유/관계: bench → outside → sideline; seating → beyond → bench
- 혼동 경계: 체육관=프롬·경기 진행·헤이징으로 자동 의미 확장 금지
- 원본 픽셀 gate: 코트 경계·벤치·관람석이 서로 분리됨
- 제안 슬롯: location, object_structure; scope: authored gym

## S12 실제 기숙 생활 공간

- 분류/우선순위: `visible` / P0
- 원 항목: 18, 40, 85
- 근거 범위: S05, S06
- EN 제안: A bed and personal study desk share one residential room, with everyday belongings occupying the desk and bedside storage.
- KO 제안: 생활실 안에 침대와 개인 책상이 함께 있고 일상 소지품이 책상과 침대 옆 수납에 놓인다.
- 소유/관계: bed → shares_room_with → desk; belongings → stored_at → bedside
- 혼동 경계: 기숙사=다인실·영국 고성·억압적 사감이라는 등식 금지
- 원본 픽셀 gate: 숙면·학습·생활 수납의 공존; 학교 소속은 문맥
- 제안 슬롯: location, prop_placement; scope: boarding variants optional

## S13 하우스 공용 휴게실

- 분류/우선순위: `visible` / P0
- 원 항목: 19, 85, 36
- 근거 범위: S05, S06
- EN 제안: Communal seating faces a shared noticeboard in a house common room, with a small study table beside the seating.
- KO 제안: 하우스 공용실의 좌석들이 공동 게시판을 향하고 옆에 작은 학습용 테이블이 있다.
- 소유/관계: seating → faces → noticeboard; study_table → beside → seating
- 혼동 경계: 문장 속 house를 건물 주택/기숙 소속/마법 기숙사와 구분
- 원본 픽셀 gate: 공용 좌석·게시판·학습 공간; 소속 제도는 별도
- 제안 슬롯: location, prop; scope: one possible house common room

## S14 구교사와 통행 제한

- 분류/우선순위: `visible` / P1
- 원 항목: 86, 182, 192
- 근거 범위: S23
- EN 제안: A worn classroom corridor ends at a closed door, with a visible temporary barrier crossing the approach before the door.
- KO 제안: 낡은 교실 복도 끝 닫힌 문 앞의 접근로를 임시 차단물이 가로지른다.
- 소유/관계: barrier → crosses → approach; approach → leads_to → door
- 혼동 경계: 낡음=폐교·금지·유령의 증거 아님; 차단물의 현재 위치만 확인
- 원본 픽셀 gate: 손상 표면과 실제 통행 차단을 별도 확인
- 제안 슬롯: space_condition, location; scope: authored fiction

## S15 실내화 교체 구역

- 분류/우선순위: `visible` / P0
- 원 항목: 87, 198
- 근거 범위: S01
- EN 제안: A low entrance step separates outdoor shoes on the lower floor from indoor shoes beside open cubbies above the step.
- KO 제안: 낮은 현관 턱 아래 바닥의 실외화와 턱 위 열린 칸 옆 실내화가 구분된다.
- 소유/관계: step → separates → outdoor_indoor_floors; outdoor_shoes → on → lower_floor; indoor_shoes → beside → cubbies
- 혼동 경계: 모든 나라의 학교에 실내화·신발장 강제 금지
- 원본 픽셀 gate: 바닥 경계·두 종류 신발·수납 접점
- 제안 슬롯: location, footwear, prop_placement; scope: JP-inspired selected convention

## S16 학교 밖 사교육 공간

- 분류/우선순위: `visible` / P1
- 원 항목: 11, 113
- 근거 범위: S07, S08
- EN 제안: A compact tutorial room has tightly arranged desks facing one teaching screen, with workbooks open at the seats.
- KO 제안: 작은 보충수업 방의 촘촘한 책상이 한 수업 화면을 향하고 각 자리에 문제집이 펼쳐져 있다.
- 소유/관계: desks → face → screen; workbooks → rest_on → desks
- 혼동 경계: 학원물=사교육학원 번역 금지; 건물만으로 영리성·주쿠·요비코 확정 불가
- 원본 픽셀 gate: 작은 수업 공간의 배치만 가시 판정
- 제안 슬롯: location, occasion_context; scope: authored after-school tutorial room

## W01 세일러 칼라 구성

- 분류/우선순위: `visible` / P0
- 원 항목: 88
- 근거 범위: S03
- EN 제안: The blouse has a broad square-backed sailor collar that continues over both shoulders to a V-shaped front opening.
- KO 제안: 블라우스의 넓고 등판이 사각인 세일러 칼라가 두 어깨를 지나 앞의 V자 여밈으로 이어진다.
- 소유/관계: collar → lies_over → shoulders; collar → frames → front_opening
- 혼동 경계: 가쿠란 입깃·블레이저 라펠·교복 코스프레 인물과 구분
- 원본 픽셀 gate: 등/앞을 동시에 볼 수 없으면 부분 판정; 선택 뷰에 맞춰 gate를 사전 한정
- 제안 슬롯: garment_detail, wardrobe_style; scope: specific garment variant

## W02 가쿠란 입깃과 단추

- 분류/우선순위: `visible` / P0
- 원 항목: 88, 138
- 근거 범위: S03
- EN 제안: A dark jacket has a short upright collar and one central row of metal buttons, with matching straight trousers.
- KO 제안: 어두운 재킷에 짧게 선 입깃과 중앙 한 줄 금속 단추가 있고 같은 천의 곧은 바지가 이어진다.
- 소유/관계: collar → stands_at → neck; buttons → run_down → jacket_front
- 혼동 경계: 입깃·단추가 불량성·폭력·남성 정체성을 증명하지 않음
- 원본 픽셀 gate: 입깃과 중앙 단추열이 라펠로 바뀌지 않음
- 제안 슬롯: garment_detail; scope: specific garment variant

## W03 블레이저 교복의 연결

- 분류/우선순위: `visible` / P0
- 원 항목: 88, 89
- 근거 범위: S03
- EN 제안: A lapelled blazer sits over a collared shirt, with a tie centered beneath the shirt collar and an emblem attached to the blazer breast.
- KO 제안: 라펠 재킷 안에 깃 셔츠가 있고 셔츠 깃 아래 중앙에 넥타이, 재킷 가슴에 교표가 부착된다.
- 소유/관계: blazer → over → shirt; tie → under → shirt_collar; emblem → attached_to → blazer_breast
- 혼동 경계: 의복 체계·교표·학교 소속을 한 가지 신원 주장으로 묶지 않음
- 원본 픽셀 gate: 레이어·깃·매듭·부착부를 같은 착용자에 연결
- 제안 슬롯: wardrobe_layering, garment_detail; scope: specific garment variant

## W04 완장의 정확한 착용자

- 분류/우선순위: `visible` / P0
- 원 항목: 26, 28, 89
- 근거 범위: S04
- EN 제안: A fabric armband encircles one upper sleeve of the selected wearer, with its fastening on that same sleeve.
- KO 제안: 천 완장이 선택한 착용자의 한쪽 위팔 소매를 두르고 잠금부도 같은 소매에 붙어 있다.
- 소유/관계: armband → encircles → selected_sleeve; fastener → attached_to → armband
- 혼동 경계: 완장만으로 풍기위원·프리펙트·권한·정당성 확정 금지
- 원본 픽셀 gate: 착용자·팔·소매·띠·잠금부가 이어짐
- 제안 슬롯: wearable_accessory, contact_point; scope: fictional insignia allowed

## W05 학생 배지와 명찰

- 분류/우선순위: `visible` / P0
- 원 항목: 25, 37, 89
- 근거 범위: S04
- EN 제안: A small badge is fastened flat to the selected person's jacket, while a separate name card hangs from a visible lanyard.
- KO 제안: 작은 배지는 선택한 인물의 재킷에 평평하게 고정되고 별도 이름표는 보이는 목줄에 매달린다.
- 소유/관계: badge → fastened_to → jacket; name_card → hangs_from → lanyard
- 혼동 경계: 숫자·이름·직책은 읽을 수 있을 때만 텍스트 증거; 명찰=학년 증거 금지
- 원본 픽셀 gate: 같은 인물 소유·고정점·두 물품 구별
- 제안 슬롯: wearable_accessory, visible_text; scope: fictional label optional

## W06 졸업앨범 속 인물의 층위

- 분류/우선순위: `visible` / P0
- 원 항목: 90, 185, 205
- 근거 범위: S01, S23
- EN 제안: An open yearbook rests on a desk, showing a grid of small printed portraits and one visibly blank cell within the grid.
- KO 제안: 책상 위 펼친 졸업앨범에 작은 인쇄 초상 격자가 있고 그 격자 안 한 칸이 비어 있다.
- 소유/관계: yearbook → rests_on → desk; portrait_grid → printed_on → page; blank_cell → inside → portrait_grid
- 혼동 경계: 인쇄 인물을 실제 인원수에 추가하지 않음; 빈칸=실종·삭제 원인 확정 금지
- 원본 픽셀 gate: 책·페이지·인쇄 격자·빈칸의 일관된 층위
- 제안 슬롯: prop, visible_text; scope: authored printed yearbook

## W07 편지 전달의 양끝

- 분류/우선순위: `visible` / P0
- 원 항목: 61, 63, 75, 98, 207
- 근거 범위: S16
- EN 제안: One person extends a sealed envelope toward another person's open hand, with the envelope still touching the giver's fingers.
- KO 제안: 한 사람이 밀봉 봉투를 다른 사람의 펼친 손 쪽으로 내밀고 봉투는 아직 건네는 손가락에 닿아 있다.
- 소유/관계: giver_fingers → touch → envelope; envelope → extends_toward → receiver_hand
- 혼동 경계: 러브레터·첫사랑·동의·짝사랑은 봉투 모양으로 확정 불가
- 원본 픽셀 gate: 두 손의 인물 소유와 봉투 위치; 융합·추가 손 실패
- 제안 슬롯: relational_action, contact_point; scope: nonsexual interpersonal scene

## W08 공유 우산의 실제 보호 범위

- 분류/우선순위: `visible` / P0
- 원 항목: 61, 65, 198, 207
- 근거 범위: S01, S16
- EN 제안: One hand grips a single umbrella shaft, and the canopy extends above two people walking side by side on a wet path.
- KO 제안: 한 손이 우산대 하나를 잡고 그 우산 천이 젖은 길을 나란히 걷는 두 사람 위로 펼쳐진다.
- 소유/관계: hand → grips → shaft; canopy → above → person_A; canopy → above → person_B
- 혼동 경계: 공유 우산=연인·소꿉친구·가난·동의로 확정하지 않음
- 원본 픽셀 gate: 한 우산·한 지지손·두 사람·우산대 연속성
- 제안 슬롯: prop, proxemics, contact_point; scope: authored rainy commute

## A01 학생회 회의의 실물 관계

- 분류/우선순위: `proxy` / P0
- 원 항목: 24, 37, 104, 175
- 근거 범위: S04
- EN 제안: Participants sit around a shared table, with one person pointing to the same agenda sheet that the others face.
- KO 제안: 참석자들이 공동 테이블을 둘러앉고 한 사람이 가리키는 안건 종이를 다른 사람들이 바라본다.
- 소유/관계: pointer → points_to → agenda; participants → face → agenda
- 혼동 경계: 회의=학생회·독재·수사·사법권 입증 아님
- 원본 픽셀 gate: 손가락→안건·참석자 방향·공유 작업면
- 제안 슬롯: action, participant_role; scope: realistic council or declared fiction

## A02 선거 투표의 한 순간

- 분류/우선순위: `visible` / P0
- 원 항목: 24, 104
- 근거 범위: S04
- EN 제안: A voter's fingers hold one paper ballot at the slot of a closed ballot box, with a short queue behind the voter.
- KO 제안: 투표자의 손가락이 닫힌 투표함 투입구에 종이 한 장을 대고 뒤에 짧은 대기줄이 있다.
- 소유/관계: fingers → hold → ballot; ballot → at → box_slot; queue → behind → voter
- 혼동 경계: 선거 공정성·후보 승리·민주주의 수준을 가시 사실로 바꾸지 않음
- 원본 픽셀 gate: 종이·손·투입구의 접점과 인원수
- 제안 슬롯: action, contact_point; scope: fictional school election

## A03 전학생 소개 장면의 대리 표현

- 분류/우선순위: `proxy` / P0
- 원 항목: 31, 32, 201
- 근거 범위: S01, S04
- EN 제안: One person stands beside the teacher's desk while the seated class faces toward that person and the front board.
- KO 제안: 한 사람이 교탁 옆에 서 있고 앉은 학급의 몸 방향이 그 사람과 앞 칠판 쪽으로 모인다.
- 소유/관계: standing_person → beside → teacher_desk; seated_class → faces → standing_person
- 혼동 경계: 전학생·복학생·방문자 신원과 과거 이력은 문맥
- 원본 픽셀 gate: 소개 대상·교탁·학급 방향만 판정
- 제안 슬롯: action, proxemics; scope: authored classroom introduction

## A04 짝꿍의 필기 공유

- 분류/우선순위: `visible` / P0
- 원 항목: 39, 108, 207
- 근거 범위: S08
- EN 제안: Two adjacent students lean toward one notebook between their desks, and one pencil tip points to a line on that page.
- KO 제안: 옆자리 두 학생이 책상 사이 공책 하나를 향하고 연필 끝 하나가 그 페이지의 한 줄을 가리킨다.
- 소유/관계: notebook → between → desks; pencil_tip → points_to → page_line; students → face → notebook
- 혼동 경계: 관계 친밀도·부정행위·학력·지능을 자동 추론하지 않음
- 원본 픽셀 gate: 공책 하나·연필 접점·각 인물의 손 소유
- 제안 슬롯: relational_action, contact_point; scope: authored shared study

## A05 급식 배식 동작

- 분류/우선순위: `visible` / P0
- 원 항목: 93
- 근거 범위: S01
- EN 제안: A server holds a ladle above one bowl on a tray while classmates wait beyond the serving table.
- KO 제안: 배식자가 쟁반 위 그릇 하나 위로 국자를 들고 다른 학생들은 배식대 건너에서 기다린다.
- 소유/관계: server_hand → holds → ladle; ladle → above → bowl; bowl → on → tray
- 혼동 경계: 급식·도시락·식당 노동·가정 식사를 구별; 봉사 강요 여부는 별도
- 원본 픽셀 gate: 국자→그릇→쟁반의 수와 지지
- 제안 슬롯: action, contact_point, prop; scope: JP example not universal

## A06 청소 당번의 도구 접점

- 분류/우선순위: `visible` / P0
- 원 항목: 93
- 근거 범위: S01
- EN 제안: One person pushes a broom whose bristles touch the classroom floor while a second person holds a dustpan at the end of the swept path.
- KO 제안: 한 사람이 빗자루 솔을 교실 바닥에 대고 밀며 다른 사람이 그 경로 끝에서 쓰레받기를 든다.
- 소유/관계: person_A → holds → broom; bristles → touch → floor; person_B → holds → dustpan
- 혼동 경계: 청소=처벌·착취·헤이징으로 자동 판정 금지
- 원본 픽셀 gate: 솔과 바닥·각 손과 도구·수거 위치
- 제안 슬롯: action, contact_point; scope: JP example not universal

## A07 문화제 준비와 완성 행사 구분

- 분류/우선순위: `visible` / P0
- 원 항목: 94, 127
- 근거 범위: S01, S04
- EN 제안: Students tape hand-painted panels to a temporary classroom booth frame, with spare panels and tools on the floor beside it.
- KO 제안: 학생들이 손으로 그린 판을 교실 안 임시 부스 틀에 테이프로 붙이고 여분 판과 도구가 옆 바닥에 놓여 있다.
- 소유/관계: hands → attach → panels; panels → on → booth_frame; tools → beside → frame
- 혼동 경계: 준비 중·영업 중·공연 중을 같은 후보에 union하지 않음
- 원본 픽셀 gate: 부착 동작·미완성 구조·예비 재료 동시 가시성
- 제안 슬롯: action, procedure_step; scope: authored cultural festival preparation

## A08 체육대회 계주 인계

- 분류/우선순위: `visible` / P0
- 원 항목: 95, 131
- 근거 범위: S01
- EN 제안: One runner extends a baton toward the next runner's open rearward hand within the marked lane.
- KO 제안: 한 주자가 표시된 레인 안에서 다음 주자의 뒤로 펼친 손을 향해 바통을 내민다.
- 소유/관계: runner_A_hand → extends → baton; baton → toward → runner_B_hand; runners → within → lane
- 혼동 경계: 전달 성공·우승·팀워크 역사는 사진 한 장으로 증명 불가
- 원본 픽셀 gate: 바통 하나·서로 다른 두 손·레인·진행 방향
- 제안 슬롯: action, contact_point, physical_motion; scope: authored sports day

## A09 졸업증서 수여 접점

- 분류/우선순위: `visible` / P0
- 원 항목: 91, 99, 200
- 근거 범위: S01, S04
- EN 제안: A presenter and recipient support opposite edges of one certificate folder above a ceremony table.
- KO 제안: 수여자와 수령자가 의식용 테이블 위 증서 폴더 하나의 서로 반대 가장자리를 잡는다.
- 소유/관계: presenter_hand → supports → folder_left; recipient_hand → supports → folder_right
- 혼동 경계: 증서 형태=학위·나이·합격·특정 국가의 졸업식 증명 아님
- 원본 픽셀 gate: 한 폴더·두 인물의 손·지지 방향
- 제안 슬롯: action, occasion_context; scope: authored ceremony

## A10 프롬의 비선정적 장면

- 분류/우선순위: `proxy` / P1
- 원 항목: 101, 68
- 근거 범위: S05, S17
- EN 제안: Formally dressed pairs stand near a school dance floor, with a staffed ticket table at the entrance and decorations above the floor.
- KO 제안: 격식을 갖춰 입은 사람들이 학교 무도장 바닥 가까이에 서 있고 입구에는 담당자가 있는 표 확인 테이블, 바닥 위에는 장식이 있다.
- 소유/관계: ticket_table → at → entrance; decorations → above → dance_floor; attendees → near → dance_floor
- 혼동 경계: 프롬·홈커밍·결혼식은 외형만으로 동일/확정 금지; 연인·성인 여부 별도
- 원본 픽셀 gate: 학교 행사 선언과 보이는 무도장 구성 분리
- 제안 슬롯: occasion_context, location; scope: declared prom setting

## A11 홈커밍 퍼레이드의 한 구성

- 분류/우선순위: `proxy` / P1
- 원 항목: 100, 102, 103
- 근거 범위: S10
- EN 제안: A decorated float moves along a campus parade route, with spectators standing on both sides behind the route boundary.
- KO 제안: 장식한 퍼레이드 차량이 캠퍼스 길에 있고 관람자가 통행 경계 바깥 양쪽에 서 있다.
- 소유/관계: float → within → route; spectators → outside → route_boundary
- 혼동 경계: 동문이라는 신원·귀환의 시간성·미국 전역 관습을 이미지에서 확정하지 않음
- 원본 픽셀 gate: 차량·행렬 경로·경계·양측 관객
- 제안 슬롯: occasion_context, action; scope: US university example

## A12 조별과제의 공유 결과물

- 분류/우선순위: `visible` / P0
- 원 항목: 108, 118
- 근거 범위: S08
- EN 제안: Group members work around one tabletop model, with different hands holding a ruler, joining pieces and recording measurements on a shared sheet.
- KO 제안: 조원들이 모형 하나를 둘러싸고 서로 다른 손이 자를 대고 부품을 연결하며 공동 기록지에 치수를 적는다.
- 소유/관계: ruler → against → model; joining_hand → touches → pieces; recording_hand → writes_on → sheet
- 혼동 경계: 공동 작업 외형만으로 공정 기여·문화자본·평가 점수 판정 금지
- 원본 픽셀 gate: 동일 모형·역할별 손·기록지의 관계; 인원 잠금 지킴
- 제안 슬롯: action, relational_action; scope: authored classroom task

## A13 시험의 현재 배치

- 분류/우선순위: `visible` / P0
- 원 항목: 106, 109, 110, 114
- 근거 범위: S08
- EN 제안: Spaced desks each hold a question booklet and an answer sheet, while the selected examinee marks a box with a pencil.
- KO 제안: 간격을 둔 각 책상에 문제지와 답안지가 있고 선택한 응시자가 연필로 답안 칸을 표시한다.
- 소유/관계: pencil_tip → touches → answer_box; booklet → beside → answer_sheet; examinee → seated_at → desk
- 혼동 경계: 수능/내신/모의고사·부정행위·성적·입시 전형은 별도
- 원본 픽셀 gate: 지문과 답안 층위·펜 끝·문서 수; 정확 텍스트는 별도
- 제안 슬롯: action, prop_placement; scope: generic exam not current CSAT replica

## A14 야간 자습의 가시 성분

- 분류/우선순위: `visible` / P0
- 원 항목: 112, 119
- 근거 범위: S08
- EN 제안: A student studies at an illuminated desk while the classroom window shows a dark exterior and reflections of the room lights.
- KO 제안: 학생이 밝은 책상에서 공부하고 교실 창문에는 어두운 바깥과 실내 조명 반사가 함께 보인다.
- 소유/관계: lamp → lights → desk; window → shows → dark_exterior; window → reflects → room_lights
- 혼동 경계: 어둠=강제 야자·과로·번아웃의 확정 증거 아님
- 원본 픽셀 gate: 실내 작업면·창밖·반사·빛 소유 분리
- 제안 슬롯: action, time_of_day, lighting; scope: authored evening study

## A15 삼자면담 배치

- 분류/우선순위: `proxy` / P1
- 원 항목: 105, 117
- 근거 범위: S04, S05
- EN 제안: Three participants occupy different sides of a desk, and one turns a progress sheet so the other two can see it.
- KO 제안: 세 참석자가 책상 서로 다른 쪽에 앉고 한 사람이 경과표를 다른 두 명 쪽으로 돌려 보여 준다.
- 소유/관계: sheet → on → desk; presenter → turns_toward → listeners; listeners → face → sheet
- 혼동 경계: 세 명=교사·학부모·학생의 증거 아님; 압박·진로 통제는 문맥
- 원본 픽셀 gate: 세 참석자·문서·공유 시선; 역할 선언 별도
- 제안 슬롯: proxemics, participant_role; scope: authored school meeting

## A16 비선정적 관계·경계 교육

- 분류/우선순위: `visible` / P0
- 원 항목: 151, 158, 165
- 근거 범위: S15
- EN 제안: An educator points to a classroom diagram of personal-space circles while learners sit facing the diagram with worksheets on their desks.
- KO 제안: 교육자가 개인 공간 원을 그린 수업 도해를 가리키고 학습자들은 책상에 활동지를 놓고 도해를 향해 앉아 있다.
- 소유/관계: educator → points_to → diagram; learners → face → diagram; worksheets → on → desks
- 혼동 경계: 성교육을 성행위·노출로 치환하지 않음; 동의 획득 사실은 장면으로 판정 불가
- 원본 픽셀 gate: 교육자·도해·활동지; 비선정적 교육 장면만
- 제안 슬롯: action, prop; scope: age-appropriate educational context

## R01 동아리 모집 접수

- 분류/우선순위: `visible` / P0
- 원 항목: 9, 123, 126, 127, 202
- 근거 범위: S02, S17
- EN 제안: One student offers a club flyer across a recruitment table while another holds a pen above the sign-up sheet on that table.
- KO 제안: 한 학생이 모집 테이블 건너로 동아리 전단을 내밀고 다른 학생은 같은 테이블의 신청서 위에 펜을 든다.
- 소유/관계: flyer → offered_across → table; pen → above → signup_sheet; signup_sheet → on → table
- 혼동 경계: 폐부 위기·최소 인원·귀가부 실제 조직을 자동 추가 금지
- 원본 픽셀 gate: 전단·신청서·손·공유 테이블
- 제안 슬롯: action, relational_action; scope: authored recruitment

## R02 학생 매니저의 기록 지원

- 분류/우선순위: `visible` / P0
- 원 항목: 124, 125, 129, 130
- 근거 범위: S02
- EN 제안: A team assistant holds a clipboard beside the sideline bench, with a water carrier resting under the bench and players visible on the court.
- KO 제안: 팀 지원 인물이 사이드라인 벤치 옆에서 기록판을 들고 벤치 아래 물통 운반대와 코트의 선수들이 보인다.
- 소유/관계: assistant → holds → clipboard; water_carrier → under → bench; players → within → court
- 혼동 경계: 매니저 성별·복종 관계·선발 서열은 가시 성분에서 분리
- 원본 픽셀 gate: 코트/벤치/지원 도구의 위치; assistant 신분은 선언
- 제안 슬롯: action, participant_role; scope: authored sports support

## R03 실제 합주의 협업 접점

- 분류/우선순위: `visible` / P0
- 원 항목: 134, 131
- 근거 범위: S01, S02
- EN 제안: The conductor's raised baton faces players whose instruments point toward music stands, with each player's hands attached to their own instrument.
- KO 제안: 지휘자의 든 지휘봉이 연주자들을 향하고 연주자 각자의 손이 자기 악기를 잡은 채 보면대 쪽으로 놓인다.
- 소유/관계: conductor → holds → baton; players → hold → own_instruments; players → face → music_stands
- 혼동 경계: 조화로운 소리·연습 기간·팀워크 품질은 사진 gate 아님
- 원본 픽셀 gate: 각 손-악기 소유·지휘와 합주 방향
- 제안 슬롯: action, gaze_target; scope: wind ensemble variant

## R04 경음악 밴드의 연결

- 분류/우선순위: `visible` / P1
- 원 항목: 134
- 근거 범위: S02
- EN 제안: A guitarist's instrument cable runs to an amplifier, a singer faces a separate microphone, and a drum kit occupies the rear of the same practice space.
- KO 제안: 기타 케이블이 앰프로 이어지고 가수는 별도 마이크를 향하며 드럼 세트가 같은 연습실 뒤편에 있다.
- 소유/관계: guitar → cabled_to → amplifier; singer → faces → microphone; drumkit → behind → frontline
- 혼동 경계: 취주악 편성·음악의 질·큰 소리·유명 밴드를 추론하지 않음
- 원본 픽셀 gate: 기타-앰프 양끝·가수-마이크·드럼 자리
- 제안 슬롯: action, contact_point; scope: electric band variant

## R05 오디션과 포트폴리오 제시

- 분류/우선순위: `proxy` / P1
- 원 항목: 22, 135
- 근거 범위: S02, S08
- EN 제안: An applicant holds an open portfolio toward a seated review panel, with both pages visible above the table edge.
- KO 제안: 지원자가 펼친 포트폴리오를 앉은 심사자들 쪽으로 들고 두 페이지가 테이블 가장자리 위에 보인다.
- 소유/관계: applicant → holds → portfolio; portfolio → faces → review_panel
- 혼동 경계: 합격·재능·공정 심사·악의적 평가를 도출하지 않음
- 원본 픽셀 gate: 같은 포트폴리오·페이지 지지·심사자 방향
- 제안 슬롯: action, prop; scope: authored review

## R06 훈련의 도구와 공간

- 분류/우선순위: `visible` / P1
- 원 항목: 10, 128, 129, 130, 133
- 근거 범위: S02, S09
- EN 제안: Players repeat a ball drill on a marked field while spare balls remain in a basket outside the practice lane.
- KO 제안: 선수들이 표시된 운동장에서 공 훈련 자세를 취하고 여분 공은 훈련선 바깥 바구니에 담겨 있다.
- 소유/관계: practice_ball → within → lane; spare_balls → inside → basket; basket → outside → lane
- 혼동 경계: 반복 훈련·합숙·인터하이·고시엔 신원은 한 순간으로 입증 불가
- 원본 픽셀 gate: 연습자·선택 공·여분 도구·동선 분리
- 제안 슬롯: action, prop_placement; scope: authored practice not branded tournament

## R07 세대교체의 대리 장면

- 분류/우선순위: `proxy` / P1
- 원 항목: 38, 124, 132
- 근거 범위: S02
- EN 제안: Two team members hold opposite ends of one folded team banner, with the receiving person's hands beneath its lower edge.
- KO 제안: 팀원 두 명이 접힌 팀 깃발 하나의 양끝을 잡고 받는 사람의 손이 아래 가장자리를 받친다.
- 소유/관계: giver_hand → holds → banner_end_A; receiver_hand → supports → banner_end_B
- 혼동 경계: 외형 나이=선배·후배·은퇴·승계 동의의 증거 아님
- 원본 픽셀 gate: 깃발 하나·양끝·각 인물 손의 지지
- 제안 슬롯: relational_action, contact_point; scope: authored handover

## R08 고립과 집단 배치

- 분류/우선순위: `proxy` / P0
- 원 항목: 48, 49, 50, 52, 139, 141
- 근거 범위: S11, S17
- EN 제안: One student sits at a separate table while a nearby group turns their chairs inward around a shared table, leaving a visible gap between the tables.
- KO 제안: 한 학생이 별도 테이블에 앉고 가까운 집단은 공동 테이블 안쪽으로 의자를 돌려 두 테이블 사이에 간격이 남는다.
- 소유/관계: individual → at → separate_table; group_chairs → face → shared_table; gap → between → tables
- 혼동 경계: 혼자 있음=왕따·외로움·집단 의도·성격·카스트를 입증하지 않음
- 원본 픽셀 gate: 개인·집단·방향·빈 간격만 가시 판정
- 제안 슬롯: proxemics, composition; scope: authored social scene

## F01 학습이 보이는 마법 교실

- 분류/우선순위: `visible` / P1
- 원 항목: 166, 172
- 근거 범위: S18
- EN 제안: At a classroom workbench, a learner holds a wand toward a small suspended object while an instructor points to the object's position above the bench.
- KO 제안: 교실 작업대에서 학습자가 지팡이를 작은 공중 물체 쪽으로 들고 지도자는 작업대 위 그 물체 위치를 가리킨다.
- 소유/관계: learner → aims → wand; object → above → bench; instructor → points_to → object
- 혼동 경계: 특정 IP·주문 효능·초능력 소유·학교 체제는 별도
- 원본 픽셀 gate: 작은 물체·작업대·두 인물 방향; 허공 물체의 지지 규칙은 창작 설정
- 제안 슬롯: world, location, action; scope: original fictional school

## F02 전투 교육의 연습 구역

- 분류/우선순위: `visible` / P1
- 원 항목: 167, 170, 171
- 근거 범위: S18
- EN 제안: Two trainees stand on opposite marked positions inside a practice ring while an instructor watches from outside its boundary.
- KO 제안: 두 훈련자가 연습장 안 서로 반대 표식 위에 서고 지도자는 경계 밖에서 지켜본다.
- 소유/관계: trainees → inside → ring; instructor → outside → ring
- 혼동 경계: 성적·계급·실제 전투·강요·부상 자동 부여 금지
- 원본 픽셀 gate: 훈련 구역·두 위치·감독 위치; 무기 세부는 별도
- 제안 슬롯: location, action; scope: original fictional academy

## F03 적성 측정의 접점

- 분류/우선순위: `proxy` / P1
- 원 항목: 169, 172, 178
- 근거 범위: S21
- EN 제안: A test subject rests one palm on a measurement plate connected by a cable to a display on the same desk.
- KO 제안: 검사 대상이 같은 책상의 표시장치와 케이블로 이어진 측정판에 한 손바닥을 댄다.
- 소유/관계: palm → rests_on → plate; plate → cabled_to → display
- 혼동 경계: 숫자=실제 능력·가치·낮은 재능·숨은 최강자 판정 금지
- 원본 픽셀 gate: 손바닥-판·케이블 양끝·표시장치
- 제안 슬롯: action, object_structure; scope: original fictional test

## F04 랭킹과 포인트의 기록 매체

- 분류/우선순위: `proxy` / P1
- 원 항목: 170, 173, 174
- 근거 범위: S21
- EN 제안: A wall display shows a clearly separated class list, numerical columns and one highlighted row, with students standing in front of the display.
- KO 제안: 벽 화면에 구분된 학급 목록과 숫자 열, 강조된 행 하나가 있고 학생들은 그 화면 앞에 서 있다.
- 소유/관계: class_list → on → display; highlight → marks → one_row; students → in_front_of → display
- 혼동 경계: 포인트=돈·복지·통치권·실제 성적은 명시된 설정 없으면 미확정
- 원본 픽셀 gate: 화면 층위·열·강조 행; 문자 정확성은 별도 gate
- 제안 슬롯: prop, visible_text; scope: original fictional interface

## F05 학교 결계의 가시 경계

- 분류/우선순위: `visible` / P1
- 원 항목: 176
- 근거 범위: S18
- EN 제안: A translucent curved boundary crosses the school courtyard, and a small airborne object meets a localized glow at that same boundary.
- KO 제안: 반투명 곡면 경계가 학교 중정을 가르고 작은 공중 물체가 같은 경계의 국소 발광점에 닿아 있다.
- 소유/관계: boundary → crosses → courtyard; object → meets → glow; glow → on → boundary
- 혼동 경계: 빛 원=실제 보호·원인·안전·성공적 방어 증명 아님
- 원본 픽셀 gate: 동일 경계·물체 접점·학교와 규모; 전체 후광으로 대체 실패
- 제안 슬롯: surreal_physics_detail, scale_relation; scope: original fictional barrier

## F06 교외 실습의 경계 통과

- 분류/우선순위: `visible` / P1
- 원 항목: 177, 171
- 근거 범위: S18
- EN 제안: A small team follows a marked path from a school practice gate toward a cave entrance, carrying the same equipment through the gate.
- KO 제안: 작은 팀이 학교 실습문에서 동굴 입구로 이어지는 표시 길을 따라 같은 장비를 들고 통과한다.
- 소유/관계: path → starts_at → gate; path → ends_at → cave; team → follows → path; equipment → carried_by → team
- 혼동 경계: 던전 시험·평가권·실제 위험은 장소로 확정하지 않음
- 원본 픽셀 gate: 문·동굴·연결길·팀 인원·장비 소유
- 제안 슬롯: action, location; scope: original fictional field exercise

## F07 학급재판의 창작 공간

- 분류/우선순위: `proxy` / P1
- 원 항목: 189
- 근거 범위: S19
- EN 제안: Separated lecterns face an open central area, with participants standing at the lecterns and evidence images displayed on a wall beyond them.
- KO 제안: 분리된 발언대들이 열린 중앙 공간을 향하고 각 발언대의 참석자 뒤쪽 벽에 증거 이미지가 표시된다.
- 소유/관계: lecterns → face → central_space; participants → at → lecterns; evidence_images → on → wall
- 혼동 경계: 일반 학급회의·법정·정의 실현과 구분; 원작 게임 공간 정확 복제 아님
- 원본 픽셀 gate: 발언대·참석자·중앙 공간·화면 속 증거 층위
- 제안 슬롯: composition, location; scope: series-specific concept; original arrangement

## F08 학원도시의 복수 교육시설

- 분류/우선순위: `visible` / P1
- 원 항목: 168, 175
- 근거 범위: S18, S21
- EN 제안: Several distinct educational buildings surround a shared transit corridor, with classroom blocks, a research tower and residences occupying separate zones.
- KO 제안: 여러 교육 건물이 공동 교통축 둘레에 있고 교실 동, 연구탑, 생활동이 서로 다른 구역을 차지한다.
- 소유/관계: transit_corridor → links → educational_blocks; research_tower → separate_from → residences
- 혼동 경계: 학교 수·학생 비율·도시 자치권·연구 불법성을 건물로 입증하지 않음
- 원본 픽셀 gate: 교육·연구·주거의 구별된 규모와 연결
- 제안 슬롯: location, scale_relation; scope: original fictional city

## H01 현재의 물리적 통행 방해

- 분류/우선순위: `proxy` / P0
- 원 항목: 136, 137, 140, 143, 144
- 근거 범위: S11, S23
- EN 제안: One figure stands across another person's route through a corridor, leaving that person between the blocker and the wall.
- KO 제안: 한 인물이 복도의 다른 인물 이동 경로를 가로막아 그 사람이 가로막는 인물과 벽 사이에 놓인다.
- 소유/관계: blocker → across → route; person → between_endpoint_A → blocker; person → between_endpoint_B → wall
- 혼동 경계: 현재 방해=반복 괴롭힘·범죄·동의·가해자 정체 확정 아님
- 원본 픽셀 gate: 행위자·대상·막힌 경로·벽의 관계
- 제안 슬롯: relational_action, proxemics; scope: non-graphic conflict

## H02 방어자의 개입 배치

- 분류/우선순위: `proxy` / P0
- 원 항목: 147
- 근거 범위: S11
- EN 제안: A third person steps between two people and extends an open hand toward the nearer person while leaving a clear exit route beside the other.
- KO 제안: 제삼자가 두 사람 사이에 서서 가까운 사람 쪽으로 펼친 손을 내밀고 다른 사람 옆에는 빠져나갈 길이 남는다.
- 소유/관계: defender → between_endpoint_A → person_A; defender → between_endpoint_B → person_B; open_hand → toward → person_A; exit_route → beside → person_B
- 혼동 경계: 내면 의도·용기·실제 구조 성공을 외형에서 판정하지 않음
- 원본 픽셀 gate: 세 사람·손 소유·간격·탈출 동선
- 제안 슬롯: relational_action, contact_point; scope: non-graphic intervention

## H03 온라인 위협의 기록 매체

- 분류/우선순위: `proxy` / P0
- 원 항목: 142, 148, 162
- 근거 범위: S11, S14
- EN 제안: A hand holds a phone displaying a fictional message thread, with a highlighted warning bubble and a visible report control on the same screen.
- KO 제안: 손에 든 휴대전화의 가상 메시지 대화에 강조된 경고 말풍선과 신고 조작부가 같은 화면에 보인다.
- 소유/관계: hand → holds → phone; message_thread → on → screen; report_control → within → screen
- 혼동 경계: 실제 비동의 이미지·성적 이미지 재현 금지; 화면=유포·위협 사실의 독립 증거 아님
- 원본 픽셀 gate: 화면과 실물 구분·손 소유·가상 UI; 민감 내용은 비선정적
- 제안 슬롯: prop, visible_text; scope: non-explicit fictional screen

## H04 막힌 학교 출입구

- 분류/우선순위: `visible` / P0
- 원 항목: 184, 187, 188, 190, 192
- 근거 범위: S19, S20
- EN 제안: Desks are stacked against the interior of a classroom door, with the nearest desk legs braced on the same floor as the door frame.
- KO 제안: 책상이 교실 문 안쪽에 쌓여 있고 가장 가까운 책상 다리가 문틀과 같은 바닥을 버틴다.
- 소유/관계: desks → block → door; desk_legs → brace_on → floor
- 혼동 경계: 봉쇄 원인·살인 게임·감염·탈출 불가능성을 자동 확정하지 않음
- 원본 픽셀 gate: 문-책상 접촉·무게 지지·문 개방 방향
- 제안 슬롯: object_structure, space_condition; scope: fictional confinement scene

## H05 거울 속 대응 불일치

- 분류/우선순위: `visible` / P1
- 원 항목: 182, 183
- 근거 범위: S23
- EN 제안: One person faces a mirror with both arms down, while the corresponding mirror figure has one arm raised in the same reflection frame.
- KO 제안: 한 사람이 두 팔을 내린 채 거울을 향하지만 같은 반사 프레임의 대응 인물은 한 팔을 든다.
- 소유/관계: person → faces → mirror; reflected_person → within → mirror; reflected_arm → differs_from → actual_arm
- 혼동 경계: 유령 정체·원한·장소에 묶임은 불일치로 입증하지 않음
- 원본 픽셀 gate: 원인 몸·반사 프레임·대응 팔이 동시에 가시; 두 실제 인물 실패
- 제안 슬롯: reflection_logic, composition; scope: original supernatural image

## H06 사건 이후의 학교 사물

- 분류/우선순위: `visible` / P1
- 원 항목: 149, 150, 193, 195
- 근거 범위: S23
- EN 제안: An overturned desk and torn papers lie beside a damaged classroom door, while the corridor beyond remains visibly empty.
- KO 제안: 넘어진 책상과 찢긴 종이가 파손된 교실 문 옆에 있고 그 너머 복도는 비어 있다.
- 소유/관계: desk → overturned_on → floor; papers → beside → damaged_door; corridor → beyond → door
- 혼동 경계: 손상=자해·사망·범인·원인·복수 성공으로 해석 금지
- 원본 픽셀 gate: 현재 손상 상태·실내외 층위·빈 복도; 고어 자동 추가 금지
- 제안 슬롯: aftermath_trace, prop_state; scope: non-graphic aftermath

## H07 감시 장치의 가시 방향

- 분류/우선순위: `visible` / P1
- 원 항목: 192, 175
- 근거 범위: S19, S21
- EN 제안: A ceiling camera points toward a classroom doorway, and a wall monitor shows a framed view of that same doorway from above.
- KO 제안: 천장 카메라가 교실 출입문을 향하고 벽 모니터에는 같은 문을 위에서 본 프레임이 표시된다.
- 소유/관계: camera → points_to → doorway; monitor → shows → doorway_view
- 혼동 경계: 감시 체제·불법성·모든 학생 추적·통치 권한은 문맥
- 원본 픽셀 gate: 실제 문/카메라/화면 속 문의 위치 대응
- 제안 슬롯: prop_placement, object_structure; scope: original fictional school

## H08 현재의 기억·애도 공간

- 분류/우선순위: `proxy` / P1
- 원 항목: 150, 195, 210
- 근거 범위: S23
- EN 제안: Flowers and handwritten cards rest beside an unoccupied school desk, with a clear space preserved around the chair.
- KO 제안: 비어 있는 학교 책상 옆에 꽃과 손글씨 카드가 놓이고 의자 둘레 공간이 비어 있다.
- 소유/관계: flowers → beside → desk; cards → beside → flowers; chair → within → clear_space
- 혼동 경계: 애도 표현=자살·사망 원인·책임·치유 완료 증명 불가
- 원본 픽셀 gate: 꽃·카드·빈 자리의 관계만 가시; 문구 읽기 별도
- 제안 슬롯: prop_placement, occasion_context; scope: non-graphic remembrance

## A17 자리 배치 변경의 현재 상태

- 분류/우선순위: `visible` / P0
- 원 항목: 92
- 근거 범위: S04
- EN 제안: A student carries a chair between two desk rows while another desk stands outside the otherwise aligned row.
- KO 제안: 한 학생이 두 책상 열 사이로 의자를 들고 있고 다른 책상 하나가 정렬된 열에서 벗어나 있다.
- 소유/관계: student → carries → chair; chair → between → desk_rows; loose_desk → outside → aligned_row
- 혼동 경계: 현재 재배치=이전 자리·추첨 공정성·반 편성 결과 증거 아님
- 원본 픽셀 gate: 의자 지지·통로 폭·정렬 기준·벗어난 책상
- 제안 슬롯: prop_placement, object_structure; scope: authored classroom rearrangement

## A18 수학여행 집합의 대리 표현

- 분류/우선순위: `proxy` / P1
- 원 항목: 96
- 근거 범위: S01, S04
- EN 제안: A group waits beside a parked coach with small travel bags while one leader holds a checklist at the open coach door.
- KO 제안: 한 집단이 작은 여행 가방을 들고 주차된 버스 옆에서 기다리며 인솔자 한 명이 열린 문 앞에서 점검표를 든다.
- 소유/관계: group → beside → coach; bags → carried_by → group; leader → holds → checklist; leader → at → coach_door
- 혼동 경계: 학교 수학여행·도착지·숙박·공식 인솔 권한은 가시 장면에서 확정 불가
- 원본 픽셀 gate: 버스 문·인솔 위치·가방 소유·선택한 집단 인원
- 제안 슬롯: occasion_context, action; scope: authored group excursion

## C01 학원물·장르·성장·AU의 범위

- 분류/우선순위: `context` / P0
- 원 항목: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
- 근거 범위: S01, S16, S17, S18, S22
- 한 장에서 증명 불가: 장르·성장·세계 존망·원작과의 동일성
- 처리: 장르 route는 advisory. 학생 나이·교복·벚꽃·일본·고딕·괴물을 강제하지 않는다. 구체 성분을 고른 뒤 별도 가시 카드만 제안한다.

## C02 제도·학교급·학교의 평판

- 분류/우선순위: `context` / P0
- 원 항목: 16, 17, 18, 19, 20, 21, 22, 23, 27, 28, 29, 30
- 근거 범위: S04, S05, S06, S07
- 한 장에서 증명 불가: 공립/사립·명문·재단·학칙 권한·소속·젠더 구성
- 처리: country/region·school_level·era·real_or_fiction·institution_variant를 분리한다. public school은 지역별 뜻 확인 전 번역을 보류한다.

## C03 신분·교직·선후배·능력 낙인

- 분류/우선순위: `context` / P0
- 원 항목: 25, 26, 28, 31, 32, 33, 34, 35, 36, 37, 38, 41, 42, 43, 44, 45, 46, 47, 124, 125
- 근거 범위: S04, S05, S06
- 한 장에서 증명 불가: 학년·복학 이력·교사 자격·부·재능·인격
- 처리: 외형 나이·안경·재산 소품·성적표로 역할과 도덕을 확정하지 않는다. 역할은 사용자 선언으로 보존하고 행동만 선택한다.

## C04 인기·카스트·하위문화의 해석

- 분류/우선순위: `context` / P0
- 원 항목: 48, 49, 50, 51, 52, 53, 137, 138, 139
- 근거 범위: S11, S17
- 한 장에서 증명 불가: 인기·고립의 선택성·하위문화의 가치·폭력성
- 처리: 집단 위치·외형 스타일은 선택 가능한 현재 표현. 갸루·너드·조크·퀸비·불량문화를 성행동·지능·신분과 묶지 않는다. 세부 문화사는 추가 검증한다.

## C05 팬덤 성격·모에·위장 신분

- 분류/우선순위: `context` / P1
- 원 항목: 54, 55, 56, 57, 58, 59, 60
- 근거 범위: S17
- 한 장에서 증명 불가: 츤데레/얀데레·정신질환·숨은 친밀함·성별 정체성·이중생활
- 처리: 표정·의복·행동 한 조각을 성격/질환/정체성의 PASS로 사용하지 않는다. 팬덤용 명칭과 실제 진단·성별을 분리한다.

## C06 연애 감정·관계 변화·다각 구조

- 분류/우선순위: `context` / P0
- 원 항목: 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 75, 98
- 근거 범위: S16
- 한 장에서 증명 불가: 첫사랑·상호감정·계약·비밀·관계의 변화·감정 기한
- 처리: 한 우산·봉투·인물 세 명은 각각 소품/전달/구도만 증명한다. 관계와 시간은 명시 문맥으로 남기고 접촉 수위를 자동 올리지 않는다.

## C07 BL·GL·친밀함·커밍아웃과 아웃팅

- 분류/우선순위: `context` / P0
- 원 항목: 71, 72, 73, 74
- 근거 범위: S15
- 한 장에서 증명 불가: 성적 지향·당사자 정체성·동의된 공개·시핑의 정사성
- 처리: 동성 인물 배치나 의복으로 지향/성별/동의를 확정하지 않는다. 이성 관계와 같은 비선정적 행동 후보를 제공하며 정체성을 소품으로 고정하지 않는다.

## C08 학업 제도·평가·계층·불안

- 분류/우선순위: `context` / P0
- 원 항목: 106, 107, 109, 110, 111, 114, 115, 116, 117, 118, 119, 120
- 근거 범위: S07, S08
- 한 장에서 증명 불가: 학력·내신·학생부·전형·번아웃·등교거부·경제적 원인
- 처리: 문서와 작업 장면은 보이는 것만. 실제 입시·수시/정시·학생부 양식·야자 규칙은 연도와 지역의 공식 문서 검토 후 별도 채택한다.

## C09 부활동 운영·선발·귀가부·은퇴

- 분류/우선순위: `context` / P0
- 원 항목: 9, 10, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135
- 근거 범위: S02, S09
- 한 장에서 증명 불가: 최소 부원 수·가입 의무·천재/언더독·팀워크·합숙·은퇴
- 처리: 귀가부를 실제 부실로 만들지 않는다. 인터하이·고시엔·봄 선발·여름 선수권·일반 대회를 분리하고 운영 규칙은 작품/학교 판본으로 둔다.

## C10 괴롭힘·강요·반복성과 집단 역할

- 분류/우선순위: `context` / P0
- 원 항목: 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147
- 근거 범위: S11, S12
- 한 장에서 증명 불가: 반복·권력차·원치 않음·소속 압력·가해/방관/방어 의도
- 처리: 폭력·갈취·헤이징을 평범한 친구 장면으로 소거하지 않되, 현재의 통행 방해·접촉·기록과 비가시 행위 맥락을 별도로 기록한다.

## C11 은폐·보복·제도적 책임·복수

- 분류/우선순위: `context` / P0
- 원 항목: 148, 149, 175, 192
- 근거 범위: S11, S19, S23
- 한 장에서 증명 불가: 은폐 목적·책임·복수의 정당성·2차 가해·통치 권리
- 처리: 지워진 종이·흉터·감시장치·엄한 표정을 범죄/책임의 증거로 쓰지 않는다. 제도 비판 범주는 유지하며 특정 시각 장식으로 자동 실현하지 않는다.

## C12 자해·자살·상실·회복

- 분류/우선순위: `context` / P0
- 원 항목: 150, 195
- 근거 범위: S23
- 한 장에서 증명 불가: 손상의 자해 원인·사망 원인·진단·생존자 죄책감·회복 완료
- 처리: 개념을 비평·서사 문맥에 보존한다. 방법·도구·실행 장면을 후보 초안으로 만들지 않고 비그래픽 도움·관계·애도 장면을 별도로 제안한다.

## C13 사춘기·성적 금기·팬서비스·에치

- 분류/우선순위: `context` / P0
- 원 항목: 151, 152, 153, 154, 155
- 근거 범위: S15
- 한 장에서 증명 불가: 성적 각성·대사 이중 의미·내면 욕망·팬 기대·금기의 원인
- 처리: 비평 용어는 문맥에 남긴다. 미성년 또는 나이 불명 학교 인물에 성적 시각 레시피를 제공하지 않는다. 팬서비스의 비성적 뜻과 성교육 장면을 유지한다.

## C14 대상화·시선·관음·페티시화

- 분류/우선순위: `context` / P0
- 원 항목: 156, 157
- 근거 범위: S00
- 한 장에서 증명 불가: 서술/카메라/관객의 시선 구조·성적 소비·몰래 촬영 의도
- 처리: 원 대화의 비평 범주로 보존하며 장면·편집·출처를 추가 검토한다. 성적 신체 분절 프레이밍·학생 페티시 의상 후보로 변환하지 않는다.

## C15 동의·관계 경계의 비가시성

- 분류/우선순위: `context` / P0
- 원 항목: 158
- 근거 범위: S15
- 한 장에서 증명 불가: 자발적·지속적·정보에 기반한 동의와 거부·강요의 부재
- 처리: 미소·침묵·접촉·나이 설정을 동의 증명으로 쓰지 않는다. 교육·대화·거리 조절 같은 비선정적 선택지만 독립적으로 검토한다.

## C16 사제 관계·그루밍·평가권

- 분류/우선순위: `context` / P0
- 원 항목: 159, 160
- 근거 범위: S13, S15
- 한 장에서 증명 불가: 학대 의도·누적 관계 조작·평가 통제·거절 비용
- 처리: 교사·성인·선물·멘토링 외형만으로 학대 또는 동의를 확정하지 않는다. 미성년 성적 묘사를 생성하지 않으며 비평·신고·지원 맥락으로 다룬다.

## C17 성폭력·이미지 기반 가해·낙인·착취

- 분류/우선순위: `context` / P0
- 원 항목: 161, 162, 163, 164
- 근거 범위: S13, S14
- 한 장에서 증명 불가: 비동의·이미지 실제 유포·허위 합성·대가 조건·강요
- 처리: 피해 범주는 삭제하지 않는다. 성적 피해 이미지·성적 메시지의 재현 초안 없이 비선정적 기록/신고/지원 표현과 문맥으로 분리한다.

## C18 성교육·임신·재생산 선택

- 분류/우선순위: `context` / P0
- 원 항목: 165
- 근거 범위: S15
- 한 장에서 증명 불가: 임신 진단·개인의 선택·관계 이력·사회적 제약
- 처리: 성교육은 연령에 맞는 교육. 외형 체형으로 임신을 확정하거나 진로/선택을 추론하지 않는다. 의료 사실은 별도의 정확한 출처와 요청 필요.

## C19 학원 판타지의 제도와 능력

- 분류/우선순위: `context` / P1
- 원 항목: 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180
- 근거 범위: S18, S21
- 한 장에서 증명 불가: 능력 실재·객관 등급·학생 통치·숨은 최강·게임 빙의·회귀
- 처리: 구체 학교·판본·보이는 효과를 선택한다. 숫자·색·마법진·로브를 단일 세트로 자동 강제하지 않는다. IP-specific와 original-fiction을 분리한다.

## C20 학교괴담·원혼·일곱 불가사의

- 분류/우선순위: `context` / P1
- 원 항목: 182, 183
- 근거 범위: S23
- 한 장에서 증명 불가: 귀신 정체·원한·장소 결박·일곱 가지 고정 목록
- 처리: 어둠·창백한 사람·거울 불일치는 각각 별도 상태. 특정 작품의 일곱 불가사의를 보편 학교 목록으로 만들지 않는다.

## C21 미스터리·기록·폐쇄·죽음의 게임

- 분류/우선순위: `context` / P1
- 원 항목: 181, 184, 185, 186, 187, 188, 189, 190, 193, 194
- 근거 범위: S19, S20, S23
- 한 장에서 증명 불가: 범인·실종·밀실 성립·고립·죽음의 룰·감염·실험 원인
- 처리: 잠긴 문/지도/명부·신체 변화의 가시 형태와 범죄/게임 규칙을 분리한다. class trial은 특정 작품 개념. 실험체·고어는 학교 라벨에서 자동 활성화하지 않는다.

## C22 시간 구조·세계 소개·졸업 이후

- 분류/우선순위: `sequence` / P1
- 원 항목: 100, 180, 191, 196, 200, 201, 210
- 근거 범위: S00
- 한 장에서 증명 불가: 반복된 하루·회귀·성장·동일 인물의 전후·수미상관
- 처리: 정지사진 1장으로 sequence PASS 불가. 달력·전후 병치는 가시 기록일 뿐 실제 시간 반복 증거 아님. 시퀀스 작업에서 별도 계약 필요.

## C23 계절·공간·소품·비밀·화자와 상징

- 분류/우선순위: `context` / P1
- 원 항목: 6, 97, 197, 198, 199, 202, 203, 204, 205, 206, 207, 209
- 근거 범위: S16, S17, S22
- 한 장에서 증명 불가: 청춘 유한성·공범·정보차·미화·작가의 상징 의도
- 처리: 벚꽃=봄 입학·눈=상실·계단=위계 등 보편 대응표 금지. 보이는 계절 단서·대응 사물·프레임 관계와 문맥 해석을 분리한다.

## C24 생활음·종소리·교내 방송

- 분류/우선순위: `audio` / P0
- 원 항목: 78, 208
- 근거 범위: S01
- 한 장에서 증명 불가: 소리의 실재·음량·방송 내용·종이 울린 시각
- 처리: 스피커·방송 장비·진동 표현은 visual proxy일 뿐 소리의 PASS가 아니다. audio/sequence 전용 평가에만 음향 증거를 부여한다.

