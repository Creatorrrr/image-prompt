Arm A의 독립 랜덤 역사 복식 테스트는 원본 픽셀 검사와 승인된 1회 좁은 수정 재시험까지 완료했습니다. 전체 qualification은 FAIL입니다. 새 uniform profile은 두 번째 이미지에서 2/2 gate를 만족하지만, 원래 sash 삽입 행동 및 전체 주아브 구성 관계는 완전 통과하지 못했습니다.

랜덤 seed는 3294407901809763550입니다. 일반 역사 복식 지식으로 함께 쓰기 쉬운 동다리+전복, 후사르+펠리스, 주아브 세 묶음을 독립적으로 추첨해 주아브를 선택했습니다. 성인 가상 여성 모델이 오후 창빛의 station baggage hall에서 열린 의상 trunk 옆에 서서 오른손으로 sash tail을 넣는 작은 행동을 하는 full-length 사진입니다. Navy 짧은 open jacket, 독립 waistcoat, broad red sash, 두 scarlet full trousers, white gaiters, dark shoes, low red fez와 tassel을 조합하고 원본 첨부 얼굴·단발 외형을 참조했습니다. 컨셉과 checklist는 agent-authored이며 사용자 원문·정의·필수 assertion으로 올리지 않았습니다.

사용자 envelope/core/controls/intent lock 및 최초 supplemental checklist bytes는 그대로입니다. Envelope file SHA256은 5839e3317ba0975e6c606af8838c42967ff6ea12147b06be38a032df3aa78fcc, core file SHA256은 bc0e022b61976559f58039d617e76cf62cf8b847b9372901d1d019c7cd196c00입니다. 첨부 실제 신원·연령은 판단하지 않았고 requesting-user acceptance는 pending입니다.

같은 frozen core와 pack seed 7583216431674104022로 초기 snapshot pack ae9a4276a69e4d0d 및 보강 snapshot-2 pack 7368cb12b1aef16e를 비교했습니다. 초기 ordinary retrieval은 unif_shoulder_draped_empty_sleeve와 unif_jacket_attached_false_vest를 반환했지만 각각 다른 Hussar/pelisse 의미와 독립 waistcoat 충돌 때문에 거절했습니다. 이후에도 이 ordinary 후보는 거절했으며, 새/보강 ordinary 후보 채택은 0개입니다. Snapshot-2가 반환한 visual-concept:uniform_full_trousers_gathered_cuffs를 기존 두 부피 바지+ankle gathering과 맞는 optional 의미로 독립 채택했습니다. Profile uniform_full_trousers_gathered_cuffs의 두 전체 구성관계가 literal prompt evidence로 바인딩되어 vo_uniform_full_trousers_gathered_cuffs_1 및 _2 native gate로 실제 컴파일되었습니다. 선택이 사용자 hard assertion에서 발생한 것은 아닙니다.

두 composed/runtime audit 모두 PASS입니다. 첫 composed quality는 미해결 generic uncovered-intent warning 4개이며, literal anchor는 보존됐습니다. 수정 composed에는 같은 4개와 460 words/권장 360 words advisory 두 개가 추가됐으나 hard failure는 없습니다. Pixel audit는 두 번 모두 schema failure 없이 failed_technical_hard_gates입니다. Prompt/runtime 통과는 픽셀 통과와 구분했습니다.

| 판정 범위 | 첫 이미지 | 수정 이미지 |
|---|---:|---:|
| 실제 compiled gate PASS | 3/7 | 5/7 |
| 실제 uniform profile gate PASS | 1/2 | 2/2 |
| 최초 supplemental keyword gate PASS | 4/7 | 3/7 |
| 최초 supplemental component PASS | 15/18 | 14/18 |
| 전체 결과 | FAIL | FAIL |

아래는 동일하게 유지된 실제 compiled 7개 gate입니다. 분자/분모는 해당 gate의 독립 픽셀 관찰 단위이며, gate 전체 통과 여부는 모든 해당 단위가 필요합니다.

| 실제 gate | 첫 이미지 | 수정 이미지 |
|---|---|---|

| vo_uniform_full_trousers_gathered_cuffs_1 | PASS 2/2 | PASS 2/2 |

| vo_uniform_full_trousers_gathered_cuffs_2 | UNOBSERVABLE 0/2 | PASS 2/2 |

| embodiment_body_ownership | PASS 1/1 | PASS 1/1 |

| embodiment_joint_chain_and_reach | FAIL 0/1 | PASS 1/1 |

| embodiment_support_and_balance | PASS 1/1 | PASS 1/1 |

| embodiment_contact_and_space | FAIL 0/1 | UNOBSERVABLE 0/1 |

| embodiment_visibility_and_projection | UNOBSERVABLE 0/1 | UNOBSERVABLE 0/1 |


