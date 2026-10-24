# 시각 의미 카드

관계의 양 끝과 물리적 귀속을 보존한다. 아래 구도는 연구자가 제안한 실현이며 문헌이 모든 geometry를 증명한 것은 아니다.

## S01 대형 강의실, 강의실

- 유형: observable / P0
- 한글: 단차가 있는 긴 좌석 열이 앞 강연대와 스크린을 향하고 옆 통로가 각 열로 이어진다.
- English: Tiered rows of long seats face a front lectern and screen, with a side aisle reaching each row.
- 관계: seat_rows → face → lectern; screen → behind → lectern; aisle → connects_to → seat_rows
- 혼동 경계: 홈룸의 개별 책상이나 극장과 구별하며 대학 신원은 별도 맥락이다.
- 관찰 게이트: 단차·강연대·스크린·통로가 함께 보인다.
- 제안 슬롯: location, object_structure; 출처: S04, S05

## S02 과방

- 유형: staged_proxy / P1
- 한글: 공용 탁자 둘레에 서로 다른 가방이 놓이고 벽 게시판 옆에는 학생용 공용 사물함이 있다.
- English: Different bags surround a shared table, with communal lockers beside a wall noticeboard.
- 관계: bags → beside → table; lockers → beside → noticeboard
- 혼동 경계: 과방의 선택적 연출안이며 이 물건만으로 학과 소유나 이용자 신원을 확정하지 않는다.
- 관찰 게이트: 공용 탁자와 수납·게시 공간의 구획이 보인다.
- 제안 슬롯: location, environment_detail; 출처: S05, S07

## S03 과사, 학과사무실

- 유형: staged_proxy / P0
- 한글: 방문자 의자는 접수대 앞에 있고 직원 책상과 서류 보관장은 접수대 안쪽에 놓인다.
- English: A visitor chair stands before a service counter, with a staff desk and document cabinets behind it.
- 관계: visitor_chair → in_front_of → counter; staff_desk → behind → counter; cabinets → behind → counter
- 혼동 경계: 과방과 기능을 구별한다. 서류 내용·학적 처리 권한은 외형만으로 확정되지 않는다.
- 관찰 게이트: 방문자와 업무 구역의 경계가 한 화면에 드러난다.
- 제안 슬롯: location, space_condition; 출처: S05

## S04 동방, 동아리방

- 유형: staged_proxy / P1
- 한글: 소파 옆 선반에는 악기 케이스와 공연 소품 상자가 따로 있고 탁자에는 회의 자료가 놓인다.
- English: A shelf beside a sofa holds separate instrument cases and performance-prop boxes, while meeting papers lie on a table.
- 관계: cases → on → shelf; prop_boxes → on → shelf; shelf → beside → sofa; papers → on → table
- 혼동 경계: 공연 동아리방의 한 예이며 모든 동아리를 음악·낡은 소파로 고정하지 않는다.
- 관찰 게이트: 케이스·상자·회의 탁자가 분리되어 보인다.
- 제안 슬롯: location, prop_placement; 출처: S06

## S05 학식, 학생식당, 밥약

- 유형: observable / P1
- 한글: 두 사람이 맞은편에 앉은 탁자 위에 각자의 식판 하나와 수저가 놓인다.
- English: Two people sit opposite each other at a table with one meal tray and utensils for each person.
- 관계: tray_A → in_front_of → A; tray_B → in_front_of → B; A → opposite → B
- 혼동 경계: 밥약·데이트·선후배 관계·저렴한 가격은 식판만으로 증명하지 않는다.
- 관찰 게이트: 두 식판과 각각의 착석자·탁자 경계가 보인다.
- 제안 슬롯: location, prop_placement, proxemics; 출처: S05

## S06 도서관, 열람실

- 유형: observable / P1
- 한글: 높은 서가 구역과 칸막이 개인 열람석 구역 사이에 통로가 나 있다.
- English: An aisle separates tall bookshelves from a zone of partitioned individual reading desks.
- 관계: aisle → between_endpoint_A → bookshelves; aisle → between_endpoint_B → reading_desks
- 혼동 경계: 자료 검색과 개인 열람·협업실은 서로 다른 기능이며 나무 서가를 강제하지 않는다.
- 관찰 게이트: 서가·칸막이 책상·통로가 동시에 식별된다.
- 제안 슬롯: location, object_structure; 출처: S24

## S07 스터디룸, 세미나실, 팀플

- 유형: observable / P0
- 한글: 한 탁자 주위의 이동식 의자들이 벽 화이트보드와 탁자 중앙을 함께 향한다.
- English: Movable chairs around one table face both a wall whiteboard and the table center.
- 관계: chairs → around → table; whiteboard → on → wall; chairs → oriented_toward → whiteboard
- 혼동 경계: 회사 회의실과도 공유되는 구조이다. 실제 예약·공동 과제 이력은 별도다.
- 관찰 게이트: 탁자·의자 방향·보드가 같은 공간 안에 보인다.
- 제안 슬롯: location, object_structure; 출처: S24, S13

## S08 실험실, 랩, 랩실

- 유형: observable / P1
- 한글: 실험대 위의 용기는 받침대에 고정된 클램프가 잡고 싱크는 용기와 떨어진 같은 작업대 끝에 있다.
- English: A clamp on a stable stand holds a vessel above a lab bench, with a sink at the far end of the same bench.
- 관계: clamp → attached_to → stand; clamp → holds → vessel; stand → on → bench; sink → at_end_of → bench
- 혼동 경계: 컴퓨터 연구실까지 유리기구·흰 가운으로 고정하지 않는다. 실험 성공·무균은 외형으로 입증 불가다.
- 관찰 게이트: 클램프부터 받침대·용기·작업대까지 연결이 보인다.
- 제안 슬롯: location, object_structure; 출처: S14, S15

## S09 설계실, 작업실, 스튜디오, 졸업설계

- 유형: observable / P0
- 한글: 큰 작업대에 절단 매트와 축소 모형이 놓이고 뒤 게시판에는 도면 시트가 각각 고정되어 있다.
- English: A large worktable holds a cutting mat and a scale model, with separate drawing sheets fixed to a board behind it.
- 관계: mat → on → table; model → on → mat; drawings → fixed_to → board; board → behind → table
- 혼동 경계: 건축 작업의 선택적 실현이다. 완성도·학년·마감 시간은 구조와 별개다.
- 관찰 게이트: 모형·매트·고정된 도면·탁자의 지지가 보인다.
- 제안 슬롯: location, prop_placement; 출처: S13

## S10 연습실, 합주실, 리허설

- 유형: observable / P1
- 한글: 서로 다른 악기와 보면대가 반원으로 놓이고 거울은 연주자 뒤 벽에 부착되어 있다.
- English: Distinct instruments and music stands form a semicircle, with a mirror attached to the wall behind the players.
- 관계: instruments → beside → music_stands; stands → form → semicircle; mirror → attached_to → wall
- 혼동 경계: 연주 능력·합주의 실제 소리·방음 성능은 정지 화면에서 통과시키지 않는다.
- 관찰 게이트: 악기와 보면대의 개별 위치·거울의 벽 부착이 보인다.
- 제안 슬롯: location, prop_placement; 출처: S06

## S11 기숙사, 생활관, 룸메이트

- 유형: observable / P0
- 한글: 한 방에 침대 두 개와 개인 책상 두 개가 있고 각 침대 옆 수납은 해당 책상 쪽으로 나뉜다.
- English: One room contains two beds and two personal desks, with separate bedside storage next to each desk zone.
- 관계: bed_A → beside → desk_A; bed_B → beside → desk_B; storage_A → beside → bed_A; storage_B → beside → bed_B
- 혼동 경계: 모든 기숙사의 침대 수가 둘이라는 뜻은 아니다. 기숙사·셰어하우스·연인 관계는 별도 맥락이다.
- 관찰 게이트: 침대 둘·책상 둘과 서로 다른 생활 구역을 셀 수 있다.
- 제안 슬롯: location, object_structure; 출처: S22

## S12 자취방, 원룸, 하숙집, 셰어하우스

- 유형: staged_proxy / P1
- 한글: 침대와 작은 조리대가 한 생활 공간 안에 있고 별도 식탁 위에 개인 교재가 놓인다.
- English: A bed and compact kitchenette share one living space, with personal study books on a separate dining table.
- 관계: bed → within → living_space; kitchenette → within → living_space; books → on → dining_table
- 혼동 경계: 하숙의 식사 제공·임대·동거 이력은 원룸 구조로 입증되지 않는다. 이 카드는 단일 원룸 예다.
- 관찰 게이트: 침대·조리대·식탁의 분리된 지면과 경계가 보인다.
- 제안 슬롯: location, space_condition; 출처: S22, S30

## S13 학생회실, 학생운동, 대자보, 학내 시위

- 유형: staged_proxy / P1
- 한글: 게시판에 서로 다른 큰 종이가 붙어 있고 한 사람이 팔을 뻗어 한 종이의 모서리를 고정한다.
- English: Separate large sheets cover a noticeboard while one person fixes a corner of a sheet with an outstretched hand.
- 관계: sheet → attached_to → noticeboard; hand → belongs_to → A; hand → contacts → sheet_corner
- 혼동 경계: 대자보 글의 진실·학생회 비리·시위 이유·정치 입장은 문서와 맥락이 필요하다.
- 관찰 게이트: 게시 위치·종이 경계·손의 주인과 접촉 모서리가 보인다.
- 제안 슬롯: narrative_clue, prop_placement, visible_text; 출처: S07, S30

## S14 잔디광장, 중정, Quad, 정문, 통학버스 정류장

- 유형: staged_proxy / P1
- 한글: 건물 세 면이 잔디 공간을 둘러싸고 열린 한 면의 보행로 옆에 벤치가 있다.
- English: Three building fronts border a lawn, with a bench beside the path at its open side.
- 관계: buildings → border → lawn; bench → beside → path; path → at_open_side_of → lawn
- 혼동 경계: 이 표본은 열린 중정이다. quad·정문·버스 정류장 각각의 정의를 모두 충족하는 한 구조로 사용하지 않는다.
- 관찰 게이트: 건물의 둘러쌈·열린 면·길·벤치가 보인다. 정류장 후보는 별도 분할한다.
- 제안 슬롯: location, composition; 출처: S09, S30

## W01 과잠, 바시티 재킷, 레터맨 재킷

- 유형: observable / P0
- 한글: 한 착용자의 재킷에 배색 소매와 몸판이 연결되고 골지 깃·소맷단·허리단 및 앞 스냅이 보인다.
- English: One wearer's jacket joins contrasting sleeves to a torso panel and has a ribbed collar, cuffs, waistband and front snaps.
- 관계: jacket → worn_by → A; sleeves → joined_to → torso_panel; ribbing → at → collar_cuffs_waist; snaps → on → jacket_front
- 혼동 경계: 과잠은 소속 표현의 맥락, 바시티는 옷 구조다. 글자 없이도 구조를 평가하되 학적·운동선수·원소유를 확정하지 않는다.
- 관찰 게이트: 양 소매와 몸판 연결·골지·스냅이 동시에 식별된다.
- 제안 슬롯: wardrobe_style, garment_detail; 출처: S08, S09, S11

## W02 레터 스웨터, Varsity

- 유형: observable / P0
- 한글: 한 성인의 니트 풀오버 가슴에 테두리가 있는 큰 글자 패치 하나가 평평하게 붙어 있다.
- English: One adult wears a knitted pullover with a single large outlined letter patch lying flat on the chest.
- 관계: pullover → worn_by → A; patch → attached_to → pullover_chest
- 혼동 경계: 레터 스웨터와 배색 재킷 구별. 글자·색·수여 자격은 해당 학교 사례로 제한한다.
- 관찰 게이트: 편직 몸판과 단일 패치의 테두리·부착면이 보인다.
- 제안 슬롯: wardrobe_style, garment_detail, visible_text; 출처: S10, S12

## W03 후디, 집업 후디, 크루넥 스웨트셔츠

- 유형: observable / P1
- 한글: 지퍼가 없는 스웨트셔츠의 둥근 골지 목둘레는 이어진 앞 몸판 위에 놓이고 뒤쪽 후드는 없다.
- English: A zipless sweatshirt has a round ribbed neckline above one continuous front panel, with no hood behind the neck.
- 관계: neck_ribbing → bounds → neck_opening; front_panel → continuous_below → neck_opening
- 혼동 경계: 이 카드는 크루넥 표본이다. 후디는 부착된 후드, 집업은 열린 지퍼선이 각각 필요하며 같은 뜻으로 라우팅하지 않는다.
- 관찰 게이트: 목 뒤와 앞 몸판을 함께 보여 후드·지퍼 유무를 판별한다.
- 제안 슬롯: wardrobe_style, garment_detail; 출처: S09

## W04 옥스퍼드 버튼다운 셔츠, OCBD

