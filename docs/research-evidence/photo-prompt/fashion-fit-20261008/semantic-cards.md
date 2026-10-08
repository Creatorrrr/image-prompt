# 패션 핏 시각 의미 상세 카드

2026-10-08 KST. 64개 의미군과 119개 후보 문장 초안이다. 실제 신규 엔트리 수가 아니다. 중복 검토·소유자 결속·효과 범위 검토·runtime 변환은 실행 계획에 남아 있다.

문장들은 서로 다른 선택형 변형이다. 카드 전체를 한 프로필의 필수 all-of로 합치지 않는다. 수치·촉감·제작 이력·숨은 구조·동적 성능은 정지 사진의 hard gate로 만들지 않는다.

## FF01 부위별 여유와 측정 여유량

여유량은 부위별 완성복 치수와 신체 치수의 차이다. 사진에서는 분리된 윤곽·접촉 구역만 관찰한다.

- 소유자: `declared garment panels`. 축: `ease`. 우선순위: `P0`.
- 속성 범위: `fit.local_ease`.
- 혼동 경계: 플러스·제로·마이너스 여유의 수치를 사진의 간격으로 역산하지 않는다. 밀착만으로 negative ease를 확정하지 않는다.
- 관찰 조건: 동일 옷의 경계와 해당 몸 부위가 읽혀야 한다. 치수는 별도 측정 자료를 요구한다.
- 검토할 기존 ID: `pfe_skimming_candidate`
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Proper Cloth: Standard Sizes, Types of Fit, and Size Charts](https://propercloth.com/reference/standard-sizes-types-of-fit-and-size-charts/)

후보 표현 초안:

- The shirt hangs away from the waist; its side panels leave visible space beside the same torso.
- The dress follows the upper torso while its skirt hangs with separate folds below the hip.

## FF02 피티드·스키밍·밀착의 구별

피티드는 형태를 맞춘 설계이며 스키밍은 국소 접촉 사이에 떨어지는 직물 구간이 남는다.

- 소유자: `declared dress or top`. 축: `contact`. 우선순위: `P0`.
- 속성 범위: `fit.contact_distribution`.
- 혼동 경계: 피티드·타이트·사이즈 부족·압박복을 한 축으로 합치지 않는다. snug가 통증을 뜻하지 않는다.
- 관찰 조건: 원단 외곽과 접촉·비접촉 구역이 같은 옷에서 읽혀야 한다.
- 검토할 기존 ID: `pfe_skimming`, `pfe_skimming_candidate`, `bias_cut_body_skimming_drape`
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Seamwork: What's So Great About Princess Seams?](https://www.seamwork.com/sewing-patterns/whats-so-great-about-princess-seams)

후보 표현 초안:

- The dress fabric touches the torso at selected curves; hanging folds bridge the spaces between those contact areas.
- The top follows the torso continuously; its neck and hem remain distinct textile edges.

## FF03 루스·릴랙스드·오버사이즈

국소 여유, 전체 분량, 의도된 큰 비율을 따로 모델링한다.

- 소유자: `declared shirt or jacket`. 축: `volume`. 우선순위: `P0`.
- 속성 범위: `fit.body_clearance`, `fit.shoulder.seam_position`, `fit.sleeve_width`.
- 혼동 경계: 브랜드의 regular와 classic을 고정 수치로 순서화하지 않는다. 한 장의 사진이 큰 사이즈 구매와 oversized 설계 이력을 구별하지 못한다.
- 관찰 조건: 몸통·어깨·소매 중 실제 요청된 구역을 함께 읽을 수 있어야 한다.
- 검토할 기존 ID: `ctx_c150`
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Levi's: Men's Denim Fit Guide](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Proper Cloth: Standard Sizes, Types of Fit, and Size Charts](https://propercloth.com/reference/standard-sizes-types-of-fit-and-size-charts/)

후보 표현 초안:

- The shirt has roomy torso panels and wide sleeves; both remain visibly separate from the wearer's contours.
- The jacket extends broadly across the shoulders; its roomy sleeves and torso share the same enlarged proportions.

## FF04 박시 윤곽과 짧은 비율

박시는 허리 수축이 약한 몸통 윤곽이고 cropped·shrunken은 길이·비율 선택이다.

- 소유자: `declared top`. 축: `silhouette`. 우선순위: `P0`.
- 속성 범위: `silhouette.torso_outline`, `length.hem_landmark`.
- 혼동 경계: 박시가 긴 옷이나 drop shoulder를 필수로 만들지 않는다. shrunken을 세탁 수축의 증거로 쓰지 않는다.
- 관찰 조건: 몸판 양쪽 외곽과 밑단, 요청된 기준선이 보인다.
- 검토할 기존 ID: `ctx_c150`
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Proper Cloth: Standard Sizes, Types of Fit, and Size Charts](https://propercloth.com/reference/standard-sizes-types-of-fit-and-size-charts/)

후보 표현 초안:

- The cropped jacket has nearly straight side edges; its broad hem ends above the trouser waistband.
- The short top has a broad rectangular body; its hem remains level while the sleeves keep their separately requested length.

## FF05 커비·애슬레틱의 부위 비율

커비·애슬레틱은 특정 부위의 상대적 분량을 조정하는 제품 체계다.

- 소유자: `declared trousers or shirt`. 축: `regional_ratio`. 우선순위: `P0`.
- 속성 범위: `fit.waist_to_hip_distribution`, `fit.thigh_ease`, `fit.chest_to_waist_distribution`.
- 혼동 경계: curvy fit을 plus size·curvy body·가슴 확대와 합치지 않는다. Madewell의 치수 기준을 보편 기준으로 복사하지 않는다.
- 관찰 조건: 이미 설정된 착용자의 몸을 유지한다. 상품·패턴 설명과 외관 증거를 분리한다.
- 검토할 기존 ID: `clt_ct014_v1`
- 한정된 근거: [Levi's: Men's Denim Fit Guide](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Madewell: Women's Denim: Our Jeans Guide](https://www.madewell.com/womens/denim/)

후보 표현 초안:

- The trousers have a contoured waistband close to the waist; their hip and upper-thigh panels retain more room.
- The shirt has space through the chest and shoulders; its side seams narrow toward the waist without changing the wearer.

## FF06 A·H·I·X·Y 윤곽

의복의 어깨·허리·힙·밑단 폭 관계를 정의하고 문자 이름은 접근 표현으로 둔다.

- 소유자: `declared dress or ensemble`. 축: `silhouette`. 우선순위: `P1`.
- 속성 범위: `silhouette.width_distribution`, `fit.waist_suppression`.
- 혼동 경계: hourglass garment가 hourglass body를 자동 생성하지 않는다. H·I는 문맥에 따라 겹치므로 엄격한 상호 배타 분류로 만들지 않는다.
- 관찰 조건: 비교에 필요한 의복 윤곽 구역이 모두 프레임 안에 남는다.
- 검토할 기존 ID: `one_piece_dress_construction`
- 한정된 근거: [Victoria and Albert Museum: Corsets, Crinolines and Bustles: Fashionable Victorian Underwear](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [Pronovias: Wedding Dresses and Bridal Gowns](https://www.pronovias.com/wedding-dresses)

후보 표현 초안:

- The dress widens progressively from its upper body toward the hem; both outer edges form a clear A-shaped garment outline.
- The ensemble is wider at the shoulders and skirt than at the cinched waist; the width contrast belongs to the clothing.

## FF07 코쿤·벌룬·블루종 볼륨 배치

최대 볼륨이 생기는 위치와 상·하단 수축, 고정 밑단 위 부풀음을 따로 기록한다.

- 소유자: `declared coat or blouse`. 축: `silhouette`. 우선순위: `P1`.
- 속성 범위: `silhouette.convex_volume`, `fit.hem_gathering`.
- 혼동 경계: 헐렁함만으로 코쿤·벌룬을 만족하지 않는다. O-line·tulip은 선택한 실제 윤곽을 기준으로 세분한다.
- 관찰 조건: 중간 볼륨과 끝단의 관계가 가리지 않은 동일 의복에 보인다.
- 검토할 기존 ID: `cocoon_relaxed_drape`
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Victoria and Albert Museum: Corsets, Crinolines and Bustles: Fashionable Victorian Underwear](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

후보 표현 초안:

- The coat's side edges bow outward around the torso; the lower garment narrows again toward its hem.
- The blouse gathers into a fitted waist band; loose fabric blouses outward immediately above that band.

## FF08 머메이드·트럼펫의 퍼짐 시작점

밀착 구간의 끝과 퍼짐 시작 위치를 실제 신체 기준선에 연결한다.

- 소유자: `declared gown skirt`. 축: `flare`. 우선순위: `P0`.
- 속성 범위: `fit.hip_thigh_contact`, `silhouette.flare_origin`.
- 혼동 경계: 같은 Pronovias 페이지도 명칭을 동의어로 쓰고 다른 문단에서는 구별한다. 이름만으로 무릎 위치를 hard 요구하지 않는다. 인어 신체와 분리한다.
- 관찰 조건: 허리·힙·허벅지·퍼짐 전환·밑단이 읽히는 의상 프레임이 필요하다.
- 검토할 기존 ID: `one_piece_dress_construction`
- 한정된 근거: [Pronovias: Mermaid Wedding Dresses](https://www.pronovias.com/wedding-dresses/mermaid)

후보 표현 초안:

- The gown follows the hips and thighs closely; its skirt begins a pronounced flare near the knees.
- The gown's skirt starts widening above the knees; the widening develops gradually toward the hem.

## FF09 드롭·익스텐디드 숄더의 경계 위치

드롭 숄더는 몸의 어깨 끝보다 팔 쪽으로 내려간 소매 연결선으로 표현한다.

- 소유자: `declared shirt or jacket`. 축: `shoulder`. 우선순위: `P0`.
- 속성 범위: `fit.shoulder.seam_position`, `structure.sleeve_attachment`.
- 혼동 경계: 어깨만 넓은 padded shoulder·래글런 사선·착용자 넓은 어깨를 같은 의미로 취급하지 않는다.
- 관찰 조건: 소매 연결선과 어깨 기준이 읽힌다. 포즈 때문에 내린 어깨와 구별한다.
- 검토할 기존 ID: `sff_pro_c24`
- 한정된 근거: [Proper Cloth: Advanced Tips for Tailored Jacket Fit](https://propercloth.com/reference/advance-tips-for-tailored-jacket-fit/), [Mood Fabrics / Sewciety: All About Sleeves](https://blog.moodfabrics.com/all-about-sleeves/)

후보 표현 초안:

- The shirt's sleeve-attachment seam sits beyond the shoulder tip on the upper arm; the sleeve hangs from that lower join.
- The jacket shoulder extends outward beyond the wearer's shoulder; its sleeve attaches at the extended garment edge.

## FF10 내추럴·스트럭처드·로프드 숄더

관찰되는 어깨 경사와 윤곽 유지, 소매산의 국소 솟음으로 기술한다.

- 소유자: `declared tailored jacket`. 축: `shoulder`. 우선순위: `P1`.
- 속성 범위: `silhouette.shoulder_profile`, `structure.sleeve_head`.
- 혼동 경계: 겉의 단단한 윤곽만으로 패드·캔버스 유무를 확정하지 않는다. roped는 넓은 어깨의 동의어가 아니다.
- 관찰 조건: 어깨-소매산 경계가 가리지 않는다. 내부 원인은 분해 자료가 있어야 확정한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Proper Cloth: Jacket Construction and the Options Proper Cloth Offers](https://propercloth.com/reference/jacket-construction-and-the-options-we-offer/), [Proper Cloth: Advanced Tips for Tailored Jacket Fit](https://propercloth.com/reference/advance-tips-for-tailored-jacket-fit/)

후보 표현 초안:

- The jacket follows the shoulder slope with a smooth sleeve transition; its shoulder outline remains softly rounded.
- The sleeve head rises slightly above the shoulder join; a narrow ridge outlines that same attachment seam.

## FF11 셋인·래글런 소매 연결선

몸판 암홀에 연결되는 곡선 솔기와 목 부근에서 겨드랑이로 향하는 사선 솔기를 구별한다.

- 소유자: `declared sleeved garment`. 축: `attachment`. 우선순위: `P1`.
- 속성 범위: `structure.sleeve_attachment`.
- 혼동 경계: 소매의 밀착도·길이·패드 유무는 별도 변수다. 래글런을 drop shoulder로 대체하지 않는다.
- 관찰 조건: 연결선의 양 끝과 같은 소매·몸판 소유가 읽힌다.
- 검토할 기존 ID: `clt_ct044_v1`, `clt_ct044_v2`, `clothing_ct044_v1`
- 한정된 근거: [Mood Fabrics / Sewciety: All About Sleeves](https://blog.moodfabrics.com/all-about-sleeves/)

후보 표현 초안:

- A curved seam joins the separate sleeve to the shirt's armhole; the join surrounds the shoulder socket.
- A diagonal seam runs from the garment neckline toward the underarm; it separates the sleeve panel from the torso panel.

## FF12 돌먼·배트윙·기모노 컷의 연속부

몸판에서 팔 아래로 이어지는 넓은 직물 구간과 소매-몸판의 연결 방식을 기술한다.

- 소유자: `declared broad-underarm top`. 축: `attachment`. 우선순위: `P1`.
- 속성 범위: `structure.underarm_connection`, `fit.underarm_volume`.
- 혼동 경계: 명칭별 봉제법은 제품마다 달라질 수 있다. 서양 kimono-cut sleeve를 전통 기모노 전체 구조로 확대하지 않는다.
- 관찰 조건: 팔 아래 공간을 읽을 수 있는 포즈가 필요하지만 특정 고정 자세를 전역 규칙으로 쓰지 않는다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Mood Fabrics / Sewciety: All About Sleeves](https://blog.moodfabrics.com/all-about-sleeves/), [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [Seamwork: Introducing the Opal Sewing Pattern](https://www.seamwork.com/sewing-patterns/introducing-the-opal-sewing-pattern)

후보 표현 초안:

- Broad fabric continues from the torso beneath the raised arm; the underarm curve descends well below the armpit.
- The top's body and sleeve form one continuous fabric area across the shoulder; the sleeve narrows toward the wrist.

## FF13 암홀 높이·소매 피치·이세

암홀 위치는 보이는 경계 관계다. 소매산 이세·피치의 정확한 설계값은 패턴·측정 근거가 필요하다.

- 소유자: `declared armhole and sleeve`. 축: `construction_measurement`. 우선순위: `P1`.
- 속성 범위: `fit.armhole_depth`, `structure.sleeve_orientation`.
- 혼동 경계: 주름 하나를 소매 피치나 어깨 경사 한 원인으로 확정하지 않는다. 이세를 눈에 띄는 개더로 대체하지 않는다.
- 관찰 조건: 겨드랑이와 암홀 경계가 보인다. 숨은 설계·수치는 기술 메타데이터로 남긴다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Proper Cloth: Advanced Tips for Tailored Jacket Fit](https://propercloth.com/reference/advance-tips-for-tailored-jacket-fit/), [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)

후보 표현 초안:

- The armhole edge sits close beneath the armpit; the sleeve joins the body at that high boundary.
- The garment armhole descends below the armpit; extra fabric hangs between the torso and sleeve junction.

## FF14 퍼프·지고의 상부 볼륨

볼륨이 모인 상부 구역과 아래팔의 좁은 구역을 따로 지정한다.

- 소유자: `declared sleeve`. 축: `sleeve_volume`. 우선순위: `P1`.
- 속성 범위: `silhouette.sleeve_volume`, `structure.sleeve_gathering`.
- 혼동 경계: puff를 모든 긴 풍성한 소매와 합치지 않는다. gigot의 역사적 시기를 현대 소매 후보에 자동 부여하지 않는다.
- 관찰 조건: 상부 볼륨·팔꿈치 전후 변화·끝단 중 해당 변형의 필수 구역이 보인다.
- 검토할 기존 ID: `clt_ct046_v2`, `clothing_ct046_v2`
- 한정된 근거: [Mood Fabrics / Sewciety: All About Sleeves](https://blog.moodfabrics.com/all-about-sleeves/), [Fashion Institute of Technology: Gigot Sleeve](https://fashionhistory.fitnyc.edu/gigot-sleeve/)

후보 표현 초안:

- The short sleeve gathers into the shoulder seam; a rounded puff expands between that seam and the sleeve edge.
- The sleeve is very full above the elbow; its lower portion narrows closely toward the wrist.

## FF15 비숍·벨 소매의 끝단 차이

비숍은 풍성한 긴 소매와 모인 손목, 벨은 열린 퍼지는 끝단으로 구별한다.

- 소유자: `declared sleeve and cuff`. 축: `sleeve_volume`. 우선순위: `P0`.
- 속성 범위: `fit.cuff_gathering`, `silhouette.sleeve_flare`.
- 혼동 경계: 같은 소매에 좁게 모인 커프스와 열린 벨 끝단을 동시에 강제하지 않는다.
- 관찰 조건: 상부에서 끝단까지의 연결과 실제 커프스 유무가 보인다.
- 검토할 기존 ID: `clt_ct047_v1`, `clothing_ct047_v1`
- 한정된 근거: [Mood Fabrics / Sewciety: All About Sleeves](https://blog.moodfabrics.com/all-about-sleeves/)

후보 표현 초안:

- The long full sleeve gathers into a narrow wrist cuff; soft folds expand above the cuff.
- The sleeve widens toward a freely open wrist edge; the flared end hangs without a gathered cuff.

## FF16 랜턴·마리의 분절 볼륨

반복 결속 구간과 그 사이의 팽창을 기록한다. lantern은 Oliver 패턴의 실제 용어로 확인했으며 개별 패널 도해는 추가 확인 후 분리한다.

- 소유자: `declared segmented sleeve`. 축: `sleeve_volume`. 우선순위: `P2`.
- 속성 범위: `silhouette.sleeve_segments`, `structure.sleeve_panel_joins`.
- 혼동 경계: Marie의 반복 결속을 임의의 주름 많은 소매로 대체하지 않는다. lantern의 명칭·제품 예 확인과 특정 연결·볼륨의 검증은 구분한다.
- 관찰 조건: 각 분절과 결속 경계가 모두 보인다. 이름만 있는 항목은 승격 보류한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Mood Fabrics / Sewciety: All About Sleeves](https://blog.moodfabrics.com/all-about-sleeves/), [Seamwork: All About the Oliver Top](https://www.seamwork.com/sewing-patterns/all-about-the-oliver-top)

후보 표현 초안:

- Several narrow bands gather the long sleeve at separate levels; rounded fabric segments swell between those bands.

## FF17 목둘레의 평면 곡선

좌우 가장자리·중앙 저점·모서리·곡률을 기술한다. 깊이와 기본 곡선을 분리한다.

- 소유자: `declared top neckline`. 축: `neckline`. 우선순위: `P1`.
- 속성 범위: `neckline.outline`, `neckline.depth`.
- 혼동 경계: V-neck이 plunge 깊이를 강제하지 않는다. round·crew·scoop·U의 상품 경계는 문맥에 따른다.
- 관찰 조건: 목둘레 전체 경계와 필요한 쇄골·가슴 기준이 읽힌다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Pronovias: Sweetheart Neckline Wedding Dresses](https://www.pronovias.com/wedding-dresses/sweetheart-neckline), [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/)

후보 표현 초안:

- Two neckline edges descend diagonally toward one central V point; the same top retains continuous fabric below that point.
- The bodice's upper edge forms two rounded arcs; they meet in a lower central notch.

## FF18 카울·모크·터틀·퍼널 목 구조

높게 감싸는 직물과 접어 내린 목 부분, 여분 원단이 늘어지는 앞주름을 구별한다.

- 소유자: `declared neck fabric`. 축: `neckline`. 우선순위: `P1`.
- 속성 범위: `neckline.height`, `structure.neck_folds`.
- 혼동 경계: 높은 네크라인이 전신 밀착도·보온 성능을 뜻하지 않는다. cowl은 액세서리 스카프와 소유를 구별한다.
- 관찰 조건: 목 부위 직물의 몸판 연결과 접힘 경계가 보인다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [Pronovias: Sweetheart Neckline Wedding Dresses](https://www.pronovias.com/wedding-dresses/sweetheart-neckline)

후보 표현 초안:

- Extra fabric descends from the top's neckline into several soft front folds; those folds remain part of the same garment.
- The tall neck fabric folds outward over itself; its doubled edge surrounds the wearer's neck.

## FF19 홀터·오프·콜드·원숄더 지지

드러난 어깨, 끈의 연결점, 내려온 목둘레 가장자리를 각각 기록한다.

- 소유자: `declared bodice and straps`. 축: `coverage_topology`. 우선순위: `P0`.
- 속성 범위: `coverage.shoulder`, `structure.strap_attachment`.
- 혼동 경계: strapless와 tube top, halter와 racerback은 구조 차원이다. 어깨 노출을 전신 노출·신체 변경으로 확대하지 않는다.
- 관찰 조건: 어깨 경계와 끈·소매가 몸판에 연결되는 지점이 읽힌다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Pronovias: Sweetheart Neckline Wedding Dresses](https://www.pronovias.com/wedding-dresses/sweetheart-neckline), [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/)

후보 표현 초안:

- The bodice straps lead around the neck; both shoulders remain outside the garment's supporting straps.
- The garment's upper edge runs below both shoulder tips; its sleeves connect to the lowered bodice edge.

## FF20 키홀·오픈백·컷아웃의 연결

실제 빈 개구부와 원단으로 연결된 패널을 구분하고 위치·둘레·연결점에 소유를 준다.

- 소유자: `declared garment opening`. 축: `coverage_topology`. 우선순위: `P1`.
- 속성 범위: `coverage.opening_location`, `structure.panel_connection`.
- 혼동 경계: 원단의 작은 무늬·그림자·피부색 안감을 실제 구멍으로 오인하지 않는다. backless의 범위는 선택한 디자인으로 한정한다.
- 관찰 조건: 개구부의 둘레와 그 안의 피부·안쪽 층이 실제로 읽힌다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [Pronovias: Sweetheart Neckline Wedding Dresses](https://www.pronovias.com/wedding-dresses/sweetheart-neckline)

후보 표현 초안:

- A small enclosed opening sits beneath the neckline; its complete fabric boundary remains connected to the surrounding top.
- The dress has an open back region; its side panels stay connected at the separately requested waist and shoulder supports.

## FF21 엠파이어·드롭·바스크 허리선

연결선의 높이와 중앙 V·U 형태를 몸의 자연 허리와 구별한다.

- 소유자: `declared bodice-skirt join`. 축: `waist_landmark`. 우선순위: `P0`.
- 속성 범위: `structure.waist_seam_position`, `structure.waist_seam_outline`.
- 혼동 경계: 높은 선이 임신·큰 가슴을 뜻하지 않는다. 바지 허리단·가슴 아래선·드레스 연결선을 구분한다.
- 관찰 조건: 연결선과 해석에 필요한 몸통 기준이 보인다.
- 검토할 기존 ID: `clt_ct075_v2`, `clt_ct014_v1`
- 한정된 근거: [Victoria and Albert Museum: Corsets, Crinolines and Bustles: Fashionable Victorian Underwear](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [Fashion Institute of Technology: 1880](https://fashionhistory.fitnyc.edu/1880-2/)

후보 표현 초안:

- The bodice joins the skirt along a seam directly below the bust; the skirt hangs from that elevated join.
- The dress's bodice-skirt seam sits below the natural waist; the torso panel continues down to that lower join.

## FF22 허리 수축과 조절 기구

벨트·끈·탄성·다트·옆선으로 의복의 허리 분량이 줄어드는 위치를 설명한다.

- 소유자: `declared waist garment`. 축: `waist_shaping`. 우선순위: `P0`.
- 속성 범위: `fit.waist_suppression`, `structure.waist_adjuster`.
- 혼동 경계: 신치드 의복을 착용자의 실제 허리 축소로 확정하지 않는다. elastic·drawstring·belt를 한 구조로 합치지 않는다.
- 관찰 조건: 의복의 좁아짐과 선언한 조절 기구의 연결이 함께 보인다.
- 검토할 기존 ID: `clt_ct060_v2`, `clt_ct031_v2`
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Seamwork: What's So Great About Princess Seams?](https://www.seamwork.com/sewing-patterns/whats-so-great-about-princess-seams)

후보 표현 초안:

- A belt encircles the dress at the waist; the fabric gathers directly into the belt's narrowed region.
- The jacket's side seams curve inward at the waist; the garment widens again over the hips.

## FF23 라이즈·밑위 길이·밑위 깊이

허리단 위치, 앞뒤 밑위 곡선 길이, 수직 깊이를 독립 변수로 둔다.

- 소유자: `declared trousers top block`. 축: `rise`. 우선순위: `P0`.
- 속성 범위: `fit.waistband_landmark`, `structure.crotch_junction`.
- 혼동 경계: low-rise와 drop-crotch를 동의어로 만들지 않는다. high-rise가 high-leg를 뜻하지 않는다. 패턴의 crotch extension은 보이지 않으면 수치 검증하지 않는다.
- 관찰 조건: 허리단과 다리 분기 지점이 읽힌다. 신체 표식이 가리면 정확한 높이는 불확실로 둔다.
- 검토할 기존 ID: `clt_ct014_v1`
- 한정된 근거: [Levi's: Men's Denim Fit Guide](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Proper Cloth: Standard Sizes, Types of Fit, and Size Charts](https://propercloth.com/reference/standard-sizes-types-of-fit-and-size-charts/), [Tilly and the Buttons: Common Trouser Fitting Adjustments](https://tillyandthebuttons.com/blogs/sewing/common-trouser-fitting-adjustments)

후보 표현 초안:

- The trouser waistband sits above the wearer's natural waist; the two leg tubes begin at their separately defined crotch junction.
- The trouser leg junction hangs below the body's crotch; the waistband retains its separately requested height.

## FF24 스트레이트·슬림·테이퍼드의 직교성

슬림은 지역 여유, 테이퍼드는 폭이 줄어드는 방향이다. straight는 비교 구간의 폭 변화를 뜻한다.

- 소유자: `declared trouser legs`. 축: `leg_geometry`. 우선순위: `P0`.
- 속성 범위: `fit.thigh_ease`, `silhouette.knee_to_hem_width`.
- 혼동 경계: tapered 단어를 화장·선·귀 끝 형태에서 의상으로 가져오지 않는다. slim이 발목 밀착을 필수로 만들지 않는다.
- 관찰 조건: 두 다리의 허벅지·무릎·밑단 외곽이 읽힌다. 카메라 원근을 감안한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Levi's: Men's Denim Fit Guide](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Levi's Customer Service: Levi's Product Size Guide](https://help.levi.com/hc/en-us/articles/360025097092-Levi-s-Product-Size-Guide)

후보 표현 초안:

- The trousers retain room through the upper thighs; each leg narrows from the knee toward the ankle opening.
- The trouser legs remain narrow through the thighs; their knee and hem widths change little along the lower leg.

## FF25 부츠컷·플레어·벨보텀

폭이 늘어나기 시작하는 구역과 밑단의 상대 폭으로 분해한다.

- 소유자: `declared lower trouser legs`. 축: `leg_geometry`. 우선순위: `P1`.
- 속성 범위: `silhouette.flare_origin`, `silhouette.hem_width`.
- 혼동 경계: 허벅지 밀착·원단·굽·성별·시대는 명칭만으로 정하지 않는다. bell-bottom의 퍼짐 크기는 변형별로 정의한다.
- 관찰 조건: 무릎 아래 전환과 밑단이 같은 다리에 읽힌다.
- 검토할 기존 ID: `clt_ct013_v2`, `clothing_ct013_v2`, `y2kr_bootcut`
- 한정된 근거: [Levi's: Men's Denim Fit Guide](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Levi's Customer Service: Levi's Product Size Guide](https://help.levi.com/hc/en-us/articles/360025097092-Levi-s-Product-Size-Guide)

후보 표현 초안:

- Each trouser leg is narrower at the knee; it widens modestly toward an opening that falls over the shoe.
- The lower trouser legs flare markedly below the knees; the wide hems preserve the distinct two-leg structure.

## FF26 배럴·호스슈와 벌룬 팬츠

볼록한 옆선·최대 분량·밑단의 재수축을 독립 관계로 둔다.

- 소유자: `declared curved trouser legs`. 축: `leg_geometry`. 우선순위: `P0`.
- 속성 범위: `silhouette.outer_leg_curve`, `silhouette.volume_peak`, `fit.hem_taper`.
- 혼동 경계: 현재 벌룬 프로필은 매우 가까운 의미다. barrel 이름의 부재가 신규 시각 구조의 부재는 아니다. horseshoe는 브랜드별 변형 확인이 남았다.
- 관찰 조건: 양쪽 옆선과 밑단이 보인다. 안쪽 다리 공간은 요청된 경우에만 조건으로 삼는다.
- 검토할 기존 ID: `balloon_leg_curve_tapered_hem`, `balloon_curved_leg_tapered_hem`
- 한정된 근거: [Levi's: Men's Denim Fit Guide](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Madewell: Women's Denim: Our Jeans Guide](https://www.madewell.com/womens/denim/)

후보 표현 초안:

- Both trouser outer seams bow outward around the mid-leg; each curved leg narrows smoothly into a smaller hem.
- The trousers have rounded volume through the upper legs; their lower openings taper without gathered ankle cuffs.

## FF27 하렘·조거·큐롯의 끝점

다리 분기 높이·끝단 모음·개별 바지통 길이를 기록한다.

- 소유자: `declared trousers and cuffs`. 축: `leg_topology`. 우선순위: `P1`.
- 속성 범위: `structure.leg_bifurcation`, `fit.ankle_gathering`, `length.hem_landmark`.
- 혼동 경계: harem의 느슨한 가랑이와 jogger의 커프스는 서로 다른 차원이다. culottes의 치마 같은 외곽이 한 장 스커트가 되는 것을 막는다.
- 관찰 조건: 두 다리 분기와 각각의 끝단을 읽는다.
- 검토할 기존 ID: `harem_gathered_waist_ankle_cuff`, `gathered_ankle_voluminous_trouser`
- 한정된 근거: [Levi's: Men's Denim Fit Guide](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Tilly and the Buttons: Common Trouser Fitting Adjustments](https://tillyandthebuttons.com/blogs/sewing/common-trouser-fitting-adjustments)

후보 표현 초안:

- Two voluminous trouser legs gather into separate ankle cuffs; loose fabric hangs above each cuff.
- The wide cropped trousers divide into two distinct legs; each free hem ends below the knee.

## FF28 펜슬·시프트·쉬스·보디콘

옆선의 수축, 허리 맞춤, 몸의 여러 곡면을 따르는 정도를 분리한다.

- 소유자: `declared skirt or dress`. 축: `dress_geometry`. 우선순위: `P1`.
- 속성 범위: `silhouette.side_outline`, `fit.waist_contact`, `fit.hip_contact`.
- 혼동 경계: 겉옷 보디콘을 의료·성능 압박과 합치지 않는다. bandage는 밴드 패널 의복과 상처 붕대의 문맥을 구분한다.
- 관찰 조건: 의복 경계와 허리·힙의 대응 구간이 읽힌다.
- 검토할 기존 ID: `one_piece_dress_construction`
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Pronovias: Sweetheart Neckline Wedding Dresses](https://www.pronovias.com/wedding-dresses/sweetheart-neckline)

후보 표현 초안:

- The skirt follows the hips closely; its lower side edges narrow toward the knee-length hem.
- The dress falls from the shoulders with straight side edges; its waist remains visually uncinched.

## FF29 랩·고어·고데·티어드 스커트

원단 패널의 연결·겹침·삽입으로 생긴 분량을 기술한다.

- 소유자: `declared skirt panels`. 축: `panel_topology`. 우선순위: `P1`.
- 속성 범위: `structure.panel_joins`, `structure.wrap_overlap`, `silhouette.lower_fullness`.
- 혼동 경계: 고어드 패널과 삽입 고데, 풀리는 랩과 고정 surplice를 같게 만들지 않는다. 원형 재단의 정확한 각도는 외관만으로 증명하지 않는다.
- 관찰 조건: 솔기·겹침 또는 삽입의 경계와 해당 퍼짐이 연결되어 보인다.
- 검토할 기존 ID: `clt_ct030_v1`, `clt_ct030_v2`, `clothing_ct030_v1`, `clt_ct018_v2`
- 한정된 근거: [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [Seamwork: What's So Great About Princess Seams?](https://www.seamwork.com/sewing-patterns/whats-so-great-about-princess-seams)

후보 표현 초안:

- A triangular fabric insert opens between two skirt seams; the inserted panel widens toward the lower hem.
- One skirt panel crosses over another at the front; a continuous overlapping fabric edge leads toward the tied waist.

## FF30 크롭·미디·맥시·트레인 길이

명칭 대신 밑단이 어디에 끝나며 앞뒤 길이가 어떻게 다른지 명시한다.

- 소유자: `declared garment hem`. 축: `length`. 우선순위: `P1`.
- 속성 범위: `length.hem_landmark`, `length.front_back_difference`.
- 혼동 경계: crop은 tight가 아니다. midi·tea·maxi의 제품별 범위를 고정 센티미터로 만들지 않는다. train은 바닥 뒤로 이어진 같은 옷의 연장부다.
- 관찰 조건: 해당 신체 기준선·밑단·바닥 접촉을 필요한 만큼 보인다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Proper Cloth: What Is a Pant Break?](https://propercloth.com/reference/what-is-pant-break/), [Pronovias: Sweetheart Neckline Wedding Dresses](https://www.pronovias.com/wedding-dresses/sweetheart-neckline)

후보 표현 초안:

- The skirt hem ends between the knee and ankle; its width and contact fit retain their separately requested values.
- The gown hem reaches the floor; a connected length of the same skirt extends behind the wearer across the floor.

## FF31 브레이크·스태킹·풀링

밑단이 신발에 닿아 생긴 굽힘과 반복 쌓임, 바닥에 퍼지는 분량을 구별한다.

- 소유자: `declared trouser hem and shoe or floor`. 축: `hem_contact`. 우선순위: `P0`.
- 속성 범위: `length.hem_contact`, `fit.lower_leg_fold_distribution`.
- 혼동 경계: no-break가 맨발목 노출을 항상 뜻하지 않는다. 발목 크롭과 구두 높이·다리 폭을 따로 보며 통상 자세를 명시한다.
- 관찰 조건: 기립 상태의 밑단·신발 윗면 또는 바닥이 같은 프레임에서 읽힌다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Proper Cloth: What Is a Pant Break?](https://propercloth.com/reference/what-is-pant-break/)

후보 표현 초안:

- The trouser front touches the shoe's upper; one shallow fold interrupts the otherwise straight lower-leg drape.
- Extra trouser length forms several folds above the shoe; the lowest fabric spreads onto the floor beside that shoe.

## FF32 재킷 전면·라펠·벤트

단추 위치, 앞판 겹침, 라펠 접힘, 하단의 벌어짐을 별도 요소로 둔다.

- 소유자: `declared jacket front and back`. 축: `jacket_topology`. 우선순위: `P1`.
- 속성 범위: `structure.front_overlap`, `structure.lapel_fold`, `structure.vent_location`.
- 혼동 경계: single·double-breasted가 slim·wide를 결정하지 않는다. lapel roll과 뒤목 collar roll의 위치를 구분한다.
- 관찰 조건: 검사하는 전면 또는 후면 구성과 실제 연결이 보인다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Proper Cloth: Jacket Construction and the Options Proper Cloth Offers](https://propercloth.com/reference/jacket-construction-and-the-options-we-offer/), [Proper Cloth: Advanced Tips for Tailored Jacket Fit](https://propercloth.com/reference/advance-tips-for-tailored-jacket-fit/), [Savile Row Bespoke Association: Tailoring Terms](https://www.savilerowbespoke.com/about-us/tailoring-terms/)

후보 표현 초안:

- The jacket's front panels overlap across the torso; two visible button columns belong to that same closure.
- The jacket's lower front edges curve apart below the fastening point; the opening remains distinct from its lapel folds.

## FF33 캔버스·안감·내부 구조의 증거

canvas·shoulder pad·lining은 서로 다른 내부 구성이다. 외관 드레이프는 구성의 유일한 증거가 아니다.

- 소유자: `declared opened jacket`. 축: `hidden_construction`. 우선순위: `P0`.
- 속성 범위: `structure.visible_lining`.
- 혼동 경계: unlined를 unstructured로 합치지 않는다. soft tailoring에 캔버스가 없다고 단정하지 않는다.
- 관찰 조건: 안감 후보는 열린 옷에서 실제 안쪽 층이 보일 때만 쓴다. 캔버스 비율은 기술 자료로 남긴다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Proper Cloth: Jacket Construction and the Options Proper Cloth Offers](https://propercloth.com/reference/jacket-construction-and-the-options-we-offer/)

후보 표현 초안:

- The opened jacket reveals a separate inner lining layer; its visible edge follows the inside of the front panel.

## FF34 다트와 프린세스 심

접어 소거한 쐐기형 분량과 두 패널을 잇는 긴 곡선 솔기를 구별한다.

- 소유자: `declared bodice fabric`. 축: `panel_shaping`. 우선순위: `P0`.
- 속성 범위: `structure.dart`, `structure.princess_seam`.
- 혼동 경계: dart를 시선이 dart하는 행동에 연결하지 않는다. princess dress 명칭을 프린세스 심 증거로 쓰지 않는다.
- 관찰 조건: 다트 끝점 또는 패널 연결선이 실제 몸판에 읽힌다.
- 검토할 기존 ID: `clt_ct031_v1`, `clt_ct031_v2`, `clothing_ct031_v1`, `clothing_ct031_v2`, `sff_pro_c01`
- 한정된 근거: [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [Seamwork: What's So Great About Princess Seams?](https://www.seamwork.com/sewing-patterns/whats-so-great-about-princess-seams)

후보 표현 초안:

- A short tapered dart ends near the bust; the folded intake shapes the same bodice fabric.
- A curved seam connects the front and side-front bodice panels; it continues through the shaped waist region.

## FF35 요크·거싯·고어의 패널 소유

새 조각의 경계와 기존 몸판·소매·다리 패널에 붙는 위치를 기록한다.

- 소유자: `declared garment junction`. 축: `panel_topology`. 우선순위: `P1`.
- 속성 범위: `structure.yoke`, `structure.gusset`, `structure.panel_joins`.
- 혼동 경계: 움직임을 돕도록 설계됨과 실제 활동성·편안함의 성능을 구분한다. gusset을 노출 개구부로 자동 번역하지 않는다.
- 관찰 조건: 해당 연결 패널의 둘레와 이웃 원단 연결이 보인다. 가려진 내부 조각은 pixel 미판정이다.
- 검토할 기존 ID: `athletic_gusset_panel`, `baju_kurung_tunic_skirt_boundary`
- 한정된 근거: [Tilly and the Buttons: Common Trouser Fitting Adjustments](https://tillyandthebuttons.com/blogs/sewing/common-trouser-fitting-adjustments), [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)

후보 표현 초안:

- A separate polygonal gusset joins the garment panels at the underarm; each gusset edge connects to adjacent fabric.
- A distinct yoke spans the upper back of the shirt; its lower seam joins the torso panel beneath it.

## FF36 플리트·턱의 접힘 방향

접힘의 산·골·방향과 박아 고정한 구간, 자유롭게 풀리는 구간을 구별한다.

- 소유자: `declared folded fabric panel`. 축: `fold_topology`. 우선순위: `P1`.
- 속성 범위: `structure.pleat_direction`, `structure.fold_attachment`.
- 혼동 경계: 프레스 crease와 sewn tuck를 혼동하지 않는다. box와 inverted box는 접힘 방향을 뒤집은 변형이다.
- 관찰 조건: 반복 접힘의 양쪽 경계와 방향이 읽힌다.
- 검토할 기존 ID: `clt_ct063_v1`, `clt_ct063_v2`, `clothing_ct063_v1`, `clothing_ct063_v2`, `pleat_fold_ridge_valley_geometry`
- 한정된 근거: [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)

후보 표현 초안:

- Several fabric pleats fold in the same direction; each ridge continues from the attached top toward the free hem.
- Two inward-facing folds meet at the center of the panel; the joined folds form an inverted box pleat.

## FF37 개더·셔링·루칭·스모킹

모이는 솔기, 반복 박음선, 장식 연결망을 각각 기술한다.

- 소유자: `declared gathered fabric`. 축: `gather_topology`. 우선순위: `P0`.
- 속성 범위: `structure.gather_anchor`, `structure.stitch_rows`, `structure.smocking_network`.
- 혼동 경계: shirring이 항상 탄성실을 뜻하지 않는다. smocking을 평면 인쇄 다이아몬드로 대체하지 않는다.
- 관찰 조건: 주름 끝과 모음 솔기 또는 반복 스티치의 연결이 읽힌다.
- 검토할 기존 ID: `clt_ct064_v1`, `clt_ct064_v2`, `sw_ruched`, `sw_shirred`, `sw_smocked`
- 한정된 근거: [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)

후보 표현 초안:

- Small fabric folds converge into one gathering seam; that seam anchors their ends on the same panel.
- Several parallel stitch rows cross the panel; small repeated gathers occupy the spaces between the rows.

## FF38 바이어스·드레이프·강성

유연한 처짐, 곧게 버티는 접힘, 보이는 결 방향을 구분한다. 재단 이력은 보이는 결 또는 제작 근거로 뒷받침한다.

- 소유자: `declared textile surface`. 축: `fabric_behavior`. 우선순위: `P0`.
- 속성 범위: `material.drape`, `material.visible_grain_orientation`.
- 혼동 경계: fluid·drapey를 특정 섬유·얇음·비침으로 강제하지 않는다. bias cut이 모든 구역 밀착이나 스판덱스를 뜻하지 않는다.
- 관찰 조건: 원단 가장자리·접힘 방향·중력 또는 접촉 위치가 보인다. 촉감은 사진으로 확정하지 않는다.
- 검토할 기존 ID: `bias_cut_body_skimming_drape`, `pr_fabric_tension_fold_attachment`
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained)

후보 표현 초안:

- The dress forms soft continuous folds from the hip toward its hem; a distinct textile edge separates the drape from the body.
- The jacket fabric holds broad angular folds; its lower edge stays clearly defined rather than collapsing into soft ripples.

## FF39 신축·복원·중량·성분의 비시각성

신축률·복원력·GSM·혼용률은 측정 또는 제품 정보이며 사진의 밀착·주름·비침과 동일하지 않다.

- 소유자: `declared fabric test specimen`. 축: `material_measurement`. 우선순위: `P0`.
- 속성 범위: `material.measured_stretch`, `material.recovery`, `material.mass`, `material.fiber`.
- 혼동 경계: LYCRA는 상표이고 모든 stretch의 일반명은 아니다. four-way의 방향 표기는 공급자 문맥을 확인한다. knit·woven·두께·불투명도를 동일 축으로 합치지 않는다.
- 관찰 조건: 외관 후보와 기술 메타데이터를 나눈다. 전후 상태 없는 한 컷은 recovery·growth·shrinkage의 변화를 증명하지 못한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Apostrophe Patterns: Fabric Stretch](https://apostrophepatterns.com/pages/fabric-stretch), [The LYCRA Company: Quality - LYCRA Frequently Asked Questions](https://one.lycra.com/en/lycra-frequently-asked-questions/quality-lycra), [The LYCRA Company: Made to Measure: LYCRA SPORT Performance Indexing](https://one.lycra.com/en/business/news/made-measure-lycra-sport-performance-indexing)

후보 표현 초안:

측정·공정 메타데이터로 유지한다. 명칭만으로 pixel hard gate를 만들지 않는다.

## FF40 브라의 컵·밴드·고어·와이어

각 컵과 밴드·중앙 연결부·와이어 케이싱을 같은 의복의 구성요소로 연결한다.

- 소유자: `declared bra components`. 축: `support_topology`. 우선순위: `P1`.
- 속성 범위: `structure.cup_band_connection`, `structure.center_gore`, `structure.underwire_casing`.
- 혼동 경계: 컵 용량·깊이·와이어 폭은 서로 다르다. underwire가 보이지 않으면 주름이나 프린트만으로 금속을 확정하지 않는다.
- 관찰 조건: 해당 구성요소가 실제 의복에 보인다. 속에 숨은 뼈대는 도해·제작 근거가 필요하다.
- 검토할 기존 ID: `clt_ct072_v1`, `clothing_ct072_v1`
- 한정된 근거: [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/), [Freya: Bra Fitting Guide - The Perfect Fit](https://www.freyalingerie.com/us/en/advice/the-perfect-fit/), [Bravissimo: The Bravissimo Bra Fitting Guide](https://www.bravissimo.com/bra-fitting-guide/)

후보 표현 초안:

- Two shaped cups connect through a central fabric gore; both cups join the same underband around the torso.
- A curved casing follows the lower boundary of each bra cup; the two casings remain distinct from the shoulder straps.

## FF41 브라 커버리지·성형·패딩

풀·하프·발코니·플런지는 컵 가장자리와 중앙 연결 높이로 분해하고 moulded·padded를 별도로 둔다.

- 소유자: `declared bra cup edges`. 축: `coverage_topology`. 우선순위: `P0`.
- 속성 범위: `coverage.cup_edge`, `structure.center_height`, `structure.visible_padding`.
- 혼동 경계: moulded가 padded를 뜻하지 않는다. bralette가 항상 non-wired는 아니다. shelf bra의 내장 지지층과 열린 받침형 상품 의미를 나눈다.
- 관찰 조건: 보이는 컵 가장자리·스트랩 연결과 실제 padding 증거만 검증한다. 내부 형태·성능은 추정하지 않는다.
- 검토할 기존 ID: `clt_ct072_v1`
- 한정된 근거: [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/)

후보 표현 초안:

- The bra's center front sits low between angled cup edges; the outer cup edges remain attached to their straps.
- The bra cups have an open upper edge and laterally placed strap attachments; the underband remains a separate supporting component.

## FF42 컵 들뜸·넘침·밴드 이동의 상태

컵 가장자리와 몸 사이의 빈 공간, 컵 경계 밖 윤곽, 밴드의 비수평을 각각 기록한다.

- 소유자: `declared bra edge and skin boundary`. 축: `fit_state`. 우선순위: `P0`.
- 속성 범위: `fit.cup_edge_gap`, `fit.band_alignment`, `fit.strap_position`.
- 혼동 경계: 컵 개핑을 무조건 큰 컵 한 원인으로 진단하지 않는다. 중앙 고어 밀착 규칙을 모든 무와이어·소프트 브라에 적용하지 않는다.
- 관찰 조건: 검사하는 경계와 피부·직물 사이 공간이 읽혀야 한다. 움직임 이력은 정지 프레임 밖 근거가 필요하다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Freya: Bra Fitting Guide - The Perfect Fit](https://www.freyalingerie.com/us/en/advice/the-perfect-fit/), [Bravissimo: The Bravissimo Bra Fitting Guide](https://www.bravissimo.com/bra-fitting-guide/)

후보 표현 초안:

- A small air gap separates the upper cup edge from the body; the cup and gap belong to the same bra.
- The bra's rear band sits higher than its side band; the change in band height is visible along the same torso.

## FF43 코르셋의 상·하단과 패널

가슴 위·아래에서 끝나는 상단, 허리·힙으로 이어지는 하단, 패널·케이싱을 분리한다.

- 소유자: `declared corset panels`. 축: `bodice_topology`. 우선순위: `P1`.
- 속성 범위: `coverage.upper_edge`, `length.lower_edge`, `structure.bone_casing`.
- 혼동 경계: 현대 steel-boned 상품의 구조를 모든 시대의 corset·stays·corset top에 강제하지 않는다. 몸통 윤곽을 실제 영구 변화로 해석하지 않는다.
- 관찰 조건: 실제 의복 상·하단과 연결된 케이싱이 보인다. 내부 재료는 따로 검증한다.
- 검토할 기존 ID: `clt_ct023_v2`
- 한정된 근거: [LUXE NOIR corset maker: Corset Glossary: Corsetry Terms Explained](https://www.luxenoir.com/pages/corset-glossary), [Victoria and Albert Museum: Corsets, Crinolines and Bustles: Fashionable Victorian Underwear](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

후보 표현 초안:

- The corset's upper edge ends beneath the bust; its shaped panels continue through the waist toward the upper hips.
- The bodice covers the bust and waist; narrow vertical casings follow its connected panel seams.

## FF44 버스크·레이싱·갭·모더스티 패널

앞 여밈의 대응 금속부와 끈·아일릿·양쪽 가장자리·뒤받침 패널을 구별한다.

- 소유자: `declared bodice closure`. 축: `closure_topology`. 우선순위: `P0`.
- 속성 범위: `structure.front_fastener`, `structure.lacing`, `coverage.lacing_backing`.
- 혼동 경계: busk를 지퍼·프린트로 대체하지 않는다. 피부가 가려진 갭도 갭이며, 모더스티 패널을 기본 의상으로 새로 추가하지 않는다.
- 관찰 조건: 여밈의 서로 연결되는 끝점이 보인다. 앞면만 보이면 뒤 레이싱은 UNOBSERVABLE이다.
- 검토할 기존 ID: `clt_ct023_v2`, `clothing_ct023_v2`, `sff_pro_c14`
- 한정된 근거: [LUXE NOIR corset maker: Corset Glossary: Corsetry Terms Explained](https://www.luxenoir.com/pages/corset-glossary), [Victoria and Albert Museum: Corsets, Crinolines and Bustles: Fashionable Victorian Underwear](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

후보 표현 초안:

- The bodice's two front edges are joined by paired metal loops and studs; each loop engages its matching stud.
- Crossed laces pass through eyelets on both bodice edges; a visible fabric panel lies behind the gap between those edges.

## FF45 코르셋 스프링·리덕션·내부 테이프

hip·rib spring은 정의된 위치의 둘레 차이이며 waist reduction은 측정 상태를 명시해야 한다.

- 소유자: `declared corset measurements`. 축: `construction_measurement`. 우선순위: `P2`.
- 속성 범위: `fit.measured_hip_spring`, `fit.measured_rib_spring`, `structure.internal_waist_tape`.
- 혼동 경계: 브랜드의 권장 갭·감량·착용 시간·소재 조건을 보편 규칙으로 복사하지 않는다. 사진의 잘록함은 수치 증거가 아니다.
- 관찰 조건: 치수표·패턴·실측 또는 보이는 내부 테이프 자료가 필요하다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [LUXE NOIR corset maker: Corset Glossary: Corsetry Terms Explained](https://www.luxenoir.com/pages/corset-glossary), [Victoria and Albert Museum: Corsets, Crinolines and Bustles: Fashionable Victorian Underwear](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

후보 표현 초안:

측정·공정 메타데이터로 유지한다. 명칭만으로 pixel hard gate를 만들지 않는다.

## FF46 보정복의 패널과 외관 정리

보이는 강화 패널·밴드·직물 경계를 기술하고 smoothing·sculpting 효과를 제품 주장과 나눈다.

- 소유자: `declared shaping garment`. 축: `support_topology`. 우선순위: `P1`.
- 속성 범위: `structure.control_panel`, `material.surface_continuity`.
- 혼동 경계: 보정복 명칭만으로 몸 치수·건강·영구 변화·압력을 확정하지 않는다.
- 관찰 조건: 실제 패널 경계를 보거나 제작 자료를 쓴다. 겉옷의 매끈함만으로 숨은 보정복을 생성하지 않는다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/), [The LYCRA Company: Made to Measure: LYCRA SPORT Performance Indexing](https://one.lycra.com/en/business/news/made-measure-lycra-sport-performance-indexing)

후보 표현 초안:

- The shaping garment has a distinct reinforced abdominal panel; its boundary remains connected to the adjacent stretch fabric.

## FF47 보디수트·레오타드·유니타드 연결

몸판에서 하부로 이어지는 동일 의복과 개별 다리통의 유무·길이를 정의한다.

- 소유자: `declared one-piece bodywear`. 축: `garment_topology`. 우선순위: `P1`.
- 속성 범위: `structure.torso_lower_connection`, `structure.leg_bifurcation`, `length.leg_coverage`.
- 혼동 경계: catsuit·unitard 등의 상품명 경계는 변형을 확인한다. bodysuit가 투명함·성적 용도·특정 몸을 요구하지 않는다.
- 관찰 조건: 몸판 연결과 두 다리 개구부 또는 다리통이 보인다.
- 검토할 기존 ID: `sw_onepiece`
- 한정된 근거: [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/)

후보 표현 초안:

- The one-piece garment continues through the waist into its brief section; it has two distinct leg openings.
- The fitted garment continues from the torso into two long leg tubes; the waist and leg sections remain one connected item.

## FF48 하이레그와 뒤판 커버리지

다리 개구부의 옆 높이와 뒤판이 덮는 면적·띠 폭을 독립 변수로 둔다.

- 소유자: `declared bodywear brief edges`. 축: `coverage`. 우선순위: `P0`.
- 속성 범위: `coverage.leg_opening`, `coverage.rear_panel`.
- 혼동 경계: high waist와 high leg를 섞지 않는다. cheeky·Brazilian·thong의 범위는 제품마다 달라 고정 비율을 강제하지 않는다.
- 관찰 조건: 옆 다리 경계와 검사하는 앞·뒤판이 실제 보이는 시점이 필요하다.
- 검토할 기존 ID: `sw_candidate_highleg`, `sw_highleg`
- 한정된 근거: [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/)

후보 표현 초안:

- The garment's leg opening rises high at the outer hip; its waist edge remains a separate boundary.
- The brief's rear fabric panel covers the declared area; its edge remains distinct from the garment's waist and leg openings.

## FF49 시어·불투명·일루전·안감

빛이 통과하는 겉감, 실제 피부·안쪽 옷, 피부색 계열 안감의 소유를 분리한다.

- 소유자: `declared fabric layers`. 축: `layer_visibility`. 우선순위: `P0`.
- 속성 범위: `material.transmission`, `structure.visible_lining`, `coverage.illusion_panel`.
- 혼동 경계: 피부색이 보인다고 피부가 노출됐다고 판정하지 않는다. sheer를 tight·nude와 합치지 않는다. 요청 없는 안감을 추가하지 않는다.
- 관찰 조건: 각 층의 경계와 보이는 아래층이 읽힌다. 실제 구멍과 망사 연결을 구별한다.
- 검토할 기존 ID: `sw_onepiece`
- 한정된 근거: [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/)

후보 표현 초안:

- The translucent outer panel reveals a separate lining layer beneath it; the lining edge remains visible at the garment opening.
- The loose sheer sleeve hangs away from the arm; its open weave and the arm beneath it remain separately readable.

## FF50 중앙·옆·아래 개구부의 노출 위치

cleavage·sideboob·underboob 등을 의복 경계와 신체 부위의 위치 관계로 기록한다.

- 소유자: `declared garment aperture`. 축: `coverage`. 우선순위: `P2`.
- 속성 범위: `coverage.opening_location`, `coverage.edge_to_body_region`.
- 혼동 경계: 이 용어를 몸의 크기·성격·성별·사생활 또는 다른 개구부로 확대하지 않는다. cupless·open-cup·open-crotch는 컵·밑부분 구조 의미를 각각 유지한다.
- 관찰 조건: 명시적으로 요청된 위치와 실제 경계만 해석한다. 가려진 부위의 노출 여부를 추정하지 않는다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/), [Collins English Dictionary: Sideboob Definition and Meaning](https://www.collinsdictionary.com/dictionary/english/sideboob)

후보 표현 초안:

- The neckline opening lies between the two cup regions; its location is distinct from the garment's side openings.
- The garment has a lateral opening beside the cup; the side aperture remains separate from its front neckline.

## FF51 겉옷 위 윤곽·VPL·스크런치

직물 위에 드러난 아래층 경계와 뒤중심 모음 구조를 연결한다. bulge·camel toe·wedgie는 요청·제품 문맥을 보존한다.

- 소유자: `declared outer fabric and underwear edge`. 축: `surface_outline`. 우선순위: `P2`.
- 속성 범위: `material.surface_relief`, `structure.rear_gathering`.
- 혼동 경계: VPL을 직접 피부 노출과 합치지 않는다. Levi's Wedgie 제품명을 끼임 상태로 자동 해석하지 않는다. 일반 tight 후보에 국부 윤곽을 덧붙이지 않는다.
- 관찰 조건: 외곽의 선과 그 소유를 읽는다. 숨은 원인을 한 가지로 진단하지 않는다. camel toe 명칭은 Cambridge 사전으로 확인했다. bulge·wedgie 상태 등의 개별 확인은 남았다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Bravissimo: The Bravissimo Bra Fitting Guide](https://www.bravissimo.com/bra-fitting-guide/), [Levi's: Wedgie Straight Women's Jeans](https://www.levi.com/US/en_US/clothing/women/jeans/straight/wedgie-straight-womens-jeans/p/349640287), [Cambridge University Press: Camel Toe - Cambridge English Dictionary](https://dictionary.cambridge.org/us/dictionary/english/camel-toe)

후보 표현 초안:

- A narrow underwear-edge ridge is visible beneath the outer trousers; the outer fabric remains continuous over that trace.
- The rear center seam gathers the garment fabric; small folds converge into that same stitched line.

## FF52 레이서백과 크로스백

Y자 합류와 X자 교차를 별도 접속 관계로 둔다.

- 소유자: `declared back straps and band`. 축: `strap_topology`. 우선순위: `P0`.
- 속성 범위: `structure.back_strap_connection`.
- 혼동 경계: 교차 두 끈이 합쳐진 한 요크가 되지 않게 한다. racerback 명칭만으로 실제 지지 수준을 확정하지 않는다.
- 관찰 조건: 끈의 시작·교차 또는 합류·하부 부착점이 같은 옷에서 보인다.
- 검토할 기존 ID: `racerback_sports_bra_strap_convergence`, `racerback_strap_yoke_convergence`, `crossback_strap_intersection`
- 한정된 근거: [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/), [Nike: The Best Plus-Size Sports Bras From Nike](https://www.nike.com/my/a/best-plus-size-sports-bra)

후보 표현 초안:

- Two shoulder straps converge between the shoulder blades into one central yoke; that yoke connects to the lower band.
- Two straps cross once on the back; each continues to an attachment on the opposite lower side.

## FF53 노 프런트 심·플랫록·심리스

선택한 앞중심 솔기의 유무와 보이는 봉제선의 낮은 돌출을 구분한다.

- 소유자: `declared athletic garment surface`. 축: `seam_topology`. 우선순위: `P1`.
- 속성 범위: `structure.front_center_seam`, `structure.seam_relief`.
- 혼동 경계: seamless가 제품 전체에 봉제가 전혀 없다는 뜻은 아니다. no-front-seam을 모든 밑위 주름 제거로 확정하지 않는다.
- 관찰 조건: 선택 구역과 실제 봉제선이 충분한 해상도로 읽힌다. 시접 내부는 별도 자료가 필요하다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Charlotte Kan pattern designer: Sewing Glossary - Sewing Terms Explained](https://charlottekan.com/blogs/sewingblog/sewing-glossary-sewing-terms-explained), [Coats thread manufacturer: Eliminating Seam Puckering](https://www.coats.com/en-us/info-hub/eliminating-seam-puckering/)

후보 표현 초안:

- The leggings' front center panel is continuous; the visible joining seams lie at its sides instead of its center.
- A low-profile stitched seam joins two athletic fabric panels; the seam remains distinct from a thick raised allowance.

## FF54 아티큘레이션·앉은 자세 대응

곡선 패널·무릎 선형·앞뒤 허리단 위치로 이미 선언된 동작·착용 자세에 대응한다.

- 소유자: `declared trouser knee or seated waistband`. 축: `articulation`. 우선순위: `P1`.
- 속성 범위: `structure.articulation_panel`, `fit.front_back_rise_distribution`.
- 혼동 경계: adaptive를 장애·의료·나이 추정으로 연결하지 않는다. seated-fit 제품의 앞뒤 길이 조정을 전 의상 기본값으로 쓰지 않는다.
- 관찰 조건: 해당 패널 연결 또는 앉은 자세의 앞뒤 허리단이 실제 읽힌다. 성능은 별도 근거다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Tilly and the Buttons: Common Trouser Fitting Adjustments](https://tillyandthebuttons.com/blogs/sewing/common-trouser-fitting-adjustments), [Tommy Hilfiger: Seated Fit Straight Fit Jean](https://usa.tommy.com/en/tommy-adaptive/mens-adaptive/mens-adaptive-sale/seated-fit-straight-fit-jean/7T00370-409.html)

후보 표현 초안:

- Curved panels shape the trouser knee around its bent position; their seams remain connected above and below the joint.
- The seated trousers retain a higher rear waistband; their front panel leaves less loose fabric over the lap.

## FF55 액션 백·조절기·움직임 여유

펼쳐지는 주름과 끈·버클·벨크로의 조절 경로를 보여준다.

- 소유자: `declared garment folds and adjusters`. 축: `adjustment`. 우선순위: `P1`.
- 속성 범위: `structure.action_back`, `structure.adjuster`.
- 혼동 경계: 보이는 조절기가 모든 치수·성능을 보장하지 않는다. 한 컷의 주름은 실제 전후 움직임 여유를 증명하지 않는다.
- 관찰 조건: 고정 끝점·자유 끝점·연결 경로가 읽힌다. 움직임 확인은 시퀀스를 별도로 사용한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Tilly and the Buttons: Common Trouser Fitting Adjustments](https://tillyandthebuttons.com/blogs/sewing/common-trouser-fitting-adjustments), [Savile Row Bespoke Association: Tailoring Terms](https://www.savilerowbespoke.com/about-us/tailoring-terms/)

후보 표현 초안:

- An opened pleat reveals extra fabric beside the shoulder blade; both sides remain joined to the jacket's back panel.
- A drawstring passes through the waistband casing; its two free ends emerge from the same adjustment channel.

## FF56 당김선과 국소 들뜸

원단 당김이 모이는 고정점과 실제 벌어진 틈의 위치를 기록한다.

- 소유자: `declared garment edge or fastening`. 축: `fit_state`. 우선순위: `P0`.
- 속성 범위: `fit.strain_lines`, `fit.edge_gap`, `fit.closure_gap`.
- 혼동 경계: 모든 주름을 poor fit으로 판정하지 않는다. 옷 주름에서 신체 치수 부족·불편·원인을 단정하지 않는다.
- 관찰 조건: 같은 원단의 당김선·고정점·틈 가장자리가 함께 보인다.
- 검토할 기존 ID: `pr_fabric_tension_fold_attachment`
- 한정된 근거: [Proper Cloth: Advanced Tips for Tailored Jacket Fit](https://propercloth.com/reference/advance-tips-for-tailored-jacket-fit/), [Tilly and the Buttons: Common Trouser Fitting Adjustments](https://tillyandthebuttons.com/blogs/sewing/common-trouser-fitting-adjustments)

후보 표현 초안:

- Short tension folds radiate toward the jacket's fastened button; the surrounding front panels pull toward that same point.
- The rear waistband stands away from the lower back; a visible air gap separates the fabric edge from the body.

## FF57 퍼커링·레그 트위스트·결 방향

봉제선 주변의 잔잔한 오그라듦과 다리를 따라 돌아가는 솔기의 위치를 기술한다.

- 소유자: `declared seam and leg panel`. 축: `fit_state`. 우선순위: `P0`.
- 속성 범위: `fit.seam_puckering`, `structure.leg_seam_orientation`.
- 혼동 경계: 퍼커링은 실 장력·원단·피드·치수 변화가 복합적이다. leg twist를 off-grain 하나의 원인으로 확정하지 않는다.
- 관찰 조건: 솔기와 인접 직물의 변형이 읽힌다. 제작 원인은 기술 자료·시험으로 따로 확인한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Tilly and the Buttons: Common Trouser Fitting Adjustments](https://tillyandthebuttons.com/blogs/sewing/common-trouser-fitting-adjustments), [Coats thread manufacturer: Eliminating Seam Puckering](https://www.coats.com/en-us/info-hub/eliminating-seam-puckering/)

후보 표현 초안:

- Small ripples gather immediately beside the seam; the puckering follows the stitched line on the same panel.
- The trouser side seam turns toward the front of the lower leg; its path remains attached to the same leg tube.

## FF58 라이딩 업·롤링·번칭·새깅

올라간 가장자리·접혀 말린 단·뭉친 원단·처진 구역의 현재 상태를 기록한다.

- 소유자: `declared garment hem or band`. 축: `fit_state`. 우선순위: `P1`.
- 속성 범위: `fit.hem_displacement`, `fit.band_roll`, `fit.local_bunching`.
- 혼동 경계: 한 장의 사진은 원래 위치·반복 이동·세탁 이력을 증명하지 못한다. riding up과 단순 cropped를 구분한다.
- 관찰 조건: 원래 기준이 요청·전후 자료에 있으면 이동을, 없으면 현재 위치만 기술한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Tilly and the Buttons: Common Trouser Fitting Adjustments](https://tillyandthebuttons.com/blogs/sewing/common-trouser-fitting-adjustments), [Bravissimo: The Bravissimo Bra Fitting Guide](https://www.bravissimo.com/bra-fitting-guide/)

후보 표현 초안:

- The waistband edge folds outward into a narrow roll; the rolled fabric remains connected to the band beneath it.
- The sleeve fabric bunches above the elbow; its gathered mass is separate from the sleeve's free edge.

## FF59 사이즈·치수 체계·맞춤·보정 과정

POM·flat measurement·sister size·suit drop·RTW·MTO·MTM·bespoke·grading·FBA 등은 치수·공정·체계 정보를 보존한다.

- 소유자: `declared garment specification`. 축: `nonvisual_metadata`. 우선순위: `P2`.
- 속성 범위: `specification.sizing`, `specification.production_process`.
- 혼동 경계: 프티트를 마른 몸, plus를 curvy, unisex를 특정 성별로 자동 생성하지 않는다. bespoke나 true-to-size는 외관 품질의 증거가 아니다.
- 관찰 조건: 치수표·패턴·제작 기록·피팅 과정이 필요하다. 외형 결과가 요청되면 별도 시각 후보로 분해한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Proper Cloth: Standard Sizes, Types of Fit, and Size Charts](https://propercloth.com/reference/standard-sizes-types-of-fit-and-size-charts/), [Bravissimo: The Bravissimo Bra Fitting Guide](https://www.bravissimo.com/bra-fitting-guide/), [Donna Karan: Women's Petite Sizing](https://www.donnakaran.com/pages/copy-of-size-chart-petite-sizing), [Savile Row Bespoke Association: Tailoring Terms](https://www.savilerowbespoke.com/about-us/tailoring-terms/)

후보 표현 초안:

측정·공정 메타데이터로 유지한다. 명칭만으로 pixel hard gate를 만들지 않는다.

## FF60 파니에·크리놀린·버슬의 지지 방향

좌우 확장, 전체 종 모양 부피, 허리 아래 뒤 돌출을 실제 의복 관계로 구분한다.

- 소유자: `declared supported skirt`. 축: `historical_volume`. 우선순위: `P1`.
- 속성 범위: `silhouette.lateral_volume`, `silhouette.rear_projection`, `structure.visible_support`.
- 혼동 경계: 같은 커다란 치맛단으로 세 구조를 대체하지 않는다. 겉 윤곽으로 숨은 받침 재료를 확정하지 않는다.
- 관찰 조건: 측면 또는 정면의 필요한 폭·깊이를 읽거나 공개된 내부 받침 자료를 사용한다.
- 검토할 기존 ID: `hw_lateral_pannier`, `hw_lateral_pannier_1`, `hw_lateral_pannier_2`, `hw_shelf_bustle`, `hw_shelf_bustle_1`, `hw_shelf_bustle_2`
- 한정된 근거: [Victoria and Albert Museum: Corsets, Crinolines and Bustles: Fashionable Victorian Underwear](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [Fashion Institute of Technology: Cage Crinoline](https://fashionhistory.fitnyc.edu/cage-crinoline/), [Fashion Institute of Technology: Panniers](https://fashionhistory.fitnyc.edu/panniers/), [Fashion Institute of Technology: Bum Roll](https://fashionhistory.fitnyc.edu/bum-roll/)

후보 표현 초안:

- The skirt extends strongly to both sides of the waist; its front-to-back depth is smaller than its lateral width.
- The gown projects backward immediately below the waist; the rear skirt falls from that raised projecting mass.

## FF61 스테이스·큐라스·패딩의 시대별 형태

역사적 보디스 길이·형태·받침 구성을 버전별로 묶고 현대 재해석은 분리한다.

- 소유자: `declared long bodice or support`. 축: `historical_structure`. 우선순위: `P2`.
- 속성 범위: `silhouette.torso_outline`, `length.bodice_lower_edge`, `structure.visible_support`.
- 혼동 경계: 모든 stays를 빅토리아 모래시계형으로 만들지 않는다. cuirass bodice가 실제 보호 갑옷을 뜻하지 않는다. bombast와 bum roll은 FIT의 개별 정의를 확인했다. 구조가 가리면 겉 결과만 판정한다.
- 관찰 조건: 시대·용도 출처와 실제 구역이 필요하다. 구조 미관찰이면 겉 결과만 평가한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Victoria and Albert Museum: Corsets, Crinolines and Bustles: Fashionable Victorian Underwear](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [Fashion Institute of Technology: 1880](https://fashionhistory.fitnyc.edu/1880-2/), [Fashion Institute of Technology: Bum Roll](https://fashionhistory.fitnyc.edu/bum-roll/), [Fashion Institute of Technology: Bombast / Bombasted](https://fashionhistory.fitnyc.edu/bombast-bombasted/)

후보 표현 초안:

- The long fitted bodice continues below the natural waist over the upper hips; its lower edge remains distinct from the skirt beneath it.
- A separate support form is visible beneath the lifted skirt layer; the upper fabric rests on that same support.

## FF62 슬래싱·하네스·본디지·해체

절개 안쪽에 나타나는 다른 원단과 실제 스트랩 연결·금속 여밈·해진 가장자리를 기록한다.

- 소유자: `declared fashion straps and layers`. 축: `garment_topology`. 우선순위: `P1`.
- 속성 범위: `structure.strap_anchors`, `structure.slashes`, `material.distress`.
- 혼동 경계: bondage trousers를 성행위 장면으로 자동 확장하지 않는다. body harness를 안전 성능 장비로 확정하지 않는다. distressed가 폭력 원인을 뜻하지 않는다.
- 관찰 조건: 스트랩 끝점·원단 절개 둘레·아래층 소유가 읽힌다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Fashion Institute of Technology / V&A references: Slashing](https://fashionhistory.fitnyc.edu/slashing/), [Victoria and Albert Museum: Vivienne Westwood: Punk, New Romantic and Beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

후보 표현 초안:

- Garment straps connect to visible attachment points on the trousers; the loose strap spans remain separate from the leg seams.
- Repeated cuts open in the outer sleeve fabric; a separate inner textile layer shows through those openings.

## FF63 한국어 인상 표현의 문맥 분해

여리·탄탄·각 잡힌·촤르르·항아리 등을 요청의 의복·부위·거동에 따라 가능한 해석으로 분해한다.

- 소유자: `declared garment and fabric`. 축: `colloquial_interpretation`. 우선순위: `P0`.
- 속성 범위: `fit.local_ease`, `material.drape`, `silhouette.width_distribution`.
- 혼동 경계: 여리핏을 몸 축소·여성성·성격으로 고정하지 않는다. 머슬핏이 실제 근육량을 바꾸지 않는다. 출처가 없는 속어를 정규 규격으로 승격하지 않는다.
- 관찰 조건: 문맥의 의복과 관찰 부위를 먼저 정한다. 해석이 여러 개면 advisory 제안으로 남긴다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Levi's: Men's Denim Fit Guide](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Apostrophe Patterns: Fabric Stretch](https://apostrophepatterns.com/pages/fabric-stretch)

후보 표현 초안:

- The shirt hangs softly from its lowered shoulder joins; long sleeves and flowing fabric create the requested loose impression.
- The garment keeps a clearly defined shoulder edge and straight lower outline; its fabric holds the requested shape.

## FF64 직교 요소를 조합하는 후보 번들

의상 종류·부위 밀착·윤곽·기준선·길이·구조·물성·커버리지를 개별 소유자와 효과 범위로 조합한다.

- 소유자: `declared garment instances`. 축: `composition`. 우선순위: `P0`.
- 속성 범위: `fit.local_ease`, `silhouette.outer_leg_curve`, `length.hem_landmark`, `structure.sleeve_attachment`, `material.transmission`.
- 혼동 경계: 고정 장면·카메라·몸 비율·분위기를 함께 강제하는 preset을 만들지 않는다. 요청되지 않은 constituent는 optional이다.
- 관찰 조건: 각 선택 부품의 선행 의복·층·시점이 실현 가능하고 고정 속성을 보존한다.
- 검토할 기존 ID: 개별 동등성 검토 필요
- 한정된 근거: [Seamwork pattern development: Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Levi's: Men's Denim Fit Guide](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Proper Cloth: Jacket Construction and the Options Proper Cloth Offers](https://propercloth.com/reference/jacket-construction-and-the-options-we-offer/), [Bravissimo: Types of Bra Explained - Bra Style Guide](https://www.bravissimo.com/bra-style-guide/)

후보 표현 초안:

- The cropped boxy jacket has lowered sleeve joins and wide sleeves; its torso and sleeve proportions belong to that same jacket.
- The trousers sit high at the waist with room through the thighs; their lower legs taper toward separate ankle-length hems.

