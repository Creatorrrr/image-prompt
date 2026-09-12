# 현실적 배경 시각 관계 상세 카탈로그

모든 항목은 연구 제안이다. 출처는 물리·관행·경계 판단을 지원하며, 아래 장면과 판정 기준은 이를 바탕으로 작성한 설계다. 생성 효과는 아직 시험하지 않았다.

## 기존 건축의 접속 구조 — rb_architecture_connectivity

**대상:** 문틀·벽 두께·바닥 경계. **적용 조건:** 문과 벽 및 바닥이 한 프레임에 보임.

**관찰할 요소:** 문틀이 벽 두께 안에 들어감 / 바닥이 문턱까지 연속됨 / 창·배관의 부착 위치가 건물 면과 연결됨.

**혼동 경계:** 건물 이름만 제시 / 벽에 붙인 평면 벽지 / 끊긴 문턱.

> The recessed doorway has visible wall thickness, and the pavement continues to its threshold beneath wall-mounted fixtures.

**기존 연결:** `architectural_threshold_frame_depth_relation`.

**근거 연결:** [S04](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-distortion.pdf). S04는 원근 기하만 지원한다. 설비·건축 접속 예시는 일반 설계 가설이며 지역별 건축 사실이 아니다.

## 사용 목적에 맞는 생활 흔적 — rb_use_trace_affordance

**대상:** 선택한 작업면과 사용하는 소품. **적용 조건:** 사용 중인 공간이며 적절한 소품 1–3개 선택.

**관찰할 요소:** 소품이 안정된 지지면에 놓임 / 손이 닿는 위치에 사용 물건이 있음 / 통행 경로가 유지됨.

**혼동 경계:** 무작위 쓰레기 / 모든 공간의 빈곤화 / 부유 소품.

> A recently used mug rests within reach beside a folded cloth, with the walking route left clear.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** 직접 실증 자료 없는 설계 가설. 직접 실증 근거를 확보하지 않은 배치·역학 가설. 우선 수동 검토하고 hard 자동 활성화하지 않는다.

## 일상 설비의 부착과 배치 — rb_infrastructure_attachment

**대상:** 배수구·배관·배선 중 선택한 두 설비. **적용 조건:** 요청 장소와 시대에 설비가 적합함.

**관찰할 요소:** 배수구가 보행면 안에 맞물림 / 배관이 벽 지지대에 고정됨 / 선택 설비가 공간 용도를 방해하지 않음.

**혼동 경계:** 서울이면 쓰레기 강제 / 공중에 끝나는 케이블 / 시대 불일치 설비.

> A drain cover sits flush with the path while a service pipe follows the wall on visible brackets.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** 직접 실증 자료 없는 설계 가설. 직접 실증 근거를 확보하지 않은 배치·역학 가설. 우선 수동 검토하고 hard 자동 활성화하지 않는다.

## 국소적인 보수 경계 — rb_repair_patch_locality

**대상:** 벽 도장과 보수 부위. **적용 조건:** 보수가 있는 공간을 선택함.

**관찰할 요소:** 한정된 패치 경계 / 기존 면과 약한 색·결 차이 / 벽 모서리와 줄눈 연속성 유지.

**혼동 경계:** 폐허 전역 균열 / 랜덤 디지털 얼룩.