- 유형: observable / P0
- 한글: 셔츠의 두 깃 끝이 각각 작은 단추로 앞 몸판에 고정되고 중앙 여밈은 별도 단추 줄로 이어진다.
- English: Each collar tip of a shirt fastens to the front panel with a small button, separate from the central placket buttons.
- 관계: left_collar_tip → fastened_to → left_front_panel; right_collar_tip → fastened_to → right_front_panel; placket → between → front_panels
- 혼동 경계: button-down은 깃 끝 고정과 관련된다. 모든 앞단추 셔츠를 OCBD로 부르거나 직물 조직을 멀리서 확정하지 않는다.
- 관찰 게이트: 두 깃 단추와 중앙 여밈이 분리되어 보인다.
- 제안 슬롯: garment_detail, wardrobe_style; 출처: S09

## W05 폴로 셔츠, 럭비 셔츠

- 유형: observable / P1
- 한글: 폴로 셔츠의 부드러운 접힌 깃 아래에 짧은 단추 여밈이 있고 몸판의 아래쪽은 이어진다.
- English: A polo shirt has a soft folded collar and a short button placket above a continuous lower torso panel.
- 관계: collar → above → short_placket; short_placket → ends_above → continuous_lower_panel
- 혼동 경계: 럭비 셔츠의 소재·긴 소매·가로 줄무늬는 별도 선택이며 모든 폴로의 필수 요소가 아니다.
- 관찰 게이트: 짧은 여밈의 끝과 이어지는 몸판을 보인다.
- 제안 슬롯: wardrobe_style, garment_detail; 출처: S10

## W06 블레이저, 트위드 재킷, 프레피, 아이비 스타일

- 유형: observable / P1
- 한글: 라펠 재킷 안에 셔츠가 있고 칼라 끝과 재킷 라펠 사이 경계가 각각 드러난다.
- English: A lapelled jacket lies over a shirt, with the shirt collar tips distinct from the jacket lapels.
- 관계: jacket → over → shirt; lapels → part_of → jacket; collar_tips → part_of → shirt
- 혼동 경계: 트위드는 직물이고 블레이저는 재킷 계열이다. 부·학벌·성적·dark academia 서사를 옷으로 확정하지 않는다.
- 관찰 게이트: 셔츠·재킷의 두 옷 경계와 깃 귀속이 보인다.
- 제안 슬롯: wardrobe_layering, wardrobe_style; 출처: S09, S11

## W07 카디건, 니트 베스트, 케이블 니트, 아가일 니트

- 유형: observable / P1
- 한글: 소매 없는 니트 베스트의 암홀이 안쪽 셔츠 소매를 둘러싸고 베스트 V넥은 셔츠 깃 아래로 내려온다.
- English: The armholes of a sleeveless knitted vest surround the shirt sleeves beneath it, and its V-neck descends below the shirt collar.
- 관계: vest → over → shirt; armholes → bound → shirt_sleeve_roots; vest_vneck → below → shirt_collar
- 혼동 경계: 베스트의 소매 없음과 카디건의 앞열림을 구별한다. 케이블은 편직 구조·아가일은 문양으로 별도 속성이다.
- 관찰 게이트: 두 암홀·셔츠 소매·V넥·독립 밑단이 보인다.
- 제안 슬롯: wardrobe_layering, garment_detail; 출처: S09

## W08 치노, 슬랙스, 스트레이트 데님, 와이드 데님

- 유형: observable / P1
- 한글: 허리에서 두 바지통이 갈라지고 넓은 두 밑단은 각각의 신발 위로 떨어진다.
- English: Two trouser legs separate below the waistband, with wide hems falling over two separate shoes.
- 관계: left_leg → ends_above → left_shoe; right_leg → ends_above → right_shoe; legs → join_at → waistband
- 혼동 경계: 이 카드는 와이드 실루엣 표본이다. 치노·슬랙스·데님 직물·직선통은 별도 축으로 심사한다.
- 관찰 게이트: 허리부터 두 다리·밑단·신발까지 보여 통 폭과 분리를 확인한다.
- 제안 슬롯: garment_fit, silhouette_proportion; 출처: S09

## W09 플리츠 스커트, 테니스 스커트, 미니, 미디, 맥시

- 유형: observable / P1
- 한글: 한 치마의 반복 주름이 허리에서 밑단으로 내려가고 그 밑단은 착용자의 무릎 위에 놓인다.
- English: Repeated pleats descend from one skirt waistband to a hem above the wearer's knees.
- 관계: pleats → descend_from → waistband; hem → above → wearer_knees; skirt → worn_by → A
- 혼동 경계: 주름 구조·길이·운동 용도는 독립 축이다. 테니스 스커트가 항상 실제 경기복·속바지 일체형은 아니다.
- 관찰 게이트: 허리·주름·양 무릎을 함께 보여 길이를 상대적으로 평가한다.
- 제안 슬롯: garment_detail, silhouette_proportion; 출처: S09, S11

## W10 오버사이즈, 레이어링, 애슬레저, 놈코어, 스트리트웨어

- 유형: observable / P1
- 한글: 같은 착용자의 바깥 재킷 어깨 봉제선이 실제 어깨보다 바깥에 있고 안쪽 티셔츠 밑단은 재킷 아래에 드러난다.
- English: The outer jacket's shoulder seams sit beyond the same wearer's shoulders, while an inner tee hem shows below the jacket.
- 관계: jacket → worn_by → A; shoulder_seams → outside → A_shoulders; tee → under → jacket; tee_hem → below → jacket_hem; A_shoulders → belongs_to → A
- 혼동 경계: 오버사이즈의 상대 치수와 레이어의 별도 경계를 구별한다. 거리 패션·성격·사회 계층을 자동 판정하지 않는다.
- 관찰 게이트: 실제 어깨·봉제선·두 밑단이 보인다.
- 제안 슬롯: garment_fit, wardrobe_layering; 출처: S09

## W11 크롭트 톱, 크롭톱

- 유형: observable / P1
- 한글: 한 상의의 밑단이 같은 착용자의 허리선 위에서 끝나며 아래 바지 허리단과 간격이 보인다.
- English: A top ends above the same wearer's waist, with a visible gap above the trouser waistband.
- 관계: top → worn_by → A; top_hem → above → A_waist; trouser_waistband → below → top_hem; A_waist → belongs_to → A
- 혼동 경계: 짧은 길이와 꼭 맞는 핏은 별개다. 노출·옷차림은 성적 의도·동의를 증명하지 않는다.
- 관찰 게이트: 상의 밑단·신체 허리선·하의 허리단을 함께 보인다.
- 제안 슬롯: silhouette_proportion, garment_detail; 출처: S18

## W12 베이비 티, Baby tee

- 유형: observable / P1
- 한글: 성인 착용자의 짧은 소매 티셔츠가 몸통 윤곽을 따라 붙고 둥근 목둘레와 별도 밑단이 보인다.
- English: An adult wears a short-sleeved tee fitted along the torso, with a round neckline and a distinct hem.
- 관계: tee → worn_by → A; sleeves → part_of → tee; tee → follows → A_torso; A_torso → belongs_to → A
- 혼동 경계: baby는 착장명이지 아동 모델 요구가 아니다. 짧은 길이는 별도 결정하며 정확한 역사·유행은 추가 출처가 필요하다.
- 관찰 게이트: 성인 인물 맥락과 소매·목둘레·핏·밑단을 확인한다.
- 제안 슬롯: garment_fit, wardrobe_style; 출처: S18

## W13 오프숄더

- 유형: observable / P1
- 한글: 상의 목둘레가 성인 착용자의 양 어깨 바깥쪽 아래를 지나고 두 소매는 위팔에 걸린다.
- English: A top's neckline runs below an adult wearer's exposed shoulders, with both sleeves resting on the upper arms.
- 관계: neckline → below → A_shoulders; sleeves → rest_on → A_upper_arms; A_shoulders → belongs_to → A; A_upper_arms → belongs_to → A
- 혼동 경계: 한쪽 소매가 우연히 내려간 상태와 설계된 양쪽 neckline을 구별한다. 동의·관계 추론 금지다.
- 관찰 게이트: 양 어깨·목둘레 연속선·소매의 귀속이 보인다.
- 제안 슬롯: garment_detail, wardrobe_style; 출처: S18

## W14 홀터넥

- 유형: observable / P1
- 한글: 성인의 상의 끈 두 갈래가 가슴 위에서 목 뒤로 이어지고 양 어깨 바깥쪽에는 끈이 없다.
- English: Two straps of an adult's top rise from the bodice to behind the neck, leaving the outer shoulders free of straps.
- 관계: straps → from → bodice; straps → continue_behind → A_neck; top → worn_by → A; A_neck → belongs_to → A
- 혼동 경계: 캐미솔의 어깨끈과 목 둘레 지지 경로를 구별한다. 뒤가 가리면 매듭 방식은 통과할 수 없다.
- 관찰 게이트: 앞 몸판에서 목 뒤까지 지지 경로가 보인다.
- 제안 슬롯: garment_detail, wardrobe_style; 출처: S18

## W15 시어, 시스루

- 유형: observable / P1
- 한글: 성인의 바깥 소매 천을 통해 안쪽의 불투명 긴소매 윤곽이 보이고 두 옷의 소맷단은 떨어져 있다.
- English: An opaque inner sleeve remains visible through an adult's sheer outer sleeve, with separate cuffs for the two garments.
- 관계: sheer_sleeve → over → opaque_sleeve; outer_cuff → separate_from → inner_cuff
- 혼동 경계: 투명도는 광학 성질이며 레이스·망사·노출·란제리와 동의어가 아니다.
- 관찰 게이트: 천 경계·안쪽 옷의 지속성·별도 커프가 보인다.
- 제안 슬롯: material_thickness, wardrobe_layering; 출처: S25, S26, S18

## W16 레이스, 피시넷, 망사

- 유형: observable / P1
- 한글: 성인 착용자의 소매 끝에 꽃 모양 실망과 그 사이 빈 구멍이 반복되며 안쪽 안감은 소매 본체에서 끝난다.
- English: Floral threadwork and intervening openings repeat along an adult wearer's lace cuff, while the inner lining ends at the sleeve body.
- 관계: lace → attached_to → sleeve_end; openings → between → threadwork; lining → ends_at → sleeve_body
- 혼동 경계: 레이스 꽃망·규칙적 피시넷 격자·단순 투명천은 다른 구조다. 원 유물과 같은 재료·시대라는 주장은 하지 않는다.
- 관찰 게이트: 실 조직·구멍·안감 끝의 서로 다른 경계가 보인다.
- 제안 슬롯: surface_pattern, garment_detail; 출처: S25, S26

## W17 캐미솔

- 유형: observable / P1
- 한글: 성인의 상의 몸판이 두 가는 어깨끈에 매달리고 밑단은 하의 위에서 별도 상의로 끝난다.
- English: An adult's top is supported by two narrow shoulder straps, and its hem ends separately above the lower garment.
- 관계: strap_left → supports → bodice; strap_right → supports → bodice; top_hem → separate_from → lower_garment
- 혼동 경계: 이 표본은 별도 상의다. 슬립 드레스의 길이와 스커트 연결, 홀터의 목 지지 경로와 구별한다.
- 관찰 게이트: 두 어깨끈·몸판·끝나는 밑단이 보인다.
- 제안 슬롯: wardrobe_style, garment_detail; 출처: S25, S26, S18

## W18 슬립 드레스, 란제리 룩

- 유형: observable / P1
- 한글: 성인의 두 어깨끈이 가슴 몸판을 지지하고 같은 옷이 허리 아래 치마까지 연속해서 내려온다.
- English: Two shoulder straps support an adult's bodice, and the same garment continues below the waist into a skirt.
- 관계: straps → support → bodice; bodice → continuous_with → skirt; dress → worn_by → A
- 혼동 경계: 슬립 드레스·속옷 슬립·란제리풍 스타일은 용도·소재·맥락을 따로 확인한다. 소장품 텍스트는 모든 현대 재단의 근거가 아니다.
- 관찰 게이트: 끈-몸판-허리-치마의 연속성이 보인다.
- 제안 슬롯: wardrobe_style, garment_detail; 출처: S25, S26, S18

## W19 뷔스티에

- 유형: observable / P1
- 한글: 성인의 상체를 감싸는 별도 몸판에 세로 패널 봉제선이 있고 밑단은 하의와 분리된다.
- English: A separate adult torso garment has vertical panel seams and a hem distinct from the lower garment.
- 관계: panel_seams → on → torso_garment; garment_hem → separate_from → lower_garment
- 혼동 경계: 외형 예만 제안한다. boning·내부 지지·조임·코르셋 기능·정확한 뷔스티에 정의는 표본 추가 전 보류한다.
- 관찰 게이트: 분리된 몸판·세로 봉제선·밑단만 평가하고 내부 지지는 UNSCORED다.
- 제안 슬롯: garment_detail, wardrobe_style; 출처: S26

## W20 보디콘, Bodycon

