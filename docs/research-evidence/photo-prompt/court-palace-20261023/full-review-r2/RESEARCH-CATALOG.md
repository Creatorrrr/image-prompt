# 궁중물 2차 보강: 관측 요소·연결·혼동 경계

2026-10-23 공식 본문과 실물/재현 사진 판독을 근거로 작성한 범위다. 각 항목은 선택 가능한 구성 요소이며 큰 고증 일습 전체를 승인하지 않는다. 이미지의 품계·신분·정체성·향기·의도와 숨은 내부 구조는 관측되지 않으면 성공으로 보지 않는다.

시각 대안 18개와 진단 6개를 실제 후보 데이터에 반영했다. 19개 기존 항목에는 구성 요소 연결을, 프렌치 후드에는 게이블 쓰개와의 차이만 알리는 contrast 연결을 추가했다. 기존 보류 복합 카드 40개는 유지한다.

## R2V01 — 거들지

색 소매 끝의 흰 안감이 겉으로 접혀 올라가며 접힌 가장자리와 안팎 전환이 보인다.

연결: white lining → turns_over → colored sleeve; folded edge → bounds → white lining.

혼동 경계: 흰 띠 인쇄나 별도 장갑과 구별; 한지심은 소매 밖 모습으로 판정 불가.

픽셀 기준: 색 소매와 흰 접힘의 경계 / 접힌 두께/되돌아가는 가장자리 / 같은 소매에 이어진 안팎 전환.

근거: [거들지 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0001803) — Turned sleeve-end construction; lining/paper variants are not universally visible.

후보: `cand_62417f539ce85c71b6a80fafca578545`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V02 — 노리개, 띠돈, 술

옷고름의 띠돈에서 끈목이 이어져 매듭과 중심 장식을 지탱하고 그 아래로 술이 내려온다.

연결: top clasp → attaches_to → garment tie; cord → connects → top clasp; knot → above → central ornament; tassel → hangs_below → central ornament.

혼동 경계: 목걸이·분리된 술과 구별; 궁중 신분·주술적 효능을 확정하지 않음.

픽셀 기준: 옷고름 접속 / 띠돈-끈목 연결 / 장식 위 매듭 / 장식 아래 술 / 중력에 맞는 연속 지지.

