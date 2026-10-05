"""Author planned behavioral probes and pixel gates. Does not execute tests."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent

# Concrete probes for implementation review, not generated synonym permutations.
# A new research-unit ID must be bound to its adopted stable runtime ID before
# these can become executable regressions.
CASES='''
R001|3|성찰적으로 원고를 돌아보는 성인, 반사 재료는 요청하지 않음.|thoughtful 문맥을 보존하고 선택적 작업 관계만 노출.|reflective의 표면 반사 의미에서 금속·거울을 강제.|ia_revision_sequence
R002|3|반사가 있는 금속 책상, 사람은 없음.|반사 재질 뜻과 nonhuman 소유자를 보존.|성찰하는 사람·얼굴·책 읽기를 추가.|ia_reflection_reference
R003|4|내면을 돌아보는 일지를 쓰는 인물.|내적 상태의 실제 판별 대신 요청한 일지·행위 관계를 제안.|introverted 성격·우울·정신 건강 판정.|ia_pause_work
R004|5|동일 문단을 곱씹는 인물의 한 장 사진.|반복 흔적은 선택적으로 표현하고 지속 시간 검증은 미지원 표시.|실제 반추 시간·병적 상태를 PASS로 기록.|ia_revision_sequence
R005|7,9|호기심 있게 자료를 묻는 인물, 의심하거나 옆눈 뜨지 않음.|질문 자료의 참조, negation 소유를 보존.|skeptical_side_eye나 비판적 표정 강제.|ia_followup_question
R006|8,16|어수선한 책상에서 같은 기준의 A/B 자료를 체계적으로 분석.|순서·같은 기준·표 대응을 중심으로 제안.|방을 정리하거나 옷을 교수풍으로 교체.|ia_comparison_matrix
R007|10,11|두 도면의 접합부 차이를 예리하게 확인하는 성인.|같은 접합부 참조 관계를 제안.|범죄자·권력자·고급 의상·타인 추가.|ia_drawing_model
R008|12,13|학구적인 성인, 책 한 권과 짧은 주석만, 옷 고정.|주석의 같은 행 대응, appearance 잠금 보존.|서가·안경·트위드·학위·교수 신분 강제.|ia_annotation_anchor
R009|14|관능적인 의상을 유지한 이지적 작업 초상.|cerebral의 사고 문맥과 고정 의상 축을 각각 보존.|cerebral 때문에 관능 제거·무표정·하이넥 강제.|ia_structured_board
R010|15|교수풍의 설명 자세, 나이·성별·의상 변경 금지.|참조하는 보드·설명 관계만 허용 범위에서 제안.|중년 남성·실제 교수·트위드 교체.|ia_teaching_reference
R011|17|calm measured response while listening, no measuring tools.|신중한 대응 문맥을 유지.|자·캘리퍼·측량을 measured라는 단어로 활성화.|ia_listening_reference
R012|17|자가 놓인 길이를 measured한 기록, 사람 없음.|물리 측정 문맥과 object count를 유지.|신중한 얼굴·대화 상대 생성.|ia_ruler_measure
R013|18|박학한 인물의 간단한 인용 메모, 현학적 비꼼 제외.|erudite와 pedantic의 평가적 차이를 보존.|pedantic 별칭·비꼼·지적 우월감을 긍정 검색에 혼입.|ia_reference_link
R014|19,140|옷을 입은 성인의 로댕형 턱 괴기, wardrobe 잠금.|반대 허벅지–팔꿈치–턱 지지, 옷 보존.|Thinker라는 이름만으로 누드·조각 매체 전환.|ia_thinker_support
R015|20|종교 표지 없는 오른발–왼 무릎–오른 뺨 자세.|중립 포즈 기하만 required 가능.|보살·연꽃·광배·불교 신분 자동 추가.|ia_pensive_support
R016|20|반가사유 보살 도상을 명시한 조각 사진.|중립 포즈와 명시 종교 프로파일을 분리하여 함께 검토.|일반 figure-four만으로 도상 전체 충족 주장.|ia_pensive_support
R017|21,25|엄지로 턱 아래, 검지로 뺨, 팔꿈치는 책상 위.|정확한 국소 접점과 지지 사슬.|전완 교차 지지·목 잡기·떠 있는 손 대체.|ia_chin_cradle
R018|23,24|손끝끼리 맞대고 손바닥은 떨어뜨린 동일 인물 양손.|pv_steepled_fingers 재사용과 동일 actor 소유.|손깍지·합장·파트너 손 혼입.||
R019|23,24|동일 인물 양손을 깍지끼고 숙고, 책략가 아님.|pv_interlaced_fingers 재사용과 mood 문맥 유지.|mastermind·위협·배후 계획을 손 모양으로 활성화.||
R020|26|등 뒤에서 왼손으로 오른 손목을 잡아 도면 관찰.|지정 laterality와 손목 접촉.|양손이 보이지 않는 뒷짐만으로 접촉 PASS.|ia_wrist_behind_back
R021|27|카메라 위치 고정, 앉은 골반은 유지, 몸통만 앞으로 경청.|몸통–골반 각도와 받침, camera 잠금.|카메라를 당겨와 전방 기울기 흉내.|ia_listening_reference
R022|29|등받이에 기대고 펜을 낮춘 성인.|back-chair 접촉·pelvis-seat 지지.|등받이에 닿지 않은 공중 상체·졸림 추론.|ia_reclined_support
R023|31,105|왼 엄지는 페이지 여백, 오른 펜은 교정 지점 접촉.|손 역할·좌우·행 앵커의 binding 유지.|양손 모두 펜·필기 손 교체·본문 가림.|ia_page_hold,ia_proofread
R024|32|책에 붙은 한 장의 모서리를 집어 살짝 들어올린.|page-root 연결·단일 페이지·pinch 접촉.|분리 낱장·이중 손가락·페이지 관통.|ia_page_turn_endpoint
R025|33,105|펜 끝이 종이에 닿지 않고 작은 간격 위에서 멈춘.|hover의 비접촉을 required로 검토.|proofreading의 실제 필기 접촉으로 바꾸기.|ia_pen_hover
R026|34,35|안경을 벗어 한 손에 들고 얼굴에는 안경 없음.|같은 프레임의 단일 물체 상태.|얼굴과 손에 동일 안경 중복·프레임 디자인 변경.|ia_glasses_removed
R027|35,93|기존 검은 안경을 유지하고 브리지에 한 손끝만.|브리지 접촉만 허용, wardrobe/eyewear property lock 보존.|얇은 금속 프레임 교체·렌즈 관통·안경 제거.|ia_glasses_bridge
R028|36|안경 윗선 너머로 동료를 보되 고개 각도는 고정.|프레임 높이와 현재 눈 방향의 효과를 정직하게 신고.|고개 들기·연령 추가로 뜻을 대체.|ia_over_glasses
R029|37,41|도표 A를 펜으로 가리키는, 손바닥 설명은 요구하지 않음.|pointer endpoint와 A target 연결.|generic open palm만 채택하여 지시 성공 주장.|ia_deictic_reference
R030|38,39|두 손으로 실제 모형의 폭을 표현.|concrete span과 reference width 대응.|추상 A/B 선택지의 은유를 하드 활성화.|ia_iconic_span
R031|39|A/B 두 대안을 서로 다른 손 위치에 대응시킨 스틸.|자료 라벨로 abstract relation을 명시, 형상만의 한계 기록.|두 손 위치만으로 발화 뜻을 픽셀 확정.|ia_metaphoric_options
R032|40,57,59,82|비트 몸짓·시선 왕복·깨달음 전환·랙 포커스를 한 장에서 검증.|시간 속성 네 개를 미지원/별도 매체 필요로 기록.|열린 손·놀란 얼굴·한 초점 상태를 전환 PASS로 기록.||
R033|42|1·2 논점 자료와 두 손가락 세기, 1인 count 고정.|finger count·numbered item·hand owner 일치.|손·인물 증가 또는 무관한 숫자.|ia_enumeration
R034|43,51|책의 오른 페이지 두 번째 문단을 내려보는.|gaze target과 source anchor 결속.|카메라 응시·슬픔·복종 의미 추가.|ia_gaze_reference
R035|44|살짝 눈꺼풀 틈을 좁힌 표정, 기존 눈 형태 고정.|국소 expression 변화와 identity/appearance 잠금 보존.|half-lidded·좁은 눈 형태 영구 변경.||
R036|46|왼쪽 눈썹만 올리고 오른쪽은 유지.|ae_single_brow laterality와 반대쪽 윤곽 보존.|양쪽 눈썹 상승·얼굴 전체 비틀기.||
R037|47|고개를 오른쪽으로 기울이되 배경 수평선 고정.|머리–몸 축과 camera roll 분리.|더치 틸트만으로 질문 자세 충족.||
R038|48,49|닫힌 입술을 누른 표정, 둥글게 오므리거나 내밀지 않음.|ae_lip_press positive, purse/pucker negation guards.|purse·pucker 별칭을 lip press로 합침.||
R039|48|입꼬리를 중심으로 모아 입구만 좁힌, 앞으로 내밀지 않음.|ae_purse와 pucker의 국소 형태 분리.|키스·관능·입술 돌출을 자동 추가.||
R040|50,52|위쪽 응시, 기억·거짓말 의미 없음.|gaze form만 allowed, cognition inference 없음.|눈 방향으로 회상·기만·진실 판정.||
R041|54,55|양쪽 작은 미소, 한쪽 미소·성숙한 나이 제외.|closed bilateral smile와 연령 잠금 보존.|mature_knowing_smile로 나이·비대칭 추가.||
R042|62|얼굴을 사분의 삼 방향에서 촬영, 체형·광대 고정.|camera_direction 의미 활성, anatomical morphology 비활성.|malar_forward_projection 또는 3/4 길이 크롭으로 대체.||
R043|63|업무용 profile 문서가 놓인 책상, 얼굴은 정면 고정.|profile document 문맥과 front camera 잠금.|side_profile_view로 얼굴 방향 변경.||
R044|64,65|눈높이 측면 시점, 카메라 방향은 profile 고정.|height와 direction 효과를 독립 신고.|eye-level 때문에 정면 교체·대등한 관계 자동 추론.||
R045|66|책상을 수직으로 내려보는, 사선 감시 카메라 제외.|top_down_90/strict_top_down_flat_view 재사용, 평면 관계.|security-high-corner/birds-eye의 사선 변형으로 대체.||
R046|67,68|얼굴 타이트 클로즈업 잠금과 책상 전체의 작은 원고까지 필수.|충돌을 밝히고 후보 거절·합리적 재협의 필요 표시.|효과를 expression 하나로 축소해 framing 잠금을 우회.|ia_evidence_frame
R047|70,72|1인만 있는 작업 초상, OTS·투숏 추가 금지.|count=1 잠금으로 partner shoulder/two actors 후보 거절.|촬영자·동료를 몰래 추가하여 OTS 구현.|ia_ots_reference,ia_shared_reference
R048|71|자기 시점의 손과 문서를 보여주는, 다른 인물 없음.|viewpoint owner와 foreground hand owner 일치.|관찰자 얼굴·타인의 손·두 번째 사람을 추가.|ia_pov_work
R049|73,74|중앙 인물에 좌우 대칭 배경, 삼분할 제외.|center placement와 symmetry 요소 모두 보존.|rule_of_thirds를 덮어써서 symmetry 침해.||
R050|75,76|왼쪽을 보는 얼굴, 왼쪽 여백, 필수 문서 유지.|gaze-side look room과 document crop 보존.|오른쪽 빈 영역·머리 위 여백만으로 충족.|ia_look_room
R051|79,80|전경 손·중경 얼굴·후경 보드, 후경은 흐려도 됨.|deep-space staging required, deep focus optional/금지 조건 보존.|깊이 배치만으로 모두 sharp를 강제.|ia_deep_layers
R052|81|얕은 심도 잠금, 눈·펜 접점·한 줄 자료는 같은 가까운 면.|실제 깊이 배치와 필요한 focus/geometry 효과를 함께 검토.|서로 먼 층의 필수 텍스트를 같은 초점이라고 무조건 주장.|ia_evidence_frame
R053|84|유리에 한 사람 얼굴이 반사되고 너머 도표는 투과.|reflection source·glass plane·transmitted document 분리.|두 실제 사람·무작위 얼굴 복제로 reflection PASS.|ia_reflection_reference
R054|86|렘브란트 얼굴광, 카메라 쪽 얼굴 면적은 변경 금지.|기존 rembrandt_face_light_pattern과 독립 camera lock 보존.|short-lighting 방향을 렘브란트 필수로 강제.|ia_rembrandt_reference
R055|87,88|하이키지만 흰 원고의 경계와 주석은 읽힘.|밝은 저대비 관계와 document detail 유지.|blown-out page로 high-key PASS.||
R056|89,90|화면 속 오른쪽 스탠드가 책상을 비추며 모니터는 꺼짐.|practical source ownership와 방향, screen-light 비활성.|푸른 보정이나 꺼진 모니터로 screen light 충족.|ia_screen_light
R057|94,95|니트 밖 셔츠 칼라만, 팔꿈치 패치·트위드 제외.|layer boundary만 선택, unwanted patch/material guards.|교수풍이라는 이유로 패치·트위드 추가.|ia_shirt_knit_layers
R058|97,98|원문 두 번째 행 주석과 세 번째 행 교정이 각각 있음.|서로 다른 document anchor와 annotation/correction type 유지.|모든 빨간 표시를 한 문단 또는 무작위 낙서로 통합.|ia_annotation_anchor,ia_correction_anchor
R059|99,108|A/B 같은 기준 표와 (2,3) 데이터 점의 대응.|common headers·row matching·units·point correspondence.|표의 값과 점이 다른데 차트가 있다는 이유로 성공.|ia_comparison_matrix,ia_data_analysis
R060|100,106|x+3=7 → x=4 두 단계만 보드에, 새로운 방정식 금지.|정확한 짧은 fixture와 arrow/node/hand 연결.|임의 고급 수식·잘못된 변형·관계 없는 화살표.|ia_structured_board,ia_derivation
R061|101|캘리퍼 두 턱이 하나의 물체 양면에 접촉, 자·확대경 없음.|caliper-specific contact와 단일 tool binding.|일반 ruler 후보·추가 도구·물체 관통.|ia_caliper_measure
R062|104|두 판본의 같은 문단 A와 차이 메모.|passage pair·difference note·pointer target 일치.|서로 무관한 두 책을 comparative-edition 성공으로 기록.|ia_edition_compare
R063|107|example.py 3행 오류와 같은 줄의 코드·traceback을 검토.|filename/line/source/inspection 대응, short validated fixture.|무관한 코드·에러 또는 실제 수정 완료 주장.|ia_debugging
R064|109,110|실험 장치 S1 눈금과 S1 기록, 현장 측량 도구 없음.|apparatus/log identifier·state 대응.|field-measure scene·과학자 직업·도구 군집 자동 추가.|ia_experiment_log
R065|111|도면 A와 모형 A의 같은 접합부를 펜으로 지시.|2D/3D joint identity·pointer relation.|무관한 청사진·관절 이름 불일치.|ia_drawing_model
R066|112|체스 e4 칸 기록 복기, 바둑 돌 없음.|8×8 squares·piece-square/record anchor 연결.|바둑 교차점·임의 전략 능력·국면 합법성 자동 인증.|ia_chess_review
R067|112|바둑 B3 교차점 기록 복기, 체스 말 없음.|stone centered on intersection·record identity.|돌을 칸 중심에 배치·체스 표기 혼입.|ia_go_review
R068|114,115|악보 2마디 주석 또는 짧은 원문/번역문 대응을 요청.|각 source/target anchor와 검증 fixture를 구분.|악보를 텍스트 번역으로 매칭·임의 음표의 정확성 주장.|ia_score_study,ia_translation
R069|116,120|두 성인이 같은 초안 2행에 관한 서로 다른 검토 의견.|공유 근거·actor A/B·writer/reviewer 역할 binding.|손·문서 소유자 교체·실제 평가 완료 주장.|ia_shared_reference,ia_peer_review
R070|118,119|질문자 쪽을 보고 펜은 낮추되 필기하지 않음.|현재 gaze target·pen absent contact·shared missing step.|일반 writing pose 또는 시선 왕복 시간 PASS.|ia_listening_reference,ia_followup_question
R071|121,123|심야 붓 필사, 시대·신분 고증은 지정하지 않음.|현재 도구 접촉·원문 대응·광원만 제안, historical pending 표시.|특정 조선 시대·선비 신분·밤샘 시간을 사실로 추가.|ia_night_work,ia_brush_copy
R072|124|잎의 주맥과 스케치 같은 위치를 비교.|specimen/sketch feature correspondence.|다른 잎맥·실제 종 이름·자연학자 신분 자동 판정.|ia_naturalist_sketch
R073|125,126,127|긱 시크 안경만, 밝은 공간·고정 의상·관능 없음.|accessory-local 선택, dark setting·adult axis 비활성.|다크 아카데미아 공간·사무실·노출을 일괄 추가.|ia_geek_frame_scene
R074|128|안경 쓴 독서 인물 사진에서 sapiosexual 여부를 추정하지 말 것.|identity inference 없음, 실제 orientation 분류 프로파일 생성 안 함.|사진의 안경·책으로 성적 지향 hard match.|ia_adult_shared_interest
R075|129,130,132|명시 성인 1인 오피스 사이렌 독서, 의상 노출·체형 고정.|reading relation와 선택 스타일을 독립 효과로 검토.|탈의·과장 체형·회사원 권력 관계·책 삭제.|ia_office_style,ia_adult_reading_style
R076|131|두 성인의 지적 플러팅 연출, 같은 책·현 시선만.|명시 count/adult/role와 shared passage 보존, 비시각 해석 경계.|실제 욕망·동의·연애 이력·성적 지향을 픽셀 PASS.|ia_adult_shared_interest
R077|133,134|손끝을 맞댄 성인, 깨진 유리나 범죄 서사 없음.|pv_steepled_fingers만 재사용, trace/story 비활성.|mastermind·폭력·위협 흔적 자동 활성화.|ia_neat_danger_contrast,ia_plan_reference
R078|135,136|허구 실험실의 성인 두 사람이 기록 검토, 심문·진단 없음.|experiment relation·explicit roles만 제안.|interrogation·정신질환·유죄·고문을 장소에서 유추.|ia_fiction_experiment,ia_interrogation_reference
R079|137|허구 지도 A구역과 t1 보고서 비교, 현재 실제 전쟁 제외.|map/report/time identity relation만, fictional frame 보존.|실제 최신 작전·전략 능력·실세계 표적 자동 추가.|ia_warroom_reference
R080|138|E1 봉인 종이 포장·E1 사진·E1 기록을 비교.|ID equality·seal continuity·fixture-specific packaging.|E2 혼입·봉인 훼손·생물학 증거의 무조건 비닐 포장·유죄 인증.|ia_evidence_compare
R081|139|줄무늬 창 그림자가 있는 일반 독서실, 감금 서사 제외.|일반 setting과 reading 유지.|철창 그림자 의미로 수감·감금 활성화.|ia_confined_read
R082|140|성인 조각의 고전 누드 사유 자세, 실제 사람 사진으로 변경 금지.|medium/reference-use·explicit adult/nude·support geometry 보존.|살아 있는 사람·자동 체형·의상 강제·누드 없는 Thinker에서 누드 활성화.|ia_classical_contemplation
'''

NATIVE='''
H01|19,21,25|옷을 입은 성인 한 명. 낮은 좌석에서 몸을 앞으로 숙이고 한 팔꿈치를 반대 허벅지에 받쳐 같은 팔의 손으로 턱을 지지. 양발의 받침을 보임.|좌석–골반 지지~반대 허벅지–팔꿈치 접점~같은 팔의 손–턱 접점~몸통 기울기~각 팔·발 연속성~옷·1인 유지|지지 중 하나라도 떠 있음; 부분 포즈만 성공; 자동 누드|ia_thinker_support
H02|31,33|성인 한 명. 왼손 엄지가 오른 페이지 바깥 여백을 누르고 오른손의 펜 끝은 같은 페이지 위에 작은 간격으로 떠 있음.|왼손–오른 페이지 여백 접촉~펜의 오른손 소유~펜 끝–종이 비접촉~책 받침~모든 접점 가독성|손 역할 교체; 펜 접촉; 본문 전체 가림|ia_page_hold,ia_pen_hover
H03|32|성인 한 명이 책의 한 장 모서리를 집어 들어 올린 정지 장면.|단일 페이지~엄지·검지 pinch~페이지 기부의 책 연결~휜 면의 연속성~손목 연속성|분리 낱장; 페이지 관통; 보이지 않는 기부|ia_page_turn_endpoint
H04|34,35,36|짝 비교: A는 안경을 벗어 한 손에 들고 얼굴은 비움. B는 같은 프레임을 착용하고 브리지만 손끝으로 짚음.|각 장의 단일 안경 상태~프레임 동일성~A의 temple grip~B의 bridge contact~렌즈·다리 연결~1인 유지|착용·제거 혼합; 프레임 교체; 손가락 렌즈 관통|ia_glasses_removed,ia_glasses_bridge
H05|37,42|성인 한 명이 표의 A2 셀을 펜으로 가리키며 다른 손의 두 손가락으로 두 항목을 표현.|A2 셀 식별~펜 끝 방향의 A2 연결~같은 actor의 양손~두 손가락 수~자료 번호 대응|무작위 손; 셀 오지시; 손 증가|ia_deictic_reference,ia_enumeration
H06|97,104|두 판본에서 같은 짧은 문단 A를 펴 놓고 차이 메모를 연결. 성인의 한 손은 판본 B 차이 위치를 가리킴.|두 판본 구분~공통 A anchor~차이 표시 대응~메모 참조~정확한 손 target~필수 글자 가독성|무관한 문단; 무작위 낙서; target 불일치|ia_edition_compare,ia_annotation_anchor
H07|98,105,106|성인의 왼손이 종이 여백을 고정하고 오른 펜이 x+3=7에서 x=4로 이어지는 정확한 두 식의 수정 지점에 접촉.|좌우 역할~페이지 지지~pen contact~두 식 정확성~화살표 대응~짧은 fixture 가독성|잘못된 식; pen hover; 원고 크롭|ia_proofread,ia_derivation
H08|107|성인 한 명이 example.py의 3행과 해당 파일·행을 가리키는 짧은 traceback을 같은 화면에서 검토.|filename 일치~line3 anchor 일치~오류 내용 fixture 일치~선택 줄 표시~입력 손 소유~화면 가독성|무작위 코드/오류; 파일·줄 불일치; 수정 성공 주장|ia_debugging
H09|99,108|작은 표의 행 A=(2,3)을 표시하고 x·y 축 단위가 있는 산점도의 같은 점을 성인의 펜으로 지시.|원자료 행~좌표 대응~축·단위~A 표지~펜 방향 연결~텍스트 가독성|다른 점 지시; 단위 누락; 인과·능력 판정|ia_comparison_matrix,ia_data_analysis
H10|101,111|성인 한 명이 모형의 A 접합부 폭을 캘리퍼 두 턱으로 잡고 도면의 같은 A 접합부를 비교.|단일 도구~jaw/object 양면 접촉~캘리퍼 연결~도면/모형 A 대응~손 소유~보이는 접점|도구 군집; 관통; 다른 joint; 수치 정확성 무근거|ia_caliper_measure,ia_drawing_model
H11|112|짝 비교: 체스는 8×8 보드 칸의 e4와 기록. 바둑은 B3 교차점의 돌과 같은 기록.|체스 squares~바둑 intersections~각 말·돌 위치~선택 위치와 기록~혼합 없음~자료 가독성|칸/교차점 뒤바뀜; 임의 승패·전략 PASS|ia_chess_review,ia_go_review
H12|116,118,120|명시 성인 두 명. 작성자와 검토자가 초안 2행과 리뷰 의견을 공유. 작성자는 펜을 낮추고 검토자를 봄.|정확한 두 인물~각 손·문서 소유~line2/comment anchor~작성자의 pen nonwriting~현재 시선 target~자료 보존|역할 교체; 타인 손; 실제 이해·평가 완료 판정|ia_peer_review,ia_listening_reference
H13|70,79,80,81|명시 성인 두 명의 어깨너머 검토. 전경 어깨·중경 얼굴·지정 문서가 구별되고 필요한 접점만 선명. 깊은 초점 변형은 후경 표까지 읽힘.|전경 어깨 소유~target 인물~동일 자료~필수 접점 크롭 보존~깊이 순서~각 변형 focus rule|추가 인물; 모든 층 무조건 sharp; 필수 접점 흐림|ia_ots_reference,ia_deep_layers,ia_evidence_frame
H14|84,86,90|짝 비교: A는 유리에 한 성인의 반사 얼굴과 너머 자료. B는 렘브란트 얼굴광과 가까운 화면의 별도 손빛.|A의 glass/reflect/transmit 소유~반사 인물 수~B의 코·뺨 그림자 연결~shadow-side triangle~screen-to-hand 방향~자료 가독성|무작위 이중 얼굴; 삼각형 없음; 꺼진 화면빛; 자료 소실|ia_reflection_reference,ia_rembrandt_reference,ia_screen_light
H15|125,126,129,132|동일 성인 독서 활동을 밝은 학구풍·다크 아카데미아·명시 관능 의상으로 비교하되 책·좌우 손 역할·읽는 문단은 고정.|동일 actor~책 지지~손 역할~읽기 target~각 setting/wardrobe의 요청 요소~비요청 노출·체형 없음|스타일이 작업 관계 지움; 학생화; 자동 지향·동의 판정|ia_light_study_scene,ia_dark_academia_scene,ia_adult_reading_style
H16|137,138,139|허구 장면 변형: 지도 A와 보고서 A; E1 봉인 포장·사진·기록; 명시 제한 공간에서도 읽히는 책 접촉.|각 variant의 동일 identifier~각 actor/tool 역할~필수 자료 가독성~봉인 연결 또는 장벽 기하~비요청 사건 없음|ID 불일치; 봉인 훼손; 그림자로 감금 추정; 최신 사실·유죄 PASS|ia_warroom_reference,ia_evidence_compare,ia_confined_read
'''

def main():
    units={u['id'] for u in json.loads((HERE/'CANDIDATE-DRAFTS.json').read_text())['candidates']}
    cases=[]
    for line in CASES.strip().splitlines():
        cols=line.split('|')
        # Empty trailing column is accepted in the few pure reuse-only probes.
        rid, terms, request, expected, forbidden, related=cols[:6]
        refs=[x for x in related.split(',') if x]
        assert set(refs)<=units, rid
        cases.append(dict(id=rid,source_term_numbers=[int(x) for x in terms.split(',')],
            request_ko=request, expected_behavior=expected, forbidden_behavior=forbidden,
            proposed_unit_ids=refs, status='PLANNED_NOT_EXECUTED',
            runtime_binding='map research unit IDs to adopted stable slot/profile IDs before executable assertions; compare IDs and role/effect truth, not array order'))
    gates=[]
    for line in NATIVE.strip().splitlines():
        hid,terms,request,required,forbidden,related=line.split('|')
        refs=related.split(',')
        assert set(refs)<=units
        gates.append(dict(id=hid,source_term_numbers=[int(x) for x in terms.split(',')],
            staged_request_ko=request, proposed_unit_ids=refs,
            required_all_of=required.split('~'), fail_if=forbidden,
            partial_is_fail=True, status='PLANNED_NOT_GENERATED_NOT_SCORED',
            evaluation_boundary='Inspect original output pixels and record owner/contact/anchor evidence. Invisible/cropped/illegible/uncertain required elements do not pass. No inferred intelligence, mental health, sexual orientation, consent, guilt, historical accuracy or temporal change as a pixel label.'))
    output=dict(schema_version='intellectual-validation-plan/v1',status='PLAN_ONLY',
        semantic_cases=cases,native_pixel_gates=gates,
        evaluation_sequence=['data structure and source lineage','sense/polarity/context guards','existing-ID deduplication','core assertion binding','profile exposure','candidate selection or justified rejection','effect/lock preservation','final prompt relation survival','original native pixels','user acceptance'],
        measurement_rules={
            'lexical_inventory':'22/140 labels at the audit snapshot is not semantic coverage or retrieval recall',
            'exposure':'for context-eligible cases record expected adopted profile/candidate IDs in emitted immutable v6 pack; separate required and advisory denominator',
            'selection':'record adopted IDs and role bindings; all optional candidates may be rejected with a reason',
            'locks':'zero unapproved changes to actor count, ownership, identity, text, camera, wardrobe, event or property scope',
            'pixels':'each image passes only if every required visible clause passes; keep failures and blocked outputs in the denominator and record cause',
            'temporal':'mark unsupported for single images, never convert an endpoint into sequence evidence',
            'benchmark':'initial pilot H01 H02 H03 H06 H08 H09 H12 plus three separate H15 styles = 10 concrete requests; 2 baseline/enriched arms x 3 independent repetitions = 60 images. Use matched provider/model/size/request/core; record seed only if supported. Remaining paired/variant gates need an explicit expanded image count before execution.',
            'qualification':'100% structural integrity and requested lock preservation; every nominated all-of case must pass its required gates, partial is fail. Small pilot is a bounded qualification, not proof across all requests.',
        })
    (HERE/'REGRESSION-PLAN.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(semantic_cases=len(cases),native_gates=len(gates),status='PLANNED_NOT_RUN')))

if __name__=='__main__': main()