- 유형: observable / P1
- 한글: 성인의 드레스가 몸통과 엉덩이 윤곽을 따라 붙고 하나의 옷 밑단까지 이어진다.
- English: An adult's dress follows the torso and hip contours closely and continues to one garment hem.
- 관계: dress → worn_by → A; dress → follows → A_torso_and_hips; dress → continuous_to → hem; A_torso_and_hips → belongs_to → A
- 혼동 경계: 보디콘은 핏이며 반드시 짧음·시스루·특정 동의 상태를 뜻하지 않는다.
- 관찰 게이트: 몸-천 경계와 연속 드레스·밑단을 보인다.
- 제안 슬롯: garment_fit, silhouette_proportion; 출처: S18, S26

## W21 타이츠, 스타킹, 니삭스, 오버니

- 유형: observable / P1
- 한글: 성인의 긴 양말 두 짝은 각각 무릎 위의 독립된 상단 띠에서 끝나고 치마 밑단과 간격이 있다.
- English: An adult wears two separate over-knee socks, each ending in its own band above the knee with a gap below the skirt hem.
- 관계: sock_left → ends_above → A_left_knee; sock_right → ends_above → A_right_knee; bands → below → skirt_hem; A_left_knee → belongs_to → A; A_right_knee → belongs_to → A
- 혼동 경계: 이 카드는 오버니 표본이다. 허리까지 연결된 타이츠·허벅지 스타킹·무릎 아래 니삭스는 별도 후보로 분리한다.
- 관찰 게이트: 양 무릎·두 상단·치마 밑단을 함께 보인다.
- 제안 슬롯: garment_detail, silhouette_proportion; 출처: S16, S18

## W22 로퍼, 메리제인, 스니커즈, 캔버스화

- 유형: observable / P1
- 한글: 낮은 신발의 발등을 가로지르는 스트랩이 신발 옆 버클로 이어지고 발은 그 안에 놓인다.
- English: A strap crosses the instep of a low shoe and joins a side buckle, with the wearer's foot inside the shoe.
- 관계: strap → crosses → instep; strap → joins → side_buckle; foot → inside → shoe
- 혼동 경계: 메리제인의 한 표본이다. 로퍼의 무끈 구조·스니커즈의 고무창·캔버스 소재를 같은 분류로 합치지 않는다.
- 관찰 게이트: 발등 스트랩-측면 버클-신발 몸체의 연결이 보인다.
- 제안 슬롯: footwear, garment_detail; 출처: S09

## W23 실험복, 보호안경, 장갑

- 유형: observable / P0
- 한글: 성인이 앞을 잠근 실험복과 눈을 덮은 보안경·장갑을 착용하고 소매 끝과 장갑 사이 손목 피부가 드러나지 않는다.
- English: An adult wears a closed lab coat, protective eyewear over the eyes and gloves, with no exposed wrist gap between cuff and glove.
- 관계: coat → worn_by → A; eyewear → over → A_eyes; gloves → cover → A_hands; coat_cuffs → meet → glove_cuffs; A_eyes → belongs_to → A; A_hands → belongs_to → A
- 혼동 경계: 해당 기관 촬영 지침의 실현안이다. 위험별 장비 선택·실제 안전성은 사진만으로 인증하지 않는다. 열린 가운 후보와 구분한다.
- 관찰 게이트: 앞 잠금·눈 보호·양 손목 경계가 함께 보인다.
- 제안 슬롯: wardrobe_layering, wearable_accessory, garment_state; 출처: S14, S15

## W24 스크럽, Scrubs, 작업 앞치마, 커버올

- 유형: observable / P1
- 한글: 성인의 앞치마 몸판은 가슴 앞을 덮고 목끈과 허리끈이 각각 몸판 위·옆에 붙어 안쪽 옷은 별개로 보인다.
- English: An adult's apron panel covers the chest, with a neck loop and waist ties attached at separate points over distinct inner clothing.
- 관계: neck_loop → attached_to → apron_top; waist_ties → attached_to → apron_sides; apron → over → inner_clothes
- 혼동 경계: 이 카드는 앞치마 표본이다. 의료 스크럽의 분리된 상하의·커버올 일체형은 별도 고증 대상으로 남긴다.
- 관찰 게이트: 몸판·목·허리 지지 경로와 안쪽 옷 경계가 보인다.
- 제안 슬롯: wardrobe_layering, garment_detail; 출처: S13, S15

## W25 트레이닝웨어, 팀 유니폼, 응원복, 무대 의상

- 유형: staged_proxy / P1
- 한글: 성인 두 명의 운동 상의에 서로 다른 큰 등번호가 있고 각자의 반바지 옆선은 같은 배색 띠로 이어진다.
- English: Two adults wear sports tops with different large back numbers and shorts with matching side stripes.
- 관계: number_A → on → A_top; number_B → on → B_top; stripe_A → on → A_shorts; stripe_B → on → B_shorts; A_shorts → belongs_to → A; A_top → belongs_to → A; B_shorts → belongs_to → B; B_top → belongs_to → B
- 혼동 경계: 종목·학교 대표 자격·승리·응원단 직책은 별도 맥락이다. 무대 의상을 모든 운동복과 합치지 않는다.
- 관찰 게이트: 두 착용자·각 등번호·상의/하의 소유가 구별된다.
- 제안 슬롯: wardrobe_style, visible_text; 출처: S10, S12

## W26 발표복, 면접복, 스마트 캐주얼

- 유형: staged_proxy / P1
- 한글: 성인의 재킷이 셔츠 위에 놓이고 바지 두 다리와 닫힌 신발이 보이며 손에는 별도 서류철을 든다.
- English: An adult wears a jacket over a shirt with two trouser legs and closed shoes, holding a separate document folder.
- 관계: jacket → over → shirt; folder → held_by → A_hand; trousers → worn_by → A; A_hand → belongs_to → A
- 혼동 경계: 정장 외형이 실제 면접·채용·전공·평가권을 입증하지 않는다.
- 관찰 게이트: 의복 층·양 다리·서류철과 손의 귀속이 보인다.
- 제안 슬롯: wardrobe_style, prop; 출처: S30

## W27 학위복, 아카데믹 가운, 학위 후드, 학사모

- 유형: observable / P0
- 한글: 성인의 긴 가운은 정장 위로 내려오고 별도 후드가 어깨 뒤에 놓이며 네모난 모자판 아래 머리가 분리되어 보인다.
- English: An adult's long gown falls over formal clothes, with a separate hood behind the shoulders and a square cap board above the head.
- 관계: gown → over → formal_clothes; hood → behind → A_shoulders; cap_board → above → A_head; A_head → belongs_to → A; A_shoulders → belongs_to → A
- 혼동 경계: 학교·학위별 후드/모자 변형이 있다. 모든 학위복의 필수 조합으로 고정하거나 학위 취득 사실을 외형으로 인증하지 않는다.
- 관찰 게이트: 가운·후드·모자·머리의 별도 경계가 보인다.
- 제안 슬롯: wardrobe_layering, wearable_accessory; 출처: S16

## W28 서브 푸스크, Sub fusc

- 유형: observable / P0
- 한글: 성인의 흰 깃 셔츠와 검은 목 매듭·어두운 바지가 검은 학위 가운 안쪽에 따로 드러난다.
- English: An adult's white collared shirt, black neck tie and dark trousers remain distinct beneath a black academic gown.
- 관계: shirt → under → gown; neck_tie → below → shirt_collar; trousers → under → gown
- 혼동 경계: Oxford 규정의 선택적 한 조합이다. sub fusc를 가운 자체·검은 평상복·전 세계 대학 교복으로 정의하지 않는다.
- 관찰 게이트: 가운 안쪽의 셔츠·목 매듭·바지 층이 분리되어 보인다.
- 제안 슬롯: wardrobe_layering, attire_context; 출처: S16

## W29 라운지웨어, 파자마, 베드헤드

- 유형: staged_proxy / P1
- 한글: 성인의 느슨한 앞단추 상의가 같은 천의 긴 바지 위에 놓이고 접힌 담요가 의자에 걸려 있다.
- English: An adult's loose button-front top lies over matching long trousers, with a folded blanket over a chair.
- 관계: top → worn_by → A; trousers → worn_by → A; blanket → over → chair
- 혼동 경계: 잠옷 외형·헝클어진 머리가 수면 이력·동거·성적 사건을 증명하지 않는다.
- 관찰 게이트: 두 옷의 분리와 담요 지지를 확인한다.
- 제안 슬롯: wardrobe_style, garment_fit; 출처: S18, S22

## W30 코케트, 발레코어, 긱 시크, 라이트 아카데미아

- 유형: staged_proxy / P1
- 한글: 성인의 카디건 앞에는 작은 리본 두 개가 붙고 안쪽 티셔츠와 별도 주름 치마가 보인다.
- English: Two small ribbons attach to an adult's cardigan front over a distinct tee and a separate pleated skirt.
- 관계: ribbons → attached_to → cardigan_front; cardigan → over → tee; skirt → separate_from → tee
- 혼동 경계: 스타일 선택 예다. 네 미학의 정의·유행·공통 필수 요소를 이 조합으로 대체하지 않는다. 전문 자료와 표본을 보강하기 전 명칭 승인은 보류한다.
- 관찰 게이트: 리본의 부착·옷 층만 평가하며 미학 분류는 사용자 판단이다.
- 제안 슬롯: aesthetic_trend, wardrobe_layering; 출처: S09, S18

## P01 학생증, 랜야드

- 유형: observable / P1
- 한글: 한 성인의 목끈 양 끝이 카드 홀더 고리에 연결되고 직사각형 카드가 홀더 안에 들어 있다.
- English: Both ends of an adult's lanyard connect to a card-holder loop, with a rectangular card inside the holder.
- 관계: lanyard_ends → connect_to → holder_loop; card → inside → holder; lanyard → around → A_neck; A_neck → belongs_to → A
- 혼동 경계: 카드 모양·학교 로고가 진위·성인 나이·등록 상태를 보증하지 않는다. 개인정보 텍스트와 시각 구조를 분리한다.
- 관찰 게이트: 목끈-고리-홀더-카드의 전체 연결이 보인다.
- 제안 슬롯: wearable_accessory, object_structure; 출처: S03

## P02 백팩, 토트백, 메신저백, 가방끈

- 유형: observable / P1
- 한글: 성인의 한 어깨에서 대각선 끈이 반대쪽 엉덩이의 가방까지 이어지고 손 하나가 그 끈을 잡는다.
- English: A strap runs diagonally from one adult shoulder to a bag at the opposite hip, gripped by one hand.
- 관계: strap → from → A_shoulder; strap → to → bag; bag → beside → A_opposite_hip; hand → belongs_to → A; hand → grips → strap; A_opposite_hip → belongs_to → A; A_shoulder → belongs_to → A
- 혼동 경계: 메신저백의 한 표본이다. 양어깨 백팩·손잡이 토트백은 지지 경로가 다르다. 통학 목적은 별도다.
- 관찰 게이트: 끈 시작-가로지름-가방·손 연결이 보인다.
- 제안 슬롯: prop, contact_point; 출처: S30

## P03 전공책, 제본 자료, 포스트잇, 족보

- 유형: observable / P1
- 한글: 제본된 책의 열린 두 페이지에 밑줄이 있고 서로 다른 세 색의 접착 메모가 책 가장자리에서 나온다.
- English: An open bound book shows underlined pages and three differently colored sticky tabs extending from its edges.
- 관계: pages → bound_in → book; underlines → on → pages; sticky_tabs → attached_to → page_edges
- 혼동 경계: 공개 기출·부정 유출·전공·성적은 책의 외형으로 알 수 없다. 개별 글자 판독은 별도 과제다.
- 관찰 게이트: 제본·페이지·탭의 부착과 세 색을 확인한다.
- 제안 슬롯: prop, visible_text; 출처: S04, S17

## P04 도면통, 포트폴리오 케이스, 포트폴리오

- 유형: observable / P1
- 한글: 성인이 어깨끈에 연결된 단단한 원통 케이스를 옆구리에 메고 위쪽 원형 뚜껑은 본체와 경계가 있다.
- English: An adult carries a rigid cylindrical case on a shoulder strap, with a circular top cap distinct from the tube body.
- 관계: strap → connects_to → case; case → beside → A_torso; cap → joins → tube_top; A_torso → belongs_to → A
- 혼동 경계: 도면통·평평한 포트폴리오 케이스를 구별한다. 내용물·전공·작품 수준은 닫힌 통에서 입증되지 않는다.
- 관찰 게이트: 끈-통 부착과 캡-몸체 경계가 보인다.
- 제안 슬롯: prop, object_structure; 출처: S13

## P05 악기 케이스, 악보, 대본

- 유형: observable / P1
- 한글: 열린 케이스의 성형 홈 안에 악기가 놓이고 별도의 보면대에는 펼친 악보가 놓인다.
- English: An instrument rests in the shaped recess of an open case, while a separate stand holds open sheet music.
- 관계: instrument → inside → case_recess; sheet_music → supported_by → stand
- 혼동 경계: 케이스 모양만으로 악기 모델·실제 연주·소리·배역을 확정하지 않는다.
- 관찰 게이트: 악기-내부 홈·악보-받침의 두 지지 관계가 보인다.
- 제안 슬롯: prop, prop_placement; 출처: S06, S10

