# 171개 용어의 반영 판단표

기준본: `900848816f88a494e5bf16ea475a25074d584911`. 현재 운영 데이터에 적용된 목록이 아닙니다.

| ID | 원 용어 | 선택한 해석 | 슬롯 제안 | 우선순위 | 판단 / 상태 |
|---|---|---|---|---|---|
| H01 | 아호게／アホ毛／Ahoge | single ahoge tuft | `hair_style` | P0 | atom / ATOM_REVIEW |
| H02 | 안테나 헤어／촉각 머리 | paired antenna-like hair tufts | `hair_style` | P0 | atom / ATOM_REVIEW |
| H03 | 히메컷／姫カット | structural hime cut | `hair_style` | P0 | reuse / EXISTING_OWNER_REVIEW |
| H04 | 트윈테일 | bilateral twin-tail gather | `hair_style` | P0 | reuse / EXISTING_OWNER_REVIEW |
| H05 | 트윈 드릴 | bilateral tapered spiral hair | `hair_style` | P0 | atom / ATOM_REVIEW |
| H06 | 포니드릴 | single pony-drill gather | `hair_style` | P0 | atom / ATOM_REVIEW |
| H07 | 오당고／더블 번 | paired hair buns | `hair_style` | P1 | atom / ATOM_REVIEW |
| H08 | 번＋롱테일 조합 | bun with descending tail | `hair_style` | P1 | atom / ATOM_REVIEW |
| H09 | 사이드 포니테일 | unilateral side ponytail | `hair_style` | P1 | atom / ATOM_REVIEW |
| H10 | 크라운 브레이드 | crown braid path | `hair_style` | P1 | atom / ATOM_REVIEW |
| H11 | 땋은 양갈래 | bilateral braided tails | `hair_style` | P1 | atom / ATOM_REVIEW |
| H12 | 보브／블런트 보브 | blunt bob perimeter | `hair_style` | P1 | split / ATOM_REVIEW |
| H13 | 한쪽 눈 가림 앞머리／Peek-a-boo hair | one-eye hair occlusion | `hair_style` | P0 | atom / ATOM_REVIEW |
| H14 | 양눈 가림 앞머리／메카쿠레 계열 | two-eye fringe occlusion | `hair_style` | P0 | atom / ATOM_REVIEW |
| H15 | 울프컷·샤기 계열 | layered wolf-cut interpretation | `hair_style` | P1 | split / ATOM_REVIEW |
| H16 | 언더컷 | undercut length discontinuity | `hair_style` | P1 | reuse / EXISTING_OWNER_REVIEW |
| H17 | 폼파두르／리젠트형 전면 볼륨 | raised swept-back front volume | `hair_style` | P2 | split / ATOM_REVIEW |
| H18 | 리버티 스파이크 | radial liberty spikes | `hair_style` | P1 | atom / ATOM_REVIEW |
| H19 | 스플릿 컬러／좌우 분할 염색 | left-right split hair color | `hair_color` | P0 | atom / ATOM_REVIEW |
| H20 | 이너 컬러 | inner-layer hair color | `hair_color` | P1 | atom / ATOM_REVIEW |
| H21 | 그라데이션 헤어 | root-to-tip hair color gradient | `hair_color` | P1 | atom / ATOM_REVIEW |
| F01 | 츠리메／吊り目 | upturned outer eye corners | `face_shape_relation` | P0 | atom / ATOM_REVIEW |
| F02 | 타레메／垂れ目 | downturned outer eye corners | `face_shape_relation` | P0 | atom / ATOM_REVIEW |
| F03 | 지토메／반쯤 감긴 응시 | half-lidded gaze configuration | `expression` | P0 | reuse / EXISTING_OWNER_REVIEW |
| F04 | 삼백안 | lower scleral exposure | `eye_detail` | P0 | atom / ATOM_REVIEW |
| F05 | 오드아이／이색 홍채 | heterochromic iris color placement | `eye_detail` | P0 | split / ATOM_REVIEW |
| F06 | 세로 동공／슬릿 동공 | vertical slit pupil | `eye_detail` | P0 | atom / ATOM_REVIEW |
| F07 | 동심원 홍채 | concentric iris rings | `eye_detail` | P1 | atom / ATOM_REVIEW |
| F08 | 별 모양 눈 | star-shaped eye motif | `eye_detail` | P0 | split / ATOM_REVIEW |
| F09 | 하트형 동공 | heart-shaped pupil | `eye_detail` | P0 | atom / ATOM_REVIEW |
| F10 | 검은 공막 | black scleral region | `eye_detail` | P1 | atom / ATOM_REVIEW |
| F11 | 하이라이트 없는 눈 | no illustrated eye highlight | `eye_detail` | P1 | medium_guard / MEDIUM_CONDITIONAL_REVIEW |
| F12 | 긴 아래 속눈썹 | long lower eyelashes | `lash_style` | P1 | atom / ATOM_REVIEW |
| F13 | 야에바／돌출 송곳니 표현 | yaeba tooth displacement | `face_shape_relation` | P0 | split / ATOM_REVIEW |
| F14 | 상어 이빨형 | repeated triangular tooth row | `face_shape_relation` | P0 | atom / ATOM_REVIEW |
| F15 | 고양이 입／ω형 입 | omega-like illustrated mouth | `expression` | P2 | medium_guard / MEDIUM_CONDITIONAL_REVIEW |
| F16 | 주근깨 | scattered freckles | `body_marking` | P1 | reuse / EXISTING_OWNER_REVIEW |
| F17 | 눈물점·입가 점 | localized facial beauty mark | `body_marking` | P1 | reuse / EXISTING_OWNER_REVIEW |
| F18 | 얼굴 분할 색면 | split facial color fields | `body_marking` | P0 | atom / ATOM_REVIEW |
| F19 | 얼굴 문양／페이셜 마킹 | localized facial markings | `body_marking` | P1 | reuse / EXISTING_OWNER_REVIEW |
| F20 | 눈가 흉터 | scar crossing an eye region | `body_marking` | P1 | reuse / EXISTING_OWNER_REVIEW |
| B01 | 슬렌더형 | slender overall frame | `silhouette_proportion` | P1 | reuse / EXISTING_OWNER_REVIEW |
| B02 | 장신·장지형 | tall elongated-limb proportions | `silhouette_proportion` | P1 | split / ATOM_REVIEW |
| B03 | 긴 다리형 | long-leg torso ratio | `silhouette_proportion` | P0 | reuse / EXISTING_OWNER_REVIEW |
| B04 | 긴 몸통형 | long-torso leg ratio | `silhouette_proportion` | P1 | reuse / EXISTING_OWNER_REVIEW |
| B05 | 다부진 체형／Stocky | stocky frame | `silhouette_proportion` | P0 | reuse / EXISTING_OWNER_REVIEW |
| B06 | 역삼각형 체형 | inverted-triangle breadth ratio | `silhouette_proportion` | P0 | reuse / EXISTING_OWNER_REVIEW |
| B07 | 벌크형 근육질 | high muscle volume | `silhouette_proportion` | P1 | reuse / EXISTING_OWNER_REVIEW |
| B08 | 마른 근육형／Lean athletic | lean athletic morphology | `silhouette_proportion` | P1 | split / ATOM_REVIEW |
| B09 | 모래시계형 | hourglass breadth relation | `silhouette_proportion` | P0 | reuse / EXISTING_OWNER_REVIEW |
| B10 | 하체 중심형／Pear-shaped | lower-body dominant breadth | `silhouette_proportion` | P1 | reuse / EXISTING_OWNER_REVIEW |
| B11 | 풍성한 체적／Full-figured | region-specific full volume | `silhouette_proportion` | P0 | split / ATOM_REVIEW |
| B12 | 중성적 실루엣 | androgynous silhouette interpretation | `silhouette_proportion` | P2 | label_only / HOLD_LABEL_ONLY |
| B13 | 초과장 손발 비율 | oversized extremity proportions | `silhouette_proportion` | P1 | split / ATOM_REVIEW |
| B14 | 치비／SD 비율 | chibi head-body proportion | `silhouette_proportion` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| N01 | 케모미미／獣耳 | animal-ear anatomical interpretation | `anatomical_connection` | P0 | split / ATOM_REVIEW |
| N02 | 네코미미／고양이 귀 | triangular feline-like ears | `anatomical_connection` | P0 | split / ATOM_REVIEW |
| N03 | 늘어진 개 귀 | pendent canine-like ears | `anatomical_connection` | P1 | split / ATOM_REVIEW |
| N04 | 여우 귀형 | elongated pointed fox-like ears | `anatomical_connection` | P1 | split / ATOM_REVIEW |
| N05 | 토끼 귀형 | elongated rabbit-like ears | `anatomical_connection` | P0 | split / ATOM_REVIEW |
| N06 | 엘프 귀형 | pointed lateral elf-like ears | `anatomical_connection` | P1 | atom / ATOM_REVIEW |
| N07 | 수인／Anthropomorphic animal | anthropomorphic animal configuration | `species_marker` | P1 | cross_dimension / HOLD_CROSS_DIMENSION |
| N08 | 지행형 다리／Digitigrade | digitigrade support geometry | `anatomical_connection` | P0 | atom / ATOM_REVIEW |
| N09 | 단순 원뿔형 뿔 | unbranched conical horns | `anatomical_connection` | P0 | split / ATOM_REVIEW |
| N10 | 양·염소형 말린 뿔 | curled horn path | `anatomical_connection` | P1 | split / ATOM_REVIEW |
| N11 | 사슴형 가지뿔 | branched antler topology | `anatomical_connection` | P0 | split / ATOM_REVIEW |
| N12 | 다중 꼬리 | multiple tail roots and count | `anatomical_connection` | P0 | atom / ATOM_REVIEW |
| N13 | 깃털 날개 | feathered wing structure | `anatomical_connection` | P1 | split / ATOM_REVIEW |
| N14 | 박쥐형 막날개 | membranous supported wings | `anatomical_connection` | P1 | split / ATOM_REVIEW |
| N15 | 곤충형 날개 | insect-like wing panels | `anatomical_connection` | P1 | split / ATOM_REVIEW |
| N16 | 하피형 | wing-arm harpy configuration | `anatomical_connection` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| N17 | 라미아형 | human-torso serpentine lower body | `anatomical_connection` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| N18 | 켄타우로스형 | human-torso quadruped transition | `anatomical_connection` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| N19 | 아라크네형 | human-torso arachnid transition | `anatomical_connection` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| N20 | 슬라임형 | deformable slime-body interpretation | `surface_material` | P2 | cross_dimension / HOLD_CROSS_DIMENSION |
| N21 | 수정·광물형 신체 | faceted crystalline body interpretation | `surface_material` | P1 | cross_dimension / HOLD_CROSS_DIMENSION |
| N22 | 구체관절 인형형 | ball-and-socket doll joints | `anatomical_connection` | P0 | atom / ATOM_REVIEW |
| N23 | 사이보그형 | cyborg integrated segment interface | `anatomical_connection` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| N24 | 다완형 | multiple upper-limb roots | `anatomical_connection` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| N25 | 제3의 눈 | third-eye organ placement | `anatomical_connection` | P0 | split / ATOM_REVIEW |
| N26 | 촉수형 부속지 | rooted tentacular appendages | `anatomical_connection` | P0 | split / ATOM_REVIEW |
| C01 | 메이드복 | selected maid garment configuration | `costume_style` | P1 | recipe / CONTEXT_RECIPE_REVIEW |
| C02 | 변형 무녀복 | selected detached-sleeve shrine-inspired outfit | `costume_style` | P0 | recipe / CONTEXT_RECIPE_REVIEW |
| C03 | 마녀복 | selected witch garment configuration | `costume_style` | P1 | recipe / CONTEXT_RECIPE_REVIEW |
| C04 | 마법소녀형 전투복 | selected magical-warrior garment configuration | `costume_style` | P2 | recipe / CONTEXT_RECIPE_REVIEW |
| C05 | 고딕 로리타 | selected Gothic Lolita configuration | `costume_style` | P1 | recipe / CONTEXT_RECIPE_REVIEW |
| C06 | 스위트 로리타 | selected Sweet Lolita configuration | `costume_style` | P1 | recipe / CONTEXT_RECIPE_REVIEW |
| C07 | 클래식 로리타 | selected Classic Lolita configuration | `costume_style` | P1 | recipe / CONTEXT_RECIPE_REVIEW |
| C08 | 오우지／왕자풍 복식 | selected ouji trouser configuration | `costume_style` | P2 | recipe / CONTEXT_RECIPE_REVIEW |
| C09 | 와 로리타／기모노 혼합형 | selected kimono-influenced Lolita configuration | `costume_style` | P2 | recipe / CONTEXT_RECIPE_REVIEW |
| C10 | 차이나드레스·치파오형 | selected qipao garment construction | `costume_style` | P1 | recipe / CONTEXT_RECIPE_REVIEW |
| C11 | 세일러복형 | selected sailor-collar garment | `costume_style` | P1 | recipe / CONTEXT_RECIPE_REVIEW |
| C12 | 군복·의장복형 | selected military-inspired garment | `costume_style` | P0 | recipe / CONTEXT_RECIPE_REVIEW |
| C13 | 전투수녀형 | selected armored religious-inspired garment | `costume_style` | P2 | recipe / CONTEXT_RECIPE_REVIEW |
| C14 | 쿠노이치·닌자형 | selected ninja-inspired garment | `costume_style` | P1 | recipe / CONTEXT_RECIPE_REVIEW |
| C15 | 메카무스메／메카 의인화 | human with attached mechanical equipment | `costume_style` | P0 | split / ATOM_REVIEW |
| C16 | 전술·테크웨어형 | selected technical garment construction | `wardrobe_style` | P1 | recipe / CONTEXT_RECIPE_REVIEW |
| C17 | 스팀펑크형 | selected steampunk hardware layering | `costume_style` | P2 | recipe / CONTEXT_RECIPE_REVIEW |
| C18 | 광대·제스터형 | selected jester garment configuration | `costume_style` | P2 | recipe / CONTEXT_RECIPE_REVIEW |
| C19 | 발키리형 갑주 | selected fantasy armor configuration | `costume_style` | P2 | recipe / CONTEXT_RECIPE_REVIEW |
| G01 | 분리 소매／Detached sleeves | detached sleeve gap | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| G02 | 벨 슬리브 | bell sleeve flare | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G03 | 퍼프 슬리브 | puffed sleeve volume | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G04 | 모에소데／손을 덮는 긴 소매 | hand-covering sleeve length | `garment_detail` | P0 | atom / ATOM_REVIEW |
| G05 | 러프 칼라 | radial pleated ruff collar | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G06 | 프릴·러플 | frill and ruffle construction | `garment_detail` | P1 | split / ATOM_REVIEW |
| G07 | 플리츠 | repeated garment pleats | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G08 | 페티코트／코스튬용 패니에 | cosplay petticoat skirt support | `garment_detail` | P0 | split / ATOM_REVIEW |
| G09 | 비대칭 밑단 | asymmetrical garment hem | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G10 | 테일코트형 뒤꼬리 | paired rear coat tails | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G11 | 케이플릿 | short shoulder capelet | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G12 | 타바드형 겉천 | tabard panel layering | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G13 | 오페라 글러브 | long opera gloves | `wearable_accessory` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G14 | 건틀릿 | armored hand gauntlet | `wearable_accessory` | P0 | split / ATOM_REVIEW |
| G15 | 폴드런／어깨 장갑 | shoulder armor attachment | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G16 | 그리브／정강이 장갑 | shin armor coverage | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G17 | 견장／에폴레트 | epaulette shoulder placement | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| G18 | 레이스업 | lace-up eyelet crossing | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| G19 | 벨트 과다 배치형 | multiple garment belt paths | `garment_detail` | P1 | atom / ATOM_REVIEW |
| G20 | 색상 파이핑 | contrasting edge piping | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| G21 | 라텍스 표면 | selected latex-sheet surface behavior | `surface_material` | P0 | split / ATOM_REVIEW |
| G22 | 에나멜·코팅 표면 | selected coated garment finish | `surface_material` | P0 | split / ATOM_REVIEW |
| G23 | 시스루·반투명 원단 | translucent fabric layer relation | `surface_material` | P0 | reuse / EXISTING_OWNER_REVIEW |
| G24 | 망사／Fishnet | open-net fishnet lattice | `surface_material` | P0 | reuse / EXISTING_OWNER_REVIEW |
| G25 | 털·깃털 트림 | fur versus feather edge trim | `garment_detail` | P1 | split / ATOM_REVIEW |
| A01 | 풍만한 가슴／Large bust | large adult bust volume | `silhouette_proportion` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A02 | 평평한 흉부／Small or flat bust | small versus flat adult bust | `silhouette_proportion` | P0 | split / ATOM_REVIEW |
| A03 | 과장된 흉부 비율 | exaggerated adult bust ratio | `silhouette_proportion` | P1 | medium_guard / MEDIUM_CONDITIONAL_REVIEW |
| A04 | 굵은 허벅지／Thick thighs | large thigh transverse volume | `silhouette_proportion` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A05 | 언더버스트 코르셋 | underbust corset upper edge | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| A06 | 뷔스티에형 상의 | bustier panel structure | `garment_detail` | P1 | split / ATOM_REVIEW |
| A07 | 플런지 네크라인 | plunging neckline opening | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A08 | 키홀 컷아웃 | bounded keyhole cutout | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A09 | 언더붑형 컷 | lower-bust garment exposure | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A10 | 사이드붑형 컷 | lateral-bust garment exposure | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A11 | 백리스／등 파임 | open back garment coverage | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A12 | 하이레그／하이컷 | high-cut leg-opening placement | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A13 | 보디수트 | one-piece bodysuit continuity | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| A14 | 캣슈트 | torso-to-ankle catsuit continuity | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| A15 | 비키니 아머 | minimal fantasy plate coverage | `costume_style` | P2 | recipe / CONTEXT_RECIPE_REVIEW |
| A16 | 버니 수트 | selected bunny costume assembly | `costume_style` | P0 | recipe / CONTEXT_RECIPE_REVIEW |
| A17 | 가터 벨트 | garter-belt stocking connection | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A18 | 사이하이／허벅지 길이 스타킹 | thigh-high stocking upper edge | `garment_detail` | P1 | reuse / EXISTING_OWNER_REVIEW |
| A19 | 절대영역／絶対領域 | hem-to-stocking exposed thigh band | `garment_detail` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A20 | 바디 하네스 | body harness strap attachment | `wearable_accessory` | P0 | reuse / EXISTING_OWNER_REVIEW |
| A21 | 본디지풍 복식 | restraint-inspired garment hardware | `wearable_accessory` | P1 | split / ATOM_REVIEW |
| A22 | ‘동정을 죽이는 스웨터’／Virgin killer sweater | sleeveless open-back knit assembly | `garment_detail` | P1 | split / ATOM_REVIEW |
| A23 | 치치부쿠로／乳袋 | illustrated clinging chest fabric | `garment_detail` | P0 | medium_guard / MEDIUM_CONDITIONAL_REVIEW |
| P01 | 오버사이즈 무기 | oversized weapon part-to-grip ratio | `prop` | P1 | hold_scope / HOLD_UNSCOPED_SLOT |
| P02 | 대검·슬래브 소드형 | slab-like broad sword blade | `prop` | P1 | hold_scope / HOLD_UNSCOPED_SLOT |
| P03 | 건블레이드형 | combined gun-and-blade assembly | `prop` | P1 | hold_scope / HOLD_UNSCOPED_SLOT |
| P04 | 열쇠형 무기 | key-shaped weapon assembly | `prop` | P0 | hold_scope / HOLD_UNSCOPED_SLOT |
| P05 | 사슬 연결 무기 | chain-linked weapon assembly | `prop` | P1 | hold_scope / HOLD_UNSCOPED_SLOT |
| P06 | 부유 비트·지원 유닛 | detached support-unit spacing | `prop` | P0 | hold_scope / HOLD_UNSCOPED_SLOT |
| P07 | 헤일로／후광 고리 | detached halo ring placement | `wearable_accessory` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| P08 | 기계식 날개 | back-mounted mechanical wing assembly | `wearable_accessory` | P0 | atom / ATOM_REVIEW |
| P09 | 바이저 얼굴 | display-visor face panel | `wearable_accessory` | P0 | split / ATOM_REVIEW |
| P10 | 외부 광학 눈 | integrated optical eye module | `anatomical_connection` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| P11 | 전면 마스크 | full-face mask coverage | `wearable_accessory` | P0 | atom / ATOM_REVIEW |
| P12 | 봉투·상자형 머리 덮개 | packaging object worn as head cover | `wearable_accessory` | P0 | split / ATOM_REVIEW |
| P13 | 케이지·철창형 투구 | open-bar cage helmet | `wearable_accessory` | P1 | atom / ATOM_REVIEW |
| P14 | 봉합·패치워크 신체 | stitched body-segment boundaries | `body_marking` | P1 | cross_dimension / HOLD_CROSS_DIMENSION |
| P15 | 바이오메카니컬 | organic-mechanical continuous interface | `anatomical_connection` | P1 | cross_dimension / HOLD_CROSS_DIMENSION |
| P16 | 배틀 대미지 | region-specific battle damage | `aftermath_trace` | P0 | hold_scope / HOLD_UNSCOPED_SLOT |
| P17 | 혈흔·피 튀김 | localized blood-like surface marks | `aftermath_trace` | P1 | hold_scope / HOLD_UNSCOPED_SLOT |
| P18 | 혈루형 표현 | blood-like tear path | `aftermath_trace` | P1 | hold_scope / HOLD_UNSCOPED_SLOT |
| P19 | 노출 골격형 | visible skeleton beneath missing outer surface | `anatomical_connection` | P1 | cross_dimension / HOLD_CROSS_DIMENSION |
| P20 | 내부 배선 노출형 | exposed wiring inside artificial shell | `anatomical_connection` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| P21 | 기생·침식형 부속물 | rooted intrusion-like appendages | `anatomical_connection` | P1 | cross_dimension / HOLD_CROSS_DIMENSION |
| P22 | 다안·다구형 | multiple eye or mouth organ placement | `anatomical_connection` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
| P23 | 가면 아래 비어 있는 얼굴 | visible empty region beneath mask opening | `wearable_accessory` | P0 | cross_dimension / HOLD_CROSS_DIMENSION |
