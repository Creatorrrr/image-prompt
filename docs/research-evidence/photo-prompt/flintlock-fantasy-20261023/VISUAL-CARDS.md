# 시각 의미 카드

모든 장면 문구는 연구용 완전 대안이다. 출처가 장면의 모든 부품·숫자·배치·판타지 효과를 보증하지 않는다. 모든 native/pixel 검토는 미실행이며, I군 문맥은 양성 시각 프롬프트로 변환하지 않는다.

## A01 · 수석식의 부싯돌·물림쇠·프리즌·접시

외부 물림쇠가 작은 부싯돌을 물고 있으며 같은 격발장치의 별도 얕은 화약접시 바로 위에 굽은 강철 프리즌이 서 있다.

The external cock grips a small flint; a curved steel frizzen stands directly over the separate shallow pan on the same lock.

- 처리 제안: new / P0; 역할: object_structure, prop
- 관계: flint → clamped_in → cock; frizzen → overlaps → pan
- 혼동: 횃불/심지/회전 wheel/뇌관 nipple과 혼합
- 주장 한계: 발화 성공·장전 여부·실총 기능은 정지 외형으로 증명되지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S02 · Ignition Systems](https://nij.ojp.gov/nij-hosted-online-training-courses/firearms-examiner-training/module-03/ignition-systems)

## A02 · 화승식은 타는 심지의 소유자가 다르다

굽은 측면 홀더가 작은 접시 위에서 한쪽 끝이 붉게 빛나는 심지를 잡고 있고 심지는 나무 총상과 별도 경계를 유지한다.

A curved side holder grips a cord with one glowing tip above a small pan; the cord remains separate from the wooden stock.

- 처리 제안: new / P0; 역할: object_structure, prop
- 관계: cord → held_by → holder; cord → above → pan
- 혼동: 화승과 총용 부싯돌/장식 끈
- 주장 한계: 빛나는 심지 끝은 점화 성공이나 특정 나라·부대의 증거가 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S02 · Ignition Systems](https://nij.ojp.gov/nij-hosted-online-training-courses/firearms-examiner-training/module-03/ignition-systems)

## A03 · 휠록의 외부 휠

전시된 휠록 권총의 나무 총상 옆 격발장치에 둥근 외부 휠이 별도 부품으로 보인다.

A displayed wheellock pistol has a distinct round external lock wheel on the side of its wooden stock.

- 처리 제안: defer / P0; 역할: object_structure, prop
- 관계: wheel → part_of → lock; lock → mounted_on → stock
- 혼동: 톱니 장식/시계 문자판/플린트록의 프리즌
- 주장 한계: 실제 wheel 노출 범위·위치는 모델별 도판 검토가 필요하다. 특정 기존 후보의 below-barrel 조건도 보존한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S02 · Ignition Systems](https://nij.ojp.gov/nij-hosted-online-training-courses/firearms-examiner-training/module-03/ignition-systems), [S04 · Gun 51.84](https://art.thewalters.org/object/51.84/)

## A04 · 스냅헌스의 분리된 접시 덮개

격발장치 학습 모형에서 강철 타격면 옆에 별도의 접시 덮개가 있고 두 부품 사이 이음 경계가 보인다.

A labeled lock study shows a steel striking surface beside a separate pan cover, with a visible seam between the two pieces.

- 처리 제안: defer / P0; 역할: object_structure
- 관계: cover → covers → pan; striker → separate_from → cover
- 혼동: 프리즌 한 부품의 통합 덮개를 두 부품으로 오독
- 주장 한계: 학습 모형이라는 표현 층을 보존한다. 정확한 snaphaunce 형상은 추가 실물 도판 전까지 보류한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S02 · Ignition Systems](https://nij.ojp.gov/nij-hosted-online-training-courses/firearms-examiner-training/module-03/ignition-systems)

## A05 · 오스만 미켈레트 표본의 총열·격발부 분리

박물관 장총 표본에서 나무 총상 옆의 외부 격발부와 총열을 따라 이어진 금빛 상감 무늬가 서로 구분된다.

A museum long-gun specimen has a separate external lock beside its wooden stock and gold-colored inlay running along its barrel.

- 처리 제안: defer / P0; 역할: object_structure, surface_pattern
- 관계: inlay → on_surface_of → barrel; lock → beside → stock
- 혼동: 금 상감이 곧 miquelet 기계 구조/오스만 정체라는 오판
- 주장 한계: 명칭·지역은 박물관 provenance이고 외형 일반 법칙이 아니다. 1733 총/1862 lock 같은 혼합 연대를 유지한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S03 · Miquelet Gun, 1784–85](https://www.metmuseum.org/art/collection/search/30605), [S04 · Gun 51.84](https://art.thewalters.org/object/51.84/)

## A06 · 뇌관식의 nipple과 타격 해머

뇌관식 학습 모형에서 작은 뇌관 돌기 위의 해머와 그 돌기가 각각 독립된 윤곽을 갖는다.

A percussion-lock study has a compact hammer above a small capped nipple, with the hammer and nipple separately outlined.

- 처리 제안: new / P1; 역할: object_structure
- 관계: hammer → above → nipple; nipple → part_of → lock
- 혼동: 외부 부싯돌/큰 접시를 추가해 혼합 기구 생성
- 주장 한계: 모형 외형은 폭발·발사 성공을 보증하지 않는다. 화약 판타지의 인접 기술로 구분한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S02 · Ignition Systems](https://nij.ojp.gov/nij-hosted-online-training-courses/firearms-examiner-training/module-03/ignition-systems)

## A07 · 강선은 총열 안쪽 축이다

박물관 단면 모형이 노출된 나선 홈 총열과 부싯돌을 문 측면 격발부를 각각 보여준다.

A museum section model pairs an exposed spiral-grooved bore with a separately visible flint-gripping side lock.

- 처리 제안: new / P0; 역할: object_structure
- 관계: grooves → inside → bore; lock → beside → bore
- 혼동: rifle=현대 자동소총; 외부 총열의 나선 장식=강선
- 주장 한계: 단면 모형/실물의 층을 구분한다. flintlock과 rifling은 공존하며 정확도는 이 그림만으로 측정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S05 · Waterloo 1815](https://royalarmouries.org/objects-and-stories/stories/waterloo-1815)

## A08 · 전장/후장 분류는 별도 속성이다

역사 교육 모형이 총열 뒤의 열린 약실을 드러내고 앞쪽 총열은 별도의 이어진 부품으로 남아 있다.

A historic teaching model exposes an opened chamber at the rear of a barrel while the forward barrel remains a separate continuous piece.

- 처리 제안: defer / P1; 역할: object_structure, narrative_clue
- 관계: breech → behind → barrel; breech → part_of → model
- 혼동: 초기 후장식=현대 연발; 전장식=활강
- 주장 한계: 특정 Egg/Ferguson형으로 단정하지 않는다. 소장 모델과 도판을 먼저 골라야 구현 가능하다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S05 · Waterloo 1815](https://royalarmouries.org/objects-and-stories/stories/waterloo-1815)

## B01 · 머스킷 전신의 장총 비례

긴 나무 어깨 총상이 장총열 하나를 받치고 총열 뒤쪽 옆에는 별도의 외부 수석식 격발부가 보인다.

A long wooden shoulder stock supports one long barrel and a visibly separate external flintlock near the rear of that barrel.

- 처리 제안: new / P0; 역할: prop, object_structure
- 관계: barrel → extends_from → stock; lock → mounted_beside → barrel
- 혼동: 현대 box magazine/자동소총 receiver 자동 추가
- 주장 한계: 특정 Brown Bess/Charleville 제식명과 총열 내부를 비례만으로 판정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S05 · Waterloo 1815](https://royalarmouries.org/objects-and-stories/stories/waterloo-1815), [S07 · Flintlock dog-lock musket, 1704](https://collection.nam.ac.uk/detail.php?acc=1984-08-96-1)

## B02 · 수석식 권총의 작은 총상과 외부 lock

굽은 나무 권총 손잡이 위에 짧은 총열 하나가 있고 그 옆에 부싯돌을 문 외부 격발부가 붙어 보인다.

A curved wooden pistol grip sits below one short barrel, with an external flint-gripping lock visibly attached beside the barrel.

- 처리 제안: new / P0; 역할: prop, object_structure
- 관계: barrel → above → grip; lock → beside → barrel
- 혼동: 리볼버 cylinder/반자동 slide의 시대 혼입
- 주장 한계: 짧은 총이 모두 결투용·해적용인 것은 아니다. 결투의 법/의도는 별도 문맥이다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S02 · Ignition Systems](https://nij.ojp.gov/nij-hosted-online-training-courses/firearms-examiner-training/module-03/ignition-systems), [S04 · Gun 51.84](https://art.thewalters.org/object/51.84/)

## B03 · 블런더버스의 벌어진 총구

나무 총상 위의 짧고 굵은 총열 끝이 뚜렷하게 벌어진 종 모양 총구로 끝난다.

A short thick barrel ends in a clearly flared bell-shaped muzzle above a wooden stock.

- 처리 제안: defer / P0; 역할: prop, object_structure
- 관계: muzzle → at_end_of → barrel; barrel → supported_by → stock
- 혼동: 나팔 악기/현대 산탄총/포구 화염을 필수로 추가
- 주장 한계: 나팔 총구와 소장명 연결은 원전 도판 검토 대기다. 어떤 물체를 넣어도 발사된다는 주장으로 확장하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S08 · Flintlock Blunderbuss with Spring Bayonet](https://www.metmuseum.org/art/collection/search/32783)

## B04 · 소켓 총검과 열린 총구

소켓이 머스킷 총열 끝 둘레를 감싸고 칼날은 총강을 메우지 않은 채 열린 총구 옆으로 이어진다.

A socket encircles the end of the musket barrel; its blade runs beside the open muzzle without filling the bore.

- 처리 제안: new / P0; 역할: object_structure, contact_point
- 관계: socket → around → barrel; blade → offset_from → muzzle
- 혼동: 총구에 꽂은 plug bayonet/카메라 bayonet mount
- 주장 한계: 총검의 부착 위치와 열린 구멍을 동시에 보여야 한다. 실제 사용 안전성의 판정은 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S07 · Flintlock dog-lock musket, 1704](https://collection.nam.ac.uk/detail.php?acc=1984-08-96-1)

## B05 · 종이 탄약포와 구형 탄환

전시 탁자 위에서 말린 종이 탄약포 포장 옆에 별도의 구형 금속 탄환이 놓여 있다.

A rolled paper cartridge wrapper lies beside a separate spherical metal ball on a display table.

- 처리 제안: new / P0; 역할: prop, surface_material
- 관계: paper → on → table; ball → beside → paper
- 혼동: 종이 탄약포를 황동 탄피/뾰족한 현대 탄두로 변환
- 주장 한계: 포장 속 내용·화학 조성·장전 완료는 보이지 않는다. 1743 주머니 자료와 후기 뇌관총 탄약을 구분한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S09 · French infantry leather cartridge pouch, 1743](https://collection.nam.ac.uk/detail.php?acc=1963-10-331-1)

## B06 · 총열 아래 장전봉의 독립 경계

가느다란 봉이 주 총열 아래 별도 고정 고리들을 지나며 봉과 총열 사이에 좁은 틈이 남아 있다.

A slender rod runs through separate retaining loops below the main barrel, with a narrow gap between rod and barrel.

- 처리 제안: new / P0; 역할: object_structure, prop_placement
- 관계: rod → passes_through → loops; rod → below → barrel
- 혼동: 두 번째 총열/총검/긴 장식선으로 융합
- 주장 한계: 해당 모델에 장전봉이 실제 있는지 도판으로 확인한다. 순차 장전 절차를 한 장으로 주장하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S05 · Waterloo 1815](https://royalarmouries.org/objects-and-stories/stories/waterloo-1815)

## B07 · 포구 연기와 환경 안개의 소유

불투명하고 옅은 연기 기둥이 머스킷 총구에 닿아 먼 배경 일부를 가리키며 측면 격발부는 보인다.

A pale opaque smoke plume touches the musket muzzle and partly hides the distant background while the side lock remains visible.

- 처리 제안: new / P0; 역할: ambient_particle, atmospheric_medium
- 관계: muzzle → part_of → musket; lock → part_of → musket; plume → touches → muzzle; plume → occludes → background
- 혼동: 비/안개/마법 발광을 흑색화약의 화학 증거로 오판
- 주장 한계: 연기 사진은 화약 조성·소리·불발/지연발화·연속 일제사격의 증거가 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S02 · Ignition Systems](https://nij.ojp.gov/nij-hosted-online-training-courses/firearms-examiner-training/module-03/ignition-systems), [S05 · Waterloo 1815](https://royalarmouries.org/objects-and-stories/stories/waterloo-1815)

## B08 · 세이버와 칼집의 분리

보호 가드가 있는 손잡이에서 굽은 칼날이 이어지고 그 옆에 별도의 빈 칼집이 놓여 있다.

A curved blade extends from a guarded hilt, with its separate empty scabbard laid alongside it.

- 처리 제안: new / P1; 역할: prop, prop_placement
- 관계: blade → extends_from → guard; scabbard → beside → blade
- 혼동: smallsword/rapier의 길이·손잡이 구조와 합치기
- 주장 한계: 국가·병과·계급·날의 기능과 역사 제식명은 외형 일반성에서 얻지 못한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S06 · Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles)

