B 독립 시험은 최초 native 이미지 호출의 출력 심사 차단으로 종료되었습니다. 신규 데이터가 현재 pack과 최종 프롬프트·감사·실제 참조 첨부 호출에 사용된 사실은 확인했습니다. 이미지가 반환되지 않아 픽셀 반영·전체 인상·사용자 수용은 확인하지 못했습니다.

## 독립 저작과 요청 보존

OS 랜덤 seed `2358601300`을 세 가지 독립 저작 극장 컨셉에 modulo 3으로 적용해 `clockwork_moth_cabaret`를 선택했습니다. 막이 열리는 극장 날개에서 공연자가 검은 보면대 모서리에 걸린 나방 망토 레이스를 풀고, 오른손으로 무게를 덜며 왼손으로 루프를 해제하는 한 순간입니다. 의상·장면·팔레트·카메라는 에이전트 선택이며 사용자 지정으로 잠그지 않았습니다. 원문 envelope를 보존했고 사진의 보이는 얼굴·헤어만 guidance로 사용했습니다. 다른 arm 입력을 읽지 않았다는 활동 선언을 보존했으며, 해시 자체가 독립 저작 순서를 증명한다는 주장은 하지 않습니다.

- 원문 envelope SHA256: `7faf539417a1cf780578a41a8b544423b834fb7f7a6b68993b3d6443f02389cd`
- frozen core: `bed565446e982bf95d4d1505bcd0cfe0f01c8bef9430ccb5708ff90665e71206`
- intent lock: `e1b4962a80e07e7fb45bf3cf40ec08c887f08582d5d0986c934daad5608d6fb8`
- controls: `eb52bb793f521c0d1e5d88407a039431767a4a63702f2bdc600b454d0e9d344d`
- skill: `9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b`
- reference: `048adbd3e4343a3725fec6aa0455aa1f367878560bc15d4493a18fde1ce8604c`

저장된 강도를 그대로 사용했습니다: sensual=1, fetish=0, surreal=0, creativity=1, sensual_led, viewer_experience=false, reference_edit_mode=off, trend=off. 생성 후 강도 보정은 수행하지 않았습니다.

## 검색 노출과 실제 선택

최초 `run`에서 한 pack `821bd9074ee5b434`를 조회했으나 115개 catalog 전체에서 신규 `wkr_`가 0개였습니다. 원본 pack·receipt·core·노출 실패를 그대로 보존하고 해당 run에서는 이미지 호출을 하지 않았습니다. 부모의 source 보완 게시 후 byte-equal neutral 입력으로 `run_requalification_01`에서 정확히 한 새 pack `60ba1eadbdebc7c2`를 조회했습니다. receipt generation은 `c68a7d2e44db608a6372800dae6f51dc99ca907bfb561e6e5c8fd05aae262f14`, source fingerprint는 `c934e9f60126fe1f111ede9e80bf045907624404589b8d28fb45ebd669b73444`입니다. 새 pack SHA256는 `5bb7852298fd4c80813b333948b4bbbc9b5099d6807d54fa10e011a471038ff4`입니다.

새 catalog 116개 중 신규 visual concept 2개가 노출되었고 ordinary/bundle 신규 노출은 각각 0개였습니다. 신규 2개를 모두 전체 의미로 선택했습니다. 불투명 벨벳 몸판과 같은 의상의 시어 오간자 소매는 처음의 의상에 이미 있었으므로 어깨의 봉제 접합을 명확히 했습니다. 목선 안쪽의 좁은 검은 스캘럽 트림은 기존 몸판 경계에만 추가했습니다. 몸판 투명화·별도 속옷·전신 새 층은 선택 의미의 대체물로 인정하지 않습니다.

- `visual-concept:wkr_wk074_selected_relation`
- `visual-concept:wkr_wk025_selected_relation`
- `visual-concept:sheer_garment_optical_layering`

함께 선택한 기존 후보는 `slot:garment_detail:clt_ct031_v1`, `slot:focus:vg_face_hands_place_readability`, `slot:lighting:sf_174_base`입니다. 일반 품질 후보 5개는 전체 effects가 보호된 reference 얼굴·헤어 속성과 양립한다는 근거가 부족해 첫 감사 실패 후 제외했고 원래 effects를 축소해 통과시키지 않았습니다. 선택/거절 근거와 full-detail source는 [composition_selection_review.json](composition_selection_review.json), [requalification_candidate_details.json](requalification_candidate_details.json)에 있습니다.

원본 retrieval seed는 `377896235271679795`, 새 seed는 `9202785328979850488`입니다. core·controls는 동일하나 검색 seed가 달라 matched before/after 인과 실험이 아닙니다. 현재 게시 세대에서의 실제 노출·opt-in·실제 호출 사용을 확인한 증거입니다.

## 감사와 실제 호출

