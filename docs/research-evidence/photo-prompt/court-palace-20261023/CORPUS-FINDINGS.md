# 기존 후보 의미·조건·효과·binding 대조

원본 20,871개 / binding 15,839개. 지정 어휘 일치 81개 중 19개에 명시 처리 판단을 저술했다. 나머지 일치는 이웃 요소·동음·다른 장르·false positive를 포함한다. 실제 검색·ranking·전수 의미 동등성 조사는 아니다.

| CID | 원본 EN | 처리 | 카드 | 이유 |
|---|---|---|---|---|
| `cand_281b4625d6e0537588ab748e28ec9ef0` | Joseon palace residential zone with layered thresholds courtyard heated rooms and household work areas separated from a public throne hall | reuse | I01, I06 | 조선 궁중 주거의 중첩 문턱·안마당·온돌·작업 구역이 존재한다. 공적 정전이나 성적 하렘으로 의미를 바꾸지 않는다. |
| `cand_412c5d71d396544d9e62f544bd7bf0cb` | empty throne behind the subject | refine_context_claim | J05, K01 | EN/KO는 인물 뒤 빈 왕좌인데 embedding은 succession pressure를 주장한다. 비어 있음은 유지하고 계승 압박은 optional narrative reading으로 분리한다. |
| `cand_89be8a1c4fd95159bbee8c848ed56b58` | a dangui outer jacket has long rounded front and back panels | reuse_refine | B04 | 긴 둥근 당의 앞뒤 자락은 존재한다. KO 표제가 open sides를 강조하지만 EN은 패널 길이·곡선만 적는다. 트임 관계의 명시 여부와 다른 단위의 의존을 확인한다. |
| `cand_2344e8ec30c152788b5adb55fd7f9a85` | a royal embroidered apron over hanbok-inspired maid attire | preserve_fictional_hybrid | K13 | 왕실 자수 앞치마+한복 메이드의 전체 의미를 보존한다. 침방/수방의 실제 궁녀 제복으로 재분류하지 않는다. |
| `cand_174671d01d9755c0a9915cf83f7114d0` | a kimono wraps wearer-left over wearer-right and is secured by an obi | reuse_with_scope | E03 | 착용자 왼쪽 앞판이 오른쪽 위, 오비의 허리 감김이 있다. 안쪽 기모노의 관계를 우치카케 바깥에도 무조건 추가하지 않는다. |
| `cand_e012bd19cf7a560b8182a1d8d00a6529` | royal princess hanbok dress with a delicate tiara | preserve_fictional_hybrid | C05, K13 | 티아라+왕실 공주풍 한복의 창작 대안을 보존한다. 역사형 조선 왕비나 공주의 정본으로 고쳐 쓰지 않는다. 역사/창작의 별도 검색 대비가 필요하다. |
| `cand_d6b51c3007f353d9a8d124dbb4c50edf` | a royal court physician robe | context_defer_specific_history | I06, K02 | royal court physician robe라는 일반 표제만으로 조선 어의/의녀의 품계·관모·도구 고증을 충족했다고 볼 수 없다. |
| `cand_b0ccb6c00f395136b328aba4c0b08e5c` | a wax-sealed envelope with no readable writing | reuse_only_blank_prop | J02, K14 | 읽을 글자 없는 봉투라는 전체 뜻을 보존한다. legible 교지·계보 요청에는 별도 visible_text 후보가 필요하다. 빈 effects를 무제한 변경 허가로 읽지 않는다. |
| `cand_74c968440a0e56b1907e181579c565b4` | a garment repair table returning a Rococo-volume outfit to its wearer after a broken pannier stay is replaced with a reused part and visible mending remains | preserve_complete_repair_scene | F02 | 파니에 수리·재사용 부품·기움질·착용자 인계가 포함된다. 일반 역사복식 파니에만 추출하려고 수선 서사를 제거하지 않는다. |
| `cand_bdc72b86b6975c66818f68a18b9bbfbe` | a material and level transition from courtyard stone or earth to raised timber maru and room threshold | reuse | I01 | 마당-마루-문턱 재료·높이 관계를 재사용할 수 있다. 이 CID만으로 경복궁/특정 의례의 신원을 증명하지 않는다. |
| `cand_e3986086d7c157059e3ac31a714ce2c0` | gaze toward the empty throne | reuse | K01 | 빈 왕좌를 바라보는 시선은 외형으로 활용 가능하다. 시선이 계승권·죽음·야망을 증명한다는 뜻을 추가하지 않는다. |
| `cand_e855260164c15d79b266c9725a770089` | light cuff extensions finish the narrow dangui sleeves | refine_bilingual | B04 | EN은 light cuff extensions이나 KO는 옆이 트인 당의 자락이다. 거들지·소매 끝이라는 구체 뜻을 양 언어와 embedding에 맞춘다. 원래 ID의 다른 조건/효과를 건드리지 않는다. |
| `cand_7b91c180a57a55aea337d17b912573f2` | a fitting where wearer and maker diagnose asymmetrical pannier load, reused stays, exposed seam allowance, and lace tension during movement | preserve_complete_repair_scene | F02 | 착용자와 제작자의 움직임 중 피팅·비대칭 하중·재사용 보강재라는 전체 장면이다. 순수한 궁정 초상과 별도 대안으로 유지한다. |
| `cand_3671de101025584d832f8dc031a5ec61` | bustle back volume | reuse_existing_garment_carrier | F04 | 이미 스커트 뒤라는 owner와 appearance→wardrobe 효과·골반 자체 확대 혼동 경계가 있다. 이 범위를 재사용한다. 후방 내부 받침의 가시 구조가 필요하면 별도 실현을 검토하며 기존 레코드를 신체 보정 대상으로 오인하지 않는다. |
| `cand_de6bae158e86581ebf5e215af9eb6335` | open side slits separate the dangui panels above the chima skirt | reuse | B04 | 옆트임이 당의 패널을 치마 위에서 분리한다는 뜻이 있다. 새 당의라는 중복 CID보다 이 관계를 재사용 검토한다. KO의 세부 구별도 보정 대상이다. |
| `cand_8732ff983ca8590ebb932dfd8c619dbe` | a Moroccan caftan with a long robe body, center-front trim and fastening, and an optional ceremonial belt | preserve_separate_culture | H01 | 모로코 카프탄의 중앙 장식선·여밈·선택적 mdamma가 명시되어 있다. Ottoman kaftan의 공통 번역만으로 alias를 병합하지 않는다. |
| `cand_a3f718e6fe215abba76cd90281a42491` | a distinct stomacher panel tapers downward inside the gown bodice opening | reuse | F05 | 별도 스토머커의 아래로 좁아지는 패널과 가운 앞 opening이 있다. 역사 시기·소재를 추가할 때 이 의미를 삭제하지 않는다. |
| `cand_11f0f0fd765e50ae85e0d5ad684d52a5` | crinoline bell silhouette | reuse_silhouette_separate_hidden_support | F03 | 이미 성인 패션 스커트라는 owner와 wardrobe 효과가 있다. 종 모양 겉 실루엣은 재사용한다. 내부 cage 후프가 필요한 요청은 별도 구조 실현으로 분리하고 기존 의미를 과장하지 않는다. |
| `cand_b5fcefb9b6395f3783778346ce2a081e` | the outer gown bodice edges frame the inserted stomacher panel | reuse | F05 | 겉가운 가장자리가 삽입 패널을 framing하는 관계다. 별도 패널 CID와 중복인지 구성 단위인지 native 원본 계약을 비교한다. |

