# 종교·신화 도상 상세 카탈로그

140개 연구 단위의 관찰 제안이다. 모든 관계는 연구 엔티티이며 실제 frozen core target 바인딩 전에는 운영 의무나 채택 후보가 아니다.

원본 도판의 픽셀 검토와 새 이미지 생성은 수행하지 않았다. 출처의 해석·서사와 아래의 가시성 검증 제안을 구별한다.

## attribute_owner — 지물의 소유자와 역할

- 범위: 이름 자체가 아닌 인물–지물 결합
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 식별 지물의 형태; 그 지물을 가진 인물; 손·몸·받침과 지물의 위치 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: represented_actor → holds_or_associated_with → attribute
- 혼동 경계: 배경 장식에 지물이 있다고 주인공의 정체가 바뀌지 않는다; 사람의 실제 신앙은 지물에서 추정할 수 없다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Attribute | Glossary | National Gallery, London](https://www.nationalgallery.org.uk/paintings/glossary/attribute)

## head_halo — 머리 중심 두광

- 범위: 투르판 5–6세기 불상 표본의 두광
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 광휘 중심이 머리 뒤에 놓임; 머리 윤곽과 두광의 범위 구별; 전신 광휘와 별도 경계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: head_halo → centered_behind → represented_actor.head
- 혼동 경계: 전신 만돌라와 동의어가 아니다; 노출 과다·렌즈 플레어로 대체하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Buddha with radiate halo and mandorla - China (Xinjiang Autonomous Region, Turfan area) - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/36038)

## body_mandorla — 전신 만돌라

- 범위: 1480–1500년경 해당 이탈리아 성모자상의 아몬드형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 아몬드형 광휘의 위·아래 끝; 광휘 안에 놓인 전신; 머리 두광과 공간 범위 차이
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: body_aureole → encloses → represented_actor.full_body
- 혼동 경계: 다른 지역 불교 광배까지 아몬드형으로 강제하지 않는다; 머리 원반만으로 전신 광휘가 충족되지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Italian, Umbrian or Roman | The Virgin and Child in a Mandorla with Cherubim | NG702 | National Gallery, London](https://www.nationalgallery.org.uk/paintings/italian-umbrian-or-roman-the-virgin-and-child-in-a-mandorla-with-cherubim)

## arm_reliquary — 팔 모양 성유물함

- 범위: 남네덜란드 1230년경 팔형 용기
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 금속 팔·손 형태의 외함; 내용물을 보이는 두 창; 용기와 내포된 유물의 경계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: reliquary_shell → contains → relic; inspection_windows → reveal → container_interior
- 혼동 경계: 잘린 살아 있는 팔과 혼동하지 않는다; 창 없는 외함에서 유골 존재를 픽셀로 판정하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Arm Reliquary - South Netherlandish - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/471270)

## apotropaic_role — 벽사 기능과 공포 외형의 분리

- 범위: 파주주의 보호 기능 설명
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 요청에서 지정한 수호 형상; 그 형상과 보호 대상의 위치를 따로 기록
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: guardian_image → protective_context_for → protected_target
- 혼동 경계: 괴물 외형이 악역 역할을 자동 지정하지 않는다; 보호 효능 자체는 정지 이미지에서 입증할 수 없다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Pazuzu, le roi des démons de l'empire assyrien](https://www.louvre.fr/louvreplus/video-pazuzu-le-roi-des-demons-de-l-empire-assyrien)

## buddhapada — 불족적의 기호형

- 범위: 초기 인도 불교 조각의 발자국형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 발바닥·발가락을 읽을 수 있는 발자국 윤곽; 선택 표본의 길상 기호; 표현 면과 참배 맥락
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: footprint_motif → marks_presence_of → represented_buddha
- 혼동 경계: 평범한 발자국만으로 불족적을 확정하지 않는다; 현대 작가의 개인적 문자 배열을 고대 표준으로 만들지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Tree & Serpent: Early Buddhist Art in India, 200 BCE–400 CE - The Metropolitan Museum of Art](https://www.metmuseum.org/de/exhibitions/tree-and-serpent/visiting-guide)

## empty_throne — 빈 보좌–보리수 표상

- 범위: 초기 조각의 각성 장소 기호
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 사람이 앉지 않은 보좌; 보좌 위나 뒤의 수목; 참배 인물과 빈 자리의 분리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: bodhi_tree → above_or_behind → empty_throne; worshippers → face → empty_throne
- 혼동 경계: 빈 자리를 새 불상으로 채우지 않는다; 모든 빈 의자가 불교 기호는 아니다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Tree & Serpent: Early Buddhist Art in India, 200 BCE–400 CE - The Metropolitan Museum of Art](https://www.metmuseum.org/de/exhibitions/tree-and-serpent/visiting-guide)

## stupa_path — 탑과 회랑

- 범위: 초기 인도 스투파 설명에 한정
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 중심 봉안 기념 구조; 둘러싼 난간; 중심 구조 바깥의 순회 경로
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: circumambulatory_path → encircles → stupa; railing → bounds → circumambulatory_path
- 혼동 경계: 모든 탑을 반구형이나 같은 층수로 만들지 않는다; 서양 묘비·일반 원형 건물로 대체하지 않는다
- 후보 위치: `location`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Buddhism and Buddhist Art - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/buddhism-and-buddhist-art)

## earth_touch — 항마성도의 지면 접촉 수인

- 범위: 캄보디아 1923년 명문 불상
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 좌상; 자기 오른손이 아래 지면을 향함; 손과 좌대·지면의 위치 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: buddha.proper_right_hand → extends_toward → earth
- 혼동 경계: 화면 오른쪽과 인물 오른쪽을 혼동하지 않는다; 수인 하나에서 마라 군대 전체를 자동 추가하지 않는다
- 후보 위치: `action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Enthroned Buddha - Cambodia (probably Phnom Penh) - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/78429)

## avalokiteshvara_variants — 관음의 지역별 표상 보류

- 범위: 인도·티베트와 동아시아 표상 차이
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 요청에 명시된 지역·시대형을 우선 선택; 선택형에서의 지물·관·팔 수만 따로 조사
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: variant_record → scopes → represented_bodhisattva
- 혼동 경계: 관음이라는 이름만으로 여성·흰 옷·천수형 중 하나를 고정하지 않는다; 실제 참조 인물의 성별·신앙을 추론하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Glossary | Project Himalayan Art](https://rubinmuseum.org/projecthimalayanart/glossary/)

## five_buddha_families — 오불의 방위·색·지물 배치

- 범위: 자료에 명시된 Yoga Tantra 오불 체계
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 중앙 비로자나 백색·륜; 동방 아촉 청색·금강저, 서방 아미타 적색·연꽃; 남방 보생 황색·보주, 북방 불공성취 녹색·교차 금강저
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: mandala_record → assigns_direction_color_attribute_to → five_family_actors
- 혼동 경계: 나침반 방위와 그림의 위아래를 동일시하지 않는다; 다른 만다라·종파의 배치를 이 레시피로 덮지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Glossary | Project Himalayan Art](https://rubinmuseum.org/projecthimalayanart/glossary/)

## vajra_bell_pair — 금강저–금강령 짝

- 범위: 티베트 18세기 금강령 표본과 설명
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 종 몸통과 손잡이를 가진 금강령; 끝이 갈라지는 짧은 금강저; 서로 다른 도구의 동시 식별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: vajra → paired_with → bell
- 혼동 경계: 둘을 하나의 무기로 합치지 않는다; 우·좌 손 배치는 선택 도상의 근거 없이 보편 규칙으로 정하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Bell | Rubin Museum of Himalayan Art](https://rubinmuseum.org/collection/sc2022-3-2-2/)

## five_prong_bell — 오고령의 다섯 갈래 구조

- 범위: 일본 e-Museum 해당 금속품
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 중앙의 팔각형 금강 끝; 안으로 굽는 주변 네 갈래; 아래쪽 종 몸통
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: bell_handle → terminates_in → central_prong_and_four_side_prongs
- 혼동 경계: 끝 다섯 개와 손잡이 다섯 개를 혼동하지 않는다; 다른 일고·삼고·구고형에 오고 수를 강제하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [e-Museum - Five-Pronged <i>Vajra</i> Bell with the Four Great Wisdom Kings](https://emuseum.nich.go.jp/detail?content_base_id=100042&content_part_id=000&content_pict_id=0&langId=en)

## kartika_shape — 카트리카의 곡도 구조

- 범위: 밀교 도상 안내의 곡도
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 넓은 곡선 칼날; 칼날 위 손잡이; 지물을 잡는 손과 칼의 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: deity.hand → grips → curved_knife.handle
- 혼동 경계: 시바 삼지창·주방 칼·서양 낫으로 대체하지 않는다; 칼이 있다는 이유로 새 공격 사건을 만들지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Rubin Museum: Project Himalayan Art Looking Guide](https://rubinmuseum.org/projecthimalayanart/wp-content/uploads/sites/2/2023/01/Looking-Guide-Project-Himalayan-Art.pdf)

## kapala_shape — 카팔라의 잔 구조

- 범위: 해골잔이라는 도구 범주; 재료 인증은 별도
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 그릇처럼 열린 상부; 두개골형 곡면; 선택 도상에서의 받침·내용물
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: holder.hand → supports → skull_cup
- 혼동 경계: 두개골 전체·해골 가면과 같은 물체가 아니다; 내용물의 종류나 실제 인간 유래는 외형으로 인증하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Rubin Museum: Project Himalayan Art Looking Guide](https://rubinmuseum.org/projecthimalayanart/wp-content/uploads/sites/2/2023/01/Looking-Guide-Project-Himalayan-Art.pdf)

## khatvanga_owner — 캇방가의 팔꿈치–어깨 지지

- 범위: HAR 94 붉은 바즈라바라히 중심상
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 긴 지팡이; 자기 왼쪽 팔꿈치 굽힘에 지팡이가 걸림; 지팡이가 왼쪽 어깨 방향으로 이어짐
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: vajravarahi.left_elbow → supports → khatvanga; khatvanga → leans_against → vajravarahi.left_shoulder
- 혼동 경계: 손에 든 칼·잔과 지팡이의 소유자가 뒤섞이지 않는다; 모든 캇방가의 장식 머리 수를 이 표본으로 고정하지 않는다
- 후보 위치: `action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Mandala of Vajrayogini (Buddhist Deity) - Vajravarahi (Himalayan Art)](https://www.himalayanart.org/items/94)

## vajravarahi_red — 붉은 바즈라바라히

- 범위: HAR 94 중심상 변형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 한 인간 얼굴과 별도 멧돼지 머리 표지; 오른손의 곡도와 왼손 가슴 높이 해골잔; 붉은 몸과 춤 자세
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: deity.right_hand → holds → curved_knife; deity.left_hand → holds_at_heart → skull_cup; boar_head → attached_to → deity.head
- 혼동 경계: 멧돼지 머리 없는 바즈라요기니와 구별한다; 히indu 바라히의 전신 멧돼지 얼굴로 교체하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Mandala of Vajrayogini (Buddhist Deity) - Vajravarahi (Himalayan Art)](https://www.himalayanart.org/items/94)

## chakra_blue12 — 차크라삼바라 청색 열두 팔형

- 범위: 카트만두 1575–1600년 작품
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 청색 주 신격의 열두 팔; 주 팔이 붉은 배우자를 감싸고 금강저·령을 가짐; 청색 바이라바·적색 칼라라트리 위의 발
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: main_deity.principal_arms → embrace → consort; main_deity.feet → trample → two_named_subordinates
- 혼동 경계: 백색 두 팔 좌상과 하나의 조합으로 합치지 않는다; 팔 수만 맞고 배우자와 지물 소유자가 틀리면 실패
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Chakrasamvara and Vajravarahi - Nepal, Kathmandu Valley - Malla period - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/78190)

