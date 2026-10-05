# 후보 초안과 반영 결정

**71개 후보 초안**은 같은 구조를 재사용하기 위한 저작 단위다. 같은 수의 활성 ID를 자동으로 만들자는 뜻이 아니다. 모든 `target_binding`과 `proposed_property_area`는 현재 runtime의 dimension/target/property로 변환·검증해야 한다. 중립적인 물체와 인물에 착용한 장신구의 owner가 다르다.

## GD01 한 표면에 한정한 촘촘한 장식

의미 단위: GO002, GO013, GX01. 제안 slot: `composition`. 소유 바인딩: `selected_surface`.

**가시 관계:** motifs lie within the selected surface boundary.

**효과:** composition / selected_surface / detail_distribution; appearance / selected_surface / ornament_density.

**채택 조건:** 주변 화면·얼굴까지 채우지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 화면 전체와 한 대상 표면의 점유 범위가 다르다 / 고밀도·규칙성·복잡함은 서로 다른 축 / 호러 바쿠이의 범위가 화면·벽·보석 사이에서 새어 나가지 않게 한다

**근거:** [S08](SOURCES.md), [S51](SOURCES.md).

## GD02 큰 구조와 작은 반복의 밀도 계층

의미 단위: GO001, GO013, GX02. 제안 slot: `composition`. 소유 바인딩: `bound_scene`.

**가시 관계:** large forms contain repeated medium motifs with smaller junctions.

**효과:** composition / bound_scene / scale_hierarchy; setting / bound_scene / existing_surface_details; style / bound_scene / density.

**채택 조건:** 새 인물/사물 증가와 구별. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 미세한 물건 하나의 정교함과 전체 요소의 풍부함을 구별 / 고밀도·규칙성·복잡함은 서로 다른 축 / 미세 노이즈·개수 증가와 크기 계층을 분리

**근거:** [S08](SOURCES.md), [S46](SOURCES.md), [S51](SOURCES.md).

## GD03 적은 사물의 미세 구조

의미 단위: GO014, GO015, GX20. 제안 slot: `prop`. 소유 바인딩: `bound_focal_object`.

**가시 관계:** fine grooves and attachments belong to the existing object.

**효과:** appearance / bound_focal_object / object_detail; material / bound_focal_object / surface_relief.

**채택 조건:** 밀도나 소품 수를 올리지 않음. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 새 사물·장식 추가와 묘사 정밀도를 구별 / 렌더 노이즈·과도한 선명화와 의미 있는 미세 구조를 구별 / 선명한 피부·전체 고해상도·업스케일링이 세공 구조의 증거는 아니다

**근거:** [S12](SOURCES.md), [S14](SOURCES.md), [S31](SOURCES.md), [S52](SOURCES.md), [S53](SOURCES.md).

## GD04 재료별 질감과 광택 분리

의미 단위: GO016, GX15. 제안 slot: `surface_material`. 소유 바인딩: `selected_garment_regions`.

**가시 관계:** adjacent materials retain separate boundaries on one owner.

**효과:** material / selected_garment_regions / fabric_surface; appearance / selected_garment_regions / wardrobe_surface.

**채택 조건:** 몸·옷의 색/재료 잠금 우선. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 모든 소재를 같은 광택으로 처리하는 것과 구별 / 검은 소재를 모두 같은 gloss로 바꾸거나 금속색을 천 전체에 새게 하지 않는다

**근거:** [S14](SOURCES.md), [S17](SOURCES.md), [S19](SOURCES.md).

## GD05 잎 달린 연속 스크롤 띠

의미 단위: GO032, GO034. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_accessory_border`.

**가시 관계:** leaves branch from the scroll stem along the same border.

**효과:** appearance / selected_accessory_border / accessories_jewelry; material / selected_accessory_border / ornament_relief.

**채택 조건:** rinceau를 broad strap으로 바꾸지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 넓은 리본 스트랩워크와 가는 식물 줄기를 구별 / 스크롤의 형태와 filigree라는 금속 기법을 구별

**근거:** [S05](SOURCES.md), [S27](SOURCES.md).

## GD06 아칸서스 잎과 스크롤

의미 단위: GO033, GO034. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_accessory_frame`.

**가시 관계:** deeply lobed leaves curl from a continuous frame.

**효과:** appearance / selected_accessory_frame / accessories_jewelry; material / selected_accessory_frame / carved_or_cast_surface.

**채택 조건:** 잎 윤곽을 보존. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 일반 꽃잎·실제 식물 종 판정과 구별 / 스크롤의 형태와 filigree라는 금속 기법을 구별

**근거:** [S04](SOURCES.md), [S05](SOURCES.md), [S27](SOURCES.md).

## GD07 로카유 카르투슈

의미 단위: GO036, GO040. 제안 slot: `prop`. 소유 바인딩: `bound_frame_object`.

**가시 관계:** unequal shell-like folds enclose one distinct central field.

**효과:** appearance / bound_frame_object / object_frame; material / bound_frame_object / relief.

**채택 조건:** 중앙 문자 내용은 별도. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 정원석·일반 나선·파스텔 팔레트와 구별 / 프레임의 형태와 내부 글자의 내용은 별개

**근거:** [S04](SOURCES.md), [S27](SOURCES.md).

## GD08 오리큘러 테두리

의미 단위: GO024. 제안 slot: `prop`. 소유 바인딩: `bound_frame_object`.

**가시 관계:** soft rounded lobes fold around the central opening.

**효과:** appearance / bound_frame_object / object_frame; material / bound_frame_object / relief.

**채택 조건:** 실제 신체·장기를 추가하지 않음. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 아칸서스 잎이나 몸의 실제 장기와 구별

**근거:** [S05](SOURCES.md).