> One small repaired patch differs slightly in paint tone while the wall joints continue through the surrounding surface.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S10](https://www.nps.gov/articles/this-masonry-is-for-the-bees.htm). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 접촉 위치에 집중된 마모 — rb_contact_wear_locality

**대상:** 손잡이·문 가장자리·바닥 동선 중 하나. **적용 조건:** 사용 흔적을 허용하고 해당 부위가 충분히 큼.

**관찰할 요소:** 접촉 부분의 국소 광택·마모 / 비접촉 부분의 상대적 보존 / 기하 구조 연속성.

**혼동 경계:** 모든 표면에 같은 스크래치 / 카메라 노이즈로 대체.

> The door pull is slightly polished at the gripping area, while the adjacent painted panel remains intact.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S11](https://www.cs.columbia.edu/CAVE/databases/tvbrdf/about.php). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 물 경로에 연결된 변색 — rb_water_path_stain

**대상:** 배수 출구와 그 아래 벽. **적용 조건:** 물 흔적이 있는 외벽을 선택함.

**관찰할 요소:** 출구·돌출부가 보임 / 그 아래 제한된 흐름 흔적 / 주변 마른 면과 구분.

**혼동 경계:** 무작위 세로 줄무늬 / 벽 전체 곰팡이 자동 생성 / 사진으로 누수 진단.

> A faint runoff mark begins below the drain outlet and follows a narrow path down the wall.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S10](https://www.nps.gov/articles/this-masonry-is-for-the-bees.htm). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 재료별 반사 응답 차이 — rb_material_response_contrast

**대상:** 같은 조명 아래 콘크리트·금속·유리. **적용 조건:** 서로 다른 재료가 인접해 보임.

**관찰할 요소:** 무광 면의 넓은 명암 / 코팅 금속의 제한된 하이라이트 / 유리의 장면에 맞는 반사·투과.

**혼동 경계:** 모든 재료의 동일 플라스틱 광택 / 재료마다 불필요한 오염.

> Matte plaster, painted metal and window glass respond differently to the same side light.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S06](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory), [S07](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 젖은 부분과 마른 부분의 경계 — rb_wet_dry_boundary

**대상:** 바닥·물·반사의 원본. **적용 조건:** 젖은 바닥과 반사 원본이 함께 보임.

**관찰할 요소:** 국소적인 젖음 경계 / 원본에 대응하는 반사 위치 / 타일 틈이나 발이 반사를 끊음.

**혼동 경계:** 아무 출처 없는 네온 줄 / 바닥 전체 거울 / 젖음만으로 침수 판정.

> A shallow wet patch reflects the visible doorway light, interrupted by grout lines and bordered by dry stone.

**기존 연결:** `wet_surface_light_reflection_owner_relation`.

**근거 연결:** [S07](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S11](https://www.cs.columbia.edu/CAVE/databases/tvbrdf/about.php). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 유리 반사와 투과의 공존 — rb_glass_reflection_transmission

**대상:** 창 유리·반사 원본·유리 뒤 공간. **적용 조건:** 반투명 효과가 아닌 투명 유리 창.

**관찰할 요소:** 창틀과 유리 면이 일치 / 반사 원본과 대응하는 형태 / 유리 뒤 실내가 선택 영역에서 읽힘.

**혼동 경계:** 거울로 대체 / 유리 뒤 물체가 유리 앞에 겹침 / 모든 반사를 왜곡.

> The window holds a restrained reflection of the opposite facade while the interior table remains visible through it.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S07](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 창에서 실내로 이어지는 밝기 차이 — rb_window_room_gradient

**대상:** 창·가까운 벽·깊은 실내. **적용 조건:** 창이 주요 광원인 장면 선택.

**관찰할 요소:** 창 방향을 받는 면이 밝음 / 실내 깊이에 따른 명암 차이 / 피사체와 인접 물체가 같은 빛 방향을 공유.

**혼동 경계:** 화면 가장자리 비네트 / 모든 얼굴에 독립 조명 / 무조건 어두운 방.

> Daylight enters from the left window, brightening the nearby tabletop and falling to a softer level deeper in the room.

**기존 연결:** `window_seat_daylight_activity_relation`.

**근거 연결:** [S01](https://www.nikonusa.com/learn-and-explore/photography-glossary), [S09](https://pbr-book.org/4ed/Light_Sources/Area_Lights). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 보이는 조명과 조명 영역의 대응 — rb_practical_pool

**대상:** 벽등·램프와 수광면. **적용 조건:** 보이는 practical의 효과가 필요함.

**관찰할 요소:** 발광 기구가 식별됨 / 가까운 수광면의 국소 조도 상승 / 먼 곳과 영역 경계가 자연스럽게 이어짐.

**혼동 경계:** 빛나기만 하는 소품 / 천장등과 무관한 스포트라이트.

> The wall lamp produces a localized pool on the adjacent wall and table, fading into the surrounding room light.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S01](https://www.nikonusa.com/learn-and-explore/photography-glossary), [S09](https://pbr-book.org/4ed/Light_Sources/Area_Lights). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 서로 다른 광원의 공간적 색 구역 — rb_mixed_source_zones

**대상:** 창광 구역과 실내등 구역. **적용 조건:** 둘 이상의 다른 색 광원을 명시함.

**관찰할 요소:** 두 광원 또는 명확한 방향 단서 / 각 수광면에 연결된 색 구역 / 겹침 영역의 점진적인 혼합.

**혼동 경계:** 전역 청록·주황 LUT / 서로 다른 표면 고유색만 있음 / 모든 야경 네온화.

> Cool window light reaches the window-side sleeve, while the nearby lamp gives the tabletop a warmer local tone.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S02](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/setting-white-balance). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 근접 표면에서 돌아온 색 — rb_bounce_owner

**대상:** 색 벽과 가까운 중성 의상 부위. **적용 조건:** 바운스를 받을 지정 owner가 보임.

**관찰할 요소:** 근접한 유색 표면 / 그쪽을 향한 작은 영역의 색 영향 / 다른 면은 원래 색을 유지.

**혼동 경계:** 옷 자체의 배색 / 전체 화이트밸런스 변화 / 멀리 떨어진 면의 동일 색.

> A muted green wall adds a faint green return only to the nearby white sleeve facing it.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S06](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory), [S07](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 피사체와 주변 물체의 투영 그림자 일관성 — rb_shared_cast_shadow

**대상:** 피사체·선택 주변 물체·바닥. **적용 조건:** 하나의 우세한 광원과 보이는 수광면.

**관찰할 요소:** 선택 물체들의 그림자 방향이 광원과 양립 / 수광면 기하에 따라 그림자가 변형 / 인물 그림자가 해당 접촉부와 연결.

**혼동 경계:** 모든 그림자가 반드시 평행 / 복수 광원 무시 / 몸과 무관한 바닥 얼룩.

> The person and nearby bollard cast shadows consistent with the same late-afternoon light onto the sloping pavement.

**기존 연결:** `hard_light_shadow_edge_relation`.

**근거 연결:** [S09](https://pbr-book.org/4ed/Light_Sources/Area_Lights), [S18](https://journals.sagepub.com/doi/10.1068/p260171). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 확산광 아래 발과 바닥의 접촉 — rb_soft_ground_contact

**대상:** 보이는 지지 발·바닥. **적용 조건:** 서 있는 인물의 발과 지지면이 프레임에 있음.

**관찰할 요소:** 밑창과 바닥의 접점 / 확산광에 맞는 절제된 주변 어둠 / 무게를 받는 발과 다리 연결.

**혼동 경계:** 떠 있는 발 / 모든 발 주위 검은 외곽선 / 숨겨진 발을 통과 처리.

> The supporting shoe sits flush on the paving, with only a soft local darkening under the sole in the overcast light.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S09](https://pbr-book.org/4ed/Light_Sources/Area_Lights). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 장면 내 밝기 우선순위 — rb_exposure_priority

**대상:** 주요 의상·밝은 창·실내 어두운 면. **적용 조건:** 보존할 디테일 영역을 요청에서 지정함.

**관찰할 요소:** 핵심 영역의 읽히는 중간톤 / 광원에 가까운 영역이 더 밝음 / 어두운 구역이 자기 위치에서 더 어둡게 남음.

**혼동 경계:** 모든 면 균일 밝기 / 얼굴 전체 클리핑 / 그림자 디테일 보존 금지.

> Expose for the person and interior surfaces, allowing the distant window to remain brighter without flattening the room's tonal separation.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S14](https://blog.adobe.com/en/publish/2023/10/10/hdr-explained). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 밝은 면에서 흰색까지의 이행 — rb_highlight_shoulder

**대상:** 선택 밝은 벽·하이라이트 가장자리. **적용 조건:** 톤 응답이 명시된 사진.

**관찰할 요소:** 밝은 면의 경계에서 점진적 톤 변화 / 핵심 주변 결 유지 / 작은 강한 코어와 넓은 밝은 면 구분.

**혼동 경계:** 광범위 흰 페인트 덮기 / 반드시 클리핑 요구 / 안개로 대비 지우기.

> Bright wall tones approach white gradually, retaining nearby texture around the small brightest reflection.

**기존 연결:** `highlight_rolloff_tone_response`.

**근거 연결:** [S14](https://blog.adobe.com/en/publish/2023/10/10/hdr-explained). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 거리에 따른 대기층 분리 — rb_distance_haze

**대상:** 근경·먼 건물 또는 산. **적용 조건:** 충분한 시선 거리와 산란 매질을 허용함.

**관찰할 요소:** 근경 대비 보존 / 먼 형태의 상대적 대비 감소 / 공간 거리와 변화가 대응.

**혼동 경계:** 2m 카페의 뿌연 필터 / 유리 오염 / 모든 원경의 일률 청색.

> Distant buildings lose some contrast through the long air path while the nearby railing stays clear.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S08](https://www.pbr-book.org/4ed/Volume_Scattering). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 인물 분리와 환경 가독성 — rb_readable_environment_focus

**대상:** 초점 인물·중경 장소 단서. **적용 조건:** 장소를 알아볼 수 있어야 하는 인물 사진.

**관찰할 요소:** 인물의 선택 부분이 선명 / 중경의 구조 단서 2개가 식별됨 / 멀수록 흐림이 공간적으로 일관됨.

**혼동 경계:** 조리개 숫자만 만족 / 모든 배경 추상 보케 / 전역 샤프닝.

> Keep the subject distinct while the doorway and sidewalk junction remain recognizable in the middle distance.

**기존 연결:** `shallow_depth_focus_falloff_relation`.

**근거 연결:** [S03](https://www.usa.canon.com/pro/rf-lens-world/features/depth-of-field). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 가림 경계의 연속적인 초점 이행 — rb_depth_focus_continuity

**대상:** 선명면·앞뒤의 가는 구조물. **적용 조건:** 얕은 심도 요청이 있음.

**관찰할 요소:** 선명면의 안정된 디테일 / 거리 순서에 맞는 흐림 / 가림 가장자리에서 후광·절단 최소화.

**혼동 경계:** 머리 주위 마스크 테두리 / 보케를 붙인 콜라주 / 움직임 번짐.

> The near railing and distant facade leave focus according to their depth, without a cutout halo around the subject.

**기존 연결:** `shallow_depth_focus_falloff_relation`.

**근거 연결:** [S03](https://www.usa.canon.com/pro/rf-lens-world/features/depth-of-field). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 프레임 가장자리의 실제 전경 가림 — rb_foreground_occlusion

**대상:** 의자 등받이 등 전경 물체·중경 대상. **적용 조건:** 주요 대상의 필수 부분 가림을 허용하지 않음.

**관찰할 요소:** 전경 물체 일부가 프레임 밖으로 이어짐 / 중경 일부를 일관되게 가림 / 가린 물체의 나머지 형태가 유지.

**혼동 경계:** 얼굴의 필수 표정 가림 / 공중에 뜬 장식 스트립 / 가림 없는 물체 목록.

> A nearby chair back enters one lower edge of the frame and overlaps the table without covering the person's hands.

**기존 연결:** `three_plane_depth_chain`.

**근거 연결:** [S04](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-distortion.pdf). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 공간 깊이와 상대 크기의 일관성 — rb_scale_perspective

**대상:** 바닥 선·근경 기둥·먼 문. **적용 조건:** 동일 공간의 깊이 표지가 두 개 이상 보임.

**관찰할 요소:** 거리와 양립하는 크기 차이 / 바닥 선의 일관된 수렴 / 문·창의 건축 연결.

**혼동 경계:** 모든 문 같은 화면 크기 / 배럴 왜곡을 원근으로 대체 / 광각이면 신체 변형 강제.

> Paving lines and repeated doorways recede consistently from the near post toward the far end of the street.

**기존 연결:** `wide_angle_near_field_perspective`, `three_plane_depth_chain`.

**근거 연결:** [S04](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-distortion.pdf). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 움직인 부위에 제한된 번짐 — rb_local_motion_blur

**대상:** 움직이는 손·바퀴 등과 정지 구조. **적용 조건:** 셔터 시간 동안 일부 움직임을 표현함.

**관찰할 요소:** 선택 운동 부위의 방향성 번짐 / 정지 배경의 상대적 선명도 / 관절·물체 연결 유지.

**혼동 경계:** 사진 전체 흐리기 / 가짜 속도선 / 모든 손가락 융합.

> A small blur follows the moving hand while the stationary doorframe and torso remain clear.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S19](https://www.usa.canon.com/pro/rf-lens-world/features/aperture). Canon의 셔터에 의한 운동 표현 설명에 대응; 지정 부위·방향·정지면 비교는 별도 설계다.

## 동일 바람과 양립하는 반응 — rb_shared_wind_response

**대상:** 느슨한 옷 끝·머리카락·근처 잎. **적용 조건:** 바람이 있고 서로 다른 물체 반응을 요청함.

**관찰할 요소:** 각 물체의 고정점 유지 / 가벼운 부분의 그럴듯한 휘어짐 / 국소 가림·재질 차이를 허용한 방향 양립.

**혼동 경계:** 모든 잎·옷이 똑같이 평행 / 인물 머리만 강풍 / 바람 속도 인증.

> Loose hair, the free jacket hem and exposed leaves respond compatibly to the breeze, each retaining its own attachment and stiffness.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** 직접 실증 자료 없는 설계 가설. 직접 실증 근거를 확보하지 않은 배치·역학 가설. 우선 수동 검토하고 hard 자동 활성화하지 않는다.

## 저조도 명도 노이즈의 제한적 질감 — rb_low_light_noise

**대상:** 어두운 중성 면·디테일 경계. **적용 조건:** 거친 디지털 촬영 질감을 선택함.

**관찰할 요소:** 미세한 무작위 명도 변화 / 주요 윤곽 보존 / 색 얼룩·JPEG 블록과 구분.

**혼동 경계:** 대낮 저감도에도 강제 / 필름 긁힘 / 벽 재질을 노이즈로 대체.

> Subtle luminance noise is visible in the darker wall tones while edges and material differences remain readable.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S12](https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 선택적인 렌즈 주변 광량 감소 — rb_optional_lens_falloff

**대상:** 프레임 중심·주변. **적용 조건:** 비네트를 사용하겠다는 요청이 있음.

**관찰할 요소:** 중심에서 주변으로 완만한 변화 / 장면 안 광원 명암도 유지 / 검은 테두리가 되지 않음.

**혼동 경계:** 방 구석 어둠과 혼동 / 모든 실제 사진의 필수 결함.

> A mild optical falloff gently darkens the outer field without replacing the room's own lighting pattern.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S12](https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 국소적인 색수차 표현 — rb_optional_chromatic_fringe

**대상:** 주변부 고대비 경계. **적용 조건:** 색수차를 명시하고 필요한 디테일을 해치지 않음.

**관찰할 요소:** 선택 경계에 약한 색 어긋남 / 다른 평탄 영역은 유지 / 색 조명과 구분.

**혼동 경계:** 전체 RGB 분리 / 피부 얼룩 / 현실감 기본값으로 강제.

> A very slight color fringe appears only at a few high-contrast edges near the image periphery.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S12](https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 처리 흔적을 억제한 경계와 톤 — rb_restrained_processing

**대상:** 피사체 윤곽·벽 명암·재료 결. **적용 조건:** 과한 처리 느낌을 줄이려는 요청.

**관찰할 요소:** 윤곽 주변 밝고 어두운 후광 억제 / 국소 질감과 넓은 톤 구분 / 광원·재료 색의 역할 유지.

**혼동 경계:** 무보정 인증 / 노이즈를 추가해 결함 은폐 / 모든 색보정 금지.

> Keep edge contrast restrained and preserve broad tonal transitions without sharpening halos around the architecture.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S12](https://helpx.adobe.com/photoshop/using/correcting-image-distortion-noise.html), [S15](https://helpx.adobe.com/be_en/camera-raw/desktop/get-started/overview-and-setup/introduction-camera-raw.html). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 깨끗한 공간의 현실적 구조 — rb_clean_space_plausibility

**대상:** 신축 실내·설비 접점·표면. **적용 조건:** 깨끗함·고급 공간이 잠겨 있음.

**관찰할 요소:** 벽·바닥·창틀 접속이 읽힘 / 재료별 반사 차이 / 안정된 지지와 공간 사용성.

**혼동 경계:** 낡음·쓰레기·곰팡이로 현실감 강제 / 깨끗하면 CG 판정.

> The clean lobby retains readable joints, securely placed furniture and distinct stone, fabric and glass responses.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S06](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory), [S17](https://www.arri.com/en/learn-help/lighting/lighting-handbook). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 일상 물체 밀도의 국소 차이 — rb_spatial_density_variation

**대상:** 작업대·선반·비어 있는 동선. **적용 조건:** 생활감은 허용하되 과밀을 요청하지 않음.

**관찰할 요소:** 관련 물건의 작은 군집 / 비어 있는 사용 면 / 보행 경로 분리.

**혼동 경계:** 모든 픽셀 소품 / 무작위 배치 / 생활감이면 빈곤 판정.

> A few used objects cluster near the work surface, leaving the chair space and main passage open.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** 직접 실증 자료 없는 설계 가설. 직접 실증 근거를 확보하지 않은 배치·역학 가설. 우선 수동 검토하고 hard 자동 활성화하지 않는다.

## 앉거나 기대는 지지 관계 — rb_support_compression

**대상:** 몸·좌면·의복. **적용 조건:** 접촉 부위가 보이는 착석·기댐.

**관찰할 요소:** 좌면 위 하중 위치 / 의복 주름이 접점에 대응 / 쿠션 변형은 재료가 부드러울 때만.

**혼동 경계:** 단단한 돌 의자 압축 / 몸이 좌면 관통 / 그림자만으로 지지 대체.

> The seated body meets the cushion at a coherent support area, with fabric folds and a small depression localized to the load.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** 직접 실증 자료 없는 설계 가설. 직접 실증 근거를 확보하지 않은 배치·역학 가설. 우선 수동 검토하고 hard 자동 활성화하지 않는다.

## 유리 표면의 국소 접촉 흔적 — rb_glass_smudge_locality

**대상:** 유리 손잡이 주변·나머지 유리. **적용 조건:** 생활 흔적과 유리 가독성을 함께 허용함.

**관찰할 요소:** 손 닿는 곳에 작은 번짐 / 유리 면 위에 붙은 흔적 / 반사·투과가 다른 구역에서 유지.

**혼동 경계:** 화면 전체 안개 / 렌즈 오염 / 큰 지문을 원경에 강제.

> A faint smudge remains near the glass pull while the rest of the pane keeps its reflection and transparency.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S07](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S11](https://www.cs.columbia.edu/CAVE/databases/tvbrdf/about.php). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 식생과 바닥 조건의 접속 — rb_vegetation_site_relation

**대상:** 풀·흙 틈·수목 밑동. **적용 조건:** 자연·공원 또는 허용된 틈새 식생.

**관찰할 요소:** 줄기·뿌리 위치가 지면과 연결 / 선택 틈에 국소 식생 / 관리된 구역과 양립.

**혼동 경계:** 포장 전체 잡초 / 복제한 식물 타일 / 현실 공원은 무조건 야생화.

> A few small plants emerge from soil at the paving edge, while the maintained walking surface remains clear.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** 직접 실증 자료 없는 설계 가설. 직접 실증 근거를 확보하지 않은 배치·역학 가설. 우선 수동 검토하고 hard 자동 활성화하지 않는다.

## 도막과 금속 바탕의 경계 — rb_coating_substrate_boundary

**대상:** 도장 금속의 마모 부위. **적용 조건:** 작은 도막 마모를 선택함.

**관찰할 요소:** 페인트 층의 제한된 손실 / 노출 바탕의 다른 반사 / 손실 경계와 부품 형태 유지.

**혼동 경계:** 모든 금속에 주황 녹 / 금속 종류 진위 판정 / 전역 스크래치.

> A tiny worn edge exposes metal beneath the paint, with a different highlight response limited to that patch.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S06](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory), [S11](https://www.cs.columbia.edu/CAVE/databases/tvbrdf/about.php). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 큰 광원의 부드러운 명암 — rb_soft_source_environment

**대상:** 흐린 하늘·피사체·바닥. **적용 조건:** 확산광이 요청됨.

**관찰할 요소:** 완만한 그림자 경계 / 인물·배경의 양립하는 면 명암 / 접촉과 깊이 유지.

**혼동 경계:** 소프트광이면 무명암 / 안개로 전체 번짐 / 반드시 회색 우울톤.

> Overcast skylight creates broad gentle transitions on the person and the surroundings while local contact remains legible.

**기존 연결:** `soft_light_shadow_edge_relation`.

**근거 연결:** [S09](https://pbr-book.org/4ed/Light_Sources/Area_Lights). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 작은 광원의 선명한 그림자 — rb_hard_source_environment

**대상:** 직사광·처마·수광면. **적용 조건:** 맑은 직사광 요청이 있음.

**관찰할 요소:** 선명한 투영 경계 / 광원에 맞는 그림자 방향 / 그늘 속 필수 구조 가독성.

**혼동 경계:** 하드광은 CG라는 규칙 / 임의의 고보 무늬 / 항상 클리핑.

> Direct sun draws a crisp eave shadow across the wall and pavement, with the same light direction shaping the person.

**기존 연결:** `hard_light_shadow_edge_relation`.

**근거 연결:** [S09](https://pbr-book.org/4ed/Light_Sources/Area_Lights). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.

## 선택한 필름 계열의 입자 느낌 — rb_film_grain_choice

**대상:** 표시된 사진 전체의 미세 질감. **적용 조건:** 필름 매체나 필름적 질감을 명시함.

**관찰할 요소:** 과하지 않은 불규칙 입자 / 기본 윤곽과 재료 구분 유지 / 디지털 색 노이즈·긁힘과 구분.

**혼동 경계:** 실제 필름 인증 / 센서 노이즈와 동일 원인 / 모든 사진에 필름 추가.

> A restrained irregular film-like grain remains subordinate to the scene's edges and material textures.

**기존 연결:** 새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님.

**근거 연결:** [S13](https://www.kodak.com/content/products-brochures/Film/kodak-essential-reference-guide-for-filmmakers.pdf). 관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.