## P06 텀블러, 테이크아웃 컵, 야식, 생활 흔적

- 유형: observable / P1
- 한글: 탁자에 서로 다른 컵 두 개가 있고 컵 하나는 열린 교재 옆에, 다른 하나는 빈 의자 앞에 놓인다.
- English: Two distinct cups sit on a table, one beside an open book and the other before an empty chair.
- 관계: cup_A → beside → book; cup_B → in_front_of → empty_chair; cups → on → table
- 혼동 경계: 두 컵은 두 사람의 동거·연애·부재·방문 이력을 증명하지 않는다.
- 관찰 게이트: 두 컵·교재·빈 의자와 각각의 위치가 구별된다.
- 제안 슬롯: narrative_clue, prop_placement; 출처: S30

## P07 단톡방, 익명 커뮤니티, 사이버불링

- 유형: observable / P0
- 한글: 노트북 화면 안에 분리된 별명 행과 답글 행이 있고 화면 테두리 밖의 방에는 실제 인물 한 명만 있다.
- English: Separate alias and reply rows remain inside a laptop screen, while only one physical person occupies the room outside the screen.
- 관계: reply_rows → inside → screen; screen → part_of → laptop; A → outside → screen
- 혼동 경계: 화면 속 발신자와 실제 인물을 중복 생성하지 않는다. 괴롭힘의 반복·동일인·악의는 텍스트와 맥락이 필요하다.
- 관찰 게이트: 스크린 경계·행 구조·방 안 인물 수를 확인한다.
- 제안 슬롯: visible_text, prop, composition; 출처: S17, S18

## P08 포니테일, 하프업, 메시 번, 내추럴 메이크업, 다크서클, 번진 메이크업

- 유형: observable / P1
- 한글: 성인의 뒤통수에서 모은 머리 한 묶음이 고무줄 하나를 지나 아래로 이어지고 다른 잔머리는 목 옆에 남는다.
- English: One gathered bundle at an adult's back of head passes through a single elastic into a hanging tail, with loose strands beside the neck.
- 관계: hair_bundle → gathered_at → elastic; tail → continues_from → elastic; loose_strands → beside → A_neck; A_neck → belongs_to → A
- 혼동 경계: 이 카드는 포니테일이다. 하프업·번·메이크업은 별도 형상이며 머리·다크서클로 밤샘·수면·진단을 확정하지 않는다.
- 관찰 게이트: 두피-묶음-고무줄-꼬리의 연결을 확인한다.
- 제안 슬롯: hair_style; 출처: S18

## P09 커플룩, 시밀러 룩, 빌린 과잠, 빌린 후디

- 유형: observable / P1
- 한글: 성인 A와 B가 서로 다른 상의를 입고 두 옷의 소맷단에 같은 색 띠가 각각 나타난다.
- English: Adults A and B wear different tops, each with a matching colored band at its own cuff.
- 관계: top_A → worn_by → A; top_B → worn_by → B; band_A → on → top_A_cuff; band_B → on → top_B_cuff
- 혼동 경계: 같은 색·큰 옷·타 대학 표식은 커플 관계·대여·원소유의 증거가 아니다.
- 관찰 게이트: 두 착용자와 각 옷·띠 귀속이 구별된다.
- 제안 슬롯: character_contrast, garment_detail; 출처: S08, S18

## A01 가방끈을 잡고 걷기

- 유형: observable / P1
- 한글: A의 오른손은 같은 사람 오른어깨의 백팩 끈을 잡고 왼발은 오른발보다 앞에 놓인다.
- English: A's right hand grips the backpack strap on A's right shoulder, with the left foot ahead of the right foot.
- 관계: right_hand → belongs_to → A; right_hand → grips → backpack_strap; strap → over → A_right_shoulder; left_foot → ahead_of → right_foot; A_right_shoulder → belongs_to → A
- 혼동 경계: 보폭 외형과 실제 보행·등교·긴장은 별개다. 반대 사람 손을 붙이지 않는다.
- 관찰 게이트: 손-손목-팔·끈·어깨와 두 발이 동시에 보인다.
- 제안 슬롯: action, contact_point, body_pose; 출처: S30

## A02 달리다가 뒤돌아보기

- 유형: staged_proxy / P1
- 한글: A의 몸통과 앞 무릎은 진행 방향을 향하고 머리는 어깨 너머 뒤쪽으로 돌며 뒤꿈치 하나가 바닥에서 떨어져 있다.
- English: A's torso and front knee face forward while the head turns over a shoulder and one heel lifts off the ground.
- 관계: head → turns_over → A_shoulder; torso → faces → forward_direction; heel → above → ground; A_shoulder → belongs_to → A
- 혼동 경계: 스틸은 달리기 속도·이전 동작·누가 불렀는지를 증명하지 않는다.
- 관찰 게이트: 목 연결·몸통/머리 방향 차이·지면 발 간격이 보인다.
- 제안 슬롯: body_orientation, physical_motion; 출처: S30

## A03 턱 괴고 강의 듣기

- 유형: observable / P1
- 한글: A의 턱이 A의 한 손바닥 위에 놓이고 같은 팔꿈치가 책상에 지지되며 다른 손은 책 옆에 있다.
- English: A's chin rests on A's palm, the same elbow supported by the desk, while the other hand lies beside a book.
- 관계: palm → belongs_to → A; chin → supported_by → palm; elbow → supported_by → desk; other_hand → beside → book
- 혼동 경계: 기존 볼 지지 후보와 턱 접촉을 구별한다. 집중·지루함·실제 강의 청취는 자세만으로 알 수 없다.
- 관찰 게이트: 턱-손바닥·손목-팔꿈치·책상 접점이 보인다.
- 제안 슬롯: body_pose, contact_point; 출처: S30

## A04 필기하며 옆눈질하기

- 유형: observable / P1
- 한글: A의 한 손은 펼친 공책 위 연필을 잡고 A의 눈동자는 옆자리 B 쪽을 향한다.
- English: A holds a pencil above an open notebook while A's pupils point toward adjacent B.
- 관계: hand → belongs_to → A; hand → holds → pencil; pencil → above → notebook; A_pupils → directed_toward → B; A_pupils → belongs_to → A
- 혼동 경계: 짝사랑·경쟁·부정행위·실제 필기의 시간 진행은 별도다.
- 관찰 게이트: 손·연필·공책과 눈 방향·B 위치가 동시에 보인다.
- 제안 슬롯: gaze_target, hand_pose, action; 출처: S17

## A05 책상에 엎드리기

- 유형: observable / P1
- 한글: 앉은 A의 이마가 책상 위 포갠 두 팔뚝에 닿고 A의 두 다리가 의자 앞에서 바닥에 이어진다.
- English: Seated A rests the forehead on crossed forearms on a desk, with both legs extending to the floor before the chair.
- 관계: forehead → contacts → A_forearms; forearms → supported_by → desk; A → supported_by → chair; feet → on → floor; A_forearms → belongs_to → A
- 혼동 경계: 수면·밤샘·소진·질병·성적 원인은 외형과 분리한다.
- 관찰 게이트: 머리·양팔 귀속·의자·두 발의 지지를 확인한다.
- 제안 슬롯: body_pose, contact_point; 출처: S30

## A06 기지개, 목과 어깨 풀기

- 유형: observable / P1
- 한글: A의 두 팔은 머리 위로 올라가고 두 손의 손가락은 서로 깍지 낀 채 손바닥이 위를 향한다.
- English: A raises both arms above the head, interlacing the fingers with palms facing upward.
- 관계: arms → belong_to → A; hands → above → A_head; fingers → interwoven_with → opposite_hand_fingers; A_head → belongs_to → A
- 혼동 경계: 편안함·오래 공부함·스트레칭의 실제 횟수는 정지 포즈만으로 입증되지 않는다.
- 관찰 게이트: 두 어깨에서 손목까지 경로와 손가락 분리가 보인다.
- 제안 슬롯: body_pose, hand_pose; 출처: S30

## A07 서가의 책에 손 뻗기

- 유형: observable / P1
- 한글: A의 오른팔이 위로 뻗어 손끝이 윗선반 책등에 닿고 A의 왼손은 아래 선반 끝을 짚는다.
- English: A reaches upward with the right fingertips touching a book spine while the left hand rests on a lower shelf edge.
- 관계: right_fingertips → belong_to → A; right_fingertips → contact → book_spine; left_hand → belongs_to → A; left_hand → contacts → lower_shelf
- 혼동 경계: 도움·친밀감·키 차이·실제 대출은 별도다. 선반의 실제 하중 지지는 점검 대상이다.
- 관찰 게이트: 두 팔의 주인·손끝-책·손-선반 접점이 보인다.
- 제안 슬롯: action, contact_point, gaze_target; 출처: S24

## A08 책을 가슴 앞에 안기

- 유형: observable / P1
- 한글: A의 양팔은 책 더미를 가슴 앞에서 받치고 책의 아래 모서리는 A의 팔뚝 위에 놓인다.
- English: A holds stacked books before the chest, their lower edges supported by A's forearms.
- 관계: books → supported_by → A_forearms; books → in_front_of → A_chest; hands → belong_to → A; A_chest → belongs_to → A; A_forearms → belongs_to → A
- 혼동 경계: 방어·수줍음·학생 신원은 소품과 포즈만으로 확정하지 않는다.
- 관찰 게이트: 책 수·팔뚝 지지·손목 연결을 확인한다.
- 제안 슬롯: body_pose, prop_placement; 출처: S24

## A09 잔디밭에 앉거나 눕기

- 유형: observable / P1
- 한글: A가 잔디 위에 앉아 한 무릎을 세우고 뒤쪽의 두 손바닥이 지면에 닿아 몸통을 지지한다.
- English: A sits on grass with one knee raised, both palms on the ground behind supporting the torso.
- 관계: A_hips → on → grass; palms → belong_to → A; palms → support → A_torso; A_hips → belongs_to → A; A_torso → belongs_to → A
- 혼동 경계: 이 표본은 앉기이며 눕기는 별도 지지 구조다. 공강·평온·데이트는 맥락이 필요하다.
- 관찰 게이트: 엉덩이·손바닥·발의 지면 접점과 팔 귀속이 보인다.
- 제안 슬롯: body_pose, contact_point; 출처: S30

## A10 벤치 끝에 걸터앉기

- 유형: observable / P1
- 한글: A의 엉덩이가 벤치 좌판 끝에 놓이고 양발은 바닥에 닿으며 좌판의 나머지 공간이 비어 있다.
- English: A sits on the end of a bench seat with both feet on the ground and the remaining seat empty.
- 관계: A_hips → supported_by → bench_end; A_feet → on → ground; empty_seat → beside → A; A_feet → belongs_to → A; A_hips → belongs_to → A
- 혼동 경계: 떠날 예정·기다림·이별·고립의 원인은 이 배치의 확정 사실이 아니다.
- 관찰 게이트: 좌판 끝·체중 지지·두 발·빈 좌석을 함께 보인다.
- 제안 슬롯: body_pose, composition; 출처: S30

## A11 이어폰·헤드폰 한쪽 벗기

- 유형: observable / P1
- 한글: A의 손이 같은 사람 오른쪽 헤드폰 컵을 귀 바깥으로 벌리고 왼쪽 컵은 왼귀를 덮는다.
- English: A's hand pulls A's right headphone cup away from the ear while the left cup remains over the left ear.
- 관계: hand → belongs_to → A; hand → grips → right_earcup; right_earcup → away_from → A_right_ear; left_earcup → over → A_left_ear; A_left_ear → belongs_to → A; A_right_ear → belongs_to → A
- 혼동 경계: 실제 음악·상대 말 청취·관심 변화는 스틸로 증명하지 않는다.
- 관찰 게이트: 두 귀·각 컵·손의 연결과 오른쪽 공기 틈을 보인다.
- 제안 슬롯: hand_pose, contact_point; 출처: S30

## A12 휴대전화를 보다가 고개 들기

- 유형: staged_proxy / P1
- 한글: A의 손은 허리 앞 전화기를 잡고 A의 얼굴과 눈은 앞에 선 B를 향한다.
- English: A holds a phone before the waist while A's face and eyes point toward standing B.
- 관계: phone → held_by → A_hand; A_face → directed_toward → B; A_eyes → directed_toward → B; A_eyes → belongs_to → A; A_face → belongs_to → A; A_hand → belongs_to → A
- 혼동 경계: 이전 전화 확인·소식 내용·도착 순간은 시간 자료가 필요하다.
- 관찰 게이트: 전화기 위치·손의 주인·시선 종단 B가 보인다.
- 제안 슬롯: gaze_target, prop_placement; 출처: S30

## A13 한 노트북 화면을 함께 보기, 팀플

