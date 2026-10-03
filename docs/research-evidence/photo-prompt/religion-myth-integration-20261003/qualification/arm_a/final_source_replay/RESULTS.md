최종 소스 후보 노출 재검사는 PASS입니다. 동결 원문·core·controls·embodiment와 seed 297620939를 그대로 사용해 진단용 v6 팩을 1회 생성했습니다. 원래 이미지 생성에 사용한 팩은 1개이며, 이번 별도 팩은 이미지 생성에 사용하지 않았습니다.

| 검사 대상 | 생성 당시 노출 | 최종 소스 노출 |
|---|---|---|
| `ri_daoist_robe_xuanwu` / `visual-concept:ri_daoist_robe_xuanwu` | 확인 | 확인 |
| `ri_body_mandorla` / `visual-concept:ri_body_mandorla` | 확인 | 확인 |
| `slot:composition:ri_daoist_robe_xuanwu_readable_composition` | 확인 | 확인 |
| `slot:composition:ri_body_mandorla_readable_composition` | 확인 | 확인 |

두 프로파일은 최종 데이터의 `activation.semantic_discovery_requires_component_evidence=true`와 좁은 한국어·영어 대체 표현이 적용된 상태에서도 선택적 후보로 노출되었습니다. composer view와 실제 후보 상세에서 동일 ID를 확인했습니다. 이 재검사에서는 새 후보 채택이나 프롬프트 재작성을 하지 않았습니다.

생성 당시 스냅샷의 composed·runtime 감사는 두 시도 모두 PASS이며, 저장된 원본 픽셀의 최종 판정은 **FAIL을 유지합니다**. 만돌라의 아래 뾰족한 끝이 발 아래까지 전신을 완전히 둘러싸는 관계를 확인할 수 없고, 더 엄격한 사전 작성 테스트인 거북의 짧은 꼬리 연결은 UNOBSERVABLE입니다. 실패 gate는 `vo_ri_body_mandorla_1`, `vo_ri_body_mandorla_2`, `embodiment_visibility_and_projection`입니다. 최종 소스 후보 노출 결과는 이 이미지 실패 판정을 바꾸지 않습니다.

머리 두광의 등록 프로파일 `ri_head_halo`는 생성 당시와 이번 최종 소스 팩의 visual-concept 목록 모두에 노출되지 않았습니다. 최종 팩에는 `slot:composition:ri_head_halo_readable_composition` 구도 후보가 있으나 이번 재검사에서는 채택하지 않았습니다. 기존 이미지의 머리 원반 PASS는 사전에 동결한 agent-owned 픽셀 gate만을 근거로 합니다.

추가 이미지 호출은 0회이며, 기존 2회 원장의 bytes와 이미지·standalone prompt·negative·runtime request·감사·리뷰를 포함한 원래 산출물의 SHA-256이 모두 보존되었습니다. 기존 감사는 현재 소스에 재실행하거나 덮어쓰지 않았습니다. 두 단계의 source binding은 서로 별도로 기록했습니다.

생성 당시 팩 ID는 `7cdd848904005037`, `core_retrieval_sha256`은 `52db4c4d1aa760769aa3a002af05a127f7605678541b50089403b60e89c96c54`입니다. 최종 소스 진단 팩 ID는 `203363f124620f23`, `core_retrieval_sha256`은 `145dac2a8f0aba2de0708e96ae1c953b3c9854de6418bf6cd7977a9e2b10d198`입니다. core·intent lock·controls·embodiment canonical hash는 서로 동일합니다.

근거 파일:

- [최종 소스 팩](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/final_source_replay/candidate_pack.json)
- [composer view](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/final_source_replay/composer_view.json)
- [실제 후보 상세](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/final_source_replay/candidate_details.json)
- [노출·binding·보존 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/final_source_replay/replay_exposure.json)
- [별도 무결성 검증](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/final_source_replay/replay_integrity.json)
- [생성 당시 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/RESULTS.md)
- [기존 픽셀 리뷰](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/pixel_review.json)
- [시도 1 원본 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/attempt_1.png)
- [시도 2 원본 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/attempt_2.png)
- [시도 1 exact standalone prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/standalone_prompt.txt)
- [시도 2 exact standalone prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/standalone_prompt_attempt_2.txt)
- [기존 이미지 호출 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/religion-myth-integration-20261003/qualification/arm_a/image_runs.ndjson)
