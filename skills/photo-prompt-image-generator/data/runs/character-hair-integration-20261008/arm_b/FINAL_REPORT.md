B 실행은 완료됐으며 첫 이미지와 보정 이미지 모두 원래 B1–B5 **ALL_OF FAIL**입니다. 실제 built-in native 호출은 **2회**(초기1+허용된 보정1)이고, 두 원본·리뷰·ledger를 보존했습니다. 공식 보정 리뷰 감사는 `PASS / record_valid=true`, 픽셀 기술 적합성은 `fail`입니다. 사용자 선호·수락은 아직 받지 않았습니다.

독립 컨셉은 비가 샌 식물 온실에서 마지막 젖은 식물 표본지를 나무 건조 프레스에 옮기는 작업 초상입니다. seed는 `3927461530`. 초기 컨셉·다섯 관찰 조건을 후보 데이터 접근 전에 동결했습니다. 첨부 사진은 보이는 얼굴 인상만 참고했고 머리 형태는 agent proposal로 두었습니다. 보정은 검증된 닫힌 계약에서 땋기 시작·끝 접합, 은색 장식의 접합 위치, 카메라 방향·높이만 변경했습니다. 원문 사용자 요청·다섯 조건·참고 사진·설정은 유지됐습니다.

설정은 sensual1/fetish0/creativity1/surreal0, emphasis auto→sensual_led, reference_edit_mode off, viewer_experience false, trend off입니다. 같은 controls hash `d3542ea44f81683d9d069ceae86ba5ef78159792dd045690063cb02bb27be8cf`를 사용했습니다.

| 원래 조건 | 첫 이미지 agent | 보정 agent | 보정 root 독립 리뷰 |
|---|---|---|---|
| B1 한쪽 낮은 묶음·연속 꼬리·윗가슴 끝점 | PASS | FAIL | FAIL |
| B2 관자놀이 시작의 세 가닥 땋기 | FAIL | FAIL | FAIL |
| B3 땋기 끝→같은 묶음 뿌리의 보이는 연속 접합 | UNOBSERVABLE_NOT_PASS | UNOBSERVABLE_NOT_PASS | UNOBSERVABLE_NOT_PASS |
| B4 뿌리의 cobalt 천 리본·매듭·두 loop/두 짧은 끝 | PASS | UNOBSERVABLE_NOT_PASS | PASS |
| B5 뿌리 바로 위 금속 crescent·모발 접촉 | FAIL | PASS | PASS |
| ALL_OF | FAIL | FAIL | FAIL |

보정에서는 은색 장식의 위치와 접촉이 읽히지만 땋기 시작이 여전히 crown 쪽이며, 끝 접합은 귀·머리·리본 뒤에 가려집니다. 꼬리 끝도 지정 윗가슴보다 아래입니다. B4의 접힘/겹침을 두 loop와 두 끝으로 읽을 수 있는지는 두 리뷰가 달랐으며 두 원본 리뷰를 각각 보존했습니다. agent의 해부학적 좌우 해석은 추론임을 비교 파일에 별도 한정했고, 보이는 꼬리 끝점만으로도 B1 FAIL이 성립합니다. 서로 다른 이미지의 성공 요소를 합쳐 통과로 만들지 않았습니다.

실제 헤어 검색은 두 pack 모두 `core_bm25f`의 BM25F/RRF입니다. sensual contextual lane의 `keyword`/`semantic_candidate_coverage=0`은 그 별도 lane에만 해당합니다. 초기에는 `sca_h09`를 complete owner/base-tail 계약으로 채택했고 신규 main-daenggi candidate/bundle은 노출됐지만 채택하지 않았습니다. 보정에서는 crown 경로인 `sca_h10`만 헤어 후보로 노출돼 거절했고 optional 후보를 채택하지 않았습니다. 원하는 `chrh_hair_topology_three_strand_braid`와 `appearance_h106`는 두 pack에 모두 노출되지 않았습니다. sca_h09/10의 추가 paraphrase는 source에 존재하지만 public pack에는 새 문구가 literal로 실리지 않습니다. 기존 동등 semantic units/entry 노출과 추가 문구 노출을 구분했습니다. 예전 데이터 버전으로 렌더한 비교군이 없으므로 데이터 보강이 검색·픽셀 개선을 일으켰다는 결론은 내리지 않습니다.

시험한 immutable runtime generation은 `0a3b19f34fb2ef66f6406cbf4f38c9aac196ebc515b8bb918aa2d1c16fc40000`입니다. 이후 primary metadata 발행과 이 frozen 시험 결과를 구분합니다.

- [첫 원본 PNG](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/results/attempt_1.png): SHA `4a3381a18a73dc1d3a0c507eb440d11434be59b27453862da31bf976d643f0f3`, native1024×1536.
- [보정 원본 PNG](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/results/attempt_2.png): SHA `b49dc76f528a6e726b9d0308688307ef03e6511a402386d738e85c87a87752ca`, native1237×1272.
- [첫 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/final_prompt.txt), [보정 프롬프트](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/repair_1/final_prompt.txt).
- [첫 pack9b1598f9e77eb8fb](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/revisions/ed8e7c04fd794de8a4d51f249bc245ea/pack.json), [보정 packacebd051d2119606](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/repair_1/revisions/9c3dedcc2d6f4bcaa494375d9b8aa60b/pack.json).
- [보정 agent5조건 리뷰](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/native_hair_review_2.json), [root 리뷰 원본 보존본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/peer_root_repair_review.json), [두 리뷰 비교](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/review_comparison_2.json), [공식 리뷰 감사](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/repair_1/revisions/11d7491bfe4c4f7990e4dcdba122f5fe/review_audit.json).
- [ledger2행](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/image_runs.ndjson), [누적2회 manifest](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/run_manifest.json), [보존 증거](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/manifest_attachment_evidence_2.json), [source/index→노출→선택→prompt→pixels 전체 경로와 해시](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008/arm_b/evidence_chain.json).
