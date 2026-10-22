# 기존 소스와의 구체적인 비교

## 감사 범위와 해석

첫 고정 필드 감사는 19,471개 레코드, 13,644개 바인딩, 59개 모듈을 읽었다. 감사 도중 모듈 변화는 []였고 manifest 변화는 False였다.

추가 의미 비교 시점에는 19,559개 레코드가 있었다. 동시 작업에 의한 시점 차이다. 두 스냅샷을 동일한 현재 상태라고 합치지 않는다.

검색한 지정 필드는 en/ko/definition/phrase/composition/runtime expression이다. alias·tag·연구 주석·별도 negative metadata는 제외했지만, 선택 필드 안의 문장 자체에 부정·진단·문맥이 있을 수 있다. 따라서 모든 hit가 긍정 시각 후보라는 가정도 하지 않는다.

키워드 130개 중 89개는 이 제한된 literal 검사에서 0이었다. 의미 부재·새 후보 필요·H-F2 미노출의 증거가 아니다. 키워드 분할 방식과 표기의 영향도 있다.

첫 목록은 manifest 순서와 짧은 양성 원문을 이용한 진단 표본이다. relevance rank나 top8 결과가 아니다. 별도의 17개 의미 이웃은 원문·조건·효과·바인딩의 지정 필드를 읽고 아래와 같이 비교했다. 전체 코퍼스 동치 검토·원전/native 승인까지 완료했다는 뜻은 아니다.

## 17개 의미 이웃

| CID | 연결 초안 | 판단 | 근거와 남은 차이 |
|---|---|---|---|
| cand_226dbc8b671c52d192f8bec5b04e2e1a | C01 | reuse_base_then_review_explicit_delta | 이미 닮은 얼굴·옷, 다른 손동작, 독립 위치를 담는다. 연구안의 특정 손 자세·코트·개별 접지는 강화분이다. |
| cand_95b8bff50eb257ebacb87d2234ba51e2 | C01 | refine_or_choose_existing_variant | 연속 바닥과 두 성인 위치를 담는다. 다른 손동작까지 같은 source에 있는지 별도로 심사한다. |
| cand_ce7b80fdc8f55da78b01b8a61ab3946d | C05 G01 | reuse_base_then_review_explicit_delta | 잔존 사지–소켓–보철 구간은 이미 있다. 분리 부품·기어·피부 재질을 임의로 덧붙이지 않는다. |
| cand_4bf6edf0f73a53208c3a6c5616f12398 | D01 | context_guard_preserve | 빈 캐릭터 시트 등 TTRPG 소품이며 ttrpg_practice 조건이 있다. 능력치 칸을 조작하는 세계 내부 시트와 자동 동치가 아니다. |
| cand_105315097a755bbe9b04a7918ef5add8 | D01 D02 D08 | refine_not_equivalent | 실제 광택 면을 가진 휴대 화면 소품이다. 표시·대상·가시성·의미의 진실성을 추가로 바인딩해야 한다. |
| cand_3bcf055a0fc65bc086785a701bedfa28 | B02 | reuse_redaction_base | 문서·텍스트·검열 막대의 물리 관계를 재사용 가능하다. 초상·이름 소멸·정사 개정은 추가 문맥이다. |
| cand_7ab76deb4e4257079391fc1dfc59c9a7 | B02 | duplicate_neighborhood_review | 다른 모듈의 검열 문서와 겹친다. 신규 등록 전 두 원문의 범위·조건·효과를 비교한다. |
| cand_88cfb33603915893a445d0cfa975e22f | B03 B05 | refine_or_variant | 같은 식별자와 다른 도식의 문서 비교가 있다. 지도·인원 개수·문/벽 차이는 새롭게 제한한 실현이다. |
| cand_b99c238a660a5456a449f51519650678 | B02 B05 B08 | reuse_material_distinction | 아래 흔적과 위 글씨의 중첩이라는 팔림프세스트 관계다. 검열·역사 개정·세계 생성과 동치로 합치지 않는다. |
| cand_dc1d9e9da9cc5dc997e7e73a30a8a16f | B04 H04 | refine_or_variant | 두 기록과 빠진 이름/얼굴, 공통 식별자 관계가 이미 있다. 실제 인물·명찰·현재 벤치를 더하면 별도 효과다. |
| cand_2d2f38385dde51a0b2d1bf2f405a8bf2 | B05 B08 | reuse_text_edit_base | 취소선과 삽입 위치의 관계는 재사용 가능하다. 메타서술·레트콘의 인과로 확대하지 않는다. |
| cand_7f66aaa8a21854ab9a80cb19e98a96fe | B05 F07 | reuse_absence_base | 벽의 문 크기 흔적과 연속 걸레받이 관계다. 삭제의 원인·이전 문 존재·소프트락은 별도다. |
| cand_f850b68409b05e9a94b67b2dd004972c | D04 D07 | context_guard_preserve | 퀘스트 물증·보상·이의 검토 행동과 status_system_quest_evidence_scene 조건이 있다. 일반 행동으로 확장하지 않는다. |
| cand_cfbed1a0d52d5af9add84e04a64baeba | D04 | reuse_prop_set_with_conditions | 퀘스트 판·저울·납품 기록·통행 서류 세트다. 삼각 표식과 봉인 물품의 정확한 대응은 추가 실현이다. |
| cand_780edb3a55e9595d950384aaaf7797e6 | D04 D07 | reuse_prop_set_with_conditions | 봉인 퀘스트 토큰·증거 케이스·보상 선반이 있다. 손–물건–빈자리의 현재 관계를 별도로 심사한다. |
| cand_f8e4aa3ec92d5463a0eee8e6b6cefafc | F03 F04 | different_owner_not_equivalent | 반사 속 와이어프레임/기계 골격이다. 실제 벽의 고체–메시 경계와 소유 매체가 다르다. |
| cand_8e61383ef2e454b19e9fa25cab1ce5df | B02 B03 G06 | reuse_chart_base | 연결선이 지워진 관계도와 남은 이름 표식. 혈연·생식·강제 실험·삭제 인격으로 확정하지 않는다. |