## C01 · 전열은 사람들의 횡방향 정렬

얕은 횡대 하나가 화면을 가로지르며 각 보병의 별도 머스킷이 같은 열린 전경을 향한다.

One shallow transverse rank of infantry spans the frame, with separate muskets held toward the same open foreground.

- 처리 제안: new / P0; 역할: proxemics, composition
- 관계: muskets → carried_by → rank; rank → faces → front
- 혼동: 행군 종대/원형 관중/모든 병사의 총구가 신체를 관통
- 주장 한계: rank 수와 인원 수는 요청별 고정한다. 그림 한 장으로 규율·복종·발사 동기화를 증명하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S15 · Napoleonic warfare](https://exhibitions.lib.cam.ac.uk/waterloo/case/napoleonic-warfare/), [S16 · Battle of Waterloo 1815, MPH 1/387/3](https://www.nationalarchives.gov.uk/education/resources/significant-events/battle-of-waterloo-1815/)

## C02 · 사방을 향한 빈 중심 보병방진

이어진 네 면의 보병이 빈 중심을 둘러싸고 각 면의 머스킷은 중심 바깥쪽을 향한다.

Four connected sides of infantry surround an open center, and their muskets point outward on every side.

- 처리 제안: new / P0; 역할: proxemics, composition
- 관계: sides → surround → center; muskets → point_away_from → center
- 혼동: 채워진 정사각형 군중/한 면만 전방인 대열
- 주장 한계: 높은 시점에서 네 면·중앙·방향이 읽혀야 한다. 전술상 무적·승리·기병 공포는 추정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S15 · Napoleonic warfare](https://exhibitions.lib.cam.ac.uk/waterloo/case/napoleonic-warfare/), [S16 · Battle of Waterloo 1815, MPH 1/387/3](https://www.nationalarchives.gov.uk/education/resources/significant-events/battle-of-waterloo-1815/)

## C03 · 종대의 좁은 폭과 깊이

폭이 좁은 보병 종대가 길을 따라 깊이 이어지고 선두 열 뒤로 여러 뒤쪽 대열이 보인다.

A narrow column of infantry follows a road into depth, with several rear ranks visible behind the leading files.

- 처리 제안: new / P0; 역할: proxemics, spatial_depth
- 관계: files → aligned_along → road; rear → behind → files
- 혼동: 횡대/모든 종대가 돌격 종대
- 주장 한계: 깊이는 배치 증거이며 행군 속도·돌격 의도·정확한 조직 단위는 별도 문맥이다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S16 · Battle of Waterloo 1815, MPH 1/387/3](https://www.nationalarchives.gov.uk/education/resources/significant-events/battle-of-waterloo-1815/)

## C04 · 산개 배치와 엄폐물 사이 간격

보병 세 명이 각각 떨어진 바위 옆에 자리하고 위치 사이에는 열린 지면이 있으며 각자의 머스킷 경계가 구별된다.

Three infantry figures occupy separate rocks, with open ground visible between their positions and each figure’s musket kept distinct.

- 처리 제안: new / P0; 역할: proxemics, environment_detail
- 관계: soldiers → beside → cover; ground → separates → soldiers
- 혼동: 산병=모두 라이플병/예거=특정 제복 자동 고정
- 주장 한계: 셋은 제안 장면의 수량이다. 부대 정원·정찰 임무·사격 능력의 역사 규칙이 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S05 · Waterloo 1815](https://royalarmouries.org/objects-and-stories/stories/waterloo-1815), [S15 · Napoleonic warfare](https://exhibitions.lib.cam.ac.uk/waterloo/case/napoleonic-warfare/)

## C05 · 기마 전령의 몸·말·봉인 문서

말 한 마리에 탄 전령이 고삐와 떨어진 봉인 종이 꾸러미를 들고 있으며 손과 문서의 경계가 보인다.

A mounted courier on one horse holds a sealed paper packet clear of the reins, with packet and hand boundaries visible.

- 처리 제안: new / P1; 역할: relational_action, prop_placement
- 관계: rider → mounted_on → horse; packet → held_by → hand; hand → part_of → rider
- 혼동: 문서를 든 사람=적법 명령/기병=용기병 고정
- 주장 한계: 전령이라는 역할은 요청 문맥이다. 전달 완료·문서 진위·읽힌 내용은 손에 든 외형으로 증명되지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S06 · Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles)

## C06 · 흉갑·천 제복·말의 경계

말을 탄 성인 병사가 천 코트 바깥에 별도 가장자리의 단단한 흉갑을 입으며 흉갑은 말·고삐와 독립된 경계를 갖는다.

An adult mounted soldier wears a separately edged rigid breastplate over a cloth coat; the plate remains distinct from the horse and reins.

- 처리 제안: new / P0; 역할: wardrobe_layering, garment_detail
- 관계: plate → outside → coat; coat → worn_by → rider; rider → mounted_on → horse
- 혼동: 전신 중세 plate armor/흉갑+러프 bundle의 무단 절단
- 주장 한계: 금속빛은 재료 성분/방탄 등급을 증명하지 않는다. 해당 시대의 backplate·helmet은 별도 검토한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S06 · Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles)

## C07 · 한 어깨 pelisse와 속 재킷

성인이 몸에 맞는 별도 재킷 위 한쪽 어깨에 털 가장자리의 짧은 겉재킷을 걸치고 비어 늘어진 소매 하나의 윤곽이 보인다.

An adult wears a fitted jacket beneath a short fur-edged overjacket slung over one shoulder, with one empty hanging sleeve visibly edged.

- 처리 제안: defer / P0; 역할: wardrobe_layering, garment_detail
- 관계: shoulder → part_of → wearer; underjacket → worn_by → wearer; pelisse → draped_over → shoulder; pelisse → outside → underjacket; sleeve → part_of → pelisse
- 혼동: 가죽 코트/양팔을 모두 넣은 재킷/어깨 천을 털로 융합
- 주장 한계: 특정 regiment·국적·연도는 별도 정한다. 후사르=모든 기병이 아니고 삼각모도 자동 추가하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S06 · Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles)

## C08 · 견장은 어깨 부착물이고 계급은 문맥

장식 견장들이 재킷 어깨 위에 놓이고 각 부착 밑판이 보인다.

Decorative epaulettes sit on the jacket shoulders with visible bases.

- 처리 제안: refine / P1; 역할: garment_detail, wearable_accessory
- 관계: epaulettes → attached_at → bases; bases → on → shoulders
- 혼동: 견장=왕실/귀족/공주/장교·군적 자동 추론
- 주장 한계: 장식 부착 구조만 관찰한다. 계급·군적·왕실 문양은 요청/명문·자료가 각각 필요하다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S06 · Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles)

## D01 · 포대의 포문-포신 정렬

설치된 대포가 흉벽 뒤의 넓은 포좌에 놓이고 포신 하나가 대응하는 포문 하나를 통하여 바깥을 향한다.

A mounted cannon rests on a broad platform behind a parapet, its barrel aligned outward through one matching embrasure.

