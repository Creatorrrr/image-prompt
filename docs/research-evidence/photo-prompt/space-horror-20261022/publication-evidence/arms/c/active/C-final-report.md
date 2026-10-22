# C — The Missing Calibration Observer

native 이미지 1회 생성과 저장, 독립 ledger/manifest 기록, 직접 픽셀 검토 및 검토 기록 감사를 완료했다. 최종 testcase는 5 pass / 1 fail, 관리형 technical qualification은 fail이다. 사용자 판단은 pending이다. 생성 성공과 관계 실현의 실패는 별도 결과다.

## 결과와 파일

- 이미지: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/space-horror-20261022-d2fb17a8-c/active/images/missing-calibration-observer-native.png`
- 이미지 SHA256: `de8dc8a2cce379e05c85e9cddf6991edaea326dd451448ccbc33183534199569`
- 크기: 1312 × 1199
- exact prompt: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/space-horror-20261022-d2fb17a8-c/active/final_prompt.txt`
- exact prompt UTF-8 SHA256 (끝 개행 제외): `473d06118ea0db8f1a67850a530841d683359bd03a67490a7d7edf659e811976`
- negative_en: null
- 도구: native image_gen
- 실제 이미지 호출: 1, 추가 호출: 0, 외부 API/CLI fallback: 0
- 실제 이미지 모델명: 도구가 명시하지 않아 unknown
- 실제 tool이 돌려준 원본 경로: `/Users/chasoik/.codex/generated_images/01a163f1-9435-76b0-8813-caac333a5008/exec-03d11b1a-a22e-4a9d-826c-ce5b64149b54.png`
- 로컬 사본: 위 실행 폴더에 저장, 원본 보존
- 독립 ledger: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/space-horror-20261022-d2fb17a8-c/active/image_runs.ndjson`
- 독립 manifest: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/space-horror-20261022-d2fb17a8-c/active/run_manifest.json`
- ledger_run_id: `f6b85201894827a4`

## 픽셀 testcase

모든 관계는 독립적으로 고정한 agent-owned testcase이다. 사용자 추가 요구나 requester lock이 아니다. native 원본 전체와 장치/좌석 crop을 직접 확인했다. partial/unobservable은 통과로 바꾸지 않았다.

| Gate | 판정 | 관측성 | 실제 픽셀 근거 |

|---|---|---|---|

| space_isolation | pass | visible | A large bolted circular pressure window shows a hard blue-white planetary limb and black starfield behind the same interior engineer and gantry. |

| vacant_seat | pass | visible | The pale seat and back cushions are empty. Both lap-strap ends and separate unjoined buckle halves lie exposed on the cushion; the empty region around the seat remains readable beneath the mounted oval. |

| machine_surrogate | pass | visible | A matte-black oval occupies head height and two slim dark rectangular paddles sit below and to its sides at shoulder width. Thin vertical rods and the overhead gantry visibly support them, forming a mechanical head-and-shoulder suggestion over the empty chair. |

| autonomous_addressing | pass | visible | Two jointed sensing assemblies descend from the top gantry with their green-lit optical apertures directed inward toward the oval region rather than the engineer. Both endpoints and their joints are visible. This passes the specified visible orientation only; autonomous control or machine intention is not proved. |

| human_response | fail | visible | The eyes turn toward the apparatus, but the near fingers visibly contact a raised red control/cover on the console. The hand is not resting on the rail and a fingertip-to-recessed-switch gap is not present, so the complete response relation fails despite the directed gaze. |

| reference_appearance | pass | visible | The short dark bob, fine separated fringe, dark rounded eyes and soft oval facial proportions are consistent with the viewed portrait at a large usable face scale. The changed gaze and lighting are scene choices; this is broad appearance fidelity rather than identity proof. |

## 관리형 신체 관계 검토

| Gate | 판정 | 실제 픽셀 근거 |

|---|---|---|

