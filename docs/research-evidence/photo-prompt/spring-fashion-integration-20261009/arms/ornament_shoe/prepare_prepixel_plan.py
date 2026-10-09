from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
ROOT=Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
S=ROOT/'skills/photo-prompt-image-generator'
w=json.loads((B/'run/workflow.json').read_text());core=json.loads(Path(w['artifacts']['authorial_core_normalized']['path']).read_text());controls=json.loads(Path(w['artifacts']['creative_controls']['path']).read_text())
raw=(B/'run/workflow.json').read_bytes();workflow_sha=hashlib.sha256(raw).hexdigest()
ref=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
rows=[]
def add(i,title,evidence,owners,edges,view,success,failures,limits,scale='native',authority='agent_authored_baseline'):
 for phrase in evidence:assert phrase in core['baseline_prompt_en'],(i,phrase)
 rows.append({'observation_id':i,'title_ko':title,'authority':authority,'baseline_evidence':evidence,'owners':owners,
 'directed_relations':[{'type':t,'subject':a,'object':b} for t,a,b in edges],
 'required_view':view,'review_scale':scale,'success_criterion':success,'false_substitutes':failures,'claim_limits':limits,
 'future_hard_contract':'Only duties derived from the immutable pack and an explicitly adopted compatible opt-in obligation become hard. This observation row is not itself a hard gate.',
 'status':'not_run'})
add('obs_reference','참고 얼굴과 짧은 검은 머리',
 ['visible facial features and short black hair guided by the supplied portrait'],
 ['reference portrait','same main subject'], [('guides_visible_appearance','reference portrait.face_and_hair','main_subject.face_and_hair')],
 'A readable oblique face view and visible bob outline; compare source and result at native scale without requiring a new camera angle.',
 'The face is visibly guided by the supplied eye/brow, nose and lip appearance, and the hair remains short and black with a fine forehead fringe and bob contour.',
 ['Generic substituted face with unrelated appearance','Long hair replacing the short bob','Face hidden beyond comparison'],
 ['Appearance guidance is not proof of personal identity, biography or exact biometric equality. Body dimensions and source outfit are outside reference scope.'],'native','request_owned_reference_scope')
add('obs_flower','어깨 장식의 실제 고정점과 입체 꽃잎',
 ["A fabric flower is fixed at the left shoulder: separate curled petal edges gather around a compact center, and the flower's base sits flush against the blouse at that single attachment point"],
 ['main_subject','same blouse','fabric flower'],
 [('attached_to','flower.base','blouse.left_shoulder'),('gathers_around','flower.curled_petals','flower.compact_center')],
 'The left shoulder, flower base and blouse contact surface must remain visible together; shallow contact shadow can support depth.',
 'Petal edges resolve as raised curled fabric forms around one center, and the base contacts the same blouse at the left shoulder.',
 ['Flat floral print','A flower floating beside the shoulder','A real flower, jewelry motif or ornament on another garment'],
 ['Visible attachment does not prove a hidden pin, stitch method, fiber content or removable fastening.'])
add('obs_drape','장식 아래에서 반대 허리로 이어지는 블라우스 드레이프',
 ["Her pale apricot blouse has a soft diagonal drape descending from the left shoulder toward the opposite waist", "The folds radiate from beneath that base instead of floating beside it"],
 ['same blouse','same shoulder flower'],
 [('descends_toward','blouse.diagonal_drape','blouse.opposite_waist'),('radiates_from_beneath','blouse.fold_bases','flower.attached_base')],
 'See the flower base, diagonal fold starts and destination at the opposite waist in the same front/oblique torso view.',
 'The blouse folds emerge below the attached base and follow a coherent downward diagonal on that same garment.',
 ['Detached fabric ribbon across the body','A shadow or printed stripe masquerading as a fold','Unconnected wrinkles far from the flower'],
 ['A static fold arrangement does not reveal sewing history or physical tension values.'])
add('obs_wrap','치마 앞판의 층 순서와 사선 자유 경계',
 ["Her sage skirt has an upper wrap panel crossing the waist, its diagonal free edge visibly lying over the under-panel"],
 ['same skirt','outer wrap panel','under-panel'],
 [('overlaps','skirt.upper_wrap_panel','skirt.under_panel'),('crosses','skirt.upper_wrap_panel','wearer.waist')],
 'The waist crossing, diagonal free edge and a continuation of the under-panel must all be visible; the sheet stays beside the torso.',
 'Two actual skirt surfaces remain separable along a diagonal edge, and the free edge lies over the under-panel with consistent local depth.',
 ['One dark line on a single panel','A center slit substituting for overlap','Pose or perspective alone creating apparent diagonal order'],
 ['Visible overlap does not prove an adjustable wrap closure, hidden tie or opening mechanism.'])
