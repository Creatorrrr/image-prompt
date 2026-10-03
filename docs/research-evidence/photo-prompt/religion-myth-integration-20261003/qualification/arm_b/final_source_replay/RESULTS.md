최종 소스 replay에서는 **두 구도 후보의 노출은 유지됐지만, 두 시각 프로파일의 노출은 유지되지 않았다**. 이는 최종 source retrieval 검증이며 기존 생성 당시 snapshot의 픽셀 판정과 분리한다. 기존 이미지 전체 판정 **FAIL**을 그대로 유지했다.

동결된 원문·authorial core·creative controls·baseline embodiment 파일을 수정하지 않고 한 번만 별도 v6 pack을 생성했다. 최종 소스 pack ID는 `5401e2b2a428ead0`, 생성 당시 pack ID는 `2983d23e47c6eac8`다.

| 확인 ID | 최종 pack 노출 | 상태 |
| --- | --- | --- |
| `slot:composition:ri_siren_human_bird_readable_composition` | 예 | eligible |
| `slot:composition:ri_chimera_topology_readable_composition` | 예 | eligible |
| `visual-concept:ri_siren_human_bird` | 아니오 | ID 부재 |
| `visual-concept:ri_chimera_topology` | 아니오 | ID 부재 |
| clarification profile `ri_siren_human_bird` | 아니오 | ID 부재 |
| clarification profile `ri_chimera_topology` | 아니오 | ID 부재 |

새 프로파일의 `semantic_discovery_requires_component_evidence=True` 및 좁은 한국어·영어 대체 표현 추가는 root가 전달한 최종 소스 변경 조건이다. 이 arm은 두 프로파일의 부재를 실제 pack에서 확인했으며, 그 부재의 원인을 확정하거나 동결된 입력을 새 의미로 고치지 않았다. 추가 pack 생성도 하지 않았다.

생성 당시 pack·composed/runtime 요청·감사·원장·manifest·원본 PNG 2개·각 시도 prompt·negative·pixel review·원래 RESULTS.md 등 **23개 기존 파일의 SHA-256이 replay 전후 모두 동일**하다. 두 PNG와 최종 standalone prompt의 exact bytes를 그대로 보존했다. 후속 이미지 호출은 **0회**, 누적 네이티브 호출은 계속 2회다.

핵심 몸 접합이 읽힌다는 생성 당시 관찰과, 왼쪽 날개 외곽 잘림으로 인한 `whole_structure_visibility=UNOBSERVABLE` 및 전체 FAIL도 변경하지 않았다. 최종 소스 pack은 이미지 검증 결과를 새 소스의 렌더 성공으로 전환하는 근거가 아니다.

- [최종 소스 별도 pack](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_b/final_source_replay/candidate_pack.json)
- [최종 소스 overview](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_b/final_source_replay/composer_view.json)
- [ID 노출·bindings·23개 보호 파일 hash 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_b/final_source_replay/exposure_check.json)
- [replay 전 입력·기존 파일 hash](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_b/final_source_replay/input_preservation_before.json)
- [생성 당시 RESULTS](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_b/RESULTS.md)
- [보존한 최종 생성 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_b/image_attempt_2.png)
- [보존한 최종 prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_b/standalone_prompt.txt)
- [보존한 최종 pixel review](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_b/pixel_review.json)
