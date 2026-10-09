C의 신규 플러터 소매 시각 계약은 원본에서 3/3 통과했고, 신규 A라인 번들의 두 구성요소와 옆선→밑단 관계도 같은 이미지에서 읽힌다. 전체 hard gate는 7/8이며, 이 사례의 all-of 판정은 FAIL이다. 기능적인 지도 접촉은 성립하지만 actor-left palm / actor-right stone으로 검토한 좌우 역할이 실제 이미지에서 바뀌었다. 해부학적 결함을 주장하는 실패가 아니다.

독립적인 세 상황의 난수 선택은 seed 6893528243682979591, index 0이며, 후보 접근 전에 core와 reference scope를 고정했다. 이후 source generation 4d983fa8c19d53c5be8f1269ef5897d9c04ae02a90ed3e3d76eff0e7e47cb756와 fingerprint 3627d26fe90e911e3c3ce6001eed297d98767530a3bbe2b042078ae5af1c8060에서 조회했다. 실제 내장 image_gen 호출은 1회, ledger 행도 1개이며 재호출은 없다. 원본은 1024×1536, SHA-256 55b2818e8800809b4a76e1f51dfa403a21629fa9ccf9e0a067643cf50f904a1c다.

사진을 먼저 읽으면 햇빛 아래 책가판의 여름 패션 화보로 보인다. 연속된 하늘색 드레스가 가장 큰 형태이고, 얼굴과 지도 위 손이 다음 시선을 이끈다. 손바닥·돌·눌린 종이·들린 종이가 지도 안정화라는 작은 사건을 구성한다. 바람은 가능한 설명이지만, 종이의 접힌 형태만으로 실제 바람을 확정할 수는 없다.

인물의 짧은 어두운 단발, 분리된 앞머리, 보이는 얼굴은 참고 사진의 가시 얼굴·머리 안내와 일관된다. 정체성, 나이, 체형 유사성, 성격이나 실제 내면을 판단하지 않았다. 정돈된 포착, 열린 목선과 느슨한 천의 흐름은 일상적인 여름 화보에서 보조적인 매력을 만든다는 agent 판단이며 사용자 수용이 아니다.

신규 노출은 visual-concept:suf_sf032_v1, bundle:suf_sf058_v2_bundle, slot:wardrobe_style:suf_sf058_v2_candidate다. 채택한 것은 앞의 profile과 bundle이며, 마지막 member는 동일 번들의 중복이어서 선택하지 않았다. A라인 associated profile은 자동으로 hard profile에 승격하지 않았다. V-neck, wrap, 비대칭 밑단, 에스파드리유 스타일, 두 목걸이, 가방은 독립 초안의 관찰 축이며 이 축 전체를 신규 데이터 채택으로 주장하지 않는다.

| Gate | 판정 | 원본 근거 |
|---|---|---|
| vo_suf_sf032_v1_1 | PASS | Native upper-body crop shows the same blue dress sleeve ending in a loose, curved flared edge on both sides. The edge extends laterally beyond the upper-arm skin rather than fitting it tightly. |
| vo_suf_sf032_v1_2 | PASS | Native sleeve crop shows the lower fabric projecting outward from the upper arm, with readable space and an underside shadow between the outer free edge and the arm. This is visible cloth clearance, not a claim about fiber content or hidden lining. |
| vo_suf_sf032_v1_owner | PASS | The sleeve attachment at the shoulder, the blue sleeve fabric, its flared lower perimeter and the adjacent upper arm are visible on the same dress and woman. The shoulder-to-free-edge path is not borrowed from a different garment or accessory. |
| embodiment_body_ownership | PASS | Full frame and native hand crop show both forearms continuing from the same woman into two separate hands. Both lower legs continue toward the visible sandals; no extra actor or detached action-bearing part is seen. |
| embodiment_joint_chain_and_reach | PASS | Shoulder-to-upper-arm-to-elbow-to-wrist paths remain coherent. Modest forward torso inclination and bent elbows reach the nearby waist-high map without an impossible joint turn or excessive reach. |
| embodiment_support_and_balance | PASS | Both sandal soles visibly meet the dry paving, with a staggered two-foot base under the inclined torso. The stance and table height support a plausible modest working lean. Hidden knee surfaces are not being claimed as directly observed. |
| embodiment_contact_and_space | FAIL | The native map crop clearly shows one palm pressing the paper and the other hand gripping a separate stone on the map; the boundaries and space are coherent. However, the actor-right hand presses the paper and the actor-left hand holds the stone, mirroring the reviewed actor-left-palm/actor-right-stone choreography. Functional contact is present, but the complete reviewed actuation is not preserved, so this conservative full-fidelity gate is FAIL rather than a partial PASS. |
| embodiment_visibility_and_projection | PASS | The full frame and native map crop expose the two hands, stone, flattened paper and lifted paper edge together; the body supports and footwear remain within the frame. This permits assessment of the actual contact and of the handedness mismatch rather than hiding the mechanism. |

부가 장면 관찰은 8/12다. A라인의 퍼지는 옆선과 A형 윤곽, V-neck과 wrap overlap, 서로 다른 높이의 wrap hem, 두 목걸이의 분리된 호, 두 strap endpoint를 가진 같은 가방, 교차 toe straps와 ankle ties, 지도 안정화는 관찰된다. 가방은 초안의 actor-left 대신 actor-right에 있고, 눈은 지도 코너보다 옆을 바라본다. 두 신발의 뒤꿈치 쐐기 구조는 앞쪽 시점으로 충분히 관찰되지 않아 UNOBSERVABLE_NOT_PASS다. 일부 축의 성공을 전체 장면 PASS로 바꾸지 않았다.

source·prompt/runtime·native pixels·user acceptance는 별도다. composed 및 runtime audit는 PASS, native review record는 유효하며 technical qualification은 FAIL, 사용자 판단은 pending이다. 전달용 prompt와 실제 native runtime bytes는 각각 아래 파일에 보존했다. 공식 manifest helper는 실제 ledger 행을 읽어 manifest를 만들었으며 추가 ledger 행이나 호출을 만들지 않았다. 현재 managed native_result의 arm/worktree/skill/source 메타데이터 자동 전달 공백은 별도 provenance 파일에 남겼다.

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/final-prompt.txt) · [실제 native runtime prompt](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/final-runtime-prompt.txt) · [원본 이미지](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/generated_images/case-c-canal-bookstall.png) · [픽셀 리뷰](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/visual-review.json) · [선택과 literal evidence](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/topic-selection.json) · [실행 ledger](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/image_runs.ndjson) · [독립 manifest](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/run_manifest.json)

![C 원본](/Users/chasoik/Projects/image-prompt/runs/summer-fashion-qualification-20261009/case_c/generated_images/case-c-canal-bookstall.png)