- 처리 제안: refine / P0; 역할: location, object_structure
- 관계: gun → on → platform; gun → points_through → opening; opening → in → parapet
- 혼동: 포가 벽과 접촉 없이 떠 있음/포문과 불일치
- 주장 한계: 기존 CID의 완전 배치를 재사용·번역 보정한다. 배터리의 수·성능·발사 여부는 별도다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S12 · Bastion](https://sites-vauban.org/en/resources/glossary/bastion), [S17 · What was a carronade?](https://www.rmg.co.uk/stories/maritime-history/what-was-carronade)

## D02 · 실체탄은 전시된 구형 물체

철빛 구체 하나가 전시대에 놓이고 바깥 표면은 절개 없이 이어진다.

One unbroken iron-colored sphere rests on a display stand, with a continuous outer surface and no visible cutaway.

- 처리 제안: new / P0; 역할: prop, prop_state
- 관계: ball → rests_on → stand
- 혼동: 둥근 포탄=무조건 폭발탄/내부가 보인다는 주장
- 주장 한계: solid shot이라는 분류는 사료/선언에서 온다. 닫힌 표면만으로 속이 비었는지 꽉 찼는지 판정할 수 없다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S10 · Artillery – Types of Rounds](https://www.nps.gov/fosc/learn/education/artshot.htm), [S11 · A Rusty Shrapnel Round](https://en.rcamuseum.com/a-rusty-shrapnel-round/)

## D03 · canister는 용기와 내부 작은 탄자

표기가 있는 원통형 탄약 절개 모형의 열린 단면 안에 작은 구형 탄자들이 별도로 쌓여 보인다.

A labeled cutaway cylindrical ammunition container reveals separate small balls stacked inside its open section.

- 처리 제안: new / P0; 역할: object_structure, prop
- 관계: balls → inside → container
- 혼동: 유산탄의 공중 폭발/산탄통=포도탄의 동일 포장
- 주장 한계: 절개 교육 모형 층을 유지한다. 19세기 예시를 전 시대 제식으로 고정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S10 · Artillery – Types of Rounds](https://www.nps.gov/fosc/learn/education/artshot.htm)

## D04 · 구형 포탄 단면과 폭발 주장의 분리

구형 포탄 단면 모형이 두꺼운 굽은 벽으로 둘러싸인 내부 공동 하나를 드러낸다.

A spherical shell section model exposes one inner cavity bounded by a thick curved wall.

- 처리 제안: new / P0; 역할: object_structure
- 관계: cavity → inside → wall; wall → part_of → model
- 혼동: WW1 길쭉한 shell을 1803 구형 유산탄으로 사용
- 주장 한계: 공동은 내용의 폭약 조성/신관 동작/실제 폭발을 증명하지 않는다. 단면의 교육 모델임을 보존한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S10 · Artillery – Types of Rounds](https://www.nps.gov/fosc/learn/education/artshot.htm), [S11 · A Rusty Shrapnel Round](https://en.rcamuseum.com/a-rusty-shrapnel-round/)

## D05 · 본체에 붙은 낮은 오각 보루

비스듬한 높은 시점에서 낮고 각진 보루가 주 성벽에 붙어 바깥으로 돌출한다.

A low angular bastion projects from and remains joined to the main defensive wall in an elevated oblique view.

- 처리 제안: refine / P0; 역할: location, object_structure
- 관계: bastion → joined_to → wall; bastion → projects_from → wall
- 혼동: 독립 ravelin/중세 원형 탑/별 모양 도시 전체 강제
- 주장 한계: 기존 보루+외보 bundle을 선택할 때는 외보를 삭제하지 않는다. 단독 보루는 별도 새 실현 여부를 검토한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S12 · Bastion](https://sites-vauban.org/en/resources/glossary/bastion)

## D06 · 해자 건너 분리된 라블랭

별도의 삼각 외보가 주 출입구 앞에 놓이며 이어진 해자가 외보를 주 성벽과 분리해 보인다.

A separate triangular outwork sits in front of the main gate, with a continuous ditch visibly separating it from the main wall.

- 처리 제안: refine / P0; 역할: location, spatial_depth
- 관계: ditch → separates → ravelin; ravelin → in_front_of → gate
- 혼동: 외보가 본체에 융합/물 해자만 요새의 필수 요소로 고정
- 주장 한계: 마른 해자도 가능하다. 외보·성벽·해자의 양끝이 한 프레임에서 구별되어야 한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S13 · Demi-lune or ravelin](https://sites-vauban.org/en/resources/glossary/demi-lune-or-ravelin)

## D07 · 글라시스의 완사면

넓고 완만한 흙 경사면이 피복도 정상에서 바깥 들판으로 내려가고 측면에서 경사 변화가 보인다.

A broad gentle earth slope descends from the covered-way crest to the outer field, with the change of grade visible in profile.

- 처리 제안: new / P0; 역할: location, spatial_depth
- 관계: slope → descends_from → crest; slope → meets → field
- 혼동: 가파른 절벽/해자 바닥/높은 성벽
- 주장 한계: 고저가 안 보이는 정면 크롭은 판정 불가다. 고정 각도나 현대 토목 규격을 주장하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S14 · Glacis](https://sites-vauban.org/ressources/glossaire/glacis)

## D08 · 포차·전차의 운송 연결

야포 포가와 별도의 두 바퀴 전차가 지면 위의 뚜렷한 연결부 하나에서 만난다.

A field-gun carriage and a separate two-wheeled limber meet at one clearly visible coupling on the ground.

- 처리 제안: defer / P1; 역할: object_structure, contact_point
- 관계: coupling → joins → gun; coupling → joins → limber
- 혼동: 기마포병=말 없는 고정 대포/현대 견인 트레일러
- 주장 한계: 정확한 coupling과 바퀴수는 모델별 도판 검토가 필요하다. 운송·빠른 재배치의 성공은 정지 관계와 별개다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S06 · Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles)

## E01 · 목조 범선의 현측 포문

목조 범선 선체 측면을 따라 열린 포문들이 있고 별도 포신들이 돛대·돛 아래에서 돌출한다.

A wooden sailing hull carries a row of open side gunports with separate projecting barrels, beneath masts and sails.