core freeze와 독립 feature selection은 PASS였습니다. composition attempt 1의 failures를 보존하고, 후보 제외·fetish=0 baseline brief 보완 후 attempt 2는 PASS, quality는 WARN(자유 서술로 보존된 anchor 진단 4건)이었습니다. runtime audit는 PASS이며 참조 1개 bytes, negative prompt, intent와 effective visual contract가 일치했습니다. 최종 본문은 658단어이며 prompt SHA256는 `aa3b3409885d32f098218bc5114cf29d449623ef9d02e39ebb3e0c63c6269963`, runtime prompt SHA256는 `072114d4b3ff75e569739dff06770e1f5912b8c7085f40accb7a9bdfe5fc0733`입니다.

현재 image-runtime의 shared capture helper와 감사된 native-plan/start/result를 사용했습니다. arm-local wrapper는 첫 official recorder call에 provenance와 manifest 인자만 추가했고 canonical script를 수정하거나 ledger를 중복 append하지 않았습니다. 실제 내장 `image_gen` 호출 1회에 원본 참조 경로를 첨부했습니다. 도구는 HTTP 400 `moderation_blocked`, `output` 단계, `sexual` 분류를 반환했습니다. request id는 `adfc0888-f928-47b4-aed9-61bde9d9db82`입니다. 이는 반환된 분류이며 어떤 문구가 정확한 차단 원인인지는 분리 검증하지 않았습니다. 요청 transport model은 gpt-image-2지만 반환 도구가 실제 모델을 식별하지 않아 관측 모델을 주장하지 않습니다.

공식 ledger는 1행, run id `19f504c80ece86c9`, 상태 `safety_block`, `image_call_count=1`, image paths/hashes는 빈 배열입니다. 오류 전체 문자열을 exact_string fidelity로 [attempt01_native_error.json](attempt01_native_error.json)에 저장했습니다. SHA256는 `933b833317214699dfdffba662cfd017fd05e2491d4c4a34578473f257691434`입니다. 수리 호출·fallback·근접 재시도는 각각 0회입니다.

## 필수 픽셀 게이트와 전체 상황

effective contract SHA256는 `fd95956313fbadc56405af1699e2703f05d539a599abb4bf70552a15fcebefdb`입니다. 선택 visual gate 7개와 embodiment gate 5개 모두 이미지가 없어 관찰 불가입니다. 이미지 path/hash가 필요한 정식 픽셀 감사기를 가짜 입력으로 호출하지 않았습니다. 통과 0개이며 텍스트만으로 신체 결함을 진단하지도 않았습니다.

| Gate | Scale | 결과 |
| --- | --- | --- |
| `vo_wkr_wk074_selected_relation_1` | native | UNOBSERVABLE_NOT_PASS |
| `vo_wkr_wk025_selected_relation_1` | native | UNOBSERVABLE_NOT_PASS |
| `vo_sheer_textile_first_read` | thumbnail | UNOBSERVABLE_NOT_PASS |
| `vo_sheer_weave_edge_legibility` | native | UNOBSERVABLE_NOT_PASS |
| `vo_sheer_transmission_relationship` | both | UNOBSERVABLE_NOT_PASS |
| `vo_sheer_layer_coherence` | native | UNOBSERVABLE_NOT_PASS |
| `vo_sheer_not_optical_or_generation_substitute` | both | UNOBSERVABLE_NOT_PASS |
| `embodiment_body_ownership` | native | UNOBSERVABLE_NOT_PASS |
| `embodiment_joint_chain_and_reach` | native | UNOBSERVABLE_NOT_PASS |
| `embodiment_support_and_balance` | native | UNOBSERVABLE_NOT_PASS |
| `embodiment_contact_and_space` | native | UNOBSERVABLE_NOT_PASS |
| `embodiment_visibility_and_projection` | native | UNOBSERVABLE_NOT_PASS |

별도 전체상황 체크 9개(브로치/체인 양 끝, 자수 carrier/패널 접합, 허리 리본, 레이스 실제 걸림·해제, 양손의 역할/무게 지지, 소매/몸판 접합, 귀걸이 소유자/수량, 무대 목적지, 얼굴·헤어 guidance)도 모두 관찰 불가입니다. 원본 픽셀·thumbnail·미학·행위 인과·강도 calibration은 평가하지 못했습니다. 직접 사용자 수용은 **pending**입니다. 전체 기록은 [pixel_review_not_run.json](pixel_review_not_run.json)에 있습니다.

## 경로와 호출수

arm 폴더: `/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/wardrobe-keyword-integration-20261010/arms/b`

- pack retrieve: 총 2회, 각 run 1회
- 실제 native image call: 1회, 반환 이미지: 0개
- repair/fallback image call: 0회
- 공식 ledger append: 1회, manifest: 1개
- 정식 픽셀 감사 호출: 0회
- composition audit: 2회(최초 실패 보존)