## GD09 분기 식물 아라베스크

의미 단위: GO031. 제안 slot: `prop`. 소유 바인딩: `selected_ornamental_panel`.

**가시 관계:** vegetal branches continue between repeated leaf units.

**효과:** appearance / selected_ornamental_panel / panel_motif; material / selected_ornamental_panel / surface_pattern.

**채택 조건:** 기하·서예는 별도. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 모든 별·다각형 기하 문양과 구별

**근거:** [S09](SOURCES.md).

## GD10 띠 교차 카르투슈

의미 단위: GO039, GO040. 제안 slot: `prop`. 소유 바인딩: `bound_frame_object`.

**가시 관계:** wide bands cross around the bounded central compartment.

**효과:** appearance / bound_frame_object / object_frame; material / bound_frame_object / strap_relief.

**채택 조건:** 끈 폭과 겹침 앞뒤가 보임. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 가느다란 덩굴·금속선과 띠의 폭을 구별 / 프레임의 형태와 내부 글자의 내용은 별개

**근거:** [S27](SOURCES.md), [S60](SOURCES.md).

## GD11 방사형 로제트 단위

의미 단위: GO041. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_jewelry`.

**가시 관계:** lobes radiate from one bounded center on the mounting.

**효과:** appearance / selected_jewelry / accessories_jewelry; material / selected_jewelry / motif_surface.

**채택 조건:** rose window와 구별. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 원형 전체·고딕 rose window와 작은 모티프를 구별

**근거:** [S32](SOURCES.md).

## GD12 규칙적 기하 교차무늬

의미 단위: GO043. 제안 slot: `prop`. 소유 바인딩: `selected_ornamental_panel`.

**가시 관계:** repeated bands interlace with consistent adjacency.

**효과:** appearance / selected_ornamental_panel / panel_motif; material / selected_ornamental_panel / surface_pattern.

**채택 조건:** 문화·종교 자동 추론 없음. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 식물 아라베스크·무작위 낙서와 구별

**근거:** [S10](SOURCES.md).

## GD13 바탕판 없는 선재 필리그리

의미 단위: GO054, GX03, GX05. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_jewelry`.

**가시 관계:** wire loops join the rim with background visible through their gaps.

**효과:** appearance / selected_jewelry / accessories_jewelry; material / selected_jewelry / wire_surface.

**채택 조건:** sff_pro_j06 의미 재사용; 실제 소유·노출은 후속 바인딩. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_sensual_fetish_fashion_extension.json:wearable_accessory:sff_pro_j06`.

**구별:** 선재 필리그리와 홈 선각을 구별; 열린형과 바탕판형을 별도 / 선각/프린트와 구별하고 열린형으로 명시한 경우만 구멍을 필수화 / 주얼리라는 라벨로 보석·문양·부품 전체를 한 덩어리로 만들지 않는다

**근거:** [S12](SOURCES.md), [S32](SOURCES.md).

## GD14 바탕판 위의 선재 필리그리

의미 단위: GO054, GX04. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_jewelry`.

**가시 관계:** wire relief stands over a continuous backing within the rim.

**효과:** appearance / selected_jewelry / accessories_jewelry; material / selected_jewelry / wire_and_backing.

**채택 조건:** 열린형의 음공간 의무를 물려주지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_sensual_fetish_fashion_extension.json:wearable_accessory:sff_pro_j06`.

**구별:** 선재 필리그리와 홈 선각을 구별; 열린형과 바탕판형을 별도 / 기본 filigree를 열린형으로만 판정하는 과잉 의무 방지

**근거:** [S12](SOURCES.md), [S32](SOURCES.md).

## GD15 금속 알갱이의 배열

의미 단위: GO055, GX16. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_jewelry`.

**가시 관계:** distinct rounded grains rise from the metal ground.

**효과:** appearance / selected_jewelry / accessories_jewelry; material / selected_jewelry / granular_relief.

**채택 조건:** 피부/천의 구슬과 소유 분리. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 거친 주조 표면·점무늬·시퀸과 구별 / 점이 많다는 이유로 모두 granulation으로 판정하지 않는다

**근거:** [S12](SOURCES.md), [S32](SOURCES.md), [S50](SOURCES.md).

## GD16 연속 판재의 볼록 부조

의미 단위: GO056, GX14. 제안 slot: `prop`. 소유 바인딩: `bound_metal_object`.

**가시 관계:** raised broad motifs remain continuous with the metal sheet.

**효과:** appearance / bound_metal_object / object_relief; material / bound_metal_object / sheet_metal.

**채택 조건:** 제작 공정 대신 가시 부조만 검증. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 파인 선·별도 붙인 조각과 판재 부조를 구별 / 어두운 선이나 반짝임 하나로 입체 기법 판정 금지

**근거:** [S12](SOURCES.md).

## GD17 큰 부조 위 작은 윤곽

의미 단위: GO056, GO057. 제안 slot: `prop`. 소유 바인딩: `bound_metal_object`.

**가시 관계:** fine contours articulate the same raised relief.

**효과:** appearance / bound_metal_object / object_relief; material / bound_metal_object / contour_depth.

**채택 조건:** repousse/chasing 공정 확정은 별도. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 파인 선·별도 붙인 조각과 판재 부조를 구별 / 금속을 제거하는 engraving과 제작 의미를 구별

**근거:** [S12](SOURCES.md).

## GD18 금속 표면의 가는 음각선

의미 단위: GO058, GX14. 제안 slot: `prop`. 소유 바인딩: `bound_metal_object`.

**가시 관계:** incised grooves interrupt the continuous reflective surface.

**효과:** appearance / bound_metal_object / object_motif; material / bound_metal_object / incised_surface.