## chakra_white2 — 차크라삼바라 백색 두 팔 좌상

- 범위: HAR 432의 중앙 장수 성취형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 백색 한 얼굴 두 손; 가슴에서 교차한 금강저·령; 붉은 배우자가 무릎에 앉아 다리로 감쌈
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: main_deity.hands → cross_at → main_deity.heart; consort.legs → embrace → main_deity; consort → seated_in → main_deity.lap
- 혼동 경계: 청색 열두 팔형의 팔·입상·발밑 인물을 섞지 않는다; 주변 보살의 손 수를 중심상에 옮기지 않는다
- 후보 위치: `relational_action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Chakrasamvara (Buddhist Deity) (Himalayan Art)](https://www.himalayanart.org/items/432)

## hevajra_eight16 — 헤바즈라 여덟 얼굴·열여섯 손형

- 범위: HAR 90531
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 총 여덟 얼굴; 열여섯 손이 각각 해골잔을 가짐; 밝은 청색 나이라트미야와 중심 팔 결합
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: each_hevajra_hand → holds → its_own_skull_cup; central_arms → embrace → nairatmya
- 혼동 경계: 차크라삼바라 12팔과 대체하지 않는다; 잔 속 모든 내용을 하나로 통일하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Hevajra (Buddhist Deity) (Himalayan Art)](https://www.himalayanart.org/items/90531)

## wrathful_protector — 분노존 외형과 보호 역할

- 범위: 티베트 야만타카 해당 작품의 해석
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 요청에서 지정한 야만타카 형상; 분노 표정·지물의 소유자를 선택형 안에서 확인
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: wrathful_form → represents → specified_protector_role
- 혼동 경계: 야만타카 이름만으로 모든 얼굴·팔 수를 확정하지 않는다; 불꽃·송곳니를 악역이나 공격 의사로 자동 번역하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Yamantaka, Destroyer of the God of Death - Tibet - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/37807)

## vajrakila_dagger — 바즈라킬라와 삼면 칼날형

- 범위: 기관 용어 설명에 있는 하반신 킬라형 변형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택형의 상부 분노존; 아래쪽으로 길어지는 칼날 몸; 서로 만나는 세 면의 날
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: selected_deity.lower_body → takes_form_of → three_sided_kila
- 혼동 경계: 일반 휴대 푸르바와 신격 전신형은 별도; 모든 바즈라킬라를 이 칼날 몸으로 고정하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Vajrakila | Project Himalayan Art](https://rubinmuseum.org/projecthimalayanart/glossary/vajrakila/)

## mandala_architecture — 네 문 궁전형 만다라

- 범위: 네팔 1100년경 해당 차크라삼바라 만다라
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 사각 궁전의 네 출입구; 중앙 도상과 연꽃 구역; 외곽 금강·불꽃 고리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: four_gate_palace → contains → central_deity_region; outer_rings → encircle → palace
- 혼동 경계: 어떤 원형 장식도 만다라로 확정하지 않는다; 모든 만다라에 이 팔 시체림 배열을 추가하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Chakrasamvara Mandala - Nepal - Thakuri–early Malla periods - The Metropolitan Museum of Art](https://www.metmuseum.org/ko/art/collection/search/38021)

## mandala_foundation — 교차 삼각형 기초와 육각별 경계

- 범위: HAR 94 만다라 중앙 기초
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택 만다라의 두 교차 삼각형; 중앙 신격과 기초의 위치
- 비시각적 맥락: 설명상 두 사면체의 투영 맥락
- 소유·관계: crossed_triangle_foundation → underlies → mandala_central_region
- 혼동 경계: 육각형 실루엣이 같아도 마겐 다비드 별칭으로 병합하지 않는다; 평면 픽셀에서 숨은 입체 구조를 검증했다고 하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Mandala of Vajrayogini (Buddhist Deity) - Vajravarahi (Himalayan Art)](https://www.himalayanart.org/items/94)

## cham_mask_performer — 참의 가면과 착용자

- 범위: 구루 도르제 드롤로 의례 춤용 가면 자료
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 별도 가면의 얼굴 형상; 가면 아래 착용자의 몸과 의복; 공연 맥락의 착용 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: performer.head → wears → ritual_mask
- 혼동 경계: 가면의 신격과 실제 착용자를 같은 정체로 추론하지 않는다; 기괴한 가면을 일반 축제 소품으로만 축소하지 않는다
- 후보 위치: `costume_style`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Project Himalayan Art: Ritual Dance Mask of Guru Dorje Drolo](https://rubinmuseum.org/projecthimalayanart/wp-content/uploads/sites/2/2024/01/Ritual-Dance-Mask-of-Guru-Dorje-Drolo-I-Project-Himalayan-Art.pdf)

## nataraja_chola — 촐라 나타라자의 손·발 지물

- 범위: 타밀나두 11세기 해당 청동
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 위 오른손 북·위 왼손 불; 아래 오른손 시무외인·앞 왼손이 든 왼발을 가리킴; 오른발이 아파스마라를 밟고 둘레에 불꽃 고리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: shiva.upper_right_hand → holds → drum; shiva.upper_left_hand → holds → fire; shiva.right_foot → tramples → apasmara; shiva.front_left_hand → points_to → shiva.raised_left_foot
- 혼동 경계: 화면 좌우를 인물 좌우로 오인하지 않는다; 수호 제압을 성인 간 임의 폭행 사건으로 바꾸지 않는다
- 후보 위치: `action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Shiva as Lord of Dance (Nataraja) - Indian (Tamil Nadu) - Chola period (880–1279) - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/39328)

## ardhana_cambodia — 한 몸의 아르다나리슈바라

- 범위: 캄보디아 7–8세기 반환 작품 기록
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 공유된 하나의 몸; 한쪽 파르바티 머리·긴 치마; 다른 쪽 시바 수염·제삼안
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: one_body → integrates → shiva_side_and_parvati_side
- 혼동 경계: 두 인물의 포옹·두 머리 레비스와 다른 연결 구조; 이 도상에서 실제 인물의 성별·신체·정체를 추론하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Ardhanarishvara (Composite of Shiva and Parvati) - Cambodia - pre-Angkor period - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/39198)

## durga_eight — 두르가 여덟 팔 제압형

- 범위: 참바 추정 12세기 제단형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 여덟 팔과 각각의 무기; 발로 눌린 물소; 삼지창 접촉과 나타나는 인간형 마히샤
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: durga.foot → crushes → buffalo; durga.trident → impales → mahisha; human_demon → emerges_from → buffalo_form
- 혼동 경계: 네 팔 승리상에 여덟 팔을 추가하지 않는다; 물소·사자·인간형을 하나의 몸으로 무작위 합성하지 않는다
- 후보 위치: `action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [The Goddess Durga Slaying the Demon Buffalo Mahisha - India (Himachal Pradesh, probably Chamba Valley) - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/74502)

## durga_four — 두르가 네 팔 승리상

- 범위: 캄보디아 900년대 청동 표본
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 네 팔; 륜·소라·곤봉·흙덩이 지물; 발 아래 잘린 물소 머리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: durga.four_hands → hold → four_documented_attributes; buffalo_head → below → durga.feet
- 혼동 경계: 이 작품에 삼지창을 꽂는 전투 중 장면을 강제하지 않는다; 두르가를 항상 8·10팔로 고정하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Durga as the Slayer of the Buffalo Demon | Cleveland Museum of Art](https://www.clevelandart.org/art/1996.27)

## chinnamasta_streams — 친나마스타의 자기 참수·세 혈류

- 범위: 박물관이 설명한 해당 인쇄 도상의 서사
- 근거 단계: `SEARCH_EXCERPT_BODY_REACCESS_BLOCKED`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 분리된 자기 머리를 든 신격; 목에서 나오는 세 갈래 혈류; 자기 머리와 두 동반자에게 각각 이어지는 흐름
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: neck_stream_1 → reaches → self_held_head; neck_stream_2 → reaches → companion_a; neck_stream_3 → reaches → companion_b
- 혼동 경계: 다른 사람이 참수하는 장면과 다르다; 두 팔·네 팔 등 변형의 수는 별도 근거로 선택한다
- 후보 위치: `action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Demystifying Tantric sex | British Museum](https://www.britishmuseum.org/blog/demystifying-tantric-sex)

## mithuna_couple — 길상 연인상 미투나

- 범위: 오디샤 13세기 사원 파사드 부조
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 장신구를 한 두 인물; 서로 얽힌 팔·몸과 시선; 사원 장식이라는 부조 형식
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: actor_a → embraces → actor_b; actor_a.gaze → directed_to → actor_b
- 혼동 경계: 미투나라는 말만으로 성교 행위를 추가하지 않는다; 실제 참조 인물 간 관계·동의를 판정하지 않는다
- 후보 위치: `relational_action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Loving Couple (Mithuna) - India (Orissa) - Eastern Ganga dynasty - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/38141)

## maithuna_boundary — 미투나·마이투나·얍윰의 의미 경계

- 범위: 범주 구분을 위한 연구 메모; 독립 완성 도상 아님
- 근거 단계: `ANALYTIC_BOUNDARY_NOT_OBJECT_TEMPLATE`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 연인상·성적 결합·신격 결합을 서로 다른 사건 축으로 기록; 상징 해석과 실제 보이는 접촉을 분리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: request_event → selects → one_defined_union_category
- 혼동 경계: 연애·성교·밀교 합일이 같은 activation alias 집합으로 섞이지 않는다; 금욕적 나체가 결합 행위로 자동 승격되지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Loving Couple (Mithuna) - India (Orissa) - Eastern Ganga dynasty - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/38141), [Demystifying Tantric sex | British Museum](https://www.britishmuseum.org/blog/demystifying-tantric-sex)

## sri_yantra_graph — 슈리 얀트라의 위상 구조

- 범위: CE1998/7/6 교차 아홉 삼각형형; 완전한 그래프 검증 필요
- 근거 단계: `SEARCH_EXCERPT_GRAPH_REQUIRES_REVIEW`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 서로 교차하는 아홉 삼각형; 중심과 교차점을 가진 연결 그래프; 선택 표본의 바깥 경계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: triangle_graph → organized_around → central_region
- 혼동 경계: 무작위 삼각형 무늬·육각별로 대체하지 않는다; 이 자료만으로 모든 내부 소삼각형 수·정확한 정점을 검증했다고 하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [CER.es Colecciones en Red - Búsqueda general](https://ceres.mcu.es/pages/Main?inventary=CE1998%2F7%2F6&museum=58)

## generic_yantra — 연꽃형 얀트라와 슈리 얀트라 구별

- 범위: 북인도 18세기 연꽃형 금속판
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 꽃잎 형태 외곽; 꽃잎의 문자; 중앙 두 원과 삼각형
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: central_triangle → inside → two_circles; inscriptions → on → lotus_petals
- 혼동 경계: 모든 얀트라가 아홉 삼각형은 아니다; 태국 천 얀트라·밀교 기초와 같은 도상으로 합치지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [yantra | British Museum](https://www.britishmuseum.org/collection/object/A_1940-0716-329)

## jina_kayotsarga — 디감바라 카요트사르가

- 범위: 카르나타카 12세기 티르탕카라
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 장신구 없는 직립형; 팔이 몸 곁에 내려온 정적인 자세; 선택 실물의 머리 형상
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: jina.arms → hang_beside → jina.torso
- 혼동 경계: 나체가 성적 행위·현대 누드 장르를 자동 뜻하지 않는다; 해당 작품의 곱슬머리 예외를 불상과의 동일 정체 근거로 삼지 않는다
- 후보 위치: `body_orientation`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Jain Digambara Tirthanhara Standing in Kayotsarga Meditation Posture - India (Deccan, Karnataka) - Western Chalukyan period - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/39193)

## dastar_scope — 다스타르의 착용 외형과 정체 경계

- 범위: 시크 공동체의 터번 설명
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 요청된 감기 방식과 천의 겹; 머리를 감싼 착용 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: wearer.head → wrapped_by → specified_turban
- 혼동 경계: 터번만으로 실제 사람의 민족·신앙·직업을 단정하지 않는다; 모든 시크의 터번 색·형상을 하나로 고정하지 않는다
- 후보 위치: `wearable_accessory`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Identity](https://www.sikhcoalition.org/about-sikhs/identity/)

## five_ks_visible — 다섯 K의 가시성과 불가시성

- 범위: 각 요청된 다섯 K 항목의 가시성; 전 항목을 완성했다고 주장하는 프로필 아님
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 보이는 카라의 금속 고리; 선택 의복에서 보이는 캉가·키르판
- 비시각적 맥락: 감춰진 머리·속의복은 관찰 불가로 기록
- 소유·관계: kara → encircles → wearer.wrist; visible_kirpan → carried_by → wearer
- 혼동 경계: 모든 다섯 K가 한 사진에서 보여야 한다고 옷 안을 추정하지 않는다; 키르판의 착용이 공격 사건을 자동 만들지 않는다
- 후보 위치: `wearable_accessory`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Identity](https://www.sikhcoalition.org/about-sikhs/identity/)

## icon_media — 이콘의 매체와 예배 맥락

- 범위: 비잔틴 이콘의 매체 다양성
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택된 평면·모자이크·금속 피복 형식; 도상과 물질적 지지체의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: icon_image → rendered_on → selected_support
- 혼동 경계: 이콘을 컴퓨터 UI 아이콘 별칭과 섞지 않는다; 예배 기능·기적적 제작을 외형에서 입증하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Icons and Iconoclasm in Byzantium - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/icons-and-iconoclasm-in-byzantium)

## hodegetria_pointing — 호데게트리아의 가리키기

- 범위: 자료에서 설명한 성모자의 좌우 관계
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 성모 왼팔에 놓인 아기; 성모 오른손이 아기를 가리킴; 두 인물과 손 접촉의 소유자
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: mary.left_arm → supports → child; mary.right_hand → points_to → child
- 혼동 경계: 성모자라는 말만으로 이 좌우 배치를 모든 작품에 강제하지 않는다; 엘레우사의 얼굴 접촉을 필수로 섞지 않는다
- 후보 위치: `relational_action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Icons and Iconoclasm in Byzantium - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/icons-and-iconoclasm-in-byzantium)