- 유형: observable / P0
- 한글: A와 B가 탁자 같은 쪽에 앉아 하나의 열린 노트북 화면으로 눈과 상체를 향한다.
- English: A and B sit on the same side of a table, directing their eyes and upper bodies toward one open laptop screen.
- 관계: A_gaze → toward → laptop_screen; B_gaze → toward → laptop_screen; laptop → on → table; A → beside → B; A_gaze → belongs_to → A; B_gaze → belongs_to → B
- 혼동 경계: 한 화면 공유와 협업 기여·팀플 관계·연애는 별개다. 기기 둘이나 화면 뒤를 보는 시선은 실패다.
- 관찰 게이트: 두 눈의 방향·공통 화면·단일 노트북·손의 귀속이 함께 보인다.
- 제안 슬롯: relational_action, gaze_target, proxemics; 출처: S13, S24

## A14 도면 위로 상체 기울이기

- 유형: observable / P0
- 한글: 탁자 맞은편 A와 B의 상체가 같은 펼친 도면 쪽으로 기울고 A 손끝은 도면 왼쪽 선에 닿는다.
- English: Across a table A and B lean toward the same open drawing, with A's fingertip touching a line on its left side.
- 관계: A_torso → leans_toward → drawing; B_torso → leans_toward → drawing; A_fingertip → contacts → drawing_line; drawing → on → table; A_fingertip → belongs_to → A; A_torso → belongs_to → A; B_torso → belongs_to → B
- 혼동 경계: 협력·라이벌·마감·전공은 구도와 별개 맥락이다.
- 관찰 게이트: 두 몸통 방향·한 도면·손끝 종단·탁자 지지를 보인다.
- 제안 슬롯: relational_action, contact_point; 출처: S13

## A15 작업물의 한 부분을 손가락으로 짚기

- 유형: observable / P1
- 한글: A의 오른손 검지가 탁자 위 모형의 한 모서리를 가리키고 나머지 손가락은 모형에서 떨어져 있다.
- English: A's right index finger points toward one corner of a model on a table, with the remaining fingers clear of the model.
- 관계: index_finger → belongs_to → A; index_finger → points_toward → model_corner; model → on → table
- 혼동 경계: 접촉과 가리킴을 구별한다. 비난·의견 차이·오류 발견은 포즈만으로 확정되지 않는다.
- 관찰 게이트: 손목의 주인·검지 방향·대상 모서리·비접촉 틈이 보인다.
- 제안 슬롯: hand_pose, gaze_target; 출처: S13

## A16 화이트보드 앞에서 설명하기, 세미나

- 유형: observable / P1
- 한글: A가 보드 옆에서 보드의 한 도형을 손으로 가리키고 앉은 B와 C는 보드를 향한다.
- English: A stands beside a board pointing at one diagram while seated B and C face the board.
- 관계: A_hand → points_toward → diagram; diagram → on → board; B → faces → board; C → faces → board; A_hand → belongs_to → A
- 혼동 경계: 교수·TA·PI 직책·실제 설명·이해·발화 내용은 별도다.
- 관찰 게이트: 발표자-손-도형과 두 청중의 방향이 보인다.
- 제안 슬롯: relational_action, participant_role; 출처: S13, S23

## A17 열린 손바닥으로 발표하기

- 유형: observable / P1
- 한글: A가 한 팔꿈치를 굽혀 열린 손바닥을 위로 향하고 그 손은 옆의 게시 도면 아래에 놓인다.
- English: A bends one elbow with the open palm facing upward below a displayed drawing beside A.
- 관계: palm → belongs_to → A; palm → faces → upward_direction; palm → below → drawing
- 혼동 경계: 설득력·진실·교수 신분·실제 말은 이 손짓으로 증명하지 않는다.
- 관찰 게이트: 손바닥 면·손목-팔·도면 위치를 확인한다.
- 제안 슬롯: hand_pose, body_pose; 출처: S13

## A18 악보·대본 함께 들여다보기

- 유형: observable / P1
- 한글: A와 B가 각기 한 손으로 펼친 악보의 반대 끝을 잡고 두 얼굴은 같은 페이지를 향한다.
- English: A and B each hold opposite edges of one open score, both faces directed toward the same page.
- 관계: A_hand → holds → score_left_edge; B_hand → holds → score_right_edge; A_face → toward → score; B_face → toward → score; A_face → belongs_to → A; A_hand → belongs_to → A; B_face → belongs_to → B; B_hand → belongs_to → B
- 혼동 경계: 합주 소리·배역·친밀감·암기 여부는 스틸에서 판단하지 않는다.
- 관찰 게이트: 페이지 하나·두 끝의 손·각 손 주인·시선이 보인다.
- 제안 슬롯: relational_action, prop_placement; 출처: S06

## A19 바닥에 앉아 모형·소품 만들기

- 유형: observable / P1
- 한글: A와 B가 바닥의 절단 매트 양편에 앉고 A의 손은 모형 조각 하나를, B의 손은 별도 판을 받친다.
- English: A and B sit on opposite sides of a floor cutting mat, A holding one model piece and B supporting a separate board.
- 관계: A → beside → mat_left; B → beside → mat_right; A_hand → holds → model_piece; B_hand → supports → board; A_hand → belongs_to → A; B_hand → belongs_to → B
- 혼동 경계: 마감·빈곤·실제 제작 시간·공구 사용의 안전성은 별도다. 날 선 도구를 자동 추가하지 않는다.
- 관찰 게이트: 두 사람의 지지·매트·각 손의 물건을 분리해 보인다.
- 제안 슬롯: action, contact_point, prop_placement; 출처: S13

## A20 무대 뒤에서 차례 기다리기

- 유형: staged_proxy / P1
- 한글: A는 닫힌 무대막 옆에 서서 대본을 두 손으로 잡고 막 틈 너머 밝은 무대 바닥이 보인다.
- English: A stands beside a closed stage curtain holding a script with both hands, with bright stage flooring visible through a gap.
- 관계: script → held_by → A_hands; A → beside → curtain; stage_floor → visible_through → curtain_gap; A_hands → belongs_to → A
- 혼동 경계: 차례·대기 시간·긴장·공연 진행은 정지 화면 밖 맥락이다.
- 관찰 게이트: 막-틈-무대 바닥과 A 손-대본 연결을 보인다.
- 제안 슬롯: body_pose, space_condition; 출처: S06

## A21 졸업사진에서 가운·학사모 정리하기

- 유형: observable / P0
- 한글: 성인 B의 손가락이 A의 모자판 앞 모서리를 잡고 A의 두 손은 몸 앞에 떨어져 있다.
- English: Adult B's fingers hold the front edge of A's cap board while A's own hands remain apart before the torso.
- 관계: B_fingers → belong_to → B; B_fingers → contact → A_cap_edge; cap → worn_by → A; A_hands → in_front_of → A_torso; A_cap_edge → belongs_to → A; A_hands → belongs_to → A; A_torso → belongs_to → A; B_fingers → belongs_to → B
- 혼동 경계: B가 모자를 착용한 것으로 혼동하지 않는다. 졸업 사실·연애·정리 전후는 별도다.
- 관찰 게이트: 모자 착용자 A와 손 주인 B·접촉 모서리가 함께 보인다.
- 제안 슬롯: relational_action, contact_point; 출처: S16

## A22 우산 함께 쓰기

- 유형: observable / P1
- 한글: 성인 A의 한 손이 우산대 하나를 잡고 하나의 우산 천이 나란한 A와 B의 머리 위를 덮는다.
- English: Adult A grips one umbrella shaft, and one canopy covers the heads of side-by-side adults A and B.
- 관계: hand → belongs_to → A; hand → grips → shaft; shaft → supports → canopy; canopy → above → A_head; canopy → above → B_head; A_head → belongs_to → A; B_head → belongs_to → B
- 혼동 경계: 호의·연애·동의·완전한 방수는 확정 불가다. 우산 둘이나 B만 덮이면 이 선택의 실패다.
- 관찰 게이트: 단일 우산·손 주인·두 머리와 천의 덮는 범위를 보인다.
- 제안 슬롯: prop, contact_point, proxemics; 출처: S18

## A23 겉옷을 어깨에 걸쳐 주기, 빌린 과잠

- 유형: observable / P0
- 한글: 성인 B의 양손이 재킷 윗모서리를 잡고 소매에 팔을 넣지 않은 A의 양 어깨 위로 재킷이 걸친다.
- English: Adult B holds both upper edges of a jacket draped over adult A's shoulders, with A's arms outside its sleeves.
- 관계: B_hands → belong_to → B; B_hands → hold → jacket_edges; jacket → rests_on → A_shoulders; A_arms → outside → jacket_sleeves; A_arms → belongs_to → A; A_shoulders → belongs_to → A; B_hands → belongs_to → B
- 혼동 경계: 동일 착용자의 옷 당기기와 구별한다. 원소유·대여·연애·보호 의도는 별도 맥락이다.
- 관찰 게이트: B 손-재킷·A 어깨-재킷 지지와 빈 소매가 보인다.
- 제안 슬롯: relational_action, wardrobe_layering, contact_point; 출처: S08, S18

## A24 컵·노트·필기구 건네기

- 유형: observable / P1
- 한글: 성인 A가 한 컵 아래를 받치고 B는 같은 컵의 손잡이를 잡으며 두 손목은 서로 다른 팔로 이어진다.
- English: Adult A supports a cup's base while adult B grips the same cup's handle, each wrist joined to a different arm.
- 관계: A_hand → supports → cup_base; B_hand → grips → cup_handle; A_wrist → connected_to → A_arm; B_wrist → connected_to → B_arm; A_arm → belongs_to → A; A_hand → belongs_to → A; A_wrist → belongs_to → A; B_arm → belongs_to → B; B_hand → belongs_to → B; B_wrist → belongs_to → B
- 혼동 경계: 이 순간은 공동 접촉이다. 전달 방향·수령 완료·호감은 시간과 맥락이 필요하다.
- 관찰 게이트: 컵 하나·손 두 개·바닥/손잡이의 다른 접점과 손목을 보인다.
- 제안 슬롯: relational_action, contact_point; 출처: S18

## A25 손끝이 닿기, 손잡기, 깍지 끼기

- 유형: observable / P0
- 한글: 성인 A 오른손과 B 왼손의 손가락이 번갈아 엇갈리고 두 엄지와 손목은 분리되어 보인다.
- English: Adult A's right and adult B's left fingers interlace alternately, with both thumbs and wrists remaining distinct.
- 관계: A_fingers → interwoven_with → B_fingers; A_right_hand → connected_to → A_arm; B_left_hand → connected_to → B_arm; A_arm → belongs_to → A; A_fingers → belongs_to → A; A_right_hand → belongs_to → A; B_arm → belongs_to → B; B_fingers → belongs_to → B; B_left_hand → belongs_to → B
- 혼동 경계: 이 카드는 깍지 표본이다. 손끝만 닿기·단순 손잡기·관계 전환은 별도다. 동의는 사진 판정 불가다.
- 관찰 게이트: 손가락 교대·두 엄지·손목 소유와 팔 연결이 보인다.
- 제안 슬롯: contact_point, relational_action; 출처: S18

## A26 어깨에 기대기

- 유형: observable / P1
- 한글: 성인 A의 관자가 앉은 성인 B 어깨에 닿고 B의 몸통은 바로 서 있으며 B 양손은 무릎 위에 보인다.
- English: Adult A's temple rests against seated adult B's shoulder while B sits upright with both hands visible in the lap.
- 관계: A_temple → contacts → B_shoulder; B_torso → upright_on → seat; B_hands → on → B_lap; A_temple → belongs_to → A; B_hands → belongs_to → B; B_lap → belongs_to → B; B_shoulder → belongs_to → B; B_torso → belongs_to → B
- 혼동 경계: 위로·피로·신뢰·수면·연애는 접촉과 별개다.
- 관찰 게이트: A 머리-목·B 어깨-몸통·양손의 지지를 보인다.
- 제안 슬롯: contact_point, relational_action; 출처: S18

## A27 무릎베개

- 유형: observable / P0
- 한글: 누운 성인 A의 머리는 앉은 성인 B의 양 허벅지 위에 놓이고 A 몸통은 옆 벤치에 이어진다.
- English: Reclining adult A rests the head across seated adult B's thighs, with A's torso continuing along the bench.
- 관계: A_head → supported_by → B_thighs; A_neck → connects_to → A_torso; A_torso → supported_by → bench; A_head → belongs_to → A; A_neck → belongs_to → A; A_torso → belongs_to → A; B_thighs → belongs_to → B
- 혼동 경계: 무릎에 앉기와 지지 부위가 다르다. 수면·성적 의도·관계·동의를 확정하지 않는다.
- 관찰 게이트: 머리-목-몸통과 B의 허벅지-골반·벤치 지지가 보인다.
- 제안 슬롯: body_pose, contact_point, relational_action; 출처: S18

## A28 이마 맞대기

- 유형: observable / P1
- 한글: 마주 선 두 성인의 이마가 한 접점에서 닿고 두 코와 입술 사이에는 각각 틈이 남는다.
- English: Two facing adults touch at their foreheads, leaving separate gaps between their noses and lips.
- 관계: A_forehead → contacts → B_forehead; A_lips → separated_from → B_lips; A_nose → separated_from → B_nose; A_forehead → belongs_to → A; A_lips → belongs_to → A; A_nose → belongs_to → A; B_forehead → belongs_to → B; B_lips → belongs_to → B; B_nose → belongs_to → B
- 혼동 경계: 입맞춤·성적 관계·안정·화해를 같은 의미로 판정하지 않는다.
- 관찰 게이트: 두 머리의 귀속·이마 접점·코와 입술의 틈을 보인다.
- 제안 슬롯: contact_point, proxemics; 출처: S18

