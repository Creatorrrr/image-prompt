# 수영복 키워드 → 시각 의미 설계표

상세 문맥·한계는 research-report.md와 sources.json 참조. 각 행은 구현 전 설계안이며 공식 사전 정의나 검증 완료 프로파일이 아니다.

| ID / 관련어 | 독립 축 | 관찰할 관계 | 혼동 경계 | 필요한 시점 |
|---|---|---|---|---|
| sw_onepiece / one-piece swimsuit, 원피스 수영복, maillot | garment_topology | 상체 패널이 몸통을 지나 하의와 한 의복으로 연결됨 | 드레스 밑단·분리형 상하의·점프수트 바지통으로 대체 | front_three_quarter |
| sw_bikini / bikini, 비키니, two-piece swimwear | garment_topology | 독립된 수영 상의와 하의의 두 의복 경계 | 색이 같다는 이유로 일체형 처리 | front_three_quarter |
| sw_tankini / tankini, 탱키니, blouson tankini, flared tankini | garment_topology | 몸통을 덮는 상의의 자유 밑단과 별도 하의 | 하복부가 가려졌다고 원피스로 단정 | hem_detail |
| sw_swimdress / swim dress, 스윔드레스, skirted swimsuit | garment_topology | 수영복 본체 위로 이어지는 치마 패널과 독립된 치마 밑단 | 일반 비치 드레스·별도 sarong과 혼동 | hem_detail |
| sw_legsuit / legsuit, leg suit, 레그수트 | garment_topology | 몸통과 짧은 두 바지통이 연결된 수영 의복 | 긴소매만 추가하고 다리 구조 누락 | front_full |
| sw_triangle / triangle bikini, 트라이앵글 비키니 | top_shape | 상의 좌우에 구별되는 삼각 패널과 그 꼭짓점 연결 | 목끈만 있고 삼각 패널은 사라짐 | front |
| sw_string / string bikini, 스트링 비키니, side-string | strap_width | 폭이 좁은 끈의 출발점과 연결 또는 매듭 위치 | 무조건 삼각 컵·특정 하의 커버리지로 고정 | detail |
| sw_bandeau / bandeau, 반두, 밴듀 | top_shape | 가로 밴드형 상의 전면을 유지 | bandeau를 모든 끈 없음과 동일시 | front |
| sw_strapless / strapless, 스트랩리스 | strap_topology | 어깨 또는 목으로 올라가는 지지끈 없는 선택형 | 장식끈과 숨은 끈의 존재를 정면만으로 확정 | front_and_back |
| sw_halter / halter, 홀터넥, halter neck | strap_topology | 상의에서 올라오는 끈이 목 뒤로 이어지는 경로 | 등 중앙 X자 경로로 대체 | three_quarter_back |
| sw_bralette / bralette bikini, 브라렛 비키니 | top_shape | 선택한 패널 형태와 언더밴드를 먼저 명시 | 편안함·무와이어를 외관만으로 단정 | front |
| sw_balconette / balconette, 발코넷, demi-cup, 데미컵 | top_shape | 선택한 낮은 컵 윗선·컵 분할·스트랩 부착점 | 두 판매 용어를 단일 정확 규격으로 고정 | front_detail |
| sw_underwire / underwire, 언더와이어, 와이어 비키니 | internal_structure | 외부에 보이는 컵 아래 곡선 채널만 시각 증거로 기록 | 와이어 실물·지지력을 착용 사진에서 증명 | cup_detail |
| sw_longline / longline bikini, 롱라인 비키니 | top_length | 컵 아래 언더밴드가 아래쪽으로 연장됨 | 탱키니의 몸통 길이와 자동 동일화 | front |
| sw_sporttop / sport bikini top, crop-top bikini, tank bikini | top_shape | 선택된 크롭 길이·넓은 어깨끈·전면 패널 구조 | 스포츠브라와 동일 실루엣만으로 용도 증명 | front |
| sw_scoop / scoop neck, 스쿱넥 | neckline | 전면 윗선이 완만한 U자 곡선을 이룸 | 등 파임과 같은 필드로 저장 | front |
| sw_square / square neck, 스퀘어넥 | neckline | 전면 윗선의 수평부와 양쪽 모서리 | U자 윗선으로 대체 | front |
| sw_sweetheart / sweetheart neckline, 스위트하트 | neckline | 좌우 둥근 윗선이 중앙의 얕은 골에서 만남 | 단순 깊은 V로 대체 | front |
| sw_plunge / plunge, deep V-neck, 플런지 | neckline | 깊이와 종료 지점을 명시한 전면 V 개구부 | 허리 컷아웃을 대신 추가 | front |
| sw_highneck / high-neck, 하이넥 | neckline | 전면 윗선이 목 기저 가까이 올라옴 | 긴소매나 등 전체 덮기를 자동 추가 | front |
| sw_oneshoulder / one-shoulder, 원숄더 | strap_topology | 착용자 기준 한쪽 어깨에만 연결되는 구조 | 카메라 좌우 반전·가려진 반대 끈 | front_and_back |
| sw_offshoulder / off-shoulder, 오프숄더 | sleeve_attachment | 양 어깨 아래 팔 위쪽을 지나는 선택된 소매 또는 밴드 | 원숄더로 대체 | front |
| sw_racerback / racerback, 레이서백 | back_topology | 견갑 사이 중앙으로 모이는 등판 또는 끈 구조 | 교차만 하는 X자 두 끈으로 대체 | back |
| sw_crossback / crossback, X-back, 크로스백 | back_topology | 독립된 두 끈이 등을 가로질러 X 교차 후 부착점에 연결 | 중앙 단일 판으로 합쳐짐 | back |
| sw_scoopback / scoop back, U-back, low back, 로우백 | back_opening | 등의 U형 경계와 파임 종료 위치를 선택해 표시 | 앞 네크라인 깊이로 대체 | back |
| sw_vback / V-back, 브이백 | back_opening | V가 개구부인지 끈 경로인지 먼저 특정 | V 개구부와 V형 끈을 무조건 같은 구조로 처리 | back |
| sw_laceup / lace-up back, 레이스업, corset lacing | closure | 두 경계의 여러 연결점을 오가며 조이는 반복 끈 경로 | 단일 X 끈·장식 bow만 추가 | back_detail |
| sw_tieback / tie-back, 타이백 | closure | 등의 두 끈 끝이 실제 매듭에서 만남 | 지퍼·끈 없는 장식 매듭으로 대체 | back_detail |
| sw_keyhole / keyhole back, 키홀, cut-out back | opening | 등의 특정 위치에 경계가 닫힌 개구부 | 등 전체 파임과 동일화 | back |
| sw_straps / spaghetti straps, wide straps, double straps, adjustable straps | strap_detail | 폭·개수·길이조절 슬라이더를 각각 선택 기록 | 이중 끈을 교차끈으로 변경·슬라이더 위치 유실 | detail |
| sw_highrise / high-waisted, high-rise, 하이웨이스트, 하이라이즈 | waist_height | 하의 윗선이 착용자의 허리 부근에 놓임 | 다리 개구부 높이도 함께 변경 | front |
| sw_midlowrise / mid-rise, low-rise, 로우라이즈 | waist_height | 하의 윗선의 위치를 중간 또는 낮은 위치로 명시 | 커버리지 감소·끈 하의로 자동 치환 | front |
| sw_highleg / high-leg, high-cut, 하이레그, 하이컷 | leg_opening | 다리 개구부 옆 경계가 위로 올라가는 절개 | 높은 허리선만으로 충족 | front_three_quarter |
| sw_boyleg / boyleg, boyshort, 보이레그, 보이쇼츠 | leg_length | 짧은 두 바지통의 하단이 허벅지 위쪽을 가로지름 | 브리프 다리 구멍만 넓게 만듦 | front_three_quarter |
| sw_coverage / full coverage, classic, moderate, cheeky, Brazilian, thong | rear_coverage | 후면 패널 경계의 폭과 위치를 선택한 참조에 상대적으로 명시 | 판매 명칭의 엄격한 공통 순서·국적·체형 추론 | back |
| sw_tieside / tie-side bottom, 타이사이드 | side_closure | 좌우 하의 측면 패널 끝이 끈 매듭에서 연결 | 별도 장식 리본·무조건 low-rise | side_detail |
| sw_vfront / V-front, V-cut bottom, 브이컷 하의 | waist_shape | 전면 허리선 중앙이 V로 내려감 | 다리 절개 high-leg와 동일화 | front |
| sw_foldover / fold-over waist, 접어내린 허리밴드 | waist_detail | 허리밴드가 겉으로 접혀 두 겹 가장자리 형성 | 프린트 띠·독립 벨트로 대체 | front_detail |
| sw_skirtbottom / swim skirt, skirted bottom, 스윔스커트 | lower_layer | 별도 수영 하의에 붙은 치마와 그 밑단 | swim dress 전체와 동일시 | hem_detail |
| sw_rashguard / rashguard, rash vest, 래시가드, surf shirt | garment_topology | 독립 상의의 밑단·소매 길이·선택한 여밈 | 긴소매만으로 wetsuit을 판정 | front_full |
| sw_surfsuit / surf suit, 서프수트, long-sleeve swimsuit | garment_topology | 소매와 수영 하의가 몸통에 연결된 일체형 변형 | 분리형 rashguard·필수 neoprene으로 치환 | front_full |
| sw_wetsuit / wetsuit, 웨트수트, fullsuit, steamer | garment_topology | 선택된 팔다리 길이·분할 패널·입구 경로·두께감 | 검은 catsuit·모든 제품의 neoprene 조성 단정 | front_and_back |
| sw_springsuit / springsuit, spring suit, shorty | limb_coverage | 소매 길이와 다리 길이를 별개 값으로 지정 | 모든 springsuit을 반팔 반바지로 고정 | front_full |
| sw_jane / Long Jane, Short Jane | limb_coverage | 민소매 몸통과 선택한 긴 또는 짧은 바지통 | 민소매면 다리도 짧다고 추론 | front_full |
| sw_swimskin / swimskin, swim skin | garment_function | 선택된 얇은 경기용 겉레이어의 봉제선·밑단·여밈 | wetsuit 또는 dive skin 동의어 병합 | front_and_back |
| sw_leggings / swim tights, swim leggings, 수영 레깅스, jammers | leg_length | 별도 하의의 허리밴드와 선택된 무릎 또는 발목 길이 | 두 길이를 동의어 취급·자전거 패드 추가 | front_full |
| sw_boardshorts / boardshorts, 보드쇼츠, swim shorts | garment_topology | 별도 직선 바지통·선택한 밑위·여밈·밑단 | 타이트 jammer 또는 일반 속옷으로 치환 | front_full |
| sw_bodysuit / bodysuit, 바디수트, leotard, 레오타드 | adjacent_garment | 지정된 의복 용도와 외부 경계를 따로 보존 | 수영장 배경만으로 수영복 판정 | front_and_back |
| sw_unitard / unitard, 유니타드, catsuit, 캣수트 | adjacent_garment | 몸통과 다리의 연속성·다리 길이·소매를 따로 지정 | 팔 길이만으로 유니타드 정의·수영 성능 추론 | front_full |
| sw_wrapcover / sarong, pareo, 파레오, 사롱, beach wrap | outer_layer | 독립 천이 허리를 감싸며 겹침·매듭·자유 밑단을 만듦 | 수영복에 붙은 치마로 합침·착용자 문화 정체성 추론 | front_three_quarter |
| sw_coverup / kaftan, caftan, beach tunic, kimono cover-up, robe-style cover-up | outer_layer | 수영복 바깥 별도 의복의 앞섶·소매·밑단 경계 | 상업 kimono 명칭만으로 전통 기모노 구조 부여 | front_full |
| sw_beachshirt / beach shirt, linen shirt, cover-up dress, beach pants, palazzo pants | outer_layer | 선택한 겉옷의 고유 여밈·밑단·실루엣 보존 | 수영복 자체 구조로 흡수 | front_full |
| sw_rib / ribbed, 골지 | surface_topography | 규칙적인 평행 돌출 능선과 골의 국소 음영 | 평면 줄무늬로 대체 | macro |
| sw_crinkle / crinkle, 크링클, seersucker | surface_topography | 선택된 잔요철의 반복 간격과 조직 영역 | 봉제열 셔링·수평 큰 주름과 혼동 | macro |
| sw_terry / terry cloth, 테리, 타월지 | surface_topography | 선택된 루프 또는 파일 표면의 세밀한 경계 | 땀방울·보풀·매끈한 무광면으로 대체 | macro |
| sw_jacquard / jacquard, 자카드 | surface_pattern | 실 또는 편직 구조와 연동된 무늬의 국소 변화 가설 | 프린트와 원거리에서 확실히 구분 가능하다고 단정 | macro |
| sw_crochet / crochet, 크로셰, lace overlay | layered_surface | 실 고리 무늬의 겉층과 선택한 별도 안감의 경계 | 무조건 무안감·물에 못 들어가는 옷으로 판정 | macro_and_hem |
| sw_mesh / mesh panel, 메시, sheer panel, power mesh | panel_optics | 패널 위치·구멍 조직·뒤층·안감 유무를 지정 | 열린 컷아웃으로 대체·내부 power mesh를 노출 패널화 | detail |
| sw_finish / matte technical, glossy stretch, satin-look, metallic, Lurex | surface_finish | 매트 확산·넓은 광택·금속성 반사·점상 반짝임 중 선택 | 광택 하나로 실크·라텍스·젖음 확정 | detail |
| sw_ruched / ruching, 루싱, gathering, 개더 | fabric_manipulation | 선택된 솔기나 끈 위치로 모이는 주름 방향과 종료점 | 원단 전체 crinkle로 대체 | detail |
| sw_shirred / shirring, 셔링, elastic shirring | fabric_manipulation | 여러 평행 봉제열 사이로 잔주름이 모임 | 보이는 봉제열 없이 crinkle만 추가 | detail |
| sw_smocked / smocking, 스모킹 | fabric_manipulation | 선택된 주름과 장식 스티치의 규칙적 연결 | 기계 elastic shirring과 항상 동일시 | macro |
| sw_pleats / pleats, 플리츠 | fabric_manipulation | 방향이 일정한 접힌 주름 능선과 겹침 | 잡아모은 무작위 잔주름으로 대체 | detail |
| sw_ruffle / ruffle, frill, flounce, tiered ruffle | edge_volume | 고정 가장자리와 떨어져 물결치는 자유 가장자리 | scallop 절개선만으로 충족 | detail |
| sw_scallop / scalloped edge, 스캘럽, picot trim | edge_shape | 반복 둥근 가장자리 또는 작은 고리 장식 중 선택 | 프릴의 자유 천 층과 혼동 | detail |
| sw_piping / contrast piping, binding, contrast trim | edge_construction | 솔기 속 돌출 선·가장자리 감싼 띠·단순 대비 띠를 구별 | 모두 평면 색칠로 구현 | macro |
| sw_cutout / cut-out, 컷아웃, waist cut-out | opening | 위치가 특정된 열린 공간의 폐쇄 경계와 남은 연결 패널 | 살색 천·메시 삽입으로 대체 | front_three_quarter |
| sw_wrapfront / wrap-front, 랩프런트 | panel_overlap | 앞판이 비스듬히 포개지며 겹침 가장자리가 이어짐 | 그려진 사선·중앙 꼬임으로 대체 | front |
| sw_twist / twist-front, knot-front, 트위스트, 매듭 앞판 | panel_connection | 중앙의 실제 꼬임 또는 매듭으로 양쪽 천이 수렴 | O-ring 또는 인쇄 무늬로 대체 | front_detail |
| sw_ring / O-ring, ring connector, 링 연결 | hardware | 두 천 또는 끈이 같은 링의 서로 다른 쪽에 물리적으로 연결 | 신체 위에 떠 있는 장신구 | detail |
| sw_belt / belted, buckle, 벨트, 버클 | hardware | 허리를 지나는 별도 띠와 선택한 버클 연결 | 프린트 허리띠·몸통 절개선으로 대체 | front_detail |
| sw_zip / zip-front, back zip, chest zip, 지퍼 수영복 | closure | 지퍼 이빨선·슬라이더·끝점이 특정한 입구 위치에 있음 | 앞 세로 지퍼와 가슴 가로 입구 혼동 | detail |
| sw_print / polka dots, gingham, nautical stripes, floral, animal print, checkerboard, ombre, tie-dye, toile | surface_pattern | 무늬 요소·규모·간격·방향·색 전이를 독립 기록 | 무늬만으로 촬영 연도·섬유·민족 추정 | front_detail |
| sw_wet / wet fabric, water droplets, beaded water, 젖은 수영복 | surface_state | 원단 위 물방울과 젖음 경계를 광택 반사와 별개로 지정 | 젖음에서 자동 투명화·라텍스화·chlorine 성분 추론 | detail |
| sw_internal / molded cups, soft cups, removable pads, shelf bra, boning, fully lined, double-lined | hidden_metadata | 제품 명세 또는 안쪽이 보이는 상품컷에서만 내부 구조 판정 | 정면 착용샷으로 탈착성·안감 겹수 확인 | inside_product_only |
| sw_performance / UPF, chlorine-resistant, quick-drying, four-way stretch, shape retention, anti-pilling, compression, tummy-control | performance_metadata | 명세로 유지하고 필요 시 보이는 패널 구성만 따로 기술 | 성능 수치·편안함·체형 교정의 픽셀 PASS | not_pixel_scoreable |
| sw_fibers / nylon, polyamide, polyester, elastane, spandex, Lycra, neoprene | material_metadata | 소재 명세와 실제 표면 관찰을 분리 | 원료에서 광택·안감·신축률·정확 혼용률을 생성 | not_pixel_scoreable |
| sw_era / bathing costume, 1910s, 1920s, 1930s, 1940s, 1950s, 1960s, 1970s, 1980s, 1990s, Y2K | historical_context | 소장품 단위 연대·구조·소재를 함께 선택 | 시대별 한 가지 룩을 사실로 고정·사진 연대 추정 | reference_specific |
| sw_monokini / monokini, 모노키니 | ambiguous_label | 역사적 1964 의미와 현대 연결형 컷아웃 용례를 먼저 구분 | 현대 상품 요청에 역사적 노출 형태를 자동 도입 | context_required |
| sw_mood / resort chic, Riviera, pin-up, mermaidcore, scuba-inspired, quiet luxury, coquette, bohemian | optional_style | 사용자가 선택한 색·배치·형태 조합의 제안 | 의복 형태·신체·소득·국적·브랜드를 강제 | scene |
| sw_accessories / swim cap, goggles, sun hat, sunglasses, body chain, beach tote, towel, surfboard, snorkel, fins | optional_prop | 물건별 착용·잡음·놓임 관계와 가림 영역 | 장신구를 수영복 구조로 흡수·소품만으로 종목 확정 | scene |
| sw_environment / poolside, infinity pool, beach, lagoon, cabana, yacht deck, underwater studio | optional_location | 배경의 물 표면·건축·지면 관계를 선택 | 수영복만으로 해변 강제·배경만으로 의복 종류 판정 | scene |
