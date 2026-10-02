# 91개 구체 형상·관계 축의 검토안

각 항목은 연구 제안이다. 기존 owner가 없는 항목도 전체 코퍼스 중복 검토 전에는 신규 프로필로 확정되지 않는다. 게이트는 저자가 제안한 검증 기준이며 실제 픽셀 검증은 미실행이다.

## P1

### stature_scale — 비교 기준이 있는 작은 성인 신장

- 관찰 형태: short adult stature against an explicit same-plane scale reference
- 소유자/속성: `adult_person` / `stature_scale`.
- 구성요소: adult head-to-foot extent; explicit comparison reference; same depth plane.
- 보기·상태: 전신, 같은 깊이 평면의 크기 기준.
- 가까운 반례: 골격 폭이 좁거나 광각으로 짧아 보일 뿐 실제 비교 기준이 없음.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S08](https://www.landsend.co.uk/Bottoms/co/mobile-size-chart-women-bottoms.html).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### compact_frame — 짧은 신장과 별도로 기술한 조밀한 몸통·사지 규모

- 관찰 형태: compact torso and limb frame with separately specified stature
- 소유자/속성: `adult_torso` / `frame_extent`.
- 구성요소: torso transverse extent; limb segment scale; stature declared separately.
- 보기·상태: 전신, 원근 단축이 적은 보기.
- 가까운 반례: 키가 작다는 이유만으로 가는 몸이나 마른 체형을 부여.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S05](https://dictionaryblog.cambridge.org/2012/05/07/body-shapes/), [S07](https://www.merriam-webster.com/dictionary/stocky), [S08](https://www.landsend.co.uk/Bottoms/co/mobile-size-chart-women-bottoms.html).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### stocky_build — 사지 길이에 비해 두툼한 몸통과 팔다리의 체격

- 관찰 형태: relatively thick torso and limbs in relation to segment length
- 소유자/속성: `adult_body` / `width_length_relation`.
- 구성요소: thick transverse torso; thick limb volumes; segment length comparison.
- 보기·상태: 전신과 3/4 보기.
- 가까운 반례: 근육 윤곽만 선명하거나 큰 옷으로 넓어 보임.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S05](https://dictionaryblog.cambridge.org/2012/05/07/body-shapes/), [S07](https://www.merriam-webster.com/dictionary/stocky).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### slender_build — 몸통과 사지의 가로 볼륨이 가늘게 이어지는 체형

- 관찰 형태: consistently narrow torso and limb volumes with coherent joint transitions
- 소유자/속성: `adult_body` / `transverse_volume`.
- 구성요소: narrow torso volume; narrow limb volumes; continuous joint transitions.
- 보기·상태: 전신, 같은 축척.
- 가까운 반례: 긴 키 또는 검은 옷만으로 가늘어 보임.
- 기존 소유자: `slender_linear_build`.
- 자료: [S05](https://dictionaryblog.cambridge.org/2012/05/07/body-shapes/), [S45](https://www.merriam-webster.com/dictionary/lean).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### long_limb_build — 몸통에 비해 길고 가는 팔다리의 비율

- 관찰 형태: long slender limb segments relative to a readable torso
- 소유자/속성: `adult_limbs` / `segment_length_relation`.
- 구성요소: torso reference length; upper and lower limb lengths; slender transverse volumes.
- 보기·상태: 전신, 과장된 광각 제외.
- 가까운 반례: 몸 전체가 크기만 크거나 높은 신발로 다리만 늘어남.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S05](https://dictionaryblog.cambridge.org/2012/05/07/body-shapes/).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### wiry_definition — 가는 몸통·사지에 국소 근육과 힘줄 윤곽이 읽히는 체격

- 관찰 형태: narrow torso and limbs with restrained muscle planes and tendon contours
- 소유자/속성: `adult_body` / `narrow_defined_build`.
- 구성요소: narrow transverse volumes; localized muscle planes; localized tendon contours.
- 보기·상태: 전신과 해당 부위 확대.
- 가까운 반례: 털의 wiry 질감 또는 힘이 세다는 서술만 있음.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S05](https://dictionaryblog.cambridge.org/2012/05/07/body-shapes/), [S06](https://dictionary.cambridge.org/us/dictionary/english/wiry?topic=hair), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### soft_volume — 몸통과 사지에 연속된 부드러운 볼륨 분포

- 관찰 형태: continuous soft volume across torso and limbs
- 소유자/속성: `adult_body` / `soft_volume_distribution`.
- 구성요소: soft torso contour; soft limb contour; multi-region continuity.
- 보기·상태: 전신과 3/4 보기.
- 가까운 반례: 가슴만 크거나 배 한 부위만 둥글게 보임.
- 기존 소유자: `soft_full_figure_volume`.
- 자료: [S05](https://dictionaryblog.cambridge.org/2012/05/07/body-shapes/), [S44](https://www.merriam-webster.com/dictionary/voluptuous).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### curvilinear_relation — 상체·허리·골반의 들어가고 나오는 윤곽 관계

- 관찰 형태: coherent inward and outward contours across upper torso waist and hips
- 소유자/속성: `adult_body` / `contour_relation`.
- 구성요소: upper torso contour; inward waist transition; outward hip transition.
- 보기·상태: 전신 또는 몸통 전체.
- 가까운 반례: 큰 가슴 하나나 특정 체중만으로 곡선 관계를 대신함.
- 기존 소유자: `curvilinear_figure_relation`.
- 자료: [S05](https://dictionaryblog.cambridge.org/2012/05/07/body-shapes/), [S44](https://www.merriam-webster.com/dictionary/voluptuous).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### muscle_volume — 부위가 명시된 근육의 두꺼운 부피

- 관찰 형태: substantial regional muscle volume with readable anatomical attachments
- 소유자/속성: `adult_muscles` / `regional_volume`.
- 구성요소: named muscle region; expanded muscle belly; continuous joint attachments.
- 보기·상태: 해당 부위와 연결 관절.
- 가까운 반례: 조명으로 홈만 진해지고 근육 부피는 같음.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S09](https://npcnewsonline.com/official-npc-figure-division-rules/), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### muscle_definition — 근육 부피와 별개로 읽히는 평면·경계의 선명도

- 관찰 형태: readable muscle planes and separations with volume declared separately
- 소유자/속성: `adult_muscles` / `surface_definition`.
- 구성요소: muscle surface planes; separation boundaries; volume declared separately.
- 보기·상태: 같은 자세·조명 비교.
- 가까운 반례: 체중·체지방률·운동 능력을 대신 주장.
- 기존 소유자: `toned_muscular_build`.
- 자료: [S09](https://npcnewsonline.com/official-npc-figure-division-rules/), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### shoulder_width — 흉곽과 비교해 읽히는 양쪽 어깨 폭

- 관찰 형태: bilateral shoulder width compared with the ribcage
- 소유자/속성: `adult_shoulders` / `transverse_width`.
- 구성요소: left and right shoulder endpoints; ribcage reference; comparable camera plane.
- 보기·상태: 상체 정면과 3/4.
- 가까운 반례: 어깨 패드나 팔을 벌린 자세가 폭을 대신함.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### shoulder_slope — 목 뿌리에서 어깨 끝으로 이어지는 경사

- 관찰 형태: shoulder slope from the neck base to each shoulder endpoint
- 소유자/속성: `adult_shoulders` / `slope`.
- 구성요소: neck base anchor; shoulder endpoint; height transition.
- 보기·상태: 상체 정면, 몸통 기울기 기록.
- 가까운 반례: 넓은 어깨를 수평 어깨와 동의어 처리.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### ribcage_width — 가슴 돌출과 구분되는 흉곽의 가로 폭

- 관찰 형태: ribcage transverse width separated from breast projection
- 소유자/속성: `adult_ribcage` / `transverse_width`.
- 구성요소: lateral ribcage boundaries; torso centerline; breast contour separated.
- 보기·상태: 정면과 3/4 상체.
- 가까운 반례: 큰 가슴·넓은 어깨·등 근육을 흉곽 폭으로 합침.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S13](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax), [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### ribcage_depth — 흉곽의 앞뒤 깊이

- 관찰 형태: front-to-back ribcage depth with breast and back contours separated
- 소유자/속성: `adult_ribcage` / `front_back_depth`.
- 구성요소: anterior chest wall; posterior thoracic reference; front-back extent.
- 보기·상태: 측면 몸통, 자세 기록.
- 가까운 반례: 허리 과신전이나 가슴 돌출만으로 깊이를 주장.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S02](https://www.iso.org/standard/65246.html), [S13](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax), [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### torso_limb_ratio — 몸통 길이와 다리 길이의 상대 관계

- 관찰 형태: torso-to-leg length relation with anatomical endpoints specified
- 소유자/속성: `adult_body` / `torso_limb_length_relation`.
- 구성요소: torso endpoints; leg endpoints; same-scale comparison.
- 보기·상태: 전신, 신발·원근 기록.
- 가까운 반례: 하이웨이스트 바지를 해부학적 긴 다리와 동일시.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S03](https://wwwn.cdc.gov/nchs/data/nhanes/public/2021/manuals/2021-Anthropometry-Procedures-Manual-508.pdf).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### waist_level — 의복 허리선과 별도로 기술한 몸통 허리 위치

- 관찰 형태: anatomical waist level separated from a garment waistband
- 소유자/속성: `adult_torso` / `anatomical_waist_level`.
- 구성요소: torso waist landmark; ribcage pelvic references; garment boundary separated.
- 보기·상태: 몸통과 골반 포함.
- 가까운 반례: 높은 바지 허리선을 몸의 high waist로 자동 번역.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S03](https://wwwn.cdc.gov/nchs/data/nhanes/public/2021/manuals/2021-Anthropometry-Procedures-Manual-508.pdf).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### bust_prominence — 흉곽에 비해 두드러지는 양쪽 가슴 볼륨

- 관찰 형태: bilateral breast prominence relative to ribcage and natural waist
- 소유자/속성: `adult_breasts` / `ribcage_relative_prominence`.
- 구성요소: bilateral breast volume; ribcage comparison; natural waist reference.
- 보기·상태: 앞·3/4·측면 중 필요한 보기.
- 가까운 반례: 전신 곡선·hourglass·컵 문자만으로 대체.
- 기존 소유자: `bust_prominence_relation`.
- 자료: [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S15](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0172122), [S16](https://www.bravissimo.com/sister-sizes/).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### breast_root_width — 각 가슴이 흉곽에 붙는 내측부터 외측까지의 범위

- 관찰 형태: medial-to-lateral breast attachment width on the chest wall
- 소유자/속성: `adult_breast` / `attachment_width`.
- 구성요소: medial attachment extent; lateral attachment extent; chest wall ownership.
- 보기·상태: 정면과 3/4, 가림 여부 기록.
- 가까운 반례: 양쪽 사이 간격 또는 외측 한쪽 확장만으로 폭을 확정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S15](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0172122), [S47](https://billysbras.com/blogs/billys-bra-blog/understanding-root-width-and-breast-shape).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### breast_projection — 가슴 기저 흉벽에서 앞쪽으로 나온 깊이

- 관찰 형태: anterior breast projection from the local chest-wall base
- 소유자/속성: `adult_breast` / `anterior_projection`.
- 구성요소: local chest wall plane; anterior breast contour; projection extent.
- 보기·상태: 측면 또는 비교 가능한 3/4.
- 가까운 반례: 넓은 기저 폭·컵 문자·상체 앞으로 숙임으로 대신함.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S15](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0172122).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### waist_width_depth — 허리의 가로 폭과 앞뒤 두께를 구분

- 관찰 형태: waist transverse width and front-back depth described separately
- 소유자/속성: `adult_waist` / `transverse_width_depth`.
- 구성요소: bilateral waist boundaries; front-back contour; rib and pelvis references.
- 보기·상태: 정면과 측면.
- 가까운 반례: 둘레·WHR·코르셋 압박을 실측 없는 단일 사진으로 확정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S03](https://wwwn.cdc.gov/nchs/data/nhanes/public/2021/manuals/2021-Anthropometry-Procedures-Manual-508.pdf).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### hip_width — 허리·상체와 비교해 읽는 골반 부위 가로 폭

- 관찰 형태: bilateral hip-region width relative to waist and upper torso
- 소유자/속성: `adult_hips` / `transverse_width`.
- 구성요소: left and right hip boundaries; waist reference; upper torso reference.
- 보기·상태: 정면과 3/4.
- 가까운 반례: 엉덩이의 뒤쪽 돌출이나 플레어 스커트만으로 폭을 판단.
- 기존 소유자: `triangle_lower_body_dominant_relation`.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### gluteal_projection — 골반과 허벅지 연결에 대한 엉덩이 뒤쪽 돌출

- 관찰 형태: posterior gluteal projection relative to pelvis and thigh attachment
- 소유자/속성: `adult_gluteal_region` / `posterior_projection`.
- 구성요소: pelvic side reference; posterior gluteal contour; upper thigh attachment.
- 보기·상태: 측면·3/4, 골반 기울기 기록.
- 가까운 반례: 넓은 골반·허리 과신전·패딩으로 돌출을 대신함.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs), [S42](https://www.merriam-webster.com/dictionary/statuesque), [S43](https://www.merriam-webster.com/dictionary/callipygian).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### hip_dip_local — 골반 바깥쪽에서 허벅지 위쪽으로 이어지는 국소 들어감

- 관찰 형태: localized lateral hip indentation above the outer upper thigh
- 소유자/속성: `adult_lateral_hip` / `local_contour_indentation`.
- 구성요소: lateral pelvic contour; local indentation; outer upper thigh continuation.
- 보기·상태: 정면 또는 3/4, 체중 이동 기록.
- 가까운 반례: 허리 움푹함·옷 주름·디지털 body dip 효과를 대신함.
- 기존 소유자: `lateral_waist_hip_contour_transition`.
- 자료: [S18](https://health.clevelandclinic.org/hip-dips).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### thigh_gap — 가까운 양발 자세에서 허벅지 안쪽 경계 사이의 실제 배경 틈

- 관찰 형태: background gap bounded by inner thighs in a close-foot stance
- 소유자/속성: `adult_inner_thighs` / `stance_bounded_negative_space`.
- 구성요소: close-foot stance; inner-thigh boundaries; background continuity.
- 보기·상태: 전신 또는 하체와 양발 포함.
- 가까운 반례: 넓게 선 자세·치맛자락 틈·칠한 어두운 선으로 대체.
- 기존 소유자: `inner_thigh_negative_space`.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

## P2

### vascular_surface — 위치가 명확한 피부 아래 표재 혈관의 가시성

- 관찰 형태: visible superficial vessel paths on a specified skin region
- 소유자/속성: `adult_skin_region` / `superficial_vessel_visibility`.
- 구성요소: skin surface ownership; branching vessel paths; localized continuity.
- 보기·상태: 해당 부위 확대, 색과 부조 구분.
- 가까운 반례: 문신 선이나 근육 골을 혈관으로 읽음.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: additional focused sources required.

### muscle_striation — 명시된 근육 부위의 미세한 반복 줄무늬 윤곽

- 관찰 형태: fine repeated striation across a specified muscle region
- 소유자/속성: `adult_muscle_region` / `fine_surface_striation`.
- 구성요소: named muscle surface; repeated fine lines; consistent fiber direction.
- 보기·상태: 부위 확대, 일관된 조명.
- 가까운 반례: 셀룰라이트나 옷의 리브 조직으로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S09](https://npcnewsonline.com/official-npc-figure-division-rules/), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### back_width_depth — 등의 가로 확장과 뒤쪽 부피를 별도로 기술

- 관찰 형태: back width and posterior muscle depth described as separate axes
- 소유자/속성: `adult_back` / `regional_width_depth`.
- 구성요소: bilateral back width; posterior muscle depth; waist reference.
- 보기·상태: 후면과 측면 비교.
- 가까운 반례: V 테이퍼 하나로 등 깊이까지 추정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S09](https://npcnewsonline.com/official-npc-figure-division-rules/), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### neck_proportion — 목의 보이는 길이와 두께의 관계

- 관찰 형태: visible neck length and transverse thickness between head and torso
- 소유자/속성: `adult_neck` / `length_width_relation`.
- 구성요소: jaw-to-shoulder span; neck transverse thickness; head and torso anchors.
- 보기·상태: 머리·어깨 포함, 고개 각도 기록.
- 가까운 반례: 옷깃 높이 또는 턱 들기만으로 긴 목을 판단.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### clavicle_landmark — 쇄골의 선과 위쪽 오목한 면의 연결

- 관찰 형태: clavicular ridge with a distinct supraclavicular hollow
- 소유자/속성: `adult_upper_torso` / `clavicle_hollow_relief`.
- 구성요소: clavicular ridge; supraclavicular depression; neck shoulder chest continuity.
- 보기·상태: 상흉부와 목 포함.
- 가까운 반례: 쇄골 음영을 체중·건강의 증거로 읽음.
- 기존 소유자: `clavicle_supraclavicular_hollow`.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### scapular_relief — 팔 자세와 연결해 읽는 견갑골 주변 표면 윤곽

- 관찰 형태: scapular surface relief connected to the current arm and shoulder position
- 소유자/속성: `adult_upper_back` / `scapular_surface_relief`.
- 구성요소: scapular region; overlying surface relief; arm position relation.
- 보기·상태: 후면 상체와 팔 연결.
- 가까운 반례: 옷 솔기 또는 의학적 winging 진단으로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### head_body_ratio — 측정 기준을 명시한 머리 대 전신 길이 관계

- 관찰 형태: head-to-body length relation using an explicit anatomical convention
- 소유자/속성: `adult_body` / `head_body_length_relation`.
- 구성요소: head reference endpoints; body reference endpoints; same-scale extent.
- 보기·상태: 전신과 머리 기준점.
- 가까운 반례: 예술의 이상화 등신을 인체 보편 기준으로 제시.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S32](https://www.proko.com/course-lesson/human-proportions-idealistic-figures/).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### breast_root_height — 상흉부부터 아래 경계까지의 세로 부착 범위

- 관찰 형태: vertical breast attachment extent on the chest wall
- 소유자/속성: `adult_breast` / `attachment_height`.
- 구성요소: superior attachment extent; inferior attachment region; chest wall reference.
- 보기·상태: 부착 경계가 확인되는 교육적 보기.
- 가까운 반례: 가슴이 높이 놓임·상부 볼륨·상체 길이를 같은 뜻으로 처리.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S47](https://billysbras.com/blogs/billys-bra-blog/understanding-root-width-and-breast-shape).
- 세부 근거 상태: additional focused sources required.

### breast_fullness — 위·아래와 내·외측의 볼륨 분포

- 관찰 형태: upper-lower and medial-lateral breast fullness distribution
- 소유자/속성: `adult_breast` / `regional_fullness_distribution`.
- 구성요소: named regional partition; regional contour fullness; shared breast ownership.
- 보기·상태: 각도·지지 상태 기록.
- 가까운 반례: 큰 가슴을 모두 upper-full 또는 같은 모양으로 처리.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S15](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0172122), [S47](https://billysbras.com/blogs/billys-bra-blog/understanding-root-width-and-breast-shape).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### breast_spacing — 정중선 양쪽의 가슴 사이 간격과 방향

- 관찰 형태: bilateral breast spacing and orientation about the torso midline
- 소유자/속성: `adult_breasts` / `bilateral_spacing`.
- 구성요소: left medial contour; right medial contour; torso centerline.
- 보기·상태: 정면, 팔·브라 압박 기록.
- 가까운 반례: push-up으로 만든 cleavage를 자연 간격으로 확정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S15](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0172122), [S26](https://www.merriam-webster.com/dictionary/cleavage), [S47](https://billysbras.com/blogs/billys-bra-blog/understanding-root-width-and-breast-shape).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### breast_vertical_position — 가슴 아래 주름과 돌출점의 세로 위치 관계

- 관찰 형태: vertical relation of the breast contour and nipple to the inframammary fold
- 소유자/속성: `adult_breast` / `landmark_vertical_relation`.
- 구성요소: inframammary fold reference; breast contour; relative nipple position.
- 보기·상태: 측면·3/4, 지지 상태 명시.
- 가까운 반례: 형태에서 나이·출산·수술 이력을 추정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S15](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0172122), [S47](https://billysbras.com/blogs/billys-bra-blog/understanding-root-width-and-breast-shape).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### breast_asymmetry — 동일 보기에서 좌우 볼륨·위치·부착 차이

- 관찰 형태: bilateral differences in breast volume position or attachment in the same view
- 소유자/속성: `adult_breasts` / `bilateral_asymmetry`.
- 구성요소: left breast reference; right breast reference; same-state comparison.
- 보기·상태: 정면과 필요시 3/4.
- 가까운 반례: 몸통 회전·한쪽 가림·다른 조명을 실제 비대칭으로 판단.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S15](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0172122), [S47](https://billysbras.com/blogs/billys-bra-blog/understanding-root-width-and-breast-shape).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### abdominal_projection — 상복부와 하복부의 국소 돌출 관계

- 관찰 형태: upper and lower abdominal projection relative to the torso
- 소유자/속성: `adult_abdomen` / `regional_projection`.
- 구성요소: upper abdomen region; lower abdomen region; side contour continuity.
- 보기·상태: 측면과 3/4, 호흡·자세 기록.
- 가까운 반례: 배가 나온 외관에서 임신·건강·체지방률을 추정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S13](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### seated_skin_folds — 앉거나 구부린 자세에서 생기는 복부 접힘

- 관찰 형태: abdominal skin folds at a seated or flexed torso position
- 소유자/속성: `adult_abdominal_skin` / `pose_dependent_folding`.
- 구성요소: flexed torso state; localized skin folds; continuous skin surface.
- 보기·상태: 자세와 접힘 부위를 함께 보임.
- 가까운 반례: 정지 체형·흉터·의복 주름으로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S13](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### abdominal_segmentation — 복직근 구획과 중앙 연결선의 표면 윤곽

- 관찰 형태: rectus-abdominis surface segments about a central abdominal line
- 소유자/속성: `adult_abdominal_wall` / `muscle_surface_segmentation`.
- 구성요소: left and right segments; central line; tendinous intersection pattern.
- 보기·상태: 복부와 몸통 연결, 조명 기록.
- 가까운 반례: 셔츠 프린트·그린 선·허리 V 윤곽을 six-pack으로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S13](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### abdominal_v_boundary — 하복부에서 사타구니 쪽으로 모이는 V 모양 윤곽

- 관찰 형태: paired lower-abdominal contours converging toward the groin region
- 소유자/속성: `adult_lower_abdomen` / `inguinal_contour_relation`.
- 구성요소: left oblique contour; right oblique contour; lower abdominal ownership.
- 보기·상태: 하복부 범위가 명확한 보기.
- 가까운 반례: V형 턱선·상의 V넥·등 V taper를 같은 뜻으로 처리.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [S13](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-4-axial-muscles-of-the-abdominal-wall-and-thorax).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### navel_shape — 배꼽의 함몰·돌출과 주변 피부 연결

- 관찰 형태: navel depression or protrusion connected to surrounding abdominal skin
- 소유자/속성: `adult_navel` / `surface_shape`.
- 구성요소: navel boundary; local depth or projection; abdominal skin continuity.
- 보기·상태: 배꼽 확대와 복부 위치.
- 가까운 반례: 단추·피어싱만 읽거나 수술·질환을 추정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: additional focused sources required.

### gluteal_fullness — 엉덩이 상부와 하부의 볼륨 분포

- 관찰 형태: upper and lower gluteal fullness along a continuous posterior contour
- 소유자/속성: `adult_gluteal_region` / `regional_fullness`.
- 구성요소: upper gluteal region; lower gluteal region; continuous posterior outline.
- 보기·상태: 후면과 측면.
- 가까운 반례: 애플힙·복숭아힙의 칭찬만으로 고정 모양을 생성.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs), [S43](https://www.merriam-webster.com/dictionary/callipygian).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### gluteal_fold — 엉덩이와 뒤쪽 허벅지 사이의 접힘 경계

- 관찰 형태: gluteal fold at the transition to the posterior upper thigh
- 소유자/속성: `adult_gluteal_thigh_boundary` / `fold_relation`.
- 구성요소: gluteal lower contour; posterior upper thigh; localized fold boundary.
- 보기·상태: 해당 부위 연결이 읽히는 보기.
- 가까운 반례: 바지 밑단·허리선·엉덩이 중앙 골과 혼동.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### back_dimples — 아래 등과 골반 연결 부근의 짝을 이룬 오목함

- 관찰 형태: paired local lumbosacral depressions above the pelvic transition
- 소유자/속성: `adult_lumbosacral_surface` / `paired_local_depressions`.
- 구성요소: lower back ownership; paired localized depressions; pelvic reference.
- 보기·상태: 아래 등 전체와 골반 연결.
- 가까운 반례: 노출된 골반 모양에서 체지방·미적 우수성을 추정.
- 기존 소유자: `posterior_lumbosacral_landmarks`.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### thigh_volume — 허벅지의 가로 볼륨과 무릎 쪽 변화

- 관찰 형태: thigh transverse volume with a coherent transition toward the knee
- 소유자/속성: `adult_thighs` / `transverse_volume`.
- 구성요소: upper thigh volume; mid-thigh contour; knee transition.
- 보기·상태: 상·하단 관절 포함.
- 가까운 반례: 꿀벅지라는 가치 표현을 근육·지방 구성비로 변환.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### calf_contour — 종아리의 국소 볼륨과 발목으로의 좁아짐

- 관찰 형태: localized calf fullness tapering toward a connected ankle
- 소유자/속성: `adult_lower_leg` / `calf_taper_relation`.
- 구성요소: calf belly contour; lower-leg taper; ankle attachment.
- 보기·상태: 하퇴 전체, 발목 포함.
- 가까운 반례: 포인팅 발·하이힐·압박 스타킹만으로 원래 윤곽 확정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### limb_alignment — 현재 자세에서 읽히는 골반·무릎·발목 정렬

- 관찰 형태: projected hip knee and ankle alignment in a specified stance
- 소유자/속성: `adult_lower_limbs` / `projected_axis_relation`.
- 구성요소: hip reference; knee reference; ankle reference.
- 보기·상태: 전신 정면, 발 간격·회전 기록.
- 가까운 반례: X/O 인상으로 골격 질환이나 보행 능력을 진단.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### finger_proportion — 손바닥과 비교되는 손가락 길이·굵기

- 관찰 형태: finger length and thickness relative to the connected palm
- 소유자/속성: `adult_hand` / `finger_palm_length_relation`.
- 구성요소: palm reference; finger segment lengths; finger transverse thickness.
- 보기·상태: 손 전체, 원근·굽힘 기록.
- 가까운 반례: 손가락 포즈나 렌즈만으로 길이를 과장.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### knuckle_relief — 손가락 관절 위치와 연결된 마디 윤곽

- 관찰 형태: knuckle surface relief at anatomically connected finger joints
- 소유자/속성: `adult_hand` / `joint_surface_relief`.
- 구성요소: finger joint location; localized joint relief; continuous finger segments.
- 보기·상태: 손과 손가락 연결 확대.
- 가까운 반례: 주름·반지·힘줄을 관절 위치와 혼동.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### foot_arch_instep — 발바닥 아치와 발등 높이의 별도 관계

- 관찰 형태: plantar arch and dorsal instep height as distinct foot features
- 소유자/속성: `adult_foot` / `arch_instep_relation`.
- 구성요소: plantar boundary; dorsal instep contour; load state.
- 보기·상태: 측면과 발바닥 보기, 하중 상태 기록.
- 가까운 반례: 하이힐·발끝 세움 또는 신발만으로 원래 아치 확정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S01](https://sizekorea.kr/support/how-to-use), [S02](https://www.iso.org/standard/65246.html), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: additional focused sources required.

### eye_aperture — 눈꺼풀 사이 개구의 가로·세로 비율

- 관찰 형태: horizontal and vertical eye-opening extent between eyelid margins
- 소유자/속성: `adult_eye_region` / `aperture_aspect_relation`.
- 구성요소: upper eyelid margin; lower eyelid margin; inner outer corners.
- 보기·상태: 정면 얼굴과 확대, 표정 기록.
- 가까운 반례: 눈썹 높이·아이메이크업·눈 크게 뜸을 고정 눈 크기로 처리.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S23](https://www.adobe.com/learn/photoshop/web/face-aware-liquify).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### eyelid_fold — 눈꺼풀 접힘과 눈 개구 경계의 관계

- 관찰 형태: visible eyelid fold in relation to the eye-opening margin
- 소유자/속성: `adult_eyelids` / `visible_fold_relation`.
- 구성요소: eyelid skin ownership; fold line; eye-opening margin.
- 보기·상태: 얼굴 확대, 눈의 열림 상태 기록.
- 가까운 반례: 아이라인·속눈썹·그림자를 쌍꺼풀로 판정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S23](https://www.adobe.com/learn/photoshop/web/face-aware-liquify), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: additional focused sources required.

### eye_spacing — 양쪽 눈 내측 모서리와 얼굴 중심의 간격

- 관찰 형태: bilateral eye spacing relative to the facial midline
- 소유자/속성: `adult_eyes` / `bilateral_spacing`.
- 구성요소: left inner corner; right inner corner; facial midline.
- 보기·상태: 정면, 렌즈·얼굴 회전 기록.
- 가까운 반례: 안경 프레임·머리카락·원근으로 간격이 달라 보임.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S23](https://www.adobe.com/learn/photoshop/web/face-aware-liquify).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### nose_projection — 콧대·코끝·콧방울의 개별 돌출과 폭

- 관찰 형태: nasal bridge tip projection and alar width as distinct features
- 소유자/속성: `adult_nose` / `regional_projection`.
- 구성요소: bridge contour; tip projection; alar width.
- 보기·상태: 정면과 측면.
- 가까운 반례: 코 쉐딩·표정·회전을 실제 뼈나 연골 치수로 확정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S02](https://www.iso.org/standard/65246.html), [S23](https://www.adobe.com/learn/photoshop/web/face-aware-liquify).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### lip_volume — 입술 붉은 면의 위·아래 두께와 외곽

- 관찰 형태: upper and lower vermilion thickness and lip perimeter
- 소유자/속성: `adult_lips` / `vermilion_contour_relation`.
- 구성요소: upper vermilion; lower vermilion; mouth opening boundary.
- 보기·상태: 정면 확대, 표정·메이크업 기록.
- 가까운 반례: 립 오버라인·광택을 고정 입술 부피로 읽음.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S23](https://www.adobe.com/learn/photoshop/web/face-aware-liquify).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### philtral_contour — 인중 능선·골과 윗입술 중앙 윤곽의 연결

- 관찰 형태: philtral ridges and groove connected to the central upper-lip contour
- 소유자/속성: `adult_upper_lip` / `philtral_cupid_relation`.
- 구성요소: paired philtral ridges; central groove; Cupid bow connection.
- 보기·상태: 코 아래부터 윗입술 포함.
- 가까운 반례: 입술 색·입 벌림·인중 길이 하나로 전체 형태 대체.
- 기존 소유자: `upper_lip_philtral_contour`.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [S23](https://www.adobe.com/learn/photoshop/web/face-aware-liquify).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### ear_attachment — 귓불과 얼굴 옆면의 부착 경계

- 관찰 형태: earlobe attachment boundary to the lateral facial surface
- 소유자/속성: `adult_ear` / `lobe_attachment_relation`.
- 구성요소: earlobe contour; facial-side attachment; continuous ear ownership.
- 보기·상태: 귀 전체와 옆얼굴.
- 가까운 반례: 귀걸이·헤어 가림만으로 attached/detached를 판정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology).
- 세부 근거 상태: additional focused sources required.

### facial_asymmetry — 같은 표정·보기에서의 국소 좌우 차이

- 관찰 형태: localized bilateral facial differences under the same expression and view
- 소유자/속성: `adult_face` / `bilateral_asymmetry`.
- 구성요소: left feature reference; right feature reference; same-view comparison.
- 보기·상태: 정면 얼굴, 표정과 조명 기록.
- 가까운 반례: 회전·한쪽 미소·한쪽 그림자를 고정 비대칭으로 읽음.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S23](https://www.adobe.com/learn/photoshop/web/face-aware-liquify).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### pose_surface_change — 하중·구부림·접촉으로 달라지는 국소 표면 형태

- 관찰 형태: localized surface change tied to current load flexion or contact
- 소유자/속성: `adult_body_region` / `pose_dependent_surface_change`.
- 구성요소: specified pose state; localized surface response; continuous regional anatomy.
- 보기·상태: 원인 자세와 부위를 함께 보임.
- 가까운 반례: 표면 변화에서 고정 체형·병력·감정을 추정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [S11](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-5-muscles-of-the-pectoral-girdle-and-upper-limbs), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

## P3

### compression_contour — 벨트·밴드 접촉에 의해 변형된 국소 몸 윤곽

- 관찰 형태: localized contour deformation at a garment band contact
- 소유자/속성: `garment_body_contact` / `local_compression`.
- 구성요소: identifiable band edge; contact region; adjacent contour displacement.
- 보기·상태: 접촉 부위와 의복 주인 포함.
- 가까운 반례: 선천적 허리 모양·피부 질환·의복 자체 주름으로 판단.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S03](https://wwwn.cdc.gov/nchs/data/nhanes/public/2021/manuals/2021-Anthropometry-Procedures-Manual-508.pdf), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### nail_shape — 손발톱판의 길이와 외곽을 장식과 구분

- 관찰 형태: nail plate length and perimeter separated from polish and extensions
- 소유자/속성: `adult_nail` / `plate_length_contour`.
- 구성요소: nail bed ownership; plate perimeter; free-edge length.
- 보기·상태: 손가락 또는 발가락 확대.
- 가까운 반례: 네일 연장·광택·색을 자연 손톱 모양으로 판단.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: additional focused sources required.

### skin_tone_appearance — 조명과 화이트밸런스가 기록된 피부의 보이는 색

- 관찰 형태: apparent skin color with illumination and white balance recorded
- 소유자/속성: `adult_skin` / `apparent_color`.
- 구성요소: specified skin region; local color appearance; capture-light reference.
- 보기·상태: 같은 조명·노출, 여러 부위 가능.
- 가까운 반례: 피부색에서 민족·국적·인종을 추정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### skin_pigment_pattern — 피부 바탕 위의 점·반점 색 분포

- 관찰 형태: localized pigment dots or patches on a continuous skin surface
- 소유자/속성: `adult_skin_region` / `pigment_distribution`.
- 구성요소: skin base color; pigment boundaries; spatial distribution.
- 보기·상태: 부위 확대, 실제 반점 경계.
- 가까운 반례: 그림자·메이크업·프린트를 점이나 진단명으로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### skin_relief_texture — 모공과 미세 요철을 광택과 별도로 기술

- 관찰 형태: skin pores and fine relief separated from specular finish
- 소유자/속성: `adult_skin_region` / `microrelief`.
- 구성요소: pore distribution; fine surface relief; specular layer separated.
- 보기·상태: 원본 크기 확대, 초점 확인.
- 가까운 반례: 노이즈·샤픈·플라스틱 매끈함을 실제 요철로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### striae_surface — 몸 표면의 길쭉한 띠 모양 선과 국소 질감

- 관찰 형태: elongated skin striae with localized color and texture variation
- 소유자/속성: `adult_skin_region` / `linear_striae_pattern`.
- 구성요소: elongated stripe paths; localized color; continuous skin ownership.
- 보기·상태: 선의 방향과 범위 확대.
- 가까운 반례: 셀룰라이트·주름·상처와 동일시하거나 발생 이력 단정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S20](https://www.aad.org/public/cosmetic/scars-stretch-marks/stretch-marks-why-appear), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### cellulite_relief — 연속 피부에 분포한 국소 패임과 울퉁불퉁한 부조

- 관찰 형태: localized dimpling and uneven relief on continuous skin
- 소유자/속성: `adult_skin_region` / `dimpled_relief`.
- 구성요소: continuous skin surface; distributed shallow dimples; local relief variation.
- 보기·상태: 부위 확대, 자세·조명 기록.
- 가까운 반례: 선형 튼살·노이즈·의복 퀼팅으로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S21](https://dermnetnz.org/topics/cellulite), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### scar_surface — 피부에 연결된 국소 선·면의 색과 높낮이 차이

- 관찰 형태: localized scar-like line or patch with color and relief differences
- 소유자/속성: `adult_skin_region` / `scar_like_relief`.
- 구성요소: bounded line or patch; local color difference; raised or depressed relief.
- 보기·상태: 해당 부위 확대.
- 가까운 반례: 피부 형태만으로 수술·외상 원인이나 기간을 확정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S19](https://dermnetnz.org/topics/terminology), [S20](https://www.aad.org/public/cosmetic/scars-stretch-marks/stretch-marks-why-appear).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### skin_fold_wrinkle — 피부 접힘·주름의 방향과 자세에 따른 변화

- 관찰 형태: skin folds and wrinkles with orientation and pose state specified
- 소유자/속성: `adult_skin_region` / `fold_wrinkle_relation`.
- 구성요소: continuous skin ownership; fold line direction; pose-state relation.
- 보기·상태: 원본 확대, 관절 상태 포함.
- 가까운 반례: 나이·수분·생활 습관을 단정하거나 옷 주름과 혼동.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### body_hair_fiber — 신체 털의 굵기·색과 피부에 붙는 관계

- 관찰 형태: body-hair fiber thickness and pigmentation on its skin region
- 소유자/속성: `adult_body_hair` / `fiber_thickness_color`.
- 구성요소: skin attachment; fiber thickness; fiber pigmentation.
- 보기·상태: 부위 확대, 조명 기록.
- 가까운 반례: 털의 굵기만으로 나이·성별·호르몬을 판단.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S22](https://dermnetnz.org/topics/skin-changes-at-puberty), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### body_hair_distribution — 부위별 털 밀도·길이·분포

- 관찰 형태: regional body-hair density length and distribution
- 소유자/속성: `adult_body_hair` / `density_length_distribution`.
- 구성요소: specified body region; fiber density; fiber length distribution.
- 보기·상태: 부위와 주변 피부 함께 보임.
- 가까운 반례: 수염·두발·다리 털을 하나의 hairy 기본값으로 확장.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S22](https://dermnetnz.org/topics/skin-changes-at-puberty), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### hair_grooming_state — 잔털·짧은 수염자국·긴 털의 보이는 상태

- 관찰 형태: visible fine hairs short stubble or longer fibers on a specified region
- 소유자/속성: `adult_body_hair` / `visible_grooming_state`.
- 구성요소: specified region; visible fiber state; skin continuity.
- 보기·상태: 부위 확대, 관찰 가능한 섬유.
- 가까운 반례: 매끈한 피부만으로 제모 방법·위생·최근 면도 이력 단정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S22](https://dermnetnz.org/topics/skin-changes-at-puberty), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### neckline_exposure — 옷 목선이 경계 짓는 목·상흉부 피부 범위

- 관찰 형태: neck and upper-chest skin bounded by the same garment neckline
- 소유자/속성: `adult_garment_torso_boundary` / `upper_chest_exposure`.
- 구성요소: same garment neckline; neck and upper chest; bounded exposed region.
- 보기·상태: 상체와 의복 연결.
- 가까운 반례: 큰 가슴·전신 곡선·cleavage가 필수라고 추가.
- 기존 소유자: `decolletage_neckline_exposure`.
- 자료: [S26](https://www.merriam-webster.com/dictionary/cleavage).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### lateral_chest_boundary — 같은 상의 옆 경계 밖의 제한된 가슴 외측 윤곽

- 관찰 형태: bounded lateral breast contour beside the same opaque bodice edge
- 소유자/속성: `adult_garment_breast_boundary` / `lateral_exposure`.
- 구성요소: lateral breast ownership; opaque central bodice; continuous side edge.
- 보기·상태: 상체 옆 경계와 팔 구분.
- 가까운 반례: 등·겨드랑이·팔만 보이거나 상의 전체를 투명하게 바꿈.
- 기존 소유자: `pfe_lateral_chest`.
- 자료: [S27](https://www.merriam-webster.com/dictionary/sideboob), [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### lower_chest_boundary — 같은 상의 밑단 아래의 제한된 가슴 하부 윤곽

- 관찰 형태: bounded lower breast contour below the same opaque top hem
- 소유자/속성: `adult_garment_breast_boundary` / `lower_exposure`.
- 구성요소: lower breast ownership; identifiable textile hem; abdomen separated.
- 보기·상태: 상의 밑단과 하흉부·복부 포함.
- 가까운 반례: 배 피부만 보이거나 중앙 가슴 가림을 제거.
- 기존 소유자: `pfe_lower_chest`.
- 자료: [S28](https://www.merriam-webster.com/dictionary/underboob), [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### cleavage_relation — 목선과 양쪽 안쪽 가슴 사이의 노출 관계

- 관찰 형태: intermammary contour visible within the garment neckline
- 소유자/속성: `adult_garment_breast_boundary` / `intermammary_exposure`.
- 구성요소: left inner breast contour; right inner breast contour; neckline boundary.
- 보기·상태: 상체와 목선, 지지 상태 기록.
- 가까운 반례: 개별 가슴 부피·컵 문자·자연 간격을 확정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S26](https://www.merriam-webster.com/dictionary/cleavage), [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S16](https://www.bravissimo.com/sister-sizes/).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### midriff_boundary — 상의 밑단과 하의 허리선 사이 복부 피부

- 관찰 형태: abdominal skin between the same top hem and lower-garment waistband
- 소유자/속성: `adult_garment_abdomen_boundary` / `midriff_exposure`.
- 구성요소: top hem; lower waistband; abdominal skin interval.
- 보기·상태: 몸통과 상·하의 연결.
- 가까운 반례: 하흉부 노출·속옷·고정 몸 허리선으로 혼동.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### fabric_body_outline — 불투명한 옷이 접촉해 드러내는 신체 윤곽

- 관찰 형태: body contour transmitted by contact with an opaque garment
- 소유자/속성: `opaque_garment_body_boundary` / `contact_outline`.
- 구성요소: opaque textile surface; body contact contour; fabric continuity.
- 보기·상태: 의복 영역 전체와 접촉 부위.
- 가까운 반례: 비침·맨살·몸 자체 치수와 동일시.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S29](https://www.merriam-webster.com/dictionary/camel%20toe).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### sheer_layering — 같은 천의 조직과 그 뒤 신체가 겹쳐 읽히는 비침

- 관찰 형태: readable garment fibers layered optically over the underlying body
- 소유자/속성: `sheer_garment_body_boundary` / `optical_layering`.
- 구성요소: garment fiber layer; underlying body layer; overlap transmission.
- 보기·상태: 섬유 조직과 신체 경계를 함께 확대.
- 가까운 반례: 맨살·살색 천·단순한 타이트핏으로 대체.
- 기존 소유자: `sheer_garment_optical_layering`.
- 자료: [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

## P4

### nipple_projection — 유륜면과 구분되는 유두의 표면 돌출 상태

- 관찰 형태: nipple surface projection relative to the surrounding areolar plane
- 소유자/속성: `adult_nipple` / `surface_projection`.
- 구성요소: nipple ownership; areolar plane; projection relation.
- 보기·상태: 명시적으로 요청된 중립 해부 문맥.
- 가까운 반례: 형태에서 흥분·임신·수유·병력을 단정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S17](https://my.clevelandclinic.org/health/body/nipple).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### areolar_surface — 유두 주변 유륜의 경계·색과 표면 질감

- 관찰 형태: areolar pigment boundary and surface texture around the nipple
- 소유자/속성: `adult_areola` / `pigment_boundary_texture`.
- 구성요소: nipple center; surrounding pigment boundary; localized surface texture.
- 보기·상태: 명시적으로 요청된 중립 해부 문맥.
- 가까운 반례: 문신·그림자·신체 이력으로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S14](https://my.clevelandclinic.org/health/articles/8330-breast-anatomy), [S17](https://my.clevelandclinic.org/health/body/nipple), [S19](https://dermnetnz.org/topics/terminology).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### gluteal_cleft — 좌우 엉덩이 사이의 정중선 표면 골

- 관찰 형태: midline surface cleft between the left and right gluteal regions
- 소유자/속성: `adult_gluteal_region` / `midline_cleft`.
- 구성요소: left gluteal surface; right gluteal surface; midline cleft continuity.
- 보기·상태: 명시된 해부 문맥, 가림 조건 유지.
- 가까운 반례: 속옷 주름·옆 노출·하부 접힘을 중앙 골로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### under_gluteal_boundary — 하의 밑단과 엉덩이 하부·허벅지의 노출 관계

- 관찰 형태: lower gluteal contour and upper thigh bounded by the garment hem
- 소유자/속성: `adult_garment_gluteal_boundary` / `lower_gluteal_exposure`.
- 구성요소: same lower garment hem; lower gluteal contour; upper thigh separated.
- 보기·상태: 명시된 의복 문맥의 후면 또는 3/4.
- 가까운 반례: 엉덩이 중앙 골·다리 피부만으로 underbutt라 함.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [S12](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-6-appendicular-muscles-of-the-pelvic-girdle-and-lower-limbs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### garment_bulge — 불투명 의복의 위치가 명시된 국소 돌출

- 관찰 형태: localized projection of opaque garment fabric at a specified body contact
- 소유자/속성: `opaque_garment_contact` / `localized_fabric_projection`.
- 구성요소: opaque garment ownership; localized surface projection; contact location.
- 보기·상태: 명시된 성인 의복 문맥.
- 가까운 반례: 실제 생식기 치수·흥분 상태·성별·허벅지 윤곽을 자동 확정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S29](https://www.merriam-webster.com/dictionary/camel%20toe), [S31](https://my.clevelandclinic.org/health/body/penis).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### garment_central_crease — 타이트한 하의의 중앙 골과 양쪽 윤곽 관계

- 관찰 형태: localized central garment crease with adjacent paired contours
- 소유자/속성: `opaque_garment_contact` / `localized_central_crease`.
- 구성요소: continuous opaque textile; central crease; paired adjacent contours.
- 보기·상태: 명시된 성인 의복 문맥.
- 가까운 반례: 일반 솔기·배 주름·노출된 해부 형태로 대체.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S29](https://www.merriam-webster.com/dictionary/camel%20toe), [S30](https://my.clevelandclinic.org/health/body/vulva).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### vulvar_topology — 명시된 중립 해부 문맥의 외음부 외부 구성 연결

- 관찰 형태: external vulvar surface structures in an explicitly requested neutral anatomical context
- 소유자/속성: `adult_vulvar_surface` / `external_anatomical_topology`.
- 구성요소: mons pubis and outer labial surfaces; inner labial folds and clitoral hood relation; external opening region and perineal boundary.
- 보기·상태: 중립 해부 설명·도식, 원래 가림 조건 유지.
- 가까운 반례: 외음부를 내부 질인 vagina와 동일시하거나 성적 행위를 추가.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S30](https://my.clevelandclinic.org/health/body/vulva).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### penile_topology — 명시된 중립 해부 문맥의 음경 외부 구성 연결

- 관찰 형태: penile shaft glans and optional foreskin as connected external structures
- 소유자/속성: `adult_penile_surface` / `external_anatomical_topology`.
- 구성요소: shaft continuity; glans relation; visible foreskin state.
- 보기·상태: 중립 해부 설명·도식, 원래 가림 조건 유지.
- 가까운 반례: 표면에서 개인 이력·치수·흥분이나 행위를 추정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S31](https://my.clevelandclinic.org/health/body/penis).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### scrotal_testis_boundary — 외부 음낭 표면과 내부 고환의 구분

- 관찰 형태: external scrotal surface separated from the internal testes
- 소유자/속성: `adult_scrotal_surface` / `external_internal_boundary`.
- 구성요소: external scrotal skin; attachment relation; internal organ distinction.
- 보기·상태: 중립 해부 설명·도식.
- 가까운 반례: 내부 고환을 사진에 보이는 독립 외부 기관처럼 표현.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S31](https://my.clevelandclinic.org/health/body/penis).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### perineal_location — 외부 생식기와 항문 주변 사이의 회음부 위치

- 관찰 형태: perineal region located by adjacent external anatomical landmarks
- 소유자/속성: `adult_perineal_surface` / `regional_location`.
- 구성요소: external genital regional boundary; anal regional boundary; intervening perineal surface.
- 보기·상태: 중립 해부 설명·도식.
- 가까운 반례: 부위 이름에서 노출·성행위·건강 의미를 추가.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S10](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-6-anatomical-terminology), [S30](https://my.clevelandclinic.org/health/body/vulva), [S31](https://my.clevelandclinic.org/health/body/penis).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### limb_difference — 요청에 명시된 사지의 길이·수·연결 차이

- 관찰 형태: explicitly requested limb segment differences with coherent body attachment
- 소유자/속성: `adult_limb` / `segment_attachment`.
- 구성요소: requested limb configuration; continuous attachment; visible segment endpoints.
- 보기·상태: 요청된 신체 구성과 자세.
- 가까운 반례: 원인을 자동 보정하거나 원인·능력을 추정.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S39](https://www.ossur.com/en-gb/prosthetics/information/guide-to-prosthetic-legs), [S40](https://www.who.int/publications/i/item/9789240074521).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### prosthetic_connection — 잔존 사지·소켓·보철 부분의 실제 연결 관계

- 관찰 형태: coherent residual-limb socket and prosthetic-segment connection
- 소유자/속성: `adult_prosthesis_limb_relation` / `socket_segment_attachment`.
- 구성요소: residual limb endpoint; socket interface; prosthetic segment continuity.
- 보기·상태: 장치 전체와 부착 부위.
- 가까운 반례: 보철을 장식·별도 소품·금속 피부로만 처리.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S39](https://www.ossur.com/en-gb/prosthetics/information/guide-to-prosthetic-legs).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.

### mobility_contact — 몸과 이동 보조 장치의 접촉·지지 관계

- 관찰 형태: body support contacts with the explicitly requested mobility aid
- 소유자/속성: `adult_mobility_aid_relation` / `support_contact`.
- 구성요소: body contact points; aid support surfaces; continuous supported pose.
- 보기·상태: 몸과 장치 전체, 지지점 포함.
- 가까운 반례: 도구만 존재하고 신체 지지·접촉이 없음.
- 기존 소유자: 전체 코퍼스 대조 후 결정.
- 자료: [S40](https://www.who.int/publications/i/item/9789240074521).
- 세부 근거 상태: cross-domain authoring basis; operational gates remain proposals.