## A29 백허그

- 유형: observable / P0
- 한글: 성인 B가 A 뒤에 서서 양팔로 A의 허리 앞을 감싸고 B의 두 손은 A 배 앞에서 만나며 A 양손은 따로 보인다.
- English: Adult B stands behind A with both arms around A's waist, B's hands meeting before A's abdomen while A's hands remain separate.
- 관계: B → behind → A; B_arms → around → A_waist; B_hands → meet_before → A_abdomen; A_hands → separate_from → B_hands; A_abdomen → belongs_to → A; A_hands → belongs_to → A; A_waist → belongs_to → A; B_arms → belongs_to → B; B_hands → belongs_to → B
- 혼동 경계: 앞 포옹·구속·성적 동의·재회를 한 포즈로 동일화하지 않는다.
- 관찰 게이트: 최소 네 손의 귀속·B 어깨-팔-손·A 몸통을 함께 보인다.
- 제안 슬롯: relational_action, contact_point, proxemics; 출처: S18

## A30 무릎에 앉기

- 유형: observable / P0
- 한글: 성인 A의 골반이 앉은 성인 B의 두 허벅지 위에 놓이고 A 발 하나는 바닥에, B 양발은 바닥에 닿는다.
- English: Adult A sits across seated adult B's thighs, with one A foot and both B feet contacting the floor.
- 관계: A_pelvis → supported_by → B_thighs; B_pelvis → supported_by → chair; A_foot → on → floor; B_feet → on → floor; A_foot → belongs_to → A; A_pelvis → belongs_to → A; B_feet → belongs_to → B; B_pelvis → belongs_to → B; B_thighs → belongs_to → B
- 혼동 경계: 무릎베개와 지지 대상이 다르다. 성적 행위·친밀 관계·동의의 증명으로 점수화하지 않는다.
- 관찰 게이트: 두 골반·허벅지·의자·구별되는 다리와 발 지지를 보인다.
- 제안 슬롯: body_pose, contact_point, relational_action; 출처: S18

## A31 입맞춤, 키스 직전의 멈춤

- 유형: observable / P1
- 한글: 마주 선 성인 A와 B의 얼굴은 가까우나 두 입술 윤곽 사이에 가는 공기 틈이 있다.
- English: Facing adults A and B bring their faces close while a narrow air gap remains between their distinct lip contours.
- 관계: A_face → faces → B_face; A_lips → separated_by_gap_from → B_lips; A_face → belongs_to → A; A_lips → belongs_to → A; B_face → belongs_to → B; B_lips → belongs_to → B
- 혼동 경계: 이 카드는 비접촉 표본이다. 실제 키스·직전이라는 시간·욕망·동의를 확정하지 않는다.
- 관찰 게이트: 양 입술 윤곽·공기 틈·두 목의 연결이 식별된다.
- 제안 슬롯: proxemics, contact_point; 출처: S18

## A32 벽짚기, 벽쿵, 카베돈

- 유형: observable / P0
- 한글: 성인 A의 한 손바닥이 B 머리 옆 벽에 닿고 A와 B의 몸통 사이에는 공간이 있으며 B 옆 출입 통로가 보인다.
- English: Adult A places one palm on the wall beside B's head, leaving space between their torsos and a visible passage beside B.
- 관계: A_palm → contacts → wall; A_palm → beside → B_head; A_torso → separated_from → B_torso; passage → beside → B; A_palm → belongs_to → A; A_torso → belongs_to → A; B_head → belongs_to → B; B_torso → belongs_to → B
- 혼동 경계: 벽 타격 소리·연애·상호 동의·이동의 자유는 한 접점만으로 확정하지 않는다. 출입 봉쇄 A37과 별도다.
- 관찰 게이트: 손목 소유·벽 접점·몸 사이 틈·측면 통로를 보인다.
- 제안 슬롯: contact_point, proxemics, space_condition; 출처: S18

## A33 멀어지다 돌아보기

- 유형: staged_proxy / P1
- 한글: 성인 A 몸통은 통로 먼 쪽을 향하고 얼굴은 뒤의 B 쪽으로 돌며 두 사람 사이에 빈 바닥이 이어진다.
- English: Adult A's torso faces down a path while the face turns toward B behind, with empty ground between them.
- 관계: A_torso → faces → path_far_end; A_face → toward → B; empty_ground → between → A_and_B; A_face → belongs_to → A; A_torso → belongs_to → A
- 혼동 경계: 떠남·이별·고백·재회·전후 움직임은 시간/대사가 필요하다.
- 관찰 게이트: 몸통과 얼굴의 다른 방향·B의 위치·거리의 지면을 보인다.
- 제안 슬롯: body_orientation, gaze_target, composition; 출처: S30

## A34 팔짱, 소품을 몸 앞에 두기

- 유형: observable / P1
- 한글: A의 두 팔뚝은 자기 가슴 앞에서 교차하고 양 손목은 반대쪽 팔꿈치 가까이에 놓인다.
- English: A crosses both forearms before A's own chest, with each wrist near the opposite elbow.
- 관계: forearms → belong_to → A; forearms → cross_before → A_chest; wrists → near → opposite_elbows; A_chest → belongs_to → A
- 혼동 경계: 방어·거부·분노·계층은 팔 모양으로 확정하지 않는다. 소품 가림과도 다른 구조다.
- 관찰 게이트: 두 어깨-팔꿈치-손목의 연속 소유가 보인다.
- 제안 슬롯: body_pose, hand_pose; 출처: S18

## A35 책상 양편에서 대치하기

- 유형: staged_proxy / P1
- 한글: A와 B가 탁자의 반대편에 서고 A 두 손은 탁자 가장자리에, B 두 손은 서류철 위에 놓인다.
- English: A and B stand across a table, A's hands on the table edge and B's hands on a folder.
- 관계: A → opposite → B; table → between → A_and_B; A_hands → on → table_edge; B_hands → on → folder; A_hands → belongs_to → A; B_hands → belongs_to → B
- 혼동 경계: 회의·갈등의 선택적 구도다. 비리·가해자·평가권·실제 논쟁을 배치로 판정하지 않는다.
- 관찰 게이트: 탁자 경계·두 몸·네 손의 별도 접점을 보인다.
- 제안 슬롯: proxemics, relational_action; 출처: S20, S30

## A36 앉은 사람을 서서 내려다보기

- 유형: staged_proxy / P1
- 한글: 서 있는 A의 눈이 앉은 B 얼굴 쪽 아래를 향하고 B 눈은 A 얼굴 쪽 위를 향한다.
- English: Standing A looks downward toward seated B's face while B looks upward toward A's face.
- 관계: A → standing_above → B_seated_head; A_gaze → toward → B_face; B_gaze → toward → A_face; A_face → belongs_to → A; A_gaze → belongs_to → A; B_face → belongs_to → B; B_gaze → belongs_to → B; B_seated_head → belongs_to → B
- 혼동 경계: 높이 차이는 교수 평가권·갑질·강압의 충분조건이 아니다.
- 관찰 게이트: 서고 앉은 지지와 서로 다른 시선 종단을 보인다.
- 제안 슬롯: gaze_target, proxemics, scale_relation; 출처: S20

## A37 출입문을 막아 서기

- 유형: staged_proxy / P0
- 한글: 열린 문틀 안에 A가 서서 문턱 폭 대부분을 차지하고 B는 방 안쪽에서 문을 바라본다.
- English: A stands in an open doorway occupying most of its width while B faces the doorway from inside the room.
- 관계: A → within → doorframe; A_body → spans → doorway_width; B → inside → room; B_gaze → toward → doorway; A_body → belongs_to → A; B_gaze → belongs_to → B
- 혼동 경계: 가시적인 경로 점유를 평가한다. 실제 감금·다른 출구 부재·법적 범죄는 단일 프레임으로 확정하지 않는다.
- 관찰 게이트: 문 양쪽 기둥·문턱·A 발 위치·B의 공간 관계를 보인다.
- 제안 슬롯: space_condition, proxemics; 출처: S18, S20

## A38 손목을 붙잡아 멈추게 하기

- 유형: observable / P0
- 한글: 성인 A의 오른손 손가락이 성인 B의 왼손목 둘레에 놓이고 B 손은 손가락을 펼친 채 A 손에서 이어진다.
- English: Adult A's right fingers encircle adult B's left wrist while B's open hand continues beyond A's grip.
- 관계: A_right_hand → belongs_to → A; A_fingers → encircle → B_left_wrist; B_left_wrist → connects_to → B_hand; A_fingers → belongs_to → A; B_hand → belongs_to → B; B_left_wrist → belongs_to → B
- 혼동 경계: 소매 집기와 피부 손목 접촉을 구별한다. 멈춤 시간·자발성·가해·동의는 별도 맥락이다.
- 관찰 게이트: 두 손 주인·B 팔-손목-손과 A 손가락 둘레가 보인다.
- 제안 슬롯: contact_point, relational_action; 출처: S18

## A39 한 사람을 여럿이 둘러싸기, 따돌림

- 유형: staged_proxy / P1
- 한글: 중앙 A 주위 서로 다른 세 방향에 B·C·D가 서고 A 앞 바닥의 빈 틈은 한쪽에만 남는다.
- English: B, C and D stand on three different sides of central A, leaving an open floor gap on one side.
- 관계: B → on_left_of → A; C → on_right_of → A; D → in_front_of → A; gap → beside → A
- 혼동 경계: 인물 수·공간 압박을 평가한다. 가해·배척·회원가입·헤이징 동기·보복은 별도 맥락이다.
- 관찰 게이트: 네 사람·발 위치·둘러싼 각도·남은 틈이 보인다.
- 제안 슬롯: composition, proxemics, subject_count; 출처: S19

## A40 몸을 움츠리거나 팔로 보호하기

- 유형: observable / P1
- 한글: A가 상체를 앞으로 굽혀 두 팔뚝을 머리 앞에 세우고 양손은 자기 머리 옆에 놓인다.
- English: A bends the torso forward with both forearms raised before the head and hands beside A's own head.
- 관계: A_torso → bent_forward_over → A_hips; A_forearms → before → A_head; A_hands → beside → A_head; A_forearms → belongs_to → A; A_hands → belongs_to → A; A_head → belongs_to → A; A_hips → belongs_to → A; A_torso → belongs_to → A
- 혼동 경계: 자기 보호처럼 보이는 형상과 실제 공포·사건·진단·가해 원인을 분리한다.
- 관찰 게이트: 목-몸통과 두 팔의 소유·머리 가림 경계를 보인다.
- 제안 슬롯: body_pose, contact_point; 출처: S18, S19

## A41 떨어진 물건을 혼자 줍기

- 유형: staged_proxy / P1
- 한글: 쪼그린 A의 손끝이 바닥의 책 한 권에 닿고 다른 종이 두 장이 그 옆에 떨어져 있다.
- English: Crouching A touches one book on the floor with the fingertips, with two separate papers beside it.
- 관계: A_fingertips → contact → book; book → on → floor; papers → beside → book; A_feet → on → floor; A_feet → belongs_to → A; A_fingertips → belongs_to → A
- 혼동 경계: 싸움·모욕·실패의 이후라는 시간·원인을 확정하지 않는다.
- 관찰 게이트: 몸의 지지·손 주인·책·두 종이 수를 보인다.
- 제안 슬롯: action, prop_placement, narrative_clue; 출처: S30

## A42 멍, 붕대, 찢어진 소매, 피 묻은 옷

- 유형: observable / P1
- 한글: 성인 A의 팔뚝에 겹친 흰 붕대 띠가 감기고 같은 팔 소매에는 가장자리 실이 풀린 작은 찢김이 있다.
- English: Overlapping white bandage strips wrap adult A's forearm, and the same sleeve has a small tear with frayed edges.
- 관계: bandage → wraps → A_forearm; tear → in → A_sleeve; frayed_threads → border → tear; A_forearm → belongs_to → A; A_sleeve → belongs_to → A
- 혼동 경계: 붕대·색 자국·찢김은 사고·폭행·동의·가해자·피의 성분을 증명하지 않는다. 멍·출혈 별도 실현은 추가 연구 대상이다.
- 관찰 게이트: 팔-붕대·같은 팔의 소매·찢김 가장자리를 분리해 보인다.
- 제안 슬롯: aftermath_trace, garment_state; 출처: S18, S19

## F01 설정숏, Establishing shot

- 유형: staged_proxy / P1
- 한글: 넓은 화면에 건물 입구·연결 보행로·사람 여럿이 함께 보이고 사람은 건물보다 작게 놓인다.
- English: A wide view includes a building entrance, its connecting path and several people small relative to the building.
- 관계: path → leads_to → entrance; people → smaller_than → building
- 혼동 경계: 이것만으로 대학·계절·도입 순서·특정 캠퍼스를 증명하지 않는다.
- 관찰 게이트: 출입구-길 연결과 인물/건물 상대 크기를 확인한다.
- 제안 슬롯: composition, shot_scale; 출처: S30