읽기 가능한 지도는 [ARTIFACT_MAP.md](ARTIFACT_MAP.md), 구조화 보고는 [ARM_B_REPORT.json](ARM_B_REPORT.json), 공식 실행 기록은 [image_runs.ndjson](image_runs.ndjson)와 [run_manifest.json](run_manifest.json)입니다. 무이미지 gate 추출 중 발생한 로컬 key/shape 오류 두 건과, raw request text를 JSON으로 일괄 읽으려던 무결성 검사 오류 한 건을 원본 오류 파일로 보존했습니다. corrected derivation의 failures는 빈 배열이며 무결성·해시·실행 증거 검사 83건은 PASS입니다. [FINAL_VERIFICATION.json](FINAL_VERIFICATION.json)에 결과가 있습니다. 이 오류들은 이미지 호출이나 픽셀 평가 시도가 아닙니다. 공식 workflow의 요약 phase는 `invocation_reserved`지만 operation은 `provider_blocked`, 마지막 이벤트는 `attempt_recorded`, terminal=true입니다. 상태 파일을 임의 변경하지 않았습니다.

## 최종 영어 프롬프트

[final_prompt_en.txt](final_prompt_en.txt)와 아래 본문은 감사된 composed prompt와 동일합니다. 실제 호출에는 pack의 negative prompt와 원본 참조 path가 별도 감사된 transport로 함께 전달되었습니다.

A richly layered photographic scene captures a person whose face and hair are guided by the supplied portrait, in a visible costume action with a readable material consequence. A cabaret performer stands in the narrow wing of a small theatre, just as the crimson curtain opens onto an amber lane of stage light. The portrait's soft facial outline, brown eyes, dark chin-length bob and fine center-parted fringe guide her visible appearance. She has turned her face toward the troublesome cape edge, lips gently parted in concentrated patience; the warmth on her cheek keeps her poised presence intimate and immediate. Her fitted forest-green velvet bodice has a softly curved neckline and cream organza puff sleeves. The same garment has an opaque bodice and a distinct sheer sleeve with a readable joining boundary. At the shoulder, the cream organza is sewn directly into the forest-green velvet edge, so both fabric surfaces and their joining stitch line remain visible. A narrow scalloped trim follows the inside of the same garment's neckline edge. Tiny black lace scallops sit just inside the green neckline, with the green outer fabric edge still visible. A continuous princess seam sweeps down the green front panel to the waist, visibly stitching its edge to the adjacent side-front panel. The velvet's dense dark pile absorbs light. A translucent organza layer forms the cream sleeves, where fine visible organza weave follows the puffed curves. Their visible weave seam and edge catch the cooler wing fill; a visible seam edge and fold identify the same sleeve layer. Along those sleeves, light passes through the fabric from the stage opening. At her upper arms, underlying body contours remain partly visible beneath the readable garment fibers. Where the organza doubles near the gathered cuffs, folds become denser and less transparent. A copper satin waist ribbon is tied into a compact bow over a deep teal pleated skirt. A midnight-blue satin cape hangs from two bronze moth brooches at her upper chest, joined by a short curved bronze chain; each end attaches visibly to one brooch. Amber organza inserts interrupt the dark cape panels, and raised copper embroidery follows branching moth-wing veins across those inserts. A narrow black scalloped lace border is sewn along the cape's lower edge. One bronze drop earring hangs from each visible ear, catching small warm highlights near her bob. The cape border has snagged on the outer corner of the black music stand beside her. Her right hand lifts a loose fold above the snag to take the fabric's weight, while her left thumb and forefinger ease one caught lace loop upward from the stand's corner. Both forearms connect visibly back to her shoulders; her elbows stay in the clear space beside her torso. The pinched lace makes a small compressed crease between her left finger pads, with a tiny contact shadow at the black corner. The remaining loop is taut at the metal corner, and a newly released length of lace curls softly below her left hand. Her balanced stance lets the skirt settle into long downward folds. The open curtain and stage-light lane sit behind the freed cloth, giving the little practical struggle an immediate destination. Make a vertical environmental portrait from head to below the knees, observed nearby at chest height from slightly in front of her. Keep her face, hands, chest clasp and music-stand corner readable together. Keep the eyes and fingertip-to-lace contact in the same clear focal zone, with the crimson curtain recognizable behind them. Cooler backstage fill preserves the green bodice and blue cape beside the amber stage glow. The amber stage lamp behind her shoulder runs a thin light line along the outer strands of her bob, while the cooler wing light keeps her face at a comfortable reading exposure. Fine cloth weave, seam joins, skin texture and scuffed floor boards remain naturally photographic. The face leads, the fabric tension answers it, and the bright opening beyond is the third beat.