근거: [국가유산진흥원 - 노리개](https://www.kh.or.kr/brd/board/741/L/menu/740?bbIdx=100194&brdType=R&searchField=&searchText=&thisPage=1) — Suspension, ornament, knot and tassel structure; wearing and object realization are authored.

후보: `cand_834d1148460c56b6ae0c5dcdb21d3a7b`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V03 — 흉배, 쌍학흉배

검은 단령 앞 몸판에 학 두 마리의 사각 자수 흉배가 평평하게 붙어 네 변이 보인다.

연결: square badge → attached_to → front torso; two cranes → depicted_on → square badge.

혼동 경계: 왕실 원형 보·소매 원형 장식과 구별; 실제 관직·품계는 미판정.

픽셀 기준: 몸판 위치 / 사각 패치 네 변 / 학 두 마리 / 자수/천 경계.

근거: [흉배 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0065867) — Attached badges and historically variable motifs; rank is not established by generated pixels.

후보: `cand_12ef7865b56058afad067f31be971425`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V04 — 화분저, 기혜, 마제저

자수 갑피의 낮은 신이 발바닥 중앙의 높은 목제 받침 위에 놓이고 앞코와 뒤꿈치가 받침 밖으로 뻗는다.

연결: central wooden support → under_center_of → sole; toe → extends_beyond → central wooden support; heel → extends_beyond → central wooden support.

혼동 경계: 전족용 작은 궁혜나 뒤꿈치 힐과 구별; 발 크기·보행·민족은 외형만으로 미판정.

픽셀 기준: 갑피-받침 연결 / 받침의 중앙 위치 / 앞뒤 돌출 / 바닥 지지.

근거: [Female footwear - Museo d Arte Cinese ed Etnografico](https://museocineseparma.org/en/museo/collezioni-etnografiche/cina-etno/361-calzature-femminili) — Central wooden support under shoe; this object is catalogued Republic period, not proof of every Qing court shoe.

후보: `cand_ea206876d2845ba58e8635f0680b57a3`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V05 — 가리기누, 狩衣

가리기누 소매는 몸판 뒤쪽 일부에만 붙어 겨드랑이가 열리고 수구에는 조임끈이 이어진다.

연결: sleeve → joined_at → rear attachment; open underarm → separates → sleeve; gathering cord → runs_through → sleeve opening.

혼동 경계: 보통 넓은 소매나 찢어진 겨드랑이와 구별; 소쿠타이 전체와 동일시하지 않음.

픽셀 기준: 뒤쪽 부분 접합 / 열린 겨드랑이 공간 / 수구의 끈 경로.

근거: [狩衣姿 - 風俗博物館](https://www.iz2.or.jp/fukushoku/f_disp.php?page_no=0000043) — Open underarm, partial rear sleeve attachment and gathering cord; reconstruction display, not excavated original.

후보: `cand_5fed7ef497fb58318cf519ee3b5128d4`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V06 — 샤쿠, 笏

좁고 평평한 샤쿠 한 개를 몸 앞에서 세워 들고 손가락이 아래 끝을 쥐는 접촉이 보인다.

연결: fingers → grip → lower end; flat tablet → upright_in_front_of → robe front.

혼동 경계: 닫힌 부채·검·둥근 지팡이와 구별; 손 자세는 저자 제안이며 의식 규범을 보증하지 않음.

픽셀 기준: 편평한 판 한 개 / 하단 손가락 접촉 / 몸 앞의 수직 배치.

근거: [公卿冬束帯 - 風俗博物館](https://www.iz2.or.jp/fukushoku/f_disp.php?page_no=0000026) — Shaku and shitagasane train are separate components, not complete sokutai qualification.

후보: `cand_6ce57f41767557418b30ca8b77b2432f`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V07 — 폴로네즈

몸에 맞는 폴로네즈 보디스 아래 겉치마 뒷부분이 세 덩이로 걷혀 그 밑 별도 페티코트가 드러난다.

연결: back overskirt → gathered_into → three puffed sections; three puffed sections → reveal → petticoat.

혼동 경계: 프랑세즈 등판 주름·단일 버슬과 구별; 숨은 끈/링 방식은 미판정.

픽셀 기준: 보디스-치마 연결 / 뒤쪽 세 덩이 / 드러난 별도 속치마 / 겉/속 레이어 경계.

근거: [Polonaise - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/83887) — Three lifted back-skirt sections expose petticoat; alternative hidden lifting mechanisms cannot be jointly assumed.

후보: `cand_e0787ada558956899abc1f3e229757f3`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V08 — 맨투아

궁정 맨투아의 보디스가 뒤 트레인으로 이어지고 넓은 별도 페티코트와 앞가슴 삼각 스토머커가 구별된다.

연결: bodice → continues_into → rear train; triangular stomacher → fills_front_of → bodice; petticoat → separate_under → bodice.

혼동 경계: 원래 분실된 스토머커를 현재 전시 예시와 동일 유물로 단정하지 않음.

픽셀 기준: 앞 삼각 패널 / 별도 치마 / 뒤로 이어진 트레인 / 한 착장으로 연결된 세 영역.

근거: [Luxury in fashion: the 18th-century court mantua - National Museums Scotland](https://www.nms.ac.uk/discover-catalogue/luxury-in-fashion-the-18th-century-court-mantua) — Surviving mantua ensemble; illustrated stomacher is a separate example, not the lost original.

후보: `cand_03fea544c58e53f6bdad3dffe980674d`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V09 — 포맨더

열린 포맨더의 속 빈 분할 용기가 중심 기둥 둘레로 펼쳐지고 분할 덮개와 위쪽 고리 달린 마개가 보인다.

연결: hinged hollow segments → spread_around → central stem; sliding covers → cover → hinged hollow segments; loop-topped cap → above → central stem.

혼동 경계: 구멍만 있는 구형 펜던트와 구별; 향기와 질병 예방은 픽셀 판정 불가.

픽셀 기준: 중심 기둥 / 열린 복수 용기 / 각 덮개 경계 / 상단 고리.

근거: [Pomander - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/196980) — Hinged compartments, sliding lids and screwcap loop; no medical efficacy or smell qualification.

후보: `cand_e5e49914e77951bcb2f06c31d70b0dbe`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V10 — 파뤼르, 장식 빗

굽은 금색 장식 빗의 띠 위에는 보라색 자수정 장식이, 아래에는 빗살이 이어져 두 부분의 연결이 보인다.

연결: purple stone settings → above → curved band; comb teeth → below → curved band.

혼동 경계: 티아라 앞면만으로 빗살이나 파뤼르 전체를 추정하지 않음; 실제 광물·금 순도는 별도.

픽셀 기준: 굽은 띠 / 위 보라 장식 / 아래 빗살 / 세 부분 접합.

근거: [Comb (part of a set) - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/197155) — Gold/amethyst object and matched-set definition; individual comb does not prove a full parure.

후보: `cand_3e1b7fa677e95960a649299534b8046b`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V11 — 스너프박스

닫힌 작은 금색 스너프박스의 꽃 부조가 뚜껑과 옆면에 이어지되 얇은 뚜껑 이음선이 몸통과 구별된다.

연결: thin seam → separates → lid; floral relief → continues_across → box body.

혼동 경계: 단순 금색 덩어리와 구별; 내용물·선물 여부·사용자 성격은 미판정.

픽셀 기준: 독립 뚜껑 이음선 / 몸통 / 뚜껑/옆면 꽃 부조 / 손이나 받침에 맞는 스케일.

근거: [Snuffbox - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/200390) — Floral decoration crosses lid/side division; contents, gift or vanity cannot be inferred.

후보: `cand_cb9c168324515813a4a1ed78f35dfd87`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V12 — 게이블 후드, 프렌치 후드

천으로 덮인 게이블 쓰개가 이마 둘레에 각진 박공 윤곽을 이루고 천 표면이 얼굴과 구별된다.

연결: angular peaked outline → frames → forehead; fabric cover → outside → face.

혼동 경계: 둥근 프렌치 후드와 구별; 가려진 황동 철사 프레임은 이 외형만으로 확인하지 않음.

픽셀 기준: 각진 상단 윤곽 / 이마 둘레 천 / 얼굴/천 경계.

근거: [Head dress frame - London Museum](https://www.londonmuseum.org.uk/collections/v/object-117855/head-dress-frame/) — Angular gable and curved French hood profiles are distinguished; concealed wire is unobservable when covered.

후보: `cand_a993d431bb30552aa611b64119cbd90a`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V13 — 파스망트리, 술 장식

장식 실 브레이드가 옷 가장자리를 따라 이어지고 끝에 달린 술의 낱실이 아래로 내려온다.

연결: braided trim → attached_along → garment edge; tassel head → attached_to → braided trim; loose thread strands → hang_below → tassel head.

혼동 경계: 프린트 줄무늬와 구별; 금속 성분·직조 조직을 광택만으로 확정하지 않음.

픽셀 기준: 옷 가장자리 부착 / 브레이드 조직 / 술 접속 / 자유 낱실.

근거: [passementerie - FIT Fashion History Timeline](https://fashionhistory.fitnyc.edu/passementerie/) — Thread trim category; weave, print and precious-metal assay need separate evidence.

후보: `cand_2e3f795893c75372bbf9d6d6560979ae`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V14 — 페즈, 프록코트

19세기 오스만 개혁 복식 해석으로 페즈 모자·프록코트·몸에 맞는 바지가 각각 보인다.

연결: fez cap → above → frock coat; fitted trousers → below → frock coat.

혼동 경계: 16세기 카프탄·샬바르와 자동 결합하지 않음; 특정 직위·종교·실제 착용 사건은 미판정.

픽셀 기준: 페즈 윤곽 / 프록코트 구조 / 별도 바지 실루엣 / 한 인물의 일관된 착장.

근거: [The Later Ottomans and the Impact of Europe - The Metropolitan Museum of Art](https://www.metmuseum.org/de/essays/the-later-ottomans-and-the-impact-of-europe) — 19th-century fez, frock coat and fitted trousers example; do not transpose to 16th-century robe ensemble.

후보: `cand_4e4175932a165f36a01e20309bef242e`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V15 — 친타마니, 카프탄

자홍색 카프탄 몸판에 노란 원 세 개가 삼각으로 모인 문양이 반복되고 로브 천 위의 문양임이 보인다.

연결: three-disc clusters → repeat_on → magenta robe body; three-disc clusters → depicted_on → fabric surface.

혼동 경계: 보석 단추·노리개와 구별; 이 유물 변형에는 물결띠를 추가하지 않음.

픽셀 기준: 세 원의 삼각 배열 / 복수 반복 / 몸판 천의 표면 / 문양과 장신구 구별.

근거: [Robe (Kaftan) - Smithsonian National Museum of Asian Art](https://asia-archive.si.edu/exhibition/style-and-status-robe-kaftan-13-41/) — Triple-ball triangular motif; bands occur in some variants but not on this pictured robe.

후보: `cand_8bb64cc64c555b1889b3abc72ecbd876`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V16 — 요질

꼰 삼 요질이 소박한 상복 허리를 둘러 앞에서 묶이고 끝은 긴 뿌리 가닥 없이 정리된다.

연결: twisted hemp tie → encircles → waist; front knot → secures → tied ends.

혼동 경계: 수질·교대와 구별; 선택한 산수 없는 변형이며 사망·친족·상복 등급을 증명하지 않음.

픽셀 기준: 허리 둘레 연속성 / 꼰 섬유 외형 / 앞 매듭 / 길게 늘어진 뿌리 없음.

근거: [상복 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0027105) — Twisted hemp waist tie; selected no-dangling-root variant, not all mourning grades.

후보: `cand_a44e5e00d9bd5ffd93a4180fd7cfdc86`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V17 — 소쿠타이, 시타가사네

소쿠타이 겉포 뒤 아래에서 밝은 시타가사네 자락이 나와 착용자 뒤 바닥을 따라 길게 놓인다.

연결: pale inner hem → emerges_beneath → outer robe back; rear train → rests_on → floor.

혼동 경계: 서양 어깨 부착 망토 트레인과 구별; 모든 속옷 층·품계는 미판정.

픽셀 기준: 겉포 아래 출현점 / 밝은 연속 자락 / 뒤로 뻗는 트레인 / 바닥 접촉.

근거: [公卿冬束帯 - 風俗博物館](https://www.iz2.or.jp/fukushoku/f_disp.php?page_no=0000026) — Shaku and shitagasane train are separate components, not complete sokutai qualification.

후보: `cand_d544259c30de51c6a57ea034058eec83`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2V18 — 가리마

접은 짙은 쓰개가 이마와 정수리를 덮고 뒤 어깨에 드리워지며 얼굴 옆에 두 겹 천 가장자리가 보인다.

연결: doubled dark cloth → covers → forehead; doubled dark cloth → covers → crown; doubled dark cloth → drapes_over → back shoulders.

혼동 경계: 가체·족두리와 구별; 안쪽 종이·직업·신분은 외형으로 미판정.

픽셀 기준: 이마/정수리 덮음 / 뒤 어깨 드리움 / 두 겹 접힘 가장자리.

근거: [가리마 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0000145) — Folded headcloth covers forehead/crown and back shoulders; hidden paper and occupation are not visible.

후보: `cand_7b77cba44bb35542b3734a1206bfaa74`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2D01 — 흉배로 실제 품계 확정 금지

혼동 경계: Badge motifs varied historically; a generated pair of cranes does not verify a real office or rank.

픽셀 기준: UNOBSERVABLE_NOT_PASS.

근거: [흉배 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0065867) — Attached badges and historically variable motifs; rank is not established by generated pixels.

후보: `cand_a6748d1969c3527dab60ffebfc90a7b0`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2D02 — 가려진 쓰개 프레임 미판정

혼동 경계: A covered hood profile cannot prove concealed brass wire; inspect an exposed construction view separately.

픽셀 기준: UNOBSERVABLE_NOT_PASS.

근거: [Head dress frame - London Museum](https://www.londonmuseum.org.uk/collections/v/object-117855/head-dress-frame/) — Angular gable and curved French hood profiles are distinguished; concealed wire is unobservable when covered.

후보: `cand_b7c71f55c87455578c1d8b9e52362f01`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2D03 — 폴로네즈 숨은 고정 기구 미판정

혼동 경계: Three puffs do not show whether inner rings, cords, ribbons or outer buttons produced them.

픽셀 기준: UNOBSERVABLE_NOT_PASS.

근거: [Polonaise - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/83887) — Three lifted back-skirt sections expose petticoat; alternative hidden lifting mechanisms cannot be jointly assumed.

후보: `cand_0817cacc1dde5883a0b5eb77593f9cdf`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2D04 — 포맨더 향기·예방 효능 미판정

혼동 경계: Visible compartments do not prove aroma, contents or disease prevention.

픽셀 기준: UNOBSERVABLE_NOT_PASS.

근거: [Pomander - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/196980) — Hinged compartments, sliding lids and screwcap loop; no medical efficacy or smell qualification.

후보: `cand_5560c8989eb75665bea04d713a32d010`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2D05 — 장식 빗 한 개로 파뤼르 전체 충족 금지

혼동 경계: A comb is one object; matched jewelry requires the requested separate pieces and correspondence to be visible.

픽셀 기준: UNOBSERVABLE_NOT_PASS.

근거: [Comb (part of a set) - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/197155) — Gold/amethyst object and matched-set definition; individual comb does not prove a full parure.

후보: `cand_77f0321982b153f9bc04bbfaef78a10c`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.

## R2D06 — 퇴장 순서·반복 의례 미판정

혼동 경계: A still posture cannot demonstrate a curtsy followed by stepping aside and backing away.

픽셀 기준: UNOBSERVABLE_NOT_PASS.

근거: [Court gown and train, 1907 - ASU FIDM Museum](https://fidmmuseum.org/learn/articles/court-gown-and-train-1907) — A curtsy/backing-away sequence is temporal context, not proof from a single still.

후보: `cand_bb2bb715f491573fbe56849bff8a28af`. native 승인 false; partial 및 관측 불가는 통과로 집계하지 않는다.