## F02 투숏, Two-shot

- 유형: observable / P1
- 한글: A와 B의 머리와 몸통이 한 화면에 함께 보이고 그 사이에 빈 공간이 남는다.
- English: A and B's heads and torsos share one frame with visible space between them.
- 관계: A → within → frame; B → within → frame; space → between → A_and_B
- 혼동 경계: 연애·관계·갈등을 두 사람 배치만으로 확정하지 않는다.
- 관찰 게이트: 인물 둘과 사이 공간이 프레임 안에 보인다.
- 제안 슬롯: composition, subject_framing; 출처: S30

## F03 오버더숄더, Over-the-shoulder

- 유형: observable / P1
- 한글: 가까운 A 어깨와 뒤통수가 화면 한쪽 전경을 차지하고 먼 B 얼굴은 그 너머에 보인다.
- English: A's near shoulder and back of head occupy one foreground edge, with B's face visible beyond.
- 관계: A_shoulder → in → foreground; A_back_head → in → foreground; B_face → beyond → A_shoulder; A_back_head → belongs_to → A; A_shoulder → belongs_to → A; B_face → belongs_to → B
- 혼동 경계: 시점 소유·실제 대화·몰래봄·교수 평가권은 별도다.
- 관찰 게이트: A 어깨-목-머리와 먼 B 얼굴이 분리되어 보인다.
- 제안 슬롯: viewer_position, composition; 출처: S30

## F04 인서트, Insert shot, 선택적 초점, 얕은 심도

- 유형: observable / P1
- 한글: 가까운 손과 교재 모서리는 선명하고 뒤쪽 사람 얼굴과 서가는 흐릿하게 남는다.
- English: A near hand and book corner are sharp while a distant face and bookshelves remain blurred.
- 관계: hand → at → sharp_focus_plane; book_corner → at → sharp_focus_plane; face → in → blurred_background
- 혼동 경계: 이 카드는 초점 표본이다. 인서트의 편집상 기능·실제 초점 이동·성적표 정보는 별도다.
- 관찰 게이트: 선명한 평면과 흐린 후경 구분을 확인한다.
- 제안 슬롯: focus, depth_of_field; 출처: S24

## F05 프레임 속 프레임, 네거티브 스페이스

- 유형: staged_proxy / P1
- 한글: 문틀 네 변 안쪽 먼 곳에 A가 있고 A 옆 벽과 바닥의 큰 부분은 비어 있다.
- English: Distant A stands within four edges of a doorway frame, with a large empty wall and floor area beside A.
- 관계: doorframe → surrounds → A; empty_area → beside → A
- 혼동 경계: 고립·실종·헤어진 연인의 부재·몰래 관찰은 빈 면적과 별개다.
- 관찰 게이트: 문틀 네 변·인물 위치·빈 면적의 경계를 보인다.
- 제안 슬롯: composition, visual_density; 출처: S30

## F06 공간별 조명 대비, 강의실, 작업실, 축제

- 유형: observable / P1
- 한글: 한 탁자의 스탠드는 손과 도면을 밝히고 그 뒤 복도는 더 어두우며 스탠드 몸체가 탁자에 닿는다.
- English: A desk lamp lights a hand and drawing on a table while the corridor behind stays darker, with the lamp base on the table.
- 관계: lamp_base → on → table; lamp_light → falls_on → hand_and_drawing; corridor → darker_than → table_zone
- 혼동 경계: 조명은 실제 시간·전기 상태·공부 시간·불길함을 확정하지 않는다. 모든 캠퍼스를 따뜻한 노을로 고정하지 않는다.
- 관찰 게이트: 물리 광원·조명 영역·후경 대비가 보인다.
- 제안 슬롯: lighting, light_direction; 출처: S13

## F07 시선 연결, 반복 구도, 계절 대비

- 유형: temporal / P1
- 한글: 한 프레임의 시선 방향과 컷 간 연결·반복 구도·계절 변화는 서로 다른 증거 단위다.
- English: A gaze direction in one frame is distinct from an eyeline edit, repeated framing or seasonal change across frames.
- 관계: still_frame → distinct_from → ordered_sequence; seasonal_change → requires → multiple_timepoints
- 혼동 경계: 스틸 한 장의 벚꽃·낙엽·빈자리로 시간 변화나 과거 관계를 증명하지 않는다.
- 관찰 게이트: 동일 구도 식별자와 서로 다른 시간점의 자료가 없으면 변화는 UNSCORED다.
- 제안 슬롯: narrative_phase, calendar_context; 출처: S30

## C01 캠퍼스물, 캠퍼스 로맨스, 청춘물, 성장물, 청춘 군상극, 캠퍼스 일상물, 뉴 어덜트, 아카데믹 노블, 대학원물, 대학 스포츠 로맨스, 캠퍼스 BL·GL, 캠퍼스 미스터리·스릴러, 캠퍼스 호러, 다크 아카데미아

- 유형: context_only / P1
- 한글: 장르는 대학·학문 공동체·관계·진로의 선택 문맥이며 고딕 건물·교복·성적 관계·흰 가운을 자동 추가하지 않는다.
- English: Genre cues guide choices about education, community, relationships and careers without imposing gothic buildings, uniforms, sex or lab coats.
- 관계: genre → offers → optional_context; requester_core → controls → visual_selection
- 혼동 경계: OUP 연구자의 academic/campus 구분과 다른 기관의 넓은 용례가 공존한다. 대학 배경·NA·이용등급을 독립 축으로 둔다.
- 관찰 게이트: 장르 입력만으로 고정 복장·신체 접촉·성적 의미를 강제하지 않는지 검사한다.
- 제안 슬롯: genre, narrative_core; 출처: S01, S02, S30

## C02 학번, 새내기, 헌내기, 고학번, 화석, 동기, 선배·후배, 휴학생·복학생, 군휴학·군필 복학생, 편입생, 만학도·성인학습자, 유학생·교환학생, 통학생·기숙사생·자취생, 취준생, 졸업유예생·수료생

- 유형: context_only / P0
- 한글: 학적·입학 연도·나이·현재 학년·국적·거주와 외형 나이는 별도 정보다.
- English: Enrollment, entry year, age, current year, nationality, residence and visible age presentation are separate information.
- 관계: entry_year → distinct_from → age; enrollment_state → requires → declared_context; appearance → does_not_prove → identity
- 혼동 경계: 복학생을 나이 많은 남성·유학생을 특정 외모·새내기를 미성년·과잠을 재학 증거로 자동 지정하지 않는다.
- 관찰 게이트: 신원은 선언/기록으로 확인하며 픽셀 단독 신원 PASS는 없다.
- 제안 슬롯: declared_person_background, participant_role; 출처: S03, S22

## C03 단과대학·단대, 학부·학과·전공, 과대, 학생회·총학생회, 동아리연합회·동연, 조교, TA·RA, 학부연구생, 지도교수, PI, Office hours

- 유형: context_only / P1
- 한글: 대표·조교·교수·PI의 역할과 실제 평가·고용·연구비 권한을 각각 기록한다.
- English: Representative, assistant, faculty and PI roles are separate from actual grading, employment and funding authority.
- 관계: role → has_scope → declared_authority; title → distinct_from → visible_pose
- 혼동 경계: 서 있는 사람=교수·안경=PI·과대=교수 평가권 금지다. RA는 생활관/연구의 다의어다.
- 관찰 게이트: 책상 배치와 공식 역할을 분리한 문맥 판정이 필요하다.
- 제안 슬롯: participant_role, declared_person_background; 출처: S07, S20, S22, S23

## C04 수강신청, 수강정정·드랍, 증원·정원 외 수강, 강의계획서, 전필·전선, 교필·교선, 복전·부전, 전과, 학점·평점, 공강, 우주공강, 연강, 분반, 청강, 재수강, 계절학기·계절수업, 학사경고·학고, 휴강·보강, 졸업사정

- 유형: context_only / P1
- 한글: 학사 절차·시간표·성적·학위 요건은 기관·입학년도·과정 맥락과 판독 가능한 문서가 필요하다.
- English: Academic procedures, timetables, grades and degree requirements need institution, entry-year and program context plus readable records.
- 관계: requirement → belongs_to → institution_and_cohort; schedule_claim → requires → readable_context
- 혼동 경계: 노트북 화면빛=수강신청 성공·빈 교실=휴강·낙제=즉시 제적 등식을 만들지 않는다.
- 관찰 게이트: 문서 내용·절차 결과·픽셀 가독성을 별도로 평가한다.
- 제안 슬롯: situation_context, visible_text; 출처: S03, S04, S05

## C05 팀플·조별과제, 조장·팀장, 프리라이더·무임승차, 잠수, 리포트·레포트, 족보, 꿀강·헬강, 출튀·대출, 벼락치기·밤샘, 장학금·근로장학생, 공모전·대외활동, 인턴·현장실습, 스펙·취업스터디

- 유형: context_only / P1
- 한글: 기여·불참·평가·부정행위·공부 이력은 행동의 시간 기록과 계약·학사 맥락으로 확인한다.
- English: Contribution, absence, evaluation, misconduct and study history need records over time and the relevant employment or academic context.
- 관계: contribution_claim → requires → work_history; fatigue_appearance → distinct_from → cause
- 혼동 경계: 빈 의자=무임승차·안경=과탑·다크서클=밤샘·책=유출 족보·노트북=수강 성공으로 판정하지 않는다.
- 관찰 게이트: 가시적인 공동 작업과 기여·수면·부정행위 사실을 따로 점수화한다.
- 제안 슬롯: offscreen_context, situation_context; 출처: S04, S05, S17

## C06 OT, 새터, MT, 개총·종총, 뒤풀이, 밥약, 짝선·짝후, 뻔선·뻔후, 미팅, 소개팅, 과팅, 자만추, 중앙동아리·과동아리, 연합동아리, 학회·스터디, 동아리박람회, 대동제, 축제 부스·주점, 정기공연·정기전시, 체육대회·과대항전·정기전, 농활·봉사활동

- 유형: context_only / P1
- 한글: 행사 목적·주최·참가 관계·이름은 학교별 맥락으로 유지하고 그 안의 가시 행동만 선택적으로 제안한다.
- English: Event purpose, organizer, participants and name remain institution-specific context, with only selected visible activities proposed.
- 관계: event_name → scoped_to → institution; event → may_include → authored_scene
- 혼동 경계: OT·새터·MT·총회를 모두 술자리로 합치지 않는다. 밥약=데이트·대동제=모든 대학 축제도 아니다.
- 관찰 게이트: 행사 태그만으로 음주·폭력·연애 후보를 자동 채택하지 않는지 검사한다.
- 제안 슬롯: occasion_context, situation_context; 출처: S05, S06, S07

## C07 과탑, 모범생형, 장학생형, 생계형 대학생, 인싸, 아싸·아웃사이더, 과여신·과남신·퀸카·킹카, 너드, 다정한 선배·멘토형, 능글맞은 선배, 직진 후배·연하 직진형, 라이벌·수석 경쟁자, 팀플 빌런, 부잣집 학생·상속자형, 예술 천재형, 겉과 속이 다른 모범생

- 유형: context_only / P1
- 한글: 성격·인기·성적·재산·재능·사회적 평판은 안경·피부·브랜드·자세와 독립된 서사 정보다.
- English: Personality, popularity, grades, wealth, talent and reputation are narrative information independent of glasses, skin, brands or posture.
- 관계: archetype → distinct_from → visible_styling; rank_claim → requires → independent_context
- 혼동 경계: 너드=안경·부자=특정 브랜드·과탑=단정한 옷·아싸=괴롭힘 피해라는 자동 분류를 만들지 않는다.
- 관찰 게이트: 단일 외형으로 인물 등급·성격·재산을 확정하는 후보가 없어야 한다.
- 제안 슬롯: declared_person_background, character_contrast; 출처: S30

## C08 CC, 과CC, 썸, 짝사랑, 쌍방삽질, 선후배 로맨스, 비밀연애·공개연애, 친구에서 연인으로, 라이벌에서 연인으로, 혐관·앙숙에서 연인으로, 계약연애, 가짜 연애, 룸메이트 로맨스, 튜터·과외 로맨스, 슬로 번, 상반된 성격의 끌림, 그럼피×선샤인, 재회물, 삼각관계·다각관계, 하렘·역하렘, 금지된 사랑, 장거리 연애, 헤어진 CC

- 유형: context_only / P1
- 한글: 관계의 명칭·독점성·숨김·과거·감정 변화는 독립 선언과 시간 자료로 유지한다.
- English: Relationship labels, exclusivity, secrecy, history and emotional change require independent declarations and temporal evidence.
- 관계: relationship_label → requires → declared_context; contact_geometry → distinct_from → relationship_history
- 혼동 경계: 같은 학교·시밀러 룩·컵 둘·세 인물 구도는 CC·불륜·하렘·과거 이별의 증거가 아니다.
- 관찰 게이트: 외형 평가는 접촉/거리까지, 관계의 진실·전환은 별도 평가한다.
- 제안 슬롯: narrative_core, offscreen_context; 출처: S18, S30