조건과 효과를 함께 읽은 뒤의 주의점:

- 당의 garment_detail 두 항목의 현재 binding은 human 적합성을 요구하며 product·jewelry·food·wildlife를 거부한다. 당의 attire_context binding은 documentary·craft도 거부한다. standalone 전시 요구에 재사용하려면 catalog 의미와 이 거부 조건의 이유를 먼저 검토한다.
- 파니에의 옷 지지와 body_geometry의 신체 변형을 혼동하지 않는다. 버슬/크리놀린 두 기존 레코드는 이미 wardrobe carrier와 관련 혼동 경계를 보존한다. 내부 받침 구조를 외형만으로 검증하는 식으로 의미를 확대하지 않는다.
- 궁중 주거에는 requires_primary_any_tags=joseon_naemyeongbu_household_context, 마루에는 requires_any_tags=hanok_madang_maru_inside_outside_relation, 파니에 피팅/수리 장면에는 requires_primary_any_tags=punk_rococopunk가 있다. 재사용은 이 조건을 지킨다는 뜻이며 general court 요청을 위해 조건을 삭제하는 뜻이 아니다.
- 기모노 여밈은 wardrobe.details.kimono_wrap_obi를 main_subject에 적용한다. 전시 우치카케나 타인의 옷으로 target을 옮길 때 기존 자격을 승계하지 않는다.
- 81개 snapshot의 record/conditions/effects/provenance/bindings와 canonical hash를 existing-source-mapping.json에 보존했다.
- 원본 후보를 수정하지 않았고 이 처리는 제안이다. 조회 당시 워킹트리 source와 후속 HEAD의 source가 달라질 수 있으므로 실제 구현 전에 rebaseline한다.
