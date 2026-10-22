# 시각 의미 카드

출처는 정의·경계의 근거다. 구체적 구도·소유 관계는 이번에 저술한 창작 제안이며 임상 사진 관찰 결과가 아니다.

## A01 수술등·테이블·기구대의 중심 배치

연결 용어: Operating Theatre; Surgical Horror
처리: still / P0

An articulated surgical lamp hangs over one operating table; a separate metal instrument trolley stands alongside the table.

관절식 수술등이 수술대 하나 위에 걸려 있고, 별도의 금속 기구대가 수술대 옆에 놓여 있다.

관계: lamp → above → table; trolley → beside → table
슬롯 제안: location, object_structure, prop_placement
혼동: 해부극장의 계단식 관람석; 식탁

주장 한계: 장비 배치의 창작 실현이며 실제 수술·무균·기관 인증을 입증하지 않는다.

근거: [S06 NIGMS Anesthesia](https://www.nigms.nih.gov/education/fact-sheets/Pages/anesthesia)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A02 중환자실 침상과 분리된 모니터

연결 용어: Intensive Care Unit, ICU; Mechanical Breathing
처리: still / P0

A bedside monitor and a ventilator occupy separate stands beside one hospital bed, leaving their separate cables and breathing circuit visible.

침상 모니터와 인공호흡기가 병상 하나 옆의 서로 다른 받침대에 놓여 있으며, 각각의 전선과 호흡 회로가 구별되어 보인다.

관계: monitor → beside → bed; ventilator → beside → bed
슬롯 제안: location, prop, object_structure
혼동: 모니터를 인공호흡기로 취급; 장비가 환자를 가림

주장 한계: 기계의 존재는 작동·중증도·생존·의식의 증거가 아니다.

근거: [S33 NHLBI What Is a Ventilator](https://www.nhlbi.nih.gov/health/ventilator)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A03 격리 경계의 문·유리·전실

연결 용어: Isolation Ward; Hospital Horror
처리: still / P0

A glazed door separates a single hospital room from a small anteroom; a second door separates that anteroom from the corridor.

유리창이 있는 문이 1인 병실과 작은 전실을 나누고, 두 번째 문이 전실과 복도를 나눈다.

관계: door_a → separates → room_and_anteroom; door_b → separates → anteroom_and_corridor
슬롯 제안: location, object_structure, spatial_depth
혼동: 감옥 철창; 단순 복도 문

주장 한계: 격리 목적·압력 방향·감금·감염을 건축 외형만으로 확정하지 않는다.

근거: [S05 CDC Environmental Infection Control: Air](https://www.cdc.gov/infection-control/hcp/environmental-control/air.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A04 음압 표시와 문 경계의 도식

연결 용어: Negative-Pressure Room
처리: proxy / P0

A clearly fictional schematic beside a room door shows an arrow from the corridor into the room and the label "NEGATIVE".

병실 문 옆의 명백한 허구 도식에는 복도에서 병실 안으로 향하는 화살표와 "NEGATIVE"라는 글자가 표시되어 있다.

관계: diagram.arrow → points_from → diagram.corridor; diagram.arrow → points_into → diagram.room
슬롯 제안: visible_text, prop_placement, narrative_clue
혼동: 실제 공기 흐름; 양압 방향 화살표

주장 한계: 보이는 것은 도식의 주장이다. 작동하는 음압·기류·안전 인증은 이미지에서 입증되지 않는다.

근거: [S05 CDC Environmental Infection Control: Air](https://www.cdc.gov/infection-control/hcp/environmental-control/air.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A05 양압 보호환경 표시의 역방향 도식

연결 용어: Protective Environment
처리: proxy / P0

A clearly fictional schematic beside a room door shows an arrow from the room into the corridor and the label "POSITIVE".

병실 문 옆의 명백한 허구 도식에는 병실에서 복도로 향하는 화살표와 "POSITIVE"라는 글자가 표시되어 있다.

관계: diagram.arrow → points_from → diagram.room; diagram.arrow → points_into → diagram.corridor
슬롯 제안: visible_text, prop_placement, narrative_clue
혼동: 음압 격리실; 산소 농도 표시

주장 한계: 도식의 방향만 평가하며 실제 보호환경 성능·환자의 면역 상태는 판단하지 않는다.

근거: [S05 CDC Environmental Infection Control: Air](https://www.cdc.gov/infection-control/hcp/environmental-control/air.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A06 긴 창가 회랑의 요양시설 제안

연결 용어: Sanatorium; Medical Gothic
처리: still / P1

A long glazed corridor contains widely spaced reclining chairs facing the windows, with a closed clinical door at its far end.

긴 유리창 회랑에 창을 향한 안락의자들이 띄엄띄엄 놓여 있고, 회랑 끝에는 닫힌 진료실 문이 있다.

관계: chairs → face → windows; door → at_end_of → corridor
슬롯 제안: location, prop_placement, spatial_depth
혼동: 일반 리조트를 특정 시대 결핵요양소로 단정

주장 한계: 창작 공간 제안이다. 시대·국가·질병에 따른 요양소 역사 실현은 별도 도면·사진 조사가 필요하다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A07 닫힌 영안실 서랍

연결 용어: Morgue; Hospital Horror
처리: still / P0

Several closed stainless-steel compartment doors form one wall; each has a handle and a small external label holder.

닫힌 스테인리스 칸막이 문 여러 개가 한 벽을 이루며, 각 문에는 손잡이와 작은 외부 라벨 꽂이가 있다.

관계: compartment_doors → form → wall; label_holders → attached_to → compartment_doors
슬롯 제안: location, object_structure, surface_material
혼동: 내부 시신을 가시 사실로 주장; 주방 냉장고

주장 한계: 불투명하게 닫힌 서랍의 내용·시신 수·신원·생사·온도는 보이지 않는다.

근거: [S41 British Council The Autopsy of Jane Doe](https://filmsandfestivals.britishcouncil.org/projects/the-autopsy-of-jane-doe)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A08 현미경 작업대와 슬라이드 트레이

연결 용어: Pathology Laboratory; Histopathology
처리: still / P0

A microscope stands on a laboratory bench beside a rack of labeled glass slides and a separate specimen container.

실험대 위 현미경 옆에 라벨이 붙은 유리 슬라이드 랙과 별도의 표본 용기가 놓여 있다.

관계: slides → held_by → rack; microscope → beside → rack
슬롯 제안: location, prop, prop_placement
혼동: 육안 표본을 현미경 조직으로 취급

주장 한계: 병리 진단·시료의 인체 기원·세포 상태를 작업대 외형으로 확정하지 않는다.

근거: [S10 NCI Biopsy](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/biopsy)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A09 환자 운반 침대의 천장 시점

연결 용어: Gurney; Hospital Horror
처리: still / P0

From a low reclining viewpoint, the near edges of a wheeled stretcher frame the bottom corners while ceiling panels recede toward a closed double door.

낮게 누운 시점에서 바퀴 달린 운반 침대의 가까운 가장자리가 화면 아래 양쪽을 감싸고, 천장 패널이 닫힌 양문을 향해 멀어진다.

관계: stretcher.edges → frame → image.bottom; ceiling.panels → recede_toward → door
슬롯 제안: apparatus_pov, viewer_position, composition
혼동: 공중에서 내려다본 침대; 이동 소리

주장 한계: 정지 시점의 구도이며 실제 운반·이동 방향·의식 상태는 확정하지 않는다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A10 해부극장의 계단과 중앙대

연결 용어: Anatomical Theatre; Surgical Spectacle
처리: still / P1

Stepped concentric viewing rails descend toward a single central demonstration table; the table remains separate from the surrounding seats.

계단식 동심 관람 난간이 중앙의 시연대 하나를 향해 내려가며, 시연대는 둘러싼 좌석과 분리되어 있다.

관계: viewing_rails → surround → demonstration_table
슬롯 제안: location, object_structure, composition
혼동: 현대 수술실; 경기장

주장 한계: 박물관 재현에서 착안한 구도다. 역사적 시신·관객 신분·모든 시대의 해부극장을 대표하지 않는다.

근거: [S37 Rijksmuseum Boerhaave Anatomical Theatre](https://www.rijksmuseumboerhaave.nl/en/our-worlds/anatomical-theatre)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A11 밝고 정돈된 임상 공간의 단일 어긋남

연결 용어: Sterile Dread; Clinical Horror
처리: still / P0

In a brightly lit clinical room, aligned trays and an uninterrupted pale wall surround one chair positioned at a slight angle.

밝게 조명된 진료실에서 정렬된 트레이와 이어지는 옅은 벽 사이에 의자 하나만 조금 비스듬히 놓여 있다.

관계: chair → angled_against → aligned_trays
슬롯 제안: space_condition, composition, lighting
혼동: 청결을 실제 무균으로 주장; 어둠을 공포 필수로 추가

주장 한계: 정렬과 한 어긋남은 창작 제안이며 관객의 불안·무균·공포 성공을 보장하지 않는다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## A12 시설 쇠락과 남아 있는 기구

연결 용어: Hospital Decay
처리: still / P1

Flaking wall paint and rust-colored streaks surround an intact hospital bed; a thin puddle reflects the bed legs on the corridor floor.

벗겨진 벽 도장과 녹빛 얼룩 사이에 형태가 온전한 병상이 있고, 복도 바닥의 얕은 물웅덩이가 침대 다리를 비춘다.

관계: puddle → reflects → bed.legs; paint → flakes_from → wall
슬롯 제안: space_condition, surface_pattern, reflection_logic
혼동: 폐허를 감염원으로 확정; 젖은 바닥을 체액으로 확정

주장 한계: 쇠락의 외형만 제안한다. 운영 중단·돌봄 부재·오염 성분은 별도 문맥이다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D01 수술포의 시야 차단

연결 용어: Surgical Drape; Local / Regional Anesthesia
처리: still / P0

An opaque drape rises across an adult patient’s upper torso, separating the visible face from a covered lower-body work area.

불투명한 수술포가 성인 환자의 상체를 가로질러 세워져, 보이는 얼굴과 가려진 하체 작업 구역을 나눈다.

관계: drape → separates → patient.face_and_work_area; drape → occludes → patient.lower_body
슬롯 제안: prop_placement, body_region, subject_framing
혼동: 가려진 절개를 보았다고 판정; 국소마취를 실패라고 명명

주장 한계: 수술포와 가림만 확인 가능하다. 의식·통증·마취 종류·가려진 처치는 단정하지 않는다.

근거: [S06 NIGMS Anesthesia](https://www.nigms.nih.gov/education/fact-sheets/Pages/anesthesia)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D02 견인기와 조직 가장자리의 접점

연결 용어: Retractor / Speculum; Surgical Horror
처리: still / P0

Two metal retractor tips hold opposite margins of a fictional tissue opening apart; both tips and both contacted margins remain visible.

금속 견인기 끝 두 개가 가상 조직 개구부의 맞은편 가장자리를 벌리고 있으며, 두 끝과 접촉한 양 가장자리가 모두 보인다.

관계: retractor_a.tip → contacts → opening.left_margin; retractor_b.tip → contacts → opening.right_margin
슬롯 제안: contact_point, object_structure, anatomical_connection
혼동: 공중에 뜬 기구; 검경과 동의어

주장 한계: 형태 연구용 창작 실현이다. 실제 시술 방법·생체 상태·통증·동의를 제시하지 않는다.

근거: [S15 ACS/ASE Postoperative Care](https://www.facs.org/media/iccbhdga/postoperative_care.pdf)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D03 독립된 Cusco형 두 날 검경

연결 용어: Retractor / Speculum
처리: still / P0

A standalone chrome-colored bivalve speculum rests on a tray, with two opposed blades joined to a hinged handle and a visible adjustment screw.

독립된 크롬빛 두 날 검경이 트레이에 놓여 있으며, 마주 보는 두 날이 경첩 손잡이에 연결되고 조절 나사가 보인다.

관계: blades → joined_to → hinged_handle; screw → mounted_on → handle
슬롯 제안: object_structure, prop, surface_material
혼동: 모든 검경의 보편 외형; 구강 개구기

주장 한계: 특정 검경 유형에서 착안한 기구다. 신체 접촉·사용 부위·성적 의미를 자동 추가하지 않는다.

근거: [S36 Science Museum Group Cusco-type speculum](https://collection.sciencemuseumgroup.org.uk/objects/co93477/vaginal-speculum-vaginal-speculum)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D04 배액관 삽입부에서 수집 벌브까지

연결 용어: Catheter / Drain
처리: still / P0

One flexible tube emerges beside a covered abdominal incision on an adult and continues without a gap to a small external collection bulb clipped to the gown.

성인의 덮인 복부 절개부 옆에서 유연한 관 하나가 나와, 환자복에 고정된 작은 외부 수집 벌브까지 끊김 없이 이어진다.

관계: tube → emerges_at → patient.abdomen_entry; tube → connects_to → collection_bulb; bulb → clipped_to → gown
슬롯 제안: anatomical_connection, contact_point, prop_placement
혼동: 정맥 주입관; 중간에 끊긴 관; 벌브가 신체에 융합

주장 한계: 삽입부와 외부 연결만 평가한다. 피부 아래 경로·흡인 작동·배액 성분은 보이지 않는다.

근거: [S34 MSK Caring for Your Jackson-Pratt Drain](https://www.mskcc.org/cancer-care/patient-education/caring-your-jackson-pratt-drain)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D05 주입펌프의 저장부·관·팔 접점

연결 용어: Infusion Pump; Catheter / Drain
처리: still / P0

A fluid bag feeds tubing through a pump beside an adult patient; the same tubing reaches a taped connector on the patient’s forearm.

성인 환자 옆 수액 주머니에서 나온 관이 펌프를 통과하고, 같은 관이 환자 팔뚝의 테이프로 고정된 연결부에 닿는다.

관계: bag → connected_via → tube; tube → passes_through → pump; tube → ends_at → patient.forearm_connector
슬롯 제안: anatomical_connection, prop_placement, contact_point
혼동: 배액 벌브; 관이 모니터로 연결; 속도값을 실제 투여로 취급

주장 한계: 실제 정맥 삽입·유량·약 성분·치료 효과를 외부 연결만으로 입증하지 않는다.

근거: [S35 FDA What Is an Infusion Pump](https://www.fda.gov/medical-devices/infusion-pumps/what-infusion-pump)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D06 입의 튜브와 외부 호흡 회로

연결 용어: Intubation / Mechanical Ventilation
처리: still / P0

An adult’s mouth holds a secured breathing tube whose external connector joins a corrugated breathing circuit leading to a separate ventilator.

성인의 입에 고정된 호흡 튜브의 외부 연결부가 주름진 호흡 회로에 이어지고, 회로는 별도의 인공호흡기로 연결된다.

관계: tube → secured_at → patient.mouth; tube.connector → joins → breathing_circuit; circuit → connects_to → ventilator
슬롯 제안: anatomical_connection, contact_point, prop
혼동: 코 산소관; 마스크; 목으로 관이 관통; 기관 내부 경로 추정

주장 한계: 외부 구강 경로만 평가한다. 올바른 기관 내 위치·실제 환기·의식·생존은 확인 불가.

근거: [S33 NHLBI What Is a Ventilator](https://www.nhlbi.nih.gov/health/ventilator)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D07 밀착 마스크와 호흡 회로

연결 용어: Intubation / Mechanical Ventilation
처리: still / P0

A fitted mask covers an adult’s nose and mouth; a visible connector joins the mask to a corrugated circuit leading to a bedside breathing machine.

밀착 마스크가 성인의 코와 입을 덮고, 보이는 연결부가 마스크와 주름진 회로를 이어 침상 옆 호흡 장치로 연결한다.

관계: mask → covers → patient.nose_and_mouth; mask → connected_to → circuit
슬롯 제안: anatomical_connection, prop, contact_point
혼동: 마스크를 기관삽관으로 명명; 마스크 아래 입을 가시 판정

주장 한계: 비침습적 외부 연결의 제안이며 작동 방식·임상 적합성은 사진만으로 판정하지 않는다.

근거: [S33 NHLBI What Is a Ventilator](https://www.nhlbi.nih.gov/health/ventilator)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D08 기관절개관의 목 연결부

연결 용어: Intubation / Mechanical Ventilation; Mechanical Breathing
처리: still / P1

A short tube flange rests at the front of an adult’s neck, held by a neck strap; its external connector joins a breathing circuit.

짧은 관의 고정판이 성인의 목 앞에 놓여 목끈으로 지지되며, 외부 연결부가 호흡 회로에 이어진다.

관계: flange → at → patient.neck_front; strap → holds → flange; connector → joins → circuit
슬롯 제안: anatomical_connection, contact_point, object_structure
혼동: 구강 튜브; 목 장신구; 관이 온전한 피부에 융합

주장 한계: 별도 목 경로다. 내부 해부·시술 단계·환기 상태는 평가하지 않는다.

근거: [S33 NHLBI What Is a Ventilator](https://www.nhlbi.nih.gov/health/ventilator)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D09 환자복의 등쪽 여밈

연결 용어: Hospital Gown / Identification Band
처리: still / P0

An adult wearing a loose hospital gown is shown from behind; two fabric ties close a narrow overlap along the upper back.

헐렁한 환자복을 입은 성인을 뒤에서 보며, 천 끈 두 개가 등 위쪽의 좁은 겹침을 여민다.

관계: ties → close → gown.back_overlap
슬롯 제안: garment_detail, garment_state, wardrobe_style
혼동: 등 노출을 동의 없는 노출로 단정; 속박 끈

주장 한계: 환자복 외형만 제안한다. 노출 강요·성적 의미·성인 연령 판정은 별도다.

근거: [S26 GMC Intimate examinations and chaperones](https://www.gmc-uk.org/professional-standards/the-professional-standards/intimate-examinations-and-chaperones/intimate-examinations-and-chaperones)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D10 손목 확인 팔찌의 소유자

연결 용어: Hospital Gown / Identification Band
처리: still / P0

A white identification band encircles one adult’s wrist, with its clasp and printed code "AB12" facing the camera.

흰색 확인 팔찌가 성인 한 명의 손목을 둘러싸며, 잠금부와 인쇄된 코드 "AB12"가 카메라를 향한다.

관계: band → encircles → patient.wrist; code → printed_on → band
슬롯 제안: wearable_accessory, visible_text, contact_point
혼동: 바코드만으로 신원 확정; 다른 사람의 손목

주장 한계: 팔찌와 글자만 가시 사실이다. 실제 신원·번호 오류·입원 자격은 판정하지 않는다.

근거: [S45 AHRQ PSNet Diagnostic Errors](https://psnet.ahrq.gov/primer/diagnostic-errors)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D11 서로 다른 코드가 보이는 팔찌와 차트

연결 용어: The Unreliable Chart; Hospital Gown / Identification Band
처리: proxy / P0

An adult’s wristband reads "AB12" while the adjacent chart header reads "AB21"; both short codes are large and legible in the same frame.

성인의 손목 팔찌에는 "AB12", 옆 차트 머리글에는 "AB21"이 적혀 있으며, 두 짧은 코드가 같은 화면에서 크게 읽힌다.

관계: band.code → differs_from → chart.code
슬롯 제안: visible_text, narrative_clue, composition
혼동: 동일 글자; 그럴듯한 가짜 문자; 오진 자동 확정

주장 한계: 문자 불일치만 평가한다. 두 문서가 같은 환자를 가리킴·오진·은폐·시간 역전은 서사 주장이다.

근거: [S45 AHRQ PSNet Diagnostic Errors](https://psnet.ahrq.gov/primer/diagnostic-errors)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D12 밀봉 투명 표본병의 내용과 경계

연결 용어: Specimen Jar / Slide; Biopsy
처리: still / P0

A capped transparent jar contains a small irregular pink specimen submerged below a visible liquid meniscus; the jar stands separate from the body.

뚜껑이 닫힌 투명 병 안에서 작은 불규칙한 분홍 표본이 보이는 액면 아래 잠겨 있으며, 병은 신체와 떨어져 놓여 있다.

관계: specimen → inside → jar; specimen → below → liquid.meniscus
슬롯 제안: liquid_inclusion, object_structure, prop_state
혼동: 불투명 병의 내부; 병 밖에 놓인 표본; 사람 장기 확정

주장 한계: 표본·액면·병의 관계만 보인다. 조직 기원·보존액 성분·생체 상태는 입증하지 않는다.

근거: [S10 NCI Biopsy](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/biopsy)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D13 슬라이드·커버글라스·조직 절편

연결 용어: Specimen Jar / Slide; Histopathology
처리: still / P0

A thin tinted tissue section lies on a rectangular glass slide beneath a smaller coverslip, with a label occupying one end of the slide.

직사각 유리 슬라이드 위에 얇게 착색된 조직 절편이 작은 커버글라스 아래 놓이고, 라벨이 슬라이드 한쪽 끝을 차지한다.

관계: section → between → slide_and_coverslip; label → at_end_of → slide
슬롯 제안: object_structure, prop_placement, scale_relation
혼동: 육안 장기; 절편 위의 미니어처 인체

주장 한계: 가시 배치의 창작 제안이다. 조직학적 진단·염색법·확대율은 별도 검증한다.

근거: [S10 NCI Biopsy](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/biopsy)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D14 치과 의자와 분리된 진료 기구

연결 용어: Dental Horror
처리: still / P0

A reclined dental chair sits beneath a focused examination lamp; a handpiece and a small mirror lie on a separate tray beside the chair.

뒤로 기울어진 치과 의자 위에 집중형 진료등이 있고, 핸드피스와 작은 거울이 의자 옆 별도 트레이에 놓여 있다.

관계: lamp → above → chair; handpiece → on → tray; mirror → on → tray
슬롯 제안: location, prop, prop_placement
혼동: 수술실; 드릴 소리를 가시 판정; 치과를 고문으로 등치

주장 한계: 기구·공간의 실현이다. 실제 드릴 작동·통증·폭력·공포증 진단을 확정하지 않는다.

근거: [S03 Tracing dental horror in contemporary American cinema](https://intellectdiscover.com/content/journals/10.1386/host_00077_1)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D15 얼굴 마스크의 인공 경계

연결 용어: Cosmetic Surgery Horror; The Perfect Replacement
처리: still / P1

A smooth pale face mask covers an adult’s face, with separate eye openings and a thin visible rim above the jaw.

매끈하고 옅은 얼굴 마스크가 성인의 얼굴을 덮으며, 두 눈 구멍과 턱 위의 얇은 가장자리가 구별되어 보인다.

관계: mask → covers → patient.face; mask.rim → above → patient.jaw
슬롯 제안: prop, facial_geometry, contact_point
혼동: 얼굴 피부 자체; 복제 정체성 확정

주장 한계: 작품에서 착안한 독립 소품 제안이다. 수술 성공·기증자·본래 얼굴·실제 영화 마스크 동일성은 주장하지 않는다.

근거: [S38 Criterion Eyes Without a Face](https://www.criterion.com/films/950-eyes-without-a-face)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D16 표면을 잇는 봉합사의 경로

연결 용어: Surgical Horror; Scar / Contracture
처리: still / P0

Short dark suture loops cross a narrow closed seam on fictional skin; each visible loop meets both opposing margins.

가상 피부의 좁게 닫힌 이음선을 짧고 어두운 봉합사 고리들이 가로지르며, 각 고리가 맞은편 양 가장자리에 닿는다.

관계: suture.loops → bridge → seam.opposing_margins
슬롯 제안: skin_condition, contact_point, surface_pattern
혼동: 봉합을 흉터로 취급; 끈이 피부 위에 떠 있음

주장 한계: 봉합 형태만 평가한다. 치유 시점·시술 원인·동의·특정 수술은 알 수 없다.

근거: [S14 Cleveland Clinic Wound Dehiscence](https://my.clevelandclinic.org/health/diseases/wound-dehiscence)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W01 봉합선의 부분 벌어짐

연결 용어: Wound Dehiscence
처리: proxy / P0

On fictional skin, a previously sutured seam has a central gap between opposing margins; remaining sutures still bridge the closed sections at both ends.

가상 피부의 봉합선 중앙에서 맞은편 가장자리가 벌어지고, 양끝의 닫힌 구간에는 봉합사가 남아 연결되어 있다.

관계: gap → between → seam.margins; sutures → bridge → seam.closed_ends
슬롯 제안: skin_condition, anatomical_connection, contact_point
혼동: 처음부터 열린 절개; 외부로 돌출된 장기

주장 한계: 봉합선·틈의 형태 제안이다. 이전에 닫혔다 다시 열렸다는 시간적 이력은 스틸로 증명하지 않는다.

근거: [S14 Cleveland Clinic Wound Dehiscence](https://my.clevelandclinic.org/health/diseases/wound-dehiscence), [S15 ACS/ASE Postoperative Care](https://www.facs.org/media/iccbhdga/postoperative_care.pdf)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W02 개구부 경계 밖으로 이어지는 조직

연결 용어: Wound Evisceration
처리: still / P1

In a fictional anatomical model, a loop of internal tissue continues through an abdominal opening and protrudes beyond the plane of the surrounding skin.

가상의 해부 모형에서 내부 조직 고리가 복부 개구부를 통과해 이어지고, 주변 피부면 바깥으로 돌출한다.

관계: tissue.loop → continues_through → abdomen.opening; tissue.loop → projects_beyond → skin.plane
슬롯 제안: body_form, anatomical_connection, body_region
혼동: 절개 속에만 보이는 조직; 분리된 장기; 정상 통로 탈출

주장 한계: 교육적 가상 모델의 연결 구조다. 살아 있는 사람의 상태·원인·사후 여부를 판정하지 않는다.

근거: [S15 ACS/ASE Postoperative Care](https://www.facs.org/media/iccbhdga/postoperative_care.pdf)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W03 누공의 두 끝을 보이는 단면 도식

연결 용어: Fistula
처리: still / P1

A clearly illustrative cutaway model shows a narrow continuous channel connecting one hollow organ wall to a separate skin opening; both endpoints are visible.

명백한 단면 모형에 좁고 연속적인 통로가 속 빈 기관의 벽과 별도의 피부 개구부를 이어 주며, 양 끝이 모두 보인다.

관계: channel → connects → organ.wall_and_skin.opening
슬롯 제안: anatomical_connection, object_structure, medium
혼동: 피부의 한 구멍; 카테터; 내부 경로를 사진에서 투시

주장 한계: 단면 모형의 관계만 검증한다. 통로의 자연 발생·수술적 생성·질병 원인을 확정하지 않는다.

근거: [S12 NCI Fistula](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/fistula)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W04 정상 통로 방향의 조직 돌출 모형

연결 용어: Prolapse
처리: still / P2

A labeled anatomical cutaway model shows a tissue segment displaced down a pre-existing passage and extending through that passage’s outlet.

라벨이 있는 해부 단면 모형에서 조직 일부가 기존 통로를 따라 아래로 이동한 위치에 있고, 그 통로의 출구 밖까지 이어져 있다.

관계: tissue.segment → extends_through → passage.outlet
슬롯 제안: anatomical_connection, body_form, medium
혼동: 새로 찢어진 복부 상처; 처진 외부 피부

주장 한계: 일반적 공간 관계의 창작 도식이다. 부위별 임상 정의와 정확한 모델은 추가 전문 자료가 필요하다.

근거: [S12 NCI Fistula](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/fistula)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W05 피부층과 하부층의 분리 모형

연결 용어: Degloving Injury
처리: still / P1

A fictional cutaway model shows an outer skin flap separated from an underlying soft-tissue layer, with the two layers still joined at one edge.

가상 단면 모형에서 바깥 피부 피판과 하부 연조직층이 떨어져 있으며, 한쪽 가장자리에서는 두 층이 이어져 있다.

관계: skin.flap → separated_from → underlying_tissue; skin.flap → joined_at → remaining_edge
슬롯 제안: body_form, anatomical_connection, medium
혼동: 완전 절단; 표면 긁힘; 폐쇄형 박리 자동 표면화

주장 한계: 열린 층 분리의 도식 제안이다. 모든 박리 손상이 열린 상처를 갖는다는 뜻이 아니다.

근거: [S16 NHS Hand Injuries: closed degloving](https://www.rightdecisions.scot.nhs.uk/media/jujp5l25/hand-injuries-dec-24.pdf)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W06 검고 건조한 표면의 한정 패치

연결 용어: Necrosis; Gangrene
처리: proxy / P1

A sharply bounded dark, dry patch interrupts the lighter surrounding surface of a fictional anatomical model.

가상의 해부 모형에서 경계가 뚜렷한 어둡고 건조한 패치가 주변의 옅은 표면을 끊는다.

관계: dark_patch → bounded_within → model.surface
슬롯 제안: skin_condition, surface_pattern, texture
혼동: 검은 분장을 괴사 진단; 괴사와 괴저를 완전 동의어화

주장 한계: 색과 표면의 대리 실현이며 조직 사망·혈류·감염·질병을 진단하지 않는다.

근거: [S11 NCI Necrosis](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/necrosis)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W07 표면 결손의 깊이와 가장자리

연결 용어: Ulceration
처리: proxy / P1

A fictional surface model has one shallow recessed defect with a visible rim and an uneven floor, rather than a raised bump.

가상의 표면 모형에 보이는 테두리와 고르지 않은 바닥을 지닌 얕은 함몰 결손 하나가 있으며, 솟은 돌기가 아니다.

관계: defect.floor → below → surrounding_surface
슬롯 제안: skin_condition, object_structure, texture
혼동: 농양; 붉은색 반점; 병명 추정

주장 한계: 형상만 제안한다. 특정 궤양·종양·감염·병기는 별도 근거가 필요하다.

근거: [S47 NCI Ulcer](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/ulcer)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W08 공간에 모인 불투명 액체의 단면 모형

연결 용어: Abscess
처리: proxy / P1

A fictional cutaway model shows a localized cavity containing opaque yellow fluid, with the cavity wall separate from the surrounding solid tissue.

가상 단면 모형에서 국소 공동 안에 불투명한 노란 액체가 모이고, 공동 벽이 주변의 고형 조직과 구별된다.

관계: opaque_fluid → inside → localized_cavity
슬롯 제안: liquid_inclusion, object_structure, medium
혼동: 표면의 노란색을 고름으로 확정; 액체를 병원체로 등치

주장 한계: 농양을 설명하기 위한 창작 대리 도식이다. 액체 성분·감염·미생물을 외형으로 확정하지 않는다.

근거: [S48 NCI Abscess](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/abscess)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W09 모형 표본 안의 이질적 조직형

연결 용어: Teratoma
처리: proxy / P1

A clearly fictional opened specimen model contains a tuft of hair-like fibers and a small hard white fragment within the same rounded mass.

명백한 가상 절개 표본 모형에서 털 같은 섬유 다발과 작고 단단해 보이는 흰 조각이 하나의 둥근 덩어리 안에 함께 있다.

관계: fibers → inside → specimen.mass; white_fragment → inside → specimen.mass
슬롯 제안: object_structure, material_form, prop
혼동: 소형 인간; 태아; 의식 있는 덩어리; 모든 기형종 동일형

주장 한계: 여러 조직형이라는 개념의 창작 대리형이다. 기형종 진단·양악성·실제 조직 정체는 입증하지 않는다.

근거: [S13 NCI Teratoma](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/teratoma)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W10 흉터의 유한한 선과 당겨진 표면

연결 용어: Scar / Contracture
처리: proxy / P0

A pale raised scar crosses an adult model’s forearm; adjacent skin folds converge toward one end of the scar.

성인 모형의 팔뚝을 옅게 솟은 흉터가 가로지르며, 이웃 피부 주름들이 흉터 한쪽 끝으로 모인다.

관계: skin.folds → converge_toward → scar.end
슬롯 제안: skin_condition, surface_pattern, body_region
혼동: 새 봉합사; 흉터만으로 구축 기능장애 확정

주장 한계: 흉터·당김 형태만 평가한다. 운동 제한·통증·외상 원인·시간은 보이지 않는다.

근거: [S14 Cleveland Clinic Wound Dehiscence](https://my.clevelandclinic.org/health/diseases/wound-dehiscence)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W11 절단단과 별도 의지의 경계

연결 용어: Amputation; Phantom Limb Pain
처리: still / P1

An adult figure has a healed residual forearm ending above the wrist, while a separate prosthetic hand rests on the nearby table.

성인 인물의 치유된 잔여 팔뚝이 손목 위에서 끝나며, 별도의 의수 손이 가까운 탁자 위에 놓여 있다.

관계: residual_forearm → ends_above → wrist_position; prosthetic_hand → separate_from → figure
슬롯 제안: body_form, body_region, prop_placement
혼동: 가림 때문에 손이 안 보임; 의수가 신체에 붙음; 환상지통 가시 확정

주장 한계: 신체 끝과 분리된 소품만 제안한다. 통증·절단 원인·정체성·불완전한 인간이라는 가치판단은 부여하지 않는다.

근거: [S06 NIGMS Anesthesia](https://www.nigms.nih.gov/education/fact-sheets/Pages/anesthesia)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## W12 연속 신체에 붙은 가상 패치 이음선

연결 용어: Transplantation; Foreign-Body Reaction; The Perfect Replacement
처리: proxy / P1

A clearly fictional skin patch lies flush within an adult model’s surrounding skin, with a continuous oval seam tracing the patch boundary.

명백한 가상의 피부 패치가 성인 모형의 주변 피부와 같은 높이에 놓이고, 연속적인 타원형 이음선이 패치 경계를 따라간다.

관계: patch → flush_with → surrounding_skin; seam → traces → patch.boundary
슬롯 제안: anatomical_connection, skin_condition, contact_point
혼동: 이음선만으로 이식·거부반응 확정; 동물 유전자 외형화

주장 한계: 창작 이음선일 뿐 실제 이식·면역 반응·기증자·기억 전이를 입증하지 않는다.

근거: [S22 MedlinePlus Transplant rejection](https://medlineplus.gov/ency/article/000815.htm)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## L01 작은 배양 구조의 용기·눈금

연결 용어: Organoid; Tissue Engineering
처리: still / P0

A shallow culture dish contains several tiny rounded tissue-like structures; a visible millimeter scale beside the dish keeps their small size explicit.

얕은 배양 접시에 작은 둥근 조직 유사 구조들이 담겨 있고, 접시 옆의 밀리미터 눈금이 작은 크기를 명시한다.

관계: structures → inside → dish; scale → beside → dish
슬롯 제안: scale_relation, prop, object_structure
혼동: 육안 완전 장기; 배양 접시 속 소형 사람

주장 한계: 실험용 배양 구조의 창작 제안이다. 특정 장기 기능·의식·세포 기원을 판정하지 않는다.

근거: [S21 NCI Organoid](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/organoid)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## L02 배양 플라스크·라벨·관찰 배율의 분리

연결 용어: Immortal Cell Line; Biobanking / Nonconsensual Tissue Use
처리: proxy / P0

A translucent culture flask with a small external identifier stands beside a microscope image on a separate screen; the screen image stays inside its bezel.

작은 외부 식별자가 붙은 반투명 배양 플라스크가 별도 화면의 현미경 영상 옆에 있고, 영상은 화면 테두리 안에만 머문다.

관계: identifier → on → flask; micrograph → inside → screen.bezel
슬롯 제안: prop, visible_text, scale_relation
혼동: 플라스크만으로 불멸성·HeLa·동의 침해 확정

주장 한계: 증식 지속성·개인·계약·동의는 비가시 문맥이다. HeLa의 비동의 채취는 NIH 검색 본문에서 재확인했으나 용기 외형으로 시료 신원을 확인할 수 없다.

근거: [S21 NCI Organoid](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/organoid), [S32 NIH-Lacks Family Agreement](https://grants.nih.gov/policy-and-compliance/policy-topics/sharing-policies/dms/privacy/nih-lacks-family-agreement)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## L03 반복 시료의 재고 배치

연결 용어: Organ Farm; Corporate Medical Horror; Reproductive Commodification
처리: proxy / P1

Identical sealed specimen containers occupy numbered rack positions; one empty position interrupts the regular grid.

동일한 밀봉 표본 용기들이 번호가 있는 랙 위치에 놓이고, 빈자리 하나가 규칙적인 격자를 끊는다.

관계: containers → occupy → rack.positions; empty_position → interrupts → grid
슬롯 제안: prop_placement, composition, narrative_clue
혼동: 용기를 인간 사육으로 확정; 반복형을 동일 유전자 복제로 확정

주장 한계: 재고 배치는 상품화의 창작 대리형이며 장기 밀매·사람 생산·불법성은 입증하지 않는다.

근거: [S02 Transplantation Gothic: The bioemporium](https://www.cambridge.org/core/books/abs/transplantation-gothic/bioemporium-corporate-medical-horror-in-late-twentiethcentury-american-transfer-fiction/6395F77E3425618EEC30E7AF532C276D), [S40 Sitges Antiviral](https://sitgesfilmfestival.com/en/film/2012/antiviral)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## L04 기구 표면의 막과 묻은 물질

연결 용어: Biofilm; Contamination; Surgical Site Infection
처리: proxy / P1

A close view of a fictional catheter connector shows a thin translucent film adhering to its outer surface, with the connector edges still distinct.

가상 도관 연결부를 가까이 보면 얇은 반투명 막이 외부 표면에 붙어 있고, 연결부의 가장자리가 여전히 구별된다.

관계: film → adheres_to → connector.outer_surface
슬롯 제안: surface_material, texture, prop_state
혼동: 광택·점액을 실제 생물막으로 확정; 집락화를 감염으로 확정

주장 한계: 막의 외형은 창작 대리형이다. 세균·생물막·감염·병원 기원을 사진만으로 진단하지 않는다.

근거: [S17 CDC About HAIs](https://www.cdc.gov/healthcare-associated-infections/about/index.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## L05 닫힌 생물안전 구역의 장갑 경계

연결 용어: Pathogen; Contamination; Healthcare-Associated Infection
처리: still / P0

A gloved hand holds a capped specimen tube entirely inside a transparent work enclosure; the enclosure wall remains between the tube and the viewer.

장갑 낀 손이 뚜껑이 닫힌 시료 튜브를 투명 작업함 안에서 들고 있으며, 작업함 벽이 튜브와 관객 사이에 남아 있다.

관계: hand → holds → tube; tube → inside → enclosure
슬롯 제안: contact_point, prop_placement, object_structure
혼동: 장갑을 무균 인증으로 취급; 튜브가 유리를 관통

주장 한계: 밀폐·접촉 위치만 평가하며 실제 생물안전 등급·병원체·오염 방지는 입증하지 않는다.

근거: [S17 CDC About HAIs](https://www.cdc.gov/healthcare-associated-infections/about/index.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## L06 가상 생물과 숙주 사이의 단일 접점

연결 용어: Parasitism; Parasitic Gestation
처리: proxy / P1

A clearly fictional small organism grips the outside of a larger creature through one visible attachment pad; the two bodies retain separate outer contours.

명백한 가상의 작은 생물이 보이는 부착판 하나로 더 큰 생물의 외부를 붙잡고 있으며, 두 몸의 바깥 윤곽은 분리되어 있다.

관계: organism.pad → attached_to → host.outer_surface
슬롯 제안: anatomical_connection, contact_point, scale_relation
혼동: 장신구; 융합체; 실제 임신을 기생 질환으로 취급

주장 한계: 가상 부착 관계다. 영양 교환·기생·번식·유전자 관계는 스틸로 입증하지 않는다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## L07 허구 인공 배양 장치의 빈 챔버

연결 용어: Ectogenesis / Artificial Womb; Organ Farm
처리: still / P2

A clearly fictional empty fluid chamber connects to two external tubes and a control panel; no body or embryo is present inside the chamber.

명백한 허구의 빈 유체 챔버가 외부 관 두 개와 조작 패널에 연결되어 있으며, 챔버 안에는 몸이나 배아가 없다.

관계: chamber → connected_to → tube_a; chamber → connected_to → tube_b; panel → beside → chamber
슬롯 제안: object_structure, prop, prop_placement
혼동: 완전한 인간 생산 공장의 현실화; 조산 지원 연구와 등치

주장 한계: 장치의 허구적 외형 제안이다. 생식 기능·승인 현황·발달 지원 능력을 뜻하지 않는다.

근거: [S24 FDA Artificial Womb Technology 2023 Summary](https://www.fda.gov/media/172441/download)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## L08 체내 장치와 외부 통신 표시의 분리

연결 용어: Connected Implant
처리: proxy / P2

A clearly illustrative cutaway shows a small implanted device beneath skin; a separate external receiver displays a wireless-link symbol.

명백한 단면 도식에 작은 장치가 피부 아래 놓여 있고, 별도의 외부 수신기 화면에 무선 연결 기호가 표시되어 있다.

관계: device → beneath → skin; wireless_symbol → on → receiver.screen
슬롯 제안: object_structure, anatomical_connection, visible_text
혼동: 기호를 실제 연결·해킹으로 확정; 외부 장치가 체내로 융합

주장 한계: 신호·보안 침해·원격 통제는 외형으로 입증 불가하며 특정 의료기기 설계 사실을 주장하지 않는다.

근거: [S35 FDA What Is an Infusion Pump](https://www.fda.gov/medical-devices/infusion-pumps/what-infusion-pump)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E01 침상 난간과 닿지 않는 호출기

연결 용어: Institutional Horror; Caregiver–Captor
처리: proxy / P0

An adult lies behind a raised bed rail while the call handset rests on a wall hook beyond the adult’s outstretched hand.

성인이 올린 침상 난간 안에 누워 있고, 호출기는 성인이 뻗은 손이 닿지 않는 벽 고리에 걸려 있다.

관계: rail → between → patient_and_handset; handset → beyond → patient.hand
슬롯 제안: proxemics, prop_placement, body_pose
혼동: 침상 안전장치를 고문으로 확정; 거리 때문에 동의 상실 확정

주장 한계: 거리와 장애물만 가시 사실이다. 감금 의도·돌봄 방치·환자의 능력은 서사 문맥이다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E02 피부에 닿는 넓은 억제대와 고정점

연결 용어: Physical / Chemical Restraint; Bodily Autonomy
처리: proxy / P1

A broad padded strap crosses a clothed adult model’s forearm and connects visibly to the bed frame on either side.

넓고 패드가 있는 끈이 옷을 입은 성인 모형의 팔뚝을 가로지르고, 양쪽에서 침대 틀에 연결되는 고정점이 보인다.

관계: strap → crosses → model.forearm; strap.ends → attached_to → bed.frame
슬롯 제안: contact_point, object_structure, body_pose
혼동: 의복 끈; 성적 구속 자동화; 약물적 억제를 끈으로 표현

주장 한계: 물리적 장치만 제안한다. 강요·법적 지위·동의·임상 필요·성적 의미는 판단하지 않는다.

근거: [S25 HHS Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/index.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E03 서명칸·가려진 본문·넘겨진 페이지

연결 용어: Consent Trap; Informed Consent
처리: proxy / P0

An adult hand holds a multipage form open to a large signature box while a folded upper sheet hides most of the surrounding body text.

성인의 손이 여러 장짜리 서류를 큰 서명칸이 보이도록 펼치고 있으며, 접힌 윗장이 주변 본문 대부분을 가린다.

관계: hand → holds → form; folded_sheet → occludes → form.body_text
슬롯 제안: narrative_clue, prop_placement, contact_point
혼동: 서명만으로 충분한 동의; 가림을 사기로 확정

주장 한계: 서류·가림의 관계만 평가한다. 이해·자발성·계약 효력·은폐 의도는 별도다.

근거: [S25 HHS Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/index.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E04 검사 화면 앞에서 가려지는 얼굴

연결 용어: Medical Gaze; Dehumanization / Objectification; Anatomical Fragmentation
처리: proxy / P0

A large medical-image display occupies the foreground while an adult patient remains partly hidden behind it; the display and the person remain separate objects.

큰 의료 영상 화면이 전경을 차지하고 성인 환자는 그 뒤에 일부 가려져 있으며, 화면과 인물은 별개 물체로 남아 있다.

관계: display → occludes → patient.part; display → foreground_to → patient
슬롯 제안: composition, visual_hierarchy, subject_framing
혼동: 인체와 영상의 융합; 의사 악의 확정

주장 한계: 구도는 대상화의 창작 대리형이다. 실제 비인간화·직업적 태도·진단은 사진에서 확정하지 않는다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976), [S45 AHRQ PSNet Diagnostic Errors](https://psnet.ahrq.gov/primer/diagnostic-errors)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E05 불가능한 구조가 화면 안에만 존재

연결 용어: Impossible Medical Imaging; The Uncanny
처리: still / P0

A clearly fictional scan on a monitor shows three nested rib-like rings in one chest silhouette; the adult beside the monitor has no visible external rings.

모니터의 명백한 허구 스캔은 가슴 실루엣 하나 안에 겹친 갈비뼈 모양 고리 세 개를 보여 주며, 모니터 옆 성인의 외부에는 고리가 보이지 않는다.

관계: rings → inside → screen.scan_chest; scan → inside → monitor.bezel
슬롯 제안: surreal_concept, object_structure, prop
혼동: 화면 속 형상을 신체에 이식; 실제 X선 소견

주장 한계: 허구 영상의 화면 내 내용만 평가한다. 실제 내부 해부·진단·초자연적 원인은 입증하지 않는다.

근거: [S41 British Council The Autopsy of Jane Doe](https://filmsandfestivals.britishcouncil.org/projects/the-autopsy-of-jane-doe)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E06 수술 시연의 관객·유리·작업대

연결 용어: Surgical Spectacle; Surgical Eroticism
처리: proxy / P1

Behind a glass partition, several adult observers face an illuminated demonstration table; a clothed adult model lies on the table beneath an opaque drape.

유리 칸막이 뒤에서 성인 관람자 여러 명이 조명된 시연대를 바라보고, 옷을 입은 성인 모형이 불투명한 천 아래 시연대에 누워 있다.

관계: glass → separates → observers_and_table; observers → face → table
슬롯 제안: composition, participant_role, proxemics
혼동: 수술 이름으로 성적 의미 자동화; 관객을 의료진과 합침

주장 한계: 관람 배치만 제안한다. 실제 수술·동의·공연 목적·관객 욕망은 비가시 문맥이다.

근거: [S37 Rijksmuseum Boerhaave Anatomical Theatre](https://www.rijksmuseumboerhaave.nl/en/our-worlds/anatomical-theatre), [S42 BFI Crimes of the Future](https://www.bfi.org.uk/sight-and-sound/reviews/crimes-future-darkly-funny-world-organ-ised-crime)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E07 신체 노출을 줄이는 진료 가림막

연결 용어: Nonconsensual Intimate Examination; Forced Exposure; Medical Voyeurism
처리: proxy / P0

An opaque privacy screen stands between an adult patient in a closed gown and a doorway, blocking the doorway’s view of the patient’s lower body.

불투명 사생활 가림막이 여민 환자복을 입은 성인 환자와 출입문 사이에 서서, 출입문 쪽에서 환자의 하체를 볼 수 없게 한다.

관계: screen → between → patient_and_door; screen → occludes → patient.lower_body_from_door
슬롯 제안: prop_placement, subject_framing, proxemics
혼동: 가림막 존재로 동의 증명; 임상 노출을 페티시로 등치

주장 한계: 가림의 범위만 평가한다. 비동의·관음·강제·검사 실행을 가시 사실로 바꾸지 않는다.

근거: [S26 GMC Intimate examinations and chaperones](https://www.gmc-uk.org/professional-standards/the-professional-standards/intimate-examinations-and-chaperones/intimate-examinations-and-chaperones)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E08 설정된 성인 의료 역할극의 소품

연결 용어: Medical Fetishism; Consensual Medical Roleplay
처리: proxy / P2

On a clearly staged studio set, two fully clothed adult performers stand beside a prop examination chair; one wears a stylized white coat and holds unused gloves.

명백히 연출된 스튜디오 세트에서 옷을 완전히 입은 성인 연기자 두 명이 소품 진료 의자 옆에 서며, 한 명은 양식화된 흰 가운을 입고 쓰지 않은 장갑을 들고 있다.

관계: performer_a → holds → gloves; performers → beside → prop_chair
슬롯 제안: attire_context, staging_degree, participant_role
혼동: 실제 진료 관계; 의료복만으로 성적 관심·동의 확정

주장 한계: 성인·연출은 명시적 설정 조건이다. 동의나 성적 취향은 외형으로 승인하지 않으며 성적 연출은 별도 요청 차원이다.

근거: [S28 APA Paraphilic Disorders](https://www.psychiatry.org/File%20Library/Psychiatrists/Practice/DSM/APA_DSM-5-Paraphilic-Disorders.pdf)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E09 문밖에 놓인 퇴원 서류와 닫힌 문

연결 용어: Discharge Denial; Institutional Betrayal
처리: proxy / P1

A short sheet labeled "DISCHARGE" sits on a desk beyond a closed glazed door, while an adult stands on the near side of the door.

"DISCHARGE"라고 적힌 짧은 서류가 닫힌 유리문 너머 책상에 놓이고, 성인은 문 이쪽에 서 있다.

관계: door → between → adult_and_document; document → on → desk
슬롯 제안: visible_text, proxemics, narrative_clue
혼동: 문이 닫혔다고 잠금·감금 확정; 퇴원 거부가 가시 사실

주장 한계: 문·인물·서류의 위치만 보인다. 퇴원 자격·규정·강제입원·동의는 서사 문맥이다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E10 같은 장면의 거울과 얼굴 차이

연결 용어: The Perfect Replacement; Depersonalization / Derealization
처리: still / P2

In a clearly surreal staged image, an adult faces a mirror whose reflected face has a different artificial mask rim, while the body pose and room edges otherwise align.

명백히 초현실적으로 연출된 이미지에서 성인이 거울을 보며, 반사된 얼굴에는 다른 인공 마스크 가장자리가 있고 몸 자세와 방의 가장자리는 그 밖에는 맞아 있다.

관계: reflection.face_rim → differs_from → adult.face_rim; reflection.room_edges → align_with → room.edges
슬롯 제안: reflection_logic, surreal_concept, facial_geometry
혼동: 실제 카그라 망상 진단; 다른 거울 각도를 정체성 교체로 단정

주장 한계: 허구 반사 차이만 평가한다. 망상·인격·기증자 기억·정신질환은 입증하지 않는다.

근거: [S38 Criterion Eyes Without a Face](https://www.criterion.com/films/950-eyes-without-a-face)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D17 바늘과 떨어진 손의 거리

연결 용어: Trypanophobia; Iatrophobia; Tomophobia
처리: proxy / P0

A clothed adult holds one hand against their own chest while an unused capped syringe remains on a tray at arm’s length, without touching the body.

옷을 입은 성인이 한 손을 자기 가슴에 대고 있으며, 쓰지 않은 뚜껑 달린 주사기가 팔 길이만큼 떨어진 트레이에 놓여 몸에 닿지 않는다.

관계: syringe → on → tray; hand → against → adult.chest; syringe → separate_from → adult
슬롯 제안: body_pose, prop_placement, proxemics
혼동: 바늘 접촉; 공포증 진단; 통증의 증명

주장 한계: 거리·손 자세는 창작 대리형이다. 실제 공포·회피 동기·공포증은 판정하지 않는다.

근거: [S06 NIGMS Anesthesia](https://www.nigms.nih.gov/education/fact-sheets/Pages/anesthesia)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## D18 머리 표면의 전극과 별도 장치

연결 용어: Electroconvulsive Therapy, ECT
처리: proxy / P1

An adult anatomical mannequin has two separate electrode pads on the scalp, with visible leads ending at a separate tabletop device.

성인 해부 마네킹의 두피에 전극 패드 두 개가 따로 놓이고, 보이는 전선이 별도의 탁상 장치로 이어진다.

관계: pads → on → mannequin.scalp; leads → connect → pads_and_device
슬롯 제안: contact_point, object_structure, prop
혼동: 전기고문; 로보토미; 전극만으로 ECT 확정

주장 한계: 외부 장치 도식이며 실제 ECT·전류·치료·동의·의식을 입증하지 않는다. 절차나 설정값은 제공하지 않는다.

근거: [S09 NIMH Brain Stimulation Therapies](https://www.nimh.nih.gov/health/topics/brain-stimulation-therapies/brain-stimulation-therapies)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## L09 서로 다른 코드가 붙은 같은 외형의 시료

연결 용어: Chimerism; Mosaicism; Cloning / Genetic Engineering; Xenotransplantation
처리: proxy / P1

Two visually similar sealed sample tubes stand side by side, labeled "SOURCE A" and "SOURCE B"; neither contains a visible miniature organism.

외형이 비슷한 밀봉 시료 튜브 두 개가 나란히 있고 각각 "SOURCE A", "SOURCE B"로 표시되며, 어느 쪽에도 육안으로 보이는 소형 생물은 없다.

관계: label_a → on → tube_a; label_b → on → tube_b; tubes → beside → each_other
슬롯 제안: visible_text, prop_placement, object_structure
혼동: 동일 외형을 복제 증거로 취급; 라벨을 유전자 검사로 취급

주장 한계: 보이는 것은 표기 차이뿐이다. 키메라·모자이크·이종이식·복제·유전자 조작은 입증하지 않는다.

근거: [S20 NCI Chimerism](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/chimerism), [S23 FDA Xenotransplantation](https://www.fda.gov/vaccines-blood-biologics/xenotransplantation)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E11 얼굴은 보이고 작업부는 가려진 시선

연결 용어: Accidental Awareness; Local / Regional Anesthesia; General Anesthesia
처리: proxy / P0

An adult’s open eyes face the lower edge of an opaque surgical drape while the covered work area remains entirely hidden behind it.

성인의 열린 눈이 불투명 수술포의 아래 가장자리를 향하고 있으며, 덮인 작업 구역은 수술포 뒤에 완전히 가려져 있다.

관계: eyes → oriented_toward → drape.edge; drape → occludes → work_area
슬롯 제안: gaze_target, subject_framing, prop_placement
혼동: 눈이 열렸으므로 각성 사고 확정; 통증·의식·기억 등치

주장 한계: 눈·수술포의 관계만 제안한다. 의식 보존 국소마취·전신마취 우발적 각성·단순 연출을 사진만으로 구별하지 않는다.

근거: [S06 NIGMS Anesthesia](https://www.nigms.nih.gov/education/fact-sheets/Pages/anesthesia), [S07 ASA Awareness and Anesthesia](https://www.asahq.org/~/media/sites/asahq/files/public/resources/patient-brochures/asa_awareness-anesthesia_final.pdf?la=en)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E12 하나의 신체 일부로 제한된 프레이밍

연결 용어: Anatomical Fragmentation; Medical Gaze
처리: still / P0

A tight photograph frames one adult forearm on a clinical support, excluding the face and the rest of the body while keeping the forearm continuous within the frame.

조밀한 사진 구도가 진료 받침대 위 성인의 팔뚝 하나를 담고, 얼굴과 나머지 신체는 화면 밖에 두되 팔뚝은 화면 안에서 연속적으로 보인다.

관계: frame → includes → adult.forearm; frame → excludes → adult.face
슬롯 제안: subject_framing, body_region, composition
혼동: 실제 절단; 신체 파편을 자동 생성

주장 한계: 프레이밍과 신체 절단은 다른 의미다. 얼굴 부재는 비인간화·신원 상실의 증거가 아니다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## E13 해부 기록과 덮인 운반대의 역사 대리형

연결 용어: Resurrectionists / Body Snatchers; Corpse Medicine / Medicinal Cannibalism; Medical Gothic
처리: proxy / P2

In a clearly fictional historical study, a canvas-covered stretcher rests beside an open ledger labeled "1811"; no contents are visible beneath the cover.

명백한 허구의 역사적 서재에서 천으로 덮인 운반대가 "1811"이라고 적힌 펼친 장부 옆에 있고, 덮개 아래 내용은 보이지 않는다.

관계: cover → occludes → stretcher.contents; ledger → beside → stretcher
슬롯 제안: historical_period, prop_placement, narrative_clue
혼동: 도굴 사건 재현을 실제 사료로 취급; 덮개 아래 시신 확정

주장 한계: 1811–12년 런던 기록에서 착안한 창작 소품 배치다. 거래·도굴·시체 약재·내용물은 입증하지 않는다.

근거: [S29 RCS Diary of a resurrectionist](https://www.rcseng.ac.uk/library-and-publications/library/blog/diary-of-a-resurrectionist/)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X01 장르·하위 경향

연결 용어: Medical Horror; Medical Gothic; Biomedical Horror; Body Horror; Surgical Horror; Clinical Horror; Hospital Horror; Institutional Horror; Medical Thriller; Dental Horror; Cosmetic Surgery Horror; Reproductive Horror; Gynaehorror; Transplantation Gothic; Corporate Medical Horror; Biopunk; Splatter / Gore; Torture Porn
처리: advisory / P2

주장 한계: 장르 라벨은 검색 문맥이다. 병원·어둠·고어·나체·성적 의미·폭력 강도를 자동 의무로 만들지 않는다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976), [S02 Transplantation Gothic: The bioemporium](https://www.cambridge.org/core/books/abs/transplantation-gothic/bioemporium-corporate-medical-horror-in-late-twentiethcentury-american-transfer-fiction/6395F77E3425618EEC30E7AF532C276D), [S03 Tracing dental horror in contemporary American cinema](https://intellectdiscover.com/content/journals/10.1386/host_00077_1), [S04 Women, Monstrosity and Horror Film: Gynaehorror](https://www.routledge.com/Women-Monstrosity-and-Horror-Film-Gynaehorror-1st-Edition/Harrington/p/book/9781315546568?PageSpeed=noscript)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X02 비평 개념과 관측의 경계

연결 용어: Medical Gaze; Bodily Autonomy; Bodily Integrity; Abjection; The Uncanny; Grotesque; Biopower; Medicalization / Pathologization; Dehumanization / Objectification; Monstrous-Feminine
처리: context / P2

주장 한계: 비평 용례와 창작 해석을 구별한다. 개인의 신체·여성·장애·질병에 본질적 괴물성·열등성을 부여하지 않는다. 개별 이론의 원전 정의는 추가 확인 대상이다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976), [S04 Women, Monstrosity and Horror Film: Gynaehorror](https://www.routledge.com/Women-Monstrosity-and-Horror-Film-Gynaehorror-1st-Edition/Harrington/p/book/9781315546568?PageSpeed=noscript), [S25 HHS Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/index.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X03 진단 불확실성과 오류

연결 용어: Diagnostic Uncertainty; Differential Diagnosis; Diagnostic Error; False Negative / False Positive; Idiopathic; Iatrogenic; Adverse Event; Medical Gaslighting; Diagnostic Overshadowing
처리: context / P2

주장 한계: 증상·검사·실제 상태·시점·원인의 관계를 필요로 한다. 차트 불일치나 불안한 얼굴로 오진·과실·악의·가스라이팅을 확정하지 않는다.

근거: [S45 AHRQ PSNet Diagnostic Errors](https://psnet.ahrq.gov/primer/diagnostic-errors)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X04 마취·진정·진통·운동·기억의 독립 축

연결 용어: General Anesthesia; Local / Regional Anesthesia; Sedation; Analgesia; Neuromuscular Blockade; Accidental Awareness; Amnesia
처리: context / P2

주장 한계: 의식·통증·움직임·회상은 다른 축이다. 국소마취 중 깨어 있음은 곧 실패가 아니며, 움직이지 않는 모습만으로 통증이나 무의식을 단정하지 않는다. 약리 세부는 후속 전문 자료로 검토한다.

근거: [S06 NIGMS Anesthesia](https://www.nigms.nih.gov/education/fact-sheets/Pages/anesthesia), [S07 ASA Awareness and Anesthesia](https://www.asahq.org/~/media/sites/asahq/files/public/resources/patient-brochures/asa_awareness-anesthesia_final.pdf?la=en)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X05 혼수·폐쇄증후군·뇌사

연결 용어: Coma; Locked-in Syndrome; Brain Death
처리: context / P2

주장 한계: 세 상태를 같은 병상 외형으로 합치지 않는다. 혼수 정의는 확인했으나 폐쇄증후군·뇌사의 세부 판정 기준은 이 연구에서 승인하지 않는다. 표정·열린 눈·장치만으로 진단 금지.

근거: [S08 MedlinePlus Coma](https://medlineplus.gov/coma.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X06 공포증·지각·망상

연결 용어: Iatrophobia; Nosocomephobia; Trypanophobia; Tomophobia; Nosophobia; Mysophobia / Germophobia; Hallucination; Depersonalization / Derealization; Capgras Delusion; Cotard Delusion; Delirium
처리: context / P2

주장 한계: 특정 공포·망상·섬망의 임상 정의·진단은 별도 조사 대상이다. 장면은 주관적 지각의 허구적 대리형으로만 저술하고 외형을 실제 개인 진단으로 사용하지 않는다.

근거: [S45 AHRQ PSNet Diagnostic Errors](https://psnet.ahrq.gov/primer/diagnostic-errors)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X07 주관적 통증과 기대 효과

연결 용어: Phantom Limb Pain; Nocebo Effect
처리: context / P2

주장 한계: 통증·노시보의 인과는 비가시다. NCI는 기대와 관련된 증상 발생으로 노시보를 정의한다. 환상지통의 전문 정의는 추가 확인 대상이며, 부위 부재나 약병만으로 통증·기대를 입증하지 않는다.

근거: [S06 NIGMS Anesthesia](https://www.nigms.nih.gov/education/fact-sheets/Pages/anesthesia), [S51 NCI Nocebo effect](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/nocebo-effect)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X08 혈류·산소·위축의 비가시성

연결 용어: Ischemia; Hypoxia; Atrophy
처리: context / P2

주장 한계: 허혈의 혈액 공급 부족과 저산소의 산소 공급 감소는 구별된다. 색·가는 사지를 진단으로 바꾸지 않는다. 위축의 세부 정의와 전후 변화는 추가 전문 자료가 필요하다.

근거: [S49 NCI Ischemia](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/ischemia), [S50 NCI Hypoxia](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/hypoxia)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X09 오염·집락화·감염·생물막

연결 용어: Pathogen; Contamination; Colonization; Healthcare-Associated Infection; Surgical Site Infection; Biofilm
처리: context / P2

주장 한계: 표면에 물질이 묻음, 미생물 존재, 조직 감염, 발병, 의료관련성은 각각 다르다. 현미경·배양·병력을 장식 소품만으로 대체하지 않는다.

근거: [S17 CDC About HAIs](https://www.cdc.gov/healthcare-associated-infections/about/index.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X10 전염·기생·프리온·패혈증

연결 용어: Parasitism; Zoonosis; Prion Disease; Sepsis
처리: context / P2

주장 한계: 기생은 관계, 인수공통 전염은 전파 경로, 프리온은 접힘 이상, 패혈증은 감염 반응의 위기다. 동물·관·검은 혈액 하나를 공통 증거로 사용하지 않는다.

근거: [S18 CDC About Prion Diseases](https://www.cdc.gov/prions/about/), [S19 WHO Sepsis](https://www.who.int/news-room/fact-sheets/detail/sepsis)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X11 면역 반응·이물·이식의 구별

연결 용어: Transplantation; Transplant Rejection; Immunosuppression; Foreign-Body Reaction; Xenotransplantation
처리: context / P2

주장 한계: 이식의 종·재료·면역 반응과 외부 봉합선은 별개다. 이종이식을 동물 외형으로 바꾸거나 모든 임플란트 문제를 이식 거부반응으로 부르지 않는다.

근거: [S22 MedlinePlus Transplant rejection](https://medlineplus.gov/ency/article/000815.htm), [S23 FDA Xenotransplantation](https://www.fda.gov/vaccines-blood-biologics/xenotransplantation)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X12 유전적 기원과 외형

연결 용어: Chimerism; Mosaicism; Cloning / Genetic Engineering
처리: context / P2

주장 한계: 서로 다른 세포 기원·발달 과정·유전정보 조작은 외형만으로 확인되지 않는다. 모자이크의 세부 정의는 추가 조사 대상이며 복제는 기억·인격의 동일성 증거가 아니다.

근거: [S20 NCI Chimerism](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/chimerism), [S23 FDA Xenotransplantation](https://www.fda.gov/vaccines-blood-biologics/xenotransplantation)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X13 배양·인공자궁·세포의 지속성

연결 용어: Organoid; Tissue Engineering; Immortal Cell Line; Ectogenesis / Artificial Womb; Organ Farm; Donor-Memory Transfer; Connected Implant
처리: context / P2

주장 한계: 배양 구조·실험 장치와 사람의 의식·생식 기능·기억 전이·통신 침해를 분리한다. 기증자 기억 전이는 허구 가정이며 인공자궁 자료는 2023년 연구 목적까지만 지지한다.

근거: [S21 NCI Organoid](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/organoid), [S24 FDA Artificial Womb Technology 2023 Summary](https://www.fda.gov/media/172441/download)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X14 동의·능력·강요

연결 용어: Informed Consent; Decision-Making Capacity; Coercion; Undue Influence; Therapeutic Misconception; Medical Paternalism; Non-Maleficence
처리: context / P2

주장 한계: 동의는 정보·이해·자발성과 범위·시점이 필요하다. 서명·미소·고개 끄덕임을 충분한 동의 또는 의사결정능력의 증명으로 사용하지 않는다. 상세 능력·법역 기준은 별도다.

근거: [S25 HHS Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/index.html), [S26 GMC Intimate examinations and chaperones](https://www.gmc-uk.org/professional-standards/the-professional-standards/intimate-examinations-and-chaperones/intimate-examinations-and-chaperones)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X15 제도·노동·권한·착취

연결 용어: Research Exploitation; Dual Loyalty; Institutional Betrayal; Involuntary Admission; Physical / Chemical Restraint; Biobanking / Nonconsensual Tissue Use; Organ Trafficking
처리: context / P2

주장 한계: 기관의 의도·법적 권한·거래·동의 이력은 외형 밖의 사실이다. 합법적 기증·돌봄·약물치료를 장기밀매·약물적 억제로 자동 재명명하지 않는다.

근거: [S02 Transplantation Gothic: The bioemporium](https://www.cambridge.org/core/books/abs/transplantation-gothic/bioemporium-corporate-medical-horror-in-late-twentiethcentury-american-transfer-fiction/6395F77E3425618EEC30E7AF532C276D), [S25 HHS Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/index.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X16 생식권과 강제 변경

연결 용어: Reproductive Coercion; Forced Pregnancy; Forced Abortion; Forced / Coerced Sterilization; Obstetric Violence; Forced Alteration of Sex Characteristics; Castration / Genital Mutilation
처리: context / P2

주장 한계: 임신·출산·불임화·성징 변경의 강제·선택 여부는 몸의 외형으로 확정되지 않는다. 치료·자기 선택·폭력·차별의 문맥을 각각 보존한다. 특정 법률 정의는 별도 검증한다.

근거: [S26 GMC Intimate examinations and chaperones](https://www.gmc-uk.org/professional-standards/the-professional-standards/intimate-examinations-and-chaperones/intimate-examinations-and-chaperones), [S27 WHO Involuntary sterilization statement](https://www.who.int/publications/i/item/9789241507325)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X17 성적 경계·관음·역할극의 분리

연결 용어: Nonconsensual Intimate Examination; Sexual Boundary Violation; Medical Voyeurism; Medical Fetishism; Consensual Medical Roleplay; Forced Exposure; Surgical Eroticism; Necrophilia
처리: context / P2

주장 한계: 임상 노출·성적 관심·연출·동의·비동의·시신 대상 행위는 별개다. 의료복만으로 페티시·장애·동의·성폭력 또는 시체성애를 판정하지 않는다. 비동의 성행위는 선정적 시각 후보로 변환하지 않는다.

근거: [S26 GMC Intimate examinations and chaperones](https://www.gmc-uk.org/professional-standards/the-professional-standards/intimate-examinations-and-chaperones/intimate-examinations-and-chaperones), [S28 APA Paraphilic Disorders](https://www.psychiatry.org/File%20Library/Psychiatrists/Practice/DSM/APA_DSM-5-Paraphilic-Disorders.pdf), [S42 BFI Crimes of the Future](https://www.bfi.org.uk/sight-and-sound/reviews/crimes-future-darkly-funny-world-organ-ised-crime)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X18 실험·고문·살아 있음·사후 검사

연결 용어: Mad Scientist / Rogue Surgeon; Medical Torture; Nonconsensual Human Experimentation; Vivisection; Dissection / Autopsy; Lobotomy / Leucotomy; Self-Surgery; Electroconvulsive Therapy, ECT
처리: context / P2

주장 한계: 기구·절개·전극은 고문·실험 목적·동의·생존·사망의 증거가 아니다. 현대 ECT·역사적 정신외과·형벌적 전기폭력을 합치지 않는다. 구체적 처치나 위해 방법은 후보 내용으로 넣지 않는다.

근거: [S09 NIMH Brain Stimulation Therapies](https://www.nimh.nih.gov/health/topics/brain-stimulation-therapies/brain-stimulation-therapies), [S25 HHS Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/read-the-belmont-report/index.html), [S29 RCS Diary of a resurrectionist](https://www.rcseng.ac.uk/library-and-publications/library/blog/diary-of-a-resurrectionist/)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X19 시신·부활·약용 신체의 역사와 허구

연결 용어: Resurrectionists / Body Snatchers; Reanimation; Corpse Medicine / Medicinal Cannibalism; Necrophilia
처리: context / P2

주장 한계: 도굴 역사와 허구적 재활성화·의학적 소생은 구별한다. 약용 식인·시체성애의 개별 역사·진단 정의는 후속 원전 조사가 필요하며, 덮인 운반대·해부 관심으로 추정하지 않는다.

근거: [S29 RCS Diary of a resurrectionist](https://www.rcseng.ac.uk/library-and-publications/library/blog/diary-of-a-resurrectionist/), [S46 NLM Frankenstein exhibition](https://www.nlm.nih.gov/exhibition/frankenstein/exhibition3.html)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X20 전후·원인·결과가 필요한 연출

연결 용어: Clinical Detachment; The Unreliable Chart; Escalating Treatment; The False Cure; Discharge Denial; Consent Trap; The Perfect Replacement; Caregiver–Captor; Menstrual Horror; Maternal Horror; Reproductive Commodification; Parasitic Gestation; Medical Cover-up
처리: sequence / P2

주장 한계: 치료가 커짐·효과·기억·규정 변경·정체성·은폐는 시간·대사·서사가 필요하다. 한 장의 기구 수·서류·붉은 액체로 전후 인과·월경·임신·악의를 입증하지 않는다.

근거: [S01 Medical Humanities and the Twentieth-Century Gothic](https://academic.oup.com/edinburgh-scholarship-online/book/56658/chapter-abstract/453346976), [S02 Transplantation Gothic: The bioemporium](https://www.cambridge.org/core/books/abs/transplantation-gothic/bioemporium-corporate-medical-horror-in-late-twentiethcentury-american-transfer-fiction/6395F77E3425618EEC30E7AF532C276D), [S04 Women, Monstrosity and Horror Film: Gynaehorror](https://www.routledge.com/Women-Monstrosity-and-Horror-Film-Gynaehorror-1st-Edition/Harrington/p/book/9781315546568?PageSpeed=noscript)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X21 시간적 호흡과 음향

연결 용어: Mechanical Breathing; Fluorescent Hum; Somatic Sound
처리: audio / P2

주장 한계: 기계 주기·호흡 동기화·형광등 소음·조직 마찰음은 정지 이미지에서 청취할 수 없다. 주름관·조명·습한 표면은 소리의 대리형일 뿐이다.

근거: [S33 NHLBI What Is a Ventilator](https://www.nhlbi.nih.gov/health/ventilator)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.

## X22 역사적 사례와 잘못된 과학

연결 용어: Eugenics; Nonconsensual Human Experimentation; Biobanking / Nonconsensual Tissue Use; Forced / Coerced Sterilization
처리: historical / P2

주장 한계: 터스키기는 고의 감염으로 바꾸지 않는다. 우생학적 서열은 사실이 아닌 차별적 주장이다. HeLa의 1951년 비동의 채취와 2013년 합의는 NIH 검색 본문으로 재확인했으며 세포 지속성을 개인 의식의 지속성으로 설명하지 않는다.

근거: [S30 NHGRI Eugenics and Scientific Racism](https://www.genome.gov/about-genomics/fact-sheets/Eugenics-and-Scientific-Racism), [S31 CDC Tuskegee study](https://www.cdc.gov/tuskegee/about/), [S32 NIH-Lacks Family Agreement](https://grants.nih.gov/policy-and-compliance/policy-topics/sharing-policies/dms/privacy/nih-lacks-family-agreement)

판정: 명시한 모든 관계·끝점·수가 함께 보여야 한다. `UNOBSERVABLE_NOT_PASS`, `partial_is_fail`. 운영·native 승인 미수행.