## C09 성인 캠퍼스물·19금 캠퍼스물, 성적 긴장, 스킨십, 첫 경험·성적 탐색, 훅업, 원나잇, FWB, 시추에이션십, 스파이시·고수위, 오픈 도어, 클로즈드 도어·페이드 투 블랙

- 유형: context_only / P0
- 한글: 성인 등장인물·독자 이용등급·관계·묘사 강도·장면 생략 방식을 서로 다른 축으로 남긴다.
- English: Adult characters, audience rating, relationship type, explicitness and scene omission remain separate axes.
- 관계: audience_rating → distinct_from → character_age; relationship_type → distinct_from → depiction_intensity
- 혼동 경계: 대학생·NA=모두 성인·FWB=모든 접촉 허용·닫힌 방문=성관계 생략 완료·노출=의도라는 추론을 금지한다.
- 관찰 게이트: 성인 조건은 독립 확인, 장르·수위·관계는 픽셀만으로 PASS 없음.
- 제안 슬롯: adult_presentation_context, narrative_phase; 출처: S02, S18

## C10 성적 동의, 성희롱, 성폭력·강간·성적 강압, 약물 이용 성폭력, 이미지 기반 성적 학대

- 유형: context_only / P0
- 한글: 동의·원치 않음·능력 저하·촬영이나 공유의 허락은 옷·표정·침묵과 별도로 다룬다.
- English: Consent, unwanted conduct, impaired capacity and permission to record or share are separate from clothing, expression or silence.
- 관계: consent → requires → independent_context; clothing → does_not_prove → consent
- 혼동 경계: 사건 용어는 조사 범위에 보존하되 성적 폭력의 실행·관능적 시각 후보로 자동 변환하지 않는다. 법적 판단과 사진 외형도 분리한다.
- 관찰 게이트: 픽셀로 동의·약물·범죄 여부 판정 불가. 문맥은 context_only로 유지한다.
- 제안 슬롯: offscreen_context; 출처: S18, S20

## C11 동거, 비독점 관계, 폴리아모리, 바람·양다리, NTR·네토라레, 커밍아웃·아우팅

- 유형: context_only / P1
- 한글: 동거·관계 합의·독점성 위반·자기 공개와 타인의 공개는 서로 다른 사건과 정보다.
- English: Cohabitation, relationship agreements, violated exclusivity, self-disclosure and disclosure by another are distinct facts.
- 관계: nonexclusivity → distinct_from → betrayal; self_disclosure → distinct_from → outing
- 혼동 경계: 침대 하나·세 사람·동성 접촉·과잠 대여는 성적 지향·동거·외도·아우팅을 증명하지 않는다. GLAAD 원문은 접근 실패로 추가 검증 필요다.
- 관찰 게이트: 관계 합의와 공개 주체를 독립 문맥으로 확인한다.
- 제안 슬롯: offscreen_context, narrative_core; 출처: S18, S28

## C12 페티시, BDSM·D, s, 스폰서·대가성 관계

- 유형: context_only / P1
- 한글: 의상·질감·역할 연출·성인 합의·교수의 평가권·경제 의존을 독립된 정보로 둔다.
- English: Clothing, texture, role staging, adult agreement, academic authority and financial dependence remain independent information.
- 관계: clothing_preference → distinct_from → sexual_interest; academic_power → distinct_from → consensual_roleplay
- 혼동 경계: 망사·목걸이·리본·란제리풍=페티시·BDSM·교수 지배라는 자동 의미 부여 금지. 구체 정의와 관계별 자료는 추가 검증한다.
- 관찰 게이트: 이 카드에는 성적 positive·구속 구현 지시를 만들지 않는다.
- 제안 슬롯: offscreen_context, fetish_styling; 출처: S18, S20

## C13 강제 근접, 침대가 하나뿐

- 유형: context_only / P1
- 한글: 반복적으로 같은 장소를 쓰게 되는 서사 장치·실제 이동 제한·합의된 잠자리 조율을 구별한다.
- English: Narrative proximity, actual movement restriction and agreed sleeping arrangements are distinct.
- 관계: forced_proximity_trope → distinct_from → coercion; one_bed_count → does_not_prove → sexual_event
- 혼동 경계: 과제·합숙=성적 강압·침대 하나=성관계·문 옆 손=감금의 등식은 성립하지 않는다.
- 관찰 게이트: 침대 수·공간만 가시 평가하고 합의·시간·사건은 별도다.
- 제안 슬롯: situation_context, offscreen_context; 출처: S18, S22

## C14 연구실 갑질, 표절, 데이터 위조·변조, 부당한 저자 표시, 내부고발

- 유형: context_only / P0
- 한글: 위조·변조·표절·기여 왜곡·고발·정직한 오류는 원자료와 절차·기여 이력으로 구별한다.
- English: Fabrication, falsification, plagiarism, authorship disputes, reporting and honest error require original records and histories.
- 관계: fabrication → distinct_from → falsification; plagiarism → distinct_from → honest_error; allegation → distinct_from → verified_finding
- 혼동 경계: 표 두 개의 차이·빨간 교정·지운 이름·외장디스크·표정만으로 연구부정을 확정하지 않는다.
- 관찰 게이트: 가독성·자료 차이·실제 부정 판정을 각각 나눈다.
- 제안 슬롯: visible_text, offscreen_context; 출처: S17, S20

## C15 권력 불균형, 지도교수, PI, 금지된 사랑, 튜터·과외 로맨스

- 유형: context_only / P0
- 한글: 교수·조교·학생대표·동료 튜터의 실제 평가·고용·자금 권한과 사적 관계를 구분한다.
- English: Actual grading, employment and funding power of faculty, assistants, representatives and peer tutors is distinct from private relationships.
- 관계: grading_power → requires → declared_institutional_role; seating_height → does_not_prove → authority
- 혼동 경계: 연령 차이·높은 의자·흰 가운·책상 소유만으로 평가권을 생성하지 않는다. Cornell 정책은 기관 범위 사례다.
- 관찰 게이트: 권한과 이해충돌은 문맥/규정 검증, 포즈는 별도 픽셀 검사다.
- 제안 슬롯: participant_role, offscreen_context; 출처: S20, S23

## C16 헤이징, 군기·얼차려·집단 기합, 음주 강요, 집단폭행·린치, 2차 가해·보복

- 유형: context_only / P1
- 한글: 가입·소속 유지·압박·위험·가해와 반복·보복 동기를 가시적 배치와 분리한다.
- English: Affiliation, pressure, risk, aggression, repetition and retaliation motives are separate from visible arrangements.
- 관계: hazing_claim → requires → affiliation_and_harm_context; group_pose → does_not_prove → coercion
- 혼동 경계: 원형 모임·팔굽혀펴기·술잔·환영 행사만으로 헤이징이나 동의를 판정하지 않는다.
- 관찰 게이트: 사건 용어는 보존, 실제 행위/맥락 없이 범죄·자발성 PASS 금지다.
- 제안 슬롯: offscreen_context; 출처: S19, S18

## C17 스토킹, 교제폭력, 가스라이팅, 따돌림·사이버불링, 단톡방·익명 커뮤니티

- 유형: context_only / P1
- 한글: 반복 접촉·원치 않음·통제·기억 흔들기·집단 배제는 시간·내용·당사자 맥락이 필요하다.
- English: Repeated contact, unwanted behavior, control, manipulation and exclusion require time, content and participant context.
- 관계: repeated_behavior → requires → temporal_records; message_geometry → distinct_from → harassment_finding
- 혼동 경계: 뒤따른 두 인물·한 통의 메시지·혼자 앉기=스토킹·가스라이팅·왕따로 확정하지 않는다.
- 관찰 게이트: 기기 화면 안/밖과 실제 인물 수를 먼저 검증하고 사건 판단은 분리한다.
- 제안 슬롯: offscreen_context, visible_text; 출처: S18, S19

## C18 학업 소진·번아웃, 가면이 벗겨질 것 같은 불안, 자해·자살 위기·회복 서사, 피폐물

- 유형: context_only / P1
- 한글: 피로 외형·주관적 불안·임상 진단·자해 의도·위기·회복 경과를 별도 정보로 유지한다.
- English: Fatigue appearance, subjective anxiety, diagnosis, self-harm intent, crisis and recovery course remain separate information.
- 관계: visible_fatigue → distinct_from → diagnosis; recovery → requires → time_and_context
- 혼동 경계: 다크서클·붕대·번진 화장·엎드림으로 진단·의도·원인·회복을 확정하지 않는다. 위기 방법을 시각 구현으로 추가하지 않는다.
- 관찰 게이트: 연구 범위 보존, 의도·진단·회복의 픽셀 PASS는 없음.
- 제안 슬롯: offscreen_context, narrative_phase; 출처: S18, S30

## C19 실종·살인·사건 은폐, 비밀결사·폐쇄적 학회, 학내 괴담·기숙사 괴담, 오컬트 동아리·금지된 연구, 캠퍼스 슬래셔, 고어·스플래터, 생존·봉쇄 캠퍼스

- 유형: context_only / P1
- 한글: 위협·초자연 원인·죽음·사건 은폐·고어 표현 강도와 빈 복도·손상·색 자국을 분리한다.
- English: Threat, supernatural cause, death, concealment and graphic intensity are separate from empty corridors, damage and colored stains.
- 관계: empty_space → does_not_prove → missing_person; damage → does_not_prove → murder; fictional_cause → requires → declared_world
- 혼동 경계: 대학 장르=살인·학회=비밀결사·붉은 얼룩=사람 피·쓰러짐=사망으로 자동 변환하지 않는다. 장르별 구체 표현은 별도 모듈 심사다.
- 관찰 게이트: 손상·공간은 보이고 원인/생사/범인은 UNSCORED다.
- 제안 슬롯: genre, offscreen_context; 출처: S01, S30

## C20 Freshman·Sophomore·Junior·Senior, Freshers, Fraternity·Sorority, Greek life, Chapter, Rush·Recruitment, Bid, Pledge·New member, RA, Varsity, Homecoming, Formal, Quad, Office hours

- 유형: context_only / P0
- 한글: 북미 조직·영국 신입생 행사·학년·기숙사 역할·연구조교·정기 면담을 지역·기관·약자 의미별로 나눈다.
- English: North American organizations, British entry events, year labels, residence roles, research jobs and office hours are separated by locale and institution.
- 관계: RA_resident → distinct_from → RA_research; chapter → distinct_from → academic_department; formal → distinct_from → prom
- 혼동 경계: 미국 고교 prom을 보편 대학 행사로 이식하지 않는다. varsity 재킷은 선수 신분을 보증하지 않으며 해외 문화 전체 정의의 독립 검증은 일부 남아 있다.
- 관찰 게이트: 약자·장소·행사별 다의어 질의를 분리하고 지역이 없으면 고정 선택하지 않는다.
- 제안 슬롯: occasion_context, participant_role; 출처: S21, S22, S23, S16

## C21 다크 아카데미아, 라이트 아카데미아, 긱 시크, 놈코어, 애슬레저, 스트리트웨어, 코케트, 발레코어, 칼리지에이트, 바시티 스타일, 프레피, 아이비 스타일

- 유형: context_only / P1
- 한글: 스타일 명칭은 옷 구조·색·장소를 고르는 문맥이며 특정 계급·성적 의미·나이·인기 순위가 아니다.
- English: Style names guide optional garment, color and setting choices without fixing class, sexuality, age or popularity.
- 관계: style_label → offers → optional_components; style_label → does_not_prove → social_identity
- 혼동 경계: FIT의 아이비 근거를 모든 현대 스타일의 정의로 확대하지 않는다. 미확인 미학·신조어는 별도 자료 수집 후 승인한다.
- 관찰 게이트: 스타일명만으로 고정 조합·교복·노출·고딕 건물을 강제하지 않는지 검사한다.
- 제안 슬롯: aesthetic_trend, wardrobe_style; 출처: S09, S10, S29

## C22 계층 갈등, 문화자본, 학벌주의·학력주의, 장학금·기회 경쟁, 가족의 기대와 통제, 학생회 정치·회계 비리, 학생운동·대자보·학내 시위

- 유형: context_only / P1
- 한글: 생활비·기회·교육 경험·가족 기대·대표성·회계 사실은 옷차림·표정·좌석 배치보다 넓은 사회적 맥락이다.
- English: Costs, opportunities, educational experience, family expectations, representation and accounting facts require social context beyond clothes, expressions or seating.
- 관계: economic_status → requires → independent_context; poster_claim → distinct_from → verified_fact
- 혼동 경계: 명품=상속자·알바 복장=가난·대자보=비리 사실·고풍 건물=엘리트라는 자동 판정은 금지다.
- 관찰 게이트: 가시 소품·주장의 내용·입증된 사실·의도는 각각 구분한다.
- 제안 슬롯: offscreen_context, narrative_core; 출처: S07, S17, S30