- 처리 제안: new / P0; 역할: location, object_structure
- 관계: ports → along_side_of → hull; guns → through → ports; masts → above → hull
- 혼동: 현대 강철 전함/선수 주포/세 포갑판을 모든 frigate에 추가
- 주장 한계: gun deck 수·제식 함종은 특정 선박 자료가 필요하다. broadside는 측면 방향이며 선수 방향과 다르다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S17 · What was a carronade?](https://www.rmg.co.uk/stories/maritime-history/what-was-carronade), [S38 · Teacher’s Highlights: HMS Victory](https://www.nmrn.org.uk/sites/default/files/2022-09/PHD-Teachers-Highlights-FINAL.pdf)

## E02 · 캐러네이드의 짧은 포신·슬라이드

짧고 굵은 함포 포신이 선박 갑판에 고정된 낮은 슬라이드 포가 위에 놓여 있다.

A short broad cannon barrel sits on a low sliding carriage fixed to a ship deck.

- 처리 제안: new / P0; 역할: object_structure
- 관계: barrel → mounted_on → slide; slide → on → deck
- 혼동: 장포신 함포/야전 대형 차륜 포가와 자동 결합
- 주장 한계: 모든 carronade가 같은 포가인 것은 아니다. 슬라이드 변형 한 가지의 선택안이다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S17 · What was a carronade?](https://www.rmg.co.uk/stories/maritime-history/what-was-carronade)

## E03 · 현측 사격의 방향 관계

뒤쪽 높은 시점에서 한 줄의 포문으로부터 옅은 연기가 옆으로 뻗고 선수는 그와 다른 뚜렷한 축을 향한다.

Seen from above and behind, pale plumes extend sideways from one gunport row while the bow points along a different clear axis.

- 처리 제안: new / P0; 역할: composition, physical_motion
- 관계: smoke → extends_from → side; side → part_of → ship; bow → part_of → ship
- 혼동: 연기 방향=전진 방향/모든 포 동시 발사의 시간 증거
- 주장 한계: 이 프레임은 배치와 연기 접점만 보인다. salvo 동기화·바람·교전 결과는 시간/서사 정보가 필요하다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S17 · What was a carronade?](https://www.rmg.co.uk/stories/maritime-history/what-was-carronade), [S38 · Teacher’s Highlights: HMS Victory](https://www.nmrn.org.uk/sites/default/files/2022-09/PHD-Teachers-Highlights-FINAL.pdf)

## E04 · 막대탄의 두 탄체와 단단한 연결

전시 표면 위에서 별도의 두 탄체 끝이 곧고 단단한 철빛 막대 하나로 연결된다.

Two distinct shot ends are connected by one straight rigid iron-colored bar on a display surface.

- 처리 제안: defer / P0; 역할: object_structure, prop
- 관계: bar → connects_to → end1; bar → connects_to → end2
- 혼동: bar shot=chain shot/실제 비행 중 회전
- 주장 한계: 양끝 연결은 시각 제안이다. 원전 사진 검토 전 정확한 탄체 모양·연대는 보류한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S18 · Bar shot KTP1022](https://www.rmg.co.uk/collections/objects/rmgc-object-36875)

## E05 · 사슬탄과 막대탄의 유연 연결 차이

학습 전시에서 두 탄체 끝이 느슨하게 늘어진 고리 사슬로 이어지고 양쪽 부착점이 보인다.

A study display shows two shot ends joined by a slack linked chain, with both attachment points visible.

- 처리 제안: defer / P1; 역할: object_structure
- 관계: chain → attached_to → end1; chain → attached_to → end2
- 혼동: 직선 bar/장식 체인/연결점 소실
- 주장 한계: S18은 bar shot만 확인했다. chain shot의 직접 소장 원전은 미확보이므로 새 양성 후보 채택을 보류한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S18 · Bar shot KTP1022](https://www.rmg.co.uk/collections/objects/rmgc-object-36875)

## E06 · 사략허가장이라는 문서의 가시 층

"LETTER OF MARQUE" 머리글이 있는 허구 허가장 한 장이 해도 탁자 위에 놓이고 종이에 붙은 봉인 하나가 보인다.

A fictional commission sheet headed "LETTER OF MARQUE" rests on a chart table, with one visible seal attached to the paper.

- 처리 제안: new / P1; 역할: prop, visible_text
- 관계: seal → on → document; document → on → table
- 혼동: 문서 외형=실제 국가 허가/해적=사략선
- 주장 한계: 문구·봉인은 요청자 승인 후 선택하는 시각 장치다. 법적 효력·진위·발행 국가를 증명하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S19 · Privateers](https://www.history.navy.mil/our-collections/art/exhibits/conflicts-and-operations/the-war-of-1812/privateers.html)

## E07 · 두 선박 사이의 승선 접점

판자 하나가 별도 목조 갑판 두 개 사이 틈을 가로지르고 성인 한 명이 양 갑판 가장자리와 구별되는 발로 판자 위에 서 있다.

A plank spans the gap between two distinct wooden decks while one adult figure stands on the plank with a foot clear of each deck edge.

- 처리 제안: new / P1; 역할: relational_action, contact_point
- 관계: plank → bridges → ship1; plank → bridges → ship2; adult → on → plank
- 혼동: 접현/승선 배치=나포·공격·적대 의도
- 주장 한계: 공격인지 구조인지 교역인지 배치만으로 판정하지 않는다. 도약·승선 완료 같은 시간 주장도 분리한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S19 · Privateers](https://www.history.navy.mil/our-collections/art/exhibits/conflicts-and-operations/the-war-of-1812/privateers.html), [S39 · His Majesty’s Dragon](https://www.penguinrandomhouse.com/books/122950/his-majestys-dragon-by-naomi-novik/)

## E08 · 풍상 위치는 도식의 선언 정보

허구 해전 도식이 "WIND"라고 적힌 뚜렷한 화살표의 양쪽에 별도 선박 기호 두 개를 놓는다.

A fictional sea diagram places two separate ship icons on opposite sides of a clear arrow labeled "WIND".

- 처리 제안: defer / P1; 역할: composition, visible_text
- 관계: arrow → on → chart; ships → on → chart
- 혼동: 사진 속 돛 모양만으로 풍상 우위/항해 성공 추정
- 주장 한계: 이것은 도식의 주장이지 실제 바람 측정이 아니다. weather gauge의 원전 전술 검토는 추가 필요하다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S17 · What was a carronade?](https://www.rmg.co.uk/stories/maritime-history/what-was-carronade), [S38 · Teacher’s Highlights: HMS Victory](https://www.nmrn.org.uk/sites/default/files/2022-09/PHD-Teachers-Highlights-FINAL.pdf)

## F01 · 보급 수송 수레의 적재·차체 관계

천 자루들이 목조 수레 적재함 안에 놓이고 짐의 경계가 바퀴·차축과 분리되어 있다.

Cloth sacks sit inside a wooden wagon bed, with the load boundary kept separate from the wheels and axle.

- 처리 제안: new / P1; 역할: prop, prop_placement
- 관계: sacks → inside → bed; bed → part_of → wagon
- 혼동: 중세 마차/현대 군용 트럭; 모든 자루=화약
- 주장 한계: 보급이라는 문맥을 외형으로 확정하지 않는다. 내용물·배급 충분성·수송 성공은 별도다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S06 · Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles), [S20 · Camp Followers](https://www.amrevmuseum.org/virtualexhibits/picturing-washington-s-army/pages/campfollowers)

## F02 · 화약고는 저장실 문맥

닫힌 통들이 단순한 석조 저장실 안의 높인 나무 받침 위에 놓여 있다.

Closed barrels stand on a raised wooden platform inside a plain masonry storage chamber.

- 처리 제안: new / P1; 역할: location, prop_placement
- 관계: barrels → on → platform; platform → inside → room
- 혼동: magazine=탄창/잡지; 통 외형=화약 함량
- 주장 한계: 화약고라는 명칭은 요청/명문에 의존한다. 이 구성은 안전한 저장법이나 실제 내용물의 증거가 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S12 · Bastion](https://sites-vauban.org/en/resources/glossary/bastion), [S14 · Glacis](https://sites-vauban.org/ressources/glossaire/glacis)

## F03 · 종군 세탁 노동과 젖은 천

성인 세탁 노동자가 나무 통 위에서 젖은 천 하나를 들고 있으며 물방울이 천 가장자리와 통 테두리 사이에 보인다.

An adult laundry worker holds one wet cloth above a wooden tub, with water drops separating the cloth edge from the tub rim.

- 처리 제안: new / P0; 역할: relational_action, contact_point
- 관계: cloth → held_by → hands; cloth → above → tub; hands → part_of → adult
- 혼동: camp follower=매춘부; 젖은 천=질병/성적 노출
- 주장 한계: 직업 문맥은 요청에서 선언한다. 성적 관계·가족 관계·공식 군적은 이미지로 추정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S20 · Camp Followers](https://www.amrevmuseum.org/virtualexhibits/picturing-washington-s-army/pages/campfollowers), [S21 · The Army Laundress](https://www.nps.gov/articles/000/the-army-laundress.htm)

## F04 · 종군 판매인의 음식 인계

성인 판매인과 성인 병사가 음식 그릇 하나를 사이에 두고 마주 보며 각자의 손이 그릇의 반대쪽 가장자리에 닿는다.

An adult seller and an adult soldier face each other over one food bowl, their separate hands meeting opposite edges of the bowl.

- 처리 제안: new / P0; 역할: relational_action, contact_point
- 관계: seller_hand → part_of → seller; buyer_hand → part_of → buyer; seller_hand → touches → bowl; buyer_hand → touches → bowl
- 혼동: 비방디에르/캉티니에르=특정 연도 제복 자동 고정
- 주장 한계: 양손의 actor owner는 추후 typed effect에서 각각 분리해야 한다. 돈·보수·동의·생계 원인은 별도 문맥이다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S20 · Camp Followers](https://www.amrevmuseum.org/virtualexhibits/picturing-washington-s-army/pages/campfollowers)

## F05 · 기마포의 말과 연결구

마구를 착용한 말 두 마리가 별도 전차 앞에 서 있고 마구 조립체와 차량 사이로 끌줄 하나가 이어져 보인다.

Two harnessed horses stand ahead of a separate limber, with one visible trace continuing between the harness assembly and vehicle.

- 처리 제안: defer / P1; 역할: relational_action, object_structure
- 관계: harness → on → horses; trace → attached_to → harness; trace → attached_to → limber
- 혼동: 말=고정 여섯 마리; 끌줄이 몸/바퀴를 관통
- 주장 한계: 두 마리는 제안 수량이며 역사 표준이 아니다. 마구 연결과 하중의 물리 검토를 추가한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S06 · Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles)

## F06 · 완목전신의 팔·피벗·탑

신호탑 위의 중앙 보에 별도의 관절형 끝팔 두 개가 서로 다른 각도로 놓여 있고 피벗이 뚜렷하게 구별된다.

A signal tower supports a central beam with two separately jointed end arms held at distinct visible angles, with their pivots clearly outlined.

