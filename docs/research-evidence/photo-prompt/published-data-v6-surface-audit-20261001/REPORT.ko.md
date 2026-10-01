# 게시된 DATA 58개 행의 최종 V6 표면 검토

최종 V6 후보는 중간20-term projection에서 끝나지 않는다. build_candidate_pack이 완전한 entry에서 semantic_source를 연결하고, 뒤의 apply_public_semantics가 concept_units·relations를 복원하며 concept_terms를 concept_units로 교체한다. compose_pack_view의 detail도 이 최종 후보를 해시로 묶어 반환한다.

58개 게시된 변경을 각각 과거 frozen 행과 현재 행으로 비교했다. 실제 rule-mode generator로 유효한 core/control/embodiment 계약을 만든 뒤, 한 후보가 보이는 조건을 trace에서 통제하여 실제 production pack builder와 detail 검증을 실행했다. 자연 질의에서 그 후보가 검색되거나 채택된다는 실험은 아니다.

첫58개×2 상태 실행에서 mirror_selfie, poised_standing, harbor_fisherman은 양쪽 모두 singleton-to-authorial-opening 정책에 따라 표시되지 않았다. 나머지55개는 실제 최종 후보/detail로 확인했다. 이 세 행은 같은 유효 계약과 바뀌지 않은 두 번째 선택지를 둔 추가6개 pack 실행에서 표시됐으며 detail 해시도 통과했다. singleton 정책을 끄거나 필수 concept/subject/event 잠금을 완화하지 않았다.

최종 비교는 다음과 같다.

- 27개 owner 관계 수정이 실제 최종 relations와 detail에 그대로 남는다
- 우산·말없이 함께 앉기·glitter의 영어 문구 수정3개는 concept_units/concept_terms에 남는다
- 다른28개 행의 최종 후보 의미 표면은 같다. source/index 변경이 모두 public prose로 복사된다는 뜻은 아니다
- 표시된 후보에서 새로운 의미 손실은 발견하지 않았다. 이 범위는 조건부 serialization 검증이다

## 한국어 범위 설명 정정

crochet와 harbor의 한국어 라벨은 source와 localize 결과에 존재하고 검색 index에도 기여한다. 앞선 lexical 진단 이득은 그대로다. 다만 label_en/label_ko를 바꿔 얻은 한국어 단어 추가는 중간 projection에서만 관찰됐다. 최종 semantic_source는 변경되지 않은 영어 label을 사용하고, 뒤의 overlay가 중간 단어를 덮어쓴다. 따라서 최종 V6 한국어 concept coverage가 늘었다는 이전 설명은 철회한다. 데이터 변경을 되돌릴 이유가 되는 최종 표면 손실은 이 두 행에서 발견하지 않았다.

원래 intermediate JSON과 frozen 질의·원안·API 기록은 그대로 보존한다. 이번에 고친 것은 검증 단계와 효과를 설명하는 범위다. 별도 미게시 실험은 이 문서에 제안 데이터로 포함하지 않았다.

API 호출0회, source/index 변경0개. 실제 request 노출·선택·이미지 품질이나 전체 저장소 green을 주장하지 않는다.
