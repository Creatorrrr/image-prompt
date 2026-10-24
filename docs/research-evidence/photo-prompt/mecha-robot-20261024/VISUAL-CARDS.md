# 메카·로봇 시각 카드 108개

2026-10-24 KST. 모든 카드는 선택적 창작 초안이다. 운영 등록·native 승인·이미지 검증은 아직 없다. 출처는 용어의 구분과 맥락을 지원하고 아래의 구체적인 부품 수·배치·소유 관계는 작성한 제안이다.

## A01 거대 탑승형과 인간 스케일

성인 한 명이 거대한 이족 기계의 열린 흉부 해치 옆 정비 발판에 서 있고 해치 안에는 좌석 크기의 공간이 있다.

An adult stands on a service platform beside an open chest hatch in a towering bipedal machine; the hatch surrounds a seat-sized recess.

- 관계: hatch → part_of → machine; seat_recess → inside → hatch; adult → stands_on → platform; platform → beside → hatch
- 혼동 경계: 착용 외골격, 작은 모형의 접사
- 관찰 한계: 크기 비교는 보이지만 거대함만으로 실전 병기·파일럿 직업을 확정하지 않는다.
- 검토 슬롯: subject, object_structure, scale_relation
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/), [S23](https://en.gundam-official.com/feature/pgu-rx93/images/system_img_chest_250603.png)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A02 인간형 몸 구성

기계의 몸통 위에 별도 머리가 있고 양어깨에 관절 팔 두 개, 골반 아래에 다리 두 개가 이어진다.

A machine has a distinct head above one torso, two articulated arms at the shoulders and two legs below the pelvis.

- 관계: head → above → torso; arms → attached_to → torso; legs → attached_to → pelvis
- 혼동 경계: 사람 외관을 재현한 안드로이드, 인간 의식
- 관찰 한계: 몸 구성이 인간형이라는 뜻이며 피부·성별·자율성을 요구하지 않는다.
- 검토 슬롯: body_form, object_structure
- 출처 범위: [S05](https://bostondynamics.com/blog/electric-new-era-for-atlas)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A03 안드로이드의 표면과 점검구

사람을 닮은 인공 얼굴의 관자놀이 점검판이 작게 열려 그 안에 배선이 보이고 주변 얼굴은 피부 같은 표면을 유지한다.

A humanlike artificial face has a small open temple panel; wiring is visible inside the panel while the surrounding face retains a skinlike surface.

- 관계: temple_panel → part_of → face; wiring → inside → temple_panel; skin_surface → surrounds → temple_panel
- 혼동 경계: 얼굴에 붙인 전자 장신구, 인공피부라는 실제 화학 성분
- 관찰 한계: 인간 외관과 국소 기계 단서의 창작안이다. 의식·인격·인간 기원을 입증하지 않는다.
- 검토 슬롯: subject, body_form, object_structure
- 출처 범위: [S19](https://spectrum.ieee.org/the-uncanny-valley), [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A04 국소 의체 접속부

성인의 보이는 위팔이 맞춤형 접속 링에서 기계 아래팔과 만나고 기계 손은 그 아래팔에 이어져 있다.

An adult's visible upper arm meets a mechanical forearm at a fitted interface ring; the mechanical hand is continuous with that forearm.

- 관계: adult_upper_arm → meets → interface_ring; mechanical_forearm → meets → interface_ring; mechanical_hand → part_of → mechanical_forearm
- 혼동 경계: 외부 장갑, 손에 든 로봇팔
- 관찰 한계: 경계 형태만 다룬다. 신경 연결의 작동·수술 이력·강제 개조를 입증하지 않는다.
- 검토 슬롯: anatomical_connection, body_form
- 출처 범위: [S04](https://www.cyberdyne.jp/en/products/about-hal), [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A05 착용 외골격의 외부 지지 경로

성인이 허리 벨트·허벅지 커프·정강이 지지대로 고정된 열린 외부 프레임을 착용하고 프레임 경첩은 착용자의 무릎 옆에 놓인다.

An adult wears an open external frame with a waist belt, thigh cuffs and shin braces; frame hinges sit beside the wearer's knees.

- 관계: frame → outside → adult; waist_belt → secures → frame; thigh_cuffs → secures → frame; shin_braces → secures → frame; knee_hinges → beside → adult
- 혼동 경계: 탑승형 콕핏, 전신 의체
- 관찰 한계: 착용형 지지 구조만으로 실제 출력·재활 효과·생체 개조를 판정하지 않는다.
- 검토 슬롯: object_structure, garment_detail, contact_point
- 출처 범위: [S04](https://www.cyberdyne.jp/en/products/about-hal)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A06 방호 외장과 유연한 기층

성인 착용자의 흉부·위팔·허벅지에 단단한 판이 둘러지고 팔꿈치와 무릎 판 사이로 어두운 유연한 언더슈트가 보인다.

Rigid chest, upper-arm and thigh plates surround an adult wearer, with a flexible dark undersuit visible between the elbow and knee plates.

- 관계: rigid_plates → worn_by → wearer; undersuit → beneath → rigid_plates; undersuit → visible_in → elbow_gap; undersuit → visible_in → knee_gap
- 혼동 경계: 일반 코스튬의 동력 보증, 외골격의 생물화
- 관찰 한계: 겹침·피복 범위만 보인다. 방탄·동력 보조·압력 성능은 별도다.
- 검토 슬롯: garment_detail, surface_material, object_structure
- 출처 범위: [S01](https://modernrobotics.northwestern.edu/nu-gm-book-resource/2-2-degrees-of-freedom-of-a-robot/), [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A07 무인기 외형과 관제 화면

소형 바퀴 기계에 카메라 마스트가 달리고 별도 조작대의 경계가 있는 모니터에는 그 기계가 표시된다.

A compact wheeled machine carries a camera mast; a separate control desk displays a view of that same machine within a bounded monitor.

- 관계: mast → mounted_on → machine; monitor → mounted_on → desk; depicted_machine → represented_in → monitor
- 혼동 경계: 실물 두 대, 자율성과 원격조종의 확정
- 관찰 한계: 화면과 실물의 대응만 표현한다. 제어 방식·통신 연결은 확정하지 않는다.
- 검토 슬롯: subject, prop, object_structure
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A08 교체식 작업 말단

고정 로봇팔 끝의 볼트 플랜지에 두 턱 집게가 달리고 별도 드릴 부착구가 옆 선반에 놓여 있다.

A fixed robot arm ends in a bolted tool flange holding a two-jaw gripper; a separate drill attachment rests on a nearby rack.

- 관계: flange → terminates → arm; gripper → bolted_to → flange; drill → rests_on → rack
- 혼동 경계: 집게와 드릴을 한 말단에 융합, 이미 완료된 교체
- 관찰 한계: 부착된 도구와 교체 대기 도구의 소유를 구별한다. 작업 성능은 별도다.
- 검토 슬롯: object_structure, prop
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/), [S05](https://bostondynamics.com/blog/electric-new-era-for-atlas)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A09 의인화 장비의 소유자

성인 캐릭터가 보이는 천 슈트 위에 기계 어깨 팩과 종아리 장갑을 착용하고 장비는 몸 바깥에 남아 있다.

An adult character wears a mechanical shoulder pack and calf armor over a visible fabric suit; the pack and armor remain external to the body.

- 관계: suit → worn_by → adult; shoulder_pack → outside → adult; calf_armor → outside → adult
- 혼동 경계: 안드로이드·사이보그라는 기원 추정, 성별과 연령 추정
- 관찰 한계: 장착 장비의 의인화 디자인 제안이다. 신체 기원·생물학적 성별·성적 의미는 별도다.
- 검토 슬롯: garment_detail, prop
- 출처 범위: [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A10 구난 플랫폼과 견인 경로

작업 기계가 잔해 틈 옆에 평평한 구조 플랫폼을 낮춰 두고 케이블이 플랫폼 인양 고리에서 기계의 드럼까지 이어진다.

A utility machine lowers a flat rescue platform beside a rubble gap; a cable runs from the platform's lifting eye to a drum on the machine.

- 관계: platform → beside → rubble_gap; lifting_eye → part_of → platform; cable → joins → lifting_eye; cable → joins → drum; drum → part_of → machine
- 혼동 경계: 공격 무장, 이미 구조 성공
- 관찰 한계: 기구와 접속 경로의 제안이다. 구조 성공·사람의 생존·안전 인증은 별도다.
- 검토 슬롯: object_structure, prop
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## A11 문양의 금속 매체

기계에 투구형 머리 외장과 겹친 어깨판이 있고 흉부 장갑의 경계가 있는 홈에는 새긴 기하학 문양이 들어 있다.

A machine wears a helmetlike head shell and overlapping shoulder plates; engraved geometric signs occupy bounded recesses in its chest armor.

- 관계: head_shell → part_of → machine; shoulder_plates → part_of → machine; chest_armor → part_of → machine; recesses → part_of → chest_armor; signs → inside → recesses
- 혼동 경계: 실제 마력·영혼·종교 소속, 문양을 몸 밖에 띄움
- 관찰 한계: 기사형 의장과 물리 문양의 창작안이다. 마력·신앙·고대 기원을 입증하지 않는다.
- 검토 슬롯: object_structure, surface_pattern
- 출처 범위: [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B01 노출 프레임과 탈거 외장

열린 몸통 외장 안에 구조 레일과 어깨 회전축이 드러나고 탈거한 외장판은 그 몸통 옆 받침대에 놓인다.

An open torso casing exposes structural rails and shoulder pivots; a removed outer plate rests on a stand beside that torso.

- 관계: rails → inside → torso; pivots → attached_to → rails; outer_plate → rests_on → stand; stand → beside → torso
- 혼동 경계: 프레임과 외장의 동일시, 자동 파손 판정
- 관찰 한계: 탈거 상태만으로 전투 손상·미완성·정비 원인을 확정하지 않는다.
- 검토 슬롯: object_structure, prop_state
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/), [S23](https://en.gundam-official.com/feature/pgu-rx93/images/system_img_chest_250603.png)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B02 회전 관절과 링크

단단한 팔 마디 두 개가 원통형 팔꿈치 회전축에서 만나고 그 축은 두 마디의 연결 귀를 관통한다.

Two rigid arm segments meet at a cylindrical elbow pivot; the pivot axis crosses both segment lugs.

- 관계: pivot → joins → upper_link; pivot → joins → lower_link; pivot → passes_through → lugs
- 혼동 경계: 장식 원판, 전체 자유도 수
- 관찰 한계: 특정 회전 연결의 배치이며 전체 DOF·가동 한계·강도는 측정되지 않는다.
- 검토 슬롯: object_structure
- 출처 범위: [S01](https://modernrobotics.northwestern.edu/nu-gm-book-resource/2-2-degrees-of-freedom-of-a-robot/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B03 유압 실린더의 양끝

실린더 몸통은 위팔 링크에 핀으로 고정되고 뻗은 로드는 열린 팔꿈치를 가로질러 아래팔 링크에 핀으로 연결된다.

A cylinder barrel is pinned to the upper arm link and its extended rod is pinned to the forearm link across an open elbow joint.

- 관계: barrel → pinned_to → upper_link; rod → emerges_from → barrel; rod → pinned_to → lower_link; rod → crosses → elbow
- 혼동 경계: 양끝 없는 피스톤 장식, 호스가 곧 동력원
- 관찰 한계: 양끝·축선·관절 간섭을 함께 검토한다. 유압 압력·출력·실제 가동은 별도다.
- 검토 슬롯: object_structure, contact_point
- 출처 범위: [S01](https://modernrobotics.northwestern.edu/nu-gm-book-resource/2-2-degrees-of-freedom-of-a-robot/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B04 직동 레일과 캐리지

기계 팔 내부의 직사각 캐리지가 평행 가이드 레일 두 개를 걸치고 곧은 액추에이터 로드가 그 중앙에 연결된다.

A rectangular carriage straddles two parallel guide rails inside a machine arm; a straight actuator rod joins the carriage at its center.

- 관계: carriage → straddles → rails; rod → joins → carriage; rails → inside → arm
- 혼동 경계: 회전 관절, 실제 이동 속도
- 관찰 한계: 직선 이동을 허용하는 외형의 제안이며 이동 이력·구동 속도는 보이지 않는다.
- 검토 슬롯: object_structure
- 출처 범위: [S01](https://modernrobotics.northwestern.edu/nu-gm-book-resource/2-2-degrees-of-freedom-of-a-robot/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B05 감속기와 모터의 분리

작은 모터 하우징이 열린 감속기 상자 옆에 있고 축 하나가 모터 하우징과 감속기 입력을 잇는다.

A compact motor housing sits beside an open reduction gearbox; a shaft links the motor housing to the gearbox input.

- 관계: shaft → joins → motor; shaft → joins → input; input → part_of → gearbox
- 혼동 경계: 모터·감속기·서보의 동의어 처리
- 관찰 한계: 서보는 피드백 제어 개념이며 하우징만으로 제어 오차·기어비를 알 수 없다.
- 검토 슬롯: object_structure
- 출처 범위: [S01](https://modernrobotics.northwestern.edu/nu-gm-book-resource/2-2-degrees-of-freedom-of-a-robot/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B06 하드포인트와 분리된 팩

등 장착 장비 팩이 기계 등판의 비어 있는 키형 장착 레일 맞은편 트롤리에 놓인다.

A back-mounted equipment pack sits on a trolley opposite a bare keyed mounting rail on a machine's back.

- 관계: mount → part_of → machine; pack → rests_on → trolley; pack → aligned_with → mount
- 혼동 경계: 이미 결합된 팩, 변형·합체
- 관찰 한계: 분리된 상태와 맞물림 위치만 보인다. 호환성과 교체 절차는 별도다.
- 검토 슬롯: object_structure, prop_state
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/), [S16](https://news.xbox.com/en-us/2023/08/24/five-things-you-should-know-armored-core-6-fires-of-rubicon/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B07 변형 후 남은 차체 부품

인간형 기계의 등에 자동차 지붕이 접혀 있고 양어깨 옆에는 바퀴가 하나씩 고정되어 있다.

A humanoid machine has a car roof folded against its back and a visible wheel fixed beside each shoulder.

- 관계: car_roof → folded_against → back; back → part_of → machine; wheels → beside → shoulders
- 혼동 경계: 장식 바퀴, 변형 경로·질량 보존의 입증
- 관찰 한계: 변형 후 흔적을 보이는 창작안이다. 동일 차체에서 실제 변형했다는 시간 증거는 아니다.
- 검토 슬롯: object_structure, body_form
- 출처 범위: [S13](https://macross.jp/pages/series?title=macrosszero)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B08 합체 결합부의 서로 다른 유닛

색이 다른 기계 모듈 두 개가 큰 결합 칼라에서 만나고 각 모듈은 칼라 양쪽에서 자기 외장을 유지한다.

Two differently colored machine modules meet at a large coupling collar; each module retains its own outer shell on its side of the collar.

- 관계: module_a → joins → collar; module_b → joins → collar; module_a → distinct_from → module_b
- 혼동 경계: 한 기체의 변형, 장비 환장
- 관찰 한계: 결합된 구조를 제안한다. 원래 독립 기체·합체 순서·작동 가능성은 별도다.
- 검토 슬롯: object_structure
- 출처 범위: [S13](https://macross.jp/pages/series?title=macrosszero), [S16](https://news.xbox.com/en-us/2023/08/24/five-things-you-should-know-armored-core-6-fires-of-rubicon/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B09 추가 장갑의 이중 경계

추가 어깨 장갑판이 보이는 이격 브래킷 위에서 원래 어깨 외장 위에 놓이고 두 층 사이에는 좁은 틈이 남는다.

An extra shoulder plate sits above the original shoulder shell on visible standoff brackets, leaving a narrow gap between both layers.

- 관계: extra_plate → above → original_shell; brackets → joins → extra_plate; brackets → joins → original_shell; gap → between → brackets
- 혼동 경계: 도장 경계, 원래 외장 자체
- 관찰 한계: 추가 층과 고정점만 관찰한다. 복합재 구성·방호력은 별도다.
- 검토 슬롯: object_structure
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## B10 퍼지의 분리 상태

떨어진 장갑판이 기계의 드러난 고정 훅 옆에 떠 있고 판과 본체 사이에는 분명한 틈이 있다.

A detached armor panel floats beside a machine's exposed mounting hooks, with a clear gap separating the panel from the body.

- 관계: hooks → part_of → body; panel → separated_from → body; gap → separates → panel
- 혼동 경계: 추가 팔다리, 장갑에 그린 선
- 관찰 한계: 분리 상태와 공중 배치만 보인다. 자발적 퍼지·폭발·탈거 원인은 별도다.
- 검토 슬롯: prop_state, object_structure
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## C01 흉부 해치와 조종석의 경계

성인이 흉부 해치에서 반쯤 나와 한 손으로 위 손잡이를 잡고 한쪽 부츠를 아래 발판에 올리며 개구부 뒤에는 좌석이 남아 있다.

An adult stands half outside a chest hatch, gripping its upper handhold with one hand and placing one boot on a lower step; a seat remains behind the opening.

- 관계: hand → part_of → adult; hand → grips → handhold; boot → contacts → step; handhold → part_of → hatch; seat → behind → hatch
- 혼동 경계: 허공의 손·발, 사람 크기보다 작은 해치
- 관찰 한계: 지지 접점과 해치 위치를 함께 검토한다. 실제 출입 순서·안전성은 별도다.
- 검토 슬롯: body_pose, contact_point, object_structure
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/), [S23](https://en.gundam-official.com/feature/pgu-rx93/images/system_img_chest_250603.png)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## C02 좌석·하네스·몸의 고정

성인이 조종석 등받이에 기대고 어깨끈 두 개와 허리띠가 허리 버클 하나에 모이며 끈 끝은 좌석 프레임에 붙어 있다.

An adult reclines against a cockpit seat; two shoulder straps and a lap belt meet at one waist buckle, with strap ends attached to the seat frame.

- 관계: adult → supported_by → seat; straps → joins → buckle; lap_belt → joins → buckle; straps → anchored_to → seat_frame
- 혼동 경계: 장식 띠, 강제 구속이라는 의미
- 관찰 한계: 몸·버클·앵커를 모두 관찰한다. 동의·억압·충돌 보호 성능은 추정하지 않는다.
- 검토 슬롯: body_pose, garment_detail, contact_point
- 출처 범위: [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## C03 손·조종간과 발·페달

착좌한 성인이 좌우의 별도 조종간을 각각 잡고 각 부츠 밑창은 좌석 아래의 별도 페달에 닿아 있다.

A seated adult grips separate left and right control sticks; each boot sole rests on a separate pedal below the seat.

- 관계: left_hand → grips → left_stick; right_hand → grips → right_stick; left_boot → rests_on → left_pedal; right_boot → rests_on → right_pedal
- 혼동 경계: 손끼리 융합, 같은 페달에 양발, 손 발 생략
- 관찰 한계: 모든 접점을 한 시점에 보이는 구도를 먼저 설계한다. 조작 명령의 유효성은 별도다.
- 검토 슬롯: body_pose, contact_point, prop
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/), [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## C04 복좌 탠덤과 측면 병렬의 구별

사람이 앉은 조종석 두 개가 같은 전후 중심선에 놓이고 뒤 좌석은 별도 머리받침이 보일 만큼 높다.

Two occupied cockpit seats lie on the same fore-aft centerline; the rear seat is raised enough to reveal its separate headrest.

- 관계: front_adult → sits_on → front_seat; rear_adult → sits_on → rear_seat; rear_seat → behind → front_seat; headrest → part_of → rear_seat
- 혼동 경계: 나란한 복좌, 한 사람의 반사
- 관찰 한계: 탠덤 배치의 창작 제안이며 두 사람의 신경 공유·역할 분담을 입증하지 않는다.
- 검토 슬롯: object_structure, body_pose
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## C05 파노라마 표시의 매체 경계

조종석 좌석을 연속된 도시 영상을 표시하는 이어진 디스플레이 패널 세 개가 둘러싸며 표현된 스카이라인 주변에는 얇은 패널 경계가 보인다.

A cockpit seat is surrounded by three joined display panels showing a continuous city view; thin panel borders remain visible around the depicted skyline.

- 관계: display_panels → surrounds → seat; depicted_city → represented_in → display_panels; borders → bounds → display_panels
- 혼동 경계: 실제 창밖 도시, 실제 전방위 시야
- 관찰 한계: 화면 배치와 표시만 다룬다. 360도 커버리지·실시간 영상 여부는 별도다.
- 검토 슬롯: object_structure, composition
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## C06 별도 조작소의 대응 화면

성인이 손 조종기가 있는 조작소에 서 있고 테두리가 있는 화면에는 밸브를 잡은 원격 로봇이 표시된다.

An adult stands at a control station with a hand controller; a bordered screen shows a remote robot gripping a valve.

- 관계: adult → holds → controller; depicted_robot → represented_in → screen; depicted_valve → represented_in → screen; depicted_robot → grips → depicted_valve
- 혼동 경계: 실물 밸브를 화면 밖에 추가, 직접 신경 지배
- 관찰 한계: 공유·감독·완전 수동 제어의 비율과 통신 지연은 화면만으로 알 수 없다.
- 검토 슬롯: action, prop, composition
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## C07 접속 포트의 양끝 연결

케이블 하나가 성인의 목 칼라 소켓에서 좌석 뒤 커넥터까지 연속해 이어지고 어깨 옆에는 여유 길이가 남는다.

A cable runs continuously from a socket on an adult's neck collar to a connector on the rear of a seat, leaving slack beside the shoulder.

- 관계: collar → worn_by → adult; socket → part_of → collar; cable → joins → socket; cable → joins → seat_connector; seat_connector → part_of → seat
- 혼동 경계: 목걸이 장식, 통증·동기화의 확정
- 관찰 한계: 외부 케이블의 양끝만 입증한다. 뇌 침습·신호 전달·기억 공유·동의는 별도다.
- 검토 슬롯: contact_point, object_structure, garment_detail
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/), [S04](https://www.cyberdyne.jp/en/products/about-hal)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## C08 동작 추종의 병치

성인이 열린 추적 프레임 안에서 한 팔을 들고 프레임 너머의 별도 로봇도 대응하는 팔을 비슷한 자세로 둔다.

An adult stands in an open tracking frame with one arm raised; a separate robot beyond the frame holds its corresponding arm in a similar pose.

- 관계: adult → inside → tracking_frame; adult_arm → part_of → adult; robot_arm → part_of → robot; adult_arm → visually_matches → robot_arm
- 혼동 경계: 한 몸의 추가 팔, 시간 동기화의 증명
- 관찰 한계: 한 정지 시점의 자세 대응이며 실시간 추종·인과 제어를 입증하지 않는다.
- 검토 슬롯: body_pose, composition
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## C09 탈출 블록의 분리 경계

작은 좌석 캡슐이 열린 조종석 베이 위로 분리되어 있고 캡슐의 가이드 레일은 베이 안의 레일과 정렬된다.

A compact seat capsule is separated above an open cockpit bay; guide rails on the capsule align with rails inside the bay.

- 관계: seat → inside → capsule; capsule → separated_from → bay; capsule_rails → aligned_with → bay_rails
- 혼동 경계: 열린 해치가 곧 사출, 조종자 사망
- 관찰 한계: 분리 위치를 보일 뿐 실제 사출·생존·가속·탈출 순서를 확인하지 않는다.
- 검토 슬롯: object_structure, prop_state
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## D01 엄빌리컬의 설비·기체 양끝

굵은 케이블이 벽 서비스 소켓에서 기계 허리 뒤 접속구까지 바닥 케이블 가이드를 거쳐 연속해 이어진다.

A thick cable forms a continuous route from a wall service socket to a machine's lower-back receptacle, passing through a floor cable guide.

- 관계: cable → joins → wall_socket; cable → passes_through → guide; cable → joins → receptacle; receptacle → part_of → machine
- 혼동 경계: 끝 없는 전선, 전력·신호·유체의 자동 동일시
- 관찰 한계: 경로와 양끝만 확인한다. 전압·유량·기능은 독립 설정이다.
- 검토 슬롯: object_structure, contact_point
- 출처 범위: [S07](https://www.nasa.gov/reference/european-service-module/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## D02 분리형 배터리의 접속면

직사각 배터리형 팩이 열린 장비 베이 옆에 있고 팩의 노출 접점은 베이 내부의 대응 접점을 향한다.

A rectangular battery-like pack sits beside an open equipment bay; exposed contacts on the pack face corresponding contacts inside the bay.

- 관계: pack_contacts → part_of → pack; bay_contacts → inside → bay; pack_contacts → faces → bay_contacts
- 혼동 경계: 반응로·발전기, 잔량의 추정
- 관찰 한계: 배터리형 교체 구조의 제안이다. 실제 화학·충전 상태·발전 기능은 보이지 않는다.
- 검토 슬롯: object_structure, prop_state
- 출처 범위: [S07](https://www.nasa.gov/reference/european-service-module/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## D03 동력부와 발광 코어의 구별

둥근 발광 하우징이 기계 몸통에 볼트로 고정되어 있고 주위에는 별도의 굵은 케이블과 리브형 냉각관이 놓인다.

A round illuminated housing is bolted into a machine's torso between separate thick cables and ribbed cooling lines.

- 관계: housing → bolted_to → torso; cables → adjacent_to → housing; cooling_lines → adjacent_to → housing
- 혼동 경계: 빛이 곧 핵융합로·에너지원, 과학적 작동 원리
- 관찰 한계: 발광 중심부라는 외형만 채택한다. 반응로·축전기·AI 코어는 요청 정의가 있어야 한다.
- 검토 슬롯: object_structure, lighting
- 출처 범위: [S07](https://www.nasa.gov/reference/european-service-module/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## D04 냉각 배관의 국소 누출

젖은 자국이 기계 종아리의 갈라진 호스 이음부에서 시작해 외장을 따라 아래의 작은 웅덩이까지 이어진다.

A wet trail begins at a cracked hose coupling on a machine's calf and runs down the casing to a small puddle below.

- 관계: coupling → part_of → hose; trail → starts_at → coupling; trail → runs_down → casing; trail → ends_at → puddle
- 혼동 경계: 배경 빗물, 인간 혈액, 유체 종류의 단정
- 관찰 한계: 국소 기점과 경로만 보인다. 냉각수·유압유·혈액의 성분·고장 원인은 별도다.
- 검토 슬롯: prop_state, object_structure
- 출처 범위: [S08](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## D05 라디에이터와 뿌리 배관

얇고 밝은 패널 두 개가 기계 등에서 경첩으로 펼쳐지고 보이는 배관이 몸통에서 각 패널 뿌리로 이어진다.

Two thin pale panels extend from a machine's back on hinges; visible tubing runs from the torso to the root of each panel.

- 관계: panels → hinged_to → torso; tubing → joins → torso; tubing → joins → panels
- 혼동 경계: 태양전지·방패·장식 날개, 방열량 추정
- 관찰 한계: 열 제어를 연상하는 창작안이다. 기능·온도·방사율은 외형으로 확인되지 않는다.
- 검토 슬롯: object_structure
- 출처 범위: [S08](https://www.nasa.gov/smallsat-institute/sst-soa/thermal-control/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## D06 주 추진기와 보조 노즐

큰 뒤쪽 노즐 주위에 옆을 향한 작은 노즐 네 개가 같은 백팩 하우징에 붙어 있다.

A large rear nozzle is surrounded by four smaller side-facing nozzles attached to the same backpack housing.

- 관계: main_nozzle → part_of → backpack; small_nozzles → part_of → backpack; small_nozzles → surrounds → main_nozzle
- 혼동 경계: 모든 작은 구멍을 버니어로 판정, 개구부와 추진기 혼동
- 관찰 한계: 노즐 크기·방향만 표현한다. 추력·추진제·제어권은 별도다.
- 검토 슬롯: object_structure
- 출처 범위: [S07](https://www.nasa.gov/reference/european-service-module/), [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## D07 추력 편향의 관절 지지

노즐 벨이 기계 백팩 아래 짐벌 링에 놓이고 링에 대해 기울어 있으며 밝은 분출은 노즐 축 방향을 따른다.

A nozzle bell sits in a gimbal ring below a machine's backpack, tilted relative to the ring while a bright plume follows the bell axis.

- 관계: gimbal → attached_to → backpack; nozzle → inside → gimbal; plume → aligned_with → nozzle
- 혼동 경계: 장식 불꽃, 정지 그림으로 가속 증명
- 관찰 한계: 축 정렬과 지지 연결의 제안이다. 추력 크기·호버 안정성·대기 유무는 별도다.
- 검토 슬롯: object_structure, prop_state
- 출처 범위: [S07](https://www.nasa.gov/reference/european-service-module/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E01 실탄 무장의 급탄 경로

다총열 포가 아래팔 거치대에 붙고 탄띠가 별도 탄약 드럼에서 포 뒤쪽까지 연속해 이어진다.

A multi-barrel gun is attached to a forearm mount; an ammunition belt runs continuously from a separate drum to the rear of the gun.

- 관계: barrels → part_of → gun; gun → attached_to → mount; mount → part_of → forearm; belt → joins → drum; belt → joins → gun
- 혼동 경계: 발광선만 있는 빔, 포와 드럼을 연결하지 않은 띠
- 관찰 한계: 외부 구조만 제안한다. 작동 가능한 제작 치수·발사 순서·성능은 제공하지 않는다.
- 검토 슬롯: object_structure, prop
- 출처 범위: [S10](https://www.onr.navy.mil/media-center/news-releases/bang-navy-begins-tests-electromagnetic-railgun-prototype-launcher), [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E02 미사일 포드의 셀과 해치

열린 어깨 포드 안에 움푹 들어간 미사일 앞부분이 두 줄로 보이고 열린 해치는 포드 위쪽 가장자리에 경첩으로 붙어 있다.

An open shoulder pod reveals two rows of recessed missile noses, with its raised hatch hinged along the pod's top edge.

- 관계: pod → mounted_on → shoulder; missile_noses → inside → pod; hatch → attached_to → hinge; hinge → part_of → pod
- 혼동 경계: 노출 탄두를 센서로 오인, 발사 완료
- 관찰 한계: 개구·배열·소유만 보인다. 유도 방식·발사 이력·폭발 성능은 별도다.
- 검토 슬롯: object_structure, prop_state
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/), [S16](https://news.xbox.com/en-us/2023/08/24/five-things-you-should-know-armored-core-6-fires-of-rubicon/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E03 로켓 펀치의 분리 전완

기계 주먹과 아래팔이 위팔 앞쪽에 분리되어 있고 떨어진 아래팔 뒤쪽에서 밝은 배기가 나온다.

A mechanical fist and forearm are separated in front of the upper arm; a bright exhaust plume exits the detached forearm's rear.

- 관계: fist → attached_to → forearm; forearm → separated_from → upper_arm; plume → exits → forearm
- 혼동 경계: 팔 추가 생성, 일반 절단과 고어의 혼동
- 관찰 한계: 분리형 무장의 창작 제안이며 회수·재결합·실제 궤적은 별도다.
- 검토 슬롯: action, object_structure
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E04 파일 벙커의 단일 축선

굵은 말뚝이 기계 손목에 고정된 짧은 직동 하우징에서 뻗고 말뚝과 하우징은 한 축을 공유한다.

A thick spike projects from a short linear housing fixed to a machine's wrist, with the spike and housing sharing one axis.

- 관계: spike → emerges_from → housing; housing → fixed_to → wrist; spike → aligned_with → housing
- 혼동 경계: 드릴·회전 칼날, 창과 집게
- 관찰 한계: 밀어내는 구조의 외형 제안이다. 실제 충격·관통·작동 원리는 입증하지 않는다.
- 검토 슬롯: object_structure, prop
- 출처 범위: [S16](https://news.xbox.com/en-us/2023/08/24/five-things-you-should-know-armored-core-6-fires-of-rubicon/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E05 히트 블레이드와 발광 날

단단한 금속 칼날의 등은 어둡고 절삭 날은 주황색으로 빛나며 손잡이와 날 사이에는 금속 몸체가 계속 보인다.

A solid metal blade has a dark spine and an orange glowing cutting edge; the metal body remains visible between edge and hilt.

- 관계: spine → part_of → blade; edge → part_of → blade; blade → joins → hilt
- 혼동 경계: 빛만으로 만든 날, 실제 온도·고주파 진동
- 관찰 한계: 고체와 발광 영역을 구별한다. 가열·진동·에너지장의 물리 성능은 별도다.
- 검토 슬롯: prop, surface_material, lighting
- 출처 범위: [S09](https://www.nist.gov/history/nists-role-laser-measurements-and-applications/what-laser)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E06 원격 무장의 본체·분리체

작은 지느러미형 유닛 세 개가 큰 기계 주위에 공간적으로 분리되고 각 유닛은 별도 외장과 본체와의 틈을 가진다.

Three small finlike units are spatially separated around a larger machine; each small unit has its own casing and a visible gap from the main body.

- 관계: unit_a → separated_from → main_body; unit_b → separated_from → main_body; unit_c → separated_from → main_body
- 혼동 경계: 바인더·등 장갑, 정신 제어의 자동 부여
- 관찰 한계: 분리체 수·간격만 보인다. 사이코뮤·자율성·공격·공중 부양 원리는 별도다.
- 검토 슬롯: object_structure, composition
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/), [S12](https://en.gundam-official.com/witch-from-mercury/words/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E07 물리 방패와 손·거치대

넓은 방패가 뒤쪽 브래킷 두 개로 기계 왼쪽 아래팔에 붙어 보이는 위협 방향에서 몸통을 가린다.

A broad shield is attached to a machine's left forearm by two rear brackets, covering the torso from a visible incoming direction.

- 관계: brackets → joins → shield; brackets → joins → left_forearm; shield → faces → threat; shield → in_front_of → torso
- 혼동 경계: 에너지 장벽, 손에서 떠 있는 방패
- 관찰 한계: 차폐 방향과 고정 구조를 제안한다. 실제 방호력·승패는 별도다.
- 검토 슬롯: body_pose, contact_point, prop
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E08 가시 장벽과 물리 기체의 경계

반투명 곡면이 기계 앞을 둘러 휘고 표면에는 밝은 접촉 섬광이 있으며 금속 장갑과 곡면 사이에는 보이는 틈이 있다.

A translucent curved surface arcs in front of a machine, with a bright contact flare on the surface and a visible gap between it and the metal armor.

- 관계: barrier → in_front_of → machine; flare → on → barrier; barrier → separated_from → armor
- 혼동 경계: 코팅 자체의 발광, 과학적 에너지 방패 보증
- 관찰 한계: 허구적 장벽 표현이다. 재료·물리 법칙·실제 요격 성공은 주장하지 않는다.
- 검토 슬롯: prop_state, lighting
- 출처 범위: [S09](https://www.nist.gov/history/nists-role-laser-measurements-and-applications/what-laser)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E09 장갑 단면과 부착 블록

절개된 장갑 표본에 구별되는 접합층 세 개가 보이고 옆의 온전한 판에는 별도 직사각 외부 블록 배열이 붙어 있다.

A cutaway armor sample displays three distinct bonded layers; a separate array of rectangular exterior blocks is mounted on the adjacent intact panel.

- 관계: layers → part_of → sample; blocks → mounted_on → intact_panel; sample → beside → intact_panel
- 혼동 경계: 겹장갑이 곧 특정 복합재, 블록이 곧 반응장갑
- 관찰 한계: 단면과 표면 부착 방식을 비교한다. 재료 성분·폭발성·방호 원리는 확정하지 않는다.
- 검토 슬롯: object_structure, composition
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## E10 센서·안테나와 표시의 분리

기계의 마스트에 접시형 안테나 두 개와 별도 렌즈 군집이 달리고 옆의 경계가 있는 화면에는 아이콘을 둘러싼 표적 괄호가 표시된다.

A machine carries a mast with two dishlike antennas and a separate lens cluster; a nearby bounded display shows target brackets around an icon.

- 관계: mast → part_of → machine; antennas → mounted_on → mast; lenses → mounted_on → mast; icon → represented_in → display; brackets → surrounds → icon
- 혼동 경계: 안테나가 곧 교란 성공, 화면 아이콘이 곧 실제 적군
- 관찰 한계: 센서 외형·표시만 보인다. 탐지·피아 판정·통신 차단은 별도다.
- 검토 슬롯: object_structure, prop
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F01 역관절 실루엣의 마디 구분

기계 다리는 앞쪽 위 마디, 뚜렷이 뒤로 나온 중간 관절, 넓은 발로 끝나는 긴 아래 마디로 나뉜다.

A machine leg has a forward upper segment, a sharply rearward middle joint and an elongated lower segment ending in a broad foot.

- 관계: middle_joint → joins → upper_segment; middle_joint → joins → lower_segment; foot → attached_to → lower_segment
- 혼동 경계: 새 발목을 뒤집힌 인간 무릎으로 단정, 한 장의 실제 보행
- 관찰 한계: 가상 기체의 마디 배치다. 동물 해부학과 동일시하지 않는다.
- 검토 슬롯: body_form, object_structure
- 출처 범위: [S16](https://news.xbox.com/en-us/2023/08/24/five-things-you-should-know-armored-core-6-fires-of-rubicon/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F02 사족과 궤도의 독립 대안

낮은 기계 몸통이 서로 다른 관절 다리 네 개 위에 놓이고 각 다리는 몸통 주위의 별도 지면 접점으로 끝난다.

A low machine torso stands on four separate articulated legs, each ending at a distinct ground contact around the torso.

- 관계: legs → attached_to → torso; feet → part_of → legs; feet → contacts → ground
- 혼동 경계: 한 쌍 다리를 사족으로 세기, 같은 후보에 궤도까지 강제 결합
- 관찰 한계: 정확히 네 다리의 배치만 제안한다. 정적 접지로 동적 안정성을 보증하지 않는다.
- 검토 슬롯: body_form, body_pose
- 출처 범위: [S16](https://news.xbox.com/en-us/2023/08/24/five-things-you-should-know-armored-core-6-fires-of-rubicon/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F03 궤도 하부와 상부 기체

기계 몸통 아래에 연속 궤도 루프 두 개가 놓이고 각 루프 안에는 주행륜 여러 개가 들어 있다.

A machine torso is mounted above two continuous track loops, with several road wheels enclosed by each loop.

- 관계: torso → above → track_loops; road_wheels → inside → track_loops
- 혼동 경계: 바퀴형·족형, 궤도 위에 추가 발 생성
- 관찰 한계: 연속 궤도와 내부 바퀴 관계만 보인다. 기동성·중량·반동 흡수는 별도다.
- 검토 슬롯: body_form, object_structure
- 출처 범위: [S16](https://news.xbox.com/en-us/2023/08/24/five-things-you-should-know-armored-core-6-fires-of-rubicon/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F04 모노아이 센서 레일

둥근 발광 렌즈 하나가 어두운 머리 홈 안의 수평 트랙에 놓이고 홈은 단단한 얼굴 장갑으로 둘러싸여 있다.

One round illuminated lens sits on a horizontal track inside a dark head recess; the recess is enclosed by rigid face armor.

- 관계: lens → mounted_on → track; track → inside → recess; face_armor → surrounds → recess
- 혼동 경계: 센서 띠·두 눈, 렌즈 이동의 입증
- 관찰 한계: 센서 하나와 레일의 배치다. 시선·감정·실제 이동은 별도다.
- 검토 슬롯: object_structure, body_form
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F05 트윈아이와 띠형 센서

중앙 얼굴 능선 양쪽에 구별되는 발광 개구부 두 개가 있고 어두운 장갑이 두 개구부를 나눈다.

Two distinct luminous apertures sit on opposite sides of a central face ridge, with dark armor separating the apertures.

- 관계: left_aperture → beside → ridge; right_aperture → beside → ridge; armor → separates → left_aperture
- 혼동 경계: 끊기지 않은 바이저, 눈 수와 인격
- 관찰 한계: 두 개구부의 분리를 보인다. 인간의 눈·의식·영웅성을 자동 부여하지 않는다.
- 검토 슬롯: object_structure, body_form
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F06 머리 돌출물과 얼굴 덮개

칼날형 핀 두 개가 기계 이마의 별도 거치점에서 올라가고 단단한 페이스플레이트가 센서 개구부 아래의 하관을 덮는다.

Two blade-shaped fins rise from separate mounts on a machine's forehead; a rigid faceplate covers the lower face below the sensor apertures.

- 관계: fins → attached_to → mounts; mounts → part_of → forehead; faceplate → below → sensors
- 혼동 경계: 장식이 곧 통신 안테나, 모든 V핀이 건담
- 관찰 한계: 위치와 형태만 보인다. 기능·소속·작품 정체성은 별도다.
- 검토 슬롯: object_structure
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F07 스커트 장갑의 골반 소유

별도 장갑판 네 개가 기계 허리에서 골반 주위로 내려오고 고관절 위에는 틈이 남는다.

Four separate armor panels hang from the machine's waist around the pelvis, leaving gaps over the hip joints.

- 관계: panels → attached_to → waist; panels → surrounds → pelvis; panels → separated_from → hip_joints
- 혼동 경계: 천 치마·인간 골반, 다리 관통
- 관찰 한계: 기계 허리판의 연결이다. 의복의 성별 코드·실제 가동 범위는 별도다.
- 검토 슬롯: object_structure, body_form
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F08 등 팩과 날개형 유닛

중앙 백팩 하우징이 기계 등에 붙고 길고 칼날형인 유닛 두 개가 하우징의 별도 경첩에서 뻗는다.

A central backpack housing is attached to a machine's back; two long blade-shaped units extend from separate hinges on the housing.

- 관계: backpack → attached_to → back; hinges → part_of → backpack; blade_units → attached_to → hinges
- 혼동 경계: 날개형 판의 기능 자동 확정, 같은 판에 추진·방열·실드 모두 부여
- 관찰 한계: 형상과 부착만 제안한다. 추진·방열·무장 기능은 요청 정의가 필요하다.
- 검토 슬롯: object_structure
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F09 영웅 비례와 SD 대조

설명판에 같은 기체 디자인의 경계가 있는 그림 두 개가 있고 하나는 작은 머리의 장신, 다른 하나는 커진 머리와 압축된 몸통의 단신이다.

A display board contains two bounded drawings of one machine design: one tall with a small head, the other short with an enlarged head and compressed torso.

- 관계: drawing_a → on → board; drawing_b → on → board; tall_machine → represented_in → drawing_a; short_machine → represented_in → drawing_b
- 혼동 경계: 실물 두 대의 크기 비교, 실제 키 축소 사건
- 관찰 한계: 비례의 표현 비교다. 사진 단일 현실층에는 자동 추가하지 않는다.
- 검토 슬롯: composition, body_form
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F10 패널라인과 그리블

넓고 평평한 장갑 표면을 움푹한 이음선이 나누고 별도의 작은 정비 홈 안에는 배관·리브·체결 머리가 들어 있다.

Broad flat armor surfaces are divided by recessed seams; a separate small service recess contains pipes, ribs and fastener heads.

- 관계: seams → divides → armor; recess → part_of → armor; pipes → inside → recess; ribs → inside → recess; fasteners → inside → recess
- 혼동 경계: 무작위 잡동사니, 세부가 곧 기능 증거
- 관찰 한계: 표면 밀도·접합 표현의 창작안이다. 그리블 출처 S24의 정확한 정의 지원은 보류다.
- 검토 슬롯: object_structure, surface_pattern
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/), [S24](https://www.starwars.com/news/empire-at-40-new-vehicles)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F11 치핑의 층 경계

작은 벗겨짐이 장갑판 도장 모서리를 끊어 더 어두운 밑층을 드러내고 장갑판 구조 자체는 이어져 있다.

Small chips interrupt the painted edge of an armor plate, exposing a darker underlayer; the plate remains structurally continuous.

- 관계: paint → covers → plate; chips → interrupts → paint; underlayer → beneath → paint
- 혼동 경계: 장갑 결손·혈액, 실제 전투 이력
- 관찰 한계: 도막 손상만 보인다. 전투·노후·실제 재료 조성은 별도다.
- 검토 슬롯: surface_material, prop_state
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F12 열흔과 배기 방향

금속 배기 칼라 끝 근처에 색띠가 있고 어두운 자국이 출구 뒤쪽으로 옆 외장을 따라 이어진다.

A metal exhaust collar has colored bands near its lip and a dark streak extending behind the outlet across the adjacent casing.

- 관계: bands → near → lip; lip → part_of → collar; streak → begins_at → outlet; streak → on → casing
- 혼동 경계: 특정 온도·합금 확정, 방사능 발광
- 관찰 한계: 방향과 표면 흔적의 제안이다. 온도·시간·재료는 별도다.
- 검토 슬롯: surface_material, surface_pattern
- 출처 범위: [S07](https://www.nasa.gov/reference/european-service-module/), [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F13 비대칭 장갑의 실제 차이

기계 왼어깨에는 넓은 직사각 방패판이 있고 오른어깨에는 작은 둥근 외장이 있으며 두 어깨는 같은 몸통에 이어져 있다.

A machine's left shoulder carries a broad rectangular shield plate while its right shoulder has a smaller rounded shell; both shoulders remain attached to one torso.

- 관계: left_shoulder → attached_to → torso; right_shoulder → attached_to → torso; large_plate → on → left_shoulder; small_shell → on → right_shoulder
- 혼동 경계: 서로 다른 기체의 합성, 원근 차이만 생김
- 관찰 한계: 같은 몸체의 구조적 비대칭만 제안한다. 개조 이력·중량·특정 파일럿은 별도다.
- 검토 슬롯: object_structure, body_form
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F14 연속 바이저와 단일 렌즈

하나의 어둡고 투명한 띠가 기계 얼굴 위쪽을 좌우로 가로지르고 그 아래에는 별도 불투명 페이스플레이트가 있다.

A single dark transparent band crosses the machine's upper face from side to side, above a separate opaque lower faceplate.

- 관계: band → across → upper_face; band → above → lower_faceplate; band → distinct_from → lower_faceplate
- 혼동 경계: 사람 헬멧의 바이저, 트윈아이 구멍
- 관찰 한계: 얼굴 영역의 연속 띠 외형이다. 내부 센서 수·통신·인격은 별도다.
- 검토 슬롯: object_structure, body_form
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## F15 세라믹 같은 표면과 균열

밝은 장갑판이 매끄러운 저광택 표면과 가늘게 갈라지는 균열 하나를 보이고 가장자리에는 더 어두운 구조층이 드러난다.

A pale armor plate has a smooth low-gloss surface and one fine branching crack; a darker structural layer remains visible at its edge.

- 관계: surface → part_of → plate; crack → on → surface; structural_layer → beneath → surface
- 혼동 경계: 실제 세라믹 성분·내열성 확정, 피부 균열
- 관찰 한계: 질감·색·균열의 외관만 제안한다. 실제 화학 성분·제조법·방호 성능은 별도다.
- 검토 슬롯: surface_material, prop_state
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G01 작업형 조종복의 구성

성인이 앞 지퍼·닫힌 허벅지 주머니·여민 소맷단이 있는 여유 있는 일체형 비행 작업복과 발목 위 부츠를 입는다.

An adult wears a loose one-piece flight coverall with a front zipper, closed thigh pockets, fitted cuffs and ankle-high boots.

- 관계: coverall → worn_by → adult; zipper → part_of → coverall; pockets → part_of → coverall; cuffs → part_of → coverall; boots → worn_by → adult
- 혼동 경계: 밀착 슈트·압력복·항G복의 자동 등치
- 관찰 한계: 복식 형태만 제안한다. 실제 비행 자격·방염·압력·항G 기능은 별도다.
- 검토 슬롯: garment_detail, wardrobe_style
- 출처 범위: [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/), [S22](https://www.luke.af.mil/News/Article-Display/Article/358586/new-g-suit-comes-to-luke/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G02 압력복 연결부와 호스

성인이 단단한 헬멧 링과 밀폐형처럼 보이는 손목 이음부를 가진 두툼한 복장을 입고 호스는 가슴 피팅과 별도 선실 패널을 잇는다.

An adult wears a bulky suit with a rigid helmet ring and sealed-looking wrist joints; a hose connects a chest fitting to a separate cabin panel.

- 관계: suit → worn_by → adult; helmet_ring → part_of → suit; wrist_joints → part_of → suit; hose → joins → chest_fitting; hose → joins → cabin_panel
- 혼동 경계: 몸에 붙는 천이 곧 우주복, EVA와 LEA 자동 동일시
- 관찰 한계: 형태와 외부 공급 연결만 보인다. 기밀·압력·독립 생명유지 인증은 별도다.
- 검토 슬롯: garment_detail, contact_point
- 출처 범위: [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G03 항G복의 외부 덧층

성인이 비행 작업복 위에 별도의 하체 덧바지를 입고 옆 여밈과 허리의 호스 커넥터가 보인다.

An adult wears separate lower-body overtrousers above a flight coverall, with visible side closures and a hose connector at the waist.

- 관계: coverall → worn_by → adult; overtrousers → over → coverall; closures → part_of → overtrousers; connector → part_of → overtrousers
- 혼동 경계: 압력복 전체, 중력 제거
- 관찰 한계: 개략 복식 제안이며 S22 도판 검토 전 실제 모델의 봉제·공기주머니 위치는 보류한다.
- 검토 슬롯: garment_detail
- 출처 범위: [S22](https://www.luke.af.mil/News/Article-Display/Article/358586/new-g-suit-comes-to-luke/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G04 헬멧·바이저·호흡장비의 구분

성인 헬멧에는 투명 바이저가 있고 그 아래에 입과 코를 덮는 별도 밀착 마스크가 있으며 주름 호스 하나가 마스크에서 가슴 피팅으로 이어진다.

An adult's helmet has a transparent visor above a separate fitted mouth-and-nose mask; one corrugated hose runs from the mask to a chest fitting.

- 관계: helmet → worn_by → adult; visor → part_of → helmet; mask → worn_by → adult; hose → joins → mask; hose → joins → chest_fitting
- 혼동 경계: 바이저가 곧 산소마스크, 호스 끝 생략
- 관찰 한계: 장비의 층과 양끝만 표현한다. 산소 공급·기밀·착용 안전은 별도다.
- 검토 슬롯: garment_detail, contact_point
- 출처 범위: [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G05 HMD의 눈앞 광학부

작은 표시 광학부가 헬멧에 붙은 측면 암에 지지되어 한쪽 눈앞에 놓이고 전체 바이저와는 분리되어 있다.

A small display optic is held in front of one eye by a side arm attached to the helmet; it remains separate from the full visor.

- 관계: optic → in_front_of → eye; optic → attached_to → side_arm; side_arm → attached_to → helmet; optic → distinct_from → visor
- 혼동 경계: 공중 HUD, 눈 자체를 기계로 변형
- 관찰 한계: 거치·위치만 보인다. 실제 정보 투영·시선 추적은 별도다.
- 검토 슬롯: garment_detail, object_structure
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G06 정비 커버올과 도구의 위치

헐렁한 커버올과 보호안경을 쓴 성인이 엉덩이 옆에 닫힌 공구 주머니를 달고 열린 점검판 옆에서 스패너를 든다.

An adult in a loose coverall and safety goggles carries a closed tool pouch at the hip while holding a spanner beside an open service panel.

- 관계: coverall → worn_by → adult; goggles → worn_by → adult; pouch → attached_to → coverall; adult → holds → spanner; spanner → beside → panel
- 혼동 경계: 정비 직업 확정, 공구가 손 대신 생성
- 관찰 한계: 복장·장비 소유의 제안이다. 직업·수리 성공·군 소속은 별도다.
- 검토 슬롯: garment_detail, prop, action
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G07 제복 패치와 문장 매체

성인이 어깨 탭 두 개와 봉제 가슴 패치 하나가 있는 높은 칼라 재킷을 입고 별도 기계 장갑에는 같은 기하학 문양이 있다.

An adult wears a high-collared jacket with two shoulder tabs and one stitched chest patch; a separate machine bears a matching geometric emblem on its armor.

- 관계: jacket → worn_by → adult; tabs → part_of → jacket; patch → sewn_to → jacket; emblem → on → machine
- 혼동 경계: 실제 군 계급·법적 소속 확정, 피부에 패치
- 관찰 한계: 비슷한 표식의 매체 소유만 보인다. 동일 조직·콜사인·신분은 독립 설정이다.
- 검토 슬롯: garment_detail, surface_pattern, wearable_accessory
- 출처 범위: [S12](https://en.gundam-official.com/witch-from-mercury/words/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G08 성인 밀착 인터페이스 슈트

성인이 긴 소매와 바지가 이어진 불투명 밀착 슈트를 입고 대비되는 절개 패널이 몸통을 따르며 작은 커넥터는 한쪽 어깨 바깥에 고정된다.

An adult wears an opaque fitted suit with long sleeves and legs; contrasting seam panels follow the torso and a small connector is fixed outside one shoulder.

- 관계: suit → worn_by → adult; seam_panels → part_of → suit; connector → outside → shoulder
- 혼동 경계: 나체·미성년 원작 캐릭터·압력 기능
- 관찰 한계: 성인 복식 형태만 제안한다. 소재 성능·신경 기능·성적 의도는 별도다.
- 검토 슬롯: garment_detail, wardrobe_style
- 출처 범위: [S17](https://www.evangelion.jp/news/nurie/), [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G09 컷아웃과 시어의 별도 경계

성인의 불투명 슈트에는 맨살이 보이는 경계가 있는 어깨 컷아웃 하나와 아래팔 윤곽이 비치는 별도 반투명 소매 삽입부가 있다.

An adult's opaque suit has one bounded shoulder cutout showing bare skin and a separate translucent sleeve insert through which the forearm outline is visible.

- 관계: suit → worn_by → adult; cutout → part_of → suit; skin → visible_in → cutout; sheer_insert → part_of → suit; forearm → behind → sheer_insert
- 혼동 경계: 구멍과 투명 천, 옷과 인공피부의 혼동
- 관찰 한계: 노출 위치와 피복을 명시한 성인 비노골적 디자인안이다. 기능·동의·연령을 외형으로 추정하지 않는다.
- 검토 슬롯: garment_detail, surface_material
- 출처 범위: [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G10 광택 외관과 실제 재료의 분리

성인의 불투명 밀착 슈트 곡면 패널에는 좁고 밝은 반사가 있고 옆의 단단한 흉부 장갑판에는 더 부드럽게 퍼지는 표면 반사가 있다.

An adult's opaque fitted suit carries narrow bright reflections along curved fabric panels, while the neighboring rigid chest plate has a softer diffuse finish.

- 관계: suit → worn_by → adult; reflections → on → suit; chest_plate → over → suit
- 혼동 경계: 광택이 곧 라텍스·PVC·금속 성분, 자동 페티시 분류
- 관찰 한계: 반사 외관만 비교한다. 실제 재질·성적 취향·기능은 별도다.
- 검토 슬롯: surface_material, lighting
- 출처 범위: [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G11 성인 하이컷 복식의 피복선

성인이 다리선이 높게 올라간 불투명 민소매 일체형 슈트와 별도 짧은 재킷을 입고 양옆 골반에는 복장의 테두리 마감이 보인다.

An adult wears an opaque sleeveless one-piece suit with high leg openings and a separate short jacket; the garment's bound edges remain visible at both hips.

- 관계: suit → worn_by → adult; leg_openings → part_of → suit; bound_edges → borders → leg_openings; jacket → worn_by → adult
- 혼동 경계: 피부와 의복의 경계 소실, 보호 기능 자동 부여
- 관찰 한계: 성인 비노골적 복식의 피복 범위를 제안한다. 직업·성적 의도·기능·동의는 별도다.
- 검토 슬롯: garment_detail, wardrobe_style
- 출처 범위: [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G12 의복 없는 인공 외장의 중립 관찰

성인으로 설정된 안드로이드가 의복 없이 매끈한 인공 외장을 드러낸 중립 자세로 서 있고 몸통 외장·골반 덮개·관절 링은 분명한 패널 경계로 나뉜다.

An adult-presenting android stands in a neutral pose with an unclothed smooth artificial outer shell; clear panel borders separate the torso casing, hip cover and joint rings.

- 관계: outer_shell → part_of → android; torso_casing → part_of → outer_shell; hip_cover → part_of → outer_shell; joint_rings → part_of → android; borders → separates → torso_casing
- 혼동 경계: 성적 기능·욕망·동의의 자동 판정, 인공피부와 실제 피부 혼동
- 관찰 한계: 성인 인공 외장의 비노골적 관찰안이다. 외장 노출은 성적 목적이나 실제 생물학을 증명하지 않는다.
- 검토 슬롯: body_form, surface_material
- 출처 범위: [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G13 복식 파손과 신체 손상의 분리

성인 비행 재킷의 팔꿈치 소매가 찢어져 천 가장자리가 흐트러지고 아래에는 온전한 어두운 언더슈트가 보인다.

An adult's outer flight-jacket sleeve has a torn elbow section with frayed fabric edges; an intact dark undersuit remains visible underneath.

- 관계: jacket → worn_by → adult; sleeve → part_of → jacket; tear → in → sleeve; undersuit → beneath → sleeve
- 혼동 경계: 옷 파손=신체 상해·강제 노출, 자동 전투 원인
- 관찰 한계: 파손된 의복과 온전한 기층을 구별한다. 원인·신체 상해·동의·시간은 별도다.
- 검토 슬롯: garment_detail, prop_state
- 출처 범위: [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf), [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## G14 착의의 지퍼와 손끝

불투명 언더슈트를 입은 성인이 가슴 위에서 반쯤 여민 비행 작업복 지퍼를 잡고 다른 손은 지퍼 레일 옆 천을 받친다.

An adult in an opaque undersuit holds a partly closed flight-coverall zipper at the upper chest; the other hand steadies the fabric beside the zipper track.

- 관계: undersuit → worn_by → adult; coverall → over → undersuit; hand_a → holds → zipper; hand_b → steadies → fabric; zipper → part_of → coverall
- 혼동 경계: 정지 상태로 착의·탈의 방향 확정, 피복 경계 삭제
- 관찰 한계: 손과 여밈의 현재 상태만 제안한다. 동작의 시간 방향·성적 목적·동의는 별도다.
- 검토 슬롯: action, garment_detail, contact_point
- 출처 범위: [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/), [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## H01 안정 입상과 여유 공간

이족 기계가 같은 바닥 평면에 두 발을 벌려 딛고 무릎은 조금 굽히며 아래팔은 골반 장갑에서 떨어져 있다.

A bipedal machine stands with both feet apart on one floor plane, knees slightly bent and forearms clear of the hip armor.

- 관계: left_foot → contacts → floor; right_foot → contacts → floor; forearms → separated_from → hip_armor
- 혼동 경계: 시각적 자신감이 곧 승리, 허공의 발
- 관찰 한계: 지지·관절 여유의 한 자세다. 동적 균형·성격·카토키 규격을 단정하지 않는다.
- 검토 슬롯: body_pose, contact_point
- 출처 범위: [S01](https://modernrobotics.northwestern.edu/nu-gm-book-resource/2-2-degrees-of-freedom-of-a-robot/), [S02](https://modernrobotics.northwestern.edu/chapters/chapter6/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## H02 삼점 착지의 세 접점

기계의 왼손바닥·오른발·왼무릎이 같은 지면에 닿고 다른 손은 지면에서 떨어져 있다.

A machine's left palm, right foot and left knee contact the same ground plane; its other hand remains clear of the ground.

- 관계: left_palm → contacts → ground; right_foot → contacts → ground; left_knee → contacts → ground; other_hand → separated_from → ground
- 혼동 경계: 무릎쏴·네 점 지지, 실제 착지 순간
- 관찰 한계: 세 지점의 정적 배치다. 추락·감속·충격량·시간 전후는 별도다.
- 검토 슬롯: body_pose, contact_point
- 출처 범위: [S01](https://modernrobotics.northwestern.edu/nu-gm-book-resource/2-2-degrees-of-freedom-of-a-robot/), [S02](https://modernrobotics.northwestern.edu/chapters/chapter6/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## H03 무릎쏴와 무장 지지

기계가 한쪽 무릎을 꿇고 반대 발을 딛으며 두 손은 낮은 엄폐물 위로 겨눈 긴 무기 하나를 지지한다.

A machine kneels on one knee with the opposite foot planted; both hands support one long weapon aimed above a low barrier.

- 관계: knee → contacts → ground; foot → contacts → ground; hands → supports → weapon; weapon → above → barrier
- 혼동 경계: 손상으로 주저앉음, 무장과 손의 융합
- 관찰 한계: 지지·조준 배치만 관찰한다. 실제 발사·반동·적대 의도는 별도다.
- 검토 슬롯: body_pose, contact_point, prop
- 출처 범위: [S02](https://modernrobotics.northwestern.edu/chapters/chapter6/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## H04 검끝과 카메라 원근

기계가 검 하나를 잡고 검끝은 카메라 가까이 있으며 손잡이·손목·어깨는 뒤로 멀어지는 팔을 따라 연결되어 있다.

A machine grips one sword whose tip is close to the camera, while the hilt, wrist and shoulder remain connected along the receding arm.

- 관계: tip → part_of → sword; hilt → part_of → sword; hand → grips → hilt; wrist → joins → hand; tip → near → camera
- 혼동 경계: 검 자체의 거대화, 팔 분리, 실제 내려베기 완료
- 관찰 한계: 원근과 손 소유를 제안한다. 공식 포즈 규격·운동 궤적·승패는 별도다.
- 검토 슬롯: body_pose, composition, contact_point
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## H05 발진 웅크림과 고정 장치

웅크린 기계가 발진 레일 위에 놓이고 발목에 클램프 두 개가 보이며 앞 출구 문은 열려 있다.

A crouched machine rests on a launch rail with two visible clamps at its ankles; the exit door stands open ahead.

- 관계: machine → supported_by → rail; clamps → at → ankles; door → in_front_of → machine
- 혼동 경계: 이미 발진·해제된 상태, 시퀀스 전체
- 관찰 한계: 현재의 고정·문 상태만 보인다. 점검·해제·사출 순서는 별도다.
- 검토 슬롯: body_pose, object_structure
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## H06 정비 인양의 지지 경로

팽팽한 인양 끈 두 개가 크레인 훅에서 매달린 기계의 별도 어깨 인양 고리로 이어지고 두 발은 바닥 위에 떠 있다.

Two taut lifting straps run from a crane hook to separate shoulder lifting eyes on a suspended machine; its feet hang above the floor.

- 관계: straps → joins → hook; straps → joins → lifting_eyes; lifting_eyes → part_of → machine; feet → above → floor
- 혼동 경계: 허공에 떠 있는 기체, 끈이 목에 연결, 안전 인증
- 관찰 한계: 하중 지지 경로의 창작안이다. 실제 인양 안전·질량·정비 원인은 별도다.
- 검토 슬롯: object_structure, contact_point, body_pose
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## H07 손바닥 위 성인의 접지

성인이 거대 기계의 열린 손바닥에 앉아 허벅지와 버티는 한 손을 손바닥에 대고 기계 손가락은 성인 어깨보다 낮게 굽어 있다.

An adult sits on the open palm of a giant machine, with thighs and one bracing hand touching the palm while the machine's fingers curve below shoulder level.

- 관계: adult → sits_on → palm; thighs → part_of → adult; human_hand → part_of → adult; thighs → contacts → palm; human_hand → contacts → palm; palm → part_of → robot_hand; robot_fingers → part_of → robot_hand
- 혼동 경계: 사람을 움켜쥠, 떠 있는 사람, 자동 보호·동의
- 관찰 한계: 지지와 크기 관계만 보인다. 감정·힘 제어·안전·자발성을 확인하지 않는다.
- 검토 슬롯: body_pose, contact_point, scale_relation
- 출처 범위: [S02](https://modernrobotics.northwestern.edu/chapters/chapter6/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## H08 손상 기체의 지지 자세

기계가 한쪽 무릎과 땅에 박힌 무기 끝에 기대고 깨진 어깨판 안으로 어두운 프레임이 보이며 온전한 손은 무기 자루를 잡는다.

A machine rests on one knee and a planted weapon tip; a broken shoulder plate exposes dark framing while the intact hand holds the weapon shaft.

- 관계: knee → contacts → ground; weapon_tip → contacts → ground; hand → grips → shaft; frame → inside → broken_plate
- 혼동 경계: 사망·동력 고갈·필살기 성공
- 관찰 한계: 자세와 결손의 동시 외형이다. 원인·감정·시간 전후는 별도다.
- 검토 슬롯: body_pose, prop_state, contact_point
- 출처 범위: [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## H09 부유 상태와 지면의 틈

기계 두 발이 분명히 바닥 위에 떠 있고 등 팩 아래로 아래쪽 노즐 분출 두 개가 뻗으며 떨어진 그림자가 바닥에 놓인다.

A machine's two feet remain visibly above the floor while two downward nozzle plumes extend below its rear pack; a separated shadow lies on the floor.

- 관계: feet → part_of → machine; feet → above → floor; pack → part_of → machine; plumes → below → pack; shadow → on → floor
- 혼동 경계: 인양 끈 지지·서 있는 자세, 실제 부양력 계산
- 관찰 한계: 그림에서 지면과 떨어진 상태만 보인다. 실제 추력·지속시간·안정성은 별도다.
- 검토 슬롯: body_pose, prop_state
- 출처 범위: [S07](https://www.nasa.gov/reference/european-service-module/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## I01 버클을 당기는 손

착좌한 성인이 한 손으로 허리 버클을 잡고 다른 손으로 어깨끈의 남는 끝을 당기며 등받이에서 앞으로 몸을 기울인다.

A seated adult holds the waist buckle with one hand and pulls the free end of a shoulder strap with the other, leaning forward from the seat back.

- 관계: adult → sits_on → seat; hand_a → holds → buckle; hand_b → pulls → strap; strap → joins → buckle
- 혼동 경계: 옷을 벗는 동작·구속, 끈 양끝 없음
- 관찰 한계: 손·버클·끈의 현재 배치다. 출격 준비·자의·강제 여부는 별도다.
- 검토 슬롯: action, body_pose, contact_point
- 출처 범위: [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## I02 바이저 가장자리와 손

성인의 장갑 낀 손가락이 반쯤 내려온 바이저 아래 가장자리에 닿고 경첩은 헬멧 옆에 붙어 있다.

An adult's gloved fingers touch the lower edge of a partly lowered visor whose hinge remains attached to the helmet side.

- 관계: glove → worn_by → adult; glove → touches → visor; visor → attached_to → hinge; hinge → part_of → helmet
- 혼동 경계: 얼굴 자체가 투명, 동작 방향·완료
- 관찰 한계: 반개방 상태와 접점만 보인다. 실제 올림·내림의 시간 방향은 별도다.
- 검토 슬롯: body_pose, contact_point
- 출처 범위: [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## I03 옆구리에 낀 헬멧

성인이 기계 옆에 서서 굽힌 아래팔과 옆구리 사이에 헬멧을 끼고 다른 손은 허리 벨트에 둔다.

An adult stands beside a machine, holding a helmet between the bent forearm and hip; the other hand rests on a waist belt.

- 관계: helmet → between → forearm; helmet → contacts → hip; other_hand → rests_on → belt; adult → beside → machine
- 혼동 경계: 헬멧 착용과 동시 손실, 자동 성적 의미
- 관찰 한계: 성인 화보의 비노골적 대안이다. 조종사 신분·관객 욕망·동의는 외형으로 확정하지 않는다.
- 검토 슬롯: body_pose, prop, contact_point
- 출처 범위: [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/), [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## I04 정비 패널과 공구 끝

쪼그린 성인이 한 손을 기계의 열린 점검구 테두리에 받치고 다른 손의 공구 끝은 홈 내부 체결부에 닿는다.

A crouching adult braces one hand on a machine's open panel rim while a tool in the other hand meets a fastener inside the recess.

- 관계: hand_a → contacts → rim; hand_b → holds → tool; tool → contacts → fastener; fastener → inside → recess
- 혼동 경계: 손이 기계 안에서 사라짐, 수리 완료
- 관찰 한계: 지지와 작업 말단의 한 순간만 보인다. 정비 효과·전기 안전·직업은 별도다.
- 검토 슬롯: action, body_pose, contact_point
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## I05 새들 좌석과 발 디딤

성인이 좁은 새들 좌석 양옆으로 다리를 나눠 걸터앉고 손은 앞 핸들에, 부츠는 별도 발받침에 둔다.

An adult sits astride a narrow saddle seat with one leg on each side, hands on forward bars and boots resting on separate footrests.

- 관계: adult → sits_on → saddle; left_leg → beside → saddle; right_leg → beside → saddle; adult → holds → bars; boots → rests_on → footrests
- 혼동 경계: 성행위·강제 장치, 좌석을 관통한 다리
- 관찰 한계: 성인 착좌와 지지 배치다. 성적 기능·동의·신경 제어는 별도다.
- 검토 슬롯: body_pose, contact_point, object_structure
- 출처 범위: [S02](https://modernrobotics.northwestern.edu/chapters/chapter6/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## I06 기체를 올려다보는 시선

격납고 바닥의 성인이 기계의 높은 얼굴을 향해 고개를 들고 바닥 가까운 카메라는 두 대상을 한 화면에 담는다.

An adult on the hangar floor tilts the head toward a machine's raised face; the camera sits near floor level with both figures in one view.

- 관계: adult → on → floor; head → oriented_toward → machine_face; camera → near → floor
- 혼동 경계: 공포·존경·소유권 확정, 별도 그림의 크기 비교
- 관찰 한계: 같은 공간의 시선과 크기 관계다. 감정·정확한 키는 별도다.
- 검토 슬롯: gaze_target, composition, scale_relation
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## I07 안드로이드 대기와 시선 대응

성인으로 설정된 안드로이드가 양손을 무릎 위에 놓고 앉아 같은 탁자에 앉은 별도 성인을 향해 얼굴을 돌린다.

An adult-presenting android sits with both hands resting on the knees and its face turned toward a separate adult seated at the same table.

- 관계: hands → part_of → android; hands → rests_on → knees; android → faces → adult; adult → beside → table
- 혼동 경계: 정지=무자아·복종, 시선=사랑·동의
- 관찰 한계: 대기 자세와 얼굴 방향만 보인다. 부팅·각성·로맨스·관계의 진정성은 별도다.
- 검토 슬롯: body_pose, gaze_target, relational_action
- 출처 범위: [S19](https://spectrum.ieee.org/the-uncanny-valley), [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## I08 귀환을 암시하는 소지·자세

성인이 격납고 벤치에 앉아 옆자리에 헬멧을 두고 장갑 낀 손을 허벅지 위에 느슨하게 올린다.

An adult sits on a hangar bench with the helmet on the adjacent seat and gloved hands resting loosely on the thighs.

- 관계: adult → sits_on → bench; helmet → on → bench; hands → rests_on → thighs
- 혼동 경계: 전투 이력·의학적 피로·탈의의 자동 판정
- 관찰 한계: 현재의 소지와 자세만 보인다. 직전 출격·탈진·동의는 별도다.
- 검토 슬롯: body_pose, prop
- 출처 범위: [S06](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## J01 기계 절단의 분리·노출

분리된 기계 팔이 기계의 빈 어깨 소켓 옆에 놓이고 양쪽 떨어진 끝에 흐트러진 케이블이 보인다.

A detached mechanical arm lies beside the machine's empty shoulder socket; frayed cables remain visible at both separated ends.

- 관계: shoulder_socket → part_of → machine; arm → separated_from → shoulder_socket; arm_cables → part_of → arm; body_cables → inside → shoulder_socket
- 혼동 경계: 인간 절단·혈액, 분리 팔다리 소유 오류
- 관찰 한계: 기계 부품의 결손만 제안한다. 유기체 손상·통증·동의·원인은 별도다.
- 검토 슬롯: prop_state, object_structure
- 출처 범위: [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## J02 장갑 박리와 프레임의 연속

벗겨진 장갑 시트가 기계 리브 프레임에서 바깥으로 말리고 한 가장자리는 붙어 있으며 아래 프레임은 이어져 있다.

A peeled armor sheet curls outward from a machine's rib frame while one edge stays attached; the frame beneath remains continuous.

- 관계: attached_edge → part_of → sheet; attached_edge → attached_to → frame; sheet → curls_away_from → frame
- 혼동 경계: 장갑이 천이나 피부로 변함, 박리 과정 완료
- 관찰 한계: 박리된 현재 상태의 창작안이다. 손상 원인·실제 재료는 별도다.
- 검토 슬롯: prop_state, object_structure
- 출처 범위: [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## J03 합성 피부 아래 기계와 매체 소유

성인으로 설정된 안드로이드 아래팔 가장자리의 피부 같은 얇은 덮개가 들려 아래 금속 리브와 배선을 드러내고 나머지 몸은 불투명 작업복에 가려져 있다.

A skinlike flap at an adult-presenting android's forearm edge reveals metal ribs and wiring beneath; the rest of the body is covered by an opaque work garment.

- 관계: flap → part_of → forearm; forearm → part_of → android; ribs → beneath → flap; wiring → beneath → flap; garment → worn_by → android
- 혼동 경계: 인간 피부 상해, 무의미한 전신 노출로 대체
- 관찰 한계: 표면·기계 층만 보인다. 유기체 기원·통증·로봇화의 시간 변화는 별도다.
- 검토 슬롯: body_form, prop_state, object_structure
- 출처 범위: [S20](https://escholarship.org/content/qt4qn696qm/qt4qn696qm_noSplash_003e980880283926108e8646b3a84a9a.pdf), [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## J04 유기형 형상과 실제 조직의 경계

주름진 살 같은 다발이 단단한 금속 리브 사이를 지나 기계 내부 몸통의 경계가 있는 소켓으로 들어간다.

Ridged fleshlike bundles pass between rigid metal ribs and enter bounded sockets along a machine's inner torso.

- 관계: bundles → passes_between → metal_ribs; bundles → enters → sockets; sockets → part_of → inner_torso
- 혼동 경계: 호스가 곧 생체조직, 실제 공생·기생 증명
- 관찰 한계: 유기적 외관과 물리 접속을 제안한다. 생물학·생명·감염·강제성은 별도다.
- 검토 슬롯: object_structure, surface_material
- 출처 범위: [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## J05 콕핏 파열과 내부 좌석

기계 흉부 장갑의 찢어진 개구부 뒤로 휘어진 내부 버팀대와 별도의 온전한 빈 조종석 좌석이 보인다.

A torn opening in the machine's chest armor exposes a separate intact cockpit seat behind bent inner struts; no person occupies the seat.

- 관계: opening → breaches → chest_armor; struts → inside → opening; seat → behind → struts
- 혼동 경계: 외장 흠집=콕핏 관통, 사람의 상해·사망 자동 추가
- 관찰 한계: 파열 범위와 빈 좌석만 보인다. 사건 원인·전후 탑승자·생존 여부는 별도다.
- 검토 슬롯: prop_state, object_structure
- 출처 범위: [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186), [S23](https://en.gundam-official.com/feature/pgu-rx93/images/system_img_chest_250603.png)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## J06 코어 파열과 에너지 주장 분리

갈라진 원형 하우징이 열린 몸통 베이 안에 놓이고 베이 가장자리에는 분리된 외장 파편, 균열 안에는 작은 밝은 빛이 있다.

A cracked circular housing lies inside an open torso bay, with separated casing fragments around the bay rim and a small bright glow within the crack.

- 관계: housing → inside → bay; crack → part_of → housing; fragments → around → bay; glow → inside → crack
- 혼동 경계: 핵폭발·방사선·과부하의 실제 증거
- 관찰 한계: 파손과 발광의 현재 외형이다. 반응로 종류·방사선·폭발 원인·위력은 별도다.
- 검토 슬롯: prop_state, lighting
- 출처 범위: [S07](https://www.nasa.gov/reference/european-service-module/), [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## J07 기생형 표면 침입의 국소 배치

갈라지는 유기물 같은 덩어리가 기계 어깨 외장 위에 퍼져 열린 정비 틈 하나로 들어가고 반대 어깨는 덮이지 않은 채 남는다.

A branching organic-looking mass spreads across a machine's shoulder casing and enters one open service gap while leaving the opposite shoulder uncovered.

- 관계: mass → on → shoulder_casing; mass → enters → service_gap; mass → distinct_from → opposite_shoulder
- 혼동 경계: 장식 덩굴, 실제 감염·제어권 탈취
- 관찰 한계: 피복·침입 경계만 보인다. 생명·증식·시간·제어권·강제성은 별도다.
- 검토 슬롯: prop_state, object_structure
- 출처 범위: [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## J08 잔해 회수와 부품 전용

도색이 다른 교체 팔이 기계의 열린 어깨 결합부 옆 인양기에 놓이고 맞은편 커넥터 면이 서로 향한다.

A replacement arm with a different paint color rests on a hoist beside a machine's open shoulder coupling; matching connector faces point toward each other.

- 관계: replacement_arm → supported_by → hoist; coupling → part_of → machine; connector_a → part_of → replacement_arm; connector_b → part_of → coupling; connector_a → faces → connector_b
- 혼동 경계: 다른 기체의 역사·약탈 확정, 장착 완료
- 관찰 한계: 교체 부품의 현재 배치다. 기원·소유권·전후 시간·재난 원인은 별도다.
- 검토 슬롯: prop_state, object_structure
- 출처 범위: [S21](https://iopn.library.illinois.edu/journals/jams/article/view/1186)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## K01 컷어웨이와 현장 점검의 표현층

경계가 있는 기술 그림에 깨끗한 절개 경계 하나를 가진 기계 몸통이 그려지고 생략한 외장 뒤로 좌석과 내부 프레임이 표현된다.

A bounded technical illustration depicts a machine torso with one clean section boundary, exposing a seat and internal frame behind the omitted shell.

- 관계: depicted_torso → represented_in → illustration; section → part_of → depicted_torso; depicted_seat → behind → section; depicted_frame → behind → section
- 혼동 경계: 실제 외장 파괴, 현실층에 없는 내부를 투시 사진처럼 주장
- 관찰 한계: 도해 표현만 제안한다. 실제 단일 사진·파손·시공 순서를 뜻하지 않는다.
- 검토 슬롯: composition, object_structure
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/), [S23](https://en.gundam-official.com/feature/pgu-rx93/images/system_img_chest_250603.png)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## K02 분해도의 축 정렬

경계가 있는 조립 도해에 어깨판·스페이서·프레임 연결 귀가 하나의 점선 조립축을 따라 떨어져 있고 각 부품은 한 번씩 그려져 있다.

A bounded assembly diagram shows a shoulder plate, spacer and frame lug separated along one dashed assembly axis, with each part drawn once.

- 관계: plate → represented_in → diagram; spacer → represented_in → diagram; lug → represented_in → diagram; plate → aligned_with → axis; spacer → aligned_with → axis; lug → aligned_with → axis
- 혼동 경계: 부품이 실제 공중부양, 조립 동작·숨은 부품
- 관찰 한계: 도해의 공간 분리다. 단일 사진·실제 순서·설계 검증으로 자동 전환하지 않는다.
- 검토 슬롯: composition, object_structure
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## K03 삼면도의 대응과 일관성

설정 시트 하나에 기계 정면·측면·후면의 경계가 있는 도면이 있고 수평 안내선이 같은 어깨·골반 높이를 맞춘다.

One design sheet contains bounded front, side and rear views of a machine, with horizontal guide lines aligning the same shoulder and hip heights.

- 관계: front_view → on → sheet; side_view → on → sheet; rear_view → on → sheet; guides → aligns → front_view; guides → aligns → side_view; guides → aligns → rear_view
- 혼동 경계: 실물 세 대, 원근 사진이 정투상
- 관찰 한계: 표현층의 대응만 보인다. 모든 부품의 완전한 3D 일관성·정확 치수는 별도 검토한다.
- 검토 슬롯: composition
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## K04 HUD와 실물 표적의 분리

바이저의 경계가 있는 투명 표시창에 작은 조준선이 먼 기계의 보이는 모습 위로 겹치고 표시창 끝과 바이저 테두리는 계속 보인다.

A visor's bounded transparent display carries a small reticle over the view of a distant machine; the display edge and visor rim remain visible.

- 관계: display → part_of → visor; reticle → represented_in → display; reticle → overlays → distant_machine; rim → bounds → visor
- 혼동 경계: 공중 거대 홀로그램, 정확 록온·사격 성공
- 관찰 한계: 표시와 외부 실물의 층만 표현한다. 센서 정확도·공격 의도·교차편집 시간은 별도다.
- 검토 슬롯: composition, prop
- 출처 범위: [S03](https://www-robotics.jpl.nasa.gov/what-we-do/research-tasks/shared-and-traded-control-for-remote-teleoperation/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## K05 순차 연출을 위한 별도 패널

3칸 스토리보드에서 같은 기계의 닫힌 해치, 열린 해치, 분리된 좌석 캡슐이 각기 별도 경계의 칸에 그려져 있다.

A three-panel storyboard shows one machine with a closed hatch, the hatch open, and a seat capsule separated; each panel has a distinct border.

- 관계: panel_a → part_of → storyboard; panel_b → part_of → storyboard; panel_c → part_of → storyboard; machine_a → represented_in → panel_a; machine_b → represented_in → panel_b; machine_c → represented_in → panel_c
- 혼동 경계: 한 사진에서 시간 전체 증명, 기체 복제
- 관찰 한계: 순서가 명시된 연속 도해 전용 제안이다. 각 패널의 동일성·연속성은 별도 검토한다.
- 검토 슬롯: composition
- 출처 범위: [S13](https://macross.jp/pages/series?title=macrosszero)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## K06 궤적과 다량 발사의 차이

경계가 있는 액션 그림에 서로 다른 깊이의 굽은 연기 궤적을 가진 별도 미사일 여러 개가 항공기 실루엣 하나 주위를 휘감는다.

A bounded action illustration contains several separate missiles with curving smoke trails at different depths, weaving around one aircraft silhouette.

- 관계: missiles → represented_in → illustration; trails → represented_in → illustration; trails → curves_around → aircraft; aircraft → represented_in → illustration
- 혼동 경계: 그냥 다량 미사일=특정 연출가의 기법, 움직임·타격 증명
- 관찰 한계: 궤적을 묘사한 정지 그림의 창작안이다. 이타노 기법의 정확한 계보·영상 리듬 검토는 보류다.
- 검토 슬롯: composition, prop_state
- 출처 범위: [S13](https://macross.jp/pages/series?title=macrosszero)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

## K07 실루엣과 부분 리빌의 가림

역광을 받는 기계가 격납고 문 뒤에 일부 가려져 문 틈에는 한쪽 어깨·머리 윤곽·딛은 한 발만 보인다.

A backlit machine is partly hidden behind a hangar door; only one shoulder, the head outline and one planted foot remain visible at the doorway.

- 관계: door → occludes → machine; shoulder → part_of → machine; head_outline → part_of → machine; foot → contacts → ground
- 혼동 경계: 가린 부품을 검증한 것으로 처리, 전체 형태의 자동 완성
- 관찰 한계: 의도적 부분 공개안이다. 다른 카드의 숨겨진 연결·센서·부품 조건을 대신 충족하지 않는다.
- 검토 슬롯: composition, lighting
- 출처 범위: [S11](https://en.gundam-official.com/feature/pgu-rx93/)
- 상태: 전체 한영 문장과 모든 관계 양끝을 함께 확인해야 함. `partial_is_fail`; `UNOBSERVABLE_NOT_PASS`; pixels `NOT_RUN`.

