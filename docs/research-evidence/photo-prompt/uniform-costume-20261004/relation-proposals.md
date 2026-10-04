# 시각 관계 보강 초안

83개는 추가 런타임 레코드 수가 아니다. 기존 관계 재사용·근거 있는 관계 초안·검증 대기·선택 디자인을 합친 연구 백로그다.

상태·소유·구성 요소·속성 매핑 제안은 [relation-proposals.json](relation-proposals.json), 비교 풀은 [bundle-proposals.json](bundle-proposals.json)에 있다. 속성 경로와 관계 type의 런타임 적합성은 미검증이다.

## U01 — 몸판과 소매의 배색 경계

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the robe body separate from the contrasting sleeves`.
- 관찰 1: The body is one continuous color area below the armhole.
- 관찰 2: A different sleeve color begins at the selected armhole or sleeve boundary.
- 혼동 경계: 동다리의 모든 연대를 한 배색으로 고정한 긴 코트
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S03](https://encykorea.aks.ac.kr/Article/E0066034). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U02 — 소매 없는 전복이 안쪽 소매 위에 겹침

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the sleeveless outer robe layered over the inner long-sleeved robe`.
- 관찰 1: The outer robe has open armholes rather than its own sleeves.
- 관찰 2: The inner sleeves emerge through those armholes and belong to the same wearer.
- 혼동 경계: 소매 달린 겉두루마기 또는 식재료 전복
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S02](https://encykorea.aks.ac.kr/Article/E0049431). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U03 — 철릭의 상의와 주름 하의가 허리에서 연결됨

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the robe upper body connected to the pleated lower robe at the waist`.
- 관찰 1: A visible waist join separates the upper body from the lower folds.
- 관찰 2: The pleated lower cloth continues from that same join.
- 혼동 경계: 독립된 치마를 코트 아래에 입은 조합
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S01](https://encykorea.aks.ac.kr/Article/E0056124). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U04 — 선택된 철릭 소매의 탈착 경계

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the detachable sleeve connected to the upper robe attachment edge`.
- 관찰 1: The selected sleeve has its own attachment edge.
- 관찰 2: A fastening or separation boundary is visible at that edge rather than only a decorative seam.
- 혼동 경계: 모든 철릭에 탈착 소매를 부과하거나 숨은 여밈을 보였다고 판정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S01](https://encykorea.aks.ac.kr/Article/E0056124). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U05 — 가슴 브레이드의 양끝이 같은 재킷에 붙음

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the repeated chest braids attached to the same jacket front`.
- 관찰 1: Each selected braid has visible front attachment points.
- 관찰 2: The braid crosses between those points on the same jacket.
- 혼동 경계: 공중에 떠 있는 끈 또는 옆 사람의 견장 끈
- 재사용 우선 ID: ccx_cc05_02, costume_ccx_cc05_02.
- 근거/반례 탐색 위치: [S04](https://www.nam.ac.uk/explore/cavalry-roles). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U06 — 어깨에 걸친 펠리스의 빈 소매와 고정끈

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the fur-edged short coat draped over one shoulder of the inner-jacket wearer`.
- 관찰 1: A separate short coat rests on one shoulder above the inner jacket.
- 관찰 2: Its hanging sleeve is unoccupied and the support cord belongs to the coat.
- 혼동 경계: 양팔을 모두 끼운 모피 재킷이나 어깨 위 모피 스톨
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S04](https://www.nam.ac.uk/explore/cavalry-roles). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U07 — 차프카의 각진 윗판과 별도 챙

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the four-cornered cap top connected to the lower cap body above its brim`.
- 관찰 1: The top has a distinct four-corner outline.
- 관찰 2: A separate lower body and brim remain below the angular top.
- 혼동 경계: 원통 샤코나 단순 사각 학사모
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S05](https://collection.nam.ac.uk/detail.php?acc=1978-02-37-91). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U08 — 플라스트론 앞판이 튜닉 몸판 안에 놓임

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the contrasting chest plastron attached to the front of the selected tunic`.
- 관찰 1: A bounded chest panel belongs to the tunic front.
- 관찰 2: The panel edge remains inside the body rather than becoming a separate vest.
- 혼동 경계: 출처가 확인되지 않은 연대 배색을 모든 창기병에 적용
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S05](https://collection.nam.ac.uk/detail.php?acc=1978-02-37-91). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U09 — 주아브 재킷에 붙은 가짜 조끼 앞판

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the false vest panel attached to the short jacket`.
- 관찰 1: The vest-like front panel is joined to the jacket construction.
- 관찰 2: Its boundary does not establish an independently worn inner waistcoat.
- 혼동 경계: 별도 조끼를 필수로 추가한 삼중 겹침
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S06](https://www.metmuseum.org/art/collection/search/151912). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U10 — 넓은 바지통이 발목의 좁은 경계로 모임

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the full trouser legs gathered into the narrow lower-leg boundary`.
- 관찰 1: Each leg has visible excess width above the lower leg.
- 관찰 2: That same cloth narrows toward the selected ankle or gaiter boundary.
- 혼동 경계: 넓은 치마 한 장 또는 모든 주아브복의 발목 주름 강제
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S06](https://www.metmuseum.org/art/collection/search/151912). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U11 — 높은 모피 모자가 머리 위에 독립된 부피를 가짐

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the tall fur-textured cap worn by the tunic wearer`.
- 관찰 1: The cap has a tall continuous outer volume above the head.
- 관찰 2: Its lower edge sits on the same wearer rather than merging with hair.
- 혼동 경계: 검은 머리카락을 베어스킨으로 판정하거나 모든 연대에 깃털 추가
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S60](https://www.army.mod.uk/news/scots-guards-fond-farewell-to-hrh-the-duke-of-kent/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U12 — 킬트 앞의 스포런이 허리에서 별도로 매달림

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the sporran pouch suspended from the waist belt in front of the kilt`.
- 관찰 1: A distinct pouch has its own outline in front of the kilt.
- 관찰 2: A belt or chain supports it at the same wearer's waist.
- 혼동 경계: 타탄 주름치마만으로 특정 하이랜드 연대와 스포런을 확정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S05](https://collection.nam.ac.uk/detail.php?acc=1978-02-37-91). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U13 — 짧은 야전 상의 밑단이 별도 하의 허리에 닿음

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the short field blouse hem meets the separate trouser waist`.
- 관찰 1: The upper garment ends at a visible hem near the waist.
- 관찰 2: Separate trousers continue beneath that hem.
- 혼동 경계: 일체형 커버올 또는 모든 시대 야전복의 공통 재단으로 확대
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S07](https://collection.nam.ac.uk/detail.php?acc=1992-02-33--24). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U14 — 선택된 역사 표식의 부착 위치와 바탕 면

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the requested historical insignia attached to its specified garment or cap carrier`.
- 관찰 1: The requested emblem has a bounded visible shape.
- 관찰 2: Its placement is tied to the selected sleeve band, collar tab or cap rather than floating nearby.
- 혼동 경계: 검은 제복만으로 SS를 추론하거나 요청된 유물 표식을 임의의 판타지 문양으로 바꿈
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S08](https://www.nmm.nl/nl/stories/uniform-hugo-boss/), [S09](https://samlinger.natmus.dk/khs/object/60162). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U15 — AGSU의 코트·셔츠·하의 배색이 각 부품에 귀속됨

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the green service coat layered over the tan shirt above taupe trousers`.
- 관찰 1: The green outer coat remains distinct from the tan shirt at its opening.
- 관찰 2: The trousers form a separate taupe lower garment on the same wearer.
- 혼동 경계: 상의·셔츠·하의를 모두 같은 녹색으로 칠한 군복
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S11](https://www.peosoldier.army.mil/Equipment/Equipment-Portfolio/Project-Manager-Soldier-Survivability-Portfolio/Army-Green-Service-Uniform/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U16 — 청색 정복 외피와 흰 셔츠의 경계

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the blue service coat layered over the white shirt`.
- 관찰 1: The blue coat has its own lapel or front opening.
- 관찰 2: The white shirt is visible within that opening rather than recoloring the coat.
- 혼동 경계: ASU와 AGSU의 색을 혼합하거나 모든 바지에 금색 줄을 강제
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S12](https://www.peosoldier.army.mil/Equipment/Equipment-Portfolio/Project-Manager-Soldier-Survivability-Portfolio/Army-Service-Uniform/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U17 — 전투복 여밈과 몸판 주머니가 별도 기능 면을 이룸

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the utility pockets attached to the jacket body beside its front closure`.
- 관찰 1: The front closure follows the jacket's center axis.
- 관찰 2: The selected pocket openings lie on the body and do not become printed camouflage shapes.
- 혼동 경계: 카모 무늬만으로 주머니·여밈·계급·성능이 충족됐다고 판정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S13](https://www.peosoldier.army.mil/Equipment/Equipment-Portfolio/Project-Manager-Soldier-Survivability-Portfolio/Army-Combat-Uniform/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U18 — 같은 재단 위에 놓인 선택 위장 무늬

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `surface_material`.
- 방향 관계: `the selected camouflage shapes distributed across the garment panels`.
- 관찰 1: Pattern areas lie within cloth panels and continue across the selected seams.
- 관찰 2: Their scale and colors follow one chosen pattern version.
- 혼동 경계: ACU 재단과 OCP 무늬를 한 동의어로 취급하거나 봄·가을 양면을 동시에 표시
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S10](https://www.awm.gov.au/collection/C106357), [S13](https://www.peosoldier.army.mil/Equipment/Equipment-Portfolio/Project-Manager-Soldier-Survivability-Portfolio/Army-Combat-Uniform/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U19 — 세일러 칼라가 어깨에서 직사각 등판으로 이어짐

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the sailor collar continues onto the upper back panel`.
- 관찰 1: The collar spreads across both shoulders of one wearer.
- 관찰 2: Its rear portion has a distinct broad panel rather than a narrow shirt collar.
- 혼동 경계: V넥 리본만으로 세일러 칼라를 충족하거나 군인·학생 신분 자동 부여
- 재사용 우선 ID: ccx_cc03_01, costume_ccx_cc03_01, clothing_ct041_v2.
- 근거/반례 탐색 위치: [S56](https://www.history.navy.mil/research/library/online-reading-room/title-list-alphabetically/u/uniforms-usnavy/historical-surveys-of-the-evolution-of-us-navy-uniforms.html), [S61](https://kanko-gakuseifuku.co.jp/media/parents/purchase). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U20 — 1859 청색 프록의 깃·커프스가 몸판과 같은 계열임

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the collar and cuffs share color with the blue frock body`.
- 관찰 1: The visible collar is blue without the earlier white applied collar.
- 관찰 2: The visible cuff edges remain blue rather than added white cuffs.
- 혼동 경계: 1841의 흰 덧깃을 1859 이후 기본형에도 필수로 유지
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S56](https://www.history.navy.mil/research/library/online-reading-room/title-list-alphabetically/u/uniforms-usnavy/historical-surveys-of-the-evolution-of-us-navy-uniforms.html). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U21 — 바지통이 무릎 아래에서 넓어지는 하단 윤곽

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the lower trouser legs widen toward their separate hems`.
- 관찰 1: Each trouser leg remains a separate tube below the knee.
- 관찰 2: Its hem is wider than the selected knee region.
- 혼동 경계: 모든 수병복·교복에 벨보텀을 강제하거나 긴 치마로 대체
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S56](https://www.history.navy.mil/research/library/online-reading-room/title-list-alphabetically/u/uniforms-usnavy/historical-surveys-of-the-evolution-of-us-navy-uniforms.html). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U22 — 노퍽 재킷의 세로 주름을 가로 벨트가 감쌈

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the coat waist belt crosses over the vertical coat pleats`.
- 관찰 1: Visible pleat lines descend along the selected coat panels.
- 관찰 2: A separate belt encircles that same coat at waist level.
- 혼동 경계: 1917 여성 사무병복을 짧은 세일러 미니드레스로 바꿈
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S57](https://www.history.navy.mil/research/library/online-reading-room/title-list-alphabetically/w/womens-uniform-1918.html). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U23 — 직물 일체형 비행복의 앞지퍼와 별도 지퍼 주머니

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the front zipper runs along the fabric coverall body`.
- 관찰 1: A single fabric body continues from torso into separate trouser legs.
- 관찰 2: The main zipper is distinct from selected pocket zippers on that body.
- 혼동 경계: 항공 조종사 셔츠·바지 또는 헬멧 연결 압력복과 합침
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S15](https://airandspace.si.edu/collection-objects/suit-flying-type-k-2b-united-states-air-force/nasm_A19790546000). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U24 — 조종사 셔츠 견장과 흉장 표식의 위치 분리

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the shirt shoulder tabs attached to the shoulders above a separate chest badge`.
- 관찰 1: The tabs sit on the selected shirt's shoulders.
- 관찰 2: A requested wing badge occupies the chest independently of the shoulder tabs.
- 혼동 경계: 항공사·계급 확인 없이 네 줄 견장·흰 모자·윙 배지를 필수화
- 재사용 우선 ID: ccx_cc05_01, costume_ccx_cc05_01.
- 근거/반례 탐색 위치: [S18](https://airandspace.si.edu/collection-objects/cap-pilot-northwest-airlines/nasm_A20060603000). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U25 — 헬멧 경계가 압력복 몸체의 목 연결부에 닿음

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the integrated helmet edge connected to the suit neck assembly`.
- 관찰 1: The helmet and visor have visible enclosing boundaries around the head.
- 관찰 2: The lower helmet boundary meets the suit's neck assembly rather than a simple open shirt collar.
- 혼동 경계: 청색 NASA 훈련복이라는 이유로 압력복 헬멧을 추가하거나 보호 성능을 픽셀로 입증
- 재사용 우선 ID: ccx_cc13_01, ccx_cc13_02.
- 근거/반례 탐색 위치: [S17](https://www.nasa.gov/blogs/commercialcrew/2024/05/06/nasas-boeing-crew-flight-test-astronauts-suiting-up-2/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U26 — 스위스 갈라복의 세 배색이 한 외피의 분할 면에 놓임

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected colored garment sections belong to the same gala garment`.
- 관찰 1: Red, yellow and blue areas remain assigned to the selected garment sections.
- 관찰 2: Their borders follow one wearer's garment rather than a background flag.
- 혼동 경계: 배경의 삼색만으로 갈라복을 충족하거나 모든 소매 재단을 추정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S19](https://schweizergarde.ch/fileadmin/files/Kasernenstiftung/SPENDENBROSCHUERE_SCHWEIZERGARDE_I.pdf). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U27 — 흉갑이 직물 갈라복과 목 러프 바깥에 겹침

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the ceremonial breastplate layered over the cloth uniform below its ruff`.
- 관찰 1: The metal breastplate has an independent outer edge over cloth.
- 관찰 2: A separate ruff encircles the neck above that breastplate.
- 혼동 경계: 러프와 흉갑을 갈라복 모든 근무 버전에 강제
- 재사용 우선 ID: clothing_ct043_v1, ccx_cc13_02.
- 근거/반례 탐색 위치: [S19](https://schweizergarde.ch/fileadmin/files/Kasernenstiftung/SPENDENBROSCHUERE_SCHWEIZERGARDE_I.pdf). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U28 — 군악 역할의 황흑 배색을 갈라 삼색과 구분

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the yellow-and-black garment areas belong to the selected drummer variant`.
- 관찰 1: The selected garment carries a yellow-and-black scheme.
- 관찰 2: The ordinary red-yellow-blue gala scheme is not mixed into that same selected variant.
- 혼동 경계: 고수의 배색을 근위대 전원의 기본복으로 사용
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S20](https://www.nb.admin.ch/en/uniforms-arent-uniform). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U29 — 긴 뒤자락 코트 안에 독립된 조끼 앞섶이 남음

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the waistcoat front visible inside the open short-front long-back coat`.
- 관찰 1: The outer coat has a distinct short front and longer rear tails.
- 관찰 2: A separate waistcoat front remains inside its lapels.
- 혼동 경계: 영국·네덜란드의 다른 의례·시대를 모두 같은 색의 연미복으로 병합
- 재사용 우선 ID: ccx_cc02_01, ccx_cc02_02, costume_ccx_cc02_02.
- 근거/반례 탐색 위치: [S35](https://resources.metmuseum.org/resources/metpublications/pdf/Fashions_of_the_Hapsburg_Era_Austria_Hungary.pdf), [S58](https://www.rct.uk/collection/stories/royal-mews/liveries-worn-by-royal-mews-staff-at-the-time-of-queen-victorias-golden-jubilee). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U30 — 무릎바지 끝의 여밈과 아래 스타킹이 분리됨

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the knee-breeches hem meets the separate stocking below it`.
- 관찰 1: The trouser ends stop near the knee with their own closure edge.
- 관찰 2: Separate stockings continue beneath that edge.
- 혼동 경계: 현대 긴 바지로 대체하거나 특정 궁정의 노란 바지를 미확인 상태로 확정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S35](https://resources.metmuseum.org/resources/metpublications/pdf/Fashions_of_the_Hapsburg_Era_Austria_Hungary.pdf). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U31 — 튜닉과 헬멧의 시대 조합을 초기 톱햇과 분리

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the domed helmet worn with the selected later tunic`.
- 관찰 1: The headwear has a domed helmet outline rather than a tall flat-topped hat.
- 관찰 2: The outer garment is a tunic rather than the earlier tailcoat.
- 혼동 경계: 1829 초기 코트에 후대 헬멧을 시간 구분 없이 결합
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S22](https://www.met.police.uk/police-forces/metropolitan-police/areas/about-us/about-the-met/met-museums-archives/timeline/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U32 — 레드서지 상의 아래 바지 바깥선의 노란 줄

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the yellow trouser stripe runs along the outside seam below the red coat`.
- 관찰 1: The red coat remains a distinct upper garment.
- 관찰 2: A yellow stripe follows the outer trouser leg on the same wearer.
- 혼동 경계: 모든 캐나다 경찰 일상복에 적색 상의·스테트슨을 강제
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S23](https://rcmp.ca/en/gazette/evolution-rcmp-uniform-historical-look). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U33 — 보호조끼 외곽이 셔츠 몸판과 팔을 남김

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the protective vest layered over the shirt torso`.
- 관찰 1: The vest has a separate torso outline and armholes.
- 관찰 2: The shirt sleeves remain visible outside those vest armholes.
- 혼동 경계: 짙은 셔츠만으로 조끼를 충족하거나 실제 방탄 성능을 추론
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S22](https://www.met.police.uk/police-forces/metropolitan-police/areas/about-us/about-the-met/met-museums-archives/timeline/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U34 — 재킷에 부착된 반사 띠와 바탕 직물의 경계

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the reflective bands attached to the turnout jacket panels`.
- 관찰 1: The selected bands have bounded sewn placement on the jacket.
- 관찰 2: Their optical response differs from the surrounding cloth when lighting makes it observable.
- 혼동 경계: 노란 도색을 무조건 반사체로 판정하거나 특정 제품 배색을 모든 소방복에 확대
- 재사용 우선 ID: clothing_ct028_v1.
- 근거/반례 탐색 위치: [S25](https://stacks.cdc.gov/view/cdc/210816/cdc_210816_DS1.pdf). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U35 — 소방서 근무복과 방화 외피를 별도 선택으로 다룸

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected turnout outer garment layered over the station garment when requested`.
- 관찰 1: The protective outer layer has an independent enclosing edge.
- 관찰 2: Any visible station garment remains beneath it rather than replacing that outer layer.
- 혼동 경계: 소방관이라는 직업만으로 방화복·공기호흡기·진압 동작 추가
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S25](https://stacks.cdc.gov/view/cdc/210816/cdc_210816_DS1.pdf). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U36 — 가로 줄무늬가 상하 의복 면에 귀속됨

상태: `design_only`. 요청에 따라 선택할 수 있는 시각적 변형 설계다. 역사·규정·직업의 사실 주장으로 승격하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the alternating stripe bands distributed across the selected prison-costume garment`.
- 관찰 1: Stripe boundaries run across actual garment panels.
- 관찰 2: The selected palette and stripe direction remain consistent for that version.
- 혼동 경계: 줄무늬가 모든 실제 교정복의 규칙이거나 그 옷이 유죄를 뜻한다고 추론
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S26](https://nmaahc.si.edu/object/nmaahc_2017.34.1-.2). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U37 — 일체형 복장의 상체 여밈이 바지 부분으로 이어짐

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the coverall upper body continues into the trouser section of the same garment`.
- 관찰 1: A continuous garment body crosses the waist.
- 관찰 2: A separate front closure belongs to that body rather than an independent jacket.
- 혼동 경계: 드라마 소품의 주황색을 실제 전 세계 수용복 규정으로 일반화
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S27](https://nmaahc.si.edu/object/nmaahc_2020.47.1). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U38 — 단색 교정복 상의 밑단과 별도 하의 허리

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the plain sweatshirt hem separate from the trouser waistband`.
- 관찰 1: The upper garment has its own ending hem.
- 관찰 2: Separate trousers begin beneath it in the selected plain palette.
- 혼동 경계: 주황 일체형·흑백 줄무늬만 교정복 후보로 허용
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S26](https://nmaahc.si.edu/object/nmaahc_2017.34.1-.2). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U39 — 간호 원피스 바깥 앞치마와 별도 깃·커프스

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the apron panel layered over the nurse-dress body`.
- 관찰 1: The apron has its own edge over the underlying dress.
- 관찰 2: The dress collar or cuffs remain separate garment details.
- 혼동 경계: 박물관 합성 전시복을 한 벌의 원본으로 선언하거나 모자를 모든 간호복에 강제
- 재사용 우선 ID: ccx_cc01_01, ccx_cc01_02, ccx_cc01_03.
- 근거/반례 탐색 위치: [S28](https://collection.sciencemuseumgroup.org.uk/objects/co122317). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U40 — 스크럽 상의와 바지의 별도 허리 경계

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the scrub top hem separate from the scrub trouser waist`.
- 관찰 1: A loose top ends at its own hem.
- 관찰 2: The trousers remain an independent lower garment rather than a white fitted dress.
- 혼동 경계: 간호사라는 역할만으로 치료·환자·차트를 추가
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S29](https://medicalmuseum.health.mil/micrograph/index.cfm/posts/2026/BUMED-collection-expands-navy-medicine-story-at-NMHM). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U41 — 열린 백의가 안쪽 일상복을 둘러쌈

상태: `design_only`. 요청에 따라 선택할 수 있는 시각적 변형 설계다. 역사·규정·직업의 사실 주장으로 승격하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the lab-coat opening reveals the independent inner garment`.
- 관찰 1: The coat front has two separate edges around the torso.
- 관찰 2: An inner garment remains visible between them without being recolored into the coat.
- 혼동 경계: 흰 긴 코트만으로 의사·연구자 신분이나 장갑을 추론
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S30](https://www.dupont.com/safespec/tyvek/featured-products.facetgroup%24%24F%40%40PS30.html). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U42 — 후드와 직물 커버올 몸체의 연결 경계

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the fabric hood connected to the selected coverall neck`.
- 관찰 1: The hood is fabric continuous with or attached at the coverall neck.
- 관찰 2: Its face opening remains a distinct edge rather than an enclosing rigid helmet.
- 혼동 경계: 후드만으로 기밀 밀봉·생물학적 보호 성능이 검증됐다고 판정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S30](https://www.dupont.com/safespec/tyvek/featured-products.facetgroup%24%24F%40%40PS30.html). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U43 — 수술모와 마스크가 각각 머리와 얼굴에 귀속됨

상태: `design_only`. 요청에 따라 선택할 수 있는 시각적 변형 설계다. 역사·규정·직업의 사실 주장으로 승격하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the surgical mask worn by the selected wearer below a separate cap`.
- 관찰 1: The mask has its own border and support on the face.
- 관찰 2: A separate cap contains the head hair region and does not merge into the mask.
- 혼동 경계: 눈가리개를 수술 마스크로 대체하거나 모든 의료복에 마스크 강제
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S29](https://medicalmuseum.health.mil/micrograph/index.cfm/posts/2026/BUMED-collection-expands-navy-medicine-story-at-NMHM). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U44 — 의복 앞섶의 단일 단추열과 이중 단추열 분리

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected button row attached to one garment front configuration`.
- 관찰 1: Buttons occupy one selected single-row or double-row configuration.
- 관찰 2: The overlapping front edge follows that chosen configuration.
- 혼동 경계: JAL의 다른 시대·일반/책임자 앞섶을 한 의복에 혼합
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S31](https://www.jal.com/ja-jp/about/uniform/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U45 — 1970 JAL의 앞벨트와 별도 뒤지퍼

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the red waist belt encircles the dress with a separate rear zipper`.
- 관찰 1: A red belt forms an independent waist band over the dress.
- 관찰 2: The selected closure is on the back rather than an invented front button row.
- 혼동 경계: 가슴 금색 단추가 있는 다른 시대 JAL 재킷을 자동 추가
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S31](https://www.jal.com/ja-jp/about/uniform/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U46 — 모자 없는 선택 버전에서 머리 위 독립 모자 외피를 배제

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the visible head silhouette remains separate from any unrequested hat shell`.
- 관찰 1: The full selected head region is observable.
- 관찰 2: No independent hat crown or brim is imposed on that region for this selected no-hat variant.
- 혼동 경계: 1996 JAL 버전에 이전 시대 보울 모자를 자동 추가하거나 가린 머리를 모자 없음의 증거로 사용
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S31](https://www.jal.com/ja-jp/about/uniform/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U47 — 승무원 스카프의 상승한 끝과 별도 머리 장식

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the raised scarf end extends from the neck accessory below the separate hair ornament`.
- 관찰 1: The scarf originates from the neck and has its own projecting end.
- 관찰 2: The separate hair ornament belongs to the hair rather than continuing from that scarf.
- 혼동 경계: 목 스카프를 머리 장식으로 연결하거나 2019 설명을 2026 현행 규정으로 선언
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S32](https://news.koreanair.com/?p=1204). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U48 — 사롱 위에 겹친 케바야 블라우스

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the kebaya blouse layered over the wrapped sarong`.
- 관찰 1: The upper blouse has its own lower edge.
- 관찰 2: A wrapped sarong continues below that edge on the same wearer.
- 혼동 경계: 배색만으로 블레이저를 케바야로 판정하거나 모든 SQ 버전에 케로상 세 개를 강제
- 재사용 우선 ID: clothing_ct141_v2.
- 근거/반례 탐색 위치: [S33](https://www.singaporeair.com/en_UK/bn/flying-withus/our-story/our-cabin-crew/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U49 — 계급별 색은 선택 의복 면에만 매핑

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected rank color belongs to the version-specific uniform garment`.
- 관찰 1: One chosen garment palette is assigned to its actual cloth panels.
- 관찰 2: It is not copied onto skin, background or unrelated accessories.
- 혼동 경계: 네 색의 존재 확인을 색-직급의 정확한 대응표 확인으로 확대
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S33](https://www.singaporeair.com/en_UK/bn/flying-withus/our-story/our-cabin-crew/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U50 — 같은 재킷의 스커트형과 바지형을 대안으로 유지

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected jacket worn with one selected skirt or trouser alternative`.
- 관찰 1: The upper jacket remains the common selected garment.
- 관찰 2: Exactly the requested lower garment type is present for that wearer.
- 혼동 경계: 한 사람에게 스커트와 바지를 두 버전의 필수 조합으로 겹침
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S32](https://news.koreanair.com/?p=1204). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U51 — 벨홉의 짧은 재킷과 독립된 모자

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the short service jacket worn with the separate pillbox-like cap`.
- 관찰 1: The jacket ends at its own selected short hem.
- 관찰 2: The cap has a bounded crown independent from the jacket collar.
- 혼동 경계: 리버리·궁정·호텔의 같은 색 재킷을 모두 벨홉으로 명명
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S34](https://www.rct.uk/visit/the-royal-mews-buckingham-palace/highlights-of-the-royal-mews). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U52 — 앞치마 가슴판·허리띠·치마 패널의 귀속

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the apron bib and lower panel connected to their own waist band over the dress`.
- 관찰 1: The selected apron bib has its own upper support.
- 관찰 2: Its lower panel and band remain outside a separately bounded dress.
- 혼동 경계: 허리 앞치마를 가슴판 앞치마의 증거로 쓰거나 앞치마에 실제 가사 역할 강제
- 재사용 우선 ID: ccx_cc01_01, ccx_cc01_02, ccx_cc01_03.
- 근거/반례 탐색 위치: [S59](https://www.detroithistorical.org/learn/online-research/collection/object/uniform-occupational-1), [S62](https://www.metmuseum.org/art/collection/search/123766). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U53 — 조리복의 겹친 앞섶과 이중 단추열

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the chef-jacket overlapping front closed by two selected button rows`.
- 관찰 1: The front panels overlap as one jacket construction.
- 관찰 2: The button rows are attached to that front rather than a printed pattern.
- 혼동 경계: 조리복을 무조건 흰색으로 한정하거나 특정 유물 색을 모든 조리사에 부여
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S36](https://collection.sciencemuseumgroup.org.uk/objects/co145971), [S37](https://nmaahc.si.edu/object/nmaahc_2021.96.2). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U54 — 버니 머리 장식이 의복 착용자의 머리에 붙음

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the artificial ears attached to the headpiece of the leotard wearer`.
- 관찰 1: The ear shapes have their own manufactured outlines.
- 관찰 2: Their base belongs to a headpiece worn by the same garment wearer.
- 혼동 경계: 인간을 토끼 종으로 바꾸거나 옷만으로 성적 행위·관계·신체 비율을 부과
- 재사용 우선 ID: ccx_cc17_01, ccx_cc17_02.
- 근거/반례 탐색 위치: [S38](https://americanhistory.si.edu/collections/object/nmah_1117598), [S39](https://www.americanhistory.si.edu/de/collections/object/nmah_1117599). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U55 — 흰 칼라·커프스가 검은 원피스 몸판에 붙음

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the white collar and cuffs attached to the black dress neckline and sleeve ends`.
- 관찰 1: The white collar follows the dress neckline with its own edge.
- 관찰 2: The white cuffs lie at the actual sleeve ends of that same dress.
- 혼동 경계: 무릎 길이 실제 사용인복을 무조건 긴 치마·흰 앞치마로 교체
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S59](https://www.detroithistorical.org/learn/online-research/collection/object/uniform-occupational-1). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U56 — 입식깃과 중앙 앞섶이 같은 가쿠란 상의를 이룸

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the standing collar connected to the central-front jacket closure`.
- 관찰 1: The collar rises from the jacket neckline.
- 관찰 2: The central closure belongs to the same structured jacket body.
- 혼동 경계: 상표·학교 확인 없이 모든 가쿠란의 단추 수·금속 색을 확정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S40](https://kanko-gakuseifuku.co.jp/museum/history_uniform), [S61](https://kanko-gakuseifuku.co.jp/media/parents/purchase). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U57 — 세일러 선이 칼라 가장자리의 윤곽을 따름

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected collar lines follow the sailor-collar edge`.
- 관찰 1: Each line stays within the collar panel near its edge.
- 관찰 2: The number and spacing follow the chosen school or version rather than a universal count.
- 혼동 경계: 선이 배경이나 리본에만 있거나 모든 학교에 세 줄을 강제
- 재사용 우선 ID: clothing_ct041_v2, ccx_cc03_01.
- 근거/반례 탐색 위치: [S61](https://kanko-gakuseifuku.co.jp/media/parents/purchase). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U58 — 민소매 점퍼스커트 아래 블라우스 소매가 나옴

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the sleeveless jumper dress layered over the separate blouse`.
- 관찰 1: The outer dress has its own open armholes.
- 관찰 2: The inner blouse sleeves emerge from those openings on the same wearer.
- 혼동 경계: 소매가 붙은 원피스를 점퍼스커트 겹침으로 판정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S40](https://kanko-gakuseifuku.co.jp/museum/history_uniform). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U59 — 개조 교복의 상의 길이와 하의 폭을 각각 조절

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the modified jacket hem sits relative to the selected trouser waist`.
- 관찰 1: The jacket's hem has a chosen long or short position relative to the waist.
- 관찰 2: The lower garment keeps its separately chosen wide or ordinary leg outline.
- 혼동 경계: 초란과 탄란을 동시에 적용하거나 넓은 바지에서 비행·폭력 성향 추론
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S40](https://kanko-gakuseifuku.co.jp/museum/history_uniform). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U60 — 가운과 독립된 학위 모자를 같은 착용자에 귀속

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the academic headwear worn by the gown wearer`.
- 관찰 1: The selected cap has its own crown or top shape above the head.
- 관찰 2: The gown remains a separate shoulder-supported outer garment on the same wearer.
- 혼동 경계: 모든 학위·기관에 사각모·탐모·후드를 동시에 강제
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S41](https://www.ox.ac.uk/students/academic/dress). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U61 — 수단의 긴 몸판과 중앙 앞섶

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the central front closure runs along the long cassock body`.
- 관찰 1: The garment body descends continuously below the waist.
- 관찰 2: A selected front closure belongs to that body rather than an outer stole.
- 혼동 경계: 사제의 교단·계급별 단추 수·색을 확인 없이 고정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S43](https://www.sbfranciscans.org/be-a-friar/formation/stages-of-formation/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U62 — 수도복 튜닉과 별도 후드·허리끈

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the waist cord encircles the habit tunic below its separate hood`.
- 관찰 1: The tunic has a continuous torso and lower cloth body.
- 관찰 2: A separate cord gathers its waist while the hood or capuche retains its own edge.
- 혼동 경계: 모든 프란치스코회에 갈색·세 매듭을 부과하거나 수련자와 서원자를 합침
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S43](https://www.sbfranciscans.org/be-a-friar/formation/stages-of-formation/), [S44](https://franciscanfriars.org/2025/03/03/preparation-of-the-grey-conventual-habits/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U63 — 수녀 베일과 머리 둘레 흰 층을 분리

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the outer veil layered over the selected inner headcloth`.
- 관찰 1: The outer veil has its own descending edge.
- 관찰 2: A separately bounded inner headcloth remains visible where requested.
- 혼동 경계: 모든 수도회 수녀복을 흑백 한 형태로 고정하거나 신앙·성격을 추론
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S44](https://franciscanfriars.org/2025/03/03/preparation-of-the-grey-conventual-habits/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U64 — 직사각 가사의 안쪽 패치와 바깥 테두리

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the rectangular inner patchwork enclosed by the outer kesa border`.
- 관찰 1: Interior cloth blocks form a bounded rectangular field.
- 관찰 2: A separate border surrounds that field rather than a random all-over print.
- 혼동 경계: 모든 가사에 동일 열 수·색·주름을 부과하거나 입는 방식 없이 신분 확정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S42](https://www.metmuseum.org/art/collection/search/69886). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U65 — 흰 상의·붉은 하카마 위 선택된 치하야 겉옷

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected chihaya outer layer layered over the white upper garment above red hakama`.
- 관찰 1: The white upper garment and red lower garment remain separate pieces.
- 관찰 2: When chihaya is selected, it has its own outer edge above those pieces.
- 혼동 경계: 일반 미코복에도 춤용 겉옷을 항상 추가하거나 성인·미성년 나이를 의복으로 판정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S45](https://mamechishiki.tokyo/?p=906). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U66 — 부서색 상의와 검은 하의의 TOS 계열 배치

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected department-color top worn with the separate dark lower garment`.
- 관찰 1: The chosen color belongs to the top body.
- 관찰 2: The lower garment retains a separate dark region without importing another show's yoke.
- 혼동 경계: Star Trek 모든 판본의 가슴·어깨·깃 색을 한 기본 제복으로 병합
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S46](https://www.startrek.com/news/you-wear-it-well-the-uniforms-of-star-trek). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U67 — TNG 초기 일체형과 후기 별도 상하의 경계

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the chosen TNG upper body meets its version-specific lower construction`.
- 관찰 1: The selected early or later construction has one defined waist boundary.
- 관찰 2: The alternative version's waist treatment is not added to that same garment.
- 혼동 경계: 이름만으로 초기·후기 재단을 동시 부과하거나 성별로 바지 종류를 고정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S46](https://www.startrek.com/news/you-wear-it-well-the-uniforms-of-star-trek). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U68 — 회색 어깨 요크 아래 검은 몸판과 별도 부서색 목층

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the grey shoulder yoke attached to the black body above the separate color neck layer`.
- 관찰 1: The selected upper yoke is grey and belongs to the black outer body.
- 관찰 2: A separate colored neck layer remains visible within the opening.
- 혼동 경계: 초기 DS9의 부서색 어깨와 후기의 회색 어깨를 서로 바꿈
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S46](https://www.startrek.com/news/you-wear-it-well-the-uniforms-of-star-trek), [S48](https://www.startrek.com/news/check-it-out-star-trek-first-contact-deep-space-nine-standard-line-uniform). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U69 — 적갈색 앞섶과 별도 사슬·속목층

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected lapel chain attached to the maroon outer lapel above the inner neck layer`.
- 관찰 1: The chain has its own attachment on the selected outer lapel.
- 관찰 2: The raised undershirt neckline remains an independent inner layer.
- 혼동 경계: 허가 복제품의 소재를 원본 촬영복의 정확한 소재로 확정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S47](https://www.startrek.com/news/first-look-spocks-wrath-of-khan-uniform). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U70 — Enterprise 작업복 어깨의 얇은 부서색 영역

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the narrow department trim attached to the work-style suit shoulder`.
- 관찰 1: The suit is one chosen work-style outer garment.
- 관찰 2: The selected department color stays in a narrow shoulder area rather than recoloring the whole torso.
- 혼동 경계: NASA 비행복에 해당 작품의 표식을 자동 이식
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S46](https://www.startrek.com/news/you-wear-it-well-the-uniforms-of-star-trek). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U71 — 흰 장갑판 사이 검은 보디글러브 관절층

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the armor plates layered over the black body glove at the joints`.
- 관찰 1: Armor pieces have separate hard-looking outer edges.
- 관찰 2: Black cloth remains visible between selected plate edges at the joints.
- 혼동 경계: 흰 로봇 몸체로 바꾸거나 복장만으로 총·전투 동작을 자동 추가
- 재사용 우선 ID: ccx_cc13_02, ccx_cc13_03, ccx_cc15_01, ccx_cc15_02.
- 근거/반례 탐색 위치: [S49](https://www.starwars.com/databank/clone-trooper-armor), [S50](https://www.starwars.com/databank/stormtroopers/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U72 — 스노트루퍼 후드·벨트 아래 케이프가 별도 층임

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the hood and belt-supported cape layered over the selected insulated suit`.
- 관찰 1: A separate hood surrounds the head region.
- 관찰 2: A cape edge continues below its belt support rather than becoming rear armor plates.
- 혼동 경계: 일반 스톰트루퍼·스카우트·퍼스트 오더에 같은 후드와 케이프를 부과
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S51](https://www.starwars.com/databank/snowtroopers). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U73 — 선택 헬멧의 눈·입·하단 면을 판본별로 유지

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the selected helmet face planes belong to one edition-specific helmet shell`.
- 관찰 1: Eye and mouth openings occupy the selected helmet face.
- 관찰 2: Their connecting planes and lower outline remain one chosen edition.
- 혼동 경계: Phase I·II·제국·퍼스트 오더의 얼굴 면을 기억만으로 혼합
- 재사용 우선 ID: ccx_cc13_01.
- 근거/반례 탐색 위치: [S49](https://www.starwars.com/databank/clone-trooper-armor), [S50](https://www.starwars.com/databank/stormtroopers/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U74 — 2B 눈가리개와 독립된 높은 깃·가슴 개구부

상태: `observed_crop_only`. 공식 화면에서 관찰한 크롭의 요소만 지지한다. 화면 밖 구조와 다른 매체 판본은 미확인이다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the eye covering worn by the selected 2B-version wearer above the garment opening`.
- 관찰 1: The eye covering has a visible edge across the eye region.
- 관찰 2: The high garment neckline and selected chest opening remain separate below it.
- 혼동 경계: 관찰하지 않은 치마 밑단·부츠까지 검증했다고 하거나 게임·애니 판본을 합침
- 재사용 우선 ID: ccx_cc28_02.
- 근거/반례 탐색 위치: [S52](https://nierautomata-anime.com/character/detail/?chara=2b), [S53](https://nierautomata-anime.com/character/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U75 — 퀴디치 로브와 훈련복·경기 보호대의 판본 분리

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected sports outer garment worn with its requested training or match equipment`.
- 관찰 1: One chosen robe or tracksuit construction is visible.
- 관찰 2: Protective pads or a helmet appear only for the selected match configuration.
- 혼동 경계: 혼혈 왕자의 훈련복에 경기용 보호대를 항상 얹거나 초기 두 영화의 무거운 로브를 유지
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S54](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U76 — 보바통의 푸른 의복과 독립된 뾰족 모자

상태: `supported_relation`. 출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the pointed blue hat worn by the selected blue-costume wearer`.
- 관찰 1: The hat has its own pointed crown above the head.
- 관찰 2: The selected blue garment remains a separate cloth body beneath it.
- 혼동 경계: 다른 마법학교의 검은 로브를 보바통의 대표 의복으로 대체
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S54](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U77 — 흰 날개형 머리 가리개와 적색 외피의 분리

상태: `needs_primary_verification`. 형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `wearable_accessory`.
- 방향 관계: `the white winged head covering worn with the selected red outer garment`.
- 관찰 1: The head covering has independent lateral projecting edges.
- 관찰 2: The red outer garment belongs to the same wearer below that covering.
- 혼동 경계: 적색만으로 시녀 신분·갈색 이모복·청록 아내복을 혼합하거나 신체 통제를 자동 장면화
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S55](https://interviews.televisionacademy.com/shows/handmaids-tale-the). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U78 — 장교 모티프 외피와 코르셋 구조선의 소유 분리

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the corset channels belong to the corset beneath optional jacket motifs`.
- 관찰 1: Vertical channels continue within the corset's own outline.
- 관찰 2: Any selected braid or shoulder motif attaches to a separate outer garment or its declared carrier.
- 혼동 경계: 직업 이름에서 실제 군 계급·무기·신체 비율을 추론
- 재사용 우선 ID: ccx_cc26_01, ccx_cc26_02, ccx_cc05_01, ccx_cc05_02.
- 근거/반례 탐색 위치: [S04](https://www.nam.ac.uk/explore/cavalry-roles). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U79 — 무대 의복의 선택된 짧은 밑단과 바디수트 경계

상태: `design_only`. 요청에 따라 선택할 수 있는 시각적 변형 설계다. 역사·규정·직업의 사실 주장으로 승격하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the selected short hem or leg opening belongs to the stage garment`.
- 관찰 1: The chosen ending edge belongs to the garment itself.
- 관찰 2: The visible leg region remains the wearer anatomy rather than added cloth panels.
- 혼동 경계: 미니·성인 무대복을 실제 간호·경찰 규정으로 선언하거나 신체 크기를 임의 변경
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S59](https://www.detroithistorical.org/learn/online-research/collection/object/uniform-occupational-1). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U80 — 광택 하이라이트가 제복 표면의 주름을 따름

상태: `design_only`. 요청에 따라 선택할 수 있는 시각적 변형 설계다. 역사·규정·직업의 사실 주장으로 승격하지 않는다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `surface_material`.
- 방향 관계: `the specular highlight follows the selected garment surface`.
- 관찰 1: The highlight lies on the garment's curved or folded surface.
- 관찰 2: Its path changes with those visible folds rather than emitting light at every seam.
- 혼동 경계: 광택만으로 라텍스·가죽·내구성·성적 취향을 확정
- 재사용 우선 ID: 동등 항목 추가 대조 후 결정.
- 근거/반례 탐색 위치: [S38](https://americanhistory.si.edu/collections/object/nmah_1117598). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U81 — 헤짐과 수선 패치의 위치를 같은 의복에 묶음

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the repair patch and frayed edge belong to the selected garment region`.
- 관찰 1: The patch has its own sewn boundary on the chosen panel.
- 관찰 2: Fraying stays localized to the requested edge and does not become body injury.
- 혼동 경계: 오래된 군복에서 사망·부상·피해자·가해자를 자동 추가
- 재사용 우선 ID: ccx_cc32_01, ccx_cc32_02.
- 근거/반례 탐색 위치: [S10](https://www.awm.gov.au/collection/C106357). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U82 — 발광 패널 경계와 비발광 직물 관절층 분리

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `garment_detail`.
- 방향 관계: `the luminous panel edges separate from the unlit fabric joint gaps`.
- 관찰 1: The selected panel border carries a visible light source or glow.
- 관찰 2: The cloth gaps between panels remain a different unlit material region.
- 혼동 경계: SF 제복이라는 이름만으로 전신 네온·로봇 종·보안 임무를 자동 추가
- 재사용 우선 ID: ccx_cc35_01, ccx_cc35_02, ccx_cc13_03.
- 근거/반례 탐색 위치: [S49](https://www.starwars.com/databank/clone-trooper-armor). 원문 인용이나 전체 형상 승인 표시가 아니다.

## U83 — 명시적으로 든 소품과 종교 의복의 소유 분리

상태: `reuse_existing`. 동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.

- 소유: `the request-supported costume wearer`; 후보 슬롯 제안: `prop`.
- 방향 관계: `the explicitly requested handheld prop held by the selected garment wearer`.
- 관찰 1: The requested prop has a separate handle and outer silhouette.
- 관찰 2: The same wearer's hand visibly grips it without changing the garment into a weapon.
- 혼동 경계: 수도복만으로 무기·전투·폭력을 추가하거나 의복을 곧바로 실제 신앙으로 판정
- 재사용 우선 ID: ccx_cc36_01, ccx_cc36_02.
- 근거/반례 탐색 위치: [S43](https://www.sbfranciscans.org/be-a-friar/formation/stages-of-formation/). 원문 인용이나 전체 형상 승인 표시가 아니다.