- 처리 제안: new / P0; 역할: object_structure, location
- 관계: beam → above → tower; arms → jointed_to → beam
- 혼동: 전기 전신/안테나; 1933 모형=1792 실물
- 주장 한계: 도식/모형/실물의 표현 층을 선택한다. 한 팔 각도로 메시지 송수신·암호·작동 시간을 확인하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S22 · One model of Chappe semaphore tower](https://collection.sciencemuseumgroup.org.uk/objects/co48224/one-model-of-chappe-semaphore-tower)

## F07 · 구체적 수술 기구의 전시와 피해 분리

소형 활틀형 외과 톱을 전시하여 틀 안의 짧고 곧은 날과 별도의 나무 손잡이를 보여준다.

A small bow-frame surgical saw is displayed with a short straight blade inside its frame and a separate wooden handle.

- 처리 제안: new / P1; 역할: prop, object_structure
- 관계: blade → within → frame; handle → attached_to → frame
- 혼동: 손뼈용 소형 톱=모든 절단 도구/수술 장면
- 주장 한계: 기구 존재는 절단·절차·회복·통증·감염을 증명하지 않는다. 환자·상처·혈흔은 자동 추가하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S35 · Benjamin Bell-type metacarpal amputation saw](https://collection.sciencemuseumgroup.org.uk/objects/co167835/benjamin-bell-type-metacarpal-amputation-saw-europe-1780-1850)

## F08 · 구속구의 고리·막대와 신분 분리

박물관 전시 표면 위 연결 막대 하나에 굽은 철빛 고리 두 개가 끼워져 있다.

Two curved iron-colored loops are threaded onto one connecting bar on a museum display surface.

- 처리 제안: new / P0; 역할: prop, object_structure
- 관계: loops → threaded_on → bar; bar → on → surface
- 혼동: 구속구=이미지 속 사람의 노예/범죄 신분
- 주장 한계: 이 실현에는 사람이 없다. 소장 분류·알려진 역사적 사용과 새 피사체의 원인/동의/법적 신분을 분리한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S33 · Leg-irons ZBA2471](https://www.rmg.co.uk/collections/objects/rmgc-object-254405), [S34 · Set of wrought iron leg shackles](https://nmaahc.si.edu/object/nmaahc_2008.10.2)

## G01 · 혁명 코케이드의 실제 부착점

삼색 리본 장미장식이 모자 한쪽에 고정되어 주름과 부착부가 모자 표면과 구별된다.

A three-color ribbon rosette is pinned to one side of a hat, its folds and attachment kept separate from the hat surface.

- 처리 제안: new / P0; 역할: garment_detail, wearable_accessory
- 관계: cockade → attached_by → pin; pin → on → hat
- 혼동: 장식 색=정치 충성·시민권·프랑스인 확정
- 주장 한계: 국가별 색 순서·연도는 별도 검토한다. 소속 상징의 서사 의미를 사실로 자동 부여하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S26 · Cap, ca. 1790](https://www.metmuseum.org/art/collection/search/689887)

## G02 · 선전 낱장과 현측포의 다의어

"PUBLIC NOTICE" 머리글을 인쇄한 종이 한 장이 회벽에 붙어 있고 네 가장자리가 모두 보인다.

One printed sheet headed "PUBLIC NOTICE" is pasted onto a plaster wall, with all four paper edges visible.

- 처리 제안: new / P0; 역할: visible_text, prop
- 관계: sheet → pasted_on → wall; heading → printed_on → sheet
- 혼동: broadside=함포 broadside; 무작위 가짜 텍스트
- 주장 한계: 정확한 문구는 별도 요청/승인이 필요하다. 붙은 공고가 혁명·검열·동원 성공의 증거는 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S27 · The Popularity of Broadsides](https://www.loc.gov/static/collections/broadsides-and-other-printed-ephemera/articles-and-essays/introduction-to-printed-ephemera-collection/the-popularity-of-broadsides.html)

## G03 · 회사군의 동일 표지와 사람의 개별성

성인 병사 두 명이 같은 허구 회사 표지가 붙은 별도의 코트를 입고 얼굴과 개인 소지품은 서로 구별된다.

Two adult soldiers wear separate coats bearing the same fictional company badge, while their faces and personal belongings remain distinct.

- 처리 제안: new / P1; 역할: social_cue, garment_detail
- 관계: badges → on → coats; coats → worn_by → adults
- 혼동: 회사군=모두 외국인 용병; 피부/터번=직위·충성
- 주장 한계: 회사군이라는 제도는 문맥이다. 현지인/외부인·식민 피지배·종교를 외형에서 자동 분류하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S25 · Armies of the East India Company](https://www.nam.ac.uk/explore/armies-east-india-company)

## G04 · 회계 장부와 전쟁금융의 비가시성

줄을 그은 칸이 있는 펼친 장부가 책상 위에 놓이고 옆에는 별도의 동전과 펜이 있다.

An open ledger with ruled columns lies on a desk beside separate coins and a pen.

- 처리 제안: new / P1; 역할: prop, visible_text
- 관계: columns → on → ledger; coins → beside → ledger; ledger → on → desk
- 혼동: 장부/동전=국가채무·수탈·횡령 확정
- 주장 한계: 장부의 구체 텍스트·역사 문서 내용이 없으면 제도와 거래를 판정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S28 · History](https://www.bankofengland.co.uk/about/history)

## G05 · 커피하우스의 교류 공간

앉은 성인 세 명이 공동 탁자 주위에 모이고 탁자 위에는 별도 커피잔들과 그들 사이의 종이 한 장이 있다.

Three seated adults gather around a shared table with separate coffee cups and one paper sheet between them.

- 처리 제안: new / P1; 역할: location, relational_action
- 관계: adults → around → table; cups → on → table; paper → on → table
- 혼동: 모든 coffeehouse=유럽 남성 살롱/음모·계몽주의 자동 판정
- 주장 한계: 지역·성별·계층·종교와 발화 내용은 요청에 맡긴다. 컵·종이만으로 정치 토론이 증명되지는 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S37 · Life in a cup: coffee culture in the Islamic world](https://www.britishmuseum.org/exhibitions/life-cup-coffee-culture-islamic-world)

## G06 · 로코코의 비대칭 곡선 장식

벽 장식틀에 비대칭 S·C자 곡선 장식이 있고 그 안의 조개 모티프가 별도로 읽힌다.

A wall frame carries asymmetric S- and C-shaped ornament around a separately readable shell motif.

- 처리 제안: new / P1; 역할: surface_pattern, environment_detail
- 관계: curves → on → frame; shell → within → frame
- 혼동: 금색=로코코; 로코코=퇴폐·성적 의도
- 주장 한계: 표면 장식만 제안한다. 제국·귀족·성적 맥락이나 전체 시대를 자동 활성화하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S29 · The Rococo style – an introduction](https://www.vam.ac.uk/articles/the-rococo-style-an-introduction)

## G07 · 로브의 앞트임·별도 속치마

성인 크기의 의복 전시 마네킹을 앞에서 보아 겉가운의 앞트임 안쪽으로 별도 가장자리를 가진 장식 속치마가 드러난다.

The front view of an adult-sized dress form shows an outer gown opening over a separately edged decorated underskirt.

- 처리 제안: new / P1; 역할: garment_detail, wardrobe_layering
- 관계: gown → on → form; underskirt → visible_through → opening; opening → part_of → gown
- 혼동: 속치마=노출 피부; 앞모습에서 등 주름까지 증명
- 주장 한계: 등 주름은 G09로 분리했다. 의복만으로 연령·신분·직업·동의·성적 의미를 확정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S30 · Robe à la française, ca. 1780](https://www.metmuseum.org/art/collection/search/159432)

## G08 · 단두대 상징물과 실제 장비의 층

보석 전시대의 고리에 작은 단두대 모양 귀걸이가 매달리고 고리는 작은 칼날 모티프보다 크게 보인다.

A miniature guillotine-shaped earring hangs from its hook on a jewelry stand, with the hook larger than the tiny blade motif.

- 처리 제안: new / P1; 역할: prop, scale_relation
- 관계: earring → hangs_from → hook; hook → on → stand
- 혼동: 약1880 귀걸이=1792 처형 기계/장신구=실제 폭력
- 주장 한계: 후대 기념/상징물이다. 실제 처형 기구는 별도 당시 원전과 후보가 필요하다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S36 · Pendants d’oreilles à la guillotine](https://www.carnavalet.paris.fr/collections/pendants-doreilles-la-guillotine)

## G09 · 로브의 뒤쪽 상자주름

의복 전시 마네킹 가운의 뒷모습에서 넓은 상자주름이 어깨 부위로부터 등을 따라 내려온다.

The rear view of a dress-form gown shows broad box pleats descending from its shoulder region down the back.

- 처리 제안: new / P1; 역할: garment_detail
- 관계: pleats → on_back_of → gown; pleats → descend_from → shoulders
- 혼동: 뒤 주름=앞 속치마 노출/앞뒤 동시 관찰
- 주장 한계: 앞트임은 G07의 별도 실현이다. 같은 옷의 앞뒤가 모두 요청되면 뷰별 이미지와 정체 연결을 따로 검증한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S30 · Robe à la française, ca. 1780](https://www.metmuseum.org/art/collection/search/159432)

## H01 · 화약-마법 매개를 손과 분리

성인 판타지 병사의 펼친 손바닥 위에서 별도 어두운 알갱이들이 가는 발광 곡선을 따라 떠 있고 피부와 융합되지 않는다.

Above an adult fantasy soldier’s open palm, separate dark grains hover along a thin luminous arc without merging into the skin.

- 처리 제안: new / P0; 역할: surreal_physics_detail, relational_action
- 관계: grains → above → hand; arc → between → grains; hand → part_of → adult
- 혼동: 검은 알갱이=흑색화약 화학 증명; 모든 powder mage=같은 능력
- 주장 한계: 화약이라는 매개는 요청에 선언해야 한다. 이 효과는 새 창작안이며 작품의 흡입 방식이나 정본 능력 재현이 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood)

## H02 · 결계는 보호 대상·바깥의 경계

투명한 굽은 장벽이 성인 보병 세 명 앞에 서서 아래 가장자리가 땅에 닿고 그 너머에는 열린 들판이 남아 있다.

A transparent curved barrier stands in front of three adult infantry, its lower edge touching the ground while open field remains beyond it.

- 처리 제안: new / P0; 역할: surreal_physics_detail, spatial_depth
- 관계: ward → in_front_of → soldiers; outside → beyond → ward; ward → touches → ground
- 혼동: 바리어가 인물을 관통; 구체적 방호 반경·불사성 추정
- 주장 한계: 결계라는 이름과 효과는 요청 문맥이다. 이 이미지는 탄환 차단/반사·지속 시간·방탄 성능을 증명하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S24 · The Shadow Campaigns](https://djangowexler.com/series/the-shadow-campaigns/)

## H03 · 탄도 조작은 도식적 궤적 제안

떠 있는 구형 투사체 하나가 보이는 총구에서 시작된 발광 곡선 궤적 하나의 끝에 놓인다.

One floating spherical projectile sits at the end of a single curved luminous trace beginning at a visible gun muzzle.

- 처리 제안: defer / P0; 역할: surreal_physics_detail, composition
- 관계: trail → extends_from → muzzle; ball → at_end_of → trail
- 혼동: 곡선 trail=시간상 궤적·마법 원인 실증
- 주장 한계: 정지 이미지의 궤적 표현이며 실제 속도·사격 능력·목표 명중을 증명하지 않는다. source는 이 구체 궤적의 정본이 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood)

## H04 · 마법 신호의 두 끝점

가는 발광선이 별도의 신호 원반 두 개에 닿고 한 프레임에서 양 접점이 보인다.

A thin luminous line touches two separate signal disks, with both contact points visible in one frame.