## eleousa_contact — 엘레우사의 얼굴 친밀 접촉

- 범위: 기관이 대조한 엘레우사형; 개별 원본 선정 후 보강
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 아기 얼굴이 성모 목·뺨 방향으로 올라감; 얼굴 간 가까운 접촉; 성모가 아기 몸을 지지함
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: child.face → nestles_against → mary.cheek_or_neck
- 혼동 경계: 호데게트리아 변형에서 얼굴이 떨어져 있으면 접촉 PASS로 추정하지 않는다; 실제 모자 관계나 감정을 인증하는 기준으로 쓰지 않는다
- 후보 위치: `relational_action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Byzantine or Crusader - Icon of the Virgin and Child, Hodegetria variant - Byzantine or Crusader - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/831188)

## virgin_hybrid_variant — 호데게트리아 혼합 변형

- 범위: 13세기 비잔틴·십자군 해당 작품
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 성모의 아기 가리키기; 위로 향한 아기 얼굴; 성모 목에 완전히 붙지 않은 아기 위치
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: mary.hand → points_to → child; child.face → turned_up_toward → mary; child.face → separated_from → mary.neck
- 혼동 경계: 호데게트리아와 엘레우사 단어가 함께 있음을 곧 모순으로 판정하지 않는다; 자료가 구별한 거리 차이를 지워서 표준형으로 돌리지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Byzantine or Crusader - Icon of the Virgin and Child, Hodegetria variant - Byzantine or Crusader - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/831188)

## mandylion_face_cloth — 만딜리온의 얼굴–천

- 범위: 자료에 설명된 만딜리온 전승
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 흰 천의 경계; 천 위 그리스도 얼굴; 독립된 얼굴상과 지지 천의 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: christ_face_image → on → white_cloth
- 혼동 경계: 케라미온의 타일과 천을 같은 재료로 처리하지 않는다; 실제 제작 방식이 기적임을 이미지로 입증하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Icons and Iconoclasm in Byzantium - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/icons-and-iconoclasm-in-byzantium)

## acheiropoieta_status — 아케이로포이에타의 비시각적 제작 전승

- 범위: 기적적 제작이라는 해석 범주
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택된 물질과 얼굴상은 별도 관찰; 제작 전승은 출처·맥락 필드에만 기록
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: tradition_record → attributes_origin_to → icon_image
- 혼동 경계: 특정 외형·필터가 기적적 제작의 증거가 되지 않는다; 모든 만딜리온 복제물이 원본 유물과 같은 정체는 아니다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Icons and Iconoclasm in Byzantium - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/icons-and-iconoclasm-in-byzantium)

## anastasis_harrowing — 아나스타시스의 끌어올림 관계

- 범위: 비잔틴 구원 도상의 서사; 세부 실물 재검토 필요
- 근거 단계: `SEARCH_EXCERPT_DETAILS_PENDING`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 그리스도가 아래 인물을 끌어올리는 접촉; 아담·하와의 구별된 위치; 하부 지하세계의 문·공간
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: christ → raises → adam; christ → raises_or_addresses → eve; broken_gates → below → christ
- 혼동 경계: 지하세계 진입·피에타·개별 무덤 부활을 하나의 사건으로 합치지 않는다; 그림별 손목 소유자·문 수는 원본으로 확정한다
- 후보 위치: `relational_action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Smarthistory – The lives of Christ and the Virgin in Byzantine art](https://smarthistory.org/the-lives-of-christ-and-the-virgin-in-byzantine-art/)

## dormition_soul — 성모 안식의 몸과 영혼 표상

- 범위: 비잔틴 성모 안식 도상; 세부 표본 재검토 필요
- 근거 단계: `SEARCH_EXCERPT_DETAILS_PENDING`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 누워 있는 성모의 몸; 뒤쪽 그리스도; 그리스도가 든 작은 영혼 표상
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: mary.body → lies_on → bed; christ.hands → hold → small_soul_representation
- 혼동 경계: 작은 표상을 새 현실 아기로 자동 해석하지 않는다; 피에타의 성모–성인 아들 지지 관계와 소유자가 뒤바뀌지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Smarthistory – The lives of Christ and the Virgin in Byzantine art](https://smarthistory.org/the-lives-of-christ-and-the-virgin-in-byzantine-art/)

## pieta_support — 피에타의 성인 몸 지지

- 범위: 보헤미아 1400년경 베스페르빌트
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 성모의 옷 입은 몸; 성인 그리스도의 힘없는 몸; 무릎·팔의 지지와 손목 잡기
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: mary.lap → supports → christ.body; mary.hand → grasps → christ.wrist
- 혼동 경계: 성모자상의 아기나 연인 포옹으로 축소하지 않는다; 경전의 직접 장면인지 여부는 도상 외형과 별도
- 후보 위치: `relational_action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Pietà (Vesperbild) - Bohemian - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/473331)

## lucy_plate_eyes — 루치아의 접시 위 눈

- 범위: 크리벨리 NG788.12
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 한 손의 둥근 목제 접시; 접시 위 별도 두 눈; 다른 손의 순교 종려
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: lucy.hand_a → holds → wooden_plate; two_eye_attributes → rest_on → plate; lucy.hand_b → holds → martyr_palm
- 혼동 경계: 순교 표지를 얼굴의 빈 안와로 자동 확대하지 않는다; 안구처럼 보이는 배경 구슬은 접시 위 지물을 충족하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Carlo Crivelli | Saint Lucy | NG788.12 | National Gallery, London](https://www.nationalgallery.org.uk/paintings/carlo-crivelli-saint-lucy)

## bartholomew_knife — 바르톨로메오의 칼 지물

- 범위: 성인 식별 지물과 순교 전승의 분리
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 성인과 칼의 위치 연결; 별도 요청 없을 때 온전한 인물 외형
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: saint.hand → holds → knife_attribute
- 혼동 경계: 칼 지물 요청을 박피 실행이나 피부 훼손으로 자동 확대하지 않는다; 해골잔·곡도 지물과 이름만으로 동일시하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [St Bartholomew | Glossary | National Gallery, London](https://www.nationalgallery.org.uk/paintings/glossary/st-bartholomew)

## agatha_attribution — 성 아가타 지물과 초상 정체

- 범위: 박물관 제목상 성 아가타의 지물을 가진 여인
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 초상 인물; 소유한 순교 표지; 얼굴·몸과 별도 지물의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: portrait_sitter → carries → saint_attributes
- 혼동 경계: 성인 지물을 지닌 초상 인물이 곧 그 성인이라는 자동 추론을 막는다; 지물의 정확한 신체 부분 외형은 본문·원본 확인까지 보류
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Sebastiano del Piombo | Portrait of a Lady with the Attributes of Saint Agatha | NG24 | National Gallery, London](https://www.nationalgallery.org.uk/paintings/sebastiano-del-piombo-portrait-of-a-lady-with-the-attributes-of-saint-agatha)

## peter_keys — 베드로의 열쇠 소유자

- 범위: 로렌초 코스타 해당 작품
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 인물 손에 모인 열쇠 지물; 열쇠와 손의 접촉; 다른 손의 제스처
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: peter.hand → holds → keys
- 혼동 경계: 열쇠가 배경 문에 있다고 같은 식별 관계가 성립하지 않는다; 열쇠 수·색·역십자가는 선택 원본 없이 강제하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Lorenzo Costa | Saint Peter | NG629.2 | National Gallery, London](https://www.nationalgallery.org.uk/paintings/lorenzo-costa-saint-peter)

## hanukkiah_holders — 하누키아의 여덟 심지와 샤마시

- 범위: 볼페르트 1935–48년 은제 표본
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 반원 배열의 여덟 심지 받침; 따로 놓인 작은 샤마시 주전자; 각 점등 자리가 서로 구별됨
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: eight_wick_holders → arranged_in → semicircle; shamash_jug → distinct_from → eight_holders
- 혼동 경계: 아홉 점등 자리를 아홉 가지로 일률 변환하지 않는다; 일곱 가지 메노라·이미 켜진 불 수와 구조 수를 구별한다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [The Jewish Museum - Online Collection - Hanukkah Lamp](https://collections.thejewishmuseum.org/collection/1527-hanukkah-lamp)

## tefillin_pair — 테필린 두 상자와 착용부

- 범위: Chabad 설명의 머리·위팔 세트
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 검은 가죽 머리 상자; 위팔의 별도 상자; 상자를 몸에 잇는 끈
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: head_box → strapped_to → wearer.head; arm_box → strapped_to → wearer.upper_arm
- 혼동 경계: 이마와 손목에 같은 장신구를 복사하지 않는다; 닫힌 상자 안의 두루마리·칸 수를 보였다고 판정하지 않는다
- 후보 위치: `wearable_accessory`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [What Are Tefillin? - Chabad.org](https://www.chabad.org/library/article_cdo/aid/1918251/jewish/What-Are-Tefillin.htm)

## tallit_corner_fringe — 탈리트 모서리 치치트

- 범위: 해당 공동체의 의례 물건 설명
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택된 숄 모서리; 모서리에 달린 술; 의복 본체와 별도 술의 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: tzitzit → attached_to → tallit.corners
- 혼동 경계: 줄무늬만으로 탈리트를 판정하지 않는다; 화면 밖 모서리의 술을 보인 것으로 추정하지 않는다
- 후보 위치: `garment_detail`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [19 Ritual Items Found in a Jewish Home - Chabad.org](https://www.chabad.org/library/article_cdo/aid/5489978/jewish/19-Ritual-Items-Found-in-a-Jewish-Home.htm)

## sefirot_diagram — 세피로트 도식의 연결과 문자

- 범위: 국립도서관 일라노트 자료의 원고별 도식
- 근거 단계: `DIAGRAM_REQUIRES_CURATED_TRANSCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택 원고의 노드 배열; 노드 사이 연결; 노드 명칭과 본문의 문자 영역
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: named_nodes → connected_by → documented_edges
- 혼동 경계: 모든 카발라 도식을 현대 오컬트의 같은 10구 도형으로 고정하지 않는다; 문자 정확성 없이 점·원 개수만으로 PASS하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [The Kabbalistic Tree: The Map of God](https://blog.nli.org.il/en/djm_ilanot/)

## mihrab_minbar — 미흐라브와 민바르의 공간 역할

- 범위: 기관 용어집의 전형적 모스크 관계
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 벽의 기도 방향 니치; 니치 옆 계단형 설교단; 니치·계단의 서로 다른 기능적 구조
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: mihrab → in → qibla_wall; minbar → beside → mihrab
- 혼동 경계: 미흐라브는 제단·설교단과 같은 물체가 아니다; 민바르가 보통 오른쪽이라는 설명을 모든 실물에 강제하지 않는다
- 후보 위치: `location`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Glossary | The Metropolitan Museum of Art](https://www.metmuseum.org/learn/educators/curriculum-resources/art-of-the-islamic-world/resources/glossary)

## muqarnas_cells — 무카르나스의 입체 셀

- 범위: 종유석·벌집형 건축 요소 정의
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 반복되는 입체 셀; 층별 돌출과 후퇴; 아치·천장 등 실제 배치면
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: three_dimensional_cells → step_across → architectural_surface
- 혼동 경계: 평면 기하 문양·샹들리에·금속 그릴로 대체하지 않는다; 이 구조만으로 건물의 종교 정체를 인증하지 않는다
- 후보 위치: `location`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Glossary | The Metropolitan Museum of Art](https://www.metmuseum.org/learn/educators/curriculum-resources/art-of-the-islamic-world/resources/glossary)

## kaba_focus — 카바의 건물과 주변 예배 공간

- 범위: 기관 정의의 메카 카바
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 입방형 중심 건물; 주변의 별도 예배 공간; 건물과 주변 인물·경로의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: prayer_space → surrounds → kaba_structure
- 혼동 경계: 검은 입방체라는 형상만으로 실제 장소를 확정하지 않는다; 현재 건물 장식·행사·군중 규모는 이 정의에서 추정하지 않는다
- 후보 위치: `location`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Glossary | The Metropolitan Museum of Art](https://www.metmuseum.org/learn/educators/curriculum-resources/art-of-the-islamic-world/resources/glossary)

## islam_figural_context — 이슬람 미술의 형상 사용 맥락

- 범위: 종교 공간·세속 물건·회화의 구분
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택 작품의 매체·용도; 사람·동물·문자 영역의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: source_record → scopes → depiction_context
- 혼동 경계: 이슬람이라는 범주에서 모든 인물·동물 표현을 지우지 않는다; 세속 회화 표본을 모든 모스크에 그대로 적용하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Figural Representation in Islamic Art - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/figural-representation-in-islamic-art)

## sema_motion_evidence — 세마 의례와 정지 장면 한계

- 범위: UNESCO 메블레비 의례 설명
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택된 의례복과 참가자 배열; 회전을 암시하는 몸·옷 자세; 의례 맥락과 공연·인물 외형의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: performer.body → poses_within → specified_ceremony_context
- 혼동 경계: 정지 이미지 한 장에서 실제 회전 방향·연속 동작을 확인했다고 하지 않는다; 비슷한 긴 치마를 입었다고 세마나 신앙을 확정하지 않는다
- 후보 위치: `action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Mevlevi Sema ceremony - UNESCO Intangible Cultural Heritage](https://ich.unesco.org/en/RL/mevlevi-sema-ceremony-00100?RL=00100)

## buraq_golconda — 골콘다 합성체 부라크

- 범위: 1660–80년 해당 회화의 무탑승자형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 여성 얼굴 표상; 작은 동물·물고기·새로 이루어진 몸; 탑승자가 없는 표본의 구성
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: small_animal_forms → compose → buraq.body; human_face → belongs_to → buraq.head
- 혼동 경계: 일반 날개 달린 말과 동일하지 않다; 요청 없이 탑승자를 추가하거나 모든 부라크를 무탑승자로 고정하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [The Fabulous Creature Buraq - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/453334)

## daoist_robe_sky — 도교 의례복의 천상 자수

- 범위: 청대 18세기 말 해당 의례복의 뒷면
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 탑이 든 큰 원형 구역; 위쪽 해·금까마귀와 달·옥토끼 구역; 옷 전면의 흰 학 자수
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: sun_crow_and_moon_rabbit → above → pagoda_roundel; crane_motifs → embroidered_on → robe
- 혼동 경계: 화면 좌우 표기와 입은 사람의 좌우를 재검토한다; 모든 도교 복식에 이 구성을 복사하지 않는다
- 후보 위치: `garment_detail`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Daoist priest’s ritual robe with celestial palace - China - Qing dynasty (1644–1911) - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/68508)

## daoist_robe_xuanwu — 도교 의례복의 현무 연결

- 범위: 같은 청대 옷의 하단 동물 자수
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 거북 형상; 거북을 감은 별도 뱀; 자수라는 물질적 표현
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: snake_motif → entwines → tortoise_motif
- 혼동 경계: 자수 표지를 인물의 생물학적 몸으로 흡수하지 않는다; 진무 신격 전체와 현무 동물 모티프를 같은 인물로 병합하지 않는다
- 후보 위치: `garment_detail`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Daoist priest’s ritual robe with celestial palace - China - Qing dynasty (1644–1911) - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/68508)

## daoist_system_scope — 도교의 분파·신격 체계

- 범위: 범주 수준의 맥락; 개별 지물은 별도 조사
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택 분파·시대·물건 기록; 관료형 신격·불사 선경을 다른 장면 유형으로 구분
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: tradition_variant → scopes → named_iconography
- 혼동 경계: 팔선이라는 이름에서 특정 장면·8인 배치를 자동 고정하지 않는다; 노자·여동빈 지물을 일반 동아시아 의상 소품과 병합하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Daoism and Daoist Art - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/daoism-and-daoist-art)

## musindo_genre — 무신도의 신격·장르 구분

- 범위: 무신도 범주 설명; 개별 신당 기록 필요
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 그려진 신격과 그림 지지체; 신당의 봉안 위치는 개별 사례; 방울·부채 등 집행자의 물건은 별도 소유자
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: deity_portrait → depicts → named_deity; ritual_tools → owned_by → specified_practitioner
- 혼동 경계: 무신도·무당 초상·굿 장면을 같은 그림으로 취급하지 않는다; 불교·도교 도상을 모두 임의 혼합 가능한 소품으로 만들지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [무신도 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0019111)

## sanshin_old_tiger — 노인·호랑이형 산신도

- 범위: 백과사전의 대체적 일반형에 한정
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 백발·긴 수염의 산신; 산·골짜기 배경; 산신이 기대 앉은 별도 호랑이
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: sanshin.body → leans_against → tiger; mountain_landscape → behind → sanshin_and_tiger
- 혼동 경계: 일반형이 모든 산신도의 정의는 아니다; 호랑이 자체가 인물 몸의 일부가 되지 않는다
- 후보 위치: `relational_action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [산신도 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0026273)

## sanshin_variant_guard — 여성·무호랑이 산신도 허용

- 범위: 자료가 열거한 소수 변형
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택된 여성·제왕·승려 등 변형 기록; 호랑이 동반 여부를 독립 필드로 둠
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: variant_record → determines → figure_type_and_companions
- 혼동 경계: 산신 검색 hit가 여성형을 백발 남성으로 바꾸지 않는다; 호랑이 없는 명시 요청에 호랑이를 필수 지물로 추가하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [산신도 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0026273)

## jangseung_face_post — 장승의 얼굴 기둥

- 범위: 마을 경계의 목·석 장승
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 기둥형 몸과 새겨진 얼굴; 목재·석재 중 선택 재료; 선택 사례에서의 명문
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: face_carving → integrated_in → guardian_post
- 혼동 경계: 새가 장대 끝에 앉는 솟대와 구별한다; 무서운 얼굴이 악귀 역할이나 실제 효능을 입증하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [장승 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0048619)

## sotdae_three_birds — 세 새형 솟대

- 범위: 자료에 명시된 세 갈래·세 새 변형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 긴 장대; 끝의 세 갈래 가지; 각 가지 위 새 조각
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: three_bird_carvings → perch_on → three_branch_pole_top
- 혼동 경계: 솟대 일반형의 새 수를 항상 셋으로 강제하지 않는다; 장승의 얼굴·몸과 새 장대를 합치지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [솟대 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0030608)

## bari_narrative — 바리공주의 약수 획득 서사

- 범위: 무가의 서사 단락; 고정 초상 외형 없음
- 근거 단계: `NARRATIVE_SOURCE_NOT_FIXED_ICONOGRAPHY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 요청된 약수 획득 사건; 인물·물·용기의 소유자; 현실·저승 공간은 선택 각색에 맞춰 분리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: bari → obtains → life_restoring_water
- 혼동 경계: 이 이야기를 관음이나 페르세포네의 도상 외형으로 자동 대체하지 않는다; 서사 자료만으로 단일 관복·머리모양을 인증하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [바리공주 - 한국민족문화대백과사전](https://encykorea.aks.ac.kr/Article/E0020479)

## torii_boundary — 도리이의 경계 구조

- 범위: 국학원 신사 개념 설명; 세부 형태 별도 선택
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 두 기둥과 가로 부재의 문형; 문을 기준으로 구별되는 앞·뒤 공간
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: gateway → marks_boundary_of → selected_shrine_space
- 혼동 경계: 모든 도리이를 붉은 목재 명신형으로 고정하지 않는다; 일반 아치나 탑을 도리이로 대체하지 않는다
- 후보 위치: `location`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Introduction: Jinja | 國學院大學デジタルミュージアム](https://d-museum.kokugakuin.ac.jp/eos/detail/?id=9705)

## shintai_not_statue — 신체의 물건·봉안 맥락

- 범위: 신체 개념; 거울·검·곡옥의 선택형은 추가 실물 필요
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 요청된 물건 또는 자연물; 봉안·가림 상태; 대상과 용기의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: selected_shintai → enshrined_in → specified_shrine_context
- 혼동 경계: 신체를 인간형 신상과 같은 필수 외형으로 고정하지 않는다; 닫힌 봉안물을 보였다고 내부 형태를 추정하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Introduction: Jinja | 國學院大學デジタルミュージアム](https://d-museum.kokugakuin.ac.jp/eos/detail/?id=9705)

## uzume_narrative — 우즈메 춤과 동굴 은둔의 서사

- 범위: 고사기·일본서기 설명의 분리
- 근거 단계: `NARRATIVE_SOURCE_NOT_FIXED_ICONOGRAPHY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 동굴 안·밖의 관계; 춤추는 우즈메와 다른 관람 신격의 구별; 요청된 옷·노출 상태만 표시
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: uzume → performs_outside → amaterasu_cave
- 혼동 경계: 문헌의 노출을 모든 현대 재현의 동일 의상·행동으로 강제하지 않는다; 춤의 결과·감정·효능은 픽셀로 인증하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Amenouzume | 國學院大學デジタルミュージアム](https://d-museum.kokugakuin.ac.jp/eos/detail/?id=9422)

## tsukumogami_object_body — 쓰쿠모가미의 도구 몸

- 범위: 그림 두루마리 연구에서 식별되는 도구형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 원래 생활 도구의 실루엣; 그 도구에 붙은 얼굴·팔다리; 도구 몸과 추가 생명 표지의 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: animated_face_and_limbs → attach_to → recognizable_utensil_body
- 혼동 경계: 일반 사람 요괴·오니·로봇과 동일하지 않다; 백 년의 실제 사용 이력은 외형으로 입증하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [NIJL: Tsukumogami emaki and Urban Spaces](https://www.nijl.ac.jp/pages/onlinejournal/sjlc/images/sjlc04.pdf)

## hyakki_scroll — 백귀야행의 두루마리 행렬

- 범위: 선정한 두루마리의 행렬 구성
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 여러 개별 요괴·도구형 인물; 가로로 이어지는 행렬; 그림 지지체와 장면의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: distinct_figures → form → horizontal_procession
- 혼동 경계: 백귀를 숫자 100마리 강제 생성으로 해석하지 않는다; 박물관 두루마리 촬영과 실물 판타지 장면을 합치지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [NIJL: Tsukumogami emaki and Urban Spaces](https://www.nijl.ac.jp/pages/onlinejournal/sjlc/images/sjlc04.pdf), [付喪神絵詞 | 日文研デジタルアーカイブ](https://da.nichibun.ac.jp/en/item/004637120)

## heart_ani_roles — 아니 파피루스의 계량 역할

- 범위: BM EA10470-3
- 근거 단계: `SEARCH_EXCERPT_BODY_REACCESS_BLOCKED`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 명시된 심판 대상인 죽은 인물; 양팔 저울의 심장과 마아트 깃털; 아누비스의 저울 조정; 토트의 기록 행위; 암미트 대기 또는 오시리스 결과 수령
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: anubis → steadies → scale; heart → weighed_against → maat_feather; thoth → records → weighing; deceased → faces → judgment_scale; ammit_or_osiris → establishes → judgment_consequence
- 혼동 경계: 아누비스·토트·암미트의 역할을 뒤바꾸지 않는다; 기존 egyptian_heart_weighing_judgment 의미 소유자를 재사용한다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [British Museum: 아니 파피루스 EA10470-3](https://www.britishmuseum.org/collection/object/Y_EA10470-3)

## heart_maat_figure — 깃털 대신 마아트 소형상 계량형

- 범위: BM EA10554-80 그린필드 파피루스
- 근거 단계: `SEARCH_EXCERPT_BODY_REACCESS_BLOCKED`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 한 저울 접시의 심장; 다른 접시의 앉은 마아트 형상; 마아트 머리의 깃털 표지
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: heart → weighed_against → small_maat_figure; feather → on → maat_figure.head
- 혼동 경계: 모든 심장 계량 장면의 반대편을 단독 깃털로 고정하지 않는다; 소형상을 새 동반 인물로 복제하지 않는다; 현재 기존 profile의 heart_feather_balance를 그대로 만족하지 않는다. 의미를 몰래 넓히지 말고 별도 변형 profile 초안이 필요하다.
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [British Museum: 그린필드 파피루스 EA10554-80](https://www.britishmuseum.org/collection/object/Y_EA10554-80)

## wedjat_form — 우자트의 눈 형태

- 범위: 선택 이집트 눈 부적; 좌우 변형 별도
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 눈썹·눈·아래 표지로 구성된 윤곽; 부적의 외곽; 현실 얼굴과 독립된 물건
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: eye_motif → incised_or_formed_on → amulet
- 혼동 경계: 실제 손상된 안구·루치아의 접시 눈과 같은 물체가 아니다; 좌·우 눈이나 모든 내부 선은 선정 표본으로 확정한다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Ancient Egyptian Amulets - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/egyptian-amulets)

## scarab_heart_scope — 스카라브와 심장 스카라브의 범주

- 범위: 풍뎅이 부적의 형상과 특정 장례 기능
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 풍뎅이 등껍질 윤곽; 물건의 밑면·명문은 보일 때만 기록
- 비시각적 맥락: 몸 위 배치 여부는 요청·실물 근거에 따름
- 소유·관계: inscription_if_visible → on → scarab.underside
- 혼동 경계: 풍뎅이 모양만으로 심장용 주문·장례 기능을 인증하지 않는다; 모든 스카라브를 파란 파이앙스로 고정하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Ancient Egyptian Amulets - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/egyptian-amulets)

## faience_visible_finish — 이집트 파이앙스의 표면과 재료 경계

- 범위: 소장품 재료 설명과 표면 관찰의 분리
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택한 유약 광택; 선택 표본의 색·마모
- 비시각적 맥락: 재료명은 소장 기록에서 인용
- 소유·관계: documented_material → described_in → object_record
- 혼동 경계: 청록색이라 해서 파이앙스라고 픽셀로 인증하지 않는다; 일반 점토 도기·금속·유리와 재료명을 자동 병합하지 않는다
- 후보 위치: `surface_material`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Ancient Egyptian Amulets - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/egyptian-amulets)

## book_dead_corpus — 사자의 서의 주문 집합

- 범위: 장례 주문·도상 자료의 범주
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택 파피루스의 문장과 도상 구역; 각 주문·삽화 단위; 전체 두루마리와 일부 장면의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: selected_vignette → part_of → specific_funeral_manuscript
- 혼동 경계: 하나의 고정 책·한 가지 심판 장면으로 모든 사자의 서를 대체하지 않는다; 문자 전사를 확인하지 않고 의미를 인증하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [What is a Book of the Dead? | British Museum](https://www.britishmuseum.org/blog/what-book-dead)

## meso_horn_crown — 메소포타미아 뿔 관

- 범위: 신성 표지 범주; 시대별 관형은 별도
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 머리에 놓인 관; 겹치는 뿔 쌍; 관과 머리 자체의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: horn_pairs → belong_to → crown; crown → worn_on → represented_head
- 혼동 경계: 신의 관 장식을 생물학적 뿔로 흡수하지 않는다; 뿔 수·신격 정체를 일반형 하나로 고정하지 않는다
- 후보 위치: `wearable_accessory`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Mesopotamian Deities - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/mesopotamian-deities)

## ishtar_emblem — 이슈타르의 지물 조합

- 범위: 출처가 연결하는 별·로제트·사자 범주
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택한 별 또는 로제트; 인물·사자와의 소유·동반 위치; 표지의 배치면
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: star_or_rosette → associated_with → named_ishtar_form
- 혼동 경계: 별 모양 하나에서 모든 신격 정체를 확정하지 않는다; 북유럽·도교·유대교 별 도식과 같은 activation으로 섞지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Mesopotamian Deities - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/mesopotamian-deities)

## sin_crescent — 신·난나의 초승달 표지

- 범위: 달 표지와 신격 연결 설명
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 명확한 초승달 윤곽; 지정한 신격·표석과의 위치 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: crescent → associated_with → named_sin_representation
- 혼동 경계: 하늘의 실제 달·칼날·다른 전통의 초승달이 같은 신격을 자동 활성화하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Mesopotamian Deities - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/mesopotamian-deities)

