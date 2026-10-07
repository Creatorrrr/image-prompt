#!/usr/bin/env python3
"""Build reviewable research proposals, never active candidate assets."""
import collections, csv, hashlib, json
from pathlib import Path
OUT=Path(__file__).resolve().parent
BASE=OUT.parent
def save(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=json.loads((OUT/'SOURCE-DECOMPOSITION.json').read_text())
original=json.loads((BASE/'SOURCE-KEYWORDS.json').read_text())
oldunits={e['id']:e for e in json.loads((BASE/'SEMANTIC-UNITS.json').read_text())['units']}
inv=json.loads((OUT/'CURRENT-INVENTORY.json').read_text())
cards=[]
def ks(*numbers):return [f'K{n:03}' for n in numbers]
def card(number,title,keys,kind,slots,owner,components,relations,keep,optional,confounds,existing,sources,cases,priority='P0'):
    cards.append({'id':f'VD-{number:03}','title_ko':title,'keyword_ids':ks(*keys),'prior_card_ids':sorted({p for k in ks(*keys) for p in oldunits[k]['proposal_ids']}),'proposal_kind':kind,'priority':priority,'target_slots':slots,'owner_scope':owner,'required_components_en':components,'directed_relations':[{'subject':s,'type':t,'object':o} for s,t,o in relations],'source_case_keep_ko':keep,'optional_realization_ko':optional,'confusion_boundaries_ko':confounds,'existing_ids_to_review':existing,'research_source_ids':sources,'regression_examples':cases,'minimum_view_ko':'모든 선택된 소유자·경계·관계가 동시에 읽히는 화면. 세부 질감은 native 크기로 추가 확인한다.','runtime_ready':False,'activation_policy':'후보 조회는 frozen core 이후의 선택 도움이다. 키워드·유사도만으로 hard 의무를 만들지 않는다. 요청에 명시된 구성은 후보를 고르지 않아도 보존한다.','evidence_status':'source-derived paraphrase plus researcher-designed relations; historical original and native pixels not independently authenticated','pixel_gate':'Every selected component and directed relation must be visible on its declared owner. A wrong owner, substitute, or partial realization fails; unavailable or blocked evidence remains unscored.'})

card(1,'닫힌 허리 베스트와 중앙의 안쪽 탑·넥타이', [8,9,10,11,12,15,52,53], 'new_relation_trial', ['wardrobe_style','garment_detail','wearable_accessory'], '같은 착용자의 재킷·탑·베스트·칼라·넥타이, 각각 독립 층',
 ['The vest waist panel has a continuous closed front over the inner top.','The side straps and panels ascend along the sides while the central upper-chest area retains the inner top and tie.','The jacket opening reveals the selected inner layers without merging their edges.'],
 [('vest waist panel','lies_over','inner top waist region'),('side straps','attach_to','vest side panels'),('jacket opening','reveals','inner top and vest'),('tie','lies_over','inner top central front')],
 'S02 문맥: 검정 베스트·흰색 U넥 골지 탑·검정 가죽 넥타이·파란 칼라·핀스트라이프 재킷을 사례 조건으로 보존한다. 닫힌 허리 앞판과 열린 상흉부 중앙은 서로 다른 영역이다.',
 '일반형의 색·문양·버클 수·숨은 패드 치수는 요청에서 따로 정한다. busk, lacing, boning을 자동 추가하지 않는다.',
 ['닫힌 앞판을 중앙이 뚫린 하네스로 대체','탑을 제거하거나 베스트와 한 벌로 합침','닫힌 허리 조건을 가슴 중앙까지 완전 차폐로 확대'],
 ['slot:wardrobe_style:clt_ct023_v2','slot:wardrobe_style:y2kr_corset_top','slot:garment_detail:ccx_cc26_01'], ['A04','A06','R08'],
 [{'input_ko':'흰 탑 위 베스트 허리 앞판은 닫고 가슴 중앙의 탑과 넥타이는 남겨줘.','expected':'closed waist and visible upper center coexist'}, {'input_ko':'코르셋처럼 보이는 절개선만 있는 드레스.','expected':'no layered vest, busk or lacing obligation'}, {'mutation':'remove inner top while preserving black vest','expected':'FAIL_SOURCE_CASE_KEEP'}])
card(2,'골지 높낮이·평면 줄무늬·봉제선의 별도 소유', [8,9,15,181], 'extend_review', ['wardrobe_style','texture','garment_detail'], '골지 탑 표면, 재킷 인쇄/직조 무늬, 패널 봉제선',
 ['Raised knit ribs and recessed channels repeat on the declared top surface.','The selected stripe pattern follows the jacket panels without becoming raised knit ribs.','Seams remain garment construction boundaries rather than skin marks.'],
 [('raised ribs','belong_to','top fabric'),('pinstripes','follow_surface_of','jacket panels'),('seam channels','divide','garment panels')],
 'K009의 U자 목선·흰 바탕·세로 골, S02 재킷의 핀스트라이프는 해당 사례 안에서 보존한다.',
 '골 간격의 변화는 편직 종류·당김·관점에 따른 변형 후보다. 모든 골지를 일정 치수나 동일 신장률로 고정하지 않는다.',
 ['평면 스트라이프를 골지 돌출로 통과','faille의 가로 직조 리브를 세로 니트로 자동 대체','주름·모공·피부 긁힘을 옷의 골로 통과'],
 ['y2kr_rib_tank','sw_rib','vg_faille_crossgrain_ribs_profile','slot:wardrobe_style:y2kr_rib_tank'], ['A01','A02','A03','A06'],
 [{'input_ko':'U넥 탑 표면의 세로 돌출 골과 골 사이 음영을 보여줘.','expected':'top-owned relief'}, {'input_ko':'매끈한 재킷에 평평한 가는 줄무늬.','expected':'no rib relief obligation'}, {'mutation':'put ribs only on background curtain','expected':'FAIL_OWNER'}])
card(3,'흘러내린 한쪽 끈과 반대쪽 지지의 비대칭', [29,30,33], 'new_relation_trial', ['garment_detail','wearable_accessory'], '같은 드레스의 두 어깨끈과 앞뒤 몸판',
 ['One strap has left its shoulder support and lies loosely on the outside of that upper arm.','The opposite strap remains over its own shoulder.','Both straps retain their declared garment attachment endpoints.'],
 [('fallen strap','rests_on','same-side upper arm'),('retained strap','passes_over','opposite shoulder'),('strap endpoints','attach_to','same garment panels')],
 'K030의 한쪽 상태와 다른 쪽 잔존 지지를 보존한다. 끈을 내린 행위자나 미래의 탈의는 주어지지 않았다.',
 '끈의 좌우는 요청으로 결정한다. 끈 폭·소재·늘어진 곡선 크기는 독립 변수다.',
 ['원래 한 끈인 원숄더 디자인으로 대체','두 끈을 모두 어깨 아래로 내림','머리에 가린 끈을 흘러내린 끈으로 통과'],
 ['pfe_one_shoulder','slot:garment_detail:pfe_one_shoulder_candidate'], ['A04'],
 [{'input_ko':'오른쪽 끈만 위팔 바깥에 내려오고 왼쪽은 어깨에 남아 있어.','expected':'asymmetric current state'}, {'input_ko':'원래 한쪽 어깨만 지지하는 드레스 디자인.','expected':'not a fallen two-strap state'}, {'mutation':'hide retained strap behind hair','expected':'UNOBSERVABLE_NOT_PASS'}])
card(4,'레이스 구멍·의복 파임·원단 비침의 분리', [25,27,28,31,32,34,35,37], 'extend_review', ['garment_detail','surface_material'], '레이스 띠, 바탕 원단, 목선의 열린 영역, 그 뒤의 지정 대상',
 ['Openwork cells belong to the attached lace strip.','The base garment remains a separate surface with its own opacity.','A neckline opening exposes only its declared bounded region.'],
 [('lace strip','attaches_along','base garment edge'),('openwork cells','interrupt','lace strip coverage'),('neckline boundary','bounds','declared exposed region')],
 '원문이 명시한 가슴골은 지우지 않고 나머지 의복 가림도 남긴다. 레이스의 빈 셀은 그 아래 바탕층에 가려질 수 있다.',
 '꽃무늬·스캘럽 한 가지를 모든 lace trim의 필수 도안으로 고정하지 않는다. 투과도는 해당 원단/영역에만 적용한다.',
 ['레이스 프린트를 실제 구멍으로 통과','레이스 띠 때문에 드레스 전체를 투명화','일반 neckline에 추가 파임/가슴골을 발명'],
 ['lace_trim_attached_edge','slot:garment_detail:lace_trim_edge','decolletage_neckline_exposure'], ['A03','A05','A06','R07'],
 [{'input_ko':'불투명 바탕의 목선 가장자리에 열린 셀을 가진 레이스 띠를 달아줘.','expected':'open lace over independently opaque base'}, {'input_ko':'새틴에 인쇄된 꽃무늬 테두리.','expected':'not openwork lace'}, {'mutation':'replace bounded neckline with removed bodice','expected':'FAIL_BOUNDARY'}])
card(5,'젖음·밀착·반사·부분 비침의 조건부 결합', [16,17,18,19,20,21,22,23,24,26,35,36,37,38,39,40,42], 'claim_guard', ['surface_material','texture','garment_detail'], '지정된 원단/머리/피부의 국소 영역과 광원·겹침 경로',
 ['Wetness, adherence, surface reflection and light transmission remain separate selected properties.','Any transmitted underlying color passes through the declared cloth region while its textile boundary stays visible.','Highlight placement follows the local surface orientation and the declared light-view geometry.'],
 [('wet region','belongs_to','declared material owner'),('cloth overlap','changes_path_through','selected textile layers'),('highlight','is_received_on','source-facing local surface')],
 'K042의 wet OR clingy를 AND로 바꾸지 않는다. K035/037의 약한 비침은 유지하되 젖음 하나만으로 추가 비침을 만들지 않는다.',
 '젖어 어두워지는 영역·늘어진 주름·겹쳐 덜 비침은 선택된 소재와 장면의 실현 예다. 무광, 가죽 결, 주름 산의 밝음을 전 소재의 법칙으로 만들지 않는다.',
 ['wet를 transparent로 자동 동의어화','반사 띠를 젖음의 유일한 증거로 삼음','능선은 언제나 밝고 골은 언제나 어둡다고 강제','NIR/UV 투과 연구를 가시광 노출 증거로 전용'],
 ['pfe_opaque_fit','satin_directional_luster_drape_surface','wet_damp_clumped_hair_state'], ['A03','A05','A06','A08','R11','R12','R20'],
 [{'input_ko':'젖었지만 불투명한 탑.','expected':'wetness without transmission'}, {'input_ko':'마른 원단이 몸에 붙고 광택은 약해.','expected':'cling without wet or gloss'}, {'mutation':'turn wet-or-clingy into both mandatory','expected':'FAIL_LOGICAL_OPERATOR'}])
card(6,'거울의 결로 표면과 얼굴 초점의 다른 경로', [41,43,59,61,77,79], 'new_relation_trial', ['surface_material','focus','garment_detail'], '거울 전면의 결로 패치, 거울 반사 경로, 인물 얼굴',
 ['Condensation droplets or a scattering haze occupy a localized patch of the mirror surface.','The reflected image loses local contrast through that patch rather than the whole scene acquiring uniform blur.','The requested face-focus hierarchy remains readable through the selected usable viewing region.'],
 [('condensation patch','lies_on','mirror front surface'),('scattering patch','attenuates','local reflected image contrast'),('selected focus','prioritizes','requested face plane')],
 'K043의 김 서림·물방울 소유자를 거울로 유지하고 K079의 얼굴 주 초점을 별도로 보존한다.',
 '물막이 항상 희거나 불투명한 것은 아니다. 닦인 영역·흐른 자국·방울 크기는 원문/선택에 있을 때만 사용한다.',
 ['렌즈 디포커스를 거울 결로로 통과','얼굴 자체를 얼룩/백색 막으로 덮음','거울이 김 서렸다는 이유로 젖은 의상을 추가'],
 ['slot:texture:condensation_window_smear_texture','rb_glass_reflection_transmission'], ['A06','A07','A09'],
 [{'input_ko':'거울 한쪽 결로는 남기고 반사된 얼굴은 선명하게 읽히게.','expected':'surface patch and face focus coexist'}, {'input_ko':'맑은 거울 앞에서 배경만 디포커스.','expected':'not condensation'}, {'mutation':'haze the face skin instead of mirror','expected':'FAIL_OWNER'}])
card(7,'초커 앞의 열린 금속 고리와 부착점', [46,47], 'new_relation_trial', ['wearable_accessory','garment_detail'], '초커 띠, 그 앞 중앙의 고리, 고리 안의 실제 배경/띠',
 ['A rigid circular metal perimeter is attached at the front center of the declared choker band.','Its center is an actual aperture rather than a solid round medallion.','The band follows the neck while the rigid ring retains its own shape.'],
 [('ring fitting','attaches_to','choker front center'),('ring perimeter','bounds','open aperture'),('choker band','follows_contour_of','neck')],
 'S04의 검정 띠와 은색 O-ring은 사례값이다. 고리 안으로 보이는 대상은 실제 시점·겹침에 맞춘다.',
 '금속 반사와 얕은 접촉 그림자는 광원/시점에 따른 실현 단서다. 고리가 있다고 사슬·견인·조임을 추가하지 않는다.',
 ['단단한 원판 팬던트로 대체','귀걸이/손가락 고리를 목의 고리로 통과','고리 중앙에 검정 색칠만 해서 구멍처럼 처리'],
 ['slot:wearable_accessory:ctx_c019','slot:wearable_accessory:y2kr_grommet','slot:wearable_accessory:y2kr_tattoo_choker'], ['A06','R11'],
 [{'input_ko':'검정 목 띠 앞 중앙에 가운데가 빈 은색 고리가 부착되어 있어.','expected':'owned aperture and connection'}, {'input_ko':'목 띠 중앙의 둥근 은색 원판.','expected':'not open ring'}, {'mutation':'put hoop on ear with choker unchanged','expected':'FAIL_OWNER'}])
card(8,'초커 또는 넥 아머의 대안과 사례 보석', [48,51], 'context_guard', ['wearable_accessory','garment_detail'], '선택된 목 장식 또는 보호판, 앞 중앙 장식',
 ['Only the chosen collar-band or neck-armor realization occupies the specified neck region.','A source-case central gem belongs to that chosen accessory and has a visible mounting.'],
 [('chosen accessory','surrounds','declared neck region'),('central gem','mounts_on','chosen accessory front')],
 'S03의 엘프 문양, 깊은 청/남청 보석, 허벅지 일부 보호판은 해당 원문 문맥값이다.',
 '일반 넥 아머에 엘프 문양·청색 보석을 필수화하지 않는다. 초커 OR 넥 아머 선택을 유지한다.',
 ['대안 두 물건을 무조건 동시 착용','넥 아머에 원문 없는 보호 성능을 부여','일부 허벅지 보호판을 전신 중갑으로 확대'],
 ['slot:wearable_accessory:royal_crest_choker'], ['R16','A06'],
 [{'input_ko':'문양이 없는 목 보호판 하나.','expected':'no source gem or elf pattern obligation'}, {'input_ko':'청색 보석 초커 또는 넥 아머 중 초커를 선택.','expected':'one chosen variant'}, {'mutation':'force both alternative neck pieces','expected':'FAIL_LOGICAL_OPERATOR'}],priority='P1')
card(9,'장식 사슬의 끝점·중력 곡선·부품별 반사', [49,50,53], 'extend_review', ['wearable_accessory','garment_detail'], '의복의 두 부착점과 그 사이 사슬, 버클',
 ['The selected chain has visible attachment endpoints on the declared garment hardware.','The loose span sags between its supports while the links remain distinct from the flexible strap.','Buckles connect their own strap ends and panels.'],
 [('chain endpoint A','attaches_to','garment anchor A'),('chain endpoint B','attaches_to','garment anchor B'),('loose chain span','hangs_between','two garment anchors')],
 'S03 허리·골반의 느슨한 장식 연결과 S02 버클은 소유자와 위치를 섞지 않는다.',
 '사슬의 모양은 길이·끝점 높이·자세에 따른다. 한 끝에 매단 펜던트는 별도 대안으로 다룬다.',
 ['사슬이 허공에 뜸','끝점 없이 늘어진 선만 그려 연결로 통과','느슨한 장식을 팽팽한 구속 사슬로 전환'],
 ['slot:wearable_accessory:y2kr_chain_strap','slot:wearable_accessory:unif_lapel_chain_separate_inner_neck'], ['A04','R17'],
 [{'input_ko':'재킷 두 부착점 사이에 느슨하게 처진 장식 사슬.','expected':'two anchored ends and loose span'}, {'input_ko':'목걸이 끝 하나에 달린 팬던트.','expected':'not mandatory two-anchor span'}, {'mutation':'move chain anchor to skin with no garment fitting','expected':'FAIL_CONNECTION'}],priority='P1')
card(10,'침구 눌림과 휴식 자세의 국소 대응', [54,55,56,57,65], 'new_relation_trial', ['body_pose','contact_point','texture'], '누운 인물의 머리·등/어깨, 베개·시트의 해당 접촉 패치',
 ['The resting body has the selected support contacts without floating or penetrating.','The soft bedding depression occurs directly under the declared contact patch.','The adjacent bedding remains relatively less compressed and traceable as the same surface.'],
 [('head or shoulder','rests_on','selected pillow patch'),('body contact patch','deforms','local bedding region'),('free hand','remains_near','declared head or neck position')],
 'S03의 베개·긴 은백색 머리 퍼짐은 사례 조건이다. 손을 목 근처에 둔 휴식을 목 압박으로 바꾸지 않는다.',
 '모든 supine 자세에 베개·긴 머리·침대나 접촉 주름을 추가하지 않는다. 우연히 시선이 만남·잠들기 전은 서사다.',
 ['빈 곳의 주름을 신체 접촉 흔적으로 통과','베개가 몸을 관통','누운 자세에 반드시 고개/시선 방향을 한 가지로 고정'],
 ['pv_profile_supine','pv_profile_side_lying'], ['A04','R17'],
 [{'input_ko':'머리를 베개에 기대고 머리 아래의 베개만 눌려 있어.','expected':'localized support deformation'}, {'input_ko':'바닥에 바로 누운 짧은 머리 인물.','expected':'no pillow or long-hair requirement'}, {'mutation':'depress pillow far from the head','expected':'FAIL_LOCATION'}])
card(11,'작은 입술 틈·치아 비노출·자연 비대칭', [69,70,71,72,196,197,198,207,208,211], 'new_relation_trial', ['expression','lip_finish','body_pose'], '같은 초상 인물의 입술·턱·눈꺼풀과 별도의 어깨/골반',
 ['The lips retain a small gap without a large jaw drop.','In the S07 case the teeth remain concealed while the requested quiet expression persists.','Source-specified small shoulder and pelvic asymmetries survive anatomy-defect exclusions.'],
 [('lip gap','belongs_to','subject mouth'),('teeth','remain_occluded_by','selected lip-jaw configuration'),('hands and shoulders','remain_connected_in','declared towel-holding posture')],
 '1–2 mm는 요청 수치로 보존하지만 픽셀 스케일 없는 사진으로 실측 PASS를 주장하지 않는다. S07 치아 비노출을 모든 parted lips의 뜻으로 일반화하지 않는다.',
 '편안한 눈꺼풀은 반쯤 감은 눈·졸음의 고정 형상이 아니다. 미세 비대칭의 방향/크기도 요청 범위다.',
 ['치아를 보여주는 큰 웃음으로 바꿈','small gap를 밀리미터 계측 성공으로 보고','broken wrist 제외를 강제 양손 대칭으로 처리'],
 ['ae_profile_lip_press','ae_profile_lip_tighten','contrapposto_weight_shift'], ['A07','R05'],
 [{'input_ko':'아주 작게 벌어진 입술, 치아는 보이지 않고 어깨는 살짝 비대칭.','expected':'preserve all independent face/pose constraints'}, {'input_ko':'활짝 웃으며 치아를 보여줘.','expected':'not S07 small-gap realization'}, {'mutation':'remove the small gap to satisfy no pout','expected':'FAIL_POSITIVE_RETENTION'}])
card(12,'머리 방향·안구 시선·거울 목표의 독립 축', [56,59,60,61,65,66,67,68,69,72,77,127], 'extend_review', ['gaze_target','gaze_engagement','body_orientation','expression'], '실제 머리, 두 눈의 시선 방향, 렌즈 또는 자신의 거울상 위치',
 ['The selected gaze target is retained independently of head orientation.','A reflected-face target corresponds to the same depicted actor rather than a second person.','A raised chin may coexist with eyes directed toward the declared interlocutor.'],
 [('eyes','look_toward','selected target'),('head orientation','belongs_to','same actor'),('mirror image','corresponds_to','depicted actor')],
 'S07은 렌즈, S06은 자기 거울상, S14는 상대 인물을 목표로 한다. 얼굴을 보는 POV의 목표도 유지한다.',
 '눈·머리 방향이 항상 일치해야 한다는 규칙을 만들지 않는다. 시선 머묾·움직임을 따라가지 않음은 정지 이미지로 시간 검증되지 않는다.',
 ['거울 안 두 번째 인물 생성','턱을 든다는 이유로 상대를 향한 안구 방향까지 위로 이동','직접 응시를 동의/욕망/적대로 동의어화'],
 ['slot:gaze_target:head_eye_counterorientation_relation','slot:gaze_engagement:pv_gaze_direct'], ['A07','A11','R04','R05'],
 [{'input_ko':'턱은 조금 위로 들고 눈은 맞은편 사람을 바라봐.','expected':'separate head and eye targets'}, {'input_ko':'거울에 반사된 자기 얼굴을 바라봐.','expected':'gaze to own reflection, not lens'}, {'mutation':'redirect eyes to camera while preserving mirror','expected':'FAIL_TARGET'}])
card(13,'시점 높이·거리·촬영 방향·초점의 네 가지 보존', [73,74,75,76,78,79,80,81,82,117,212], 'extend_review', ['camera_height','camera_direction','subject_framing','focus'], 'capture camera, 상대 얼굴, 접촉/가림의 필수 경계',
 ['Camera height is specified relative to the declared observer and subject.','The camera axis retains its named face target.','Viewing distance, projected proportions and the selected focus plane are recorded separately.'],
 [('camera optical axis','points_toward','declared face target'),('camera viewpoint','has_height_relative_to','observer or subject'),('focus plane','prioritizes','declared face and necessary relation')],
 'S15 바닥 가까운 눈 위치와 얼굴을 올려다봄은 비성적 시점이다. K079 얼굴 초점을 재질 강조를 이유로 옮기지 않는다.',
 '같은 framing은 크롭으로도 만들 수 있으므로 close-up만으로 실제 거리 실측을 주장하지 않는다. 렌즈 초점거리만으로 원근을 확정하지 않는다.',
 ['카메라 저각을 옷 안쪽 시선으로 바꿈','얼굴을 확대/재설계해 가까움처럼 처리','거울 초점과 거울 표면 초점을 같은 평면으로 자동 취급'],
 ['slot:camera_height:water_w191'], ['A07','R13'],
 [{'input_ko':'관찰자 눈을 바닥 가까이 두고 상대 얼굴을 향해 올려다봐.','expected':'height, target and observer binding'}, {'input_ko':'같은 위치에서 크롭만 더 좁혀줘.','expected':'no camera-distance obligation'}, {'mutation':'shift sharpest focus from face to necklace','expected':'FAIL_FOCUS_OWNER'}])
card(14,'반투명 방어막·공격 경로·충돌 영역의 깊이 순서', [104,105,106,107,108,109,110,111,112,113], 'new_relation_trial', ['surreal_physics_detail','relational_action','ambient_particle'], '시전자/지팡이, 방어막, 뒤의 인물, 충돌점·입자',
 ['The selected barrier lies between the incoming effect and the protected figure.','The figure remains partly readable behind the barrier surface.','The localized impact zone occurs where the incoming path meets that surface rather than on the figure.'],
 [('incoming effect','meets','barrier contact zone'),('barrier','lies_in_front_of','protected figure'),('impact particles','originate_near','declared contact zone'),('cloak attachment','remains_on','same actor shoulder')],
 'S10의 teen/young adult 혼용은 비성적 판타지 액션으로만 유지한다. white-gold 입자는 해당 충돌 효과의 색 조건이다.',
 '막의 문양·형태, 모든 입자의 초점 차이·속도는 고정하지 않는다. 원문 없는 신체 명중은 추가하지 않는다.',
 ['방어막을 인물 뒤 장식으로 이동','투명 원을 만들고 공격 경로는 몸에 명중','입자를 모두 같은 전경층에 겹쳐 관통'],
 ['slot:ambient_particle:egr_localized_suspended_particles'], ['A05','A06','A07','R04'],
 [{'input_ko':'들어오는 빛이 인물 앞 반투명 막 한곳에 부딪히고 뒤의 인물은 일부 보인다.','expected':'front barrier with localized encounter'}, {'input_ko':'인물 뒤의 장식용 빛 고리.','expected':'not blocking barrier'}, {'mutation':'move the impact onto the body','expected':'FAIL_TARGET_AND_STAGE'}])

card(15,'등 뒤 기계 장비의 연결과 원문 색 변형', [83,84,85,86,87,88,89,90,91,92,93,94,182,183,190,202], 'extend_review', ['prop','wearable_accessory','garment_detail'], '기계식 등 장비, 그 지지 프레임, 같은 인물의 외부 갑옷',
 ['The external back equipment is connected to a visible support on the same torso.','Equipment arms remain distinct from biological limbs.','The specified prop count, carried state and support connections are independently preserved.'],
 [('equipment arms','attach_to','back frame'),('back frame','mounts_on','same actor external armor'),('declared weapons','remain_in','selected held holstered or mounted state')],
 'S16 검정·흰색·은색 외장과 작은 주황 관절 발광은 해당 사례 변형에만 둔다. 붉은 코드/기계 발광과 색 소유자를 분리한다.',
 '장비 수와 방향, 색을 미래 무장의 보편 형상으로 고정하지 않는다. 등 연결이 읽히지 않으면 실제 연결 PASS를 주장하지 않는다.',
 ['장비 팔을 추가 신체 팔로 합침','본체와 떨어진 부유 장비로 대체','두 권총을 양손 사격 상태로 자동 강화'],
 ['slot:prop:real_holstered_service_pistol','slot:action:carrying_holstered_real_sidearm'], ['A04','A06','R16'],
 [{'input_ko':'등 프레임에 붙은 외부 장비 팔, 생물학적 팔은 두 개.','expected':'equipment attachment distinct from anatomy'}, {'input_ko':'권총 두 자루를 집에 넣은 인물.','expected':'count does not imply dual wielding'}, {'mutation':'force orange light on any futuristic equipment','expected':'FAIL_CASE_TO_GENERIC_LEAK'}],priority='P1')
card(16,'접촉을 만드는 신발과 별도의 지지 발', [80,81,82,114,115,117,118,119,120], 'new_relation_trial', ['contact_point','relational_action','body_pose'], '서 있는 인물 A의 접촉 신발, 낮은 위치의 상대 B 윗가슴 의복, A의 다른 발과 바닥',
 ['The declared shoe contacts the declared upper-chest clothing patch of the other actor.','That local soft cloth patch responds at the same contact location.','The other foot supports the standing actor on the floor independently of the contact shoe.'],
 [('actor A contact shoe','contacts','actor B upper-chest clothing patch'),('actor A other foot','rests_on','floor'),('actor A support leg','supports','actor A torso'),('observer eye viewpoint','belongs_to','actor B')],
 'S15는 비성적 강압 문맥으로만 보존한다. 접촉 도구가 신발이라는 뒤쪽 분해의 추가값은 원문 인증 전 사례 주장으로 기록한다.',
 '힘의 수치, 통증, 호흡 손상, 반복 타격, 노출을 추가하지 않는다. 장래 중립 검증은 별도 성인 가상 인물과 비성적 장면으로 설계한다.',
 ['손 접촉으로 신발 접촉을 대체','접촉 발에 모든 체중을 이전','바닥 지지 발을 상대 몸 위로 이동','낮은 카메라만 있고 실제 접촉은 없음'],
 ['slot:contact_point:pv_foot_wall'], ['A04','R17'],
 [{'input_ko':'A의 신발과 B의 윗가슴 옷이 맞닿고 A의 다른 발은 바닥에 있어.','expected':'effector, receiver and support remain distinct'}, {'input_ko':'A가 B 옆에 서 있고 신발은 바닥에만 닿아.','expected':'no bodily contact obligation'}, {'mutation':'make both feet contact B','expected':'FAIL_SUPPORT_OWNER'}])
card(17,'접촉·누름·제한·지속 압력의 증거 단계', [115,116,118,120,182,183], 'claim_guard', ['contact_point','relational_action'], '맞닿은 두 표면, 국소 변형, 동작 제한 관계, 별도의 시간 구간',
 ['Contact is recorded at the named surfaces rather than inferred from projected overlap.','A selected pressing depiction retains a local contact-response cue on the soft receiver.','Steady duration and force magnitude remain unmeasured from one still image.'],
 [('declared effector','contacts','declared receiver patch'),('local response','belongs_to','receiver surface'),('temporal claim','requires','specified multi-frame evidence')],
 'holds down의 강압 의미를 자발적 휴식으로 순화하지 않는다. 한 프레임에서는 제약을 읽히는 배치만 검토하며 실제 움직임 제한 실험을 했다고 주장하지 않는다.',
 '그림자가 어둡다고 큰 힘으로 판정하지 않는다. 정적 균형과 실제 동적 하중은 별도다.',
 ['화면상의 겹침을 실제 접촉으로 통과','단단한 접촉 그림자만으로 힘/시간을 정량화','정지 이미지로 반복 유지·호흡 영향까지 PASS'],
 ['slot:contact_point:no_contact_just_close'], ['A04','A11','R17'],
 [{'input_ko':'한 장의 그림에서 접촉 위치와 옷 눌림은 보이지만 힘은 계측하지 않았어.','expected':'geometry scored; magnitude and duration unscored'}, {'input_ko':'여러 프레임에서 접촉 위치가 유지됨.','expected':'temporal evidence still does not measure force'}, {'mutation':'infer steady pressure solely from dark shadow','expected':'FAIL_UNSUPPORTED_CLAIM'}])
card(18,'질책 손과 얼굴 사이의 가시적인 간격', [121,122,123,124,125,126,127,128,129,130,131,132], 'new_relation_trial', ['proxemics','contact_point','relational_action'], '발화자 손, 상대 얼굴, 두 인물의 문턱 위치',
 ['The raised or extended hand and the other actor face remain separated by a readable gap.','Both endpoints and the intervening space are framed together.','The dialogue or rebuff context remains separate from physical striking.'],
 [('speaker hand','remains_separated_from','other actor face'),('visible interval','lies_between','same hand and same face'),('actors','occupy_sides_of','declared threshold')],
 'S14의 비성적 언쟁, 치켜든 턱, 상한 자존심은 신체 부상·폭행으로 바꾸지 않는다. 문턱은 source-case 공간값이다.',
 '손을 가리거나 화면 밖으로 보내 비접촉을 통과시키지 않는다. 원근상 겹쳐 경계가 확인되지 않으면 미관찰이다.',
 ['손이 얼굴을 누르는 접촉으로 변경','두 끝점 중 하나를 가려 무접촉으로 통과','wounded disbelief를 멍/출혈로 해석'],
 ['slot:contact_point:no_contact_just_close'], ['A07','R04','R05'],
 [{'input_ko':'내민 손과 상대 얼굴 사이로 배경이 보이고 두 경계가 모두 보여.','expected':'visible separation'}, {'input_ko':'손은 얼굴을 실제로 누르고 있어.','expected':'not noncontact rebuke'}, {'mutation':'crop the raised hand outside the image','expected':'UNOBSERVABLE_NOT_PASS'}])
card(19,'내려든 검·장갑 벗기·발도의 현재 상태', [87,95,96,97,98,99,100,101,102,103,133,137,138,139], 'extend_review', ['action','hand_pose','prop'], '검/장갑/칼집/손의 독립 연결과 현재 배치',
 ['A lowered sword points toward the floor with its holding arm down beside the actor.','A glove-removal state retains the pulling hand, the glove edge and the other wrist.','A partially drawn prop remains aligned with its storage opening without being converted to a discharged or striking state.'],
 [('holding hand','grips','declared prop'),('glove-removal hand','grasps','other glove edge'),('partly drawn blade','continues_into','same sheath opening')],
 'S09 전투 후 정리 동작과 S19 발도 도중은 서로 다른 사례다. 느리게·막 끝난이라는 시간 수식은 별도 서사로 유지한다.',
 '세 상태를 한 인물/한 손에 무조건 동시 합치지 않는다. 재장전의 기술 절차나 실제 무기 성능은 연구 범위가 아니다.',
 ['내려든 검을 상대 조준 상태로 변경','장갑 벗김을 상대 손목 잡기로 대체','발도 순간을 찌르기/발사 결과로 확대'],
 ['slot:action:carrying_holstered_real_sidearm'], ['A04','A11'],
 [{'input_ko':'검 끝은 아래로, 다른 손은 자기 장갑 입구를 잡아 벗기는 중.','expected':'two owned current states'}, {'input_ko':'칼집에 완전히 들어간 검.','expected':'not partly drawn'}, {'mutation':'change lowered sword to threat-facing sword','expected':'FAIL_ACTION_STAGE'}],priority='P1')
card(20,'유리 파편과 불투명 잔해의 재질 대비', [112,134,135,136,140,141,142,143,144], 'new_relation_trial', ['aftermath_trace','surface_material','ambient_particle'], '지정된 유리 파편과 별도의 불투명 잔해, 그 근처 파손 물체',
 ['The broken glass retains angular transparent or reflective fragment surfaces.','The selected opaque rubble remains a different material with traceable broken faces.','Damage belongs to the declared environment object rather than the character body.'],
 [('glass fragments','belong_to','declared broken glass object'),('opaque rubble','belongs_to','declared damaged structure'),('fragment reflection','receives','local light')],
 '원문의 일부 파손·아주 옅은 먼지와 S16의 도시 폐허/검은 연기는 규모와 소유자를 분리한다.',
 '모든 유리 모서리의 반짝임이나 모든 돌의 무광을 의무화하지 않는다. 빛·거칠기·오염 상태에 따라 가시 단서를 정한다.',
 ['회색 불투명 자갈을 유리 파편으로 통과','환경 잔해를 인체에 박힌 파편으로 전환','약한 먼지를 짙은 연막/대형 화재로 확대'],
 ['rb_glass_reflection_transmission'], ['A06','R11','R12'],
 [{'input_ko':'바닥의 유리 조각과 옆의 거친 돌 잔해를 다른 표면으로 보여줘.','expected':'owned material contrast'}, {'input_ko':'닦이지 않은 어두운 유리라 뚜렷한 반짝임은 없어.','expected':'no universal edge-glint duty'}, {'mutation':'put all fragments in skin','expected':'FAIL_DAMAGE_OWNER'}],priority='P1')
card(21,'유리에 눌린 접촉을 가까움·반사와 구별', [169,173,183], 'new_relation_trial', ['contact_point','surface_material','body_pose'], '지정된 신체/의복 부분, 유리면, 실제 접촉 패치',
 ['The declared contacting part meets the glass plane rather than stopping across a visible gap.','A pressed depiction has a bounded local contact-response cue, consistent with the stated material.','Reflected overlap is recorded as an optical image and does not substitute for contact geometry.'],
 [('declared body or cloth patch','contacts','glass plane'),('local flattening or cloth compression','belongs_to','contacting soft patch'),('reflection','is_optical_image_of','nearby scene')],
 'K169 분해의 바로 가까이에 놓임 OR 반사 겹침만으로 pressed를 통과시키지 않는다. 원래의 접촉 의도는 보존한다.',
 '원문에 없는 강한 변형, 밀어붙인 행위자, 부상은 추가하지 않는다. 지정된 접촉 부위는 frozen core로 해결한다.',
 ['유리와 떨어져 있는 근접 초상으로 대체','반사 얼굴을 실제 유리 접촉 얼굴로 통과','모든 접촉을 심한 얼굴 변형으로 과장'],
 ['rb_glass_reflection_transmission'], ['A04','A06','A07','R11'],
 [{'input_ko':'손바닥이 유리에 맞닿아 국소 접촉 패치가 보인다.','expected':'contact-plane geometry'}, {'input_ko':'손은 유리에서 떨어져 있고 반사만 겹친다.','expected':'not pressed contact'}, {'mutation':'leave a visible gap and claim pressed','expected':'FAIL_CONTACT'}])
card(22,'수중·닫힌 용기·막힌 경로와 갇힘 서사', [166,167,168,170,171,172,174], 'context_guard', ['space_condition','location','relational_action'], '용기 경계, 내부 인물과 물, 요청된 이동 경로의 장벽',
 ['The underwater setting has declared water and container cues on their own carriers.','The chamber boundaries remain continuous where shown.','If confinement is requested, a declared attempted path meets its blocking boundary rather than relying only on absent exits in a crop.'],
 [('container boundaries','enclose','selected interior'),('water cues','belong_to','selected interior medium'),('declared attempted path','meets','blocking boundary')],
 '갇힘/불안 설정은 서사로 남긴다. 열린 출구가 프레임에 없다는 사실로 실제 탈출 불가·질식·사망을 인증하지 않는다.',
 '일반 수중 초상에는 막힌 경로·공포·구조를 발명하지 않는다. 경로는 요청이 갇힘을 요구하고 명확한 관계가 있을 때만 검증 대상으로 둔다.',
 ['크롭에서 출구 부재를 물리적 감금 증거로 통과','닫힌 챔버를 우주 유해환경 habitat으로 자동 전환','물방울만으로 인물이 수중에 있다고 확정'],
 ['slot:location:hr_sealed_habitat_external_limit'], ['A05','A07','R18'],
 [{'input_ko':'수중 전시 용기 안의 평온한 초상.','expected':'no unrequested confinement'}, {'input_ko':'인물이 닫힌 창 쪽으로 손을 내미나 경계가 그 경로를 막는다.','expected':'authored blocked-path depiction; no real diagnosis'}, {'mutation':'claim inescapable solely because no exit is in crop','expected':'FAIL_UNSUPPORTED_CLAIM'}])
card(23,'붉은 얼룩·빛 기호·기계 발광·반사 수신면', [19,40,146,149,154,155,173,185,188,201,214,215], 'new_relation_trial', ['light_type','ambient_particle','surface_material','color'], '공중 코드 기호, 기계 틈의 광원, 근처 금속 수신면, 표면 얼룩',
 ['Airborne red symbols remain separated luminous shapes rather than surface smears.','The subtle machine light originates inside its declared seam or aperture.','Any red reflection belongs to the adjacent receiver surface and follows the selected light geometry.'],
 [('code symbols','occupy','declared air volume'),('machine seam light','emits_from','machine aperture'),('emitted light','is_received_on','adjacent metal edge'),('stain','adheres_to','separate specified surface')],
 'S16 no blood 아래에도 붉은 코드·진홍 기계 발광은 남긴다. S18 dark red stains는 혈액인지 원문 문맥 없이 판정하지 않는다.',
 '코드 문자의 정확한 텍스트가 없으면 읽히는 임의 주문/문장을 추가하지 않는다. 빨강 하나로 광원 또는 혈액을 진단하지 않는다.',
 ['no blood 때문에 붉은 광원까지 삭제','코드 입자를 피부의 혈흔으로 대체','기계 틈이 아니라 인물 피부를 자체 발광체로 만듦','반사 색을 재질의 본래 색으로 확정'],
 ['slot:light_type:status_led_glow','slot:ambient_particle:egr_localized_suspended_particles'], ['A06','R11','R12'],
 [{'input_ko':'기계 틈의 붉은 빛이 가까운 금속에만 비치며 혈흔은 없어.','expected':'emitter-receiver relation with scoped exclusion'}, {'input_ko':'칼날에 어두운 붉은 비발광 얼룩.','expected':'surface mark, not emitted light'}, {'mutation':'delete red code to satisfy no blood','expected':'FAIL_POSITIVE_RETENTION'}])
card(24,'양손 타월 윗단 장력·중앙 가림·수영복 가시 창', [69,71,196,197,198,207,208,209,210,211], 'new_relation_trial', ['hand_pose','garment_detail','prop'], '동일 타월의 양쪽 손잡힘, 가로 윗단, 중앙/아랫단, 뒤의 수영복',
 ['Each hand grips a declared point on the same towel upper edge.','The upper edge is tensioned between the hands while the central and lower towel area hangs in front of the torso and pelvis.','The selected towel coverage remains continuous across the specified front region.','Only the source-specified small shoulder-strap window of the swimsuit remains visible.'],
 [('left hand','grips','same towel upper-edge point A'),('right hand','grips','same towel upper-edge point B'),('towel front panel','occludes','declared torso and pelvis front'),('visible shoulder strap','belongs_to','swimsuit behind towel')],
 'S07 윗가슴 아래부터 허벅지 위쪽까지의 전면 가림, 대부분 가려진 산호색 수영복과 좁은 어깨끈은 사례 조건이다. 양손·자연스러운 높이 차이도 유지한다.',
 '타월이 몸을 감싸는 변형과 양손으로 앞에 드는 변형은 별도다. 원문에 없는 배면 전체 가림·젖음·타월 크기 수치를 강제하지 않는다.',
 ['양팔 벌림 때문에 타월 중앙을 열어 전면을 노출','타월을 두 개로 나눔','수영복 대신 맨 피부를 가시 창으로 통과','몸에 두른 타월로 양손 지지 관계를 대체'],
 ['water_rel_w159','slot:garment_detail:water_w159'], ['A04','A06','A07'],
 [{'input_ko':'양손으로 타월 윗단을 잡되 중앙 천이 앞 몸통과 골반을 계속 가려.','expected':'two grips and continuous front occlusion'}, {'input_ko':'몸에 두른 수건, 손은 내려놓음.','expected':'not two-hand held-front state'}, {'mutation':'show swimsuit body through a towel center gap','expected':'FAIL_COVERAGE'}])
card(25,'형태 오류 배제 아래 남아야 할 미세 비대칭', [3,55,69,72,119,120,182,198,207,208,212,216], 'claim_guard', ['body_pose','hand_pose','body_orientation'], '주체의 관절 연결, 각 손과 타월, 좌우 지지/어깨 높이',
 ['Wrists and shoulders retain anatomically coherent connections for the selected action.','The request-specific small asymmetries are preserved rather than repaired into forced symmetry.','Support leg and body alignment remain separate from style or attitude labels.'],
 [('hand','connects_through','same-arm wrist and elbow'),('upper arm','connects_to','same actor shoulder'),('selected asymmetry','belongs_to','declared pose or face property')],
 'K207/208은 생성된 형태 결함 제외이며 부상 설정이 아니다. S07의 미세 골반 이동·어깨 높이 차이와 S08의 참조 얼굴 자연 비대칭을 보존한다.',
 '일반 균형을 contrapposto로 통일하지 않는다. 신체/표정 참조의 각도와 투영은 따로 검토한다.',
 ['자연 비대칭을 탈구로 오인','좋은 해부학을 이유로 요청된 한쪽 지지를 양쪽 동등 지지로 변경','비대칭 명칭만으로 관절 연결 결함을 허용'],
 ['contrapposto_weight_shift','slot:gaze_target:head_eye_counterorientation_relation'], ['A07','R17'],
 [{'input_ko':'오른손을 조금 더 높게 들어 어깨 높이도 자연스럽게 달라.','expected':'coherent asymmetry'}, {'input_ko':'양손이 같은 높이인 대칭 동작.','expected':'no compulsory asymmetry'}, {'mutation':'force symmetric shoulders while unequal hand heights remain','expected':'FAIL_SOURCE_POSE_RETENTION'}])
card(26,'감정·역할 분해를 선택 가능한 연기 예시로 유지', [1,2,3,4,62,64,65,66,67,68,72,83,90,100,101,103,106,121,123,124,125,128,129,130,139,145,156,157,159,161,162,163,166,167,168,174,177,179,204,211], 'authoring_guidance', ['expression','intent_state','situation_context'], '요청된 정서/역할, 독립 외형 단서와 그 장면 맥락',
 ['The requested affect or role remains an authored semantic layer.','One compatible acting realization may support it without becoming its unique exact geometry.','Alternative meanings and nonsexual distress contexts remain distinct.'],
 [('selected acting cue','supports','authored scene meaning'),('context','qualifies','cue interpretation'),('alternative affect option','remains_distinct_from','other option')],
 '32개 해석 예시를 예시로 유지한다. 관능/몽환/경멸/불안과 눈꺼풀/입꼬리의 한 형태를 동의어로 만들지 않는다.',
 '같은 의미의 다른 연기가 허용된다. 필요한 경우 원래 사건·반응·결과를 readable prose로 보존하며 예시의 기계적 강제는 피한다.',
 ['pensive를 느린 눈 움직임 실측으로 통과','직접 시선을 자신감·동의의 충분조건으로 사용','고통/소진을 쾌락이나 자발적 복종으로 재해석'],
 [], ['R05','A11'],
 [{'input_ko':'차분하지만 상대에게 시선을 돌리지 않는 인물.','expected':'another compatible calm realization'}, {'input_ko':'입술이 조금 열렸다는 것만 확인.','expected':'no inferred emotion or consent'}, {'mutation':'make source acting example a universal exact alias','expected':'FAIL_AUTHORITY'}],priority='P1')
card(27,'참조 외형 비례·투영 변화·성인 대상 조건', [3,212,216,217], 'claim_guard', ['subject','subject_framing','body_orientation'], '요청된 주체 수/성인 설정, 참조의 보이는 얼굴·머리, 촬영 방향',
 ['The depicted subject count remains the declared count.','Adult status remains an explicit subject setting independent of facial appearance inference.','Visible reference proportions are reviewed under compatible head orientation and perspective before claiming a redesign.'],
 [('reference proportions','guide','requested visible face appearance'),('head orientation','changes_projection_of','same face'),('adult setting','belongs_to','declared subject')],
 'FACE=LOCKED의 요청된 외형 유지와 ONE ADULT WOMAN의 한 명·성인 설정을 각각 보존한다. 실제 신원/법적 나이는 사진에서 인증하지 않는다.',
 '표정·빛·고개 회전에 의한 apparent ratio 차이를 실제 골격 변경으로 단정하지 않는다. 근거 없는 비율 수치/생체 측정은 추가하지 않는다.',
 ['카메라 원근을 얼굴폭 확대 재설계로 보정','청순함을 아동 외형으로 변경','성인 외형처럼 보임을 실제 성인 확인으로 주장'],
 [], ['A07','R05'],
 [{'input_ko':'성인 한 명의 참조 얼굴 외형을 유지하되 고개를 약간 돌려줘.','expected':'appearance guidance with projection caveat'}, {'input_ko':'사진에서 어려 보이는 얼굴.','expected':'no age verification'}, {'mutation':'add a second reflected person to a one-person portrait','expected':'FAIL_SUBJECT_COUNT'}],priority='P1')
card(28,'부정 조건의 소유 범위와 긍정 형상 보존', list(range(189,209))+[7,27,31,42,48,66,157,163,209,210,213,214,215], 'negative_firewall_plan', ['garment_detail','expression','prop','ambient_particle'], '원래 부정 지시의 대상과 동시에 보존해야 할 의상·표정·장비·색',
 ['Each exclusion retains its source owner, context and polarity.','Allowed garment fit, slit, weapon, colored light and quiet expression remain intact under their relevant exclusions.','OR alternatives remain alternatives, and source-specific coverage does not become a universal rule.'],
 [('source exclusion','constrains','its declared target property'),('retained positive component','coexists_with','scoped exclusion'),('alternative options','remain_in','authored OR relation')],
 '20개 원래 부정 지시를 positive retrieval로 뒤집지 않는다. no gore/no blood 아래 전투 장비·붉은 빛은 남기고, 노골적 표현 금지 아래 원래 핏/슬릿은 남긴다.',
 '타월·갑옷·상처 배제·소재 불투명을 다른 원자료에 전파하지 않는다. 제외조건을 더 안전한 새로운 장면으로 바꾸는 대신 원래 허용된 형상을 보존한다.',
 ['nudity/lingerie 같은 부정 토큰을 새 후보 검색 요청으로 사용','no blood로 모든 빨강을 제거','관능성 배제로 모든 표정을 삭제','원문의 OR를 all-of로 강제'],
 ['pfe_slit','pfe_opaque_fit','slot:light_type:status_led_glow'], ['A06','A10','R02'],
 [{'input_ko':'원래 허벅지 시작 슬릿과 몸에 맞는 긴 드레스는 남기고 추가 노출은 없어.','expected':'positive slit and scoped exclusion coexist'}, {'input_ko':'붉은 기계 발광은 유지하고 혈흔은 제외.','expected':'color source retained'}, {'mutation':'route negative lingerie token into wardrobe selection','expected':'FAIL_NEGATION_FIREWALL'}])

sources=[]
def ref(id,title,url,access,fact,limit,location):
 sources.append({'id':id,'title':title,'url':url,'checked_at':'2026-10-07','origin':'additional_web_research','access_scope':access,'supports_ko':fact,'claim_limit_ko':limit,'reviewed_location':location})
ref('A01','Programming Mechanics in Knitted Materials, Stitch by Stitch (v2)','https://arxiv.org/abs/2302.13467v2','author abstract and version metadata','편직의 탄성 반응은 실 재료뿐 아니라 국소 스티치 위상과 패턴에 영향을 받는다.','모든 골지의 간격 변화·신장률을 동일하게 예측하거나 가시 소재를 화학적으로 식별한 근거가 아니다.','abstract; v2 dated 2023-12-04')
ref('A02','Stitch Meshes for Modeling Knitted Clothing with Yarn-level Detail','https://www.cs.cornell.edu/projects/stitchmeshes/','author university project page','큰 의복 표면·스티치 배열·실 곡선은 서로 다른 규모의 구조이며 시뮬레이션은 실 관통을 피하도록 다룬다.','탑의 색·목선·골 방향은 이 연구가 정해 주지 않는다.','project abstract and modeling stages, 2012')
ref('A03','Modeling and Rendering Fabrics at Micron-Resolution','https://www.cs.cornell.edu/projects/ctcloth/','author university project abstracts','직물 외관에는 섬유/실의 구조와 빛 상호작용이 관여하며 표면 반사 하나만으로 두꺼운 직물의 모든 외관을 설명하지 않는다.','각 연결 PDF를 전부 읽은 것은 아니다. 재료 라벨 하나에 모든 드레이프·투과를 강제하지 않는다.','2011, 2012, 2015 and 2016 project abstracts')
ref('A04','Robust Treatment of Collisions, Contact and Friction for Cloth Animation','https://www.cs.ubc.ca/~rbridson/docs/cloth2002.pdf','author-hosted accepted paper PDF, 10 pages; relevant text reviewed','천의 두께·자기 접촉·마찰·관통 방지는 서로 구별되는 기하/시뮬레이션 문제다.','천 시뮬레이션 논문은 사진에서 사람의 체중·압력·접촉 지속을 측정하는 도구가 아니다.','PDF pages 1-2, introduction and cloth model')
ref('A05','PBRT 4e: Scattering from Layered Materials','https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials','official book chapter text','층·두께·흡수/산란과 이동 경로에 따라 반사와 투과가 달라진다.','책의 단순 층 모델을 실제 젖은 의복의 보편 수치나 인체 가시성 보장으로 전용하지 않는다.','section 14.3; Figure 14.17 caption and transmittance text')
ref('A06','Khronos glTF PBR Properties Glossary','https://www.khronos.org/gltf/pbr','official standards organization documentation','표면 요철, base color, roughness, alpha coverage, transmission, emission은 별도 속성이다.','그래픽 표현 구별이며 실제 화학 재료/공학 기능 또는 키워드 생성 효과의 인증이 아니다.','Alpha Coverage, Normal, Roughness, Transmission, Emissive sections')
ref('A07','PBRT 4e: Projective Camera Models','https://www.pbr-book.org/4ed/Cameras_and_Film/Projective_Camera_Models','official book chapter text','시점·투영·심도 모델은 별도이며 물체의 투영 크기와 초점면 앞뒤의 디포커스를 구별해야 한다.','사진에서 실제 초점거리·거리·밀리미터 치수를 역으로 인증하는 근거는 아니다.','section 5.2, perspective model and depth-of-field text')
ref('A08','The Colour of Textiles when Wet (Smith, 1979)','https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1478-4408.1979.tb03477.x','publisher indexed abstract and bibliographic record; direct article unavailable','젖은 섬유의 색/반사와 마른 상태 관계를 다룬 연구가 있다.','초록 범위다. 모든 직물이 젖으면 반드시 어두워지거나 가시광으로 투명해진다는 주장을 뒷받침하지 않는다.','publisher indexed abstract, Journal of the Society of Dyers and Colourists 95:220-225')
ref('A09','Plasmonic nanocomposite helices for weather-adaptive LiDAR function','https://www.nature.com/articles/s41467-026-75037-1','publisher indexed abstract and visible/NIR condensation-test excerpt; later cookie redirect blocked','유리 위 응축 방울은 산란으로 표면 뒤 영상의 가시성을 낮출 수 있다. 가시광과 NIR 결과를 구분해야 한다.','숫자나 성능을 인용하지 않는다. 모든 물막이 희거나 불투명하다는 뜻도 아니며 거울 초상 전체를 검증한 논문도 아니다.','abstract and Clearance of multiscale water droplets indexed excerpt')
ref('A10','T2I-CompBench (2023 original v1)','https://arxiv.org/abs/2307.06350v1','author abstract and version metadata','색·형태·질감의 대상 결합과 공간/비공간 관계, 복합 장면은 분리된 평가 축이다.','최신 v3 제목은 T2I-CompBench++이다. 여기서는 원래 v1만 인용하며 이 프로젝트의 성공률을 외삽하지 않는다.','v1 abstract; submitted 2023-07-12')
ref('A11','Following Gaze in Video (ICCV 2017)','https://openaccess.thecvf.com/content_iccv_2017/html/Recasens_Following_Gaze_in_ICCV_2017_paper.html','official CVF indexed abstract; direct page returned 403','영상의 시선 목표는 프레임 간 관계를 포함하며 시선 자세와 뷰 사이 기하를 따로 다룬다.','초록 범위다. 표정으로 실제 마음을 판정하거나 정확한 시선 계측을 했다는 근거는 아니다.','official indexed abstract; ICCV 2017 pp.1435-1443')
oldsrc=json.loads((BASE/'SOURCES.json').read_text())
oldsource_list=oldsrc.get('primary_sources',[]) if isinstance(oldsrc,dict) else oldsrc
used_old={s for c in cards for s in c['research_source_ids'] if s.startswith('R')}
for s in oldsource_list:
 if s['id'] in used_old:
  sources.append({**s,'origin':'inherited_initial_research','provenance_file':'../SOURCES.json','followup_live_reverification':False})
save('SOURCES.json',{'schema_version':'vel-appearance-sources/v1','sources':sources,'new_source_count':11,'inheritance_note':'Rxx carry the initial study review and its limitations; Axx are the additional primary-source research.'})
save('RESEARCH-CARDS.json',{'schema_version':'vel-appearance-cards/v1','status':'RESEARCH_ONLY','not_current_runtime_schema':True,'cards':cards})
fidelity={
 'K003':'메이크업 색이 반드시 실제 얼굴 그림자를 줄인다고 단정하지 않는다. 색·음영·빛은 별도 속성이다.',
 'K004':'오래 머무는 시선은 정지 이미지로 지속 시간 확인이 불가하다. 선택된 정서 예시는 보편 형상이 아니다.',
 'K005':'관절 주변에만 주름이 있다는 배타 조건은 기본 핏의 보편 뜻이 아니다. 재단·자세·소재별 변형으로 둔다.',
 'K008':'핀스트라이프와 안쪽 의복 층은 S02 사례값이다. 일반 fitted jacket에 자동 주입하지 않는다.',
 'K009':'골 간격 변화는 특정 편직/장력의 조건부 실현이다. 평면 줄무늬와 구별하되 모든 골지의 동일 변형을 강제하지 않는다.',
 'K010':'닫힌 허리 앞판과 탑/넥타이가 보이는 상흉부 중앙을 서로 다른 영역으로 기록한다.',
 'K017':'leather-like에 뚜렷한 결·두꺼운 가장자리를 모두 필수화하지 않는다. 코팅/평활 가죽 외관도 있다.',
 'K020':'모든 주름 능선이 항상 밝고 골이 항상 어두운 것은 아니다. 광원·뷰·표면 법선에 조건화한다.',
 'K022':'옛 금속 표현을 심한 녹이나 부서짐, 실제 금속 화학 판정으로 확대하지 않는다.',
 'K025':'꽃·망상 도안과 scallop은 선택된 레이스 변형이다. 구멍 아래 바탕층의 별도 가림을 보존한다.',
 'K035':'젖음에 따른 어두워짐·무거운 드레이프·겹쳐 덜 비침은 조건부 실현이며 젖음에서 자동 투명도를 추론하지 않는다.',
 'K037':'겹쳐 덜 비치는 정도는 실제 소재/빛 경로에 의존한다. 약한 가시 투과라는 원래 정도는 유지한다.',
 'K040':'하이라이트는 광원 방향만 아니라 관찰 방향과 국소 표면에도 의존한다. 피부 전체를 같은 반사로 만들지 않는다.',
 'K042':'wet OR clingy라는 선택 구조와 shiny의 수식 범위를 원문 그대로 해석한다. 논리 범위가 미확정이면 전부 필수로 만들지 않는다.',
 'K043':'결로를 무조건 흰 연속 물막으로 모델링하지 않는다. 표면 방울/산란 흐림과 카메라 디포커스를 분리한다.',
 'K048':'초커 OR 넥 아머를 둘 다 필수로 만들지 않는다. 보석 색과 엘프 문양은 S03 사례값이다.',
 'K062':'붉은 쿠션·제단·촛불·아래 시선은 S04의 선택된 기도 장면이다. 일반 kneeling의 필수 요소가 아니다.',
 'K069':'머리 방향과 안구 목표는 독립 축이다. 자연스러운 시선을 이유로 모든 직접 응시의 머리를 정면으로 고정하지 않는다.',
 'K071':'1–2 mm와 치아 비노출은 S07 요청값으로 유지한다. 스케일 없는 이미지에서 mm 실측을 PASS로 기록하지 않는다.',
 'K077':'거울상/실체/테두리의 공동 프레임은 선택된 구성이다. 모든 거울 초상에 실체 노출을 강제하지 않는다.',
 'K079':'반사된 얼굴의 가상 초점 거리와 거울 전면 거리는 별도다. 전경 반사상 전부가 항상 흐려진다는 규칙을 만들지 않는다.',
 'K110':'입자마다 물리 크기가 달라질 수 있다. 크기 차이를 깊이의 계측 증거로 단정하지 않는다.',
 'K114':'신발이라는 접촉 도구는 뒤쪽 분해의 문맥 주장으로 기록하고, 원래 S15 텍스트 인증 전 새 원문 확인이라고 부르지 않는다.',
 'K116':'한 장의 접촉 배치는 시간적 유지·실제 힘 크기의 증거가 아니다.',
 'K118':'접촉 그림자 하나만으로 접촉이나 큰 압력을 확정하지 않는다. 표면 위치와 경계가 함께 읽혀야 한다.',
 'K120':'몸통이 지지 다리 가까이 있음은 지지 배치 단서다. 체중 비율을 실측한 근거가 아니다.',
 'K126':'물러서지 않음은 서사/시간 조건이다. 한 장에서 이전 이동이나 정지 이력을 인증하지 않는다.',
 'K138':'장갑 벗기 중간 상태는 보일 수 있으나 천천히라는 속도는 한 프레임으로 인증하지 않는다.',
 'K149':'혈흔의 섬유 번짐/매끈한 표면 경계는 선택된 표면의 조건부 외형이다. 혈액 화학 정체나 시점을 사진으로 인증하지 않는다.',
 'K164':'일반 kneeling은 양쪽 무릎·한쪽 무릎 등 선택 변형이 있다. 양쪽 무릎을 보편 exact 의미로 만들지 않는다.',
 'K165':'정확한 글자 敗北은 보존하되 세로 배열·큰 크기·밝은 글자색은 원자료 문맥 확인 전 보편 뜻으로 만들지 않는다.',
 'K169':'가까움 OR 반사 겹침만으로 pressed contact를 대체할 수 없다. 실제 소유된 접촉 패치를 요구한다.',
 'K170':'프레임 안 출구 부재만으로 탈출 불가를 인증하지 않는다. 갇힘 의도는 별도 서사/경로 차단 관계로 보존한다.',
 'K174':'quiet·suspended의 실제 소리/지속/정지 상태는 한 장에서 계측되지 않는다.',
 'K186':'노란 테이프에 반드시 반복된 검정 경고 문자가 있다는 뜻은 아니다. 실제 문자 조건은 사례 확인 뒤 분리한다.',
 'K198':'no exaggerated thrust가 모든 대칭을 뜻하지 않는다. 원문의 미세한 골반 이동과 어깨 비대칭을 보존한다.',
 'K207':'손목 형태 오류 제외를 실제 손목 부상 설정으로 해석하지 않는다.',
 'K208':'어깨 형태 오류 제외를 강제 좌우 대칭으로 해석하지 않는다.',
 'K209':'전면 가림 범위와 양손 잡힘은 S07 문맥값이다. 일반 towel/wrap에 전체 몸 가림을 전파하지 않는다.',
 'K210':'거의 가려진 수영복의 존재와 작은 끈의 가시 창을 동시에 유지한다.',
 'K212':'동일 관점/투영 조건으로 참조 외형 비례를 검토한다. 고개 회전/거리 효과를 실제 얼굴 재설계로 단정하지 않는다.',
 'K213':'기념물·머리띠 대안과 실제 원문 위치를 확인한다. bandage를 자동 치료/새 부상으로 바꾸지 않는다.',
 'K214':'공중 발광 기호와 표면 혈흔은 소유자·광원·부착 상태가 다르다.',
 'K215':'기계 틈 광원과 금속 수신면, 바탕 재질 색을 분리한다.',
 'K216':'요청된 보이는 얼굴/머리 외형 유지를 실제 신원 인증과 혼동하지 않는다.',
 'K217':'한 명·성인 설정은 별도 대상 조건이며 사진 외형으로 법적 나이를 인증하지 않는다.'
}
save('FIDELITY-CORRECTIONS.json',{'status':'research_review_notes_not_source_rewrites','corrections':[{'keyword_id':k,'review_ko':v,'prior_card_ids':oldunits[k]['proposal_ids']} for k,v in fidelity.items()]})

units=[]
for e,o in zip(source['entries'],original['entries']):
 linked=[c['id'] for c in cards if e['id'] in c['keyword_ids']]
 basis=e['decomposition_basis']
 policy={'직접 분해':'physical paraphrase proposal; detail is not necessarily verbatim or independently seen','문맥 결합':'source-case composition; never universalize colors, props, role, layering or coverage','해석 예시':'optional acting realization; no unique emotion-to-face geometry','제외 조건':'source-scoped negative; retain compatible positive structure','대상 조건':'explicit subject setting; not visually authenticated'}[basis]
 units.append({**e,'prior_semantic_unit_id':oldunits[e['id']]['semantic_unit_id'],'prior_card_ids':oldunits[e['id']]['proposal_ids'],'followup_card_ids':linked,'review_status':'reviewed_with_additional_relation' if linked else 'reviewed_carry_prior_plan','adoption_policy':policy,'source_is_not_independent_observation':True,'original_metadata_preserved':{'role':o['role'],'evidence':o['evidence']},'review_note_ko':fidelity.get(e['id'],'분해의 원래 출처·극성·연령·범위를 유지한다. 구체화의 각 세부는 runtime 채택 전에 invariant·사례값·선택 예시로 나눈다.'),'visual_atoms':[{'id':f"VD-A-{e['id']}-{n:02}",**atom,'source_basis':basis,'runtime_ready':False,'owner_binding_status':'use referenced followup card or prior VEL card; atom is not independently compiled','is_hard_obligation':False} for n,atom in enumerate(e['visual_elements'],1)],'runtime_ready':False})
save('SEMANTIC-UNITS.json',{'schema_version':'vel-appearance-units/v1','status':'RESEARCH_ONLY','units':units})
with (OUT/'KEYWORD-CROSSWALK.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['id','category','original_phrase','polarity','source_id','basis','old_cards','followup_cards','review_note'])
 for u in units:w.writerow([u['id'],u['category'],u['original_phrase'],u['original_polarity'],u['source_id'],u['decomposition_basis'],';'.join(u['prior_card_ids']),';'.join(u['followup_card_ids']),u['review_note_ko']])
md=['# 전체 217개 추가 분해 대조표','','원본 ID·출처·극성·연령 문맥을 유지한다. VD는 추가 검토 카드이며 후보 채택을 뜻하지 않는다.','','| ID | 표현 | 분해 근거 | 기존 카드 | 추가 카드 | 검토 상태 |','|---|---|---|---|---|---|']
for u in units:md.append('| '+' | '.join([u['id'],u['original_phrase'].replace('|','/'),u['decomposition_basis'],', '.join(u['prior_card_ids']),', '.join(u['followup_card_ids']) or '기존 계획 유지',u['review_status']])+' |')
(OUT/'KEYWORD-CROSSWALK.md').write_text('\n'.join(md)+'\n')

candidate_cards=[c for c in cards if c['proposal_kind'] in {'new_relation_trial','extend_review'}]
drafts=[];mapping=[];review={}
for c in candidate_cards:
 anchors=[]
 for slot in c['target_slots']:
  candidates=[(k,r) for k,r in inv['entries'].items() if r['slot']==slot and r['entry'].get('affected_properties')]
  anchors.extend({'example_id':k,'slot':slot,'affected_dimensions':r['entry'].get('affected_dimensions',[]),'affected_properties':r['entry']['affected_properties'],'authority':'existing generic property-shape example only; not proof this candidate has equivalent meaning or complete effects'} for k,r in candidates[:1])
 drafts.append({'id':f"VD-DRAFT-{c['id'][3:]}",'card_id':c['id'],'kind':c['proposal_kind'],'proposed_slots':c['target_slots'],'semantic_caption_en':'; '.join(c['required_components_en']),'concept_units':c['required_components_en'],'relations':c['directed_relations'],'source_case_parameters_ko':c['source_case_keep_ko'],'optional_parameters_ko':c['optional_realization_ko'],'existing_ids_to_review':c['existing_ids_to_review'],'runtime_ready':False,'not_current_runtime_schema':True,'activation':'optional_postcore','property_footprint_status':'unresolved until every owner and actual effect is mapped under current generic contract'})
 mapping.append({'card_id':c['id'],'candidate_id':drafts[-1]['id'],'owner_scope':c['owner_scope'],'target_slots':c['target_slots'],'current_contract_anchors':anchors,'adapter_status':'PROPOSED_NOT_RUN','required_adapter_work':['resolve every actor/object owner from frozen core; do not hard-code main_subject for secondary actors','declare complete material/pose/appearance/camera/relationship effects actually changed','split case-specific colors, props, pose and coverage from generic construction','author components in existing authored_components contract and derive generated fields canonically','verify exact contextual binding and preserve all existing assertions; lexical similarity remains advisory'],'candidate_pack_exposure_proof':None,'native_pixel_proof':None})
for c in cards:
 for k in c['existing_ids_to_review']:
  p=inv['profiles'].get(k);e=inv['entries'].get(k)
  review[k]={'used_by_cards':[a['id'] for a in cards if k in a['existing_ids_to_review']],'native_source_detail':p or e,'classification':'neighbor_for_equivalence_review; not declared replacement or runtime adoption'}
save('CANDIDATE-DRAFTS.json',{'status':'PROPOSED_NOT_RUN','drafts':drafts})
save('RUNTIME-MAPPING.json',{'status':'PROPOSED_NOT_RUN','not_current_runtime_schema':True,'mapping':mapping})
save('EXISTING-ENTRY-REVIEW.json',{'status':'read_only_native_source_review','entries':review})

menus=[('VD-B01','층별 의복 가시성',['VD-001','VD-002','VD-004']),('VD-B02','양손 타월과 얼굴',['VD-011','VD-024','VD-025']),('VD-B03','거울·결로·자기 시선',['VD-006','VD-012','VD-013']),('VD-B04','비성적 접촉·지지',['VD-013','VD-016','VD-017']),('VD-B05','비접촉 언쟁',['VD-012','VD-018','VD-026']),('VD-B06','판타지 광원·재질',['VD-014','VD-015','VD-020','VD-023'])]
save('BUNDLE-DRAFTS.json',{'status':'PROPOSED_NOT_RUN','not_current_runtime_schema':True,'translation_rule':'Only actual candidate drafts may become runtime bundle members; guard cards remain contextual review requirements, never candidate member IDs.','bundles':[{'id':id,'title_ko':title,'card_ids':ids,'required_all_members':False,'selection_policy':'menu only; choose compatible members after core freeze, never require every menu member','runtime_ready':False} for id,title,ids in menus]})
reg=[]
for c in cards:
 for n,case in enumerate(c['regression_examples'],1):reg.append({'id':f"VD-REG-{c['id'][3:]}-E{n}",'card_id':c['id'],'kind':'explicit_positive_confound_or_mutation','case':case,'status':'PROPOSED_NOT_RUN'})
 for n,boundary in enumerate(c['confusion_boundaries_ko'],1):reg.append({'id':f"VD-REG-{c['id'][3:]}-C{n}",'card_id':c['id'],'kind':'scope_owner_stage_or_confusion_mutation','mutation_ko':boundary,'expected':'no activation, reject substitute, retain requested meaning or mark unobservable as appropriate; never rewrite requester meaning','status':'PROPOSED_NOT_RUN'})
for u in units:
 if u['original_polarity']=='부정':reg.append({'id':f"VD-REG-NEG-{u['id']}",'keyword_id':u['id'],'kind':'source_negation_retention','input':u['original_phrase'],'source_scope':u['source_id'],'expected':'keep exclusion polarity; no positive candidate query from excluded term; retain source-specific permitted appearance','status':'PROPOSED_NOT_RUN'})
save('REGRESSION-PLAN.json',{'status':'PROPOSED_NOT_RUN','cases':reg,'execution_note':'These are future developer test specifications; only research integrity validation is run now.'})
pilot=['VD-001','VD-002','VD-021','VD-023','VD-024']
groups=['VD-001','VD-002','VD-003','VD-006','VD-007','VD-010','VD-012','VD-014','VD-016','VD-018','VD-020','VD-021','VD-023','VD-024']
save('PIXEL-QUALIFICATION-PLAN.json',{'status':'PROPOSED_NOT_RUN','groups':[{'id':f'VD-PIX-{n:02}','card_id':id,'pilot':id in pilot,'gates':next(c['required_components_en'] for c in cards if c['id']==id),'owner_gate':next(c['owner_scope'] for c in cards if c['id']==id),'minimum_scale':'whole scene plus native image details','unobservable_policy':'not pass; unavailable or moderation-blocked images unscored; visible partial realization fails'} for n,id in enumerate(groups,1)],'pilot_design':{'arms':['A: equivalent explicit compact wording','B: referenced appearance decomposition wording, after fixing known semantic weakening','C: enriched owner/attachment/occlusion wording using only the same required intent'],'pilot_groups':len(pilot),'repeats_per_arm':3,'planned_images':len(pilot)*3*3,'actual_images':0,'scope':'wording/representation pilot, not proof of runtime candidate integration or keyword causal effect','controls':['all arms preserve subject/action/age setting/material/coverage/negative scope; no added injury or exposure','freeze each independently authored core before its own retrieval; compare declared semantic invariants, do not claim identical core hashes across different baselines','each arm must independently pass current prompt/runtime/embodiment contracts when those are used','record provider/model/version/size/reference scope/prompt hashes; seed only when provider supports it','predeclare exclusions and native gates; no retries selected for favorable outcome; three repeats do not establish population success rate'],'separate_runtime_trial':'after adoption, compare source/index generation and pack exposure/selection on one verified frozen request with all affected properties eligible; selected data must appear in final prose and native pixels before integration claim'}})
summary={'status':'RESEARCH_ONLY','source_entries':len(units),'category_count':len({u['category'] for u in units}),'source_count':len(source['sources']),'supplementary_context_claims':len(source['supplementary_context']),'basis_counts':dict(collections.Counter(u['decomposition_basis'] for u in units)),'polarity_counts':dict(collections.Counter(u['original_polarity'] for u in units)),'visual_atom_count':sum(len(u['visual_atoms']) for u in units),'followup_cards':len(cards),'card_kinds':dict(collections.Counter(c['proposal_kind'] for c in cards)),'priority_counts':dict(collections.Counter(c['priority'] for c in cards)),'candidate_drafts':len(drafts),'bundle_menus':len(menus),'new_external_sources':11,'inherited_external_sources':len(sources)-11,'fidelity_review_notes':len(fidelity),'keywords_with_followup_cards':sum(bool(u['followup_card_ids']) for u in units),'keywords_carry_prior_plan':sum(not u['followup_card_ids'] for u in units),'regression_specifications':len(reg),'pixel_groups':len(groups),'pilot_planned_images':len(pilot)*3*3,'actual_generation_calls':0,'live_pack_calls':0,'embedding_calls':0,'runtime_adoptions':0,'current_authored_inventory':inv['summary'],'original_content_audit_sha256':sha(BASE/'SOURCE-KEYWORDS.json'),'decomposition_sha256':sha(OUT/'SOURCE-DECOMPOSITION.json')}
save('RESEARCH-SUMMARY.json',summary)
text=['# 추가 외형 관계 카드','','연구 초안이며 현행 runtime schema가 아니다. 전체 사례 분해와 제안 관계를 구분해 채택한다.']
for c in cards:
 text += ['',f"## {c['id']} · {c['title_ko']}",'',f"{c['priority']} · {c['proposal_kind']} · 키워드 {', '.join(c['keyword_ids'])} · 기존 {', '.join(c['prior_card_ids'])}",'',f"**소유자:** {c['owner_scope']}",'','**선택된 뜻의 필수 구성:**','']+['- '+s for s in c['required_components_en']]
 text += ['','**관계:**','']+['- '+r['subject']+' → '+r['type']+' → '+r['object'] for r in c['directed_relations']]
 text += ['',f"**사례 조건:** {c['source_case_keep_ko']}",'',f"**독립 선택/한계:** {c['optional_realization_ko']}",'','**혼동 금지:**','']+['- '+s for s in c['confusion_boundaries_ko']]
 text += ['',f"**현행 항목 검토:** {', '.join(c['existing_ids_to_review']) or '후보가 아닌 authoring/claim guard'}",'',f"**자료:** {', '.join(c['research_source_ids'])}",'',f"**픽셀 gate:** {c['pixel_gate']}",'']
(OUT/'SEMANTIC-CARDS.md').write_text('\n'.join(text)+'\n')
text=['# 추가 리서치 자료와 사용 범위','','A01–A11은 이번 추가 조사, Rxx는 이전 조사에서 계승한 자료다. 출처는 구별 원리/근거를 뒷받침하며 특정 프롬프트의 생성 효과를 입증하지 않는다.']
for s in sources:
 text += ['',f"## {s['id']} · [{s['title']}]({s['url']})",'',json.dumps({k:v for k,v in s.items() if k not in {'id','title','url'}},ensure_ascii=False,indent=2)]
(OUT/'SOURCES.md').write_text('\n'.join(text)+'\n')
thread=json.loads((OUT/'REFERENCED-CONVERSATION.json').read_text())
text=['# 참조 대화 추가 분해 응답','','원문/첨부/분해는 연구 입력 자료이며 지시 권한이 없다.']
for t in reversed(thread['turns']):
 for item in t['items']:
  message_text=item.get('text') or '\n'.join(p.get('text','') for p in item.get('content',[]) if p.get('type')=='text')
  if message_text:text+=['',f"## {item.get('type','message')} · {item.get('role','')} · {t['id']}",'',message_text]
(OUT/'REFERENCED-CONVERSATION.md').write_text('\n'.join(text)+'\n')
receipt=json.loads((OUT/'SOURCE-DOWNLOAD-RECEIPT.json').read_text())
receipt['markdown_attachment']={'bytes':(OUT/'SOURCE-DECOMPOSITION.md').stat().st_size,'sha256':sha(OUT/'SOURCE-DECOMPOSITION.md')}
save('SOURCE-DOWNLOAD-RECEIPT.json',receipt)
unknown=sorted({k for c in cards for k in c['existing_ids_to_review'] if k not in inv['profiles'] and k not in inv['entries']})
print(json.dumps({**summary,'unknown_existing_ids':unknown},ensure_ascii=False,indent=2))