add('obs_pleats','같은 치마의 반복 플리츠와 무릎 아래 연속성',
 ["below that edge, a broad lower section falls in repeated narrow vertical pleats", "The pleats open slightly over the nearer bent knee and continue into long folds below it"],
 ['same skirt lower section','nearer knee'],
 [('below','skirt.pleated_section','skirt.wrap_edge'),('opens_over','skirt.pleats','wearer.nearer_bent_knee'),('continues_below','skirt.pleat_paths','wearer.nearer_knee')],
 'Show the wrap-to-lower-section transition, the nearer knee region and the lower fold paths toward the hem together.',
 'Repeated folded edges belong to the same lower skirt section, widen locally over the bent knee, and continue below rather than stopping as disconnected stripes.',
 ['Printed stripes','Rib knitting','Random wrinkles without repeated fold edges','A separate pleated background panel'],
 ['Pleat geometry does not prove heat setting or a manufacturing process. A fan-to-hem profile would be an additional optional variant, not automatically equivalent to local knee opening.'])
add('obs_ribbons','신발에서 발등 교차를 거쳐 발목 매듭까지 이어지는 끈',
 ["thin ribbons threaded from the shoe's side attachments across the instep in clear X crossings, then continuing around the ankle into a small tied bow", "the ribbon paths remain visible against the skin and separate from the skirt hem"],
 ['left shoe and left foot','right shoe and right foot','each shoe own ribbons'],
 [('starts_at','shoe.ribbon_paths','same_shoe.side_attachments'),('crosses_over','same_shoe.ribbon_pair','same_foot.instep'),('continues_around','same_shoe.ribbon_paths','same_ankle'),('joins','same_shoe.ribbon_ends','same_ankle.bow')],
 'Both foot uppers and ankle loops remain in frame, the nearer foot turned outward, and skirt hems clear of the ribbons. Inspect each shoe separately at native scale.',
 'The ribbons can be traced from the shoe attachments through an instep X and around the same ankle to a tied bow, retaining the correct foot and shoe owner.',
 ['Ankle bracelet disconnected from the shoe','Painted skin lines','Crossings joining different feet','Straps vanishing beneath an occluded hem','Ribbon ends unrelated to the bow'],
 ['A strap route does not prove fastening strength, comfort, dance skill or material composition.'])
add('obs_clip','오른손·클립·종이·와이어의 실제 접촉',
 ["the right thumb and forefinger pressing a wooden clip over the paper and wire", "The other upper corner is already fastened"],
 ['same main subject right hand','wooden clip','same route sheet','notice-frame wire'],
 [('presses','right_thumb_and_forefinger','wooden_clip'),('holds_together','wooden_clip','sheet.upper_corner_and_frame_wire')],
 'An oblique view must show the right thumb/forefinger ownership, clip jaw region, paper corner and wire within reachable side space.',
 'Digits belong to the right hand, contact the clip coherently, and the clip catches the paper corner at the same wire while the other corner is visibly supported.',
 ['Floating clip','Fingers fused into the paper','Clip on the board but disconnected from paper/wire','A removed or relocated sheet avoiding the contact'],
 ['The initial run has no repair lineage. Use pack-derived embodiment duties; do not invent rr repair gates or diagnose unseen joint mechanics.'])
add('obs_support','앉은 지지와 두 발의 소유·균형',
 ["Her hips are supported by the bench", "her left palm rests beside her hip on the seat", "Both feet rest flat on the planks, the nearer foot half a shoe-length ahead and angled outward"],
 ['same main subject','bench seat','landing planks'],
 [('supported_by','wearer.pelvis','bench.seat'),('rests_on','wearer.left_palm','bench.seat'),('rests_on','wearer.both_feet','landing.planks')],
 'Retain enough bench and floor context to read sitting and both foot contacts; garment-covered anatomy need not be exposed merely to prove support.',
 'The seated torso, connected legs and seat agree with one body; left palm contact and two coherent feet on planks support the intended state.',
 ['Detached limbs','Seat impossible relative to pelvis','A hovering foot described as flat contact','Foot paths belonging to another body'],
 ['Hidden but ordinary support is not automatically failure. Judge consequential relationships, not universal body ratios or reference body measurements.'])