**채택 조건:** 프린트/선재 대체 실패. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 선재·볼록 부조·프린트 선과 구별 / 어두운 선이나 반짝임 하나로 입체 기법 판정 금지

**근거:** [S12](SOURCES.md).

## GD19 에칭형 얕은 칸과 무늬

의미 단위: GO059. 제안 slot: `prop`. 소유 바인딩: `bound_metal_object`.

**가시 관계:** shallow patterned recesses define the decorated field.

**효과:** appearance / bound_metal_object / object_motif; material / bound_metal_object / shallow_relief.

**채택 조건:** 실제 화학 공정 의무는 보류. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 에칭이 항상 선만 파는 기법이라는 축소를 피함

**근거:** [S12](SOURCES.md).

## GD20 선재 구획과 에나멜 색면

의미 단위: GO063. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_jewelry`.

**가시 관계:** continuous thin partitions enclose each enamel field.

**효과:** appearance / selected_jewelry / accessories_jewelry; material / selected_jewelry / enamel_fields.

**채택 조건:** sff_pro_j07 재사용 검토. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_sensual_fetish_fashion_extension.json:wearable_accessory:sff_pro_j07`.

**구별:** 샹르베의 바탕 금속 면과 선재 경계를 구별

**근거:** [S33](SOURCES.md).

## GD21 바탕 금속의 오목한 에나멜 칸

의미 단위: GO064. 제안 slot: `prop`. 소유 바인딩: `bound_metal_object`.

**가시 관계:** broad unrecessed metal separates the colored recesses.

**효과:** appearance / bound_metal_object / object_cells; material / bound_metal_object / enamel_recesses.

**채택 조건:** cloisonne와 동일한 선재 경계를 강제하지 않음. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 클루아조네처럼 모든 경계가 가는 별도 선재는 아님

**근거:** [S12](SOURCES.md).

## GD22 밝은 금속의 어두운 선 채움

의미 단위: GO065. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_jewelry`.

**가시 관계:** dark-filled grooves form a pattern within the bright metal field.

**효과:** appearance / selected_jewelry / accessories_jewelry; material / selected_jewelry / dark_inlay.

**채택 조건:** 니엘로의 조성·진위는 별도. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 검은 에나멜 덩어리·녹·그림자와 구별

**근거:** [S39](SOURCES.md), [S40](SOURCES.md).

## GD23 어두운 금속 바탕의 밝은 상감

의미 단위: GO066. 제안 slot: `prop`. 소유 바인딩: `bound_metal_object`.

**가시 관계:** flush-looking bright-metal motifs lie within the darker ground.

**효과:** appearance / bound_metal_object / object_motif; material / bound_metal_object / metal_inlay.

**채택 조건:** 직물 damask/강재 결 무늬와 분리. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 다마스크 직물·다마스커스강 물결과 구별

**근거:** [S12](SOURCES.md).

## GD24 면이 나뉜 작은 금속 스터드

의미 단위: GO067. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_jewelry`.

**가시 관계:** individual faceted studs attach to a shared mounting.

**효과:** appearance / selected_jewelry / accessories_jewelry; material / selected_jewelry / faceted_studs.

**채택 조건:** 실제 steel/diamond 진위 판정 없음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 유리 보석·둥근 금속 알갱이와 구별

**근거:** [S12](SOURCES.md).

## GD25 일부 돌출부의 길딩

의미 단위: GO062. 제안 slot: `prop`. 소유 바인딩: `bound_ornament_object`.

**가시 관계:** warm reflective coating occupies only the stated raised edges.

**효과:** appearance / bound_ornament_object / object_finish; material / bound_ornament_object / partial_coating; color / bound_ornament_object / bound_regions.

**채택 조건:** 전체 금색으로 번지지 않음. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 통금 물체·노란 페인트·전체 금색 강제와 구별

**근거:** [S12](SOURCES.md).

## GD26 은색 바탕 위 얇은 금색 패치

의미 단위: GO068. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_jewelry`.

**가시 관계:** thin patches remain bounded within the cool-metal field.

**효과:** appearance / selected_jewelry / accessories_jewelry; material / selected_jewelry / thin_overlay; color / selected_jewelry / bound_regions.

**채택 조건:** 금부 공정과 시각 변형을 분리. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 전체 길딩·사진의 색온도 차이와 구별

**근거:** [S13](SOURCES.md).

## GD27 정밀 반복 홈의 금속 필드

의미 단위: GO038, GO061. 제안 slot: `prop`. 소유 바인딩: `bound_metal_object`.

**가시 관계:** regular intersecting lines occupy a bounded engraved field.

**효과:** appearance / bound_metal_object / object_motif; material / bound_metal_object / engine_turned_appearance.

**채택 조건:** 관통 구멍·부품 증가와 구별. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 옛 띠 문양과 시계 엔진 터닝의 용법을 분리 / 임의 스크래치·그리블 부착물과 구별

**근거:** [S31](SOURCES.md).

## GD28 얇은 재료 조각의 맞춤 문양

의미 단위: GO069. 제안 slot: `prop`. 소유 바인딩: `bound_veneer_object`.

**가시 관계:** contrasting fitted pieces meet along flush boundaries.

**효과:** appearance / bound_veneer_object / object_motif; material / bound_veneer_object / veneer_joins; color / bound_veneer_object / bound_regions.

**채택 조건:** 인쇄·그림이 아닌 조각의 경계. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 위에 칠한 그림·재료를 깊게 깎은 부조와 구별

**근거:** [S28](SOURCES.md), [S34](SOURCES.md).

## GD29 직물 바탕과 추가 직조 문양

의미 단위: GO070. 제안 slot: `surface_material`. 소유 바인딩: `selected_garment`.

**가시 관계:** woven supplementary motifs follow the cloth folds.

**효과:** material / selected_garment / woven_surface; appearance / selected_garment / wardrobe_surface.

**채택 조건:** hw_brocade_raised_motifs_1 재사용 우선. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_historical_womenswear_extension.json:surface_material:hw_brocade_raised_motifs_1`, `photo_prompt_tags.json:surface_material:brocade_raised_supplementary_weft_surface`, `photo_prompt_tags.json:texture:brocade_supplementary_pattern_texture`.