| embodiment_body_ownership | pass | The visible near hand connects through its wrist and jacket sleeve to the engineer; the face and torso form one coherent person. The separate oval and paddles have their own rods and are visibly machine parts rather than another human body. |

| embodiment_joint_chain_and_reach | pass | The near forearm reaches the adjacent console with a plausible wrist/finger chain and ordinary bend. The shoulder-to-sleeve continuity is readable; the lower elbow continuation is an ordinary crop rather than a diagnosed hidden defect. |

| embodiment_support_and_balance | fail | The torso can plausibly stand below the crop and the targets have visible overhead supports, but the authored hand-on-control-rail support is not realized: the hand is over the console and red control, while the rail lies below the forearm. This fails that specific support relation, not human balance or an inferred unseen defect. |

| embodiment_contact_and_space | fail | Fingertips visibly touch the top/edge of a raised red control or safety cover. The reviewed baseline required fingertips stopped short of a recessed interrupt switch with a visible gap and hand supported on the rail. The intended no-contact state and recessed control boundary are replaced by contact with a raised control. |

| embodiment_visibility_and_projection | pass | The view simultaneously exposes the engineer's face, near hand and red control, empty pale chair cushion and straps, both sensor apertures, oval target, two paddles and their rods. The incorrect hand contact can be directly judged, so it is not hidden or promoted from partial evidence. |

review-audit: record_valid=true, status=pass, technical_qualification=fail. 이는 실패 판정이 포함된 검토 기록의 형식/바인딩이 유효하다는 뜻이며 이미지의 전체 요구 충족이나 사용자 수락을 뜻하지 않는다.

## 전체 인상과 약점

처음 보이는 인상은 작동 중인 궤도 광학실에서 뒤를 돌아보는 인물과 빈 의자 위 사람 같은 교정 표적의 조용한 SF 불안이다. 얼굴·빈 의자·표적의 시각적 위계와 참조 외형은 강하다. 다만 손이 이미 조작부에 닿아 있어 “누를지 멈춘 순간”의 인과가 약해졌다. 표적이 지나치게 정돈되어 평범한 교정 마네킹으로 읽힐 여지가 있고, 즉각적인 공포 강도는 제한적이다. 정지 화면은 센서 방향과 장치 지지만 보여 주며 자율 소프트웨어의 의도, 실제 제작 과정, 이전 고장, 관객 감정을 증명하지 않는다.

## 소스 노출과 사용

- 최신 기본 H-F2 `c34c69bb6a031f2938987cc687a51481e01d24710e7ba06f5e05f4130a91f849` / native `f764682eefe81421e209e28d5dddfeb63981a25834c73799790f44a09fcff431` 확인 후 실행.
- 직접 저술한 slot 3개: prop_state, relational_action, location. 자동 전체 장면 query 2개 포함 총 5개.
- 반환 query/CID/RID occurrence 40개, 고유 source 39개 모두 검토 및 개별 결정 기록.
- 새 space-horror source 노출: V02 `cand_85efea06edc050df8e26491433c115f0` (location), V64 `cand_ad404f4ef4a959779e011d2753f31587` (__baseline_prompt__).
- 다섯 standalone 대안과 baseline을 비교한 뒤 baseline 유지. retained inspiration 0, native whole-source adoption 0, 모든 occurrence use=skip.
- V02의 완전한 압력계/해치/장갑 손 관계나 V64의 lone crew/doorway/corridor/unlit viewport 관계를 부분 취해 채택으로 위장하지 않았다.
- 이 arm은 최신 신규 소스가 실제 검색에서 노출됐음을 보여 준다. 이미지가 신규 소스를 채택해 좋아졌다는 인과 증거는 아니다.
- 소스별 원문 의미/조건/효과와 개별 사유: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/space-horror-20261022-d2fb17a8-c/active/candidate-reviews.json`
- 완성 대안과 비교: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/space-horror-20261022-d2fb17a8-c/active/composition-comparison.md`
- 전체 노출/사용 요약: `/Users/chasoik/Projects/image-prompt/generated/photo-runs/space-horror-20261022-d2fb17a8-c/active/source-exposure-use.json`