- 처리 제안: new / P0; 역할: surreal_physics_detail, relational_action
- 관계: line → touches → sender; line → touches → receiver
- 혼동: 발광선=정보 전달·암호 해독·응답 성공
- 주장 한계: 선은 창작 표현이다. 송수신·내용 일치·거리·시차는 별도 서사 또는 시간/데이터 검증이 필요하다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S22 · One model of Chappe semaphore tower](https://collection.sciencemuseumgroup.org.uk/objects/co48224/one-model-of-chappe-semaphore-tower), [S24 · The Shadow Campaigns](https://djangowexler.com/series/the-shadow-campaigns/)

## H05 · 마법의 치유 부위와 손의 owner

성인 치유자의 손이 성인 환자의 붕대를 감은 팔 위에 떠 있고 손과 붕대 사이에는 작은 빛 조각이 보인다.

An adult healer’s hand hovers over a wrapped adult patient’s forearm, with a small luminous patch between hand and bandage.

- 처리 제안: new / P0; 역할: contact_point, surreal_physics_detail
- 관계: hand → part_of → healer; arm → part_of → patient; wrap → around → arm; hand → above → wrap; light → below → hand; light → above → wrap
- 혼동: 손의 주인 혼동/빛=치유 완료·통증 없음
- 주장 한계: 손의 actor와 환자의 팔 owner를 분리한다. 이 빛이 치료 성공·환자 동의·진단을 증명하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S24 · The Shadow Campaigns](https://djangowexler.com/series/the-shadow-campaigns/)

## H06 · 군사 강령술은 뼈·제복·대형의 실현

관절형 해골 형상 하나가 별도 군복풍 코트를 입고 서 있으며 보이는 갈비뼈가 천 가장자리와 구별된다.

One articulated skeleton figure stands in a separate military-style coat, its visible rib bones kept distinct from the cloth edges.

- 처리 제안: new / P1; 역할: body_form, wardrobe_layering
- 관계: coat → worn_by → figure; figure → stands_on → ground
- 혼동: 해골 소품=실제 죽음·부활/서서 있음=병역·의식
- 주장 한계: 군사 강령술의 선택적 창작 실현이다. 사후 복무·시체 소유·생사·의식·강제는 원문/서사로 남긴다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S01 · Django Wexler Collection](https://findingaids.library.tamu.edu/index.php/django-wexler-collection), [S24 · The Shadow Campaigns](https://djangowexler.com/series/the-shadow-campaigns/)

## H07 · 용·마구·승무원의 하중 관계

큰 용의 몸을 별도 마구가 감싸며 그 마구에 붙은 작은 승무원 발판 위에 성인 승무원 한 명이 서 있다.

A large dragon wears a separate body harness supporting a small crew platform with one adult crew member standing on it.

- 처리 제안: defer / P1; 역할: relational_action, scale_relation
- 관계: harness → around → dragon; platform → attached_to → harness; adult → on → platform
- 혼동: 팔/날개와 마구 융합; 발판이 허공에 떠 있음
- 주장 한계: 구체 마구는 창작안이며 작품 정본이 아니다. 해부·하중·날개 가동 범위 검토를 마친 뒤 채택한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S39 · His Majesty’s Dragon](https://www.penguinrandomhouse.com/books/122950/his-majestys-dragon-by-naomi-novik/)

## H08 · 군수 마법의 공방·검수 물체

성인 공방 노동자가 집게로 새김 무늬의 금속빛 구체 하나를 잡아 별도의 검수 받침 위에 둔다.

An adult workshop worker holds one etched metal-colored sphere with tongs above a separate inspection tray.

- 처리 제안: new / P1; 역할: object_structure, relational_action
- 관계: ball → held_by → tongs; tongs → held_by → worker; tray → below → ball
- 혼동: 무늬=마법 탄약 성능·검수 통과; 노동자=노예
- 주장 한계: 마법 탄약·독점·군수 생산이라는 문맥은 별도 선언이다. 전시·금속 작업·수리와도 구분한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S25 · Armies of the East India Company](https://www.nam.ac.uk/explore/armies-east-india-company)

## J01 · 삼각모의 접힌 세 방향

낡은 삼각모 소품을 위에서 전시하여 중앙 모자통 둘레의 접어 올린 챙 세 부분이 구별된다.

A weathered tricorn hat prop is displayed from above with three upturned brim sections clearly separated around its crown.

- 처리 제안: defer / P1; 역할: prop, object_structure
- 관계: brim → around → crown; crown → part_of → hat
- 혼동: 이각모/카우보이모/착용자=해적
- 주장 한계: 원문 삼각모 소품은 재사용 가능하나 정확한 세 접힘은 실물 도판 검토 후 보강한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S40 · Eighteenth-Century European Dress](https://www.metmuseum.org/essays/eighteenth-century-european-dress)

## J02 · 이각모의 두 끝과 긴 접힌 챙

이각모 학습 소품이 중앙 모자통 양옆의 뾰족한 챙 끝 두 개를 보여 주며 전시대 위 별도 물체로 놓인다.

A bicorne study prop has two opposed pointed brim ends flanking a central crown, shown as a separate object on a stand.

- 처리 제안: defer / P1; 역할: prop, object_structure
- 관계: ends → flank → crown; crown → part_of → hat
- 혼동: 삼각모의 세 접힘/착용자=나폴레옹
- 주장 한계: 구체 이각모 실물과 착용 방향 자료가 더 필요하다. 역사 인물 정체·직위는 자동 추가하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S40 · Eighteenth-Century European Dress](https://www.metmuseum.org/essays/eighteenth-century-european-dress)

## J03 · 샤코의 높은 몸체·챙·금속판

높고 어두운 샤코 몸체에 짧은 앞챙이 돌출하고 앞면에는 별도 가장자리를 가진 금속빛 장식판이 붙어 있다.

A tall dark shako body has a short projecting front peak and a separately edged metal-colored plate on its front surface.

- 처리 제안: new / P1; 역할: prop, object_structure
- 관계: peak → projects_from → body; plate → on_front_of → body
- 혼동: 높은 top hat/모든 샤코에 같은 깃털·민병대 문맥
- 주장 한계: 특정 소장 예의 plate/peak 구별만 참고한다. 국가·계급·장식 문양은 별도 요청과 원전이 필요하다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S49 · 1812-pattern Shako, c1813](https://collection.nam.ac.uk/detail.php?acc=1966-08-4-3)

## J04 · 코티의 짧은 앞자락과 뒤 꼬리

전시 마네킹의 코티를 옆에서 보아 짧은 앞 밑단과 그보다 긴 별도 가장자리의 뒤 옷자락을 보여 준다.

A side view of a coatee on a dress form shows its short front hem and longer separately edged rear tails.

- 처리 제안: defer / P1; 역할: garment_detail, silhouette_proportion
- 관계: front → part_of → coat; tails → behind → front
- 혼동: 프록코트의 긴 전체 치마/앞뒤 대칭 재킷
- 주장 한계: short-tailed의 특정 형상을 도판으로 확인하기 전 보류한다. 모든 coatee 길이가 같지는 않다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S50 · Officer’s short-tailed coatee, c1815](https://collection.nam.ac.uk/detail.php?acc=1963-09-286-1)

## J05 · 고젯은 목 아래 별도 현수 금속판

초승달 모양 금속빛 고젯이 양 끝 구멍 두 개를 지나는 별도 끈에 매달려 코트 가슴 앞에 놓여 있다.

A crescent-shaped metal-colored gorget hangs in front of a coat chest from a separate cord passing through its two end holes.

- 처리 제안: new / P1; 역할: wearable_accessory, contact_point
- 관계: holes → in → plate; cord → through → holes; plate → in_front_of → coat
- 혼동: 갑옷 목받침과 융합/작은 장식=실제 방어·계급
- 주장 한계: 양 끝 구멍과 끈은 구체 실현 선택이다. 문장·문구·직위는 요청·자료와 별도 대조한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S51 · Gorget, East India Company, 1798–1799](https://collection.nam.ac.uk/detail.php?acc=1986-12-33-1)

## J06 · 코트 안의 별도 열린 조끼

겉코트 안에서 앞이 열린 별도 조끼가 보이고 조끼의 고유 앞 가장자리가 코트 라펠과 구별된다.

A separate open-front waistcoat remains visible inside an outer coat, with its own front edges distinct from the coat lapels.

- 처리 제안: refine / P1; 역할: wardrobe_layering, garment_detail
- 관계: waistcoat → inside → coat; edge → part_of → waistcoat
- 혼동: 재킷에 붙은 조끼형 패널/현대 three-piece 전체 강제
- 주장 한계: 독립 조끼와 붙박이 앞패널을 구별한다. 조끼만으로 18세기·남성 정체·귀족 신분을 확정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S40 · Eighteenth-Century European Dress](https://www.metmuseum.org/essays/eighteenth-century-european-dress), [S48 · Europe 1600–1815: City & Commerce audio transcript](https://www.vam.ac.uk/audioguide/europeaudio/tour/5/)

## J07 · 무릎바지 끝과 별도 스타킹

마네킹의 무릎바지가 무릎 부근에서 끝나고 양 밑단 아래로 별도 스타킹 천이 이어진다.

Knee-length breeches on a mannequin end near the knees, with separate stocking fabric continuing below both hems.

- 처리 제안: defer / P1; 역할: garment_detail, contact_point
- 관계: hem → near → knees; stockings → below → hem
- 혼동: 현대 긴 바지/스타킹을 피부·바지와 융합
- 주장 한계: 정확한 연도·단추·길이 변형은 개별 실물 자료가 필요하여 보류한다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S40 · Eighteenth-Century European Dress](https://www.metmuseum.org/essays/eighteenth-century-european-dress)

## J08 · 크라바트의 목 감김과 앞 매듭

목천이 마네킹 목을 감싸 앞 매듭에서 만나고 별도 가장자리의 천 끝 두 개가 아래로 내려온다.

A neckcloth wraps around a mannequin neck and meets at a front knot with two separately edged cloth ends.

- 처리 제안: defer / P1; 역할: garment_detail, wearable_accessory
- 관계: cloth → around → neck; knot → in_front_of → neck; ends → descend_from → knot
- 혼동: 주름 러프/현대 넥타이/목 졸림 자동 의미
- 주장 한계: 매듭의 시대별 실물 검토가 필요하다. 목천은 강제·성적 의미·조임 정도의 증거가 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S40 · Eighteenth-Century European Dress](https://www.metmuseum.org/essays/eighteenth-century-european-dress)

## J09 · 스테이즈·슈미즈의 층과 몸판

의복 전시 마네킹에서 별도의 밝은 슈미즈 바깥에 구조적인 스테이즈 몸판이 있고 몸판 패널 위에는 길고 좁은 케이싱이 보인다.

A dress-form display shows a structured stays bodice over a separate light chemise, with long narrow casings on the bodice panels.

- 처리 제안: defer / P1; 역할: wardrobe_layering, garment_detail
- 관계: stays → outside → chemise; casings → on → stays
- 혼동: 후기 hourglass corset/겉 케이싱=내부 보강재 성분
- 주장 한계: V&A는 층을 설명한다. 정확한 케이싱·보강재·silhouette는 개별 실물 확인 전 보류한다. 신체 압박·성적 의미는 자동 판정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S40 · Eighteenth-Century European Dress](https://www.metmuseum.org/essays/eighteenth-century-european-dress), [S48 · Europe 1600–1815: City & Commerce audio transcript](https://www.vam.ac.uk/audioguide/europeaudio/tour/5/)

## J10 · 파니에의 지지 구조와 겉치마 실루엣

의복 전시 마네킹에 좌우로 뻗은 후프 받침을 노출하고 앞뒤 깊이가 좌우 폭보다 좁게 보인다.

A dress-form display exposes a hoop support extending to the left and right, with the support’s front-to-back depth visibly narrower than its lateral width.

- 처리 제안: defer / P1; 역할: object_structure, silhouette_proportion
- 관계: support → around → form; left → part_of → support; right → part_of → support
- 혼동: 겉치마의 넓은 silhouette=숨은 후프 구조 직접 증명
- 주장 한계: 특정 지지 구조의 도판 검토 전 보류한다. 기존 겉치마 폭 관계는 재사용할 수 있어도 내부 받침의 증거는 아니다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S30 · Robe à la française, ca. 1780](https://www.metmuseum.org/art/collection/search/159432), [S48 · Europe 1600–1815: City & Commerce audio transcript](https://www.vam.ac.uk/audioguide/europeaudio/tour/5/)

## J11 · 엠파이어의 가슴 아래 이음선

드레스 치마가 가슴 바로 아래에서 몸판에 이어지고 그 높인 이음선으로부터 아래로 내려온다.

A dress skirt joins its bodice directly below the bust and falls downward from that raised seam.

- 처리 제안: refine / P1; 역할: garment_detail, silhouette_proportion
- 관계: skirt → joined_at → seam; bodice → meets → seam; seam → below → bust
- 혼동: 자연 허리선/Empire라는 정치 체제와 동일시
- 주장 한계: 기존 같은 관계 source를 재사용 검토한다. 신체 정체·계급·정치적 제국·역사 연도를 이음선만으로 판정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S31 · Shirt dress and spencer](https://www.cultura.gob.es/mtraje/en/visita/visita-virtual/afrancesados-burgueses/clasicismo-burguesia-1/vestido-camisa-spencer.html), [S40 · Eighteenth-Century European Dress](https://www.metmuseum.org/essays/eighteenth-century-european-dress)

## J12 · 가면의 얼굴·끈 경계

성인 가면무도회 참가자가 별도 가장자리의 눈가면을 착용하고 묶는 끈은 머리카락·얼굴과 구별된다.

An adult masquerade attendee wears a separately edged eye mask, with its ties distinct from the hair and face.

- 처리 제안: new / P1; 역할: wearable_accessory, contact_point
- 관계: mask → in_front_of → face; ties → attached_to → mask; face → part_of → adult
- 혼동: 가면=성적 익명성·기만·실제 신분 은닉 확정
- 주장 한계: 참가라는 역할은 선언된 문맥이다. 성별 정체·연애·동의·왕실 관계는 외형으로 추론하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S41 · Madame de Pompadour](https://en.chateauversailles.fr/discover/history/great-characters/madame-pompadour), [S48 · Europe 1600–1815: City & Commerce audio transcript](https://www.vam.ac.uk/audioguide/europeaudio/tour/5/)

## J13 · 부두아르·옆 침실의 공간 경계

거울을 둔 화장 탁자가 문 곁에 있고 문 너머의 별도 공간에 침대가 놓인다.

A dressing table with its mirror stands beside a doorway, with a bed in the separate space beyond.

- 처리 제안: reuse / P1; 역할: location, spatial_depth
- 관계: mirror → on → table; table → beside → doorway; bed → beyond → doorway
- 혼동: 부두아르=침실=성매매 공간/사적 방=관계의 동의
- 주장 한계: 기존 완전 공간 후보를 재사용 검토한다. 가구 배치만으로 방의 역사적 기능·성적 행위·거주자 신분을 확정하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S41 · Madame de Pompadour](https://en.chateauversailles.fr/discover/history/great-characters/madame-pompadour), [S48 · Europe 1600–1815: City & Commerce audio transcript](https://www.vam.ac.uk/audioguide/europeaudio/tour/5/)

## J14 · 기동 구호마차의 바퀴·뒷문·들것

덮개가 있는 두 바퀴 구호마차의 뒷문이 열리고 별도의 들것이 뒤쪽 개구부와 정렬되어 있다.

A covered two-wheeled ambulance wagon has open rear doors with a separate stretcher aligned at the rear opening.

- 처리 제안: defer / P1; 역할: object_structure, contact_point
- 관계: wheels → support → wagon; doors → at_rear_of → wagon; stretcher → aligned_with → doors
- 혼동: flying ambulance=비행체/현대 monitor·엔진 구급차 자동 재사용
- 주장 한계: 구조 도판과 적재 접점은 추가 검토한다. 환자·상처·후송 성공·치료 결과는 자동 추가하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S44 · Medicine and Surgery at Waterloo](https://heritageblog.rcpsg.ac.uk/2015/06/09/medicine-and-surgery-at-the-battle-of-waterloo/)

## J15 · 마이소르 총의 호랑이 머리 cock

박물관 총 표본에서 호랑이 머리 모양 외부 물림쇠가 나무 총상 옆에서 작은 부싯돌을 물고 위쪽에는 별도 장식 총열이 보인다.

A museum gun specimen shows a tiger-head-shaped external cock holding a small flint beside its wooden stock, with a separately decorated barrel above.

- 처리 제안: defer / P1; 역할: object_structure, surface_pattern
- 관계: flint → held_by → cock; cock → beside → stock; barrel → above → stock
- 혼동: 총 자체=살아 있는 호랑이/오스만 miquelet 표본과 혼합
- 주장 한계: 특정 1793–94년 실물의 장식이다. 미세 lock/장식 도판 검토 후 채택하며 모든 남아시아 무기에 일반화하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S45 · Flintlock Blunderbuss, Seringapatam, 1793–94](https://www.metmuseum.org/art/collection/search/24490)

## J16 · 로더넘 소장병과 보이는 표기의 층

유리 마개가 있는 사각 유리병 옆에 "LAUDANUM"이라고 적힌 별도의 박물관 표찰이 놓여 있다.

A square glass bottle with a glass stopper stands beside a separate museum label reading "LAUDANUM".

- 처리 제안: new / P1; 역할: prop, visible_text
- 관계: stopper → in_neck_of → bottle; label → beside → bottle
- 혼동: 라벨/갈색 액체=실제 약물 조성·용량·효능
- 주장 한계: 표찰 문구는 창작 전시 제안이다. 소장 기록의 화학 분류와 새 이미지의 내용물을 구분하고 사용법을 추가하지 않는다.
- 픽셀 gate: 모든 관계의 양끝·접점·방향·수량을 함께 확인. partial_is_fail; UNOBSERVABLE_NOT_PASS.

출처: [S47 · Bottle of Laudanum, 1820–1840](https://collection.sciencemuseumgroup.org.uk/objects/co8345344/bottle-of-laudanum)

## I01 · 장르·서사 규모

장르명은 선택적 탐색 문맥이다. 제복·유럽·총·마법 VFX·어두운 팔레트를 전부 강제하지 않는다.

용어: Flintlock Fantasy, Gunpowder Fantasy, Black Powder Fantasy, Muskets and Magic, Epic Fantasy, Secondary-World Fantasy

출처: [S01 · Django Wexler Collection](https://findingaids.library.tamu.edu/index.php/django-wexler-collection), [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S24 · The Shadow Campaigns](https://djangowexler.com/series/the-shadow-campaigns/)

## I02 · 기술 축·제식 이름·전투 실패

점화/총열/장전 축을 분리한다. 개별 모델 도판과 연대를 명시하며 불발/지연발화는 시간 증거가 필요하다.

용어: Firelock, Smoothbore, Muzzle-loader, Breech-loader, Brown Bess, Charleville, Baker Rifle, Misfire, Hangfire

출처: [S02 · Ignition Systems](https://nij.ojp.gov/nij-hosted-online-training-courses/firearms-examiner-training/module-03/ignition-systems), [S05 · Waterloo 1815](https://royalarmouries.org/objects-and-stories/stories/waterloo-1815)

## I03 · 군 조직·계급·군기·사기

군복·군기에서 조직의 정원·계급·충성·사기·명예를 자동 추론하지 않는다. 척탄병에게 수류탄을 항상 붙이지 않는다.

용어: Grenadier, Fusilier, Guards, NCO, Aide-de-camp, Company, Battalion, Regiment, Colours, Standards, Morale, Esprit de Corps

출처: [S06 · Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles), [S16 · Battle of Waterloo 1815, MPH 1/387/3](https://www.nationalarchives.gov.uk/education/resources/significant-events/battle-of-waterloo-1815/)

## I04 · 작전·전술·정보·시간

공간 배치와 연속 행위/지휘/결과를 분리한다. 연기=전장의 불확실성이라는 인과를 단정하지 않는다.

용어: Volley Fire, Platoon Fire, Drill, Bayonet Charge, Combined Arms, Enfilade, Fog of War, Guerrilla Warfare

출처: [S05 · Waterloo 1815](https://royalarmouries.org/objects-and-stories/stories/waterloo-1815), [S15 · Napoleonic warfare](https://exhibitions.lib.cam.ac.uk/waterloo/case/napoleonic-warfare/), [S16 · Battle of Waterloo 1815, MPH 1/387/3](https://www.nationalarchives.gov.uk/education/resources/significant-events/battle-of-waterloo-1815/)

## I05 · 포병 탄종의 추가 원전 필요

canister/포도탄/유산탄을 합치지 않는다. 직접 시대별 도판을 확보한 뒤 물건별 실현을 분리한다. 현대 휴대 박격포를 대입하지 않는다.

용어: Grapeshot, Chain Shot, Mortar, Howitzer, Siege Artillery, Redoubt, Sapping, Siege Works

출처: [S10 · Artillery – Types of Rounds](https://www.nps.gov/fosc/learn/education/artshot.htm), [S11 · A Rusty Shrapnel Round](https://en.rcamuseum.com/a-rusty-shrapnel-round/), [S12 · Bastion](https://sites-vauban.org/en/resources/glossary/bastion), [S18 · Bar shot KTP1022](https://www.rmg.co.uk/collections/objects/rmgc-object-36875)

## I06 · 해군의 허가·나포·봉쇄·강제징모

문서·깃발·억제된 몸짓은 허가의 진위·노예/포로 신분·강제·봉쇄 효과를 증명하지 않는다.

용어: Privateer, Letter of Marque, Prize, Prize Money, Impressment, Press Gang, Blockade, Weather Gauge

출처: [S19 · Privateers](https://www.history.navy.mil/our-collections/art/exhibits/conflicts-and-operations/the-war-of-1812/privateers.html), [S38 · Teacher’s Highlights: HMS Victory](https://www.nmrn.org.uk/sites/default/files/2022-09/PHD-Teachers-Highlights-FINAL.pdf)

## I07 · 국가·혁명·신분·권위

왕관·리본·군중·단두대는 제도/사상/사건 성공의 직접 증거가 아니다. 구체 공고와 서사 주장을 별도 저장한다.

용어: Ancien Régime, Absolutism, Divine Right, Estates, Privilege, Bourgeoisie, Constitutional Monarchy, Republicanism, Revolution, Counterrevolution, Coup d’État, Levée en Masse

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S26 · Cap, ca. 1790](https://www.metmuseum.org/art/collection/search/689887), [S36 · Pendants d’oreilles à la guillotine](https://www.carnavalet.paris.fr/collections/pendants-doreilles-la-guillotine)

## I08 · 회사·재정·독점·수탈·토지

장부·농장·피부·제복에서 식민 지배·재산권·부채·이익·강제노동의 진위를 확정하지 않는다. 각 개념의 전문 원전 보완이 필요하다.

용어: Chartered Company, Company Army, Mercantilism, Colonialism, Extractive Economy, Plantation Economy, Fiscal-Military State, Public Debt, War Finance, Patronage, Purchase of Commissions, Enclosure, Commons, War Profiteering

출처: [S25 · Armies of the East India Company](https://www.nam.ac.uk/explore/armies-east-india-company), [S28 · History](https://www.bankofengland.co.uk/about/history)

## I09 · 노예제·노예무역·폐지·포로

역사 제도와 알려진 유물 provenance를 보존한다. 새 사람의 피부·족쇄·노동 자세만으로 법적 신분·동의·범죄·해방을 추정하지 않는다.

용어: Slavery, Slave Trade, Abolitionism, Captivity, Forced Labour

출처: [S25 · Armies of the East India Company](https://www.nam.ac.uk/explore/armies-east-india-company), [S33 · Leg-irons ZBA2471](https://www.rmg.co.uk/collections/objects/rmgc-object-254405), [S34 · Set of wrought iron leg shackles](https://nmaahc.si.edu/object/nmaahc_2008.10.2)

## I10 · 성매매·살롱·밀통·권력과 성

용어를 삭제하지 않되 구체 역사어 검토 전 의미를 합치지 않는다. 성인·직업·대가·관계·동의는 의복/돈/침대/군영에서 자동 판정하지 않는다.

용어: Prostitution, Brothel, Courtesan, Mistress, Sexual Patronage, Sexual Relationship

출처: [S20 · Camp Followers](https://www.amrevmuseum.org/virtualexhibits/picturing-washington-s-army/pages/campfollowers), [S32 · Hogarth: 101](https://www.soane.org/features/hogarth-101)

## I11 · 전시 성폭력·강제·매혹

연구 문맥의 중대한 사건/동의 개념이다. 자세·노출·눈동자·빛으로 동의나 강제 원인을 확정하지 않는다. 장르→자동 성적 시각 대안을 만들지 않는다.

용어: Wartime Sexual Violence, Sexual Coercion, Charm, Compulsion, Consent

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S24 · The Shadow Campaigns](https://djangowexler.com/series/the-shadow-campaigns/), [S32 · Hogarth: 101](https://www.soane.org/features/hogarth-101)

## I12 · 처형·고문·학살·신체 훼손

장비·상처·전후 흔적과 원인·의도·시점·사망을 분리한다. 기구 원전은 실제 사건/정도/임상 결과의 증거가 아니다. 직접 사건별 원전 연구는 후속 과제다.

용어: Execution, Guillotine, Firing Squad, Flogging, Torture, Massacre, Dismemberment, Amputation

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S35 · Benjamin Bell-type metacarpal amputation saw](https://collection.sciencemuseumgroup.org.uk/objects/co167835/benjamin-bell-type-metacarpal-amputation-saw-europe-1780-1850), [S36 · Pendants d’oreilles à la guillotine](https://www.carnavalet.paris.fr/collections/pendants-doreilles-la-guillotine)

## I13 · 지식·종교·검열·정치 담론

모임·책·실험기구·성당은 발화 내용/사상/종교적 정체의 증거가 아니다. 교단·철학별 설명 원전은 추가 필요하다.

용어: Salon, Censorship, Natural Philosophy, Learned Society, Academy, State Church, Religious Dissent, Deism, Enlightenment

출처: [S27 · The Popularity of Broadsides](https://www.loc.gov/static/collections/broadsides-and-other-printed-ephemera/articles-and-essays/introduction-to-printed-ephemera-collection/the-popularity-of-broadsides.html), [S32 · Hogarth: 101](https://www.soane.org/features/hogarth-101), [S37 · Life in a cup: coffee culture in the Islamic world](https://www.britishmuseum.org/exhibitions/life-cup-coffee-culture-islamic-world)

## I14 · 서사 속 비가시 마법 제도

매개·효과·소유자·대상은 구체 창작안으로 분리한다. 효능·독점·의식·예언 적중·정신 조작·동의는 이미지로 입증하지 않는다.

용어: Powder Mage, Magical Monopoly, Magical Arms Race, Countermagic, Antimagic, Ritual Artillery, Weather Magic, Scrying, Divination, Healing Magic, Alchemy, Military Necromancy

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S24 · The Shadow Campaigns](https://djangowexler.com/series/the-shadow-campaigns/), [S39 · His Majesty’s Dragon](https://www.penguinrandomhouse.com/books/122950/his-majestys-dragon-by-naomi-novik/)

## I15 · 인접 장르·독립 시대·미학

서사·시대·기술·미학·비평 관점을 동일 시각 태그로 묶지 않는다. 플린트록이라는 말로 증기·다른 지역·환한 낮을 무조건 배제하지 않는다.

용어: Early Modern Fantasy, Napoleonic Fantasy, Military Fantasy, Historical Fantasy, Alternate-History Fantasy, Swashbuckling Fantasy, Nautical Fantasy, Pirate Fantasy, Gaslamp Fantasy, Steampunk, Clockpunk, Grimdark, Revolutionary Fantasy, Postcolonial Fantasy, Baroque, Neoclassicism

출처: [S01 · Django Wexler Collection](https://findingaids.library.tamu.edu/index.php/django-wexler-collection), [S29 · The Rococo style – an introduction](https://www.vam.ac.uk/articles/the-rococo-style-an-introduction), [S31 · Shirt dress and spencer](https://www.cultura.gob.es/mtraje/en/visita/visita-virtual/afrancesados-burgueses/clasicismo-burguesia-1/vestido-camisa-spencer.html)

## I16 · 민간 보급·군영 거래·불법 유통

가시 노동·도구·운송과 계약·징발·불법·약탈·직업·가족 관계를 분리한다. 각 국가의 세부 제도는 추가 원전 대기다.

용어: Commissariat, Supply Depot, Arsenal, Armoury, Requisition, Foraging, Rations, Fodder, Billeting, Camp Followers, Sutler, Vivandière, Cantinière, Smuggling, Black Market

출처: [S20 · Camp Followers](https://www.amrevmuseum.org/virtualexhibits/picturing-washington-s-army/pages/campfollowers), [S21 · The Army Laundress](https://www.nps.gov/articles/000/the-army-laundress.htm), [S25 · Armies of the East India Company](https://www.nam.ac.uk/explore/armies-east-india-company)

## I17 · 궁정 관계·퀴어 사교·정체·비방

행위·역할·제도·성별 표현·정체·동의·풍자 내용을 분리한다. 몰리 하우스를 성매매 업소로 축소하지 않고 정부의 조언/후원 역할과 시기 변화도 보존한다. 재생산 강제는 현대 분석어다.

용어: Libertine, Libertinism, Rake, Royal Mistress, Molly House, Gender Disguise, Arranged Marriage, Dowry, Adultery, Legitimacy, Sexual Double Standard, Erotic Libel, Political Pornography, Reproductive Coercion, Court Etiquette

출처: [S32 · Hogarth: 101](https://www.soane.org/features/hogarth-101), [S41 · Madame de Pompadour](https://en.chateauversailles.fr/discover/history/great-characters/madame-pompadour), [S42 · Molly houses & queer subculture in Georgian London](https://www.londonmuseum.org.uk/blog/molly-houses-queer-subculture-georgian-london/)

## I18 · 전쟁 피해·군율·의학·현대 분석어

피해와 가해 원인/지휘/의도를 구별한다. flying ambulance의 비행 오독을 막고 질병·도덕적 손상·트라우마는 외형 진단하지 않는다. 현대 분석어와 당시 언어도 구별한다.

용어: Sack, Pillage, Atrocity, Collective Reprisal, Corporal Punishment, Court-Martial, Desertion, Mutiny, Duel, Code of Honour, Public Execution, Siege Famine, Field Hospital, Flying Ambulance, Gangrene, Wound Infection, Laudanum, Camp Disease, War Trauma, Moral Injury, Body Horror, Posthumous Exploitation

출처: [S43 · Peninsular War](https://www.nam.ac.uk/explore/peninsular-war), [S44 · Medicine and Surgery at Waterloo](https://heritageblog.rcpsg.ac.uk/2015/06/09/medicine-and-surgery-at-the-battle-of-waterloo/), [S47 · Bottle of Laudanum, 1820–1840](https://collection.sciencemuseumgroup.org.uk/objects/co8345344/bottle-of-laudanum)

## I19 · 지역 계보·기술 이전·혼합 무장

같은 시대·피부·복장으로 같은 점화 체계/군적을 강제하지 않는다. 오스만·마이소르·동아시아 원전을 개별 유지하며 장인/문서/부품의 이동은 이력/제도 정보다.

용어: Ottoman Firearms, Mysorean Armouries, Sepoy, Matchlock East Asia, Technology Transfer, Hybrid Arsenal

출처: [S03 · Miquelet Gun, 1784–85](https://www.metmuseum.org/art/collection/search/30605), [S25 · Armies of the East India Company](https://www.nam.ac.uk/explore/armies-east-india-company), [S45 · Flintlock Blunderbuss, Seringapatam, 1793–94](https://www.metmuseum.org/art/collection/search/24490), [S46 · 조총과 홍이포: 화약무기의 시대를 열다](https://contents.history.go.kr/front/kc/printViewPopup.do?levelId=kc_i305630)

## I20 · 대표작·연관작은 독립된 참고 체계

작품 소개/용어집과 역사 기술 사료를 구별한다. 고유 주인공·인종/종교 대응·마법 규칙·색채·게임 제목을 장르 공통 시각 사실로 합치지 않는다. 소설 전문/게임 플레이는 미검토다.

용어: 《Powder Mage》, 《The Shadow Campaigns》, 《Guns of the Dawn》, 《Temeraire》, 《Lightbringer》, 《The Age of Unreason》, 《On Stranger Tides》, 《GreedFall》, 《Flintlock: The Siege of Dawn》

출처: [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S24 · The Shadow Campaigns](https://djangowexler.com/series/the-shadow-campaigns/), [S39 · His Majesty’s Dragon](https://www.penguinrandomhouse.com/books/122950/his-majestys-dragon-by-naomi-novik/), [S52 · Guns of the Dawn](https://www.panmacmillan.com/authors/adrian-tchaikovsky/guns-of-the-dawn/9781509864614), [S53 · Lightbringer Glossary](https://www.brentweeks.com/extras/lightbringer-extras/lightbringer-glossary/), [S54 · Newton’s Cannon catalog record](https://egrove.olemiss.edu/mwp_books/230/), [S55 · On Stranger Tides](https://subterraneanpress.com/on-stranger-tides/), [S56 · GreedFall, E3 2018 story trailer article](https://www.focus-entmt.com/en/news/e3-2018-greedfall-paints-the-genesis-of-the-games-story-in-e3-trailer), [S57 · Flintlock: The Siege of Dawn](https://www.playstation.com/en-tw/games/flintlock-the-siege-of-dawn/)

## I21 · 장르 조합의 창작 의도와 가시 장면

원문 17절은 창작 조합이지 독립된 장르의 공식 taxonomy가 아니다. 새 인물·폭력·성적 의미·신분·기계·마법을 자동 활성화하지 않고 장면 전체 관계와 core를 먼저 결정한다.

용어: Flintlock Fantasy × Gothic Horror, Flintlock Fantasy × Cosmic Horror, Flintlock Fantasy × Medical Horror, Flintlock Fantasy × Clockpunk, Flintlock Fantasy × Decadent Aesthetic, Flintlock Fantasy × Political Thriller, Flintlock Fantasy × Cozy Fantasy, Flintlock Fantasy × Posthuman Fiction

출처: [S01 · Django Wexler Collection](https://findingaids.library.tamu.edu/index.php/django-wexler-collection), [S23 · Promise of Blood](https://www.brianmcclellan.com/promise-of-blood), [S24 · The Shadow Campaigns](https://djangowexler.com/series/the-shadow-campaigns/), [S39 · His Majesty’s Dragon](https://www.penguinrandomhouse.com/books/122950/his-majestys-dragon-by-naomi-novik/)