## marduk_nabu_emblems — 마르두크 삽–나부 쐐기 구별

- 범위: 서로 다른 신격 표지
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 삽 모양 표지; 별도의 쐐기 표지; 각 표지와 해당 신격의 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: spade_emblem → associated_with → marduk; wedge_emblem → associated_with → nabu
- 혼동 경계: 두 기호를 같은 무기·깃대로 합치지 않는다; 평범한 삽·필기 도구가 이름 없이 신격 장면을 생성하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Mesopotamian Deities - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/mesopotamian-deities)

## enki_fish_streams — 에아·엔키의 물과 물고기

- 범위: ORACC가 설명한 물 표지
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 인물에서 이어지는 물줄기; 물줄기 안의 물고기; 선택 관·좌상 표지
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: fish → within → flowing_streams; streams → associated_with → ea_enki
- 혼동 경계: 일반 바다·분수·포세이돈의 삼지창으로 대체하지 않는다; 압주라는 개념만으로 같은 인물 외형을 강제하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Ancient Mesopotamian Gods and Goddesses - Enki/Ea (god)](https://oracc.museum.upenn.edu/amgg/listofdeities/enki/index.html)

## pazuzu_lamashtu_role — 파주주·라마슈투 역할 경계

- 범위: 루브르가 설명한 보호 관계
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택한 파주주 실물 표상; 별도 기록된 라마슈투와 보호 대상
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: pazuzu → protective_opposition_to → lamashtu
- 혼동 경계: 악마 명칭·혼합 몸이 보호 역할을 지우지 않는다; 라마슈투 지물을 파주주 몸에 혼합하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Pazuzu, le roi des démons de l'empire assyrien](https://www.louvre.fr/louvreplus/video-pazuzu-le-roi-des-demons-de-l-empire-assyrien)

## fire_altar_identity — 불의 제단 외형과 종교 정체 한계

- 범위: Iranica의 역사·식별 한계
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 그릇·받침 또는 제단의 형상; 불이 담긴 위치; 시대·소장 출처는 별도 기록
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: flame_if_requested → contained_by → fire_holder
- 혼동 경계: 불을 올린 용기만으로 조로아스터교 제의라고 확정하지 않는다; 향로·난로·노천 불과 의미를 일괄 병합하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [FIRE ALTARS - Encyclopaedia Iranica](https://www.iranicaonline.org/articles/fire-altars/)

## chinvat_narrative — 친바트 다리의 심판 장소

- 범위: 분다히슌 등 문헌의 지리·사후 서사
- 근거 단계: `NARRATIVE_SOURCE_NOT_FIXED_ICONOGRAPHY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 다리와 양쪽 공간의 연결; 선택 각색의 사후 인물; 문헌 근거와 상상된 건축 외형의 분리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: bridge → connects → two_afterlife_regions
- 혼동 경계: 북유럽 비프로스트의 무지개·발할라 요소를 자동 추가하지 않는다; 문헌만으로 단일 길이·재료·수호자 수를 인증하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [ALBORZ ii. In Myth and Legend - Encyclopaedia Iranica](https://www.iranicaonline.org/articles/alborz-myth-legend/)

## siren_human_bird — 고대 사이렌의 인간–새 연결

- 범위: 남이탈리아·시칠리아 테라코타 도상
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 인간 머리 또는 상체; 새의 몸·날개·발; 인간부와 조류부 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: human_head_or_torso → joins → avian_body
- 혼동 경계: 현대 인어의 물고기 꼬리와 고대 사이렌을 동일시하지 않는다; 여성 사자 몸 스핑크스와 몸 소유를 섞지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Catalogue | Ancient Terracottas from South Italy and Sicily](https://www.getty.edu/publications/terracottas/catalogue/2/)

## sphinx_greek — 그리스 스핑크스의 사자 몸

- 범위: 기원전 6세기 말–5세기 초 청동
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 여성 머리 표상; 사자 몸; 날개가 몸에 연결됨
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: human_head → joins → lion_body; wings → attach_to → lion_body
- 혼동 경계: 이집트 스핑크스에 그리스 여성 얼굴·날개를 강제하지 않는다; 사이렌의 새 몸·그리핀의 독수리 머리와 구별한다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Bronze sphinx - Greek - Archaic - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/329999)

## griffin_eagle_lion — 그리핀의 독수리–사자 연결

- 범위: 남이탈리아 9–10세기 기독교 부조 표본
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 독수리 머리와 부리; 독수리 날개; 사자 몸·뒷다리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: eagle_head_and_wings → join → lion_body
- 혼동 경계: 인간 얼굴 스핑크스·날개 달린 말과 구별한다; 동물 혼합 형상이 하나의 종교 정체를 보편적으로 뜻하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Relief Panel with Two Griffins Drinking from a Cup - South Italian - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/467079)

## odin_attributes — 오딘의 한 눈·두 까마귀

- 범위: 스웨덴 역사박물관의 인물 설명
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택 표상에서 한 눈 상태; 서로 구별되는 두 까마귀; 까마귀와 오딘의 동반 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: two_ravens → accompany → odin
- 혼동 경계: 외눈 인물·검은 새만으로 오딘을 확정하지 않는다; 한 눈을 가린 구도에서 잃은 눈의 신체 상태를 추정하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Odin – leader of the gods - Historiska museet](https://historiska.se/en/explore-history/history-hub/odin-leader-of-the-gods/)

## sleipnir_eight_legs — 슬레이프니르 여덟 다리

- 범위: 여덟 다리 말 표상; 그림돌 해석은 맥락
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 같은 말 몸에 연결된 여덟 다리; 각 다리의 관절·발굽; 겹친 두 말과 구별되는 하나의 몸
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: eight_distinct_legs → attach_to → one_horse_body
- 혼동 경계: 숨은 다리를 추정해서 여덟 개 PASS로 세지 않는다; 장례 운반자 해석을 모든 여덟 다리 도상의 사실로 고정하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Odin – leader of the gods - Historiska museet](https://historiska.se/en/explore-history/history-hub/odin-leader-of-the-gods/), [The Viking World — Display: Four scenes in stone](https://dev.vikingar.historiska.se/objects.php?e=no&l=en&showcase=772a155d-bfbc-4107-9ab3-2f61d275d838)

## babayaga_hut — 바바 야가의 닭발 오두막

- 범위: 박물관이 소개한 현대 동화 삽화 전승
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 집 모양 오두막; 닭 다리형 받침; 집과 다리의 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: chicken_legs → support → hut
- 혼동 경계: 닭이 집 앞에 서 있는 것과 구별한다; 이 현대 삽화의 문·울타리를 모든 역사 판본에 고정하지 않는다
- 후보 위치: `location`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Introduction to Goddess | Children’s book celebrating Feminine power | British Museum](https://www.britishmuseum.org/blog/introduction-goddess-childrens-book-celebrating-feminine-power)

## babayaga_mortar — 바바 야가의 절구 이동형

- 범위: 같은 동화 전승의 절구·공이
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 절구 형태 이동 용기; 그 안의 바바 야가; 별도 공이
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: babayaga → rides_in → mortar; pestle → associated_with → rider
- 혼동 경계: 빗자루만 탄 일반 마녀로 대체하지 않는다; 모든 판본에서 공이·빗자루의 정확한 손 배치를 추정하지 않는다
- 후보 위치: `action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Introduction to Goddess | Children’s book celebrating Feminine power | British Museum](https://www.britishmuseum.org/blog/introduction-goddess-childrens-book-celebrating-feminine-power)

## sheela_interpretation — 실라 나 긱의 형태와 기능 보류

- 범위: 보일 수도원 사례; 기능 해석은 복수
- 근거 단계: `FUNCTION_DISPUTED_REFERENCE_IMAGE_REVIEW_REQUIRED`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 건축물의 조각형 인물; 선택 원본의 다리·손 배치; 원본에 있는 신체 노출 표지
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: carved_figure → installed_on → architectural_surface
- 혼동 경계: 노출 외형을 곧 풍요·음란·경고 중 하나로 확정하지 않는다; 벨라우 딜루카이와 공통 기능의 동의어로 병합하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Boyle Cistercian Abbey | Heritage Ireland](https://heritageireland.ie/visit/places-to-visit/boyle-cistercian-abbey//highlights/)

## selkie_skin_change — 셀키의 가죽 변신

- 범위: 스코틀랜드 전승을 해석한 현대 미술 맥락
- 근거 단계: `NARRATIVE_AND_ARTIST_INTERPRETATION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 인간형 또는 물개형의 선택 단계; 벗겨진 물개 가죽; 가죽과 인물의 소유 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: seal_skin → separate_from → human_form
- 혼동 경계: 물고기 꼬리 인어와 같은 몸으로 만들지 않는다; 한 컷에서 변신 전·중·후를 모두 성립했다고 주장하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [‘The Creeping and The Wise’: How the metamorphosis of animals in Scottish folklore and fossils became a recipe for glass | National Museums Scotland Blog](https://blog.nms.ac.uk/2021/10/25/the-creeping-and-the-wise-how-the-metamorphosis-of-animals-in-scottish-folklore-and-fossils-became-a-recipe-for-glass/)

## nkisi_container_scope — 은키시의 물건과 권능 맥락

- 범위: 콩고 19–20세기 물건의 추가물
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택한 목조 형상; 그 형상에 부착된 천·종·비즈 등; 내용물과 외함의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: attachments → added_to → nkisi_object
- 혼동 경계: 모든 은키시에 못을 필수로 추가하지 않는다; 감춰진 약재·권능의 존재를 표면 픽셀로 인증하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Kongo artist and nganga (ritual specialist) - Nkisi (power figure) - Kongo peoples - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/311035)

## mangaaka_nkondi — 망가카 은콘디의 자세·금속

- 범위: 콩고·앙골라 해안 19세기 말 작품
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 앞으로 기울며 손을 허리에 둔 형상; 상체에 박힌 금속; 복부 저장부 흔적과 mpu 머리 장식
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: figure.hands → rest_on → figure.hips; metal_elements → embedded_in → figure.torso; recess → in → figure.abdomen
- 혼동 경계: 일반 저주 인형·실제 사람의 신체 피해로 대체하지 않는다; 모든 금속을 동일 못·새 상처로 통일하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Yombe-Kongo artist and nganga (ritual specialist) - Mangaaka Power Figure (Nkisi N’Kondi) - Kongo peoples - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/320053)

## mami_wata_snake — 마미 와타의 뱀 표본

- 범위: 아낭·이비비오 해당 조각; 다른 지역형과 분리
- 근거 단계: `SEARCH_EXCERPT_BODY_REACCESS_BLOCKED`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 여성형 인물 표상; 인물이 들거나 걸친 뱀; 몸의 하단 형상은 해당 원본으로 확정
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: snake → held_or_draped_by → mami_wata_figure
- 혼동 경계: 물의 신격이라는 말만으로 물고기 꼬리를 추가하지 않는다; 지역·작가·시대가 다른 도상을 하나의 표준형으로 고정하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Mami Wata figure | National Museum of African Art](https://africa.si.edu/collection/object/nmafa_2009-16-1)

## egungun_partial_garment — 에궁군 속의복 표본의 한계

- 범위: Met 소장 속의복 한 점
- 근거 단계: `PARTIAL_OBJECT_CANNOT_ESTABLISH_WHOLE`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 한 벌 속의복의 직물; 그 의복의 경계; 완전한 가면·겉복·공연은 별도 자료
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: undergarment → component_of → possible_masquerade_ensemble
- 혼동 경계: 속의복 하나를 완전한 에궁군 의례복으로 인증하지 않는다; 직물만으로 착용자의 실제 정체·조상을 판정하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Yoruba artist - Masquerade Element: Undergarment (Egungun) - Yoruba peoples - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/315912)

## drapo_material — 드라포의 봉헌 깃발

- 범위: 포울러 전시의 20세기 아이티 제의 깃발
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 직물 바탕; 스팽글·비즈·아플리케 장식; 선택한 루아의 중심 도상과 테두리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: beads_and_sequins → decorate → textile_flag; dedication_record → names → specific_lwa
- 혼동 경계: 바닥 베베와 깃발을 같은 재료·동의어로 처리하지 않는다; 한 깃발의 루아 표지를 다른 신격으로 자동 옮기지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Saluting Vodou Spirits: Haitian Flags from the Fowler Collection | Fowler Museum at UCLA](https://fowler.ucla.edu/exhibitions/saluting-vodou-spirits-haitian-flags-from-the-fowler-collection/)

## gede_distinct_name — 파파 게데 깃발의 명칭 보존

- 범위: 파파 게데 헌정 깃발에 대한 별도 비교 자료
- 근거 단계: `COMPARISON_SOURCE_NOT_REQUESTED_FIGURE_EVIDENCE`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 그 깃발의 헌정 이름; 선정된 도상·문자; 깃발의 제작자·시대 기록
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: dedication → names → papa_gede
- 혼동 경계: 게데 계열을 바롱 사메디 하나로 무조건 병합하지 않는다; 이 자료는 바롱 사메디 고정 도상의 직접 증거가 아니다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Curator’s Choice: A Vodou Drapo for Papa Gede | Fowler Museum at UCLA](https://fowler.ucla.edu/curators-choice-a-vodou-drapo-for-papa-gede/)

## poto_relation — 포토 미탕의 공간 관계

- 범위: 포울러 공개 연구의 제의 중심 기둥 맥락
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택 기록의 중심 기둥; 기둥 주위의 집행 공간; 기둥·제단·깃발을 별도 물건으로 기록
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: ceremonial_space → organized_around → central_post
- 혼동 경계: 중심 기둥이 있는 모든 방을 같은 제의 공간으로 판정하지 않는다; 공개 시각자료를 실제 제의 절차 지시로 바꾸지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Welcome to Vital Matters.](https://vitalmatters.fowler.ucla.edu/perspectives/v0017)

## coatlicue_sculpture — 코아틀리쿠에 뱀·목걸이 조합

- 범위: INAH가 설명한 멕시카 조각
- 근거 단계: `SEARCH_EXCERPT_BODY_REACCESS_BLOCKED`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 뱀으로 구성된 치마; 손·심장·중앙 두개골의 목걸이; 쌍두 뱀 허리 장식
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: serpent_forms → compose → skirt; hands_hearts_and_skull → compose → necklace; serpent_belt → at → waist
- 혼동 경계: 무작위 해골·뱀 여신과 같은 조합으로 축소하지 않는다; 신격 동일성 논쟁·머리 구조의 세부는 원본 재검토까지 별도
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Coatlicue: majestuosidad escultórica mexica](https://www.inah.gob.mx/foto-del-dia/coatlicue-majestuosidad-escultorica-mexica?highlight=WyJjb2F0bGljdWUiXQ%3D%3D)

## ballgame_player — 공놀이 선수의 허리 장비

- 범위: 노필로아 도기 선수 표본
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선수의 몸; 허리 둘레 장비; 몸과 장비의 착용 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: protective_waist_gear → encircles → player.waist
- 혼동 경계: 도기 표현의 장비가 실제 무거운 돌 요크 착용의 증거는 아니다; 축구·농구 장면으로 대체하지 않는다
- 후보 위치: `wearable_accessory`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Ball Player - Nopiloa - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/316267)

## hacha_notch — 아차의 연결 홈

- 범위: 베라크루스 7–9세기 석제품
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 도끼형 얇은 석조 형상; 바닥의 각진 홈; 요크 위에 얹히는 방향 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: hacha.base_notch → fits_over → yoke.top
- 혼동 경계: 현대 도끼라는 이름에서 손잡이·찍기 동작을 추가하지 않는다; 추정 연결 방식·끈 고정을 실물에 확인된 것으로 주장하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Hacha - Veracruz - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/310474)

## ballgame_sacrifice_limit — 공놀이–희생–재생의 인과 한계

- 범위: Met가 설명한 엘 타힌·치첸이트사 부조 사례
- 근거 단계: `HISTORICAL_MECHANISM_UNCERTAIN`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택 희생 장면과 경기 공간; 참수 인물 목에서 이어지는 뱀·식물; 경기 인물과 희생 대상의 역할 분리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: serpents_and_vegetation → emerge_from → decapitated_neck
- 혼동 경계: 경기 패자를 항상 희생했다고 규칙화하지 않는다; 모든 경기 장면에 희생·피를 자동 삽입하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [The Mesoamerican Ballgame - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/the-mesoamerican-ballgame)

## hero_twins_xibalba — 영웅 쌍둥이와 시발바의 문헌 맥락

- 범위: 포폴 부와 경기·저승 서사의 설명
- 근거 단계: `NARRATIVE_SOURCE_NOT_FIXED_ICONOGRAPHY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선택한 두 형제 또는 두 쌍의 사건 단계; 공놀이와 저승의 관계; 실제 인물 수는 해당 대목에 따라 확정
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: named_brothers → play_against → lords_of_xibalba
- 혼동 경계: 모든 장면을 두 사람으로 고정하지 않는다; 그리스 카타바시스나 기독교 지하세계 구조로 자동 교체하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [The Mesoamerican Ballgame - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/the-mesoamerican-ballgame)

## hei_tiki_object — 헤이 티키의 실제 물건 기록

- 범위: Te Papa 1750–1850년 표본
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 목걸이형 인간 표상; 선정 물건의 포우나무 재료·패화 눈
- 비시각적 맥락: 정확한 관절·머리 방향은 물건별 확인
- 소유·관계: carved_figure → forms → pendant; inset_eyes → in → carved_head
- 혼동 경계: 모든 태평양 인물 조각을 tiki 하나로 묶지 않는다; 풍요 기능·연대·진품성을 표면만으로 인증하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Hei tiki (pendant in human form)](https://collections.tepapa.govt.nz/object/56145)

## ngalyod_regional — 서부 아넘랜드 무지개뱀

- 범위: 이리왈라·피터 마랄왕가 등 지역·작가 표본
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선정 작가의 뱀 몸 형상; 그 표본의 복합 동물 부분; 명시된 경우 깃털 머리 장식
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: selected_animal_parts → compose → regional_serpent_form
- 혼동 경계: 이름에 rainbow가 있다고 무지개색 일반 뱀으로 대체하지 않는다; 다른 원주민 지역·클랜의 문양 권한과 표상을 하나로 합치지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Western Arnhem Land | National Museum of Australia](https://www.nma.gov.au/exhibitions/old-masters/western-arnhem-land)

## barong_rangda_balance — 바롱·랑다의 인물·가면·역할

- 범위: 박물관 전시 안내의 발리 설명
- 근거 단계: `REFERENCE_IMAGE_REVIEW_REQUIRED`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 서로 구별되는 두 가면형; 가면·의복·착용자 연결; 선택 공연의 상대 위치
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: performer → wears → named_mask; barong_form → contrasts_with → rangda_form
- 혼동 경계: 두 도상의 균형 맥락을 단순 악역 제거로 변형하지 않는다; 의례 가면을 실제 배우자의 생물학적 얼굴로 흡수하지 않는다
- 후보 위치: `costume_style`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Feminine power the divine to the demonic – large prints guide](https://www.britishmuseum.org/sites/default/files/2022-05/feminine_power_exhibition_large_print_guide.pdf)

## dilukai_gable — 벨라우 딜루카이의 건축 설치

- 범위: 벨라우 19세기 말–20세기 초 gable figure
- 근거 단계: `REFERENCE_IMAGE_REVIEW_REQUIRED`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 목조 여성형 도상; 선정 실물의 자세·노출; 남성 집 출입구 위 박공 설치
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: dilukai_figure → installed_above → mens_house_entrance
- 혼동 경계: 실라 나 긱과 동일한 기능·기원으로 합치지 않는다; 박물관의 전승 설명과 살아 있는 사람의 성적 성향을 혼동하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Belauan artist - Dilukai (gable figure) - Belauan peoples - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/310454)

## coniunctio_scope — 콘융크티오의 합일 도상

- 범위: 쿠스토스 1633년 해당 판화
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선정 판화의 합일 도상; 동일 판화 안 상징·문자 구역; 물질 변환과 인물 사건의 해석 분리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: emblem_record → represents → alchemical_conjunction
- 혼동 경계: 곧바로 성교·결혼·탄트라 합일로 동의어 처리하지 않는다; 시대·저작이 다른 상징을 하나의 실험 레시피로 섞지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [The Art of Alchemy | Getty Research Institute | The Getty Research Institute](https://www.getty.edu/research/exhibitions_events/exhibitions/alchemy/)

## rebis_two_heads — 레비스의 두 머리·날개형

- 범위: Lux Lucens in tenebris 1584 도판
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 연결된 한 몸에 두 머리; 선택 도판의 날개; 각 손의 거울·돌 표지
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: two_heads → attach_to → shared_body; wings → attach_to → shared_body
- 혼동 경계: 한 머리 반신 아르다나리슈바라와 다르다; 다른 레비스 도판의 도구·다리 수를 이 표본에 합치지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [The Afterlife of Alchemy in the Warburg Institute Library’s Collection - History Collections](https://historycollections.blogs.sas.ac.uk/2025/10/22/warburg-afterlife-of-alchemy/)

## rebis_three_legs — 합성체의 세 다리 변형

- 범위: Zentralbibliothek 172, fol. VD 2, 15세기 도판
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 각기 머리·상체를 가진 두 인물부; 골반에서 합쳐진 몸; 공유된 세 다리와 뒤쪽 불사조
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: two_torsos → join_at → hips; three_legs → support → joined_form; phoenix → behind → joined_form
- 혼동 경계: 레비스 일반형을 한 몸 두 머리 두 다리로만 고정하지 않는다; 세 번째 다리가 가려지면 성공으로 추정하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [The Afterlife of Alchemy in the Warburg Institute Library’s Collection - History Collections](https://historycollections.blogs.sas.ac.uk/2025/10/22/warburg-afterlife-of-alchemy/)

## volvelle_layers — 볼벨의 회전 층 구조

- 범위: 힐레·투르나이서 1574–75년 표본
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 한 중심축에 겹친 원판; 층마다 별도 가장자리; 회전 가능한 부재와 고정 바탕의 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: movable_discs → pivot_around → common_axis
- 혼동 경계: 정적 동심원 그림을 볼벨로 판정하지 않는다; 한 정지 사진에서 실제 회전 작동을 확인했다고 하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [The Art of Alchemy | Getty Research Institute | The Getty Research Institute](https://www.getty.edu/research/exhibitions_events/exhibitions/alchemy/)

## ripley_static_wheel — 리플리 정적 바퀴 도표

- 범위: 1652년 인쇄 도판
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 인쇄면의 동심 구역; 도표 문자·행성 구역; 회전 부재 없는 단일 면
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: concentric_bands → printed_on → single_sheet
- 혼동 경계: wheel이라는 이름이 물리적 회전 도구를 뜻하지 않는다; 볼벨의 회전판·피벗을 자동 추가하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Here followeth the Figure conteyning containing all the secrets of the Treatise both great & small - Science History Institute Digital Collections](https://digital.sciencehistory.org/works/0c483k14n)

## baphomet_levi_scope — 레비 바포메트의 역사적 범위

- 범위: 레비 1854 최초 도상·1855–56 합본 속표지; Strube 2016
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 선정 레비 도상의 염소형 머리; 인간형 몸과 도상 속 상반 표지
- 비시각적 맥락: 특정 도판의 제스처·문자는 원본 단위로 확인
- 소유·관계: goat_head → joins → selected_humanlike_emblem_body
- 혼동 경계: 염소 머리 역오각별·현대 바포메트 동상과 같은 도상으로 병합하지 않는다; 최초 등장 연도를 1856 하나로 단정하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Julian Strube, The Baphomet of Eliphas Lévi: Its Meaning and Historical Context (2016)](https://publikationen.uni-tuebingen.de/xmlui/bitstream/10900/141891/1/Strube_019.pdf)

## alchemy_process_context — 연금술의 실험실·색 단계 맥락

- 범위: 전시 수준의 자료; 개별 용기·니그레도 등 별도 표본 필요
- 근거 단계: `CONTEXT_ONLY_REQUIRES_OBJECT_LEVEL_SOURCES`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 실험 도구·도식·상징 판화는 별도 매체; 검정·흰색·적색은 요청된 변환 단계와 묶어 기록; 특정 용기 형상·해체 인물은 출처 보강 전 보류
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: process_stage_record → scopes → selected_emblem_or_apparatus
- 혼동 경계: 검은 화면을 니그레도·붉은 화면을 루베도로 자동 판정하지 않는다; 연금술을 모두 유럽 중세 실험실이나 하나의 마법 효능으로 고정하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [The Art of Alchemy | Getty Research Institute | The Getty Research Institute](https://www.getty.edu/research/exhibitions_events/exhibitions/alchemy/)

## anasyrma_lifting — 아나시르마의 옷 올리기 관계

- 범위: Met Journal 실물 연구의 치마 올림 모티프
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 입은 치마의 경계; 손이 치마를 잡고 올림; 옷의 움직임과 요청된 신체 노출 범위
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: figure.hands → lift → figure.skirt
- 혼동 경계: 금욕적 나체·옷 없는 인물·실라 나 긱과 같은 행위가 아니다; 외형만으로 벽사·출산·음란 해석 하나를 확정하지 않는다
- 후보 위치: `action`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Metropolitan Museum Journal 50 (2015): anasyrma 관련 논의](https://resources.metmuseum.org/resources/metpublications/pdf/Metropolitan_Museum_Journal_v_50_2015.pdf)

## danae_gold — 다나에의 황금비 서사

- 범위: 티치아노 프라도 1565년 설명
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 다나에 인물; 위에서 내려오는 황금비 표상; 선택 그림의 침상·동반자 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: golden_shower → descends_toward → danae
- 혼동 경계: 금색 조명·황금 드레스만으로 황금비 사건을 대체하지 않는다; 인물의 실제 동의·욕망을 시각 표정에서 인증하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Danaë and the Shower of Gold. Titian - Easy-to-read artwork - Museo Nacional del Prado](https://www.museodelprado.es/en/easy-to-read/danae-and-the-shower-of-gold-titian/8731a7a3-5fcb-fff3-73d2-bf885d0d22e6)

## leda_swan — 레다와 백조의 서사 변형

- 범위: NG151.1와 해당 신화의 복수 판본
- 근거 단계: `NARRATIVE_VARIANTS_REQUIRE_OBJECT_REVIEW`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 레다와 별도 백조; 선택 판본의 접촉 위치; 그림 매체·시대형
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: leda → interacts_with → separate_swan
- 혼동 경계: 단순 백조 인물 사진이 이름 없이 이 신화를 자동 활성화하지 않는다; 서사 판본의 관계·강제를 낭만이나 동의로 임의 번역하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Style of Pier Francesco Mola | Leda and the Swan | NG151.1 | National Gallery, London](https://www.nationalgallery.org.uk/paintings/style-of-pier-francesco-mola-leda-and-the-swan)

## persephone_abduction — 페르세포네 납치의 사건 경계

- 범위: Getty CONA의 명시적 납치 서사
- 근거 단계: `NARRATIVE_SOURCE_NOT_FIXED_ICONOGRAPHY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 명시된 데려가는 주체와 대상; 요청한 이동·억류 관계; 저승·계절 해석은 별도 맥락
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: hades → abducts → persephone
- 혼동 경계: 납치 사건을 자발적 연애·결혼 포즈로 바꾸지 않는다; 모든 하데스·페르세포네 동반 장면이 납치 단계는 아니다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Getty CONA 901000646: Abduction of Persephone](https://www.getty.edu/cona/CONAIconographyRecord.aspx?iconid=901000646)

## ganesha_chola — 촐라 가네샤의 네 손

- 범위: 타밀나두 12세기 해당 청동
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 코끼리 머리와 인간형 몸 연결; 위 왼손 밧줄·위 오른손 도끼; 아래 왼손 과자·아래 오른손 부러진 상아
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: elephant_head → joins → humanlike_body; upper_left_hand → holds → lasso; upper_right_hand → holds → axe; lower_left_hand → holds → sweet; lower_right_hand → holds → tusk
- 혼동 경계: 일반 코끼리와 코끼리 가면 인물과 구별한다; 이 표본의 네 팔·지물을 모든 가네샤에 고정하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Ganesha - India, Tamil Nadu - Chola period - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/37397)

## naga_seven_hood — 일곱 머리 나가가 받치는 불상

- 범위: 캄보디아 12세기 말–13세기 초 단편
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 뱀의 몸이 만든 감긴 좌대; 남아 있는 중앙 불상 표상; 머리 위로 펼쳐진 일곱 후드
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: snake_coils → support → central_buddha_form; seven_headed_hood → above → central_buddha_form
- 혼동 경계: 나가라는 일반 이름에 항상 일곱 머리를 강제하지 않는다; 단편의 보이지 않는 신체를 원본에서 관찰한 것으로 추정하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Buddha Protected by a Seven-headed Naga - Cambodia - Angkor period - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/38451)

## naga_handle_five — 다섯 나가로 구성된 의례 손잡이

- 범위: 네팔 13세기 투각 손잡이
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 다섯 나가의 얽힌 몸; 인간 상체와 뱀 후드; 늘어진 뱀 몸이 이루는 손잡이 윤곽
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: five_naga_forms → intertwine_to_form → ritual_vessel_handle; human_torsos → join → extended_snake_bodies
- 혼동 경계: 다섯 머리 한 뱀과 다섯 인물 합성을 혼동하지 않는다; 손잡이 실물을 실제 다섯 사람 장면으로 자동 바꾸지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Handle with Intertwined Figures - Nepal (Kathmandu Valley) - early Malla period - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/39389)

## centaur_rimmer_form — 리머 켄타우로스의 몸 연결

- 범위: 1869년 모델·1905년 주조 조각
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 인간 머리·상체; 말 하체; 쓰러졌다가 일어나려는 선택 자세와 잘린 조각 팔
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: human_torso → joins → horse_lower_body
- 혼동 경계: 원본 조각의 팔 단절을 실제 인물의 새 부상 사건으로 확대하지 않는다; 모든 초기 켄타우로스에 이 연결 구조를 강제하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [William Rimmer - The Dying Centaur - American - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/11915)

## centaur_nessos_human_knees — 네소스의 사람 무릎형

- 범위: 기원전 7세기 2사분기 암포라
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 사람 무릎으로 꿇은 켄타우로스; 앞으로 뻗은 인간 손; 뒤로 이어지는 말 몸
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: nessos.human_knees → kneel_on → ground; horse_body → extends_behind → human_front_form
- 혼동 경계: 현대 네 말다리형으로 초기 사람 다리를 교체하지 않는다; 이 설명만으로 총 다리 수를 여섯 개로 추정하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Attributed to the New York Nessos Painter - Terracotta neck-amphora (storage jar) - Greek, Attic - Proto-Attic - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/248578)

## centaur_pholos_horse_chest — 폴로스의 말 가슴–사람 다리형

- 범위: 기원전 490년경 레키토스
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 말 가슴과 몸; 말 몸에 직접 이어지는 인간 다리; 일반형에서 기대되는 인간 복부의 부재
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: human_legs → attach_directly_to → equine_body
- 혼동 경계: 켄타우로스가 항상 인간 복부와 말 네 다리라는 정의를 강제하지 않는다; 구도 가림과 자료가 설명한 복부 부재를 구분한다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Attributed to the Class of Athens 581.1 - Terracotta lekythos (oil flask) - Greek, Attic - Archaic - The Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/248101)

## minotaur_bull_head — 황소 머리·인간 몸 미노타우로스

- 범위: BM 1850,0302.3 킬릭스의 가려진 형상
- 근거 단계: `SEARCH_EXCERPT_BODY_REACCESS_BLOCKED`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 황소 머리; 보이는 인간 팔·상체; 건물 뒤에 가려진 하반신
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: bull_head → joins → human_upper_body; lower_body → occluded_by → building
- 혼동 경계: 말 몸 켄타우로스나 황소 몸 라마수와 구별한다; 가려진 하반신의 발 수·자세를 원본에서 본 것으로 추정하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [kylix | British Museum](https://www.britishmuseum.org/collection/object/G_1850-0302-3)

## chimera_topology — 키마이라의 세 동물 연결

- 범위: Getty 정의·아레초 표본 맥락
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 사자 몸과 앞쪽 머리; 등 가운데 별도 염소 머리; 뱀 머리로 끝나는 꼬리
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: goat_head → emerges_from → lion_back; snake_head → terminates → tail
- 혼동 경계: 사자·염소·뱀 세 동물을 옆에 놓기만 해서는 합성체가 아니다; 모든 현대 chimera를 이 고전 신화 도상으로 활성화하지 않는다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Getty CONA 901000661: Chimera](https://www.getty.edu/cona/CONAIconographyRecord.aspx?iconid=901000661), [The Chimaera of Arezzo (Getty Villa Exhibitions)](https://www.getty.edu/art/exhibitions/chimaera/english.html)

## cerberus_two_heads — 케르베로스 두 머리형

- 범위: CVA의 두 머리 기술; 도판·소장번호 대조 전 보류
- 근거 단계: `CURATORIAL_EXCERPT_OBJECT_PLATE_PENDING`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 같은 개 몸에 두 머리; 각 머리 위에 자라는 별도 뱀 표지
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: two_dog_heads → attach_to → one_dog_body; snake_markers → grow_from → each_head_top
- 혼동 경계: 세 머리 일반 설명을 이 두 머리형에 강제하지 않는다; 상태가 가려져 두 머리만 보이는 세 머리형과 구별한다
- 후보 위치: `anatomical_connection`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Metropolitan Museum: Attic Black-Figured Neck-Amphorae, CVA Fascicule 4](https://resources.metmuseum.org/resources/metpublications/pdf/Attic_Black_Figured_Neck_Amphorae_Corpus_Vasorum_Antiquorum_Fascicule_4.pdf)

## thor_hammer_ring — 고리에 끼운 토르 망치형

- 범위: 멜라렌 계곡의 철제 망치 고리
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 큰 철 고리; 고리에 끼워진 작은 망치 표상; 고리와 작은 지물의 관통·걸림 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: small_hammer_forms → threaded_onto → larger_iron_ring
- 혼동 경계: 현대 거대 전투 망치로 대체하지 않는다; 망치형 목걸이에서 착용자의 실제 신앙을 인증하지 않는다
- 후보 위치: `prop`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Thor's hammer rings - Historiska museet](https://historiska.se/en/explore-history/history-hub/thors-hammer-rings/)

## hera_polos — 헤라의 높은 폴로스 관

- 범위: 기관이 설명한 고대 그리스 흔한 표지
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 높은 관 형태; 관과 머리의 착용 연결
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: polos_crown → worn_on → hera.head
- 혼동 경계: 르네상스 유노의 공작을 모든 고대 헤라에 필수로 붙이지 않는다; 높은 관만으로 실제 사람 정체를 확정하지 않는다
- 후보 위치: `wearable_accessory`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Greek Gods and Religious Practices - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/greek-gods-and-religious-practices)

## athena_aegis — 아테나의 아이기스·갑옷

- 범위: 고대 그리스 기관 설명; 표본별 세부 확인 필요
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 투구·갑옷; 뱀 모양 가장자리를 가진 아이기스; 별도 창
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: snaky_fringe → bounds → aegis; helmet → worn_on → athena.head; spear → owned_by → athena
- 혼동 경계: 뱀 가장자리를 몸에 붙은 실제 뱀·머리카락으로 흡수하지 않는다; 투구·창이 배경에만 있는 것으로 인물 지물 관계가 충족되지 않는다
- 후보 위치: `costume_style`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Greek Gods and Religious Practices - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/greek-gods-and-religious-practices)

## apollo_kithara — 아폴론의 키타라 지물

- 범위: 고대 그리스 흔한 키타라형
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 지정한 신격과 별도 키타라; 악기의 소유·보유 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: apollo → holds_or_accompanies → kithara
- 혼동 경계: 키타라·일반 리라·현대 기타의 악기 구조를 같게 처리하지 않는다; 지물만 요청한 장면에 새 연주 사건을 자동 추가하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Greek Gods and Religious Practices - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/greek-gods-and-religious-practices)

## artemis_bow_quiver — 아르테미스의 활·화살통

- 범위: 고대 그리스 사냥 여신 지물 범주
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 활의 굽은 몸과 시위; 별도 화살통; 인물과 두 물건의 보유 관계
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: artemis → carries → bow; artemis → carries → quiver
- 혼동 경계: 화살통을 창·금강저로 바꾸지 않는다; 지물 요청에서 사냥 대상·새 공격 행위를 자동 생성하지 않는다
- 후보 위치: `composition`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Greek Gods and Religious Practices - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/greek-gods-and-religious-practices)

## hermes_staff_winged_sandals — 헤르메스의 전령장과 날개 신발

- 범위: 고대 그리스 기관 설명의 전령 신격
- 근거 단계: `CURATORIAL_DESCRIPTION`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 별도 전령장 케뤼케이온; 샌들에 붙은 날개 표지; 발·신발·지팡이의 소유 구별
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: wing_markers → attach_to → sandals; hermes → owns → herald_staff
- 혼동 경계: 신발 날개를 등 날개나 생물학적 발의 날개로 교체하지 않는다; 전령장과 현대 의료용 막대 기호를 임의 동의어로 묶지 않는다
- 후보 위치: `wearable_accessory`; 운영 번역·소유권 검토 전 채택 보류.
- 출처: [Greek Gods and Religious Practices - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/greek-gods-and-religious-practices)

## greek_deity_context — 그리스 신격의 기능·속성물 맥락

- 범위: 제우스·포세이돈·데메테르·디오니소스의 역할 기록
- 근거 단계: `CONTEXT_ONLY`; 직접 원본 도판 대조 미실행.
- 관찰 요소: 특정 신격의 요청된 이름과 시대; 선정 실물에서 확인된 지물만 따로 보강
- 비시각적 맥락: 정체·효능·해석은 픽셀 판정에서 분리한다.
- 소유·관계: selected_deity_record → scopes → attribute_research
- 혼동 경계: 하늘·바다·농업·술이라는 역할만으로 모든 지물을 완성했다고 하지 않는다; 로마 이름·후대 회화 변형을 원형과 무조건 같은 시각 슬롯으로 병합하지 않는다
- 후보 위치: `context_only`; 맥락만, 후보 없음.
- 출처: [Greek Gods and Religious Practices - The Metropolitan Museum of Art](https://www.metmuseum.org/essays/greek-gods-and-religious-practices)