**구별:** 자수와 직조의 제작 의미를 구별; damask와 공존 가능

**근거:** [S18](SOURCES.md), [S19](SOURCES.md).

## GD30 같은 직물의 방향성 광택 문양

의미 단위: GO071. 제안 slot: `surface_material`. 소유 바인딩: `selected_garment`.

**가시 관계:** motif and ground retain distinct sheen within the same cloth.

**효과:** material / selected_garment / woven_sheen; appearance / selected_garment / wardrobe_surface.

**채택 조건:** hw_damask_tonal_pattern_1 재사용 우선; tonal 선택형. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_historical_womenswear_extension.json:surface_material:hw_damask_tonal_pattern_1`.

**구별:** 색 프린트·브로케이드와 구별

**근거:** [S19](SOURCES.md).

## GD31 망 바탕의 가는 꽃 레이스

의미 단위: GO074. 제안 slot: `garment_detail`. 소유 바인딩: `selected_garment_lace`.

**가시 관계:** fine floral motifs connect to a visible lightweight mesh ground.

**효과:** appearance / selected_garment_lace / wardrobe_lace; material / selected_garment_lace / net_structure.

**채택 조건:** 샹티이 색/제작법 자동 확정 없음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 기퓌르의 큰 모티프/브리지형과 구별

**근거:** [S37](SOURCES.md), [S59](SOURCES.md).

## GD32 안감 위 브리지형 기퓌르

의미 단위: GO075, GX13. 제안 slot: `garment_detail`. 소유 바인딩: `selected_garment_lace`.

**가시 관계:** short bars join dense motifs while a continuous lining appears below.

**효과:** appearance / selected_garment_lace / wardrobe_lace; material / selected_garment_lace / bridge_structure.

**채택 조건:** 피부 노출 잠금 보존; guipure의 한 선택형. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 연속적인 고운 망 바탕과 브리지 연결을 구별 / 레이스 구조가 열렸어도 의상 노출은 별도 잠금

**근거:** [S38](SOURCES.md), [S61](SOURCES.md).

## GD33 놓은 실과 고정 스티치

의미 단위: GO076, GO077. 제안 slot: `garment_detail`. 소유 바인딩: `selected_embroidery_area`.

**가시 관계:** small transverse stitches secure the thick laid thread to fabric.

**효과:** appearance / selected_embroidery_area / wardrobe_embroidery; material / selected_embroidery_area / thread_relief.

**채택 조건:** 금속사 색상은 별도 잠금. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 금색 프린트·금속판·금장 물체와 구별 / 단순 같은 굵기의 자수 선과 고정 스티치의 관계를 구별

**근거:** [S14](SOURCES.md), [S15](SOURCES.md).

## GD34 바탕에서 솟는 자수 모티프

의미 단위: GO078. 제안 slot: `garment_detail`. 소유 바인딩: `selected_embroidery_area`.

**가시 관계:** raised petals project above the cloth with local contact shadows.

**효과:** appearance / selected_embroidery_area / wardrobe_embroidery; material / selected_embroidery_area / raised_threadwork.

**채택 조건:** 패딩/와이어 실제 제작법은 주장 안 함. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 평면 프린트·두껍게 칠한 그림과 구별

**근거:** [S16](SOURCES.md).

## GD35 붙인 천 조각의 둘레 스티치

의미 단위: GO079. 제안 slot: `garment_detail`. 소유 바인딩: `selected_applique_area`.

**가시 관계:** the separate shape's stitched edge joins it to the cloth ground.

**효과:** appearance / selected_applique_area / wardrobe_applique; material / selected_applique_area / layered_fabric.

**채택 조건:** 색면 프린트 대체 실패. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 직물 내부 색면·프린트 무늬와 겹침 경계를 구별

**근거:** [S15](SOURCES.md).

## GD36 단색 자수의 반복 채움

의미 단위: GO080. 제안 slot: `garment_detail`. 소유 바인딩: `selected_embroidery_area`.

**가시 관계:** repeated monochrome stitch units form denser bounded fill areas.

**효과:** appearance / selected_embroidery_area / wardrobe_embroidery; material / selected_embroidery_area / stitch_pattern; color / selected_embroidery_area / bound_regions.

**채택 조건:** 검정 천 전체로 대체하지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 검은 천·검은 레이스·모든 검은 선묘와 구별

**근거:** [S14](SOURCES.md), [S15](SOURCES.md).

## GD37 흰 바탕/실의 자수 명암

의미 단위: GO081. 제안 slot: `garment_detail`. 소유 바인딩: `selected_embroidery_area`.

**가시 관계:** white raised stitching remains distinct through depth on white cloth.

**효과:** appearance / selected_embroidery_area / wardrobe_embroidery; material / selected_embroidery_area / stitch_relief; color / selected_embroidery_area / bound_regions.

**채택 조건:** 구멍 없는 변형도 허용. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 흰색 프린트·모든 흰 레이스와 구별

**근거:** [S15](SOURCES.md).

## GD38 트리밍의 개별 술과 연속 프린지

의미 단위: GO082, GO083, GO084. 제안 slot: `garment_detail`. 소유 바인딩: `selected_garment_edge`.

**가시 관계:** separate tassel bundles and repeated strands attach to the named edge.

**효과:** appearance / selected_garment_edge / wardrobe_trim; material / selected_garment_edge / thread_bundles.

**채택 조건:** 선택형 분기: 태슬/프린지 모두 강제 금지. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 태슬·프린지 하나와 상위 범주를 구별 / 가장자리 전체 프린지와 개별 묶음을 구별 / 개별 태슬·천의 찢어진 결손과 구별

**근거:** [S50](SOURCES.md).

## GD39 둥근 구슬과 얇은 시퀸의 분리

의미 단위: GO085, GO086. 제안 slot: `garment_detail`. 소유 바인딩: `selected_garment_regions`.

**가시 관계:** rounded beads and flat discs occupy separately named trim areas.

**효과:** appearance / selected_garment_regions / wardrobe_trim; material / selected_garment_regions / bead_vs_disc.

**채택 조건:** 한종류만 요청되면 다른 종류 추가 안 함. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 그래뉼레이션의 금속 접합·평평한 시퀸과 구별 / 둥근 구슬·작은 보석 세팅과 구별

**근거:** [S14](SOURCES.md), [S50](SOURCES.md).

## GD40 코르셋 패널/보강선/센터 여밈

의미 단위: GO095, GX11. 제안 slot: `garment_detail`. 소유 바인딩: `selected_corset`.

**가시 관계:** boning channels follow panels beside a distinct front fastening.

**효과:** appearance / selected_corset / wardrobe_structure; material / selected_corset / boning_channels.

**채택 조건:** 체형·가슴·허리 크기·노출은 변경하지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** waist emphasis·임의 X무늬·몸 자체 변형과 구별 / 보닝·버스크·끈 묶기를 X자 무늬 하나로 대체하지 않는다

**근거:** [S55](SOURCES.md).

## GD41 아일릿과 교차 끈의 여밈

의미 단위: GX12. 제안 slot: `garment_detail`. 소유 바인딩: `selected_garment_closure`.

**가시 관계:** one continuous lace passes through opposed eyelets and bridges the panel gap.

**효과:** appearance / selected_garment_closure / wardrobe_closure; material / selected_garment_closure / lace_hardware.

**채택 조건:** 장식 X프린트로 통과 못함. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 인쇄된 X·끊긴 줄·다른 소유자의 장식을 여밈으로 통과시키지 않는다

**근거:** [S55](SOURCES.md).

## GD42 레이스 위 자수와 구슬의 층

의미 단위: GO008, GO077, GO085. 제안 slot: `garment_detail`. 소유 바인딩: `selected_garment_regions`.

**가시 관계:** fixed embroidery lies above lace and beads attach only at selected centers.

**효과:** appearance / selected_garment_regions / wardrobe_layers; material / selected_garment_regions / layer_order.

**채택 조건:** 후보의 모든 층 effects가 열렸을 때만 적용. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 표면 무늬의 색 혼합과 물리적 층을 구별 / 단순 같은 굵기의 자수 선과 고정 스티치의 관계를 구별 / 그래뉼레이션의 금속 접합·평평한 시퀸과 구별

**근거:** [S14](SOURCES.md), [S18](SOURCES.md), [S50](SOURCES.md).

## GD43 판형 트레이서리 창 머리

의미 단위: GO045, GO046. 제안 slot: `location`. 소유 바인딩: `selected_window`.

**가시 관계:** openings pierce a broad stone field above the window lights.

**효과:** setting / selected_window / architectural_tracery; material / selected_window / stone_surface.

**채택 조건:** 판 두께/음공간이 보이는 선택형. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 트레이서리·스테인드글라스·금속 필리그리의 역할을 분리 / 가는 바가 연결되는 bar tracery와 구별

**근거:** [S02](SOURCES.md), [S03](SOURCES.md), [S56](SOURCES.md).

## GD44 가는 부재형 트레이서리

의미 단위: GO045, GX06. 제안 slot: `location`. 소유 바인딩: `selected_window`.

**가시 관계:** slender stone bars connect mullions to curved upper compartments.

**효과:** setting / selected_window / architectural_tracery; material / selected_window / stone_members.

**채택 조건:** 기존 판형과 동시에 같은 부분에 넣지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 트레이서리·스테인드글라스·금속 필리그리의 역할을 분리 / 판형의 넓은 석재 면과 부재 연결을 구별; 도판 대조 전 형태 초안

**근거:** [S02](SOURCES.md), [S03](SOURCES.md), [S56](SOURCES.md).

## GD45 곡률이 반전하는 오지 아치

의미 단위: GO049. 제안 slot: `location`. 소유 바인딩: `selected_arch`.

**가시 관계:** both sides reverse curvature before meeting at the pointed crown.

**효과:** setting / selected_arch / architectural_arch; material / selected_arch / arch_surface.

**채택 조건:** 일반 pointed arch로 대체 실패. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 단순 첨두아치와 곡률의 반전을 구별

**근거:** [S58](SOURCES.md).

## GD46 세 로브/네 로브 개구부

의미 단위: GO047, GO048. 제안 slot: `prop`. 소유 바인딩: `selected_ornamental_opening`.

**가시 관계:** one selected lobe-count variant forms a complete bounded contour.

**효과:** appearance / selected_ornamental_opening / motif_geometry; material / selected_ornamental_opening / opening_boundary.

**채택 조건:** 배타 선택 3/4; 두 변형의 합집합을 hard duty로 만들지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 쿼트러포일·실제 클로버 잎·대칭 장식 일반과 구별 / 세잎·꽃잎 수가 다른 로제트와 구별

**근거:** [S01](SOURCES.md).

## GD47 기점에서 펼쳐진 팬 볼트

의미 단위: GO050. 제안 slot: `location`. 소유 바인딩: `selected_ceiling`.

**가시 관계:** fan ribs emerge from springing points and meet adjacent fan units.

**효과:** setting / selected_ceiling / architectural_vault; material / selected_ceiling / rib_relief.

**채택 조건:** 필요한 시점 변경은 별도 composition 후보. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 일반 rib vault·그물형 선각과 팬의 기점을 구별

**근거:** [S41](SOURCES.md).

## GD48 수직 부재 끝의 피니얼

의미 단위: GO051, GX10. 제안 slot: `location`. 소유 바인딩: `selected_upright`.

**가시 관계:** the terminal caps the same upright at its highest tip.

**효과:** setting / selected_upright / architectural_terminal; material / selected_upright / terminal_surface.

**채택 조건:** 가운데 떠 있는 보석/꽃 대체 실패. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 첨탑 전체와 끝 장식을 구별 / 뾰족한 물체 전체와 끝/측면 부착 장식을 구별; crocket 세부 용어는 후속 근거 필요

**근거:** [S02](SOURCES.md), [S03](SOURCES.md).

## GD49 기괴한 형상의 배수 출구

의미 단위: GO052. 제안 slot: `location`. 소유 바인딩: `selected_building_spout`.

**가시 관계:** the sculpted mouth-like outlet belongs to a visible drainage route.

**효과:** setting / selected_building_spout / architectural_spout; material / selected_building_spout / stone_form.

**채택 조건:** 기능 메타데이터 확인 전 가시 spout만 평가. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 모든 괴물 석조상·키메라와 구별

**근거:** [S42](SOURCES.md).

## GD50 층과 깊이가 읽히는 무카르나스

의미 단위: GO053. 제안 slot: `location`. 소유 바인딩: `selected_ceiling_transition`.

**가시 관계:** recessed cells form successive tiers through the wall-to-ceiling transition.

**효과:** setting / selected_ceiling_transition / architectural_cells; material / selected_ceiling_transition / recessed_depth.

**채택 조건:** pf_muqarnas_location/profiles 재사용; camera/조명 분리. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_palace_fortification_extension.json:location:pf_muqarnas_location`, `photo_prompt_palace_fortification_extension.json:composition:pf_muqarnas_composition`.

