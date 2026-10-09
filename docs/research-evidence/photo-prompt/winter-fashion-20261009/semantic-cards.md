# 겨울 패션 시각 의미 카드

가족 수준 리서치와 후보 초안이다. 변형은 대안이며 전체를 한 의무로 활성화하지 않는다. 직접 출처의 사실 범위와 연구자의 그래프·문장 제안을 구분한다.

## WF01 — 레이어의 역할·순서·드러나는 경계 (P0)

레이어는 별개 의복의 안팎 순서와 목선·커프·밑단의 가림 관계로 표현한다. 기능적 베이스·미드·셸과 사진에서 보이는 안팎 관계는 별도다

- 소유자: 같은 착용자의 이미 선언된 이너·중간층·외투
- 관계 예: `declared_inner_cuff → extends_beyond → declared_outer_cuff`. 같은 착용자·서로 다른 선언된 두 의복; 어느 커프인지 명시
- 속성 후보 풀: layers.order, layers.visible_edges. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 같은 색 하나의 패널을 세 벌로 세지 않는다; 겨울이라는 말로 삼중 레이어나 후드·눈을 강제하지 않는다
- 관찰 조건: 서로 다른 두 의복의 실제 가장자리와 연속면이 함께 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S01: Patagonia](https://www.patagonia.com/guides/cold-weather-layering/), [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html)

각각 독립된 선택형 문장 초안:

1. the declared inner knit cuff extends visibly beyond the same wearer's coat cuff
2. the declared open coat panels frame a separate knit layer beneath

## WF02 — 서멀·방풍·발수·방수의 비시각 명세 (P0)

보온·통기·방풍·발수·방수는 용도·성능 또는 설계 명세다. 요청된 외관이 있으면 그 표면·부품을 별도 의미로 작성한다

- 소유자: 명시된 의복 제품과 시험·소재 명세
- 관계 예: `declared_product_specification → declares_performance → named_weather_resistance`. 비시각 명세 관계; 시각 hard obligation으로 컴파일하지 않음
- 속성 후보 풀: specification.thermal, specification.weather_resistance. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 두껍거나 매끈함, 물방울 한 개, 눈 배경은 성능 인증이나 실제 체온을 증명하지 않는다
- 관찰 조건: 명세·시험은 별도 근거; 사진은 명시적으로 선택된 표면·봉제·플랩만 검사
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S01: Patagonia](https://www.patagonia.com/guides/cold-weather-layering/), [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html)

비시각 명세다. 자동 시각 후보를 작성하지 않는다.

## WF03 — 다운·합성 충전재·필파워·충전량 (P0)

원료·필파워·충전량과 겉의 부풀음은 독립이다. 필파워와 충전량은 별도 수치이며 내부 재료는 겉사진에서 특정하지 않는다

- 소유자: 해당 재킷의 충전재 및 표기 명세
- 관계 예: `declared_fill_specification → records_measurement → named_fill_power_or_weight`. 두 수치를 분리한 명세 관계; 겉 볼륨과 동치가 아님
- 속성 후보 풀: specification.fill_type, specification.fill_power, specification.fill_weight. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: puffer를 down으로 자동 번역하지 않는다; 더 두껍게 보인다고 높은 필파워나 더 따뜻함을 판정하지 않는다
- 관찰 조건: 수치·원료는 제품 명세 또는 단면 증거가 필요하며 일반 인물사진은 UNSCORED
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html), [S03: REI](https://www.rei.com/learn/expert-advice/what-is-down-fill-power.html), [S04: Rab](https://rab.equipment/eu/rab-lab/down-jackets-buying-guide)

비시각 명세다. 자동 시각 후보를 작성하지 않는다.

## WF04 — 배플·퀼팅·납작한 인쇄선 (P0)

배플은 충전재 구획 구조이며 퀼팅은 겹을 연결하는 누빔이다. 외관 후보는 눌린 구획선과 그 사이 솟은 면을 구분해 표현한다

- 소유자: 이미 선언된 충전 외투의 겉패널·구획선·볼록 구획
- 관계 예: `declared_recessed_stitch_line → separates → adjacent_inflated_chambers`. 같은 충전 외투 겉패널; 내부 박스월·원료는 별도
- 속성 후보 풀: structure.visible_chambers, surface.stitched_relief. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 평면 격자 프린트·엠보스와 혼동하지 않는다; 겉선만으로 박스월·충전재 성분·보온성을 확정하지 않는다
- 관찰 조건: 원본 해상도에서 패널 볼륨과 연결된 낮은 구획선이 같이 보여야 한다
- 기존 ID 검토: clt_ct097_v1, clt_ct097_v2, clothing_ct097_v1
- 근거: [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html), [S04: Rab](https://rab.equipment/eu/rab-lab/down-jackets-buying-guide), [S10: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/weaving/complex-woven-fabric-designs/)

각각 독립된 선택형 문장 초안:

1. the declared puffer panel forms inflated horizontal chambers separated by recessed stitched lines
2. the declared quilted panel has shallow diamond cells bounded by visible stitching

## WF05 — 울·동물성 섬유의 원료와 표면 분리 (P0)

울·메리노·램스울·캐시미어·모헤어·앙고라·알파카·카멜 헤어는 원료 범주다. 가공·혼방·실과 조직 때문에 이름과 털 외관은 일대일이 아니다

- 소유자: 원료는 해당 의복 명세; 표면은 해당 의복의 직물면
- 관계 예: `declared_fiber_halo → projects_from → declared_knit_ground`. 같은 의복면; 원료 ID는 제품 명세에 남김
- 속성 후보 풀: specification.fiber_identity, surface.fiber_halo. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 모헤어 산양과 앙고라토끼를 합치지 않는다; 카멜색을 낙타털로, 비싼 듯한 외관을 캐시미어 진위로 판정하지 않는다
- 관찰 조건: 이미지는 선택된 잔털·매끈함·파일만 검사하며 원료와 혼용률은 별도 명세
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S05: Woolmark](https://www.woolmark.com/fibre/), [S06: CCMI](https://cashmere.org/facts.php), [S07: Mohair South Africa](https://www.mohair.co.za/natural-fibre)

각각 독립된 선택형 문장 초안:

1. a fine low halo of short fibers lies over the declared knit panel without obscuring its stitches
2. long wispy fibers project from the declared knit yarn while the knitted ground remains visible

## WF06 — 퍼·페이크 퍼의 길이·밀도·바탕 (P0)

털룩은 파일의 길이·밀도·방향·바탕에서 보이는 경계로 분해한다. 원료 및 천연·인조 여부는 명세에 남긴다

- 소유자: 해당 의복의 바탕과 붙어 있는 파일
- 관계 예: `declared_pile → attached_to → declared_coat_backing`. 같은 패널의 바탕·끝단; 착용자 체모·머리에서 분리
- 속성 후보 풀: surface.pile_length, surface.pile_density. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 긴 머리카락·착용자의 체모·배경 털로 대체하지 않는다; 풍성한 표면이 천연 모피 증거는 아니다
- 관찰 조건: 파일이 해당 의복의 바탕에 연속적으로 붙어 있는 구역과 외곽이 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S08: UGG](https://www.ugg.com/ca/help-center.html?a=Information-on-UGG%28r%29-and-Our-Brand---id--J6cPk4gJT4aqfLYPB4K1ig), [S09: Patagonia](https://www.patagonia.com/product/mens-retro-pile-fleece-jacket/22802.html), [S42: Patagonia Worn Wear](https://wornwear.patagonia.com/products/mens-reversible-recycled-sherpa-jacket_20430_smdb)

각각 독립된 선택형 문장 초안:

1. dense short pile covers the declared coat surface with its fabric edge still readable
2. long pile projects outward from the declared coat panel and partially veils its own seam

## WF07 — 시어링·셰르파·테디의 다른 의미 (P0)

전통적 시어링은 털 붙은 양가죽, 셰르파는 털을 닮은 플리스 외관, 테디는 코트의 포근한 외관 표현이다. 상품 shearling fleece는 합성일 수도 있다

- 소유자: 선택한 재킷의 털면·가죽 또는 편물 바탕·접힌 단
- 관계 예: `declared_turned_edge → reveals_reverse_of → same_outer_panel`. 같은 패널 양면의 연속; 천연·합성은 독립 명세
- 속성 후보 풀: surface.curled_pile, structure.visible_backing. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 셰르파를 항상 순수 합성, 테디를 항상 양가죽으로 고정하지 않는다; 두 외관의 유사성은 소재 동등성 근거가 아니다
- 관찰 조건: 양면 관계를 검사할 때 접힌 단에서 두 면의 연속성을 보여야 하며 숨은 바탕은 미관찰
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S08: UGG](https://www.ugg.com/ca/help-center.html?a=Information-on-UGG%28r%29-and-Our-Brand---id--J6cPk4gJT4aqfLYPB4K1ig), [S09: Patagonia](https://www.patagonia.com/product/mens-retro-pile-fleece-jacket/22802.html), [S42: Patagonia Worn Wear](https://wornwear.patagonia.com/products/mens-reversible-recycled-sherpa-jacket_20430_smdb)

각각 독립된 선택형 문장 초안:

1. the declared jacket's turned collar reveals a smooth leather-like face continuous with its short woolly reverse
2. rounded curled pile covers the declared fleece jacket over a visibly textile-backed edge

## WF08 — 퍼 트림·페더 트림의 부착 위치 (P0)

몸판 전체 소재와 특정 가장자리의 트림을 구분한다. 털 다발과 깃털의 줄기·가는 가지형 외곽도 다른 관찰 축이다

- 소유자: 해당 코트·후드·커프·밑단과 거기에 붙인 트림
- 관계 예: `declared_pile_trim → follows_and_attaches_to → declared_collar_edge`. 같은 코트 칼라만 효과; 몸판 전체로 전파하지 않음
- 속성 후보 풀: trim.location, trim.material_appearance, trim.attachment. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 퍼 칼라를 전체 퍼 코트로 전파하지 않는다; 얼굴 머리카락이나 떠다니는 깃털은 부착된 트림의 증거가 아니다
- 관찰 조건: 몸판과 트림이 만나는 부착 경계 및 선택된 가장자리만 검사
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S08: UGG](https://www.ugg.com/ca/help-center.html?a=Information-on-UGG%28r%29-and-Our-Brand---id--J6cPk4gJT4aqfLYPB4K1ig), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. a pile trim follows the edge of the declared coat collar while its body panel remains smooth
2. separate feather-like vanes attach along the declared cuff edge and project beyond it

## WF09 — 트위드·헤링본·하운드투스 (P0)

트위드는 원단군, 헤링본은 방향 전환과 오프셋이 있는 조직·무늬, 하운드투스는 꺾인 격자 모티프다. 하운드투스는 니트에도 나타난다

- 소유자: 선택한 직물 패널의 실·반복 무늬
- 관계 예: `declared_opposed_twill_runs → offset_at → direction_reversal_boundary`. 같은 직물 반복; 셰브론 연속점과 비교
- 속성 후보 풀: surface.mottled_yarns, surface.pattern_geometry. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 헤링본을 점이 이어지는 셰브론과 합치지 않는다; 무늬 이름으로 반드시 울·직물·흑백이라고 고정하지 않는다
- 관찰 조건: 실제 조직을 주장할 때 실 방향·반복 끊김이 보이는 근접 증거가 필요
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S13: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/knit-basics/), [S21: Hainsworth](https://www.hainsworth.co.uk/wp-content/uploads/2018/03/Hainsworth-True-Heritage-Shade-Card.pdf), [S39: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)

각각 독립된 선택형 문장 초안:

1. opposed diagonal runs on the declared coat panel break and offset where their directions reverse
2. the declared knit panel carries repeating broken-check motifs whose color boundaries follow the stitches

## WF10 — 부클레·멜턴·플란넬 (P1)

부클레는 고리·매듭 효과, 멜턴은 치밀한 코팅 원단 범주, 플란넬은 기모한 직물 범주로 나눈다. 멜란지 색과 체크는 별도다

- 소유자: 선택한 원단의 고리·치밀면·기모면
- 관계 예: `declared_yarn_loops → rise_from → declared_fabric_ground`. 같은 원단 면; 빈 개구·모피와 분리
- 속성 후보 풀: surface.looped_yarn, surface.compacted_face, surface.nap. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 부클레 고리를 니트 구멍·모피로, 플란넬을 체크무늬로, 멜턴을 특정 색·원료로 자동 고정하지 않는다
- 관찰 조건: 고리·얕은 잔털·조직을 가리는 치밀한 면 중 선택된 변형이 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S12: Cotton Incorporated CottonWorks](https://cottonworks.com/encyclopedia-item/boucle/), [S21: Hainsworth](https://www.hainsworth.co.uk/wp-content/uploads/2018/03/Hainsworth-True-Heritage-Shade-Card.pdf), [S40: Cotton Incorporated CottonWorks](https://cottonworks.com/encyclopedia-item/flannel/)

각각 독립된 선택형 문장 초안:

1. small irregular yarn loops rise from the declared boucle panel while its woven ground stays readable
2. a short brushed nap softens the declared flannel panel without imposing a check pattern

## WF11 — 코듀로이·벨벳·벨루어와 골지 (P0)

코듀로이의 솟은 골은 파일 구조이며 리브 니트의 앞뒤 웨일과 다르다. 벨벳·벨루어는 파일 외관과 조직·용례를 분리한다

- 소유자: 해당 패널의 솟은 파일 웨일 또는 짧은 파일면
- 관계 예: `declared_pile_wales → separated_by → ground_channels`. 같은 코듀로이 패널; 니트 웨일 대체 금지
- 속성 후보 풀: surface.pile_wales, surface.directional_nap. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 모든 세로줄을 골지로 합치지 않는다; 정면 매끈함만으로 벨벳 직조·벨루어 편직을 판정하지 않는다
- 관찰 조건: 골의 솟음·사이 바탕·파일 방향이 충분히 읽히는 해상도에서 검사
- 기존 ID 검토: clt_ct089_v1, sff_pro_t10
- 근거: [S10: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/weaving/complex-woven-fabric-designs/), [S11: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/)

각각 독립된 선택형 문장 초안:

1. raised pile wales run along the declared corduroy panel with narrow ground channels between them
2. the declared velvet-like panel has dense short pile and direction-dependent light and dark areas

## WF12 — 스웨이드·레더·페이크 레더 (P1)

짧은 무광 보풀, 매끈한 주름·그레인·광택을 별도 외관 후보로 만든다. 천연·인조·가공 이력은 명세다

- 소유자: 해당 의복 또는 부츠의 갑피 표면
- 관계 예: `declared_short_nap → covers → declared_boot_upper`. 같은 갑피 표면; 재료 진위·방수 추론 금지
- 속성 후보 풀: surface.short_nap, surface.smooth_grain. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 스웨이드룩과 천연 가죽, 유광과 방수, 주름과 낡은 상태를 동의어로 묶지 않는다
- 관찰 조건: 선택된 표면에 보풀·그레인·주름·빛 반응이 붙어 있어야 한다
- 기존 ID 검토: suede_nap_texture, clt_ct080_v1
- 근거: [S08: UGG](https://www.ugg.com/ca/help-center.html?a=Information-on-UGG%28r%29-and-Our-Brand---id--J6cPk4gJT4aqfLYPB4K1ig), [S10: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/weaving/complex-woven-fabric-designs/)

각각 독립된 선택형 문장 초안:

1. a short diffuse suede-like nap covers the declared boot shaft
2. the declared leather-like panel has a smooth face with shallow bending creases

## WF13 — 새틴·저지와 원료 (P1)

새틴은 조직 계열이며 실크라는 원료와 다르다. 저지는 편물 구조다. 부드러운 반사·작은 루프는 외관 증거로 분리한다

- 소유자: 선택한 원단면의 광택·루프와 드레이프
- 관계 예: `declared_highlight_band → follows → declared_fabric_fold`. 같은 원단의 빛 반응; 조명·카메라 자동 변경 금지
- 속성 후보 풀: surface.specular_behavior, surface.knit_loops. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 새틴을 자동 실크·시어·슬립 드레스로, 저지를 항상 밀착·얇은 면 소재로 만들지 않는다
- 관찰 조건: 광택 띠는 원단 주름을 따라가고 루프는 같은 면에 있어야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S10: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/weaving/complex-woven-fabric-designs/), [S11: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [S13: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/knit-basics/)

각각 독립된 선택형 문장 초안:

1. a smooth satin-like highlight band follows the folds of the declared skirt panel
2. small face-side knit loops remain visible on the declared jersey panel

## WF14 — 플리스·기모·브러시드의 위치 (P0)

기모는 표면 가공, 플리스는 보송한 소재군이다. 겉의 파일과 숨은 안기모를 독립 명세·관찰로 다룬다

- 소유자: 선택한 옷의 겉면 또는 드러난 안쪽 면
- 관계 예: `declared_brushed_inner_face → lies_behind → declared_outer_face`. 같은 커프의 실제 안팎 노출에 한정
- 속성 후보 풀: surface.nap, layers.visible_lining. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 매끈한 겉면으로 안기모를 PASS하지 않는다; 기모를 모피·울과 합치지 않는다
- 관찰 조건: 안면 의무는 뒤집힌 커프·열린 단 등 실제 안면이 보일 때만 검사
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S09: Patagonia](https://www.patagonia.com/product/mens-retro-pile-fleece-jacket/22802.html), [S11: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [S40: Cotton Incorporated CottonWorks](https://cottonworks.com/encyclopedia-item/flannel/), [S42: Patagonia Worn Wear](https://wornwear.patagonia.com/products/mens-reversible-recycled-sherpa-jacket_20430_smdb)

각각 독립된 선택형 문장 초안:

1. a fuzzy fleece surface covers only the declared midlayer
2. the declared turned cuff exposes a brushed inner face beneath its smoother outer face

## WF15 — 파인 게이지·청키의 코 크기와 촬영 (P0)

촘촘한 작은 코와 굵고 큰 코의 외관은 구별하되 게이지 숫자·바늘·밀도는 명세 또는 측정이다

- 소유자: 선택한 니트 패널의 실 굵기·코 간격
- 관계 예: `declared_knit_loops → repeat_across → declared_knit_panel`. 코 크기 외관과 수치 게이지를 분리
- 속성 후보 풀: surface.stitch_scale, surface.yarn_bulk. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 멀리서 안 보이는 작은 코를 매끈한 인쇄 니트로 PASS하지 않는다; 청키라는 이름으로 오버사이즈 몸판을 강제하지 않는다
- 관찰 조건: 요청된 구도를 유지한 원본에서 코가 읽히는지 먼저 판정하며 보이지 않으면 미관찰
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S11: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [S13: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/knit-basics/), [S15: Purl Soho](https://www.purlsoho.com/create/working-into-the-stitch-below/)

각각 독립된 선택형 문장 초안:

1. small closely spaced stitches cover the declared knit panel
2. thick yarn forms large individually readable loops on the declared sweater panel

## WF16 — 리브·와이드 리브·피셔맨 립 (P0)

리브의 솟은 줄과 숨은 뒤줄, 와이드 리브의 넓은 반복, 피셔맨 립의 아래 코 제작 의미를 구분한다

- 소유자: 선택한 니트 구역의 앞·뒤 웨일 및 홈
- 관계 예: `declared_knitted_ridge → alternates_with → declared_recessed_knit_channel`. 같은 니트 구역; 별개 커프나 건축 리브 제외
- 속성 후보 풀: surface.rib_repeat, surface.rib_depth. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 코듀로이 파일 골·넥타이 리브·건축 리브를 제외한다; 깊은 골만으로 피셔맨 제작법·브리오슈 동일성을 보장하지 않는다
- 관찰 조건: 같은 직물에서 능선·홈·코가 읽히며 골 폭은 해당 변형 기준으로만 검사
- 기존 ID 검토: clt_ct087_v1, clt_ct087_v2, clothing_ct087_v1
- 근거: [S11: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [S15: Purl Soho](https://www.purlsoho.com/create/working-into-the-stitch-below/)

각각 독립된 선택형 문장 초안:

1. raised knitted columns alternate with recessed channels on the declared top
2. broad knitted ribs repeat across the declared panel with visibly wider recessed intervals

## WF17 — 케이블 니트와 아란 문맥 (P0)

케이블은 뜬 줄의 입체 교차, 아란은 전통·복합 배치 문맥이다. 아란의 색·지역·원료·제작 이력은 전부 같은 시각 의무가 아니다

- 소유자: 같은 니트 패널의 솟은 줄·교차점·바탕
- 관계 예: `declared_knitted_strand_A → crosses_over → declared_knitted_strand_B`. 같은 니트의 교차 전후 연속; 평면 프린트 제외
- 속성 후보 풀: surface.cable_crossings, surface.cable_layout. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 밧줄 프린트나 얹힌 머리카락으로 대체하지 않는다; 모든 케이블을 아란·고대 상징으로 고정하지 않는다
- 관찰 조건: 각 교차 전후 줄의 연속성과 앞뒤 솟음이 같은 패널에서 보인다
- 기존 ID 검토: clt_ct008_v1, clt_ct008_v2, clothing_ct008_v1
- 근거: [S14: V and A](https://www.vam.ac.uk/articles/british-knitting-traditions), [S15: Purl Soho](https://www.purlsoho.com/create/working-into-the-stitch-below/)

각각 독립된 선택형 문장 초안:

1. raised knitted strands cross over and under one another on the declared sweater panel
2. separate cable and textured-knit columns occupy the declared Aran-inspired panel

## WF18 — 페어아일·노르딕·요크의 서로 다른 축 (P0)

페어아일은 전통 색무늬 문맥, 노르딕은 넓은 상업 모티프군, 요크는 배치 구역이다. 같은 옷에 이 축들이 함께 있을 수 있다

- 소유자: 선택한 니트의 모티프·가로 띠·목어깨 요크
- 관계 예: `declared_motif_band → follows → declared_neck_shoulder_yoke`. 같은 니트의 배치 구역; 모티프와 역사 범주 독립
- 속성 후보 풀: surface.motif_repeat, surface.motif_placement. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 모든 다색·순록·눈꽃을 페어아일로 합치지 않는다; 배경 눈·국적·스키 장비를 자동 추가하지 않는다
- 관찰 조건: 반복 작은 모티프와 구역 경계가 읽히며 겨울 문맥은 별도 유지
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S14: V and A](https://www.vam.ac.uk/articles/british-knitting-traditions), [S17: Brooklyn Tweed](https://brooklyntweed.com/pages/stranded-colorwork-101)

각각 독립된 선택형 문장 초안:

1. small multicolor geometric motifs repeat in horizontal bands on the declared knit
2. a patterned band follows the declared sweater's neck-and-shoulder yoke while the lower body remains plain

## WF19 — 아가일과 대각선 오버레이 (P1)

아가일은 마름모 반복과 그 위를 가로지르는 가는 선의 배치로 표현한다. 프레피는 별도 스타일 문맥이다

- 소유자: 선택한 니트·양말의 마름모 색면과 가는 대각선
- 관계 예: `declared_fine_diagonal_line → crosses → declared_diamond_color_block`. 같은 아가일 반복; 다이아몬드 퀼트와 구분
- 속성 후보 풀: surface.argyle_geometry. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 큰 마름모 퀼팅·일반 격자·모든 페어아일을 아가일로 통합하지 않는다
- 관찰 조건: 색면 경계와 가는 대각선이 충분히 보이는 반복 영역이 필요
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S13: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/knit-basics/), [S14: V and A](https://www.vam.ac.uk/articles/british-knitting-traditions), [S34: Vogue](https://www.vogue.com/article/core-aesthetic-microtrends-2023)

각각 독립된 선택형 문장 초안:

1. contrasting diamond blocks repeat across the declared knit panel with thin diagonal lines crossing them

## WF20 — 자카드·인타르시아·스트랜디드 (P0)

색면의 크기·경계·코, 뒤쪽 실 운반은 구분한다. 인타르시아 공정과 스트랜디드 플로트는 뒷면 또는 제작 증거를 요구한다

- 소유자: 해당 니트의 앞 색면·코와 드러난 뒷면 플로트
- 관계 예: `declared_reverse_float → spans_between → declared_reverse_stitches`. 뒤면이 실제 보이는 니트 변형에 한정
- 속성 후보 풀: surface.colorwork_stitches, structure.visible_reverse. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 큰 그림이 인타르시아 제작 증거는 아니다; 프린트·자수·중복뜨기와 니트 공정을 정면만으로 단정하지 않는다
- 관찰 조건: 앞은 코에 맞는 색면만, 뒤면 공정은 실제 노출된 뒷면과 선 경로가 있을 때 검사
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S11: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [S16: Purl Soho](https://www.purlsoho.com/create/intarsia/), [S17: Brooklyn Tweed](https://brooklyntweed.com/pages/stranded-colorwork-101)

각각 독립된 선택형 문장 초안:

1. large contrasting color areas follow the stitches of the declared knit panel
2. the declared turned knit edge exposes separate yarn floats spanning its reverse side

## WF21 — 포인텔·오픈워크·크로셰 (P0)

포인텔은 규칙적 작은 구멍의 니트 변형, 오픈워크는 빈 공간 외관, 크로셰는 코바늘 공정이다. 구멍의 형태와 아래층을 따로 결속한다

- 소유자: 해당 니트 바탕·작은 구멍·그 아래 층
- 관계 예: `declared_eyelet_boundary → surrounds_opening_revealing → declared_opaque_inner_layer`. 같은 니트 구멍·그 아래 선언된 이너; 맨살 자동화 금지
- 속성 후보 풀: surface.openwork_geometry, layers.visible_underlayer. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 얇은 시어 면·찢어진 구멍·레이스 프린트와 구분한다; 작은 구멍이 반드시 맨살·속옷 비침을 뜻하지 않는다
- 관찰 조건: 구멍의 테두리 루프와 연속 바탕, 그 아래 선택한 이너가 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S13: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/knit-basics/), [S18: UNIQLO](https://www.uniqlo.com/sg/en/products/E487121-000/00)

각각 독립된 선택형 문장 초안:

1. small repeating eyelets open through the declared knitted ground and reveal the declared opaque inner layer
2. larger open loop spaces form a mesh-like area on the declared knit panel

## WF22 — 퍼지 니트·멜란지의 표면·색 독립 (P1)

퍼지는 솟은 잔털 외관, 멜란지는 미세 색 혼합이다. 한 옷에서 따로 또는 같이 선택한다

- 소유자: 선택한 니트의 잔털과 실색 혼합
- 관계 예: `declared_light_dark_flecks → intermingle_within → declared_knit_yarn`. 색 혼합은 해당 직물만; 화면 노이즈와 분리
- 속성 후보 풀: surface.fiber_halo, surface.melange_color. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 퍼지를 모헤어 진위·전체 퍼로, 멜란지를 노이즈·보케·곰팡이·낡음으로 대체하지 않는다
- 관찰 조건: 잔털은 니트에 붙어 있고 색 혼합은 해당 실·면에 국소적으로 있어야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S05: Woolmark](https://www.woolmark.com/fibre/), [S07: Mohair South Africa](https://www.mohair.co.za/natural-fibre), [S12: Cotton Incorporated CottonWorks](https://cottonworks.com/encyclopedia-item/boucle/), [S21: Hainsworth](https://www.hainsworth.co.uk/wp-content/uploads/2018/03/Hainsworth-True-Heritage-Shade-Card.pdf)

각각 독립된 선택형 문장 초안:

1. wispy fibers soften the declared knit's edge while its knitted ground stays visible
2. fine light and dark yarn flecks intermingle within the declared knit rather than forming large printed spots

## WF23 — 오버코트·체스터필드·카·맥시 길이 (P1)

긴 겉코트라는 범주, 단정한 테일러드 변형, 활동형 짧은 코트, 발목 근처 길이를 나눈다. 벨벳 칼라는 체스터필드 전통형 중 선택 요소다

- 소유자: 선택한 코트의 라펠·앞판·밑단과 착용자 기준점
- 관계 예: `declared_coat_hem → ends_near → same_wearer_ankle_landmark`. 같은 착용자; 카메라·신체 길이 효과 없음
- 속성 후보 풀: type.tailored_coat, length.hem_landmark. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 체스터필드를 항상 특정 칼라·단추 수로 고정하지 않는다; maxi를 바닥 끌림이나 신체 키 변화로 실현하지 않는다
- 관찰 조건: 밑단·무릎·종아리·발목 등 요청한 기준점이 같은 착용자에 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S19: Gloverall](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat), [S21: Hainsworth](https://www.hainsworth.co.uk/wp-content/uploads/2018/03/Hainsworth-True-Heritage-Shade-Card.pdf), [S38: TOTEME](https://toteme.com/products/embroidered-scarf-coat-black)

각각 독립된 선택형 문장 초안:

1. the declared tailored coat hem ends near the same wearer's ankles
2. the declared shorter coat ends below the hips while leaving the lower thighs clear

## WF24 — 싱글·더블브레스트와 피코트 (P0)

앞판 겹침과 여밈열을 실제 패널 관계로 표현한다. 피코트는 전통적으로 짧은 모직·큰 라펠·더블 여밈을 조합한다

- 소유자: 해당 코트의 두 앞판·단추열·라펠
- 관계 예: `declared_left_front_panel → overlaps → declared_right_front_panel`. 같은 코트; 단추열 장식과 실제 여밈 분리
- 속성 후보 풀: structure.front_overlap, structure.button_rows. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 단추가 두 줄로 장식된 것과 실제 겹친 여밈을 구분한다; 열린 코트에서도 여밈 구조와 현재 상태는 다르다
- 관찰 조건: 겹침 가장자리 또는 양쪽 패널의 이어지는 여밈 부품이 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S19: Gloverall](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat)

각각 독립된 선택형 문장 초안:

1. the declared coat's front panels overlap broadly beneath two visible rows of buttons
2. the declared single-front coat closes along a narrow overlap with one main button row

## WF25 — 더플코트 토글·고리의 경로 (P0)

더플의 후드·토글은 다른 구성요소다. 닫힌 토글은 한 앞판 부품이 맞은편 고리를 통과해 고정되는 관계로 쓴다

- 소유자: 같은 코트 양 앞판의 토글·고리·부착점
- 관계 예: `declared_toggle → passes_through → opposite_front_loop`. 양 부착점은 같은 코트의 서로 다른 앞판
- 속성 후보 풀: closure.toggle_path, structure.hood_attachment. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 토글 모양 금속 장식·주머니 고리·늘어진 끈으로 여밈 성공을 판정하지 않는다
- 관찰 조건: 토글·통과한 고리·양 부착점이 같은 여밈 경로에 연결되어야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S19: Gloverall](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat)

각각 독립된 선택형 문장 초안:

1. a toggle on the declared coat passes through the loop anchored on its opposite front panel
2. the declared duffle coat's hood joins its neckline above the visible toggle fastenings

## WF26 — 랩·로브·벨티드 코트 (P0)

앞판을 감싸 겹치는 랩, 가운 같은 느슨한 인상, 벨트 보유와 실제 조임을 분리한다

- 소유자: 같은 코트의 겹친 앞판·허리띠·고정점
- 관계 예: `declared_coat_belt → encircles_and_indents → declared_coat_waist`. 안쪽 니트·몸 윤곽 변경으로 전파 금지
- 속성 후보 풀: closure.wrap_overlap, closure.belt_route. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 벨트가 있다는 이유만으로 랩·허리 조임을 자동 확정하지 않는다; 코트 벨트를 안쪽 니트 허리 변화로 전파하지 않는다
- 관찰 조건: 앞판 겹침과 허리띠의 연결된 경로·매듭 또는 버클을 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S19: Gloverall](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat), [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

각각 독립된 선택형 문장 초안:

1. the declared coat's front panels overlap under a belt tied around that same coat
2. the belt visibly indents only the declared coat at the waist while its upper and lower panels remain fuller

## WF27 — 코쿤·스윙의 폭 분포 (P1)

코쿤은 둥근 몸통 여유와 하부 수축, 스윙은 상부에서 하부로 퍼지는 외곽으로 선택 변형을 만든다. 움직임 이력은 별도다

- 소유자: 선택한 코트 상부·몸통·밑단의 외곽
- 관계 예: `declared_coat_torso_contour → narrows_toward → declared_coat_hem_contour`. 같은 외곽의 폭 분포; 동작 시퀀스 추론 금지
- 속성 후보 풀: silhouette.width_distribution. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 오버사이즈·A라인·고치 배경과 이름만으로 합치지 않는다; 사진 한 장으로 흔들림의 전후 변화를 증명하지 않는다
- 관찰 조건: 양 외곽·몸통 최대폭·밑단 폭을 비교할 수 있는 구도가 필요
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S19: Gloverall](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat), [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/)

각각 독립된 선택형 문장 초안:

1. the declared coat's rounded torso narrows toward its lower hem
2. the declared coat widens from the shoulders toward a loose flaring hem

## WF28 — 케이프 코트와 팔 개구부 (P0)

케이프는 어깨에서 받쳐 팔을 덮는 망토형이다. 팔 슬릿이 있는 변형과 단순 덮개를 분리한다

- 소유자: 선택한 케이프의 어깨 받침·드레이프·팔 틈
- 관계 예: `declared_forearm → emerges_through → declared_cape_arm_slit`. 같은 착용자·해당 케이프의 경계 닫힌 틈
- 속성 후보 풀: structure.arm_openings, structure.shoulder_support. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 일반 소매를 없애 팔을 비현실적으로 관통시키지 않는다; cape라는 단어의 지형 의미와 분리한다
- 관찰 조건: 어깨 지지·양 끝 드레이프·팔이 나오는 선택 개구부의 실제 경계가 읽혀야 한다
- 기존 ID 검토: clt_ct011_v1
- 근거: [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/)

각각 독립된 선택형 문장 초안:

1. the declared cape coat hangs from the shoulders over the upper arms
2. the same wearer's forearm emerges through a bounded slit in the declared cape panel

## WF29 — 트렌치의 독립 부품 (P1)

트렌치라는 범주와 견장·스톰 플랩·벨트·여밈의 선택 구조를 분리한다. 겨울용 충전·안감은 별도다

- 소유자: 해당 코트의 견장·스톰 플랩·라펠·벨트
- 관계 예: `declared_storm_flap → overlaps → declared_coat_upper_front`. 해당 코트의 부착된 별개 덧패널
- 속성 후보 풀: details.storm_flap, details.epaulette, closure.belt_route. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 모든 트렌치에 모든 부품·방수·전쟁 맥락을 강제하지 않는다; 견장을 어깨끈 하네스로 바꾸지 않는다
- 관찰 조건: 선택된 부품의 모양·접합·겹침 경계가 해당 코트 위에 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html), [S19: Gloverall](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. a storm flap overlaps the declared trench coat's upper front panel
2. a narrow epaulette anchors along the declared coat shoulder while its belt remains a separate waist fastening

## WF30 — 스카프 코트·탈착·별도 스카프 (P0)

붙은 스카프, 탈착식, 코트와 별개로 두른 스카프를 제품·요청 문맥으로 분리한다. 넥워머 통 구조와도 다르다

- 소유자: 이미 선언된 코트와 그 스카프 부분의 접합·끝단
- 관계 예: `declared_scarf_panel → joined_at → declared_coat_neckline`. 부착 변형에 한정; 별개 스카프 변형과 섞지 않음
- 속성 후보 풀: details.scarf_attachment, layers.scarf_route. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 목에 긴 천이 있다고 코트 부착을 PASS하지 않는다; 상품 예의 자수·색·브랜드를 필수 기본값으로 만들지 않는다
- 관찰 조건: 접합부 또는 분리 경계가 보이며 스카프의 연속 경로·끝단이 같은 물체로 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S31: BUFF](https://www.buff.com/blog/en/neck-head-clothing-accessories/what-is-neck-gaiter/), [S38: TOTEME](https://toteme.com/products/embroidered-scarf-coat-black)

각각 독립된 선택형 문장 초안:

1. a scarf panel is visibly joined to the declared coat neckline and wraps around the same wearer's neck
2. a separate scarf lies over the declared coat with its own free ends and independent fabric boundary

## WF31 — 크롭·롱·벨티드 푸퍼 (P0)

부푼 구획, 짧음·김, 허리의 벨트 조임은 독립 축이다. 크롭 푸퍼만으로 배꼽이 보이거나 하의를 로라이즈로 바꾸지 않는다

- 소유자: 선택한 충전 외투의 구획·밑단·벨트와 착용자 기준점
- 관계 예: `declared_puffer_belt → locally_narrows → declared_puffer_waist`. 같은 외투; 길이·노출·충전 원료를 독립 유지
- 속성 후보 풀: structure.visible_chambers, length.hem_landmark, closure.belt_route. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: down 원료·노출·날씨를 자동 추가하지 않는다; 벨트 장식만으로 겉의 구획이 실제 조여졌다고 판정하지 않는다
- 관찰 조건: 같은 외투의 부풀음·밑단 또는 벨트가 선택된 범위에서 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html), [S03: REI](https://www.rei.com/learn/expert-advice/what-is-down-fill-power.html), [S04: Rab](https://rab.equipment/eu/rab-lab/down-jackets-buying-guide)

각각 독립된 선택형 문장 초안:

1. the declared puffer hem ends near the same wearer's waist above the existing lower garment
2. a belt locally narrows the declared puffer's waist while its inflated chambers remain visible above and below

## WF32 — 파카·피시테일·아노락 (P0)

후드 외투 범주, 뒤쪽 갈라진 피시테일, 풀오버·부분 지퍼 아노락 변형을 분리한다. 역사·현대 명칭 범위는 별도다

- 소유자: 해당 외투의 후드·뒤 밑단·앞 개구부
- 관계 예: `declared_rear_hem → splits_into → declared_left_right_tail_points`. 같은 파카 뒤면; 정면만으로 판정 금지
- 속성 후보 풀: structure.hood_attachment, length.rear_split, closure.front_access. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 생선 꼬리 몸체·항상 군복·항상 방수로 바꾸지 않는다; 정면만으로 뒤 밑단 트임을 PASS하지 않는다
- 관찰 조건: 뒤 밑단의 두 갈라진 끝 또는 앞 부분 개구부·후드 접합을 해당 구도에서 검사
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html), [S20: FIT Fashion History Timeline](https://fashionhistory.fitnyc.edu/anorak/), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. the declared parka's rear hem divides into two tail-like points
2. the declared hooded pullover has a short front zipper that ends above its lower torso panel

## WF33 — 퀼티드 라이너·플리스 재킷·질레 (P1)

라이너는 다른 옷 안의 역할과 단독 착용 가능성을 가진다. 질레는 민소매 겉옷이며 소재·충전재가 고정되지 않는다

- 소유자: 이미 선언된 라이너·외투·민소매 겉층의 경계
- 관계 예: `declared_sleeveless_outer_armhole → frames → declared_inner_sleeve`. 같은 착용자의 서로 다른 겉층·이너
- 속성 후보 풀: layers.role, structure.sleeve_presence, surface.stitched_relief. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 누빔을 다운으로, 질레를 니트 베스트로 자동 고정하지 않는다; 소매가 잘려 보이는 크롭을 민소매 증거로 삼지 않는다
- 관찰 조건: 암홀의 닫힌 가장자리·다른층 소매·누빔 또는 보송한 면이 같은 의복에서 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S01: Patagonia](https://www.patagonia.com/guides/cold-weather-layering/), [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html), [S09: Patagonia](https://www.patagonia.com/product/mens-retro-pile-fleece-jacket/22802.html)

각각 독립된 선택형 문장 초안:

1. the declared sleeveless outer layer has finished armhole edges over the existing long-sleeved inner layer
2. a shallow quilted liner remains visibly separate beneath the declared open outer coat

## WF34 — 보머·바이커·바시티·셔킷 (P1)

보머의 시보리, 바이커의 비대칭 지퍼, 바시티의 몸판·소매 배색, 셔킷의 셔츠형 칼라·앞열은 다른 선택 구성이다

- 소유자: 선택한 재킷의 몸판·소매·시보리·앞여밈
- 관계 예: `declared_ribbed_cuff → gathers → declared_jacket_sleeve_edge`. 같은 소매의 끝; 재킷 종류의 다른 부품은 별도 변형
- 속성 후보 풀: details.cuff_hem_finish, closure.front_geometry, details.panel_contrast. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 보머 이름으로 둥근 몸통·항공기, 바이커로 폭력·차량, 바시티로 나이·학교·특정 로고를 강제하지 않는다
- 관찰 조건: 소매와 몸판의 연결·마감 또는 선택된 지퍼의 양끝이 실제로 읽혀야 한다
- 기존 ID 검토: clt_ct010_v1
- 근거: [S19: Gloverall](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat), [S24: YKK Americas](https://ykkamericas.com/what-kind-of-two-way-zipper-do-i-need/), [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. ribbed cuffs and a ribbed hem gather the edges of the declared short jacket
2. an asymmetric zipper crosses the declared jacket front between its own lapel and lower fastening

## WF35 — 시어링·에비에이터·페니 레인 코트 (P1)

양면 소재, 항공복풍 큰 칼라·버클, 복고풍 털 트림을 별도 관계로 만든다. 명칭의 겹침은 선택한 부품으로 해결한다

- 소유자: 해당 외투의 몸판·털 칼라·커프·목버클
- 관계 예: `declared_collar_buckle → joins → declared_two_collar_tabs`. 같은 외투 칼라의 실제 탭 끝점
- 속성 후보 풀: surface.body_texture, trim.location, closure.collar_buckle. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 무스탕을 말이나 자동차로, 에비에이터를 조종사 직업으로, 페니 레인을 인물·장소·코스튬 동일성으로 강제하지 않는다
- 관찰 조건: 몸판과 칼라·트림의 경계, 버클이 연결하는 두 탭이 같은 옷에 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S08: UGG](https://www.ugg.com/ca/help-center.html?a=Information-on-UGG%28r%29-and-Our-Brand---id--J6cPk4gJT4aqfLYPB4K1ig), [S19: Gloverall](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. a broad woolly collar contrasts with the declared jacket's smooth body panel
2. a buckle joins the two collar tabs of the declared aviator-inspired jacket

## WF36 — 풀오버·가디건과 길이·랩 (P0)

풀오버의 몸판 연속, 가디건의 전면 개방, 크롭·롱라인 길이, 교차 랩을 독립 축으로 작성한다

- 소유자: 해당 니트 상의의 앞판·여밈·밑단
- 관계 예: `declared_wrap_front_A → crosses_over → declared_wrap_front_B`. 같은 가디건 앞판; 옆 허리 고정점은 별도 노드로 승격
- 속성 후보 풀: closure.front_access, length.hem_landmark, closure.wrap_overlap. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 단추 프린트와 실제 개방 전면을 구분한다; 짧음만으로 노출·긴 상의만으로 드레스 착용을 강제하지 않는다
- 관찰 조건: 앞판의 개구 경계·교차 겹침·밑단이 선택된 형태대로 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas)

각각 독립된 선택형 문장 초안:

1. the declared cardigan has two separate front edges joined by its own button fastening
2. the declared wrap knit has crossing front panels secured by a tie at its own side waist

## WF37 — 트윈세트·니트 폴로·하프집·집스루 (P1)

세트의 두 벌 관계와 한 벌의 짧은 여밈·전면 지퍼 길이를 분리한다. 세트는 같거나 조율된 외관을 명시할 때만 평가한다

- 소유자: 같은 착용자의 두 니트 또는 한 니트의 칼라·지퍼
- 관계 예: `declared_front_zipper → extends_from_neckline_to → declared_knit_hem`. 같은 니트; 하프집과 집스루를 대안으로 분리
- 속성 후보 풀: layers.set_relation, details.collar, closure.zipper_extent. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 한 벌을 두 벌로 세거나 보이지 않는 민소매 이너를 추정하지 않는다; 두 슬라이더와 전체 전면 지퍼는 별개다
- 관찰 조건: 두 벌의 가장자리·칼라·지퍼가 끝나는 위치가 보이고 각각 같은 의복에 붙어 있어야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S24: YKK Americas](https://ykkamericas.com/what-kind-of-two-way-zipper-do-i-need/), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas)

각각 독립된 선택형 문장 초안:

1. the declared knit polo has a collar and a short fastening ending on its upper chest panel
2. the declared knit cardigan's zipper continues from its neckline to its lower hem

## WF38 — 튜닉·볼레로·슈러그 (P1)

긴 튜닉의 밑단, 짧은 몸판을 가진 볼레로, 어깨·팔 중심 슈러그의 피복 구역을 분리한다. 상품 경계가 겹치면 구체 형태가 우선이다

- 소유자: 해당 상의·짧은 덧옷·그 아래 선언된 의복
- 관계 예: `declared_shrug_edge → leaves_visible → declared_inner_torso_garment`. 별개 덧옷과 이너 경계; 신체 피복 임의 수정 금지
- 속성 후보 풀: length.hem_landmark, layers.coverage_region. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 모든 슈러그를 브라렛·맨몸과 결합하지 않는다; 한쪽 팔만 보인다고 무봉제 연속 소매라고 추정하지 않는다
- 관찰 조건: 어깨와 양팔 덧층의 끝단, 몸통의 열린 영역에 실제로 무엇이 있는지가 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas)

각각 독립된 선택형 문장 초안:

1. the declared shrug covers the shoulders and arms while leaving the separate inner torso garment visible
2. the declared tunic knit ends over the upper thighs of the same wearer

## WF39 — 민소매 터틀넥·니트 브라렛·보디수트 (P0)

목 피복·소매 부재·짧은 니트 상의·일체형 몸통 연결은 다른 축이다. 보디수트의 하부 연결은 안보이면 명세로 보존한다

- 소유자: 선택한 상의의 목·암홀·몸통 및 필요한 연결부
- 관계 예: `declared_high_neck_panel → connected_to → declared_sleeveless_bodice`. 같은 상의; 암홀 가시 상태는 별도 관계
- 속성 후보 풀: structure.neck_coverage, structure.arm_openings, structure.torso_continuity. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 높은 목을 소매 있음으로, 민소매를 겨드랑이 맨살로, 보디수트를 긴 다리 캣수트로 자동 확정하지 않는다
- 관찰 조건: 암홀의 실제 경계와 그 안쪽 층을 검사; 숨은 하부 연결은 일반 상의 사진에서 UNSCORED
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S11: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas)

각각 독립된 선택형 문장 초안:

1. the declared sleeveless knit has a high neck collar and two finished armholes
2. the declared short knit top retains visible knitted fabric and its own bounded lower edge

## WF40 — 터틀·모크·퍼널·카울넥 (P0)

접어 내린 높은 칼라, 낮은 미접힘 모크, 위로 넓어지는 퍼널, 앞으로 처진 카울의 선택 형태를 구분한다. 높이는 제품별로 달라진다

- 소유자: 한 상의의 목둘레 패널·접힘·목 기준점
- 관계 예: `declared_collar_upper_panel → folds_down_over → same_collar_lower_panel`. 터틀 접힘 변형에 한정; 모크·카울은 다른 노드
- 속성 후보 풀: neckline.collar_height, neckline.fold_geometry. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 카울을 스카프·가슴 노출의 자동값으로, 높음만으로 모두 터틀넥으로 합치지 않는다
- 관찰 조건: 칼라 접힘의 두 겹·개구 폭·앞쪽 처짐이 같은 목패널에 연결되어 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S23: Seamwork](https://www.seamwork.com/sewing-patterns/all-about-the-ace-top), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared top has a high collar visibly folded down onto itself
2. extra fabric from the declared neckline hangs forward in a soft cowl fold

## WF41 — 크루·V·딥V·스쿠프·스퀘어·하트·보트 (P0)

곡선·각·가로폭·최저점의 상대 위치로 목선 변형을 작성한다. sweetheart의 두 곡선과 central dip, boat의 넓고 얕은 형태는 독립이다

- 소유자: 해당 상의의 좌우 목선과 앞중심 최저점
- 관계 예: `declared_neckline_lower_edge → meets_at_angle → declared_neckline_side_edge`. 같은 스퀘어 목선; 깊이·피부 가시는 독립
- 속성 후보 풀: neckline.edge_shape, neckline.width, neckline.depth. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: square·boat·deep 이름만으로 가슴 노출이나 정확한 깊이를 강제하지 않는다; 목선 형태와 옷의 밀착은 별도다
- 관찰 조건: 선택된 좌우 경계·앞중심의 모양을 읽을 수 있어야 하며 스카프 가림은 미관찰
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared square neckline has a level lower edge meeting two more upright side edges
2. the declared sweetheart neckline forms two upper curves separated by a central dip
3. the declared boat neckline runs wide and shallow across the upper chest

## WF42 — 오프숄더·콜드숄더·원숄더·홀터·스트랩리스 (P0)

어깨 아래 상단, 남은 어깨 연결부의 국소 구멍, 한쪽 지지, 목 뒤 끈, 어깨끈 없는 몸통을 다른 구조로 분리한다. bandeau는 가로 띠 외형이다

- 소유자: 해당 상의 상단·어깨 지지·소매 시작·목끈
- 관계 예: `declared_offshoulder_upper_edge → lies_below → same_wearer_two_shoulders`. 같은 상의·착용자; 겨드랑이·등의 맨살 자동 추가 금지
- 속성 후보 풀: structure.shoulder_support, coverage.shoulder_region. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 오프숄더를 겨드랑이·등 개방의 자동값으로 만들지 않는다; 원숄더 방향·홀터 경로를 미확정으로 합치지 않는다
- 관찰 조건: 지지 또는 단절 경계·양쪽 어깨와 소매의 시작점이 선택된 형태대로 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared off-shoulder top's upper edge lies below both shoulders while its sleeves remain around the upper arms
2. the declared cold-shoulder top retains shoulder bridges above bounded shoulder openings
3. the declared halter top's straps connect its front panel around the back of the same wearer's neck

## WF43 — 키홀·서플리스·일루전 목선 (P0)

작은 경계 닫힌 구멍, 교차해 만든 V, 피부색·시어 패널이 실제 연결하는 구조를 분리한다

- 소유자: 해당 목선의 개구·교차 앞판·망사 연결부
- 관계 예: `declared_illusion_mesh → bridges → declared_neckline_boundary`. 실제 직물면·경계가 보이는 피복 구조
- 속성 후보 풀: neckline.keyhole, closure.surplice_overlap, layers.illusion_mesh. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 피부색은 빈 공간 증거가 아니다; surplice를 실제 허리 랩 여밈과 완전히 동의어로 만들지 않는다
- 관찰 조건: 망사는 가장자리·그 위 장식·직물 결 중 적어도 실체 단서가 보일 때 피복으로 판정
- 기존 ID 검토: clt_ct079_v1
- 근거: [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. a bounded keyhole opening sits below the declared top's connected neckline
2. a fine mesh panel visibly bridges the declared neckline opening with its own fabric edge

## WF44 — 피티드·슬림·보디콘·세컨드스킨 (P0)

핏은 부위별 접촉·비접촉·처짐 분포로 표현한다. 얇고 밀착된 외관과 몸의 크기·노출·비침은 독립이다

- 소유자: 선택한 의복 원단과 같은 착용자의 윤곽
- 관계 예: `declared_knit_fabric → follows_with_selected_contact → same_wearer_torso_contour`. 이미 고정된 신체를 유지; 지역 접촉만 효과
- 속성 후보 풀: fit.contact_regions, fit.visible_clearance. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 몸을 새 체형으로 바꾸거나 모든 bodycon을 불투명·시어·노출로 고정하지 않는다; 압박 수치를 밀착으로 증명하지 않는다
- 관찰 조건: 선택한 지역의 연속 직물면과 윤곽·주름을 검사하며 아래 피부 구조를 과도하게 새로 부여하지 않는다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S11: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

각각 독립된 선택형 문장 초안:

1. the declared knit follows the existing torso contour with small bending folds at the waist
2. the declared top retains a narrow visible clearance from the same torso at its side seam

## WF45 — 허리 조임·코르셋·컵·언더버스트 (P0)

허리의 국소 수축, 컵 솔기, 보닝 케이싱, 코르셋풍 상의, 가슴 아래 별개 의복을 분리한다. hourglass는 옷의 외곽으로도 실현된다

- 소유자: 해당 옷의 허리 구역·컵·패널·보닝 케이싱·여밈
- 관계 예: `declared_underbust_waist_garment → lies_over → declared_continuous_inner_top`. 별개 의복 두 벌; 가슴 아래 끝 위치는 따로 결속
- 속성 후보 풀: structure.cup_boundary, structure.visible_boning_channels, fit.waist_gathering. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: underbust를 underboob 노출과 합치지 않는다; 보이는 케이싱을 내부 철재·압력·몸 수정 증거로 삼지 않는다
- 관찰 조건: 별개 상의와 허리 의복의 경계, 컵 곡선 또는 선택한 케이싱 연결이 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared underbust waist garment ends below the bust over a separate continuous inner top
2. curved cup seams and narrow vertical casing lines remain visible on the declared corset-style bodice

## WF46 — 프린세스 심·다트·루싱·스모킹·페플럼 (P1)

연결된 곡선 패널, 짧게 끝나는 다트, 한 선에 모인 주름, 장식 스티치로 묶인 작은 주름, 허리의 별도 퍼지는 단을 구분한다. 드레이프는 흘러내리는 원단 관계다

- 소유자: 한 의복의 절개선·주름 고정점·짧은 덧단
- 관계 예: `declared_curved_shaping_seam → joins → declared_bodice_panels`. 같은 몸판 패널; 단순 선 장식과 실제 연결 분리
- 속성 후보 풀: structure.shaping_seams, details.gather_anchor, details.peplum_attachment. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: princess를 인물 역할로, dart를 시선 행동으로, 스모킹을 단순 셔링·인쇄선으로 합치지 않는다
- 관찰 조건: 선·끝점·고정된 주름·덧단의 부착선이 같은 의복에서 실제로 보여야 한다
- 기존 ID 검토: clt_ct031_v2, clt_ct064_v2, sff_pro_c01
- 근거: [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/)

각각 독립된 선택형 문장 초안:

1. a curved seam joins the declared bodice panels from the upper garment through its bust region
2. a short tapered dart ends near the bust on the declared bodice
3. a short flaring peplum joins the declared garment at its waist seam

## WF47 — 크롭·미드리프·배꼽의 두 경계 (P0)

크롭은 상의 길이, midriff는 실제 복부 구역, navel-baring은 실제 배꼽 가시 상태다. 하의 높이·이너·외투 가림으로 결과가 달라진다

- 소유자: 같은 착용자의 상의 밑단·하의 허리단·배꼽 및 이너
- 관계 예: `declared_top_hem → spaced_above → declared_lower_waistband`. 같은 착용자 두 의복; 구간의 실제 표면은 별도 판정
- 속성 후보 풀: length.top_hem, coverage.torso_interval. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 크롭+하이라이즈를 무조건 배꼽 노출로 만들지 않는다; underbust 길이와 노출 위치를 이름만으로 합치지 않는다
- 관찰 조건: 상의 밑단과 하의 허리단 사이 실제 표면을 읽고 배꼽 의무는 그 기준점이 보일 때만 검사
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S28: Calzedonia](https://www.calzedonia.com/us/product/sheer_thermal_tights-MODC1919.html), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared cropped top ends above the existing lower garment's waistband with a visible interval between them
2. the existing high waistband reaches the declared cropped top hem and leaves no bare torso interval

## WF48 — 가슴·허리·옆구리·언더버스트 컷아웃 (P0)

컷아웃은 위치·범위·테두리·남은 연결 원단의 개구 구조다. 복부·허리·가슴 아래라는 위치와 실제 보이는 신체 표면은 분리한다

- 소유자: 해당 의복의 절개 테두리·연결 원단과 그 아래 선언된 층
- 관계 예: `declared_cutout_boundary → surrounds_opening_in → declared_dress_panel`. 하나의 드레스에 남은 연결 원단 보존
- 속성 후보 풀: coverage.cutout_location, structure.cutout_boundary. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 구멍 프린트·주름 그림자·피부색 패널로 빈 개구를 대체하지 않는다; 가슴 아래 위치가 underboob를 자동 의미하지 않는다
- 관찰 조건: 둘러싸인 경계·연속 의복·그 아래 표면이 읽혀야 한다; 추가 노출은 요청·선택 조건에만 결속
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/), [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

각각 독립된 선택형 문장 초안:

1. a bounded side-waist opening interrupts only the declared dress panel while connecting fabric remains above and below
2. the declared underbust opening reveals the existing opaque inner layer beneath its bounded edge

## WF49 — 오픈백·백리스·딥 암홀 (P0)

열린 등판 크기·남은 연결끈·목 피복과 암홀 깊이를 독립 처리한다. 높은 목·긴소매와 등 개방은 양립한다

- 소유자: 해당 상의의 등판 개구·암홀과 동일 착용자의 등·팔
- 관계 예: `declared_armhole_lower_edge → ends_below → same_wearer_underarm_landmark`. 암홀 위치만; 이너·포즈·노출 상태 임의 변경 금지
- 속성 후보 풀: coverage.back_region, structure.armhole_depth. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 민소매만으로 겨드랑이 맨살을 단정하지 않는다; 정면 하이넥만으로 등 개방이나 폐쇄를 판정하지 않는다
- 관찰 조건: 암홀 하부 또는 등 테두리·연결부가 실제 보이는 방향에서 검사
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared long-sleeved high-neck dress retains a bounded open back with visible connecting fabric at its upper edge
2. the declared sleeveless top's armhole extends below the same wearer's underarm and reveals the declared inner layer

## WF50 — sideboob·underboob의 관찰 범위 (P1)

두 용어는 특정 옷 이름이 아니라 옆·아래 부분이 보이는 상태다. 의복 구조·명시 요청·실제 가시 경계로 제한한다

- 소유자: 명시된 성인 착용자의 의복 가장자리와 해당 가슴 측면·하부
- 관계 예: `declared_adult_garment_edge → leaves_requested_region_visible → same_adult_bust_region`. 명시된 성인 부위·옷의 경계만; 직접 용어 출처 추가 확인
- 속성 후보 풀: coverage.bust_side, coverage.bust_lower_edge. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: underbust corset·복부 컷아웃·deep armhole이라는 이름만으로 상태를 활성화하지 않는다; 원료·핏·성행동과 합치지 않는다
- 관찰 조건: 정확한 의복 가장자리·해당 성인 부위·가림 상태가 함께 읽혀야 하며 직접 용어 출처 검증은 승격 전 추가 필요
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared adult garment's side edge leaves the explicitly requested lateral bust region visible
2. the declared adult top's lower edge leaves only the explicitly requested lower-bust region visible

## WF51 — 타이프런트·스플릿·투웨이 지퍼 (P0)

끈의 고정, 전면 분기, 양방향 작동 구조, 현재 어느 구간이 열렸는지를 각각 기록한다. 구조 보유가 개방 상태를 자동 뜻하지 않는다

- 소유자: 같은 상의의 두 앞판·매듭·지퍼 슬라이더·치형
- 관계 예: `declared_lower_zip_slider → bounds_closed_above_and_open_below → declared_zip_teeth_segments`. 같은 여밈; 일반 두 슬라이더 구조와 현재 개방 분리
- 속성 후보 풀: closure.tie_anchor, closure.front_split, closure.lower_zip_state. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 끈 장식을 실제 묶음으로, 두 슬라이더를 아래 개방으로, 개방을 맨살 노출로 자동 판정하지 않는다
- 관찰 조건: 매듭·양 부착점 또는 두 슬라이더와 닫힌·열린 치형 구간이 같은 여밈에 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S24: YKK Americas](https://ykkamericas.com/what-kind-of-two-way-zipper-do-i-need/), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared cardigan's front ties form a knot linking its two front panels
2. the declared two-way zipper is closed above its lower slider while the panels separate below that slider

## WF52 — 시어·피카부·일루전·실제 아래층 (P0)

비침은 원단을 통과해 보이는 아래층, 피카부는 틈·겹의 부분 가시 효과, 일루전은 실제 피복과 피부색 인상을 구분한다

- 소유자: 해당 겉패널·틈·그 뒤의 피부 또는 선언된 이너
- 관계 예: `declared_sheer_outer_panel → transmits_view_of → declared_separate_opaque_inner_panel`. 같은 착용자의 실제 두층; 맨살과 혼동 금지
- 속성 후보 풀: surface.transmission, layers.underlayer_identity. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 피부색 원단·검은 타이츠·이너를 맨살로 잘못 분류하지 않는다; 시어 외층 아래 불투명 이너를 삭제하지 않는다
- 관찰 조건: 겉원단의 실체와 아래층의 경계가 같이 보여야 한다; 색만으로 아래층 정체를 추론하지 않는다
- 기존 ID 검토: clt_ct079_v1, clt_ct079_v2
- 근거: [S18: UNIQLO](https://www.uniqlo.com/sg/en/products/E487121-000/00), [S27: Wolford](https://www.wolford.com/en-ca/our-tights-guide.html), [S28: Calzedonia](https://www.calzedonia.com/us/product/sheer_thermal_tights-MODC1919.html), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared sheer outer panel reveals a separate continuous opaque inner panel
2. a small opening between the declared overlapping panels reveals only the existing inner garment

## WF53 — 겨울 드레스의 재료·구조 조합 (P1)

스웨터·리브·보디콘은 원피스 재료·표면·핏이고 랩·슬립·블레이저·피나포어·코르셋은 서로 다른 구조다. 오프숄더·컷아웃은 별도 지역 변형이다

- 소유자: 선택한 드레스의 몸판·목선·어깨끈·솔기·밑단
- 관계 예: `declared_dress_torso_panel → continues_into → declared_dress_skirt_panel`. 같은 드레스; 별개 블레이저+하의로 대체 금지
- 속성 후보 풀: type.dress, structure.panel_continuity, surface.selected_knit. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 블레이저와 하의가 따로인 착장을 블레이저 드레스로, 피나포어를 앞치마로, 슬립을 시어·속옷 노출로 자동 대체하지 않는다
- 관찰 조건: 선택된 드레스 몸판·하부의 연속, 라펠·끈·겹침 등 구별 부품이 같은 옷에 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared knit dress retains continuous knitted fabric from its torso into its skirt
2. the declared pinafore dress remains a separate sleeveless layer over the existing high-neck top

## WF54 — 스커트 길이·펜슬·A라인·플리츠·머메이드 (P1)

미니·미디·맥시는 몸 기준점 길이, 펜슬·A라인·머메이드는 폭 분포, 플리츠는 접힌 면이다. 같은 치마에 독립 조합이 가능하다

- 소유자: 한 스커트의 허리·힙·하부·반복 접힘·끝단
- 관계 예: `declared_skirt_outer_contour → widens_from_waist_to → declared_skirt_hem`. 같은 치마; 길이·접힘·트임은 독립
- 속성 후보 풀: length.hem_landmark, silhouette.lower_width, details.pleat_folds. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 마이크로 미니에 통일 센티미터를 부여하지 않는다; 플리츠 프린트·그림자와 실제 반복 접힘을 구분하며 머메이드를 신화로 읽지 않는다
- 관찰 조건: 밑단·필요 기준점·선택한 폭 또는 접힘 양면이 원본에서 보인다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/)

각각 독립된 선택형 문장 초안:

1. the declared skirt widens gradually from its waist toward an A-shaped hem
2. repeated folded panels on the declared skirt have readable ridges and recessed returns
3. the declared skirt follows the hips and upper legs before widening in its selected lower region

## WF55 — 슬릿·랩 벌어짐·스코트의 구조 (P0)

트임은 위치·최고점·양 경계, 랩은 겹친 두 패널, 스코트는 치마 겉과 반바지 내부 연결이다. 트임의 보유와 현재 벌어짐을 분리한다

- 소유자: 해당 하의의 트임 양 경계·최고점·랩 겹·안쪽 반바지
- 관계 예: `declared_slit_edge_A → separates_from_below_apex → declared_slit_edge_B`. 같은 치마 트임; 랩 겹침·숨은 반바지와 분리
- 속성 후보 풀: structure.slit_location, structure.slit_apex, structure.inner_short. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 긴 하이슬릿을 짧은 치마로 대체하거나 다리 면을 전부 맨살로 확정하지 않는다; 스코트 내부를 보이지 않는 사진으로 PASS하지 않는다
- 관찰 조건: 트임 양 경계·최고점·실제 안쪽 표면을 검사; 숨은 반바지는 명세로 보존
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. the declared long skirt has a side slit with a visible apex above the knee
2. the declared wrap skirt's overlapping front edge separates from its underlying panel without becoming a sewn slit

## WF56 — 바지의 다리 폭·밑위와 원료 (P1)

와이드·스트레이트·스키니·부츠컷·플레어·배럴은 폭 변화, 하이·로라이즈는 허리단 기준이다. 울은 원료 명세이며 시각 핏과 별개다

- 소유자: 같은 바지의 허리단·허벅지·무릎·발목 구역
- 관계 예: `declared_trouser_knee_region → widens_toward → declared_trouser_hem`. 같은 바지 다리; 부츠·신체 크기 자동 추가 금지
- 속성 후보 풀: fit.leg_width_distribution, fit.waistband_landmark, specification.fiber_identity. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 하이라이즈를 하이레그로, bootcut을 부츠 자동 추가로, 배럴을 모든 벌룬과 동일 숫자 규격으로 합치지 않는다
- 관찰 조건: 같은 양 다리의 폭 변화 및 허리단 기준이 보이며 숨은 밑위 치수는 명세
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/)

각각 독립된 선택형 문장 초안:

1. the declared trousers remain narrow near the knees and widen modestly toward their hems
2. the declared trousers form rounded outer curves around the knees and taper toward the ankles

## WF57 — 울 쇼츠·핫팬츠·레깅스·스티럽·캣수트 (P0)

짧은 하의 길이·밀착, 발 아래 고리, 몸통부터 양 다리까지 이어지는 구조를 분리한다. 원료·투명도·내부 성능은 별도다

- 소유자: 해당 하의의 다리 구역·끝단·발밑 고리·몸통 연결
- 관계 예: `declared_stirrup_loop → passes_beneath → same_wearer_foot`. 같은 레깅스 끝에 붙은 고리; 신발끈·외부 밴드 제외
- 속성 후보 풀: length.leg_hem, structure.stirrup_route, structure.torso_leg_continuity. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 레깅스를 타이츠·발 피복으로, 보디수트를 긴 다리 일체복으로 합치지 않는다; 스티럽 고리를 신발 스트랩으로 대체하지 않는다
- 관찰 조건: 고리는 해당 하의 끝에 붙어 발바닥 아래 이어지고 캣수트 연결은 보이는 패널로 확인
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S30: Charles and Keith](https://www.charleskeith.in/in/guides/types-of-boots.html), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas)

각각 독립된 선택형 문장 초안:

1. the declared leggings' stirrup loops continue from their hems beneath the same wearer's feet
2. the declared catsuit has continuous fabric joining its torso to both long leg sections

## WF58 — 타이츠·비침·데니어의 분리 (P0)

허리부터 발까지 이어지는 타이츠·팬티호즈는 지역 용어 중첩을 남긴다. 시어·세미시어·불투명은 가시 투과, 데니어는 선밀도다

- 소유자: 선택한 레그웨어의 연속 직물면과 아래층
- 관계 예: `declared_hosiery_layer → partially_transmits_view_of → same_wearer_leg_surface`. 실제 직물 가시 경계; 데니어는 명세
- 속성 후보 풀: surface.hosiery_transmission, structure.hosiery_continuity, specification.denier. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 검은색이나 20·50·100 수치로 투과를 보편 확정하지 않는다; 보이는 피부색을 무조건 맨살로 해석하지 않는다
- 관찰 조건: 직물 경계와 실제 아래층·빛 조건을 같이 검사; 데니어는 명세 근거로만 수치 판정
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S27: Wolford](https://www.wolford.com/en-ca/our-tights-guide.html), [S29: Cotton Incorporated CottonWorks](https://cottonworks.com/encyclopedia-item/denier/)

각각 독립된 선택형 문장 초안:

1. the declared hosiery forms a continuous dark textile layer through which the same leg's surface remains partially visible
2. the declared opaque tights conceal the underlying leg surface while retaining their own fabric boundary

## WF59 — 페이크 시어·기모 안층·연결 가장자리 (P0)

피부색 안층 위 어두운 시어 겉층의 인상은 실제 피부 투과와 다르다. 안기모의 보유·실체·보온 성능도 독립이다

- 소유자: 한 타이츠의 시어 겉층·피부색 안층·이중 가장자리
- 관계 예: `declared_dark_sheer_hosiery → lies_over → declared_skin_toned_textile_lining`. 해당 타이츠 두층; 착용자 피부색 수정 금지
- 속성 후보 풀: layers.hosiery_double_layer, layers.lining_color, surface.outer_transmission. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 검은 망 아래 베이지색만으로 피부 노출·피부 정체·기모를 PASS하지 않는다; 임의의 더 밝은 피부로 착용자를 바꾸지 않는다
- 관찰 조건: 접힌 커프·허리단·제품 단면처럼 두 층의 실체가 보일 때 구성만 검사; 일반 착용샷은 숨은 안층 미관찰
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S27: Wolford](https://www.wolford.com/en-ca/our-tights-guide.html), [S28: Calzedonia](https://www.calzedonia.com/us/product/sheer_thermal_tights-MODC1919.html), [S29: Cotton Incorporated CottonWorks](https://cottonworks.com/encyclopedia-item/denier/)

각각 독립된 선택형 문장 초안:

1. the declared hosiery's turned edge reveals a dark sheer outer layer over a separate skin-toned textile lining
2. the declared dark outer hosiery layer transmits the color of its opaque inner lining rather than exposing bare skin

## WF60 — 피시넷·레이스·백심 (P0)

마름모 그물·장식적 레이스 공간·다리 뒤 선의 위치를 다른 속성으로 만든다. 백심은 실제 솔기 또는 장식선일 수 있다

- 소유자: 해당 레그웨어의 그물 교점·레이스 바탕·뒤 세로선
- 관계 예: `declared_mesh_strand_A → joins_at_intersection → declared_mesh_strand_B`. 같은 레그웨어 실제 그물; 프린트·피부 문양 제외
- 속성 후보 풀: surface.mesh_geometry, surface.lace_pattern, details.back_line. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 피시넷 프린트·피부 문신·진짜 상처로 대체하지 않는다; 뒤 선을 항상 제작 솔기로 확정하지 않는다
- 관찰 조건: 그물의 연결 교점과 구멍, 뒤 중심선은 해당 관찰 방향에서 연속으로 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S13: Cotton Incorporated CottonWorks](https://cottonworks.com/learning-hub/knitting/knit-basics/), [S27: Wolford](https://www.wolford.com/en-ca/our-tights-guide.html), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. connected diamond mesh openings repeat across the declared hosiery over the existing opaque layer
2. a narrow continuous line runs down the rear of the declared stocking

## WF61 — 사이하이·홀드업·가터·타이츠 연결 (P0)

별개 두 스타킹과 허리 연속형 타이츠, 자체 고정형 밴드와 벨트 지지끈의 경로를 구분한다. 숨은 실리콘은 명세다

- 소유자: 같은 착용자의 독립 스타킹·상단밴드·벨트·지지끈
- 관계 예: `declared_support_strap_fastener → attached_to → declared_stocking_upper_band`. 같은 착용자의 벨트·끈·밴드를 후속 구체 노드로 연결
- 속성 후보 풀: structure.stocking_top, structure.support_path, structure.waist_continuity. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 허벅지 밴드만으로 허리 지지끈·실리콘을 추정하지 않는다; 끈이 근처에 있다는 이유로 밴드와 연결된 것으로 PASS하지 않는다
- 관찰 조건: 벨트→끈→고정부→같은 스타킹 상단의 실제 끝점이 보여야 한다
- 기존 ID 검토: clt_ct025_v1, clt_ct107_v1, pfe_garter_path_candidate, pfe_garter_path
- 근거: [S27: Wolford](https://www.wolford.com/en-ca/our-tights-guide.html), [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

각각 독립된 선택형 문장 초안:

1. the declared stocking ends in a separate upper-thigh band with no visible waist textile connection
2. the declared waist belt's strap reaches and visibly fastens to that same stocking's upper band

## WF62 — 니삭스·오버니·레그워머 (P0)

양말 높이는 무릎 기준으로, 레그워머는 발을 전부 감싸지 않는 덧통 구조와 별도 아래층으로 구분한다

- 소유자: 같은 착용자의 양말 또는 덧통과 무릎·발목·발
- 관계 예: `declared_legwarmer_lower_edge → ends_around → same_wearer_ankle`. 덧통·양말·타이츠·신발을 별개 소유자로 유지
- 속성 후보 풀: length.legwear_landmark, structure.foot_coverage, layers.legwarmer_route. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 니하이 양말과 니하이 부츠, 레그워머와 일체 레깅스를 합치지 않는다; 높이 명칭에 단일 센티미터를 강제하지 않는다
- 관찰 조건: 양끝과 발 또는 아래층의 경계를 읽어 어느 물체가 발을 덮는지 검사
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S30: Charles and Keith](https://www.charleskeith.in/in/guides/types-of-boots.html), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas)

각각 독립된 선택형 문장 초안:

1. the declared sock ends just below the same wearer's knee while its foot section remains continuous
2. a separate knitted leg warmer ends around the ankle over the existing hosiery and leaves the foot garment distinct

## WF63 — 부츠통 높이와 무릎·허벅지 기준 (P0)

앵클·미드카프·니하이·오버니·사이하이는 착용자 기준점과 끝단 관계로 표현한다. 상품명 사이 겹침은 실제 끝 위치로 해결한다

- 소유자: 해당 부츠의 갑피 끝·발 연결부와 동일 다리 기준
- 관계 예: `declared_boot_upper_edge → ends_relative_to → same_wearer_knee_or_thigh`. 변형마다 기준점 하나 확정; 부츠 발 연결 보존
- 속성 후보 풀: length.boot_shaft_landmark, structure.boot_foot_continuity. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 허벅지 스타킹을 롱부츠로 대체하지 않는다; 부츠통을 늘리려고 다리 길이·포즈를 수정하지 않는다
- 관찰 조건: 갑피가 발로 이어지고 선택한 무릎·허벅지 기준점과 윗단이 같은 다리에서 보인다
- 기존 ID 검토: tall_suede_boots, fishnet_thigh_high_boots
- 근거: [S30: Charles and Keith](https://www.charleskeith.in/in/guides/types-of-boots.html)

각각 독립된 선택형 문장 초안:

1. the declared boot shaft ends below the same wearer's knee
2. the declared boot's upper edge rises above the same knee toward the thigh while remaining continuous with its foot

## WF64 — 삭스·라이딩·첼시·컴뱃·엔지니어 부츠 (P1)

밀착 신축 갑피·낮은 굽 긴 승마풍·측면 탄성패널·레이스업·버클 탭은 별도 구조다. 같은 부츠에 일부 조합이 가능하다

- 소유자: 해당 부츠 갑피·측면 탄성패널·끈·버클·부츠통
- 관계 예: `declared_elastic_gusset → joins_between → declared_front_rear_boot_panels`. 같은 첼시 갑피; 발·관절 변경 없음
- 속성 후보 풀: structure.upper_panel, closure.boot_fastener, silhouette.shaft_fit. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 첼시를 사람·도시, 컴뱃을 전투 행동, 라이딩을 승마 장면으로 강제하지 않는다; sock boot를 양말 한 장으로 대체하지 않는다
- 관찰 조건: 선택한 갑피 부품이 해당 발의 부츠에 연결되고 끈·버클 끝점이 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S30: Charles and Keith](https://www.charleskeith.in/in/guides/types-of-boots.html), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. an elastic side gusset interrupts the declared Chelsea boot's upper between solid front and rear panels
2. a strap and buckle visibly join around the declared engineer-style boot shaft

## WF65 — 플랫폼·러그솔·눈용·슬라우치·폴드오버 (P0)

앞발까지 두꺼운 플랫폼, 깊은 밑창 요철, 눈용 기능 범주, 내려앉는 주름, 접힌 덧단을 각각 기록한다

- 소유자: 같은 부츠의 앞발 밑창·뒤꿈치·요철·접힌 부츠통
- 관계 예: `declared_thick_forefoot_sole → supports → declared_boot_forefoot_upper`. 같은 부츠; 굽만 높은 하이힐과 분리
- 속성 후보 풀: structure.forefoot_platform, structure.sole_lugs, details.shaft_fold. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 하이힐만으로 플랫폼, 러그 요철만으로 방수·빙판 안전·스노 성능을 판정하지 않는다; 슬라우치를 낡음이나 착용 실패 원인으로 확정하지 않는다
- 관찰 조건: 앞발 단면·밑창 바닥·부츠통의 접힘 중 활성화된 부위를 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html), [S30: Charles and Keith](https://www.charleskeith.in/in/guides/types-of-boots.html)

각각 독립된 선택형 문장 초안:

1. the declared boot has a visibly thick sole beneath both the forefoot and heel
2. the declared boot shaft folds outward at its upper edge into a continuous turned cuff
3. the declared boot shaft settles into soft folds above the ankle

## WF66 — 스카프·스톨·숄·블랭킷·스누드 (P0)

길게 늘어진 천·넓은 어깨 덮개·목통의 끝단·고리를 구체적으로 표현한다. 스톨·숄의 상품 경계는 겹칠 수 있으며 스누드는 다의어다

- 소유자: 선택한 목·어깨 액세서리의 폭·끝단·고리와 몸 위 경로
- 관계 예: `declared_stole → drapes_across → same_wearer_shoulders`. 자유 끝단 둘과 천 경로; 목통·후드의 대안과 분리
- 속성 후보 풀: structure.accessory_loop, layers.drape_route, length.accessory_extent. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 스누드를 머리망으로만 고정하거나 넥통을 별개 머플러 끝단으로 바꾸지 않는다; 담요 크기를 모든 스카프에 부여하지 않는다
- 관찰 조건: 천의 연속 경로·자유 끝단 또는 닫힌 고리와 받침 몸 구역이 읽혀야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S31: BUFF](https://www.buff.com/blog/en/neck-head-clothing-accessories/what-is-neck-gaiter/), [S33: FIT Fashion History Timeline](https://fashionhistory.fitnyc.edu/muff/)

각각 독립된 선택형 문장 초안:

1. the declared rectangular stole rests across the shoulders with two independent hanging ends
2. the declared neck warmer forms a continuous textile tube around the neck without scarf-like free ends

## WF67 — 발라클라바·후드 스카프·모자·귀마개 (P0)

머리·목을 잇는 덮개, 후드+자유 스카프 끝, 비니의 밀착 챙 없음, 베레의 납작한 원반, 트래퍼의 귀플랩, 귀 패드 두 개를 분리한다

- 소유자: 같은 착용자의 머리 덮개·얼굴 개구·귀 패드·연결부
- 관계 예: `declared_ear_pad_pair → connected_by → declared_earmuff_band`. 같은 액세서리 두 패드; 모자·머프 혼동 금지
- 속성 후보 풀: coverage.head_face_region, structure.hood_scarf_join, structure.earpad_bridge. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 발라클라바를 범죄 정체성·가면으로, 털 모자를 천연 모피로, 귀마개를 머프로 자동 대체하지 않는다
- 관찰 조건: 덮개 끝과 선택된 얼굴 구멍·플랩·귀 패드 연결이 실제로 보인다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S31: BUFF](https://www.buff.com/blog/en/neck-head-clothing-accessories/what-is-neck-gaiter/), [S33: FIT Fashion History Timeline](https://fashionhistory.fitnyc.edu/muff/)

각각 독립된 선택형 문장 초안:

1. the declared balaclava continuously covers the head and neck around a bounded face opening
2. two distinct pads of the declared earmuffs cover the ears and connect by their own band
3. the declared hooded scarf has a head-covering section joined to two hanging scarf ends

## WF68 — 미튼·핑거리스·오페라·암워머·머프 (P0)

미튼은 엄지와 공용 손가락 공간, 핑거리스는 손끝 개구, 긴 장갑은 팔+손, 암워머는 분리 덧통, 머프는 양손이 들어가는 공용 통으로 구분한다

- 소유자: 해당 손 덮개·엄지 공간·손가락 끝·팔통·양손 머프
- 관계 예: `declared_thumb_chamber → branches_from → declared_common_finger_chamber`. 같은 미튼; 암워머·머프는 별개 변형의 공간 노드
- 속성 후보 풀: structure.finger_compartments, coverage.hand_arm_region, structure.muff_tube. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 엄지가 둘·손가락 분기 오류·팔통이 몸판과 연결되는 오류를 검사한다; 머프와 귀마개는 이름·공간이 다르다
- 관찰 조건: 손가락·엄지 개구·팔 끝 또는 양손이 들어가는 두 입구와 통의 연속성이 보여야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S15: Purl Soho](https://www.purlsoho.com/create/working-into-the-stitch-below/), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas), [S33: FIT Fashion History Timeline](https://fashionhistory.fitnyc.edu/muff/)

각각 독립된 선택형 문장 초안:

1. the declared mitten has a separate thumb section beside one shared finger chamber
2. the declared fingerless glove ends before the fingers' tips while retaining its own wrist section
3. the same wearer's hands enter the two ends of one declared muff

## WF69 — 탈착 칼라·코르셋 벨트·패션 하네스 (P0)

부품이 옷과 별개인지·어떤 구역을 덮는지·무엇에 연결되는지 기록한다. 코르셋풍 벨트의 장식과 실제 지지·압박은 별도다

- 소유자: 선택한 의복 위 별개 칼라·허리띠·연속 스트랩·앵커
- 관계 예: `declared_harness_strap → crosses_over → declared_continuous_clothed_panel`. 별개 스트랩·의복과 명시 앵커; 강제 이벤트 추가 없음
- 속성 후보 풀: layers.accessory_order, closure.accessory_fastener, details.harness_route. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 별개 스트랩을 원피스 솔기로 합치지 않는다; 패션 하네스에 강제·속박·상해·성행동을 자동 부여하지 않는다
- 관찰 조건: 각 스트랩의 연속 경로·교차·앵커·그 아래 연속 의복면이 보인다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. a separate corset-style belt encircles only the waist of the declared outer garment
2. the declared fashion harness forms continuous straps over the existing clothed torso with visible junctions

## WF70 — 소매 연결·볼륨·틈·썸홀 (P0)

드롭숄더·래글런은 연결선, 돌먼·배트윙은 몸판 연속·폭, 퍼프·벌룬·비숍·벨은 볼륨 분포·끝단, 스플릿·썸홀은 개구다

- 소유자: 한 상의의 몸판·소매·연결선·커프·엄지개구
- 관계 예: `declared_thumb → passes_through → declared_sleeve_cuff_opening`. 같은 손·그 손의 소매; 관통 오류·장갑 대체 제외
- 속성 후보 풀: structure.sleeve_attachment, details.sleeve_volume, details.thumb_opening. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 어깨 노출과 드롭숄더를 합치지 않는다; 비숍의 모인 커프와 벨의 열린 끝단을 대체하지 않는다; 썸홀은 장갑 소유가 아니다
- 관찰 조건: 연결선 또는 선택된 커프·구멍에 엄지가 통과하는 경계가 같은 소매에서 보인다
- 기존 ID 검토: thumbhole_cuff_hand_opening
- 근거: [S26: Mood Sewciety](https://blog.moodfabrics.com/all-about-sleeves/), [S15: Purl Soho](https://www.purlsoho.com/create/working-into-the-stitch-below/)

각각 독립된 선택형 문장 초안:

1. the declared sleeve seam lies beyond the same wearer's shoulder tip along the upper arm
2. the declared sleeve gathers into a narrow closed cuff rather than flaring open
3. the same hand's thumb passes through a dedicated opening in the declared extended sleeve cuff

## WF71 — 레이스업·아일릿·프린지·장식석 (P1)

끈이 구멍을 지나는 경로, 자유 끝 프린지, 납작한 시퀸·솟은 장식석·구슬을 각각 분리한다. 반짝임은 부착된 물체와 조명 조건의 관계다

- 소유자: 한 의복 또는 액세서리의 끈·고리·얇은 판·장식석·가장자리
- 관계 예: `declared_lacing_cord → passes_through → declared_opposed_eyelet_rows`. 같은 옷 양 패널·고리; 장식끈만으로 여밈 판정 금지
- 속성 후보 풀: details.lacing_route, details.eyelet, trim.fringe, ornament.surface_attachment. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: lace-up과 lace fabric, 머리 앞머리 fringe, 보케·금속색 잉크를 실제 부착물과 혼동하지 않는다; 보석 진위·가격을 추론하지 않는다
- 관찰 조건: 교차 끈의 양 끝·고리 또는 장식판의 경계·부착 바탕·돌출이 읽혀야 한다
- 기존 ID 검토: clt_ct069_v1, orn_gd39
- 근거: [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. a cord crosses between two eyelet rows anchored on the declared garment panels
2. individual flat sequin plates overlap on the declared fabric surface
3. fine fringe strands attach to the declared scarf edge and terminate in separate free ends

## WF72 — 클래식·미니멀·럭셔리·프레피·아카데미아 (P1)

클래식·미니멀·스칸디·콰이어트·올드머니·프레피·다크 아카데미아는 고정 복장이 아닌 탐색 문맥이다. 기존 요소를 선택형 조합으로 제안한다

- 소유자: 요청에 선언된 의복·색·모티프·장식 밀도의 선택 조합
- 관계 예: `declared_patterned_knit_vest → lies_over → declared_collared_shirt`. 선택형 프레피 조합만; 가족 전체 스타일의 all-of가 아님
- 속성 후보 풀: style.optional_components. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 실제 재산·신분·국적·직업·인물 나이·브랜드를 외관으로 추정하거나 새로 추가하지 않는다; 어두운 색만으로 academia를 확정하지 않는다
- 관찰 조건: 선택된 각 옷과 모티프만 검사하며 스타일 라벨에 보편 all-of 게이트를 붙이지 않는다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S19: Gloverall](https://www.gloverall.com/blogs/journal/duffle-coat-vs-peacoat), [S21: Hainsworth](https://www.hainsworth.co.uk/wp-content/uploads/2018/03/Hainsworth-True-Heritage-Shade-Card.pdf), [S34: Vogue](https://www.vogue.com/article/core-aesthetic-microtrends-2023), [S45: Vogue](https://www.vogue.com/article/from-tiktok-to-depop-fashions-new-trend-funnel)

각각 독립된 선택형 문장 초안:

1. the declared tailoring ensemble combines an existing clean-lined coat with a separate fine-knit layer
2. the declared preppy-inspired ensemble places a patterned knit vest over the existing collared shirt

## WF73 — 아프레 스키·고프코어·테크웨어·애슬레저 (P1)

스키 이후 휴식 문맥, 아웃도어를 일상에 쓰는 조합, 기능풍 부품, 운동·일상 결합을 분리한다. 실제 스포츠·성능은 이름과 별개다

- 소유자: 이미 선언된 셸·보온층·하의·수납·조절 부품
- 관계 예: `declared_fleece_midlayer → lies_beneath → declared_shell`. 선택형 아웃도어 조합만; 성능·장소·날씨 추가 없음
- 속성 후보 풀: style.optional_components, details.visible_adjustment. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 아프레 스키로 스키 장비·산·눈을, 테크웨어로 무기·SF·전체 검정·방수 인증을 자동 추가하지 않는다
- 관찰 조건: 선택된 기능풍 부품·층·조절 경로만 해당 소유자에서 검사
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S01: Patagonia](https://www.patagonia.com/guides/cold-weather-layering/), [S02: REI](https://www.rei.com/learn/expert-advice/insulated-outerwear.html), [S24: YKK Americas](https://ykkamericas.com/what-kind-of-two-way-zipper-do-i-need/), [S30: Charles and Keith](https://www.charleskeith.in/in/guides/types-of-boots.html), [S43: Vogue](https://www.vogue.com/article/apres-ski-style), [S44: GQ interview with Errolson Hugh](https://www.gq.com/story/stealth-in-the-city-nike-taps-erollson-hugh-of-acronym-for-acg-re-launch), [S46: Vogue Business](https://www.vogue.com/article/the-vogue-business-glossary)

각각 독립된 선택형 문장 초안:

1. the declared outdoor-inspired ensemble keeps a visible fleece layer beneath its existing shell
2. visible pocket and adjustment details remain on the declared technical-style outer garment

## WF74 — 발레코어·코케트의 선택 요소 (P1)

발레 연습·무대복의 영향과 로맨틱 장식 요소를 선택 조합으로 다룬다. 리본·레이스는 기존 소유자와 실제 부착점을 갖는다

- 소유자: 선택된 랩 니트·타이츠·리본·레이스·레그워머
- 관계 예: `declared_wrap_knit → lies_over → declared_bodysuit`. 선택형 조합만; 리본·포즈·발레 정체성 자동 추가 없음
- 속성 후보 풀: style.optional_components, ornament.ribbon_attachment. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 발레 기술·전문직·어린 나이·순종적 성격·특정 포즈를 스타일 라벨로 강제하지 않는다; 둘을 완전 동의어로 합치지 않는다
- 관찰 조건: 요청 또는 선택된 레이어·장식만 검사하며 모든 코케트에 같은 색·리본을 필수화하지 않는다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas), [S34: Vogue](https://www.vogue.com/article/core-aesthetic-microtrends-2023), [S35: Vogue](https://www.vogue.com/article/balletcore-a-look-back-at-how-designers-have-been-inspired-by-dance)

각각 독립된 선택형 문장 초안:

1. a separate wrap knit lies over the declared bodysuit while leg warmers remain distinct from the tights
2. a small bow attaches at the declared garment edge with two loops and separate tails

## WF75 — 고딕·펑크·그런지·바이커·유틸리티 (P1)

어두운 장식적 조합, 펑크 하드웨어, 거친 느슨한 옷, 모터사이클풍, 작업·군복 유래 구조는 각각 선택 요소를 가진다. 하위문화와 사건은 별개다

- 소유자: 요청된 의복의 벨벳·레이스·체크·금속·포켓·스트랩
- 관계 예: `declared_stud → attached_to → declared_garment_panel`. 선택된 펑크 장식만; 폭력 사건·신체 상처 추가 없음
- 속성 후보 풀: style.optional_components, details.visible_hardware. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 펑크·밀리터리·하네스라는 이름으로 폭력·무기·범죄·강제·상처를 자동 추가하지 않는다; 그런지를 빈곤·비위생으로 추정하지 않는다
- 관찰 조건: 선택된 장식·마모 외관·수납 부품의 위치를 검사하며 라벨만으로 정체성을 판정하지 않는다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond), [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S40: Cotton Incorporated CottonWorks](https://cottonworks.com/encyclopedia-item/flannel/)

각각 독립된 선택형 문장 초안:

1. the declared punk-inspired garment has visible studs attached to its own panel beside a separate check-pattern layer
2. the declared utility-inspired coat retains bounded patch pockets and readable fastening tabs

## WF76 — Y2K·McBling·몹 와이프의 분기 (P1)

Y2K 미래적 디자인과 McBling 장식적 변형은 이미 있는 의미를 우선 재사용한다. 몹 와이프는 특정 시기 편집 라벨로 풍성한 외투·장식을 조합한다

- 소유자: 선택된 저층 허리선·벨루어·금속 장식·파일 외투의 조합
- 관계 예: `declared_metallic_ornament → attached_to → declared_accessory_backing`. 선택된 McBling 변형만; 모든 Y2K·몹 와이프에 강제하지 않음
- 속성 후보 풀: style.optional_components. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 한 라벨로 로라이즈·배꼽·레오퍼드·금색·천연 모피·혼인·범죄·민족을 모두 강제하지 않는다; 2024 기사로 현재 유행을 주장하지 않는다
- 관찰 조건: 선택된 구성요소는 각각 자기 소유자와 게이트를 유지하며 미감은 제안으로 남긴다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S34: Vogue](https://www.vogue.com/article/core-aesthetic-microtrends-2023), [S36: Vogue](https://www.vogue.com/article/the-mob-wife-look-is-trending-is-it-sustainable), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. the declared McBling-inspired outfit retains its selected velour-like surface and separate reflective ornaments
2. the declared glamorous winter ensemble combines its existing pile coat with separate large metallic accessories

## WF77 — 란제리 드레싱·윈터 글램 (P1)

속옷 유래 의복을 겉으로 스타일링하는 문맥과 벨벳·파일·반짝임·긴장갑의 파티 조합을 다룬다. 겨울 야외·실내 조건은 요청에서 유지한다

- 소유자: 명시된 성인의 브라렛·슬립·코르셋풍 의복과 외투·긴장갑
- 관계 예: `declared_open_coat_panels → frame → declared_separate_corset_style_top`. 선택된 성인 착장만; 실제 가림과 피복 유지
- 속성 후보 풀: style.optional_components, layers.editorial_order. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 라벨만으로 시어·노출·성행동·새 체형을 강제하지 않는다; 코트가 가리면 숨은 이너를 PASS하지 않는다
- 관찰 조건: 선택된 의복·외투의 겹침과 가시 구역만 검사하며 보이지 않는 형태는 미관찰
- 기존 ID 검토: sff_pro_e19
- 근거: [S25: V and A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas), [S37: V and A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

각각 독립된 선택형 문장 초안:

1. the declared open coat frames a separate corset-style top worn over the existing opaque layer
2. long gloves remain a separate arm layer beside the declared sleeveless evening garment

## WF78 — 신체 부위별 색인의 관계 질의 (P0)

부위 색인 15행은 새 의복명이 아니라 의미 검색의 질문이다. 윤곽·맨살·이너 투과·피부색 피복·가림을 목적 부위마다 구분한다

- 소유자: 같은 착용자의 상의·하의·겉옷·레그웨어·부츠와 기준점
- 관계 예: `declared_interval_between_skirt_and_boot → occupied_by → declared_opaque_hosiery`. 같은 다리·세 의복 경계; 구간을 맨살로 재분류 금지
- 속성 후보 풀: coverage.resolved_surface, layers.occlusion_order. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 크롭·미니·민소매·딥V 라벨을 실제 노출과 동치로 만들지 않는다; 바깥 코트·스카프·타이츠가 가리는 사실을 삭제하지 않는다
- 관찰 조건: 각 부위의 상하·옆 경계와 실제 가장 앞 표면을 같은 착용자에서 읽어야 한다
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S01: Patagonia](https://www.patagonia.com/guides/cold-weather-layering/), [S27: Wolford](https://www.wolford.com/en-ca/our-tights-guide.html), [S28: Calzedonia](https://www.calzedonia.com/us/product/sheer_thermal_tights-MODC1919.html), [S30: Charles and Keith](https://www.charleskeith.in/in/guides/types-of-boots.html), [S41: Mood Sewciety](https://blog.moodfabrics.com/all-about-necklines/)

각각 독립된 선택형 문장 초안:

1. between the declared skirt hem and boot top, the existing opaque tights remain the foremost visible layer
2. the declared scarf covers the otherwise wide neckline while that same top remains unchanged

## WF79 — 코디 조합의 동일 소유자·가림 검사 (P0)

원문 10개 코디는 의복·소재·길이·핏·경계의 독립 선택을 보존하는 번들 초안이다. 보이는 속성과 숨은 속성을 분리한다

- 소유자: 선택된 복수 의복과 각 부품의 의복 ID·착용자
- 관계 예: `declared_outer_garment_edges → leave_visible → declared_selected_inner_neckline`. 선택 번들의 가림 관계; 몸·구도·모든 다른 의복 고정
- 속성 후보 풀: layers.owner_bindings, layers.occlusion_order. 선택 변형별로 범위를 다시 좁혀야 한다.
- 혼동 경계: 코트 추가로 이너 의미가 가려진 것을 무시하거나 슬롯 문장을 합쳐 불가능한 한 벌로 만들지 않는다; 조합 이름이 카메라·신체·날씨를 바꾸지 않는다
- 관찰 조건: 원문 요청의 구도·옷을 고정하고 가시 의무를 모두 검사; 가려진 의무는 미관찰 또는 사용자 의도에 따라 별도 진단 장면으로 분리
- 기존 ID 검토: 용어별 표의 긍정 필드 이웃과 별도 의미 동등성 검토 필요
- 근거: [S01: Patagonia](https://www.patagonia.com/guides/cold-weather-layering/), [S22: Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/stretch-freya-sweater-dress), [S24: YKK Americas](https://ykkamericas.com/what-kind-of-two-way-zipper-do-i-need/), [S28: Calzedonia](https://www.calzedonia.com/us/product/sheer_thermal_tights-MODC1919.html), [S30: Charles and Keith](https://www.charleskeith.in/in/guides/types-of-boots.html), [S32: Capezio](https://www.capezio.com/pages/shop-balletcore-outfit-ideas)

각각 독립된 선택형 문장 초안:

1. the declared open coat leaves the selected knit neckline visible without changing either garment
2. the declared skirt hem and hosiery top define one interval on the same leg while each garment retains its own boundary

