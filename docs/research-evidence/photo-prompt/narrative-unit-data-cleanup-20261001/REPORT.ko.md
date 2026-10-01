# 관할 세계의 기존 구분을 최종 후보에 보존

세 개의 장문 narrative_core 제안 중 spirit_jurisdiction_narrative_core 한 행만 채택했다. 기존 영어 문장을 그대로 담은 concept_units 하나를 추가했으며, 라벨·aliases·embedding_text·tags·facets·weights·기존 guard는 바꾸지 않았다. 이전 cycle10의 기록 장면 수정도 그대로 유지했다.

원래 문장은 한 장면의 창작 관할 전통을 하나로 유지하고 한국 저승 인도, 중국 지역 수호, 일본 괴이 기록을 하나의 교리로 합치지 않는다는 관계를 표현한다. 기존 28단어 라벨은 명시적 unit이 없어 최종 V6에서 순서 없는 단어로 바뀌었다. 실제 production pack과 검증된 detail에서는 이번 추가로 원래 문장 전체가 optional, concept-only 단위로 보존된다. 중간 helper 단어 목록만 검사한 결론이 아니다. 한국어 source/localization/search는 그대로이며, 최종 한국어 coverage 증가를 주장하지 않는다.

## 세 제안 중 두 개를 되돌린 이유

처음에는 management_world_narrative_core와 media_mix_narrative_core에도 각각 기존 문장을 unit으로 추가했다. 정착지와 던전의 역할 구분, 장르·제작 노동·매체 정체성의 구분이 최종 표면에 복원되는 실제 장점은 있었다. 그러나 전체 제안의 dense 진단에서 다음 부작용이 발생했다.

- 관할 기록보관소 견학 질의 n06에서 management_world가 새로 4위에 진입
- 관리 체계를 혼동하는 질의 n10에서 media_mix가 새로 5위에 진입
- management/media의 한국어 혼동 대조 질의 cosine도 상승

새로 노출된 후보의 관련성이 충분히 뒷받침되지 않고 자연 질의의 실제 채택 검증도 없으므로, 의미 표면 개선이 이 손해를 분명히 상쇄한다고 판단하지 않았다. 두 행은 모든 필드를 baseline 그대로 복원했다. 문제가 해결되었거나 원래 표현이 충분하다고 분류하지 않고 미해결로 남긴다. 전체 제안·벡터·측정·원본 API 기록은 보존했다. 결과에 맞춘 문구 재작성이나 추가 API 호출은 없었다.

## 최종 한 행의 측정 결과

수정 전에 9개 행과 22개 질의를 고정했다. 18개는 독립 검토자가 작성한 영어·한국어 양성, 혼동 대조, 공존 진단이고 4개는 인접 세계 메커니즘 통제군이다. 모두 공개적으로 검토 가능한 작성 진단이며 blind holdout이 아니다.

- 양성 6개와 일반 통제군 4개는 두 방식 모두 대상 1위를 유지
- 관할 세계의 영어 공존 질의 n05는 dense 2→1위, lexical 3위 유지
- 혼동 대조 6개는 dense와 lexical에서 모두 여전히 대상 1위다. 혼동 분류나 배제 문제를 해결한 결과가 아니다
- 모든 lexical top5 ID 순서가 동일하다
- Dense top5는 n05의 1·2위 순서 변경과 n13의 5위 교체만 남는다. 미디어 양성 질의 n13에서 spirit가 5위 밖으로 내려가고 aristocratic이 들어온다. 교체 후보가 이상적인 정답이라는 주장은 하지 않는다
- 전체 제안의 n06/n10 management/media 신규 진입은 최종 subset에서 사라진다
- spirit 양성 cosine은 낮아졌지만 1위는 유지한다. 모든 점수가 좋아졌다거나 모든 후보 순서가 동일하다는 주장은 하지 않는다

단일한 창작 시각 전통 안에서 다양한 출신의 방문객이 공존할 수 있다는 원래 범위를 유지한다. 새로운 전역 금지, parser, schema, 검색 로직, 영향 차원 선언이나 guard는 추가하지 않았다. 실제 자연 노출·채택·이미지 품질은 검증 범위 밖이다.

## 검증과 재현

독립 검토가 전체 제안 88개 및 최종 subset 44개 결과 행, 실제 source/index/BM25/cache와 최종 후보/detail을 확인했다. 현재 index는 문서 10,174개 중 새 벡터 1개와 정확한 baseline 벡터 재사용 10,173개로 구성된다. 두 rejected 행과 모든 bundle은 baseline 그대로다.

원본 evaluate_cycle.py는 당시 세 행 전체 제안용 실행 기록이다. 게시된 subset에서 전체 baseline·제안·채택 결과를 API 없이 재현하려면 같은 디렉터리의 replay_acceptance.py --replay를 사용한다. 이 runner는 네트워크 분기가 없으며 132개 결과 행과 현재 물리 index를 검증한다. 최종 source의 이전 capture 질의 8개와 기존 role 질의 3개도 별도로 재생했다.

전체 세 행 제안에서 203개 관련 테스트가 통과했으나 이는 최종 subset 통과 수로 재사용하지 않는다. 최종 subset에서는 DATA/public/background 174개와 의미·CJK·profile-index 15개, 총 189개가 통과했다. 결과는 accepted-*.log에 분리한다. 기존 지역 평판 fixture는 social recognition 후보가 7위여서 요구 top6에 들지 못하는 baseline 실패가 있으며, 그 기대값을 바꾸지 않았다. 최종 role 모듈 8개 중 7개는 통과하고 해당 1개만 실패했으며, 수정 전후 세 질의의 top12 ID 순서가 동일하다. 수용 요약의 표현을 정확히 고친 뒤 hash-bound 테스트 16개를 다시 실행해 통과했다. 전체 저장소 green이나 CI 통과를 주장하지 않는다.

## 비용과 공개 단계

문서 3개와 질의 22개, 총 25개 입력이 각각 한 번 성공했다. 전송량은 9,282 UTF-8 bytes이며 추가 비용의 보수적 상한은 $0.04096, 추적 누적 상한은 $1.2075008이다. 최종적으로 사용하지 않은 두 문서 벡터의 비용도 포함한다. 청구서 실측이 아니며 별도 upstream 계정 사용액과 대조하지 않았다. subset 선정·복원·재생에는 추가 API 호출이 없었다.

최신 origin/main pull, 적절한 후속 검사, 정상 push 및 정확한 remote commit/CI 확인은 publication 단계에서 별도로 수행한다. 원래 reef trial의 deferred 상태는 이 변경과 무관하며 그대로 유지된다.