완전 원문·조건·효과·바인딩·레코드 SHA는 [reviewed-neighbors.json](reviewed-neighbors.json)에 있다. 40개 초기 표본은 [existing-source-mapping.json](existing-source-mapping.json)에 별도로 보존했다.

## 어휘 오탐을 의미 공백으로 오해하지 않기

- `quest`가 `request` 안에 매치되던 초기 정규식을 단어 경계로 제한했다. 교정 후 world_interface 가족의 literal hit는 23개다. 그중 홀로그램 팔레트·스티커·광택 필름은 작중 상태창과 다르다.
- `checkpoint`의 표본은 검문소였고 `inventory`는 선반 재고일 수 있었다. 이것을 게임 저장점·인격 수납으로 채택하지 않는다.
- `평판`은 평평한 태그를 뜻하는 원문에도 등장했고 `말소`는 말소리의 일부일 수 있다. 말소리 오탐은 최종 패턴에서 제외했다.
- `miniature`는 조상 초상 소품·틸트시프트 도시 구도일 수 있고 `frame`은 화면 밖 인물이나 물리 프레임 부품을 가리킬 수 있다. 재귀/서사 침범의 존재 증명이 아니다.
- `texture`의 한국어 텍스처 일치에는 먼지·기어·오일 등 일반 표면이 포함된다. 실제 공간의 누락 재질과 구별한다.
- diagnostic 레코드와 visual_profile은 단순 visual_option과 다른 종류다. 전체 레코드 수와 search metadata의 문서/RID 수는 직접 비교하지 않는다.

## 채택 판단

새 데이터의 우선 가치는 단어 수보다 비교 기준점·소유 매체·양쪽 끝점·연속 경계의 정밀화다. A01/A03/A04/E01/E02/F03처럼 새로운 관계를 제안한 항목도 전체 유사 소스를 검토하기 전에는 확정 new가 아니다. 문서 불일치·두 인물·의수·퀘스트 소품은 특히 기존 모듈과 공동으로 심사한다.

이 조사에서는 기존 레코드나 모듈·인덱스를 수정하지 않았다. 후속 구현은 최신 source baseline을 다시 잡고 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)를 따른다.
