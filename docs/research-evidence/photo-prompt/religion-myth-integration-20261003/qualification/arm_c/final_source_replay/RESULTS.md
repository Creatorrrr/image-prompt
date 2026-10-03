최종 소스의 후보 노출 재검사는 통과했습니다. 이 결과는 기존 이미지의 픽셀 검증과 별개의 retrieval 증거입니다. 두 기존 이미지의 전체 판정은 계속 **FAIL**이며, 당시 exact 이미지·프롬프트·negative·감사·원장 bytes를 모두 보존했습니다.

동결 원문, authorial core, creative controls, embodiment review를 그대로 사용해 이 디렉터리에 별도 v6pack을 정확히 한 번 만들고 실제 composer view를 조회했습니다. 새 이미지 호출은 0회이고, 새 프롬프트 구성·runtime 감사·기존 산출물 교체도 수행하지 않았습니다.

| 이전 채택 source entry | 최종 팩 노출 ID | 결과 |
| --- | --- | --- |
| `moirai_spin_measure_cut_action` | augmentation:adult_appeal:sensual:action:moirai_spin_measure_cut_action | PASS: 기존 노출 ID 유지 |
| `axis_mundi_connection_aesthetic` | augmentation:adult_appeal:sensual:aesthetic_trend:axis_mundi_connection_aesthetic | PASS: 기존 노출 ID 유지 |

위 후보 두 개는 최종 팩에도 노출되며 candidate adoption은 `optional`을 유지합니다. 이번 단계에서 새 채택은 하지 않았습니다. 기존 core가 정한 모이라이의 한 생명실과 세 역할, 세계축의 삼계 연결 의미는 그대로입니다. 후보 노출의 `context_preflight`는 새 이미지나 구성 검토를 요청받지 않았으므로 `unassessed`이며 픽셀 성공을 뜻하지 않습니다.

기존 프로파일 노출 8개 중 `ri_chakra_white2`가 사라졌고, `bottom_hourglass_silhouette_relation`가 대신 노출되었습니다. 최종 팩에 노출된 `ri_*` 프로파일은 0개입니다. 기존·최종 후보 catalog는 각각 113행, 105개 고유 ID입니다. 프로파일은 양쪽 모두 8개이고 실제 채택은 모두 0개입니다. 새로운 체형 프로파일도 미채택이며 참조 인물의 체형 추론에 쓰지 않았습니다. 전체 ID 차이는 [비교 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/final_source_replay/retrieval_comparison.json)에 남겼습니다.

현행 religion-iconography 원본의 54개 프로파일 모두 `semantic_discovery_requires_component_evidence=true`입니다. 좁은 한국어·영어 표현도 현행 소스에서 확인해 [프로파일 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/final_source_replay/final_profile_source_evidence.json)에 저장했습니다. 예컨대 `ri_chakra_white2`는 별도 배우자와 가슴에서 교차한 도구를 명시합니다. 과거 source 원본 전체는 새로 복원하지 않았으며, 과거 노출은 보존된 생성 당시 팩과 composer view로 비교했습니다.

`slot:composition:ri_heart_maat_figure_readable_composition`와 `bundle:ri_heart_maat_figure`는 계속 노출되지만 기존 거절을 유지합니다. 이 변형은 반대편 접시에 앉은 마아트 소상을 두고 그 머리에 깃털 표식을 귀속시킵니다. 동결 장면은 심장과 깃털 자체를 서로 다른 접시에 두므로 대체할 수 없습니다. 일부 구성만 분리해 원래 사건 의미로 바꾸지 않았습니다.

| binding | 생성 당시 | 최종 retrieval replay |
| --- | --- | --- |
| pack ID | `37dc2140e374ad65` | `b43cac64ae0c98f7` |
| core retrieval SHA256 | `223e54d9fb5a0c730602a209ff0ebe6dacd39773534d196b550049efdbb82936` | `efd490b5122eadf1bc7d3daf71fa6ed4b25a99021bb4c4fa497032d5958566e7` |
| slot corpus SHA256 | `d4797bb565665abebd922fa9f2141153db69ef5986503caab72c05e08c244b6e` | `f7a8ef1b3594392cc0345d308ae257e85b9022484dea7c370cce17bb32f9d24a` |

정규화 authorial core, intent preservation, request query, creative controls, embodiment preflight, baseline review, whole-scene query 및 active slot query binding은 모두 동일합니다. 데이터 변경으로 pack 및 corpus/retrieval hash만 갱신된 별도 증거입니다. 41개 보호 파일의 재해시에서 전부 bytes 불변을 확인했습니다. 원래 원장은 2행, 이미지 생성은 누적 2회 그대로입니다.

생성 당시 1·2차 리뷰는 각각 PASS 7개, FAIL 3개, UNOBSERVABLE 2개였습니다. 실제 방적, 자르는 단일 실의 절단, 동일 실 소유·연결 관계가 실패했고, 고인과 심장의 동일 소유 및 토트 펜촉의 기록 접점은 관찰 불가였습니다. `partial_is_fail=true`에 따라 두 전체 FAIL을 보존합니다. 사용자 선호와 신원 일치는 평가하지 않습니다.

이미지 원본 SHA256은 1차 `0dc374a92221887cb959bce025bc76af3330216980ff0ace03ea4c843331150b`, 2차 `1a2ea776cfe0459c9df41762a991acf521654f98c5d2a8088bb95717394d3a70`입니다. 이미지·exact 프롬프트·negative의 각 hash와 41개 불변 검사는 [integrity.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/final_source_replay/integrity.json)에 있습니다.

최종 retrieval 산출물: [별도 팩](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/final_source_replay/candidate_pack.json), [실제 composer view](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/final_source_replay/composer_view.json), [비교 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/final_source_replay/retrieval_comparison.json), [동결 입력 binding](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/final_source_replay/input_binding.json).

보존된 생성 당시 산출물: [원래 결과 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/RESULTS.md), [1차 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_01/image.png), [2차 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_02/image.png), [2차 exact 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_02/standalone_prompt.txt), [2차 pixel review](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_02/pixel_review.json), [2차 composed audit](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_02/composed_audit.json), [2차 runtime audit](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/attempt_02/runtime_audit.json), [원래 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_c/image_runs.ndjson).