add('obs_story','젖은 흔적·재고정된 모서리·돌아오는 배의 현재 순간',
 ["a damp crease runs diagonally across the paper, and a small ferry is entering the gap between the landing posts", "Darkened wet planks and a pale reflection under the bench carry the recent rain"],
 ['route sheet','wet landing','small returning ferry','same wearer'],
 [('carries_trace','sheet.damp_crease','recent_rain_context'),('enters_between','small_ferry','landing.posts')],
 'Read the complete frame first, then inspect the sheet crease and wet-plank reflections while keeping the boat subordinate in the background.',
 'The fastening act, already-held corner, weather traces and approaching small boat form a plausible current situation without needing the title explained.',
 ['Unrelated decorative boat','Dry generic backdrop despite the wet trace story','A striking portrait whose work situation is unreadable'],
 ['The image cannot prove actual ferry schedules, a real preceding storm, private feelings or the portrait person biography. This is supplemental artistic observation.'],'both')

docs=['SKILL.md','references/photo-workflow.md','references/image-runtime.md','references/composition-contract.md','references/embodiment-preflight.md']
plan={
 'schema_version':'photo-prepixel-observation-plan/v1','arm':'ornament_shoe','concept_name':'비 뒤 첫 배를 기다리는 접힌 항로','independent_no_cross_arm_inputs':True,
 'state':'prepared_before_retrieval_awaiting_same_generation_READY','run':str(B/'run'),
 'bindings':{'core_canonical_sha256':core['canonical_sha256'],'intent_lock_canonical_sha256':core['intent_lock']['canonical_sha256'],'baseline_sha256':w['artifacts']['baseline']['sha256'],'workflow_sha256':workflow_sha,'request_envelope_file_sha256':w['artifacts']['request_envelope_input']['sha256'],'creative_controls_sha256':controls['canonical_sha256']},
 'reference':{'path':str(ref),'sha256':hashlib.sha256(ref.read_bytes()).hexdigest(),'scope':'visible facial appearance and short black hair only; no body measurements, outfit or biography inference'},
 'postcore_documents':[{'path':str(S/p),'sha256':hashlib.sha256((S/p).read_bytes()).hexdigest()} for p in docs],
 'scope':{'requester_owned':['core topic test photograph','reference-guided subject','spring clothing visibly worn','reference face/hair use'],
 'authorial_and_optional':['ferry landing and rain traces','fastening gesture and notice sheet','shoulder flower and blouse drape','upper skirt wrap and lower pleats','lace-up ballet flats','seated pose, color, camera, framing and light'],
 'additional_test_garments':'None selected or added. After READY, any compatible test refinement remains an authored open-dimension choice or an explicitly selected optional contract.'},
 'angle_and_information_budget':{
 'current_camera_plan':'Vertical head-to-toe, just below seated eye level and obliquely across the bench; this is baseline staging on an open camera dimension.',
 'critical_projection':'Keep both feet and ankle loops in frame, the center clothing area unobscured by the side notice sheet, and the reaching hand/clip/wire beside the torso.',
 'focal_hierarchy':'Reference-guided face and fastening fingertips lead; shoulder flower, wrap/pleats and shoe ribbons form subordinate structural rhythms; small boat and wet landing supply context.',
 'complexity':'One main person, one active right-hand fastening, a separate left-hand support, one blouse, one skirt, and two shoes. Complexity comes from connected attachment, overlap, fold and ribbon relationships already authored.',
 'legibility_tradeoff':'If a small required structure is hidden or below native resolution, record fail for its actual effective gate rather than inventing details from the prompt. Read optional projections after pack retrieval before deciding whether a refinement improves visibility.'},
 'observations':rows,
 'effective_hard_gate_set':{'status':'not_derived_before_pack_and_composed_selection','gate_ids':[],'derivation':'After READY use review-shape from the exact immutable generation and audited composed selection. Copy that exact union into review records; do not substitute this planning table.'},
 'anticipated_embodiment_contract':{'source':'references/embodiment-preflight.md; final policy still to be derived from pack','likely_applicable_check_names':['body_ownership','joint_chain_and_reach','support_and_balance','contact_and_space','visibility_and_projection'],'review_scale':'native','planned_status':'not_run'},
 'selection_boundary':{'bundle_profile_rule':'Bundle-associated profile IDs remain advisory. A separately selected opt-in visual concept carries its whole obligation and gates.',
 'topic_specific_cautions':['A neckline-mounted rolled rosette is not automatically equal to the baseline shoulder flower.','A fan-to-hem pleat arrangement is not automatically equal to local opening over a bent knee.','A shoe bow is not sufficient evidence for a continuous ankle lace route.','Pointelle would need each opening rim formed by actual knit yarn loops; it is not inserted merely to use a new term.']},
 'review_sequence':['View the saved whole image and describe its impression before consulting control intensity labels.','Use the actual image path/hash and observe each declared thumbnail/native scale.','Fill every exact effective hard gate with pass or fail and image-grounded evidence; partial or unseen relationships cannot pass.','Keep supplementary relation observations, overall preference and intensity impression separate from the exact hard_gates list.','Use user_judgment.source=not_yet_received until direct requester feedback.'],
 'execution_boundary':{'runtime':'built-in image_gen','planned_actual_invocations':1,'authorization':'existing actual requesting-user image-generation instruction; no additional API/CLI path is authorized','native_attachment':'Use the exact local reference through referenced_image_paths after fresh runtime audit, with the same reference hash.','unknown_or_preview_only':'Retain the observed outcome and stop; no inferred image path, fabricated saved-image ledger or automatic rerender.','pending_steps':['coordinator validated generation READY','one pack retrieve and exact receipt generation check','full compatible candidate details and authored composition','fresh composed and runtime audits','durable native-plan/native-started before one tool invocation','save concrete returned file and review against exact effective gates']},
 'documentation_note':'composition-contract.md explains prompt-budget V3 near its start but its final marker paragraph still says budget V2. The actual current pack and matching generation auditors remain the execution authority; this plan does not rewrite shared docs.'
}
(B/'prepixel-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
lines=['# C arm 사전 픽셀 관찰표','',f"컨셉: **{plan['concept_name']}**",'', '상태: READY 대기. 아직 retrieve·compose·generate 미실행. 이 표는 사전 관찰 계획이며 실제 hard gate 목록을 대신하지 않는다.','',
 f"Frozen core: `{core['canonical_sha256']}`",'',
 '현재 구도는 앉은 눈높이 바로 아래의 세로 전신·비스듬한 시점이다. 옆 항로표가 상의 중앙을 가리지 않게 하고, 두 발과 발목 끈을 프레임에 남긴다. 얼굴과 손의 현재 행동이 먼저 읽히고 의복의 부착·겹침·반복·끈 경로가 이어져 보이는 것이 목표다.','',
 '| 관찰 관계 | 필요한 시점/표면 | 픽셀 성공 기준 | 혼동·제한 |','| --- | --- | --- | --- |']
for r in rows:
 lines.append('| '+r['title_ko']+' | '+r['required_view'].replace('|','/')+' | '+r['success_criterion'].replace('|','/')+' | '+(' / '.join(r['false_substitutes'][:2])+'; '+r['claim_limits'][0]).replace('|','/')+' |')
lines+=['','READY 이후 pack과 실제 optional selection으로 산출한 모든 hard gate를 `review-shape`에서 받아 한 저장 이미지에서 평가한다. 이 표의 authorial 관찰은 보충 기록에 두며, 선택하지 않은 프로필은 게이트가 되지 않는다. 부분 충족·가려진 연결·native 해상도에서 읽히지 않는 필수 관계는 통과로 기록하지 않는다.','',
 '추가 의복이나 기존 구조의 변형은 아직 선택하지 않았다. 필요하면 open dimensions 안에서 authorial refinement 또는 complete optional selection으로 처리하며 사용자 envelope·anchors·locks는 수정하지 않는다.','',
 '실제 사용자의 선호와 수용은 별도이며 아직 받지 않았다. built-in image_gen 1회 실행 준비만 하고 있으며, 구체 저장 경로가 반환되지 않으면 preview-only로 기록하고 추가 호출하지 않는다.','',
 '문서 확인 사항: composition-contract.md 첫 부분은 budget V3, 끝 marker 문장은 V2로 표기되어 있다. 실행 시 검증된 generation의 실제 pack 및 auditors를 따른다.']
(B/'prepixel-plan.md').write_text('\n'.join(lines)+'\n')
# Preparation leaves every managed run role byte-identical.
assert hashlib.sha256((B/'run/workflow.json').read_bytes()).hexdigest()==workflow_sha
assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in w['artifacts'].values())
report={'status':'pass','baseline_literal_binding':'pass','observation_rows':len(rows),'native_or_both_rows':len(rows),'exact_effective_gate_set':'pending_after_ready','core_and_run_artifacts':'unchanged','retrieve':'not_run','compose':'not_run','generate':'not_run','prepixel_plan_sha256':hashlib.sha256((B/'prepixel-plan.json').read_bytes()).hexdigest()}
(B/'prepixel-plan-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
