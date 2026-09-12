"""Rebuild research proposals only. No runtime mutation, network, index build or image generation."""
import collections
import json
import re
from pathlib import Path

HERE=Path(__file__).resolve().parent
def save(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

# Each line is an authored design, not a measured model capability.
# id | label | owner | prerequisites | visible components | confusion | expression | sources | existing profiles
SPEC='''
architecture_connectivity|기존 건축의 접속 구조|문틀·벽 두께·바닥 경계|문과 벽 및 바닥이 한 프레임에 보임|문틀이 벽 두께 안에 들어감;바닥이 문턱까지 연속됨;창·배관의 부착 위치가 건물 면과 연결됨|건물 이름만 제시;벽에 붙인 평면 벽지;끊긴 문턱|The recessed doorway has visible wall thickness, and the pavement continues to its threshold beneath wall-mounted fixtures.|S04|architectural_threshold_frame_depth_relation
use_trace_affordance|사용 목적에 맞는 생활 흔적|선택한 작업면과 사용하는 소품|사용 중인 공간이며 적절한 소품 1–3개 선택|소품이 안정된 지지면에 놓임;손이 닿는 위치에 사용 물건이 있음;통행 경로가 유지됨|무작위 쓰레기;모든 공간의 빈곤화;부유 소품|A recently used mug rests within reach beside a folded cloth, with the walking route left clear.|S16|-
infrastructure_attachment|일상 설비의 부착과 배치|배수구·배관·배선 중 선택한 두 설비|요청 장소와 시대에 설비가 적합함|배수구가 보행면 안에 맞물림;배관이 벽 지지대에 고정됨;선택 설비가 공간 용도를 방해하지 않음|서울이면 쓰레기 강제;공중에 끝나는 케이블;시대 불일치 설비|A drain cover sits flush with the path while a service pipe follows the wall on visible brackets.|S04|-
repair_patch_locality|국소적인 보수 경계|벽 도장과 보수 부위|보수가 있는 공간을 선택함|한정된 패치 경계;기존 면과 약한 색·결 차이;벽 모서리와 줄눈 연속성 유지|폐허 전역 균열;랜덤 디지털 얼룩|One small repaired patch differs slightly in paint tone while the wall joints continue through the surrounding surface.|S10|-
contact_wear_locality|접촉 위치에 집중된 마모|손잡이·문 가장자리·바닥 동선 중 하나|사용 흔적을 허용하고 해당 부위가 충분히 큼|접촉 부분의 국소 광택·마모;비접촉 부분의 상대적 보존;기하 구조 연속성|모든 표면에 같은 스크래치;카메라 노이즈로 대체|The door pull is slightly polished at the gripping area, while the adjacent painted panel remains intact.|S11|-
water_path_stain|물 경로에 연결된 변색|배수 출구와 그 아래 벽|물 흔적이 있는 외벽을 선택함|출구·돌출부가 보임;그 아래 제한된 흐름 흔적;주변 마른 면과 구분|무작위 세로 줄무늬;벽 전체 곰팡이 자동 생성;사진으로 누수 진단|A faint runoff mark begins below the drain outlet and follows a narrow path down the wall.|S10|-
material_response_contrast|재료별 반사 응답 차이|같은 조명 아래 콘크리트·금속·유리|서로 다른 재료가 인접해 보임|무광 면의 넓은 명암;코팅 금속의 제한된 하이라이트;유리의 장면에 맞는 반사·투과|모든 재료의 동일 플라스틱 광택;재료마다 불필요한 오염|Matte plaster, painted metal and window glass respond differently to the same side light.|S06,S07|-
wet_dry_boundary|젖은 부분과 마른 부분의 경계|바닥·물·반사의 원본|젖은 바닥과 반사 원본이 함께 보임|국소적인 젖음 경계;원본에 대응하는 반사 위치;타일 틈이나 발이 반사를 끊음|아무 출처 없는 네온 줄;바닥 전체 거울;젖음만으로 침수 판정|A shallow wet patch reflects the visible doorway light, interrupted by grout lines and bordered by dry stone.|S07,S11|wet_surface_light_reflection_owner_relation
glass_reflection_transmission|유리 반사와 투과의 공존|창 유리·반사 원본·유리 뒤 공간|반투명 효과가 아닌 투명 유리 창|창틀과 유리 면이 일치;반사 원본과 대응하는 형태;유리 뒤 실내가 선택 영역에서 읽힘|거울로 대체;유리 뒤 물체가 유리 앞에 겹침;모든 반사를 왜곡|The window holds a restrained reflection of the opposite facade while the interior table remains visible through it.|S07|-
window_room_gradient|창에서 실내로 이어지는 밝기 차이|창·가까운 벽·깊은 실내|창이 주요 광원인 장면 선택|창 방향을 받는 면이 밝음;실내 깊이에 따른 명암 차이;피사체와 인접 물체가 같은 빛 방향을 공유|화면 가장자리 비네트;모든 얼굴에 독립 조명;무조건 어두운 방|Daylight enters from the left window, brightening the nearby tabletop and falling to a softer level deeper in the room.|S01,S09|window_seat_daylight_activity_relation
practical_pool|보이는 조명과 조명 영역의 대응|벽등·램프와 수광면|보이는 practical의 효과가 필요함|발광 기구가 식별됨;가까운 수광면의 국소 조도 상승;먼 곳과 영역 경계가 자연스럽게 이어짐|빛나기만 하는 소품;천장등과 무관한 스포트라이트|The wall lamp produces a localized pool on the adjacent wall and table, fading into the surrounding room light.|S01,S09|-
mixed_source_zones|서로 다른 광원의 공간적 색 구역|창광 구역과 실내등 구역|둘 이상의 다른 색 광원을 명시함|두 광원 또는 명확한 방향 단서;각 수광면에 연결된 색 구역;겹침 영역의 점진적인 혼합|전역 청록·주황 LUT;서로 다른 표면 고유색만 있음;모든 야경 네온화|Cool window light reaches the window-side sleeve, while the nearby lamp gives the tabletop a warmer local tone.|S02|-
bounce_owner|근접 표면에서 돌아온 색|색 벽과 가까운 중성 의상 부위|바운스를 받을 지정 owner가 보임|근접한 유색 표면;그쪽을 향한 작은 영역의 색 영향;다른 면은 원래 색을 유지|옷 자체의 배색;전체 화이트밸런스 변화;멀리 떨어진 면의 동일 색|A muted green wall adds a faint green return only to the nearby white sleeve facing it.|S06,S07|-
shared_cast_shadow|피사체와 주변 물체의 투영 그림자 일관성|피사체·선택 주변 물체·바닥|하나의 우세한 광원과 보이는 수광면|선택 물체들의 그림자 방향이 광원과 양립;수광면 기하에 따라 그림자가 변형;인물 그림자가 해당 접촉부와 연결|모든 그림자가 반드시 평행;복수 광원 무시;몸과 무관한 바닥 얼룩|The person and nearby bollard cast shadows consistent with the same late-afternoon light onto the sloping pavement.|S09,S18|hard_light_shadow_edge_relation
soft_ground_contact|확산광 아래 발과 바닥의 접촉|보이는 지지 발·바닥|서 있는 인물의 발과 지지면이 프레임에 있음|밑창과 바닥의 접점;확산광에 맞는 절제된 주변 어둠;무게를 받는 발과 다리 연결|떠 있는 발;모든 발 주위 검은 외곽선;숨겨진 발을 통과 처리|The supporting shoe sits flush on the paving, with only a soft local darkening under the sole in the overcast light.|S09|-
exposure_priority|장면 내 밝기 우선순위|주요 의상·밝은 창·실내 어두운 면|보존할 디테일 영역을 요청에서 지정함|핵심 영역의 읽히는 중간톤;광원에 가까운 영역이 더 밝음;어두운 구역이 자기 위치에서 더 어둡게 남음|모든 면 균일 밝기;얼굴 전체 클리핑;그림자 디테일 보존 금지|Expose for the person and interior surfaces, allowing the distant window to remain brighter without flattening the room's tonal separation.|S14|-
highlight_shoulder|밝은 면에서 흰색까지의 이행|선택 밝은 벽·하이라이트 가장자리|톤 응답이 명시된 사진|밝은 면의 경계에서 점진적 톤 변화;핵심 주변 결 유지;작은 강한 코어와 넓은 밝은 면 구분|광범위 흰 페인트 덮기;반드시 클리핑 요구;안개로 대비 지우기|Bright wall tones approach white gradually, retaining nearby texture around the small brightest reflection.|S14|highlight_rolloff_tone_response
distance_haze|거리에 따른 대기층 분리|근경·먼 건물 또는 산|충분한 시선 거리와 산란 매질을 허용함|근경 대비 보존;먼 형태의 상대적 대비 감소;공간 거리와 변화가 대응|2m 카페의 뿌연 필터;유리 오염;모든 원경의 일률 청색|Distant buildings lose some contrast through the long air path while the nearby railing stays clear.|S08|-
readable_environment_focus|인물 분리와 환경 가독성|초점 인물·중경 장소 단서|장소를 알아볼 수 있어야 하는 인물 사진|인물의 선택 부분이 선명;중경의 구조 단서 2개가 식별됨;멀수록 흐림이 공간적으로 일관됨|조리개 숫자만 만족;모든 배경 추상 보케;전역 샤프닝|Keep the subject distinct while the doorway and sidewalk junction remain recognizable in the middle distance.|S03|shallow_depth_focus_falloff_relation
depth_focus_continuity|가림 경계의 연속적인 초점 이행|선명면·앞뒤의 가는 구조물|얕은 심도 요청이 있음|선명면의 안정된 디테일;거리 순서에 맞는 흐림;가림 가장자리에서 후광·절단 최소화|머리 주위 마스크 테두리;보케를 붙인 콜라주;움직임 번짐|The near railing and distant facade leave focus according to their depth, without a cutout halo around the subject.|S03|shallow_depth_focus_falloff_relation
foreground_occlusion|프레임 가장자리의 실제 전경 가림|의자 등받이 등 전경 물체·중경 대상|주요 대상의 필수 부분 가림을 허용하지 않음|전경 물체 일부가 프레임 밖으로 이어짐;중경 일부를 일관되게 가림;가린 물체의 나머지 형태가 유지|얼굴의 필수 표정 가림;공중에 뜬 장식 스트립;가림 없는 물체 목록|A nearby chair back enters one lower edge of the frame and overlaps the table without covering the person's hands.|S04|three_plane_depth_chain
scale_perspective|공간 깊이와 상대 크기의 일관성|바닥 선·근경 기둥·먼 문|동일 공간의 깊이 표지가 두 개 이상 보임|거리와 양립하는 크기 차이;바닥 선의 일관된 수렴;문·창의 건축 연결|모든 문 같은 화면 크기;배럴 왜곡을 원근으로 대체;광각이면 신체 변형 강제|Paving lines and repeated doorways recede consistently from the near post toward the far end of the street.|S04|wide_angle_near_field_perspective,three_plane_depth_chain
local_motion_blur|움직인 부위에 제한된 번짐|움직이는 손·바퀴 등과 정지 구조|셔터 시간 동안 일부 움직임을 표현함|선택 운동 부위의 방향성 번짐;정지 배경의 상대적 선명도;관절·물체 연결 유지|사진 전체 흐리기;가짜 속도선;모든 손가락 융합|A small blur follows the moving hand while the stationary doorframe and torso remain clear.|S03|-
shared_wind_response|동일 바람과 양립하는 반응|느슨한 옷 끝·머리카락·근처 잎|바람이 있고 서로 다른 물체 반응을 요청함|각 물체의 고정점 유지;가벼운 부분의 그럴듯한 휘어짐;국소 가림·재질 차이를 허용한 방향 양립|모든 잎·옷이 똑같이 평행;인물 머리만 강풍;바람 속도 인증|Loose hair, the free jacket hem and exposed leaves respond compatibly to the breeze, each retaining its own attachment and stiffness.|S04|-
low_light_noise|저조도 명도 노이즈의 제한적 질감|어두운 중성 면·디테일 경계|거친 디지털 촬영 질감을 선택함|미세한 무작위 명도 변화;주요 윤곽 보존;색 얼룩·JPEG 블록과 구분|대낮 저감도에도 강제;필름 긁힘;벽 재질을 노이즈로 대체|Subtle luminance noise is visible in the darker wall tones while edges and material differences remain readable.|S12|-
optional_lens_falloff|선택적인 렌즈 주변 광량 감소|프레임 중심·주변|비네트를 사용하겠다는 요청이 있음|중심에서 주변으로 완만한 변화;장면 안 광원 명암도 유지;검은 테두리가 되지 않음|방 구석 어둠과 혼동;모든 실제 사진의 필수 결함|A mild optical falloff gently darkens the outer field without replacing the room's own lighting pattern.|S12|-
optional_chromatic_fringe|국소적인 색수차 표현|주변부 고대비 경계|색수차를 명시하고 필요한 디테일을 해치지 않음|선택 경계에 약한 색 어긋남;다른 평탄 영역은 유지;색 조명과 구분|전체 RGB 분리;피부 얼룩;현실감 기본값으로 강제|A very slight color fringe appears only at a few high-contrast edges near the image periphery.|S12|-
restrained_processing|처리 흔적을 억제한 경계와 톤|피사체 윤곽·벽 명암·재료 결|과한 처리 느낌을 줄이려는 요청|윤곽 주변 밝고 어두운 후광 억제;국소 질감과 넓은 톤 구분;광원·재료 색의 역할 유지|무보정 인증;노이즈를 추가해 결함 은폐;모든 색보정 금지|Keep edge contrast restrained and preserve broad tonal transitions without sharpening halos around the architecture.|S12,S15|-
clean_space_plausibility|깨끗한 공간의 현실적 구조|신축 실내·설비 접점·표면|깨끗함·고급 공간이 잠겨 있음|벽·바닥·창틀 접속이 읽힘;재료별 반사 차이;안정된 지지와 공간 사용성|낡음·쓰레기·곰팡이로 현실감 강제;깨끗하면 CG 판정|The clean lobby retains readable joints, securely placed furniture and distinct stone, fabric and glass responses.|S06,S17|-
spatial_density_variation|일상 물체 밀도의 국소 차이|작업대·선반·비어 있는 동선|생활감은 허용하되 과밀을 요청하지 않음|관련 물건의 작은 군집;비어 있는 사용 면;보행 경로 분리|모든 픽셀 소품;무작위 배치;생활감이면 빈곤 판정|A few used objects cluster near the work surface, leaving the chair space and main passage open.|S16|-
support_compression|앉거나 기대는 지지 관계|몸·좌면·의복|접촉 부위가 보이는 착석·기댐|좌면 위 하중 위치;의복 주름이 접점에 대응;쿠션 변형은 재료가 부드러울 때만|단단한 돌 의자 압축;몸이 좌면 관통;그림자만으로 지지 대체|The seated body meets the cushion at a coherent support area, with fabric folds and a small depression localized to the load.|S04|-
glass_smudge_locality|유리 표면의 국소 접촉 흔적|유리 손잡이 주변·나머지 유리|생활 흔적과 유리 가독성을 함께 허용함|손 닿는 곳에 작은 번짐;유리 면 위에 붙은 흔적;반사·투과가 다른 구역에서 유지|화면 전체 안개;렌즈 오염;큰 지문을 원경에 강제|A faint smudge remains near the glass pull while the rest of the pane keeps its reflection and transparency.|S07,S11|-
vegetation_site_relation|식생과 바닥 조건의 접속|풀·흙 틈·수목 밑동|자연·공원 또는 허용된 틈새 식생|줄기·뿌리 위치가 지면과 연결;선택 틈에 국소 식생;관리된 구역과 양립|포장 전체 잡초;복제한 식물 타일;현실 공원은 무조건 야생화|A few small plants emerge from soil at the paving edge, while the maintained walking surface remains clear.|S04|-
coating_substrate_boundary|도막과 금속 바탕의 경계|도장 금속의 마모 부위|작은 도막 마모를 선택함|페인트 층의 제한된 손실;노출 바탕의 다른 반사;손실 경계와 부품 형태 유지|모든 금속에 주황 녹;금속 종류 진위 판정;전역 스크래치|A tiny worn edge exposes metal beneath the paint, with a different highlight response limited to that patch.|S06,S11|-
soft_source_environment|큰 광원의 부드러운 명암|흐린 하늘·피사체·바닥|확산광이 요청됨|완만한 그림자 경계;인물·배경의 양립하는 면 명암;접촉과 깊이 유지|소프트광이면 무명암;안개로 전체 번짐;반드시 회색 우울톤|Overcast skylight creates broad gentle transitions on the person and the surroundings while local contact remains legible.|S09|soft_light_shadow_edge_relation
hard_source_environment|작은 광원의 선명한 그림자|직사광·처마·수광면|맑은 직사광 요청이 있음|선명한 투영 경계;광원에 맞는 그림자 방향;그늘 속 필수 구조 가독성|하드광은 CG라는 규칙;임의의 고보 무늬;항상 클리핑|Direct sun draws a crisp eave shadow across the wall and pavement, with the same light direction shaping the person.|S09|hard_light_shadow_edge_relation
film_grain_choice|선택한 필름 계열의 입자 느낌|표시된 사진 전체의 미세 질감|필름 매체나 필름적 질감을 명시함|과하지 않은 불규칙 입자;기본 윤곽과 재료 구분 유지;디지털 색 노이즈·긁힘과 구분|실제 필름 인증;센서 노이즈와 동일 원인;모든 사진에 필름 추가|A restrained irregular film-like grain remains subordinate to the scene's edges and material textures.|S13|-
'''
proposals=[]
for line in SPEC.strip().splitlines():
    ident,label,owner,pre,components,confusion,expr,sources,reuse=line.split('|')
    rid='rb_'+ident
    proposals.append({'id':rid,'label_ko':label,'status':'research_draft','runtime_registered':False,
      'scope':'single_image','owner':owner,'prerequisites':[pre],
      'activation':{'mode':'explicit_relation_or_component_evidence_only','broad_realism_keyword_is_hard_trigger':False,
       'proposed_exact_terms':[label,ident.replace('_',' ')+' relation'],
       'alias_status':'proposal_not_registered'},
      'required_visible_components':components.split(';'),'confusion_boundaries':confusion.split(';'),
      'candidate_expression_en':expr,'source_ids':sources.split(','),
      'evidence_level':'authored_design_informed_by_sources_not_generator_validation',
      'existing_profile_ids':[] if reuse=='-' else reuse.split(','),
      'integration_disposition':'compare_and_reuse_with_scope_check' if reuse!='-' else 'proposed_new_relation',
      'evaluation':{'require_all_components_on_declared_owner':True,'partial_is_fail':True,
       'unobservable_status':'unscored_not_pass','generated_image_test':'not_run','user_judgment':'pending'}})
design_only={'rb_use_trace_affordance','rb_infrastructure_attachment','rb_shared_wind_response',
 'rb_spatial_density_variation','rb_support_compression','rb_vegetation_site_relation'}
for p in proposals:
    p['source_support_scope']='관련 물리 또는 혼동 경계만 지원한다. 구체 장면·구성요소·PASS 기준은 연구 설계이며 출처의 실험 결론이 아니다.'
    if p['id'] in design_only:
        p['source_ids']=[]
        p['evidence_level']='authored_design_hypothesis_without_direct_empirical_source'
        p['source_support_scope']='직접 실증 근거를 확보하지 않은 배치·역학 가설. 우선 수동 검토하고 hard 자동 활성화하지 않는다.'
    if p['id']=='rb_local_motion_blur':
        p['source_ids']=['S19']
        p['source_support_scope']='Canon의 셔터에 의한 운동 표현 설명에 대응; 지정 부위·방향·정지면 비교는 별도 설계다.'
    if p['id']=='rb_architecture_connectivity':
        p['source_support_scope']='S04는 원근 기하만 지원한다. 설비·건축 접속 예시는 일반 설계 가설이며 지역별 건축 사실이 아니다.'
save('visual-proposals.json',{'schema_version':'photo-realistic-background-proposals/research-v1','proposals':proposals})

# A bundle is an optional combination, never a runtime-selected template.
# id | scenario | mandatory relations for this example only | optional relations | exclude | authored realization
BUNDLES='''
cafe_day|낮 카페 창가|window_room_gradient,readable_environment_focus,use_trace_affordance|glass_smudge_locality,foreground_occlusion|헤이즈·필름 자동 추가|Window daylight reaches a used table beside the seated adult; a mug and folded cloth stay within reach, and the doorway remains recognizable behind the table.
residential_street|서울 주택가를 참고한 가상 골목|architecture_connectivity,infrastructure_attachment,scale_perspective|repair_patch_locality,contact_wear_locality|동네 진위 인증·쓰레기 강제|Show a continuous residential path with a recessed entrance, a flush drain and a wall-mounted service pipe; the doorways recede coherently into the street.
park_overcast|흐린 날 관리된 공원|vegetation_site_relation,soft_source_environment,soft_ground_contact|foreground_occlusion,readable_environment_focus|안개·진한 그림자 강제|An adult stands on a maintained park path under overcast skylight; planted edges meet the soil naturally and the supporting shoe rests flush on the paving.
clean_hotel|깨끗한 고급 호텔|clean_space_plausibility,material_response_contrast,glass_reflection_transmission|practical_pool|낡음·소품 과밀·무조건 무광|Keep the lobby clean, with distinct stone, upholstery and glass responses; the window preserves both a restrained exterior reflection and a readable interior beyond it.
storefront_night|야간 점포 앞|practical_pool,mixed_source_zones,exposure_priority|low_light_noise,soft_ground_contact|모든 야간을 네온·젖은 바닥으로 변환|The warm storefront lamp lights the nearby wall while cooler street illumination reaches the far side of the subject; preserve local brightness and color boundaries.
blue_hour|블루아워 거리|mixed_source_zones,readable_environment_focus,architecture_connectivity|practical_pool|깊은 밤 LUT로 대체|Remaining cool sky light keeps the street and entrances readable while selected warm fixtures form local pools below them.
sunny_courtyard|맑은 낮 중정|hard_source_environment,shared_cast_shadow,material_response_contrast|contact_wear_locality|하드광 배제·클리핑 강제|Direct sun projects the eave shadow across the wall and paving; the adult and a nearby post share the same acting light direction.
rain_aftermath|비가 그친 보도|wet_dry_boundary,soft_ground_contact,architecture_connectivity|water_path_stain|실시간 폭우·전체 수면|A shallow wet patch reflects the doorway lamp within a visible dry boundary; paving joints interrupt the reflection below the grounded shoes.
dry_noon|건조하고 맑은 거리|scale_perspective,hard_source_environment,clean_space_plausibility|infrastructure_attachment|물웅덩이·도시 안개 자동 추가|Keep the dry street clear and sunlit, with coherent doorway scale, firm paving joints and crisp shadows from the visible eaves.
distant_city|원경 도시 전망|distance_haze,scale_perspective,material_response_contrast|foreground_occlusion|근경까지 전역 뿌연 처리|The near railing stays clear while the distant building layers lose contrast gradually along the long viewing path.
maintained_home|정리된 생활 실내|use_trace_affordance,spatial_density_variation,support_compression|window_room_gradient|집이면 가난·무조건 어수선함|A seated adult uses a clear work surface with a small cluster of nearby objects; the cushion and clothing show a coherent support contact.
repair_workshop|사용 중인 작업실|contact_wear_locality,repair_patch_locality,material_response_contrast|coating_substrate_boundary|모든 물체의 폐허화|Local wear appears at the bench's hand-contact edge and the door pull, while intact surfaces retain their different material responses.
day_transit|주간 정류장|infrastructure_attachment,foreground_occlusion,readable_environment_focus|local_motion_blur|노선명 진위·군중 자동 생성|A shelter edge enters the frame near the camera; its supports meet the paving, and the waiting area and entrance remain legible behind the subject.
night_transit|야간 정류장|practical_pool,exposure_priority,glass_reflection_transmission|low_light_noise|스마트폰 야경은 반드시 거친 노이즈|The shelter fixture illuminates its immediate seat and pavement; the glass carries a local street reflection without erasing the space beyond it.
environment_editorial|환경이 읽히는 에디토리얼|readable_environment_focus,architecture_connectivity,shared_cast_shadow|bounce_owner|에디토리얼 금지·포즈 제거|Preserve the intended editorial pose and styling while the doorway and paving remain readable, with light and cast shadows integrated into the same space.
breeze_garden|약한 바람의 정원|shared_wind_response,vegetation_site_relation,soft_ground_contact|foreground_occlusion|모든 잎·옷 방향을 평행하게 정렬|Loose hair, the jacket hem and exposed leaves respond compatibly to a light breeze while the feet remain supported by the path.
shallow_bokeh_retained|얕은 심도를 유지한 현장 인물|depth_focus_continuity,soft_ground_contact,practical_pool|restrained_processing|현실감 때문에 f/4로 무단 변경|Keep the requested shallow focus; the nearby lamp's pool and visible ground contact integrate the subject even while the distant background remains blurred.
film_location|필름적 질감의 현장 사진|film_grain_choice,architecture_connectivity,exposure_priority|contact_wear_locality|필름 진위 인증·센서 노이즈 혼합|The doorway and path retain coherent structure under restrained film-like grain, with the interior left darker than the bright exterior opening.
clean_clinic|청결한 진료 공간|clean_space_plausibility,material_response_contrast,soft_source_environment|readable_environment_focus|오염·균열·곰팡이 기본값|Keep the clinical room clean and orderly, with readable furniture supports and different responses from painted walls, fabric and glass under broad light.
glass_entry|유리 출입문|glass_reflection_transmission,glass_smudge_locality,architecture_connectivity|contact_wear_locality|유리를 거울·안개로 대체|A small contact smudge stays near the door pull; the rest of the pane preserves the outside reflection, inside space and frame thickness.
'''
bundles=[]
for line in BUNDLES.strip().splitlines():
    ident,label,required,optional,exclude,expr=line.split('|')
    bundles.append({'id':'rbb_'+ident,'scenario_ko':label,'status':'research_draft','runtime_registered':False,
      'required_if_this_bundle_is_explicitly_selected':['rb_'+x for x in required.split(',')],
      'optional_proposal_ids':['rb_'+x for x in optional.split(',')],
      'do_not_infer':exclude,'example_en':expr,
      'selection_policy':'unordered_optional; respect locked location, medium, appearance, action, camera, lighting and color',
      'candidate_pack_exposure':'not_run','image_test':'not_run'})
save('candidate-bundles.json',{'schema_version':'photo-realistic-background-bundles/research-v1','bundles':bundles})

src=json.loads((HERE/'source-conversation.json').read_text())
message=src['turns'][0]['items'][1]['text']
heading='introduction';occurrences=[];unique={}
for line_no,line in enumerate(message.splitlines(),1):
    if line.startswith('#'):heading=re.sub(r'^#+\s*','',line)
    for m in re.finditer(r'`([^`]+)`',line):
        term=m.group(1)
        row={'occurrence_id':'kw_occ_'+str(len(occurrences)+1).zfill(3),'text':term,'heading':heading,'line':line_no}
        occurrences.append(row)
        unique.setdefault(term,{'id':'kw_'+str(len(unique)+1).zfill(3),'text':term,'occurrence_ids':[], 'headings':[]})
        unique[term]['occurrence_ids'].append(row['occurrence_id'])
        if heading not in unique[term]['headings']:unique[term]['headings'].append(heading)
routes={
 1:['architecture_connectivity','use_trace_affordance','clean_space_plausibility'],
 2:['contact_wear_locality','repair_patch_locality','water_path_stain','spatial_density_variation'],
 3:['window_room_gradient','practical_pool','mixed_source_zones','bounce_owner'],
 4:['exposure_priority','highlight_shoulder','shared_cast_shadow','soft_source_environment'],
 5:['distance_haze'],6:['material_response_contrast','glass_reflection_transmission','wet_dry_boundary'],
 7:['depth_focus_continuity','local_motion_blur','low_light_noise','optional_lens_falloff','optional_chromatic_fringe'],
 8:['readable_environment_focus','depth_focus_continuity'],9:['foreground_occlusion','scale_perspective'],
 10:['infrastructure_attachment','vegetation_site_relation','spatial_density_variation'],
 11:['bounce_owner','shared_cast_shadow','soft_ground_contact','support_compression','shared_wind_response'],
 12:['restrained_processing','film_grain_choice','low_light_noise'],13:[],14:[]}
for term,row in unique.items():
    h=next((int(m.group(1)) for x in row['headings'] if (m:=re.match(r'(\d+)\.',x))),0)
    row.update({'research_family':h,'related_proposal_ids':['rb_'+i for i in routes.get(h,[])],
        'mapping_granularity':'section_level_research_route_not_exact_alias','hard_activation':False,
        'treatment':'contextual_visual_cue','note':'구체 owner·조건을 선택한 후 관계로 변환; 단어 자체의 생성 효과는 미검증.'})
    t=term.lower()
    if len(term.split())>12 or term.startswith('a woman'):
        row.update(treatment='compound_example',note='복합 예문으로 보존하며 단일 키워드나 exact alias로 등록하지 않는다.')
    elif 'focus breathing' in t:
        row.update(treatment='split_temporal_from_static',note='초점 변화에 따른 화각 변화와 imperfect focus를 분리; 브리딩은 정지 이미지에서 인증하지 않는다.',related_proposal_ids=[])
    elif any(x in t for x in ['raw','unretouched','unstaged','uncontrived','documentary','on-location','on location','actual location','real-world location','real physical environment','handheld']):
        row.update(treatment='style_or_provenance_split',note='표현 목표와 실제 장소·촬영·보정 이력을 분리; 생성 픽셀은 제작 이력 증거가 아니다.')
    elif h==13 or t in ['photorealistic','8k','8k uhd','masterpiece','best quality','global illumination','hdr']:
        row.update(treatment='contextual_style_or_quality_label',note='전역 금지어로 등록하지 않는다. HDR·고급 공간·선명도·정돈은 현실감과 양립 가능하다.')
    elif any(x in t for x in ['noise','grain','vignet','aberration','barrel','clipping','underexposure','haze','humidity','airborne','moisture','imperfect white balance']):
        row.update(treatment='optional_conditioned_effect',note='매체·날씨·거리·광학·노출 조건 또는 명시 요청에 한정; 현실감 요청의 자동 필수값으로 금지.')
    elif re.search(r'\b\d+mm\b|f/\d',t):
        row.update(treatment='capture_parameter_not_visual_proof',note='촬영 거리·포맷·배경 거리와 함께 해석; 조리개만으로 가독성 PASS 불가.')
core_spec='''
on-location photography|architecture_connectivity,clean_space_plausibility|장소 표현과 실제 촬영 이력 분리
real-world location|architecture_connectivity,scale_perspective|실재 장소 인증 없이 접속·원근 구조로 구체화
lived-in environment|use_trace_affordance,spatial_density_variation,contact_wear_locality|사용 위치·접촉 부위·통행 공간; 쓰레기·빈곤으로 자동 확장 금지
documentary photography|use_trace_affordance,foreground_occlusion|스타일과 사건·제작 사실 분리; 소품·구도는 선택 가설
unstaged|foreground_occlusion|비연출 이력은 픽셀로 판정 불가; 우연한 프레이밍도 자동 강제하지 않음
available light|window_room_gradient,practical_pool,soft_source_environment,hard_source_environment|자연광과 기존 인공 광원 모두 가능; 화면 내 광원 노출은 별도 조건
mixed lighting|mixed_source_zones,bounce_owner|색의 원인과 지정 수광면 구역 연결; LUT·표면색과 구분
natural exposure|exposure_priority,highlight_shoulder|필수 디테일과 밝기 위계; 클리핑 의무 없음
uneven illumination|window_room_gradient,practical_pool|장면 위치와 연결된 조도 차이; 화면 비네트로 대체 금지
natural shadow falloff|soft_source_environment,hard_source_environment,shared_cast_shadow|조도 감소·그림자 경계·톤 응답은 문맥에서 분리
incidental background details|infrastructure_attachment,use_trace_affordance|무작위 물건 수 대신 부착·지지·사용 위치
subtle material wear|contact_wear_locality,coating_substrate_boundary|접촉 부위에 제한된 변화; 전역 스크래치 금지
weathered surfaces|water_path_stain,repair_patch_locality|장소·재료·상태 지정; 모든 건물 노후화 금지
realistic surface roughness|material_response_contrast|미세면 개별 과장 대신 반사 분포와 재료 차이
imperfect reflections|glass_reflection_transmission,wet_dry_boundary|원본·반사면·가림 유지; 무작위 왜곡 금지
atmospheric haze|distance_haze|거리·매질 조건부; 초점 흐림·렌즈 오염과 분리
realistic spatial layering|foreground_occlusion,scale_perspective|가림·상대 크기·원근이 연결된 공간
natural optical depth of field|depth_focus_continuity,readable_environment_focus|심도와 환경 가독성 별도 선택; 수치만으로 PASS 불가
subtle sensor noise|low_light_noise|선택적 디지털 질감; 필름 입자·표면 결과 구분
minimally processed RAW photograph|restrained_processing|경계·톤 보존; RAW 파일·무보정 이력 인증 불가
'''
core=[]
for line in core_spec.strip().splitlines():
    term,ids,note=line.split('|');row=unique[term]
    row.update(related_proposal_ids=['rb_'+x for x in ids.split(',')],mapping_granularity='reviewed_core_keyword_to_conditional_relations',note=note)
    core.append({'keyword_id':row['id'],'term':term,'proposal_ids':row['related_proposal_ids'],
        'decision':note,'hard_activation':False,'generation_effect':'not_verified'})
save('core-keyword-map.json',{'schema_version':'photo-realism-core-keyword-map/research-v1','rows':core})
save('keyword-inventory.json',{'schema_version':'photo-research-keyword-inventory/v1','conversation_id':src['thread']['id'],
 'extraction':'All inline-code spans of the referenced assistant message; includes examples and repeated core keywords.',
 'occurrence_count':len(occurrences),'unique_span_count':len(unique),'occurrences':occurrences,'terms':list(unique.values())})

# Specification fixtures. No entry here claims an executed runtime or pixel result.
cases=[]
for p in proposals:
    for kind in ['positive','near_miss']:
        cases.append({'id':p['id']+'_'+kind,'kind':'pixel_rubric_specification','proposal_id':p['id'],
         'input':p['candidate_expression_en'] if kind=='positive' else p['confusion_boundaries'][0],
         'preconditions':p['prerequisites'],'expected':{'qualified':kind=='positive',
           'required_components':p['required_visible_components'],'declared_owner':p['owner']},
         'reason':'모든 구성요소가 지정 owner에서 읽힐 때만 통과' if kind=='positive' else '인접 효과가 필수 관계를 대체함',
         'execution_status':'not_run'})
special=[
 ('broad_ko','현실적인 배경','advisory_only','오염·헤이즈·노이즈 hard profile 생성 금지'),
 ('broad_en','real-world location','advisory_only','실제 장소 인증 금지'),
 ('clean_hotel','깨끗한 신축 호텔의 현실적인 사진','preserve_cleanliness','생활감으로 마모·쓰레기 삽입 금지'),
 ('shallow_lock','85mm f/1.4 크리미 보케는 유지하고 합성 느낌만 줄여줘','preserve_camera_intent','f/4로 바꾸지 않고 빛·접촉으로 통합'),
 ('dry_weather','건조하고 먼지 없는 맑은 낮 거리','no_added_wetness_or_haze','현실감 패키지로 비·안개 추가 금지'),
 ('clean_digital','낮 저감도 디지털 사진, 노이즈 없이','no_added_grain','센서 노이즈 필수화 금지'),
 ('night_computational','깨끗한 스마트폰 야간 모드 사진','low_noise_allowed','밤이면 노이즈 hard 활성화 금지'),
 ('breathing_static','정지 사진에 focus breathing','temporal_unverifiable','imperfect focus와 동의어 병합 금지'),
 ('hdr','실제 HDR 사진의 자연스러운 톤','no_global_hdr_ban','HDR와 과도한 국소 대비를 구분'),
 ('cinematic','현실적인 영화적 현장 인물 사진','preserve_style','cinematic 또는 조명장비 자동 배제 금지'),
 ('unseen_feet','허리 위 사진, 발 접촉 그림자','unscored_visibility_conflict','보이지 않는 owner를 PASS 금지'),
 ('offframe_light','화면 밖 창문에서 들어온 빛','causal_source_offframe_allowed','모든 광원을 화면 안에 삽입 금지'),
 ('no_fake_seoul','서울 주택가를 참고한 가상 골목','fictional_location','주소·전형적 설비의 진위 주장 금지'),
 ('short_airpath','2미터 거리의 깨끗한 실내','no_required_haze','대기 원근과 얕은 심도 혼동 금지'),
 ('film_digital','필름 입자와 센서 색노이즈의 차이','separate_causes','동일 원인으로 병합 금지'),
 ('multi_source','두 가로등에서 오는 두 그림자','allow_multiple_consistent_shadows','모든 그림자 하나로 강제 금지'),
 ('sun_perspective','가까운 램프 아래 두 물체의 그림자','geometric_consistency','동일 광원이라도 그림자는 반드시 평행하지 않음'),
 ('grain_vs_wall','벽의 미세한 질감은 살리고 노이즈는 없게','separate_surface_and_capture','벽 질감을 필름으로 대체 금지'),
 ('clean_metal','산화 없는 새 알루미늄 프레임','preserve_material_state','모든 금속 주황 녹 강제 금지'),
 ('real_doc','documentary style generated image','no_capture_authenticity_claim','다큐멘터리 스타일을 실제 사건 기록으로 인증 금지'),
 ('no_wind','바람 없는 실내 사진','no_wind_augmentation','인물·식생 바람 프로필 활성화 금지'),
 ('intensity_scope','유리 손잡이 주변에만 약한 지문','local_scope_only','유리 전체와 렌즈에 얼룩 번짐 금지'),
 ('color_owner','초록 벽 옆 흰 소매에만 약한 색반사','declared_owner_only','다른 소매나 배경 초록색으로 대체 통과 금지'),
 ('exposure_detail','밝은 창 앞 인물과 의상 디테일 유지','preserve_critical_detail','현실감 이유로 의상이나 얼굴 클리핑 금지')]
for ident,query,expect,reason in special:
    cases.append({'id':'rb_boundary_'+ident,'kind':'routing_and_intent_specification','input':query,
        'expected':expect,'reason':reason,'execution_status':'not_run'})
(HERE/'evaluation-cases.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in cases))

# Generate a readable full catalog from the exact structured records.
links={x['id']:x for x in json.loads((HERE/'sources.json').read_text())['sources']}
catalog=['# 현실적 배경 시각 관계 상세 카탈로그','',
 '모든 항목은 연구 제안이다. 출처는 물리·관행·경계 판단을 지원하며, 아래 장면과 판정 기준은 이를 바탕으로 작성한 설계다. 생성 효과는 아직 시험하지 않았다.','']
for p in proposals:
    catalog += ['## '+p['label_ko']+' — '+p['id'],'', '**대상:** '+p['owner']+'. **적용 조건:** '+'; '.join(p['prerequisites'])+'.','',
      '**관찰할 요소:** '+' / '.join(p['required_visible_components'])+'.','',
      '**혼동 경계:** '+' / '.join(p['confusion_boundaries'])+'.','',
      '> '+p['candidate_expression_en'],'',
      '**기존 연결:** '+(', '.join('`'+x+'`' for x in p['existing_profile_ids']) or '새 관계 제안; 관련 데이터가 전혀 없다는 뜻은 아님')+'.','',
      '**근거 연결:** '+(', '.join('['+s+']('+links[s]['url']+')' for s in p['source_ids']) or '직접 실증 자료 없는 설계 가설')+'. '+p['source_support_scope'],'']
(HERE/'visual-catalog.md').write_text('\n'.join(catalog))
print(json.dumps({'proposals':len(proposals),'bundles':len(bundles),'specification_cases':len(cases),
 'unique_spans':len(unique),'occurrences':len(occurrences)},ensure_ascii=False))