## 보존과 독립성

원본 requester envelope input SHA256 `106ea97d0d090eff5c846479ebfda86bdd1c79c6b936a33a27611895ed9ecd66`를 그대로 사용했다. /active의 frozen normalized core file SHA256 `1b6085cfb509615f37b9c1430a0fbce5551c5bc7336ca2816ae289be0a79c512`, testcase SHA256 `aedf4e27ad6f511c976bb77e93c7849cacabaca9865ef1a448155bbb1bc1cf34`, controls와 baseline 등 모든 freeze 파일이 실제 바인딩과 일치한다. 최초 수정 전 freeze도 보존했고 /active만 실제 실행했다. 상세 증거는 final-preservation-proof.json.

설치 구현이 검증에 사용한 canonical core SHA256 `6c9e41eea96237456b4992f7105bc305720edd11ef089d3d73b56a3b6cb9de40`와 intent-lock SHA256 `65c5218bd41fd831152dda6fa5cbbec21ed341bc998d86fa6935d4021d101ae9`는 runtime manifest에 별도 기록된다. frozen 입력 파일의 byte hash와 canonical binding hash는 구별한다.

참조 사진은 호출 전 view_image로 확인하고 원본 경로를 실제 referenced_image_paths로 첨부했다. facial/hair appearance만 사용했으며 실제 신원·나이·성격·이력은 추론하지 않았다. 다른 arm의 프롬프트·이미지·후보·결과나 연구 산출물은 입력으로 사용하지 않았고 공용 소스/설치 config는 수정하지 않았다. 공용 checkout `/Users/chasoik/Projects/image-prompt`, source-ref `9dc853e6148f164f039e7156b8ea0a4455ea32de`, skill SHA256 `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`. 사용자 수락은 아직 없다.

## Exact runtime prompt

```text

A cinematic space-horror photograph of a person guided by the supplied portrait's facial and hair appearance, amidst spaceborne dread. In the optical calibration bay of an orbital observatory, a short dark bob and fine separated fringe frame the engineer's face; her dark rounded eyes, soft oval facial contours, natural skin texture and slightly parted lips retain the portrait's appearance. Her individual presence stays quiet and intimate against the impersonal apparatus. She stands at the left edge of an empty observer chair, wearing a worn ivory utility jacket over a charcoal undershirt. One hand rests on the control rail with the fingertips stopped just short of a recessed red interrupt switch. Her torso has turned away from the console, and her eyes follow the apparatus over the chair, lips slightly open at the realization of what it resembles. The pale seat cushion, open lap straps and empty space above the cushion are fully exposed. Two jointed sensor arms descend from an overhead calibration gantry and aim their black optical apertures toward a matte-black oval alignment target suspended above the chair at seated head height. Two thin rectangular calibration paddles hang below the oval at shoulder width. The target and paddles together suggest a silent seated figure, while their narrow mounting rods remain plainly visible as machine parts. The apparatus has arranged an apparent observer over a chair whose actual seat is empty. Green calibration light cuts across the empty cushion, and the little sensor heads remain directed inward toward their own assembled silhouette. Behind this action, a round pressure window shows the hard blue-white curve of a planet against black space; the bolted window frame, sealed wall seams and worn handrail make the room feel inhabited but isolated. Frame her face, the empty cushion and the hanging target together in one moderately wide view, with her nearer face large enough to preserve the reference cues. A restrained 40 mm perspective from her chest height keeps the rods, apertures and chair separable. Pale instrument light grazes her cheek and catches a strand of hair; a dim amber service lamp gives the chair edge a second tone. Deep but readable shadows, cool desaturated metal, subtle grain and carefully controlled practical light support the human-machine standoff. The horror rests in ordinary equipment behaving as though it has built someone to look back at her.

```