**구별:** 벌집 평면 프린트·팬 리브와 구별

**근거:** [S57](SOURCES.md).

## GD51 고딕 구획을 옮긴 목 장식

의미 단위: GO045, GO051, GX18. 제안 slot: `wearable_accessory`. 소유 바인딩: `selected_collar_frame`.

**가시 관계:** miniature pointed compartments connect within the collar's own frame.

**효과:** appearance / selected_collar_frame / accessories_jewelry; material / selected_collar_frame / miniature_architecture.

**채택 조건:** 성당 배경·새 인물 자동 추가 금지. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 트레이서리·스테인드글라스·금속 필리그리의 역할을 분리 / 첨탑 전체와 끝 장식을 구별 / 성당·건물 추가가 아닌 형태 유추; 실제 역사 유물로 주장하지 않는다

**근거:** [S01](SOURCES.md), [S02](SOURCES.md), [S03](SOURCES.md).

## GD52 역사적 고딕의 구조적 실내

의미 단위: GO017. 제안 slot: `location`. 소유 바인딩: `selected_interior`.

**가시 관계:** pointed openings and ribs align with the existing vertical supports.

**효과:** setting / selected_interior / architectural_structure; material / selected_interior / masonry; style / selected_interior / gothic_vocabulary.

**채택 조건:** 현대 goth makeup/의상은 독립. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_tags.json:world:victorian_gothic_world`.

**구별:** 중세 고딕과 현대 고스 패션을 구별

**근거:** [S01](SOURCES.md), [S02](SOURCES.md).

## GD53 로코코 가구의 비대칭 구획

의미 단위: GO021, GO036, GO040. 제안 slot: `prop`. 소유 바인딩: `selected_furniture`.

**가시 관계:** unequal scrolling ornaments frame the furniture's central opening.

**효과:** appearance / selected_furniture / object_ornament; material / selected_furniture / carved_surface; style / selected_furniture / rococo_vocabulary.

**채택 조건:** 팔레트·시대는 요청을 보존. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 파스텔색·공주 이미지 하나와 구별 / 정원석·일반 나선·파스텔 팔레트와 구별 / 프레임의 형태와 내부 글자의 내용은 별개

**근거:** [S04](SOURCES.md), [S27](SOURCES.md).

## GD54 흐르는 선과 프레임의 통합

의미 단위: GO025, GO037. 제안 slot: `prop`. 소유 바인딩: `selected_frame_object`.

**가시 관계:** the long stem-like curve continues into the supporting frame.

**효과:** appearance / selected_frame_object / object_structure; material / selected_frame_object / curved_members; style / selected_frame_object / art_nouveau_vocabulary.

**채택 조건:** 관련 자연 모티프는 선택형. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 아르데코의 일반 기하·로코코 조개와 구별 / 짧은 둥근 나선·임의의 곡선 노이즈와 구별

**근거:** [S06](SOURCES.md).

## GD55 용도 표면에 맞춘 반복 식물무늬

의미 단위: GO028, GO031. 제안 slot: `surface_material`. 소유 바인딩: `selected_fabric_surface`.

**가시 관계:** repeated plant motifs follow the cloth's usable bounded field.

**효과:** material / selected_fabric_surface / patterned_fabric; appearance / selected_fabric_surface / wardrobe_surface; style / selected_fabric_surface / craft_pattern.

**채택 조건:** 실제 수공예·윤리·운동 소속을 주장 안 함. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 장식 최대량을 뜻하는 말과 구별 / 모든 별·다각형 기하 문양과 구별

**근거:** [S07](SOURCES.md), [S09](SOURCES.md).

## GD56 성인의 고딕 로리타 의상 형태

의미 단위: GO089. 제안 slot: `costume_style`. 소유 바인딩: `explicit_adult_subject`.

**가시 관계:** frills and a structured full skirt belong to the adult street-fashion outfit.

**효과:** appearance / explicit_adult_subject / wardrobe_silhouette; material / explicit_adult_subject / trim; style / explicit_adult_subject / gothic_lolita_variant.

**채택 조건:** 나이/노출을 명칭에서 추론하지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_tags.json:costume_style:gothic_lolita_dress`.