수정은 parent-bound 두 축만 사용했습니다: gathered cuff visibility와 원래 right-fingertip sash contact visibility. 두 red cloth cuff 자체의 좁은 상·하 경계를 white gaiter와 분리해 노출했고, 착용자 오른팔(image left)이 waist로 가도록 기존 좌우를 구현했습니다. 두 full trouser volume, 다른 복식, 얼굴·단발, 장면·빛은 유지했습니다. 오른손의 tail 외부 접촉은 보이지만 윗 wrap fold 안으로 tail이 들어가는 접합이 손 뒤에 가려져 contact/visibility는 UNOBSERVABLE입니다. 새 gate를 추가하거나 기준을 완화하지 않았습니다.

| 최초 supplemental gate | 첫 이미지 | 수정 이미지 |
|---|---|---|

| agent_zouave_short_open_jacket | FAIL 2/3 | FAIL 2/3 |

| agent_zouave_separate_waistcoat | UNOBSERVABLE 1/2 | UNOBSERVABLE 1/2 |

| agent_zouave_waist_sash | FAIL 2/3 | FAIL 2/3 |

| agent_zouave_full_trousers | PASS 3/3 | PASS 3/3 |

| agent_zouave_gaiter_junction | PASS 3/3 | UNOBSERVABLE 2/3 |

| agent_zouave_fez_bob_relation | PASS 3/3 | PASS 3/3 |

| agent_zouave_same_wearer | PASS 1/1 | PASS 1/1 |


Jacket hem이 broad sash 윗부분과 겹쳐 첫 checklist의 위아래 관계는 두 이미지 모두 FAIL입니다. Navy 내부 V-neck/button panel은 보이지만 독립적으로 착용한 waistcoat인지 attached false vest인지 접합이 가려져 UNOBSERVABLE입니다. 수정에서 red cuff는 white gaiter 위에 분리되어 보이지만 trouser terminal이 gaiter 내부에 들어가는 실제 겹침은 가려져 gaiter enclosure 구성도 UNOBSERVABLE입니다. 이 관찰은 선정 profile의 cuff/gaiter 분리 PASS와 구분했습니다. Partial=FAIL, 가린 접합=UNOBSERVABLE→audit fail로 처리하고 서로 다른 이미지의 구성요소를 합치지 않았습니다. Moderation은 두 호출 모두 차단되지 않았습니다.

Native built-in image_gen.imagegen을 총 2회 사용했습니다. 첫 호출은 첨부 원본만, 수정은 첨부 원본+첫 이미지를 referenced_image_paths로 전달했습니다. CLI/API fallback과 추가 호출은 없습니다. Native 원본을 삭제하지 않고 own arm에 byte-identical copy를 보존하고 view_image detail original로 검사했습니다. 첫 원본 1237×1272, 수정 원본 1236×1272입니다.

1번 결과: /Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-a/snapshot-2/zouave-native-attempt-1.png

원본 tool 경로: /Users/chasoik/.codex/generated_images/01a10547-e6a7-7ad2-a78c-a36e4273cbdd/exec-93aa7503-3a55-40f2-a7c7-47e4e0bdc631.png

SHA256: c356e7d0b15667e624c6cf08e381857e16e6f3da98f76ea26b7d68b5150d0c91

2번 결과: /Users/chasoik/Projects/image-prompt/outputs/uniform-costume-qualification-20261004/arm-a/snapshot-2/zouave-native-attempt-2.png

원본 tool 경로: /Users/chasoik/.codex/generated_images/01a10547-e6a7-7ad2-a78c-a36e4273cbdd/exec-f497dc82-8a1d-409c-9b34-11fb749f1d30.png

SHA256: 4c03f980e26f66fc4508daadc436b238df5efff20a0751443dc37d9f6716d1a1

정확한 audit/runtime prompt bytes는 snapshot-2/final_prompt.txt, runtime_prompt.txt 및 attempt-2 suffix 파일에 각각 보존했습니다. Runtime SHA256은 첫 13e324023efaab0782f50cb0650cda1fa13862e8338a22637fcd6acbfbcba631, 수정 32cb7ab89dca0ba0b78e362817da16260828aa2a39709cf107f2556b97c1b730입니다. Effective visual contract는 두 번 모두 9792cbe28f926ba9ab97c2f10defaed2a0b6a3d24bcd0c6baf0a6fd8ae388219입니다.

주요 기록은 arm-a/image_runs.ndjson, snapshot-2/native_invocation*.json, run_manifest-attempt-*.json, source_hashes*.json, snapshot_source_manifest-final.json, parent_bound_visibility_repair.json, active_compiled_gate_set*.json, pixel-review-attempt-*.json, native_render_review-attempt-*.json, pixel-audit-attempt-*.json, integration_trace-final.json 및 final_preservation_verification.json입니다. 초기 retrieval/adoption 실패와 최초 compiled/supplemental gate/첫 실패 이미지는 덮어쓰지 않았습니다.
