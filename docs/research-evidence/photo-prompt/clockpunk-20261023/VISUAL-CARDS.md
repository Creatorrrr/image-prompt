# 시각 의미 카드

상태: 연구 초안. 실제 source 등록·native 자격·검색·픽셀은 미실행. source가 지원하는 의미와 새로 저술한 장면을 구분한다. 관계 표식은 실제 runtime schema가 아니다.

## A01 동력 태엽과 태엽통

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure, prop
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S02](https://catalogue.museogalileo.it/object/ModelPendulumClock.html)
- 소유자: spring: flat coiled mainspring; barrel: open spring barrel; arbor: central arbor
- 관계: spring → inside → barrel; spring → coiled_around → arbor
- EN: An open spring barrel contains a broad flat mainspring coiled around its central arbor.
- KO: 열린 태엽통 안에서 넓고 납작한 동력 태엽이 중심 축 둘레에 감겨 있다.
- 혼동: 밸런스 실태엽·장식 나선
- 입증 한계: 저장 에너지·합금·실제 작동 시간은 외형만으로 측정되지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: A01-R1, A01-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A02 추 구동과 수직 여유

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure, space_condition
- 출처: [S02](https://catalogue.museogalileo.it/object/ModelPendulumClock.html)
- 소유자: weight: hanging weight; cord: support cord; drum: winding drum; shaft: clear vertical shaft
- 관계: weight → suspended_from → cord; cord → wound_on → drum; weight → within → shaft
- EN: A hanging weight is suspended by a cord wound on a drum above a clear vertical shaft.
- KO: 비어 있는 수직 공간 위의 무게추가 드럼에 감긴 줄에 매달려 있다.
- 혼동: 태엽 구동·진자 추
- 입증 한계: 중력 동력의 가능한 배치를 제안하며 실제 하강·출력 토크는 입증하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: A02-R1, A02-R2, A02-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A03 맞물린 기어열

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S02](https://catalogue.museogalileo.it/object/ModelPendulumClock.html)
- 소유자: large: large toothed wheel; small: small pinion; frame: movement frame
- 관계: large → meshes_with → small; small → mounted_in → frame
- EN: A large toothed wheel meshes with a smaller pinion, both mounted on separate arbors in one movement frame.
- KO: 같은 무브먼트 프레임의 서로 다른 축에 놓인 큰 톱니바퀴와 작은 피니언이 맞물린다.
- 혼동: 기어가 흩어진 표면 장식
- 입증 한계: 기어는 전달계이며 독립 에너지원이 아니다. 속도비 계산·맞물림 전체의 기능 검증은 별도다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: A03-R1, A03-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A04 탈진기 접촉

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure, contact_point
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S02](https://catalogue.museogalileo.it/object/ModelPendulumClock.html)
- 소유자: wheel: escape wheel; pallet: pallet; frame: clock frame
- 관계: pallet → contacts_tooth_of → wheel; wheel → mounted_in → frame
- EN: In an open clock frame, one pallet contacts a tooth of the escape wheel while the neighboring teeth remain visible.
- KO: 열린 시계 프레임 안에서 팔레트 하나가 탈진 바퀴의 이 하나와 접촉하고 주변 이들도 보인다.
- 혼동: 조속 날개·단순 기어열
- 입증 한계: 한 장면은 접촉 형상만 보여 준다. 똑딱임·주기·정확한 동력 전달은 시간 검증 대상이다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: A04-R1, A04-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A05 버지와 폴리엇

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, historical_period
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S03](https://www.cabinet.ox.ac.uk/key-innovation-escapement-0)
- 소유자: crown: crown wheel; verge: vertical verge; bar: horizontal foliot; weights: pair of adjustable weights
- 관계: verge → beside → crown; bar → crosses → verge; weights → on → bar
- EN: A vertical verge stands beside a crown wheel; a horizontal foliot crosses its top with an adjustable weight near each end.
- KO: 수직 버지가 크라운 휠 옆에 서고 상단의 가로 폴리엇 양끝 가까이에 조절 추가 놓인다.
- 혼동: 추시계 진자·밸런스 휠
- 입증 한계: 시대 해설은 색인 근거다. 이 배치의 제작 연대와 진동 성능은 사진으로 확정하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: A05-R1, A05-R2, A05-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A06 밸런스 휠과 실태엽

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches)
- 소유자: balance: balance wheel; spring: fine spiral balance spring; staff: balance staff
- 관계: spring → centered_on → staff; balance → mounted_on → staff
- EN: A fine spiral balance spring sits above a balance wheel, with both centered on the same balance staff.
- KO: 가느다란 나선 실태엽이 밸런스 휠 위에 놓이고 둘은 같은 밸런스 축을 중심으로 한다.
- 혼동: 굵은 동력 태엽·회전 플라이휠
- 입증 한계: 실태엽은 복원 요소다. 모든 시대의 휴대시계에 자동 부여하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: A06-R1, A06-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A07 퓨지의 원뿔과 체인

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches)
- 소유자: cone: grooved fusee cone; chain: fine chain; barrel: spring barrel
- 관계: chain → follows_groove_of → cone; chain → connects_to → barrel
- EN: A fine chain follows the spiral groove of a fusee cone and connects to the neighboring spring barrel.
- KO: 가느다란 체인이 퓨지 원뿔의 나선 홈을 따라 감겨 옆 태엽통에 연결된다.
- 혼동: 원뿔 장식·시계 태엽 자체
- 입증 한계: 원뿔·홈·체인의 두 종단이 함께 보여야 한다. 힘 보정 수치는 별도 측정한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: A07-R1, A07-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A08 래칫과 걸쇠

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, contact_point
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S13](https://museoleonardiano.it/en/opera/the-self-moving-carriage-2010/)
- 소유자: ratchet: asymmetric toothed ratchet; pawl: pivoted pawl; pin: pawl pivot
- 관계: pawl → seated_between_teeth_of → ratchet; pawl → hinged_on → pin
- EN: A pivoted pawl rests between two asymmetric ratchet teeth, with its pivot and contact point exposed.
- KO: 축에 달린 걸쇠가 비대칭 래칫 이 사이에 걸려 있고 걸쇠 축과 접촉점이 드러난다.
- 혼동: 톱니 모양 장식·무조건 완벽한 잠금
- 입증 한계: 정방향/역방향 응답과 잠금 강도는 정지 사진에서 검증하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: A08-R1, A08-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A09 플라이휠의 림과 허브

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure
- 출처: [S02](https://catalogue.museogalileo.it/object/ModelPendulumClock.html), [S14](https://khkgears.net/gear-knowledge/gear-technical-reference/calculation-gear-dimensions/)
- 소유자: rim: heavy wheel rim; spokes: wheel spokes; hub: central hub; shaft: shaft
- 관계: spokes → connect → rim; spokes → connect → hub; hub → mounted_on → shaft
- EN: Broad spokes connect a heavy circular rim to a hub mounted on a shaft.
- KO: 굵은 스포크가 무거워 보이는 원형 림과 축에 끼워진 허브를 연결한다.
- 혼동: 얇은 조속 날개·장식 원판
- 입증 한계: 질량·관성·회전 안정화의 실제 크기는 외형으로 입증하지 않는다. 기술 상세의 추가 원전 검토가 필요하다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: True
- 관계 gate: A09-R1, A09-R2, A09-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A10 조속 날개와 타종 계통

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)
- 소유자: vane: pair of thin vanes; spindle: slender spindle; train: striking gear train
- 관계: vane → mounted_on → spindle; spindle → connected_to → train
- EN: Two thin flat vanes extend from a slender spindle connected to the exposed striking train.
- KO: 노출된 타종 기어열에 연결된 가느다란 축에서 얇고 평평한 날개 두 개가 뻗는다.
- 혼동: 플라이휠·원심구 조속기
- 입증 한계: 공기저항 조속이라는 기능은 설정/기술 문헌의 별도 주장이다. 구체 형식의 기술 원전 추가 검토가 필요하다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: True
- 관계 gate: A10-R1, A10-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A11 타종 망치와 종

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, prop_state
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)
- 소유자: hammer: bell hammer; bell: bell; rod: hammer linkage
- 관계: hammer → beside → bell; rod → attached_to → hammer
- EN: A linked bell hammer is held just clear of the bell rim, its connecting rod visible behind it.
- KO: 종 테두리 바로 앞에 망치가 떨어져 있고 뒤로 망치에 연결된 막대가 보인다.
- 혼동: 종 자체·방금 울렸다는 주장
- 입증 한계: 소리·정시·타격 횟수는 보이지 않는다. 시각 다이얼과 타종 계통을 무조건 같은 출력으로 합치지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: A11-R1, A11-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## A12 파워 리저브 표시

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: prop_state, visible_text
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S11](https://www.rmg.co.uk/stories/time/harrisons-clocks-longitude-problem)
- 소유자: indicator: reserve indicator; hand: indicator hand; scale: marked scale; socket: accessible winding square
- 관계: hand → points_to → scale; scale → part_of → indicator; socket → beside → indicator
- EN: A small reserve indicator has a hand near the low end of its marked scale beside an accessible winding square.
- KO: 감는 사각 축 옆 작은 잔량 표시계의 바늘이 표시 눈금의 낮은 쪽을 가리킨다.
- 혼동: 표시 바늘=실제 잔여 시간
- 입증 한계: 눈금·단위·보정이 없으면 잔여 시간을 수치로 확정하지 않는다. 표시와 실제 동력 상태는 분리한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: A12-R1, A12-R2, A12-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B01 캠과 팔로어

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure, contact_point
- 출처: [S05](https://blog.sciencemuseum.org.uk/introducing-the-draughtsman-writer-automaton/)
- 소유자: cam: shaped cam; follower: roller follower; rod: follower rod
- 관계: follower → contacts_profile_of → cam; rod → attached_to → follower
- EN: A roller follower contacts the uneven edge of a shaped cam, with a rod extending from the follower.
- KO: 롤러 팔로어가 윤곽이 불균일한 캠 가장자리에 닿고 팔로어에서 막대가 이어진다.
- 혼동: 기어 맞물림·임의 타원 장식
- 입증 한계: 접촉과 형상은 보이지만 회전 전 주기의 궤적·출력 동작은 시간 검증이 필요하다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: B01-R1, B01-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B02 캠 스택과 분리 출력

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure
- 출처: [S05](https://blog.sciencemuseum.org.uk/introducing-the-draughtsman-writer-automaton/)
- 소유자: cams: stack of three cams; shaft: shared shaft; followers: three follower rods
- 관계: cams → mounted_on → shaft; followers → contact → cams
- EN: Three differently shaped cams share one shaft, each touched by its own separate follower rod.
- KO: 서로 다른 윤곽의 캠 세 개가 같은 축에 있고 각각 별도 팔로어 막대와 접촉한다.
- 혼동: 캠 수=인형의 지능·동일 동작
- 입증 한계: 세 출력의 소유자와 연결을 유지한다. 완전한 프로그램·성격·기억 교체는 허구적 확장이다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: B02-R1, B02-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B03 핀 실린더와 빗살

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)
- 소유자: barrel: pinned cylinder; comb: tuned metal comb; axle: cylinder axle
- 관계: barrel → mounted_on → axle; comb → beside → barrel
- EN: Rows of raised pins cover a cylinder mounted on an axle beside a metal comb with separately cut teeth.
- KO: 축에 끼운 원통 표면에 핀이 줄지어 있고 옆에는 이가 따로 잘린 금속 빗살이 놓인다.
- 혼동: 캠 묶음·천공 카드·하프시코드
- 입증 한계: 선율·발음 방식·실제 재생은 정지 이미지에서 판정하지 않는다. 장치 형식의 추가 원전 대조가 필요하다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: True
- 관계 gate: B03-R1, B03-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B04 링크의 관절 사슬

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure
- 출처: [S12](https://museoleonardiano.it/en/opera/rack-and-pinion/), [S13](https://museoleonardiano.it/en/opera/the-self-moving-carriage-2010/)
- 소유자: link1: first rigid link; link2: second rigid link; pivot: shared pin; hand: automaton hand
- 관계: link1 → joined_by_pin_to → link2; link2 → connected_to → hand; pivot → joins → link1; pivot → joins → link2
- EN: Two rigid links meet at an exposed pin joint, and the second link connects to the automaton hand.
- KO: 단단한 링크 두 개가 드러난 핀 관절에서 만나고 두 번째 링크가 자동인형 손에 연결된다.
- 혼동: 기계 관절 장식·공중에서 끊긴 연결
- 입증 한계: 손의 소유자·출력 종단을 유지한다. 실제 손 궤적은 별도 검증한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: B04-R1, B04-R2, B04-R3, B04-R4 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B05 크랭크 슬라이더

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure
- 출처: [S12](https://museoleonardiano.it/en/opera/rack-and-pinion/), [S13](https://museoleonardiano.it/en/opera/the-self-moving-carriage-2010/), [S42](https://digital.library.cornell.edu/catalog/ss%3A372515)
- 소유자: crank: offset crank pin; rod: connecting rod; slider: rectangular slider; guide: straight guide
- 관계: rod → connects → crank; rod → connects → slider; slider → inside → guide
- EN: A connecting rod links an offset crank pin to a rectangular slider seated inside a straight guide.
- KO: 커넥팅 로드가 편심 크랭크 핀과 직선 가이드 안의 사각 슬라이더를 연결한다.
- 혼동: 회전축 없는 막대·왕복 운동의 완주
- 입증 한계: 구체 기하는 저술한 공학 제안이다. 기구학 치수·간섭·작동 전 주기는 검증 전이다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: True
- 관계 gate: B05-R1, B05-R2, B05-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B06 랙과 피니언

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure
- 출처: [S12](https://museoleonardiano.it/en/opera/rack-and-pinion/)
- 소유자: rack: straight toothed rack; pinion: round toothed pinion; guide: rack guide
- 관계: pinion → meshes_with → rack; rack → inside → guide
- EN: A round pinion meshes with a straight vertical toothed rack held inside a guide.
- KO: 둥근 피니언이 가이드 안에 놓인 수직 직선 톱니 랙과 맞물린다.
- 혼동: 기어 두 개·장식 사다리
- 입증 한계: 회전→직선 변환의 가능한 구조를 보이며 실제 하중·리프트 성공은 입증하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: B06-R1, B06-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B07 웜과 웜휠

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure
- 출처: [S14](https://khkgears.net/gear-knowledge/gear-technical-reference/calculation-gear-dimensions/), [S45](https://www.qtcgears.com/tools/catalogs/PDF_Q420/Tech.pdf)
- 소유자: worm: screw-like worm; wheel: worm wheel; shafts: two nonparallel nonintersecting shafts
- 관계: worm → meshes_with → wheel; shafts → carry → worm; shafts → carry → wheel
- EN: A screw-like worm meshes with a toothed worm wheel on a separate nonintersecting shaft.
- KO: 나사 모양 웜이 서로 교차하지 않는 별도 축의 톱니 웜휠과 맞물린다.
- 혼동: 웜 기어=항상 역구동 불가
- 입증 한계: 자기잠김·효율·감속비·하중 안전성은 별도다. S14는 색인 구절만 확인했다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: B07-R1, B07-R2, B07-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B08 베벨 기어의 축 방향

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure
- 출처: [S14](https://khkgears.net/gear-knowledge/gear-technical-reference/calculation-gear-dimensions/), [S45](https://www.qtcgears.com/tools/catalogs/PDF_Q420/Tech.pdf)
- 소유자: gear1: first bevel gear; gear2: second bevel gear; axis1: first shaft; axis2: second shaft
- 관계: gear1 → meshes_with → gear2; axis1 → intersects_axis_of → axis2
- EN: Two conical bevel gears mesh on shafts whose axes intersect at the corner of the frame.
- KO: 원뿔형 베벨 기어 두 개가 프레임 모서리에서 축선이 만나는 두 축 위에 맞물린다.
- 혼동: 웜 기어·평행 스퍼 기어
- 입증 한계: 보이는 축선 관계를 평가하고 기어 형태만으로 회전 방향·비율을 추정하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: B08-R1, B08-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B09 유성기어의 소유 구조

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure
- 출처: [S14](https://khkgears.net/gear-knowledge/gear-technical-reference/calculation-gear-dimensions/), [S26](https://www.ucl.ac.uk/news/2021/mar/experts-recreate-mechanical-cosmos-worlds-first-computer), [S45](https://www.qtcgears.com/tools/catalogs/PDF_Q420/Tech.pdf)
- 소유자: sun: central sun gear; planets: three planet gears; ring: internally toothed ring; carrier: carrier
- 관계: planets → surround → sun; planets → inside → ring; carrier → holds → planets
- EN: Three planet gears surround a central sun gear inside an internally toothed ring, with their pins held by one carrier.
- KO: 내치 링 안의 중심 선기어를 유성기어 세 개가 둘러싸고 한 캐리어가 각 핀을 지지한다.
- 혼동: 오러리·단순 동심 고리
- 입증 한계: 행성이라는 이름이 천문기구를 뜻하지 않는다. 입력/고정/출력 부재는 요청별로 따로 선언한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: B09-R1, B09-R2, B09-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B10 제네바 기구의 슬롯 진입

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure, contact_point
- 출처: [S15](https://www.dmg-lib.org/dmglib/handler?mcdsc=208025)
- 소유자: driver: driver disk; pin: offset driver pin; wheel: four-slot wheel
- 관계: pin → mounted_on → driver; pin → inside_slot_of → wheel
- EN: An offset pin on a driver disk sits within one radial slot of a four-slot Geneva wheel.
- KO: 구동 원판의 편심 핀이 네 슬롯 제네바 휠의 방사형 슬롯 하나 안에 들어 있다.
- 혼동: 별 모양 장식·연속 기어 맞물림
- 입증 한계: 네 슬롯은 이 실현의 선택이다. 간헐 회전·정지 시간은 연속 영상이나 기구 검증으로 평가한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: B10-R1, B10-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B11 차동의 다축 연결

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure
- 출처: [S14](https://khkgears.net/gear-knowledge/gear-technical-reference/calculation-gear-dimensions/)
- 소유자: carrier: central carrier; pinions: internal bevel pinions; left: left side gear; right: right side gear
- 관계: carrier → holds → pinions; pinions → mesh_with → left; pinions → mesh_with → right
- EN: An open carrier holds small bevel pinions between two opposed side gears on separate output shafts.
- KO: 열린 캐리어가 서로 마주 보는 별도 출력축의 사이드 기어 사이에 작은 베벨 피니언들을 지지한다.
- 혼동: 유성 감속기·축이 하나인 장식
- 입증 한계: 이는 저술한 구조 초안이다. 정확한 차동 관계·역사 연대는 추가 기술 원전 검토 뒤 확정한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: True
- 관계 gate: B11-R1, B11-R2, B11-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## B12 계산기와 기계 기억 경계

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: object_structure, visible_text
- 출처: [S05](https://blog.sciencemuseum.org.uk/introducing-the-draughtsman-writer-automaton/), [S26](https://www.ucl.ac.uk/news/2021/mar/experts-recreate-mechanical-cosmos-worlds-first-computer)
- 소유자: wheels: number wheels; windows: separate readout windows; lever: setting lever
- 관계: wheels → visible_through → windows; lever → beside → windows
- EN: Number wheels are visible through separate readout windows, with a setting lever beside the display.
- KO: 각각 나뉜 표시창으로 숫자 바퀴가 보이고 표시부 옆에 설정 레버가 놓인다.
- 혼동: 숫자 표시=정답·지능·기억 이해
- 입증 한계: 실제 계산 정확도·연산 종류·자동 결정은 보이지 않는다. 특정 역사 계산기 복제로 주장하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: B12-R1, B12-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## C01 필기 자동인형의 손과 종이

- 우선순위/가시성: P0 / still_proxy
- 제안 역할: relational_action, contact_point
- 출처: [S05](https://blog.sciencemuseum.org.uk/introducing-the-draughtsman-writer-automaton/), [S39](https://www.theinventionofhugocabret.com/about_hugo_auto.htm)
- 소유자: figure: writing automaton; hand: its articulated hand; pen: pen; paper: paper
- 관계: hand → part_of → figure; hand → holds → pen; pen → touches → paper
- EN: The writing automaton's articulated hand holds a pen with its nib touching a line on the paper.
- KO: 필기 자동인형의 관절 손이 펜을 잡고 펜촉이 종이 위 선에 닿는다.
- 혼동: 인형 옆 완성 편지=작성 증명
- 입증 한계: 펜촉 접촉은 보이지만 작품 전체를 썼다는 인과·제작자 서명·자유로운 저술 능력은 입증하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: C01-R1, C01-R2, C01-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## C02 연주 동작과 발음 장치

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: relational_action, object_structure
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)
- 소유자: figure: mechanical performer; hand: its hand; instrument: small musical instrument; keys: instrument keys; pipes: organ pipes
- 관계: hand → part_of → figure; hand → touches → keys; keys → part_of → instrument; pipes → part_of → instrument
- EN: A mechanical performer's hand touches the keys of a small instrument with a separate row of organ pipes belonging to that instrument behind it.
- KO: 기계 연주자의 손이 작은 악기의 건반에 닿고 뒤에는 그 악기에 속한 별도 오르간 파이프 줄이 보인다.
- 혼동: 몸짓만 하는 인형=실제 발음
- 입증 한계: 손·건반·음원은 분리 소유자로 정제해야 한다. 소리와 연주 인과는 시간/음향 검증 대상이다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: C02-R1, C02-R2, C02-R3, C02-R4 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## C03 식탁 자동장치의 숨은 바퀴

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, prop_state
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)
- 소유자: animal: metal stag-shaped vessel; base: wheeled base; head: detachable head; neck: neck opening
- 관계: animal → mounted_on → base; head → beside → neck
- EN: A metal stag-shaped vessel sits on a small wheeled base, its detached head beside the open neck.
- KO: 금속 사슴형 용기가 작은 바퀴 받침 위에 놓이고 분리된 머리가 열린 목 옆에 있다.
- 혼동: 장난감 사슴·살아 있는 동물 절단
- 입증 한계: 이는 기물의 분리 구조다. 원 유물의 정확한 복제·연회 규칙·주행은 주장하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: C03-R1, C03-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## C04 종탑 인형의 망치

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, scale_relation
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)
- 소유자: figure: bell-striking figure; hammer: its hammer; bell: tower bell; ledge: tower ledge
- 관계: figure → stands_on → ledge; hammer → held_by → figure; hammer → beside → bell
- EN: A bell-striking figure stands on a tower ledge holding a hammer beside the tower bell.
- KO: 종 치는 인형이 탑 돌출턱에 서서 탑의 종 옆에 망치를 들고 있다.
- 혼동: 사람 종지기·스스로 판단하는 수호자
- 입증 한계: 실제 타종 시각·도시 지배·인격은 외형으로 판정하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: C04-R1, C04-R2, C04-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## C05 기계 하인의 솔과 표면

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: relational_action, contact_point
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: servant: articulated mechanical servant; brush: small brush; counter: shop counter
- 관계: servant → grips → brush; brush → touches → counter
- EN: An articulated mechanical servant grips a small brush against a shop counter.
- KO: 관절 기계 하인이 작은 솔을 잡고 가게 계산대 표면에 대고 있다.
- 혼동: 일하는 자세=노예 신분·무한 노동
- 입증 한계: 보이는 청소 접촉과 노동 제도·권리·자발성은 별개다. 기존 후보 재사용부터 검토한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: C05-R1, C05-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## C06 기계 새 패밀리어

- 우선순위/가시성: P1 / still_structure
- 제안 역할: subject, object_structure
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)
- 소유자: bird: mechanical bird; wing: jointed wing; perch: perch; link: exposed wing link
- 관계: wing → part_of → bird; link → connected_to → wing; bird → on → perch
- EN: A mechanical bird rests on a perch with one jointed wing raised and its connecting link exposed.
- KO: 기계 새가 횃대에 앉아 관절 날개 하나를 들고 연결 링크를 드러낸다.
- 혼동: 실제 새·깃털 로봇=정찰 사역마
- 입증 한계: 마법 계약·감시·영상 기록·비행 능력은 별도 요청 맥락으로 남는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: C06-R1, C06-R2, C06-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## C07 기계 두뇌·호문쿨루스

- 우선순위/가시성: P1 / context_only
- 제안 역할: world, surreal_concept
- 출처: [S05](https://blog.sciencemuseum.org.uk/introducing-the-draughtsman-writer-automaton/), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: automaton: declared fictional automaton; program: declared control program
- 관계: program → declared_to_govern → automaton
- EN: A fictional premise may assign a clockwork mind to an automaton; no still arrangement establishes consciousness or an alchemical origin.
- KO: 허구 설정에서 자동인형에 기계 두뇌를 부여할 수 있으나 정지 배치로 의식이나 연금술 기원을 입증하지 않는다.
- 혼동: 캠 기억=사람의 기억·영혼·호문쿨루스
- 입증 한계: 동작 저장·계산·자아·주술적 생명은 서로 다른 선언이다. 긍정 시각 후보로 수출하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: C07-R1 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## D01 천문시계의 다중 다이얼

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, visible_text
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion), [S07](https://catalogue.museogalileo.it/section/AstronomicalInstruments.html)
- 소유자: clock: astronomical clock; time: time dial; calendar: calendar dial; moon: moon aperture
- 관계: time → part_of → clock; calendar → part_of → clock; moon → part_of → clock
- EN: An astronomical clock face carries a time dial, a separate calendar dial and a small moon-phase aperture.
- KO: 천문시계 전면에 시각 다이얼과 별도 달력 다이얼, 작은 달 위상 창이 놓인다.
- 혼동: 원형 장식=천체 계산 정확도
- 입증 한계: 동일 장치의 다이얼 구조를 보존한다. 천체 예측 성공·정확한 날짜는 별도다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: D01-R1, D01-R2, D01-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## D02 평면 아스트롤라베

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure, prop
- 출처: [S07](https://catalogue.museogalileo.it/section/AstronomicalInstruments.html), [S09](https://catalogue.museogalileo.it/object/PlaneAstrolabe.html)
- 소유자: disk: flat astrolabe body; rete: openwork rete; rule: rotating rule; ring: suspension ring
- 관계: rete → overlays → disk; rule → crosses → disk; ring → attached_to → disk
- EN: A flat astrolabe body carries an openwork rete and a rule crossing its face, with a suspension ring above.
- KO: 평평한 아스트롤라베 몸체 위에 투각 레테와 가로지르는 자가 놓이고 위에는 현수 고리가 달린다.
- 혼동: 구형 고리·태엽 포켓워치
- 입증 한계: 장치의 일반 구조를 설명한다. 모든 아스트롤라베가 같은 판·위도·시대인 것은 아니다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: D02-R1, D02-R2, D02-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## D03 환구의의 중심과 고리

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure
- 출처: [S07](https://catalogue.museogalileo.it/section/AstronomicalInstruments.html), [S08](https://catalogue.museogalileo.it/object/ArmillarySphere_n02.html)
- 소유자: globe: central Earth globe; rings: celestial coordinate rings; axis: tilted polar axis; stand: stand
- 관계: rings → surround → globe; axis → passes_through → globe; rings → supported_by → stand
- EN: Graduated celestial rings surround an Earth globe crossed by a tilted polar axis above a stand.
- KO: 눈금 있는 천구 고리들이 기울어진 극축이 지나는 지구 모형을 둘러싸며 받침이 지지한다.
- 혼동: 행성 공전팔·일반 구형 장식
- 입증 한계: 혼천의형 관측/천구 기구와 오러리를 구별한다. 동아시아 기구의 정본 구조를 서양 물건으로 대체하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: D03-R1, D03-R2, D03-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## D04 오러리의 행성 팔

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure, scale_relation
- 출처: [S10](https://www.rmg.co.uk/collections/objects/rmgc-object-11220)
- 소유자: sun: central Sun sphere; planets: planet spheres; arms: separate support arms; drum: gear drum
- 관계: arms → carry → planets; arms → around → sun; arms → above → drum
- EN: Separate arms carry planet spheres at different distances around a central Sun sphere above a gear drum.
- KO: 기어 드럼 위에서 별도 팔들이 중심 태양 구체 둘레의 서로 다른 거리에 행성 구체를 지지한다.
- 혼동: 환구의·천구 고리·장식 모빌
- 입증 한계: 기계적 공전 모형 구조와 실제 천체 인과를 구별한다. 후보 한영 번역의 핵심 수정 대상이다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: D04-R1, D04-R2, D04-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## D05 항해 시계와 관측 기록

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: prop, prop_placement
- 출처: [S11](https://www.rmg.co.uk/stories/time/harrisons-clocks-longitude-problem)
- 소유자: clock: marine timekeeper; box: wooden box; log: observation log; chart: nautical chart
- 관계: clock → inside → box; log → beside → box; chart → under → log
- EN: A marine timekeeper rests in an open wooden box beside an observation log on a nautical chart.
- KO: 열린 나무 상자 안의 항해 시계 옆에 관측 기록이 놓이고 그 아래 항해도가 펼쳐져 있다.
- 혼동: 바다 배경=경도 해결·위도 측정
- 입증 한계: 기록·시계·지도가 보여도 정확도와 경도 계산의 성공은 검증되지 않는다. 특정 H1/H4 디자인은 복제하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: D05-R1, D05-R2, D05-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## D06 황도대·달 위상 표시

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, visible_text
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S07](https://catalogue.museogalileo.it/section/AstronomicalInstruments.html), [S10](https://www.rmg.co.uk/collections/objects/rmgc-object-11220)
- 소유자: dial: zodiac dial; aperture: moon aperture; disk: half-lit Moon disk
- 관계: aperture → within → dial; disk → visible_through → aperture
- EN: A moon disk with a lit and dark portion is visible through an aperture within a zodiac-marked dial.
- KO: 황도대 표시 다이얼 안의 창으로 밝고 어두운 부분을 가진 달 원판이 보인다.
- 혼동: 점성 기호=주술 작동·실제 달 위상
- 입증 한계: 도상·표시 기능·종교 의례·천체력 표의 계산 정확도를 분리한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: D06-R1, D06-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## E01 선반의 절삭 접촉

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: object_structure, contact_point
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion), [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide)
- 소유자: blank: wooden blank; lathe: lathe centers; tool: cutting tool; rest: tool rest
- 관계: blank → between → lathe; tool → supported_by → rest; tool → touches → blank
- EN: A wooden blank is held between lathe centers while a cutting tool rests on a support and touches its surface.
- KO: 나무 공작물이 선반 양 센터 사이에 잡히고 받침 위 절삭 공구가 표면에 닿는다.
- 혼동: 완성 부품=제작 과정 증명
- 입증 한계: 회전·정확한 치수·공차 달성은 별도다. 특정 역사 선반의 작동 복제로 주장하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: E01-R1, E01-R2, E01-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## E02 기어 절삭과 미완성 이

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: object_structure, contact_point
- 출처: [S12](https://museoleonardiano.it/en/opera/rack-and-pinion/), [S14](https://khkgears.net/gear-knowledge/gear-technical-reference/calculation-gear-dimensions/)
- 소유자: blank: gear blank; cutter: tooth cutter; vice: holding fixture
- 관계: blank → held_by → vice; cutter → touches → blank
- EN: A clamped gear blank has several finished teeth beside an uncut arc, with a tooth cutter touching that arc.
- KO: 고정구에 잡힌 기어 공작물의 완성 이 몇 개 옆에 미절삭 원호가 있고 절삭 공구가 그 부분에 닿는다.
- 혼동: 기어 장식·역사적 대량생산 단정
- 입증 한계: 구체 가공법·공차·공작기계 연대는 추가 기술 원전 검토가 필요하다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: True
- 관계 gate: E02-R1, E02-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## E03 황동·청색 강철의 부품별 색

- 우선순위/가시성: P1 / still_structure
- 제안 역할: surface_material, color
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches)
- 소유자: plate: brass plate; screw: blued-steel screw; hand: blued-steel hand
- 관계: screw → set_in → plate; hand → above → plate
- EN: A blue steel screw is set into a warm brass plate, with a separate blue steel hand above it.
- KO: 따뜻한 황동 판에 청색 강철 나사가 박혀 있고 그 위에 별도 청색 강철 바늘이 놓인다.
- 혼동: 금색=금·청동=황동·푸른빛=열처리 증명
- 입증 한계: 요청에서 지정한 재료를 시각화한다. 합금 조성·가공법·물성은 픽셀에서 확정하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: E03-R1, E03-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## E04 기요셰와 필리그리

- 우선순위/가시성: P1 / still_structure
- 제안 역할: surface_pattern, object_structure
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide)
- 소유자: disk: engraved metal disk; grooves: repeated cut grooves; border: fine-wire filigree border
- 관계: grooves → cut_into → disk; border → surrounds → disk
- EN: Repeated curved grooves are cut into a solid metal disk, while a distinct fine-wire openwork border surrounds its edge.
- KO: 반복 곡선 홈이 단단한 금속 원판에 새겨지고 가장자리 둘레에는 별도 가는 금속선 투각 테두리가 있다.
- 혼동: 기계식 각인=금속선 세공=도금
- 입증 한계: 두 기법의 표면/선 구조를 분리한다. 실제 엔진 터닝·산부식 가공 이력은 별도다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: E04-R1, E04-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## E05 공차 비교·윤활·수리

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: relational_action, prop_state
- 출처: [S05](https://blog.sciencemuseum.org.uk/introducing-the-draughtsman-writer-automaton/), [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion), [S45](https://www.qtcgears.com/tools/catalogs/PDF_Q420/Tech.pdf)
- 소유자: old: worn cam plate; new: replacement cam plate; gauge: measuring gauge; tip: oiler tip; pivot: exposed pivot
- 관계: old → beside → new; gauge → contacts → new; tip → touches → pivot
- EN: A worn cam plate lies beside a replacement plate; a measuring gauge contacts the replacement while an oiler tip touches a separate exposed pivot.
- KO: 마모된 캠판과 대체 캠판이 나란히 놓이고 게이지가 대체판에 닿으며 주유기 끝은 별도 노출 피벗에 닿는다.
- 혼동: 기름때=윤활 성공·오차 감소·금속 피로
- 입증 한계: 복수 접촉이 경쟁하면 두 완전 대안으로 분리한다. 물성·반복 피로·동작 검증은 한 장면으로 통과하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: E05-R1, E05-R2, E05-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## E06 도안·제작물·후대 모형

- 우선순위/가시성: P1 / still_structure
- 제안 역할: prop, prop_placement
- 출처: [S12](https://museoleonardiano.it/en/opera/rack-and-pinion/), [S13](https://museoleonardiano.it/en/opera/the-self-moving-carriage-2010/), [S41](https://www2.museogalileo.it/en/library-and-research-institute/projects/temporary-exhibitions/1802-leonardo-da-vinci-and-perpetual-motion.html)
- 소유자: codex: open design codex; drawing: machine drawing; model: wooden interpretation model
- 관계: drawing → on → codex; model → beside → codex
- EN: An open codex displays a machine drawing beside a separate wooden interpretation model.
- KO: 열린 코덱스에 기계 도안이 있고 옆에는 별도 나무 해석 모형이 놓인다.
- 혼동: 도안 존재=역사상 제작·작동 성공
- 입증 한계: 도안 연대·모형 제작 연대·해석자·실험 결과를 별도 provenance 필드로 둔다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: E06-R1, E06-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## F01 시계탑 내부의 접근 동선

- 우선순위/가시성: P1 / still_structure
- 제안 역할: environment_detail, space_condition
- 출처: [S02](https://catalogue.museogalileo.it/object/ModelPendulumClock.html), [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)
- 소유자: frame: tower clock frame; shaft: weight shaft; walkway: maintenance walkway; rail: walkway rail
- 관계: walkway → beside → frame; rail → edges → walkway; shaft → below → frame
- EN: A maintenance walkway with a railing runs beside the tower clock frame above a deep weight shaft.
- KO: 난간 있는 정비 통로가 깊은 무게추 수직 공간 위의 탑 시계 프레임 옆을 지난다.
- 혼동: 기어가 붙은 벽=공공 시간 권력
- 입증 한계: 통로·하중 공간의 크기는 저술한 선택이다. 시보 통제·건축 안전은 입증하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: F01-R1, F01-R2, F01-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## F02 가동 방과 벽 뒤 통로

- 우선순위/가시성: P1 / still_structure
- 제안 역할: environment_detail, object_structure
- 출처: [S16](https://www.vam.ac.uk/articles/performance-and-the-baroque), [S37](https://bethesda.net/en-US/news/dishonored-2-inside-the-epic-themed-missions)
- 소유자: panel: moving room panel; rail: floor rail; passage: service passage; room: decorated room
- 관계: panel → on → rail; panel → reveals → passage; passage → behind → room
- EN: A decorated room panel stands partway along a floor rail, exposing a service passage behind the room.
- KO: 장식된 방의 패널이 바닥 레일 중간에 놓여 방 뒤 정비 통로가 드러난다.
- 혼동: 문이 열림=방 전체 재배치·순간이동
- 입증 한계: 정지 상태의 배치만 보여 준다. 방 변환 전후와 작품 정본 기구는 별도 검증한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: F02-R1, F02-R2, F02-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## F03 태엽 충전소의 작업 관계

- 우선순위/가시성: P0 / still_proxy
- 제안 역할: relational_action, environment_detail
- 출처: [S13](https://museoleonardiano.it/en/opera/the-self-moving-carriage-2010/), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: worker: adult winding worker; crank: winding crank; socket: automaton winding socket; automaton: declared automaton
- 관계: worker → grips → crank; crank → engages → socket; socket → part_of → automaton
- EN: An adult winding worker grips a crank engaged in the automaton's exposed winding socket at a service bench.
- KO: 성인 태엽 작업자가 정비대에서 자동인형의 노출 감기 소켓에 맞물린 크랭크를 잡고 있다.
- 혼동: 열쇠 장식=충전·복종
- 입증 한계: 동력 전달 성공·노동 신분·소유권은 맥락이다. 팔과 크랭크의 공간·접촉을 한 장면에서 검토한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: F03-R1, F03-R2, F03-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## F04 팔라초·로지아와 기계 운반

- 우선순위/가시성: P1 / still_structure
- 제안 역할: environment_detail, prop_placement
- 출처: [S16](https://www.vam.ac.uk/articles/performance-and-the-baroque), [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide), [S40](https://www.ubisoft.com/en-gb/games/assassins-creed-ii)
- 소유자: arcade: open arcade; courtyard: courtyard; cart: parts cart; arches: arches
- 관계: arcade → opens_onto → courtyard; arches → border → arcade; cart → within → arcade
- EN: A parts cart stands in an open arched arcade overlooking a courtyard.
- KO: 부품 수레가 안뜰을 향해 열린 아치 회랑 안에 서 있다.
- 혼동: 아치=특정 도시국가·계급 증명
- 입증 한계: 일반 공간 제안이며 특정 팔라초 고증은 아니다. 로지아의 개방 구조를 장식 벽화와 구별한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: F04-R1, F04-R2, F04-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## F05 분더카머의 분리 진열

- 우선순위/가시성: P1 / still_structure
- 제안 역할: environment_detail, prop_placement
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion), [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide)
- 소유자: cabinet: collector cabinet; instrument: astronomical instrument; specimen: natural specimen; drawers: specimen drawers
- 관계: instrument → within → cabinet; specimen → within → cabinet; drawers → below → instrument
- EN: An astronomical instrument and a natural specimen occupy separate compartments of a collector cabinet above shallow drawers.
- KO: 수집장 안의 별도 칸에 천문기구와 자연 표본이 놓이고 아래에는 얕은 서랍이 있다.
- 혼동: 모든 물건=마법·식민 출처·정본 수집품
- 입증 한계: 수집 배치·후원·공예 맥락과 각 물건의 원산지·권리·수탈 이력은 분리한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: F05-R1, F05-R2, F05-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## F06 무대 윙과 윈치

- 우선순위/가시성: P1 / still_structure
- 제안 역할: environment_detail, object_structure
- 출처: [S16](https://www.vam.ac.uk/articles/performance-and-the-baroque)
- 소유자: wing: painted stage wing; track: stage track; rope: haul rope; winch: backstage winch
- 관계: wing → on → track; rope → connects → wing; rope → runs_to → winch
- EN: A painted stage wing sits on a track, with a haul rope running behind it to a backstage winch.
- KO: 그려진 무대 윙이 레일 위에 놓이고 당김줄이 뒤로 이어져 무대 뒤 윈치에 연결된다.
- 혼동: 환영=건물 실제 변환·소리
- 입증 한계: 무대 전환 속도·효과음·궁정 권력은 픽셀 구조와 별개다. 그로토 수력은 다른 대안이다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: F06-R1, F06-R2, F06-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## F07 자주 수레와 트레드휠

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, scale_relation
- 출처: [S13](https://museoleonardiano.it/en/opera/the-self-moving-carriage-2010/), [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide)
- 소유자: cart: wooden cart; drums: two spring drums; wheels: drive wheels; frame: cart frame
- 관계: drums → beneath → frame; wheels → attached_to → frame; frame → part_of → cart
- EN: Two spring drums sit beneath a wooden cart frame between its driving wheels.
- KO: 구동 바퀴 사이의 나무 수레 프레임 아래 태엽통 두 개가 놓인다.
- 혼동: 트레드휠 인력=태엽 동력
- 입증 한계: 이 카드는 수레 대안이다. 인력이 들어가는 트레드휠 크레인은 별도 소유자·동력 입력을 저술해야 한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: F07-R1, F07-R2, F07-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## F08 비행 도안·기계 보행의 한계

- 우선순위/가시성: P1 / context_only
- 제안 역할: world, surreal_physics_detail
- 출처: [S13](https://museoleonardiano.it/en/opera/the-self-moving-carriage-2010/), [S41](https://www2.museogalileo.it/en/library-and-research-institute/projects/temporary-exhibitions/1802-leonardo-da-vinci-and-perpetual-motion.html)
- 소유자: design: declared flight or walking design; prototype: declared prototype
- 관계: prototype → interprets → design
- EN: Aerial screws, flapping wings and mechanical walkers can be designed as fictional machines; a drawing or posed model alone does not establish successful flight or walking.
- KO: 공중 나사·날갯짓·기계 보행체를 허구 장치로 설계할 수 있으나 도안이나 세운 모형만으로 비행·보행 성공을 입증하지 않는다.
- 혼동: 다빈치 도안=검증된 헬리콥터·영구기관
- 입증 한계: 동력·하중·운동의 기술 원전 추가 조사가 필요하다. 장치별 양성 대안으로 분해하기 전 보류한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: F08-R1 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## G01 러프·더블릿의 분리 부품

- 우선순위/가시성: P1 / still_structure
- 제안 역할: garment_detail, wardrobe_layering
- 출처: [S17](https://fashionhistory.fitnyc.edu/1580-1589/)
- 소유자: wearer: adult wearer; ruff: pleated ruff; doublet: fitted doublet; sleeve: slashed sleeve; lining: contrasting lining
- 관계: ruff → encircles_neck_of → wearer; doublet → worn_by → wearer; lining → visible_through → sleeve; sleeve → part_of → doublet
- EN: A pleated ruff encircles an adult wearer's neck above a fitted doublet; contrasting lining shows through cuts in one sleeve.
- KO: 성인 착용자의 목을 주름 러프가 감싸고 아래에는 몸에 맞는 더블릿이 있으며 한 소매의 절개 사이로 대비색 안감이 보인다.
- 혼동: 레이스 칼라·찢어진 상처·빅토리아 복식
- 입증 한계: 시대·지역·계급은 요청 맥락이다. 복식의 이음·안감·절개 소유자를 별도 기록한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: G01-R1, G01-R2, G01-R3, G01-R4 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## G02 스테이즈와 현대 코르셋

- 우선순위/가시성: P1 / still_structure
- 제안 역할: garment_detail, wardrobe_layering
- 출처: [S17](https://fashionhistory.fitnyc.edu/1580-1589/), [S23](https://www.metmuseum.org/art/collection/search/356244), [S44](https://heritage.southwark.gov.uk/objects/11787/stays)
- 소유자: stays: structured stays; boning: boning channels; lacing: back lacing; wearer: adult wearer
- 관계: boning → part_of → stays; lacing → closes → stays; stays → worn_by → wearer
- EN: An adult wearer has structured stays with visible boning channels and separate back lacing over an underlayer.
- KO: 성인 착용자가 속옷층 위에 보닝 채널과 별도 등 끈 여밈이 보이는 스테이즈를 입고 있다.
- 혼동: 모든 코르셋=르네상스·성적 구속
- 입증 한계: 특정 연대의 패턴은 추가 복식 원전 검토가 필요하다. 지지 구조가 동의·성적 맥락을 자동 활성화하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: True
- 관계 gate: G02-R1, G02-R2, G02-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## G03 바로크·로코코·장식의 분리

- 우선순위/가시성: P1 / still_structure
- 제안 역할: surface_pattern, environment_detail
- 출처: [S16](https://www.vam.ac.uk/articles/performance-and-the-baroque), [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide)
- 소유자: panel: ornament panel; scroll: curved scroll; strap: interlaced strapwork; cartouche: asymmetric cartouche
- 관계: scroll → on → panel; strap → on → panel; cartouche → on → panel
- EN: A display panel places a scrolling relief, interlaced strapwork and an asymmetric shell-like cartouche in separate labeled sections.
- KO: 전시 패널의 서로 구분된 칸에 곡선 부조, 얽힌 스트랩워크, 비대칭 조개형 카르투슈가 놓인다.
- 혼동: 로코코=르네상스·그로테스크=괴물
- 입증 한계: 비교 전시 실현이다. 장식 하나로 양식·연대를 확정하지 않는다. 한 후보에 양식 필수 속성을 합치지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: G03-R1, G03-R2, G03-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## G04 소재 마감과 스켈레톤 외장

- 우선순위/가시성: P1 / still_structure
- 제안 역할: surface_material, object_structure
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion)
- 소유자: plate: pierced metal plate; opening: plate opening; gear: internal gear; edge: engraved gilded edge
- 관계: opening → within → plate; gear → visible_through → opening; edge → borders → opening
- EN: An internal gear is visible through a cut opening in a metal plate bordered by an engraved gilded edge.
- KO: 새김과 금도금 테두리가 있는 금속판의 절개 창으로 내부 기어가 보인다.
- 혼동: 투각 장식=실제 구동·파티나=오래됨
- 입증 한계: 외장 개방·표면 마감·기계 기능을 분리한다. 에나멜·브로케이드·벨벳도 각각 별도 물성/표면 대안으로 남는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: G04-R1, G04-R2, G04-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## G05 가면과 플랫폼 신발

- 우선순위/가시성: P1 / still_structure
- 제안 역할: wearable_accessory, footwear
- 출처: [S23](https://www.metmuseum.org/art/collection/search/356244)
- 소유자: wearer: adult wearer; mask: face mask; shoe: platform chopine; sole: raised sole
- 관계: mask → worn_by → wearer; shoe → worn_by → wearer; sole → part_of → shoe
- EN: An adult wearer holds a face mask beside their cheek while one platform chopine and its raised sole remain visible below the hem.
- KO: 성인 착용자가 뺨 옆에 가면을 들고 옷단 아래로 쇼핀 한 짝과 높은 밑창이 보인다.
- 혼동: 가면=쿠르티잔·쇼핀=성매매 신분
- 입증 한계: 직업·욕망·권리·동의는 외형으로 추정하지 않는다. 가면무도회와 궁정 마스크 공연도 다른 맥락이다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: G05-R1, G05-R2, G05-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## G06 음향·그로토·공압

- 우선순위/가시성: P1 / context_only
- 제안 역할: sensory_cue, world
- 출처: [S06](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/art-in-motion), [S16](https://www.vam.ac.uk/articles/performance-and-the-baroque), [S27](https://www.metmuseum.org/art/collection/search/451302)
- 소유자: source: declared acoustic or pneumatic source; output: declared sound or air-driven action
- 관계: source → declared_to_produce → output
- EN: Ticking, friction, harpsichord notes and pneumatic effects remain declared sensory or mechanism context unless their distinct physical sources are specified.
- KO: 똑딱임·마찰음·하프시코드 음·공압 효과는 서로 다른 물리 음원과 동력원이 지정되기 전에는 감각·기구 맥락으로 유지한다.
- 혼동: 증기처럼 보이는 안개=증기 동력·파이프=공압
- 입증 한계: 음향은 사진에서 직접 입증하지 않는다. 수력·공압·태엽을 동의어로 묶지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: G06-R1 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## H01 길드 자격작과 심사

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: relational_action, social_cue
- 출처: [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide)
- 소유자: artisan: adult artisan; work: mechanical submission; panel: inspection panel; tool: measuring tool
- 관계: artisan → presents → work; panel → examines → work; tool → beside → work
- EN: An adult artisan presents a mechanical piece across an inspection table while a panel examines it beside measuring tools.
- KO: 성인 장인이 검사 탁자 너머로 기계 작품을 내밀고 심사자들이 측정 도구 옆에서 그것을 살핀다.
- 혼동: 작품의 정교함=길드 자격·천재성
- 입증 한계: 도제/직인/마스터 지위·합격·궁정 후원은 별도 선언이다. 인물 수를 후보 때문에 강제하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: H01-R1, H01-R2, H01-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## H02 열쇠 보관·수리 접근

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: relational_action, prop_state
- 출처: [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: keeper: adult key keeper; key: winding key; cabinet: locked parts cabinet; worker: repair worker
- 관계: keeper → holds → key; worker → beside → cabinet
- EN: An adult keeper holds a winding key beside a closed parts cabinet while a repair worker waits across the bench.
- KO: 성인 보관자가 닫힌 부품장 옆에서 감기 열쇠를 들고 있고 수리 작업자가 정비대 건너편에 기다린다.
- 혼동: 열쇠를 쥠=합법 소유·독점·예속
- 입증 한계: 소유·수리 자격·지식 독점은 세계 설정이다. 장면은 접근 비대칭의 단서만 준다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: H02-R1, H02-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## H03 태엽 노동의 몸과 작업점

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: relational_action, contact_point
- 출처: [S13](https://museoleonardiano.it/en/opera/the-self-moving-carriage-2010/), [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide)
- 소유자: worker: adult worker; crank: large crank; drum: winding drum; platform: worker platform
- 관계: worker → grips → crank; crank → mounted_on → drum; worker → supported_by → platform
- EN: An adult worker stands on a platform and grips both handles of a large crank mounted on a winding drum.
- KO: 성인 작업자가 발판에 서서 감기 드럼에 달린 큰 크랭크의 두 손잡이를 잡는다.
- 혼동: 노동 자세=착취·자발성·생산량
- 입증 한계: 팔 reach·하중 지지·손잡이 회전 공간은 구현 시 검토한다. 계급·동력 고갈·시간 규율은 별도다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: H03-R1, H03-R2, H03-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## H04 예속·사치법·식민 수탈

- 우선순위/가시성: P1 / context_only
- 제안 역할: world, declared_person_background
- 출처: [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: institution: declared institution; person: declared person or machine; resource: declared resource
- 관계: institution → declared_to_control → person; institution → declared_to_control → resource
- EN: Servitude, sumptuary law, patronage and colonial extraction are distinct institutional claims that require declared context or historical evidence.
- KO: 예속·사치법·후원·식민 수탈은 각각 선언 맥락이나 역사 자료가 필요한 별도 제도 주장이다.
- 혼동: 황동 피부=노예·비싼 옷=귀족·광산=식민지
- 입증 한계: 민족·인종·성별·외관에서 신분·노동 조건을 추론하지 않는다. 제도별 출처를 보강해 분리 등록한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: H04-R1, H04-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## I01 철제 의수의 접합 경계

- 우선순위/가시성: P0 / still_structure
- 제안 역할: object_structure, anatomical_connection
- 출처: [S19](https://www.britishmuseum.org/collection/object/H_1870-1013-38), [S20](https://collection.sciencemuseumgroup.org.uk/objects/co126769/artificial-hand-and-forearm-1601-1700)
- 소유자: wearer: adult prosthesis wearer; socket: forearm socket; hand: articulated metal hand; catch: wrist catch
- 관계: socket → fitted_to → wearer; hand → attached_to → socket; catch → part_of → socket
- EN: An adult prosthesis wearer's forearm socket supports an articulated metal hand, with a separate catch at the wrist.
- KO: 성인 의수 사용자의 전완 소켓이 관절 금속 손을 지지하고 손목에는 별도 걸쇠가 보인다.
- 혼동: 갑옷 장갑·신경 연결·악당 신체
- 입증 한계: 실제 몸/의지의 소유 경계와 연결을 따로 검토한다. 장애를 공포·비인간성의 자동 표식으로 쓰지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: I01-R1, I01-R2, I01-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## I02 외골격의 몸 밖 하중 경로

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, body_orientation
- 출처: [S19](https://www.britishmuseum.org/collection/object/H_1870-1013-38), [S38](https://blog.playstation.com/2022/09/01/steelrising-combat-system-breakdown/)
- 소유자: wearer: adult wearer; frame: external support frame; cuff: forearm cuff; brace: torso brace
- 관계: cuff → connected_to → frame; frame → connected_to → brace; brace → worn_by → wearer
- EN: An external support frame joins a forearm cuff to a torso brace outside an adult wearer's clothing.
- KO: 성인 착용자의 옷 바깥에서 외부 지지 프레임이 전완 커프와 몸통 지지대를 연결한다.
- 혼동: 외골격=신체 내부 의지·초인적 힘
- 입증 한계: 허구적 확장이다. 동력·신경 연결·하중 안전·효능은 입증하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: I02-R1, I02-R2, I02-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## I03 밀랍 비너스의 분리 층

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, prop_state
- 출처: [S21](https://www.sma.unifi.it/index.php?func=viewpage&module=CMpro&newlang=eng&pageid=631)
- 소유자: model: wax anatomical model; cover: removable torso cover; layers: modeled internal layers; tray: display tray
- 관계: cover → beside → model; layers → inside → model; model → on → tray
- EN: A wax anatomical model lies on a display tray with its removable torso cover beside it and modeled internal layers exposed.
- KO: 밀랍 해부 모형이 전시 받침 위에 누워 있고 분리된 몸통 덮개가 옆에 놓여 내부 모형 층이 드러난다.
- 혼동: 밀랍 모형=실제 사체·살아 있는 해부
- 입증 한계: 표현된 해부와 실제 생체 조직을 분리한다. 후기 18세기 전통을 르네상스 일반 기술로 자동 합치지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: I03-R1, I03-R2, I03-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## I04 생체·기계 연결의 선택적 경계

- 우선순위/가시성: P0 / still_structure
- 제안 역할: anatomical_connection, object_structure
- 출처: [S19](https://www.britishmuseum.org/collection/object/H_1870-1013-38), [S21](https://www.sma.unifi.it/index.php?func=viewpage&module=CMpro&newlang=eng&pageid=631), [S38](https://blog.playstation.com/2022/09/01/steelrising-combat-system-breakdown/)
- 소유자: body: declared fictional adult body; rim: body opening rim; coupling: mechanical coupling; housing: metal housing
- 관계: coupling → crosses → rim; coupling → connected_to → housing; rim → part_of → body
- EN: In a declared fictional adult body, a mechanical coupling crosses the edge of an opened panel and connects to an internal metal housing.
- KO: 선언된 허구 성인 신체의 열린 패널 가장자리를 기계 커플링이 가로질러 내부 금속 하우징에 연결된다.
- 혼동: 몸 앞 기어=이식·피부 위 금속=조직 연속
- 입증 한계: 유기 조직/모형/자동인형 외장 중 어떤 몸인지 먼저 선언한다. 생존·통증·개조 원인은 별도다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: I04-R1, I04-R2, I04-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## I05 강제 기계화·생체해부·교체 정체성

- 우선순위/가시성: P1 / context_only
- 제안 역할: world, narrative_core
- 출처: [S19](https://www.britishmuseum.org/collection/object/H_1870-1013-38), [S21](https://www.sma.unifi.it/index.php?func=viewpage&module=CMpro&newlang=eng&pageid=631), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: person: declared adult person; procedure: declared procedure; parts: declared replacement parts
- 관계: procedure → declared_to_affect → person; parts → declared_to_replace_parts_of → person
- EN: Forced mechanization, vivisection and total replacement are distinct narrative or temporal claims; an opened body does not by itself establish them.
- KO: 강제 기계화·생체해부·전부품 교체는 서로 다른 서사·시간 주장이다. 열린 몸만으로 이를 입증할 수 없다.
- 혼동: 열린 신체=강압·살아 있음·모든 부품 교체
- 입증 한계: 폭력·신체 개조 연구를 유지한다. 실제 손상 정도·자발성·연속성은 요청과 자료에 맞춰 별도 저술한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: I05-R1, I05-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## J01 숨은 에로틱 시계의 표현 층

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, prop_state
- 출처: [S22](https://www.britishmuseum.org/collection/object/H_OA-10757)
- 소유자: watch: historical watch; lid: raised inner cover; miniature: adult intimate miniature representation
- 관계: lid → part_of → watch; miniature → beneath → lid
- EN: A historical watch is displayed with its inner cover raised to reveal a miniature representation of an adult couple in an intimate pose.
- KO: 역사적 시계의 안쪽 덮개를 들어 성인 커플의 친밀한 자세를 표현한 작은 도상을 드러내 전시한다.
- 혼동: 시계 속 표현=장면 속 실제 성행위·항상 움직이는 장치
- 입증 한계: 유물 도상·가동 기구·실제 인물을 분리한다. 정확한 성행위 기하나 움직임은 이 출처 범위에서 재구성하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: J01-R1, J01-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## J02 플랩 판화의 겉면과 아래 그림

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, contact_point
- 출처: [S23](https://www.metmuseum.org/art/collection/search/356244)
- 소유자: print: paper print; flap: skirt-shaped flap; hand: viewer hand; underprint: depicted undergarments and shoes
- 관계: flap → attached_to → print; hand → lifts → flap; underprint → beneath → flap
- EN: A viewer lifts the skirt-shaped paper flap of a print, exposing the depicted undergarments and raised shoes beneath.
- KO: 관람자가 판화의 치마형 종이 플랩을 들어 아래에 그려진 속옷과 높은 신발을 드러낸다.
- 혼동: 실제 여성의 치마 들기·그냥 겹친 종이
- 입증 한계: 그림 속 인물·플랩·현실 관람자의 손을 서로 다른 소유자로 둔다. 실제 인물의 동의나 직업을 추정하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: J02-R1, J02-R2, J02-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## J03 성인 자동인형 동반자·인형화

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: relational_action, object_structure
- 출처: [S23](https://www.metmuseum.org/art/collection/search/356244), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: adult: declared adult person; automaton: adult-coded mechanical companion; hand: automaton hand; key: winding key
- 관계: hand → part_of → automaton; adult → holds → key; key → beside → automaton
- EN: A declared adult person holds a winding key beside an adult-coded mechanical companion whose hand has visible manufactured joints.
- KO: 선언된 성인이 제조된 관절이 보이는 손을 가진 성인형 기계 동반자 옆에서 감기 열쇠를 들고 있다.
- 혼동: 인형 관절=복종 욕망·연애·강제 인형화
- 입증 한계: 피그말리온·연인·욕망·변신·주문제작 성격은 선언 맥락이다. 특정 자세를 동의의 증거로 쓰지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: J03-R1, J03-R2, J03-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## J04 동의와 프로그램

- 우선순위/가시성: P0 / context_only
- 제안 역할: world, concept_tension
- 출처: [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: automaton: declared fictional adult automaton; program: control program; consent: declared consent state
- 관계: program → declared_to_control → automaton; consent → belongs_to → automaton
- EN: A programmed response and a declared consent state are separate claims; compliance, refusal gestures or a winding key alone do not settle either.
- KO: 프로그램된 반응과 선언된 동의 상태는 별개 주장이다. 복종·거부 몸짓이나 태엽 열쇠만으로 어느 것도 확정되지 않는다.
- 혼동: 복종=욕망·미소=동의·키 소유=정당한 통제
- 입증 한계: 상충 설정은 그대로 기록한다. 픽셀 PASS 항목이나 장르 기본 속성으로 수출하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: J04-R1, J04-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## J05 유곽·쿠르티잔·리베르틴

- 우선순위/가시성: P1 / context_only
- 제안 역할: situation_context, declared_person_background
- 출처: [S23](https://www.metmuseum.org/art/collection/search/356244), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: venue: declared adult venue; person: declared adult participant; role: declared social role
- 관계: person → declared_present_in → venue; role → declared_for → person
- EN: A brothel, courtesan role, libertine identity or boudoir setting requires its own declared social or architectural context.
- KO: 유곽·쿠르티잔 역할·리베르틴 정체·부두아르 배경에는 각각 선언된 사회·건축 맥락이 필요하다.
- 혼동: 여성 사적 방=성매매·노출 복식=직업
- 입증 한계: 성인 사회 연구를 누락하지 않되 외관에서 직업·성적 서비스·착취를 단정하지 않는다. 세부 역사 검토 전 양성 후보는 보류한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: J05-R1, J05-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## J06 정조대 유물과 위조 분류

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, prop
- 출처: [S24](https://www.britishmuseum.org/collection/object/H_M-574)
- 소유자: belt: metal belt artifact; lock: separate lock; case: museum case; label: provenance label
- 관계: lock → attached_to → belt; belt → inside → case; label → beside → belt
- EN: A metal belt artifact with a separate lock is displayed in a museum case beside a provenance label.
- KO: 별도 잠금장치가 달린 금속 벨트 유물이 박물관 진열장 안의 출처 설명 옆에 놓인다.
- 혼동: 유물 존재=중세에 널리 착용·모든 물건 위조
- 입증 한계: M.574의 위조 분류만 확인했다. 사용 시기·실제 착용·통제 제도를 장면 외형에서 확정하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: J06-R1, J06-R2, J06-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## J07 기계 페티시·본디지의 opt-in

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: wearable_accessory, contact_point
- 출처: [S23](https://www.metmuseum.org/art/collection/search/356244), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: wearer: declared adult wearer; harness: separate harness; ring: harness ring; key: separate winding key
- 관계: harness → worn_by → wearer; ring → part_of → harness; key → beside → ring
- EN: A declared adult wearer has a separate harness with a metal ring; a winding key lies beside the ring without joining the body.
- KO: 선언된 성인 착용자가 금속 고리가 달린 별도 하네스를 착용하고 감기 열쇠는 몸과 연결되지 않은 채 고리 옆에 놓인다.
- 혼동: 가죽·금속·정비=페티시·구속·신체 관통
- 입증 한계: 현대 창작 결합이며 역사 기본 복식이 아니다. 성적 해석은 명시 선택하고 하네스·신체·열쇠 소유자를 보존한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: J07-R1, J07-R2, J07-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## J08 관찰 구멍과 시선 경로

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: gaze_target, object_structure
- 출처: [S23](https://www.metmuseum.org/art/collection/search/356244), [S37](https://bethesda.net/en-US/news/dishonored-2-inside-the-epic-themed-missions)
- 소유자: observer: declared adult observer; peephole: wall aperture; room: private room; eye: observer eye
- 관계: eye → belongs_to → observer; eye → aligned_with → peephole; peephole → opens_into → room
- EN: An adult observer's eye aligns with a small wall aperture opening toward a private room.
- KO: 성인 관찰자의 눈이 사적인 방을 향해 열린 작은 벽 구멍과 같은 선상에 놓인다.
- 혼동: 관찰창=비동의 관음·보안 감시
- 입증 한계: 의도·비밀성·상대 동의는 보이지 않는다. 방 안 인물·신체·성행위를 자동 추가하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: J08-R1, J08-R2, J08-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## K01 레이피어와 망고슈의 분리

- 우선순위/가시성: P1 / still_structure
- 제안 역할: prop, prop_placement
- 출처: [S25](https://www.metmuseum.org/art/collection/search/22387), [S40](https://www.ubisoft.com/en-gb/games/assassins-creed-ii), [S43](https://www.metmuseum.org/art/collection/search/32166)
- 소유자: rapier: long slim sword; dagger: short parrying dagger; table: display table
- 관계: rapier → on → table; dagger → beside → rapier
- EN: A long slim sword with a complex hand guard lies on a display table beside a separate short parrying dagger.
- KO: 복잡한 손 보호대가 달린 길고 가는 검이 전시대 위의 별도 짧은 방어 단검 옆에 놓인다.
- 혼동: 모든 검=레이피어·소유자=암살자
- 입증 한계: 레이피어·방어 단검 병용의 역사 맥락을 S43으로 확인했다. 특정 물건의 도판·정확한 형식과 지역은 추가 검토한다. 소유자를 암살자로 단정하지 않는다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: K01-R1, K01-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## K02 휠록·플린트록의 점화 경계

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure
- 출처: [S25](https://www.metmuseum.org/art/collection/search/22387)
- 소유자: pistol: historic wheellock pistol; wheel: external lock wheel; barrel: barrel; stock: stock
- 관계: wheel → part_of → pistol; barrel → above → stock
- EN: A historic wheellock pistol is displayed with its external lock wheel visible beside the stock below the barrel.
- KO: 역사적 휠록 권총을 전시하여 총열 아래 개머리판 옆의 외부 점화 휠이 보인다.
- 혼동: 태엽 추진 탄환·부싯돌 락과 동일
- 입증 한계: 점화와 탄환 추진을 나눈다. 조립·제작·사용 절차를 제공하는 후보가 아니며 다른 화기는 별도 구조로 연구한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: K02-R1, K02-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## K03 기계 병사와 신체 부착 장비

- 우선순위/가시성: P1 / still_structure
- 제안 역할: object_structure, prop
- 출처: [S36](https://www.blackgate.com/2012/08/19/the-english-civil-war-with-clockwork-war-machines-an-intro-to-clockwork-chivalry/), [S38](https://blog.playstation.com/2022/09/01/steelrising-combat-system-breakdown/)
- 소유자: soldier: fictional mechanical soldier; arm: its articulated arm; mount: arm mount; shield: mounted shield
- 관계: arm → part_of → soldier; mount → attached_to → arm; shield → attached_to → mount
- EN: A fictional mechanical soldier has an articulated arm with a separate mount supporting a shield.
- KO: 허구 기계 병사의 관절 팔에 별도 장착부가 있고 그 장착부가 방패를 지지한다.
- 혼동: 장식 갑옷=자동 병사·장착=무적
- 입증 한계: 보유 장비·신체 부착·주행·전투 능력·명령 복종을 따로 기록한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: K03-R1, K03-R2, K03-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## K04 고문·자동 처형·암살 명령

- 우선순위/가시성: P1 / context_only
- 제안 역할: world, narrative_core
- 출처: [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/), [S36](https://www.blackgate.com/2012/08/19/the-english-civil-war-with-clockwork-war-machines-an-intro-to-clockwork-chivalry/), [S38](https://blog.playstation.com/2022/09/01/steelrising-combat-system-breakdown/)
- 소유자: institution: declared violent institution; device: declared machine; victim: declared victim
- 관계: institution → declared_to_command → device; device → declared_to_target → victim
- EN: Mechanized torture, automated execution and assassination orders are distinct violent settings whose actors, victims and responsibility must be declared separately.
- KO: 기계 고문·자동 처형·암살 명령은 행위자·피해자·책임을 따로 선언해야 하는 별도 폭력 설정이다.
- 혼동: 정밀 기계=고문 장치·위협 자세=실행 완료
- 입증 한계: 폭력 범주를 유지하되 보이지 않는 고통·과거 실행·책임 소재를 픽셀에서 확정하지 않는다. 구체 역사 장치의 추가 출처 필요.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: K04-R1, K04-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## K05 사보타주 흔적과 원인

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: aftermath_trace, narrative_clue
- 출처: [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide), [S36](https://www.blackgate.com/2012/08/19/the-english-civil-war-with-clockwork-war-machines-an-intro-to-clockwork-chivalry/), [S37](https://bethesda.net/en-US/news/dishonored-2-inside-the-epic-themed-missions)
- 소유자: train: exposed gear train; gap: missing coupling gap; piece: detached coupling; bench: service bench
- 관계: gap → within → train; piece → on → bench; bench → beside → train
- EN: A detached coupling rests on a service bench beside a visible gap in the exposed gear train.
- KO: 노출 기어열에 연결부가 빠진 틈이 보이고 옆 정비대에 분리된 커플링이 놓인다.
- 혼동: 분리 부품=고의 파괴·혁명·시간 교란
- 입증 한계: 정비·우발 고장·사보타주의 원인과 시보 교란 결과는 정지 장면으로 확정하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: K05-R1, K05-R2, K05-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## L01 자유의지·결정론·기계론

- 우선순위/가시성: P1 / context_only
- 제안 역할: world, concept_tension
- 출처: [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide), [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/)
- 소유자: agent: declared fictional agent; law: declared world rule
- 관계: law → declared_to_constrain → agent
- EN: Mechanism, determinism and free will are distinct philosophical claims about a fictional agent and world rule.
- KO: 기계론·결정론·자유의지는 허구 행위자와 세계 규칙에 관한 서로 다른 철학 주장이다.
- 혼동: 정해진 자세=결정론·거부 동작=자유의지 증명
- 입증 한계: 작품 설정·철학 해석·관찰 가능한 몸짓을 분리한다. 긍정 시각 후보로 수출하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: L01-R1 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## L02 테세우스·빙의·역병·영구기관

- 우선순위/가시성: P1 / context_only
- 제안 역할: world, narrative_core
- 출처: [S34](https://iantregillis.com/home-top-stub/writing/the-alchemy-wars/), [S35](https://us.macmillan.com/books/9781427204899/mainspring/), [S41](https://www2.museogalileo.it/en/library-and-research-institute/projects/temporary-exhibitions/1802-leonardo-da-vinci-and-perpetual-motion.html)
- 소유자: entity: declared entity; history: declared history; cause: declared supernatural or mechanical cause
- 관계: history → declared_for → entity; cause → declared_to_affect → entity
- EN: Identity after replacement, possession, a clockwork plague and perpetual motion require separate temporal or fictional premises.
- KO: 교체 뒤 정체성·빙의·태엽 역병·영구기관에는 각각 별도 시간·허구 전제가 필요하다.
- 혼동: 기어 노출=감염·멈춘 인형=죽음·그림=영구기관 성공
- 입증 한계: 현실 기술의 성공으로 설명하지 않는다. 이 카드는 보류 경계이며 실제 반영 시 네 개 이상의 맥락 레코드로 분할한다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: L02-R1, L02-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## L03 메멘토 모리·바니타스

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: prop_placement, narrative_clue
- 출처: [S01](https://www.metmuseum.org/essays/seventeenth-century-european-watches), [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide)
- 소유자: watch: open watch; skull: skull representation; flower: wilted flower; table: table
- 관계: watch → on → table; skull → beside → watch; flower → beside → watch
- EN: An open watch lies on a table beside a skull representation and a wilted flower.
- KO: 열린 시계가 해골 표현물과 시든 꽃 옆의 탁자 위에 놓인다.
- 혼동: 상징물=실제 죽음·멈춘 시간
- 입증 한계: 죽음 성찰·덧없음은 맥락 해석이다. 바늘 한 위치로 고장·멈춤을 확정하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: L03-R1, L03-R2, L03-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## L04 시계장치 우주와 사람 규모

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: surreal_concept, scale_relation
- 출처: [S18](https://www.metmuseum.org/ko/exhibitions/layered-narratives-the-northern-renaissance-gallery/visiting-guide), [S35](https://us.macmillan.com/books/9781427204899/mainspring/)
- 소유자: person: declared adult person; gear: colossal gear; walkway: narrow walkway; stars: star-like points
- 관계: person → on → walkway; walkway → beside → gear; stars → behind → gear
- EN: A declared adult person stands on a narrow walkway beside a colossal gear silhouetted against star-like points.
- KO: 선언된 성인이 별 같은 점들을 배경으로 한 거대 기어 옆의 좁은 통로에 서 있다.
- 혼동: 대형 오러리=실제 우주 구조·신의 부재
- 입증 한계: 허구적 규모 대비다. 우주 원인·존재 의미·코스믹 공포·종교적 사실은 사진에서 확정하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: L04-R1, L04-R2, L04-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## L05 불가사의한 인형의 정지 자세

- 우선순위/가시성: P1 / still_proxy
- 제안 역할: body_pose, object_structure
- 출처: [S05](https://blog.sciencemuseum.org.uk/introducing-the-draughtsman-writer-automaton/), [S31](https://www.getty.edu/news/new-book-tells-the-story-of-a-praying-renaissance-robot/)
- 소유자: figure: adult-coded automaton; face: fixed faceplate; arm: raised arm; joint: exposed elbow joint
- 관계: face → part_of → figure; arm → part_of → figure; joint → part_of → arm
- EN: An adult-coded automaton holds one arm raised beneath a fixed faceplate, with an exposed elbow joint.
- KO: 성인형 자동인형이 고정된 얼굴판 아래 한 팔을 들고 팔꿈치 관절을 드러낸다.
- 혼동: 고정 미소=사악함·지연·반복·빙의
- 입증 한계: 반복·정지 고장·동작 지연은 시간 증거가 필요하다. 표정만으로 감정·도덕·영혼을 단정하지 않는다.
- 원전 검토 범위: family_context_and_authored_proposal; 추가 기술 검토: False
- 관계 gate: L05-R1, L05-R2, L05-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## M01 안티키테라의 유물·복원 분리

- 우선순위/가시성: P1 / still_structure
- 제안 역할: prop_placement, object_structure
- 출처: [S26](https://www.ucl.ac.uk/news/2021/mar/experts-recreate-mechanical-cosmos-worlds-first-computer)
- 소유자: fragment: corroded gear fragment; model: separate reconstruction model; case: divided display case
- 관계: fragment → within → case; model → beside → fragment
- EN: A corroded gear fragment and a separate clean reconstruction model occupy distinct compartments of a display case.
- KO: 부식된 기어 파편과 별도 깨끗한 복원 모형이 전시장의 구분된 칸에 놓인다.
- 혼동: 복원 가설=온전한 고대 원형·태엽 지능
- 입증 한계: 수동 천문 계산·남은 파편·현대 가설·제작 검증을 구분한다. 유물 형상을 직접 복제한 것은 아니다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: M01-R1, M01-R2 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## M02 알자자리 수력과 도해

- 우선순위/가시성: P1 / still_structure
- 제안 역할: prop, object_structure
- 출처: [S27](https://www.metmuseum.org/art/collection/search/451302)
- 소유자: folio: illustrated folio; drawing: water-clock diagram; reservoir: depicted reservoir; bird: depicted peacock
- 관계: drawing → on → folio; reservoir → within → drawing; bird → within → drawing
- EN: An illustrated folio shows a water-clock diagram with a reservoir and peacock figures contained within the drawing.
- KO: 삽화 필사본 페이지에 물통과 공작 인형이 그림 안에 들어 있는 물시계 도해가 보인다.
- 혼동: 도해 속 수조=실제 현장 수조·모든 이슬람 기계 동일
- 입증 한계: 그림 내부 소유자를 보존한다. 필사본 연대와 발명 연대·원형 실물은 구분한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: M02-R1, M02-R2, M02-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## M03 수운의상대·자격루의 수력 경계

- 우선순위/가시성: P0 / still_structure
- 제안 역할: environment_detail, object_structure
- 출처: [S28](https://hk.space.museum/en/web/spm/resources/curators-blog/2020/12/su-song-and-the-water-driven-astronomical-clock-tower.html), [S29](https://www.gogung.go.kr/gogung/pgm/psgudMng/view.do?menuNo=800065&psgudSn=370348)
- 소유자: vessels: three supply vessels and two receiving vessels; display: separate interpretive display; water: visible water line; receiver: one of the receiving vessels
- 관계: vessels → beside → display; water → inside → receiver; receiver → member_of → vessels
- EN: Three supply vessels and two receiving vessels stand beside a separate interpretive display, with a visible water line inside one receiving vessel.
- KO: 파수 용기 세 개와 수수 용기 두 개가 별도 설명 전시 옆에 서고 수수 용기 하나 안에 수면이 보인다.
- 혼동: 항아리=완전 작동 자격루·북송 탑과 동일
- 입증 한계: 자격루의 남은 1536년 항아리와 현대 해석 실현에 한정한다. 수운의상대 상중하 탑 구조는 별도 후보로 분리한다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: M03-R1, M03-R2, M03-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

## M04 가라쿠리 차 운반과 감춰진 인간

- 우선순위/가시성: P0 / still_proxy
- 제안 역할: object_structure, relational_action
- 출처: [S30](https://www.kahaku.go.jp/exhibitions/vm/past_parmanent/rikou/computer/karakuripuppet.html), [S32](https://www.computerhistory.org/chess/stl-431e1a07e7e40/)
- 소유자: puppet: wooden tea-carrying puppet; tray: puppet tray; cup: tea cup; panel: opened service panel; cam: visible cam
- 관계: tray → held_by → puppet; cup → on → tray; cam → visible_through → panel
- EN: A wooden tea-carrying puppet holds a tray with a cup while an opened service panel exposes a cam.
- KO: 목제 차 운반 인형이 찻잔 있는 쟁반을 들고 열린 정비 패널로 캠을 드러낸다.
- 혼동: 가라쿠리=메커니컬 터크·인간 조작=기계 지능
- 입증 한계: 패널 위치는 저술한 선택이며 복원 모형의 정본이 아니다. 차 운반/회귀와 숨은 인간 체스 조작은 별도 전통이다.
- 원전 검토 범위: targeted_source_distinction_reviewed; 추가 기술 검토: False
- 관계 gate: M04-R1, M04-R2, M04-R3 (NOT_RUN; context_only는 이미지 PASS 대상 아님)

