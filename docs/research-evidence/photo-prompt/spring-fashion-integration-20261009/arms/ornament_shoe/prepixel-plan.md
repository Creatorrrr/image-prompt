# C arm 사전 픽셀 관찰표

컨셉: **비 뒤 첫 배를 기다리는 접힌 항로**

상태: READY 대기. 아직 retrieve·compose·generate 미실행. 이 표는 사전 관찰 계획이며 실제 hard gate 목록을 대신하지 않는다.

Frozen core: `393271e22974a13aa70795cce9d045625ca01288116378a4df28bee37d786af2`

현재 구도는 앉은 눈높이 바로 아래의 세로 전신·비스듬한 시점이다. 옆 항로표가 상의 중앙을 가리지 않게 하고, 두 발과 발목 끈을 프레임에 남긴다. 얼굴과 손의 현재 행동이 먼저 읽히고 의복의 부착·겹침·반복·끈 경로가 이어져 보이는 것이 목표다.

| 관찰 관계 | 필요한 시점/표면 | 픽셀 성공 기준 | 혼동·제한 |
| --- | --- | --- | --- |
| 참고 얼굴과 짧은 검은 머리 | A readable oblique face view and visible bob outline; compare source and result at native scale without requiring a new camera angle. | The face is visibly guided by the supplied eye/brow, nose and lip appearance, and the hair remains short and black with a fine forehead fringe and bob contour. | Generic substituted face with unrelated appearance / Long hair replacing the short bob; Appearance guidance is not proof of personal identity, biography or exact biometric equality. Body dimensions and source outfit are outside reference scope. |
| 어깨 장식의 실제 고정점과 입체 꽃잎 | The left shoulder, flower base and blouse contact surface must remain visible together; shallow contact shadow can support depth. | Petal edges resolve as raised curled fabric forms around one center, and the base contacts the same blouse at the left shoulder. | Flat floral print / A flower floating beside the shoulder; Visible attachment does not prove a hidden pin, stitch method, fiber content or removable fastening. |
| 장식 아래에서 반대 허리로 이어지는 블라우스 드레이프 | See the flower base, diagonal fold starts and destination at the opposite waist in the same front/oblique torso view. | The blouse folds emerge below the attached base and follow a coherent downward diagonal on that same garment. | Detached fabric ribbon across the body / A shadow or printed stripe masquerading as a fold; A static fold arrangement does not reveal sewing history or physical tension values. |
| 치마 앞판의 층 순서와 사선 자유 경계 | The waist crossing, diagonal free edge and a continuation of the under-panel must all be visible; the sheet stays beside the torso. | Two actual skirt surfaces remain separable along a diagonal edge, and the free edge lies over the under-panel with consistent local depth. | One dark line on a single panel / A center slit substituting for overlap; Visible overlap does not prove an adjustable wrap closure, hidden tie or opening mechanism. |
| 같은 치마의 반복 플리츠와 무릎 아래 연속성 | Show the wrap-to-lower-section transition, the nearer knee region and the lower fold paths toward the hem together. | Repeated folded edges belong to the same lower skirt section, widen locally over the bent knee, and continue below rather than stopping as disconnected stripes. | Printed stripes / Rib knitting; Pleat geometry does not prove heat setting or a manufacturing process. A fan-to-hem profile would be an additional optional variant, not automatically equivalent to local knee opening. |
| 신발에서 발등 교차를 거쳐 발목 매듭까지 이어지는 끈 | Both foot uppers and ankle loops remain in frame, the nearer foot turned outward, and skirt hems clear of the ribbons. Inspect each shoe separately at native scale. | The ribbons can be traced from the shoe attachments through an instep X and around the same ankle to a tied bow, retaining the correct foot and shoe owner. | Ankle bracelet disconnected from the shoe / Painted skin lines; A strap route does not prove fastening strength, comfort, dance skill or material composition. |
| 오른손·클립·종이·와이어의 실제 접촉 | An oblique view must show the right thumb/forefinger ownership, clip jaw region, paper corner and wire within reachable side space. | Digits belong to the right hand, contact the clip coherently, and the clip catches the paper corner at the same wire while the other corner is visibly supported. | Floating clip / Fingers fused into the paper; The initial run has no repair lineage. Use pack-derived embodiment duties; do not invent rr repair gates or diagnose unseen joint mechanics. |
| 앉은 지지와 두 발의 소유·균형 | Retain enough bench and floor context to read sitting and both foot contacts; garment-covered anatomy need not be exposed merely to prove support. | The seated torso, connected legs and seat agree with one body; left palm contact and two coherent feet on planks support the intended state. | Detached limbs / Seat impossible relative to pelvis; Hidden but ordinary support is not automatically failure. Judge consequential relationships, not universal body ratios or reference body measurements. |
| 젖은 흔적·재고정된 모서리·돌아오는 배의 현재 순간 | Read the complete frame first, then inspect the sheet crease and wet-plank reflections while keeping the boat subordinate in the background. | The fastening act, already-held corner, weather traces and approaching small boat form a plausible current situation without needing the title explained. | Unrelated decorative boat / Dry generic backdrop despite the wet trace story; The image cannot prove actual ferry schedules, a real preceding storm, private feelings or the portrait person biography. This is supplemental artistic observation. |

READY 이후 pack과 실제 optional selection으로 산출한 모든 hard gate를 `review-shape`에서 받아 한 저장 이미지에서 평가한다. 이 표의 authorial 관찰은 보충 기록에 두며, 선택하지 않은 프로필은 게이트가 되지 않는다. 부분 충족·가려진 연결·native 해상도에서 읽히지 않는 필수 관계는 통과로 기록하지 않는다.

추가 의복이나 기존 구조의 변형은 아직 선택하지 않았다. 필요하면 open dimensions 안에서 authorial refinement 또는 complete optional selection으로 처리하며 사용자 envelope·anchors·locks는 수정하지 않는다.

실제 사용자의 선호와 수용은 별도이며 아직 받지 않았다. built-in image_gen 1회 실행 준비만 하고 있으며, 구체 저장 경로가 반환되지 않으면 preview-only로 기록하고 추가 호출하지 않는다.

문서 확인 사항: composition-contract.md 첫 부분은 budget V3, 끝 marker 문장은 V2로 표기되어 있다. 실행 시 검증된 generation의 실제 pack 및 auditors를 따른다.