**구별:** 명칭을 성적 장르·나이 판정과 혼동하지 않는다

**근거:** [S49](SOURCES.md).

## GD57 의상에 속한 교차 스트랩/고리

의미 단위: GO094. 제안 slot: `garment_detail`. 소유 바인딩: `explicit_adult_subject_garment`.

**가시 관계:** each ring joins identified strap ends attached to the garment.

**효과:** appearance / explicit_adult_subject_garment / wardrobe_straps; material / explicit_adult_subject_garment / hardware.

**채택 조건:** 실제 손·몸 구속 사건과 별도. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 단순 스트랩 장식과 실제 몸/손 구속 사건을 구별

**근거:** [S20](SOURCES.md).

## GD58 성취와 덧없음의 정물 관계

의미 단위: GO102, GO103. 제안 slot: `prop`. 소유 바인딩: `requested_still_life`.

**가시 관계:** an achievement object and a mortality reminder share the same arrangement.

**효과:** subject / requested_still_life / still_life_object_set; composition / requested_still_life / object_relation; concept / requested_still_life / mortality.

**채택 조건:** 두 objects가 요청/열린 scope에 있을 때만; 사망 event 추가 금지. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_tags.json:subject:mortality_symbol_still_life`, `photo_prompt_tags.json:narrative_phase:mortality_symbol_contemplation`, `photo_prompt_tags.json:prop:extinguished_candle_prop`.

**구별:** 실제 시체·사망 사건과 상징을 구별 / 해골 하나·일반 어두운 정물·memento mori와 범주를 구별

**근거:** [S39](SOURCES.md), [S54](SOURCES.md).

## GD59 장식 틀이 둘러싼 유물 용기

의미 단위: GO105. 제안 slot: `prop`. 소유 바인딩: `requested_container`.

**가시 관계:** architectural ornament frames the container's bounded compartment.

**효과:** appearance / requested_container / object_architecture; material / requested_container / mixed_ornament; concept / requested_container / reliquary_context.

**채택 조건:** 내용물·종교 의미는 출처/요청과 따로 기록. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 장식 왕관·일반 상자·실제 유해와 구별

**근거:** [S01](SOURCES.md).

## GD60 장식품에 한정한 마모/쇠락

의미 단위: GO106, GX17. 제안 slot: `prop`. 소유 바인딩: `selected_ornament_object`.

**가시 관계:** local chips or tarnish interrupt only named finish regions.

**효과:** appearance / selected_ornament_object / object_condition; material / selected_ornament_object / finish_wear.

**채택 조건:** pristine 잠금·신체 손상과 혼동 금지. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 실제 가난·도덕적 타락·해골 필수와 구별 / 장식품의 손상과 인물의 신체 손상·도덕적 쇠락을 연결하지 않는다

**근거:** [S20](SOURCES.md).

## GD61 명시된 허구 신체의 변형 연결

의미 단위: GO109. 제안 slot: `anatomical_connection`. 소유 바인딩: `explicit_fictional_body`.

**가시 관계:** one requested transformed part remains connected to its stated body owner.

**효과:** body_geometry / explicit_fictional_body / requested_connection; appearance / explicit_fictional_body / fictional_surface; concept / explicit_fictional_body / body_horror.

**채택 조건:** 변형 위치·매체·강도는 요청 의미에 바인딩. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 보철 장신구·조각 그로테스크·단순 상처와 구별

**근거:** [S47](SOURCES.md), [S48](SOURCES.md).

## GD62 큰 패널 안의 작은 판/그리블

의미 단위: GO113, GO121, GX19. 제안 slot: `prop`. 소유 바인딩: `selected_casing`.

**가시 관계:** fasteners attach subpanels and fittings within the larger recessed field.

**효과:** appearance / selected_casing / object_detail; material / selected_casing / hardware; composition / selected_casing / part_hierarchy.

**채택 조건:** 실제 기계 기능을 부품 수로 주장하지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 기능을 알 수 없는 부품을 실제 작동 장치로 판정하지 않는다 / 큰 사물 개수와 단계적 구조를 구별 / 무작위 부품의 근접만으로 조립 관계를 추정하지 않는다

**근거:** [S46](SOURCES.md).

## GD63 덮개 경계 안의 기구부

의미 단위: GO117. 제안 slot: `prop`. 소유 바인딩: `selected_apparatus`.

**가시 관계:** gears and shafts occupy the defined open cavity inside the casing.

**효과:** appearance / selected_apparatus / object_mechanism; material / selected_apparatus / hardware.

**채택 조건:** 정지 구조만 검증; 작동은 시간 근거 필요. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 표면에 붙인 장식 기어·실제 작동 사건과 구별

**근거:** [S46](SOURCES.md).

## GD64 유기형과 기계형의 명시 허구 접합

의미 단위: GO115, GO118. 제안 slot: `anatomical_connection`. 소유 바인딩: `explicit_fictional_body`.

**가시 관계:** an organic-looking region joins a rigid mechanism at a stated interface.

**효과:** body_geometry / explicit_fictional_body / requested_connection; appearance / explicit_fictional_body / fictional_surface; material / explicit_fictional_body / mixed_structure.

**채택 조건:** 착용 장신구·실제 질병/수술과 분리. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 생체역학 학문·wearable hardware·실제 의학 분류와 구별 / 무작위 선·수술 결과·실제 생명과학 주장을 구별

**근거:** [S48](SOURCES.md).

## GD65 명암으로 부조의 부피 드러내기

의미 단위: GO122, GX14. 제안 slot: `lighting`. 소유 바인딩: `bound_focal_object`.

**가시 관계:** light-shadow transitions make the same relief's depth readable.

**효과:** lighting / bound_focal_object / tonal_distribution; composition / bound_focal_object / focal_legibility.

**채택 조건:** chiaroscuro 기존 ID 재사용 검토; camera 자동 변경 없음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** `photo_prompt_tags.json:lighting:chiaroscuro`, `photo_prompt_tags.json:lighting:chiaroscuro_window_light`, `photo_prompt_tags.json:lighting:baroque_gilded_chiaroscuro_lighting`.

**구별:** 어두운 화면 전체·테네브리즘과 구별 / 어두운 선이나 반짝임 하나로 입체 기법 판정 금지

**근거:** [S12](SOURCES.md), [S52](SOURCES.md).

## GD66 어두운 환경의 선택적 디테일 조명

의미 단위: GO123, GX20. 제안 slot: `lighting`. 소유 바인딩: `bound_focal_object`.

**가시 관계:** a chosen focal region is illuminated within a predominantly dark field.

**효과:** lighting / bound_focal_object / tonal_distribution; composition / bound_focal_object / focal_legibility.

**채택 조건:** required 구조를 어둠으로 숨기면 실패. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 모든 미세 구조를 균일하게 보이는 목적과 분리 / 선명한 피부·전체 고해상도·업스케일링이 세공 구조의 증거는 아니다

**근거:** [S52](SOURCES.md), [S53](SOURCES.md).

## GD67 허구 상처/흔적의 소유와 영역

의미 단위: GO110. 제안 slot: `aftermath_trace`. 소유 바인딩: `explicit_fictional_injury_region`.

**가시 관계:** requested injury and blood traces belong to separately named body and surface regions.

**효과:** appearance / explicit_fictional_injury_region / requested_injury_trace; event / explicit_fictional_injury_region / requested_aftermath.

**채택 조건:** 고어 강도 자동 증가 없음; policy block은 별도 상태. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 단순 붉은색·해골 상징·몸의 변형 전체와 구별

**근거:** [S47](SOURCES.md).

## GD68 성인 관능 연출과 죽음 모티프의 병치

의미 단위: GO107. 제안 slot: `composition`. 소유 바인딩: `explicit_adult_figure_and_requested_motif`.

**가시 관계:** the stated adult figure and symbolic object have separately bound spacing and contact.

**효과:** composition / explicit_adult_figure_and_requested_motif / figure_object_relation; sexual_tone / explicit_adult_figure_and_requested_motif / requested_styling; concept / explicit_adult_figure_and_requested_motif / mortality.

**채택 조건:** 동의·성행위·실제 사망을 새로 만들지 않음. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 사망·폭력·성적 접촉을 분위기 단어로 새로 만들지 않는다

**근거:** [S20](SOURCES.md).

## GD69 불꽃처럼 휘는 석조 트레이서리

의미 단위: GO018, GO045. 제안 slot: `location`. 소유 바인딩: `selected_window`.

**가시 관계:** wavy stone members enclose flame-like pointed openings.

**효과:** setting / selected_window / architectural_tracery; material / selected_window / stone_members.

**채택 조건:** flamboyant는 고딕 전체의 공통 의무가 아님. Reuse the current family owner if it actually owns this target. A research family is not an automatic runtime route.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 직선 방사형 창살과 불꽃형 윤곽을 구별 / 트레이서리·스테인드글라스·금속 필리그리의 역할을 분리

**근거:** [S02](SOURCES.md), [S03](SOURCES.md).

## GD70 인물/동물/식물이 이어진 장식 모티프

의미 단위: GO042. 제안 slot: `prop`. 소유 바인딩: `selected_ornamental_panel`.

**가시 관계:** figural heads and animal forms merge into a continuous vegetal scroll.

**효과:** appearance / selected_ornamental_panel / panel_motif; material / selected_ornamental_panel / ornament_relief.

**채택 조건:** 조각 장식의 혼성을 살아 있는 몸의 손상으로 바꾸지 않음. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 장식적 그로테스크·바디 호러·고어를 분리

**근거:** [S25](SOURCES.md).

## GD71 지정 금속 패널의 열린 음공간

의미 단위: GO060, GX14. 제안 slot: `prop`. 소유 바인딩: `bound_metal_panel`.

**가시 관계:** cut openings remain within the panel with the backing visible through them.

**효과:** appearance / bound_metal_panel / panel_openings; material / bound_metal_panel / pierced_surface.

**채택 조건:** 프린트된 어두운 모양으로 개구부를 대체하지 않음. Ordinary object ornament needs a neutral object route. Reuse the accessory meaning, but do not force a wearable main_subject target or adult/fetish guards. Decide whether existing object/prop ownership suffices before creating a neutral ornament extension.

**기존 ID 재사용 검토:** 확정 없음. 기존 소유 파일의 원자를 먼저 대조..

**구별:** 그려진 구멍·어두운 얼룩과 실제 개구부를 구별 / 어두운 선이나 반짝임 하나로 입체 기법 판정 금지

**근거:** [S12](SOURCES.md), [S27](SOURCES.md).
